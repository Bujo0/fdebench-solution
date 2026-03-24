#!/usr/bin/env python3
"""Hackathon evaluation harness.

Scores a participant's /triage endpoint against a gold-standard dataset.
This script tests Part 1 (functional accuracy) only. Part 2 (engineering
quality) is evaluated separately after submission.

Usage:
    uv run python run_eval.py \
        --endpoint http://localhost:8000 \
        --dataset ../data/tickets/sample.json \
        --gold ../data/tickets/sample_gold.json

Math:
    Per-ticket score = weighted sum of 6 dimensions (weights sum to 1.0):
        0.15 * category  + 0.15 * priority + 0.20 * routing
      + 0.20 * missing   + 0.10 * escalation + 0.20 * remediation

    Each dimension produces a value in [0.0, 1.0].
    Final functional score = mean(per-ticket scores) * 100 → range [0, 100].

    On the leaderboard this counts as 50% of the final 0-100 score.
    The other 50% comes from engineering quality (not tested here).
"""

import argparse
import json
import sys
import time
from pathlib import Path
from urllib.parse import urljoin

import httpx

# ── Dimension weights (must sum to 1.0) ──────────────────────────────────────

WEIGHTS = {
    "category": 0.15,
    "priority": 0.15,
    "routing": 0.20,
    "missing_info": 0.20,
    "escalation": 0.10,
    "remediation": 0.20,
}

assert abs(sum(WEIGHTS.values()) - 1.0) < 1e-9, "Weights must sum to 1.0"

# ── Scoring functions ─────────────────────────────────────────────────────────


def score_category(pred: str | None, gold: str) -> float:
    """Exact match, case-insensitive. Returns 0.0 or 1.0."""
    if not pred:
        return 0.0
    return 1.0 if pred.strip().lower() == gold.strip().lower() else 0.0


def score_priority(pred: str | None, gold: str) -> float:
    """Exact match with ordinal distance penalty.

    Same level     → 1.0
    Off by 1 level → 0.67
    Off by 2       → 0.33
    Off by 3       → 0.0
    Invalid value  → 0.0
    """
    order = {"P1": 0, "P2": 1, "P3": 2, "P4": 3}
    p = order.get(pred, -1) if pred else -1
    g = order.get(gold, -1)
    if p == -1 or g == -1:
        return 0.0
    distance = abs(p - g)
    if distance == 0:
        return 1.0
    if distance == 1:
        return 0.67
    if distance == 2:
        return 0.33
    return 0.0


def score_routing(pred: str | None, gold: str) -> float:
    """Exact match, case-insensitive. Returns 0.0 or 1.0."""
    if not pred:
        return 0.0
    return 1.0 if pred.strip().lower() == gold.strip().lower() else 0.0


def score_escalation(pred: bool | None, gold: bool) -> float:
    """Binary match. Returns 0.0 or 1.0."""
    if pred is None:
        return 0.0
    return 1.0 if bool(pred) == bool(gold) else 0.0


def score_missing_info(pred_list: list[str] | None, gold_list: list[str]) -> float:
    """Set F1 score using exact string match on the constrained vocabulary.

    F1 = 2 * precision * recall / (precision + recall)

    Both empty → 1.0 (correctly identified nothing is missing).
    Gold empty, pred non-empty → 0.0 (false positives).
    Gold non-empty, pred empty → 0.0 (false negatives).
    """
    pred_set = set(s.strip().lower() for s in (pred_list or []))
    gold_set = set(s.strip().lower() for s in gold_list)

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


def score_remediation_simple(pred: dict, gold: dict) -> float:
    """Simplified remediation scoring for local eval (no LLM judge).

    Checks:
    1. Did the participant provide a next_best_action? (0.0 or 0.33)
    2. Did the participant provide remediation_steps? (0.0 or 0.33)
    3. Step count within reasonable range of gold? (0.0 or 0.34)

    This is a proxy. The hidden eval uses an LLM judge for semantic comparison.
    """
    score = 0.0

    pred_action = (pred.get("next_best_action") or "").strip()
    gold_action = (gold.get("next_best_action") or "").strip()
    if pred_action and gold_action:
        score += 0.33

    pred_steps = pred.get("remediation_steps") or []
    gold_steps = gold.get("remediation_steps") or []
    if pred_steps and gold_steps:
        score += 0.33

    if pred_steps and gold_steps:
        ratio = len(pred_steps) / len(gold_steps)
        if 0.5 <= ratio <= 2.0:
            score += 0.34

    return min(score, 1.0)


# ── Per-ticket scoring ────────────────────────────────────────────────────────


def score_ticket(pred: dict, gold: dict) -> dict[str, float]:
    """Score a single ticket prediction against gold. Returns per-dimension scores."""
    scores = {
        "category": score_category(pred.get("category"), gold["category"]),
        "priority": score_priority(pred.get("priority"), gold["priority"]),
        "routing": score_routing(pred.get("assigned_team"), gold["assigned_team"]),
        "missing_info": score_missing_info(
            pred.get("missing_information"), gold["missing_information"]
        ),
        "escalation": score_escalation(pred.get("needs_escalation"), gold["needs_escalation"]),
        "remediation": score_remediation_simple(pred, gold),
    }
    scores["weighted_total"] = sum(scores[k] * WEIGHTS[k] for k in WEIGHTS)
    return scores


# ── HTTP client ───────────────────────────────────────────────────────────────


def call_endpoint(client: httpx.Client, endpoint: str, ticket: dict) -> dict | None:
    """POST a ticket to the /triage endpoint. Returns parsed JSON or None on error."""
    url = urljoin(endpoint.rstrip("/") + "/", "triage")
    try:
        resp = client.post(url, json=ticket, timeout=30.0)
        resp.raise_for_status()
        return resp.json()
    except Exception as e:
        print(f"  ✗ {ticket['ticket_id']}: {e}")
        return None


def check_health(client: httpx.Client, endpoint: str) -> bool:
    """GET /health and check for 200."""
    url = urljoin(endpoint.rstrip("/") + "/", "health")
    try:
        resp = client.get(url, timeout=10.0)
        return resp.status_code == 200
    except Exception:
        return False


# ── Main ──────────────────────────────────────────────────────────────────────


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Score a /triage endpoint against gold-standard ticket data."
    )
    parser.add_argument(
        "--endpoint",
        required=True,
        help="Base URL of the service (e.g., http://localhost:8000)",
    )
    parser.add_argument(
        "--dataset",
        required=True,
        help="Path to the ticket dataset JSON file",
    )
    parser.add_argument(
        "--gold",
        default=None,
        help="Path to the gold answers JSON file. If not provided, "
        "looks for a file named <dataset>_gold.json next to the dataset, "
        "or sample_gold.json if dataset is sample.json.",
    )
    args = parser.parse_args()

    # ── Load data ─────────────────────────────────────────────────────────
    dataset_path = Path(args.dataset)
    if not dataset_path.exists():
        print(f"Error: dataset file not found: {dataset_path}")
        return 1

    tickets = json.loads(dataset_path.read_text())

    # Resolve gold file
    if args.gold:
        gold_path = Path(args.gold)
    else:
        # Convention: sample.json → sample_gold.json
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

    # Validate ticket/gold alignment
    ticket_ids = [t["ticket_id"] for t in tickets]
    gold_ids = set(gold_by_id.keys())
    missing_gold = [tid for tid in ticket_ids if tid not in gold_ids]
    if missing_gold:
        print(f"Error: {len(missing_gold)} tickets have no gold answer: {missing_gold[:5]}")
        return 1

    print(f"Loaded {len(tickets)} tickets, {len(golds)} gold answers")
    print(f"Endpoint: {args.endpoint}")
    print()

    # ── Health check ──────────────────────────────────────────────────────
    client = httpx.Client()
    healthy = check_health(client, args.endpoint)
    print(f"Health check: {'✓ OK' if healthy else '✗ FAILED'}")
    if not healthy:
        print("Warning: GET /health did not return 200. Continuing with scoring...")
    print()

    # ── Score each ticket ─────────────────────────────────────────────────
    results: list[dict] = []
    latencies: list[float] = []
    errors = 0

    for ticket in tickets:
        tid = ticket["ticket_id"]
        gold = gold_by_id[tid]

        start = time.monotonic()
        pred = call_endpoint(client, args.endpoint, ticket)
        elapsed_ms = (time.monotonic() - start) * 1000
        latencies.append(elapsed_ms)

        if pred is None:
            errors += 1
            results.append({"ticket_id": tid, "weighted_total": 0.0, "error": True})
            continue

        scores = score_ticket(pred, gold)
        scores["ticket_id"] = tid
        scores["latency_ms"] = round(elapsed_ms, 0)
        results.append(scores)

        # Per-ticket output
        marks = {
            k: "✓" if scores[k] >= 0.99 else ("~" if scores[k] >= 0.5 else "✗")
            for k in WEIGHTS
        }
        print(
            f"  {tid}  [{scores['weighted_total']*100:5.1f}]  "
            f"cat={marks['category']} pri={marks['priority']} "
            f"route={marks['routing']} esc={marks['escalation']} "
            f"miss={marks['missing_info']}({scores['missing_info']:.2f}) "
            f"rem={scores['remediation']:.2f}  "
            f"{elapsed_ms:.0f}ms"
        )

    client.close()

    # ── Aggregate ─────────────────────────────────────────────────────────
    valid = [r for r in results if not r.get("error")]
    n_total = len(tickets)
    n_valid = len(valid)
    n_errors = errors

    if not valid:
        print("\nNo valid responses received. Score: 0.0")
        return 1

    # Per-dimension averages
    dim_avgs = {}
    for dim in WEIGHTS:
        dim_avgs[dim] = sum(r[dim] for r in valid) / n_valid

    # Functional score: mean of per-ticket weighted totals, scaled to 0-100
    functional_score = sum(r["weighted_total"] for r in valid) / n_valid * 100

    # Latency stats
    sorted_latencies = sorted(latencies)
    p50 = sorted_latencies[len(sorted_latencies) // 2]
    p95_idx = min(int(len(sorted_latencies) * 0.95), len(sorted_latencies) - 1)
    p95 = sorted_latencies[p95_idx]

    # ── Print results ─────────────────────────────────────────────────────
    print()
    print("=" * 60)
    print(f"  FUNCTIONAL SCORE (Part 1 of final leaderboard)")
    print("=" * 60)
    print()
    for dim in WEIGHTS:
        pct = dim_avgs[dim] * 100
        weight_pct = WEIGHTS[dim] * 100
        contribution = dim_avgs[dim] * WEIGHTS[dim] * 100
        print(f"  {dim:<16s}  {pct:5.1f}% accuracy  × {weight_pct:.0f}% weight  = {contribution:5.2f} pts")
    print(f"  {'─' * 54}")
    print(f"  {'FUNCTIONAL':16s}  {functional_score:5.1f} / 100")
    print()
    print(f"  Tickets scored: {n_valid}/{n_total}")
    if n_errors:
        print(f"  Errors (scored as 0): {n_errors}")
    print(f"  Latency p50: {p50:.0f}ms  p95: {p95:.0f}ms")
    print()
    print("  ┌─────────────────────────────────────────────────┐")
    print(f"  │  This score counts as 50% of your final score.  │")
    print(f"  │  Engineering quality (50%) is evaluated after    │")
    print(f"  │  submission on your repo and documentation.      │")
    print("  └─────────────────────────────────────────────────┘")
    print()

    # ── Write JSON results ────────────────────────────────────────────────
    output = {
        "functional_score": round(functional_score, 2),
        "tickets_scored": n_valid,
        "tickets_total": n_total,
        "tickets_errored": n_errors,
        "dimension_averages": {k: round(v, 4) for k, v in dim_avgs.items()},
        "weights": WEIGHTS,
        "latency_p50_ms": round(p50, 0),
        "latency_p95_ms": round(p95, 0),
        "per_ticket": [
            {k: v for k, v in r.items() if k != "error"} for r in results
        ],
    }
    output_path = Path("eval_results.json")
    output_path.write_text(json.dumps(output, indent=2) + "\n")
    print(f"  Results saved to {output_path}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
