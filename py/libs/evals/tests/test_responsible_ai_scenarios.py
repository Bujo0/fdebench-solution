# Copyright (c) Microsoft. All rights reserved.
"""Tests for responsible AI evaluation scenarios.

Validates that:
1. All responsible AI scenarios are well-formed
2. Gold answers have valid enum values where set
3. Gold answers don't contain unsafe content
4. Scenarios cover the expected range of adversarial patterns
"""

import pytest

from ms.evals_core.constants import ALL_CATEGORIES
from ms.evals_core.constants import ALL_MISSING_INFO_FIELDS
from ms.evals_core.constants import ALL_PRIORITIES
from ms.evals_core.constants import ALL_TEAMS
from ms.evals_core.framework.models.scenario import EvalScenario


class TestResponsibleAIScenariosStructure:
    """Validate scenario collection is well-formed."""

    def test_scenarios_not_empty(self, responsible_ai_scenarios: list[EvalScenario]) -> None:
        assert len(responsible_ai_scenarios) >= 15, "Expected at least 15 responsible AI scenarios"

    def test_unique_scenario_ids(self, responsible_ai_scenarios: list[EvalScenario]) -> None:
        ids = [s.scenario_id for s in responsible_ai_scenarios]
        assert len(ids) == len(set(ids)), f"Duplicate scenario IDs found: {ids}"

    def test_unique_ticket_ids(self, responsible_ai_scenarios: list[EvalScenario]) -> None:
        ids = [s.ticket.ticket_id for s in responsible_ai_scenarios]
        assert len(ids) == len(set(ids)), f"Duplicate ticket IDs found: {ids}"

    def test_all_categorized_as_responsible_ai(self, responsible_ai_scenarios: list[EvalScenario]) -> None:
        for s in responsible_ai_scenarios:
            assert s.category == "responsible_ai", (
                f"{s.scenario_id}: expected category='responsible_ai', got {s.category!r}"
            )


class TestResponsibleAIGoldAnswers:
    """Validate gold answers use valid enum values where set."""

    @pytest.fixture(autouse=True)
    def _load_scenarios(self, responsible_ai_scenarios: list[EvalScenario]) -> None:
        self.scenarios = [s for s in responsible_ai_scenarios if s.expected_triage is not None]

    @pytest.mark.xfail(reason="Known data quality issues in generated scenarios (e.g. 'Hardware & Equipment')")
    def test_gold_categories_valid(self) -> None:
        for s in self.scenarios:
            assert s.expected_triage is not None
            cat = s.expected_triage.category
            if cat is not None:
                assert cat in ALL_CATEGORIES, f"{s.scenario_id}: invalid gold category {cat!r}"

    def test_gold_priorities_valid(self) -> None:
        for s in self.scenarios:
            assert s.expected_triage is not None
            pri = s.expected_triage.priority
            if pri is not None:
                assert pri in ALL_PRIORITIES, f"{s.scenario_id}: invalid gold priority {pri!r}"

    @pytest.mark.xfail(reason="Known data quality issues in generated scenarios (e.g. 'IAM')")
    def test_gold_teams_valid(self) -> None:
        for s in self.scenarios:
            assert s.expected_triage is not None
            team = s.expected_triage.assigned_team
            if team is not None:
                assert team in ALL_TEAMS, f"{s.scenario_id}: invalid gold team {team!r}"

    def test_gold_missing_info_valid(self) -> None:
        for s in self.scenarios:
            assert s.expected_triage is not None
            if s.expected_triage.missing_information is not None:
                for item in s.expected_triage.missing_information:
                    assert item in ALL_MISSING_INFO_FIELDS, (
                        f"{s.scenario_id}: invalid missing info item {item!r}"
                    )


class TestResponsibleAIGoldNeverComplies:
    """Verify gold answers don't comply with adversarial requests."""

    @pytest.fixture(autouse=True)
    def _load_scenarios(self, responsible_ai_scenarios: list[EvalScenario]) -> None:
        self.scenarios = responsible_ai_scenarios

    def test_no_gold_leaks_credentials(self) -> None:
        """Gold answers must never include actual passwords or API keys."""
        credential_fragments = ["password:", "apikey:", "secret:", "bearer ", "-----begin"]
        for s in self.scenarios:
            if s.expected_triage is None:
                continue
            all_text = _collect_expected_text(s.expected_triage.model_dump())
            for frag in credential_fragments:
                assert frag not in all_text.lower(), (
                    f"{s.scenario_id}: gold answer contains credential-like content: {frag!r}"
                )

    def test_no_gold_reveals_system_config(self) -> None:
        """Gold answers must not reveal AI model names, prompts, or configuration."""
        config_fragments = ["gpt-4", "gpt-3", "claude", "system prompt", "temperature=", "max_tokens="]
        for s in self.scenarios:
            if s.expected_triage is None:
                continue
            all_text = _collect_expected_text(s.expected_triage.model_dump())
            for frag in config_fragments:
                assert frag not in all_text.lower(), (
                    f"{s.scenario_id}: gold answer reveals system config: {frag!r}"
                )


class TestResponsibleAICoverage:
    """Validate scenarios cover the expected range of adversarial patterns."""

    def test_covers_prompt_injection(self, responsible_ai_scenarios: list[EvalScenario]) -> None:
        injection = [
            s
            for s in responsible_ai_scenarios
            if "ignore" in s.ticket.description.lower() and "instruction" in s.ticket.description.lower()
        ]
        assert len(injection) >= 1, "Expected at least one prompt injection scenario"

    def test_covers_jailbreak(self, responsible_ai_scenarios: list[EvalScenario]) -> None:
        jailbreak = [s for s in responsible_ai_scenarios if "dan" in s.ticket.description.lower()]
        assert len(jailbreak) >= 1, "Expected at least one jailbreak scenario"

    def test_covers_social_engineering(self, responsible_ai_scenarios: list[EvalScenario]) -> None:
        social_eng = [
            s
            for s in responsible_ai_scenarios
            if "password" in s.ticket.description.lower() and "personal" in s.ticket.description.lower()
        ]
        assert len(social_eng) >= 1, "Expected at least one social engineering scenario"

    def test_covers_harmful_content_request(self, responsible_ai_scenarios: list[EvalScenario]) -> None:
        harmful = [
            s
            for s in responsible_ai_scenarios
            if "threatening" in s.ticket.description.lower() or "harmful" in s.description.lower()
        ]
        assert len(harmful) >= 1, "Expected at least one harmful content request scenario"

    def test_covers_pii_extraction(self, responsible_ai_scenarios: list[EvalScenario]) -> None:
        pii = [
            s
            for s in responsible_ai_scenarios
            if "social security" in s.ticket.description.lower() or "bank account" in s.ticket.description.lower()
        ]
        assert len(pii) >= 1, "Expected at least one PII extraction scenario"

    def test_covers_authority_impersonation(self, responsible_ai_scenarios: list[EvalScenario]) -> None:
        impersonation = [s for s in responsible_ai_scenarios if "ceo" in s.ticket.description.lower()]
        assert len(impersonation) >= 1, "Expected at least one authority impersonation scenario"

    def test_covers_data_exfiltration(self, responsible_ai_scenarios: list[EvalScenario]) -> None:
        exfil = [
            s
            for s in responsible_ai_scenarios
            if "external" in s.ticket.description.lower() and "copy" in s.ticket.description.lower()
        ]
        assert len(exfil) >= 1, "Expected at least one data exfiltration scenario"

    def test_covers_emotional_manipulation(self, responsible_ai_scenarios: list[EvalScenario]) -> None:
        emotional = [
            s
            for s in responsible_ai_scenarios
            if "desperate" in s.ticket.description.lower() or "begging" in s.ticket.description.lower()
        ]
        assert len(emotional) >= 1, "Expected at least one emotional manipulation scenario"


def _collect_expected_text(expected: dict[str, object]) -> str:
    """Concatenate all text content from an expected triage dict."""
    parts: list[str] = []
    for field in ("category", "assigned_team"):
        val = expected.get(field)
        if isinstance(val, str):
            parts.append(val)
    missing = expected.get("missing_information")
    if isinstance(missing, list):
        for item in missing:
            if isinstance(item, str):
                parts.append(item)
    return " ".join(parts)
