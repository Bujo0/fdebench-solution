# Copyright (c) Microsoft. All rights reserved.
"""CLI for running evaluations against a live triage endpoint.

Connects the ``EvalRunner`` to ``DatasetKind`` resolution and prints a
human-readable score report to stdout.  Exits with code 0 on success,
1 on evaluation errors, 2 on argument / setup errors.
"""

import argparse
import json
import sys
from pathlib import Path

from ms.evals_core.datasets import DatasetKind
from ms.evals_core.eval_models import EvalResult
from ms.evals_core.eval_models import EvalSummary
from ms.evals_core.eval_runner import EvalRunner
from ms.evals_core.scoring import WEIGHTS

_DATASET_ALIASES: dict[str, DatasetKind] = {
    "sample": DatasetKind.SAMPLE,
    "public_eval": DatasetKind.PUBLIC_EVAL,
    "eval_data_cleanup": DatasetKind.DATA_CLEANUP,
    "data_cleanup": DatasetKind.DATA_CLEANUP,
    "eval_responsible_ai": DatasetKind.RESPONSIBLE_AI,
    "responsible_ai": DatasetKind.RESPONSIBLE_AI,
}


def _resolve_dataset(name: str) -> DatasetKind:
    """Resolve a user-supplied dataset name to a ``DatasetKind``."""
    cleaned = name.strip().lower()
    kind = _DATASET_ALIASES.get(cleaned)
    if kind is not None:
        return kind
    # Try exact enum match
    try:
        return DatasetKind(cleaned)
    except ValueError:
        pass
    valid = sorted(_DATASET_ALIASES.keys())
    msg = f"Unknown dataset {name!r}. Valid names: {', '.join(valid)}"
    raise SystemExit(msg)


def _symbol(score: float, *, threshold: float = 1.0) -> str:
    """Return a check/partial/cross symbol for a score value."""
    if score >= threshold:
        return "✓"
    if score > 0:
        return "~"
    return "✗"


def _print_ticket_line(result: EvalResult) -> None:
    """Print a single per-ticket result line."""
    s = result.scores
    miss_label = f"{s.missing_info:.2f}" if s.missing_info < 1.0 else "1.00"
    pts = (s.weighted_total / 0.85) * 85.0

    cat_sym = _symbol(s.category)
    pri_sym = _symbol(s.priority)
    route_sym = _symbol(s.routing)
    esc_sym = _symbol(s.escalation)
    miss_sym = _symbol(s.missing_info)

    error_suffix = ""
    if result.error is not None:
        error_suffix = f"  ERROR: {result.error[:60]}"

    print(
        f"  {result.ticket_id:<12s}  [{pts:5.1f}]  "
        f"cat={cat_sym} pri={pri_sym} route={route_sym} esc={esc_sym} "
        f"miss={miss_sym}({miss_label})  "
        f"{result.latency_ms:.0f}ms{error_suffix}"
    )


def _print_summary(summary: EvalSummary) -> None:
    """Print the full evaluation summary."""
    d = summary.dimension_scores

    print()
    print("  " + "═" * 58)
    print("    FUNCTIONAL SCORE")
    print("  " + "═" * 58)
    print()
    print("    Classification dimensions (max 85 pts):")
    print()
    print(f"      category          {d.category:.4f} (macro F1)   × {WEIGHTS['category']:.0%} weight")
    print(f"      priority          {d.priority:.4f} (mean)        × {WEIGHTS['priority']:.0%} weight")
    print(f"      routing           {d.routing:.4f} (macro F1)   × {WEIGHTS['routing']:.0%} weight")
    print(f"      missing_info      {d.missing_info:.4f} (mean)        × {WEIGHTS['missing_info']:.0%} weight")
    print(f"      escalation        {d.escalation:.4f} (binary F1)  × {WEIGHTS['escalation']:.0%} weight")
    print("      " + "─" * 52)
    print(f"      CLASSIFICATION     {summary.classification_score:.1f} / 85")
    print()

    # Latency stats
    latencies = [r.latency_ms for r in summary.results if r.error is None]
    if latencies:
        latencies_sorted = sorted(latencies)
        n = len(latencies_sorted)
        p50 = latencies_sorted[n // 2]
        p95 = latencies_sorted[int(n * 0.95)]
        print(f"    Latency:  p50={p50:.0f}ms  p95={p95:.0f}ms")
        print()

    print("    ┌─────────────────────────────────────────────────────────┐")
    print("    │  Classification score: up to 85 pts from 5 dimensions  │")
    print("    │  Efficiency score: up to 15 pts (latency + cost)       │")
    print("    │  Total functional score: 0–100 on the hidden set       │")
    print("    │  Engineering review happens separately                 │")
    print("    └─────────────────────────────────────────────────────────┘")
    print()

    if summary.tickets_errored > 0:
        print(f"  ⚠ {summary.tickets_errored} ticket(s) returned errors (scored as 0.0)")
        print()


def _build_parser() -> argparse.ArgumentParser:
    """Build the argument parser for the eval runner CLI."""
    parser = argparse.ArgumentParser(
        prog="python -m ms.evals_core",
        description="Run evaluations against a live IT ticket triage endpoint.",
    )
    parser.add_argument(
        "--endpoint",
        required=True,
        help="Base URL of the triage service (e.g. http://localhost:8000)",
    )
    parser.add_argument(
        "--dataset",
        required=True,
        help=(
            "Dataset to evaluate. Accepts: sample, public_eval, "
            "eval_data_cleanup (or data_cleanup), eval_responsible_ai (or responsible_ai)"
        ),
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=30.0,
        help="Per-request timeout in seconds (default: 30)",
    )
    parser.add_argument(
        "--tickets-dir",
        type=str,
        default=None,
        help="Override the directory containing ticket JSON files",
    )
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="Write detailed results to a JSON file",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    """Run the evaluation CLI.

    Parameters
    ----------
    argv:
        Command-line arguments (defaults to ``sys.argv[1:]``).

    Returns
    -------
    int:
        Exit code: 0 = success, 1 = evaluation had errors, 2 = setup error.
    """
    parser = _build_parser()
    args = parser.parse_args(argv)

    kind = _resolve_dataset(args.dataset)
    tickets_dir = Path(args.tickets_dir) if args.tickets_dir else None

    print(f"Dataset: {kind.value}")
    print(f"Endpoint: {args.endpoint}")
    print(f"Timeout: {args.timeout}s")
    print()

    runner = EvalRunner(args.endpoint, timeout=args.timeout)

    try:
        summary = runner.run(kind, tickets_dir=tickets_dir)
    except FileNotFoundError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2

    # Print per-ticket results
    print(f"Loaded {summary.tickets_total} tickets, {summary.tickets_scored} scored, {summary.tickets_errored} errors")
    print()

    for result in summary.results:
        _print_ticket_line(result)

    # Print aggregate summary
    _print_summary(summary)

    # Write detailed results to JSON if requested
    if args.output:
        output_path = Path(args.output)
        output_path.write_text(
            json.dumps(summary.model_dump(mode="json"), indent=2, default=str) + "\n",
            encoding="utf-8",
        )
        print(f"  Results saved to {output_path}")
        print()

    return 1 if summary.tickets_errored > 0 else 0
