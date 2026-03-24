# Challenge

> **Build like an FDE. Bring your best.**

## The Scenario

Contoso Financial Services is a mid-size financial enterprise (~4,500 employees) drowning in IT support tickets. Their support team of 12 manually triages ~180 tickets per day across 6 specialist teams. Average time-to-route is 3.4 hours. 42% of tickets get misrouted at least once. Their VP of IT Operations is asking for help.

**Read the full customer brief:** [customer_brief.md](customer_brief.md)
**Review their internal routing guide:** [routing_guide.md](routing_guide.md) *(note: this guide is incomplete — some ticket types aren't covered)*

Your job: **build an AI-powered ticket triage API** that Contoso can call for every incoming ticket.

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

See [../data/](../data/) for the full input/output JSON schemas.

### Missing Information Vocabulary

When identifying missing information, your system must use **only** values from this list. Deterministic scoring uses exact set matching — free-text values will not match.

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

## The Data

| Dataset | Size | Where | Purpose |
|---|---|---|---|
| **Sample set + gold answers** | 25 tickets | [sample.json](../data/tickets/sample.json) + [sample_gold.json](../data/tickets/sample_gold.json) | Iterate locally — compare your output to the correct answers |
| **Public eval set** | ~50 tickets | [public_eval.json](../data/tickets/public_eval.json) | Test at scale before submitting (no gold answers) |
| **Hidden eval set** | ~100 tickets | Not in this repo | Final scoring — includes edge cases not in the public data |

Tickets vary in quality. Some are clean. Some are vague, contradictory, multi-issue, garbled, or not real support requests. This is realistic.

## Rules

- **24-hour build window** from the published start time
- **One final submission** per participant
- Any programming language, framework, or AI model
- Deployed and callable via HTTPS
- AI coding assistants allowed and encouraged
- All code must be your own work

## Evaluation

Your final leaderboard score is **0–100**, composed of two equally weighted parts:

| Part | Weight | What it measures |
|---|---|---|
| **Functional accuracy** | 50% | How correctly your system triages ~100 hidden tickets |
| **Engineering quality** | 50% | How well you built it — design, code, docs, evals, infrastructure |

---

### Part 1 — Functional Score (50% of final score)

Your endpoint is called with **~100 hidden tickets**. Each response is scored against gold answers using the **same logic** you practice with on the sample set:

| Dimension | Method |
|---|---|
| Category | Exact match |
| Priority | Exact match — off by 1 level = partial credit, off by 2+ = zero |
| Routing | Exact match |
| Missing information | Set F1 (precision + recall on the constrained vocabulary) |
| Escalation | Binary match |
| Remediation | Completeness, specificity, logical ordering |

Calibrate on the 25 sample tickets. Test on the 50 public tickets. The hidden set has scenarios not in the public data.

---

### Part 2 — Engineering Quality (50% of final score)

We evaluate your repository across multiple dimensions: system design, code quality, infrastructure, tests, documentation, eval rigor, and production readiness.

**Three documents are mandatory.** Missing any = reduced engineering score.

#### `docs/architecture.md`

- System overview — what your service does
- Component diagram (ASCII, Mermaid, or image)
- Data flow — ticket in, response out, what happens in between
- AI pipeline — how you use LLMs, why this approach
- Tradeoffs — alternatives you considered, what you'd change
- Production readiness — what would need to change for real use

#### `docs/methodology.md`

- Problem framing — how you read the customer brief and routing guide
- Strategy — baseline first? Edge cases early? How you prioritized
- Iteration — what you tried, what failed, what you changed
- Prompt engineering — how you designed, tested, improved prompts
- Time allocation — how you spent the 24 hours
- Retrospective — what you'd do differently with more time

#### `docs/evals.md`

- How you tested — gold set scoring, custom test cases, other methods
- Results — actual numbers per dimension on the sample set
- Error analysis — which tickets fail and why
- Edge cases — hardest ticket types for your system
- Limitations — where your system is strong and where it's weak

---

### Finalist Round (top N only)

30-minute solution walkthrough + 30-minute technical Q&A with FDE engineers.

## Quick Start

```bash
# 1. Read the customer brief and routing guide
open docs/challenge/customer_brief.md
open docs/challenge/routing_guide.md

# 2. Explore sample tickets + gold answers
python -m json.tool docs/data/tickets/sample.json
python -m json.tool docs/data/tickets/sample_gold.json

# 3. Build your solution
# ... your code ...

# 4. Test locally against sample gold
cd docs/eval
uv run python run_eval.py --endpoint http://localhost:8000 --dataset ../data/tickets/sample.json --gold ../data/tickets/sample_gold.json

# 5. Deploy and submit
# See docs/submission/
```

## Submission

See [../submission/](../submission/) for how to submit.
