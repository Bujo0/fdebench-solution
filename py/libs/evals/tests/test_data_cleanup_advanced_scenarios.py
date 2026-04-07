# Copyright (c) Microsoft. All rights reserved.
"""Tests for advanced data cleanup evaluation scenarios (DC-265 through DC-284).

Validates that:
1. All new data cleanup scenarios are well-formed (valid ScenarioDefinitions)
2. Gold answers use valid enum values from the constrained vocabulary
3. New scenario IDs are unique and don't conflict with existing ones
4. Scenarios cover the expected range of advanced data quality issues
5. All scenarios can be converted to Scenario models
"""

from ms.evals_core.constants import ALL_CATEGORIES
from ms.evals_core.constants import ALL_MISSING_INFO_FIELDS
from ms.evals_core.constants import ALL_PRIORITIES
from ms.evals_core.constants import ALL_TEAMS
from ms.evals_core.scenarios.data_cleanup import get_scenarios


class TestAdvancedDataCleanupScenarios:
    """Verify that DC-265 through DC-284 scenarios are well-formed."""

    def test_advanced_scenario_ids_exist(self) -> None:
        """Verify all advanced scenario IDs DC-265 through DC-284 exist."""
        scenarios = get_scenarios()
        ids = {s.scenario_id for s in scenarios}
        expected = {f"DC-{i:03d}" for i in range(265, 285)}
        assert expected.issubset(ids), f"Missing advanced DC IDs: {expected - ids}"

    def test_total_scenario_count_increased(self) -> None:
        """Data cleanup should now have at least 284 scenarios."""
        scenarios = get_scenarios()
        assert len(scenarios) >= 284, f"Expected >= 284 DC scenarios, got {len(scenarios)}"

    def test_all_ids_still_unique(self) -> None:
        """No duplicate scenario IDs after adding new ones."""
        scenarios = get_scenarios()
        ids = [s.scenario_id for s in scenarios]
        assert len(ids) == len(set(ids)), f"Duplicate IDs: {[x for x in ids if ids.count(x) > 1]}"

    def test_new_scenarios_have_required_fields(self) -> None:
        """All new scenarios must have required fields populated."""
        scenarios = get_scenarios()
        new_ids = {f"DC-{i:03d}" for i in range(265, 285)}
        new_scenarios = [s for s in scenarios if s.scenario_id in new_ids]
        assert len(new_scenarios) == 20, f"Expected 20 new scenarios, got {len(new_scenarios)}"

        for s in new_scenarios:
            assert s.subject, f"{s.scenario_id}: empty subject"
            assert s.description, f"{s.scenario_id}: empty description"
            assert len(s.description) >= 200, f"{s.scenario_id}: description too short ({len(s.description)} chars)"
            assert s.reporter_name, f"{s.scenario_id}: empty reporter_name"
            assert s.reporter_email, f"{s.scenario_id}: empty reporter_email"
            assert "@contoso.com" in s.reporter_email, f"{s.scenario_id}: email not @contoso.com"
            assert s.reporter_department, f"{s.scenario_id}: empty reporter_department"
            assert s.next_best_action, f"{s.scenario_id}: empty next_best_action"
            assert len(s.remediation_steps) > 0, f"{s.scenario_id}: no remediation_steps"

    def test_new_scenarios_have_data_cleanup_tag(self) -> None:
        """All new scenarios must have the 'data-cleanup' tag."""
        scenarios = get_scenarios()
        new_ids = {f"DC-{i:03d}" for i in range(265, 285)}
        new_scenarios = [s for s in scenarios if s.scenario_id in new_ids]

        for s in new_scenarios:
            assert "data-cleanup" in s.tags, f"{s.scenario_id}: missing 'data-cleanup' tag"

    def test_new_scenarios_gold_categories_valid(self) -> None:
        """All gold categories must be from the valid vocabulary."""
        scenarios = get_scenarios()
        new_ids = {f"DC-{i:03d}" for i in range(265, 285)}
        new_scenarios = [s for s in scenarios if s.scenario_id in new_ids]

        for s in new_scenarios:
            assert s.category.value in ALL_CATEGORIES, f"{s.scenario_id}: invalid category '{s.category}'"

    def test_new_scenarios_gold_priorities_valid(self) -> None:
        """All gold priorities must be from the valid vocabulary."""
        scenarios = get_scenarios()
        new_ids = {f"DC-{i:03d}" for i in range(265, 285)}
        new_scenarios = [s for s in scenarios if s.scenario_id in new_ids]

        for s in new_scenarios:
            assert s.priority.value in ALL_PRIORITIES, f"{s.scenario_id}: invalid priority '{s.priority}'"

    def test_new_scenarios_gold_teams_valid(self) -> None:
        """All gold teams must be from the valid vocabulary."""
        scenarios = get_scenarios()
        new_ids = {f"DC-{i:03d}" for i in range(265, 285)}
        new_scenarios = [s for s in scenarios if s.scenario_id in new_ids]

        for s in new_scenarios:
            assert s.team.value in ALL_TEAMS, f"{s.scenario_id}: invalid team '{s.team}'"

    def test_new_scenarios_gold_missing_info_valid(self) -> None:
        """All gold missing_info items must be from the valid vocabulary."""
        scenarios = get_scenarios()
        new_ids = {f"DC-{i:03d}" for i in range(265, 285)}
        new_scenarios = [s for s in scenarios if s.scenario_id in new_ids]

        for s in new_scenarios:
            for item in s.missing_info:
                assert item.value in ALL_MISSING_INFO_FIELDS, f"{s.scenario_id}: invalid missing info '{item}'"

    def test_new_scenarios_convert_to_scenario_model(self) -> None:
        """All new scenarios must successfully convert to Scenario models."""
        scenarios = get_scenarios()
        new_ids = {f"DC-{i:03d}" for i in range(265, 285)}
        new_scenarios = [s for s in scenarios if s.scenario_id in new_ids]

        for idx, s in enumerate(new_scenarios):
            scenario = s.to_scenario(f"INC-ADV-{idx:04d}")
            assert scenario.ticket.ticket_id == f"INC-ADV-{idx:04d}"
            assert scenario.gold.ticket_id == f"INC-ADV-{idx:04d}"
            assert scenario.gold.category is not None
            assert scenario.gold.priority is not None
            assert scenario.gold.assigned_team is not None


class TestAdvancedDataCleanupDiversity:
    """Verify that new scenarios cover diverse categories and noise types."""

    def test_covers_multiple_categories(self) -> None:
        """New scenarios should span at least 4 different categories."""
        scenarios = get_scenarios()
        new_ids = {f"DC-{i:03d}" for i in range(265, 285)}
        new_scenarios = [s for s in scenarios if s.scenario_id in new_ids]

        categories = {s.category.value for s in new_scenarios}
        assert len(categories) >= 4, f"Expected >= 4 categories, got {len(categories)}: {categories}"

    def test_covers_multiple_priorities(self) -> None:
        """New scenarios should span at least 3 priority levels."""
        scenarios = get_scenarios()
        new_ids = {f"DC-{i:03d}" for i in range(265, 285)}
        new_scenarios = [s for s in scenarios if s.scenario_id in new_ids]

        priorities = {s.priority.value for s in new_scenarios}
        assert len(priorities) >= 3, f"Expected >= 3 priorities, got {len(priorities)}: {priorities}"

    def test_covers_multiple_channels(self) -> None:
        """New scenarios should use at least 3 different channels."""
        scenarios = get_scenarios()
        new_ids = {f"DC-{i:03d}" for i in range(265, 285)}
        new_scenarios = [s for s in scenarios if s.scenario_id in new_ids]

        channels = {s.channel.value for s in new_scenarios}
        assert len(channels) >= 3, f"Expected >= 3 channels, got {len(channels)}: {channels}"

    def test_new_tags_cover_advanced_noise_types(self) -> None:
        """New scenarios should introduce tags for advanced data quality issues."""
        scenarios = get_scenarios()
        new_ids = {f"DC-{i:03d}" for i in range(265, 285)}
        new_scenarios = [s for s in scenarios if s.scenario_id in new_ids]

        all_new_tags = set()
        for s in new_scenarios:
            all_new_tags.update(s.tags)
        all_new_tags.discard("data-cleanup")

        # Should have at least 15 distinct specific tags across 20 scenarios
        assert len(all_new_tags) >= 15, f"Expected >= 15 distinct tags, got {len(all_new_tags)}: {all_new_tags}"

    def test_descriptions_are_substantial(self) -> None:
        """Descriptions should be substantial (> 300 chars) for data cleanup scenarios."""
        scenarios = get_scenarios()
        new_ids = {f"DC-{i:03d}" for i in range(265, 285)}
        new_scenarios = [s for s in scenarios if s.scenario_id in new_ids]

        for s in new_scenarios:
            assert len(s.description) >= 300, (
                f"{s.scenario_id}: description too short ({len(s.description)} chars), "
                f"data cleanup scenarios need substantial noisy content"
            )

    def test_no_duplicate_subjects(self) -> None:
        """No two new scenarios should have the same subject."""
        scenarios = get_scenarios()
        new_ids = {f"DC-{i:03d}" for i in range(265, 285)}
        new_scenarios = [s for s in scenarios if s.scenario_id in new_ids]

        subjects = [s.subject for s in new_scenarios]
        assert len(subjects) == len(set(subjects)), "Duplicate subjects found among new scenarios"
