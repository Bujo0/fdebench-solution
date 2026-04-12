# Dataset

🛰️ Synthetic signals modeled on real deep-space mission control operations. They're messy on purpose — because in space, signals arrive garbled, contradictory, panicked, and occasionally from someone who just wants to know where the mess hall is.

## Structure

```
data/
├── README.md                  # This file (you are here, operator)
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
| `subject` | string | Short summary. May be vague, misleading, or written during an explosion. |
| `description` | string | Full signal body. Quality varies wildly — from detailed engineering reports to panicked one-liners. |
| `reporter` | object | `{ name, email, department }` |
| `created_at` | datetime | ISO 8601 timestamp |
| `channel` | enum | `subspace_relay`, `holodeck_comm`, `bridge_terminal`, or `emergency_beacon` |
| `attachments` | string[] | Filenames mentioned (not actual files — we're 0.3 AU from the nearest file server) |

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

*Remediation quality is assessed during the separate engineering review. A system that says "investigate the anomaly" for every signal is telling us you phoned it in from 1 AU away.

See [schemas/output.json](schemas/output.json) for the formal JSON Schema with all valid enum values.

## What to Expect

The signals include:

- **Clean signals**: well-written, clear, all the details you need — the rare, beautiful ones
- **Vague signals**: "systems are failing" with zero specifics — helpful as a blank viewport
- **Multi-issue signals**: "can't access airlock AND my viewport is flickering" (good luck picking one category)
- **Hidden urgency**: no "RED ALERT" flag, but the body describes a hull breach — the quiet ones that kill
- **Missing info**: half the context you need isn't there — welcome to every deep-space comms channel ever
- **Contradictions**: subject says "routine", body says hull integrity is compromised — crew members are *terrible* at summaries
- **Noise**: beacon echoes, "acknowledged" messages, automated responses, space interference (these are "Not a Mission Signal", routed to "None" — the void is chatty)
- **Jargon**: dense technical language that requires actually understanding spacecraft operations
- **Ambiguous routing**: is a biometric failure Crew Identity or Threat Response? Depends on the context. (Sound familiar? Read the routing protocol.)
- **Adversarial signals**: attempts to manipulate your triage with logical arguments, social engineering, and existential dread

This is what real mission control signals look like. Your system needs to handle all of it, or the crew handles it for you — by submitting a signal about *your* system failing.

## Dataset Splits

| Set | Signals | Gold answers? | Purpose |
|---|---|---|---|
| **Sample** | 25 | Yes | Primary development loop, score locally |
| **Public eval** | 100 | No | Pre-submission validation, checks for errors and timeouts |
| **Hidden eval** | 1000+ | No (held back) | Final scoring, includes edge cases not in public data |

> **Don't overfit.** The hidden set has signal types you won't find in the public data. Build for robustness, not memorization. A system that memorized 25 signals and panics at the 26th is not a system — it's a liability. And in space, liabilities have a way of becoming hull decorations.
