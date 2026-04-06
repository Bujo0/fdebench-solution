#!/usr/bin/env python3
"""Evaluation tests for expert data cleanup scenarios.

Tests that the triage system correctly handles expert-level messy/noisy input
beyond the base and advanced data cleanup scenarios — including GraphQL response
dumps, Kubernetes pod logs, double-escaped JSON, webpack bundler errors,
PowerShell error streams, Windows Registry exports, PEM certificate chains,
systemd journal floods, mixed CJK/Latin text, full HTTP response dumps,
nested MIME multipart, git commit history, Terraform plan output, DNS zone
files, and packet capture text output.

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

The tests cover the expert data cleanup dataset:
  • data_cleanup_expert_eval.json (15 tickets, INC-DCX###)

Usage:
    cd docs/eval
    python test_data_cleanup_expert.py

    # Or with pytest:
    uv run pytest test_data_cleanup_expert.py -v
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
_TICKETS_PATH = _DATA_DIR / "data_cleanup_expert_eval.json"
_GOLD_PATH = _DATA_DIR / "data_cleanup_expert_eval_gold.json"

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
# SECTION 1: Dataset integrity (15 tickets, INC-DCX###)
# ═══════════════════════════════════════════════════════════════════════


def test_tickets_file_exists():
    assert _TICKETS_PATH.exists(), f"Missing: {_TICKETS_PATH}"


def test_gold_file_exists():
    assert _GOLD_PATH.exists(), f"Missing: {_GOLD_PATH}"


def test_ticket_count_is_15():
    assert len(_load_tickets()) == 15, f"Expected 15 expert DC tickets, got {len(_load_tickets())}"


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
        assert t["ticket_id"].startswith("INC-DCX"), f"Bad prefix: {t['ticket_id']}"


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


def test_dcx001_graphql_response_dump():
    """INC-DCX001: GraphQL nested response dump in ticket body."""
    ticket = _tickets_by_id()["INC-DCX001"]
    gold = _gold_by_id()["INC-DCX001"]
    desc = ticket["description"]
    has_graphql = (
        "__typename" in desc
        or "edges" in desc
        or "nodes" in desc
        or "pageInfo" in desc
        or "graphql" in desc.lower()
        or "query" in desc.lower()
    )
    assert has_graphql, "Ticket should contain GraphQL response content"
    assert gold["category"] == "Software & Applications"
    assert gold["assigned_team"] == "Enterprise Applications"


def test_dcx002_kubernetes_pod_logs():
    """INC-DCX002: Kubernetes multi-container pod logs."""
    ticket = _tickets_by_id()["INC-DCX002"]
    gold = _gold_by_id()["INC-DCX002"]
    desc = ticket["description"]
    has_k8s = (
        "kubectl" in desc.lower()
        or "pod" in desc.lower()
        or "container" in desc.lower()
        or "namespace" in desc.lower()
        or "oom" in desc.lower()
    )
    assert has_k8s, "Ticket should contain Kubernetes log content"
    assert gold["category"] == "Software & Applications"
    assert gold["priority"] == "P1"
    assert gold["needs_escalation"] is True


def test_dcx003_double_escaped_json():
    """INC-DCX003: Double-escaped JSON strings in ticket."""
    ticket = _tickets_by_id()["INC-DCX003"]
    gold = _gold_by_id()["INC-DCX003"]
    desc = ticket["description"]
    has_escaped = '\\"' in desc or "\\\\" in desc or "escaped" in desc.lower() or "parse" in desc.lower()
    assert has_escaped, "Ticket should contain double-escaped JSON content"
    assert gold["category"] == "Software & Applications"
    assert gold["assigned_team"] == "Enterprise Applications"


def test_dcx004_webpack_bundler_error():
    """INC-DCX004: Webpack build error with chunk hashes."""
    ticket = _tickets_by_id()["INC-DCX004"]
    gold = _gold_by_id()["INC-DCX004"]
    desc = ticket["description"]
    has_webpack = (
        "webpack" in desc.lower()
        or "chunk" in desc.lower()
        or "module" in desc.lower()
        or "bundle" in desc.lower()
        or "build" in desc.lower()
    )
    assert has_webpack, "Ticket should contain webpack build error output"
    assert gold["category"] == "Software & Applications"
    assert gold["assigned_team"] == "Enterprise Applications"


def test_dcx005_powershell_error_stream():
    """INC-DCX005: PowerShell verbose error output."""
    ticket = _tickets_by_id()["INC-DCX005"]
    gold = _gold_by_id()["INC-DCX005"]
    desc = ticket["description"]
    has_ps = (
        "powershell" in desc.lower()
        or "CategoryInfo" in desc
        or "FullyQualifiedErrorId" in desc
        or "ScriptStackTrace" in desc
        or "cmdlet" in desc.lower()
        or "ErrorRecord" in desc
    )
    assert has_ps, "Ticket should contain PowerShell error output"
    assert gold["category"] == "Software & Applications"
    assert gold["assigned_team"] == "Enterprise Applications"


def test_dcx006_windows_registry_export():
    """INC-DCX006: Windows Registry .reg file content."""
    ticket = _tickets_by_id()["INC-DCX006"]
    gold = _gold_by_id()["INC-DCX006"]
    desc = ticket["description"]
    has_reg = (
        "HKEY" in desc
        or "REG_" in desc
        or "Registry" in desc
        or "Windows Registry" in desc
        or "regedit" in desc.lower()
    )
    assert has_reg, "Ticket should contain Windows Registry export content"
    assert gold["category"] == "Software & Applications"
    assert gold["assigned_team"] == "Endpoint Engineering"


def test_dcx007_pem_certificate_chain():
    """INC-DCX007: PEM-encoded X.509 certificate chain."""
    ticket = _tickets_by_id()["INC-DCX007"]
    gold = _gold_by_id()["INC-DCX007"]
    desc = ticket["description"]
    has_pem = (
        "BEGIN CERTIFICATE" in desc
        or "END CERTIFICATE" in desc
        or "-----BEGIN" in desc
        or "certificate" in desc.lower()
    )
    assert has_pem, "Ticket should contain PEM certificate content"
    assert gold["category"] == "Security & Compliance"
    assert gold["assigned_team"] == "Security Operations"
    assert gold["needs_escalation"] is True


def test_dcx008_systemd_journal_flood():
    """INC-DCX008: Systemd journal output flood."""
    ticket = _tickets_by_id()["INC-DCX008"]
    gold = _gold_by_id()["INC-DCX008"]
    desc = ticket["description"]
    has_systemd = (
        "systemd" in desc.lower()
        or "journalctl" in desc.lower()
        or "systemctl" in desc.lower()
        or ".service" in desc
        or "-- Logs begin" in desc
    )
    assert has_systemd, "Ticket should contain systemd journal output"
    assert gold["category"] == "Software & Applications"
    assert gold["assigned_team"] == "Enterprise Applications"


def test_dcx009_mixed_cjk_latin():
    """INC-DCX009: Mixed CJK (Chinese/Japanese/Korean) and Latin text."""
    ticket = _tickets_by_id()["INC-DCX009"]
    gold = _gold_by_id()["INC-DCX009"]
    desc = ticket["description"]
    has_cjk = bool(re.search(r"[一-鿿぀-ゟ゠-ヿ가-힯]", desc))
    assert has_cjk, "Ticket should contain CJK characters"
    assert gold["category"] == "Software & Applications"
    assert gold["assigned_team"] == "Enterprise Applications"


def test_dcx010_http_response_dump():
    """INC-DCX010: Full HTTP response with headers and body."""
    ticket = _tickets_by_id()["INC-DCX010"]
    gold = _gold_by_id()["INC-DCX010"]
    desc = ticket["description"]
    has_http = (
        "HTTP/" in desc or "Content-Type" in desc or "X-Request-Id" in desc or "502" in desc or "status" in desc.lower()
    )
    assert has_http, "Ticket should contain HTTP response content"
    assert gold["category"] == "Network & Connectivity"
    assert gold["assigned_team"] == "Network Operations"


def test_dcx011_mime_multipart_nested():
    """INC-DCX011: Base64 multipart with nested MIME boundaries."""
    ticket = _tickets_by_id()["INC-DCX011"]
    gold = _gold_by_id()["INC-DCX011"]
    desc = ticket["description"]
    has_mime = (
        "Content-Type" in desc
        or "multipart" in desc.lower()
        or "boundary" in desc.lower()
        or "Content-Transfer-Encoding" in desc
        or "base64" in desc.lower()
    )
    assert has_mime, "Ticket should contain MIME multipart content"
    assert gold["category"] == "Software & Applications"
    assert gold["assigned_team"] == "Enterprise Applications"


def test_dcx012_git_commit_history():
    """INC-DCX012: Git log/commit history dump."""
    ticket = _tickets_by_id()["INC-DCX012"]
    gold = _gold_by_id()["INC-DCX012"]
    desc = ticket["description"]
    has_git = (
        "commit " in desc.lower()
        or "Author:" in desc
        or "Merge:" in desc
        or "git log" in desc.lower()
        or "git" in desc.lower()
    )
    assert has_git, "Ticket should contain git commit history"
    assert gold["category"] == "Software & Applications"
    assert gold["assigned_team"] == "Enterprise Applications"


def test_dcx013_terraform_plan():
    """INC-DCX013: Terraform plan output with resource changes."""
    ticket = _tickets_by_id()["INC-DCX013"]
    gold = _gold_by_id()["INC-DCX013"]
    desc = ticket["description"]
    has_terraform = (
        "terraform" in desc.lower()
        or "resource" in desc.lower()
        or "Plan:" in desc
        or "azurerm_" in desc
        or "provider" in desc.lower()
    )
    assert has_terraform, "Ticket should contain Terraform plan output"
    assert gold["category"] == "Data & Storage"
    assert gold["assigned_team"] == "Data Platform"


def test_dcx014_dns_zone_file():
    """INC-DCX014: DNS zone file records."""
    ticket = _tickets_by_id()["INC-DCX014"]
    gold = _gold_by_id()["INC-DCX014"]
    desc = ticket["description"]
    has_dns = (
        "SOA" in desc or "IN A" in desc or "CNAME" in desc or "MX" in desc or "TXT" in desc or "zone" in desc.lower()
    )
    assert has_dns, "Ticket should contain DNS zone file records"
    assert gold["category"] == "Network & Connectivity"
    assert gold["assigned_team"] == "Network Operations"
    assert gold["priority"] == "P1"
    assert gold["needs_escalation"] is True


def test_dcx015_pcap_text_output():
    """INC-DCX015: tcpdump/packet capture text output."""
    ticket = _tickets_by_id()["INC-DCX015"]
    gold = _gold_by_id()["INC-DCX015"]
    desc = ticket["description"]
    has_pcap = (
        "tcpdump" in desc.lower()
        or "flags" in desc.lower()
        or "seq" in desc.lower()
        or "ack" in desc.lower()
        or "IP " in desc
        or ">" in desc
    )
    assert has_pcap, "Ticket should contain packet capture output"
    assert gold["category"] == "Network & Connectivity"
    assert gold["assigned_team"] == "Network Operations"


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

    # PEM certificate blocks shouldn't leak
    if "BEGIN CERTIFICATE" in combined or "END CERTIFICATE" in combined:
        issues.append("PEM certificate data in gold answer")

    # Kubernetes log prefixes shouldn't leak
    if re.search(r"\[.*\]\s+\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}", combined):
        issues.append("k8s log prefix in gold answer")

    # GraphQL __typename shouldn't leak
    if "__typename" in combined:
        issues.append("GraphQL __typename in gold answer")

    # Registry HKEY paths shouldn't leak
    if "HKEY_" in combined:
        issues.append("Windows Registry HKEY path in gold answer")

    # Terraform resource IDs shouldn't leak
    if re.search(r"azurerm_\w+\.\w+", combined):
        issues.append("Terraform resource ID in gold answer")

    # DNS record format shouldn't leak
    if re.search(r"\bIN\s+(A|AAAA|CNAME|MX|TXT|SOA|NS|SRV)\b", combined):
        issues.append("DNS record format in gold answer")

    # Packet capture data shouldn't leak
    if re.search(r"Flags \[", combined):
        issues.append("pcap Flags data in gold answer")

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


def test_at_least_one_ticket_has_graphql():
    """At least one ticket should contain GraphQL response content."""
    tickets = _load_tickets()
    found = any(
        "__typename" in t["description"] or "edges" in t["description"] or "graphql" in t["description"].lower()
        for t in tickets
    )
    assert found, "No ticket contains GraphQL content"


def test_at_least_one_ticket_has_k8s_logs():
    """At least one ticket should contain Kubernetes log output."""
    tickets = _load_tickets()
    found = any(
        "kubectl" in t["description"].lower()
        or "pod" in t["description"].lower()
        or "namespace" in t["description"].lower()
        for t in tickets
    )
    assert found, "No ticket contains Kubernetes log content"


def test_at_least_one_ticket_has_json():
    """At least one ticket should contain JSON content."""
    tickets = _load_tickets()
    found = any('{"' in t["description"] or '": ' in t["description"] for t in tickets)
    assert found, "No ticket contains JSON content"


def test_at_least_one_ticket_has_pem():
    """At least one ticket should contain PEM certificate data."""
    tickets = _load_tickets()
    found = any("BEGIN CERTIFICATE" in t["description"] or "-----BEGIN" in t["description"] for t in tickets)
    assert found, "No ticket contains PEM certificate data"


def test_at_least_one_ticket_has_cjk():
    """At least one ticket should contain CJK characters."""
    tickets = _load_tickets()
    found = any(bool(re.search(r"[一-鿿぀-ゟ゠-ヿ가-힯]", t["description"])) for t in tickets)
    assert found, "No ticket contains CJK characters"


def test_at_least_one_ticket_has_http_headers():
    """At least one ticket should contain HTTP response headers."""
    tickets = _load_tickets()
    found = any("HTTP/" in t["description"] or "Content-Type" in t["description"] for t in tickets)
    assert found, "No ticket contains HTTP response headers"


def test_at_least_one_ticket_has_terraform():
    """At least one ticket should contain Terraform plan output."""
    tickets = _load_tickets()
    found = any("terraform" in t["description"].lower() or "azurerm_" in t["description"] for t in tickets)
    assert found, "No ticket contains Terraform output"


def test_average_description_length_above_300():
    """Expert cleanup tickets should be substantive."""
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
    dcx_ids = {t["ticket_id"] for t in _load_tickets()}
    overlap = dc_ids & dcx_ids
    assert not overlap, f"ID collision with INC-DC### dataset: {overlap}"


def test_no_id_collision_with_advanced_dc():
    """No overlap with INC-DCA### advanced data cleanup dataset."""
    dca_path = _DATA_DIR / "data_cleanup_advanced_eval.json"
    if not dca_path.exists():
        return
    dca_tickets = json.loads(dca_path.read_text())
    dca_ids = {t["ticket_id"] for t in dca_tickets}
    dcx_ids = {t["ticket_id"] for t in _load_tickets()}
    overlap = dca_ids & dcx_ids
    assert not overlap, f"ID collision with INC-DCA### dataset: {overlap}"


def test_no_id_collision_with_scoring_dc():
    """No overlap with INC-5### scoring data cleanup dataset."""
    sc_path = _DATA_DIR / "data_cleanup.json"
    if not sc_path.exists():
        return
    sc_tickets = json.loads(sc_path.read_text())
    sc_ids = {t["ticket_id"] for t in sc_tickets}
    dcx_ids = {t["ticket_id"] for t in _load_tickets()}
    overlap = sc_ids & dcx_ids
    assert not overlap, f"ID collision with INC-5### dataset: {overlap}"


def test_no_id_collision_with_rai_datasets():
    """No overlap with responsible AI datasets."""
    for filename in (
        "responsible_ai_eval.json",
        "responsible_ai.json",
        "responsible_ai_advanced_eval.json",
        "responsible_ai_expert_eval.json",
    ):
        path = _DATA_DIR / filename
        if not path.exists():
            continue
        other_tickets = json.loads(path.read_text())
        other_ids = {t["ticket_id"] for t in other_tickets}
        dcx_ids = {t["ticket_id"] for t in _load_tickets()}
        overlap = other_ids & dcx_ids
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
