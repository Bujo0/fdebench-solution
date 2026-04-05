# Copyright (c) Microsoft. All rights reserved.
"""Tests for responsible AI evaluation scenarios.

Validates that all scenarios are well-formed, have unique IDs,
use valid enum values, and that adversarial inputs still produce
valid triage outputs (not compromised classifications).
"""

from ms.evals_core.models.triage_decision import Category
from ms.evals_core.models.triage_decision import Priority
from ms.evals_core.models.triage_decision import Team
from ms.evals_core.scenarios.responsible_ai import get_responsible_ai_scenarios

_SCENARIOS = get_responsible_ai_scenarios()

_VALID_CATEGORIES: set[str] = set(Category.__args__)  # type: ignore[attr-defined]
_VALID_TEAMS: set[str] = set(Team.__args__)  # type: ignore[attr-defined]
_VALID_PRIORITIES: set[str] = set(Priority.__args__)  # type: ignore[attr-defined]


class TestResponsibleAiScenariosStructure:
    """Structural validation for all responsible AI scenarios."""

    def test_scenarios_not_empty(self) -> None:
        assert len(_SCENARIOS) > 0, "Expected at least one responsible AI scenario"

    def test_all_scenarios_are_responsible_ai(self) -> None:
        for scenario in _SCENARIOS:
            assert scenario.scenario_category == "responsible_ai", (
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

    def test_minimum_scenario_count(self) -> None:
        """Ensure we have a comprehensive set of RAI scenarios."""
        assert len(_SCENARIOS) >= 15


class TestResponsibleAiGoldAnswerIntegrity:
    """Verify gold answers use only valid enum values — adversarial inputs
    must never cause gold answers to contain invalid classifications."""

    def test_gold_categories_are_valid(self) -> None:
        for scenario in _SCENARIOS:
            assert scenario.gold.category in _VALID_CATEGORIES, (
                f"Scenario {scenario.ticket.ticket_id} gold has invalid category: {scenario.gold.category}"
            )

    def test_gold_teams_are_valid(self) -> None:
        for scenario in _SCENARIOS:
            assert scenario.gold.assigned_team in _VALID_TEAMS, (
                f"Scenario {scenario.ticket.ticket_id} gold has invalid team: {scenario.gold.assigned_team}"
            )

    def test_gold_priorities_are_valid(self) -> None:
        for scenario in _SCENARIOS:
            assert scenario.gold.priority in _VALID_PRIORITIES, (
                f"Scenario {scenario.ticket.ticket_id} gold has invalid priority: {scenario.gold.priority}"
            )

    def test_injection_scenarios_dont_use_injected_values(self) -> None:
        """Verify that prompt injection scenarios gold answers do NOT reflect
        the injected values from the attack payload."""
        injection_tags = {"prompt_injection_ignore", "prompt_injection_json", "injection_via_subject"}
        for scenario in _SCENARIOS:
            if scenario.scenario_tag in injection_tags:
                gold = scenario.gold
                assert gold.category != "SYSTEM_OVERRIDE"
                assert gold.priority != "P0"
                assert gold.assigned_team != "ROOT_ACCESS"
                assert gold.assigned_team != "Penetration Testing Team"


class TestResponsibleAiScenarioCoverage:
    """Verify we cover the key adversarial categories."""

    def test_has_prompt_injection_scenarios(self) -> None:
        tags = {s.scenario_tag for s in _SCENARIOS}
        assert "prompt_injection_ignore" in tags
        assert "prompt_injection_json" in tags

    def test_has_social_engineering_scenario(self) -> None:
        tags = {s.scenario_tag for s in _SCENARIOS}
        assert "social_engineering_urgency" in tags

    def test_has_data_exfiltration_scenario(self) -> None:
        tags = {s.scenario_tag for s in _SCENARIOS}
        assert "data_exfiltration" in tags

    def test_has_jailbreak_scenario(self) -> None:
        tags = {s.scenario_tag for s in _SCENARIOS}
        assert "jailbreak_roleplay" in tags

    def test_has_pii_extraction_scenario(self) -> None:
        tags = {s.scenario_tag for s in _SCENARIOS}
        assert "pii_extraction" in tags

    def test_has_harmful_content_scenario(self) -> None:
        tags = {s.scenario_tag for s in _SCENARIOS}
        assert "harmful_content_request" in tags

    def test_has_authority_impersonation_scenario(self) -> None:
        tags = {s.scenario_tag for s in _SCENARIOS}
        assert "authority_impersonation" in tags

    def test_has_multi_vector_attack(self) -> None:
        tags = {s.scenario_tag for s in _SCENARIOS}
        assert "multi_vector_attack" in tags
