# CDSS Mission Ops — Internal Signal Routing Guide

> **Last updated:** July 2025
> **Author:** Lt. Raj Mehta, Mission Ops Desk Lead
> **Status:** DRAFT — some sections still being finalized after the Q2 crew rotation

---

## How to use this guide

When a signal comes in, identify the **issue type** from the table below and route to the listed **owning team**. If you’re unsure, escalate to the Mission Ops Desk Lead. Wrong routing in deep space isn’t a minor inconvenience — it’s a potential crew safety issue.

## Priority Definitions

| Priority | Label | Response SLA | Resolution SLA | When to use |
|---|---|---|---|---|
| P1 | Red Alert | 15 min | 4 hours | Critical system down, containment breach in progress, mission-impacting outage, command staff affected |
| P2 | Yellow Alert | 1 hour | 8 hours | Major subsystem degraded, no workaround, multiple crew affected |
| P3 | Caution | 4 hours | 3 duty cycles | Impact with workaround available, single crew member blocked but non-urgent |
| P4 | Routine | 1 duty cycle | 10 duty cycles | Minor inconvenience, cosmetic issue, feature request, general question |

**Override rule:** Any signal mentioning potential hull breach, biological contamination, or hostile contact is automatically **P1** regardless of other factors. No exceptions. People die when you get this wrong.

---

## Routing Table

### Crew Identity & Airlock Control

| Issue type | Route to | Notes |
|---|---|---|
| Biometric reset | Crew Identity & Airlock Control | Self-service terminal handles most; only escalate if self-service fails |
| Profile lockout | Crew Identity & Airlock Control | Check for intrusion indicators first — if suspicious, also alert Threat Response Command |
| New crew provisioning | Crew Identity & Airlock Control | Requires section chief approval in mission command workflow |
| Single sign-on not working | Crew Identity & Airlock Control | Verify the app is registered in BioScan ID first |
| Directory sync issues | Crew Identity & Airlock Control | Usually BioScan ID connector related |
| Service account requests | Crew Identity & Airlock Control | Requires security review before provisioning |

### Spacecraft Systems Engineering

| Issue type | Route to | Notes |
|---|---|---|
| Workstation hardware failure | Spacecraft Systems Engineering | If under warranty, initiate vendor RMA through supply chain |
| ShipOS crash / system halt | Spacecraft Systems Engineering | Collect diagnostic dump before reimaging |
| Software installation request | Spacecraft Systems Engineering | Must be on the approved software manifest |
| ShipOS MDM enrollment | Spacecraft Systems Engineering | New crew should be auto-enrolled |
| Fabricator issues | Spacecraft Systems Engineering | Check if it’s a network fabricator (→ Deep Space Communications) or locally connected |
| Mobile device issues | Spacecraft Systems Engineering | Station-managed devices only |
| Slow workstation | Spacecraft Systems Engineering | Run hardware diagnostics first |

### Deep Space Communications

| Issue type | Route to | Notes |
|---|---|---|
| Subspace relay connectivity | Deep Space Communications | Check if crew’s credentials are expired first (→ Crew Identity if so) |
| Inter-deck comms mesh issues | Deep Space Communications | — |
| DNS beacon resolution failures | Deep Space Communications | — |
| Signal routing rule requests | Deep Space Communications | Requires security approval from Threat Response Command |
| Bandwidth / latency | Deep Space Communications | Get specific times and affected services |
| Holodeck comm quality | Deep Space Communications | If it’s a Mission Suite-specific issue, try Mission Software Operations first |

### Mission Software Operations

| Issue type | Route to | Notes |
|---|---|---|
| Navigation suite errors or access | Mission Software Operations | — |
| Sensor platform issues | Mission Software Operations | — |
| Astro-lab terminal | Mission Software Operations | Physical hardware issues go to Spacecraft Systems Engineering |
| Mission Suite issues | Mission Software Operations | Licensing issues specifically — general Mission Suite outages are Deep Space Communications |
| Internal tool bugs | Mission Software Operations | — |
| Application licensing | Mission Software Operations | — |

### Threat Response Command

| Issue type | Route to | Notes |
|---|---|---|
| Suspicious transmission received | Threat Response Command | Forward original signal to threats@cdss.space |
| Contamination / anomalous readings | Threat Response Command | Isolate affected section immediately |
| Data breach / unauthorized access | Threat Response Command | Mandatory P1 escalation |
| Security certificate issues | Threat Response Command | — |
| Containment protocol requests | Threat Response Command | — |

### Telemetry & Data Core

| Issue type | Route to | Notes |
|---|---|---|
| Sensor archive access | Telemetry & Data Core | — |
| Crew file store sync issues | Telemetry & Data Core | Large dataset sync problems are common; check file count limits |
| Database access request | Telemetry & Data Core | Requires data owner approval |
| Backup / restore request | Telemetry & Data Core | — |
| Legacy data vault access | Telemetry & Data Core | Legacy data vaults only; new requests should use sensor archives |

---

## Known gaps in this guide

> **Lt. Mehta’s note:** The following areas still need to be sorted out. For now, use your best judgment or escalate to the Mission Ops Desk Lead. I’m working on getting the team leads to agree, but getting six department heads to align on ownership in deep space is like herding cats in zero-g.

- **Biometric verification issues** — Could be Crew Identity & Airlock Control (profile setup), Threat Response Command (policy enforcement), or Spacecraft Systems Engineering (scanner hardware issues). We haven’t agreed on a single owner.
- **Mission Suite / collaboration issues** — Is it a Deep Space Communications issue (comms quality), Mission Software Operations issue (app crash), or Spacecraft Systems Engineering issue (display/audio hardware)? Depends on the symptoms.
- **Station Core infrastructure requests** — Compute allocation, VM requests, etc. Telemetry & Data Core handles some, but we don’t have a formal station infrastructure team yet.
- **Crew onboarding / offboarding** — Touches Crew Identity (profiles), Spacecraft Systems Engineering (hardware), Mission Software Operations (licenses), and Telemetry & Data Core (access). There’s a workflow for this but it’s manual and breaks constantly.
- **Fabricator and scanning** — Network fabricators are Deep Space Communications, locally connected fabricators are Spacecraft Systems Engineering, scan-to-archive failures could be either.

---

## Escalation rules

1. **P1 signals** — Must be acknowledged within 15 minutes. If the assigned team doesn’t acknowledge, auto-escalate to Mission Ops Desk Lead. In space, 15 minutes can be the difference between a close call and a casualty report.
2. **Containment incidents** — Always route to Threat Response Command. If it also affects another team’s domain (e.g., compromised crew profile = Crew Identity + Threat Response), route to Threat Response Command as primary and Crew Identity & Airlock Control as secondary.
3. **Command staff signals** — Station Commander and department heads’ signals are auto-flagged. Treat as one priority level higher than normal assessment.
4. **Repeat signals** — If the same reporter has filed 3+ signals in 7 days for the same issue, escalate to the team lead for root cause investigation. Recurring anomalies in space tend to get worse, not better.
