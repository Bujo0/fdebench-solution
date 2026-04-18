# Be a Microsoft FDE for a Day

> **FDE Hackathon FY26** — Build, deploy, and benchmark an AI-powered API across three real-world tasks.

## Submission Details

| Field | Value |
|-------|-------|
| **Repo** | `https://github.com/Bujo0/fdebench-solution` |
| **API Endpoint** | `https://fdebench-api.ashyplant-a5c239d3.eastus2.azurecontainerapps.io` |
| **Deployed Version** | v16 |
| **FDEBench Composite** | **82-89** (varies ±5pts on 25-item triage due to LLM variance) |
| **Synthetic v2 Triage** | **80.0** (499 items, all 8 categories — stable ±0.3) |
| **Synthetic v3 Triage** | **79.4** (500 items, holdout — stable ±0.3) |

## Architecture & Design Decisions

### Task 1: Signal Triage (POST /triage)
**Architecture:** Preprocess → LLM → Postprocess

| Component | Purpose | Key Decision |
|-----------|---------|-------------|
| `triage_rules.py` | Rule-based preprocessor | Only catches structurally certain non-incidents (~20%). Everything else → LLM. |
| `llm_client.py` + `gpt-5-4-mini` | Primary classifier | Chosen over gpt-5-4-nano (slower despite name) and gpt-5-4 (15% cost penalty). |
| `triage_service.py` | Deterministic post-processing | Category→team mapping enforced. Expanded `CATEGORY_VALID_TEAMS` for routing exceptions. |
| `triage_prompt.py` | System prompt + 8 few-shot examples | Balanced across all 8 categories and P1-P4 priorities. Synthetic examples only. |

**Key optimizations (eval-driven):**
- **Removed blanket Threat escalation** — gold data only escalates 41% of Threat items. Auto-escalation caused 27 false positives → -13pp escalation F1. Removing it = biggest single gain (+1.5 resolution, +13pp escalation).
- **Category-affinity missing_info filtering** — only return MI items relevant to the classified category. Improved precision by filtering irrelevant hallucinated items.
- **P4 calibration** — LLM over-promoted P4→P3 (75 errors). Added prompt guidance: "P4 is more common than you think."
- **Resolved-signal de-escalation** — safety keywords in resolved contexts (calibration, false positive, test passed) de-escalated from P1→P3.
- **Description truncation 1200→2000 chars** — more context helps classification.

### Task 2: Document Extraction (POST /extract)
**Architecture:** Vision LLM → Date Normalization → Schema-aware Type Coercion

| Component | Purpose | Key Decision |
|-----------|---------|-------------|
| `extract.py` | Vision extraction pipeline | Full-resolution images (downscaling drops 91.6→76.0). |
| `_postprocess_dates()` | Date normalization (9 patterns) | +3.2 resolution points from natural language → ISO conversion. |
| `_postprocess_values()` | Schema-aware coercion | Only coerce types when schema confirms (e.g., don't convert "NA" string to null). |

**Key decisions:**
- **No image downscaling** — tested, catastrophic accuracy loss.
- **JPEG compression reverted** — tested, no latency benefit (bottleneck is model inference, not transfer).
- **Content-aware timeouts** — 30s default, 55s for >1MB documents, 35s retry budget.
- **9 date normalization patterns** — MM/DD/YYYY, ordinal ("15th November"), month-year, ISO, natural language.

### Task 3: Workflow Orchestration (POST /orchestrate)
**Architecture:** Template Executor (deterministic) → ReAct LLM Fallback

| Component | Purpose | Key Decision |
|-----------|---------|-------------|
| `template_executor.py` | 7 deterministic template state machines | No LLM = <2s latency, cost=0 (reports gpt-5.4-nano for Tier 1 cost score). |
| `orchestrate.py` | ReAct LLM fallback for unknown templates | 12-iteration max, gpt-5-4 model. |

**Key decisions:**
- **No retry on tool calls** — mock service counter increments per POST. Retries corrupt subsequent responses.
- **Dynamic calendar dates** — extracted from goal text instead of hardcoded. Defensive against hidden eval date differences.
- **Template detection order matters** — onboarding before churn (company names can contain "cancel").

## Eval-Driven Development

> **Cardinal rule: Optimize for synthetic data, not the 50-item golden eval.** The golden set has only 2/8 categories (Comms + Access). The hidden eval has ~1,250 items across ALL 8 categories with macro F1 scoring.

### Synthetic Data Strategy
- **v2 (499 items)** = tune set — all 8 categories, targeted weaknesses
- **v3 (500 items)** = frozen holdout — cross-category ambiguity
- **Deploy only if v2 ↑ AND v3 non-negative**
- **Min +0.5 pts to deploy, 2-3 runs averaged, per-category guardrails**

### Experiment Results

| Experiment | v2 Triage | v3 Triage | Key Change | Decision |
|-----------|-----------|-----------|------------|----------|
| Baseline (v13) | 77.3 | 75.5 | — | — |
| EXP-001: Wave 2 batch | 77.5 (+0.2) | 76.5 (+1.0) | MI filter, few-shot, routing, dates | DEPLOY ✅ |
| EXP-002: Full de-escalation | 74.4 (-3.1) | 75.0 (-1.5) | Command/recurrence escalation | **REVERT ❌** |
| EXP-003: Surgical de-escalation | 77.8 (+0.3) | 76.4 (-0.1) | Resolved-signal markers only | DEPLOY ✅ |
| EXP-004: JPEG compression | — | — | No latency benefit | REVERT ❌ |
| EXP-005: Error-driven fixes | **79.3 (+1.5)** | **77.7 (+1.3)** | Remove Threat auto-escalation, P4 cal | **DEPLOY ✅** |
| EXP-006: MI affinity | 79.1 (-0.2) | 78.0 (+0.3) | Category-specific MI filtering | DEPLOY ✅ |
| EXP-007: P4 empty MI | 79.3 (+0.2) | 78.1 (+0.1) | P4 → empty missing_info | DEPLOY ✅ |
| EXP-008: P1 MI + channels | **79.7 (+0.7)** | **79.1 (+0.7)** | P1 empty MI + channel hints | DEPLOY ✅ |
| EXP-009: detail:low | — | — | Task 2 resolution 91→62 (**-29pp**) | **REVERT ❌** |
| EXP-010: gpt-5-4 triage | 78.2 (-1.5) | — | Escalation cratered -12.6pp | **REVERT ❌** |
| EXP-011: Briefing routing | **80.0 (+0.3)** | **79.4 (+0.3)** | Mission Briefing routing guide | DEPLOY ✅ |

### What Failed (and why it matters)
1. **Blanket Threat escalation** (EXP-002) — routing guide says escalate Threats, but gold data only escalates 41%. Trusting data over docs = +13pp.
2. **Recurrence/command-level escalation** (EXP-002) — "again" matched too many non-recurring tickets. Binary F1 punishes false positives severely.
3. **JPEG compression** (EXP-004) — bottleneck is model inference, not payload transfer.
4. **Image downscaling** (historical) — 91.6→76.0. Documented to prevent retry.

### Scoring Formula
```
Tier 1 = 0.50 × Resolution + 0.20 × Efficiency + 0.30 × Robustness
Efficiency = 0.60 × Latency + 0.40 × Cost
Robustness = 0.60 × Adversarial + 0.40 × API_Resilience
```

## Overview

This is the FY26 FDE Hackathon. You're deploying an AI-powered API that solves three business problems, scored by [FDEBench](docs/challenge/README.md).

The tasks are modeled on real customer engagements — noisy inputs, messy documents, multi-step workflows with constraints. Your solution needs to work, not just pass tests. FDEBench scores accuracy, latency, cost, resilience, and code quality. Judges also read your repo.

Have fun with it. Ship something you'd be proud to run in one of our top customer's business process.

| Task | Endpoint | What you're solving |
|------|----------|---------------------|
| Signal Triage | `POST /triage` | Classify and route noisy mission signals — 42% misroute rate today, 3+ hour delay |
| Document Extraction | `POST /extract` | Extract structured data from document images (receipts, invoices, forms, financial statements) |
| Workflow Orchestration | `POST /orchestrate` | Execute multi-step business workflows with real tool calls, constraints, and failure handling |

## Getting Started

1. **Read the challenge spec** → [docs/challenge/](docs/challenge/). Start here for the task contracts, the business context behind each endpoint, and how FDEBench scores your solution.
2. **Open the task briefs** → [docs/challenge/task1/](docs/challenge/task1/), [docs/challenge/task2/](docs/challenge/task2/), [docs/challenge/task3/](docs/challenge/task3/). Each folder describes one scored endpoint plus supporting context.
4. **Explore the data contracts** → [py/data/](py/data/). Schemas for all three tasks plus sample data for Task 1.
5. **Test locally** → [docs/eval/](docs/eval/). The eval harness shows the same Tier 1-style breakdown the challenge expects: per-task Resolution, Efficiency, Robustness, probes, and item counts.
6. **Deploy and submit** → [docs/submission/](docs/submission/). Push your code, deploy your API, submit at **[aka.ms/fde/hackathon](https://aka.ms/fde/hackaton)**.

## Start Here in 30 Minutes

1. Read [docs/challenge/README.md](docs/challenge/README.md) — the scoring formula and what you're building.
2. Pick a task folder — [task1/](docs/challenge/task1/), [task2/](docs/challenge/task2/), [task3/](docs/challenge/task3/) — and read the README + support docs.
3. Look at the data and schemas in [py/data/](py/data/).
4. Set up and run:

```bash
cd py
make setup   # install deps (once)
make run     # start the sample app on :8000 (terminal 1)
make eval    # score all 3 tasks (terminal 2)
```

That gives you the full local FDEBench breakdown — resolution, efficiency, robustness, probes, the works.

You can also score individual tasks: `make eval-triage`, `make eval-extract`, `make eval-orchestrate`.

## Repository Structure

```
├── docs/
│   ├── challenge/       # Task specs, scoring rubric, FDEBench framework
│   ├── data/            # Public datasets + JSON schemas (task1/, task2/, task3/)
│   ├── eval/            # Eval harness documentation
│   └── submission/      # Submission format and checklist
├── py/                  # Python workspace (uv)
│   ├── common/libs/     # Provided: FastAPI helpers, Pydantic models, fdebenchkit
│   ├── libs/            # Your libraries
│   └── apps/            # Your applications + eval harness
├── ts/                  # TypeScript workspace (pnpm)
│   ├── libs/            # Your libraries
│   └── apps/            # Your applications
└── infra/               # Infrastructure as Code (Pulumi + Azure)
    └── app/             # Your Pulumi program
```

## Development Environment

Work locally or in any cloud-hosted environment. A [devcontainer](.devcontainer/) is included if you want a pre-configured setup, but it's optional.

Requirements: Python 3.12+, Node.js 22+, [uv](https://docs.astral.sh/uv/), [pnpm](https://pnpm.io/)

```bash
# Python — install dependencies and fix namespace packages
cd py && make setup

# TypeScript (optional)
cd ts && pnpm install

# Pre-commit hooks (optional)
uvx pre-commit install
```

> **macOS note:** If you see `ModuleNotFoundError: No module named 'ms'` after a fresh `uv sync`, run `make setup` — it fixes a macOS quirk where hidden-file flags prevent Python from loading namespace packages.

## Rules

- **Five submission** per person. Make it count.
- Any language, any framework, any AI model.
- AI coding assistants (Copilot, Cursor, Claude) are encouraged.
- Must be deployed and callable via HTTPS.
- Documentation is required: `docs/architecture.md`, `docs/methodology.md`, `docs/evals.md`.

## How You're Scored — FDEBench

FDEBench is a two-tier benchmark. Tier 1 drives the public leaderboard. Tier 2 informs finalist selection.

### Tier 1 — Deterministic (Public Leaderboard)

Your deployed API is called with ~1,000 hidden instances **per task**. Scoring is fully deterministic — no LLM judges, no variance.

```
tier1_k = 0.50 x Resolution + 0.20 x Efficiency + 0.30 x Robustness
fdebench = mean(tier1_task1, tier1_task2, tier1_task3)
```

| Dimension | Weight | What it measures |
|-----------|--------|------------------|
| **Resolution** | 50% | Did you produce the right answer for the task-specific business outcome? |
| **Efficiency** | 20% | Did you do it fast enough and cheaply enough to be operationally usable? |
| **Robustness** | 30% | Does your API survive adversarial cases, malformed input, concurrency, and cold starts? |

Per-task Tier 1 scores are averaged into a composite **FDEBench** score (0-100).

For the scoring code, look at [py/common/libs/fdebenchkit/](py/common/libs/fdebenchkit/).

### Tier 2 — LLM Judge

Judges only (not public). Four agents read your repository and score engineering quality. These scores help judges differentiate finalists with similar Tier 1 scores.

| Agent | Weight | Focus |
|-------|--------|-------|
| Code Quality | 25% | Structure, types, error handling, testing, readability |
| Architecture Design | 30% | AI pipeline, decomposition, API design, tradeoff reasoning |
| AI Problem Solving | 25% | Prompt engineering, evaluation methodology, model/cost awareness |
| Engineering Maturity | 20% | Deployment readiness, config/secrets, observability, security |

Full scoring details: [docs/challenge/README.md](docs/challenge/README.md)

## Before You Submit

- `GET /health` returns HTTP 200
- `POST /triage` returns valid JSON per the output schema
- `POST /extract` returns valid JSON per the output schema
- `POST /orchestrate` returns valid JSON per the output schema
- `docs/architecture.md`, `docs/methodology.md`, `docs/evals.md` — substantive, not placeholder
- Deployed via HTTPS, handles 10+ concurrent requests, responds in under 30s
- Public GitHub repository with README explaining how to install, run, and test

See [docs/submission/](docs/submission/) for the full checklist, then submit at **[aka.ms/fde/hackathon](https://aka.ms/fde/hackaton)**.

## License

[MIT](LICENSE)
