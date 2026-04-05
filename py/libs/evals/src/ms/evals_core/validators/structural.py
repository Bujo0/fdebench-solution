# Copyright (c) Microsoft. All rights reserved.
"""Structural validation for triage API responses.

Verifies that a triage response conforms to the output schema:
all required fields present, enum values valid, types correct.
"""

from ms.evals_core.constants import Category
from ms.evals_core.constants import MissingInfoField
from ms.evals_core.constants import Priority
from ms.evals_core.constants import Team

_VALID_CATEGORIES = {c.value.strip().lower() for c in Category}
_VALID_PRIORITIES = {p.value.strip().lower() for p in Priority}
_VALID_TEAMS = {t.value.strip().lower() for t in Team}
_VALID_MISSING_INFO = {m.value.strip().lower() for m in MissingInfoField}

_REQUIRED_FIELDS = frozenset(
    {
        "ticket_id",
        "category",
        "priority",
        "assigned_team",
        "needs_escalation",
        "missing_information",
        "next_best_action",
        "remediation_steps",
    }
)


class StructuralViolation(Exception):
    """Raised when a triage response has a structural problem."""

    def __init__(self, ticket_id: str, field: str, message: str) -> None:
        self.ticket_id = ticket_id
        self.field = field
        super().__init__(f"{ticket_id} [{field}]: {message}")


def validate_response_structure(
    response: dict[str, object],
) -> list[StructuralViolation]:
    """Validate that a triage response has all required fields with valid values.

    Returns a list of violations (empty means the response is structurally valid).
    Does not check correctness — only schema conformance.
    """
    violations: list[StructuralViolation] = []
    ticket_id = str(response.get("ticket_id", "<missing>"))

    missing_fields = _REQUIRED_FIELDS - set(response.keys())
    for field in sorted(missing_fields):
        violations.append(
            StructuralViolation(ticket_id, field, "required field is missing")
        )

    if missing_fields:
        return violations

    category = response.get("category")
    if (
        not isinstance(category, str)
        or category.strip().lower() not in _VALID_CATEGORIES
    ):
        violations.append(
            StructuralViolation(
                ticket_id,
                "category",
                f"invalid value: {category!r}",
            )
        )

    priority = response.get("priority")
    if (
        not isinstance(priority, str)
        or priority.strip().lower() not in _VALID_PRIORITIES
    ):
        violations.append(
            StructuralViolation(
                ticket_id,
                "priority",
                f"invalid value: {priority!r}",
            )
        )

    assigned_team = response.get("assigned_team")
    if (
        not isinstance(assigned_team, str)
        or assigned_team.strip().lower() not in _VALID_TEAMS
    ):
        violations.append(
            StructuralViolation(
                ticket_id,
                "assigned_team",
                f"invalid value: {assigned_team!r}",
            )
        )

    needs_escalation = response.get("needs_escalation")
    if not isinstance(needs_escalation, (bool, str, int)):
        violations.append(
            StructuralViolation(
                ticket_id,
                "needs_escalation",
                f"expected boolean, got {type(needs_escalation).__name__}",
            )
        )

    missing_info = response.get("missing_information")
    if not isinstance(missing_info, list):
        violations.append(
            StructuralViolation(
                ticket_id,
                "missing_information",
                f"expected list, got {type(missing_info).__name__}",
            )
        )
    else:
        for item in missing_info:
            if not isinstance(item, str):
                violations.append(
                    StructuralViolation(
                        ticket_id,
                        "missing_information",
                        f"list item must be string, got {type(item).__name__}",
                    )
                )
            elif item.strip().lower() not in _VALID_MISSING_INFO:
                violations.append(
                    StructuralViolation(
                        ticket_id,
                        "missing_information",
                        f"invalid vocabulary item: {item!r}",
                    )
                )

    next_action = response.get("next_best_action")
    if not isinstance(next_action, str):
        violations.append(
            StructuralViolation(
                ticket_id,
                "next_best_action",
                f"expected string, got {type(next_action).__name__}",
            )
        )
    elif len(next_action.strip()) == 0:
        violations.append(
            StructuralViolation(ticket_id, "next_best_action", "must not be empty")
        )

    remediation = response.get("remediation_steps")
    if not isinstance(remediation, list):
        violations.append(
            StructuralViolation(
                ticket_id,
                "remediation_steps",
                f"expected list, got {type(remediation).__name__}",
            )
        )
    elif len(remediation) == 0:
        violations.append(
            StructuralViolation(ticket_id, "remediation_steps", "must not be empty")
        )
    else:
        for step in remediation:
            if not isinstance(step, str):
                violations.append(
                    StructuralViolation(
                        ticket_id,
                        "remediation_steps",
                        f"list item must be string, got {type(step).__name__}",
                    )
                )

    return violations
