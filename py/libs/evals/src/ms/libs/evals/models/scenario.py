"""Domain models for evaluation scenarios."""

from pydantic import BaseModel, Field

from ms.libs.evals.models.enums import (
    AssignedTeam,
    MissingInfoField,
    Priority,
    ScenarioTag,
    TicketCategory,
    TicketChannel,
)


class Reporter(BaseModel):
    """Ticket reporter information."""

    name: str
    email: str
    department: str


class Ticket(BaseModel):
    """An IT support ticket submitted to the triage API."""

    ticket_id: str = Field(pattern=r"^INC-[0-9]+$")
    subject: str
    description: str
    reporter: Reporter
    created_at: str = Field(description="ISO 8601 timestamp")
    channel: TicketChannel
    attachments: list[str] = Field(default_factory=list)


class TriageDecision(BaseModel):
    """Expected triage output for a single ticket (gold standard)."""

    ticket_id: str = Field(pattern=r"^INC-[0-9]+$")
    category: TicketCategory
    priority: Priority
    assigned_team: AssignedTeam
    needs_escalation: bool
    missing_information: list[MissingInfoField]
    next_best_action: str
    remediation_steps: list[str] = Field(min_length=1)


class EvalScenario(BaseModel):
    """A single evaluation scenario: a ticket paired with its gold answer and test metadata."""

    ticket: Ticket
    gold: TriageDecision
    tag: ScenarioTag
    test_name: str = Field(description="Short identifier for what this scenario tests")
    test_description: str = Field(description="Explanation of the adversarial or edge-case property")
