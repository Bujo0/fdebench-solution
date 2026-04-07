# Copyright (c) Microsoft. All rights reserved.
"""Constants for the evals dataset generator.

Defines all valid enum values for ticket triage categories, priorities,
teams, channels, departments, and missing information types.
"""

from enum import StrEnum


class Category(StrEnum):
    """Ticket issue categories."""

    ACCESS_AUTH = "Access & Authentication"
    HARDWARE = "Hardware & Peripherals"
    NETWORK = "Network & Connectivity"
    SOFTWARE = "Software & Applications"
    SECURITY = "Security & Compliance"
    DATA = "Data & Storage"
    GENERAL = "General Inquiry"
    NOT_SUPPORT = "Not a Support Ticket"


class Priority(StrEnum):
    """Ticket priority levels."""

    P1 = "P1"
    P2 = "P2"
    P3 = "P3"
    P4 = "P4"


class Team(StrEnum):
    """Specialist IT teams for routing."""

    IAM = "Identity & Access Management"
    ENDPOINT = "Endpoint Engineering"
    NETWORK = "Network Operations"
    ENTERPRISE_APPS = "Enterprise Applications"
    SECOPS = "Security Operations"
    DATA_PLATFORM = "Data Platform"
    NONE = "None"


class Channel(StrEnum):
    """Ticket submission channels."""

    EMAIL = "email"
    CHAT = "chat"
    PORTAL = "portal"
    PHONE = "phone"


class MissingInfo(StrEnum):
    """Valid missing information types (constrained vocabulary)."""

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


# Target distribution weights for balanced generation
CATEGORY_WEIGHTS: dict[Category, float] = {
    Category.ACCESS_AUTH: 0.14,
    Category.HARDWARE: 0.12,
    Category.NETWORK: 0.13,
    Category.SOFTWARE: 0.17,
    Category.SECURITY: 0.13,
    Category.DATA: 0.11,
    Category.GENERAL: 0.10,
    Category.NOT_SUPPORT: 0.10,
}

PRIORITY_WEIGHTS: dict[Priority, float] = {
    Priority.P1: 0.12,
    Priority.P2: 0.25,
    Priority.P3: 0.38,
    Priority.P4: 0.25,
}

CHANNEL_WEIGHTS: dict[Channel, float] = {
    Channel.EMAIL: 0.30,
    Channel.PORTAL: 0.30,
    Channel.CHAT: 0.25,
    Channel.PHONE: 0.15,
}

ESCALATION_RATE = 0.25
