"""Error handling middleware for the FastAPI application."""

import json
import logging

from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

logger = logging.getLogger(__name__)


async def validation_error_handler(request: Request, exc: RequestValidationError):
    """Return 422 with detail string for Pydantic validation errors."""
    return JSONResponse(status_code=422, content={"detail": str(exc)})


async def error_handling_middleware(request: Request, call_next):
    """Catch malformed JSON and unhandled exceptions before they reach endpoints."""
    if request.method == "POST":
        content_type = request.headers.get("content-type", "")
        body = await request.body()

        if ("json" in content_type or "text/plain" in content_type or not content_type) and body:
            try:
                json.loads(body)
            except (json.JSONDecodeError, UnicodeDecodeError):
                return JSONResponse(status_code=400, content={"detail": "Malformed JSON"})

    try:
        response = await call_next(request)
        return response
    except Exception:
        logger.exception("Unhandled error")
        return JSONResponse(status_code=400, content={"detail": "Request processing error"})
