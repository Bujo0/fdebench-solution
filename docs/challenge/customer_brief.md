# Mission Briefing

> Classified transmission from Contoso Deep Space Station — shared with the FDE team during first contact.

---

**From:** Admiral Priya Kapoor, Station Commander, Contoso Deep Space Station (CDSS)
**To:** Microsoft FDE Team
**Stardate:** March 2426
**Subject:** Help us fix our signal triage — we're drowning in noise

---

## Who we are

Contoso Deep Space Station (CDSS). ~2,000 crew across 3 station sectors (Alpha Ring, Beta Ring, Gamma Ring). We run deep space exploration, resource mining, and scientific research. Hostile territory — protocol compliance matters, downtime can be fatal, and our crew is impatient.

## What's broken

Our Mission Ops team handles ~180 signals per cycle. Right now, a human operator reads every signal, decides what it is, assigns a priority, and routes it to one of our 6 response divisions. It takes **3.4 hours on average** to get a signal to the right division. That's before anyone even starts working on it.

**42% of signals get misrouted at least once.** When a signal lands with the wrong division, they bounce it back, and we start over. Some signals take 2-3 bounces before they reach the right place.

The worst part: our Mission Ops operators spend so much time triaging that they can't do actual resolution work. They're basically expensive human signal routers.

## What we want

We want to **automate first-pass triage** for every incoming signal. Specifically:

1. **Classify** the signal into the right category — what kind of anomaly is this?
2. **Set priority** — how urgent is this, really? (Crew members flag "RED ALERT" on everything.)
3. **Route** to the correct response division — get it right the first time
4. **Flag what's missing** — half our signals don't include basic info we need. We waste time pinging the reporter back to ask "which subsystem?" or "what anomaly readout?"
5. **Give our Mission Ops team a head start on remediation** — even if a human still resolves the signal, tell them what to try first

## Our response divisions

We have 6 specialist response divisions:

| Division | What they handle |
|---|---|
| **Crew Identity & Airlock Control** | Biometric auth, airlock access, crew provisioning, Station Identity Core, directory sync |
| **Spacecraft Systems Engineering** | Hull integrity, life support, habitat modules, ShipOS, fabricators, docking bays |
| **Deep Space Communications** | Subspace relays, antenna arrays, navigation beacons, signal routing, mesh network connectivity |
| **Mission Software Operations** | Mission apps (Station Resource Manager, OrbitalForce, Quantum Terminal, internal tools), licensing, integrations |
| **Threat Response Command** | Phishing transmissions, hostile code, containment breaches, protocol violations, quarantine, threat management |
| **Telemetry & Data Core** | Sensor data, telemetry streams, data vaults, backups, mission archives, data access requests |

I've attached our **internal signal routing protocol** — but fair warning, it was written 8 months ago and some things have changed. We've also reorganized since then. About 20% of signal types aren't covered in it, and some of the routing rules overlap between divisions. My division leads argue about ownership constantly. For example: who handles biometric anomalies — Crew Identity or Threat Response? Depends on the context, and honestly we're not consistent about it ourselves.

## What "good" looks like to us

- **Reduce misrouting from 42% to under 15%** in the first cycle
- **Time-to-route under 5 minutes** (from 3.4 hours)
- **Catch missing information proactively** so we stop playing subspace ping-pong with reporters
- **Actionable remediation steps** — not generic "investigate the anomaly" but specific things an operator can actually try

If you can show me this working on even 50 of our real signals, I can make the case to Fleet Command.

## Things you should know

- Our signals come in through **4 channels**: subspace relay, holodeck comms, the bridge terminal, and emergency beacon (auto-transcribed by our comms array). Quality varies wildly. Subspace relay signals tend to be longer. Holodeck comms are short and missing context. Emergency beacon transcriptions are messy.
- **Some signals aren't real incidents** — we get automated echoes, "acknowledged" messages, cryo-sleep auto-replies, and occasional space noise. Our system doesn't filter these before routing.
- **We run on a unified stack**: Station Identity Core, ShipGuard, StarSuite 365, Azure Orbital. Most of our infrastructure is on Azure Orbital. We recently deployed Defender for Deep Space. We still have some legacy onboard systems (Station Resource Manager, a few local data vaults).
- **Priority is subjective**: Crew over-escalate constantly. "RED ALERT" in the title usually isn't. But sometimes a quiet signal like "slight variance in reactor harmonic frequency" is actually critical. Context matters more than keywords.
- **Containment signals are special**: Anything involving potential hull breach, hostile contact, or quarantine protocol must be escalated to Threat Response Command immediately, regardless of category. Getting this wrong has consequences. Out here, consequences are measured in lives.

## One more thing

I don't need a holographic assistant. I don't need a dashboard. I need **an API I can plug into our existing MissionFlow workflow** that returns a JSON decision for each signal. Fast, reliable, and right most of the time. If it's not sure, it should say so.

— Admiral Kapoor
