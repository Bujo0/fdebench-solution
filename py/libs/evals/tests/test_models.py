# Copyright (c) Microsoft. All rights reserved.
"""Tests for Pydantic model validation."""

import pytest
from pydantic import ValidationError

from ms.evals.models import AssignedTeam
from ms.evals.models import Category
from ms.evals.models import GoldAnswer
from ms.evals.models import MissingInfoItem
from ms.evals.models import Reporter
from ms.evals.models import Ticket
from ms.evals.models import TriageResponse


class TestTicketModel:
    def test_valid_ticket(self) -> None:
        t = Ticket(
            ticket_id="INC-0001",
            subject="Test",
            description="A test ticket",
            reporter=Reporter(name="Alice", email="alice@contoso.com", department="IT"),
            created_at="2026-03-18T00:00:00Z",
            channel="email",
        )
        assert t.ticket_id == "INC-0001"
        assert t.channel == "email"
        assert t.attachments == []

    def test_invalid_channel_rejected(self) -> None:
        with pytest.raises(ValidationError):
            Ticket(
                ticket_id="INC-0001",
                subject="Test",
                description="Test",
                reporter=Reporter(name="Alice", email="a@b.com", department="IT"),
                created_at="2026-03-18T00:00:00Z",
                channel="fax",
            )

    def test_immutable(self) -> None:
        t = Ticket(
            ticket_id="INC-0001",
            subject="Test",
            description="Test",
            reporter=Reporter(name="Alice", email="a@b.com", department="IT"),
            created_at="2026-03-18T00:00:00Z",
            channel="email",
        )
        with pytest.raises(ValidationError):
            t.subject = "Changed"


class TestGoldAnswerModel:
    def test_valid_gold(self) -> None:
        g = GoldAnswer(
            ticket_id="INC-0001",
            category="Security & Compliance",
            priority="P1",
            assigned_team="Security Operations",
            needs_escalation=True,
            missing_information=["timestamp", "error_message"],
            next_best_action="Investigate immediately",
            remediation_steps=["Step 1", "Step 2"],
        )
        assert g.category == Category.SECURITY
        assert g.assigned_team == AssignedTeam.SECURITY_OPS
        assert len(g.missing_information) == 2

    def test_invalid_category_rejected(self) -> None:
        with pytest.raises(ValidationError):
            GoldAnswer(
                ticket_id="INC-0001",
                category="Invalid Category",
                priority="P1",
                assigned_team="Security Operations",
                needs_escalation=False,
                missing_information=[],
                next_best_action="",
                remediation_steps=[],
            )

    def test_invalid_team_rejected(self) -> None:
        with pytest.raises(ValidationError):
            GoldAnswer(
                ticket_id="INC-0001",
                category="Security & Compliance",
                priority="P1",
                assigned_team="Made Up Team",
                needs_escalation=False,
                missing_information=[],
                next_best_action="",
                remediation_steps=[],
            )

    def test_invalid_priority_rejected(self) -> None:
        with pytest.raises(ValidationError):
            GoldAnswer(
                ticket_id="INC-0001",
                category="Security & Compliance",
                priority="P5",
                assigned_team="Security Operations",
                needs_escalation=False,
                missing_information=[],
                next_best_action="",
                remediation_steps=[],
            )

    def test_invalid_missing_info_rejected(self) -> None:
        with pytest.raises(ValidationError):
            GoldAnswer(
                ticket_id="INC-0001",
                category="Security & Compliance",
                priority="P1",
                assigned_team="Security Operations",
                needs_escalation=False,
                missing_information=["not_a_valid_field"],
                next_best_action="",
                remediation_steps=[],
            )


class TestTriageResponseModel:
    def test_accepts_any_string_values(self) -> None:
        """TriageResponse is deliberately permissive — scoring handles validation."""
        r = TriageResponse(
            ticket_id="INC-0001",
            category="Anything Goes",
            priority="P99",
            assigned_team="Unknown Team",
            needs_escalation=True,
            missing_information=["made_up"],
            next_best_action="Whatever",
            remediation_steps=["Step"],
        )
        assert r.category == "Anything Goes"


class TestEnumValues:
    def test_all_categories(self) -> None:
        expected = {
            "Access & Authentication",
            "Hardware & Peripherals",
            "Network & Connectivity",
            "Software & Applications",
            "Security & Compliance",
            "Data & Storage",
            "General Inquiry",
            "Not a Support Ticket",
        }
        assert {c.value for c in Category} == expected

    def test_all_teams(self) -> None:
        expected = {
            "Identity & Access Management",
            "Endpoint Engineering",
            "Network Operations",
            "Enterprise Applications",
            "Security Operations",
            "Data Platform",
            "None",
        }
        assert {t.value for t in AssignedTeam} == expected

    def test_all_missing_info(self) -> None:
        expected = {
            "affected_system",
            "error_message",
            "steps_to_reproduce",
            "affected_users",
            "environment_details",
            "timestamp",
            "previous_ticket_id",
            "contact_info",
            "device_info",
            "application_version",
            "network_location",
            "business_impact",
            "reproduction_frequency",
            "screenshot_or_attachment",
            "authentication_method",
            "configuration_details",
        }
        assert {m.value for m in MissingInfoItem} == expected
