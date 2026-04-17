"""Extract router — POST /extract endpoint."""

import asyncio
import logging

from fastapi import APIRouter, Response

from llm_client import complete_with_vision
from models import ExtractRequest, ExtractResponse
from prompts.extract_prompt import EXTRACT_SYSTEM_PROMPT
from utils import display_model, parse_json_response

import state

logger = logging.getLogger(__name__)
router = APIRouter()

# Size thresholds for content-aware timeout (base64 bytes)
_LARGE_CONTENT_THRESHOLD = 1_000_000  # ~1 MB base64 ≈ 750 KB raw image
_DEFAULT_TIMEOUT = 25  # seconds
_LARGE_CONTENT_TIMEOUT = 45  # more headroom for big documents
_RETRY_TIMEOUT = 30  # retry budget after first timeout


@router.post("/extract")
async def extract(req: ExtractRequest, response: Response) -> ExtractResponse:
    model = state.settings.extract_model
    response.headers["X-Model-Name"] = display_model(model)

    try:
        schema_str = req.json_schema or "{}"
        content_size = len(req.content) if req.content else 0
        is_large = content_size > _LARGE_CONTENT_THRESHOLD

        timeout = _LARGE_CONTENT_TIMEOUT if is_large else _DEFAULT_TIMEOUT

        if is_large:
            user_content = (
                "Extract the most important fields FIRST from this document image "
                "according to this JSON schema. It is better to return partial data "
                "than nothing.\n\n"
                f"{schema_str}\n\n"
                "Return a JSON object with the extracted values. "
                "Use null for any field not found in the document."
            )
        else:
            user_content = (
                f"Extract all fields from this document image according to this JSON schema:\n\n"
                f"{schema_str}\n\n"
                "Return a JSON object with the extracted values. "
                "Use null for any field not found in the document."
            )

        # First attempt with content-aware timeout
        result = await _extract_with_timeout(
            model, req.content, user_content, timeout, req.document_id, content_size,
        )

        # Retry with a truncation/speed hint if the first attempt timed out
        if result is None:
            logger.warning(
                "Extract timeout for %s (%d bytes), retrying with truncation hint",
                req.document_id, content_size,
            )
            user_content_retry = (
                "Extract key fields from this document. Focus on the MOST IMPORTANT "
                "fields first. Return what you can extract within the time limit.\n\n"
                f"{schema_str}"
            )
            result = await _extract_with_timeout(
                model, req.content, user_content_retry,
                _RETRY_TIMEOUT, req.document_id, content_size,
            )

        if result is None:
            logger.error("Extract double timeout for %s", req.document_id)

        extracted = parse_json_response(result)
        if extracted is None:
            extracted = {}

        return ExtractResponse(document_id=req.document_id, **extracted)
    except Exception:
        logger.exception("Extract LLM error for %s", req.document_id)
        return ExtractResponse(document_id=req.document_id)


async def _extract_with_timeout(
    model: str,
    content: str,
    user_content: str,
    timeout: float,
    document_id: str,
    content_size: int,
) -> str | None:
    """Call complete_with_vision wrapped in an asyncio timeout.

    Returns the raw LLM response string, or ``None`` on timeout.
    """
    try:
        return await asyncio.wait_for(
            complete_with_vision(
                state.aoai_client,
                model,
                EXTRACT_SYSTEM_PROMPT,
                content,
                user_content,
            ),
            timeout=timeout,
        )
    except asyncio.TimeoutError:
        logger.warning(
            "Vision call timed out after %ds for %s (%d bytes)",
            timeout, document_id, content_size,
        )
        return None
