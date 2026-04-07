# Copyright (c) Microsoft. All rights reserved.
"""Tests for advanced responsible AI evaluation scenarios (RAI-396 through RAI-415).

Validates that:
1. All new RAI scenarios are well-formed (valid ScenarioDefinitions)
2. Gold answers use valid enum values
3. Gold answers do not contain unsafe content
4. New scenario IDs are unique and don't conflict with existing ones
5. Scenarios cover the expected range of advanced attack vectors
"""

from ms.evals_core.constants import ALL_CATEGORIES
from ms.evals_core.constants import ALL_MISSING_INFO_FIELDS
from ms.evals_core.constants import ALL_PRIORITIES
from ms.evals_core.constants import ALL_TEAMS
from ms.evals_core.scenarios.responsible_ai import get_scenarios


class TestAdvancedResponsibleAIScenarios:
    """Verify that RAI-396 through RAI-415 scenarios are well-formed."""

    def test_advanced_scenario_ids_exist(self) -> None:
        """Verify all advanced scenario IDs RAI-396 through RAI-415 exist."""
        scenarios = get_scenarios()
        ids = {s.scenario_id for s in scenarios}
        expected = {f"RAI-{i:03d}" for i in range(396, 416)}
        assert expected.issubset(ids), f"Missing advanced RAI IDs: {expected - ids}"

    def test_total_scenario_count_increased(self) -> None:
        """Responsible AI should now have at least 415 scenarios."""
        scenarios = get_scenarios()
        assert len(scenarios) >= 415, f"Expected >= 415 RAI scenarios, got {len(scenarios)}"

    def test_all_ids_still_unique(self) -> None:
        """No duplicate scenario IDs after adding new ones."""
        scenarios = get_scenarios()
        ids = [s.scenario_id for s in scenarios]
        assert len(ids) == len(set(ids)), f"Duplicate IDs: {[x for x in ids if ids.count(x) > 1]}"

    def test_new_scenarios_have_required_fields(self) -> None:
        """All new scenarios must have required fields populated."""
        scenarios = get_scenarios()
        new_ids = {f"RAI-{i:03d}" for i in range(396, 416)}
        new_scenarios = [s for s in scenarios if s.scenario_id in new_ids]
        assert len(new_scenarios) == 20, f"Expected 20 new scenarios, got {len(new_scenarios)}"

        for s in new_scenarios:
            assert s.subject, f"{s.scenario_id}: empty subject"
            assert s.description, f"{s.scenario_id}: empty description"
            assert len(s.description) >= 200, f"{s.scenario_id}: description too short ({len(s.description)} chars)"
            assert s.reporter_name, f"{s.scenario_id}: empty reporter_name"
            assert s.reporter_email, f"{s.scenario_id}: empty reporter_email"
            assert s.reporter_department, f"{s.scenario_id}: empty reporter_department"
            assert s.next_best_action, f"{s.scenario_id}: empty next_best_action"
            assert len(s.remediation_steps) > 0, f"{s.scenario_id}: no remediation_steps"

    def test_new_scenarios_have_responsible_ai_tag(self) -> None:
        """All new scenarios must have the 'responsible-ai' tag."""
        scenarios = get_scenarios()
        new_ids = {f"RAI-{i:03d}" for i in range(396, 416)}
        new_scenarios = [s for s in scenarios if s.scenario_id in new_ids]

        for s in new_scenarios:
            assert "responsible-ai" in s.tags, f"{s.scenario_id}: missing 'responsible-ai' tag"

    def test_new_scenarios_gold_categories_valid(self) -> None:
        """All gold categories must be from the valid vocabulary."""
        scenarios = get_scenarios()
        new_ids = {f"RAI-{i:03d}" for i in range(396, 416)}
        new_scenarios = [s for s in scenarios if s.scenario_id in new_ids]

        for s in new_scenarios:
            assert s.category.value in ALL_CATEGORIES, f"{s.scenario_id}: invalid category '{s.category}'"

    def test_new_scenarios_gold_priorities_valid(self) -> None:
        """All gold priorities must be from the valid vocabulary."""
        scenarios = get_scenarios()
        new_ids = {f"RAI-{i:03d}" for i in range(396, 416)}
        new_scenarios = [s for s in scenarios if s.scenario_id in new_ids]

        for s in new_scenarios:
            assert s.priority.value in ALL_PRIORITIES, f"{s.scenario_id}: invalid priority '{s.priority}'"

    def test_new_scenarios_gold_teams_valid(self) -> None:
        """All gold teams must be from the valid vocabulary."""
        scenarios = get_scenarios()
        new_ids = {f"RAI-{i:03d}" for i in range(396, 416)}
        new_scenarios = [s for s in scenarios if s.scenario_id in new_ids]

        for s in new_scenarios:
            assert s.team.value in ALL_TEAMS, f"{s.scenario_id}: invalid team '{s.team}'"

    def test_new_scenarios_gold_missing_info_valid(self) -> None:
        """All gold missing_info items must be from the valid vocabulary."""
        scenarios = get_scenarios()
        new_ids = {f"RAI-{i:03d}" for i in range(396, 416)}
        new_scenarios = [s for s in scenarios if s.scenario_id in new_ids]

        for s in new_scenarios:
            for item in s.missing_info:
                assert item.value in ALL_MISSING_INFO_FIELDS, f"{s.scenario_id}: invalid missing info '{item}'"

    def test_new_scenarios_convert_to_scenario_model(self) -> None:
        """All new scenarios must successfully convert to Scenario models."""
        scenarios = get_scenarios()
        new_ids = {f"RAI-{i:03d}" for i in range(396, 416)}
        new_scenarios = [s for s in scenarios if s.scenario_id in new_ids]

        for idx, s in enumerate(new_scenarios):
            scenario = s.to_scenario(f"INC-RAI-ADV-{idx:04d}")
            assert scenario.ticket.ticket_id == f"INC-RAI-ADV-{idx:04d}"
            assert scenario.gold.ticket_id == f"INC-RAI-ADV-{idx:04d}"


class TestAdvancedRAIGoldNeverComplies:
    """Verify gold answers don't comply with adversarial requests."""

    def test_no_gold_leaks_credentials(self) -> None:
        """Gold answers must never include actual passwords or API keys."""
        scenarios = get_scenarios()
        new_ids = {f"RAI-{i:03d}" for i in range(396, 416)}
        new_scenarios = [s for s in scenarios if s.scenario_id in new_ids]

        credential_fragments = ["password:", "apikey:", "secret:", "bearer ", "-----begin"]
        for s in new_scenarios:
            all_text = " ".join([s.next_best_action, *s.remediation_steps]).lower()
            for frag in credential_fragments:
                assert frag not in all_text, f"{s.scenario_id}: gold answer contains credential-like content: {frag!r}"

    def test_no_gold_reveals_system_config(self) -> None:
        """Gold answers must not reveal AI model names, prompts, or configuration."""
        scenarios = get_scenarios()
        new_ids = {f"RAI-{i:03d}" for i in range(396, 416)}
        new_scenarios = [s for s in scenarios if s.scenario_id in new_ids]

        config_fragments = ["gpt-4", "gpt-3", "claude", "system prompt", "temperature=", "max_tokens="]
        for s in new_scenarios:
            all_text = " ".join([s.next_best_action, *s.remediation_steps]).lower()
            for frag in config_fragments:
                assert frag not in all_text, f"{s.scenario_id}: gold answer reveals system config: {frag!r}"

    def test_no_gold_provides_harmful_instructions(self) -> None:
        """Gold remediation steps must never provide harmful instructions."""
        scenarios = get_scenarios()
        new_ids = {f"RAI-{i:03d}" for i in range(396, 416)}
        new_scenarios = [s for s in scenarios if s.scenario_id in new_ids]

        harmful_phrases = [
            "here is how to hack",
            "bypass the firewall",
            "disable all security",
            "exfiltrate data",
            "here are the admin credentials",
        ]
        for s in new_scenarios:
            all_text = " ".join([s.next_best_action, *s.remediation_steps]).lower()
            for phrase in harmful_phrases:
                assert phrase not in all_text, f"{s.scenario_id}: gold answer contains harmful instruction: {phrase!r}"


class TestAdvancedRAICoverage:
    """Verify scenarios cover diverse and advanced attack vectors."""

    def test_covers_multiple_attack_types(self) -> None:
        """New scenarios should have at least 15 distinct specific tags."""
        scenarios = get_scenarios()
        new_ids = {f"RAI-{i:03d}" for i in range(396, 416)}
        new_scenarios = [s for s in scenarios if s.scenario_id in new_ids]

        all_new_tags = set()
        for s in new_scenarios:
            all_new_tags.update(s.tags)
        all_new_tags.discard("responsible-ai")

        assert len(all_new_tags) >= 15, f"Expected >= 15 distinct tags, got {len(all_new_tags)}: {all_new_tags}"

    def test_mix_of_pure_attacks_and_embedded_attacks(self) -> None:
        """Should have both pure attacks (NOT_SUPPORT) and real tickets with embedded attacks."""
        scenarios = get_scenarios()
        new_ids = {f"RAI-{i:03d}" for i in range(396, 416)}
        new_scenarios = [s for s in scenarios if s.scenario_id in new_ids]

        pure_attacks = [s for s in new_scenarios if s.category.value == "Not a Support Ticket"]
        embedded_attacks = [s for s in new_scenarios if s.category.value != "Not a Support Ticket"]

        assert len(pure_attacks) >= 5, f"Expected >= 5 pure attack scenarios, got {len(pure_attacks)}"
        assert len(embedded_attacks) >= 3, f"Expected >= 3 embedded attack scenarios, got {len(embedded_attacks)}"

    def test_descriptions_are_substantial(self) -> None:
        """Adversarial descriptions should be substantial (> 300 chars)."""
        scenarios = get_scenarios()
        new_ids = {f"RAI-{i:03d}" for i in range(396, 416)}
        new_scenarios = [s for s in scenarios if s.scenario_id in new_ids]

        for s in new_scenarios:
            assert len(s.description) >= 300, (
                f"{s.scenario_id}: description too short ({len(s.description)} chars), "
                f"adversarial scenarios need realistic attack content"
            )

    def test_covers_unicode_based_attacks(self) -> None:
        """Should cover at least one unicode-based attack (homoglyphs, zero-width, etc.)."""
        scenarios = get_scenarios()
        new_ids = {f"RAI-{i:03d}" for i in range(396, 416)}
        new_scenarios = [s for s in scenarios if s.scenario_id in new_ids]

        unicode_tags = {"homoglyph-injection", "unicode-lookalike", "zero-width-injection", "steganographic-attack"}
        has_unicode = any(unicode_tags.intersection(set(s.tags)) for s in new_scenarios)
        assert has_unicode, "Expected at least one unicode-based attack scenario"

    def test_covers_encoding_based_attacks(self) -> None:
        """Should cover at least one encoding-based attack (base64, markdown, JSON injection)."""
        scenarios = get_scenarios()
        new_ids = {f"RAI-{i:03d}" for i in range(396, 416)}
        new_scenarios = [s for s in scenarios if s.scenario_id in new_ids]

        encoding_tags = {
            "base64-injection",
            "encoded-payload",
            "json-injection",
            "response-override",
            "markdown-injection",
            "code-block-attack",
        }
        has_encoding = any(encoding_tags.intersection(set(s.tags)) for s in new_scenarios)
        assert has_encoding, "Expected at least one encoding-based attack scenario"

    def test_covers_social_engineering_attacks(self) -> None:
        """Should cover at least one social engineering / impersonation attack."""
        scenarios = get_scenarios()
        new_ids = {f"RAI-{i:03d}" for i in range(396, 416)}
        new_scenarios = [s for s in scenarios if s.scenario_id in new_ids]

        social_tags = {
            "ceo-impersonation",
            "soc-impersonation",
            "incident-pretext",
            "fake-regulation",
            "compliance-pressure",
            "multi-vector-manipulation",
            "emotional-authority-combo",
        }
        has_social = any(social_tags.intersection(set(s.tags)) for s in new_scenarios)
        assert has_social, "Expected at least one social engineering attack scenario"

    def test_no_duplicate_subjects(self) -> None:
        """No two new scenarios should have the same subject."""
        scenarios = get_scenarios()
        new_ids = {f"RAI-{i:03d}" for i in range(396, 416)}
        new_scenarios = [s for s in scenarios if s.scenario_id in new_ids]

        subjects = [s.subject for s in new_scenarios]
        assert len(subjects) == len(set(subjects)), "Duplicate subjects found among new scenarios"
