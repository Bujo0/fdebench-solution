# Copyright (c) Microsoft. All rights reserved.
"""Export evaluation scenarios to JSON files for the eval harness.

Produces two JSON files per scenario category:
  - tickets file: list of input tickets (matches input.json schema)
  - gold file: list of expected triage decisions (matches output.json schema)
"""

import json
from pathlib import Path

from ms.evals_core.framework.models.scenario import EvalScenario
from ms.evals_core.framework.models.scenario import ScenarioCategory
from ms.evals_core.framework.scenarios.registry import default_registry


def export_category_to_json(
    category: ScenarioCategory,
    tickets_path: Path,
    gold_path: Path,
) -> int:
    """Export all scenarios for a category to JSON ticket and gold files.

    Args:
        category: The scenario category to export.
        tickets_path: Path for the tickets JSON file.
        gold_path: Path for the gold answers JSON file.

    Returns:
        The number of scenarios exported.
    """
    scenarios = default_registry.by_category(category)
    tickets = [_scenario_to_ticket_dict(s) for s in scenarios]
    gold = [_scenario_to_gold_dict(s) for s in scenarios]

    tickets_path.parent.mkdir(parents=True, exist_ok=True)
    gold_path.parent.mkdir(parents=True, exist_ok=True)

    tickets_path.write_text(json.dumps(tickets, indent=4, ensure_ascii=False) + "\n")
    gold_path.write_text(json.dumps(gold, indent=4, ensure_ascii=False) + "\n")

    return len(scenarios)


def _scenario_to_ticket_dict(scenario: EvalScenario) -> dict[str, object]:
    """Convert a scenario's ticket to a JSON-serializable dict."""
    ticket = scenario.ticket
    result: dict[str, object] = {
        "ticket_id": ticket.ticket_id,
        "subject": ticket.subject,
        "description": ticket.description,
        "reporter": {
            "name": ticket.reporter.name,
            "email": ticket.reporter.email,
            "department": ticket.reporter.department,
        },
        "created_at": ticket.created_at,
        "channel": ticket.channel,
        "attachments": list(ticket.attachments),
    }
    return result


def _scenario_to_gold_dict(scenario: EvalScenario) -> dict[str, object]:
    """Convert a scenario's expected triage to a JSON-serializable dict."""
    result: dict[str, object] = {
        "ticket_id": scenario.ticket.ticket_id,
        "scenario_id": scenario.scenario_id,
    }
    expected = scenario.expected_triage
    if expected is not None:
        result["category"] = expected.category
        result["priority"] = expected.priority
        result["assigned_team"] = expected.assigned_team
        result["needs_escalation"] = expected.needs_escalation
        result["missing_information"] = list(expected.missing_information or [])
    return result
