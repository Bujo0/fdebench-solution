# Copyright (c) Microsoft. All rights reserved.
"""Shared fixtures for evals tests."""

import pytest

from ms.evals_core.framework.models.scenario import EvalScenario
from ms.evals_core.framework.models.scenario import ScenarioCategory
from ms.evals_core.framework.scenarios.registry import default_registry


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
