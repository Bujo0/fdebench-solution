# Copyright (c) Microsoft. All rights reserved.
"""Tests for evaluation data models."""

import json

from evals.models import Category
from evals.models import Channel
from evals.models import EvalScenario
from evals.models import MissingInfoField
from evals.models import Priority
from evals.models import Reporter
from evals.models import ScenarioSuite
from evals.models import ScenarioTag
from evals.models import Team
from evals.models import Ticket
from evals.models import TriageDecision


class TestEnumValues:
    """Verify enum values match the challenge specification exactly."""

    def test_categories_count(self):
        assert len(Category) == 8

    def test_categories_values(self):
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

    def test_teams_count(self):
        assert len(Team) == 7

    def test_teams_values(self):
        expected = {
            "Identity & Access Management",
            "Endpoint Engineering",
            "Network Operations",
            "Enterprise Applications",
            "Security Operations",
            "Data Platform",
            "None",
        }
        assert {t.value for t in Team} == expected

    def test_priorities_count(self):
        assert len(Priority) == 4

    def test_priorities_values(self):
        assert {p.value for p in Priority} == {"P1", "P2", "P3", "P4"}

    def test_missing_info_count(self):
        assert len(MissingInfoField) == 16

    def test_missing_info_values(self):
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
        assert {f.value for f in MissingInfoField} == expected

    def test_channels_count(self):
        assert len(Channel) == 4

    def test_channels_values(self):
        assert {c.value for c in Channel} == {"email", "chat", "portal", "phone"}


class TestTicketModel:
    """Verify Ticket model serialization matches the input JSON schema."""

    def test_ticket_serialization_has_required_fields(self):
        ticket = Ticket(
            ticket_id="INC-0001",
            subject="Test",
            description="Test description",
            reporter=Reporter(name="Test", email="test@contoso.com", department="IT"),
            created_at="2026-03-17T09:00:00Z",
            channel=Channel.EMAIL,
        )
        data = ticket.model_dump()
        required = {"ticket_id", "subject", "description", "reporter", "created_at", "channel", "attachments"}
        assert set(data.keys()) == required

    def test_ticket_id_format(self):
        ticket = Ticket(
            ticket_id="INC-9001",
            subject="Test",
            description="Test",
            reporter=Reporter(name="Test", email="test@contoso.com", department="IT"),
            created_at="2026-03-17T09:00:00Z",
            channel=Channel.EMAIL,
        )
        assert ticket.ticket_id.startswith("INC-")

    def test_ticket_json_serializable(self):
        ticket = Ticket(
            ticket_id="INC-0001",
            subject="Test",
            description="Test",
            reporter=Reporter(name="Test", email="test@contoso.com", department="IT"),
            created_at="2026-03-17T09:00:00Z",
            channel=Channel.EMAIL,
        )
        # Should not raise
        json.dumps(ticket.model_dump())


class TestTriageDecisionModel:
    """Verify TriageDecision model serialization matches the output JSON schema."""

    def test_triage_has_all_required_fields(self):
        decision = TriageDecision(
            ticket_id="INC-0001",
            category=Category.NETWORK,
            priority=Priority.P3,
            assigned_team=Team.NETWORK_OPS,
            needs_escalation=False,
            missing_information=[],
            next_best_action="Test action",
            remediation_steps=["Step 1"],
        )
        data = decision.model_dump()
        required = {
            "ticket_id",
            "category",
            "priority",
            "assigned_team",
            "needs_escalation",
            "missing_information",
            "next_best_action",
            "remediation_steps",
        }
        assert set(data.keys()) == required

    def test_triage_json_serializable(self):
        decision = TriageDecision(
            ticket_id="INC-0001",
            category=Category.NETWORK,
            priority=Priority.P3,
            assigned_team=Team.NETWORK_OPS,
            needs_escalation=False,
            missing_information=[MissingInfoField.ERROR_MESSAGE],
            next_best_action="Test",
            remediation_steps=["Step 1"],
        )
        serialized = json.dumps(decision.model_dump())
        deserialized = json.loads(serialized)
        assert deserialized["missing_information"] == ["error_message"]

    def test_triage_missing_info_uses_enum_values(self):
        decision = TriageDecision(
            ticket_id="INC-0001",
            category=Category.NETWORK,
            priority=Priority.P3,
            assigned_team=Team.NETWORK_OPS,
            needs_escalation=False,
            missing_information=[MissingInfoField.DEVICE_INFO, MissingInfoField.ERROR_MESSAGE],
            next_best_action="Test",
            remediation_steps=["Step 1"],
        )
        data = decision.model_dump()
        for item in data["missing_information"]:
            assert item in {f.value for f in MissingInfoField}


class TestScenarioSuite:
    """Test ScenarioSuite export methods."""

    def test_get_tickets_returns_list_of_dicts(self):
        suite = ScenarioSuite(
            suite_name="Test",
            suite_description="Test suite",
            suite_type="data_cleanup",
            scenarios=[
                EvalScenario(
                    scenario_id="T-001",
                    name="Test",
                    description="Test scenario",
                    tags=[ScenarioTag.DATA_CLEANUP],
                    ticket=Ticket(
                        ticket_id="INC-0001",
                        subject="Test",
                        description="Test",
                        reporter=Reporter(name="Test", email="test@contoso.com", department="IT"),
                        created_at="2026-03-17T09:00:00Z",
                        channel=Channel.EMAIL,
                    ),
                    gold=TriageDecision(
                        ticket_id="INC-0001",
                        category=Category.NETWORK,
                        priority=Priority.P3,
                        assigned_team=Team.NETWORK_OPS,
                        needs_escalation=False,
                        missing_information=[],
                        next_best_action="Test",
                        remediation_steps=["Step 1"],
                    ),
                    rationale="Test rationale",
                ),
            ],
        )
        tickets = suite.get_tickets()
        assert len(tickets) == 1
        assert tickets[0]["ticket_id"] == "INC-0001"

    def test_get_gold_answers_returns_list_of_dicts(self):
        suite = ScenarioSuite(
            suite_name="Test",
            suite_description="Test suite",
            suite_type="data_cleanup",
            scenarios=[
                EvalScenario(
                    scenario_id="T-001",
                    name="Test",
                    description="Test scenario",
                    tags=[ScenarioTag.DATA_CLEANUP],
                    ticket=Ticket(
                        ticket_id="INC-0001",
                        subject="Test",
                        description="Test",
                        reporter=Reporter(name="Test", email="test@contoso.com", department="IT"),
                        created_at="2026-03-17T09:00:00Z",
                        channel=Channel.EMAIL,
                    ),
                    gold=TriageDecision(
                        ticket_id="INC-0001",
                        category=Category.NETWORK,
                        priority=Priority.P3,
                        assigned_team=Team.NETWORK_OPS,
                        needs_escalation=False,
                        missing_information=[],
                        next_best_action="Test",
                        remediation_steps=["Step 1"],
                    ),
                    rationale="Test rationale",
                ),
            ],
        )
        golds = suite.get_gold_answers()
        assert len(golds) == 1
        assert golds[0]["category"] == "Network & Connectivity"
