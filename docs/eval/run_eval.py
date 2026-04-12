#!/usr/bin/env python3
"""🛰️ CONTOSO DEEP SPACE STATION — SCORING COMPUTER 🛰️
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

    "The scoring computer doesn't care about your feelings.
     It doesn't care about your excuses. It doesn't care that
     the LLM was 'pretty close.' Space doesn't grade on a curve."
                                        — Admiral Chen, CDSS

Evaluation harness for Signal Triage — the same cold, unforgiving
math the platform uses to score your submission. Run it locally.
See exactly how you'll be scored. No surprises on launch day.

Usage:
    uv run python run_eval.py \\
        --endpoint http://localhost:8000 \\
        --dataset ../data/signals/sample.json \\
        --gold ../data/signals/sample_gold.json

Architecture:
    The scoring computer evaluates your submission on 7 dimensions:

    5 classification dimensions (max 85 pts total):
        0.20 × category      — macro F1 across 8 anomaly categories
        0.20 × priority      — mean ordinal partial credit (P1–P4)
        0.20 × routing       — macro F1 across 7 response divisions
        0.15 × missing_info  — mean per-signal set F1
        0.10 × escalation    — binary F1 on the positive class

    2 efficiency dimensions (max 15 pts total):
        0.10 × latency       — normalized p50 response time
        0.05 × cost          — normalized $/signal from token usage

    Total = classification (0–85) + efficiency (0–15) = 0–100.

    Why macro F1 instead of accuracy:
        Accuracy is gameable — always predicting the most common class
        gets you high accuracy while the crew dies from an unrouted hull
        breach. Macro F1 computes F1 per class then averages, so every
        anomaly type matters equally. A system that ignores rare-but-critical
        classes (e.g., "Threat Detection & Containment") gets a score as
        cold as the void outside.

    On the leaderboard this counts as 50% of the final 0-100 score.
    The other 50% comes from engineering quality (evaluated after submission).

    Note: remediation_steps and next_best_action are still required in
    your API response (they are part of the output schema), but they are
    not deterministically scored. Quality of remediation is evaluated as
    part of the engineering quality assessment — because a system that says
    "investigate the anomaly" for every signal is telling us you phoned it
    in from a comfortable 1 AU away.

    Efficiency scoring: To participate in latency and cost scoring, your
    API should return these response headers:
        X-Model-Name:         model name (e.g., "gpt-4o-mini")
        X-Prompt-Tokens:      integer token count
        X-Completion-Tokens:  integer token count
    These are optional — missing headers result in worst-case cost scoring.
    (As if you're burning GPT-4 with zero caching. The Admiral will have
    questions about your fuel budget.)
"""

import argparse
import json
import re
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


def _normalize(text: str | None) -> str:
    """Lowercase, collapse whitespace, strip punctuation edges.

    Matches the platform's normalize_text behavior so local eval scores
    are consistent with the official scoring computer. Returns empty
    string for None input — because the void returns nothing.
    """
    if text is None:
        return ""
    text = str(text).strip().lower()
    text = re.sub(r"\s+", " ", text)
    return text.strip(" .;:,")


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


# ── Per-signal scoring functions ──────────────────────────────────────
# Each function scores one dimension for one signal. Think of it as
# the black-box recorder for each individual triage decision.


def score_category(pred: str | None, gold: str) -> float:
    """Per-signal anomaly category match (0.0 or 1.0).

    Misclassify and the wrong division scrambles — Threat Response Command
    arrives at a fabricator jam while an actual hull breach goes unattended.
    Congratulations, you've invented a new way to fail.
    """
    return 1.0 if _normalize(pred) == _normalize(gold) else 0.0


def score_priority(pred: str | None, gold: str) -> float:
    """Priority match with partial credit — because "close" only counts in asteroid dodging.

    Returns:
        1.0  — exact match (correct threat assessment, gold star, the crew lives)
        0.67 — off by one level (wrong, but you're in the right solar system)
        0.0  — off by two or more levels, or invalid (you called a hull breach
               "routine" and now there's a new window in Deck 7 that wasn't
               in the blueprints)
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
    """Route-to-team match — send a signal to the wrong division and watch
    chaos unfold in zero gravity. Case-insensitive exact match. 0.0 or 1.0.
    """
    return 1.0 if _normalize(pred) == _normalize(gold) else 0.0


def score_escalation(pred: bool | None, gold: bool) -> float:
    """Escalation flag — did you correctly decide whether to wake up the
    Station Commander at 0300 hours? Binary match. 0.0 or 1.0.
    """
    if pred is None:
        return 0.0
    return 1.0 if bool(pred) == bool(gold) else 0.0


def score_missing_info(pred_list: list[str] | None, gold_list: list[str]) -> float:
    """Missing intel F1 — did you identify which sensor readings, crew data,
    or system diagnostics are still needed before the signal can be resolved?

    Uses set-based F1 over the constrained vocabulary.

    Both empty → 1.0 (signal is self-contained — proceed to fix).
    Gold empty, pred non-empty → 0.0 (you're hallucinating missing data).
    Gold non-empty, pred empty → 0.0 (you missed critical gaps).
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


# ── Per-signal scoring ────────────────────────────────────────────────


def score_signal(pred: dict, gold: dict) -> dict[str, float]:
    """Score a single signal prediction against gold. Returns per-dimension scores.

    Note: the submission-level score uses macro F1 for category and routing,
    and binary F1 for escalation. The per-signal total here is an
    approximation useful for identifying which specific signals went sideways.
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
      - category:     macro F1 across 8 anomaly-category labels
      - priority:     mean per-signal ordinal partial credit
      - routing:      macro F1 across 7 division labels
      - missing_info: mean per-signal set F1
      - escalation:   binary F1 on the positive class

    Returns dict with classification_score (0–85), dimension breakdowns,
    and per-signal details.
    """
    if not gold_answers:
        msg = "Gold answer set is empty"
        raise ValueError(msg)

    per_signal: list[dict[str, float]] = []

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
            per_signal.append({k: 0.0 for k in [*WEIGHTS, "weighted_total"]})
            all_cat_cands.append("")
            all_cat_golds.append(_normalize(str(gold.get("category", ""))))
            all_rte_cands.append("")
            all_rte_golds.append(_normalize(str(gold.get("assigned_team", ""))))
            all_esc_cands.append(False)
            all_esc_golds.append(_coerce_bool(gold.get("needs_escalation")))
            all_pri_scores.append(0.0)
            all_miss_scores.append(0.0)
        else:
            signal_result = score_signal(cand, gold)
            per_signal.append(signal_result)

            all_cat_cands.append(_normalize(str(cand.get("category", ""))))
            all_cat_golds.append(_normalize(str(gold.get("category", ""))))
            all_rte_cands.append(_normalize(str(cand.get("assigned_team", ""))))
            all_rte_golds.append(_normalize(str(gold.get("assigned_team", ""))))
            all_esc_cands.append(_coerce_bool(cand.get("needs_escalation")))
            all_esc_golds.append(_coerce_bool(gold.get("needs_escalation")))
            all_pri_scores.append(signal_result["priority"])
            all_miss_scores.append(signal_result["missing_info"])

    n = len(per_signal)

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
        "signals_scored": n - len(errors),
        "signals_errored": len(errors),
        "per_signal": per_signal,
        "errors": errors,
    }


# ── HTTP client ───────────────────────────────────────────────────────


def call_endpoint(client: httpx.Client, endpoint: str, signal: dict) -> tuple[dict | None, float]:
    """POST a signal to /triage. Returns (parsed JSON or None, latency_ms)."""
    url = urljoin(endpoint.rstrip("/") + "/", "triage")
    start = time.monotonic()
    try:
        resp = client.post(url, json=signal, timeout=30.0)
        elapsed_ms = (time.monotonic() - start) * 1000
        resp.raise_for_status()
        return resp.json(), elapsed_ms
    except Exception as e:
        elapsed_ms = (time.monotonic() - start) * 1000
        print(f"  ✗ {signal['ticket_id']}: SIGNAL LOST TO THE VOID — {e}")
        return None, elapsed_ms


def check_health(client: httpx.Client, endpoint: str) -> bool:
    """GET /health — life-signs check. If the service has no pulse, we can't score it."""
    url = urljoin(endpoint.rstrip("/") + "/", "health")
    try:
        resp = client.get(url, timeout=10.0)
        return resp.status_code == 200
    except Exception:
        return False


# ── Main ──────────────────────────────────────────────────────────────


def main() -> int:
    parser = argparse.ArgumentParser(
        description="🛰️ CDSS Scoring Computer — score a /triage endpoint against gold-standard signal data.",
    )
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
        print(f"  ✗ Signal archive not found: {dataset_path}")
        return 1

    signals = json.loads(dataset_path.read_text())

    # Resolve gold file
    if args.gold:
        gold_path = Path(args.gold)
    else:
        stem = dataset_path.stem
        gold_path = dataset_path.parent / f"{stem}_gold.json"
        if not gold_path.exists():
            print(f"  ✗ Gold answer archive not found: {gold_path}")
            print("  Provide --gold explicitly or ensure <dataset>_gold.json exists.")
            return 1

    if not gold_path.exists():
        print(f"  ✗ Gold answer archive not found: {gold_path}")
        return 1

    golds = json.loads(gold_path.read_text())
    gold_by_id = {g["ticket_id"]: g for g in golds}

    # Validate signal/gold alignment
    signal_ids = [t["ticket_id"] for t in signals]
    gold_ids = set(gold_by_id.keys())
    missing_gold = [tid for tid in signal_ids if tid not in gold_ids]
    if missing_gold:
        print(f"  ✗ {len(missing_gold)} signals missing gold answers: {missing_gold[:5]}")
        return 1

    print()
    print("  🛰️  CONTOSO DEEP SPACE STATION — SCORING COMPUTER  🛰️")
    print("  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print()
    print(f"  Incoming signals:  {len(signals)}")
    print(f"  Gold answers:      {len(golds)}")
    print(f"  Target endpoint:   {args.endpoint}")
    print()

    # ── Health check ──────────────────────────────────────────────────
    client = httpx.Client()
    healthy = check_health(client, args.endpoint)
    if healthy:
        status = "✓ LIFE SIGNS DETECTED — the station breathes"
    else:
        status = "✗ NO LIFE SIGNS — FLATLINE — check the reactor"
    print(f"  Health check: {status}")
    if not healthy:
        print("  ⚠ Warning: GET /health did not return 200. Proceeding with scoring anyway...")
        print("  (The scoring computer is brave. Or indifferent. Same thing in space.)")
    print()

    # ── Score each signal ─────────────────────────────────────────────
    print("  Transmitting signals to triage endpoint... stand by for contact.")
    print()
    results: list[dict] = []
    responses: list[dict] = []
    latencies: list[float] = []
    errors = 0

    for signal in signals:
        tid = signal["ticket_id"]
        gold = gold_by_id[tid]

        pred, elapsed_ms = call_endpoint(client, args.endpoint, signal)
        latencies.append(elapsed_ms)

        if pred is None:
            errors += 1
            results.append({"ticket_id": tid, "weighted_total": 0.0, "error": True})
            responses.append({"ticket_id": tid})
            continue

        responses.append(pred)
        scores = score_signal(pred, gold)
        scores["ticket_id"] = tid
        scores["latency_ms"] = round(elapsed_ms, 0)
        results.append(scores)

        # Per-signal output
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

    n_total = len(signals)
    n_valid = n_total - errors

    # Latency stats
    sorted_latencies = sorted(latencies)
    p50 = sorted_latencies[len(sorted_latencies) // 2] if sorted_latencies else 0
    p95_idx = min(int(len(sorted_latencies) * 0.95), len(sorted_latencies) - 1) if sorted_latencies else 0
    p95 = sorted_latencies[p95_idx] if sorted_latencies else 0

    # ── Print results ─────────────────────────────────────────────────
    print()
    print("  ╔═══════════════════════════════════════════════════════════╗")
    print("  ║  🛰️  MISSION SCORING REPORT — CLASSIFICATION RESULTS    ║")
    print("  ╚═══════════════════════════════════════════════════════════╝")
    print()
    print("  Classification dimensions (max 85 pts):")
    print()
    for dim, weight in WEIGHTS.items():
        score = dim_scores[dim]
        pts = score * weight / _CLASSIFICATION_WEIGHT_SUM * 85
        method = "macro F1" if dim in ("category", "routing") else ("binary F1" if dim == "escalation" else "mean")
        bar = "█" * int(score * 20) + "░" * (20 - int(score * 20))
        print(f"    {dim:<16s}  {bar}  {score:.4f} ({method})  × {weight * 100:.0f}%  = {pts:5.2f} pts")
    print(f"    {'─' * 62}")
    print(f"    {'CLASSIFICATION':16s}  {'':20s}  {classification_score:5.1f} / 85")
    print()
    print("  Efficiency dimensions (max 15 pts, scored by platform):")
    print()
    print(f"    latency           p50={p50:.0f}ms  p95={p95:.0f}ms  (10% weight)")
    print("    cost              from response headers     (5% weight)")
    print()
    print(f"  Signals processed: {n_valid}/{n_total}")
    if errors:
        print(f"  Signals lost to the void: {errors}")
    print()
    print("  ┌─────────────────────────────────────────────────────────────┐")
    print("  │  Classification:  up to 85 pts from 5 scoring dimensions   │")
    print("  │  Efficiency:      up to 15 pts (latency + cost)            │")
    print("  │  Total functional score: 0–100                             │")
    print("  │  Engineering review: evaluated separately from your repo   │")
    print("  │                                                            │")
    if classification_score >= 75:
        print("  │  Status: 🟢 Strong signal — the crew salutes you.         │")
        print("  │  Commander Kapoor nods approvingly. This is rare.          │")
    elif classification_score >= 55:
        print("  │  Status: 🟡 Moderate — some signals lost in static.       │")
        print("  │  The crew survives, but Mehta is writing margin notes.     │")
    elif classification_score >= 30:
        print("  │  Status: 🟠 Weak signal — review your triage logic.       │")
        print("  │  Hull breaches going to the wrong team. People notice.     │")
    else:
        print("  │  Status: 🔴 Critical — Commander Kapoor has been notified.│")
        print("  │  She is 0.3 AU away and she is not patient.               │")
    print("  └─────────────────────────────────────────────────────────────┘")
    print()

    # ── Write JSON results ────────────────────────────────────────────
    output = {
        "classification_score": classification_score,
        "dimension_scores": dim_scores,
        "signals_scored": n_valid,
        "signals_total": n_total,
        "signals_errored": errors,
        "latency_p50_ms": round(p50, 0),
        "latency_p95_ms": round(p95, 0),
        "per_signal": [{k: v for k, v in r.items() if k != "error"} for r in results],
    }
    output_path = Path("eval_results.json")
    output_path.write_text(json.dumps(output, indent=2) + "\n")
    print(f"  📡 Results transmitted to {output_path}")
    print()
    print("  End of scoring run. The void awaits your submission.")
    print("  May the scoring computer be less merciless next time. (It won't be.)")
    print()

    return 0


if __name__ == "__main__":
    sys.exit(main())
