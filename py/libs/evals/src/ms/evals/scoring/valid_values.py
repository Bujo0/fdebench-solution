# Copyright (c) Microsoft. All rights reserved.
"""Valid values for triage output fields.

Single source of truth for the constrained vocabulary used
in scoring and validation, matching the platform's label sets.
"""

VALID_CATEGORIES = frozenset({
    "Access & Authentication",
    "Hardware & Peripherals",
    "Network & Connectivity",
    "Software & Applications",
    "Security & Compliance",
    "Data & Storage",
    "General Inquiry",
    "Not a Support Ticket",
})

VALID_PRIORITIES = frozenset({"P1", "P2", "P3", "P4"})

VALID_TEAMS = frozenset({
    "Identity & Access Management",
    "Endpoint Engineering",
    "Network Operations",
    "Enterprise Applications",
    "Security Operations",
    "Data Platform",
    "None",
})

VALID_MISSING_INFO = frozenset({
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
})
