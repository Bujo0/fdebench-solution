"""Scenario registry that collects all scenarios from category modules."""

import ms.evals_core.scenarios.data_cleanup as data_cleanup
import ms.evals_core.scenarios.data_storage as data_storage
import ms.evals_core.scenarios.general_inquiry as general_inquiry
import ms.evals_core.scenarios.hardware as hardware
import ms.evals_core.scenarios.network as network
import ms.evals_core.scenarios.not_support as not_support
import ms.evals_core.scenarios.responsible_ai as responsible_ai
from ms.evals_core.scenarios.base import ScenarioDefinition


def get_all_scenarios() -> list[ScenarioDefinition]:
    """Collect all scenario definitions from all category modules.

    Returns:
        List of all scenario definitions across all categories.
    """
    all_scenarios: list[ScenarioDefinition] = []
    all_scenarios.extend(hardware.get_scenarios())
    all_scenarios.extend(network.get_scenarios())
    all_scenarios.extend(data_storage.get_scenarios())
    all_scenarios.extend(general_inquiry.get_scenarios())
    all_scenarios.extend(not_support.get_scenarios())
    all_scenarios.extend(data_cleanup.get_scenarios())
    all_scenarios.extend(responsible_ai.get_scenarios())

    return all_scenarios
