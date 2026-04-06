# Copyright (c) Microsoft. All rights reserved.
"""Output triage decision model matching the docs/data/schemas/output.json schema."""

from enum import StrEnum

from ms.common.models.base import FrozenBaseModel


class TicketCategory(StrEnum):
    """The 8 valid ticket categories."""

    ACCESS_AUTH = "Access & Authentication"
    HARDWARE = "Hardware & Peripherals"
    NETWORK = "Network & Connectivity"
    SOFTWARE = "Software & Applications"
    SECURITY = "Security & Compliance"
    DATA_STORAGE = "Data & Storage"
    GENERAL = "General Inquiry"
    NOT_SUPPORT = "Not a Support Ticket"


class Priority(StrEnum):
    """Ticket priority levels."""

    P1 = "P1"
    P2 = "P2"
    P3 = "P3"
    P4 = "P4"


class AssignedTeam(StrEnum):
    """The 7 valid specialist teams."""

    IAM = "Identity & Access Management"
    ENDPOINT = "Endpoint Engineering"
    NETWORK = "Network Operations"
    ENTERPRISE_APPS = "Enterprise Applications"
    SECURITY = "Security Operations"
    DATA_PLATFORM = "Data Platform"
    NONE = "None"


class MissingInformation(StrEnum):
    """The 16 valid missing information values."""

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


class TriageDecision(FrozenBaseModel):
    """The expected triage output for a single ticket.

    Matches the output schema defined in docs/data/schemas/output.json.
    """

    ticket_id: str
    category: TicketCategory
    priority: Priority
    assigned_team: AssignedTeam
    needs_escalation: bool
    missing_information: list[MissingInformation]
    next_best_action: str
    remediation_steps: list[str]
