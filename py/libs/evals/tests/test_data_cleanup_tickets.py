# Copyright (c) Microsoft. All rights reserved.
"""Tests for data cleanup evaluation tickets.

Validates that the data cleanup test dataset is well-formed and that
the tickets exercise the expected edge cases: very long descriptions,
base64 content, HTML, embedded credentials, unicode, etc.
"""

import json
from pathlib import Path

import pytest

from ms.evals_core.constants import ALL_CATEGORIES
from ms.evals_core.constants import ALL_MISSING_INFO_FIELDS
from ms.evals_core.constants import ALL_PRIORITIES
from ms.evals_core.constants import ALL_TEAMS
from ms.evals_core.datasets.loader import load_dataset_pair
from ms.evals_core.models.ticket_input import TicketInput
from ms.evals_core.models.triage_response import TriageResponse
from ms.evals_core.validators.content_safety import validate_content_safety
from ms.evals_core.validators.schema import validate_response_schema


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
        assert len(tickets) == 15
        assert len(golds) == 15

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
        assert ids == [f"INC-{5000 + i}" for i in range(1, 16)]

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

    def test_gold_teams_are_valid(self, dataset: tuple[tuple[TicketInput, ...], tuple[TriageResponse, ...]]) -> None:
        _, golds = dataset
        for gold in golds:
            assert gold.assigned_team in ALL_TEAMS, f"{gold.ticket_id}: invalid team '{gold.assigned_team}'"

    def test_gold_missing_info_items_are_valid(
        self, dataset: tuple[tuple[TicketInput, ...], tuple[TriageResponse, ...]]
    ) -> None:
        _, golds = dataset
        for gold in golds:
            for item in gold.missing_information:
                assert item in ALL_MISSING_INFO_FIELDS, f"{gold.ticket_id}: invalid missing info '{item}'"

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

    def test_description_is_long(self, dataset: tuple[tuple[TicketInput, ...], tuple[TriageResponse, ...]]) -> None:
        tickets, _ = dataset
        ticket = next(t for t in tickets if t.ticket_id == "INC-5001")
        assert len(ticket.description) > 2000

    def test_classified_as_network(self, dataset: tuple[tuple[TicketInput, ...], tuple[TriageResponse, ...]]) -> None:
        _, golds = dataset
        gold = next(g for g in golds if g.ticket_id == "INC-5001")
        assert gold.category == "Network & Connectivity"


class TestBase64Content:
    """INC-5002: Base64 encoded images and data in description."""

    def test_contains_base64(self, dataset: tuple[tuple[TicketInput, ...], tuple[TriageResponse, ...]]) -> None:
        tickets, _ = dataset
        ticket = next(t for t in tickets if t.ticket_id == "INC-5002")
        assert "base64" in ticket.description.lower()

    def test_classified_as_software(self, dataset: tuple[tuple[TicketInput, ...], tuple[TriageResponse, ...]]) -> None:
        _, golds = dataset
        gold = next(g for g in golds if g.ticket_id == "INC-5002")
        assert gold.category == "Software & Applications"


class TestHtmlContent:
    """INC-5003: HTML-heavy email thread."""

    def test_contains_html_tags(self, dataset: tuple[tuple[TicketInput, ...], tuple[TriageResponse, ...]]) -> None:
        tickets, _ = dataset
        ticket = next(t for t in tickets if t.ticket_id == "INC-5003")
        assert "<html>" in ticket.description.lower() or "<blockquote>" in ticket.description.lower()

    def test_classified_as_software(self, dataset: tuple[tuple[TicketInput, ...], tuple[TriageResponse, ...]]) -> None:
        _, golds = dataset
        gold = next(g for g in golds if g.ticket_id == "INC-5003")
        assert gold.category == "Software & Applications"


class TestNestedEmailChain:
    """INC-5004: Deeply nested email thread with many forwarding layers."""

    def test_contains_original_message_markers(
        self, dataset: tuple[tuple[TicketInput, ...], tuple[TriageResponse, ...]]
    ) -> None:
        tickets, _ = dataset
        ticket = next(t for t in tickets if t.ticket_id == "INC-5004")
        assert ticket.description.count("Original Message") >= 4

    def test_classified_as_hardware(self, dataset: tuple[tuple[TicketInput, ...], tuple[TriageResponse, ...]]) -> None:
        _, golds = dataset
        gold = next(g for g in golds if g.ticket_id == "INC-5004")
        assert gold.category == "Hardware & Peripherals"


class TestUnicodeCharacters:
    """INC-5005: Emoji and unicode in subject, password in body."""

    def test_contains_unicode(self, dataset: tuple[tuple[TicketInput, ...], tuple[TriageResponse, ...]]) -> None:
        tickets, _ = dataset
        ticket = next(t for t in tickets if t.ticket_id == "INC-5005")
        assert any(ord(c) > 127 for c in ticket.subject)

    def test_classified_as_access_auth(
        self, dataset: tuple[tuple[TicketInput, ...], tuple[TriageResponse, ...]]
    ) -> None:
        _, golds = dataset
        gold = next(g for g in golds if g.ticket_id == "INC-5005")
        assert gold.category == "Access & Authentication"


class TestLongSubject:
    """INC-5007: Extremely long subject line with overstated urgency."""

    def test_subject_is_very_long(self, dataset: tuple[tuple[TicketInput, ...], tuple[TriageResponse, ...]]) -> None:
        tickets, _ = dataset
        ticket = next(t for t in tickets if t.ticket_id == "INC-5007")
        assert len(ticket.subject) > 200

    def test_classified_as_software(self, dataset: tuple[tuple[TicketInput, ...], tuple[TriageResponse, ...]]) -> None:
        _, golds = dataset
        gold = next(g for g in golds if g.ticket_id == "INC-5007")
        assert gold.category == "Software & Applications"
        assert gold.priority == "P4"
        assert gold.needs_escalation is False


class TestDatabaseTimeout:
    """INC-5006: Database connection timeout requiring escalation."""

    def test_classified_as_data_storage(
        self, dataset: tuple[tuple[TicketInput, ...], tuple[TriageResponse, ...]]
    ) -> None:
        _, golds = dataset
        gold = next(g for g in golds if g.ticket_id == "INC-5006")
        assert gold.category == "Data & Storage"
        assert gold.priority == "P1"
        assert gold.needs_escalation is True


class TestSharePointAccess:
    """INC-5008: SharePoint site access request."""

    def test_classified_as_access_auth(
        self, dataset: tuple[tuple[TicketInput, ...], tuple[TriageResponse, ...]]
    ) -> None:
        _, golds = dataset
        gold = next(g for g in golds if g.ticket_id == "INC-5008")
        assert gold.category == "Access & Authentication"
        assert gold.needs_escalation is False


class TestFrenchLanguageTicket:
    """INC-5009: Ticket partially written in French."""

    def test_contains_non_ascii(self, dataset: tuple[tuple[TicketInput, ...], tuple[TriageResponse, ...]]) -> None:
        tickets, _ = dataset
        ticket = next(t for t in tickets if t.ticket_id == "INC-5009")
        assert any(ord(c) > 127 for c in ticket.subject)

    def test_classified_as_software(self, dataset: tuple[tuple[TicketInput, ...], tuple[TriageResponse, ...]]) -> None:
        _, golds = dataset
        gold = next(g for g in golds if g.ticket_id == "INC-5009")
        assert gold.category == "Software & Applications"


class TestStackTrace:
    """INC-5010: Application error with Java stack trace in body."""

    def test_contains_stack_trace(self, dataset: tuple[tuple[TicketInput, ...], tuple[TriageResponse, ...]]) -> None:
        tickets, _ = dataset
        ticket = next(t for t in tickets if t.ticket_id == "INC-5010")
        assert "stack trace" in ticket.description.lower()

    def test_classified_as_software(self, dataset: tuple[tuple[TicketInput, ...], tuple[TriageResponse, ...]]) -> None:
        _, golds = dataset
        gold = next(g for g in golds if g.ticket_id == "INC-5010")
        assert gold.category == "Software & Applications"
