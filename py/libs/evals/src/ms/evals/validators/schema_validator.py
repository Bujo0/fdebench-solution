# Copyright (c) Microsoft. All rights reserved.
"""Schema validation for triage API responses.

Validates that a raw API response dictionary conforms to the output
schema: correct field presence, valid enum values, correct types.
Designed to catch common mistakes before scoring.
"""

from ms.evals.constants import CATEGORIES
from ms.evals.constants import MISSING_INFO_VOCABULARY
from ms.evals.constants import PRIORITIES
from ms.evals.constants import TEAMS

_CATEGORIES_LOWER = frozenset(c.lower() for c in CATEGORIES)
_TEAMS_LOWER = frozenset(t.lower() for t in TEAMS)
_PRIORITIES_UPPER = frozenset(PRIORITIES)
_MISSING_INFO_LOWER = frozenset(v.lower() for v in MISSING_INFO_VOCABULARY)

_REQUIRED_FIELDS = (
    "ticket_id",
    "category",
    "priority",
    "assigned_team",
    "needs_escalation",
    "missing_information",
    "next_best_action",
    "remediation_steps",
)


class SchemaViolation:
    """A single schema validation failure."""

    def __init__(self, field: str, message: str) -> None:
        self.field = field
        self.message = message

    def __repr__(self) -> str:
        return f"SchemaViolation(field={self.field!r}, message={self.message!r})"

    def __str__(self) -> str:
        return f"{self.field}: {self.message}"


def validate_triage_response(response: dict[str, object]) -> list[SchemaViolation]:
    """Validate a triage response dictionary against the output schema.

    Returns a list of violations. Empty list means the response is valid.
    """
    violations: list[SchemaViolation] = []

    # Check required fields
    for field in _REQUIRED_FIELDS:
        if field not in response:
            violations.append(SchemaViolation(field, f"required field '{field}' is missing"))

    # Validate category
    category = response.get("category")
    if isinstance(category, str):
        if category.strip().lower() not in _CATEGORIES_LOWER:
            violations.append(
                SchemaViolation("category", f"invalid category: {category!r}. Must be one of {CATEGORIES}")
            )
    elif category is not None:
        violations.append(SchemaViolation("category", f"expected string, got {type(category).__name__}"))

    # Validate priority
    priority = response.get("priority")
    if isinstance(priority, str):
        if priority.strip().upper() not in _PRIORITIES_UPPER:
            violations.append(
                SchemaViolation("priority", f"invalid priority: {priority!r}. Must be one of {PRIORITIES}")
            )
    elif priority is not None:
        violations.append(SchemaViolation("priority", f"expected string, got {type(priority).__name__}"))

    # Validate assigned_team
    team = response.get("assigned_team")
    if isinstance(team, str):
        if team.strip().lower() not in _TEAMS_LOWER:
            violations.append(SchemaViolation("assigned_team", f"invalid team: {team!r}. Must be one of {TEAMS}"))
    elif team is not None:
        violations.append(SchemaViolation("assigned_team", f"expected string, got {type(team).__name__}"))

    # Validate needs_escalation
    escalation = response.get("needs_escalation")
    if (
        escalation is not None
        and not isinstance(escalation, bool)
        and (not isinstance(escalation, str) or escalation.strip().lower() not in {"true", "false", "1", "0"})
    ):
        violations.append(
            SchemaViolation(
                "needs_escalation",
                f"expected boolean, got {type(escalation).__name__}: {escalation!r}",
            )
        )

    # Validate missing_information
    missing_info = response.get("missing_information")
    if missing_info is not None:
        if not isinstance(missing_info, list):
            violations.append(
                SchemaViolation(
                    "missing_information",
                    f"expected list, got {type(missing_info).__name__}",
                )
            )
        else:
            for item in missing_info:
                if not isinstance(item, str):
                    violations.append(
                        SchemaViolation("missing_information", f"list item must be string, got {type(item).__name__}")
                    )
                elif item.lower() not in _MISSING_INFO_LOWER:
                    violations.append(
                        SchemaViolation(
                            "missing_information",
                            f"invalid vocab item: {item!r}. Must be from the 16-value vocabulary.",
                        )
                    )

    # Validate next_best_action
    nba = response.get("next_best_action")
    if nba is not None:
        if not isinstance(nba, str):
            violations.append(SchemaViolation("next_best_action", f"expected string, got {type(nba).__name__}"))
        elif len(nba.strip()) == 0:
            violations.append(SchemaViolation("next_best_action", "must not be empty"))

    # Validate remediation_steps
    steps = response.get("remediation_steps")
    if steps is not None:
        if not isinstance(steps, list):
            violations.append(SchemaViolation("remediation_steps", f"expected list, got {type(steps).__name__}"))
        else:
            if len(steps) == 0:
                violations.append(SchemaViolation("remediation_steps", "must contain at least one step"))
            for idx, step in enumerate(steps):
                if not isinstance(step, str):
                    violations.append(
                        SchemaViolation("remediation_steps", f"step [{idx}] must be string, got {type(step).__name__}")
                    )

    return violations
