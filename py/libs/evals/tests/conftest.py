# Copyright (c) Microsoft. All rights reserved.
"""Shared fixtures for evals tests."""

from pathlib import Path

import pytest

from ms.evals_core.framework.models.scenario import EvalScenario
from ms.evals_core.framework.models.scenario import ScenarioCategory
from ms.evals_core.framework.scenarios.registry import default_registry


@pytest.fixture
def data_dir() -> Path:
    """Path to the docs/data/tickets/ directory."""
    current = Path(__file__).resolve()
    for parent in current.parents:
        tickets_dir = parent / "docs" / "data" / "tickets"
        if tickets_dir.is_dir():
            return tickets_dir
    pytest.fail("Could not locate docs/data/tickets/ directory")


@pytest.fixture()
def data_cleanup_scenarios() -> list[EvalScenario]:
    """Load all data cleanup scenarios."""
    import ms.evals_core.framework.scenarios.data_cleanup  # noqa: F401, PLC0415

    return default_registry.by_category(ScenarioCategory.DATA_CLEANUP)


@pytest.fixture()
def responsible_ai_scenarios() -> list[EvalScenario]:
    """Load all responsible AI scenarios."""
    import ms.evals_core.framework.scenarios.responsible_ai  # noqa: F401, PLC0415

    return default_registry.by_category(ScenarioCategory.RESPONSIBLE_AI)
