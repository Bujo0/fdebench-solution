#!/usr/bin/env python3
"""Unit tests for the scoring functions in run_eval.py.

🛰️ SCORING COMPUTER SELF-DIAGNOSTICS 🛰️
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    "Before you trust a scoring computer to grade triage decisions
     that affect 2,000 lives, you'd better make sure the scoring
     computer itself isn't hallucinating. Run these tests. All of
     them. Every time."
                                    — Lt. Mehta, Mission Control

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

_spec = importlib.util.spec_from_file_location("run_eval", Path(__file__).resolve().parent / "run_eval.py")
assert _spec and _spec.loader, "Failed to locate run_eval.py — is it in the same directory as this test?"
_run_eval = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_run_eval)

WEIGHTS = _run_eval.WEIGHTS
_coerce_bool = _run_eval._coerce_bool
binary_f1 = _run_eval.binary_f1
macro_f1 = _run_eval.macro_f1
score_category = _run_eval.score_category
score_escalation = _run_eval.score_escalation
score_missing_info = _run_eval.score_missing_info
score_priority = _run_eval.score_priority
score_routing = _run_eval.score_routing
score_submission = _run_eval.score_submission
score_signal = _run_eval.score_signal

# ── Category (did you identify the right anomaly type?) ─────────────


def test_category_exact():
    """Exact anomaly classification — gold star, the right team scrambles."""
    assert score_category("Crew Access & Biometrics", "Crew Access & Biometrics") == 1.0


def test_category_case_insensitive():
    """Case doesn't matter in space — the void doesn't care about capitalization."""
    assert score_category("crew access & biometrics", "Crew Access & Biometrics") == 1.0


def test_category_mismatch():
    """Wrong category — Threat Response is now staring at a biometric scanner. Someone else is on fire."""
    assert score_category("Communications & Navigation", "Crew Access & Biometrics") == 0.0


def test_category_none():
    """No answer is not an answer. The crew is waiting. The void is patient. You should not be."""
    assert score_category(None, "Crew Access & Biometrics") == 0.0


def test_category_empty():
    """Empty string — you had one job and you returned nothing. Even the cats on Deck 9 judge you."""
    assert score_category("", "Crew Access & Biometrics") == 0.0


def test_category_whitespace_trimmed():
    """Extra whitespace is forgiven — the scoring computer is strict, not petty."""
    assert score_category("  Crew Access & Biometrics  ", "Crew Access & Biometrics") == 1.0


# ── Priority (is it a Red Alert or just a jammed nutrient synthesizer?) ──────────


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
    """Off by 2 levels = 0.0 — you called a hull breach 'routine.' Deck 7 now has mood lighting. From space."""
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


# ── Routing (did you send the signal to the right division?) ────────


def test_routing_exact():
    """Right team, first try — no bouncing signals across the station like a zero-g pinball."""
    assert score_routing("Threat Response Command", "Threat Response Command") == 1.0


def test_routing_case():
    """Case insensitive — the scoring computer doesn't care if you whisper or shout the team name."""
    assert score_routing("threat response command", "Threat Response Command") == 1.0


def test_routing_mismatch():
    """Wrong team — Telemetry & Data Core is now responding to a hostile contact report. Awkward."""
    assert score_routing("Telemetry & Data Core", "Threat Response Command") == 0.0


def test_routing_none_team():
    """'None' is a valid team for non-mission signals. The void gets routed to no one. As it should."""
    assert score_routing("None", "None") == 1.0


def test_routing_empty():
    """No team assigned — the signal floats in the queue like debris in orbit. Forever."""
    assert score_routing("", "Threat Response Command") == 0.0


def test_routing_whitespace_trimmed():
    """Whitespace around team names is trimmed — we're lenient about formatting, not about routing."""
    assert score_routing("  Threat Response Command  ", "Threat Response Command") == 1.0


# ── Escalation (did you sound the alarm when it mattered?) ──────────


def test_escalation_true_true():
    """Hostile contact flagged, Admiral notified — you saved careers today."""
    assert score_escalation(True, True) == 1.0


def test_escalation_false_false():
    """No escalation needed, none triggered — the rare art of correctly doing nothing."""
    assert score_escalation(False, False) == 1.0


def test_escalation_mismatch():
    """False alarm pulled — Threat Response Command mobilized for a fabricator jam. They're not happy."""
    assert score_escalation(True, False) == 0.0


def test_escalation_none():
    """No answer on escalation — the Admiral found out from the news. You're in trouble."""
    assert score_escalation(None, True) == 0.0


# ── Missing info (did you ask for the right intel?) ──────────────────


def test_missing_both_empty():
    """Both empty — signal was complete, you recognized it. Don't waste subspace bandwidth asking for more."""
    assert score_missing_info([], []) == 1.0


def test_missing_false_positive():
    """Asked for intel that wasn't needed — you asked for more. They're annoyed."""
    assert score_missing_info(["module_specs"], []) == 0.0


def test_missing_false_negative():
    """Needed intel but didn't ask — now you're flying blind. The void doesn't volunteer information."""
    assert score_missing_info([], ["module_specs"]) == 0.0


def test_missing_perfect():
    """Asked for exactly what was missing — precise, efficient, no wasted subspace relay capacity."""
    assert score_missing_info(["module_specs"], ["module_specs"]) == 1.0


def test_missing_perfect_different_order():
    """Order doesn't matter — ask the right questions and the scoring computer is satisfied."""
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


# ── Boolean coercion (because crew members return weird stuff) ──────


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


# ── Macro F1 (the great equalizer — every anomaly type matters) ──────


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
    """Always predicting majority class should score poorly. Space doesn't reward lazy triage."""
    golds = ["A"] * 8 + ["B"] * 1 + ["C"] * 1
    candidates = ["A"] * 10
    score = macro_f1(candidates, golds, ["A", "B", "C"])
    assert score < 0.35


def test_macro_f1_case_insensitive():
    assert macro_f1(["a", "b"], ["A", "B"], ["A", "B"]) == 1.0


def test_macro_f1_absent_classes_excluded():
    """Classes with zero TP, FP, and FN don't count — quiet sectors stay off the scorecard."""
    assert macro_f1(["A", "A"], ["A", "A"], ["A", "B", "C"]) == 1.0


def test_macro_f1_empty():
    assert macro_f1([], [], ["A", "B"]) == 0.0


# ── Binary F1 (escalation: did you call for backup?) ─────────────────


def test_binary_f1_all_true_positives():
    assert binary_f1([True, True], [True, True]) == 1.0


def test_binary_f1_all_true_negatives():
    """No positive cases anywhere → perfect agreement on "all clear, Admiral" → 1.0."""
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


# ── Per-signal scoring (the after-action report) ─────────────────────


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
    """Participant returns 'true' as string — should be treated as True.

    The crew doesn't care about your type system.
    """
    gold = {
        "category": "Comms",
        "priority": "P1",
        "assigned_team": "DeepSpace",
        "needs_escalation": True,
        "missing_information": [],
    }
    cand = {
        "category": "Comms",
        "priority": "P1",
        "assigned_team": "DeepSpace",
        "needs_escalation": "true",
        "missing_information": [],
    }
    s = score_signal(cand, gold)
    assert s["escalation"] == 1.0


def test_signal_escalation_string_false():
    """'false' string must NOT be treated as True — Python's bool('false') is a trap.

    A cosmic trap that has ended more careers than airlock malfunctions.
    """
    gold = {
        "category": "Comms",
        "priority": "P1",
        "assigned_team": "DeepSpace",
        "needs_escalation": False,
        "missing_information": [],
    }
    cand = {
        "category": "Comms",
        "priority": "P1",
        "assigned_team": "DeepSpace",
        "needs_escalation": "false",
        "missing_information": [],
    }
    s = score_signal(cand, gold)
    assert s["escalation"] == 1.0


def test_signal_missing_info_string_not_list():
    """Participant returns a string instead of list — treated as empty.

    The scoring computer is strict, like the void.
    """
    gold = {
        "category": "Comms",
        "priority": "P1",
        "assigned_team": "DeepSpace",
        "needs_escalation": False,
        "missing_information": ["anomaly_readout"],
    }
    cand = {
        "category": "Comms",
        "priority": "P1",
        "assigned_team": "DeepSpace",
        "needs_escalation": False,
        "missing_information": "anomaly_readout",
    }
    s = score_signal(cand, gold)
    assert s["missing_info"] == 0.0


def test_signal_returns_five_dimensions_plus_total():
    signal = {
        "category": "Comms",
        "priority": "P1",
        "assigned_team": "DeepSpace",
        "needs_escalation": False,
        "missing_information": [],
    }
    result = score_signal(signal, signal)
    assert set(result.keys()) == {"category", "priority", "routing", "missing_info", "escalation", "weighted_total"}


def test_signal_total_is_weighted_sum():
    """Verify the total equals the documented weighted sum formula. No rounding errors in space — those cost lives."""
    gold = {
        "category": "Communications & Navigation",
        "priority": "P1",
        "assigned_team": "Deep Space Communications",
        "needs_escalation": True,
        "missing_information": ["anomaly_readout", "stardate"],
    }
    cand = {
        "category": "Communications & Navigation",
        "priority": "P2",
        "assigned_team": "Wrong Division",
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


# ── Full submission scoring (the final reckoning) ────────────────────


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
    """One signal, perfect triage — even a broken clock gets one right. But you earned this one."""
    gold = [_make_signal("SIG-0001")]
    result = score_submission(gold, gold)
    assert result["classification_score"] == 85.0
    assert result["signals_scored"] == 1
    assert result["signals_errored"] == 0


def test_submission_perfect_multiple():
    """Ten signals, all perfect — the crew is naming a corridor after you. Or at least thinking about it."""
    gold = [_make_signal(f"SIG-{i:04d}") for i in range(10)]
    result = score_submission(gold, gold)
    assert result["classification_score"] == 85.0


def test_submission_missing_response():
    """One signal went unanswered — somewhere on Deck 7, someone is still waiting. The cats are watching."""
    gold = [_make_signal("SIG-0001"), _make_signal("SIG-0002")]
    cands = [_make_signal("SIG-0001")]
    result = score_submission(cands, gold)
    assert result["signals_errored"] == 1
    assert result["classification_score"] < 60


def test_submission_all_missing():
    """No responses at all — you built a triage system that triages nothing. The void approves. The crew does not."""
    gold = [_make_signal("SIG-0001"), _make_signal("SIG-0002")]
    result = score_submission([], gold)
    assert result["signals_errored"] == 2
    assert result["classification_score"] <= 15


def test_submission_dimension_scores_are_fractions():
    """All dimension scores should be 0-1 fractions — not percentages, not credits, not decibels."""
    gold = [_make_signal("SIG-0001")]
    result = score_submission(gold, gold)
    for v in result["dimension_scores"].values():
        assert 0.0 <= v <= 1.0


def test_submission_has_five_dimensions():
    """Exactly 5 dimensions — like the 5 decks between you and the nearest airlock if you get these wrong."""
    gold = [_make_signal("SIG-0001")]
    result = score_submission(gold, gold)
    expected = {"category", "priority", "routing", "missing_info", "escalation"}
    assert set(result["dimension_scores"].keys()) == expected


def test_submission_extra_signals_ignored():
    """Signals you answered that weren't in the gold set — ignored. The scoring computer does not reward enthusiasm."""
    gold = [_make_signal("SIG-0001")]
    cands = [_make_signal("SIG-0001"), _make_signal("SIG-9999")]
    result = score_submission(cands, gold)
    assert result["signals_scored"] == 1
    assert result["classification_score"] == 85.0


def test_weights_sum():
    """Classification weights should sum to 0.85. The remaining 0.15 is efficiency — the fuel budget."""
    total = sum(WEIGHTS.values())
    assert abs(total - 0.85) < 1e-9


# ── Self-diagnostics runner ────────────────────────────────────────────

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
