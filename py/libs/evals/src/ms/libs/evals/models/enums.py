"""Enumeration types for ticket triage classification."""

from enum import StrEnum


class TicketCategory(StrEnum):
    """The 8 closed-set ticket categories."""

    ACCESS_AUTH = "Access & Authentication"
    HARDWARE = "Hardware & Peripherals"
    NETWORK = "Network & Connectivity"
    SOFTWARE = "Software & Applications"
    SECURITY = "Security & Compliance"
    DATA_STORAGE = "Data & Storage"
    GENERAL_INQUIRY = "General Inquiry"
    NOT_A_TICKET = "Not a Support Ticket"


class Priority(StrEnum):
    """Ticket priority levels (P1 = Critical, P4 = Low)."""

    P1 = "P1"
    P2 = "P2"
    P3 = "P3"
    P4 = "P4"


class AssignedTeam(StrEnum):
    """The 7 closed-set specialist teams."""

    IDENTITY_ACCESS = "Identity & Access Management"
    ENDPOINT_ENG = "Endpoint Engineering"
    NETWORK_OPS = "Network Operations"
    ENTERPRISE_APPS = "Enterprise Applications"
    SECURITY_OPS = "Security Operations"
    DATA_PLATFORM = "Data Platform"
    NONE = "None"


class MissingInfoField(StrEnum):
    """The 16-value constrained vocabulary for missing information."""

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


class TicketChannel(StrEnum):
    """How the ticket was submitted."""

    EMAIL = "email"
    CHAT = "chat"
    PORTAL = "portal"
    PHONE = "phone"


class ScenarioTag(StrEnum):
    """Tags for categorizing evaluation scenarios."""

    DATA_CLEANUP = "data_cleanup"
    RESPONSIBLE_AI = "responsible_ai"
