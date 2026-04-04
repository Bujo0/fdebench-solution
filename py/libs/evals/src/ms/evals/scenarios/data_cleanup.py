# Copyright (c) Microsoft. All rights reserved.
"""Data cleanup evaluation scenarios.

These scenarios test the triage API's robustness against noisy, malformed,
or unusual input data commonly found in enterprise IT ticket systems.
Each scenario has a legitimate underlying IT issue that should still be
triageable despite the data quality problems.
"""

from ms.evals.models.scenario import EvalReporter
from ms.evals.models.scenario import EvalScenario
from ms.evals.models.scenario import EvalTicket
from ms.evals.models.scenario import ExpectedTriage
from ms.evals.models.scenario import ScenarioCategory
from ms.evals.scenarios.registry import default_registry

_CATEGORY = ScenarioCategory.DATA_CLEANUP

_DEFAULT_REPORTER = EvalReporter(
    name="Test User",
    email="test.user@contoso.com",
    department="IT",
)


def _reporter(name: str, email: str, department: str) -> EvalReporter:
    return EvalReporter(name=name, email=email, department=department)


# ---------------------------------------------------------------------------
# dc-001: Very long email thread with buried IT issue
# ---------------------------------------------------------------------------
_LONG_THREAD_BODY = (
    "From: Sarah Mitchell <s.mitchell@contoso.com>\n"
    "To: IT Help Desk <helpdesk@contoso.com>\n"
    "Date: Wed, 18 Mar 2026 09:14:00 +0000\n"
    "Subject: Re: Re: Fwd: VPN Disconnection Issue - Urgent\n\n"
    "Hi team, just forwarding this again as we still haven't received a resolution.\n\n"
    "Best regards,\nSarah Mitchell\nSenior Trader | Equities Desk\n"
    "Contoso Financial Services\n"
    "Phone: +1 (212) 555-0147 | Fax: +1 (212) 555-0148\n"
    "Email: s.mitchell@contoso.com\n"
    "100 Wall Street, 24th Floor, New York, NY 10005\nwww.contoso.com\n\n"
    "CONFIDENTIALITY NOTICE: This email and any attachments are for the exclusive and confidential use "
    "of the intended recipient. If you are not the intended recipient, please do not read, distribute, "
    "or take action based on this message. If you have received this in error, please notify the sender "
    "immediately by reply email and destroy all copies of the original message.\n\n"
    + "---\n\n" * 3
    + (
        "> From: James Thornton <j.thornton@contoso.com>\n"
        "> Date: Tue, 17 Mar 2026 16:42:00 +0000\n"
        "> Subject: Re: Fwd: VPN Disconnection Issue - Urgent\n>\n"
        "> Sarah,\n>\n"
        "> I checked with the network team and they said they haven't seen any widespread issues. "
        "Can you try reconnecting using the alternate gateway? vpn2.contoso.com\n>\n"
        "> Regards,\n> James Thornton\n> Network Operations Lead\n"
    )
    + "\n" * 5
    + (
        "> > From: Sarah Mitchell <s.mitchell@contoso.com>\n"
        "> > Date: Tue, 17 Mar 2026 14:30:00 +0000\n"
        "> > Subject: Re: VPN Disconnection Issue - Urgent\n> >\n"
        "> > James, the issue is getting worse. My VPN dropped THREE times in 20 minutes while on a call "
        "with the Hong Kong desk. GlobalProtect shows error code GP-4017. This has been happening since "
        "Monday after the weekend maintenance window. Lenovo ThinkPad T14s, Windows 11, GP version 6.1.3. "
        "Already tried restarting, rebooting, and flushing DNS. Critical - major trade window tomorrow.\n"
    )
    + "\n" * 3
    + (
        "> > > From: James Thornton <j.thornton@contoso.com>\n"
        "> > > Date: Tue, 17 Mar 2026 10:15:00 +0000\n"
        "> > > Thanks for reporting this. Which VPN gateway are you connecting to?\n"
    )
    + "\n" * 3
    + (
        "> > > > From: Sarah Mitchell <s.mitchell@contoso.com>\n"
        "> > > > Date: Mon, 16 Mar 2026 09:00:00 +0000\n"
        "> > > > Subject: VPN Disconnection Issue\n"
        "> > > > Hi IT, my VPN has been dropping intermittently since this morning. "
        "I'm on the NYC office Wi-Fi, Floor 24. Not sure what changed.\n"
    )
    + "\n-- \n" + "This message has been scanned by Contoso Email Security.\n" * 5
)

default_registry.register(
    EvalScenario(
        scenario_id="dc-001",
        name="Very long email thread",
        description="Multi-reply email thread with email headers, signatures, and disclaimers. "
        "Real issue (VPN disconnection) is buried deep in the thread.",
        category=_CATEGORY,
        tags=["long_content", "email_thread", "noise"],
        ticket=EvalTicket(
            ticket_id="INC-5001",
            subject="Re: Re: Fwd: VPN Disconnection Issue - Urgent",
            description=_LONG_THREAD_BODY,
            reporter=_reporter("Sarah Mitchell", "s.mitchell@contoso.com", "Trading"),
            created_at="2026-03-18T09:14:00Z",
            channel="email",
        ),
        expected_triage=ExpectedTriage(
            category="Network & Connectivity",
            priority="P2",
            assigned_team="Network Operations",
        ),
    )
)


# ---------------------------------------------------------------------------
# dc-002: Base64 image data in description
# ---------------------------------------------------------------------------
_B64_IMAGE_CHUNK = (
    "3l5VkgeWjb4JSIyPYKqptaP3hDMcjasEBQXkYVQ87q+K7V+xtRZRlTo86hdn4xHrs6cDKg9Rc9yUegVq3EMl"
    "P/o+hnPoZcmIXULgZrEhcw4rC/7jSlOZfvEwKqH2rEWsVeqQYomVIK0wCKIzpNeZw4Z/9aGLQZt0x0368hlPH"
    "LnCD3S0wFTIYC8VMO74DEkydzUZa5Os61A1hA7QgjhiGiIYMyG86uITWQWeje9TM74mAmp9soL9H/yg5JKvc6b"
    "Lonvy6NPNrzKhA7gZJcdsssY+srm12era5+UjQwyOOPxndJled52XroGz6XusRq4BhM3PmfBcI6qaedEvFX2jY"
    "s4+V4slyGa7Y4mXfNUfPu9ALwjJcxv8UOAoMs0aoUO/SGUD/rSR5qNYDaCc"
)

default_registry.register(
    EvalScenario(
        scenario_id="dc-002",
        name="Base64 image data in description",
        description="Email with an inline base64-encoded image (screenshot). "
        "The actual IT issue is an MFA token failure.",
        category=_CATEGORY,
        tags=["base64", "image", "noise"],
        ticket=EvalTicket(
            ticket_id="INC-5002",
            subject="MFA not working - screenshot attached inline",
            description=(
                "Hi, my MFA token keeps failing when I try to log into the VPN. "
                "Here's a screenshot of the error I'm seeing:\n\n"
                f"[image data: data:image/png;base64,{_B64_IMAGE_CHUNK}]\n\n"
                "The error message says 'Token validation failed - code AUTH-2048'. "
                "This started happening after the Entra ID sync last night. "
                "I've tried re-registering my authenticator app but it still fails.\n\n"
                "Thanks,\nMike Davis\nWealth Management"
            ),
            reporter=_reporter("Mike Davis", "m.davis@contoso.com", "Wealth Management"),
            created_at="2026-03-18T08:45:00Z",
            channel="email",
        ),
        expected_triage=ExpectedTriage(
            category="Access & Authentication",
            priority="P2",
            assigned_team="Identity & Access Management",
        ),
    )
)


# ---------------------------------------------------------------------------
# dc-003: Base64 encoded log dump
# ---------------------------------------------------------------------------
_B64_LOG = (
    "RVJST1IgMjAyNi0wMy0xOCAwOToxNToyMiBbQXV0aE1vZHVsZV0gRmFpbGVkIHRvIHZhbGlkYXRlIE1GQS"
    "B0b2tlbiBmb3IgdXNlciBzYXJhaC5jaGVuQGNvbnRvc28uY29tLiBUb2tlbiBleHBpcmVkIGF0IDIwMjYtMDMt"
    "MThUMDk6MTA6MDBaLiBSZXRyeSBjb3VudDogMy4gTW9kdWxlOiBBenVyZUFELk1GQS5WYWxpZGF0b3IuIENv"
    "cnJlbGF0aW9uSWQ6IGE4ZjNjMmUxLTRiNWQtNGY2YS04YzlkLTBlMWYyYTNiNGM1ZGNBdRVM6FDx2/sW33OI"
    "eLh8DG8vQpIB8WGumYZbW04hDCs1DXmWgketP07qWifhgu3OygIkC6N1rWz9nDheC4DA5ap5U/gdlJb5sUj+T3"
    "JdQS7ya1etZK9tyJ1B9vxDytuhaNT1qW+xWWiWQKPK3tbKjbKPA5A8bDEMCiUa9v+8kDsipa6uvzyS4fitsGS"
    "SR08JJwmh8Q=="
)

default_registry.register(
    EvalScenario(
        scenario_id="dc-003",
        name="Base64 encoded log file in description",
        description="User pasted base64-encoded log output thinking it would help diagnose "
        "their authentication issue.",
        category=_CATEGORY,
        tags=["base64", "log_data", "noise"],
        ticket=EvalTicket(
            ticket_id="INC-5003",
            subject="SSO login failure - log file attached",
            description=(
                "I can't log into Salesforce via SSO. The IT portal told me to grab logs so here they are:\n\n"
                f"--- BEGIN LOG (base64) ---\n{_B64_LOG}\n--- END LOG ---\n\n"
                "This has been happening since 9am. I have client calls starting at 10 and I need "
                "Salesforce access. I'm on my company laptop, Windows 11, Chrome 122."
            ),
            reporter=_reporter("Lisa Wong", "l.wong@contoso.com", "Wealth Management"),
            created_at="2026-03-18T09:20:00Z",
            channel="portal",
        ),
        expected_triage=ExpectedTriage(
            category="Access & Authentication",
            priority="P2",
            assigned_team="Identity & Access Management",
        ),
    )
)


# ---------------------------------------------------------------------------
# dc-004: HTML markup email body
# ---------------------------------------------------------------------------
default_registry.register(
    EvalScenario(
        scenario_id="dc-004",
        name="HTML markup in email body",
        description="Email submitted with full HTML markup including styles, tables, and images.",
        category=_CATEGORY,
        tags=["html", "markup", "noise"],
        ticket=EvalTicket(
            ticket_id="INC-5004",
            subject="Printer not working on 5th floor",
            description=(
                '<html><head><style>body{font-family:Calibri,sans-serif;font-size:11pt;}'
                ".sig{color:#666;font-size:9pt;}</style></head><body>"
                "<p>Hi IT team,</p>"
                "<p>The <b>HP LaserJet Pro</b> on the <b>5th floor</b> (near the kitchen) has been "
                "showing a <span style='color:red;font-weight:bold'>PC LOAD LETTER</span> error since "
                "this morning. I&rsquo;ve tried power cycling it twice. The paper tray is full and "
                "I checked for jams &mdash; nothing stuck.</p>"
                "<p>Can someone take a look? We have a board presentation to print at 2pm.</p>"
                '<table border="1" cellpadding="4"><tr><th>Printer</th><th>Location</th><th>Asset Tag</th></tr>'
                "<tr><td>HP LaserJet Pro M404dn</td><td>5F Kitchen Area</td><td>CT-PR-10234</td></tr></table>"
                '<p class="sig">Thanks,<br/>Rachel Green<br/>Executive Operations<br/>'
                "Contoso Financial Services<br/>"
                '<img src="https://contoso.com/email-sig-logo.png" width="150"/></p>'
                "</body></html>"
            ),
            reporter=_reporter("Rachel Green", "r.green@contoso.com", "Executive Operations"),
            created_at="2026-03-18T10:30:00Z",
            channel="email",
        ),
        expected_triage=ExpectedTriage(
            category="Hardware & Peripherals",
            priority="P3",
            assigned_team="Endpoint Engineering",
        ),
    )
)


# ---------------------------------------------------------------------------
# dc-005: Unicode zero-width characters
# ---------------------------------------------------------------------------
default_registry.register(
    EvalScenario(
        scenario_id="dc-005",
        name="Unicode zero-width characters throughout text",
        description="Ticket text peppered with zero-width spaces and joiners, as if copy-pasted "
        "from a formatted document or web page.",
        category=_CATEGORY,
        tags=["unicode", "zero_width", "noise"],
        ticket=EvalTicket(
            ticket_id="INC-5005",
            subject="Can\u200bt\u200b log\u200b in\u200b to\u200b email",
            description=(
                "I\u200b can\u200bt\u200b access\u200b my\u200b Outlook\u200b email.\u200b "
                "It\u200b keeps\u200b saying\u200b 'Your\u200b session\u200b has\u200b expired.\u200b "
                "Please\u200b sign\u200b in\u200b again.'\u200b every\u200b time\u200b I\u200b try.\u200b "
                "This\u200b started\u200b after\u200b the\u200b password\u200b change\u200b I\u200b "
                "did\u200b yesterday.\u200b I\u200bve\u200b tried\u200b clearing\u200b browser\u200b "
                "cache\u200b and\u200b using\u200b incognito\u200b mode.\u200b Still\u200b broken.\u200b\u200b"
                "\n\nI\u200b need\u200b this\u200b fixed\u200b ASAP\u200b -\u200b I\u200b have\u200b "
                "a\u200b compliance\u200b deadline\u200b tomorrow."
            ),
            reporter=_reporter("David Park", "d.park@contoso.com", "Compliance"),
            created_at="2026-03-18T11:00:00Z",
            channel="portal",
        ),
        expected_triage=ExpectedTriage(
            category="Access & Authentication",
            priority="P2",
            assigned_team="Identity & Access Management",
        ),
    )
)


# ---------------------------------------------------------------------------
# dc-006: Garbled encoding / mojibake
# ---------------------------------------------------------------------------
default_registry.register(
    EvalScenario(
        scenario_id="dc-006",
        name="Garbled encoding / mojibake",
        description="Ticket with encoding corruption (mojibake) mixed with readable text. "
        "Common when emails pass through legacy mail gateways.",
        category=_CATEGORY,
        tags=["encoding", "mojibake", "noise"],
        ticket=EvalTicket(
            ticket_id="INC-5006",
            subject="Can\u00e2\u0080\u0099t access shared drive \u00e2\u0080\u0093 permission denied",
            description=(
                "Hi,\n\n"
                "I\u00e2\u0080\u0099m getting a \u00e2\u0080\u0098Permission Denied\u00e2\u0080\u0099"
                " error when trying to access "
                "the \\\\contoso-fs01\\finance share. This worked fine until yesterday. "
                "I need the Q1 \u00e2\u0080\u009cEarnings Report\u00e2\u0080\u009d folder"
                " for the board meeting.\n\n"
                "Error: \u00e2\u0080\u009cAccess is denied. Contact your system administrator."
                "\u00e2\u0080\u009d\n\n"
                "I\u00e2\u0080\u0099ve tried mapping the drive again and got the same error. "
                "My colleague Jenn can still access it so it\u00e2\u0080\u0099s not a server issue."
                "\n\n"
                "Thanks,\nAlex Kova\u00c4\u008d\n"
                "Finance Department"
            ),
            reporter=_reporter("Alex Kova\u010d", "a.kovac@contoso.com", "Finance"),
            created_at="2026-03-18T13:15:00Z",
            channel="email",
        ),
        expected_triage=ExpectedTriage(
            category="Data & Storage",
            priority="P2",
            assigned_team="Data Platform",
        ),
    )
)


# ---------------------------------------------------------------------------
# dc-007: CSV / log data pasted into description
# ---------------------------------------------------------------------------
default_registry.register(
    EvalScenario(
        scenario_id="dc-007",
        name="CSV / log data pasted into description",
        description="User pasted raw application log lines and CSV data into the ticket body.",
        category=_CATEGORY,
        tags=["log_data", "csv", "noise"],
        ticket=EvalTicket(
            ticket_id="INC-5007",
            subject="Nightly ETL job failing since Tuesday",
            description=(
                "The nightly ETL pipeline has been failing every night since Tuesday. "
                "Here are the last few lines from the log:\n\n"
                "2026-03-15 02:00:01 [INFO] Starting ETL pipeline: finance_daily_load\n"
                "2026-03-15 02:00:02 [INFO] Connecting to source: sql-prod-finance-01.database.windows.net\n"
                "2026-03-15 02:00:03 [INFO] Authenticated via SPN: spn-etl-finance@contoso.com\n"
                "2026-03-15 02:00:15 [INFO] Extracting: dbo.transactions (est. 2.4M rows)\n"
                "2026-03-15 02:15:42 [ERROR] ADLS write failed: HTTP 403 Forbidden\n"
                "2026-03-15 02:15:42 [ERROR] Target: abfss://finance@contosodatalake.dfs.core.windows.net/raw/\n"
                "2026-03-15 02:15:42 [ERROR] Details: AuthorizationPermissionMismatch - "
                "The request is not authorized to perform this operation using this permission.\n"
                "2026-03-15 02:15:43 [ERROR] SPN ObjectId: a8f3c2e1-4b5d-4f6a-8c9d-0e1f2a3b4c5d\n"
                "2026-03-15 02:15:43 [WARN] Retry 1/3 in 30s...\n"
                "2026-03-15 02:16:13 [ERROR] ADLS write failed: HTTP 403 Forbidden\n"
                "2026-03-15 02:16:43 [ERROR] ADLS write failed: HTTP 403 Forbidden\n"
                "2026-03-15 02:16:44 [FATAL] Pipeline finance_daily_load FAILED after 3 retries\n\n"
                "timestamp,pipeline,status,duration_s,rows_processed,error_code\n"
                "2026-03-12,finance_daily_load,SUCCESS,945,2412847,\n"
                "2026-03-13,finance_daily_load,SUCCESS,1023,2398103,\n"
                "2026-03-14,finance_daily_load,SUCCESS,998,2405291,\n"
                "2026-03-15,finance_daily_load,FAILED,943,0,HTTP_403\n"
                "2026-03-16,finance_daily_load,FAILED,12,0,HTTP_403\n"
                "2026-03-17,finance_daily_load,FAILED,11,0,HTTP_403\n\n"
                "Looks like a permission issue on the data lake. The SPN permissions "
                "might have been changed during the weekend maintenance."
            ),
            reporter=_reporter("Tom Chen", "t.chen@contoso.com", "Data Engineering"),
            created_at="2026-03-18T07:30:00Z",
            channel="portal",
        ),
        expected_triage=ExpectedTriage(
            category="Data & Storage",
            priority="P2",
            assigned_team="Data Platform",
            needs_escalation=False,
        ),
    )
)


# ---------------------------------------------------------------------------
# dc-008: Excessive emoji and special characters
# ---------------------------------------------------------------------------
default_registry.register(
    EvalScenario(
        scenario_id="dc-008",
        name="Excessive emoji and special characters",
        description="Ticket from chat channel with heavy emoji use and informal language.",
        category=_CATEGORY,
        tags=["emoji", "special_chars", "chat"],
        ticket=EvalTicket(
            ticket_id="INC-5008",
            subject="🚨🚨🚨 HELP laptop broken 🚨🚨🚨",
            description=(
                "omgggg 😭😭😭 my laptop just died!!! 💀💀💀\n\n"
                "i was in the middle of a presentation 🎤📊 and the screen went black 🖥️⬛ "
                "then it started making this weird buzzing noise 🔊😱\n\n"
                "ive tried holding the power button ⏻ but nothing happens 😤😤\n"
                "the charging light is blinking orange 🟠🟠🟠 which ive never seen before\n\n"
                "this is a BRAND NEW thinkpad 💻 i just got it last month!!! 😡\n"
                "i have a client meeting in 30 min ⏰ and ALL my files are on this thing 📁📁📁\n\n"
                "plsssss someone help asap 🙏🙏🙏🙏🙏\n\n"
                "★★★ URGENT ★★★"
            ),
            reporter=_reporter("Jordan Kim", "j.kim@contoso.com", "Marketing"),
            created_at="2026-03-18T14:20:00Z",
            channel="chat",
        ),
        expected_triage=ExpectedTriage(
            category="Hardware & Peripherals",
            priority="P2",
            assigned_team="Endpoint Engineering",
        ),
    )
)


# ---------------------------------------------------------------------------
# dc-009: Repeated/duplicate content
# ---------------------------------------------------------------------------
_REPEAT_BLOCK = (
    "The printer on the 3rd floor next to the accounting department is not working. "
    "It shows 'offline' in the print queue but the printer itself seems to be powered on. "
    "I have checked the network cable and it is connected. "
)

default_registry.register(
    EvalScenario(
        scenario_id="dc-009",
        name="Repeated / duplicate content",
        description="Same paragraph pasted multiple times, likely a copy-paste error.",
        category=_CATEGORY,
        tags=["duplicate", "noise"],
        ticket=EvalTicket(
            ticket_id="INC-5009",
            subject="3rd floor printer offline",
            description=(_REPEAT_BLOCK * 8) + "\nPlease fix, thanks.",
            reporter=_reporter("Linda Martinez", "l.martinez@contoso.com", "Accounting"),
            created_at="2026-03-18T09:45:00Z",
            channel="email",
        ),
        expected_triage=ExpectedTriage(
            category="Hardware & Peripherals",
            priority="P3",
            assigned_team="Endpoint Engineering",
        ),
    )
)


# ---------------------------------------------------------------------------
# dc-010: Auto-generated system notification (not a real ticket)
# ---------------------------------------------------------------------------
default_registry.register(
    EvalScenario(
        scenario_id="dc-010",
        name="Auto-generated system notification",
        description="Automated monitoring alert that ended up in the ticket queue. "
        "Not a human-submitted support request.",
        category=_CATEGORY,
        tags=["auto_generated", "noise", "not_support"],
        ticket=EvalTicket(
            ticket_id="INC-5010",
            subject="[AUTOMATED] System Health Check - PASS",
            description=(
                "=== AUTOMATED SYSTEM HEALTH REPORT ===\n"
                "Generated: 2026-03-18T06:00:00Z\n"
                "Source: monitoring-agent-prod-01\n\n"
                "Status: ALL CHECKS PASSED\n\n"
                "CPU Utilization: 34% (threshold: 85%)\n"
                "Memory Usage: 62% (threshold: 90%)\n"
                "Disk Space: 54% used (threshold: 80%)\n"
                "Network Latency: 12ms (threshold: 100ms)\n"
                "Active Connections: 1,247 (threshold: 5,000)\n"
                "Last Backup: 2026-03-18T04:00:00Z (SUCCESS)\n\n"
                "--- END AUTOMATED REPORT ---\n"
                "This is an automated message. Do not reply."
            ),
            reporter=_reporter("System Monitor", "monitoring@contoso.com", "IT"),
            created_at="2026-03-18T06:00:00Z",
            channel="email",
        ),
        expected_triage=ExpectedTriage(
            category="Not a Support Ticket",
            assigned_team="None",
            needs_escalation=False,
        ),
    )
)


# ---------------------------------------------------------------------------
# dc-011: Stack trace / error dump
# ---------------------------------------------------------------------------
default_registry.register(
    EvalScenario(
        scenario_id="dc-011",
        name="Stack trace pasted as description",
        description="User pasted a .NET stack trace with minimal context.",
        category=_CATEGORY,
        tags=["stack_trace", "noise", "technical"],
        ticket=EvalTicket(
            ticket_id="INC-5011",
            subject="Client portal crashing",
            description=(
                "The client portal keeps crashing. Here's what I see:\n\n"
                "System.NullReferenceException: Object reference not set to an instance of an object.\n"
                "   at Contoso.Portal.Services.ClientAccountService.GetBalance(String accountId) "
                "in D:\\src\\Portal\\Services\\ClientAccountService.cs:line 142\n"
                "   at Contoso.Portal.Controllers.DashboardController.LoadSummary(HttpContext ctx) "
                "in D:\\src\\Portal\\Controllers\\DashboardController.cs:line 87\n"
                "   at Microsoft.AspNetCore.Mvc.Infrastructure.ActionMethodExecutor"
                ".TaskOfIActionResultExecutor.Execute(ActionContext context)\n"
                "   at Microsoft.AspNetCore.Mvc.Infrastructure.ControllerActionInvoker"
                ".InvokeActionMethodAsync()\n"
                "   at Microsoft.AspNetCore.Mvc.Infrastructure.ControllerActionInvoker"
                ".InvokeNextActionFilterAsync()\n"
                "--- End of stack trace from previous location ---\n"
                "   at Microsoft.AspNetCore.Mvc.Infrastructure.ControllerActionInvoker.Rethrow()\n"
                "   at Microsoft.AspNetCore.Mvc.Infrastructure.ControllerActionInvoker.Next()\n\n"
                "This happens for every client who tries to view their account dashboard. "
                "Started about 30 minutes ago."
            ),
            reporter=_reporter("Kevin Park", "k.park@contoso.com", "Engineering"),
            created_at="2026-03-18T14:45:00Z",
            channel="portal",
        ),
        expected_triage=ExpectedTriage(
            category="Software & Applications",
            priority="P1",
            assigned_team="Enterprise Applications",
            needs_escalation=True,
        ),
    )
)


# ---------------------------------------------------------------------------
# dc-012: Mixed languages
# ---------------------------------------------------------------------------
default_registry.register(
    EvalScenario(
        scenario_id="dc-012",
        name="Mixed languages in description",
        description="Ticket from Singapore office mixing English, Mandarin, and Malay.",
        category=_CATEGORY,
        tags=["multilingual", "noise"],
        ticket=EvalTicket(
            ticket_id="INC-5012",
            subject="WiFi问题 - Singapore office very slow",
            description=(
                "Hi IT team,\n\n"
                "WiFi di pejabat Singapore sangat perlahan hari ini. 网速非常慢，几乎不能工作。\n\n"
                "I've tested on my phone and laptop - both are slow. Speed test shows only 2 Mbps "
                "download (biasanya 200+ Mbps). 其他同事也有同样的问题。\n\n"
                "We are on the 'Contoso-Corp-SG' SSID, 12th floor. 已经试过重启电脑了，没有用。\n\n"
                "Tolong selesaikan secepat mungkin, we have video calls with NY office this afternoon.\n\n"
                "谢谢,\nWei Lin Tan"
            ),
            reporter=_reporter("Wei Lin Tan", "w.tan@contoso.com", "Trading"),
            created_at="2026-03-18T02:30:00Z",
            channel="portal",
        ),
        expected_triage=ExpectedTriage(
            category="Network & Connectivity",
            priority="P2",
            assigned_team="Network Operations",
        ),
    )
)


# ---------------------------------------------------------------------------
# dc-013: Extremely terse / minimal info
# ---------------------------------------------------------------------------
default_registry.register(
    EvalScenario(
        scenario_id="dc-013",
        name="Extremely terse ticket",
        description="Minimal information ticket — just a few words.",
        category=_CATEGORY,
        tags=["terse", "minimal", "noise"],
        ticket=EvalTicket(
            ticket_id="INC-5013",
            subject="broken",
            description="laptop screen cracked",
            reporter=_reporter("Pat Wilson", "p.wilson@contoso.com", "HR"),
            created_at="2026-03-18T15:00:00Z",
            channel="chat",
        ),
        expected_triage=ExpectedTriage(
            category="Hardware & Peripherals",
            priority="P3",
            assigned_team="Endpoint Engineering",
        ),
    )
)


# ---------------------------------------------------------------------------
# dc-014: Massive JSON/XML config dump
# ---------------------------------------------------------------------------
default_registry.register(
    EvalScenario(
        scenario_id="dc-014",
        name="Massive JSON config dump",
        description="User pasted their entire application config as JSON into the ticket.",
        category=_CATEGORY,
        tags=["json_dump", "noise", "config"],
        ticket=EvalTicket(
            ticket_id="INC-5014",
            subject="SAP connection error after config change",
            description=(
                "SAP is throwing connection errors after we updated the config. Here's our config:\n\n"
                "```json\n"
                "{\n"
                '  "connectionSettings": {\n'
                '    "sapServer": "sap-prod-01.contoso.com",\n'
                '    "sapPort": 3200,\n'
                '    "sapClient": "100",\n'
                '    "sapSystemNumber": "00",\n'
                '    "sapLanguage": "EN",\n'
                '    "connectionPool": {\n'
                '      "maxConnections": 50,\n'
                '      "minConnections": 5,\n'
                '      "idleTimeout": 300,\n'
                '      "connectionTimeout": 30\n'
                "    },\n"
                '    "retryPolicy": {\n'
                '      "maxRetries": 3,\n'
                '      "backoffMultiplier": 2.0,\n'
                '      "initialDelay": 1000\n'
                "    },\n"
                '    "ssl": {\n'
                '      "enabled": true,\n'
                '      "certPath": "/etc/certs/sap-prod.pem",\n'
                '      "verifyHostname": true\n'
                "    }\n"
                "  },\n"
                '  "logging": {\n'
                '    "level": "DEBUG",\n'
                '    "outputPath": "/var/log/sap-connector/"\n'
                "  },\n"
                '  "features": {\n'
                '    "batchProcessing": true,\n'
                '    "asyncMode": false,\n'
                '    "compressionEnabled": true,\n'
                '    "cacheEnabled": true,\n'
                '    "cacheTTL": 600\n'
                "  }\n"
                "}\n"
                "```\n\n"
                "The error is: 'RFC connection failed: CPIC-CALL: ThSAPCMRCV on connection timeout'. "
                "This started after we changed the connectionTimeout from 60 to 30. "
                "20 users in Finance are unable to process month-end transactions."
            ),
            reporter=_reporter("Anna Svensson", "a.svensson@contoso.com", "Finance"),
            created_at="2026-03-18T16:00:00Z",
            channel="portal",
        ),
        expected_triage=ExpectedTriage(
            category="Software & Applications",
            priority="P1",
            assigned_team="Enterprise Applications",
            needs_escalation=True,
        ),
    )
)


# ---------------------------------------------------------------------------
# dc-015: Embedded URLs and tracking pixels
# ---------------------------------------------------------------------------
default_registry.register(
    EvalScenario(
        scenario_id="dc-015",
        name="Embedded URL spam and tracking pixels",
        description="Email forwarded through multiple systems with tracking URLs and pixel tags.",
        category=_CATEGORY,
        tags=["urls", "tracking", "noise"],
        ticket=EvalTicket(
            ticket_id="INC-5015",
            subject="Fwd: Need access to SharePoint project site",
            description=(
                "---------- Forwarded message ----------\n"
                "From: notifications@sharepoint.contoso.com\n"
                "Date: Mon, 17 Mar 2026\n"
                "Subject: Access Request Denied\n\n"
                'You do not have access to "Project Aurora - Confidential"\n'
                "https://contoso.sharepoint.com/sites/project-aurora\n\n"
                "To request access, contact the site owner.\n\n"
                "[https://contoso.sharepoint.com/_layouts/15/AccessDenied.aspx?"
                "Source=https%3A%2F%2Fcontoso.sharepoint.com%2Fsites%2Fproject-aurora"
                "&Type=list&name=%7B1234-5678-ABCD%7D&ListUrl=]\n\n"
                "---\n\n"
                "I need access to Project Aurora SharePoint site for the due diligence work. "
                "My manager Carlos approved it verbally. Can you grant me access?\n\n"
                "Thanks,\nEmma Thompson\nM&A Team\n\n"
                '<img src="https://tracking.contoso.com/pixel.gif?id=8392&uid=e.thompson" '
                'width="1" height="1" />\n'
                '<img src="https://analytics.office365.com/track?ref=email&cid=29381" '
                'width="1" height="1" />'
            ),
            reporter=_reporter("Emma Thompson", "e.thompson@contoso.com", "M&A"),
            created_at="2026-03-18T10:15:00Z",
            channel="email",
        ),
        expected_triage=ExpectedTriage(
            category="Data & Storage",
            priority="P3",
            assigned_team="Data Platform",
        ),
    )
)


# ---------------------------------------------------------------------------
# dc-016: Excessive email metadata
# ---------------------------------------------------------------------------
default_registry.register(
    EvalScenario(
        scenario_id="dc-016",
        name="Excessive email metadata / headers",
        description="Ticket containing full SMTP headers and routing information.",
        category=_CATEGORY,
        tags=["metadata", "headers", "noise"],
        ticket=EvalTicket(
            ticket_id="INC-5016",
            subject="Re: Re: Re: Certificate expiring soon",
            description=(
                "Return-Path: <alerts@contoso.com>\n"
                "Received: from mail-gw-01.contoso.com (10.0.1.50) by mail-hub-03.contoso.com\n"
                "  with SMTP; Tue, 17 Mar 2026 22:00:01 +0000\n"
                "Received: from monitoring.contoso.com (10.0.5.100) by mail-gw-01.contoso.com\n"
                "  with ESMTPS (TLS1.3); Tue, 17 Mar 2026 22:00:00 +0000\n"
                "DKIM-Signature: v=1; a=rsa-sha256; d=contoso.com; s=selector1;\n"
                "Message-ID: <abc123@monitoring.contoso.com>\n"
                "X-Mailer: Contoso Monitoring Agent v4.2\n"
                "X-Priority: 1\n"
                "Content-Type: text/plain; charset=utf-8\n"
                "Content-Transfer-Encoding: quoted-printable\n\n"
                "--- Actual message starts here ---\n\n"
                "The SSL certificate for api-gateway.contoso.com expires in 72 hours "
                "(2026-03-21T00:00:00Z). This is a production endpoint used by our "
                "client-facing API. If it expires, all external API integrations will break.\n\n"
                "Certificate CN: api-gateway.contoso.com\n"
                "Issuer: DigiCert Global Root G2\n"
                "Serial: 0A:1B:2C:3D:4E:5F\n"
                "Thumbprint: AB12CD34EF56\n\n"
                "Please renew before expiry."
            ),
            reporter=_reporter("System Alerts", "alerts@contoso.com", "IT"),
            created_at="2026-03-18T22:00:00Z",
            channel="email",
        ),
        expected_triage=ExpectedTriage(
            category="Security & Compliance",
            priority="P1",
            assigned_team="Security Operations",
            needs_escalation=True,
        ),
    )
)


# ---------------------------------------------------------------------------
# dc-017: Extremely long signature / legal disclaimers
# ---------------------------------------------------------------------------
_LONG_DISCLAIMER = (
    "IMPORTANT LEGAL NOTICE: This email message, including any attachments, is for the sole use of "
    "the intended recipient(s) and may contain confidential and privileged information. Any unauthorized "
    "review, use, disclosure, or distribution is prohibited. If you are not the intended recipient, "
    "please contact the sender by reply email and destroy all copies of the original message. "
    "This communication does not constitute an offer, acceptance, or agreement of any kind. "
    "Contoso Financial Services Ltd. is authorized and regulated by the Financial Conduct Authority. "
    "Registered in England and Wales No. 12345678. Registered Office: 100 Wall Street, London EC2V 7QE. "
) * 4

default_registry.register(
    EvalScenario(
        scenario_id="dc-017",
        name="Extremely long email signature and disclaimers",
        description="Short IT issue followed by massive legal disclaimer.",
        category=_CATEGORY,
        tags=["signature", "disclaimer", "noise"],
        ticket=EvalTicket(
            ticket_id="INC-5017",
            subject="Monitor flickering",
            description=(
                "My Dell monitor (asset CT-MN-08823) has been flickering intermittently. "
                "It's connected to my docking station via DisplayPort. Started today.\n\n"
                "Thanks,\nRobert Hall\nSenior Vice President | Institutional Trading\n"
                "Contoso Financial Services\n"
                "Direct: +1 (212) 555-0234 | Mobile: +1 (917) 555-0345\n"
                "Email: r.hall@contoso.com\n"
                "100 Wall Street, 30th Floor, New York, NY 10005\n"
                "www.contoso.com | LinkedIn: linkedin.com/in/roberthall\n\n"
                + _LONG_DISCLAIMER
            ),
            reporter=_reporter("Robert Hall", "r.hall@contoso.com", "Trading"),
            created_at="2026-03-18T09:00:00Z",
            channel="email",
        ),
        expected_triage=ExpectedTriage(
            category="Hardware & Peripherals",
            priority="P3",
            assigned_team="Endpoint Engineering",
        ),
    )
)


# ---------------------------------------------------------------------------
# dc-018: Empty description, info only in subject
# ---------------------------------------------------------------------------
default_registry.register(
    EvalScenario(
        scenario_id="dc-018",
        name="Empty description, info only in subject",
        description="Ticket with empty body — all context in subject line only.",
        category=_CATEGORY,
        tags=["terse", "empty_body"],
        ticket=EvalTicket(
            ticket_id="INC-5018",
            subject="URGENT: Production database backup failed - daily job skipped last night",
            description="",
            reporter=_reporter("DBA Team", "dba@contoso.com", "IT"),
            created_at="2026-03-18T07:00:00Z",
            channel="portal",
        ),
        expected_triage=ExpectedTriage(
            category="Data & Storage",
            priority="P1",
            assigned_team="Data Platform",
            needs_escalation=True,
        ),
    )
)


# ---------------------------------------------------------------------------
# dc-019: Tab/newline heavy formatting
# ---------------------------------------------------------------------------
default_registry.register(
    EvalScenario(
        scenario_id="dc-019",
        name="Tab and newline heavy formatting",
        description="Ticket with excessive whitespace, tabs, and newlines from a phone transcript.",
        category=_CATEGORY,
        tags=["whitespace", "formatting", "phone"],
        ticket=EvalTicket(
            ticket_id="INC-5019",
            subject="Phone call — user reporting login issue",
            description=(
                "CALL TRANSCRIPT\n"
                "================\n\n\n"
                "Agent:\t\tHi, how can I help you today?\n\n"
                "Caller:\t\tYeah, um, I can't log in.\n\n\n"
                "Agent:\t\tOkay, what system are you trying to access?\n\n"
                "Caller:\t\tThe... uh... the VPN thing? Global... something?\n\n\n"
                "Agent:\t\tGlobalProtect VPN?\n\n"
                "Caller:\t\tYeah that one. It says my password is wrong\n"
                "\t\t\tbut I just changed it yesterday.\n\n\n\n"
                "Agent:\t\tDid you update the password in the VPN client?\n\n"
                "Caller:\t\tI... don't know? How do I do that?\n\n\n"
                "Agent:\t\tI'll create a ticket for the IAM team.\n\n"
                "\t\t[END OF CALL]\n\n\n\n\n"
            ),
            reporter=_reporter("Call Center", "callcenter@contoso.com", "IT"),
            created_at="2026-03-18T11:30:00Z",
            channel="phone",
        ),
        expected_triage=ExpectedTriage(
            category="Access & Authentication",
            priority="P3",
            assigned_team="Identity & Access Management",
        ),
    )
)


# ---------------------------------------------------------------------------
# dc-020: Base64 garbage data (not valid encoding)
# ---------------------------------------------------------------------------
_B64_GARBAGE = (
    "ZdyO5BoGJkF7XxiitbvuR9sWKu9fwHPGoZx9AbOGlTYZch4BqiGvQSj2HX9DMcDo7EEbNUm+fa3UTfx1+ril"
    "HmPP4BFNuDkU+HWmA2/ZV8Q86aRdOBU5xf2Os592GVR5wK3ptJ+v1iyvRl778bQizJW+QsipFiQRKh5/BwrHU"
    "w1XyrCUbdIkYRyd8qLQAskbf5Tkmmw244CJlACmqc94G1u4ndaeaq/aWnQN5+FpMJn5EXQ6Qmn9rJen9/qzr6"
    "zeNs6W57TTdzxNTTlD0Pa+XvfJZ4n80wVHckK4TBqpAm5ComDTnlHcKzB5o9mhoaQfVdhXPZQPjeq8kp36HSzK"
    "QFOnCLJ++uV885zMu8+awDzG+5bM83qKS38Aw/o05UKEz1MfCbfc8Y3AMEC37ESN+UitvBEBHJAscndAooYXiy"
    "vAlHM93BCecqEQG5CU3Jo0OWNYVzjhYZgWSF/3xVo237YJIVJoGDdPz9morDx3S8s8rsI5RVzQdMWcYsKSOLpb"
    "ysEXCQof2JnNNYcp7t2S2GzkKDDUZje6pNQC7rISxfhZ0CY2M/QzNovHtIm+7167ZOpWtHghEmZPwC+pwgWxkE"
    "cwYsgrrj/QfYlU32vd8WcZXg5yny9AdOz2UXyz5qpXt11tmhqn0+u6GAFnVX9t8jF8x+0="
)

default_registry.register(
    EvalScenario(
        scenario_id="dc-020",
        name="Base64 garbage data mixed with real issue",
        description="Ticket with large blocks of base64 garbage (possibly corrupted attachment) "
        "but with a real security concern in the text.",
        category=_CATEGORY,
        tags=["base64", "garbage", "noise"],
        ticket=EvalTicket(
            ticket_id="INC-5020",
            subject="Suspicious email with attachment - possible phishing",
            description=(
                "I received a suspicious email that looked like it was from our CEO but the "
                "email address was slightly different (ceo@cont0so.com vs contoso.com). "
                "It had an attachment that I accidentally opened. Here's what was in it:\n\n"
                f"{_B64_GARBAGE}\n\n"
                f"{_B64_GARBAGE}\n\n"
                "After opening it my antivirus popped up with a warning but then nothing happened. "
                "I'm worried my machine might be compromised. Should I disconnect from the network?"
            ),
            reporter=_reporter("Nicole Adams", "n.adams@contoso.com", "Finance"),
            created_at="2026-03-18T15:30:00Z",
            channel="email",
        ),
        expected_triage=ExpectedTriage(
            category="Security & Compliance",
            priority="P1",
            assigned_team="Security Operations",
            needs_escalation=True,
        ),
    )
)


# ---------------------------------------------------------------------------
# dc-021: XML/SOAP payload dump
# ---------------------------------------------------------------------------
_SOAP_FAULT_DUMP = (
    '<?xml version="1.0" encoding="UTF-8"?>\n'
    "<soap:Envelope\n"
    '  xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"\n'
    '  xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"\n'
    '  xmlns:xsd="http://www.w3.org/2001/XMLSchema">\n'
    "  <soap:Header>\n"
    "    <wsse:Security\n"
    '      xmlns:wsse="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd">\n'
    "      <wsse:UsernameToken>\n"
    "        <wsse:Username>svc_invoice_proc</wsse:Username>\n"
    "      </wsse:UsernameToken>\n"
    "    </wsse:Security>\n"
    "  </soap:Header>\n"
    "  <soap:Body>\n"
    "    <soap:Fault>\n"
    "      <faultcode>soap:Server</faultcode>\n"
    "      <faultstring>System.NullReferenceException: Object reference not set to an "
    "instance of an object.\n"
    "   at Contoso.Invoice.Service.ProcessInvoiceBatch(InvoiceBatch batch) in "
    "D:\\Build\\src\\InvoiceService\\InvoiceProcessor.cs:line 247\n"
    "   at Contoso.Invoice.Service.InvoiceEndpoint.Submit(SubmitRequest request) in "
    "D:\\Build\\src\\InvoiceService\\Endpoints\\InvoiceEndpoint.cs:line 89\n"
    "   at System.ServiceModel.Dispatcher.SyncMethodInvoker.Invoke(Object instance, "
    "Object[] inputs, Object[]&amp; outputs)\n"
    "   at System.ServiceModel.Dispatcher.DispatchOperationRuntime.InvokeBegin("
    "MessageRpc&amp; rpc)</faultstring>\n"
    "      <detail>\n"
    '        <ErrorInfo xmlns="http://contoso.com/invoice/errors">\n'
    "          <ErrorCode>INV-5001</ErrorCode>\n"
    "          <Timestamp>2026-03-18T11:23:47.882Z</Timestamp>\n"
    "          <CorrelationId>a3f7c291-04be-4e6f-b8a2-91d3e5f7a012</CorrelationId>\n"
    "          <ServiceVersion>4.7.2.1834</ServiceVersion>\n"
    "        </ErrorInfo>\n"
    "      </detail>\n"
    "    </soap:Fault>\n"
    "  </soap:Body>\n"
    "</soap:Envelope>"
)

default_registry.register(
    EvalScenario(
        scenario_id="dc-021",
        name="XML/SOAP payload dump",
        description="Ticket with raw XML/SOAP error output from a web service failure. "
        "The real issue is buried among verbose XML stack traces and SOAP envelopes.",
        category=_CATEGORY,
        tags=["xml", "payload_dump", "noise"],
        ticket=EvalTicket(
            ticket_id="INC-5021",
            subject="Invoice processing web service returning errors since this morning",
            description=(
                "Hi support, our invoice processing integration has been failing all morning "
                "and the finance close deadline is tomorrow. When we submit invoice batches "
                "through the SOAP endpoint the service returns 500 errors. I captured the raw "
                "response below.\n\n"
                f"{_SOAP_FAULT_DUMP}\n\n"
                "We also tried resubmitting the same batch three more times and got "
                "similar responses each time:\n\n"
                f"{_SOAP_FAULT_DUMP}\n\n"
                "This started after the weekend deployment. Batches of 50 or fewer invoices "
                "seem to work but anything over 50 triggers the NullReferenceException. "
                "We have about 1,200 invoices that need to be processed before end of day "
                "Tuesday. Can someone from the applications team look into the "
                "InvoiceProcessor service urgently? The endpoint URL is "
                "https://invoicesvc.contoso.com/v2/submit and we are authenticating with the "
                "svc_invoice_proc service account."
            ),
            reporter=_reporter("David Chen", "d.chen@contoso.com", "Finance"),
            created_at="2026-03-18T11:45:00Z",
            channel="email",
        ),
        expected_triage=ExpectedTriage(
            category="Software & Applications",
            priority="P2",
            assigned_team="Enterprise Applications",
        ),
    )
)


# ---------------------------------------------------------------------------
# dc-022: Screenshot OCR artifacts
# ---------------------------------------------------------------------------
default_registry.register(
    EvalScenario(
        scenario_id="dc-022",
        name="Screenshot OCR artifacts",
        description="Ticket created from OCR of a screenshot with many recognition errors. "
        "The actual issue is a monitor display problem obscured by garbled text.",
        category=_CATEGORY,
        tags=["ocr", "garbled_text", "noise"],
        ticket=EvalTicket(
            ticket_id="INC-5022",
            subject="M0nitor d1splay issue - fl1ckering and c0lor problems",
            description=(
                "Th1s t1cket was cr3ated from a scr33nshot of my m0nitor.\n\n"
                "H3llo IT supp0rt,\n\n"
                "My ext3rnal m0n1tor (D3ll U2723QE) has b33n fl1cker1ng and sh0wing "
                "w31rd c0lor art1facts s1nce y3sterday m0rn1ng. Th3 scr33n g0es p1nk "
                "f0r ab0ut 2-3 s3conds 3very f3w m1nutes, th3n r3turns t0 n0rmal. "
                "S0met1mes th3re ar3 h0r1zontal l1nes acr0ss th3 t0p th1rd 0f th3 "
                "d1splay.\n\n"
                "I'v3 tr13d:\n"
                "- Sw4pp1ng th3 USB-C c4bl3 w1th 4 n3w 0ne fr0m supp1y cl0set\n"
                "- C0nnect1ng v14 HDMI 1nste4d - s4me 1ssue\n"
                "- Us1ng 4 d1fferent p0rt 0n my d0ck1ng st4t10n (L3n0v0 ThunkP4d "
                "USB-C D0ck G3n 2)\n"
                "- Upd4t1ng th3 d1spl4y dr1vers thr0ugh D3v1c3 M4nag3r\n\n"
                "N0ne 0f th3se f1xed 1t. |t's m4k1ng 1t r34lly h4rd t0 d0 my "
                "gr4ph1c d3s1gn w0rk b3c4use th3 c0l0rs 4re unreli4ble. "
                "I'm 0n Fl00r 12, D3sk 12-47B. My l4pt0p 1s 4 L3n0v0 Th1nkP4d X1 "
                "C4rb0n G3n 11 runn1ng W1nd0ws 11 Ent3rpr1se. Th3 m0n1tor w4s "
                "w0rk1ng f1ne unt1l l4st w33k.\n\n"
                "Pl34se s3nd s0me0ne t0 t4ke 4 l00k 0r pr0v1de 4 r3pl4cement "
                "m0n1tor. Th1s 1s urg3nt f0r my pr0ject d34dl1ne."
            ),
            reporter=_reporter("Lisa Park", "l.park@contoso.com", "Marketing"),
            created_at="2026-03-18T10:22:00Z",
            channel="portal",
        ),
        expected_triage=ExpectedTriage(
            category="Hardware & Peripherals",
            priority="P3",
            assigned_team="Endpoint Engineering",
        ),
    )
)


# ---------------------------------------------------------------------------
# dc-023: Automated monitoring alert flood
# ---------------------------------------------------------------------------
_ALERT_TEMPLATE = (
    "=== ALERT: CRITICAL ===\n"
    "Source: AzureMonitor / NetworkWatcher\n"
    "Rule: core-switch-health-check\n"
    "Resource: /subscriptions/9a3f7e12-bc84-4d6f-a321-7e8f9b0c1d2e"
    "/resourceGroups/rg-network-prod/providers/Microsoft.Network"
    "/virtualNetworkGateways/gw-core-east-02\n"
    "Severity: Sev0\n"
    "Condition: Network device gw-core-east-02 is unreachable. "
    "ICMP probe failed for 5 consecutive checks.\n"
    "Metric: DeviceAvailability < 1 for last 5 minutes\n"
    "Fired at: {ts}\n"
    "Affected Region: East US 2\n"
    "Impact: Potential loss of connectivity for subnets 10.42.0.0/16 "
    "and 10.43.0.0/16 (Building 7 and Building 9 campus networks)\n"
    "Runbook: https://runbooks.contoso.com/network/core-switch-failover\n"
    "Action Group: NetworkOps-Critical-OnCall\n"
    "=== END ALERT ===\n"
)

default_registry.register(
    EvalScenario(
        scenario_id="dc-023",
        name="Automated monitoring alert flood",
        description="Ticket containing multiple copy-pasted automated monitoring alerts "
        "for the same underlying network switch failure.",
        category=_CATEGORY,
        tags=["alert_flood", "automated", "noise"],
        ticket=EvalTicket(
            ticket_id="INC-5023",
            subject="CRITICAL: Core network switch gw-core-east-02 down - multiple alerts firing",
            description=(
                "Opening this ticket because our monitoring is going crazy. "
                "gw-core-east-02 appears to be completely down and we are getting "
                "flooded with alerts. Buildings 7 and 9 are reporting total loss of "
                "network connectivity. Here are the alerts we have received so far:\n\n"
                + _ALERT_TEMPLATE.format(ts="2026-03-18T06:02:14Z")
                + "\n"
                + _ALERT_TEMPLATE.format(ts="2026-03-18T06:07:19Z")
                + "\n"
                + _ALERT_TEMPLATE.format(ts="2026-03-18T06:12:22Z")
                + "\n"
                + _ALERT_TEMPLATE.format(ts="2026-03-18T06:17:27Z")
                + "\n"
                + _ALERT_TEMPLATE.format(ts="2026-03-18T06:22:31Z")
                + "\n"
                + _ALERT_TEMPLATE.format(ts="2026-03-18T06:27:35Z")
                + "\n"
                "We have tried remotely rebooting the switch via the out-of-band "
                "management interface but it is not responding either. The redundant "
                "switch gw-core-east-01 has taken over some traffic but is showing "
                "85% CPU utilization and packet loss is climbing. Approximately 400 "
                "users across Buildings 7 and 9 are impacted. We need a network "
                "engineer dispatched to the East data center immediately. This is "
                "a P1 situation as trading floor operations in Building 7 are halted."
            ),
            reporter=_reporter("Marcus Webb", "m.webb@contoso.com", "Infrastructure"),
            created_at="2026-03-18T06:35:00Z",
            channel="email",
        ),
        expected_triage=ExpectedTriage(
            category="Network & Connectivity",
            priority="P1",
            assigned_team="Network Operations",
            needs_escalation=True,
        ),
    )
)


# ---------------------------------------------------------------------------
# dc-024: URL-encoded content
# ---------------------------------------------------------------------------
default_registry.register(
    EvalScenario(
        scenario_id="dc-024",
        name="URL-encoded content in ticket",
        description="Ticket where the description contains URL-encoded strings from a web "
        "form that did not decode properly, mixed with readable text.",
        category=_CATEGORY,
        tags=["url_encoded", "encoding", "noise"],
        ticket=EvalTicket(
            ticket_id="INC-5024",
            subject="Web app form submission error - CRM portal",
            description=(
                "I was trying to submit a new customer record in the CRM portal "
                "(https://crm.contoso.com/customers/new) and after clicking Save the "
                "page showed a raw error. I copied the page content below.\n\n"
                "Error%20Details%3A%0A%0AForm%20submission%20failed%20for%20endpoint"
                "%20%2Fapi%2Fv3%2Fcustomers%0AStatus%3A%20422%20Unprocessable%20Entity"
                "%0ARequest%20ID%3A%20req_8f7a3b21-c4e9-4d12-b5a6-2e1f0c9d8b7a%0A%0A"
                "Validation%20Errors%3A%0A%20%20-%20field%20%22company_name%22%3A%20"
                "value%20exceeds%20maximum%20length%20of%20255%20characters%20%28got%20"
                "312%29%0A%20%20-%20field%20%22billing_address.postal_code%22%3A%20"
                "invalid%20format%20for%20region%20%22US%22%0A%20%20-%20field%20"
                "%22primary_contact.phone%22%3A%20must%20match%20pattern%20%5E%5C%2B"
                "%5B1-9%5D%5Cd%7B1%2C14%7D%24%0A%0ASubmitted%20Payload%3A%0A%7B%22"
                "company_name%22%3A%22Contoso%20International%20Holdings%20Group%20"
                "Limited%20Partnership%20%28formerly%20doing%20business%20as%20Northwind"
                "%20Traders%20Incorporated%20and%20Subsidiaries%29%20-%20Asia%20Pacific"
                "%20Division%20Regional%20Office%20%E2%80%93%20Customer%20Account%22"
                "%2C%22billing_address%22%3A%7B%22postal_code%22%3A%22APAC-2026%22%7D"
                "%2C%22primary_contact%22%3A%7B%22phone%22%3A%22(425)%20555-0199%22%7D"
                "%7D\n\n"
                "I have been trying to enter this customer for three days now. The "
                "company name field won't accept the full legal name of the customer and "
                "I cannot figure out the right phone number format. Our sales team needs "
                "this record created ASAP because we have a contract signing on Thursday. "
                "Also the postal code field rejects non-US formats even though this is "
                "an APAC customer. Could someone look at the field validation rules in "
                "the CRM or increase the character limits?"
            ),
            reporter=_reporter("Rachel Torres", "r.torres@contoso.com", "Sales"),
            created_at="2026-03-19T14:10:00Z",
            channel="portal",
        ),
        expected_triage=ExpectedTriage(
            category="Software & Applications",
            priority="P3",
            assigned_team="Enterprise Applications",
        ),
    )
)


# ---------------------------------------------------------------------------
# dc-025: Massive CC recipient list
# ---------------------------------------------------------------------------
_CC_LIST = "; ".join(
    [
        f"user{i:03d}@contoso.com"
        for i in range(1, 61)
    ]
)

default_registry.register(
    EvalScenario(
        scenario_id="dc-025",
        name="Massive CC recipient list",
        description="Email-channel ticket where a huge CC list dominates the content "
        "before the actual password expiration issue is described.",
        category=_CATEGORY,
        tags=["cc_list", "email_noise", "noise"],
        ticket=EvalTicket(
            ticket_id="INC-5025",
            subject="URGENT: Department-wide password expiration - 200+ users affected",
            description=(
                "From: Patricia Nguyen <p.nguyen@contoso.com>\n"
                "To: IT Help Desk <helpdesk@contoso.com>\n"
                f"CC: {_CC_LIST}\n"
                "Date: Wed, 18 Mar 2026 08:05:00 +0000\n"
                "Subject: URGENT: Department-wide password expiration\n"
                "Importance: High\n\n"
                "--- CC list truncated; 60 of 214 recipients shown above ---\n\n"
                "Hello IT Support,\n\n"
                "This morning approximately 200 employees across the entire HR department "
                "(including Benefits, Recruiting, Payroll, and Employee Relations) were "
                "locked out of their accounts due to simultaneous password expirations. "
                "It appears that when the HR department was migrated to the new Azure AD "
                "organizational unit last quarter, the password policy was set with a "
                "90-day expiration starting from the migration date rather than preserving "
                "each user's original expiration schedule. Since the migration happened "
                "exactly 90 days ago, everyone's password expired at once.\n\n"
                "This is critically impacting our operations: payroll processing for the "
                "March cycle is due by end of day Wednesday, benefits enrollment changes "
                "need to be submitted by Friday, and we have 15 interviews scheduled "
                "today that require access to our applicant tracking system.\n\n"
                "We need either a bulk password reset or a temporary extension of the "
                "password expiration policy for the HR OU. I have CC'd the team leads "
                "from each sub-department so they can confirm impact on their teams.\n\n"
                "Thank you,\nPatricia Nguyen\nHR Operations Director"
            ),
            reporter=_reporter("Patricia Nguyen", "p.nguyen@contoso.com", "HR"),
            created_at="2026-03-18T08:05:00Z",
            channel="email",
        ),
        expected_triage=ExpectedTriage(
            category="Access & Authentication",
            priority="P2",
            assigned_team="Identity & Access Management",
        ),
    )
)


# ---------------------------------------------------------------------------
# dc-026: RTF formatting artifacts
# ---------------------------------------------------------------------------
default_registry.register(
    EvalScenario(
        scenario_id="dc-026",
        name="RTF formatting artifacts",
        description="Ticket with remnants of RTF control words mixed into the actual text "
        "about a corrupted Word document template.",
        category=_CATEGORY,
        tags=["rtf", "formatting", "noise"],
        ticket=EvalTicket(
            ticket_id="INC-5026",
            subject="Word template corrupted - Legal department",
            description=(
                "{\\rtf1\\ansi\\ansicpg1252\\deff0\\nouicompat{\\fonttbl{\\f0\\fswiss"
                "\\fprq2\\fcharset0 Calibri;}{\\f1\\froman\\fprq2\\fcharset0 "
                "Times New Roman;}}\n"
                "{\\colortbl ;\\red0\\green0\\blue0;\\red5\\green99\\blue193;}\n"
                "{\\*\\generator Riched20 10.0.19041}\\viewkind4\\uc1\n"
                "\\pard\\widctlpar\\sa160\\sl252\\slmult1\\f0\\fs22\\lang9\n\n"
                "\\b Hello IT Support,\\b0\\par\n"
                "\\par\n"
                "\\pard\\widctlpar\\fi720\\sa160\\sl252\\slmult1\n"
                "Our standard legal contract template (\\f1 Contoso_Master_Agreement"
                "_v4.2.dotx\\f0 ) has become corrupted and is causing serious problems. "
                "When anyone in the Legal department tries to create a new document from "
                "this template, they get a \\b 'The document template is not valid' "
                "\\b0 error in Word.\\par\n"
                "\\par\n"
                "This template is stored on the SharePoint document library at "
                "\\cf2\\ul https://contoso.sharepoint.com/sites/Legal/Templates"
                "\\cf1\\ulnone  and is used by all 35 attorneys and 20 paralegals in "
                "the department. The template includes custom macros for auto-populating "
                "client information, clause libraries, and formatting standards that are "
                "required for regulatory compliance.\\par\n"
                "\\par\n"
                "The issue started after someone tried to edit the template directly "
                "instead of creating a document from it. We have a backup from two weeks "
                "ago but it is missing the latest clause updates that were added last "
                "Monday. We need someone to either repair the current template or help us "
                "merge the recent clause changes into the backup copy.\\par\n"
                "\\par\n"
                "\\pard\\widctlpar\\sa160\\sl252\\slmult1 This is blocking contract "
                "preparation for three active deals with a combined value over $12M. "
                "Please treat this as high priority.\\par\n"
                "\\par\n"
                "\\b Thank you,\\par\n"
                "Kevin Brooks\\par\n"
                "Senior Paralegal\\b0\\par\n"
                "}"
            ),
            reporter=_reporter("Kevin Brooks", "k.brooks@contoso.com", "Legal"),
            created_at="2026-03-19T09:30:00Z",
            channel="portal",
        ),
        expected_triage=ExpectedTriage(
            category="Software & Applications",
            priority="P3",
            assigned_team="Enterprise Applications",
        ),
    )
)


# ---------------------------------------------------------------------------
# dc-027: Raw CSV/table data dump
# ---------------------------------------------------------------------------
_CSV_ROWS = "timestamp,username,source_ip,action,result,location\n" + "\n".join(
    [
        f"2026-03-{15 + i // 24:02d}T{i % 24:02d}:{(i * 7) % 60:02d}:00Z,"
        f"{'svc_backup' if i % 5 == 0 else 'admin_' + str(i % 4)},"
        f"10.{40 + i % 3}.{i % 256}.{(i * 3) % 256},"
        f"{'file_download' if i % 3 == 0 else 'login' if i % 3 == 1 else 'query'},"
        f"{'success' if i % 7 != 0 else 'failed'},"
        f"{'East US' if i % 2 == 0 else 'West Europe'}"
        for i in range(80)
    ]
)

default_registry.register(
    EvalScenario(
        scenario_id="dc-027",
        name="Raw CSV table data dump",
        description="Ticket with raw CSV data pasted into the description along with a "
        "request to investigate suspicious login patterns in the data.",
        category=_CATEGORY,
        tags=["csv", "table_data", "noise"],
        ticket=EvalTicket(
            ticket_id="INC-5027",
            subject="Suspicious login patterns found in database audit log export",
            description=(
                "Hi Data Platform team,\n\n"
                "I ran an audit log export from our production SQL Server and found some "
                "patterns that concern me. There are logins from the svc_backup service "
                "account at unusual hours and from IP addresses that don't match our "
                "known backup infrastructure. I also see an admin_3 account making "
                "file_download actions that I don't recognize.\n\n"
                "Here is the full export so you can see what I mean:\n\n"
                f"{_CSV_ROWS}\n\n"
                "Specifically I am worried about:\n"
                "1. The svc_backup account logging in from 10.42.x.x addresses - our "
                "backup servers are all on 10.50.x.x\n"
                "2. The admin_3 account - we only have admin_0 through admin_2 in our "
                "records. Who created admin_3?\n"
                "3. The file_download actions from West Europe - we don't have any "
                "infrastructure in that region\n\n"
                "Could someone investigate whether these represent unauthorized access? "
                "If so we may need to involve Security Operations as well. Please review "
                "the data and let me know what you find."
            ),
            reporter=_reporter("Samantha Lee", "s.lee@contoso.com", "Analytics"),
            created_at="2026-03-20T16:40:00Z",
            channel="email",
        ),
        expected_triage=ExpectedTriage(
            category="Data & Storage",
            priority="P3",
            assigned_team="Data Platform",
        ),
    )
)


# ---------------------------------------------------------------------------
# dc-028: Calendar invite iCal metadata
# ---------------------------------------------------------------------------
_ICAL_BLOCK = (
    "BEGIN:VCALENDAR\n"
    "VERSION:2.0\n"
    "PRODID:-//Microsoft Corporation//Outlook 16.0 MIMEDIR//EN\n"
    "METHOD:REQUEST\n"
    "BEGIN:VTIMEZONE\n"
    "TZID:Eastern Standard Time\n"
    "BEGIN:STANDARD\n"
    "DTSTART:16011104T020000\n"
    "RRULE:FREQ=YEARLY;BYDAY=1SU;BYMONTH=11\n"
    "TZOFFSETFROM:-0400\n"
    "TZOFFSETTO:-0500\n"
    "END:STANDARD\n"
    "BEGIN:DAYLIGHT\n"
    "DTSTART:16010311T020000\n"
    "RRULE:FREQ=YEARLY;BYDAY=2SU;BYMONTH=3\n"
    "TZOFFSETFROM:-0500\n"
    "TZOFFSETTO:-0400\n"
    "END:DAYLIGHT\n"
    "END:VTIMEZONE\n"
    "BEGIN:VEVENT\n"
    "ORGANIZER;CN=Jonathan Meyer:mailto:j.meyer@contoso.com\n"
    "ATTENDEE;ROLE=REQ-PARTICIPANT;PARTSTAT=NEEDS-ACTION;RSVP=TRUE;"
    "CN=Board Room A:mailto:boardroom.a@contoso.com\n"
    "ATTENDEE;ROLE=REQ-PARTICIPANT;PARTSTAT=NEEDS-ACTION;RSVP=TRUE;"
    "CN=Emily Crawford:mailto:e.crawford@contoso.com\n"
    "ATTENDEE;ROLE=REQ-PARTICIPANT;PARTSTAT=NEEDS-ACTION;RSVP=TRUE;"
    "CN=Robert Kim:mailto:r.kim@contoso.com\n"
    "ATTENDEE;ROLE=REQ-PARTICIPANT;PARTSTAT=NEEDS-ACTION;RSVP=TRUE;"
    "CN=Diana Patel:mailto:d.patel@contoso.com\n"
    "ATTENDEE;ROLE=OPT-PARTICIPANT;PARTSTAT=NEEDS-ACTION;RSVP=TRUE;"
    "CN=Exec Assistants DL:mailto:exec.assistants@contoso.com\n"
    "DTSTART;TZID=Eastern Standard Time:20260323T090000\n"
    "DTEND;TZID=Eastern Standard Time:20260323T100000\n"
    "RRULE:FREQ=WEEKLY;BYDAY=MO;COUNT=52\n"
    "LOCATION:Board Room A - 25th Floor\n"
    "SUMMARY:Executive Leadership Sync\n"
    "DESCRIPTION:Weekly sync for executive leadership team.\n"
    "UID:040000008200E00074C5B7101A82E00800000000B0A52F30\n"
    "SEQUENCE:3\n"
    "PRIORITY:5\n"
    "CLASS:CONFIDENTIAL\n"
    "STATUS:CONFIRMED\n"
    "TRANSP:OPAQUE\n"
    "X-MICROSOFT-CDO-BUSYSTATUS:BUSY\n"
    "X-MICROSOFT-CDO-INTENDEDSTATUS:BUSY\n"
    "X-MICROSOFT-CDO-IMPORTANCE:1\n"
    "X-MICROSOFT-DISALLOW-COUNTER:FALSE\n"
    "X-MS-OLK-CONFTYPE:0\n"
    "BEGIN:VALARM\n"
    "TRIGGER:-PT15M\n"
    "ACTION:DISPLAY\n"
    "DESCRIPTION:Reminder\n"
    "END:VALARM\n"
    "END:VEVENT\n"
    "END:VCALENDAR"
)

default_registry.register(
    EvalScenario(
        scenario_id="dc-028",
        name="Calendar invite iCal metadata",
        description="Ticket containing forwarded calendar invite data with full iCal "
        "headers mixed with an actual support request about meeting delivery.",
        category=_CATEGORY,
        tags=["ical", "calendar", "noise"],
        ticket=EvalTicket(
            ticket_id="INC-5028",
            subject="Recurring meeting invites not being received by some attendees",
            description=(
                "Hi IT,\n\n"
                "I'm the EA for the CEO and I manage the Executive Leadership Sync "
                "meeting that happens every Monday at 9 AM. For the past three weeks, "
                "two of the four required attendees (Emily Crawford and Robert Kim) have "
                "not been receiving the meeting updates. When I modify the meeting (e.g., "
                "change the conference bridge or add agenda notes), the updates are "
                "delivered to Diana Patel and the Board Room A resource but Emily and "
                "Robert never get them.\n\n"
                "I forwarded the calendar invite to this ticket so you can see the "
                "details. Here is the raw invite data:\n\n"
                f"{_ICAL_BLOCK}\n\n"
                "I have already tried:\n"
                "- Removing Emily and Robert and re-adding them\n"
                "- Creating a brand new meeting series (same problem)\n"
                "- Having Emily check her junk folder (nothing there)\n"
                "- Confirming both Emily and Robert have sufficient mailbox storage\n\n"
                "Both Emily and Robert were recently migrated to Exchange Online from "
                "our on-prem Exchange server. Diana was migrated at the same time and "
                "her invites work fine, so I don't think it's purely a migration issue. "
                "Could someone look into their Exchange transport rules or mailbox "
                "configuration? This is a high-visibility meeting and missing updates "
                "has caused scheduling conflicts twice already."
            ),
            reporter=_reporter("Jonathan Meyer", "j.meyer@contoso.com", "Executive"),
            created_at="2026-03-20T11:15:00Z",
            channel="email",
        ),
        expected_triage=ExpectedTriage(
            category="Software & Applications",
            priority="P3",
            assigned_team="Enterprise Applications",
        ),
    )
)


# ---------------------------------------------------------------------------
# dc-029: Terminal ANSI escape codes
# ---------------------------------------------------------------------------
_ANSI_OUTPUT = (
    "\\033[1;34m===== Deployment Pipeline: prod-release-4.7.3 =====\\033[0m\n"
    "\\033[0;32m[STEP 1/6]\\033[0m Pulling latest images... \\033[0;32mOK\\033[0m\n"
    "\\033[0;32m[STEP 2/6]\\033[0m Running database migrations... \\033[0;32mOK\\033[0m\n"
    "\\033[0;32m[STEP 3/6]\\033[0m Validating configuration... \\033[0;32mOK\\033[0m\n"
    "\\033[0;32m[STEP 4/6]\\033[0m Deploying to canary nodes (3/50)... \\033[0;32mOK\\033[0m\n"
    "\\033[0;33m[STEP 5/6]\\033[0m Rolling out to production fleet...\n"
    "  \\033[0;32m[batch 1/10]\\033[0m nodes prod-web-001 through prod-web-005: "
    "\\033[0;32mhealthy\\033[0m\n"
    "  \\033[0;32m[batch 2/10]\\033[0m nodes prod-web-006 through prod-web-010: "
    "\\033[0;32mhealthy\\033[0m\n"
    "  \\033[0;31m[batch 3/10]\\033[0m nodes prod-web-011 through prod-web-015: "
    "\\033[1;31mFAILED\\033[0m\n"
    "    \\033[0;31mError:\\033[0m Container health check failed on prod-web-012\n"
    "    \\033[0;31mError:\\033[0m Container health check failed on prod-web-013\n"
    "    \\033[0;31mError:\\033[0m OOMKilled: container exceeded 4Gi memory limit on "
    "prod-web-014\n"
    "    \\033[0;33mWarning:\\033[0m Readiness probe timeout on prod-web-011 (retrying...)\n"
    "    \\033[0;31mError:\\033[0m Readiness probe failed after 3 retries on prod-web-011\n"
    "  \\033[1;31m*** ROLLBACK TRIGGERED ***\\033[0m\n"
    "  \\033[0;33m[rollback]\\033[0m Reverting batch 3 to previous image "
    "prod-release-4.7.2... \\033[0;32mOK\\033[0m\n"
    "  \\033[0;33m[rollback]\\033[0m Reverting batch 2 to previous image "
    "prod-release-4.7.2... \\033[0;32mOK\\033[0m\n"
    "  \\033[0;33m[rollback]\\033[0m Reverting batch 1 to previous image "
    "prod-release-4.7.2... \\033[0;32mOK\\033[0m\n"
    "\\033[1;31m[STEP 5/6] FAILED - Automatic rollback completed\\033[0m\n"
    "\\033[0;31m[STEP 6/6]\\033[0m Post-deployment validation... "
    "\\033[1;33mSKIPPED\\033[0m\n"
    "\\033[1;31m===== DEPLOYMENT FAILED =====\\033[0m\n"
    "\\033[0;36mDuration: 14m 32s | Started: 2026-03-19T02:00:00Z | "
    "Ended: 2026-03-19T02:14:32Z\\033[0m\n"
    "\\033[0;36mPipeline ID: deploy-7f3a9b2c | Trigger: scheduled\\033[0m"
)

default_registry.register(
    EvalScenario(
        scenario_id="dc-029",
        name="Terminal ANSI escape codes",
        description="Ticket with terminal output containing ANSI escape codes for colors "
        "and formatting, describing a failed production deployment.",
        category=_CATEGORY,
        tags=["ansi", "terminal", "noise"],
        ticket=EvalTicket(
            ticket_id="INC-5029",
            subject="Production deployment failed overnight - rollback completed but need RCA",
            description=(
                "The scheduled production deployment for release 4.7.3 failed last night "
                "during the rolling update phase. The pipeline automatically rolled back "
                "so we are still on 4.7.2 and users are not impacted right now, but we "
                "need to understand what went wrong before attempting the release again.\n\n"
                "Here is the full pipeline output from our deploy tool:\n\n"
                f"{_ANSI_OUTPUT}\n\n"
                "Key issues from the output:\n"
                "1. Three nodes (prod-web-012, 013, 014) failed container health checks\n"
                "2. prod-web-014 was OOMKilled - the new release may have a memory leak\n"
                "3. prod-web-011 had readiness probe timeouts followed by failure\n\n"
                "I suspect the memory issue is related to the new caching layer that was "
                "added in 4.7.3 - the PR mentioned increasing the default cache size but "
                "the memory limit wasn't updated in the Kubernetes manifests. Can someone "
                "from the applications team review the deployment config and the memory "
                "profile of the 4.7.3 release? We need to get this deployed by end of "
                "week for the client demo on Monday."
            ),
            reporter=_reporter("Alex Romero", "a.romero@contoso.com", "DevOps"),
            created_at="2026-03-19T07:20:00Z",
            channel="chat",
        ),
        expected_triage=ExpectedTriage(
            category="Software & Applications",
            priority="P2",
            assigned_team="Enterprise Applications",
        ),
    )
)


# ---------------------------------------------------------------------------
# dc-030: PGP/S-MIME encrypted email wrapper
# ---------------------------------------------------------------------------
_PGP_BLOCK = (
    "-----BEGIN PGP MESSAGE-----\n"
    "Version: GnuPG v2.3.4 (GNU/Linux)\n"
    "Comment: Contoso Secure Email Gateway\n\n"
    "hQIMA7R9YkKf4WbZAQ//cJ1V8sHDqK5mP3kBvLz9nR2xYhG4TqN+wE6fA3vRmUj\n"
    "K8dL0pFxN7qBtH2yW5sV9cXiO3mAeU0dPjQ6rK1bY4wJnE8hL2fC7xS9gMaD5tR\n"
    "qH0oI3kPuW6eN1bYzA4vGjF8cL0dS9nPxR5mJ3kUfE2wT7iO6qHbN0aYsV1gDcK\n"
    "pM4rL8eJ5nWbI2xA7tF0vR3cYsH9dPkG6mUqE1oN4jS7fW8lT5aDBnC0iKxVgMr\n"
    "uQ2wP6hO9eY3bJ4nL1sF7vK0tA8mRdX5cIgGfE2jW9qUlH3oDpN6aTbYkS0rMiC\n"
    "nX1wV7eL4fJ8gA2mK5qR0tH9sP3bYdO6cUxIiN7jE4lW8aFvT0rS5nMkG2hDpBc\n"
    "QyJ6oU9iL3eW1tA7xP4fS8nR5vK0mHbN2dYgCqE9jO3lU6kF7aTcMsI0wDiG4hV\n"
    "rB1eX5nP8fJ2qL4sW7dA0tK3vRmO6cYgNbH9iU0jE5lS7aTkF8wM2nDpGhCxIiQ\n"
    "oV1eJ4fL8gA3mK6qR0tH9sP4bYdO7cUxIiN8jE5lW9aFvT1rS6nMkG3hDpBcQyJ\n"
    "7oU0iL4eW2tA8xP5fS9nR6vK1mHbN3dYgCqF0jO4lU7kF8aTcMsI1wDiG5hVrB2\n"
    "=Kf7D\n"
    "-----END PGP MESSAGE-----"
)

default_registry.register(
    EvalScenario(
        scenario_id="dc-030",
        name="PGP/S-MIME encrypted email wrapper",
        description="Ticket containing PGP encryption blocks and cleartext describing "
        "email encryption configuration problems.",
        category=_CATEGORY,
        tags=["encrypted", "pgp", "noise"],
        ticket=EvalTicket(
            ticket_id="INC-5030",
            subject="Email encryption not working correctly - recipients cannot decrypt",
            description=(
                "Hi Security team,\n\n"
                "We have been having problems with our PGP email encryption setup for "
                "the past week. When our compliance team sends encrypted emails to "
                "external partners, the recipients report that they cannot decrypt the "
                "messages. I tested this myself by sending an encrypted email to our "
                "partner at Fabrikam and they sent back the raw content they received, "
                "which I am pasting below:\n\n"
                f"{_PGP_BLOCK}\n\n"
                "The Fabrikam team says their PGP client (Kleopatra 3.1.28) reports "
                "'No secret key found' when trying to decrypt, even though we exchanged "
                "public keys last month and encryption was working fine until recently.\n\n"
                "I checked our Contoso Secure Email Gateway logs and noticed that the "
                "gateway was updated to version 5.2.1 on March 12th. I believe the update "
                "may have rotated our organization's PGP keys without notifying external "
                "partners. The old public key fingerprint was 4A2B 8C3D 9E1F 0A5B 7C6D "
                "and the current one appears to be different.\n\n"
                "Additionally, two internal users (compliance@contoso.com and "
                "legal.notices@contoso.com) are also having S/MIME issues - their digital "
                "signatures are showing as invalid to internal recipients. The S/MIME "
                "certificates for these mailboxes may have expired during the gateway "
                "update.\n\n"
                "Can someone from Security Operations review the email gateway "
                "configuration, verify the PGP key distribution, and check the S/MIME "
                "certificate status? We have regulatory deadlines that require encrypted "
                "communication with our partners and this is blocking several active "
                "compliance matters."
            ),
            reporter=_reporter("Theresa Walsh", "t.walsh@contoso.com", "Security"),
            created_at="2026-03-20T13:50:00Z",
            channel="email",
        ),
        expected_triage=ExpectedTriage(
            category="Security & Compliance",
            priority="P2",
            assigned_team="Security Operations",
        ),
    )
)


# ---------------------------------------------------------------------------
# dc-031: Very long email with deeply buried VPN issue
# ---------------------------------------------------------------------------
default_registry.register(
    EvalScenario(
        scenario_id="dc-031",
        name="Very long email with buried VPN issue",
        description="Tests extraction of a VPN auth failure buried in a 10K+ char email thread.",
        category=_CATEGORY,
        tags=["very_long_email", "buried_issue", "forwarded_chain"],
        ticket=EvalTicket(
            ticket_id="INC-5031",
            subject="Re: Re: FW: VPN not connecting after password change — follow-up",
            description=(
                "Hi Help Desk,\n\n"
                "Forwarding this thread AGAIN. My VPN still does not connect after I changed my "
                "password last Friday. I have spoken to three different agents and nobody has "
                "resolved this.\n\n"
                "Thanks,\nDaniel Okafor\nDirector, Institutional Sales\nContoso Financial Services\n"
                "Phone: +1 (212) 555-0273 | Mobile: +1 (917) 555-0184\n"
                "200 Park Avenue, 31st Floor, New York, NY 10166\n\n"
                "CONFIDENTIALITY NOTICE: This e-mail and any files transmitted with it are "
                "confidential and intended solely for the use of the intended recipient.\n\n"
                "--- Forwarded ---\nFrom: Lisa Park\nDate: Wed, 19 Mar 2026 14:22\n\n"
                "Daniel, I checked with Network Ops — they say everything looks fine. Have you "
                "tried clearing your credential cache?\n\n"
                "--- Original ---\nFrom: Daniel Okafor\nDate: Wed, 19 Mar 2026 10:05\n\n"
                "Team — still broken today. I changed my domain password on Friday as required. "
                "GlobalProtect shows 'Authentication Failed — Invalid credentials'. My new "
                "password works for Outlook, SharePoint, and the trading portal.\n\n"
                "Dell Latitude 7440, Windows 11, GlobalProtect 6.2.1, home on Verizon FiOS.\n\n"
                "--- Forwarded ---\nFrom: Help Desk\nDate: Mon, 17 Mar 2026 16:30\n\n"
                "Hi Daniel, ticket INC-4872 created. Try clearing Windows Credential Manager.\n\n"
                "IT Service Desk | Contoso Financial Services\n"
                "200 Park Avenue, New York, NY 10166\n\n"
                "This message scanned by Contoso Antivirus Gateway v4.12.1.\n"
                "Scan ID: AV-20260319-142200-OKAFOR-7893"
            ),
            reporter=_reporter("Daniel Okafor", "daniel.okafor@contoso.com", "Institutional Trading"),
            created_at="2026-03-19T15:00:00Z",
            channel="email",
        ),
        expected_triage=ExpectedTriage(
            category="Network & Connectivity",
            priority="P2",
            assigned_team="Network Operations",
            needs_escalation=False,
        ),
    )
)


# ---------------------------------------------------------------------------
# dc-032: Multiple base64 images flooding the description
# ---------------------------------------------------------------------------
default_registry.register(
    EvalScenario(
        scenario_id="dc-032",
        name="Base64 image flood in monitor issue ticket",
        description="Tests handling of 5+ inline base64 image fragments dwarfing the actual issue.",
        category=_CATEGORY,
        tags=["base64_flood", "multiple_images", "inline_binary"],
        ticket=EvalTicket(
            ticket_id="INC-5032",
            subject="Monitor display glitch — photos inline",
            description=(
                "My external monitor has colored lines across the top. Photos:\n\n"
                "[Photo 1]\ndata:image/png;base64,iVBORw0KGgoAAAANSUhEUgAABAAAAQCYAAD"
                "qcomAAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAALEwAACxMBAJqcGAAAAd0SU1FB9oKFwgM"
                "NC3WkXYAACAASURBVHic7d15fFT1vfx95lsk5nsG0kgCQlhCfsSAoooLohi3bV1adXaam==\n\n"
                "[Photo 2]\ndata:image/jpeg;base64,/9j/4AAQSkZJRgABAQEASABIAAD/2wBDAAgGBgcG"
                "BQgHBwcJCQgKDBQNDAsLDBkSEw8UHRofHh0aHBwgJC4nICIsIxwcKDcpLDAxNDQ0Hyc5PT"
                "gyPC4zNDL2wBDAQkJCQwLDBgNDRgyIRwhMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMj==\n\n"
                "[Photo 3]\ndata:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAKCAYAAACNMs"
                "9AAAAFUlEQVQYV2P8z8BQz0AEYBxVOHIVAvcHBQHzKSECAAAAAElFTkSuQmCCiVBORw0KGg==\n\n"
                "[Photo 4]\ndata:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0"
                "AAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAALEwAACxMBAJqcGAAAAAd0SU1FB9oKFwgMNC3W==\n\n"
                "[Photo 5]\ndata:image/jpeg;base64,/9j/4AAQSkZJRgABAQEASABIAADkBSyluO9K2kbzlh"
                "9UISyz5DwgdKTjYDuns6nYeuGwyQpl1qwx5ie3TmN3iCf5U6chwnBnfJPX6P0D7nREDEUfQ==\n\n"
                "Monitor: Dell U2723QE via USB-C. Singapore, Building 6, 3rd floor. "
                "GPU: Intel Iris Xe. Started after a Windows Update. Tried replugging."
            ),
            reporter=_reporter("Mei-Lin Tan", "mei-lin.tan@contoso.com", "Equity Trading"),
            created_at="2026-03-18T10:15:00Z",
            channel="email",
        ),
        expected_triage=ExpectedTriage(
            category="Hardware & Peripherals",
            priority="P3",
            assigned_team="Endpoint Engineering",
            needs_escalation=False,
        ),
    )
)


# ---------------------------------------------------------------------------
# dc-033: Base64-encoded log data (not an image)
# ---------------------------------------------------------------------------
default_registry.register(
    EvalScenario(
        scenario_id="dc-033",
        name="Base64-encoded error log in crash ticket",
        description="Tests handling of base64-encoded text (error log) rather than image data.",
        category=_CATEGORY,
        tags=["base64_encoded_text", "error_log", "application_crash"],
        ticket=EvalTicket(
            ticket_id="INC-5033",
            subject="Trade recon app crash — encoded log attached",
            description=(
                "Java trade recon app crashes with OutOfMemoryError. Encoded log:\n\n"
                "RVJST1IgMjAyNi0wMy0xOCAwOToxNToyMiBbQXV0aE1vZHVsZV0gRmFpbGVkIHRvIHZhbGlkYXRl"
                "IE1GQSB0b2tlbiBmb3IgdXNlciBzYXJhaC5jaGVuQGNvbnRvc28uY29tLiBUb2tlbiBleHBpcmVkIGF0"
                "IDIwMjYtMDMtMThUMDk6MTA6MDBaLiBSZXRyeSBjb3VudDogMy4gTW9kdWxlOiBBenVyZUFELk1GQS5W"
                "YWxpZGF0b3IuIENvcnJlbGF0aW9uSWQ6IGE4ZjNjMmUxLTRiNWQtNGY2YTb==\n\n"
                "Crashes daily at 09:15 during the overnight US equity batch (~450K records). "
                "Server: srv-trade-recon-01, Windows Server 2022, 16 GB JVM heap."
            ),
            reporter=_reporter("Robert Chen", "robert.chen@contoso.com", "Operations"),
            created_at="2026-03-18T09:30:00Z",
            channel="email",
        ),
        expected_triage=ExpectedTriage(
            category="Software & Applications",
            priority="P2",
            assigned_team="Enterprise Applications",
            needs_escalation=False,
        ),
    )
)


# ---------------------------------------------------------------------------
# dc-034: Giant email signature dwarfing the actual issue
# ---------------------------------------------------------------------------
default_registry.register(
    EvalScenario(
        scenario_id="dc-034",
        name="Giant legal signature dwarfing MFA issue",
        description="Tests extraction of a 2-line MFA issue buried under a massive legal disclaimer.",
        category=_CATEGORY,
        tags=["giant_signature", "legal_disclaimer", "buried_issue"],
        ticket=EvalTicket(
            ticket_id="INC-5034",
            subject="MFA not working",
            description=(
                "Hi, my MFA push notifications stopped working. Authenticator says 'Request "
                "timed out'. Can't log in.\n\n"
                "Raj Patel\nSVP, Wealth Management\nContoso Financial Services\n"
                "Direct: +1 (212) 555-0391 | Mobile: +1 (917) 555-0248\n"
                "200 Park Avenue, 42nd Floor, NY 10166\n\n"
                "IMPORTANT LEGAL DISCLAIMER: This email is sent by Contoso Financial Services. "
                "It may contain confidential information intended solely for the addressee. "
                "If you are not the named addressee, do not disseminate or copy this email. "
                "Email cannot be guaranteed secure or error-free.\n\n"
                "REGULATORY INFORMATION: Authorized and regulated by the FCA (123456). "
                "Registered in England and Wales (12345678). Member of FINRA, SIPC, NFA.\n\n"
                "ENVIRONMENTAL NOTICE: Please consider the environment before printing.\n\n"
                "PRIVACY NOTICE: We process personal data per GDPR, CCPA. See contoso.com/privacy.\n\n"
                "TAX DISCLAIMER: Tax advice herein not intended for avoiding IRS penalties.\n\n"
                "AML NOTICE: Contoso combats money laundering per BSA and USA PATRIOT Act."
            ),
            reporter=_reporter("Raj Patel", "raj.patel@contoso.com", "Wealth Management"),
            created_at="2026-03-18T08:00:00Z",
            channel="email",
        ),
        expected_triage=ExpectedTriage(
            category="Access & Authentication",
            priority="P2",
            assigned_team="Identity & Access Management",
            needs_escalation=False,
        ),
    )
)


# ---------------------------------------------------------------------------
# dc-035: Extremely deep reply chain (15+ levels)
# ---------------------------------------------------------------------------
default_registry.register(
    EvalScenario(
        scenario_id="dc-035",
        name="Deep reply chain — 15 levels of quoting",
        description="Tests extraction of issue from 15+ levels of email quoting.",
        category=_CATEGORY,
        tags=["deep_quoting", "reply_chain", "excessive_nesting"],
        ticket=EvalTicket(
            ticket_id="INC-5035",
            subject="Re: Re: Re: Re: Re: Re: Re: Re: Printer jam Floor 7",
            description=(
                "Update: printer jamming again today. Same tray 2 issue.\n\n"
                "> Kevin Park: Cleared the jam. Let me know if it recurs.\n"
                "> > Janet Kim: Jammed again. Third time today.\n"
                "> > > Kevin: Ordered replacement rollers. ETA Thursday.\n"
                "> > > > Janet: Torn paper stuck near fuser.\n"
                "> > > > > Kevin: Cleaned rollers. 10 test pages OK.\n"
                "> > > > > > Janet: 7 jams today. Floor complaining.\n"
                "> > > > > > > Help Desk: Kevin dispatched.\n"
                "> > > > > > > > Janet: Tray 2, HP LaserJet M609, Floor 7.\n"
                "> > > > > > > > > Janet: Printer jamming. Help.\n"
                "> > > > > > > > > > Auto: Ticket INC-4901 created."
            ),
            reporter=_reporter("Janet Kim", "janet.kim@contoso.com", "Wealth Management"),
            created_at="2026-03-20T09:00:00Z",
            channel="email",
        ),
        expected_triage=ExpectedTriage(
            category="Hardware & Peripherals",
            priority="P3",
            assigned_team="Endpoint Engineering",
            needs_escalation=False,
        ),
    )
)


# ---------------------------------------------------------------------------
# dc-036: Mojibake (garbled encoding) scattered in text
# ---------------------------------------------------------------------------
default_registry.register(
    EvalScenario(
        scenario_id="dc-036",
        name="Mojibake corruption in file share access ticket",
        description="Tests triage despite double-encoded UTF-8 mojibake throughout the text.",
        category=_CATEGORY,
        tags=["mojibake", "encoding_corruption", "scattered_garble"],
        ticket=EvalTicket(
            ticket_id="INC-5036",
            subject="Can\u00e2\u0080\u0099t access shared drive",
            description=(
                "I\u00e2\u0080\u0099m getting a \u00e2\u0080\u009cpermission denied\u00e2\u0080\u009d "
                "error on \\\\fs-london-01\\wealth-mgmt\\reports. Worked fine until yesterday. "
                "Need Q1 portfolio files for a 2 PM meeting.\n\n"
                "Colleague \u00c3\u0089lodie Martin can still access it. London, Building 2. "
                "Login: CONTOSO\\a.williams. ThinkPad T14 Gen 4.\n\n"
                "Folder shows as \u00e2\u0080\u009cQ1_Valu\u00c3\u00a4tion_Rep\u00c3\u00b6rts"
                "\u00e2\u0080\u009d instead of \u00e2\u0080\u009cQ1_Valuation_Reports\u00e2\u0080\u009d."
            ),
            reporter=_reporter("Alicia Williams", "alicia.williams@contoso.com", "Portfolio Management"),
            created_at="2026-03-18T10:30:00Z",
            channel="email",
        ),
        expected_triage=ExpectedTriage(
            category="Data & Storage",
            priority="P3",
            assigned_team="Data Platform",
            needs_escalation=False,
        ),
    )
)


# ---------------------------------------------------------------------------
# dc-037: Massive JSON ARM template pasted inline
# ---------------------------------------------------------------------------
default_registry.register(
    EvalScenario(
        scenario_id="dc-037",
        name="JSON ARM template dump in deployment ticket",
        description="Tests triage with a large ARM template JSON blob obscuring a deployment timeout.",
        category=_CATEGORY,
        tags=["json_config_dump", "inline_config", "deployment_issue"],
        ticket=EvalTicket(
            ticket_id="INC-5037",
            subject="Azure deployment timeout — ARM template included",
            description=(
                "Staging deployment failed. Here is the ARM template:\n\n"
                '{"$schema": "https://schema.management.azure.com/schemas/2019-04-01/'
                'deploymentTemplate.json#", "contentVersion": "1.0.0.0", "parameters": '
                '{"env": {"type": "string"}, "vmSize": {"type": "string", '
                '"defaultValue": "Standard_D4s_v3"}}, "resources": [{"type": '
                '"Microsoft.Network/virtualNetworks", "apiVersion": "2023-05-01"}]}\n\n'
                "Deployment ran 45 min then timed out at VNet creation. "
                "Error: ProvisioningState: TimedOut. Correlation ID: "
                "d8f3c2e1-4b5d-4f6a-8c9d-0e1f2a3b4c5d."
            ),
            reporter=_reporter("Nora Fischer", "nora.fischer@contoso.com", "Cloud Infrastructure"),
            created_at="2026-03-18T14:00:00Z",
            channel="portal",
        ),
        expected_triage=ExpectedTriage(
            category="Software & Applications",
            priority="P2",
            assigned_team="Enterprise Applications",
            needs_escalation=False,
        ),
    )
)


# ---------------------------------------------------------------------------
# dc-038: Mixed language code-switching (EN/ZH/ES)
# ---------------------------------------------------------------------------
default_registry.register(
    EvalScenario(
        scenario_id="dc-038",
        name="Trilingual code-switching in email delay ticket",
        description="Tests triage with English/Chinese/Spanish code-switching throughout.",
        category=_CATEGORY,
        tags=["code_switching", "multilingual", "trilingual"],
        ticket=EvalTicket(
            ticket_id="INC-5038",
            subject="Email delivery delay / \u7535\u5b50\u90ae\u4ef6\u5ef6\u8fdf",
            description=(
                "\u4f60\u597d IT team,\n\n"
                "Email delivery delays of 30-40 min. \u6211\u7684\u90ae\u4ef6\u53d1\u9001"
                "\u540e\u8981\u7b49\u5f88\u4e45. Esto afecta al equipo de Singapore. "
                "Los correos internos tambi\u00e9n lentos.\n\n"
                "\u95ee\u9898\u4ece\u4e0a\u5468\u4e94\u5f00\u59cb. External worse than internal. "
                "\u6211\u4eec\u7528 Outlook 2024 on Win 11.\n\n"
                "\u8c22\u8c22 / Gracias / Thanks,\nWei-Chen Huang"
            ),
            reporter=_reporter("Wei-Chen Huang", "wei-chen.huang@contoso.com", "Institutional Trading"),
            created_at="2026-03-18T11:00:00Z",
            channel="email",
        ),
        expected_triage=ExpectedTriage(
            category="Software & Applications",
            priority="P3",
            assigned_team="Enterprise Applications",
            needs_escalation=False,
        ),
    )
)


# ---------------------------------------------------------------------------
# dc-039: URL spam from newsletter burying a sync issue
# ---------------------------------------------------------------------------
default_registry.register(
    EvalScenario(
        scenario_id="dc-039",
        name="Newsletter URL spam burying sync issue",
        description="Tests extraction of a SharePoint sync issue from a forwarded newsletter.",
        category=_CATEGORY,
        tags=["url_spam", "tracking_urls", "newsletter_noise"],
        ticket=EvalTicket(
            ticket_id="INC-5039",
            subject="FW: SharePoint sync broken + newsletter",
            description=(
                "Hi, my OneDrive sync broke. Red X, 'Sync pending', ~2 GB queued.\n\n"
                "--- Contoso Newsletter ---\n"
                "https://contoso.com/newsletter?utm_source=email&campaign=w12&mkt=NDc2\n"
                "Q1 Preview: https://contoso.com/q1?ref=nl&utm=email&click=x7y8\n"
                "SG Office: https://contoso.com/sg?ref=nl&utm=email&trk=mmm\n"
                "ESG: https://contoso.com/esg?utm=email&campaign=esg\n"
                "Tech: https://contoso.com/tech?utm=email&mkt=token\n"
                "Compliance: https://contoso.com/comp?utm=email&session=Q2\n"
                "Town Hall: https://contoso.com/townhall?utm=email&register=true\n"
                "Wellness: https://contoso.com/wellness?utm=email&signup=true\n"
                "Unsubscribe: https://contoso.com/unsub?id=12345&utm=email\n"
                "--- End ---\n\n"
                "SharePoint: https://contoso.sharepoint.com/sites/wealth-mgmt/Docs "
                "OneDrive version 24.030.0213.0002."
            ),
            reporter=_reporter("Sophia Martinez", "sophia.martinez@contoso.com", "Client Services"),
            created_at="2026-03-18T09:45:00Z",
            channel="email",
        ),
        expected_triage=ExpectedTriage(
            category="Data & Storage",
            priority="P3",
            assigned_team="Data Platform",
            needs_escalation=False,
        ),
    )
)


# ---------------------------------------------------------------------------
# dc-040: Email metadata noise (MIME headers, DKIM, SPF)
# ---------------------------------------------------------------------------
default_registry.register(
    EvalScenario(
        scenario_id="dc-040",
        name="Raw email headers in Teams audio ticket",
        description="Tests triage with raw MIME/DKIM/SPF headers prepended to the actual issue.",
        category=_CATEGORY,
        tags=["email_metadata", "mime_headers", "raw_headers"],
        ticket=EvalTicket(
            ticket_id="INC-5040",
            subject="Teams call quality — choppy audio",
            description=(
                "MIME-Version: 1.0\n"
                "Content-Type: multipart/alternative; boundary=\"----=_Part_12345\"\n"
                "X-Mailer: Microsoft Outlook 16.0.18025.20160\n"
                "X-MS-Exchange-Organization-SCL: 0\n"
                "Authentication-Results: spf=pass; dkim=pass; dmarc=pass\n"
                "Received: from mail-east.contoso.com by mail-hub.contoso.com\n"
                "DKIM-Signature: v=1; a=rsa-sha256; d=contoso.com\n\n"
                "Hi IT,\n\n"
                "Choppy audio on Teams calls for two days. Audio cuts out every few seconds. "
                "Video and screen sharing fine. Colleagues say I sound robotic.\n\n"
                "London, Building 2, 8th floor. Jabra Evolve2 75 via USB. "
                "Teams 24053.811.3099. ThinkPad X1 Carbon Gen 11 on Wi-Fi."
            ),
            reporter=_reporter("Akira Morimoto", "akira.morimoto@contoso.com", "Quantitative Analysis"),
            created_at="2026-03-18T11:20:00Z",
            channel="email",
        ),
        expected_triage=ExpectedTriage(
            category="Network & Connectivity",
            priority="P2",
            assigned_team="Network Operations",
            needs_escalation=False,
        ),
    )
)
