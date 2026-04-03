# Copyright (c) Microsoft. All rights reserved.
"""Collects all scenario definitions from category modules."""

from ms.eval_generator.scenarios._base import ScenarioDefinition
from ms.eval_generator.scenarios._base import ScenarioGold
from ms.eval_generator.scenarios.access_auth import ACCESS_AUTH_SCENARIOS
from ms.eval_generator.scenarios.data_storage import DATA_STORAGE_SCENARIOS
from ms.eval_generator.scenarios.edge_cases import EDGE_CASE_SCENARIOS
from ms.eval_generator.scenarios.general_inquiry import GENERAL_INQUIRY_SCENARIOS
from ms.eval_generator.scenarios.hardware import HARDWARE_SCENARIOS
from ms.eval_generator.scenarios.network import NETWORK_SCENARIOS
from ms.eval_generator.scenarios.non_ticket import NON_TICKET_SCENARIOS
from ms.eval_generator.scenarios.security import SECURITY_SCENARIOS
from ms.eval_generator.scenarios.software import SOFTWARE_SCENARIOS


def collect_all_scenarios() -> list[ScenarioDefinition]:
    """Return all scenario definitions from every category module."""
    all_scenarios: list[ScenarioDefinition] = []
    all_scenarios.extend(ACCESS_AUTH_SCENARIOS)
    all_scenarios.extend(HARDWARE_SCENARIOS)
    all_scenarios.extend(NETWORK_SCENARIOS)
    all_scenarios.extend(SOFTWARE_SCENARIOS)
    all_scenarios.extend(SECURITY_SCENARIOS)
    all_scenarios.extend(DATA_STORAGE_SCENARIOS)
    all_scenarios.extend(GENERAL_INQUIRY_SCENARIOS)
    all_scenarios.extend(NON_TICKET_SCENARIOS)
    all_scenarios.extend(EDGE_CASE_SCENARIOS)

    # Validate uniqueness of scenario IDs
    ids = [s.scenario_id for s in all_scenarios]
    duplicates = [sid for sid in ids if ids.count(sid) > 1]
    if duplicates:
        raise ValueError(f"Duplicate scenario IDs found: {set(duplicates)}")

    return all_scenarios


__all__ = [
    "ScenarioDefinition",
    "ScenarioGold",
    "collect_all_scenarios",
]
