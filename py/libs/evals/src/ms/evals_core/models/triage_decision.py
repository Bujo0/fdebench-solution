# Copyright (c) Microsoft. All rights reserved.
"""Triage decision model matching docs/data/schemas/output.json."""

from typing import Literal

from ms.common.models.base import FrozenBaseModel

Category = Literal[
    "Access & Authentication",
    "Hardware & Peripherals",
    "Network & Connectivity",
    "Software & Applications",
    "Security & Compliance",
    "Data & Storage",
    "General Inquiry",
    "Not a Support Ticket",
]

Team = Literal[
    "Identity & Access Management",
    "Endpoint Engineering",
    "Network Operations",
    "Enterprise Applications",
    "Security Operations",
    "Data Platform",
    "None",
]

Priority = Literal["P1", "P2", "P3", "P4"]

MissingInfoField = Literal[
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
]


class TriageDecision(FrozenBaseModel):
    """Expected triage output for a single ticket.

    Matches the JSON schema at docs/data/schemas/output.json.
    """

    ticket_id: str
    category: Category
    priority: Priority
    assigned_team: Team
    needs_escalation: bool
    missing_information: list[MissingInfoField]
    next_best_action: str
    remediation_steps: list[str]
