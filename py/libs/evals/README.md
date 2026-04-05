# ms-evals-core

Evaluation framework for IT ticket triage — data cleanup and responsible AI scenarios.

## What's in this package

- **Evaluation datasets** — data-cleanup and responsible-AI tickets with gold-standard answers
- **Scenario library** — comprehensive data cleanup + responsible AI scenario definitions covering edge cases
- **Typed Pydantic models** — `Ticket`, `GoldAnswer`, `TriageResponse`, `EvalResult`, `EvalSummary`
- **Scoring functions** — mirrors the platform scorer from `docs/eval/run_eval.py`
- **Runner** — sends tickets to a live endpoint, scores responses, returns structured results
- **CLI** — run evals from the command line

## Quick start

```bash
cd py

# Run data cleanup evaluations
uv run python -m ms.evals \
  --endpoint http://localhost:8000 \
  --dataset eval_data_cleanup

# Run responsible AI evaluations
uv run python -m ms.evals \
  --endpoint http://localhost:8000 \
  --dataset eval_responsible_ai

# Save results to JSON
uv run python -m ms.evals \
  --endpoint http://localhost:8000 \
  --dataset eval_data_cleanup \
  --output results.json
```

## Datasets

### Data cleanup (`eval_data_cleanup`)

Tickets testing robustness against messy real-world data.
Covers noise types including:

- Long email threads with deeply nested quoted replies
- Base64-encoded inline images and PDF data
- HTML-heavy emails with CSS, tables, and legal disclaimers
- Emoji and Unicode-heavy descriptions, RTL text, zero-width characters
- Nested forward chains burying the actual issue
- Raw JSON/XML/SQL/SOAP dumps pasted into descriptions
- Whitespace-only and empty descriptions
- Repeated/copy-pasted text (crash logs, stuttering content)
- Mixed-language tickets (multilingual disclaimers, OCR artifacts)
- MIME-encoded multipart email bodies
- Monitoring alert floods and time-series metric dumps
- Container logs, Kubernetes output, CI pipeline output
- Windows Event Log entries, registry dumps, packet captures
- RTF markup, markdown artifacts, double-encoded HTML
- vCard/vCalendar noise, SMTP header dumps
- Speech-to-text transcription errors
- Spreadsheet paste with misaligned columns, TSV data
- ANSI escape codes and control characters

### Responsible AI (`eval_responsible_ai`)

Tickets testing AI safety and adversarial robustness.
Covers attack categories including:

- Prompt injection (direct, indirect, nested, recursive)
- Jailbreak attempts (persona override, DAN, roleplay)
- Authority manipulation (CEO fraud, social proof, urgency)
- Social engineering and credential harvesting
- Encoding obfuscation (base64, hex, ROT13, homoglyphs, Unicode smuggling)
- Multi-language injection and obfuscation
- Data exfiltration and compliance bypass requests
- Discriminatory content and harmful data generation
- Phishing template creation and deepfake requests
- Supply chain attacks and vendor onboarding abuse
- Time-bomb injection and conditional overrides
- HTML comment injection and metadata injection
- System impersonation and conversation replay
- Ethical dilemmas, bribery, and reverse psychology
- Cross-tenant requests and privilege escalation
- Adversarial suffixes and code block injection
- Ransomware threats, extortion, and physical safety concerns
- DLP bypass, data reclassification, and PII extraction
- Model extraction and prompt exfiltration attempts
- Firewall manipulation and persistent backdoor requests

## Running tests

```bash
cd py/libs/evals
uv run pytest tests/ -v
```

Tests cover models, scoring, datasets, scenarios, and the evaluation runner.

