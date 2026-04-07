# Copyright (c) Microsoft. All rights reserved.
"""Tests for mastery-level data cleanup evaluation scenarios (dc-171 through dc-190).

Validates that the new batch of framework-registered data cleanup scenarios
are well-formed, cover the expected extreme noise types, and have consistent
expected triage values. These scenarios test edge cases beyond the extended
set: Zalgo text, control characters, URL-encoded bodies, hex dumps, etc.
"""

import unicodedata

import pytest

import ms.evals_core.framework.scenarios.data_cleanup_mastery  # noqa: F401
from ms.evals_core.framework.models.scenario import EvalScenario
from ms.evals_core.framework.models.scenario import ScenarioCategory
from ms.evals_core.framework.scenarios.registry import default_registry

VALID_CATEGORIES = {
    "Access & Authentication",
    "Hardware & Peripherals",
    "Network & Connectivity",
    "Software & Applications",
    "Security & Compliance",
    "Data & Storage",
    "General Inquiry",
    "Not a Support Ticket",
}
VALID_TEAMS = {
    "Identity & Access Management",
    "Endpoint Engineering",
    "Network Operations",
    "Enterprise Applications",
    "Security Operations",
    "Data Platform",
    "None",
}
VALID_PRIORITIES = {"P1", "P2", "P3", "P4"}

_MASTERY_IDS = {f"dc-{i}" for i in range(171, 191)}


@pytest.fixture(scope="module")
def mastery_dc_scenarios() -> list[EvalScenario]:
    """Load the mastery data cleanup scenarios dc-171..dc-190."""
    scenarios = [s for s in default_registry.all() if s.scenario_id in _MASTERY_IDS]
    return sorted(scenarios, key=lambda s: s.scenario_id)


# ── Structural integrity ─────────────────────────────────────────────


class TestMasteryDcScenarioIntegrity:
    """All mastery DC scenarios must be structurally valid."""

    def test_all_twenty_scenarios_exist(self, mastery_dc_scenarios: list[EvalScenario]) -> None:
        ids = {s.scenario_id for s in mastery_dc_scenarios}
        assert _MASTERY_IDS.issubset(ids), f"Missing IDs: {_MASTERY_IDS - ids}"

    def test_all_are_data_cleanup_category(self, mastery_dc_scenarios: list[EvalScenario]) -> None:
        for s in mastery_dc_scenarios:
            assert s.category == ScenarioCategory.DATA_CLEANUP, (
                f"{s.scenario_id}: expected DATA_CLEANUP, got {s.category}"
            )

    def test_all_have_non_empty_ticket_description(self, mastery_dc_scenarios: list[EvalScenario]) -> None:
        for s in mastery_dc_scenarios:
            assert len(s.ticket.description) > 100, (
                f"{s.scenario_id}: description too short ({len(s.ticket.description)} chars)"
            )

    def test_all_have_valid_expected_triage(self, mastery_dc_scenarios: list[EvalScenario]) -> None:
        for s in mastery_dc_scenarios:
            assert s.expected_triage is not None, f"{s.scenario_id}: missing expected_triage"
            triage = s.expected_triage
            if triage.category is not None:
                assert triage.category in VALID_CATEGORIES, f"{s.scenario_id}: invalid category '{triage.category}'"
            if triage.priority is not None:
                assert triage.priority in VALID_PRIORITIES, f"{s.scenario_id}: invalid priority '{triage.priority}'"
            if triage.assigned_team is not None:
                assert triage.assigned_team in VALID_TEAMS, f"{s.scenario_id}: invalid team '{triage.assigned_team}'"

    def test_all_have_tags(self, mastery_dc_scenarios: list[EvalScenario]) -> None:
        for s in mastery_dc_scenarios:
            assert len(s.tags) > 0, f"{s.scenario_id}: no tags"

    def test_all_have_reporter_info(self, mastery_dc_scenarios: list[EvalScenario]) -> None:
        for s in mastery_dc_scenarios:
            assert s.ticket.reporter.name, f"{s.scenario_id}: empty reporter name"
            assert s.ticket.reporter.email, f"{s.scenario_id}: empty reporter email"
            assert "@contoso.com" in s.ticket.reporter.email, f"{s.scenario_id}: reporter email not from contoso.com"

    def test_no_duplicate_ticket_ids(self, mastery_dc_scenarios: list[EvalScenario]) -> None:
        ticket_ids = [s.ticket.ticket_id for s in mastery_dc_scenarios]
        assert len(ticket_ids) == len(set(ticket_ids)), (
            f"Duplicate ticket IDs: {[x for x in ticket_ids if ticket_ids.count(x) > 1]}"
        )

    def test_all_ticket_ids_start_with_inc(self, mastery_dc_scenarios: list[EvalScenario]) -> None:
        for s in mastery_dc_scenarios:
            assert s.ticket.ticket_id.startswith("INC-"), (
                f"{s.scenario_id}: ticket_id {s.ticket.ticket_id} should start with INC-"
            )


# ── Noise type verification ──────────────────────────────────────────


class TestMasteryDcNoiseTypes:
    """Verify each scenario exhibits its claimed noise type."""

    def test_dc171_has_combining_characters(self, mastery_dc_scenarios: list[EvalScenario]) -> None:
        """Zalgo text should contain many Unicode combining marks."""
        s = next((s for s in mastery_dc_scenarios if s.scenario_id == "dc-171"), None)
        if s is None:
            pytest.skip("dc-171 not registered")
        combining_count = sum(1 for c in s.ticket.description if unicodedata.category(c).startswith("M"))
        assert combining_count >= 10, f"dc-171: expected Zalgo combining marks, found {combining_count}"

    def test_dc172_has_emoji_subject(self, mastery_dc_scenarios: list[EvalScenario]) -> None:
        """Subject should be primarily emoji characters."""
        s = next((s for s in mastery_dc_scenarios if s.scenario_id == "dc-172"), None)
        if s is None:
            pytest.skip("dc-172 not registered")
        # Emoji should be the majority of the subject
        emoji_chars = sum(1 for c in s.ticket.subject if unicodedata.category(c).startswith("So"))
        assert emoji_chars >= 3, f"dc-172: expected emoji-heavy subject, found {emoji_chars} emoji"

    def test_dc173_has_control_characters(self, mastery_dc_scenarios: list[EvalScenario]) -> None:
        """Description should contain ASCII control characters."""
        s = next((s for s in mastery_dc_scenarios if s.scenario_id == "dc-173"), None)
        if s is None:
            pytest.skip("dc-173 not registered")
        control_count = sum(1 for c in s.ticket.description if ord(c) < 32 and c not in "\n\r\t")
        assert control_count >= 5, f"dc-173: expected control characters, found {control_count}"

    def test_dc174_has_url_encoding(self, mastery_dc_scenarios: list[EvalScenario]) -> None:
        """Description should contain URL-encoded content."""
        s = next((s for s in mastery_dc_scenarios if s.scenario_id == "dc-174"), None)
        if s is None:
            pytest.skip("dc-174 not registered")
        assert "%20" in s.ticket.description or "%0A" in s.ticket.description, "dc-174: expected URL-encoded content"

    def test_dc175_has_tab_delimited_data(self, mastery_dc_scenarios: list[EvalScenario]) -> None:
        """Description should contain tab characters in a data table."""
        s = next((s for s in mastery_dc_scenarios if s.scenario_id == "dc-175"), None)
        if s is None:
            pytest.skip("dc-175 not registered")
        tab_count = s.ticket.description.count("\t")
        assert tab_count >= 50, f"dc-175: expected many tabs in data dump, found {tab_count}"

    def test_dc176_has_sql_content(self, mastery_dc_scenarios: list[EvalScenario]) -> None:
        """Description should contain SQL query content."""
        s = next((s for s in mastery_dc_scenarios if s.scenario_id == "dc-176"), None)
        if s is None:
            pytest.skip("dc-176 not registered")
        desc = s.ticket.description.upper()
        assert "SELECT" in desc and "FROM" in desc, "dc-176: expected SQL query content"

    def test_dc177_is_very_long_single_line(self, mastery_dc_scenarios: list[EvalScenario]) -> None:
        """Description should be extremely long with minimal line breaks."""
        s = next((s for s in mastery_dc_scenarios if s.scenario_id == "dc-177"), None)
        if s is None:
            pytest.skip("dc-177 not registered")
        assert len(s.ticket.description) > 2000, (
            f"dc-177: expected very long description, got {len(s.ticket.description)} chars"
        )
        # Check that newlines are rare compared to length
        newline_ratio = s.ticket.description.count("\n") / len(s.ticket.description)
        assert newline_ratio < 0.005, f"dc-177: too many newlines ({newline_ratio:.4f} ratio)"

    def test_dc178_has_base64_body(self, mastery_dc_scenarios: list[EvalScenario]) -> None:
        """Description should contain base64-encoded content."""
        s = next((s for s in mastery_dc_scenarios if s.scenario_id == "dc-178"), None)
        if s is None:
            pytest.skip("dc-178 not registered")
        desc = s.ticket.description
        assert "base64" in desc.lower() or "Content-Transfer-Encoding" in desc, (
            "dc-178: expected base64 transfer encoding"
        )

    def test_dc179_has_nested_json(self, mastery_dc_scenarios: list[EvalScenario]) -> None:
        """Description should contain deeply nested JSON."""
        s = next((s for s in mastery_dc_scenarios if s.scenario_id == "dc-179"), None)
        if s is None:
            pytest.skip("dc-179 not registered")
        # Check nesting depth by counting consecutive indentation
        brace_depth = 0
        max_depth = 0
        for char in s.ticket.description:
            if char == "{":
                brace_depth += 1
                max_depth = max(max_depth, brace_depth)
            elif char == "}":
                brace_depth -= 1
        assert max_depth >= 5, f"dc-179: expected deep JSON nesting, max depth was {max_depth}"

    def test_dc180_has_hebrew_text(self, mastery_dc_scenarios: list[EvalScenario]) -> None:
        """Description should contain Hebrew (RTL) characters."""
        s = next((s for s in mastery_dc_scenarios if s.scenario_id == "dc-180"), None)
        if s is None:
            pytest.skip("dc-180 not registered")
        hebrew_count = sum(1 for c in s.ticket.description if "\u0590" <= c <= "\u05ff")
        assert hebrew_count >= 10, f"dc-180: expected Hebrew characters, found {hebrew_count}"

    def test_dc181_has_cid_references(self, mastery_dc_scenarios: list[EvalScenario]) -> None:
        """Description should contain PDF CID reference artifacts."""
        s = next((s for s in mastery_dc_scenarios if s.scenario_id == "dc-181"), None)
        if s is None:
            pytest.skip("dc-181 not registered")
        assert "(cid:" in s.ticket.description, "dc-181: expected (cid:) PDF extraction artifacts"

    def test_dc182_has_svg_content(self, mastery_dc_scenarios: list[EvalScenario]) -> None:
        """Description should contain inline SVG markup."""
        s = next((s for s in mastery_dc_scenarios if s.scenario_id == "dc-182"), None)
        if s is None:
            pytest.skip("dc-182 not registered")
        assert "<svg" in s.ticket.description.lower(), "dc-182: expected inline SVG content"

    def test_dc183_has_many_alert_lines(self, mastery_dc_scenarios: list[EvalScenario]) -> None:
        """Description should contain many repetitive alert lines."""
        s = next((s for s in mastery_dc_scenarios if s.scenario_id == "dc-183"), None)
        if s is None:
            pytest.skip("dc-183 not registered")
        alert_count = s.ticket.description.count("[ALERT")
        assert alert_count >= 50, f"dc-183: expected 50+ alert lines, found {alert_count}"

    def test_dc184_has_transcript_timestamps(self, mastery_dc_scenarios: list[EvalScenario]) -> None:
        """Description should contain phone transcript with timestamps."""
        s = next((s for s in mastery_dc_scenarios if s.scenario_id == "dc-184"), None)
        if s is None:
            pytest.skip("dc-184 not registered")
        assert "[00:" in s.ticket.description, "dc-184: expected phone transcript timestamps"
        assert "AGENT" in s.ticket.description or "CALLER" in s.ticket.description, "dc-184: expected speaker labels"

    def test_dc185_has_hex_dump(self, mastery_dc_scenarios: list[EvalScenario]) -> None:
        """Description should contain hexadecimal dump content."""
        s = next((s for s in mastery_dc_scenarios if s.scenario_id == "dc-185"), None)
        if s is None:
            pytest.skip("dc-185 not registered")
        assert "0x" in s.ticket.description, "dc-185: expected hex addresses"

    def test_dc186_has_excessive_punctuation(self, mastery_dc_scenarios: list[EvalScenario]) -> None:
        """Description should contain excessive special characters."""
        s = next((s for s in mastery_dc_scenarios if s.scenario_id == "dc-186"), None)
        if s is None:
            pytest.skip("dc-186 not registered")
        exclamation_count = s.ticket.description.count("!")
        star_count = s.ticket.description.count("★")
        assert exclamation_count >= 20 or star_count >= 5, (
            f"dc-186: expected excessive punctuation (! count: {exclamation_count}, ★ count: {star_count})"
        )

    def test_dc187_has_long_url(self, mastery_dc_scenarios: list[EvalScenario]) -> None:
        """Description should contain a very long URL."""
        s = next((s for s in mastery_dc_scenarios if s.scenario_id == "dc-187"), None)
        if s is None:
            pytest.skip("dc-187 not registered")
        # Find the longest URL-like string
        desc = s.ticket.description
        assert "oauth2/authorize?" in desc, "dc-187: expected OAuth URL"
        assert "code_challenge" in desc, "dc-187: expected PKCE parameters"

    def test_dc188_has_merged_ticket_markers(self, mastery_dc_scenarios: list[EvalScenario]) -> None:
        """Description should contain merged ticket artifact markers."""
        s = next((s for s in mastery_dc_scenarios if s.scenario_id == "dc-188"), None)
        if s is None:
            pytest.skip("dc-188 not registered")
        assert "MERGED" in s.ticket.description, "dc-188: expected merged ticket markers"
        assert "INC-5188a" in s.ticket.description, "dc-188: expected sub-ticket IDs"

    def test_dc189_has_event_log_xml(self, mastery_dc_scenarios: list[EvalScenario]) -> None:
        """Description should contain Windows Event Log XML."""
        s = next((s for s in mastery_dc_scenarios if s.scenario_id == "dc-189"), None)
        if s is None:
            pytest.skip("dc-189 not registered")
        assert "<Event" in s.ticket.description, "dc-189: expected Event XML"
        assert "<EventID>" in s.ticket.description, "dc-189: expected EventID element"

    def test_dc190_has_mojibake(self, mastery_dc_scenarios: list[EvalScenario]) -> None:
        """Description should contain Mojibake (double-encoded UTF-8) artifacts."""
        s = next((s for s in mastery_dc_scenarios if s.scenario_id == "dc-190"), None)
        if s is None:
            pytest.skip("dc-190 not registered")
        # â€™ is the classic Mojibake for right single quote (UTF-8 bytes read as Latin-1)
        assert "\u00e2\u0080" in s.ticket.description, "dc-190: expected Mojibake characters"


# ── Classification correctness ───────────────────────────────────────


class TestMasteryDcClassification:
    """Verify expected triage classifications are reasonable."""

    def test_network_scenarios_route_to_network_ops(self, mastery_dc_scenarios: list[EvalScenario]) -> None:
        for s in mastery_dc_scenarios:
            if s.expected_triage and s.expected_triage.category == "Network & Connectivity":
                assert s.expected_triage.assigned_team == "Network Operations", (
                    f"{s.scenario_id}: network issue should route to Network Operations"
                )

    def test_hardware_scenarios_route_to_endpoint(self, mastery_dc_scenarios: list[EvalScenario]) -> None:
        for s in mastery_dc_scenarios:
            if s.expected_triage and s.expected_triage.category == "Hardware & Peripherals":
                assert s.expected_triage.assigned_team == "Endpoint Engineering", (
                    f"{s.scenario_id}: hardware issue should route to Endpoint Engineering"
                )

    def test_security_scenarios_route_to_security_ops(self, mastery_dc_scenarios: list[EvalScenario]) -> None:
        for s in mastery_dc_scenarios:
            if s.expected_triage and s.expected_triage.category == "Security & Compliance":
                assert s.expected_triage.assigned_team == "Security Operations", (
                    f"{s.scenario_id}: security issue should route to Security Operations"
                )

    def test_software_scenarios_route_to_enterprise_apps(self, mastery_dc_scenarios: list[EvalScenario]) -> None:
        for s in mastery_dc_scenarios:
            if s.expected_triage and s.expected_triage.category == "Software & Applications":
                assert s.expected_triage.assigned_team == "Enterprise Applications", (
                    f"{s.scenario_id}: software issue should route to Enterprise Applications"
                )

    def test_access_scenarios_route_to_iam(self, mastery_dc_scenarios: list[EvalScenario]) -> None:
        for s in mastery_dc_scenarios:
            if s.expected_triage and s.expected_triage.category == "Access & Authentication":
                assert s.expected_triage.assigned_team == "Identity & Access Management", (
                    f"{s.scenario_id}: access issue should route to IAM"
                )

    def test_data_storage_scenarios_route_to_data_platform(self, mastery_dc_scenarios: list[EvalScenario]) -> None:
        for s in mastery_dc_scenarios:
            if s.expected_triage and s.expected_triage.category == "Data & Storage":
                assert s.expected_triage.assigned_team == "Data Platform", (
                    f"{s.scenario_id}: data storage issue should route to Data Platform"
                )

    def test_p1_scenarios_have_escalation(self, mastery_dc_scenarios: list[EvalScenario]) -> None:
        """P1 scenarios should typically need escalation."""
        for s in mastery_dc_scenarios:
            if s.expected_triage and s.expected_triage.priority == "P1":
                assert s.expected_triage.needs_escalation is True, (
                    f"{s.scenario_id}: P1 scenario should need escalation"
                )

    def test_category_coverage(self, mastery_dc_scenarios: list[EvalScenario]) -> None:
        """Mastery scenarios should cover multiple categories."""
        categories = {
            s.expected_triage.category for s in mastery_dc_scenarios if s.expected_triage and s.expected_triage.category
        }
        assert len(categories) >= 4, f"Expected coverage of at least 4 categories, got {len(categories)}: {categories}"
