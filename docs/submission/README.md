# 🛰️ Submission — Final Transmission Protocol

> *"You've built the system. You've tested it against the scoring computer's cold judgment. Now it's time to launch. This is the part where most operators either feel confident or start making peace with their leaderboard ranking. Either way — transmission window is open."*
> — Chief Signal Officer Mehta, pre-launch briefing, 0600 station time

## How to Submit

1. **Fork** this repo (your fork must be **public** — we can't score what we can't see, and stealth mode is not a submission strategy)
2. **Build** your solution (the fun part — or the stressful part, depending on how many protein cubes you've consumed)
3. **Deploy** it somewhere callable via HTTPS (not localhost — localhost is 0.3 AU away and the scoring computer cannot reach it, no matter how aggressively it pings)
4. **Test** with the eval harness: sample set for scoring, public eval for smoke testing (if you skip this step, the scoring computer will test it for you, and it will not be gentle)
5. **Write** your three docs: `docs/architecture.md`, `docs/methodology.md`, `docs/evals.md` (Commander Kapoor reads all three — she reads fast and remembers everything)
6. **Create** `submission.json` at the root (see below)
7. **Push** everything (the moment of commitment — like stepping through an airlock, except reversible)
8. **Submit** at **[aka.ms/fde/hackathon](https://aka.ms/fde/hackathon)** (the platform where you register your endpoint and trigger the scoring run — this is the airlock you can't un-step-through)

## Required Files

Your repo should look like this. Think of it as the mission kit — if any component is missing, the mission proceeds with reduced confidence and the Admiral starts asking questions:

```
your-repo/
├── submission.json          # Mission telemetry beacon (your endpoint coordinates)
├── README.md                # Crew orientation guide (install, run, test)
├── docs/
│   ├── architecture.md      # Station blueprint (system design, AI pipeline, tradeoffs)
│   ├── methodology.md       # Captain's log (approach, iteration, what worked, what didn't)
│   └── evals.md             # After-action report (scores, error analysis, honest limitations)
└── ...                      # Your code, tests, infrastructure, hopes, dreams
```

**All three docs are mandatory.** Missing one is like deploying without a hull inspection — technically possible, definitely noticeable, career-limiting. Commander Kapoor reads all three docs. She reads them the way an astronomer reads a supernova — thoroughly, and with an opinion.

Important nuance: the hidden signals are for the **0-100 functional score**. Engineering review happens separately from what is in your repo after you submit. The scoring computer judges your outputs. The engineering review judges your soul. Professionally speaking.

What we want to see is not just that you got a decent score. We want to see how you built a system: clear design, sensible model usage, attention to latency and cost, tests that cover real failure modes, and engineering choices that would hold up in front of a station ops team. The kind of engineering that keeps 2,000 crew members breathing.

## submission.json

Drop this at the root of your repo. Think of it as your mission beacon — it tells the scoring platform where to find you in the void:

```json
{
  "participant": "your-name",
  "endpoint_url": "https://your-deployed-endpoint.example.com",
  "repository_url": "https://github.com/your-username/your-repo",
  "timestamp": "2026-03-23T00:00:00Z"
}
```

If `endpoint_url` doesn't respond, the scoring computer will note this fact with the emotional warmth of a neutron star. Which is to say: none.

## What Gets Evaluated

| Component | Weight | How it's scored |
|---|---|---|
| **Classification accuracy** | Up to 85 pts | 5 dimensions via macro F1, ordinal credit, set F1, binary F1 |
| **Efficiency** | Up to 15 pts | Latency (p50) + cost ($/signal) from response headers |
| **Engineering review** | Separate review | Repo review of system design, code quality, tests, docs, evals, infrastructure, and production readiness |

Full scoring details: [challenge README](../challenge/README.md#how-we-score-you)

## Required Documents

See [challenge README: Engineering Review](../challenge/README.md#engineering-review) for what goes in each one.

| Document | What we want to see |
|---|---|
| `docs/architecture.md` | System design, data flow, AI pipeline, tradeoffs, what you'd change for prod |
| `docs/methodology.md` | How you approached it, what you tried, what failed, how you spent your time |
| `docs/evals.md` | Your actual numbers, which signals you got wrong and why, where your system breaks |

> **Seriously:** a clean, simple solution with honest error analysis beats a complex system with no explanation. Every single time. Like Titan Outpost learned, complexity without clarity ends badly.

## Before You Submit

Pre-launch checklist. Skip any of these and the scoring run will teach you why we have checklists. In space, checklists are the difference between "successful mission" and "cautionary tale discussed at the Academy for decades."

- [ ] `GET /health` returns HTTP 200 (life signs detected — the station breathes)
- [ ] `POST /triage` returns valid JSON matching the [output schema](../data/schemas/output.json) (not a stack trace, not HTML, not your hopes and dreams in plain text)
- [ ] All 8 response fields are present: `ticket_id`, `category`, `priority`, `assigned_team`, `needs_escalation`, `missing_information`, `next_best_action`, `remediation_steps` (yes, all eight — the schema is not a suggestion)
- [ ] `category` values are from the 8 valid categories (creative synonyms score zero — the scoring computer has no imagination, like the void)
- [ ] `assigned_team` values are from the 7 valid teams (including `"None"` — for when the signal is cosmic noise, not a crisis)
- [ ] `missing_information` values are from the 16-value constrained vocabulary (exact strings only — `anomaly_read` is not `anomaly_readout` and the scoring computer will not squint)
- [ ] Your API handles **10 concurrent requests** without errors or timeouts (space doesn't queue signals politely)
- [ ] Each request responds in **under 30 seconds** (that's the timeout — aim for well under, because 30 seconds is an eternity when the hull is compromised and a blink when the scoring computer is judging you)
- [ ] Eval harness runs against 25 sample signals with gold scoring (your primary dev loop — run it until the numbers stop making you wince)
- [ ] Eval harness runs against 100 public eval signals without errors or timeouts (the smoke test — if it crashes here, it'll crash harder on the hidden set)
- [ ] `submission.json` at repo root with correct endpoint URL (not localhost — the scoring computer cannot reach your machine, it's in the cloud, you're at 0.3 AU)
- [ ] `docs/architecture.md` exists and is substantive (more than a paragraph — Commander Kapoor can tell when you wrote it at 2 AM in a panic)
- [ ] `docs/methodology.md` exists and is substantive (tell us the story — the good parts, the bad parts, the "why did I think that would work" parts)
- [ ] `docs/evals.md` exists and includes actual numbers from the sample set (real scores, real analysis — not "the system performed well" with no evidence)
- [ ] Your repo is **public** on GitHub (private repos are like encrypted distress signals — technically a signal, functionally useless)
- [ ] Your README explains how to install, run, and test your solution locally (someone should be able to clone it and have it running before their protein cube gets cold)
- [ ] You've submitted at **[aka.ms/fde/hackathon](https://aka.ms/fde/hackathon)** (the final step — the airlock opens, the void awaits)

## Tips

> *"These are the things I wish someone had told me before my first mission ops deployment. Actually, someone did tell me. I didn't listen. That's why I'm writing this."* — Chief Signal Officer Mehta

- **Deploy early.** Get something live in hour 2 and iterate. The number of people who deploy at hour 23 and then panic is... nonzero. Much like hull breach drills, the best time to prepare is before the emergency. The second-best time is not hour 23.
- **Run the eval harness constantly.** It's the same scoring logic as the platform. Trust the numbers. They're colder and more honest than Commander Kapoor's memos, and that's saying something.
- **Read the mission briefing.** Candidates who skip it produce noticeably worse output — they route hull breaches to Mission Software Operations and wonder why their score looks like a distress signal. The operational context matters. Commander Kapoor *will* notice. She notices everything. It's a space station. There's nowhere to hide.
- **Handle the anomalous signals.** The hidden eval has stuff you haven't seen: vague signals filed by crew who communicate exclusively in panic, multi-anomaly signals where three things broke and the reporter describes a fourth unrelated thing, deep space background noise that the comm array mistook for a distress call. If your system 500s on a garbled transmission, that's a zero on every dimension. The void is creative in its chaos, and so is the hidden dataset.
- **Return valid JSON even when confused.** A reasonable default beats a stack trace. A stack trace in response to a hull breach report is not just a bad score — it's a narrative tragedy. The void does not accept exceptions. Neither does the scoring computer.
- **Explain your decisions.** "I chose X because Y" is worth more than a polished README that says nothing. We want to see how you think, not how well you generate filler text. Filler text is the software equivalent of dispensing vanilla protein cubes when someone ordered chocolate — technically a response, functionally useless.
- **Send the cost headers.** It's only 5% of the score, but it signals you actually read the spec. Like checking your oxygen levels — small effort, big consequence if you skip it. The scoring computer will assume worst-case cost if you don't send headers, which is like the scoring computer assuming you heated the station by venting plasma directly into the hull — technically possible, wildly expensive.
- **Treat the repo like part of the mission.** The endpoint drives your functional score. The repo is what reviewers use to judge the engineering. Both matter. Like hull integrity and life support — you need both to survive. A fast endpoint with spaghetti code is a ticking time bomb. A beautiful repo with a broken endpoint is a monument to unrealized potential.
- **Show engineering judgment.** Good submissions usually have explicit timeouts, validation, useful tests, clean config, and a believable story for scale, security, and operability. The kind of engineering that keeps 2,000 crew alive at 0.3 AU from Earth — not because the code is clever, but because it's reliable.
- **Be honest about what you got wrong.** We respect a submission that says "I got these 5 signals wrong because my system can't distinguish comms hardware from comms software failures" more than one that says "results were satisfactory" with a 42% misroute rate. Self-awareness is the most underrated engineering skill. Just ask the Titan Outpost. Actually, you can't ask them. That's the point.
