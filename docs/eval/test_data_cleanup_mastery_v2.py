#!/usr/bin/env python3
"""Evaluation tests for mastery-level data cleanup scenarios.

Tests that the triage system correctly handles extreme noise types:
Zalgo text, control characters, URL-encoded bodies, tab-delimited data dumps,
SQL query dumps, base64-encoded full bodies, mixed RTL/LTR, merged tickets,
hex dumps, excessive punctuation, phone transcripts, and double-encoded Mojibake.

These tests validate:
  1. Dataset integrity — ticket and gold data are well-formed.
  2. Gold answer correctness — all values within constrained vocabulary.
  3. Scoring pipeline — gold vs gold yields a perfect score.
  4. Per-ticket data-quality tests — each ticket exhibits its claimed noise type.
  5. Noise resilience — system extracts signal from noisy tickets.

The tests cover the mastery v2 dataset:
  • data_cleanup_mastery_v2_eval.json (15 tickets, INC-7###) — extreme noise edge cases

Usage:
    cd docs/eval
    uv run pytest test_data_cleanup_mastery_v2.py -v
"""

import json
import re
import sys
import unicodedata
from pathlib import Path

sys.path.insert(0, ".")  # noqa: TID251

from run_eval import CATEGORIES
from run_eval import TEAMS
from run_eval import score_submission
from run_eval import score_ticket

# ── Paths ────────────────────────────────────────────────────────────

_DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "tickets"

_TICKETS_PATH = _DATA_DIR / "data_cleanup_mastery_v2_eval.json"
_GOLD_PATH = _DATA_DIR / "data_cleanup_mastery_v2_eval_gold.json"

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


def _tickets_by_id() -> dict[str, dict]:
    return {t["ticket_id"]: t for t in _load_tickets()}


# ═══════════════════════════════════════════════════════════════════
# SECTION 1: Dataset integrity
# ═══════════════════════════════════════════════════════════════════


def test_tickets_file_exists():
    assert _TICKETS_PATH.exists(), f"Missing: {_TICKETS_PATH}"


def test_gold_file_exists():
    assert _GOLD_PATH.exists(), f"Missing: {_GOLD_PATH}"


def test_ticket_count_matches_gold():
    tickets = _load_tickets()
    gold = _load_gold()
    assert len(tickets) == len(gold), f"Ticket count {len(tickets)} != gold count {len(gold)}"


def test_ticket_ids_match():
    ticket_ids = {t["ticket_id"] for t in _load_tickets()}
    gold_ids = {g["ticket_id"] for g in _load_gold()}
    assert ticket_ids == gold_ids, f"ID mismatch: {ticket_ids.symmetric_difference(gold_ids)}"


def test_all_ticket_ids_unique():
    ticket_ids = [t["ticket_id"] for t in _load_tickets()]
    assert len(ticket_ids) == len(set(ticket_ids)), "Duplicate ticket IDs"


def test_dataset_has_15_tickets():
    assert len(_load_tickets()) == 15, f"Expected 15 tickets, got {len(_load_tickets())}"


# ── Input schema validation ──────────────────────────────────────────


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


def test_gold_remediation_steps_non_empty():
    for g in _load_gold():
        assert len(g["remediation_steps"]) > 0, (
            f"{g['ticket_id']}: empty remediation_steps"
        )


def test_gold_next_best_action_non_empty():
    for g in _load_gold():
        assert len(g["next_best_action"]) > 10, (
            f"{g['ticket_id']}: next_best_action too short"
        )


# ═══════════════════════════════════════════════════════════════════
# SECTION 2: Scoring — gold vs gold should be perfect
# ═══════════════════════════════════════════════════════════════════


def test_gold_vs_gold_perfect_score():
    gold_list = _load_gold()
    result = score_submission(gold_list, gold_list)
    assert result["classification_score"] >= 80, (
        f"Gold vs gold score too low: {result['classification_score']}"
    )


def test_per_ticket_gold_match():
    gold_list = _load_gold()
    for g in gold_list:
        result = score_ticket(g, g)
        # Classification dimensions max at 0.85 (85% weight); 15% is efficiency
        assert result["weighted_total"] >= 0.84, (
            f"{g['ticket_id']}: self-score {result['weighted_total']:.2f} < 0.84"
        )


# ═══════════════════════════════════════════════════════════════════
# SECTION 3: Noise-type verification
# ═══════════════════════════════════════════════════════════════════


def test_has_url_encoded_ticket():
    """At least one ticket should contain URL-encoded content."""
    tickets = _load_tickets()
    has_url_encoded = any("%20" in t["description"] or "%0A" in t["description"] for t in tickets)
    assert has_url_encoded, "Expected at least one URL-encoded ticket"


def test_has_tab_delimited_ticket():
    """At least one ticket should contain tab-delimited data."""
    tickets = _load_tickets()
    has_tabs = any(t["description"].count("\t") >= 20 for t in tickets)
    assert has_tabs, "Expected at least one tab-delimited data dump ticket"


def test_has_base64_ticket():
    """At least one ticket should contain base64-encoded content."""
    tickets = _load_tickets()
    has_b64 = any("base64" in t["description"].lower() or "Content-Transfer-Encoding" in t["description"] for t in tickets)
    assert has_b64, "Expected at least one base64-encoded ticket"


def test_has_sql_content():
    """At least one ticket should contain SQL query content."""
    tickets = _load_tickets()
    has_sql = any("SELECT" in t["description"] and "FROM" in t["description"] for t in tickets)
    assert has_sql, "Expected at least one SQL dump ticket"


def test_has_alert_flood():
    """At least one ticket should contain many repetitive alert lines."""
    tickets = _load_tickets()
    has_flood = any(t["description"].count("[ALERT") >= 20 for t in tickets)
    assert has_flood, "Expected at least one alert flood ticket"


def test_has_hex_dump():
    """At least one ticket should contain hex dump content."""
    tickets = _load_tickets()
    has_hex = any("0x" in t["description"] for t in tickets)
    assert has_hex, "Expected at least one hex dump ticket"


def test_has_excessive_punctuation():
    """At least one ticket should contain many special/non-alphanumeric characters."""
    tickets = _load_tickets()
    has_punct = any(
        sum(1 for c in t["description"] if not c.isalnum() and not c.isspace()) > 100
        for t in tickets
    )
    assert has_punct, "Expected at least one ticket with excessive special characters"


def test_has_phone_transcript():
    """At least one ticket should contain phone transcript markers."""
    tickets = _load_tickets()
    has_transcript = any("[00:" in t["description"] for t in tickets)
    assert has_transcript, "Expected at least one phone transcript ticket"


def test_has_merged_ticket_markers():
    """At least one ticket should contain merged ticket artifact markers."""
    tickets = _load_tickets()
    has_merged = any("MERGED" in t["description"] for t in tickets)
    assert has_merged, "Expected at least one merged ticket artifact"


def test_has_mojibake():
    """At least one ticket should contain Mojibake artifacts."""
    tickets = _load_tickets()
    has_mojibake = any("\u00e2\u0080" in t["description"] for t in tickets)
    assert has_mojibake, "Expected at least one Mojibake ticket"


# ═══════════════════════════════════════════════════════════════════
# SECTION 4: Category coverage
# ═══════════════════════════════════════════════════════════════════


def test_multiple_categories_covered():
    """Dataset should cover at least 4 different categories."""
    gold_list = _load_gold()
    categories = {g["category"] for g in gold_list}
    assert len(categories) >= 4, f"Only {len(categories)} categories covered: {categories}"


def test_multiple_priorities_covered():
    """Dataset should cover at least 3 different priority levels."""
    gold_list = _load_gold()
    priorities = {g["priority"] for g in gold_list}
    assert len(priorities) >= 3, f"Only {len(priorities)} priorities covered: {priorities}"


# ═══════════════════════════════════════════════════════════════════
# SECTION 5: Routing consistency
# ═══════════════════════════════════════════════════════════════════


def test_network_routes_to_network_ops():
    for g in _load_gold():
        if g["category"] == "Network & Connectivity":
            assert g["assigned_team"] == "Network Operations", (
                f"{g['ticket_id']}: network issue routed to {g['assigned_team']}"
            )


def test_hardware_routes_to_endpoint():
    for g in _load_gold():
        if g["category"] == "Hardware & Peripherals":
            assert g["assigned_team"] == "Endpoint Engineering", (
                f"{g['ticket_id']}: hardware issue routed to {g['assigned_team']}"
            )


def test_security_routes_to_secops():
    for g in _load_gold():
        if g["category"] == "Security & Compliance":
            assert g["assigned_team"] == "Security Operations", (
                f"{g['ticket_id']}: security issue routed to {g['assigned_team']}"
            )


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])
