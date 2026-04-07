"""Security & Compliance scenario definitions."""

from generator.models import Scenario

SCENARIOS: list[Scenario] = [
    # ── 1. Phishing email received but NOT clicked ───────────────────────────
    Scenario(
        scenario_id="sec-phishing-reported",
        category="Security & Compliance",
        priority="P3",
        assigned_team="Security Operations",
        needs_escalation=True,
        missing_information=["timestamp", "screenshot_or_attachment"],
        subjects=[
            "Suspicious email — didn't click anything",
            "Possible phishing email in my inbox",
            "Reporting a suspicious email I received",
            "Got a weird email pretending to be IT — did NOT click",
        ],
        descriptions=[
            "I received an email claiming to be from our IT department asking me to verify my credentials via a link. "
            "The sender address looked off — it was something like support@contoso-security.net instead of our real "
            "domain. I did NOT click the link or download any attachments. I wanted to report it so the security team "
            "can investigate.",
            "Got an email this morning that looks like a phishing attempt. Subject line was 'Urgent: Verify Your "
            "Account'. The from address doesn't match our corporate domain. I haven't interacted with it at all — just "
            "flagging it for the SOC.",
            "Reporting a suspicious email that landed in my inbox around 9:15 AM. It asks me to 'confirm my identity' "
            "through an external link. The branding looks like ours but the URL is clearly wrong. I did not click "
            "anything.",
        ],
        next_best_actions=[
            "Acknowledge report and collect the original email headers for analysis. Check if other users received the "
            "same message.",
            "Thank the reporter, extract email headers and URLs for threat intel analysis, and check email gateway logs"
            " for campaign scope.",
        ],
        remediation_steps=[
            [
                "Collect the original email (full headers) from the reporter",
                "Submit URLs and attachments to the threat intelligence platform for analysis",
                "Query email gateway logs to determine campaign scope and affected recipients",
                "Block sender domain and malicious URLs at the email gateway",
                "Send targeted advisory to affected users if campaign is widespread",
                "Update phishing detection rules based on indicators of compromise",
            ],
        ],
        tags=["phishing", "email-security"],
    ),
    # ── 2. Phishing email clicked — credentials entered ──────────────────────
    Scenario(
        scenario_id="sec-phishing-credentials-compromised",
        category="Security & Compliance",
        priority="P1",
        assigned_team="Security Operations",
        needs_escalation=True,
        missing_information=["timestamp", "affected_system", "authentication_method"],
        subjects=[
            "URGENT — I clicked a phishing link and entered my password",
            "Think I fell for a phishing email — entered my credentials",
            "Accidentally gave my password to a fake login page",
            "Phishing email — I entered my username and password before realizing",
        ],
        descriptions=[
            "I'm really sorry but I clicked a link in an email that looked like it was from our HR department about "
            "benefits enrollment. It took me to a page that looked exactly like our login portal and I entered my full "
            "credentials before I realized the URL was wrong. I immediately closed the browser. My employee ID handles "
            "access to the trading floor reconciliation systems and I have access to client PII in Salesforce.",
            "I received an email about a mandatory compliance training and clicked the link without checking. It "
            "prompted me for my credentials and I entered them. The page then showed an error and redirected me to our "
            "real intranet. I think my account may be compromised. I have access to the SOX-regulated financial "
            "reporting tools.",
            "Fell for a phishing email about 30 minutes ago. I entered my AD credentials on a fake page. I have "
            "privileged access to several production databases with customer financial data. Please help — I'm worried "
            "about a data breach.",
        ],
        next_best_actions=[
            "IMMEDIATE: Force password reset for the compromised account. Revoke all active sessions and MFA tokens. "
            "Begin forensic review of account activity since compromise.",
            "Trigger the credential compromise incident response playbook. Reset credentials, revoke sessions, and "
            "check for unauthorized access to sensitive systems.",
        ],
        remediation_steps=[
            [
                "Immediately force-reset the user's password and revoke all active sessions",
                "Revoke and re-provision MFA tokens for the compromised account",
                "Review Azure AD sign-in logs for the account from the last 72 hours",
                "Check for mail forwarding rules or inbox rules added to the account",
                "Audit access to sensitive systems (trading, PII, financial reporting)",
                "Submit the phishing email to threat intelligence for indicator extraction",
                "Block malicious URLs and sender domains at the email gateway",
                "Determine if any data was exfiltrated; if so, initiate breach notification procedures",
                "File incident report per Contoso Financial Services IR policy",
            ],
        ],
        tags=["phishing", "credential-compromise", "incident-response"],
    ),
    # ── 3. Suspicious login from foreign country ─────────────────────────────
    Scenario(
        scenario_id="sec-suspicious-foreign-login",
        category="Security & Compliance",
        priority="P2",
        assigned_team="Security Operations",
        needs_escalation=True,
        missing_information=["timestamp", "network_location", "authentication_method"],
        subjects=[
            "Suspicious login alert from another country on my account",
            "Got an alert — someone logged in from overseas?",
            "Azure AD impossible travel alert on my account",
            "Sign-in from foreign country I've never visited",
        ],
        descriptions=[
            "I just received an alert from Azure AD that my account was signed into from an IP address in Eastern "
            "Europe. I'm currently at our New York office and haven't traveled recently. I don't use a VPN. I have "
            "access to the client portfolio management system and several internal financial tools.",
            "Our SIEM flagged an impossible travel alert for my account — a successful sign-in from Southeast Asia at 3"
            " AM ET last night, followed by a normal login from my home in Connecticut at 7 AM. I definitely wasn't tra"
            "veling. My account has access to compliance reporting dashboards.",
            "I received a suspicious sign-in notification for a login from Brazil. I haven't been to Brazil and I don't"
            " know anyone there. I'm concerned my account may be compromised. I have read access to several SharePoint "
            "sites containing client financial data.",
        ],
        next_best_actions=[
            "Verify with the user that the sign-in was not legitimate. If confirmed suspicious, force password reset "
            "and revoke sessions. Investigate sign-in logs for lateral movement.",
            "Confirm the sign-in is unauthorized, initiate account containment, and correlate the IP with known threat "
            "intelligence feeds.",
        ],
        remediation_steps=[
            [
                "Confirm with the user that the foreign sign-in is unauthorized",
                "Force password reset and revoke all active sessions",
                "Review Azure AD sign-in and audit logs for additional suspicious activity",
                "Check for newly created mail forwarding rules or app registrations",
                "Correlate the source IP with threat intelligence databases",
                "Review Conditional Access policies for gaps (consider named locations)",
                "Document findings and close or escalate based on evidence of compromise",
            ],
        ],
        tags=["suspicious-login", "impossible-travel", "identity-threat"],
    ),
    # ── 4. DLP alert — sensitive data shared externally ──────────────────────
    Scenario(
        scenario_id="sec-dlp-external-share",
        category="Security & Compliance",
        priority="P1",
        assigned_team="Security Operations",
        needs_escalation=True,
        missing_information=[
            "affected_system",
            "business_impact",
            "affected_users",
        ],
        subjects=[
            "DLP alert — sensitive financial data shared outside the org",
            "Data Loss Prevention triggered — PII sent to external recipient",
            "URGENT: DLP policy violation — client data emailed externally",
            "Compliance alert — confidential data shared with external party",
        ],
        descriptions=[
            "Our DLP system flagged an email sent by a user in the Wealth Management division to a personal Gmail "
            "address. The email contained an Excel attachment with client Social Security numbers, account balances, "
            "and portfolio details for approximately 200 clients. This is a potential SOX and GDPR violation.",
            "Microsoft Purview DLP triggered a high-severity alert: a user shared a SharePoint folder containing SEC "
            "pre-filing documents with an external collaborator who is not authorized. The folder includes draft 10-K "
            "filings and internal audit notes. This could constitute a material information leak.",
            "DLP alert fired at 2:47 PM — a contractor in the finance department uploaded a file to a personal OneDrive"
            " account containing client tax identification numbers and account statements. The file contains records fo"
            "r over 500 clients across three regional offices.",
        ],
        next_best_actions=[
            "IMMEDIATE: Contain the data exposure by revoking external sharing links and quarantining the email. Begin "
            "compliance impact assessment.",
            "Invoke the data leakage incident response procedure. Revoke access, preserve evidence, and assess "
            "regulatory notification requirements.",
        ],
        remediation_steps=[
            [
                "Immediately revoke external sharing links and quarantine the outbound email",
                "Preserve all audit logs and evidence for compliance investigation",
                "Identify the full scope of exposed data (record count, data types, affected clients)",
                "Notify the compliance team and legal counsel for regulatory assessment",
                "Contact the external recipient to request deletion and confirmation",
                "Assess notification requirements under GDPR, SOX, and state breach laws",
                "Review and tighten DLP policies to prevent recurrence",
                "File incident report and update the risk register",
            ],
        ],
        tags=["dlp", "data-leakage", "compliance", "sox", "gdpr"],
    ),
    # ── 5. Malware / ransomware detected by Defender ─────────────────────────
    Scenario(
        scenario_id="sec-malware-ransomware-detected",
        category="Security & Compliance",
        priority="P1",
        assigned_team="Security Operations",
        needs_escalation=True,
        missing_information=["device_info", "timestamp", "network_location"],
        subjects=[
            "URGENT — Defender detected ransomware on my workstation",
            "Malware alert — files are being encrypted on my laptop",
            "Microsoft Defender flagged active ransomware — need help NOW",
            "Ransomware detected — workstation quarantined",
        ],
        descriptions=[
            "Microsoft Defender for Endpoint just popped up a critical alert on my workstation saying it detected "
            "ransomware behavior. Some of my local files have been renamed with a .locked extension. I immediately "
            "disconnected from WiFi. I'm in the trading operations group and this machine has cached credentials for "
            "Bloomberg and our order management system.",
            "I opened a file from what I thought was a legitimate vendor email and now Defender is showing multiple "
            "critical alerts. My desktop background changed to a ransom note and I can see files being encrypted in "
            "real-time. I've unplugged the ethernet cable. This is a workstation on the trading floor network segment.",
            "Getting multiple Defender alerts about Trojan:Win32/Conti.A on my workstation. Several files are already e"
            "ncrypted. I pulled the network cable immediately. I'm concerned about lateral spread — I was connected to "
            "three shared network drives when this started.",
        ],
        next_best_actions=[
            "IMMEDIATE: Confirm network isolation of the affected device. Invoke the ransomware incident response "
            "playbook. Assess scope of encryption and potential lateral movement.",
            "Trigger ransomware IR playbook. Verify device isolation, identify patient zero, and assess lateral "
            "movement risk across the network segment.",
        ],
        remediation_steps=[
            [
                "Confirm the device is fully isolated from the network (no WiFi, Ethernet, or VPN)",
                "Invoke the ransomware incident response playbook and assemble the IR team",
                "Identify the ransomware variant from Defender alerts and IOCs",
                "Scan all network segments for indicators of lateral movement",
                "Isolate any additional affected endpoints via Defender for Endpoint",
                "Preserve forensic evidence (memory dump, disk image) before remediation",
                "Restore affected files from clean backups after confirming no persistence",
                "Reset all credentials that were cached or used on the affected workstation",
                "Conduct post-incident review and update endpoint protection policies",
                "File regulatory incident report if client data was potentially affected",
            ],
        ],
        tags=["ransomware", "malware", "incident-response", "critical"],
    ),
    # ── 6. Data breach — PII exposed on SharePoint ───────────────────────────
    Scenario(
        scenario_id="sec-pii-breach-sharepoint",
        category="Security & Compliance",
        priority="P1",
        assigned_team="Security Operations",
        needs_escalation=True,
        missing_information=[
            "affected_users",
            "business_impact",
            "timestamp",
        ],
        subjects=[
            "CRITICAL — Client PII found on publicly accessible SharePoint site",
            "Data breach — sensitive client data exposed on SharePoint",
            "PII exposure — client records found on improperly secured site",
            "URGENT: SharePoint site with client SSNs is accessible to all employees",
        ],
        descriptions=[
            "During a routine access review, I discovered a SharePoint site in the Wealth Management division that "
            "contains spreadsheets with client Social Security numbers, dates of birth, account numbers, and net worth "
            "figures. The site permissions are set to 'Everyone except external users' — meaning all 4,000+ Contoso "
            "employees can access it. This has been in place since at least Q2 2024.",
            "A colleague forwarded me a link to a SharePoint document library that contains unencrypted client PII "
            "including tax IDs, bank routing numbers, and investment account details. The library is shared with the "
            "entire organization. We estimate over 15,000 client records are exposed. This is a serious regulatory "
            "concern under GDPR and state privacy laws.",
            "I found a SharePoint site belonging to the Client Onboarding team that has full client Know Your Customer "
            "(KYC) documents — passports, utility bills, tax returns — with permissions open to the entire company. "
            "Some of these documents appear to be for European clients which makes this a GDPR issue as well.",
        ],
        next_best_actions=[
            "IMMEDIATE: Restrict SharePoint site permissions to authorized personnel only. Begin data exposure "
            "assessment and engage the compliance and legal teams.",
            "Lock down the SharePoint site permissions immediately. Initiate the data breach response procedure and "
            "assess regulatory notification obligations.",
        ],
        remediation_steps=[
            [
                "Immediately restrict SharePoint site permissions to the minimum required group",
                "Generate SharePoint audit logs to determine who accessed the data and when",
                "Quantify the breach: number of records, data types, duration of exposure",
                "Notify the Chief Privacy Officer, compliance team, and legal counsel",
                "Assess regulatory notification requirements (GDPR 72-hour window, state laws)",
                "Engage external counsel if client notification is required",
                "Conduct a broader SharePoint permissions audit across the organization",
                "Implement sensitivity labels and DLP policies for PII-containing sites",
                "File incident report and update the data protection risk register",
            ],
        ],
        tags=["data-breach", "pii", "sharepoint", "compliance", "gdpr"],
    ),
    # ── 7. Compliance audit finding — immediate remediation needed ────────────
    Scenario(
        scenario_id="sec-compliance-audit-finding",
        category="Security & Compliance",
        priority="P1",
        assigned_team="Security Operations",
        needs_escalation=False,
        missing_information=["affected_system", "configuration_details", "business_impact"],
        subjects=[
            "Compliance audit finding — immediate remediation required",
            "SOX audit deficiency — critical control gap identified",
            "Regulatory audit finding needs urgent IT remediation",
            "External audit flagged critical security control failure",
        ],
        descriptions=[
            "Our external auditors (Deloitte) identified a critical deficiency during the SOX IT General Controls audit"
            ": privileged access reviews for the core banking platform have not been completed for the last two quarter"
            "s. This is a material weakness finding that must be remediated before the audit report is finalized in 3 w"
            "eeks. We need IT to provide evidence of completed reviews or perform them immediately.",
            "The SEC examination team flagged that our production change management process for the trade execution "
            "platform does not have documented evidence of segregation of duties. Specifically, the same individuals "
            "who develop changes are also approving and deploying them. This needs to be remediated with documented "
            "evidence within 10 business days.",
            "Internal audit completed a PCI-DSS readiness assessment and found that network segmentation between the ca"
            "rdholder data environment and the corporate network is insufficient. We have 30 days to remediate before o"
            "ur official PCI assessment. This requires immediate coordination between network ops and security.",
        ],
        next_best_actions=[
            "Engage the relevant IT teams to assess the finding and create a remediation plan with specific deadlines. "
            "Coordinate with the compliance team on evidence requirements.",
            "Assemble a remediation task force, assess the control gap, and establish a timeline that meets audit "
            "deadlines.",
        ],
        remediation_steps=[
            [
                "Review the audit finding in detail with the compliance team",
                "Identify the specific control gap and affected systems",
                "Assign remediation owners and establish a timeline within audit deadlines",
                "Implement the required controls or compensating controls",
                "Collect and organize evidence of remediation (screenshots, logs, approvals)",
                "Submit remediation evidence to the compliance team for auditor review",
                "Schedule follow-up verification to ensure controls remain effective",
            ],
        ],
        tags=["compliance", "audit", "sox", "regulatory"],
    ),
    # ── 8. USB device policy violation detected ──────────────────────────────
    Scenario(
        scenario_id="sec-usb-policy-violation",
        category="Security & Compliance",
        priority="P3",
        assigned_team="Endpoint Engineering",
        needs_escalation=False,
        missing_information=["device_info", "business_impact", "affected_users"],
        subjects=[
            "USB device blocked — need to use external drive for work",
            "Endpoint protection blocked my USB drive",
            "Can't use USB flash drive — Defender policy blocking it",
            "USB device policy violation — need exception or resolution",
        ],
        descriptions=[
            "I plugged in a USB flash drive to transfer some presentation files to a conference room PC and Defender fo"
            "r Endpoint blocked it with a policy violation. I understand the security policy but I need a way to move t"
            "hese files. Is there an approved process for temporary USB exceptions?",
            "I received a notification that my USB external hard drive was blocked by company policy. I use this drive "
            "to back up large design files that are too big for OneDrive sync. Can IT provide an alternative solution "
            "or grant an exception?",
            "Our team received new USB security tokens from a vendor for a client project, but the endpoint protection "
            "is blocking them. We need these devices whitelisted for the project. They're hardware authentication "
            "tokens, not storage devices.",
        ],
        next_best_actions=[
            "Review the USB policy violation details and advise the user on approved file transfer alternatives. "
            "Evaluate exception request if business-justified.",
            "Investigate the specific device type and advise on policy-compliant alternatives or the exception request "
            "process.",
        ],
        remediation_steps=[
            [
                "Review the Defender for Endpoint alert to identify the specific device and violation type",
                "Determine if the use case qualifies for a USB policy exception",
                "If exception is warranted, submit a policy exception request with business justification",
                "If not, guide the user to approved file transfer methods (OneDrive, SharePoint, SFTP)",
                "Document the resolution and close the ticket",
            ],
        ],
        tags=["usb-policy", "endpoint", "dlp"],
    ),
    # ── 9. Insider threat — departing employee bulk downloading ───────────────
    Scenario(
        scenario_id="sec-insider-threat-bulk-download",
        category="Security & Compliance",
        priority="P1",
        assigned_team="Security Operations",
        needs_escalation=True,
        missing_information=[
            "affected_system",
            "timestamp",
            "business_impact",
        ],
        subjects=[
            "URGENT: Departing employee downloading large volumes of data",
            "Insider threat alert — employee in notice period bulk downloading files",
            "DLP alert — employee leaving company is exfiltrating data",
            "Suspicious bulk download activity from resigning employee",
        ],
        descriptions=[
            "HR informed us that a Senior Portfolio Manager in the Equities division submitted their two-week notice "
            "yesterday. Our UEBA system is now flagging anomalous behavior: the employee has downloaded over 12 GB of "
            "data from SharePoint in the last 8 hours, including client relationship files, proprietary trading "
            "strategies, and performance reports. They appear to be syncing everything to a personal device.",
            "Microsoft Defender for Cloud Apps alerted on a departing VP in Investment Banking who has been "
            "mass-downloading files from the M&A deal pipeline SharePoint site. The user is leaving for a competitor "
            "next month. The downloaded files include confidential pitch decks, financial models, and client contact "
            "lists totaling over 3,000 documents.",
            "A manager reported that an analyst who resigned last week has been accessing and downloading files they "
            "don't normally work with. Our DLP dashboard shows over 500 files downloaded in the past 48 hours from "
            "three different confidential project sites. The employee's last day is Friday.",
        ],
        next_best_actions=[
            "IMMEDIATE: Restrict the employee's access to sensitive repositories. Coordinate with HR and legal for an "
            "insider threat investigation. Preserve all audit evidence.",
            "Invoke the insider threat response procedure. Limit access to sensitive data, coordinate with HR and "
            "legal, and preserve forensic evidence.",
        ],
        remediation_steps=[
            [
                "Immediately restrict the employee's access to sensitive SharePoint sites and file shares",
                "Preserve all audit logs and DLP alerts as evidence",
                "Coordinate with HR and legal to determine appropriate response",
                "Review the full scope of downloaded data using Cloud App Security logs",
                "Check for any data sent to personal email, cloud storage, or USB devices",
                "If data exfiltration is confirmed, engage legal for potential litigation hold",
                "Conduct an exit interview with security awareness component",
                "Ensure all access is revoked on or before the employee's last day",
                "Document the incident and update the insider threat risk register",
            ],
        ],
        tags=["insider-threat", "data-exfiltration", "departing-employee"],
    ),
    # ── 10. SSL certificate expiring on production API gateway ────────────────
    Scenario(
        scenario_id="sec-ssl-cert-expiring-prod",
        category="Security & Compliance",
        priority="P1",
        assigned_team="Network Operations",
        needs_escalation=True,
        missing_information=[
            "affected_system",
            "environment_details",
            "configuration_details",
        ],
        subjects=[
            "URGENT — SSL certificate expiring in 48 hours on production API gateway",
            "Production API gateway certificate about to expire",
            "SSL cert renewal needed ASAP — production trading API",
            "Critical: TLS certificate for client-facing API expires this weekend",
        ],
        descriptions=[
            "The SSL/TLS certificate for our production API gateway (api.contoso-fs.com) expires in 48 hours. This "
            "gateway handles all client-facing portfolio API calls and is used by our mobile app and third-party "
            "integrations. If it expires, all client connections will fail with certificate errors. We need an "
            "emergency renewal and deployment.",
            "Monitoring alerted that the TLS certificate on our production Azure API Management instance for the "
            "trading execution API expires on Saturday at midnight. This endpoint processes approximately 50,000 "
            "transactions per day. Certificate auto-renewal failed because the certificate authority requires manual "
            "domain validation this time.",
            "The wildcard certificate for *.prod.contoso-financial.com is expiring in 3 days. It covers 14 production "
            "services including the client portal, advisor dashboard, and payment processing gateway. Our certificate "
            "management tool shows the renewal was not initiated due to a workflow approval stuck in queue.",
        ],
        next_best_actions=[
            "IMMEDIATE: Initiate emergency certificate renewal process. Coordinate with the certificate authority and "
            "schedule deployment during the next available maintenance window.",
            "Fast-track the certificate renewal through the CA. Prepare for off-hours deployment to minimize client "
            "impact.",
        ],
        remediation_steps=[
            [
                "Verify the exact expiration date and affected endpoints",
                "Initiate emergency certificate renewal with the certificate authority",
                "Complete domain validation if required by the CA",
                "Test the new certificate in staging before production deployment",
                "Schedule deployment during low-traffic window with rollback plan",
                "Deploy the renewed certificate to all affected endpoints",
                "Verify certificate chain and connectivity from multiple clients",
                "Update the certificate management system to prevent future lapses",
                "Review and fix the auto-renewal process that failed",
            ],
        ],
        tags=["ssl-certificate", "production", "api-gateway"],
    ),
    # ── 11. Penetration testing access request ────────────────────────────────
    Scenario(
        scenario_id="sec-pentest-access-request",
        category="Security & Compliance",
        priority="P3",
        assigned_team="Security Operations",
        needs_escalation=False,
        missing_information=[
            "environment_details",
            "network_location",
            "configuration_details",
        ],
        subjects=[
            "Penetration testing access request for Q4 assessment",
            "Need firewall exceptions for external pen test next week",
            "Request: pen test scope and access provisioning",
            "Third-party pen test — need environment access set up",
        ],
        descriptions=[
            "Our annual penetration test is scheduled for next Monday. The third-party firm (CrowdStrike Services) "
            "needs VPN access to our staging environment and firewall exceptions for their source IPs. Attached is the "
            "signed Statement of Work and Rules of Engagement. Can we get this set up by Friday?",
            "We're running a targeted pen test on the new client onboarding portal before go-live. The testing firm nee"
            "ds access to the UAT environment at uat.onboarding.contoso-fs.com. They'll be testing from three static IP"
            "s that need to be whitelisted. Test window is December 2-6.",
            "Requesting access provisioning for our quarterly penetration test. The security firm needs a test account "
            "with standard user privileges in the production-mirror environment, plus network access from their testing"
            " lab IP range. All approvals from the CISO are in place.",
        ],
        next_best_actions=[
            "Verify the signed Rules of Engagement and SOW. Coordinate with network ops to provision VPN access and "
            "firewall exceptions within the approved scope.",
            "Review the engagement documentation, confirm CISO approval, and coordinate access provisioning with a "
            "defined start/end window.",
        ],
        remediation_steps=[
            [
                "Verify signed Statement of Work and Rules of Engagement documents",
                "Confirm CISO and stakeholder approval for the test scope",
                "Provision test accounts with appropriate privilege levels",
                "Configure firewall exceptions for the testing firm's source IPs",
                "Set up VPN access with time-limited credentials",
                "Notify the SOC to whitelist expected testing activity and avoid false alerts",
                "Schedule access removal for the end of the engagement window",
            ],
        ],
        tags=["penetration-testing", "access-provisioning"],
    ),
    # ── 12. Security awareness training question ─────────────────────────────
    Scenario(
        scenario_id="sec-training-question",
        category="Security & Compliance",
        priority="P4",
        assigned_team="Security Operations",
        needs_escalation=False,
        missing_information=[],
        subjects=[
            "Question about security awareness training requirement",
            "When is the security training due?",
            "Can't find the link to complete my annual security training",
            "Security awareness training — need access to the portal",
        ],
        descriptions=[
            "I received a reminder that my annual security awareness training is due by end of month but I can't find "
            "the link to the training portal. Can someone point me in the right direction? I want to make sure I "
            "complete it before the deadline.",
            "My manager said I need to complete the security awareness training before my compliance certification is "
            "renewed. Where do I access this? Is it through the LMS or a separate platform?",
            "I'm a new hire and was told I need to complete security awareness training within my first 30 days. I "
            "don't see it in my onboarding checklist in Workday. Can you help me find it?",
        ],
        next_best_actions=[
            "Provide the user with the direct link to the security awareness training portal and verify their "
            "enrollment status.",
            "Direct the user to the training platform and confirm their enrollment. Check if there are access issues "
            "with the LMS.",
        ],
        remediation_steps=[
            [
                "Provide the user with the direct URL to the security awareness training portal",
                "Verify the user's enrollment status in the Learning Management System",
                "If not enrolled, add the user to the appropriate training program",
                "Confirm the completion deadline and any consequences of non-completion",
            ],
        ],
        tags=["training", "security-awareness"],
    ),
    # ── 13. Defender false positive on internal tool ─────────────────────────
    Scenario(
        scenario_id="sec-defender-false-positive",
        category="Security & Compliance",
        priority="P3",
        assigned_team="Endpoint Engineering",
        needs_escalation=False,
        missing_information=[
            "application_version",
            "device_info",
            "error_message",
        ],
        subjects=[
            "Defender blocking our internal tool — false positive",
            "Microsoft Defender quarantined our custom application",
            "False positive — Defender flagging legitimate internal script",
            "Antivirus blocking approved internal automation tool",
        ],
        descriptions=[
            "Microsoft Defender for Endpoint is quarantining our internally developed reconciliation tool (ReconEngine."
            "exe) every time it runs. This tool is used by the operations team daily to reconcile trade settlements. It"
            " was working fine until the latest Defender signature update. We need it whitelisted — it's a signed inter"
            "nal binary.",
            "Defender is blocking a Python script that our quant team uses for portfolio risk calculations. It's "
            "flagging it as HackTool:Python/Mimikatz which is clearly a false positive — it's a pandas-based analytics "
            "script. This is disrupting our daily risk reporting process.",
            "Our DevOps team's deployment automation tool is being flagged by Defender as Trojan:Win32/Generic. This is"
            " a custom-built tool that's been in use for two years and is digitally signed with our internal certificat"
            "e. The false positive started after yesterday's definition update.",
        ],
        next_best_actions=[
            "Verify the flagged binary is legitimate by checking its digital signature and hash against known-good "
            "versions. If confirmed as false positive, submit to Microsoft and create a targeted exclusion.",
            "Validate the binary's integrity, submit a false positive report to Microsoft, and create a scoped Defender"
            " exclusion for the application.",
        ],
        remediation_steps=[
            [
                "Verify the file hash and digital signature of the flagged binary",
                "Compare against the known-good version in the internal software repository",
                "If confirmed as false positive, submit the sample to Microsoft for reclassification",
                "Create a scoped Defender exclusion for the specific file path and hash",
                "Restore the quarantined file on affected endpoints",
                "Monitor for the updated Defender definitions that resolve the false positive",
                "Document the exclusion in the security exception register",
            ],
        ],
        tags=["defender", "false-positive", "endpoint"],
    ),
    # ── 14. Unauthorized software installed on workstation ────────────────────
    Scenario(
        scenario_id="sec-unauthorized-software",
        category="Security & Compliance",
        priority="P3",
        assigned_team="Endpoint Engineering",
        needs_escalation=False,
        missing_information=["device_info", "application_version", "affected_users"],
        subjects=[
            "Unauthorized software detected on my workstation",
            "Software compliance alert — unapproved app installed",
            "Need to install software not in the approved catalog",
            "App Control blocked a program I need for work",
        ],
        descriptions=[
            "I installed a free PDF editor from the internet because the one we have doesn't support batch processing. "
            "Now I'm getting alerts from the endpoint management system saying it's not approved software. I need this "
            "for my daily workflow — is there an approved alternative or can this one be added to the whitelist?",
            "Intune compliance check flagged my workstation for having unauthorized software: a personal cloud sync "
            "client (Dropbox) and a remote desktop tool (AnyDesk). I installed them for convenience but I understand "
            "they may violate our security policy. What should I do?",
            "I'm a developer and I need to install Wireshark for network troubleshooting on a client integration "
            "project. The software deployment portal says it's restricted. Can I get an exception for this? It's a "
            "legitimate business need and our team lead has approved it.",
        ],
        next_best_actions=[
            "Review the unauthorized software list, assess risk, and either provide approved alternatives or guide the "
            "user through the software exception request process.",
            "Verify the software detected, assess compliance and security risk, and advise on removal or exception "
            "procedures.",
        ],
        remediation_steps=[
            [
                "Identify the specific unauthorized software installed on the workstation",
                "Assess the security risk of the unauthorized software",
                "If high-risk (remote access tools, cloud sync), instruct immediate removal",
                "If low-risk with business justification, guide user through the software exception process",
                "Recommend approved alternatives from the software catalog",
                "Verify the workstation is compliant after remediation",
            ],
        ],
        tags=["unauthorized-software", "endpoint-compliance"],
    ),
    # ── 15. Privileged account compromise suspected ───────────────────────────
    Scenario(
        scenario_id="sec-privileged-account-compromise",
        category="Security & Compliance",
        priority="P1",
        assigned_team="Security Operations",
        needs_escalation=True,
        missing_information=[
            "affected_system",
            "timestamp",
            "authentication_method",
        ],
        subjects=[
            "CRITICAL — Suspected compromise of domain admin account",
            "Privileged account anomaly — potential admin credential theft",
            "URGENT: Service account showing unauthorized activity",
            "Possible compromise of DBA privileged account",
        ],
        descriptions=[
            "Our SIEM detected highly anomalous activity on a domain admin account (svc-admin-prod): Kerberoasting "
            "patterns followed by lateral movement to three domain controllers at 2 AM. No change requests were "
            "scheduled. The account has full administrative privileges across all production Active Directory forests "
            "including the ones hosting our core banking infrastructure.",
            "Azure AD Identity Protection flagged our global admin account with a high-risk score. We're seeing "
            "sign-ins from TOR exit nodes and the creation of new service principals with Graph API permissions. This "
            "account has access to the Azure AD tenant that manages all employee and contractor identities for the "
            "firm.",
            "The database team's privileged admin account for the production SQL cluster is showing login activity "
            "outside of normal maintenance windows. Someone used the account at 11 PM to export the entire client "
            "transactions table. No DBAs were working and no maintenance was scheduled. This database holds 5 years of "
            "regulated financial transaction data.",
        ],
        next_best_actions=[
            "IMMEDIATE: Disable the compromised privileged account and cut active sessions. Invoke the critical "
            "incident response playbook. Assess scope of access and potential data exposure.",
            "Trigger the privileged account compromise incident response procedure. Disable the account, preserve logs,"
            " and begin forensic investigation of all systems accessed.",
        ],
        remediation_steps=[
            [
                "Immediately disable the suspected compromised privileged account",
                "Terminate all active sessions and revoke tokens associated with the account",
                "Rotate all credentials, including Kerberos keys and service account passwords",
                "Conduct forensic analysis of all systems accessed by the account",
                "Review Active Directory/Azure AD audit logs for unauthorized changes",
                "Check for persistence mechanisms (scheduled tasks, service principals, golden tickets)",
                "Assess whether regulated data was accessed or exfiltrated",
                "If data exposure is confirmed, initiate regulatory breach notification procedures",
                "Implement Privileged Access Workstations (PAW) if not already in place",
                "Conduct a comprehensive review of all privileged accounts and access policies",
            ],
        ],
        tags=["privileged-account", "credential-theft", "incident-response", "critical"],
    ),
    # ── 16. Cloud security posture finding (Azure) ───────────────────────────
    Scenario(
        scenario_id="sec-cloud-posture-finding",
        category="Security & Compliance",
        priority="P2",
        assigned_team="Security Operations",
        needs_escalation=False,
        missing_information=[
            "affected_system",
            "environment_details",
            "configuration_details",
        ],
        subjects=[
            "Azure Security Center — high severity finding on storage account",
            "Cloud security posture issue — public blob storage detected",
            "Defender for Cloud flagged misconfigured Azure resources",
            "CSPM finding — Azure SQL database without encryption",
        ],
        descriptions=[
            "Microsoft Defender for Cloud flagged a high-severity finding: an Azure Storage Account in the production "
            "subscription has anonymous blob access enabled. The storage account name suggests it belongs to the data "
            "analytics team and may contain exported client reports. Secure Score dropped from 78% to 71%.",
            "Our weekly CSPM review identified three Azure SQL databases in the production environment that don't have "
            "Transparent Data Encryption (TDE) enabled. These databases are used by the loan origination platform and "
            "contain applicant financial data. This likely violates our encryption-at-rest policy and PCI-DSS "
            "requirements.",
            "Defender for Cloud is reporting that several Azure Virtual Machines in our production subscription have "
            "public IP addresses with unrestricted NSG rules (0.0.0.0/0 inbound on port 3389). These VMs are running "
            "our financial reporting middleware. This is a critical exposure that needs to be locked down.",
        ],
        next_best_actions=[
            "Assess the finding severity and determine if any data is currently exposed. Remediate the misconfiguration"
            " and audit other resources in the same subscription for similar issues.",
            "Investigate the misconfigured resources, determine data exposure risk, and apply the correct security "
            "configurations.",
        ],
        remediation_steps=[
            [
                "Review the Defender for Cloud finding details and severity",
                "Determine if any data was exposed or accessed due to the misconfiguration",
                "Apply the recommended security configuration to remediate the finding",
                "Verify the fix resolved the finding in Defender for Cloud",
                "Audit other resources in the subscription for similar misconfigurations",
                "Implement Azure Policy to prevent future misconfigurations",
                "Update cloud security baseline documentation",
            ],
        ],
        tags=["cloud-security", "azure", "cspm", "misconfiguration"],
    ),
    # ── 17. GDPR data subject deletion request ───────────────────────────────
    Scenario(
        scenario_id="sec-gdpr-data-deletion",
        category="Security & Compliance",
        priority="P2",
        assigned_team="Data Platform",
        needs_escalation=False,
        missing_information=[
            "affected_users",
            "affected_system",
            "contact_info",
        ],
        subjects=[
            "GDPR right to erasure request — client data deletion",
            "Data subject deletion request from EU client",
            "GDPR Article 17 request — need personal data removed",
            "Client requesting full data deletion under GDPR",
        ],
        descriptions=[
            "We received a formal GDPR Article 17 (right to erasure) request from a former client based in Germany. The"
            "y want all their personal data deleted from our systems within the 30-day regulatory window. Their data ex"
            "ists in our CRM (Salesforce), the client portal database, email archives, and potentially in analytics dat"
            "a lakes. We need to coordinate the deletion across all systems.",
            "A UK-based client has exercised their right to erasure under UK GDPR. They've sent a formal request "
            "through our Data Protection Officer. We need to locate and delete their personal data from all systems "
            "within the statutory timeframe. The client had an active advisory relationship from 2019-2023 so their "
            "data may be in multiple systems.",
            "The legal team forwarded a GDPR deletion request from a French client. We need to identify all personal "
            "data across our systems and execute deletion while preserving any data required for legal holds or "
            "regulatory retention requirements. This needs to be carefully handled to balance deletion with our SOX "
            "retention obligations.",
        ],
        next_best_actions=[
            "Initiate the GDPR data subject request workflow. Identify all systems containing the individual's data and"
            " coordinate deletion while respecting legal hold and retention requirements.",
            "Engage the data privacy team to map all systems containing the subject's data. Begin the deletion process "
            "within the regulatory timeframe.",
        ],
        remediation_steps=[
            [
                "Log the GDPR request in the data subject request tracker with the statutory deadline",
                "Conduct a data discovery across all systems to locate the individual's personal data",
                "Review legal hold and regulatory retention requirements (SOX, SEC) for any conflicts",
                "Coordinate deletion across all identified systems (CRM, databases, email, data lake)",
                "Verify deletion completeness and generate a compliance evidence report",
                "Notify the Data Protection Officer of completion",
                "Respond to the data subject confirming deletion within the statutory timeframe",
            ],
        ],
        tags=["gdpr", "data-deletion", "compliance", "privacy"],
    ),
    # ── 18. SOX compliance question / finding ────────────────────────────────
    Scenario(
        scenario_id="sec-sox-compliance-finding",
        category="Security & Compliance",
        priority="P1",
        assigned_team="Security Operations",
        needs_escalation=False,
        missing_information=[
            "affected_system",
            "configuration_details",
            "business_impact",
        ],
        subjects=[
            "SOX ITGC deficiency — access control gap in financial system",
            "SOX compliance finding — segregation of duties violation",
            "Urgent SOX question — change management evidence gap",
            "SOX audit prep — need IT controls evidence for financial reporting systems",
        ],
        descriptions=[
            "During our SOX 404 testing, we found that the access control matrix for the general ledger system (SAP FIC"
            "O) has not been updated after the last organizational restructuring. Several terminated employees still ha"
            "ve active accounts, and three users in the finance team have conflicting roles that violate segregation of"
            " duties. This needs immediate remediation before the external auditors begin fieldwork in two weeks.",
            "Our SOX compliance team identified a gap in the change management controls for the financial reporting pla"
            "tform: 15 production deployments in Q3 were missing documented approval from the change advisory board. We"
            " need IT to locate the approval records or document the finding and remediation plan for the external audi"
            "tors.",
            "Question from the CFO's office: we're being asked by our external auditors to provide evidence that all ac"
            "cess to the financial consolidation system is reviewed quarterly. Can IT provide the last four quarters of"
            " access review reports? If they haven't been done, we need to start immediately — this is a SOX material w"
            "eakness if unaddressed.",
        ],
        next_best_actions=[
            "Assess the SOX finding, identify the specific control deficiency, and create a remediation plan with "
            "deadlines aligned to the audit timeline.",
            "Engage the IT controls team and compliance to evaluate the finding severity and coordinate immediate "
            "remediation actions.",
        ],
        remediation_steps=[
            [
                "Review the specific SOX control deficiency with the compliance team",
                "Identify all affected systems and control processes",
                "Remediate the immediate finding (access review, SoD conflicts, change evidence)",
                "Generate or reconstruct evidence of compliance where possible",
                "Implement compensating controls if full remediation cannot be completed before audit",
                "Document the remediation plan and timeline for the external auditors",
                "Establish recurring controls testing to prevent future deficiencies",
                "Schedule quarterly reviews to maintain continuous compliance",
            ],
        ],
        tags=["sox", "compliance", "itgc", "audit", "financial-controls"],
    ),
    # ── 19. Vulnerability scan finding on production server ──────────────────
    Scenario(
        scenario_id="sec-vuln-scan-production",
        category="Security & Compliance",
        priority="P2",
        assigned_team="Security Operations",
        needs_escalation=False,
        missing_information=[
            "affected_system",
            "environment_details",
            "configuration_details",
        ],
        subjects=[
            "Critical vulnerability found on production server — needs patching",
            "Qualys scan results — CVE with CVSS 9.8 on production host",
            "Vulnerability scan flagged critical finding on trading platform server",
            "Production server missing critical security patches",
        ],
        descriptions=[
            "Our weekly Qualys vulnerability scan identified a critical vulnerability (CVE-2024-38077, CVSS 9.8) on a "
            "Windows Server hosting the trade matching engine. The vulnerability allows remote code execution without "
            "authentication. The server is internet-facing through the DMZ and processes real-time trade executions. "
            "Patch is available from Microsoft but requires a reboot.",
            "Vulnerability scan results show three production Linux servers running the client API layer have OpenSSL v"
            "ersions affected by CVE-2024-5535 (heap buffer overflow). These servers handle TLS termination for all cli"
            "ent-facing HTTPS traffic. The vulnerable OpenSSL version needs to be upgraded, which requires a service re"
            "start during a maintenance window.",
            "Tenable scan flagged a critical Apache Struts vulnerability on our financial reporting web application ser"
            "ver. This is the same class of vulnerability that caused the Equifax breach. The server hosts our quarterl"
            "y earnings data during filing periods. We need to patch this immediately but it's currently in the SOX cha"
            "nge freeze period.",
        ],
        next_best_actions=[
            "Assess the vulnerability's exploitability and potential impact. Schedule emergency patching within the SLA"
            " for critical vulnerabilities. Request change freeze exception if necessary.",
            "Evaluate the risk, check for active exploitation in the wild, and coordinate emergency patching with a "
            "defined rollback plan.",
        ],
        remediation_steps=[
            [
                "Review the vulnerability details, CVSS score, and affected systems",
                "Check threat intelligence for active exploitation in the wild",
                "Test the patch in a staging environment that mirrors production",
                "If in a change freeze, submit an emergency change request with risk justification",
                "Schedule the patching window during lowest-traffic period",
                "Apply the patch with a documented rollback plan",
                "Verify the vulnerability is resolved with a follow-up scan",
                "Update the vulnerability management tracker and report to compliance",
            ],
        ],
        tags=["vulnerability", "patching", "production", "cve"],
    ),
    # ── 20. Suspicious DLP alerts from departing employee ────────────────────
    Scenario(
        scenario_id="sec-dlp-departing-employee",
        category="Security & Compliance",
        priority="P1",
        assigned_team="Security Operations",
        needs_escalation=True,
        missing_information=["affected_system", "timestamp", "business_impact"],
        subjects=[
            "URGENT: DLP alerts from employee who just resigned",
            "Multiple DLP violations from departing team member",
            "Data exfiltration suspected — resigning employee triggering DLP",
            "Departing employee sending confidential files to personal email",
        ],
        descriptions=[
            "We have multiple DLP alerts firing for an employee in the Investment Advisory group who submitted their re"
            "signation yesterday. The alerts show the employee emailing large attachments containing client portfolio d"
            "ata and proprietary investment research to a personal email address. Over the past 24 hours, they've sent "
            "47 emails with attachments totaling 2.3 GB to three different external addresses.",
            "A departing Managing Director in the M&A division has triggered 12 DLP alerts in the past 6 hours. The "
            "alerts indicate they're uploading confidential deal documents, client financial statements, and revenue "
            "projections to a personal cloud storage service. This individual had access to material non-public "
            "information for three active acquisitions.",
            "HR escalated to us that an employee who was terminated this morning (effective immediately) was observed a"
            "t their desk before the termination meeting sending emails. Our DLP dashboard now shows 23 policy matches "
            "in the last 2 hours — all outbound emails with attachments containing client PII and financial data sent t"
            "o addresses outside our domain.",
        ],
        next_best_actions=[
            "IMMEDIATE: Block the employee's outbound email and external sharing capabilities. Preserve all DLP "
            "evidence and coordinate with HR and legal for the insider threat investigation.",
            "Restrict the employee's access to email and external sharing. Invoke the insider threat response procedure"
            " with HR and legal involvement.",
        ],
        remediation_steps=[
            [
                "Immediately block the employee's ability to send external email",
                "Disable the employee's access to SharePoint, OneDrive, and cloud storage",
                "Preserve all DLP alert data, email logs, and file access audit trails",
                "Quantify the data exposure: number of files, data types, external recipients",
                "Coordinate with HR and legal on the investigation and potential legal action",
                "Contact external recipients to request data deletion (via legal counsel)",
                "Assess regulatory notification requirements for exposed client data",
                "Conduct a full review of the employee's data access for the past 30 days",
                "Disable all remaining access and collect company devices",
            ],
        ],
        tags=["dlp", "insider-threat", "departing-employee", "data-exfiltration"],
    ),
    # ── 21. Phishing simulation — user reporting test email ──────────────────
    Scenario(
        scenario_id="sec-phishing-sim-report",
        category="Security & Compliance",
        priority="P4",
        assigned_team="Security Operations",
        needs_escalation=False,
        missing_information=[],
        subjects=[
            "Reporting a suspicious email — possible phishing",
            "I think I got a phishing email (it's the test one, right?)",
            "Flagging suspicious email — might be the phishing simulation",
            "Reporting potential phishing email to security team",
        ],
        descriptions=[
            "I received a suspicious email that claims to be from our benefits provider asking me to update my banking "
            "details. I'm pretty sure it's the monthly phishing simulation test but I wanted to report it anyway just "
            "in case it's real. I did NOT click any links.",
            "Got an email asking me to verify my identity for a bonus payout. Looks phishy (pun intended). I used the R"
            "eport Phishing button in Outlook. If it's a real phish, you're welcome. If it's the simulation test, do I "
            "get a gold star?",
            "Reporting a suspicious email I received about an urgent wire transfer approval. I think this might be the "
            "security team's phishing test. Either way, I'm flagging it as suspicious and not interacting with it.",
        ],
        next_best_actions=[
            "Acknowledge the report positively. If this was a phishing simulation, record the successful report. If "
            "not, escalate to the phishing analysis queue.",
            "Thank the user for their vigilance, verify if this was a simulation exercise, and record the interaction "
            "appropriately.",
        ],
        remediation_steps=[
            [
                "Check if the reported email matches a current phishing simulation campaign",
                "If simulation: record the successful report and send a congratulatory acknowledgment",
                "If real: escalate to the phishing analysis queue for investigation",
                "Thank the user for reporting regardless of whether it was a test",
            ],
        ],
        tags=["phishing-simulation", "security-awareness"],
    ),
    # ── 22. Cryptomining process detected on server ──────────────────────────
    Scenario(
        scenario_id="sec-cryptomining-detected",
        category="Security & Compliance",
        priority="P1",
        assigned_team="Security Operations",
        needs_escalation=True,
        missing_information=[
            "affected_system",
            "device_info",
            "network_location",
        ],
        subjects=[
            "CRITICAL — Cryptomining process detected on production server",
            "Unauthorized cryptocurrency miner running on server",
            "URGENT: Server compromised — cryptomining malware found",
            "Defender for Server flagged cryptomining activity",
        ],
        descriptions=[
            "Microsoft Defender for Servers flagged a cryptomining process (xmrig) running on one of our production "
            "application servers in the Azure East US region. The server's CPU has been pegged at 98% for the past 6 "
            "hours, which initially appeared as a performance issue. This server hosts a microservice in the payment "
            "processing pipeline and has network access to the cardholder data environment.",
            "Our infrastructure monitoring team noticed abnormal CPU usage on a Linux server in the data center. Invest"
            "igation revealed an unauthorized process making outbound connections to known cryptomining pools on port 3"
            "333. The server runs batch processing for overnight trade settlements. We suspect it was compromised throu"
            "gh an unpatched Apache vulnerability we identified in last week's scan.",
            "During a routine performance investigation, we discovered a hidden cryptomining binary running under a "
            "legitimate service account on a production Windows server. The process was disguised as a system service "
            "and has been running for approximately 2 weeks based on file timestamps. This server is part of our "
            "PCI-DSS scoped environment for card transaction processing.",
        ],
        next_best_actions=[
            "IMMEDIATE: Isolate the compromised server from the network. Determine the initial access vector and assess"
            " whether the attacker has moved laterally. This is a confirmed compromise of a production system.",
            "Invoke the server compromise incident response playbook. Isolate the host, preserve forensic evidence, and"
            " determine how the attacker gained access.",
        ],
        remediation_steps=[
            [
                "Immediately isolate the compromised server from the network",
                "Preserve forensic evidence (memory dump, disk snapshot, running processes)",
                "Identify and terminate the cryptomining process and any persistence mechanisms",
                "Determine the initial access vector (unpatched vulnerability, stolen credentials, etc.)",
                "Scan all servers in the same network segment for similar compromise indicators",
                "Check for lateral movement to other systems, especially PCI-scoped environments",
                "Rotate all credentials and service account passwords on the affected server",
                "Patch the vulnerability that enabled initial access",
                "Rebuild the server from a known-good image if integrity cannot be verified",
                "Assess PCI-DSS impact and determine if the QSA needs to be notified",
                "File incident report and conduct post-incident review",
            ],
        ],
        tags=["cryptomining", "server-compromise", "incident-response", "pci-dss"],
    ),
    Scenario(
        scenario_id="sec-spear-phishing-executive",
        category="Security & Compliance",
        priority="P1",
        assigned_team="Security Operations",
        needs_escalation=True,
        missing_information=["screenshot_or_attachment", "timestamp"],
        subjects=[
            "CFO received targeted phishing email impersonating the CEO",
            "Sophisticated spear-phishing targeting executive team",
            "CEO impersonation email sent to finance leadership",
        ],
        descriptions=[
            "Our CFO just forwarded me a suspicious email that appeared to come from our CEO asking for an urgent wire "
            "transfer of $2.3M to a new vendor. The email came from a lookalike domain (contoso-financial.com instead o"
            "f contoso.com). The CFO almost approved it before noticing the domain discrepancy. We need to investigate "
            "if anyone else received similar emails.",
            "A highly targeted phishing email was received by three members of the executive team today. The email "
            "perfectly mimics our CEO's writing style and references an actual board meeting from last week. It "
            "requests approval for a 'confidential acquisition payment.' The email headers show it originated from "
            "Eastern Europe.",
        ],
        next_best_actions=[
            "Immediately quarantine the phishing email across all mailboxes. Investigate the extent of the campaign and"
            " block the lookalike domain.",
        ],
        remediation_steps=[
            [
                "Quarantine the phishing email across all affected mailboxes using Exchange admin",
                "Block the sender domain and email addresses in Exchange transport rules",
                "Search all mailboxes for similar emails from the spoofed domain",
                "Verify no recipients clicked links or replied with sensitive information",
                "Report the lookalike domain for takedown to the registrar",
                "Send a company-wide alert about the targeted phishing campaign",
                "Review DMARC/DKIM enforcement to prevent future spoofing",
            ],
        ],
        tags=["phishing", "spear_phishing", "executive"],
        channel_weights={"email": 0.50, "chat": 0.10, "portal": 0.10, "phone": 0.30},
    ),
    Scenario(
        scenario_id="sec-dlp-bulk-download",
        category="Security & Compliance",
        priority="P1",
        assigned_team="Security Operations",
        needs_escalation=True,
        missing_information=["business_impact", "affected_users"],
        subjects=[
            "DLP alert — employee downloaded 10,000 client records",
            "Bulk data exfiltration alert from DLP system",
            "Large-scale download of sensitive client data detected",
        ],
        descriptions=[
            "Our DLP system flagged a user in the Client Services team who downloaded over 10,000 client records "
            "including names, SSNs, and account numbers to their local machine today. The user has a 2-week notice "
            "period and their last day is next Friday. This could be data exfiltration by a departing employee.",
            "Microsoft Purview DLP triggered a high-severity alert: a user exported the entire client contact database "
            "(12,500 records with PII) from Dynamics CRM to a CSV file. The user is in the Wealth Management division. "
            "The download happened at 11 PM last night, which is unusual for this user.",
        ],
        next_best_actions=[
            "Immediately disable the user's data export capabilities and investigate. Determine if this is authorized "
            "activity or potential data exfiltration. Preserve forensic evidence.",
        ],
        remediation_steps=[
            [
                "Restrict the user's data access and export capabilities immediately",
                "Preserve the downloaded files and audit logs for forensic investigation",
                "Interview the user's manager to determine if the download was authorized",
                "Check the user's recent activity for other suspicious data access patterns",
                "If departing employee, accelerate offboarding and device collection",
                "Assess potential regulatory reporting obligations (PII exposure)",
                "Document findings for compliance and legal review",
            ],
        ],
        tags=["dlp", "data_exfiltration", "insider_threat"],
    ),
    Scenario(
        scenario_id="sec-zero-day-vulnerability",
        category="Security & Compliance",
        priority="P1",
        assigned_team="Security Operations",
        needs_escalation=True,
        missing_information=["affected_system", "affected_users", "configuration_details"],
        subjects=[
            "Critical zero-day vulnerability in Exchange Server — CVE published today",
            "New CVE affecting our Exchange servers — active exploitation reported",
            "Emergency patch needed for Exchange zero-day vulnerability",
        ],
        descriptions=[
            "Microsoft just published CVE-2026-XXXXX, a critical remote code execution vulnerability in Exchange Server"
            " that's being actively exploited. Our Exchange hybrid deployment uses on-prem Exchange 2019 servers. The C"
            "ISA advisory says this is being used in targeted attacks against financial services. We need to patch imme"
            "diately.",
            "A critical zero-day was disclosed today affecting Exchange Server 2019 CU14. Active exploitation has been "
            "confirmed by multiple security vendors. Our on-prem Exchange servers are potentially vulnerable. The CVE "
            "has a CVSS score of 9.8 and doesn't require authentication to exploit.",
        ],
        next_best_actions=[
            "Immediately assess exposure to the CVE. Apply emergency mitigations while preparing to deploy the patch. "
            "Scan for indicators of compromise.",
        ],
        remediation_steps=[
            [
                "Identify all on-premises Exchange servers and their current patch level",
                "Apply recommended mitigations (URL rewrite rules, disable vulnerable feature)",
                "Scan Exchange servers for indicators of compromise (webshells, suspicious files)",
                "Download and test the emergency security update in a staging environment",
                "Deploy the security update to all Exchange servers in emergency change window",
                "Verify patch installation and run post-patch IOC scan",
                "Monitor for continued exploitation attempts in WAF/IDS logs",
            ],
        ],
        tags=["zero_day", "vulnerability", "exchange", "critical"],
        channel_weights={"email": 0.10, "chat": 0.20, "portal": 0.10, "phone": 0.60},
    ),
    Scenario(
        scenario_id="sec-usb-data-transfer-alert",
        category="Security & Compliance",
        priority="P3",
        assigned_team="Security Operations",
        needs_escalation=False,
        missing_information=["device_info", "business_impact", "timestamp"],
        subjects=[
            "USB device policy violation alert for my team member",
            "Employee plugged in personal USB drive — DLP triggered",
            "USB mass storage device detected on managed workstation",
        ],
        descriptions=[
            "I received an alert that one of my team members plugged a personal USB flash drive into their workstation "
            "and copied files to it. Our policy prohibits unauthorized USB storage devices. The employee says they were"
            " just transferring a presentation for an off-site meeting. I need guidance on how to handle this.",
            "Endpoint protection flagged a USB mass storage device connection on a workstation in the Trading "
            "department. The user attempted to copy 2.3 GB of data to the drive before the DLP policy blocked it. The "
            "user claims it was accidental.",
        ],
        next_best_actions=[
            "Review the DLP alert details and determine what data was accessed. Verify with the user's manager if the "
            "activity was authorized.",
        ],
        remediation_steps=[
            [
                "Review the DLP alert details including files accessed and transfer status",
                "Determine if any data was successfully copied before the block",
                "Verify with the user's manager if the data transfer was authorized",
                "If unauthorized, initiate security policy violation process",
                "Remind the user of the USB device usage policy",
                "Document the incident in the security incident tracker",
            ],
        ],
        tags=["usb", "dlp", "policy_violation"],
    ),
    Scenario(
        scenario_id="sec-mde-false-positive-trading",
        category="Security & Compliance",
        priority="P2",
        assigned_team="Security Operations",
        needs_escalation=False,
        missing_information=["affected_system", "steps_to_reproduce", "reproduction_frequency"],
        subjects=[
            "Defender blocking our trading application as malicious",
            "Microsoft Defender quarantining legitimate trading software",
            "MDE false positive on critical trading desk application",
        ],
        descriptions=[
            "Microsoft Defender for Endpoint is flagging and quarantining our proprietary trading application "
            "(ContosoTrader.exe) as potentially unwanted software. This started after today's signature update. The "
            "trading floor is losing the ability to execute trades every time Defender runs a scan. We need an "
            "immediate exclusion.",
            "Defender is blocking our custom-built risk analytics tool as 'Trojan:Win32/Generic'. This is our own "
            "internally developed software, not malware. The latest Defender definitions update caused this false "
            "positive. 40 traders can't do their jobs.",
        ],
        next_best_actions=[
            "Create an immediate Defender exclusion for the legitimate application while submitting a false positive "
            "report to Microsoft.",
        ],
        remediation_steps=[
            [
                "Create a Defender for Endpoint indicator exclusion for the application hash",
                "Add path exclusion in Intune Defender policy for the application directory",
                "Restore quarantined files on affected endpoints",
                "Submit the false positive to Microsoft Security Intelligence portal",
                "Verify the application runs without being blocked after exclusion",
                "Monitor for the next Defender signature update to confirm the fix",
            ],
        ],
        tags=["defender", "false_positive", "trading"],
    ),
]
