"""Extract router — POST /extract endpoint."""

import base64
import io
import logging

from fastapi import APIRouter, Response
from PIL import Image

from llm_client import complete_with_vision
from models import ExtractRequest, ExtractResponse
from prompts.extract_prompt import EXTRACT_SYSTEM_PROMPT
from utils import display_model, parse_json_response

import state

logger = logging.getLogger(__name__)
router = APIRouter()

_MAX_IMAGE_DIM = 2048


def _optimize_image(image_base64: str) -> tuple[str, str]:
    """Downscale oversized images and convert to JPEG for smaller payload. Returns (base64, mime_type)."""
    img_bytes = base64.b64decode(image_base64)
    img = Image.open(io.BytesIO(img_bytes))
    w, h = img.size

    needs_resize = max(w, h) > _MAX_IMAGE_DIM
    if not needs_resize and len(img_bytes) < 200_000:
        return image_base64, "image/png"

    if needs_resize:
        scale = _MAX_IMAGE_DIM / max(w, h)
        img = img.resize((int(w * scale), int(h * scale)), Image.LANCZOS)

    if img.mode in ("RGBA", "P"):
        img = img.convert("RGB")
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=85)
    return base64.b64encode(buf.getvalue()).decode(), "image/jpeg"


@router.post("/extract")
async def extract(req: ExtractRequest, response: Response) -> ExtractResponse:
    model = state.settings.extract_model
    response.headers["X-Model-Name"] = display_model(model)

    try:
        schema_str = req.json_schema or "{}"
        user_content = f"""Extract all fields from this document image according to this JSON schema:

{schema_str}

Return a JSON object with the extracted values. Use null for any field not found in the document."""

        optimized_b64, mime = _optimize_image(req.content)

        result = await complete_with_vision(
            state.aoai_client,
            model,
            EXTRACT_SYSTEM_PROMPT,
            optimized_b64,
            user_content,
            mime_type=mime,
        )

        extracted = parse_json_response(result)
        if extracted is None:
            extracted = {}

        return ExtractResponse(document_id=req.document_id, **extracted)
    except Exception:
        logger.exception("Extract LLM error for %s", req.document_id)
        return ExtractResponse(document_id=req.document_id)
