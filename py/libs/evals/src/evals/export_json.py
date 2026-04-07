# Copyright (c) Microsoft. All rights reserved.
"""Export evaluation scenarios to JSON files compatible with run_eval.py.

Usage:
    cd py/libs/evals
    uv run python -m evals.export_json

This generates JSON files in docs/data/tickets/ that can be used directly
with the evaluation harness:
    cd docs/eval
    uv run python run_eval.py \\
        --endpoint http://localhost:8000 \\
        --dataset ../data/tickets/edge_cases_data_cleanup.json \\
        --gold ../data/tickets/edge_cases_data_cleanup_gold.json
"""

import json
from pathlib import Path

from evals.scenarios.data_cleanup import build_data_cleanup_suite
from evals.scenarios.responsible_ai import build_responsible_ai_suite

_TICKETS_DIR = Path(__file__).resolve().parents[5] / "docs" / "data" / "tickets"


def _write_json(data: list[dict[str, object]], path: Path) -> None:
    """Write JSON data with consistent formatting."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"  Wrote {len(data)} items to {path}")


def export_all() -> None:
    """Export all scenario suites to JSON files."""
    print("Exporting evaluation scenarios to JSON...\n")

    data_cleanup = build_data_cleanup_suite()
    _write_json(data_cleanup.get_tickets(), _TICKETS_DIR / "edge_cases_data_cleanup.json")
    _write_json(data_cleanup.get_gold_answers(), _TICKETS_DIR / "edge_cases_data_cleanup_gold.json")

    responsible_ai = build_responsible_ai_suite()
    _write_json(responsible_ai.get_tickets(), _TICKETS_DIR / "edge_cases_responsible_ai.json")
    _write_json(responsible_ai.get_gold_answers(), _TICKETS_DIR / "edge_cases_responsible_ai_gold.json")

    print(f"\nDone. Files written to {_TICKETS_DIR}")


if __name__ == "__main__":
    export_all()
