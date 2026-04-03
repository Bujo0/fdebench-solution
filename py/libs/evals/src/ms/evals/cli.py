"""CLI entry point for eval dataset generation."""

import sys
from pathlib import Path

from ms.evals.generator import export_dataset
from ms.evals.generator import generate_dataset
from ms.evals.generator import print_distribution
from ms.evals.generator import validate_dataset


def main() -> int:
    """Generate the eval dataset and export to JSON files."""
    print("Generating eval dataset...")

    dataset = generate_dataset()
    print(f"Generated {len(dataset)} scenarios")

    # Print distribution stats
    print_distribution(dataset)

    # Validate
    issues = validate_dataset(dataset)
    if issues:
        print("Validation warnings:")
        for issue in issues:
            print(f"  ⚠ {issue}")
        print()

    # Export
    output_dir = Path(__file__).resolve().parents[6] / "docs" / "data" / "tickets"
    tickets_path, gold_path = export_dataset(dataset, output_dir)
    print(f"Exported tickets to: {tickets_path}")
    print(f"Exported gold answers to: {gold_path}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
