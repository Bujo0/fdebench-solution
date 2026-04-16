"""Structured JSON logging setup for FDEBench solution.

Provides:
- JSONFormatter: emits each log record as a single JSON line
- request_id_var: ContextVar for per-request correlation
- setup_logging(): call once at startup to wire everything up
"""

import json
import logging
import sys
import uuid
from contextvars import ContextVar

request_id_var: ContextVar[str] = ContextVar("request_id", default="")


def new_request_id() -> str:
    """Generate a short request ID (first 12 chars of a UUID4)."""
    return uuid.uuid4().hex[:12]


class JSONFormatter(logging.Formatter):
    """Emit log records as single-line JSON objects."""

    def format(self, record: logging.LogRecord) -> str:
        log_obj: dict = {
            "timestamp": self.formatTime(record),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "request_id": request_id_var.get(""),
        }
        if record.exc_info and record.exc_info[0] is not None:
            log_obj["exception"] = self.formatException(record.exc_info)
        # Structured extra fields added via `extra={...}` or LoggerAdapter
        for key in (
            "task",
            "model",
            "latency_ms",
            "llm_latency_ms",
            "status_code",
            "endpoint",
            "method",
            "path",
            "tool_calls",
            "iterations",
            "success",
            "document_id",
            "ticket_id",
            "task_id",
        ):
            if hasattr(record, key):
                log_obj[key] = getattr(record, key)
        return json.dumps(log_obj)


def setup_logging(level: str = "INFO") -> None:
    """Configure the root logger with structured JSON output to stdout."""
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JSONFormatter())
    logging.root.handlers = [handler]
    logging.root.setLevel(getattr(logging, level.upper(), logging.INFO))
