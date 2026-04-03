# Copyright (c) Microsoft. All rights reserved.
"""Pydantic models for eval ticket generation.

Defines the data structures for scenario templates, generated tickets,
and gold-standard triage answers.
"""

from ms.common.models.base import FrozenBaseModel
from ms.evals.constants import Category
from ms.evals.constants import MissingInfo
from ms.evals.constants import Priority
from ms.evals.constants import Team


class Reporter(FrozenBaseModel):
    """Ticket reporter information."""

    name: str
    email: str
    department: str


class Ticket(FrozenBaseModel):
    """An IT support ticket submitted to the triage system."""

    ticket_id: str
    subject: str
    description: str
    reporter: Reporter
    created_at: str
    channel: str
    attachments: list[str] = []


class TriageGold(FrozenBaseModel):
    """Gold-standard triage output for scoring."""

    ticket_id: str
    category: str
    priority: str
    assigned_team: str
    needs_escalation: bool
    missing_information: list[str]
    next_best_action: str
    remediation_steps: list[str]


class ScenarioTemplate(FrozenBaseModel):
    """A template for generating a specific type of ticket.

    Each scenario defines both the ticket content patterns and the
    deterministic gold answer. Templates use {placeholder} syntax
    for parameterizable elements.
    """

    scenario_id: str
    category: Category
    priority: Priority
    assigned_team: Team
    needs_escalation: bool
    missing_information: list[MissingInfo]
    subjects: list[str]
    descriptions: list[str]
    next_best_actions: list[str]
    remediation_steps: list[list[str]]
    attachment_options: list[list[str]] = []


class GenerationStats(FrozenBaseModel):
    """Statistics about a generated dataset."""

    total_tickets: int
    category_counts: dict[str, int]
    priority_counts: dict[str, int]
    team_counts: dict[str, int]
    channel_counts: dict[str, int]
    escalation_counts: dict[str, int]
    missing_info_counts: dict[str, int]
    modifier_counts: dict[str, int]
    unique_subjects: int
    unique_descriptions: int
