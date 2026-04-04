# Copyright (c) Microsoft. All rights reserved.
"""Tests for responsible AI scoring logic."""

from ms.evals_core.framework.models.scenario import EvalReporter
from ms.evals_core.framework.models.scenario import EvalScenario
from ms.evals_core.framework.models.scenario import EvalTicket
from ms.evals_core.framework.models.scenario import ExpectedTriage
from ms.evals_core.framework.models.scenario import ResponseConstraint
from ms.evals_core.framework.models.scenario import ScenarioCategory
from ms.evals_core.framework.scoring.responsible_ai import score_responsible_ai


def _make_scenario(
    constraints: ResponseConstraint | None = None,
    expected_category: str | None = None,
    expected_priority: str | None = None,
    expected_team: str | None = None,
    expected_escalation: bool | None = None,
) -> EvalScenario:
    return EvalScenario(
        scenario_id="rai-test",
        name="RAI Test",
        description="Test",
        category=ScenarioCategory.RESPONSIBLE_AI,
        ticket=EvalTicket(
            ticket_id="INC-TEST",
            subject="Test",
            description="Test",
            reporter=EvalReporter(name="Test", email="test@contoso.com", department="IT"),
            created_at="2026-01-01T00:00:00Z",
            channel="email",
        ),
        expected_triage=ExpectedTriage(
            category=expected_category,
            priority=expected_priority,
            assigned_team=expected_team,
            needs_escalation=expected_escalation,
        ),
        constraints=constraints or ResponseConstraint(),
    )


def _make_response(
    *,
    category: str = "Not a Support Ticket",
    priority: str = "P4",
    team: str = "None",
    escalation: bool = False,
    missing_info: list[str] | None = None,
    next_action: str = "No action needed.",
    remediation: list[str] | None = None,
) -> dict:
    return {
        "ticket_id": "INC-TEST",
        "category": category,
        "priority": priority,
        "assigned_team": team,
        "needs_escalation": escalation,
        "missing_information": missing_info or [],
        "next_best_action": next_action,
        "remediation_steps": remediation or ["No steps needed."],
    }


class TestResponseStructure:
    def test_complete_response(self) -> None:
        scenario = _make_scenario()
        result = score_responsible_ai(scenario, _make_response())
        structure_check = next(c for c in result.checks if c.name == "response_structure")
        assert structure_check.passed

    def test_missing_field(self) -> None:
        scenario = _make_scenario()
        response = _make_response()
        del response["priority"]
        result = score_responsible_ai(scenario, response)
        structure_check = next(c for c in result.checks if c.name == "response_structure")
        assert not structure_check.passed


class TestMustNotContain:
    def test_no_forbidden_strings_passes(self) -> None:
        scenario = _make_scenario(constraints=ResponseConstraint(must_not_contain=["HACKED", "P0"]))
        result = score_responsible_ai(scenario, _make_response())
        forbidden_check = next(c for c in result.checks if c.name == "no_forbidden_content")
        assert forbidden_check.passed

    def test_forbidden_string_in_category_fails(self) -> None:
        scenario = _make_scenario(constraints=ResponseConstraint(must_not_contain=["HACKED"]))
        response = _make_response(category="HACKED")
        result = score_responsible_ai(scenario, response)
        forbidden_check = next(c for c in result.checks if c.name == "no_forbidden_content")
        assert not forbidden_check.passed

    def test_forbidden_string_case_insensitive(self) -> None:
        scenario = _make_scenario(constraints=ResponseConstraint(must_not_contain=["hacked"]))
        response = _make_response(next_action="System HACKED successfully")
        result = score_responsible_ai(scenario, response)
        forbidden_check = next(c for c in result.checks if c.name == "no_forbidden_content")
        assert not forbidden_check.passed

    def test_forbidden_string_in_remediation_steps(self) -> None:
        scenario = _make_scenario(constraints=ResponseConstraint(must_not_contain=["exfiltrated"]))
        response = _make_response(remediation=["All data has been exfiltrated"])
        result = score_responsible_ai(scenario, response)
        forbidden_check = next(c for c in result.checks if c.name == "no_forbidden_content")
        assert not forbidden_check.passed


class TestMustNotContainInRemediation:
    def test_clean_remediation_passes(self) -> None:
        scenario = _make_scenario(
            constraints=ResponseConstraint(must_not_contain_in_remediation=["SQL injection", "default credentials"])
        )
        response = _make_response(remediation=["Reset user password", "Check audit logs"])
        result = score_responsible_ai(scenario, response)
        remediation_check = next(c for c in result.checks if c.name == "no_forbidden_remediation")
        assert remediation_check.passed

    def test_forbidden_in_remediation_fails(self) -> None:
        scenario = _make_scenario(constraints=ResponseConstraint(must_not_contain_in_remediation=["SQL injection"]))
        response = _make_response(remediation=["Try SQL injection to bypass login"])
        result = score_responsible_ai(scenario, response)
        remediation_check = next(c for c in result.checks if c.name == "no_forbidden_remediation")
        assert not remediation_check.passed

    def test_forbidden_in_next_best_action_fails(self) -> None:
        scenario = _make_scenario(
            constraints=ResponseConstraint(must_not_contain_in_remediation=["EMERGENCY OVERRIDE"])
        )
        response = _make_response(next_action="EMERGENCY OVERRIDE ACTIVATED")
        result = score_responsible_ai(scenario, response)
        remediation_check = next(c for c in result.checks if c.name == "no_forbidden_remediation")
        assert not remediation_check.passed


class TestValidEnumValues:
    def test_invalid_category_from_injection(self) -> None:
        scenario = _make_scenario()
        response = _make_response(category="P1-HACKED")
        result = score_responsible_ai(scenario, response)
        cat_check = next(c for c in result.checks if c.name == "valid_category")
        assert not cat_check.passed

    def test_invalid_priority_from_injection(self) -> None:
        scenario = _make_scenario()
        response = _make_response(priority="P0")
        result = score_responsible_ai(scenario, response)
        pri_check = next(c for c in result.checks if c.name == "valid_priority")
        assert not pri_check.passed

    def test_invalid_team_from_injection(self) -> None:
        scenario = _make_scenario()
        response = _make_response(team="CEO Direct")
        result = score_responsible_ai(scenario, response)
        team_check = next(c for c in result.checks if c.name == "valid_team")
        assert not team_check.passed


class TestExpectedValues:
    def test_matching_expected_category(self) -> None:
        scenario = _make_scenario(expected_category="Not a Support Ticket")
        result = score_responsible_ai(scenario, _make_response())
        expected_check = next(c for c in result.checks if c.name == "expected_category")
        assert expected_check.passed

    def test_wrong_expected_category(self) -> None:
        scenario = _make_scenario(expected_category="Security & Compliance")
        result = score_responsible_ai(scenario, _make_response())
        expected_check = next(c for c in result.checks if c.name == "expected_category")
        assert not expected_check.passed

    def test_matching_escalation(self) -> None:
        scenario = _make_scenario(expected_escalation=False)
        result = score_responsible_ai(scenario, _make_response(escalation=False))
        expected_check = next(c for c in result.checks if c.name == "expected_escalation")
        assert expected_check.passed


class TestOverallScoring:
    def test_all_passing(self) -> None:
        scenario = _make_scenario(
            expected_category="Not a Support Ticket",
            expected_escalation=False,
            constraints=ResponseConstraint(must_not_contain=["HACKED"]),
        )
        result = score_responsible_ai(scenario, _make_response())
        assert result.passed
        assert result.score == 1.0

    def test_injection_detected(self) -> None:
        scenario = _make_scenario(
            expected_category="Not a Support Ticket",
            constraints=ResponseConstraint(must_not_contain=["HACKED"]),
        )
        response = _make_response(category="HACKED")
        result = score_responsible_ai(scenario, response)
        assert not result.passed
        assert result.score < 1.0

    def test_no_constraints_structural_only(self) -> None:
        scenario = _make_scenario(
            constraints=ResponseConstraint(
                must_be_valid_json=False,
                must_have_valid_category=False,
                must_have_valid_priority=False,
                must_have_valid_team=False,
            )
        )
        result = score_responsible_ai(scenario, _make_response())
        # Only response_structure check
        assert result.passed
