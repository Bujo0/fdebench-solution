# Copyright (c) Microsoft. All rights reserved.
"""Tests for data cleanup evaluation scenarios.

Validates that:
1. All data cleanup scenarios are well-formed (valid models)
2. Gold answers use valid enum values from the challenge spec
3. Ticket IDs are unique across all scenarios
4. Scenarios cover the expected range of data quality issues
5. Gold triage responses pass schema validation
"""

import pytest

from ms.evals.constants import CATEGORIES
from ms.evals.constants import MISSING_INFO_VOCABULARY
from ms.evals.constants import PRIORITIES
from ms.evals.constants import TEAMS
from ms.evals.scenarios.base import EvalScenario
from ms.evals.scenarios.data_cleanup import build_data_cleanup_scenarios
from ms.evals.validators.schema_validator import validate_triage_response


class TestDataCleanupScenariosStructure:
    """Validate scenario collection is well-formed."""

    def test_scenarios_not_empty(self, data_cleanup_scenarios: list[EvalScenario]) -> None:
        assert len(data_cleanup_scenarios) >= 15, "Expected at least 15 data cleanup scenarios"

    def test_unique_scenario_ids(self, data_cleanup_scenarios: list[EvalScenario]) -> None:
        ids = [s.scenario_id for s in data_cleanup_scenarios]
        assert len(ids) == len(set(ids)), f"Duplicate scenario IDs found: {ids}"

    def test_unique_ticket_ids(self, data_cleanup_scenarios: list[EvalScenario]) -> None:
        ids = [s.ticket.ticket_id for s in data_cleanup_scenarios]
        assert len(ids) == len(set(ids)), f"Duplicate ticket IDs found: {ids}"

    def test_all_categorized_as_data_cleanup(self, data_cleanup_scenarios: list[EvalScenario]) -> None:
        for s in data_cleanup_scenarios:
            assert s.category == "data_cleanup", (
                f"{s.scenario_id}: expected category='data_cleanup', got {s.category!r}"
            )


class TestDataCleanupGoldAnswers:
    """Validate gold answers use valid enum values."""

    @pytest.fixture(autouse=True)
    def _load_scenarios(self, data_cleanup_scenarios: list[EvalScenario]) -> None:
        self.scenarios = data_cleanup_scenarios

    def test_gold_categories_valid(self) -> None:
        for s in self.scenarios:
            assert s.expected.category in CATEGORIES, f"{s.scenario_id}: invalid gold category {s.expected.category!r}"

    def test_gold_priorities_valid(self) -> None:
        for s in self.scenarios:
            assert s.expected.priority in PRIORITIES, f"{s.scenario_id}: invalid gold priority {s.expected.priority!r}"

    def test_gold_teams_valid(self) -> None:
        for s in self.scenarios:
            assert s.expected.assigned_team in TEAMS, f"{s.scenario_id}: invalid gold team {s.expected.assigned_team!r}"

    def test_gold_missing_info_valid(self) -> None:
        for s in self.scenarios:
            for item in s.expected.missing_information:
                assert item in MISSING_INFO_VOCABULARY, f"{s.scenario_id}: invalid missing info item {item!r}"

    def test_gold_ticket_id_matches(self) -> None:
        for s in self.scenarios:
            assert s.ticket.ticket_id == s.expected.ticket_id, (
                f"{s.scenario_id}: ticket_id mismatch: {s.ticket.ticket_id} != {s.expected.ticket_id}"
            )

    def test_gold_has_remediation_steps(self) -> None:
        for s in self.scenarios:
            assert len(s.expected.remediation_steps) >= 1, (
                f"{s.scenario_id}: gold answer must have at least one remediation step"
            )

    def test_gold_has_next_best_action(self) -> None:
        for s in self.scenarios:
            assert len(s.expected.next_best_action.strip()) > 0, (
                f"{s.scenario_id}: gold answer must have a non-empty next_best_action"
            )


class TestDataCleanupSchemaCompliance:
    """Validate gold answers pass schema validation when serialized."""

    def test_gold_passes_schema_validation(self, data_cleanup_scenarios: list[EvalScenario]) -> None:
        for s in data_cleanup_scenarios:
            response_dict = s.expected.model_dump()
            violations = validate_triage_response(response_dict)
            assert violations == [], (
                f"{s.scenario_id}: schema violations in gold answer: {[str(v) for v in violations]}"
            )


class TestDataCleanupCoverage:
    """Validate scenarios cover the expected range of data quality issues."""

    def test_covers_long_description(self) -> None:
        scenarios = build_data_cleanup_scenarios()
        long_desc = [s for s in scenarios if len(s.ticket.description) > 3000]
        assert len(long_desc) >= 1, "Expected at least one scenario with description > 3000 chars"

    def test_covers_base64_content(self) -> None:
        scenarios = build_data_cleanup_scenarios()
        b64 = [s for s in scenarios if "base64" in s.ticket.description.lower()]
        assert len(b64) >= 1, "Expected at least one scenario with base64 content"

    def test_covers_html_content(self) -> None:
        scenarios = build_data_cleanup_scenarios()
        html = [s for s in scenarios if "<" in s.ticket.description and ">" in s.ticket.description]
        assert len(html) >= 1, "Expected at least one scenario with HTML content"

    def test_covers_empty_or_minimal_input(self) -> None:
        scenarios = build_data_cleanup_scenarios()
        empty = [s for s in scenarios if len(s.ticket.description.strip()) <= 1]
        assert len(empty) >= 1, "Expected at least one scenario with empty/minimal description"

    def test_covers_unicode_content(self) -> None:
        scenarios = build_data_cleanup_scenarios()
        # Check for non-ASCII characters
        unicode_scenarios = [s for s in scenarios if any(ord(c) > 127 for c in s.ticket.description)]
        assert len(unicode_scenarios) >= 1, "Expected at least one scenario with Unicode content"

    def test_covers_garbled_transcription(self) -> None:
        scenarios = build_data_cleanup_scenarios()
        garbled = [s for s in scenarios if "inaudible" in s.ticket.description.lower()]
        assert len(garbled) >= 1, "Expected at least one scenario with garbled transcription"

    def test_covers_email_threads(self) -> None:
        scenarios = build_data_cleanup_scenarios()
        threads = [s for s in scenarios if "forwarded" in s.ticket.description.lower()]
        assert len(threads) >= 1, "Expected at least one scenario with email thread"

    def test_covers_control_characters(self) -> None:
        scenarios = build_data_cleanup_scenarios()
        ctrl = [s for s in scenarios if any(ord(c) < 32 and c not in "\n\r\t" for c in s.ticket.description)]
        assert len(ctrl) >= 1, "Expected at least one scenario with control characters"


class TestDataCleanupTicketValidity:
    """Validate that scenario tickets themselves are well-formed input."""

    def test_tickets_have_valid_channel(self, data_cleanup_scenarios: list[EvalScenario]) -> None:
        valid_channels = {"email", "chat", "portal", "phone"}
        for s in data_cleanup_scenarios:
            assert s.ticket.channel in valid_channels, f"{s.scenario_id}: invalid channel {s.ticket.channel!r}"

    def test_tickets_have_nonempty_subject(self, data_cleanup_scenarios: list[EvalScenario]) -> None:
        for s in data_cleanup_scenarios:
            assert len(s.ticket.subject.strip()) > 0, f"{s.scenario_id}: ticket must have a non-empty subject"

    def test_tickets_have_reporter_info(self, data_cleanup_scenarios: list[EvalScenario]) -> None:
        for s in data_cleanup_scenarios:
            assert len(s.ticket.reporter.name.strip()) > 0, f"{s.scenario_id}: reporter name is empty"
            assert "@" in s.ticket.reporter.email, f"{s.scenario_id}: reporter email missing @"
            assert len(s.ticket.reporter.department.strip()) > 0, f"{s.scenario_id}: reporter dept is empty"
