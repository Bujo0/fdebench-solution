"""Async Azure OpenAI client factory with retry and structured output support."""

import logging
from typing import Any

from azure.identity import DefaultAzureCredential, get_bearer_token_provider
from openai import AsyncAzureOpenAI

from config import Settings

logger = logging.getLogger(__name__)

_client: AsyncAzureOpenAI | None = None


def get_client(settings: Settings) -> AsyncAzureOpenAI:
    """Return a cached AsyncAzureOpenAI client (app-scoped singleton).

    Uses DefaultAzureCredential (managed identity / az login) for auth,
    falling back to API key if the endpoint supports it.
    """
    global _client
    if _client is None:
        try:
            credential = DefaultAzureCredential()
            token_provider = get_bearer_token_provider(
                credential, "https://cognitiveservices.azure.com/.default"
            )
            _client = AsyncAzureOpenAI(
                azure_endpoint=settings.azure_openai_endpoint,
                azure_ad_token_provider=token_provider,
                api_version=settings.azure_openai_api_version,
                max_retries=3,
                timeout=settings.llm_timeout_seconds,
            )
            logger.info("Using DefaultAzureCredential for AOAI auth")
        except Exception:
            logger.warning("DefaultAzureCredential failed, falling back to API key")
            _client = AsyncAzureOpenAI(
                azure_endpoint=settings.azure_openai_endpoint,
                api_key=settings.azure_openai_api_key,
                api_version=settings.azure_openai_api_version,
                max_retries=3,
                timeout=settings.llm_timeout_seconds,
            )
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
        resp = await client.beta.chat.completions.parse(
            **kwargs,
            response_format=response_format,
        )
        return resp.choices[0].message.parsed
    else:
        resp = await client.chat.completions.create(**kwargs)
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
    detail: str = "auto",
    mime_type: str = "image/png",
) -> Any:
    """Send a vision chat completion with a base64 image."""
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
        resp = await client.beta.chat.completions.parse(
            **kwargs,
            response_format=response_format,
        )
        return resp.choices[0].message.parsed
    else:
        resp = await client.chat.completions.create(**kwargs)
        return resp.choices[0].message.content
