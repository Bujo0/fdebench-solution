# Copyright (c) Microsoft. All rights reserved.
"""Pydantic models for evaluation tickets and gold answers.

These models enforce the exact schemas defined in
docs/data/schemas/input.json and docs/data/schemas/output.json.
"""

from ms.common.models.base import FrozenBaseModel
from ms.evals.constants import Category
from ms.evals.constants import Channel
from ms.evals.constants import MissingInfoField
from ms.evals.constants import Priority
from ms.evals.constants import Team


class Reporter(FrozenBaseModel):
    """Ticket reporter information."""

    name: str
    email: str
    department: str


class EvalTicket(FrozenBaseModel):
    """An IT support ticket used as evaluation input.

    Matches the schema in docs/data/schemas/input.json.
    """

    ticket_id: str
    subject: str
    description: str
    reporter: Reporter
    created_at: str
    channel: Channel
    attachments: list[str] = []


class GoldAnswer(FrozenBaseModel):
    """Expected triage output for an evaluation ticket.

    Matches the schema in docs/data/schemas/output.json.
    """

    ticket_id: str
    category: Category
    priority: Priority
    assigned_team: Team
    needs_escalation: bool
    missing_information: list[MissingInfoField]
    next_best_action: str
    remediation_steps: list[str]


class EvalCase(FrozenBaseModel):
    """A single evaluation case pairing a ticket with its gold answer."""

    ticket: EvalTicket
    gold: GoldAnswer
    tags: list[str] = []
    description: str = ""


class EvalDataset(FrozenBaseModel):
    """A named collection of evaluation cases."""

    name: str
    description: str
    cases: list[EvalCase]

    def tickets(self) -> list[dict[str, object]]:
        """Export tickets as list of dicts (compatible with run_eval.py)."""
        return [case.ticket.model_dump() for case in self.cases]

    def golds(self) -> list[dict[str, object]]:
        """Export gold answers as list of dicts (compatible with run_eval.py)."""
        return [case.gold.model_dump() for case in self.cases]
