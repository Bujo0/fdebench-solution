# Copyright (c) Microsoft. All rights reserved.
"""Domain constants for IT ticket triage evaluation.

Defines the closed sets of valid values used in scoring and validation.
These match the platform's scoring harness exactly.
"""

from enum import StrEnum


class Category(StrEnum):
    """Valid ticket categories for classification."""

    ACCESS_AUTH = "Access & Authentication"
    HARDWARE = "Hardware & Peripherals"
    NETWORK = "Network & Connectivity"
    SOFTWARE = "Software & Applications"
    SECURITY = "Security & Compliance"
    DATA_STORAGE = "Data & Storage"
    GENERAL = "General Inquiry"
    NOT_SUPPORT = "Not a Support Ticket"


class Priority(StrEnum):
    """Priority levels from P1 (critical) to P4 (low)."""

    P1 = "P1"
    P2 = "P2"
    P3 = "P3"
    P4 = "P4"


class AssignedTeam(StrEnum):
    """Valid routing destinations."""

    IAM = "Identity & Access Management"
    ENDPOINT = "Endpoint Engineering"
    NETWORK_OPS = "Network Operations"
    ENTERPRISE_APPS = "Enterprise Applications"
    SECURITY_OPS = "Security Operations"
    DATA_PLATFORM = "Data Platform"
    NONE = "None"


class MissingInfoField(StrEnum):
    """Constrained vocabulary for missing information."""

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


class Channel(StrEnum):
    """How a ticket was submitted."""

    EMAIL = "email"
    CHAT = "chat"
    PORTAL = "portal"
    PHONE = "phone"


ALL_CATEGORIES: frozenset[str] = frozenset(c.value for c in Category)
ALL_PRIORITIES: frozenset[str] = frozenset(p.value for p in Priority)
ALL_TEAMS: frozenset[str] = frozenset(t.value for t in AssignedTeam)
ALL_MISSING_INFO_FIELDS: frozenset[str] = frozenset(f.value for f in MissingInfoField)
ALL_CHANNELS: frozenset[str] = frozenset(c.value for c in Channel)
