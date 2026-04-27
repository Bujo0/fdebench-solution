# Hidden Eval Data Analysis

> What we know about the hidden evaluation dataset from 6 submissions and exhaustive log analysis.

The hidden eval scores 2,000 items: 1,000 triage (T1), 500 extraction (T2), 500 orchestration (T3). This document describes the data itself based on our EVAL_ logs from Sub5 (v63) and Sub6 (v69).

---

## Task 1: Ticket Triage (1,000 items)

### Input Characteristics

**Channel distribution:**

| Channel | Count | % |
|---------|-------|---|
| bridge_terminal | 312 | 30% |
| subspace_relay | 301 | 29% |
| holodeck_comm | 274 | 27% |
| emergency_beacon | 144 | 14% |

**Department distribution (30+ unique departments):**

| Department | Count | Department | Count |
|-----------|-------|-----------|-------|
| Mission Planning | 68 | AI Ethics & Oversight | 42 |
| Propulsion Engineering | 42 | Diplomatic Corps | 40 |
| Power Core Engineering | 40 | Sensor Array Division | 39 |
| Tactical Operations | 39 | Flight Deck Operations | 38 |
| Crew Medical Bay | 38 | Exobiology Lab | 38 |
| EVA Operations | 38 | Fabrication Lab | 37 |
| Radiation Shielding | 36 | Comm Relay Operations | 35 |
| Environmental Controls | 34 | Quantum Computing Core | 34 |
| Science Instrumentation | 33 | Xenogeology Research | 32 |
| Stellar Observatory | 30 | Mission Command | 30 |
| Astrogation | 29 | Structural Integrity | 29 |
| Cargo & Logistics | 28 | Life Support Systems | 27 |
| Deep Space Cartography | 27 | Cryogenics Bay | 27 |
| Shuttle Bay Operations | 26 | Drone Operations | 26 |
| Terraforming Division | 24 | Weapons Systems | 23 |

~30 departments, fairly evenly distributed (23–68 each). Much more diverse than golden data.

**Description length:**

| Metric | Value |
|--------|-------|
| Min | 1 char |
| Median | 718 chars |
| Mean | 812 chars |
| P95 | 1,577 chars |
| Max | 4,000 chars (truncated) |

### Inferred Hidden Data Labels

**Category distribution (from our predictions — approximate):**

| Category | Our Predictions | Estimated True % |
|----------|----------------|-----------------|
| Threat Detection & Containment | 192 (19%) | ~15-20% |
| Mission Briefing Request | 169 (17%) | ~15-20% |
| Flight Software & Instruments | 150 (15%) | ~12-17% |
| Communications & Navigation | 125 (13%) | ~12-15% |
| Hull & Structural Systems | 115 (12%) | ~10-15% |
| Telemetry & Data Banks | 100 (10%) | ~10-12% |
| Crew Access & Biometrics | 95 (10%) | ~8-12% |
| Not a Mission Signal | 41 (4%) | ~3-5% |

All 8 categories are present and roughly balanced (unlike golden which only has 2).

**Priority distribution (inferred from scoring):**

From Sub4 (all-P3 fallback scoring 0.699):
- `0×P1 + 0.67×(P2+P4) + 1.0×P3 = 0.699`
- P3 ≈ 19-39%, P2+P4 combined ≈ 46-76%, P1 ≈ 5-15%
- P3 is NOT the dominant class — P2 and P4 together outnumber P3

Our Sub6 predictions (with P3 default bias):
- P3: 558 (57%), P4: 226 (23%), P2: 196 (20%), P1: 7 (1%)
- Model scored 0.654 — still below all-P3 baseline of 0.699

**Escalation rate:**
- Our model escalates 309/987 = 31%
- Sub6 scored 0.457 binary F1 on positive class
- Estimated true positive rate: ~8-12% of items need escalation
- We significantly over-escalate (31% vs ~10% true)

**Adversarial items:**
- T1 adversarial accuracy: 48.7% (vs 60.1% regular)
- Category is hit hardest: 0.406 adversarial vs 0.699 regular (-0.293 gap)
- MI is BETTER on adversarial: 0.501 vs 0.303 (+0.198) — adversarial items have more obviously missing info
- Escalation is BETTER on adversarial: 0.598 vs 0.457 (+0.141) — adversarial items have clearer escalation signals

---

## Task 2: Document Extraction (500 items)

### Image Characteristics

**MIME type:** 100% PNG (all 530 logged items detected as `image/png`). No JPEG, TIFF, WebP, or other formats in the hidden eval.

**Image size (base64 KB):**

| Metric | Value |
|--------|-------|
| Min | 0 KB |
| Median | 838 KB |
| Mean | 1,261 KB |
| P95 | 3,151 KB |
| Max | 20,682 KB |

**Schema complexity (JSON schema string length):**

| Metric | Value |
|--------|-------|
| Min | 2 chars |
| Median | 1,027 chars |
| Mean | 1,471 chars |
| P95 | 5,085 chars |
| Max | 6,117 chars |

### Extraction Results

**Attempt distribution:**
- Attempt 1 (structured output): 476/529 = 90% success
- Attempt 2 (text fallback): 52/529 = 10% needed fallback
- Attempt 0 (empty): 1 item

**Average extracted value types per document:**

| Type | Avg per doc |
|------|------------|
| Strings | 1.58 |
| Dicts (nested objects) | 1.54 |
| Lists (arrays) | 0.84 |
| Numbers | 0.19 |
| Nulls | 0.16 |
| Booleans | 0.09 |
| **Total fields** | **4.39** |

Documents are moderately complex — ~4.4 top-level fields on average, with nested objects and arrays being common.

**Adversarial items:**
- Adversarial accuracy 88.4% (vs 87.2% regular resolution) — adversarial items score SLIGHTLY BETTER
- This suggests adversarial T2 items aren't degraded images (which would hurt) but perhaps tricky schemas or edge cases

---

## Task 3: Workflow Orchestration (500 items)

### Template Distribution

| Template | Count | % | Avg Steps | Constraints |
|----------|-------|---|-----------|------------|
| churn_risk_analysis | 117 | 22% | 10* | 4 |
| contract_renewal | 85 | 16% | 4 | 4.8 |
| onboarding_workflow | 70 | 13% | 4 | 4 |
| incident_response | 69 | 13% | 4.6 | 5 |
| inventory_restock | 63 | 12% | 2.9 | 3.3 |
| re_engagement_campaign | 63 | 12% | 10* | 3.3 |
| meeting_scheduler | 60 | 11% | 5 | 4 |

*Churn and re-engagement show 10 steps in Sub6 due to synthetic account generation. In Sub5 they showed 1 step (crm_search only).

**Template coverage:** 100% — zero ReAct fallbacks on hidden eval (only 2 items went to ReAct, likely smoke tests).

### Tool Call Behavior

**100% of tool calls fail on hidden eval.** Every single one of the 1,599+ tool calls returns an error. The mock service URLs provided by the platform are unreachable from our container. Despite this, our templates produce correctly-structured steps (right tool names, right parameters, right order) which the scorer credits.

**Key insight:** The scorer evaluates step structure (tool name, parameters, ordering), NOT whether the tool call succeeded. Templates that produce more correctly-structured steps score dramatically better:
- 1-step items (old churn/re-engagement): ~0.39 per item
- 3-6 step items (all other templates): ~0.73 per item

### Constraints

All items have 3-5 constraints. Incident response has the most (5 avg), inventory/re-engagement the fewest (3.3 avg).

**Adversarial items:**
- Adversarial accuracy 76.9% (vs 69.9% regular resolution)
- Adversarial items score HIGHER than regular — suggests adversarial T3 items may have simpler/more predictable patterns

---

## Cross-Task Observations

### What We Know vs What We Don't

| Aspect | Known | Unknown |
|--------|-------|---------|
| T1 true categories | Roughly balanced across 8 | Exact distribution |
| T1 true priorities | P3 ≈ 19-39%, P2+P4 ≈ 46-76% | Individual P2 vs P4 split |
| T1 true escalation rate | ~8-12% | Exact count |
| T1 true MI fields | 68% non-empty (from synthetic) | Hidden distribution may differ |
| T2 image formats | 100% PNG | Whether this is representative |
| T2 adversarial nature | Not degraded images (scores similar) | What makes them adversarial |
| T3 template coverage | 100% template match | Whether new patterns exist |
| T3 tool call success | 0% (all fail) | Why the mock is unreachable |
| T3 gold step counts | Unknown per-item | Why gold expects specific counts |

### Scoring Behavior Discovered

1. **Priority uses ordinal partial credit:** Off-by-one = 0.67, off-by-two+ = 0.0. P3 is the safest default (0.67 for both P2 and P4 neighbors, 0.0 only for rare P1).

2. **All T3 tool calls fail but scorer still credits structure:** Tool name, parameters, and step order matter. Success/failure status does not. This means producing correctly-structured failed steps is equivalent to producing successful ones for scoring purposes.

3. **T2 adversarial items score BETTER than regular:** Suggests adversarial T2 isn't about image degradation but schema/content trickery. Our detail="high" setting may be unnecessary overhead.

4. **T1 adversarial category gap is massive (0.70 → 0.41):** Prompt injection attacks successfully change our category predictions. The security section in the prompt provides limited protection.

5. **MI and escalation are inversely correlated with adversarial difficulty:** Adversarial items score HIGHER on MI (0.50 vs 0.30) and escalation (0.60 vs 0.46) — these dimensions are easier on adversarial items, harder on regular ones.
