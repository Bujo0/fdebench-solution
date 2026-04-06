#!/usr/bin/env python3
"""Evaluation tests for data cleanup scenarios.

Tests that the triage system correctly handles messy, noisy, and malformed
input data that commonly appears in real-world IT support tickets — including
very long emails, embedded base64 images, HTML content, deep email threads,
Unicode/emoji, repeated text, and garbled input.

These tests validate two things:
  1. The scoring pipeline correctly evaluates predictions against the gold
     standard for data cleanup scenarios (using the same scoring functions
     as test_scoring.py).
  2. The gold-standard answers themselves represent reasonable triage
     decisions for noisy input data.

Usage:
    cd docs/eval
    python test_data_cleanup.py

    # Or with pytest:
    uv run pytest test_data_cleanup.py -v

    # Run against a live endpoint:
    uv run python run_eval.py \
        --endpoint http://localhost:8000 \
        --dataset ../data/tickets/eval_data_cleanup.json \
        --gold ../data/tickets/eval_data_cleanup_gold.json
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, ".")  # noqa: TID251

from run_eval import CATEGORIES
from run_eval import TEAMS
from run_eval import score_category
from run_eval import score_escalation
from run_eval import score_missing_info
from run_eval import score_priority
from run_eval import score_routing
from run_eval import score_submission
from run_eval import score_ticket

# ── Paths ────────────────────────────────────────────────────────────

_DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "tickets"
_TICKETS_PATH = _DATA_DIR / "eval_data_cleanup.json"
_GOLD_PATH = _DATA_DIR / "eval_data_cleanup_gold.json"

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


# ── Helper: load datasets ───────────────────────────────────────────


def _load_tickets() -> list[dict]:
    return json.loads(_TICKETS_PATH.read_text())


def _load_gold() -> list[dict]:
    return json.loads(_GOLD_PATH.read_text())


def _gold_by_id() -> dict[str, dict]:
    return {g["ticket_id"]: g for g in _load_gold()}


# ── Dataset integrity tests ─────────────────────────────────────────


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
    assert len(ticket_ids) == len(set(ticket_ids)), "Duplicate ticket IDs in dataset"


def test_ticket_count():
    """Dataset should contain 15 data cleanup scenarios."""
    assert len(_load_tickets()) == 15


# ── Input schema validation ──────────────────────────────────────────


def test_all_tickets_have_required_fields():
    required = {"ticket_id", "subject", "description", "reporter", "created_at", "channel"}
    for ticket in _load_tickets():
        missing = required - set(ticket.keys())
        assert not missing, f"{ticket['ticket_id']} missing fields: {missing}"


def test_all_reporters_have_required_fields():
    required = {"name", "email", "department"}
    for ticket in _load_tickets():
        missing = required - set(ticket["reporter"].keys())
        assert not missing, f"{ticket['ticket_id']} reporter missing fields: {missing}"


def test_all_channels_valid():
    valid_channels = {"email", "chat", "portal", "phone"}
    for ticket in _load_tickets():
        assert ticket["channel"] in valid_channels, (
            f"{ticket['ticket_id']} invalid channel: {ticket['channel']}"
        )


def test_ticket_ids_follow_pattern():
    for ticket in _load_tickets():
        tid = ticket["ticket_id"]
        assert tid.startswith("INC-"), f"Invalid ticket ID format: {tid}"


# ── Gold answer validation ───────────────────────────────────────────


def test_gold_categories_valid():
    for gold in _load_gold():
        assert gold["category"].lower() in VALID_CATEGORIES, (
            f"{gold['ticket_id']} invalid category: {gold['category']}"
        )


def test_gold_priorities_valid():
    for gold in _load_gold():
        assert gold["priority"].lower() in VALID_PRIORITIES, (
            f"{gold['ticket_id']} invalid priority: {gold['priority']}"
        )


def test_gold_teams_valid():
    for gold in _load_gold():
        assert gold["assigned_team"].lower() in VALID_TEAMS, (
            f"{gold['ticket_id']} invalid team: {gold['assigned_team']}"
        )


def test_gold_escalation_is_boolean():
    for gold in _load_gold():
        assert isinstance(gold["needs_escalation"], bool), (
            f"{gold['ticket_id']} escalation is not boolean: {type(gold['needs_escalation'])}"
        )


def test_gold_missing_info_values_valid():
    for gold in _load_gold():
        for item in gold["missing_information"]:
            assert item.lower() in VALID_MISSING_INFO, (
                f"{gold['ticket_id']} invalid missing_info: {item}"
            )


def test_gold_has_required_output_fields():
    required = {
        "ticket_id",
        "category",
        "priority",
        "assigned_team",
        "needs_escalation",
        "missing_information",
        "next_best_action",
        "remediation_steps",
    }
    for gold in _load_gold():
        missing = required - set(gold.keys())
        assert not missing, f"{gold['ticket_id']} gold missing fields: {missing}"


def test_gold_remediation_steps_nonempty():
    for gold in _load_gold():
        assert len(gold["remediation_steps"]) > 0, (
            f"{gold['ticket_id']} has empty remediation_steps"
        )


def test_gold_next_best_action_nonempty():
    for gold in _load_gold():
        assert len(gold["next_best_action"].strip()) > 0, (
            f"{gold['ticket_id']} has empty next_best_action"
        )


# ── Perfect-prediction scoring tests ─────────────────────────────────


def test_perfect_submission_scores_85():
    gold = _load_gold()
    result = score_submission(gold, gold)
    assert result["classification_score"] == 85.0, (
        f"Perfect submission should score 85.0, got {result['classification_score']}"
    )


def test_perfect_submission_all_dimensions_1():
    gold = _load_gold()
    result = score_submission(gold, gold)
    for dim, score in result["dimension_scores"].items():
        assert score == 1.0, f"Dimension {dim} should be 1.0 for perfect, got {score}"


def test_perfect_submission_no_errors():
    gold = _load_gold()
    result = score_submission(gold, gold)
    assert result["tickets_errored"] == 0
    assert result["tickets_scored"] == 15


# ── Per-ticket scoring for data cleanup scenarios ────────────────────


def test_very_long_email_scored_correctly():
    """INC-5001: Very long email should be scored like any other ticket."""
    gold_map = _gold_by_id()
    gold = gold_map["INC-5001"]
    scores = score_ticket(dict(gold), gold)
    assert scores["weighted_total"] > 0.84


def test_base64_image_ticket_scored_correctly():
    """INC-5002: Base64 images in description should not prevent scoring."""
    gold_map = _gold_by_id()
    gold = gold_map["INC-5002"]
    scores = score_ticket(dict(gold), gold)
    assert scores["weighted_total"] > 0.84


def test_html_email_ticket_scored_correctly():
    """INC-5003: HTML email content should not prevent scoring."""
    gold_map = _gold_by_id()
    gold = gold_map["INC-5003"]
    scores = score_ticket(dict(gold), gold)
    assert scores["weighted_total"] > 0.84


def test_deep_email_thread_scored_correctly():
    """INC-5004: Deep reply chain should not prevent scoring."""
    gold_map = _gold_by_id()
    gold = gold_map["INC-5004"]
    scores = score_ticket(dict(gold), gold)
    assert scores["weighted_total"] > 0.84


def test_unicode_emoji_ticket_scored_correctly():
    """INC-5005: Unicode and emoji should not prevent scoring."""
    gold_map = _gold_by_id()
    gold = gold_map["INC-5005"]
    scores = score_ticket(dict(gold), gold)
    assert scores["weighted_total"] > 0.84


def test_repeated_content_scored_correctly():
    """INC-5006: Duplicate/repeated text should not prevent scoring."""
    gold_map = _gold_by_id()
    gold = gold_map["INC-5006"]
    scores = score_ticket(dict(gold), gold)
    assert scores["weighted_total"] > 0.84


def test_misleading_subject_scored_correctly():
    """INC-5007: Extremely long misleading subject vs simple actual issue."""
    gold_map = _gold_by_id()
    gold = gold_map["INC-5007"]
    scores = score_ticket(dict(gold), gold)
    assert scores["weighted_total"] > 0.84


def test_url_heavy_ticket_scored_correctly():
    """INC-5008: Many URLs in description should not prevent scoring."""
    gold_map = _gold_by_id()
    gold = gold_map["INC-5008"]
    scores = score_ticket(dict(gold), gold)
    assert scores["weighted_total"] > 0.84


def test_mixed_language_scored_correctly():
    """INC-5009: Mixed English/French should not prevent scoring."""
    gold_map = _gold_by_id()
    gold = gold_map["INC-5009"]
    scores = score_ticket(dict(gold), gold)
    assert scores["weighted_total"] > 0.84


def test_stack_trace_scored_correctly():
    """INC-5010: Stack trace dump should not prevent scoring."""
    gold_map = _gold_by_id()
    gold = gold_map["INC-5010"]
    scores = score_ticket(dict(gold), gold)
    assert scores["weighted_total"] > 0.84


def test_attachment_only_scored_correctly():
    """INC-5011: 'See attached' with minimal description."""
    gold_map = _gold_by_id()
    gold = gold_map["INC-5011"]
    scores = score_ticket(dict(gold), gold)
    assert scores["weighted_total"] > 0.84


def test_garbled_text_scored_correctly():
    """INC-5012: Misspelled/garbled text should not prevent scoring."""
    gold_map = _gold_by_id()
    gold = gold_map["INC-5012"]
    scores = score_ticket(dict(gold), gold)
    assert scores["weighted_total"] > 0.84


def test_base64_log_data_scored_correctly():
    """INC-5013: Base64 encoded log data mixed with description."""
    gold_map = _gold_by_id()
    gold = gold_map["INC-5013"]
    scores = score_ticket(dict(gold), gold)
    assert scores["weighted_total"] > 0.84


def test_json_payload_scored_correctly():
    """INC-5014: JSON payload embedded in description."""
    gold_map = _gold_by_id()
    gold = gold_map["INC-5014"]
    scores = score_ticket(dict(gold), gold)
    assert scores["weighted_total"] > 0.84


def test_email_headers_scored_correctly():
    """INC-5015: Email headers pasted into body."""
    gold_map = _gold_by_id()
    gold = gold_map["INC-5015"]
    scores = score_ticket(dict(gold), gold)
    assert scores["weighted_total"] > 0.84


# ── Data-quality-specific gold validation ────────────────────────────


def test_misleading_subject_not_p1():
    """INC-5007: Subject screams P0/P1 but actual issue is slow Excel → P4."""
    gold_map = _gold_by_id()
    assert gold_map["INC-5007"]["priority"] == "P4"
    assert gold_map["INC-5007"]["needs_escalation"] is False


def test_db_timeout_affecting_150_traders_is_p1():
    """INC-5006: Real high-impact issue should be P1 with escalation."""
    gold_map = _gold_by_id()
    assert gold_map["INC-5006"]["priority"] == "P1"
    assert gold_map["INC-5006"]["needs_escalation"] is True


def test_attachment_only_requests_missing_info():
    """INC-5011: 'See attached' without description should flag missing info."""
    gold_map = _gold_by_id()
    missing = gold_map["INC-5011"]["missing_information"]
    assert len(missing) >= 2, "Attachment-only ticket should request multiple missing items"


def test_security_anomaly_escalated():
    """INC-5013: MFA anomaly + possible tampering should be escalated."""
    gold_map = _gold_by_id()
    assert gold_map["INC-5013"]["needs_escalation"] is True
    assert gold_map["INC-5013"]["category"] == "Security & Compliance"


def test_diverse_categories_represented():
    """Gold answers should cover multiple categories for data cleanup."""
    gold = _load_gold()
    categories = {g["category"] for g in gold}
    assert len(categories) >= 5, f"Only {len(categories)} categories represented"


def test_diverse_teams_represented():
    """Gold answers should cover multiple teams."""
    gold = _load_gold()
    teams = {g["assigned_team"] for g in gold}
    assert len(teams) >= 4, f"Only {len(teams)} teams represented"


def test_diverse_priorities_represented():
    """Gold answers should cover multiple priority levels."""
    gold = _load_gold()
    priorities = {g["priority"] for g in gold}
    assert len(priorities) >= 3, f"Only {len(priorities)} priorities represented"


def test_escalation_has_both_true_and_false():
    """Gold answers should include both escalated and non-escalated tickets."""
    gold = _load_gold()
    escalation_values = {g["needs_escalation"] for g in gold}
    assert True in escalation_values and False in escalation_values


# ── Scoring edge cases specific to noisy data ────────────────────────


def test_wrong_category_for_long_email():
    """Wrong category on a long email should score 0.0 for category."""
    gold_map = _gold_by_id()
    gold = gold_map["INC-5001"]
    wrong = dict(gold)
    wrong["category"] = "Hardware & Peripherals"
    assert score_category(wrong["category"], gold["category"]) == 0.0


def test_wrong_priority_for_misleading_subject():
    """System tricked by misleading subject into P1 should get 0.0."""
    gold_map = _gold_by_id()
    gold = gold_map["INC-5007"]
    assert score_priority("P1", gold["priority"]) == 0.0


def test_partial_missing_info_for_attachment_only():
    """Getting some but not all missing info items for INC-5011."""
    gold_map = _gold_by_id()
    gold = gold_map["INC-5011"]
    partial = [gold["missing_information"][0]]
    score = score_missing_info(partial, gold["missing_information"])
    assert 0.0 < score < 1.0, "Partial missing info should give partial credit"


def test_empty_response_for_data_cleanup_ticket():
    """Empty response should score 0.0 for category, priority, routing, and escalation.

    Note: missing_info scores 1.0 when both pred and gold are empty (correct
    agreement on "nothing is missing"), so a ticket with empty gold missing_info
    will get partial weighted credit even with an empty response.
    """
    gold_map = _gold_by_id()
    gold = gold_map["INC-5001"]
    empty = {"ticket_id": "INC-5001"}
    scores = score_ticket(empty, gold)
    assert scores["category"] == 0.0
    assert scores["priority"] == 0.0
    assert scores["routing"] == 0.0
    assert scores["escalation"] == 0.0


def test_submission_with_some_missing_responses():
    """Missing half the responses should significantly reduce the score."""
    gold = _load_gold()
    partial = gold[:8]
    result = score_submission(partial, gold)
    assert result["tickets_errored"] == 7
    assert result["classification_score"] < 60


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
