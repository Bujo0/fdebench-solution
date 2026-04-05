# Copyright (c) Microsoft. All rights reserved.
"""Data cleanup evaluation scenarios.

These scenarios test the triage API's robustness against noisy, malformed,
or unusual input data commonly found in enterprise IT ticket systems.
Each scenario has a legitimate underlying IT issue that should still be
triageable despite the data quality problems.
"""

from ms.evals_core.framework.models.scenario import EvalReporter
from ms.evals_core.framework.models.scenario import EvalScenario
from ms.evals_core.framework.models.scenario import EvalTicket
from ms.evals_core.framework.models.scenario import ExpectedTriage
from ms.evals_core.framework.models.scenario import ScenarioCategory
from ms.evals_core.framework.scenarios.registry import default_registry

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
    + "\n-- \n"
    + "This message has been scanned by Contoso Email Security.\n" * 5
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
        description="User pasted base64-encoded log output thinking it would help diagnose their authentication issue.",
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
                "<html><head><style>body{font-family:Calibri,sans-serif;font-size:11pt;}"
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
                "www.contoso.com | LinkedIn: linkedin.com/in/roberthall\n\n" + _LONG_DISCLAIMER
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
_CC_LIST = "; ".join([f"user{i:03d}@contoso.com" for i in range(1, 61)])

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
                'Content-Type: multipart/alternative; boundary="----=_Part_12345"\n'
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


# ---------------------------------------------------------------------------
# dc-041: PDF-to-text extraction artifacts
# ---------------------------------------------------------------------------
default_registry.register(
    EvalScenario(
        scenario_id="dc-041",
        name="PDF-to-text extraction artifacts in SAP ticket",
        description="Tests triage when PDF-to-text conversion leaves ligature fragments, "
        "broken columns, and header/footer repetition throughout the description.",
        category=_CATEGORY,
        tags=["pdf_extraction", "ocr_artifacts", "garbled_text"],
        ticket=EvalTicket(
            ticket_id="INC-5041",
            subject="SAP GUI crashes on transaction MB52",
            description=(
                "— Page 1 of 3 — Contoso Financial Services — Conﬁdential —\n\n"
                "Hi IT,\n\n"
                "SAP GUI crashes when I run transaction MB52 (warehouse stock list). "
                "The applica\xadtion freezes for ~30 seconds then throws a DBIF_RSQL_SQL_ERROR "
                "short dump. This aﬀects our end-of-day inventory reconciliation.\n\n"
                "— Page 2 of 3 — Contoso Financial Services — Conﬁdential —\n\n"
                "Error details from ST22:\n"
                "Runtime Errors: DBIF_RSQL_SQL_ERROR\n"
                "Date and Time: 18.03.2026 / 14:32:17\n"
                "ﬁle: /usr/sap/PRD/DVEBMGS00/work/dev_w3\n"
                "Theconnectiontotheunderlyingdatabasewaslost.\n\n"
                "— Page 3 of 3 — Contoso Financial Services — Conﬁdential —\n\n"
                "SAP GUI 8.00 PL4, Windows 11, server: sap-prd-01. "
                "Works ﬁne for smaller queries. Only crashes on MB52 with full plant scope.\n\n"
                "Thanks,\nHiroshi Tanaka\nOperations"
            ),
            reporter=_reporter("Hiroshi Tanaka", "hiroshi.tanaka@contoso.com", "Operations"),
            created_at="2026-03-18T14:32:00Z",
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
# dc-042: OCR'd screenshot with recognition errors
# ---------------------------------------------------------------------------
default_registry.register(
    EvalScenario(
        scenario_id="dc-042",
        name="OCR'd screenshot text with recognition errors",
        description="Tests triage when a user OCR'd a screenshot of a printer error panel, "
        "introducing character substitutions and spacing errors.",
        category=_CATEGORY,
        tags=["ocr_errors", "screenshot_text", "recognition_noise"],
        ticket=EvalTicket(
            ticket_id="INC-5042",
            subject="Printer error — OCR of display panel attached",
            description=(
                "Hi, the printer on Floor 5 is showing an error. I took a photo of the "
                "display and used my phone's OCR to copy the text:\n\n"
                "HP C0l0r LaserJet Enterpr1se MFP M776\n"
                "Err0r: 49.4C.O2 — F1rmware Err0r\n"
                "T0 c0ntinue turn 0ff then 0n\n"
                "lP: 1O.O.5.38 | H0stname: prn-f1r5-O5\n\n"
                "I tried p0wer cycling but the err0r came 8ack after printing ~1O pages. "
                "Tray 2 pu11s paper at an ang1e. This is the 0nly c0lor printer on our "
                "f1oor and we need it for c1ient presentations.\n\n"
                "Thanks,\nAmara Osei\nClient Services, Floor 5"
            ),
            reporter=_reporter("Amara Osei", "amara.osei@contoso.com", "Client Services"),
            created_at="2026-03-18T10:50:00Z",
            channel="portal",
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
# dc-043: PowerPoint clipboard paste artifacts
# ---------------------------------------------------------------------------
default_registry.register(
    EvalScenario(
        scenario_id="dc-043",
        name="Clipboard paste artifacts from PowerPoint in Teams ticket",
        description="Tests triage when the user pasted from a PowerPoint slide, bringing "
        "along bullet markers, layout text, and slide metadata.",
        category=_CATEGORY,
        tags=["clipboard_artifacts", "paste_noise", "formatting_corruption"],
        ticket=EvalTicket(
            ticket_id="INC-5043",
            subject="Teams screen sharing broken since update",
            description=(
                "\uf0a7 Q2 Strategy Review — DRAFT — Slide 14 of 38\n"
                "\uf0a7 Click to edit Master title style\n"
                "\uf0a7 Click to edit Master subtitle style\n\n"
                "Hi IT — sorry about the formatting, I was copying notes from my "
                "presentation and it pasted the slide template too.\n\n"
                "\uf0a7 Issue: Teams screen sharing shows a black screen to attendees "
                "since the app updated to version 24345.1234.3456.7890 last night. "
                "I can see my own screen fine but participants see nothing.\n\n"
                "\uf0a7 Agenda Item 3 — Technology Refresh\n"
                "\uf0a7 [Presenter: J. Rivera]\n\n"
                "Audio and video work. It's only the screen sharing / presentation "
                "mode that's broken. Tried both 'Window' and 'Desktop' sharing. "
                "ThinkPad X1 Carbon Gen 11, Windows 11, dual monitor setup.\n\n"
                "\uf0a7 Appendix — Disclosures — Not for distribution\n\n"
                "Thanks,\nJulia Rivera"
            ),
            reporter=_reporter("Julia Rivera", "julia.rivera@contoso.com", "Strategy"),
            created_at="2026-03-18T09:10:00Z",
            channel="chat",
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
# dc-044: Auto-translated Japanese with artifacts
# ---------------------------------------------------------------------------
default_registry.register(
    EvalScenario(
        scenario_id="dc-044",
        name="Auto-translated Japanese ticket with translation artifacts",
        description="Tests triage when a Japanese ticket was auto-translated with "
        "garbled placeholders, untranslated fragments, and grammar artifacts.",
        category=_CATEGORY,
        tags=["auto_translation", "japanese", "translation_artifacts"],
        ticket=EvalTicket(
            ticket_id="INC-5044",
            subject="[Auto-Translated] VPN connection of problem / VPN\u63a5\u7d9a\u306e\u554f\u984c",
            description=(
                "[This message was automatically translated from Japanese]\n\n"
                "Good morning IT team,\n\n"
                "The VPN is <<\u63a5\u7d9a\u5931\u6557>> disconnection repeatedly making. "
                'Since from Monday of morning, Cisco AnyConnect is "connection has been '
                'unexpectedly lost" the error <<\u30a8\u30e9\u30fc\u30b3\u30fc\u30c9>> GP-4022 '
                "to display doing.\n\n"
                "The Tokyo office <<\u6771\u4eac\u30aa\u30d5\u30a3\u30b9>> of 12th floor "
                "<<12\u968e>> from working I am. The internet connection itself <<\u30a4\u30f3\u30bf"
                "\u30fc\u30cd\u30c3\u30c8\u63a5\u7d9a>> is problem <<\u554f\u984c>> none, "
                "VPN only <<VPN\u306e\u307f>> is failing.\n\n"
                "Computer: ThinkPad T14s, Windows 11\n"
                "AnyConnect version: 5.0.03072\n\n"
                "<<\u3088\u308d\u3057\u304f\u304a\u9858\u3044\u3057\u307e\u3059>>\n"
                "Kenji Watanabe"
            ),
            reporter=_reporter("Kenji Watanabe", "kenji.watanabe@contoso.com", "Equity Research"),
            created_at="2026-03-18T01:30:00Z",
            channel="portal",
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
# dc-045: Voice dictation errors
# ---------------------------------------------------------------------------
default_registry.register(
    EvalScenario(
        scenario_id="dc-045",
        name="Voice dictation transcription errors in password reset",
        description="Tests triage when a ticket was submitted via voice dictation "
        "with numerous speech-to-text misrecognitions and missing punctuation.",
        category=_CATEGORY,
        tags=["voice_dictation", "speech_to_text", "transcription_errors"],
        ticket=EvalTicket(
            ticket_id="INC-5045",
            subject="Password reset needed",
            description=(
                "hey i t this is marcus from the wealth management floor i need a "
                "passed word ree set for my add account because i got locked out this "
                "mourning after entering the wrong passed word tree times my user name "
                "is marcus dot williams at could tow so dot com and im on the forth "
                "floor in the new york office i tried the self sir vis portal but it "
                "says my security questions are wrong witch is weird because i definitely "
                "know my mothers maiden name please help a sap because i have a client "
                "coil at ten thirty and i cant access any think right now also my manager "
                "is tom brennan he can very phi my eye dee if needed thanks"
            ),
            reporter=_reporter("Marcus Williams", "marcus.williams@contoso.com", "Wealth Management"),
            created_at="2026-03-18T09:45:00Z",
            channel="chat",
        ),
        expected_triage=ExpectedTriage(
            category="Access & Authentication",
            priority="P3",
            assigned_team="Identity & Access Management",
            needs_escalation=False,
        ),
    )
)


# ---------------------------------------------------------------------------
# dc-046: SMS/chat ultra-terse shorthand
# ---------------------------------------------------------------------------
default_registry.register(
    EvalScenario(
        scenario_id="dc-046",
        name="Ultra-terse SMS shorthand in access request",
        description="Tests triage of an extremely abbreviated SMS-style message "
        "with texting shorthand, missing vowels, and no punctuation.",
        category=_CATEGORY,
        tags=["sms_shorthand", "abbreviations", "ultra_terse"],
        ticket=EvalTicket(
            ticket_id="INC-5046",
            subject="cant login pls hlp",
            description=(
                "yo IT\n"
                "cnt gt into shrpnt since ths morn. gts err 403 evry time. "
                "nd access 4 the Q1 rpts folder asap, big mtg @ 2pm w/ client. "
                "uname: d.kim. tried clrng cache + diff browser, same thng. "
                "pls fix b4 lunch thx\n"
                "- DK"
            ),
            reporter=_reporter("Daniel Kim", "d.kim@contoso.com", "Sales"),
            created_at="2026-03-18T10:20:00Z",
            channel="chat",
        ),
        expected_triage=ExpectedTriage(
            category="Access & Authentication",
            priority="P3",
            assigned_team="Identity & Access Management",
            needs_escalation=False,
        ),
    )
)


# ---------------------------------------------------------------------------
# dc-047: SQL query result dump in ticket
# ---------------------------------------------------------------------------
default_registry.register(
    EvalScenario(
        scenario_id="dc-047",
        name="SQL query result dump in database connectivity ticket",
        description="Tests triage when a DBA pasted raw SQL query output and error traces "
        "alongside a description of intermittent database connectivity failures.",
        category=_CATEGORY,
        tags=["sql_dump", "query_output", "database_noise"],
        ticket=EvalTicket(
            ticket_id="INC-5047",
            subject="Intermittent DB connection failures — prod cluster",
            description=(
                "Getting intermittent connection drops to the prod PostgreSQL cluster. "
                "Here's what I captured:\n\n"
                "sql> SELECT pid, state, query, wait_event_type FROM pg_stat_activity "
                "WHERE state != 'idle';\n"
                " pid  |  state  |              query              | wait_event_type\n"
                "------+---------+---------------------------------+----------------\n"
                " 4821 | active  | SELECT * FROM trades WHERE ...  | Client\n"
                " 4903 | active  | UPDATE positions SET mark=...   | Lock\n"
                " 5017 | active  | INSERT INTO audit_log (even...  | IO\n"
                " 5102 | active  | VACUUM ANALYZE risk_metrics     | IO\n"
                " 5234 | idle in | BEGIN; SELECT portfolio_id,...  | Client\n"
                "(5 rows)\n\n"
                "ERROR: could not connect to server: Connection timed out\n"
                '\tIs the server running on host "prod-db-03.contoso.internal" '
                "(10.2.8.43) and accepting TCP/IP connections on port 5432?\n\n"
                "Happens ~every 15 min, lasts 30-60 sec. Started after the "
                "network maintenance window Saturday night. Cluster: prod-db-01 "
                "through prod-db-04, pgBouncer in front. No disk or CPU alerts."
            ),
            reporter=_reporter("Nikolai Petrov", "nikolai.petrov@contoso.com", "Database Administration"),
            created_at="2026-03-18T07:15:00Z",
            channel="email",
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
# dc-048: Webpack build output pasted inline
# ---------------------------------------------------------------------------
default_registry.register(
    EvalScenario(
        scenario_id="dc-048",
        name="Webpack build output in deployment ticket",
        description="Tests triage when a developer pasted extensive webpack build "
        "output and chunk hashes into a deployment failure ticket.",
        category=_CATEGORY,
        tags=["build_output", "webpack_noise", "deployment_issue"],
        ticket=EvalTicket(
            ticket_id="INC-5048",
            subject="Staging deployment failed — webpack build output",
            description=(
                "Staging deploy pipeline failed at the build step. Webpack output:\n\n"
                "asset main.8a3f2c1d.js 1.42 MiB [emitted] [minimized] (name: main)\n"
                "asset vendor.7b9e4f0a.js 892 KiB [emitted] [minimized] (name: vendor)\n"
                "asset styles.3d2e1f0b.css 234 KiB [emitted] (name: styles)\n"
                "asset runtime.c4d5e6f7.js 12.4 KiB [emitted] (name: runtime)\n"
                "asset images/logo.a1b2c3d4.svg 8.42 KiB [emitted]\n"
                "Entrypoint main [big] 2.34 MiB = runtime.c4d5e6f7.js vendor.7b9e4f0a.js "
                "styles.3d2e1f0b.css main.8a3f2c1d.js\n"
                "orphan modules 1.82 MiB [orphan] 487 modules\n"
                "webpack 5.91.0 compiled with 3 errors in 47832 ms\n\n"
                "ERROR in ./src/components/TradeBlotter.tsx\n"
                "Module build failed: SyntaxError: Unexpected token (line 142)\n\n"
                "ERROR in ./src/api/marketData.ts\n"
                "Module not found: Can't resolve '@contoso/market-feed' in '/app/src/api'\n\n"
                "The '@contoso/market-feed' package was removed from our internal "
                "registry during last week's npm audit cleanup. Deployment to "
                "staging (deploy-stg-04) has been blocked since Friday.\n\n"
                "— Priya Sharma, Platform Engineering"
            ),
            reporter=_reporter("Priya Sharma", "priya.sharma@contoso.com", "Platform Engineering"),
            created_at="2026-03-18T15:00:00Z",
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
# dc-049: macOS crash report with stack traces
# ---------------------------------------------------------------------------
default_registry.register(
    EvalScenario(
        scenario_id="dc-049",
        name="macOS crash report with stack traces in app crash ticket",
        description="Tests triage when a user pasted a full macOS crash report "
        "including thread stacks, binary images, and exception details.",
        category=_CATEGORY,
        tags=["crash_report", "stack_trace", "macos"],
        ticket=EvalTicket(
            ticket_id="INC-5049",
            subject="Bloomberg Terminal app crashes every morning",
            description=(
                "Bloomberg Terminal crashes daily around 08:30 when loading market data. "
                "macOS crash report:\n\n"
                "Process:         BloombergTerminal [48291]\n"
                "Path:            /Applications/Bloomberg/BloombergTerminal.app\n"
                "Identifier:      com.bloomberg.terminal\n"
                "Version:         2026.3.14 (build 14823)\n"
                "Code Type:       ARM-64 (Native)\n"
                "Parent Process:  launchd [1]\n\n"
                "Date/Time:       2026-03-18 08:31:42.817 +0000\n"
                "OS Version:      macOS 15.3 (24D5034f)\n\n"
                "Exception Type:  EXC_BAD_ACCESS (SIGSEGV)\n"
                "Exception Codes: KERN_INVALID_ADDRESS at 0x0000000000000010\n\n"
                "Thread 0 Crashed:\n"
                "0   libsystem_platform.dylib   0x1a0734f28 _platform_memmove + 312\n"
                "1   BloombergTerminal          0x104a2f1c0 MarketDataCache::refresh + 448\n"
                "2   BloombergTerminal          0x104a31240 SessionManager::onOpen + 192\n"
                "3   libdispatch.dylib          0x1a06e4a10 _dispatch_call_block + 32\n\n"
                "Binary Images:\n"
                "0x104800000 - 0x106ffffff BloombergTerminal ARM-64\n"
                "0x1a06e0000 - 0x1a0720fff libdispatch.dylib ARM-64\n\n"
                'MacBook Pro 16" M3 Pro. Happens only at market open. '
                "Reinstalled twice, same crash. Other apps fine."
            ),
            reporter=_reporter("Elena Vasquez", "elena.vasquez@contoso.com", "Equity Trading"),
            created_at="2026-03-18T08:35:00Z",
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
# dc-050: Browser console log dump
# ---------------------------------------------------------------------------
default_registry.register(
    EvalScenario(
        scenario_id="dc-050",
        name="Browser console log dump in authentication failure ticket",
        description="Tests triage when a user dumped browser DevTools console output "
        "full of JavaScript errors, network traces, and CORS warnings.",
        category=_CATEGORY,
        tags=["console_log", "browser_debug", "auth_failure"],
        ticket=EvalTicket(
            ticket_id="INC-5050",
            subject="Can't log in to internal portal — console errors",
            description=(
                "I can't log in to the risk dashboard at https://risk.contoso.com. "
                "Gets stuck on the login redirect. IT told me to open the browser "
                "console so here's what I see:\n\n"
                "[09:14:22.341] Navigating to https://risk.contoso.com/auth/callback\n"
                "[09:14:22.587] GET https://login.contoso.com/oauth2/token 401 (Unauthorized)\n"
                "[09:14:22.589] Access to XMLHttpRequest at 'https://login.contoso.com/oauth2/"
                "token' from origin 'https://risk.contoso.com' has been blocked by CORS policy: "
                "No 'Access-Control-Allow-Origin' header is present.\n"
                "[09:14:22.612] Uncaught (in promise) Error: Token refresh failed\n"
                "    at AuthModule.refreshToken (auth.bundle.js:1423:17)\n"
                "    at async SessionManager.init (session.bundle.js:87:9)\n"
                "[09:14:23.001] [React] Warning: Cannot update during existing state transition\n"
                "[09:14:23.150] POST https://api.contoso.com/graphql 403 (Forbidden)\n"
                "[09:14:23.200] Error: ChunkLoadError: Loading chunk 'vendors-risk' failed.\n\n"
                "Chrome 122.0.6261.112, Windows 11, Contoso VPN connected. "
                "Colleague next to me can log in fine on her machine.\n\n"
                "— Tariq Hassan, Risk Management"
            ),
            reporter=_reporter("Tariq Hassan", "tariq.hassan@contoso.com", "Risk Management"),
            created_at="2026-03-18T09:15:00Z",
            channel="portal",
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
# dc-051: Very long email with 5 forwarded messages and a VPN issue buried at the end
# ---------------------------------------------------------------------------
_FORWARDED_CHAIN_BODY = (
    "From: Angela Rivera <a.rivera@contoso.com>\n"
    "To: IT Help Desk <helpdesk@contoso.com>\n"
    "Date: Tue, 18 Mar 2026 10:05:00 +0000\n"
    "Subject: Fwd: Fwd: Fwd: Fwd: Fwd: Network problems\n\n"
    "Help desk — please see the chain below. We've been going back and forth "
    "on this for days and nobody has fixed it yet.\n\n"
    "Thanks,\nAngela Rivera\nSenior Compliance Analyst\n"
    "Contoso Financial Services | Compliance Division\n"
    "Phone: +1 (312) 555-0193 | Mobile: +1 (312) 555-0194\n"
    "angela.rivera@contoso.com\n"
    "200 S. Wacker Drive, Suite 3100, Chicago, IL 60606\n\n"
    "DISCLAIMER: This communication is intended solely for the addressee and may contain "
    "confidential information. If you received this message in error, please delete it and "
    "notify the sender immediately. Unauthorized dissemination is strictly prohibited.\n\n"
    "---------- Forwarded message ----------\n"
    "From: David Park <d.park@contoso.com>\n"
    "Date: Mon, 17 Mar 2026 16:30:00 +0000\n"
    "Subject: Re: Fwd: Fwd: Fwd: Network problems\n\n"
    "Angela, I think this is an IT thing not a facilities thing. Forward to the help desk.\n\n"
    "— David\n\n"
    "---------- Forwarded message ----------\n"
    "From: Karen Liu <k.liu@contoso.com>\n"
    "Date: Mon, 17 Mar 2026 14:12:00 +0000\n"
    "Subject: Re: Fwd: Fwd: Network problems\n\n"
    "David, this isn't a facilities issue. The network drop is happening on the VPN, not "
    "the physical network. Please escalate to IT.\n\n"
    "Best,\nKaren Liu\nFacilities Manager\nContoso Financial Services\n\n"
    "---------- Forwarded message ----------\n"
    "From: David Park <d.park@contoso.com>\n"
    "Date: Mon, 17 Mar 2026 11:45:00 +0000\n"
    "Subject: Re: Fwd: Network problems\n\n"
    "Karen — Angela says her network keeps dying. Can you check the wiring on floor 31? "
    "Maybe it's a loose cable.\n\n"
    "---------- Forwarded message ----------\n"
    "From: Angela Rivera <a.rivera@contoso.com>\n"
    "Date: Mon, 17 Mar 2026 09:20:00 +0000\n"
    "Subject: Fwd: Network problems\n\n"
    "David, can you help route this? My manager said to forward it to you.\n\n"
    "---------- Forwarded message ----------\n"
    "From: Angela Rivera <a.rivera@contoso.com>\n"
    "Date: Fri, 14 Mar 2026 15:40:00 +0000\n"
    "Subject: Network problems\n\n"
    "Hi IT,\n\n"
    "Every afternoon around 3 PM my VPN drops for about 5-10 minutes. I'm remote in Chicago "
    "using GlobalProtect 6.2.1 on a Dell Latitude 5540 running Windows 11 23H2. The VPN client "
    "shows error GP-5012 (gateway timeout) and the connection log says 'tunnel keepalive lost'. "
    "My ISP is Comcast, 200 Mbps down. The issue started after the GlobalProtect update pushed "
    "last Wednesday. Colleagues on the same ISP in Chicago are not affected. I need this fixed "
    "before the SOX audit prep starts Thursday.\n\n"
    "— Angela Rivera"
)

default_registry.register(
    EvalScenario(
        scenario_id="dc-051",
        name="Five-deep forwarded email chain with buried VPN issue",
        description="Tests triage when a VPN connectivity issue is buried at the bottom of "
        "five forwarded messages with signatures, disclaimers, and inter-department chatter.",
        category=_CATEGORY,
        tags=["forwarded_chain", "email_thread", "vpn", "noise"],
        ticket=EvalTicket(
            ticket_id="INC-5051",
            subject="Fwd: Fwd: Fwd: Fwd: Fwd: Network problems",
            description=_FORWARDED_CHAIN_BODY,
            reporter=_reporter("Angela Rivera", "a.rivera@contoso.com", "Compliance"),
            created_at="2026-03-18T10:05:00Z",
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
# dc-052: Base64 image data (1000+ chars) mixed with a printer issue
# ---------------------------------------------------------------------------
_B64_PRINTER_IMAGE = (
    "iVBORw0KGgoAAAANSUhEUgAAAoAAAAHgCAYAAAA10dzkAAAABHNCSVQICAgIfAhkiAAAAAlwSFlz"
    "AAAOxAAADsQBlSsOGwAAABl0RVh0U29mdHdhcmUAcGFpbnQubmV0IDQuMC4xMkMEa+wAADcJ"
    "SURBVHhe7d0HnBTV+f/x7y5lYem9NwEVBRUrVqyxRGNiYkyMxqiJ+jcx0fRiYknUGBOTGBN7"
    "jL1gVyxYsICKIL0Xaauw9P/o+hnPoZcmIXULgZrEhcw4rC/7jSlOZfvEwKqH2rEWsVeqQYomVIK0wCKIzpNeZw4Z/9aGLQZt0x0368hlPH"
    "LnCD3S0wFTIYC8VMO74DEkydzUZa5Os61A1hA7QgjhiGiIYMyG86uITWQWeje9TM74mAmp9soL9H/yg5JKvc6b"
    "Lonvy6NPNrzKhA7gZJcdsssY+srm12era5+UjQwyOOPxndJled52XroGz6XusRq4BhM3PmfBcI6qaedEvFX2jY"
    "s4+V4slyGa7Y4mXfNUfPu9ALwjJcxv8UOAoMs0aoUO/SGUD/rSR5qNYDaCc"
    "xQMlKpT3WYhUVzB4dHr2eF8sA3qPm0jG5CbkyYP8aR7v6zUdkC4FZ0nXGQDkv/YAcF35fTMwh"
    "vOI7Z2IqwTPb9kcccuK3UvE7rxZxCIiIiKiEsDLyomIiIhKGBagRERERCUMC1AiIiKiEoYFKBER"
    "EVEJwwKUiIiIqIRhAUpERERUwrAAJSIiIiphWIASERERlTAsQImIiIhKGBagRERERCUMC1AiIiKi"
    "EoYFKBEREVEJwwKUiIiIqIRhAUpERERUwrAAJSIiIiphWIASERERlTAsQImIiIhKGBagRERERCUM"
    "C1AiIiKiEoYFKBEREVEJwwKUiIiIqIRhAUpERERUwrAAJSIiIiphSvwdkUKhUNy/6aL/p+c6IS"
)

default_registry.register(
    EvalScenario(
        scenario_id="dc-052",
        name="Base64 image blob embedded in printer issue ticket",
        description="Tests triage when a large base64-encoded image (over 1000 characters) "
        "is pasted inline alongside a legitimate printer hardware issue.",
        category=_CATEGORY,
        tags=["base64", "image_blob", "printer", "noise"],
        ticket=EvalTicket(
            ticket_id="INC-5052",
            subject="Floor 12 printer jamming and printing garbled pages — photo attached",
            description=(
                "Hi IT,\n\n"
                "The HP LaserJet Enterprise M609dn on Floor 12 east wing (asset tag PRT-1247) "
                "has been jamming constantly since Monday. Every 3-4 pages it pulls multiple "
                "sheets and produces garbled output — random ASCII characters across the page. "
                "I took a photo of the output, here it is:\n\n"
                f"data:image/png;base64,{_B64_PRINTER_IMAGE}\n\n"
                "The printer displays error code 13.20.00 (paper jam in Tray 2) and the "
                "maintenance counter shows 385,000 pages — well past the 250,000-page fuser "
                "replacement interval. The toner cartridge was replaced last week (CF237A) but "
                "the issue persists. We have 200+ people on this floor relying on this printer "
                "and the only alternative is two floors down. Can someone from endpoint "
                "engineering come take a look or arrange a service call?\n\n"
                "Thanks,\nRobert Chen\nOperations, Floor 12"
            ),
            reporter=_reporter("Robert Chen", "r.chen@contoso.com", "Operations"),
            created_at="2026-03-18T10:30:00Z",
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
# dc-053: HTML table with CSS styles and a legitimate software update request
# ---------------------------------------------------------------------------
_HTML_TABLE_BODY = (
    "Hi team,\n\n"
    "I need the Bloomberg Terminal updated to the latest version on my workstation. "
    "The current version is crashing when loading fixed-income analytics. Below is the "
    "compatibility matrix I pulled from the vendor portal — sorry it pasted weird:\n\n"
    '<table style="border-collapse:collapse;width:100%;font-family:Calibri,sans-serif;">'
    '<thead><tr style="background-color:#1a3e5c;color:#ffffff;font-weight:bold;">'
    '<th style="border:1px solid #2c5f8a;padding:8px 12px;text-align:left;">Component</th>'
    '<th style="border:1px solid #2c5f8a;padding:8px 12px;text-align:left;">Current Version</th>'
    '<th style="border:1px solid #2c5f8a;padding:8px 12px;text-align:left;">Required Version</th>'
    '<th style="border:1px solid #2c5f8a;padding:8px 12px;text-align:left;">Status</th>'
    "</tr></thead><tbody>"
    '<tr style="background-color:#f0f4f8;">'
    '<td style="border:1px solid #d0d8e0;padding:6px 12px;">Bloomberg Terminal</td>'
    '<td style="border:1px solid #d0d8e0;padding:6px 12px;">2025.4.18</td>'
    '<td style="border:1px solid #d0d8e0;padding:6px 12px;">2026.1.12</td>'
    '<td style="border:1px solid #d0d8e0;padding:6px 12px;color:#c0392b;">&#10060; Outdated</td>'
    "</tr>"
    '<tr style="background-color:#ffffff;">'
    '<td style="border:1px solid #d0d8e0;padding:6px 12px;">.NET Runtime</td>'
    '<td style="border:1px solid #d0d8e0;padding:6px 12px;">8.0.2</td>'
    '<td style="border:1px solid #d0d8e0;padding:6px 12px;">8.0.4</td>'
    '<td style="border:1px solid #d0d8e0;padding:6px 12px;color:#c0392b;">&#10060; Outdated</td>'
    "</tr>"
    '<tr style="background-color:#f0f4f8;">'
    '<td style="border:1px solid #d0d8e0;padding:6px 12px;">MSVC Redistributable</td>'
    '<td style="border:1px solid #d0d8e0;padding:6px 12px;">14.38.33130</td>'
    '<td style="border:1px solid #d0d8e0;padding:6px 12px;">14.40.33810</td>'
    '<td style="border:1px solid #d0d8e0;padding:6px 12px;color:#c0392b;">&#10060; Outdated</td>'
    "</tr>"
    '<tr style="background-color:#ffffff;">'
    '<td style="border:1px solid #d0d8e0;padding:6px 12px;">Windows 11</td>'
    '<td style="border:1px solid #d0d8e0;padding:6px 12px;">23H2 (22631.3296)</td>'
    '<td style="border:1px solid #d0d8e0;padding:6px 12px;">23H2 (22631.3447)</td>'
    '<td style="border:1px solid #d0d8e0;padding:6px 12px;color:#27ae60;">&#10004; OK</td>'
    "</tr></tbody></table>\n\n"
    "Machine: WS-FI-0042 (Dell Precision 5820, 64 GB RAM, Xeon W-2245). "
    "The crash happens specifically in the FICC Analytics module with error BT-FICC-4401. "
    "This is blocking my end-of-quarter analysis. Can we get the update scheduled for "
    "today or tomorrow before market close?\n\n"
    "— Naomi Whitfield, Fixed Income Trading"
)

default_registry.register(
    EvalScenario(
        scenario_id="dc-053",
        name="HTML table with inline CSS in software update request",
        description="Tests triage when a user pastes an HTML compatibility matrix with "
        "heavy inline CSS styling alongside a legitimate software update request.",
        category=_CATEGORY,
        tags=["html", "css", "table", "software_update"],
        ticket=EvalTicket(
            ticket_id="INC-5053",
            subject="Bloomberg Terminal update needed — crashing on FICC analytics",
            description=_HTML_TABLE_BODY,
            reporter=_reporter("Naomi Whitfield", "n.whitfield@contoso.com", "Fixed Income Trading"),
            created_at="2026-03-18T11:00:00Z",
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
# dc-054: Mojibake (corrupted encoding) throughout a hardware failure report
# ---------------------------------------------------------------------------
_MOJIBAKE_BODY = (
    "Hi IT support,\n\n"
    "My docking station stopped working this morning. When I plug in my laptop "
    "nothing happens \u00e2\u0080\u0094 no external monitors, no USB devices, no Ethernet. "
    "Here\u00e2\u0080\u0099s what I\u00e2\u0080\u0099ve tried:\n\n"
    "\u00e2\u0080\u00a2 Unplugged and re-plugged the Thunderbolt cable \u00e2\u0080\u0094 no change\n"
    "\u00e2\u0080\u00a2 Tried a different Thunderbolt port on the laptop \u00e2\u0080\u0094 same result\n"
    "\u00e2\u0080\u00a2 Tested with a colleague\u00e2\u0080\u0099s dock \u00e2\u0080\u0094 "
    "my laptop works fine on theirs\n"
    "\u00e2\u0080\u00a2 Tested my dock with colleague\u00e2\u0080\u0099s laptop "
    "\u00e2\u0080\u0094 their laptop doesn\u00e2\u0080\u0099t detect it either\n\n"
    "The dock\u00e2\u0080\u0099s power LED is on but the \u00e2\u0080\u009cconnected\u00e2\u0080\u009d "
    "indicator stays off. Device Manager shows \u00e2\u0080\u009cUnknown USB Device "
    "(Device Descriptor Request Failed)\u00e2\u0080\u009d with error code 43 under "
    "Universal Serial Bus controllers.\n\n"
    "Equipment details:\n"
    "\u00e2\u0080\u00a2 Dock: Lenovo ThinkPad Thunderbolt 4 Dock (40B00135US), "
    "asset tag DCK-3891\n"
    "\u00e2\u0080\u00a2 Laptop: ThinkPad X1 Carbon Gen 11, asset tag LPT-7723\n"
    "\u00e2\u0080\u00a2 Firmware: dock firmware v1.0.48 (latest is 1.0.52 per Lenovo site)\n"
    "\u00e2\u0080\u00a2 OS: Windows 11 23H2\n\n"
    "I\u00e2\u0080\u0099m on Floor 8 in the Risk Analytics area, desk 8-142. "
    "I need this fixed ASAP \u00e2\u0080\u0094 I have two external monitors "
    "I can\u00e2\u0080\u0099t use and I\u00e2\u0080\u0099m running on laptop screen only, "
    "which is making it really hard to work with the multi-panel dashboards.\n\n"
    "Thanks,\nYuki Tanaka\u00e3\u0082\u00ad\nRisk Analytics"
)

default_registry.register(
    EvalScenario(
        scenario_id="dc-054",
        name="Mojibake-corrupted encoding in hardware failure report",
        description="Tests triage when a ticket contains pervasive mojibake (UTF-8 bytes "
        "decoded as Latin-1) corrupting dashes, bullets, and quotes throughout a "
        "legitimate docking station hardware failure report.",
        category=_CATEGORY,
        tags=["mojibake", "encoding", "hardware", "docking_station"],
        ticket=EvalTicket(
            ticket_id="INC-5054",
            subject="Docking station completely dead \u00e2\u0080\u0094 no devices detected",
            description=_MOJIBAKE_BODY,
            reporter=_reporter("Yuki Tanaka", "y.tanaka@contoso.com", "Risk Analytics"),
            created_at="2026-03-18T08:15:00Z",
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
# dc-055: Email with multiple base64 encoded attachments inline in the body
# ---------------------------------------------------------------------------
_B64_ATTACHMENT_1 = (
    "UEsDBBQAAAAIAGRkYVkAAAAA//8AABIAHABDb250b3NvX1ZQTl9Mb2cuZG9jeAEAEAAAAAAA"
    "AAAAABQAAAAAAAAAUEsFBgAAAAABAAEAWAAAAD4AAAAAAA0MjctMDMtMTggMDk6MTI6MzQgW1"
    "ZQTl0gQ29ubmVjdGlvbiB0byBndy1jaGktMDEuY29udG9zby5jb20gZmFpbGVkOiBUTFMgaG"
    "FuZHNoYWtlIHRpbWVvdXQgYWZ0ZXIgMzBzCjIwMjYtMDMtMTggMDk6MTM6MDEgW1ZQTl0g"
    "UmV0cnlpbmcgd2l0aCBndy1jaGktMDIuY29udG9zby5jb20KMjAyNi0wMy0xOCAwOToxMzox"
    "NSBbVlBOXSBDb25uZWN0ZWQgdG8gZ3ctY2hpLTAyLmNvbnRvc28uY29tIChEVExTIDEuMikK"
)

_B64_ATTACHMENT_2 = (
    "UEsDBBQAAAAIAHJkYVkAAAAA//8AABMAHABOZXR3b3JrRGlhZ25vc3RpYy50eHQBABAAAAAAAA"
    "AAABQAAAAAAAAAUEsFBgAAAAABAAEAWQAAAD8AAAAAPHN5c3RlbWluZm8+CkhPU1ROQU1FOiBD"
    "SEktRklOLVdTMDQyClRyYWNlcm91dGUgdG8gZ3ctY2hpLTAxLmNvbnRvc28uY29tOgogIDEg"
    "ICA8MW1zICAgIDEwLjEuMS4xIChHYXRld2F5KQogIDIgICAgMm1zICAgIDE3Mi4xNi4wLjEK"
    "ICAzICAgIDVtcyAgICAxOTIuMTY4LjEwMC4xCiAgNCAgICAqICogKiAoVGltZW91dCkKICA1"
    "ICAgIDQybXMgICAxMC4yNTQuMC4xIChWUE4gR2F0ZXdheSkKUGluZyBndy1jaGktMDE6IDQv"
)

_B64_ATTACHMENT_3 = (
    "UEsDBBQAAAAIAIJkYVkAAAAA//8AABQAHABFdmVudFZpZXdlckV4cG9ydC5ldnR4AQAQAAAA"
    "AAAAAAAUAAAAAAAAAFBLBQYAAAAAAQABAFoAAABAAAAATG9nIE5hbWU6ICAgICAgU3lzdGVtCl"
    "NvdXJjZTogICAgICAgIFJhc0NsaWVudApFdmVudCBJRDogICAgIDIwMjcxCkxldmVsOiAgIC"
    "AgICAgRXJyb3IKRGVzY3JpcHRpb246IENvQ29ubmVjdGlvbkF0dGVtcHRGYWlsZWQgLSBSZW"
    "Fzb246IFRoZSByZW1vdGUgY29ubmVjdGlvbiB3YXMgZGVuaWVkIGJlY2F1c2UgdGhlIHVz"
    "ZXIgbmFtZSBhbmQgcGFzc3dvcmQgY29tYmluYXRpb24geW91IHByb3ZpZGVkIGlzIG5vdA"
)

default_registry.register(
    EvalScenario(
        scenario_id="dc-055",
        name="Multiple base64 attachments inline in VPN connectivity ticket",
        description="Tests triage when a user pastes three separate base64-encoded file "
        "attachments (VPN log, network diagnostic, event viewer export) directly into "
        "the ticket body alongside a VPN connectivity issue.",
        category=_CATEGORY,
        tags=["base64", "attachments", "vpn", "multi_blob"],
        ticket=EvalTicket(
            ticket_id="INC-5055",
            subject="VPN keeps dropping — logs and diagnostics attached inline",
            description=(
                "IT team,\n\n"
                "My VPN connection to the Chicago gateway drops every 15-20 minutes. "
                "I've collected logs and diagnostics. My email client wouldn't let me "
                "attach .evtx files so I'm pasting them base64 encoded:\n\n"
                "=== Attachment 1: VPN Client Log (Contoso_VPN_Log.docx) ===\n"
                f"{_B64_ATTACHMENT_1}\n"
                "=== Attachment 2: Network Diagnostic (NetworkDiagnostic.txt) ===\n"
                f"{_B64_ATTACHMENT_2}\n"
                "=== Attachment 3: Event Viewer Export (EventViewerExport.evtx) ===\n"
                f"{_B64_ATTACHMENT_3}\n\n"
                "The key issue: GlobalProtect 6.2.1 on Windows 11 loses tunnel connectivity "
                "to gw-chi-01.contoso.com every 15-20 minutes. The logs show TLS handshake "
                "timeouts followed by failover to gw-chi-02. After the March 15 maintenance "
                "window, the primary gateway seems to be rejecting DTLS 1.2 sessions. "
                "Error in event viewer is RasClient 20271. Machine is CHI-FIN-WS042, "
                "Dell Latitude 5550. This is impacting real-time trade monitoring.\n\n"
                "— Marcus Webb, Trade Surveillance"
            ),
            reporter=_reporter("Marcus Webb", "m.webb@contoso.com", "Trade Surveillance"),
            created_at="2026-03-18T09:30:00Z",
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
# dc-056: ANSI color codes and terminal escape sequences in a container log dump
# ---------------------------------------------------------------------------
_ANSI_CONTAINER_LOG = (
    "kubectl logs risk-engine-7f8b9c4d5-xk2lm --tail=80 --since=1h\n\n"
    "\x1b[36m2026-03-18T08:00:01.123Z\x1b[0m \x1b[32mINFO \x1b[0m "
    "\x1b[1m[RiskEngine]\x1b[0m Starting risk calculation batch job-2026-0318-0800\n"
    "\x1b[36m2026-03-18T08:00:01.456Z\x1b[0m \x1b[32mINFO \x1b[0m "
    "\x1b[1m[PortfolioLoader]\x1b[0m Loading 14,832 positions from "
    "redis://risk-cache.contoso.internal:6379/db2\n"
    "\x1b[36m2026-03-18T08:00:03.789Z\x1b[0m \x1b[32mINFO \x1b[0m "
    "\x1b[1m[PortfolioLoader]\x1b[0m Loaded 14,832 positions in 2.33s\n"
    "\x1b[36m2026-03-18T08:00:04.012Z\x1b[0m \x1b[33mWARN \x1b[0m "
    "\x1b[1m[MarketDataFeed]\x1b[0m Stale price detected for AAPL "
    "(last update 2026-03-17T20:00:00Z, threshold 12h)\n"
    "\x1b[36m2026-03-18T08:00:04.234Z\x1b[0m \x1b[33mWARN \x1b[0m "
    "\x1b[1m[MarketDataFeed]\x1b[0m Stale price detected for 847 instruments "
    "from feed NYSE-ARCA-RT\n"
    "\x1b[36m2026-03-18T08:00:04.567Z\x1b[0m \x1b[31mERROR\x1b[0m "
    "\x1b[1m[MarketDataFeed]\x1b[0m \x1b[31mConnection refused to "
    "mktdata-nyc.contoso.internal:9092 (Kafka broker)\x1b[0m\n"
    "\x1b[36m2026-03-18T08:00:04.568Z\x1b[0m \x1b[31mERROR\x1b[0m "
    "\x1b[1m[MarketDataFeed]\x1b[0m \x1b[31morg.apache.kafka.common.errors."
    "TimeoutException: Failed to update metadata after 60000 ms.\x1b[0m\n"
    "\x1b[36m2026-03-18T08:00:05.890Z\x1b[0m \x1b[31mERROR\x1b[0m "
    "\x1b[1m[RiskEngine]\x1b[0m \x1b[1;31mFATAL: Risk calculation aborted — "
    "unable to fetch live market data. Positions at risk: 14,832. "
    "VaR calculation deadline: 08:30 UTC.\x1b[0m\n"
    "\x1b[36m2026-03-18T08:00:06.001Z\x1b[0m \x1b[31mERROR\x1b[0m "
    "\x1b[1m[AlertManager]\x1b[0m Sending PagerDuty alert: risk-engine-market-data-failure "
    "(severity: critical)\n"
    "\x1b[36m2026-03-18T08:00:06.123Z\x1b[0m \x1b[32mINFO \x1b[0m "
    "\x1b[1m[HealthCheck]\x1b[0m Pod health: \x1b[31mUNHEALTHY\x1b[0m "
    "(reason: upstream_dependency_failure)\n"
)

default_registry.register(
    EvalScenario(
        scenario_id="dc-056",
        name="ANSI escape codes in container log dump",
        description="Tests triage when a user pastes kubectl container logs containing "
        "ANSI color codes, escape sequences, and terminal formatting throughout. "
        "The underlying issue is a Kafka broker connectivity failure in the risk engine.",
        category=_CATEGORY,
        tags=["ansi_codes", "terminal", "container_logs", "kafka"],
        ticket=EvalTicket(
            ticket_id="INC-5056",
            subject="Risk engine failing — Kafka broker unreachable in prod",
            description=(
                "URGENT: The morning risk calculation batch is failing because the "
                "risk-engine pod can't reach the Kafka market data broker. VaR numbers "
                "are due to the regulators by 09:00 UTC and we're already late. "
                "Here are the pod logs — sorry about the formatting, copied straight "
                "from my terminal:\n\n"
                f"{_ANSI_CONTAINER_LOG}\n"
                "The Kafka broker at mktdata-nyc.contoso.internal:9092 is refusing "
                "connections. The broker was healthy yesterday. Risk cluster is "
                "risk-prod-aks-east in the contoso-risk-prod namespace. "
                "14,832 positions are stuck without live market data and VaR "
                "cannot be computed. This is a regulatory deadline.\n\n"
                "— Sanjay Patel, Quantitative Risk"
            ),
            reporter=_reporter("Sanjay Patel", "s.patel@contoso.com", "Quantitative Risk"),
            created_at="2026-03-18T08:10:00Z",
            channel="chat",
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
# dc-057: XML/SOAP response envelope pasted as the ticket description
# ---------------------------------------------------------------------------
_SOAP_ENVELOPE = (
    '<?xml version="1.0" encoding="UTF-8"?>\n'
    "<soap:Envelope "
    'xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" '
    'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '
    'xmlns:wsse="http://docs.oasis-open.org/wss/2004/01/oasis-200401-wss-wssecurity-secext-1.0.xsd" '
    'xmlns:ctso="http://services.contoso.com/trading/v2">\n'
    "  <soap:Header>\n"
    "    <wsse:Security>\n"
    "      <wsse:UsernameToken>\n"
    "        <wsse:Username>svc-trade-reconciler</wsse:Username>\n"
    "        <wsse:Password>********</wsse:Password>\n"
    "      </wsse:UsernameToken>\n"
    "    </wsse:Security>\n"
    "    <ctso:RequestContext>\n"
    "      <ctso:CorrelationId>a3f8e2c1-7b4d-4e9a-b6c3-8d2f1a5e7c9b</ctso:CorrelationId>\n"
    "      <ctso:Timestamp>2026-03-18T07:45:22.341Z</ctso:Timestamp>\n"
    "      <ctso:SourceSystem>TradeReconciler-v4.2.1</ctso:SourceSystem>\n"
    "    </ctso:RequestContext>\n"
    "  </soap:Header>\n"
    "  <soap:Body>\n"
    "    <soap:Fault>\n"
    "      <faultcode>soap:Server</faultcode>\n"
    "      <faultstring>Service Unavailable: The downstream settlement "
    "service (SETTLE-ENGINE-03) is not responding. Connection pool exhausted "
    "after 120 seconds. Active connections: 200/200. Queued requests: 1,847. "
    "Last successful response: 2026-03-18T06:12:44Z.</faultstring>\n"
    "      <detail>\n"
    "        <ctso:ErrorDetail>\n"
    "          <ctso:ErrorCode>CTSO-SETTLE-5003</ctso:ErrorCode>\n"
    "          <ctso:Severity>CRITICAL</ctso:Severity>\n"
    "          <ctso:AffectedTrades>2,341</ctso:AffectedTrades>\n"
    "          <ctso:SettlementDate>2026-03-18</ctso:SettlementDate>\n"
    '          <ctso:RetryAttempts max="3">3</ctso:RetryAttempts>\n'
    "        </ctso:ErrorDetail>\n"
    "      </detail>\n"
    "    </soap:Fault>\n"
    "  </soap:Body>\n"
    "</soap:Envelope>"
)

default_registry.register(
    EvalScenario(
        scenario_id="dc-057",
        name="SOAP XML fault envelope pasted as ticket body",
        description="Tests triage when a user pastes a full SOAP/XML response envelope "
        "with WS-Security headers, namespaces, and fault details. The underlying issue "
        "is a settlement service outage affecting trade reconciliation.",
        category=_CATEGORY,
        tags=["xml", "soap", "envelope", "settlement_service"],
        ticket=EvalTicket(
            ticket_id="INC-5057",
            subject="Trade reconciliation failing — settlement service down",
            description=(
                "The trade reconciliation batch has been failing since 07:45 UTC. "
                "The SOAP call to the settlement engine returns this fault — I'm pasting "
                "the full response so you can see the error details:\n\n"
                f"{_SOAP_ENVELOPE}\n\n"
                "2,341 trades from yesterday are stuck in 'pending settlement' status. "
                "The settlement engine SETTLE-ENGINE-03 appears to have exhausted its "
                "connection pool. This has downstream impact on T+1 settlement reporting "
                "to the DTCC. The reconciliation service is TradeReconciler-v4.2.1 "
                "running on app-server-chi-04. Please investigate the settlement engine "
                "immediately — we have a regulatory deadline at 11:00 ET.\n\n"
                "— Patricia Okonkwo, Trade Operations"
            ),
            reporter=_reporter("Patricia Okonkwo", "p.okonkwo@contoso.com", "Trade Operations"),
            created_at="2026-03-18T08:00:00Z",
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
# dc-058: Calendar ICS data mixed with a meeting room AV issue
# ---------------------------------------------------------------------------
_ICS_DATA = (
    "BEGIN:VCALENDAR\n"
    "VERSION:2.0\n"
    "PRODID:-//Contoso//Exchange//EN\n"
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
    "DTSTART;TZID=Eastern Standard Time:20260318T140000\n"
    "DTEND;TZID=Eastern Standard Time:20260318T160000\n"
    "SUMMARY:Q1 Board Review — Quarterly Earnings Presentation\n"
    "LOCATION:Boardroom A (Floor 40) [NYC-HQ-40-BOARDROOM-A]\n"
    "ORGANIZER;CN=Catherine Ross:mailto:c.ross@contoso.com\n"
    "ATTENDEE;CN=CEO;ROLE=REQ-PARTICIPANT:mailto:ceo@contoso.com\n"
    "ATTENDEE;CN=CFO;ROLE=REQ-PARTICIPANT:mailto:cfo@contoso.com\n"
    "ATTENDEE;CN=Board Members;ROLE=REQ-PARTICIPANT:mailto:board@contoso.com\n"
    "ATTENDEE;CN=IR Team;ROLE=OPT-PARTICIPANT:mailto:ir-team@contoso.com\n"
    "UID:a1b2c3d4-e5f6-7890-abcd-ef1234567890@contoso.com\n"
    "SEQUENCE:3\n"
    "STATUS:CONFIRMED\n"
    "PRIORITY:1\n"
    "X-MICROSOFT-CDO-IMPORTANCE:2\n"
    "X-MICROSOFT-CDO-BUSYSTATUS:BUSY\n"
    "DESCRIPTION:Q1 2026 earnings review with the board of directors. "
    "Presentation deck and financial summary will be displayed on the main "
    "screen. Video conference bridge for remote board members.\n"
    "END:VEVENT\n"
    "END:VCALENDAR"
)

default_registry.register(
    EvalScenario(
        scenario_id="dc-058",
        name="Calendar ICS data mixed with meeting room AV issue",
        description="Tests triage when a user pastes a full iCalendar (.ics) meeting invite "
        "with timezone rules, attendee lists, and Exchange metadata alongside a "
        "meeting room audio-visual equipment failure report.",
        category=_CATEGORY,
        tags=["ics", "calendar", "av_equipment", "meeting_room"],
        ticket=EvalTicket(
            ticket_id="INC-5058",
            subject="Boardroom A (Floor 40) — projector and video conferencing not working",
            description=(
                "URGENT — The Q1 Board Review meeting is at 2:00 PM today in Boardroom A "
                "on Floor 40 and the AV system is completely down. The Crestron control panel "
                "on the wall shows 'System Offline' and none of the inputs work — no HDMI, "
                "no wireless casting, no video conferencing. The Polycom Studio video bar "
                "has a blinking red LED instead of the normal green. "
                "Here's the meeting invite so you can see the urgency:\n\n"
                f"{_ICS_DATA}\n\n"
                "This is a board of directors meeting with the CEO, CFO, and external board "
                "members dialing in remotely. We have less than 4 hours to fix this. The room "
                "was working yesterday for a dry-run. The Crestron processor is model "
                "CP4N, serial AV-40-001. Polycom Studio is asset tag AV-40-015. "
                "The HDMI matrix switcher (Extron DTP CrossPoint 84) may also be affected. "
                "Can someone from AV support come to Floor 40 immediately?\n\n"
                "— Catherine Ross, Executive Assistant to the CEO"
            ),
            reporter=_reporter("Catherine Ross", "c.ross@contoso.com", "Executive Office"),
            created_at="2026-03-18T10:15:00Z",
            channel="phone",
        ),
        expected_triage=ExpectedTriage(
            category="Hardware & Peripherals",
            priority="P1",
            assigned_team="Endpoint Engineering",
            needs_escalation=True,
        ),
    )
)


# ---------------------------------------------------------------------------
# dc-059: Windows minidump/BSOD output with a driver crash issue
# ---------------------------------------------------------------------------
_BSOD_OUTPUT = (
    "* ******************************************************************************\n"
    "*                                                                              *\n"
    "*                        STOP ERROR (Blue Screen of Death)                     *\n"
    "*                                                                              *\n"
    "* ******************************************************************************\n\n"
    "SYSTEM_THREAD_EXCEPTION_NOT_HANDLED (7e)\n"
    "Bug Check Code:           0x0000007E\n"
    "Parameter 1:              0xFFFFF8024A3B1000\n"
    "Parameter 2:              0xFFFFF80249C72148\n"
    "Parameter 3:              0xFFFFE40137A9E8F0\n"
    "Parameter 4:              0xFFFFE40137A9E100\n\n"
    "FAULTING_MODULE: nt\n"
    "DEFAULT_BUCKET_ID: WIN8_DRIVER_FAULT\n\n"
    "PROCESS_NAME:  System\n"
    "IMAGE_NAME:    nvlddmkm.sys\n"
    "MODULE_NAME:   nvlddmkm\n"
    "IMAGE_VERSION: 32.0.15.6094\n\n"
    "STACK_TEXT:\n"
    "ffffe401`37a9e8f0 fffff802`49c72148 : nt!KeBugCheckEx\n"
    "ffffe401`37a9e8f8 fffff802`49a8b230 : nt!PspSystemThreadStartup+0x58\n"
    "ffffe401`37a9e950 fffff802`4a3b1423 : nvlddmkm!NvDmaEngineChannelSchedule+0x1a3\n"
    "ffffe401`37a9e9b0 fffff802`4a3c8891 : nvlddmkm!NvDmaEngineSubmitCommands+0x451\n"
    "ffffe401`37a9ea20 fffff802`4a2f1c40 : nvlddmkm!NvRmApiAlloc+0x2c1\n"
    "ffffe401`37a9ea90 fffff802`49c35670 : dxgkrnl!DxgkSubmitCommandToHardware+0x340\n"
    "ffffe401`37a9eb00 fffff802`49c10234 : dxgkrnl!DxgkPresentDisplayOnly+0x1f4\n"
    "ffffe401`37a9eb70 fffff802`49b04560 : win32kfull!NtGdiDdDDIPresent+0x234\n\n"
    "FAILURE_BUCKET_ID: 0x7E_nvlddmkm!NvDmaEngineChannelSchedule\n\n"
    "Followup:     MachineOwner\n"
    "Dump file:    C:\\Windows\\MEMORY.DMP\n"
    "Dump written: 18 Mar 2026 07:42:15 UTC\n"
    "System uptime before crash: 0 days 2:14:37.412"
)

default_registry.register(
    EvalScenario(
        scenario_id="dc-059",
        name="Windows BSOD minidump output in driver crash ticket",
        description="Tests triage when a user pastes raw Windows blue screen stop error "
        "output including bug check codes, stack traces, and faulting module info. "
        "The underlying issue is an NVIDIA GPU driver crash.",
        category=_CATEGORY,
        tags=["bsod", "minidump", "driver_crash", "gpu"],
        ticket=EvalTicket(
            ticket_id="INC-5059",
            subject="Workstation blue-screening daily — NVIDIA driver crash",
            description=(
                "My workstation has been blue-screening every morning since the NVIDIA "
                "driver update was pushed last Thursday (version 32.0.15.6094). It crashes "
                "within 2 hours of booting, always during GPU-accelerated tasks like "
                "running Monte Carlo simulations in our pricing engine. "
                "I ran WinDbg on the memory dump and here's the analysis:\n\n"
                f"{_BSOD_OUTPUT}\n\n"
                "The faulting module is nvlddmkm.sys (NVIDIA display driver). The previous "
                "driver version (31.0.15.5201) was stable for 6 months. Machine is a Dell "
                "Precision 7875 Tower with NVIDIA RTX A6000 (asset tag WS-QR-0089), "
                "128 GB RAM, Windows 11 23H2. I need this machine for quant model "
                "development — the GPU compute is essential. Can we roll back the driver "
                "to the previous version or get a hotfix from NVIDIA?\n\n"
                "— Dr. Henrik Lindqvist, Quantitative Research"
            ),
            reporter=_reporter("Henrik Lindqvist", "h.lindqvist@contoso.com", "Quantitative Research"),
            created_at="2026-03-18T07:50:00Z",
            channel="portal",
        ),
        expected_triage=ExpectedTriage(
            category="Hardware & Peripherals",
            priority="P2",
            assigned_team="Endpoint Engineering",
            needs_escalation=False,
        ),
    )
)


# ---------------------------------------------------------------------------
# dc-060: Raw JSON API error response (headers + body) for a software integration issue
# ---------------------------------------------------------------------------
_JSON_API_RESPONSE = (
    "HTTP/1.1 502 Bad Gateway\n"
    "Date: Wed, 18 Mar 2026 08:22:14 GMT\n"
    "Content-Type: application/json; charset=utf-8\n"
    "Content-Length: 1247\n"
    "Connection: keep-alive\n"
    "X-Request-Id: 7e4f2a91-3c8d-4b6e-a5f2-9d1c3b7e8a4f\n"
    "X-Correlation-Id: trade-svc-b2f8a3e1-6d4c-4a9b-8e7f-2c1d5a3b9e6f\n"
    "X-RateLimit-Limit: 1000\n"
    "X-RateLimit-Remaining: 847\n"
    "X-RateLimit-Reset: 1742285400\n"
    "Strict-Transport-Security: max-age=31536000; includeSubDomains\n"
    "X-Content-Type-Options: nosniff\n"
    "X-Frame-Options: DENY\n"
    "Cache-Control: no-store, no-cache, must-revalidate\n"
    "Server: contoso-api-gateway/2.4.1\n\n"
    "{\n"
    '  "error": {\n'
    '    "code": "UPSTREAM_SERVICE_UNAVAILABLE",\n'
    '    "message": "The upstream service \'portfolio-analytics-v3\' is not responding.",\n'
    '    "status": 502,\n'
    '    "timestamp": "2026-03-18T08:22:14.567Z",\n'
    '    "request_id": "7e4f2a91-3c8d-4b6e-a5f2-9d1c3b7e8a4f",\n'
    '    "details": {\n'
    '      "upstream_host": "portfolio-analytics.contoso.internal:8443",\n'
    '      "upstream_path": "/api/v3/portfolios/risk-attribution",\n'
    '      "timeout_ms": 30000,\n'
    '      "retry_count": 3,\n'
    '      "circuit_breaker_state": "OPEN",\n'
    '      "circuit_breaker_trips": 47,\n'
    '      "last_successful_request": "2026-03-18T06:45:22Z",\n'
    '      "health_check_status": "UNHEALTHY",\n'
    '      "pod_status": {\n'
    '        "desired": 5,\n'
    '        "ready": 0,\n'
    '        "not_ready": 5,\n'
    '        "restart_count": 23\n'
    "      }\n"
    "    },\n"
    '    "trace": [\n'
    '      "api-gateway -> portfolio-analytics-v3 (timeout after 30000ms)",\n'
    '      "portfolio-analytics-v3 -> risk-calc-engine (connection refused)",\n'
    '      "risk-calc-engine: CrashLoopBackOff (OOMKilled)"\n'
    "    ]\n"
    "  }\n"
    "}"
)

default_registry.register(
    EvalScenario(
        scenario_id="dc-060",
        name="Raw JSON API error response with HTTP headers in integration ticket",
        description="Tests triage when a user pastes a full HTTP response including "
        "headers, JSON error body with nested objects, circuit breaker status, "
        "and distributed trace for a portfolio analytics service outage.",
        category=_CATEGORY,
        tags=["json", "api_response", "http_headers", "integration"],
        ticket=EvalTicket(
            ticket_id="INC-5060",
            subject="Portfolio analytics API returning 502 — all risk dashboards down",
            description=(
                "All our risk attribution dashboards are broken since about 06:45 UTC. "
                "The portfolio-analytics-v3 API is returning 502 errors. I captured the "
                "full HTTP response from curl including headers:\n\n"
                f"{_JSON_API_RESPONSE}\n\n"
                "Key findings from the response: the risk-calc-engine pods are in "
                "CrashLoopBackOff due to OOMKilled — they're running out of memory and "
                "restarting (23 restarts so far). All 5 pods are not-ready. The circuit "
                "breaker on portfolio-analytics has tripped 47 times and is now OPEN, "
                "meaning all requests fail immediately. This is affecting every risk "
                "dashboard in the firm — portfolio managers, compliance, and the trading "
                "desk all rely on these APIs. The risk-calc-engine likely needs its memory "
                "limits increased in the Kubernetes deployment spec. Currently running in "
                "the contoso-analytics-prod namespace on AKS cluster aks-east-prod-01.\n\n"
                "— Thomas Brennan, Platform Engineering"
            ),
            reporter=_reporter("Thomas Brennan", "t.brennan@contoso.com", "Platform Engineering"),
            created_at="2026-03-18T08:25:00Z",
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
