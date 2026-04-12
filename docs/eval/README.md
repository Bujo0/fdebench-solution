# 🛰️ Eval Harness — The Scoring Computer

> *"The scoring computer doesn't negotiate. It doesn't accept bribes. It doesn't care that your LLM was 'pretty close' or that you 'meant' P1 when you returned P3. It has the emotional range of a neutron star and the forgiveness of hard vacuum."* — Admiral Chen, CDSS

This is the same scoring logic Mission Control uses. Run it locally, see exactly how you'll be scored. No surprises on launch day. The scoring computer is deterministic, auditable, and completely indifferent to your feelings.

> **What this scores:** The 5 classification dimensions (up to 85 pts).
> **What it doesn't score:** Efficiency (latency + cost) and the separate engineering review. Those happen after you submit — like the post-mission debrief, except the debrief doesn't affect your leaderboard position and this does.

## Quick Start

```bash
cd docs/eval

# Score against the 25 sample signals (with gold answers)
uv run python run_eval.py \
  --endpoint http://localhost:8000 \
  --dataset ../data/signals/sample.json \
  --gold ../data/signals/sample_gold.json
```

## How Scoring Works

Full details in the [challenge README](../challenge/README.md#how-we-score-you). Here's the short version — the executive summary for those who want to know what the scoring computer is doing to their score and why.

### Your functional score (0–100)

```
functional = classification (0–85) + efficiency (0–15)
```

The local eval harness computes the **classification** portion. The platform adds efficiency after calling your live endpoint. Think of it as two separate verdicts: "did you get the right answer?" and "did you get it without burning through half the station's compute budget?"

### Classification dimensions (what this harness scores)

Five dimensions. Five ways to succeed. Five ways to fail. The scoring computer evaluates each with surgical precision and the compassion of an asteroid:

| Dimension | Weight | Metric | Scoring logic |
|---|---|---|---|
| `category` | 20% | **Macro F1** | Per-class F1, averaged across 8 categories. Systems that ignore rare classes are penalized — like ignoring the quiet oxygen alarm because the loud fabricator jam is more dramatic. |
| `priority` | 20% | **Mean partial credit** | Exact = 1.0, off-by-one = 0.67, off-by-two+ = 0.0. Close only counts in asteroid dodging. |
| `routing` | 20% | **Macro F1** | Per-class F1, averaged across 7 teams. Send a hull breach to Deep Space Comms and they'll stare at it like a cat staring at a starfield — interested, but unhelpful. |
| `missing_info` | 15% | **Mean set F1** | Per-signal F1 on constrained vocabulary, then averaged. Ask for the right intel. Don't ask for intel the signal already provided — the crew is 0.3 AU from patience. |
| `escalation` | 10% | **Binary F1** | F1 for the positive class across all signals. Miss an escalation and someone important finds out the hard way. Important people finding out the hard way is how disciplinary hearings start. |

The classification score is:

```
weighted = 0.20×category + 0.20×priority + 0.20×routing + 0.15×missing_info + 0.10×escalation
classification_pts = (weighted / 0.85) × 85  →  range [0, 85]
```

### Efficiency dimensions (scored by the platform, not this harness)

Two dimensions measuring whether you built a lean, fast triage system or a lumbering behemoth that processes signals with the urgency of a glacier:

| Dimension | Weight | Best (1.0) | Worst (0.0) |
|---|---|---|---|
| Latency | 10% | p50 ≤ 200ms | p50 ≥ 2000ms |
| Cost | 5% | ≤ $0.001/signal | ≥ $0.05/signal |

The harness shows latency stats so you can keep an eye on it, but doesn't fold them into the score. Consider it a preview of what the platform will do — like seeing the asteroid before it hits, except you can actually do something about it.

### Priority partial credit

You get credit for being close, but only one level off. Two or more? Zero. Like docking procedure — close enough to the airlock is still not docked, and off by two decks is a collision.

| Pred \ Gold | P1 | P2 | P3 | P4 |
|---|---|---|---|---|
| **P1** | 1.00 | 0.67 | 0.00 | 0.00 |
| **P2** | 0.67 | 1.00 | 0.67 | 0.00 |
| **P3** | 0.00 | 0.67 | 1.00 | 0.67 |
| **P4** | 0.00 | 0.00 | 0.67 | 1.00 |

Calling a P1 hull breach "P4 Routine" scores 0.0 and also describes a catastrophe that would make Titan Outpost look well-managed.

### Missing info set F1

Exact string match on the 16-value vocabulary from the [output schema](../data/schemas/output.json). No fuzzy matching, no synonyms, no creative paraphrasing. If you return `"anomaly_read"` instead of `"anomaly_readout"`, that's a miss. The scoring computer doesn't squint. It doesn't infer. It matches strings with the cold precision of a targeting computer and the sympathy of deep space.

```
precision = |pred ∩ gold| / |pred|
recall    = |pred ∩ gold| / |gold|
F1        = 2 × precision × recall / (precision + recall)

Both empty → 1.0 (correctly identified nothing is missing)
One empty  → 0.0 (either all false positives or all false negatives)
```

### Boolean coercion

Operators transmit weird stuff from APIs. Humans are inconsistent across 0.3 AU. The harness handles the common representations so you don't get penalized for returning `"true"` instead of `true` — because debugging boolean serialization while a hull breach goes unrouted is not how we want operators spending their time:
- String `"true"` / `"false"` → boolean (Python's `bool("false")` is `True`, which is the kind of gotcha that keeps ops officers up at night — which in space is indistinguishable from the day)
- String `"1"` / `"0"` → boolean
- Integer `1` / `0` → boolean
- `None` → `False` (the absence of an answer is not an escalation)

### What about remediation?

`next_best_action` and `remediation_steps` must be in your response (the schema requires them), but the harness doesn't score them deterministically. We look at those when we review your repo. A system that says "investigate the anomaly" for every signal is telling us you phoned it in from a safe distance — and at 0.3 AU, there is no safe distance, just varying degrees of delayed consequence.

## Usage

### 25 sample signals (with gold answers)

This is your main dev loop. Run it early, run it often. Run it like your score depends on it — because it does.

```bash
cd docs/eval
uv run python run_eval.py \
  --endpoint http://localhost:8000 \
  --dataset ../data/signals/sample.json \
  --gold ../data/signals/sample_gold.json
```

### 100 public eval signals (no gold answers)

Run this before you submit. There's no gold file so you won't get a score, but it'll catch crashes, timeouts, and schema violations on signals you haven't seen. Think of it as a dress rehearsal — except the audience is 1,000+ hidden signals waiting to judge you for real.

```bash
cd docs/eval
uv run python run_eval.py \
  --endpoint http://localhost:8000 \
  --dataset ../data/signals/public_eval.json
```

If your system crashes on signal 37 of 100, imagine what the hidden set will do. The hidden set has signals you haven't even imagined yet. It's like space — there's always something worse out there.

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
  🛰️  CONTOSO DEEP SPACE STATION — SCORING COMPUTER  🛰️
  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

  Incoming signals:  25
  Gold answers:      25
  Target endpoint:   http://localhost:8000

  Health check: ✓ LIFE SIGNS DETECTED — the station breathes

  Transmitting signals to triage endpoint... stand by for contact.

  SIG-0001  [ 85.0]  cat=✓ pri=✓ route=✓ esc=✓ miss=✓(1.00)  142ms
  SIG-0002  [ 60.1]  cat=✓ pri=✓ route=✗ esc=✓ miss=~(0.67)  198ms
  SIG-0003  [ 51.7]  cat=✓ pri=~ route=✓ esc=✗ miss=✗(0.00)  156ms
  ...

  ╔═══════════════════════════════════════════════════════════╗
  ║  🛰️  MISSION SCORING REPORT — CLASSIFICATION RESULTS    ║
  ╚═══════════════════════════════════════════════════════════╝

  Classification dimensions (max 85 pts):

    category          ████████████████░░░░  0.8200 (macro F1)   × 20%  = 16.40 pts
    priority          ██████████████████░░  0.9100 (mean)        × 20%  = 18.20 pts
    routing           ███████████████░░░░░  0.7500 (macro F1)   × 20%  = 15.00 pts
    missing_info      █████████████░░░░░░░  0.6800 (mean)        × 15%  = 10.20 pts
    escalation        ██████████████████░░  0.9000 (binary F1)  × 10%  =  9.00 pts
    ──────────────────────────────────────────────────────────────
    CLASSIFICATION                          72.5 / 85

  Efficiency dimensions (max 15 pts, scored by platform):

    latency           p50=320ms  p95=890ms  (10% weight)
    cost              from response headers  (5% weight)

  Signals processed: 25/25

  ┌─────────────────────────────────────────────────────────────┐
  │  Classification:  up to 85 pts from 5 scoring dimensions   │
  │  Efficiency:      up to 15 pts (latency + cost)            │
  │  Total functional score: 0–100                             │
  │  Engineering review: evaluated separately from your repo   │
  │                                                            │
  │  Status: 🟡 Moderate — some signals lost in static.       │
  │  The crew survives, but Mehta is writing margin notes.     │
  └─────────────────────────────────────────────────────────────┘

  📡 Results transmitted to eval_results.json

  End of scoring run. The void awaits your submission.
  May the scoring computer be less merciless next time. (It won't be.)
```

The `eval_results.json` file contains full per-signal breakdowns for error analysis.

## Running the Tests

The scoring functions have their own test suite (87 tests covering every edge case, boundary condition, and creative way a participant might return a boolean value). Run them if you want to understand exactly how scoring works, or if you've been tinkering with the harness code and want to make sure you haven't accidentally made the scoring computer more forgiving. (You haven't. It can't be.)

```bash
cd docs/eval
python test_scoring.py
```

All 87 should pass. If they don't, something's wrong with your environment, not the tests. The tests are deterministic. They are, in this regard, the only thing you can count on in the void.
