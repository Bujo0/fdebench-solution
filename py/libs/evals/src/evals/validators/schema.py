# Copyright (c) Microsoft. All rights reserved.
"""Schema validation for triage responses.

Validates that triage responses conform to the output schema and use
only valid enum values. This catches structural issues before scoring.
"""

from evals.models import Category
from evals.models import MissingInfoField
from evals.models import Priority
from evals.models import Team
from evals.models import TriageDecision

_VALID_CATEGORIES = frozenset(c.value for c in Category)
_VALID_TEAMS = frozenset(t.value for t in Team)
_VALID_PRIORITIES = frozenset(p.value for p in Priority)
_VALID_MISSING_INFO = frozenset(f.value for f in MissingInfoField)


class SchemaViolation:
    """A single schema validation failure."""

    def __init__(self, field: str, message: str) -> None:
        self.field = field
        self.message = message

    def __repr__(self) -> str:
        return f"SchemaViolation(field={self.field!r}, message={self.message!r})"


def validate_triage_response(response: dict[str, object]) -> list[SchemaViolation]:
    """Validate a raw triage response dict against the output schema.

    Returns a list of SchemaViolation objects. Empty list means valid.
    """
    violations: list[SchemaViolation] = []

    required_fields = (
        "ticket_id",
        "category",
        "priority",
        "assigned_team",
        "needs_escalation",
        "missing_information",
        "next_best_action",
        "remediation_steps",
    )

    for field in required_fields:
        if field not in response:
            violations.append(SchemaViolation(field, f"Required field '{field}' is missing"))

    if "category" in response and response["category"] not in _VALID_CATEGORIES:
        violations.append(
            SchemaViolation(
                "category",
                f"Invalid category: {response['category']!r}. Must be one of {_VALID_CATEGORIES}",
            )
        )

    if "priority" in response and response["priority"] not in _VALID_PRIORITIES:
        violations.append(
            SchemaViolation(
                "priority", f"Invalid priority: {response['priority']!r}. Must be one of {_VALID_PRIORITIES}"
            )
        )

    if "assigned_team" in response and response["assigned_team"] not in _VALID_TEAMS:
        violations.append(
            SchemaViolation(
                "assigned_team", f"Invalid team: {response['assigned_team']!r}. Must be one of {_VALID_TEAMS}"
            )
        )

    if "needs_escalation" in response and not isinstance(response["needs_escalation"], bool):
        violations.append(
            SchemaViolation("needs_escalation", f"Must be boolean, got {type(response['needs_escalation']).__name__}")
        )

    if "missing_information" in response:
        mi = response["missing_information"]
        if not isinstance(mi, list):
            violations.append(SchemaViolation("missing_information", f"Must be a list, got {type(mi).__name__}"))
        else:
            for item in mi:
                if item not in _VALID_MISSING_INFO:
                    violations.append(
                        SchemaViolation("missing_information", f"Invalid value: {item!r}. Must be from vocabulary")
                    )

    if "remediation_steps" in response:
        rs = response["remediation_steps"]
        if not isinstance(rs, list):
            violations.append(SchemaViolation("remediation_steps", f"Must be a list, got {type(rs).__name__}"))

    return violations


def validate_triage_decision(decision: TriageDecision) -> list[SchemaViolation]:
    """Validate a typed TriageDecision model (should always pass for well-constructed models)."""
    return validate_triage_response(decision.model_dump())
