# Copyright (c) Microsoft. All rights reserved.
"""CLI entry point for generating eval datasets.

Usage:
    uv run generate-evals --count 2000 --output docs/data/tickets --seed 42
"""

import argparse
import sys
from pathlib import Path

from ms.evals.generator import generate_dataset
from ms.evals.validator import analyze_balance
from ms.evals.validator import validate_dataset
from ms.evals.validator import write_dataset


def main() -> int:
    """Generate an eval dataset for the ticket triage system."""
    parser = argparse.ArgumentParser(
        description="Generate a diverse, balanced eval dataset for IT ticket triage.",
    )
    parser.add_argument(
        "--count",
        type=int,
        default=2000,
        help="Number of tickets to generate (default: 2000)",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Random seed for reproducibility (default: 42)",
    )
    parser.add_argument(
        "--output",
        type=str,
        default="docs/data/tickets",
        help="Output directory for generated files (default: docs/data/tickets)",
    )
    parser.add_argument(
        "--prefix",
        type=str,
        default="eval_generated",
        help="Filename prefix (default: eval_generated)",
    )
    parser.add_argument(
        "--start-id",
        type=int,
        default=2001,
        help="Starting ticket ID number (default: 2001)",
    )
    parser.add_argument(
        "--validate-only",
        action="store_true",
        help="Only validate an existing dataset",
    )

    args = parser.parse_args()
    output_dir = Path(args.output)

    print(f"Generating {args.count} eval tickets (seed={args.seed})...")
    print()

    tickets, golds, stats = generate_dataset(
        count=args.count,
        seed=args.seed,
        start_id=args.start_id,
    )

    # Validate
    errors = validate_dataset(tickets, golds)
    if errors:
        print(f"VALIDATION ERRORS ({len(errors)}):")
        for err in errors[:20]:
            print(f"  ✗ {err}")
        if len(errors) > 20:
            print(f"  ... and {len(errors) - 20} more")
        print()
        return 1

    print("✓ All tickets pass schema validation")
    print()

    # Print balance report
    report = analyze_balance(stats)
    print(report)
    print()

    # Write output
    tickets_path, gold_path = write_dataset(tickets, golds, output_dir, args.prefix)
    print(f"✓ Tickets written to: {tickets_path}")
    print(f"✓ Gold answers written to: {gold_path}")
    print()

    return 0


if __name__ == "__main__":
    sys.exit(main())
