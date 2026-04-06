# Copyright (c) Microsoft. All rights reserved.
"""Data cleanup evaluation scenarios.

Synthetic tickets that test the triage API's robustness against messy,
real-world input: excessively long descriptions, embedded base64 data,
HTML email content, garbled/corrupted text, Unicode edge cases,
empty/minimal input, and other data quality issues the hidden eval set
may contain.

Each scenario has a gold triage answer so it can be scored with the
same deterministic harness used for the sample and public eval sets.
"""

from ms.evals.models.ticket import Ticket
from ms.evals.models.ticket import TicketReporter
from ms.evals.models.triage import TriageResponse
from ms.evals.scenarios.base import EvalScenario

_LONG_PADDING = (
    " I have tried everything I can think of and nothing works."
    " I restarted my computer, cleared the cache, updated the drivers,"
    " checked the cables, and even reinstalled the application."
    " Still no luck. I really need this fixed urgently."
)

_BASE64_IMAGE_BLOCK = (
    "data:image/png;base64,"
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk"
    "+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="
)

_LARGE_BASE64_BLOCK = "data:image/png;base64," + "A" * 5000


def _html_email_wrapper(content: str, name: str, dept: str, email: str) -> str:
    """Build a realistic HTML email body with embedded content and signature."""
    return (
        '<html><head><meta charset="utf-8"><style>'
        "body{font-family:Calibri,sans-serif;font-size:11pt;}"
        ".signature{color:#666;font-size:9pt;}"
        "</style></head><body>"
        f"<p>{content}</p>"
        '<div class="signature">'
        f"<p>Best regards,<br/>{name}<br/>{dept}<br/>"
        f'<a href="mailto:{email}">{email}</a></p>'
        '<img src="cid:logo@contoso.com" width="120"/>'
        "</div></body></html>"
    )


def _reporter(
    name: str = "Test User",
    email: str = "test.user@contoso.com",
    department: str = "Engineering",
) -> TicketReporter:
    return TicketReporter(name=name, email=email, department=department)


def build_data_cleanup_scenarios() -> list[EvalScenario]:
    """Return all data cleanup evaluation scenarios."""
    return [
        _very_long_description(),
        _base64_image_inline(),
        _large_base64_attachment_dump(),
        _html_rich_email(),
        _html_email_with_nested_tables(),
        _unicode_heavy_description(),
        _emoji_laden_ticket(),
        _empty_description(),
        _whitespace_only_description(),
        _garbled_phone_transcription(),
        _extremely_long_subject(),
        _repeated_text_spam(),
        _mixed_language_ticket(),
        _email_thread_with_signatures(),
        _control_characters_in_description(),
        _csv_data_dump_in_description(),
        _log_dump_in_description(),
    ]


def _very_long_description() -> EvalScenario:
    """Ticket with an excessively long description (~6000 chars)."""
    core = (
        "My VPN keeps disconnecting every 10-15 minutes when I'm on the office Wi-Fi."
        " I'm on the 5th floor in the London office using GlobalProtect."
    )
    description = core + (_LONG_PADDING * 40)

    return EvalScenario(
        scenario_id="DC-001",
        category="data_cleanup",
        description="Very long ticket description (~6000 chars) with repetitive padding",
        ticket=Ticket(
            ticket_id="INC-DC-001",
            subject="VPN keeps disconnecting",
            description=description,
            reporter=_reporter("Emma Wilson", "emma.wilson@contoso.com", "Trading"),
            created_at="2026-03-18T08:30:00Z",
            channel="email",
        ),
        expected=TriageResponse(
            ticket_id="INC-DC-001",
            category="Network & Connectivity",
            priority="P3",
            assigned_team="Network Operations",
            needs_escalation=False,
            missing_information=["device_info"],
            next_best_action=(
                "Investigate VPN disconnection pattern on London office 5th floor Wi-Fi."
                " Check GlobalProtect client logs and Wi-Fi access point health."
            ),
            remediation_steps=[
                "Check GlobalProtect client version and update if needed",
                "Review Wi-Fi signal strength and channel congestion on 5th floor",
                "Check VPN gateway session timeout configuration",
                "Test with a wired connection to isolate Wi-Fi as the cause",
            ],
        ),
    )


def _base64_image_inline() -> EvalScenario:
    """Ticket with a base64-encoded image embedded in the description."""
    description = (
        "I keep getting this error when opening SAP:\n\n"
        f"Screenshot: {_BASE64_IMAGE_BLOCK}\n\n"
        "The error says 'Connection to application server lost' and appears"
        " every time I try to run the month-end financial report."
    )

    return EvalScenario(
        scenario_id="DC-002",
        category="data_cleanup",
        description="Base64-encoded image embedded inline in ticket description",
        ticket=Ticket(
            ticket_id="INC-DC-002",
            subject="SAP connection error with screenshot",
            description=description,
            reporter=_reporter("David Park", "david.park@contoso.com", "Finance"),
            created_at="2026-03-18T09:15:00Z",
            channel="portal",
        ),
        expected=TriageResponse(
            ticket_id="INC-DC-002",
            category="Software & Applications",
            priority="P2",
            assigned_team="Enterprise Applications",
            needs_escalation=False,
            missing_information=["environment_details", "error_message"],
            next_best_action=(
                "Investigate SAP application server connectivity issue."
                " Check SAP server health and network path from user's workstation."
            ),
            remediation_steps=[
                "Verify SAP application server is running and accepting connections",
                "Check network connectivity between user workstation and SAP server",
                "Review SAP client configuration for correct server address",
                "Check if other Finance users are experiencing the same issue",
            ],
        ),
    )


def _large_base64_attachment_dump() -> EvalScenario:
    """Ticket where the user pasted a large base64 blob as the description."""
    description = (
        "Here is the error log from my computer:\n\n"
        f"{_LARGE_BASE64_BLOCK}\n\n"
        f"{_LARGE_BASE64_BLOCK}\n\n"
        "Please help, my laptop is very slow since yesterday."
    )

    return EvalScenario(
        scenario_id="DC-003",
        category="data_cleanup",
        description="Large base64 data blobs (~10KB) pasted into the ticket body",
        ticket=Ticket(
            ticket_id="INC-DC-003",
            subject="Laptop very slow - attaching logs",
            description=description,
            reporter=_reporter("Lisa Chen", "lisa.chen@contoso.com", "HR"),
            created_at="2026-03-18T10:00:00Z",
            channel="portal",
        ),
        expected=TriageResponse(
            ticket_id="INC-DC-003",
            category="Hardware & Peripherals",
            priority="P3",
            assigned_team="Endpoint Engineering",
            needs_escalation=False,
            missing_information=["device_info", "error_message"],
            next_best_action=(
                "Investigate laptop performance degradation."
                " Run hardware diagnostics and check for resource-heavy processes."
            ),
            remediation_steps=[
                "Check Task Manager for processes consuming excessive CPU, memory, or disk",
                "Run hardware diagnostics on the laptop",
                "Check Windows Update status for pending or stuck updates",
                "If hardware diagnostics pass, consider reimaging the device",
            ],
        ),
    )


def _html_rich_email() -> EvalScenario:
    """Ticket submitted via email with full HTML formatting."""
    content = (
        "Hi IT team,<br/><br/>"
        "I <b>cannot access</b> my <span style='color:red'>OneDrive</span> files."
        " When I try to sync, I get error code <code>0x8004de40</code>."
        " This has been going on since Monday."
        " I have <u>critical client documents</u> I need for a presentation tomorrow."
    )
    html_body = _html_email_wrapper(
        content=content,
        name="Rachel Green",
        dept="Wealth Management",
        email="rachel.green@contoso.com",
    )

    return EvalScenario(
        scenario_id="DC-004",
        category="data_cleanup",
        description="HTML-rich email with inline styling, tags, and embedded CID images",
        ticket=Ticket(
            ticket_id="INC-DC-004",
            subject="Cannot access OneDrive files - URGENT",
            description=html_body,
            reporter=_reporter("Rachel Green", "rachel.green@contoso.com", "Wealth Management"),
            created_at="2026-03-18T11:20:00Z",
            channel="email",
        ),
        expected=TriageResponse(
            ticket_id="INC-DC-004",
            category="Data & Storage",
            priority="P2",
            assigned_team="Data Platform",
            needs_escalation=False,
            missing_information=["device_info"],
            next_best_action=(
                "Investigate OneDrive sync error 0x8004de40."
                " This typically indicates an authentication or network issue with the OneDrive client."
            ),
            remediation_steps=[
                "Check OneDrive sync status and error code 0x8004de40",
                "Verify user's OneDrive license is active",
                "Reset OneDrive sync client credentials",
                "If credential reset fails, unlink and relink the OneDrive account",
            ],
        ),
    )


def _html_email_with_nested_tables() -> EvalScenario:
    """Email with complex nested HTML tables (newsletter-style formatting)."""
    description = (
        '<table border="1" cellpadding="5"><tr><td>'
        '<table><tr><td style="background:#0078d4;color:white;padding:10px">'
        "<b>IT Support Request</b></td></tr>"
        "<tr><td>"
        "<p>My Outlook is crashing every time I open a calendar invite."
        " It started after the M365 update pushed last night.</p>"
        "<p>Error in Event Viewer: OUTLOOK.EXE - Application Error, code 0xc0000005</p>"
        "</td></tr>"
        '<tr><td style="font-size:8pt;color:#888">'
        "Sent from Outlook for Windows 365 | Version 2403 Build 17425.20000"
        "</td></tr></table>"
        "</td></tr></table>"
    )

    return EvalScenario(
        scenario_id="DC-005",
        category="data_cleanup",
        description="Email with complex nested HTML tables (newsletter-style)",
        ticket=Ticket(
            ticket_id="INC-DC-005",
            subject="Outlook crashing on calendar invites",
            description=description,
            reporter=_reporter("James Taylor", "james.taylor@contoso.com", "Legal"),
            created_at="2026-03-18T07:45:00Z",
            channel="email",
        ),
        expected=TriageResponse(
            ticket_id="INC-DC-005",
            category="Software & Applications",
            priority="P2",
            assigned_team="Enterprise Applications",
            needs_escalation=False,
            missing_information=["affected_users"],
            next_best_action=(
                "Investigate Outlook crash after M365 update."
                " Check if the update rollback is needed or if a repair resolves the issue."
            ),
            remediation_steps=[
                "Check if other users are experiencing the same Outlook crash after the M365 update",
                "Run Office repair from Control Panel",
                "If repair fails, roll back the M365 update to the previous version",
                "Clear the Outlook local cache and rebuild the profile if needed",
            ],
        ),
    )


def _unicode_heavy_description() -> EvalScenario:
    """Ticket with heavy Unicode characters, diacritics, and non-Latin scripts."""
    description = (
        "我的电脑无法连接到VPN。I'm in the Shànghǎi office (上海办公室) "
        "and the VPN client shows «Verbindung fehlgeschlagen» error. "
        "Это началось после обновления Windows. "
        "الرجاء المساعدة في أقرب وقت ممكن. "
        "Error code: ERR_CONN_REFUSED — 接続が拒否されました。"
        "Já tentei reiniciar o computador três vezes."
    )

    return EvalScenario(
        scenario_id="DC-006",
        category="data_cleanup",
        description="Multi-script Unicode (Chinese, Arabic, Russian, Japanese, Portuguese, German)",
        ticket=Ticket(
            ticket_id="INC-DC-006",
            subject="VPN连接失败 — Cannot connect to VPN",
            description=description,
            reporter=_reporter("Wei Zhang", "wei.zhang@contoso.com", "Trading"),
            created_at="2026-03-18T02:30:00Z",
            channel="portal",
        ),
        expected=TriageResponse(
            ticket_id="INC-DC-006",
            category="Network & Connectivity",
            priority="P2",
            assigned_team="Network Operations",
            needs_escalation=False,
            missing_information=["device_info", "network_location"],
            next_best_action=(
                "Investigate VPN connection failure from the Shanghai office."
                " ERR_CONN_REFUSED suggests the VPN gateway may be unreachable from this location."
            ),
            remediation_steps=[
                "Verify VPN gateway accessibility from the Shanghai office network",
                "Check for regional firewall or proxy rules blocking VPN traffic",
                "Verify VPN client version is current and compatible with the recent Windows update",
                "Test connectivity to the VPN gateway IP directly",
            ],
        ),
    )


def _emoji_laden_ticket() -> EvalScenario:
    """Ticket with excessive emoji usage."""
    description = (
        "😱😱😱 My laptop screen is BROKEN 💔💔💔\n\n"
        "There's a huge crack 🔨 across the display and I can barely see anything 👀\n"
        "I dropped it when running to a meeting 🏃‍♂️💨\n"
        "PLEASE HELP 🙏🙏🙏 I have a client presentation 📊 in 2 hours ⏰\n"
        "Can I get a loaner? 💻✨\n\n"
        "Thanks!! 🎉👍😊"
    )

    return EvalScenario(
        scenario_id="DC-007",
        category="data_cleanup",
        description="Ticket with excessive emoji usage throughout",
        ticket=Ticket(
            ticket_id="INC-DC-007",
            subject="🆘 BROKEN SCREEN 🆘 need help ASAP!!!",
            description=description,
            reporter=_reporter("Sophie Adams", "sophie.adams@contoso.com", "Marketing"),
            created_at="2026-03-18T13:00:00Z",
            channel="chat",
        ),
        expected=TriageResponse(
            ticket_id="INC-DC-007",
            category="Hardware & Peripherals",
            priority="P2",
            assigned_team="Endpoint Engineering",
            needs_escalation=False,
            missing_information=["device_info"],
            next_best_action=(
                "Dispatch loaner laptop immediately — user has client presentation in 2 hours."
                " Schedule screen repair or replacement for the damaged device."
            ),
            remediation_steps=[
                "Provide a loaner laptop from IT stock immediately",
                "Assist user with logging into the loaner and accessing presentation files",
                "Assess physical damage to the original laptop screen",
                "If under warranty, initiate RMA; otherwise schedule internal repair",
            ],
        ),
    )


def _empty_description() -> EvalScenario:
    """Ticket with completely empty description field."""
    return EvalScenario(
        scenario_id="DC-008",
        category="data_cleanup",
        description="Ticket with empty description — only subject line has information",
        ticket=Ticket(
            ticket_id="INC-DC-008",
            subject="Can't print",
            description="",
            reporter=_reporter("Mark Johnson", "mark.johnson@contoso.com", "Compliance"),
            created_at="2026-03-18T14:15:00Z",
            channel="chat",
        ),
        expected=TriageResponse(
            ticket_id="INC-DC-008",
            category="Hardware & Peripherals",
            priority="P3",
            assigned_team="Endpoint Engineering",
            needs_escalation=False,
            missing_information=[
                "affected_system",
                "error_message",
                "device_info",
                "network_location",
            ],
            next_best_action=(
                "Contact reporter to gather details: which printer, what error message,"
                " and whether this is a network or local printer issue."
            ),
            remediation_steps=[
                "Contact Mark Johnson to gather specific details about the printing issue",
                "Determine which printer and whether it is network or USB connected",
                "Once details are gathered, route to Network Operations if network printer",
            ],
        ),
    )


def _whitespace_only_description() -> EvalScenario:
    """Ticket where description is only whitespace/newlines."""
    return EvalScenario(
        scenario_id="DC-009",
        category="data_cleanup",
        description="Ticket where description is only whitespace and newlines",
        ticket=Ticket(
            ticket_id="INC-DC-009",
            subject="password reset needed",
            description="\n\n   \t\t  \n\n  \n",
            reporter=_reporter("Amy Foster", "amy.foster@contoso.com", "Finance"),
            created_at="2026-03-18T08:00:00Z",
            channel="portal",
        ),
        expected=TriageResponse(
            ticket_id="INC-DC-009",
            category="Access & Authentication",
            priority="P3",
            assigned_team="Identity & Access Management",
            needs_escalation=False,
            missing_information=["affected_system", "authentication_method"],
            next_best_action=(
                "Process password reset request."
                " Verify user identity and determine which system password needs resetting."
            ),
            remediation_steps=[
                "Verify user identity through standard verification process",
                "Determine which password needs resetting (Windows, VPN, application-specific)",
                "Guide user through self-service password reset portal if available",
                "If SSPR fails, perform manual password reset in Entra ID",
            ],
        ),
    )


def _garbled_phone_transcription() -> EvalScenario:
    """Simulates a messy phone call transcription with errors."""
    description = (
        "[Automated transcription — confidence: 42%]\n\n"
        "yeah hi um my my computer the thing is that um the screen goes black "
        "and then it comes back and then there's like these uh blue lines "
        "across the the monitor ya know and I tried the I tried connecting "
        "it to the other the thing the dock the docking station and same "
        "thing happpens [inaudible] probably about three days now since "
        "tueday no wednesday yeah wensday and I'm in in the um the new "
        "york office fourth floor near the uh [inaudible] near the kitchen "
        "I think its maybe the the cable or [inaudible]"
    )

    return EvalScenario(
        scenario_id="DC-010",
        category="data_cleanup",
        description="Garbled phone transcription with low confidence, inaudible sections",
        ticket=Ticket(
            ticket_id="INC-DC-010",
            subject="Phone call — display issues",
            description=description,
            reporter=_reporter("Robert Kim", "robert.kim@contoso.com", "Operations"),
            created_at="2026-03-18T15:30:00Z",
            channel="phone",
        ),
        expected=TriageResponse(
            ticket_id="INC-DC-010",
            category="Hardware & Peripherals",
            priority="P3",
            assigned_team="Endpoint Engineering",
            needs_escalation=False,
            missing_information=["device_info", "error_message"],
            next_best_action=(
                "Investigate monitor display issues — blue lines and blackouts."
                " Test with replacement cable and different docking station."
            ),
            remediation_steps=[
                "Test with a replacement display cable (DisplayPort or HDMI)",
                "Test monitor with a different docking station",
                "If issue persists, test with a different monitor to isolate the fault",
                "If the monitor is faulty, schedule replacement",
            ],
        ),
    )


def _extremely_long_subject() -> EvalScenario:
    """Ticket with an absurdly long subject line."""
    base_subject = "URGENT HELP NEEDED "
    subject = (base_subject * 30).strip()

    return EvalScenario(
        scenario_id="DC-011",
        category="data_cleanup",
        description="Extremely long subject line (~600 chars) with repeated urgent text",
        ticket=Ticket(
            ticket_id="INC-DC-011",
            subject=subject,
            description=(
                "My account keeps getting locked out every 30 minutes."
                " I've changed my password three times today."
                " I think there might be a service or script somewhere"
                " using my old credentials."
            ),
            reporter=_reporter("Alex Turner", "alex.turner@contoso.com", "Engineering"),
            created_at="2026-03-18T09:45:00Z",
            channel="email",
        ),
        expected=TriageResponse(
            ticket_id="INC-DC-011",
            category="Access & Authentication",
            priority="P2",
            assigned_team="Identity & Access Management",
            needs_escalation=False,
            missing_information=["affected_system"],
            next_best_action=(
                "Investigate repeated account lockouts."
                " Check for stale credentials in services, scheduled tasks, or cached sessions."
            ),
            remediation_steps=[
                "Check Entra ID sign-in logs for the source of failed authentication attempts",
                "Identify any services or scheduled tasks using stale credentials",
                "Clear cached credentials on user's workstation and any mapped drives",
                "If suspicious activity detected, alert Security Operations",
            ],
        ),
    )


def _repeated_text_spam() -> EvalScenario:
    """Ticket with massively repeated identical content."""
    line = "Please fix my email it is not working. "
    description = line * 100

    return EvalScenario(
        scenario_id="DC-012",
        category="data_cleanup",
        description="Ticket with same sentence repeated 100 times",
        ticket=Ticket(
            ticket_id="INC-DC-012",
            subject="email broken",
            description=description,
            reporter=_reporter("Karen White", "karen.white@contoso.com", "HR"),
            created_at="2026-03-18T16:00:00Z",
            channel="portal",
        ),
        expected=TriageResponse(
            ticket_id="INC-DC-012",
            category="Software & Applications",
            priority="P3",
            assigned_team="Enterprise Applications",
            needs_escalation=False,
            missing_information=["error_message", "affected_system", "device_info"],
            next_best_action=(
                "Contact user to gather specific details about the email issue."
                " Determine whether this affects Outlook, OWA, or mobile email."
            ),
            remediation_steps=[
                "Contact Karen White to clarify the email issue and gather error details",
                "Check if Outlook or OWA is affected",
                "Verify mailbox health and license status in M365 admin center",
                "If Outlook-specific, try running Office repair",
            ],
        ),
    )


def _mixed_language_ticket() -> EvalScenario:
    """Ticket mixing multiple languages in a realistic way."""
    description = (
        "Bonjour l'équipe IT,\n\n"
        "Je n'arrive pas à me connecter au WiFi du bureau de Montréal. "
        "The error message says 'Network security key mismatch'. "
        "J'ai essayé de me reconnecter plusieurs fois mais ça ne marche pas. "
        "My colleague Pierre also has the same issue. "
        "Est-ce qu'il y a eu un changement de mot de passe du WiFi?\n\n"
        "Merci beaucoup,\nMarie"
    )

    return EvalScenario(
        scenario_id="DC-013",
        category="data_cleanup",
        description="Bilingual ticket (French/English) common in Canadian offices",
        ticket=Ticket(
            ticket_id="INC-DC-013",
            subject="WiFi connexion impossible — Montréal office",
            description=description,
            reporter=_reporter("Marie Dubois", "marie.dubois@contoso.com", "Wealth Management"),
            created_at="2026-03-18T12:00:00Z",
            channel="email",
        ),
        expected=TriageResponse(
            ticket_id="INC-DC-013",
            category="Network & Connectivity",
            priority="P3",
            assigned_team="Network Operations",
            needs_escalation=False,
            missing_information=["network_location", "affected_users"],
            next_best_action=(
                "Investigate WiFi connectivity issue at the Montréal office."
                " 'Network security key mismatch' suggests the WiFi password"
                " may have been changed without notifying users."
            ),
            remediation_steps=[
                "Verify if the WiFi password was recently changed for the Montréal office",
                "If changed, distribute the new WiFi credentials to affected users",
                "Check if the issue is isolated to specific access points or floor",
                "Verify WiFi authentication settings (WPA2/WPA3) on the access points",
            ],
        ),
    )


def _email_thread_with_signatures() -> EvalScenario:
    """Ticket that is a forwarded email thread with multiple signature blocks."""
    description = (
        "---------- Forwarded message ----------\n"
        "From: jennifer.lee@contoso.com\n"
        "Date: Mon, Mar 17, 2026 at 4:30 PM\n"
        "Subject: Re: SharePoint permissions\n"
        "To: it-helpdesk@contoso.com\n\n"
        "Hi team, following up on my original request below. I still cannot access"
        " the Compliance team SharePoint site. My manager approved my access request"
        " in ServiceNow (REQ-4521) two weeks ago but nothing happened.\n\n"
        "Thanks,\n"
        "Jennifer Lee\n"
        "Senior Compliance Analyst | Contoso Financial Services\n"
        "T: +1 (212) 555-0147 | M: +1 (646) 555-0198\n"
        "jennifer.lee@contoso.com\n"
        "-----\n"
        "CONFIDENTIALITY NOTICE: This email and any attachments are confidential"
        " and intended solely for the addressee(s). If you are not the intended"
        " recipient, please notify the sender immediately.\n"
        "-----\n\n"
        "---------- Original message ----------\n"
        "From: jennifer.lee@contoso.com\n"
        "Date: Mon, Mar 3, 2026 at 9:15 AM\n"
        "Subject: SharePoint permissions\n\n"
        "Hi, I need access to the Compliance team SharePoint site at"
        " https://contoso.sharepoint.com/sites/compliance-docs."
        " My manager has approved this.\n\n"
        "Thanks,\n"
        "Jennifer Lee\n"
        "Senior Compliance Analyst | Contoso Financial Services\n"
        "T: +1 (212) 555-0147\n"
        "jennifer.lee@contoso.com\n"
        "-----\n"
        "CONFIDENTIALITY NOTICE: This email and any attachments are confidential...\n"
    )

    return EvalScenario(
        scenario_id="DC-014",
        category="data_cleanup",
        description="Forwarded email thread with multiple signature blocks and disclaimers",
        ticket=Ticket(
            ticket_id="INC-DC-014",
            subject="Fwd: Re: SharePoint permissions",
            description=description,
            reporter=_reporter("Jennifer Lee", "jennifer.lee@contoso.com", "Compliance"),
            created_at="2026-03-18T16:45:00Z",
            channel="email",
        ),
        expected=TriageResponse(
            ticket_id="INC-DC-014",
            category="Data & Storage",
            priority="P3",
            assigned_team="Data Platform",
            needs_escalation=False,
            missing_information=["previous_ticket_id"],
            next_best_action=(
                "Process overdue SharePoint access request."
                " Approved request REQ-4521 has been pending for two weeks."
                " Grant access to the Compliance team SharePoint site."
            ),
            remediation_steps=[
                "Verify approval status of ServiceNow request REQ-4521",
                "Grant SharePoint site access to jennifer.lee@contoso.com",
                "Verify user can access https://contoso.sharepoint.com/sites/compliance-docs",
                "Investigate why the original approved request was not fulfilled",
            ],
        ),
    )


def _control_characters_in_description() -> EvalScenario:
    """Ticket with control characters and null bytes mixed in."""
    description = (
        "My laptop\x00 won't boot\x01 properly.\r\n"
        "It shows\x07 a blue screen\x08 with error\x1b[31m CRITICAL_PROCESS_DIED\x1b[0m\r\n"
        "and then restarts\x0c in a loop.\r\r\n"
        "This started after I installed\x00\x00 a Windows update last night.\r\n"
        "Asset tag: CT-L-5567"
    )

    return EvalScenario(
        scenario_id="DC-015",
        category="data_cleanup",
        description="Ticket with embedded control characters, null bytes, and ANSI codes",
        ticket=Ticket(
            ticket_id="INC-DC-015",
            subject="Laptop boot loop — blue screen",
            description=description,
            reporter=_reporter("Tom Harris", "tom.harris@contoso.com", "Engineering"),
            created_at="2026-03-18T07:00:00Z",
            channel="portal",
        ),
        expected=TriageResponse(
            ticket_id="INC-DC-015",
            category="Hardware & Peripherals",
            priority="P2",
            assigned_team="Endpoint Engineering",
            needs_escalation=False,
            missing_information=[],
            next_best_action=(
                "Investigate CRITICAL_PROCESS_DIED BSOD loop after Windows update."
                " Boot into Safe Mode to uninstall the problematic update."
            ),
            remediation_steps=[
                "Boot into Windows Recovery Environment or Safe Mode",
                "Uninstall the most recent Windows update",
                "If Safe Mode is inaccessible, boot from USB recovery media",
                "Run system file checker (sfc /scannow) from recovery console",
                "If system is unrecoverable, reimage from standard image and restore data from backup",
            ],
        ),
    )


def _csv_data_dump_in_description() -> EvalScenario:
    """Ticket where user pasted raw CSV data into the description."""
    csv_rows = "\n".join(
        [
            "timestamp,source_ip,dest_ip,port,status",
            "2026-03-17T22:01:00Z,10.0.1.45,10.0.2.100,443,BLOCKED",
            "2026-03-17T22:01:01Z,10.0.1.45,10.0.2.100,443,BLOCKED",
            "2026-03-17T22:01:02Z,10.0.1.45,10.0.2.100,443,BLOCKED",
            "2026-03-17T22:01:03Z,10.0.1.45,10.0.2.100,443,BLOCKED",
            "2026-03-17T22:01:04Z,10.0.1.45,10.0.2.100,443,BLOCKED",
            "2026-03-17T22:02:00Z,10.0.1.45,10.0.2.100,8443,BLOCKED",
            "2026-03-17T22:03:00Z,10.0.1.45,10.0.2.101,443,ALLOWED",
        ]
    )
    description = (
        "Our internal app at 10.0.2.100 is unreachable from the trading floor."
        " Here are the firewall logs showing the blocks:\n\n"
        f"{csv_rows}\n\n"
        "Can you open port 443 on the firewall for 10.0.1.0/24 to 10.0.2.100?"
    )

    return EvalScenario(
        scenario_id="DC-016",
        category="data_cleanup",
        description="Ticket with raw CSV firewall log data pasted into description",
        ticket=Ticket(
            ticket_id="INC-DC-016",
            subject="Firewall blocking internal app — need rule change",
            description=description,
            reporter=_reporter("Kevin Patel", "kevin.patel@contoso.com", "Trading"),
            created_at="2026-03-18T06:30:00Z",
            channel="portal",
        ),
        expected=TriageResponse(
            ticket_id="INC-DC-016",
            category="Network & Connectivity",
            priority="P2",
            assigned_team="Network Operations",
            needs_escalation=False,
            missing_information=["business_impact"],
            next_best_action=(
                "Review firewall rule change request."
                " Validate that opening port 443 from 10.0.1.0/24 to 10.0.2.100"
                " is appropriate and obtain security approval."
            ),
            remediation_steps=[
                "Verify the firewall block entries match the reported issue",
                "Obtain security team approval for the firewall rule change",
                "Create firewall rule allowing 10.0.1.0/24 to 10.0.2.100 on port 443",
                "Test connectivity after rule implementation",
                "Document the rule change with business justification",
            ],
        ),
    )


def _log_dump_in_description() -> EvalScenario:
    """Ticket with a large application log dump."""
    log_lines = "\n".join(
        [
            "2026-03-18 09:15:22 [ERROR] AuthModule: Failed to validate MFA token"
            " for user sarah.chen@contoso.com. Token expired at 2026-03-18T09:10:00Z."
            " Retry count: 3. Module: AzureAD.MFA.Validator.",
            "2026-03-18 09:15:23 [WARN] SessionManager: Session timeout for sid=a8f3c2e1-4b5d. Redirecting to login.",
            "2026-03-18 09:15:24 [ERROR] AuthModule: MFA challenge failed."
            " Provider: Microsoft Authenticator. Error: AADSTS50076.",
            "2026-03-18 09:15:25 [INFO] AuditLog: Login failure recorded. IP: 10.0.5.42. Location: NYC-FL4.",
            "2026-03-18 09:15:26 [ERROR] AuthModule: Max retry exceeded."
            " Account locked: sarah.chen@contoso.com. Lockout duration: 30min.",
        ]
    )
    description = (
        "Our MFA system is locking out users who shouldn't be locked out."
        " Here are the relevant logs:\n\n"
        f"```\n{log_lines}\n```\n\n"
        "This is affecting multiple traders and they can't access Bloomberg this morning."
    )

    return EvalScenario(
        scenario_id="DC-017",
        category="data_cleanup",
        description="Ticket with application log dump including structured log entries",
        ticket=Ticket(
            ticket_id="INC-DC-017",
            subject="MFA locking out traders — need immediate fix",
            description=description,
            reporter=_reporter("Mike Chen", "mike.chen@contoso.com", "IT"),
            created_at="2026-03-18T09:20:00Z",
            channel="portal",
        ),
        expected=TriageResponse(
            ticket_id="INC-DC-017",
            category="Access & Authentication",
            priority="P1",
            assigned_team="Identity & Access Management",
            needs_escalation=True,
            missing_information=["affected_users"],
            next_best_action=(
                "Investigate MFA lockout issue affecting multiple traders."
                " AADSTS50076 errors suggest a Conditional Access policy or MFA provider issue."
                " Revenue-impacting — traders cannot access Bloomberg."
            ),
            remediation_steps=[
                "Check Entra ID for recent MFA policy changes or Conditional Access updates",
                "Identify all affected user accounts and unlock them",
                "Investigate AADSTS50076 error — check MFA provider health",
                "If systemic, temporarily reduce MFA lockout threshold while investigating",
                "Confirm traders can access Bloomberg after account unlock",
            ],
        ),
    )
