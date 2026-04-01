# Dataset

Synthetic tickets modeled on real enterprise IT support. They're messy on purpose.

## Structure

```
data/
├── README.md                  # This file
├── tickets/
│   ├── sample.json            # 25 tickets for local development
│   ├── sample_gold.json       # Gold-standard triage outputs for the sample set
│   └── public_eval.json       # 50 tickets for pre-submission testing
└── schemas/
    ├── input.json             # JSON Schema for ticket input
    └── output.json            # JSON Schema for expected triage output
```

## Ticket Format (Input)

Each ticket has these fields:

| Field | Type | Description |
|---|---|---|
| `ticket_id` | string | Unique ID (e.g., `INC-4829`) |
| `subject` | string | Short summary. May be vague or misleading. |
| `description` | string | Full ticket body. Quality varies wildly. |
| `reporter` | object | `{ name, email, department }` |
| `created_at` | datetime | ISO 8601 timestamp |
| `channel` | enum | `email`, `chat`, `portal`, or `phone` |
| `attachments` | string[] | Filenames mentioned (not actual files) |

See [schemas/input.json](schemas/input.json) for the formal JSON Schema.

## Triage Output Format

Your `/triage` endpoint must return **all 8 fields**:

| Field | Type | Scored? | Notes |
|---|---|---|---|
| `ticket_id` | string | — | Must match the input exactly |
| `category` | string | **Yes** (20%) | One of 8 valid categories |
| `priority` | string | **Yes** (20%) | `P1`, `P2`, `P3`, or `P4` |
| `assigned_team` | string | **Yes** (20%) | One of 7 valid teams (including `"None"`) |
| `needs_escalation` | boolean | **Yes** (10%) | `true` or `false` |
| `missing_information` | string[] | **Yes** (15%) | From the 16-value constrained vocabulary |
| `next_best_action` | string | No* | Required but not deterministically scored |
| `remediation_steps` | string[] | No* | Required but not deterministically scored |

*Remediation quality is assessed as part of engineering quality (Part 2).

See [schemas/output.json](schemas/output.json) for the formal JSON Schema with all valid enum values.

## What to Expect

The tickets include:

- **Clean tickets** — well-written, clear, all the details you need
- **Vague tickets** — "system is down" with zero specifics
- **Multi-issue tickets** — "can't login AND my monitor is flickering" (good luck picking one category)
- **Hidden urgency** — no "URGENT" flag, but the body describes a production outage
- **Missing info** — half the context you need isn't there
- **Contradictions** — subject says "low priority", body says revenue is impacted
- **Noise** — auto-replies, "thanks" messages, out-of-office, spam (these are "Not a Support Ticket", routed to "None")
- **Jargon** — dense technical language that requires actually understanding IT support
- **Ambiguous routing** — is an MFA issue Identity or Security? Depends on the context. (Sound familiar? Read the routing guide.)

This is what real enterprise tickets look like. Your system needs to handle all of it.

## Dataset Splits

| Set | Tickets | Gold answers? | Purpose |
|---|---|---|---|
| **Sample** | 25 | Yes | Primary development loop — score locally |
| **Public eval** | 50 | No | Pre-submission validation — checks for errors and timeouts |
| **Hidden eval** | 100+ | No (held back) | Final scoring — includes edge cases not in public data |

> **Don't overfit.** The hidden set has ticket types you won't find in the public data. Build for robustness, not memorization.
