# Copyright (c) Microsoft. All rights reserved.
"""Canonical enum values and constants for evaluation.

All valid classification values match the challenge specification exactly.
Scoring uses exact string matching, so these must not be modified.
"""

CATEGORIES: tuple[str, ...] = (
    "Access & Authentication",
    "Hardware & Peripherals",
    "Network & Connectivity",
    "Software & Applications",
    "Security & Compliance",
    "Data & Storage",
    "General Inquiry",
    "Not a Support Ticket",
)

TEAMS: tuple[str, ...] = (
    "Identity & Access Management",
    "Endpoint Engineering",
    "Network Operations",
    "Enterprise Applications",
    "Security Operations",
    "Data Platform",
    "None",
)

PRIORITIES: tuple[str, ...] = ("P1", "P2", "P3", "P4")

MISSING_INFO_VOCABULARY: tuple[str, ...] = (
    "affected_system",
    "error_message",
    "steps_to_reproduce",
    "affected_users",
    "environment_details",
    "timestamp",
    "previous_ticket_id",
    "contact_info",
    "device_info",
    "application_version",
    "network_location",
    "business_impact",
    "reproduction_frequency",
    "screenshot_or_attachment",
    "authentication_method",
    "configuration_details",
)

CHANNELS: tuple[str, ...] = ("email", "chat", "portal", "phone")
