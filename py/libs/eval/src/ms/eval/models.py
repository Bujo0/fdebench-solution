# Copyright (c) Microsoft. All rights reserved.
"""Pydantic models for ticket input and triage output schemas.

These models mirror the JSON schemas defined in docs/data/schemas/input.json
and docs/data/schemas/output.json. They are used to validate evaluation
scenario data and ensure compatibility with the run_eval.py harness.
"""

from typing import Literal

from ms.common.models.base import FrozenBaseModel


class Reporter(FrozenBaseModel):
    """Reporter information for a support ticket."""

    name: str
    email: str
    department: str


class TicketInput(FrozenBaseModel):
    """An IT support ticket submitted to Contoso Financial Services.

    Matches the input schema in docs/data/schemas/input.json.
    """

    ticket_id: str
    subject: str
    description: str
    reporter: Reporter
    created_at: str
    channel: Literal["email", "chat", "portal", "phone"]
    attachments: list[str] = []


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

Priority = Literal["P1", "P2", "P3", "P4"]

Team = Literal[
    "Identity & Access Management",
    "Endpoint Engineering",
    "Network Operations",
    "Enterprise Applications",
    "Security Operations",
    "Data Platform",
    "None",
]


class TriageDecision(FrozenBaseModel):
    """The expected triage output for a single ticket.

    Matches the output schema in docs/data/schemas/output.json.
    """

    ticket_id: str
    category: Category
    priority: Priority
    assigned_team: Team
    needs_escalation: bool
    missing_information: list[MissingInfoField]
    next_best_action: str
    remediation_steps: list[str]
