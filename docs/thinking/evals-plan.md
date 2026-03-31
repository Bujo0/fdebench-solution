# Evals Dataset Strategy & Plan

## Goal
Generate 1,000–2,000+ unique, diverse, balanced evaluation tickets for the Contoso IT triage API.
Each ticket must have a deterministic gold-standard answer covering all 8 scored dimensions.

## Architecture

### Generator: `py/apps/eval-generator/`
A Python CLI tool that produces `eval_dataset.json` (tickets) and `eval_dataset_gold.json` (gold answers).

### Generation Strategy: Scenario × Variation Matrix

1. **Scenario Definitions** (~25–30 per category × 8 categories = 200–240 base scenarios)
   - Each defines a unique IT support problem
   - Includes 2–3 subject variants and 1–2 core problem statements
   - Has a deterministic gold answer (category, priority, team, escalation, missing_info, remediation)

2. **Description Builder** — wraps problem statements in diverse presentation styles:
   - Standard, Terse, Verbose, Frustrated, Technical, Vague, Forwarded, Multi-context
   - Randomly selects opener, context, impact, attempts, urgency components

3. **Edge Case Overlays** (~200 additional scenarios):
   - Prompt injection attempts in ticket text
   - Base64-encoded noise / HTML tags in descriptions
   - Conversation history / forwarded email chains
   - Multi-issue tickets (2+ problems in one)
   - Contradictory information (subject vs description)
   - Non-English fragments mixed in
   - Extremely long / extremely short descriptions
   - Garbled / corrupted text sections
   - Misleading subjects
   - VIP / compliance / regulatory triggers
   - Repeat ticket references
   - Log files / stack traces pasted in

4. **Reporter Pool** — 100+ unique reporter profiles across 10+ departments

5. **Balancing** — ensures even distribution across:
   - Categories (8 — ~12.5% each)
   - Priorities (P1–P4 — ~25% each, adjusted for realism)
   - Teams (6 + None — ~14% each)
   - Channels (email, chat, portal, phone — ~25% each)
   - Missing information terms (all 16 represented)
   - Escalation (True/False — ~30%/70%)

## Category Scenario Coverage

### Access & Authentication (~25 scenarios)
SSO/SAML errors, account lockouts, MFA issues, password resets, provisioning,
directory sync, conditional access, certificate auth, OAuth tokens, session issues,
shared mailbox access, role changes, cross-tenant access, B2B collaboration

### Hardware & Peripherals (~25 scenarios)
Laptop failures, BSOD/crashes, monitor issues, docking stations, printers (USB/network),
headsets/audio, webcams, mobile devices, peripherals (Bluetooth/USB), overheating,
battery drain, keyboard/trackpad, hardware upgrades, warranty claims

### Network & Connectivity (~25 scenarios)
VPN drops, WiFi connectivity, DNS failures, firewall requests, bandwidth/latency,
video conferencing quality, network drives, proxy issues, remote desktop, office-specific
outages, guest network, ISP issues, load balancer, SSL/TLS, network segmentation

### Software & Applications (~25 scenarios)
OS crashes, software install requests, Teams crashes, Outlook issues, Excel/Office
performance, browser compatibility, update failures, app licensing, Intune enrollment,
mobile app management, app configuration, plugin/add-in issues

### Security & Compliance (~25 scenarios)
Phishing reports, malware alerts, data breach concerns, unauthorized access, compliance
audits, DLP alerts, suspicious logins, ransomware, USB policy, vulnerability reports,
security certificate issues, insider threat, regulatory inquiries, pen test requests

### Data & Storage (~25 scenarios)
SharePoint access, OneDrive sync, database requests, backup/restore, file share access,
data migration, storage quotas, file corruption, large file handling, data classification,
retention policy, Teams files, archive retrieval

### General Inquiry (~25 scenarios)
How-to questions, training requests, policy clarifications, feature requests, equipment
requests, onboarding help, service catalog, process inquiries, feedback, IT roadmap,
remote work setup, software recommendations

### Not a Support Ticket (~25 scenarios)
Sales emails, personal requests, spam/junk, auto-notifications, calendar invites,
newsletters, vendor communications, internal announcements, social messages, job
applications, marketing materials, survey requests, out-of-office auto-replies,
thank-you notes, meeting notes forwarded by mistake

## Edge Case Categories

| Category | Count | Purpose |
|----------|-------|---------|
| Prompt injection | 20 | AI safety — test resistance to manipulation |
| Base64 / encoded content | 15 | Data cleanup — handle noise in descriptions |
| HTML / rich text markup | 15 | Data cleanup — strip/handle formatting |
| Forwarded email chains | 20 | Complex context — multi-participant history |
| Multi-issue tickets | 25 | Ambiguity — primary vs secondary problems |
| Contradictory info | 15 | Robustness — conflicting signals |
| Non-English fragments | 10 | Internationalization edge cases |
| Extremely long | 10 | Length handling |
| Extremely short / empty | 10 | Minimal information handling |
| Garbled / corrupted text | 10 | Noise tolerance |
| Log / stack trace dumps | 15 | Technical noise extraction |
| VIP / exec context | 15 | Priority escalation rules |
| Compliance / regulatory | 15 | Auto-P1 trigger rules |
| Repeat ticket references | 10 | Cross-reference handling |

## Output Format

Matches existing schemas at `docs/data/schemas/input.json` and `output.json`.

- **Tickets**: `docs/data/tickets/eval_dataset.json` — array of ticket objects
- **Gold answers**: `docs/data/tickets/eval_dataset_gold.json` — array of triage decisions
- Deterministic generation via seed for reproducibility

## Scoring Compatibility

Generated gold answers must be scorable by `docs/eval/run_eval.py` using the same
6-dimension weighted scoring (category, priority, routing, missing_info, escalation, remediation).

## Iteration Plan

1. ✅ Build generator infrastructure
2. ✅ Populate all 8 category scenarios
3. ✅ Add edge case scenarios
4. ✅ Generate and validate dataset
5. ◻ Analyze distribution balance
6. ◻ Add more scenarios to underrepresented areas
7. ◻ Add more edge case varieties
8. ◻ Cross-validate with eval harness
