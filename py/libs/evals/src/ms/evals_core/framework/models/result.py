# Copyright (c) Microsoft. All rights reserved.
"""Pydantic models for evaluation results."""

from ms.common.models.base import FrozenBaseModel


class CheckResult(FrozenBaseModel):
    """Result of a single evaluation check."""

    name: str
    passed: bool
    message: str


class ScenarioResult(FrozenBaseModel):
    """Result of running a single evaluation scenario."""

    scenario_id: str
    passed: bool
    score: float
    checks: list[CheckResult]
    error: str | None = None


class CategorySummary(FrozenBaseModel):
    """Aggregated results for a scenario category."""

    category: str
    total_scenarios: int
    passed: int
    failed: int
    pass_rate: float
    mean_score: float
    per_scenario: list[ScenarioResult]
