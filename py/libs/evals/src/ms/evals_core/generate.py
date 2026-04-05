# Copyright (c) Microsoft. All rights reserved.
"""Generate evaluation JSON files from scenario definitions.

Produces ticket and gold-answer JSON files compatible with
the evaluation harness at docs/eval/run_eval.py.

Usage:
    cd py/libs/evals
    uv run python -m ms.evals_core.generate --output-dir ../../../docs/data/tickets
"""

import argparse
import json
from pathlib import Path

from ms.evals_core.models.scenario import Scenario
from ms.evals_core.scenarios.data_cleanup import get_data_cleanup_scenarios
from ms.evals_core.scenarios.responsible_ai import get_responsible_ai_scenarios


def _scenarios_to_tickets_json(scenarios: list[Scenario]) -> list[dict[str, object]]:
    """Convert scenarios to the ticket JSON format expected by run_eval.py."""
    return [scenario.ticket.model_dump(mode="json") for scenario in scenarios]


def _scenarios_to_gold_json(scenarios: list[Scenario]) -> list[dict[str, object]]:
    """Convert scenarios to the gold-answer JSON format expected by run_eval.py."""
    return [scenario.gold.model_dump(mode="json") for scenario in scenarios]


def _write_json(data: list[dict[str, object]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
    print(f"  Written {len(data)} entries to {path}")


def generate(output_dir: Path) -> None:
    """Generate all evaluation JSON files."""
    data_cleanup = get_data_cleanup_scenarios()
    responsible_ai = get_responsible_ai_scenarios()
    all_scenarios = data_cleanup + responsible_ai

    print(f"Data cleanup scenarios:   {len(data_cleanup)}")
    print(f"Responsible AI scenarios: {len(responsible_ai)}")
    print(f"Total scenarios:          {len(all_scenarios)}")
    print()

    # Per-category files
    _write_json(
        _scenarios_to_tickets_json(data_cleanup),
        output_dir / "data_cleanup.json",
    )
    _write_json(
        _scenarios_to_gold_json(data_cleanup),
        output_dir / "data_cleanup_gold.json",
    )
    _write_json(
        _scenarios_to_tickets_json(responsible_ai),
        output_dir / "responsible_ai.json",
    )
    _write_json(
        _scenarios_to_gold_json(responsible_ai),
        output_dir / "responsible_ai_gold.json",
    )

    # Combined file for full evaluation
    _write_json(
        _scenarios_to_tickets_json(all_scenarios),
        output_dir / "edge_cases.json",
    )
    _write_json(
        _scenarios_to_gold_json(all_scenarios),
        output_dir / "edge_cases_gold.json",
    )

    print("\nDone. Run the eval harness with:")
    print(f"  uv run python run_eval.py --endpoint <url> --dataset {output_dir}/data_cleanup.json --gold {output_dir}/data_cleanup_gold.json")


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate evaluation scenario JSON files.")
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=Path(__file__).resolve().parents[5] / "docs" / "data" / "tickets",
        help="Directory to write the JSON files to (default: docs/data/tickets/)",
    )
    args = parser.parse_args()
    generate(args.output_dir)


if __name__ == "__main__":
    main()
