# Copyright (c) Microsoft. All rights reserved.
"""Tests for data cleanup evaluation scenarios.

Validates that all data cleanup scenarios:
- Produce valid TicketInput and TriageDecision models
- Have unique ticket IDs
- Use valid enum values from the schemas
- Cover the expected categories of messy data
- Are compatible with the run_eval.py scoring harness
"""

import json

import pytest

from ms.eval.models import TicketInput
from ms.eval.models import TriageDecision
from ms.eval.scenarios.data_cleanup import get_all_data_cleanup_scenarios
from ms.eval.scenarios.data_cleanup import scenario_ansi_terminal_output
from ms.eval.scenarios.data_cleanup import scenario_auto_reply_loop
from ms.eval.scenarios.data_cleanup import scenario_base64_attachment_flood
from ms.eval.scenarios.data_cleanup import scenario_base64_image_in_description
from ms.eval.scenarios.data_cleanup import scenario_binary_hex_dump
from ms.eval.scenarios.data_cleanup import scenario_control_characters
from ms.eval.scenarios.data_cleanup import scenario_corrupted_json
from ms.eval.scenarios.data_cleanup import scenario_csv_tabular_data
from ms.eval.scenarios.data_cleanup import scenario_deeply_nested_java_exception
from ms.eval.scenarios.data_cleanup import scenario_dns_zone_file
from ms.eval.scenarios.data_cleanup import scenario_docker_container_logs
from ms.eval.scenarios.data_cleanup import scenario_double_encoded_html_entities
from ms.eval.scenarios.data_cleanup import scenario_duplicate_ticket_concatenation
from ms.eval.scenarios.data_cleanup import scenario_email_thread_noise
from ms.eval.scenarios.data_cleanup import scenario_empty_description
from ms.eval.scenarios.data_cleanup import scenario_enormous_cc_list
from ms.eval.scenarios.data_cleanup import scenario_excessive_whitespace
from ms.eval.scenarios.data_cleanup import scenario_extremely_long_subject
from ms.eval.scenarios.data_cleanup import scenario_garbled_ocr_text
from ms.eval.scenarios.data_cleanup import scenario_git_diff_in_ticket
from ms.eval.scenarios.data_cleanup import scenario_html_email_body
from ms.eval.scenarios.data_cleanup import scenario_ics_calendar_content
from ms.eval.scenarios.data_cleanup import scenario_json_config_dump
from ms.eval.scenarios.data_cleanup import scenario_kubernetes_pod_yaml
from ms.eval.scenarios.data_cleanup import scenario_markdown_formatted_ticket
from ms.eval.scenarios.data_cleanup import scenario_massive_email_signature
from ms.eval.scenarios.data_cleanup import scenario_minified_code_dump
from ms.eval.scenarios.data_cleanup import scenario_mixed_languages
from ms.eval.scenarios.data_cleanup import scenario_mojibake_encoding
from ms.eval.scenarios.data_cleanup import scenario_multiple_issues_one_ticket
from ms.eval.scenarios.data_cleanup import scenario_nested_quoted_replies
from ms.eval.scenarios.data_cleanup import scenario_packet_capture_text
from ms.eval.scenarios.data_cleanup import scenario_pdf_to_text_artifacts
from ms.eval.scenarios.data_cleanup import scenario_pem_certificate_chain
from ms.eval.scenarios.data_cleanup import scenario_powershell_verbose_output
from ms.eval.scenarios.data_cleanup import scenario_raw_mime_multipart
from ms.eval.scenarios.data_cleanup import scenario_registry_export_dump
from ms.eval.scenarios.data_cleanup import scenario_repeated_content
from ms.eval.scenarios.data_cleanup import scenario_soap_fault_xml
from ms.eval.scenarios.data_cleanup import scenario_special_characters_and_encoding
from ms.eval.scenarios.data_cleanup import scenario_spreadsheet_tab_paste
from ms.eval.scenarios.data_cleanup import scenario_sql_query_dump
from ms.eval.scenarios.data_cleanup import scenario_stack_trace_flood
from ms.eval.scenarios.data_cleanup import scenario_subject_description_mismatch
from ms.eval.scenarios.data_cleanup import scenario_syslog_flood
from ms.eval.scenarios.data_cleanup import scenario_terraform_plan_output
from ms.eval.scenarios.data_cleanup import scenario_unicode_rtl_and_homoglyphs
from ms.eval.scenarios.data_cleanup import scenario_url_heavy_description
from ms.eval.scenarios.data_cleanup import scenario_very_long_email
from ms.eval.scenarios.data_cleanup import scenario_windows_event_log_dump

# ── Schema validation for all scenarios ──────────────────────────────


_ALL_SCENARIOS = get_all_data_cleanup_scenarios()


class TestAllScenariosSchemaCompliance:
    """Verify every data cleanup scenario produces valid models."""

    @pytest.mark.parametrize(
        ("ticket", "gold"),
        _ALL_SCENARIOS,
        ids=[t.ticket_id for t, _ in _ALL_SCENARIOS],
    )
    def test_ticket_is_valid_model(self, ticket: TicketInput, gold: TriageDecision) -> None:
        assert isinstance(ticket, TicketInput)
        assert isinstance(gold, TriageDecision)

    @pytest.mark.parametrize(
        ("ticket", "gold"),
        _ALL_SCENARIOS,
        ids=[t.ticket_id for t, _ in _ALL_SCENARIOS],
    )
    def test_ticket_id_matches(self, ticket: TicketInput, gold: TriageDecision) -> None:
        assert ticket.ticket_id == gold.ticket_id

    @pytest.mark.parametrize(
        ("ticket", "gold"),
        _ALL_SCENARIOS,
        ids=[t.ticket_id for t, _ in _ALL_SCENARIOS],
    )
    def test_gold_has_required_fields(self, ticket: TicketInput, gold: TriageDecision) -> None:
        assert gold.category
        assert gold.priority
        assert gold.assigned_team
        assert isinstance(gold.needs_escalation, bool)
        assert isinstance(gold.missing_information, list)
        assert gold.next_best_action
        assert len(gold.remediation_steps) > 0

    @pytest.mark.parametrize(
        ("ticket", "gold"),
        _ALL_SCENARIOS,
        ids=[t.ticket_id for t, _ in _ALL_SCENARIOS],
    )
    def test_json_serializable(self, ticket: TicketInput, gold: TriageDecision) -> None:
        """Ensure scenarios can be exported to JSON for run_eval.py."""
        ticket_json = json.loads(ticket.model_dump_json())
        gold_json = json.loads(gold.model_dump_json())
        assert ticket_json["ticket_id"] == gold_json["ticket_id"]

    def test_unique_ticket_ids(self) -> None:
        ids = [t.ticket_id for t, _ in _ALL_SCENARIOS]
        assert len(ids) == len(set(ids)), f"Duplicate ticket IDs found: {ids}"

    def test_minimum_scenario_count(self) -> None:
        """Ensure we have a meaningful number of data cleanup scenarios."""
<<<<<<< HEAD
        assert len(_ALL_SCENARIOS) >= 48
=======
        assert len(_ALL_SCENARIOS) >= 38
>>>>>>> users/fde-platform-agent/fde-hiring-test-3/boyevche


# ── Scenario-specific tests ──────────────────────────────────────────


class TestVeryLongEmail:
    """Verify the very long email scenario has appropriate characteristics."""

    def test_description_is_long(self) -> None:
        ticket, _ = scenario_very_long_email()
        assert len(ticket.description) > 5000

    def test_classified_as_network(self) -> None:
        _, gold = scenario_very_long_email()
        assert gold.category == "Network & Connectivity"
        assert gold.assigned_team == "Network Operations"


class TestBase64ImageInDescription:
    """Verify base64 image scenario contains actual base64 data."""

    def test_contains_base64_data_uri(self) -> None:
        ticket, _ = scenario_base64_image_in_description()
        assert "data:image/png;base64," in ticket.description

    def test_classified_as_hardware(self) -> None:
        _, gold = scenario_base64_image_in_description()
        assert gold.category == "Hardware & Peripherals"


class TestHtmlEmailBody:
    """Verify HTML email scenario contains HTML tags."""

    def test_contains_html_tags(self) -> None:
        ticket, _ = scenario_html_email_body()
        assert "<html>" in ticket.description
        assert "</html>" in ticket.description
        assert "<p>" in ticket.description

    def test_classified_as_data_storage(self) -> None:
        _, gold = scenario_html_email_body()
        assert gold.category == "Data & Storage"


class TestExcessiveWhitespace:
    """Verify whitespace scenario has lots of noise characters."""

    def test_contains_excessive_whitespace(self) -> None:
        ticket, _ = scenario_excessive_whitespace()
        whitespace_count = sum(1 for c in ticket.description if c in " \t\n")
        total_count = len(ticket.description)
        assert whitespace_count / total_count > 0.4

    def test_phone_channel(self) -> None:
        ticket, _ = scenario_excessive_whitespace()
        assert ticket.channel == "phone"

    def test_classified_as_hardware(self) -> None:
        _, gold = scenario_excessive_whitespace()
        assert gold.category == "Hardware & Peripherals"


class TestUnicodeRtlAndHomoglyphs:
    """Verify unicode scenario contains adversarial characters."""

    def test_contains_zero_width_spaces(self) -> None:
        ticket, _ = scenario_unicode_rtl_and_homoglyphs()
        assert "\u200b" in ticket.description

    def test_contains_rtl_override(self) -> None:
        ticket, _ = scenario_unicode_rtl_and_homoglyphs()
        assert "\u202e" in ticket.description

    def test_classified_as_access(self) -> None:
        _, gold = scenario_unicode_rtl_and_homoglyphs()
        assert gold.category == "Access & Authentication"


class TestExtremelyLongSubject:
    """Verify long subject scenario has an unusually long subject."""

    def test_subject_is_long(self) -> None:
        ticket, _ = scenario_extremely_long_subject()
        assert len(ticket.subject) > 200

    def test_classified_as_hardware(self) -> None:
        _, gold = scenario_extremely_long_subject()
        assert gold.category == "Hardware & Peripherals"


class TestEmptyDescription:
    """Verify empty description scenario."""

    def test_description_is_empty(self) -> None:
        ticket, _ = scenario_empty_description()
        assert ticket.description == ""

    def test_has_missing_information(self) -> None:
        _, gold = scenario_empty_description()
        assert len(gold.missing_information) >= 2

    def test_classified_as_software(self) -> None:
        _, gold = scenario_empty_description()
        assert gold.category == "Software & Applications"


class TestRepeatedContent:
    """Verify repeated content scenario."""

    def test_has_repeated_phrases(self) -> None:
        ticket, _ = scenario_repeated_content()
        count = ticket.description.count("I need to reset my password.")
        assert count >= 20

    def test_classified_as_access(self) -> None:
        _, gold = scenario_repeated_content()
        assert gold.category == "Access & Authentication"


class TestEmailThreadNoise:
    """Verify email thread noise scenario."""

    def test_contains_forwarded_headers(self) -> None:
        ticket, _ = scenario_email_thread_noise()
        assert "Forwarded message" in ticket.description
        assert "Original message" in ticket.description

    def test_classified_as_data_storage(self) -> None:
        _, gold = scenario_email_thread_noise()
        assert gold.category == "Data & Storage"

    def test_needs_escalation_due_to_repeat(self) -> None:
        _, gold = scenario_email_thread_noise()
        assert gold.needs_escalation is True


class TestMixedLanguages:
    """Verify mixed languages scenario."""

    def test_contains_chinese_characters(self) -> None:
        ticket, _ = scenario_mixed_languages()
        assert any("\u4e00" <= c <= "\u9fff" for c in ticket.description)

    def test_classified_as_network(self) -> None:
        _, gold = scenario_mixed_languages()
        assert gold.category == "Network & Connectivity"


class TestBase64AttachmentFlood:
    """Verify multi-attachment base64 scenario."""

    def test_contains_multiple_base64_blobs(self) -> None:
        ticket, _ = scenario_base64_attachment_flood()
        count = ticket.description.count("data:image/jpeg;base64,")
        assert count >= 5

    def test_classified_as_software(self) -> None:
        _, gold = scenario_base64_attachment_flood()
        assert gold.category == "Software & Applications"


class TestSpecialCharactersAndEncoding:
    """Verify special characters scenario."""

    def test_contains_emoji(self) -> None:
        ticket, _ = scenario_special_characters_and_encoding()
        assert "\U0001f629" in ticket.description or "😩" in ticket.subject

    def test_contains_smart_quotes(self) -> None:
        ticket, _ = scenario_special_characters_and_encoding()
        assert "\u201c" in ticket.description or "\u2019" in ticket.description

    def test_classified_as_data_storage(self) -> None:
        _, gold = scenario_special_characters_and_encoding()
        assert gold.category == "Data & Storage"


# ── New scenario-specific tests ──────────────────────────────────────


class TestCsvTabularData:
    """Verify CSV/tabular data scenario."""

    def test_contains_csv_header(self) -> None:
        ticket, _ = scenario_csv_tabular_data()
        assert "Hostname,IP,Status,CPU,Memory" in ticket.description

    def test_contains_critical_entries(self) -> None:
        ticket, _ = scenario_csv_tabular_data()
        assert "CRITICAL" in ticket.description

    def test_classified_as_hardware(self) -> None:
        _, gold = scenario_csv_tabular_data()
        assert gold.category == "Hardware & Peripherals"
        assert gold.priority == "P1"

    def test_needs_escalation(self) -> None:
        _, gold = scenario_csv_tabular_data()
        assert gold.needs_escalation is True


class TestMassiveEmailSignature:
    """Verify massive email signature scenario."""

    def test_signature_dominates_description(self) -> None:
        ticket, _ = scenario_massive_email_signature()
        # Signature block repeated 3 times should dwarf the one-line issue
        assert len(ticket.description) > 2000

    def test_contains_confidentiality_notice(self) -> None:
        ticket, _ = scenario_massive_email_signature()
        assert "CONFIDENTIALITY NOTICE" in ticket.description

    def test_classified_as_software(self) -> None:
        _, gold = scenario_massive_email_signature()
        assert gold.category == "Software & Applications"


class TestUrlHeavyDescription:
    """Verify URL-heavy description scenario."""

    def test_contains_many_urls(self) -> None:
        ticket, _ = scenario_url_heavy_description()
        url_count = ticket.description.count("https://sharepoint.contoso.com")
        assert url_count >= 8

    def test_contains_error_codes(self) -> None:
        ticket, _ = scenario_url_heavy_description()
        assert "500 Internal Server Error" in ticket.description

    def test_classified_as_software_p1(self) -> None:
        _, gold = scenario_url_heavy_description()
        assert gold.category == "Software & Applications"
        assert gold.priority == "P1"
        assert gold.needs_escalation is True


class TestAnsiTerminalOutput:
    """Verify ANSI terminal output scenario."""

    def test_contains_ansi_escape_codes(self) -> None:
        ticket, _ = scenario_ansi_terminal_output()
        assert "\x1b[" in ticket.description

    def test_contains_error_info(self) -> None:
        ticket, _ = scenario_ansi_terminal_output()
        assert "authentication required" in ticket.description

    def test_classified_as_access(self) -> None:
        _, gold = scenario_ansi_terminal_output()
        assert gold.category == "Access & Authentication"


class TestGarbledOcrText:
    """Verify garbled OCR text scenario."""

    def test_contains_ocr_artifacts(self) -> None:
        ticket, _ = scenario_garbled_ocr_text()
        # OCR artifacts: 0 instead of o, 1 instead of l
        assert "netw0rk" in ticket.description.lower()
        assert "f1oor" in ticket.description.lower()

    def test_classified_as_network(self) -> None:
        _, gold = scenario_garbled_ocr_text()
        assert gold.category == "Network & Connectivity"
        assert gold.priority == "P1"

    def test_needs_escalation(self) -> None:
        _, gold = scenario_garbled_ocr_text()
        assert gold.needs_escalation is True


class TestMultipleIssuesOneTicket:
    """Verify multiple-issues-in-one-ticket scenario."""

    def test_contains_multiple_numbered_issues(self) -> None:
        ticket, _ = scenario_multiple_issues_one_ticket()
        assert "1)" in ticket.description
        assert "5)" in ticket.description

    def test_prioritizes_security_issue(self) -> None:
        _, gold = scenario_multiple_issues_one_ticket()
        assert gold.category == "Security & Compliance"
        assert gold.assigned_team == "Security Operations"

    def test_needs_escalation_for_malware(self) -> None:
        _, gold = scenario_multiple_issues_one_ticket()
        assert gold.needs_escalation is True


class TestMarkdownFormattedTicket:
    """Verify markdown formatted ticket scenario."""

    def test_contains_markdown_headers(self) -> None:
        ticket, _ = scenario_markdown_formatted_ticket()
        assert "# " in ticket.description
        assert "## " in ticket.description

    def test_contains_code_block(self) -> None:
        ticket, _ = scenario_markdown_formatted_ticket()
        assert "```" in ticket.description

    def test_contains_markdown_table(self) -> None:
        ticket, _ = scenario_markdown_formatted_ticket()
        assert "|--------|" in ticket.description

    def test_classified_as_network(self) -> None:
        _, gold = scenario_markdown_formatted_ticket()
        assert gold.category == "Network & Connectivity"


class TestSubjectDescriptionMismatch:
    """Verify subject/description mismatch scenario."""

    def test_subject_references_old_issue(self) -> None:
        ticket, _ = scenario_subject_description_mismatch()
        assert "RESOLVED" in ticket.subject
        assert "printer" in ticket.subject.lower()

    def test_description_has_different_issue(self) -> None:
        ticket, _ = scenario_subject_description_mismatch()
        assert "Salesforce" in ticket.description

    def test_classified_on_description_not_subject(self) -> None:
        _, gold = scenario_subject_description_mismatch()
        assert gold.category == "Software & Applications"
        assert gold.priority == "P1"
        assert gold.needs_escalation is True


# ── New data cleanup scenario tests ──────────────────────────────────


class TestJsonConfigDump:
    """Verify JSON config dump scenario."""

    def test_contains_json_structure(self) -> None:
        ticket, _ = scenario_json_config_dump()
        assert '"appSettings"' in ticket.description
        assert '"connectionString"' in ticket.description

    def test_description_is_long(self) -> None:
        ticket, _ = scenario_json_config_dump()
        assert len(ticket.description) > 1000

    def test_classified_as_software(self) -> None:
        _, gold = scenario_json_config_dump()
        assert gold.category == "Software & Applications"
        assert gold.assigned_team == "Enterprise Applications"


class TestStackTraceFlood:
    """Verify stack trace flood scenario."""

    def test_contains_stack_frames(self) -> None:
        ticket, _ = scenario_stack_trace_flood()
        assert "\tat " in ticket.description
        assert "java.sql.SQLTransientConnectionException" in ticket.description

    def test_description_is_very_long(self) -> None:
        ticket, _ = scenario_stack_trace_flood()
        assert len(ticket.description) > 3000

    def test_classified_as_software_p1(self) -> None:
        _, gold = scenario_stack_trace_flood()
        assert gold.category == "Software & Applications"
        assert gold.priority == "P1"
        assert gold.needs_escalation is True


class TestDoubleEncodedHtmlEntities:
    """Verify double-encoded HTML entities scenario."""

    def test_contains_double_encoded_entities(self) -> None:
        ticket, _ = scenario_double_encoded_html_entities()
        assert "&amp;apos;" in ticket.description
        assert "&amp;quot;" in ticket.description
        assert "&amp;amp;" in ticket.description

    def test_classified_as_access(self) -> None:
        _, gold = scenario_double_encoded_html_entities()
        assert gold.category == "Access & Authentication"
        assert gold.assigned_team == "Identity & Access Management"


class TestAutoReplyLoop:
    """Verify auto-reply loop scenario."""

    def test_contains_repeated_auto_replies(self) -> None:
        ticket, _ = scenario_auto_reply_loop()
        count = ticket.description.count("--- Auto-Reply ---")
        assert count >= 20

    def test_actual_issue_is_present(self) -> None:
        ticket, _ = scenario_auto_reply_loop()
        assert "Accounts Payable" in ticket.description
        assert "external emails" in ticket.description

    def test_classified_as_software_p1(self) -> None:
        _, gold = scenario_auto_reply_loop()
        assert gold.category == "Software & Applications"
        assert gold.priority == "P1"
        assert gold.needs_escalation is True


class TestBinaryHexDump:
    """Verify binary hex dump scenario."""

    def test_contains_hex_dump_format(self) -> None:
        ticket, _ = scenario_binary_hex_dump()
        assert "00000000" in ticket.description
        assert "lsusb" in ticket.description

    def test_classified_as_hardware(self) -> None:
        _, gold = scenario_binary_hex_dump()
        assert gold.category == "Hardware & Peripherals"
        assert gold.assigned_team == "Endpoint Engineering"


class TestControlCharacters:
    """Verify control characters scenario."""

    def test_contains_control_chars(self) -> None:
        ticket, _ = scenario_control_characters()
        assert "\x07" in ticket.description
        assert "\x0c" in ticket.description

    def test_classified_as_network_p1(self) -> None:
        _, gold = scenario_control_characters()
        assert gold.category == "Network & Connectivity"
        assert gold.priority == "P1"
        assert gold.needs_escalation is True


class TestMinifiedCodeDump:
    """Verify minified code dump scenario."""

    def test_contains_minified_code(self) -> None:
        ticket, _ = scenario_minified_code_dump()
        assert "function(e,t)" in ticket.description
        assert "module.exports" in ticket.description

    def test_description_is_very_long(self) -> None:
        ticket, _ = scenario_minified_code_dump()
        assert len(ticket.description) > 2000

    def test_classified_as_software_p1(self) -> None:
        _, gold = scenario_minified_code_dump()
        assert gold.category == "Software & Applications"
        assert gold.priority == "P1"
        assert gold.needs_escalation is True


class TestMojibakeEncoding:
    """Verify mojibake encoding scenario."""

    def test_contains_mojibake_characters(self) -> None:
        ticket, _ = scenario_mojibake_encoding()
        assert "\u00c3" in ticket.description

    def test_mentions_encoding_issue(self) -> None:
        ticket, _ = scenario_mojibake_encoding()
        assert "garbled" in ticket.description

    def test_classified_as_software(self) -> None:
        _, gold = scenario_mojibake_encoding()
        assert gold.category == "Software & Applications"
        assert gold.assigned_team == "Enterprise Applications"


# ── Wave-3 data cleanup scenario tests ───────────────────────────────


class TestWindowsEventLogDump:
    """Verify Windows Event Log dump scenario."""

    def test_contains_event_xml(self) -> None:
        ticket, _ = scenario_windows_event_log_dump()
        assert "<Event xmlns=" in ticket.description

    def test_description_is_long(self) -> None:
        ticket, _ = scenario_windows_event_log_dump()
        assert len(ticket.description) > 3000

    def test_classified_as_hardware_p2(self) -> None:
        _, gold = scenario_windows_event_log_dump()
        assert gold.category == "Hardware & Peripherals"
        assert gold.priority == "P2"
        assert gold.assigned_team == "Endpoint Engineering"


class TestSoapFaultXml:
    """Verify SOAP fault XML scenario."""

    def test_contains_soap_envelope(self) -> None:
        ticket, _ = scenario_soap_fault_xml()
        assert "<soap:Envelope" in ticket.description

    def test_contains_soap_fault(self) -> None:
        ticket, _ = scenario_soap_fault_xml()
        assert "<soap:Fault>" in ticket.description

    def test_classified_as_software_p2(self) -> None:
        _, gold = scenario_soap_fault_xml()
        assert gold.category == "Software & Applications"
        assert gold.priority == "P2"
        assert gold.assigned_team == "Enterprise Applications"


class TestSyslogFlood:
    """Verify syslog flood scenario."""

    def test_contains_syslog_timestamps(self) -> None:
        ticket, _ = scenario_syslog_flood()
        assert "Mar 18 14:" in ticket.description

    def test_description_is_very_long(self) -> None:
        ticket, _ = scenario_syslog_flood()
        assert len(ticket.description) > 5000

    def test_classified_as_data_storage_p1(self) -> None:
        _, gold = scenario_syslog_flood()
        assert gold.category == "Data & Storage"
        assert gold.priority == "P1"
        assert gold.assigned_team == "Data Platform"

    def test_needs_escalation(self) -> None:
        _, gold = scenario_syslog_flood()
        assert gold.needs_escalation is True


class TestDuplicateTicketConcatenation:
    """Verify duplicate ticket concatenation scenario."""

    def test_contains_multiple_submissions(self) -> None:
        ticket, _ = scenario_duplicate_ticket_concatenation()
        count = ticket.description.count("Submitted:")
        assert count >= 3

    def test_classified_as_hardware_p3(self) -> None:
        _, gold = scenario_duplicate_ticket_concatenation()
        assert gold.category == "Hardware & Peripherals"
        assert gold.priority == "P3"
        assert gold.assigned_team == "Endpoint Engineering"


class TestCorruptedJson:
    """Verify corrupted JSON scenario."""

    def test_contains_malformed_json(self) -> None:
        ticket, _ = scenario_corrupted_json()
        assert "{" in ticket.description

    def test_classified_as_software_p1(self) -> None:
        _, gold = scenario_corrupted_json()
        assert gold.category == "Software & Applications"
        assert gold.priority == "P1"
        assert gold.assigned_team == "Enterprise Applications"

    def test_needs_escalation(self) -> None:
        _, gold = scenario_corrupted_json()
        assert gold.needs_escalation is True


class TestRegistryExportDump:
    """Verify Windows registry export dump scenario."""

    def test_contains_registry_paths(self) -> None:
        ticket, _ = scenario_registry_export_dump()
        has_hklm = "HKEY_LOCAL_MACHINE" in ticket.description
        has_hkcu = "HKEY_CURRENT_USER" in ticket.description
        assert has_hklm or has_hkcu

    def test_description_is_long(self) -> None:
        ticket, _ = scenario_registry_export_dump()
        assert len(ticket.description) > 2000

    def test_classified_as_software_p3(self) -> None:
        _, gold = scenario_registry_export_dump()
        assert gold.category == "Software & Applications"
        assert gold.priority == "P3"
        assert gold.assigned_team == "Endpoint Engineering"


class TestPowershellVerboseOutput:
    """Verify PowerShell verbose output scenario."""

    def test_contains_powershell_columns(self) -> None:
        ticket, _ = scenario_powershell_verbose_output()
        assert "Status" in ticket.description
        assert "Name" in ticket.description

    def test_classified_as_data_storage_p1(self) -> None:
        _, gold = scenario_powershell_verbose_output()
        assert gold.category == "Data & Storage"
        assert gold.priority == "P1"
        assert gold.assigned_team == "Data Platform"

    def test_needs_escalation(self) -> None:
        _, gold = scenario_powershell_verbose_output()
        assert gold.needs_escalation is True


class TestIcsCalendarContent:
    """Verify ICS calendar content scenario."""

    def test_contains_vcalendar_markers(self) -> None:
        ticket, _ = scenario_ics_calendar_content()
        assert "BEGIN:VCALENDAR" in ticket.description

    def test_classified_as_software_p3(self) -> None:
        _, gold = scenario_ics_calendar_content()
        assert gold.category == "Software & Applications"
        assert gold.priority == "P3"
        assert gold.assigned_team == "Enterprise Applications"


class TestPdfToTextArtifacts:
    """Verify PDF-to-text artifacts scenario."""

    def test_description_contains_garbled_text(self) -> None:
        ticket, _ = scenario_pdf_to_text_artifacts()
        # PDF extraction artifacts produce garbled/jumbled column text
        assert len(ticket.description) > 200

    def test_classified_as_software_p2(self) -> None:
        _, gold = scenario_pdf_to_text_artifacts()
        assert gold.category == "Software & Applications"
        assert gold.priority == "P2"
        assert gold.assigned_team == "Enterprise Applications"


class TestEnormousCcList:
    """Verify enormous CC list scenario."""

    def test_contains_many_email_addresses(self) -> None:
        ticket, _ = scenario_enormous_cc_list()
        count = ticket.description.count("@contoso.com")
        assert count >= 5

    def test_description_is_long(self) -> None:
        ticket, _ = scenario_enormous_cc_list()
        assert len(ticket.description) > 2000

    def test_classified_as_software_p2(self) -> None:
        _, gold = scenario_enormous_cc_list()
        assert gold.category == "Software & Applications"
        assert gold.priority == "P2"
        assert gold.assigned_team == "Enterprise Applications"


class TestNestedQuotedReplies:
    """Verify nested quoted replies scenario."""

    def test_contains_deep_quoting(self) -> None:
        ticket, _ = scenario_nested_quoted_replies()
        assert "> > >" in ticket.description

    def test_classified_as_access_p2(self) -> None:
        _, gold = scenario_nested_quoted_replies()
        assert gold.category == "Access & Authentication"
        assert gold.priority == "P2"
        assert gold.assigned_team == "Identity & Access Management"


class TestSqlQueryDump:
    """Verify SQL query dump scenario."""

    def test_contains_sql_keywords(self) -> None:
        ticket, _ = scenario_sql_query_dump()
        desc = ticket.description
        has_sql = any(kw in desc for kw in ("SELECT", "FROM", "JOIN", "WHERE"))
        assert has_sql

    def test_classified_as_data_storage_p2(self) -> None:
        _, gold = scenario_sql_query_dump()
        assert gold.category == "Data & Storage"
        assert gold.priority == "P2"
        assert gold.assigned_team == "Data Platform"
<<<<<<< HEAD


# ── New comprehensive scenario tests (INC-DC-5001 through INC-DC-5010) ──


class TestDockerContainerLogs:
    """Verify Docker container log scenario has realistic log output."""

    def test_contains_log_timestamps(self) -> None:
        ticket, _ = scenario_docker_container_logs()
        assert "2026-03" in ticket.description

    def test_contains_oom_error(self) -> None:
        ticket, _ = scenario_docker_container_logs()
        assert "OutOfMemoryError" in ticket.description

    def test_contains_restart_attempts(self) -> None:
        ticket, _ = scenario_docker_container_logs()
        assert "restart" in ticket.description.lower()

    def test_classified_as_software_p1(self) -> None:
        _, gold = scenario_docker_container_logs()
        assert gold.category == "Software & Applications"
        assert gold.priority == "P1"
        assert gold.assigned_team == "Enterprise Applications"
        assert gold.needs_escalation is False


class TestKubernetesPodYaml:
    """Verify Kubernetes pod YAML scenario has K8s resource output."""

    def test_contains_pod_describe_output(self) -> None:
        ticket, _ = scenario_kubernetes_pod_yaml()
        assert "kubectl describe" in ticket.description or "Namespace:" in ticket.description

    def test_contains_crashloopbackoff(self) -> None:
        ticket, _ = scenario_kubernetes_pod_yaml()
        assert "CrashLoopBackOff" in ticket.description

    def test_classified_as_software_p2(self) -> None:
        _, gold = scenario_kubernetes_pod_yaml()
        assert gold.category == "Software & Applications"
        assert gold.priority == "P2"
        assert gold.assigned_team == "Enterprise Applications"


class TestTerraformPlanOutput:
    """Verify Terraform plan scenario has IaC plan output."""

    def test_contains_terraform_actions(self) -> None:
        ticket, _ = scenario_terraform_plan_output()
        assert "Terraform will perform" in ticket.description

    def test_contains_destroy_action(self) -> None:
        ticket, _ = scenario_terraform_plan_output()
        assert "DESTROYED" in ticket.description

    def test_description_is_long(self) -> None:
        ticket, _ = scenario_terraform_plan_output()
        assert len(ticket.description) > 1500

    def test_classified_as_network_p1_escalated(self) -> None:
        _, gold = scenario_terraform_plan_output()
        assert gold.category == "Network & Connectivity"
        assert gold.priority == "P1"
        assert gold.assigned_team == "Network Operations"
        assert gold.needs_escalation is True


class TestGitDiffInTicket:
    """Verify git diff scenario has unified diff format."""

    def test_contains_diff_markers(self) -> None:
        ticket, _ = scenario_git_diff_in_ticket()
        assert "diff --git" in ticket.description
        assert "---" in ticket.description
        assert "+++" in ticket.description

    def test_classified_as_access_p2(self) -> None:
        _, gold = scenario_git_diff_in_ticket()
        assert gold.category == "Access & Authentication"
        assert gold.priority == "P2"
        assert gold.assigned_team == "Identity & Access Management"
        assert gold.needs_escalation is False


class TestPemCertificateChain:
    """Verify PEM certificate scenario has cert data."""

    def test_contains_pem_markers(self) -> None:
        ticket, _ = scenario_pem_certificate_chain()
        assert "-----BEGIN CERTIFICATE-----" in ticket.description
        assert "-----END CERTIFICATE-----" in ticket.description

    def test_description_is_long(self) -> None:
        ticket, _ = scenario_pem_certificate_chain()
        assert len(ticket.description) > 1000

    def test_classified_as_security_p1_escalated(self) -> None:
        _, gold = scenario_pem_certificate_chain()
        assert gold.category == "Security & Compliance"
        assert gold.priority == "P1"
        assert gold.assigned_team == "Security Operations"
        assert gold.needs_escalation is True


class TestRawMimeMultipart:
    """Verify raw MIME multipart scenario has email source."""

    def test_contains_mime_boundary(self) -> None:
        ticket, _ = scenario_raw_mime_multipart()
        assert "boundary=" in ticket.description
        assert "Content-Type:" in ticket.description

    def test_contains_quoted_printable(self) -> None:
        ticket, _ = scenario_raw_mime_multipart()
        assert "quoted-printable" in ticket.description

    def test_classified_as_software_p3(self) -> None:
        _, gold = scenario_raw_mime_multipart()
        assert gold.category == "Software & Applications"
        assert gold.priority == "P3"
        assert gold.assigned_team == "Enterprise Applications"


class TestDnsZoneFile:
    """Verify DNS zone file scenario has zone records."""

    def test_contains_zone_records(self) -> None:
        ticket, _ = scenario_dns_zone_file()
        desc = ticket.description
        assert "$TTL" in desc or "IN  A" in desc or "IN  SOA" in desc

    def test_contains_corrupted_records(self) -> None:
        ticket, _ = scenario_dns_zone_file()
        assert "0.0.0.0" in ticket.description

    def test_classified_as_network_p2(self) -> None:
        _, gold = scenario_dns_zone_file()
        assert gold.category == "Network & Connectivity"
        assert gold.priority == "P2"
        assert gold.assigned_team == "Network Operations"
        assert gold.needs_escalation is False


class TestPacketCaptureText:
    """Verify packet capture scenario has tcpdump-like output."""

    def test_contains_tcp_flags(self) -> None:
        ticket, _ = scenario_packet_capture_text()
        assert "Flags [" in ticket.description

    def test_contains_retransmission(self) -> None:
        ticket, _ = scenario_packet_capture_text()
        assert "Retransmission" in ticket.description

    def test_classified_as_network_p2(self) -> None:
        _, gold = scenario_packet_capture_text()
        assert gold.category == "Network & Connectivity"
        assert gold.priority == "P2"
        assert gold.assigned_team == "Network Operations"
        assert gold.needs_escalation is False


class TestDeeplyNestedJavaException:
    """Verify deeply nested Java exception has multi-level Caused by chain."""

    def test_contains_caused_by_chain(self) -> None:
        ticket, _ = scenario_deeply_nested_java_exception()
        caused_count = ticket.description.count("Caused by:")
        assert caused_count >= 4, f"Expected ≥4 'Caused by:' levels, got {caused_count}"

    def test_contains_hikari_pool_exhaustion(self) -> None:
        ticket, _ = scenario_deeply_nested_java_exception()
        assert "HikariPool" in ticket.description
        assert "Active: 50" in ticket.description

    def test_classified_as_data_storage_p1_escalated(self) -> None:
        _, gold = scenario_deeply_nested_java_exception()
        assert gold.category == "Data & Storage"
        assert gold.priority == "P1"
        assert gold.assigned_team == "Data Platform"
        assert gold.needs_escalation is True


class TestSpreadsheetTabPaste:
    """Verify spreadsheet tab paste scenario has tabular data."""

    def test_contains_tab_separated_data(self) -> None:
        ticket, _ = scenario_spreadsheet_tab_paste()
        assert "\t" in ticket.description

    def test_contains_employee_data(self) -> None:
        ticket, _ = scenario_spreadsheet_tab_paste()
        assert "Employee ID" in ticket.description

    def test_classified_as_access_p3(self) -> None:
        _, gold = scenario_spreadsheet_tab_paste()
        assert gold.category == "Access & Authentication"
        assert gold.priority == "P3"
        assert gold.assigned_team == "Identity & Access Management"

=======
>>>>>>> users/fde-platform-agent/fde-hiring-test-3/boyevche
