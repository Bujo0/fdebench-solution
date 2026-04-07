# Copyright (c) Microsoft. All rights reserved.
"""Pydantic models for triage response output.

Mirrors the output schema at docs/data/schemas/output.json.
"""

from typing import Literal

from ms.common.models.base import FrozenBaseModel
from ms.evals_core.constants import MissingInfo

MissingInfoLiteral = Literal[
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

MISSING_INFO_VALUES: frozenset[str] = frozenset(m.value for m in MissingInfo)


class TriageResponse(FrozenBaseModel):
    """Expected triage output for a single ticket.

    All classification fields use constrained values matching
    the challenge specification.
    """

    ticket_id: str
    category: Literal[
        "Access & Authentication",
        "Hardware & Peripherals",
        "Network & Connectivity",
        "Software & Applications",
        "Security & Compliance",
        "Data & Storage",
        "General Inquiry",
        "Not a Support Ticket",
    ]
    priority: Literal["P1", "P2", "P3", "P4"]
    assigned_team: Literal[
        "Identity & Access Management",
        "Endpoint Engineering",
        "Network Operations",
        "Enterprise Applications",
        "Security Operations",
        "Data Platform",
        "None",
    ]
    needs_escalation: bool
    missing_information: list[MissingInfoLiteral] = []
    next_best_action: str
    remediation_steps: list[str]
