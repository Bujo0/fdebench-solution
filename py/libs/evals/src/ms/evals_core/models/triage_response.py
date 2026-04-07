# Copyright (c) Microsoft. All rights reserved.
"""Pydantic models for triage response output."""

from ms.common.models.base import FrozenBaseModel
from ms.evals_core.constants import AssignedTeam
from ms.evals_core.constants import Category
from ms.evals_core.constants import MissingInfoField
from ms.evals_core.constants import Priority


class TriageResponse(FrozenBaseModel):
    """Expected triage output for a single ticket.

    Matches the output schema defined in docs/data/schemas/output.json.
    All fields are required per the scoring contract.
    """

    ticket_id: str
    category: Category
    priority: Priority
    assigned_team: AssignedTeam
    needs_escalation: bool
    missing_information: list[MissingInfoField]
    next_best_action: str
    remediation_steps: list[str]
