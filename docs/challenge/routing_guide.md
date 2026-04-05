# Contoso IT Support — Internal Routing Guide

> **Last updated:** July 2025
> **Author:** Raj Mehta, IT Service Desk Manager
> **Status:** DRAFT — some sections still being finalized after the Q2 reorg

---

## How to use this guide

When a ticket comes in, identify the **issue type** from the table below and route to the listed **owning team**. If you're unsure, escalate to the Service Desk Lead.

## Priority Definitions

| Priority | Label | Response SLA | Resolution SLA | When to use |
|---|---|---|---|---|
| P1 | Critical | 15 min | 4 hours | Production system down, security breach in progress, revenue-impacting outage, executive-impacting |
| P2 | High | 1 hour | 8 hours | Major feature broken, no workaround, multiple users affected |
| P3 | Medium | 4 hours | 3 business days | Impact with workaround available, single user blocked but non-urgent |
| P4 | Low | 1 business day | 10 business days | Minor inconvenience, cosmetic issue, feature request, general question |

**Override rule:** Any ticket mentioning potential data breach, regulatory issue, or compliance audit is automatically **P1** regardless of other factors.

---

## Routing Table

### Identity & Access Management (IAM)

| Issue type | Route to | Notes |
|---|---|---|
| Password reset | IAM | Self-service portal handles most; only escalate if SSPR fails |
| Account lockout | IAM | Check for brute-force indicators first — if suspicious, also alert SecOps |
| New user provisioning | IAM | Requires manager approval in ServiceNow |
| SSO not working | IAM | Verify the app is in the Entra ID gallery first |
| Directory sync issues | IAM | Usually Entra Connect related |
| Service account requests | IAM | Requires security review before provisioning |

### Endpoint Engineering

| Issue type | Route to | Notes |
|---|---|---|
| Laptop hardware failure | Endpoint Engineering | If under warranty, initiate vendor RMA |
| OS crash / blue screen | Endpoint Engineering | Collect crash dump before reimaging |
| Software installation request | Endpoint Engineering | Must be on the approved software list |
| Intune enrollment | Endpoint Engineering | New hires should be auto-enrolled |
| Printer issues | Endpoint Engineering | Check if it's a network printer (→ Network Ops) or USB-connected |
| Mobile device issues | Endpoint Engineering | Company-managed devices only |
| Slow computer | Endpoint Engineering | Run hardware diagnostics first |

### Network Operations

| Issue type | Route to | Notes |
|---|---|---|
| VPN connectivity | Network Operations | Check if user's credentials are expired first (→ IAM if so) |
| Office WiFi issues | Network Operations | — |
| DNS resolution failures | Network Operations | — |
| Firewall rule requests | Network Operations | Requires security approval from SecOps |
| Bandwidth / latency | Network Operations | Get specific times and affected services |
| Video conferencing quality | Network Operations | If it's a Teams-specific issue, try Enterprise Apps first |

### Enterprise Applications

| Issue type | Route to | Notes |
|---|---|---|
| SAP errors or access | Enterprise Applications | — |
| Salesforce issues | Enterprise Applications | — |
| Bloomberg terminal | Enterprise Applications | Physical hardware issues go to Endpoint Engineering |
| Microsoft 365 issues | Enterprise Applications | Licensing issues specifically — general M365 outages are Network Ops |
| Internal web app bugs | Enterprise Applications | — |
| Application licensing | Enterprise Applications | — |

### Security Operations (SecOps)

| Issue type | Route to | Notes |
|---|---|---|
| Phishing email received | SecOps | Forward original as attachment to phishing@contoso.com |
| Malware / suspicious activity | SecOps | Isolate device from network immediately |
| Data loss / unauthorized access | SecOps | Mandatory P1 escalation |
| Security certificate issues | SecOps | — |
| Compliance / audit requests | SecOps | — |

### Data Platform

| Issue type | Route to | Notes |
|---|---|---|
| SharePoint site access | Data Platform | — |
| OneDrive sync issues | Data Platform | Large file sync problems are common; check file count limits |
| Database access request | Data Platform | Requires data owner approval |
| Backup / restore request | Data Platform | — |
| File share access | Data Platform | Legacy file shares only; new requests should use SharePoint |

---

## Known gaps in this guide

> **Raj's note:** The following areas still need to be sorted out. For now, use your best judgment or escalate to the Service Desk Lead.

- **Multi-factor authentication (MFA) issues** — Could be IAM (user setup), SecOps (policy enforcement), or Endpoint Engineering (authenticator app issues). We haven't agreed on a single owner.
- **Teams/collaboration issues** — Is it a Network Ops issue (call quality), Enterprise Apps issue (Teams app crash), or Endpoint Engineering issue (headset/camera)? Depends on the symptoms.
- **Cloud infrastructure requests** — Azure subscription access, VM requests, etc. Data Platform handles some, but we don't have a formal cloud ops team yet.
- **Onboarding / offboarding** — Touches IAM (accounts), Endpoint Engineering (hardware), Enterprise Apps (licenses), and Data Platform (access). There's a workflow for this but it's manual and breaks constantly.
- **Printer and scanning** — Network printers are Network Ops, USB printers are Endpoint Engineering, scanning-to-email failures could be either.

---

## Escalation rules

1. **P1 tickets** — Must be acknowledged within 15 minutes. If the assigned team doesn't acknowledge, auto-escalate to Service Desk Lead.
2. **Security incidents** — Always route to SecOps. If it also affects another team's domain (e.g., compromised account = IAM + SecOps), route to SecOps as primary and IAM as secondary.
3. **VIP tickets** — C-suite and SVP+ tickets are auto-flagged. Treat as one priority level higher than normal assessment.
4. **Repeat tickets** — If the same reporter has filed 3+ tickets in 7 days for the same issue, escalate to the team lead for root cause investigation.
