# Copyright (c) Microsoft. All rights reserved.
"""Tests for scenario definitions and validation."""

from ms.eval_generator.models import VALID_CATEGORIES
from ms.eval_generator.models import VALID_MISSING_INFO
from ms.eval_generator.models import VALID_PRIORITIES
from ms.eval_generator.models import VALID_TEAMS
from ms.eval_generator.scenarios import collect_all_scenarios


class TestScenarioCollection:
    def test_collect_all_scenarios_returns_nonempty(self) -> None:
        scenarios = collect_all_scenarios()
        assert len(scenarios) > 0

    def test_all_scenario_ids_are_unique(self) -> None:
        scenarios = collect_all_scenarios()
        ids = [s.scenario_id for s in scenarios]
        duplicates = [sid for sid in ids if ids.count(sid) > 1]
        assert len(duplicates) == 0, f"Duplicate scenario IDs: {set(duplicates)}"

    def test_all_scenarios_have_subjects(self) -> None:
        scenarios = collect_all_scenarios()
        for s in scenarios:
            assert len(s.subjects) > 0, f"Scenario {s.scenario_id} has no subjects"

    def test_all_scenarios_have_descriptions(self) -> None:
        scenarios = collect_all_scenarios()
        for s in scenarios:
            assert len(s.descriptions) > 0, f"Scenario {s.scenario_id} has no descriptions"


class TestScenarioGoldValues:
    def test_all_categories_are_valid(self) -> None:
        scenarios = collect_all_scenarios()
        for s in scenarios:
            assert s.gold.category in VALID_CATEGORIES, (
                f"Scenario {s.scenario_id} has invalid category: {s.gold.category}"
            )

    def test_all_priorities_are_valid(self) -> None:
        scenarios = collect_all_scenarios()
        for s in scenarios:
            assert s.gold.priority in VALID_PRIORITIES, (
                f"Scenario {s.scenario_id} has invalid priority: {s.gold.priority}"
            )

    def test_all_teams_are_valid(self) -> None:
        scenarios = collect_all_scenarios()
        for s in scenarios:
            assert s.gold.assigned_team in VALID_TEAMS, (
                f"Scenario {s.scenario_id} has invalid team: {s.gold.assigned_team}"
            )

    def test_all_missing_info_terms_are_valid(self) -> None:
        scenarios = collect_all_scenarios()
        for s in scenarios:
            for mi in s.gold.missing_information:
                assert mi in VALID_MISSING_INFO, f"Scenario {s.scenario_id} has invalid missing_info term: {mi}"

    def test_all_scenarios_have_next_best_action(self) -> None:
        scenarios = collect_all_scenarios()
        for s in scenarios:
            assert s.gold.next_best_action, f"Scenario {s.scenario_id} has empty next_best_action"

    def test_all_scenarios_have_remediation_steps(self) -> None:
        scenarios = collect_all_scenarios()
        for s in scenarios:
            assert len(s.gold.remediation_steps) > 0, f"Scenario {s.scenario_id} has no remediation_steps"


class TestScenarioCoverage:
    def test_all_categories_are_covered(self) -> None:
        scenarios = collect_all_scenarios()
        covered = {s.gold.category for s in scenarios}
        assert covered == VALID_CATEGORIES, f"Missing categories: {VALID_CATEGORIES - covered}"

    def test_all_priorities_are_covered(self) -> None:
        scenarios = collect_all_scenarios()
        covered = {s.gold.priority for s in scenarios}
        assert covered == VALID_PRIORITIES, f"Missing priorities: {VALID_PRIORITIES - covered}"

    def test_all_teams_are_covered(self) -> None:
        scenarios = collect_all_scenarios()
        covered = {s.gold.assigned_team for s in scenarios}
        assert covered == VALID_TEAMS, f"Missing teams: {VALID_TEAMS - covered}"
