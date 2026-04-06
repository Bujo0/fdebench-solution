#!/usr/bin/env python3
"""Validation tests for all evaluation datasets.

Ensures every ticket dataset and its gold labels:
  - Conform to the input/output JSON schemas (required fields, types, enums)
  - Have matching ticket IDs between input and gold
  - Use only valid enum values from the closed label sets
  - Have no duplicate ticket IDs
"""

import json
import re
import sys
from pathlib import Path

# ── Paths ─────────────────────────────────────────────────────────────

_DOCS = Path(__file__).resolve().parent.parent
_DATA = _DOCS / "data" / "tickets"

# All dataset pairs: (tickets_file, gold_file)
_DATASETS: list[tuple[str, str]] = [
    ("sample.json", "sample_gold.json"),
    ("data_cleanup_eval.json", "data_cleanup_eval_gold.json"),
    ("responsible_ai_eval.json", "responsible_ai_eval_gold.json"),
]

# ── Closed label sets (must match run_eval.py) ────────────────────────

CATEGORIES = {
    "Access & Authentication",
    "Hardware & Peripherals",
    "Network & Connectivity",
    "Software & Applications",
    "Security & Compliance",
    "Data & Storage",
    "General Inquiry",
    "Not a Support Ticket",
}

TEAMS = {
    "Identity & Access Management",
    "Endpoint Engineering",
    "Network Operations",
    "Enterprise Applications",
    "Security Operations",
    "Data Platform",
    "None",
}

PRIORITIES = {"P1", "P2", "P3", "P4"}

CHANNELS = {"email", "chat", "portal", "phone"}

MISSING_INFO_VOCAB = {
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

_TICKET_ID_PATTERN = re.compile(r"^INC-[0-9]+$")

# ── Helpers ───────────────────────────────────────────────────────────


def _load(name: str) -> list[dict]:
    path = _DATA / name
    assert path.exists(), f"File not found: {path}"
    return json.loads(path.read_text(encoding="utf-8"))


# ── Input ticket validation ──────────────────────────────────────────


def _validate_ticket(ticket: dict, file_name: str) -> list[str]:
    """Return a list of validation errors for a single input ticket."""
    errors: list[str] = []
    tid = ticket.get("ticket_id", "<missing>")
    prefix = f"{file_name} / {tid}"

    # Required fields
    for field in ("ticket_id", "subject", "description", "reporter", "created_at", "channel"):
        if field not in ticket:
            errors.append(f"{prefix}: missing required field '{field}'")

    # ticket_id format
    if "ticket_id" in ticket and not _TICKET_ID_PATTERN.match(str(ticket["ticket_id"])):
        errors.append(f"{prefix}: ticket_id does not match pattern ^INC-[0-9]+$")

    # channel enum
    if "channel" in ticket and ticket["channel"] not in CHANNELS:
        errors.append(f"{prefix}: invalid channel '{ticket['channel']}'")

    # reporter structure
    reporter = ticket.get("reporter", {})
    for field in ("name", "email", "department"):
        if field not in reporter:
            errors.append(f"{prefix}: reporter missing field '{field}'")

    # reporter email format (basic check)
    email = reporter.get("email", "")
    if email and "@" not in email:
        errors.append(f"{prefix}: reporter email '{email}' missing '@'")

    # attachments type
    attachments = ticket.get("attachments")
    if attachments is not None and not isinstance(attachments, list):
        errors.append(f"{prefix}: attachments must be a list, got {type(attachments).__name__}")

    # created_at basic ISO format check
    created = ticket.get("created_at", "")
    if created and not re.match(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}", created):
        errors.append(f"{prefix}: created_at does not look like ISO 8601")

    return errors


# ── Gold label validation ─────────────────────────────────────────────


def _validate_gold(gold: dict, file_name: str) -> list[str]:
    """Return a list of validation errors for a single gold label."""
    errors: list[str] = []
    tid = gold.get("ticket_id", "<missing>")
    prefix = f"{file_name} / {tid}"

    # Required fields
    for field in (
        "ticket_id",
        "category",
        "priority",
        "assigned_team",
        "needs_escalation",
        "missing_information",
        "next_best_action",
        "remediation_steps",
    ):
        if field not in gold:
            errors.append(f"{prefix}: missing required field '{field}'")

    # Enum validations
    if "category" in gold and gold["category"] not in CATEGORIES:
        errors.append(f"{prefix}: invalid category '{gold['category']}'")

    if "priority" in gold and gold["priority"] not in PRIORITIES:
        errors.append(f"{prefix}: invalid priority '{gold['priority']}'")

    if "assigned_team" in gold and gold["assigned_team"] not in TEAMS:
        errors.append(f"{prefix}: invalid assigned_team '{gold['assigned_team']}'")

    # needs_escalation must be bool
    if "needs_escalation" in gold and not isinstance(gold["needs_escalation"], bool):
        errors.append(f"{prefix}: needs_escalation must be bool, got {type(gold['needs_escalation']).__name__}")

    # missing_information must be list of valid vocab
    mi = gold.get("missing_information")
    if mi is not None:
        if not isinstance(mi, list):
            errors.append(f"{prefix}: missing_information must be a list")
        else:
            for item in mi:
                if item not in MISSING_INFO_VOCAB:
                    errors.append(f"{prefix}: invalid missing_information item '{item}'")

    # remediation_steps must be non-empty list of strings
    steps = gold.get("remediation_steps")
    if steps is not None:
        if not isinstance(steps, list):
            errors.append(f"{prefix}: remediation_steps must be a list")
        elif len(steps) == 0:
            errors.append(f"{prefix}: remediation_steps should not be empty")
        else:
            for i, step in enumerate(steps):
                if not isinstance(step, str):
                    errors.append(f"{prefix}: remediation_steps[{i}] must be a string")

    # next_best_action must be a non-empty string
    nba = gold.get("next_best_action")
    if nba is not None and (not isinstance(nba, str) or not nba.strip()):
        errors.append(f"{prefix}: next_best_action must be a non-empty string")

    return errors


# ── Tests ─────────────────────────────────────────────────────────────


def test_all_datasets_exist():
    """All expected dataset files exist on disk."""
    for tickets_file, gold_file in _DATASETS:
        assert (_DATA / tickets_file).exists(), f"Missing: {tickets_file}"
        assert (_DATA / gold_file).exists(), f"Missing: {gold_file}"


def test_datasets_are_valid_json():
    """All dataset files parse as valid JSON arrays."""
    for tickets_file, gold_file in _DATASETS:
        tickets = _load(tickets_file)
        golds = _load(gold_file)
        assert isinstance(tickets, list), f"{tickets_file} is not a JSON array"
        assert isinstance(golds, list), f"{gold_file} is not a JSON array"


def test_no_duplicate_ticket_ids():
    """No dataset contains duplicate ticket IDs."""
    for tickets_file, _ in _DATASETS:
        tickets = _load(tickets_file)
        ids = [t["ticket_id"] for t in tickets]
        assert len(ids) == len(set(ids)), (
            f"{tickets_file} has duplicate ticket IDs: {[x for x in ids if ids.count(x) > 1]}"
        )


def test_ticket_gold_id_alignment():
    """Every ticket has a matching gold label and vice versa."""
    for tickets_file, gold_file in _DATASETS:
        tickets = _load(tickets_file)
        golds = _load(gold_file)
        ticket_ids = {t["ticket_id"] for t in tickets}
        gold_ids = {g["ticket_id"] for g in golds}
        assert ticket_ids == gold_ids, (
            f"{tickets_file}/{gold_file} ID mismatch. "
            f"In tickets but not gold: {ticket_ids - gold_ids}. "
            f"In gold but not tickets: {gold_ids - ticket_ids}"
        )


def test_ticket_count_matches():
    """Ticket count equals gold count for each dataset pair."""
    for tickets_file, gold_file in _DATASETS:
        tickets = _load(tickets_file)
        golds = _load(gold_file)
        assert len(tickets) == len(golds), f"{tickets_file}: {len(tickets)} tickets but {gold_file}: {len(golds)} golds"


def test_all_tickets_valid_schema():
    """Every ticket in every dataset conforms to the input schema."""
    all_errors: list[str] = []
    for tickets_file, _ in _DATASETS:
        tickets = _load(tickets_file)
        for ticket in tickets:
            all_errors.extend(_validate_ticket(ticket, tickets_file))
    assert not all_errors, "Input ticket validation errors:\n  " + "\n  ".join(all_errors)


def test_all_golds_valid_schema():
    """Every gold label in every dataset conforms to the output schema."""
    all_errors: list[str] = []
    for _, gold_file in _DATASETS:
        golds = _load(gold_file)
        for gold in golds:
            all_errors.extend(_validate_gold(gold, gold_file))
    assert not all_errors, "Gold label validation errors:\n  " + "\n  ".join(all_errors)


def test_no_id_collisions_across_datasets():
    """Ticket IDs are unique across all datasets (no cross-dataset collisions)."""
    all_ids: list[str] = []
    for tickets_file, _ in _DATASETS:
        tickets = _load(tickets_file)
        all_ids.extend(t["ticket_id"] for t in tickets)
    assert len(all_ids) == len(set(all_ids)), (
        f"Cross-dataset ID collision: {[x for x in all_ids if all_ids.count(x) > 1]}"
    )


def test_data_cleanup_dataset_size():
    """Data cleanup dataset has at least 15 tickets."""
    tickets = _load("data_cleanup_eval.json")
    assert len(tickets) >= 15, f"Expected >= 15 data cleanup tickets, got {len(tickets)}"


def test_responsible_ai_dataset_size():
    """Responsible AI dataset has at least 15 tickets."""
    tickets = _load("responsible_ai_eval.json")
    assert len(tickets) >= 15, f"Expected >= 15 responsible AI tickets, got {len(tickets)}"


def test_gold_categories_cover_multiple_values():
    """Gold labels collectively use multiple distinct category values (not all the same)."""
    for _, gold_file in _DATASETS:
        golds = _load(gold_file)
        categories = {g["category"] for g in golds}
        assert len(categories) >= 2, f"{gold_file}: all tickets have the same category '{next(iter(categories))}'"


def test_gold_priorities_cover_multiple_values():
    """Gold labels collectively use multiple distinct priority values."""
    for _, gold_file in _DATASETS:
        golds = _load(gold_file)
        priorities = {g["priority"] for g in golds}
        assert len(priorities) >= 2, f"{gold_file}: all tickets have the same priority '{next(iter(priorities))}'"


def test_gold_teams_cover_multiple_values():
    """Gold labels collectively use multiple distinct team values."""
    for _, gold_file in _DATASETS:
        golds = _load(gold_file)
        teams = {g["assigned_team"] for g in golds}
        assert len(teams) >= 2, f"{gold_file}: all tickets have the same team '{next(iter(teams))}'"


def test_gold_escalation_has_both_values():
    """Gold labels include both True and False escalation values in each dataset."""
    for _, gold_file in _DATASETS:
        golds = _load(gold_file)
        escalation_values = {g["needs_escalation"] for g in golds}
        assert True in escalation_values, f"{gold_file}: no tickets have needs_escalation=True"
        assert False in escalation_values, f"{gold_file}: no tickets have needs_escalation=False"


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
