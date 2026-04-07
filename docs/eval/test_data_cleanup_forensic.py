#!/usr/bin/env python3
"""Evaluation tests for forensic data cleanup scenarios.

Tests that the triage system correctly handles forensic-level messy/noisy input
beyond all previous tiers — including SQL injection strings embedded in ticket
bodies, mixed encoding mojibake, corrupted binary pastes, spreadsheet formulas,
JWT token dumps, Docker container logs, Azure DevOps pipeline YAML failures,
Windows Event Log XML, browser console JavaScript errors, email threads with
conflicting timezones, clipboard paste bombs, API rate limit JSON responses,
corrupted CSV with mismatched columns, file paths with special characters, and
Log4j-style logging patterns from security scans.

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

The tests cover the forensic data cleanup dataset:
  • data_cleanup_forensic_eval.json (15 tickets, INC-DCF###)

Usage:
    cd docs/eval
    python test_data_cleanup_forensic.py

    # Or with pytest:
    uv run pytest test_data_cleanup_forensic.py -v
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
_TICKETS_PATH = _DATA_DIR / "data_cleanup_forensic_eval.json"
_GOLD_PATH = _DATA_DIR / "data_cleanup_forensic_eval_gold.json"

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
# SECTION 1: Dataset integrity (15 tickets, INC-DCF###)
# ═══════════════════════════════════════════════════════════════════════


def test_tickets_file_exists():
    assert _TICKETS_PATH.exists(), f"Missing: {_TICKETS_PATH}"


def test_gold_file_exists():
    assert _GOLD_PATH.exists(), f"Missing: {_GOLD_PATH}"


def test_ticket_count_is_15():
    assert len(_load_tickets()) == 15, f"Expected 15 forensic DC tickets, got {len(_load_tickets())}"


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
        assert t["ticket_id"].startswith("INC-DCF"), f"Bad prefix: {t['ticket_id']}"


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


def test_dcf001_sql_injection_strings():
    """INC-DCF001: SQL injection-like strings in ticket body."""
    ticket = _tickets_by_id()["INC-DCF001"]
    gold = _gold_by_id()["INC-DCF001"]
    desc = ticket["description"]
    has_sql = (
        "SELECT" in desc
        or "INSERT" in desc
        or "DROP" in desc
        or "DELETE" in desc
        or "FROM" in desc
        or "sql" in desc.lower()
        or "query" in desc.lower()
    )
    assert has_sql, "Ticket should contain SQL query strings"
    assert gold["category"] == "Data & Storage"
    assert gold["assigned_team"] == "Data Platform"


def test_dcf002_mixed_encoding_mojibake():
    """INC-DCF002: Mixed encoding / mojibake characters."""
    ticket = _tickets_by_id()["INC-DCF002"]
    gold = _gold_by_id()["INC-DCF002"]
    desc = ticket["description"]
    has_mojibake = (
        "Ã" in desc
        or "â€" in desc
        or "Ã©" in desc
        or "Ã¼" in desc
        or "garbled" in desc.lower()
        or "encoding" in desc.lower()
        or "mojibake" in desc.lower()
    )
    assert has_mojibake, "Ticket should contain mojibake / encoding artifacts"
    assert gold["category"] == "Software & Applications"
    assert gold["assigned_team"] == "Enterprise Applications"


def test_dcf003_corrupted_binary_paste():
    """INC-DCF003: Corrupted binary / clipboard data."""
    ticket = _tickets_by_id()["INC-DCF003"]
    gold = _gold_by_id()["INC-DCF003"]
    desc = ticket["description"]
    has_binary = (
        "\\x00" in desc
        or "\\ufffd" in desc
        or "\ufffd" in desc
        or "corrupt" in desc.lower()
        or "garble" in desc.lower()
        or "binary" in desc.lower()
        or bool(re.search(r"[^\x20-\x7e\n\r\t]", desc))
    )
    assert has_binary, "Ticket should contain corrupted/binary data artifacts"
    assert gold["category"] == "Data & Storage"
    assert gold["assigned_team"] == "Data Platform"


def test_dcf004_spreadsheet_formulas():
    """INC-DCF004: Excel/spreadsheet formula strings."""
    ticket = _tickets_by_id()["INC-DCF004"]
    gold = _gold_by_id()["INC-DCF004"]
    desc = ticket["description"]
    has_formulas = (
        "=VLOOKUP" in desc
        or "=IF(" in desc
        or "=SUM" in desc
        or "=INDEX" in desc
        or "#REF" in desc
        or "#VALUE" in desc
        or "#NAME" in desc
        or "formula" in desc.lower()
    )
    assert has_formulas, "Ticket should contain spreadsheet formulas"
    assert gold["category"] == "Software & Applications"
    assert gold["assigned_team"] == "Enterprise Applications"


def test_dcf005_jwt_token_dump():
    """INC-DCF005: JWT token strings in ticket body."""
    ticket = _tickets_by_id()["INC-DCF005"]
    gold = _gold_by_id()["INC-DCF005"]
    desc = ticket["description"]
    has_jwt = (
        "eyJ" in desc
        or "jwt" in desc.lower()
        or "token" in desc.lower()
        or "bearer" in desc.lower()
    )
    assert has_jwt, "Ticket should contain JWT token content"
    assert gold["category"] == "Access & Authentication"
    assert gold["assigned_team"] == "Identity & Access Management"
    assert gold["needs_escalation"] is True


def test_dcf006_docker_container_logs():
    """INC-DCF006: Docker/container log output."""
    ticket = _tickets_by_id()["INC-DCF006"]
    gold = _gold_by_id()["INC-DCF006"]
    desc = ticket["description"]
    has_docker = (
        "docker" in desc.lower()
        or "container" in desc.lower()
        or "compose" in desc.lower()
        or "health" in desc.lower()
        or "port" in desc.lower()
        or "restart" in desc.lower()
    )
    assert has_docker, "Ticket should contain Docker/container log content"
    assert gold["category"] == "Software & Applications"
    assert gold["assigned_team"] == "Enterprise Applications"


def test_dcf007_azure_devops_pipeline():
    """INC-DCF007: Azure DevOps pipeline YAML failure output."""
    ticket = _tickets_by_id()["INC-DCF007"]
    gold = _gold_by_id()["INC-DCF007"]
    desc = ticket["description"]
    has_pipeline = (
        "pipeline" in desc.lower()
        or "yaml" in desc.lower()
        or "azure devops" in desc.lower()
        or "build" in desc.lower()
        or "task" in desc.lower()
        or "stage" in desc.lower()
    )
    assert has_pipeline, "Ticket should contain Azure DevOps pipeline output"
    assert gold["category"] == "Software & Applications"
    assert gold["assigned_team"] == "Enterprise Applications"


def test_dcf008_windows_event_log_xml():
    """INC-DCF008: Windows Event Log XML export."""
    ticket = _tickets_by_id()["INC-DCF008"]
    gold = _gold_by_id()["INC-DCF008"]
    desc = ticket["description"]
    has_event_log = (
        "<Event" in desc
        or "EventID" in desc
        or "Event Viewer" in desc
        or "event log" in desc.lower()
        or "Source:" in desc
        or "Level:" in desc
    )
    assert has_event_log, "Ticket should contain Windows Event Log content"
    assert gold["category"] == "Software & Applications"
    assert gold["assigned_team"] == "Endpoint Engineering"


def test_dcf009_browser_console_errors():
    """INC-DCF009: Browser console JavaScript errors."""
    ticket = _tickets_by_id()["INC-DCF009"]
    gold = _gold_by_id()["INC-DCF009"]
    desc = ticket["description"]
    has_console = (
        "console" in desc.lower()
        or "TypeError" in desc
        or "ReferenceError" in desc
        or "Uncaught" in desc
        or "undefined" in desc
        or "null" in desc
        or "fetch" in desc.lower()
        or "javascript" in desc.lower()
    )
    assert has_console, "Ticket should contain browser console error output"
    assert gold["category"] == "Software & Applications"
    assert gold["assigned_team"] == "Enterprise Applications"


def test_dcf010_timezone_confusion():
    """INC-DCF010: Email thread with conflicting timezones."""
    ticket = _tickets_by_id()["INC-DCF010"]
    gold = _gold_by_id()["INC-DCF010"]
    desc = ticket["description"]
    tz_patterns = ["EST", "UTC", "IST", "AEST", "PST", "CET", "GMT", "PDT", "EDT"]
    tz_count = sum(1 for tz in tz_patterns if tz in desc)
    assert tz_count >= 2, f"Ticket should contain at least 2 timezone references, found {tz_count}"
    assert gold["category"] == "Network & Connectivity"
    assert gold["assigned_team"] == "Network Operations"
    assert gold["priority"] == "P1"
    assert gold["needs_escalation"] is True


def test_dcf011_clipboard_paste_bomb():
    """INC-DCF011: Same text repeated many times (clipboard paste bomb)."""
    ticket = _tickets_by_id()["INC-DCF011"]
    gold = _gold_by_id()["INC-DCF011"]
    desc = ticket["description"]
    # Find repeated lines
    lines = [line.strip() for line in desc.split("\n") if line.strip()]
    if len(lines) >= 5:
        from collections import Counter
        line_counts = Counter(lines)
        most_common_line, most_common_count = line_counts.most_common(1)[0]
        assert most_common_count >= 10, (
            f"Clipboard paste bomb should have ≥10 repeated lines, found max {most_common_count}"
        )
    assert gold["category"] == "Network & Connectivity"
    assert gold["assigned_team"] == "Network Operations"


def test_dcf012_api_rate_limit_json():
    """INC-DCF012: API rate limit JSON error responses."""
    ticket = _tickets_by_id()["INC-DCF012"]
    gold = _gold_by_id()["INC-DCF012"]
    desc = ticket["description"]
    has_rate_limit = (
        "429" in desc
        or "rate limit" in desc.lower()
        or "too many requests" in desc.lower()
        or "retry" in desc.lower()
        or "throttl" in desc.lower()
    )
    assert has_rate_limit, "Ticket should contain API rate limit content"
    assert gold["category"] == "Software & Applications"
    assert gold["assigned_team"] == "Enterprise Applications"


def test_dcf013_corrupted_csv():
    """INC-DCF013: Corrupted CSV with mismatched columns."""
    ticket = _tickets_by_id()["INC-DCF013"]
    gold = _gold_by_id()["INC-DCF013"]
    desc = ticket["description"]
    has_csv = (
        "," in desc
        or "\t" in desc
        or "csv" in desc.lower()
        or "column" in desc.lower()
        or "delimiter" in desc.lower()
        or "import" in desc.lower()
    )
    assert has_csv, "Ticket should contain CSV/data import content"
    assert gold["category"] == "Data & Storage"
    assert gold["assigned_team"] == "Data Platform"


def test_dcf014_special_char_file_paths():
    """INC-DCF014: File paths with special characters / unicode."""
    ticket = _tickets_by_id()["INC-DCF014"]
    gold = _gold_by_id()["INC-DCF014"]
    desc = ticket["description"]
    has_paths = (
        "C:\\" in desc
        or "/" in desc
        or "\\\\" in desc
        or "OneDrive" in desc
        or "sync" in desc.lower()
        or "file" in desc.lower()
    )
    assert has_paths, "Ticket should contain file paths"
    # Check for special characters in the paths
    has_special = bool(re.search(r"[àâäéèêëïîôùûüÿçñ]|año|José|García|Ñ", desc))
    assert has_special or "special" in desc.lower() or "unicode" in desc.lower(), (
        "Ticket should contain paths with special characters"
    )
    assert gold["category"] == "Data & Storage"
    assert gold["assigned_team"] == "Data Platform"


def test_dcf015_log4j_security_scan():
    """INC-DCF015: Log4j/logging pattern strings from security scan report."""
    ticket = _tickets_by_id()["INC-DCF015"]
    gold = _gold_by_id()["INC-DCF015"]
    desc = ticket["description"]
    has_log4j = (
        "${jndi" in desc
        or "log4j" in desc.lower()
        or "log4shell" in desc.lower()
        or "jndi" in desc.lower()
        or "vulnerability" in desc.lower()
        or "CVE-" in desc
    )
    assert has_log4j, "Ticket should contain Log4j/security scan patterns"
    assert gold["category"] == "Security & Compliance"
    assert gold["assigned_team"] == "Security Operations"
    assert gold["priority"] == "P1"
    assert gold["needs_escalation"] is True


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


def test_all_predict_same_category_scores_low():
    """Predicting the same category for all tickets should score poorly."""
    gold = _load_gold()
    bad_submissions = []
    for g in gold:
        bad_submissions.append({
            "ticket_id": g["ticket_id"],
            "category": "Software & Applications",
            "priority": "P3",
            "assigned_team": "Enterprise Applications",
            "needs_escalation": False,
            "missing_information": [],
            "next_best_action": "Investigate",
            "remediation_steps": ["Check logs"],
        })
    result = score_submission(bad_submissions, gold)
    assert result["classification_score"] < 75, (
        f"All same category should score < 75, got {result['classification_score']}"
    )


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

    # SQL statements shouldn't leak into gold answers
    if re.search(r"\bSELECT\b.*\bFROM\b", combined, re.IGNORECASE):
        issues.append("SQL SELECT statement in gold answer")

    if re.search(r"\bDROP\s+TABLE\b", combined, re.IGNORECASE):
        issues.append("DROP TABLE in gold answer")

    # Base64 data shouldn't leak into gold answers
    if re.search(r"data:image/[a-z]+;base64,", combined):
        issues.append("base64 image data in gold answer")

    # JWT tokens shouldn't leak
    if re.search(r"eyJ[A-Za-z0-9_-]{20,}", combined):
        issues.append("JWT token in gold answer")

    # Raw XML event log shouldn't leak
    if "<Event " in combined or "<EventID>" in combined:
        issues.append("Windows Event XML in gold answer")

    # Docker log prefixes shouldn't leak
    if re.search(r"container_\w+\s*\|", combined):
        issues.append("Docker log prefix in gold answer")

    # JNDI lookup strings shouldn't leak
    if "${jndi:" in combined:
        issues.append("JNDI lookup string in gold answer")

    # Pipeline YAML shouldn't leak
    if "- task:" in combined.lower() or "displayName:" in combined:
        issues.append("Pipeline YAML in gold answer")

    # CSV data rows shouldn't leak
    if re.search(r"(?:\w+,){4,}\w+", combined):
        issues.append("CSV data row in gold answer")

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
            assert g["assigned_team"] == "None", f"{g['ticket_id']}: 'Not a Support Ticket' should route to 'None'"


def test_none_team_only_for_non_support():
    allowed_categories = {"Not a Support Ticket", "General Inquiry"}
    for g in _load_gold():
        if g["assigned_team"] == "None":
            assert g["category"] in allowed_categories, f"{g['ticket_id']}: team 'None' with category '{g['category']}'"


# ═══════════════════════════════════════════════════════════════════════
# SECTION 7: Data-quality property tests (across dataset)
# ═══════════════════════════════════════════════════════════════════════


def test_at_least_one_ticket_has_sql():
    """At least one ticket should contain SQL content."""
    tickets = _load_tickets()
    found = any(
        "SELECT" in t["description"] or "INSERT" in t["description"] or "sql" in t["description"].lower()
        for t in tickets
    )
    assert found, "No ticket contains SQL content"


def test_at_least_one_ticket_has_json():
    """At least one ticket should contain JSON content."""
    tickets = _load_tickets()
    found = any('{"' in t["description"] or '"error"' in t["description"] for t in tickets)
    assert found, "No ticket contains JSON content"


def test_at_least_one_ticket_has_xml():
    """At least one ticket should contain XML/event log content."""
    tickets = _load_tickets()
    found = any("<Event" in t["description"] or "<?xml" in t["description"] for t in tickets)
    assert found, "No ticket contains XML content"


def test_at_least_one_ticket_has_encoding_issues():
    """At least one ticket should contain encoding mojibake."""
    tickets = _load_tickets()
    found = any("Ã" in t["description"] or "â€" in t["description"] for t in tickets)
    assert found, "No ticket contains encoding mojibake"


def test_at_least_one_ticket_has_token():
    """At least one ticket should contain authentication token data."""
    tickets = _load_tickets()
    found = any("eyJ" in t["description"] or "bearer" in t["description"].lower() for t in tickets)
    assert found, "No ticket contains token data"


def test_at_least_one_ticket_has_container_logs():
    """At least one ticket should contain container/Docker log output."""
    tickets = _load_tickets()
    found = any(
        "docker" in t["description"].lower() or "container" in t["description"].lower()
        for t in tickets
    )
    assert found, "No ticket contains container log output"


def test_at_least_one_ticket_has_log4j_pattern():
    """At least one ticket should contain log4j/JNDI patterns."""
    tickets = _load_tickets()
    found = any(
        "${jndi" in t["description"] or "log4j" in t["description"].lower()
        for t in tickets
    )
    assert found, "No ticket contains log4j/JNDI patterns"


def test_average_description_length_above_400():
    """Forensic cleanup tickets should be substantial."""
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
    dc_ids = _load_ids_from("data_cleanup_eval.json")
    our_ids = {t["ticket_id"] for t in _load_tickets()}
    overlap = dc_ids & our_ids
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


def test_no_id_collision_with_mastery_dc():
    """No overlap with mastery data cleanup dataset."""
    other_ids = _load_ids_from("data_cleanup_mastery_eval.json")
    our_ids = {t["ticket_id"] for t in _load_tickets()}
    overlap = other_ids & our_ids
    assert not overlap, f"ID collision with data_cleanup_mastery_eval: {overlap}"


def test_no_id_collision_with_comprehensive_dc():
    """No overlap with comprehensive data cleanup dataset."""
    other_ids = _load_ids_from("data_cleanup_comprehensive_eval.json")
    our_ids = {t["ticket_id"] for t in _load_tickets()}
    overlap = other_ids & our_ids
    assert not overlap, f"ID collision with data_cleanup_comprehensive_eval: {overlap}"


def test_no_id_collision_with_scoring_dc():
    """No overlap with scoring data cleanup dataset."""
    other_ids = _load_ids_from("data_cleanup.json")
    our_ids = {t["ticket_id"] for t in _load_tickets()}
    overlap = other_ids & our_ids
    assert not overlap, f"ID collision with data_cleanup.json: {overlap}"


def test_no_id_collision_with_rai_datasets():
    """No overlap with any responsible AI datasets."""
    for filename in (
        "responsible_ai_eval.json",
        "responsible_ai.json",
        "responsible_ai_advanced_eval.json",
        "responsible_ai_expert_eval.json",
        "responsible_ai_mastery_eval.json",
        "responsible_ai_comprehensive_eval.json",
        "responsible_ai_forensic_eval.json",
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
