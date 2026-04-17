#!/usr/bin/env python3
"""
Example: How to use the experiment runner programmatically.

This script demonstrates how to:
1. Run a single experiment with specific models
2. Load and inspect results
3. Compare multiple experiments
"""

import json
import subprocess
import sys
from pathlib import Path

RESULTS_DIR = Path(__file__).resolve().parent / "results"
SCRIPT_DIR = Path(__file__).resolve().parent


def run_single_experiment(
    experiment_id: str,
    triage_model: str,
    extract_model: str,
    orchestrate_model: str,
    endpoint: str = "http://localhost:8000",
) -> bool:
    """Run a single experiment and return success status."""
    cmd = [
        sys.executable,
        str(SCRIPT_DIR / "run_experiment.py"),
        "--experiment-id",
        experiment_id,
        "--triage-model",
        triage_model,
        "--extract-model",
        extract_model,
        "--orchestrate-model",
        orchestrate_model,
        "--endpoint",
        endpoint,
    ]
    result = subprocess.run(cmd)
    return result.returncode == 0


def load_result(experiment_id: str) -> dict | None:
    """Load a result file and return the parsed JSON."""
    result_file = RESULTS_DIR / f"{experiment_id}.json"
    if not result_file.exists():
        return None
    return json.loads(result_file.read_text())


def compare_experiments(exp_ids: list[str]) -> None:
    """Load and compare multiple experiments."""
    print("\n" + "=" * 80)
    print("Experiment Comparison")
    print("=" * 80 + "\n")

    results = []
    for exp_id in exp_ids:
        result = load_result(exp_id)
        if result:
            results.append(result)
        else:
            print(f"⚠️  Could not load result for {exp_id}")

    if not results:
        print("No results to compare")
        return

    # Sort by FDEBench score
    sorted_results = sorted(results, key=lambda r: r["fdebench_composite"], reverse=True)

    # Print table
    print(f"{'Rank':<5} {'Experiment':<25} {'FDEBench':<12} {'Resolution':<12} {'Efficiency':<12} {'Robustness':<12}")
    print("-" * 80)

    for rank, result in enumerate(sorted_results, 1):
        exp_id = result["experiment_id"]
        fdebench = result["fdebench_composite"]
        resolution = result["resolution_avg"]
        efficiency = result["efficiency_avg"]
        robustness = result["robustness_avg"]

        print(
            f"{rank:<5} {exp_id:<25} {fdebench:>10.2f}   {resolution:>10.2f}   "
            f"{efficiency:>10.2f}   {robustness:>10.2f}"
        )

    print()

    # Show model configurations
    print("Model Configurations:")
    print("-" * 80)
    for result in sorted_results:
        config = result["model_config"]
        print(f"  {result['experiment_id']:<25}")
        print(f"    Triage:       {config['triage']}")
        print(f"    Extract:      {config['extract']}")
        print(f"    Orchestrate:  {config['orchestrate']}")
        print()


def analyze_task_performance(experiment_id: str) -> None:
    """Analyze per-task performance for an experiment."""
    result = load_result(experiment_id)
    if not result:
        print(f"Could not load result for {experiment_id}")
        return

    print("\n" + "=" * 80)
    print(f"Task Performance Analysis: {experiment_id}")
    print("=" * 80 + "\n")

    tasks = result.get("tasks", [])
    for task in tasks:
        print(f"{task['label']}")
        print(f"  Tier 1 Score:         {task['tier1_score']:.2f}")
        print(f"  Resolution:           {task['resolution']:.2f}")
        print(f"  Efficiency Score:     {task['efficiency_score']:.2f}")
        print(f"  Robustness Score:     {task['robustness_score']:.2f}")
        print(f"  Latency (P95):        {task['latency_p95_ms']:.1f} ms")
        print(f"  Items Scored:         {task['items_scored']}")
        print(f"  Items Errored:        {task['items_errored']}")
        print(f"  Model Used:           {task['primary_model']}")

        # Show dimension scores
        if task.get("dimension_scores"):
            print("  Dimension Scores:")
            for dim, score in task["dimension_scores"].items():
                weight = task.get("dimension_weights", {}).get(dim, 0)
                print(f"    {dim:<25} {score:.4f} (weight: {weight:.0%})")

        print()


if __name__ == "__main__":
    # Example 1: Run a custom experiment
    print("Example 1: Running a custom experiment...")
    print("=" * 80)
    # Uncomment to run:
    # success = run_single_experiment(
    #     experiment_id="custom-001",
    #     triage_model="gpt-5-4-nano",
    #     extract_model="gpt-5-4-mini",
    #     orchestrate_model="gpt-5-4",
    # )
    # print(f"Experiment completed: {success}")

    # Example 2: Load and inspect a result
    print("Example 2: Loading results...")
    print("=" * 80)
    result = load_result("E3-base-all")
    if result:
        print(f"Experiment ID: {result['experiment_id']}")
        print(f"FDEBench Score: {result['fdebench_composite']:.2f}")
        print(f"Timestamp: {result['timestamp']}")
    else:
        print("E3-base-all result not found (run the experiment first)")

    # Example 3: Compare experiments
    print("\nExample 3: Comparing experiments...")
    print("=" * 80)
    # compare_experiments(["E1-nano-all", "E3-base-all", "E4-mixed-nano-base"])

    # Example 4: Analyze task performance
    print("Example 4: Analyzing task performance...")
    print("=" * 80)
    # analyze_task_performance("E3-base-all")

    print("\nFor full usage, see README.md in the experiments directory")
