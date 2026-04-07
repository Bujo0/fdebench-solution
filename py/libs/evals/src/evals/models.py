# Copyright (c) Microsoft. All rights reserved.
"""Pydantic models for evaluation test scenarios.

These models mirror the JSON schemas in docs/data/schemas/ and provide
type-safe representations of tickets, triage decisions, and test scenarios.
"""

from enum import StrEnum
from typing import Literal

from ms.common.models.base import FrozenBaseModel


class Channel(StrEnum):
    """Ticket submission channels."""

    EMAIL = "email"
    CHAT = "chat"
    PORTAL = "portal"
    PHONE = "phone"


class Category(StrEnum):
    """Valid ticket categories (8 values)."""

    ACCESS_AUTH = "Access & Authentication"
    HARDWARE = "Hardware & Peripherals"
    NETWORK = "Network & Connectivity"
    SOFTWARE = "Software & Applications"
    SECURITY = "Security & Compliance"
    DATA = "Data & Storage"
    GENERAL = "General Inquiry"
    NOT_SUPPORT = "Not a Support Ticket"


class Team(StrEnum):
    """Valid routing teams (7 values)."""

    IAM = "Identity & Access Management"
    ENDPOINT = "Endpoint Engineering"
    NETWORK_OPS = "Network Operations"
    ENTERPRISE_APPS = "Enterprise Applications"
    SECURITY_OPS = "Security Operations"
    DATA_PLATFORM = "Data Platform"
    NONE = "None"


class Priority(StrEnum):
    """Ticket priority levels."""

    P1 = "P1"
    P2 = "P2"
    P3 = "P3"
    P4 = "P4"


class MissingInfoField(StrEnum):
    """Valid missing information vocabulary (16 values)."""

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


class ScenarioTag(StrEnum):
    """Tags for categorizing test scenarios."""

    DATA_CLEANUP = "data_cleanup"
    RESPONSIBLE_AI = "responsible_ai"
    PROMPT_INJECTION = "prompt_injection"
    JAILBREAK = "jailbreak"
    SOCIAL_ENGINEERING = "social_engineering"
    NOISE = "noise"
    ENCODING = "encoding"
    LONG_CONTENT = "long_content"
    MALFORMED = "malformed"
    MANIPULATION = "manipulation"
    HARMFUL_CONTENT = "harmful_content"
    DATA_EXFILTRATION = "data_exfiltration"


class Reporter(FrozenBaseModel):
    """Ticket reporter details."""

    name: str
    email: str
    department: str


class Ticket(FrozenBaseModel):
    """An IT support ticket matching the input JSON schema."""

    ticket_id: str
    subject: str
    description: str
    reporter: Reporter
    created_at: str
    channel: Channel
    attachments: list[str] = []


class TriageDecision(FrozenBaseModel):
    """Expected triage output matching the output JSON schema."""

    ticket_id: str
    category: Category
    priority: Priority
    assigned_team: Team
    needs_escalation: bool
    missing_information: list[MissingInfoField]
    next_best_action: str
    remediation_steps: list[str]


class EvalScenario(FrozenBaseModel):
    """A single evaluation test scenario pairing a ticket with its gold answer.

    Each scenario documents what edge case it tests and why the expected
    triage decision is correct.
    """

    scenario_id: str
    name: str
    description: str
    tags: list[ScenarioTag]
    ticket: Ticket
    gold: TriageDecision
    rationale: str


class ScenarioSuite(FrozenBaseModel):
    """A collection of evaluation scenarios."""

    suite_name: str
    suite_description: str
    suite_type: Literal["data_cleanup", "responsible_ai"]
    scenarios: list[EvalScenario]

    def get_tickets(self) -> list[dict[str, object]]:
        """Export tickets as list of dicts for JSON serialization."""
        return [scenario.ticket.model_dump() for scenario in self.scenarios]

    def get_gold_answers(self) -> list[dict[str, object]]:
        """Export gold answers as list of dicts for JSON serialization."""
        return [scenario.gold.model_dump() for scenario in self.scenarios]
