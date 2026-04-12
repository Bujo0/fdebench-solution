# Customer Brief

> Operational memo from the Contoso Deep Space Station (CDSS) — shared with the FDE team during discovery.

---

**From:** Commander Priya Kapoor, Mission Ops Director, Contoso Deep Space Station
**To:** Microsoft FDE Team
**Date:** March 2026
**Subject:** Help us fix our signal triage — we're drowning out here

---

## Who we are

Contoso Deep Space Station. ~2,000 crew orbiting at the edge of known space across 3 station sectors (Command Deck, Research Ring, Engineering Bay). We run deep space operations, scientific research, and spacecraft engineering. Heavily regulated by Interstellar Safety Command — compliance matters, system downtime can be life-threatening, and our crew does not have the patience for slow ops when they're dodging micrometeorites.

## What's broken

Our Mission Ops team handles ~180 incoming signals per day — anomaly reports, system alerts, crew requests, you name it. Right now, a human Mission Ops operator reads every signal, decides what it is, assigns a priority, and routes it to one of our 6 specialist teams. It takes **3.4 hours on average** to get a signal to the right team. That's before anyone even starts working on it. Out here, 3.4 hours can mean the difference between a minor hull patch and a catastrophic decompression event.

**42% of signals get misrouted at least once.** When a signal lands with the wrong team, they bounce it back, and we start over. Some signals take 2-3 bounces before they reach the right division. Meanwhile, Deck 7 is venting atmosphere and everyone's pointing fingers.

The worst part: our Mission Ops operators spend so much time triaging that they can't do actual resolution work. They're basically expensive human signal routers floating in zero-G.

## What we want

We want to **automate first-pass triage** for every incoming signal. Specifically:

1. **Classify** the signal into the right category — what kind of anomaly or request is this?
2. **Set priority** — how urgent is this, really? (Crew members flag "CRITICAL" on everything, including broken coffee dispensers.)
3. **Route** to the correct specialist team — get it right the first time
4. **Flag what's missing** — half our signals don't include basic info we need. We waste time pinging the reporter back over subspace to ask "which system?" or "what error code?"
5. **Give our Mission Ops team a head start on remediation** — even if a human still resolves the issue, tell them what to try first before suiting up

## Our teams

We have 6 specialist operations teams:

| Team | What they handle |
|---|---|
| **Crew Identity & Airlock Control** | Login issues, SSO, MFA, crew provisioning, Entra ID, biometric directory sync, airlock access codes |
| **Spacecraft Systems Engineering** | Workstation terminals, mobile consoles, OS issues, Intune device management, peripheral hardware |
| **Deep Space Communications** | Subspace relay links, local mesh WiFi, DNS, firewall rules, proxy, WAN/LAN, inter-deck and inter-ship connectivity |
| **Mission Software Operations** | Mission-critical apps (SAP logistics, Salesforce crew services, deep space scanner terminals, internal tools), licensing, integrations |
| **Threat Response Command** | Phishing attempts, malware, suspicious signal activity, data exfiltration, compliance incidents, certificate management |
| **Telemetry & Data Core** | Databases, file shares, OneDrive/SharePoint, backup systems, data access requests, ETL pipelines, sensor telemetry streams |

I've attached our **internal routing guide** — but fair warning, it was written 8 months ago and some things have changed. We've reorganized divisions since the last crew rotation. About 20% of signal types aren't covered in it, and some of the routing rules overlap between teams. My team leads argue about ownership constantly. For example: who handles MFA lockouts — Crew Identity or Threat Response? Depends on whether someone fat-fingered their retinal scan or we have an actual intruder. Honestly, we're not consistent about it ourselves.

## What "good" looks like to us

- **Reduce misrouting from 42% to under 15%** in the first month
- **Time-to-route under 5 minutes** (from 3.4 hours)
- **Catch missing information proactively** so we stop playing subspace ping-pong with reporters three sectors away
- **Actionable remediation steps** — not generic "investigate the anomaly" but specific things an operator can actually try before escalating to EVA

If you can show me this working on even 50 of our real signals, I can make the business case to our Fleet Admiral.

## Things you should know

- Our signals come in through **4 channels**: subspace relay, holodeck comm (Teams), the bridge terminal self-service portal, and emergency beacon (transcribed by our comms center AI). Quality varies wildly. Subspace relays tend to be longer and more detailed. Holodeck comms are short and missing context. Emergency beacon transcriptions are garbled at best.
- **Some signals aren't real incidents** — we get auto-acknowledgments, "thanks" replies, crew out-of-station notifications, and occasional subspace spam from passing freighters. Our system doesn't filter these before routing.
- **We use Microsoft's station systems stack**: Entra ID for crew identity, Intune for device management, Microsoft 365 for collaboration, Azure for our core infrastructure. Most of our compute runs on Azure orbital nodes. We recently deployed Defender for Endpoint across all terminals. We still have some legacy on-station systems (SAP logistics, a few local data servers that survived the last solar flare).
- **Priority is subjective**: Crew over-escalate constantly. "CRITICAL" in the signal header usually isn't. But sometimes a quiet report like "slight vibration in docking ring 4" is actually a hull breach in progress. Context matters more than keywords out here.
- **Compliance signals are special**: Anything involving potential data breach, regulatory inquiry from Interstellar Safety Command, or audit findings must be escalated to Threat Response Command immediately, regardless of category. Getting this wrong has consequences — and at this altitude, "consequences" can mean losing your oxygen privileges.

## One more thing

I don't need a chatbot. I don't need a holographic dashboard. I need **an API I can plug into our Mission Ops workflow** that returns a JSON decision for each signal. Fast, reliable, and right most of the time. If it's not sure, it should say so — we'd rather flag uncertainty than misroute a hull breach report to the coffee machine repair queue.

— Commander Kapoor, signing off from the edge of known space
