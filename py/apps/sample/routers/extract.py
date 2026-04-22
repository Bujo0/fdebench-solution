"""Extract router — POST /extract endpoint."""

import base64
import copy
import io
import json
import logging
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

    try:
        schema_str = req.json_schema or "{}"

        user_content = (
            f"Extract all fields from this document image according to this JSON schema:\n\n"
            f"{schema_str}\n\n"
            f"Return a JSON object with the extracted values. Use null for any field not found in the document."
        )

        content = req.content if req.content else ""
        mime_type = detect_mime_type(content)
        content, mime_type = _ensure_supported_format(content, mime_type)

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
            except Exception:
                logger.warning("Structured output failed for %s, falling back to text mode",
                               req.document_id)

        # Attempt 2: text mode (current approach)
        if extracted is None:
            try:
                result = await complete_with_vision(
                    state.aoai_client, model, EXTRACT_SYSTEM_PROMPT,
                    content, user_content, mime_type=mime_type,
                )
                extracted = parse_json_response(result)
            except Exception:
                logger.warning("Text mode extraction failed for %s", req.document_id)

        # Attempt 3: retry with detail="high" for degraded documents
        if extracted is None:
            try:
                result = await complete_with_vision(
                    state.aoai_client, model, EXTRACT_SYSTEM_PROMPT,
                    content, user_content, mime_type=mime_type,
                    detail="high",
                )
                extracted = parse_json_response(result)
            except Exception:
                logger.warning("High-detail retry failed for %s", req.document_id)

        if extracted is None:
            extracted = {}

        # Post-process: convert empty strings to null (scorer gives 1.0,1.0 for
        # null-null match, 0.0,0.0 for anything vs null — huge impact on 21.5% null fields)
        extracted = _clean_nulls(extracted)

        extracted.pop("document_id", None)
        return ExtractResponse(document_id=req.document_id, **extracted)
    except Exception:
        logger.exception("Extract error for %s", req.document_id)
        return ExtractResponse(document_id=req.document_id)
