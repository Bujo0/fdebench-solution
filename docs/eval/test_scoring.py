#!/usr/bin/env python3
"""Unit tests for the scoring functions in run_eval.py.

Test structure mirrors the scoring pipeline:
  1. Per-dimension scorers (category, priority, routing, missing_info, escalation)
  2. Boolean coercion helper (_coerce_bool)
  3. Submission-level aggregate metrics (macro_f1, binary_f1)
  4. Per-signal composite (score_signal)
  5. Full submission aggregate (score_submission)
"""

import importlib.util
import sys
from pathlib import Path

import pytest

# Load run_eval from the same directory as this script, using importlib
# to avoid sys.path manipulation (banned by project lint rules).
_EVAL_PATH = Path(__file__).resolve().parent / "run_eval.py"
_spec = importlib.util.spec_from_file_location("run_eval", _EVAL_PATH)
_mod = importlib.util.module_from_spec(_spec)
sys.modules["run_eval"] = _mod
_spec.loader.exec_module(_mod)

WEIGHTS = _mod.WEIGHTS
CATEGORIES = _mod.CATEGORIES
TEAMS = _mod.TEAMS
_coerce_bool = _mod._coerce_bool
binary_f1 = _mod.binary_f1
macro_f1 = _mod.macro_f1
score_category = _mod.score_category
score_escalation = _mod.score_escalation
score_missing_info = _mod.score_missing_info
score_priority = _mod.score_priority
score_routing = _mod.score_routing
score_signal = _mod.score_signal
score_submission = _mod.score_submission

# ── Category (multi-class exact match, case-insensitive) ────────────


def test_category_exact():
    assert score_category("Crew Access & Biometrics", "Crew Access & Biometrics") == 1.0


def test_category_case_insensitive():
    assert score_category("crew access & biometrics", "Crew Access & Biometrics") == 1.0


def test_category_mismatch():
    assert score_category("Communications & Navigation", "Crew Access & Biometrics") == 0.0


def test_category_none():
    assert score_category(None, "Crew Access & Biometrics") == 0.0


def test_category_empty():
    assert score_category("", "Crew Access & Biometrics") == 0.0


def test_category_whitespace_trimmed():
    assert score_category("  Crew Access & Biometrics  ", "Crew Access & Biometrics") == 1.0


def test_category_extra_whitespace_collapsed():
    """Extra internal whitespace should be collapsed to match."""
    assert score_category("Crew Access  &  Biometrics", "Crew Access & Biometrics") == 1.0


def test_category_trailing_punctuation_stripped():
    """Trailing punctuation should not prevent a match."""
    assert score_category("Crew Access & Biometrics.", "Crew Access & Biometrics") == 1.0


def test_category_both_empty():
    """Both empty strings should match — absence agrees with absence."""
    assert score_category("", "") == 1.0


def test_category_whitespace_only_vs_real():
    """Whitespace-only candidate should not match a real category."""
    assert score_category("   ", "Communications & Navigation") == 0.0


@pytest.mark.parametrize("category", CATEGORIES)
def test_category_exact_all_labels(category):
    """Every category in the closed label set should match itself."""
    assert score_category(category, category) == 1.0


@pytest.mark.parametrize("category", CATEGORIES)
def test_category_case_insensitive_all_labels(category):
    """Every category should match its lowercased form."""
    assert score_category(category.lower(), category) == 1.0


def test_categories_label_set_completeness():
    """Guard against accidental additions or removals in CATEGORIES."""
    expected = {
        "Crew Access & Biometrics",
        "Hull & Structural Systems",
        "Communications & Navigation",
        "Flight Software & Instruments",
        "Threat Detection & Containment",
        "Telemetry & Data Banks",
        "Mission Briefing Request",
        "Not a Mission Signal",
    }
    assert set(CATEGORIES) == expected
    assert len(CATEGORIES) == 8


def test_teams_label_set_completeness():
    """Guard against accidental additions or removals in TEAMS."""
    expected = {
        "Crew Identity & Airlock Control",
        "Spacecraft Systems Engineering",
        "Deep Space Communications",
        "Mission Software Operations",
        "Threat Response Command",
        "Telemetry & Data Core",
        "None",
    }
    assert set(TEAMS) == expected
    assert len(TEAMS) == 7


# ── Priority (ordinal P1-P4, partial credit for off-by-one only) ────


def test_priority_exact():
    assert score_priority("P1", "P1") == 1.0


def test_priority_all_levels():
    for p in ("P1", "P2", "P3", "P4"):
        assert score_priority(p, p) == 1.0


def test_priority_off_by_1():
    assert score_priority("P2", "P1") == 0.67


def test_priority_off_by_1_symmetric():
    assert score_priority("P1", "P2") == 0.67
    assert score_priority("P3", "P4") == 0.67


def test_priority_off_by_2():
    """Off by 2 levels = 0.0 (no partial credit)."""
    assert score_priority("P3", "P1") == 0.0


def test_priority_off_by_3():
    assert score_priority("P4", "P1") == 0.0


def test_priority_off_by_2_symmetric():
    assert score_priority("P1", "P3") == 0.0


def test_priority_invalid():
    assert score_priority("X", "P1") == 0.0


def test_priority_none():
    assert score_priority(None, "P1") == 0.0


def test_priority_empty():
    assert score_priority("", "P1") == 0.0


def test_priority_case_insensitive():
    assert score_priority("p2", "P2") == 1.0


def test_priority_numeric_string():
    assert score_priority("1", "P1") == 0.0


def test_priority_invalid_gold():
    """Invalid gold label should return 0.0."""
    assert score_priority("P1", "CRITICAL") == 0.0


def test_priority_both_invalid():
    """Both invalid labels should return 0.0."""
    assert score_priority("HIGH", "LOW") == 0.0


# ── Routing (multi-class exact match, case-insensitive) ─────────────


def test_routing_exact():
    assert score_routing("Threat Response Command", "Threat Response Command") == 1.0


def test_routing_case():
    assert score_routing("threat response command", "Threat Response Command") == 1.0


def test_routing_mismatch():
    assert score_routing("Telemetry & Data Core", "Threat Response Command") == 0.0


def test_routing_none_team():
    """'None' is a valid team for non-mission signals."""
    assert score_routing("None", "None") == 1.0


def test_routing_empty():
    assert score_routing("", "Threat Response Command") == 0.0


def test_routing_whitespace_trimmed():
    assert score_routing("  Threat Response Command  ", "Threat Response Command") == 1.0


def test_routing_extra_whitespace_collapsed():
    """Extra internal whitespace should be collapsed to match."""
    assert score_routing("Threat  Response  Command", "Threat Response Command") == 1.0


@pytest.mark.parametrize("team", TEAMS)
def test_routing_exact_all_teams(team):
    """Every team in the closed label set should match itself."""
    assert score_routing(team, team) == 1.0


@pytest.mark.parametrize("team", TEAMS)
def test_routing_case_insensitive_all_teams(team):
    """Every team should match its lowercased form."""
    assert score_routing(team.lower(), team) == 1.0


# ── Escalation (binary exact match) ─────────────────────────────────


def test_escalation_true_true():
    assert score_escalation(True, True) == 1.0


def test_escalation_false_false():
    assert score_escalation(False, False) == 1.0


def test_escalation_mismatch():
    assert score_escalation(True, False) == 0.0


def test_escalation_none():
    assert score_escalation(None, True) == 0.0


# ── Missing info (set F1 over constrained vocabulary) ────────────────


def test_missing_both_empty():
    assert score_missing_info([], []) == 1.0


def test_missing_false_positive():
    assert score_missing_info(["module_specs"], []) == 0.0


def test_missing_false_negative():
    assert score_missing_info([], ["module_specs"]) == 0.0


def test_missing_perfect():
    assert score_missing_info(["module_specs"], ["module_specs"]) == 1.0


def test_missing_perfect_different_order():
    assert score_missing_info(["module_specs", "anomaly_readout"], ["anomaly_readout", "module_specs"]) == 1.0


def test_missing_partial_recall():
    # pred=1 of 2 gold. P=1/1=1.0, R=1/2=0.5, F1=2*1*0.5/1.5=0.667
    f1 = score_missing_info(["module_specs"], ["module_specs", "anomaly_readout"])
    assert abs(f1 - 2 / 3) < 0.01


def test_missing_partial_precision():
    # pred=2, gold=1. P=1/2=0.5, R=1/1=1.0, F1=2*0.5*1/1.5=0.667
    f1 = score_missing_info(["module_specs", "anomaly_readout"], ["module_specs"])
    assert abs(f1 - 2 / 3) < 0.01


def test_missing_partial_overlap():
    # 1 TP, 1 FP, 1 FN → precision=0.5, recall=0.5, F1=0.5
    score = score_missing_info(["anomaly_readout", "module_specs"], ["anomaly_readout", "stardate"])
    assert abs(score - 0.5) < 0.01


def test_missing_no_overlap():
    assert score_missing_info(["anomaly_readout"], ["module_specs"]) == 0.0


def test_missing_case_insensitive():
    assert score_missing_info(["Anomaly_Readout"], ["anomaly_readout"]) == 1.0


def test_missing_duplicates_deduplicated():
    """Candidate sends same item twice — should still score as 1 TP."""
    score = score_missing_info(["anomaly_readout", "anomaly_readout"], ["anomaly_readout"])
    assert score == 1.0


def test_missing_superset_penalizes_precision():
    """Candidate returns all gold items plus extras — precision drops."""
    score = score_missing_info(
        ["anomaly_readout", "module_specs", "sensor_log_or_capture", "stardate"],
        ["anomaly_readout", "module_specs"],
    )
    # 2 TP, 2 FP → precision=0.5, recall=1.0, F1=0.667
    assert 0.6 < score < 0.7


_ALL_MISSING_INFO_VOCAB = [
    "affected_subsystem",
    "anomaly_readout",
    "sequence_to_reproduce",
    "affected_crew",
    "habitat_conditions",
    "stardate",
    "previous_signal_id",
    "crew_contact",
    "module_specs",
    "software_version",
    "sector_coordinates",
    "mission_impact",
    "recurrence_pattern",
    "sensor_log_or_capture",
    "biometric_method",
    "system_configuration",
]


@pytest.mark.parametrize("term", _ALL_MISSING_INFO_VOCAB)
def test_missing_each_vocab_term_matches_itself(term):
    """Every valid missing_information term should match when predicted."""
    assert score_missing_info([term], [term]) == 1.0


def test_missing_full_vocabulary_perfect():
    """All 16 missing_information terms predicted and gold — perfect F1."""
    assert score_missing_info(_ALL_MISSING_INFO_VOCAB, _ALL_MISSING_INFO_VOCAB) == 1.0


def test_missing_full_vocabulary_subset():
    """Predicting half the vocab against full vocab gives partial recall."""
    gold = _ALL_MISSING_INFO_VOCAB
    pred = _ALL_MISSING_INFO_VOCAB[:8]
    score = score_missing_info(pred, gold)
    # 8 TP, 0 FP, 8 FN → P=1.0, R=0.5, F1=0.667
    assert abs(score - 2 / 3) < 0.01


# ── Boolean coercion (_coerce_bool) ─────────────────────────────────


def test_coerce_true_bool():
    assert _coerce_bool(True) is True


def test_coerce_false_bool():
    assert _coerce_bool(False) is False


def test_coerce_string_true():
    assert _coerce_bool("true") is True


def test_coerce_string_false():
    assert _coerce_bool("false") is False


def test_coerce_string_True_capitalized():
    assert _coerce_bool("True") is True


def test_coerce_string_FALSE_uppercase():
    assert _coerce_bool("FALSE") is False


def test_coerce_string_yes():
    assert _coerce_bool("yes") is True


def test_coerce_string_no():
    assert _coerce_bool("no") is False


def test_coerce_string_1():
    assert _coerce_bool("1") is True


def test_coerce_string_0():
    assert _coerce_bool("0") is False


def test_coerce_int_1():
    assert _coerce_bool(1) is True


def test_coerce_int_0():
    assert _coerce_bool(0) is False


def test_coerce_none():
    assert _coerce_bool(None) is False


def test_coerce_empty_string():
    assert _coerce_bool("") is False


def test_coerce_whitespace_true():
    assert _coerce_bool("  true  ") is True


def test_coerce_random_string():
    assert _coerce_bool("maybe") is False


# ── Macro F1 (submission-level multi-class metric) ───────────────────


def test_macro_f1_perfect_two_classes():
    assert macro_f1(["A", "B"], ["A", "B"], ["A", "B"]) == 1.0


def test_macro_f1_all_wrong():
    assert macro_f1(["B", "B"], ["A", "A"], ["A", "B"]) == 0.0


def test_macro_f1_half_correct():
    # Gold: [A, B], Candidate: [A, A]
    # Class A: TP=1, FP=1, FN=0 → P=0.5, R=1.0, F1=0.667
    # Class B: TP=0, FP=0, FN=1 → P=0, R=0, F1=0.0
    # Macro F1 = (0.667 + 0.0) / 2 = 0.333
    score = macro_f1(["A", "A"], ["A", "B"], ["A", "B"])
    assert 0.3 < score < 0.4


def test_macro_f1_majority_class_gaming_penalized():
    """Always predicting majority class should score poorly."""
    golds = ["A"] * 8 + ["B"] * 1 + ["C"] * 1
    candidates = ["A"] * 10
    score = macro_f1(candidates, golds, ["A", "B", "C"])
    assert score < 0.35


def test_macro_f1_case_insensitive():
    assert macro_f1(["a", "b"], ["A", "B"], ["A", "B"]) == 1.0


def test_macro_f1_absent_classes_excluded():
    """Classes with zero TP, FP, and FN are not counted."""
    assert macro_f1(["A", "A"], ["A", "A"], ["A", "B", "C"]) == 1.0


def test_macro_f1_empty():
    assert macro_f1([], [], ["A", "B"]) == 0.0


# ── Binary F1 (submission-level escalation metric) ───────────────────


def test_binary_f1_all_true_positives():
    assert binary_f1([True, True], [True, True]) == 1.0


def test_binary_f1_all_true_negatives():
    """No positive cases anywhere → perfect agreement → 1.0."""
    assert binary_f1([False, False], [False, False]) == 1.0


def test_binary_f1_perfect_mixed():
    assert binary_f1([True, False, True], [True, False, True]) == 1.0


def test_binary_f1_all_false_positives():
    assert binary_f1([True, True], [False, False]) == 0.0


def test_binary_f1_all_false_negatives():
    assert binary_f1([False, False], [True, True]) == 0.0


def test_binary_f1_partial():
    # TP=1, FP=1, FN=1 → P=0.5, R=0.5, F1=0.5
    score = binary_f1([True, True, False], [True, False, True])
    assert abs(score - 0.5) < 0.01


def test_binary_f1_always_false_when_positives_exist():
    """Never escalating when gold has escalations → F1=0."""
    assert binary_f1([False, False, False], [True, True, False]) == 0.0


def test_binary_f1_empty():
    assert binary_f1([], []) == 1.0


# ── Per-signal scoring (score_signal) ────────────────────────────────


def test_perfect_signal():
    gold = {
        "ticket_id": "SIG-TEST",
        "category": "Threat Detection & Containment",
        "priority": "P1",
        "assigned_team": "Threat Response Command",
        "needs_escalation": True,
        "missing_information": ["stardate"],
    }
    s = score_signal(dict(gold), gold)
    # Weighted total should be 0.85 (classification weight sum)
    assert s["weighted_total"] > 0.84


def test_empty_signal():
    gold = {
        "ticket_id": "SIG-TEST",
        "category": "Threat Detection & Containment",
        "priority": "P1",
        "assigned_team": "Threat Response Command",
        "needs_escalation": True,
        "missing_information": ["stardate"],
    }
    s = score_signal({"ticket_id": "SIG-TEST"}, gold)
    assert s["weighted_total"] == 0.0


def test_signal_escalation_string_true():
    """Participant returns 'true' as string — should be treated as True."""
    gold = {
        "category": "Net",
        "priority": "P1",
        "assigned_team": "Ops",
        "needs_escalation": True,
        "missing_information": [],
    }
    cand = {
        "category": "Net",
        "priority": "P1",
        "assigned_team": "Ops",
        "needs_escalation": "true",
        "missing_information": [],
    }
    s = score_signal(cand, gold)
    assert s["escalation"] == 1.0


def test_signal_escalation_string_false():
    """'false' string must NOT be treated as True."""
    gold = {
        "category": "Net",
        "priority": "P1",
        "assigned_team": "Ops",
        "needs_escalation": False,
        "missing_information": [],
    }
    cand = {
        "category": "Net",
        "priority": "P1",
        "assigned_team": "Ops",
        "needs_escalation": "false",
        "missing_information": [],
    }
    s = score_signal(cand, gold)
    assert s["escalation"] == 1.0


def test_signal_missing_info_string_not_list():
    """Participant returns a string instead of list — treated as empty."""
    gold = {
        "category": "Net",
        "priority": "P1",
        "assigned_team": "Ops",
        "needs_escalation": False,
        "missing_information": ["anomaly_readout"],
    }
    cand = {
        "category": "Net",
        "priority": "P1",
        "assigned_team": "Ops",
        "needs_escalation": False,
        "missing_information": "anomaly_readout",
    }
    s = score_signal(cand, gold)
    assert s["missing_info"] == 0.0


def test_signal_returns_five_dimensions_plus_total():
    signal = {
        "category": "Net",
        "priority": "P1",
        "assigned_team": "Ops",
        "needs_escalation": False,
        "missing_information": [],
    }
    result = score_signal(signal, signal)
    assert set(result.keys()) == {"category", "priority", "routing", "missing_info", "escalation", "weighted_total"}


def test_signal_total_is_weighted_sum():
    """Verify the total equals the documented weighted sum formula."""
    gold = {
        "category": "Network",
        "priority": "P1",
        "assigned_team": "Operations",
        "needs_escalation": True,
        "missing_information": ["anomaly_readout", "stardate"],
    }
    cand = {
        "category": "Network",
        "priority": "P2",
        "assigned_team": "Wrong Team",
        "needs_escalation": True,
        "missing_information": ["anomaly_readout"],
    }
    result = score_signal(cand, gold)
    expected = (
        0.20 * result["category"]
        + 0.20 * result["priority"]
        + 0.20 * result["routing"]
        + 0.15 * result["missing_info"]
        + 0.10 * result["escalation"]
    )
    assert abs(result["weighted_total"] - expected) < 0.001


def test_signal_completely_wrong():
    """All dimensions wrong — a catastrophic triage failure."""
    gold = {
        "category": "Communications & Navigation",
        "priority": "P1",
        "assigned_team": "Deep Space Communications",
        "needs_escalation": True,
        "missing_information": ["anomaly_readout"],
    }
    cand = {
        "category": "Hull & Structural Systems",
        "priority": "P4",
        "assigned_team": "Spacecraft Systems Engineering",
        "needs_escalation": False,
        "missing_information": ["module_specs"],
    }
    result = score_signal(cand, gold)
    assert result["weighted_total"] < 0.1
    assert result["category"] == 0.0
    assert result["routing"] == 0.0
    assert result["escalation"] == 0.0


def test_signal_missing_all_fields():
    """Candidate returns empty dict — should score 0 on everything."""
    gold = {
        "category": "Threat Detection & Containment",
        "priority": "P1",
        "assigned_team": "Threat Response Command",
        "needs_escalation": True,
        "missing_information": ["anomaly_readout"],
    }
    result = score_signal({}, gold)
    assert result["category"] == 0.0
    assert result["priority"] == 0.0
    assert result["routing"] == 0.0
    assert result["escalation"] == 0.0
    assert result["missing_info"] == 0.0


def test_signal_none_missing_information():
    """Candidate returns None for missing_information — treated as empty list."""
    gold = {
        "category": "Net",
        "priority": "P1",
        "assigned_team": "Ops",
        "needs_escalation": False,
        "missing_information": [],
    }
    cand = {
        "category": "Net",
        "priority": "P1",
        "assigned_team": "Ops",
        "needs_escalation": False,
        "missing_information": None,
    }
    result = score_signal(cand, gold)
    assert result["missing_info"] == 1.0  # Both effectively empty → 1.0


def test_signal_extra_fields_ignored():
    """remediation_steps and other fields should not affect scoring."""
    signal = {
        "category": "Communications & Navigation",
        "priority": "P1",
        "assigned_team": "Deep Space Communications",
        "needs_escalation": False,
        "missing_information": [],
        "remediation_steps": ["Reboot the subspace relay"],
        "confidence": 0.95,
    }
    result = score_signal(signal, signal)
    assert result["weighted_total"] > 0.84
    assert "remediation" not in result
    assert "confidence" not in result


# ── Submission-level scoring (score_submission) ──────────────────────


def _make_signal(
    ticket_id,
    *,
    category="Communications & Navigation",
    priority="P1",
    assigned_team="Deep Space Communications",
    needs_escalation=False,
    missing_information=None,
):
    return {
        "ticket_id": ticket_id,
        "category": category,
        "priority": priority,
        "assigned_team": assigned_team,
        "needs_escalation": needs_escalation,
        "missing_information": missing_information or [],
    }


def test_submission_perfect_single():
    gold = [_make_signal("SIG-0001")]
    result = score_submission(gold, gold)
    assert result["classification_score"] == 85.0
    assert result["signals_scored"] == 1
    assert result["signals_errored"] == 0


def test_submission_perfect_multiple():
    gold = [_make_signal(f"SIG-{i:04d}") for i in range(10)]
    result = score_submission(gold, gold)
    assert result["classification_score"] == 85.0


def test_submission_missing_response():
    gold = [_make_signal("SIG-0001"), _make_signal("SIG-0002")]
    cands = [_make_signal("SIG-0001")]
    result = score_submission(cands, gold)
    assert result["signals_errored"] == 1
    assert result["classification_score"] < 60


def test_submission_all_missing():
    gold = [_make_signal("SIG-0001"), _make_signal("SIG-0002")]
    result = score_submission([], gold)
    assert result["signals_errored"] == 2
    assert result["classification_score"] <= 15


def test_submission_dimension_scores_are_fractions():
    gold = [_make_signal("SIG-0001")]
    result = score_submission(gold, gold)
    for v in result["dimension_scores"].values():
        assert 0.0 <= v <= 1.0


def test_submission_has_five_dimensions():
    gold = [_make_signal("SIG-0001")]
    result = score_submission(gold, gold)
    expected = {"category", "priority", "routing", "missing_info", "escalation"}
    assert set(result["dimension_scores"].keys()) == expected


def test_submission_extra_signals_ignored():
    gold = [_make_signal("SIG-0001")]
    cands = [_make_signal("SIG-0001"), _make_signal("SIG-9999")]
    result = score_submission(cands, gold)
    assert result["signals_scored"] == 1
    assert result["classification_score"] == 85.0


def test_weights_sum():
    """Classification weights should sum to 0.85."""
    total = sum(WEIGHTS.values())
    assert abs(total - 0.85) < 1e-9


def test_submission_empty_gold_raises():
    """Empty gold answer set should raise ValueError — can't score nothing."""
    with pytest.raises(ValueError, match="empty"):
        score_submission([], [])


def test_submission_per_signal_list_length():
    """per_signal list should match gold answer count."""
    gold = [_make_signal(f"SIG-{i:04d}") for i in range(5)]
    result = score_submission(gold, gold)
    assert len(result["per_signal"]) == 5


def test_submission_duplicate_ids_in_candidate():
    """If candidate has duplicate IDs, last occurrence is used (dict overwrite)."""
    gold = [_make_signal("SIG-0001", category="Communications & Navigation")]
    cands = [
        _make_signal("SIG-0001", category="Hull & Structural Systems"),
        _make_signal("SIG-0001", category="Communications & Navigation"),
    ]
    result = score_submission(cands, gold)
    assert result["dimension_scores"]["category"] == 1.0


def test_submission_errors_describe_missing_signals():
    """Error messages should mention missing signal IDs."""
    gold = [_make_signal("SIG-0001"), _make_signal("SIG-0002")]
    cands = [_make_signal("SIG-0001")]
    result = score_submission(cands, gold)
    assert len(result["errors"]) == 1
    assert "SIG-0002" in result["errors"][0]


def test_submission_half_correct_half_wrong():
    """2 signals: one perfect, one completely wrong → roughly half score."""
    gold = [
        _make_signal("SIG-0001"),
        _make_signal(
            "SIG-0002",
            category="Flight Software & Instruments",
            priority="P2",
            assigned_team="Mission Software Operations",
        ),
    ]
    cands = [
        _make_signal("SIG-0001"),
        _make_signal(
            "SIG-0002",
            category="Hull & Structural Systems",
            priority="P4",
            assigned_team="Spacecraft Systems Engineering",
        ),
    ]
    result = score_submission(cands, gold)
    assert 20 < result["classification_score"] < 55


def test_submission_classification_never_exceeds_85():
    """Classification-only max is 85 points (efficiency added externally)."""
    gold = [_make_signal(f"SIG-{i:04d}") for i in range(100)]
    result = score_submission(gold, gold)
    assert result["classification_score"] == 85.0


def test_submission_all_wrong_scores_low():
    """All wrong predictions should score near zero."""
    gold = [
        _make_signal(
            "SIG-0001",
            category="Threat Detection & Containment",
            priority="P1",
            assigned_team="Threat Response Command",
        )
    ]
    cands = [
        {
            "ticket_id": "SIG-0001",
            "category": "Hull & Structural Systems",
            "priority": "P4",
            "assigned_team": "Spacecraft Systems Engineering",
            "needs_escalation": True,
            "missing_information": ["wrong"],
        }
    ]
    result = score_submission(cands, gold)
    assert result["classification_score"] < 5.0


def test_submission_majority_class_gaming_penalized():
    """Always predicting the same category should score poorly on macro F1."""
    gold = [
        _make_signal("SIG-0001", category="Flight Software & Instruments"),
        _make_signal("SIG-0002", category="Flight Software & Instruments"),
        _make_signal("SIG-0003", category="Flight Software & Instruments"),
        _make_signal("SIG-0004", category="Flight Software & Instruments"),
        _make_signal("SIG-0005", category="Not a Mission Signal"),
        _make_signal("SIG-0006", category="Threat Detection & Containment"),
    ]
    cands = [_make_signal(f"SIG-{i:04d}", category="Flight Software & Instruments") for i in range(1, 7)]
    result = score_submission(cands, gold)
    assert result["dimension_scores"]["category"] < 0.5


def test_submission_uses_macro_f1_not_accuracy():
    """Verify submission score uses macro F1, not mean accuracy, for category."""
    gold = [
        _make_signal("SIG-0001", category="A"),
        _make_signal("SIG-0002", category="B"),
    ]
    cands = [
        _make_signal("SIG-0001", category="A"),
        _make_signal("SIG-0002", category="A"),
    ]
    result = score_submission(cands, gold)
    # Mean accuracy would be 0.5 (1/2 correct).
    # Macro F1: class A → TP=1, FP=1, FN=0 → F1=0.667; class B → TP=0, FP=0, FN=1 → F1=0
    # Macro F1 = (0.667 + 0) / 2 = 0.333 — lower than accuracy
    assert result["dimension_scores"]["category"] < 0.4


def test_submission_binary_f1_for_escalation():
    """Verify escalation uses binary F1, not per-signal accuracy."""
    gold = [
        _make_signal("SIG-0001", needs_escalation=True),
        _make_signal("SIG-0002", needs_escalation=True),
        _make_signal("SIG-0003", needs_escalation=False),
    ]
    # Never escalate — miss all positive cases
    cands = [
        _make_signal("SIG-0001", needs_escalation=False),
        _make_signal("SIG-0002", needs_escalation=False),
        _make_signal("SIG-0003", needs_escalation=False),
    ]
    result = score_submission(cands, gold)
    # Per-signal accuracy would be 1/3 = 0.333 (one correct: SIG-0003)
    # Binary F1 on positive class: TP=0, FP=0, FN=2 → F1=0.0
    assert result["dimension_scores"]["escalation"] == 0.0


def test_submission_all_categories_and_teams():
    """Submission with every category and team should score perfectly."""
    category_team_pairs = [
        ("Crew Access & Biometrics", "Crew Identity & Airlock Control"),
        ("Hull & Structural Systems", "Spacecraft Systems Engineering"),
        ("Communications & Navigation", "Deep Space Communications"),
        ("Flight Software & Instruments", "Mission Software Operations"),
        ("Threat Detection & Containment", "Threat Response Command"),
        ("Telemetry & Data Banks", "Telemetry & Data Core"),
        ("Mission Briefing Request", "None"),
        ("Not a Mission Signal", "None"),
    ]
    gold = [
        _make_signal(
            f"SIG-{i:04d}",
            category=cat,
            assigned_team=team,
            priority=f"P{(i % 4) + 1}",
            needs_escalation=i % 3 == 0,
            missing_information=["affected_subsystem", "anomaly_readout"] if i % 2 == 0 else [],
        )
        for i, (cat, team) in enumerate(category_team_pairs, start=1)
    ]
    result = score_submission(gold, gold)
    assert result["classification_score"] == 85.0
    assert result["signals_scored"] == 8
    assert result["signals_errored"] == 0


# ── Runner ────────────────────────────────────────────────────────────

if __name__ == "__main__":
    sys.exit(pytest.main([__file__, "-v"]))
