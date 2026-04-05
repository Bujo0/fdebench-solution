# Copyright (c) Microsoft. All rights reserved.
"""Tests for data cleanup evaluation scenarios.

Validates that all scenarios are well-formed, have unique IDs,
use valid enum values, and match ticket_id between ticket and gold.
"""

from ms.evals_core.scenarios.data_cleanup import get_data_cleanup_scenarios

_SCENARIOS = get_data_cleanup_scenarios()


class TestDataCleanupScenariosStructure:
    """Structural validation for all data cleanup scenarios."""

    def test_scenarios_not_empty(self) -> None:
        assert len(_SCENARIOS) > 0, "Expected at least one data cleanup scenario"

    def test_all_scenarios_are_data_cleanup(self) -> None:
        for scenario in _SCENARIOS:
            assert scenario.scenario_category == "data_cleanup", (
                f"Scenario {scenario.ticket.ticket_id} has wrong category: {scenario.scenario_category}"
            )

    def test_ticket_ids_are_unique(self) -> None:
        ids = [s.ticket.ticket_id for s in _SCENARIOS]
        assert len(ids) == len(set(ids)), f"Duplicate ticket IDs found: {[x for x in ids if ids.count(x) > 1]}"

    def test_ticket_id_matches_gold(self) -> None:
        for scenario in _SCENARIOS:
            assert scenario.ticket.ticket_id == scenario.gold.ticket_id, (
                f"Ticket ID mismatch: ticket={scenario.ticket.ticket_id}, gold={scenario.gold.ticket_id}"
            )

    def test_scenario_tags_are_unique(self) -> None:
        tags = [s.scenario_tag for s in _SCENARIOS]
        assert len(tags) == len(set(tags)), f"Duplicate tags found: {[x for x in tags if tags.count(x) > 1]}"

    def test_gold_has_remediation_steps(self) -> None:
        for scenario in _SCENARIOS:
            assert len(scenario.gold.remediation_steps) >= 1, (
                f"Scenario {scenario.ticket.ticket_id} has no remediation steps"
            )

    def test_gold_has_next_best_action(self) -> None:
        for scenario in _SCENARIOS:
            assert len(scenario.gold.next_best_action) > 10, (
                f"Scenario {scenario.ticket.ticket_id} has a trivial next_best_action"
            )

    def test_scenario_descriptions_are_nonempty(self) -> None:
        for scenario in _SCENARIOS:
            assert len(scenario.description) > 10, (
                f"Scenario {scenario.ticket.ticket_id} has a trivial description"
            )


class TestDataCleanupScenarioContent:
    """Content-level checks for specific scenario categories."""

    def test_long_email_thread_is_long(self) -> None:
        long_threads = [s for s in _SCENARIOS if s.scenario_tag == "long_email_thread"]
        assert len(long_threads) == 1
        assert len(long_threads[0].ticket.description) > 1000

    def test_base64_image_contains_data_uri(self) -> None:
        b64_scenarios = [s for s in _SCENARIOS if "base64" in s.scenario_tag]
        assert len(b64_scenarios) >= 1
        for scenario in b64_scenarios:
            desc = scenario.ticket.description
            assert "base64" in desc.lower() or "Base64" in desc

    def test_html_body_contains_html_tags(self) -> None:
        html_scenarios = [s for s in _SCENARIOS if s.scenario_tag == "html_email_body"]
        assert len(html_scenarios) == 1
        assert "<html>" in html_scenarios[0].ticket.description

    def test_garbled_encoding_has_mojibake(self) -> None:
        garbled = [s for s in _SCENARIOS if s.scenario_tag == "garbled_encoding"]
        assert len(garbled) == 1
        # Check for common UTF-8 mojibake patterns
        desc = garbled[0].ticket.description
        assert "Ã" in desc

    def test_unicode_emoji_has_emojis(self) -> None:
        emoji_scenarios = [s for s in _SCENARIOS if s.scenario_tag == "unicode_emoji_overload"]
        assert len(emoji_scenarios) == 1
        desc = emoji_scenarios[0].ticket.description
        assert "🚨" in desc or "😡" in desc

    def test_json_xml_dump_has_json(self) -> None:
        json_scenarios = [s for s in _SCENARIOS if s.scenario_tag == "json_xml_dump"]
        assert len(json_scenarios) == 1
        desc = json_scenarios[0].ticket.description
        assert '"error"' in desc or "SalesOrder" in desc

    def test_terse_ticket_is_short(self) -> None:
        terse = [s for s in _SCENARIOS if s.scenario_tag == "extremely_terse"]
        assert len(terse) == 1
        assert len(terse[0].ticket.description) < 50

    def test_minimum_scenario_count(self) -> None:
        """Ensure we have a comprehensive set of scenarios."""
        assert len(_SCENARIOS) >= 15
