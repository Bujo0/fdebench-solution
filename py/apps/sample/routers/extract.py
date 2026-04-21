"""Extract router — POST /extract endpoint."""

import logging

from fastapi import APIRouter, Response

from llm_client import complete_with_vision
from models import ExtractRequest, ExtractResponse
from prompts.extract_prompt import EXTRACT_SYSTEM_PROMPT
from utils import display_model, parse_json_response

import state

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/extract")
async def extract(req: ExtractRequest, response: Response) -> ExtractResponse:
    model = state.settings.extract_model
    response.headers["X-Model-Name"] = display_model(model)

    try:
        schema_str = req.json_schema or "{}"
        user_content = f"""Extract all fields from this document image according to this JSON schema:

{schema_str}

Return a JSON object with the extracted values. Use null for any field not found in the document."""

        result = await complete_with_vision(
            state.aoai_client,
            model,
            EXTRACT_SYSTEM_PROMPT,
            req.content,
            user_content,
        )

        extracted = parse_json_response(result)
        if extracted is None:
            extracted = {}

        return ExtractResponse(document_id=req.document_id, **extracted)
    except Exception:
        logger.exception("Extract LLM error for %s", req.document_id)
        return ExtractResponse(document_id=req.document_id)
