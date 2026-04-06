# Copyright (c) Microsoft. All rights reserved.
"""Scoring logic for data cleanup evaluation scenarios.

Data cleanup scoring checks whether the triage API:
1. Returns a structurally valid response (valid JSON, required fields)
2. Uses only valid enum values from the constrained vocabulary
3. Correctly classifies the ticket despite noisy/corrupted input
"""

from ms.evals_core.framework.models.result import CheckResult
from ms.evals_core.framework.models.result import ScenarioResult
from ms.evals_core.framework.models.scenario import EvalScenario
from ms.evals_core.framework.scoring.valid_values import VALID_CATEGORIES
from ms.evals_core.framework.scoring.valid_values import VALID_MISSING_INFO
from ms.evals_core.framework.scoring.valid_values import VALID_PRIORITIES
from ms.evals_core.framework.scoring.valid_values import VALID_TEAMS


def _normalize(text: str) -> str:
    return text.strip().lower()


def _check_response_structure(response: dict) -> CheckResult:
    """Verify the response has all required fields."""
    required_fields = {
        "ticket_id",
        "category",
        "priority",
        "assigned_team",
        "needs_escalation",
        "missing_information",
        "next_best_action",
        "remediation_steps",
    }
    missing = required_fields - set(response.keys())
    if missing:
        return CheckResult(
            name="response_structure",
            passed=False,
            message=f"Missing required fields: {sorted(missing)}",
        )
    return CheckResult(
        name="response_structure",
        passed=True,
        message="All required fields present",
    )


def _check_valid_category(response: dict) -> CheckResult:
    """Verify category is from the valid set."""
    category = response.get("category", "")
    if not isinstance(category, str):
        return CheckResult(name="valid_category", passed=False, message=f"Category is not a string: {type(category)}")
    normalized_valid = {_normalize(c) for c in VALID_CATEGORIES}
    if _normalize(category) in normalized_valid:
        return CheckResult(name="valid_category", passed=True, message=f"Valid category: {category}")
    return CheckResult(name="valid_category", passed=False, message=f"Invalid category: '{category}'")


def _check_valid_priority(response: dict) -> CheckResult:
    """Verify priority is from the valid set."""
    priority = response.get("priority", "")
    if not isinstance(priority, str):
        return CheckResult(name="valid_priority", passed=False, message=f"Priority is not a string: {type(priority)}")
    if priority.strip().upper() in VALID_PRIORITIES:
        return CheckResult(name="valid_priority", passed=True, message=f"Valid priority: {priority}")
    return CheckResult(name="valid_priority", passed=False, message=f"Invalid priority: '{priority}'")


def _check_valid_team(response: dict) -> CheckResult:
    """Verify assigned_team is from the valid set."""
    team = response.get("assigned_team", "")
    if not isinstance(team, str):
        return CheckResult(name="valid_team", passed=False, message=f"Team is not a string: {type(team)}")
    normalized_valid = {_normalize(t) for t in VALID_TEAMS}
    if _normalize(team) in normalized_valid:
        return CheckResult(name="valid_team", passed=True, message=f"Valid team: {team}")
    return CheckResult(name="valid_team", passed=False, message=f"Invalid team: '{team}'")


def _check_valid_missing_info(response: dict) -> CheckResult:
    """Verify missing_information items are from the valid vocabulary."""
    items = response.get("missing_information", [])
    if not isinstance(items, list):
        return CheckResult(
            name="valid_missing_info",
            passed=False,
            message=f"missing_information is not a list: {type(items)}",
        )
    normalized_valid = {_normalize(v) for v in VALID_MISSING_INFO}
    invalid = [item for item in items if _normalize(str(item)) not in normalized_valid]
    if invalid:
        return CheckResult(
            name="valid_missing_info",
            passed=False,
            message=f"Invalid missing_information values: {invalid}",
        )
    return CheckResult(name="valid_missing_info", passed=True, message="All missing_information values are valid")


def _check_expected_category(response: dict, expected: str) -> CheckResult:
    """Check if the category matches the expected value."""
    actual = response.get("category", "")
    if _normalize(str(actual)) == _normalize(expected):
        return CheckResult(name="expected_category", passed=True, message=f"Category matches: {actual}")
    return CheckResult(
        name="expected_category",
        passed=False,
        message=f"Expected category '{expected}', got '{actual}'",
    )


def _check_expected_priority(response: dict, expected: str) -> CheckResult:
    """Check if the priority matches the expected value."""
    actual = response.get("priority", "")
    if str(actual).strip().upper() == expected.strip().upper():
        return CheckResult(name="expected_priority", passed=True, message=f"Priority matches: {actual}")
    return CheckResult(
        name="expected_priority",
        passed=False,
        message=f"Expected priority '{expected}', got '{actual}'",
    )


def _check_expected_team(response: dict, expected: str) -> CheckResult:
    """Check if the assigned_team matches the expected value."""
    actual = response.get("assigned_team", "")
    if _normalize(str(actual)) == _normalize(expected):
        return CheckResult(name="expected_team", passed=True, message=f"Team matches: {actual}")
    return CheckResult(
        name="expected_team",
        passed=False,
        message=f"Expected team '{expected}', got '{actual}'",
    )


def _check_expected_escalation(response: dict, expected: bool) -> CheckResult:
    """Check if needs_escalation matches the expected value."""
    actual = response.get("needs_escalation")
    coerced = _coerce_bool(actual)
    if coerced == expected:
        return CheckResult(name="expected_escalation", passed=True, message=f"Escalation matches: {coerced}")
    return CheckResult(
        name="expected_escalation",
        passed=False,
        message=f"Expected escalation={expected}, got '{actual}' (coerced to {coerced})",
    )


def _coerce_bool(value: object) -> bool:
    """Safely coerce a value to boolean, matching run_eval.py behavior."""
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().lower() in {"true", "1", "yes"}
    if isinstance(value, int):
        return value != 0
    return False


def score_data_cleanup(scenario: EvalScenario, response: dict) -> ScenarioResult:
    """Score a data cleanup scenario against an API response.

    Scoring dimensions:
    - Response structure (required fields present)
    - Schema compliance (valid enum values)
    - Classification accuracy (if expected values provided)

    Returns a ScenarioResult with per-check details and an overall score.
    """
    checks: list[CheckResult] = []

    # Structural validity checks
    checks.append(_check_response_structure(response))
    checks.append(_check_valid_category(response))
    checks.append(_check_valid_priority(response))
    checks.append(_check_valid_team(response))
    checks.append(_check_valid_missing_info(response))

    # Classification accuracy checks (only for expected values provided)
    expected = scenario.expected_triage
    if expected is not None:
        if expected.category is not None:
            checks.append(_check_expected_category(response, expected.category))
        if expected.priority is not None:
            checks.append(_check_expected_priority(response, expected.priority))
        if expected.assigned_team is not None:
            checks.append(_check_expected_team(response, expected.assigned_team))
        if expected.needs_escalation is not None:
            checks.append(_check_expected_escalation(response, expected.needs_escalation))

    passed_count = sum(1 for c in checks if c.passed)
    total_count = len(checks)
    score = passed_count / total_count if total_count > 0 else 0.0
    all_passed = all(c.passed for c in checks)

    return ScenarioResult(
        scenario_id=scenario.scenario_id,
        passed=all_passed,
        score=round(score, 4),
        checks=checks,
    )
