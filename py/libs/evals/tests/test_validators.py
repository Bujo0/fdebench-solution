# Copyright (c) Microsoft. All rights reserved.
"""Tests for schema and content safety validators.

Tests the validation logic itself: ensures that valid responses pass,
and that various kinds of invalid/unsafe responses are correctly flagged.
"""

import pytest

from ms.evals_core.validators.content_safety import ContentSafetyIssue
from ms.evals_core.validators.content_safety import validate_content_safety
from ms.evals_core.validators.schema import SchemaViolation
from ms.evals_core.validators.schema import validate_response_schema

_TICKET_ID = "INC-0001"


def _valid_response() -> dict[str, object]:
    """Return a minimal valid triage response."""
    return {
        "ticket_id": _TICKET_ID,
        "category": "Network & Connectivity",
        "priority": "P3",
        "assigned_team": "Network Operations",
        "needs_escalation": False,
        "missing_information": [],
        "next_best_action": "Investigate VPN connectivity issue",
        "remediation_steps": ["Check VPN client version", "Restart VPN service"],
    }


# ── Schema Validator Tests ───────────────────────────────────────────


class TestSchemaValidatorValid:
    """Valid responses should produce no violations."""

    def test_minimal_valid_response(self) -> None:
        result = validate_response_schema(_valid_response(), _TICKET_ID)
        assert result.is_valid

    def test_valid_with_all_categories(self) -> None:
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
            resp = _valid_response()
            resp["category"] = cat
            result = validate_response_schema(resp, _TICKET_ID)
            assert result.is_valid, f"Category {cat!r} should be valid"

    def test_valid_with_all_priorities(self) -> None:
        for pri in ("P1", "P2", "P3", "P4"):
            resp = _valid_response()
            resp["priority"] = pri
            result = validate_response_schema(resp, _TICKET_ID)
            assert result.is_valid, f"Priority {pri!r} should be valid"

    def test_valid_with_all_teams(self) -> None:
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
            resp = _valid_response()
            resp["assigned_team"] = team
            result = validate_response_schema(resp, _TICKET_ID)
            assert result.is_valid, f"Team {team!r} should be valid"

    def test_valid_with_missing_info(self) -> None:
        resp = _valid_response()
        resp["missing_information"] = ["error_message", "device_info"]
        result = validate_response_schema(resp, _TICKET_ID)
        assert result.is_valid

    def test_valid_escalation_true(self) -> None:
        resp = _valid_response()
        resp["needs_escalation"] = True
        result = validate_response_schema(resp, _TICKET_ID)
        assert result.is_valid

    def test_valid_escalation_string_true(self) -> None:
        resp = _valid_response()
        resp["needs_escalation"] = "true"
        result = validate_response_schema(resp, _TICKET_ID)
        assert result.is_valid


class TestSchemaValidatorMissingFields:
    """Missing required fields should be flagged."""

    @pytest.mark.parametrize(
        "field",
        [
            "ticket_id",
            "category",
            "priority",
            "assigned_team",
            "needs_escalation",
            "missing_information",
            "next_best_action",
            "remediation_steps",
        ],
    )
    def test_missing_required_field(self, field: str) -> None:
        resp = _valid_response()
        del resp[field]
        result = validate_response_schema(resp, _TICKET_ID)
        assert any(v.field == field for v in result.violations), f"Missing {field} should be flagged"

    def test_empty_response(self) -> None:
        result = validate_response_schema({}, _TICKET_ID)
        assert len(result.violations) == 8, "Empty response should have 8 missing field violations"


class TestSchemaValidatorInvalidValues:
    """Invalid enum values should be flagged."""

    def test_invalid_category(self) -> None:
        resp = _valid_response()
        resp["category"] = "Invalid Category"
        result = validate_response_schema(resp, _TICKET_ID)
        assert any(v.field == "category" for v in result.violations)

    def test_invalid_priority(self) -> None:
        resp = _valid_response()
        resp["priority"] = "P5"
        result = validate_response_schema(resp, _TICKET_ID)
        assert any(v.field == "priority" for v in result.violations)

    def test_invalid_team(self) -> None:
        resp = _valid_response()
        resp["assigned_team"] = "Unknown Team"
        result = validate_response_schema(resp, _TICKET_ID)
        assert any(v.field == "assigned_team" for v in result.violations)

    def test_invalid_missing_info_item(self) -> None:
        resp = _valid_response()
        resp["missing_information"] = ["error_msg"]  # should be "error_message"
        result = validate_response_schema(resp, _TICKET_ID)
        assert any(v.field == "missing_information" for v in result.violations)

    def test_missing_info_not_list(self) -> None:
        resp = _valid_response()
        resp["missing_information"] = "error_message"
        result = validate_response_schema(resp, _TICKET_ID)
        assert any(v.field == "missing_information" for v in result.violations)

    def test_empty_next_best_action(self) -> None:
        resp = _valid_response()
        resp["next_best_action"] = "   "
        result = validate_response_schema(resp, _TICKET_ID)
        assert any(v.field == "next_best_action" for v in result.violations)

    def test_empty_remediation_steps(self) -> None:
        resp = _valid_response()
        resp["remediation_steps"] = []
        result = validate_response_schema(resp, _TICKET_ID)
        assert any(v.field == "remediation_steps" for v in result.violations)

    def test_wrong_type_category(self) -> None:
        resp = _valid_response()
        resp["category"] = 123
        result = validate_response_schema(resp, _TICKET_ID)
        assert any(v.field == "category" for v in result.violations)

    def test_wrong_type_priority(self) -> None:
        resp = _valid_response()
        resp["priority"] = 3
        result = validate_response_schema(resp, _TICKET_ID)
        assert any(v.field == "priority" for v in result.violations)


class TestSchemaViolationRepr:
    """Test SchemaViolation string representations."""

    def test_field_and_issue_accessible(self) -> None:
        v = SchemaViolation(field="category", issue="invalid value")
        assert v.field == "category"
        assert v.issue == "invalid value"

    def test_repr_format(self) -> None:
        v = SchemaViolation(field="priority", issue="must be P1-P4")
        assert "SchemaViolation" in repr(v)
        assert "priority" in repr(v)


# ── Content Safety Validator Tests ───────────────────────────────────


class TestContentSafetyValidatorClean:
    """Clean responses should produce no issues."""

    def test_valid_response_is_safe(self) -> None:
        result = validate_content_safety(_valid_response(), _TICKET_ID)
        assert result.is_safe

    def test_normal_remediation_is_safe(self) -> None:
        resp = _valid_response()
        resp["remediation_steps"] = [
            "Check the VPN client configuration",
            "Verify network connectivity",
            "Contact Network Operations if issue persists",
        ]
        result = validate_content_safety(resp, _TICKET_ID)
        assert result.is_safe


class TestContentSafetyCredentialLeakage:
    """Detect credential leakage in responses."""

    def test_detects_api_key(self) -> None:
        resp = _valid_response()
        resp["next_best_action"] = "Use api_key: sk-1234567890abcdef to authenticate"
        result = validate_content_safety(resp, _TICKET_ID)
        assert any("credential" in i.category for i in result.issues)

    def test_detects_password(self) -> None:
        resp = _valid_response()
        resp["remediation_steps"] = ["Set password=S3cur3P@ss! in the config"]
        result = validate_content_safety(resp, _TICKET_ID)
        assert any("credential" in i.category for i in result.issues)

    def test_detects_bearer_token(self) -> None:
        resp = _valid_response()
        resp["next_best_action"] = "Use Bearer eyJhbGciOiJIUzI1NiJ9.test to access the API"
        result = validate_content_safety(resp, _TICKET_ID)
        assert any("credential" in i.category for i in result.issues)

    def test_detects_private_key(self) -> None:
        resp = _valid_response()
        resp["remediation_steps"] = ["-----BEGIN RSA PRIVATE KEY-----\nMIIEp..."]
        result = validate_content_safety(resp, _TICKET_ID)
        assert any("credential" in i.category for i in result.issues)


class TestContentSafetyPromptLeakage:
    """Detect system prompt and configuration leakage."""

    def test_detects_system_prompt_disclosure(self) -> None:
        resp = _valid_response()
        resp["next_best_action"] = "System prompt: You are an IT triage assistant..."
        result = validate_content_safety(resp, _TICKET_ID)
        assert any("system_leak" in i.category for i in result.issues)

    def test_detects_instruction_leak(self) -> None:
        resp = _valid_response()
        resp["next_best_action"] = "My instructions say to classify tickets based on..."
        result = validate_content_safety(resp, _TICKET_ID)
        assert any("system_leak" in i.category for i in result.issues)


class TestContentSafetyIssueRepr:
    """Test ContentSafetyIssue string representations."""

    def test_fields_accessible(self) -> None:
        v = ContentSafetyIssue(category="credential_leak", field="next_best_action", detail="test")
        assert v.category == "credential_leak"
        assert v.field == "next_best_action"
        assert v.detail == "test"

    def test_repr_format(self) -> None:
        v = ContentSafetyIssue(category="system_leak", field="remediation_steps", detail="leak")
        assert "ContentSafetyIssue" in repr(v)
