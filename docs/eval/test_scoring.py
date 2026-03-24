#!/usr/bin/env python3
"""Unit tests for the scoring functions in run_eval.py."""
import sys
sys.path.insert(0, ".")

from run_eval import (
    WEIGHTS,
    score_category,
    score_escalation,
    score_missing_info,
    score_priority,
    score_remediation_simple,
    score_routing,
    score_ticket,
)


def test_weights_sum_to_one():
    assert abs(sum(WEIGHTS.values()) - 1.0) < 1e-9


def test_category_exact():
    assert score_category("Access & Authentication", "Access & Authentication") == 1.0


def test_category_case_insensitive():
    assert score_category("access & authentication", "Access & Authentication") == 1.0


def test_category_mismatch():
    assert score_category("Network & Connectivity", "Access & Authentication") == 0.0


def test_category_none():
    assert score_category(None, "Access & Authentication") == 0.0


def test_priority_exact():
    assert score_priority("P1", "P1") == 1.0


def test_priority_off_by_1():
    assert score_priority("P2", "P1") == 0.67


def test_priority_off_by_2():
    assert score_priority("P3", "P1") == 0.33


def test_priority_off_by_3():
    assert score_priority("P4", "P1") == 0.0


def test_priority_symmetric():
    assert score_priority("P1", "P4") == 0.0


def test_priority_invalid():
    assert score_priority("X", "P1") == 0.0


def test_priority_none():
    assert score_priority(None, "P1") == 0.0


def test_routing_exact():
    assert score_routing("Security Operations", "Security Operations") == 1.0


def test_routing_case():
    assert score_routing("security operations", "Security Operations") == 1.0


def test_routing_mismatch():
    assert score_routing("Data Platform", "Security Operations") == 0.0


def test_escalation_true_true():
    assert score_escalation(True, True) == 1.0


def test_escalation_false_false():
    assert score_escalation(False, False) == 1.0


def test_escalation_mismatch():
    assert score_escalation(True, False) == 0.0


def test_escalation_none():
    assert score_escalation(None, True) == 0.0


def test_missing_both_empty():
    assert score_missing_info([], []) == 1.0


def test_missing_false_positive():
    assert score_missing_info(["device_info"], []) == 0.0


def test_missing_false_negative():
    assert score_missing_info([], ["device_info"]) == 0.0


def test_missing_perfect():
    assert score_missing_info(["device_info"], ["device_info"]) == 1.0


def test_missing_partial_recall():
    # pred=1 of 2 gold. P=1/1=1.0, R=1/2=0.5, F1=2*1*0.5/1.5=0.667
    f1 = score_missing_info(["device_info"], ["device_info", "error_message"])
    assert abs(f1 - 2 / 3) < 0.01


def test_missing_partial_precision():
    # pred=2, gold=1. P=1/2=0.5, R=1/1=1.0, F1=2*0.5*1/1.5=0.667
    f1 = score_missing_info(["device_info", "error_message"], ["device_info"])
    assert abs(f1 - 2 / 3) < 0.01


def test_missing_overlap():
    # pred={device_info, error_message, timestamp}, gold={device_info, steps_to_reproduce}
    # TP=1, P=1/3, R=1/2, F1=2*(1/3)*(1/2)/((1/3)+(1/2))=0.4
    f1 = score_missing_info(
        ["device_info", "error_message", "timestamp"],
        ["device_info", "steps_to_reproduce"],
    )
    assert abs(f1 - 0.4) < 0.01


def test_perfect_ticket():
    gold = {
        "ticket_id": "INC-TEST",
        "category": "Security & Compliance",
        "priority": "P1",
        "assigned_team": "Security Operations",
        "needs_escalation": True,
        "missing_information": ["timestamp"],
        "next_best_action": "Investigate immediately",
        "remediation_steps": ["Step 1", "Step 2", "Step 3"],
    }
    s = score_ticket(dict(gold), gold)
    assert s["weighted_total"] == 1.0


def test_empty_ticket():
    gold = {
        "ticket_id": "INC-TEST",
        "category": "Security & Compliance",
        "priority": "P1",
        "assigned_team": "Security Operations",
        "needs_escalation": True,
        "missing_information": ["timestamp"],
        "next_best_action": "Investigate immediately",
        "remediation_steps": ["Step 1", "Step 2", "Step 3"],
    }
    s = score_ticket({"ticket_id": "INC-TEST"}, gold)
    assert s["weighted_total"] == 0.0


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
