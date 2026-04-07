# Copyright (c) Microsoft. All rights reserved.
"""Tests for data cleanup evaluation scenarios.

Validates that all data cleanup scenarios are well-formed, have valid
gold answers, and cover the expected edge cases.
"""

import json

from evals.models import Category
from evals.models import EvalScenario
from evals.models import MissingInfoField
from evals.models import Priority
from evals.models import ScenarioSuite
from evals.models import ScenarioTag
from evals.models import Team
from evals.validators.data_cleanup import validate_no_base64_leak
from evals.validators.data_cleanup import validate_no_email_headers
from evals.validators.data_cleanup import validate_no_html_leak
from evals.validators.data_cleanup import validate_no_log_dump
from evals.validators.data_cleanup import validate_response_for_scenario
from evals.validators.schema import validate_triage_decision


class TestDataCleanupSuiteBuild:
    """Verify the suite builds successfully and has expected structure."""

    def test_suite_builds_without_error(self, data_cleanup_suite: ScenarioSuite):
        assert data_cleanup_suite is not None

    def test_suite_has_correct_type(self, data_cleanup_suite: ScenarioSuite):
        assert data_cleanup_suite.suite_type == "data_cleanup"

    def test_suite_has_minimum_scenarios(self, data_cleanup_suite: ScenarioSuite):
        assert len(data_cleanup_suite.scenarios) >= 15

    def test_all_scenario_ids_unique(self, data_cleanup_suite: ScenarioSuite):
        ids = [s.scenario_id for s in data_cleanup_suite.scenarios]
        assert len(ids) == len(set(ids))

    def test_all_ticket_ids_unique(self, data_cleanup_suite: ScenarioSuite):
        ids = [s.ticket.ticket_id for s in data_cleanup_suite.scenarios]
        assert len(ids) == len(set(ids))

    def test_all_scenario_ids_start_with_dc(self, data_cleanup_suite: ScenarioSuite):
        for scenario in data_cleanup_suite.scenarios:
            assert scenario.scenario_id.startswith("DC-"), f"{scenario.scenario_id} should start with DC-"

    def test_all_ticket_ids_start_with_inc(self, data_cleanup_suite: ScenarioSuite):
        for scenario in data_cleanup_suite.scenarios:
            assert scenario.ticket.ticket_id.startswith("INC-"), (
                f"{scenario.ticket.ticket_id} should start with INC-"
            )

    def test_ticket_id_matches_gold(self, data_cleanup_suite: ScenarioSuite):
        for scenario in data_cleanup_suite.scenarios:
            assert scenario.ticket.ticket_id == scenario.gold.ticket_id

    def test_all_scenarios_tagged_data_cleanup(self, data_cleanup_suite: ScenarioSuite):
        for scenario in data_cleanup_suite.scenarios:
            assert ScenarioTag.DATA_CLEANUP in scenario.tags, (
                f"{scenario.scenario_id} should be tagged data_cleanup"
            )


class TestDataCleanupGoldAnswers:
    """Verify all gold answers are valid triage decisions."""

    def test_all_gold_pass_schema_validation(self, data_cleanup_suite: ScenarioSuite):
        for scenario in data_cleanup_suite.scenarios:
            violations = validate_triage_decision(scenario.gold)
            assert violations == [], f"{scenario.scenario_id}: {violations}"

    def test_all_gold_categories_valid(self, data_cleanup_suite: ScenarioSuite):
        valid = {c.value for c in Category}
        for scenario in data_cleanup_suite.scenarios:
            assert scenario.gold.category in valid, (
                f"{scenario.scenario_id}: {scenario.gold.category} not in valid categories"
            )

    def test_all_gold_priorities_valid(self, data_cleanup_suite: ScenarioSuite):
        valid = {p.value for p in Priority}
        for scenario in data_cleanup_suite.scenarios:
            assert scenario.gold.priority in valid

    def test_all_gold_teams_valid(self, data_cleanup_suite: ScenarioSuite):
        valid = {t.value for t in Team}
        for scenario in data_cleanup_suite.scenarios:
            assert scenario.gold.assigned_team in valid

    def test_all_gold_missing_info_valid(self, data_cleanup_suite: ScenarioSuite):
        valid = {f.value for f in MissingInfoField}
        for scenario in data_cleanup_suite.scenarios:
            for item in scenario.gold.missing_information:
                assert item in valid, f"{scenario.scenario_id}: {item} not in valid missing info"

    def test_all_gold_have_remediation_steps(self, data_cleanup_suite: ScenarioSuite):
        for scenario in data_cleanup_suite.scenarios:
            assert len(scenario.gold.remediation_steps) >= 1, (
                f"{scenario.scenario_id}: gold must have at least one remediation step"
            )

    def test_all_gold_have_next_best_action(self, data_cleanup_suite: ScenarioSuite):
        for scenario in data_cleanup_suite.scenarios:
            assert len(scenario.gold.next_best_action) > 10, (
                f"{scenario.scenario_id}: next_best_action should be substantive"
            )


class TestDataCleanupGoldSelfValidation:
    """Gold answers should pass their own data cleanup validators."""

    def test_gold_responses_pass_data_cleanup_validation(self, data_cleanup_suite: ScenarioSuite):
        for scenario in data_cleanup_suite.scenarios:
            violations = validate_response_for_scenario(scenario, scenario.gold.model_dump())
            assert violations == [], f"{scenario.scenario_id}: {violations}"


class TestDataCleanupJsonExport:
    """Verify export to JSON is valid and matches run_eval.py expectations."""

    def test_tickets_json_is_list(self, data_cleanup_suite: ScenarioSuite):
        tickets = data_cleanup_suite.get_tickets()
        assert isinstance(tickets, list)

    def test_gold_json_is_list(self, data_cleanup_suite: ScenarioSuite):
        golds = data_cleanup_suite.get_gold_answers()
        assert isinstance(golds, list)

    def test_tickets_json_serializable(self, data_cleanup_suite: ScenarioSuite):
        tickets = data_cleanup_suite.get_tickets()
        serialized = json.dumps(tickets)
        assert len(serialized) > 0

    def test_gold_json_serializable(self, data_cleanup_suite: ScenarioSuite):
        golds = data_cleanup_suite.get_gold_answers()
        serialized = json.dumps(golds)
        assert len(serialized) > 0

    def test_tickets_and_gold_same_count(self, data_cleanup_suite: ScenarioSuite):
        tickets = data_cleanup_suite.get_tickets()
        golds = data_cleanup_suite.get_gold_answers()
        assert len(tickets) == len(golds)

    def test_tickets_and_gold_matching_ids(self, data_cleanup_suite: ScenarioSuite):
        tickets = data_cleanup_suite.get_tickets()
        golds = data_cleanup_suite.get_gold_answers()
        ticket_ids = [t["ticket_id"] for t in tickets]
        gold_ids = [g["ticket_id"] for g in golds]
        assert ticket_ids == gold_ids


class TestDataCleanupScenarioCoverage:
    """Verify scenarios cover the expected range of edge cases."""

    def test_has_long_content_scenarios(self, data_cleanup_suite: ScenarioSuite):
        tagged = [s for s in data_cleanup_suite.scenarios if ScenarioTag.LONG_CONTENT in s.tags]
        assert len(tagged) >= 3, "Should have at least 3 long content scenarios"

    def test_has_encoding_scenarios(self, data_cleanup_suite: ScenarioSuite):
        tagged = [s for s in data_cleanup_suite.scenarios if ScenarioTag.ENCODING in s.tags]
        assert len(tagged) >= 2, "Should have at least 2 encoding scenarios"

    def test_has_noise_scenarios(self, data_cleanup_suite: ScenarioSuite):
        tagged = [s for s in data_cleanup_suite.scenarios if ScenarioTag.NOISE in s.tags]
        assert len(tagged) >= 5, "Should have at least 5 noise scenarios"

    def test_has_malformed_scenarios(self, data_cleanup_suite: ScenarioSuite):
        tagged = [s for s in data_cleanup_suite.scenarios if ScenarioTag.MALFORMED in s.tags]
        assert len(tagged) >= 2, "Should have at least 2 malformed scenarios"

    def test_covers_multiple_categories(self, data_cleanup_suite: ScenarioSuite):
        categories = {s.gold.category for s in data_cleanup_suite.scenarios}
        assert len(categories) >= 5, f"Should cover at least 5 categories, got {len(categories)}: {categories}"

    def test_covers_multiple_priorities(self, data_cleanup_suite: ScenarioSuite):
        priorities = {s.gold.priority for s in data_cleanup_suite.scenarios}
        assert len(priorities) >= 3, f"Should cover at least 3 priorities, got {priorities}"

    def test_has_not_a_support_ticket_scenario(self, data_cleanup_suite: ScenarioSuite):
        not_support = [s for s in data_cleanup_suite.scenarios if s.gold.category == Category.NOT_SUPPORT]
        assert len(not_support) >= 2, "Should have at least 2 'Not a Support Ticket' scenarios"

    def test_has_escalation_required_scenario(self, data_cleanup_suite: ScenarioSuite):
        escalated = [s for s in data_cleanup_suite.scenarios if s.gold.needs_escalation]
        assert len(escalated) >= 1, "Should have at least 1 scenario requiring escalation"


class TestDataCleanupSpecificScenarios:
    """Test specific edge case scenarios for correctness."""

    def _find_scenario(self, suite: ScenarioSuite, scenario_id: str) -> EvalScenario:
        for s in suite.scenarios:
            if s.scenario_id == scenario_id:
                return s
        msg = f"Scenario {scenario_id} not found"
        raise ValueError(msg)

    def test_long_email_has_real_issue(self, data_cleanup_suite: ScenarioSuite):
        scenario = self._find_scenario(data_cleanup_suite, "DC-001")
        assert len(scenario.ticket.description) > 5000, "Long email should be 5000+ chars"
        assert scenario.gold.category == Category.NETWORK

    def test_base64_image_ticket_has_binary_data(self, data_cleanup_suite: ScenarioSuite):
        scenario = self._find_scenario(data_cleanup_suite, "DC-002")
        assert "base64" in scenario.ticket.description
        assert scenario.gold.category == Category.SOFTWARE

    def test_html_email_has_tags(self, data_cleanup_suite: ScenarioSuite):
        scenario = self._find_scenario(data_cleanup_suite, "DC-003")
        assert "<html>" in scenario.ticket.description or "<div" in scenario.ticket.description
        assert scenario.gold.category == Category.DATA

    def test_signature_only_is_not_support(self, data_cleanup_suite: ScenarioSuite):
        scenario = self._find_scenario(data_cleanup_suite, "DC-004")
        assert scenario.gold.category == Category.NOT_SUPPORT
        assert scenario.gold.assigned_team == Team.NONE

    def test_bounce_back_is_not_support(self, data_cleanup_suite: ScenarioSuite):
        scenario = self._find_scenario(data_cleanup_suite, "DC-005")
        assert scenario.gold.category == Category.NOT_SUPPORT
        assert "MAILER-DAEMON" in scenario.ticket.reporter.name

    def test_log_dump_is_production_issue(self, data_cleanup_suite: ScenarioSuite):
        scenario = self._find_scenario(data_cleanup_suite, "DC-006")
        assert scenario.gold.priority == Priority.P1
        assert scenario.gold.needs_escalation is True

    def test_empty_description_uses_subject(self, data_cleanup_suite: ScenarioSuite):
        scenario = self._find_scenario(data_cleanup_suite, "DC-008")
        assert scenario.ticket.description == ""
        assert scenario.gold.category == Category.HARDWARE

    def test_phone_transcript_extracts_issue(self, data_cleanup_suite: ScenarioSuite):
        scenario = self._find_scenario(data_cleanup_suite, "DC-009")
        assert scenario.ticket.channel == "phone"
        assert scenario.gold.category == Category.HARDWARE


class TestDataCleanupValidators:
    """Test the data cleanup validators themselves."""

    def test_base64_validator_catches_leak(self):
        text = "Do this: " + "A" * 60 + " then that"
        violations = validate_no_base64_leak(text)
        assert len(violations) > 0

    def test_base64_validator_allows_short_text(self):
        violations = validate_no_base64_leak("Check the SAP server configuration")
        assert violations == []

    def test_html_validator_catches_tags(self):
        violations = validate_no_html_leak("Try <script>alert(1)</script> to test")
        assert len(violations) > 0

    def test_html_validator_allows_clean_text(self):
        violations = validate_no_html_leak("Check the server status and restart if needed")
        assert violations == []

    def test_log_validator_catches_dump(self):
        log_text = "\n".join(
            f"2026-03-17T09:{i:02d}:00.000Z ERROR [prod] Connection failed" for i in range(5)
        )
        violations = validate_no_log_dump(log_text)
        assert len(violations) > 0

    def test_log_validator_allows_few_lines(self):
        violations = validate_no_log_dump("Check error code 0x80180014 in the logs")
        assert violations == []

    def test_email_header_validator_catches_headers(self):
        text = "From: user@contoso.com\nTo: admin@contoso.com\nSubject: Test"
        violations = validate_no_email_headers(text)
        assert len(violations) > 0

    def test_email_header_validator_allows_clean_text(self):
        violations = validate_no_email_headers("Contact the user for more information")
        assert violations == []
