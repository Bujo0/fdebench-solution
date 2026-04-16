# FDEBench Experiment Runner

A complete automation system for running FDEBench evaluations with different model configurations and tracking results.

## Overview

This system provides two main tools:

1. **`run_experiment.py`** — Run a single experiment with specified model configuration
2. **`sweep.py`** — Run multiple predefined experiments in sequence and compare results

## Quick Start

### Single Experiment

```bash
cd apps/sample

# Run with specific models
python experiments/run_experiment.py \
    --experiment-id exp-001 \
    --triage-model gpt-5-4-nano \
    --extract-model gpt-5-4 \
    --orchestrate-model gpt-5-4 \
    --endpoint http://localhost:8000
```

Results are saved to `experiments/results/exp-001.json`

### Experiment Sweep

```bash
cd apps/sample

# Run all default experiments and compare
python experiments/sweep.py --endpoint http://localhost:8000

# Run specific experiments
python experiments/sweep.py \
    --endpoint http://localhost:8000 \
    --experiments E1-nano-all E3-base-all
```

## Default Experiments

The sweep script includes 5 predefined experiments for hill-climbing:

| ID | Name | Configuration |
|---|---|---|
| **E1** | `E1-nano-all` | gpt-5-4-nano for all tasks |
| **E2** | `E2-mini-all` | gpt-5-4-mini for all tasks |
| **E3** | `E3-base-all` | gpt-5-4 for all tasks |
| **E4** | `E4-mixed-nano-base` | nano (T1), base (T2/T3) |
| **E5** | `E5-mixed-nano-mini` | nano (T1), base (T2), o4-mini (T3) |

## Command-Line Options

### `run_experiment.py`

```
--experiment-id ID              Experiment identifier (required)
--triage-model MODEL            Model for Task 1 (default: gpt-5-4-nano)
--extract-model MODEL           Model for Task 2 (default: gpt-5-4)
--orchestrate-model MODEL       Model for Task 3 (default: gpt-5-4)
--endpoint URL                  Service URL (required)
--concurrency N                 Max concurrent requests (default: 5)
--timeout SEC                   Per-request timeout (default: 30)
```

### `sweep.py`

```
--endpoint URL                  Service URL (required)
--experiments ID [ID ...]       Run specific experiments (default: all)
--concurrency N                 Max concurrent requests (default: 5)
--timeout SEC                   Per-request timeout (default: 30)
```

## Output Format

### Results File: `results/{experiment_id}.json`

Each experiment produces a JSON file with:

```json
{
  "experiment_id": "exp-001",
  "timestamp": "2024-04-16T23:15:00.123456",
  "model_config": {
    "triage": "gpt-5-4-nano",
    "extract": "gpt-5-4",
    "orchestrate": "gpt-5-4"
  },
  "endpoint": "http://localhost:8000",
  "fdebench_composite": 72.45,
  "resolution_avg": 75.20,
  "efficiency_avg": 68.10,
  "robustness_avg": 73.80,
  "tasks": [
    {
      "name": "ticket_triage",
      "label": "Task 1: Ticket Triage",
      "tier1_score": 74.32,
      "resolution": 76.50,
      "efficiency_score": 69.20,
      "robustness_score": 74.10,
      "latency_p95_ms": 850.5,
      "latency_score": 0.8234,
      "cost_score": 0.9123,
      "adversarial_accuracy": 72.50,
      "api_resilience": 75.30,
      "items_scored": 50,
      "items_errored": 0,
      "primary_model": "gpt-5-4-nano",
      "dimension_scores": {
        "accuracy": 0.7650,
        "relevance": 0.7450
      },
      "dimension_weights": {
        "accuracy": 0.6,
        "relevance": 0.4
      },
      "probe_results": {
        "basic_triage": true,
        "edge_cases": false
      }
    },
    ...
  ],
  "errors": []
}
```

### Console Output

Each experiment prints a summary table:

```
======================================================================
  Experiment: exp-001
======================================================================

  FDEBench Composite:        72.45 / 100
  Resolution (avg):          75.20 / 100
  Efficiency (avg):          68.10 / 100
  Robustness (avg):          73.80 / 100

----------------------------------------------------------------------
  Model Configuration
----------------------------------------------------------------------
    extract         gpt-5-4
    orchestrate     gpt-5-4
    triage          gpt-5-4-nano

----------------------------------------------------------------------
  Per-Task Scores
----------------------------------------------------------------------
  Task 1: Ticket Triage              74.32  (R:76.5  E:69.2  Ro:74.1)
  Task 2: Document Extraction        70.18  (R:74.1  E:67.5  Ro:71.2)
  Task 3: Workflow Orchestration     72.80  (R:75.8  E:68.5  Ro:72.5)

======================================================================
```

The sweep script prints a comparison table after all experiments:

```
========================================================================================================================
  FDEBench Sweep Results — Sorted by Composite Score
========================================================================================================================

Rank  Experiment           FDEBench     Resolution   Efficiency   Robustness   Timestamp
-----  ----                 -----        -----        -----        -----        -----
1     E3-base-all              72.45       75.20        68.10        73.80       23:15:45
2     E4-mixed-nano-base       71.32       74.10        67.50        72.40       23:20:12
3     E1-nano-all              68.90       71.50        65.20        69.80       23:25:33
...
```

## Makefile Targets

Add these targets to your Makefile:

```makefile
experiment: ## Run a single experiment
	cd apps/sample && python experiments/run_experiment.py \
		--experiment-id $(EXP_ID) \
		--triage-model $(TRIAGE_MODEL) \
		--extract-model $(EXTRACT_MODEL) \
		--orchestrate-model $(ORCHESTRATE_MODEL) \
		--endpoint http://localhost:8000

sweep: ## Run all experiment configs
	cd apps/sample && python experiments/sweep.py --endpoint http://localhost:8000

sweep-partial: ## Run specific experiments
	cd apps/sample && python experiments/sweep.py \
		--endpoint http://localhost:8000 \
		--experiments $(EXPERIMENTS)
```

Usage:

```bash
# Run a single experiment
make experiment EXP_ID=my-exp-001 TRIAGE_MODEL=gpt-5-4-nano EXTRACT_MODEL=gpt-5-4 ORCHESTRATE_MODEL=gpt-5-4

# Run all default experiments
make sweep

# Run specific experiments
make sweep-partial EXPERIMENTS="E1-nano-all E3-base-all"
```

## Hill-Climbing Workflow

The system is designed for iterative optimization:

1. **Establish baseline**: Run E3 (base model across all tasks)
   ```bash
   python experiments/sweep.py --endpoint http://localhost:8000 --experiments E3-base-all
   ```

2. **Test cost-reduction**: Run E1, E2 (smaller models)
   ```bash
   python experiments/sweep.py --endpoint http://localhost:8000 --experiments E1-nano-all E2-mini-all
   ```

3. **Test mixed configurations**: Run E4, E5 (task-specific optimization)
   ```bash
   python experiments/sweep.py --endpoint http://localhost:8000 --experiments E4-mixed-nano-base E5-mixed-nano-mini
   ```

4. **Add custom experiments**: Create new configurations in `sweep.py`
   ```python
   {
       "id": "E6-custom",
       "name": "E6: Custom configuration",
       "triage_model": "gpt-5-4-nano",
       "extract_model": "o4-mini",
       "orchestrate_model": "gpt-5-4",
   }
   ```

5. **Compare results**: Review `experiments/results/` directory
   ```bash
   ls -lh experiments/results/
   cat experiments/results/E3-base-all.json | jq '.fdebench_composite'
   ```

## Result Analysis

### Compare two experiments:

```bash
# Compare using jq
jq '.fdebench_composite' experiments/results/E1-nano-all.json experiments/results/E3-base-all.json

# Get per-task scores
jq '.tasks[] | {name: .label, tier1_score}' experiments/results/E3-base-all.json
```

### Find best experiment:

```bash
for f in experiments/results/*.json; do
  echo "$(basename $f): $(jq '.fdebench_composite' $f)"
done | sort -t: -k2 -rn
```

## Files and Structure

```
apps/sample/experiments/
├── __init__.py                  # Package marker
├── run_experiment.py            # Single experiment runner (executable)
├── sweep.py                     # Multi-experiment sweep (executable)
├── results/                     # Results directory
│   ├── .gitkeep
│   ├── E1-nano-all.json
│   ├── E2-mini-all.json
│   └── ...
└── README.md                    # This file
```

## Environment Variables

The experiment runner sets these environment variables during execution:

- `TRIAGE_MODEL` — Model for Task 1
- `EXTRACT_MODEL` — Model for Task 2
- `ORCHESTRATE_MODEL` — Model for Task 3

Your application should read these from `config.py` using Pydantic settings.

## Performance Notes

- **Concurrency**: Default is 5 concurrent requests. Increase for faster runs (up to 10-20 depending on system).
- **Timeout**: Default is 30 seconds per request. Larger models may need longer.
- **Mock Service**: Task 3 requires the mock tool service (started automatically).
- **Sequential Runs**: Sweep runs experiments sequentially; runs take ~2-3 min each.

## Troubleshooting

### "Preflight validation failed"

The endpoint isn't running or isn't responsive. Check:
```bash
curl http://localhost:8000/health
```

### "Dataset not found"

Data files are missing. Verify:
```bash
ls data/task{1,2,3}/
```

### "Mock tool service did not start"

Port 9090 may be in use:
```bash
lsof -i :9090
```

### Results show all zeros

Models may not be set correctly. Check environment:
```bash
python -c "import os; print(os.environ.get('TRIAGE_MODEL', 'NOT SET'))"
```

## Next Steps

- Add custom experiment configurations to `sweep.py`
- Integrate with CI/CD pipeline
- Automate result aggregation and reporting
- Set up alerts for performance regressions
