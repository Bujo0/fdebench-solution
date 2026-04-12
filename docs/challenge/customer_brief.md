# Mission Brief

> Internal transmission from Contoso Deep Space Station (CDSS) — shared with the FDE Mission Support Team during discovery.

---

**From:** Commander Priya Kapoor, Station Operations Chief, Contoso Deep Space Station
**To:** FDE Mission Support Team
**Date:** March 2026
**Subject:** Help us fix our signal triage — crew survival depends on it

---

## Who we are

Contoso Deep Space Station (CDSS). ~2,000 crew across 12 decks, parked 0.3 AU from Earth. We run deep space research, stellar cartography, and long-range exploration support. This is deep space where mistakes cost lives — containment protocols matter, system downtime can be fatal, and our crew does not have the luxury of patience when the atmospheric processor is acting up.

## What’s broken

Our mission ops team handles ~180 signals per day. Right now, a human ops officer reads every incoming signal, decides what it is, assigns a priority, and routes it to one of our 6 specialist teams. It takes **3.4 hours on average** to get a signal to the right team. That’s before anyone even starts working on it. At 0.3 AU from Earth, 3.4 hours is the difference between a contained anomaly and a hull breach that vents Deck 9.

**42% of signals get misrouted at least once.** When a signal lands with the wrong team, they bounce it back, and we start over. Some signals take 2–3 bounces before they reach the right crew. Last month, a contamination alert bounced between Spacecraft Systems and Deep Space Comms for six hours. Six. Hours.

The worst part: our ops officers spend so much time triaging that they can’t do actual resolution work. They’re basically expensive human routers floating in space.

## What we want

We want to **automate first-pass triage** for every incoming signal. Specifically:

1. **Classify** the signal into the right category — what kind of anomaly is this?
2. **Set priority** — how urgent is this, really? (Crew write “URGENT” on everything. Even lunch menu complaints.)
3. **Route** to the correct specialist team — get it right the first time, because the second time might be too late
4. **Flag what’s missing** — half our signals don’t include basic info we need. We waste time pinging the reporter back to ask “which subsystem?” or “what was the anomaly readout?”
5. **Give our ops team a head start on remediation** — even if a human still resolves the signal, tell them what to try first

## Our teams

We have 6 specialist operations teams:

| Team | What they handle |
|---|---|
| **Crew Identity & Airlock Control** | Biometric access, crew identity, profile provisioning, BioScan ID, directory sync |
| **Spacecraft Systems Engineering** | Workstations, hull-mounted systems, mobile devices, ShipOS issues, ShipOS MDM, peripherals |
| **Deep Space Communications** | Subspace relay, local comms mesh, DNS beacons, signal routing, proxy, inter-deck links |
| **Mission Software Operations** | Mission apps (navigation suite, sensor platforms, astro-lab tools, internal tools), licensing, integrations |
| **Threat Response Command** | Hostile contact, contamination, anomalous readings, data breaches, containment protocol incidents, certificate management |
| **Telemetry & Data Core** | Databases, crew file stores, sensor archives, backups, data access requests, telemetry pipelines |

I’ve attached our **internal routing guide** — but fair warning, it was written 8 months ago and some things have changed. We’ve also reorganized since the Q2 crew rotation. About 20% of signal types aren’t covered in it, and some of the routing rules overlap between teams. My team leads argue about ownership constantly. For example: who handles biometric scan failures — Crew Identity or Threat Response? Depends on the context, and honestly we’re not consistent about it ourselves.

## What “good” looks like to us

- **Reduce misrouting from 42% to under 15%** in the first month
- **Time-to-route under 5 minutes** (from 3.4 hours — in space, hours matter)
- **Catch missing information proactively** so we stop playing subspace ping-pong with reporters
- **Actionable remediation steps** — not generic “investigate the anomaly” but specific things an ops officer can actually try before someone freezes to death

If you can show me this working on even 50 of our real signals, I can make the case to Station Command.

## Things you should know

- Our signals come in through **4 channels**: subspace relay (long-form reports), holodeck comm (quick crew chatter), the bridge terminal (self-service kiosk), and emergency beacon (transcribed by ops — usually panicked and garbled). Quality varies wildly. Subspace relay signals tend to be longer. Holodeck comms are short and missing context. Emergency beacon transcriptions are messy.
- **Some signals aren’t real incidents** — we get auto-replies, “thanks” messages, out-of-rotation notices, and occasional junk transmissions. Our system doesn’t filter these before routing.
- **We run a unified station stack**: BioScan ID (biometric identity system), ShipOS MDM (shipboard device management), Mission Suite (comms, planning, docs), Station Core (compute/storage cluster). Most of our infrastructure runs on Station Core. We recently deployed SentinelGrid (threat detection). We still have some legacy modules — like the legacy atmospheric processors from the original build and a few isolated data vaults that predate the station refit.
- **Priority is subjective**: Crew over-escalate constantly. “URGENT” in the subject usually isn’t. But sometimes a quiet signal like “slight fluctuation in oxygen recycler output” is actually Red Alert material. Context matters more than keywords.
- **Containment protocol signals are special**: Any signal mentioning hull breach, biological contamination, or hostile contact must be escalated to Threat Response Command immediately, regardless of category. Getting this wrong has consequences. Fatal ones.

## One more thing

I don’t need a chatbot. I don’t need a holographic dashboard. I need **an API I can plug into our existing station operations workflow** that returns a JSON decision for each signal. Fast, reliable, and right most of the time. If it’s not sure, it should say so. People’s lives are on the line.

— Commander Kapoor
