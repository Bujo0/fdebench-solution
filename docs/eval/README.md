# Evaluation Harness

Test your solution locally before submitting. This harness scores **Part 1 only** (functional accuracy). Part 2 (engineering quality) is evaluated after submission.

## Final Leaderboard Score

Your leaderboard score is **0–100**:

| Part | Weight | Source |
|---|---|---|
| **Functional accuracy** | 50% | Deterministic scoring on ~100 hidden tickets |
| **Engineering quality** | 50% | Repo evaluation: design, code, docs, evals, infra |

## Scoring Math

### Per-ticket score

Each ticket response is scored on 6 dimensions. Each dimension produces a value in **[0.0, 1.0]**. The per-ticket score is their weighted sum:

```
ticket_score = 0.15 × category
             + 0.15 × priority
             + 0.20 × routing
             + 0.20 × missing_info
             + 0.10 × escalation
             + 0.20 × remediation
```

| Dimension | Weight | Scoring function |
|---|---|---|
| `category` | 15% | 1.0 if exact match (case-insensitive), else 0.0 |
| `priority` | 15% | 1.0 if exact match. Off by 1 level = 0.67. Off by 2 = 0.33. Off by 3 = 0.0 |
| `routing` | 20% | 1.0 if exact match (case-insensitive), else 0.0 |
| `missing_info` | 20% | Set F1 = 2×P×R/(P+R). Both empty = 1.0. One empty = 0.0 |
| `escalation` | 10% | 1.0 if boolean match, else 0.0 |
| `remediation` | 20% | Simplified locally (see below). Full LLM judge on hidden set |

### Functional score (0–100)

```
functional_score = mean(ticket_score for all N tickets) × 100
```

### Priority distance table

| Pred \ Gold | P1 | P2 | P3 | P4 |
|---|---|---|---|---|
| **P1** | 1.00 | 0.67 | 0.33 | 0.00 |
| **P2** | 0.67 | 1.00 | 0.67 | 0.33 |
| **P3** | 0.33 | 0.67 | 1.00 | 0.67 |
| **P4** | 0.00 | 0.33 | 0.67 | 1.00 |

### Missing info F1

Uses exact string match on the constrained vocabulary (16 valid values defined in the output schema).

```
precision = |pred ∩ gold| / |pred|
recall    = |pred ∩ gold| / |gold|
F1        = 2 × precision × recall / (precision + recall)

Both empty → 1.0
One empty  → 0.0
```

### Remediation (local vs hidden)

**Locally:** The eval harness uses a simplified proxy (presence + step count). This lets you iterate without needing an LLM.

**On the hidden set:** Remediation is scored by an LLM judge on completeness, specificity, and ordering against the gold answer. Build for quality — the local proxy is not the final score.

## Usage

### 25 sample tickets (with gold answers)

Use for local development. Compare your output to the gold answers to understand every scoring dimension.

```bash
cd docs/eval
uv run python run_eval.py \
  --endpoint http://localhost:8000 \
  --dataset ../data/tickets/sample.json \
  --gold ../data/tickets/sample_gold.json
```

### 50 public eval tickets (no gold answers)

Use to test at scale before submitting. No gold file = no scoring, but the harness still validates schema compliance and measures latency.

```bash
cd docs/eval
uv run python run_eval.py \
  --endpoint http://localhost:8000 \
  --dataset ../data/tickets/public_eval.json
```

> **Note:** The public eval set has no gold file in this repo. You cannot score against it locally. Use it to verify your endpoint handles 50 tickets without errors or timeouts.

## Output

```
  INC-0001  [ 85.0]  cat=✓ pri=✓ route=✓ esc=✓ miss=✓(1.00) rem=0.67  142ms
  INC-0002  [ 62.3]  cat=✓ pri=✓ route=✗ esc=✓ miss=~(0.67) rem=0.67  198ms
  ...
  ════════════════════════════════════════════════════════════
    FUNCTIONAL SCORE (Part 1 of final leaderboard)
  ════════════════════════════════════════════════════════════

    category          80.0% accuracy  × 15% weight  =  12.00 pts
    priority          92.0% accuracy  × 15% weight  =  13.80 pts
    routing           72.0% accuracy  × 20% weight  =  14.40 pts
    missing_info      65.0% accuracy  × 20% weight  =  13.00 pts
    escalation        88.0% accuracy  × 10% weight  =   8.80 pts
    remediation       70.0% accuracy  × 20% weight  =  14.00 pts
    ──────────────────────────────────────────────────────────
    FUNCTIONAL         76.0 / 100

    ┌─────────────────────────────────────────────────┐
    │  This score counts as 50% of your final score.  │
    │  Engineering quality (50%) is evaluated after    │
    │  submission on your repo and documentation.      │
    └─────────────────────────────────────────────────┘
```

Results are also saved to `eval_results.json` with per-ticket breakdowns.

## What This Harness Does NOT Test

- Engineering quality (Part 2) — evaluated after submission
- LLM-as-judge remediation scoring — uses simplified proxy locally
- The hidden 100-ticket dataset — you only see the 25 sample + 50 public
