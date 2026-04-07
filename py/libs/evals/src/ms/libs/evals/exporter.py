"""Export evaluation scenarios to JSON files compatible with run_eval.py."""

import json
from pathlib import Path

from ms.libs.evals.models.scenario import EvalScenario


def export_scenarios_to_json(
    scenarios: list[EvalScenario],
    tickets_path: Path,
    gold_path: Path,
) -> None:
    """Export scenarios to separate tickets and gold-standard JSON files.

    The output format is identical to docs/data/tickets/sample.json and
    docs/data/tickets/sample_gold.json, making the exported files directly
    usable with the existing run_eval.py harness.
    """
    tickets = [scenario.ticket.model_dump(mode="json") for scenario in scenarios]
    golds = [scenario.gold.model_dump(mode="json") for scenario in scenarios]

    tickets_path.parent.mkdir(parents=True, exist_ok=True)
    gold_path.parent.mkdir(parents=True, exist_ok=True)

    tickets_path.write_text(json.dumps(tickets, indent=4) + "\n")
    gold_path.write_text(json.dumps(golds, indent=4) + "\n")


def export_scenario_metadata(
    scenarios: list[EvalScenario],
    metadata_path: Path,
) -> None:
    """Export scenario test metadata (names, descriptions, tags) for documentation."""
    metadata = [
        {
            "ticket_id": scenario.ticket.ticket_id,
            "tag": scenario.tag.value,
            "test_name": scenario.test_name,
            "test_description": scenario.test_description,
        }
        for scenario in scenarios
    ]

    metadata_path.parent.mkdir(parents=True, exist_ok=True)
    metadata_path.write_text(json.dumps(metadata, indent=4) + "\n")
