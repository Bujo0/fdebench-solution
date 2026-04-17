"""Extract router — POST /extract endpoint."""

import asyncio
import json
import logging
import re
from datetime import datetime

from fastapi import APIRouter, Response

from llm_client import complete_with_vision
from models import ExtractRequest, ExtractResponse
from prompts.extract_prompt import EXTRACT_SYSTEM_PROMPT_V4
from utils import display_model, parse_json_response

import state

logger = logging.getLogger(__name__)
router = APIRouter()

# Size thresholds for content-aware timeout (base64 bytes)
_LARGE_CONTENT_THRESHOLD = 1_000_000  # ~1 MB base64 ≈ 750 KB raw image
_DEFAULT_TIMEOUT = 30  # seconds
_LARGE_CONTENT_TIMEOUT = 55  # more headroom for big documents
_RETRY_TIMEOUT = 35  # retry budget after first timeout

# Date patterns for post-processing normalization
_DATE_PATTERNS = [
    # "November 2, 2025" or "Nov 2, 2025"
    (re.compile(r"^([A-Z][a-z]+)\s+(\d{1,2}),?\s+(\d{4})$"), "%B %d, %Y"),
    (re.compile(r"^([A-Z][a-z]{2})\s+(\d{1,2}),?\s+(\d{4})$"), "%b %d, %Y"),
    # "2 November 2025"
    (re.compile(r"^(\d{1,2})\s+([A-Z][a-z]+)\s+(\d{4})$"), "%d %B %Y"),
]

# Fields known to contain dates (by naming convention)
_DATE_FIELD_NAMES = {"weekStartDate", "startDate", "endDate", "date", "taxDateEnd"}


def _try_normalize_date(value: str) -> str:
    """Try to convert a natural-language date to ISO format (YYYY-MM-DD)."""
    value = value.strip()
    # Already ISO format
    if re.match(r"^\d{4}-\d{2}-\d{2}$", value):
        return value
    for pattern, fmt in _DATE_PATTERNS:
        if pattern.match(value):
            try:
                dt = datetime.strptime(value.replace(",", ""), fmt.replace(",", ""))
                return dt.strftime("%Y-%m-%d")
            except ValueError:
                continue
    return value


def _postprocess_dates(data: dict, schema_str: str) -> dict:
    """Normalize date fields in extracted data to ISO format when appropriate."""
    try:
        schema = json.loads(schema_str)
    except (json.JSONDecodeError, TypeError):
        return data

    properties = schema.get("properties", {})

    def _should_normalize(field: str, spec: dict) -> bool:
        desc = spec.get("description", "").lower()
        # Don't normalize if schema says "as it appears"
        if "as it appears" in desc:
            return False
        # Normalize known date fields
        if field in _DATE_FIELD_NAMES:
            return True
        # Normalize if field name ends with "Date"
        if field.endswith("Date") or field.endswith("_date"):
            return True
        return False

    def _normalize_recursive(obj: dict | list, props: dict) -> dict | list:
        if isinstance(obj, dict):
            result = {}
            for k, v in obj.items():
                spec = props.get(k, {})
                if isinstance(v, str) and _should_normalize(k, spec):
                    result[k] = _try_normalize_date(v)
                elif isinstance(v, dict) and spec.get("type") == "object":
                    sub_props = spec.get("properties", {})
                    result[k] = _normalize_recursive(v, sub_props)
                elif isinstance(v, list) and spec.get("type") == "array":
                    item_spec = spec.get("items", {})
                    if item_spec.get("type") == "object":
                        sub_props = item_spec.get("properties", {})
                        result[k] = [_normalize_recursive(item, sub_props) if isinstance(item, dict) else item for item in v]
                    else:
                        result[k] = v
                else:
                    result[k] = v
            return result
        return obj

    return _normalize_recursive(data, properties)


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
                "Extract all fields from this document image according to this JSON schema. "
                "Include ALL rows in tables/arrays — do not truncate.\n\n"
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

        # Post-process: normalize date fields to ISO format
        if schema_str and extracted:
            extracted = _postprocess_dates(extracted, schema_str)

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
                EXTRACT_SYSTEM_PROMPT_V4,
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
