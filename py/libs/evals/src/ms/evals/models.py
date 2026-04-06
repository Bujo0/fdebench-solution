# Copyright (c) Microsoft. All rights reserved.
"""Pydantic models for evaluation scenarios.

Defines structured models for IT support tickets, triage responses,
and evaluation scenarios used to test the triage system against
edge cases and adversarial inputs.
"""

import enum
from typing import Literal

from ms.common.models.base import FrozenBaseModel


class Channel(str, enum.Enum):
    """Ticket submission channel."""

    EMAIL = "email"
    CHAT = "chat"
    PORTAL = "portal"
    PHONE = "phone"


class Category(str, enum.Enum):
    """Valid ticket categories."""

    ACCESS_AUTH = "Access & Authentication"
    HARDWARE = "Hardware & Peripherals"
    NETWORK = "Network & Connectivity"
    SOFTWARE = "Software & Applications"
    SECURITY = "Security & Compliance"
    DATA_STORAGE = "Data & Storage"
    GENERAL = "General Inquiry"
    NOT_SUPPORT = "Not a Support Ticket"


class Priority(str, enum.Enum):
    """Valid priority levels."""

    P1 = "P1"
    P2 = "P2"
    P3 = "P3"
    P4 = "P4"


class AssignedTeam(str, enum.Enum):
    """Valid team assignments."""

    IAM = "Identity & Access Management"
    ENDPOINT = "Endpoint Engineering"
    NETWORK_OPS = "Network Operations"
    ENTERPRISE_APPS = "Enterprise Applications"
    SECURITY_OPS = "Security Operations"
    DATA_PLATFORM = "Data Platform"
    NONE = "None"


class MissingInformation(str, enum.Enum):
    """Constrained vocabulary for missing information items."""

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


class ScenarioTag(str, enum.Enum):
    """Tags that classify what a scenario is testing."""

    # Data cleanup tags
    LONG_EMAIL = "long_email"
    BASE64_CONTENT = "base64_content"
    HTML_EMAIL = "html_email"
    EMAIL_CHAIN = "email_chain"
    GARBLED_TEXT = "garbled_text"
    EMPTY_DESCRIPTION = "empty_description"
    MASSIVE_SIGNATURE = "massive_signature"
    REPEATED_CONTENT = "repeated_content"
    MIXED_LANGUAGE = "mixed_language"
    ATTACHMENT_ONLY = "attachment_only"
    UNICODE_HEAVY = "unicode_heavy"
    EXCESSIVE_WHITESPACE = "excessive_whitespace"

    # Responsible AI tags
    JAILBREAK = "jailbreak"
    PROMPT_INJECTION = "prompt_injection"
    HARMFUL_REQUEST = "harmful_request"
    SOCIAL_ENGINEERING = "social_engineering"
    PII_EXTRACTION = "pii_extraction"
    SYSTEM_PROMPT_LEAK = "system_prompt_leak"
    AUTHORITY_MANIPULATION = "authority_manipulation"
    THREAT_LANGUAGE = "threat_language"
    INSTRUCTION_OVERRIDE = "instruction_override"
    ADVERSARIAL_SUFFIX = "adversarial_suffix"
    MULTI_VECTOR_ATTACK = "multi_vector_attack"
    BIAS_EXPLOITATION = "bias_exploitation"


class Reporter(FrozenBaseModel):
    """Ticket reporter details."""

    name: str
    email: str
    department: str


class TicketInput(FrozenBaseModel):
    """An IT support ticket submitted for triage."""

    ticket_id: str
    subject: str
    description: str
    reporter: Reporter
    created_at: str
    channel: Channel
    attachments: list[str] = []


class TriageGold(FrozenBaseModel):
    """Expected gold-standard triage response for a ticket."""

    ticket_id: str
    category: Category
    priority: Priority
    assigned_team: AssignedTeam
    needs_escalation: bool
    missing_information: list[MissingInformation]
    next_best_action: str
    remediation_steps: list[str]


class EvalScenario(FrozenBaseModel):
    """A single evaluation scenario combining input, expected output, and metadata."""

    ticket: TicketInput
    gold: TriageGold
    tags: list[ScenarioTag]
    description: str
    category: Literal["data_cleanup", "responsible_ai"]

    def to_input_dict(self) -> dict[str, object]:
        """Return the ticket as a plain dict suitable for the /triage endpoint."""
        return self.ticket.model_dump(mode="json")

    def to_gold_dict(self) -> dict[str, object]:
        """Return the gold answer as a plain dict suitable for the scoring harness."""
        return self.gold.model_dump(mode="json")
