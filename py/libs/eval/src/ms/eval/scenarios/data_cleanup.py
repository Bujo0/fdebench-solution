# Copyright (c) Microsoft. All rights reserved.
"""Data cleanup evaluation scenarios.

Generates tickets with messy, noisy, or malformed input data that a robust
triage system must handle gracefully. Each scenario pair consists of a
TicketInput (the dirty data) and a TriageDecision (the expected gold answer).

Scenario categories:
- Very long email bodies
- Base64-encoded images embedded in descriptions
- HTML markup in ticket text
- Excessive whitespace and formatting noise
- Unicode edge cases (RTL, zero-width, homoglyphs)
- Extremely long or garbled subjects
- Empty / near-empty tickets
- Repeated / duplicate content
"""

import base64

from ms.eval.models import Reporter
from ms.eval.models import TicketInput
from ms.eval.models import TriageDecision

_DEFAULT_REPORTER = Reporter(
    name="Test User",
    email="test.user@contoso.com",
    department="IT",
)

_DEFAULT_TIMESTAMP = "2026-03-20T10:00:00Z"


def _ticket(
    ticket_id: str,
    subject: str,
    description: str,
    *,
    channel: str = "email",
    reporter: Reporter | None = None,
) -> TicketInput:
    """Build a TicketInput with sensible defaults for eval scenarios."""
    return TicketInput(
        ticket_id=ticket_id,
        subject=subject,
        description=description,
        reporter=reporter or _DEFAULT_REPORTER,
        created_at=_DEFAULT_TIMESTAMP,
        channel=channel,
        attachments=[],
    )


def _gold(
    ticket_id: str,
    *,
    category: str,
    priority: str,
    assigned_team: str,
    needs_escalation: bool = False,
    missing_information: list[str] | None = None,
    next_best_action: str = "Review the ticket and take appropriate action.",
    remediation_steps: list[str] | None = None,
) -> TriageDecision:
    """Build a TriageDecision with sensible defaults for gold answers."""
    return TriageDecision(
        ticket_id=ticket_id,
        category=category,
        priority=priority,
        assigned_team=assigned_team,
        needs_escalation=needs_escalation,
        missing_information=missing_information or [],
        next_best_action=next_best_action,
        remediation_steps=remediation_steps or ["Investigate and resolve the reported issue."],
    )


def scenario_very_long_email() -> tuple[TicketInput, TriageDecision]:
    """Ticket with an extremely long email body (~10K chars of padding).

    Tests that the system doesn't truncate, crash, or misclassify when the
    description is far longer than a typical ticket.
    """
    core_issue = (
        "I can't connect to the VPN from our London office. "
        "Error code: SSL_ERROR_HANDSHAKE_FAILURE. "
        "This started after the network maintenance last weekend."
    )
    padding = (
        " I've been trying various troubleshooting steps. "
        "I restarted my laptop, cleared the browser cache, "
        "tried a different network cable, and even moved to a different desk. "
        "Nothing seems to work and I'm running out of ideas."
    )
    long_body = core_issue + (padding * 50)

    return (
        _ticket("INC-DC-0001", "VPN connection failing — London office", long_body),
        _gold(
            "INC-DC-0001",
            category="Network & Connectivity",
            priority="P2",
            assigned_team="Network Operations",
            missing_information=["network_location"],
            next_best_action="Investigate SSL handshake failure on VPN gateway for London office.",
            remediation_steps=[
                "Check VPN gateway SSL certificate validity for the London office",
                "Verify network maintenance changes did not alter VPN configuration",
                "Test VPN connectivity from a known-good device in the same location",
                "If issue persists, escalate to network engineering for SSL troubleshooting",
            ],
        ),
    )


def scenario_base64_image_in_description() -> tuple[TicketInput, TriageDecision]:
    """Ticket with a base64-encoded image blob pasted into the description.

    Users sometimes paste screenshots as base64 data URIs into email bodies.
    The system must extract the actual text content and not be confused.
    """
    fake_image_data = base64.b64encode(b"\x89PNG\r\n\x1a\n" + b"\x00" * 200).decode("ascii")
    description = (
        "My monitor keeps flickering every few seconds. Here's a photo of what it looks like:\n\n"
        f"data:image/png;base64,{fake_image_data}\n\n"
        "It started after the Windows update yesterday. The flickering happens on both "
        "my external monitors but not the laptop screen. Using Dell U2722D monitors with "
        "a USB-C dock."
    )

    return (
        _ticket("INC-DC-0002", "Monitor flickering — screenshot attached", description),
        _gold(
            "INC-DC-0002",
            category="Hardware & Peripherals",
            priority="P3",
            assigned_team="Endpoint Engineering",
            missing_information=["device_info"],
            next_best_action="Investigate monitor flickering linked to recent Windows update and USB-C dock.",
            remediation_steps=[
                "Check for updated display drivers for the Dell U2722D monitors",
                "Test with a different USB-C dock to isolate the issue",
                "Verify Windows update did not alter display settings",
                "If flickering persists, test monitors directly connected without dock",
            ],
        ),
    )


def scenario_html_email_body() -> tuple[TicketInput, TriageDecision]:
    """Ticket body containing raw HTML markup from a rich-text email client.

    Common when email-to-ticket ingestion doesn't strip HTML properly.
    """
    description = (
        "<html><body>"
        "<div style='font-family: Calibri; font-size: 14px;'>"
        "<p><b>Hi IT Support,</b></p>"
        "<p>I'm getting an <span style='color:red'>Access Denied</span> error when trying "
        "to open the <a href='https://sharepoint.contoso.com/sites/finance'>Finance SharePoint site</a>.</p>"
        "<p>Error message: <code>403 Forbidden - You do not have permission to access this resource</code></p>"
        "<p>I was able to access it last week. My manager (Jennifer Walsh) said my access "
        "should still be active.</p>"
        "<br><p>Thanks,<br>Robert Kim</p>"
        "</div></body></html>"
    )

    return (
        _ticket(
            "INC-DC-0003",
            "Can't access Finance SharePoint site",
            description,
            reporter=Reporter(
                name="Robert Kim",
                email="robert.kim@contoso.com",
                department="Finance",
            ),
        ),
        _gold(
            "INC-DC-0003",
            category="Data & Storage",
            priority="P3",
            assigned_team="Data Platform",
            missing_information=[],
            next_best_action="Verify SharePoint site permissions for Robert Kim on the Finance site.",
            remediation_steps=[
                "Check site collection permissions for robert.kim@contoso.com",
                "Verify no recent permission changes were made to the Finance SharePoint site",
                "Confirm with manager Jennifer Walsh that access should be granted",
                "If permissions are correct, check for conditional access policy blocks",
            ],
        ),
    )


def scenario_excessive_whitespace() -> tuple[TicketInput, TriageDecision]:
    """Ticket with excessive whitespace, tabs, and blank lines throughout.

    Common in phone transcriptions and copy-pasted content.
    """
    description = (
        "\n\n\n"
        "   Caller reports     that their    \t  laptop\t\t  is not\n"
        "\n\n"
        "    booting up  .    \n\n\n\n"
        "     They see a    blue    screen    with   error   code  \n"
        "  \t  0x0000007E    \n\n"
        "   \n\n\n"
        "    Laptop model:    \t  ThinkPad T14s  \n"
        "      \n\n\n"
        "   This has happened     twice   this week   already.   \n"
        "\n\n\n\n\n"
    )

    return (
        _ticket("INC-DC-0004", "Phone  call  —  laptop  not  booting", description, channel="phone"),
        _gold(
            "INC-DC-0004",
            category="Hardware & Peripherals",
            priority="P2",
            assigned_team="Endpoint Engineering",
            missing_information=["steps_to_reproduce"],
            next_best_action="Investigate recurring blue screen error 0x0000007E on ThinkPad T14s.",
            remediation_steps=[
                "Collect crash dump logs from the ThinkPad T14s",
                "Run hardware diagnostics to check for memory or storage failures",
                "If hardware passes, attempt safe mode boot and check recent driver changes",
                "Prepare reimaging as fallback if diagnostics are inconclusive",
            ],
        ),
    )


def scenario_unicode_rtl_and_homoglyphs() -> tuple[TicketInput, TriageDecision]:
    """Ticket with RTL override characters and homoglyph substitutions.

    Tests that text normalization doesn't break classification. Could also
    be an adversarial input attempting to confuse the model.
    """
    # \u202e is RTL override, \u200b is zero-width space
    description = (
        "I\u200bm hav\u200bing tro\u200buble with my \u202eemail\u202c account. "
        "Outlo\u200bok keeps asking for my p\u0430ssword (that 'a' is a Cyrillic а). "
        "I've changed it three times today but it keeps prompting. "
        "Other apps like Teams and SharePoint work fine. "
        "Started this morning around 9 AM."
    )

    return (
        _ticket("INC-DC-0005", "Email\u200b password\u200b issue", description),
        _gold(
            "INC-DC-0005",
            category="Access & Authentication",
            priority="P3",
            assigned_team="Identity & Access Management",
            missing_information=["authentication_method"],
            next_best_action="Investigate repeated password prompts in Outlook that persist after reset.",
            remediation_steps=[
                "Clear cached credentials in Windows Credential Manager",
                "Remove and re-add the Outlook profile",
                "Check for failed sign-in attempts in Entra ID audit logs",
                "If prompting persists, check app-specific password or modern auth requirements",
            ],
        ),
    )


def scenario_extremely_long_subject() -> tuple[TicketInput, TriageDecision]:
    """Ticket with an absurdly long subject line (~500 chars).

    Some email clients allow very long subjects; the system must handle them.
    """
    subject = (
        "URGENT PLEASE HELP — I cannot print to the network printer on the 5th floor "
        "and I have a board meeting in 30 minutes and need to print 50 copies of the "
        "quarterly report and the printer keeps showing offline error and I tried "
        "restarting it but it didn't help and the IT person on the floor is out sick "
        "today and nobody else knows how to fix it and my manager is going to be really "
        "upset if I can't get these printed in time PLEASE HELP ASAP!!!"
    )
    description = "Please see subject. Floor 5, printer near room 512. Printer model: HP LaserJet M609."

    return (
        _ticket("INC-DC-0006", subject, description, channel="chat"),
        _gold(
            "INC-DC-0006",
            category="Hardware & Peripherals",
            priority="P2",
            assigned_team="Network Operations",
            missing_information=[],
            next_best_action="Restore network printer connectivity on Floor 5 before board meeting.",
            remediation_steps=[
                "Check network connectivity to the HP LaserJet M609 near room 512",
                "Verify printer IP address and DNS resolution",
                "Restart print spooler service on the print server",
                "If offline persists, check for physical network cable or switch port issues",
            ],
        ),
    )


def scenario_empty_description() -> tuple[TicketInput, TriageDecision]:
    """Ticket with an empty description body — only subject has info.

    Common from quick chat messages or mobile submissions.
    """
    return (
        _ticket("INC-DC-0007", "SAP is broken", "", channel="chat"),
        _gold(
            "INC-DC-0007",
            category="Software & Applications",
            priority="P3",
            assigned_team="Enterprise Applications",
            missing_information=[
                "error_message",
                "affected_system",
                "steps_to_reproduce",
            ],
            next_best_action="Contact reporter to gather details about the SAP issue.",
            remediation_steps=[
                "Reach out to reporter for error details and affected SAP module",
                "Check SAP system health dashboard for active alerts",
                "Verify reporter's SAP access and credentials are valid",
            ],
        ),
    )


def scenario_repeated_content() -> tuple[TicketInput, TriageDecision]:
    """Ticket where the same sentence is repeated many times.

    Happens with stuck form submissions or copy-paste errors.
    """
    repeated = "I need to reset my password. " * 30
    description = f"Subject: Password reset\n\n{repeated}\n\nPlease help, my account is locked."

    return (
        _ticket("INC-DC-0008", "Password reset", description),
        _gold(
            "INC-DC-0008",
            category="Access & Authentication",
            priority="P3",
            assigned_team="Identity & Access Management",
            missing_information=[],
            next_best_action="Process password reset and unlock the account.",
            remediation_steps=[
                "Verify reporter identity through standard verification procedures",
                "Reset password via Entra ID admin portal",
                "Unlock account if lockout threshold was reached",
                "Advise user on self-service password reset for future use",
            ],
        ),
    )


def scenario_email_thread_noise() -> tuple[TicketInput, TriageDecision]:
    """Ticket that includes a long email thread chain with reply headers.

    The actual issue is buried under layers of "From: ... Sent: ... Subject: ..."
    """
    description = (
        "---------- Forwarded message ----------\n"
        "From: Sarah Mitchell <sarah.mitchell@contoso.com>\n"
        "Date: Tue, Mar 19, 2026 at 4:15 PM\n"
        "Subject: Re: Re: Re: Database access for analytics team\n"
        "To: IT Support <it-support@contoso.com>\n\n"
        "Hi team, following up again. We still can't access the prod-analytics-db. "
        "Getting 'connection refused' on port 5432.\n\n"
        "---------- Original message ----------\n"
        "From: IT Support <it-support@contoso.com>\n"
        "Date: Mon, Mar 18, 2026 at 9:00 AM\n"
        "Subject: Re: Re: Database access for analytics team\n"
        "To: Sarah Mitchell <sarah.mitchell@contoso.com>\n\n"
        "We've forwarded your request to the data platform team. "
        "Please allow 24 hours for processing.\n\n"
        "---------- Original message ----------\n"
        "From: Sarah Mitchell <sarah.mitchell@contoso.com>\n"
        "Date: Fri, Mar 15, 2026 at 2:30 PM\n"
        "Subject: Re: Database access for analytics team\n"
        "To: IT Support <it-support@contoso.com>\n\n"
        "Bumping this again — it's been a week since I requested access "
        "to prod-analytics-db for the analytics team. Four people are blocked.\n\n"
        "---------- Original message ----------\n"
        "From: Sarah Mitchell <sarah.mitchell@contoso.com>\n"
        "Date: Fri, Mar 8, 2026 at 10:00 AM\n"
        "Subject: Database access for analytics team\n"
        "To: IT Support <it-support@contoso.com>\n\n"
        "Hi, I need read access to prod-analytics-db for myself and three team members: "
        "David Park, Lisa Wong, and James O'Brien. We need it for the Q1 reporting project. "
        "Our manager (VP Analytics) has approved this."
    )

    return (
        _ticket(
            "INC-DC-0009",
            "Fwd: Re: Re: Re: Database access for analytics team",
            description,
            reporter=Reporter(
                name="Sarah Mitchell",
                email="sarah.mitchell@contoso.com",
                department="Analytics",
            ),
        ),
        _gold(
            "INC-DC-0009",
            category="Data & Storage",
            priority="P2",
            assigned_team="Data Platform",
            needs_escalation=True,
            missing_information=[],
            next_best_action="Expedite database access provisioning — request is overdue and blocking team.",
            remediation_steps=[
                "Verify manager approval for prod-analytics-db access",
                "Create read-only database roles for the four team members",
                "Check firewall rules for port 5432 connectivity",
                "Test connection from analytics team workstations after provisioning",
            ],
        ),
    )


def scenario_mixed_languages() -> tuple[TicketInput, TriageDecision]:
    """Ticket with mixed English and non-English text (Mandarin / Spanish).

    Singapore office staff may write tickets in mixed languages.
    """
    description = (
        "我的笔记本电脑连不上WiFi了。Error message says 'No networks found'. "
        "I'm in the Singapore office, 12th floor. 我试了重启但没有用。 "
        "My colleague sitting next to me has no issues connecting. "
        "Laptop: Surface Pro 9, Windows 11. Por favor help ASAP, "
        "tengo una reunión importante en una hora."
    )

    return (
        _ticket(
            "INC-DC-0010",
            "WiFi not working — Singapore office",
            description,
            channel="chat",
            reporter=Reporter(
                name="Wei Lin",
                email="wei.lin@contoso.com",
                department="Trading",
            ),
        ),
        _gold(
            "INC-DC-0010",
            category="Network & Connectivity",
            priority="P3",
            assigned_team="Network Operations",
            missing_information=[],
            next_best_action="Investigate WiFi connectivity issue isolated to single device in Singapore 12th floor.",
            remediation_steps=[
                "Check WiFi adapter status on the Surface Pro 9",
                "Run network diagnostics and reset WiFi adapter",
                "Verify device can see SSIDs from other networks to isolate hardware vs software",
                "If adapter is functional, check for MAC filtering or network policy issues",
            ],
        ),
    )


def scenario_base64_attachment_flood() -> tuple[TicketInput, TriageDecision]:
    """Ticket with multiple base64 blobs simulating inline image attachments.

    Tests handling of very large payloads with mostly non-text content.
    """
    fake_blob = base64.b64encode(b"\xff\xd8\xff\xe0" + b"\xab" * 500).decode("ascii")
    attachments_text = "\n".join(
        f"[Inline image {i}]: data:image/jpeg;base64,{fake_blob}" for i in range(1, 6)
    )
    description = (
        "Multiple errors appearing on my screen. See screenshots below:\n\n"
        f"{attachments_text}\n\n"
        "The errors pop up every time I open Excel. Something about 'COM Surrogate has stopped working'. "
        "This is blocking my work on the quarterly financials."
    )

    return (
        _ticket("INC-DC-0011", "Excel errors — screenshots attached", description),
        _gold(
            "INC-DC-0011",
            category="Software & Applications",
            priority="P2",
            assigned_team="Endpoint Engineering",
            missing_information=["application_version"],
            next_best_action="Investigate COM Surrogate crash when launching Excel.",
            remediation_steps=[
                "Check Event Viewer for COM Surrogate crash details",
                "Repair or reinstall Microsoft Office",
                "Check for conflicting COM add-ins in Excel",
                "If repair fails, create a new Windows user profile to test isolation",
            ],
        ),
    )


def scenario_special_characters_and_encoding() -> tuple[TicketInput, TriageDecision]:
    """Ticket with special characters, emoji, and encoding artifacts.

    Common when text passes through multiple systems with different encodings.
    """
    description = (
        "Can\u2019t access OneDrive \u2014 getting error \u201cSync pending\u201d for 3 days \U0001f629\n"
        "Files show as \u00e2\u20ac\u0153syncing\u00e2\u20ac\u009d but never complete.\n"
        "Tried: \u2022 Restart \u2022 Sign out/in \u2022 Reset OneDrive\n"
        "Storage: 45GB/1TB used\n"
        "OS: Windows 11 23H2 \u00a9 Microsoft\n"
        "\u26a0\ufe0f IMPORTANT: Contains client documents for the Morrison deal"
    )

    return (
        _ticket("INC-DC-0012", "OneDrive sync stuck 😩", description),
        _gold(
            "INC-DC-0012",
            category="Data & Storage",
            priority="P2",
            assigned_team="Data Platform",
            missing_information=[],
            next_best_action="Investigate OneDrive sync failure persisting after standard troubleshooting.",
            remediation_steps=[
                "Check OneDrive sync status logs for specific error codes",
                "Verify no files exceed OneDrive size or path length limits",
                "Clear OneDrive cache and force full resync",
                "If sync remains stuck, check for conditional access or DLP policy interference",
            ],
        ),
    )


def scenario_csv_tabular_data() -> tuple[TicketInput, TriageDecision]:
    """Ticket with raw CSV / spreadsheet data pasted into the description.

    Users sometimes copy-paste entire spreadsheet ranges into ticket bodies.
    The system must extract the actual issue from the tabular noise.
    """
    csv_rows = "\n".join(
        f"Server{i:02d},10.0.1.{i},{status},{cpu}%,{mem}GB"
        for i, (status, cpu, mem) in enumerate(
            [
                ("OK", 12, 4),
                ("OK", 23, 6),
                ("CRITICAL", 98, 15),
                ("OK", 15, 3),
                ("WARNING", 75, 12),
                ("OK", 8, 2),
                ("CRITICAL", 99, 16),
                ("OK", 30, 5),
                ("OK", 18, 4),
                ("WARNING", 65, 10),
            ],
            start=1,
        )
    )
    description = (
        "Here is the server health report from this morning's check:\n\n"
        "Hostname,IP,Status,CPU,Memory\n"
        f"{csv_rows}\n\n"
        "As you can see, Server03 and Server07 are showing CRITICAL status. "
        "Both are in our production cluster running the trading platform. "
        "CPU is pegged at ~99% and memory is over 15GB. "
        "This started around 6 AM today. Needs immediate attention."
    )

    return (
        _ticket(
            "INC-DC-0013",
            "Server health report — critical servers",
            description,
            channel="portal",
            reporter=Reporter(
                name="Michael Torres",
                email="michael.torres@contoso.com",
                department="Infrastructure",
            ),
        ),
        _gold(
            "INC-DC-0013",
            category="Hardware & Peripherals",
            priority="P1",
            assigned_team="Endpoint Engineering",
            needs_escalation=True,
            missing_information=["error_message"],
            next_best_action="Investigate critical CPU and memory usage on production trading servers.",
            remediation_steps=[
                "Check running processes on Server03 and Server07 for runaway tasks",
                "Review application logs on both servers for errors starting around 6 AM",
                "Assess impact to the trading platform and prepare failover if needed",
                "Scale resources or restart affected services once root cause is identified",
            ],
        ),
    )


def scenario_massive_email_signature() -> tuple[TicketInput, TriageDecision]:
    """Ticket where the actual issue is buried under a massive corporate signature.

    Common when auto-forwarded emails include multiple nested signatures
    with legal disclaimers, contact blocks, and social media links.
    """
    signature = (
        "\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "Patricia D. Henderson, CFA, MBA\n"
        "Senior Vice President — Global Wealth Management\n"
        "Contoso Financial Services, LLC\n"
        "350 Park Avenue, 42nd Floor\n"
        "New York, NY 10022\n"
        "Office: +1 (212) 555-0142 | Mobile: +1 (917) 555-0198\n"
        "Fax: +1 (212) 555-0199\n"
        "Email: patricia.henderson@contoso.com\n"
        "LinkedIn: linkedin.com/in/patriciahenderson\n"
        "Website: www.contoso.com/wealth-management\n\n"
        "🌟 Voted #1 Wealth Management Firm — Financial Times 2025\n"
        "📈 Managing $42B in client assets\n\n"
        "CONFIDENTIALITY NOTICE: This electronic message and any files "
        "transmitted with it are intended exclusively for the individual or "
        "entity to which it is addressed. This message may contain information "
        "that is proprietary, privileged, confidential, or otherwise legally "
        "exempt from disclosure. If you are not the named addressee, you should "
        "not disseminate, distribute, or copy this email. Please notify the "
        "sender immediately by email if you have received this email by mistake "
        "and delete this email from your system. E-mail transmission cannot be "
        "guaranteed to be secure or error-free, as information could be "
        "intercepted, corrupted, lost, destroyed, arrive late or incomplete, "
        "or contain viruses. The sender therefore does not accept liability for "
        "any errors or omissions in the contents of this message which arise as "
        "a result of email transmission.\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
    )
    description = (
        "I can't open the Bloomberg Terminal app — it crashes on launch with "
        "a license error."
        + signature * 3
    )

    return (
        _ticket(
            "INC-DC-0014",
            "Bloomberg Terminal not launching",
            description,
            reporter=Reporter(
                name="Patricia Henderson",
                email="patricia.henderson@contoso.com",
                department="Wealth Management",
            ),
        ),
        _gold(
            "INC-DC-0014",
            category="Software & Applications",
            priority="P2",
            assigned_team="Enterprise Applications",
            missing_information=["error_message"],
            next_best_action="Investigate Bloomberg Terminal license error preventing launch.",
            remediation_steps=[
                "Check Bloomberg Terminal license status and expiration",
                "Verify the Bloomberg BLP API service is running",
                "Reinstall Bloomberg Terminal if license is valid but app fails",
                "Contact Bloomberg support if license issue persists",
            ],
        ),
    )


def scenario_url_heavy_description() -> tuple[TicketInput, TriageDecision]:
    """Ticket description consisting mostly of URLs and hyperlinks.

    Users sometimes paste a list of URLs to show which pages are broken.
    The system must extract the actual issue from the URL soup.
    """
    urls = "\n".join(
        f"- https://sharepoint.contoso.com/sites/finance/{page} → {error}"
        for page, error in [
            ("reports/q1-2026", "500 Internal Server Error"),
            ("reports/q4-2025", "500 Internal Server Error"),
            ("dashboards/revenue", "This page can't be reached"),
            ("dashboards/expenses", "500 Internal Server Error"),
            ("team/documents", "This page can't be reached"),
            ("team/calendar", "OK"),
            ("policies/travel", "500 Internal Server Error"),
            ("forms/expense-report", "This page can't be reached"),
            ("announcements", "OK"),
            ("training/compliance-2026", "500 Internal Server Error"),
        ]
    )
    description = (
        "Multiple pages on Finance SharePoint are down. Tested each one:\n\n"
        f"{urls}\n\n"
        "8 out of 10 pages are broken. This is blocking the entire Finance "
        "department from accessing Q1 reports. Started about an hour ago."
    )

    return (
        _ticket(
            "INC-DC-0015",
            "Finance SharePoint — multiple pages returning 500 errors",
            description,
            channel="portal",
        ),
        _gold(
            "INC-DC-0015",
            category="Software & Applications",
            priority="P1",
            assigned_team="Enterprise Applications",
            needs_escalation=True,
            missing_information=[],
            next_best_action="Investigate widespread 500 errors on Finance SharePoint site collection.",
            remediation_steps=[
                "Check SharePoint application pool health and IIS logs",
                "Verify backend database connectivity for the Finance site collection",
                "Review recent deployments or configuration changes to SharePoint",
                "If server-side issue confirmed, restart application pool and monitor",
            ],
        ),
    )


def scenario_ansi_terminal_output() -> tuple[TicketInput, TriageDecision]:
    """Ticket with raw terminal output containing ANSI escape sequences.

    Developers sometimes paste terminal output with color codes directly
    into tickets when reporting build or deployment failures.
    """
    description = (
        "Deploy failed. Here's the output:\n\n"
        "\x1b[32m[INFO]\x1b[0m Starting deployment pipeline v3.2.1\n"
        "\x1b[32m[INFO]\x1b[0m Building container image...\n"
        "\x1b[33m[WARN]\x1b[0m Deprecated API version in manifest\n"
        "\x1b[32m[INFO]\x1b[0m Pushing to acr-prod.azurecr.io/trading-api:latest\n"
        "\x1b[31m[ERROR]\x1b[0m Push failed: unauthorized: authentication required\n"
        "\x1b[31m[ERROR]\x1b[0m Service principal token expired\n"
        "\x1b[31m[FATAL]\x1b[0m Pipeline aborted at stage: push-image\n"
        "\x1b[90m  exit code: 1\x1b[0m\n"
        "\x1b[90m  duration: 4m 32s\x1b[0m\n\n"
        "This is blocking our release to production."
    )

    return (
        _ticket(
            "INC-DC-0016",
            "Deploy pipeline failed — auth error",
            description,
            channel="chat",
            reporter=Reporter(
                name="Dev Team Lead",
                email="devlead@contoso.com",
                department="Engineering",
            ),
        ),
        _gold(
            "INC-DC-0016",
            category="Access & Authentication",
            priority="P2",
            assigned_team="Identity & Access Management",
            missing_information=["affected_system"],
            next_best_action="Renew expired service principal credentials for container registry access.",
            remediation_steps=[
                "Check and renew the service principal token for acr-prod.azurecr.io",
                "Verify RBAC role assignments for the deployment pipeline identity",
                "Re-run the failed deployment pipeline after credential renewal",
                "Set up alerts for upcoming service principal expiration",
            ],
        ),
    )


def scenario_garbled_ocr_text() -> tuple[TicketInput, TriageDecision]:
    """Ticket created from a badly scanned document via OCR.

    OCR artifacts include misrecognized characters, merged words, and
    random symbols replacing actual text. Common with scanned forms.
    """
    description = (
        "Fr0m: Faci1ities Desk\n"
        "Re: Netw0rk 0utage — B1dg 7, F1oor 3\n\n"
        "A11 netw0rk p0rts 0n the th1rd f1oor 0f bui1ding 7 are d0wn.\n"
        "Approx|mately 45 emp1oyees are affect3d and cann0t c0nnect t0\n"
        "any netw0rk res0urces inc1uding Wi-Fi and wir3d c0nnecti0ns.\n"
        "The 1ssue start3d at 2:30 PM t0day after a p0wer f1icker.\n"
        "Sw1tch r00m 0n f1oor 3 may need phys1cal inspect10n.\n"
        "Ple@se send s0me0ne ASAP — peop1e are 1eaving f0r the day."
    )

    return (
        _ticket(
            "INC-DC-0017",
            "Netw0rk 0utage — B1dg 7 F1oor 3",
            description,
            channel="email",
            reporter=Reporter(
                name="Facilities Desk",
                email="facilities@contoso.com",
                department="Facilities",
            ),
        ),
        _gold(
            "INC-DC-0017",
            category="Network & Connectivity",
            priority="P1",
            assigned_team="Network Operations",
            needs_escalation=True,
            missing_information=[],
            next_best_action="Dispatch network technician to Building 7 Floor 3 switch room.",
            remediation_steps=[
                "Physically inspect network switch room on Floor 3 of Building 7",
                "Check for tripped breakers or damaged equipment after power flicker",
                "Test switch port connectivity and replace failed hardware if needed",
                "Restore network service to all 45 affected employees",
            ],
        ),
    )


def scenario_multiple_issues_one_ticket() -> tuple[TicketInput, TriageDecision]:
    """Ticket that reports multiple unrelated problems in a single submission.

    Users sometimes bundle several issues into one ticket. The system must
    identify the primary/most urgent issue for triage.
    """
    description = (
        "Hi, I have a few things:\n\n"
        "1) My Outlook keeps crashing every time I open an attachment. "
        "This has been going on for 3 days and I've lost unsaved emails twice.\n\n"
        "2) Also, the printer on Floor 8 is out of toner but that's not urgent.\n\n"
        "3) Can someone reset the conference room Polycom in Room 410? "
        "The display is frozen on the Contoso logo.\n\n"
        "4) My parking badge stopped working last week for the underground garage. "
        "I've been parking on the street.\n\n"
        "5) Most importantly — I think my laptop has a virus. I'm getting random "
        "pop-ups and my browser keeps redirecting to weird sites even when I'm "
        "not browsing. The pop-ups started appearing on Monday."
    )

    return (
        _ticket(
            "INC-DC-0018",
            "Several issues — Outlook, printer, badge, laptop",
            description,
            channel="email",
            reporter=Reporter(
                name="Jessica Wang",
                email="jessica.wang@contoso.com",
                department="Operations",
            ),
        ),
        _gold(
            "INC-DC-0018",
            category="Security & Compliance",
            priority="P2",
            assigned_team="Security Operations",
            needs_escalation=True,
            missing_information=["device_info"],
            next_best_action="Investigate potential malware on laptop — browser redirects and pop-ups.",
            remediation_steps=[
                "Isolate the laptop from the network to prevent potential spread",
                "Run full antimalware scan using Microsoft Defender",
                "Check browser extensions and installed programs for malicious entries",
                "If malware confirmed, reimage the device and restore from clean backup",
            ],
        ),
    )


def scenario_markdown_formatted_ticket() -> tuple[TicketInput, TriageDecision]:
    """Ticket written in full Markdown with headers, code blocks, and tables.

    Common from developers who write tickets in Markdown-aware tools.
    The system must extract content from the formatting noise.
    """
    description = (
        "# VPN Split-Tunnel Configuration Error\n\n"
        "## Environment\n"
        "- **OS**: Windows 11 Enterprise 23H2\n"
        "- **VPN Client**: GlobalProtect 6.2.1\n"
        "- **Location**: Remote — home office\n\n"
        "## Problem\n"
        "After the latest GlobalProtect update, split tunneling is broken. "
        "**ALL** traffic is now routed through the VPN tunnel, including personal "
        "traffic and streaming services.\n\n"
        "## Steps to Reproduce\n"
        "1. Connect to VPN via GlobalProtect\n"
        "2. Run `tracert 8.8.8.8`\n"
        "3. Notice all hops go through `10.0.0.x` corporate range\n\n"
        "## Expected Behavior\n"
        "Only `*.contoso.com` and internal `10.x.x.x` traffic should route via VPN.\n\n"
        "## Actual Behavior\n"
        "```\n"
        "C:\\> tracert 8.8.8.8\n"
        " 1    <1 ms    <1 ms    <1 ms  10.0.0.1\n"
        " 2     3 ms     2 ms     2 ms  10.0.0.254\n"
        " 3    15 ms    14 ms    14 ms  172.16.1.1\n"
        "```\n\n"
        "## Impact\n"
        "| Metric | Before | After |\n"
        "|--------|--------|-------|\n"
        "| Internet speed | 500 Mbps | 25 Mbps |\n"
        "| Latency | 5ms | 120ms |\n"
        "| Affected users | 0 | ~200 remote |\n"
    )

    return (
        _ticket(
            "INC-DC-0019",
            "VPN split-tunnel broken after update",
            description,
            channel="portal",
            reporter=Reporter(
                name="Kevin Zhao",
                email="kevin.zhao@contoso.com",
                department="Engineering",
            ),
        ),
        _gold(
            "INC-DC-0019",
            category="Network & Connectivity",
            priority="P2",
            assigned_team="Network Operations",
            missing_information=[],
            next_best_action="Investigate GlobalProtect split-tunnel misconfiguration affecting remote workers.",
            remediation_steps=[
                "Review GlobalProtect split-tunnel policy for recent changes",
                "Compare current VPN configuration with the pre-update baseline",
                "Restore correct split-tunnel rules for non-corporate traffic",
                "Test and validate that only internal traffic routes through VPN",
            ],
        ),
    )


def scenario_subject_description_mismatch() -> tuple[TicketInput, TriageDecision]:
    """Ticket where the subject line describes a completely different issue than the body.

    Occurs when users reply to an old ticket thread with a new, unrelated issue.
    The system must prioritize the description content over the misleading subject.
    """
    description = (
        "Ignore the subject — this is a new issue.\n\n"
        "Our entire Salesforce instance is down. Nobody in the Sales department "
        "(about 120 people) can log in. We're getting 'Service Unavailable' errors. "
        "This started 15 minutes ago and we have a major client demo at 2 PM. "
        "Revenue pipeline worth $3M is at risk if we can't get in for this demo. "
        "Please treat this as highest priority."
    )

    return (
        _ticket(
            "INC-DC-0020",
            "Re: Re: Fwd: Old printer issue from January (RESOLVED)",
            description,
            channel="email",
            reporter=Reporter(
                name="Sales Operations",
                email="sales.ops@contoso.com",
                department="Sales",
            ),
        ),
        _gold(
            "INC-DC-0020",
            category="Software & Applications",
            priority="P1",
            assigned_team="Enterprise Applications",
            needs_escalation=True,
            missing_information=[],
            next_best_action="Investigate Salesforce outage blocking 120 users before client demo.",
            remediation_steps=[
                "Check Salesforce service status page and trust.salesforce.com",
                "Verify SSO and identity provider connectivity to Salesforce",
                "If Contoso-side issue, check network connectivity to Salesforce endpoints",
                "If Salesforce-side issue, open a Severity 1 case with Salesforce support",
            ],
        ),
    )


def get_all_data_cleanup_scenarios() -> list[tuple[TicketInput, TriageDecision]]:
    """Return all data cleanup evaluation scenarios as (ticket, gold) pairs."""
    return [
        scenario_very_long_email(),
        scenario_base64_image_in_description(),
        scenario_html_email_body(),
        scenario_excessive_whitespace(),
        scenario_unicode_rtl_and_homoglyphs(),
        scenario_extremely_long_subject(),
        scenario_empty_description(),
        scenario_repeated_content(),
        scenario_email_thread_noise(),
        scenario_mixed_languages(),
        scenario_base64_attachment_flood(),
        scenario_special_characters_and_encoding(),
        scenario_csv_tabular_data(),
        scenario_massive_email_signature(),
        scenario_url_heavy_description(),
        scenario_ansi_terminal_output(),
        scenario_garbled_ocr_text(),
        scenario_multiple_issues_one_ticket(),
        scenario_markdown_formatted_ticket(),
        scenario_subject_description_mismatch(),
    ]
