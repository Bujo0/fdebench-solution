# The Challenge

## The Scenario

Contoso Financial Services (∼4,500 employees) is drowning in IT support tickets. Their team of 12 manually triages ∼180 tickets per day across 6 specialist teams. Average time-to-route: 3.4 hours. Misroute rate: 42%. Their VP of IT Operations just got off a call with your manager and wants this fixed.

**Start here — read the customer brief:** [customer_brief.md](customer_brief.md)
**Then review their routing guide:** [routing_guide.md](routing_guide.md) *(heads up: it's incomplete — some ticket types aren't covered, and some rules contradict each other. Welcome to enterprise IT.)*

Your job: **build an AI-powered ticket triage API** that Contoso can plug into their ServiceNow workflow.

---

## What You Are Building

A deployed API that accepts an IT support ticket and returns a triage decision. One endpoint, one JSON in, one JSON out.

### API Contract

**Endpoint:** `POST /triage`

**Request body** — a single ticket:

```json
{
  "ticket_id": "INC-4829",
  "subject": "cant login since this morning!!!",
  "description": "Hi, I've been trying to login to the VPN since around 7am but it keeps saying my credentials are wrong. I haven't changed my password. I'm remote today and have a client call at 10. URGENT PLEASE. - Sarah",
  "reporter": {
    "name": "Sarah Chen",
    "email": "sarah.chen@contoso.com",
    "department": "Wealth Management"
  },
  "created_at": "2026-03-15T07:32:00Z",
  "channel": "email",
  "attachments": []
}
```

**Response body** — your triage decision:

```json
{
  "ticket_id": "INC-4829",
  "category": "Access & Authentication",
  "priority": "P2",
  "assigned_team": "Identity & Access Management",
  "needs_escalation": false,
  "missing_information": [
    "application_version",
    "affected_users"
  ],
  "next_best_action": "Verify account lockout status in Entra ID and check for recent MFA policy changes affecting the Wealth Management OU",
  "remediation_steps": [
    "Check Entra ID for account lockout or disabled status",
    "Verify VPN gateway health and recent policy deployments",
    "If account is locked, unlock and force password reset via self-service portal",
    "If VPN-specific, verify client version and re-push VPN profile via Intune",
    "Confirm resolution with reporter and close ticket"
  ]
}
```

See [../data/schemas/](../data/schemas/) for the formal JSON schemas.

### Valid Values for Classification Fields

Your system must use **exactly** these values. The scoring is deterministic — anything not in these lists scores zero.

**Categories** (8 values):

| Category | Description |
|---|---|
| `Access & Authentication` | Login, SSO, MFA, account provisioning, directory sync |
| `Hardware & Peripherals` | Laptops, desktops, monitors, printers, peripherals |
| `Network & Connectivity` | VPN, WiFi, DNS, firewall, bandwidth, WAN/LAN |
| `Software & Applications` | Business apps, M365, installations, licensing, integrations |
| `Security & Compliance` | Phishing, malware, data loss, compliance, certificates |
| `Data & Storage` | SharePoint, OneDrive, databases, backups, file shares |
| `General Inquiry` | Questions, how-tos, or issues that don't fit other categories |
| `Not a Support Ticket` | Auto-replies, spam, "thanks" messages, out-of-office |

**Teams** (7 values):

| Team | When to route |
|---|---|
| `Identity & Access Management` | Login, SSO, MFA, account provisioning, Entra ID |
| `Endpoint Engineering` | Laptops, OS, Intune, peripherals, software installs |
| `Network Operations` | VPN, WiFi, DNS, firewall, proxy |
| `Enterprise Applications` | SAP, Salesforce, Bloomberg, M365, internal tools |
| `Security Operations` | Phishing, malware, data loss, compliance, certificates |
| `Data Platform` | SharePoint, OneDrive, databases, backups, file shares |
| `None` | Use when the ticket is not a real support request |

**Priorities** (4 values): `P1` (Critical), `P2` (High), `P3` (Medium), `P4` (Low)

### Missing Information Vocabulary

When identifying missing information, use **only** values from this list. Scoring uses exact set matching — free-text values will not match.

| Value | What it means |
|---|---|
| `affected_system` | Which system, app, or service is impacted |
| `error_message` | Exact error text or code observed |
| `steps_to_reproduce` | How to reproduce the issue |
| `affected_users` | How many or which users are impacted |
| `environment_details` | OS, region, config specifics, system IDs |
| `timestamp` | When the issue started or was observed |
| `previous_ticket_id` | Reference to a prior related ticket |
| `contact_info` | Reporter contact details or alternate contact |
| `device_info` | Device make, model, specs |
| `application_version` | Software or app version number |
| `network_location` | Office, floor, network segment, IP address |
| `business_impact` | Business consequence or urgency context |
| `reproduction_frequency` | How often the issue occurs |
| `screenshot_or_attachment` | Visual evidence or log file |
| `authentication_method` | MFA method, SSO type, credential type |
| `configuration_details` | System config, policy, or setup specifics |

### Health Check

Your service must also respond to `GET /health` with HTTP 200.

---

## The Data

| Dataset | Tickets | Where | Purpose |
|---|---|---|---|
| **Sample + gold answers** | 25 | [sample.json](../data/tickets/sample.json) + [sample_gold.json](../data/tickets/sample_gold.json) | Iterate locally — compare your output to the correct answers |
| **Public eval set** | 50 | [public_eval.json](../data/tickets/public_eval.json) | Test at scale before submitting (no gold answers provided) |
| **Hidden eval set** | ~100 | Not in this repo | Final scoring — includes edge cases not in the public data |

Tickets vary in quality. Some are clean. Some are vague, contradictory, multi-issue, garbled, or not real support requests at all. That's not a bug in the dataset — that's what enterprise tickets actually look like.

> **Don't overfit.** The hidden set has ticket types you won't see in the public data. Build for the real world, not for 25 specific tickets.

---

## Rules

- **One submission.** Make it count.
- Any language, framework, or AI model.
- Deployed and callable via HTTPS. Not localhost.
- AI coding assistants — encouraged. Use everything you've got.
- All code must be your own work (AI-assisted is fine, copy-pasting someone else's solution is not).

---

## How We Score You

Your final score is **0–100**. Two halves, equally weighted:

| Part | Weight | What we're looking at |
|---|---|---|
| **Functional accuracy** | 50 pts | Does your system actually triage correctly? How fast and cheap is it? |
| **Engineering quality** | 50 pts | How did you build it? Can we read your code? Did you test it? Do your docs tell us *why*? |

### Part 1 — Functional Score (50 pts)

We call your live endpoint with **~100 tickets you've never seen**. Every response is scored deterministically against gold answers. **No LLM judges. No vibes. Same logic as the local eval harness** — you can see exactly how you'll be scored before you submit.

#### What the platform does when it scores you

Here's exactly what happens when you hit "submit" on the platform:

1. **Health check** — `GET /health` must return 200. If it doesn't, scoring fails immediately.
2. **Warm-up** — We send 3 throwaway requests first. These don't count toward your score. They exist so your cold start / first-request latency doesn't penalize you unfairly.
3. **Scoring run** — We send all ~100 tickets to your `POST /triage` endpoint with **up to 10 requests in parallel**. Your API needs to handle concurrent load — if it can only process one request at a time, you'll hit timeouts.
4. **Timeout** — Each request has a **30-second timeout**. If your endpoint doesn't respond in 30 seconds, that ticket scores zero on all dimensions.
5. **Retries** — Transient failures (5xx, timeouts) get **2 automatic retries** with backoff. Don't rely on this — fix your errors instead.
6. **Latency measurement** — We record the wall-clock time per request. Top and bottom 5% of latencies are trimmed before computing p50/p95 so a single spike doesn't tank your latency score.
7. **Cost measurement** — We read your `X-Model-Name`, `X-Prompt-Tokens`, and `X-Completion-Tokens` response headers (if present) and compute $/ticket using published model pricing.

**Bottom line:** your API should comfortably handle 10 concurrent requests, respond in under 30 seconds each, and not fall over under sustained load. If you're using an LLM, make sure your model endpoint can handle the throughput — rate limits and cold starts are your problem to solve.

The functional score has two components:

#### Classification (max 85 pts)

Five dimensions, scored at the **submission level** (not per-ticket):

| Dimension | Weight | Metric | What it means |
|---|---|---|---|
| **Category** | 20% | Macro F1 | Per-class F1 averaged across all 8 categories. Systems that ignore rare classes are penalized. |
| **Priority** | 20% | Mean partial credit | Exact match = 1.0. Off by one level = 0.67. Off by two or more = 0.0. Averaged across all tickets. |
| **Routing** | 20% | Macro F1 | Per-class F1 averaged across all 7 teams. Same logic as category. |
| **Missing info** | 15% | Mean set F1 | Per-ticket F1 over the constrained vocabulary, then averaged. Both empty = 1.0. |
| **Escalation** | 10% | Binary F1 | F1 for the positive class (`needs_escalation=true`) across all tickets. |

The classification score is computed as:

```
weighted = 0.20×category + 0.20×priority + 0.20×routing + 0.15×missing_info + 0.10×escalation
classification_pts = (weighted / 0.85) × 85
```

> **Why macro F1 instead of accuracy?** Because accuracy is gameable. If 80% of tickets are "Software & Applications", always predicting that class gets you 80% accuracy — and a terrible macro F1. We want systems that handle *every* class well, including the rare ones like "Not a Support Ticket" that trip people up.

#### Efficiency (max 15 pts)

Two dimensions measuring whether you built something fast and lean, or something that burns $0.50 of GPT-4 per ticket:

| Dimension | Weight | Best (1.0) | Worst (0.0) |
|---|---|---|---|
| **Latency** | 10% | p50 ≤ 200ms | p50 ≥ 2000ms |
| **Cost** | 5% | ≤ $0.001/ticket | ≥ $0.05/ticket |

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

This 0–100 number is then weighted as 50% of your leaderboard score.

#### What about `next_best_action` and `remediation_steps`?

They're **required** in your response — the schema enforces it. But they're **not part of the functional score**. We look at remediation quality when we review your repo (Part 2). Write good ones anyway — a system that says "investigate the issue" for every ticket is telling us you phoned it in.

---

### Part 2 — Engineering Quality (50 pts)

We review your repo the way a senior engineer reviews a pull request. Not a checkbox exercise — a holistic read of how you think, build, and communicate.

We're looking for: clean code, good tests, sensible architecture, infrastructure that works, and documentation that shows you *understood* the problem — not just threw tokens at it.

**Three documents are mandatory.** Skip one and you'll feel it in the score.

#### `docs/architecture.md`

- What does your service do? How does it fit into Contoso's world?
- Draw something — ASCII, Mermaid, napkin sketch, whatever. Show the moving parts.
- Data flow: ticket goes in, triage comes out, what happened in between?
- AI pipeline: what model(s), why, how do you call them?
- Tradeoffs: what else did you consider? Why not that?
- Production readiness: what would you change if this had to handle 10,000 tickets/day?

#### `docs/methodology.md`

- How did you read the customer brief? What jumped out?
- What was your strategy? Baseline first? Edge cases early? How did you decide what to do in what order?
- What did you try that didn't work? What did you change?
- How did you design and iterate on your prompts?
- How did you actually spend your time?
- What would you do differently with another day?

#### `docs/evals.md`

- How did you test? Just the gold set, or did you write your own test cases too?
- Show us your numbers — per-dimension scores on the sample set.
- Which tickets did your system get wrong? Why?
- What are the hardest ticket types for your system?
- Where does it break? Be honest — we can tell when you're not.

> **Real talk:** a straightforward solution with honest error analysis and clear docs will outscore a complex system with no explanation. Every time. We've seen it.

We also look at: code quality, test coverage, error handling, infrastructure, CI/CD, and whether your README actually lets someone else clone and run your system in under 5 minutes.

---

### Finalist Round (top N)

30-minute walkthrough of your solution, then 30 minutes of Q&A with FDE engineers. Think of it as a design review, not an interview. We're curious about your decisions, not trying to catch you out.

---

## Quick Start

```bash
# 1. Read the customer brief and routing guide first. Seriously. It matters.
open docs/challenge/customer_brief.md
open docs/challenge/routing_guide.md

# 2. Look at the sample tickets and gold answers
python -m json.tool docs/data/tickets/sample.json | head -50
python -m json.tool docs/data/tickets/sample_gold.json | head -50

# 3. Build something
# ... your code ...

# 4. Score it against the 25 sample tickets
cd docs/eval
uv run python run_eval.py \
  --endpoint http://localhost:8000 \
  --dataset ../data/tickets/sample.json \
  --gold ../data/tickets/sample_gold.json

# 5. Stress-test against the 50 public eval tickets
uv run python run_eval.py \
  --endpoint http://localhost:8000 \
  --dataset ../data/tickets/public_eval.json

# 6. Deploy, write your docs, submit at aka.ms/fde/hackathon
# See docs/submission/
```

## Submission

When you're ready, submit at **[aka.ms/fde/hackathon](https://aka.ms/fde/hackathon)**. Full checklist at [../submission/](../submission/).
