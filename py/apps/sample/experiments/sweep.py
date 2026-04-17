#!/usr/bin/env python3
"""FDEBench Experiment Sweep.

Runs multiple FDEBench experiments in sequence with different model
configurations and compiles a comparison report.

Usage:
    python sweep.py --endpoint http://localhost:8000

Results are saved to experiments/results/{experiment_id}.json for each run.
A comparison summary is printed at the end.
"""

import argparse
import asyncio
import json
import logging
import subprocess
import sys
from pathlib import Path
from typing import Any

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)-5s %(message)s",
)
logger = logging.getLogger(__name__)

# Results directory
_RESULTS_DIR = Path(__file__).resolve().parent / "results"

# ── Default Experiment Configurations ──────────────────────────────
DEFAULT_EXPERIMENTS = [
    {
        "id": "E1-nano-all",
        "name": "E1: gpt-5-4-nano (all tasks)",
        "triage_model": "gpt-5-4-nano",
        "extract_model": "gpt-5-4-nano",
        "orchestrate_model": "gpt-5-4-nano",
    },
    {
        "id": "E2-mini-all",
        "name": "E2: gpt-5-4-mini (all tasks)",
        "triage_model": "gpt-5-4-mini",
        "extract_model": "gpt-5-4-mini",
        "orchestrate_model": "gpt-5-4-mini",
    },
    {
        "id": "E3-base-all",
        "name": "E3: gpt-5-4 (all tasks)",
        "triage_model": "gpt-5-4",
        "extract_model": "gpt-5-4",
        "orchestrate_model": "gpt-5-4",
    },
    {
        "id": "E4-mixed-nano-base",
        "name": "E4: gpt-5-4-nano (T1), gpt-5-4 (T2/T3)",
        "triage_model": "gpt-5-4-nano",
        "extract_model": "gpt-5-4",
        "orchestrate_model": "gpt-5-4",
    },
    {
        "id": "E5-mixed-nano-mini",
        "name": "E5: gpt-5-4-nano (T1), gpt-5-4 (T2), o4-mini (T3)",
        "triage_model": "gpt-5-4-nano",
        "extract_model": "gpt-5-4",
        "orchestrate_model": "o4-mini",
    },
]


def _load_result(experiment_id: str) -> dict[str, Any] | None:
    """Load a result JSON file."""
    result_file = _RESULTS_DIR / f"{experiment_id}.json"
    if not result_file.exists():
        logger.warning("Result file not found: %s", result_file)
        return None
    try:
        return json.loads(result_file.read_text(encoding="utf-8"))
    except Exception as e:
        logger.error("Failed to load result file %s: %s", result_file, e)
        return None


def _print_comparison_table(results: list[dict[str, Any]]) -> None:
    """Print a comparison table of all experiment results."""
    if not results:
        print("\nNo results to compare.\n")
        return

    # Sort by FDEBench score (descending)
    sorted_results = sorted(results, key=lambda r: r.get("fdebench_composite", 0), reverse=True)

    print()
    print("=" * 120)
    print("  FDEBench Sweep Results — Sorted by Composite Score")
    print("=" * 120)
    print()
    print(
        f"{'Rank':<5} {'Experiment':<20} {'FDEBench':<12} "
        f"{'Resolution':<12} {'Efficiency':<12} {'Robustness':<12} "
        f"{'Timestamp':<20}"
    )
    print("-" * 120)

    for rank, result in enumerate(sorted_results, start=1):
        exp_id = result.get("experiment_id", "unknown")
        fdebench = result.get("fdebench_composite", 0)
        resolution = result.get("resolution_avg", 0)
        efficiency = result.get("efficiency_avg", 0)
        robustness = result.get("robustness_avg", 0)
        timestamp = result.get("timestamp", "unknown")
        # Parse ISO timestamp to get just the date and time
        if timestamp and "T" in timestamp:
            timestamp = timestamp.split("T")[1].split(".")[0]

        print(
            f"{rank:<5} {exp_id:<20} {fdebench:>10.2f}   {resolution:>10.2f}   "
            f"{efficiency:>10.2f}   {robustness:>10.2f}   {timestamp:<20}"
        )

    print()
    print("=" * 120)
    print()

    # Per-task detail
    print("Per-Task Breakdown:")
    print("-" * 120)
    print(f"{'Experiment':<20} {'Triage (T1)':<20} {'Extract (T2)':<20} {'Orchestrate (T3)':<20}")
    print("-" * 120)

    for result in sorted_results:
        exp_id = result.get("experiment_id", "unknown")
        tasks = result.get("tasks", [])
        task_scores = [f"{t.get('tier1_score', 0):.2f}" for t in tasks]
        while len(task_scores) < 3:
            task_scores.append("—")

        print(f"{exp_id:<20} {task_scores[0]:<20} {task_scores[1]:<20} {task_scores[2]:<20}")

    print()
    print("=" * 120)
    print()


async def run_experiment(endpoint: str, config: dict[str, str]) -> bool:
    """Run a single experiment using run_experiment.py."""
    logger.info("Running experiment: %s", config["id"])
    logger.info("  %s", config["name"])

    cmd = [
        sys.executable,
        str(Path(__file__).resolve().parent / "run_experiment.py"),
        "--experiment-id",
        config["id"],
        "--triage-model",
        config["triage_model"],
        "--extract-model",
        config["extract_model"],
        "--orchestrate-model",
        config["orchestrate_model"],
        "--endpoint",
        endpoint,
    ]

    try:
        result = subprocess.run(cmd, check=True, capture_output=False)
        return result.returncode == 0
    except subprocess.CalledProcessError as e:
        logger.error("Experiment %s failed: %s", config["id"], e)
        return False


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Run multiple FDEBench experiments and compare results.",
    )
    parser.add_argument(
        "--endpoint",
        required=True,
        help="Base URL of the deployed service",
    )
    parser.add_argument(
        "--experiments",
        nargs="+",
        help="Specific experiment IDs to run (default: all)",
    )
    parser.add_argument(
        "--concurrency",
        type=int,
        default=5,
        help="Max concurrent requests per experiment (default: 5)",
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

    logger.info("FDEBench Sweep — Running multiple experiments")
    logger.info("Endpoint: %s", args.endpoint)
    logger.info("Results directory: %s", _RESULTS_DIR)

    _RESULTS_DIR.mkdir(parents=True, exist_ok=True)

    # Determine which experiments to run
    experiments_to_run = DEFAULT_EXPERIMENTS
    if args.experiments:
        experiments_to_run = [exp for exp in DEFAULT_EXPERIMENTS if exp["id"] in args.experiments]
        if not experiments_to_run:
            logger.error("No matching experiments found")
            sys.exit(1)

    logger.info("Running %d experiments...", len(experiments_to_run))
    print()

    # Run experiments sequentially
    results = []
    for idx, config in enumerate(experiments_to_run, start=1):
        logger.info("[%d/%d] %s", idx, len(experiments_to_run), config["id"])
        success = await run_experiment(args.endpoint, config)

        if success:
            result = _load_result(config["id"])
            if result:
                results.append(result)
        else:
            logger.warning("Experiment %s did not complete successfully", config["id"])

        print()

    # Print comparison table
    if results:
        _print_comparison_table(results)
    else:
        logger.error("No experiments completed successfully")
        sys.exit(1)


if __name__ == "__main__":
    asyncio.run(main())
