"""Advanced data cleanup edge-case scenario definitions.

Covers scenarios not in the base data_cleanup module: CSV/spreadsheet data in
ticket bodies, XML/SOAP fault messages, ANSI terminal escape codes, auto-reply
chains, concatenated multi-issue tickets, NDR bounce-backs, massive email
signatures, URL-encoded content, JSON config dumps, RTF formatting artifacts,
OCR recognition errors, inconsistent date formats, ASCII art tables, raw
markdown, and MIME multipart boundaries.
"""

from generator.models import Scenario

SCENARIOS: list[Scenario] = [
    # ──────────────────────────────────────────────────────────────────
    # 1. CSV / spreadsheet data embedded in ticket body
    # ──────────────────────────────────────────────────────────────────
    Scenario(
        scenario_id="cleanup-csv-embedded-data",
        category="Data & Storage",
        priority="P2",
        assigned_team="Data Platform",
        needs_escalation=False,
        missing_information=["affected_users", "business_impact"],
        subjects=[
            "Database performance issue — metrics pasted below",
            "Slow SQL queries on billing DB — see data export",
        ],
        descriptions=[
            "Hi IT,\n\nOur billing database is running very slow. "
            "Here are the metrics I exported from the monitoring dashboard:\n\n"
            "ServerName,CPU_Percent,Memory_MB,DiskIO_IOPS,QueryTime_ms,ActiveConnections,Status\n"
            "SQLPROD-01,87.3,28672,4500,2340,185,WARNING\n"
            "SQLPROD-02,92.1,30720,5200,3100,210,CRITICAL\n"
            "SQLPROD-03,45.6,16384,1200,450,62,OK\n"
            "SQLPROD-04,89.7,29184,4800,2890,195,WARNING\n"
            "SQLREP-01,23.4,8192,300,120,15,OK\n"
            "SQLREP-02,67.8,20480,2100,890,98,WARNING\n"
            "BKUP-SQL-01,12.1,4096,150,45,3,OK\n"
            "BKUP-SQL-02,15.3,4096,180,52,5,OK\n"
            "ETL-PROC-01,78.9,24576,3800,1560,142,WARNING\n"
            "ETL-PROC-02,81.2,25600,3900,1680,155,WARNING\n"
            "CACHE-01,34.5,65536,800,25,320,OK\n"
            "CACHE-02,36.7,65536,850,28,340,OK\n"
            "LB-SQL-01,22.3,2048,100,5,0,OK\n"
            "LB-SQL-02,23.1,2048,110,6,0,OK\n"
            "MONITOR-01,8.5,1024,50,3,2,OK\n\n"
            "The billing team says month-end reports that used to take 5 minutes now take over "
            "30 minutes. This started about 3 days ago. Please investigate SQLPROD-01 and "
            "SQLPROD-02 specifically.",
            "Pasting the performance CSV from our monitoring tool — something is clearly wrong "
            "with the production SQL cluster:\n\n"
            "timestamp,server,metric,value,threshold,alert_level\n"
            "2026-03-12T09:00:00Z,SQLPROD-01,cpu,87.3,80.0,HIGH\n"
            "2026-03-12T09:00:00Z,SQLPROD-01,memory,93.2,90.0,HIGH\n"
            "2026-03-12T09:00:00Z,SQLPROD-01,disk_iops,4500,4000,HIGH\n"
            "2026-03-12T09:00:00Z,SQLPROD-02,cpu,92.1,80.0,CRITICAL\n"
            "2026-03-12T09:00:00Z,SQLPROD-02,memory,96.8,90.0,CRITICAL\n"
            "2026-03-12T09:00:00Z,SQLPROD-02,disk_iops,5200,4000,CRITICAL\n"
            "2026-03-12T09:00:00Z,SQLPROD-02,query_time_ms,3100,1000,CRITICAL\n\n"
            "Billing reports are timing out. This is urgent for month-end.",
        ],
        next_best_actions=[
            "Investigate high CPU and memory on SQLPROD-01/02 — check for long-running "
            "queries, missing indexes, or parameter sniffing issues.",
            "Analyze slow billing queries — review execution plans and index usage on "
            "production SQL cluster.",
        ],
        remediation_steps=[
            [
                "Identify the top long-running queries on SQLPROD-01 and SQLPROD-02",
                "Review execution plans for billing report stored procedures",
                "Check for missing or fragmented indexes on billing tables",
                "Verify no blocking or deadlocking is occurring",
                "Consider temporarily scaling up resources during month-end",
            ],
        ],
        tags=["data-cleanup", "csv-data", "embedded-data"],
    ),
    # ──────────────────────────────────────────────────────────────────
    # 2. XML / SOAP fault message pasted into description
    # ──────────────────────────────────────────────────────────────────
    Scenario(
        scenario_id="cleanup-xml-soap-fault",
        category="Software & Applications",
        priority="P2",
        assigned_team="Enterprise Applications",
        needs_escalation=False,
        missing_information=["environment_details", "steps_to_reproduce"],
        subjects=[
            "Web service integration failing — SOAP fault attached",
            "ERP integration error — XML error response below",
        ],
        descriptions=[
            "Our ERP integration with the vendor API started returning errors this morning. "
            "Here's the full SOAP response I captured:\n\n"
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            "<soap:Envelope "
            'xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" '
            'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '
            'xmlns:xsd="http://www.w3.org/2001/XMLSchema">\n'
            "  <soap:Body>\n"
            "    <soap:Fault>\n"
            "      <faultcode>soap:Server</faultcode>\n"
            "      <faultstring>System.ServiceModel.FaultException: "
            "The request channel timed out attempting to send after 00:01:00. "
            "Increase the timeout value passed to the call to Request or increase "
            "the SendTimeout value on the Binding.\n"
            "   at System.ServiceModel.Channels.RequestChannel.Request("
            "Message message, TimeSpan timeout)\n"
            "   at System.ServiceModel.Dispatcher.RequestChannelBinder.Request("
            "Message message, TimeSpan timeout)\n"
            "   at System.ServiceModel.Channels.ServiceChannel.Call("
            "String action, Boolean oneway, ProxyOperationRuntime operation)\n"
            "      </faultstring>\n"
            "      <detail>\n"
            "        <ErrorInfo "
            'xmlns="http://vendor.example.com/api/v2/errors">\n'
            "          <ErrorCode>TIMEOUT_001</ErrorCode>\n"
            "          <Severity>Critical</Severity>\n"
            "          <Timestamp>2026-03-14T08:23:45.123Z</Timestamp>\n"
            "          <CorrelationId>a1b2c3d4-e5f6-7890-abcd-ef1234567890"
            "</CorrelationId>\n"
            "          <ServerNode>APPSVR-PROD-03</ServerNode>\n"
            "        </ErrorInfo>\n"
            "      </detail>\n"
            "    </soap:Fault>\n"
            "  </soap:Body>\n"
            "</soap:Envelope>\n\n"
            "This is blocking all purchase order submissions. About 50 orders are queued up.",
        ],
        next_best_actions=[
            "Investigate SOAP timeout on vendor API integration — check network latency, "
            "connection pool exhaustion, and vendor API health.",
            "Review WCF binding configuration for send timeout and check vendor API status.",
        ],
        remediation_steps=[
            [
                "Check vendor API status page and contact vendor support if down",
                "Review WCF binding SendTimeout configuration",
                "Check network latency between application server and vendor endpoint",
                "Verify connection pool settings and look for leaked connections",
                "Implement retry logic with exponential backoff if not already present",
            ],
        ],
        tags=["data-cleanup", "xml-soap", "embedded-data"],
    ),
    # ──────────────────────────────────────────────────────────────────
    # 3. ANSI terminal escape codes in pasted output
    # ──────────────────────────────────────────────────────────────────
    Scenario(
        scenario_id="cleanup-ansi-escape-codes",
        category="Software & Applications",
        priority="P2",
        assigned_team="Enterprise Applications",
        needs_escalation=False,
        missing_information=["environment_details", "application_version"],
        subjects=[
            "CI/CD pipeline deployment failed — error output below",
            "Build pipeline broken — terminal output attached inline",
        ],
        descriptions=[
            "The nightly deployment pipeline failed. Here's the terminal output I copied:\n\n"
            "\x1b[36m[2026-03-14 02:15:33]\x1b[0m Starting deployment pipeline v3.2.1\n"
            "\x1b[32m[INFO]\x1b[0m  Pulling latest artifacts from registry...\n"
            "\x1b[32m[INFO]\x1b[0m  Artifact: app-service:2026.3.14-nightly \x1b[32m✓\x1b[0m\n"
            "\x1b[32m[INFO]\x1b[0m  Running pre-deployment health checks...\n"
            "\x1b[33m[WARN]\x1b[0m  Database migration check: 3 pending migrations\n"
            "\x1b[32m[INFO]\x1b[0m  Applying migration 0047_add_audit_columns...\n"
            "\x1b[31m[ERROR]\x1b[0m Migration 0047_add_audit_columns \x1b[1;31mFAILED\x1b[0m\n"
            "\x1b[31m[ERROR]\x1b[0m \x1b[1mSqlException:\x1b[0m Column 'created_by' "
            "already exists in table 'orders'\n"
            "\x1b[31m[ERROR]\x1b[0m Stack trace:\n"
            "\x1b[90m  at Migrator.ApplyMigration(Migration m) in "
            "/src/Migrator.cs:line 142\x1b[0m\n"
            "\x1b[90m  at Pipeline.RunMigrations() in "
            "/src/Pipeline.cs:line 87\x1b[0m\n"
            "\x1b[31m[FATAL]\x1b[0m \x1b[1;31mDeployment aborted. "
            "Rolling back...\x1b[0m\n"
            "\x1b[33m[WARN]\x1b[0m  Rollback completed. Previous version restored.\n\n"
            "This is the third time this week the migration has failed. "
            "We need help fixing the migration script.",
        ],
        next_best_actions=[
            "Investigate failed database migration — column 'created_by' already exists, "
            "suggesting migration was partially applied or manually run previously.",
            "Fix migration 0047_add_audit_columns — add idempotent column existence check.",
        ],
        remediation_steps=[
            [
                "Check if migration 0047 was partially applied in a previous run",
                "Add IF NOT EXISTS guards to the migration DDL statements",
                "Verify migration tracking table is in sync with actual schema",
                "Re-run the pipeline after fixing the migration script",
                "Add pre-deployment schema validation to prevent future conflicts",
            ],
        ],
        tags=["data-cleanup", "ansi-codes", "terminal-output"],
    ),
    # ──────────────────────────────────────────────────────────────────
    # 4. Auto-reply / out-of-office chain mixed with real issue
    # ──────────────────────────────────────────────────────────────────
    Scenario(
        scenario_id="cleanup-auto-reply-chain-v2",
        category="Network & Connectivity",
        priority="P3",
        assigned_team="Network Operations",
        needs_escalation=False,
        missing_information=["error_message", "device_info"],
        subjects=[
            "RE: RE: Out of Office: RE: VPN connection drops repeatedly",
            "FW: Automatic reply: RE: VPN not working",
        ],
        descriptions=[
            "--- Auto-Reply ---\n"
            "Thank you for your email. I am currently out of the office from March 10-17 "
            "with limited access to email. For urgent matters, please contact my backup "
            "Sarah Chen (s.chen@contoso.com) or call the IT help desk at x4357.\n"
            "Best regards, James Wilson\n\n"
            "--- Auto-Reply ---\n"
            "I am out of the office attending the Global Sales Conference in Orlando. "
            "I will return on March 18th and respond to your email then.\n"
            "If this is time-sensitive, please reach out to Mark Thompson (m.thompson@contoso.com).\n"
            "Regards, Amanda Peters\n\n"
            "--- Original Message ---\n"
            "From: David Kim <d.kim@contoso.com>\n"
            "Subject: VPN connection drops repeatedly\n\n"
            "Hi IT team,\n\n"
            "I've been having persistent VPN disconnections since yesterday. The VPN client "
            "connects successfully but drops the connection every 10-15 minutes. I work from "
            "home and this is severely impacting my productivity. I'm on the Seattle office VPN "
            "profile using the Cisco AnyConnect client.\n\n"
            "Thanks,\nDavid",
        ],
        next_best_actions=[
            "Ignore auto-reply content — investigate VPN disconnection issue for David Kim "
            "using Cisco AnyConnect on Seattle profile.",
            "Troubleshoot intermittent VPN drops — check client configuration, DPD settings, "
            "and ISP stability.",
        ],
        remediation_steps=[
            [
                "Check Cisco AnyConnect client version and update if needed",
                "Review VPN concentrator logs for David Kim's session disconnects",
                "Verify Dead Peer Detection (DPD) and keepalive settings",
                "Test with a different VPN profile to isolate the issue",
                "Check for ISP-related packet loss or MTU issues",
            ],
        ],
        tags=["data-cleanup", "auto-reply", "out-of-office"],
    ),
    # ──────────────────────────────────────────────────────────────────
    # 5. Multiple tickets concatenated into one submission
    # ──────────────────────────────────────────────────────────────────
    Scenario(
        scenario_id="cleanup-concatenated-tickets",
        category="General Inquiry",
        priority="P3",
        assigned_team="Endpoint Engineering",
        needs_escalation=False,
        missing_information=["error_message", "device_info", "steps_to_reproduce"],
        subjects=[
            "Several issues — printer + Outlook + WiFi",
            "Multiple problems that need fixing ASAP",
        ],
        descriptions=[
            "Hi IT,\n\nI have several issues I need help with:\n\n"
            "ISSUE 1: PRINTER\n"
            "The printer on the 4th floor (HP LaserJet near Room 412) keeps jamming. "
            "Every time I print more than 5 pages it jams. I've cleared the paper path "
            "twice today already.\n\n"
            "ISSUE 2: OUTLOOK\n"
            "Outlook crashes every time I try to open a meeting invite with more than 20 "
            "attendees. It just freezes and I have to force-close it. This has been happening "
            "since last week's update.\n\n"
            "ISSUE 3: WIFI\n"
            "The WiFi in the west wing conference rooms is extremely slow. Speed tests show "
            "less than 5 Mbps down when we need at least 50 Mbps for video calls. It's been "
            "like this for about 2 weeks.\n\n"
            "Can you please look into ALL of these? They're all affecting my team's "
            "productivity.\n\nThanks,\nLisa",
        ],
        next_best_actions=[
            "Create separate tickets for each issue — printer jam (Endpoint), Outlook crash "
            "(Enterprise Apps), WiFi performance (Network Ops). Triage each independently.",
            "Split into three tickets: printer hardware, Outlook software, WiFi network. "
            "Advise reporter to submit separate tickets in the future.",
        ],
        remediation_steps=[
            [
                "Create separate tickets for each distinct issue for proper routing",
                "Route printer issue to Endpoint Engineering for hardware inspection",
                "Route Outlook crash to Enterprise Applications for investigation",
                "Route WiFi performance to Network Operations for AP analysis",
                "Advise user to submit separate tickets for unrelated issues",
            ],
        ],
        tags=["data-cleanup", "concatenated", "multi-issue"],
    ),
    # ──────────────────────────────────────────────────────────────────
    # 6. NDR / Email bounce-back pasted as ticket body
    # ──────────────────────────────────────────────────────────────────
    Scenario(
        scenario_id="cleanup-ndr-bounceback",
        category="Software & Applications",
        priority="P3",
        assigned_team="Enterprise Applications",
        needs_escalation=False,
        missing_information=["affected_users", "timestamp"],
        subjects=[
            "Can't email client — error message below",
            "Email delivery failure to external address",
        ],
        descriptions=[
            "I keep getting this bounce-back when I try to email our client. Can you help?\n\n"
            "--- Non-Delivery Report ---\n"
            "Delivery has failed to these recipients or groups:\n\n"
            "john.doe@clientcorp.com\n"
            "The email address you entered couldn't be found. Please check the recipient's "
            "email address and try to resend the message.\n\n"
            "Diagnostic information for administrators:\n"
            "Generating server: EXCH-PROD-02.contoso.com\n\n"
            "john.doe@clientcorp.com\n"
            "Remote Server returned '550 5.1.1 RESOLVER.ADR.RecipNotFound; "
            "not found #SMTP#'\n\n"
            "Original message headers:\n"
            "Received: from EXCH-PROD-02.contoso.com (10.50.12.44) by\n"
            " EXCH-HUB-01.contoso.com (10.50.12.10) with Microsoft SMTP Server\n"
            " (version=TLS1_2, cipher=TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384) id\n"
            " 15.2.1118.26; Thu, 14 Mar 2026 10:15:23 -0500\n"
            "Message-ID: <abc123@EXCH-PROD-02.contoso.com>\n"
            "From: Lisa Park <l.park@contoso.com>\n"
            "To: John Doe <john.doe@clientcorp.com>\n"
            "Subject: Q1 Contract Review\n"
            "Date: Thu, 14 Mar 2026 10:15:22 -0500\n"
            "X-Mailer: Microsoft Outlook 16.0\n"
            "MIME-Version: 1.0\n"
            "Content-Type: multipart/mixed;\n"
            ' boundary="----=_NextPart_000_0001_01DAF23A.B8C7D890"\n\n'
            "I've been trying to send this for two days. The contract review is due Friday.",
        ],
        next_best_actions=[
            "Investigate 550 RESOLVER.ADR.RecipNotFound error — verify recipient address "
            "with client and check for DNS/MX record issues for clientcorp.com.",
            "Check if clientcorp.com MX records are resolving correctly and verify the "
            "recipient address is valid.",
        ],
        remediation_steps=[
            [
                "Verify the recipient email address is correct with the client",
                "Check DNS resolution and MX records for clientcorp.com",
                "Test email delivery to another address at clientcorp.com",
                "Check if clientcorp.com has blocked contoso.com domain",
                "If address is correct, contact clientcorp IT to verify mailbox exists",
            ],
        ],
        tags=["data-cleanup", "ndr-bounceback", "email-headers"],
    ),
    # ──────────────────────────────────────────────────────────────────
    # 7. Massive email signature burying the actual issue
    # ──────────────────────────────────────────────────────────────────
    Scenario(
        scenario_id="cleanup-massive-signature-v2",
        category="Access & Authentication",
        priority="P3",
        assigned_team="Identity & Access Management",
        needs_escalation=False,
        missing_information=["error_message", "steps_to_reproduce"],
        subjects=[
            "Can't access SharePoint after password change",
            "Login issue after credential update",
        ],
        descriptions=[
            "I changed my password yesterday and now I can't access SharePoint. "
            "It keeps saying my credentials are invalid.\n\n"
            "Best regards,\n\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            "Robert J. Henderson III\n"
            "Senior Vice President, Global Strategic Partnerships\n"
            "Enterprise Solutions Division\n"
            "Contoso International Holdings, Ltd.\n\n"
            "Office: +1 (425) 555-0142 ext. 7834\n"
            "Mobile: +1 (206) 555-0198\n"
            "Fax: +1 (425) 555-0143\n\n"
            "Email: r.henderson@contoso.com\n"
            "LinkedIn: linkedin.com/in/robert-henderson-contoso\n"
            "Twitter: @RHendersonContoso\n\n"
            "🏢 Contoso Tower, Suite 4200\n"
            "    1234 Innovation Boulevard\n"
            "    Redmond, WA 98052\n"
            "    United States of America\n\n"
            "🌐 www.contoso.com | www.contoso-partners.com\n\n"
            "📞 24/7 Partner Hotline: 1-800-CONTOSO\n\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
            "CONFIDENTIALITY NOTICE: This email and any attachments are for the exclusive "
            "and confidential use of the intended recipient. If you are not the intended "
            "recipient, please do not read, distribute, or take action based on this "
            "message. If you have received this in error, please notify the sender "
            "immediately by return email and delete this message from your system. "
            "Any unauthorized use, disclosure, or distribution is strictly prohibited "
            "and may be unlawful.\n\n"
            "ENVIRONMENTAL NOTICE: Please consider the environment before printing this "
            "email. 🌿\n\n"
            "LEGAL DISCLAIMER: The views and opinions expressed in this email are those "
            "of the author and do not necessarily reflect the official policy or position "
            "of Contoso International Holdings, Ltd. or any of its subsidiaries. This "
            "email does not constitute legal, financial, or professional advice.\n\n"
            "ISO 27001 CERTIFIED | SOC 2 TYPE II COMPLIANT | GDPR READY\n\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n",
        ],
        next_best_actions=[
            "Investigate SharePoint authentication failure after password change — likely "
            "cached credentials or token refresh issue.",
            "Check for stale cached credentials in Windows Credential Manager and verify "
            "Azure AD token refresh.",
        ],
        remediation_steps=[
            [
                "Clear cached credentials in Windows Credential Manager",
                "Sign out and sign back in to all Microsoft 365 applications",
                "Check if Azure AD password sync has completed",
                "Verify the new password meets SharePoint access policy requirements",
                "If issue persists, reset the user's Azure AD session tokens",
            ],
        ],
        tags=["data-cleanup", "massive-signature", "buried-issue"],
    ),
    # ──────────────────────────────────────────────────────────────────
    # 8. URL-encoded content in description
    # ──────────────────────────────────────────────────────────────────
    Scenario(
        scenario_id="cleanup-url-encoded-content-v2",
        category="Software & Applications",
        priority="P3",
        assigned_team="Enterprise Applications",
        needs_escalation=False,
        missing_information=["error_message", "environment_details"],
        subjects=[
            "Web application error — URL with error code below",
            "Internal portal returning errors — see encoded URL",
        ],
        descriptions=[
            "I'm getting errors on our internal portal. Here's the URL I see when it fails "
            "(I copied it from the browser bar):\n\n"
            "https%3A%2F%2Fportal.contoso.com%2Fapp%2Finvoice-management%2F"
            "error%3Fcode%3D500%26message%3DInternal%2520Server%2520Error%26"
            "timestamp%3D2026-03-14T10%253A30%253A00Z%26trace_id%3D"
            "7f8a9b2c-3d4e-5f6a-8b9c-0d1e2f3a4b5c%26"
            "module%3Dinvoice_processing%26action%3Dsubmit_batch%26"
            "user%3Dl.park%2540contoso.com%26"
            "session%3Ds_abc123def456%26"
            "details%3DNull%2520reference%2520exception%2520in%2520"
            "BatchProcessor.ProcessInvoice%2528%2529\n\n"
            "This happens every time I try to submit a batch of invoices. "
            "Single invoices work fine but batch submissions fail.",
        ],
        next_best_actions=[
            "Investigate NullReferenceException in BatchProcessor.ProcessInvoice — "
            "decode the URL parameters to extract the trace ID and error details.",
            "Debug batch invoice submission failure — 500 error with null reference "
            "in BatchProcessor module.",
        ],
        remediation_steps=[
            [
                "Decode the URL-encoded error details to identify the exact error",
                "Look up trace_id 7f8a9b2c-3d4e-5f6a-8b9c-0d1e2f3a4b5c in application logs",
                "Investigate NullReferenceException in BatchProcessor.ProcessInvoice",
                "Check for differences between single and batch invoice code paths",
                "Deploy a fix and verify batch submission works end-to-end",
            ],
        ],
        tags=["data-cleanup", "url-encoded", "web-error"],
    ),
    # ──────────────────────────────────────────────────────────────────
    # 9. JSON config dump with hundreds of lines
    # ──────────────────────────────────────────────────────────────────
    Scenario(
        scenario_id="cleanup-json-config-dump",
        category="Network & Connectivity",
        priority="P3",
        assigned_team="Network Operations",
        needs_escalation=False,
        missing_information=["error_message", "steps_to_reproduce", "environment_details"],
        subjects=[
            "Firewall config not working — full config pasted below",
            "Network rules config broken — please review JSON",
        ],
        descriptions=[
            "This firewall config doesn't work. Please fix it:\n\n"
            "{\n"
            '  "firewall_config": {\n'
            '    "version": "3.2.1",\n'
            '    "last_modified": "2026-03-13T22:45:00Z",\n'
            '    "modified_by": "netadmin@contoso.com",\n'
            '    "global_settings": {\n'
            '      "default_action": "deny",\n'
            '      "logging_level": "verbose",\n'
            '      "max_connections": 50000,\n'
            '      "connection_timeout_seconds": 300,\n'
            '      "icmp_rate_limit": 100,\n'
            '      "syn_flood_protection": true,\n'
            '      "geo_blocking_enabled": true,\n'
            '      "blocked_countries": ["XX", "YY", "ZZ"],\n'
            '      "ssl_inspection": {\n'
            '        "enabled": true,\n'
            '        "certificate": "/etc/ssl/fw-inspect.pem",\n'
            '        "bypass_categories": ["banking", "healthcare"],\n'
            '        "min_tls_version": "1.2"\n'
            "      }\n"
            "    },\n"
            '    "zones": [\n'
            '      {"name": "DMZ", "interface": "eth0", "vlan_id": 100},\n'
            '      {"name": "Internal", "interface": "eth1", "vlan_id": 200},\n'
            '      {"name": "Guest", "interface": "eth2", "vlan_id": 300},\n'
            '      {"name": "Servers", "interface": "eth3", "vlan_id": 400}\n'
            "    ],\n"
            '    "rules": [\n'
            '      {"id": 1, "name": "Allow DNS", "source": "Internal", '
            '"destination": "DMZ", "port": 53, "protocol": "udp", "action": "allow"},\n'
            '      {"id": 2, "name": "Allow HTTP", "source": "Internal", '
            '"destination": "any", "port": 80, "protocol": "tcp", "action": "allow"},\n'
            '      {"id": 3, "name": "Allow HTTPS", "source": "Internal", '
            '"destination": "any", "port": 443, "protocol": "tcp", "action": "allow"},\n'
            '      {"id": 4, "name": "Allow SMTP", "source": "Servers", '
            '"destination": "DMZ", "port": 25, "protocol": "tcp", "action": "allow"},\n'
            '      {"id": 5, "name": "Block Guest to Internal", "source": "Guest", '
            '"destination": "Internal", "port": "any", "protocol": "any", "action": "deny"},\n'
            '      {"id": 6, "name": "Allow Guest Internet", "source": "Guest", '
            '"destination": "any", "port": "443,80", "protocol": "tcp", "action": "allow"},\n'
            '      {"id": 7, "name": "Allow SSH Admin", "source": "10.0.1.0/24", '
            '"destination": "Servers", "port": 22, "protocol": "tcp", "action": "allow"},\n'
            '      {"id": 8, "name": "Allow RDP", "source": "Internal", '
            '"destination": "Servers", "port": 3389, "protocol": "tcp", "action": "allow"},\n'
            '      {"id": 9, "name": "Allow VPN", "source": "any", '
            '"destination": "DMZ", "port": 443, "protocol": "tcp", "action": "allow"},\n'
            '      {"id": 10, "name": "Block All", "source": "any", '
            '"destination": "any", "port": "any", "protocol": "any", "action": "deny"}\n'
            "    ],\n"
            '    "nat_rules": [\n'
            '      {"type": "SNAT", "source": "Internal", "translated": "203.0.113.1"},\n'
            '      {"type": "DNAT", "source": "any", "port": 443, "translated": "10.0.4.10:443"}\n'
            "    ]\n"
            "  }\n"
            "}\n\n"
            "After applying this config, guest WiFi users can't access the internet at all.",
        ],
        next_best_actions=[
            "Review firewall rule configuration — guest internet access rule (ID 6) may have "
            "incorrect port format or rule ordering issue.",
            "Analyze rule ordering and guest zone configuration for internet access blockage.",
        ],
        remediation_steps=[
            [
                "Check rule 6 port format — '443,80' may need to be separate rules or use range syntax",
                "Verify rule ordering — rule 5 (deny guest→internal) may be blocking DNS lookups",
                "Ensure guest zone has DNS resolution allowed (add DNS rule for guest zone)",
                "Check NAT rules — guest traffic may not have proper SNAT configured",
                "Test guest WiFi after each change to identify the specific blocking rule",
            ],
        ],
        tags=["data-cleanup", "json-dump", "config-data"],
    ),
    # ──────────────────────────────────────────────────────────────────
    # 10. RTF / Word formatting artifacts
    # ──────────────────────────────────────────────────────────────────
    Scenario(
        scenario_id="cleanup-rtf-artifacts",
        category="Hardware & Peripherals",
        priority="P3",
        assigned_team="Endpoint Engineering",
        needs_escalation=False,
        missing_information=["device_info", "error_message"],
        subjects=[
            "Laptop docking station not working",
            "Docking station display issues",
        ],
        descriptions=[
            r"{\rtf1\ansi\ansicpg1252\deff0\nouicompat{\fonttbl{\f0\fswiss\fcharset0 "
            r"Calibri;}{\f1\fnil\fcharset2 Symbol;}}" "\n"
            r"{\*\generator Riched20 10.0.22621}\viewkind4\uc1" "\n"
            r"\pard\sa200\sl276\slmult1\f0\fs22\lang9 "
            "My laptop docking station stopped working this morning."
            r"\par" "\n"
            r"\b Issue Details:\b0\par" "\n"
            r"{\pntext\f1\'B7\tab}"
            "When I connect my laptop to the dock, the external monitors don't turn on"
            r"\par" "\n"
            r"{\pntext\f1\'B7\tab}"
            "USB devices connected to the dock are not recognized"
            r"\par" "\n"
            r"{\pntext\f1\'B7\tab}"
            "The dock's power LED is amber instead of green"
            r"\par" "\n"
            r"{\pntext\f1\'B7\tab}"
            "Ethernet through the dock also doesn't work"
            r"\par" "\n"
            r"\b What I\rquote ve tried:\b0\par" "\n"
            r"{\pntext\f1\'B7\tab}Unplugged and reconnected the dock\par" "\n"
            r"{\pntext\f1\'B7\tab}Restarted my laptop\par" "\n"
            r"{\pntext\f1\'B7\tab}Tried a different USB-C cable\par" "\n"
            r"}\par" "\n"
            "The dock worked fine yesterday before I left.",
        ],
        next_best_actions=[
            "Investigate docking station failure — amber LED indicates hardware or firmware "
            "issue. Check firmware version and power delivery.",
            "Troubleshoot docking station — check firmware update, power supply, and USB-C "
            "port on the laptop.",
        ],
        remediation_steps=[
            [
                "Check docking station firmware version and update if available",
                "Verify the dock power supply is delivering sufficient wattage",
                "Test the laptop's USB-C port with a different peripheral",
                "Try the dock with a different laptop to isolate the issue",
                "If amber LED persists after firmware update, request dock replacement",
            ],
        ],
        tags=["data-cleanup", "rtf-artifacts", "formatting"],
    ),
    # ──────────────────────────────────────────────────────────────────
    # 11. Screenshot OCR with recognition artifacts
    # ──────────────────────────────────────────────────────────────────
    Scenario(
        scenario_id="cleanup-ocr-artifacts",
        category="Software & Applications",
        priority="P2",
        assigned_team="Enterprise Applications",
        needs_escalation=False,
        missing_information=["screenshot_or_attachment", "steps_to_reproduce"],
        subjects=[
            "App1ication err0r — copied from screen",
            "SAP err0r message (screenshot text)",
        ],
        descriptions=[
            "I t00k a screenshot of the err0r and c0pied the text:\n\n"
            "Micr0soft Dynamics 365 — Fata1 Err0r\n"
            "────────────────────────────\n"
            "An unhand1ed excepti0n has 0ccurred in the app1ication.\n\n"
            "Err0r C0de: CRM_EXC_0x80040265\n"
            "M0dule: Sa1esF0rceAut0mation.d11\n"
            "Descripti0n: 0bject reference n0t set t0 an\n"
            "instance 0f an 0bject\n\n"
            "Stack Trace (partia1):\n"
            "  at Micr0s0ft.Dynamics.Sa1es.Pipe1ine\n"
            "  .ProcessLead(1nt32 1eadId) in\n"
            "  C:\\src\\Sa1es\\Pipe1ine.cs:1ine 247\n"
            "  at Micr0s0ft.Dynamics.Runtime\n"
            "  .ExecuteP1ugin(IP1ugin p1ugin) in\n"
            "  C:\\src\\Runtime\\Executor.cs:1ine 89\n\n"
            "P1ease save y0ur w0rk and restart the\n"
            "app1ication. If the pr0b1em persists,\n"
            "c0ntact y0ur system administrat0r.\n\n"
            "[0K] [Cancel]\n\n"
            "This happens every time I try to 0pen a 1ead rec0rd. Very frustratlng.",
        ],
        next_best_actions=[
            "Investigate Dynamics 365 NullReferenceException in SalesForceAutomation module — "
            "decode OCR artifacts to extract actual error code CRM_EXC_0x80040265.",
            "Debug CRM plugin error on lead processing — check for null references in "
            "Pipeline.ProcessLead method.",
        ],
        remediation_steps=[
            [
                "Identify actual error code from OCR text — likely CRM_EXC_0x80040265",
                "Check Dynamics 365 server logs for the full stack trace",
                "Investigate NullReferenceException in ProcessLead method",
                "Verify lead record data integrity — check for corrupted records",
                "Deploy plugin fix if a code defect is found",
            ],
        ],
        tags=["data-cleanup", "ocr-artifacts", "garbled"],
    ),
    # ──────────────────────────────────────────────────────────────────
    # 12. Inconsistent date/time formats throughout
    # ──────────────────────────────────────────────────────────────────
    Scenario(
        scenario_id="cleanup-inconsistent-dates",
        category="Software & Applications",
        priority="P3",
        assigned_team="Enterprise Applications",
        needs_escalation=False,
        missing_information=["steps_to_reproduce", "reproduction_frequency"],
        subjects=[
            "Meeting scheduler showing wrong dates",
            "Calendar sync bug — dates are all mixed up",
        ],
        descriptions=[
            "The meeting scheduler is showing different dates depending on where you look:\n\n"
            "In the calendar view, my meeting shows as 03/15/2026 (March 15th).\n"
            "In the list view, same meeting shows as 15-Mar-26.\n"
            "The API returns it as 2026.03.14 (a day off!).\n"
            "The email confirmation said 'March 15, 2026 at 2:00 PM PST'.\n"
            "The export to CSV shows 1742054400 (Unix timestamp).\n"
            "The mobile app says 'Tue, 15 Mar 2026 22:00:00 GMT'.\n"
            "The iCal file has DTSTART:20260315T140000 with no timezone.\n"
            "My Outlook shows it as '3/15/2026 2:00 PM' but the web version says "
            "'15/3/2026 22:00' (which seems like UTC).\n\n"
            "I'm in the PST timezone. The meeting is supposed to be at 2 PM my time "
            "on March 15th. But I joined the Teams call at 2 PM and nobody was there. "
            "Turns out the API thinks the meeting is on the 14th.\n\n"
            "This is the third time this has happened with meetings that have attendees "
            "in different timezones.",
        ],
        next_best_actions=[
            "Investigate timezone handling in meeting scheduler — API returns different date "
            "than calendar views, suggesting UTC/local conversion bug.",
            "Debug timezone conversion issue — the API stores UTC but renders inconsistently "
            "across calendar, list, and mobile views.",
        ],
        remediation_steps=[
            [
                "Audit timezone handling across all calendar display surfaces",
                "Verify the API stores dates in UTC with proper timezone metadata",
                "Check the iCal export for missing VTIMEZONE components",
                "Test cross-timezone meeting creation and verify consistency",
                "Fix any surfaces that render UTC as local time or vice versa",
            ],
        ],
        tags=["data-cleanup", "date-formats", "inconsistent"],
    ),
    # ──────────────────────────────────────────────────────────────────
    # 13. ASCII art table formatting
    # ──────────────────────────────────────────────────────────────────
    Scenario(
        scenario_id="cleanup-ascii-art-table",
        category="Network & Connectivity",
        priority="P1",
        assigned_team="Network Operations",
        needs_escalation=True,
        missing_information=["affected_users", "business_impact"],
        subjects=[
            "Multiple servers offline — status table below",
            "URGENT: Server outage across multiple data centers",
        ],
        descriptions=[
            "Several production servers went offline in the last hour. Here's the current "
            "status from our monitoring tool:\n\n"
            "+------------------+----------+---------+-------+------------------+\n"
            "| Server           | Status   | DC      | Rack  | Last Seen        |\n"
            "+------------------+----------+---------+-------+------------------+\n"
            "| WEBPROD-01       | DOWN     | US-EAST | R12   | 2026-03-14 08:30 |\n"
            "| WEBPROD-02       | DOWN     | US-EAST | R12   | 2026-03-14 08:31 |\n"
            "| WEBPROD-03       | OK       | US-WEST | R04   | 2026-03-14 09:15 |\n"
            "| APPPROD-01       | DOWN     | US-EAST | R13   | 2026-03-14 08:28 |\n"
            "| APPPROD-02       | DOWN     | US-EAST | R13   | 2026-03-14 08:29 |\n"
            "| APPPROD-03       | OK       | US-WEST | R05   | 2026-03-14 09:15 |\n"
            "| DBPROD-01        | DEGRADED | US-EAST | R14   | 2026-03-14 08:35 |\n"
            "| DBPROD-02        | OK       | US-WEST | R06   | 2026-03-14 09:15 |\n"
            "| CACHE-01         | DOWN     | US-EAST | R12   | 2026-03-14 08:30 |\n"
            "| LB-PROD-01       | DEGRADED | US-EAST | R10   | 2026-03-14 08:32 |\n"
            "| LB-PROD-02       | OK       | US-WEST | R02   | 2026-03-14 09:15 |\n"
            "+------------------+----------+---------+-------+------------------+\n\n"
            "All DOWN servers are in US-EAST datacenter, racks R12-R14. Looks like it "
            "might be a power or network issue affecting those specific racks. US-WEST "
            "is fine. Customer-facing services are degraded.",
        ],
        next_best_actions=[
            "URGENT: Investigate US-EAST datacenter rack-level outage affecting R12-R14 — "
            "check power distribution and top-of-rack switches.",
            "Escalate to datacenter operations — multiple racks in US-EAST offline, likely "
            "power or network infrastructure failure.",
        ],
        remediation_steps=[
            [
                "Contact datacenter operations for US-EAST R12-R14 status",
                "Check power distribution unit (PDU) status for affected racks",
                "Verify top-of-rack switch connectivity for R12, R13, R14",
                "Failover customer traffic to US-WEST if not already done",
                "Once root cause is identified, bring servers back online in priority order",
            ],
        ],
        tags=["data-cleanup", "ascii-table", "monitoring-output"],
    ),
    # ──────────────────────────────────────────────────────────────────
    # 14. Raw markdown that wasn't rendered
    # ──────────────────────────────────────────────────────────────────
    Scenario(
        scenario_id="cleanup-raw-markdown",
        category="Software & Applications",
        priority="P2",
        assigned_team="Enterprise Applications",
        needs_escalation=False,
        missing_information=["error_message", "environment_details"],
        subjects=[
            "Deployment failed — notes from runbook below",
            "Production deployment issue — runbook steps and errors",
        ],
        descriptions=[
            "## Deployment Failure Report\n\n"
            "**Date:** 2026-03-14\n"
            "**Environment:** Production (PROD-CLUSTER-01)\n"
            "**Version:** v4.7.2 → v4.8.0\n\n"
            "### What Happened\n\n"
            "The deployment of `invoice-service` v4.8.0 failed during the "
            "rolling update phase. Here are the details:\n\n"
            "1. Pre-deployment checks **passed** ✅\n"
            "2. Database migration **passed** ✅\n"
            "3. Rolling update started — 3 of 8 pods updated\n"
            "4. Pod `invoice-service-7f8b9c-xk4pl` entered **CrashLoopBackOff** ❌\n"
            "5. Rolling update **halted** — automatic rollback triggered\n\n"
            "### Error Log\n\n"
            "```\n"
            "panic: runtime error: invalid memory address or nil pointer dereference\n"
            "[signal SIGSEGV: segmentation violation code=0x1 addr=0x0 pc=0x4a2f8c]\n"
            "\n"
            "goroutine 1 [running]:\n"
            "main.initializeCache(0x0)\n"
            "\t/app/cmd/server/main.go:142 +0x2c\n"
            "main.main()\n"
            "\t/app/cmd/server/main.go:87 +0x1a4\n"
            "```\n\n"
            "### Relevant Links\n\n"
            "- [Deployment Pipeline](https://ci.contoso.com/pipelines/invoice-service/482)\n"
            "- [Kubernetes Dashboard](https://k8s.contoso.com/namespaces/production)\n"
            "- [Previous Successful Deploy](https://ci.contoso.com/pipelines/invoice-service/479)\n\n"
            "### Action Needed\n\n"
            "The `initializeCache` function has a nil pointer because the **Redis connection "
            "string** environment variable `$REDIS_URL` is not set in the v4.8.0 deployment "
            "manifest. This was a _new dependency_ added in v4.8.0 that wasn't documented.\n\n"
            "> **Note:** v4.7.2 is currently running and stable.\n",
        ],
        next_best_actions=[
            "Fix v4.8.0 deployment manifest — add missing REDIS_URL environment variable "
            "and re-deploy.",
            "Update deployment manifest with REDIS_URL and add cache connection validation "
            "to startup checks.",
        ],
        remediation_steps=[
            [
                "Add REDIS_URL environment variable to v4.8.0 deployment manifest",
                "Verify Redis connectivity from the production namespace",
                "Add startup validation to check required environment variables before serving",
                "Re-run the deployment pipeline for v4.8.0",
                "Update the deployment runbook to include new Redis dependency",
            ],
        ],
        tags=["data-cleanup", "raw-markdown", "deployment"],
    ),
    # ──────────────────────────────────────────────────────────────────
    # 15. MIME multipart boundaries visible in email
    # ──────────────────────────────────────────────────────────────────
    Scenario(
        scenario_id="cleanup-mime-boundaries",
        category="Software & Applications",
        priority="P3",
        assigned_team="Enterprise Applications",
        needs_escalation=False,
        missing_information=["device_info", "application_version"],
        subjects=[
            "Email attachment problem — raw email data below",
            "Can't open email attachments — weird content showing",
        ],
        descriptions=[
            "When I try to open certain emails, instead of seeing the message and attachments "
            "normally, I see this raw content:\n\n"
            "MIME-Version: 1.0\n"
            "Content-Type: multipart/mixed;\n"
            ' boundary="----=_Part_12345_67890.1710412800000"\n\n'
            "------=_Part_12345_67890.1710412800000\n"
            "Content-Type: text/plain; charset=UTF-8\n"
            "Content-Transfer-Encoding: quoted-printable\n\n"
            "Hi team,\n\n"
            "Please find the Q1 financial report attached. Key highlights:\n"
            "- Revenue up 12% YoY\n"
            "- Operating margin improved to 23.5%\n"
            "- Customer acquisition cost down 8%\n\n"
            "Let me know if you have questions.\n\n"
            "Best,\nSarah\n\n"
            "------=_Part_12345_67890.1710412800000\n"
            "Content-Type: application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;\n"
            ' name="Q1_Financial_Report_2026.xlsx"\n'
            "Content-Transfer-Encoding: base64\n"
            "Content-Disposition: attachment;\n"
            ' filename="Q1_Financial_Report_2026.xlsx"\n\n'
            "UEsDBBQAAAAIAAAAAACyIhAAaAAAAGQAAAARAAAAZG9jUHJvcHMvY29yZS54bWyNkE1qwzAQhe+F\n"
            "3kHo3pEcl1JkZZNC6KKFJhfoShp7HIn+Icmpe/rKTkIh0M1jZr43846cbnqXfUGMLqChKLgo\n"
            "MgDt7Mb0DVVqALlwpVFBW0NRdq06pQi7nFT1fHUDaEuHzgKK...\n"
            "[truncated — 800+ more lines of base64 data]\n\n"
            "------=_Part_12345_67890.1710412800000--\n\n"
            "This only happens with emails from external senders. Internal emails display "
            "fine. I'm using the Outlook web app.",
        ],
        next_best_actions=[
            "Investigate MIME rendering failure in Outlook Web App for external emails — "
            "likely a content-type handling or Exchange transport rule issue.",
            "Check Exchange Online transport rules for external email processing — MIME "
            "parsing may be broken for certain senders.",
        ],
        remediation_steps=[
            [
                "Check Exchange transport rules for modifications to external email content",
                "Verify Outlook Web App rendering settings for MIME content",
                "Test with a specific external sender to reproduce the issue",
                "Check if any email security appliance is stripping MIME headers",
                "If transport rules are clean, escalate to Microsoft support",
            ],
        ],
        tags=["data-cleanup", "mime-boundaries", "email-rendering"],
    ),
]
