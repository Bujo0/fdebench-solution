# Copyright (c) Microsoft. All rights reserved.
"""Extended tests for data cleanup evaluation scenarios (dc-131 through dc-150).

Validates that the new batch of framework-registered data cleanup scenarios
are well-formed, cover the expected noise types, and have consistent
expected triage values.
"""

import unicodedata

import pytest

# Ensure scenarios are registered before tests run.
import ms.evals_core.framework.scenarios.data_cleanup  # noqa: F401
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


@pytest.fixture(scope="module")
def extended_dc_scenarios() -> list[EvalScenario]:
    """Load the extended data cleanup scenarios dc-131..dc-150."""
    ids = {f"dc-{i}" for i in range(131, 151)}
    scenarios = [s for s in default_registry.all() if s.scenario_id in ids]
    return sorted(scenarios, key=lambda s: s.scenario_id)


# ── Structural integrity ─────────────────────────────────────────────


class TestExtendedDcScenarioIntegrity:
    """All extended DC scenarios must be structurally valid."""

    def test_all_twenty_scenarios_exist(self, extended_dc_scenarios: list[EvalScenario]) -> None:
        ids = {s.scenario_id for s in extended_dc_scenarios}
        expected = {f"dc-{i}" for i in range(131, 151)}
        assert expected.issubset(ids), f"Missing IDs: {expected - ids}"

    def test_all_are_data_cleanup_category(self, extended_dc_scenarios: list[EvalScenario]) -> None:
        for s in extended_dc_scenarios:
            assert s.category == ScenarioCategory.DATA_CLEANUP, (
                f"{s.scenario_id}: expected DATA_CLEANUP, got {s.category}"
            )

    def test_all_have_non_empty_ticket_description(self, extended_dc_scenarios: list[EvalScenario]) -> None:
        for s in extended_dc_scenarios:
            assert len(s.ticket.description) > 100, (
                f"{s.scenario_id}: description too short ({len(s.ticket.description)} chars)"
            )

    def test_all_have_valid_expected_triage(self, extended_dc_scenarios: list[EvalScenario]) -> None:
        for s in extended_dc_scenarios:
            assert s.expected_triage is not None, f"{s.scenario_id}: missing expected_triage"
            triage = s.expected_triage
            if triage.category is not None:
                assert triage.category in VALID_CATEGORIES, f"{s.scenario_id}: invalid category '{triage.category}'"
            if triage.priority is not None:
                assert triage.priority in VALID_PRIORITIES, f"{s.scenario_id}: invalid priority '{triage.priority}'"
            if triage.assigned_team is not None:
                assert triage.assigned_team in VALID_TEAMS, f"{s.scenario_id}: invalid team '{triage.assigned_team}'"

    def test_all_have_tags(self, extended_dc_scenarios: list[EvalScenario]) -> None:
        for s in extended_dc_scenarios:
            assert len(s.tags) > 0, f"{s.scenario_id}: no tags"

    def test_all_have_reporter_info(self, extended_dc_scenarios: list[EvalScenario]) -> None:
        for s in extended_dc_scenarios:
            assert s.ticket.reporter.name, f"{s.scenario_id}: empty reporter name"
            assert s.ticket.reporter.email, f"{s.scenario_id}: empty reporter email"
            assert "@contoso.com" in s.ticket.reporter.email, f"{s.scenario_id}: reporter email not from contoso.com"

    def test_no_duplicate_ticket_ids(self, extended_dc_scenarios: list[EvalScenario]) -> None:
        ticket_ids = [s.ticket.ticket_id for s in extended_dc_scenarios]
        assert len(ticket_ids) == len(set(ticket_ids)), (
            f"Duplicate ticket IDs: {[x for x in ticket_ids if ticket_ids.count(x) > 1]}"
        )


# ── Noise type verification ──────────────────────────────────────────


class TestExtendedDcNoiseTypes:
    """Verify each scenario exhibits its claimed noise type."""

    def test_dc131_has_rtl_or_zero_width(self, extended_dc_scenarios: list[EvalScenario]) -> None:
        s = next((s for s in extended_dc_scenarios if s.scenario_id == "dc-131"), None)
        if s is None:
            pytest.skip("dc-131 not registered")
        desc = s.ticket.description
        has_zwj = "\u200d" in desc or "\u200f" in desc or "\u200e" in desc
        has_arabic = any("\u0600" <= c <= "\u06ff" for c in desc)
        assert has_zwj or has_arabic, "dc-131: expected RTL/zero-width/Arabic characters"

    def test_dc133_has_base64(self, extended_dc_scenarios: list[EvalScenario]) -> None:
        s = next((s for s in extended_dc_scenarios if s.scenario_id == "dc-133"), None)
        if s is None:
            pytest.skip("dc-133 not registered")
        assert "base64" in s.ticket.description.lower() or "data:image" in s.ticket.description.lower(), (
            "dc-133: expected base64 data URIs"
        )

    def test_dc134_has_mime_boundaries(self, extended_dc_scenarios: list[EvalScenario]) -> None:
        s = next((s for s in extended_dc_scenarios if s.scenario_id == "dc-134"), None)
        if s is None:
            pytest.skip("dc-134 not registered")
        desc = s.ticket.description.lower()
        assert "boundary" in desc or "content-type" in desc, "dc-134: expected MIME boundary markers"

    def test_dc136_has_combining_marks(self, extended_dc_scenarios: list[EvalScenario]) -> None:
        s = next((s for s in extended_dc_scenarios if s.scenario_id == "dc-136"), None)
        if s is None:
            pytest.skip("dc-136 not registered")

        combining_count = sum(1 for c in s.ticket.description if unicodedata.category(c).startswith("M"))
        assert combining_count >= 5, f"dc-136: expected Zalgo combining marks, found {combining_count}"

    def test_dc138_has_ansi_or_pipeline_markers(self, extended_dc_scenarios: list[EvalScenario]) -> None:
        s = next((s for s in extended_dc_scenarios if s.scenario_id == "dc-138"), None)
        if s is None:
            pytest.skip("dc-138 not registered")
        desc = s.ticket.description
        has_ansi = "\x1b[" in desc or "\\x1b[" in desc or "[0m" in desc
        has_pipeline = "[Pipeline]" in desc or "[INFO]" in desc
        assert has_ansi or has_pipeline, "dc-138: expected ANSI codes or pipeline markers"

    def test_dc139_has_terraform_markers(self, extended_dc_scenarios: list[EvalScenario]) -> None:
        s = next((s for s in extended_dc_scenarios if s.scenario_id == "dc-139"), None)
        if s is None:
            pytest.skip("dc-139 not registered")
        desc = s.ticket.description
        assert "terraform" in desc.lower() or "plan" in desc.lower() or "# " in desc, (
            "dc-139: expected Terraform plan markers"
        )

    def test_dc141_has_pgp_markers(self, extended_dc_scenarios: list[EvalScenario]) -> None:
        s = next((s for s in extended_dc_scenarios if s.scenario_id == "dc-141"), None)
        if s is None:
            pytest.skip("dc-141 not registered")
        desc = s.ticket.description
        assert "BEGIN PGP" in desc or "-----BEGIN" in desc, "dc-141: expected PGP armor blocks"

    def test_dc143_has_xml_event_log(self, extended_dc_scenarios: list[EvalScenario]) -> None:
        s = next((s for s in extended_dc_scenarios if s.scenario_id == "dc-143"), None)
        if s is None:
            pytest.skip("dc-143 not registered")
        desc = s.ticket.description
        has_xml = "<Event" in desc or "<System>" in desc or "<EventData" in desc
        has_event = "Event" in desc and ("Source" in desc or "Level" in desc)
        assert has_xml or has_event, "dc-143: expected Windows Event XML"

    def test_dc146_has_arm_template(self, extended_dc_scenarios: list[EvalScenario]) -> None:
        s = next((s for s in extended_dc_scenarios if s.scenario_id == "dc-146"), None)
        if s is None:
            pytest.skip("dc-146 not registered")
        desc = s.ticket.description.lower()
        assert "microsoft" in desc or "arm" in desc or "template" in desc or "$schema" in desc, (
            "dc-146: expected ARM template content"
        )

    def test_dc150_has_long_description(self, extended_dc_scenarios: list[EvalScenario]) -> None:
        s = next((s for s in extended_dc_scenarios if s.scenario_id == "dc-150"), None)
        if s is None:
            pytest.skip("dc-150 not registered")
        assert len(s.ticket.description) > 1500, (
            f"dc-150: expected extremely verbose description, got {len(s.ticket.description)} chars"
        )


# ── Classification correctness ───────────────────────────────────────


class TestExtendedDcClassification:
    """Verify expected triage classifications are reasonable."""

    def test_network_scenarios_route_to_network_ops(self, extended_dc_scenarios: list[EvalScenario]) -> None:
        """Scenarios with network issues should route to Network Operations."""
        for s in extended_dc_scenarios:
            if s.expected_triage and s.expected_triage.category == "Network & Connectivity":
                assert s.expected_triage.assigned_team == "Network Operations", (
                    f"{s.scenario_id}: network issue should route to Network Operations"
                )

    def test_hardware_scenarios_route_to_endpoint(self, extended_dc_scenarios: list[EvalScenario]) -> None:
        """Scenarios with hardware issues should route to Endpoint Engineering."""
        for s in extended_dc_scenarios:
            if s.expected_triage and s.expected_triage.category == "Hardware & Peripherals":
                assert s.expected_triage.assigned_team == "Endpoint Engineering", (
                    f"{s.scenario_id}: hardware issue should route to Endpoint Engineering"
                )

    def test_security_scenarios_route_to_security_ops(self, extended_dc_scenarios: list[EvalScenario]) -> None:
        """Scenarios with security issues should route to Security Operations."""
        for s in extended_dc_scenarios:
            if s.expected_triage and s.expected_triage.category == "Security & Compliance":
                assert s.expected_triage.assigned_team == "Security Operations", (
                    f"{s.scenario_id}: security issue should route to Security Operations"
                )
