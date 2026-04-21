"""Extract router — POST /extract endpoint."""

import base64
import io
import json
import logging

from fastapi import APIRouter, Response
from PIL import Image

from llm_client import complete_with_vision, detect_mime_type
from models import ExtractRequest, ExtractResponse
from prompts.extract_prompt import EXTRACT_SYSTEM_PROMPT
from utils import display_model, parse_json_response

import state

logger = logging.getLogger(__name__)
router = APIRouter()

# Formats Azure OpenAI vision API natively supports
_SUPPORTED_VISION_MIMES = {"image/png", "image/jpeg", "image/gif", "image/webp"}


def _ensure_supported_format(content_b64: str, detected_mime: str) -> tuple[str, str]:
    """Convert unsupported image formats (TIFF, BMP, etc.) to PNG.

    Azure OpenAI vision API only supports PNG, JPEG, GIF, WEBP.
    If the image is in another format, convert it to PNG via Pillow.
    Returns (base64_content, mime_type).
    """
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


def _coerce_to_schema(data: dict, schema_str: str) -> dict:
    """Light type coercion to match json_schema expectations.

    Only coerces obvious safe cases — doesn't transform complex structures.
    """
    try:
        schema = json.loads(schema_str)
    except (json.JSONDecodeError, TypeError):
        return data

    props = schema.get("properties", {})
    if not props:
        return data

    for field, spec in props.items():
        if field not in data or data[field] is None:
            continue

        expected_type = spec.get("type", "")
        value = data[field]

        try:
            if expected_type == "integer" and isinstance(value, str):
                cleaned = value.replace(",", "").replace("$", "").replace("%", "").strip()
                if cleaned.lstrip("-").isdigit():
                    data[field] = int(cleaned)
            elif expected_type == "number" and isinstance(value, str):
                cleaned = value.replace(",", "").replace("$", "").replace("%", "").strip()
                data[field] = float(cleaned)
            elif expected_type == "boolean" and isinstance(value, str):
                data[field] = value.lower() in ("true", "yes", "1")
            elif expected_type == "integer" and isinstance(value, float):
                if value == int(value):
                    data[field] = int(value)
        except (ValueError, TypeError):
            pass  # Leave original value if coercion fails

    return data


@router.post("/extract")
async def extract(req: ExtractRequest, response: Response) -> ExtractResponse:
    model = state.settings.extract_model
    response.headers["X-Model-Name"] = display_model(model)

    try:
        schema_str = req.json_schema or "{}"

        # Build field-level instructions from schema descriptions
        field_instructions = ""
        try:
            import json as _json
            schema_obj = _json.loads(schema_str)
            props = schema_obj.get("properties", {})
            if props:
                instructions = []
                for field_name, field_spec in props.items():
                    desc = field_spec.get("description", "")
                    ftype = field_spec.get("type", "")
                    if desc:
                        instructions.append(f"- {field_name} ({ftype}): {desc}")
                    else:
                        instructions.append(f"- {field_name} ({ftype})")
                field_instructions = "Fields to extract:\n" + "\n".join(instructions) + "\n\n"
        except Exception:
            pass

        user_content = (
            f"Extract all fields from this document image according to this JSON schema:\n\n"
            f"{field_instructions}"
            f"{schema_str}\n\n"
            f"Return a JSON object with the extracted values. Use null for any field not found in the document."
        )

        # Auto-detect image format and convert unsupported formats to PNG
        content = req.content if req.content else ""
        mime_type = detect_mime_type(content)
        content, mime_type = _ensure_supported_format(content, mime_type)

        result = await complete_with_vision(
            state.aoai_client,
            model,
            EXTRACT_SYSTEM_PROMPT,
            content,
            user_content,
            mime_type=mime_type,
        )

        extracted = parse_json_response(result)
        if extracted is None:
            extracted = {}

        # Remove document_id from extracted to prevent duplicate kwarg crash
        extracted.pop("document_id", None)

        # Light schema validation: coerce types to match json_schema
        extracted = _coerce_to_schema(extracted, schema_str)

        return ExtractResponse(document_id=req.document_id, **extracted)
    except Exception:
        logger.exception("Extract LLM error for %s", req.document_id)
        return ExtractResponse(document_id=req.document_id)
