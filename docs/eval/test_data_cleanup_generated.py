#!/usr/bin/env python3
"""Evaluation tests for the LARGE data cleanup dataset (eval_data_cleanup).

Validates dataset integrity, gold-answer correctness, distribution properties,
and data-quality characteristics across 235+ generated tickets covering noisy,
malformed, and degraded input.

Test categories:
  1. Dataset integrity — counts, IDs, schema compliance
  2. Gold answer validation — all values within constrained vocabulary
  3. Scoring sanity — gold vs gold = perfect score
  4. Distribution coverage — every category/team/priority is represented
  5. Data-quality characteristics — tickets actually contain the noise they claim
  6. Cross-dataset consistency — no overlap with handcrafted 15-ticket set
  7. Robustness property checks — structural invariants

Usage:
    cd docs/eval
    python test_data_cleanup_generated.py

    # Or with pytest:
    uv run pytest test_data_cleanup_generated.py -v
"""

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, ".")  # noqa: TID251

from run_eval import CATEGORIES
from run_eval import TEAMS
from run_eval import score_submission
from run_eval import score_ticket

# ── Load datasets ────────────────────────────────────────────────────

_DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "tickets"
_TICKETS_PATH = _DATA_DIR / "eval_data_cleanup.json"
_GOLD_PATH = _DATA_DIR / "eval_data_cleanup_gold.json"

_TICKETS: list[dict] = json.loads(_TICKETS_PATH.read_text())
_GOLD: list[dict] = json.loads(_GOLD_PATH.read_text())
_GOLD_BY_ID: dict[str, dict] = {g["ticket_id"]: g for g in _GOLD}
_TICKETS_BY_ID: dict[str, dict] = {t["ticket_id"]: t for t in _TICKETS}

# Valid values from the output schema
_VALID_CATEGORIES = set(CATEGORIES)
_VALID_TEAMS = set(TEAMS)
_VALID_PRIORITIES = {"P1", "P2", "P3", "P4"}
_VALID_MISSING_INFO = {
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
_REQUIRED_FIELDS = {
    "ticket_id",
    "category",
    "priority",
    "assigned_team",
    "needs_escalation",
    "missing_information",
    "next_best_action",
    "remediation_steps",
}
_REQUIRED_INPUT_FIELDS = {
    "ticket_id",
    "subject",
    "description",
    "reporter",
    "created_at",
    "channel",
}
_VALID_CHANNELS = {"email", "chat", "portal", "phone"}


# ── 1. Dataset integrity tests ───────────────────────────────────────


def test_dataset_has_at_least_200_tickets():
    assert len(_TICKETS) >= 200, f"Expected ≥200 data cleanup tickets, got {len(_TICKETS)}"


def test_gold_count_matches_ticket_count():
    assert len(_GOLD) == len(_TICKETS), f"Gold count ({len(_GOLD)}) != ticket count ({len(_TICKETS)})"


def test_ticket_ids_match_between_tickets_and_gold():
    ticket_ids = {t["ticket_id"] for t in _TICKETS}
    gold_ids = {g["ticket_id"] for g in _GOLD}
    assert ticket_ids == gold_ids, f"Mismatched IDs: {ticket_ids.symmetric_difference(gold_ids)}"


def test_all_ticket_ids_follow_inc_prefix():
    for t in _TICKETS:
        assert re.match(r"^INC-\d+$", t["ticket_id"]), f"Bad ticket_id format: {t['ticket_id']}"


def test_no_duplicate_ticket_ids():
    ids = [t["ticket_id"] for t in _TICKETS]
    assert len(ids) == len(set(ids)), "Duplicate ticket IDs found"


def test_ticket_id_ordering_matches():
    """Ticket and gold files should be in the same order."""
    for t, g in zip(_TICKETS, _GOLD, strict=True):
        assert t["ticket_id"] == g["ticket_id"], f"Ordering mismatch: ticket {t['ticket_id']} vs gold {g['ticket_id']}"


# ── 2. Gold answer validation ────────────────────────────────────────


def test_gold_categories_all_valid():
    for g in _GOLD:
        assert g["category"] in _VALID_CATEGORIES, f"{g['ticket_id']}: invalid category '{g['category']}'"


def test_gold_priorities_all_valid():
    for g in _GOLD:
        assert g["priority"] in _VALID_PRIORITIES, f"{g['ticket_id']}: invalid priority '{g['priority']}'"


def test_gold_teams_all_valid():
    for g in _GOLD:
        assert g["assigned_team"] in _VALID_TEAMS, f"{g['ticket_id']}: invalid team '{g['assigned_team']}'"


def test_gold_missing_info_all_valid():
    for g in _GOLD:
        for item in g["missing_information"]:
            assert item in _VALID_MISSING_INFO, f"{g['ticket_id']}: invalid missing_information value '{item}'"


def test_gold_schema_fields_present():
    for g in _GOLD:
        missing = _REQUIRED_FIELDS - set(g.keys())
        assert not missing, f"{g['ticket_id']}: missing fields {missing}"


def test_gold_escalation_is_boolean():
    for g in _GOLD:
        assert isinstance(g["needs_escalation"], bool), (
            f"{g['ticket_id']}: needs_escalation is {type(g['needs_escalation'])}"
        )


def test_gold_missing_info_is_list():
    for g in _GOLD:
        assert isinstance(g["missing_information"], list), (
            f"{g['ticket_id']}: missing_information is {type(g['missing_information'])}"
        )


def test_gold_remediation_steps_is_nonempty_list():
    for g in _GOLD:
        assert isinstance(g["remediation_steps"], list), (
            f"{g['ticket_id']}: remediation_steps is {type(g['remediation_steps'])}"
        )
        assert len(g["remediation_steps"]) > 0, f"{g['ticket_id']}: remediation_steps should not be empty"


def test_gold_next_best_action_nonempty():
    for g in _GOLD:
        assert g.get("next_best_action", "").strip(), f"{g['ticket_id']}: next_best_action is empty"


# ── 3. Scoring sanity (gold vs gold = perfect) ──────────────────────


def test_perfect_submission_scores_85():
    result = score_submission(_GOLD, _GOLD)
    assert result["classification_score"] == 85.0, (
        f"Perfect submission should score 85.0, got {result['classification_score']}"
    )


def test_perfect_submission_no_errors():
    result = score_submission(_GOLD, _GOLD)
    assert result["tickets_errored"] == 0


def test_each_gold_ticket_scores_above_threshold():
    for g in _GOLD:
        scores = score_ticket(dict(g), g)
        assert scores["weighted_total"] > 0.84, (
            f"{g['ticket_id']}: expected weighted_total > 0.84, got {scores['weighted_total']}"
        )


# ── 4. Distribution coverage ────────────────────────────────────────


def test_at_least_5_categories_represented():
    """Data cleanup tickets should span many categories, not just one."""
    cats = {g["category"] for g in _GOLD}
    assert len(cats) >= 5, f"Only {len(cats)} categories represented: {cats}"


def test_at_least_4_teams_represented():
    teams = {g["assigned_team"] for g in _GOLD}
    assert len(teams) >= 4, f"Only {len(teams)} teams represented: {teams}"


def test_all_priority_levels_represented():
    pris = {g["priority"] for g in _GOLD}
    assert pris == _VALID_PRIORITIES, f"Missing priorities: {_VALID_PRIORITIES - pris}"


def test_both_escalation_values_present():
    esc_vals = {g["needs_escalation"] for g in _GOLD}
    assert True in esc_vals, "No escalated tickets in dataset"
    assert False in esc_vals, "No non-escalated tickets in dataset"


def test_multiple_channels_represented():
    channels = {t["channel"] for t in _TICKETS}
    assert len(channels) >= 3, f"Only {len(channels)} channels: {channels}"


def test_missing_info_variety():
    """Multiple different missing_information values should appear across tickets."""
    all_missing = set()
    for g in _GOLD:
        all_missing.update(g["missing_information"])
    assert len(all_missing) >= 8, f"Only {len(all_missing)} unique missing_information values across dataset"


# ── 5. Data-quality characteristics ─────────────────────────────────


def test_some_tickets_have_very_long_descriptions():
    """At least some tickets should have very long descriptions (> 3000 chars)."""
    long_tickets = [t for t in _TICKETS if len(t["description"]) > 3000]
    assert len(long_tickets) >= 5, f"Expected ≥5 tickets with very long descriptions, got {len(long_tickets)}"


def test_some_tickets_contain_base64_data():
    """At least some tickets should contain base64-encoded data."""
    b64_pattern = re.compile(r"[A-Za-z0-9+/]{50,}={0,2}")
    b64_tickets = [t for t in _TICKETS if b64_pattern.search(t["description"])]
    assert len(b64_tickets) >= 3, f"Expected ≥3 tickets with base64 data, got {len(b64_tickets)}"


def test_some_tickets_contain_html_markup():
    """At least some tickets should contain HTML tags."""
    html_pattern = re.compile(r"<[a-zA-Z][^>]*>")
    html_tickets = [t for t in _TICKETS if html_pattern.search(t["description"])]
    assert len(html_tickets) >= 3, f"Expected ≥3 tickets with HTML markup, got {len(html_tickets)}"


def test_some_tickets_contain_code_blocks():
    """At least some tickets should contain code/logs."""
    code_tickets = [
        t
        for t in _TICKETS
        if "```" in t["description"] or "Traceback" in t["description"] or "Exception" in t["description"]
    ]
    assert len(code_tickets) >= 3, f"Expected ≥3 tickets with code/logs, got {len(code_tickets)}"


def test_some_tickets_have_emoji():
    """At least some tickets should contain emoji characters."""
    emoji_pattern = re.compile(r"[\U0001F600-\U0001F9FF\U00002600-\U000027BF\U0001FA00-\U0001FA6F]")
    emoji_tickets = [t for t in _TICKETS if emoji_pattern.search(t["description"])]
    assert len(emoji_tickets) >= 2, f"Expected ≥2 tickets with emoji, got {len(emoji_tickets)}"


def test_some_tickets_have_non_english_text():
    """At least some tickets should contain non-English text."""
    non_english_patterns = [
        re.compile(r"[À-ɏ]"),  # Latin Extended (accents)
        re.compile(r"[Ѐ-ӿ]"),  # Cyrillic
        re.compile(r"[一-鿿]"),  # CJK
    ]
    non_eng_tickets = [t for t in _TICKETS if any(p.search(t["description"]) for p in non_english_patterns)]
    assert len(non_eng_tickets) >= 2, f"Expected ≥2 tickets with non-English text, got {len(non_eng_tickets)}"


def test_some_tickets_have_excessive_whitespace():
    """At least some tickets should contain excessive whitespace/formatting."""
    ws_tickets = [t for t in _TICKETS if "\n\n\n" in t["description"] or "     " in t["description"]]
    assert len(ws_tickets) >= 3, f"Expected ≥3 tickets with excessive whitespace, got {len(ws_tickets)}"


def test_average_description_length_above_500():
    """Cleanup tickets should be substantive, not trivial."""
    avg = sum(len(t["description"]) for t in _TICKETS) / len(_TICKETS)
    assert avg > 500, f"Average description length is only {avg:.0f} chars"


# ── 6. Cross-dataset consistency ─────────────────────────────────────


def test_no_overlap_with_handcrafted_set():
    """Generated dataset should not contain any IDs from the 15-ticket handcrafted set."""
    handcrafted_path = _DATA_DIR / "data_cleanup_eval.json"
    if not handcrafted_path.exists():
        return  # Skip if handcrafted set doesn't exist
    handcrafted = json.loads(handcrafted_path.read_text())
    hc_ids = {t["ticket_id"] for t in handcrafted}
    gen_ids = {t["ticket_id"] for t in _TICKETS}
    overlap = hc_ids & gen_ids
    assert not overlap, f"Overlap with handcrafted set: {overlap}"


# ── 7. Robustness property checks ───────────────────────────────────


def test_all_tickets_have_required_input_fields():
    for t in _TICKETS:
        missing = _REQUIRED_INPUT_FIELDS - set(t.keys())
        assert not missing, f"{t['ticket_id']}: missing input fields {missing}"


def test_all_reporters_have_required_fields():
    for t in _TICKETS:
        reporter = t["reporter"]
        for field in ("name", "email", "department"):
            assert field in reporter, f"{t['ticket_id']}: reporter missing {field}"


def test_all_channels_are_valid():
    for t in _TICKETS:
        assert t["channel"] in _VALID_CHANNELS, f"{t['ticket_id']}: invalid channel '{t['channel']}'"


def test_not_a_support_ticket_routed_to_none():
    for g in _GOLD:
        if g["category"] == "Not a Support Ticket":
            assert g["assigned_team"] == "None", (
                f"{g['ticket_id']}: 'Not a Support Ticket' should route to 'None', got '{g['assigned_team']}'"
            )


def test_none_team_only_for_non_support_or_unroutable():
    """Team 'None' should only be used for non-support or completely unroutable tickets."""
    allowed_categories = {"Not a Support Ticket", "General Inquiry"}
    for g in _GOLD:
        if g["assigned_team"] == "None":
            assert g["category"] in allowed_categories, (
                f"{g['ticket_id']}: team 'None' with category '{g['category']}' — expected one of {allowed_categories}"
            )


def test_no_duplicate_missing_info_in_gold():
    """Gold answers should not have duplicate missing_information items."""
    for g in _GOLD:
        items = g["missing_information"]
        assert len(items) == len(set(items)), f"{g['ticket_id']}: duplicate missing_information items"


def test_remediation_steps_are_strings():
    """Every remediation step should be a non-empty string."""
    for g in _GOLD:
        for i, step in enumerate(g["remediation_steps"]):
            assert isinstance(step, str) and step.strip(), (
                f"{g['ticket_id']}: remediation step {i} is empty or not a string"
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
    print(f"\n{passed} passed, {failed} failed")
    sys.exit(1 if failed else 0)
