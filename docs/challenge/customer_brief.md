# Customer Brief

> Internal memo from Contoso Financial Services — shared with the FDE team during discovery.

---

**From:** Priya Kapoor, VP of IT Operations, Contoso Financial Services
**To:** Microsoft FDE Team
**Date:** March 2026
**Subject:** Help us fix our ticket triage — we're drowning

---

## Who we are

Contoso Financial Services. ~4,500 employees across 3 offices (New York, London, Singapore). We run wealth management, institutional trading, and retail banking. Regulated industry — compliance matters, downtime is expensive, and our people are impatient.

## What's broken

Our IT support team handles ~180 tickets per day. Right now, a human L1 analyst reads every ticket, decides what it is, assigns a priority, and routes it to one of our 6 specialist teams. It takes **3.4 hours on average** to get a ticket to the right team. That's before anyone even starts working on it.

**42% of tickets get misrouted at least once.** When a ticket lands with the wrong team, they bounce it back, and we start over. Some tickets take 2-3 bounces before they reach the right place.

The worst part: our L1 analysts spend so much time triaging that they can't do actual resolution work. They're basically expensive human routers.

## What we want

We want to **automate first-pass triage** for every incoming ticket. Specifically:

1. **Classify** the ticket into the right category — what kind of issue is this?
2. **Set priority** — how urgent is this, really? (People write "URGENT" on everything.)
3. **Route** to the correct specialist team — get it right the first time
4. **Flag what's missing** — half our tickets don't include basic info we need. We waste time going back to the reporter to ask "which system?" or "what error message?"
5. **Give our L1 team a head start on remediation** — even if a human still resolves the ticket, tell them what to try first

## Our teams

We have 6 specialist IT teams:

| Team | What they handle |
|---|---|
| **Identity & Access Management** | Login issues, SSO, MFA, account provisioning, Entra ID, directory sync |
| **Endpoint Engineering** | Laptops, desktops, mobile devices, OS issues, Intune, peripherals |
| **Network Operations** | VPN, WiFi, DNS, firewall rules, proxy, WAN/LAN, office connectivity |
| **Enterprise Applications** | Business apps (SAP, Salesforce, Bloomberg terminal, internal tools), licensing, integrations |
| **Security Operations** | Phishing, malware, suspicious activity, data loss, compliance incidents, certificate management |
| **Data Platform** | Databases, file shares, OneDrive/SharePoint, backups, data access requests, ETL pipelines |

I've attached our **internal routing guide** — but fair warning, it was written 8 months ago and some things have changed. We've also reorganized since then. About 20% of ticket types aren't covered in it, and some of the routing rules overlap between teams. My team leads argue about ownership constantly. For example: who handles MFA issues — Identity or Security? Depends on the context, and honestly we're not consistent about it ourselves.

## What "good" looks like to us

- **Reduce misrouting from 42% to under 15%** in the first month
- **Time-to-route under 5 minutes** (from 3.4 hours)
- **Catch missing information proactively** so we stop playing email ping-pong with reporters
- **Actionable remediation steps** — not generic "investigate the issue" but specific things an L1 can actually try

If you can show me this working on even 50 of our real tickets, I can make the business case to our CTO.

## Things you should know

- Our tickets come in through **4 channels**: email, chat (Teams), the self-service portal, and phone (transcribed by our call center). Quality varies wildly. Email tickets tend to be longer. Chat tickets are short and missing context. Phone transcriptions are messy.
- **Some tickets aren't real incidents** — we get auto-replies, "thanks" messages, out-of-office notifications, and occasional spam. Our system doesn't filter these before routing.
- **We use Microsoft's stack**: Entra ID, Intune, Microsoft 365, Azure. Most of our infra is on Azure. We recently moved to Defender for Endpoint. We still have some legacy on-prem systems (SAP, a few file servers).
- **Priority is subjective**: People over-escalate constantly. "URGENT" in the title usually isn't. But sometimes a quiet ticket like "slight delay in trade execution" is actually critical. Context matters more than keywords.
- **Compliance tickets are special**: Anything involving potential data breach, regulatory inquiry, or audit findings must be escalated to SecOps immediately, regardless of category. Getting this wrong has consequences.

## One more thing

I don't need a chatbot. I don't need a dashboard. I need **an API I can plug into our existing ServiceNow workflow** that returns a JSON decision for each ticket. Fast, reliable, and right most of the time. If it's not sure, it should say so.

— Priya
