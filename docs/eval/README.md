# Eval Harness

🛰️ **CDSS SCORING COMPUTER — SELF-SERVICE TERMINAL** 🛰️

This is the same scoring logic the platform uses. Run it locally, see exactly how you'll be scored. No surprises on launch day.

> **What this scores:** The 5 classification dimensions (up to 85 pts).
> **What it doesn't score:** Efficiency (latency + cost) and the separate engineering review. Those happen after you submit. The scoring computer is cold, unforgiving math — like the vacuum outside the viewport.

## Quick Start

```bash
cd docs/eval

# Score against the 25 sample signals (with gold answers)
uv run python run_eval.py \
  --endpoint http://localhost:8000 \
  --dataset ../data/tickets/sample.json \
  --gold ../data/tickets/sample_gold.json
```

## How Scoring Works

Full details in the [challenge README](../challenge/README.md#how-we-score-you). Here's the mission briefing version.

### Your functional score (0–100)

```
functional = classification (0–85) + efficiency (0–15)
```

The local eval harness computes the **classification** portion. The platform adds efficiency after calling your live endpoint — because we time your triage decisions with the same ruthlessness as a countdown clock.

### Classification dimensions (what this harness scores)

| Dimension | Weight | Metric | Scoring logic |
|---|---|---|---|
| `category` | 20% | **Macro F1** | Per-class F1, averaged across 8 anomaly categories. Ignore rare categories and the void will teach you why they matter. |
| `priority` | 20% | **Mean partial credit** | Exact = 1.0, off-by-one = 0.67, off-by-two+ = 0.0. Call a hull breach "routine" and that's a zero — and a new window in Deck 7. |
| `routing` | 20% | **Macro F1** | Per-class F1, averaged across 7 response divisions. Send the wrong team and the clock ticks. |
| `missing_info` | 15% | **Mean set F1** | Per-signal F1 on constrained vocabulary, then averaged. Don't waste the crew's time asking for data they already gave you. |
| `escalation` | 10% | **Binary F1** | F1 for the positive class across all signals. Miss an escalation and the Admiral finds out the hard way. |

The classification score is:

```
weighted = 0.20×category + 0.20×priority + 0.20×routing + 0.15×missing_info + 0.10×escalation
classification_pts = (weighted / 0.85) × 85  →  range [0, 85]
```

### Efficiency dimensions (scored by the platform, not this harness)

| Dimension | Weight | Best (1.0) | Worst (0.0) |
|---|---|---|---|
| Latency | 10% | p50 ≤ 200ms | p50 ≥ 2000ms |
| Cost | 5% | ≤ $0.001/signal | ≥ $0.05/signal |

The harness shows latency stats so you can keep an eye on your fuel consumption, but doesn't fold them into the score.

### Priority partial credit

You get credit for being close, but only one level off. Two or more? Zero. Space doesn't grade on a curve.

| Pred \ Gold | P1 | P2 | P3 | P4 |
|---|---|---|---|---|
| **P1** | 1.00 | 0.67 | 0.00 | 0.00 |
| **P2** | 0.67 | 1.00 | 0.67 | 0.00 |
| **P3** | 0.00 | 0.67 | 1.00 | 0.67 |
| **P4** | 0.00 | 0.00 | 0.67 | 1.00 |

### Missing info set F1

Exact string match on the 16-value vocabulary from the [output schema](../data/schemas/output.json). No fuzzy matching, no synonyms, no "I meant the other kind of anomaly readout." If you return `"anomaly_msg"` instead of `"anomaly_readout"`, that's a miss. The scoring computer doesn't interpret intent — it matches strings with the empathy of a docking clamp.

```
precision = |pred ∩ gold| / |pred|
recall    = |pred ∩ gold| / |gold|
F1        = 2 × precision × recall / (precision + recall)

Both empty → 1.0 (correctly identified nothing is missing — well done, operator)
One empty  → 0.0 (either all false positives or all false negatives)
```

### Boolean coercion

Crew members return weird stuff from APIs. The scoring computer has seen things. `"true"` as a string. `1` as an integer. `"yes"` as if it's having a conversation. The harness handles the common ones so you don't get penalized for returning `"true"` instead of `true`:
- String `"true"` / `"false"` → boolean (Python's `bool("false")` is `True` — a cosmic trap that has claimed more victims than the airlock on Deck 3)
- String `"1"` / `"0"` → boolean
- String `"yes"` / `"no"` → boolean (the scoring computer respects the classics)
- Integer `1` / `0` → boolean
- `None` → `False`
- Literally anything else → `False` (the scoring computer doesn't negotiate)

### What about remediation?

`next_best_action` and `remediation_steps` must be in your response (the schema requires them), but the harness doesn't score them. We look at those when we review your repo. A system that says "investigate the anomaly" for every signal is telling us you phoned it in from a comfortable 1 AU away. Write remediation steps a Tier 1 controller could actually follow while alarm klaxons are blaring and the Admiral is making pointed remarks about "that AI system I was told would fix everything."

## Usage

### 25 sample signals (with gold answers)

This is your main dev loop. Run it early, run it often. The scoring computer never sleeps.

```bash
cd docs/eval
uv run python run_eval.py \
  --endpoint http://localhost:8000 \
  --dataset ../data/tickets/sample.json \
  --gold ../data/tickets/sample_gold.json
```

### 100 public eval signals (no gold answers)

Run this before you submit. There's no gold file so you won't get a score, but it'll catch crashes, timeouts, and schema issues on signals you haven't seen. Consider it your pre-launch checklist.

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
  --dataset path/to/signals.json \
  --gold path/to/gold.json
```

## Sample Output

Each signal shows its per-signal classification score (max 85 pts):

```
Loaded 25 signals, 25 gold answers
Endpoint: http://localhost:8000

Health check: ✓ OK

  SIG-0001  [ 85.0]  cat=✓ pri=✓ route=✓ esc=✓ miss=✓(1.00)  142ms
  SIG-0002  [ 60.1]  cat=✓ pri=✓ route=✗ esc=✓ miss=~(0.67)  198ms
  SIG-0003  [ 51.7]  cat=✓ pri=~ route=✓ esc=✗ miss=✗(0.00)  156ms
  ...

  🛰️ ════════════════════════════════════════════════════════════
    MISSION CONTROL SCORING COMPUTER — FINAL VERDICT
  🛰️ ════════════════════════════════════════════════════════════

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

    ┌─────────────────────────────────────────────────────────────┐
    │  Classification: up to 85 pts from 5 dimensions            │
    │  Efficiency: up to 15 pts (latency + cost)                 │
    │  Total functional score: 0–100 (50% of leaderboard)        │
    │  Engineering quality: 50% of leaderboard                   │
    │                                                             │
    │  The scoring computer has rendered its verdict.             │
    │  Space doesn't grade on a curve. Neither do we. 🫡         │
    └─────────────────────────────────────────────────────────────┘

  Results saved to eval_results.json
```

The `eval_results.json` file contains full per-signal breakdowns for your post-mission debrief.

## Running the Tests

The scoring functions have their own test suite (84 tests covering every edge case the void could conceivably throw at a triage system — the scoring computer's self-diagnostics, if you will). Run them if you want to understand exactly how scoring works, or if you've been poking at the harness code, or if you just enjoy watching 84 green checkmarks cascade down your terminal like stars outside the viewport:

```bash
cd docs/eval
python test_scoring.py
```

All 84 should pass. If they don't, something's wrong with your environment, not the tests. The scoring computer has been tested more thoroughly than your station's life support. Probably. (Lt. Mehta would like the record to reflect that he has *also* tested life support. Recently. After an incident.)
