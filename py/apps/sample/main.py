"""Minimal FDEBench starter — stub endpoints that pass schema validation.

Run:
    cd py
    make setup     # once — install deps
    make run       # start on :8000

Score:
    make eval      # score all 3 tasks (in a second terminal)

Every endpoint returns valid stub JSON. The eval harness will run
end-to-end and show you the full scoring breakdown. Replace the stub
logic with your LLM calls to improve the scores.
"""

from fastapi import FastAPI
from fastapi import Response
from models import Category
from models import ExtractRequest
from models import ExtractResponse
from models import OrchestrateRequest
from models import OrchestrateResponse
from models import Team
from models import TriageRequest
from models import TriageResponse

app = FastAPI(title="FDEBench Starter")

MODEL_NAME = "gpt-4.1-mini"  # Change to whatever model you use


def _add_headers(response: Response) -> None:
    """Add cost-tracking headers. The platform reads X-Model-Name for cost scoring."""
    response.headers["X-Model-Name"] = MODEL_NAME


# ── Health ───────────────────────────────────────────────────────────


@app.get("/health")
async def health() -> dict:
    return {"status": "ok"}


# ── Task 1: Signal Triage ────────────────────────────────────────────


@app.post("/triage")
async def triage(req: TriageRequest, response: Response) -> TriageResponse:
    _add_headers(response)
    # TODO: replace with LLM classification
    return TriageResponse(
        ticket_id=req.ticket_id,
        category=Category.BRIEFING,
        priority="P3",
        assigned_team=Team.SYSTEMS,
        needs_escalation=False,
        missing_information=[],
        next_best_action="Investigate the reported issue.",
        remediation_steps=["Review the signal details.", "Route to the appropriate team."],
    )


# ── Task 2: Document Extraction ─────────────────────────────────────


@app.post("/extract")
async def extract(req: ExtractRequest, response: Response) -> ExtractResponse:
    _add_headers(response)
    # TODO: replace with vision model extraction using req.json_schema
    return ExtractResponse(document_id=req.document_id)


# ── Task 3: Workflow Orchestration ───────────────────────────────────


@app.post("/orchestrate")
async def orchestrate(req: OrchestrateRequest, response: Response) -> OrchestrateResponse:
    _add_headers(response)
    # TODO: replace with LLM planning + tool execution
    return OrchestrateResponse(
        task_id=req.task_id,
        status="completed",
        steps_executed=[],
        constraints_satisfied=[],
    )
