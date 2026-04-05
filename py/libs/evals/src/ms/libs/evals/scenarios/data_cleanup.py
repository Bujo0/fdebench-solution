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


def _pdf_text_extraction() -> EvalScenario:
    """Ticket description contains PDF-to-text extraction artifacts."""
    description = (
        "Hi IT,\n\n"
        "I\u2019m having issues with our CRM. Pasting the error from the PDF report our vendor "
        "sent:\n\n"
        "C u s t o m e r   R e l a t i o n s h i p   M a n a g e m e n t\n"
        "E r r o r   R e p o r t   \u2014   M a r c h   2 0 2 6\n\n"
        "Page 1 of 3\n\n"
        "                                              \n"
        "Er ror  Co de:  CRM -40 3- RE FRESH\n"
        "Aff ect ed  Mo dul e:  Da sh bo ard  Syn c\n"
        "Ti me sta mp:  20 26- 03- 18 T0 8: 30 :0 0Z\n\n"
        "De scr ipt ion:  Th e  da sh bo ard  fa il ed  to  re fr es h\n"
        "af te r  th e  la te st  da ta ba se  mi gr at io n.  Us er s\n"
        "re po rt  st al e  da ta  fr om  Ma rc h  15 th.\n\n"
        "\x0c"  # form feed character
        "Page 2 of 3\n\n"
        "Re com me nd at ion:  Cl ea r  ca ch e  an d  re -i ni ti al iz e\n"
        "da sh bo ard  co nn ec ti on  po ol.\n\n"
        "\x0c"
        "Page 3 of 3\n\n"
        "--- END OF REPORT ---\n\n"
        "Basically our CRM dashboard hasn\u2019t refreshed since the database migration on the 15th. "
        "The whole sales team is seeing stale data. Can someone look at this?"
    )

    return EvalScenario(
        ticket=Ticket(
            ticket_id="INC-9201",
            subject="CRM dashboard stale after migration — vendor error report attached",
            description=description,
            reporter=Reporter(
                name="Diana Morales",
                email="diana.morales@contoso.com",
                department="Sales",
            ),
            created_at="2026-03-18T09:00:00Z",
            channel=TicketChannel.EMAIL,
            attachments=["vendor_error_report.pdf"],
        ),
        gold=TriageDecision(
            ticket_id="INC-9201",
            category=TicketCategory.SOFTWARE,
            priority=Priority.P2,
            assigned_team=AssignedTeam.ENTERPRISE_APPS,
            needs_escalation=False,
            missing_information=[
                MissingInfoField.AFFECTED_USERS,
            ],
            next_best_action=(
                "Investigate CRM dashboard refresh failure after database migration. "
                "Error CRM-403-REFRESH indicates a stale connection pool. Clear cache and "
                "re-initialize dashboard connections."
            ),
            remediation_steps=[
                "Clear the CRM dashboard cache and re-initialize the connection pool",
                "Verify database migration completed successfully and data integrity is intact",
                "Test dashboard refresh with a sample user account",
                "Confirm the full sales team can see current data after the fix",
            ],
        ),
        tag=_TAG,
        test_name="pdf_text_extraction",
        test_description=(
            "Tests handling of PDF-to-text extraction artifacts: spaced-out characters, "
            "form feed characters, page headers, and broken word boundaries. The actual "
            "issue is a CRM dashboard refresh failure after a database migration."
        ),
    )


def _screenshot_ocr_errors() -> EvalScenario:
    """Ticket description created from OCR of a screenshot with recognition errors."""
    description = (
        "[Transcribed from screenshot via OCR]\n\n"
        "H1 IT Supp0rt,\n\n"
        "l\u2019m gett1ng an err0r when I try t0 0pen Micr0s0ft Teams. "
        "The err0r message says:\n\n"
        "\"We\u2019re s0rry\u2014we\u2019ve run int0 an 1ssue.\n"
        "Err0r c0de: CAA2000B\n"
        "C0rrelati0n lD: 8f3a2b1c-4d5e-6f7a-8b9c-0d1e2f3a4b5c\n"
        "Timestarnp: 2O26-O3-18TO9:45:OOZ\"\n\n"
        "l\u2019ve tried:\n"
        "- Ciearing the Teams cache (de1eted %appdata%\\Micr0s0ft\\Tearns)\n"
        "- Reinstal1ing Tearns\n"
        "- Restarting rny c0rnputer\n\n"
        "N0thing w0rks. l need Teams f0r a cl1ent call at 2 PM.\n\n"
        "Thanks,\n"
        "Rache1 Kim\n"
        "Acc0unt Management"
    )

    return EvalScenario(
        ticket=Ticket(
            ticket_id="INC-9202",
            subject="Teams err0r — CAA2000B — cant j0in meetings",
            description=description,
            reporter=Reporter(
                name="Rachel Kim",
                email="rachel.kim@contoso.com",
                department="Account Management",
            ),
            created_at="2026-03-18T10:00:00Z",
            channel=TicketChannel.PORTAL,
            attachments=["teams_error_screenshot.png"],
        ),
        gold=TriageDecision(
            ticket_id="INC-9202",
            category=TicketCategory.SOFTWARE,
            priority=Priority.P3,
            assigned_team=AssignedTeam.ENTERPRISE_APPS,
            needs_escalation=False,
            missing_information=[
                MissingInfoField.DEVICE_INFO,
                MissingInfoField.APPLICATION_VERSION,
            ],
            next_best_action=(
                "Investigate Microsoft Teams error CAA2000B. This error typically indicates "
                "an authentication or conditional access issue. Check Azure AD sign-in logs "
                "and Conditional Access policies."
            ),
            remediation_steps=[
                "Check Azure AD sign-in logs for the user to identify authentication failures",
                "Verify Conditional Access policies are not blocking the Teams desktop client",
                "Clear cached credentials from Windows Credential Manager in addition to Teams cache",
                "If CAA2000B persists, check for proxy or firewall rules blocking Teams auth endpoints",
            ],
        ),
        tag=_TAG,
        test_name="screenshot_ocr_errors",
        test_description=(
            "Tests handling of OCR-transcribed text with systematic recognition errors: "
            "0/O confusion, l/1/I swaps, rn/m substitutions. The model must parse through "
            "OCR noise to extract the real error code and issue."
        ),
    )


def _powerpoint_clipboard_paste() -> EvalScenario:
    """Ticket created by pasting from PowerPoint with formatting artifacts."""
    description = (
        "\u2022 SLIDE 1 OF 12\n"
        "Q1 Infrastructure Review\n"
        "Contoso Financial Services \u2014 IT Operations\n"
        "CONFIDENTIAL\n\n"
        "Click to edit Master title style\n"
        "Click to edit Master subtitle style\n\n"
        "\u2022 SLIDE 4 OF 12\n"
        "Issue: Shared Drive Performance\n\n"
        "\t\u25ba Response times on \\\\contoso-fs01\\shared have degraded from <100ms to >3s\n"
        "\t\u25ba Affecting ~150 users in the London and Singapore offices\n"
        "\t\u25ba Started after the storage array firmware update on March 14\n"
        "\t\u25ba Finance team cannot open large Excel models (>50MB) from the share\n\n"
        "Speaker Notes: Ask IT to check if the NetApp firmware update caused a regression "
        "on the CIFS shares. Bob mentioned something about jumbo frames being disabled.\n\n"
        "\u2022 SLIDE 5 OF 12\n"
        "Impact Assessment\n\n"
        "\t\u25ba Business impact: HIGH \u2014 month-end close delayed\n"
        "\t\u25ba Users affected: Finance (London), Risk (Singapore)\n"
        "\t\u25ba Workaround: Copy files locally first (not ideal for 50MB+ files)\n\n"
        "Click to add notes\n\n"
        "\u2022 SLIDE 12 OF 12\n"
        "Thank You\n"
        "Questions?\n"
        "Contact: infrastructure@contoso.com\n"
    )

    return EvalScenario(
        ticket=Ticket(
            ticket_id="INC-9203",
            subject="Shared drive performance — see attached deck",
            description=description,
            reporter=Reporter(
                name="Tom Bradley",
                email="tom.bradley@contoso.com",
                department="IT Operations",
            ),
            created_at="2026-03-18T11:30:00Z",
            channel=TicketChannel.EMAIL,
            attachments=["Q1_Infrastructure_Review.pptx"],
        ),
        gold=TriageDecision(
            ticket_id="INC-9203",
            category=TicketCategory.DATA_STORAGE,
            priority=Priority.P2,
            assigned_team=AssignedTeam.DATA_PLATFORM,
            needs_escalation=False,
            missing_information=[
                MissingInfoField.CONFIGURATION_DETAILS,
            ],
            next_best_action=(
                "Investigate shared drive performance degradation on \\\\contoso-fs01\\shared "
                "after the NetApp storage array firmware update on March 14. Check CIFS share "
                "configuration and jumbo frame settings."
            ),
            remediation_steps=[
                "Review NetApp firmware update changelog for known CIFS performance regressions",
                "Check if jumbo frames were disabled during the firmware update and re-enable if appropriate",
                "Monitor CIFS response times on contoso-fs01 and compare with pre-update baseline",
                "If firmware-related, consider rolling back or applying a hotfix from NetApp",
                "Confirm Finance and Risk teams can open large files with acceptable performance",
            ],
        ),
        tag=_TAG,
        test_name="powerpoint_clipboard_paste",
        test_description=(
            "Tests handling of content pasted from a PowerPoint presentation: slide headers, "
            "placeholder text ('Click to edit Master title style'), speaker notes, and bullet "
            "formatting artifacts. The real issue is buried across multiple slides."
        ),
    )


def _auto_translation_artifacts() -> EvalScenario:
    """Ticket run through machine translation with awkward phrasing and artifacts."""
    description = (
        "[Auto-translated from Japanese by Google Translate]\n\n"
        "The printer of our floor does not do printing. When the document is sent to the "
        "printer, the work enters the queue but it is stuck in the state of \"sending\". "
        "The printer display says \"Ready\" but it is lying.\n\n"
        "Things we have already tried to do:\n"
        "- The restart of the printer (the power was turned off and on again)\n"
        "- The deletion of all works from the print queue\n"
        "- The reinstallation of the driver of the printer\n"
        "- The connection of the USB cable was confirmed to be tight\n\n"
        "The model of the printer: HP LaserJet Enterprise M507dn\n"
        "The location: Tokyo office, 4th floor, near to the pantry\n"
        "The IP address of the printer: 10.20.4.100\n\n"
        "This printer is used by approximately 40 persons of the team. "
        "Since yesterday\u2019s afternoon, nobody has been able to make printing. "
        "We are now going to the 3rd floor to use their printer but it is very "
        "inconvenient because of the distance.\n\n"
        "Please do the investigation with urgency. Thank you for your cooperation.\n\n"
        "[Original language: \u65e5\u672c\u8a9e / End of translation]"
    )

    return EvalScenario(
        ticket=Ticket(
            ticket_id="INC-9204",
            subject="[Translated] The printer does not do printing — Tokyo 4F",
            description=description,
            reporter=Reporter(
                name="Takeshi Yamamoto",
                email="takeshi.yamamoto@contoso.com",
                department="Operations",
            ),
            created_at="2026-03-18T01:30:00Z",
            channel=TicketChannel.PORTAL,
            attachments=[],
        ),
        gold=TriageDecision(
            ticket_id="INC-9204",
            category=TicketCategory.HARDWARE,
            priority=Priority.P3,
            assigned_team=AssignedTeam.ENDPOINT_ENG,
            needs_escalation=False,
            missing_information=[
                MissingInfoField.ERROR_MESSAGE,
            ],
            next_best_action=(
                "Investigate HP LaserJet Enterprise M507dn print queue stuck in 'sending' state "
                "at the Tokyo office 4th floor. Printer reports ready but jobs are not printing. "
                "Affects ~40 users."
            ),
            remediation_steps=[
                "Check network connectivity to the printer at 10.20.4.100 (ping, SNMP status)",
                "Review the print server spooler for stuck jobs and clear the queue",
                "Verify the print driver is compatible and check for firmware updates on the HP M507dn",
                "Test printing directly via USB to isolate network vs. printer hardware issue",
                "If network-related, check the switch port and VLAN configuration for the printer",
            ],
        ),
        tag=_TAG,
        test_name="auto_translation_artifacts",
        test_description=(
            "Tests handling of machine-translated text with awkward phrasing, over-literal "
            "translations ('does not do printing', 'the restart of the printer'), and "
            "translation metadata tags. The technical details are present but linguistically garbled."
        ),
    )


def _voice_dictation_errors() -> EvalScenario:
    """Ticket dictated via speech-to-text with homophones and punctuation errors."""
    description = (
        "hey so i need to report a nit work issue um our sails force application "
        "is loading really slow like takes about too minutes just too see the home "
        "page and its been like this for a weak now i think sense the last up date "
        "um my colleagues are having the same issue to so its not just me\n\n"
        "eye tried clearing the cash and using in cog neat oh mode in chrome but "
        "it didnt help the loading bar gets to about a tea percent and then just "
        "sits their four ever\n\n"
        "were in the new york office on the ate floor and we all use chrome version "
        "won twenty too i think the i tea team pushed some kind of proxy change last "
        "weak that mite be related\n\n"
        "this is really affecting hour productivity because we cant log client in "
        "her actions in a timely manor please look in two this as soon as possible\n\n"
        "thanks mike davis sails department"
    )

    return EvalScenario(
        ticket=Ticket(
            ticket_id="INC-9205",
            subject="sails force loading slow — new york office",
            description=description,
            reporter=Reporter(
                name="Mike Davis",
                email="mike.davis@contoso.com",
                department="Sales",
            ),
            created_at="2026-03-18T10:15:00Z",
            channel=TicketChannel.PHONE,
            attachments=[],
        ),
        gold=TriageDecision(
            ticket_id="INC-9205",
            category=TicketCategory.SOFTWARE,
            priority=Priority.P3,
            assigned_team=AssignedTeam.ENTERPRISE_APPS,
            needs_escalation=False,
            missing_information=[
                MissingInfoField.APPLICATION_VERSION,
            ],
            next_best_action=(
                "Investigate Salesforce slow loading (~2 minutes to homepage) affecting "
                "multiple users on Floor 8 of the New York office. Likely related to a "
                "recent proxy configuration change. Check proxy and network settings."
            ),
            remediation_steps=[
                "Check the recent proxy configuration change for any impact on Salesforce traffic",
                "Test Salesforce loading times from the New York office with and without the proxy",
                "Verify Salesforce is on the proxy bypass list if applicable",
                "Check Salesforce status page for any ongoing performance incidents",
                "If proxy-related, update the configuration to restore normal Salesforce performance",
            ],
        ),
        tag=_TAG,
        test_name="voice_dictation_errors",
        test_description=(
            "Tests handling of speech-to-text dictation errors: homophones (too/to/two, "
            "their/there, eye/I, weak/week), missing punctuation, and phonetic misspellings "
            "(nit work, sails force, in cog neat oh). The underlying issue is clear but "
            "heavily garbled."
        ),
    )


def _sms_chat_shorthand() -> EvalScenario:
    """Ultra-terse SMS/chat-style ticket with abbreviations and shorthand."""
    description = (
        "yo vpn ded again lol\n"
        "cant connect 2 anything\n"
        "err msg says smth abt cert expired??\n"
        "tried reboot no luck\n"
        "need asap got demo @ 3\n"
        "thx"
    )

    return EvalScenario(
        ticket=Ticket(
            ticket_id="INC-9206",
            subject="vpn broke",
            description=description,
            reporter=Reporter(
                name="Jake Torres",
                email="jake.torres@contoso.com",
                department="Engineering",
            ),
            created_at="2026-03-18T13:45:00Z",
            channel=TicketChannel.CHAT,
            attachments=[],
        ),
        gold=TriageDecision(
            ticket_id="INC-9206",
            category=TicketCategory.NETWORK,
            priority=Priority.P3,
            assigned_team=AssignedTeam.NETWORK_OPS,
            needs_escalation=False,
            missing_information=[
                MissingInfoField.DEVICE_INFO,
                MissingInfoField.ERROR_MESSAGE,
                MissingInfoField.APPLICATION_VERSION,
            ],
            next_best_action=(
                "Investigate VPN connection failure with possible certificate expiry error. "
                "Check VPN gateway certificate status and client configuration."
            ),
            remediation_steps=[
                "Check VPN gateway certificate expiry status",
                "If certificate is expired, renew and deploy the updated certificate",
                "Verify the VPN client has the correct root CA certificates installed",
                "Test VPN connectivity after certificate remediation",
            ],
        ),
        tag=_TAG,
        test_name="sms_chat_shorthand",
        test_description=(
            "Tests handling of ultra-terse SMS/chat-style input with abbreviations "
            "(2=to, abt=about, smth=something, thx=thanks, ded=dead, asap, @=at). "
            "Minimal punctuation and maximum brevity."
        ),
    )


def _sql_result_dump() -> EvalScenario:
    """User pasted raw SQL query results into the ticket description."""
    sql_output = (
        "mysql> SELECT id, status, error_msg, created_at FROM sync_jobs "
        "WHERE status = 'FAILED' ORDER BY created_at DESC LIMIT 20;\n"
        "+-------+--------+------------------------------------------+---------------------+\n"
        "| id    | status | error_msg                                | created_at          |\n"
        "+-------+--------+------------------------------------------+---------------------+\n"
        "| 10842 | FAILED | ORA-01017: invalid username/password     | 2026-03-18 08:00:01 |\n"
        "| 10841 | FAILED | ORA-01017: invalid username/password     | 2026-03-18 07:00:01 |\n"
        "| 10840 | FAILED | ORA-01017: invalid username/password     | 2026-03-18 06:00:01 |\n"
        "| 10839 | FAILED | ORA-01017: invalid username/password     | 2026-03-18 05:00:01 |\n"
        "| 10838 | FAILED | ORA-01017: invalid username/password     | 2026-03-18 04:00:01 |\n"
        "| 10837 | FAILED | ORA-01017: invalid username/password     | 2026-03-18 03:00:01 |\n"
        "| 10836 | FAILED | ORA-01017: invalid username/password     | 2026-03-18 02:00:01 |\n"
        "| 10835 | FAILED | ORA-01017: invalid username/password     | 2026-03-18 01:00:01 |\n"
        "| 10834 | FAILED | ORA-01017: invalid username/password     | 2026-03-17 23:00:01 |\n"
        "| 10833 | FAILED | ORA-01017: invalid username/password     | 2026-03-17 22:00:01 |\n"
        "+-------+--------+------------------------------------------+---------------------+\n"
        "10 rows in set (0.03 sec)\n"
    )

    description = (
        "Our Oracle-to-Snowflake data sync has been failing since last night. "
        "Here are the last 10 failures:\n\n"
        + sql_output
        + "\n"
        "All failures show the same Oracle auth error. I suspect the service account "
        "password was rotated by the DBA team without updating our sync config. "
        "The sync job runs hourly and feeds our BI dashboards — the dashboards are now "
        "12+ hours stale.\n\n"
        "Service account: svc_oracle_sync\n"
        "Source: Oracle DB (ora-prod-01.contoso.com)\n"
        "Target: Snowflake (contoso.snowflakecomputing.com)"
    )

    return EvalScenario(
        ticket=Ticket(
            ticket_id="INC-9207",
            subject="Oracle sync job failing — ORA-01017 auth errors since last night",
            description=description,
            reporter=Reporter(
                name="Priya Sharma",
                email="priya.sharma@contoso.com",
                department="Data Engineering",
            ),
            created_at="2026-03-18T08:30:00Z",
            channel=TicketChannel.PORTAL,
            attachments=["sync_job_full_log.txt"],
        ),
        gold=TriageDecision(
            ticket_id="INC-9207",
            category=TicketCategory.ACCESS_AUTH,
            priority=Priority.P2,
            assigned_team=AssignedTeam.DATA_PLATFORM,
            needs_escalation=False,
            missing_information=[],
            next_best_action=(
                "Investigate ORA-01017 authentication failure for service account svc_oracle_sync. "
                "Likely caused by a password rotation. Update sync configuration with the new "
                "credentials to restore the hourly Oracle-to-Snowflake data pipeline."
            ),
            remediation_steps=[
                "Confirm with the DBA team whether the svc_oracle_sync password was recently rotated",
                "Update the Oracle sync job configuration with the current service account credentials",
                "Test connectivity from the sync server to ora-prod-01.contoso.com with the new credentials",
                "Trigger a manual sync run to backfill the 12+ hours of stale data",
                "Verify BI dashboards are displaying current data after the sync completes",
            ],
        ),
        tag=_TAG,
        test_name="sql_result_dump",
        test_description=(
            "Tests handling of raw SQL query output (mysql CLI format with ASCII table borders) "
            "pasted into the ticket description. The model must parse through the tabular output "
            "to identify the repeated ORA-01017 error pattern."
        ),
    )


def _webpack_build_output() -> EvalScenario:
    """Developer pasted webpack/npm build output as the ticket description."""
    build_output = (
        "$ npm run build\n\n"
        "> contoso-portal@4.2.1 build\n"
        "> webpack --config webpack.prod.js\n\n"
        "asset main.8a3f2b1c.js 2.4 MiB [emitted] [minimized] (name: main) 1 related asset\n"
        "asset vendors.3d5e7f9a.js 1.8 MiB [emitted] [minimized] (name: vendors)\n"
        "asset styles.b2c4d6e8.css 342 KiB [emitted] (name: styles)\n"
        "asset runtime.f0a1b2c3.js 12.4 KiB [emitted] [minimized] (name: runtime)\n"
        "Entrypoint main [big] 4.5 MiB (5.2 MiB) = runtime.f0a1b2c3.js 12.4 KiB "
        "vendors.3d5e7f9a.js 1.8 MiB styles.b2c4d6e8.css 342 KiB main.8a3f2b1c.js 2.4 MiB\n\n"
        "WARNING in asset size limit: The following asset(s) exceed the recommended size limit (244 KiB).\n"
        "  main.8a3f2b1c.js (2.4 MiB)\n"
        "  vendors.3d5e7f9a.js (1.8 MiB)\n\n"
        "WARNING in entrypoint size limit: The following entrypoint(s) combined asset size exceeds "
        "the recommended limit (244 KiB).\n"
        "  main (4.5 MiB)\n\n"
        "ERROR in ./src/components/ClientDashboard/index.tsx 47:12\n"
        "Module not found: Error: Can't resolve '@contoso/shared-auth' in "
        "'/app/src/components/ClientDashboard'\n\n"
        "ERROR in ./src/services/api.ts 3:0-52\n"
        "Module not found: Error: Can't resolve '@contoso/shared-auth' in "
        "'/app/src/services'\n\n"
        "webpack 5.91.0 compiled with 2 errors and 2 warnings in 45230 ms\n"
    )

    description = (
        "The internal client portal build is broken on the CI/CD pipeline. Full output:\n\n"
        + build_output
        + "\nThis started after the shared-auth package was moved to a new npm registry "
        "yesterday. The build worked fine on Monday. We can\u2019t deploy the hotfix for the "
        "client dashboard bug (INC-9150) until this is resolved.\n\n"
        "Build pipeline: Azure DevOps > contoso-portal > main branch\n"
        "Last successful build: #4217 (2026-03-17T16:00:00Z)"
    )

    return EvalScenario(
        ticket=Ticket(
            ticket_id="INC-9208",
            subject="CI/CD build broken — client portal can't resolve @contoso/shared-auth",
            description=description,
            reporter=Reporter(
                name="Alex Chen",
                email="alex.chen@contoso.com",
                department="Engineering",
            ),
            created_at="2026-03-18T10:45:00Z",
            channel=TicketChannel.PORTAL,
            attachments=["build_log_4218.txt"],
        ),
        gold=TriageDecision(
            ticket_id="INC-9208",
            category=TicketCategory.SOFTWARE,
            priority=Priority.P2,
            assigned_team=AssignedTeam.ENTERPRISE_APPS,
            needs_escalation=False,
            missing_information=[
                MissingInfoField.CONFIGURATION_DETAILS,
            ],
            next_best_action=(
                "Investigate CI/CD build failure caused by unresolvable @contoso/shared-auth "
                "package after npm registry migration. Update the .npmrc or package registry "
                "configuration to point to the new registry location."
            ),
            remediation_steps=[
                "Verify the @contoso/shared-auth package is published to the new npm registry",
                "Update the .npmrc or pipeline configuration with the new registry URL",
                "Clear the npm cache in the CI/CD pipeline and re-run the build",
                "Verify build #4219 completes successfully with no module resolution errors",
                "Deploy the pending client dashboard hotfix (INC-9150) once the build is green",
            ],
        ),
        tag=_TAG,
        test_name="webpack_build_output",
        test_description=(
            "Tests handling of raw webpack/npm build output with asset listings, size warnings, "
            "and module resolution errors. The model must identify the actual errors (missing "
            "@contoso/shared-auth) amid verbose build noise."
        ),
    )


def _macos_crash_report() -> EvalScenario:
    """User pasted a macOS crash report with stack traces into the ticket."""
    crash_report = (
        "Process:               Microsoft Outlook [12847]\n"
        "Path:                  /Applications/Microsoft Outlook.app/Contents/MacOS/Microsoft Outlook\n"
        "Identifier:            com.microsoft.Outlook\n"
        "Version:               16.83 (24031820)\n"
        "Code Type:             ARM-64 (Native)\n"
        "Parent Process:        launchd [1]\n\n"
        "Date/Time:             2026-03-18 08:12:33.482 +0000\n"
        "OS Version:            macOS 14.4 (23E214)\n\n"
        "Exception Type:        EXC_CRASH (SIGABRT)\n"
        "Exception Codes:       0x0000000000000000, 0x0000000000000000\n\n"
        "Termination Reason:    Namespace SIGNAL, Code 6 Abort trap: 6\n\n"
        "Thread 0 Crashed:\n"
        "0   libsystem_kernel.dylib        0x1a2b3c4d5 __pthread_kill + 8\n"
        "1   libsystem_pthread.dylib       0x1a2b3c4d6 pthread_kill + 288\n"
        "2   libsystem_c.dylib             0x1a2b3c4d7 abort + 128\n"
        "3   com.microsoft.Outlook         0x1001a2b3c -[MSOutlookDatabase openMailbox:] + 412\n"
        "4   com.microsoft.Outlook         0x1001a2b3d -[MSOutlookSyncEngine startSync:] + 248\n"
        "5   com.microsoft.Outlook         0x1001a2b3e -[MSOutlookAppDelegate applicationDidFinishLaunching:] + 1024\n"
        "6   AppKit                        0x1a3b4c5d6 -[NSApplication _sendFinishLaunchingNotification] + 208\n\n"
        "Thread 1:\n"
        "0   libsystem_kernel.dylib        0x1a2b3c4d8 __workq_kernreturn + 8\n"
        "1   libsystem_pthread.dylib       0x1a2b3c4d9 _pthread_wqthread + 364\n\n"
        "Binary Images:\n"
        "0x100000000 - 0x10234ffff  com.microsoft.Outlook (16.83) <ABC12345-DEF6-7890-ABCD-EF1234567890> /Applications/Microsoft Outlook.app/Contents/MacOS/Microsoft Outlook\n"
    )

    description = (
        "Outlook crashes every time I open it on my MacBook. It opens for about 2 seconds "
        "then immediately closes. I\u2019ve tried reinstalling but the same thing happens. "
        "Here\u2019s the crash report:\n\n"
        + crash_report
        + "\nThis started today. I have a Board of Directors meeting at 1 PM and all my "
        "prep emails are in Outlook. Using OWA as a workaround for now but it\u2019s not ideal.\n\n"
        "Device: MacBook Pro M3, macOS 14.4\n"
        "Outlook version: 16.83"
    )

    return EvalScenario(
        ticket=Ticket(
            ticket_id="INC-9209",
            subject="Outlook crashing on launch — macOS crash report inside",
            description=description,
            reporter=Reporter(
                name="Margaret Chen",
                email="margaret.chen@contoso.com",
                department="Executive Office",
            ),
            created_at="2026-03-18T08:30:00Z",
            channel=TicketChannel.EMAIL,
            attachments=["outlook_crash_report.txt"],
        ),
        gold=TriageDecision(
            ticket_id="INC-9209",
            category=TicketCategory.SOFTWARE,
            priority=Priority.P2,
            assigned_team=AssignedTeam.ENDPOINT_ENG,
            needs_escalation=False,
            missing_information=[],
            next_best_action=(
                "Investigate Outlook 16.83 crash on launch on macOS 14.4 (MacBook Pro M3). "
                "Crash occurs in MSOutlookDatabase openMailbox during sync engine startup. "
                "Likely a corrupt mailbox database — rebuild the Outlook profile."
            ),
            remediation_steps=[
                "Remove and rebuild the Outlook profile to clear a potentially corrupt local database",
                "If rebuild fails, delete the Outlook data in ~/Library/Group Containers and re-add the account",
                "Check for Outlook updates — 16.83 may have a known crash bug fixed in a newer build",
                "Verify the user can access emails in OWA as a temporary workaround before the 1 PM meeting",
                "If issue persists after profile rebuild, collect a sysdiagnose and escalate to Microsoft support",
            ],
        ),
        tag=_TAG,
        test_name="macos_crash_report",
        test_description=(
            "Tests handling of a macOS crash report with full stack traces, binary image "
            "listings, and kernel exception details pasted into the description. The model "
            "must extract the crashing application and relevant crash context from low-level "
            "system diagnostics."
        ),
    )


def _browser_console_dump() -> EvalScenario:
    """User pasted browser DevTools console output into the ticket."""
    console_output = (
        "[HMR] Waiting for update signal from WDS...\n"
        "react-dom.development.js:86 Warning: ReactDOM.render is no longer supported in React 18.\n"
        "auth.js:142 POST https://api.contoso.com/v2/auth/token 401 (Unauthorized)\n"
        "auth.js:143 Error: Authentication failed: Token refresh returned 401\n"
        "    at refreshToken (auth.js:142:15)\n"
        "    at async handleApiCall (api-client.js:87:22)\n"
        "    at async loadDashboard (dashboard.js:34:18)\n"
        "auth.js:156 Retry 1/3: Attempting token refresh...\n"
        "auth.js:142 POST https://api.contoso.com/v2/auth/token 401 (Unauthorized)\n"
        "auth.js:156 Retry 2/3: Attempting token refresh...\n"
        "auth.js:142 POST https://api.contoso.com/v2/auth/token 401 (Unauthorized)\n"
        "auth.js:156 Retry 3/3: Attempting token refresh...\n"
        "auth.js:142 POST https://api.contoso.com/v2/auth/token 401 (Unauthorized)\n"
        "auth.js:161 Error: All token refresh attempts failed. Redirecting to login.\n"
        "    at handleRefreshFailure (auth.js:161:11)\n"
        "    at async refreshToken (auth.js:155:5)\n"
        "navigation.js:23 Navigating to /login?reason=token_expired&redirect=/dashboard\n"
        "index.js:44 [Sentry] Captured exception: AuthenticationError: Token refresh failed\n"
        "index.js:44 [Sentry] Event ID: a1b2c3d4e5f6\n"
        "favicon.ico:1 GET https://portal.contoso.com/favicon.ico 404 (Not Found)\n"
        "manifest.json:1 Manifest: Line: 1, column: 1, Syntax error.\n"
    )

    description = (
        "The internal portal keeps logging me out every 5 minutes. I log in, use it for "
        "a few minutes, then get bounced back to the login page. Happening all day. "
        "Opened the browser console and this is what I see:\n\n"
        + console_output
        + "\nLooks like the token refresh is failing? Multiple people on my team are seeing "
        "the same thing. We\u2019re all on Chrome 122 in the NYC office. The portal worked "
        "fine yesterday.\n\n"
        "This is blocking our client onboarding work \u2014 we can\u2019t stay logged in long "
        "enough to complete a single form."
    )

    return EvalScenario(
        ticket=Ticket(
            ticket_id="INC-9210",
            subject="Portal keeps logging us out — console errors inside",
            description=description,
            reporter=Reporter(
                name="Jason Park",
                email="jason.park@contoso.com",
                department="Client Services",
            ),
            created_at="2026-03-18T14:30:00Z",
            channel=TicketChannel.PORTAL,
            attachments=[],
        ),
        gold=TriageDecision(
            ticket_id="INC-9210",
            category=TicketCategory.SOFTWARE,
            priority=Priority.P2,
            assigned_team=AssignedTeam.ENTERPRISE_APPS,
            needs_escalation=False,
            missing_information=[],
            next_best_action=(
                "Investigate token refresh failure (401 Unauthorized) on the internal portal "
                "at api.contoso.com/v2/auth/token. Affecting multiple users in Client Services. "
                "Check the authentication service and token signing configuration."
            ),
            remediation_steps=[
                "Check the auth token service at api.contoso.com/v2/auth/token for errors or misconfigurations",
                "Verify the token signing key or certificate has not expired or been rotated without updating the portal",
                "Review recent deployments or configuration changes to the auth service",
                "Check Sentry for the captured AuthenticationError events for additional context",
                "Confirm the portal maintains sessions correctly after the fix is applied",
            ],
        ),
        tag=_TAG,
        test_name="browser_console_dump",
        test_description=(
            "Tests handling of raw browser DevTools console output with JavaScript errors, "
            "network request failures, stack traces, HMR noise, and Sentry logs. The model "
            "must identify the auth token refresh failure as the root cause."
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
        _pdf_text_extraction(),
        _screenshot_ocr_errors(),
        _powerpoint_clipboard_paste(),
        _auto_translation_artifacts(),
        _voice_dictation_errors(),
        _sms_chat_shorthand(),
        _sql_result_dump(),
        _webpack_build_output(),
        _macos_crash_report(),
        _browser_console_dump(),
    ]
