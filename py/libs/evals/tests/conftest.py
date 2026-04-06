# Copyright (c) Microsoft. All rights reserved.
"""Shared pytest fixtures for evaluation tests."""

import pytest

from ms.evals.scenarios.base import EvalScenario
from ms.evals.scenarios.data_cleanup import build_data_cleanup_scenarios
from ms.evals.scenarios.responsible_ai import build_responsible_ai_scenarios


@pytest.fixture(scope="session")
def data_cleanup_scenarios() -> list[EvalScenario]:
    """All data cleanup evaluation scenarios."""
    return build_data_cleanup_scenarios()


@pytest.fixture(scope="session")
def responsible_ai_scenarios() -> list[EvalScenario]:
    """All responsible AI evaluation scenarios."""
    return build_responsible_ai_scenarios()


@pytest.fixture(scope="session")
def all_scenarios(
    data_cleanup_scenarios: list[EvalScenario],
    responsible_ai_scenarios: list[EvalScenario],
) -> list[EvalScenario]:
    """All evaluation scenarios combined."""
    return [*data_cleanup_scenarios, *responsible_ai_scenarios]
