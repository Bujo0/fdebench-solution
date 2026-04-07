# Copyright (c) Microsoft. All rights reserved.
<<<<<<< HEAD
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
=======
"""Schema validator for triage API responses.

Validates that a triage response has all required fields with correct types
and values within the allowed enums. This catches structural errors that
go beyond the scoring harness's tolerance (e.g., missing fields, wrong types,
invalid enum values).
"""

from ms.evals_core.constants import Category
from ms.evals_core.constants import MissingInfo as MissingInformation
from ms.evals_core.constants import Priority
from ms.evals_core.constants import Team as AssignedTeam

_VALID_CATEGORIES = frozenset(c.value for c in Category)
_VALID_PRIORITIES = frozenset(p.value for p in Priority)
_VALID_TEAMS = frozenset(t.value for t in AssignedTeam)
_VALID_MISSING_INFO = frozenset(m.value for m in MissingInformation)
>>>>>>> users/fde-platform-agent/fde-hiring-test-3/boyevche

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
<<<<<<< HEAD
    """A single schema validation failure."""
=======
    """A single schema validation error."""

    __slots__ = ("field", "message")
>>>>>>> users/fde-platform-agent/fde-hiring-test-3/boyevche

    def __init__(self, field: str, message: str) -> None:
        self.field = field
        self.message = message

    def __repr__(self) -> str:
        return f"SchemaViolation(field={self.field!r}, message={self.message!r})"

<<<<<<< HEAD
    def __str__(self) -> str:
        return f"{self.field}: {self.message}"


def validate_triage_response(response: dict[str, object]) -> list[SchemaViolation]:
    """Validate a triage response dictionary against the output schema.

    Returns a list of violations. Empty list means the response is valid.
=======
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, SchemaViolation):
            return NotImplemented
        return self.field == other.field and self.message == other.message


def validate_response_schema(response: dict[str, object]) -> list[SchemaViolation]:
    """Validate a triage response dict against the output schema.

    Returns a list of SchemaViolation objects. An empty list means
    the response is fully compliant.
>>>>>>> users/fde-platform-agent/fde-hiring-test-3/boyevche
    """
    violations: list[SchemaViolation] = []

    # Check required fields
    for field in _REQUIRED_FIELDS:
        if field not in response:
<<<<<<< HEAD
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
=======
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
>>>>>>> users/fde-platform-agent/fde-hiring-test-3/boyevche

    # Validate missing_information
    missing_info = response.get("missing_information")
    if missing_info is not None:
        if not isinstance(missing_info, list):
            violations.append(
<<<<<<< HEAD
                SchemaViolation(
                    "missing_information",
                    f"expected list, got {type(missing_info).__name__}",
                )
=======
                SchemaViolation("missing_information", f"Expected list, got {type(missing_info).__name__}")
>>>>>>> users/fde-platform-agent/fde-hiring-test-3/boyevche
            )
        else:
            for item in missing_info:
                if not isinstance(item, str):
                    violations.append(
<<<<<<< HEAD
                        SchemaViolation("missing_information", f"list item must be string, got {type(item).__name__}")
                    )
                elif item.lower() not in _MISSING_INFO_LOWER:
                    violations.append(
                        SchemaViolation(
                            "missing_information",
                            f"invalid vocab item: {item!r}. Must be from the 16-value vocabulary.",
                        )
=======
                        SchemaViolation("missing_information", f"List item must be string, got {type(item).__name__}")
                    )
                elif item not in _VALID_MISSING_INFO:
                    violations.append(
                        SchemaViolation("missing_information", f"Invalid missing_information value: {item!r}")
>>>>>>> users/fde-platform-agent/fde-hiring-test-3/boyevche
                    )

    # Validate next_best_action
    nba = response.get("next_best_action")
    if nba is not None:
        if not isinstance(nba, str):
<<<<<<< HEAD
            violations.append(SchemaViolation("next_best_action", f"expected string, got {type(nba).__name__}"))
        elif len(nba.strip()) == 0:
            violations.append(SchemaViolation("next_best_action", "must not be empty"))
=======
            violations.append(SchemaViolation("next_best_action", f"Expected string, got {type(nba).__name__}"))
        elif len(nba.strip()) == 0:
            violations.append(SchemaViolation("next_best_action", "Must not be empty"))
>>>>>>> users/fde-platform-agent/fde-hiring-test-3/boyevche

    # Validate remediation_steps
    steps = response.get("remediation_steps")
    if steps is not None:
        if not isinstance(steps, list):
<<<<<<< HEAD
            violations.append(SchemaViolation("remediation_steps", f"expected list, got {type(steps).__name__}"))
        else:
            if len(steps) == 0:
                violations.append(SchemaViolation("remediation_steps", "must contain at least one step"))
            for idx, step in enumerate(steps):
                if not isinstance(step, str):
                    violations.append(
                        SchemaViolation("remediation_steps", f"step [{idx}] must be string, got {type(step).__name__}")
=======
            violations.append(SchemaViolation("remediation_steps", f"Expected list, got {type(steps).__name__}"))
        else:
            for step in steps:
                if not isinstance(step, str):
                    violations.append(
                        SchemaViolation("remediation_steps", f"List item must be string, got {type(step).__name__}")
>>>>>>> users/fde-platform-agent/fde-hiring-test-3/boyevche
                    )

    return violations
