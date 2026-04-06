# Copyright (c) Microsoft. All rights reserved.
"""Scenario registry for collecting and selecting scenario templates.

Provides a central registry that scenario modules register their templates
into, and selection logic for balanced dataset generation.
"""

import random

from ms.evals.constants import Category
from ms.evals.models import ScenarioTemplate

_REGISTRY: dict[Category, list[ScenarioTemplate]] = {cat: [] for cat in Category}


def register(template: ScenarioTemplate) -> ScenarioTemplate:
    """Register a scenario template in the global registry."""
    _REGISTRY[template.category].append(template)
    return template


def get_scenarios(category: Category) -> list[ScenarioTemplate]:
    """Get all registered scenarios for a category."""
    return _REGISTRY[category]


def get_all_scenarios() -> list[ScenarioTemplate]:
    """Get all registered scenarios across all categories."""
    result: list[ScenarioTemplate] = []
    for scenarios in _REGISTRY.values():
        result.extend(scenarios)
    return result


def pick_scenario(category: Category, rng: random.Random) -> ScenarioTemplate:
    """Pick a random scenario template for the given category."""
    scenarios = _REGISTRY[category]
    if not scenarios:
        msg = f"No scenarios registered for category: {category}"
        raise ValueError(msg)
    return rng.choice(scenarios)


def get_scenario_counts() -> dict[str, int]:
    """Get the count of registered scenarios per category."""
    return {cat.value: len(scenarios) for cat, scenarios in _REGISTRY.items()}
