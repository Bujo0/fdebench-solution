# Copyright (c) Microsoft. All rights reserved.
"""Tests for data cleanup scoring logic."""

from ms.evals.models.scenario import EvalReporter
from ms.evals.models.scenario import EvalScenario
from ms.evals.models.scenario import EvalTicket
from ms.evals.models.scenario import ExpectedTriage
from ms.evals.models.scenario import ScenarioCategory
from ms.evals.scoring.data_cleanup import score_data_cleanup


def _make_scenario(
    expected_category: str | None = None,
    expected_priority: str | None = None,
    expected_team: str | None = None,
    expected_escalation: bool | None = None,
) -> EvalScenario:
    return EvalScenario(
        scenario_id="dc-test",
        name="Test scenario",
        description="Test",
        category=ScenarioCategory.DATA_CLEANUP,
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
    )


def _make_response(
    *,
    category: str = "Network & Connectivity",
    priority: str = "P2",
    team: str = "Network Operations",
    escalation: bool = False,
    missing_info: list[str] | None = None,
) -> dict:
    return {
        "ticket_id": "INC-TEST",
        "category": category,
        "priority": priority,
        "assigned_team": team,
        "needs_escalation": escalation,
        "missing_information": missing_info or [],
        "next_best_action": "Investigate the issue.",
        "remediation_steps": ["Step 1", "Step 2"],
    }


class TestResponseStructure:
    def test_complete_response_passes(self) -> None:
        scenario = _make_scenario()
        result = score_data_cleanup(scenario, _make_response())
        structure_check = next(c for c in result.checks if c.name == "response_structure")
        assert structure_check.passed

    def test_missing_field_fails(self) -> None:
        scenario = _make_scenario()
        response = _make_response()
        del response["category"]
        result = score_data_cleanup(scenario, response)
        structure_check = next(c for c in result.checks if c.name == "response_structure")
        assert not structure_check.passed
        assert "category" in structure_check.message


class TestValidCategory:
    def test_valid_category(self) -> None:
        scenario = _make_scenario()
        result = score_data_cleanup(scenario, _make_response(category="Network & Connectivity"))
        cat_check = next(c for c in result.checks if c.name == "valid_category")
        assert cat_check.passed

    def test_case_insensitive(self) -> None:
        scenario = _make_scenario()
        result = score_data_cleanup(scenario, _make_response(category="network & connectivity"))
        cat_check = next(c for c in result.checks if c.name == "valid_category")
        assert cat_check.passed

    def test_invalid_category(self) -> None:
        scenario = _make_scenario()
        result = score_data_cleanup(scenario, _make_response(category="HACKED"))
        cat_check = next(c for c in result.checks if c.name == "valid_category")
        assert not cat_check.passed


class TestValidPriority:
    def test_valid_priorities(self) -> None:
        for p in ("P1", "P2", "P3", "P4"):
            scenario = _make_scenario()
            result = score_data_cleanup(scenario, _make_response(priority=p))
            pri_check = next(c for c in result.checks if c.name == "valid_priority")
            assert pri_check.passed

    def test_invalid_priority(self) -> None:
        scenario = _make_scenario()
        result = score_data_cleanup(scenario, _make_response(priority="P0"))
        pri_check = next(c for c in result.checks if c.name == "valid_priority")
        assert not pri_check.passed


class TestValidTeam:
    def test_valid_team(self) -> None:
        scenario = _make_scenario()
        result = score_data_cleanup(scenario, _make_response(team="Network Operations"))
        team_check = next(c for c in result.checks if c.name == "valid_team")
        assert team_check.passed

    def test_none_team_valid(self) -> None:
        scenario = _make_scenario()
        result = score_data_cleanup(scenario, _make_response(team="None"))
        team_check = next(c for c in result.checks if c.name == "valid_team")
        assert team_check.passed

    def test_invalid_team(self) -> None:
        scenario = _make_scenario()
        result = score_data_cleanup(scenario, _make_response(team="CEO Direct"))
        team_check = next(c for c in result.checks if c.name == "valid_team")
        assert not team_check.passed


class TestValidMissingInfo:
    def test_empty_list(self) -> None:
        scenario = _make_scenario()
        result = score_data_cleanup(scenario, _make_response(missing_info=[]))
        mi_check = next(c for c in result.checks if c.name == "valid_missing_info")
        assert mi_check.passed

    def test_valid_items(self) -> None:
        scenario = _make_scenario()
        result = score_data_cleanup(scenario, _make_response(missing_info=["error_message", "device_info"]))
        mi_check = next(c for c in result.checks if c.name == "valid_missing_info")
        assert mi_check.passed

    def test_invalid_item(self) -> None:
        scenario = _make_scenario()
        result = score_data_cleanup(scenario, _make_response(missing_info=["classified_data"]))
        mi_check = next(c for c in result.checks if c.name == "valid_missing_info")
        assert not mi_check.passed


class TestExpectedValues:
    def test_matching_category(self) -> None:
        scenario = _make_scenario(expected_category="Network & Connectivity")
        result = score_data_cleanup(scenario, _make_response(category="Network & Connectivity"))
        expected_check = next(c for c in result.checks if c.name == "expected_category")
        assert expected_check.passed

    def test_wrong_category(self) -> None:
        scenario = _make_scenario(expected_category="Security & Compliance")
        result = score_data_cleanup(scenario, _make_response(category="Network & Connectivity"))
        expected_check = next(c for c in result.checks if c.name == "expected_category")
        assert not expected_check.passed

    def test_matching_priority(self) -> None:
        scenario = _make_scenario(expected_priority="P2")
        result = score_data_cleanup(scenario, _make_response(priority="P2"))
        expected_check = next(c for c in result.checks if c.name == "expected_priority")
        assert expected_check.passed

    def test_matching_team(self) -> None:
        scenario = _make_scenario(expected_team="Network Operations")
        result = score_data_cleanup(scenario, _make_response(team="Network Operations"))
        expected_check = next(c for c in result.checks if c.name == "expected_team")
        assert expected_check.passed

    def test_matching_escalation(self) -> None:
        scenario = _make_scenario(expected_escalation=False)
        result = score_data_cleanup(scenario, _make_response(escalation=False))
        expected_check = next(c for c in result.checks if c.name == "expected_escalation")
        assert expected_check.passed

    def test_wrong_escalation(self) -> None:
        scenario = _make_scenario(expected_escalation=True)
        result = score_data_cleanup(scenario, _make_response(escalation=False))
        expected_check = next(c for c in result.checks if c.name == "expected_escalation")
        assert not expected_check.passed


class TestOverallScoring:
    def test_perfect_score(self) -> None:
        scenario = _make_scenario(
            expected_category="Network & Connectivity",
            expected_priority="P2",
            expected_team="Network Operations",
            expected_escalation=False,
        )
        result = score_data_cleanup(scenario, _make_response())
        assert result.passed
        assert result.score == 1.0

    def test_all_wrong_score(self) -> None:
        scenario = _make_scenario(
            expected_category="Security & Compliance",
            expected_priority="P1",
            expected_team="Security Operations",
            expected_escalation=True,
        )
        result = score_data_cleanup(scenario, _make_response())
        assert not result.passed
        # 5 structural checks pass + 4 expected checks fail
        assert result.score < 1.0

    def test_no_expectations_only_structural(self) -> None:
        scenario = EvalScenario(
            scenario_id="dc-no-expect",
            name="No expectations",
            description="Test",
            category=ScenarioCategory.DATA_CLEANUP,
            ticket=EvalTicket(
                ticket_id="INC-TEST",
                subject="Test",
                description="Test",
                reporter=EvalReporter(name="Test", email="test@contoso.com", department="IT"),
                created_at="2026-01-01T00:00:00Z",
                channel="email",
            ),
        )
        result = score_data_cleanup(scenario, _make_response())
        assert result.passed
        # Only 5 structural checks, all passing
        assert len(result.checks) == 5
        assert result.score == 1.0
