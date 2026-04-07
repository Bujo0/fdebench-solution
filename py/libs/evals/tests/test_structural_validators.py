# Copyright (c) Microsoft. All rights reserved.
"""Tests for the structural response validator."""

from ms.evals_core.validators.structural import validate_response_structure


def _make_response(**overrides: object) -> dict[str, object]:
    base: dict[str, object] = {
        "ticket_id": "INC-TEST",
        "category": "Network & Connectivity",
        "priority": "P3",
        "assigned_team": "Network Operations",
        "needs_escalation": False,
        "missing_information": [],
        "next_best_action": "Investigate the VPN issue.",
        "remediation_steps": ["Check VPN client version"],
    }
    base.update(overrides)
    return base


class TestValidateResponseStructure:
    """Tests for structural validation of triage responses."""

    def test_valid_response_no_violations(self) -> None:
        violations = validate_response_structure(_make_response())
        assert len(violations) == 0

    def test_missing_required_fields(self) -> None:
        violations = validate_response_structure({"ticket_id": "INC-TEST"})
        assert len(violations) > 0
        missing_fields = {v.field for v in violations}
        assert "category" in missing_fields
        assert "priority" in missing_fields
        assert "assigned_team" in missing_fields

    def test_invalid_category(self) -> None:
        violations = validate_response_structure(_make_response(category="Invalid Category"))
        assert any(v.field == "category" for v in violations)

    def test_invalid_priority(self) -> None:
        violations = validate_response_structure(_make_response(priority="P5"))
        assert any(v.field == "priority" for v in violations)

    def test_invalid_team(self) -> None:
        violations = validate_response_structure(_make_response(assigned_team="Invalid Team"))
        assert any(v.field == "assigned_team" for v in violations)

    def test_none_team_is_valid(self) -> None:
        violations = validate_response_structure(_make_response(assigned_team="None"))
        team_violations = [v for v in violations if v.field == "assigned_team"]
        assert len(team_violations) == 0

    def test_invalid_escalation_type(self) -> None:
        violations = validate_response_structure(_make_response(needs_escalation=[1, 2, 3]))
        assert any(v.field == "needs_escalation" for v in violations)

    def test_string_escalation_accepted(self) -> None:
        """String 'true'/'false' should be accepted (coercible)."""
        violations = validate_response_structure(_make_response(needs_escalation="true"))
        escalation_violations = [v for v in violations if v.field == "needs_escalation"]
        assert len(escalation_violations) == 0

    def test_missing_info_not_list(self) -> None:
        violations = validate_response_structure(_make_response(missing_information="device_info"))
        assert any(v.field == "missing_information" for v in violations)

    def test_missing_info_invalid_vocab(self) -> None:
        violations = validate_response_structure(_make_response(missing_information=["device_info", "invalid_field"]))
        assert any(v.field == "missing_information" and "invalid_field" in v.args[0] for v in violations)

    def test_empty_next_best_action(self) -> None:
        violations = validate_response_structure(_make_response(next_best_action=""))
        assert any(v.field == "next_best_action" for v in violations)

    def test_empty_remediation_steps(self) -> None:
        violations = validate_response_structure(_make_response(remediation_steps=[]))
        assert any(v.field == "remediation_steps" for v in violations)

    def test_remediation_steps_non_string(self) -> None:
        violations = validate_response_structure(_make_response(remediation_steps=[123]))
        assert any(v.field == "remediation_steps" for v in violations)

    def test_case_insensitive_category(self) -> None:
        violations = validate_response_structure(_make_response(category="network & connectivity"))
        category_violations = [v for v in violations if v.field == "category"]
        assert len(category_violations) == 0

    def test_all_categories_accepted(self) -> None:
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
            violations = validate_response_structure(_make_response(category=cat))
            cat_violations = [v for v in violations if v.field == "category"]
            assert len(cat_violations) == 0, f"Category {cat!r} rejected"

    def test_all_priorities_accepted(self) -> None:
        for pri in ["P1", "P2", "P3", "P4"]:
            violations = validate_response_structure(_make_response(priority=pri))
            pri_violations = [v for v in violations if v.field == "priority"]
            assert len(pri_violations) == 0, f"Priority {pri!r} rejected"

    def test_all_teams_accepted(self) -> None:
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
            violations = validate_response_structure(_make_response(assigned_team=team))
            team_violations = [v for v in violations if v.field == "assigned_team"]
            assert len(team_violations) == 0, f"Team {team!r} rejected"

    def test_violation_contains_ticket_id(self) -> None:
        violations = validate_response_structure({"ticket_id": "INC-1234"})
        assert all(v.ticket_id == "INC-1234" for v in violations)
