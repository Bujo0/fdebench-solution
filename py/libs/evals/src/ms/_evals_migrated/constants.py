# Copyright (c) Microsoft. All rights reserved.
"""Shared constants from the hackathon challenge specification.

These values must match the platform's closed label sets exactly.
Source of truth: docs/data/schemas/output.json and docs/challenge/README.md.
"""

from enum import StrEnum


class Category(StrEnum):
    """Valid ticket categories (8 values)."""

    ACCESS_AUTH = "Access & Authentication"
    HARDWARE = "Hardware & Peripherals"
    NETWORK = "Network & Connectivity"
    SOFTWARE = "Software & Applications"
    SECURITY = "Security & Compliance"
    DATA_STORAGE = "Data & Storage"
    GENERAL_INQUIRY = "General Inquiry"
    NOT_SUPPORT = "Not a Support Ticket"


class Priority(StrEnum):
    """Valid priority levels."""

    P1 = "P1"
    P2 = "P2"
    P3 = "P3"
    P4 = "P4"


class Team(StrEnum):
    """Valid assigned team values (7 values including 'None')."""

    IAM = "Identity & Access Management"
    ENDPOINT = "Endpoint Engineering"
    NETWORK_OPS = "Network Operations"
    ENTERPRISE_APPS = "Enterprise Applications"
    SECURITY_OPS = "Security Operations"
    DATA_PLATFORM = "Data Platform"
    NONE = "None"


class MissingInfoField(StrEnum):
    """Constrained vocabulary for missing_information (16 values)."""

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
    """Valid submission channels."""

    EMAIL = "email"
    CHAT = "chat"
    PORTAL = "portal"
    PHONE = "phone"
