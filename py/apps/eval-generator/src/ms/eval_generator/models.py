# Copyright (c) Microsoft. All rights reserved.
"""Pydantic models for eval ticket generation — matching docs/data/schemas/*.json."""

from ms.common.models.base import FrozenBaseModel


class Reporter(FrozenBaseModel):
    """Reporter info attached to a support ticket."""

    name: str
    email: str
    department: str


class Ticket(FrozenBaseModel):
    """An IT support ticket submitted to Contoso Financial Services."""

    ticket_id: str
    subject: str
    description: str
    reporter: Reporter
    created_at: str
    channel: str
    attachments: list[str] = []


class TriageGold(FrozenBaseModel):
    """Gold-standard triage decision for a ticket."""

    ticket_id: str
    category: str
    priority: str
    assigned_team: str
    needs_escalation: bool
    missing_information: list[str]
    next_best_action: str
    remediation_steps: list[str]


# ── Valid enum values (from schemas) ──────────────────────────────────────────

VALID_CATEGORIES = frozenset(
    {
        "Access & Authentication",
        "Hardware & Peripherals",
        "Network & Connectivity",
        "Software & Applications",
        "Security & Compliance",
        "Data & Storage",
        "General Inquiry",
        "Not a Support Ticket",
    }
)

VALID_PRIORITIES = frozenset({"P1", "P2", "P3", "P4"})

VALID_TEAMS = frozenset(
    {
        "Identity & Access Management",
        "Endpoint Engineering",
        "Network Operations",
        "Enterprise Applications",
        "Security Operations",
        "Data Platform",
        "None",
    }
)

VALID_CHANNELS = frozenset({"email", "chat", "portal", "phone"})

VALID_MISSING_INFO = frozenset(
    {
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
    }
)

VALID_DEPARTMENTS = [
    "Engineering",
    "Wealth Management",
    "Trading",
    "Compliance",
    "HR",
    "IT",
    "Finance",
    "Legal",
    "Operations",
    "Investor Relations",
    "Risk Management",
    "Marketing",
    "Executive Office",
    "Research",
    "Client Services",
    "Internal Audit",
]
