# Mission Briefing

> Internal briefing from Contoso Deep Space Station (CDSS) — shared with the FDE team during discovery.

---

**From:** Admiral Chen, Admiral of Mission Operations, Contoso Deep Space Station (CDSS)
**To:** Microsoft FDE Team
**Date:** March 2026
**Subject:** Help us fix our signal triage — we're drowning out here

---

## Who we are

Contoso Deep Space Station — CDSS. ~450 crew members across 3 stations (Orbital Ring Alpha, Lunar Outpost Armstrong, Mars Station Olympus). We run astrogation, deep-space exploration, and interplanetary logistics. Regulated operations — compliance matters, downtime can be life-threatening, and our crew is impatient.

## What's broken

Our Mission Control Desk handles ~180 signals per day. Right now, a Mission Ops Analyst reads every signal, decides what it is, assigns a priority, and routes it to one of our 6 specialist divisions. It takes **3.4 hours on average** to get a signal to the right division. That's before anyone even starts working on it.

**42% of signals get misrouted at least once.** When a signal lands with the wrong division, they bounce it back, and we start over. Some signals take 2-3 bounces before they reach the right place.

The worst part: our Mission Ops Analysts spend so much time triaging that they can't do actual resolution work. They're basically expensive human routers.

## What we want

We want to **automate first-pass triage** for every incoming signal. Specifically:

1. **Classify** the signal into the right category — what kind of issue is this?
2. **Set priority** — how urgent is this, really? (Crew members write "URGENT" on everything.)
3. **Route** to the correct specialist division — get it right the first time
4. **Flag what's missing** — half our signals don't include basic info we need. We waste time going back to the reporter to ask "which subsystem?" or "what anomaly readout?"
5. **Give our Mission Ops team a head start on remediation** — even if a human still resolves the signal, tell them what to try first

## Our divisions

We have 6 specialist Mission Operations divisions:

| Division | What they handle |
|---|---|
| **Crew Identity & Airlock Control** | Crew login issues, SSO, biometric auth, account provisioning, Ship Identity Registry, registry sync |
| **Spacecraft Systems Engineering** | Hull modules, structural systems, mobile units, OS issues, Fleet Device Manager, airlocks |
| **Deep Space Communications** | Subspace relay links, comms arrays, nav beacons, signal routing rules, proxies, sector links, station connectivity |
| **Mission Software Operations** | Mission apps (ATLAS Cargo System, HERMES Trade System, ORION Market Terminal, internal tools), licensing, integrations |
| **Threat Response Command** | Hostile contacts, malware, suspicious activity, data breaches, compliance incidents, certificate management |
| **Telemetry & Data Core** | Databases, data archives, PersonalVault/DataVault, backups, data access requests, ETL pipelines |

I've attached our **internal routing guide** — but fair warning, it was written 8 months ago and some things have changed. We've also reorganized since then. About 20% of signal types aren't covered in it, and some of the routing rules overlap between divisions. My division leads argue about ownership constantly. For example: who handles biometric scanner issues — Crew Identity or Threat Response? Depends on the context, and honestly we're not consistent about it ourselves.

## What "good" looks like to us

- **Reduce misrouting from 42% to under 15%** in the first month
- **Time-to-route under 5 minutes** (from 3.4 hours)
- **Catch missing information proactively** so we stop playing comms ping-pong with reporters
- **Actionable remediation steps** — not generic "investigate the issue" but specific things a Mission Ops Analyst can actually try

If you can show me this working on even 50 of our real signals, I can make the case to our Station Commander.

## Things you should know

- Our signals come in through **4 channels**: subspace relay, holodeck comm (HoloComm), the bridge terminal, and emergency beacon (transcribed by our comms center). Quality varies wildly. Subspace relay signals tend to be longer. Holodeck comm signals are short and missing context. Emergency beacon transcriptions are messy.
- **Some signals aren't real incidents** — we get auto-replies, "thanks" messages, out-of-office notifications, and occasional spam. Our system doesn't filter these before routing.
- **We use Microsoft's stack**: Ship Identity Registry, Fleet Device Manager, Mission Suite, Orbital Platform. Most of our infrastructure is on Orbital Platform. We recently moved to AEGIS Defense System for endpoint protection. We still have some legacy on-station systems (ATLAS Cargo System, a few local data servers).
- **Priority is subjective**: Crew members over-escalate constantly. "URGENT" in the title usually isn't. But sometimes a quiet signal like "slight anomaly in reactor cooling loop" is actually critical. Context matters more than keywords.
- **Compliance signals are special**: Anything involving potential data breach, regulatory inquiry, or audit findings must be escalated to Threat Response Command immediately, regardless of category. Getting this wrong has consequences.

## One more thing

I don't need a chatbot. I don't need a dashboard. I need **an API I can plug into our existing Mission Control System workflow** that returns a JSON decision for each signal. Fast, reliable, and right most of the time. If it's not sure, it should say so.

— Admiral Chen
