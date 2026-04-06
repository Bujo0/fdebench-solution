#!/usr/bin/env python3
"""Cross-dataset consistency and generator validation tests.

Validates relationships between all eval datasets, ensures no ID collisions,
verifies the scenario generator produces valid output, and checks statistical
properties across the combined eval corpus.

Test categories:
  1. Cross-dataset ID uniqueness — no ticket_id collisions between datasets
  2. Schema consistency — all datasets follow the same schema
  3. Value vocabulary consistency — all datasets use the same constrained values
  4. Generator scenario validation — all scenario definitions are well-formed
  5. Statistical balance — combined corpus covers all dimensions adequately

Usage:
    cd docs/eval
    python test_cross_dataset.py

    # Or with pytest:
    uv run pytest test_cross_dataset.py -v
"""

import json
import sys
from collections import Counter
from pathlib import Path

sys.path.insert(0, ".")  # noqa: TID251

from run_eval import CATEGORIES
from run_eval import TEAMS

# ── Load all datasets ────────────────────────────────────────────────

_DATA_DIR = Path(__file__).resolve().parent.parent / "data" / "tickets"

_DATASETS: dict[str, tuple[list[dict], list[dict] | None]] = {}


def _load(name: str, has_gold: bool = True) -> None:
    tickets_path = _DATA_DIR / f"{name}.json"
    if not tickets_path.exists():
        return
    tickets = json.loads(tickets_path.read_text())
    gold = None
    if has_gold:
        gold_path = _DATA_DIR / f"{name}_gold.json"
        if gold_path.exists():
            gold = json.loads(gold_path.read_text())
    _DATASETS[name] = (tickets, gold)


_load("sample", has_gold=True)
_load("data_cleanup_eval", has_gold=True)
_load("responsible_ai_eval", has_gold=True)
_load("eval_data_cleanup", has_gold=True)
_load("eval_responsible_ai", has_gold=True)
_load("public_eval", has_gold=False)

_VALID_CATEGORIES = set(CATEGORIES)
_VALID_TEAMS = set(TEAMS)
_VALID_PRIORITIES = {"P1", "P2", "P3", "P4"}
_VALID_CHANNELS = {"email", "chat", "portal", "phone"}
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
_REQUIRED_TICKET_FIELDS = {"ticket_id", "subject", "description", "reporter", "created_at", "channel"}
_REQUIRED_GOLD_FIELDS = {
    "ticket_id", "category", "priority", "assigned_team",
    "needs_escalation", "missing_information", "next_best_action", "remediation_steps",
}


# ── 1. Cross-dataset ID uniqueness ──────────────────────────────────


def test_no_id_collisions_between_datasets():
    """Ticket IDs should be unique across all datasets."""
    seen: dict[str, str] = {}
    collisions: list[str] = []
    for name, (tickets, _gold) in _DATASETS.items():
        for t in tickets:
            tid = t["ticket_id"]
            if tid in seen:
                collisions.append(f"{tid} in both '{seen[tid]}' and '{name}'")
            else:
                seen[tid] = name
    assert not collisions, f"ID collisions found: {collisions[:10]}"


def test_sample_has_25_tickets():
    if "sample" not in _DATASETS:
        return
    tickets, gold = _DATASETS["sample"]
    assert len(tickets) == 25
    assert gold is not None
    assert len(gold) == 25


def test_handcrafted_dc_has_15_tickets():
    if "data_cleanup_eval" not in _DATASETS:
        return
    tickets, gold = _DATASETS["data_cleanup_eval"]
    assert len(tickets) == 15
    assert gold is not None
    assert len(gold) == 15


def test_handcrafted_rai_has_15_tickets():
    if "responsible_ai_eval" not in _DATASETS:
        return
    tickets, gold = _DATASETS["responsible_ai_eval"]
    assert len(tickets) == 15
    assert gold is not None
    assert len(gold) == 15


def test_public_eval_has_50_tickets():
    if "public_eval" not in _DATASETS:
        return
    tickets, _gold = _DATASETS["public_eval"]
    assert len(tickets) == 50


# ── 2. Schema consistency ────────────────────────────────────────────


def test_all_tickets_have_required_fields():
    """Every ticket in every dataset should have the same required fields."""
    failures = []
    for name, (tickets, _gold) in _DATASETS.items():
        for t in tickets:
            missing = _REQUIRED_TICKET_FIELDS - set(t.keys())
            if missing:
                failures.append(f"{name}/{t.get('ticket_id', '?')}: missing {missing}")
    assert not failures, f"Schema violations: {failures[:10]}"


def test_all_gold_answers_have_required_fields():
    """Every gold answer should have the same required fields."""
    failures = []
    for name, (_tickets, gold) in _DATASETS.items():
        if gold is None:
            continue
        for g in gold:
            missing = _REQUIRED_GOLD_FIELDS - set(g.keys())
            if missing:
                failures.append(f"{name}/{g.get('ticket_id', '?')}: missing {missing}")
    assert not failures, f"Schema violations: {failures[:10]}"


def test_all_reporters_have_name_email_department():
    failures = []
    for name, (tickets, _gold) in _DATASETS.items():
        for t in tickets:
            reporter = t.get("reporter", {})
            for field in ("name", "email", "department"):
                if field not in reporter:
                    failures.append(f"{name}/{t['ticket_id']}: reporter missing {field}")
    assert not failures, f"Reporter schema violations: {failures[:10]}"


# ── 3. Value vocabulary consistency ──────────────────────────────────


def test_all_gold_categories_valid():
    failures = []
    for name, (_tickets, gold) in _DATASETS.items():
        if gold is None:
            continue
        for g in gold:
            if g["category"] not in _VALID_CATEGORIES:
                failures.append(f"{name}/{g['ticket_id']}: '{g['category']}'")
    assert not failures, f"Invalid categories: {failures[:10]}"


def test_all_gold_teams_valid():
    failures = []
    for name, (_tickets, gold) in _DATASETS.items():
        if gold is None:
            continue
        for g in gold:
            if g["assigned_team"] not in _VALID_TEAMS:
                failures.append(f"{name}/{g['ticket_id']}: '{g['assigned_team']}'")
    assert not failures, f"Invalid teams: {failures[:10]}"


def test_all_gold_priorities_valid():
    failures = []
    for name, (_tickets, gold) in _DATASETS.items():
        if gold is None:
            continue
        for g in gold:
            if g["priority"] not in _VALID_PRIORITIES:
                failures.append(f"{name}/{g['ticket_id']}: '{g['priority']}'")
    assert not failures, f"Invalid priorities: {failures[:10]}"


def test_all_channels_valid():
    failures = []
    for name, (tickets, _gold) in _DATASETS.items():
        for t in tickets:
            if t["channel"] not in _VALID_CHANNELS:
                failures.append(f"{name}/{t['ticket_id']}: '{t['channel']}'")
    assert not failures, f"Invalid channels: {failures[:10]}"


def test_all_gold_missing_info_valid():
    failures = []
    for name, (_tickets, gold) in _DATASETS.items():
        if gold is None:
            continue
        for g in gold:
            for item in g["missing_information"]:
                if item not in _VALID_MISSING_INFO:
                    failures.append(f"{name}/{g['ticket_id']}: '{item}'")
    assert not failures, f"Invalid missing_info values: {failures[:10]}"


def test_all_gold_escalation_boolean():
    failures = []
    for name, (_tickets, gold) in _DATASETS.items():
        if gold is None:
            continue
        for g in gold:
            if not isinstance(g["needs_escalation"], bool):
                failures.append(f"{name}/{g['ticket_id']}: {type(g['needs_escalation'])}")
    assert not failures, f"Non-boolean escalation: {failures[:10]}"


# ── 4. Generator scenario validation ────────────────────────────────


def test_generator_scenarios_have_unique_ids():
    """All scenario_ids in the generator should be unique."""
    scenarios_dir = Path(__file__).resolve().parent / "generator" / "scenarios"
    if not scenarios_dir.exists():
        return

    all_ids: list[str] = []
    for py_file in sorted(scenarios_dir.glob("*.py")):
        if py_file.name.startswith("_"):
            continue
        content = py_file.read_text()
        import re
        ids = re.findall(r'scenario_id="([^"]+)"', content)
        all_ids.extend(ids)

    dupes = [sid for sid in all_ids if all_ids.count(sid) > 1]
    assert not dupes, f"Duplicate scenario IDs: {set(dupes)}"


def test_generator_scenarios_use_valid_categories():
    """All scenario definitions should use valid categories."""
    scenarios_dir = Path(__file__).resolve().parent / "generator" / "scenarios"
    if not scenarios_dir.exists():
        return

    import re
    failures = []
    for py_file in sorted(scenarios_dir.glob("*.py")):
        if py_file.name.startswith("_"):
            continue
        content = py_file.read_text()
        categories = re.findall(r'category="([^"]+)"', content)
        for cat in categories:
            if cat not in _VALID_CATEGORIES:
                failures.append(f"{py_file.name}: '{cat}'")
    assert not failures, f"Invalid categories in generator: {failures[:10]}"


def test_generator_scenarios_use_valid_teams():
    """All scenario definitions should use valid team names."""
    scenarios_dir = Path(__file__).resolve().parent / "generator" / "scenarios"
    if not scenarios_dir.exists():
        return

    import re
    failures = []
    for py_file in sorted(scenarios_dir.glob("*.py")):
        if py_file.name.startswith("_"):
            continue
        content = py_file.read_text()
        teams = re.findall(r'assigned_team="([^"]+)"', content)
        for team in teams:
            if team not in _VALID_TEAMS:
                failures.append(f"{py_file.name}: '{team}'")
    assert not failures, f"Invalid teams in generator: {failures[:10]}"


def test_generator_scenarios_use_valid_priorities():
    scenarios_dir = Path(__file__).resolve().parent / "generator" / "scenarios"
    if not scenarios_dir.exists():
        return

    import re
    failures = []
    for py_file in sorted(scenarios_dir.glob("*.py")):
        if py_file.name.startswith("_"):
            continue
        content = py_file.read_text()
        priorities = re.findall(r'priority="([^"]+)"', content)
        for pri in priorities:
            if pri not in _VALID_PRIORITIES:
                failures.append(f"{py_file.name}: '{pri}'")
    assert not failures, f"Invalid priorities in generator: {failures[:10]}"


# ── 5. Statistical balance (combined gold corpus) ────────────────────


def _combined_golds() -> list[dict]:
    """Collect all gold answers across all scored datasets."""
    golds: list[dict] = []
    for _name, (_tickets, gold) in _DATASETS.items():
        if gold is not None:
            golds.extend(gold)
    return golds


def test_combined_corpus_covers_all_categories():
    golds = _combined_golds()
    cats = {g["category"] for g in golds}
    assert cats == _VALID_CATEGORIES, f"Missing categories: {_VALID_CATEGORIES - cats}"


def test_combined_corpus_covers_all_teams():
    golds = _combined_golds()
    teams = {g["assigned_team"] for g in golds}
    expected = _VALID_TEAMS | {"None"}
    assert teams == expected, f"Missing teams: {expected - teams}"


def test_combined_corpus_covers_all_priorities():
    golds = _combined_golds()
    pris = {g["priority"] for g in golds}
    assert pris == _VALID_PRIORITIES, f"Missing priorities: {_VALID_PRIORITIES - pris}"


def test_combined_corpus_no_single_category_dominates():
    """No single category should exceed 40% of the combined scored corpus."""
    golds = _combined_golds()
    if not golds:
        return
    counts = Counter(g["category"] for g in golds)
    for cat, count in counts.items():
        ratio = count / len(golds)
        assert ratio < 0.40, (
            f"Category '{cat}' dominates at {ratio:.0%} ({count}/{len(golds)})"
        )


def test_combined_corpus_has_both_escalation_values():
    golds = _combined_golds()
    vals = {g["needs_escalation"] for g in golds}
    assert True in vals and False in vals


def test_combined_corpus_uses_most_missing_info_values():
    """At least 12 of 16 missing_information values should appear."""
    golds = _combined_golds()
    all_values = set()
    for g in golds:
        all_values.update(g["missing_information"])
    assert len(all_values) >= 12, (
        f"Only {len(all_values)}/16 missing_information values used: "
        f"missing {_VALID_MISSING_INFO - all_values}"
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
