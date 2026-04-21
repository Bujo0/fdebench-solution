"""Extract router — POST /extract endpoint."""

import asyncio
import base64
import io
import json
import logging
import state
from fastapi import APIRouter
from fastapi import Response
from llm_client import complete_with_vision
from models import ExtractRequest
from models import ExtractResponse
from PIL import Image
from prompts.extract_prompt import EXTRACT_SYSTEM_PROMPT
from utils import display_model
from utils import parse_json_response

logger = logging.getLogger(__name__)
router = APIRouter()

# Size thresholds for content-aware timeout (base64 bytes)
_LARGE_CONTENT_THRESHOLD = 1_000_000  # ~1 MB base64 ≈ 750 KB raw image
_MAX_IMAGE_DIMENSION = 2048  # Max width/height before downscaling
_DEFAULT_TIMEOUT = 30  # seconds
_LARGE_CONTENT_TIMEOUT = 55  # more headroom for big documents
_RETRY_TIMEOUT = 35  # retry budget after first timeout


def _optimize_image(content_b64: str) -> str:
    """Downscale oversized images to reduce AOAI processing time.

    The vision API processes images at max 2048×2048 internally,
    so resizing client-side saves upload time with zero quality loss.
    """
    try:
        raw = base64.b64decode(content_b64)
        img = Image.open(io.BytesIO(raw))
        w, h = img.size

        if w <= _MAX_IMAGE_DIMENSION and h <= _MAX_IMAGE_DIMENSION:
            return content_b64  # Already within bounds

        # Downscale preserving aspect ratio
        ratio = min(_MAX_IMAGE_DIMENSION / w, _MAX_IMAGE_DIMENSION / h)
        new_w, new_h = int(w * ratio), int(h * ratio)
        img = img.resize((new_w, new_h), Image.LANCZOS)

        buf = io.BytesIO()
        img.save(buf, format="PNG", optimize=True)
        optimized = base64.b64encode(buf.getvalue()).decode("ascii")

        logger.info(
            "Image optimized: %dx%d → %dx%d, %dKB → %dKB",
            w, h, new_w, new_h, len(content_b64) // 1024, len(optimized) // 1024,
        )
        return optimized
    except Exception:
        return content_b64  # Can't process — return original


def _compress_to_jpeg(content_b64: str, quality: int = 85) -> tuple[str, str]:
    """Compress image to JPEG without resizing. Returns (base64, mime_type)."""
    try:
        raw = base64.b64decode(content_b64)
        img = Image.open(io.BytesIO(raw))
        if img.mode in ("RGBA", "P"):
            img = img.convert("RGB")
        buf = io.BytesIO()
        img.save(buf, format="JPEG", quality=quality, optimize=True)
        compressed = base64.b64encode(buf.getvalue()).decode("ascii")
        # Only use compressed if it's actually smaller
        if len(compressed) < len(content_b64):
            return compressed, "image/jpeg"
        return content_b64, "image/png"
    except Exception:
        return content_b64, "image/png"


@router.post("/extract")
async def extract(req: ExtractRequest, response: Response) -> ExtractResponse:
    model = state.settings.extract_model
    response.headers["X-Model-Name"] = display_model(model)

    try:
        schema_str = req.json_schema or "{}"
        # Optimize oversized images to reduce AOAI processing time
        # Image resize disabled — EXP-045 showed -2pp resolution, +1.8s latency
        optimized_content = req.content if req.content else ""
        mime_type = "image/png"
        content_size = len(optimized_content)
        is_large = content_size > _LARGE_CONTENT_THRESHOLD

        timeout = _LARGE_CONTENT_TIMEOUT if is_large else _DEFAULT_TIMEOUT

        # Build field-level instructions from schema descriptions
        field_instructions = ""
        try:
            schema_obj = json.loads(schema_str)
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
        except (json.JSONDecodeError, TypeError):
            pass

        if is_large:
            user_content = (
                "Extract all fields from this document image according to this JSON schema. "
                "Include ALL rows in tables/arrays — do not truncate.\n\n"
                f"{field_instructions}"
                f"{schema_str}\n\n"
                "Return a JSON object with the extracted values. "
                "Use null for any field not found in the document."
            )
        else:
            user_content = (
                f"Extract all fields from this document image according to this JSON schema:\n\n"
                f"{field_instructions}"
                f"{schema_str}\n\n"
                "Return a JSON object with the extracted values. "
                "Use null for any field not found in the document."
            )

        # First attempt with content-aware timeout
        result = await _extract_with_timeout(
            model,
            optimized_content,
            user_content,
            timeout,
            req.document_id,
            content_size,
            mime_type=mime_type,
        )

        # Retry with a truncation/speed hint if the first attempt timed out
        if result is None:
            logger.warning(
                "Extract timeout for %s (%d bytes), retrying with truncation hint",
                req.document_id,
                content_size,
            )
            user_content_retry = (
                "Extract key fields from this document. Focus on the MOST IMPORTANT "
                "fields first. Return what you can extract within the time limit.\n\n"
                f"{schema_str}"
            )
            result = await _extract_with_timeout(
                model,
                optimized_content,
                user_content_retry,
                _RETRY_TIMEOUT,
                req.document_id,
                content_size,
                mime_type=mime_type,
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
    mime_type: str = "image/png",
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
                mime_type=mime_type,
            ),
            timeout=timeout,
        )
    except asyncio.TimeoutError:
        logger.warning(
            "Vision call timed out after %ds for %s (%d bytes)",
            timeout,
            document_id,
            content_size,
        )
        return None
