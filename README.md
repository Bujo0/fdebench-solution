# 🛰️ Be a Microsoft FDE for a Day

## What Is This

A **build challenge** where you tackle the kind of problem FDEs actually solve — except the stakes are higher, the coffee is worse, and the nearest help desk is 0.3 AU away. Contoso Deep Space Station is drowning in incoming mission signals, and they need an AI-powered signal triage API. Yesterday. Before the hull breach in Sector 7 finishes its slow-motion audition for "most expensive window installation in human history" and the atmospheric processor on Deck 7 completes whatever chemical experiment it's conducting on the air supply.

You'll read Commander Kapoor's (messy, incomplete, delightfully passive-aggressive) mission briefing, dig through their signal data — which ranges from "hull breach in progress" to "the nutrient synthesizer dispensed vanilla instead of chocolate and I require an explanation" — build a real deployed API, and ship it. Then we score it against a hidden evaluation set you've never seen. The scoring computer has all the empathy of a neutron star.

**This is not a chatbot challenge.** This is not a holographic dashboard. This is not an "AI-powered insights platform." It's an engineering challenge. One endpoint, one JSON in, one JSON out, deployed and callable. The kind of thing you'd actually build for a mission ops team that has 2,000 crew, zero patience, and an Admiral who reviews the fuel budget personally.

## Getting Started

1. **Read the mission briefing** → [docs/challenge/customer_brief.md](docs/challenge/customer_brief.md). Understand the mission before you write code. Commander Kapoor took the time to explain. The least you can do is read it. People's lives depend on it. Fictional people, but they feel increasingly real the longer you work on this.
2. **Review the routing protocol** → [docs/challenge/routing_guide.md](docs/challenge/routing_guide.md). Their internal (incomplete, occasionally contradictory, written 8 months ago by someone who has since been reassigned) signal routing rules
3. **Read the challenge spec** → [docs/challenge/](docs/challenge/). API contract, schemas, scoring rubric, and exactly how the scoring computer will judge you
4. **Explore the data** → [docs/data/](docs/data/). Synthetic signals for development and testing — including vague ones, contradictory ones, and one that's mostly just heavy breathing into the emergency beacon
5. **Test locally** → [docs/eval/](docs/eval/). Run the eval harness against your endpoint. Run it early. Run it often. The scoring computer never sleeps.
6. **Submit** → deploy, push, then go to **[aka.ms/fde/hackathon](https://aka.ms/fde/hackathon)** to submit. One shot. Make it count.

## Repository Structure

```
├── docs/
│   ├── challenge/       # Problem statement, mission briefing, rules, scoring
│   ├── data/            # Synthetic signal dataset + schemas
│   ├── eval/            # Public evaluation harness (run locally)
│   └── submission/      # How to submit your solution
├── py/                  # Python workspace (uv)
│   ├── common/libs/     # Provided common libraries (FastAPI, Pydantic models)
│   ├── libs/            # Your libraries
│   └── apps/            # Your applications
├── ts/                  # TypeScript workspace (pnpm)
│   ├── libs/            # Your libraries
│   └── apps/            # Your applications
└── infra/               # Infrastructure as Code (Pulumi + Azure)
    └── app/             # Your Pulumi program
```

## Development Environment

Work locally or in any cloud-hosted environment, your choice. A [devcontainer](.devcontainer/) is included if you want a pre-configured setup, but it's entirely optional.

Requirements: Python 3.12+, Node.js 22+, [uv](https://docs.astral.sh/uv/), [pnpm](https://pnpm.io/)

```bash
# Python
cd py && uv sync

# TypeScript
cd ts && pnpm install

# Pre-commit hooks
uvx pre-commit install
```

## Rules

- **One submission** per person. Make it count. Like a torpedo lock — you get one shot, and the Admiral is watching. No second chances. No "but I meant to deploy the other branch." No "the shuttle ate my homework."
- Any language, any framework, any AI model. Your call. The scoring computer does not discriminate.
- Copilot, Cursor, Claude: all fair game. Use everything you've got. The crew doesn't care how you built it — they care that it works when the alarms are blaring and Deck 7 smells like burning ozone.
- Must be deployed and callable via HTTPS. Not "it works on my machine." Your machine is 0.3 AU from the scoring platform, and Commander Kapoor has no patience for localhost.
- Documentation is required. If you can't explain it, you didn't build it. If you can't explain it under pressure while the Admiral asks pointed questions, you definitely didn't build it.

## Evaluation

Your hidden-set **functional score** is **0–100**.

Functional scoring is deterministic: **macro F1** for classification and routing, **partial credit** for priority, **set F1** for missing info, **binary F1** for escalation. Plus latency and cost. No LLM judges. No vibes. No mercy. Just math — as cold and unforgiving as the vacuum outside the viewport. The scoring computer has rendered its verdict on better systems than yours. See [docs/challenge/](docs/challenge/) for every detail you need and several you didn't know you needed.

Separately, we review repos for engineering quality: clean design, sensible tradeoffs, attention to latency and cost, real tests, and a system another engineer could trust at 0300 during a solar flare while the Admiral is making pointed remarks about "that AI system I was told would fix everything."

Final rankings use a **hidden evaluation set** with edge cases you haven't seen — including signals that are 90% panic and 10% consonants. Don't overfit to the public data. Build it like Commander Kapoor is going to plug it into the station ops workflow tomorrow — because in this scenario, she is. And she will find you if it routes a hull breach to Mission Software Operations. Metaphorically. Across 0.3 AU. She's patient.


## Before You Submit

Your solution must:

- Be **deployed** and callable via HTTPS — not localhost, not your quarters terminal, not a Raspberry Pi duct-taped to the hull with hope and zip ties
- Pass `GET /health` with HTTP 200 — if it doesn't, scoring fails immediately and the void claims another victim
- Accept `POST /triage` with the documented JSON schema — all 8 response fields, all valid enum values, no creative interpretations
- Handle **10 concurrent requests** without errors or timeouts — the scoring platform is not gentle, and the crew doesn't file signals one at a time
- Include `submission.json` with your endpoint URL and repo link
- Include three mandatory docs: `docs/architecture.md`, `docs/methodology.md`, `docs/evals.md` — missing one is a big hit in engineering review, like showing up to a mission briefing without your flight plan
- Have a clean, well-tested, well-documented **public repository** — treat it like part of the product, because it is

See [docs/submission/](docs/submission/) for the full checklist, then submit at **[aka.ms/fde/hackathon](https://aka.ms/fde/hackathon)**. The crew is counting on you. Don't let them down. The cats on Deck 9 are watching too, but they've never been particularly helpful.

## License

[MIT](LICENSE)
