# Copyright (c) Microsoft. All rights reserved.
"""Base types for scenario definitions."""

from dataclasses import dataclass
from dataclasses import field


@dataclass(frozen=True)
class ScenarioGold:
    """Deterministic gold-standard triage answer for a scenario."""

    category: str
    priority: str
    assigned_team: str
    needs_escalation: bool
    missing_information: tuple[str, ...]
    next_best_action: str
    remediation_steps: tuple[str, ...]


@dataclass(frozen=True)
class ScenarioDefinition:
    """A unique IT support scenario that can be expanded into multiple tickets.

    Each scenario represents a distinct problem. The generator combines
    subjects/descriptions with reporter and channel variations to produce
    multiple unique tickets from one scenario.
    """

    scenario_id: str
    subjects: tuple[str, ...]
    descriptions: tuple[str, ...]
    gold: ScenarioGold
    # Optional constraints
    departments: tuple[str, ...] = ()
    channels: tuple[str, ...] = ()
    attachment_sets: tuple[tuple[str, ...], ...] = ()
    tags: tuple[str, ...] = field(default_factory=tuple)
