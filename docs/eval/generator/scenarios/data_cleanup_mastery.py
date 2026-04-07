"""Mastery-level data cleanup scenario definitions.

Covers extreme noise patterns: Zalgo text, control characters, URL-encoded
bodies, tab-delimited data dumps, SQL query dumps, single-line walls of text,
base64-encoded full bodies, deeply nested JSON, mixed RTL/LTR Unicode,
corrupted PDF extraction, inline SVG, auto-generated alert floods,
phone transcripts, hex dumps, excessive punctuation, merged ticket artifacts,
Windows Event Log XML, and double-encoded Mojibake.
"""

import base64

from generator.models import Scenario

_ZALGO_CHARS = "\u0335\u0310\u0366\u0300\u0336\u030f\u0312\u0360"

_BASE64_BLOCK = base64.b64encode(
    b"This is a test message about a SharePoint access issue. "
    b"I need access to the M&A deal room urgently."
).decode()

_TAB_ROWS = "\n".join(
    f"SRV-{i:03d}\t{'CRITICAL' if i % 7 == 0 else 'OK'}\t{90 + i % 10}%"
    for i in range(1, 31)
)

_ALERT_LINES = "\n".join(
    f"[ALERT {i:04d}] WARNING: Service health check failed at 2026-03-18T{8 + i // 60:02d}:{i % 60:02d}:00Z"
    for i in range(50)
)

_HEX_ROWS = "\n".join(
    f"0x{i * 16:08x}  " + " ".join(f"{(i * 16 + j) % 256:02x}" for j in range(16))
    for i in range(15)
)

SCENARIOS: list[Scenario] = [
    # ──────────────────────────────────────────────────────────────
    # 1. Zalgo text with combining Unicode characters
    # ──────────────────────────────────────────────────────────────
    Scenario(
        scenario_id="cleanup-mastery-zalgo-text",
        category="Software & Applications",
        priority="P2",
        assigned_team="Enterprise Applications",
        needs_escalation=False,
        missing_information=["error_message"],
        subjects=[
            f"O{_ZALGO_CHARS}utlook cra{_ZALGO_CHARS}shing on startup",
            f"E{_ZALGO_CHARS}xcel freez{_ZALGO_CHARS}ing with large files",
        ],
        descriptions=[
            f"H{_ZALGO_CHARS}i IT,\n\n"
            f"My Out{_ZALGO_CHARS}look 365 crash{_ZALGO_CHARS}es every time I open it. "
            f"I get a Visual C++ runtime error. This star{_ZALGO_CHARS}ted after the latest "
            f"Windows Update. Already tried /resetnavpane and safe mode.\n\n"
            f"Ple{_ZALGO_CHARS}ase help.",
            f"Exc{_ZALGO_CHARS}el hangs for 2+ minutes when open{_ZALGO_CHARS}ing our "
            f"quarterly financial model (85MB file with pivot tab{_ZALGO_CHARS}les). "
            f"This started after the Office upda{_ZALGO_CHARS}te last Tuesday. "
            f"Other smaller files open fi{_ZALGO_CHARS}ne.",
        ],
        next_best_actions=[
            "Investigate Outlook crash caused by Visual C++ runtime error after Windows Update.",
            "Check Excel performance with large files after recent Office update.",
        ],
        remediation_steps=[
            [
                "Run Office Quick Repair from Control Panel",
                "Check for conflicting COM add-ins by starting Outlook in safe mode",
                "Update Visual C++ Redistributable to latest version",
                "If crash persists, run full Online Repair of Office installation",
            ],
        ],
        tags=["data-cleanup", "zalgo", "unicode-combining"],
    ),
    # ──────────────────────────────────────────────────────────────
    # 2. Control characters embedded in ticket body
    # ──────────────────────────────────────────────────────────────
    Scenario(
        scenario_id="cleanup-mastery-control-chars",
        category="Network & Connectivity",
        priority="P2",
        assigned_team="Network Operations",
        needs_escalation=False,
        missing_information=["network_location"],
        subjects=[
            "Network share not mapping on login",
            "Cannot access shared drive after reboot",
        ],
        descriptions=[
            "Hi,\x01\x02\x03\n\n"
            "My network drive \\\\contoso-fs01\\shared\\trading is not\x04\x05 "
            "mapping automatically on login. I used to have it as Z: drive.\x06\x07 "
            "gpresult /r shows the policy is applied but drive doesn't appear.\x08 "
            "Manual mapping gives 'System error 53'.\x0b\x0c\n\n"
            "Marcus Chen\x0e\x0f\nTrading Floor",
            "Cannot access \\\\fs-nyc-02\\compliance\x01\x02 after rebooting my "
            "laptop this morning.\x03\x04 Error code: 0x80070035 — The network "
            "path was not found.\x05\x06 Other network resources work fine.\x07",
        ],
        next_best_actions=[
            "Investigate network drive mapping failure with System error 53 — check DNS and SMB connectivity.",
            "Check network path resolution and SMB signing configuration.",
        ],
        remediation_steps=[
            [
                "Verify DNS resolution for the file server hostname",
                "Test SMB connectivity: net view \\\\contoso-fs01",
                "Check Group Policy drive mapping settings in gpresult",
                "Verify SMB signing requirements match between client and server",
                "If DNS issue, flush DNS cache and renew DHCP lease",
            ],
        ],
        tags=["data-cleanup", "control-chars", "binary-artifact"],
    ),
    # ──────────────────────────────────────────────────────────────
    # 3. Entire body is URL-encoded
    # ──────────────────────────────────────────────────────────────
    Scenario(
        scenario_id="cleanup-mastery-url-encoded-body",
        category="Hardware & Peripherals",
        priority="P3",
        assigned_team="Endpoint Engineering",
        needs_escalation=False,
        missing_information=["device_info"],
        subjects=[
            "Screen flickering issue",
            "Display problems with external monitor",
        ],
        descriptions=[
            "Hi%20IT%2C%0A%0AMy%20laptop%20screen%20is%20flickering%20"
            "intermittently.%20It%20happens%20every%2010-15%20minutes.%20"
            "Dell%20Latitude%205540%2C%20Windows%2011%2C%20Intel%20Iris%20Xe.%20"
            "The%20external%20monitor%20is%20a%20Dell%20U2722D%20via%20USB-C.%0A%0A"
            "Thanks%2C%0AAisha%20Patel",
            "My%20monitor%20keeps%20going%20black%20for%202-3%20seconds%20"
            "then%20comes%20back.%20Happens%20about%205%20times%20per%20hour.%20"
            "Connected%20via%20DisplayPort%20to%20a%20Lenovo%20ThinkPad%20dock.",
        ],
        next_best_actions=[
            "Investigate screen flickering on Dell Latitude 5540 with external monitor via USB-C.",
            "Check monitor connection and display driver for intermittent blackouts.",
        ],
        remediation_steps=[
            [
                "Update Intel Iris Xe graphics driver to latest version",
                "Test with a different USB-C cable or port on the dock",
                "Check display refresh rate settings (lower to 60Hz if higher)",
                "Try connecting monitor directly via HDMI to rule out dock issue",
            ],
        ],
        tags=["data-cleanup", "url-encoded", "form-corruption"],
    ),
    # ──────────────────────────────────────────────────────────────
    # 4. Tab-delimited server monitoring data dump
    # ──────────────────────────────────────────────────────────────
    Scenario(
        scenario_id="cleanup-mastery-tab-data-dump",
        category="Data & Storage",
        priority="P1",
        assigned_team="Data Platform",
        needs_escalation=True,
        missing_information=["affected_users"],
        subjects=[
            "Server SRV-007 needs immediate attention — monitoring data attached",
            "CRITICAL: Database replication server at 96% CPU",
        ],
        descriptions=[
            "Hi team,\n\nHere's the monitoring data:\n\n"
            f"SERVER\tSTATUS\tCPU\n{_TAB_ROWS}\n\n"
            "SRV-007 is CRITICAL — primary database replication server for London. "
            "96% CPU, 0MB free memory. This is blocking settlement processing.",
            "Full server health report from this morning:\n\n"
            f"{_TAB_ROWS}\n\n"
            "Please investigate SRV-007 immediately. Replication job appears stuck.",
        ],
        next_best_actions=[
            "Investigate SRV-007 critical status — high CPU and memory exhaustion on DB replication server.",
            "Check database replication job status on SRV-007 and clear stuck jobs.",
        ],
        remediation_steps=[
            [
                "Check running queries on SRV-007 for long-running or blocked operations",
                "Verify replication agent status and clear any stuck jobs",
                "Check disk space and tempdb growth on the replication server",
                "Restart SQL Server Agent if replication jobs are orphaned",
                "Monitor CPU and memory after intervention to confirm recovery",
            ],
        ],
        tags=["data-cleanup", "tab-delimited", "monitoring-dump"],
    ),
    # ──────────────────────────────────────────────────────────────
    # 5. SQL query dump in ticket body
    # ──────────────────────────────────────────────────────────────
    Scenario(
        scenario_id="cleanup-mastery-sql-dump",
        category="Access & Authentication",
        priority="P3",
        assigned_team="Identity & Access Management",
        needs_escalation=False,
        missing_information=["affected_users"],
        subjects=[
            "Need help with stale account cleanup — query results attached",
            "Bulk disable request for 847 inactive accounts",
        ],
        descriptions=[
            "Hi IAM team,\n\n"
            "I ran this query:\n\n"
            "SELECT u.user_id, u.display_name, u.last_login,\n"
            "       DATEDIFF(day, u.last_login, GETDATE()) AS days_inactive\n"
            "FROM dbo.Users u\n"
            "WHERE u.account_status = 'active'\n"
            "    AND u.last_login < DATEADD(month, -3, GETDATE())\n"
            "ORDER BY u.last_login ASC;\n\n"
            "/* 847 rows returned */\n\n"
            "Per SEC-POL-007, accounts inactive 90+ days should be disabled. "
            "Can you run the bulk disable process?",
            "SQL output shows 847 stale accounts:\n\n"
            "SELECT * FROM Users WHERE last_login < '2025-12-18';\n\n"
            "Please schedule bulk disable per our security policy.",
        ],
        next_best_actions=[
            "Process bulk account disable request for 847 inactive accounts per security policy SEC-POL-007.",
            "Review stale account list and schedule bulk disable operation.",
        ],
        remediation_steps=[
            [
                "Verify the query results against the current Active Directory",
                "Exclude service accounts and shared mailboxes from the disable list",
                "Run the bulk disable in a maintenance window with rollback capability",
                "Notify affected department heads before disabling accounts",
                "Generate a report of disabled accounts for audit trail",
            ],
        ],
        tags=["data-cleanup", "sql-dump", "code-paste"],
    ),
    # ──────────────────────────────────────────────────────────────
    # 6. Base64-encoded entire email body
    # ──────────────────────────────────────────────────────────────
    Scenario(
        scenario_id="cleanup-mastery-base64-full-body",
        category="Access & Authentication",
        priority="P2",
        assigned_team="Identity & Access Management",
        needs_escalation=False,
        missing_information=["error_message"],
        subjects=[
            "SharePoint access issue — URGENT",
            "403 Forbidden on deal room SharePoint site",
        ],
        descriptions=[
            "Content-Transfer-Encoding: base64\nContent-Type: text/plain; charset=UTF-8\n\n"
            + _BASE64_BLOCK,
            "Content-Transfer-Encoding: base64\n\n"
            + base64.b64encode(
                b"Cannot access https://contoso.sharepoint.com/sites/MA-Atlas. "
                b"Getting 403 Forbidden since yesterday. Was working fine before."
            ).decode(),
        ],
        next_best_actions=[
            "Restore SharePoint access to the M&A deal room — user getting 403 Forbidden error.",
            "Investigate 403 Forbidden error on SharePoint site for the user.",
        ],
        remediation_steps=[
            [
                "Check the user's SharePoint permissions on the deal room site",
                "Verify the user's Azure AD group memberships haven't changed",
                "Check if the site collection has new conditional access policies",
                "Re-grant access if permissions were accidentally removed",
                "Test access from different browser/device to rule out caching",
            ],
        ],
        tags=["data-cleanup", "base64-full-body", "mime-encoding"],
    ),
    # ──────────────────────────────────────────────────────────────
    # 7. Auto-generated repetitive monitoring alerts
    # ──────────────────────────────────────────────────────────────
    Scenario(
        scenario_id="cleanup-mastery-alert-flood",
        category="Network & Connectivity",
        priority="P1",
        assigned_team="Network Operations",
        needs_escalation=True,
        missing_information=["affected_users"],
        subjects=[
            "FW: [PagerDuty] API Gateway health check failures (100+ alerts)",
            "URGENT: API gateway returning 503s — alert dump attached",
        ],
        descriptions=[
            f"Auto-forwarded from PagerDuty:\n\n{_ALERT_LINES}\n\n"
            "Please investigate why the API gateway is returning 503s. "
            "Backend services seem fine — might be load balancer health probe config.",
            f"Alert flood:\n\n{_ALERT_LINES}\n\n"
            "API gateway has been failing since 6 AM. Suspect the health probe "
            "configuration change from yesterday's maintenance window.",
        ],
        next_best_actions=[
            "Investigate API gateway 503 errors — possible load balancer health probe misconfiguration.",
            "Check load balancer health probe settings changed in yesterday's maintenance window.",
        ],
        remediation_steps=[
            [
                "Review load balancer health probe configuration for recent changes",
                "Check API gateway pod/container health and restart if needed",
                "Verify backend service endpoints are reachable from the load balancer subnet",
                "Roll back health probe configuration if yesterday's change caused the issue",
                "Set up proper health check endpoint that validates backend connectivity",
            ],
        ],
        tags=["data-cleanup", "alert-flood", "monitoring-dump"],
    ),
    # ──────────────────────────────────────────────────────────────
    # 8. Phone transcript with timestamps and speaker labels
    # ──────────────────────────────────────────────────────────────
    Scenario(
        scenario_id="cleanup-mastery-phone-transcript",
        category="Software & Applications",
        priority="P2",
        assigned_team="Enterprise Applications",
        needs_escalation=False,
        missing_information=["error_message"],
        subjects=[
            "Phone call transcript — Excel crash on large file",
            "Transcribed call: user reporting spreadsheet crashes",
        ],
        descriptions=[
            "[Call Start: 2026-03-18 09:14:22 EST]\n"
            "[00:00] AGENT: How can I help?\n"
            "[00:05] CALLER: Excel keeps crashing on my financial model.\n"
            "[00:12] AGENT: Which version?\n"
            "[00:17] CALLER: Microsoft 365, version 2402.\n"
            "[00:28] AGENT: When does it crash?\n"
            "[00:33] CALLER: When opening our 85MB quarterly model with VLOOKUPs.\n"
            "[00:48] AGENT: Error message?\n"
            "[00:51] CALLER: 'Excel has stopped working.'\n"
            "[Call End: 2026-03-18 09:16:02 EST]",
            "[00:00] AGENT: IT support, how can I help?\n"
            "[00:03] USER: My PowerPoint crashes whenever I try to save.\n"
            "[00:10] AGENT: Is it a specific file?\n"
            "[00:13] USER: Yes, a 200-slide deck with embedded videos.\n"
            "[00:25] USER: It just says 'not responding' when I hit save.\n"
            "[00:35] AGENT: Creating a ticket for this.",
        ],
        next_best_actions=[
            "Investigate Excel crash on large 85MB financial model file after Office 2402 update.",
            "Investigate PowerPoint crash when saving large presentation with embedded videos.",
        ],
        remediation_steps=[
            [
                "Test opening the file in Excel safe mode (hold Ctrl while launching)",
                "Check if the file has volatile functions causing recalculation on open",
                "Try opening the file on a different machine to rule out local issues",
                "Run Office Online Repair if the crash affects multiple files",
            ],
        ],
        tags=["data-cleanup", "phone-transcript", "speaker-labels"],
    ),
    # ──────────────────────────────────────────────────────────────
    # 9. Binary/hex dump pasted in description
    # ──────────────────────────────────────────────────────────────
    Scenario(
        scenario_id="cleanup-mastery-hex-dump",
        category="Software & Applications",
        priority="P1",
        assigned_team="Enterprise Applications",
        needs_escalation=True,
        missing_information=["affected_users"],
        subjects=[
            "Application crash with memory dump — heap corruption",
            "ContosoTrader crash — WinDbg output attached",
        ],
        descriptions=[
            f"ContosoTrader v4.2.1 crashing with access violation:\n\n{_HEX_ROWS}\n\n"
            "Crash at ntdll!RtlAllocateHeap — looks like heap corruption. "
            "Affects 12 traders on derivatives desk.",
            f"Memory dump from crash:\n\n{_HEX_ROWS}\n\n"
            "Stack trace shows corruption in the options pricing module. "
            "This is blocking all options trading for the morning session.",
        ],
        next_best_actions=[
            "Investigate heap corruption crash in ContosoTrader affecting 12 derivatives traders.",
            "Debug access violation in options pricing module of ContosoTrader.",
        ],
        remediation_steps=[
            [
                "Collect full crash dump using procdump -ma for detailed analysis",
                "Enable page heap verification to catch heap corruption source",
                "Check for recent updates to ContosoTrader or its dependencies",
                "Roll back to previous version if recently updated",
                "Engage application development team for code-level debugging",
            ],
        ],
        tags=["data-cleanup", "hex-dump", "debug-output"],
    ),
    # ──────────────────────────────────────────────────────────────
    # 10. Excessive punctuation and decorative characters
    # ──────────────────────────────────────────────────────────────
    Scenario(
        scenario_id="cleanup-mastery-excessive-punctuation",
        category="Network & Connectivity",
        priority="P1",
        assigned_team="Network Operations",
        needs_escalation=True,
        missing_information=[],
        subjects=[
            "!!! *** URGENT *** !!! WiFi NOT WORKING !!! ★★★ HELP ★★★ !!!",
            "★★★ EXTREMELY URGENT ★★★ Entire floor has no WiFi ★★★",
        ],
        descriptions=[
            "!!!!!!!!!!!!!!!!!!\n★★★★★★ EXTREMELY URGENT ★★★★★★\n▬▬▬▬▬▬▬▬▬▬▬▬▬▬▬\n\n"
            "THE WIFI ON THE ENTIRE 4TH FLOOR IS DOWN!!!!!!!\n"
            "Building 2, NYC. All 50+ people affected since 8 AM.\n"
            "APs show solid red (CONTOSO-AP-4F-01 through 4F-08).\n"
            "Ethernet still works. Client meetings at 10 AM!!!!!!\n\n"
            "★★★ THIS IS BLOCKING THE ENTIRE FLOOR ★★★",
            "◆◆◆ CRITICAL ◆◆◆ WiFi down on Floor 7!!!!!!\n"
            ">>>>> ALL access points showing red LED <<<<<\n"
            "50+ users affected, conference rooms unusable.\n"
            "===== PLEASE RESPOND IMMEDIATELY =====",
        ],
        next_best_actions=[
            "Investigate complete WiFi outage on Floor 4, Building 2 — all 8 APs showing red LED.",
            "Investigate WiFi outage affecting 50+ users on Floor 7.",
        ],
        remediation_steps=[
            [
                "Check the PoE switch serving Floor 4 APs for power or port issues",
                "Verify VLAN and SSID configuration on the wireless controller",
                "Check if a recent firmware push to the APs caused the outage",
                "Power cycle the APs in sequence and monitor recovery",
                "If switch issue, fail over to redundant uplink if available",
            ],
        ],
        tags=["data-cleanup", "excessive-punctuation", "special-chars"],
    ),
    # ──────────────────────────────────────────────────────────────
    # 11. Mixed RTL/LTR Unicode (Hebrew + English)
    # ──────────────────────────────────────────────────────────────
    Scenario(
        scenario_id="cleanup-mastery-rtl-ltr-mix",
        category="Network & Connectivity",
        priority="P2",
        assigned_team="Network Operations",
        needs_escalation=False,
        missing_information=["network_location"],
        subjects=[
            "VPN connection issue — \u05d1\u05e2\u05d9\u05d4 \u05d1\u05d7\u05d9\u05d1\u05d5\u05e8 VPN",
            "GlobalProtect error GP-0011 — \u05e9\u05e2\u05e8 VPN \u05dc\u05d0 \u05e0\u05d2\u05d9\u05e9",
        ],
        descriptions=[
            "\u05e9\u05dc\u05d5\u05dd \u05e6\u05d5\u05d5\u05ea IT,\n\n"
            "I am trying to connect to GlobalProtect VPN gateway vpn-eu.contoso.com "
            "but keep getting error GP-0011 (Gateway not reachable). "
            "\u05d4\u05d1\u05e2\u05d9\u05d4 \u05d4\u05ea\u05d7\u05d9\u05dc\u05d4 "
            "\u05d0\u05d7\u05e8\u05d9 \u05e9\u05d3\u05e8\u05d5\u05d2 \u05d4\u05e8\u05e9\u05ea. "
            "My colleague can connect fine. Windows 11 with GP 6.2.1.\n\n"
            "\u05ea\u05d5\u05d3\u05d4,\nDaniel Levy",
            "\u05e9\u05dc\u05d5\u05dd,\n\n"
            "VPN \u05dc\u05d0 \u05e2\u05d5\u05d1\u05d3. "
            "GlobalProtect shows 'portal unreachable' error. "
            "\u05d0\u05e0\u05d9 \u05d1\u05de\u05e9\u05e8\u05d3 \u05ea\u05dc \u05d0\u05d1\u05d9\u05d1. "
            "Local network works — only VPN is broken.",
        ],
        next_best_actions=[
            "Investigate GlobalProtect VPN connectivity failure with GP-0011 error.",
            "Check VPN gateway reachability from the Tel Aviv office network.",
        ],
        remediation_steps=[
            [
                "Verify VPN gateway vpn-eu.contoso.com is reachable via ping/traceroute",
                "Check if there's a firewall rule change blocking VPN traffic from the office",
                "Verify the GlobalProtect portal configuration hasn't changed",
                "Try connecting to an alternate VPN gateway if available",
                "Check with the network team if the office uplink has issues",
            ],
        ],
        tags=["data-cleanup", "rtl-ltr-mix", "hebrew", "bidi"],
    ),
    # ──────────────────────────────────────────────────────────────
    # 12. Merged multi-ticket artifact
    # ──────────────────────────────────────────────────────────────
    Scenario(
        scenario_id="cleanup-mastery-merged-tickets",
        category="Security & Compliance",
        priority="P1",
        assigned_team="Security Operations",
        needs_escalation=True,
        missing_information=["affected_system"],
        subjects=[
            "[MERGED] Multiple issues — compliance + facilities",
            "Two tickets accidentally merged by the system",
        ],
        descriptions=[
            "=== TICKET A (Original) ===\n"
            "Compliance monitoring system shows 47 trade records failed to sync to "
            "the audit database. Error: FK_CONSTRAINT_VIOLATION. SOX compliance "
            "issue — records needed in audit trail within 24 hours.\n\n"
            "=== MERGED WITH TICKET B ===\n"
            "Badge reader on 3rd floor south entrance stopped working. "
            "Employees propping door open — security concern.",
            "=== MERGED TICKETS ===\n"
            "Ticket 1: DLP alert — 500+ emails with PII sent to personal addresses. "
            "Needs immediate investigation per data protection policy.\n\n"
            "Ticket 2: Coffee machine on Floor 2 is broken. "
            "Not dispensing hot water. Please send facilities.",
        ],
        next_best_actions=[
            "Prioritize the compliance issue: investigate 47 failed trade record syncs for SOX audit trail.",
            "Prioritize the DLP alert: investigate bulk PII email exfiltration.",
        ],
        remediation_steps=[
            [
                "Investigate the database FK constraint violation blocking trade record sync",
                "Manually sync the 47 failed records to meet the SOX 24-hour deadline",
                "Create a separate ticket for the badge reader issue",
                "Notify compliance team of the sync delay and remediation progress",
            ],
        ],
        tags=["data-cleanup", "merged-tickets", "multi-issue"],
    ),
    # ──────────────────────────────────────────────────────────────
    # 13. Deeply nested JSON config dump
    # ──────────────────────────────────────────────────────────────
    Scenario(
        scenario_id="cleanup-mastery-nested-json",
        category="Network & Connectivity",
        priority="P1",
        assigned_team="Network Operations",
        needs_escalation=True,
        missing_information=["configuration_details"],
        subjects=[
            "AKS ingress not routing after config change — config dump attached",
            "502 Bad Gateway on production API — Kubernetes config below",
        ],
        descriptions=[
            'Hi team,\n\nAfter applying this config:\n\n{\n  "cluster": {\n    "config": {\n'
            '      "ingress": {\n        "controller": {\n          "replicas": 3,\n'
            '          "resources": {\n            "limits": {"cpu": "2000m"}\n'
            "          }\n        }\n      }\n    }\n  }\n}\n\n"
            "Ingress controller stopped routing. All requests return 502. "
            "Think the subnet annotation is wrong (aks-subnet-01 vs 02).",
            "Config causing 502:\n\n"
            '{"ingress":{"tls":{"enabled":true,"secret":"contoso-tls",'
            '"ca":{"issuer":{"name":"letsencrypt","config":{"acme":'
            '{"server":"https://acme-v02.api.letsencrypt.org"}}}}}}}"\n\n'
            "Cert rotation happened yesterday, might be TLS related.",
        ],
        next_best_actions=[
            "Investigate 502 Bad Gateway after AKS ingress config change — check subnet annotation and TLS.",
            "Debug Kubernetes ingress routing failure — likely config or TLS issue.",
        ],
        remediation_steps=[
            [
                "Check ingress controller pod logs for errors",
                "Verify the subnet annotation matches the current AKS subnet",
                "Check TLS certificate validity and secret reference",
                "Roll back the config change if it was the trigger",
                "Test with a simple health check endpoint to isolate the issue",
            ],
        ],
        tags=["data-cleanup", "nested-json", "kubernetes-config"],
    ),
    # ──────────────────────────────────────────────────────────────
    # 14. Emoji-only subject line
    # ──────────────────────────────────────────────────────────────
    Scenario(
        scenario_id="cleanup-mastery-emoji-subject",
        category="Access & Authentication",
        priority="P2",
        assigned_team="Identity & Access Management",
        needs_escalation=True,
        missing_information=["authentication_method"],
        subjects=[
            "🔒🚫💻😭🆘❗❗❗",
            "🔑❌🖥️😱⚠️🔴",
        ],
        descriptions=[
            "I can't log in to the finance portal since this morning. "
            "Shows 'account locked due to too many failed attempts.' "
            "I didn't try multiple times — someone else may be trying my account. "
            "Username: jpark-fin. Need access for quarterly close.",
            "Locked out of all systems. Error says 'account disabled by administrator' "
            "but nobody told me about this. Need immediate access restored.",
        ],
        next_best_actions=[
            "Investigate account lockout — possible brute force attack on user jpark-fin.",
            "Restore user account access and investigate reason for administrative disablement.",
        ],
        remediation_steps=[
            [
                "Check Active Directory for lockout source (failed login IP addresses)",
                "Verify if lockout was caused by brute force attempts or misconfigured service",
                "Unlock the account and reset password if compromise is suspected",
                "Enable MFA if not already configured for this account",
                "Review security logs for the affected time period",
            ],
        ],
        tags=["data-cleanup", "emoji-subject", "minimal-metadata"],
    ),
    # ──────────────────────────────────────────────────────────────
    # 15. Double-encoded Mojibake
    # ──────────────────────────────────────────────────────────────
    Scenario(
        scenario_id="cleanup-mastery-mojibake",
        category="Network & Connectivity",
        priority="P3",
        assigned_team="Network Operations",
        needs_escalation=False,
        missing_information=["device_info"],
        subjects=[
            "Wi-Fi disconnecting \u00e2\u0080\u0093 limited connectivity",
            "Wifi keeps dropping \u00e2\u0080\u0094 showing \u00e2\u0080\u009cpoor signal\u00e2\u0080\u009d",
        ],
        descriptions=[
            "I\u00e2\u0080\u0099m having trouble with my laptop\u00e2\u0080\u0099s Wi-Fi. "
            "It keeps disconnecting and shows \u00e2\u0080\u009cpoor\u00e2\u0080\u009d signal "
            "even next to the AP. Error: \u00e2\u0080\u009cLimited connectivity\u00e2\u0080\u009d. "
            "Intel Wi-Fi 6E AX211. Driver update didn\u00e2\u0080\u0099t help.",
            "Wi-Fi is unstable \u00e2\u0080\u0094 drops every 5 minutes. "
            "Signal shows \u00e2\u0080\u009cweak\u00e2\u0080\u009d despite being 3m from AP. "
            "Colleague on same floor has no issues.",
        ],
        next_best_actions=[
            "Investigate Wi-Fi disconnection with Intel AX211 adapter — poor signal despite proximity to AP.",
            "Debug Wi-Fi instability — possible driver or AP channel configuration issue.",
        ],
        remediation_steps=[
            [
                "Check wireless adapter power management settings (disable power saving)",
                "Update Intel AX211 driver from Intel's download center (not Windows Update)",
                "Check the AP channel utilization and DFS status",
                "Test on 2.4GHz band if issue is only on 5GHz/6GHz",
                "Replace the wireless adapter if driver updates don't resolve",
            ],
        ],
        tags=["data-cleanup", "mojibake", "double-encoding"],
    ),
]
