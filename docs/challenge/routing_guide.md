# Contoso Deep Space Station — Internal Signal Routing Protocol

> **Last updated:** Stardate 2025.195
> **Author:** Lt. Raj Mehta, Mission Control Shift Manager
> **Status:** DRAFT — some sections still being finalized after the Q2 division reorg

---

## How to use this protocol

When a signal comes in, identify the **anomaly type** from the table below and route to the listed **owning division**. If you're unsure, escalate to the Shift Commander.

## Priority Definitions

| Priority | Label | Response SLA | Resolution SLA | When to use |
|---|---|---|---|---|
| P1 | 🔴 Red Alert | 15 min | 4 hours | Life support failure, hull breach, hostile contact, crew medical emergency, active containment breach |
| P2 | 🟡 Yellow Alert | 1 hour | 8 hours | Significant mission impact but not immediate danger; time-sensitive maneuvers, security anomalies, science windows at risk |
| P3 | 🟠 Caution | 4 hours | 3 business days | Standard anomalies with workarounds, non-urgent maintenance, single crew member blocked but non-urgent |
| P4 | 🟢 Routine | 1 business day | 10 business days | Informational queries, cosmetic issues, feature requests, general questions |

**Override rule:** Any signal mentioning potential hull breach, unidentified contact, or containment protocol violation is automatically **P1** regardless of other factors. Judge by IMPACT, not by the sender's label.

---

## Routing Table

### Crew Identity & Airlock Control

| Anomaly type | Route to | Notes |
|---|---|---|
| Biometric reset | Crew Identity & Airlock Control | Self-service portal handles most; only escalate if self-service fails |
| Crew lockout | Crew Identity & Airlock Control | Check for unauthorized access indicators first — if suspicious, also alert Threat Response |
| New crew provisioning | Crew Identity & Airlock Control | Requires command officer approval in Mission Control |
| SSO not working | Crew Identity & Airlock Control | Verify the app is in the crew identity database first |
| Identity sync issues | Crew Identity & Airlock Control | Usually crew database replication related |
| Service account requests | Crew Identity & Airlock Control | Requires security review before provisioning |

### Spacecraft Systems Engineering

| Anomaly type | Route to | Notes |
|---|---|---|
| Hull panel failure | Spacecraft Systems Engineering | If under warranty, initiate manufacturer RMA |
| Module crash / reboot loop | Spacecraft Systems Engineering | Collect diagnostic dump before reflashing |
| Equipment installation request | Spacecraft Systems Engineering | Must be on the approved hardware list |
| Docking port enrollment | Spacecraft Systems Engineering | New docking berths should be auto-enrolled |
| Solar panel issues | Spacecraft Systems Engineering | Check if it's array-connected (→ Deep Space Comms) or module-connected |
| Personal module device issues | Spacecraft Systems Engineering | Station-issued devices only |
| Slow console | Spacecraft Systems Engineering | Run hardware diagnostics first |

### Deep Space Communications

| Anomaly type | Route to | Notes |
|---|---|---|
| Subspace relay connectivity | Deep Space Communications | Check if crew credentials are expired first (→ Crew Identity if so) |
| Habitat Wi-Fi issues | Deep Space Communications | — |
| Signal resolution failures | Deep Space Communications | — |
| Comm filter rule requests | Deep Space Communications | Requires security approval from Threat Response |
| Bandwidth / latency | Deep Space Communications | Get specific stardates and affected subsystems |
| Holodeck comm quality | Deep Space Communications | If it's a flight-software-specific issue, try Mission Software first |

### Mission Software Operations

| Anomaly type | Route to | Notes |
|---|---|---|
| Navigation plotter errors | Mission Software Operations | — |
| Science instrument issues | Mission Software Operations | — |
| Star chart terminal | Mission Software Operations | Physical hardware issues go to Spacecraft Systems Engineering |
| Mission planning software | Mission Software Operations | Licensing issues specifically — general outages are Deep Space Comms |
| Internal station app bugs | Mission Software Operations | — |
| Software licensing | Mission Software Operations | — |

### Threat Response Command

| Anomaly type | Route to | Notes |
|---|---|---|
| Suspicious transmission received | Threat Response Command | Forward original signal data to threats@contoso.com |
| Anomalous object / hostile contact | Threat Response Command | Initiate containment protocol immediately |
| Data breach / unauthorized access | Threat Response Command | Mandatory P1 escalation |
| Encryption certificate issues | Threat Response Command | — |
| Compliance / audit requests | Threat Response Command | — |

### Telemetry & Data Core

| Anomaly type | Route to | Notes |
|---|---|---|
| Data bank access | Telemetry & Data Core | — |
| Sensor sync issues | Telemetry & Data Core | Large telemetry sync problems are common; check data volume limits |
| Database access request | Telemetry & Data Core | Requires data owner approval |
| Backup / restore request | Telemetry & Data Core | — |
| Legacy data bank access | Telemetry & Data Core | Legacy local data banks only; new requests should use cloud storage |

---

## Known gaps in this protocol

> **Lt. Mehta's note:** The following areas still need to be sorted out. For now, use your best judgment or escalate to the Shift Commander.

- **Biometric scanner failures** — Could be Crew Identity (profile setup), Threat Response (security policy enforcement), or Spacecraft Systems Engineering (scanner hardware). We haven't agreed on a single owner.
- **Holodeck / recreation issues** — Is it a Deep Space Comms issue (signal quality), Mission Software issue (holodeck program crash), or Spacecraft Systems issue (projector/emitter hardware)? Depends on the symptoms.
- **Cloud infrastructure requests** — Azure compute access, VM requests, etc. Telemetry & Data Core handles some, but we don't have a formal cloud ops division yet.
- **Crew onboarding / departure** — Touches Crew Identity (profiles), Spacecraft Systems (hardware), Mission Software (licenses), and Telemetry (data access). There's a workflow for this but it's manual and breaks constantly.
- **Fabricator and recycler units** — Station-networked fabricators are Deep Space Comms, module-connected recyclers are Spacecraft Systems, scan-to-database failures could be either.

---

## Escalation rules

1. **P1 signals** — Must be acknowledged within 15 minutes. If the assigned division doesn't acknowledge, auto-escalate to the Shift Commander.
2. **Threat incidents** — Always route to Threat Response Command. If it also affects another division's domain (e.g., compromised biometrics = Crew Identity + Threat Response), route to Threat Response as primary and Crew Identity as secondary.
3. **VIP signals** — Command crew and Admiral+ signals are auto-flagged. Treat as one priority level higher than normal assessment.
4. **Repeat signals** — If the same crew member has filed 3+ signals in 7 days for the same anomaly, escalate to the division lead for root cause investigation.
