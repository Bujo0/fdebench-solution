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
        "looks for a file named <dataset>_gold.json next to the dataset. "
        "If no gold file is found, runs in smoke-test mode (no scoring).",
    )
    args = parser.parse_args()

    # ── Load data ─────────────────────────────────────────────────────
    dataset_path = Path(args.dataset)
    if not dataset_path.exists():
        print(f"  ✗ Signal archive not found: {dataset_path}")
        return 1

    signals = json.loads(dataset_path.read_text())

    # Resolve gold file — if no gold answers exist, run in smoke-test mode
    gold_path: Path | None = None
    if args.gold:
        gold_path = Path(args.gold)
        if not gold_path.exists():
            print(f"  ✗ Gold answer archive not found: {gold_path}")
            return 1
    else:
        candidate = dataset_path.parent / f"{dataset_path.stem}_gold.json"
        if candidate.exists():
            gold_path = candidate

    if gold_path is not None:
        return _run_scored(signals, gold_path, args.endpoint)
    return _run_smoke_test(signals, args.endpoint)


# ── Smoke-test mode (no gold answers) ────────────────────────────────
# When no gold file is available, we still send every signal to the
# endpoint and validate that responses come back intact, correctly
# shaped, and without the kind of explosions that make the Admiral
# write memos. No scoring — just survival checks.

_CATEGORY_SET = {_normalize(c) for c in CATEGORIES}
_TEAM_SET = {_normalize(t) for t in TEAMS}
_PRIORITY_SET = {"p1", "p2", "p3", "p4"}
_MISSING_INFO_SET = {
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
}
_REQUIRED_FIELDS = {
    "ticket_id",
    "category",
    "priority",
    "assigned_team",
    "needs_escalation",
    "missing_information",
    "next_best_action",
    "remediation_steps",
}


def _validate_response(pred: dict, signal_id: str) -> list[str]:
    """Validate a triage response against the output schema.

    Returns a list of schema violations. Empty list = all clear.
    The void demands compliance. The schema demands completeness.
    """
    issues: list[str] = []

    missing_fields = _REQUIRED_FIELDS - set(pred.keys())
    if missing_fields:
        issues.append(f"missing fields: {', '.join(sorted(missing_fields))}")

    if "category" in pred and _normalize(str(pred["category"])) not in _CATEGORY_SET:
        issues.append(f"invalid category: '{pred['category']}'")

    if "priority" in pred:
        p = str(pred["priority"]).strip().lower()
        if p not in _PRIORITY_SET:
            issues.append(f"invalid priority: '{pred['priority']}'")

    if "assigned_team" in pred and _normalize(str(pred["assigned_team"])) not in _TEAM_SET:
        issues.append(f"invalid team: '{pred['assigned_team']}'")

    if "needs_escalation" in pred and not isinstance(pred["needs_escalation"], (bool, str, int)):
        issues.append(f"needs_escalation not boolean-coercible: {type(pred['needs_escalation']).__name__}")

    if "missing_information" in pred:
        mi = pred["missing_information"]
        if not isinstance(mi, list):
            issues.append(f"missing_information not a list: {type(mi).__name__}")
        else:
            invalid_terms = [t for t in mi if _normalize(str(t)) not in _MISSING_INFO_SET]
            if invalid_terms:
                issues.append(f"invalid missing_info terms: {invalid_terms[:3]}")

    if "remediation_steps" in pred:
        rs = pred["remediation_steps"]
        if not isinstance(rs, list):
            issues.append(f"remediation_steps not a list: {type(rs).__name__}")
        elif not rs:
            issues.append("remediation_steps is empty")

    if "ticket_id" in pred and str(pred["ticket_id"]) != signal_id:
        issues.append(f"ticket_id mismatch: expected '{signal_id}', got '{pred['ticket_id']}'")

    return issues


def _run_smoke_test(signals: list[dict], endpoint: str) -> int:
    """Run in smoke-test mode — no gold answers, just survival checks.

    Like a hull integrity scan: no score, but you'll know exactly
    where the cracks are before the void finds them for you.
    """
    print()
    print("         ╱╲")
    print("        ╱  ╲")
    print("       ╱    ╲")
    print("      ╱  /\\  ╲")
    print("     ╱  /  \\  ╲")
    print("    ╱  / 🛰️  \\  ╲")
    print("   ╱  /________\\  ╲")
    print("   ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾")
    print("   ┃  ┃        ┃  ┃")
    print("   ┃  ┃  CDSS  ┃  ┃")
    print("   ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾")
    print("       💨💨💨💨")
    print()
    print("  🛰️  CONTOSO DEEP SPACE STATION — SMOKE TEST  🛰️")
    print("  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("  « Pre-flight hull integrity scan — no scoring, just survival. »")
    print()
    print()
    print(f"  Incoming signals:  {len(signals)}")
    print("  Gold answers:      — (smoke test — no scoring, just survival)")
    print(f"  Target endpoint:   {endpoint}")
    print()
    print("  ⚠ No gold file detected. Running in SMOKE TEST mode.")
    print("  This checks for crashes, timeouts, and schema violations —")
    print("  the kind of problems that turn a promising triage system into")
    print("  a cautionary tale whispered between decks at 0300 station time.")
    print()

    client = httpx.Client()
    healthy = check_health(client, endpoint)
    if healthy:
        status = "✓ LIFE SIGNS DETECTED — the station breathes. The Deck 9 cat approves."
    else:
        status = "✗ NO LIFE SIGNS — FLATLINE — your service is as responsive as a frozen crewmate"
    print(f"  Health check: {status}")
    if not healthy:
        print("  ⚠ Warning: GET /health did not return 200. Proceeding anyway...")
        print("  (The smoke test is brave. Or indifferent. Like the nutrient synthesizer.)")
    print()

    print("  Transmitting signals... stand by for contact.")
    print("  (No scoring — just checking if your system survives first contact")
    print("   with signals it's never seen. Like a hull integrity test, but for code.)")
    print()

    latencies: list[float] = []
    transport_errors = 0
    schema_violations = 0
    per_signal_results: list[dict] = []

    for signal in signals:
        tid = signal["ticket_id"]
        pred, elapsed_ms = call_endpoint(client, endpoint, signal)
        latencies.append(elapsed_ms)

        if pred is None:
            transport_errors += 1
            per_signal_results.append({"ticket_id": tid, "status": "error", "latency_ms": round(elapsed_ms, 0)})
            continue

        issues = _validate_response(pred, tid)
        if issues:
            schema_violations += 1
            print(f"  {tid}  ⚠ SCHEMA — {'; '.join(issues)}  {elapsed_ms:.0f}ms")
            per_signal_results.append(
                {
                    "ticket_id": tid,
                    "status": "schema_violation",
                    "issues": issues,
                    "latency_ms": round(elapsed_ms, 0),
                }
            )
        else:
            print(f"  {tid}  ✓ valid  {elapsed_ms:.0f}ms")
            per_signal_results.append({"ticket_id": tid, "status": "ok", "latency_ms": round(elapsed_ms, 0)})

    client.close()

    n_total = len(signals)
    n_ok = n_total - transport_errors - schema_violations

    # Latency stats
    sorted_latencies = sorted(latencies)
    p50 = sorted_latencies[len(sorted_latencies) // 2] if sorted_latencies else 0
    p95_idx = min(int(len(sorted_latencies) * 0.95), len(sorted_latencies) - 1) if sorted_latencies else 0
    p95 = sorted_latencies[p95_idx] if sorted_latencies else 0

    print()
    print("  ╔═══════════════════════════════════════════════════════════╗")
    print("  ║  🛰️  SMOKE TEST REPORT — HULL INTEGRITY SCAN            ║")
    print("  ╚═══════════════════════════════════════════════════════════╝")
    print()
    print(f"  Signals transmitted:     {n_total}")
    print(f"  Valid responses:         {n_ok}")
    if transport_errors:
        print(f"  Transport errors:        {transport_errors}  ← signals lost to the void")
    if schema_violations:
        print(f"  Schema violations:       {schema_violations}  ← responses the scoring computer would reject")
    print()
    print(f"  Latency:  p50={p50:.0f}ms   p95={p95:.0f}ms")
    if p50 > 2000:
        print("    ⚠ p50 > 2000ms — your system responds slower than a cryo-sleep wake-up.")
        print("      The scoring run uses 30s timeouts. At this pace, the void will time you out.")
    elif p50 > 200:
        print(f"    ⚠ p50={p50:.0f}ms — above the 200ms ideal. The crew is tapping their boots.")
    else:
        print("    ✓ Latency looking sharp. The crew barely has time to worry.")
    print()

    print("  ┌─────────────────────────────────────────────────────────────┐")
    print("  │  This was a SMOKE TEST — no classification scores.         │")
    print("  │  To see scores, run against sample.json with gold answers. │")
    print("  │                                                            │")
    if transport_errors == 0 and schema_violations == 0:
        print("  │  Status: 🟢 All clear — hull integrity confirmed.         │")
        print("  │  Every signal got a valid response. No crashes, no schema  │")
        print("  │  violations, no mysterious explosions. The Deck 9 cat is   │")
        print("  │  cautiously optimistic. Mehta is cautiously Mehta.         │")
    elif transport_errors == 0 and schema_violations <= n_total * 0.1:
        print("  │  Status: 🟡 Minor hull stress — a few schema issues.      │")
        print("  │  No crashes, but some responses don't match the schema.    │")
        print("  │  Fix these before submission or the scoring computer will  │")
        print("  │  score them as zeroes. It has no sympathy. Like asteroids. │")
    elif transport_errors <= n_total * 0.1:
        print("  │  Status: 🟠 Hull damage detected — errors found.          │")
        print("  │  Some signals didn't survive first contact. The hidden     │")
        print("  │  set has 1000+ signals. Multiply these problems by 10x.   │")
        print("  │  The Admiral notices patterns. Especially bad patterns.    │")
    else:
        print("  │  Status: 🔴 Critical hull failure — major errors.         │")
        print("  │  Your system is venting atmosphere. Figuratively. But the  │")
        print("  │  scoring run will be even less forgiving. Recommend full   │")
        print("  │  system diagnostic before submission. The Titan Outpost    │")
        print("  │  had better uptime. And they're a debris field now.        │")
    print("  └─────────────────────────────────────────────────────────────┘")
    print()

    # Write results
    output = {
        "mode": "smoke_test",
        "signals_total": n_total,
        "signals_ok": n_ok,
        "transport_errors": transport_errors,
        "schema_violations": schema_violations,
        "latency_p50_ms": round(p50, 0),
        "latency_p95_ms": round(p95, 0),
        "per_signal": per_signal_results,
    }
    output_path = Path("eval_results.json")
    output_path.write_text(json.dumps(output, indent=2) + "\n")
    print(f"  📡 Results transmitted to {output_path}")
    print()
    if transport_errors == 0 and schema_violations == 0:
        print("  Smoke test complete. All systems nominal.")
        print("  Now run against sample.json with gold answers for actual scores.")
        print("  The scoring computer awaits. It is patient. It is eternal. It is math.")
    else:
        print("  Smoke test complete. Issues detected.")
        print("  Fix the errors above, then re-run. The void is patient,")
        print("  but the submission deadline is not.")
    print()

    return 0


# ── Scored mode (with gold answers) ──────────────────────────────────


def _run_scored(signals: list[dict], gold_path: Path, endpoint: str) -> int:
    """Run full scoring against gold answers — the real deal."""
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
    print("         ╱╲")
    print("        ╱  ╲")
    print("       ╱    ╲")
    print("      ╱  /\\  ╲")
    print("     ╱  /  \\  ╲")
    print("    ╱  / 🛰️  \\  ╲")
    print("   ╱  /________\\  ╲")
    print("   ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾")
    print("   ┃  ┃        ┃  ┃")
    print("   ┃  ┃  CDSS  ┃  ┃")
    print("   ‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾‾")
    print("     🔥🔥🔥🔥🔥🔥")
    print()
    print("  🛰️  CONTOSO DEEP SPACE STATION — SCORING COMPUTER  🛰️")
    print("  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    print("  « All stations — scoring run initiated. This is not a drill. »")
    print("  « The math is real. The void is watching. The cat is judging. »")
    print()
    print(f"  Incoming signals:  {len(signals)}")
    print(f"  Gold answers:      {len(golds)}")
    print(f"  Target endpoint:   {endpoint}")
    print()

    # ── Health check ──────────────────────────────────────────────────
    client = httpx.Client()
    healthy = check_health(client, endpoint)
    if healthy:
        status = "✓ LIFE SIGNS DETECTED — station is online. The Deck 9 cat stirs approvingly."
    else:
        status = "✗ NO LIFE SIGNS — your service has the responsiveness of a frozen crewmate in Sector 7G"
    print(f"  Health check: {status}")
    if not healthy:
        print("  ⚠ Warning: GET /health did not return 200. Proceeding with scoring anyway...")
        print("  (The scoring computer charges ahead regardless, like a probe with a")
        print("   broken proximity sensor. Brave? Reckless? The distinction is academic.)")
    print()

    # ── Score each signal ─────────────────────────────────────────────
    print("  ⚡ Transmitting signals to triage endpoint... stand by for contact.")
    print("  (Every signal is a life-or-death decision. Or a protein cube complaint.")
    print("   The scoring computer doesn't know which until it reads the gold answer.")
    print("   It processes both with equal, terrifying precision.)")
    print()
    results: list[dict] = []
    responses: list[dict] = []
    latencies: list[float] = []
    errors = 0

    for signal in signals:
        tid = signal["ticket_id"]
        gold = gold_by_id[tid]

        pred, elapsed_ms = call_endpoint(client, endpoint, signal)
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

    # Dimension-specific commentary — because numbers without opinions are just... numbers
    _print_dimension_commentary(dim_scores)
    print()
    print("  Efficiency dimensions (max 15 pts, scored by platform):")
    print()
    print(f"    latency           p50={p50:.0f}ms  p95={p95:.0f}ms  (10% weight)")
    print("    cost              from response headers     (5% weight)")
    print()
    print(f"  Signals processed: {n_valid}/{n_total}")
    if errors:
        print(f"  Signals lost to the void: {errors} — the Deck 9 cat could have caught those")
    print()
    _print_status_box(classification_score)
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
    _print_closing_message(classification_score)
    print()

    return 0


def _print_dimension_commentary(dim_scores: dict[str, float]) -> None:
    """Print dimension-specific tactical advice.

    Because numbers without opinions are just... numbers floating
    in the void, signifying nothing.
    """
    if dim_scores["category"] < 0.5:
        print("    ⚠ Category: Your system confuses anomaly types like a cadet who thinks")
        print("      every warning light means 'hull breach.' Threat Response just got")
        print("      dispatched to a nutrient synthesizer jam. They are armed. And annoyed.")
    if dim_scores["priority"] < 0.5:
        print("    ⚠ Priority: You rated a hull breach as Routine and a protein cube shortage")
        print("      as Red Alert. The crew is evacuating Deck 3 over a seasoning error while")
        print("      actual vacuum seeps through Deck 7. Recalibrate your threat model.")
    if dim_scores["routing"] < 0.5:
        print("    ⚠ Routing: Signals arriving at the wrong teams like a malfunctioning")
        print("      turbolift that exclusively visits decks where the problem isn't. Deep")
        print("      Space Comms just received a containment breach. They have questions.")
    if dim_scores["missing_info"] < 0.5:
        print("    ⚠ Missing info: Either demanding data the signal already provided (the crew")
        print("      can hear you asking their name from 0.3 AU away, and they are not amused)")
        print("      or missing critical gaps like 'which deck is currently on fire.'")
    if dim_scores["escalation"] < 0.5:
        print("    ⚠ Escalation: Missing real emergencies or crying wolf on routine maintenance.")
        print("      Commander Kapoor was woken at 0300 for a font rendering issue, and slept")
        print("      through an actual hostile contact. She has opinions about this. Strong ones.")


def _print_status_box(classification_score: float) -> None:
    """Print the final status box with score-appropriate commentary.

    The box is fixed-width because even chaos should be well-formatted.
    Commander Kapoor insists on presentation standards.
    """
    print("  ┌─────────────────────────────────────────────────────────────┐")
    print("  │  Classification:  up to 85 pts from 5 scoring dimensions   │")
    print("  │  Efficiency:      up to 15 pts (latency + cost)            │")
    print("  │  Total functional score: 0–100                             │")
    print("  │  Engineering review: evaluated separately from your repo   │")
    print("  │                                                            │")
    if classification_score >= 80:
        print("  │  Status: 🟢 STELLAR — the crew salutes. Kapoor nods once. │")
        print("  │  Mehta puts down his pen. The Deck 9 cat purrs for the    │")
        print("  │  first time in recorded station history. The void itself   │")
        print("  │  seems to soften, briefly, as if impressed. It isn't. But │")
        print("  │  for a moment, it looked like it might be. That's enough.  │")
    elif classification_score >= 65:
        print("  │  Status: 🟢 Strong signal — crew survives with style.    │")
        print("  │  Mehta's margin notes are almost complimentary. He wrote  │")
        print("  │  'acceptable' which is his version of a standing ovation. │")
        print("  │  Protein cubes taste slightly better today. Coincidence?  │")
    elif classification_score >= 50:
        print("  │  Status: 🟡 Moderate — some signals lost in static.      │")
        print("  │  Crew survives, but Mehta is writing margin notes. Many   │")
        print("  │  margin notes. The Deck 3 fabricator has better accuracy. │")
        print("  │  That fabricator is ALWAYS broken. Think about that.      │")
    elif classification_score >= 30:
        print("  │  Status: 🟠 Weak signal — review your triage logic.      │")
        print("  │  Hull breaches routed to the wrong team. Containment      │")
        print("  │  alerts sent to Telemetry. The nutrient synthesizer has   │")
        print("  │  better judgment than this, and it thinks everything is   │")
        print("  │  vanilla. The Admiral has started composing a memo.       │")
    else:
        print("  │  Status: 🔴 CRITICAL — Commander Kapoor has been paged.  │")
        print("  │  She is 0.3 AU away and she is not patient. Mehta has run │")
        print("  │  out of margins to write in. The Deck 9 cat looked at    │")
        print("  │  your scores, yawned, and walked away. Even the void     │")
        print("  │  seems embarrassed on your behalf. Titan Outpost's last  │")
        print("  │  triage system scored higher. They are a debris field.    │")
    print("  └─────────────────────────────────────────────────────────────┘")


def _print_closing_message(classification_score: float) -> None:
    """Print the closing message — the last words before the void reclaims silence."""
    if classification_score >= 80:
        print("  End of scoring run. The void respects your engineering.")
        print("  Commander Kapoor has added your name to the 'Do Not Jettison' list.")
        print("  The Deck 9 cat would headbutt your ankle approvingly, if it weren't")
        print("  a cat, and therefore above such displays of affection. But you'd know.")
    elif classification_score >= 65:
        print("  End of scoring run. Solid work, operator.")
        print("  The scoring computer has processed your results with something that,")
        print("  if it had emotions, might be described as 'grudging respect.'")
        print("  It does not have emotions. But the numbers speak. And they're decent.")
    elif classification_score >= 50:
        print("  End of scoring run. The void awaits your next attempt.")
        print("  May the scoring computer be less merciless next time. (It won't be.)")
        print("  The protein cubes wish you luck. They are the only ones who do.")
        print("  Mehta has left a sticky note on your file: 'shows promise, needs work.'")
    else:
        print("  End of scoring run. The void has formed opinions about your submission.")
        print("  Mehta recommends re-reading the routing guide. All of it. Twice. Out loud.")
        print("  Then re-reading the mission briefing. Then sitting quietly in the dark")
        print("  of the observation deck, contemplating the cosmic indifference of F1 scores,")
        print("  before trying again. The Titan Outpost had better scores. They're an")
        print("  asteroid field now, but at least they could route a hull breach correctly.")


if __name__ == "__main__":
    sys.exit(main())
