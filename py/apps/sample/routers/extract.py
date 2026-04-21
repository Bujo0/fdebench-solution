"""Extract router — POST /extract endpoint."""

import base64
import io
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


@router.post("/extract")
async def extract(req: ExtractRequest, response: Response) -> ExtractResponse:
    model = state.settings.extract_model
    response.headers["X-Model-Name"] = display_model(model)

    try:
        schema_str = req.json_schema or "{}"
        user_content = f"""Extract all fields from this document image according to this JSON schema:

{schema_str}

Return a JSON object with the extracted values. Use null for any field not found in the document."""

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

        return ExtractResponse(document_id=req.document_id, **extracted)
    except Exception:
        logger.exception("Extract LLM error for %s", req.document_id)
        return ExtractResponse(document_id=req.document_id)
