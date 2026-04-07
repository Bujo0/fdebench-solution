#!/usr/bin/env python3
"""Evaluation tests for the comprehensive data cleanup scenarios.

Tests that the triage system correctly handles advanced real-world data quality
issues including Docker container logs, Kubernetes YAML manifests, Terraform plan
output, git diffs, PEM certificate chains, raw MIME multipart content, DNS zone
files, packet capture text, deeply nested Java exceptions, and spreadsheet
tab-delimited pastes.

These tests validate:
  1. Dataset integrity — ticket and gold data are well-formed.
  2. Gold answer correctness — all values within constrained vocabulary.
  3. Scoring pipeline — gold vs gold yields a perfect score.
  4. Per-ticket data-quality tests — each ticket exhibits its claimed noise type.
  5. Noise resilience — gold classification is correct despite noise.
  6. Structural invariants — team/category consistency.
  7. Output contamination detection — gold answers don't contain input noise.
  8. Cross-dataset consistency — no ID overlap with other datasets.

The tests cover the comprehensive data cleanup dataset:
  • data_cleanup_comprehensive_eval.json (10 tickets, INC-DC-5001–INC-DC-5010)

Usage:
    cd docs/eval
    python test_data_cleanup_comprehensive.py

    # Or with pytest:
    uv run pytest test_data_cleanup_comprehensive.py -v
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
_TICKETS_PATH = _DATA_DIR / "data_cleanup_comprehensive_eval.json"
_GOLD_PATH = _DATA_DIR / "data_cleanup_comprehensive_eval_gold.json"

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

# ── Load datasets ────────────────────────────────────────────────────

_TICKETS: list[dict] = json.loads(_TICKETS_PATH.read_text())
_GOLD: list[dict] = json.loads(_GOLD_PATH.read_text())
_GOLD_BY_ID: dict[str, dict] = {g["ticket_id"]: g for g in _GOLD}
_TICKETS_BY_ID: dict[str, dict] = {t["ticket_id"]: t for t in _TICKETS}


# ── 1. Dataset integrity ─────────────────────────────────────────────


def test_dataset_has_10_tickets():
    assert len(_TICKETS) == 10, f"Expected 10 tickets, got {len(_TICKETS)}"


def test_gold_count_matches():
    assert len(_GOLD) == len(_TICKETS)


def test_ticket_ids_match():
    t_ids = {t["ticket_id"] for t in _TICKETS}
    g_ids = {g["ticket_id"] for g in _GOLD}
    assert t_ids == g_ids


def test_all_ids_follow_pattern():
    for t in _TICKETS:
        assert re.match(r"^INC-DC-\d+$", t["ticket_id"]), f"Bad ID: {t['ticket_id']}"


def test_no_duplicate_ids():
    ids = [t["ticket_id"] for t in _TICKETS]
    assert len(ids) == len(set(ids))


def test_ordering_matches():
    for t, g in zip(_TICKETS, _GOLD, strict=True):
        assert t["ticket_id"] == g["ticket_id"]


# ── 2. Gold answer validation ────────────────────────────────────────


def test_gold_categories_valid():
    for g in _GOLD:
        assert g["category"] in _VALID_CATEGORIES, f"{g['ticket_id']}: '{g['category']}'"


def test_gold_priorities_valid():
    for g in _GOLD:
        assert g["priority"] in _VALID_PRIORITIES, f"{g['ticket_id']}: '{g['priority']}'"


def test_gold_teams_valid():
    for g in _GOLD:
        assert g["assigned_team"] in _VALID_TEAMS, f"{g['ticket_id']}: '{g['assigned_team']}'"


def test_gold_missing_info_valid():
    for g in _GOLD:
        for item in g["missing_information"]:
            assert item in _VALID_MISSING_INFO, f"{g['ticket_id']}: '{item}'"


def test_gold_schema_fields():
    for g in _GOLD:
        missing = _REQUIRED_GOLD_FIELDS - set(g.keys())
        assert not missing, f"{g['ticket_id']}: missing {missing}"


def test_gold_escalation_is_bool():
    for g in _GOLD:
        assert isinstance(g["needs_escalation"], bool)


def test_gold_remediation_nonempty():
    for g in _GOLD:
        assert isinstance(g["remediation_steps"], list) and len(g["remediation_steps"]) > 0


def test_gold_next_best_action_nonempty():
    for g in _GOLD:
        assert g.get("next_best_action", "").strip()


# ── 3. Scoring sanity ────────────────────────────────────────────────


def test_perfect_submission_scores_85():
    result = score_submission(_GOLD, _GOLD)
    assert result["classification_score"] == 85.0


def test_perfect_submission_no_errors():
    result = score_submission(_GOLD, _GOLD)
    assert result["tickets_errored"] == 0


def test_each_ticket_scores_perfectly():
    for g in _GOLD:
        scores = score_ticket(dict(g), g)
        assert scores["weighted_total"] > 0.84, f"{g['ticket_id']}: {scores['weighted_total']}"


# ── 4. Per-ticket data-quality tests ─────────────────────────────────


def test_docker_logs_contain_oom():
    """INC-DC-5001: Docker container logs should contain OOM errors."""
    t = _TICKETS_BY_ID["INC-DC-5001"]
    assert "OutOfMemoryError" in t["description"]
    assert "Container killed" in t["description"] or "OOM" in t["description"]
    g = _GOLD_BY_ID["INC-DC-5001"]
    assert g["category"] == "Software & Applications"
    assert g["priority"] == "P1"


def test_kubernetes_yaml_has_crashloop():
    """INC-DC-5002: K8s output should show CrashLoopBackOff."""
    t = _TICKETS_BY_ID["INC-DC-5002"]
    assert "CrashLoopBackOff" in t["description"]
    g = _GOLD_BY_ID["INC-DC-5002"]
    assert g["category"] == "Software & Applications"


def test_terraform_plan_has_destroy():
    """INC-DC-5003: Terraform plan should show resource destruction."""
    t = _TICKETS_BY_ID["INC-DC-5003"]
    assert "DESTROYED" in t["description"] or "destroy" in t["description"].lower()
    assert "Terraform" in t["description"]
    g = _GOLD_BY_ID["INC-DC-5003"]
    assert g["category"] == "Network & Connectivity"
    assert g["priority"] == "P1"
    assert g["needs_escalation"] is True


def test_git_diff_has_diff_markers():
    """INC-DC-5004: Git diff should have unified diff format."""
    t = _TICKETS_BY_ID["INC-DC-5004"]
    assert "diff --git" in t["description"]
    assert "---" in t["description"] and "+++" in t["description"]
    g = _GOLD_BY_ID["INC-DC-5004"]
    assert g["category"] == "Access & Authentication"
    assert g["needs_escalation"] is False


def test_pem_cert_has_markers():
    """INC-DC-5005: PEM cert should have certificate markers."""
    t = _TICKETS_BY_ID["INC-DC-5005"]
    assert "-----BEGIN CERTIFICATE-----" in t["description"]
    assert "-----END CERTIFICATE-----" in t["description"]
    g = _GOLD_BY_ID["INC-DC-5005"]
    assert g["category"] == "Security & Compliance"
    assert g["priority"] == "P1"
    assert g["needs_escalation"] is True


def test_mime_multipart_has_boundaries():
    """INC-DC-5006: Raw MIME should have multipart boundaries."""
    t = _TICKETS_BY_ID["INC-DC-5006"]
    assert "boundary=" in t["description"]
    assert "Content-Type:" in t["description"]
    g = _GOLD_BY_ID["INC-DC-5006"]
    assert g["category"] == "Software & Applications"


def test_dns_zone_has_records():
    """INC-DC-5007: DNS zone file should have DNS records."""
    t = _TICKETS_BY_ID["INC-DC-5007"]
    desc = t["description"]
    assert "IN  A" in desc or "$TTL" in desc
    g = _GOLD_BY_ID["INC-DC-5007"]
    assert g["category"] == "Network & Connectivity"
    assert g["priority"] == "P2"


def test_packet_capture_has_tcp():
    """INC-DC-5008: Packet capture should have TCP packet data."""
    t = _TICKETS_BY_ID["INC-DC-5008"]
    assert "Flags [" in t["description"]
    assert "Retransmission" in t["description"]
    g = _GOLD_BY_ID["INC-DC-5008"]
    assert g["category"] == "Network & Connectivity"


def test_nested_java_exception_has_caused_by():
    """INC-DC-5009: Java exception should have multi-level nesting."""
    t = _TICKETS_BY_ID["INC-DC-5009"]
    caused_count = t["description"].count("Caused by:")
    assert caused_count >= 4, f"Expected ≥4 'Caused by:' levels, got {caused_count}"
    g = _GOLD_BY_ID["INC-DC-5009"]
    assert g["category"] == "Data & Storage"
    assert g["priority"] == "P1"
    assert g["needs_escalation"] is True


def test_spreadsheet_paste_has_tabs():
    """INC-DC-5010: Spreadsheet paste should have tab-delimited data."""
    t = _TICKETS_BY_ID["INC-DC-5010"]
    assert "\t" in t["description"]
    g = _GOLD_BY_ID["INC-DC-5010"]
    assert g["category"] == "Access & Authentication"


# ── 5. Distribution coverage ─────────────────────────────────────────


def test_multiple_categories():
    cats = {g["category"] for g in _GOLD}
    assert len(cats) >= 4, f"Only {len(cats)} categories: {cats}"


def test_multiple_teams():
    teams = {g["assigned_team"] for g in _GOLD}
    assert len(teams) >= 4, f"Only {len(teams)} teams: {teams}"


def test_multiple_priorities():
    pris = {g["priority"] for g in _GOLD}
    assert len(pris) >= 3, f"Only {len(pris)} priorities: {pris}"


def test_has_escalated_tickets():
    escalated = sum(1 for g in _GOLD if g["needs_escalation"])
    assert escalated >= 3, f"Only {escalated} escalated tickets"


# ── 6. Structural invariants ─────────────────────────────────────────


def test_all_tickets_have_required_fields():
    for t in _TICKETS:
        missing = _REQUIRED_INPUT_FIELDS - set(t.keys())
        assert not missing, f"{t['ticket_id']}: {missing}"


def test_all_reporters_have_fields():
    for t in _TICKETS:
        for field in ("name", "email", "department"):
            assert field in t["reporter"], f"{t['ticket_id']}: reporter missing {field}"


def test_all_channels_valid():
    for t in _TICKETS:
        assert t["channel"] in _VALID_CHANNELS


def test_no_duplicate_missing_info():
    for g in _GOLD:
        items = g["missing_information"]
        assert len(items) == len(set(items)), f"{g['ticket_id']}: duplicates"


def test_not_a_support_ticket_routes_to_none():
    for g in _GOLD:
        if g["category"] == "Not a Support Ticket":
            assert g["assigned_team"] == "None"


# ── 7. Gold answers should not contain raw input noise ───────────────


def test_gold_remediation_no_base64_data():
    """Gold remediation should not contain large base64 blocks from input."""
    b64_pattern = re.compile(r"[A-Za-z0-9+/]{100,}={0,2}")
    for g in _GOLD:
        text = " ".join(g["remediation_steps"])
        assert not b64_pattern.search(text), f"{g['ticket_id']}: base64 in remediation"


def test_gold_remediation_no_stack_traces():
    """Gold remediation should not contain Java stack traces."""
    for g in _GOLD:
        text = " ".join(g["remediation_steps"])
        assert "at com." not in text and "\tat " not in text, f"{g['ticket_id']}: stack trace in remediation"


# ── 8. Cross-dataset consistency ─────────────────────────────────────


def test_no_overlap_with_other_dc_sets():
    """No ID collisions with other data cleanup datasets."""
    our_ids = {t["ticket_id"] for t in _TICKETS}
    for name in ["data_cleanup_eval", "data_cleanup_advanced_eval", "data_cleanup_expert_eval", "eval_data_cleanup"]:
        path = _DATA_DIR / f"{name}.json"
        if path.exists():
            try:
                other = json.loads(path.read_text())
                if isinstance(other, list):
                    other_ids = {t["ticket_id"] for t in other if isinstance(t, dict)}
                    overlap = our_ids & other_ids
                    assert not overlap, f"Overlap with {name}: {overlap}"
            except (json.JSONDecodeError, KeyError):
                pass


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
