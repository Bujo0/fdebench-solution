# Dataset

> *"Every signal in this dataset was forged in the fires of real deep-space station chaos, distilled through the tears of ops officers, and seasoned with the kind of ambiguity that makes you question whether the reporter is describing a system failure or having an existential crisis. Probably both."*
> — Unnamed data engineer, 0300 station time, third protein cube

Synthetic signals modeled on real deep-space station operations. They're messy on purpose. Like the real thing, except nobody dies when you get one wrong. Probably. We make no guarantees about the emotional damage to your leaderboard ranking.

## Structure

```
data/
├── README.md                  # This file (you are here, operator — don't panic)
├── signals/
│   ├── sample.json            # 25 signals for local development (your training ground)
│   ├── sample_gold.json       # Gold-standard triage outputs (the answers you wish you had for the hidden set)
│   └── public_eval.json       # 100 signals for pre-submission testing (no gold — you're on your own, like the crew)
└── schemas/
    ├── input.json             # JSON Schema for signal input (what the station sends you)
    └── output.json            # JSON Schema for expected triage output (what you send back, if you want to keep your score)
```

## Signal Format (Input)

Each signal has these fields:

| Field | Type | Description |
|---|---|---|
| `ticket_id` | string | Unique ID (e.g., `SIG-4829`) |
| `subject` | string | Short summary. May be vague or misleading. |
| `description` | string | Full signal transmission body. Quality varies wildly. |
| `reporter` | object | `{ name, email, department }` |
| `created_at` | datetime | ISO 8601 timestamp |
| `channel` | enum | `subspace_relay`, `holodeck_comm`, `bridge_terminal`, or `emergency_beacon` |
| `attachments` | string[] | Filenames mentioned (not actual files) |

Subspace relay transmissions tend to be longer and more detailed — these are from crew who had time to think, which is both a blessing and a curse (some of them overthink). Holodeck comm signals are short, missing context, and occasionally filed while the reporter is upside down in zero-g. Emergency beacon transcriptions are messy, panicked, and sometimes just someone breathing heavily into the comm for thirty seconds before a cryo-sleep auto-reply kicks in. Bridge terminal entries are somewhere in between — form fields are treated as creative suggestions by most crew members.

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

*Remediation quality is assessed during the separate engineering review. A system that says "investigate the anomaly" for every signal is telling us you phoned it in from 1 AU away while sipping something with an umbrella in it. We've seen this. It does not end well for the leaderboard ranking or the hypothetical crew depending on your remediation advice. Write remediation steps like someone's career — or oxygen supply — depends on them. Because in this scenario, it does.

See [schemas/output.json](schemas/output.json) for the formal JSON Schema with all valid enum values.

## What to Expect

The signals include everything you'd see scroll across the Mission Ops terminal at 0300 during a solar flare when half the crew can't sleep and the other half shouldn't be awake:

- **Clean signals**: well-written, clear, all the details you need
- **Vague signals**: "systems are failing" with zero specifics (which systems? all of them? some of them? the nutrient synthesizer?)
- **Multi-issue signals**: "airlock code broken AND holodisplay flickering AND also the gravity feels weird" (good luck picking one category)
- **Hidden urgency**: no "CRITICAL" flag, but the body describes a hull breach
- **Missing info**: half the context you need isn't there
- **Contradictions**: subject says "low priority," body says oxygen levels are dropping. These are the ones that keep ops officers up at night — which, in space, is indistinguishable from the day
- **Noise**: automated beacon echoes, "thanks" messages, cryo-sleep auto-replies ("I am currently frozen. Please try again in 6–18 months."), and deep space background noise that the comm array occasionally mistakes for a distress signal. These are "Not a Mission Signal," routed to "None"
- **Jargon**: dense technical space-station terminology that requires actually understanding station operations (no, you cannot search "BioScan ID connector timeout" from 0.3 AU away)
- **Ambiguous routing**: is a biometric scanner issue Crew Identity or Threat Response? Depends on the context. (Sound familiar? Read the routing guide.)

This is what real space station signals look like. Your system needs to handle all of it. Gracefully. Without panicking. Unlike some of the reporters.

## Dataset Splits

| Set | Signals | Gold answers? | Purpose |
|---|---|---|---|
| **Sample** | 25 | Yes | Primary development loop, score locally |
| **Public eval** | 100 | No | Pre-submission validation, checks for errors and timeouts |
| **Hidden eval** | 1000+ | No (held back) | Final scoring, includes edge cases not in public data |

Gold answers include a `difficulty` field (`"standard"` or `"adversarial"`) so you can analyze how your system performs on routine station ops vs. the tricky signals — the vague, contradictory, multi-issue chaos that space throws at you when you're least prepared and most caffeinated. The hidden eval set is partitioned roughly 70/30 standard/adversarial. If your system only handles the easy ones, the leaderboard will reflect that with brutal honesty. Much like space itself, the leaderboard has no feelings and no mercy.

> **Don't overfit.** The hidden set has signal types you won't find in the public data. Build for robustness, not memorization. The void doesn't repeat itself, and neither does the hidden eval. If your system only handles the 25 signals it's seen, it'll score like a crew member who studied for the wrong exam, showed up to the wrong deck, and then blamed the gravitational anomaly. The scoring computer will not care about the gravitational anomaly.
