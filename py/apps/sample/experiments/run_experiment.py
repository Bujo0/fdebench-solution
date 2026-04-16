#!/usr/bin/env python3
"""FDEBench Experiment Runner.

Runs the FDEBench eval harness with a specific model configuration
and captures results to a structured JSON file.

Usage:
    python run_experiment.py \\
        --experiment-id exp-001 \\
        --triage-model gpt-5-4-nano \\
        --extract-model gpt-5-4 \\
        --orchestrate-model gpt-5-4 \\
        --endpoint http://localhost:8000

Results are saved to experiments/results/{experiment_id}.json
"""

import argparse
import asyncio
import json
import logging
import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

# Add libraries to the import path
_REPO_ROOT = Path(__file__).resolve().parent.parent.parent.parent
sys.path.insert(0, str(_REPO_ROOT / "common" / "libs" / "fdebenchkit" / "src"))
sys.path.insert(0, str(_REPO_ROOT / "common" / "libs" / "models" / "src"))

from ms.common.fdebenchkit.runner import run_scoring, ScoringResult, PreflightValidationError
from ms.common.fdebenchkit.registry import get_task_definition, TaskRun

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)-5s %(message)s",
)
logger = logging.getLogger(__name__)

# ── Data paths ──────────────────────────────────────────────────────
_DATA_DIR = _REPO_ROOT / "data"

_TASK_DATASETS: dict[str, dict[str, Path]] = {
    "triage": {
        "input": _DATA_DIR / "task1" / "sample.json",
        "gold": _DATA_DIR / "task1" / "sample_gold.json",
    },
    "triage-50": {
        "input": _DATA_DIR / "task1" / "public_eval_50.json",
        "gold": _DATA_DIR / "task1" / "public_eval_50_gold.json",
    },
    "extract": {
        "input": _DATA_DIR / "task2" / "public_eval_50.json",
        "gold": _DATA_DIR / "task2" / "public_eval_50_gold.json",
    },
    "orchestrate": {
        "input": _DATA_DIR / "task3" / "public_eval_50.json",
        "gold": _DATA_DIR / "task3" / "public_eval_50_gold.json",
    },
}

_TASK_ID_MAP = {
    "triage": "ticket_triage",
    "triage-50": "ticket_triage",
    "extract": "document_extraction",
    "orchestrate": "workflow_orchestration",
}

_MOCK_RESPONSES_PATH = _DATA_DIR / "task3" / "public_eval_50_mock_responses.json"
_MOCK_SERVICE_SCRIPT = _REPO_ROOT / "apps" / "eval" / "mock_tool_service.py"
_MOCK_SERVICE_PORT = 9090
_MOCK_BASE_URL = f"http://127.0.0.1:{_MOCK_SERVICE_PORT}/scenario"

# Results directory (relative to this script)
_RESULTS_DIR = Path(__file__).resolve().parent / "results"


def _port_in_use(port: int) -> bool:
    """Check if a port is already in use."""
    import socket
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(("127.0.0.1", port)) == 0


def _start_mock_service() -> subprocess.Popen | None:
    """Start the mock tool service for Task 3 in a subprocess."""
    if not _MOCK_RESPONSES_PATH.exists():
        logger.warning("Mock responses not found: %s — Task 3 tool calls will fail", _MOCK_RESPONSES_PATH)
        return None

    if _port_in_use(_MOCK_SERVICE_PORT):
        logger.info("Mock tool service already running on port %d", _MOCK_SERVICE_PORT)
        return None

    logger.info("Starting mock tool service on port %d ...", _MOCK_SERVICE_PORT)
    import signal
    proc = subprocess.Popen(
        [sys.executable, str(_MOCK_SERVICE_SCRIPT), "--port", str(_MOCK_SERVICE_PORT)],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.PIPE,
    )
    # Wait for the server to be ready (up to 5 seconds)
    import time
    for _ in range(50):
        if _port_in_use(_MOCK_SERVICE_PORT):
            logger.info("Mock tool service ready")
            return proc
        time.sleep(0.1)
    logger.warning("Mock tool service did not start within 5s — Task 3 tool calls may fail")
    return proc


def _stop_mock_service(proc: subprocess.Popen | None) -> None:
    """Gracefully shut down the mock service subprocess."""
    if proc is None:
        return
    import signal
    proc.send_signal(signal.SIGTERM)
    try:
        proc.wait(timeout=3)
    except subprocess.TimeoutExpired:
        proc.kill()


def _rewrite_task3_urls(items: list[dict]) -> list[dict]:
    """Replace placeholder tool endpoints with the local mock service URL."""
    rewritten: list[dict] = []
    for item in items:
        updated = dict(item)
        task_id = updated.get("task_id", "")
        mock_url = f"{_MOCK_BASE_URL}/{task_id}"
        updated["mock_service_url"] = mock_url
        if "available_tools" in updated:
            new_tools = []
            for tool in updated["available_tools"]:
                t = dict(tool)
                t["endpoint"] = f"{mock_url}/{t['name']}"
                new_tools.append(t)
            updated["available_tools"] = new_tools
        rewritten.append(updated)
    return rewritten


def _load_dataset(path: Path, id_field: str) -> list[dict]:
    """Load a JSON array dataset."""
    if not path.exists():
        logger.error("Dataset not found: %s", path)
        sys.exit(1)
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, list):
        logger.error("Dataset must be a JSON array: %s", path)
        sys.exit(1)
    logger.info("Loaded %d items from %s", len(data), path.name)
    return data


def _build_task_runs(tasks: list[str]) -> list[TaskRun]:
    """Build TaskRun objects for the requested tasks."""
    runs: list[TaskRun] = []

    for task_key in tasks:
        task_id = _TASK_ID_MAP[task_key]
        definition = get_task_definition(task_id)

        paths = _TASK_DATASETS[task_key]
        input_items = _load_dataset(paths["input"], definition.request_id_key)
        gold_items = _load_dataset(paths["gold"], definition.request_id_key)

        # Task 3: rewrite tool endpoints to point at the local mock service
        if task_id == "workflow_orchestration":
            input_items = _rewrite_task3_urls(input_items)

        runs.append(
            TaskRun(
                definition=definition,
                input_items=input_items,
                gold_items=gold_items,
            )
        )

    return runs


def _result_to_dict(result: ScoringResult) -> dict[str, Any]:
    """Convert ScoringResult to a serializable dictionary."""
    task_data = []
    for task in result.task_scores:
        task_dict = {
            "name": task.name,
            "label": task.label,
            "tier1_score": round(task.tier1_score, 2),
            "resolution": round(task.resolution, 2),
            "efficiency_score": round(task.efficiency_score, 2),
            "robustness_score": round(task.robustness_score, 2),
            "latency_p95_ms": round(task.latency_p95_ms, 1),
            "latency_score": round(task.latency_score, 4),
            "cost_score": round(task.cost_score, 4),
            "adversarial_accuracy": round(task.adversarial_accuracy, 2),
            "api_resilience": round(task.api_resilience, 2),
            "items_scored": task.items_scored,
            "items_errored": task.items_errored,
            "primary_model": task.primary_model,
            "dimension_scores": {k: round(v, 4) for k, v in task.dimension_scores.items()},
            "dimension_weights": {k: v for k, v in task.dimension_weights.items()},
            "probe_results": task.probe_results or {},
        }
        task_data.append(task_dict)

    return {
        "fdebench_composite": round(result.total, 2),
        "resolution_avg": round(result.resolution_score, 2),
        "efficiency_avg": round(result.efficiency_score, 2),
        "robustness_avg": round(result.robustness_score, 2),
        "tasks": task_data,
        "errors": result.errors or [],
    }


def _print_summary(
    experiment_id: str,
    model_config: dict[str, str],
    result: ScoringResult,
) -> None:
    """Print a summary table of key metrics."""
    w = 70
    print()
    print("=" * w)
    print(f"  Experiment: {experiment_id}")
    print("=" * w)
    print()
    print(f"  FDEBench Composite:      {result.total:6.1f} / 100")
    print(f"  Resolution (avg):        {result.resolution_score:6.1f} / 100")
    print(f"  Efficiency (avg):        {result.efficiency_score:6.1f} / 100")
    print(f"  Robustness (avg):        {result.robustness_score:6.1f} / 100")
    print()
    print("-" * w)
    print("  Model Configuration")
    print("-" * w)
    for task, model in sorted(model_config.items()):
        print(f"    {task:15s}  {model}")
    print()
    print("-" * w)
    print("  Per-Task Scores")
    print("-" * w)
    for task in result.task_scores:
        print(f"  {task.label:30s}  {task.tier1_score:6.1f}  (R:{task.resolution:5.1f} E:{task.efficiency_score:5.1f} Ro:{task.robustness_score:5.1f})")
    print()
    print("=" * w)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run a single FDEBench experiment with specified model configuration.",
    )
    parser.add_argument(
        "--experiment-id",
        required=True,
        help="Experiment identifier (used for output filename)",
    )
    parser.add_argument(
        "--triage-model",
        default="gpt-5-4-nano",
        help="Model for triage task (Task 1)",
    )
    parser.add_argument(
        "--extract-model",
        default="gpt-5-4",
        help="Model for extraction task (Task 2)",
    )
    parser.add_argument(
        "--orchestrate-model",
        default="gpt-5-4",
        help="Model for orchestration task (Task 3)",
    )
    parser.add_argument(
        "--endpoint",
        required=True,
        help="Base URL of the deployed service",
    )
    parser.add_argument(
        "--concurrency",
        type=int,
        default=5,
        help="Max concurrent requests (default: 5)",
    )
    parser.add_argument(
        "--timeout",
        type=float,
        default=30.0,
        help="Per-request timeout in seconds (default: 30)",
    )
    return parser.parse_args()


async def main() -> None:
    args = parse_args()
    mock_proc: subprocess.Popen | None = None

    # Model configuration
    model_config = {
        "triage": args.triage_model,
        "extract": args.extract_model,
        "orchestrate": args.orchestrate_model,
    }

    # Set environment variables for the models
    os.environ["TRIAGE_MODEL"] = args.triage_model
    os.environ["EXTRACT_MODEL"] = args.extract_model
    os.environ["ORCHESTRATE_MODEL"] = args.orchestrate_model

    logger.info("Starting experiment: %s", args.experiment_id)
    logger.info("Model configuration: %s", model_config)
    logger.info("Endpoint: %s", args.endpoint)

    # Check data files exist
    for key in ["triage", "extract", "orchestrate"]:
        paths = _TASK_DATASETS[key + "-50" if key == "triage" else key]
        for label, path in paths.items():
            if not path.exists():
                logger.error("Missing %s dataset: %s", label, path)
                sys.exit(1)

    # Start mock tool service if needed
    mock_proc = _start_mock_service()

    task_runs = _build_task_runs(["triage", "extract", "orchestrate"])

    try:
        result = await run_scoring(
            args.endpoint,
            task_runs=task_runs,
            concurrency=args.concurrency,
            timeout=args.timeout,
            max_retries=2,
            warm_up_requests=3,
        )
    except PreflightValidationError as exc:
        logger.error("Preflight validation failed: %s", exc)
        if exc.validation_summary:
            for check in exc.validation_summary.get("endpoint_checks", []):
                status = "OK" if check.get("ok") else "FAIL"
                logger.error("  %s %s: %s", status, check.get("name"), check.get("error_message", ""))
        sys.exit(1)
    finally:
        _stop_mock_service(mock_proc)

    # Print summary
    _print_summary(args.experiment_id, model_config, result)

    # Save results
    _RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    result_file = _RESULTS_DIR / f"{args.experiment_id}.json"

    results_data = {
        "experiment_id": args.experiment_id,
        "timestamp": datetime.now().isoformat(),
        "model_config": model_config,
        "endpoint": args.endpoint,
    }
    results_data.update(_result_to_dict(result))

    result_file.write_text(json.dumps(results_data, indent=2), encoding="utf-8")
    logger.info("Results saved to: %s", result_file)

    # Exit code: 0 if scored, 1 if all items errored
    if result.items_scored == 0:
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
