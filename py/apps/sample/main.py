"""FDEBench AI-powered solution — FastAPI app factory.

Run:
    cd py
    make setup     # once — install deps
    make run       # start on :8000

Score:
    make eval      # score all 3 tasks (in a second terminal)
"""

import logging
from contextlib import asynccontextmanager

import httpx
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from config import Settings
from llm_client import get_client
from middleware import error_handling_middleware, validation_error_handler
from prompts.triage_prompt import load_few_shot_examples, load_routing_guide
from routers import extract, orchestrate, triage

import state

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    state.settings = Settings()
    state.aoai_client = get_client(state.settings)
    state.tool_http_client = httpx.AsyncClient(timeout=httpx.Timeout(20.0), follow_redirects=True)
    state.ROUTING_GUIDE = load_routing_guide()
    state.FEW_SHOT_EXAMPLES = load_few_shot_examples()
    logger.info(
        "Loaded routing guide (%d chars), %d few-shot examples",
        len(state.ROUTING_GUIDE),
        state.FEW_SHOT_EXAMPLES.count("<example>"),
    )
    yield
    await state.tool_http_client.aclose()


app = FastAPI(title="FDEBench Solution", lifespan=lifespan)

app.add_exception_handler(RequestValidationError, validation_error_handler)
app.middleware("http")(error_handling_middleware)

app.include_router(triage.router)
app.include_router(extract.router)
app.include_router(orchestrate.router)


@app.get("/health")
async def health() -> dict:
    return {"status": "ok"}
