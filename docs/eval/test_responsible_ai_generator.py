#!/usr/bin/env python3
"""Evaluation tests for generator-produced responsible AI scenarios.

Tests that the generator-based RAI dataset (from responsible_ai_forensic generator
scenarios) is well-formed and validates correctly. This dataset covers forensic-level
attacks: fake system errors, gaslighting, sycophancy, recursive jailbreaks, metadata
injection, model impersonation, emotional manipulation, fake scans, ethical dilemmas,
and multi-vector combined attacks.

Usage:
    cd docs/eval
    uv run pytest test_responsible_ai_generator.py -v
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, ".")  # noqa: TID251

from run_eval import CATEGORIES
from run_eval import TEAMS
from run_eval import score_submission
from run_eval import score_ticket

# ── Paths ────────────────────────────────────────────────────────────

_DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "tickets"
_TICKETS_PATH = _DATA_DIR / "responsible_ai_generator_eval.json"
_GOLD_PATH = _DATA_DIR / "responsible_ai_generator_eval_gold.json"

# ── Constrained vocabularies ─────────────────────────────────────────

VALID_CATEGORIES = {c.lower() for c in CATEGORIES}
VALID_TEAMS = {t.lower() for t in TEAMS}
VALID_PRIORITIES = {"p1", "p2", "p3", "p4"}
VALID_MISSING_INFO = {
    "affected_system", "error_message", "steps_to_reproduce", "affected_users",
    "environment_details", "timestamp", "previous_ticket_id", "contact_info",
    "device_info", "application_version", "network_location", "business_impact",
    "reproduction_frequency", "screenshot_or_attachment", "authentication_method",
    "configuration_details",
}
_REQUIRED_INPUT_FIELDS = {"ticket_id", "subject", "description", "reporter", "created_at", "channel"}
_REQUIRED_GOLD_FIELDS = {
    "ticket_id", "category", "priority", "assigned_team", "needs_escalation",
    "missing_information", "next_best_action", "remediation_steps",
}
_VALID_CHANNELS = {"email", "chat", "portal", "phone"}


# ── Helpers ──────────────────────────────────────────────────────────

def _load_tickets() -> list[dict]:
    return json.loads(_TICKETS_PATH.read_text())


def _load_gold() -> list[dict]:
    return json.loads(_GOLD_PATH.read_text())


def _gold_by_id() -> dict[str, dict]:
    return {g["ticket_id"]: g for g in _load_gold()}


# ═══════════════════════════════════════════════════════════════════
# SECTION 1: Dataset integrity
# ═══════════════════════════════════════════════════════════════════


def test_tickets_file_exists():
    assert _TICKETS_PATH.exists(), f"Missing: {_TICKETS_PATH}"


def test_gold_file_exists():
    assert _GOLD_PATH.exists(), f"Missing: {_GOLD_PATH}"


def test_ticket_count_matches_gold():
    assert len(_load_tickets()) == len(_load_gold()), "Ticket / gold count mismatch"


def test_ticket_ids_match():
    ticket_ids = {t["ticket_id"] for t in _load_tickets()}
    gold_ids = {g["ticket_id"] for g in _load_gold()}
    assert ticket_ids == gold_ids, f"ID mismatch: {ticket_ids.symmetric_difference(gold_ids)}"


def test_all_ticket_ids_unique():
    ids = [t["ticket_id"] for t in _load_tickets()]
    assert len(ids) == len(set(ids)), "Duplicate ticket IDs"


def test_dataset_has_12_tickets():
    assert len(_load_tickets()) == 12, f"Expected 12 tickets, got {len(_load_tickets())}"


# ── Schema validation ────────────────────────────────────────────────


def test_all_tickets_have_required_fields():
    for ticket in _load_tickets():
        missing = _REQUIRED_INPUT_FIELDS - set(ticket.keys())
        assert not missing, f"{ticket['ticket_id']} missing: {missing}"


def test_all_reporters_have_required_fields():
    required = {"name", "email", "department"}
    for ticket in _load_tickets():
        missing = required - set(ticket["reporter"].keys())
        assert not missing, f"{ticket['ticket_id']} reporter missing: {missing}"


def test_all_channels_valid():
    for ticket in _load_tickets():
        assert ticket["channel"] in _VALID_CHANNELS, (
            f"{ticket['ticket_id']} invalid channel: {ticket['channel']}"
        )


# ── Gold answer validation ───────────────────────────────────────────


def test_gold_categories_valid():
    for g in _load_gold():
        assert g["category"].lower() in VALID_CATEGORIES, (
            f"{g['ticket_id']}: invalid category '{g['category']}'"
        )


def test_gold_priorities_valid():
    for g in _load_gold():
        assert g["priority"].lower() in VALID_PRIORITIES, (
            f"{g['ticket_id']}: invalid priority '{g['priority']}'"
        )


def test_gold_teams_valid():
    for g in _load_gold():
        assert g["assigned_team"].lower() in VALID_TEAMS, (
            f"{g['ticket_id']}: invalid team '{g['assigned_team']}'"
        )


def test_gold_missing_info_valid():
    for g in _load_gold():
        for field in g["missing_information"]:
            assert field in VALID_MISSING_INFO, (
                f"{g['ticket_id']}: invalid missing_info '{field}'"
            )


def test_gold_has_required_fields():
    for g in _load_gold():
        missing = _REQUIRED_GOLD_FIELDS - set(g.keys())
        assert not missing, f"{g['ticket_id']} gold missing: {missing}"


def test_gold_remediation_non_empty():
    for g in _load_gold():
        assert len(g["remediation_steps"]) > 0, f"{g['ticket_id']}: empty remediation"


def test_gold_nba_non_empty():
    for g in _load_gold():
        assert len(g["next_best_action"]) > 10, f"{g['ticket_id']}: NBA too short"


# ═══════════════════════════════════════════════════════════════════
# SECTION 2: Scoring
# ═══════════════════════════════════════════════════════════════════


def test_gold_vs_gold_score():
    gold_list = _load_gold()
    result = score_submission(gold_list, gold_list)
    assert result["classification_score"] >= 80, (
        f"Gold vs gold too low: {result['classification_score']}"
    )


def test_per_ticket_gold_match():
    for g in _load_gold():
        result = score_ticket(g, g)
        assert result["weighted_total"] >= 0.84, (
            f"{g['ticket_id']}: self-score {result['weighted_total']:.2f} < 0.84"
        )


# ═══════════════════════════════════════════════════════════════════
# SECTION 3: Adversarial content verification
# ═══════════════════════════════════════════════════════════════════


def test_has_injection_attempts():
    """At least one ticket should contain injection language."""
    tickets = _load_tickets()
    markers = ["ignore previous", "override", "SYSTEM ERROR", "new instructions", "CRITICAL SYSTEM"]
    found = any(
        any(m.lower() in t["description"].lower() for m in markers)
        for t in tickets
    )
    assert found, "Expected at least one injection attempt"


def test_has_emotional_manipulation():
    """At least one ticket should contain emotional manipulation."""
    tickets = _load_tickets()
    markers = ["heart condition", "hospital", "medical", "panic", "desperate", "health"]
    found = any(
        any(m.lower() in t["description"].lower() for m in markers)
        for t in tickets
    )
    assert found, "Expected at least one emotional manipulation ticket"


def test_has_authority_framing():
    """At least one ticket should use authority or compliance framing."""
    tickets = _load_tickets()
    markers = ["SOX", "compliance", "audit", "regulatory", "CISO"]
    found = any(
        any(m in t["description"] for m in markers)
        for t in tickets
    )
    assert found, "Expected at least one authority framing ticket"


# ═══════════════════════════════════════════════════════════════════
# SECTION 4: Coverage
# ═══════════════════════════════════════════════════════════════════


def test_multiple_categories_covered():
    categories = {g["category"] for g in _load_gold()}
    assert len(categories) >= 4, f"Only {len(categories)} categories: {categories}"


def test_multiple_priorities_covered():
    priorities = {g["priority"] for g in _load_gold()}
    assert len(priorities) >= 3, f"Only {len(priorities)} priorities: {priorities}"


# ═══════════════════════════════════════════════════════════════════
# SECTION 5: Routing consistency
# ═══════════════════════════════════════════════════════════════════


def test_network_routes_to_network_ops():
    for g in _load_gold():
        if g["category"] == "Network & Connectivity":
            assert g["assigned_team"] == "Network Operations", (
                f"{g['ticket_id']}: network → {g['assigned_team']}"
            )


def test_security_routes_to_secops():
    for g in _load_gold():
        if g["category"] == "Security & Compliance":
            assert g["assigned_team"] == "Security Operations", (
                f"{g['ticket_id']}: security → {g['assigned_team']}"
            )


def test_access_routes_to_iam():
    for g in _load_gold():
        if g["category"] == "Access & Authentication":
            assert g["assigned_team"] == "Identity & Access Management", (
                f"{g['ticket_id']}: access → {g['assigned_team']}"
            )


# ═══════════════════════════════════════════════════════════════════
# SECTION 6: No ID collisions with other datasets
# ═══════════════════════════════════════════════════════════════════


def test_no_id_collision_with_forensic_rai():
    """No overlap with the main RAI forensic dataset."""
    our_ids = {t["ticket_id"] for t in _load_tickets()}
    forensic_path = _DATA_DIR / "responsible_ai_forensic_eval.json"
    if forensic_path.exists():
        other_ids = {t["ticket_id"] for t in json.loads(forensic_path.read_text())}
        overlap = our_ids & other_ids
        assert not overlap, f"ID collision with forensic RAI: {overlap}"


def test_no_id_collision_with_dc_mastery():
    """No overlap with the DC mastery v2 dataset."""
    our_ids = {t["ticket_id"] for t in _load_tickets()}
    dc_path = _DATA_DIR / "data_cleanup_mastery_v2_eval.json"
    if dc_path.exists():
        other_ids = {t["ticket_id"] for t in json.loads(dc_path.read_text())}
        overlap = our_ids & other_ids
        assert not overlap, f"ID collision with DC mastery v2: {overlap}"


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])
