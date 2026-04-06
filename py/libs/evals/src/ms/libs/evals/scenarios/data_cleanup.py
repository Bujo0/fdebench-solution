"""Data cleanup evaluation scenarios.

Tests the triage API's ability to handle messy, noisy, or malformed input
while still extracting the underlying support request and producing correct
triage decisions.
"""

from ms.libs.evals.models.enums import AssignedTeam
from ms.libs.evals.models.enums import MissingInfoField
from ms.libs.evals.models.enums import Priority
from ms.libs.evals.models.enums import ScenarioTag
from ms.libs.evals.models.enums import TicketCategory
from ms.libs.evals.models.enums import TicketChannel
from ms.libs.evals.models.scenario import EvalScenario
from ms.libs.evals.models.scenario import Reporter
from ms.libs.evals.models.scenario import Ticket
from ms.libs.evals.models.scenario import TriageDecision

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
        'Location: Building 2, Ground Floor, Café "Thé Crème"\n'
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
        repeated_block * 3 + "\n\nACTUAL ISSUE: My Salesforce account shows 'License expired' when I try to "
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
                "If permissions are correct, check for Conditional Access policies"
                " that may block after password change",
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
        "Our ETL service account keeps failing to authenticate. Here are the logs:\n\n" + log_lines + "\n\n"
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
        '"We\u2019re s0rry\u2014we\u2019ve run int0 an 1ssue.\n'
        "Err0r c0de: CAA2000B\n"
        "C0rrelati0n lD: 8f3a2b1c-4d5e-6f7a-8b9c-0d1e2f3a4b5c\n"
        'Timestarnp: 2O26-O3-18TO9:45:OOZ"\n\n'
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
        'printer, the work enters the queue but it is stuck in the state of "sending". '
        'The printer display says "Ready" but it is lying.\n\n'
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
        "Here are the last 10 failures:\n\n" + sql_output + "\n"
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
        "0x100000000 - 0x10234ffff  com.microsoft.Outlook (16.83)"
        " <ABC12345-DEF6-7890-ABCD-EF1234567890>"
        " /Applications/Microsoft Outlook.app/Contents/MacOS/Microsoft Outlook\n"
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
                "Verify the token signing key or certificate has not expired"
                " or been rotated without updating the portal",
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


def _terraform_state_dump() -> EvalScenario:
    """Terraform state JSON pasted in a cloud provisioning issue."""
    return EvalScenario(
        ticket=Ticket(
            ticket_id="INC-9211",
            subject="Azure VM provisioning stuck in pending state",
            description=(
                '{"version": 4, "terraform_version": "1.7.3", "serial": 42,\n'
                '"lineage": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",\n'
                '"outputs": {"vm_public_ip": {"value": "20.62.134.87", "type": "string"}},\n'
                '"resources": [{"module": "module.compute", "mode": "managed",\n'
                '"type": "azurerm_linux_virtual_machine", "name": "analytics_vm",\n'
                '"provider": "provider[\\"registry.terraform.io/hashicorp/azurerm\\"]",\n'
                '"instances": [{"schema_version": 0,\n'
                '"attributes": {"id": "/subscriptions/xxxx/resourceGroups/rg-analytics-prod/'
                'providers/Microsoft.Compute/virtualMachines/vm-analytics-01",\n'
                '"name": "vm-analytics-01", "location": "eastus2",\n'
                '"size": "Standard_D8s_v5", "admin_username": "azureadmin",\n'
                '"network_interface_ids": ["/subscriptions/xxxx/..."],\n'
                '"os_disk": {"caching": "ReadWrite", "storage_account_type": "Premium_LRS",\n'
                '"disk_size_gb": 128}, "source_image_reference": {\n'
                '"publisher": "Canonical", "offer": "0001-com-ubuntu-server-jammy",\n'
                '"sku": "22_04-lts-gen2", "version": "latest"},\n'
                '"provisioning_state": "Creating"}}]}]}\n\n'
                "The Terraform state above shows vm-analytics-01 stuck in 'Creating' state "
                "for over 2 hours. We need this VM for the quarterly analytics pipeline that "
                "runs tomorrow. The provisioning seems to hang at the NIC attachment stage."
            ),
            reporter=Reporter(
                name="Dmitri Volkov",
                email="dmitri.volkov@contoso.com",
                department="Cloud Infrastructure",
            ),
            created_at="2026-03-18T14:30:00Z",
            channel=TicketChannel.PORTAL,
            attachments=[],
        ),
        gold=TriageDecision(
            ticket_id="INC-9211",
            category=TicketCategory.SOFTWARE,
            priority=Priority.P2,
            assigned_team=AssignedTeam.ENTERPRISE_APPS,
            needs_escalation=False,
            missing_information=[MissingInfoField.ERROR_MESSAGE],
            next_best_action=(
                "Investigate Azure VM provisioning stuck in 'Creating' state for vm-analytics-01 "
                "in rg-analytics-prod. Check Azure Activity Log and NIC allocation for the stuck resource."
            ),
            remediation_steps=[
                "Check Azure Activity Log for provisioning errors on vm-analytics-01",
                "Verify subnet and NIC availability in the target VNet",
                "If stuck, cancel and re-run the Terraform apply with -target flag for the VM resource",
            ],
        ),
        tag=_TAG,
        test_name="terraform_state_dump",
        test_description=(
            "Tests handling of Terraform state JSON pasted inline in a cloud provisioning issue. "
            "The model must extract the real issue (VM stuck in Creating state) from the JSON noise."
        ),
    )


def _graphql_query_paste() -> EvalScenario:
    """GraphQL mutation pasted in an API issue."""
    return EvalScenario(
        ticket=Ticket(
            ticket_id="INC-9212",
            subject="Portfolio API mutation returns 500 since deployment",
            description=(
                "Since this morning's release the updatePortfolioAllocation mutation is failing:\n\n"
                "```graphql\n"
                "mutation UpdateAllocation($input: AllocationInput!) {\n"
                "  updatePortfolioAllocation(input: $input) {\n"
                "    portfolio { id name allocations { assetClass weight targetWeight } }\n"
                "    errors { field message code }\n"
                "  }\n"
                "}\n"
                "```\n\n"
                'Variables: {"input": {"portfolioId": "PF-88291", "allocations": [\n'
                '  {"assetClass": "US_EQUITY", "weight": 0.45},\n'
                '  {"assetClass": "INTL_EQUITY", "weight": 0.25},\n'
                '  {"assetClass": "FIXED_INCOME", "weight": 0.20},\n'
                '  {"assetClass": "ALTERNATIVES", "weight": 0.10}\n'
                "]}}\n\n"
                'Response: {"errors": [{"message": "Internal server error",\n'
                '"extensions": {"code": "INTERNAL_SERVER_ERROR",\n'
                '"exception": {"stacktrace": ["Error: Cannot read properties of null '
                "(reading 'validateWeights')\",\n"
                '"    at PortfolioResolver.updateAllocation (portfolio-resolver.ts:142:38)"]}}}]}\n\n'
                "This affects all portfolio managers trying to rebalance after the March review."
            ),
            reporter=Reporter(
                name="Aisha Patel",
                email="aisha.patel@contoso.com",
                department="Portfolio Management",
            ),
            created_at="2026-03-18T10:15:00Z",
            channel=TicketChannel.EMAIL,
            attachments=[],
        ),
        gold=TriageDecision(
            ticket_id="INC-9212",
            category=TicketCategory.SOFTWARE,
            priority=Priority.P1,
            assigned_team=AssignedTeam.ENTERPRISE_APPS,
            needs_escalation=True,
            missing_information=[],
            next_best_action=(
                "Investigate updatePortfolioAllocation mutation returning 500 after this morning's "
                "deployment. Null reference in validateWeights suggests a breaking schema change."
            ),
            remediation_steps=[
                "Check the latest deployment diff for portfolio-resolver.ts changes",
                "Verify the validateWeights method signature and null safety",
                "If urgent, rollback the deployment to restore portfolio rebalancing",
            ],
        ),
        tag=_TAG,
        test_name="graphql_query_paste",
        test_description=(
            "Tests handling of GraphQL mutations, variables, and error responses pasted inline. "
            "The model must identify the null reference error as the root cause."
        ),
    )


def _azure_devops_pipeline_output() -> EvalScenario:
    """Azure DevOps CI/CD pipeline log output."""
    return EvalScenario(
        ticket=Ticket(
            ticket_id="INC-9213",
            subject="Build pipeline failing for compliance-service",
            description=(
                "##[section]Starting: Build compliance-service\n"
                "##[command]/usr/bin/docker build -t compliance-service:20260318.1 .\n"
                "Step 1/14 : FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build\n"
                " ---> a8b2c3d4e5f6\n"
                "Step 2/14 : WORKDIR /src\n"
                "Step 3/14 : COPY *.csproj ./\n"
                "Step 4/14 : RUN dotnet restore\n"
                "  Determining projects to restore...\n"
                "  Restored /src/ComplianceService.csproj (in 4.2 sec).\n"
                "Step 5/14 : COPY . .\n"
                "Step 6/14 : RUN dotnet build -c Release\n"
                "  Microsoft (R) Build Engine version 17.9.0+abcdef\n"
                "  Build started 03/18/2026 06:14:22.\n"
                "  CSC : error CS8032: An instance of analyzer cannot be created [/src/"
                "ComplianceService.csproj]\n"
                "  error CS0246: The type or namespace name 'ComplianceRule' could not be "
                "found (are you missing a using directive?)\n"
                "##[error]Process completed with exit code 1.\n"
                "##[section]Finishing: Build compliance-service\n\n"
                "This has been blocking our release for 2 days. The ComplianceRule class was "
                "moved to a shared library last sprint but the import wasn't updated."
            ),
            reporter=Reporter(
                name="Chen Wei",
                email="chen.wei@contoso.com",
                department="Compliance",
            ),
            created_at="2026-03-18T06:30:00Z",
            channel=TicketChannel.PORTAL,
            attachments=[],
        ),
        gold=TriageDecision(
            ticket_id="INC-9213",
            category=TicketCategory.SOFTWARE,
            priority=Priority.P2,
            assigned_team=AssignedTeam.ENTERPRISE_APPS,
            needs_escalation=False,
            missing_information=[],
            next_best_action=(
                "Fix the missing ComplianceRule import in ComplianceService.csproj after "
                "the class was moved to a shared library. Build pipeline has been blocked for 2 days."
            ),
            remediation_steps=[
                "Add the missing project reference to the shared library containing ComplianceRule",
                "Update the using directive in the affected source files",
                "Verify the build passes locally before pushing to the pipeline",
            ],
        ),
        tag=_TAG,
        test_name="azure_devops_pipeline_output",
        test_description=(
            "Tests handling of Azure DevOps CI/CD pipeline log output with Docker build steps, "
            "MSBuild errors, and section markers. Must extract the CS0246 missing type error."
        ),
    )


def _slack_webhook_payload() -> EvalScenario:
    """Slack webhook JSON notification pasted as context."""
    return EvalScenario(
        ticket=Ticket(
            ticket_id="INC-9214",
            subject="Slack integration not posting alerts to #incidents channel",
            description=(
                "Our PagerDuty-to-Slack integration stopped posting to #incidents. "
                "Here's the webhook payload we're sending:\n\n"
                '{"channel": "#incidents", "username": "PagerDuty Bot",\n'
                '"icon_emoji": ":rotating_light:",\n'
                '"attachments": [{"fallback": "P1 Alert: DB connection pool exhausted",\n'
                '"color": "#FF0000", "title": "P1 — Database Connection Pool Exhausted",\n'
                '"title_link": "https://contoso.pagerduty.com/incidents/Q1Z2A3",\n'
                '"fields": [{"title": "Service", "value": "payment-gateway", "short": true},\n'
                '{"title": "Severity", "value": "critical", "short": true},\n'
                '{"title": "Triggered", "value": "2026-03-18T07:42:00Z", "short": true}],\n'
                '"footer": "PagerDuty", "ts": 1742284920}]}\n\n'
                "Slack API returns 403 Forbidden. The webhook URL hasn't changed. Suspect "
                "the bot token was rotated during last week's Slack workspace migration."
            ),
            reporter=Reporter(
                name="Marcus Johnson",
                email="marcus.johnson@contoso.com",
                department="DevOps",
            ),
            created_at="2026-03-18T08:00:00Z",
            channel=TicketChannel.CHAT,
            attachments=[],
        ),
        gold=TriageDecision(
            ticket_id="INC-9214",
            category=TicketCategory.SOFTWARE,
            priority=Priority.P2,
            assigned_team=AssignedTeam.ENTERPRISE_APPS,
            needs_escalation=False,
            missing_information=[],
            next_best_action=(
                "Investigate Slack webhook returning 403 Forbidden for PagerDuty integration "
                "to #incidents channel. Likely caused by bot token rotation during workspace migration."
            ),
            remediation_steps=[
                "Verify the Slack bot token in PagerDuty webhook configuration",
                "Re-authorize the PagerDuty Slack app if the token was rotated",
                "Test the webhook with a manual POST to confirm the fix",
            ],
        ),
        tag=_TAG,
        test_name="slack_webhook_payload",
        test_description=(
            "Tests handling of Slack webhook JSON payloads with attachments, fields, "
            "and emoji markup. Must identify the 403 token issue as the root cause."
        ),
    )


def _registry_export() -> EvalScenario:
    """Windows Registry export pasted in a desktop issue."""
    return EvalScenario(
        ticket=Ticket(
            ticket_id="INC-9215",
            subject="Outlook keeps crashing on startup after registry edit",
            description=(
                "I was trying to fix my Outlook profile and edited the registry. "
                "Now Outlook crashes immediately on startup. Here's what I exported:\n\n"
                "Windows Registry Editor Version 5.00\n\n"
                "[HKEY_CURRENT_USER\\Software\\Microsoft\\Office\\16.0\\Outlook\\Profiles"
                "\\Default Outlook Profile]\n"
                '"DefaultProfile"="Default Outlook Profile"\n'
                '"LastChangeVer"="16.0.17928.20114"\n\n'
                "[HKEY_CURRENT_USER\\Software\\Microsoft\\Office\\16.0\\Outlook\\Profiles"
                "\\Default Outlook Profile\\9375CFF0413111d3B88A00104B2A6676]\n"
                '"01023d15"=hex:00,00,00,00\n'
                '"01023d13"=hex:01,00,00,00\n'
                '"0102664f"=hex:6d,73,70,73,74,2e,64,6c,6c,00\n\n'
                "I think I may have deleted a key I shouldn't have. Outlook version "
                "16.0.17928.20114 on Windows 11 Pro."
            ),
            reporter=Reporter(
                name="Linda Park",
                email="linda.park@contoso.com",
                department="Marketing",
            ),
            created_at="2026-03-18T15:20:00Z",
            channel=TicketChannel.PHONE,
            attachments=[],
        ),
        gold=TriageDecision(
            ticket_id="INC-9215",
            category=TicketCategory.SOFTWARE,
            priority=Priority.P3,
            assigned_team=AssignedTeam.ENTERPRISE_APPS,
            needs_escalation=False,
            missing_information=[MissingInfoField.ERROR_MESSAGE],
            next_best_action=(
                "Restore Outlook profile after user's registry edit caused startup crash. "
                "May need to recreate the Outlook profile or restore registry keys from backup."
            ),
            remediation_steps=[
                "Try creating a new Outlook profile via Control Panel > Mail",
                "If that fails, restore the registry keys from the user's last system restore point",
                "Verify Outlook launches correctly with the new or restored profile",
            ],
        ),
        tag=_TAG,
        test_name="registry_export",
        test_description=(
            "Tests handling of Windows Registry .reg export format with hex values and "
            "deeply nested HKEY paths. Must identify the Outlook profile corruption issue."
        ),
    )


def _xml_config_dump() -> EvalScenario:
    """Apache/Nginx XML configuration pasted in a web server issue."""
    return EvalScenario(
        ticket=Ticket(
            ticket_id="INC-9216",
            subject="Internal API gateway returning 502 after config change",
            description=(
                "After updating the nginx config, our API gateway returns 502 for all "
                "/api/v2/* routes. Here's the relevant config:\n\n"
                "server {\n"
                "    listen 443 ssl http2;\n"
                "    server_name api-gateway.contoso.internal;\n"
                "    ssl_certificate /etc/nginx/certs/contoso-internal.crt;\n"
                "    ssl_certificate_key /etc/nginx/certs/contoso-internal.key;\n\n"
                "    location /api/v2/ {\n"
                "        proxy_pass http://backend-v2;\n"
                "        proxy_set_header Host $host;\n"
                "        proxy_connect_timeout 5s;\n"
                "        proxy_read_timeout 30s;\n"
                "    }\n\n"
                "    upstream backend-v2 {\n"
                "        server 10.0.4.10:8080;\n"
                "        server 10.0.4.11:8080;\n"
                "        server 10.0.4.12:8080 down;\n"
                "    }\n"
                "}\n\n"
                "The upstream block is defined inside the server block instead of outside — "
                "I think that's the issue but I'm not sure how to fix it without downtime."
            ),
            reporter=Reporter(
                name="Raj Krishnamurthy",
                email="raj.krishnamurthy@contoso.com",
                department="Backend Engineering",
            ),
            created_at="2026-03-18T11:45:00Z",
            channel=TicketChannel.PORTAL,
            attachments=[],
        ),
        gold=TriageDecision(
            ticket_id="INC-9216",
            category=TicketCategory.NETWORK,
            priority=Priority.P1,
            assigned_team=AssignedTeam.NETWORK_OPS,
            needs_escalation=True,
            missing_information=[],
            next_best_action=(
                "Fix nginx configuration error causing 502 on all /api/v2/ routes. The upstream "
                "block is incorrectly placed inside the server block."
            ),
            remediation_steps=[
                "Move the upstream block outside the server block in the nginx config",
                "Test the config with nginx -t before reloading",
                "Reload nginx with zero-downtime: nginx -s reload",
            ],
        ),
        tag=_TAG,
        test_name="xml_config_dump",
        test_description=(
            "Tests handling of nginx configuration syntax pasted inline in a gateway issue. "
            "Must identify the misconfigured upstream block placement."
        ),
    )


def _base64_pdf_attachment() -> EvalScenario:
    """Base64-encoded PDF content inline in description."""
    _b64_fragment = "JVBERi0xLjcKMSAwIG9iago8PCAvVHlwZSAvQ2F0YWxvZyAvUGFnZXMgMiAw" * 8
    return EvalScenario(
        ticket=Ticket(
            ticket_id="INC-9217",
            subject="Cannot open compliance report PDF from SharePoint",
            description=(
                "When I try to download the Q1 compliance report from SharePoint, it opens "
                "as raw data instead of a PDF. Here's what I see in my browser:\n\n"
                f"data:application/pdf;base64,{_b64_fragment}...\n\n"
                "(truncated — the full blob is about 2MB)\n\n"
                "This happens with Chrome 122 and Edge 122. Firefox opens it correctly. "
                "The file is stored in the Compliance team's SharePoint library at "
                "contoso.sharepoint.com/sites/Compliance/Shared Documents/Q1-2026-Report.pdf"
            ),
            reporter=Reporter(
                name="Sandra Okafor",
                email="sandra.okafor@contoso.com",
                department="Compliance",
            ),
            created_at="2026-03-18T13:10:00Z",
            channel=TicketChannel.EMAIL,
            attachments=["Q1-2026-Report.pdf"],
        ),
        gold=TriageDecision(
            ticket_id="INC-9217",
            category=TicketCategory.SOFTWARE,
            priority=Priority.P3,
            assigned_team=AssignedTeam.ENTERPRISE_APPS,
            needs_escalation=False,
            missing_information=[],
            next_best_action=(
                "Investigate SharePoint PDF rendering issue in Chromium browsers. The MIME type "
                "or Content-Disposition header may be incorrect for PDF downloads."
            ),
            remediation_steps=[
                "Check the SharePoint library's MIME type settings for .pdf files",
                "Verify Content-Disposition header is set to 'attachment' not 'inline'",
                "Clear browser cache and test in an InPrivate/Incognito window",
            ],
        ),
        tag=_TAG,
        test_name="base64_pdf_attachment",
        test_description=(
            "Tests handling of base64-encoded PDF data pasted inline. The model must "
            "look past the binary noise and identify the SharePoint PDF rendering issue."
        ),
    )


def _duplicate_forward_chain() -> EvalScenario:
    """Same issue forwarded 4 times creating duplicate content."""
    return EvalScenario(
        ticket=Ticket(
            ticket_id="INC-9218",
            subject="Fwd: Fwd: Fwd: Fwd: Printer on 5th floor not working",
            description=(
                "---------- Forwarded message ----------\n"
                "From: Reception <reception@contoso.com>\n"
                "Subject: Fwd: Fwd: Fwd: Printer on 5th floor not working\n\n"
                "Hi IT, forwarding this again...\n\n"
                "---------- Forwarded message ----------\n"
                "From: Office Manager <office.mgr@contoso.com>\n"
                "Subject: Fwd: Fwd: Printer on 5th floor not working\n\n"
                "Please look into this.\n\n"
                "---------- Forwarded message ----------\n"
                "From: Floor Warden <floor5@contoso.com>\n"
                "Subject: Fwd: Printer on 5th floor not working\n\n"
                "Forwarding from Tom below.\n\n"
                "---------- Forwarded message ----------\n"
                "From: Tom Chen <tom.chen@contoso.com>\n"
                "Subject: Printer on 5th floor not working\n\n"
                "The HP LaserJet Pro M404dn on the 5th floor (near the kitchen) shows "
                "'Paper Jam' but there's no paper stuck. I've opened all trays and checked. "
                "Asset tag: PRN-5F-003. It's been like this since yesterday."
            ),
            reporter=Reporter(
                name="Reception Desk",
                email="reception@contoso.com",
                department="Facilities",
            ),
            created_at="2026-03-18T09:45:00Z",
            channel=TicketChannel.EMAIL,
            attachments=[],
        ),
        gold=TriageDecision(
            ticket_id="INC-9218",
            category=TicketCategory.HARDWARE,
            priority=Priority.P3,
            assigned_team=AssignedTeam.ENDPOINT_ENG,
            needs_escalation=False,
            missing_information=[],
            next_best_action=(
                "Investigate false paper jam error on HP LaserJet Pro M404dn (PRN-5F-003) "
                "on the 5th floor. Sensor may need cleaning or replacement."
            ),
            remediation_steps=[
                "Clean the paper path sensors with compressed air",
                "Check for any small torn paper fragments in the sensor area",
                "If the error persists, replace the paper jam sensor assembly",
            ],
        ),
        tag=_TAG,
        test_name="duplicate_forward_chain",
        test_description=(
            "Tests handling of a 4-level forward chain where the original issue is buried "
            "at the bottom. Must identify the printer paper jam sensor issue."
        ),
    )


def _rtf_format_codes() -> EvalScenario:
    """Rich Text Format codes in description."""
    return EvalScenario(
        ticket=Ticket(
            ticket_id="INC-9219",
            subject="Document formatting broken after migration",
            description=(
                "{\\rtf1\\ansi\\ansicpg1252\\deff0\\nouicompat\\deflang1033"
                "{\\fonttbl{\\f0\\fswiss\\fprq2\\fcharset0 Calibri;}}\n"
                "{\\colortbl ;\\red0\\green0\\blue0;\\red255\\green0\\blue0;}\n"
                "\\viewkind4\\uc1\\pard\\f0\\fs22 "
                "Help! After the SharePoint migration, all our Word templates show RTF codes "
                "instead of formatted text. The investment proposal template "
                "(TMPL-INV-2026-Q1) is the most critical — we have client presentations "
                "this week.\\par\n"
                "\\pard\\cf2\\b ERROR:\\cf0\\b0  The Quick Parts gallery is also empty. "
                "All custom building blocks are gone.\\par\n"
                "\\pard Normal.dotm seems corrupted. Location: "
                "C:\\\\Users\\\\james.wright\\\\AppData\\\\Roaming\\\\Microsoft\\\\Templates"
                "\\\\Normal.dotm\\par}"
            ),
            reporter=Reporter(
                name="James Wright",
                email="james.wright@contoso.com",
                department="Wealth Management",
            ),
            created_at="2026-03-18T16:00:00Z",
            channel=TicketChannel.EMAIL,
            attachments=[],
        ),
        gold=TriageDecision(
            ticket_id="INC-9219",
            category=TicketCategory.SOFTWARE,
            priority=Priority.P2,
            assigned_team=AssignedTeam.ENTERPRISE_APPS,
            needs_escalation=False,
            missing_information=[],
            next_best_action=(
                "Restore Word templates after SharePoint migration broke formatting. "
                "Normal.dotm may be corrupted and Quick Parts gallery is empty."
            ),
            remediation_steps=[
                "Rename the corrupted Normal.dotm to force Word to regenerate it",
                "Restore the investment proposal template from the migration backup",
                "Rebuild the Quick Parts gallery from the pre-migration backup",
            ],
        ),
        tag=_TAG,
        test_name="rtf_format_codes",
        test_description=(
            "Tests handling of raw RTF markup codes in the ticket description. Must extract "
            "the real issue: corrupted Word templates after SharePoint migration."
        ),
    )


def _teams_chat_export() -> EvalScenario:
    """Microsoft Teams chat export with JSON metadata."""
    return EvalScenario(
        ticket=Ticket(
            ticket_id="INC-9220",
            subject="Teams meeting recordings not saving to OneDrive",
            description=(
                '{"@odata.context": "https://graph.microsoft.com/v1.0/$metadata#chats/'
                'messages",\n'
                '"value": [{"id": "1742284800000", "messageType": "message",\n'
                '"createdDateTime": "2026-03-18T08:00:00Z",\n'
                '"from": {"user": {"displayName": "Olivia Santos",\n'
                '"id": "a1b2c3d4-e5f6-7890"}},\n'
                '"body": {"content": "Has anyone else noticed that meeting recordings '
                "aren't saving to OneDrive since Monday? I've recorded 3 meetings this week "
                'and none of them show up in my OneDrive/Recordings folder."}},\n'
                '{"id": "1742285400000", "messageType": "message",\n'
                '"createdDateTime": "2026-03-18T08:10:00Z",\n'
                '"from": {"user": {"displayName": "Kevin Nakamura"}},\n'
                '"body": {"content": "Same here. The recording icon shows during the meeting '
                "but afterwards it says 'Recording expired' in the chat. We're on Teams "
                'Business Premium."}}]}\n\n'
                "This export is from our team chat. Multiple people are affected. "
                "Recordings show 'expired' immediately after the meeting ends."
            ),
            reporter=Reporter(
                name="Olivia Santos",
                email="olivia.santos@contoso.com",
                department="Client Services",
            ),
            created_at="2026-03-18T08:30:00Z",
            channel=TicketChannel.CHAT,
            attachments=[],
        ),
        gold=TriageDecision(
            ticket_id="INC-9220",
            category=TicketCategory.SOFTWARE,
            priority=Priority.P2,
            assigned_team=AssignedTeam.ENTERPRISE_APPS,
            needs_escalation=False,
            missing_information=[MissingInfoField.AFFECTED_USERS],
            next_best_action=(
                "Investigate Teams meeting recordings failing to save to OneDrive. "
                "Multiple users affected since Monday. Recordings show 'expired' immediately."
            ),
            remediation_steps=[
                "Check the Teams admin center for recording storage policy changes",
                "Verify OneDrive storage quotas for affected users",
                "Check if a recent Teams or OneDrive update changed recording behavior",
            ],
        ),
        tag=_TAG,
        test_name="teams_chat_export",
        test_description=(
            "Tests handling of Microsoft Graph API JSON chat export format with @odata.context, "
            "nested user objects, and message bodies. Must identify the recording storage issue."
        ),
    )


def _postman_collection_paste() -> EvalScenario:
    """Postman collection JSON pasted in API issue."""
    return EvalScenario(
        ticket=Ticket(
            ticket_id="INC-9221",
            subject="REST API returning 401 for all authenticated endpoints",
            description=(
                "Exporting my Postman collection for reference:\n\n"
                '{"info": {"name": "Contoso Trading API", "schema": '
                '"https://schema.getpostman.com/json/collection/v2.1.0/collection.json"},\n'
                '"auth": {"type": "bearer", "bearer": [{"key": "token", "value": '
                '"{{access_token}}"}]},\n'
                '"item": [{"name": "Get Portfolio", "request": {"method": "GET",\n'
                '"url": "{{base_url}}/api/v1/portfolios/{{portfolio_id}}",\n'
                '"header": [{"key": "Authorization", "value": "Bearer {{access_token}}"},\n'
                '{"key": "X-Request-ID", "value": "{{$guid}}"}]}},\n'
                '{"name": "Place Order", "request": {"method": "POST",\n'
                '"url": "{{base_url}}/api/v1/orders",\n'
                '"body": {"mode": "raw", "raw": "{\\"symbol\\": \\"MSFT\\", '
                '\\"quantity\\": 100, \\"side\\": \\"BUY\\"}"}}}]}\n\n'
                "Every endpoint returns 401 Unauthorized since we switched from API keys to "
                "OAuth2. The token endpoint works fine but the access tokens are rejected "
                "by the API gateway."
            ),
            reporter=Reporter(
                name="Ryan Fischer",
                email="ryan.fischer@contoso.com",
                department="Trading",
            ),
            created_at="2026-03-18T12:00:00Z",
            channel=TicketChannel.PORTAL,
            attachments=[],
        ),
        gold=TriageDecision(
            ticket_id="INC-9221",
            category=TicketCategory.ACCESS_AUTH,
            priority=Priority.P2,
            assigned_team=AssignedTeam.IDENTITY_ACCESS,
            needs_escalation=False,
            missing_information=[MissingInfoField.CONFIGURATION_DETAILS],
            next_best_action=(
                "Investigate OAuth2 access tokens being rejected by API gateway after migration "
                "from API keys. Token endpoint works but API gateway returns 401."
            ),
            remediation_steps=[
                "Verify the API gateway's OAuth2 audience and issuer configuration matches the token endpoint",
                "Check if the token signing algorithm matches what the gateway expects",
                "Test with a manually decoded JWT to verify claims and expiry",
            ],
        ),
        tag=_TAG,
        test_name="postman_collection_paste",
        test_description=(
            "Tests handling of Postman collection JSON with auth config, request templates, "
            "and variable placeholders. Must identify the OAuth2 token rejection issue."
        ),
    )


def _cron_job_output() -> EvalScenario:
    """Crontab and cron job execution output."""
    return EvalScenario(
        ticket=Ticket(
            ticket_id="INC-9222",
            subject="Nightly backup cron job failing silently",
            description=(
                "Our nightly database backup cron isn't running. Here's the crontab:\n\n"
                "# m h dom mon dow command\n"
                "0 2 * * * /opt/backup/run_backup.sh >> /var/log/backup.log 2>&1\n"
                "30 2 * * * /opt/backup/verify_backup.sh >> /var/log/backup_verify.log 2>&1\n"
                "0 3 * * 0 /opt/backup/weekly_offsite.sh >> /var/log/offsite.log 2>&1\n\n"
                "Last entries in /var/log/backup.log:\n"
                "[2026-03-16 02:00:01] Starting backup of postgres-prod-01...\n"
                "[2026-03-16 02:00:01] ERROR: pg_dump: connection to server at "
                '"10.0.2.50", port 5432 failed: FATAL: password authentication '
                'failed for user "backup_svc"\n'
                "[2026-03-16 02:00:01] Backup FAILED. Exit code: 2\n"
                "[2026-03-17 02:00:01] Starting backup of postgres-prod-01...\n"
                "[2026-03-17 02:00:01] ERROR: pg_dump: same error as above\n\n"
                "The backup service account password was rotated Friday but nobody "
                "updated the cron job's .pgpass file."
            ),
            reporter=Reporter(
                name="Ahmad Hassan",
                email="ahmad.hassan@contoso.com",
                department="Data Engineering",
            ),
            created_at="2026-03-18T07:00:00Z",
            channel=TicketChannel.EMAIL,
            attachments=[],
        ),
        gold=TriageDecision(
            ticket_id="INC-9222",
            category=TicketCategory.DATA_STORAGE,
            priority=Priority.P1,
            assigned_team=AssignedTeam.DATA_PLATFORM,
            needs_escalation=True,
            missing_information=[],
            next_best_action=(
                "Update the .pgpass file for the backup_svc account on the backup server. "
                "Nightly database backups have been failing for 2+ days due to password rotation."
            ),
            remediation_steps=[
                "Update /root/.pgpass (or backup user's .pgpass) with the new backup_svc password",
                "Run the backup script manually to verify it works",
                "Verify the verify_backup.sh script also succeeds",
            ],
        ),
        tag=_TAG,
        test_name="cron_job_output",
        test_description=(
            "Tests handling of crontab entries and cron log output. Must identify the "
            "backup failure due to password rotation and .pgpass not being updated."
        ),
    )


def _jira_import_artifacts() -> EvalScenario:
    """Jira ticket import with markup artifacts."""
    return EvalScenario(
        ticket=Ticket(
            ticket_id="INC-9223",
            subject="[JIRA-MIG] OPS-4521: SSO login loop on trading platform",
            description=(
                "h2. Issue Description\n\n"
                "Users are experiencing an infinite redirect loop when trying to log into "
                "the trading platform via SSO. The login page redirects to Azure AD, which "
                "redirects back to the login page, creating an endless loop.\n\n"
                "h3. Steps to Reproduce\n"
                "# Navigate to https://trading.contoso.internal\n"
                "# Click 'Sign in with SSO'\n"
                "# Observe the redirect loop (URL bar flickers between contoso.internal and "
                "login.microsoftonline.com)\n\n"
                "h3. Environment\n"
                "||Component||Version||\n"
                "|Trading Platform|4.2.1|\n"
                "|Azure AD|N/A|\n"
                "|Browser|Chrome 122, Edge 122|\n\n"
                "{code:java}\n"
                "// Browser console shows:\n"
                "// [ERROR] OIDC: redirect_uri mismatch — expected "
                "'https://trading.contoso.internal/auth/callback'\n"
                "//   but received 'https://trading.contoso.internal/auth/callback/'\n"
                "{code}\n\n"
                "Reported by: [~john.doe] | Priority: {color:red}Blocker{color} | "
                "Sprint: Sprint-42 | Labels: sso, auth, p1\n\n"
                "This was imported from Jira OPS-4521. ~200 traders affected in NYC office."
            ),
            reporter=Reporter(
                name="Migration Bot",
                email="jira-migration@contoso.com",
                department="IT",
            ),
            created_at="2026-03-18T07:30:00Z",
            channel=TicketChannel.PORTAL,
            attachments=[],
        ),
        gold=TriageDecision(
            ticket_id="INC-9223",
            category=TicketCategory.ACCESS_AUTH,
            priority=Priority.P1,
            assigned_team=AssignedTeam.IDENTITY_ACCESS,
            needs_escalation=True,
            missing_information=[],
            next_best_action=(
                "Fix redirect_uri mismatch causing SSO login loop on trading platform. "
                "The trailing slash difference between expected and actual callback URLs is "
                "blocking ~200 traders."
            ),
            remediation_steps=[
                "Update the Azure AD app registration redirect_uri to include the trailing slash variant",
                "Alternatively, update the trading platform's auth config to remove the trailing slash",
                "Clear browser cookies and test SSO login after the fix",
            ],
        ),
        tag=_TAG,
        test_name="jira_import_artifacts",
        test_description=(
            "Tests handling of Jira wiki markup (h2/h3 headers, tables, {code} blocks, "
            "[~user] mentions, {color} macros) from a ticket migration. Must identify "
            "the SSO redirect_uri mismatch issue."
        ),
    )


def _binary_log_corruption() -> EvalScenario:
    """Binary MySQL binlog data leaking into text."""
    binlog_noise = (
        "\x00\x00\x00\x00\xfe\x62\x69\x6e\x00\x00\x00"
        "\\x9a\\x4f\\x66\\x01\\x0f\\x01\\x00\\x00\\x00\\x77\\x00\\x00\\x00"
        "\\x7b\\x00\\x00\\x00\\x00\\x00\\x04\\x00\\x38\\x2e\\x30\\x2e\\x33"
        "\\x36\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00"
        "\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00"
        "\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x00\\x13\\x00\\x0d\\x00\\x08"
        "\\x00\\x00\\x00\\x00\\x08\\x00\\x12\\x00\\x04\\x04\\x04\\x04\\x12"
    )
    description = (
        "MySQL replication between our primary (mysql-prod-01) and replica "
        "(mysql-replica-02) is broken. The replica is stuck and the relay log "
        "seems corrupted. When I tried to inspect the binlog I got garbled output:\n\n"
        f"mysqlbinlog --read-from-remote-server --host=mysql-prod-01 binlog.000847:\n{binlog_noise}\n"
        f"{binlog_noise}\n"
        "# at 4\n"
        "#260318  9:00:00 server id 1  end_log_pos 126  Format_desc\n"
        "# Server ver: 8.0.36, Binlog ver: 4\n"
        "ERROR: Error in Log_event::read_log_event(): 'Event too big', "
        "data_len: 1347420867, event_type: 35\n"
        "ERROR: Could not read entry at offset 4: Error in log event.\n\n"
        "Replication has been down for ~4 hours. The replica serves all read "
        "queries for our reporting dashboards so this is impacting the BI team. "
        "Replica status shows: Slave_SQL_Running: No, Last_Error: Could not "
        "parse relay log event entry.\n\n"
        "Primary: mysql-prod-01.contoso.com (8.0.36)\n"
        "Replica: mysql-replica-02.contoso.com (8.0.36)\n"
        "Affected database: contoso_analytics"
    )

    return EvalScenario(
        ticket=Ticket(
            ticket_id="INC-9224",
            subject="MySQL replication broken — binlog corruption on replica",
            description=description,
            reporter=Reporter(
                name="Raj Patel",
                email="raj.patel@contoso.com",
                department="Data Engineering",
            ),
            created_at="2026-03-18T13:00:00Z",
            channel=TicketChannel.PORTAL,
            attachments=["binlog_error_output.txt"],
        ),
        gold=TriageDecision(
            ticket_id="INC-9224",
            category=TicketCategory.DATA_STORAGE,
            priority=Priority.P2,
            assigned_team=AssignedTeam.DATA_PLATFORM,
            needs_escalation=False,
            missing_information=[],
            next_best_action=(
                "Restore MySQL replication between mysql-prod-01 and mysql-replica-02. "
                "The relay log on the replica is corrupted, causing replication to halt. "
                "BI reporting dashboards depend on the replica for read queries."
            ),
            remediation_steps=[
                "Stop replication on the replica and reset the relay logs with RESET SLAVE",
                "Re-initialize replication from the primary's current binlog position",
                "Verify the binlog on the primary is intact by running mysqlbinlog locally",
                "Monitor replication lag after restoration to ensure it catches up",
                "Investigate root cause of relay log corruption (disk issues, network errors)",
            ],
        ),
        tag=_TAG,
        test_name="binary_log_corruption",
        test_description=(
            "Tests handling of binary MySQL binlog data mixed into ticket text. The "
            "description contains hex escape sequences and binary fragments from a "
            "corrupted relay log. The model must identify the MySQL replication failure."
        ),
    )


def _markdown_rendering_noise() -> EvalScenario:
    """Rendered markdown with HTML artifacts mixed in."""
    description = (
        "Our internal wiki at wiki.contoso.com is rendering pages incorrectly. "
        "Here's what the page source looks like when I view it:\n\n"
        '<div class="markdown-body">\n'
        "<h1>Onboarding Guide</h1>\n"
        '<p>Welcome to <strong class="highlight">Contoso Financial</strong>.</p>\n'
        "<!-- confluence-macro: {toc} -->\n"
        '<span data-macro-name="toc" data-macro-id="abc123"></span>\n'
        "<h2>Step 1: Access Setup</h2>\n"
        '<p>Request access via <a href="javascript:void(0)" '
        'data-linktype="internal">ServiceNow portal</a></p>\n'
        "<ul>\n"
        "  <li>&#x2610; VPN configuration</li>\n"
        "  <li>&#x2610; Email setup</li>\n"
        "  <li>&#x2611; Badge access (auto-provisioned)</li>\n"
        "</ul>\n"
        '<div class="aui-message warning">\n'
        "  <p>Note: HTML entities &amp;amp; &amp;lt; &amp;gt; are not rendering</p>\n"
        "</div>\n"
        "<!-- JIRA: WIKI-4521 -->\n"
        '<img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUg..." '
        'alt="broken-image" onerror="this.style.display=\'none\'">\n'
        '<p style="color: undefined; font-size: NaNpx;">Footer text</p>\n\n'
        "All pages in the Engineering space are showing raw HTML instead of "
        "rendered content. Started after the wiki platform update last night. "
        "About 200 engineers use this wiki daily for runbooks and documentation."
    )

    return EvalScenario(
        ticket=Ticket(
            ticket_id="INC-9225",
            subject="Wiki pages showing raw HTML — rendering broken after update",
            description=description,
            reporter=Reporter(
                name="Tom Bradley",
                email="tom.bradley@contoso.com",
                department="Engineering",
            ),
            created_at="2026-03-18T10:45:00Z",
            channel=TicketChannel.PORTAL,
            attachments=["wiki_screenshot.png"],
        ),
        gold=TriageDecision(
            ticket_id="INC-9225",
            category=TicketCategory.SOFTWARE,
            priority=Priority.P2,
            assigned_team=AssignedTeam.ENTERPRISE_APPS,
            needs_escalation=False,
            missing_information=[],
            next_best_action=(
                "Investigate wiki rendering failure affecting the Engineering space after "
                "last night's platform update. Pages are showing raw HTML instead of "
                "rendered markdown/content. Approximately 200 engineers are impacted."
            ),
            remediation_steps=[
                "Check the wiki platform's recent update logs for rendering engine changes",
                "Rollback the wiki platform update if a quick fix is not available",
                "Verify the markdown rendering pipeline and HTML sanitization settings",
                "Test rendering on a single page after applying the fix before full rollout",
            ],
        ),
        tag=_TAG,
        test_name="markdown_rendering_noise",
        test_description=(
            "Tests handling of mixed HTML and markdown artifacts including Confluence macros, "
            "HTML entities, inline base64 images, and broken CSS values. The model must "
            "identify the wiki rendering failure as the core issue."
        ),
    )


def _pgp_signed_email() -> EvalScenario:
    """PGP-signed email wrapping a docking station issue."""
    description = (
        "-----BEGIN PGP SIGNED MESSAGE-----\n"
        "Hash: SHA256\n\n"
        "Hi IT Support,\n\n"
        "My docking station stopped working after the firmware "
        "update pushed last Thursday. The model is a Dell WD19S "
        "connected via USB-C. When I plug in, the external "
        "monitors flicker for about two seconds then go black. "
        "The laptop charges through the dock but no video output "
        "and the USB peripherals attached to the dock are not "
        "recognised either.\n\n"
        "I have tried:\n"
        "- Rebooting the laptop\n"
        "- Using a different USB-C cable\n"
        "- Connecting directly to HDMI (works fine)\n\n"
        "Regards,\nSandra\n\n"
        "-----BEGIN PGP SIGNATURE-----\n"
        "iQIzBAEBCAAdFiEEuL4cyR0xN2P+dGhJqFsM0aL1r8E"
        "FAmXmK5AACgkQqFsM0aL1r8HtPA//bH8kZiB+qOFIz8"
        "gA4XG5Fj2rQmNOlVPGqkR/2wYOCh7RKxLP+1KWM5X4V"
        "kW3C+nISAGx3fAqFH0dA6kQEaJY8mWpD9v+FGJkn3MZz"
        "7RqFO5BoJfAHciPkX0F7b/0jLbD9G8WqI8jP=\n"
        "=kX2q\n"
        "-----END PGP SIGNATURE-----"
    )
    return EvalScenario(
        ticket=Ticket(
            ticket_id="INC-9226",
            subject="Docking station not working after update",
            description=description,
            reporter=Reporter(
                name="Sandra Okafor",
                email="sandra.okafor@contoso.com",
                department="Finance",
            ),
            created_at="2026-04-07T09:00:00Z",
            channel=TicketChannel.EMAIL,
        ),
        gold=TriageDecision(
            ticket_id="INC-9226",
            category=TicketCategory.HARDWARE,
            priority=Priority.P3,
            assigned_team=AssignedTeam.ENDPOINT_ENG,
            needs_escalation=False,
            missing_information=[
                MissingInfoField.DEVICE_INFO,
            ],
            next_best_action=(
                "Investigate Dell WD19S docking station failure "
                "after firmware update. External monitors and USB "
                "peripherals unresponsive via dock. Direct HDMI "
                "works, suggesting a dock-specific issue."
            ),
            remediation_steps=[
                "Roll back dock firmware to previous version",
                "Test with a known-good Dell WD19S from inventory",
                "Update laptop USB-C and Thunderbolt drivers",
            ],
        ),
        tag=_TAG,
        test_name="pgp_signed_email",
        test_description=(
            "Tests handling of PGP-signed email wrapping a real IT issue about a docking station failure."
        ),
    )


def _long_cc_bcc_headers() -> EvalScenario:
    """Extremely long CC/BCC headers burying an Outlook crash."""
    cc_list = ", ".join(f"user{i}@contoso.com" for i in range(1, 61))
    description = (
        f"CC: {cc_list}\n"
        f"BCC: {cc_list}\n\n"
        "--- Forwarded 14 times ---\n\n"
        "Original issue: Outlook desktop client crashes every "
        "time I try to open a calendar invite from the Legal "
        "team. The error dialog says 'MAPI_E_CALL_FAILED'. "
        "Version is Microsoft 365 Apps, build 16.0.17328. "
        "Happens on both my laptop and desktop. Started after "
        "yesterday's update. Other users on the Legal team "
        "confirm the same behaviour."
    )
    return EvalScenario(
        ticket=Ticket(
            ticket_id="INC-9227",
            subject="FW: FW: FW: RE: Calendar issue",
            description=description,
            reporter=Reporter(
                name="Derek Nguyen",
                email="derek.nguyen@contoso.com",
                department="Legal",
            ),
            created_at="2026-04-07T10:15:00Z",
            channel=TicketChannel.EMAIL,
        ),
        gold=TriageDecision(
            ticket_id="INC-9227",
            category=TicketCategory.SOFTWARE,
            priority=Priority.P2,
            assigned_team=AssignedTeam.ENTERPRISE_APPS,
            needs_escalation=False,
            missing_information=[
                MissingInfoField.ERROR_MESSAGE,
            ],
            next_best_action=(
                "Investigate Outlook crash with MAPI_E_CALL_FAILED "
                "when opening Legal team calendar invites. Multiple "
                "users affected since recent update on build "
                "16.0.17328."
            ),
            remediation_steps=[
                "Collect Outlook crash logs from affected machines",
                "Test rolling back the recent Office update",
                "Repair the Office installation via control panel",
                "Recreate the Outlook mail profile if needed",
            ],
        ),
        tag=_TAG,
        test_name="long_cc_bcc_headers",
        test_description=(
            "Tests handling of extremely long CC/BCC header "
            "lists and forwarding chains that obscure the "
            "actual Outlook crash issue underneath."
        ),
    )


def _xml_soap_fault() -> EvalScenario:
    """XML SOAP Fault from SAP data sync failure."""
    description = (
        "Getting this error from our SAP integration:\n\n"
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        "<soap:Envelope "
        'xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">\n'
        "  <soap:Body>\n"
        "    <soap:Fault>\n"
        "      <faultcode>"
        "soap:Server.GeneralException</faultcode>\n"
        "      <faultstring>"
        "System exception in program CL_BAPI_MATERIAL "
        "method CHANGE_MATERIAL: Row 4821 — field "
        "MAKTX contains invalid character \\x0B "
        "(vertical tab)</faultstring>\n"
        "      <detail>\n"
        "        <ns1:SystemFault "
        'xmlns:ns1="urn:sap-com:document:sap:rfc">\n'
        "          <Host>sapapp01.contoso.local</Host>\n"
        "          <Component>BC-MID-RFC</Component>\n"
        "          <MsgType>E</MsgType>\n"
        "          <MsgClass>SY</MsgClass>\n"
        "          <MsgNumber>002</MsgNumber>\n"
        "        </ns1:SystemFault>\n"
        "      </detail>\n"
        "    </soap:Fault>\n"
        "  </soap:Body>\n"
        "</soap:Envelope>\n\n"
        "The nightly data sync between SAP and our data "
        "warehouse has been failing for the last three nights. "
        "Finance closes the quarter next week and needs this "
        "data reconciled."
    )
    return EvalScenario(
        ticket=Ticket(
            ticket_id="INC-9228",
            subject="SAP data sync SOAP fault — quarter close",
            description=description,
            reporter=Reporter(
                name="Patricia Lehmann",
                email="patricia.lehmann@contoso.com",
                department="Finance",
            ),
            created_at="2026-04-07T07:30:00Z",
            channel=TicketChannel.PORTAL,
        ),
        gold=TriageDecision(
            ticket_id="INC-9228",
            category=TicketCategory.DATA_STORAGE,
            priority=Priority.P2,
            assigned_team=AssignedTeam.DATA_PLATFORM,
            needs_escalation=False,
            missing_information=[
                MissingInfoField.TIMESTAMP,
            ],
            next_best_action=(
                "Fix the invalid vertical-tab character in SAP "
                "material master row 4821 field MAKTX, then "
                "re-run the nightly data sync before quarter close."
            ),
            remediation_steps=[
                "Sanitise the invalid character in MAKTX row 4821",
                "Re-trigger the nightly SAP-to-warehouse sync job",
                "Add input validation to prevent control characters",
                "Verify data reconciliation with Finance team",
            ],
        ),
        tag=_TAG,
        test_name="xml_soap_fault",
        test_description=(
            "Tests extraction of the real data sync issue from a verbose XML SOAP Fault envelope returned by SAP."
        ),
    )


def _kubernetes_pod_describe() -> EvalScenario:
    """Kubernetes pod describe output with CrashLoopBackOff."""
    description = (
        "Our payments microservice keeps crashing. Here is the "
        "pod describe output:\n\n"
        "Name:         payments-api-6b8f9c4d77-xk2lp\n"
        "Namespace:    prod-payments\n"
        "Priority:     0\n"
        "Node:         aks-nodepool1-38471925-vmss000004\n"
        "Start Time:   Mon, 07 Apr 2026 03:12:44 +0000\n"
        "Labels:       app=payments-api\n"
        "              pod-template-hash=6b8f9c4d77\n"
        "Status:       Running\n"
        "IP:           10.244.3.42\n"
        "Containers:\n"
        "  payments-api:\n"
        "    Image:        acr.contoso.com/payments:v2.14.1\n"
        "    Port:         8080/TCP\n"
        "    State:        Waiting\n"
        "      Reason:     CrashLoopBackOff\n"
        "    Last State:   Terminated\n"
        "      Reason:     OOMKilled\n"
        "      Exit Code:  137\n"
        "    Ready:        False\n"
        "    Restart Count: 47\n"
        "    Limits:\n"
        "      cpu:     500m\n"
        "      memory:  256Mi\n"
        "    Requests:\n"
        "      cpu:     250m\n"
        "      memory:  128Mi\n"
        "Events:\n"
        "  Type     Reason     Message\n"
        "  ----     ------     -------\n"
        "  Warning  BackOff    Back-off restarting container\n"
        "  Warning  OOMKilled  Memory limit 256Mi exceeded\n\n"
        "This is blocking customer payments in production."
    )
    return EvalScenario(
        ticket=Ticket(
            ticket_id="INC-9229",
            subject="Payments pod CrashLoopBackOff in prod",
            description=description,
            reporter=Reporter(
                name="Ivan Petrov",
                email="ivan.petrov@contoso.com",
                department="Engineering",
            ),
            created_at="2026-04-07T03:45:00Z",
            channel=TicketChannel.PORTAL,
            attachments=["pod_describe.txt"],
        ),
        gold=TriageDecision(
            ticket_id="INC-9229",
            category=TicketCategory.SOFTWARE,
            priority=Priority.P1,
            assigned_team=AssignedTeam.ENTERPRISE_APPS,
            needs_escalation=True,
            missing_information=[
                MissingInfoField.APPLICATION_VERSION,
            ],
            next_best_action=(
                "Payments pod is OOMKilled with 256Mi limit and "
                "has restarted 47 times. Increase memory limit "
                "immediately to restore customer payments."
            ),
            remediation_steps=[
                "Increase pod memory limit from 256Mi to 512Mi",
                "Investigate memory leak in payments-api v2.14.1",
                "Review recent code changes for memory regressions",
                "Set up memory usage alerting for this namespace",
            ],
        ),
        tag=_TAG,
        test_name="kubernetes_pod_describe",
        test_description=(
            "Tests extraction of the OOMKilled root cause from "
            "verbose Kubernetes pod describe output in a "
            "production CrashLoopBackOff scenario."
        ),
    )


def _raw_hex_dump() -> EvalScenario:
    """Raw hex dump from TLS handshake failure."""
    description = (
        "Our load balancer is dropping connections. Captured "
        "this with tcpdump:\n\n"
        "0000  16 03 01 02 00 01 00 01  fc 03 03 5a 8b 7e 2c 4d\n"
        "0010  9a 3b 1f 6e 04 a3 d8 f1  22 c7 5b 91 0e 38 47 c6\n"
        "0020  b2 d4 15 ee 9f 00 00 1c  c0 2b c0 2f c0 2c c0 30\n"
        "0030  cc a9 cc a8 c0 09 c0 13  c0 0a c0 14 00 9c 00 9d\n"
        "0040  00 2f 00 35 00 0a 01 00  01 97 00 00 00 12 00 10\n"
        "0050  00 00 0d 61 70 69 2e 63  6f 6e 74 6f 73 6f 2e 63\n"
        "0060  6f 6d ff 01 00 01 00 00  0a 00 08 00 06 00 1d 00\n"
        "0070  17 00 18 00 0b 00 02 01  00 00 23 00 00 00 10 00\n\n"
        "The TLS handshake fails at ServerHello. Clients get "
        "ERR_SSL_VERSION_OR_CIPHER_MISMATCH. Affects the "
        "api.contoso.com endpoint. Started after the security "
        "team rotated certificates last night. About 40% of "
        "external API traffic is failing."
    )
    return EvalScenario(
        ticket=Ticket(
            ticket_id="INC-9230",
            subject="TLS failures on api.contoso.com",
            description=description,
            reporter=Reporter(
                name="Mei-Lin Chang",
                email="mei-lin.chang@contoso.com",
                department="Engineering",
            ),
            created_at="2026-04-07T04:20:00Z",
            channel=TicketChannel.CHAT,
        ),
        gold=TriageDecision(
            ticket_id="INC-9230",
            category=TicketCategory.NETWORK,
            priority=Priority.P1,
            assigned_team=AssignedTeam.NETWORK_OPS,
            needs_escalation=True,
            missing_information=[
                MissingInfoField.CONFIGURATION_DETAILS,
            ],
            next_best_action=(
                "TLS handshake failures on api.contoso.com after "
                "certificate rotation. 40 percent of external API "
                "traffic is failing. Verify the new certificate "
                "chain and cipher suite configuration immediately."
            ),
            remediation_steps=[
                "Verify the new certificate chain is complete",
                "Check cipher suite config on the load balancer",
                "Roll back to the previous certificate if needed",
                "Confirm TLS version compatibility with clients",
            ],
        ),
        tag=_TAG,
        test_name="raw_hex_dump",
        test_description=(
            "Tests extraction of a TLS handshake failure from "
            "a raw hex dump captured via tcpdump. The model "
            "must identify the cipher mismatch root cause."
        ),
    )


def _mixed_encoding_wifi() -> EvalScenario:
    """Mixed encoding artefacts around a Wi-Fi drop issue."""
    description = (
        "Iâ\u0080\u0099m having trouble with the Wi-Fi on floor 3. "
        "It keeps disconnecting every 10â\u0080\u009315 minutes. "
        "The SSID is â\u0080\u009cContoso-Corpâ\u0080\u009d and "
        "Iâ\u0080\u0099ve tried forgetting the network and "
        "reconnecting.\n\n"
        "Error message says: â\u0080\u009cNetwork connection was "
        "lost. Please check your Wi-Fi settings.â\u0080\u009d\n\n"
        "Iâ\u0080\u0099m using a ThinkPad T14 Gen 3 with "
        "Windows 11. The issue started Monday. Other people "
        "on floor 3 are also affected â\u0080\u0094 at least "
        "five of us.\n\n"
        "My MAC address is 5C:EA:1D:67:3B:A2 if that helps. "
        "Please fix ASAP â\u0080\u0094 we have client demos "
        "this week."
    )
    return EvalScenario(
        ticket=Ticket(
            ticket_id="INC-9231",
            subject="WiFi keeps dropping on floor 3",
            description=description,
            reporter=Reporter(
                name="Rachel Kim",
                email="rachel.kim@contoso.com",
                department="Sales",
            ),
            created_at="2026-04-07T11:00:00Z",
            channel=TicketChannel.PORTAL,
        ),
        gold=TriageDecision(
            ticket_id="INC-9231",
            category=TicketCategory.NETWORK,
            priority=Priority.P2,
            assigned_team=AssignedTeam.NETWORK_OPS,
            needs_escalation=False,
            missing_information=[
                MissingInfoField.NETWORK_LOCATION,
            ],
            next_best_action=(
                "Investigate recurring Wi-Fi disconnections on "
                "floor 3 affecting multiple users. Check access "
                "point health and channel interference for the "
                "Contoso-Corp SSID."
            ),
            remediation_steps=[
                "Check floor-3 access point logs for client drops",
                "Run a wireless site survey for interference",
                "Restart or replace the affected access point",
                "Confirm connectivity with reporter after fix",
            ],
        ),
        tag=_TAG,
        test_name="mixed_encoding_wifi",
        test_description=(
            "Tests handling of UTF-8 mojibake and mixed encoding "
            "artefacts (curly quotes rendered as multi-byte "
            "garbage) wrapping a Wi-Fi connectivity issue."
        ),
    )


def _sql_query_data_corruption() -> EvalScenario:
    """SQL query results pasted into a data corruption ticket."""
    description = (
        "We found data corruption in the customer table. "
        "Here are the affected rows:\n\n"
        "SELECT customer_id, name, email, balance,\n"
        "       last_modified\n"
        "  FROM dbo.Customers\n"
        " WHERE balance < 0\n"
        "   AND last_modified > '2026-04-01';\n\n"
        "+-------------+------------------+-------+\n"
        "| customer_id | name             |balance|\n"
        "+-------------+------------------+-------+\n"
        "| C-10042     | Acme Corp        | -4.2E7|\n"
        "| C-10099     | NULL             |  -999 |\n"
        "| C-10153     | Beta Ltd         |-1E+12 |\n"
        "| C-10200     | \\x00\\x00\\x00 |     0 |\n"
        "| C-10317     | Gamma Inc        | -0.01 |\n"
        "+-------------+------------------+-------+\n"
        "5 rows affected\n\n"
        "Execution plan: Clustered Index Scan on PK_Customers "
        "(cost 42.7, rows 5 of 2.4M)\n\n"
        "Balance values went negative after the overnight ETL "
        "job on April 1st. Finance noticed when monthly "
        "statements showed impossible figures. One row has a "
        "balance of negative 10 billion which is clearly wrong. "
        "We need the ETL job audited and the data restored from "
        "the last clean backup."
    )
    return EvalScenario(
        ticket=Ticket(
            ticket_id="INC-9232",
            subject="Negative balances in customer table after ETL",
            description=description,
            reporter=Reporter(
                name="Carlos Rivera",
                email="carlos.rivera@contoso.com",
                department="Data Engineering",
            ),
            created_at="2026-04-07T08:00:00Z",
            channel=TicketChannel.PORTAL,
        ),
        gold=TriageDecision(
            ticket_id="INC-9232",
            category=TicketCategory.DATA_STORAGE,
            priority=Priority.P1,
            assigned_team=AssignedTeam.DATA_PLATFORM,
            needs_escalation=True,
            missing_information=[
                MissingInfoField.TIMESTAMP,
                MissingInfoField.ENVIRONMENT_DETAILS,
            ],
            next_best_action=(
                "Audit the overnight ETL job that corrupted "
                "customer balance data on April 1st. Restore "
                "affected rows from the last clean backup and "
                "halt the ETL until the root cause is fixed."
            ),
            remediation_steps=[
                "Pause the nightly ETL job to prevent further damage",
                "Restore corrupted rows from the last clean backup",
                "Audit the ETL transformation logic for the bug",
                "Add validation checks to reject negative balances",
                "Reconcile restored data with Finance team",
            ],
        ),
        tag=_TAG,
        test_name="sql_query_data_corruption",
        test_description=(
            "Tests extraction of a data corruption issue from "
            "pasted SQL query results, execution plans, and "
            "tabular output mixed into the ticket body."
        ),
    )


def _multilingual_legal_disclaimer() -> EvalScenario:
    """Multilingual legal disclaimers wrapping a password reset."""
    description = (
        "Hi, I need my password reset for the finance portal. "
        "My username is p.fischer and I have been locked out "
        "since this morning.\n\n"
        "---\n"
        "VERTRAULICHKEITSHINWEIS: Diese E-Mail und alle "
        "Anhaenge sind vertraulich und ausschliesslich fuer "
        "den bezeichneten Adressaten bestimmt. Sollten Sie "
        "diese E-Mail irrtuemlich erhalten haben, informieren "
        "Sie bitte sofort den Absender und loeschen Sie die "
        "Nachricht.\n"
        "---\n"
        "AVIS DE CONFIDENTIALITE: Ce message electronique et "
        "toutes les pieces jointes sont confidentiels et "
        "destines exclusivement a lusage du destinataire "
        "indique. Si vous avez recu ce message par erreur, "
        "veuillez en informer lexpéditeur immediatement et "
        "supprimer le message.\n"
        "---\n"
        "AVISO DE CONFIDENCIALIDAD: Este mensaje y cualquier "
        "archivo adjunto son confidenciales y estan destinados "
        "exclusivamente al uso del destinatario indicado. Si "
        "usted ha recibido este mensaje por error, notifique "
        "al remitente inmediatamente y elimine el mensaje.\n"
        "---\n"
        "This message may contain legally privileged or "
        "confidential information of Contoso Financial Services "
        "and its global subsidiaries. Unauthorized use is "
        "strictly prohibited."
    )
    return EvalScenario(
        ticket=Ticket(
            ticket_id="INC-9233",
            subject="Password reset needed",
            description=description,
            reporter=Reporter(
                name="Petra Fischer",
                email="p.fischer@contoso.com",
                department="Finance",
            ),
            created_at="2026-04-07T08:45:00Z",
            channel=TicketChannel.EMAIL,
        ),
        gold=TriageDecision(
            ticket_id="INC-9233",
            category=TicketCategory.ACCESS_AUTH,
            priority=Priority.P3,
            assigned_team=AssignedTeam.IDENTITY_ACCESS,
            needs_escalation=False,
            missing_information=[
                MissingInfoField.AUTHENTICATION_METHOD,
            ],
            next_best_action=(
                "Reset password for user p.fischer on the "
                "finance portal. Verify identity before reset "
                "and confirm the account is not compromised."
            ),
            remediation_steps=[
                "Verify reporter identity via standard process",
                "Reset the finance portal password for p.fischer",
                "Check for signs of account compromise or brute force",
                "Confirm successful login with the reporter",
            ],
        ),
        tag=_TAG,
        test_name="multilingual_legal_disclaimer",
        test_description=(
            "Tests handling of multilingual legal disclaimers "
            "in German, French, and Spanish that pad a simple "
            "password-reset request."
        ),
    )


def _near_empty_ticket() -> EvalScenario:
    """Near-empty ticket with almost no useful information."""
    description = "monitor not working"
    return EvalScenario(
        ticket=Ticket(
            ticket_id="INC-9234",
            subject="issue",
            description=description,
            reporter=Reporter(
                name="Jordan Blake",
                email="jordan.blake@contoso.com",
                department="Marketing",
            ),
            created_at="2026-04-07T14:00:00Z",
            channel=TicketChannel.CHAT,
        ),
        gold=TriageDecision(
            ticket_id="INC-9234",
            category=TicketCategory.HARDWARE,
            priority=Priority.P4,
            assigned_team=AssignedTeam.ENDPOINT_ENG,
            needs_escalation=False,
            missing_information=[
                MissingInfoField.DEVICE_INFO,
                MissingInfoField.ERROR_MESSAGE,
                MissingInfoField.STEPS_TO_REPRODUCE,
                MissingInfoField.AFFECTED_SYSTEM,
            ],
            next_best_action=(
                "Gather basic details from the reporter: which "
                "monitor, what symptoms, and whether it is a "
                "display, cable, or connection issue."
            ),
            remediation_steps=[
                "Contact reporter for monitor model and symptoms",
                "Ask whether the issue is no power or no signal",
                "Schedule a desk visit if remote triage fails",
            ],
        ),
        tag=_TAG,
        test_name="near_empty_ticket",
        test_description=(
            "Tests triage of an extremely terse ticket with "
            "almost no detail — only three words in the "
            "description and a one-word subject."
        ),
    )


def _vulnerability_scanner_dump() -> EvalScenario:
    """Vulnerability scanner output hiding a TLS cert expiry."""
    description = (
        "Nessus scan results for prod-web-cluster:\n\n"
        "Plugin 10863 - SSL Certificate Expiry\n"
        "  Risk: High\n"
        "  Host: 10.0.4.21 (web01.contoso.com)\n"
        "  Port: 443/tcp\n"
        "  Output: The SSL certificate will expire on "
        "2026-04-09T23:59:59Z (in 2 days).\n"
        "  CN=*.contoso.com  O=Contoso Ltd  "
        "Issuer=DigiCert SHA2 Extended Validation\n\n"
        "Plugin 42873 - SSL Medium Strength Ciphers\n"
        "  Risk: Medium\n"
        "  Host: 10.0.4.21\n"
        "  Port: 443/tcp\n"
        "  Cipher: TLS_RSA_WITH_AES_128_CBC_SHA\n\n"
        "Plugin 11219 - Nessus SYN Scanner\n"
        "  Risk: None\n"
        "  Host: 10.0.4.21\n"
        "  Open ports: 22, 80, 443, 8080\n\n"
        "Plugin 19506 - Nessus Scan Information\n"
        "  Scan Start: 2026-04-07T02:00:00Z\n"
        "  Scan End:   2026-04-07T02:47:33Z\n"
        "  Policy:     Contoso PCI Quarterly\n"
        "  Scanner:    nessus-scanner-01.contoso.local\n\n"
        "Plugin 33929 - PCI DSS Compliance Checks\n"
        "  Risk: None\n"
        "  Overall: 14 passed, 1 failed (SSL expiry)\n\n"
        "Total: 247 plugins run, 2 high, 3 medium, "
        "242 informational.\n\n"
        "The wildcard cert for *.contoso.com expires in two "
        "days. If it lapses our entire public web presence "
        "goes down. Please renew ASAP."
    )
    return EvalScenario(
        ticket=Ticket(
            ticket_id="INC-9235",
            subject="Nessus scan — critical cert expiry in 2 days",
            description=description,
            reporter=Reporter(
                name="Amara Osei",
                email="amara.osei@contoso.com",
                department="Security",
            ),
            created_at="2026-04-07T06:00:00Z",
            channel=TicketChannel.PORTAL,
            attachments=["nessus_report.csv"],
        ),
        gold=TriageDecision(
            ticket_id="INC-9235",
            category=TicketCategory.SECURITY,
            priority=Priority.P1,
            assigned_team=AssignedTeam.SECURITY_OPS,
            needs_escalation=True,
            missing_information=[],
            next_best_action=(
                "Renew the wildcard TLS certificate for "
                "*.contoso.com before it expires on April 9. "
                "Failure to renew will cause outages across "
                "the entire public web presence."
            ),
            remediation_steps=[
                "Initiate emergency certificate renewal with DigiCert",
                "Deploy the renewed cert to all prod web servers",
                "Verify renewed cert across all affected endpoints",
                "Set up automated certificate expiry alerting",
            ],
        ),
        tag=_TAG,
        test_name="vulnerability_scanner_dump",
        test_description=(
            "Tests extraction of an urgent TLS certificate "
            "expiry from verbose Nessus vulnerability scanner "
            "output containing hundreds of plugin results."
        ),
    )


def _prometheus_metrics_flood() -> EvalScenario:
    """Prometheus metrics pasted into a database performance ticket."""
    description = (
        "Hi team,\n\n"
        "Our production Postgres cluster has been extremely slow since "
        "yesterday morning. I grabbed some Prometheus metrics that might "
        "help. Here they are:\n\n"
        "# HELP pg_stat_activity_count Number of connections\n"
        "# TYPE pg_stat_activity_count gauge\n"
        'pg_stat_activity_count{datname="orders_db",state="active"} 487\n'
        'pg_stat_activity_count{datname="orders_db",state="idle"} 312\n'
        'pg_stat_activity_count{datname="orders_db",state="idle_in_transaction"} 74\n'
        'pg_stat_activity_count{datname="inventory_db",state="active"} 23\n'
        'pg_stat_activity_count{datname="inventory_db",state="idle"} 156\n\n'
        "# HELP pg_locks_count Number of locks\n"
        "# TYPE pg_locks_count gauge\n"
        'pg_locks_count{datname="orders_db",mode="AccessShareLock"} 1024\n'
        'pg_locks_count{datname="orders_db",mode="RowExclusiveLock"} 893\n'
        'pg_locks_count{datname="orders_db",mode="ExclusiveLock"} 12\n\n'
        "# HELP pg_replication_lag_seconds Replication lag in seconds\n"
        "# TYPE pg_replication_lag_seconds gauge\n"
        'pg_replication_lag_seconds{replica="pg-replica-01"} 47.3\n'
        'pg_replication_lag_seconds{replica="pg-replica-02"} 112.8\n'
        'pg_replication_lag_seconds{replica="pg-replica-03"} 0.4\n\n'
        "# HELP pg_stat_bgwriter_buffers_checkpoint Total buffers written during checkpoints\n"
        "# TYPE pg_stat_bgwriter_buffers_checkpoint counter\n"
        "pg_stat_bgwriter_buffers_checkpoint 9.284731e+06\n\n"
        "# HELP pg_database_size_bytes Database size in bytes\n"
        "# TYPE pg_database_size_bytes gauge\n"
        'pg_database_size_bytes{datname="orders_db"} 5.28934e+11\n'
        'pg_database_size_bytes{datname="inventory_db"} 1.73421e+10\n\n'
        "# HELP node_cpu_seconds_total CPU time in seconds\n"
        "# TYPE node_cpu_seconds_total counter\n"
        'node_cpu_seconds_total{cpu="0",mode="user"} 4.82931e+05\n'
        'node_cpu_seconds_total{cpu="0",mode="system"} 1.23847e+05\n'
        'node_cpu_seconds_total{cpu="0",mode="iowait"} 8.7421e+04\n'
        'node_cpu_seconds_total{cpu="1",mode="user"} 4.91283e+05\n'
        'node_cpu_seconds_total{cpu="1",mode="iowait"} 9.1032e+04\n\n'
        "The orders_db is the one causing problems. Queries that normally "
        "take 200ms are now timing out after 30 seconds. The application "
        "team is complaining about checkout failures.\n\n"
        "Thanks,\nJorge"
    )
    return EvalScenario(
        ticket=Ticket(
            ticket_id="INC-9236",
            subject="Postgres cluster severe performance degradation",
            description=description,
            reporter=Reporter(
                name="Jorge Delgado",
                email="jorge.delgado@contoso.com",
                department="Database Engineering",
            ),
            created_at="2026-03-18T09:15:00Z",
            channel=TicketChannel.EMAIL,
            attachments=["prometheus_snapshot.tar.gz"],
        ),
        gold=TriageDecision(
            ticket_id="INC-9236",
            category=TicketCategory.DATA_STORAGE,
            priority=Priority.P2,
            assigned_team=AssignedTeam.DATA_PLATFORM,
            needs_escalation=False,
            missing_information=[
                MissingInfoField.TIMESTAMP,
                MissingInfoField.ENVIRONMENT_DETAILS,
            ],
            next_best_action=(
                "Investigate the high lock contention and replication "
                "lag on the orders_db Postgres cluster causing query "
                "timeouts and checkout failures."
            ),
            remediation_steps=[
                "Identify and terminate long-running or blocked queries holding exclusive locks",
                "Investigate root cause of replication lag on pg-replica-02",
                "Review recent schema or query changes to orders_db",
                "Consider increasing max_connections or implementing connection pooling",
            ],
        ),
        tag=_TAG,
        test_name="prometheus_metrics_flood",
        test_description=(
            "Tests extraction of a database performance issue from "
            "a ticket flooded with raw Prometheus metrics exposition "
            "format data including gauges, counters, and labels."
        ),
    )


def _systeminfo_command_dump() -> EvalScenario:
    """Windows systeminfo output dumped in laptop overheating ticket."""
    description = (
        "My laptop keeps overheating and shutting down randomly. Here is "
        "my system info:\n\n"
        "Host Name:                 DESKTOP-A4F8K2L\n"
        "OS Name:                   Microsoft Windows 11 Enterprise\n"
        "OS Version:                10.0.22631 N/A Build 22631\n"
        "OS Manufacturer:           Microsoft Corporation\n"
        "OS Configuration:          Member Workstation\n"
        "OS Build Type:             Multiprocessor Free\n"
        "Registered Owner:          Priya Nair\n"
        "Registered Organization:   Contoso Ltd\n"
        "Product ID:                00329-00000-00003-AA842\n"
        "Original Install Date:     8/14/2025, 3:22:17 PM\n"
        "System Boot Time:          3/17/2026, 8:01:53 AM\n"
        "System Manufacturer:       Dell Inc.\n"
        "System Model:              Latitude 5540\n"
        "System Type:               x64-based PC\n"
        "Processor(s):              1 Processor(s) Installed.\n"
        "                           [01]: Intel64 Family 6 Model 186 "
        "Stepping 3 GenuineIntel ~2419 Mhz\n"
        "BIOS Version:              Dell Inc. 1.18.0, 6/12/2025\n"
        "Windows Directory:         C:\\Windows\n"
        "System Directory:          C:\\Windows\\system32\n"
        "Boot Device:               \\Device\\HarddiskVolume1\n"
        "System Locale:             en-us;English (United States)\n"
        "Input Locale:              en-us;English (United States)\n"
        "Time Zone:                 (UTC-05:00) Eastern Time (US & Canada)\n"
        "Total Physical Memory:     16,157 MB\n"
        "Available Physical Memory: 2,314 MB\n"
        "Virtual Memory: Max Size:  18,589 MB\n"
        "Virtual Memory: Available: 3,742 MB\n"
        "Virtual Memory: In Use:    14,847 MB\n"
        "Page File Location(s):     C:\\pagefile.sys\n"
        "Domain:                    contoso.local\n"
        "Logon Server:              \\\\DC-EAST-01\n"
        "Hotfix(s):                 14 Hotfix(s) Installed.\n"
        "                           [01]: KB5034765\n"
        "                           [02]: KB5035853\n"
        "                           [03]: KB5036212\n"
        "                           [04]: KB5037019\n"
        "                           [05]: KB5037591\n"
        "                           [06]: KB5038002\n"
        "                           [07]: KB5038517\n"
        "                           [08]: KB5039103\n"
        "                           [09]: KB5039628\n"
        "                           [10]: KB5040174\n"
        "                           [11]: KB5040689\n"
        "                           [12]: KB5041231\n"
        "                           [13]: KB5041784\n"
        "                           [14]: KB5042306\n"
        "Network Card(s):           2 NIC(s) Installed.\n"
        "                           [01]: Intel(R) Ethernet I219-LM\n"
        "                           [02]: Intel(R) Wi-Fi 6E AX211 160MHz\n"
        "Hyper-V Requirements:      VM Monitor Mode Extensions: Yes\n\n"
        "It gets very hot near the fan area and sometimes just shuts off "
        "without warning during video calls. This has been happening for "
        "about two weeks now. I already tried cleaning the vents with "
        "compressed air but it did not help.\n\n"
        "Regards,\nPriya"
    )
    return EvalScenario(
        ticket=Ticket(
            ticket_id="INC-9237",
            subject="Laptop overheating and random shutdowns",
            description=description,
            reporter=Reporter(
                name="Priya Nair",
                email="priya.nair@contoso.com",
                department="Marketing",
            ),
            created_at="2026-03-18T11:30:00Z",
            channel=TicketChannel.PORTAL,
            attachments=[],
        ),
        gold=TriageDecision(
            ticket_id="INC-9237",
            category=TicketCategory.HARDWARE,
            priority=Priority.P3,
            assigned_team=AssignedTeam.ENDPOINT_ENG,
            needs_escalation=False,
            missing_information=[MissingInfoField.DEVICE_INFO],
            next_best_action=(
                "Schedule a hardware inspection of the Dell Latitude "
                "5540 to diagnose the overheating and unexpected "
                "shutdowns during video calls."
            ),
            remediation_steps=[
                "Run Dell built-in diagnostics to check thermal sensor readings",
                "Inspect internal fan and heat sink for dust buildup or failure",
                "Update BIOS and thermal management drivers to latest versions",
                "If hardware fault confirmed, arrange replacement under warranty",
            ],
        ),
        tag=_TAG,
        test_name="systeminfo_command_dump",
        test_description=(
            "Tests extraction of a straightforward hardware overheating "
            "issue buried under a full Windows systeminfo command dump "
            "including hotfixes, NIC details, and memory statistics."
        ),
    )


def _arm_template_noise() -> EvalScenario:
    """ARM/Bicep IaC template pasted in deployment failure ticket."""
    description = (
        "Our nightly deployment to staging failed again last night. I am "
        "pasting the ARM template we are using so you can see the config. "
        "The error happens when the App Service tries to start.\n\n"
        "{\n"
        '  "$schema": "https://schema.management.azure.com/schemas/'
        '2019-04-01/deploymentTemplate.json#",\n'
        '  "contentVersion": "1.0.0.0",\n'
        '  "parameters": {\n'
        '    "appServicePlanName": {\n'
        '      "type": "string",\n'
        '      "defaultValue": "asp-contoso-staging"\n'
        "    },\n"
        '    "webAppName": {\n'
        '      "type": "string",\n'
        '      "defaultValue": "app-contoso-orders-stg"\n'
        "    },\n"
        '    "location": {\n'
        '      "type": "string",\n'
        '      "defaultValue": "[resourceGroup().location]"\n'
        "    },\n"
        '    "skuName": {\n'
        '      "type": "string",\n'
        '      "defaultValue": "P1v3"\n'
        "    },\n"
        '    "linuxFxVersion": {\n'
        '      "type": "string",\n'
        '      "defaultValue": "DOTNETCORE|8.0"\n'
        "    }\n"
        "  },\n"
        '  "resources": [\n'
        "    {\n"
        '      "type": "Microsoft.Web/serverfarms",\n'
        '      "apiVersion": "2022-09-01",\n'
        '      "name": "[parameters(\'appServicePlanName\')]",\n'
        '      "location": "[parameters(\'location\')]",\n'
        '      "sku": {\n'
        '        "name": "[parameters(\'skuName\')]",\n'
        '        "capacity": 2\n'
        "      },\n"
        '      "kind": "linux",\n'
        '      "properties": {\n'
        '        "reserved": true\n'
        "      }\n"
        "    },\n"
        "    {\n"
        '      "type": "Microsoft.Web/sites",\n'
        '      "apiVersion": "2022-09-01",\n'
        '      "name": "[parameters(\'webAppName\')]",\n'
        '      "location": "[parameters(\'location\')]",\n'
        '      "dependsOn": [\n'
        "        \"[resourceId('Microsoft.Web/serverfarms', "
        "parameters('appServicePlanName'))]\"\n"
        "      ],\n"
        '      "properties": {\n'
        '        "serverFarmId": "[resourceId(\'Microsoft.Web/'
        "serverfarms', parameters('appServicePlanName'))]\",\n"
        '        "siteConfig": {\n'
        '          "linuxFxVersion": "[parameters(\'linuxFxVersion\')]",\n'
        '          "alwaysOn": true,\n'
        '          "appSettings": [\n'
        '            { "name": "ASPNETCORE_ENVIRONMENT", '
        '"value": "Staging" },\n'
        '            { "name": "ConnectionStrings__Default", '
        '"value": "Server=sql-contoso-stg.database.windows.net;'
        'Database=orders;" }\n'
        "          ]\n"
        "        }\n"
        "      }\n"
        "    }\n"
        "  ]\n"
        "}\n\n"
        'The deployment pipeline shows: "ERROR: The resource '
        "Microsoft.Web/sites/app-contoso-orders-stg failed with status "
        'CancelledByUser." But nobody cancelled it — it just timed out '
        "after 20 minutes waiting for the app to become healthy. The app "
        "logs show a connection string error but the connection string "
        "looks correct in the template above.\n\n"
        "Can someone help? This is blocking our release for Thursday.\n\n"
        "— Rafael"
    )
    return EvalScenario(
        ticket=Ticket(
            ticket_id="INC-9238",
            subject="Staging deployment fails — App Service won't start",
            description=description,
            reporter=Reporter(
                name="Rafael Costa",
                email="rafael.costa@contoso.com",
                department="DevOps",
            ),
            created_at="2026-03-18T07:45:00Z",
            channel=TicketChannel.EMAIL,
            attachments=["deploy-pipeline-log.txt"],
        ),
        gold=TriageDecision(
            ticket_id="INC-9238",
            category=TicketCategory.SOFTWARE,
            priority=Priority.P2,
            assigned_team=AssignedTeam.ENTERPRISE_APPS,
            needs_escalation=False,
            missing_information=[
                MissingInfoField.ERROR_MESSAGE,
                MissingInfoField.APPLICATION_VERSION,
            ],
            next_best_action=(
                "Investigate the App Service startup failure and "
                "connection string error that is causing the staging "
                "deployment to time out."
            ),
            remediation_steps=[
                "Review App Service application logs for the full connection string error",
                "Verify the staging SQL database is accessible from the App Service subnet",
                "Check if the managed identity or credentials for the database are configured correctly",
                "Re-run the deployment pipeline after fixing the connection issue",
            ],
        ),
        tag=_TAG,
        test_name="arm_template_noise",
        test_description=(
            "Tests extraction of a deployment failure issue from a "
            "ticket dominated by a pasted ARM JSON template with "
            "parameters, resources, and nested properties."
        ),
    )


def _codepage_mojibake_printer() -> EvalScenario:
    """CP-1252/UTF-8 encoding corruption in a printer issue ticket."""
    description = (
        "Hi IT,\n\n"
        "Iâ\x80\x99m having trouble with my printer. Every time I try to "
        "print from the finance application the output comes out garbled. "
        "The printer is an HP LaserJet Pro MFP M428fdn on the 3rd floor "
        "near room 312.\n\n"
        "Error message I see: â\x80\x9cPrint job failed â\x80\x93 "
        "driver incompatible with current configurationâ\x80\x9d\n\n"
        "I\xc2\xb4ve tried the following:\n"
        "â\x80¢ Restarting the printer â\x80\x93 didnâ\x80\x99t help\n"
        "â\x80¢ Reinstalling the driver â\x80\x93 same error\n"
        "â\x80¢ Printing from another application â\x80\x93 works fine "
        "for Word docs but not the finance app\n"
        "â\x80¢ Tried a different printer (HP Color LaserJet on 2nd "
        "floor) â\x80\x93 same issue from finance app\n\n"
        "My colleague Fran\xc3\xa7ois also has the problem since the "
        "update on March 15. Before that everything was fine. The print "
        "jobs show in the queue as â\x80\x9cprintingâ\x80\x9d for about "
        "30 seconds then change to â\x80\x9cerrorâ\x80\x9d.\n\n"
        "This is affecting our month-end close process â\x80\x93 we need "
        "to print invoices and reports for auditing purposes. About 12 "
        "people in the finance department are affected.\n\n"
        "PC info: Dell OptiPlex 7090, Windows 11, asset tag CT-PC-4418\n\n"
        "Thanks for your help,\n"
        "Mireille Dub\xc3\xa9"
    )
    return EvalScenario(
        ticket=Ticket(
            ticket_id="INC-9239",
            subject="Printer not working from finance application",
            description=description,
            reporter=Reporter(
                name="Mireille Dubé",
                email="mireille.dube@contoso.com",
                department="Finance",
            ),
            created_at="2026-03-18T14:20:00Z",
            channel=TicketChannel.EMAIL,
            attachments=[],
        ),
        gold=TriageDecision(
            ticket_id="INC-9239",
            category=TicketCategory.HARDWARE,
            priority=Priority.P3,
            assigned_team=AssignedTeam.ENDPOINT_ENG,
            needs_escalation=False,
            missing_information=[
                MissingInfoField.APPLICATION_VERSION,
                MissingInfoField.ERROR_MESSAGE,
            ],
            next_best_action=(
                "Investigate the printer driver incompatibility with "
                "the finance application that started after the "
                "March 15 update affecting the finance department."
            ),
            remediation_steps=[
                "Check which update was applied on March 15 and whether it changed print drivers",
                "Test printing from the finance application with the latest HP Universal Print Driver",
                "Verify print spooler service health and clear any stuck jobs",
                "Roll back the problematic driver update if a compatible version is identified",
            ],
        ),
        tag=_TAG,
        test_name="codepage_mojibake_printer",
        test_description=(
            "Tests triage accuracy when the ticket body is riddled "
            "with CP-1252/UTF-8 mojibake artifacts such as curly "
            "quote replacements, broken bullet points, and mangled "
            "accented characters."
        ),
    )


def _recursive_forward_chain() -> EvalScenario:
    """10+ levels of email forwarding burying a SharePoint issue."""
    description = (
        "---------- Forwarded message ----------\n"
        "From: Hannah Kim <hannah.kim@contoso.com>\n"
        "To: IT Help Desk <helpdesk@contoso.com>\n"
        "Date: March 18, 2026 at 9:47 AM\n"
        "Subject: FW: FW: FW: FW: FW: FW: FW: FW: FW: FW: SharePoint "
        "site broken\n\n"
        "Adding help desk.\n\n"
        "---------- Forwarded message ----------\n"
        "From: Tomás Herrera <tomas.herrera@contoso.com>\n"
        "To: Hannah Kim <hannah.kim@contoso.com>\n"
        "Date: March 18, 2026 at 9:38 AM\n"
        "Subject: RE: FW: FW: FW: FW: FW: FW: FW: FW: FW: SharePoint "
        "site broken\n\n"
        "Hannah — can you loop in IT? I don't have the helpdesk email.\n\n"
        "---------- Forwarded message ----------\n"
        "From: Aisha Patel <aisha.patel@contoso.com>\n"
        "To: Tomás Herrera <tomas.herrera@contoso.com>\n"
        "Date: March 18, 2026 at 9:25 AM\n"
        "Subject: RE: FW: FW: FW: FW: FW: FW: FW: FW: SharePoint "
        "site broken\n\n"
        "Same here. None of us on the project team can access it.\n\n"
        "---------- Forwarded message ----------\n"
        "From: David Okonkwo <david.okonkwo@contoso.com>\n"
        "To: Aisha Patel <aisha.patel@contoso.com>\n"
        "Date: March 18, 2026 at 9:14 AM\n"
        "Subject: RE: FW: FW: FW: FW: FW: FW: FW: SharePoint "
        "site broken\n\n"
        "Confirming — I get a 403 Forbidden error too.\n\n"
        "---------- Forwarded message ----------\n"
        "From: Li Wei <li.wei@contoso.com>\n"
        "To: David Okonkwo <david.okonkwo@contoso.com>\n"
        "Date: March 18, 2026 at 9:02 AM\n"
        "Subject: RE: FW: FW: FW: FW: FW: FW: SharePoint site broken\n\n"
        "I forwarded to the site owner but she is on PTO.\n\n"
        "---------- Forwarded message ----------\n"
        "From: Emma Johansson <emma.johansson@contoso.com>\n"
        "To: Li Wei <li.wei@contoso.com>\n"
        "Date: March 18, 2026 at 8:48 AM\n"
        "Subject: RE: FW: FW: FW: FW: FW: SharePoint site broken\n\n"
        "Yep same issue. The whole project site is inaccessible.\n\n"
        "---------- Forwarded message ----------\n"
        "From: Marcus Johnson <marcus.johnson@contoso.com>\n"
        "To: Emma Johansson <emma.johansson@contoso.com>\n"
        "Date: March 18, 2026 at 8:32 AM\n"
        "Subject: RE: FW: FW: FW: FW: SharePoint site broken\n\n"
        "I asked our manager and he said to escalate.\n\n"
        "---------- Forwarded message ----------\n"
        "From: Fatima Al-Rashid <fatima.alrashid@contoso.com>\n"
        "To: Marcus Johnson <marcus.johnson@contoso.com>\n"
        "Date: March 18, 2026 at 8:21 AM\n"
        "Subject: RE: FW: FW: FW: SharePoint site broken\n\n"
        "Same for me. Can someone contact IT?\n\n"
        "---------- Forwarded message ----------\n"
        "From: James Chen <james.chen@contoso.com>\n"
        "To: Fatima Al-Rashid <fatima.alrashid@contoso.com>\n"
        "Date: March 18, 2026 at 8:09 AM\n"
        "Subject: RE: FW: FW: SharePoint site broken\n\n"
        "Also getting 403. Started this morning.\n\n"
        "---------- Forwarded message ----------\n"
        "From: Nina Bergström <nina.bergstrom@contoso.com>\n"
        "To: James Chen <james.chen@contoso.com>\n"
        "Date: March 18, 2026 at 7:55 AM\n"
        "Subject: RE: FW: SharePoint site broken\n\n"
        "Me too! I need the Q1 budget spreadsheet from that site today.\n\n"
        "---------- Forwarded message ----------\n"
        "From: Carlos Rivera <carlos.rivera@contoso.com>\n"
        "To: Project Phoenix Team <phoenix-team@contoso.com>\n"
        "Date: March 18, 2026 at 7:41 AM\n"
        "Subject: SharePoint site broken\n\n"
        "Hey team — the Project Phoenix SharePoint site at "
        "https://contoso.sharepoint.com/sites/ProjectPhoenix is giving "
        "me a 403 Forbidden error when I try to access it. I was able "
        "to get in yesterday with no problems. I need to upload the "
        "weekly status report before 10 AM. Has anyone else noticed this?"
    )
    return EvalScenario(
        ticket=Ticket(
            ticket_id="INC-9240",
            subject="FW: FW: FW: FW: FW: FW: FW: FW: FW: FW: SharePoint site broken",
            description=description,
            reporter=Reporter(
                name="Hannah Kim",
                email="hannah.kim@contoso.com",
                department="Project Management",
            ),
            created_at="2026-03-18T09:52:00Z",
            channel=TicketChannel.EMAIL,
            attachments=[],
        ),
        gold=TriageDecision(
            ticket_id="INC-9240",
            category=TicketCategory.SOFTWARE,
            priority=Priority.P3,
            assigned_team=AssignedTeam.ENTERPRISE_APPS,
            needs_escalation=False,
            missing_information=[
                MissingInfoField.AFFECTED_USERS,
                MissingInfoField.TIMESTAMP,
            ],
            next_best_action=(
                "Restore access to the Project Phoenix SharePoint site "
                "which is returning 403 Forbidden for multiple team "
                "members since this morning."
            ),
            remediation_steps=[
                "Check SharePoint admin center for permission changes on the Project Phoenix site",
                "Verify the site collection owner account status and permissions",
                "Review audit logs for any recent permission or policy modifications",
                "Restore site access for the project team and confirm accessibility",
            ],
        ),
        tag=_TAG,
        test_name="recursive_forward_chain",
        test_description=(
            "Tests extraction of a SharePoint access issue buried "
            "under 10+ levels of email forwarding with repeated "
            "headers, timestamps, and me-too replies from different "
            "users."
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
        _terraform_state_dump(),
        _graphql_query_paste(),
        _azure_devops_pipeline_output(),
        _slack_webhook_payload(),
        _registry_export(),
        _xml_config_dump(),
        _base64_pdf_attachment(),
        _duplicate_forward_chain(),
        _rtf_format_codes(),
        _teams_chat_export(),
        _postman_collection_paste(),
        _cron_job_output(),
        _jira_import_artifacts(),
        _binary_log_corruption(),
        _markdown_rendering_noise(),
        _pgp_signed_email(),
        _long_cc_bcc_headers(),
        _xml_soap_fault(),
        _kubernetes_pod_describe(),
        _raw_hex_dump(),
        _mixed_encoding_wifi(),
        _sql_query_data_corruption(),
        _multilingual_legal_disclaimer(),
        _near_empty_ticket(),
        _vulnerability_scanner_dump(),
        _prometheus_metrics_flood(),
        _systeminfo_command_dump(),
        _arm_template_noise(),
        _codepage_mojibake_printer(),
        _recursive_forward_chain(),
    ]
