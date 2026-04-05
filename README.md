# Be a Microsoft FDE for a Day

## What Is This

A **build challenge** where you tackle the kind of problem FDEs actually solve: a financial services company is drowning in IT support tickets, and they need an AI-powered triage API. Yesterday.

You'll read their (messy, incomplete) customer brief, dig through their ticket data, build a real deployed API, and ship it. Then we score it against a hidden evaluation set you've never seen.

**This is not a chatbot challenge.** It's an engineering challenge. One endpoint, one JSON in, one JSON out, deployed and callable. The kind of thing you'd actually build for a customer.

## Getting Started

1. **Read the customer brief** → [docs/challenge/customer_brief.md](docs/challenge/customer_brief.md). Understand the business problem before you write code
2. **Review the routing guide** → [docs/challenge/routing_guide.md](docs/challenge/routing_guide.md). Their internal (incomplete) routing rules
3. **Read the challenge spec** → [docs/challenge/](docs/challenge/). API contract, schemas, scoring rubric
4. **Explore the data** → [docs/data/](docs/data/). Synthetic tickets for development and testing
5. **Test locally** → [docs/eval/](docs/eval/). Run the eval harness against your endpoint
6. **Submit** → deploy, push, then go to **[aka.ms/fde/hackathon](https://aka.ms/fde/hackathon)** to submit

## Repository Structure

```
├── docs/
│   ├── challenge/       # Problem statement, customer brief, rules, scoring
│   ├── data/            # Synthetic ticket dataset + schemas
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

- **One submission** per person. Make it count.
- Any language, any framework, any AI model. Your call.
- Copilot, Cursor, Claude: all fair game. Use everything you've got.
- Must be deployed and callable via HTTPS. Not "it works on my machine".
- Documentation is required. If you can't explain it, you didn't build it.

## Evaluation

Your hidden-set **functional score** is **0–100**.

Functional scoring is deterministic: **macro F1** for classification and routing, **partial credit** for priority, **set F1** for missing info, **binary F1** for escalation. Plus latency and cost. No LLM judges. No vibes. Just math. See [docs/challenge/](docs/challenge/) for every detail.

Separately, we review repos for engineering quality: clean design, sensible tradeoffs, attention to latency and cost, real tests, and a system another engineer could trust.

Final rankings use a **hidden evaluation set** with edge cases you haven't seen. Don't overfit to the public data. Build it like it's going to production tomorrow.


## Before You Submit

Your solution must:

- Be **deployed** and callable via HTTPS
- Pass `GET /health` with HTTP 200
- Accept `POST /triage` with the documented JSON schema
- Include `submission.json` with your endpoint URL and repo link
- Include three mandatory docs: `docs/architecture.md`, `docs/methodology.md`, `docs/evals.md`
- Have a clean, well-tested, well-documented **public repository**

See [docs/submission/](docs/submission/) for the full checklist, then submit at **[aka.ms/fde/hackathon](https://aka.ms/fde/hackathon)**.

## License

[MIT](LICENSE)
