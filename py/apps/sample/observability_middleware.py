"""Request-tracking and observability middleware for FastAPI.

Generates a unique request_id per request, logs request start/completion
with latency, and attaches X-Request-Id to every response.
"""

import logging
import time

from fastapi import Request
from fastapi import Response
from logging_config import new_request_id
from logging_config import request_id_var
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.middleware.base import RequestResponseEndpoint

logger = logging.getLogger("observability")


class ObservabilityMiddleware(BaseHTTPMiddleware):
    """Per-request tracking: request_id, timing, structured request/response logs."""

    async def dispatch(self, request: Request, call_next: RequestResponseEndpoint) -> Response:
        rid = request.headers.get("X-Request-Id") or new_request_id()
        token = request_id_var.set(rid)

        method = request.method
        path = request.url.path

        logger.info(
            "Request started",
            extra={"method": method, "path": path, "endpoint": path},
        )

        start = time.perf_counter()
        try:
            response = await call_next(request)
        except Exception:
            elapsed_ms = round((time.perf_counter() - start) * 1000, 1)
            logger.exception(
                "Request failed",
                extra={
                    "method": method,
                    "path": path,
                    "endpoint": path,
                    "latency_ms": elapsed_ms,
                    "status_code": 500,
                },
            )
            raise
        else:
            elapsed_ms = round((time.perf_counter() - start) * 1000, 1)
            logger.info(
                "Request completed",
                extra={
                    "method": method,
                    "path": path,
                    "endpoint": path,
                    "latency_ms": elapsed_ms,
                    "status_code": response.status_code,
                },
            )
            response.headers["X-Request-Id"] = rid
            return response
        finally:
            request_id_var.reset(token)
