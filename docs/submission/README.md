# Submission

## How to Submit

1. **Fork** this repo (your fork must be **public**)
2. **Build** your solution
3. **Deploy** it somewhere callable via HTTPS
4. **Test** with the eval harness: sample set for scoring, public eval for smoke testing
5. **Write** your three docs: `docs/architecture.md`, `docs/methodology.md`, `docs/evals.md`
6. **Create** `submission.json` at the root (see below)
7. **Push** everything
8. **Submit** at **[aka.ms/fde/hackathon](https://aka.ms/fde/hackathon)** (the hackathon platform where you register your endpoint and trigger scoring)

## Required Files

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

**All three docs are mandatory.** Missing one is a big hit to your engineering score.

Important nuance: the hidden tickets are for the **functional** half. The **engineering** half comes from reviewing what is in your repo after you submit.

What we want to see is not just that you got a decent score. We want to see how you built a system: clear design, sensible model usage, attention to latency and cost, tests that cover real failure modes, and engineering choices that would hold up in front of a customer team.

## submission.json

Drop this at the root of your repo:

```json
{
  "participant": "your-name",
  "endpoint_url": "https://your-deployed-endpoint.example.com",
  "repository_url": "https://github.com/your-username/your-repo",
  "timestamp": "2026-03-23T00:00:00Z"
}
```

## What Gets Evaluated

| Component | Weight | How it's scored |
|---|---|---|
| **Classification accuracy** | 42.5 pts | 5 dimensions via macro F1, ordinal credit, set F1, binary F1 (max 85 pts × 50% leaderboard weight) |
| **Efficiency** | 7.5 pts | Latency (p50) + cost ($/ticket) from response headers (max 15 pts × 50%) |
| **Engineering quality** | 50 pts | Repo review of system design, code quality, tests, docs, evals, infrastructure, and production readiness. This is not a second hidden deterministic harness |

Full scoring details: [challenge README](../challenge/README.md#how-we-score-you)

## Required Documents

See [challenge README: Engineering Quality](../challenge/README.md#part-2-engineering-quality-50-pts) for what goes in each one.

| Document | What we want to see |
|---|---|
| `docs/architecture.md` | System design, data flow, AI pipeline, tradeoffs, what you'd change for prod |
| `docs/methodology.md` | How you approached it, what you tried, what failed, how you spent your time |
| `docs/evals.md` | Your actual numbers, which tickets you got wrong and why, where your system breaks |

> **Seriously:** a clean, simple solution with honest error analysis beats a complex system with no explanation. Every single time.

## Before You Submit

- [ ] `GET /health` returns HTTP 200
- [ ] `POST /triage` returns valid JSON matching the [output schema](../data/schemas/output.json)
- [ ] All 8 response fields are present: `ticket_id`, `category`, `priority`, `assigned_team`, `needs_escalation`, `missing_information`, `next_best_action`, `remediation_steps`
- [ ] `category` values are from the 8 valid categories
- [ ] `assigned_team` values are from the 7 valid teams (including `"None"`)
- [ ] `missing_information` values are from the 16-value constrained vocabulary
- [ ] Your API handles **10 concurrent requests** without errors or timeouts
- [ ] Each request responds in **under 30 seconds** (that's the timeout, aim for well under)
- [ ] Eval harness runs against 25 sample tickets with gold scoring
- [ ] Eval harness runs against 50 public eval tickets without errors or timeouts
- [ ] `submission.json` at repo root with correct endpoint URL
- [ ] `docs/architecture.md` exists and is substantive
- [ ] `docs/methodology.md` exists and is substantive
- [ ] `docs/evals.md` exists and includes actual numbers from the sample set
- [ ] Your repo is **public** on GitHub
- [ ] Your README explains how to install, run, and test your solution locally
- [ ] You've submitted at **[aka.ms/fde/hackathon](https://aka.ms/fde/hackathon)**

## Tips

- **Deploy early.** Get something live in hour 2 and iterate. The number of people who deploy at hour 23 and then panic is... nonzero.
- **Run the eval harness constantly.** It's the same scoring logic as the platform. Trust the numbers.
- **Read the customer brief.** Candidates who skip it produce noticeably worse output. The business context matters for routing and remediation.
- **Handle the weird tickets.** The hidden eval has stuff you haven't seen: vague tickets, multi-issue tickets, spam. If your system 500s on a confusing ticket, that's a zero on every dimension.
- **Return valid JSON even when confused.** A reasonable default beats a stack trace.
- **Explain your decisions.** "I chose X because Y" is worth more than a polished README that says nothing. We want to see how you think.
- **Send the cost headers.** It's only 5% of the score, but it signals you actually read the spec.
- **Treat the repo like part of the product.** The endpoint gets you through Part 1. The repo is what earns the other 50 points.
- **Show engineering judgment.** Good submissions usually have explicit timeouts, validation, useful tests, clean config, and a believable story for scale, security, and operability.
