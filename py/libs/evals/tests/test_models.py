# Copyright (c) Microsoft. All rights reserved.
"""Tests for evaluation Pydantic models."""

import pytest
from pydantic import ValidationError

from ms.evals_core.models.scenario import Scenario
from ms.evals_core.models.ticket import Reporter
from ms.evals_core.models.ticket import Ticket
from ms.evals_core.models.triage_decision import TriageDecision


class TestTicketModel:
    def test_valid_ticket(self) -> None:
        ticket = Ticket(
            ticket_id="INC-0001",
            subject="Test subject",
            description="Test description",
            reporter=Reporter(name="Alice", email="alice@contoso.com", department="IT"),
            created_at="2026-03-18T09:00:00Z",
            channel="email",
        )
        assert ticket.ticket_id == "INC-0001"
        assert ticket.attachments == []

    def test_invalid_channel_rejected(self) -> None:
        with pytest.raises(ValidationError, match="channel"):
            Ticket(
                ticket_id="INC-0001",
                subject="Test",
                description="Test",
                reporter=Reporter(name="A", email="a@c.com", department="IT"),
                created_at="2026-03-18T09:00:00Z",
                channel="fax",  # type: ignore[arg-type]
            )

    def test_ticket_is_frozen(self) -> None:
        ticket = Ticket(
            ticket_id="INC-0001",
            subject="Test",
            description="Test",
            reporter=Reporter(name="A", email="a@c.com", department="IT"),
            created_at="2026-03-18T09:00:00Z",
            channel="portal",
        )
        with pytest.raises(ValidationError):
            ticket.subject = "Modified"  # type: ignore[misc]


class TestTriageDecisionModel:
    def test_valid_decision(self) -> None:
        decision = TriageDecision(
            ticket_id="INC-0001",
            category="Network & Connectivity",
            priority="P2",
            assigned_team="Network Operations",
            needs_escalation=False,
            missing_information=["error_message"],
            next_best_action="Investigate the issue.",
            remediation_steps=["Step 1", "Step 2"],
        )
        assert decision.category == "Network & Connectivity"

    def test_invalid_category_rejected(self) -> None:
        with pytest.raises(ValidationError, match="category"):
            TriageDecision(
                ticket_id="INC-0001",
                category="Invalid Category",  # type: ignore[arg-type]
                priority="P2",
                assigned_team="Network Operations",
                needs_escalation=False,
                missing_information=[],
                next_best_action="Test",
                remediation_steps=["Step 1"],
            )

    def test_invalid_priority_rejected(self) -> None:
        with pytest.raises(ValidationError, match="priority"):
            TriageDecision(
                ticket_id="INC-0001",
                category="Network & Connectivity",
                priority="P0",  # type: ignore[arg-type]
                assigned_team="Network Operations",
                needs_escalation=False,
                missing_information=[],
                next_best_action="Test",
                remediation_steps=["Step 1"],
            )

    def test_invalid_team_rejected(self) -> None:
        with pytest.raises(ValidationError, match="assigned_team"):
            TriageDecision(
                ticket_id="INC-0001",
                category="Network & Connectivity",
                priority="P2",
                assigned_team="Root Access Team",  # type: ignore[arg-type]
                needs_escalation=False,
                missing_information=[],
                next_best_action="Test",
                remediation_steps=["Step 1"],
            )

    def test_invalid_missing_info_rejected(self) -> None:
        with pytest.raises(ValidationError, match="missing_information"):
            TriageDecision(
                ticket_id="INC-0001",
                category="Network & Connectivity",
                priority="P2",
                assigned_team="Network Operations",
                needs_escalation=False,
                missing_information=["invalid_field"],  # type: ignore[list-item]
                next_best_action="Test",
                remediation_steps=["Step 1"],
            )

    def test_decision_is_frozen(self) -> None:
        decision = TriageDecision(
            ticket_id="INC-0001",
            category="Network & Connectivity",
            priority="P2",
            assigned_team="Network Operations",
            needs_escalation=False,
            missing_information=[],
            next_best_action="Test",
            remediation_steps=["Step 1"],
        )
        with pytest.raises(ValidationError):
            decision.priority = "P1"  # type: ignore[misc]


class TestScenarioModel:
    def test_valid_scenario(self) -> None:
        scenario = Scenario(
            ticket=Ticket(
                ticket_id="INC-0001",
                subject="Test",
                description="Test",
                reporter=Reporter(name="A", email="a@c.com", department="IT"),
                created_at="2026-03-18T09:00:00Z",
                channel="portal",
            ),
            gold=TriageDecision(
                ticket_id="INC-0001",
                category="General Inquiry",
                priority="P4",
                assigned_team="Endpoint Engineering",
                needs_escalation=False,
                missing_information=[],
                next_best_action="Test",
                remediation_steps=["Step 1"],
            ),
            scenario_category="data_cleanup",
            scenario_tag="test_tag",
            description="A test scenario.",
        )
        assert scenario.scenario_category == "data_cleanup"

    def test_invalid_scenario_category_rejected(self) -> None:
        with pytest.raises(ValidationError, match="scenario_category"):
            Scenario(
                ticket=Ticket(
                    ticket_id="INC-0001",
                    subject="Test",
                    description="Test",
                    reporter=Reporter(name="A", email="a@c.com", department="IT"),
                    created_at="2026-03-18T09:00:00Z",
                    channel="portal",
                ),
                gold=TriageDecision(
                    ticket_id="INC-0001",
                    category="General Inquiry",
                    priority="P4",
                    assigned_team="Endpoint Engineering",
                    needs_escalation=False,
                    missing_information=[],
                    next_best_action="Test",
                    remediation_steps=["Step 1"],
                ),
                scenario_category="invalid_category",  # type: ignore[arg-type]
                scenario_tag="test",
                description="Test",
            )
