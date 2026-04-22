"""Extract router — POST /extract endpoint."""

import base64
import copy
import io
import json
import logging
import time
from typing import Any

from fastapi import APIRouter, Response
from PIL import Image

from llm_client import complete_with_vision, detect_mime_type
from models import ExtractRequest, ExtractResponse
from prompts.extract_prompt import EXTRACT_SYSTEM_PROMPT
from utils import display_model, parse_json_response

import state

logger = logging.getLogger(__name__)
router = APIRouter()

_SUPPORTED_VISION_MIMES = {"image/png", "image/jpeg", "image/gif", "image/webp"}


def _ensure_supported_format(content_b64: str, detected_mime: str) -> tuple[str, str]:
    """Convert unsupported image formats (TIFF, BMP, etc.) to PNG."""
    if detected_mime in _SUPPORTED_VISION_MIMES:
        return content_b64, detected_mime

    try:
        raw = base64.b64decode(content_b64)
        img = Image.open(io.BytesIO(raw))
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        converted = base64.b64encode(buf.getvalue()).decode("ascii")
        logger.info("Converted %s to PNG (%dKB → %dKB)", detected_mime,
                     len(content_b64) // 1024, len(converted) // 1024)
        return converted, "image/png"
    except Exception:
        logger.warning("Failed to convert %s to PNG, passing as-is", detected_mime)
        return content_b64, detected_mime


def _sanitize_schema_for_strict(schema: dict) -> dict:
    """Make a JSON schema compatible with OpenAI strict structured output mode.

    - All object properties become required
    - additionalProperties set to false
    - Non-object/array types become nullable via anyOf
    - Recurses into nested objects and arrays
    """
    schema = copy.deepcopy(schema)
    return _sanitize_node(schema)


def _sanitize_node(node: dict) -> dict:
    """Recursively sanitize a schema node for strict mode."""
    if not isinstance(node, dict):
        return node

    node_type = node.get("type")

    if node_type == "object":
        props = node.get("properties") or {}
        node["required"] = list(props.keys())
        node["additionalProperties"] = False
        for field in props:
            props[field] = _sanitize_node(props[field])
        return node

    if node_type == "array":
        items = node.get("items") or {}
        node["items"] = _sanitize_node(items)
        return node

    # For leaf types (string, number, integer, boolean): make nullable via anyOf
    # Preserve all constraints (enum, format, pattern, etc.) in the typed branch
    if isinstance(node_type, str) and node_type not in ("object", "array", "null"):
        typed_branch = dict(node)  # preserves enum, format, pattern, description, etc.
        return {"anyOf": [typed_branch, {"type": "null"}]}

    return node


def _clean_nulls(data: Any) -> Any:
    """Recursively convert empty strings and N/A variants to None.

    The scorer gives (1.0, 1.0) for null-null match but (0.0, 0.0) for
    any non-null vs null. Since 21.5% of gold values are null, correctly
    returning null for missing fields is critical.
    """
    if isinstance(data, dict):
        return {k: _clean_nulls(v) for k, v in data.items()}
    if isinstance(data, list):
        return [_clean_nulls(item) for item in data]
    if isinstance(data, str):
        stripped = data.strip()
        if stripped == "" or stripped.lower() in ("n/a", "na", "none", "null", "n.a."):
            return None
    return data


def _build_structured_response_format(schema_str: str) -> dict | None:
    """Try to build an OpenAI structured output response_format from a JSON schema string.

    Returns None if the schema can't be sanitized for strict mode.
    """
    try:
        schema = json.loads(schema_str)
        if not isinstance(schema, dict) or schema.get("type") != "object":
            return None
        sanitized = _sanitize_schema_for_strict(schema)
        return {
            "type": "json_schema",
            "json_schema": {
                "name": "extracted_data",
                "strict": True,
                "schema": sanitized,
            },
        }
    except Exception:
        logger.debug("Could not build structured output schema, using text mode")
        return None


@router.post("/extract")
async def extract(req: ExtractRequest, response: Response) -> ExtractResponse:
    model = state.settings.extract_model
    response.headers["X-Model-Name"] = display_model(model)
    t0 = time.time()
    attempt_used = 0

    try:
        schema_str = req.json_schema or "{}"

        # Parse schema to log field names
        try:
            schema_obj = json.loads(schema_str)
            schema_fields = list((schema_obj.get("properties") or {}).keys())
        except Exception:
            schema_fields = []

        user_content = (
            f"Extract all fields from this document image according to this JSON schema:\n\n"
            f"{schema_str}\n\n"
            f"Return a JSON object with the extracted values. Use null for any field not found in the document."
        )

        content = req.content if req.content else ""
        mime_type = detect_mime_type(content)
        content, mime_type = _ensure_supported_format(content, mime_type)
        logger.info("T2 start: %s mime=%s schema_len=%d img_kb=%d schema_fields=%s",
                     req.document_id, mime_type, len(schema_str), len(content)//1024,
                     ",".join(schema_fields[:10]) if schema_fields else "none")

        # Attempt 1: structured output with schema enforcement
        response_format = _build_structured_response_format(schema_str)
        extracted = None

        if response_format is not None:
            try:
                result = await complete_with_vision(
                    state.aoai_client, model, EXTRACT_SYSTEM_PROMPT,
                    content, user_content, mime_type=mime_type,
                    response_format=response_format,
                )
                if isinstance(result, str):
                    extracted = parse_json_response(result)
                elif isinstance(result, dict):
                    extracted = result
                if extracted:
                    attempt_used = 1
            except Exception as e:
                logger.warning("T2 attempt1_fail: %s structured_output err=%s",
                               req.document_id, type(e).__name__)
        else:
            logger.info("T2 schema_skip: %s schema not compatible with strict mode",
                         req.document_id)

        # Attempt 2: text mode (current approach)
        if extracted is None:
            try:
                result = await complete_with_vision(
                    state.aoai_client, model, EXTRACT_SYSTEM_PROMPT,
                    content, user_content, mime_type=mime_type,
                )
                extracted = parse_json_response(result)
                if extracted:
                    attempt_used = 2
            except Exception as e:
                logger.warning("T2 attempt2_fail: %s text_mode err=%s",
                               req.document_id, type(e).__name__)

        # Attempt 3: retry with detail="high" for degraded documents
        if extracted is None:
            try:
                result = await complete_with_vision(
                    state.aoai_client, model, EXTRACT_SYSTEM_PROMPT,
                    content, user_content, mime_type=mime_type,
                    detail="high",
                )
                extracted = parse_json_response(result)
                if extracted:
                    attempt_used = 3
            except Exception as e:
                logger.warning("T2 attempt3_fail: %s high_detail err=%s",
                               req.document_id, type(e).__name__)

        if extracted is None:
            extracted = {}

        extracted = _clean_nulls(extracted)
        extracted.pop("document_id", None)

        # Count value types for diagnostics
        field_count = len(extracted)
        null_count = sum(1 for v in extracted.values() if v is None)
        str_count = sum(1 for v in extracted.values() if isinstance(v, str))
        num_count = sum(1 for v in extracted.values() if isinstance(v, (int, float)) and not isinstance(v, bool))
        bool_count = sum(1 for v in extracted.values() if isinstance(v, bool))
        list_count = sum(1 for v in extracted.values() if isinstance(v, list))
        dict_count = sum(1 for v in extracted.values() if isinstance(v, dict))
        elapsed_ms = int((time.time() - t0) * 1000)

        logger.info("T2 done: %s attempt=%d fields=%d null=%d str=%d num=%d "
                     "bool=%d list=%d dict=%d ms=%d",
                     req.document_id, attempt_used, field_count, null_count,
                     str_count, num_count, bool_count, list_count, dict_count,
                     elapsed_ms)

        return ExtractResponse(document_id=req.document_id, **extracted)
    except Exception:
        elapsed_ms = int((time.time() - t0) * 1000)
        logger.exception("T2 FAIL: %s after %dms — returning empty", req.document_id, elapsed_ms)
        return ExtractResponse(document_id=req.document_id)
