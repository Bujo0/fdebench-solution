# Multi-stage build for minimal image size + fast cold start
FROM python:3.12-slim AS builder

# Install uv for fast dependency installation
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /app

# Copy dependency files first (cache layer)
COPY py/pyproject.toml py/uv.lock ./py/
COPY py/apps/sample/pyproject.toml ./py/apps/sample/
COPY py/common/ ./py/common/

# Install dependencies
RUN cd py && uv sync --package sample --no-dev --frozen

# Copy application code
COPY py/apps/sample/ ./py/apps/sample/
COPY py/data/ ./py/data/
COPY docs/challenge/task1/routing_guide.md ./docs/challenge/task1/routing_guide.md

# Production stage
FROM python:3.12-slim

WORKDIR /app

# Copy installed packages and app from builder
COPY --from=builder /app/py/.venv /app/py/.venv
COPY --from=builder /app/py/apps/sample /app/py/apps/sample
COPY --from=builder /app/py/data /app/py/data
COPY --from=builder /app/py/common /app/py/common
COPY --from=builder /app/docs /app/docs

# Set Python path for namespace packages
ENV PYTHONPATH="/app/py/common/libs/models/src:/app/py/common/libs/fdebenchkit/src:/app/py/common/libs/fastapi/src"
ENV PATH="/app/py/.venv/bin:$PATH"

# Health check
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

EXPOSE 8000

# Run with uvicorn - 2 workers for concurrency, fast startup
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2", "--app-dir", "/app/py/apps/sample"]
