#!/usr/bin/env python3
"""🛰️ Contoso Deep Space Station — Evaluation Harness 🛰️

Scores a participant's /triage endpoint against gold-standard signal data.
This script tests Part 1 (functional accuracy) only. Part 2 (engineering
quality) is evaluated separately after submission.

Usage:
    uv run python run_eval.py \
        --endpoint http://localhost:8000 \
        --dataset ../data/tickets/sample.json \
        --gold ../data/tickets/sample_gold.json

Architecture:
    The scoring computer evaluates your submission on 7 dimensions:

    5 classification dimensions (max 85 pts total):
        0.20 × category      — macro F1 across 8 anomaly types
        0.20 × priority      — mean ordinal partial credit (P1–P4)
        0.20 × routing       — macro F1 across 7 response divisions
        0.15 × missing_info  — mean per-signal set F1
        0.10 × escalation    — binary F1 on the positive class

    2 efficiency dimensions (max 15 pts total):
        0.10 × latency       — normalized p50 response time
        0.05 × cost          — normalized $/signal from token usage

    Total = classification (0–85) + efficiency (0–15) = 0–100.

    Why macro F1 instead of accuracy:
        Accuracy lets a system game the score by always predicting the
        most common anomaly type — like classifying every signal as
        "Mission Briefing Request" and whistling past the hull breaches.
        Macro F1 computes F1 per class then averages, so every anomaly
        type matters equally regardless of frequency.

    On the leaderboard this counts as 50% of the final 0-100 score.
    The other 50% comes from engineering quality (evaluated after submission).

    Note: remediation_steps and next_best_action are still required in
    your API response (they are part of the output schema), but they are
    not deterministically scored. Quality of remediation is evaluated as
    part of the engineering quality assessment.

    Efficiency scoring: To participate in latency and cost scoring, your
    API should return these response headers:
        X-Model-Name:         model name (e.g., "gpt-4o-mini")
        X-Prompt-Tokens:      integer token count
        X-Completion-Tokens:  integer token count
    These are optional — missing headers result in default cost scoring.
"""

import argparse
import json
import sys
import time
from collections.abc import Sequence
from pathlib import Path
from urllib.parse import urljoin

import httpx

# ── Dimension weights ────────────────────────────────────────────────
# Classification weights sum to 0.85.
# Remaining 0.15 is efficiency (latency + cost), scored by the platform.

WEIGHT_CATEGORY = 0.20
WEIGHT_PRIORITY = 0.20
WEIGHT_ROUTING = 0.20
WEIGHT_MISSING_INFO = 0.15
WEIGHT_ESCALATION = 0.10

# Efficiency (informational only in local eval)
WEIGHT_LATENCY = 0.10
WEIGHT_COST = 0.05

_CLASSIFICATION_WEIGHT_SUM = (
    WEIGHT_CATEGORY + WEIGHT_PRIORITY + WEIGHT_ROUTING + WEIGHT_MISSING_INFO + WEIGHT_ESCALATION
)

WEIGHTS = {
    "category": WEIGHT_CATEGORY,
    "priority": WEIGHT_PRIORITY,
    "routing": WEIGHT_ROUTING,
    "missing_info": WEIGHT_MISSING_INFO,
    "escalation": WEIGHT_ESCALATION,
}

# ── Closed label sets (must match the platform) ─────────────────────

CATEGORIES = (
    "Crew Access & Biometrics",
    "Hull & Structural Systems",
    "Communications & Navigation",
    "Flight Software & Instruments",
    "Threat Detection & Containment",
    "Telemetry & Data Banks",
    "Mission Briefing Request",
    "Not a Mission Signal",
)

TEAMS = (
    "Crew Identity & Airlock Control",
    "Spacecraft Systems Engineering",
    "Deep Space Communications",
    "Mission Software Operations",
    "Threat Response Command",
    "Telemetry & Data Core",
    "None",
)


def _normalize(text: str) -> str:
    """Lowercase and strip for case-insensitive comparison."""
    return text.strip().lower()


def _coerce_bool(value: object) -> bool:
    """Safely coerce a value to boolean.

    Handles string representations like "true"/"false" that participants
    may return from their API. Python's bool("false") is True, so we
    need explicit string handling.
    """
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().lower() in {"true", "1", "yes"}
    if isinstance(value, int):
        return value != 0
    return False


# ── Submission-level aggregate metrics ───────────────────────────────


def macro_f1(
    candidates: Sequence[str],
    golds: Sequence[str],
    label_set: Sequence[str],
) -> float:
    """Macro-averaged F1 over a closed set of class labels.

    Computes per-class precision, recall, and F1, then averages F1 across
    all classes that appear in either golds or candidates. Classes absent
    from both are excluded from the average.
    """
    candidate_norm = [_normalize(c) for c in candidates]
    gold_norm = [_normalize(g) for g in golds]
    label_norm = [_normalize(label) for label in label_set]

    f1_scores: list[float] = []
    for label in label_norm:
        tp = sum(1 for c, g in zip(candidate_norm, gold_norm, strict=False) if c == label and g == label)
        fp = sum(1 for c, g in zip(candidate_norm, gold_norm, strict=False) if c == label and g != label)
        fn = sum(1 for c, g in zip(candidate_norm, gold_norm, strict=False) if c != label and g == label)

        if tp + fp + fn == 0:
            continue

        precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
        f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0.0
        f1_scores.append(f1)

    return sum(f1_scores) / len(f1_scores) if f1_scores else 0.0


def binary_f1(candidates: Sequence[bool], golds: Sequence[bool]) -> float:
    """F1 for the positive class (True) in binary classification.

    Returns 1.0 when there are no positive cases in either gold or
    predictions (perfect agreement on absence).
    """
    tp = sum(1 for c, g in zip(candidates, golds, strict=False) if c and g)
    fp = sum(1 for c, g in zip(candidates, golds, strict=False) if c and not g)
    fn = sum(1 for c, g in zip(candidates, golds, strict=False) if not c and g)

    if tp + fp + fn == 0:
        return 1.0

    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0

    if precision + recall == 0:
        return 0.0
    return 2 * precision * recall / (precision + recall)


# ── Per-ticket scoring functions ─────────────────────────────────────


def score_category(pred: str | None, gold: str) -> float:
    """Exact match, case-insensitive. Returns 0.0 or 1.0."""
    if not pred:
        return 0.0
    return 1.0 if _normalize(pred) == _normalize(gold) else 0.0


def score_priority(pred: str | None, gold: str) -> float:
    """Priority match with partial credit for off-by-one only.

    Same level     → 1.0
    Off by 1 level → 0.67
    Off by 2+      → 0.0
    Invalid value  → 0.0
    """
    order = {"P1": 0, "P2": 1, "P3": 2, "P4": 3}
    p = order.get(pred.strip().upper() if pred else "", -1)
    g = order.get(gold.strip().upper(), -1)
    if p == -1 or g == -1:
        return 0.0
    distance = abs(p - g)
    if distance == 0:
        return 1.0
    if distance == 1:
        return 0.67
    return 0.0


def score_routing(pred: str | None, gold: str) -> float:
    """Exact match, case-insensitive. Returns 0.0 or 1.0."""
    if not pred:
        return 0.0
    return 1.0 if _normalize(pred) == _normalize(gold) else 0.0


def score_escalation(pred: bool | None, gold: bool) -> float:
    """Binary match. Returns 0.0 or 1.0."""
    if pred is None:
        return 0.0
    return 1.0 if bool(pred) == bool(gold) else 0.0


def score_missing_info(pred_list: list[str] | None, gold_list: list[str]) -> float:
    """Set F1 score using exact string match on the constrained vocabulary.

    F1 = 2 × precision × recall / (precision + recall)

    Both empty → 1.0 (correctly identified nothing is missing).
    Gold empty, pred non-empty → 0.0 (false positives).
    Gold non-empty, pred empty → 0.0 (false negatives).
    """
    pred_set = {_normalize(s) for s in (pred_list or [])}
    gold_set = {_normalize(s) for s in gold_list}

    if not gold_set and not pred_set:
        return 1.0
    if not gold_set or not pred_set:
        return 0.0

    true_positives = len(pred_set & gold_set)
    precision = true_positives / len(pred_set)
    recall = true_positives / len(gold_set)

    if precision + recall == 0:
        return 0.0
    return 2.0 * precision * recall / (precision + recall)


# ── Per-ticket scoring ────────────────────────────────────────────────


def score_ticket(pred: dict, gold: dict) -> dict[str, float]:
    """Score a single signal prediction against gold. Returns per-dimension scores.

    Note: the submission-level score uses macro F1 for category and routing,
    and binary F1 for escalation. The per-signal total here is an
    approximation useful for identifying which specific signals were wrong.
    """
    cat = score_category(pred.get("category"), gold["category"])
    pri = score_priority(pred.get("priority"), gold["priority"])
    rte = score_routing(pred.get("assigned_team"), gold["assigned_team"])

    pred_missing = pred.get("missing_information")
    miss = score_missing_info(
        pred_missing if isinstance(pred_missing, list) else [],
        gold["missing_information"],
    )

    pred_esc = pred.get("needs_escalation")
    esc = score_escalation(
        _coerce_bool(pred_esc) if pred_esc is not None else None,
        gold["needs_escalation"],
    )

    scores = {
        "category": cat,
        "priority": pri,
        "routing": rte,
        "missing_info": miss,
        "escalation": esc,
    }
    scores["weighted_total"] = sum(scores[k] * WEIGHTS[k] for k in WEIGHTS)
    return scores


# ── Submission-level scoring ──────────────────────────────────────────


def score_submission(
    candidate_responses: list[dict],
    gold_answers: list[dict],
) -> dict:
    """Score a full submission using the same metrics as the platform.

    Dimension scoring methods (submission level):
      - category:     macro F1 across 8 anomaly type labels
      - priority:     mean per-signal ordinal partial credit
      - routing:      macro F1 across 7 response division labels
      - missing_info: mean per-signal set F1
      - escalation:   binary F1 on the positive class

    Returns dict with classification_score (0–85), dimension breakdowns,
    and per-signal details.
    """
    per_ticket: list[dict[str, float]] = []

    all_cat_cands: list[str] = []
    all_cat_golds: list[str] = []
    all_rte_cands: list[str] = []
    all_rte_golds: list[str] = []
    all_esc_cands: list[bool] = []
    all_esc_golds: list[bool] = []
    all_pri_scores: list[float] = []
    all_miss_scores: list[float] = []

    cand_by_id = {str(c.get("ticket_id", "")): c for c in candidate_responses}
    errors: list[str] = []

    for gold in gold_answers:
        tid = str(gold["ticket_id"])
        cand = cand_by_id.get(tid)

        if cand is None:
            errors.append(f"Missing response for signal {tid}")
            per_ticket.append({k: 0.0 for k in [*WEIGHTS, "weighted_total"]})
            all_cat_cands.append("")
            all_cat_golds.append(_normalize(str(gold.get("category", ""))))
            all_rte_cands.append("")
            all_rte_golds.append(_normalize(str(gold.get("assigned_team", ""))))
            all_esc_cands.append(False)
            all_esc_golds.append(_coerce_bool(gold.get("needs_escalation")))
            all_pri_scores.append(0.0)
            all_miss_scores.append(0.0)
        else:
            ticket_result = score_ticket(cand, gold)
            per_ticket.append(ticket_result)

            all_cat_cands.append(_normalize(str(cand.get("category", ""))))
            all_cat_golds.append(_normalize(str(gold.get("category", ""))))
            all_rte_cands.append(_normalize(str(cand.get("assigned_team", ""))))
            all_rte_golds.append(_normalize(str(gold.get("assigned_team", ""))))
            all_esc_cands.append(_coerce_bool(cand.get("needs_escalation")))
            all_esc_golds.append(_coerce_bool(gold.get("needs_escalation")))
            all_pri_scores.append(ticket_result["priority"])
            all_miss_scores.append(ticket_result["missing_info"])

    n = len(per_ticket)

    # Submission-level dimension scores
    category_score = macro_f1(all_cat_cands, all_cat_golds, CATEGORIES)
    priority_score = sum(all_pri_scores) / n if n > 0 else 0.0
    routing_score = macro_f1(all_rte_cands, all_rte_golds, TEAMS)
    missing_info_score = sum(all_miss_scores) / n if n > 0 else 0.0
    escalation_score = binary_f1(all_esc_cands, all_esc_golds)

    weighted_total = (
        WEIGHT_CATEGORY * category_score
        + WEIGHT_PRIORITY * priority_score
        + WEIGHT_ROUTING * routing_score
        + WEIGHT_MISSING_INFO * missing_info_score
        + WEIGHT_ESCALATION * escalation_score
    )

    classification_score = round(weighted_total / _CLASSIFICATION_WEIGHT_SUM * 85, 1)

    return {
        "classification_score": classification_score,
        "dimension_scores": {
            "category": round(category_score, 4),
            "priority": round(priority_score, 4),
            "routing": round(routing_score, 4),
            "missing_info": round(missing_info_score, 4),
            "escalation": round(escalation_score, 4),
        },
        "tickets_scored": n - len(errors),
        "tickets_errored": len(errors),
        "per_ticket": per_ticket,
        "errors": errors,
    }


# ── HTTP client ───────────────────────────────────────────────────────


def call_endpoint(client: httpx.Client, endpoint: str, ticket: dict) -> tuple[dict | None, float]:
    """POST a signal to /triage. Returns (parsed JSON or None, latency_ms)."""
    url = urljoin(endpoint.rstrip("/") + "/", "triage")
    start = time.monotonic()
    try:
        resp = client.post(url, json=ticket, timeout=30.0)
        elapsed_ms = (time.monotonic() - start) * 1000
        resp.raise_for_status()
        return resp.json(), elapsed_ms
    except Exception as e:
        elapsed_ms = (time.monotonic() - start) * 1000
        print(f"  ✗ {ticket['ticket_id']}: {e}")
        return None, elapsed_ms


def check_health(client: httpx.Client, endpoint: str) -> bool:
    """GET /health and check for 200."""
    url = urljoin(endpoint.rstrip("/") + "/", "health")
    try:
        resp = client.get(url, timeout=10.0)
        return resp.status_code == 200
    except Exception:
        return False


# ── Main ──────────────────────────────────────────────────────────────


def main() -> int:
    parser = argparse.ArgumentParser(description="Score a /triage endpoint against gold-standard signal data.")
    parser.add_argument(
        "--endpoint",
        required=True,
        help="Base URL of the service (e.g., http://localhost:8000)",
    )
    parser.add_argument(
        "--dataset",
        required=True,
        help="Path to the signal dataset JSON file",
    )
    parser.add_argument(
        "--gold",
        default=None,
        help="Path to the gold answers JSON file. If not provided, "
        "looks for a file named <dataset>_gold.json next to the dataset.",
    )
    args = parser.parse_args()

    # ── Load data ─────────────────────────────────────────────────────
    dataset_path = Path(args.dataset)
    if not dataset_path.exists():
        print(f"Error: dataset file not found: {dataset_path}")
        return 1

    tickets = json.loads(dataset_path.read_text())

    # Resolve gold file
    if args.gold:
        gold_path = Path(args.gold)
    else:
        stem = dataset_path.stem
        gold_path = dataset_path.parent / f"{stem}_gold.json"
        if not gold_path.exists():
            print(f"Error: gold file not found: {gold_path}")
            print("Provide --gold explicitly or ensure <dataset>_gold.json exists.")
            return 1

    if not gold_path.exists():
        print(f"Error: gold file not found: {gold_path}")
        return 1

    golds = json.loads(gold_path.read_text())
    gold_by_id = {g["ticket_id"]: g for g in golds}

    # Validate signal/gold alignment
    ticket_ids = [t["ticket_id"] for t in tickets]
    gold_ids = set(gold_by_id.keys())
    missing_gold = [tid for tid in ticket_ids if tid not in gold_ids]
    if missing_gold:
        print(f"Error: {len(missing_gold)} signals have no gold answer: {missing_gold[:5]}")
        return 1

    print(f"Loaded {len(tickets)} signals, {len(golds)} gold answers")
    print(f"Endpoint: {args.endpoint}")
    print()

    # ── Health check ──────────────────────────────────────────────────
    client = httpx.Client()
    healthy = check_health(client, args.endpoint)
    print(f"Health check: {'✓ OK' if healthy else '✗ FAILED'}")
    if not healthy:
        print("Warning: GET /health did not return 200. Continuing with scoring...")
    print()

    # ── Score each ticket ─────────────────────────────────────────────
    results: list[dict] = []
    responses: list[dict] = []
    latencies: list[float] = []
    errors = 0

    for ticket in tickets:
        tid = ticket["ticket_id"]
        gold = gold_by_id[tid]

        pred, elapsed_ms = call_endpoint(client, args.endpoint, ticket)
        latencies.append(elapsed_ms)

        if pred is None:
            errors += 1
            results.append({"ticket_id": tid, "weighted_total": 0.0, "error": True})
            responses.append({"ticket_id": tid})
            continue

        responses.append(pred)
        scores = score_ticket(pred, gold)
        scores["ticket_id"] = tid
        scores["latency_ms"] = round(elapsed_ms, 0)
        results.append(scores)

        # Per-ticket output
        marks = {k: "✓" if scores[k] >= 0.99 else ("~" if scores[k] >= 0.5 else "✗") for k in WEIGHTS}
        print(
            f"  {tid}  [{scores['weighted_total'] * 100:5.1f}]  "
            f"cat={marks['category']} pri={marks['priority']} "
            f"route={marks['routing']} esc={marks['escalation']} "
            f"miss={marks['missing_info']}({scores['missing_info']:.2f})  "
            f"{elapsed_ms:.0f}ms"
        )

    client.close()

    # ── Submission-level aggregate scoring ────────────────────────────
    sub_result = score_submission(responses, golds)
    dim_scores = sub_result["dimension_scores"]
    classification_score = sub_result["classification_score"]

    n_total = len(tickets)
    n_valid = n_total - errors

    # Latency stats
    sorted_latencies = sorted(latencies)
    p50 = sorted_latencies[len(sorted_latencies) // 2] if sorted_latencies else 0
    p95_idx = min(int(len(sorted_latencies) * 0.95), len(sorted_latencies) - 1) if sorted_latencies else 0
    p95 = sorted_latencies[p95_idx] if sorted_latencies else 0

    # ── Print results ─────────────────────────────────────────────────
    print()
    print("=" * 60)
    print("  FUNCTIONAL SCORE (Part 1 of final leaderboard)")
    print("=" * 60)
    print()
    print("  Classification dimensions (max 85 pts):")
    print()
    for dim, weight in WEIGHTS.items():
        score = dim_scores[dim]
        pts = score * weight / _CLASSIFICATION_WEIGHT_SUM * 85
        method = "macro F1" if dim in ("category", "routing") else ("binary F1" if dim == "escalation" else "mean")
        print(f"    {dim:<16s}  {score:.4f} ({method})  × {weight * 100:.0f}% weight  = {pts:5.2f} pts")
    print(f"    {'─' * 52}")
    print(f"    {'CLASSIFICATION':16s}  {classification_score:5.1f} / 85")
    print()
    print("  Efficiency dimensions (max 15 pts, scored by platform):")
    print()
    print(f"    latency           p50={p50:.0f}ms  p95={p95:.0f}ms  (10% weight)")
    print("    cost              from response headers     (5% weight)")
    print()
    print(f"  Signals scored: {n_valid}/{n_total}")
    if errors:
        print(f"  Errors (scored as 0): {errors}")
    print()
    print("  ┌─────────────────────────────────────────────────────────┐")
    print("  │  Classification score: up to 85 pts from 5 dimensions  │")
    print("  │  Efficiency score: up to 15 pts (latency + cost)       │")
    print("  │  Total functional score: 0–100 (50% of leaderboard)    │")
    print("  │  Engineering quality: 50% of leaderboard               │")
    print("  └─────────────────────────────────────────────────────────┘")
    print()

    # ── Write JSON results ────────────────────────────────────────────
    output = {
        "classification_score": classification_score,
        "dimension_scores": dim_scores,
        "tickets_scored": n_valid,
        "tickets_total": n_total,
        "tickets_errored": errors,
        "latency_p50_ms": round(p50, 0),
        "latency_p95_ms": round(p95, 0),
        "per_ticket": [{k: v for k, v in r.items() if k != "error"} for r in results],
    }
    output_path = Path("eval_results.json")
    output_path.write_text(json.dumps(output, indent=2) + "\n")
    print(f"  Results saved to {output_path}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
