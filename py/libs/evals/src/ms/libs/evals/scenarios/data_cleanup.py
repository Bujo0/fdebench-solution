"""Data cleanup evaluation scenarios.

Tests the triage API's ability to handle messy, noisy, or malformed input
while still extracting the underlying support request and producing correct
triage decisions.
"""

from ms.libs.evals.models.enums import (
    AssignedTeam,
    MissingInfoField,
    Priority,
    ScenarioTag,
    TicketCategory,
    TicketChannel,
)
from ms.libs.evals.models.scenario import (
    EvalScenario,
    Reporter,
    Ticket,
    TriageDecision,
)

_TAG = ScenarioTag.DATA_CLEANUP

# Reusable long legal disclaimer
_LEGAL_DISCLAIMER = (
    "\n\n---\nCONFIDENTIALITY NOTICE: This e-mail message, including any attachments, "
    "is for the sole use of the intended recipient(s) and may contain confidential and "
    "privileged information. Any unauthorized review, use, disclosure or distribution is "
    "prohibited. If you are not the intended recipient, please contact the sender by reply "
    "e-mail and destroy all copies of the original message. This e-mail does not constitute "
    "a binding agreement, nor does it create any obligation on behalf of Contoso Financial "
    "Services or any of its subsidiaries. Any views or opinions presented in this email are "
    "solely those of the author and do not necessarily represent those of the company. "
    "Employees of Contoso Financial Services are expressly required not to make defamatory "
    "statements and not to infringe or authorize any infringement of copyright or any other "
    "legal right by email communications. Any such communication is contrary to company policy "
    "and outside the scope of the employment of the individual concerned. The company will not "
    "accept any liability in respect of such communication, and the employee responsible will "
    "be personally liable for any damages or other liability arising.\n---"
)

# Reusable base64 image fragment (PNG header bytes, truncated)
_BASE64_IMAGE_FRAGMENT = (
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJ"
    "RU5ErkJggg==" * 30  # ~2.5KB of repeated base64
)


def _very_long_email() -> EvalScenario:
    """A legitimate VPN issue buried in an extremely long email body."""
    padding = (
        "I wanted to provide as much context as possible so you can understand the full "
        "situation. Our team has been working on the quarterly deliverables and the VPN "
        "disconnections are really affecting productivity. Multiple people on my floor have "
        "mentioned similar issues but I'm not sure if they filed tickets. The Wi-Fi signal "
        "seems fine for everything else — browsing, Teams calls, etc. It's specifically the "
        "VPN that drops. I've been tracking this for the past week and it happens at least "
        "3-4 times per day, always when I switch from my docking station to wireless. "
    )
    description = (
        "Hi IT Support,\n\n"
        "I'm having VPN connectivity issues that started after last week's Windows update. "
        "Every time I undock my laptop and move to Wi-Fi, GlobalProtect VPN drops and I have "
        "to manually reconnect. This happens consistently on Floor 6 in the NYC office.\n\n"
        + padding * 15
        + "\n\nThanks for looking into this.\n"
        + "Best regards,\n"
        + "Amanda Foster\n"
        + "Senior Analyst, Risk Management\n"
        + "Contoso Financial Services\n"
        + "One Financial Plaza, 42nd Floor\n"
        + "New York, NY 10004\n"
        + "Phone: +1 (212) 555-0142\n"
        + "Mobile: +1 (917) 555-0198\n"
        + _LEGAL_DISCLAIMER
    )

    return EvalScenario(
        ticket=Ticket(
            ticket_id="INC-9001",
            subject="VPN keeps dropping — very frustrated",
            description=description,
            reporter=Reporter(
                name="Amanda Foster",
                email="amanda.foster@contoso.com",
                department="Risk Management",
            ),
            created_at="2026-03-18T09:15:00Z",
            channel=TicketChannel.EMAIL,
            attachments=[],
        ),
        gold=TriageDecision(
            ticket_id="INC-9001",
            category=TicketCategory.NETWORK,
            priority=Priority.P3,
            assigned_team=AssignedTeam.NETWORK_OPS,
            needs_escalation=False,
            missing_information=[MissingInfoField.APPLICATION_VERSION],
            next_best_action=(
                "Investigate VPN disconnection on Wi-Fi transition after Windows update. "
                "Check GlobalProtect client version and known issues with the latest patch."
            ),
            remediation_steps=[
                "Verify GlobalProtect VPN client version is current",
                "Check for known compatibility issues between the latest Windows update and GlobalProtect",
                "Test VPN reconnection behavior when switching from Ethernet to Wi-Fi on a reference device",
                "If issue is widespread on Floor 6, check Wi-Fi access point configuration and signal strength",
            ],
        ),
        tag=_TAG,
        test_name="very_long_email",
        test_description=(
            "Tests handling of extremely long email body (~5000+ chars) with repeated "
            "paragraphs, email signatures, and legal disclaimers. The actual issue is a "
            "simple VPN problem buried in verbose context."
        ),
    )


def _base64_image_in_description() -> EvalScenario:
    """Ticket description contains inline base64-encoded image data."""
    description = (
        "Outlook is showing an error when I try to open attachments. Here's what I see:\n\n"
        "[Inline image: screenshot of error]\n"
        f"data:image/png;base64,{_BASE64_IMAGE_FRAGMENT}\n\n"
        "The error says 'Protected View — This file originated from an Internet location and "
        "might be unsafe.' I can't click 'Enable Editing' — the button is grayed out. This is "
        "happening with all PDF attachments from external clients. Started this morning."
    )

    return EvalScenario(
        ticket=Ticket(
            ticket_id="INC-9002",
            subject="Can't open email attachments — error screenshot attached inline",
            description=description,
            reporter=Reporter(
                name="Brian Walsh",
                email="brian.walsh@contoso.com",
                department="Wealth Management",
            ),
            created_at="2026-03-18T10:30:00Z",
            channel=TicketChannel.EMAIL,
            attachments=["error_screenshot.png"],
        ),
        gold=TriageDecision(
            ticket_id="INC-9002",
            category=TicketCategory.SOFTWARE,
            priority=Priority.P3,
            assigned_team=AssignedTeam.ENDPOINT_ENG,
            needs_escalation=False,
            missing_information=[
                MissingInfoField.APPLICATION_VERSION,
                MissingInfoField.DEVICE_INFO,
            ],
            next_best_action=(
                "Investigate Outlook Protected View blocking external PDF attachments. "
                "Check Trust Center settings and Group Policy for Protected View configuration."
            ),
            remediation_steps=[
                "Check Outlook Trust Center settings for Protected View configuration",
                "Verify Group Policy or Intune policy isn't enforcing restrictive Protected View settings",
                "Test opening the same attachment on a reference device to confirm scope",
                "If policy-related, adjust Protected View settings to allow editing for trusted senders",
            ],
        ),
        tag=_TAG,
        test_name="base64_image_in_description",
        test_description=(
            "Tests handling of inline base64-encoded image data embedded in the ticket "
            "description. The model must parse past the binary noise to extract the actual issue."
        ),
    )


def _html_email_body() -> EvalScenario:
    """Full HTML email with style tags, tables, divs wrapping a password reset request."""
    description = (
        '<!DOCTYPE html><html><head><style type="text/css">'
        "body{font-family:Calibri,sans-serif;font-size:11pt;color:#000}"
        ".footer{font-size:8pt;color:#888}"
        "table{border-collapse:collapse;width:100%}"
        "td{padding:8px;border:1px solid #ddd}"
        "</style></head><body>"
        '<div class="email-body">'
        "<p>Hi IT Team,</p>"
        "<p>I need a <strong>password reset</strong> for my SAP account. "
        "I've been locked out since this morning after entering the wrong password 3 times. "
        "My SAP username is <b>lpark01</b>.</p>"
        '<table><tr><td style="background:#f5f5f5">Account</td><td>lpark01</td></tr>'
        "<tr><td>System</td><td>SAP ERP (Production)</td></tr>"
        "<tr><td>Last successful login</td><td>2026-03-17 08:45 EST</td></tr></table>"
        "<p>I need this resolved before noon — month-end close depends on it.</p>"
        '<p class="footer">Sent from Outlook for iOS</p>'
        "</div></body></html>"
    )

    return EvalScenario(
        ticket=Ticket(
            ticket_id="INC-9003",
            subject="SAP account locked out",
            description=description,
            reporter=Reporter(
                name="Linda Park",
                email="linda.park@contoso.com",
                department="Finance",
            ),
            created_at="2026-03-18T09:05:00Z",
            channel=TicketChannel.EMAIL,
            attachments=[],
        ),
        gold=TriageDecision(
            ticket_id="INC-9003",
            category=TicketCategory.ACCESS_AUTH,
            priority=Priority.P2,
            assigned_team=AssignedTeam.ENTERPRISE_APPS,
            needs_escalation=False,
            missing_information=[],
            next_best_action=(
                "Reset SAP account password for user lpark01 and unlock the account. "
                "Time-sensitive due to month-end close deadline."
            ),
            remediation_steps=[
                "Unlock the SAP account for user lpark01 in the SAP production system",
                "Reset the password and communicate new temporary credentials securely",
                "Verify the user can log in and access month-end close transactions",
                "Review account lockout policy to ensure 3-attempt threshold is appropriate",
            ],
        ),
        tag=_TAG,
        test_name="html_email_body",
        test_description=(
            "Tests handling of a full HTML email body with inline CSS, tables, and semantic "
            "markup. The model must extract the actual request from HTML noise."
        ),
    )


def _email_thread_chain() -> EvalScenario:
    """Multi-level email thread with forwarded/replied messages; only latest is relevant."""
    description = (
        "Quick update — the shared mailbox issue is still happening. "
        "finance-reports@contoso.com is bouncing external emails as of 8 AM today. "
        "Clients are not receiving their quarterly statements.\n\n"
        "-------- Original Message --------\n"
        "From: Linda Park <linda.park@contoso.com>\n"
        "To: IT Support <support@contoso.com>\n"
        "Date: March 17, 2026 at 4:15 PM\n"
        "Subject: Re: Shared mailbox not sending\n\n"
        "Hi, I reported this yesterday and was told it was fixed. "
        "It's not. Please escalate.\n\n"
        "-------- Original Message --------\n"
        "From: IT Support <support@contoso.com>\n"
        "To: Linda Park <linda.park@contoso.com>\n"
        "Date: March 16, 2026 at 2:30 PM\n"
        "Subject: Re: Shared mailbox not sending\n\n"
        "Hi Linda, we've adjusted the mail flow rules. "
        "Please try again and let us know if the issue persists.\n\n"
        "-------- Original Message --------\n"
        "From: Linda Park <linda.park@contoso.com>\n"
        "To: IT Support <support@contoso.com>\n"
        "Date: March 16, 2026 at 11:00 AM\n"
        "Subject: Shared mailbox not sending\n\n"
        "Hi, the finance-reports shared mailbox can't send external emails. "
        "Getting NDR bounce messages. Started this morning."
    )

    return EvalScenario(
        ticket=Ticket(
            ticket_id="INC-9004",
            subject="Re: Re: Re: Shared mailbox not sending — STILL BROKEN",
            description=description,
            reporter=Reporter(
                name="Linda Park",
                email="linda.park@contoso.com",
                department="Finance",
            ),
            created_at="2026-03-18T08:20:00Z",
            channel=TicketChannel.EMAIL,
            attachments=[],
        ),
        gold=TriageDecision(
            ticket_id="INC-9004",
            category=TicketCategory.SOFTWARE,
            priority=Priority.P2,
            assigned_team=AssignedTeam.ENTERPRISE_APPS,
            needs_escalation=True,
            missing_information=[
                MissingInfoField.ERROR_MESSAGE,
            ],
            next_best_action=(
                "Investigate recurring shared mailbox delivery failure for finance-reports@contoso.com. "
                "Third report — previous fix did not resolve the issue. Clients are not receiving quarterly statements."
            ),
            remediation_steps=[
                "Check Exchange Online mail flow rules for the finance-reports shared mailbox",
                "Review NDR bounce messages to identify the specific delivery failure reason",
                "Verify the shared mailbox has not exceeded sending limits or been flagged for spam",
                "Test sending to known external addresses from the mailbox directly",
                "Escalate to Microsoft support if mail flow rules appear correct but delivery still fails",
            ],
        ),
        tag=_TAG,
        test_name="email_thread_chain",
        test_description=(
            "Tests handling of a multi-level email thread with Re:/Fwd: chains. "
            "Only the latest message contains the current issue state; older messages are context."
        ),
    )


def _excessive_whitespace() -> EvalScenario:
    """Ticket with excessive whitespace, newlines, and formatting noise."""
    description = (
        "\n\n\n\n"
        "     Hi     ,\n\n\n"
        "     My      laptop      screen      is       flickering      .\n\n\n\n"
        "     It     started      yesterday       afternoon     .\n\n\n"
        "\t\t\tI     tried     restarting     but     it      still      happens.\n\n\n\n\n"
        "     The     screen      goes       black      for      a     second\n"
        "     then      comes      back      .\n\n\n\n"
        "     It's      a      Dell      Latitude      5540      .\n\n\n\n\n\n"
        "     Please       help     .\n\n\n\n\n\n\n"
        "     Thanks     ,\n"
        "     Wei     Chen\n\n\n\n\n"
    )

    return EvalScenario(
        ticket=Ticket(
            ticket_id="INC-9005",
            subject="screen   flickering     issue",
            description=description,
            reporter=Reporter(
                name="Wei Chen",
                email="wei.chen@contoso.com",
                department="Retail Banking",
            ),
            created_at="2026-03-18T11:00:00Z",
            channel=TicketChannel.PORTAL,
            attachments=[],
        ),
        gold=TriageDecision(
            ticket_id="INC-9005",
            category=TicketCategory.HARDWARE,
            priority=Priority.P3,
            assigned_team=AssignedTeam.ENDPOINT_ENG,
            needs_escalation=False,
            missing_information=[
                MissingInfoField.REPRODUCTION_FREQUENCY,
            ],
            next_best_action=(
                "Investigate screen flickering on Dell Latitude 5540. "
                "Check display driver version and test with external monitor to isolate hardware vs. software issue."
            ),
            remediation_steps=[
                "Check and update display drivers on the Dell Latitude 5540",
                "Test with an external monitor to determine if the issue is the internal display or GPU",
                "Check for recent Windows updates that may have affected display drivers",
                "If hardware fault, schedule laptop replacement or display repair",
            ],
        ),
        tag=_TAG,
        test_name="excessive_whitespace",
        test_description=(
            "Tests handling of excessive whitespace, tabs, and newlines throughout "
            "the ticket description. The underlying issue is straightforward but heavily padded."
        ),
    )


def _unicode_special_chars() -> EvalScenario:
    """Ticket with heavy unicode usage: emojis, accented characters, RTL fragments."""
    description = (
        "🚨🚨🚨 URGENT 🚨🚨🚨\n\n"
        "Our café ☕ kiosk in the London office lobby can't connect to Wi-Fi anymore!!! 😤😤\n\n"
        "The kiosk runs a digital signage app that shows the café menu and Contoso branding. "
        "It was working fine until the network maintenance last night.\n\n"
        "Model: Samsung Tizen display with built-in Wi-Fi\n"
        "Location: Building 2, Ground Floor, Café \"Thé Crème\"\n"
        "SSID it should connect to: Contoso-Guest-IoT\n\n"
        "The display shows «Impossible de se connecter au réseau» (French error — "
        "we think the locale got changed somehow 🤷‍♂️)\n\n"
        "Please fix ASAP — we have clients visiting tomorrow and an empty screen in "
        "the lobby looks très unprofessional 😬\n\n"
        "Merci beaucoup! 🙏✨\n"
        "— François Müller-Østergaard"
    )

    return EvalScenario(
        ticket=Ticket(
            ticket_id="INC-9006",
            subject="🚨 Café kiosk Wi-Fi down — London lobby 🚨",
            description=description,
            reporter=Reporter(
                name="François Müller-Østergaard",
                email="francois.muller@contoso.com",
                department="Facilities",
            ),
            created_at="2026-03-18T16:30:00Z",
            channel=TicketChannel.CHAT,
            attachments=[],
        ),
        gold=TriageDecision(
            ticket_id="INC-9006",
            category=TicketCategory.NETWORK,
            priority=Priority.P3,
            assigned_team=AssignedTeam.NETWORK_OPS,
            needs_escalation=False,
            missing_information=[
                MissingInfoField.DEVICE_INFO,
                MissingInfoField.NETWORK_LOCATION,
            ],
            next_best_action=(
                "Investigate Wi-Fi connectivity issue for the café kiosk (Samsung Tizen display) "
                "on the Contoso-Guest-IoT SSID after last night's network maintenance in the London office."
            ),
            remediation_steps=[
                "Verify the Contoso-Guest-IoT SSID is broadcasting in Building 2, Ground Floor",
                "Check if the kiosk's MAC address is still whitelisted after the network maintenance",
                "Verify IoT network VLAN configuration was not affected by the maintenance",
                "Reconnect the kiosk to Wi-Fi and reset locale to English if needed",
                "Test connectivity and confirm the digital signage app loads correctly",
            ],
        ),
        tag=_TAG,
        test_name="unicode_special_chars",
        test_description=(
            "Tests handling of heavy Unicode content: emojis, accented characters (é, ü, ø), "
            "French text mixed with English, special quotation marks. Validates the model "
            "handles multi-script input correctly."
        ),
    )


def _repeated_content() -> EvalScenario:
    """Same paragraph copy-pasted multiple times with the actual issue buried within."""
    repeated_block = (
        "Please help. This is very important and needs to be fixed urgently. "
        "I have a deadline coming up and cannot work without this being resolved. "
        "I've been waiting for someone to help me. Please prioritize this ticket. "
    )
    description = (
        repeated_block * 3
        + "\n\nACTUAL ISSUE: My Salesforce account shows 'License expired' when I try to "
        "log in. I was able to access it fine last Friday. I need Salesforce to update "
        "client records for the Q1 review on Wednesday.\n\n"
        + repeated_block * 3
        + "\n\nPlease help ASAP.\n"
        + repeated_block * 2
    )

    return EvalScenario(
        ticket=Ticket(
            ticket_id="INC-9007",
            subject="PLEASE HELP — cannot work — very urgent!!!",
            description=description,
            reporter=Reporter(
                name="Carlos Rivera",
                email="carlos.rivera@contoso.com",
                department="Sales",
            ),
            created_at="2026-03-18T08:45:00Z",
            channel=TicketChannel.EMAIL,
            attachments=[],
        ),
        gold=TriageDecision(
            ticket_id="INC-9007",
            category=TicketCategory.SOFTWARE,
            priority=Priority.P3,
            assigned_team=AssignedTeam.ENTERPRISE_APPS,
            needs_escalation=False,
            missing_information=[
                MissingInfoField.ERROR_MESSAGE,
            ],
            next_best_action=(
                "Investigate Salesforce license expiry for the user. Check license assignment "
                "status in Salesforce admin and renew or reassign if expired."
            ),
            remediation_steps=[
                "Check the user's Salesforce license status in the Salesforce admin console",
                "Verify whether the license was removed, expired, or reassigned during recent changes",
                "Renew or reassign the license if it has lapsed",
                "Confirm the user can log in and access client records",
            ],
        ),
        tag=_TAG,
        test_name="repeated_content",
        test_description=(
            "Tests handling of excessive repeated content (same paragraph pasted 8+ times). "
            "The actual issue is a single sentence buried in the middle of the repetition."
        ),
    )


def _encoding_artifacts() -> EvalScenario:
    """Text with common encoding artifacts (mojibake) from Windows-1252 → UTF-8 misinterpretation."""
    # Mojibake sequences (UTF-8 bytes of curly quotes/dashes misread as Windows-1252)
    rsquo = "\u00c3\u00a2\u00e2\u0082\u00ac\u00e2\u0084\u00a2"  # â€™ (right single quote)
    ldquo = "\u00c3\u00a2\u00e2\u0082\u00ac\u0153"  # â€œ (left double quote)
    rdquo = "\u00c3\u00a2\u00e2\u0082\u00ac\u009d"  # â€\x9d (right double quote)
    bullet = "\u00c3\u00a2\u00e2\u0082\u00ac\u00a2"  # â€¢ (bullet)
    arrow = "\u00c3\u00a2\u0086\u0092"  # â†' (right arrow)
    mdash = "\u00c3\u00a2\u00e2\u0082\u00ac\u201c"  # â€" (em dash)

    description = (
        "Hi team,\n\n"
        f"I{rsquo}m having trouble with the company{rsquo}s SharePoint site. "
        f"When I try to upload documents, I get an error that says {ldquo}Access Denied{rdquo}. "
        "This started happening after I changed my password.\n\n"
        f"I{rsquo}ve tried:\n"
        f"{bullet} Clearing browser cache\n"
        f"{bullet} Using a different browser (Chrome {arrow} Edge)\n"
        f"{bullet} Logging out and back in\n\n"
        "The site URL is: https://contoso.sharepoint.com/sites/legal-documents\n"
        f"I need to upload the Q1 compliance report by end of day {mdash} it{rsquo}s required "
        "for the regulatory filing.\n\n"
        "Thanks,\nNatasha Romanova\n"
        f"Legal {mdash} Compliance Division"
    )

    return EvalScenario(
        ticket=Ticket(
            ticket_id="INC-9008",
            subject="SharePoint upload broken after password change",
            description=description,
            reporter=Reporter(
                name="Natasha Romanova",
                email="natasha.romanova@contoso.com",
                department="Legal",
            ),
            created_at="2026-03-18T14:00:00Z",
            channel=TicketChannel.EMAIL,
            attachments=[],
        ),
        gold=TriageDecision(
            ticket_id="INC-9008",
            category=TicketCategory.DATA_STORAGE,
            priority=Priority.P2,
            assigned_team=AssignedTeam.DATA_PLATFORM,
            needs_escalation=False,
            missing_information=[
                MissingInfoField.ENVIRONMENT_DETAILS,
            ],
            next_best_action=(
                "Investigate SharePoint 'Access Denied' error on document upload after password "
                "change. Check if the authentication token or session needs refresh after the password rotation."
            ),
            remediation_steps=[
                "Have the user sign out of all Microsoft 365 sessions and sign back in with the new password",
                "Clear cached credentials from Windows Credential Manager",
                "Check SharePoint site permissions for the user's account on the legal-documents site",
                "If permissions are correct, check for Conditional Access policies that may block after password change",
                "Verify the user can upload the Q1 compliance report successfully",
            ],
        ),
        tag=_TAG,
        test_name="encoding_artifacts",
        test_description=(
            "Tests handling of mojibake/encoding artifacts (Windows-1252 → UTF-8 misinterpretation). "
            "Common in email-to-ticket systems: â€™ instead of ', â€œ instead of \", etc."
        ),
    )


def _minimal_description() -> EvalScenario:
    """Near-empty ticket with almost no useful information."""
    return EvalScenario(
        ticket=Ticket(
            ticket_id="INC-9009",
            subject="help",
            description="broken",
            reporter=Reporter(
                name="Pat Johnson",
                email="pat.johnson@contoso.com",
                department="HR",
            ),
            created_at="2026-03-18T07:30:00Z",
            channel=TicketChannel.CHAT,
            attachments=[],
        ),
        gold=TriageDecision(
            ticket_id="INC-9009",
            category=TicketCategory.GENERAL_INQUIRY,
            priority=Priority.P4,
            assigned_team=AssignedTeam.ENDPOINT_ENG,
            needs_escalation=False,
            missing_information=[
                MissingInfoField.AFFECTED_SYSTEM,
                MissingInfoField.ERROR_MESSAGE,
                MissingInfoField.DEVICE_INFO,
                MissingInfoField.STEPS_TO_REPRODUCE,
                MissingInfoField.BUSINESS_IMPACT,
            ],
            next_best_action=(
                "Contact the reporter to gather basic information about the issue. "
                "The ticket contains no actionable details — need to determine what is broken."
            ),
            remediation_steps=[
                "Contact Pat Johnson in HR to gather details about the reported issue",
                "Determine which system, application, or device is affected",
                "Gather error messages, screenshots, or steps to reproduce",
                "Once the actual issue is identified, re-triage and route to the correct team",
            ],
        ),
        tag=_TAG,
        test_name="minimal_description",
        test_description=(
            "Tests handling of a near-empty ticket with no useful information. "
            "Subject is 'help', description is 'broken'. The system should identify "
            "all the missing information and request follow-up."
        ),
    )


def _attachment_spam() -> EvalScenario:
    """Normal ticket with an excessive number of attachment filenames listed."""
    attachment_names = [f"screenshot_{i:03d}.png" for i in range(1, 51)] + [
        "error_log_2026-03-18.txt",
        "system_info.xml",
        "event_viewer_export.evtx",
        "dxdiag_output.txt",
        "network_trace.pcap",
    ]

    return EvalScenario(
        ticket=Ticket(
            ticket_id="INC-9010",
            subject="Blue screen crashes — all evidence attached",
            description=(
                "My laptop has been crashing with a blue screen (BSOD) about 3 times a day "
                "for the past week. The stop code is DRIVER_IRQL_NOT_LESS_OR_EQUAL. I've taken "
                "a screenshot every time it happens and exported every log I could find. "
                "All 55 files are attached. The crashes seem to happen when I'm using Teams "
                "and Outlook simultaneously. Dell Latitude 7440, Windows 11 23H2."
            ),
            reporter=Reporter(
                name="Kevin O'Brien",
                email="kevin.obrien@contoso.com",
                department="Trading",
            ),
            created_at="2026-03-18T09:50:00Z",
            channel=TicketChannel.PORTAL,
            attachments=attachment_names,
        ),
        gold=TriageDecision(
            ticket_id="INC-9010",
            category=TicketCategory.HARDWARE,
            priority=Priority.P2,
            assigned_team=AssignedTeam.ENDPOINT_ENG,
            needs_escalation=False,
            missing_information=[],
            next_best_action=(
                "Investigate recurring BSOD with DRIVER_IRQL_NOT_LESS_OR_EQUAL on Dell Latitude 7440. "
                "Analyze minidump files to identify the faulting driver. Critical for Trading department user."
            ),
            remediation_steps=[
                "Analyze Windows minidump files to identify the specific faulting driver",
                "Check for driver updates for the Dell Latitude 7440, especially network and display drivers",
                "Verify Windows 11 23H2 is fully updated with latest patches",
                "If driver-related, update or roll back the faulting driver",
                "If crashes persist after driver fixes, run hardware diagnostics (Dell SupportAssist)",
            ],
        ),
        tag=_TAG,
        test_name="attachment_spam",
        test_description=(
            "Tests handling of an excessive number of attachments (55 files). "
            "The ticket itself is well-written; the noise is in the attachment list."
        ),
    )


def _log_dump_description() -> EvalScenario:
    """User pasted a large structured log dump as the ticket description."""
    log_lines = "\n".join(
        [
            f"2026-03-18T0{h}:{m:02d}:00Z ERROR [app.auth] "
            f"Failed login attempt for user svc-etl-prod from 10.0.{h}.{m} — "
            "AADSTS700016: Application not found in tenant"
            for h in range(3, 9)
            for m in range(0, 60, 5)
        ]
    )

    description = (
        "Our ETL service account keeps failing to authenticate. Here are the logs:\n\n"
        + log_lines
        + "\n\n"
        "Can someone look at this? The service account svc-etl-prod can't authenticate "
        "against Azure AD. Might be an app registration issue."
    )

    return EvalScenario(
        ticket=Ticket(
            ticket_id="INC-9011",
            subject="ETL auth failures — logs attached",
            description=description,
            reporter=Reporter(
                name="Raj Patel",
                email="raj.patel@contoso.com",
                department="Data Engineering",
            ),
            created_at="2026-03-18T09:00:00Z",
            channel=TicketChannel.PORTAL,
            attachments=["full_auth_log.txt"],
        ),
        gold=TriageDecision(
            ticket_id="INC-9011",
            category=TicketCategory.ACCESS_AUTH,
            priority=Priority.P2,
            assigned_team=AssignedTeam.IDENTITY_ACCESS,
            needs_escalation=False,
            missing_information=[
                MissingInfoField.CONFIGURATION_DETAILS,
            ],
            next_best_action=(
                "Investigate AADSTS700016 error for service account svc-etl-prod. "
                "The app registration may have been deleted or the tenant ID is incorrect."
            ),
            remediation_steps=[
                "Check Entra ID app registrations for the ETL service application",
                "Verify the application ID and tenant ID in the service account configuration",
                "If the app registration was deleted, recreate it with the correct permissions",
                "Update the service account credentials and test authentication",
                "Verify ETL pipeline runs successfully after fixing authentication",
            ],
        ),
        tag=_TAG,
        test_name="log_dump_description",
        test_description=(
            "Tests handling of a large structured log dump (~72 log lines) pasted directly "
            "into the ticket description. The actual issue summary is at the end."
        ),
    )


def _auto_generated_monitoring_alert() -> EvalScenario:
    """Monitoring system alert with excessive metadata headers."""
    description = (
        "--- AUTOMATED ALERT ---\n"
        "Alert ID: MON-2026-03-18-0847\n"
        "Severity: WARNING\n"
        "Source: Azure Monitor\n"
        "Subscription: sub-prod-eastus2 (a1b2c3d4-e5f6-7890-abcd-ef1234567890)\n"
        "Resource Group: rg-web-prod\n"
        "Resource: app-contoso-web-prod\n"
        "Resource Type: Microsoft.Web/sites\n"
        "Region: East US 2\n"
        "Alert Rule: HTTP 5xx > 5% threshold\n"
        "Time (UTC): 2026-03-18T06:15:00Z\n"
        "Condition: HTTP 5xx error rate exceeded 5% threshold\n"
        "Current Value: 12.3%\n"
        "Threshold: 5.0%\n"
        "Window: 5 minutes\n"
        "Aggregation: Average\n"
        "Signal Type: Metric\n"
        "Monitor Condition: Fired\n"
        "Fired Time: 2026-03-18T06:15:00Z\n"
        "Alert Target IDs: /subscriptions/a1b2c3d4/resourceGroups/rg-web-prod/providers/"
        "Microsoft.Web/sites/app-contoso-web-prod\n"
        "Dimensions:\n"
        "  - StatusCode: 500\n"
        "  - Instance: app-contoso-web-prod_0\n"
        "  - HttpMethod: GET, POST\n"
        "Affected Endpoints: /api/v2/clients, /api/v2/transactions\n"
        "--- END ALERT ---\n\n"
        "Action Required: Investigate HTTP 5xx spike on the client-facing web application."
    )

    return EvalScenario(
        ticket=Ticket(
            ticket_id="INC-9012",
            subject="[Azure Monitor] ALERT: HTTP 5xx > 5% — app-contoso-web-prod",
            description=description,
            reporter=Reporter(
                name="Azure Monitor",
                email="noreply-azuremonitor@contoso.com",
                department="Cloud Infrastructure",
            ),
            created_at="2026-03-18T06:15:00Z",
            channel=TicketChannel.EMAIL,
            attachments=[],
        ),
        gold=TriageDecision(
            ticket_id="INC-9012",
            category=TicketCategory.SOFTWARE,
            priority=Priority.P2,
            assigned_team=AssignedTeam.ENTERPRISE_APPS,
            needs_escalation=False,
            missing_information=[],
            next_best_action=(
                "Investigate 12.3% HTTP 5xx error rate on the client-facing web application "
                "(app-contoso-web-prod). Affecting /api/v2/clients and /api/v2/transactions endpoints."
            ),
            remediation_steps=[
                "Check application logs for the root cause of 500 errors on the affected endpoints",
                "Review recent deployments or configuration changes to app-contoso-web-prod",
                "Check downstream dependencies (database, APIs) for failures or latency",
                "If deployment-related, consider rolling back to the previous stable version",
                "Monitor error rate after mitigation and update alert status",
            ],
        ),
        tag=_TAG,
        test_name="auto_generated_monitoring_alert",
        test_description=(
            "Tests handling of an auto-generated monitoring alert with excessive metadata "
            "headers. The alert format is structured but noisy; the key info is the 5xx "
            "error rate and affected endpoints."
        ),
    )


def _multi_language_ticket() -> EvalScenario:
    """Ticket mixing English with Chinese and Japanese, common in the Singapore office."""
    description = (
        "Hi IT Support,\n\n"
        "我的VPN连接在新加坡办公室一直断开。(My VPN connection keeps disconnecting "
        "in the Singapore office.)\n\n"
        "Details:\n"
        "- 使用的是 GlobalProtect VPN client\n"
        "- 每次连接大约持续10分钟就断开 (disconnects after ~10 minutes each time)\n"
        "- Wi-Fi信号很好,其他应用没问题 (Wi-Fi signal is strong, other apps work fine)\n"
        "- 同事们没有这个问题 (colleagues don't have this issue)\n\n"
        "昨天下午重启了电脑,问题仍然存在。\n"
        "(Restarted laptop yesterday afternoon, problem persists.)\n\n"
        "ネットワークチームに確認してください。\n"
        "(Please check with the network team.)\n\n"
        "よろしくお願いします。\n"
        "谢谢！\n"
        "Yuki Watanabe"
    )

    return EvalScenario(
        ticket=Ticket(
            ticket_id="INC-9013",
            subject="VPN断开 — Singapore office VPN disconnection",
            description=description,
            reporter=Reporter(
                name="Yuki Watanabe",
                email="yuki.watanabe@contoso.com",
                department="Trading",
            ),
            created_at="2026-03-18T02:30:00Z",
            channel=TicketChannel.PORTAL,
            attachments=[],
        ),
        gold=TriageDecision(
            ticket_id="INC-9013",
            category=TicketCategory.NETWORK,
            priority=Priority.P3,
            assigned_team=AssignedTeam.NETWORK_OPS,
            needs_escalation=False,
            missing_information=[
                MissingInfoField.DEVICE_INFO,
                MissingInfoField.APPLICATION_VERSION,
            ],
            next_best_action=(
                "Investigate VPN disconnection issue for this user in the Singapore office. "
                "VPN drops after ~10 minutes despite strong Wi-Fi. Issue is user-specific — "
                "colleagues are not affected."
            ),
            remediation_steps=[
                "Verify GlobalProtect VPN client version on the user's device",
                "Check VPN gateway logs for disconnection reasons during the user's sessions",
                "Compare the user's device configuration with colleagues who are not affected",
                "Test VPN connectivity with a different device profile to isolate the issue",
                "If client-specific, reinstall GlobalProtect or update to the latest version",
            ],
        ),
        tag=_TAG,
        test_name="multi_language_ticket",
        test_description=(
            "Tests handling of a ticket mixing English, Mandarin Chinese, and Japanese. "
            "Common in multinational offices. The technical content is present in both "
            "languages; the model must handle CJK characters correctly."
        ),
    )


def _url_heavy_description() -> EvalScenario:
    """Description containing many URLs with the actual issue buried between them."""
    description = (
        "We're getting 403 Forbidden errors on several internal applications:\n\n"
        "WORKING:\n"
        "- https://portal.contoso.com/dashboard — OK\n"
        "- https://wiki.contoso.com/engineering — OK\n"
        "- https://git.contoso.com/ — OK\n"
        "- https://ci.contoso.com/pipelines — OK\n"
        "- https://monitoring.contoso.com/grafana — OK\n\n"
        "NOT WORKING (403 Forbidden):\n"
        "- https://reports.contoso.com/finance/q1 — 403\n"
        "- https://reports.contoso.com/compliance/audit — 403\n"
        "- https://reports.contoso.com/risk/dashboard — 403\n"
        "- https://api.contoso.com/v2/reports — 403\n"
        "- https://api.contoso.com/v2/analytics — 403\n\n"
        "Looks like everything under reports.contoso.com and the /v2/ API paths on "
        "api.contoso.com are returning 403. Started happening about an hour ago. "
        "Multiple people in Finance and Compliance are affected. We checked and our "
        "Azure AD group membership hasn't changed.\n\n"
        "Possibly related to the Azure Front Door rule change that was deployed at 5 AM?"
    )

    return EvalScenario(
        ticket=Ticket(
            ticket_id="INC-9014",
            subject="403 errors on multiple internal apps — list of URLs inside",
            description=description,
            reporter=Reporter(
                name="Sarah Mitchell",
                email="sarah.mitchell@contoso.com",
                department="Finance",
            ),
            created_at="2026-03-18T06:45:00Z",
            channel=TicketChannel.PORTAL,
            attachments=[],
        ),
        gold=TriageDecision(
            ticket_id="INC-9014",
            category=TicketCategory.ACCESS_AUTH,
            priority=Priority.P2,
            assigned_team=AssignedTeam.NETWORK_OPS,
            needs_escalation=False,
            missing_information=[],
            next_best_action=(
                "Investigate 403 Forbidden errors on reports.contoso.com and api.contoso.com /v2/ "
                "paths. Likely caused by the Azure Front Door rule change deployed at 5 AM. "
                "Multiple users in Finance and Compliance affected."
            ),
            remediation_steps=[
                "Review the Azure Front Door rule change deployed at 5 AM for access control impacts",
                "Check WAF rules and routing rules on Azure Front Door for the affected paths",
                "Verify Azure AD Conditional Access policies for the reports and API applications",
                "If the Front Door change caused the issue, roll back the rule change",
                "Confirm access is restored for Finance and Compliance users on all affected URLs",
            ],
        ),
        tag=_TAG,
        test_name="url_heavy_description",
        test_description=(
            "Tests handling of a URL-heavy description with 10+ URLs. "
            "The model must distinguish working vs. broken URLs and identify "
            "the pattern (specific subdomains/paths affected)."
        ),
    )


def _legal_disclaimer_email() -> EvalScenario:
    """Short request followed by a massive legal disclaimer that dwarfs the actual content."""
    description = (
        "Can you reset my Outlook password? I think it expired.\n\n"
        + _LEGAL_DISCLAIMER
        + _LEGAL_DISCLAIMER
        + _LEGAL_DISCLAIMER
    )

    return EvalScenario(
        ticket=Ticket(
            ticket_id="INC-9015",
            subject="Password reset needed",
            description=description,
            reporter=Reporter(
                name="Jennifer Liu",
                email="jennifer.liu@contoso.com",
                department="Legal",
            ),
            created_at="2026-03-18T08:10:00Z",
            channel=TicketChannel.EMAIL,
            attachments=[],
        ),
        gold=TriageDecision(
            ticket_id="INC-9015",
            category=TicketCategory.ACCESS_AUTH,
            priority=Priority.P3,
            assigned_team=AssignedTeam.IDENTITY_ACCESS,
            needs_escalation=False,
            missing_information=[
                MissingInfoField.ERROR_MESSAGE,
            ],
            next_best_action=(
                "Reset the user's Outlook/Microsoft 365 password. Verify whether the password "
                "actually expired or if there is another authentication issue."
            ),
            remediation_steps=[
                "Check if the user's password has expired in Entra ID",
                "Reset the password and send temporary credentials securely",
                "Have the user log in and set a new permanent password",
                "Verify Outlook connects successfully with the new password",
            ],
        ),
        tag=_TAG,
        test_name="legal_disclaimer_email",
        test_description=(
            "Tests handling of a short request (one sentence) followed by a massive legal "
            "disclaimer (3x repeated) that dwarfs the actual content. Signal-to-noise ratio "
            "is extremely low."
        ),
    )


def get_data_cleanup_scenarios() -> list[EvalScenario]:
    """Return all data cleanup evaluation scenarios."""
    return [
        _very_long_email(),
        _base64_image_in_description(),
        _html_email_body(),
        _email_thread_chain(),
        _excessive_whitespace(),
        _unicode_special_chars(),
        _repeated_content(),
        _encoding_artifacts(),
        _minimal_description(),
        _attachment_spam(),
        _log_dump_description(),
        _auto_generated_monitoring_alert(),
        _multi_language_ticket(),
        _url_heavy_description(),
        _legal_disclaimer_email(),
    ]
