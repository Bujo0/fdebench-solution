# Copyright (c) Microsoft. All rights reserved.
"""Tests for the eval dataset generator."""

import random
from datetime import datetime
from datetime import timezone

import pytest
from pydantic import ValidationError

from ms.evals.constants import Category
from ms.evals.constants import Channel
from ms.evals.constants import MissingInfo
from ms.evals.constants import Priority
from ms.evals.constants import Team
from ms.evals.generator import generate_dataset
from ms.evals.generator import generate_ticket_pair
from ms.evals.models import ScenarioTemplate
from ms.evals.validator import validate_dataset
from ms.evals.validator import validate_gold
from ms.evals.validator import validate_ticket


def _make_test_scenario() -> ScenarioTemplate:
    return ScenarioTemplate(
        scenario_id="test-001",
        category=Category.ACCESS_AUTH,
        priority=Priority.P3,
        assigned_team=Team.IAM,
        needs_escalation=False,
        missing_information=[MissingInfo.DEVICE_INFO],
        subjects=["Test subject A", "Test subject B"],
        descriptions=["Test description A.", "Test description B."],
        next_best_actions=["Check the system."],
        remediation_steps=[["Step 1", "Step 2", "Step 3"]],
    )


class TestScenarioTemplate:
    def test_create_scenario(self) -> None:
        scenario = _make_test_scenario()
        assert scenario.scenario_id == "test-001"
        assert scenario.category == Category.ACCESS_AUTH
        assert scenario.priority == Priority.P3
        assert len(scenario.subjects) == 2

    def test_scenario_is_frozen(self) -> None:
        scenario = _make_test_scenario()
        with pytest.raises(ValidationError):
            scenario.priority = Priority.P1  # type: ignore[misc]


class TestGenerateTicketPair:
    def test_generates_valid_ticket(self) -> None:
        scenario = _make_test_scenario()
        rng = random.Random(42)
        base_date = datetime(2026, 3, 15, tzinfo=timezone.utc)

        ticket, gold, mods = generate_ticket_pair(
            ticket_id="INC-9999",
            scenario=scenario,
            channel="email",
            rng=rng,
            base_date=base_date,
            modifiers=[],
        )

        assert ticket.ticket_id == "INC-9999"
        assert ticket.channel == "email"
        assert ticket.reporter.email.endswith("@contoso.com")
        assert ticket.subject in scenario.subjects

        assert gold.ticket_id == "INC-9999"
        assert gold.category == "Access & Authentication"
        assert gold.priority == "P3"
        assert gold.assigned_team == "Identity & Access Management"
        assert gold.needs_escalation is False
        assert gold.missing_information == ["device_info"]

    def test_modifiers_change_content(self) -> None:
        scenario = _make_test_scenario()
        rng = random.Random(42)
        base_date = datetime(2026, 3, 15, tzinfo=timezone.utc)

        _, _, _ = generate_ticket_pair(
            ticket_id="INC-8001",
            scenario=scenario,
            channel="chat",
            rng=rng,
            base_date=base_date,
            modifiers=[],
        )

        rng2 = random.Random(42)
        ticket_mod, _, mods = generate_ticket_pair(
            ticket_id="INC-8002",
            scenario=scenario,
            channel="chat",
            rng=rng2,
            base_date=base_date,
            modifiers=["frustrated"],
        )
        assert "frustrated" in mods


class TestValidation:
    def test_valid_ticket_passes(self) -> None:
        scenario = _make_test_scenario()
        rng = random.Random(42)
        base_date = datetime(2026, 3, 15, tzinfo=timezone.utc)

        ticket, gold, _ = generate_ticket_pair(
            ticket_id="INC-7001",
            scenario=scenario,
            channel="portal",
            rng=rng,
            base_date=base_date,
            modifiers=[],
        )

        assert validate_ticket(ticket) == []
        assert validate_gold(gold) == []


class TestGenerateDataset:
    def test_small_dataset(self) -> None:
        tickets, golds, stats = generate_dataset(count=50, seed=123)
        assert len(tickets) == 50
        assert len(golds) == 50
        assert stats.total_tickets == 50

        errors = validate_dataset(tickets, golds)
        assert errors == [], f"Validation errors: {errors}"

    def test_reproducible(self) -> None:
        t1, g1, _ = generate_dataset(count=20, seed=42)
        t2, g2, _ = generate_dataset(count=20, seed=42)
        assert [t.ticket_id for t in t1] == [t.ticket_id for t in t2]
        assert [g.category for g in g1] == [g.category for g in g2]

    def test_all_categories_represented(self) -> None:
        _, _, stats = generate_dataset(count=200, seed=99)
        expected_categories = {c.value for c in Category}
        actual_categories = set(stats.category_counts.keys())
        assert expected_categories == actual_categories, (
            f"Missing categories: {expected_categories - actual_categories}"
        )

    def test_all_priorities_represented(self) -> None:
        _, _, stats = generate_dataset(count=200, seed=99)
        expected_priorities = {p.value for p in Priority}
        actual_priorities = set(stats.priority_counts.keys())
        assert expected_priorities == actual_priorities

    def test_all_channels_represented(self) -> None:
        _, _, stats = generate_dataset(count=200, seed=99)
        expected_channels = {c.value for c in Channel}
        actual_channels = set(stats.channel_counts.keys())
        assert expected_channels == actual_channels

    def test_unique_ticket_ids(self) -> None:
        tickets, _, _ = generate_dataset(count=100, seed=42)
        ids = [t.ticket_id for t in tickets]
        assert len(ids) == len(set(ids)), "Duplicate ticket IDs found"
