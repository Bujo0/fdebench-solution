#!/usr/bin/env python3
"""Evaluation tests for advanced data cleanup scenarios.

Tests that the triage system correctly handles advanced messy/noisy input
beyond the base data cleanup scenarios — including CSV data embedded in tickets,
XML/SOAP fault messages, ANSI terminal escape codes, auto-reply chains,
concatenated multi-issue tickets, NDR bounce-backs, massive email signatures,
URL-encoded content, JSON config dumps, RTF formatting artifacts, OCR errors,
inconsistent date formats, ASCII art tables, raw markdown, and MIME multipart
boundaries.

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

The tests cover the advanced data cleanup dataset:
  • data_cleanup_advanced_eval.json (15 tickets, INC-DCA###)

Usage:
    cd docs/eval
    python test_data_cleanup_advanced.py

    # Or with pytest:
    uv run pytest test_data_cleanup_advanced.py -v
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
_TICKETS_PATH = _DATA_DIR / "data_cleanup_advanced_eval.json"
_GOLD_PATH = _DATA_DIR / "data_cleanup_advanced_eval_gold.json"

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
    "ticket_id", "category", "priority", "assigned_team",
    "needs_escalation", "missing_information", "next_best_action", "remediation_steps",
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
# SECTION 1: Dataset integrity (15 tickets, INC-DCA###)
# ═══════════════════════════════════════════════════════════════════════


def test_tickets_file_exists():
    assert _TICKETS_PATH.exists(), f"Missing: {_TICKETS_PATH}"


def test_gold_file_exists():
    assert _GOLD_PATH.exists(), f"Missing: {_GOLD_PATH}"


def test_ticket_count_is_15():
    assert len(_load_tickets()) == 15, f"Expected 15 advanced DC tickets, got {len(_load_tickets())}"


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
        assert t["ticket_id"].startswith("INC-DCA"), f"Bad prefix: {t['ticket_id']}"


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
        assert ticket["channel"] in _VALID_CHANNELS, (
            f"{ticket['ticket_id']} invalid channel: {ticket['channel']}"
        )


# ── Gold answer validation ───────────────────────────────────────────


def test_gold_categories_valid():
    for g in _load_gold():
        assert g["category"] in _VALID_CATEGORIES, (
            f"{g['ticket_id']}: invalid category '{g['category']}'"
        )


def test_gold_priorities_valid():
    for g in _load_gold():
        assert g["priority"] in _VALID_PRIORITIES, (
            f"{g['ticket_id']}: invalid priority '{g['priority']}'"
        )


def test_gold_teams_valid():
    for g in _load_gold():
        assert g["assigned_team"] in _VALID_TEAMS, (
            f"{g['ticket_id']}: invalid team '{g['assigned_team']}'"
        )


def test_gold_missing_info_valid():
    for g in _load_gold():
        for item in g["missing_information"]:
            assert item in _VALID_MISSING_INFO, (
                f"{g['ticket_id']}: invalid missing_information value '{item}'"
            )


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
        assert len(g["remediation_steps"]) > 0, (
            f"{g['ticket_id']}: remediation_steps should not be empty"
        )


def test_gold_next_best_action_nonempty():
    for g in _load_gold():
        assert len(g["next_best_action"].strip()) > 0, (
            f"{g['ticket_id']} has empty next_best_action"
        )


def test_gold_no_duplicate_missing_info():
    for g in _load_gold():
        items = g["missing_information"]
        assert len(items) == len(set(items)), (
            f"{g['ticket_id']}: duplicate missing_information items: {items}"
        )


def test_gold_remediation_reasonable_length():
    for g in _load_gold():
        for i, step in enumerate(g["remediation_steps"]):
            assert len(step) >= 5, (
                f"{g['ticket_id']}: remediation step {i} too short: '{step}'"
            )
            assert len(step) <= 2000, (
                f"{g['ticket_id']}: remediation step {i} too long ({len(step)} chars)"
            )


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
    assert result["tickets_scored"] == 15


def test_each_gold_ticket_scores_perfectly():
    for g in _load_gold():
        scores = score_ticket(dict(g), g)
        assert scores["weighted_total"] > 0.84, (
            f"{g['ticket_id']}: expected weighted_total > 0.84, got {scores['weighted_total']}"
        )


# ═══════════════════════════════════════════════════════════════════════
# SECTION 3: Per-ticket data-quality tests — noise type validation
# ═══════════════════════════════════════════════════════════════════════


def test_dca001_csv_data_embedded():
    """INC-DCA001: CSV/spreadsheet data in ticket body."""
    ticket = _tickets_by_id()["INC-DCA001"]
    gold = _gold_by_id()["INC-DCA001"]
    # Should contain comma-separated data with headers
    assert "," in ticket["description"] and (
        "ServerName" in ticket["description"]
        or "server" in ticket["description"].lower()
        or "CPU" in ticket["description"]
    )
    assert gold["category"] == "Data & Storage"
    assert gold["assigned_team"] == "Data Platform"


def test_dca002_xml_soap_fault():
    """INC-DCA002: XML/SOAP fault message in ticket body."""
    ticket = _tickets_by_id()["INC-DCA002"]
    gold = _gold_by_id()["INC-DCA002"]
    desc = ticket["description"]
    assert "<" in desc and ">" in desc  # Has XML-like tags
    assert "soap" in desc.lower() or "xml" in desc.lower() or "fault" in desc.lower()
    assert gold["category"] == "Software & Applications"
    assert gold["assigned_team"] == "Enterprise Applications"


def test_dca003_ansi_escape_codes():
    """INC-DCA003: ANSI terminal escape codes in pasted output."""
    ticket = _tickets_by_id()["INC-DCA003"]
    gold = _gold_by_id()["INC-DCA003"]
    desc = ticket["description"]
    # Should contain ANSI escape sequences or references to colored output
    has_ansi = (
        "\x1b[" in desc
        or "\\x1b[" in desc
        or "\\033[" in desc
        or "\033[" in desc
        or "[ERROR]" in desc
        or "[INFO]" in desc
    )
    assert has_ansi, "Ticket should contain ANSI escape codes or terminal output markers"
    assert gold["category"] == "Software & Applications"
    assert gold["assigned_team"] == "Enterprise Applications"


def test_dca004_auto_reply_chain():
    """INC-DCA004: Auto-reply/out-of-office mixed with real issue."""
    ticket = _tickets_by_id()["INC-DCA004"]
    gold = _gold_by_id()["INC-DCA004"]
    desc_lower = ticket["description"].lower()
    assert "out of" in desc_lower or "auto" in desc_lower or "automatic" in desc_lower
    assert gold["category"] == "Network & Connectivity"
    assert gold["assigned_team"] == "Network Operations"


def test_dca005_concatenated_tickets():
    """INC-DCA005: Multiple issues concatenated into one ticket."""
    ticket = _tickets_by_id()["INC-DCA005"]
    gold = _gold_by_id()["INC-DCA005"]
    desc_lower = ticket["description"].lower()
    # Should mention multiple distinct issues
    issue_keywords = ["printer", "outlook", "wifi", "email", "monitor", "vpn", "software"]
    distinct_issues = sum(1 for kw in issue_keywords if kw in desc_lower)
    assert distinct_issues >= 2, "Concatenated ticket should mention at least 2 distinct issues"
    assert gold["category"] == "General Inquiry"


def test_dca006_ndr_bounceback():
    """INC-DCA006: NDR/email bounce-back pasted as ticket."""
    ticket = _tickets_by_id()["INC-DCA006"]
    gold = _gold_by_id()["INC-DCA006"]
    desc = ticket["description"]
    assert (
        "delivery" in desc.lower()
        or "non-delivery" in desc.lower()
        or "bounce" in desc.lower()
        or "550" in desc
        or "smtp" in desc.lower()
    )
    assert gold["category"] == "Software & Applications"
    assert gold["assigned_team"] == "Enterprise Applications"


def test_dca007_massive_signature():
    """INC-DCA007: Massive email signature burying the actual issue."""
    ticket = _tickets_by_id()["INC-DCA007"]
    gold = _gold_by_id()["INC-DCA007"]
    # The signature should be much longer than the actual issue
    desc = ticket["description"]
    assert len(desc) > 500, "Massive signature ticket should be long"
    # Should contain typical signature elements
    has_signature = (
        "regards" in desc.lower()
        or "confidentiality" in desc.lower()
        or "disclaimer" in desc.lower()
        or "phone:" in desc.lower()
        or "mobile:" in desc.lower()
    )
    assert has_signature, "Ticket should contain email signature elements"
    assert gold["category"] == "Access & Authentication"
    assert gold["assigned_team"] == "Identity & Access Management"


def test_dca008_url_encoded_content():
    """INC-DCA008: URL-encoded content in description."""
    ticket = _tickets_by_id()["INC-DCA008"]
    gold = _gold_by_id()["INC-DCA008"]
    desc = ticket["description"]
    # Should contain URL encoding patterns
    assert "%2" in desc or "%3" in desc or "%20" in desc
    assert gold["category"] == "Software & Applications"
    assert gold["assigned_team"] == "Enterprise Applications"


def test_dca009_json_config_dump():
    """INC-DCA009: JSON config dump with many lines."""
    ticket = _tickets_by_id()["INC-DCA009"]
    gold = _gold_by_id()["INC-DCA009"]
    desc = ticket["description"]
    # Should contain JSON structure
    assert "{" in desc and "}" in desc
    assert '"' in desc  # JSON uses double quotes
    assert gold["category"] == "Network & Connectivity"
    assert gold["assigned_team"] == "Network Operations"


def test_dca010_rtf_artifacts():
    """INC-DCA010: RTF/Word formatting artifacts in ticket body."""
    ticket = _tickets_by_id()["INC-DCA010"]
    gold = _gold_by_id()["INC-DCA010"]
    desc = ticket["description"]
    has_rtf = (
        "\\rtf" in desc
        or "\\par" in desc
        or "\\fonttbl" in desc
        or "\\b " in desc
        or "rtf" in desc.lower()
    )
    assert has_rtf, "Ticket should contain RTF formatting artifacts"
    assert gold["category"] == "Hardware & Peripherals"
    assert gold["assigned_team"] == "Endpoint Engineering"


def test_dca011_ocr_artifacts():
    """INC-DCA011: OCR recognition artifacts in description."""
    ticket = _tickets_by_id()["INC-DCA011"]
    gold = _gold_by_id()["INC-DCA011"]
    desc = ticket["description"]
    # OCR errors typically swap 0/O and 1/l
    ocr_indicators = ["0" in desc.replace("0x", ""), "1" in desc]
    assert any(ocr_indicators), "Ticket should contain OCR-like character swaps"
    assert gold["category"] == "Software & Applications"
    assert gold["assigned_team"] == "Enterprise Applications"


def test_dca012_inconsistent_dates():
    """INC-DCA012: Inconsistent date/time formats throughout."""
    ticket = _tickets_by_id()["INC-DCA012"]
    gold = _gold_by_id()["INC-DCA012"]
    desc = ticket["description"]
    # Should have multiple date format patterns
    date_patterns = [
        re.compile(r"\d{2}/\d{2}/\d{4}"),  # MM/DD/YYYY
        re.compile(r"\d{4}[-/.]\d{2}[-/.]\d{2}"),  # YYYY-MM-DD
        re.compile(r"\d{2}-\w{3}-\d{2,4}"),  # DD-Mon-YY
    ]
    formats_found = sum(1 for p in date_patterns if p.search(desc))
    assert formats_found >= 2, f"Expected ≥2 date formats, found {formats_found}"
    assert gold["category"] == "Software & Applications"
    assert gold["assigned_team"] == "Enterprise Applications"


def test_dca013_ascii_art_table():
    """INC-DCA013: ASCII art table formatting in ticket."""
    ticket = _tickets_by_id()["INC-DCA013"]
    gold = _gold_by_id()["INC-DCA013"]
    desc = ticket["description"]
    # Should contain ASCII table characters
    has_table = "+" in desc and "|" in desc and "-" in desc
    assert has_table, "Ticket should contain ASCII art table characters"
    assert gold["category"] == "Network & Connectivity"
    assert gold["priority"] == "P1"
    assert gold["needs_escalation"] is True


def test_dca014_raw_markdown():
    """INC-DCA014: Raw markdown rendering artifacts."""
    ticket = _tickets_by_id()["INC-DCA014"]
    gold = _gold_by_id()["INC-DCA014"]
    desc = ticket["description"]
    # Should contain markdown syntax
    md_indicators = [
        "##" in desc or "**" in desc,
        "```" in desc,
        "](http" in desc or "- " in desc,
    ]
    assert sum(md_indicators) >= 2, "Ticket should contain multiple markdown indicators"
    assert gold["category"] == "Software & Applications"
    assert gold["assigned_team"] == "Enterprise Applications"


def test_dca015_mime_boundaries():
    """INC-DCA015: MIME multipart boundaries visible in email."""
    ticket = _tickets_by_id()["INC-DCA015"]
    gold = _gold_by_id()["INC-DCA015"]
    desc = ticket["description"]
    has_mime = (
        "mime" in desc.lower()
        or "boundary" in desc.lower()
        or "content-type" in desc.lower()
        or "Content-Transfer-Encoding" in desc
    )
    assert has_mime, "Ticket should contain MIME boundary content"
    assert gold["category"] == "Software & Applications"
    assert gold["assigned_team"] == "Enterprise Applications"


# ═══════════════════════════════════════════════════════════════════════
# SECTION 4: Scoring edge cases
# ═══════════════════════════════════════════════════════════════════════


def test_empty_responses_score_zero():
    """Empty response to any data cleanup ticket should score 0.0 on core dimensions."""
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
    assert result["tickets_errored"] == 15
    assert result["classification_score"] <= 15


def test_submission_with_partial_responses():
    """Missing half the responses should reduce the score significantly."""
    gold = _load_gold()
    partial = gold[:8]
    result = score_submission(partial, gold)
    assert result["tickets_errored"] == 7
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

    # Base64 data shouldn't leak into gold answers
    if re.search(r"data:image/[a-z]+;base64,", combined):
        issues.append("base64 image data in gold answer")

    # Raw HTML/XML tags shouldn't be in gold answers
    if re.search(r"<script[^>]*>", combined, re.IGNORECASE):
        issues.append("script tags in gold answer")

    # ANSI escape codes shouldn't leak
    if "\x1b[" in combined or "\\x1b[" in combined:
        issues.append("ANSI escape codes in gold answer")

    # RTF formatting shouldn't leak
    if re.search(r"\\rtf\d|\\par\b|\\fonttbl", combined):
        issues.append("RTF formatting in gold answer")

    # MIME boundaries shouldn't leak
    if re.search(r"boundary=", combined, re.IGNORECASE):
        issues.append("MIME boundary in gold answer")

    # CSV data rows shouldn't leak
    if re.search(r"^\w+,\w+,\w+,\w+", combined, re.MULTILINE):
        issues.append("CSV data rows in gold answer")

    # URL-encoded strings shouldn't leak
    if re.search(r"%[0-9A-Fa-f]{2}%[0-9A-Fa-f]{2}%[0-9A-Fa-f]{2}", combined):
        issues.append("URL-encoded strings in gold answer")

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
    assert len(categories) >= 4, f"Only {len(categories)} categories represented"


def test_diverse_teams_represented():
    gold = _load_gold()
    teams = {g["assigned_team"] for g in gold}
    assert len(teams) >= 3, f"Only {len(teams)} teams represented"


def test_diverse_priorities_represented():
    gold = _load_gold()
    priorities = {g["priority"] for g in gold}
    assert len(priorities) >= 3, f"Only {len(priorities)} priorities represented"


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
            assert g["assigned_team"] == "None", (
                f"{g['ticket_id']}: 'Not a Support Ticket' should route to 'None'"
            )


def test_none_team_only_for_non_support():
    allowed_categories = {"Not a Support Ticket", "General Inquiry"}
    for g in _load_gold():
        if g["assigned_team"] == "None":
            assert g["category"] in allowed_categories, (
                f"{g['ticket_id']}: team 'None' with category '{g['category']}'"
            )


# ═══════════════════════════════════════════════════════════════════════
# SECTION 7: Data-quality property tests (across dataset)
# ═══════════════════════════════════════════════════════════════════════


def test_at_least_one_ticket_has_csv_data():
    """At least one ticket should contain CSV/tabular data."""
    tickets = _load_tickets()
    found = any(
        t["description"].count(",") > 20 and "\n" in t["description"]
        for t in tickets
    )
    assert found, "No ticket contains CSV data"


def test_at_least_one_ticket_has_xml():
    """At least one ticket should contain XML/SOAP content."""
    tickets = _load_tickets()
    found = any(
        "</" in t["description"] or "<?xml" in t["description"]
        for t in tickets
    )
    assert found, "No ticket contains XML content"


def test_at_least_one_ticket_has_json():
    """At least one ticket should contain a JSON config dump."""
    tickets = _load_tickets()
    found = any(
        '{"' in t["description"] or '": ' in t["description"]
        for t in tickets
    )
    assert found, "No ticket contains JSON content"


def test_at_least_one_ticket_has_url_encoding():
    """At least one ticket should contain URL-encoded content."""
    tickets = _load_tickets()
    found = any("%2" in t["description"] or "%3" in t["description"] for t in tickets)
    assert found, "No ticket contains URL-encoded content"


def test_at_least_one_ticket_has_ascii_table():
    """At least one ticket should contain ASCII art table formatting."""
    tickets = _load_tickets()
    found = any(
        "+--" in t["description"] and "|" in t["description"]
        for t in tickets
    )
    assert found, "No ticket contains ASCII art tables"


def test_at_least_one_ticket_has_markdown():
    """At least one ticket should contain raw markdown."""
    tickets = _load_tickets()
    found = any(
        "##" in t["description"] or "```" in t["description"]
        for t in tickets
    )
    assert found, "No ticket contains raw markdown"


def test_at_least_one_ticket_has_mime_content():
    """At least one ticket should contain MIME multipart content."""
    tickets = _load_tickets()
    found = any(
        "boundary" in t["description"].lower() or "content-type" in t["description"].lower()
        for t in tickets
    )
    assert found, "No ticket contains MIME content"


def test_average_description_length_above_300():
    """Advanced cleanup tickets should be substantive."""
    tickets = _load_tickets()
    avg = sum(len(t["description"]) for t in tickets) / len(tickets)
    assert avg > 300, f"Average description length is only {avg:.0f} chars"


# ═══════════════════════════════════════════════════════════════════════
# SECTION 8: Cross-dataset no ID collisions
# ═══════════════════════════════════════════════════════════════════════


def test_no_id_collision_with_handcrafted_dc():
    """No overlap with INC-DC### handcrafted data cleanup dataset."""
    dc_path = _DATA_DIR / "data_cleanup_eval.json"
    if not dc_path.exists():
        return
    dc_tickets = json.loads(dc_path.read_text())
    dc_ids = {t["ticket_id"] for t in dc_tickets}
    dca_ids = {t["ticket_id"] for t in _load_tickets()}
    overlap = dc_ids & dca_ids
    assert not overlap, f"ID collision with INC-DC### dataset: {overlap}"


def test_no_id_collision_with_scoring_dc():
    """No overlap with INC-5### scoring data cleanup dataset."""
    sc_path = _DATA_DIR / "data_cleanup.json"
    if not sc_path.exists():
        return
    sc_tickets = json.loads(sc_path.read_text())
    sc_ids = {t["ticket_id"] for t in sc_tickets}
    dca_ids = {t["ticket_id"] for t in _load_tickets()}
    overlap = sc_ids & dca_ids
    assert not overlap, f"ID collision with INC-5### dataset: {overlap}"


def test_no_id_collision_with_rai_datasets():
    """No overlap with responsible AI datasets."""
    for filename in ("responsible_ai_eval.json", "responsible_ai.json",
                     "responsible_ai_advanced_eval.json"):
        path = _DATA_DIR / filename
        if not path.exists():
            continue
        other_tickets = json.loads(path.read_text())
        other_ids = {t["ticket_id"] for t in other_tickets}
        dca_ids = {t["ticket_id"] for t in _load_tickets()}
        overlap = other_ids & dca_ids
        assert not overlap, f"ID collision with {filename}: {overlap}"


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
