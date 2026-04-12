# CDSS Mission Control — Internal Routing Guide

> **Last updated:** July 2025
> **Author:** Commander Kovacs, Mission Control Desk Manager
> **Status:** DRAFT — some sections still being finalized after the Q2 reorg

---

## How to use this guide

When a signal comes in, identify the **issue type** from the table below and route to the listed **owning division**. If you're unsure, escalate to the Mission Control Desk Lead.

## Priority Definitions

| Priority | Label | Response SLA | Resolution SLA | When to use |
|---|---|---|---|---|
| P1 | Critical | 15 min | 4 hours | Critical system down, security breach in progress, mission-impacting outage, command staff-impacting |
| P2 | High | 1 hour | 8 hours | Major system broken, no workaround, multiple crew members affected |
| P3 | Medium | 4 hours | 3 business days | Impact with workaround available, single crew member blocked but non-urgent |
| P4 | Low | 1 business day | 10 business days | Minor inconvenience, cosmetic issue, feature request, general question |

**Override rule:** Any signal mentioning potential data breach, regulatory issue, or compliance audit is automatically **P1** regardless of other factors.

---

## Routing Table

### Crew Identity & Airlock Control (CIAC)

| Issue type | Route to | Notes |
|---|---|---|
| Password reset | CIAC | Self-service portal handles most; only escalate if SSPR fails |
| Account lockout | CIAC | Check for brute-force indicators first — if suspicious, also alert Threat Response Command |
| New crew provisioning | CIAC | Requires commanding officer approval in Mission Control System |
| SSO not working | CIAC | Verify the app is in the Ship Identity Registry gallery first |
| Registry sync issues | CIAC | Usually Ship Identity Registry Connect related |
| Service account requests | CIAC | Requires security review before provisioning |

### Spacecraft Systems Engineering

| Issue type | Route to | Notes |
|---|---|---|
| Module hardware failure | Spacecraft Systems Engineering | If under warranty, initiate vendor RMA |
| OS crash / system halt | Spacecraft Systems Engineering | Collect crash dump before reimaging |
| Software installation request | Spacecraft Systems Engineering | Must be on the approved software list |
| Fleet Device Manager enrollment | Spacecraft Systems Engineering | New crew should be auto-enrolled |
| Airlock / docking port issues | Spacecraft Systems Engineering | Check if it's a network-linked airlock (→ Deep Space Communications) or locally controlled |
| Mobile unit issues | Spacecraft Systems Engineering | Station-managed units only |
| Slow system | Spacecraft Systems Engineering | Run hardware diagnostics first |

### Deep Space Communications

| Issue type | Route to | Notes |
|---|---|---|
| Subspace relay link connectivity | Deep Space Communications | Check if crew's credentials are expired first (→ CIAC if so) |
| Station comms array issues | Deep Space Communications | — |
| Nav beacon resolution failures | Deep Space Communications | — |
| Signal routing rule requests | Deep Space Communications | Requires security approval from Threat Response Command |
| Bandwidth / latency | Deep Space Communications | Get specific times and affected services |
| HoloComm conferencing quality | Deep Space Communications | If it's a HoloComm-specific app issue, try Mission Software Operations first |

### Mission Software Operations

| Issue type | Route to | Notes |
|---|---|---|
| ATLAS Cargo System errors or access | Mission Software Operations | — |
| HERMES Trade System issues | Mission Software Operations | — |
| ORION Market Terminal | Mission Software Operations | Physical hardware issues go to Spacecraft Systems Engineering |
| Mission Suite issues | Mission Software Operations | Licensing issues specifically — general Mission Suite outages are Deep Space Communications |
| Internal mission app bugs | Mission Software Operations | — |
| Application licensing | Mission Software Operations | — |

### Threat Response Command (TRC)

| Issue type | Route to | Notes |
|---|---|---|
| Hostile signal received | TRC | Forward original as attachment to threats@contoso.space |
| Malware / suspicious activity | TRC | Isolate affected module from the network immediately |
| Data breach / unauthorized access | TRC | Mandatory P1 escalation |
| Security certificate issues | TRC | — |
| Compliance / audit requests | TRC | — |

### Telemetry & Data Core

| Issue type | Route to | Notes |
|---|---|---|
| DataVault access | Telemetry & Data Core | — |
| PersonalVault sync issues | Telemetry & Data Core | Large file sync problems are common; check file count limits |
| Database access request | Telemetry & Data Core | Requires data owner approval |
| Backup / restore request | Telemetry & Data Core | — |
| Data archive access | Telemetry & Data Core | Legacy data archives only; new requests should use DataVault |

---

## Known gaps in this guide

> **Commander Kovacs' note:** The following areas still need to be sorted out. For now, use your best judgment or escalate to the Mission Control Desk Lead.

- **Biometric scanner issues** — Could be CIAC (crew setup), Threat Response Command (policy enforcement), or Spacecraft Systems Engineering (scanner hardware issues). We haven't agreed on a single owner.
- **HoloComm / collaboration issues** — Is it a Deep Space Communications issue (call quality), Mission Software Operations issue (HoloComm app crash), or Spacecraft Systems Engineering issue (headset/holographic projector)? Depends on the symptoms.
- **Orbital Platform infrastructure requests** — Orbital Platform subscription access, VM requests, etc. Telemetry & Data Core handles some, but we don't have a formal cloud ops division yet.
- **Crew onboarding / offboarding** — Touches CIAC (accounts), Spacecraft Systems Engineering (hardware), Mission Software Operations (licenses), and Telemetry & Data Core (access). There's a workflow for this but it's manual and breaks constantly.
- **Airlock and docking systems** — Network-linked airlocks are Deep Space Communications, locally controlled airlocks are Spacecraft Systems Engineering, scan-to-relay failures could be either.

---

## Escalation rules

1. **P1 signals** — Must be acknowledged within 15 minutes. If the assigned division doesn't acknowledge, auto-escalate to Mission Control Desk Lead.
2. **Security incidents** — Always route to Threat Response Command. If it also affects another division's domain (e.g., compromised crew account = CIAC + Threat Response Command), route to Threat Response Command as primary and CIAC as secondary.
3. **VIP signals** — Command staff and senior officer+ signals are auto-flagged. Treat as one priority level higher than normal assessment.
4. **Repeat signals** — If the same reporter has filed 3+ signals in 7 days for the same issue, escalate to the division lead for root cause investigation.
