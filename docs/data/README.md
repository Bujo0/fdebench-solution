# Dataset

Synthetic signals modeled on real deep-space mission control operations. They're messy on purpose.

## Structure

```
data/
├── README.md                  # This file
├── tickets/
│   ├── sample.json            # 25 signals for local development
│   ├── sample_gold.json       # Gold-standard triage outputs for the sample set
│   └── public_eval.json       # 100 signals for pre-submission testing
└── schemas/
    ├── input.json             # JSON Schema for signal input
    └── output.json            # JSON Schema for expected triage output
```

## Signal Format (Input)

Each signal has these fields:

| Field | Type | Description |
|---|---|---|
| `ticket_id` | string | Unique ID (e.g., `SIG-4829`) |
| `subject` | string | Short summary. May be vague or misleading. |
| `description` | string | Full signal body. Quality varies wildly. |
| `reporter` | object | `{ name, email, department }` |
| `created_at` | datetime | ISO 8601 timestamp |
| `channel` | enum | `subspace_relay`, `holodeck_comm`, `bridge_terminal`, or `emergency_beacon` |
| `attachments` | string[] | Filenames mentioned (not actual files) |

See [schemas/input.json](schemas/input.json) for the formal JSON Schema.

## Triage Output Format

Your `/triage` endpoint must return **all 8 fields**:

| Field | Type | Scored? | Notes |
|---|---|---|---|
| `ticket_id` | string | — | Must match the input exactly |
| `category` | string | **Yes** (20%) | One of 8 valid anomaly categories |
| `priority` | string | **Yes** (20%) | `P1`, `P2`, `P3`, or `P4` |
| `assigned_team` | string | **Yes** (20%) | One of 7 valid response divisions (including `"None"`) |
| `needs_escalation` | boolean | **Yes** (10%) | `true` or `false` |
| `missing_information` | string[] | **Yes** (15%) | From the 16-value constrained vocabulary |
| `next_best_action` | string | No* | Required but not deterministically scored |
| `remediation_steps` | string[] | No* | Required but not deterministically scored |

*Remediation quality is assessed during the separate engineering review.

See [schemas/output.json](schemas/output.json) for the formal JSON Schema with all valid enum values.

## What to Expect

The signals include:

- **Clean signals**: well-written, clear, all the details you need
- **Vague signals**: "systems are failing" with zero specifics
- **Multi-issue signals**: "can't access airlock AND my viewport is flickering" (good luck picking one category)
- **Hidden urgency**: no "RED ALERT" flag, but the body describes a hull breach
- **Missing info**: half the context you need isn't there
- **Contradictions**: subject says "routine", body says hull integrity is compromised
- **Noise**: beacon echoes, "acknowledged" messages, automated responses, space interference (these are "Not a Mission Signal", routed to "None")
- **Jargon**: dense technical language that requires actually understanding spacecraft operations
- **Ambiguous routing**: is a biometric failure Crew Identity or Threat Response? Depends on the context. (Sound familiar? Read the routing protocol.)

This is what real mission control signals look like. Your system needs to handle all of it.

## Dataset Splits

| Set | Signals | Gold answers? | Purpose |
|---|---|---|---|
| **Sample** | 25 | Yes | Primary development loop, score locally |
| **Public eval** | 100 | No | Pre-submission validation, checks for errors and timeouts |
| **Hidden eval** | 1000+ | No (held back) | Final scoring, includes edge cases not in public data |

> **Don't overfit.** The hidden set has signal types you won't find in the public data. Build for robustness, not memorization.
