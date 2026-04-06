# Copyright (c) Microsoft. All rights reserved.
"""Tests for the data cleanup validators."""

from ms.evals_core.validators.data_cleanup import check_classification_despite_noise
from ms.evals_core.validators.data_cleanup import check_enum_values_clean
from ms.evals_core.validators.data_cleanup import check_output_not_contaminated
from ms.evals_core.validators.data_cleanup import validate_data_cleanup_response


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


def _make_gold(**overrides: object) -> dict[str, object]:
    base: dict[str, object] = {
        "category": "Network & Connectivity",
        "priority": "P3",
        "assigned_team": "Network Operations",
    }
    base.update(overrides)
    return base


class TestCheckOutputNotContaminated:
    """Tests for contamination detection in output fields."""

    def test_clean_output_no_issues(self) -> None:
        issues = check_output_not_contaminated("INC-TEST", _make_response())
        assert len(issues) == 0

    def test_html_in_next_best_action(self) -> None:
        response = _make_response(next_best_action="<html><body>Check the VPN</body></html>")
        issues = check_output_not_contaminated("INC-TEST", response)
        assert any(i.check == "html_contamination" for i in issues)

    def test_html_in_remediation_steps(self) -> None:
        response = _make_response(remediation_steps=["<div>Step 1</div>", "Step 2"])
        issues = check_output_not_contaminated("INC-TEST", response)
        assert any(i.check == "html_contamination" for i in issues)

    def test_base64_in_next_best_action(self) -> None:
        b64 = "iVBORw0KGgoAAAANSUhEUgAAABQAAAAUCAYAAACNiR0NAAA"
        response = _make_response(next_best_action=f"Check this data: {b64}")
        issues = check_output_not_contaminated("INC-TEST", response)
        assert any(i.check == "base64_contamination" for i in issues)

    def test_email_headers_in_output(self) -> None:
        response = _make_response(next_best_action="From: admin@contoso.com\nTo: user@contoso.com\nCheck VPN")
        issues = check_output_not_contaminated("INC-TEST", response)
        assert any(i.check == "email_header_contamination" for i in issues)

    def test_excessive_whitespace_in_output(self) -> None:
        response = _make_response(next_best_action="Check VPN\n\n\n\n\n\nstatus")
        issues = check_output_not_contaminated("INC-TEST", response)
        assert any(i.check == "whitespace_contamination" for i in issues)

    def test_no_false_positive_on_normal_html_word(self) -> None:
        """Words like 'html' in normal text should not trigger."""
        response = _make_response(next_best_action="The email was in html format")
        issues = check_output_not_contaminated("INC-TEST", response)
        # "html" alone without angle brackets shouldn't trigger
        html_issues = [i for i in issues if i.check == "html_contamination"]
        assert len(html_issues) == 0


class TestCheckClassificationDespiteNoise:
    """Tests for classification correctness validation."""

    def test_correct_classification_no_issues(self) -> None:
        response = _make_response()
        gold = _make_gold()
        issues = check_classification_despite_noise("INC-TEST", response, gold)
        assert len(issues) == 0

    def test_wrong_category_detected(self) -> None:
        response = _make_response(category="Hardware & Peripherals")
        gold = _make_gold(category="Network & Connectivity")
        issues = check_classification_despite_noise("INC-TEST", response, gold)
        assert any(i.check == "category_mismatch" for i in issues)

    def test_wrong_priority_detected(self) -> None:
        response = _make_response(priority="P1")
        gold = _make_gold(priority="P3")
        issues = check_classification_despite_noise("INC-TEST", response, gold)
        assert any(i.check == "priority_mismatch" for i in issues)

    def test_wrong_routing_detected(self) -> None:
        response = _make_response(assigned_team="Security Operations")
        gold = _make_gold(assigned_team="Network Operations")
        issues = check_classification_despite_noise("INC-TEST", response, gold)
        assert any(i.check == "routing_mismatch" for i in issues)

    def test_case_insensitive_match(self) -> None:
        response = _make_response(category="network & connectivity")
        gold = _make_gold(category="Network & Connectivity")
        issues = check_classification_despite_noise("INC-TEST", response, gold)
        assert len(issues) == 0


class TestCheckEnumValuesClean:
    """Tests for enum value cleanliness."""

    def test_clean_values_no_issues(self) -> None:
        issues = check_enum_values_clean("INC-TEST", _make_response())
        assert len(issues) == 0

    def test_category_with_whitespace(self) -> None:
        response = _make_response(category="  Network & Connectivity  ")
        issues = check_enum_values_clean("INC-TEST", response)
        assert any(i.check == "category_whitespace" for i in issues)

    def test_priority_with_whitespace(self) -> None:
        response = _make_response(priority="  P3  ")
        issues = check_enum_values_clean("INC-TEST", response)
        assert any(i.check == "priority_whitespace" for i in issues)

    def test_team_with_whitespace(self) -> None:
        response = _make_response(assigned_team="  Network Operations  ")
        issues = check_enum_values_clean("INC-TEST", response)
        assert any(i.check == "team_whitespace" for i in issues)


class TestValidateDataCleanupResponse:
    """Tests for the combined validation function."""

    def test_clean_response_no_issues(self) -> None:
        response = _make_response()
        gold = _make_gold()
        issues = validate_data_cleanup_response("INC-TEST", response, gold)
        assert len(issues) == 0

    def test_multiple_issues_returned(self) -> None:
        response = _make_response(
            category="Wrong Category",
            next_best_action="<html><body>Check</body></html>",
        )
        gold = _make_gold()
        issues = validate_data_cleanup_response("INC-TEST", response, gold)
        checks = {i.check for i in issues}
        assert "category_mismatch" in checks
        assert "html_contamination" in checks
