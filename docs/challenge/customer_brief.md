# Mission Briefing

> ⚡ PRIORITY TRANSMISSION — Contoso Deep Space Station (CDSS) — Relayed to FDE Mission Support Team via subspace channel 7.

---

**From:** Commander Priya Kapoor, Station Operations Chief, Contoso Deep Space Station
**To:** Microsoft FDE Mission Support Team
**Stardate:** March 2026
**Subject:** Help us fix our signal triage — people are going to die

---

## Who we are

Contoso Deep Space Station. ~2,000 crew aboard a research outpost parked 0.3 AU from Earth. We run deep-space sensor arrays, exobiology research, long-range communications relay, and a surprisingly competitive zero-gravity cricket league. Regulated by Terran Space Authority — containment protocols matter, hull breaches are expensive, and our crew are impatient (especially the ones who haven't had correctly flavored protein cubes in six weeks).

## What's broken

Our Mission Ops desk handles ~180 signals per day. Right now, a human Tier 1 ops controller reads every signal, decides what it is, assigns a priority, and routes it to one of our 6 specialist teams. It takes **3.4 hours on average** to get a signal to the right team. That's before anyone even starts working on it.

In space, 3.4 hours is the difference between "minor atmospheric imbalance" and "Deck 7 is now a vacuum."

**42% of signals get misrouted at least once.** When a signal lands with the wrong team, they bounce it back, and we start over. Some signals take 2-3 bounces before they reach the right place. Every bounce adds a 4-minute light delay for confirmation. I have done the math. It is not good math.

The worst part: our Tier 1 controllers spend so much time triaging that they can't do actual resolution work. They're basically expensive human routers. I could replace them with a particularly motivated houseplant — and we actually have one of those, because three specimens escaped from the Exobiology Lab during Q2 crew rotation, we caught two, and the third adapted. It lives in the hydroponics bay now. It does not route signals, but it has better judgment than some of my crew.

## What we want

We want to **automate first-pass triage** for every incoming signal. Specifically:

1. **Classify** the signal into the right category — what kind of anomaly is this?
2. **Set priority** — how urgent is this, really? (Crew write "URGENT" on everything. The correlation between "URGENT" in the subject line and actual danger is inversely proportional. The loudest signal last week was about the nutrient synthesizer dispensing vanilla protein cubes instead of chocolate. We gave it a P4. The quiet signal about oxygen recycler output dropping 3% on Deck 12? That was the actual emergency.)
3. **Route** to the correct specialist team — get it right the first time
4. **Flag what's missing** — half our signals don't include basic info we need. We waste time sending subspace relays back to the reporter to ask "which subsystem?" or "what anomaly readout?" Every round trip is 4 minutes we don't have when something is actively venting atmosphere.
5. **Give our Tier 1 team a head start on remediation** — even if a human still resolves the signal, tell them what to try first

## Our teams

We have 6 specialist operations teams:

| Team | What they handle |
|---|---|
| **Crew Identity & Airlock Control** | BioScan ID failures, airlock authentication, crew provisioning, biometric sync, access revocation (especially important when someone gets spaced — administratively, I mean) |
| **Spacecraft Systems Engineering** | Workstations, hull-mounted systems, ShipOS issues, fabricator malfunctions, peripheral modules, that one atmospheric processor on Deck 7 that has been "intermittent" since we launched |
| **Deep Space Communications** | Subspace relay, local comms mesh, DNS beacons, signal routing proxy, bandwidth allocation, external relay uplinks |
| **Mission Software Operations** | FlightOS, navigation suite, sensor platforms, Mission Suite licensing, internal tools, instrument calibration software |
| **Threat Response Command** | Hostile signal detection, malware, unauthorized access, containment breaches, compliance incidents, SentinelGrid certificate management |
| **Telemetry & Data Core** | Sensor archives, crew file stores, databases, backups, data access requests, telemetry pipelines |

I've attached our **internal signal routing guide** — but fair warning, it was written 8 months ago by Lt. Mehta, and some things have changed. We've also reorganized since then. About 20% of signal types aren't covered in it, and some of the routing rules overlap between teams. My section chiefs argue about ownership constantly. For example: who handles BioAuth panel issues — Crew Identity or Threat Response? Depends on the context, and honestly we're not consistent about it ourselves. Lt. Mehta has opinions. He has written them in the margins. They are colorful.

## What "good" looks like to us

- **Reduce misrouting from 42% to under 15%** in the first month
- **Time-to-route under 5 minutes** (from 3.4 hours)
- **Catch missing information proactively** so we stop playing subspace ping-pong with reporters
- **Actionable remediation steps** — not generic "investigate the anomaly" but specific things a Tier 1 controller can actually try

If you can show me this working on even 50 of our real signals, I can make the case to the Admiral. He has been sending memos. The memos contain phrases like "unacceptable" and "reviewing leadership decisions." The Admiral is 0.3 AU away, which means his pointed questions take 4 minutes to arrive, but they hit just as hard.

You may have heard what happened to Titan Outpost. They had a 38% misroute rate. *Had.*

## Things you should know

- Our signals come in through **4 channels**: subspace relay (long-form, detailed), holodeck comm (short, missing context, occasionally interrupted by decompression alarms), the bridge terminal (structured, but crew treat the form fields as suggestions), and emergency beacon (transcribed by the duty officer — messy, panicked, sometimes just screaming and then a cryo-sleep auto-reply).
- **Some signals aren't real incidents** — we get auto-replies, "thanks" messages, cryo-sleep out-of-rotation notifications, and occasional spam from that merchant vessel that keeps trying to sell us "premium hull sealant." Our system doesn't filter these before routing.
- **We run the station stack**: BioScan ID for biometrics, ShipOS MDM for device management, Mission Suite for crew productivity, Station Core for compute and storage. Most of our infrastructure runs on Station Core. We recently deployed SentinelGrid for threat detection. We still have some legacy systems — FlightOS has components that predate the station's launch, and we have a few standalone sensor archives that refuse to sync.
- **Priority is subjective**: Crew over-escalate constantly. "URGENT" in the subject line usually isn't. But sometimes a quiet signal like "slight variance in oxygen recycler output" is actually critical. Context matters more than keywords. The protein cube incident was filed as P1 Red Alert. The actual hull micro-fracture on Deck 4 was filed as P3 with the subject line "small draft in corridor."
- **Containment signals are special**: Anything involving potential hull breach, atmospheric compromise, or unauthorized access to restricted decks must be escalated to Threat Response Command immediately, regardless of category. Getting this wrong has consequences. The kind of consequences measured in hull integrity percentages.

## One more thing

I don't need a holographic assistant. I don't need a dashboard. I need **an API I can plug into our existing bridge terminal workflow** that returns a JSON decision for each signal. Fast, reliable, and right most of the time. If it's not sure, it should say so.

We are 0.3 AU from the nearest competent help. My patience is approximately the same distance from running out.

— Commander Kapoor
