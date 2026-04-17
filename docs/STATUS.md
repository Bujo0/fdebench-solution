# FDEBench Solution — Handoff & Next Steps

> Last updated: 2026-04-17T22:50Z
> Current composite: **86.4** (v13 deployed)
> Realistic hidden-eval estimate: **82-89**

---

## ⚠️ THE MOST IMPORTANT LESSON: DON'T OPTIMIZE FOR THE GOLDEN DATA

**The golden data (public eval sets) are NOT representative of the hidden eval.**

We learned this the hard way:
- The 50-item triage public eval has **only 2 of 8 categories** (Communications & Navigation + Crew Access & Biometrics)
- We built a keyword rules engine that scored **93.6** on this set — near-perfect
- When tested on 1,349 diverse synthetic items, it scored **60.2** — a 33-point gap
- We had to **tear down the entire rules engine** and rebuild with an LLM-primary approach

**The hidden eval has ~1,000 triage items across ALL 8 categories, ~500 extraction documents, and ~500 orchestration workflows.** The scoring uses **macro F1** for Task 1, meaning rare categories are weighted equally. If you over-optimize for the golden data distribution, you WILL score poorly on the hidden eval.

### What to do instead:
1. **Use synthetic data as your primary optimization target** — we have 1,349 triage items, 130 orchestrate scenarios
2. **Use the golden data only for sanity checks** — "does my endpoint return valid JSON?"
3. **Generate MORE synthetic data** targeting your weakest dimensions
4. **Cross-validate** — always measure on at least 2 different datasets before claiming improvement
5. **Monitor the generalization gap** — if golden score >> synthetic score, you're overfitting

---

## 🔍 Where to Find Context

| What you need | Where to look |
|--------------|--------------|
| **How the scorer ACTUALLY works** | `py/common/libs/fdebenchkit/src/ms/common/fdebenchkit/weights.py` (weights), `runner.py` (cost tiers, latency), `scorers/*.py` (per-task algorithms) |
| **What we've tried and what failed** | `docs/hill-climbing-analysis.md` — full 40+ experiment history |
| **Current architecture & design decisions** | `docs/architecture.md` (538 lines) |
| **Challenge spec & task contracts** | `docs/challenge/README.md`, `docs/challenge/task{1,2,3}/README.md` |
| **How to run/deploy/test** | `RUNBOOK.md` at repo root |
| **Our solution code** | `py/apps/sample/` — modular: `routers/`, `services/`, `prompts/` |
| **Synthetic test data** | `py/apps/sample/synthetic/` — 1,349+ triage items, 130 orchestrate |
| **Scoring formula** | Section 14 of this doc, or `weights.py` directly |
| **Azure infrastructure** | Section below — all resource names, endpoints, credentials |
| **FDE coding patterns** | `fde-moj/`, `fde-core/`, `fde-apollo/` repos on this machine |

---

## 🎯 Highest-Impact Next Steps (Do These First)

### 1. Hill-Climb Task 1 Missing Info (+1.6 composite potential)

**Current**: 0.273 | **Target**: 0.55+ | **Why it matters**: 17% of resolution weight

Missing info is scored with set F1. **11 of 25 gold items have EMPTY missing info** — if the LLM returns empty for those, we get 1.0 each. But the LLM hallucinates items on those empty tickets, scoring 0.

**What to try**:
- Post-process missing info: remove low-confidence items unless clearly needed
- Further tune the prompt to emphasize "default is empty []"
- Test against v2 synthetic (499 items) and v3 synthetic (500 items) — both have gold labels
- **Key insight from analysis**: only `module_specs` (8/25) and `anomaly_readout` (5/25) are common enough to be worth predicting. Everything else should be suppressed.

### 2. Improve Task 1 Adversarial Accuracy (+1.5 composite potential)

**Current**: ~70% | **Target**: 85% | **Why it matters**: 18% of total Task 1 score

**What we know**: The LLM over-escalates priorities (P3/P4 → P1/P2) when signals contain safety keywords even in non-serious contexts. E.g., "hull sensor showed anomaly but it was a calibration error" gets P1 instead of P3.

**What to try**:
- Add more anti-escalation examples to the prompt
- Post-process: if description contains "resolved", "calibration error", "just kidding", "test" → don't escalate
- Test against the 100 adversarial v2 signals (`synthetic/triage_adversarial_v2.json`)

### 3. Improve Task 1 Routing (+1.3 composite potential)

**Current**: 0.762 | **Target**: 0.95 | **Why it matters**: 24% of resolution weight

**Root cause**: Category is correct but team is wrong for ~6 exception cases:
- Flight Software → Spacecraft Systems Engineering (when hardware root cause)
- Mission Briefing → various teams (offboarding→Identity, provisioning→SSE, booking→MSO)
- Hull → Deep Space Communications (network-control-path issues)

**What to try**:
- Add these exceptions as examples in the LLM prompt
- Let the LLM decide team directly (not just category→team mapping)
- Add postprocessor heuristics for known exception patterns

### 4. Reduce Task 2 Latency (+0.8 composite potential)

**Current P95**: ~10s | **Target**: 5s | **Latency threshold**: 2000ms best, 20000ms worst

**Root cause**: Large document images (avg 1.4MB, max 12.9MB base64) — vision model processing time

**What to try**:
- `max_completion_tokens=500` to cap output length
- `detail:low` — reduces tile count (TEST resolution impact first!)
- Compress images (JPEG quality 85) instead of downscaling (downscaling to 2048px destroyed text — DON'T do this)
- Azure DI for OCR + text-only LLM (tested, DI was slower — but could work with async/parallel)

### 5. Run Comprehensive Synthetic Data Eval

**We have 1,349 triage items but haven't hill-climbed against v3 (500 items)** — it was generated at the end of the session. This is free improvement waiting to be captured.

```bash
# Score against all synthetic data
cd /home/fbujaroski/be-an-fde-for-a-day/py
source .venv/bin/activate
cd apps/sample
python3 << 'PYEOF'
import json, requests, sys
sys.path.insert(0, '../../common/libs/fdebenchkit/src')
from ms.common.fdebenchkit.scorers.ticket_triage import score_submission

for name, inp_path, gold_path in [
    ("v2 (499)", "synthetic/triage_v2.json", "synthetic/triage_v2_gold.json"),
    ("v3 (500)", "synthetic/triage_v3.json", "synthetic/triage_v3_gold.json"),
    ("adversarial (100)", "synthetic/triage_adversarial_v2.json", "synthetic/triage_adversarial_v2_gold.json"),
]:
    with open(inp_path) as f: inputs = json.load(f)
    with open(gold_path) as f: golds = json.load(f)
    results = [requests.post('http://localhost:8000/triage', json=inp, timeout=30).json() for inp in inputs]
    scores = score_submission(results, golds)
    print(f"{name}: Resolution={scores['resolution']:.1f}")
    for dim, s in sorted(scores['dimension_scores'].items()):
        print(f"  {dim}: {s:.3f}")
PYEOF
```

---

## 📊 Current State

### v13 Scores (deployed)

| Task | Tier 1 | Resolution | Efficiency | Robustness |
|------|--------|-----------|-----------|-----------|
| Triage | 77.2 | 71.8 | 85.0 | 81.1 |
| Extract | **88.1** | **91.6** | 69.2 | 94.9 |
| Orchestrate | **93.8** | **90.4** | 100.0 | 95.3 |
| **Composite** | **86.4** | 84.6 | 84.7 | 90.4 |

### Generalization (what to expect on hidden eval)

| Dataset | Items | Task 1 Resolution | Notes |
|---------|-------|--------------------|-------|
| 25-item golden sample | 25 | 71.8 | Used by `make eval` |
| 50-item golden eval | 50 | ~31* | Only 2/8 categories — non-representative |
| v1 synthetic | 200 | 67.0 | General distribution |
| v2 synthetic | 499 | 75.5 | Targets weaknesses |
| v3 synthetic | 500 | 75.1 | Cross-category ambiguity |
| Adversarial | 100 | 69.7 | Injection, misdirection |
| Edge cases | 50 | 66.5 | Boundary cases |

*50-item golden has only Comms+Access categories. LLM correctly classifies across all 8 but gold expects only 2.

**Realistic hidden-eval Task 1 estimate: 70-78 resolution** (based on synthetic data consistency)

---

## 🏗️ Architecture

### Task 1 — Signal Triage
```
Request → Preprocess (non-incidents only, <10ms)
            ├── Non-incident → immediate P4/None
            └── Everything else → LLM (gpt-5.4-mini) → Postprocess (team/P1/escalation)
```
- **Key files**: `routers/triage.py`, `services/triage_rules.py` (207 lines), `prompts/triage_prompt.py`
- **Why LLM-primary**: Rules engine was overfit. LLM generalizes across all 8 categories.

### Task 2 — Document Extraction
```
Request → gpt-5.4-mini vision (detail:auto, NO image resize) → postprocess (dates, schema-aware types)
```
- **Key files**: `routers/extract.py`, `prompts/extract_prompt.py`
- **⚠️ Image downscaling DISABLED** — 2048px resize destroyed text clarity (91.6→76.0)

### Task 3 — Workflow Orchestration
```
Request → detect_template(goal) → 7 deterministic executors (NO LLM, 42ms P95)
            └── Unknown template → ReAct LLM fallback (gpt-5.4)
```
- **Key files**: `routers/orchestrate.py`, `services/template_executor.py` (719 lines)
- **⚠️ No retry on tool calls** — retry consumes mock response slots

---

## ❌ What Failed (Don't Repeat These)

| Approach | Why It Failed | Score Impact |
|----------|--------------|-------------|
| **Keyword rules engine for Task 1** | Overfit to 2-category golden data. 93.6 on golden, 60.2 on synthetic. | -33 on hidden eval |
| **Image downscaling (2048px)** | Destroyed document text clarity | Resolution 91.6→76.0 |
| **Few-shot from golden data** | Biased model toward P3 over-prediction | -3 resolution |
| **gpt-5.4-nano for Task 1** | Surprisingly SLOWEST model (4-10s cold start) | Terrible latency |
| **Azure DI hybrid for Task 2** | DI OCR took ~7s alone, slower than vision-only | No improvement |
| **Retry on Task 3 tool calls** | Consumes mock service response slots, corrupts subsequent data | -1.5 resolution |
| **Blind boolean/null coercion** | "na", "no", "yes" are valid field values in some schemas | -15 Task 2 resolution |
| **Optimizing for golden data** | THE biggest mistake — golden data is non-representative | -20-30 on hidden eval |

---

## 🧪 Synthetic Data Guide

### What we have
| Dataset | Items | Location | Quality |
|---------|-------|----------|---------|
| **Triage v2** | 499 | `synthetic/triage_v2.json` | **Best for hill-climbing** — targets weaknesses |
| **Triage v3** | 500 | `synthetic/triage_v3.json` | Cross-category ambiguity, priority gray zones |
| **Triage adversarial** | 100 | `synthetic/triage_adversarial_v2.json` | Injection, misdirection, stress |
| Triage v1 | 200 | `synthetic/triage_synthetic.json` | General distribution (older) |
| Triage edge cases | 50 | `synthetic/triage_edge_cases.json` | Hand-crafted boundaries |
| **Orchestrate v2** | 130 | `synthetic/orchestrate_v2.json` | Template detection variants |
| Orchestrate detect | 80 | `synthetic/orchestrate_detection_test.json` | Paraphrase robustness |

### How to use synthetic data for optimization
1. **Make a change** (prompt, postprocessing, architecture)
2. **Score against v2 + v3 synthetic** (999 items total)
3. **Also score against 25-item golden sample** (sanity check)
4. **If synthetic improves AND golden doesn't collapse → ship it**
5. **If golden improves but synthetic doesn't → you're overfitting, revert**

### Synthetic data quality caveats
- Gold labels generated by LLM + routing guide rules — may not match competition creator's intent
- Priority P2 vs P3 boundary is subjective
- Some signals may be more/less realistic than actual eval items
- Generate MORE synthetic data if you find gaps (use `synthetic/generate_triage_v2.py` as template)

---

## 🔧 Experiments Not Yet Run

| Experiment | Expected Impact | Effort | Notes |
|-----------|----------------|--------|-------|
| **Hill-climb prompt on v3 synthetic (500 items)** | +1-3 composite | Medium | v3 was generated at session end, never tested against |
| **Missing info post-processing filter** | +1-2 composite | Low | Remove low-confidence items, keep only module_specs/anomaly_readout |
| **max_completion_tokens=500 for Task 2** | +0.5 composite (latency) | Low | Caps output, faster response |
| **detail:low for Task 2** | Unknown | Low | Test resolution vs latency tradeoff |
| **JPEG compression for Task 2 images** | +0.3 composite (latency) | Low | Compress before sending, keep resolution |
| **Claude Sonnet** | Unknown | Medium | Requires separate AOAI resource |
| **Fine-tuning gpt-4o-mini on synthetic** | +5-10% Task 1? | High | If AOAI supports it |
| **Ensemble/voting (2 models)** | +2-3% resolution | High | Latency doubles |
| **DSPy automatic prompt optimization** | Unknown | High | Could find better prompts |
| **Task 3 dynamic calendar dates** | +0.3 composite | Low | Extract dates from goal text |
| **Category→team exception examples in prompt** | +0.5 composite | Low | Add SIG-0002, SIG-0020 patterns |

---

## 🏗️ Repositories & Infrastructure

### Repos

| Repo | URL | Purpose |
|------|-----|---------|
| **Public (submit this)** | https://github.com/Bujo0/fdebench-solution | Pablo invited, public |
| Private fork (dev) | https://github.com/Bujo0/be-an-fde-for-a-day | `origin` remote |
| Competition | https://github.com/microsoft/be-an-fde-for-a-day | `upstream` remote |

### Azure Resources (all on fde-dev-01 subscription)

| Resource | Name | Location |
|----------|------|----------|
| Resource Group | fbujaroski-fdebench-rg | eastus2 |
| AOAI | fbujaroski-fdebench-aoai | eastus |
| Container Registry | fbujafdebenchacr | eastus2 |
| Container App | fdebench-api (v13) | eastus2 |
| **API Endpoint** | https://fdebench-api.ashyplant-a5c239d3.eastus2.azurecontainerapps.io | |
| Document Intelligence | fbujaroski-fdebench-di | eastus2 |

**⚠️ AOAI key auth is DISABLED** — uses DefaultAzureCredential. Run `az login` first.

### AOAI Deployments
| Name | Model | Capacity | Cost Score |
|------|-------|----------|-----------|
| gpt-5-4 | gpt-5.4 | 200 TPM | 0.75 |
| gpt-5-4-mini | gpt-5.4-mini | 200 TPM | 0.90 |
| gpt-5-4-nano | gpt-5.4-nano | 500 TPM | 1.00 |
| o4-mini | o4-mini | 200 TPM | 0.75 |
| gpt-4-1 | gpt-4.1 | 100 TPM | 0.75 |

### Push & Deploy Workflow
```bash
# Push to both repos
git push origin fdebench-solution --no-verify
GIT_LFS_SKIP_PUSH=1 git push public fdebench-solution:main --force --no-verify

# Build and deploy
az acr build --registry fbujafdebenchacr --resource-group fbujaroski-fdebench-rg --image fdebench-api:vNEW .
az containerapp update --name fdebench-api --resource-group fbujaroski-fdebench-rg --image fbujafdebenchacr.azurecr.io/fdebench-api:vNEW
```

### Submission
Submit at **[aka.ms/fde/hackathon](https://aka.ms/fde/hackaton)** with:
- **Repo**: `https://github.com/Bujo0/fdebench-solution`
- **API**: `https://fdebench-api.ashyplant-a5c239d3.eastus2.azurecontainerapps.io`

---

## 📚 Key Files Reference

### Solution Code (`py/apps/sample/`)
| File | Lines | Purpose |
|------|-------|---------|
| `main.py` | 60 | App factory, lifespan, health |
| `routers/triage.py` | ~150 | Preprocess → LLM → postprocess |
| `routers/extract.py` | ~320 | Vision + date/type postprocessing |
| `routers/orchestrate.py` | ~140 | Template executor + ReAct fallback |
| `services/triage_rules.py` | 207 | Preprocessor (non-incidents only) |
| `services/template_executor.py` | 719 | 7 deterministic template executors |
| `prompts/triage_prompt.py` | ~246 | **EDIT THIS to improve Task 1** |
| `config.py` | 29 | Env var settings |
| `llm_client.py` | 116 | AOAI client |

### Scorer Code (READ THIS — it's the ground truth)
| File | What you learn |
|------|---------------|
| `weights.py` | Tier 1 formula, efficiency/robustness sub-weights |
| `runner.py` | Cost tier mapping (`_MODEL_TIER_SCORES`), P95 trimming, warm-up |
| `registry.py` | Per-task latency thresholds |
| `scorers/ticket_triage.py` | Category/priority/routing scoring, macro F1 |
| `scorers/document_extraction.py` | Info accuracy vs text fidelity, normalization rules |
| `scorers/workflow_orchestration.py` | **Lines 493-767**: template-specific constraint checks |
| `probes.py` | 7 resilience probes, pass/fail conditions |

### Documentation
| File | Purpose |
|------|---------|
| `docs/hill-climbing-analysis.md` | Full experiment history (562 lines) |
| `docs/architecture.md` | System design for Tier 2 judges |
| `docs/methodology.md` | Approach and iteration |
| `docs/evals.md` | Scores and error analysis |
| `RUNBOOK.md` | Setup, deploy, submit |

---

## 📐 Scoring Cheat Sheet

```
tier1 = 0.50 × Resolution + 0.20 × Efficiency + 0.30 × Robustness
efficiency = 0.60 × latency + 0.40 × cost
robustness = 0.60 × adversarial + 0.40 × probes (always 100%)
composite = mean(task1, task2, task3)
```

| Task | Latency Best | Latency Worst |
|------|-------------|--------------|
| Triage | ≤500ms | ≥5,000ms |
| Extract | ≤2,000ms | ≥20,000ms |
| Orchestrate | ≤1,000ms | ≥10,000ms |

**Critical scorer behaviors**:
- Cost = modal model (most common), not average
- P95 latency is trimmed (top/bottom 5% removed)
- Task 1 uses **macro F1** — rare categories weighted equally
- Task 1 `missing_info`: empty+empty = **1.0 free point**
- Task 1 `next_best_action` and `remediation_steps` are **unscored**
- Task 2: extra fields ignored, missing fields = 0
- Task 3: `status` must be `"completed"` or goal_completion = 0
- Task 3: `audit_log` exempt from ordering dependencies
- Unknown model in X-Model-Name → cost score = **0.0**

---

*Generated from a session spanning 40+ experiments, 13 container versions, and 1,349+ synthetic items.*
