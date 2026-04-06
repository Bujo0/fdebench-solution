# Copyright (c) Microsoft. All rights reserved.
"""Schema validator for triage API responses.

Validates that a triage response has all required fields with correct types
and values within the allowed enums. This catches structural errors that
go beyond the scoring harness's tolerance (e.g., missing fields, wrong types,
invalid enum values).
"""

from ms.evals.models import AssignedTeam
from ms.evals.models import Category
from ms.evals.models import MissingInformation
from ms.evals.models import Priority

_VALID_CATEGORIES = frozenset(c.value for c in Category)
_VALID_PRIORITIES = frozenset(p.value for p in Priority)
_VALID_TEAMS = frozenset(t.value for t in AssignedTeam)
_VALID_MISSING_INFO = frozenset(m.value for m in MissingInformation)

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
    """A single schema validation error."""

    __slots__ = ("field", "message")

    def __init__(self, field: str, message: str) -> None:
        self.field = field
        self.message = message

    def __repr__(self) -> str:
        return f"SchemaViolation(field={self.field!r}, message={self.message!r})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, SchemaViolation):
            return NotImplemented
        return self.field == other.field and self.message == other.message


def validate_response_schema(response: dict[str, object]) -> list[SchemaViolation]:
    """Validate a triage response dict against the output schema.

    Returns a list of SchemaViolation objects. An empty list means
    the response is fully compliant.
    """
    violations: list[SchemaViolation] = []

    # Check required fields
    for field in _REQUIRED_FIELDS:
        if field not in response:
            violations.append(SchemaViolation(field, f"Required field '{field}' is missing"))

    # Early return if too many missing fields to validate further
    if len(violations) > 3:
        return violations

    # Validate ticket_id
    ticket_id = response.get("ticket_id")
    if ticket_id is not None and not isinstance(ticket_id, str):
        violations.append(SchemaViolation("ticket_id", f"Expected string, got {type(ticket_id).__name__}"))

    # Validate category
    category = response.get("category")
    if category is not None:
        if not isinstance(category, str):
            violations.append(SchemaViolation("category", f"Expected string, got {type(category).__name__}"))
        elif category not in _VALID_CATEGORIES:
            violations.append(SchemaViolation("category", f"Invalid category: {category!r}"))

    # Validate priority
    priority = response.get("priority")
    if priority is not None:
        if not isinstance(priority, str):
            violations.append(SchemaViolation("priority", f"Expected string, got {type(priority).__name__}"))
        elif priority not in _VALID_PRIORITIES:
            violations.append(SchemaViolation("priority", f"Invalid priority: {priority!r}"))

    # Validate assigned_team
    team = response.get("assigned_team")
    if team is not None:
        if not isinstance(team, str):
            violations.append(SchemaViolation("assigned_team", f"Expected string, got {type(team).__name__}"))
        elif team not in _VALID_TEAMS:
            violations.append(SchemaViolation("assigned_team", f"Invalid team: {team!r}"))

    # Validate needs_escalation
    escalation = response.get("needs_escalation")
    if escalation is not None and not isinstance(escalation, bool):
        # Allow string booleans and ints for tolerance
        if isinstance(escalation, str) and escalation.strip().lower() not in {"true", "false", "1", "0", "yes", "no"}:
            violations.append(
                SchemaViolation("needs_escalation", f"Expected boolean or boolean-like, got {escalation!r}")
            )
        elif not isinstance(escalation, (str, int)):
            violations.append(SchemaViolation("needs_escalation", f"Expected boolean, got {type(escalation).__name__}"))

    # Validate missing_information
    missing_info = response.get("missing_information")
    if missing_info is not None:
        if not isinstance(missing_info, list):
            violations.append(
                SchemaViolation("missing_information", f"Expected list, got {type(missing_info).__name__}")
            )
        else:
            for item in missing_info:
                if not isinstance(item, str):
                    violations.append(
                        SchemaViolation("missing_information", f"List item must be string, got {type(item).__name__}")
                    )
                elif item not in _VALID_MISSING_INFO:
                    violations.append(
                        SchemaViolation("missing_information", f"Invalid missing_information value: {item!r}")
                    )

    # Validate next_best_action
    nba = response.get("next_best_action")
    if nba is not None:
        if not isinstance(nba, str):
            violations.append(SchemaViolation("next_best_action", f"Expected string, got {type(nba).__name__}"))
        elif len(nba.strip()) == 0:
            violations.append(SchemaViolation("next_best_action", "Must not be empty"))

    # Validate remediation_steps
    steps = response.get("remediation_steps")
    if steps is not None:
        if not isinstance(steps, list):
            violations.append(SchemaViolation("remediation_steps", f"Expected list, got {type(steps).__name__}"))
        else:
            for step in steps:
                if not isinstance(step, str):
                    violations.append(
                        SchemaViolation("remediation_steps", f"List item must be string, got {type(step).__name__}")
                    )

    return violations
