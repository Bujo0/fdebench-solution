# Copyright (c) Microsoft. All rights reserved.
"""Tests for eval-generator pydantic models."""

import pytest
from pydantic import ValidationError

from ms.eval_generator.models import VALID_CATEGORIES
from ms.eval_generator.models import VALID_CHANNELS
from ms.eval_generator.models import VALID_DEPARTMENTS
from ms.eval_generator.models import VALID_MISSING_INFO
from ms.eval_generator.models import VALID_PRIORITIES
from ms.eval_generator.models import VALID_TEAMS
from ms.eval_generator.models import Reporter
from ms.eval_generator.models import Ticket
from ms.eval_generator.models import TriageGold


class TestReporter:
    def test_create_reporter(self) -> None:
        reporter = Reporter(name="Alice Smith", email="alice.smith@contoso.com", department="Engineering")
        assert reporter.name == "Alice Smith"
        assert reporter.email == "alice.smith@contoso.com"
        assert reporter.department == "Engineering"

    def test_reporter_is_frozen(self) -> None:
        reporter = Reporter(name="Alice Smith", email="alice.smith@contoso.com", department="Engineering")
        with pytest.raises(ValidationError):
            reporter.name = "Bob"  # type: ignore[misc]


class TestTicket:
    def test_create_ticket(self) -> None:
        reporter = Reporter(name="Alice Smith", email="alice.smith@contoso.com", department="Engineering")
        ticket = Ticket(
            ticket_id="INC-0001",
            subject="Test subject",
            description="Test description",
            reporter=reporter,
            created_at="2026-03-15T10:30:00Z",
            channel="email",
        )
        assert ticket.ticket_id == "INC-0001"
        assert ticket.subject == "Test subject"
        assert ticket.channel == "email"
        assert ticket.attachments == []

    def test_create_ticket_with_attachments(self) -> None:
        reporter = Reporter(name="Alice Smith", email="alice.smith@contoso.com", department="Engineering")
        ticket = Ticket(
            ticket_id="INC-0002",
            subject="Test subject",
            description="Test description",
            reporter=reporter,
            created_at="2026-03-15T10:30:00Z",
            channel="portal",
            attachments=["screenshot.png", "debug.log"],
        )
        assert ticket.attachments == ["screenshot.png", "debug.log"]

    def test_ticket_is_frozen(self) -> None:
        reporter = Reporter(name="Alice Smith", email="alice.smith@contoso.com", department="Engineering")
        ticket = Ticket(
            ticket_id="INC-0001",
            subject="Test subject",
            description="Test description",
            reporter=reporter,
            created_at="2026-03-15T10:30:00Z",
            channel="email",
        )
        with pytest.raises(ValidationError):
            ticket.subject = "Changed"  # type: ignore[misc]


class TestTriageGold:
    def test_create_triage_gold(self) -> None:
        gold = TriageGold(
            ticket_id="INC-0001",
            category="Access & Authentication",
            priority="P2",
            assigned_team="Identity & Access Management",
            needs_escalation=False,
            missing_information=["error_message"],
            next_best_action="Check SAML configuration",
            remediation_steps=["Step 1", "Step 2"],
        )
        assert gold.ticket_id == "INC-0001"
        assert gold.category == "Access & Authentication"
        assert gold.priority == "P2"
        assert gold.needs_escalation is False
        assert gold.missing_information == ["error_message"]
        assert len(gold.remediation_steps) == 2

    def test_triage_gold_is_frozen(self) -> None:
        gold = TriageGold(
            ticket_id="INC-0001",
            category="Access & Authentication",
            priority="P2",
            assigned_team="Identity & Access Management",
            needs_escalation=False,
            missing_information=[],
            next_best_action="Check configuration",
            remediation_steps=["Step 1"],
        )
        with pytest.raises(ValidationError):
            gold.priority = "P1"  # type: ignore[misc]


class TestValidConstants:
    def test_valid_categories_not_empty(self) -> None:
        assert len(VALID_CATEGORIES) > 0

    def test_valid_priorities_are_p1_through_p4(self) -> None:
        assert frozenset({"P1", "P2", "P3", "P4"}) == VALID_PRIORITIES

    def test_valid_teams_not_empty(self) -> None:
        assert len(VALID_TEAMS) > 0

    def test_valid_channels_has_expected_values(self) -> None:
        assert frozenset({"email", "chat", "portal", "phone"}) == VALID_CHANNELS

    def test_valid_missing_info_not_empty(self) -> None:
        assert len(VALID_MISSING_INFO) > 0

    def test_valid_departments_not_empty(self) -> None:
        assert len(VALID_DEPARTMENTS) > 0
