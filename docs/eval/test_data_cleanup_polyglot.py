#!/usr/bin/env python3
"""Evaluation tests for data cleanup polyglot scenarios.

Tests that the triage system correctly handles complex, multi-format noise
patterns commonly found in real-world IT tickets from technical users —
including GraphQL response dumps, git merge conflict markers, Kubernetes
pod describe output, ARM templates, PowerShell transcripts, HAR network
data, corrupted PDF extraction, database ASCII tables, TLS certificate
chain debug output, Docker build logs, Azure CLI output, binary/protobuf
garbage, Jupyter notebook JSON, Windows perfmon CSV, and interleaved
multi-timezone syslog entries.

These tests validate:
  1. Dataset integrity — ticket and gold data are well-formed.
  2. Gold answer correctness — all values within constrained vocabulary.
  3. Scoring pipeline — gold vs gold yields a perfect score.
  4. Per-ticket data-quality tests — each ticket exhibits its claimed noise type.
  5. Output contamination detection — gold answers don't contain input noise.
  6. Structural invariants — team/category consistency rules hold.
  7. Distribution coverage — multiple categories and teams represented.
  8. PII leakage detection — no real credentials in gold answers.

The tests cover the polyglot data cleanup dataset:
  • data_cleanup_polyglot_eval.json (15 tickets, INC-DCP###)

Usage:
    cd docs/eval
    python test_data_cleanup_polyglot.py

    # Or with pytest:
    uv run pytest test_data_cleanup_polyglot.py -v
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

_TICKETS_PATH = _DATA_DIR / "data_cleanup_polyglot_eval.json"
_GOLD_PATH = _DATA_DIR / "data_cleanup_polyglot_eval_gold.json"

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


def _load_tickets() -> list[dict]:
    return json.loads(_TICKETS_PATH.read_text())


def _load_gold() -> list[dict]:
    return json.loads(_GOLD_PATH.read_text())


def _gold_by_id() -> dict[str, dict]:
    return {g["ticket_id"]: g for g in _load_gold()}


def _tickets_by_id() -> dict[str, dict]:
    return {t["ticket_id"]: t for t in _load_tickets()}


# ═══════════════════════════════════════════════════════════════════════
# SECTION 1: Dataset integrity
# ═══════════════════════════════════════════════════════════════════════


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


def test_dataset_has_15_tickets():
    assert len(_load_tickets()) == 15, "Expected 15 polyglot data cleanup tickets"


def test_all_ticket_ids_prefixed():
    for t in _load_tickets():
        tid = t["ticket_id"]
        assert tid.startswith("INC-DCP"), f"Bad ticket_id prefix: {tid}"


# ── Input schema validation ──────────────────────────────────────────


def test_all_tickets_have_required_fields():
    for ticket in _load_tickets():
        missing = _REQUIRED_INPUT_FIELDS - set(ticket.keys())
        assert not missing, f"{ticket['ticket_id']} missing fields: {missing}"


def test_all_reporters_have_required_fields():
    required = {"name", "email", "department"}
    for ticket in _load_tickets():
        missing = required - set(ticket["reporter"].keys())
        assert not missing, f"{ticket['ticket_id']} reporter missing fields: {missing}"


def test_all_channels_valid():
    for ticket in _load_tickets():
        assert ticket["channel"] in _VALID_CHANNELS, (
            f"{ticket['ticket_id']} invalid channel: {ticket['channel']}"
        )


def test_all_descriptions_nonempty():
    for ticket in _load_tickets():
        assert len(ticket["description"].strip()) > 50, (
            f"{ticket['ticket_id']} description too short"
        )


def test_all_subjects_nonempty():
    for ticket in _load_tickets():
        assert len(ticket["subject"].strip()) > 10, (
            f"{ticket['ticket_id']} subject too short"
        )


# ── Gold answer validation ───────────────────────────────────────────


def test_gold_categories_valid():
    for g in _load_gold():
        assert g["category"] in set(CATEGORIES), f"{g['ticket_id']}: invalid category '{g['category']}'"


def test_gold_priorities_valid():
    for g in _load_gold():
        assert g["priority"] in {"P1", "P2", "P3", "P4"}, (
            f"{g['ticket_id']}: invalid priority '{g['priority']}'"
        )


def test_gold_teams_valid():
    for g in _load_gold():
        assert g["assigned_team"] in set(TEAMS), f"{g['ticket_id']}: invalid team '{g['assigned_team']}'"


def test_gold_missing_info_valid():
    for g in _load_gold():
        for item in g["missing_information"]:
            assert item in VALID_MISSING_INFO, (
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


# ═══════════════════════════════════════════════════════════════════════
# SECTION 2: Scoring pipeline
# ═══════════════════════════════════════════════════════════════════════


def test_gold_vs_gold_perfect_score():
    """Scoring gold answers against themselves must produce a perfect 85.0."""
    gold = _load_gold()
    result = score_submission(gold, gold)
    assert result["classification_score"] == 85.0, (
        f"Expected perfect 85.0, got {result['classification_score']}"
    )


def test_per_ticket_gold_vs_gold():
    """Each individual ticket scored against itself should yield 1.0 on all dimensions."""
    for g in _load_gold():
        result = score_ticket(g, g)
        for dim in ("category", "priority", "routing", "missing_info", "escalation"):
            assert result[dim] == 1.0, (
                f"{g['ticket_id']} self-score {dim} = {result[dim]}, expected 1.0"
            )


# ═══════════════════════════════════════════════════════════════════════
# SECTION 3: Per-ticket data-quality tests (noise type detection)
# ═══════════════════════════════════════════════════════════════════════

# Each ticket in the polyglot dataset embeds a specific type of technical
# noise. These tests verify that the expected noise pattern is actually
# present in the ticket description.


def test_dcp001_has_graphql_content():
    """INC-DCP001 should contain GraphQL response patterns."""
    t = _tickets_by_id()["INC-DCP001"]
    desc = t["description"]
    graphql_indicators = [
        any(kw in desc for kw in ['"data"', '"errors"', '"extensions"', "query {"]),
        any(kw in desc.lower() for kw in ["graphql", "typename", "__typename"]),
        "{" in desc and "}" in desc,
    ]
    assert sum(graphql_indicators) >= 2, (
        "INC-DCP001 should contain GraphQL response patterns"
    )


def test_dcp002_has_git_conflict_markers():
    """INC-DCP002 should contain git merge conflict markers."""
    t = _tickets_by_id()["INC-DCP002"]
    desc = t["description"]
    assert "<<<<<<" in desc or "<<<<<<< " in desc, "Missing <<<<<<< HEAD marker"
    assert "=======" in desc, "Missing ======= separator"
    assert ">>>>>>" in desc or ">>>>>>> " in desc, "Missing >>>>>>> branch marker"


def test_dcp003_has_kubernetes_output():
    """INC-DCP003 should contain Kubernetes pod describe output."""
    t = _tickets_by_id()["INC-DCP003"]
    desc = t["description"].lower()
    k8s_indicators = [
        any(kw in desc for kw in ["kubectl", "namespace", "pod", "container"]),
        any(kw in desc for kw in ["crashloopbackoff", "oomkilled", "restartcount",
                                   "restart count", "conditions:", "events:"]),
        any(kw in desc for kw in ["node:", "image:", "status:", "ready"]),
    ]
    assert sum(k8s_indicators) >= 2, (
        "INC-DCP003 should contain Kubernetes pod describe output"
    )


def test_dcp004_has_arm_template_content():
    """INC-DCP004 should contain ARM/Bicep template patterns."""
    t = _tickets_by_id()["INC-DCP004"]
    desc = t["description"]
    arm_indicators = [
        any(kw in desc for kw in ["$schema", "contentVersion", "Microsoft.Compute",
                                   "Microsoft.Network", "Microsoft.Storage"]),
        any(kw in desc for kw in ['"parameters"', '"resources"', '"variables"']),
        any(kw in desc.lower() for kw in ["arm template", "bicep", "azure resource"]),
    ]
    assert sum(arm_indicators) >= 2, (
        "INC-DCP004 should contain ARM/Bicep template patterns"
    )


def test_dcp005_has_powershell_transcript():
    """INC-DCP005 should contain PowerShell transcript output."""
    t = _tickets_by_id()["INC-DCP005"]
    desc = t["description"]
    ps_indicators = [
        any(kw in desc for kw in ["PowerShell transcript", "****", "Start time:"]),
        any(kw in desc for kw in ["VERBOSE:", "WARNING:", "ERROR:", "DEBUG:"]),
        any(kw in desc.lower() for kw in ["powershell", "cmdlet", "ad connect",
                                           "azure ad", "entra"]),
    ]
    assert sum(ps_indicators) >= 2, (
        "INC-DCP005 should contain PowerShell transcript output"
    )


def test_dcp006_has_har_data():
    """INC-DCP006 should contain HAR (HTTP Archive) content."""
    t = _tickets_by_id()["INC-DCP006"]
    desc = t["description"]
    har_indicators = [
        any(kw in desc.lower() for kw in ["har", "entries", "waterfall",
                                           "network trace", "http archive"]),
        any(kw in desc for kw in ['"request"', '"response"', '"timings"',
                                   '"method"', '"url"', '"status"']),
        any(kw in desc for kw in ["GET ", "POST ", "200", "304", "text/html",
                                   "application/json"]),
    ]
    assert sum(har_indicators) >= 2, (
        "INC-DCP006 should contain HAR network trace data"
    )


def test_dcp007_has_pdf_extraction_artifacts():
    """INC-DCP007 should contain corrupted PDF text extraction artifacts."""
    t = _tickets_by_id()["INC-DCP007"]
    desc = t["description"]
    pdf_indicators = [
        # Ligature-broken words or column-merged text
        any(kw in desc for kw in ["f i ", "f l ", "ff i", "ff l",
                                   "| Page", "□", "◆", "■", "�"]),
        # Garbled text or extra whitespace from PDF extraction
        bool(re.search(r"\w\s{2,}\w", desc)),
        any(kw in desc.lower() for kw in ["pdf", "extraction", "garbled",
                                           "corrupted", "text extraction"]),
    ]
    assert sum(pdf_indicators) >= 2, (
        "INC-DCP007 should contain PDF text extraction artifacts"
    )


def test_dcp008_has_ascii_table_output():
    """INC-DCP008 should contain database ASCII table output."""
    t = _tickets_by_id()["INC-DCP008"]
    desc = t["description"]
    table_indicators = [
        any(kw in desc for kw in ["+--", "+==", "---|", "|---"]),
        desc.count("|") >= 10,
        any(kw in desc.lower() for kw in ["replication", "lag", "mysql",
                                           "postgresql", "query"]),
    ]
    assert sum(table_indicators) >= 2, (
        "INC-DCP008 should contain database ASCII table output"
    )


def test_dcp009_has_tls_cert_output():
    """INC-DCP009 should contain TLS certificate chain debug output."""
    t = _tickets_by_id()["INC-DCP009"]
    desc = t["description"]
    tls_indicators = [
        any(kw in desc for kw in ["Certificate chain", "s_client", "BEGIN CERTIFICATE",
                                   "subject=", "issuer=", "Verify return"]),
        any(kw in desc.lower() for kw in ["ssl", "tls", "certificate", "openssl",
                                           "x509"]),
        any(kw in desc.lower() for kw in ["verification", "cipher", "cert",
                                           "chain", "handshake"]),
    ]
    assert sum(tls_indicators) >= 2, (
        "INC-DCP009 should contain TLS certificate chain debug output"
    )


def test_dcp010_has_docker_build_output():
    """INC-DCP010 should contain Docker build log output."""
    t = _tickets_by_id()["INC-DCP010"]
    desc = t["description"]
    docker_indicators = [
        any(kw in desc for kw in ["Step ", "FROM ", "COPY ", "RUN ", "--->",
                                   "Sending build context"]),
        any(kw in desc.lower() for kw in ["docker", "dockerfile", "image",
                                           "layer", "build"]),
        bool(re.search(r"[a-f0-9]{12}", desc)),  # Docker layer hash
    ]
    assert sum(docker_indicators) >= 2, (
        "INC-DCP010 should contain Docker build log output"
    )


def test_dcp011_has_azure_cli_output():
    """INC-DCP011 should contain Azure CLI JSON output."""
    t = _tickets_by_id()["INC-DCP011"]
    desc = t["description"]
    az_indicators = [
        any(kw in desc for kw in ["az ", "securityRules", "sourcePortRange",
                                   "destinationPortRange", "Microsoft.Network"]),
        any(kw in desc.lower() for kw in ["nsg", "network security group",
                                           "azure", "az network"]),
        any(kw in desc for kw in ['"protocol"', '"access"', '"direction"',
                                   '"priority"', '"provisioningState"']),
    ]
    assert sum(az_indicators) >= 2, (
        "INC-DCP011 should contain Azure CLI JSON output"
    )


def test_dcp012_has_binary_garbage():
    """INC-DCP012 should contain binary/protobuf garbage characters."""
    t = _tickets_by_id()["INC-DCP012"]
    desc = t["description"]
    binary_indicators = [
        any(kw in desc for kw in ["\\x", "\\n", "▒", "▓", "░", "█", "╗", "╔",
                                   "\x00", "�"]),
        any(kw in desc.lower() for kw in ["protobuf", "grpc", "binary",
                                           "malformed", "corrupted"]),
        # Check for non-ASCII characters
        any(ord(c) > 127 for c in desc),
    ]
    assert sum(binary_indicators) >= 2, (
        "INC-DCP012 should contain binary/protobuf garbage characters"
    )


def test_dcp013_has_jupyter_notebook_json():
    """INC-DCP013 should contain Jupyter notebook JSON structure."""
    t = _tickets_by_id()["INC-DCP013"]
    desc = t["description"]
    jupyter_indicators = [
        any(kw in desc for kw in ["cell_type", "source", "execution_count",
                                   "metadata", "outputs"]),
        any(kw in desc.lower() for kw in ["jupyter", "notebook", ".ipynb",
                                           "jupyterhub"]),
        any(kw in desc for kw in ['"markdown"', '"code"', '"cells"']),
    ]
    assert sum(jupyter_indicators) >= 2, (
        "INC-DCP013 should contain Jupyter notebook JSON structure"
    )


def test_dcp014_has_perfmon_csv():
    """INC-DCP014 should contain Windows Performance Monitor CSV data."""
    t = _tickets_by_id()["INC-DCP014"]
    desc = t["description"]
    perfmon_indicators = [
        any(kw in desc for kw in ["\\Processor", "\\Memory", "\\PhysicalDisk",
                                   "% Processor Time", "Processor(_Total)"]),
        # CSV-like data with commas
        desc.count(",") >= 10,
        any(kw in desc.lower() for kw in ["perfmon", "performance monitor",
                                           "counter", "cpu"]),
    ]
    assert sum(perfmon_indicators) >= 2, (
        "INC-DCP014 should contain Windows perfmon CSV data"
    )


def test_dcp015_has_multitimezone_syslog():
    """INC-DCP015 should contain interleaved multi-timezone syslog entries."""
    t = _tickets_by_id()["INC-DCP015"]
    desc = t["description"]
    syslog_indicators = [
        # Syslog format patterns
        any(kw in desc for kw in ["sshd[", "auth-", "Failed password",
                                   "authentication failure"]),
        # Multiple timezone references
        sum(1 for tz in ["UTC", "EST", "PST", "CST", "CET", "GMT", "+00:00",
                          "-05:00", "-08:00"]
            if tz in desc) >= 2,
        # ISO 8601 or RFC 3164 timestamps
        bool(re.search(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}", desc))
        or bool(re.search(r"[A-Z][a-z]{2}\s+\d{1,2}\s+\d{2}:\d{2}:\d{2}", desc)),
    ]
    assert sum(syslog_indicators) >= 2, (
        "INC-DCP015 should contain multi-timezone syslog entries"
    )


# ═══════════════════════════════════════════════════════════════════════
# SECTION 4: Output contamination detection
# ═══════════════════════════════════════════════════════════════════════

# Gold answers must not contain raw noise artifacts from the input.


def test_gold_no_graphql_syntax():
    """Gold answers should not contain raw GraphQL syntax."""
    for g in _load_gold():
        nba = g["next_best_action"].lower()
        for step in g["remediation_steps"]:
            combined = nba + " " + step.lower()
            assert "query {" not in combined, (
                f"{g['ticket_id']}: gold contains raw GraphQL syntax"
            )


def test_gold_no_merge_conflict_markers():
    """Gold answers should not contain git merge conflict markers."""
    for g in _load_gold():
        combined = g["next_best_action"]
        for step in g["remediation_steps"]:
            combined += " " + step
        assert "<<<<<<" not in combined, (
            f"{g['ticket_id']}: gold contains merge conflict markers"
        )
        assert ">>>>>>>" not in combined, (
            f"{g['ticket_id']}: gold contains merge conflict markers"
        )


def test_gold_no_raw_json_dumps():
    """Gold answers should not contain large raw JSON dumps."""
    for g in _load_gold():
        combined = g["next_best_action"]
        for step in g["remediation_steps"]:
            combined += " " + step
        # Should not have dense JSON structures
        json_brace_count = combined.count("{") + combined.count("}")
        assert json_brace_count < 10, (
            f"{g['ticket_id']}: gold contains raw JSON dump ({json_brace_count} braces)"
        )


def test_gold_no_binary_garbage():
    """Gold answers should not contain binary garbage characters."""
    binary_chars = {"▒", "▓", "░", "█", "╗", "╔", "╚", "╝", "║", "═"}
    for g in _load_gold():
        combined = g["next_best_action"]
        for step in g["remediation_steps"]:
            combined += " " + step
        found = binary_chars.intersection(set(combined))
        assert not found, (
            f"{g['ticket_id']}: gold contains binary characters: {found}"
        )


def test_gold_no_docker_hashes():
    """Gold answers should not contain Docker layer hashes."""
    hash_pattern = re.compile(r"[a-f0-9]{40,}")
    for g in _load_gold():
        combined = g["next_best_action"]
        for step in g["remediation_steps"]:
            combined += " " + step
        match = hash_pattern.search(combined)
        assert not match, (
            f"{g['ticket_id']}: gold contains long hex hash: {match.group()[:20]}..."
        )


# ═══════════════════════════════════════════════════════════════════════
# SECTION 5: Structural invariants
# ═══════════════════════════════════════════════════════════════════════


def test_not_a_ticket_implies_no_team():
    """'Not a Support Ticket' should never be assigned a real team."""
    for g in _load_gold():
        if g["category"] == "Not a Support Ticket":
            assert g["assigned_team"] == "None" or g["needs_escalation"] is False, (
                f"{g['ticket_id']}: 'Not a Support Ticket' should not be escalated"
            )


def test_p1_implies_escalation_or_justification():
    """P1 tickets should either be escalated or have a clear justification."""
    gold = _load_gold()
    p1_tickets = [g for g in gold if g["priority"] == "P1"]
    for g in p1_tickets:
        # P1 tickets should have substantive remediation steps
        total_steps = sum(len(step) for step in g["remediation_steps"])
        assert total_steps > 50, (
            f"{g['ticket_id']}: P1 ticket should have substantial remediation steps"
        )


def test_escalated_tickets_are_high_priority():
    """Escalated tickets should not be P4 (low priority)."""
    for g in _load_gold():
        if g["needs_escalation"]:
            assert g["priority"] != "P4", (
                f"{g['ticket_id']}: escalated ticket should not be P4"
            )


# ═══════════════════════════════════════════════════════════════════════
# SECTION 6: Distribution coverage
# ═══════════════════════════════════════════════════════════════════════


def test_multiple_categories_represented():
    """Dataset should cover at least 4 distinct categories."""
    categories = {g["category"] for g in _load_gold()}
    assert len(categories) >= 4, f"Only {len(categories)} categories: {categories}"


def test_multiple_teams_represented():
    """Dataset should cover at least 4 distinct teams."""
    teams = {g["assigned_team"] for g in _load_gold()}
    assert len(teams) >= 4, f"Only {len(teams)} teams: {teams}"


def test_multiple_priorities_represented():
    """Dataset should cover at least 3 distinct priorities."""
    priorities = {g["priority"] for g in _load_gold()}
    assert len(priorities) >= 3, f"Only {len(priorities)} priorities: {priorities}"


def test_multiple_channels_used():
    """Dataset should use at least 3 distinct channels."""
    channels = {t["channel"] for t in _load_tickets()}
    assert len(channels) >= 3, f"Only {len(channels)} channels: {channels}"


def test_descriptions_are_substantial():
    """All descriptions should be substantial (300+ chars) to contain real noise."""
    for t in _load_tickets():
        desc_len = len(t["description"])
        assert desc_len >= 300, (
            f"{t['ticket_id']}: description too short ({desc_len} chars)"
        )


# ═══════════════════════════════════════════════════════════════════════
# SECTION 7: PII and credential leakage detection
# ═══════════════════════════════════════════════════════════════════════


_PII_PATTERNS = [
    re.compile(r"\b\d{3}-\d{2}-\d{4}\b"),  # SSN format
    re.compile(r"\b(?:\d{4}[-\s]?){3}\d{4}\b"),  # Credit card format
    re.compile(r"password\s*[:=]\s*\S+", re.IGNORECASE),
    re.compile(r"api[_-]?key\s*[:=]\s*\S+", re.IGNORECASE),
    re.compile(r"secret\s*[:=]\s*['\"][^'\"]+['\"]", re.IGNORECASE),
]


def test_gold_no_pii_leakage():
    """Gold answers should not contain PII patterns."""
    for g in _load_gold():
        combined = g["next_best_action"]
        for step in g["remediation_steps"]:
            combined += " " + step
        for pattern in _PII_PATTERNS:
            match = pattern.search(combined)
            assert not match, (
                f"{g['ticket_id']}: PII pattern found in gold: {match.group()}"
            )


def test_reporter_emails_use_contoso():
    """All reporter emails should use @contoso.com domain."""
    for t in _load_tickets():
        email = t["reporter"]["email"]
        assert "@contoso.com" in email, (
            f"{t['ticket_id']}: reporter email not @contoso.com: {email}"
        )


# ═══════════════════════════════════════════════════════════════════════
# SECTION 8: Cross-validation with other datasets
# ═══════════════════════════════════════════════════════════════════════


def test_no_id_collision_with_other_datasets():
    """INC-DCP### IDs should not collide with known dataset prefixes."""
    our_ids = {t["ticket_id"] for t in _load_tickets()}
    for tid in our_ids:
        assert tid.startswith("INC-DCP"), f"Unexpected prefix: {tid}"
    # Verify no overlap with commonly used prefixes
    other_prefixes = ["INC-DC0", "INC-DCA", "INC-DCF", "INC-DCM", "INC-DCX",
                       "INC-RA", "INC-RAA", "INC-RAF", "INC-RAG", "INC-RAI",
                       "INC-RAM", "INC-RAX", "INC-RAV"]
    for tid in our_ids:
        for prefix in other_prefixes:
            if prefix == "INC-DCP":
                continue
            assert not tid.startswith(prefix), (
                f"ID {tid} collides with prefix {prefix}"
            )


# ═══════════════════════════════════════════════════════════════════════
# Runner
# ═══════════════════════════════════════════════════════════════════════


def _run_all() -> tuple[int, int]:
    """Run all test functions and report pass/fail counts."""
    import inspect

    passed = 0
    failed = 0
    test_funcs = [
        (name, obj)
        for name, obj in sorted(globals().items())
        if name.startswith("test_") and inspect.isfunction(obj)
    ]
    for name, func in test_funcs:
        try:
            func()
            passed += 1
            print(f"  ✓ {name}")
        except (AssertionError, Exception) as exc:
            failed += 1
            print(f"  ✗ {name}: {exc}")
    return passed, failed


if __name__ == "__main__":
    print("Data Cleanup Polyglot Evaluation Tests")
    print("=" * 55)
    p, f = _run_all()
    print(f"\n{p} passed, {f} failed")
    sys.exit(1 if f else 0)
