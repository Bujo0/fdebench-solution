# Eval Harness

This is the same scoring logic the platform uses. Run it locally, see exactly how you'll be scored. No surprises on submission day.

> **What this scores:** The 5 classification dimensions (up to 85 pts).
> **What it doesn't score:** Efficiency (latency + cost) and engineering quality — those happen after you submit.

## Quick Start

```bash
cd docs/eval

# Score against the 25 sample tickets (with gold answers)
uv run python run_eval.py \
  --endpoint http://localhost:8000 \
  --dataset ../data/tickets/sample.json \
  --gold ../data/tickets/sample_gold.json
```

## How Scoring Works

Full details in the [challenge README](../challenge/README.md#how-we-score-you). Here's the short version.

### Your functional score (0–100)

```
functional = classification (0–85) + efficiency (0–15)
```

The local eval harness computes the **classification** portion. The platform adds efficiency after calling your live endpoint.

### Classification dimensions (what this harness scores)

| Dimension | Weight | Metric | Scoring logic |
|---|---|---|---|
| `category` | 20% | **Macro F1** | Per-class F1, averaged across 8 categories |
| `priority` | 20% | **Mean partial credit** | Exact = 1.0, off-by-one = 0.67, off-by-two+ = 0.0 |
| `routing` | 20% | **Macro F1** | Per-class F1, averaged across 7 teams |
| `missing_info` | 15% | **Mean set F1** | Per-ticket F1 on constrained vocabulary, then averaged |
| `escalation` | 10% | **Binary F1** | F1 for the positive class across all tickets |

The classification score is:

```
weighted = 0.20×category + 0.20×priority + 0.20×routing + 0.15×missing_info + 0.10×escalation
classification_pts = (weighted / 0.85) × 85  →  range [0, 85]
```

### Efficiency dimensions (scored by the platform, not this harness)

| Dimension | Weight | Best (1.0) | Worst (0.0) |
|---|---|---|---|
| Latency | 10% | p50 ≤ 200ms | p50 ≥ 2000ms |
| Cost | 5% | ≤ $0.001/ticket | ≥ $0.05/ticket |

The harness shows latency stats so you can keep an eye on it, but doesn't fold them into the score.

### Priority partial credit

You get credit for being close, but only one level off. Two or more? Zero.

| Pred \ Gold | P1 | P2 | P3 | P4 |
|---|---|---|---|---|
| **P1** | 1.00 | 0.67 | 0.00 | 0.00 |
| **P2** | 0.67 | 1.00 | 0.67 | 0.00 |
| **P3** | 0.00 | 0.67 | 1.00 | 0.67 |
| **P4** | 0.00 | 0.00 | 0.67 | 1.00 |

### Missing info set F1

Exact string match on the 16-value vocabulary from the [output schema](../data/schemas/output.json). No fuzzy matching, no synonyms. If you return `"error_msg"` instead of `"error_message"`, that's a miss.

```
precision = |pred ∩ gold| / |pred|
recall    = |pred ∩ gold| / |gold|
F1        = 2 × precision × recall / (precision + recall)

Both empty → 1.0 (correctly identified nothing is missing)
One empty  → 0.0 (either all false positives or all false negatives)
```

### Boolean coercion

People return weird stuff from APIs. The harness handles the common ones so you don't get penalized for returning `"true"` instead of `true`:
- String `"true"` / `"false"` → boolean (Python's `bool("false")` is `True`, so explicit handling is needed)
- String `"1"` / `"0"` → boolean
- Integer `1` / `0` → boolean
- `None` → `False`

### What about remediation?

`next_best_action` and `remediation_steps` must be in your response (the schema requires them), but the harness doesn't score them. We look at those when we review your repo.

## Usage

### 25 sample tickets (with gold answers)

This is your main dev loop. Run it early, run it often.

```bash
cd docs/eval
uv run python run_eval.py \
  --endpoint http://localhost:8000 \
  --dataset ../data/tickets/sample.json \
  --gold ../data/tickets/sample_gold.json
```

### 50 public eval tickets (no gold answers)

Run this before you submit. There's no gold file so you won't get a score, but it'll catch crashes, timeouts, and schema issues on tickets you haven't seen.

```bash
cd docs/eval
uv run python run_eval.py \
  --endpoint http://localhost:8000 \
  --dataset ../data/tickets/public_eval.json
```

### Custom gold file

```bash
uv run python run_eval.py \
  --endpoint http://localhost:8000 \
  --dataset path/to/tickets.json \
  --gold path/to/gold.json
```

## Sample Output

Each ticket shows its per-ticket classification score (max 85 pts):

```
Loaded 25 tickets, 25 gold answers
Endpoint: http://localhost:8000

Health check: ✓ OK

  INC-0001  [ 85.0]  cat=✓ pri=✓ route=✓ esc=✓ miss=✓(1.00)  142ms
  INC-0002  [ 60.1]  cat=✓ pri=✓ route=✗ esc=✓ miss=~(0.67)  198ms
  INC-0003  [ 51.7]  cat=✓ pri=~ route=✓ esc=✗ miss=✗(0.00)  156ms
  ...

  ════════════════════════════════════════════════════════════
    FUNCTIONAL SCORE (Part 1 of final leaderboard)
  ════════════════════════════════════════════════════════════

    Classification dimensions (max 85 pts):

      category          0.8200 (macro F1)   × 20% weight  = 16.40 pts
      priority          0.9100 (mean)        × 20% weight  = 18.20 pts
      routing           0.7500 (macro F1)   × 20% weight  = 15.00 pts
      missing_info      0.6800 (mean)        × 15% weight  = 10.20 pts
      escalation        0.9000 (binary F1)  × 10% weight  =  9.00 pts
      ────────────────────────────────────────────────────────
      CLASSIFICATION     72.5 / 85

    Efficiency dimensions (max 15 pts, scored by platform):

      latency           p50=320ms  p95=890ms  (10% weight)
      cost              from response headers  (5% weight)

    ┌─────────────────────────────────────────────────────────┐
    │  Classification score: up to 85 pts from 5 dimensions  │
    │  Efficiency score: up to 15 pts (latency + cost)       │
    │  Total functional score: 0–100 (50% of leaderboard)    │
    │  Engineering quality: 50% of leaderboard               │
    └─────────────────────────────────────────────────────────┘

  Results saved to eval_results.json
```

The `eval_results.json` file contains full per-ticket breakdowns for error analysis.

## Running the Tests

The scoring functions have their own test suite — 84 tests covering every edge case. Run them if you want to understand exactly how scoring works (or if you've been poking at the harness code):

```bash
cd docs/eval
python test_scoring.py
```

All 84 should pass. If they don't, something's wrong with your environment, not the tests.
