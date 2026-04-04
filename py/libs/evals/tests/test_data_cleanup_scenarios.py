"""Tests for data cleanup evaluation scenarios.

Validates that all data cleanup scenarios are well-formed, have consistent
ticket IDs between input and gold, use valid enum values, and contain the
expected adversarial properties.
"""

import pytest

from ms.libs.evals.models.enums import ScenarioTag
from ms.libs.evals.scenarios.data_cleanup import get_data_cleanup_scenarios


@pytest.fixture
def scenarios():
    return get_data_cleanup_scenarios()


class TestDataCleanupScenarioStructure:
    """Validate structural correctness of all data cleanup scenarios."""

    def test_all_scenarios_have_correct_tag(self, scenarios) -> None:
        for scenario in scenarios:
            assert scenario.tag == ScenarioTag.DATA_CLEANUP, (
                f"{scenario.ticket.ticket_id}: expected tag DATA_CLEANUP, got {scenario.tag}"
            )

    def test_ticket_ids_match_between_input_and_gold(self, scenarios) -> None:
        for scenario in scenarios:
            assert scenario.ticket.ticket_id == scenario.gold.ticket_id, (
                f"Ticket ID mismatch: {scenario.ticket.ticket_id} != {scenario.gold.ticket_id}"
            )

    def test_all_ticket_ids_unique(self, scenarios) -> None:
        ids = [s.ticket.ticket_id for s in scenarios]
        assert len(ids) == len(set(ids)), f"Duplicate ticket IDs found: {ids}"

    def test_all_test_names_unique(self, scenarios) -> None:
        names = [s.test_name for s in scenarios]
        assert len(names) == len(set(names)), f"Duplicate test names: {names}"

    def test_all_scenarios_have_descriptions(self, scenarios) -> None:
        for scenario in scenarios:
            assert len(scenario.test_description) > 20, (
                f"{scenario.ticket.ticket_id}: test_description too short"
            )

    def test_all_gold_have_remediation_steps(self, scenarios) -> None:
        for scenario in scenarios:
            assert len(scenario.gold.remediation_steps) >= 1, (
                f"{scenario.ticket.ticket_id}: gold must have at least 1 remediation step"
            )

    def test_all_gold_have_next_best_action(self, scenarios) -> None:
        for scenario in scenarios:
            assert len(scenario.gold.next_best_action) > 10, (
                f"{scenario.ticket.ticket_id}: next_best_action too short"
            )

    def test_scenario_count(self, scenarios) -> None:
        assert len(scenarios) >= 15, f"Expected at least 15 data cleanup scenarios, got {len(scenarios)}"

    def test_ticket_ids_in_9000_range(self, scenarios) -> None:
        for scenario in scenarios:
            num = int(scenario.ticket.ticket_id.split("-")[1])
            assert 9001 <= num <= 9099, (
                f"{scenario.ticket.ticket_id}: data cleanup IDs should be INC-9001 to INC-9099"
            )


class TestDataCleanupAdversarialProperties:
    """Validate that scenarios actually test the claimed adversarial properties."""

    def test_very_long_email_is_long(self, scenarios) -> None:
        scenario = next(s for s in scenarios if s.test_name == "very_long_email")
        assert len(scenario.ticket.description) > 3000, (
            "very_long_email description should be > 3000 chars"
        )

    def test_base64_image_contains_base64(self, scenarios) -> None:
        scenario = next(s for s in scenarios if s.test_name == "base64_image_in_description")
        assert "base64," in scenario.ticket.description
        assert "iVBORw0KGgo" in scenario.ticket.description

    def test_html_email_contains_html_tags(self, scenarios) -> None:
        scenario = next(s for s in scenarios if s.test_name == "html_email_body")
        desc = scenario.ticket.description
        assert "<html>" in desc
        assert "<style" in desc
        assert "<table>" in desc

    def test_email_thread_has_multiple_messages(self, scenarios) -> None:
        scenario = next(s for s in scenarios if s.test_name == "email_thread_chain")
        desc = scenario.ticket.description
        assert desc.count("Original Message") >= 3

    def test_excessive_whitespace_has_whitespace(self, scenarios) -> None:
        scenario = next(s for s in scenarios if s.test_name == "excessive_whitespace")
        desc = scenario.ticket.description
        assert desc.count("\n\n\n") >= 3
        assert "\t\t\t" in desc

    def test_unicode_has_special_chars(self, scenarios) -> None:
        scenario = next(s for s in scenarios if s.test_name == "unicode_special_chars")
        desc = scenario.ticket.description
        assert "🚨" in desc
        assert "☕" in desc
        assert "ü" in desc or "ø" in desc

    def test_repeated_content_has_repetition(self, scenarios) -> None:
        scenario = next(s for s in scenarios if s.test_name == "repeated_content")
        desc = scenario.ticket.description
        # The repeated block should appear many times
        assert desc.count("Please help") >= 5

    def test_encoding_artifacts_has_mojibake(self, scenarios) -> None:
        scenario = next(s for s in scenarios if s.test_name == "encoding_artifacts")
        desc = scenario.ticket.description
        # Should contain garbled Unicode sequences from mojibake
        assert "\u00e2" in desc or "\u00c3" in desc

    def test_minimal_description_is_minimal(self, scenarios) -> None:
        scenario = next(s for s in scenarios if s.test_name == "minimal_description")
        assert len(scenario.ticket.description) < 20
        assert len(scenario.ticket.subject) < 10

    def test_attachment_spam_has_many_attachments(self, scenarios) -> None:
        scenario = next(s for s in scenarios if s.test_name == "attachment_spam")
        assert len(scenario.ticket.attachments) >= 50

    def test_log_dump_has_many_log_lines(self, scenarios) -> None:
        scenario = next(s for s in scenarios if s.test_name == "log_dump_description")
        lines = scenario.ticket.description.split("\n")
        log_lines = [line for line in lines if "ERROR" in line]
        assert len(log_lines) >= 50

    def test_monitoring_alert_has_metadata(self, scenarios) -> None:
        scenario = next(s for s in scenarios if s.test_name == "auto_generated_monitoring_alert")
        desc = scenario.ticket.description
        assert "AUTOMATED ALERT" in desc
        assert "Subscription:" in desc

    def test_multi_language_has_cjk(self, scenarios) -> None:
        scenario = next(s for s in scenarios if s.test_name == "multi_language_ticket")
        desc = scenario.ticket.description
        # Check for Chinese characters
        has_chinese = any("\u4e00" <= c <= "\u9fff" for c in desc)
        # Check for Japanese characters
        has_japanese = any("\u3040" <= c <= "\u30ff" for c in desc)
        assert has_chinese, "Should contain Chinese characters"
        assert has_japanese, "Should contain Japanese characters"

    def test_url_heavy_has_many_urls(self, scenarios) -> None:
        scenario = next(s for s in scenarios if s.test_name == "url_heavy_description")
        desc = scenario.ticket.description
        url_count = desc.count("https://")
        assert url_count >= 10

    def test_legal_disclaimer_has_low_signal_ratio(self, scenarios) -> None:
        scenario = next(s for s in scenarios if s.test_name == "legal_disclaimer_email")
        desc = scenario.ticket.description
        # The actual request is very short compared to the disclaimers
        first_line = desc.split("\n")[0]
        assert len(first_line) < 100
        assert len(desc) > 1500
