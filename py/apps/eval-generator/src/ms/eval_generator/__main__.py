# Copyright (c) Microsoft. All rights reserved.
"""CLI entry point for generating the eval dataset.

Usage:
    cd py && uv run python -m ms.eval_generator
    cd py && uv run python -m ms.eval_generator --seed 42 --output ../docs/data/tickets
"""

import argparse
import sys
from pathlib import Path

from ms.eval_generator.generator import EvalDatasetGenerator
from ms.eval_generator.generator import print_dataset_stats


def main() -> int:
    """Generate eval dataset and write to output directory."""
    parser = argparse.ArgumentParser(
        description="Generate a diverse eval dataset for IT ticket triage evaluation.",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Random seed for reproducible generation (default: 42)",
    )
    parser.add_argument(
        "--output",
        type=str,
        default=None,
        help="Output directory for generated JSON files (default: docs/data/tickets/)",
    )
    parser.add_argument(
        "--max-variants",
        type=int,
        default=6,
        help="Maximum ticket variants per scenario (default: 6)",
    )
    parser.add_argument(
        "--stats-only",
        action="store_true",
        help="Print stats without writing files",
    )
    args = parser.parse_args()

    # Resolve output directory
    if args.output:
        output_dir = Path(args.output)
    else:
        # Default: project root docs/data/tickets/
        output_dir = Path(__file__).resolve().parents[5] / "docs" / "data" / "tickets"

    print(f"Seed: {args.seed}")
    print(f"Max variants per scenario: {args.max_variants}")
    print(f"Output directory: {output_dir}")

    generator = EvalDatasetGenerator(seed=args.seed, max_variants_per_scenario=args.max_variants)
    tickets, golds = generator.generate()

    print_dataset_stats(tickets, golds)

    if args.stats_only:
        print("Stats-only mode — no files written.")
        return 0

    tickets_path, golds_path = generator.write_dataset(output_dir)
    print(f"Written {len(tickets)} tickets to {tickets_path}")
    print(f"Written {len(golds)} gold answers to {golds_path}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
