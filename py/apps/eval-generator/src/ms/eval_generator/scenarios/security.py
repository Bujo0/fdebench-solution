# Copyright (c) Microsoft. All rights reserved.
"""Security & Compliance category scenarios for eval dataset."""

from ms.eval_generator.scenarios._base import ScenarioDefinition
from ms.eval_generator.scenarios._base import ScenarioGold

SECURITY_SCENARIOS: list[ScenarioDefinition] = [
    # ──────────────────────────────────────────────────────────────────
    # 1. Phishing email received with suspicious link
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="security-001",
        subjects=(
            "Suspicious email with link — possible phishing",
            "Got a phishing email pretending to be IT",
        ),
        descriptions=(
            "I received an email that looks like it's from our IT department asking me to 'verify my "
            "credentials' by clicking a link. The sender is support@contoso-it-help.com (not our real "
            "domain). I haven't clicked anything. What should I do?",
            "Forwarding a suspicious email I received. Subject was 'Urgent: Password Expiry Notice.' The "
            "link goes to a sketchy URL that's not contoso.com. Looks like a phishing attempt targeting our "
            "finance team — 3 others in my group got the same email.",
        ),
        gold=ScenarioGold(
            category="Security & Compliance",
            priority="P2",
            assigned_team="Security Operations",
            needs_escalation=False,
            missing_information=(),
            next_best_action="Analyze the phishing email and block the sender domain across the organization",
            remediation_steps=(
                "Forward the original phishing email as an attachment to phishing@contoso.com",
                "Block the sender domain contoso-it-help.com in the email security gateway",
                "Scan all mailboxes for instances of this phishing email and purge",
                "Notify affected users not to click the link",
                "If anyone clicked the link, initiate credential reset and endpoint scan",
            ),
        ),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 2. Malware detected by Windows Defender
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="security-002",
        subjects=(
            "Windows Defender found malware on my laptop",
            "Malware alert — Trojan detected",
        ),
        descriptions=(
            "Windows Defender just popped up a 'Threat found' alert on my laptop. It says it detected "
            "'Trojan:Win32/Emotet' and quarantined a file. I don't know how it got there. Should I be "
            "worried? I was browsing a client's website when it happened.",
            "My laptop flagged a malware detection — Defender says it found a suspicious file in my "
            "Downloads folder. I think it came from an email attachment I opened yesterday from what I "
            "thought was a vendor invoice. The file was invoice_march2026.exe.",
        ),
        gold=ScenarioGold(
            category="Security & Compliance",
            priority="P2",
            assigned_team="Security Operations",
            needs_escalation=False,
            missing_information=(
                "device_info",
            ),
            next_best_action="Isolate the device from the network and run a full malware scan",
            remediation_steps=(
                "Disconnect the device from the network (WiFi and Ethernet)",
                "Run a full Windows Defender offline scan",
                "Check if the malware was successfully quarantined or if it executed",
                "If Emotet, check for lateral movement indicators on the network",
                "After clean scan, reconnect and monitor for 24 hours",
            ),
        ),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 3. Unauthorized access to client financial data
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="security-003",
        subjects=(
            "ALERT: Unauthorized access to client data detected",
            "Suspicious data access — client records",
        ),
        descriptions=(
            "Our DLP system flagged that someone accessed 5,000+ client financial records from the "
            "ClientData database at 2 AM last night. The access came from a service account that shouldn't "
            "have that level of access. This is a potential data breach and needs immediate investigation.",
            "We've detected unauthorized bulk export of client portfolio data. The audit log shows 12,000 "
            "records were queried and exported to a CSV file from an IP address we don't recognize. This "
            "may be a data breach — regulators require notification within 72 hours.",
        ),
        gold=ScenarioGold(
            category="Security & Compliance",
            priority="P1",
            assigned_team="Security Operations",
            needs_escalation=True,
            missing_information=(),
            next_best_action="Initiate data breach incident response — preserve evidence and notify CISO immediately",
            remediation_steps=(
                "Lock the service account used for unauthorized access immediately",
                "Preserve all audit logs and evidence for forensic investigation",
                "Notify the CISO and legal team about potential data breach",
                "Begin incident response per the data breach playbook",
                "Assess regulatory notification requirements (72-hour window)",
            ),
        ),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 4. Suspicious login from foreign country
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="security-004",
        subjects=(
            "Suspicious login from Russia at 3 AM",
            "ALERT: Foreign login attempt on executive account",
        ),
        descriptions=(
            "Entra ID flagged a successful login to my account from an IP address in Moscow at 3:14 AM. I "
            "was asleep in NYC. Someone has my credentials. I've already changed my password but I'm "
            "worried about what they accessed.",
            "Security alert — our CFO's account shows a successful authentication from an IP in China at 2 "
            "AM EST. The CFO is in the NYC office. This is a confirmed account compromise on a C-suite "
            "account with access to sensitive financial data.",
        ),
        gold=ScenarioGold(
            category="Security & Compliance",
            priority="P1",
            assigned_team="Security Operations",
            needs_escalation=True,
            missing_information=(),
            next_best_action="Initiate immediate incident response for confirmed account compromise",
            remediation_steps=(
                "Revoke all active sessions and refresh tokens for the account",
                "Force immediate password reset",
                "Review sign-in and audit logs for all activity from the suspicious IP",
                "Check for persistence mechanisms (inbox rules, app consents, MFA changes)",
                "Assess what data the compromised account could have accessed",
            ),
        ),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 5. DLP alert — sensitive data sent to personal email
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="security-005",
        subjects=(
            "DLP alert: employee sent client data to Gmail",
            "Data loss prevention triggered on outbound email",
        ),
        descriptions=(
            "Our DLP system caught an employee sending a spreadsheet with client SSNs and account numbers "
            "to their personal Gmail address. The email was blocked but the intent is concerning. Employee: "
            "James Morton, Finance department.",
            "DLP policy triggered on an outbound email containing credit card numbers and personal "
            "identification data. The recipient was a personal Outlook.com address. The email was "
            "quarantined. Need investigation into whether this was intentional exfiltration.",
        ),
        gold=ScenarioGold(
            category="Security & Compliance",
            priority="P2",
            assigned_team="Security Operations",
            needs_escalation=True,
            missing_information=(),
            next_best_action="Investigate the DLP violation for potential intentional data exfiltration",
            remediation_steps=(
                "Review the quarantined email content and DLP match details",
                "Check the employee's recent email activity for patterns of data exfiltration",
                "Interview the employee's manager about business justification",
                "If no justification, escalate to HR and Legal for further action",
                "Tighten DLP policies to prevent similar attempts",
            ),
        ),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 6. Compliance audit request from regulators
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="security-006",
        subjects=(
            "SEC audit — need security controls documentation",
            "Regulatory compliance audit — urgent request",
        ),
        descriptions=(
            "The SEC has requested documentation of our IT security controls and access management "
            "procedures for the annual audit. They need: access control policies, privileged access logs "
            "for the past 6 months, and evidence of security awareness training. Deadline: 2 weeks.",
            "FINRA compliance examination notice received. We need to provide evidence of our cybersecurity "
            "program including: incident response plans, data protection controls, access reviews, and "
            "vulnerability management reports. This is a mandatory regulatory requirement.",
        ),
        gold=ScenarioGold(
            category="Security & Compliance",
            priority="P1",
            assigned_team="Security Operations",
            needs_escalation=True,
            missing_information=(),
            next_best_action=(
                "Coordinate with compliance team to gather all required security documentation for the "
                "regulatory audit"
            ),
            remediation_steps=(
                "Compile the list of specific documents requested by the regulator",
                "Gather access control policies and privileged access management logs",
                "Export security awareness training completion records",
                "Prepare incident response plan documentation and test results",
                "Schedule a review meeting with Legal and Compliance before submission",
            ),
        ),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 7. Ransomware warning popup on screen
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="security-007",
        subjects=(
            "RANSOMWARE ALERT — screen locked with ransom message",
            "Laptop showing ransom demand — encrypted files",
        ),
        descriptions=(
            "MY LAPTOP SCREEN IS SHOWING A RANSOMWARE MESSAGE. It says all my files are encrypted and I "
            "need to pay Bitcoin to get them back. I can't access anything. The message says 'Your files "
            "have been encrypted by CryptoLocker. Pay 2 BTC within 48 hours.' HELP!",
            "I think my computer has been hit by ransomware. All my files have been renamed with a .locked "
            "extension and there's a text file on my desktop demanding payment. I was opening an email "
            "attachment when this happened. The whole C: drive seems encrypted.",
        ),
        gold=ScenarioGold(
            category="Security & Compliance",
            priority="P1",
            assigned_team="Security Operations",
            needs_escalation=True,
            missing_information=(),
            next_best_action="IMMEDIATELY disconnect the device from the network and initiate ransomware incident "
                "response",
            remediation_steps=(
                "Physically disconnect the device from all networks immediately",
                "Do NOT restart the device — preserve evidence in memory",
                "Notify the incident response team and CISO",
                "Check if the ransomware has spread to any network shares or other devices",
                "Initiate forensic imaging of the affected device",
            ),
        ),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 8. Employee clicked on phishing link
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="security-008",
        subjects=(
            "I accidentally clicked a phishing link",
            "Clicked suspicious link — what should I do?",
        ),
        descriptions=(
            "I'm embarrassed but I need to report that I clicked on a link in a phishing email about 30 "
            "minutes ago. It took me to a page that looked like our Microsoft login and I entered my "
            "credentials before realizing it was fake. I've already changed my password. What else should I "
            "do?",
            "I think I fell for a phishing scam. I clicked a link in an email that looked like it was from "
            "SharePoint and entered my username and password. The page looked weird after I submitted so I "
            "realized it was fake. This happened about an hour ago.",
        ),
        gold=ScenarioGold(
            category="Security & Compliance",
            priority="P2",
            assigned_team="Security Operations",
            needs_escalation=False,
            missing_information=(),
            next_best_action="Force credential reset and review account activity since the phishing event",
            remediation_steps=(
                "Force password reset if not already done",
                "Revoke all active sessions and MFA tokens",
                "Review sign-in logs for any unauthorized access since the phishing event",
                "Check for suspicious inbox rules or app consents added to the account",
                "Run an endpoint scan on the user's device for malware",
                "Commend the user for reporting promptly",
            ),
        ),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 9. Suspicious USB device found on workstation
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="security-009",
        subjects=(
            "Found unknown USB device plugged into my workstation",
            "Suspicious USB stick found in office",
        ),
        descriptions=(
            "I came in this morning and found a USB flash drive plugged into the back of my workstation "
            "that I didn't put there. Nobody in my team claims it. I haven't touched it. It's labeled "
            "'Salary_Review_2026.' This feels like a social engineering attack.",
            "A cleaning crew member found a USB device on the floor near the trading desk area. Before I "
            "could stop him, he plugged it into a computer to see whose it was. The computer immediately "
            "started downloading something. I pulled the USB out and disconnected the network cable.",
        ),
        gold=ScenarioGold(
            category="Security & Compliance",
            priority="P1",
            assigned_team="Security Operations",
            needs_escalation=True,
            missing_information=(
                "device_info",
            ),
            next_best_action=(
                "Treat as a potential USB-based attack — isolate the affected device and investigate the USB "
                "contents safely"
            ),
            remediation_steps=(
                "Do not plug the USB into any other device",
                "If already plugged in, disconnect the computer from the network immediately",
                "Preserve the USB device as evidence in an anti-static bag",
                "Run a full malware scan on any computer the USB was connected to",
                "Report to Security Operations for forensic analysis of the USB contents",
            ),
        ),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 10. Security certificate expiring on customer portal
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="security-010",
        subjects=(
            "SSL cert expiring on customer-facing portal in 5 days",
            "Security certificate renewal needed",
        ),
        descriptions=(
            "The SSL/TLS certificate on our customer-facing wealth management portal (portal.contoso.com) "
            "expires in 5 days. If it expires, customers will see security warnings and may not be able to "
            "access their accounts. We need to renew and install the new cert before then.",
            "Heads up — the wildcard certificate for *.contoso.com is expiring next Monday. This affects "
            "all our customer-facing HTTPS services. We need to renew with our CA and deploy to about 15 "
            "web servers.",
        ),
        gold=ScenarioGold(
            category="Security & Compliance",
            priority="P2",
            assigned_team="Security Operations",
            needs_escalation=False,
            missing_information=(),
            next_best_action="Expedite certificate renewal and schedule deployment before expiration",
            remediation_steps=(
                "Submit certificate renewal request to the CA (DigiCert/Let's Encrypt)",
                "Generate a new CSR if the renewal requires one",
                "Install the renewed certificate on all affected web servers",
                "Verify the certificate chain is valid and complete",
                "Set up automated certificate expiry monitoring to prevent future near-misses",
            ),
        ),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 11. Insider threat — employee accessing unusual files
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="security-011",
        subjects=(
            "ALERT: Employee accessing files outside their role",
            "Unusual data access pattern detected",
        ),
        descriptions=(
            "Our SIEM flagged unusual file access by an employee in Client Services. Over the past week, "
            "they've accessed 3,000+ files in the M&A deal room SharePoint site that they have no business "
            "reason to view. Their role doesn't involve M&A work. The employee recently gave their two-week "
            "notice.",
            "We've detected an anomalous data access pattern. An employee in IT operations has been "
            "downloading large volumes of source code from our internal GitLab server — repositories they "
            "don't normally access. Total download: 15 GB in the past 3 days. HR confirmed this person was "
            "denied a promotion last month.",
        ),
        gold=ScenarioGold(
            category="Security & Compliance",
            priority="P1",
            assigned_team="Security Operations",
            needs_escalation=True,
            missing_information=(),
            next_best_action="Initiate insider threat investigation — preserve evidence and restrict the employee's "
                "access",
            remediation_steps=(
                "Preserve all access logs and audit trails as evidence",
                "Restrict the employee's access to sensitive repositories and file shares",
                "Coordinate with HR and Legal before any direct confrontation",
                "Review all data accessed and downloaded by the employee",
                "Implement additional monitoring on the employee's account",
            ),
        ),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 12. Critical CVE found on production server
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="security-012",
        subjects=(
            "Critical vulnerability CVE-2026-XXXX on prod servers",
            "Vulnerability scan found critical RCE on production",
        ),
        descriptions=(
            "Our Qualys vulnerability scan found CVE-2026-1234 (CVSS 9.8) on 3 production web servers. It's "
            "a remote code execution vulnerability in Apache. These servers are internet-facing and host "
            "our customer portal. The patch was released yesterday.",
            "Nessus scan results show a critical vulnerability on our production SQL server — remote code "
            "execution with no authentication required. CVSS score 10.0. This server holds client financial "
            "data. We need to patch immediately but it requires downtime.",
        ),
        gold=ScenarioGold(
            category="Security & Compliance",
            priority="P1",
            assigned_team="Security Operations",
            needs_escalation=True,
            missing_information=(),
            next_best_action="Apply emergency patch for the critical RCE vulnerability on production servers",
            remediation_steps=(
                "Assess the exploitability and confirm exposure of the vulnerable servers",
                "Apply WAF rules to mitigate the vulnerability as an interim measure",
                "Schedule emergency patching with the application team",
                "Apply the vendor patch and verify the vulnerability is remediated",
                "Rescan to confirm the vulnerability is resolved",
            ),
        ),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 13. PCI compliance deadline approaching
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="security-013",
        subjects=(
            "PCI DSS compliance assessment due next month",
            "Need help preparing for PCI audit",
        ),
        descriptions=(
            "Our annual PCI DSS compliance assessment is due in 4 weeks. We need to review our cardholder "
            "data environment controls, run internal and external vulnerability scans, and prepare the "
            "Self-Assessment Questionnaire. Can SecOps help coordinate?",
            "PCI compliance renewal — we need to complete the required penetration test, vulnerability "
            "scans, and controls review before the March 31st deadline. Our QSA (Qualified Security "
            "Assessor) starts on-site in 3 weeks.",
        ),
        gold=ScenarioGold(
            category="Security & Compliance",
            priority="P2",
            assigned_team="Security Operations",
            needs_escalation=False,
            missing_information=(),
            next_best_action="Coordinate PCI DSS compliance preparation activities and schedule required assessments",
            remediation_steps=(
                "Review the PCI DSS requirements checklist and identify any gaps",
                "Schedule internal and external vulnerability scans with an ASV",
                "Prepare documentation for the cardholder data environment scope",
                "Coordinate the penetration test with an approved testing firm",
                "Compile evidence packages for each PCI DSS requirement",
            ),
        ),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 14. Lost corporate phone with sensitive data
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="security-014",
        subjects=(
            "Lost my company phone — has sensitive data",
            "Corporate iPhone lost — need remote wipe",
        ),
        descriptions=(
            "I lost my company iPhone at the airport yesterday. It has my work email, Teams, and Salesforce "
            "app with client data. The phone has a passcode and Face ID but I want it wiped remotely just "
            "in case. I've already tried Find My iPhone but it shows offline.",
            "My company mobile device was stolen from my hotel room during a business trip. It has access "
            "to company email, SharePoint, and the Bloomberg mobile app. I need an immediate remote wipe "
            "and a replacement device when I return.",
        ),
        gold=ScenarioGold(
            category="Security & Compliance",
            priority="P2",
            assigned_team="Security Operations",
            needs_escalation=True,
            missing_information=(),
            next_best_action="Initiate remote wipe on the lost device and revoke all mobile access tokens",
            remediation_steps=(
                "Initiate remote wipe via Intune MDM immediately",
                "Revoke all active sessions for the user on mobile platforms",
                "Mark the device as lost/stolen in the asset management system",
                "If corporate data may have been accessed, notify the data protection team",
                "Provision a replacement device when the user returns",
            ),
        ),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 15. Suspicious email forwarding rule on exec mailbox
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="security-015",
        subjects=(
            "ALERT: Unauthorized forwarding rule on CFO's mailbox",
            "Suspicious inbox rule detected on executive account",
        ),
        descriptions=(
            "During a routine audit, we discovered an inbox forwarding rule on the CFO's mailbox that "
            "forwards all emails containing 'merger,' 'acquisition,' or 'earnings' to an external Gmail "
            "address. The CFO did not create this rule. This is a serious breach — possible corporate "
            "espionage.",
            "Found a suspicious inbox rule on the CEO's Exchange mailbox. It silently BCCs all sent emails "
            "to an unknown external address. The CEO confirms they didn't set this up. The rule was created "
            "3 weeks ago — we need to investigate what was leaked.",
        ),
        gold=ScenarioGold(
            category="Security & Compliance",
            priority="P1",
            assigned_team="Security Operations",
            needs_escalation=True,
            missing_information=(),
            next_best_action="Remove the malicious forwarding rule immediately and initiate a full compromise "
                "investigation",
            remediation_steps=(
                "Remove the unauthorized forwarding rule immediately",
                "Disable the forwarding destination at the mail transport level",
                "Analyze when the rule was created and from what IP/device",
                "Review all emails forwarded to the external address",
                "Force credential reset and full security review of the executive account",
            ),
        ),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 16. Third-party vendor requesting VPN access
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="security-016",
        subjects=(
            "Vendor security review for VPN access",
            "New vendor needs remote access — security assessment needed",
        ),
        descriptions=(
            "Acme Consulting needs VPN access to our network for the SAP implementation project. They'll "
            "have 5 consultants working remotely for 6 months. Before we grant access, we need a security "
            "assessment of their practices. Can SecOps conduct the vendor review?",
            "Our new payroll processing vendor needs direct VPN connectivity to our HR systems. They've "
            "asked for site-to-site VPN access. We need a security risk assessment and vendor due diligence "
            "review before proceeding.",
        ),
        gold=ScenarioGold(
            category="Security & Compliance",
            priority="P3",
            assigned_team="Security Operations",
            needs_escalation=False,
            missing_information=(
                "configuration_details",
            ),
            next_best_action="Conduct a third-party vendor security assessment before granting network access",
            remediation_steps=(
                "Send the vendor security questionnaire to the consulting firm",
                "Review the vendor's SOC 2 report and security certifications",
                "Define the minimum network access scope required for the project",
                "If approved, configure isolated vendor VPN access with MFA required",
                "Set an access expiration date aligned with the project timeline",
            ),
        ),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 17. BitLocker recovery key needed
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="security-017",
        subjects=(
            "BitLocker recovery key required — can't boot",
            "Laptop asking for BitLocker recovery key",
        ),
        descriptions=(
            "My laptop is asking for a BitLocker recovery key after a BIOS update. I don't have the key and "
            "can't boot into Windows at all. The screen shows a 48-digit recovery key prompt. I need to get "
            "into my laptop for work today.",
            "BitLocker recovery screen appeared after I changed a hardware setting in BIOS. Now my laptop "
            "won't boot without the 48-digit recovery key. I never saved this key anywhere. Can IT look it "
            "up?",
        ),
        gold=ScenarioGold(
            category="Security & Compliance",
            priority="P3",
            assigned_team="Security Operations",
            needs_escalation=False,
            missing_information=(
                "device_info",
            ),
            next_best_action="Retrieve the BitLocker recovery key from Entra ID or MBAM and provide to the user",
            remediation_steps=(
                "Look up the device in Entra ID to find the stored BitLocker recovery key",
                "Verify the user's identity before providing the recovery key",
                "Provide the 48-digit recovery key via a secure channel",
                "Once booted, verify TPM and BitLocker status are healthy",
                "If the BIOS change is permanent, suspend and resume BitLocker to re-seal the TPM",
            ),
        ),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 18. Data classification policy question
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="security-018",
        subjects=(
            "Question about data classification labels",
            "How to classify sensitive documents?",
        ),
        descriptions=(
            "I'm working on a client proposal that contains financial projections and pricing information. "
            "What data classification label should I apply? I see options for Public, Internal, "
            "Confidential, and Highly Confidential. The document will be shared with the client.",
            "Our team is unsure about the proper data classification for our research reports. Some contain "
            "material non-public information (MNPI) that could be insider trading risk. Should these be "
            "Highly Confidential or just Confidential?",
        ),
        gold=ScenarioGold(
            category="Security & Compliance",
            priority="P4",
            assigned_team="Security Operations",
            needs_escalation=False,
            missing_information=(),
            next_best_action="Provide data classification guidance and direct user to the classification policy "
                "documentation",
            remediation_steps=(
                "Share the data classification policy and decision matrix",
                "For documents with MNPI, classify as Highly Confidential",
                "For client-shared proposals, classify as Confidential at minimum",
                "Guide the user on applying sensitivity labels in Office apps",
                "Recommend completing the data classification training module",
            ),
        ),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 19. Penetration test request for new web app
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="security-019",
        subjects=(
            "Pen test request for new customer portal",
            "Security assessment needed before go-live",
        ),
        descriptions=(
            "We're launching a new customer-facing web application next month and need a penetration test "
            "before go-live. It's a React/Node.js app hosted on Azure App Service with an API backend. Can "
            "SecOps schedule this or recommend an approved testing firm?",
            "Requesting a security assessment for our new internal HR portal before deployment. It handles "
            "employee PII and integrates with our payroll system. We need both a vulnerability assessment "
            "and a penetration test per our SDL requirements.",
        ),
        gold=ScenarioGold(
            category="Security & Compliance",
            priority="P3",
            assigned_team="Security Operations",
            needs_escalation=False,
            missing_information=(
                "affected_system",
                "environment_details",
            ),
            next_best_action="Schedule a penetration test with an approved firm and scope the assessment",
            remediation_steps=(
                "Define the scope of the penetration test (URLs, APIs, authentication flows)",
                "Engage an approved penetration testing firm or internal red team",
                "Provide the testers with application documentation and test accounts",
                "Review the findings and create a remediation plan for identified vulnerabilities",
                "Verify critical findings are remediated before go-live",
            ),
        ),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 20. GDPR data subject access request
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="security-020",
        subjects=(
            "GDPR data subject access request from EU client",
            "DSAR received — need to locate personal data",
        ),
        descriptions=(
            "We received a GDPR Data Subject Access Request from a client in Germany. They want a copy of "
            "all personal data we hold about them. We have 30 days to respond. I need help from SecOps to "
            "identify all systems where this person's data might be stored.",
            "A former employee who relocated to the EU has submitted a GDPR right to erasure request. They "
            "want all their personal data deleted from our systems. We need to map all data locations and "
            "determine what can be deleted vs. what has legal retention requirements.",
        ),
        gold=ScenarioGold(
            category="Security & Compliance",
            priority="P2",
            assigned_team="Security Operations",
            needs_escalation=False,
            missing_information=(),
            next_best_action="Initiate DSAR response process — identify all systems containing the data subject's "
                "personal data",
            remediation_steps=(
                "Log the DSAR in the privacy request tracker",
                "Search all identified data repositories for the subject's personal data",
                "Compile the data inventory and classify by retention requirements",
                "Coordinate with Legal on what can be deleted vs. retained",
                "Provide the response to the data subject within the 30-day deadline",
            ),
        ),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 21. Suspicious process running on multiple machines
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="security-021",
        subjects=(
            "Unknown process running across workstations",
            "Suspicious svchost-like process on multiple PCs",
        ),
        descriptions=(
            "Our EDR tool flagged a suspicious process 'svch0st.exe' (note the zero) running on 8 "
            "workstations in the Finance department. It's making outbound connections to IPs we don't "
            "recognize. This looks like it could be a botnet or C2 communication.",
            "Detected an unauthorized PowerShell script running as a scheduled task on 12 machines in the "
            "Trading department. The script appears to be collecting browser credentials and sending them "
            "to an external server. This was not deployed by IT.",
        ),
        gold=ScenarioGold(
            category="Security & Compliance",
            priority="P1",
            assigned_team="Security Operations",
            needs_escalation=True,
            missing_information=(),
            next_best_action="Isolate affected machines from the network and initiate malware incident response",
            remediation_steps=(
                "Isolate all affected machines from the network using EDR containment",
                "Collect forensic artifacts (process memory, network connections, scheduled tasks)",
                "Block the identified C2 IP addresses at the firewall",
                "Identify the initial infection vector and timeline",
                "Clean the affected machines and monitor for reinfection",
            ),
        ),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 22. Unauthorized crypto mining software
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="security-022",
        subjects=(
            "Employee installing crypto mining software",
            "Crypto miner detected on company workstation",
        ),
        descriptions=(
            "We detected crypto mining software (XMRig) on a developer's workstation. CPU usage was at 100% "
            "during non-business hours. The developer claims they didn't install it, but our logs show it "
            "was downloaded from their user account. Company policy prohibits this.",
            "Our monitoring detected unusual GPU utilization on 3 workstations in the Engineering "
            "department after hours. Investigation reveals a cryptocurrency mining application running as a "
            "service. This is consuming significant power and compute resources.",
        ),
        gold=ScenarioGold(
            category="Security & Compliance",
            priority="P2",
            assigned_team="Security Operations",
            needs_escalation=True,
            missing_information=(
                "device_info",
            ),
            next_best_action=(
                "Remove the mining software and investigate whether it was intentionally installed or delivered "
                "via malware"
            ),
            remediation_steps=(
                "Remove the crypto mining software from all affected devices",
                "Determine if the software was manually installed or delivered via malware",
                "If manually installed, escalate to HR for acceptable use policy violation",
                "If malware, investigate the infection vector and scan for additional compromise",
                "Block known crypto mining applications via application control policy",
            ),
        ),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 23. SOC alert — brute force attack on admin accounts
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="security-023",
        subjects=(
            "ALERT: Brute force attack on admin accounts detected",
            "Mass failed login attempts on administrator accounts",
        ),
        descriptions=(
            "Our SOC detected a brute force attack against multiple admin accounts. Over 50,000 failed "
            "login attempts in the past hour from a botnet of 200+ IP addresses. The attack is targeting "
            "our Global Admin and Exchange Admin accounts. No successful logins detected yet.",
            "SIEM alert: coordinated password spraying attack against our Azure AD admin accounts. Attacker "
            "is rotating through common passwords across all accounts with 'admin' in the name. Attack "
            "started 45 minutes ago and is ongoing.",
        ),
        gold=ScenarioGold(
            category="Security & Compliance",
            priority="P1",
            assigned_team="Security Operations",
            needs_escalation=True,
            missing_information=(),
            next_best_action="Block attacking IPs and enforce account lockout protection "
            "for admin accounts immediately",
            remediation_steps=(
                "Block the attacking IP ranges at the firewall and in conditional access",
                "Enable smart lockout in Entra ID if not already active",
                "Verify all admin accounts have strong MFA enabled",
                "Review sign-in logs to confirm no successful unauthorized authentications",
                "Implement named location-based conditional access for admin accounts",
            ),
        ),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 24. Expired SSL certificate on internal API
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="security-024",
        subjects=(
            "Internal API gateway SSL cert expired",
            "Certificate expired on api.internal.contoso.com",
        ),
        descriptions=(
            "The SSL certificate on our internal API gateway (api.internal.contoso.com) expired yesterday. "
            "All internal services that communicate through the gateway are now getting TLS errors. "
            "Microservices are failing their health checks because of certificate validation failures.",
            "Internal certificate for the service mesh has expired, causing cascading failures across our "
            "microservice architecture. Services can't communicate securely. This is affecting multiple "
            "internal applications.",
        ),
        gold=ScenarioGold(
            category="Security & Compliance",
            priority="P2",
            assigned_team="Security Operations",
            needs_escalation=False,
            missing_information=(),
            next_best_action="Issue and install a new internal certificate immediately to restore "
            "service communication",
            remediation_steps=(
                "Generate a new certificate from the internal CA",
                "Install the certificate on the API gateway",
                "Restart affected services that cached the old certificate",
                "Verify service-to-service communication is restored",
                "Add the internal certificate to automated renewal monitoring",
            ),
        ),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 25. Security awareness training tracking
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="security-025",
        subjects=(
            "Need security training completion report",
            "Which employees haven't completed security training?",
        ),
        descriptions=(
            "HR is asking for a report on security awareness training completion. The annual mandatory "
            "training deadline was last Friday and they need to know who hasn't completed it. Can SecOps "
            "pull the completion data from our training platform?",
            "We need to generate a compliance report showing security awareness training completion rates "
            "by department. Our auditors require evidence that all employees completed the annual phishing "
            "awareness and data protection modules.",
        ),
        gold=ScenarioGold(
            category="Security & Compliance",
            priority="P4",
            assigned_team="Security Operations",
            needs_escalation=False,
            missing_information=(),
            next_best_action="Generate the training completion report from the security awareness platform",
            remediation_steps=(
                "Export the training completion data from the awareness platform",
                "Generate a report broken down by department and completion status",
                "Identify employees who haven't completed mandatory training",
                "Send reminder notifications to non-compliant employees",
                "Share the report with HR and the auditing team",
            ),
        ),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 26. Shadow IT — unauthorized SaaS tool
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="security-026",
        subjects=(
            "Discovered unauthorized SaaS tool in use",
            "Shadow IT: team using unapproved cloud service",
        ),
        descriptions=(
            "I discovered that the Marketing team has been using an unapproved SaaS tool called 'DesignHub "
            "Pro' for the past 3 months. They're uploading client brand assets and campaign materials to "
            "it. It wasn't vetted by Security and they're paying with a corporate credit card.",
            "Our CASB flagged that 15 employees are using an unapproved file sharing service (MegaShare) to "
            "exchange large files with external partners. This service hasn't been through our security "
            "review and may not meet our data protection standards.",
        ),
        gold=ScenarioGold(
            category="Security & Compliance",
            priority="P3",
            assigned_team="Security Operations",
            needs_escalation=False,
            missing_information=(
                "affected_users",
                "business_impact",
            ),
            next_best_action="Assess the risk of the unauthorized SaaS tool and work with the team to find an approved "
                "alternative",
            remediation_steps=(
                "Conduct a security assessment of the unauthorized SaaS tool",
                "Identify what data has been uploaded and assess the risk exposure",
                "Work with the team to understand their business need",
                "Recommend an approved alternative that meets their requirements",
                "Block the unapproved service at the proxy/CASB level after migration",
            ),
        ),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 27. Former employee still has active VPN
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="security-027",
        subjects=(
            "ALERT: Terminated employee still has VPN access",
            "Former employee's credentials still active",
        ),
        descriptions=(
            "A former employee who was terminated 2 weeks ago still has active VPN credentials. We "
            "discovered this because they connected to the VPN last night from their home IP. Their AD "
            "account was disabled but somehow VPN access wasn't revoked. This is a critical security gap.",
            "Urgent: HR confirmed an employee was let go on March 15 but their VPN account is still active. "
            "Our logs show successful VPN connections from this person on March 20, 22, and 25. They may "
            "have accessed sensitive systems post-termination.",
        ),
        gold=ScenarioGold(
            category="Security & Compliance",
            priority="P1",
            assigned_team="Security Operations",
            needs_escalation=True,
            missing_information=(),
            next_best_action="Immediately revoke all access for the former employee and investigate post-termination "
                "activity",
            remediation_steps=(
                "Revoke VPN credentials and all remaining access immediately",
                "Review VPN logs to determine what was accessed post-termination",
                "Check for any data exfiltration or unauthorized changes",
                "Audit the offboarding process to find the gap that left VPN active",
                "Implement automated deprovisioning that covers all access types",
            ),
        ),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 28. Encrypted email configuration request
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="security-028",
        subjects=(
            "How to send encrypted emails to external parties?",
            "Need to enable email encryption for client communications",
        ),
        descriptions=(
            "Our Legal team needs to send encrypted emails to outside counsel. We know Outlook has "
            "encryption capabilities but we're not sure how to enable it or if it works with recipients who "
            "don't use Microsoft email. Can SecOps help set this up?",
            "I need to send sensitive financial documents to a client via encrypted email. I see an "
            "'Encrypt' button in Outlook but I want to make sure it actually works properly and the "
            "recipient can decrypt it. They use Gmail.",
        ),
        gold=ScenarioGold(
            category="Security & Compliance",
            priority="P4",
            assigned_team="Security Operations",
            needs_escalation=False,
            missing_information=(),
            next_best_action="Provide guidance on Microsoft 365 message encryption configuration and usage",
            remediation_steps=(
                "Verify Microsoft 365 Message Encryption is enabled for the organization",
                "Provide instructions on using the Encrypt button in Outlook",
                "Explain how external recipients access encrypted messages (OTP or Microsoft account)",
                "Test encrypted email flow with the specific recipient",
                "If enhanced encryption is needed, configure S/MIME certificates",
            ),
        ),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 29. Sensitive document on public SharePoint site
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="security-029",
        subjects=(
            "ALERT: Confidential document found on public SharePoint",
            "Sensitive client data exposed on externally shared site",
        ),
        descriptions=(
            "I just discovered that a spreadsheet containing client SSNs and account balances was uploaded "
            "to a SharePoint site that has anonymous external sharing enabled. The file has been accessible "
            "to anyone with the link for at least 2 weeks. This is a data breach.",
            "A document classified as 'Highly Confidential' containing M&A deal terms was found on a "
            "SharePoint site shared with 'Everyone except external users.' This information is material "
            "non-public information (MNPI) and its exposure could be an SEC violation.",
        ),
        gold=ScenarioGold(
            category="Security & Compliance",
            priority="P1",
            assigned_team="Security Operations",
            needs_escalation=True,
            missing_information=(),
            next_best_action="Remove the exposed document immediately and assess the scope of the data exposure",
            remediation_steps=(
                "Remove the sensitive document from the public SharePoint site immediately",
                "Disable external sharing on the site",
                "Review access logs to determine who accessed the document",
                "Notify Legal and Compliance about the potential data breach",
                "Assess regulatory notification requirements based on the data exposed",
            ),
        ),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 30. Active data exfiltration in progress
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="security-030",
        subjects=(
            "CRITICAL: Suspected data exfiltration in progress",
            "Active security incident — data leaving the network",
        ),
        descriptions=(
            "Our SIEM is alerting on massive outbound data transfers from an internal server to an external "
            "IP. Over 50 GB has been transferred in the past 2 hours via encrypted HTTPS. The source server "
            "is our HR database server. This appears to be active data exfiltration and needs immediate "
            "response.",
            "INCIDENT IN PROGRESS: Abnormal outbound traffic detected from the Client Data warehouse "
            "server. 30 GB transferred to an unknown cloud storage endpoint in the past hour. No scheduled "
            "transfers should be occurring. This looks like an active breach.",
        ),
        gold=ScenarioGold(
            category="Security & Compliance",
            priority="P1",
            assigned_team="Security Operations",
            needs_escalation=True,
            missing_information=(),
            next_best_action=(
                "Block the exfiltration immediately and contain the affected server — activate the incident "
                "response team"
            ),
            remediation_steps=(
                "Block the destination IP at the firewall immediately to stop the transfer",
                "Isolate the source server from the network while preserving evidence",
                "Activate the full incident response team and notify the CISO",
                "Capture forensic images of the affected server",
                "Begin investigation into how the attacker gained access and what data was exfiltrated",
            ),
        ),
    ),
]
