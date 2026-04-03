# Copyright (c) Microsoft. All rights reserved.
"""Tests for scoring functions.

Mirrors the structure in docs/eval/test_scoring.py but operates on
typed Pydantic models from ms.evals.
"""

import pytest

from ms.evals.models import DimensionScores
from ms.evals.models import GoldAnswer
from ms.evals.models import TriageResponse
from ms.evals.scoring import WEIGHTS
from ms.evals.scoring import binary_f1
from ms.evals.scoring import compute_aggregate_scores
from ms.evals.scoring import macro_f1
from ms.evals.scoring import score_category
from ms.evals.scoring import score_escalation
from ms.evals.scoring import score_missing_info
from ms.evals.scoring import score_priority
from ms.evals.scoring import score_routing
from ms.evals.scoring import score_ticket

# ── Category ────────────────────────────────────────────────────


class TestScoreCategory:
    def test_exact_match(self) -> None:
        assert score_category("Access & Authentication", "Access & Authentication") == 1.0

    def test_case_insensitive(self) -> None:
        assert score_category("access & authentication", "Access & Authentication") == 1.0

    def test_mismatch(self) -> None:
        assert score_category("Network & Connectivity", "Access & Authentication") == 0.0

    def test_whitespace_trimmed(self) -> None:
        assert score_category("  Access & Authentication  ", "Access & Authentication") == 1.0

    def test_empty_prediction(self) -> None:
        assert score_category("", "Access & Authentication") == 0.0


# ── Priority ────────────────────────────────────────────────────


class TestScorePriority:
    def test_exact(self) -> None:
        assert score_priority("P1", "P1") == 1.0

    @pytest.mark.parametrize("priority", ["P1", "P2", "P3", "P4"])
    def test_all_levels_exact(self, priority: str) -> None:
        assert score_priority(priority, priority) == 1.0

    def test_off_by_one(self) -> None:
        assert score_priority("P2", "P1") == 0.67

    def test_off_by_one_symmetric(self) -> None:
        assert score_priority("P1", "P2") == 0.67
        assert score_priority("P3", "P4") == 0.67

    def test_off_by_two(self) -> None:
        assert score_priority("P3", "P1") == 0.0

    def test_off_by_three(self) -> None:
        assert score_priority("P4", "P1") == 0.0

    def test_invalid_prediction(self) -> None:
        assert score_priority("X", "P1") == 0.0

    def test_empty_prediction(self) -> None:
        assert score_priority("", "P1") == 0.0

    def test_case_insensitive(self) -> None:
        assert score_priority("p2", "P2") == 1.0


# ── Routing ─────────────────────────────────────────────────────


class TestScoreRouting:
    def test_exact_match(self) -> None:
        assert score_routing("Security Operations", "Security Operations") == 1.0

    def test_case_insensitive(self) -> None:
        assert score_routing("security operations", "Security Operations") == 1.0

    def test_mismatch(self) -> None:
        assert score_routing("Data Platform", "Security Operations") == 0.0

    def test_none_team(self) -> None:
        assert score_routing("None", "None") == 1.0


# ── Escalation ──────────────────────────────────────────────────


class TestScoreEscalation:
    def test_true_true(self) -> None:
        assert score_escalation(True, True) == 1.0

    def test_false_false(self) -> None:
        assert score_escalation(False, False) == 1.0

    def test_mismatch(self) -> None:
        assert score_escalation(True, False) == 0.0

    def test_string_true(self) -> None:
        assert score_escalation("true", True) == 1.0

    def test_string_false(self) -> None:
        assert score_escalation("false", False) == 1.0

    def test_none(self) -> None:
        assert score_escalation(None, True) == 0.0


# ── Missing Info ────────────────────────────────────────────────


class TestScoreMissingInfo:
    def test_both_empty(self) -> None:
        assert score_missing_info([], []) == 1.0

    def test_false_positive(self) -> None:
        assert score_missing_info(["device_info"], []) == 0.0

    def test_false_negative(self) -> None:
        assert score_missing_info([], ["device_info"]) == 0.0

    def test_perfect(self) -> None:
        assert score_missing_info(["device_info"], ["device_info"]) == 1.0

    def test_partial_recall(self) -> None:
        f1 = score_missing_info(["device_info"], ["device_info", "error_message"])
        assert abs(f1 - 2 / 3) < 0.01

    def test_partial_precision(self) -> None:
        f1 = score_missing_info(["device_info", "error_message"], ["device_info"])
        assert abs(f1 - 2 / 3) < 0.01

    def test_no_overlap(self) -> None:
        assert score_missing_info(["error_message"], ["device_info"]) == 0.0

    def test_case_insensitive(self) -> None:
        assert score_missing_info(["Error_Message"], ["error_message"]) == 1.0


# ── Macro F1 ────────────────────────────────────────────────────


class TestMacroF1:
    def test_perfect(self) -> None:
        assert macro_f1(["A", "B"], ["A", "B"], ["A", "B"]) == 1.0

    def test_all_wrong(self) -> None:
        assert macro_f1(["B", "B"], ["A", "A"], ["A", "B"]) == 0.0

    def test_majority_gaming_penalized(self) -> None:
        golds = ["A"] * 8 + ["B"] * 1 + ["C"] * 1
        preds = ["A"] * 10
        score = macro_f1(preds, golds, ["A", "B", "C"])
        assert score < 0.35

    def test_empty(self) -> None:
        assert macro_f1([], [], ["A", "B"]) == 0.0


# ── Binary F1 ───────────────────────────────────────────────────


class TestBinaryF1:
    def test_all_true_positives(self) -> None:
        assert binary_f1([True, True], [True, True]) == 1.0

    def test_all_true_negatives(self) -> None:
        assert binary_f1([False, False], [False, False]) == 1.0

    def test_partial(self) -> None:
        score = binary_f1([True, True, False], [True, False, True])
        assert abs(score - 0.5) < 0.01

    def test_empty(self) -> None:
        assert binary_f1([], []) == 1.0


# ── Per-ticket scoring ──────────────────────────────────────────


def _make_response(**overrides: object) -> TriageResponse:
    defaults = {
        "ticket_id": "INC-TEST",
        "category": "Security & Compliance",
        "priority": "P1",
        "assigned_team": "Security Operations",
        "needs_escalation": True,
        "missing_information": ["timestamp"],
        "next_best_action": "Investigate",
        "remediation_steps": ["Step 1"],
    }
    defaults.update(overrides)
    return TriageResponse.model_validate(defaults)


def _make_gold(**overrides: object) -> GoldAnswer:
    defaults = {
        "ticket_id": "INC-TEST",
        "category": "Security & Compliance",
        "priority": "P1",
        "assigned_team": "Security Operations",
        "needs_escalation": True,
        "missing_information": ["timestamp"],
        "next_best_action": "Investigate",
        "remediation_steps": ["Step 1"],
    }
    defaults.update(overrides)
    return GoldAnswer.model_validate(defaults)


class TestScoreTicket:
    def test_perfect(self) -> None:
        resp = _make_response()
        gold = _make_gold()
        scores = score_ticket(resp, gold)
        assert scores.weighted_total > 0.84

    def test_all_wrong(self) -> None:
        resp = _make_response(
            category="General Inquiry",
            priority="P4",
            assigned_team="None",
            needs_escalation=False,
            missing_information=[],
        )
        gold = _make_gold()
        scores = score_ticket(resp, gold)
        assert scores.weighted_total < 0.01

    def test_returns_five_dimensions(self) -> None:
        expected = {"category", "priority", "routing", "escalation", "missing_info", "weighted_total"}
        assert set(DimensionScores.model_fields.keys()) == expected

    def test_weighted_sum_formula(self) -> None:
        resp = _make_response(priority="P2", assigned_team="Data Platform")
        gold = _make_gold()
        scores = score_ticket(resp, gold)
        expected = (
            0.20 * scores.category
            + 0.20 * scores.priority
            + 0.20 * scores.routing
            + 0.15 * scores.missing_info
            + 0.10 * scores.escalation
        )
        assert abs(scores.weighted_total - expected) < 0.001


# ── Weights ─────────────────────────────────────────────────────


class TestWeights:
    def test_sum_to_085(self) -> None:
        total = sum(WEIGHTS.values())
        assert abs(total - 0.85) < 1e-9


# ── Aggregate scoring ──────────────────────────────────────────


class TestComputeAggregateScores:
    def test_perfect_single_ticket(self) -> None:
        resp = _make_response()
        gold = _make_gold()
        scores = score_ticket(resp, gold)
        agg, classification = compute_aggregate_scores([scores], [resp], [gold])
        assert classification == 85.0

    def test_empty_results(self) -> None:
        agg, classification = compute_aggregate_scores([], [], [])
        # With no tickets, all dimension scores should be 0
        assert agg.category == 0.0
        assert agg.priority == 0.0
        assert agg.routing == 0.0
        assert agg.missing_info == 0.0
