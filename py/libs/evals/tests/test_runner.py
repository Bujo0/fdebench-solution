# Copyright (c) Microsoft. All rights reserved.
"""Tests for the evaluation runner."""


import httpx
import pytest
import respx

from ms.evals_core.datasets import DatasetKind
from ms.evals_core.datasets import load_dataset
from ms.evals_core.eval_models import GoldAnswer
from ms.evals_core.eval_runner import EvalRunner


def _gold_response_for(gold: GoldAnswer) -> dict:
    """Build a mock API response from a gold answer."""
    return {
        "ticket_id": gold.ticket_id,
        "category": gold.category,
        "priority": gold.priority,
        "assigned_team": gold.assigned_team,
        "needs_escalation": gold.needs_escalation,
        "missing_information": [str(m) for m in gold.missing_information],
        "next_best_action": gold.next_best_action,
        "remediation_steps": list(gold.remediation_steps),
    }


class TestEvalRunner:
    """Tests for EvalRunner using mocked HTTP responses."""

    @respx.mock
    def test_perfect_score_data_cleanup(self) -> None:
        """A perfect responder should score 85/85 on data cleanup."""
        _, gold_answers = load_dataset(DatasetKind.DATA_CLEANUP)
        assert gold_answers is not None

        route = respx.post("http://test:8000/triage")
        responses = iter([_gold_response_for(g) for g in gold_answers])

        def handler(request: httpx.Request) -> httpx.Response:
            return httpx.Response(200, json=next(responses))

        route.mock(side_effect=handler)

        runner = EvalRunner("http://test:8000")
        summary = runner.run(DatasetKind.DATA_CLEANUP)

        assert summary.tickets_total == 38
        assert summary.tickets_scored == 38
        assert summary.tickets_errored == 0
        assert summary.classification_score == 85.0

    @respx.mock
    def test_perfect_score_responsible_ai(self) -> None:
        """A perfect responder should score 85/85 on responsible AI."""
        _, gold_answers = load_dataset(DatasetKind.RESPONSIBLE_AI)
        assert gold_answers is not None

        route = respx.post("http://test:8000/triage")
        responses = iter([_gold_response_for(g) for g in gold_answers])

        def handler(request: httpx.Request) -> httpx.Response:
            return httpx.Response(200, json=next(responses))

        route.mock(side_effect=handler)

        runner = EvalRunner("http://test:8000")
        summary = runner.run(DatasetKind.RESPONSIBLE_AI)

        assert summary.tickets_total == 35
        assert summary.tickets_scored == 35
        assert summary.tickets_errored == 0
        assert summary.classification_score == 85.0

    @respx.mock
    def test_all_errors(self) -> None:
        """All requests failing should result in all errored."""
        respx.post("http://test:8000/triage").mock(
            return_value=httpx.Response(500, json={"error": "Internal Server Error"})
        )

        runner = EvalRunner("http://test:8000")
        summary = runner.run(DatasetKind.DATA_CLEANUP)

        assert summary.tickets_errored == 38
        assert summary.tickets_scored == 0

    @respx.mock
    def test_partial_failures(self) -> None:
        """Mix of successes and failures."""
        _, gold_answers = load_dataset(DatasetKind.DATA_CLEANUP)
        assert gold_answers is not None

        call_count = 0
        route = respx.post("http://test:8000/triage")

        def handler(request: httpx.Request) -> httpx.Response:
            nonlocal call_count
            call_count += 1
            if call_count <= 5:
                return httpx.Response(500, json={"error": "fail"})
            idx = call_count - 1
            if idx < len(gold_answers):
                return httpx.Response(200, json=_gold_response_for(gold_answers[idx]))
            return httpx.Response(200, json=_gold_response_for(gold_answers[0]))

        route.mock(side_effect=handler)

        runner = EvalRunner("http://test:8000")
        summary = runner.run(DatasetKind.DATA_CLEANUP)

        assert summary.tickets_errored == 5
        assert summary.tickets_scored == 33

    def test_no_gold_raises(self) -> None:
        """Running against a dataset with no gold should raise ValueError."""
        runner = EvalRunner("http://test:8000")
        with pytest.raises(ValueError, match="no gold answers"):
            runner.run(DatasetKind.PUBLIC_EVAL)
