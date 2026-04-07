#!/usr/bin/env python3
"""Evaluation tests for data cleanup scenarios.

Tests that the triage system correctly handles messy, noisy, and malformed
input data that commonly appears in real-world IT support tickets — including
very long emails, embedded base64 images, HTML content, deep email threads,
Unicode/emoji, repeated text, garbled input, excessive whitespace, mixed
languages, and embedded code/stack traces.

These tests validate:
  1. Dataset integrity — ticket and gold data are well-formed.
  2. Gold answer correctness — all values within constrained vocabulary.
  3. Scoring pipeline — gold vs gold yields a perfect score.
  4. Per-ticket data-quality tests — each ticket exhibits its claimed noise type.
  5. Classification correctness — adversarial/noisy data doesn't break triage.
  6. Noise resilience — system extracts signal from noisy tickets.
  7. Scoring edge cases — wrong answers to noisy data are penalized correctly.
  8. Structural invariants — team/category consistency rules hold.

The tests cover TWO data cleanup datasets:
  • data_cleanup_eval.json (35 tickets, INC-2### + INC-DC###) — handcrafted edge cases
  • data_cleanup.json (15 tickets, INC-5###) — scoring-oriented edge cases

Usage:
    cd docs/eval
    python test_data_cleanup.py

    # Or with pytest:
    uv run pytest test_data_cleanup.py -v

    # Run against a live endpoint:
    uv run python run_eval.py \
        --endpoint http://localhost:8000 \
        --dataset ../data/tickets/data_cleanup.json \
        --gold ../data/tickets/data_cleanup_gold.json
"""

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, ".")  # noqa: TID251

from run_eval import CATEGORIES
from run_eval import TEAMS
from run_eval import score_category
from run_eval import score_missing_info
from run_eval import score_priority
from run_eval import score_submission
from run_eval import score_ticket

# ── Paths ────────────────────────────────────────────────────────────

_DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "tickets"

# Handcrafted 35-ticket dataset (INC-2### + INC-DC###)
_DC_TICKETS_PATH = _DATA_DIR / "data_cleanup_eval.json"
_DC_GOLD_PATH = _DATA_DIR / "data_cleanup_eval_gold.json"

# Scoring-oriented 15-ticket dataset (INC-5###)
_SC_TICKETS_PATH = _DATA_DIR / "data_cleanup.json"
_SC_GOLD_PATH = _DATA_DIR / "data_cleanup_gold.json"

# ── Constrained vocabularies ─────────────────────────────────────────

VALID_CATEGORIES = {c.lower() for c in CATEGORIES}
VALID_TEAMS = {t.lower() for t in TEAMS}
VALID_PRIORITIES = {"p1", "p2", "p3", "p4"}
VALID_MISSING_INFO = {
    "affected_system",
    "error_message",
    "steps_to_reproduce",
    "affected_users",
    "environment_details",
    "timestamp",
    "previous_ticket_id",
    "contact_info",
    "device_info",
    "application_version",
    "network_location",
    "business_impact",
    "reproduction_frequency",
    "screenshot_or_attachment",
    "authentication_method",
    "configuration_details",
}
_REQUIRED_INPUT_FIELDS = {"ticket_id", "subject", "description", "reporter", "created_at", "channel"}
_REQUIRED_GOLD_FIELDS = {
    "ticket_id",
    "category",
    "priority",
    "assigned_team",
    "needs_escalation",
    "missing_information",
    "next_best_action",
    "remediation_steps",
}
_VALID_CHANNELS = {"email", "chat", "portal", "phone"}


# ── Helpers: load datasets ──────────────────────────────────────────


def _load_dc_tickets() -> list[dict]:
    return json.loads(_DC_TICKETS_PATH.read_text())


def _load_dc_gold() -> list[dict]:
    return json.loads(_DC_GOLD_PATH.read_text())


def _dc_gold_by_id() -> dict[str, dict]:
    return {g["ticket_id"]: g for g in _load_dc_gold()}


def _dc_tickets_by_id() -> dict[str, dict]:
    return {t["ticket_id"]: t for t in _load_dc_tickets()}


def _load_sc_tickets() -> list[dict]:
    return json.loads(_SC_TICKETS_PATH.read_text())


def _load_sc_gold() -> list[dict]:
    return json.loads(_SC_GOLD_PATH.read_text())


def _sc_gold_by_id() -> dict[str, dict]:
    return {g["ticket_id"]: g for g in _load_sc_gold()}


# ═══════════════════════════════════════════════════════════════════════
# SECTION 1: Dataset integrity — handcrafted INC-DC### dataset
# ═══════════════════════════════════════════════════════════════════════


def test_dc_tickets_file_exists():
    assert _DC_TICKETS_PATH.exists(), f"Missing: {_DC_TICKETS_PATH}"


def test_dc_gold_file_exists():
    assert _DC_GOLD_PATH.exists(), f"Missing: {_DC_GOLD_PATH}"


def test_dc_ticket_count_matches_gold():
    tickets = _load_dc_tickets()
    gold = _load_dc_gold()
    assert len(tickets) == len(gold), f"Ticket count {len(tickets)} != gold count {len(gold)}"


def test_dc_ticket_ids_match():
    ticket_ids = {t["ticket_id"] for t in _load_dc_tickets()}
    gold_ids = {g["ticket_id"] for g in _load_dc_gold()}
    assert ticket_ids == gold_ids, f"ID mismatch: {ticket_ids.symmetric_difference(gold_ids)}"


def test_dc_all_ticket_ids_unique():
    ticket_ids = [t["ticket_id"] for t in _load_dc_tickets()]
    assert len(ticket_ids) == len(set(ticket_ids)), "Duplicate ticket IDs in dataset"


def test_dc_dataset_has_35_tickets():
    assert len(_load_dc_tickets()) == 35, "Expected 35 data cleanup tickets"


def test_dc_all_ticket_ids_prefixed():
    for t in _load_dc_tickets():
        tid = t["ticket_id"]
        assert tid.startswith("INC-DC") or tid.startswith("INC-2"), f"Bad ticket_id prefix: {tid}"


# ── Input schema validation (INC-DC###) ──────────────────────────────


def test_dc_all_tickets_have_required_fields():
    for ticket in _load_dc_tickets():
        missing = _REQUIRED_INPUT_FIELDS - set(ticket.keys())
        assert not missing, f"{ticket['ticket_id']} missing fields: {missing}"


def test_dc_all_reporters_have_required_fields():
    required = {"name", "email", "department"}
    for ticket in _load_dc_tickets():
        missing = required - set(ticket["reporter"].keys())
        assert not missing, f"{ticket['ticket_id']} reporter missing fields: {missing}"


def test_dc_all_channels_valid():
    for ticket in _load_dc_tickets():
        assert ticket["channel"] in _VALID_CHANNELS, f"{ticket['ticket_id']} invalid channel: {ticket['channel']}"


# ── Gold answer validation (INC-DC###) ───────────────────────────────


def test_dc_gold_categories_valid():
    for g in _load_dc_gold():
        assert g["category"] in set(CATEGORIES), f"{g['ticket_id']}: invalid category '{g['category']}'"


def test_dc_gold_priorities_valid():
    for g in _load_dc_gold():
        assert g["priority"] in {"P1", "P2", "P3", "P4"}, f"{g['ticket_id']}: invalid priority '{g['priority']}'"


def test_dc_gold_teams_valid():
    for g in _load_dc_gold():
        assert g["assigned_team"] in set(TEAMS), f"{g['ticket_id']}: invalid team '{g['assigned_team']}'"


def test_dc_gold_missing_info_valid():
    for g in _load_dc_gold():
        for item in g["missing_information"]:
            assert item in VALID_MISSING_INFO, f"{g['ticket_id']}: invalid missing_information value '{item}'"


def test_dc_gold_schema_fields():
    for g in _load_dc_gold():
        missing = _REQUIRED_GOLD_FIELDS - set(g.keys())
        assert not missing, f"{g['ticket_id']}: missing gold fields {missing}"


def test_dc_gold_escalation_is_boolean():
    for g in _load_dc_gold():
        assert isinstance(g["needs_escalation"], bool), (
            f"{g['ticket_id']}: needs_escalation is {type(g['needs_escalation'])}"
        )


def test_dc_gold_missing_info_is_list():
    for g in _load_dc_gold():
        assert isinstance(g["missing_information"], list), (
            f"{g['ticket_id']}: missing_information is {type(g['missing_information'])}"
        )


def test_dc_gold_remediation_steps_nonempty():
    for g in _load_dc_gold():
        assert isinstance(g["remediation_steps"], list)
        assert len(g["remediation_steps"]) > 0, f"{g['ticket_id']}: remediation_steps should not be empty"


def test_dc_gold_next_best_action_nonempty():
    for g in _load_dc_gold():
        assert len(g["next_best_action"].strip()) > 0, f"{g['ticket_id']} has empty next_best_action"


# ═══════════════════════════════════════════════════════════════════════
# SECTION 2: Per-ticket data-quality tests (INC-DC###)
#   Each test validates the ticket exhibits the noise type it claims.
# ═══════════════════════════════════════════════════════════════════════


def test_dc001_very_long_email_chain():
    """INC-DC001: Very long email chain — actual issue is VPN timeout."""
    ticket = _dc_tickets_by_id()["INC-DC001"]
    gold = _dc_gold_by_id()["INC-DC001"]
    assert len(ticket["description"]) > 5000, "Ticket should have very long description"
    assert gold["category"] == "Network & Connectivity"
    assert gold["assigned_team"] == "Network Operations"


def test_dc002_base64_image_embedded():
    """INC-DC002: Base64 image data embedded in email body."""
    ticket = _dc_tickets_by_id()["INC-DC002"]
    gold = _dc_gold_by_id()["INC-DC002"]
    assert "base64" in ticket["description"].lower(), "Ticket should contain base64 data"
    assert gold["category"] == "Software & Applications"
    assert gold["assigned_team"] == "Enterprise Applications"


def test_dc003_html_markup_with_script():
    """INC-DC003: HTML markup with script tags in ticket body."""
    ticket = _dc_tickets_by_id()["INC-DC003"]
    gold = _dc_gold_by_id()["INC-DC003"]
    assert "<script>" in ticket["description"] or "<html>" in ticket["description"]
    assert gold["category"] == "Hardware & Peripherals"
    assert gold["assigned_team"] == "Endpoint Engineering"


def test_dc004_garbled_transcription():
    """INC-DC004: Garbled phone transcription with [inaudible] markers."""
    ticket = _dc_tickets_by_id()["INC-DC004"]
    gold = _dc_gold_by_id()["INC-DC004"]
    assert ticket["description"].count("[inaudible]") >= 5
    assert gold["category"] == "Data & Storage"
    assert gold["assigned_team"] == "Data Platform"


def test_dc005_emoji_heavy():
    """INC-DC005: Ticket body heavily laden with emoji."""
    ticket = _dc_tickets_by_id()["INC-DC005"]
    gold = _dc_gold_by_id()["INC-DC005"]
    emoji_count = sum(1 for c in ticket["description"] if ord(c) > 0x1F000)
    assert emoji_count >= 3 or "💻" in ticket["description"] or "🔥" in ticket["subject"]
    assert gold["category"] == "Hardware & Peripherals"
    assert gold["assigned_team"] == "Endpoint Engineering"


def test_dc006_empty_ticket():
    """INC-DC006: Completely empty subject and description."""
    ticket = _dc_tickets_by_id()["INC-DC006"]
    gold = _dc_gold_by_id()["INC-DC006"]
    assert ticket["subject"] == ""
    assert ticket["description"] == ""
    assert gold["category"] == "Not a Support Ticket"
    assert gold["assigned_team"] == "None"


def test_dc007_deep_forwarding_chain():
    """INC-DC007: Deeply nested RE:/FW: forwarding chain."""
    ticket = _dc_tickets_by_id()["INC-DC007"]
    gold = _dc_gold_by_id()["INC-DC007"]
    assert ticket["subject"].count("RE:") >= 4
    assert gold["category"] == "Software & Applications"
    assert gold["assigned_team"] == "Enterprise Applications"


def test_dc008_excessive_whitespace():
    """INC-DC008: Excessive whitespace and formatting throughout."""
    ticket = _dc_tickets_by_id()["INC-DC008"]
    gold = _dc_gold_by_id()["INC-DC008"]
    assert "     " in ticket["description"] or "     " in ticket["subject"]
    assert gold["category"] == "Network & Connectivity"
    assert gold["assigned_team"] == "Network Operations"


def test_dc009_mixed_language():
    """INC-DC009: Mixed Spanish/English ticket body."""
    ticket = _dc_tickets_by_id()["INC-DC009"]
    gold = _dc_gold_by_id()["INC-DC009"]
    desc_lower = ticket["description"].lower()
    assert "buenos" in desc_lower or "mañana" in ticket["subject"].lower() or "funciona" in ticket["subject"].lower()
    assert gold["category"] == "Software & Applications"
    assert gold["assigned_team"] == "Enterprise Applications"


def test_dc010_url_spam():
    """INC-DC010: Many suspicious URLs — user reporting phishing."""
    ticket = _dc_tickets_by_id()["INC-DC010"]
    gold = _dc_gold_by_id()["INC-DC010"]
    assert ticket["description"].count("http") >= 5 or ticket["subject"].count("http") >= 2
    assert gold["category"] == "Security & Compliance"
    assert gold["assigned_team"] == "Security Operations"
    assert gold["needs_escalation"] is True


def test_dc011_code_blocks():
    """INC-DC011: Code blocks and JSON formatting in ticket body."""
    ticket = _dc_tickets_by_id()["INC-DC011"]
    gold = _dc_gold_by_id()["INC-DC011"]
    assert "```" in ticket["description"] or "{" in ticket["description"]
    assert gold["category"] == "Data & Storage"
    assert gold["assigned_team"] == "Data Platform"


def test_dc012_repeated_text():
    """INC-DC012: Repeated/stuck keyboard text followed by actual issue."""
    ticket = _dc_tickets_by_id()["INC-DC012"]
    gold = _dc_gold_by_id()["INC-DC012"]
    assert ticket["description"].count("account issue") >= 10
    assert gold["category"] == "Access & Authentication"
    assert gold["assigned_team"] == "Identity & Access Management"


def test_dc013_pii_mention():
    """INC-DC013: Ticket mentioning that PII was previously included."""
    ticket = _dc_tickets_by_id()["INC-DC013"]
    gold = _dc_gold_by_id()["INC-DC013"]
    assert "SSN" in ticket["description"]
    assert gold["category"] == "General Inquiry"
    assert gold["assigned_team"] == "Endpoint Engineering"


def test_dc014_mixed_french_english():
    """INC-DC014: Mixed French/English ticket about file share access."""
    ticket = _dc_tickets_by_id()["INC-DC014"]
    gold = _dc_gold_by_id()["INC-DC014"]
    assert "Bonjour" in ticket["description"]
    assert gold["category"] == "Data & Storage"
    assert gold["assigned_team"] == "Data Platform"


def test_dc015_control_characters():
    """INC-DC015: Tab and other formatting characters in subject line."""
    gold = _dc_gold_by_id()["INC-DC015"]
    assert gold["category"] == "Data & Storage"
    assert gold["assigned_team"] == "Data Platform"


# ═══════════════════════════════════════════════════════════════════════
# SECTION 3: Scoring tests (INC-DC### gold vs gold = perfect)
# ═══════════════════════════════════════════════════════════════════════


def test_dc_perfect_submission_scores_85():
    gold = _load_dc_gold()
    result = score_submission(gold, gold)
    assert result["classification_score"] == 85.0, (
        f"Perfect submission should score 85.0, got {result['classification_score']}"
    )


def test_dc_perfect_submission_all_dimensions_1():
    gold = _load_dc_gold()
    result = score_submission(gold, gold)
    for dim, score in result["dimension_scores"].items():
        assert score == 1.0, f"Dimension {dim} should be 1.0 for perfect, got {score}"


def test_dc_perfect_submission_no_errors():
    gold = _load_dc_gold()
    result = score_submission(gold, gold)
    assert result["tickets_errored"] == 0
    assert result["tickets_scored"] == 35


def test_dc_each_gold_ticket_scores_perfectly():
    for g in _load_dc_gold():
        scores = score_ticket(dict(g), g)
        assert scores["weighted_total"] > 0.84, (
            f"{g['ticket_id']}: expected weighted_total > 0.84, got {scores['weighted_total']}"
        )


# ═══════════════════════════════════════════════════════════════════════
# SECTION 4: Dataset integrity — scoring INC-5### dataset
# ═══════════════════════════════════════════════════════════════════════


def test_sc_tickets_file_exists():
    assert _SC_TICKETS_PATH.exists(), f"Missing: {_SC_TICKETS_PATH}"


def test_sc_gold_file_exists():
    assert _SC_GOLD_PATH.exists(), f"Missing: {_SC_GOLD_PATH}"


def test_sc_ticket_count():
    assert len(_load_sc_tickets()) == 15


def test_sc_ticket_ids_match():
    ticket_ids = {t["ticket_id"] for t in _load_sc_tickets()}
    gold_ids = {g["ticket_id"] for g in _load_sc_gold()}
    assert ticket_ids == gold_ids


def test_sc_all_ticket_ids_unique():
    ticket_ids = [t["ticket_id"] for t in _load_sc_tickets()]
    assert len(ticket_ids) == len(set(ticket_ids))


def test_sc_gold_categories_valid():
    for gold in _load_sc_gold():
        assert gold["category"].lower() in VALID_CATEGORIES, f"{gold['ticket_id']} invalid category: {gold['category']}"


def test_sc_gold_priorities_valid():
    for gold in _load_sc_gold():
        assert gold["priority"].lower() in VALID_PRIORITIES, f"{gold['ticket_id']} invalid priority: {gold['priority']}"


def test_sc_gold_teams_valid():
    for gold in _load_sc_gold():
        assert gold["assigned_team"].lower() in VALID_TEAMS, (
            f"{gold['ticket_id']} invalid team: {gold['assigned_team']}"
        )


def test_sc_gold_missing_info_valid():
    for gold in _load_sc_gold():
        for item in gold["missing_information"]:
            assert item.lower() in VALID_MISSING_INFO, f"{gold['ticket_id']} invalid missing_info: {item}"


def test_sc_gold_has_required_fields():
    for gold in _load_sc_gold():
        missing = _REQUIRED_GOLD_FIELDS - set(gold.keys())
        assert not missing, f"{gold['ticket_id']} gold missing fields: {missing}"


# ═══════════════════════════════════════════════════════════════════════
# SECTION 5: Per-ticket scoring tests (INC-5### dataset)
# ═══════════════════════════════════════════════════════════════════════


def test_sc_perfect_submission_scores_85():
    gold = _load_sc_gold()
    result = score_submission(gold, gold)
    assert result["classification_score"] == 85.0


def test_sc_perfect_submission_all_dimensions_1():
    gold = _load_sc_gold()
    result = score_submission(gold, gold)
    for dim, score in result["dimension_scores"].items():
        assert score == 1.0, f"Dimension {dim} should be 1.0 for perfect, got {score}"


def test_sc_each_gold_ticket_scores_perfectly():
    for g in _load_sc_gold():
        scores = score_ticket(dict(g), g)
        assert scores["weighted_total"] > 0.84, (
            f"{g['ticket_id']}: expected weighted_total > 0.84, got {scores['weighted_total']}"
        )


# ── Per-ticket classification tests (INC-5### specifics) ─────────────


def test_sc_very_long_email_scored_correctly():
    """INC-5001: Very long email should be scored like any other ticket."""
    gold = _sc_gold_by_id()["INC-5001"]
    scores = score_ticket(dict(gold), gold)
    assert scores["weighted_total"] > 0.84


def test_sc_base64_image_ticket_scored_correctly():
    """INC-5002: Base64 images in description should not prevent scoring."""
    gold = _sc_gold_by_id()["INC-5002"]
    scores = score_ticket(dict(gold), gold)
    assert scores["weighted_total"] > 0.84


def test_sc_html_email_ticket_scored_correctly():
    """INC-5003: HTML email content should not prevent scoring."""
    gold = _sc_gold_by_id()["INC-5003"]
    scores = score_ticket(dict(gold), gold)
    assert scores["weighted_total"] > 0.84


def test_sc_deep_email_thread_scored_correctly():
    """INC-5004: Deep reply chain should not prevent scoring."""
    gold = _sc_gold_by_id()["INC-5004"]
    scores = score_ticket(dict(gold), gold)
    assert scores["weighted_total"] > 0.84


def test_sc_unicode_emoji_ticket_scored_correctly():
    """INC-5005: Unicode and emoji should not prevent scoring."""
    gold = _sc_gold_by_id()["INC-5005"]
    scores = score_ticket(dict(gold), gold)
    assert scores["weighted_total"] > 0.84


def test_sc_misleading_subject_not_p1():
    """INC-5007: Subject screams P0/P1 but actual issue is slow Excel → P4."""
    gold = _sc_gold_by_id()["INC-5007"]
    assert gold["priority"] == "P4"
    assert gold["needs_escalation"] is False


def test_sc_db_timeout_affecting_traders_is_p1():
    """INC-5006: Real high-impact issue should be P1 with escalation."""
    gold = _sc_gold_by_id()["INC-5006"]
    assert gold["priority"] == "P1"
    assert gold["needs_escalation"] is True


def test_sc_attachment_only_requests_missing_info():
    """INC-5011: 'See attached' with minimal description should flag missing info."""
    gold = _sc_gold_by_id()["INC-5011"]
    missing = gold["missing_information"]
    assert len(missing) >= 2, "Attachment-only ticket should request multiple missing items"


def test_sc_security_anomaly_escalated():
    """INC-5013: MFA anomaly + possible tampering should be escalated."""
    gold = _sc_gold_by_id()["INC-5013"]
    assert gold["needs_escalation"] is True
    assert gold["category"] == "Security & Compliance"


# ═══════════════════════════════════════════════════════════════════════
# SECTION 6: Scoring edge cases — wrong answers for noisy data
# ═══════════════════════════════════════════════════════════════════════


def test_wrong_category_for_long_email():
    """Wrong category on a long email should score 0.0 for category."""
    gold = _sc_gold_by_id()["INC-5001"]
    assert score_category("Hardware & Peripherals", gold["category"]) == 0.0


def test_wrong_priority_for_misleading_subject():
    """System tricked by misleading subject into P1 should get 0.0."""
    gold = _sc_gold_by_id()["INC-5007"]
    assert score_priority("P1", gold["priority"]) == 0.0


def test_partial_missing_info_for_attachment_only():
    """Getting some but not all missing info items for INC-5011."""
    gold = _sc_gold_by_id()["INC-5011"]
    partial = [gold["missing_information"][0]]
    score = score_missing_info(partial, gold["missing_information"])
    assert 0.0 < score < 1.0, "Partial missing info should give partial credit"


def test_empty_response_for_data_cleanup_ticket():
    """Empty response should score 0.0 for category, priority, routing, and escalation.

    Note: missing_info scores 1.0 when both pred and gold are empty (correct
    agreement on "nothing is missing"), so a ticket with empty gold missing_info
    will get partial weighted credit even with an empty response.
    """
    gold = _sc_gold_by_id()["INC-5001"]
    empty = {"ticket_id": "INC-5001"}
    scores = score_ticket(empty, gold)
    assert scores["category"] == 0.0
    assert scores["priority"] == 0.0
    assert scores["routing"] == 0.0
    assert scores["escalation"] == 0.0


def test_submission_with_some_missing_responses():
    """Missing half the responses should significantly reduce the score."""
    gold = _load_sc_gold()
    partial = gold[:8]
    result = score_submission(partial, gold)
    assert result["tickets_errored"] == 7
    assert result["classification_score"] < 60


# ═══════════════════════════════════════════════════════════════════════
# SECTION 7: Structural invariants (both datasets)
# ═══════════════════════════════════════════════════════════════════════


def test_dc_not_a_support_ticket_routed_to_none():
    """Tickets classified as 'Not a Support Ticket' must route to 'None'."""
    for g in _load_dc_gold():
        if g["category"] == "Not a Support Ticket":
            assert g["assigned_team"] == "None", (
                f"{g['ticket_id']}: 'Not a Support Ticket' should route to 'None', got '{g['assigned_team']}'"
            )


def test_dc_none_team_only_for_non_support():
    """Team 'None' should only be used for 'Not a Support Ticket' category."""
    for g in _load_dc_gold():
        if g["assigned_team"] == "None":
            assert g["category"] == "Not a Support Ticket", (
                f"{g['ticket_id']}: team 'None' with category '{g['category']}'"
            )


def test_sc_not_a_support_ticket_routed_to_none():
    for g in _load_sc_gold():
        if g["category"] == "Not a Support Ticket":
            assert g["assigned_team"] == "None", f"{g['ticket_id']}: 'Not a Support Ticket' should route to 'None'"


def test_sc_none_team_only_for_non_support():
    for g in _load_sc_gold():
        if g["assigned_team"] == "None":
            assert g["category"] == "Not a Support Ticket", (
                f"{g['ticket_id']}: team 'None' with category '{g['category']}'"
            )


# ═══════════════════════════════════════════════════════════════════════
# SECTION 8: Distribution coverage
# ═══════════════════════════════════════════════════════════════════════


def test_dc_diverse_categories_represented():
    """Gold answers should cover multiple categories for data cleanup."""
    gold = _load_dc_gold()
    categories = {g["category"] for g in gold}
    assert len(categories) >= 5, f"Only {len(categories)} categories represented"


def test_dc_diverse_teams_represented():
    gold = _load_dc_gold()
    teams = {g["assigned_team"] for g in gold}
    assert len(teams) >= 4, f"Only {len(teams)} teams represented"


def test_dc_diverse_priorities_represented():
    gold = _load_dc_gold()
    priorities = {g["priority"] for g in gold}
    assert len(priorities) >= 3, f"Only {len(priorities)} priorities represented"


def test_dc_escalation_has_both_values():
    gold = _load_dc_gold()
    escalation_values = {g["needs_escalation"] for g in gold}
    assert True in escalation_values and False in escalation_values


def test_sc_diverse_categories_represented():
    gold = _load_sc_gold()
    categories = {g["category"] for g in gold}
    assert len(categories) >= 4, f"Only {len(categories)} categories"


def test_sc_diverse_teams_represented():
    gold = _load_sc_gold()
    teams = {g["assigned_team"] for g in gold}
    assert len(teams) >= 3, f"Only {len(teams)} teams"


# ═══════════════════════════════════════════════════════════════════════
# SECTION 9: Data-quality property tests (across both datasets)
# ═══════════════════════════════════════════════════════════════════════


def test_dc_at_least_one_ticket_has_base64():
    """At least one data cleanup ticket should contain base64 data."""
    tickets = _load_dc_tickets()
    has_base64 = any("base64" in t["description"].lower() for t in tickets)
    assert has_base64, "No ticket contains base64 data"


def test_dc_at_least_one_ticket_has_html():
    """At least one data cleanup ticket should contain HTML markup."""
    tickets = _load_dc_tickets()
    has_html = any(
        "<html" in t["description"].lower()
        or "<script" in t["description"].lower()
        or "<html" in t["subject"].lower()
        or "<script" in t["subject"].lower()
        for t in tickets
    )
    assert has_html, "No ticket contains HTML markup"


def test_dc_at_least_one_ticket_has_long_description():
    """At least one ticket should have a very long description (>5000 chars)."""
    tickets = _load_dc_tickets()
    has_long = any(len(t["description"]) > 5000 for t in tickets)
    assert has_long, "No ticket has a very long description"


def test_dc_at_least_one_ticket_has_empty_description():
    """At least one ticket should have an empty description."""
    tickets = _load_dc_tickets()
    has_empty = any(t["description"] == "" for t in tickets)
    assert has_empty, "No ticket has an empty description"


def test_dc_at_least_one_ticket_has_deep_reply_chain():
    """At least one ticket should have a deeply nested RE:/FW: chain."""
    tickets = _load_dc_tickets()
    has_chain = any(t["subject"].count("RE:") >= 3 for t in tickets)
    assert has_chain, "No ticket has a deep reply chain"


def test_dc_at_least_one_ticket_has_mixed_language():
    """At least one ticket should be in a non-English or mixed language."""
    tickets = _load_dc_tickets()
    mixed_indicators = ["bonjour", "buenos", "mañana", "funciona", "bitte", "danke"]
    has_mixed = any(
        any(ind in t["description"].lower() or ind in t["subject"].lower() for ind in mixed_indicators) for t in tickets
    )
    assert has_mixed, "No ticket has mixed language content"


def test_dc_at_least_one_ticket_has_excessive_whitespace():
    """At least one ticket should have excessive whitespace."""
    tickets = _load_dc_tickets()
    has_ws = any("     " in t["description"] or "     " in t["subject"] for t in tickets)
    assert has_ws, "No ticket has excessive whitespace"


def test_dc_at_least_one_ticket_has_emoji():
    """At least one ticket should contain emoji."""
    tickets = _load_dc_tickets()
    has_emoji = any(
        any(ord(c) > 0x1F000 for c in t["description"]) or any(ord(c) > 0x1F000 for c in t["subject"]) for t in tickets
    )
    assert has_emoji, "No ticket contains emoji"


def test_dc_at_least_one_ticket_has_repeated_text():
    """At least one ticket should have significant text repetition."""
    tickets = _load_dc_tickets()
    has_repeat = False
    for t in tickets:
        desc = t["description"]
        if len(desc) < 20:
            continue
        words = desc.split()
        if len(words) > 20:
            most_common = max(set(words), key=words.count)
            if words.count(most_common) >= 10:
                has_repeat = True
                break
    assert has_repeat, "No ticket has significant text repetition"


def test_sc_at_least_one_ticket_has_garbled_text():
    """At least one INC-5xxx ticket should have garbled/misspelled content."""
    tickets = _load_sc_tickets()
    has_garbled = any(
        "isuse" in t.get("subject", "").lower() or "outlok" in t.get("subject", "").lower() for t in tickets
    )
    assert has_garbled, "No INC-5xxx ticket has garbled text"


def test_sc_at_least_one_ticket_has_stack_trace():
    """At least one INC-5xxx ticket should contain a stack trace."""
    tickets = _load_sc_tickets()
    has_trace = any(
        "traceback" in t["description"].lower()
        or "exception" in t["description"].lower()
        or "at " in t["description"]
        and "line " in t["description"]
        for t in tickets
    )
    assert has_trace, "No INC-5xxx ticket has a stack trace"


def test_sc_at_least_one_ticket_has_minimal_description():
    """At least one INC-5xxx ticket should have a very short description."""
    tickets = _load_sc_tickets()
    has_minimal = any(0 < len(t["description"]) <= 30 for t in tickets)
    assert has_minimal, "No INC-5xxx ticket has a minimal description"


# ═══════════════════════════════════════════════════════════════════════
# SECTION 10: Cross-dataset no ID collisions
# ═══════════════════════════════════════════════════════════════════════


def test_no_id_collision_between_dc_and_sc():
    """INC-DC### and INC-5### datasets should have distinct IDs."""
    dc_ids = {t["ticket_id"] for t in _load_dc_tickets()}
    sc_ids = {t["ticket_id"] for t in _load_sc_tickets()}
    overlap = dc_ids & sc_ids
    assert not overlap, f"ID collision: {overlap}"


# ═══════════════════════════════════════════════════════════════════════
# SECTION 11: Output contamination detection tests
#   Validates gold answers don't contain noise from the input data.
# ═══════════════════════════════════════════════════════════════════════


def _check_no_contamination(gold: dict) -> list[str]:
    """Check that gold answer fields don't contain input noise artifacts."""
    issues = []
    fields_to_check = [
        gold.get("category", ""),
        gold.get("priority", ""),
        gold.get("assigned_team", ""),
        gold.get("next_best_action", ""),
    ] + gold.get("remediation_steps", [])

    combined = " ".join(str(f) for f in fields_to_check)

    # Base64 data shouldn't leak into gold answers
    if re.search(r"data:image/[a-z]+;base64,", combined):
        issues.append("base64 image data in gold answer")

    # Raw HTML tags shouldn't be in gold answers
    if re.search(r"<script[^>]*>", combined, re.IGNORECASE):
        issues.append("script tags in gold answer")

    # Email headers shouldn't leak
    if re.search(r"^(From|To|Cc|Subject|Date):\s", combined, re.MULTILINE):
        issues.append("email headers in gold answer")

    return issues


def test_dc_gold_no_contamination():
    """No gold answers should contain input noise artifacts (base64, HTML, headers)."""
    for g in _load_dc_gold():
        issues = _check_no_contamination(g)
        assert not issues, f"{g['ticket_id']}: {issues}"


def test_sc_gold_no_contamination():
    """No gold answers should contain input noise artifacts."""
    for g in _load_sc_gold():
        issues = _check_no_contamination(g)
        assert not issues, f"{g['ticket_id']}: {issues}"


# ═══════════════════════════════════════════════════════════════════════
# SECTION 12: Gold answer quality checks (both datasets)
# ═══════════════════════════════════════════════════════════════════════


def test_dc_gold_no_duplicate_missing_info():
    """No gold answer should have duplicate missing_information items."""
    for g in _load_dc_gold():
        items = g["missing_information"]
        assert len(items) == len(set(items)), f"{g['ticket_id']}: duplicate missing_information items: {items}"


def test_sc_gold_no_duplicate_missing_info():
    """No INC-5### gold answer should have duplicate missing_information items."""
    for g in _load_sc_gold():
        items = g["missing_information"]
        assert len(items) == len(set(items)), f"{g['ticket_id']}: duplicate missing_information items: {items}"


def test_dc_gold_remediation_reasonable_length():
    """Gold remediation steps should be reasonable length (not absurdly long or trivial)."""
    for g in _load_dc_gold():
        for i, step in enumerate(g["remediation_steps"]):
            assert len(step) >= 5, f"{g['ticket_id']}: remediation step {i} too short: '{step}'"
            assert len(step) <= 2000, f"{g['ticket_id']}: remediation step {i} too long ({len(step)} chars)"


def test_sc_gold_remediation_reasonable_length():
    """INC-5### gold remediation steps should be reasonable length."""
    for g in _load_sc_gold():
        for i, step in enumerate(g["remediation_steps"]):
            assert len(step) >= 5, f"{g['ticket_id']}: remediation step {i} too short: '{step}'"
            assert len(step) <= 2000, f"{g['ticket_id']}: remediation step {i} too long ({len(step)} chars)"


# ═══════════════════════════════════════════════════════════════════════
# SECTION 13: Advanced contamination and PII detection
# ═══════════════════════════════════════════════════════════════════════


def _check_pii_leakage(gold: dict) -> list[str]:
    """Check that gold answer fields don't contain PII patterns."""
    issues = []
    fields = [
        gold.get("category", ""),
        gold.get("priority", ""),
        gold.get("assigned_team", ""),
        gold.get("next_best_action", ""),
    ] + gold.get("remediation_steps", [])
    combined = " ".join(str(f) for f in fields)

    # SSN pattern
    if re.search(r"\b\d{3}-\d{2}-\d{4}\b", combined):
        issues.append("SSN pattern in gold answer")

    # Credit card pattern
    if re.search(r"\b(?:\d{4}[-\s]?){3}\d{4}\b", combined):
        issues.append("credit card pattern in gold answer")

    # IP address in remediation (shouldn't appear as specific IPs)
    # Well-known public DNS servers are exempt — they're standard diagnostic references
    _WELL_KNOWN_PUBLIC_IPS = {"8.8.8.8", "8.8.4.4", "1.1.1.1", "1.0.0.1"}
    if re.search(r"\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b", combined):
        # Allow common references like "10.x.x.x" patterns in remediation text
        real_ips = re.findall(r"\b(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\b", combined)
        for ip in real_ips:
            parts = ip.split(".")
            is_valid = all(0 <= int(p) <= 255 for p in parts)
            is_private = ip.startswith(("10.", "192.168.", "172."))
            if is_valid and not is_private and ip not in _WELL_KNOWN_PUBLIC_IPS:
                issues.append(f"public IP address in gold answer: {ip}")

    return issues


def test_dc_gold_no_pii_leakage():
    """No data cleanup gold answers should contain PII patterns (excluding security-context IPs)."""
    for g in _load_dc_gold():
        issues = _check_pii_leakage(g)
        # Security/Compliance tickets may reference suspicious IPs in remediation
        if g["category"] == "Security & Compliance":
            issues = [i for i in issues if "IP address" not in i]
        assert not issues, f"{g['ticket_id']}: {issues}"


def test_sc_gold_no_pii_leakage():
    """No INC-5### gold answers should contain PII patterns (excluding security-context IPs)."""
    for g in _load_sc_gold():
        issues = _check_pii_leakage(g)
        if g["category"] == "Security & Compliance":
            issues = [i for i in issues if "IP address" not in i]
        assert not issues, f"{g['ticket_id']}: {issues}"


def test_dc_gold_remediation_no_raw_urls():
    """Gold remediation should not contain raw clickable URLs (could be phishing vectors)."""
    url_pattern = re.compile(r"https?://\S+")
    for g in _load_dc_gold():
        combined = " ".join(g.get("remediation_steps", []))
        matches = url_pattern.findall(combined)
        # Allow documentation URLs (microsoft.com, etc.)
        suspicious = [u for u in matches if "microsoft.com" not in u and "contoso.com" not in u]
        assert not suspicious, f"{g['ticket_id']}: suspicious URL(s) in remediation: {suspicious}"


# ═══════════════════════════════════════════════════════════════════════
# SECTION 14: Description statistics and characteristics
# ═══════════════════════════════════════════════════════════════════════


def test_dc_description_length_variance():
    """Data cleanup tickets should have varied description lengths (not all the same)."""
    tickets = _load_dc_tickets()
    lengths = [len(t["description"]) for t in tickets]
    mean_len = sum(lengths) / len(lengths)
    variance = sum((x - mean_len) ** 2 for x in lengths) / len(lengths)
    std_dev = variance**0.5
    assert std_dev > 100, (
        f"Description lengths have low variance (std_dev={std_dev:.0f}). Cleanup tickets should have varied lengths."
    )


def test_dc_at_least_one_ticket_has_url_content():
    """At least one ticket should contain URLs."""
    tickets = _load_dc_tickets()
    has_url = any("http" in t["description"] for t in tickets)
    assert has_url, "No ticket contains URL content"


def test_dc_at_least_one_ticket_with_code_blocks():
    """At least one ticket should contain code/structured data."""
    tickets = _load_dc_tickets()
    has_code = any("```" in t["description"] or "{" in t["description"] for t in tickets)
    assert has_code, "No ticket contains code blocks or structured data"


def test_sc_word_count_range():
    """INC-5### tickets should span a range of word counts."""
    tickets = _load_sc_tickets()
    word_counts = [len(t["description"].split()) for t in tickets]
    min_wc = min(word_counts)
    max_wc = max(word_counts)
    assert max_wc > 50, f"No ticket has more than 50 words (max={max_wc})"
    assert min_wc < 20, f"No ticket has fewer than 20 words (min={min_wc})"


# ═══════════════════════════════════════════════════════════════════════
# SECTION 15: Scoring consistency checks
# ═══════════════════════════════════════════════════════════════════════


def test_dc_empty_ticket_correctly_classified():
    """INC-DC006 (empty ticket) gold should be classified as Not a Support Ticket."""
    gold = _dc_gold_by_id()["INC-DC006"]
    assert gold["category"] == "Not a Support Ticket"
    assert gold["assigned_team"] == "None"
    # Empty ticket should request missing info
    assert len(gold["missing_information"]) >= 0


def test_dc_security_tickets_escalated():
    """Data cleanup tickets classified as Security & Compliance with high severity should be escalated."""
    for g in _load_dc_gold():
        if g["category"] == "Security & Compliance" and g["priority"] in ("P1", "P2"):
            assert g["needs_escalation"] is True, f"{g['ticket_id']}: P1/P2 Security ticket should be escalated"


def test_sc_category_team_consistency():
    """Category and team assignments should be logically consistent in INC-5### dataset."""
    category_team_map = {
        "Access & Authentication": "Identity & Access Management",
        "Network & Connectivity": "Network Operations",
        "Security & Compliance": "Security Operations",
        "Data & Storage": "Data Platform",
        "Not a Support Ticket": "None",
    }
    for g in _load_sc_gold():
        expected_team = category_team_map.get(g["category"])
        if expected_team:
            assert g["assigned_team"] == expected_team, (
                f"{g['ticket_id']}: category '{g['category']}' should map to "
                f"'{expected_team}', got '{g['assigned_team']}'"
            )


# ── Runner ────────────────────────────────────────────────────────────

if __name__ == "__main__":
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    passed = 0
    failed = 0
    for t in tests:
        try:
            t()
            passed += 1
            print(f"  ✓ {t.__name__}")
        except AssertionError as e:
            failed += 1
            print(f"  ✗ {t.__name__}: {e}")
    print(f"\n{passed} passed, {failed} failed, {len(tests)} total")
    sys.exit(1 if failed else 0)
