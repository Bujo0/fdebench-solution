"""Tests for evaluation domain models."""

import pytest
from pydantic import ValidationError

from ms.libs.evals.models.enums import (
    AssignedTeam,
    MissingInfoField,
    Priority,
    ScenarioTag,
    TicketCategory,
    TicketChannel,
)
from ms.libs.evals.models.scenario import (
    EvalScenario,
    Reporter,
    Ticket,
    TriageDecision,
)


def _make_ticket(**overrides: object) -> dict:
    """Create a valid ticket dict with optional overrides."""
    defaults: dict = {
        "ticket_id": "INC-0001",
        "subject": "Test subject",
        "description": "Test description",
        "reporter": {"name": "Test User", "email": "test@contoso.com", "department": "Engineering"},
        "created_at": "2026-03-18T10:00:00Z",
        "channel": "portal",
        "attachments": [],
    }
    defaults.update(overrides)
    return defaults


def _make_gold(**overrides: object) -> dict:
    """Create a valid gold answer dict with optional overrides."""
    defaults: dict = {
        "ticket_id": "INC-0001",
        "category": "Network & Connectivity",
        "priority": "P3",
        "assigned_team": "Network Operations",
        "needs_escalation": False,
        "missing_information": [],
        "next_best_action": "Investigate the issue.",
        "remediation_steps": ["Step 1: Check connectivity"],
    }
    defaults.update(overrides)
    return defaults


class TestReporter:
    def test_valid_reporter(self) -> None:
        reporter = Reporter(name="Test", email="test@contoso.com", department="IT")
        assert reporter.name == "Test"
        assert reporter.email == "test@contoso.com"

    def test_reporter_missing_field(self) -> None:
        with pytest.raises(ValidationError):
            Reporter(name="Test", email="test@contoso.com")  # type: ignore[call-arg]


class TestTicket:
    def test_valid_ticket(self) -> None:
        ticket = Ticket(**_make_ticket())
        assert ticket.ticket_id == "INC-0001"
        assert ticket.channel == TicketChannel.PORTAL

    def test_invalid_ticket_id_pattern(self) -> None:
        with pytest.raises(ValidationError):
            Ticket(**_make_ticket(ticket_id="TICKET-001"))

    def test_invalid_channel(self) -> None:
        with pytest.raises(ValidationError):
            Ticket(**_make_ticket(channel="fax"))

    def test_empty_attachments_default(self) -> None:
        data = _make_ticket()
        del data["attachments"]
        ticket = Ticket(**data)
        assert ticket.attachments == []


class TestTriageDecision:
    def test_valid_triage_decision(self) -> None:
        gold = TriageDecision(**_make_gold())
        assert gold.category == TicketCategory.NETWORK
        assert gold.priority == Priority.P3

    def test_invalid_category(self) -> None:
        with pytest.raises(ValidationError):
            TriageDecision(**_make_gold(category="Invalid Category"))

    def test_invalid_priority(self) -> None:
        with pytest.raises(ValidationError):
            TriageDecision(**_make_gold(priority="P5"))

    def test_invalid_team(self) -> None:
        with pytest.raises(ValidationError):
            TriageDecision(**_make_gold(assigned_team="Dream Team"))

    def test_invalid_missing_info_field(self) -> None:
        with pytest.raises(ValidationError):
            TriageDecision(**_make_gold(missing_information=["not_a_real_field"]))

    def test_empty_remediation_steps_rejected(self) -> None:
        with pytest.raises(ValidationError):
            TriageDecision(**_make_gold(remediation_steps=[]))

    def test_all_categories(self) -> None:
        for cat in TicketCategory:
            gold = TriageDecision(**_make_gold(category=cat.value))
            assert gold.category == cat

    def test_all_teams(self) -> None:
        for team in AssignedTeam:
            gold = TriageDecision(**_make_gold(assigned_team=team.value))
            assert gold.assigned_team == team

    def test_all_missing_info_fields(self) -> None:
        for field_val in MissingInfoField:
            gold = TriageDecision(**_make_gold(missing_information=[field_val.value]))
            assert gold.missing_information == [field_val]


class TestEvalScenario:
    def test_valid_scenario(self) -> None:
        scenario = EvalScenario(
            ticket=Ticket(**_make_ticket()),
            gold=TriageDecision(**_make_gold()),
            tag=ScenarioTag.DATA_CLEANUP,
            test_name="test_scenario",
            test_description="A test scenario",
        )
        assert scenario.tag == ScenarioTag.DATA_CLEANUP
        assert scenario.test_name == "test_scenario"

    def test_ticket_id_mismatch_allowed(self) -> None:
        """Scenario doesn't enforce ticket_id match — that's the exporter's job."""
        EvalScenario(
            ticket=Ticket(**_make_ticket(ticket_id="INC-0001")),
            gold=TriageDecision(**_make_gold(ticket_id="INC-0002")),
            tag=ScenarioTag.RESPONSIBLE_AI,
            test_name="mismatch_test",
            test_description="Mismatched IDs",
        )
