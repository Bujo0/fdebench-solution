# The Challenge

## The Scenario

Contoso Deep Space Station (∼2,000 crew) is drowning in mission ops signals. Their team of 12 manually triages ∼180 signals per day across 6 specialist teams. Average time-to-route: 3.4 hours. Misroute rate: 42%. In space, a misrouted signal isn't a KPI problem — it's a hull-breach-goes-unpatched problem. Commander Kapoor just got off a subspace relay with your manager and wants this fixed. She was polite about it. She is always polite about it. That is somehow worse.

**Start here. Read the mission briefing:** [customer_brief.md](customer_brief.md)
**Then review their routing guide:** [routing_guide.md](routing_guide.md) *(heads up: it's incomplete. Some signal types aren't covered, and some rules contradict each other. Chief Signal Officer Mehta's margin notes are worth reading. Welcome to deep space operations.)*

Your job: **build an AI-powered signal triage API** that CDSS can plug into their bridge terminal workflow.

---

## What You Are Building

A deployed API that accepts a mission ops signal and returns a triage decision. One endpoint, one JSON in, one JSON out. Simple as docking procedure. (Docking procedure is not simple. But you get the idea.)

### API Contract

**Endpoint:** `POST /triage`

**Request body** (a single signal):

```json
{
  "ticket_id": "SIG-4829",
  "subject": "cant get through airlock since this morning!!!",
  "description": "Hi, I've been trying to authenticate at the Deck 5 airlock since around 0700 station time but the BioAuth panel keeps rejecting my scan. I haven't changed my biometrics (obviously). I'm locked out of the lab section and have a sensor calibration scheduled at 1000. URGENT PLEASE. - Sarah",
  "reporter": {
    "name": "Sarah Chen",
    "email": "sarah.chen@cdss.space",
    "department": "Exobiology"
  },
  "created_at": "2026-03-15T07:32:00Z",
  "channel": "subspace_relay",
  "attachments": []
}
```

**Response body** (your triage decision):

```json
{
  "ticket_id": "SIG-4829",
  "category": "Crew Access & Biometrics",
  "priority": "P2",
  "assigned_team": "Crew Identity & Airlock Control",
  "needs_escalation": false,
  "missing_information": [
    "software_version",
    "affected_crew"
  ],
  "next_best_action": "Verify crew biometric profile status in BioScan ID and check for recent BioAuth policy changes affecting the Exobiology section",
  "remediation_steps": [
    "Check BioScan ID for crew profile lockout or disabled status",
    "Verify Deck 5 airlock BioAuth panel health and recent policy deployments",
    "If profile is locked, unlock and force biometric recalibration via self-service kiosk",
    "If airlock-specific, verify panel firmware version and re-push access profile via ShipOS MDM",
    "Confirm resolution with crew member and close signal"
  ]
}
```

See [../data/schemas/](../data/schemas/) for the formal JSON schemas.

### Valid Values for Classification Fields

Your system must use **exactly** these values. The scoring computer is cold and unforgiving, like the void of space. Anything not in these lists scores zero. The void does not grade on a curve.

**Categories** (8 values):

| Category | Description |
|---|---|
| `Crew Access & Biometrics` | Biometric scan, airlock codes, crew provisioning, station directory sync |
| `Hull & Structural Systems` | Hull integrity, habitat modules, fabricators, docking bays, physical systems |
| `Communications & Navigation` | Subspace relay, antenna arrays, beacon resolution, navigation, bandwidth |
| `Flight Software & Instruments` | Mission software, Station Suite, instrument calibration, licensing |
| `Threat Detection & Containment` | Hostile signals, malicious code, data breach, containment protocols, quantum certificates |
| `Telemetry & Data Banks` | Data relay hub, personal data vaults, data cores, backups, sensor archives |
| `Mission Briefing Request` | Questions, how-tos, or signals that don't fit other categories |
| `Not a Mission Signal` | Automated echoes, space noise, "thanks" messages, cryo-sleep auto-replies |

**Teams** (7 values):

| Team | When to route |
|---|---|
| `Crew Identity & Airlock Control` | Biometric scans, airlock codes, crew provisioning, station directory |
| `Spacecraft Systems Engineering` | Hull modules, OS, fleet management system, fabricators, instrument installs |
| `Deep Space Communications` | Subspace relay, antenna arrays, beacon resolution, defense grid, comm quality |
| `Mission Software Operations` | Flight nav system, mission tracking, quantum analyzer, Station Suite, internal tools |
| `Threat Response Command` | Hostile signals, malicious code, data loss, containment protocols, quantum certificates |
| `Telemetry & Data Core` | Data relay hub, personal data vaults, data cores, backups, sensor archives |
| `None` | Use when the signal is not a real mission signal |

**Priorities** (4 values): `P1` (🔴 Red Alert), `P2` (🟠 Yellow Alert), `P3` (🔵 Standard Ops), `P4` (🟢 Routine)

### Missing Information Vocabulary

When identifying missing information, use **only** values from this list. Scoring uses exact set matching, so free-text values will not match. The scoring computer does not interpret creative paraphrasing. It has no imagination. It lives in the void.

| Value | What it means |
|---|---|
| `affected_subsystem` | Which subsystem, instrument, or service is impacted |
| `anomaly_readout` | Exact error readout or anomaly code observed |
| `sequence_to_reproduce` | How to reproduce the anomaly |
| `affected_crew` | How many or which crew members are impacted |
| `habitat_conditions` | OS module, sector, configuration specifics, system IDs |
| `stardate` | When the anomaly started or was observed |
| `previous_signal_id` | Reference to a prior related signal |
| `crew_contact` | Reporter contact details or alternate contact |
| `module_specs` | Module make, model, specs |
| `software_version` | Software or instrument version number |
| `sector_coordinates` | Deck, level, sector segment, coordinates |
| `mission_impact` | Mission consequence or urgency context |
| `recurrence_pattern` | How often the anomaly occurs |
| `sensor_log_or_capture` | Visual evidence or sensor log file |
| `biometric_method` | Biometric type, authentication method, credential type |
| `system_configuration` | System config, protocol, or setup specifics |

### Health Check

Your service must also respond to `GET /health` with HTTP 200. Consider it a life-signs check. If your service doesn't have life signs, we can't score it. Much like crew members without life signs, it will be marked accordingly.

---

## The Data

| Dataset | Signals | Where | Purpose |
|---|---|---|---|
| **Sample + gold answers** | 25 | [sample.json](../data/signals/sample.json) + [sample_gold.json](../data/signals/sample_gold.json) | Iterate locally. Compare your output to the correct answers |
| **Public eval set** | 100 | [public_eval.json](../data/signals/public_eval.json) | Test at scale before submitting (no gold answers provided) |
| **Hidden eval set** | 1000+ | Not in this repo | Final scoring. Includes edge cases not in the public data. The void is creative. |

Signals vary in quality. Some are clean. Some are vague, contradictory, multi-issue, garbled, or not real mission ops requests at all. That's not a bug in the dataset. That's what signals from a 2,000-crew space station actually look like. Someone once filed a Red Alert because the nutrient synthesizer was dispensing vanilla instead of chocolate. Someone else filed a P4 Routine for a hull micro-fracture. Humans are chaos. Space makes it worse.

> **Don't overfit.** The hidden set has signal types you won't see in the public data. Build for the real void, not for 25 specific signals.

---

## Rules

- **One submission.** Make it count. There are no second chances. Like airlock procedures.
- Any language, framework, or AI model.
- Deployed and callable via HTTPS. Not localhost. Localhost is 0.3 AU away and nobody can reach it.
- AI coding assistants: encouraged. Use everything you've got. We are not above using robots to build robot helpers.
- All code must be your own work (AI-assisted is fine, copy-pasting someone else's solution is not — Commander Kapoor *will* find out).

---

## How We Score You

Your hidden-set **functional score** is **0–100**. Separately, we also review your repo for engineering quality. Think of it as two airlocks: one checks if your system works, the other checks if it was built to survive.

| Part | Weight | What we're looking at |
|---|---|---|
| **Functional scoring** | 0-100 | Does your system actually triage correctly? How fast and cheap is it? |
| **Engineering review** | Separate review | How did you build it? Can we read your code? Did you test it? Do your docs tell us *why*? |

### Functional Score (0-100)

We call your live endpoint with **1000+ signals you've never seen**. Every response is scored deterministically against gold answers. **No LLM judges. No vibes. Same logic as the local eval harness.** The scoring computer has no feelings. It has no mercy. It is, in this regard, very much like outer space. You can see exactly how you'll be scored before you submit.

#### What the platform does when it scores you

Here's exactly what happens when you hit "submit" on the platform:

1. **Health check.** `GET /health` must return 200. If it doesn't, scoring fails immediately. Your service flatlines. Mission aborted.
2. **Warm-up.** We send 3 throwaway requests first. These don't count toward your score. They exist so your cold start / first-request latency doesn't penalize you unfairly. Think of it as your system emerging from cryo-sleep — we give it a moment to get oriented.
3. **Scoring run.** We send all 1000+ signals to your `POST /triage` endpoint with **up to 10 requests in parallel**. Your API needs to handle concurrent load. If it can only process one request at a time, you'll hit timeouts. Space doesn't wait, and neither does the scoring harness.
4. **Timeout.** Each request has a **30-second timeout**. If your endpoint doesn't respond in 30 seconds, that signal scores zero on all dimensions. In space, 30 seconds is an eternity. In API design, it's generous.
5. **Retries.** Transient failures (5xx, timeouts) get **2 automatic retries** with backoff. Don't rely on this. Fix your errors instead. Hope is not a deployment strategy.
6. **Latency measurement.** We record the wall-clock time per request. Top and bottom 5% of latencies are trimmed before computing p50/p95 so a single spike doesn't tank your latency score.
7. **Cost measurement.** We read your `X-Model-Name`, `X-Prompt-Tokens`, and `X-Completion-Tokens` response headers (if present) and compute $/signal using published model pricing.

**Bottom line:** your API should comfortably handle 10 concurrent requests, respond in under 30 seconds each, and not fall over under sustained load. If you're using an LLM, make sure your model endpoint can handle the throughput. Rate limits and cold starts are your problem to solve. The void does not accept excuses about rate limiting.

The functional score has two components:

#### Classification (max 85 pts)

Five dimensions, scored at the **submission level** (not per-signal):

| Dimension | Weight | Metric | What it means |
|---|---|---|---|
| **Category** | 20% | Macro F1 | Per-class F1 averaged across all 8 categories. Systems that ignore rare classes are penalized. "Not a Mission Signal" trips everyone up — yes, even the ones who think they're ready. |
| **Priority** | 20% | Mean partial credit | Exact match = 1.0. Off by one level = 0.67. Off by two or more = 0.0. Averaged across all signals. Calling a hull breach "Routine" is a zero. And also a catastrophe. |
| **Routing** | 20% | Macro F1 | Per-class F1 averaged across all 7 teams. Same logic as category. Misrouting a containment breach to Telemetry & Data Core is the kind of mistake that ends up in the Admiral's next memo. |
| **Missing info** | 15% | Mean set F1 | Per-signal F1 over the constrained vocabulary, then averaged. Both empty = 1.0. |
| **Escalation** | 10% | Binary F1 | F1 for the positive class (`needs_escalation=true`) across all signals. |

The classification score is computed as:

```
weighted = 0.20×category + 0.20×priority + 0.20×routing + 0.15×missing_info + 0.10×escalation
classification_pts = (weighted / 0.85) × 85
```

> **Why macro F1 instead of accuracy?** Because accuracy is gameable. If 80% of signals are "Flight Software & Instruments", always predicting that class gets you 80% accuracy and a terrible macro F1. We want systems that handle *every* class well, including the rare ones like "Not a Mission Signal" that trip people up. Much like the Deck 9 cat, rare things still matter.

#### Efficiency (max 15 pts)

Two dimensions measuring whether you built something fast and lean, or something that burns through compute credits like a thruster test:

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

These headers are **optional**. If you don't send them, you get worst-case cost (as if you're running the most expensive model available with zero caching — like heating your entire deck by venting plasma). Latency is always measured server-side regardless.

#### Total functional score

```
functional_score = classification_pts + efficiency_pts
                 = (0–85)            + (0–15)
                 = 0–100
```

This is the 0–100 functional score you should optimize for on the hidden set. The closer to 100, the less likely Commander Kapoor is to mention your name in her next status report to the Admiral. (You want to avoid being mentioned.)

#### What about `next_best_action` and `remediation_steps`?

They're **required** in your response (the schema enforces it). But they're **not part of the functional score**. We look at remediation quality when we review your repo. Write good ones anyway. A system that says "investigate the anomaly" for every signal is telling us you phoned it in — and phoning it in has a 4-minute delay out here.

---

### Engineering Review

We review your repo the way Commander Kapoor reviews a mission report. Not a checkbox exercise, but a holistic read of how you think, build, and communicate.

This part is **not** a second hidden deterministic test set. There is no public `run_eng_eval.py` because this half is about the quality of the system you shipped and the reasoning you can show in your repo.

Think of it like this:

- **Functional score** asks: did your live system make the right triage decisions on hidden signals?
- **Engineering review** asks: if we opened your repo and reviewed it like fellow crew members, would we trust the engineering?

The signal we care about is very FDE-shaped: can you take an ambiguous operations problem, turn it into a clean service, make sensible tradeoffs, and ship something that still looks solid when we ask about latency, cost, failure modes, scale, security, and testing?

We're looking for: clean code, good tests, sensible architecture, infrastructure that works, and documentation that shows you *understood* the problem, not just threw tokens at it like cargo out an airlock.

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
- Did you test the edge cases you know crew will encounter?
- Could another engineer clone the repo, understand the design, and extend it without guessing what you meant?

**Three documents are mandatory.** Skip one and it will hurt the engineering review. Commander Kapoor reads all three. She reads quickly. She remembers everything.

#### `docs/architecture.md`

- What does your service do? How does it fit into CDSS's operations?
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
- Where does it break? Be honest. We can tell when you're not. Commander Kapoor can *definitely* tell.

> **Real talk:** a straightforward solution with honest error analysis and clear docs will outscore a complex system with no explanation. Every time. We've seen it. Like Titan Outpost, complexity without clarity ends badly.

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

If your repo is hard to follow, missing tests, or only works with undocumented setup magic, that will show up here. Much like an undocumented airlock bypass, it will eventually cause problems.

#### Do I need a complicated multi-agent system to score well?

No. A simple system with good judgment, good validation, solid tests, and honest writeups is a stronger submission than an overbuilt pipeline you can't explain. Overengineering is the Deck 7 atmospheric processor of software — it creates more problems than it solves.

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
- The whole thing feels like something a station ops team could actually operate

---

### Finalist Round (top N)

30-minute walkthrough of your solution, then 30 minutes of Q&A with FDE engineers. Think of it as a mission debrief, not an interrogation. We're curious about your decisions, not trying to catch you out. (That said, Commander Kapoor may attend. Remain calm.)

---

## Quick Start

```bash
# 1. Read the mission briefing and routing guide first. Seriously. It matters.
#    People who skip the brief misroute signals. People who misroute signals
#    end up in the Admiral's memos. You don't want to be in the Admiral's memos.
open docs/challenge/customer_brief.md
open docs/challenge/routing_guide.md

# 2. Look at the sample signals and gold answers
python -m json.tool docs/data/signals/sample.json | head -50
python -m json.tool docs/data/signals/sample_gold.json | head -50

# 3. Build something
# ... your code ...

# 4. Score it against the 25 sample signals
cd docs/eval
uv run python run_eval.py \
  --endpoint http://localhost:8000 \
  --dataset ../data/signals/sample.json \
  --gold ../data/signals/sample_gold.json

# 5. Stress-test against the 100 public eval signals
uv run python run_eval.py \
  --endpoint http://localhost:8000 \
  --dataset ../data/signals/public_eval.json

# 6. Deploy, write your docs, submit at aka.ms/fde/hackathon
# See docs/submission/
```

## Submission

When you're ready, submit at **[aka.ms/fde/hackathon](https://aka.ms/fde/hackathon)**. Full checklist at [../submission/](../submission/). May the void be indifferent in your favor.
