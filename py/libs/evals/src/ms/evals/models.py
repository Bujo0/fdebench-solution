"""Pydantic models for eval ticket generation."""

from pydantic import Field

from ms.common.models.base import FrozenBaseModel
from ms.evals.constants import Category
from ms.evals.constants import Channel
from ms.evals.constants import MissingInfo
from ms.evals.constants import Priority
from ms.evals.constants import Team


class Reporter(FrozenBaseModel):
    """Ticket reporter information."""

    name: str
    email: str
    department: str


class Ticket(FrozenBaseModel):
    """An IT support ticket matching the input schema."""

    ticket_id: str
    subject: str
    description: str
    reporter: Reporter
    created_at: str
    channel: Channel
    attachments: list[str] = Field(default_factory=list)


class GoldAnswer(FrozenBaseModel):
    """Expected triage output matching the output schema."""

    ticket_id: str
    category: Category
    priority: Priority
    assigned_team: Team
    needs_escalation: bool
    missing_information: list[MissingInfo]
    next_best_action: str
    remediation_steps: list[str]


class Scenario(FrozenBaseModel):
    """A complete eval scenario: ticket + gold answer pair."""

    ticket: Ticket
    gold: GoldAnswer
    tags: list[str] = Field(default_factory=list)
    difficulty: str = "medium"
