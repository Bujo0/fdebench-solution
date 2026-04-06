"""Tests for the scenario registry including data cleanup and responsible AI."""

from ms.evals_core.scenarios import get_all_scenarios


class TestScenarioRegistry:
    """Verify the complete scenario registry."""

    def test_get_all_scenarios_includes_data_cleanup(self) -> None:
        scenarios = get_all_scenarios()
        dc_ids = [s.scenario_id for s in scenarios if s.scenario_id.startswith("DC-")]
        assert len(dc_ids) > 0, "No data cleanup scenarios in registry"

    def test_get_all_scenarios_includes_responsible_ai(self) -> None:
        scenarios = get_all_scenarios()
        rai_ids = [s.scenario_id for s in scenarios if s.scenario_id.startswith("RAI-")]
        assert len(rai_ids) > 0, "No responsible AI scenarios in registry"

    def test_all_scenario_ids_globally_unique(self) -> None:
        scenarios = get_all_scenarios()
        ids = [s.scenario_id for s in scenarios]
        duplicates = [x for x in ids if ids.count(x) > 1]
        assert len(duplicates) == 0, f"Duplicate scenario IDs in registry: {set(duplicates)}"

    def test_total_scenario_count(self) -> None:
        scenarios = get_all_scenarios()
        # Ensure we have a reasonable number of total scenarios
        assert len(scenarios) >= 30, f"Expected at least 30 scenarios, got {len(scenarios)}"
