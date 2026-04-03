"""Tests for data cleanup evaluation scenarios."""

from ms.evals_core.scenarios.data_cleanup import get_scenarios


class TestDataCleanupScenarios:
    """Verify that all data cleanup scenarios are well-formed."""

    def test_returns_scenarios(self) -> None:
        scenarios = get_scenarios()
        assert len(scenarios) > 0, "No data cleanup scenarios returned"

    def test_all_scenario_ids_unique(self) -> None:
        scenarios = get_scenarios()
        ids = [s.scenario_id for s in scenarios]
        assert len(ids) == len(set(ids)), f"Duplicate IDs: {[x for x in ids if ids.count(x) > 1]}"

    def test_all_scenarios_have_required_fields(self) -> None:
        scenarios = get_scenarios()
        for s in scenarios:
            assert s.subject, f"{s.scenario_id}: empty subject"
            assert s.description, f"{s.scenario_id}: empty description"
            assert s.reporter_name, f"{s.scenario_id}: empty reporter_name"
            assert s.reporter_email, f"{s.scenario_id}: empty reporter_email"
            assert s.reporter_department, f"{s.scenario_id}: empty reporter_department"
            assert s.next_best_action, f"{s.scenario_id}: empty next_best_action"
            assert len(s.remediation_steps) > 0, f"{s.scenario_id}: no remediation_steps"

    def test_all_scenarios_have_tags(self) -> None:
        scenarios = get_scenarios()
        for s in scenarios:
            assert len(s.tags) > 0, f"{s.scenario_id}: no tags"
            assert "data-cleanup" in s.tags, f"{s.scenario_id}: missing 'data-cleanup' tag"

    def test_scenarios_convert_to_scenario_model(self) -> None:
        scenarios = get_scenarios()
        for idx, s in enumerate(scenarios):
            scenario = s.to_scenario(f"INC-TEST-{idx:04d}")
            assert scenario.ticket.ticket_id == f"INC-TEST-{idx:04d}"
            assert scenario.gold.ticket_id == f"INC-TEST-{idx:04d}"
            assert scenario.gold.category is not None
            assert scenario.gold.priority is not None
            assert scenario.gold.assigned_team is not None

    def test_known_scenario_ids(self) -> None:
        """Verify expected scenario IDs exist."""
        scenarios = get_scenarios()
        ids = {s.scenario_id for s in scenarios}
        expected = {f"DC-{i:03d}" for i in range(1, 13)}
        assert expected.issubset(ids), f"Missing IDs: {expected - ids}"
