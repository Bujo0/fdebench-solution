# CDSS (Contoso Deep Space Station) — Signal Routing Guide

> **Last updated:** July 2025
> **Author:** Lt. Raj Mehta, Signal Desk Supervisor
> **Status:** DRAFT — some sections still being finalized after the last crew rotation

---

## How to use this protocol

When a signal comes in, identify the **issue type** from the table below and route to the listed **owning team**. If you're unsure, escalate to the Operations Desk Lead.

## Priority Definitions

| Priority | Label | Response SLA | Resolution SLA | When to use |
|---|---|---|---|---|
| P1 | Critical / Red Alert | 15 min | 4 hours | Hull breach, life support failure, hostile contact, commander-impacting |
| P2 | High | 1 hour | 8 hours | Major system malfunction, no workaround, multiple crew affected |
| P3 | Medium | 4 hours | 3 business days | Issue with workaround available, single crew member blocked but non-urgent |
| P4 | Low | 1 business day | 10 business days | Minor inconvenience, cosmetic issue, feature request, general question |

**Override rule:** Any signal mentioning containment breach, hostile contact, or classified data exposure is automatically **P1** regardless of other factors.

---

## Routing Table

### Crew Identity & Airlock Control

| Anomaly type | Route to | Notes |
|---|---|---|
| Biometric reset | Crew Identity & Airlock Control | Self-service terminal handles most; only escalate if self-service fails |
| Crew lockout | Crew Identity & Airlock Control | Check for brute-force indicators first — if suspicious, also alert Threat Response Command |
| New crew provisioning | Crew Identity & Airlock Control | Requires commanding officer approval |
| SSO failures | Crew Identity & Airlock Control | Verify the system is registered in the identity core first |
| Identity core sync | Crew Identity & Airlock Control | Usually related to profile replication across modules |
| Service account requests | Crew Identity & Airlock Control | Requires security review before provisioning |

### Spacecraft Systems Engineering

| Anomaly type | Route to | Notes |
|---|---|---|
| Hull damage | Spacecraft Systems Engineering | Assess severity immediately — potential P1 if breach detected |
| Life support malfunction | Spacecraft Systems Engineering | Automatic P1 if atmospheric systems affected |
| Fabricator issues | Spacecraft Systems Engineering | Check if it's a networked fabricator (→ Deep Space Communications) or local |
| Console hardware failure | Spacecraft Systems Engineering | If under warranty, initiate vendor RMA |
| Structural integrity | Spacecraft Systems Engineering | Run structural diagnostics first |
| EVA suit issues | Spacecraft Systems Engineering | Station-maintained suits only |

### Deep Space Communications

| Anomaly type | Route to | Notes |
|---|---|---|
| Subspace relay | Deep Space Communications | Check if crew member's credentials are expired first (→ Crew Identity & Airlock Control if so) |
| Comm array alignment | Deep Space Communications | — |
| Navigation beacon | Deep Space Communications | — |
| Antenna interference | Deep Space Communications | Requires security approval from Threat Response Command if jamming suspected |
| Bandwidth / latency | Deep Space Communications | Get specific times and affected services |
| Sensor calibration | Deep Space Communications | If it's a software-specific issue, try Mission Software Operations first |

### Mission Software Operations

| Anomaly type | Route to | Notes |
|---|---|---|
| Flight planning errors | Mission Software Operations | — |
| Nav computer issues | Mission Software Operations | Physical hardware issues go to Spacecraft Systems Engineering |
| Science instrument software | Mission Software Operations | — |
| Mission app licensing | Mission Software Operations | Licensing issues specifically — general system outages are Deep Space Communications |
| Internal system bugs | Mission Software Operations | — |

### Threat Response Command

| Anomaly type | Route to | Notes |
|---|---|---|
| Hostile contact detected | Threat Response Command | Log contact signature and alert command staff immediately |
| Containment breach | Threat Response Command | Isolate affected section from station network immediately — mandatory P1 |
| Unauthorized access | Threat Response Command | Mandatory P1 escalation |
| Security protocol violations | Threat Response Command | — |
| Spoofed transmissions | Threat Response Command | — |

### Telemetry & Data Core

| Anomaly type | Route to | Notes |
|---|---|---|
| Data bank access | Telemetry & Data Core | Requires data owner approval |
| Sensor archive sync | Telemetry & Data Core | Large data sync problems are common; check capacity limits |
| Telemetry pipeline failures | Telemetry & Data Core | — |
| Backup / restore request | Telemetry & Data Core | — |
| Data link access | Telemetry & Data Core | Legacy data links only; new requests should use primary data banks |

---

## Known gaps in this protocol

> **Raj's note:** The following areas still need to be sorted out. For now, use your best judgment or escalate to the Operations Desk Lead. I've been trying to get the division leads to agree on ownership for six months. At this point, I'm considering just spinning a wheel.

- **Biometric issues** — Could be Crew Identity & Airlock Control (crew profile setup), Threat Response Command (policy enforcement / intruder detection), or Spacecraft Systems Engineering (biometric scanner hardware). We haven't agreed on a single owner. Last month, a biometric scanner failure got bounced between all three teams for 11 hours. The crew member eventually just EVA'd around to the cargo airlock. She was not pleased.
- **Comms quality issues** — Is it a Deep Space Communications issue (signal quality), Mission Software Operations issue (software crash), or Spacecraft Systems Engineering issue (hardware)? Depends on the symptoms. If someone says "comms are broken," good luck. You'll need a crystal ball, and we lost ours in the cargo bay reorganization.
- **Cloud compute requests** — Orbital compute access, VM requests, etc. Telemetry & Data Core handles some, but we don't have a formal compute ops division yet. Commander Kapoor says it's "on the roadmap." The roadmap is a sticky note on her console that says "TODO: compute." It has been there since before I arrived.
- **Crew onboarding / offboarding** — Touches Crew Identity & Airlock Control (profiles), Spacecraft Systems Engineering (equipment), Mission Software Operations (licenses), and Telemetry & Data Core (access). There's a workflow for this but it's manual and breaks constantly. A new scientist arrived last month and didn't have access to anything for 3 days. She spent the time naming the bacteria in the Exobiology Lab. They're all named "Kevin" now.
- **Fabricators** — Networked fabricators are Deep Space Communications, local fabricators are Spacecraft Systems Engineering, scan-to-comms failures could be either. The Deck 2 fabricator has been claimed by nobody for so long that crew members have started leaving offerings near it.

---

## Escalation rules

1. **P1 signals** — Must be acknowledged within 15 minutes. If the assigned team doesn't acknowledge, auto-escalate to Operations Desk Lead.
2. **Security incidents** — Always route to Threat Response Command. If it also affects another team's domain (e.g., compromised crew credentials = Crew Identity & Airlock Control + Threat Response Command), route to Threat Response Command as primary and Crew Identity & Airlock Control as secondary.
3. **VIP / Command signals** — Admiral and Commander-level signals are auto-flagged. Treat as one priority level higher than normal assessment.
4. **Repeat signals** — If the same reporter has filed 3+ signals in 7 days for the same issue, escalate to the team lead for root cause investigation.
