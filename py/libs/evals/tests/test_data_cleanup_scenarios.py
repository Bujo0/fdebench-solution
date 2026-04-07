# Copyright (c) Microsoft. All rights reserved.
"""Tests for data cleanup evaluation scenarios.

Validates that:
1. All data cleanup scenarios are well-formed (valid ScenarioDefinitions)
2. Gold answers use valid enum values from the constrained vocabulary
3. Ticket IDs are unique across all scenarios
4. Scenarios cover the expected range of data quality issues
"""

from ms.evals_core.constants import ALL_CATEGORIES
from ms.evals_core.constants import ALL_MISSING_INFO_FIELDS
from ms.evals_core.constants import ALL_PRIORITIES
from ms.evals_core.constants import ALL_TEAMS
from ms.evals_core.scenarios.data_cleanup import get_scenarios


class TestDataCleanupScenarios:
    """Verify that all data cleanup scenarios are well-formed."""

    def test_returns_scenarios(self) -> None:
        scenarios = get_scenarios()
        assert len(scenarios) > 0, "No data cleanup scenarios returned"

    def test_all_scenario_ids_unique(self) -> None:
        scenarios = get_scenarios()
        ids = [s.scenario_id for s in scenarios]
        assert len(ids) == len(set(ids)), f"Duplicate IDs: {[x for x in ids if ids.count(x) > 1]}"

    def test_all_scenarios_have_required_fields(self) -> None:
        scenarios = get_scenarios()
        for s in scenarios:
            assert s.subject, f"{s.scenario_id}: empty subject"
            assert s.description, f"{s.scenario_id}: empty description"
            assert s.reporter_name, f"{s.scenario_id}: empty reporter_name"
            assert s.reporter_email, f"{s.scenario_id}: empty reporter_email"
            assert s.reporter_department, f"{s.scenario_id}: empty reporter_department"
            assert s.next_best_action, f"{s.scenario_id}: empty next_best_action"
            assert len(s.remediation_steps) > 0, f"{s.scenario_id}: no remediation_steps"

    def test_all_scenarios_have_tags(self) -> None:
        scenarios = get_scenarios()
        for s in scenarios:
            assert len(s.tags) > 0, f"{s.scenario_id}: no tags"
            assert "data-cleanup" in s.tags, f"{s.scenario_id}: missing 'data-cleanup' tag"

    def test_scenarios_convert_to_scenario_model(self) -> None:
        scenarios = get_scenarios()
        for idx, s in enumerate(scenarios):
            scenario = s.to_scenario(f"INC-TEST-{idx:04d}")
            assert scenario.ticket.ticket_id == f"INC-TEST-{idx:04d}"
            assert scenario.gold.ticket_id == f"INC-TEST-{idx:04d}"
            assert scenario.gold.category is not None
            assert scenario.gold.priority is not None
            assert scenario.gold.assigned_team is not None

    def test_known_scenario_ids(self) -> None:
        """Verify expected scenario IDs exist."""
        scenarios = get_scenarios()
        ids = {s.scenario_id for s in scenarios}
        expected = {f"DC-{i:03d}" for i in range(1, 265)}
        assert expected.issubset(ids), f"Missing IDs: {expected - ids}"

    def test_minimum_scenario_count(self) -> None:
        """Data cleanup should have at least 264 scenarios."""
        scenarios = get_scenarios()
        assert len(scenarios) >= 264, f"Expected >= 264 DC scenarios, got {len(scenarios)}"

    def test_gold_categories_valid(self) -> None:
        """All gold categories must be from the valid vocabulary."""
        for s in get_scenarios():
            assert s.category.value in ALL_CATEGORIES, f"{s.scenario_id}: invalid gold category '{s.category}'"

    def test_gold_priorities_valid(self) -> None:
        """All gold priorities must be from the valid vocabulary."""
        for s in get_scenarios():
            assert s.priority.value in ALL_PRIORITIES, f"{s.scenario_id}: invalid gold priority '{s.priority}'"

    def test_gold_teams_valid(self) -> None:
        """All gold teams must be from the valid vocabulary."""
        for s in get_scenarios():
            assert s.team.value in ALL_TEAMS, f"{s.scenario_id}: invalid gold team '{s.team}'"

    def test_gold_missing_info_valid(self) -> None:
        """All gold missing_info items must be from the valid vocabulary."""
        for s in get_scenarios():
            for item in s.missing_info:
                assert item.value in ALL_MISSING_INFO_FIELDS, f"{s.scenario_id}: invalid missing info '{item}'"

    def test_covers_key_cleanup_categories(self) -> None:
        """Verify that key data cleanup noise types are covered."""
        scenarios = get_scenarios()
        all_tags = set()
        for s in scenarios:
            all_tags.update(s.tags)

        expected_tags = {
            "long-email",
            "base64",
            "quoted-replies",
            "garbled-text",
            "inline-code",
            "monitoring-alerts",
            "mime-encoded",
            "no-linebreaks",
            "rtf-markup",
            "conflicting-replies",
            "monitoring-metrics",
            "pdf-conversion",
            "massive-cc-list",
            "ocr-layout",
            "speech-to-text",
            "newsletter",
            "pdf-inline",
            "css-noise",
            "xml-soap",
            "sql-dump",
            "markdown-artifacts",
            "multilingual-disclaimer",
            "json-payload",
            "excessive-whitespace",
            "corrupted-headers",
            "vcalendar-noise",
            "hex-dump",
            "double-encoded-html",
            "chat-transcript",
            "registry-dump",
            "http-headers",
            "cid-references",
            "escaped-json",
            "tsv-data",
            "vcard-data",
            "cron-output",
            "concatenated-tickets",
            "all-caps",
            "long-subject",
            "container-logs",
            "k8s-output",
            "emoji-subject",
            "powershell-output",
            "view-source",
            "rtl-text",
            "form-artifacts",
            "event-log",
            "windows-events",
            "packet-capture",
            "tcpdump",
            "ci-pipeline",
            "github-actions",
            "tracking-urls",
            "calendar-forward",
            "ics-spam",
            "spreadsheet-paste",
            "misaligned-columns",
            "ansi-codes",
            "control-characters",
            "multi-topic",
            "rambling",
            "pdf-embed",
            "inline-binary",
            "screenshot-heavy",
            "autocorrect",
            "typos",
            "mobile-input",
            "voicemail",
            "accent-noise",
            "zero-width-chars",
            "invisible-unicode",
            "auto-translation",
            "translation-artifacts",
            "css-dark-mode",
            "mass-forward",
            "jwt-token",
            "oauth-dump",
            "auth-trace",
            "yaml-config",
            "docker-compose",
            "git-diff",
            "code-paste",
            "multiple-screenshots",
            "data-uri-flood",
            "terse-message",
            "minimal-context",
            "bidi-text",
            "rtl-ltr-mixed",
            "arabic-english",
            "unicode-control",
            "graphql-introspection",
            "bsod-minidump",
            "webhook-payload",
            "powershell-streams",
            "docker-compose-flood",
            "ocr-number-corruption",
            "quoted-printable-encoding",
            "servicenow-audit-trail",
            "bloomberg-terminal-paste",
            "excel-formula-artifacts",
            "sql-query-paste",
            "tabular-noise",
            "diagram-text",
            "ascii-art",
            "bsod-dump",
            "crash-stack",
            "k8s-describe",
            "container-events",
            "url-noise",
            "latex-notation",
            "math-formulas",
            "arm-template",
            "json-config-dump",
            "merge-conflict-markers",
            "git-artifacts",
            "macos-crash-report",
            "crash-reporter",
            "csv-data-inline",
            "long-urls",
            "tracking-parameters",
            "rtf-conversion",
            "document-artifacts",
            "auto-reply-chain",
            "ooo-noise",
            "svg-inline",
            "cross-threaded",
            "interleaved-issues",
            "buried-content",
            "env-var-dump",
            "config-noise",
            "git-diff-noise",
            "merge-conflicts",
            "yaml-config-dump",
            "kubernetes",
            "very-long-email",
            "base64-flood",
            "base64-encoded-text",
            "giant-signature",
            "deep-quoting",
            "mojibake-severe",
            "code-switching",
            "url-spam",
            "email-metadata",
            "csv-injection",
            "pgp-signed-email",
            "zalgo-unicode",
            "combining-diacritics",
            "deep-nested-json",
            "sql-output-noise",
            "smime-signature",
            "empty-body",
            "mobile-signature-only",
            "jira-notification",
            "transition-history-noise",
            "registry-export",
            "reg-file-noise",
            "deep-traceback",
            "long-url",
            "query-param-overflow",
            "base64-binary-inline",
            "iac-template-dump",
            "git-blame-output",
            "source-code-noise",
            "base64-image-flood",
            "ooo-stack",
            "legal-disclaimer",
            "multilingual-footer",
            "teams-transcript",
            "chat-paste",
            "http-dump",
            "response-headers",
            "inline-screenshots",
            "multi-ticket-reference",
            "thread-confusion",
            "servicedesk-template",
            "auto-notification",
            "mojibake-corruption",
            "encoding-mismatch",
            "soap-fault-dump",
            "xml-response",
            "html-table-noise",
            "inline-css-dump",
            "extremely-verbose-buried",
            "rambling-email",
            "embedded-eml",
            "rfc822-headers",
            "ocr-scan-noise",
            "recognition-errors",
            "winrm-transcript",
            "remote-session-dump",
            # Tags from DC-261..DC-264
            "enormous-cc-bcc",
            "header-overload",
            "corrupted-base64",
            "invalid-encoding",
            "deep-html-tables",
            "nested-markup",
            "zero-width-joiners",
            "mixed-direction",
            "alert-flood",
            "monitoring-noise",
        }
        assert expected_tags.issubset(all_tags), f"Missing cleanup tags: {expected_tags - all_tags}"
