# The Challenge

## The Scenario

Contoso Deep Space Station — CDSS (~450 crew members) is drowning in incoming signals. Their team of 12 mission ops analysts manually triages ~180 signals per day across 6 specialist divisions. Average time-to-route: 3.4 hours. Misroute rate: 42%. Their Admiral of Mission Operations just got off a comm-link with your manager and wants this fixed.

**Start here. Read the mission briefing:** [customer_brief.md](customer_brief.md)
**Then review their routing guide:** [routing_guide.md](routing_guide.md) *(heads up: it's incomplete. Some signal types aren't covered, and some rules contradict each other. Welcome to deep space operations.)*

Your job: **build an AI-powered signal triage API** that CDSS can plug into their Mission Control System workflow.

---

## What You Are Building

A deployed API that accepts an incoming mission signal and returns a triage decision. One endpoint, one JSON in, one JSON out.

### API Contract

**Endpoint:** `POST /triage`

**Request body** (a single signal):

```json
{
  "ticket_id": "SIG-4829",
  "subject": "Oxygen recycler malfunction in Habitat Module 3",
  "description": "The primary O2 recycler in Hab-3 started throwing anomaly codes around 0700 station time. CO2 levels rising at 0.3% per hour. Backup scrubbers are online but they're only rated for 12 hours. 53 crew in this module. We need engineering down here ASAP. - Lt. Vasquez",
  "reporter": {
    "name": "Lt. Vasquez",
    "email": "vasquez@contoso.space",
    "department": "Life Support"
  },
  "created_at": "2026-03-15T07:32:00Z",
  "channel": "emergency_beacon",
  "attachments": []
}
```

**Response body** (your triage decision):

```json
{
  "ticket_id": "SIG-4829",
  "category": "Hull & Structural Systems",
  "priority": "P1",
  "assigned_team": "Spacecraft Systems Engineering",
  "needs_escalation": true,
  "missing_information": [
    "anomaly_readout",
    "affected_crew"
  ],
  "next_best_action": "Dispatch engineering team to Hab-3 O2 recycler. Verify backup scrubber capacity and initiate crew evacuation protocol if CO2 exceeds 2.5%.",
  "remediation_steps": [
    "Run full diagnostics on primary O2 recycler and pull anomaly logs",
    "Verify backup scrubber runtime and rated capacity for 53 crew",
    "If primary recycler cannot be restarted, begin staged crew relocation to adjacent modules",
    "Cross-check atmospheric sensors station-wide for cascading failures",
    "Confirm resolution with reporting officer and close signal"
  ]
}
```

See [../data/schemas/](../data/schemas/) for the formal JSON schemas.

### Valid Values for Classification Fields

Your system must use **exactly** these values. The scoring is deterministic: anything not in these lists scores zero.

**Categories** (8 values):

| Category | Description |
|---|---|
| `Crew Access & Biometrics` | Crew login, SSO, biometric auth, account provisioning, registry sync |
| `Hull & Structural Systems` | Modules, hull integrity, airlocks, docking ports, structural components |
| `Communications & Navigation` | Subspace relay links, comms arrays, nav beacons, signal routing, sector links |
| `Flight Software & Instruments` | Mission apps, Mission Suite, installations, licensing, instrument integrations |
| `Threat Detection & Containment` | Hostile contacts, malware, data breaches, compliance, security certificates |
| `Telemetry & Data Banks` | DataVault, PersonalVault, databases, backups, data archives |
| `Mission Briefing Request` | Questions, how-tos, or issues that don't fit other categories |
| `Not a Mission Signal` | Auto-replies, spam, "thanks" messages, out-of-office |

**Teams** (7 values):

| Team | When to route |
|---|---|
| `Crew Identity & Airlock Control` | Crew login, SSO, biometric auth, account provisioning, Ship Identity Registry |
| `Spacecraft Systems Engineering` | Hull modules, structural systems, Fleet Device Manager, airlocks, hardware installs |
| `Deep Space Communications` | Subspace relay links, comms arrays, nav beacons, signal routing, proxies |
| `Mission Software Operations` | ATLAS Cargo System, HERMES Trade System, ORION Market Terminal, Mission Suite, internal tools |
| `Threat Response Command` | Hostile contacts, malware, data breaches, compliance, security certificates |
| `Telemetry & Data Core` | DataVault, PersonalVault, databases, backups, data archives |
| `None` | Use when the signal is not a real mission operations request |

**Priorities** (4 values): `P1` (Critical), `P2` (High), `P3` (Medium), `P4` (Low)

### Missing Information Vocabulary

When identifying missing information, use **only** values from this list. Scoring uses exact set matching, so free-text values will not match.

| Value | What it means |
|---|---|
| `affected_subsystem` | Which subsystem, instrument, or service is impacted |
| `anomaly_readout` | Exact anomaly text or code observed |
| `sequence_to_reproduce` | How to reproduce the issue |
| `affected_crew` | How many or which crew members are impacted |
| `habitat_conditions` | OS, sector, config specifics, system IDs |
| `stardate` | When the issue started or was observed |
| `previous_signal_id` | Reference to a prior related signal |
| `crew_contact` | Reporter contact details or alternate contact |
| `module_specs` | Module make, model, specs |
| `software_version` | Software or instrument version number |
| `sector_coordinates` | Station, deck, network segment, coordinates |
| `mission_impact` | Mission consequence or urgency context |
| `recurrence_pattern` | How often the issue occurs |
| `sensor_log_or_capture` | Visual evidence or log file |
| `biometric_method` | Biometric method, SSO type, credential type |
| `system_configuration` | System config, policy, or setup specifics |

### Health Check

Your service must also respond to `GET /health` with HTTP 200.

---

## The Data

| Dataset | Signals | Where | Purpose |
|---|---|---|---|
| **Sample + gold answers** | 25 | [sample.json](../data/tickets/sample.json) + [sample_gold.json](../data/tickets/sample_gold.json) | Iterate locally. Compare your output to the correct answers |
| **Public eval set** | 100 | [public_eval.json](../data/tickets/public_eval.json) | Test at scale before submitting (no gold answers provided) |
| **Hidden eval set** | 1000+ | Not in this repo | Final scoring. Includes edge cases not in the public data |

Signals vary in quality. Some are clean. Some are vague, contradictory, multi-issue, garbled, or not real mission signals at all. That's not a bug in the dataset. That's what deep space operations signals actually look like.

> **Don't overfit.** The hidden set has signal types you won't see in the public data. Build for the real world, not for 25 specific signals.

---

## Rules

- **One submission.** Make it count.
- Any language, framework, or AI model.
- Deployed and callable via HTTPS. Not localhost.
- AI coding assistants: encouraged. Use everything you've got.
- All code must be your own work (AI-assisted is fine, copy-pasting someone else's solution is not).

---

## How We Score You

Your hidden-set **functional score** is **0–100**. Separately, we also review your repo for engineering quality.

| Part | Weight | What we're looking at |
|---|---|---|
| **Functional scoring** | 0-100 | Does your system actually triage correctly? How fast and cheap is it? |
| **Engineering review** | Separate review | How did you build it? Can we read your code? Did you test it? Do your docs tell us *why*? |

### Functional Score (0-100)

We call your live endpoint with **1000+ signals you've never seen**. Every response is scored deterministically against gold answers. **No LLM judges. No vibes. Same logic as the local eval harness.** You can see exactly how you'll be scored before you submit.

#### What the platform does when it scores you

Here's exactly what happens when you hit "submit" on the platform:

1. **Health check.** `GET /health` must return 200. If it doesn't, scoring fails immediately.
2. **Warm-up.** We send 3 throwaway requests first. These don't count toward your score. They exist so your cold start / first-request latency doesn't penalize you unfairly.
3. **Scoring run.** We send all 1000+ signals to your `POST /triage` endpoint with **up to 10 requests in parallel**. Your API needs to handle concurrent load. If it can only process one request at a time, you'll hit timeouts.
4. **Timeout.** Each request has a **30-second timeout**. If your endpoint doesn't respond in 30 seconds, that signal scores zero on all dimensions.
5. **Retries.** Transient failures (5xx, timeouts) get **2 automatic retries** with backoff. Don't rely on this. Fix your errors instead.
6. **Latency measurement.** We record the wall-clock time per request. Top and bottom 5% of latencies are trimmed before computing p50/p95 so a single spike doesn't tank your latency score.
7. **Cost measurement.** We read your `X-Model-Name`, `X-Prompt-Tokens`, and `X-Completion-Tokens` response headers (if present) and compute $/signal using published model pricing.

**Bottom line:** your API should comfortably handle 10 concurrent requests, respond in under 30 seconds each, and not fall over under sustained load. If you're using an LLM, make sure your model endpoint can handle the throughput. Rate limits and cold starts are your problem to solve.

The functional score has two components:

#### Classification (max 85 pts)

Five dimensions, scored at the **submission level** (not per-signal):

| Dimension | Weight | Metric | What it means |
|---|---|---|---|
| **Category** | 20% | Macro F1 | Per-class F1 averaged across all 8 categories. Systems that ignore rare classes are penalized. |
| **Priority** | 20% | Mean partial credit | Exact match = 1.0. Off by one level = 0.67. Off by two or more = 0.0. Averaged across all signals. |
| **Routing** | 20% | Macro F1 | Per-class F1 averaged across all 7 teams. Same logic as category. |
| **Missing info** | 15% | Mean set F1 | Per-signal F1 over the constrained vocabulary, then averaged. Both empty = 1.0. |
| **Escalation** | 10% | Binary F1 | F1 for the positive class (`needs_escalation=true`) across all signals. |

The classification score is computed as:

```
weighted = 0.20×category + 0.20×priority + 0.20×routing + 0.15×missing_info + 0.10×escalation
classification_pts = (weighted / 0.85) × 85
```

> **Why macro F1 instead of accuracy?** Because accuracy is gameable. If 80% of signals are "Flight Software & Instruments", always predicting that class gets you 80% accuracy and a terrible macro F1. We want systems that handle *every* class well, including the rare ones like "Not a Mission Signal" that trip people up.

#### Efficiency (max 15 pts)

Two dimensions measuring whether you built something fast and lean, or something that burns $0.50 of GPT-4 per signal:

| Dimension | Weight | Best (1.0) | Worst (0.0) |
|---|---|---|---|
| **Latency** | 10% | p50 ≤ 200ms | p50 ≥ 2000ms |
| **Cost** | 5% | ≤ $0.001/signal | ≥ $0.05/signal |

Latency is interpolated linearly. Cost is interpolated on a log scale.

**To participate in cost scoring**, return these response headers from your `/triage` endpoint:

| Header | Type | Example |
|---|---|---|
| `X-Model-Name` | string | `gpt-4o-mini` |
| `X-Prompt-Tokens` | integer | `1250` |
| `X-Completion-Tokens` | integer | `340` |

These headers are **optional**. If you don't send them, you get worst-case cost (as if you're running GPT-4 with zero caching). Latency is always measured server-side regardless.

#### Total functional score

```
functional_score = classification_pts + efficiency_pts
                 = (0–85)            + (0–15)
                 = 0–100
```

This is the 0–100 functional score you should optimize for on the hidden set.

#### What about `next_best_action` and `remediation_steps`?

They're **required** in your response (the schema enforces it). But they're **not part of the functional score**. We look at remediation quality when we review your repo. Write good ones anyway. A system that says "investigate the issue" for every signal is telling us you phoned it in.

---

### Engineering Review

We review your repo the way a senior engineer reviews a pull request. Not a checkbox exercise, but a holistic read of how you think, build, and communicate.

This part is **not** a second hidden deterministic test set. There is no public `run_eng_eval.py` because this half is about the quality of the system you shipped and the reasoning you can show in your repo.

Think of it like this:

- **Functional score** asks: did your live system make the right triage decisions on hidden signals?
- **Engineering review** asks: if we opened your repo and reviewed it like teammates, would we trust the engineering?

The signal we care about is very FDE-shaped: can you take an ambiguous mission problem, turn it into a clean service, make sensible tradeoffs, and ship something that still looks solid when we ask about latency, cost, failure modes, scale, security, and testing?

We're looking for: clean code, good tests, sensible architecture, infrastructure that works, and documentation that shows you *understood* the problem, not just threw tokens at it.

In practice, the strongest submissions usually do these things well:

- Thin API layer, with business logic separated from route handlers
- Typed models and schema validation on both input and output
- Async external calls with explicit timeouts
- Clear error handling instead of generic 500s everywhere
- Tests for core logic, edge cases, and API behavior
- Environment-based configuration, no secrets in source, and runnable deployment setup
- Docs that explain **why** decisions were made, not just what files exist

In other words, we are not just looking for a model call that happens to classify signals well on a lucky day. We want to see engineering judgment:

- Can the service stay fast enough to survive the scoring run?
- Did you think about cost instead of brute-forcing everything with the biggest model?
- Do you validate inputs and outputs so bad responses do not leak into the API contract?
- Will the system fail gracefully when the model is slow, wrong, or unavailable?
- Did you test the edge cases you know crew members will hit?
- Could another engineer clone the repo, understand the design, and extend it without guessing what you meant?

**Three documents are mandatory.** Skip one and it will hurt the engineering review.

#### `docs/architecture.md`

- What does your service do? How does it fit into the CDSS mission?
- Draw something. ASCII, Mermaid, napkin sketch, whatever. Show the moving parts.
- Data flow: signal goes in, triage comes out, what happened in between?
- AI pipeline: what model(s), why, how do you call them?
- Tradeoffs: what else did you consider? Why not that?
- Production readiness: what would you change if this had to handle 10,000 signals/day?

#### `docs/methodology.md`

- How did you read the mission briefing? What jumped out?
- What was your strategy? Baseline first? Edge cases early? How did you decide what to do in what order?
- What did you try that didn't work? What did you change?
- How did you design and iterate on your prompts?
- How did you actually spend your time?
- What would you do differently with another day?

#### `docs/evals.md`

- How did you test? Just the gold set, or did you write your own test cases too?
- Show us your numbers. Per-dimension scores on the sample set.
- Which signals did your system get wrong? Why?
- What are the hardest signal types for your system?
- Where does it break? Be honest. We can tell when you're not.

> **Real talk:** a straightforward solution with honest error analysis and clear docs will outscore a complex system with no explanation. Every time. We've seen it.

We also look at: code quality, test coverage, error handling, infrastructure, CI/CD, and whether your README actually lets someone else clone and run your system in under 5 minutes.

### FAQ

#### Is engineering review another hidden test suite?

No. The hidden eval set applies to the **functional score**. Engineering review happens separately based on your repo, docs, code structure, tests, deployment readiness, and the quality of the system you built.

#### If engineering review happens separately, what should I optimize for?

Optimize for trust. A reviewer should be able to open your repo and quickly see:

- how requests flow through the system
- where the LLM or rules logic lives
- how failures are handled
- how to run and test the service
- what you tried, what failed, and what tradeoffs you made

If your repo is hard to follow, missing tests, or only works with undocumented setup magic, that will show up here.

#### Do I need a complicated multi-agent system to score well?

No. A simple system with good judgment, good validation, solid tests, and honest writeups is a stronger submission than an overbuilt pipeline you can't explain.

#### Are `next_best_action` and `remediation_steps` part of the hidden functional score?

Not directly. They are required by the schema, but they are reviewed as part of the engineering-quality half. If those fields are vague, generic, or obviously low effort, that hurts you.

#### What usually makes an engineering submission look weak?

- Business logic buried in one route file
- No timeouts or retry handling around model calls
- No tests beyond a happy path
- Missing docs or docs that only describe the final state
- Hardcoded config, secrets, or localhost-only assumptions
- README that does not let someone run the project quickly

#### What makes a submission feel strong in an FDE way?

- The design is simple, but clearly intentional
- The API contract is treated seriously, with validation and predictable errors
- Latency and cost are managed as engineering constraints, not ignored until the end
- Tests cover weird signals, failure cases, and non-happy paths
- The repo shows evidence of iteration, tradeoffs, and honest evaluation
- The whole thing feels like something a mission operations team could actually operate

---

### Finalist Round (top N)

30-minute walkthrough of your solution, then 30 minutes of Q&A with FDE engineers. Think of it as a design review, not an interview. We're curious about your decisions, not trying to catch you out.

---

## Quick Start

```bash
# 1. Read the mission briefing and routing guide first. Seriously. It matters.
open docs/challenge/customer_brief.md
open docs/challenge/routing_guide.md

# 2. Look at the sample signals and gold answers
python -m json.tool docs/data/tickets/sample.json | head -50
python -m json.tool docs/data/tickets/sample_gold.json | head -50

# 3. Build something
# ... your code ...

# 4. Score it against the 25 sample signals
cd docs/eval
uv run python run_eval.py \
  --endpoint http://localhost:8000 \
  --dataset ../data/tickets/sample.json \
  --gold ../data/tickets/sample_gold.json

# 5. Stress-test against the 100 public eval signals
uv run python run_eval.py \
  --endpoint http://localhost:8000 \
  --dataset ../data/tickets/public_eval.json

# 6. Deploy, write your docs, submit at aka.ms/fde/hackathon
# See docs/submission/
```

## Submission

When you're ready, submit at **[aka.ms/fde/hackathon](https://aka.ms/fde/hackathon)**. Full checklist at [../submission/](../submission/).
