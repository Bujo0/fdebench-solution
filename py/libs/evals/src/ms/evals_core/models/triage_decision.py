# Copyright (c) Microsoft. All rights reserved.
"""Triage decision model matching docs/data/schemas/output.json."""

from ms.common.models.base import FrozenBaseModel
from ms.evals_core.constants import Category
from ms.evals_core.constants import MissingInfo
from ms.evals_core.constants import Priority
from ms.evals_core.constants import Team


class TriageDecision(FrozenBaseModel):
    """Expected triage output for a single ticket.

    Matches the JSON schema at docs/data/schemas/output.json.
    """

    ticket_id: str
    category: Category
    priority: Priority
    assigned_team: Team
    needs_escalation: bool
    missing_information: list[MissingInfo]
    next_best_action: str
    remediation_steps: list[str]
