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
