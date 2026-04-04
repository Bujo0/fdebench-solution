# Copyright (c) Microsoft. All rights reserved.
"""Pydantic models for evaluation results — scoring, runner, and dataset loading.

These models define the domain types used by the evaluation execution framework
(as opposed to the scenario generation models in ``ms.evals_core.models``).

All domain values (categories, teams, priorities, missing-info vocabulary)
are imported from ``ms.evals_core.constants`` to maintain a single source of truth.
"""

from ms.common.models.base import FrozenBaseModel
from ms.evals_core.constants import Category
from ms.evals_core.constants import Channel
from ms.evals_core.constants import MissingInfo
from ms.evals_core.constants import Priority
from ms.evals_core.constants import Team

# Aliases for backward compatibility with test suites.
AssignedTeam = Team
MissingInfoItem = MissingInfo


class Reporter(FrozenBaseModel):
    """Ticket reporter information."""

    name: str
    email: str
    department: str


class Ticket(FrozenBaseModel):
    """An IT support ticket as input to the triage system."""

    ticket_id: str
    subject: str
    description: str
    reporter: Reporter
    created_at: str
    channel: Channel
    attachments: list[str] = []


class TriageResponse(FrozenBaseModel):
    """Expected triage output from the system under test.

    Uses loose ``str`` types because responses come from an external endpoint
    and may contain unexpected values that should still be score-able.
    """

    ticket_id: str
    category: str
    priority: str
    assigned_team: str
    needs_escalation: bool
    missing_information: list[str]
    next_best_action: str
    remediation_steps: list[str]


class GoldAnswer(FrozenBaseModel):
    """Gold-standard triage decision for scoring.

    Uses strict enum types so validation rejects malformed gold data early.
    """

    ticket_id: str
    category: Category
    priority: Priority
    assigned_team: Team
    needs_escalation: bool
    missing_information: list[MissingInfo]
    next_best_action: str
    remediation_steps: list[str]


class DimensionScores(FrozenBaseModel):
    """Per-ticket scores for each classification dimension."""

    category: float
    priority: float
    routing: float
    escalation: float
    missing_info: float
    weighted_total: float


class EvalResult(FrozenBaseModel):
    """Evaluation result for a single ticket."""

    ticket_id: str
    scores: DimensionScores
    response: TriageResponse
    gold: GoldAnswer
    latency_ms: float
    error: str | None = None


class DimensionAggregates(FrozenBaseModel):
    """Aggregate scores across all tickets for each dimension."""

    category: float
    priority: float
    routing: float
    missing_info: float
    escalation: float


class EvalSummary(FrozenBaseModel):
    """Summary of an evaluation run across all tickets."""

    dataset_kind: str
    tickets_total: int
    tickets_scored: int
    tickets_errored: int
    dimension_scores: DimensionAggregates
    classification_score: float
    results: list[EvalResult]
