# Submission

## How to Submit

1. **Fork** this repository to your own GitHub account (your fork must be **public**)
2. **Build** your solution in your fork
3. **Deploy** your solution so it's callable via HTTPS
4. **Verify** `GET /health` returns HTTP 200 and `POST /triage` returns valid JSON
5. **Run** the eval harness against the sample gold set — make sure your scores are where you want them
6. **Create** `submission.json` at the root of your repo (see below)
7. **Write** the three mandatory documents: `docs/architecture.md`, `docs/methodology.md`, `docs/evals.md`
8. **Push** everything to your public fork
9. **Submit** your entry via the designated submission form (link shared at competition start)

## Required Files

All of the following are **mandatory**. Missing documents = reduced engineering score.

```
your-repo/
├── submission.json          # Submission metadata (see below)
├── README.md                # How to install, run, and test your solution
├── docs/
│   ├── architecture.md      # System design, AI pipeline, tradeoffs
│   ├── methodology.md       # Your approach, iteration, prompt strategy
│   └── evals.md             # Eval results, error analysis, limitations
└── ...                      # Your code, tests, infrastructure
```

## submission.json

```json
{
  "participant": "your-name",
  "endpoint_url": "https://your-deployed-endpoint.example.com",
  "repository_url": "https://github.com/your-username/your-repo",
  "timestamp": "2026-03-23T00:00:00Z"
}
```

## What Gets Evaluated

Your leaderboard score is **0–100**: 50% functional accuracy + 50% engineering quality.

| Part | Weight | How |
|---|---|---|
| **Functional accuracy** | 50% | ~100 hidden tickets scored deterministically against gold answers |
| **Engineering quality** | 50% | System design, code, infrastructure, docs, evals, production readiness |
| **Finalist round** | Unscored | 30-min walkthrough + 30-min Q&A with FDE engineers (top N only) |

## Required Documents

Full guidance on what to include: [challenge README — Engineering Quality](../challenge/README.md#part-2--engineering-quality).

**`docs/architecture.md`** — System design, component diagram, data flow, AI pipeline, tradeoffs, production readiness.

**`docs/methodology.md`** — Problem framing, strategy, iteration, prompt engineering, time allocation, retrospective.

**`docs/evals.md`** — Eval approach, quantitative results on sample set, error analysis, edge cases, known limitations.

Thoughtful docs from a simple solution score higher than a complex system with no explanation.

## Before You Submit Checklist

- [ ] `GET /health` returns HTTP 200
- [ ] `POST /triage` returns valid JSON matching the output schema
- [ ] Eval harness runs successfully against the 25 sample tickets
- [ ] Eval harness runs against the 50 public eval tickets without errors or timeouts
- [ ] `submission.json` is at the root of your repo with correct endpoint URL
- [ ] `docs/architecture.md` exists and is filled in
- [ ] `docs/methodology.md` exists and is filled in
- [ ] `docs/evals.md` exists and is filled in
- [ ] Your repo is **public** on GitHub
- [ ] All CI checks pass (pre-commit, pyright, pytest)
- [ ] Your README explains how to install, run, and test your solution

## Tips

- **Deploy early.** Don't wait until hour 23 to deploy. Get something live in the first few hours and iterate.
- **Test with the eval harness.** Run it against sample data, then public eval data. Iterate on your weak dimensions.
- **Read the customer brief.** It contains business context that should inform your classification, routing, and remediation decisions. Candidates who skip it produce worse output.
- **Handle errors gracefully.** If your system can't process a ticket, return a valid JSON response with reasonable defaults — don't return a 500.
- **Document your decisions.** "I chose X because Y" is more valuable than a polished README with no reasoning.
