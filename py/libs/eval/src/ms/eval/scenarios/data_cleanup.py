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
from typing import Literal

from ms.eval.models import Category
from ms.eval.models import MissingInfoField
from ms.eval.models import Priority
from ms.eval.models import Reporter
from ms.eval.models import Team
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
    channel: Literal["email", "chat", "portal", "phone"] = "email",
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
    category: Category,
    priority: Priority,
    assigned_team: Team,
    needs_escalation: bool = False,
    missing_information: list[MissingInfoField] | None = None,
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
    attachments_text = "\n".join(f"[Inline image {i}]: data:image/jpeg;base64,{fake_blob}" for i in range(1, 6))
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
    description = "I can't open the Bloomberg Terminal app — it crashes on launch with a license error." + signature * 3

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


def scenario_json_config_dump() -> tuple[TicketInput, TriageDecision]:
    """Ticket where someone pasted a massive JSON config into the description.

    Users sometimes dump entire configuration files into ticket descriptions
    hoping IT can spot the issue. The system must extract the actual problem
    from the surrounding JSON noise.
    """
    json_blob = (
        "{\n"
        '  "appSettings": {\n'
        '    "connectionString": "Server=sql-prod-03.contoso.com;Database=FinanceDB;'
        'Trusted_Connection=True;MultipleActiveResultSets=true",\n'
        '    "maxPoolSize": 100,\n'
        '    "minPoolSize": 5,\n'
        '    "connectionTimeout": 30,\n'
        '    "commandTimeout": 120,\n'
        '    "retryCount": 3,\n'
        '    "retryInterval": 5,\n'
        '    "enableCaching": true,\n'
        '    "cacheExpiration": 3600,\n'
        '    "logLevel": "Warning",\n'
        '    "enableDetailedErrors": false,\n'
        '    "maxRequestSize": 52428800,\n'
        '    "allowedOrigins": [\n'
        '      "https://portal.contoso.com",\n'
        '      "https://finance.contoso.com",\n'
        '      "https://api.contoso.com"\n'
        "    ],\n"
        '    "authentication": {\n'
        '      "provider": "AzureAD",\n'
        '      "tenantId": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",\n'
        '      "clientId": "12345678-abcd-efgh-ijkl-1234567890ab",\n'
        '      "audience": "api://finance-app",\n'
        '      "issuer": "https://login.microsoftonline.com/contoso.com/v2.0"\n'
        "    },\n"
        '    "featureFlags": {\n'
        '      "enableNewDashboard": true,\n'
        '      "enableBetaReports": false,\n'
        '      "enableAutoReconciliation": true,\n'
        '      "maintenanceMode": false\n'
        "    },\n"
        '    "smtp": {\n'
        '      "host": "smtp.contoso.com",\n'
        '      "port": 587,\n'
        '      "useSsl": true,\n'
        '      "from": "no-reply@contoso.com"\n'
        "    }\n"
        "  }\n"
        "}"
    )

    description = (
        "After the last deployment, our internal Finance dashboard stopped loading. "
        "We get a blank white page. The config file was changed during the update — "
        "can someone check if something looks wrong?\n\n"
        f"Here's the full appsettings.json:\n\n{json_blob}\n\n"
        "The app worked fine before Friday's release. About 45 users in Finance "
        "are affected. We need this for month-end close reports."
    )

    return (
        _ticket(
            "INC-DC-0021",
            "Finance dashboard blank after deployment — config attached",
            description,
            channel="portal",
            reporter=Reporter(
                name="David Chen",
                email="david.chen@contoso.com",
                department="Finance",
            ),
        ),
        _gold(
            "INC-DC-0021",
            category="Software & Applications",
            priority="P2",
            assigned_team="Enterprise Applications",
            missing_information=["error_message", "application_version"],
            next_best_action="Investigate Finance dashboard blank page after recent deployment.",
            remediation_steps=[
                "Review deployment change log for configuration differences",
                "Check application logs for startup errors or missing dependencies",
                "Compare current appsettings.json with pre-deployment backup",
                "If config issue found, roll back the changed settings and redeploy",
            ],
        ),
    )


def scenario_stack_trace_flood() -> tuple[TicketInput, TriageDecision]:
    """Ticket flooded with a multi-page Java stack trace.

    Developers sometimes paste entire stack traces into tickets. The system
    must identify the actual issue from the brief description at the top
    despite hundreds of lines of trace output.
    """
    stack_frames = []
    packages = [
        "com.contoso.finance.service",
        "com.contoso.finance.repository",
        "com.contoso.finance.controller",
        "org.springframework.web.servlet",
        "org.springframework.beans.factory",
        "org.apache.catalina.core",
        "org.apache.coyote.http11",
        "java.lang.reflect",
        "sun.reflect",
    ]
    methods = [
        "processRequest",
        "handleInternal",
        "doDispatch",
        "invokeMethod",
        "getBean",
        "createBean",
        "initializeBean",
        "applyMiddleware",
        "executeQuery",
        "getConnection",
        "authenticate",
        "validateToken",
    ]
    for i in range(80):
        pkg = packages[i % len(packages)]
        method = methods[i % len(methods)]
        line_num = 100 + (i * 7) % 500
        stack_frames.append(f"\tat {pkg}.{method}({method}.java:{line_num})")

    stack_trace = (
        "java.sql.SQLTransientConnectionException: HikariPool-1 — Connection is not available, "
        "request timed out after 30000ms.\n"
        + "\n".join(stack_frames)
        + "\nCaused by: java.net.SocketTimeoutException: Connect timed out\n"
        + "\n".join(stack_frames[:20])
    )

    description = (
        "The Trade Reconciliation app crashes every time a user tries to generate "
        "the daily P&L report. It was working fine until this morning. About 30 traders "
        "are blocked.\n\n"
        f"Full stack trace from the application server:\n\n{stack_trace}"
    )

    return (
        _ticket("INC-DC-0022", "Trade Reconciliation app — P&L report crashing", description),
        _gold(
            "INC-DC-0022",
            category="Software & Applications",
            priority="P1",
            assigned_team="Enterprise Applications",
            needs_escalation=True,
            missing_information=["environment_details"],
            next_best_action=(
                "Investigate database connection pool exhaustion causing Trade Reconciliation "
                "app crashes blocking 30 traders."
            ),
            remediation_steps=[
                "Check database server connectivity and connection pool status",
                "Review HikariCP connection pool metrics and increase pool size if needed",
                "Verify no database maintenance or firewall changes occurred this morning",
                "Restart the application server connection pool as immediate mitigation",
            ],
        ),
    )


def scenario_double_encoded_html_entities() -> tuple[TicketInput, TriageDecision]:
    """Ticket with double-encoded HTML entities throughout.

    Occurs when email-to-ticket ingestion encodes HTML entities twice,
    e.g. '&' becomes '&amp;amp;' and '<' becomes '&amp;lt;'.
    """
    description = (
        "I can&amp;apos;t log in to the SSO portal. When I enter my credentials "
        "I get an error that says &amp;quot;Authentication failed &amp;amp; session "
        "expired&amp;quot;. The URL shows &amp;lt;redirectUri&amp;gt; as "
        "&amp;quot;https&amp;#58;//sso.contoso.com/callback&amp;amp;state=xyz&amp;quot;.\n\n"
        "I&amp;apos;ve tried clearing cookies &amp;amp; using incognito mode. "
        "Same error. My colleague Sarah &amp;lt;sarah.jones@contoso.com&amp;gt; "
        "has the same problem. We&amp;apos;re both in the Compliance department "
        "and need access for the quarterly audit &amp;#8212; deadline is Friday."
    )

    return (
        _ticket(
            "INC-DC-0023",
            "SSO login broken &amp;amp; session errors",
            description,
            reporter=Reporter(
                name="Marcus Webb",
                email="marcus.webb@contoso.com",
                department="Compliance",
            ),
        ),
        _gold(
            "INC-DC-0023",
            category="Access & Authentication",
            priority="P2",
            assigned_team="Identity & Access Management",
            missing_information=["error_message"],
            next_best_action="Investigate SSO authentication failure affecting Compliance users before audit deadline.",
            remediation_steps=[
                "Check SSO portal health and recent configuration changes",
                "Verify redirect URI configuration in Azure AD app registration",
                "Review authentication logs for Marcus Webb and Sarah Jones",
                "If widespread, check if a certificate or token signing key expired",
            ],
        ),
    )


def scenario_auto_reply_loop() -> tuple[TicketInput, TriageDecision]:
    """Ticket generated from an out-of-office auto-reply loop.

    When two mailboxes with auto-replies exchange messages, the ticket body
    becomes a chain of repeated auto-responses. The system must recognize
    the original issue buried in the noise.
    """
    auto_reply_block = (
        "--- Auto-Reply ---\n"
        "Thank you for your message. I am currently out of the office "
        "and will return on March 25, 2026. For urgent matters, please "
        "contact the IT Service Desk at ext. 4500.\n"
        "Best regards, Janet Liu\n\n"
        "--- Auto-Reply ---\n"
        "I am out of the office until March 24. Your message has been "
        "received and I will respond upon my return.\n"
        "- Michael Torres, Enterprise Applications\n\n"
    )

    description = (
        "Hi IT Support,\n\n"
        "The shared mailbox for Accounts Payable (ap@contoso.com) is not "
        "receiving any external emails. Internal emails work fine. This has "
        "been happening since Monday morning. We have 200+ invoices that "
        "vendors are trying to send us and month-end close is Thursday.\n\n"
        "Can someone look at the mail flow rules?\n\n"
        "Thanks,\nRachel Park\n\n" + (auto_reply_block * 12)
    )

    return (
        _ticket(
            "INC-DC-0024",
            "Re: Auto: Re: Auto: Re: Auto: AP mailbox not receiving external emails",
            description,
            channel="email",
            reporter=Reporter(
                name="Rachel Park",
                email="rachel.park@contoso.com",
                department="Accounts Payable",
            ),
        ),
        _gold(
            "INC-DC-0024",
            category="Software & Applications",
            priority="P1",
            assigned_team="Enterprise Applications",
            needs_escalation=True,
            missing_information=[],
            next_best_action=(
                "Investigate external email delivery failure to AP shared mailbox "
                "blocking 200+ invoices before month-end close."
            ),
            remediation_steps=[
                "Check Exchange Online mail flow rules for the AP shared mailbox",
                "Review message trace for external emails sent to ap@contoso.com",
                "Verify MX records and transport rules have not been modified recently",
                "Check spam/quarantine for blocked external messages",
            ],
        ),
    )


def scenario_binary_hex_dump() -> tuple[TicketInput, TriageDecision]:
    """Ticket with a raw hex dump pasted as the description.

    Users sometimes paste output from debugging tools like `xxd` or
    device descriptor dumps when reporting hardware issues.
    """
    hex_lines = []
    for offset in range(0, 256, 16):
        hex_bytes = " ".join(f"{(offset + i) & 0xFF:02x}" for i in range(16))
        ascii_repr = "".join(chr((offset + i) & 0x7F) if 32 <= ((offset + i) & 0x7F) < 127 else "." for i in range(16))
        hex_lines.append(f"{offset:08x}  {hex_bytes}  |{ascii_repr}|")
    hex_dump = "\n".join(hex_lines)

    description = (
        "My docking station stopped recognizing my external monitors after "
        "a firmware update. I ran the USB descriptor dump as IT asked — "
        "here it is:\n\n"
        f"$ lsusb -v -d 17ef:30b0\n{hex_dump}\n\n"
        f"$ lsusb -v -d 17ef:30b0 (port 2)\n{hex_dump}\n\n"
        "The dock LED blinks amber instead of solid white. Two Dell U2723QE "
        "monitors connected via DisplayPort. Laptop is ThinkPad X1 Carbon Gen 11. "
        "Dock model is ThinkPad USB-C Dock Gen 2 (40AS)."
    )

    return (
        _ticket(
            "INC-DC-0025",
            "Docking station not detecting monitors after firmware update",
            description,
            reporter=Reporter(
                name="Elena Vasquez",
                email="elena.vasquez@contoso.com",
                department="Risk Management",
            ),
        ),
        _gold(
            "INC-DC-0025",
            category="Hardware & Peripherals",
            priority="P3",
            assigned_team="Endpoint Engineering",
            missing_information=["steps_to_reproduce"],
            next_best_action="Investigate docking station firmware update causing monitor detection failure.",
            remediation_steps=[
                "Check if a dock firmware rollback is available from Lenovo support",
                "Test monitors with direct cable connections bypassing the dock",
                "Update ThinkPad USB-C Dock Gen 2 firmware to latest stable version",
                "If firmware rollback fails, replace docking station from inventory",
            ],
        ),
    )


def scenario_control_characters() -> tuple[TicketInput, TriageDecision]:
    """Ticket with embedded control characters — null bytes, form feeds, bell chars.

    Can occur when ticket text is copied from terminal output, binary log viewers,
    or improperly processed text streams. The system must handle these gracefully.
    """
    description = (
        "Our proxy server is blocking\x07 legitimate traffic to Azure DevOps.\x0c"
        " Multiple development teams\x00 (about 50 engineers) cannot push code "
        "or pull from repos.\x08\x08 The proxy logs show \x1b[31mACCESS DENIED"
        "\x1b[0m for all\x07 *.dev.azure.com domains.\n\n"
        "This started after the\x0c network team applied new filtering rules "
        "this morning. \x00We need this fixed ASAP — we have a production "
        "release\x07 scheduled for tonight and teams can't merge their PRs.\n\n"
        "Proxy: Zscaler ZPA\x00\n"
        "Affected URLs: dev.azure.com/contoso/*\x07\n"
        "Error: 403 \x0cForbidden\x00 — Policy violation"
    )

    return (
        _ticket("INC-DC-0026", "Proxy blocking Azure DevOps\x00 — 50 engineers blocked", description),
        _gold(
            "INC-DC-0026",
            category="Network & Connectivity",
            priority="P1",
            assigned_team="Network Operations",
            needs_escalation=True,
            missing_information=[],
            next_best_action=(
                "Investigate proxy filtering rules blocking Azure DevOps access "
                "for 50 engineers before tonight's production release."
            ),
            remediation_steps=[
                "Review Zscaler ZPA filtering rules applied this morning",
                "Add *.dev.azure.com to the proxy allow list",
                "Verify connectivity to Azure DevOps endpoints after rule change",
                "Coordinate with network team to prevent recurrence in future rule updates",
            ],
        ),
    )


def scenario_minified_code_dump() -> tuple[TicketInput, TriageDecision]:
    """Ticket where a user pasted minified JavaScript code as the description.

    Users sometimes paste browser console output including minified source
    when reporting web application errors. The code is a single enormous
    line with no whitespace.
    """
    # Generate a realistic-looking minified JS blob
    minified_chunks = [
        '!function(e,t){"object"==typeof module&&"object"==typeof module.exports',
        "?module.exports=e.document?t(e,!0):function(e){if(!e.document)throw new",
        'Error("requires a window with a document");return t(e)}:t(e)}',
        '("undefined"!=typeof window?window:this,function(e,t){var n=[],r=Object',
        ".getPrototypeOf,i=n.slice,o=n.flat?function(e){return n.flat.call(e)}",
        ":function(e){return n.concat.apply([],e)},a=n.push,s=n.indexOf,u={}",
        ",l=u.toString,c=u.hasOwnProperty,f=c.toString,p=f.call(Object),d={}",
        ',h=function(e){return"function"==typeof e&&"number"!=typeof e.nodeType',
        '&&"function"!=typeof e.item},g=function(e){return null!=e&&e===e.window}',
        ",v=e.document,m={type:!0,src:!0,nonce:!0,noModule:!0};",
    ]
    minified_js = "".join(minified_chunks) * 8

    description = (
        "The SharePoint intranet portal shows a JavaScript error on every page "
        "load since this morning's update. The page partially renders but all "
        "interactive elements (menus, search, document preview) are broken.\n\n"
        "Browser console output:\n"
        f"Uncaught TypeError: Cannot read properties of undefined (reading 'init')\n"
        f"    at {minified_js[:2000]}...\n\n"
        "About 500 employees use this portal daily. All browsers affected "
        "(Edge, Chrome, Firefox). Tried clearing cache — same error."
    )

    return (
        _ticket(
            "INC-DC-0027",
            "SharePoint portal broken — JS error on every page",
            description,
            channel="portal",
            reporter=Reporter(
                name="IT Web Services",
                email="webservices@contoso.com",
                department="IT",
            ),
        ),
        _gold(
            "INC-DC-0027",
            category="Software & Applications",
            priority="P1",
            assigned_team="Enterprise Applications",
            needs_escalation=True,
            missing_information=["application_version"],
            next_best_action=(
                "Investigate SharePoint portal JavaScript error affecting 500 users after this morning's update."
            ),
            remediation_steps=[
                "Identify the failing JavaScript bundle and the specific update that changed it",
                "Check SharePoint Online service health dashboard for known issues",
                "If caused by a custom solution, roll back the morning's deployment",
                "If caused by a Microsoft update, open a support ticket with Microsoft 365 support",
            ],
        ),
    )


def scenario_mojibake_encoding() -> tuple[TicketInput, TriageDecision]:
    """Ticket with mojibake (garbled encoding) from a charset mismatch.

    Occurs when UTF-8 text is interpreted as Latin-1 or Windows-1252,
    producing characteristic garbled sequences like 'Ã©' for 'é'.
    """
    description = (
        "The email system is displaying garbled characters for all French and "
        "German employees. Here\u00c3\u00a2\u00e2\u0082\u00ac\u00e2\u0084\u00a2s "
        "what we see:\n\n"
        "- Ren\u00c3\u00a9 Dupont\u00c3\u00a2\u00e2\u0082\u00ac\u00e2\u0084\u00a2s "
        "emails show \u00c3\u00a9 instead of \u00e9\n"
        "- The word \u00c3\u00bc for \u00fc (German umlaut)\n"
        "- \u00c3\u00a8 appears instead of \u00e8\n"
        "- Calendar invites show Conf\u00c3\u00a9rence instead of Conf\u00e9rence\n"
        "- The Paris office (Rh\u00c3\u00b4ne-Alpes region) reports "
        "\u00c3\u0080 instead of \u00c0\n\n"
        "This affects about 80 employees across the Paris and Frankfurt offices. "
        "Started after the Exchange migration to the new mail gateway last night. "
        "Email subjects, bodies, and calendar entries are all affected."
    )

    return (
        _ticket(
            "INC-DC-0028",
            "Garbled characters in emails — Paris & Frankfurt offices",
            description,
            channel="email",
            reporter=Reporter(
                name="Pierre Laurent",
                email="pierre.laurent@contoso.com",
                department="European Operations",
            ),
        ),
        _gold(
            "INC-DC-0028",
            category="Software & Applications",
            priority="P2",
            assigned_team="Enterprise Applications",
            missing_information=["configuration_details"],
            next_best_action=(
                "Investigate character encoding mismatch on new mail gateway "
                "affecting 80 employees in Paris and Frankfurt offices."
            ),
            remediation_steps=[
                "Check the new mail gateway's character encoding configuration (should be UTF-8)",
                "Review Exchange transport rules for any encoding transformations",
                "Test with a known UTF-8 encoded email to confirm the encoding path",
                "If gateway misconfigured, update charset settings and re-process queued messages",
            ],
        ),
    )


def scenario_windows_event_log_dump() -> tuple[TicketInput, TriageDecision]:
    """Ticket with verbose Windows Event Viewer XML output pasted in.

    User copied several Event Viewer entries as raw XML. The actual issue—a
    recurring BSOD—is buried among verbose system event noise.
    """
    event_xml_block = (
        '<Event xmlns="http://schemas.microsoft.com/win/2004/08/events/event">\n'
        "  <System>\n"
        '    <Provider Name="Microsoft-Windows-Kernel-Power" '
        'Guid="{331C3B3A-2005-44C2-AC5E-77220C37D6B4}" />\n'
        "    <EventID>41</EventID>\n"
        "    <Version>8</Version>\n"
        "    <Level>1</Level>\n"
        '    <Task>63</Task>\n'
        "    <Opcode>0</Opcode>\n"
        '    <Keywords>0x8000400000000002</Keywords>\n'
        '    <TimeCreated SystemTime="2026-03-18T14:32:07.1234567Z" />\n'
        '    <EventRecordID>98712</EventRecordID>\n'
        '    <Correlation />\n'
        '    <Execution ProcessID="4" ThreadID="8" />\n'
        '    <Channel>System</Channel>\n'
        '    <Computer>WS-FIN-0147.contoso.local</Computer>\n'
        "  </System>\n"
        "  <EventData>\n"
        '    <Data Name="BugcheckCode">209</Data>\n'
        '    <Data Name="BugcheckParameter1">0xfffff80212345678</Data>\n'
        '    <Data Name="BugcheckParameter2">0x2</Data>\n'
        '    <Data Name="BugcheckParameter3">0x0</Data>\n'
        '    <Data Name="BugcheckParameter4">0xfffff80298765432</Data>\n'
        '    <Data Name="SleepInProgress">0</Data>\n'
        '    <Data Name="PowerButtonTimestamp">0</Data>\n'
        '    <Data Name="BootAppStatus">0</Data>\n'
        "  </EventData>\n"
        "</Event>\n"
    )
    description = (
        "My workstation has been blue-screening about 3 times a day since Monday. "
        "I captured the Event Viewer logs — here they are:\n\n"
        + (event_xml_block * 4)
        + '\n<Event xmlns="http://schemas.microsoft.com/win/2004/08/events/event">\n'
        "  <System>\n"
        '    <Provider Name="Microsoft-Windows-WER-SystemErrorReporting" '
        'Guid="{ABCE23E7-DE45-4366-8631-84FA6C525952}" />\n'
        "    <EventID>1001</EventID>\n"
        '    <TimeCreated SystemTime="2026-03-18T14:33:01.9876543Z" />\n'
        '    <Computer>WS-FIN-0147.contoso.local</Computer>\n'
        "  </System>\n"
        "  <EventData>\n"
        '    <Data Name="DumpFile">C:\\Windows\\MEMORY.DMP</Data>\n'
        '    <Data Name="ReportId">a1b2c3d4-e5f6-7890-abcd-ef1234567890</Data>\n'
        "  </EventData>\n"
        "</Event>\n\n"
        "Every time it happens I lose whatever I was working on. The bugcheck "
        "code seems to be 0xD1 (DRIVER_IRQL_NOT_LESS_OR_EQUAL). I'm on a "
        "Dell Precision 5570 with 64 GB RAM running Windows 11 Enterprise 23H2. "
        "Please help — this is blocking my quarter-end financial modelling work."
    )

    return (
        _ticket(
            "INC-DC-0029",
            "Recurring BSOD — Event Viewer logs attached",
            description,
            channel="email",
            reporter=Reporter(
                name="Angela Torres",
                email="angela.torres@contoso.com",
                department="Finance",
            ),
        ),
        _gold(
            "INC-DC-0029",
            category="Hardware & Peripherals",
            priority="P2",
            assigned_team="Endpoint Engineering",
            missing_information=["device_info"],
            next_best_action=(
                "Investigate recurring BSOD (bugcheck 0xD1 DRIVER_IRQL_NOT_LESS_OR_EQUAL) "
                "on Dell Precision 5570 affecting quarter-end finance work."
            ),
            remediation_steps=[
                "Analyse the full memory dump (C:\\Windows\\MEMORY.DMP) to identify the faulting driver",
                "Check for recently updated or known-bad drivers on the Dell Precision 5570",
                "Run Windows Driver Verifier to isolate the offending driver",
                "If a specific driver is identified, roll back or update it; otherwise escalate to Dell support",
            ],
        ),
    )


def scenario_soap_fault_xml() -> tuple[TicketInput, TriageDecision]:
    """Ticket with a full SOAP fault XML envelope pasted in the description.

    User copied the raw SOAP/XML error from a failed web-service call.
    The real issue is that the internal CRM application is returning faults.
    """
    soap_envelope = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">\n'
        "  <soap:Body>\n"
        "    <soap:Fault>\n"
        "      <faultcode>soap:Server</faultcode>\n"
        "      <faultstring>System.ServiceModel.FaultException: "
        "The request channel timed out attempting to send after 00:01:00. "
        "Increase the timeout value passed to the call to Request or increase "
        "the SendTimeout value on the Binding. The time allotted to this "
        "operation may have been a portion of a longer timeout. "
        "---&gt; System.TimeoutException: The HTTP request to "
        "'https://crm-api.contoso.internal/v2/CustomerLookup.svc' has "
        "exceeded the allotted timeout of 00:01:00.\n"
        "   at System.ServiceModel.Channels.HttpChannelFactory.HttpRequestChannel"
        ".SendRequest(Message message, TimeSpan timeout)\n"
        "   at System.ServiceModel.Channels.RequestChannel.Request(Message message, "
        "TimeSpan timeout)\n"
        "   --- End of inner exception stack trace ---</faultstring>\n"
        "      <detail>\n"
        "        <ExceptionDetail xmlns=\"http://schemas.datacontract.org/2004/07/System\">\n"
        "          <HelpLink />\n"
        "          <InnerException>\n"
        "            <HelpLink />\n"
        "            <Message>The HTTP request has exceeded the allotted timeout.</Message>\n"
        "            <StackTrace>   at System.Net.HttpWebRequest.GetResponse()\n"
        "   at System.ServiceModel.Channels.HttpChannelFactory.HttpRequestChannel"
        ".SendRequest(Message message, TimeSpan timeout)</StackTrace>\n"
        "            <Type>System.TimeoutException</Type>\n"
        "          </InnerException>\n"
        "          <Message>The request channel timed out.</Message>\n"
        "          <Type>System.ServiceModel.FaultException</Type>\n"
        "        </ExceptionDetail>\n"
        "      </detail>\n"
        "    </soap:Fault>\n"
        "  </soap:Body>\n"
        "</soap:Envelope>\n"
    )
    description = (
        "Hi team,\n\n"
        "Our CRM application (Customer 360 Portal) is failing whenever we try "
        "to look up a customer record. The whole sales floor is affected — about "
        "35 people can't do customer look-ups right now.\n\n"
        "When we click 'Search Customer' we get a blank screen and our developer "
        "found this in the browser network tab:\n\n"
        + soap_envelope
        + "\nThis started around 09:15 this morning. We haven't deployed any "
        "changes since last Thursday. Could the backend service be down?\n\n"
        "Regards,\nMartin Cheng\nSales Operations"
    )

    return (
        _ticket(
            "INC-DC-0030",
            "CRM customer lookup failing — SOAP timeout error",
            description,
            channel="portal",
            reporter=Reporter(
                name="Martin Cheng",
                email="martin.cheng@contoso.com",
                department="Sales Operations",
            ),
        ),
        _gold(
            "INC-DC-0030",
            category="Software & Applications",
            priority="P2",
            assigned_team="Enterprise Applications",
            missing_information=["environment_details"],
            next_best_action=(
                "Investigate SOAP timeout on CRM CustomerLookup service "
                "affecting 35 sales-floor users since 09:15."
            ),
            remediation_steps=[
                "Check health and availability of the CRM backend service (crm-api.contoso.internal)",
                "Review application and IIS logs on the CRM server around 09:15 for errors or resource exhaustion",
                "Verify network connectivity between the web front-end and the CRM API tier",
                "If the backend service is healthy, increase the WCF SendTimeout as a temporary workaround while root cause is investigated",
            ],
        ),
    )


def scenario_syslog_flood() -> tuple[TicketInput, TriageDecision]:
    """Ticket flooded with hundreds of syslog-formatted log lines.

    The user pasted raw syslog output from a file server. The real issue
    is that the file server is critically low on disk space.
    """
    syslog_lines = []
    for i in range(120):
        ts_sec = 7 + (i % 53)
        facility = ["kernel", "systemd", "smbd", "auditd", "cron"][i % 5]
        messages = [
            "EXT4-fs warning (device sda1): ext4_dx_add_entry: Directory index full!",
            "systemd[1]: Started Session 4821 of user svc_backup.",
            "smbd[18432]: pwrite_sendfile: sendfile not available. Falling back to normal write.",
            "auditd[982]: Audit daemon rotating log files",
            "CRON[29104]: (svc_etl) CMD (/opt/contoso/etl/run_nightly.sh)",
        ]
        syslog_lines.append(
            f"Mar 18 14:22:{ts_sec:02d} FS-PROD-01 {facility}: {messages[i % 5]}"
        )
    syslog_block = "\n".join(syslog_lines)

    description = (
        "URGENT — the main file server FS-PROD-01 is throwing errors left and "
        "right. I pulled the syslog and here it is:\n\n"
        + syslog_block
        + "\n\nI also checked disk space and got this:\n\n"
        "Filesystem      Size  Used Avail Use% Mounted on\n"
        "/dev/sda1       2.0T  1.97T  28G  99% /\n"
        "/dev/sdb1       4.0T  3.99T  8.2G 100% /data\n\n"
        "The /data partition is completely full. Users are reporting they can't "
        "save files to the shared drives. This is production file storage for the "
        "entire trading desk — about 150 users. Please treat as critical!"
    )

    return (
        _ticket(
            "INC-DC-0031",
            "File server FS-PROD-01 — disk full, users can't save",
            description,
            channel="phone",
            reporter=Reporter(
                name="Kyle Nakamura",
                email="kyle.nakamura@contoso.com",
                department="Infrastructure",
            ),
        ),
        _gold(
            "INC-DC-0031",
            category="Data & Storage",
            priority="P1",
            assigned_team="Data Platform",
            needs_escalation=True,
            missing_information=[],
            next_best_action=(
                "Immediately free disk space on FS-PROD-01 /data partition "
                "(100% full) to restore file access for 150 trading-desk users."
            ),
            remediation_steps=[
                "Identify and remove or archive large/stale files on /data to free immediate space",
                "Check for runaway log files or failed backup snapshots consuming space",
                "Expand the /data volume or add additional storage if available",
                "Implement disk-usage monitoring and alerting to prevent recurrence",
            ],
        ),
    )


def scenario_duplicate_ticket_concatenation() -> tuple[TicketInput, TriageDecision]:
    """Same issue submitted three times by a frustrated user, all concatenated.

    Simulates a ticketing system that merged duplicate submissions into one
    long description with repeated content and timestamps.
    """
    submission_1 = (
        "[Submitted: 2026-03-18 08:05 SGT]\n"
        "Subject: Badge reader not working at main entrance\n\n"
        "Hi, the badge reader at the Singapore office main entrance (Block A, "
        "ground floor) is not working. I tapped my badge multiple times and it "
        "just shows a red light. I had to get security to let me in. Can someone "
        "please look at this?\n\n"
        "Thanks,\nPreethi Rajaram\n"
    )
    submission_2 = (
        "[Submitted: 2026-03-18 08:47 SGT]\n"
        "Subject: RE: Badge reader STILL not working\n\n"
        "Following up on my earlier ticket — the badge reader at the main "
        "entrance to Block A is still not working. Several other colleagues are "
        "also affected. We are all queuing up waiting for security to manually "
        "open the door. It's been over 40 minutes now. This is the MAIN entrance "
        "to the building!\n\n"
        "Preethi\n"
    )
    submission_3 = (
        "[Submitted: 2026-03-18 09:33 SGT]\n"
        "Subject: URGENT — badge reader broken, third time reporting\n\n"
        "I have now submitted this THREE times. The badge reader at the Block A "
        "main entrance in our Singapore office is STILL broken. Red light every "
        "time. Over 20 people have been affected this morning. Security is "
        "manually buzzing everyone in, which is a fire-safety concern because "
        "we have no accurate headcount.\n\n"
        "Please escalate this immediately.\n\n"
        "Preethi Rajaram\n"
        "Ext. 4821\n"
    )
    description = (
        "--- Merged duplicate submissions ---\n\n"
        + submission_1
        + "---\n\n"
        + submission_2
        + "---\n\n"
        + submission_3
    )

    return (
        _ticket(
            "INC-DC-0032",
            "Badge reader not working — Singapore Block A entrance (x3 submissions)",
            description,
            channel="portal",
            reporter=Reporter(
                name="Preethi Rajaram",
                email="preethi.rajaram@contoso.com",
                department="Operations",
            ),
        ),
        _gold(
            "INC-DC-0032",
            category="Hardware & Peripherals",
            priority="P3",
            assigned_team="Endpoint Engineering",
            missing_information=["device_info"],
            next_best_action=(
                "Dispatch on-site support to inspect and repair the badge reader "
                "at Singapore Block A main entrance."
            ),
            remediation_steps=[
                "Verify the badge reader hardware status and power supply on-site",
                "Check the access-control system backend for connectivity or configuration issues",
                "Test with a known-good badge to rule out per-badge problems",
                "If hardware fault confirmed, arrange replacement reader and restore access logging",
            ],
        ),
    )


def scenario_corrupted_json() -> tuple[TicketInput, TriageDecision]:
    """Ticket with truncated/corrupted JSON from an API response pasted in.

    The JSON has unterminated strings, missing closing brackets, and
    trailing garbage. The actual issue is that the internal trading
    platform API is returning malformed data.
    """
    corrupted_json = (
        '{"meta":{"api_version":"2.4.1","request_id":"f47ac10b-58cc","timestamp":'
        '"2026-03-18T11:42:07Z"},"data":{"trades":[{"trade_id":"TRD-992714",'
        '"instrument":"CONTOSO-BOND-2028","side":"BUY","quantity":500000,'
        '"price":98.375,"currency":"USD","status":"PENDING","counterparty":'
        '{"id":"CP-8812","name":"Globex Capital Partners","lei":"549300EXAMPLE'
        'LEICODE00"},{"trade_id":"TRD-992715","instrument":"CONTOSO-EQ-PREF",'
        '"side":"SELL","quantity":125000,"price":42.18,"currency":"USD",'
        '"status":"FILL\x00\x00\x00ED","counterparty":{"id":"CP-1147","name":'
        '"Initech Investments","lei":"2138001EXAMPLELEI"},"settlement_date":'
        '"2026-03-20","trader":"jsmith@contoso.com","desk":"Fixed Income",'
        '"book":"FI-NORTH-AM","exec_broker":{"id":"EB-443","name":"Woodgrove '
        'Securities","m\n\n'
        "--- response truncated; connection reset by peer ---"
    )
    description = (
        "CRITICAL — Our Contoso Trading Platform (CTP) API is returning "
        "corrupted JSON responses to the front-end. Traders on the Fixed Income "
        "desk noticed that order confirmations are coming back garbled and the "
        "UI is showing a blank screen.\n\n"
        "Here is the raw response body we captured from the /v2/trades endpoint:\n\n"
        + corrupted_json
        + "\n\nAs you can see the JSON is cut off mid-field and has null bytes "
        "embedded in it. This is affecting all 12 Fixed Income traders and they "
        "cannot confirm or settle trades. We're in the middle of a heavy "
        "trading day — we need this fixed ASAP.\n\n"
        "API endpoint: https://ctp-api.contoso.internal/v2/trades\n"
        "Environment: Production\n"
        "First observed: 2026-03-18 11:40 ET"
    )

    return (
        _ticket(
            "INC-DC-0033",
            "Trading Platform API returning corrupted JSON — traders blocked",
            description,
            channel="phone",
            reporter=Reporter(
                name="Jason Smith",
                email="jason.smith@contoso.com",
                department="Fixed Income Trading",
            ),
        ),
        _gold(
            "INC-DC-0033",
            category="Software & Applications",
            priority="P1",
            assigned_team="Enterprise Applications",
            needs_escalation=True,
            missing_information=["error_message"],
            next_best_action=(
                "Investigate corrupted JSON responses from CTP /v2/trades API "
                "blocking 12 Fixed Income traders in production."
            ),
            remediation_steps=[
                "Check CTP API server logs for errors, crashes, or out-of-memory conditions around 11:40 ET",
                "Verify network path between API servers and load balancer for packet corruption or premature resets",
                "Restart the affected API service instances if they are in a degraded state",
                "If a recent deployment caused the issue, initiate a rollback to the last known-good version",
            ],
        ),
    )


def scenario_registry_export_dump() -> tuple[TicketInput, TriageDecision]:
    """Ticket with a Windows registry (.reg) export pasted in.

    User exported a large section of the registry and pasted it. The real
    issue is that an Outlook add-in won't load after a group policy update.
    """
    reg_lines = [
        "Windows Registry Editor Version 5.00\n",
        "[HKEY_CURRENT_USER\\Software\\Microsoft\\Office\\16.0\\Outlook\\Resiliency\\DoNotDisableAddinList]\n",
        '"ContosoExpensePlugin"=dword:00000001\n',
        '"ContosoComplianceAddin"=dword:00000001\n',
        '"UCAddin.UCAddin.1"=dword:00000001\n\n',
        "[HKEY_CURRENT_USER\\Software\\Microsoft\\Office\\16.0\\Outlook\\Resiliency\\DisabledItems]\n",
    ]
    for i in range(30):
        reg_lines.append(
            f'"item{i}"=hex:04,00,00,00,{i:02x},ab,cd,ef,01,23,45,67,89,ab,cd,ef,'
            f"00,00,00,00,{i + 10:02x},00,00,00\n"
        )
    reg_lines.append("\n")
    reg_lines.append(
        "[HKEY_LOCAL_MACHINE\\SOFTWARE\\Policies\\Microsoft\\Office\\16.0\\Outlook\\Resiliency\\AddinList]\n"
    )
    for name in [
        "ContosoExpensePlugin",
        "ContosoComplianceAddin",
        "ContosoTravelBooking",
        "ContosoHRPortalHelper",
        "UCAddin.UCAddin.1",
        "Microsoft.VbaAddinForOutlook",
    ]:
        reg_lines.append(f'"{name}"=dword:00000001\n')
    reg_lines.append("\n")
    reg_lines.append(
        "[HKEY_LOCAL_MACHINE\\SOFTWARE\\Policies\\Microsoft\\Office\\16.0\\Outlook\\Security]\n"
    )
    reg_lines.append('"EnableUnsafeClientMailRules"=dword:00000000\n')
    reg_lines.append('"AdminSecurityMode"=dword:00000003\n')
    reg_lines.append('"AllowActiveXOneOffForms"=dword:00000000\n')

    registry_dump = "".join(reg_lines)

    description = (
        "After the latest group policy push last night, the Contoso Expense "
        "Plugin add-in for Outlook has stopped loading. When I go to File > "
        "Options > Add-ins it shows the add-in as 'Inactive'. I tried enabling "
        "it manually but it gets disabled again on next restart.\n\n"
        "I exported the relevant registry keys — please see below:\n\n"
        + registry_dump
        + "\nI'm on Outlook Version 2402 (Build 17328.20162) running on Windows "
        "11 Enterprise. About 200 users in the Accounting department use this "
        "add-in for expense reports. I'm guessing the GP push added something "
        "to DisabledItems? Please advise."
    )

    return (
        _ticket(
            "INC-DC-0034",
            "Outlook Expense Plugin disabled after group policy push",
            description,
            channel="email",
            reporter=Reporter(
                name="Linda Park",
                email="linda.park@contoso.com",
                department="Accounting",
            ),
        ),
        _gold(
            "INC-DC-0034",
            category="Software & Applications",
            priority="P3",
            assigned_team="Endpoint Engineering",
            missing_information=["configuration_details"],
            next_best_action=(
                "Review the group policy change that is disabling the Contoso "
                "Expense Plugin add-in for Outlook across Accounting (200 users)."
            ),
            remediation_steps=[
                "Review the latest GPO changes affecting Office 16.0 Outlook add-in resiliency settings",
                "Check the DisabledItems registry key for entries matching the Contoso Expense Plugin",
                "Update the GPO to add ContosoExpensePlugin to the DoNotDisableAddinList or AddinList",
                "Force a gpupdate on a test machine and verify the add-in remains active after restart",
            ],
        ),
    )


def scenario_powershell_verbose_output() -> tuple[TicketInput, TriageDecision]:
    """Ticket with verbose PowerShell Get-Service / Get-Process output.

    The user ran diagnostic commands and pasted all output. The real issue
    is that the SQL Server service keeps stopping on a production DB server.
    """
    service_header = (
        "Status   Name               DisplayName\n"
        "------   ----               -----------\n"
    )
    services = [
        ("Running", "AdobeARMservice   ", "Adobe Acrobat Update Service"),
        ("Running", "BrokerInfrastru...", "Background Tasks Infrastructure Ser..."),
        ("Running", "CDPSvc            ", "Connected Devices Platform Service"),
        ("Running", "CryptSvc          ", "Cryptographic Services"),
        ("Running", "DcomLaunch        ", "DCOM Server Process Launcher"),
        ("Running", "Dhcp              ", "DHCP Client"),
        ("Running", "DiagTrack         ", "Connected User Experiences and Telem..."),
        ("Running", "Dnscache          ", "DNS Client"),
        ("Running", "EventLog          ", "Windows Event Log"),
        ("Running", "LanmanServer      ", "Server"),
        ("Running", "LanmanWorkstation ", "Workstation"),
        ("Stopped", "MSSQLSERVER       ", "SQL Server (MSSQLSERVER)"),
        ("Stopped", "SQLSERVERAGENT    ", "SQL Server Agent (MSSQLSERVER)"),
        ("Running", "MpsSvc            ", "Windows Defender Firewall"),
        ("Running", "Netlogon          ", "Netlogon"),
        ("Running", "PlugPlay          ", "Plug and Play"),
        ("Running", "RpcSs             ", "Remote Procedure Call (RPC)"),
        ("Running", "SamSs             ", "Security Accounts Manager"),
        ("Running", "Schedule          ", "Task Scheduler"),
        ("Running", "Spooler           ", "Print Spooler"),
        ("Running", "W32Time           ", "Windows Time"),
        ("Running", "WinRM             ", "Windows Remote Management (WS-Manag..."),
        ("Running", "Winmgmt           ", "Windows Management Instrumentation"),
        ("Running", "wuauserv          ", "Windows Update"),
    ]
    service_lines = service_header + "\n".join(
        f"{status:<8} {name} {display}" for status, name, display in services
    )

    process_header = (
        "\nHandles  NPM(K)    PM(K)      WS(K)     CPU(s)     Id  SI ProcessName\n"
        "-------  ------    -----      -----     ------     --  -- -----------\n"
    )
    processes = [
        "    142      10    12344      18992       2.31   4512   0 csrss",
        "    812      45   198432     245120     184.72   2288   0 sqlservr",
        "    234      18    34212      42880      12.44   3104   0 svchost",
        "    567      32    89100     102400      45.67   1820   0 lsass",
        "    123       8     8432      11200       0.89   5560   1 taskhostw",
        "    345      22    56780      67840      23.11   2904   0 svchost",
        "    198      14    23456      31200       5.67   3440   0 WmiPrvSE",
        "    432      28    72344      88960      34.56   1568   0 services",
    ]
    process_lines = process_header + "\n".join(processes)

    event_output = (
        "\nPS C:\\> Get-EventLog -LogName Application -Source MSSQLSERVER -Newest 5\n\n"
        "   Index Time          EntryType   Source                 InstanceID Message\n"
        "   ----- ----          ---------   ------                 ---------- -------\n"
        "   48823 Mar 18 14:12  Error       MSSQLSERVER                17058 initerrlog: Could not open...\n"
        "   48820 Mar 18 14:12  Error       MSSQLSERVER                17058 The error log has been rein...\n"
        "   48817 Mar 18 13:45  Error       MSSQLSERVER                 9001 The log for database 'Conto...\n"
        "   48814 Mar 18 13:45  Information MSSQLSERVER                17162 SQL Server is starting at n...\n"
        "   48811 Mar 18 12:30  Error       MSSQLSERVER                 9001 The log for database 'Conto...\n"
    )

    description = (
        "The SQL Server on DB-PROD-03 keeps stopping and we've restarted it "
        "three times today already. It runs for about an hour then dies. This "
        "is the production database server for the Contoso Settlements system "
        "— all trade settlement processing is down.\n\n"
        "Here's the output of the commands I ran:\n\n"
        "PS C:\\> Get-Service | Format-Table -AutoSize\n\n"
        + service_lines
        + "\n\n"
        + "PS C:\\> Get-Process | Sort-Object CPU -Descending | Select-Object -First 8\n"
        + process_lines
        + "\n"
        + event_output
        + "\nAs you can see MSSQLSERVER and SQLSERVERAGENT are both Stopped. "
        "The event log shows error 9001 on the ContosoSettlements database. "
        "Please help — settlements are backing up!"
    )

    return (
        _ticket(
            "INC-DC-0035",
            "SQL Server keeps stopping on DB-PROD-03 — settlements down",
            description,
            channel="phone",
            reporter=Reporter(
                name="Derek Olsen",
                email="derek.olsen@contoso.com",
                department="Database Administration",
            ),
        ),
        _gold(
            "INC-DC-0035",
            category="Data & Storage",
            priority="P1",
            assigned_team="Data Platform",
            needs_escalation=True,
            missing_information=[],
            next_best_action=(
                "Investigate recurring SQL Server crashes on DB-PROD-03 "
                "(error 9001 on ContosoSettlements database) blocking trade settlement processing."
            ),
            remediation_steps=[
                "Review the SQL Server error log for the root cause of the repeated service stops",
                "Check disk health and available space on the volumes hosting the ContosoSettlements database and transaction log",
                "Verify the database integrity with DBCC CHECKDB on ContosoSettlements",
                "Restart the SQL Server service and monitor; if instability persists, fail over to the DR instance",
            ],
        ),
    )


def scenario_ics_calendar_content() -> tuple[TicketInput, TriageDecision]:
    """Ticket where the user pasted raw iCalendar (.ics) content.

    The user received a calendar invite that Outlook won't open, so they
    pasted the raw .ics text into the ticket.
    """
    ics_content = (
        "BEGIN:VCALENDAR\n"
        "VERSION:2.0\n"
        "PRODID:-//Globex Corp//Meeting Scheduler v3.2//EN\n"
        "CALSCALE:GREGORIAN\n"
        "METHOD:REQUEST\n"
        "BEGIN:VTIMEZONE\n"
        "TZID:America/New_York\n"
        "BEGIN:STANDARD\n"
        "DTSTART:20251102T020000\n"
        "RRULE:FREQ=YEARLY;BYMONTH=11;BYDAY=1SU\n"
        "TZOFFSETFROM:-0400\n"
        "TZOFFSETTO:-0500\n"
        "TZNAME:EST\n"
        "END:STANDARD\n"
        "BEGIN:DAYLIGHT\n"
        "DTSTART:20250309T020000\n"
        "RRULE:FREQ=YEARLY;BYMONTH=3;BYDAY=2SU\n"
        "TZOFFSETFROM:-0500\n"
        "TZOFFSETTO:-0400\n"
        "TZNAME:EDT\n"
        "END:DAYLIGHT\n"
        "END:VTIMEZONE\n"
        "BEGIN:VEVENT\n"
        "DTSTART;TZID=America/New_York:20260325T140000\n"
        "DTEND;TZID=America/New_York:20260325T153000\n"
        "DTSTAMP:20260318T092000Z\n"
        "ORGANIZER;CN=Sarah Chen:mailto:sarah.chen@globexcorp.com\n"
        "UID:a1b2c3d4-e5f6-7890-abcd-ef1234567890@globexcorp.com\n"
        "ATTENDEE;CUTYPE=INDIVIDUAL;ROLE=REQ-PARTICIPANT;PARTSTAT=NEEDS-ACTION;"
        "RSVP=TRUE;CN=James Whitfield:mailto:james.whitfield@contoso.com\n"
        "ATTENDEE;CUTYPE=INDIVIDUAL;ROLE=REQ-PARTICIPANT;PARTSTAT=NEEDS-ACTION;"
        "RSVP=TRUE;CN=Maria Santos:mailto:maria.santos@contoso.com\n"
        "ATTENDEE;CUTYPE=INDIVIDUAL;ROLE=OPT-PARTICIPANT;PARTSTAT=NEEDS-ACTION;"
        "RSVP=TRUE;CN=Tom Baker:mailto:tom.baker@contoso.com\n"
        "SUMMARY:Q1 Partnership Review — Contoso / Globex\n"
        "DESCRIPTION:Quarterly review of the Contoso-Globex strategic partnership.\\n"
        "\\nAgenda:\\n1. Revenue update\\n2. Joint product roadmap\\n3. Support escalation process\\n"
        "\\nDial-in: +1-555-0147\\nPasscode: 882914#\\n\n"
        "LOCATION:Globex HQ — Room 14B (or dial in)\n"
        "STATUS:CONFIRMED\n"
        "SEQUENCE:0\n"
        "END:VEVENT\n"
        "END:VCALENDAR\n"
    )
    description = (
        "I've been receiving calendar invites from our external partner Globex Corp "
        "but Outlook refuses to open them. When I double-click the .ics attachment, "
        "nothing happens. Other people on my team (Maria Santos, Tom Baker) have "
        "the same problem.\n\n"
        "I opened the .ics file in Notepad and here's what it contains:\n\n"
        + ics_content
        + "\nThis has been happening for about a week with all Globex invites. "
        "Invites from internal Contoso users work fine. We have an important "
        "quarterly review meeting next Wednesday that we need to get on our calendars."
    )

    return (
        _ticket(
            "INC-DC-0036",
            "Can't open external calendar invites from Globex Corp",
            description,
            channel="email",
            reporter=Reporter(
                name="James Whitfield",
                email="james.whitfield@contoso.com",
                department="Business Development",
            ),
        ),
        _gold(
            "INC-DC-0036",
            category="Software & Applications",
            priority="P3",
            assigned_team="Enterprise Applications",
            missing_information=["application_version"],
            next_best_action=(
                "Investigate why Outlook is unable to process .ics calendar invites "
                "from the external domain globexcorp.com."
            ),
            remediation_steps=[
                "Verify Outlook iCalendar processing settings and test with a manually crafted .ics file",
                "Check Exchange transport rules or mail-flow policies that may strip or block .ics attachments from external senders",
                "Test the specific .ics file by importing it directly via File > Open & Export in Outlook",
                "If a transport rule is blocking, add an exception for the globexcorp.com domain",
            ],
        ),
    )


def scenario_pdf_to_text_artifacts() -> tuple[TicketInput, TriageDecision]:
    """Ticket with garbled text from a failed PDF-to-text extraction.

    Columns, headers, page numbers, and body text are all scrambled
    together. The real issue is that the invoice processing system is
    failing to parse incoming vendor invoices.
    """
    garbled_text = (
        "C O N T O S O   F I N A N C I A L   S E R V I C E S\n"
        "                                                I N V O I C E\n"
        "Page 1 of 3         Invoice #: INV-2026-88412         Date: 03/15/2026\n\n"
        "Vendor:  Woodgrove       Bill To: Contoso Financial\n"
        "         Supplies Inc             Services\n"
        "         1234 Oak Ave             One Contoso Way\n"
        "         Suite 500                Redmond, WA 98052\n"
        "         Portland, OR\n\n"
        "Qty   Description                     Unit Price    Total\n"
        "---   -----------                     ----------    -----\n"
        " 50   Ergonomic Keyboard Model EK-    $    89.99    $  4,499.50\n"
        "      200 (USB-C, backlit)\n"
        " 25   Wireless Mouse WM-150           $    34.50    $    862.50\n"
        "Page 2 of 3\n"
        " 10   USB-C Docking Station DS-       $   249.00    $  2,490.00\n"
        "      Pro (dual 4K output)\n"
        "100   Cat6a Patch Cable 5ft           $     4.75    $    475.00\n"
        " 15   27\" 4K Monitor MN-2700          $   399.00    $  5,985.00\n"
        "                                      Subtotal:     $ 14,312.00\n"
        "                                      Tax (8.5%):   $  1,216.52\n"
        "                                      TOTAL:        $ 15,528.52\n"
        "Page 3 of 3\n"
        "Payment Terms: Net 30\n"
        "Due Date: 04/14/2026\n"
        "    R e m i t t a n c e   I n f o r m a t i o n\n"
        "    Bank: First National Bank\n"
        "    Routing: 021000021\n"
        "    Account: ****7890\n\n"
        "T h a n k   y o u   f o r   y o u r   b u s i n e s s !\n"
    )
    description = (
        "The automated invoice processing system (Contoso AP Automation) has "
        "been failing to parse invoices since yesterday afternoon. When we check "
        "the processing queue, all invoices from Woodgrove Supplies are stuck in "
        "'Parse Error' state.\n\n"
        "I extracted the text from one of the failing PDFs and here's what the "
        "system is seeing:\n\n"
        + garbled_text
        + "\nAs you can see, the text extraction is producing spaced-out headers, "
        "page breaks are injected mid-table, and the columns are misaligned. We "
        "have 47 invoices stuck in the queue totalling over $380,000 in payables "
        "that are approaching their due dates.\n\n"
        "The OCR/text-extraction module was updated to version 4.2.1 on Monday. "
        "This might be related."
    )

    return (
        _ticket(
            "INC-DC-0037",
            "Invoice processing failing — PDF text extraction garbled",
            description,
            channel="portal",
            reporter=Reporter(
                name="Samantha Lee",
                email="samantha.lee@contoso.com",
                department="Accounts Payable",
            ),
        ),
        _gold(
            "INC-DC-0037",
            category="Software & Applications",
            priority="P2",
            assigned_team="Enterprise Applications",
            missing_information=["application_version"],
            next_best_action=(
                "Investigate PDF text-extraction failures in Contoso AP Automation "
                "after OCR module update to v4.2.1; 47 invoices stuck."
            ),
            remediation_steps=[
                "Compare OCR module v4.2.1 output with v4.1.x on the same sample invoices to confirm regression",
                "If regression confirmed, roll back the OCR module to v4.1.x and re-process the stuck invoices",
                "Report the parsing issue to the OCR module vendor with sample PDFs",
                "Implement validation checks on extracted text to catch garbled output before it enters the processing queue",
            ],
        ),
    )


def scenario_enormous_cc_list() -> tuple[TicketInput, TriageDecision]:
    """Ticket where email headers with 80+ CC recipients are pasted in.

    The user's actual issue is that emails to large distribution lists
    are failing to deliver, but the description is dominated by the
    massive CC list.
    """
    cc_recipients = []
    departments = [
        "sales", "marketing", "finance", "legal", "hr", "engineering",
        "ops", "support", "compliance", "risk", "trading", "research",
    ]
    for i in range(84):
        dept = departments[i % len(departments)]
        cc_recipients.append(f"{dept}.user{i + 1:03d}@contoso.com")
    cc_block = "; ".join(cc_recipients)

    description = (
        "I'm trying to send an important compliance update to all department heads "
        "but the email keeps bouncing back with a delivery failure notice. Here are "
        "the full email headers:\n\n"
        "From: compliance.officer@contoso.com\n"
        "To: all-department-heads@contoso.com\n"
        f"CC: {cc_block}\n"
        "Subject: [ACTION REQUIRED] Q1 2026 Compliance Attestation Deadline — March 25\n"
        "Date: Wed, 18 Mar 2026 09:00:00 -0500\n"
        "Message-ID: <20260318090000.ABC123@mail.contoso.com>\n"
        "MIME-Version: 1.0\n"
        "Content-Type: multipart/mixed; boundary=\"----=_Part_12345\"\n"
        "X-Mailer: Microsoft Outlook 16.0\n"
        'X-MS-Exchange-Organization-SCL: -1\n'
        "X-MS-Exchange-Organization-AuthSource: EXCH-PROD-01.contoso.local\n\n"
        "The bounce-back error says:\n"
        "  550 5.1.3 Invalid address — recipient list exceeds maximum allowed "
        "recipients per message (max: 500, attempted: 847)\n\n"
        "I need to get this compliance attestation out to everyone before the "
        "March 25 deadline. Is there a way to increase the limit or split the "
        "delivery automatically?"
    )

    return (
        _ticket(
            "INC-DC-0038",
            "Email delivery failure — recipient limit exceeded for compliance notice",
            description,
            channel="email",
            reporter=Reporter(
                name="Rebecca Thornton",
                email="rebecca.thornton@contoso.com",
                department="Compliance",
            ),
        ),
        _gold(
            "INC-DC-0038",
            category="Software & Applications",
            priority="P2",
            assigned_team="Enterprise Applications",
            missing_information=[],
            next_best_action=(
                "Assist with delivery of compliance attestation email that is "
                "exceeding the Exchange per-message recipient limit (847 vs 500 max)."
            ),
            remediation_steps=[
                "Use a distribution group or dynamic distribution list instead of individual CC recipients",
                "If a higher limit is needed, review and adjust the Exchange transport rule MaxRecipientEnvelopeLimit",
                "Split the communication into batches using the compliance team's mailing tool",
                "Confirm successful delivery of the compliance attestation before the March 25 deadline",
            ],
        ),
    )


def scenario_nested_quoted_replies() -> tuple[TicketInput, TriageDecision]:
    """Ticket with deeply nested quoted email replies (8+ levels).

    A long chain of `>` quoted replies obscures the real issue:
    shared mailbox permissions were lost.
    """
    description = (
        "Hi IT,\n\n"
        "The shared mailbox permissions are definitely gone. See the thread below.\n\n"
        "—\n\n"
        "> On Mar 18, 2026, at 09:12, Nadia Kowalski wrote:\n"
        ">\n"
        "> I just checked and I can't access it either. Looks like all of us lost access.\n"
        ">\n"
        "> > On Mar 18, 2026, at 09:05, Brian Murphy wrote:\n"
        "> >\n"
        "> > Same here — I get 'You don't have permission to open this mailbox' when\n"
        "> > I click on ap-invoices@contoso.com in Outlook. Was fine on Friday.\n"
        "> >\n"
        "> > > On Mar 18, 2026, at 08:58, Yuki Tanaka wrote:\n"
        "> > >\n"
        "> > > Has anyone else lost access to the AP Invoices shared mailbox?\n"
        "> > > I can't open it this morning.\n"
        "> > >\n"
        "> > > > On Mar 17, 2026, at 17:45, IT Notifications wrote:\n"
        "> > > >\n"
        "> > > > Scheduled maintenance: Exchange mailbox database migration\n"
        "> > > > will occur tonight between 22:00 and 02:00 ET. Brief\n"
        "> > > > interruptions to mailbox access may occur.\n"
        "> > > >\n"
        "> > > > > On Mar 17, 2026, at 16:30, Diana Reyes wrote:\n"
        "> > > > >\n"
        "> > > > > Reminder: please make sure all urgent invoices are processed\n"
        "> > > > > before end of day in case the maintenance causes any issues.\n"
        "> > > > >\n"
        "> > > > > > On Mar 17, 2026, at 15:00, Brian Murphy wrote:\n"
        "> > > > > >\n"
        "> > > > > > Will do. I've got 12 invoices left to process.\n"
        "> > > > > >\n"
        "> > > > > > > On Mar 17, 2026, at 14:22, Nadia Kowalski wrote:\n"
        "> > > > > > >\n"
        "> > > > > > > Team, IT just announced Exchange maintenance tonight.\n"
        "> > > > > > > Let's make sure we're all caught up.\n"
        "> > > > > > >\n"
        "> > > > > > > > On Mar 17, 2026, at 14:00, IT Notifications wrote:\n"
        "> > > > > > > >\n"
        "> > > > > > > > [AUTOMATED] Exchange maintenance window scheduled.\n"
        "> > > > > > > > All shared mailboxes may be briefly unavailable.\n"
        "> > > > > > > > No action required from end users.\n\n"
        "So it looks like the maintenance last night broke our permissions. "
        "The AP Invoices shared mailbox (ap-invoices@contoso.com) is used by "
        "5 people in Accounts Payable: myself (Diana Reyes), Nadia Kowalski, "
        "Brian Murphy, Yuki Tanaka, and Sam Patel. None of us can access it.\n\n"
        "We have invoices due for payment by end of week. Please restore our "
        "access ASAP.\n\n"
        "Thanks,\n"
        "Diana Reyes\n"
        "Accounts Payable Lead"
    )

    return (
        _ticket(
            "INC-DC-0039",
            "Shared mailbox permissions lost after Exchange maintenance",
            description,
            channel="email",
            reporter=Reporter(
                name="Diana Reyes",
                email="diana.reyes@contoso.com",
                department="Accounts Payable",
            ),
        ),
        _gold(
            "INC-DC-0039",
            category="Access & Authentication",
            priority="P2",
            assigned_team="Identity & Access Management",
            missing_information=[],
            next_best_action=(
                "Restore shared mailbox permissions for ap-invoices@contoso.com "
                "for 5 Accounts Payable users lost during Exchange maintenance."
            ),
            remediation_steps=[
                "Verify current permissions on the ap-invoices@contoso.com shared mailbox in Exchange Admin Center",
                "Re-grant FullAccess and SendAs permissions for the 5 affected AP users",
                "Investigate the mailbox database migration scripts to determine why permissions were stripped",
                "Add a post-maintenance validation step to check shared mailbox permissions in future change windows",
            ],
        ),
    )


def scenario_sql_query_dump() -> tuple[TicketInput, TriageDecision]:
    """Ticket where the user pasted SQL queries they were running.

    The user copied several complex SQL statements to show what they were
    doing when the database started timing out. The actual issue is
    database performance degradation.
    """
    sql_queries = (
        "-- Query 1: Daily settlement reconciliation\n"
        "SELECT\n"
        "    t.trade_id,\n"
        "    t.instrument_code,\n"
        "    t.trade_date,\n"
        "    t.settlement_date,\n"
        "    t.quantity,\n"
        "    t.price,\n"
        "    t.quantity * t.price AS notional_value,\n"
        "    t.counterparty_id,\n"
        "    cp.counterparty_name,\n"
        "    cp.lei_code,\n"
        "    s.status AS settlement_status,\n"
        "    s.settled_amount,\n"
        "    s.settlement_currency,\n"
        "    CASE\n"
        "        WHEN s.settled_amount != t.quantity * t.price\n"
        "        THEN 'BREAK'\n"
        "        ELSE 'MATCHED'\n"
        "    END AS recon_status\n"
        "FROM dbo.Trades t\n"
        "INNER JOIN dbo.Counterparties cp ON t.counterparty_id = cp.counterparty_id\n"
        "LEFT JOIN dbo.Settlements s ON t.trade_id = s.trade_id\n"
        "WHERE t.trade_date = '2026-03-17'\n"
        "    AND t.instrument_type IN ('BOND', 'EQUITY', 'FX_FORWARD')\n"
        "ORDER BY t.settlement_date, t.instrument_code;\n\n"
        "-- Query 2: Outstanding position summary\n"
        "SELECT\n"
        "    p.book_id,\n"
        "    b.book_name,\n"
        "    b.desk,\n"
        "    p.instrument_code,\n"
        "    i.instrument_name,\n"
        "    i.asset_class,\n"
        "    SUM(p.quantity) AS net_position,\n"
        "    SUM(p.quantity * p.avg_price) AS total_cost_basis,\n"
        "    SUM(p.quantity * m.last_price) AS market_value,\n"
        "    SUM(p.quantity * m.last_price) - SUM(p.quantity * p.avg_price) AS unrealized_pnl\n"
        "FROM dbo.Positions p\n"
        "INNER JOIN dbo.Books b ON p.book_id = b.book_id\n"
        "INNER JOIN dbo.Instruments i ON p.instrument_code = i.instrument_code\n"
        "INNER JOIN dbo.MarketData m ON p.instrument_code = m.instrument_code\n"
        "    AND m.price_date = '2026-03-17'\n"
        "GROUP BY p.book_id, b.book_name, b.desk, p.instrument_code,\n"
        "    i.instrument_name, i.asset_class\n"
        "HAVING SUM(p.quantity) != 0\n"
        "ORDER BY b.desk, b.book_name, i.asset_class;\n\n"
        "-- Query 3: Compliance daily limit check\n"
        "SELECT\n"
        "    b.desk,\n"
        "    b.book_name,\n"
        "    cl.limit_type,\n"
        "    cl.limit_value,\n"
        "    CASE cl.limit_type\n"
        "        WHEN 'NOTIONAL' THEN SUM(t.quantity * t.price)\n"
        "        WHEN 'TRADE_COUNT' THEN CAST(COUNT(*) AS DECIMAL(18,2))\n"
        "        WHEN 'NET_EXPOSURE' THEN SUM(CASE t.side\n"
        "            WHEN 'BUY' THEN t.quantity * t.price\n"
        "            WHEN 'SELL' THEN -t.quantity * t.price END)\n"
        "    END AS current_usage,\n"
        "    CASE\n"
        "        WHEN CASE cl.limit_type\n"
        "            WHEN 'NOTIONAL' THEN SUM(t.quantity * t.price)\n"
        "            WHEN 'TRADE_COUNT' THEN CAST(COUNT(*) AS DECIMAL(18,2))\n"
        "            WHEN 'NET_EXPOSURE' THEN SUM(CASE t.side\n"
        "                WHEN 'BUY' THEN t.quantity * t.price\n"
        "                WHEN 'SELL' THEN -t.quantity * t.price END)\n"
        "        END > cl.limit_value THEN 'BREACHED'\n"
        "        ELSE 'WITHIN_LIMIT'\n"
        "    END AS limit_status\n"
        "FROM dbo.Trades t\n"
        "INNER JOIN dbo.Books b ON t.book_id = b.book_id\n"
        "INNER JOIN dbo.ComplianceLimits cl ON b.book_id = cl.book_id\n"
        "WHERE t.trade_date = '2026-03-17'\n"
        "GROUP BY b.desk, b.book_name, cl.limit_type, cl.limit_value\n"
        "ORDER BY limit_status DESC, b.desk;\n"
    )
    description = (
        "The ContosoSettlements database on DB-PROD-02 has been extremely slow "
        "since about 08:00 this morning. Queries that normally take 2-3 seconds "
        "are now taking over 90 seconds or timing out entirely.\n\n"
        "Here are the queries I was running when the timeouts started:\n\n"
        + sql_queries
        + "\nQuery 1 used to run in about 1.5 seconds — it's now timing out at "
        "the 120-second mark. Query 2 ran for 94 seconds before returning. "
        "Query 3 timed out completely.\n\n"
        "I checked sys.dm_exec_requests and there are 47 blocked sessions. "
        "The wait types are mostly LCK_M_S and PAGEIOLATCH_SH.\n\n"
        "This is affecting the morning reconciliation process for all desks. "
        "About 30 users across Fixed Income, Equities, and FX are impacted.\n\n"
        "Server: DB-PROD-02\\SQLPROD01\n"
        "Database: ContosoSettlements\n"
        "SQL Server 2022 CU12"
    )

    return (
        _ticket(
            "INC-DC-0040",
            "Database severe performance degradation — ContosoSettlements on DB-PROD-02",
            description,
            channel="portal",
            reporter=Reporter(
                name="Ahmed Hassan",
                email="ahmed.hassan@contoso.com",
                department="Trade Operations",
            ),
        ),
        _gold(
            "INC-DC-0040",
            category="Data & Storage",
            priority="P2",
            assigned_team="Data Platform",
            missing_information=[],
            next_best_action=(
                "Investigate database performance degradation on DB-PROD-02 "
                "ContosoSettlements with 47 blocked sessions affecting 30 users across trading desks."
            ),
            remediation_steps=[
                "Identify the head blocker among the 47 blocked sessions using sys.dm_exec_requests and sys.dm_os_waiting_tasks",
                "Check for long-running transactions or uncommitted changes holding locks",
                "Review PAGEIOLATCH_SH waits for potential disk I/O bottleneck or memory pressure",
                "If a runaway query is identified, terminate it and consider adding missing indexes to prevent recurrence",
            ],
        ),
    )


# ── New scenarios (INC-DC-5001 through INC-DC-5010) ──────────────────


def scenario_docker_container_logs() -> tuple[TicketInput, TriageDecision]:
    """Ticket with Docker container log output pasted as the description.

    Tests that the system extracts the actual issue (OOM-killed API service)
    from noisy container runtime logs rather than being confused by the
    structured log format, timestamps, and repeated restart messages.
    """
    description = (
        "Docker logs from our production trade-execution API:\n\n"
        "2026-03-18T09:14:23.456Z [INFO]  trade-api | Starting service on port 8080...\n"
        "2026-03-18T09:14:23.890Z [INFO]  trade-api | Connected to Redis cache at redis-prod-01:6379\n"
        "2026-03-18T09:14:24.112Z [INFO]  trade-api | Database pool initialized (min=5, max=50)\n"
        "2026-03-18T09:14:24.334Z [INFO]  trade-api | Health check endpoint registered at /healthz\n"
        "2026-03-18T09:14:25.001Z [INFO]  trade-api | Processing backlog: 1,247 pending orders\n"
        "2026-03-18T09:15:01.223Z [WARN]  trade-api | Memory usage at 78% (3.12GB / 4GB limit)\n"
        "2026-03-18T09:15:45.891Z [WARN]  trade-api | GC pressure detected, pausing 340ms\n"
        "2026-03-18T09:16:02.112Z [ERROR] trade-api | Memory usage at 94% (3.76GB / 4GB limit)\n"
        "2026-03-18T09:16:03.001Z [ERROR] trade-api | java.lang.OutOfMemoryError: Java heap space\n"
        "2026-03-18T09:16:03.002Z [ERROR] trade-api |   at com.contoso.trading.OrderProcessor.processBatch(OrderProcessor.java:247)\n"
        "2026-03-18T09:16:03.003Z [ERROR] trade-api |   at com.contoso.trading.Engine.run(Engine.java:89)\n"
        "2026-03-18T09:16:03.500Z [FATAL] trade-api | Container killed by OOM killer (exit code 137)\n"
        "--- Container restarted (attempt 3/5) ---\n"
        "2026-03-18T09:16:10.100Z [INFO]  trade-api | Starting service on port 8080...\n"
        "2026-03-18T09:16:10.890Z [INFO]  trade-api | Connected to Redis cache at redis-prod-01:6379\n"
        "2026-03-18T09:16:35.200Z [WARN]  trade-api | Memory usage at 72% after 25s\n"
        "2026-03-18T09:17:01.456Z [FATAL] trade-api | Container killed by OOM killer (exit code 137)\n"
        "--- Container restarted (attempt 4/5) ---\n"
        "--- Container restarted (attempt 5/5) ---\n"
        "2026-03-18T09:18:30.001Z [FATAL] trade-api | Max restart attempts reached. Container stopped.\n\n"
        "This has been happening since the 9am deployment. The trade execution API keeps "
        "crashing with OOM errors and orders are not being processed. Trading desk is impacted."
    )
    reporter = Reporter(
        name="Raj Patel",
        email="raj.patel@contoso.com",
        department="Platform Engineering",
    )
    ticket = _ticket(
        "INC-DC-5001",
        "API container keeps restarting - OOM kills",
        description,
        channel="chat",
        reporter=reporter,
    )
    gold = _gold(
        "INC-DC-5001",
        category="Software & Applications",
        priority="P1",
        assigned_team="Enterprise Applications",
        missing_information=["application_version", "environment_details"],
        next_best_action=(
            "Investigate the Java OutOfMemoryError in the trade-execution API container. "
            "The 9am deployment likely introduced a memory leak in OrderProcessor.processBatch. "
            "Roll back the deployment immediately while investigating."
        ),
        remediation_steps=[
            "Roll back the trade-execution API to the previous known-good image tag",
            "Increase container memory limit temporarily to 8GB to restore service",
            "Analyze heap dumps from the OOM events to identify the memory leak",
            "Review the OrderProcessor.processBatch changes in the 9am deployment",
            "Implement proper batch-size limits and memory-aware processing",
        ],
    )
    return ticket, gold


def scenario_kubernetes_pod_yaml() -> tuple[TicketInput, TriageDecision]:
    """Ticket with Kubernetes pod YAML manifest and kubectl describe output.

    Tests that the system identifies the actual issue (CrashLoopBackOff
    due to wrong image tag) from verbose K8s resource descriptions.
    """
    description = (
        "kubectl describe pod client-portal-api-7f8d9c6b4-xk2mj -n production:\n\n"
        "Name:         client-portal-api-7f8d9c6b4-xk2mj\n"
        "Namespace:    production\n"
        "Priority:     0\n"
        "Node:         aks-nodepool1-12345678-vmss000002/10.240.0.6\n"
        "Start Time:   Mon, 18 Mar 2026 08:30:00 +0000\n"
        "Labels:       app=client-portal-api\n"
        "              pod-template-hash=7f8d9c6b4\n"
        "              version=v2.4.1\n"
        "Status:       Running\n"
        "IP:           10.244.2.15\n"
        "Containers:\n"
        "  api:\n"
        "    Container ID:  containerd://abc123def456\n"
        "    Image:         contosoacr.azurecr.io/client-portal-api:v2.4.1-hotfix-typo\n"
        "    Image ID:      contosoacr.azurecr.io/client-portal-api@sha256:deadbeef\n"
        "    Port:          8443/TCP\n"
        "    State:         Waiting\n"
        "      Reason:      CrashLoopBackOff\n"
        "    Last State:    Terminated\n"
        "      Reason:      Error\n"
        "      Exit Code:   1\n"
        "      Started:     Mon, 18 Mar 2026 09:42:15 +0000\n"
        "      Finished:    Mon, 18 Mar 2026 09:42:16 +0000\n"
        "    Ready:         False\n"
        "    Restart Count: 47\n"
        "Events:\n"
        "  Type     Reason     Message\n"
        "  ----     ------     -------\n"
        "  Normal   Scheduled  Successfully assigned production/client-portal-api-7f8d9c6b4\n"
        "  Normal   Pulled     Container image pulled successfully\n"
        "  Warning  BackOff    Back-off restarting failed container\n"
        "  Warning  BackOff    Back-off 5m0s restarting failed container\n\n"
        "The client portal has been down since the hotfix deployment this morning. "
        "The image tag 'v2.4.1-hotfix-typo' doesn't exist in our registry — someone "
        "fat-fingered the tag name in the Helm values. Should be 'v2.4.1-hotfix'."
    )
    reporter = Reporter(
        name="Kenji Tanaka",
        email="kenji.tanaka@contoso.com",
        department="DevOps",
    )
    ticket = _ticket(
        "INC-DC-5002",
        "Client portal CrashLoopBackOff after hotfix deploy",
        description,
        channel="portal",
        reporter=reporter,
    )
    gold = _gold(
        "INC-DC-5002",
        category="Software & Applications",
        priority="P2",
        assigned_team="Enterprise Applications",
        missing_information=["affected_users", "business_impact"],
        next_best_action=(
            "Fix the container image tag in the Helm chart from "
            "'v2.4.1-hotfix-typo' to 'v2.4.1-hotfix' and redeploy."
        ),
        remediation_steps=[
            "Correct the image tag in Helm values to 'v2.4.1-hotfix'",
            "Run helm upgrade to deploy the corrected configuration",
            "Verify the pod enters Running state with restart count reset",
            "Confirm the client portal is accessible and healthy",
        ],
    )
    return ticket, gold


def scenario_terraform_plan_output() -> tuple[TicketInput, TriageDecision]:
    """Ticket with full terraform plan output showing infrastructure changes.

    Tests that the system identifies the critical DNS change buried in
    a large terraform plan with dozens of resource modifications.
    """
    plan_lines = [
        "Terraform will perform the following actions:\n",
        "  # azurerm_resource_group.prod will be updated in-place",
        '  ~ resource "azurerm_resource_group" "prod" {',
        '      ~ tags = {',
        '          + "cost_center" = "CC-4521"',
        "        }",
        "    }\n",
    ]
    for i in range(1, 16):
        plan_lines.append(f"  # azurerm_storage_account.data_{i:02d} will be updated in-place")
        plan_lines.append(f'  ~ resource "azurerm_storage_account" "data_{i:02d}" {{')
        plan_lines.append(f'      ~ tags = {{ + "env" = "production" }}')
        plan_lines.append("    }\n")
    plan_lines.extend([
        "  # azurerm_dns_a_record.trading_api will be DESTROYED and re-created",
        '  -/+ resource "azurerm_dns_a_record" "trading_api" {',
        '      ~ name    = "api.trading" -> "api-v2.trading"',
        '      ~ records = ["10.0.1.50"] -> ["10.0.2.100"]',
        '      ~ ttl     = 300 -> 60',
        "    }\n",
        "  # azurerm_dns_cname_record.trading_web will be DESTROYED",
        '  - resource "azurerm_dns_cname_record" "trading_web" {',
        '      - name   = "trading.contoso.internal"',
        '      - record = "api.trading.contoso.internal"',
        "    }\n",
        "Plan: 2 to add, 18 to change, 2 to destroy.\n",
    ])
    description = (
        "Hi team,\n\n"
        "We're about to apply this terraform plan for the Q2 infrastructure update. "
        "Can someone review? I'm worried about the DNS changes — the trading API "
        "record is being destroyed and recreated with a new IP, and the CNAME for "
        "trading.contoso.internal is being removed entirely. This will break all "
        "trading platform connectivity if applied during market hours.\n\n"
        + "\n".join(plan_lines)
        + "\nThis needs urgent review before the change window at 6pm tonight."
    )
    reporter = Reporter(
        name="Sarah Kim",
        email="sarah.kim@contoso.com",
        department="Infrastructure",
    )
    ticket = _ticket(
        "INC-DC-5003",
        "REVIEW NEEDED: Terraform plan destroying trading DNS records",
        description,
        reporter=reporter,
    )
    gold = _gold(
        "INC-DC-5003",
        category="Network & Connectivity",
        priority="P1",
        assigned_team="Network Operations",
        needs_escalation=True,
        missing_information=["affected_users", "business_impact"],
        next_best_action=(
            "Block the terraform apply until the DNS changes are reviewed. "
            "Destroying the trading API DNS record and CNAME during market hours "
            "will cause a production outage for the trading platform."
        ),
        remediation_steps=[
            "Put a hold on the terraform apply until after market close",
            "Review the DNS record changes with the trading platform team",
            "Plan DNS migration with a staged cutover to avoid downtime",
            "Pre-create the new DNS records before destroying old ones",
            "Schedule the change window for after-hours with rollback plan",
        ],
    )
    return ticket, gold


def scenario_git_diff_in_ticket() -> tuple[TicketInput, TriageDecision]:
    """Ticket with git diff output pasted as the description.

    Tests that the system identifies the SSO configuration change
    buried in a large unified diff.
    """
    description = (
        "After yesterday's deployment (commit abc1234), SSO login is broken for "
        "all users. Here's the relevant diff:\n\n"
        "```diff\n"
        "diff --git a/config/auth/sso.yaml b/config/auth/sso.yaml\n"
        "index 1a2b3c4..5d6e7f8 100644\n"
        "--- a/config/auth/sso.yaml\n"
        "+++ b/config/auth/sso.yaml\n"
        "@@ -12,8 +12,8 @@ sso:\n"
        "   provider: azure-ad\n"
        "   tenant_id: ${AZURE_TENANT_ID}\n"
        "-  client_id: ${SSO_CLIENT_ID}\n"
        "-  redirect_uri: https://portal.contoso.com/auth/callback\n"
        "+  client_id: 00000000-0000-0000-0000-000000000000\n"
        "+  redirect_uri: https://portal-staging.contoso.com/auth/callback\n"
        "   scopes:\n"
        "     - openid\n"
        "     - profile\n"
        "diff --git a/src/middleware/auth.ts b/src/middleware/auth.ts\n"
        "index 9a8b7c6..3d2e1f0 100644\n"
        "--- a/src/middleware/auth.ts\n"
        "+++ b/src/middleware/auth.ts\n"
        "@@ -45,7 +45,7 @@ export class AuthMiddleware {\n"
        "   private validateToken(token: string): boolean {\n"
        "-    return this.verifier.verify(token, { audience: this.config.clientId });\n"
        "+    return true; // TODO: fix token validation in staging\n"
        "   }\n"
        "```\n\n"
        "Someone accidentally pushed staging config to production. The client_id is "
        "hardcoded to zeros and the redirect goes to staging. Plus the token validation "
        "is completely disabled! Everyone is getting 'Authentication failed' errors."
    )
    reporter = Reporter(
        name="Marcus Chen",
        email="marcus.chen@contoso.com",
        department="Security Engineering",
    )
    ticket = _ticket(
        "INC-DC-5004",
        "SSO broken after yesterday's deployment - wrong config pushed",
        description,
        channel="chat",
        reporter=reporter,
    )
    gold = _gold(
        "INC-DC-5004",
        category="Access & Authentication",
        priority="P2",
        assigned_team="Identity & Access Management",
        missing_information=["affected_users"],
        next_best_action=(
            "Immediately revert commit abc1234 to restore the correct SSO configuration. "
            "The disabled token validation is a critical security vulnerability."
        ),
        remediation_steps=[
            "Revert the deployment to restore the correct SSO client_id and redirect_uri",
            "Re-enable token validation immediately (the TODO bypass is a security hole)",
            "Audit access logs during the window when token validation was disabled",
            "Implement pre-deployment config validation to prevent staging config leaks",
        ],
    )
    return ticket, gold


def scenario_pem_certificate_chain() -> tuple[TicketInput, TriageDecision]:
    """Ticket with PEM certificate chain pasted in the email body.

    Tests that the system identifies the expiring certificate issue
    despite the large block of base64 certificate data.
    """
    fake_cert = "MIIFazCCA1OgAwIBAgIUE" + "A" * 200 + "="
    description = (
        "URGENT: Our wildcard SSL certificate for *.trading.contoso.com expires "
        "TOMORROW (March 19, 2026). The renewal request has been stuck in "
        "approvals for 3 weeks.\n\n"
        "Current cert chain for reference:\n\n"
        "-----BEGIN CERTIFICATE-----\n"
        f"{fake_cert}\n"
        "-----END CERTIFICATE-----\n"
        "-----BEGIN CERTIFICATE-----\n"
        f"MIIEtjCCA56gAwIBAgIQ{'B' * 200}=\n"
        "-----END CERTIFICATE-----\n"
        "-----BEGIN CERTIFICATE-----\n"
        f"MIIDrzCCApegAwIBAgIQ{'C' * 200}=\n"
        "-----END CERTIFICATE-----\n\n"
        "Services affected if this expires:\n"
        "- Trading API (api.trading.contoso.com)\n"
        "- Client Portal (portal.trading.contoso.com)\n"
        "- Real-time Market Feed (feed.trading.contoso.com)\n"
        "- Settlement Gateway (settle.trading.contoso.com)\n\n"
        "This will cause a COMPLETE trading platform outage if not renewed today. "
        "The cert is managed through DigiCert and needs VP-level approval to renew."
    )
    reporter = Reporter(
        name="Elena Rodriguez",
        email="elena.rodriguez@contoso.com",
        department="Security Operations",
    )
    ticket = _ticket(
        "INC-DC-5005",
        "CRITICAL: Wildcard SSL cert expires tomorrow - trading platform at risk",
        description,
        reporter=reporter,
    )
    gold = _gold(
        "INC-DC-5005",
        category="Security & Compliance",
        priority="P1",
        assigned_team="Security Operations",
        needs_escalation=True,
        next_best_action=(
            "Expedite the SSL certificate renewal approval immediately. "
            "If the wildcard cert for *.trading.contoso.com expires, "
            "all trading platform services will be unavailable."
        ),
        remediation_steps=[
            "Escalate the certificate renewal approval to VP level immediately",
            "Generate a new CSR and submit to DigiCert for expedited issuance",
            "Prepare the certificate deployment pipeline for all trading services",
            "Test the new certificate in staging before production rollout",
            "Set up automated certificate expiry monitoring and alerting at 30/14/7 days",
        ],
    )
    return ticket, gold


def scenario_raw_mime_multipart() -> tuple[TicketInput, TriageDecision]:
    """Ticket with raw MIME multipart email content including boundaries.

    Tests that the system extracts the Outlook crash issue from
    raw email source with MIME headers and encoded content.
    """
    description = (
        "Content-Type: multipart/mixed;\n"
        '    boundary="----=_Part_12345_67890.1710752400000"\n'
        "MIME-Version: 1.0\n"
        "From: jsmith@contoso.com\n"
        "To: helpdesk@contoso.com\n"
        "Subject: Outlook crashes\n"
        "Date: Mon, 18 Mar 2026 10:00:00 +0000\n\n"
        "------=_Part_12345_67890.1710752400000\n"
        "Content-Type: text/plain; charset=UTF-8\n"
        "Content-Transfer-Encoding: quoted-printable\n\n"
        "Hi, my Outlook keeps crashing whenever I try to open emails from the "
        "legal department. It=E2=80=99s been happening since the March update. "
        "I get an error dialog that says =E2=80=9CMicrosoft Outlook has stopped "
        "working=E2=80=9D and then it restarts. This happens about 10 times a day "
        "and I=E2=80=99m losing unsaved draft emails each time.\n\n"
        "I=E2=80=99ve tried repairing the Office installation and creating a new "
        "Outlook profile but neither helped. Running Outlook 365 version 2402 "
        "Build 17328.20162 on Windows 11.\n\n"
        "------=_Part_12345_67890.1710752400000\n"
        "Content-Type: application/octet-stream;\n"
        '    name="outlook_crash_dump.dmp"\n'
        "Content-Transfer-Encoding: base64\n"
        "Content-Disposition: attachment;\n"
        '    filename="outlook_crash_dump.dmp"\n\n'
        "TVqQAAMAAAAEAAAA//8AALgAAAAAAAAAQAAAAAAAAAAAAAAAAAAAAAAAA"
        "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAEAAQAAAAAAQAAIAAAAAAAAAAAAAA"
        "AAAAAEAAAAAAAgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA==\n\n"
        "------=_Part_12345_67890.1710752400000--\n"
    )
    reporter = Reporter(
        name="James Smith",
        email="jsmith@contoso.com",
        department="Legal Operations",
    )
    ticket = _ticket(
        "INC-DC-5006",
        "Outlook crashes when opening legal dept emails",
        description,
        channel="email",
        reporter=reporter,
    )
    gold = _gold(
        "INC-DC-5006",
        category="Software & Applications",
        priority="P3",
        assigned_team="Enterprise Applications",
        missing_information=["error_message", "steps_to_reproduce"],
        next_best_action=(
            "Investigate the Outlook crash on version 2402 Build 17328.20162 "
            "when opening emails from the legal department. "
            "Check for known issues with the March update."
        ),
        remediation_steps=[
            "Analyze the crash dump file for the specific exception causing the crash",
            "Check for known issues with Outlook 365 version 2402 and the March update",
            "Test opening legal department emails in OWA to isolate whether it is a desktop client issue",
            "If a known bug, apply the latest Office update or rollback to the previous build",
        ],
    )
    return ticket, gold


def scenario_dns_zone_file() -> tuple[TicketInput, TriageDecision]:
    """Ticket with DNS zone file records dumped in the description.

    Tests that the system identifies the DNS resolution failure from
    a dump of zone file records.
    """
    zone_records = "\n".join([
        "; Zone file for contoso.internal",
        "$TTL 86400",
        "$ORIGIN contoso.internal.",
        "@       IN  SOA  ns1.contoso.internal. admin.contoso.internal. (",
        "                 2026031801 ; Serial",
        "                 3600       ; Refresh",
        "                 900        ; Retry",
        "                 604800     ; Expire",
        "                 86400 )    ; Minimum TTL",
        "",
        "@           IN  NS   ns1.contoso.internal.",
        "@           IN  NS   ns2.contoso.internal.",
        "ns1         IN  A    10.0.0.10",
        "ns2         IN  A    10.0.0.11",
        "",
        "; Production services",
        "db-prod-01  IN  A    10.0.1.20",
        "db-prod-02  IN  A    10.0.1.21",
        "api-prod    IN  A    10.0.1.50",
        "web-prod    IN  CNAME  api-prod.contoso.internal.",
        "mail        IN  MX   10 mail.contoso.internal.",
        "mail        IN  A    10.0.2.10",
        "",
        "; *** THESE RECORDS APPEAR CORRUPTED ***",
        "trading     IN  A    0.0.0.0",
        "settlement  IN  A    0.0.0.0",
        "compliance  IN  A    0.0.0.0",
        "",
        "; Staging (should not resolve from prod network)",
        "stg-api     IN  A    172.16.0.50",
        "stg-web     IN  A    172.16.0.51",
    ])
    description = (
        "All internal DNS lookups for *.contoso.internal are intermittently failing. "
        "The trading, settlement, and compliance services have been unreachable since "
        "8:00 AM. I pulled the zone file from ns1 and noticed the records are pointing "
        "to 0.0.0.0:\n\n"
        f"{zone_records}\n\n"
        "Someone or something zeroed out the A records for the three critical financial "
        "services. The secondary DNS (ns2) has the same corruption. We need to restore "
        "the correct records ASAP — the London office can't access trading at all."
    )
    reporter = Reporter(
        name="Thomas Wright",
        email="thomas.wright@contoso.com",
        department="Network Engineering",
    )
    ticket = _ticket(
        "INC-DC-5007",
        "DNS records corrupted - trading/settlement/compliance unreachable",
        description,
        channel="phone",
        reporter=reporter,
    )
    gold = _gold(
        "INC-DC-5007",
        category="Network & Connectivity",
        priority="P2",
        assigned_team="Network Operations",
        missing_information=["timestamp"],
        next_best_action=(
            "Immediately restore the correct A records for trading, settlement, and compliance "
            "services on both ns1 and ns2. Investigate how the records were zeroed out."
        ),
        remediation_steps=[
            "Restore the trading, settlement, and compliance A records from the last known-good backup",
            "Verify DNS resolution from multiple locations after the fix",
            "Investigate how both primary and secondary DNS were corrupted simultaneously",
            "Review DNS change logs and access audit trails for unauthorized modifications",
            "Implement DNS record change alerting and approval workflows",
        ],
    )
    return ticket, gold


def scenario_packet_capture_text() -> tuple[TicketInput, TriageDecision]:
    """Ticket with tcpdump/Wireshark text output showing network issues.

    Tests that the system identifies the high-latency database connectivity
    issue from packet capture text output.
    """
    description = (
        "We're seeing terrible latency to the settlement database. Here's a tcpdump "
        "capture showing the TCP retransmissions:\n\n"
        "09:30:01.234567 IP 10.0.1.100.54321 > 10.0.1.21.1433: Flags [S], seq 1234567890, win 65535\n"
        "09:30:01.234890 IP 10.0.1.21.1433 > 10.0.1.100.54321: Flags [S.], seq 9876543210, ack 1234567891\n"
        "09:30:01.235001 IP 10.0.1.100.54321 > 10.0.1.21.1433: Flags [.], ack 1, win 65535\n"
        "09:30:01.235500 IP 10.0.1.100.54321 > 10.0.1.21.1433: Flags [P.], seq 1:245, ack 1\n"
        "09:30:02.236000 IP 10.0.1.100.54321 > 10.0.1.21.1433: Flags [P.], seq 1:245, ack 1  [TCP Retransmission]\n"
        "09:30:04.237000 IP 10.0.1.100.54321 > 10.0.1.21.1433: Flags [P.], seq 1:245, ack 1  [TCP Retransmission]\n"
        "09:30:08.238000 IP 10.0.1.100.54321 > 10.0.1.21.1433: Flags [P.], seq 1:245, ack 1  [TCP Retransmission]\n"
        "09:30:08.238500 IP 10.0.1.21.1433 > 10.0.1.100.54321: Flags [.], ack 245, win 65535\n"
        "09:30:08.239000 IP 10.0.1.21.1433 > 10.0.1.100.54321: Flags [P.], seq 1:1460, ack 245\n"
        "09:30:08.239100 IP 10.0.1.21.1433 > 10.0.1.100.54321: Flags [P.], seq 1460:2048, ack 245\n\n"
        "--- TCP conversation summary ---\n"
        "Total packets: 847\n"
        "Retransmissions: 312 (36.8%)\n"
        "Average RTT: 3,200ms (expected: <5ms)\n"
        "Packet loss: ~15%\n"
        "Source: 10.0.1.100 (settlement-api-prod)\n"
        "Destination: 10.0.1.21 (db-prod-02, SQL Server)\n\n"
        "The settlement system is timing out on every third transaction because the "
        "DB queries take 7+ seconds instead of the normal <100ms. This is causing "
        "trade settlement failures. Started around 8:30 AM today."
    )
    reporter = Reporter(
        name="Lisa Park",
        email="lisa.park@contoso.com",
        department="Settlement Operations",
    )
    ticket = _ticket(
        "INC-DC-5008",
        "High latency to settlement DB - 36% packet retransmission",
        description,
        channel="portal",
        reporter=reporter,
    )
    gold = _gold(
        "INC-DC-5008",
        category="Network & Connectivity",
        priority="P2",
        assigned_team="Network Operations",
        missing_information=["network_location"],
        next_best_action=(
            "Investigate the network path between settlement-api-prod (10.0.1.100) "
            "and db-prod-02 (10.0.1.21) for the source of 36.8% packet retransmission "
            "and 3200ms RTT. This is causing trade settlement failures."
        ),
        remediation_steps=[
            "Check switch/router interfaces on the path between 10.0.1.100 and 10.0.1.21 for errors or congestion",
            "Verify no recent network changes (VLAN, firewall rules, QoS policies) around 8:30 AM",
            "Check for NIC errors or driver issues on both the settlement API server and DB server",
            "If a faulty switch port or cable is identified, failover to redundant path",
            "Monitor packet loss and RTT after remediation to confirm resolution",
        ],
    )
    return ticket, gold


def scenario_deeply_nested_java_exception() -> tuple[TicketInput, TriageDecision]:
    """Ticket with a 200+ line deeply nested Java exception chain.

    Tests that the system identifies the root cause (connection pool
    exhaustion) from a deeply nested 'Caused by:' exception chain
    spanning Spring, Hibernate, HikariCP, and JDBC layers.
    """
    exception_chain = (
        "Exception in thread \"main\" org.springframework.web.util.NestedServletException: "
        "Request processing failed; nested exception is "
        "org.springframework.dao.DataAccessResourceFailureException: could not extract ResultSet\n"
        "\tat org.springframework.web.servlet.FrameworkServlet.processRequest(FrameworkServlet.java:1014)\n"
        "\tat org.springframework.web.servlet.FrameworkServlet.doGet(FrameworkServlet.java:898)\n"
        "\tat javax.servlet.http.HttpServlet.service(HttpServlet.java:626)\n"
        "\tat org.springframework.web.servlet.FrameworkServlet.service(FrameworkServlet.java:883)\n"
        "\tat javax.servlet.http.HttpServlet.service(HttpServlet.java:733)\n"
        "\tat org.apache.catalina.core.ApplicationFilterChain.internalDoFilter(ApplicationFilterChain.java:227)\n"
        "\t... 45 more\n"
        "Caused by: org.springframework.dao.DataAccessResourceFailureException: could not extract ResultSet; "
        "nested exception is org.hibernate.exception.JDBCConnectionException: could not extract ResultSet\n"
        "\tat org.springframework.orm.jpa.vendor.HibernateJpaDialect.convertHibernateAccessException(HibernateJpaDialect.java:276)\n"
        "\tat org.springframework.orm.jpa.vendor.HibernateJpaDialect.translateExceptionIfPossible(HibernateJpaDialect.java:233)\n"
        "\tat org.springframework.orm.jpa.AbstractEntityManagerFactoryBean.translateExceptionIfPossible(AbstractEntityManagerFactoryBean.java:551)\n"
        "\t... 58 more\n"
        "Caused by: org.hibernate.exception.JDBCConnectionException: could not extract ResultSet\n"
        "\tat org.hibernate.exception.internal.SQLStateConversionDelegate.convert(SQLStateConversionDelegate.java:115)\n"
        "\tat org.hibernate.exception.internal.StandardSQLExceptionConverter.convert(StandardSQLExceptionConverter.java:56)\n"
        "\tat org.hibernate.engine.jdbc.spi.SqlExceptionHelper.convert(SqlExceptionHelper.java:109)\n"
        "\t... 72 more\n"
        "Caused by: com.zaxxer.hikari.pool.HikariPool$PoolInitializationException: "
        "Failed to initialize pool: Cannot create PoolableConnectionFactory\n"
        "\tat com.zaxxer.hikari.pool.HikariPool.throwPoolInitializationException(HikariPool.java:596)\n"
        "\tat com.zaxxer.hikari.pool.HikariPool.checkFailFast(HikariPool.java:582)\n"
        "\tat com.zaxxer.hikari.pool.HikariPool.<init>(HikariPool.java:115)\n"
        "\t... 80 more\n"
        "Caused by: java.sql.SQLTransientConnectionException: HikariPool-1 - Connection is not available, "
        "request timed out after 30000ms. Active: 50, Idle: 0, Waiting: 247\n"
        "\tat com.zaxxer.hikari.pool.HikariPool.createTimeoutException(HikariPool.java:695)\n"
        "\tat com.zaxxer.hikari.pool.HikariPool.getConnection(HikariPool.java:197)\n"
        "\tat com.zaxxer.hikari.pool.HikariPool.getConnection(HikariPool.java:162)\n"
        "\t... 95 more\n"
        "Caused by: com.microsoft.sqlserver.jdbc.SQLServerException: "
        "The connection to the host 10.0.1.20, named instance contosofinance has failed. "
        "Error: \"java.net.SocketTimeoutException: connect timed out\"\n"
        "\tat com.microsoft.sqlserver.jdbc.SQLServerConnection.connectHelper(SQLServerConnection.java:2568)\n"
        "\tat com.microsoft.sqlserver.jdbc.SQLServerConnection.login(SQLServerConnection.java:2234)\n"
        "\tat com.microsoft.sqlserver.jdbc.SQLServerConnection.connect(SQLServerConnection.java:1210)\n"
        "\t... 102 more\n"
    )
    description = (
        "The portfolio management service is completely down. Here are the logs:\n\n"
        f"{exception_chain}\n"
        "HikariPool is at max capacity (50 active, 0 idle, 247 waiting). "
        "The root cause looks like the SQL Server instance on 10.0.1.20 "
        "(contosofinance) is unreachable. All 50 connections are stuck "
        "waiting for the DB to respond. This is blocking all portfolio "
        "valuations and the EOD risk reports can't run."
    )
    reporter = Reporter(
        name="David Okonkwo",
        email="david.okonkwo@contoso.com",
        department="Risk Management",
    )
    ticket = _ticket(
        "INC-DC-5009",
        "Portfolio service down - DB connection pool exhausted",
        description,
        channel="phone",
        reporter=reporter,
    )
    gold = _gold(
        "INC-DC-5009",
        category="Data & Storage",
        priority="P1",
        assigned_team="Data Platform",
        needs_escalation=True,
        missing_information=["timestamp", "environment_details"],
        next_best_action=(
            "Investigate why SQL Server on 10.0.1.20 (contosofinance instance) "
            "is unreachable, causing HikariCP pool exhaustion (50 active, 247 waiting). "
            "This is blocking all portfolio valuations and EOD risk reports."
        ),
        remediation_steps=[
            "Check SQL Server health on 10.0.1.20 — verify the contosofinance instance is running",
            "Check network connectivity between the portfolio service and 10.0.1.20",
            "If the DB server is unresponsive, restart the SQL Server service",
            "Once DB is reachable, restart the portfolio management service to reset the connection pool",
            "Review and potentially increase HikariCP max pool size and add connection timeout failover",
        ],
    )
    return ticket, gold


def scenario_spreadsheet_tab_paste() -> tuple[TicketInput, TriageDecision]:
    """Ticket with tab-delimited spreadsheet data pasted from Excel.

    Tests that the system identifies the bulk permission update request
    from a pasted employee table rather than being confused by the
    tabular formatting.
    """
    rows = [
        "Employee ID\tName\tOld Department\tNew Department\tAccess Level\tStart Date",
        "E10451\tJohnson, Maria\tWealth Mgmt\tTrading Desk\tLevel 3\t2026-04-01",
        "E10452\tWilliams, Robert\tSettlement\tRisk Analytics\tLevel 2\t2026-04-01",
        "E10453\tBrown, Patricia\tCompliance\tTrading Desk\tLevel 3\t2026-04-01",
        "E10454\tDavis, Michael\tIT Support\tSecurity Ops\tLevel 4\t2026-04-01",
        "E10455\tMiller, Jennifer\tHR\tCompliance\tLevel 2\t2026-04-01",
        "E10456\tWilson, James\tTrading Desk\tWealth Mgmt\tLevel 3\t2026-04-01",
        "E10457\tMoore, Linda\tOperations\tSettlement\tLevel 2\t2026-04-01",
        "E10458\tTaylor, William\tRisk Analytics\tCompliance\tLevel 2\t2026-04-01",
        "E10459\tAnderson, Barbara\tWealth Mgmt\tOperations\tLevel 1\t2026-04-01",
        "E10460\tThomas, Richard\tTrading Desk\tRisk Analytics\tLevel 3\t2026-04-01",
        "E10461\tJackson, Susan\tCompliance\tHR\tLevel 2\t2026-04-01",
        "E10462\tWhite, Charles\tSecurity Ops\tIT Support\tLevel 4\t2026-04-01",
        "E10463\tHarris, Jessica\tSettlement\tWealth Mgmt\tLevel 3\t2026-04-01",
        "E10464\tMartin, Mark\tOperations\tTrading Desk\tLevel 3\t2026-04-01",
        "E10465\tGarcia, Nancy\tRisk Analytics\tSettlement\tLevel 2\t2026-04-01",
    ]
    table = "\n".join(rows)
    description = (
        "Hi team,\n\n"
        "We have a Q2 departmental reorganization effective April 1st. "
        "Please update Active Directory group memberships and application "
        "permissions for the following 15 employees. Each person needs to "
        "be removed from their old department's security groups and added "
        "to the new department's groups with the indicated access level.\n\n"
        f"{table}\n\n"
        "The access levels map to our standard permission tiers:\n"
        "- Level 1: Read-only access\n"
        "- Level 2: Read/write for department apps\n"
        "- Level 3: Read/write + trading system access\n"
        "- Level 4: Admin access\n\n"
        "Please ensure this is completed before April 1st. Let me know if "
        "you need the manager approval forms — they're all signed and filed "
        "in ServiceNow under CHG-20260315."
    )
    reporter = Reporter(
        name="Angela Foster",
        email="angela.foster@contoso.com",
        department="Human Resources",
    )
    ticket = _ticket(
        "INC-DC-5010",
        "Q2 reorg - bulk AD permission updates for 15 employees",
        description,
        channel="portal",
        reporter=reporter,
    )
    gold = _gold(
        "INC-DC-5010",
        category="Access & Authentication",
        priority="P3",
        assigned_team="Identity & Access Management",
        missing_information=["affected_users", "business_impact"],
        next_best_action=(
            "Process the bulk Active Directory group membership changes for the "
            "15 employees transferring departments in the Q2 reorganization. "
            "Verify manager approval forms in ServiceNow CHG-20260315."
        ),
        remediation_steps=[
            "Verify all 15 manager approval forms are signed in ServiceNow CHG-20260315",
            "Create a scripted AD group membership update for the 15 employees",
            "Remove users from old department security groups and add to new ones",
            "Update application-level permissions according to the access level mapping",
            "Send confirmation to HR and each employee's new manager by March 31",
        ],
    )
    return ticket, gold


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
        scenario_json_config_dump(),
        scenario_stack_trace_flood(),
        scenario_double_encoded_html_entities(),
        scenario_auto_reply_loop(),
        scenario_binary_hex_dump(),
        scenario_control_characters(),
        scenario_minified_code_dump(),
        scenario_mojibake_encoding(),
        scenario_windows_event_log_dump(),
        scenario_soap_fault_xml(),
        scenario_syslog_flood(),
        scenario_duplicate_ticket_concatenation(),
        scenario_corrupted_json(),
        scenario_registry_export_dump(),
        scenario_powershell_verbose_output(),
        scenario_ics_calendar_content(),
        scenario_pdf_to_text_artifacts(),
        scenario_enormous_cc_list(),
        scenario_nested_quoted_replies(),
        scenario_sql_query_dump(),
        # ── New scenarios (INC-DC-5001 through INC-DC-5010) ──
        scenario_docker_container_logs(),
        scenario_kubernetes_pod_yaml(),
        scenario_terraform_plan_output(),
        scenario_git_diff_in_ticket(),
        scenario_pem_certificate_chain(),
        scenario_raw_mime_multipart(),
        scenario_dns_zone_file(),
        scenario_packet_capture_text(),
        scenario_deeply_nested_java_exception(),
        scenario_spreadsheet_tab_paste(),
    ]
