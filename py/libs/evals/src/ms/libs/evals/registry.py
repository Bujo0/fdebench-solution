"""Scenario registry for collecting and querying evaluation scenarios."""

from ms.libs.evals.models.enums import ScenarioTag
from ms.libs.evals.models.scenario import EvalScenario
from ms.libs.evals.scenarios.data_cleanup import get_data_cleanup_scenarios
from ms.libs.evals.scenarios.responsible_ai import get_responsible_ai_scenarios


def get_all_scenarios() -> list[EvalScenario]:
    """Return all evaluation scenarios across all tags."""
    return get_data_cleanup_scenarios() + get_responsible_ai_scenarios()


def get_scenarios_by_tag(tag: ScenarioTag) -> list[EvalScenario]:
    """Return evaluation scenarios filtered by tag."""
    tag_to_loader: dict[ScenarioTag, list[EvalScenario]] = {
        ScenarioTag.DATA_CLEANUP: get_data_cleanup_scenarios(),
        ScenarioTag.RESPONSIBLE_AI: get_responsible_ai_scenarios(),
    }
    return tag_to_loader.get(tag, [])
