"""Async Azure OpenAI client factory with retry, structured output, and rate-limit protection."""

import asyncio
import base64
import logging
import time
from typing import Any

from azure.identity import DefaultAzureCredential
from azure.identity import get_bearer_token_provider
from config import Settings
from openai import AsyncAzureOpenAI

logger = logging.getLogger(__name__)

_client: AsyncAzureOpenAI | None = None
_client_2: AsyncAzureOpenAI | None = None
_client_3: AsyncAzureOpenAI | None = None
_clients: list[AsyncAzureOpenAI] = []
_call_counter = 0

_llm_semaphore = asyncio.Semaphore(200)


def _get_round_robin_client() -> AsyncAzureOpenAI:
    """Return client via round-robin across all available endpoints."""
    global _call_counter
    _call_counter += 1
    if _clients:
        return _clients[_call_counter % len(_clients)]
    return _client  # type: ignore


def detect_mime_type(image_base64: str) -> str:
    """Detect image MIME type from base64-encoded content.

    Checks the magic bytes at the start of the decoded data to determine
    the actual image format, regardless of what the caller thinks it is.
    """
    try:
        raw = base64.b64decode(image_base64[:32])
        if raw[:2] == b"\xff\xd8":
            return "image/jpeg"
        if raw[:4] == b"\x89PNG":
            return "image/png"
        if raw[:4] == b"RIFF" and raw[8:12] == b"WEBP":
            return "image/webp"
        if raw[:3] == b"GIF":
            return "image/gif"
        if raw[:2] in (b"II", b"MM"):
            return "image/tiff"
        if raw[:2] == b"BM":
            return "image/bmp"
    except Exception:
        pass
    return "image/png"  # safe fallback


def get_client(settings: Settings) -> AsyncAzureOpenAI:
    """Return a cached AsyncAzureOpenAI client (app-scoped singleton).

    Uses DefaultAzureCredential for auth. Creates up to 3 clients for
    round-robin load-balancing across AOAI endpoints.
    """
    global _client, _client_2, _client_3, _clients
    if _client is None:
        try:
            credential = DefaultAzureCredential()
            token_provider = get_bearer_token_provider(credential, "https://cognitiveservices.azure.com/.default")
            _client = AsyncAzureOpenAI(
                azure_endpoint=settings.azure_openai_endpoint,
                azure_ad_token_provider=token_provider,
                api_version=settings.azure_openai_api_version,
                max_retries=5,
                timeout=settings.llm_timeout_seconds,
            )
            _clients = [_client]
            logger.info("AOAI[A]: %s", settings.azure_openai_endpoint)

            if settings.azure_openai_endpoint_2:
                _client_2 = AsyncAzureOpenAI(
                    azure_endpoint=settings.azure_openai_endpoint_2,
                    azure_ad_token_provider=token_provider,
                    api_version=settings.azure_openai_api_version,
                    max_retries=5,
                    timeout=settings.llm_timeout_seconds,
                )
                _clients.append(_client_2)
                logger.info("AOAI[B]: %s", settings.azure_openai_endpoint_2)

            if settings.azure_openai_endpoint_3:
                _client_3 = AsyncAzureOpenAI(
                    azure_endpoint=settings.azure_openai_endpoint_3,
                    azure_ad_token_provider=token_provider,
                    api_version=settings.azure_openai_api_version,
                    max_retries=5,
                    timeout=settings.llm_timeout_seconds,
                )
                _clients.append(_client_3)
                logger.info("AOAI[C]: %s", settings.azure_openai_endpoint_3)

            logger.info("Round-robin across %d AOAI endpoints", len(_clients))
        except Exception:
            logger.warning("DefaultAzureCredential failed, falling back to API key")
            _client = AsyncAzureOpenAI(
                azure_endpoint=settings.azure_openai_endpoint,
                api_key=settings.azure_openai_api_key,
                api_version=settings.azure_openai_api_version,
                max_retries=5,
                timeout=settings.llm_timeout_seconds,
            )
            _clients = [_client]
    return _client


async def complete(
    client: AsyncAzureOpenAI,
    model: str,
    system_prompt: str,
    user_content: str,
    *,
    response_format: Any = None,
    temperature: float = 0.0,
) -> Any:
    """Send a chat completion request and return the parsed content."""
    t_wait = time.time()
    async with _llm_semaphore:
        wait_ms = int((time.time() - t_wait) * 1000)
        active_client = _get_round_robin_client()
        client_tag = "B" if active_client is _client_2 else "A"
        if wait_ms > 100:
            logger.info("EVAL_SEM|wait_ms=%d|client=%s|model=%s", wait_ms, client_tag, model)
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_content},
        ]
        kwargs: dict[str, Any] = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
        }
        if response_format is not None:
            if isinstance(response_format, dict):
                resp = await active_client.chat.completions.create(**kwargs, response_format=response_format)
                return resp.choices[0].message.content
            else:
                resp = await active_client.beta.chat.completions.parse(
                    **kwargs,
                    response_format=response_format,
                )
                return resp.choices[0].message.parsed
        else:
            resp = await active_client.chat.completions.create(**kwargs)
            return resp.choices[0].message.content


async def complete_with_vision(
    client: AsyncAzureOpenAI,
    model: str,
    system_prompt: str,
    image_base64: str,
    user_content: str,
    *,
    response_format: Any = None,
    temperature: float = 0.0,
    detail: str = "high",
    mime_type: str = "image/png",
) -> Any:
    """Send a vision chat completion with a base64 image."""
    t_wait = time.time()
    async with _llm_semaphore:
        wait_ms = int((time.time() - t_wait) * 1000)
        active_client = _get_round_robin_client()
        client_tag = "B" if active_client is _client_2 else "A"
        if wait_ms > 100:
            logger.info("EVAL_SEM|wait_ms=%d|client=%s|model=%s", wait_ms, client_tag, model)
        messages: list[dict[str, Any]] = [
            {"role": "system", "content": system_prompt},
            {
                "role": "user",
                "content": [
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:{mime_type};base64,{image_base64}", "detail": detail},
                    },
                    {"type": "text", "text": user_content},
                ],
            },
        ]
        kwargs: dict[str, Any] = {
            "model": model,
            "messages": messages,
            "temperature": temperature,
        }
        if response_format is not None:
            if isinstance(response_format, dict):
                resp = await active_client.chat.completions.create(**kwargs, response_format=response_format)
                return resp.choices[0].message.content
            else:
                resp = await active_client.beta.chat.completions.parse(
                    **kwargs,
                    response_format=response_format,
                )
                return resp.choices[0].message.parsed
        else:
            resp = await active_client.chat.completions.create(**kwargs)
            return resp.choices[0].message.content
