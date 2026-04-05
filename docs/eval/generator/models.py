"""Data models for eval ticket generation."""

from dataclasses import dataclass
from dataclasses import field

# ── Constrained vocabulary ──────────────────────────────────────────────────

CATEGORIES = [
    "Access & Authentication",
    "Hardware & Peripherals",
    "Network & Connectivity",
    "Software & Applications",
    "Security & Compliance",
    "Data & Storage",
    "General Inquiry",
    "Not a Support Ticket",
]

TEAMS = [
    "Identity & Access Management",
    "Endpoint Engineering",
    "Network Operations",
    "Enterprise Applications",
    "Security Operations",
    "Data Platform",
]

PRIORITIES = ["P1", "P2", "P3", "P4"]

CHANNELS = ["email", "chat", "portal", "phone"]

MISSING_INFO_VOCABULARY = [
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


# ── Scenario definition ─────────────────────────────────────────────────────


@dataclass
class Scenario:
    """A unique IT support scenario with triage gold answer."""

    scenario_id: str
    category: str
    priority: str
    assigned_team: str
    needs_escalation: bool
    missing_information: list[str]
    subjects: list[str]
    descriptions: list[str]
    next_best_actions: list[str]
    remediation_steps: list[list[str]]
    tags: list[str] = field(default_factory=list)
    channel_weights: dict[str, float] = field(
        default_factory=lambda: {
            "email": 0.30,
            "chat": 0.25,
            "portal": 0.25,
            "phone": 0.20,
        }
    )


@dataclass
class GeneratedTicket:
    """A generated ticket ready for JSON serialization."""

    ticket_id: str
    subject: str
    description: str
    reporter_name: str
    reporter_email: str
    reporter_department: str
    created_at: str
    channel: str
    attachments: list[str]


@dataclass
class GoldAnswer:
    """Gold-standard triage answer for a generated ticket."""

    ticket_id: str
    category: str
    priority: str
    assigned_team: str
    needs_escalation: bool
    missing_information: list[str]
    next_best_action: str
    remediation_steps: list[str]
