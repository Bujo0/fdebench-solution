# Dataset

This directory contains the synthetic ticket data for the challenge.

## Structure

```
data/
├── README.md                # This file
├── tickets/
│   ├── sample.json          # ~10 tickets for local development
│   ├── sample_gold.json     # Gold-standard triage outputs for the sample set
│   └── public_eval.json     # ~50 tickets for self-evaluation
└── schemas/
    ├── input.json           # JSON Schema for ticket input
    └── output.json          # JSON Schema for triage output
```

## Ticket Format

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

## What to Expect

The tickets are synthetic but modeled after real enterprise IT support data. They include:

- **Clean tickets** — well-written with clear descriptions and relevant details
- **Vague tickets** — "system is down" with no specifics
- **Multi-issue tickets** — "can't login AND my monitor is flickering"
- **Urgency hidden in context** — no "URGENT" flag but the body implies time sensitivity
- **Missing information** — common fields omitted, context insufficient
- **Contradictions** — subject says "low priority" but body describes a production outage
- **Noise** — auto-replies, "thanks" messages, out-of-office, spam
- **Domain jargon** — dense technical language that requires real understanding
- **Multiple valid approaches** — some tickets have more than one reasonable classification

This reflects reality. Real enterprise tickets are messy. Your system should handle all of these gracefully.

## Dataset Splits

| Set | Tickets | Visibility | Purpose |
|---|---|---|---|
| **Sample** | ~10 | Public (in this repo) | Local development |
| **Public eval** | ~50 | Public (in this repo) | Self-testing with the eval harness |
| **Hidden eval** | ~100 | Private (not in this repo) | Final scoring — includes additional edge cases |

> **Do not overfit to the public evaluation set.** Final rankings are determined by the hidden set, which includes scenarios not present in the public data.
