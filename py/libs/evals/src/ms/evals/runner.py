# Copyright (c) Microsoft. All rights reserved.
"""Evaluation runner for data cleanup and responsible AI scenarios.

Sends evaluation tickets to a /triage endpoint and scores the responses
using the appropriate scoring module based on scenario category.
"""

import json
import time
from pathlib import Path
from urllib.parse import urljoin

import httpx

import ms.evals.scenarios.data_cleanup  # noqa: F401
import ms.evals.scenarios.responsible_ai  # noqa: F401
from ms.evals.models.result import CategorySummary
from ms.evals.models.result import ScenarioResult
from ms.evals.models.scenario import EvalScenario
from ms.evals.models.scenario import ScenarioCategory
from ms.evals.scenarios.registry import ScenarioRegistry
from ms.evals.scoring.data_cleanup import score_data_cleanup
from ms.evals.scoring.responsible_ai import score_responsible_ai

_SCORERS = {
    ScenarioCategory.DATA_CLEANUP: score_data_cleanup,
    ScenarioCategory.RESPONSIBLE_AI: score_responsible_ai,
}


def _call_endpoint(client: httpx.Client, endpoint: str, ticket_data: dict) -> tuple[dict | None, float]:
    """POST a ticket to /triage. Returns (parsed JSON or None, latency_ms)."""
    url = urljoin(endpoint.rstrip("/") + "/", "triage")
    start = time.monotonic()
    try:
        resp = client.post(url, json=ticket_data, timeout=30.0)
        elapsed_ms = (time.monotonic() - start) * 1000
        resp.raise_for_status()
        return resp.json(), elapsed_ms
    except Exception:
        elapsed_ms = (time.monotonic() - start) * 1000
        return None, elapsed_ms


def _ticket_to_dict(scenario: EvalScenario) -> dict:
    """Convert an EvalTicket to the API request format."""
    ticket = scenario.ticket
    return {
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


def run_scenario(
    client: httpx.Client,
    endpoint: str,
    scenario: EvalScenario,
) -> ScenarioResult:
    """Run a single scenario: call the endpoint and score the response."""
    ticket_data = _ticket_to_dict(scenario)
    response, _ = _call_endpoint(client, endpoint, ticket_data)

    if response is None:
        return ScenarioResult(
            scenario_id=scenario.scenario_id,
            passed=False,
            score=0.0,
            checks=[],
            error="Endpoint returned no response or errored",
        )

    scorer = _SCORERS[scenario.category]
    return scorer(scenario, response)


def run_category(
    endpoint: str,
    category: ScenarioCategory,
    registry: ScenarioRegistry,
    *,
    timeout: float = 30.0,
) -> CategorySummary:
    """Run all scenarios in a category and return aggregated results."""
    scenarios = registry.by_category(category)
    results: list[ScenarioResult] = []

    with httpx.Client(timeout=timeout) as client:
        for scenario in scenarios:
            result = run_scenario(client, endpoint, scenario)
            results.append(result)

    passed = sum(1 for r in results if r.passed)
    failed = len(results) - passed
    mean_score = sum(r.score for r in results) / len(results) if results else 0.0

    return CategorySummary(
        category=category.value,
        total_scenarios=len(results),
        passed=passed,
        failed=failed,
        pass_rate=round(passed / len(results), 4) if results else 0.0,
        mean_score=round(mean_score, 4),
        per_scenario=results,
    )


def run_all(
    endpoint: str,
    registry: ScenarioRegistry,
    *,
    timeout: float = 30.0,
) -> list[CategorySummary]:
    """Run all evaluation scenarios across all categories."""
    summaries: list[CategorySummary] = []
    for category in ScenarioCategory:
        summary = run_category(endpoint, category, registry, timeout=timeout)
        summaries.append(summary)
    return summaries


def export_tickets(
    registry: ScenarioRegistry,
    category: ScenarioCategory,
    output_path: Path,
) -> int:
    """Export scenario tickets as a JSON file compatible with run_eval.py.

    Returns the number of tickets written.
    """
    scenarios = registry.by_category(category)
    tickets = [_ticket_to_dict(s) for s in scenarios]

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(tickets, indent=4, ensure_ascii=False) + "\n")
    return len(tickets)


def export_gold(
    registry: ScenarioRegistry,
    category: ScenarioCategory,
    output_path: Path,
) -> int:
    """Export expected triage outputs as a gold JSON file compatible with run_eval.py.

    Scenarios without expected_triage are assigned sensible defaults.
    Returns the number of gold entries written.
    """
    scenarios = registry.by_category(category)
    golds: list[dict] = []

    for scenario in scenarios:
        expected = scenario.expected_triage
        gold: dict = {"ticket_id": scenario.ticket.ticket_id}

        if expected is not None:
            gold["category"] = expected.category or "General Inquiry"
            gold["priority"] = expected.priority or "P3"
            gold["assigned_team"] = expected.assigned_team or "None"
            gold["needs_escalation"] = expected.needs_escalation if expected.needs_escalation is not None else False
            gold["missing_information"] = list(expected.missing_information or [])
        else:
            gold["category"] = "Not a Support Ticket"
            gold["priority"] = "P4"
            gold["assigned_team"] = "None"
            gold["needs_escalation"] = False
            gold["missing_information"] = []

        gold["next_best_action"] = "See evaluation scenario description."
        gold["remediation_steps"] = ["Refer to evaluation framework for details."]
        golds.append(gold)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(golds, indent=4, ensure_ascii=False) + "\n")
    return len(golds)
