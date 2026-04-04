# Copyright (c) Microsoft. All rights reserved.
"""Tests for evaluation dataset integrity.

Validates that all datasets conform to the expected schemas:
- All tickets have valid fields and enum values
- All gold answers reference valid categories, teams, priorities, and missing info
- Ticket IDs match between tickets and gold answers
- No duplicate ticket IDs within a dataset
"""

import pytest

from ms.evals_core.constants import Category
from ms.evals_core.constants import Channel
from ms.evals_core.constants import MissingInfoField
from ms.evals_core.constants import Priority
from ms.evals_core.constants import Team
from ms.evals_core.eval_datasets.data_cleanup import DATA_CLEANUP_DATASET
from ms.evals_core.eval_datasets.responsible_ai import RESPONSIBLE_AI_DATASET
from ms.evals_core.eval_models import EvalDataset

_ALL_DATASETS = [
    pytest.param(DATA_CLEANUP_DATASET, id="data_cleanup"),
    pytest.param(RESPONSIBLE_AI_DATASET, id="responsible_ai"),
]


@pytest.mark.parametrize("dataset", _ALL_DATASETS)
class TestDatasetIntegrity:
    """Verify structural integrity of evaluation datasets."""

    def test_has_cases(self, dataset: EvalDataset) -> None:
        assert len(dataset.cases) > 0, "Dataset must contain at least one case"

    def test_no_duplicate_ticket_ids(self, dataset: EvalDataset) -> None:
        ids = [case.ticket.ticket_id for case in dataset.cases]
        assert len(ids) == len(set(ids)), f"Duplicate ticket IDs found: {[i for i in ids if ids.count(i) > 1]}"

    def test_ticket_ids_match_gold(self, dataset: EvalDataset) -> None:
        for case in dataset.cases:
            assert case.ticket.ticket_id == case.gold.ticket_id, (
                f"Ticket ID mismatch: ticket={case.ticket.ticket_id}, gold={case.gold.ticket_id}"
            )

    def test_ticket_ids_follow_pattern(self, dataset: EvalDataset) -> None:
        for case in dataset.cases:
            tid = case.ticket.ticket_id
            assert tid.startswith("INC-"), f"Ticket ID must start with 'INC-': {tid}"

    def test_tickets_have_content(self, dataset: EvalDataset) -> None:
        for case in dataset.cases:
            ticket = case.ticket
            assert len(ticket.subject.strip()) > 0, f"{ticket.ticket_id}: subject must not be empty"
            assert len(ticket.description.strip()) > 0, f"{ticket.ticket_id}: description must not be empty"

    def test_reporters_valid(self, dataset: EvalDataset) -> None:
        for case in dataset.cases:
            reporter = case.ticket.reporter
            assert len(reporter.name.strip()) > 0, f"{case.ticket.ticket_id}: reporter name must not be empty"
            assert "@" in reporter.email, f"{case.ticket.ticket_id}: reporter email must contain @"
            assert len(reporter.department.strip()) > 0, f"{case.ticket.ticket_id}: department must not be empty"

    def test_channel_values_valid(self, dataset: EvalDataset) -> None:
        valid_channels = {c.value for c in Channel}
        for case in dataset.cases:
            assert case.ticket.channel in valid_channels, (
                f"{case.ticket.ticket_id}: invalid channel {case.ticket.channel!r}"
            )

    def test_gold_categories_valid(self, dataset: EvalDataset) -> None:
        valid_categories = {c.value for c in Category}
        for case in dataset.cases:
            assert case.gold.category in valid_categories, (
                f"{case.gold.ticket_id}: invalid category {case.gold.category!r}"
            )

    def test_gold_priorities_valid(self, dataset: EvalDataset) -> None:
        valid_priorities = {p.value for p in Priority}
        for case in dataset.cases:
            assert case.gold.priority in valid_priorities, (
                f"{case.gold.ticket_id}: invalid priority {case.gold.priority!r}"
            )

    def test_gold_teams_valid(self, dataset: EvalDataset) -> None:
        valid_teams = {t.value for t in Team}
        for case in dataset.cases:
            assert case.gold.assigned_team in valid_teams, (
                f"{case.gold.ticket_id}: invalid team {case.gold.assigned_team!r}"
            )

    def test_gold_missing_info_valid(self, dataset: EvalDataset) -> None:
        valid_fields = {m.value for m in MissingInfoField}
        for case in dataset.cases:
            for field in case.gold.missing_information:
                assert field in valid_fields, f"{case.gold.ticket_id}: invalid missing_info field {field!r}"

    def test_gold_has_next_best_action(self, dataset: EvalDataset) -> None:
        for case in dataset.cases:
            assert len(case.gold.next_best_action.strip()) > 0, (
                f"{case.gold.ticket_id}: next_best_action must not be empty"
            )

    def test_gold_has_remediation_steps(self, dataset: EvalDataset) -> None:
        for case in dataset.cases:
            assert len(case.gold.remediation_steps) > 0, f"{case.gold.ticket_id}: remediation_steps must not be empty"
            for step in case.gold.remediation_steps:
                assert len(step.strip()) > 0, f"{case.gold.ticket_id}: remediation step must not be empty"

    def test_cases_have_tags(self, dataset: EvalDataset) -> None:
        for case in dataset.cases:
            assert len(case.tags) > 0, f"{case.ticket.ticket_id}: must have at least one tag"

    def test_cases_have_description(self, dataset: EvalDataset) -> None:
        for case in dataset.cases:
            assert len(case.description.strip()) > 0, f"{case.ticket.ticket_id}: must have a description"

    def test_not_a_support_ticket_routes_to_none(self, dataset: EvalDataset) -> None:
        """If category is 'Not a Support Ticket', team must be 'None'."""
        for case in dataset.cases:
            if case.gold.category == Category.NOT_SUPPORT:
                assert case.gold.assigned_team == Team.NONE, (
                    f"{case.gold.ticket_id}: 'Not a Support Ticket' must route to 'None', "
                    f"got {case.gold.assigned_team!r}"
                )

    def test_json_export_roundtrip(self, dataset: EvalDataset) -> None:
        """Tickets and golds export to valid dicts."""
        tickets = dataset.tickets()
        golds = dataset.golds()
        assert len(tickets) == len(dataset.cases)
        assert len(golds) == len(dataset.cases)
        for ticket_dict in tickets:
            assert "ticket_id" in ticket_dict
            assert "subject" in ticket_dict
            assert "description" in ticket_dict
        for gold_dict in golds:
            assert "ticket_id" in gold_dict
            assert "category" in gold_dict
            assert "priority" in gold_dict
            assert "assigned_team" in gold_dict


class TestDataCleanupSpecific:
    """Data cleanup dataset-specific validations."""

    def test_has_30_cases(self) -> None:
        assert len(DATA_CLEANUP_DATASET.cases) == 30

    def test_covers_expected_scenarios(self) -> None:
        all_tags = set()
        for case in DATA_CLEANUP_DATASET.cases:
            all_tags.update(case.tags)
        # Verify key scenarios are covered
        expected_scenarios = [
            "long_content",
            "base64",
            "html",
            "emoji",
            "duplicated_text",
            "long_subject",
            "mojibake",
            "email_headers",
            "whitespace",
            "url_heavy",
            "tabular_data",
            "phone_transcription",
            "mixed_language",
            "auto_reply",
            "container_logs",
            "xml_payload",
            "json_payload",
            "git_diff",
            "invisible_unicode",
            "bidi_text",
            "ansi_codes",
            "markdown_artifacts",
            "spreadsheet_paste",
            "yaml_config",
            "jwt_token",
            "auto_translation",
            "voicemail_transcript",
            "css_noise",
            "concatenated_issues",
        ]
        for scenario in expected_scenarios:
            matching = [t for t in all_tags if scenario in t]
            assert len(matching) > 0, f"Missing scenario tag containing '{scenario}'"


class TestResponsibleAISpecific:
    """Responsible AI dataset-specific validations."""

    def test_has_30_cases(self) -> None:
        assert len(RESPONSIBLE_AI_DATASET.cases) == 30

    def test_covers_expected_scenarios(self) -> None:
        all_tags = set()
        for case in RESPONSIBLE_AI_DATASET.cases:
            all_tags.update(case.tags)
        expected_scenarios = [
            "jailbreak",
            "prompt_injection",
            "social_engineering",
            "offensive_content",
            "prompt_extraction",
            "malicious",
            "priority_manipulation",
            "phishing",
            "ceo_fraud",
            "timing_pressure",
            "fake_approval_chain",
            "sql_injection",
            "vulnerability_exploit",
            "phishing_creation",
            "stalking_concern",
            "ransomware_threat",
            "deepfake_transcript",
            "bundled_requests",
            "audit_disable",
            "invisible_injection",
            "mass_data_export",
            "gdpr_pretext",
            "multi_vector",
        ]
        for scenario in expected_scenarios:
            matching = [t for t in all_tags if scenario in t]
            assert len(matching) > 0, f"Missing scenario tag containing '{scenario}'"

    def test_adversarial_non_support_has_escalation(self) -> None:
        """Non-support adversarial tickets should generally require escalation."""
        not_support_cases = [
            case for case in RESPONSIBLE_AI_DATASET.cases if case.gold.category == Category.NOT_SUPPORT
        ]
        assert len(not_support_cases) > 0, "Expected some NOT_SUPPORT cases in RAI dataset"
        for case in not_support_cases:
            assert case.gold.needs_escalation is True, (
                f"{case.gold.ticket_id}: adversarial NOT_SUPPORT ticket should require escalation"
            )
