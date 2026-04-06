# Copyright (c) Microsoft. All rights reserved.
"""Evaluation runner that calls a live triage endpoint and scores responses.

The runner:
1. Loads a dataset (tickets + gold answers)
2. Sends each ticket to the target endpoint via HTTP POST
3. Scores each response against the gold answer
4. Aggregates results into an ``EvalSummary``
"""

import logging
import time
from pathlib import Path

import httpx

from ms.evals_core.constants import Category
from ms.evals_core.constants import Priority
from ms.evals_core.constants import Team
from ms.evals_core.datasets import DatasetKind
from ms.evals_core.datasets import load_dataset
from ms.evals_core.eval_models import DimensionAggregates
from ms.evals_core.eval_models import DimensionScores
from ms.evals_core.eval_models import EvalResult
from ms.evals_core.eval_models import EvalSummary
from ms.evals_core.eval_models import GoldAnswer
from ms.evals_core.eval_models import Ticket
from ms.evals_core.eval_models import TriageResponse
from ms.evals_core.scoring import compute_aggregate_scores
from ms.evals_core.scoring import score_ticket

logger = logging.getLogger(__name__)

_DEFAULT_TIMEOUT_SECONDS = 30.0


class EvalRunner:
    """Run evaluations against a live triage endpoint.

    Parameters
    ----------
    endpoint:
        Base URL of the triage service (e.g. ``http://localhost:8000``).
    timeout:
        Per-request timeout in seconds.  Matches the platform's 30 s default.
    """

    def __init__(
        self,
        endpoint: str,
        *,
        timeout: float = _DEFAULT_TIMEOUT_SECONDS,
    ) -> None:
        self._endpoint = endpoint.rstrip("/")
        self._timeout = timeout

    def run(
        self,
        kind: DatasetKind,
        *,
        tickets_dir: Path | None = None,
    ) -> EvalSummary:
        """Execute an evaluation run for the specified dataset.

        Parameters
        ----------
        kind:
            Which evaluation dataset to use.
        tickets_dir:
            Override path for ticket JSON files.

        Returns
        -------
        EvalSummary:
            Full results including per-ticket breakdowns and aggregate scores.

        Raises
        ------
        ValueError:
            If the dataset has no gold answers (scoring requires gold).
        """
        tickets, gold_answers = load_dataset(kind, tickets_dir=tickets_dir)

        if gold_answers is None:
            msg = f"Dataset {kind!r} has no gold answers — cannot score."
            raise ValueError(msg)

        gold_by_id = {g.ticket_id: g for g in gold_answers}

        results: list[EvalResult] = []
        scored_responses: list[TriageResponse] = []
        scored_golds: list[GoldAnswer] = []
        scored_dimensions: list[DimensionScores] = []
        errored = 0

        with httpx.Client(timeout=self._timeout) as client:
            for ticket in tickets:
                result = self._evaluate_ticket(client, ticket, gold_by_id.get(ticket.ticket_id))
                results.append(result)

                if result.error is not None:
                    errored += 1
                else:
                    gold = gold_by_id[ticket.ticket_id]
                    scored_responses.append(result.response)
                    scored_golds.append(gold)
                    scored_dimensions.append(result.scores)

        if scored_dimensions:
            dimension_agg, classification_score = compute_aggregate_scores(
                scored_dimensions,
                scored_responses,
                scored_golds,
            )
        else:
            dimension_agg = DimensionAggregates(
                category=0.0,
                priority=0.0,
                routing=0.0,
                missing_info=0.0,
                escalation=0.0,
            )
            classification_score = 0.0

        return EvalSummary(
            dataset_kind=kind.value,
            tickets_total=len(tickets),
            tickets_scored=len(scored_dimensions),
            tickets_errored=errored,
            dimension_scores=dimension_agg,
            classification_score=classification_score,
            results=results,
        )

    def _evaluate_ticket(
        self,
        client: httpx.Client,
        ticket: Ticket,
        gold: GoldAnswer | None,
    ) -> EvalResult:
        """Send a single ticket to the endpoint, score against gold."""
        start = time.monotonic()

        try:
            resp = client.post(
                f"{self._endpoint}/triage",
                json=ticket.model_dump(),
            )
            resp.raise_for_status()
            latency_ms = (time.monotonic() - start) * 1000

            triage = TriageResponse.model_validate(resp.json())

        except Exception as exc:
            latency_ms = (time.monotonic() - start) * 1000
            logger.warning("Ticket %s failed: %s", ticket.ticket_id, exc)

            empty_response = TriageResponse(
                ticket_id=ticket.ticket_id,
                category="",
                priority="",
                assigned_team="",
                needs_escalation=False,
                missing_information=[],
                next_best_action="",
                remediation_steps=[],
            )

            if gold is not None:
                scores = score_ticket(empty_response, gold)
            else:
                scores = DimensionScores(
                    category=0.0,
                    priority=0.0,
                    routing=0.0,
                    escalation=0.0,
                    missing_info=0.0,
                    weighted_total=0.0,
                )

            return EvalResult(
                ticket_id=ticket.ticket_id,
                scores=scores,
                response=empty_response,
                gold=gold or _placeholder_gold(ticket.ticket_id),
                latency_ms=latency_ms,
                error=str(exc),
            )

        if gold is not None:
            scores = score_ticket(triage, gold)
        else:
            scores = DimensionScores(
                category=0.0,
                priority=0.0,
                routing=0.0,
                escalation=0.0,
                missing_info=0.0,
                weighted_total=0.0,
            )

        return EvalResult(
            ticket_id=ticket.ticket_id,
            scores=scores,
            response=triage,
            gold=gold or _placeholder_gold(ticket.ticket_id),
            latency_ms=latency_ms,
        )


def _placeholder_gold(ticket_id: str) -> GoldAnswer:
    """Return a minimal gold answer when none is available."""
    return GoldAnswer(
        ticket_id=ticket_id,
        category=Category.GENERAL_INQUIRY,
        priority=Priority.P4,
        assigned_team=Team.NONE,
        needs_escalation=False,
        missing_information=[],
        next_best_action="",
        remediation_steps=[],
    )
