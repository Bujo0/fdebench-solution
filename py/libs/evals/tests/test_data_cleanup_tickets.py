# Copyright (c) Microsoft. All rights reserved.
"""Tests for data cleanup evaluation tickets.

Validates that the data cleanup test dataset is well-formed and that
the tickets exercise the expected edge cases: very long descriptions,
base64 content, HTML, embedded credentials, unicode, etc.
"""

import json
from pathlib import Path

import pytest

from ms.evals.constants import ALL_CATEGORIES
from ms.evals.constants import ALL_MISSING_INFO_FIELDS
from ms.evals.constants import ALL_PRIORITIES
from ms.evals.constants import ALL_TEAMS
from ms.evals.datasets.loader import load_dataset_pair
from ms.evals.models.ticket import TicketInput
from ms.evals.models.triage_response import TriageResponse
from ms.evals.validators.content_safety import validate_content_safety
from ms.evals.validators.schema import validate_response_schema


@pytest.fixture
def dataset(data_dir: Path) -> tuple[tuple[TicketInput, ...], tuple[TriageResponse, ...]]:
    pair = load_dataset_pair(
        data_dir / "data_cleanup.json",
        data_dir / "data_cleanup_gold.json",
    )
    return pair.tickets, pair.golds


@pytest.fixture
def raw_tickets(data_dir: Path) -> list[dict[str, object]]:
    return json.loads((data_dir / "data_cleanup.json").read_text(encoding="utf-8"))


@pytest.fixture
def raw_golds(data_dir: Path) -> list[dict[str, object]]:
    return json.loads((data_dir / "data_cleanup_gold.json").read_text(encoding="utf-8"))


# ── Dataset integrity ────────────────────────────────────────────────


class TestDatasetIntegrity:
    def test_dataset_loads_without_error(
        self, dataset: tuple[tuple[TicketInput, ...], tuple[TriageResponse, ...]]
    ) -> None:
        tickets, golds = dataset
        assert len(tickets) == 10
        assert len(golds) == 10

    def test_every_ticket_has_matching_gold(
        self, dataset: tuple[tuple[TicketInput, ...], tuple[TriageResponse, ...]]
    ) -> None:
        tickets, golds = dataset
        ticket_ids = {t.ticket_id for t in tickets}
        gold_ids = {g.ticket_id for g in golds}
        assert ticket_ids == gold_ids

    def test_ticket_ids_are_sequential(
        self, dataset: tuple[tuple[TicketInput, ...], tuple[TriageResponse, ...]]
    ) -> None:
        tickets, _ = dataset
        ids = sorted(t.ticket_id for t in tickets)
        assert ids == [f"INC-500{i}" for i in range(1, 10)] + ["INC-5010"]

    def test_gold_categories_are_valid(
        self, dataset: tuple[tuple[TicketInput, ...], tuple[TriageResponse, ...]]
    ) -> None:
        _, golds = dataset
        for gold in golds:
            assert gold.category in ALL_CATEGORIES, f"{gold.ticket_id}: invalid category '{gold.category}'"

    def test_gold_priorities_are_valid(
        self, dataset: tuple[tuple[TicketInput, ...], tuple[TriageResponse, ...]]
    ) -> None:
        _, golds = dataset
        for gold in golds:
            assert gold.priority in ALL_PRIORITIES, f"{gold.ticket_id}: invalid priority '{gold.priority}'"

    def test_gold_teams_are_valid(
        self, dataset: tuple[tuple[TicketInput, ...], tuple[TriageResponse, ...]]
    ) -> None:
        _, golds = dataset
        for gold in golds:
            assert gold.assigned_team in ALL_TEAMS, f"{gold.ticket_id}: invalid team '{gold.assigned_team}'"

    def test_gold_missing_info_items_are_valid(
        self, dataset: tuple[tuple[TicketInput, ...], tuple[TriageResponse, ...]]
    ) -> None:
        _, golds = dataset
        for gold in golds:
            for item in gold.missing_information:
                assert item in ALL_MISSING_INFO_FIELDS, (
                    f"{gold.ticket_id}: invalid missing info '{item}'"
                )

    def test_gold_schema_compliance(self, raw_golds: list[dict[str, object]]) -> None:
        """Gold answers should pass the schema validator."""
        for gold in raw_golds:
            tid = str(gold.get("ticket_id", ""))
            result = validate_response_schema(gold, tid)
            assert result.is_valid, f"{tid}: schema violations: {result.violations}"

    def test_gold_content_safety(self, raw_golds: list[dict[str, object]]) -> None:
        """Gold answers should pass content safety checks."""
        for gold in raw_golds:
            tid = str(gold.get("ticket_id", ""))
            result = validate_content_safety(gold, tid)
            assert result.is_safe, f"{tid}: content safety issues: {result.issues}"


# ── Specific ticket edge cases ───────────────────────────────────────


class TestVeryLongDescription:
    """INC-5001: Very long email body (verbose user)."""

    def test_description_is_long(
        self, dataset: tuple[tuple[TicketInput, ...], tuple[TriageResponse, ...]]
    ) -> None:
        tickets, _ = dataset
        ticket = next(t for t in tickets if t.ticket_id == "INC-5001")
        assert len(ticket.description) > 2000

    def test_classified_as_software(
        self, dataset: tuple[tuple[TicketInput, ...], tuple[TriageResponse, ...]]
    ) -> None:
        _, golds = dataset
        gold = next(g for g in golds if g.ticket_id == "INC-5001")
        assert gold.category == "Software & Applications"


class TestBase64Content:
    """INC-5002: Base64 encoded images and data in description."""

    def test_contains_base64(
        self, dataset: tuple[tuple[TicketInput, ...], tuple[TriageResponse, ...]]
    ) -> None:
        tickets, _ = dataset
        ticket = next(t for t in tickets if t.ticket_id == "INC-5002")
        assert "base64" in ticket.description.lower()

    def test_classified_as_access_auth(
        self, dataset: tuple[tuple[TicketInput, ...], tuple[TriageResponse, ...]]
    ) -> None:
        _, golds = dataset
        gold = next(g for g in golds if g.ticket_id == "INC-5002")
        assert gold.category == "Access & Authentication"


class TestHtmlContent:
    """INC-5003: HTML-heavy email thread."""

    def test_contains_html_tags(
        self, dataset: tuple[tuple[TicketInput, ...], tuple[TriageResponse, ...]]
    ) -> None:
        tickets, _ = dataset
        ticket = next(t for t in tickets if t.ticket_id == "INC-5003")
        assert "<html>" in ticket.description.lower() or "<blockquote>" in ticket.description.lower()

    def test_classified_as_network(
        self, dataset: tuple[tuple[TicketInput, ...], tuple[TriageResponse, ...]]
    ) -> None:
        _, golds = dataset
        gold = next(g for g in golds if g.ticket_id == "INC-5003")
        assert gold.category == "Network & Connectivity"
        assert gold.needs_escalation is True


class TestEmbeddedCredentials:
    """INC-5004: Ticket containing plaintext credentials."""

    def test_contains_password(
        self, dataset: tuple[tuple[TicketInput, ...], tuple[TriageResponse, ...]]
    ) -> None:
        tickets, _ = dataset
        ticket = next(t for t in tickets if t.ticket_id == "INC-5004")
        assert "password" in ticket.description.lower()

    def test_classified_as_security(
        self, dataset: tuple[tuple[TicketInput, ...], tuple[TriageResponse, ...]]
    ) -> None:
        _, golds = dataset
        gold = next(g for g in golds if g.ticket_id == "INC-5004")
        assert gold.category == "Security & Compliance"
        assert gold.priority == "P1"
        assert gold.needs_escalation is True


class TestUnicodeCharacters:
    """INC-5005: Special characters, emoji, multilingual content."""

    def test_contains_unicode(
        self, dataset: tuple[tuple[TicketInput, ...], tuple[TriageResponse, ...]]
    ) -> None:
        tickets, _ = dataset
        ticket = next(t for t in tickets if t.ticket_id == "INC-5005")
        assert any(ord(c) > 127 for c in ticket.subject)

    def test_classified_as_software(
        self, dataset: tuple[tuple[TicketInput, ...], tuple[TriageResponse, ...]]
    ) -> None:
        _, golds = dataset
        gold = next(g for g in golds if g.ticket_id == "INC-5005")
        assert gold.category == "Software & Applications"


class TestLongSubject:
    """INC-5006: Extremely long subject line."""

    def test_subject_is_very_long(
        self, dataset: tuple[tuple[TicketInput, ...], tuple[TriageResponse, ...]]
    ) -> None:
        tickets, _ = dataset
        ticket = next(t for t in tickets if t.ticket_id == "INC-5006")
        assert len(ticket.subject) > 200

    def test_classified_as_network(
        self, dataset: tuple[tuple[TicketInput, ...], tuple[TriageResponse, ...]]
    ) -> None:
        _, golds = dataset
        gold = next(g for g in golds if g.ticket_id == "INC-5006")
        assert gold.category == "Network & Connectivity"
        assert gold.priority == "P1"
        assert gold.needs_escalation is True


class TestGarbledData:
    """INC-5007: Corrupted text with null bytes and encoding issues."""

    def test_contains_corruption_indicators(
        self, dataset: tuple[tuple[TicketInput, ...], tuple[TriageResponse, ...]]
    ) -> None:
        tickets, _ = dataset
        ticket = next(t for t in tickets if t.ticket_id == "INC-5007")
        assert "NaN" in ticket.description or "\\x00" in ticket.description

    def test_classified_as_data_storage(
        self, dataset: tuple[tuple[TicketInput, ...], tuple[TriageResponse, ...]]
    ) -> None:
        _, golds = dataset
        gold = next(g for g in golds if g.ticket_id == "INC-5007")
        assert gold.category == "Data & Storage"


class TestEmailChain:
    """INC-5008: Deeply nested email thread."""

    def test_contains_original_message_markers(
        self, dataset: tuple[tuple[TicketInput, ...], tuple[TriageResponse, ...]]
    ) -> None:
        tickets, _ = dataset
        ticket = next(t for t in tickets if t.ticket_id == "INC-5008")
        assert ticket.description.count("Original Message") >= 4

    def test_classified_as_hardware(
        self, dataset: tuple[tuple[TicketInput, ...], tuple[TriageResponse, ...]]
    ) -> None:
        _, golds = dataset
        gold = next(g for g in golds if g.ticket_id == "INC-5008")
        assert gold.category == "Hardware & Peripherals"
        assert gold.needs_escalation is True


class TestLogDump:
    """INC-5009: Massive log output as ticket body."""

    def test_contains_log_entries(
        self, dataset: tuple[tuple[TicketInput, ...], tuple[TriageResponse, ...]]
    ) -> None:
        tickets, _ = dataset
        ticket = next(t for t in tickets if t.ticket_id == "INC-5009")
        assert "[ERROR]" in ticket.description and "[INFO]" in ticket.description

    def test_classified_as_software(
        self, dataset: tuple[tuple[TicketInput, ...], tuple[TriageResponse, ...]]
    ) -> None:
        _, golds = dataset
        gold = next(g for g in golds if g.ticket_id == "INC-5009")
        assert gold.category == "Software & Applications"


class TestSpamPhishing:
    """INC-5010: Spam/phishing content submitted as ticket."""

    def test_classified_as_not_support(
        self, dataset: tuple[tuple[TicketInput, ...], tuple[TriageResponse, ...]]
    ) -> None:
        _, golds = dataset
        gold = next(g for g in golds if g.ticket_id == "INC-5010")
        assert gold.category == "Not a Support Ticket"
        assert gold.assigned_team == "None"
        assert gold.priority == "P4"
