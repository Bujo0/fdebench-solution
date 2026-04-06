# Copyright (c) Microsoft. All rights reserved.
"""Data cleanup evaluation scenarios.

Tests the triage system's ability to extract meaningful information from
noisy, malformed, or unusually structured ticket data. Real-world IT support
tickets are messy — these scenarios simulate the worst of what the system
will encounter: massive email chains, embedded binary data, garbled encodings,
empty descriptions, and more.

Each scenario pairs a challenging input ticket with the correct gold answer,
ensuring the system can "see through the noise" to the actual support request.
"""

import base64

from ms.evals_core.constants import Category
from ms.evals_core.constants import Channel
from ms.evals_core.constants import MissingInfo as MissingInformation
from ms.evals_core.constants import Priority
from ms.evals_core.constants import ScenarioTag
from ms.evals_core.constants import Team as AssignedTeam
from ms.evals_core.models import GoldAnswer as TriageGold
from ms.evals_core.models import Reporter
from ms.evals_core.models import Scenario
from ms.evals_core.models import Ticket as TicketInput

_CATEGORY = "data_cleanup"


def _reporter(
    name: str = "Jane Doe",
    email: str = "jane.doe@contoso.com",
    department: str = "IT",
) -> Reporter:
    return Reporter(name=name, email=email, department=department)


def _build_long_email_chain(core_issue: str, chain_depth: int = 25) -> str:
    """Simulate a deeply nested email reply chain with the real issue buried at the bottom."""
    lines: list[str] = [core_issue, ""]
    for i in range(chain_depth):
        sender = f"user{i}@contoso.com"
        lines.append(f"--- Original message from {sender} on 2026-03-{10 + (i % 20):02d} ---")
        lines.append("Hi team, just following up on the thread below. Any updates?")
        lines.append("Thanks,")
        lines.append(f"User {i}")
        lines.append("")
        lines.append(f"> {'> ' * i}Previous reply content about unrelated topics and meeting schedules.")
        lines.append(f"> {'> ' * i}Reminder: Q2 budget review is next Thursday.")
        lines.append("")
    return "\n".join(lines)


def _build_base64_noise(size_bytes: int = 4096) -> str:
    """Generate a realistic base64-encoded block simulating an embedded image."""
    raw_bytes = bytes(range(256)) * (size_bytes // 256 + 1)
    return base64.b64encode(raw_bytes[:size_bytes]).decode("ascii")


def _build_html_email(inner_text: str) -> str:
    """Wrap a support request in verbose HTML email markup."""
    return (
        "<!DOCTYPE html><html><head>"
        '<meta charset="UTF-8">'
        "<style>body{font-family:Calibri,sans-serif;font-size:11pt;color:#333}"
        ".signature{border-top:1px solid #ccc;margin-top:20px;padding-top:10px;"
        "font-size:9pt;color:#666}"
        "</style></head><body>"
        f"<p>{inner_text}</p>"
        '<div class="signature">'
        "<p><b>Jane Doe</b> | Senior VP, Wealth Management</p>"
        "<p>Contoso Financial Services | New York Office</p>"
        "<p>Phone: +1-555-0123 | Fax: +1-555-0124</p>"
        '<p><img src="cid:logo.png" alt="Contoso Logo"></p>'
        "<p><i>This email is confidential and intended solely for the use of the "
        "individual to whom it is addressed. If you are not the intended recipient, "
        "please notify the sender immediately and delete this email. Any unauthorized "
        "copying, disclosure, or distribution of the material in this email is "
        "strictly forbidden.</i></p>"
        "</div></body></html>"
    )


def _build_massive_signature() -> str:
    """Generate an oversized corporate email signature."""
    return (
        "\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "John Alexander Worthington III\n"
        "Executive Vice President & Chief Digital Transformation Officer\n"
        "Global Technology & Innovation Division\n"
        "Contoso Financial Services Group, Inc.\n"
        "A subsidiary of Contoso Holdings International, LLC\n"
        "\n"
        "📍 One Contoso Plaza, 47th Floor\n"
        "    350 Park Avenue, New York, NY 10022\n"
        "📞 Direct: +1 (212) 555-0147\n"
        "📱 Mobile: +1 (917) 555-0283\n"
        "📠 Fax: +1 (212) 555-0148\n"
        "✉️ john.worthington@contoso.com\n"
        "🌐 www.contoso.com/leadership/worthington\n"
        "💼 linkedin.com/in/jaworthington\n"
        "\n"
        "Office Hours: Mon–Fri 7:00 AM – 7:00 PM ET\n"
        "Executive Assistant: Patricia Chen (patricia.chen@contoso.com)\n"
        "\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        "\n"
        "CONFIDENTIALITY NOTICE: This electronic message and any attachments are\n"
        "confidential and may be privileged. They are intended for the sole use of\n"
        "the addressee(s). If you are not an intended recipient, you are hereby\n"
        "notified that any disclosure, copying, distribution, or use of any of the\n"
        "information contained in or attached to this message is strictly prohibited.\n"
        "If you have received this message in error, please notify the sender by\n"
        "reply email and immediately destroy all copies of this message and any\n"
        "attachments. Thank you.\n"
        "\n"
        "REGULATORY DISCLOSURE: Contoso Financial Services Group, Inc. is registered\n"
        "with the Securities and Exchange Commission (SEC) and is a member of FINRA\n"
        "and SIPC. Investment products are: Not FDIC Insured • No Bank Guarantee •\n"
        "May Lose Value.\n"
        "\n"
        "ENVIRONMENTAL NOTE: Please consider the environment before printing this email.\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
    )


def scenario_very_long_email_chain() -> Scenario:
    """Extremely long email chain with the actual issue buried at the bottom."""
    core_issue = (
        "Hi IT Support,\n\n"
        "My VPN connection drops every 15 minutes when I'm working from home. "
        "I'm using GlobalProtect v3.2 on Windows 11. The reconnection takes about "
        "2 minutes each time and I lose my RDP sessions. This has been happening "
        "since the March 15 update. I'm on Comcast residential internet, 200 Mbps. "
        "My colleague in the same apartment building doesn't have this issue."
    )
    description = _build_long_email_chain(core_issue, chain_depth=30)

    return Scenario(
        ticket=TicketInput(
            ticket_id="EVAL-DC-0001",
            subject="Re: Re: Re: Re: Re: VPN issues — any update?",
            description=description,
            reporter=_reporter("Michael Torres", "michael.torres@contoso.com", "Wealth Management"),
            created_at="2026-03-20T14:30:00Z",
            channel=Channel.EMAIL,
            attachments=[],
        ),
        gold=TriageGold(
            ticket_id="EVAL-DC-0001",
            category=Category.NETWORK,
            priority=Priority.P3,
            assigned_team=AssignedTeam.NETWORK_OPS,
            needs_escalation=False,
            missing_information=[MissingInformation.NETWORK_LOCATION],
            next_best_action=(
                "Investigate periodic VPN disconnection on GlobalProtect v3.2 "
                "post-March update. Check for known compatibility issues with the latest Windows update."
            ),
            remediation_steps=[
                "Verify GlobalProtect v3.2 is the latest supported version",
                "Check VPN gateway logs for disconnect patterns at 15-minute intervals",
                "Test with a different VPN profile or protocol",
                "Verify Windows 11 March update compatibility with GlobalProtect",
                "If issue persists, escalate to network engineering for VPN client patch review",
            ],
        ),
        tags=[ScenarioTag.LONG_EMAIL, ScenarioTag.EMAIL_CHAIN],
        description="30-level deep email chain with VPN issue buried at bottom",
        scenario_category=_CATEGORY,
        scenario_tag="EVAL-DC-0001",
    )


def scenario_base64_image_in_description() -> Scenario:
    """Ticket description contains a large base64-encoded image inline."""
    b64_block = _build_base64_noise(8192)
    description = (
        "My monitor keeps flickering every few seconds. Here's a screenshot of the issue:\n\n"
        f"data:image/png;base64,{b64_block}\n\n"
        "This started after IT replaced my docking station last week. I'm using a Dell U2723QE "
        "connected via USB-C through the new WD19TBS dock. The flickering happens even when I "
        "unplug the external monitor and use just the laptop screen, which makes me think it "
        "might be a driver issue rather than the dock itself."
    )

    return Scenario(
        ticket=TicketInput(
            ticket_id="EVAL-DC-0002",
            subject="Monitor flickering — screenshot attached inline",
            description=description,
            reporter=_reporter("Lisa Park", "lisa.park@contoso.com", "Trading"),
            created_at="2026-03-18T10:45:00Z",
            channel=Channel.EMAIL,
            attachments=["monitor_flicker.png"],
        ),
        gold=TriageGold(
            ticket_id="EVAL-DC-0002",
            category=Category.HARDWARE,
            priority=Priority.P3,
            assigned_team=AssignedTeam.ENDPOINT,
            needs_escalation=False,
            missing_information=[MissingInformation.DEVICE_INFO],
            next_best_action=(
                "Investigate monitor flickering after docking station replacement. "
                "Check display driver version and dock firmware."
            ),
            remediation_steps=[
                "Check display driver version and update if outdated",
                "Test with a different USB-C cable and port on the dock",
                "Update WD19TBS dock firmware to latest version",
                "Test with HDMI direct connection to rule out USB-C/dock issue",
                "If flickering persists on laptop screen alone, run hardware diagnostics on the display",
            ],
        ),
        tags=[ScenarioTag.BASE64_CONTENT],
        description="Ticket with large base64-encoded image data embedded inline",
        scenario_category=_CATEGORY,
        scenario_tag="EVAL-DC-0002",
    )


def scenario_raw_html_email() -> Scenario:
    """Ticket submitted via email with full HTML markup instead of plain text."""
    inner_text = (
        "I can't access SAP after changing my password this morning. "
        "Every time I try to log in, I get error <b>AUTH_FAILED_0x8004</b>. "
        "I've tried clearing my browser cache and using a different browser (Edge and Chrome). "
        "I need SAP access urgently for end-of-quarter financial reporting — deadline is tomorrow."
    )
    description = _build_html_email(inner_text)

    return Scenario(
        ticket=TicketInput(
            ticket_id="EVAL-DC-0003",
            subject="Can't access SAP after password change",
            description=description,
            reporter=_reporter("Robert Kim", "robert.kim@contoso.com", "Finance"),
            created_at="2026-03-28T08:15:00Z",
            channel=Channel.EMAIL,
            attachments=[],
        ),
        gold=TriageGold(
            ticket_id="EVAL-DC-0003",
            category=Category.SOFTWARE,
            priority=Priority.P2,
            assigned_team=AssignedTeam.ENTERPRISE_APPS,
            needs_escalation=False,
            missing_information=[MissingInformation.APPLICATION_VERSION],
            next_best_action=(
                "Investigate SAP authentication failure after password change. "
                "Check if SAP stored credentials need to be re-synced with the new Entra ID password."
            ),
            remediation_steps=[
                "Verify new password works for other Entra ID-authenticated services",
                "Clear SAP cached credentials in the browser",
                "Check SAP single sign-on configuration for credential sync issues",
                "If SAP uses separate credentials, initiate SAP-specific password reset",
                "Provide temporary access for end-of-quarter reporting if resolution is delayed",
            ],
        ),
        tags=[ScenarioTag.HTML_EMAIL],
        description="Full HTML email with styles and confidentiality footer",
        scenario_category=_CATEGORY,
        scenario_tag="EVAL-DC-0003",
    )


def scenario_massive_email_signature() -> Scenario:
    """Tiny issue buried under a massive corporate email signature."""
    description = "Printer on 5th floor jammed again." + _build_massive_signature()

    return Scenario(
        ticket=TicketInput(
            ticket_id="EVAL-DC-0004",
            subject="Printer issue",
            description=description,
            reporter=_reporter("John Worthington", "john.worthington@contoso.com", "Technology & Innovation"),
            created_at="2026-03-19T16:00:00Z",
            channel=Channel.EMAIL,
            attachments=[],
        ),
        gold=TriageGold(
            ticket_id="EVAL-DC-0004",
            category=Category.HARDWARE,
            priority=Priority.P4,
            assigned_team=AssignedTeam.ENDPOINT,
            needs_escalation=False,
            missing_information=[MissingInformation.DEVICE_INFO, MissingInformation.NETWORK_LOCATION],
            next_best_action="Dispatch technician to clear printer jam on 5th floor.",
            remediation_steps=[
                "Identify the specific printer model on the 5th floor",
                "Clear the paper jam following the manufacturer's instructions",
                "Check for torn paper remnants in the feed mechanism",
                "Run a test print to confirm resolution",
                "If recurring, schedule preventive maintenance",
            ],
        ),
        tags=[ScenarioTag.MASSIVE_SIGNATURE],
        description="One-sentence issue dwarfed by a massive corporate email signature",
        scenario_category=_CATEGORY,
        scenario_tag="EVAL-DC-0004",
    )


def scenario_garbled_encoding() -> Scenario:
    """Ticket with encoding corruption artifacts (mojibake) mixed with readable text."""
    description = (
        "I canâ\x80\x99t connect to the Wi-Fi in the London office since Monday. "
        "My laptop shows â\x80\x9cConnectedâ\x80\x9d but I have no internet access. "
        "Iâ\x80\x99ve tried forgetting the network and reconnecting. "
        "Other colleagues on the same floor (3rd floor, Canary Wharf) "
        "are not having this issue. My laptop is a ThinkPad X1 Carbon Gen 11 "
        "running Windows 11 23H2. The Ã©rror started after I returned from "
        "a trip to the Singapore office â\x80\x94 maybe something changed in the "
        "network settings during travel?"
    )

    return Scenario(
        ticket=TicketInput(
            ticket_id="EVAL-DC-0005",
            subject="WiFi not working — London office",
            description=description,
            reporter=_reporter("Emma Watson", "emma.watson@contoso.com", "Compliance"),
            created_at="2026-03-17T09:30:00Z",
            channel=Channel.EMAIL,
            attachments=[],
        ),
        gold=TriageGold(
            ticket_id="EVAL-DC-0005",
            category=Category.NETWORK,
            priority=Priority.P3,
            assigned_team=AssignedTeam.NETWORK_OPS,
            needs_escalation=False,
            missing_information=[],
            next_best_action=(
                "Investigate Wi-Fi connectivity issue on 3rd floor, London Canary Wharf office. "
                "Check if travel-related network profile changes are causing the problem."
            ),
            remediation_steps=[
                "Check Wi-Fi adapter status and run network diagnostics on the ThinkPad",
                "Reset network settings to clear any travel-related VPN or proxy configurations",
                "Verify the correct SSID and authentication method for the London office",
                "Test with a different Wi-Fi access point on the 3rd floor",
                "If issue persists, check for MAC address filtering or network policy changes",
            ],
        ),
        tags=[ScenarioTag.GARBLED_TEXT, ScenarioTag.UNICODE_HEAVY],
        description="UTF-8/latin-1 mojibake artifacts mixed with readable support request",
        scenario_category=_CATEGORY,
        scenario_tag="EVAL-DC-0005",
    )


def scenario_empty_description() -> Scenario:
    """Ticket with an effectively empty description (whitespace only)."""
    description = "   \n\n\t\t\n   \n  "

    return Scenario(
        ticket=TicketInput(
            ticket_id="EVAL-DC-0006",
            subject="HELP",
            description=description,
            reporter=_reporter("Alex Johnson", "alex.johnson@contoso.com", "HR"),
            created_at="2026-03-21T11:00:00Z",
            channel=Channel.CHAT,
            attachments=[],
        ),
        gold=TriageGold(
            ticket_id="EVAL-DC-0006",
            category=Category.GENERAL_INQUIRY,
            priority=Priority.P4,
            assigned_team=AssignedTeam.NONE,
            needs_escalation=False,
            missing_information=[
                MissingInformation.AFFECTED_SYSTEM,
                MissingInformation.ERROR_MESSAGE,
                MissingInformation.BUSINESS_IMPACT,
                MissingInformation.CONTACT_INFO,
            ],
            next_best_action=(
                "Contact the reporter to understand their actual issue. The ticket has no actionable information."
            ),
            remediation_steps=[
                "Reach out to the reporter via chat or phone to clarify the issue",
                "Gather details about the affected system, error messages, and urgency",
                "Update the ticket with the collected information",
                "Re-triage and route to the appropriate team once details are available",
            ],
        ),
        tags=[ScenarioTag.EMPTY_DESCRIPTION],
        description="Ticket with whitespace-only description and vague subject",
        scenario_category=_CATEGORY,
        scenario_tag="EVAL-DC-0006",
    )


def scenario_repeated_content() -> Scenario:
    """Same paragraph pasted many times, simulating a paste or form glitch."""
    single_block = (
        "My Outlook keeps crashing every time I open a calendar invite. "
        "This has been happening since the March update. I'm running "
        "Microsoft 365 Apps for Enterprise version 2402. I've already "
        "tried repairing Office through Settings but the problem persists."
    )
    description = "\n\n".join([single_block] * 15)

    return Scenario(
        ticket=TicketInput(
            ticket_id="EVAL-DC-0007",
            subject="Outlook crashing on calendar invites",
            description=description,
            reporter=_reporter("David Chen", "david.chen@contoso.com", "Engineering"),
            created_at="2026-03-22T09:00:00Z",
            channel=Channel.PORTAL,
            attachments=[],
        ),
        gold=TriageGold(
            ticket_id="EVAL-DC-0007",
            category=Category.SOFTWARE,
            priority=Priority.P3,
            assigned_team=AssignedTeam.ENTERPRISE_APPS,
            needs_escalation=False,
            missing_information=[MissingInformation.ERROR_MESSAGE, MissingInformation.DEVICE_INFO],
            next_best_action=(
                "Investigate Outlook crash on calendar invite open. "
                "Check for known issues with version 2402 and calendar rendering."
            ),
            remediation_steps=[
                "Check for pending Office updates beyond version 2402",
                "Run Outlook in safe mode to rule out add-in conflicts",
                "Clear the Outlook calendar cache",
                "Repair the Outlook profile",
                "If issue persists, collect crash dumps and escalate to Microsoft support",
            ],
        ),
        tags=[ScenarioTag.REPEATED_CONTENT],
        description="Same paragraph pasted 15 times simulating a form submission glitch",
        scenario_category=_CATEGORY,
        scenario_tag="EVAL-DC-0007",
    )


def scenario_mixed_language() -> Scenario:
    """Ticket mixing English and another language, from the Singapore office."""
    description = (
        "我的VPN连接不上了。I've been trying to connect to the corporate VPN from "
        "the Singapore office since this morning. 每次输入密码后就显示 "
        "'Authentication failed - contact your administrator'. "
        "我已经重置了密码两次。My colleague sitting next to me can connect fine. "
        "This is blocking my access to the internal SharePoint and the trading platform. "
        "请尽快处理，我有一个重要的客户会议在下午2点。"
    )

    return Scenario(
        ticket=TicketInput(
            ticket_id="EVAL-DC-0008",
            subject="VPN authentication failed — 新加坡办公室",
            description=description,
            reporter=_reporter("Wei Lin", "wei.lin@contoso.com", "Trading"),
            created_at="2026-03-18T03:45:00Z",
            channel=Channel.PORTAL,
            attachments=[],
        ),
        gold=TriageGold(
            ticket_id="EVAL-DC-0008",
            category=Category.NETWORK,
            priority=Priority.P2,
            assigned_team=AssignedTeam.NETWORK_OPS,
            needs_escalation=False,
            missing_information=[MissingInformation.AUTHENTICATION_METHOD],
            next_best_action=(
                "Investigate VPN authentication failure in Singapore office. "
                "Check if the password reset properly synced to the VPN gateway."
            ),
            remediation_steps=[
                "Verify the user's Entra ID credentials are synced to the VPN gateway",
                "Check if the account is locked out after multiple failed authentication attempts",
                "Verify VPN certificate validity for the Singapore office endpoint",
                "Test VPN connection with a known-good account to rule out infrastructure issues",
                "If credential sync is the issue, force a directory sync and retry",
            ],
        ),
        tags=[ScenarioTag.MIXED_LANGUAGE],
        description="Ticket mixing English and Mandarin Chinese from Singapore office",
        scenario_category=_CATEGORY,
        scenario_tag="EVAL-DC-0008",
    )


def scenario_attachment_reference_only() -> Scenario:
    """Description says only 'see attached' with no context."""
    description = "See attached screenshots. Thanks."

    return Scenario(
        ticket=TicketInput(
            ticket_id="EVAL-DC-0009",
            subject="Issue with my computer",
            description=description,
            reporter=_reporter("Maria Garcia", "maria.garcia@contoso.com", "Legal"),
            created_at="2026-03-19T13:20:00Z",
            channel=Channel.EMAIL,
            attachments=["screenshot1.png", "screenshot2.png", "screenshot3.png"],
        ),
        gold=TriageGold(
            ticket_id="EVAL-DC-0009",
            category=Category.GENERAL_INQUIRY,
            priority=Priority.P4,
            assigned_team=AssignedTeam.NONE,
            needs_escalation=False,
            missing_information=[
                MissingInformation.AFFECTED_SYSTEM,
                MissingInformation.ERROR_MESSAGE,
                MissingInformation.STEPS_TO_REPRODUCE,
                MissingInformation.BUSINESS_IMPACT,
            ],
            next_best_action=(
                "Contact the reporter for details. Ticket description references "
                "attachments that cannot be analyzed — need a text description of the issue."
            ),
            remediation_steps=[
                "Contact the reporter to request a written description of the issue",
                "Ask for specific error messages, affected applications, and timeline",
                "Review the referenced screenshots if they become available",
                "Re-triage once sufficient detail is provided",
            ],
        ),
        tags=[ScenarioTag.ATTACHMENT_ONLY],
        description="Description is just 'see attached' with no useful text",
        scenario_category=_CATEGORY,
        scenario_tag="EVAL-DC-0009",
    )


def scenario_excessive_whitespace_and_formatting() -> Scenario:
    """Ticket with excessive blank lines, tabs, and inconsistent spacing."""
    description = (
        "\n\n\n\n\n"
        "     Hi,     \n"
        "\n\n\n"
        "\t\tI think there might be an issue     with my \t\t email.\n"
        "\n\n\n\n\n\n\n\n"
        "  Outlook    is   not     syncing   my   inbox.  \n"
        "\n\n"
        "\t\t\tIt   shows   'Last  synced:   3   days   ago'  \n"
        "\n\n\n\n\n"
        "    I'm   on the    new    laptop   they   gave me     last   week.   \n"
        "\n\n\n\n\n\n\n\n\n\n"
        "   Thanks   \n"
        "\n\n\n"
    )

    return Scenario(
        ticket=TicketInput(
            ticket_id="EVAL-DC-0010",
            subject="email problem",
            description=description,
            reporter=_reporter("Tom Brown", "tom.brown@contoso.com", "Operations"),
            created_at="2026-03-20T08:30:00Z",
            channel=Channel.PORTAL,
            attachments=[],
        ),
        gold=TriageGold(
            ticket_id="EVAL-DC-0010",
            category=Category.SOFTWARE,
            priority=Priority.P3,
            assigned_team=AssignedTeam.ENTERPRISE_APPS,
            needs_escalation=False,
            missing_information=[MissingInformation.DEVICE_INFO, MissingInformation.ERROR_MESSAGE],
            next_best_action=(
                "Investigate Outlook sync failure on a newly provisioned laptop. "
                "Check if the email profile was properly migrated."
            ),
            remediation_steps=[
                "Verify the Outlook profile is correctly configured on the new laptop",
                "Check Outlook sync status and error logs",
                "Force a full mailbox resync",
                "Verify the user's M365 license includes Exchange Online",
                "If issue persists, recreate the Outlook profile",
            ],
        ),
        tags=[ScenarioTag.EXCESSIVE_WHITESPACE],
        description="Ticket with excessive whitespace, tabs, and inconsistent formatting",
        scenario_category=_CATEGORY,
        scenario_tag="EVAL-DC-0010",
    )


def scenario_multiple_base64_blocks_with_headers() -> Scenario:
    """Email with multiple MIME-style base64 blocks between text."""
    b64_block_1 = _build_base64_noise(2048)
    b64_block_2 = _build_base64_noise(3072)
    description = (
        "I'm getting a blue screen error on my laptop. Here are the crash dump details:\n\n"
        f"------=_Part_001\nContent-Type: application/octet-stream\n"
        f"Content-Transfer-Encoding: base64\n\n{b64_block_1}\n\n"
        "The BSOD shows DRIVER_IRQL_NOT_LESS_OR_EQUAL and happens about twice a day, "
        "usually when I'm in a Teams call. My laptop is a Surface Pro 9, 16GB RAM, "
        "running Windows 11 23H2. The issue started about a week ago.\n\n"
        f"------=_Part_002\nContent-Type: image/jpeg\n"
        f"Content-Transfer-Encoding: base64\n\n{b64_block_2}\n\n"
        "Please help — this is disrupting my client calls.\n"
        "------=_End\n"
    )

    return Scenario(
        ticket=TicketInput(
            ticket_id="EVAL-DC-0011",
            subject="Blue screen crashes during Teams calls",
            description=description,
            reporter=_reporter("Karen White", "karen.white@contoso.com", "Client Services"),
            created_at="2026-03-21T15:00:00Z",
            channel=Channel.EMAIL,
            attachments=["crash_dump.dmp", "bsod_photo.jpg"],
        ),
        gold=TriageGold(
            ticket_id="EVAL-DC-0011",
            category=Category.HARDWARE,
            priority=Priority.P2,
            assigned_team=AssignedTeam.ENDPOINT,
            needs_escalation=False,
            missing_information=[MissingInformation.REPRODUCTION_FREQUENCY],
            next_best_action=(
                "Investigate DRIVER_IRQL_NOT_LESS_OR_EQUAL BSOD on Surface Pro 9 "
                "during Teams calls. Analyze crash dump for faulty driver."
            ),
            remediation_steps=[
                "Analyze the crash dump to identify the faulting driver",
                "Update all device drivers, especially audio, video, and network drivers",
                "Check for Windows 11 23H2 known issues with Surface Pro 9",
                "Update Surface Pro 9 firmware via Surface app",
                "If driver update doesn't resolve, run Windows memory diagnostic to check RAM",
            ],
        ),
        tags=[ScenarioTag.BASE64_CONTENT],
        description="Email with multiple MIME base64 blocks interspersed with actual issue description",
        scenario_category=_CATEGORY,
        scenario_tag="EVAL-DC-0011",
    )


def scenario_extremely_long_single_paragraph() -> Scenario:
    """A single enormous paragraph with no line breaks — stream of consciousness."""
    filler_sentences = [
        "I already tried restarting it but that didn't help.",
        "My colleague suggested clearing the cache which I did.",
        "I also checked the company intranet for solutions but found nothing relevant.",
        "Last time this happened was about three months ago and it resolved on its own.",
        "I'm worried this might affect the quarterly report I need to submit.",
        "The deadline for the report is Friday and I can't afford any more delays.",
        "I mentioned this to my manager and she said to file a ticket.",
        "I've been using SAP for about five years and never had this kind of issue before.",
        "Some of my colleagues in the Singapore office reported similar problems last week.",
        "I wonder if this is related to the server migration that was announced last month.",
        "The error message disappears too quickly for me to read the full text.",
        "Sometimes the application just freezes for about 30 seconds before the error appears.",
    ]
    core = (
        "SAP keeps showing an error when I try to run the GL reconciliation report "
        "and I've been trying to fix this for the past two hours and nothing works. "
    )
    # Repeat filler to make a massive single paragraph
    description = core + " ".join(filler_sentences * 8)

    return Scenario(
        ticket=TicketInput(
            ticket_id="EVAL-DC-0012",
            subject="SAP report error",
            description=description,
            reporter=_reporter("Patricia Lee", "patricia.lee@contoso.com", "Finance"),
            created_at="2026-03-25T14:00:00Z",
            channel=Channel.PORTAL,
            attachments=[],
        ),
        gold=TriageGold(
            ticket_id="EVAL-DC-0012",
            category=Category.SOFTWARE,
            priority=Priority.P2,
            assigned_team=AssignedTeam.ENTERPRISE_APPS,
            needs_escalation=False,
            missing_information=[MissingInformation.ERROR_MESSAGE, MissingInformation.APPLICATION_VERSION],
            next_best_action=(
                "Investigate SAP GL reconciliation report failure. "
                "Capture the full error message and check for recent SAP server changes."
            ),
            remediation_steps=[
                "Capture the full SAP error code and message using a screenshot or video",
                "Check if other users can run the same GL reconciliation report",
                "Verify SAP server health and check for recent configuration changes",
                "Test the report with a smaller date range to isolate the issue",
                "If widespread, escalate to SAP Basis team for server-side investigation",
            ],
        ),
        tags=[ScenarioTag.LONG_EMAIL],
        description="Single massive paragraph (~3000 chars) stream of consciousness with no line breaks",
        scenario_category=_CATEGORY,
        scenario_tag="EVAL-DC-0012",
    )


def get_all_data_cleanup_scenarios() -> list[Scenario]:
    """Return all data cleanup evaluation scenarios."""
    return [
        scenario_very_long_email_chain(),
        scenario_base64_image_in_description(),
        scenario_raw_html_email(),
        scenario_massive_email_signature(),
        scenario_garbled_encoding(),
        scenario_empty_description(),
        scenario_repeated_content(),
        scenario_mixed_language(),
        scenario_attachment_reference_only(),
        scenario_excessive_whitespace_and_formatting(),
        scenario_multiple_base64_blocks_with_headers(),
        scenario_extremely_long_single_paragraph(),
    ]
