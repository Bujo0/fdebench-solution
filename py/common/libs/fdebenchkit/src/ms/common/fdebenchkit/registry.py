"""Task registry for FDEBench Tier 1 functional scoring.

Each task declares its endpoint, identifier key, response contract, and
dimension weights. The runner uses this registry to load datasets,
run preflight validation, and dispatch to the correct deterministic scorer.
"""

from collections.abc import Callable
from dataclasses import dataclass
from typing import Any

from ms.common.fdebenchkit.scorers import document_extraction as scoring_document_extraction
from ms.common.fdebenchkit.scorers import ticket_triage as ticket_triage_scoring
from ms.common.fdebenchkit.scorers import workflow_orchestration as scoring_workflow_orchestration

ScorerFn = Callable[[list[dict[str, Any]], list[dict[str, Any]]], dict[str, Any]]


@dataclass(frozen=True)
class TaskDefinition:
    """Static configuration for one deterministic benchmark task."""

    task_id: str
    label: str
    endpoint_path: str
    request_id_key: str
    item_label: str
    response_required_keys: frozenset[str]
    dimension_weights: dict[str, float]
    scorer: ScorerFn
    # Per-task latency normalization thresholds (P95 ms).
    # Different tasks have different expected latency profiles:
    # - Text classification (triage): fast, ~500ms-3s
    # - Vision/OCR (extract): slow, ~2s-20s
    # - Multi-step orchestration: medium, ~1s-8s
    latency_best_ms: float = 500.0
    latency_worst_ms: float = 5000.0


@dataclass(frozen=True)
class TaskRun:
    """Concrete dataset bundle for one task run."""

    definition: TaskDefinition
    input_items: list[dict[str, Any]]
    gold_items: list[dict[str, Any]]

    @property
    def smoke_request(self) -> dict[str, Any]:
        """Return the first candidate request payload for preflight validation."""
        if not self.input_items:
            msg = f"Task {self.definition.task_id} has no input items"
            raise ValueError(msg)
        return self.input_items[0]


TASK_DEFINITIONS: dict[str, TaskDefinition] = {
    "ticket_triage": TaskDefinition(
        task_id="ticket_triage",
        label="Task 1: Ticket Triage",
        endpoint_path="/triage",
        request_id_key="ticket_id",
        item_label="ticket",
        response_required_keys=frozenset(
            {
                "ticket_id",
                "category",
                "priority",
                "assigned_team",
                "needs_escalation",
                "missing_information",
                "next_best_action",
                "remediation_steps",
            }
        ),
        dimension_weights={
            "category": ticket_triage_scoring.WEIGHT_CATEGORY,
            "priority": ticket_triage_scoring.WEIGHT_PRIORITY,
            "routing": ticket_triage_scoring.WEIGHT_ROUTING,
            "missing_info": ticket_triage_scoring.WEIGHT_MISSING_INFO,
            "escalation": ticket_triage_scoring.WEIGHT_ESCALATION,
        },
        scorer=ticket_triage_scoring.score_submission,
    ),
    "document_extraction": TaskDefinition(
        task_id="document_extraction",
        label="Task 2: Document Extraction",
        endpoint_path="/extract",
        request_id_key="document_id",
        item_label="document",
        response_required_keys=frozenset({"document_id"}),
        dimension_weights=scoring_document_extraction.DIMENSION_WEIGHTS,
        scorer=scoring_document_extraction.score_submission,
        # Vision/OCR is inherently slower — calibrate thresholds accordingly
        latency_best_ms=2000.0,
        latency_worst_ms=20000.0,
    ),
    "workflow_orchestration": TaskDefinition(
        task_id="workflow_orchestration",
        label="Task 3: Workflow Orchestration",
        endpoint_path="/orchestrate",
        request_id_key="task_id",
        item_label="workflow",
        response_required_keys=frozenset({"task_id", "status", "steps_executed"}),
        dimension_weights=scoring_workflow_orchestration.DIMENSION_WEIGHTS,
        scorer=scoring_workflow_orchestration.score_submission,
        # Multi-step LLM + tool calls — medium latency expected
        latency_best_ms=1000.0,
        latency_worst_ms=10000.0,
    ),
}


def get_task_definition(task_id: str) -> TaskDefinition:
    """Return one task definition or raise for an unknown task id."""
    try:
        return TASK_DEFINITIONS[task_id]
    except KeyError as exc:
        msg = f"Unknown functional scorer task: {task_id}"
        raise ValueError(msg) from exc
