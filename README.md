# Be a Microsoft FDE for a Day

> **Build like an FDE. Bring your best.**

## What Is This

A **24-hour build challenge** where you solve a real enterprise problem: build an AI-powered ticket triage API for a fictional financial services company drowning in IT support requests.

You'll read their customer brief, explore their messy ticket data, build a deployed API that classifies, routes, and generates remediation — and submit it for automated scoring against a hidden evaluation set.

**This is not a chatbot challenge.** It's an engineering challenge. One endpoint, one JSON in, one JSON out, deployed and live.

## Getting Started

1. **Read the customer brief** — [docs/challenge/customer_brief.md](docs/challenge/customer_brief.md) — understand the business problem before you write code
2. **Review the routing guide** — [docs/challenge/routing_guide.md](docs/challenge/routing_guide.md) — their internal (incomplete) routing rules
3. **Read the challenge spec** — [docs/challenge/](docs/challenge/) — API contract, schemas, scoring rubric
4. **Explore the data** — [docs/data/](docs/data/) — synthetic tickets for development and testing
5. **Test locally** — [docs/eval/](docs/eval/) — run the eval harness against your endpoint
6. **Submit** — [docs/submission/](docs/submission/) — deploy, push, submit

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

Work locally or in any cloud-hosted environment — your choice. A [devcontainer](.devcontainer/) is included if you want a pre-configured setup, but it's entirely optional.

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

- **24-hour build window** from the published start time
- **One final submission** per participant
- You may use any programming language, framework, or AI model
- AI coding assistants are allowed
- Your solution must be deployable and callable via API
- Documentation is required

## Evaluation

Submissions are scored on a **100-point scale**: **50%** functional accuracy (does your triage match the gold standard?) and **50%** engineering quality (design, code, docs, evals, production readiness).

Functional scoring uses exact match for classification/routing, F1 for missing-info detection, and **LLM-as-judge** for remediation quality. See [docs/challenge/](docs/challenge/) for the full rubric.

Final rankings use a **hidden evaluation set** with additional edge cases. Don't overfit to the public data. Build your solution as if it's going to production tomorrow — use what you consider best practices and explain why. We are looking for engineering. 


## Before You Submit

Your solution must:

- Be **deployed** and callable via HTTPS
- Pass `GET /health` with HTTP 200
- Accept `POST /triage` with the documented JSON schema
- Include `submission.json` with your endpoint URL and repo link
- Include three mandatory docs: `docs/architecture.md`, `docs/methodology.md`, `docs/evals.md`
- Have a clean, well-tested, well-documented **public repository**

See [docs/submission/](docs/submission/) for the full checklist.

## License

[MIT](LICENSE)
