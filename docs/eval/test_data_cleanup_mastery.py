#!/usr/bin/env python3
"""Evaluation tests for mastery data cleanup scenarios.

Tests that the triage system correctly handles mastery-level messy/noisy input
including: extremely long email threads (10+ forwards), massive base64 image
dumps, HTML soup with CSS/scripts, multi-encoding garbled text, application log
explosions, mixed languages with RTL text, recursive unfilled templates,
ANSI/control character contamination, contradictory email threads, massive
corporate signatures, PII-laden descriptions, and emoji/Unicode art explosions.

These tests validate:
  1. Dataset integrity — ticket and gold data are well-formed.
  2. Gold answer correctness — all values within constrained vocabulary.
  3. Scoring pipeline — gold vs gold yields a perfect score.
  4. Per-ticket data-quality tests — each ticket exhibits its claimed noise type.
  5. Noise resilience — gold classification is correct despite noise.
  6. Scoring edge cases — wrong answers for noisy data are penalized.
  7. Structural invariants — team/category consistency.
  8. Output contamination detection — gold answers don't contain input noise.
  9. Cross-dataset consistency — no ID overlap with other datasets.

The tests cover the mastery data cleanup dataset:
  • data_cleanup_mastery_eval.json (12 tickets, INC-DCM-8###)

Usage:
    cd docs/eval
    python test_data_cleanup_mastery.py

    # Or with pytest:
    uv run pytest test_data_cleanup_mastery.py -v
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

# ── Paths ────────────────────────────────────────────────────────────

_DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "tickets"
_TICKETS_PATH = _DATA_DIR / "data_cleanup_mastery_eval.json"
_GOLD_PATH = _DATA_DIR / "data_cleanup_mastery_eval_gold.json"

# ── Constrained vocabularies ─────────────────────────────────────────

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


# ── Helpers ──────────────────────────────────────────────────────────


def _load_tickets() -> list[dict]:
    return json.loads(_TICKETS_PATH.read_text())


def _load_gold() -> list[dict]:
    return json.loads(_GOLD_PATH.read_text())


def _gold_by_id() -> dict[str, dict]:
    return {g["ticket_id"]: g for g in _load_gold()}


def _tickets_by_id() -> dict[str, dict]:
    return {t["ticket_id"]: t for t in _load_tickets()}


# ═══════════════════════════════════════════════════════════════════════
# SECTION 1: Dataset integrity (12 tickets, INC-DCM-8###)
# ═══════════════════════════════════════════════════════════════════════


def test_tickets_file_exists():
    assert _TICKETS_PATH.exists(), f"Missing: {_TICKETS_PATH}"


def test_gold_file_exists():
    assert _GOLD_PATH.exists(), f"Missing: {_GOLD_PATH}"


def test_ticket_count_is_12():
    assert len(_load_tickets()) == 12, f"Expected 12 mastery DC tickets, got {len(_load_tickets())}"


def test_gold_count_matches_ticket_count():
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


def test_all_ticket_ids_prefixed():
    for t in _load_tickets():
        assert t["ticket_id"].startswith("INC-DCM-"), f"Bad prefix: {t['ticket_id']}"


# ── Input schema validation ──────────────────────────────────────────


def test_all_tickets_have_required_fields():
    for ticket in _load_tickets():
        missing = _REQUIRED_INPUT_FIELDS - set(ticket.keys())
        assert not missing, f"{ticket['ticket_id']} missing fields: {missing}"


def test_all_reporters_have_required_fields():
    required = {"name", "email", "department"}
    for ticket in _load_tickets():
        missing = required - set(ticket["reporter"].keys())
        assert not missing, f"{ticket['ticket_id']} reporter missing: {missing}"


def test_all_channels_valid():
    for ticket in _load_tickets():
        assert ticket["channel"] in _VALID_CHANNELS, f"{ticket['ticket_id']} invalid channel: {ticket['channel']}"


def test_all_reporter_emails_contoso():
    for ticket in _load_tickets():
        assert ticket["reporter"]["email"].endswith("@contoso.com"), (
            f"{ticket['ticket_id']} reporter email not @contoso.com"
        )


# ── Gold answer validation ───────────────────────────────────────────


def test_gold_categories_valid():
    for g in _load_gold():
        assert g["category"] in _VALID_CATEGORIES, f"{g['ticket_id']}: invalid category '{g['category']}'"


def test_gold_priorities_valid():
    for g in _load_gold():
        assert g["priority"] in _VALID_PRIORITIES, f"{g['ticket_id']}: invalid priority '{g['priority']}'"


def test_gold_teams_valid():
    for g in _load_gold():
        assert g["assigned_team"] in _VALID_TEAMS, f"{g['ticket_id']}: invalid team '{g['assigned_team']}'"


def test_gold_missing_info_valid():
    for g in _load_gold():
        for item in g["missing_information"]:
            assert item in _VALID_MISSING_INFO, f"{g['ticket_id']}: invalid missing_information value '{item}'"


def test_gold_schema_fields():
    for g in _load_gold():
        missing = _REQUIRED_GOLD_FIELDS - set(g.keys())
        assert not missing, f"{g['ticket_id']}: missing gold fields {missing}"


def test_gold_escalation_is_boolean():
    for g in _load_gold():
        assert isinstance(g["needs_escalation"], bool), (
            f"{g['ticket_id']}: needs_escalation is {type(g['needs_escalation'])}"
        )


def test_gold_missing_info_is_list():
    for g in _load_gold():
        assert isinstance(g["missing_information"], list), (
            f"{g['ticket_id']}: missing_information is {type(g['missing_information'])}"
        )


def test_gold_remediation_steps_nonempty():
    for g in _load_gold():
        assert isinstance(g["remediation_steps"], list)
        assert len(g["remediation_steps"]) > 0, f"{g['ticket_id']}: remediation_steps should not be empty"


def test_gold_next_best_action_nonempty():
    for g in _load_gold():
        assert len(g["next_best_action"].strip()) > 0, f"{g['ticket_id']} has empty next_best_action"


def test_gold_no_duplicate_missing_info():
    for g in _load_gold():
        items = g["missing_information"]
        assert len(items) == len(set(items)), f"{g['ticket_id']}: duplicate missing_information items: {items}"


def test_gold_remediation_reasonable_length():
    for g in _load_gold():
        for i, step in enumerate(g["remediation_steps"]):
            assert len(step) >= 5, f"{g['ticket_id']}: remediation step {i} too short: '{step}'"
            assert len(step) <= 2000, f"{g['ticket_id']}: remediation step {i} too long ({len(step)} chars)"


# ═══════════════════════════════════════════════════════════════════════
# SECTION 2: Scoring tests (gold vs gold = perfect)
# ═══════════════════════════════════════════════════════════════════════


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
    assert result["tickets_scored"] == 12


def test_each_gold_ticket_scores_perfectly():
    for g in _load_gold():
        scores = score_ticket(dict(g), g)
        assert scores["weighted_total"] > 0.84, (
            f"{g['ticket_id']}: expected weighted_total > 0.84, got {scores['weighted_total']}"
        )


# ═══════════════════════════════════════════════════════════════════════
# SECTION 3: Per-ticket data-quality tests — noise type validation
# ═══════════════════════════════════════════════════════════════════════


def test_dcm8001_extremely_long_email_thread():
    """INC-DCM-8001: Extremely long email thread with 10+ forwards."""
    ticket = _tickets_by_id()["INC-DCM-8001"]
    gold = _gold_by_id()["INC-DCM-8001"]
    desc = ticket["description"]
    has_forwarding = (
        desc.count("RE:") + desc.count("FW:") + desc.count("Fwd:") + desc.count(">>>") >= 3
        or "Original Message" in desc
        or "forwarded" in desc.lower()
    )
    assert has_forwarding, "Ticket should contain extensive email forwarding artifacts"
    assert len(desc) >= 1000, f"Extremely long email should be 1000+ chars, got {len(desc)}"
    assert gold["category"] == "Network & Connectivity"
    assert gold["assigned_team"] == "Network Operations"


def test_dcm8002_massive_base64_dump():
    """INC-DCM-8002: Massive base64 image data dump."""
    ticket = _tickets_by_id()["INC-DCM-8002"]
    gold = _gold_by_id()["INC-DCM-8002"]
    desc = ticket["description"]
    has_base64 = "base64" in desc.lower() or "data:image" in desc or re.search(r"[A-Za-z0-9+/]{50,}", desc)
    assert has_base64, "Ticket should contain base64 encoded image data"
    assert gold["category"] == "Hardware & Peripherals"
    assert gold["assigned_team"] == "Endpoint Engineering"


def test_dcm8003_html_soup_css_scripts():
    """INC-DCM-8003: HTML soup with CSS and script tags."""
    ticket = _tickets_by_id()["INC-DCM-8003"]
    gold = _gold_by_id()["INC-DCM-8003"]
    desc = ticket["description"]
    has_html = (
        "<html" in desc.lower()
        or "<div" in desc.lower()
        or "<style" in desc.lower()
        or "<script" in desc.lower()
        or "<table" in desc.lower()
    )
    assert has_html, "Ticket should contain HTML tags, CSS, or script elements"
    assert gold["category"] == "Data & Storage"
    assert gold["assigned_team"] == "Data Platform"


def test_dcm8004_multi_encoding_garbled():
    """INC-DCM-8004: Multi-encoding garbled text (mojibake)."""
    ticket = _tickets_by_id()["INC-DCM-8004"]
    gold = _gold_by_id()["INC-DCM-8004"]
    desc = ticket["description"]
    has_garbled = (
        "Ã" in desc
        or "â€" in desc
        or "\\x" in desc
        or "\\u" in desc
        or "mojibake" in desc.lower()
        or "encoding" in desc.lower()
    )
    assert has_garbled, "Ticket should contain encoding artifacts or garbled text"
    assert gold["category"] == "Software & Applications"
    assert gold["assigned_team"] == "Enterprise Applications"


def test_dcm8005_log_file_explosion():
    """INC-DCM-8005: Application log output explosion."""
    ticket = _tickets_by_id()["INC-DCM-8005"]
    gold = _gold_by_id()["INC-DCM-8005"]
    desc = ticket["description"]
    log_lines = sum(
        1
        for line in desc.split("\n")
        if re.search(r"\d{4}-\d{2}-\d{2}[T ]?\d{2}:\d{2}", line) or re.search(r"\[(ERROR|WARN|INFO|DEBUG)", line)
    )
    assert log_lines >= 5, f"Expected many log lines, found {log_lines}"
    assert gold["category"] == "Data & Storage"
    assert gold["priority"] == "P1"
    assert gold["needs_escalation"] is True


def test_dcm8006_mixed_language_rtl():
    """INC-DCM-8006: Mixed language including RTL (Arabic) and CJK text."""
    ticket = _tickets_by_id()["INC-DCM-8006"]
    gold = _gold_by_id()["INC-DCM-8006"]
    desc = ticket["description"]
    has_mixed = (
        bool(re.search(r"[\u0600-\u06FF]", desc))
        or bool(re.search(r"[一-鿿぀-ゟ゠-ヿ가-힯]", desc))
        or "arabic" in desc.lower()
        or "japanese" in desc.lower()
    )
    assert has_mixed, "Ticket should contain RTL or CJK characters"
    assert gold["category"] == "Hardware & Peripherals"
    assert gold["assigned_team"] == "Endpoint Engineering"


def test_dcm8007_recursive_unfilled_template():
    """INC-DCM-8007: Support form template with unfilled fields."""
    ticket = _tickets_by_id()["INC-DCM-8007"]
    gold = _gold_by_id()["INC-DCM-8007"]
    desc = ticket["description"]
    has_template = (
        "{" in desc
        or "[FIELD" in desc
        or "PLACEHOLDER" in desc.upper()
        or "N/A" in desc
        or "________" in desc
        or "template" in desc.lower()
    )
    assert has_template, "Ticket should contain unfilled template fields"
    assert gold["category"] == "Access & Authentication"
    assert gold["assigned_team"] == "Identity & Access Management"


def test_dcm8008_control_chars_ansi():
    """INC-DCM-8008: ANSI escape codes and control characters."""
    ticket = _tickets_by_id()["INC-DCM-8008"]
    gold = _gold_by_id()["INC-DCM-8008"]
    desc = ticket["description"]
    has_control = (
        "\\033" in desc
        or "\\x1b" in desc
        or "\033" in desc
        or "\x1b" in desc
        or "[0m" in desc
        or "[31m" in desc
        or "\\t" in desc
        or "ANSI" in desc
        or "escape" in desc.lower()
    )
    assert has_control, "Ticket should contain ANSI escape codes or control characters"
    assert gold["category"] == "Network & Connectivity"
    assert gold["assigned_team"] == "Network Operations"


def test_dcm8009_contradictory_thread():
    """INC-DCM-8009: Email thread with contradictory information."""
    ticket = _tickets_by_id()["INC-DCM-8009"]
    gold = _gold_by_id()["INC-DCM-8009"]
    desc = ticket["description"]
    has_contradiction = (
        ("works" in desc.lower() and "broken" in desc.lower())
        or ("resolved" in desc.lower() and "still" in desc.lower())
        or ("fixed" in desc.lower() and "not" in desc.lower())
    )
    assert has_contradiction, "Ticket should contain contradictory statements"
    assert gold["category"] == "Software & Applications"
    assert gold["assigned_team"] == "Enterprise Applications"


def test_dcm8010_massive_signature():
    """INC-DCM-8010: Tiny issue buried under massive corporate signature."""
    ticket = _tickets_by_id()["INC-DCM-8010"]
    gold = _gold_by_id()["INC-DCM-8010"]
    desc = ticket["description"]
    assert len(desc) >= 500, f"Massive signature ticket should be 500+ chars, got {len(desc)}"
    has_disclaimer = (
        "confidential" in desc.lower()
        or "disclaimer" in desc.lower()
        or "intended recipient" in desc.lower()
        or "privileged" in desc.lower()
    )
    assert has_disclaimer, "Ticket should contain corporate disclaimer/signature text"
    assert gold["category"] == "Hardware & Peripherals"
    assert gold["assigned_team"] == "Endpoint Engineering"


def test_dcm8011_pii_laden():
    """INC-DCM-8011: Description contains PII patterns."""
    ticket = _tickets_by_id()["INC-DCM-8011"]
    gold = _gold_by_id()["INC-DCM-8011"]
    desc = ticket["description"]
    has_pii_patterns = (
        bool(re.search(r"XXX-XX-XXXX|\d{3}-\d{2}-\d{4}|SSN", desc))
        or bool(re.search(r"XXXX-XXXX-XXXX-XXXX|\d{4}-\d{4}-\d{4}-\d{4}", desc))
        or "social security" in desc.lower()
        or "credit card" in desc.lower()
    )
    assert has_pii_patterns, "Ticket should contain PII patterns (redacted or real)"
    assert gold["category"] == "Access & Authentication"
    assert gold["needs_escalation"] is True


def test_dcm8012_emoji_unicode_art():
    """INC-DCM-8012: Emoji and Unicode art explosion."""
    ticket = _tickets_by_id()["INC-DCM-8012"]
    gold = _gold_by_id()["INC-DCM-8012"]
    desc = ticket["description"]
    emoji_count = len(re.findall(r"[\U0001F600-\U0001F9FF\U00002702-\U000027B0\U0001F680-\U0001F6FF]", desc))
    has_unicode_art = (
        emoji_count >= 3 or "╔" in desc or "═" in desc or "║" in desc or "╗" in desc or "🚨" in desc or "🔥" in desc
    )
    assert has_unicode_art, "Ticket should contain emoji or Unicode box drawing characters"
    assert gold["category"] == "Data & Storage"
    assert gold["assigned_team"] == "Data Platform"


# ═══════════════════════════════════════════════════════════════════════
# SECTION 4: Scoring edge cases
# ═══════════════════════════════════════════════════════════════════════


def test_empty_responses_score_zero():
    """Empty response to any mastery data cleanup ticket should score 0.0 on core dimensions."""
    for gold in _load_gold():
        empty = {"ticket_id": gold["ticket_id"]}
        scores = score_ticket(empty, gold)
        assert scores["category"] == 0.0
        assert scores["priority"] == 0.0
        assert scores["routing"] == 0.0
        assert scores["escalation"] == 0.0


def test_submission_all_missing_scores_low():
    """Submitting zero responses should score very low."""
    gold = _load_gold()
    result = score_submission([], gold)
    assert result["tickets_errored"] == 12
    assert result["classification_score"] <= 15


def test_submission_with_partial_responses():
    """Missing half the responses should reduce the score significantly."""
    gold = _load_gold()
    partial = gold[:6]
    result = score_submission(partial, gold)
    assert result["tickets_errored"] == 6
    assert result["classification_score"] < 60


# ═══════════════════════════════════════════════════════════════════════
# SECTION 5: Output contamination detection
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

    if re.search(r"data:image/[a-z]+;base64,", combined):
        issues.append("base64 image data in gold answer")

    if re.search(r"<script[^>]*>", combined, re.IGNORECASE):
        issues.append("script tags in gold answer")

    if re.search(r"<style[^>]*>", combined, re.IGNORECASE):
        issues.append("CSS style tags in gold answer")

    if re.search(r"\\033\[", combined) or re.search(r"\x1b\[", combined):
        issues.append("ANSI escape codes in gold answer")

    if re.search(r"\bRE: RE: RE:", combined):
        issues.append("email forwarding chain in gold answer")

    if re.search(r"\{[A-Z_]+\}", combined):
        issues.append("unfilled template placeholder in gold answer")

    if re.search(r"[╔═╗║╚═╝╠╬╣]", combined):
        issues.append("Unicode box drawing characters in gold answer")

    return issues


def test_gold_no_contamination():
    """No gold answers should contain input noise artifacts."""
    for g in _load_gold():
        issues = _check_no_contamination(g)
        assert not issues, f"{g['ticket_id']}: {issues}"


# ═══════════════════════════════════════════════════════════════════════
# SECTION 6: Distribution and structural invariants
# ═══════════════════════════════════════════════════════════════════════


def test_diverse_categories_represented():
    gold = _load_gold()
    categories = {g["category"] for g in gold}
    assert len(categories) >= 3, f"Only {len(categories)} categories represented"


def test_diverse_teams_represented():
    gold = _load_gold()
    teams = {g["assigned_team"] for g in gold}
    assert len(teams) >= 3, f"Only {len(teams)} teams represented"


def test_diverse_priorities_represented():
    gold = _load_gold()
    priorities = {g["priority"] for g in gold}
    assert len(priorities) >= 2, f"Only {len(priorities)} priorities represented"


def test_escalation_has_both_values():
    gold = _load_gold()
    escalation_values = {g["needs_escalation"] for g in gold}
    assert True in escalation_values and False in escalation_values


def test_multiple_channels_represented():
    tickets = _load_tickets()
    channels = {t["channel"] for t in tickets}
    assert len(channels) >= 3, f"Only {len(channels)} channels: {channels}"


def test_not_a_support_ticket_routed_to_none():
    for g in _load_gold():
        if g["category"] == "Not a Support Ticket":
            assert g["assigned_team"] == "None", f"{g['ticket_id']}: 'Not a Support Ticket' should route to 'None'"


def test_none_team_only_for_non_support():
    allowed_categories = {"Not a Support Ticket", "General Inquiry"}
    for g in _load_gold():
        if g["assigned_team"] == "None":
            assert g["category"] in allowed_categories, f"{g['ticket_id']}: team 'None' with category '{g['category']}'"


# ═══════════════════════════════════════════════════════════════════════
# SECTION 7: Data-quality property tests (across dataset)
# ═══════════════════════════════════════════════════════════════════════


def test_at_least_one_ticket_has_base64():
    """At least one ticket should contain base64 data."""
    tickets = _load_tickets()
    found = any("base64" in t["description"].lower() or "data:image" in t["description"] for t in tickets)
    assert found, "No ticket contains base64 content"


def test_at_least_one_ticket_has_html():
    """At least one ticket should contain HTML markup."""
    tickets = _load_tickets()
    found = any("<div" in t["description"].lower() or "<html" in t["description"].lower() for t in tickets)
    assert found, "No ticket contains HTML content"


def test_at_least_one_ticket_has_forwarded_chain():
    """At least one ticket should contain email forwarding chain."""
    tickets = _load_tickets()
    found = any(
        t["description"].count("RE:") + t["description"].count("FW:") >= 3 or "Original Message" in t["description"]
        for t in tickets
    )
    assert found, "No ticket contains email forwarding chain"


def test_at_least_one_ticket_has_emoji():
    """At least one ticket should contain emoji or Unicode art."""
    tickets = _load_tickets()
    found = any(
        bool(re.search(r"[\U0001F600-\U0001F9FF]", t["description"]))
        or "╔" in t["description"]
        or "🚨" in t["description"]
        for t in tickets
    )
    assert found, "No ticket contains emoji or Unicode art"


def test_at_least_one_ticket_has_pii_pattern():
    """At least one ticket should contain PII-like patterns."""
    tickets = _load_tickets()
    found = any(
        bool(re.search(r"XXX-XX-XXXX|\d{3}-\d{2}-\d{4}|SSN", t["description"]))
        or bool(re.search(r"XXXX-XXXX-XXXX-XXXX", t["description"]))
        for t in tickets
    )
    assert found, "No ticket contains PII patterns"


def test_average_description_length_above_400():
    """Mastery cleanup tickets should be substantive and messy."""
    tickets = _load_tickets()
    avg = sum(len(t["description"]) for t in tickets) / len(tickets)
    assert avg > 400, f"Average description length is only {avg:.0f} chars"


# ═══════════════════════════════════════════════════════════════════════
# SECTION 8: Cross-dataset no ID collisions
# ═══════════════════════════════════════════════════════════════════════


def _load_ids_from(filename: str) -> set[str]:
    path = _DATA_DIR / filename
    if not path.exists():
        return set()
    try:
        data = json.loads(path.read_text())
    except json.JSONDecodeError:
        return set()
    return {t["ticket_id"] for t in data}


def test_no_id_collision_with_handcrafted_dc():
    """No overlap with handcrafted data cleanup dataset."""
    other_ids = _load_ids_from("data_cleanup_eval.json")
    our_ids = {t["ticket_id"] for t in _load_tickets()}
    overlap = other_ids & our_ids
    assert not overlap, f"ID collision with data_cleanup_eval: {overlap}"


def test_no_id_collision_with_advanced_dc():
    """No overlap with advanced data cleanup dataset."""
    other_ids = _load_ids_from("data_cleanup_advanced_eval.json")
    our_ids = {t["ticket_id"] for t in _load_tickets()}
    overlap = other_ids & our_ids
    assert not overlap, f"ID collision with data_cleanup_advanced_eval: {overlap}"


def test_no_id_collision_with_expert_dc():
    """No overlap with expert data cleanup dataset."""
    other_ids = _load_ids_from("data_cleanup_expert_eval.json")
    our_ids = {t["ticket_id"] for t in _load_tickets()}
    overlap = other_ids & our_ids
    assert not overlap, f"ID collision with data_cleanup_expert_eval: {overlap}"


def test_no_id_collision_with_comprehensive_dc():
    """No overlap with comprehensive data cleanup dataset."""
    other_ids = _load_ids_from("data_cleanup_comprehensive_eval.json")
    our_ids = {t["ticket_id"] for t in _load_tickets()}
    overlap = other_ids & our_ids
    assert not overlap, f"ID collision with data_cleanup_comprehensive_eval: {overlap}"


def test_no_id_collision_with_scoring_dc():
    """No overlap with INC-5### scoring data cleanup dataset."""
    other_ids = _load_ids_from("data_cleanup.json")
    our_ids = {t["ticket_id"] for t in _load_tickets()}
    overlap = other_ids & our_ids
    assert not overlap, f"ID collision with data_cleanup: {overlap}"


def test_no_id_collision_with_rai_datasets():
    """No overlap with responsible AI datasets."""
    for filename in (
        "responsible_ai_eval.json",
        "responsible_ai.json",
        "responsible_ai_advanced_eval.json",
        "responsible_ai_expert_eval.json",
        "responsible_ai_comprehensive_eval.json",
        "responsible_ai_mastery_eval.json",
    ):
        other_ids = _load_ids_from(filename)
        our_ids = {t["ticket_id"] for t in _load_tickets()}
        overlap = other_ids & our_ids
        assert not overlap, f"ID collision with {filename}: {overlap}"


def test_no_id_collision_with_sample():
    """No overlap with sample dataset."""
    other_ids = _load_ids_from("sample.json")
    our_ids = {t["ticket_id"] for t in _load_tickets()}
    overlap = other_ids & our_ids
    assert not overlap, f"ID collision with sample: {overlap}"


# ═══════════════════════════════════════════════════════════════════════
# SECTION 9: PII leakage detection
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

    if re.search(r"\b\d{3}-\d{2}-\d{4}\b", combined):
        issues.append("SSN pattern in gold answer")

    if re.search(r"\b(?:\d{4}[-\s]?){3}\d{4}\b", combined):
        issues.append("credit card pattern in gold answer")

    if re.search(r"\b[A-Za-z0-9._%+-]+@(?!contoso\.com)[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b", combined):
        issues.append("non-contoso email in gold answer")

    return issues


def test_gold_no_pii_leakage():
    """No gold answers should contain PII patterns."""
    for g in _load_gold():
        issues = _check_pii_leakage(g)
        assert not issues, f"{g['ticket_id']}: {issues}"


# ═══════════════════════════════════════════════════════════════════════
# Runner
# ═══════════════════════════════════════════════════════════════════════

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
