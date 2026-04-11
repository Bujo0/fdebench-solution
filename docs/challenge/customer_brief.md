# Mission Briefing

> Internal transmission from Contoso Deep Space Station (CDSS) — shared with the FDE team during discovery.

---

**From:** Commander Priya Kapoor, Station Commander, Contoso Deep Space Station
**To:** Microsoft FDE Team
**Date:** Stardate 2026.074
**Subject:** Help us fix our signal triage — we're drowning out here

---

## Who we are

Contoso Deep Space Station. ~2,000 crew across 3 habitat rings (Alpha Ring, Beta Ring, Gamma Ring). We run deep-space exploration, orbital research, and diplomatic outpost operations. Regulated by the Interstellar Safety Directorate — compliance matters, hull breaches are expensive, and our people are impatient. Especially the ones floating in zero-G.

## What's broken

Our Mission Control team handles ~180 incoming signals per day. Right now, a human Tier 1 controller reads every signal, decides what it is, assigns a priority, and routes it to one of our 6 response divisions. It takes **3.4 hours on average** to get a signal to the right division. That's before anyone even starts working on it.

**42% of signals get misrouted at least once.** When a signal lands with the wrong division, they bounce it back, and we start over. Some signals take 2-3 bounces before they reach the right place. In deep space, a 3-hour delay on a hull breach signal isn't an inconvenience — it's a coffin.

The worst part: our Tier 1 controllers spend so much time triaging that they can't do actual resolution work. They're basically expensive human routers.

## What we want

We want to **automate first-pass triage** for every incoming signal. Specifically:

1. **Classify** the signal into the right anomaly category — what kind of issue is this?
2. **Set priority** — how urgent is this, really? (Crew members write "URGENT" on everything. The ensign who spilled coffee on their console is not a Red Alert.)
3. **Route** to the correct response division — get it right the first time
4. **Flag what's missing** — half our signals don't include basic info we need. We waste time going back to the reporter to ask "which subsystem?" or "what readout?"
5. **Give our Tier 1 team a head start on remediation** — even if a crew member still resolves the issue, tell them what to try first

## Our divisions

We have 6 specialist response divisions:

| Division | What they handle |
|---|---|
| **Crew Identity & Airlock Control** | Biometric access, SSO, MFA, crew profile provisioning, identity database, airlock authorization |
| **Spacecraft Systems Engineering** | Hull integrity, docking ports, solar panels, structural systems, radiation shielding, module hardware |
| **Deep Space Communications** | Subspace relays, antenna alignment, navigation, signal latency, comms blackouts, deep-space routing |
| **Mission Software Operations** | Flight planning tools, science instruments, mission software, licensing, payload integrations |
| **Threat Response Command** | Unidentified objects, radiation spikes, hostile contacts, containment breaches, anomalous readings, quarantine |
| **Telemetry & Data Core** | Telemetry pipelines, sensor databases, scientific data, backups, data access requests, ETL pipelines |

I've attached our **internal routing protocol** — but fair warning, it was written 8 months ago and some things have changed since the last station reorganization. About 20% of signal types aren't covered in it, and some of the routing rules overlap between divisions. My division leads argue about ownership constantly. For example: who handles biometric scanner failures — Crew Identity or Threat Response? Depends on the context, and honestly we're not consistent about it ourselves.

## What "good" looks like to us

- **Reduce misrouting from 42% to under 15%** in the first month
- **Time-to-route under 5 minutes** (from 3.4 hours)
- **Catch missing information proactively** so we stop playing subspace ping-pong with reporters
- **Actionable remediation steps** — not generic "investigate the anomaly" but specific things a Tier 1 controller can actually try

If you can show me this working on even 50 of our real signals, I can make the case to the Admiralty.

## Things you should know

- Our signals come in through **4 channels**: subspace relay, holodeck comms (crew quarters recreational terminals), the bridge terminal (self-service portal), and emergency beacons (transcribed by ops). Quality varies wildly. Subspace relay signals tend to be longer. Holodeck comms are short and missing context. Emergency beacon transcriptions are messy.
- **Some signals aren't real anomalies** — we get automated beacon echoes, "acknowledged" messages, routine acknowledgments, and occasional interference patterns. Our system doesn't filter these before routing.
- **We use Microsoft's stack**: Entra ID for crew identity, Intune for device management, Azure for all our compute. We recently deployed Defender for Endpoint across all workstations. We still have some legacy on-station systems (navigation core v3, a few local data banks).
- **Priority is subjective**: Crew members over-escalate constantly. "RED ALERT" in the subject usually isn't. But sometimes a quiet signal like "slight delay in thruster response" is actually life-threatening. Context matters more than keywords.
- **Containment signals are special**: Anything involving potential hull breach, unidentified contacts, or quarantine protocol must be escalated to Threat Response Command immediately, regardless of category. Getting this wrong has consequences. The kind where people float into the vacuum.

## One more thing

I don't need a chatbot. I don't need a holographic dashboard. I need **an API I can plug into our existing Mission Control workflow** that returns a JSON decision for each signal. Fast, reliable, and right most of the time. If it's not sure, it should say so.

— Commander Kapoor
