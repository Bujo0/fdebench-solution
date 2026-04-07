# Copyright (c) Microsoft. All rights reserved.
"""Tests for extended data cleanup evaluation scenarios (dc-151 through dc-170).

Validates that:
1. All extended scenarios are well-formed and register without errors
2. Expected triage uses valid enum values
3. Ticket descriptions contain the expected noisy data patterns
4. Scenario IDs and ticket IDs are unique and sequential
5. Scenarios cover the intended data quality challenge categories
"""

import pytest

from ms.evals_core.framework.models.scenario import EvalScenario
from ms.evals_core.framework.models.scenario import ScenarioCategory
from ms.evals_core.framework.scenarios.registry import default_registry
from ms.evals_core.framework.scoring.data_cleanup import score_data_cleanup
from ms.evals_core.framework.scoring.valid_values import VALID_CATEGORIES
from ms.evals_core.framework.scoring.valid_values import VALID_MISSING_INFO
from ms.evals_core.framework.scoring.valid_values import VALID_PRIORITIES
from ms.evals_core.framework.scoring.valid_values import VALID_TEAMS


@pytest.fixture(scope="module")
def extended_dc_scenarios() -> list[EvalScenario]:
    """Load only the extended data cleanup scenarios (dc-151..dc-170)."""
    import ms.evals_core.framework.scenarios.data_cleanup  # noqa: F401, PLC0415
    import ms.evals_core.framework.scenarios.data_cleanup_extended  # noqa: F401, PLC0415

    all_dc = default_registry.by_category(ScenarioCategory.DATA_CLEANUP)
    return [s for s in all_dc if s.scenario_id.startswith("dc-") and 151 <= int(s.scenario_id.split("-")[1]) <= 170]


# ── Structural integrity ──────────────────────────────────────────────


class TestExtendedDataCleanupStructure:
    """Validate the extended scenario collection is well-formed."""

    def test_exactly_20_extended_scenarios(self, extended_dc_scenarios: list[EvalScenario]) -> None:
        assert len(extended_dc_scenarios) == 20, (
            f"Expected 20 extended DC scenarios (dc-151..dc-170), got {len(extended_dc_scenarios)}"
        )

    def test_scenario_ids_sequential(self, extended_dc_scenarios: list[EvalScenario]) -> None:
        ids = sorted(s.scenario_id for s in extended_dc_scenarios)
        expected = [f"dc-{i}" for i in range(151, 171)]
        assert ids == expected

    def test_ticket_ids_sequential(self, extended_dc_scenarios: list[EvalScenario]) -> None:
        ids = sorted(s.ticket.ticket_id for s in extended_dc_scenarios)
        expected = [f"INC-{i}" for i in range(5151, 5171)]
        assert ids == expected

    def test_all_categorized_as_data_cleanup(self, extended_dc_scenarios: list[EvalScenario]) -> None:
        for s in extended_dc_scenarios:
            assert s.category == ScenarioCategory.DATA_CLEANUP, (
                f"{s.scenario_id}: expected DATA_CLEANUP, got {s.category}"
            )

    def test_all_have_tags(self, extended_dc_scenarios: list[EvalScenario]) -> None:
        for s in extended_dc_scenarios:
            assert len(s.tags) >= 1, f"{s.scenario_id}: must have at least one tag"

    def test_all_have_description(self, extended_dc_scenarios: list[EvalScenario]) -> None:
        for s in extended_dc_scenarios:
            assert len(s.description) > 20, f"{s.scenario_id}: description too short"

    def test_all_have_nonempty_ticket_description(self, extended_dc_scenarios: list[EvalScenario]) -> None:
        for s in extended_dc_scenarios:
            assert len(s.ticket.description) > 50, (
                f"{s.scenario_id}: ticket description too short for a data cleanup scenario"
            )


# ── Expected triage validity ──────────────────────────────────────────


class TestExtendedDataCleanupExpectedTriage:
    """Validate expected triage values use valid enums."""

    def test_expected_categories_valid(self, extended_dc_scenarios: list[EvalScenario]) -> None:
        normalized_valid = {c.strip().lower() for c in VALID_CATEGORIES}
        for s in extended_dc_scenarios:
            if s.expected_triage and s.expected_triage.category:
                assert s.expected_triage.category.strip().lower() in normalized_valid, (
                    f"{s.scenario_id}: invalid category '{s.expected_triage.category}'"
                )

    def test_expected_priorities_valid(self, extended_dc_scenarios: list[EvalScenario]) -> None:
        for s in extended_dc_scenarios:
            if s.expected_triage and s.expected_triage.priority:
                assert s.expected_triage.priority.upper() in VALID_PRIORITIES, (
                    f"{s.scenario_id}: invalid priority '{s.expected_triage.priority}'"
                )

    def test_expected_teams_valid(self, extended_dc_scenarios: list[EvalScenario]) -> None:
        normalized_valid = {t.strip().lower() for t in VALID_TEAMS}
        for s in extended_dc_scenarios:
            if s.expected_triage and s.expected_triage.assigned_team:
                assert s.expected_triage.assigned_team.strip().lower() in normalized_valid, (
                    f"{s.scenario_id}: invalid team '{s.expected_triage.assigned_team}'"
                )

    def test_expected_missing_info_valid(self, extended_dc_scenarios: list[EvalScenario]) -> None:
        normalized_valid = {v.strip().lower() for v in VALID_MISSING_INFO}
        for s in extended_dc_scenarios:
            if s.expected_triage and s.expected_triage.missing_information:
                for item in s.expected_triage.missing_information:
                    assert item.strip().lower() in normalized_valid, f"{s.scenario_id}: invalid missing info '{item}'"


# ── Data quality pattern coverage ─────────────────────────────────────


class TestExtendedDataCleanupPatterns:
    """Validate scenarios contain the expected noisy data patterns."""

    def test_dc151_contains_base64_images(self, extended_dc_scenarios: list[EvalScenario]) -> None:
        s = next(s for s in extended_dc_scenarios if s.scenario_id == "dc-151")
        desc = s.ticket.description
        assert "data:image/png;base64," in desc
        assert desc.count("[Inline image") >= 10

    def test_dc152_contains_mime_boundaries(self, extended_dc_scenarios: list[EvalScenario]) -> None:
        s = next(s for s in extended_dc_scenarios if s.scenario_id == "dc-152")
        desc = s.ticket.description
        assert "Content-Type: multipart/mixed" in desc
        assert "boundary=" in desc
        assert "Content-Transfer-Encoding:" in desc

    def test_dc153_contains_mojibake(self, extended_dc_scenarios: list[EvalScenario]) -> None:
        s = next(s for s in extended_dc_scenarios if s.scenario_id == "dc-153")
        desc = s.ticket.description
        assert "\u00e2\u20ac\u2122" in desc  # â€™ = UTF-8 ' decoded as Windows-1252

    def test_dc154_contains_zero_width_characters(self, extended_dc_scenarios: list[EvalScenario]) -> None:
        s = next(s for s in extended_dc_scenarios if s.scenario_id == "dc-154")
        desc = s.ticket.description
        assert "\u200b" in desc  # zero-width space
        assert "\ufeff" in desc  # byte order mark

    def test_dc155_contains_bidi_text(self, extended_dc_scenarios: list[EvalScenario]) -> None:
        s = next(s for s in extended_dc_scenarios if s.scenario_id == "dc-155")
        desc = s.ticket.description
        assert "\u202e" in desc  # RTL override
        # Contains Arabic text
        assert any("\u0600" <= c <= "\u06ff" for c in desc)

    def test_dc156_contains_url_encoding(self, extended_dc_scenarios: list[EvalScenario]) -> None:
        s = next(s for s in extended_dc_scenarios if s.scenario_id == "dc-156")
        desc = s.ticket.description
        assert "%20" in desc
        assert "%0A" in desc
        assert "%3D" in desc

    def test_dc157_contains_multiple_disclaimers(self, extended_dc_scenarios: list[EvalScenario]) -> None:
        s = next(s for s in extended_dc_scenarios if s.scenario_id == "dc-157")
        desc = s.ticket.description
        assert desc.count("CONFIDENTIALITY NOTICE") >= 6

    def test_dc158_contains_svg(self, extended_dc_scenarios: list[EvalScenario]) -> None:
        s = next(s for s in extended_dc_scenarios if s.scenario_id == "dc-158")
        desc = s.ticket.description
        assert "<svg" in desc
        assert "</svg>" in desc
        assert "<rect" in desc

    def test_dc159_contains_repeated_content(self, extended_dc_scenarios: list[EvalScenario]) -> None:
        s = next(s for s in extended_dc_scenarios if s.scenario_id == "dc-159")
        desc = s.ticket.description
        repeated = "My laptop is running very slowly"
        assert desc.count(repeated) >= 20

    def test_dc160_contains_ics_calendar(self, extended_dc_scenarios: list[EvalScenario]) -> None:
        s = next(s for s in extended_dc_scenarios if s.scenario_id == "dc-160")
        desc = s.ticket.description
        assert "BEGIN:VCALENDAR" in desc
        assert "BEGIN:VEVENT" in desc
        assert "END:VCALENDAR" in desc

    def test_dc161_contains_hex_dump(self, extended_dc_scenarios: list[EvalScenario]) -> None:
        s = next(s for s in extended_dc_scenarios if s.scenario_id == "dc-161")
        desc = s.ticket.description
        assert "0x00000000" in desc

    def test_dc162_contains_event_log_xml(self, extended_dc_scenarios: list[EvalScenario]) -> None:
        s = next(s for s in extended_dc_scenarios if s.scenario_id == "dc-162")
        desc = s.ticket.description
        assert "<EventID>" in desc
        assert "Microsoft-Windows-Security-Auditing" in desc

    def test_dc163_contains_markdown(self, extended_dc_scenarios: list[EvalScenario]) -> None:
        s = next(s for s in extended_dc_scenarios if s.scenario_id == "dc-163")
        desc = s.ticket.description
        assert "```" in desc
        assert "|" in desc
        assert "## " in desc

    def test_dc164_contains_nested_html_tables(self, extended_dc_scenarios: list[EvalScenario]) -> None:
        s = next(s for s in extended_dc_scenarios if s.scenario_id == "dc-164")
        desc = s.ticket.description
        assert "<table>" in desc
        assert desc.count("<table>") >= 3  # nested tables

    def test_dc165_contains_soap_fault(self, extended_dc_scenarios: list[EvalScenario]) -> None:
        s = next(s for s in extended_dc_scenarios if s.scenario_id == "dc-165")
        desc = s.ticket.description
        assert "<soap:Envelope" in desc
        assert "<soap:Fault>" in desc
        assert "<faultcode>" in desc

    def test_dc166_contains_html_diagnostic_table(self, extended_dc_scenarios: list[EvalScenario]) -> None:
        s = next(s for s in extended_dc_scenarios if s.scenario_id == "dc-166")
        desc = s.ticket.description
        assert "<th>" in desc
        assert "<td>" in desc
        assert "CRC Errors" in desc

    def test_dc167_contains_auto_reply_loop(self, extended_dc_scenarios: list[EvalScenario]) -> None:
        s = next(s for s in extended_dc_scenarios if s.scenario_id == "dc-167")
        desc = s.ticket.description
        assert "Auto-Reply" in desc
        assert "out of the office" in desc
        assert desc.count("Auto-Reply") >= 10

    def test_dc168_contains_ansi_escape_codes(self, extended_dc_scenarios: list[EvalScenario]) -> None:
        s = next(s for s in extended_dc_scenarios if s.scenario_id == "dc-168")
        desc = s.ticket.description
        assert "\x1b[" in desc  # ANSI escape sequence

    def test_dc169_contains_rtf_artifacts(self, extended_dc_scenarios: list[EvalScenario]) -> None:
        s = next(s for s in extended_dc_scenarios if s.scenario_id == "dc-169")
        desc = s.ticket.description
        assert "{\\rtf1" in desc
        assert "\\pard" in desc

    def test_dc170_contains_base64_executable(self, extended_dc_scenarios: list[EvalScenario]) -> None:
        s = next(s for s in extended_dc_scenarios if s.scenario_id == "dc-170")
        desc = s.ticket.description
        assert "TVqQAAMAAAA" in desc  # MZ header in base64


# ── Scoring sanity check ──────────────────────────────────────────────


class TestExtendedDataCleanupScoring:
    """Verify scoring works correctly against gold-standard responses."""

    def _gold_response(self, scenario: EvalScenario) -> dict:
        """Build a gold-standard response dict from the scenario's expected triage."""
        expected = scenario.expected_triage
        escalation = expected.needs_escalation if expected and expected.needs_escalation is not None else False
        return {
            "ticket_id": scenario.ticket.ticket_id,
            "category": expected.category if expected and expected.category else "General Inquiry",
            "priority": expected.priority if expected and expected.priority else "P3",
            "assigned_team": expected.assigned_team if expected and expected.assigned_team else "None",
            "needs_escalation": escalation,
            "missing_information": expected.missing_information if expected and expected.missing_information else [],
            "next_best_action": "Investigate the reported issue.",
            "remediation_steps": ["Investigate and resolve the issue."],
        }

    def test_gold_response_scores_perfectly(self, extended_dc_scenarios: list[EvalScenario]) -> None:
        """A response matching the expected triage should score 1.0."""
        for s in extended_dc_scenarios:
            response = self._gold_response(s)
            result = score_data_cleanup(s, response)
            assert result.passed, (
                f"{s.scenario_id}: gold response should pass all checks. "
                f"Failed: {[c for c in result.checks if not c.passed]}"
            )

    def test_wrong_category_lowers_score(self, extended_dc_scenarios: list[EvalScenario]) -> None:
        """A response with the wrong category should not score perfectly."""
        for s in extended_dc_scenarios:
            if not s.expected_triage or not s.expected_triage.category:
                continue
            response = self._gold_response(s)
            # Set a wrong category
            wrong = "General Inquiry" if s.expected_triage.category != "General Inquiry" else "Data & Storage"
            response["category"] = wrong
            result = score_data_cleanup(s, response)
            assert result.score < 1.0, f"{s.scenario_id}: wrong category should lower score"

    def test_missing_fields_fail_structure_check(self, extended_dc_scenarios: list[EvalScenario]) -> None:
        """A response missing required fields should fail."""
        s = extended_dc_scenarios[0]
        response = {"ticket_id": s.ticket.ticket_id}
        result = score_data_cleanup(s, response)
        assert not result.passed
        structure_check = next(c for c in result.checks if c.name == "response_structure")
        assert not structure_check.passed
