# Copyright (c) Microsoft. All rights reserved.
"""Tests for the scenario registry."""

import pytest

from ms.evals.models.scenario import EvalReporter
from ms.evals.models.scenario import EvalScenario
from ms.evals.models.scenario import EvalTicket
from ms.evals.models.scenario import ScenarioCategory
from ms.evals.scenarios.registry import ScenarioRegistry


def _make_scenario(scenario_id: str, category: ScenarioCategory, tags: list[str] | None = None) -> EvalScenario:
    return EvalScenario(
        scenario_id=scenario_id,
        name=f"Test {scenario_id}",
        description="Test scenario",
        category=category,
        tags=tags or [],
        ticket=EvalTicket(
            ticket_id=f"INC-{scenario_id}",
            subject="Test",
            description="Test description",
            reporter=EvalReporter(name="Test", email="test@contoso.com", department="IT"),
            created_at="2026-01-01T00:00:00Z",
            channel="email",
        ),
    )


class TestScenarioRegistry:
    def test_register_and_get(self) -> None:
        registry = ScenarioRegistry()
        scenario = _make_scenario("test-001", ScenarioCategory.DATA_CLEANUP)
        registry.register(scenario)
        assert registry.get("test-001") == scenario

    def test_duplicate_raises(self) -> None:
        registry = ScenarioRegistry()
        scenario = _make_scenario("dup-001", ScenarioCategory.DATA_CLEANUP)
        registry.register(scenario)
        with pytest.raises(ValueError, match="Duplicate scenario ID"):
            registry.register(scenario)

    def test_get_missing_raises(self) -> None:
        registry = ScenarioRegistry()
        with pytest.raises(KeyError):
            registry.get("nonexistent")

    def test_all_sorted(self) -> None:
        registry = ScenarioRegistry()
        registry.register(_make_scenario("z-001", ScenarioCategory.DATA_CLEANUP))
        registry.register(_make_scenario("a-001", ScenarioCategory.RESPONSIBLE_AI))
        all_scenarios = registry.all()
        assert [s.scenario_id for s in all_scenarios] == ["a-001", "z-001"]

    def test_by_category(self) -> None:
        registry = ScenarioRegistry()
        registry.register(_make_scenario("dc-001", ScenarioCategory.DATA_CLEANUP))
        registry.register(_make_scenario("rai-001", ScenarioCategory.RESPONSIBLE_AI))
        registry.register(_make_scenario("dc-002", ScenarioCategory.DATA_CLEANUP))

        dc = registry.by_category(ScenarioCategory.DATA_CLEANUP)
        assert [s.scenario_id for s in dc] == ["dc-001", "dc-002"]

        rai = registry.by_category(ScenarioCategory.RESPONSIBLE_AI)
        assert [s.scenario_id for s in rai] == ["rai-001"]

    def test_by_tag(self) -> None:
        registry = ScenarioRegistry()
        registry.register(_make_scenario("t-001", ScenarioCategory.DATA_CLEANUP, tags=["base64", "noise"]))
        registry.register(_make_scenario("t-002", ScenarioCategory.DATA_CLEANUP, tags=["html", "noise"]))
        registry.register(_make_scenario("t-003", ScenarioCategory.RESPONSIBLE_AI, tags=["jailbreak"]))

        noise = registry.by_tag("noise")
        assert [s.scenario_id for s in noise] == ["t-001", "t-002"]

        jailbreak = registry.by_tag("jailbreak")
        assert len(jailbreak) == 1
        assert jailbreak[0].scenario_id == "t-003"

    def test_count(self) -> None:
        registry = ScenarioRegistry()
        assert registry.count == 0
        registry.register(_make_scenario("c-001", ScenarioCategory.DATA_CLEANUP))
        assert registry.count == 1
        registry.register(_make_scenario("c-002", ScenarioCategory.RESPONSIBLE_AI))
        assert registry.count == 2

    def test_empty_by_category(self) -> None:
        registry = ScenarioRegistry()
        assert registry.by_category(ScenarioCategory.DATA_CLEANUP) == []

    def test_empty_by_tag(self) -> None:
        registry = ScenarioRegistry()
        assert registry.by_tag("nonexistent") == []
