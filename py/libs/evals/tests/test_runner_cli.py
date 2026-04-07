# Copyright (c) Microsoft. All rights reserved.
"""Tests for the eval runner CLI (``python -m ms.evals_core``)."""

import tempfile
from pathlib import Path
from unittest.mock import MagicMock
from unittest.mock import patch

import pytest

from ms.evals_core.constants import Category
from ms.evals_core.constants import Priority
from ms.evals_core.constants import Team
from ms.evals_core.datasets import DatasetKind
from ms.evals_core.eval_models import DimensionAggregates
from ms.evals_core.eval_models import DimensionScores
from ms.evals_core.eval_models import EvalResult
from ms.evals_core.eval_models import EvalSummary
from ms.evals_core.eval_models import GoldAnswer
from ms.evals_core.eval_models import TriageResponse
from ms.evals_core.runner_cli import _resolve_dataset
from ms.evals_core.runner_cli import main


class TestResolveDataset:
    """Tests for dataset name resolution."""

    def test_exact_name(self) -> None:
        assert _resolve_dataset("sample") == DatasetKind.SAMPLE

    def test_public_eval(self) -> None:
        assert _resolve_dataset("public_eval") == DatasetKind.PUBLIC_EVAL

    def test_data_cleanup_full_name(self) -> None:
        assert _resolve_dataset("eval_data_cleanup") == DatasetKind.DATA_CLEANUP

    def test_data_cleanup_short_name(self) -> None:
        assert _resolve_dataset("data_cleanup") == DatasetKind.DATA_CLEANUP

    def test_responsible_ai_full_name(self) -> None:
        assert _resolve_dataset("eval_responsible_ai") == DatasetKind.RESPONSIBLE_AI

    def test_responsible_ai_short_name(self) -> None:
        assert _resolve_dataset("responsible_ai") == DatasetKind.RESPONSIBLE_AI

    def test_case_insensitive(self) -> None:
        assert _resolve_dataset("SAMPLE") == DatasetKind.SAMPLE
        assert _resolve_dataset("Data_Cleanup") == DatasetKind.DATA_CLEANUP

    def test_strips_whitespace(self) -> None:
        assert _resolve_dataset("  sample  ") == DatasetKind.SAMPLE

    def test_unknown_dataset_raises(self) -> None:
        with pytest.raises(SystemExit):
            _resolve_dataset("nonexistent_dataset")


class TestMainArgParsing:
    """Tests for CLI argument parsing."""

    def test_missing_endpoint_exits(self) -> None:
        with pytest.raises(SystemExit):
            main(["--dataset", "sample"])

    def test_missing_dataset_exits(self) -> None:
        with pytest.raises(SystemExit):
            main(["--endpoint", "http://localhost:8000"])

    def test_unknown_dataset_exits(self) -> None:
        with pytest.raises(SystemExit):
            main(["--endpoint", "http://localhost:8000", "--dataset", "nonexistent"])


class TestMainExecution:
    """Tests for the main CLI execution path using mocked runner."""

    @staticmethod
    def _make_summary(*, errored: int = 0) -> EvalSummary:
        gold = GoldAnswer(
            ticket_id="INC-0001",
            category=Category.NETWORK,
            priority=Priority.P3,
            assigned_team=Team.NETWORK_OPS,
            needs_escalation=False,
            missing_information=[],
            next_best_action="Check VPN.",
            remediation_steps=["Step 1"],
        )
        response = TriageResponse(
            ticket_id="INC-0001",
            category="Network & Connectivity",
            priority="P3",
            assigned_team="Network Operations",
            needs_escalation=False,
            missing_information=[],
            next_best_action="Check VPN.",
            remediation_steps=["Step 1"],
        )
        scores = DimensionScores(
            category=1.0,
            priority=1.0,
            routing=1.0,
            escalation=1.0,
            missing_info=1.0,
            weighted_total=0.85,
        )
        result = EvalResult(
            ticket_id="INC-0001",
            scores=scores,
            response=response,
            gold=gold,
            latency_ms=42.0,
            error="connection failed" if errored else None,
        )
        return EvalSummary(
            dataset_kind="sample",
            tickets_total=1,
            tickets_scored=0 if errored else 1,
            tickets_errored=errored,
            dimension_scores=DimensionAggregates(
                category=1.0,
                priority=1.0,
                routing=1.0,
                missing_info=1.0,
                escalation=1.0,
            ),
            classification_score=85.0,
            results=[result],
        )

    @patch("ms.evals_core.runner_cli.EvalRunner")
    def test_successful_run_returns_zero(self, mock_runner_cls: MagicMock) -> None:
        mock_runner = MagicMock()
        mock_runner.run.return_value = self._make_summary()
        mock_runner_cls.return_value = mock_runner

        code = main(["--endpoint", "http://localhost:8000", "--dataset", "sample"])
        assert code == 0

    @patch("ms.evals_core.runner_cli.EvalRunner")
    def test_errored_run_returns_one(self, mock_runner_cls: MagicMock) -> None:
        mock_runner = MagicMock()
        mock_runner.run.return_value = self._make_summary(errored=1)
        mock_runner_cls.return_value = mock_runner

        code = main(["--endpoint", "http://localhost:8000", "--dataset", "sample"])
        assert code == 1

    @patch("ms.evals_core.runner_cli.EvalRunner")
    def test_file_not_found_returns_two(self, mock_runner_cls: MagicMock) -> None:
        mock_runner = MagicMock()
        mock_runner.run.side_effect = FileNotFoundError("missing file")
        mock_runner_cls.return_value = mock_runner

        code = main(["--endpoint", "http://localhost:8000", "--dataset", "sample"])
        assert code == 2

    @patch("ms.evals_core.runner_cli.EvalRunner")
    def test_data_cleanup_dataset_resolves(self, mock_runner_cls: MagicMock) -> None:
        mock_runner = MagicMock()
        mock_runner.run.return_value = self._make_summary()
        mock_runner_cls.return_value = mock_runner

        code = main(["--endpoint", "http://localhost:8000", "--dataset", "eval_data_cleanup"])
        assert code == 0
        mock_runner.run.assert_called_once_with(DatasetKind.DATA_CLEANUP, tickets_dir=None)

    @patch("ms.evals_core.runner_cli.EvalRunner")
    def test_responsible_ai_dataset_resolves(self, mock_runner_cls: MagicMock) -> None:
        mock_runner = MagicMock()
        mock_runner.run.return_value = self._make_summary()
        mock_runner_cls.return_value = mock_runner

        code = main(["--endpoint", "http://localhost:8000", "--dataset", "responsible_ai"])
        assert code == 0
        mock_runner.run.assert_called_once_with(DatasetKind.RESPONSIBLE_AI, tickets_dir=None)

    @patch("ms.evals_core.runner_cli.EvalRunner")
    def test_custom_timeout(self, mock_runner_cls: MagicMock) -> None:
        mock_runner = MagicMock()
        mock_runner.run.return_value = self._make_summary()
        mock_runner_cls.return_value = mock_runner

        code = main(["--endpoint", "http://localhost:8000", "--dataset", "sample", "--timeout", "60"])
        assert code == 0
        mock_runner_cls.assert_called_once_with("http://localhost:8000", timeout=60.0)

    @patch("ms.evals_core.runner_cli.EvalRunner")
    def test_output_file(self, mock_runner_cls: MagicMock) -> None:
        mock_runner = MagicMock()
        mock_runner.run.return_value = self._make_summary()
        mock_runner_cls.return_value = mock_runner

        with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as f:
            output_path = f.name

        code = main(
            [
                "--endpoint",
                "http://localhost:8000",
                "--dataset",
                "sample",
                "--output",
                output_path,
            ]
        )
        assert code == 0
        assert Path(output_path).exists()
        Path(output_path).unlink()
