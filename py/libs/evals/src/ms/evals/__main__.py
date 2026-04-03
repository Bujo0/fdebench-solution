# Copyright (c) Microsoft. All rights reserved.
"""CLI entry point for running evaluations.

Usage::

    uv run python -m ms.evals \
        --endpoint http://localhost:8000 \
        --dataset data_cleanup

    uv run python -m ms.evals \
        --endpoint http://localhost:8000 \
        --dataset responsible_ai
"""

import argparse
import json
import sys

from ms.evals.datasets import DatasetKind
from ms.evals.runner import EvalRunner


def _parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run data-cleanup or responsible-AI evaluations against a live triage endpoint.",
    )
    parser.add_argument(
        "--endpoint",
        required=True,
        help="Base URL of the triage service (e.g. http://localhost:8000).",
    )
    parser.add_argument(
        "--dataset",
        required=True,
        choices=[k.value for k in DatasetKind],
        help="Which evaluation dataset to run.",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=30.0,
        help="Per-request timeout in seconds (default: 30).",
    )
    parser.add_argument(
        "--output",
        default=None,
        help="Path to write JSON results (default: stdout summary only).",
    )
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """Run the evaluation and print results."""
    args = _parse_args(argv)

    kind = DatasetKind(args.dataset)
    runner = EvalRunner(args.endpoint, timeout=args.timeout)

    print(f"Running evaluation: {kind.value}")
    print(f"Endpoint: {args.endpoint}")
    print()

    summary = runner.run(kind)

    # Per-ticket results
    for result in summary.results:
        status = "ERR" if result.error else f"{result.scores.weighted_total * 100:.1f}"
        err_suffix = f"  ({result.error})" if result.error else ""
        print(f"  {result.ticket_id}  [{status:>5}]  {result.latency_ms:.0f}ms{err_suffix}")

    print()
    print("=" * 60)
    print(f"  Dataset:              {summary.dataset_kind}")
    print(f"  Tickets scored:       {summary.tickets_scored} / {summary.tickets_total}")
    print(f"  Tickets errored:      {summary.tickets_errored}")
    print()
    print("  Dimension scores:")
    print(f"    category:           {summary.dimension_scores.category:.4f}")
    print(f"    priority:           {summary.dimension_scores.priority:.4f}")
    print(f"    routing:            {summary.dimension_scores.routing:.4f}")
    print(f"    missing_info:       {summary.dimension_scores.missing_info:.4f}")
    print(f"    escalation:         {summary.dimension_scores.escalation:.4f}")
    print()
    print(f"  CLASSIFICATION SCORE: {summary.classification_score:.1f} / 85")
    print("=" * 60)

    if args.output:
        output_data = summary.model_dump(mode="json")
        with open(args.output, "w", encoding="utf-8") as f:
            json.dump(output_data, f, indent=2, ensure_ascii=False)
        print(f"\nResults saved to {args.output}")

    return 0 if summary.tickets_errored == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
