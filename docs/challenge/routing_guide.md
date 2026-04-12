# CDSS Mission Ops — Internal Signal Routing Guide

> **Last updated:** July 2025
> **Author:** Chief Signal Officer Raj Mehta
> **Status:** DRAFT — some sections still being finalized after the Q2 crew rotation. If you were expecting a polished document, I regret to inform you that we had a containment breach in Exobiology during the reorg and three cat specimens escaped. We caught two. The third one adapted. It's a long story.

---

## How to use this guide

When a signal comes in, identify the **issue type** from the table below and route to the listed **owning team**. If you're unsure, escalate to the Chief Signal Officer (that's me, and I will judge you, but at least the signal won't kill anyone).

## Priority Definitions

| Priority | Label | Response SLA | Resolution SLA | When to use |
|---|---|---|---|---|
| P1 | 🔴 Red Alert | 15 min | 4 hours | Hull breach, hostile contact in progress, life support failure, command-level emergency |
| P2 | 🟠 Yellow Alert | 1 hour | 8 hours | Major system failure, no workaround, multiple crew affected |
| P3 | 🔵 Standard Ops | 4 hours | 3 cycles | Impact with workaround available, single crew member affected but non-urgent |
| P4 | 🟢 Routine | 1 cycle | 10 cycles | Minor annoyance, cosmetic issue, feature request, general question |

**Override rule:** Any signal mentioning potential hull breach, atmospheric compromise, or containment failure is automatically **P1** regardless of other factors. I don't care if it's phrased politely. I don't care if it says "no rush." If the word "decompression" appears anywhere in the signal, it's a Red Alert. We learned this the hard way. See: Deck 4 corridor incident, January 2026.

---

## Routing Table

### Crew Identity & Airlock Control

| Issue type | Route to | Notes |
|---|---|---|
| Biometric reset | Crew Identity & Airlock Control | Self-service kiosk handles most; only escalate if biometric recalibration fails |
| Account lockout | Crew Identity & Airlock Control | Check for brute-force indicators first — if suspicious, also alert Threat Response. *Mehta's note: Three lockouts from the same airlock in one shift is not a coincidence. It's either a break-in attempt or Ensign Torres forgetting his clearance code again. Either way, flag it.* |
| New crew provisioning | Crew Identity & Airlock Control | Requires section chief approval via bridge terminal |
| SSO not working | Crew Identity & Airlock Control | Verify the system is registered in the BioScan ID directory first |
| Directory sync issues | Crew Identity & Airlock Control | Usually BioScan ID replication lag — check the sync queue before panicking |
| Service account requests | Crew Identity & Airlock Control | Requires Threat Response review before provisioning. *Mehta's note: Yes, even for the coffee machine. Especially for the coffee machine. The nutrient synthesizer incident started with an unreviewed service account.* |

### Spacecraft Systems Engineering

| Issue type | Route to | Notes |
|---|---|---|
| Workstation hardware failure | Spacecraft Systems Engineering | If under warranty, initiate manufacturer return — good luck getting a courier at 0.3 AU |
| OS crash / system fault | Spacecraft Systems Engineering | Collect diagnostic dump before reimaging. *Mehta's note: "It just stopped working" is not a diagnostic dump.* |
| Software installation request | Spacecraft Systems Engineering | Must be on the approved software manifest |
| ShipOS MDM enrollment | Spacecraft Systems Engineering | New crew should be auto-enrolled on arrival. If they weren't, check if they came in on the supply shuttle — those systems don't always sync. |
| Fabricator issues | Spacecraft Systems Engineering | Check if it's a networked fabricator (→ Deep Space Comms) or locally connected. *Mehta's note: The Deck 3 fabricator has been printing everything 2mm too thick since March. It's a known issue. It's always been a known issue. It will always be a known issue.* |
| Mobile module issues | Spacecraft Systems Engineering | Station-managed modules only |
| Slow workstation | Spacecraft Systems Engineering | Run hardware diagnostics first. In zero-g, "slow" is relative — if the crew member's workstation is literally floating away, that's Spacecraft Systems, but it's a different form. |

### Deep Space Communications

| Issue type | Route to | Notes |
|---|---|---|
| Subspace relay connectivity | Deep Space Communications | Check if crew's credentials are expired first (→ Crew Identity if so). *Mehta's note: 60% of "comms down" signals are expired credentials. I have started a tally. It brings me no joy.* |
| Local comms mesh issues | Deep Space Communications | — |
| DNS beacon failures | Deep Space Communications | — |
| Signal routing proxy requests | Deep Space Communications | Requires Threat Response approval |
| Bandwidth / latency | Deep Space Communications | Get specific stardates and affected services. "It's been slow" is not actionable at 0.3 AU. |
| SubComm call quality | Deep Space Communications | If it's a SubComm-app-specific issue, try Mission Software Ops first. *Mehta's note: If someone's holographic projection is flickering, it's comms. If their holographic projection looks like a Cubist painting, that's software. If they don't have a holographic projection at all, check if they're in a section with atmosphere first.* |

### Mission Software Operations

| Issue type | Route to | Notes |
|---|---|---|
| FlightOS errors or access | Mission Software Operations | — |
| Navigation suite issues | Mission Software Operations | *Mehta's note: If navigation is wrong, escalate to P1 immediately. We are in space. "Slightly off course" is not a P3.* |
| Sensor platform calibration | Mission Software Operations | Physical hardware issues go to Spacecraft Systems Engineering |
| Mission Suite issues | Mission Software Operations | Licensing issues specifically — general Mission Suite outages are Deep Space Comms |
| Internal tool bugs | Mission Software Operations | — |
| Application licensing | Mission Software Operations | — |

### Threat Response Command

| Issue type | Route to | Notes |
|---|---|---|
| Hostile signal received | Threat Response Command | Quarantine signal immediately in SentinelGrid. Do NOT open attachments. *Mehta's note: I cannot believe I have to write this, but do NOT open attachments from unknown vessels. Last time someone did, we spent 72 hours purging the environmental controls. The atmospheric processor on Deck 7 still smells like burnt toast and we're pretty sure it's related.* |
| Malware / suspicious activity | Threat Response Command | Isolate affected module from the network immediately |
| Data loss / unauthorized access | Threat Response Command | Mandatory P1 escalation. No exceptions. Not even if the Commander says it's fine. (The Commander will never say it's fine.) |
| Security certificate issues | Threat Response Command | — |
| Containment / audit requests | Threat Response Command | — |

### Telemetry & Data Core

| Issue type | Route to | Notes |
|---|---|---|
| Sensor archive access | Telemetry & Data Core | — |
| Crew file store sync issues | Telemetry & Data Core | Large dataset sync problems are common; check storage allocation limits. *Mehta's note: The Exobiology team is storing 4.7 TB of cat behavioral data. Yes, that cat. No, I don't know why.* |
| Database access request | Telemetry & Data Core | Requires data owner approval |
| Backup / restore request | Telemetry & Data Core | — |
| Legacy archive access | Telemetry & Data Core | Legacy sensor archives only; new data requests should use the standard sensor archive platform |

---

## Known gaps in this guide

> **Mehta's note:** The following areas still need to be sorted out. For now, use your best judgment or escalate to me. I will sigh audibly, but I will help you. That's more than Titan Outpost's ops lead did, and look what happened to them.

- **BioAuth panel issues** — Could be Crew Identity (biometric enrollment), Threat Response (access policy enforcement), or Spacecraft Systems (panel hardware malfunction). We haven't agreed on a single owner. We've had four meetings about this. The fourth meeting was interrupted by an actual BioAuth panel failure, which was ironic and unhelpful.
- **SubComm / collaboration issues** — Is it a Deep Space Comms issue (signal quality), Mission Software Ops issue (SubComm app crash), or Spacecraft Systems issue (headset/holographic projector)? Depends on the symptoms. *Mehta's note: If you can hear them but they sound like they're underwater, that's comms. If you can see them but they're upside down, that's software. If the holodeck is on fire, that's Spacecraft Systems and also a P1.*
- **Station Core compute requests** — Station Core allocation requests, container deployments, etc. Telemetry & Data Core handles some, but we don't have a formal station infrastructure ops team yet. We've been meaning to create one since before launch.
- **Crew onboarding / offboarding** — Touches Crew Identity (accounts), Spacecraft Systems (equipment), Mission Software Ops (licenses), and Telemetry & Data Core (data access). There's a workflow for this but it's manual and breaks constantly. Last rotation, three new crew members were given airlock access before they had atmosphere privileges. They were fine. Probably.
- **Fabricator and scanning** — Networked fabricators are Deep Space Comms, local fabricators are Spacecraft Systems, scan-to-archive failures could be either. The Deck 3 fabricator is always broken. Always. It's in the orientation guide now.

---

## Escalation rules

1. **P1 (🔴 Red Alert) signals** — Must be acknowledged within 15 minutes. If the assigned team doesn't acknowledge, auto-escalate to Chief Signal Officer. *Mehta's note: If I get woken up at 0300 station time because your team didn't acknowledge a Red Alert, we will have a conversation. It will not be a pleasant conversation. There will be no protein cubes.*
2. **Containment incidents** — Always route to Threat Response Command. If it also affects another team's domain (e.g., compromised crew identity = Crew Identity + Threat Response), route to Threat Response as primary and Crew Identity as secondary. The void of space does not wait for org chart debates.
3. **Command-level signals** — Commander and section chief+ signals are auto-flagged. Treat as one priority level higher than normal assessment. *Mehta's note: Commander Kapoor has never once filed a signal that wasn't genuinely urgent. If you see her name, move fast.*
4. **Repeat signals** — If the same crew member has filed 3+ signals in 7 days for the same issue, escalate to the section chief for root cause investigation. *Mehta's note: Exception — the atmospheric processor on Deck 7. That one's just like that. We all know. Move on.*
