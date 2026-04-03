# Copyright (c) Microsoft. All rights reserved.
"""Pydantic models for evaluation tickets, gold answers, and results.

All domain values (categories, teams, priorities, missing-info vocabulary)
are defined here as single-source-of-truth enums/literals so that validation
is structural rather than stringly-typed.
"""

from enum import StrEnum
from typing import Literal

from ms.common.models.base import FrozenBaseModel


class Category(StrEnum):
    """Valid ticket categories as defined in the output schema."""

    ACCESS_AUTH = "Access & Authentication"
    HARDWARE = "Hardware & Peripherals"
    NETWORK = "Network & Connectivity"
    SOFTWARE = "Software & Applications"
    SECURITY = "Security & Compliance"
    DATA_STORAGE = "Data & Storage"
    GENERAL = "General Inquiry"
    NOT_SUPPORT = "Not a Support Ticket"


class AssignedTeam(StrEnum):
    """Valid routing teams as defined in the output schema."""

    IAM = "Identity & Access Management"
    ENDPOINT = "Endpoint Engineering"
    NETWORK_OPS = "Network Operations"
    ENTERPRISE_APPS = "Enterprise Applications"
    SECURITY_OPS = "Security Operations"
    DATA_PLATFORM = "Data Platform"
    NONE = "None"


class MissingInfoItem(StrEnum):
    """Constrained vocabulary for missing information fields."""

    AFFECTED_SYSTEM = "affected_system"
    ERROR_MESSAGE = "error_message"
    STEPS_TO_REPRODUCE = "steps_to_reproduce"
    AFFECTED_USERS = "affected_users"
    ENVIRONMENT_DETAILS = "environment_details"
    TIMESTAMP = "timestamp"
    PREVIOUS_TICKET_ID = "previous_ticket_id"
    CONTACT_INFO = "contact_info"
    DEVICE_INFO = "device_info"
    APPLICATION_VERSION = "application_version"
    NETWORK_LOCATION = "network_location"
    BUSINESS_IMPACT = "business_impact"
    REPRODUCTION_FREQUENCY = "reproduction_frequency"
    SCREENSHOT_OR_ATTACHMENT = "screenshot_or_attachment"
    AUTHENTICATION_METHOD = "authentication_method"
    CONFIGURATION_DETAILS = "configuration_details"


type Priority = Literal["P1", "P2", "P3", "P4"]
type Channel = Literal["email", "chat", "portal", "phone"]


class Reporter(FrozenBaseModel):
    """Ticket reporter information."""

    name: str
    email: str
    department: str


class Ticket(FrozenBaseModel):
    """An IT support ticket as input to the triage system."""

    ticket_id: str
    subject: str
    description: str
    reporter: Reporter
    created_at: str
    channel: Channel
    attachments: list[str] = []


class TriageResponse(FrozenBaseModel):
    """Expected triage output from the system under test."""

    ticket_id: str
    category: str
    priority: str
    assigned_team: str
    needs_escalation: bool
    missing_information: list[str]
    next_best_action: str
    remediation_steps: list[str]


class GoldAnswer(FrozenBaseModel):
    """Gold-standard triage decision for scoring."""

    ticket_id: str
    category: Category
    priority: Priority
    assigned_team: AssignedTeam
    needs_escalation: bool
    missing_information: list[MissingInfoItem]
    next_best_action: str
    remediation_steps: list[str]


class DimensionScores(FrozenBaseModel):
    """Per-ticket scores for each classification dimension."""

    category: float
    priority: float
    routing: float
    escalation: float
    missing_info: float
    weighted_total: float


class EvalResult(FrozenBaseModel):
    """Evaluation result for a single ticket."""

    ticket_id: str
    scores: DimensionScores
    response: TriageResponse
    gold: GoldAnswer
    latency_ms: float
    error: str | None = None


class DimensionAggregates(FrozenBaseModel):
    """Aggregate scores across all tickets for each dimension."""

    category: float
    priority: float
    routing: float
    missing_info: float
    escalation: float


class EvalSummary(FrozenBaseModel):
    """Summary of an evaluation run across all tickets."""

    dataset_kind: str
    tickets_total: int
    tickets_scored: int
    tickets_errored: int
    dimension_scores: DimensionAggregates
    classification_score: float
    results: list[EvalResult]
