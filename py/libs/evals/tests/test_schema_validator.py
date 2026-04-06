# Copyright (c) Microsoft. All rights reserved.
"""Tests for the schema validator.

Verifies that the schema validator correctly identifies:
- Valid responses that pass all checks
- Missing required fields
- Invalid category, priority, team values
- Invalid missing_information vocabulary items
- Wrong ticket_id
- Incorrect field types
"""

from ms.evals_core.validators.schema import SchemaValidationResult
from ms.evals_core.validators.schema import validate_response_schema


def _make_valid_response(ticket_id: str = "INC-0001") -> dict[str, object]:
    """Create a minimal valid triage response."""
    return {
        "ticket_id": ticket_id,
        "category": "Network & Connectivity",
        "priority": "P2",
        "assigned_team": "Network Operations",
        "needs_escalation": False,
        "missing_information": ["error_message"],
        "next_best_action": "Investigate the network connectivity issue.",
        "remediation_steps": ["Check network cables", "Restart router"],
    }


# ── Valid response ───────────────────────────────────────────────────


class TestValidResponse:
    def test_fully_valid_response_passes(self) -> None:
        response = _make_valid_response()
        result = validate_response_schema(response, "INC-0001")
        assert result.is_valid
        assert len(result.violations) == 0

    def test_valid_response_with_all_categories(self) -> None:
        categories = [
            "Access & Authentication",
            "Hardware & Peripherals",
            "Network & Connectivity",
            "Software & Applications",
            "Security & Compliance",
            "Data & Storage",
            "General Inquiry",
            "Not a Support Ticket",
        ]
        for cat in categories:
            response = _make_valid_response()
            response["category"] = cat
            result = validate_response_schema(response, "INC-0001")
            assert result.is_valid, f"category '{cat}' should be valid"

    def test_valid_response_with_all_priorities(self) -> None:
        for p in ("P1", "P2", "P3", "P4"):
            response = _make_valid_response()
            response["priority"] = p
            result = validate_response_schema(response, "INC-0001")
            assert result.is_valid, f"priority '{p}' should be valid"

    def test_valid_response_with_all_teams(self) -> None:
        teams = [
            "Identity & Access Management",
            "Endpoint Engineering",
            "Network Operations",
            "Enterprise Applications",
            "Security Operations",
            "Data Platform",
            "None",
        ]
        for team in teams:
            response = _make_valid_response()
            response["assigned_team"] = team
            result = validate_response_schema(response, "INC-0001")
            assert result.is_valid, f"team '{team}' should be valid"

    def test_valid_response_with_empty_missing_info(self) -> None:
        response = _make_valid_response()
        response["missing_information"] = []
        result = validate_response_schema(response, "INC-0001")
        assert result.is_valid

    def test_valid_escalation_true(self) -> None:
        response = _make_valid_response()
        response["needs_escalation"] = True
        result = validate_response_schema(response, "INC-0001")
        assert result.is_valid

    def test_result_type(self) -> None:
        response = _make_valid_response()
        result = validate_response_schema(response, "INC-0001")
        assert isinstance(result, SchemaValidationResult)
        assert result.ticket_id == "INC-0001"


# ── Missing fields ───────────────────────────────────────────────────


class TestMissingFields:
    def test_missing_single_field(self) -> None:
        for field in (
            "ticket_id",
            "category",
            "priority",
            "assigned_team",
            "needs_escalation",
            "missing_information",
            "next_best_action",
            "remediation_steps",
        ):
            response = _make_valid_response()
            del response[field]
            result = validate_response_schema(response, "INC-0001")
            assert not result.is_valid, f"missing '{field}' should be invalid"
            assert any(v.field == field and "missing" in v.issue for v in result.violations)

    def test_empty_response(self) -> None:
        result = validate_response_schema({}, "INC-0001")
        assert not result.is_valid
        assert len(result.violations) == 8  # all 8 required fields missing


# ── Invalid values ───────────────────────────────────────────────────


class TestInvalidValues:
    def test_invalid_category(self) -> None:
        response = _make_valid_response()
        response["category"] = "Invalid Category"
        result = validate_response_schema(response, "INC-0001")
        assert not result.is_valid
        assert any(v.field == "category" for v in result.violations)

    def test_invalid_priority(self) -> None:
        response = _make_valid_response()
        response["priority"] = "P5"
        result = validate_response_schema(response, "INC-0001")
        assert not result.is_valid
        assert any(v.field == "priority" for v in result.violations)

    def test_invalid_team(self) -> None:
        response = _make_valid_response()
        response["assigned_team"] = "The Hacker Team"
        result = validate_response_schema(response, "INC-0001")
        assert not result.is_valid
        assert any(v.field == "assigned_team" for v in result.violations)

    def test_invalid_missing_info_item(self) -> None:
        response = _make_valid_response()
        response["missing_information"] = ["error_message", "invalid_field"]
        result = validate_response_schema(response, "INC-0001")
        assert not result.is_valid
        assert any(v.field == "missing_information" and "invalid_field" in v.issue for v in result.violations)

    def test_missing_info_not_a_list(self) -> None:
        response = _make_valid_response()
        response["missing_information"] = "error_message"
        result = validate_response_schema(response, "INC-0001")
        assert not result.is_valid
        assert any(v.field == "missing_information" and "expected list" in v.issue for v in result.violations)

    def test_ticket_id_mismatch(self) -> None:
        response = _make_valid_response("INC-9999")
        result = validate_response_schema(response, "INC-0001")
        assert not result.is_valid
        assert any(v.field == "ticket_id" for v in result.violations)

    def test_empty_next_best_action(self) -> None:
        response = _make_valid_response()
        response["next_best_action"] = ""
        result = validate_response_schema(response, "INC-0001")
        assert not result.is_valid
        assert any(v.field == "next_best_action" and "empty" in v.issue for v in result.violations)

    def test_empty_remediation_steps(self) -> None:
        response = _make_valid_response()
        response["remediation_steps"] = []
        result = validate_response_schema(response, "INC-0001")
        assert not result.is_valid
        assert any(v.field == "remediation_steps" and "empty" in v.issue for v in result.violations)

    def test_remediation_steps_not_list(self) -> None:
        response = _make_valid_response()
        response["remediation_steps"] = "single step"
        result = validate_response_schema(response, "INC-0001")
        assert not result.is_valid
        assert any(v.field == "remediation_steps" for v in result.violations)

    def test_invalid_escalation_string(self) -> None:
        response = _make_valid_response()
        response["needs_escalation"] = "maybe"
        result = validate_response_schema(response, "INC-0001")
        assert not result.is_valid
        assert any(v.field == "needs_escalation" for v in result.violations)

    def test_valid_escalation_string_true(self) -> None:
        response = _make_valid_response()
        response["needs_escalation"] = "true"
        result = validate_response_schema(response, "INC-0001")
        # "true" is a valid boolean string — no violation
        assert not any(v.field == "needs_escalation" for v in result.violations)

    def test_next_best_action_not_string(self) -> None:
        response = _make_valid_response()
        response["next_best_action"] = 42
        result = validate_response_schema(response, "INC-0001")
        assert not result.is_valid
        assert any(v.field == "next_best_action" and "expected string" in v.issue for v in result.violations)
