#!/usr/bin/env python3
# Copyright (c) Microsoft. All rights reserved.
"""Export evaluation datasets as JSON files compatible with the run_eval.py harness.

Generates ticket and gold JSON files in docs/data/tickets/ for both
the data cleanup and responsible AI evaluation datasets.

Usage:
    cd py/libs/evals
    uv run python -m ms.evals.export
"""

import json
from pathlib import Path

from ms.evals.datasets.data_cleanup import DATA_CLEANUP_DATASET
from ms.evals.datasets.responsible_ai import RESPONSIBLE_AI_DATASET
from ms.evals.models import EvalDataset


def export_dataset(dataset: EvalDataset, output_dir: Path) -> tuple[Path, Path]:
    """Export a dataset as ticket and gold JSON files.

    Returns the paths to the generated ticket and gold files.
    """
    output_dir.mkdir(parents=True, exist_ok=True)

    ticket_path = output_dir / f"eval_{dataset.name}.json"
    gold_path = output_dir / f"eval_{dataset.name}_gold.json"

    tickets = dataset.tickets()
    golds = dataset.golds()

    ticket_path.write_text(json.dumps(tickets, indent=4, ensure_ascii=False) + "\n")
    gold_path.write_text(json.dumps(golds, indent=4, ensure_ascii=False) + "\n")

    return ticket_path, gold_path


def main() -> None:
    """Export all evaluation datasets."""
    # Resolve the output directory relative to the repo root
    repo_root = Path(__file__).resolve().parents[6]
    output_dir = repo_root / "docs" / "data" / "tickets"

    for dataset in [DATA_CLEANUP_DATASET, RESPONSIBLE_AI_DATASET]:
        ticket_path, gold_path = export_dataset(dataset, output_dir)
        print(f"Exported {dataset.name}:")
        print(f"  Tickets ({len(dataset.cases)}): {ticket_path}")
        print(f"  Golds   ({len(dataset.cases)}): {gold_path}")


if __name__ == "__main__":
    main()
