# Copyright (c) Microsoft. All rights reserved.
"""Schema validation for triage API responses.

Validates that raw API responses conform to the expected triage output schema
without requiring Pydantic deserialization (which may be too strict for
detecting specific failure modes).
"""

from ms.common.models.base import FrozenBaseModel
from ms.evals_core.constants import ALL_CATEGORIES
from ms.evals_core.constants import ALL_MISSING_INFO_FIELDS
from ms.evals_core.constants import ALL_PRIORITIES
from ms.evals_core.constants import ALL_TEAMS

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


class SchemaViolation(FrozenBaseModel):
    """A single schema validation issue."""

    field: str
    issue: str


class SchemaValidationResult(FrozenBaseModel):
    """Aggregated result of schema validation for one response."""

    ticket_id: str
    is_valid: bool
    violations: tuple[SchemaViolation, ...]


def validate_response_schema(response: dict[str, object], expected_ticket_id: str) -> SchemaValidationResult:
    """Validate a raw triage response dict against the output schema.

    Checks:
    - All 8 required fields are present
    - ticket_id matches the input
    - category is from the valid set
    - priority is from the valid set
    - assigned_team is from the valid set
    - needs_escalation is a boolean (or coercible)
    - missing_information is a list of valid vocabulary items
    - next_best_action is a non-empty string
    - remediation_steps is a non-empty list of strings
    """
    violations: list[SchemaViolation] = []

    # Check required fields
    for field in _REQUIRED_FIELDS:
        if field not in response:
            violations.append(SchemaViolation(field=field, issue="missing required field"))

    # ticket_id match
    resp_tid = response.get("ticket_id")
    if resp_tid is not None and str(resp_tid) != expected_ticket_id:
        violations.append(
            SchemaViolation(
                field="ticket_id",
                issue=f"expected '{expected_ticket_id}', got '{resp_tid}'",
            )
        )

    # category validation
    category = response.get("category")
    if category is not None and str(category).strip() not in ALL_CATEGORIES:
        violations.append(
            SchemaViolation(
                field="category",
                issue=f"invalid category: '{category}'",
            )
        )

    # priority validation
    priority = response.get("priority")
    if priority is not None and str(priority).strip().upper() not in {p.upper() for p in ALL_PRIORITIES}:
        violations.append(
            SchemaViolation(
                field="priority",
                issue=f"invalid priority: '{priority}'",
            )
        )

    # assigned_team validation
    team = response.get("assigned_team")
    if team is not None and str(team).strip() not in ALL_TEAMS:
        violations.append(
            SchemaViolation(
                field="assigned_team",
                issue=f"invalid team: '{team}'",
            )
        )

    # needs_escalation type check
    escalation = response.get("needs_escalation")
    if (
        escalation is not None
        and not isinstance(escalation, bool)
        and isinstance(escalation, str)
        and escalation.strip().lower() not in {"true", "false", "1", "0", "yes", "no"}
    ):
        violations.append(
            SchemaViolation(
                field="needs_escalation",
                issue=f"not a valid boolean value: '{escalation}'",
            )
        )

    # missing_information validation
    missing_info = response.get("missing_information")
    if missing_info is not None:
        if not isinstance(missing_info, list):
            violations.append(
                SchemaViolation(
                    field="missing_information",
                    issue=f"expected list, got {type(missing_info).__name__}",
                )
            )
        else:
            for item in missing_info:
                normalized = str(item).strip().lower()
                if normalized not in ALL_MISSING_INFO_FIELDS:
                    violations.append(
                        SchemaViolation(
                            field="missing_information",
                            issue=f"invalid vocabulary item: '{item}'",
                        )
                    )

    # next_best_action validation
    nba = response.get("next_best_action")
    if nba is not None:
        if not isinstance(nba, str):
            violations.append(
                SchemaViolation(
                    field="next_best_action",
                    issue=f"expected string, got {type(nba).__name__}",
                )
            )
        elif not nba.strip():
            violations.append(
                SchemaViolation(
                    field="next_best_action",
                    issue="empty string",
                )
            )

    # remediation_steps validation
    steps = response.get("remediation_steps")
    if steps is not None:
        if not isinstance(steps, list):
            violations.append(
                SchemaViolation(
                    field="remediation_steps",
                    issue=f"expected list, got {type(steps).__name__}",
                )
            )
        elif len(steps) == 0:
            violations.append(
                SchemaViolation(
                    field="remediation_steps",
                    issue="empty list",
                )
            )
        else:
            for i, step in enumerate(steps):
                if not isinstance(step, str) or not str(step).strip():
                    violations.append(
                        SchemaViolation(
                            field="remediation_steps",
                            issue=f"item {i} is empty or not a string",
                        )
                    )

    violation_tuple = tuple(violations)
    return SchemaValidationResult(
        ticket_id=expected_ticket_id,
        is_valid=len(violation_tuple) == 0,
        violations=violation_tuple,
    )
