#!/usr/bin/env python3
"""Unit tests for the scoring functions in run_eval.py.

Test structure mirrors the scoring pipeline:
  1. Per-dimension scorers (category, priority, routing, missing_info, escalation)
  2. Boolean coercion helper (_coerce_bool)
  3. Submission-level aggregate metrics (macro_f1, binary_f1)
  4. Per-ticket composite (score_ticket)
  5. Full submission aggregate (score_submission)
"""

import sys

sys.path.insert(0, ".")  # noqa: TID251

from run_eval import WEIGHTS
from run_eval import _coerce_bool
from run_eval import binary_f1
from run_eval import macro_f1
from run_eval import score_category
from run_eval import score_escalation
from run_eval import score_missing_info
from run_eval import score_priority
from run_eval import score_routing
from run_eval import score_submission
from run_eval import score_ticket

# ── Category (multi-class exact match, case-insensitive) ────────────


def test_category_exact():
    assert score_category("Access & Authentication", "Access & Authentication") == 1.0


def test_category_case_insensitive():
    assert score_category("access & authentication", "Access & Authentication") == 1.0


def test_category_mismatch():
    assert score_category("Network & Connectivity", "Access & Authentication") == 0.0


def test_category_none():
    assert score_category(None, "Access & Authentication") == 0.0


def test_category_empty():
    assert score_category("", "Access & Authentication") == 0.0


def test_category_whitespace_trimmed():
    assert score_category("  Access & Authentication  ", "Access & Authentication") == 1.0


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


# ── Routing (multi-class exact match, case-insensitive) ─────────────


def test_routing_exact():
    assert score_routing("Security Operations", "Security Operations") == 1.0


def test_routing_case():
    assert score_routing("security operations", "Security Operations") == 1.0


def test_routing_mismatch():
    assert score_routing("Data Platform", "Security Operations") == 0.0


def test_routing_none_team():
    """'None' is a valid team for non-support tickets."""
    assert score_routing("None", "None") == 1.0


def test_routing_empty():
    assert score_routing("", "Security Operations") == 0.0


def test_routing_whitespace_trimmed():
    assert score_routing("  Security Operations  ", "Security Operations") == 1.0


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
    assert score_missing_info(["device_info"], []) == 0.0


def test_missing_false_negative():
    assert score_missing_info([], ["device_info"]) == 0.0


def test_missing_perfect():
    assert score_missing_info(["device_info"], ["device_info"]) == 1.0


def test_missing_perfect_different_order():
    assert score_missing_info(["device_info", "error_message"], ["error_message", "device_info"]) == 1.0


def test_missing_partial_recall():
    # pred=1 of 2 gold. P=1/1=1.0, R=1/2=0.5, F1=2*1*0.5/1.5=0.667
    f1 = score_missing_info(["device_info"], ["device_info", "error_message"])
    assert abs(f1 - 2 / 3) < 0.01


def test_missing_partial_precision():
    # pred=2, gold=1. P=1/2=0.5, R=1/1=1.0, F1=2*0.5*1/1.5=0.667
    f1 = score_missing_info(["device_info", "error_message"], ["device_info"])
    assert abs(f1 - 2 / 3) < 0.01


def test_missing_partial_overlap():
    # 1 TP, 1 FP, 1 FN → precision=0.5, recall=0.5, F1=0.5
    score = score_missing_info(["error_message", "device_info"], ["error_message", "timestamp"])
    assert abs(score - 0.5) < 0.01


def test_missing_no_overlap():
    assert score_missing_info(["error_message"], ["device_info"]) == 0.0


def test_missing_case_insensitive():
    assert score_missing_info(["Error_Message"], ["error_message"]) == 1.0


def test_missing_duplicates_deduplicated():
    """Candidate sends same item twice — should still score as 1 TP."""
    score = score_missing_info(["error_message", "error_message"], ["error_message"])
    assert score == 1.0


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


def test_binary_f1_empty():
    assert binary_f1([], []) == 1.0


# ── Per-ticket scoring (score_ticket) ────────────────────────────────


def test_perfect_ticket():
    gold = {
        "ticket_id": "INC-TEST",
        "category": "Security & Compliance",
        "priority": "P1",
        "assigned_team": "Security Operations",
        "needs_escalation": True,
        "missing_information": ["timestamp"],
    }
    s = score_ticket(dict(gold), gold)
    # Weighted total should be 0.85 (classification weight sum)
    assert s["weighted_total"] > 0.84


def test_empty_ticket():
    gold = {
        "ticket_id": "INC-TEST",
        "category": "Security & Compliance",
        "priority": "P1",
        "assigned_team": "Security Operations",
        "needs_escalation": True,
        "missing_information": ["timestamp"],
    }
    s = score_ticket({"ticket_id": "INC-TEST"}, gold)
    assert s["weighted_total"] == 0.0


def test_ticket_escalation_string_true():
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
    s = score_ticket(cand, gold)
    assert s["escalation"] == 1.0


def test_ticket_escalation_string_false():
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
    s = score_ticket(cand, gold)
    assert s["escalation"] == 1.0


def test_ticket_missing_info_string_not_list():
    """Participant returns a string instead of list — treated as empty."""
    gold = {
        "category": "Net",
        "priority": "P1",
        "assigned_team": "Ops",
        "needs_escalation": False,
        "missing_information": ["error_message"],
    }
    cand = {
        "category": "Net",
        "priority": "P1",
        "assigned_team": "Ops",
        "needs_escalation": False,
        "missing_information": "error_message",
    }
    s = score_ticket(cand, gold)
    assert s["missing_info"] == 0.0


def test_ticket_returns_five_dimensions_plus_total():
    ticket = {
        "category": "Net",
        "priority": "P1",
        "assigned_team": "Ops",
        "needs_escalation": False,
        "missing_information": [],
    }
    result = score_ticket(ticket, ticket)
    assert set(result.keys()) == {"category", "priority", "routing", "missing_info", "escalation", "weighted_total"}


def test_ticket_total_is_weighted_sum():
    """Verify the total equals the documented weighted sum formula."""
    gold = {
        "category": "Network",
        "priority": "P1",
        "assigned_team": "Operations",
        "needs_escalation": True,
        "missing_information": ["error_message", "timestamp"],
    }
    cand = {
        "category": "Network",
        "priority": "P2",
        "assigned_team": "Wrong Team",
        "needs_escalation": True,
        "missing_information": ["error_message"],
    }
    result = score_ticket(cand, gold)
    expected = (
        0.20 * result["category"]
        + 0.20 * result["priority"]
        + 0.20 * result["routing"]
        + 0.15 * result["missing_info"]
        + 0.10 * result["escalation"]
    )
    assert abs(result["weighted_total"] - expected) < 0.001


# ── Submission-level scoring (score_submission) ──────────────────────


def _make_ticket(
    ticket_id,
    *,
    category="Network & Connectivity",
    priority="P1",
    assigned_team="Network Operations",
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
    gold = [_make_ticket("INC-0001")]
    result = score_submission(gold, gold)
    assert result["classification_score"] == 85.0
    assert result["tickets_scored"] == 1
    assert result["tickets_errored"] == 0


def test_submission_perfect_multiple():
    gold = [_make_ticket(f"INC-{i:04d}") for i in range(10)]
    result = score_submission(gold, gold)
    assert result["classification_score"] == 85.0


def test_submission_missing_response():
    gold = [_make_ticket("INC-0001"), _make_ticket("INC-0002")]
    cands = [_make_ticket("INC-0001")]
    result = score_submission(cands, gold)
    assert result["tickets_errored"] == 1
    assert result["classification_score"] < 60


def test_submission_all_missing():
    gold = [_make_ticket("INC-0001"), _make_ticket("INC-0002")]
    result = score_submission([], gold)
    assert result["tickets_errored"] == 2
    assert result["classification_score"] <= 15


def test_submission_dimension_scores_are_fractions():
    gold = [_make_ticket("INC-0001")]
    result = score_submission(gold, gold)
    for v in result["dimension_scores"].values():
        assert 0.0 <= v <= 1.0


def test_submission_has_five_dimensions():
    gold = [_make_ticket("INC-0001")]
    result = score_submission(gold, gold)
    expected = {"category", "priority", "routing", "missing_info", "escalation"}
    assert set(result["dimension_scores"].keys()) == expected


def test_submission_extra_tickets_ignored():
    gold = [_make_ticket("INC-0001")]
    cands = [_make_ticket("INC-0001"), _make_ticket("INC-9999")]
    result = score_submission(cands, gold)
    assert result["tickets_scored"] == 1
    assert result["classification_score"] == 85.0


def test_weights_sum():
    """Classification weights should sum to 0.85."""
    total = sum(WEIGHTS.values())
    assert abs(total - 0.85) < 1e-9


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
