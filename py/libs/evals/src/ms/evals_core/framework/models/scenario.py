# Copyright (c) Microsoft. All rights reserved.
"""Pydantic models for evaluation scenarios."""

from enum import StrEnum

from ms.common.models.base import FrozenBaseModel


class ScenarioCategory(StrEnum):
    """Top-level category for evaluation scenarios."""

    DATA_CLEANUP = "data_cleanup"
    RESPONSIBLE_AI = "responsible_ai"


class EvalReporter(FrozenBaseModel):
    """Reporter details for an evaluation ticket."""

    name: str
    email: str
    department: str


class EvalTicket(FrozenBaseModel):
    """A synthetic ticket used as input for an evaluation scenario."""

    ticket_id: str
    subject: str
    description: str
    reporter: EvalReporter
    created_at: str
    channel: str
    attachments: list[str] = []


class ExpectedTriage(FrozenBaseModel):
    """Expected triage output fields.

    Fields set to None indicate "any valid value is acceptable".
    """

    category: str | None = None
    priority: str | None = None
    assigned_team: str | None = None
    needs_escalation: bool | None = None
    missing_information: list[str] | None = None


class ResponseConstraint(FrozenBaseModel):
    """Constraints on what a valid response must satisfy.

    Used for responsible AI checks: ensuring the response doesn't
    contain forbidden strings, follow injected instructions, etc.
    """

    must_be_valid_json: bool = True
    must_have_valid_category: bool = True
    must_have_valid_priority: bool = True
    must_have_valid_team: bool = True
    must_not_contain: list[str] = []
    must_not_contain_in_remediation: list[str] = []


class EvalScenario(FrozenBaseModel):
    """A single evaluation scenario with ticket input, expectations, and constraints."""

    scenario_id: str
    name: str
    description: str
    category: ScenarioCategory
    tags: list[str] = []
    ticket: EvalTicket
    expected_triage: ExpectedTriage | None = None
    constraints: ResponseConstraint = ResponseConstraint()
