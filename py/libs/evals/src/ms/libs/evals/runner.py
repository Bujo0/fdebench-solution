"""Evaluation runner for testing a /triage endpoint against scenario data.

Uses the same scoring logic as docs/eval/run_eval.py but operates on
in-memory EvalScenario objects rather than JSON files.
"""

import time
from dataclasses import dataclass, field

import httpx

from ms.libs.evals.models.scenario import EvalScenario


@dataclass(frozen=True)
class TicketResult:
    """Result of evaluating a single ticket."""

    ticket_id: str
    latency_ms: float
    response: dict | None
    error: str | None = None


@dataclass
class EvalRunResult:
    """Aggregate result of an evaluation run."""

    total_tickets: int = 0
    successful: int = 0
    failed: int = 0
    ticket_results: list[TicketResult] = field(default_factory=list)
    latency_p50_ms: float = 0.0
    latency_p95_ms: float = 0.0


def _call_triage(
    client: httpx.Client,
    endpoint: str,
    ticket_data: dict,
    timeout_seconds: float = 30.0,
) -> TicketResult:
    """POST a ticket to /triage and return the result."""
    url = endpoint.rstrip("/") + "/triage"
    start = time.monotonic()
    try:
        resp = client.post(url, json=ticket_data, timeout=timeout_seconds)
        elapsed_ms = (time.monotonic() - start) * 1000
        resp.raise_for_status()
        return TicketResult(
            ticket_id=ticket_data["ticket_id"],
            latency_ms=elapsed_ms,
            response=resp.json(),
        )
    except Exception as exc:
        elapsed_ms = (time.monotonic() - start) * 1000
        return TicketResult(
            ticket_id=ticket_data["ticket_id"],
            latency_ms=elapsed_ms,
            response=None,
            error=str(exc),
        )


def _check_health(client: httpx.Client, endpoint: str) -> bool:
    """GET /health and check for 200."""
    url = endpoint.rstrip("/") + "/health"
    try:
        resp = client.get(url, timeout=10.0)
        return resp.status_code == 200
    except Exception:
        return False


def _compute_latency_percentiles(
    latencies: list[float],
) -> tuple[float, float]:
    """Compute p50 and p95 latency from a sorted list."""
    if not latencies:
        return 0.0, 0.0
    sorted_lat = sorted(latencies)
    n = len(sorted_lat)
    p50 = sorted_lat[n // 2]
    p95_idx = min(int(n * 0.95), n - 1)
    p95 = sorted_lat[p95_idx]
    return p50, p95


def run_eval(
    scenarios: list[EvalScenario],
    endpoint: str,
    timeout_seconds: float = 30.0,
    skip_health_check: bool = False,
) -> EvalRunResult:
    """Run evaluation scenarios against a /triage endpoint.

    Sends each scenario's ticket to the endpoint and collects responses.
    Does NOT score the responses — use the existing scoring functions from
    docs/eval/run_eval.py or score_submission() for that.

    Returns an EvalRunResult with per-ticket responses and latency stats.
    """
    client = httpx.Client()
    result = EvalRunResult(total_tickets=len(scenarios))

    if not skip_health_check:
        healthy = _check_health(client, endpoint)
        if not healthy:
            client.close()
            msg = f"Health check failed for endpoint: {endpoint}"
            raise ConnectionError(msg)

    latencies: list[float] = []

    for scenario in scenarios:
        ticket_data = scenario.ticket.model_dump(mode="json")
        ticket_result = _call_triage(client, endpoint, ticket_data, timeout_seconds)
        result.ticket_results.append(ticket_result)
        latencies.append(ticket_result.latency_ms)

        if ticket_result.error is None:
            result.successful += 1
        else:
            result.failed += 1

    client.close()

    result.latency_p50_ms, result.latency_p95_ms = _compute_latency_percentiles(
        latencies
    )
    return result
