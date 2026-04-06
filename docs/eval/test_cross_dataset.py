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
import re
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

# Scoring-oriented 15-ticket sets: loaded separately for validation but
# excluded from cross-dataset ID collision checks because they are subsets
# of the generated eval datasets (eval_data_cleanup / eval_responsible_ai).
_SCORING_DATASETS: dict[str, tuple[list[dict], list[dict] | None]] = {}


def _load_scoring(name: str) -> None:
    tickets_path = _DATA_DIR / f"{name}.json"
    if not tickets_path.exists():
        return
    tickets = json.loads(tickets_path.read_text())
    gold_path = _DATA_DIR / f"{name}_gold.json"
    gold = json.loads(gold_path.read_text()) if gold_path.exists() else None
    _SCORING_DATASETS[name] = (tickets, gold)


_load_scoring("data_cleanup")
_load_scoring("responsible_ai")

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


def test_handcrafted_rai_has_25_tickets():
    if "responsible_ai_eval" not in _DATASETS:
        return
    tickets, gold = _DATASETS["responsible_ai_eval"]
    assert len(tickets) == 25
    assert gold is not None
    assert len(gold) == 25


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
        ids = re.findall(r'scenario_id="([^"]+)"', content)
        all_ids.extend(ids)

    dupes = [sid for sid in all_ids if all_ids.count(sid) > 1]
    assert not dupes, f"Duplicate scenario IDs: {set(dupes)}"


def test_generator_scenarios_use_valid_categories():
    """All scenario definitions should use valid categories."""
    scenarios_dir = Path(__file__).resolve().parent / "generator" / "scenarios"
    if not scenarios_dir.exists():
        return

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
    """Collect all gold answers across all scored datasets (excluding scoring subsets to avoid double counting)."""
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


# ── 6. Scoring-oriented dataset validation ───────────────────────────


def test_scoring_data_cleanup_has_15_tickets():
    if "data_cleanup" not in _SCORING_DATASETS:
        return
    tickets, gold = _SCORING_DATASETS["data_cleanup"]
    assert len(tickets) == 15
    assert gold is not None
    assert len(gold) == 15


def test_scoring_responsible_ai_has_15_tickets():
    if "responsible_ai" not in _SCORING_DATASETS:
        return
    tickets, gold = _SCORING_DATASETS["responsible_ai"]
    assert len(tickets) == 15
    assert gold is not None
    assert len(gold) == 15


def test_scoring_datasets_are_subsets_of_generated():
    """Scoring-oriented INC-5xxx/INC-6xxx tickets should be subsets of generated datasets."""
    pairs = [
        ("data_cleanup", "eval_data_cleanup"),
        ("responsible_ai", "eval_responsible_ai"),
    ]
    for scoring_name, generated_name in pairs:
        if scoring_name not in _SCORING_DATASETS or generated_name not in _DATASETS:
            continue
        scoring_ids = {t["ticket_id"] for t in _SCORING_DATASETS[scoring_name][0]}
        generated_ids = {t["ticket_id"] for t in _DATASETS[generated_name][0]}
        missing = scoring_ids - generated_ids
        assert not missing, (
            f"Scoring set '{scoring_name}' has IDs not in generated set '{generated_name}': "
            f"{missing}"
        )


# ── 7. Per-dataset distribution analysis ─────────────────────────────


def test_each_dataset_has_multiple_categories():
    """Every scored dataset should cover at least 3 categories."""
    for name, (_tickets, gold) in _DATASETS.items():
        if gold is None:
            continue
        cats = {g["category"] for g in gold}
        assert len(cats) >= 3, (
            f"Dataset '{name}' has only {len(cats)} categories: {cats}"
        )


def test_each_dataset_has_multiple_priorities():
    """Every scored dataset should cover at least 2 priority levels."""
    for name, (_tickets, gold) in _DATASETS.items():
        if gold is None:
            continue
        pris = {g["priority"] for g in gold}
        assert len(pris) >= 2, (
            f"Dataset '{name}' has only {len(pris)} priorities: {pris}"
        )


def test_each_dataset_has_both_escalation_values():
    """Every scored dataset should have both escalated and non-escalated tickets."""
    for name, (_tickets, gold) in _DATASETS.items():
        if gold is None:
            continue
        vals = {g["needs_escalation"] for g in gold}
        assert True in vals and False in vals, (
            f"Dataset '{name}' doesn't have both escalation values"
        )


# ── 8. Combined corpus reporter diversity ────────────────────────────


def test_combined_corpus_has_diverse_reporters():
    """Combined corpus should have many unique reporters (diverse emails)."""
    all_emails: set[str] = set()
    for _name, (tickets, _gold) in _DATASETS.items():
        for t in tickets:
            email = t.get("reporter", {}).get("email", "")
            if email:
                all_emails.add(email.lower())
    assert len(all_emails) >= 10, (
        f"Only {len(all_emails)} unique reporter emails across all datasets"
    )


def test_combined_corpus_has_diverse_departments():
    """Combined corpus should reference multiple departments."""
    all_depts: set[str] = set()
    for _name, (tickets, _gold) in _DATASETS.items():
        for t in tickets:
            dept = t.get("reporter", {}).get("department", "")
            if dept:
                all_depts.add(dept.lower())
    assert len(all_depts) >= 5, (
        f"Only {len(all_depts)} unique departments across all datasets"
    )


# ── 9. Description length variety across datasets ───────────────────


def test_combined_corpus_description_length_range():
    """Combined corpus should have descriptions ranging from very short to very long."""
    all_lengths: list[int] = []
    for _name, (tickets, _gold) in _DATASETS.items():
        for t in tickets:
            all_lengths.append(len(t.get("description", "")))

    if not all_lengths:
        return

    min_len = min(all_lengths)
    max_len = max(all_lengths)
    assert min_len <= 50, f"Shortest description is {min_len} chars — expected ≤50"
    assert max_len >= 2000, f"Longest description is {max_len} chars — expected ≥2000"


def test_combined_corpus_multiple_channels():
    """Combined corpus should use at least 3 channels."""
    all_channels: set[str] = set()
    for _name, (tickets, _gold) in _DATASETS.items():
        for t in tickets:
            all_channels.add(t.get("channel", ""))
    assert len(all_channels) >= 3, (
        f"Only {len(all_channels)} channels: {all_channels}"
    )


# ── 10. Total corpus sanity checks ──────────────────────────────────


def test_total_scored_ticket_count():
    """Total scored tickets across all datasets should be at least 100."""
    total = sum(
        len(tickets) for _name, (tickets, gold) in _DATASETS.items()
        if gold is not None
    )
    assert total >= 100, f"Only {total} scored tickets total — expected ≥100"


def test_no_gold_answer_content_overlap():
    """Independent datasets should not have identical gold answers."""
    seen_hashes: dict[str, str] = {}
    collisions: list[str] = []
    for name, (_tickets, gold) in _DATASETS.items():
        if gold is None:
            continue
        for g in gold:
            fp = f"{g['category']}|{g['priority']}|{g['assigned_team']}|{g['needs_escalation']}"
            key = f"{g['ticket_id']}:{fp}"
            if key in seen_hashes and seen_hashes[key] != name:
                collisions.append(f"{g['ticket_id']} duplicated in '{seen_hashes[key]}' and '{name}'")
            seen_hashes[key] = name
    assert not collisions, f"Content overlap found: {collisions[:5]}"


def test_all_datasets_have_valid_ticket_id_format():
    """Every ticket_id should follow the INC-XXX format."""
    failures = []
    for name, (tickets, _gold) in _DATASETS.items():
        for t in tickets:
            tid = t.get("ticket_id", "")
            if not re.match(r"^INC-[A-Z0-9]+$", tid):
                failures.append(f"{name}/{tid}")
    assert not failures, f"Invalid ticket_id format: {failures[:10]}"


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
