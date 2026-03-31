# Copyright (c) Microsoft. All rights reserved.
"""Security & Compliance scenario templates.

Covers: phishing emails, malware/suspicious activity, data loss,
unauthorized access, security certificates, compliance/audit requests,
Defender alerts, social engineering, data breach, endpoint detection,
and regulatory inquiries.
"""

from ms.evals.constants import Category
from ms.evals.constants import MissingInfo
from ms.evals.constants import Priority
from ms.evals.constants import Team
from ms.evals.models import ScenarioTemplate
from ms.evals.scenarios.registry import register

register(ScenarioTemplate(
    scenario_id="sec-001",
    category=Category.SECURITY,
    priority=Priority.P3,
    assigned_team=Team.SECOPS,
    needs_escalation=False,
    missing_information=[MissingInfo.SCREENSHOT_OR_ATTACHMENT, MissingInfo.DEVICE_INFO],
    subjects=[
        "Suspicious email with link — is this phishing?",
        "Got a weird email asking me to verify my credentials",
        "Potential phishing email received this morning",
    ],
    descriptions=[
        "I received an email this morning from what looks like our HR department asking me to verify "
        "my benefits enrollment by clicking a link. The sender address is hr-benefits@contoso-corp.net "
        "which doesn't look right to me. I haven't clicked anything yet but wanted to report it. The "
        "email has the Contoso logo and looks pretty convincing.",
        "There's an email in my inbox claiming to be from Microsoft 365 support telling me my mailbox "
        "is almost full and I need to click a link to expand it. The URL in the hover preview goes to "
        "some domain I don't recognize. I'm in the {department} team and a few colleagues mentioned "
        "getting similar emails.",
    ],
    next_best_actions=[
        "Retrieve the email headers and analyze the sender domain and embedded URLs. Check if the "
        "message was caught by Exchange Online Protection or Defender for Office 365.",
        "Ask the user to forward the email as an attachment to the phishing report mailbox. Check "
        "Defender for Office 365 threat explorer for similar messages across the organization.",
    ],
    remediation_steps=[
        [
            "Instruct user to not click any links and forward the email as attachment to phish@contoso.com",
            "Analyze email headers, sender reputation, and embedded URLs in Defender threat explorer",
            "If confirmed phishing, purge matching messages from all mailboxes via content search",
            "Add sender domain to the tenant block list if malicious",
            "Confirm with user that the email has been removed from their inbox",
        ],
        [
            "Collect the email message ID and review in Exchange admin center",
            "Check Defender Safe Links logs for any click activity on the URL",
            "Run a tenant-wide search for emails from the same sender domain",
            "If benign, inform the user; if malicious, initiate incident response playbook",
            "Update phishing simulation training library with this example",
        ],
    ],
))

register(ScenarioTemplate(
    scenario_id="sec-002",
    category=Category.SECURITY,
    priority=Priority.P2,
    assigned_team=Team.SECOPS,
    needs_escalation=True,
    missing_information=[MissingInfo.AFFECTED_USERS, MissingInfo.TIMESTAMP],
    subjects=[
        "Mass phishing campaign hitting our entire trading floor",
        "Multiple employees in Wealth Management received the same phishing email",
        "Coordinated phishing attack targeting finance department",
    ],
    descriptions=[
        "At least 15 people on the trading floor received identical emails claiming to be from our "
        "clearing partner requesting urgent wire transfer confirmations. The emails contain a link to "
        "a fake login portal. I'm worried some people may have already clicked — one trader mentioned "
        "entering his credentials before realizing it was fake. This is impacting the 3rd floor "
        "trading operations team in the New York office.",
        "Our Wealth Management team lead reported that the entire team of 20+ advisors received "
        "phishing emails impersonating our CRM vendor. The emails reference real client account "
        "numbers which is extremely concerning. At least three people clicked the link. We need "
        "this investigated immediately — we handle sensitive client financial data.",
    ],
    next_best_actions=[
        "Immediately identify all recipients and check for credential compromise. Force password "
        "resets for any users who interacted with the phishing link. Engage Defender for Office 365 "
        "automated investigation.",
        "Trigger incident response protocol. Identify the full blast radius using Defender threat "
        "explorer, revoke sessions for compromised accounts, and notify compliance team given the "
        "financial data exposure risk.",
    ],
    remediation_steps=[
        [
            "Identify all recipients of the phishing campaign via Defender threat explorer",
            "Determine which users clicked the link using Safe Links click trace data",
            "Force password reset and revoke active sessions for all users who interacted with the link",
            "Purge all matching phishing emails from tenant mailboxes",
            "Block the sender domain and phishing URL at the tenant and proxy level",
            "Notify the compliance team about potential credential compromise in a regulated unit",
            "Monitor affected accounts for suspicious sign-in activity for 72 hours",
        ],
    ],
))

register(ScenarioTemplate(
    scenario_id="sec-003",
    category=Category.SECURITY,
    priority=Priority.P2,
    assigned_team=Team.SECOPS,
    needs_escalation=True,
    missing_information=[MissingInfo.DEVICE_INFO, MissingInfo.NETWORK_LOCATION],
    subjects=[
        "Defender alert — malware detected on my work laptop",
        "Microsoft Defender flagged a Trojan on my machine",
        "Malware alert popped up on my laptop from Defender for Endpoint",
    ],
    descriptions=[
        "I just got a Defender for Endpoint alert on my laptop saying it detected 'Trojan:Win32/"
        "AgentTesla!ml' in my Downloads folder. The file name is 'Q4_Trading_Report.exe'. I think I "
        "downloaded it from an email attachment about 20 minutes ago. My laptop is YOURPC-0247 and "
        "I'm connected to the corporate network on the 2nd floor of the Chicago office. I'm in the "
        "risk analytics team and have access to client portfolio data.",
        "Defender for Endpoint quarantined something on my laptop but I'm not sure what it was. The "
        "notification said 'Threat detected and remediated' but I want to make sure my machine is "
        "clean. I was browsing a financial news site when it happened. I need my laptop for client "
        "meetings this afternoon.",
    ],
    next_best_actions=[
        "Investigate the Defender for Endpoint alert in the security portal. Check the device timeline "
        "for indicators of compromise and determine if the malware executed before quarantine.",
        "Verify the malware was fully remediated by Defender. If AgentTesla was involved, check for "
        "credential exfiltration and rotate any cached credentials on the device.",
    ],
    remediation_steps=[
        [
            "Review the Defender for Endpoint alert and device timeline in the security portal",
            "Determine if the malware executed or was quarantined pre-execution",
            "If executed, isolate the device from the network via Defender portal",
            "Run a full Defender antivirus scan on the device",
            "Check for persistence mechanisms (scheduled tasks, registry run keys)",
            "If credential-stealing malware, force password reset and revoke tokens",
            "Release device from isolation once confirmed clean and update the user",
        ],
        [
            "Verify quarantine status in Defender for Endpoint console",
            "Analyze the file hash against VirusTotal and internal threat intelligence",
            "Check if the email source has been flagged and block the sender if malicious",
            "Confirm no lateral movement by reviewing network connection logs on the device",
            "Provide user with guidance on safe download practices",
        ],
    ],
))

register(ScenarioTemplate(
    scenario_id="sec-004",
    category=Category.SECURITY,
    priority=Priority.P2,
    assigned_team=Team.SECOPS,
    needs_escalation=False,
    missing_information=[MissingInfo.DEVICE_INFO, MissingInfo.SCREENSHOT_OR_ATTACHMENT, MissingInfo.TIMESTAMP],
    subjects=[
        "Suspicious process running on my workstation",
        "Unknown process using high CPU — looks suspicious",
        "Found a weird process in Task Manager I don't recognize",
    ],
    descriptions=[
        "I noticed a process called 'svchost-update.exe' running in Task Manager that's using about "
        "30% CPU. I don't think this is a normal Windows process — the name looks slightly off. It's "
        "been running for about two hours and my machine has been noticeably slower. I'm on my "
        "corporate desktop in the Boston office, asset tag DSK-1893.",
        "There's a process called 'csrss-helper.exe' consuming network bandwidth on my machine. I "
        "checked and it's making outbound connections to an IP address that doesn't match any of our "
        "internal servers. I'm in the compliance department and I handle sensitive regulatory "
        "documents on this machine.",
    ],
    next_best_actions=[
        "Investigate the process via Defender for Endpoint advanced hunting. Check the process hash, "
        "parent process, and network connections to determine if it's malicious.",
        "Query Defender for Endpoint for the device timeline and process tree. If the process is "
        "unsigned or connecting to suspicious external IPs, isolate the device.",
    ],
    remediation_steps=[
        [
            "Identify the suspicious process in Defender for Endpoint device timeline",
            "Check the file hash, digital signature, and parent process chain",
            "Review outbound network connections from the process",
            "If malicious, isolate the device immediately via Defender portal",
            "Terminate the process and remove any associated persistence mechanisms",
            "Run a full antivirus scan and verify device integrity",
            "Release from isolation and monitor for 48 hours",
        ],
        [
            "Use Defender advanced hunting to query for the process across all endpoints",
            "If the process is found on multiple machines, escalate as a potential outbreak",
            "Collect a memory dump if the process is still running for forensic analysis",
            "Block the file hash in Defender custom indicators if confirmed malicious",
            "Update endpoint detection rules to catch similar threats",
        ],
    ],
))

register(ScenarioTemplate(
    scenario_id="sec-005",
    category=Category.SECURITY,
    priority=Priority.P1,
    assigned_team=Team.SECOPS,
    needs_escalation=True,
    missing_information=[MissingInfo.AFFECTED_USERS, MissingInfo.BUSINESS_IMPACT, MissingInfo.TIMESTAMP],
    subjects=[
        "URGENT: Sensitive client files shared to external email addresses",
        "Potential data breach — confidential documents sent outside the company",
        "Data loss alert: restricted files shared via OneDrive external link",
    ],
    descriptions=[
        "The DLP dashboard just flagged that a user in our wealth management group shared a OneDrive "
        "folder containing client SSNs, account numbers, and portfolio values with three external "
        "Gmail addresses. The share happened approximately 45 minutes ago. The folder contains over "
        "200 client records. I've already disabled the sharing link but the files may have been "
        "downloaded. This is a potential SEC and state privacy law violation.",
        "I discovered that someone in the {department} department emailed a spreadsheet containing "
        "confidential trading strategies and client PII to a personal email address. The DLP policy "
        "triggered but was set to 'notify only' mode so the email went through. The data includes "
        "financial records subject to Gramm-Leach-Bliley Act protections.",
    ],
    next_best_actions=[
        "Immediately revoke all external sharing links and disable the user's external sharing "
        "capability. Engage legal and compliance teams for regulatory breach assessment. Preserve "
        "all audit logs.",
        "Contain the breach by revoking access and disabling the sharing account. Begin incident "
        "documentation for potential regulatory notification. Pull full DLP activity logs for the "
        "past 30 days on this user.",
    ],
    remediation_steps=[
        [
            "Revoke all external sharing links and disable external sharing for the affected user",
            "Preserve full audit trail from Microsoft Purview compliance portal",
            "Determine exact scope of exposed data (record count, data types, recipients)",
            "Notify legal and compliance team for regulatory breach assessment",
            "Disable the user's account pending investigation if intentional exfiltration suspected",
            "Engage legal counsel for SEC/GLBA notification obligations",
            "Document incident timeline for regulatory reporting",
        ],
    ],
))

register(ScenarioTemplate(
    scenario_id="sec-006",
    category=Category.SECURITY,
    priority=Priority.P2,
    assigned_team=Team.SECOPS,
    needs_escalation=False,
    missing_information=[MissingInfo.AFFECTED_SYSTEM, MissingInfo.ENVIRONMENT_DETAILS],
    subjects=[
        "SSL certificate expiring in 3 days on trading gateway",
        "TLS cert for internal portal about to expire this weekend",
        "Certificate expiration warning — client-facing API endpoint",
    ],
    descriptions=[
        "Our monitoring system flagged that the SSL certificate for trading-gateway.contoso.com "
        "expires in 3 days. This is the API endpoint our trading partners use to submit orders. If "
        "the cert expires, all partner integrations will break and we'll lose the ability to process "
        "trades. The certificate is issued by DigiCert and was last renewed 12 months ago.",
        "The TLS certificate for wealthportal.contoso.com is expiring on Saturday. This portal is "
        "used by our financial advisors and their clients to view account balances and statements. "
        "We need the cert renewed before the weekend to avoid service disruption.",
    ],
    next_best_actions=[
        "Initiate emergency certificate renewal through DigiCert or the internal PKI. Coordinate "
        "with the infrastructure team for deployment during a low-traffic maintenance window.",
        "Check the certificate auto-renewal configuration and determine why the renewal failed. "
        "Submit an expedited renewal request and plan deployment before expiration.",
    ],
    remediation_steps=[
        [
            "Verify the certificate details (CN, SANs, issuer, expiration date)",
            "Submit renewal request through DigiCert or internal PKI portal",
            "Generate a new CSR if required by the certificate authority",
            "Deploy the renewed certificate to the web server or load balancer",
            "Verify the new certificate is valid and the TLS handshake completes successfully",
            "Update the certificate monitoring system with the new expiration date",
        ],
        [
            "Check if auto-renewal via ACME or internal automation should have handled this",
            "If auto-renewal failed, investigate root cause and fix the automation",
            "Manually renew the certificate as an interim measure",
            "Test the endpoint from external and internal clients after deployment",
            "Add the certificate to the centralized tracking spreadsheet",
        ],
    ],
))

register(ScenarioTemplate(
    scenario_id="sec-007",
    category=Category.SECURITY,
    priority=Priority.P1,
    assigned_team=Team.SECOPS,
    needs_escalation=True,
    missing_information=[MissingInfo.AFFECTED_SYSTEM, MissingInfo.BUSINESS_IMPACT],
    subjects=[
        "CRITICAL: SSL certificate expired on production API — partners can't connect",
        "Production TLS cert expired — trade processing is down",
        "Expired certificate on api.contoso.com causing outage",
    ],
    descriptions=[
        "The SSL certificate on api.contoso.com expired at midnight and our trading partners are "
        "getting certificate errors when trying to submit orders. We've received calls from three "
        "major clearing firms already. The entire trade processing pipeline is affected. This is a "
        "production outage impacting revenue — we need the cert renewed and deployed immediately.",
        "Our production REST API used by external partners for trade settlement has an expired TLS "
        "certificate. Clients are seeing ERR_CERT_DATE_INVALID and none of them can connect. This "
        "is impacting all partner integrations and we're losing transactions every minute. The old "
        "cert expired 6 hours ago.",
    ],
    next_best_actions=[
        "Treat as P1 outage. Immediately deploy a renewed certificate or a valid interim certificate "
        "to restore service. Notify affected trading partners of the resolution timeline.",
        "Emergency certificate deployment needed. If renewal takes time, consider deploying a "
        "temporary self-signed cert for internal services while the public cert is expedited.",
    ],
    remediation_steps=[
        [
            "Confirm the expired certificate details and the affected endpoints",
            "Submit an emergency renewal request to the certificate authority",
            "If renewal takes time, check if a wildcard cert can be temporarily deployed",
            "Deploy the new certificate to all load balancers and reverse proxies",
            "Verify partner connectivity is restored by testing TLS handshake from external",
            "Notify all affected trading partners that the issue is resolved",
            "Conduct post-incident review to prevent future certificate expirations",
        ],
    ],
))

register(ScenarioTemplate(
    scenario_id="sec-008",
    category=Category.SECURITY,
    priority=Priority.P2,
    assigned_team=Team.SECOPS,
    needs_escalation=False,
    missing_information=[MissingInfo.TIMESTAMP, MissingInfo.AFFECTED_USERS, MissingInfo.ENVIRONMENT_DETAILS],
    subjects=[
        "Compliance audit request — need access logs for past 90 days",
        "Internal audit team requesting Entra ID sign-in logs",
        "Audit requirement: export security event logs for review",
    ],
    descriptions=[
        "Our internal compliance team is conducting the quarterly SOX audit and needs access logs "
        "for all users in the trading systems group for the past 90 days. Specifically, they need "
        "Entra ID sign-in logs, VPN connection logs, and privileged access usage for the Bloomberg "
        "terminal servers. The audit committee meeting is in two weeks and this data is required for "
        "the report.",
        "The compliance department needs a full export of security event logs from our Entra ID "
        "tenant and Microsoft 365 audit logs for the period January through March. This is for the "
        "annual SOC 2 Type II audit. The auditor has provided a specific control matrix and we need "
        "to map our logs to their evidence requests.",
    ],
    next_best_actions=[
        "Export the requested logs from Entra ID and Microsoft 365 compliance center. Coordinate "
        "with the compliance team on the required format and delivery method.",
        "Review the audit request scope, pull the relevant logs from Entra ID and Microsoft Purview, "
        "and prepare the data in a format that maps to the audit control matrix.",
    ],
    remediation_steps=[
        [
            "Confirm the exact scope of the audit request (time range, users, systems)",
            "Export Entra ID sign-in and audit logs from the Azure portal or via Graph API",
            "Pull Microsoft 365 unified audit logs from the compliance portal",
            "Export VPN connection logs from the network team's log aggregation tool",
            "Package the logs in the format requested by the compliance team",
            "Deliver via secure internal file share with appropriate access controls",
            "Document the data handoff for chain-of-custody tracking",
        ],
    ],
))

register(ScenarioTemplate(
    scenario_id="sec-009",
    category=Category.SECURITY,
    priority=Priority.P1,
    assigned_team=Team.SECOPS,
    needs_escalation=True,
    missing_information=[MissingInfo.BUSINESS_IMPACT, MissingInfo.CONTACT_INFO],
    subjects=[
        "URGENT: Regulatory inquiry from FINRA regarding data handling practices",
        "SEC information request — need security documentation immediately",
        "Financial regulator requesting incident response records",
    ],
    descriptions=[
        "We received a formal inquiry from FINRA requesting documentation of our data handling "
        "practices, security controls, and incident response procedures related to client data "
        "protection. The response deadline is 10 business days. Legal has been notified and they "
        "need our security team to compile the technical documentation. This is a regulatory "
        "matter and must be treated with the highest priority.",
        "The SEC has sent an information request asking for our security incident logs, access "
        "control policies, and data retention practices for the past 24 months. Our Chief Compliance "
        "Officer needs the security operations team to gather all relevant technical artifacts. The "
        "legal team is coordinating the response but we need the raw data from our security systems.",
    ],
    next_best_actions=[
        "Immediately engage with legal and compliance to understand the full scope of the regulatory "
        "request. Begin compiling security documentation, policies, and log exports.",
        "Treat as top priority. Assign a dedicated resource to compile the requested security "
        "artifacts. Coordinate with legal on what can be shared and in what format.",
    ],
    remediation_steps=[
        [
            "Meet with legal and compliance to review the exact scope of the regulatory request",
            "Compile current security policies, incident response plans, and control documentation",
            "Export relevant security logs from SIEM, Defender, and Entra ID for the requested period",
            "Prepare a summary of security incidents and response actions during the relevant period",
            "Have legal review all materials before submission to the regulator",
            "Submit documentation within the regulatory deadline via approved channels",
            "Retain copies of all submitted materials for internal records",
        ],
    ],
))

register(ScenarioTemplate(
    scenario_id="sec-010",
    category=Category.SECURITY,
    priority=Priority.P2,
    assigned_team=Team.SECOPS,
    needs_escalation=False,
    missing_information=[MissingInfo.TIMESTAMP, MissingInfo.CONTACT_INFO, MissingInfo.STEPS_TO_REPRODUCE],
    subjects=[
        "Someone called claiming to be from IT and asked for my password",
        "Possible social engineering attempt via phone call",
        "Suspicious phone call pretending to be Microsoft support",
    ],
    descriptions=[
        "I got a phone call about 30 minutes ago from someone claiming to be from our IT helpdesk. "
        "They said there was a security issue with my account and asked me to confirm my password "
        "and employee ID. I gave them my employee ID but not my password — it seemed suspicious. The "
        "caller ID showed an internal number but the person didn't know my manager's name when I "
        "asked. I'm a portfolio manager in the Boston office.",
        "A colleague in the {department} team received a call from someone saying they were from "
        "Microsoft support and that our company's Microsoft 365 tenant was being attacked. They "
        "asked her to install a remote desktop tool so they could 'fix' her machine. She didn't "
        "install anything but she's worried because she confirmed her full name and email address.",
    ],
    next_best_actions=[
        "Document the social engineering attempt details and check if other employees received "
        "similar calls. If any credentials were shared, force an immediate password reset.",
        "Record details of the call (time, caller ID, what was requested). Check call logs if "
        "possible and send a security awareness notification to the affected department.",
    ],
    remediation_steps=[
        [
            "Document the call details: time, caller ID, what information was requested and shared",
            "If any credentials were disclosed, force immediate password reset and revoke sessions",
            "Check if other employees in the same department received similar calls",
            "Send a targeted security awareness alert to the affected office or department",
            "Report the phone number to the telecom team for blocking if external",
            "Log the incident in the security incident tracking system",
        ],
        [
            "Interview the affected employee to capture the full conversation details",
            "Cross-reference the caller ID with internal and external phone directories",
            "If information was shared, assess the risk level and take appropriate protective actions",
            "Update the social engineering playbook with this new attack vector",
            "Consider running a vishing simulation for the affected department",
        ],
    ],
))

register(ScenarioTemplate(
    scenario_id="sec-011",
    category=Category.SECURITY,
    priority=Priority.P1,
    assigned_team=Team.SECOPS,
    needs_escalation=True,
    missing_information=[MissingInfo.AFFECTED_SYSTEM, MissingInfo.AFFECTED_USERS, MissingInfo.NETWORK_LOCATION],
    subjects=[
        "CRITICAL: Ransomware encrypting files on shared drive",
        "Ransomware attack — files being renamed with .locked extension",
        "URGENT: File share encryption in progress — suspected ransomware",
    ],
    descriptions=[
        "Files on the \\\\contoso-fs01\\trading-data share are being encrypted right now. All the "
        "files are being renamed with a .locked extension and there's a ransom note called "
        "README_DECRYPT.txt in every folder. I noticed it about 5 minutes ago when I couldn't open "
        "a client report. The share is used by the entire trading operations team — about 150 users "
        "across all three offices. We need to stop this immediately.",
        "Our compliance document share is under active ransomware encryption. Files in "
        "\\\\contoso-fs02\\compliance are being encrypted and renamed. A ransom note demands Bitcoin "
        "payment. This share contains regulatory filings, audit reports, and client correspondence "
        "going back 7 years. We're legally required to retain this data. The infection appears to be "
        "spreading to adjacent shares.",
    ],
    next_best_actions=[
        "IMMEDIATELY isolate the affected file server from the network to stop encryption spread. "
        "Identify the source device and isolate it. Do NOT pay the ransom. Activate the incident "
        "response plan and engage the CIRT team.",
        "Network-isolate the file server and the suspected source device. Preserve forensic evidence. "
        "Begin identifying the ransomware variant for potential decryptor availability. Notify "
        "executive leadership and legal.",
    ],
    remediation_steps=[
        [
            "Immediately isolate the affected file server(s) from the network",
            "Identify the source device using Defender for Endpoint alerts and file access logs",
            "Isolate the source device from the network via Defender portal",
            "Determine the ransomware variant from the ransom note and file extension",
            "Check for available decryption tools from No More Ransom project",
            "Assess the scope of encrypted files and last known good backup timestamps",
            "Restore files from backup after confirming the backup is clean",
            "Notify legal and executive leadership about the incident",
            "Engage external incident response firm if needed",
            "Conduct full forensic investigation to determine initial access vector",
        ],
    ],
))

register(ScenarioTemplate(
    scenario_id="sec-012",
    category=Category.SECURITY,
    priority=Priority.P1,
    assigned_team=Team.SECOPS,
    needs_escalation=True,
    missing_information=[MissingInfo.BUSINESS_IMPACT, MissingInfo.TIMESTAMP],
    subjects=[
        "Insider threat alert — unusual bulk data download detected",
        "Employee downloading massive amounts of client data to USB",
        "DLP alert: suspicious data exfiltration by departing employee",
    ],
    descriptions=[
        "Our DLP system flagged that an employee in the wealth management division downloaded over "
        "15,000 client records to a personal USB drive yesterday evening between 8 PM and 11 PM. "
        "This employee submitted their resignation last Friday and their last day is next week. The "
        "data includes client names, account numbers, portfolio values, and contact information. HR "
        "has been notified. The employee's badge access shows they were in the office alone on the "
        "27th floor.",
        "Microsoft Purview flagged a user in the trading department who exported 3.2 GB of data from "
        "SharePoint to their local machine in the past 48 hours. The files include proprietary "
        "trading algorithms, client lists, and internal strategy documents. We recently learned this "
        "employee has been interviewing with a competitor. This data is classified as Highly "
        "Confidential under our data classification policy.",
    ],
    next_best_actions=[
        "Immediately disable the user's remote access and external sharing capabilities while "
        "preserving their account for investigation. Coordinate with HR and legal for an insider "
        "threat investigation.",
        "Contain the potential exfiltration by disabling USB access on the user's device and "
        "revoking external sharing. Pull full DLP activity history and coordinate with HR and legal.",
    ],
    remediation_steps=[
        [
            "Disable the user's external sharing capabilities and USB port access immediately",
            "Preserve all DLP alerts, audit logs, and file access history for the user",
            "Pull the full activity timeline from Microsoft Purview insider risk management",
            "Coordinate with HR and legal on next steps for the investigation",
            "Image the user's workstation for forensic evidence if warranted",
            "Assess the sensitivity and regulatory classification of the downloaded data",
            "If client PII was exfiltrated, initiate breach notification assessment with legal",
            "Review and tighten DLP policies for departing employees",
        ],
    ],
))

register(ScenarioTemplate(
    scenario_id="sec-013",
    category=Category.SECURITY,
    priority=Priority.P3,
    assigned_team=Team.SECOPS,
    needs_escalation=False,
    missing_information=[MissingInfo.ERROR_MESSAGE, MissingInfo.APPLICATION_VERSION, MissingInfo.DEVICE_INFO],
    subjects=[
        "Defender blocking our internal portfolio management tool",
        "False positive — Defender quarantined an approved internal application",
        "Microsoft Defender keeps flagging our custom trading script as malware",
    ],
    descriptions=[
        "Microsoft Defender for Endpoint is blocking our internal portfolio rebalancing tool "
        "(PortfolioOptimizer.exe v4.2.1) every time I try to run it. It flags it as "
        "'PUA:Win32/Presenoker' and quarantines the executable. This tool was developed in-house "
        "by our quant team and has been approved for use. About 30 portfolio managers need this "
        "tool for daily client rebalancing and we can't do our work without it.",
        "Defender is flagging a Python script (trade_reconciler.py) that our team runs daily for "
        "trade reconciliation as potentially unwanted software. It wasn't doing this until the "
        "latest Defender definition update. The script hasn't changed in months. This is affecting "
        "our end-of-day processing workflow.",
    ],
    next_best_actions=[
        "Verify the file hash and confirm it matches the approved internal tool. If confirmed as "
        "a false positive, create a Defender exclusion or submit the file for false positive review.",
        "Check the file's digital signature and hash against the internal software inventory. "
        "If legitimate, add an exclusion in Defender for Endpoint.",
    ],
    remediation_steps=[
        [
            "Collect the file hash (SHA256) and Defender detection details from the alert",
            "Verify the hash matches the approved version in the internal software repository",
            "If confirmed legitimate, create a Defender for Endpoint indicator to allow the file",
            "Alternatively, add a folder exclusion for the application's install directory",
            "Submit the file to Microsoft as a false positive via the Defender portal",
            "Confirm the application runs without being blocked after the exclusion is applied",
        ],
        [
            "Retrieve the quarantined file from Defender and compare its hash to the known good copy",
            "Check if the latest Defender signature update introduced the false detection",
            "Create an ASR rule exclusion if application security rules are triggering",
            "Notify affected users once the exclusion is deployed via Intune",
            "Monitor for re-detection after the next signature update cycle",
        ],
    ],
))

register(ScenarioTemplate(
    scenario_id="sec-014",
    category=Category.SECURITY,
    priority=Priority.P2,
    assigned_team=Team.SECOPS,
    needs_escalation=False,
    missing_information=[
        MissingInfo.AFFECTED_SYSTEM,
        MissingInfo.STEPS_TO_REPRODUCE,
        MissingInfo.ENVIRONMENT_DETAILS,
    ],
    subjects=[
        "Security vulnerability found in our internal client portal",
        "SQL injection vulnerability discovered in the reporting dashboard",
        "Cross-site scripting vulnerability in internal web application",
    ],
    descriptions=[
        "During a routine code review of our internal client reporting portal, I found what appears "
        "to be a SQL injection vulnerability in the account lookup endpoint (/api/v2/accounts/search). "
        "The query parameter 'accountId' is being concatenated directly into the SQL query without "
        "parameterization. This portal has access to the client database with PII and financial data. "
        "I haven't tested it with a live exploit but the code pattern is clearly vulnerable.",
        "Our application security scanner flagged a reflected XSS vulnerability in the internal "
        "performance reporting dashboard at https://reports.contoso.internal/dashboard. The "
        "'dateRange' parameter in the URL is rendered without sanitization. While this is an internal "
        "app, it's accessible to all employees and displays client financial data.",
    ],
    next_best_actions=[
        "Assess the vulnerability severity and exploitability. If the affected application handles "
        "client PII or financial data, coordinate an emergency patch with the development team.",
        "Verify the vulnerability and determine if it's actively exploitable. Implement a WAF rule "
        "as a temporary mitigation while the development team prepares a code fix.",
    ],
    remediation_steps=[
        [
            "Verify and reproduce the reported vulnerability in a non-production environment",
            "Assess the severity using CVSS scoring and determine the blast radius",
            "If critical, implement a WAF rule or input validation as immediate mitigation",
            "File an emergency change request for the development team to patch the vulnerability",
            "Review the application for similar vulnerability patterns",
            "Conduct a penetration test after the fix is deployed to confirm remediation",
            "Update the secure coding guidelines with this vulnerability pattern",
        ],
    ],
))

register(ScenarioTemplate(
    scenario_id="sec-015",
    category=Category.SECURITY,
    priority=Priority.P3,
    assigned_team=Team.SECOPS,
    needs_escalation=False,
    missing_information=[MissingInfo.DEVICE_INFO, MissingInfo.BUSINESS_IMPACT],
    subjects=[
        "USB device policy violation alert on workstation",
        "Received alert about unauthorized USB storage device",
        "Endpoint detected USB drive plugged in against policy",
    ],
    descriptions=[
        "I got an email notification from the security team saying a USB storage device was detected "
        "on my workstation. I plugged in a USB drive to transfer a presentation to the conference "
        "room display. I didn't realize this was against policy. The drive is my personal 32GB flash "
        "drive. I'm a financial advisor in the Boston office. Can you help me understand what I'm "
        "supposed to do instead?",
        "Defender for Endpoint generated an alert that an unauthorized removable storage device was "
        "connected to machine WKS-3847 at 2:15 PM today. The device is a Seagate external hard "
        "drive (VID: 0x0BC2). The machine is assigned to an employee in the {department} department. "
        "Per policy, USB storage devices are blocked on all endpoints but the alert indicates the "
        "device was connected for approximately 8 minutes before being blocked.",
    ],
    next_best_actions=[
        "Review the USB device connection alert and determine if any data was transferred during "
        "the connection window. Remind the user of the removable media policy.",
        "Check the DLP logs to verify no data was copied to the device before the block engaged. "
        "Follow up with the user about the policy and approved alternatives.",
    ],
    remediation_steps=[
        [
            "Review the Defender for Endpoint alert for USB device connection details",
            "Check DLP logs to determine if any files were copied to the removable device",
            "If data was transferred, assess the sensitivity of the copied files",
            "Contact the user to discuss the policy violation and understand the business need",
            "Recommend approved alternatives (OneDrive, approved file transfer methods)",
            "Log the policy violation in the security incident tracker",
        ],
    ],
))

register(ScenarioTemplate(
    scenario_id="sec-016",
    category=Category.SECURITY,
    priority=Priority.P2,
    assigned_team=Team.SECOPS,
    needs_escalation=True,
    missing_information=[MissingInfo.AFFECTED_USERS, MissingInfo.TIMESTAMP],
    subjects=[
        "Suspicious email forwarding rule found on executive mailbox",
        "Auto-forward rule discovered sending emails to external address",
        "Compromised mailbox — hidden forwarding rule detected",
    ],
    descriptions=[
        "During a routine mailbox audit, I discovered a hidden inbox rule on the CFO's mailbox that "
        "forwards all emails containing keywords like 'wire transfer', 'acquisition', 'merger', and "
        "'board meeting' to an external Gmail address (contoso.backup2024@gmail.com). The rule was "
        "created 12 days ago and has been silently forwarding emails this entire time. The CFO says "
        "she did not create this rule.",
        "Exchange Online protection flagged a new auto-forwarding rule on a mailbox in the executive "
        "team. The rule forwards all incoming messages to an external Outlook.com address. The user "
        "claims they didn't set it up. This could indicate a business email compromise — the user is "
        "a VP in our mergers and acquisitions group and handles highly sensitive deal information.",
    ],
    next_best_actions=[
        "Immediately delete the forwarding rule and revoke all active sessions for the affected "
        "account. Force a password reset and investigate how the rule was created. This is a "
        "potential business email compromise.",
        "Remove the forwarding rule, reset the user's password, and revoke active tokens. Check "
        "sign-in logs for unauthorized access and determine if other mailboxes are affected.",
    ],
    remediation_steps=[
        [
            "Immediately remove the malicious forwarding rule from the mailbox",
            "Force password reset and revoke all active sessions and OAuth tokens",
            "Enable MFA if not already configured on the account",
            "Review Entra ID sign-in logs for the account over the past 30 days",
            "Check for unauthorized sign-ins from unusual locations or devices",
            "Assess what emails were forwarded by reviewing the rule criteria and mail flow logs",
            "Check other executive mailboxes for similar hidden forwarding rules",
            "Notify legal and compliance if sensitive business information was exfiltrated",
            "Conduct a full mailbox audit to check for other persistence mechanisms",
        ],
    ],
))

register(ScenarioTemplate(
    scenario_id="sec-017",
    category=Category.SECURITY,
    priority=Priority.P1,
    assigned_team=Team.SECOPS,
    needs_escalation=True,
    missing_information=[MissingInfo.AFFECTED_SYSTEM, MissingInfo.NETWORK_LOCATION],
    subjects=[
        "CRITICAL: Crypto mining process detected on production server",
        "Server compromised — unauthorized cryptocurrency miner running",
        "Defender alert: CoinMiner threat on Windows Server",
    ],
    descriptions=[
        "Defender for Endpoint triggered a high-severity alert on server SVRCONT-DB04 for "
        "'Behavior:Win32/CoinMiner.A'. The server CPU has been pegged at 98% for the past 6 hours. "
        "This is one of our database servers that hosts client transaction records. The process "
        "'windowsupdate-svc.exe' is consuming all available CPU. I checked and it's not a legitimate "
        "Windows process. The server was last patched 3 weeks ago.",
        "Our monitoring dashboard shows a production application server (APP-TRADE-07) has been at "
        "100% CPU utilization since yesterday. Investigation revealed a process called 'xmrig.exe' "
        "running under the SYSTEM account. This appears to be cryptocurrency mining software. The "
        "server handles real-time trade execution and performance has degraded significantly. Initial "
        "analysis suggests the server may have been compromised through an unpatched vulnerability.",
    ],
    next_best_actions=[
        "Immediately isolate the server to prevent lateral movement. Terminate the mining process "
        "and conduct a forensic investigation to determine the initial access vector. The server "
        "compromise may indicate a broader breach.",
        "Isolate the compromised server, terminate the crypto mining process, and determine how the "
        "attacker gained access. Check if the same vulnerability exists on other servers.",
    ],
    remediation_steps=[
        [
            "Isolate the compromised server from the network immediately",
            "Terminate the crypto mining process and collect the binary for analysis",
            "Capture a forensic image of the server for evidence preservation",
            "Check for persistence mechanisms (services, scheduled tasks, startup entries)",
            "Determine the initial access vector (unpatched vulnerability, stolen credentials, etc.)",
            "Scan all servers in the same network segment for similar indicators of compromise",
            "Patch the exploited vulnerability across all affected systems",
            "Restore the server from a known clean backup if integrity cannot be verified",
            "Review server hardening configuration against security baseline",
            "Update detection rules in Defender for Endpoint to catch similar activity",
        ],
    ],
))

register(ScenarioTemplate(
    scenario_id="sec-018",
    category=Category.SECURITY,
    priority=Priority.P4,
    assigned_team=Team.SECOPS,
    needs_escalation=False,
    missing_information=[MissingInfo.CONTACT_INFO, MissingInfo.BUSINESS_IMPACT],
    subjects=[
        "Third-party vendor requesting security questionnaire completion",
        "New vendor security assessment — need InfoSec team input",
        "Security due diligence questionnaire from cloud service provider",
    ],
    descriptions=[
        "Our procurement team is evaluating a new cloud-based document management system and the "
        "vendor has sent us a security questionnaire (SIG Lite) that needs to be completed by our "
        "security team. The vendor is DataVault Solutions and they'll be handling some client "
        "documents. The procurement deadline is in 3 weeks so this isn't urgent but we need it done "
        "before we can sign the contract.",
        "We're onboarding a new market data provider and as part of due diligence they need us to "
        "complete their security assessment questionnaire. It covers data encryption, access "
        "controls, incident response, and compliance certifications. Our vendor management team "
        "needs this completed within the next month. It's about 85 questions.",
    ],
    next_best_actions=[
        "Assign the questionnaire to the appropriate security analyst. Pull from existing SOC 2 and "
        "security documentation to complete the common control questions.",
        "Review the questionnaire scope and determine which team members need to contribute. Leverage "
        "existing compliance documentation to expedite completion.",
    ],
    remediation_steps=[
        [
            "Review the vendor security questionnaire to understand the scope",
            "Assign the questionnaire to a security analyst for completion",
            "Pull relevant answers from existing SOC 2 documentation and security policies",
            "Coordinate with infrastructure and application teams for technical details",
            "Have a senior security team member review the completed questionnaire",
            "Submit the completed questionnaire to the vendor management team",
        ],
    ],
))

register(ScenarioTemplate(
    scenario_id="sec-019",
    category=Category.SECURITY,
    priority=Priority.P3,
    assigned_team=Team.SECOPS,
    needs_escalation=False,
    missing_information=[MissingInfo.SCREENSHOT_OR_ATTACHMENT],
    subjects=[
        "Is this email legitimate? Forwarding for verification",
        "User forwarded suspicious email — requesting verification",
        "Please check if this email from 'DocuSign' is real",
    ],
    descriptions=[
        "I received an email from DocuSign saying I have a document to sign regarding a client "
        "account agreement. The email looks professional and has the DocuSign logo but I wasn't "
        "expecting any documents. The sender is docusign-notify@docusign-mail.com. Before I click "
        "anything I wanted to check with the security team if this is legitimate. I've forwarded "
        "the email to phish@contoso.com as well.",
        "One of the financial advisors in our wealth management group forwarded an email to the "
        "help desk asking if it's real. The email claims to be from our custodian bank and asks the "
        "advisor to 'confirm updated wire instructions' by clicking a link. The advisor says they do "
        "receive legitimate emails from this bank but something felt off about this one.",
    ],
    next_best_actions=[
        "Analyze the forwarded email headers and URLs. Cross-reference the sender domain with known "
        "legitimate domains. Provide the user with a clear determination.",
        "Check the email against Defender for Office 365 threat intelligence. Verify the sender "
        "domain and embedded links. Respond to the user with the verdict.",
    ],
    remediation_steps=[
        [
            "Retrieve and analyze the email headers for sender authentication (SPF, DKIM, DMARC)",
            "Check the sender domain against known legitimate and malicious domain lists",
            "Inspect any URLs in the email without clicking (use URL analysis tools)",
            "Cross-reference with Defender for Office 365 threat explorer for similar messages",
            "Communicate the verdict to the user (safe or phishing)",
            "If phishing, purge matching emails and block the sender domain",
            "If legitimate, advise the user to proceed and whitelist if needed",
        ],
    ],
))

register(ScenarioTemplate(
    scenario_id="sec-020",
    category=Category.SECURITY,
    priority=Priority.P3,
    assigned_team=Team.SECOPS,
    needs_escalation=False,
    missing_information=[MissingInfo.ERROR_MESSAGE, MissingInfo.AFFECTED_SYSTEM, MissingInfo.CONFIGURATION_DETAILS],
    subjects=[
        "DLP policy blocking me from sending email with attachment",
        "Can't email client statement — DLP policy keeps blocking it",
        "Data loss prevention policy preventing legitimate business email",
    ],
    descriptions=[
        "I'm trying to send a quarterly account statement to a client via email but the DLP policy "
        "keeps blocking it. The error says the email contains sensitive information (account numbers "
        "and SSN patterns). This is a legitimate client communication — I need to send their "
        "statement as part of our normal business process. I'm a financial advisor and I send these "
        "every quarter. It worked fine last quarter.",
        "Our DLP policy is blocking an email I need to send to our external auditors. The attachment "
        "is an Excel file with financial data that they've requested for the annual audit. The "
        "policy tip says 'This message contains sensitive information that your organization doesn't "
        "allow to be sent externally.' I've tried removing some data but the auditors need the "
        "complete file.",
    ],
    next_best_actions=[
        "Review the DLP policy match details and determine if the email is a legitimate business "
        "need. If so, process a DLP override or adjust the policy to allow this communication type.",
        "Check the specific DLP rule that triggered and verify the content sensitivity. If the "
        "email is legitimate, grant a policy exception or recommend a secure sharing alternative.",
    ],
    remediation_steps=[
        [
            "Review the DLP policy match details in the Microsoft Purview compliance portal",
            "Verify the content the policy flagged and confirm it matches a legitimate business use",
            "If legitimate, process a DLP policy override or exception for this communication",
            "Alternatively, recommend using a secure file sharing method (encrypted email or portal)",
            "If the policy is too aggressive, submit a policy tuning request to reduce false positives",
            "Confirm with the user that the email was sent or provide an alternative method",
        ],
    ],
))

register(ScenarioTemplate(
    scenario_id="sec-021",
    category=Category.SECURITY,
    priority=Priority.P4,
    assigned_team=Team.SECOPS,
    needs_escalation=False,
    missing_information=[MissingInfo.CONTACT_INFO],
    subjects=[
        "Question about security awareness training deadline",
        "How do I complete the annual security training?",
        "Security awareness training — can't find the module in LMS",
    ],
    descriptions=[
        "I received a reminder that my annual security awareness training is due by the end of the "
        "month but I can't find the training module in our learning management system. I've searched "
        "for 'security awareness' and 'phishing training' but nothing comes up. I'm in the "
        "{department} team and I want to make sure I complete it before the deadline. Can someone "
        "point me to the right course?",
        "I completed the security awareness training last week but my manager says I'm still showing "
        "as non-compliant on the training dashboard. I definitely finished all the modules and passed "
        "the quiz with 90%. Can someone update my completion status? I don't want this to affect my "
        "compliance record.",
    ],
    next_best_actions=[
        "Verify the user's training enrollment status in the LMS and provide direct access to the "
        "correct training module or troubleshoot the completion status.",
        "Check the LMS for the user's training record. If completed, manually update the compliance "
        "dashboard. If not enrolled, provide the enrollment link.",
    ],
    remediation_steps=[
        [
            "Check the user's enrollment and completion status in the learning management system",
            "If not enrolled, provide the direct link to the security awareness training course",
            "If completed but not reflected, verify the completion record with the LMS administrator",
            "Manually update the compliance dashboard if needed",
            "Confirm with the user that their training status shows as complete",
        ],
    ],
))

register(ScenarioTemplate(
    scenario_id="sec-022",
    category=Category.SECURITY,
    priority=Priority.P1,
    assigned_team=Team.SECOPS,
    needs_escalation=True,
    missing_information=[MissingInfo.AFFECTED_USERS, MissingInfo.TIMESTAMP, MissingInfo.AFFECTED_SYSTEM],
    subjects=[
        "CRITICAL: Suspicious OAuth app consent grant in Entra ID",
        "Unauthorized third-party app granted access to user mailboxes",
        "Entra ID alert — bulk OAuth consent grants detected",
    ],
    descriptions=[
        "Entra ID protection flagged a risky consent grant — a third-party OAuth application called "
        "'SecureMailBackup Pro' was granted Mail.Read, Mail.ReadWrite, and Files.ReadWrite.All "
        "permissions by 8 users in the trading division this morning. The app publisher is "
        "unverified and the app ID (a3f7c912-4d8e-4b2a-9e1f-6c3d5a8b7e9f) doesn't match any "
        "approved applications. This looks like a consent phishing attack giving the attacker "
        "read/write access to mailboxes and OneDrive files.",
        "We detected an OAuth application with delegated permissions being consented to by multiple "
        "users across the organization. The app requests Calendars.ReadWrite, Contacts.Read, and "
        "Mail.Send permissions. The consent page was presented via a phishing link. At least 12 "
        "users have granted consent so far. The app can now read their email and send messages on "
        "their behalf.",
    ],
    next_best_actions=[
        "Immediately revoke the OAuth app's service principal and all granted permissions in Entra "
        "ID. Revoke refresh tokens for all affected users. Investigate what data the app accessed.",
        "Block the malicious OAuth app at the tenant level and revoke its service principal. Force "
        "re-authentication for all users who consented and audit their mailbox activity.",
    ],
    remediation_steps=[
        [
            "Remove the malicious OAuth application's service principal from Entra ID",
            "Revoke all permissions and consent grants associated with the application",
            "Identify all users who granted consent using the Entra ID enterprise applications audit",
            "Revoke refresh tokens and force re-authentication for all affected users",
            "Review the app's access logs to determine what data was accessed or exfiltrated",
            "Check affected users' mailboxes for forwarding rules or other persistence mechanisms",
            "Configure Entra ID to require admin consent for high-risk permissions",
            "Block the app ID in the tenant-wide app consent policies",
            "Notify affected users about the incident and monitor for follow-up attacks",
        ],
    ],
))

register(ScenarioTemplate(
    scenario_id="sec-023",
    category=Category.SECURITY,
    priority=Priority.P3,
    assigned_team=Team.SECOPS,
    needs_escalation=False,
    missing_information=[
        MissingInfo.AFFECTED_SYSTEM,
        MissingInfo.ENVIRONMENT_DETAILS,
        MissingInfo.CONFIGURATION_DETAILS,
    ],
    subjects=[
        "Need a code signing certificate for internal deployment tool",
        "Request for code signing certificate — internal application",
        "Code signing cert needed for automated deployment pipeline",
    ],
    descriptions=[
        "Our development team needs a code signing certificate to sign our internal portfolio "
        "analytics application before deploying it to advisor workstations. Currently, Defender "
        "flags the unsigned executable and SmartScreen blocks it for new users. We need an internal "
        "code signing certificate issued by our enterprise CA. The application is "
        "PortfolioAnalytics.exe and it's distributed via SCCM.",
        "I'm requesting a code signing certificate for our internal automation scripts that run "
        "as part of the nightly trade reconciliation process. The PowerShell execution policy "
        "requires signed scripts and we need to sign about 15 scripts that are deployed to the "
        "reconciliation servers. We currently use a certificate that expires next month.",
    ],
    next_best_actions=[
        "Verify the requester's authorization and the application's approval status. Issue a code "
        "signing certificate from the internal PKI if the request meets policy requirements.",
        "Review the code signing certificate request against the internal PKI policy. Confirm the "
        "application is approved and issue the certificate with appropriate key usage constraints.",
    ],
    remediation_steps=[
        [
            "Verify the requester has authorization to request code signing certificates",
            "Confirm the application is listed in the approved internal software inventory",
            "Generate a code signing certificate from the enterprise certificate authority",
            "Configure appropriate key usage, validity period, and revocation settings",
            "Deliver the certificate securely to the development team",
            "Verify the signed application or scripts pass Defender and execution policy checks",
            "Add the certificate to the tracking system for renewal monitoring",
        ],
    ],
))

register(ScenarioTemplate(
    scenario_id="sec-024",
    category=Category.SECURITY,
    priority=Priority.P1,
    assigned_team=Team.SECOPS,
    needs_escalation=True,
    missing_information=[MissingInfo.AFFECTED_SYSTEM, MissingInfo.NETWORK_LOCATION, MissingInfo.BUSINESS_IMPACT],
    subjects=[
        "CRITICAL: Alert from managed detection service — active threat detected",
        "MDR provider escalating active intrusion on network",
        "Managed security service reporting command-and-control traffic",
    ],
    descriptions=[
        "Our managed detection and response (MDR) provider CrowdStrike just escalated a critical "
        "alert. They've detected command-and-control (C2) beaconing traffic from three internal "
        "workstations to a known threat actor infrastructure at 185.220.101.42:443. The beaconing "
        "pattern is consistent with Cobalt Strike. The affected machines are in the 10.50.20.0/24 "
        "subnet which is our trading floor network. CrowdStrike recommends immediate isolation of "
        "the affected hosts. Their incident reference is CS-INC-2024-7823.",
        "Our managed security service provider detected suspicious lateral movement activity in our "
        "network. An account (svc_backup) is being used to authenticate to multiple servers across "
        "different segments using pass-the-hash techniques. The activity originated from a "
        "workstation in the compliance department and has spread to 7 servers in the past 4 hours. "
        "The MSSP has classified this as a high-confidence active intrusion.",
    ],
    next_best_actions=[
        "Immediately isolate the affected endpoints and coordinate with the MDR provider for a "
        "joint investigation. Activate the incident response plan and notify executive leadership. "
        "This is an active intrusion requiring immediate containment.",
        "Begin containment by isolating compromised hosts and disabling the compromised service "
        "account. Coordinate with the MSSP for threat intelligence and containment guidance. "
        "Preserve all forensic evidence.",
    ],
    remediation_steps=[
        [
            "Immediately isolate all identified compromised endpoints via network segmentation",
            "Disable the compromised service account and reset its credentials",
            "Coordinate with the MDR provider for detailed indicators of compromise (IOCs)",
            "Block the C2 IP addresses and domains at the firewall and proxy level",
            "Run IOC sweeps across all endpoints using Defender for Endpoint advanced hunting",
            "Check for persistence mechanisms on compromised hosts",
            "Engage external incident response if the scope exceeds internal capacity",
            "Notify executive leadership and legal about the active intrusion",
            "Preserve all logs and forensic evidence for potential law enforcement engagement",
            "Begin full incident timeline reconstruction",
        ],
    ],
))

register(ScenarioTemplate(
    scenario_id="sec-025",
    category=Category.SECURITY,
    priority=Priority.P2,
    assigned_team=Team.SECOPS,
    needs_escalation=False,
    missing_information=[MissingInfo.AFFECTED_USERS, MissingInfo.AFFECTED_SYSTEM, MissingInfo.CONFIGURATION_DETAILS],
    subjects=[
        "Data classification policy violation flagged on SharePoint site",
        "Purview flagged unclassified sensitive documents in team site",
        "Sensitive data found in improperly classified SharePoint library",
    ],
    descriptions=[
        "Microsoft Purview information protection flagged 47 documents in the Wealth Management "
        "team's SharePoint site that contain client PII (Social Security numbers, bank account "
        "numbers) but are classified as 'General' instead of 'Highly Confidential'. These documents "
        "are in a library that's shared with all employees rather than restricted to the wealth "
        "management team. The documents include client onboarding forms, account applications, and "
        "beneficiary designations from the past 6 months.",
        "An automated Purview scan identified a SharePoint document library in the {department} "
        "department that contains approximately 120 files with sensitive financial data that are "
        "not properly labeled. The files include trading records, client correspondence with account "
        "details, and internal financial projections. Currently, anyone in the organization can "
        "access these documents through search.",
    ],
    next_best_actions=[
        "Immediately restrict access to the affected SharePoint library while the documents are "
        "reclassified. Apply the correct sensitivity labels to protect client PII.",
        "Restrict the document library permissions to the appropriate team only. Apply bulk "
        "sensitivity labels using Purview auto-labeling policies.",
    ],
    remediation_steps=[
        [
            "Restrict the SharePoint library permissions to only the owning team immediately",
            "Remove the library from enterprise search results until classified properly",
            "Apply the correct sensitivity labels (Highly Confidential) to affected documents",
            "Use Purview auto-labeling to bulk-apply labels based on content inspection",
            "Verify that encryption and access restrictions are enforced by the labels",
            "Audit who accessed the improperly classified documents during the exposure period",
            "Notify the site owner and their manager about the policy violation",
            "Schedule a data classification training session for the affected team",
        ],
    ],
))

register(ScenarioTemplate(
    scenario_id="sec-026",
    category=Category.SECURITY,
    priority=Priority.P2,
    assigned_team=Team.SECOPS,
    needs_escalation=False,
    missing_information=[MissingInfo.PREVIOUS_TICKET_ID, MissingInfo.SCREENSHOT_OR_ATTACHMENT],
    subjects=[
        "Same user targeted by phishing AGAIN — third time this quarter",
        "Recurring phishing attempts on one employee — prior incidents on file",
        "Repeat phishing targeting — this has happened before",
    ],
    descriptions=[
        "One of our senior advisors is being targeted by phishing emails again. This is at least "
        "the third time this quarter. We had incidents reported previously where they received "
        "highly targeted spear-phishing emails impersonating our CEO and a major client. The "
        "advisor didn't save the previous ticket numbers but says IT handled them each time. This "
        "latest email claims to be from our custodian bank requesting wire transfer confirmation. "
        "The advisor deleted the email before forwarding it or taking a screenshot.",
        "We're seeing another phishing campaign targeting the same group in the trading division. "
        "The SOC handled similar incidents in the past but I don't have the previous incident "
        "references. This time the phishing email had a QR code leading to a credential "
        "harvesting page. Unfortunately, the user clicked 'Report Phishing' in Outlook which "
        "removed the email before we could capture a screenshot of the content.",
    ],
    next_best_actions=[
        "Search for previous phishing incidents involving this user to establish a pattern. "
        "Recover the email from quarantine or message trace and analyze the threat.",
    ],
    remediation_steps=[
        [
            "Search the ticketing system for prior phishing incidents involving the same user",
            "Recover the deleted or reported email from the quarantine or admin message trace",
            "Analyze the email headers, sender, and any URLs or attachments",
            "Check if the user clicked any links or entered credentials — reset password if so",
            "Block the sender domain and phishing URLs at the email gateway",
            "Escalate to the threat intelligence team if this is a persistent targeted campaign",
            "Consider additional protection for the user (VIP mailbox monitoring, stricter filtering)",
        ],
    ],
))

register(ScenarioTemplate(
    scenario_id="sec-027",
    category=Category.SECURITY,
    priority=Priority.P1,
    assigned_team=Team.SECOPS,
    needs_escalation=True,
    missing_information=[MissingInfo.AUTHENTICATION_METHOD, MissingInfo.TIMESTAMP],
    subjects=[
        "MFA bypass attempt detected on executive account",
        "Alert: possible MFA bypass — suspicious sign-in succeeded",
        "Authentication anomaly — MFA challenge may have been bypassed",
    ],
    descriptions=[
        "Entra ID Protection flagged a sign-in to an executive's account that appears to have "
        "bypassed MFA. The sign-in was marked as satisfied for MFA but the user says they didn't "
        "approve any MFA prompt at that time. We're not sure what MFA method the executive has "
        "registered — it could be push notification, phone call, or a hardware token. The alert "
        "doesn't specify the exact time clearly, just 'early this morning.'",
        "A suspicious successful authentication was detected on a senior VP's account from an "
        "unusual location. The sign-in log shows MFA was completed but the user denies approving "
        "anything. We need to determine which MFA method was used to complete the challenge and "
        "whether it was a token theft, session hijack, or MFA fatigue attack. The exact timestamp "
        "is unclear from the initial alert.",
    ],
    next_best_actions=[
        "Immediately revoke all sessions for the affected account. Identify the MFA method used "
        "and the exact sign-in time from Entra ID logs to determine if this was a legitimate bypass.",
    ],
    remediation_steps=[
        [
            "Revoke all refresh tokens and active sessions for the affected account immediately",
            "Pull the detailed sign-in log from Entra ID to identify the exact timestamp and MFA method",
            "Determine if the MFA challenge was satisfied via push approval, phone call, TOTP, or FIDO2",
            "Check for MFA fatigue patterns (repeated push notifications followed by an approval)",
            "Review conditional access policy evaluation for the sign-in event",
            "If compromise is confirmed, reset the user's password and re-register MFA methods",
            "Enable number matching and additional context for MFA push notifications",
            "Brief the executive on the incident and monitor for further anomalous activity",
        ],
    ],
))

register(ScenarioTemplate(
    scenario_id="sec-028",
    category=Category.SECURITY,
    priority=Priority.P2,
    assigned_team=Team.SECOPS,
    needs_escalation=False,
    missing_information=[MissingInfo.SCREENSHOT_OR_ATTACHMENT, MissingInfo.PREVIOUS_TICKET_ID],
    subjects=[
        "Suspicious login alert keeps recurring — same pattern as before",
        "Repeated impossible-travel alert — saw this last month too",
        "Another suspicious activity alert on the same account",
    ],
    descriptions=[
        "I'm getting impossible-travel alerts for the same user account again. This happened last "
        "month and we investigated it — turned out to be a VPN issue. But I don't have the "
        "previous incident ID to reference. The alert is showing logins from New York and "
        "Singapore within 10 minutes. I dismissed the alert in the portal before taking a "
        "screenshot of the details, so I don't have the full alert data anymore.",
        "Defender for Identity keeps flagging suspicious lateral movement from the same service "
        "account we investigated before. There was a prior security incident ticket for this "
        "but I can't find the reference number. The alert dashboard shows a red indicator but "
        "I didn't capture the alert details before the system auto-resolved it. We need to "
        "determine if this is the same false positive or a new genuine threat.",
    ],
    next_best_actions=[
        "Retrieve the alert details from the Defender portal's history. Search for prior "
        "incident tickets to determine if this is a known false positive or a new threat.",
    ],
    remediation_steps=[
        [
            "Retrieve the full alert details from the Defender portal's alert history or API",
            "Search the ticketing system for previous incidents involving the same account",
            "Compare the current alert indicators with the prior incident's root cause",
            "If it matches the prior false positive, create a suppression rule with documentation",
            "If the pattern differs, investigate as a new potential compromise",
            "Document the alert with full details and link to any prior incident tickets",
        ],
    ],
))

register(ScenarioTemplate(
    scenario_id="sec-029",
    category=Category.SECURITY,
    priority=Priority.P1,
    assigned_team=Team.SECOPS,
    needs_escalation=True,
    missing_information=[MissingInfo.AUTHENTICATION_METHOD, MissingInfo.CONTACT_INFO],
    subjects=[
        "Security key may be compromised — user unsure which type",
        "Lost or stolen hardware security key — potential credential compromise",
        "Employee's authentication device possibly stolen",
    ],
    descriptions=[
        "An employee reports that their security key may have been stolen from their bag during "
        "their commute. They're not sure exactly what kind of key it is — they think it's a "
        "YubiKey but it might be a different brand. They use it for logging into everything. "
        "The employee called from a colleague's phone and didn't leave a direct number — they "
        "said they'd try to come to the IT desk but they're not sure when. We need to disable "
        "the key immediately.",
        "A manager reported that one of their team members lost their hardware authentication "
        "device. The manager isn't sure what type it is — FIDO2, smart card, or something else. "
        "The affected employee is currently traveling and unreachable by phone. The manager "
        "doesn't have the employee's current contact information since they're overseas. We need "
        "to secure the account as a precaution.",
    ],
    next_best_actions=[
        "Immediately disable all hardware security key credentials for the user in Entra ID. "
        "Obtain contact details to reach the affected employee for verification.",
    ],
    remediation_steps=[
        [
            "Look up the user's registered authentication methods in Entra ID to identify the key type",
            "Immediately disable or remove the FIDO2 security key registration from the account",
            "Revoke all active sessions and refresh tokens for the user",
            "Obtain the user's current contact information through their manager or HR",
            "Contact the user to verify the report and assess whether the key was used after loss",
            "Issue a temporary authentication method until a replacement security key is provisioned",
            "Review sign-in logs for any suspicious authentications using the lost key",
            "Order and provision a replacement security key for the user",
        ],
    ],
))

register(ScenarioTemplate(
    scenario_id="sec-030",
    category=Category.SECURITY,
    priority=Priority.P2,
    assigned_team=Team.SECOPS,
    needs_escalation=False,
    missing_information=[MissingInfo.PREVIOUS_TICKET_ID, MissingInfo.CONTACT_INFO],
    subjects=[
        "DLP violation by the same user again — prior incident exists",
        "Repeat DLP policy violation — second occurrence this quarter",
        "Another data loss prevention trigger from same department",
    ],
    descriptions=[
        "We have another DLP policy violation from the same employee who triggered one last month. "
        "They attempted to upload client financial data to a personal cloud storage service. There "
        "was a previous incident and I believe the user was given a warning, but I don't have the "
        "prior ticket number. The user's manager needs to be notified but the manager recently "
        "changed and I don't have the new manager's contact details.",
        "A DLP alert fired for an employee trying to email a spreadsheet with client SSNs to a "
        "personal Gmail address. Purview shows this is the same type of violation we dealt with "
        "previously for this user — they were supposed to complete remedial training after the "
        "last incident. I can't find the original ticket reference and the employee's listed "
        "manager in the directory left the company last week, so I don't know who to escalate to.",
    ],
    next_best_actions=[
        "Block the data transfer and locate the previous DLP incident for this user. Identify "
        "the user's current manager through HR for escalation of a repeat violation.",
    ],
    remediation_steps=[
        [
            "Verify the DLP policy blocked the data transfer successfully",
            "Search the ticketing system for the user's prior DLP violation tickets",
            "Identify the user's current manager through HR or the corporate directory",
            "Notify the current manager about the repeat DLP violation",
            "Review whether the user completed the required remedial training from the prior incident",
            "If this is a second violation, escalate per the data handling policy (formal warning or HR action)",
            "Document the incident with references to all prior violations",
        ],
    ],
))
