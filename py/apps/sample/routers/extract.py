"""Extract router — POST /extract endpoint."""

import logging

from fastapi import APIRouter, Response

from llm_client import complete, complete_with_vision
from models import ExtractRequest, ExtractResponse
from prompts.extract_prompt import EXTRACT_SYSTEM_PROMPT
from services.extract_service import extract_with_di
from utils import display_model, parse_json_response

import state

logger = logging.getLogger(__name__)
router = APIRouter()

_DI_EXTRACT_SYSTEM_PROMPT = """You are a precise document extraction system. You will receive OCR text extracted from a document. Extract data according to the JSON schema specification.

Rules:
- Extract exactly the fields specified in the schema
- Return null for fields that cannot be found in the text
- For boolean fields, return true or false based on what's indicated
- For number fields, return the numeric value (not a string)
- For array fields, return a list of values found
- Preserve exact text as it appears (don't correct typos in names/addresses)
- For checkboxes/radio buttons, look for indicators like [x], checked, yes vs [ ], unchecked, no
- Be thorough — examine all parts of the extracted text carefully
- Tables are delimited by [TABLE] and [/TABLE] markers with pipe-separated columns

IMPORTANT: Return a JSON object matching the schema. Only include fields from the schema."""


@router.post("/extract")
async def extract(req: ExtractRequest, response: Response) -> ExtractResponse:
    settings = state.settings
    use_di = (
        settings.extract_preprocessor == "document-intelligence"
        and settings.di_endpoint
    )

    try:
        schema_str = req.json_schema or "{}"

        if use_di:
            model = "gpt-5-4-mini"
            response.headers["X-Model-Name"] = display_model(model)

            ocr_text = await extract_with_di(
                req.content,
                settings.di_endpoint,
            )

            user_content = f"""Extract all fields from this document text according to this JSON schema:

{schema_str}

--- DOCUMENT TEXT (from OCR) ---
{ocr_text}
--- END DOCUMENT TEXT ---

Return a JSON object with the extracted values. Use null for any field not found in the document."""

            result = await complete(
                state.aoai_client,
                model,
                _DI_EXTRACT_SYSTEM_PROMPT,
                user_content,
            )
        else:
            model = settings.extract_model
            response.headers["X-Model-Name"] = display_model(model)

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
