# Copyright (c) Microsoft. All rights reserved.
"""Scoring functions for evaluation results.

These mirror the scoring logic in ``docs/eval/run_eval.py`` but operate on
typed Pydantic models rather than raw dicts.  The formulas are identical so
local eval scores match the platform scorer exactly.
"""

from ms.evals_core.constants import Category
from ms.evals_core.constants import Team
from ms.evals_core.eval_models import DimensionAggregates
from ms.evals_core.eval_models import DimensionScores
from ms.evals_core.eval_models import GoldAnswer
from ms.evals_core.eval_models import TriageResponse

# Classification dimension weights — must sum to 0.85.
WEIGHTS: dict[str, float] = {
    "category": 0.20,
    "priority": 0.20,
    "routing": 0.20,
    "missing_info": 0.15,
    "escalation": 0.10,
}

_PRIORITY_ORDER = {"P1": 1, "P2": 2, "P3": 3, "P4": 4}


def score_category(predicted: str, gold: str) -> float:
    """Exact match, case-insensitive."""
    return 1.0 if predicted.strip().lower() == gold.strip().lower() else 0.0


def score_priority(predicted: str, gold: str) -> float:
    """Ordinal scoring: exact = 1.0, off-by-one = 0.67, else 0.0."""
    p = _PRIORITY_ORDER.get(predicted.strip().upper(), -1)
    g = _PRIORITY_ORDER.get(gold.strip().upper(), -1)
    if p < 0 or g < 0:
        return 0.0
    diff = abs(p - g)
    if diff == 0:
        return 1.0
    if diff == 1:
        return 0.67
    return 0.0


def score_routing(predicted: str, gold: str) -> float:
    """Exact match, case-insensitive."""
    return 1.0 if predicted.strip().lower() == gold.strip().lower() else 0.0


def _coerce_bool(value: object) -> bool:
    """Coerce common representations to bool (mirrors run_eval.py logic)."""
    if isinstance(value, bool):
        return value
    if value is None:
        return False
    if isinstance(value, int):
        return value != 0
    if isinstance(value, str):
        cleaned = value.strip().lower()
        return cleaned in {"true", "yes", "1"}
    return False


def score_escalation(predicted: object, gold: bool) -> float:
    """Binary exact match after coercing booleans."""
    return 1.0 if _coerce_bool(predicted) == gold else 0.0


def score_missing_info(predicted: list[str], gold: list[str]) -> float:
    """Set F1 on constrained vocabulary, case-insensitive."""
    pred_set = {s.strip().lower() for s in predicted}
    gold_set = {s.strip().lower() for s in gold}

    if not pred_set and not gold_set:
        return 1.0
    if not pred_set or not gold_set:
        return 0.0

    tp = len(pred_set & gold_set)
    precision = tp / len(pred_set)
    recall = tp / len(gold_set)
    if precision + recall == 0:
        return 0.0
    return 2 * precision * recall / (precision + recall)


def score_ticket(response: TriageResponse, gold: GoldAnswer) -> DimensionScores:
    """Score a single ticket across all five classification dimensions."""
    cat = score_category(response.category, gold.category)
    pri = score_priority(response.priority, gold.priority)
    rout = score_routing(response.assigned_team, gold.assigned_team)
    esc = score_escalation(response.needs_escalation, gold.needs_escalation)
    miss = score_missing_info(
        response.missing_information,
        [str(m) for m in gold.missing_information],
    )

    weighted = (
        WEIGHTS["category"] * cat
        + WEIGHTS["priority"] * pri
        + WEIGHTS["routing"] * rout
        + WEIGHTS["missing_info"] * miss
        + WEIGHTS["escalation"] * esc
    )

    return DimensionScores(
        category=cat,
        priority=pri,
        routing=rout,
        escalation=esc,
        missing_info=miss,
        weighted_total=weighted,
    )


def macro_f1(
    predictions: list[str],
    golds: list[str],
    all_labels: list[str],
) -> float:
    """Compute macro F1 across all classes (case-insensitive)."""
    if not predictions or not golds:
        return 0.0

    preds_lower = [p.strip().lower() for p in predictions]
    golds_lower = [g.strip().lower() for g in golds]
    labels = [label_str.strip().lower() for label_str in all_labels]

    f1_sum = 0.0
    active_classes = 0

    for label in labels:
        tp = sum(
            1
            for p, g in zip(preds_lower, golds_lower, strict=True)
            if p == label and g == label
        )
        fp = sum(
            1
            for p, g in zip(preds_lower, golds_lower, strict=True)
            if p == label and g != label
        )
        fn = sum(
            1
            for p, g in zip(preds_lower, golds_lower, strict=True)
            if p != label and g == label
        )

        if tp + fp + fn == 0:
            continue  # Class not present at all — skip
        active_classes += 1

        precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
        f1 = (
            2 * precision * recall / (precision + recall)
            if (precision + recall) > 0
            else 0.0
        )
        f1_sum += f1

    return f1_sum / active_classes if active_classes > 0 else 0.0


def binary_f1(predictions: list[bool], golds: list[bool]) -> float:
    """Binary F1 for escalation (positive class = True)."""
    if not predictions and not golds:
        return 1.0

    tp = sum(1 for p, g in zip(predictions, golds, strict=True) if p and g)
    fp = sum(1 for p, g in zip(predictions, golds, strict=True) if p and not g)
    fn = sum(1 for p, g in zip(predictions, golds, strict=True) if not p and g)

    if tp + fp + fn == 0:
        return 1.0  # All true negatives — perfect agreement.

    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    return (
        2 * precision * recall / (precision + recall)
        if (precision + recall) > 0
        else 0.0
    )


def compute_aggregate_scores(
    results: list[DimensionScores],
    all_responses: list[TriageResponse],
    all_golds: list[GoldAnswer],
) -> tuple[DimensionAggregates, float]:
    """Compute submission-level aggregate scores and final classification points.

    Returns
    -------
    tuple:
        ``(dimension_aggregates, classification_score_out_of_85)``
    """
    all_categories = [c.value for c in Category]
    all_teams = [t.value for t in Team]

    cat_f1 = macro_f1(
        [r.category for r in all_responses],
        [g.category for g in all_golds],
        all_categories,
    )
    routing_f1 = macro_f1(
        [r.assigned_team for r in all_responses],
        [g.assigned_team for g in all_golds],
        all_teams,
    )
    pri_mean = (
        sum(r.priority for r in results) / len(results) if results else 0.0
    )
    miss_mean = (
        sum(r.missing_info for r in results) / len(results) if results else 0.0
    )
    esc_f1 = binary_f1(
        [_coerce_bool(r.needs_escalation) for r in all_responses],
        [g.needs_escalation for g in all_golds],
    )

    agg = DimensionAggregates(
        category=cat_f1,
        priority=pri_mean,
        routing=routing_f1,
        missing_info=miss_mean,
        escalation=esc_f1,
    )

    weighted = (
        WEIGHTS["category"] * cat_f1
        + WEIGHTS["priority"] * pri_mean
        + WEIGHTS["routing"] * routing_f1
        + WEIGHTS["missing_info"] * miss_mean
        + WEIGHTS["escalation"] * esc_f1
    )
    classification_score = (weighted / 0.85) * 85.0

    return agg, round(classification_score, 2)
