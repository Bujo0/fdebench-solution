"""Triage business logic — category matching and post-processing."""

import logging
from typing import Literal

from models import Category
from models import MissingInfo
from models import Team

from ms.common.models.base import FrozenBaseModel

logger = logging.getLogger(__name__)


class TriageLLMResponse(FrozenBaseModel):
    """Structured-output model for triage LLM responses.

    Uses Literal types so OpenAI structured output ENFORCES valid values.
    Without this, the model can return variations like 'Hull Systems' which
    fail match_category() and silently fall back to BRIEFING.
    """

    category: Literal[
        "Crew Access & Biometrics",
        "Hull & Structural Systems",
        "Communications & Navigation",
        "Flight Software & Instruments",
        "Threat Detection & Containment",
        "Telemetry & Data Banks",
        "Mission Briefing Request",
        "Not a Mission Signal",
    ]
    priority: Literal["P1", "P2", "P3", "P4"]
    assigned_team: Literal[
        "Crew Identity & Airlock Control",
        "Spacecraft Systems Engineering",
        "Deep Space Communications",
        "Mission Software Operations",
        "Threat Response Command",
        "Telemetry & Data Core",
        "None",
    ]
    needs_escalation: bool
    missing_information: list[Literal[
        "affected_subsystem", "anomaly_readout", "sequence_to_reproduce",
        "affected_crew", "habitat_conditions", "stardate", "previous_signal_id",
        "crew_contact", "module_specs", "software_version", "sector_coordinates",
        "mission_impact", "recurrence_pattern", "sensor_log_or_capture",
        "biometric_method", "system_configuration",
    ]]
    next_best_action: str | None = None
    remediation_steps: list[str] | None = None


def match_category(value: str) -> Category:
    """Match a string value to the closest Category enum member."""
    v = value.strip()
    for c in Category:
        if c.value.lower() == v.lower():
            return c
    return Category.BRIEFING


def match_team(value: str) -> Team:
    """Match a string value to the closest Team enum member."""
    v = value.strip()
    for t in Team:
        if t.value.lower() == v.lower():
            return t
    return Team.NONE


CATEGORY_TEAM_DEFAULT = {
    "Crew Access & Biometrics": "Crew Identity & Airlock Control",
    "Hull & Structural Systems": "Spacecraft Systems Engineering",
    "Communications & Navigation": "Deep Space Communications",
    "Flight Software & Instruments": "Mission Software Operations",
    "Threat Detection & Containment": "Threat Response Command",
    "Telemetry & Data Banks": "Telemetry & Data Core",
    "Mission Briefing Request": "None",
    "Not a Mission Signal": "None",
}

CATEGORY_VALID_TEAMS = {
    "Crew Access & Biometrics": {"Crew Identity & Airlock Control", "Spacecraft Systems Engineering"},
    "Hull & Structural Systems": {"Spacecraft Systems Engineering", "Deep Space Communications"},
    "Communications & Navigation": {"Deep Space Communications"},
    "Flight Software & Instruments": {"Mission Software Operations", "Spacecraft Systems Engineering"},
    "Threat Detection & Containment": {"Threat Response Command"},
    "Telemetry & Data Banks": {"Telemetry & Data Core"},
    "Mission Briefing Request": {
        "None",
        "Spacecraft Systems Engineering",
        "Crew Identity & Airlock Control",
        "Mission Software Operations",
    },
    "Not a Mission Signal": {"None"},
}


def validate_category_team(category: str, team: str) -> str:
    """Validate and correct category→team mapping."""
    valid_teams = CATEGORY_VALID_TEAMS.get(category)
    if valid_teams and team not in valid_teams:
        return CATEGORY_TEAM_DEFAULT.get(category, team)
    return team


def match_missing_info(items: list[str]) -> list[MissingInfo]:
    """Filter and convert raw strings to valid MissingInfo enum values."""
    result = []
    valid = {m.value for m in MissingInfo}
    for item in items:
        v = item.strip().lower()
        if v in valid:
            result.append(MissingInfo(v))
    return result
