# CDSS Signal Routing Protocol

> **Last updated:** July 2425
> **Author:** Lt. Raj Mehta, Mission Ops Deck Manager
> **Status:** DRAFT — some sections still being finalized after the Q2 sector reorganization

---

## How to use this protocol

When a signal comes in, identify the **anomaly type** from the table below and route to the listed **owning division**. If you're unsure, escalate to the Mission Ops Deck Lead.

## Priority Definitions

| Priority | Label | Response SLA | Resolution SLA | When to use |
|---|---|---|---|---|
| P1 | 🔴 Red Alert | 15 min | 4 hours | Critical system down, containment breach in progress, mission-impacting outage, command-staff-impacting |
| P2 | 🟠 Orange Alert | 1 hour | 8 hours | Major subsystem broken, no workaround, multiple crew affected |
| P3 | 🟡 Yellow Alert | 4 hours | 3 duty cycles | Impact with workaround available, single crew member blocked but non-urgent |
| P4 | 🟢 Routine | 1 duty cycle | 10 duty cycles | Minor inconvenience, cosmetic issue, feature request, general question |

**Override rule:** Any signal mentioning potential hull breach, hostile contact, or quarantine protocol is automatically **P1** regardless of other factors.

---

## Routing Table

### Crew Identity & Airlock Control (CIAC)

| Anomaly type | Route to | Notes |
|---|---|---|
| Biometric recalibration | CIAC | Self-service kiosk handles most; only escalate if auto-recal fails |
| Crew lockout | CIAC | Check for intrusion indicators first — if suspicious, also alert Threat Response |
| New crew provisioning | CIAC | Requires commanding officer approval in MissionFlow |
| SSO not working | CIAC | Verify the system is in the Station Identity Core registry first |
| Directory sync issues | CIAC | Usually Station Identity Core connector related |
| Service account requests | CIAC | Requires security review before provisioning |

### Spacecraft Systems Engineering

| Anomaly type | Route to | Notes |
|---|---|---|
| Personal terminal hardware failure | Spacecraft Systems Engineering | If under warranty, initiate vendor RMA |
| ShipOS crash / critical fault | Spacecraft Systems Engineering | Collect diagnostic dump before reimaging |
| Software installation request | Spacecraft Systems Engineering | Must be on the approved software list |
| ShipGuard enrollment | Spacecraft Systems Engineering | New crew should be auto-enrolled |
| 3D fabricator issues | Spacecraft Systems Engineering | Check if it's a networked fabricator (→ Deep Space Comms) or local unit |
| Personal device issues | Spacecraft Systems Engineering | Station-managed devices only |
| Slow terminal | Spacecraft Systems Engineering | Run hardware diagnostics first |

### Deep Space Communications

| Anomaly type | Route to | Notes |
|---|---|---|
| Subspace relay connectivity | Deep Space Communications | Check if crew's credentials are expired first (→ CIAC if so) |
| Station mesh network issues | Deep Space Communications | — |
| Beacon resolution failures | Deep Space Communications | — |
| Signal filter rule requests | Deep Space Communications | Requires security approval from Threat Response |
| Bandwidth / latency | Deep Space Communications | Get specific times and affected services |
| HoloDeck Comms quality | Deep Space Communications | If it's a HoloDeck Comms app-specific issue, try Mission Software Ops first |

### Mission Software Operations

| Anomaly type | Route to | Notes |
|---|---|---|
| Station Resource Manager errors or access | Mission Software Operations | — |
| OrbitalForce issues | Mission Software Operations | — |
| Quantum Terminal | Mission Software Operations | Physical hardware issues go to Spacecraft Systems Engineering |
| StarSuite 365 issues | Mission Software Operations | Licensing issues specifically — general StarSuite 365 outages are Deep Space Comms |
| Internal mission app bugs | Mission Software Operations | — |
| Application licensing | Mission Software Operations | — |

### Threat Response Command (TRC)

| Anomaly type | Route to | Notes |
|---|---|---|
| Phishing transmission received | TRC | Forward original as attachment to threats@cdss.space |
| Hostile code / suspicious activity | TRC | Isolate affected system from the network immediately |
| Data loss / unauthorized access | TRC | Mandatory P1 escalation |
| Security certificate issues | TRC | — |
| Protocol compliance / audit requests | TRC | — |

### Telemetry & Data Core

| Anomaly type | Route to | Notes |
|---|---|---|
| Data nexus access | Telemetry & Data Core | — |
| Telemetry sync issues | Telemetry & Data Core | Large data stream sync problems are common; check buffer limits |
| Data vault access request | Telemetry & Data Core | Requires data owner approval |
| Backup / restore request | Telemetry & Data Core | — |
| Legacy data share access | Telemetry & Data Core | Legacy data shares only; new requests should use data nexus |

---

## Known gaps in this protocol

> **Lt. Mehta's note:** The following areas still need to be sorted out. For now, use your best judgment or escalate to the Mission Ops Deck Lead.

- **Biometric verification anomalies** — Could be CIAC (crew setup), Threat Response (policy enforcement), or Spacecraft Systems Engineering (scanner hardware issues). We haven't agreed on a single owner.
- **HoloDeck Comms / collaboration issues** — Is it a Deep Space Comms issue (call quality), Mission Software Ops issue (HoloDeck Comms app crash), or Spacecraft Systems Engineering issue (headset/holographic projector)? Depends on the symptoms.
- **Orbital infrastructure requests** — Azure Orbital subscription access, compute pod requests, etc. Telemetry & Data Core handles some, but we don't have a formal orbital ops division yet.
- **Crew onboarding / offboarding** — Touches CIAC (accounts), Spacecraft Systems Engineering (equipment), Mission Software Ops (licenses), and Telemetry & Data Core (access). There's a workflow for this but it's manual and breaks constantly.
- **3D fabricator and scanning** — Networked fabricators are Deep Space Comms, local fabricators are Spacecraft Systems Engineering, scan-to-comms failures could be either.

---

## Escalation rules

1. **P1 signals** — Must be acknowledged within 15 minutes. If the assigned division doesn't acknowledge, auto-escalate to Mission Ops Deck Lead.
2. **Threat incidents** — Always route to Threat Response Command. If it also affects another division's domain (e.g., compromised crew identity = CIAC + TRC), route to TRC as primary and CIAC as secondary.
3. **VIP signals** — Command staff and senior officers are auto-flagged. Treat as one priority level higher than normal assessment.
4. **Repeat signals** — If the same reporter has filed 3+ signals in 7 cycles for the same anomaly, escalate to the division lead for root cause investigation.
