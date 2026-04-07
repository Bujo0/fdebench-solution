# Copyright (c) Microsoft. All rights reserved.
"""Data cleanup edge case scenarios.

These scenarios test whether a triage system can correctly classify tickets
that contain noisy, malformed, or unusually formatted content — the kind
of messy data that real enterprise ticket systems produce daily.
"""

import base64

from evals.models import Category
from evals.models import Channel
from evals.models import EvalScenario
from evals.models import MissingInfoField
from evals.models import Priority
from evals.models import Reporter
from evals.models import ScenarioSuite
from evals.models import ScenarioTag
from evals.models import Team
from evals.models import Ticket
from evals.models import TriageDecision

_CONTOSO_REPORTER = Reporter(
    name="Test User",
    email="test.user@contoso.com",
    department="IT",
)

# Long corporate email disclaimer (~2KB) used to pad descriptions
_CORPORATE_DISCLAIMER = (
    "\n\n---\nCONFIDENTIALITY NOTICE: This email and any attachments are for the "
    "exclusive and confidential use of the intended recipient. If you are not the "
    "intended recipient, please do not read, distribute, or take action based on this "
    "message. If you have received this communication in error, please notify the "
    "sender immediately and delete this message from your system. Contoso Financial "
    "Services Ltd. does not accept liability for any damage caused by any virus "
    "transmitted by this email. The views expressed in this email are those of the "
    "individual sender and may not necessarily reflect the views of Contoso Financial "
    "Services Ltd. Contoso Financial Services Ltd. is registered in England and Wales "
    "with company number 12345678. Registered office: 100 Financial Plaza, London "
    "EC2V 8AA, United Kingdom. Authorized and regulated by the Financial Conduct "
    "Authority (FCA). This message has been scanned for viruses by our email security "
    "system. Any opinions expressed in this email are those of the individual and not "
    "necessarily of the company. Contoso Financial Services Ltd. reserves the right to "
    "monitor all email communications through its networks. Please consider the "
    "environment before printing this email."
)

_EMAIL_SIGNATURE = (
    "\n\n--\nSarah Chen | Senior Analyst | Wealth Management Division\n"
    "Contoso Financial Services\n"
    "Tel: +1 (212) 555-0142 | Mobile: +1 (917) 555-0198\n"
    "Email: sarah.chen@contoso.com\n"
    "100 Financial Plaza, 23rd Floor, New York, NY 10004\n"
    "LinkedIn: linkedin.com/in/sarahchen | Internal: teams.contoso.com/sarah.chen\n"
    '"Integrity, Innovation, Impact" — Contoso Values\n'
    "🌿 Please consider the environment before printing this email.\n"
)


def _make_long_description(core_message: str, repeat_count: int = 15) -> str:
    """Build a very long description by padding a real message with noise."""
    forwarding_chain = (
        "---------- Forwarded message ---------\n"
        "From: IT Helpdesk <helpdesk@contoso.com>\n"
        "Date: Mon, Mar 16, 2026 at 3:45 PM\n"
        "Subject: Re: Re: Re: VPN Issues\n"
        "To: sarah.chen@contoso.com\n\n"
        "Hi Sarah, we're looking into this. Can you provide more details?\n"
    )
    parts = [core_message]
    for _ in range(repeat_count):
        parts.append(forwarding_chain)
    parts.append(_EMAIL_SIGNATURE)
    parts.append(_CORPORATE_DISCLAIMER)
    return "\n".join(parts)


def _make_base64_image_block() -> str:
    """Generate a realistic base64-encoded image block."""
    # Minimal 1x1 red PNG pixel
    pixel_bytes = (
        b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01"
        b"\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde\x00"
        b"\x00\x00\x0cIDATx\x9cc\xf8\x0f\x00\x00\x01\x01\x00"
        b"\x05\x18\xd8N\x00\x00\x00\x00IEND\xaeB`\x82"
    )
    encoded = base64.b64encode(pixel_bytes).decode("ascii")
    # Repeat to simulate a large embedded image
    large_block = encoded * 100
    return f"\n\n[Inline image: screenshot.png]\ndata:image/png;base64,{large_block}\n\n"


def _make_html_email_body(core_message: str) -> str:
    """Wrap a message in realistic HTML email formatting noise."""
    return (
        '<html><head><meta http-equiv="Content-Type" content="text/html; charset=UTF-8">'
        "</head><body>"
        '<div style="font-family: Calibri, sans-serif; font-size: 11pt;">'
        f"<p>{core_message}</p>"
        "</div>"
        '<div style="border-top: 1px solid #ccc; padding-top: 10px; margin-top: 20px;">'
        "<p><b>Sarah Chen</b> | Senior Analyst</p>"
        "<p>Contoso Financial Services</p>"
        '<p><img src="cid:logo@contoso.com" width="150" height="40" '
        'alt="Contoso Logo"></p>'
        '<p style="font-size: 8pt; color: #666;">CONFIDENTIALITY NOTICE: '
        "This email is intended solely for the use of the individual to whom it is "
        "addressed. If you are not the intended recipient, you are hereby notified "
        "that any disclosure, copying, distribution, or use of any of the information "
        "contained in this transmission is strictly prohibited.</p>"
        "</div></body></html>"
    )


def _make_log_dump() -> str:
    """Generate a pasted server log dump."""
    lines = []
    for i in range(50):
        lines.append(
            f"2026-03-17T09:{i:02d}:00.{i * 17 % 1000:03d}Z "
            f"ERROR [prod-db-01] Connection pool exhausted - "
            f"active=50 idle=0 waiting={i + 12} "
            f"query='SELECT * FROM transactions WHERE date > ...' "
            f"elapsed={200 + i * 50}ms"
        )
    return "\n".join(lines)


def build_data_cleanup_suite() -> ScenarioSuite:
    """Build the complete data cleanup evaluation scenario suite."""
    scenarios = [
        EvalScenario(
            scenario_id="DC-001",
            name="Very long email with forwarding chain",
            description="A legitimate VPN issue buried in a 10K+ character email with "
            "repeated forwarding headers, signatures, and disclaimers.",
            tags=[ScenarioTag.DATA_CLEANUP, ScenarioTag.LONG_CONTENT, ScenarioTag.NOISE],
            ticket=Ticket(
                ticket_id="INC-9001",
                subject="Re: Re: Re: Fwd: VPN keeps disconnecting",
                description=_make_long_description(
                    "My VPN keeps dropping every 30 minutes since Monday. I'm on the "
                    "London office Wi-Fi, Floor 3. Using Contoso VPN client v4.1. "
                    "Already tried reconnecting and restarting my laptop. Need this "
                    "fixed — I have client calls all week."
                ),
                reporter=Reporter(
                    name="Sarah Chen",
                    email="sarah.chen@contoso.com",
                    department="Wealth Management",
                ),
                created_at="2026-03-17T09:14:00Z",
                channel=Channel.EMAIL,
            ),
            gold=TriageDecision(
                ticket_id="INC-9001",
                category=Category.NETWORK,
                priority=Priority.P3,
                assigned_team=Team.NETWORK_OPS,
                needs_escalation=False,
                missing_information=[MissingInfoField.ERROR_MESSAGE],
                next_best_action="Investigate VPN disconnect pattern on London office Floor 3 "
                "Wi-Fi. Check VPN client v4.1 compatibility and session timeout settings.",
                remediation_steps=[
                    "Check VPN client v4.1 is the latest supported version",
                    "Review VPN session timeout and keepalive settings",
                    "Check London Floor 3 Wi-Fi access point health and load",
                    "If pattern persists, capture network trace during next disconnect",
                ],
            ),
            rationale="The system must extract the real issue (VPN disconnects) from a very "
            "long email chain with noise. The forwarding headers, signatures, and "
            "disclaimers should not affect classification.",
        ),
        EvalScenario(
            scenario_id="DC-002",
            name="Base64 image embedded in description",
            description="A ticket with a base64-encoded screenshot embedded in the "
            "description alongside the actual error message.",
            tags=[ScenarioTag.DATA_CLEANUP, ScenarioTag.ENCODING, ScenarioTag.NOISE],
            ticket=Ticket(
                ticket_id="INC-9002",
                subject="Error when opening SAP — screenshot attached",
                description="I get an error 'SAP GUI 770: Connection refused to "
                "application server sap-prod-01:3200' every time I try to open SAP "
                "since this morning. Here is a screenshot of the error:"
                + _make_base64_image_block()
                + "Please help, I need SAP for month-end reporting due today.",
                reporter=Reporter(
                    name="Michael Torres",
                    email="michael.torres@contoso.com",
                    department="Finance",
                ),
                created_at="2026-03-17T08:45:00Z",
                channel=Channel.EMAIL,
            ),
            gold=TriageDecision(
                ticket_id="INC-9002",
                category=Category.SOFTWARE,
                priority=Priority.P2,
                assigned_team=Team.ENTERPRISE_APPS,
                needs_escalation=False,
                missing_information=[MissingInfoField.AFFECTED_USERS],
                next_best_action="Check SAP application server sap-prod-01 health and "
                "connectivity. Verify if this is an isolated user issue or a "
                "system-wide outage affecting month-end processing.",
                remediation_steps=[
                    "Check SAP application server sap-prod-01:3200 connectivity and status",
                    "Verify SAP service is running and accepting connections",
                    "Check if other Finance users are experiencing the same error",
                    "If server is down, escalate to SAP Basis team for immediate restore",
                    "Confirm resolution with user before month-end deadline",
                ],
            ),
            rationale="Base64-encoded images in email bodies should be treated as noise. "
            "The actual issue (SAP connection error) and context (month-end urgency) "
            "must be extracted from around the binary data.",
        ),
        EvalScenario(
            scenario_id="DC-003",
            name="HTML email with formatting tags",
            description="A ticket submitted via email where the description contains "
            "raw HTML tags and inline CSS from the email client.",
            tags=[ScenarioTag.DATA_CLEANUP, ScenarioTag.NOISE, ScenarioTag.ENCODING],
            ticket=Ticket(
                ticket_id="INC-9003",
                subject="Can't access SharePoint team site",
                description=_make_html_email_body(
                    "I cannot access the Wealth Management SharePoint site since "
                    "yesterday afternoon. I get a &ldquo;403 Forbidden&rdquo; error "
                    "when I try to open it in Chrome. Other SharePoint sites work fine. "
                    "I need the Q1 reporting templates that are only on this site."
                ),
                reporter=Reporter(
                    name="Amanda Foster",
                    email="amanda.foster@contoso.com",
                    department="Wealth Management",
                ),
                created_at="2026-03-17T10:22:00Z",
                channel=Channel.EMAIL,
            ),
            gold=TriageDecision(
                ticket_id="INC-9003",
                category=Category.DATA,
                priority=Priority.P3,
                assigned_team=Team.DATA_PLATFORM,
                needs_escalation=False,
                missing_information=[MissingInfoField.TIMESTAMP],
                next_best_action="Check SharePoint site permissions for the Wealth Management "
                "team site. Verify if permissions were changed recently or if site "
                "access policy was modified.",
                remediation_steps=[
                    "Check SharePoint admin center for Wealth Management site permissions",
                    "Verify user's group membership and access level",
                    "Check if recent permission changes or policy updates affected access",
                    "If permission issue, restore access and confirm user can reach the site",
                    "Verify Q1 reporting templates are accessible",
                ],
            ),
            rationale="HTML tags, CSS, and HTML entity references should be stripped or "
            "ignored. The core issue (SharePoint 403 error) must be identified "
            "through the formatting noise.",
        ),
        EvalScenario(
            scenario_id="DC-004",
            name="Email signature only — no actual issue",
            description="A ticket where the description is just a detailed email "
            "signature with no actual issue described.",
            tags=[ScenarioTag.DATA_CLEANUP, ScenarioTag.NOISE, ScenarioTag.MALFORMED],
            ticket=Ticket(
                ticket_id="INC-9004",
                subject="(no subject)",
                description=_EMAIL_SIGNATURE + _CORPORATE_DISCLAIMER,
                reporter=Reporter(
                    name="Sarah Chen",
                    email="sarah.chen@contoso.com",
                    department="Wealth Management",
                ),
                created_at="2026-03-17T11:00:00Z",
                channel=Channel.EMAIL,
            ),
            gold=TriageDecision(
                ticket_id="INC-9004",
                category=Category.NOT_SUPPORT,
                priority=Priority.P4,
                assigned_team=Team.NONE,
                needs_escalation=False,
                missing_information=[],
                next_best_action="Close — this appears to be an accidental submission "
                "containing only an email signature. No actionable issue present.",
                remediation_steps=[
                    "No action required — accidental submission detected, close ticket",
                ],
            ),
            rationale="A ticket with only an email signature and legal disclaimer has no "
            "actionable issue. It should be classified as 'Not a Support Ticket'.",
        ),
        EvalScenario(
            scenario_id="DC-005",
            name="Auto-generated bounce-back message",
            description="A delivery failure notification that was accidentally "
            "submitted as a support ticket.",
            tags=[ScenarioTag.DATA_CLEANUP, ScenarioTag.NOISE],
            ticket=Ticket(
                ticket_id="INC-9005",
                subject="Delivery Status Notification (Failure)",
                description=(
                    "This is an automatically generated Delivery Status Notification.\n\n"
                    "Delivery to the following recipient failed permanently:\n\n"
                    "    john.doe@external-partner.com\n\n"
                    "Technical details of permanent failure:\n"
                    "Google tried to deliver your message, but it was rejected by the "
                    "server for the recipient domain external-partner.com by "
                    "mx.external-partner.com [203.0.113.45].\n\n"
                    "The error that the other server returned was:\n"
                    "550 5.1.1 The email account that you tried to reach does not exist. "
                    "Please try double-checking the recipient's email address for typos "
                    "or unnecessary spaces.\n\n"
                    "----- Original message -----\n"
                    "From: sarah.chen@contoso.com\n"
                    "To: john.doe@external-partner.com\n"
                    "Subject: Q1 Financial Review Meeting\n"
                    "Date: Mon, 17 Mar 2026 09:00:00 -0400\n\n"
                    "Hi John, please find attached the Q1 review documents..."
                ),
                reporter=Reporter(
                    name="MAILER-DAEMON",
                    email="mailer-daemon@contoso.com",
                    department="IT",
                ),
                created_at="2026-03-17T09:05:00Z",
                channel=Channel.EMAIL,
            ),
            gold=TriageDecision(
                ticket_id="INC-9005",
                category=Category.NOT_SUPPORT,
                priority=Priority.P4,
                assigned_team=Team.NONE,
                needs_escalation=False,
                missing_information=[],
                next_best_action="Close — this is an automated email delivery failure "
                "notification (bounce-back), not a support request.",
                remediation_steps=[
                    "No action required — auto-generated bounce-back, close ticket",
                ],
            ),
            rationale="Email bounce-back messages from MAILER-DAEMON are not real support "
            "tickets. The system must recognize automated delivery failure "
            "notifications.",
        ),
        EvalScenario(
            scenario_id="DC-006",
            name="Server log dump pasted as description",
            description="A ticket where the user pasted 50 lines of server error logs "
            "as the description with minimal context.",
            tags=[ScenarioTag.DATA_CLEANUP, ScenarioTag.LONG_CONTENT, ScenarioTag.NOISE],
            ticket=Ticket(
                ticket_id="INC-9006",
                subject="Database errors — logs attached",
                description=(
                    "Prod database is throwing errors. Here are the logs:\n\n"
                    + _make_log_dump()
                    + "\n\nPlease investigate ASAP."
                ),
                reporter=Reporter(
                    name="DevOps Team",
                    email="devops-alerts@contoso.com",
                    department="Engineering",
                ),
                created_at="2026-03-17T06:30:00Z",
                channel=Channel.EMAIL,
            ),
            gold=TriageDecision(
                ticket_id="INC-9006",
                category=Category.DATA,
                priority=Priority.P1,
                assigned_team=Team.DATA_PLATFORM,
                needs_escalation=True,
                missing_information=[MissingInfoField.AFFECTED_USERS, MissingInfoField.BUSINESS_IMPACT],
                next_best_action="Investigate connection pool exhaustion on prod-db-01. "
                "Database is unable to serve queries — potential production outage "
                "affecting transaction processing.",
                remediation_steps=[
                    "Check prod-db-01 connection pool configuration and active connections",
                    "Identify and terminate long-running or stale connections",
                    "Increase connection pool limits if appropriate",
                    "Review the query 'SELECT * FROM transactions' for optimization",
                    "Monitor connection pool health after fix to confirm stability",
                ],
            ),
            rationale="Despite the noisy log dump, the system must identify this as a "
            "production database outage (connection pool exhausted) requiring "
            "P1/escalation. The logs contain signal — they show a real issue.",
        ),
        EvalScenario(
            scenario_id="DC-007",
            name="Unicode and encoding artifacts",
            description="A ticket with Unicode replacement characters, mojibake, "
            "and encoding artifacts from a corrupted email.",
            tags=[ScenarioTag.DATA_CLEANUP, ScenarioTag.ENCODING, ScenarioTag.MALFORMED],
            ticket=Ticket(
                ticket_id="INC-9007",
                subject="Canâ\u0080\u0099t connect to VPN â\u0080\u0093 please help",
                description=(
                    "Iâ\u0080\u0099ve been trying to connect to the VPN since this "
                    "morning but it keeps giving me an error. I\u00e2\u0080\u0099m "
                    "working from home today and I canâ\u0080\u0099t access anything "
                    "on the internal network.\n\n"
                    "Error message says: â\u0080\u009cAuthentication failed â\u0080\u0093 "
                    "please contact your administratorâ\u0080\u009d\n\n"
                    "Iâ\u0080\u0099m using Windows 11 and the Contoso VPN client. "
                    "My password was changed last week and I\u00e2\u0080\u0099ve been "
                    "using the new one.\n\n"
                    "Thanks,\n"
                    "Raj â\u0080\u0093 Trading Floor"
                ),
                reporter=Reporter(
                    name="Raj Mehta",
                    email="raj.mehta@contoso.com",
                    department="Trading",
                ),
                created_at="2026-03-17T07:45:00Z",
                channel=Channel.EMAIL,
            ),
            gold=TriageDecision(
                ticket_id="INC-9007",
                category=Category.NETWORK,
                priority=Priority.P2,
                assigned_team=Team.NETWORK_OPS,
                needs_escalation=False,
                missing_information=[MissingInfoField.APPLICATION_VERSION],
                next_best_action="Investigate VPN authentication failure. Check if recent "
                "password change synced correctly to VPN authentication backend. "
                "User is on trading floor — time-sensitive.",
                remediation_steps=[
                    "Verify user's credentials are synced to VPN auth (Entra ID / RADIUS)",
                    "Check if recent password change propagated to all auth systems",
                    "Test VPN connectivity with a known-good account from same location",
                    "If auth sync issue, force credential sync and have user retry",
                    "Confirm resolution — trading floor user needs immediate access",
                ],
            ),
            rationale="Mojibake (UTF-8 decoded as Latin-1) should not prevent the system "
            "from understanding the issue. The VPN authentication failure and "
            "trading floor urgency must be extracted through encoding noise.",
        ),
        EvalScenario(
            scenario_id="DC-008",
            name="Extremely long subject line",
            description="A ticket with a 500+ character subject line that contains "
            "the full issue description, with an empty body.",
            tags=[ScenarioTag.DATA_CLEANUP, ScenarioTag.LONG_CONTENT, ScenarioTag.MALFORMED],
            ticket=Ticket(
                ticket_id="INC-9008",
                subject=(
                    "URGENT URGENT URGENT my laptop screen went black and I cannot see "
                    "anything and I tried restarting it three times and it still wont "
                    "work and I have a presentation in one hour and I need this fixed "
                    "immediately because my manager is going to be very upset if I cant "
                    "do the presentation and I dont have a backup laptop and the IT desk "
                    "said to submit a ticket so here I am please someone help me this is "
                    "really urgent I am on Floor 5 of the NYC office near the kitchen "
                    "area and my laptop is a Dell Latitude 5520 with the docking station"
                ),
                description="",
                reporter=Reporter(
                    name="Jennifer Park",
                    email="jennifer.park@contoso.com",
                    department="Sales",
                ),
                created_at="2026-03-17T13:00:00Z",
                channel=Channel.PORTAL,
            ),
            gold=TriageDecision(
                ticket_id="INC-9008",
                category=Category.HARDWARE,
                priority=Priority.P2,
                assigned_team=Team.ENDPOINT,
                needs_escalation=False,
                missing_information=[MissingInfoField.ERROR_MESSAGE],
                next_best_action="Dispatch technician to NYC office Floor 5 with a loaner "
                "laptop. User has a presentation in one hour — Dell Latitude 5520 "
                "with black screen, possibly display or docking station failure.",
                remediation_steps=[
                    "Attempt external monitor connection to rule out display failure",
                    "Test with and without docking station",
                    "If hardware failure confirmed, provide loaner laptop immediately",
                    "Schedule Dell warranty repair for the Latitude 5520",
                    "Transfer user's data/profile to loaner if needed before presentation",
                ],
            ),
            rationale="When the subject line contains all the information and the "
            "description is empty, the system must use the subject for "
            "classification. The urgency (presentation in 1 hour) and details "
            "(Dell Latitude 5520, Floor 5) are all in the subject.",
        ),
        EvalScenario(
            scenario_id="DC-009",
            name="Phone transcript with filler words",
            description="A messy phone call transcript with speech disfluencies, "
            "filler words, and partial sentences.",
            tags=[ScenarioTag.DATA_CLEANUP, ScenarioTag.NOISE, ScenarioTag.MALFORMED],
            ticket=Ticket(
                ticket_id="INC-9009",
                subject="Phone call — user reports printing issue",
                description=(
                    "[Transcribed from phone call — 3/17/2026 10:15 AM]\n\n"
                    "Caller: Um, hi, yeah so, uh, I'm having this... this problem with "
                    "the, you know, the printer? The one on... let me think... the 4th "
                    "floor? No wait, 3rd floor. Yeah, 3rd floor, the one near the, um, "
                    "near the break room. So I tried to print — can you hear me? OK good "
                    "— so I tried to print this document, it's a... it's an important "
                    "client report, and it just... nothing happens. Like, I hit print "
                    "and it says 'sent to printer' but nothing comes out. And I tried "
                    "it like, I don't know, five times? Maybe six? And my colleague "
                    "tried too and same thing. So it's not just me I think. Oh and "
                    "also, uh, the display on the printer is showing some kind of "
                    "error, like... paper jam? But there's no paper jammed, I checked. "
                    "It's been like this since... since this morning I think. Yeah. "
                    "Can someone come look at it? Thanks."
                ),
                reporter=Reporter(
                    name="Call Center",
                    email="callcenter@contoso.com",
                    department="Operations",
                ),
                created_at="2026-03-17T10:15:00Z",
                channel=Channel.PHONE,
            ),
            gold=TriageDecision(
                ticket_id="INC-9009",
                category=Category.HARDWARE,
                priority=Priority.P3,
                assigned_team=Team.ENDPOINT,
                needs_escalation=False,
                missing_information=[MissingInfoField.DEVICE_INFO],
                next_best_action="Dispatch technician to check the 3rd floor printer near "
                "the break room. Display shows paper jam error but no jam found — "
                "likely sensor issue. Multiple users affected.",
                remediation_steps=[
                    "Check printer paper jam sensors for debris or misalignment",
                    "Clear any phantom paper jam errors and restart printer",
                    "Verify print queue is not stuck with stale jobs",
                    "Test print from multiple workstations to confirm fix",
                    "If sensor hardware failure, schedule printer service call",
                ],
            ),
            rationale="Phone transcripts are messy with fillers (um, uh, like) and "
            "self-corrections. The system must extract the real issue: a 3rd floor "
            "printer showing a false paper jam error, affecting multiple users.",
        ),
        EvalScenario(
            scenario_id="DC-010",
            name="Excessive URLs and links in description",
            description="A ticket with numerous URLs, documentation links, and "
            "Stack Overflow references cluttering the description.",
            tags=[ScenarioTag.DATA_CLEANUP, ScenarioTag.NOISE],
            ticket=Ticket(
                ticket_id="INC-9010",
                subject="Azure AD sync failing — tried everything",
                description=(
                    "Entra ID (Azure AD) sync has been failing since yesterday. I've "
                    "already tried the following from the docs:\n\n"
                    "1. https://learn.microsoft.com/en-us/entra/identity/hybrid/"
                    "connect/tshoot-connect-sync-errors\n"
                    "2. https://learn.microsoft.com/en-us/entra/identity/hybrid/"
                    "connect/how-to-connect-fix-default-rules\n"
                    "3. https://stackoverflow.com/questions/12345678/"
                    "azure-ad-connect-sync-errors\n"
                    "4. https://community.microsoft.com/t5/microsoft-entra/bd-p/"
                    "Microsoft-Entra\n"
                    "5. https://learn.microsoft.com/en-us/entra/identity/hybrid/"
                    "connect/reference-connect-sync-functions-reference\n\n"
                    "Error in sync log: 'Error Code: 0x80230619 — Unable to sync "
                    "object cn=svc-sharepoint to target directory. Object has conflicting "
                    "proxy addresses.'\n\n"
                    "This is blocking new hire onboarding — 3 new employees starting "
                    "Monday can't be provisioned until sync is working.\n\n"
                    "See also:\n"
                    "- Internal wiki: https://wiki.contoso.com/pages/entra-id-sync-guide\n"
                    "- Previous ticket: INC-3456\n"
                    "- Azure status: https://status.azure.com/en-us/status\n"
                    "- MS admin portal: https://admin.microsoft.com"
                ),
                reporter=Reporter(
                    name="Alex Wu",
                    email="alex.wu@contoso.com",
                    department="IT",
                ),
                created_at="2026-03-17T14:30:00Z",
                channel=Channel.PORTAL,
            ),
            gold=TriageDecision(
                ticket_id="INC-9010",
                category=Category.ACCESS_AUTH,
                priority=Priority.P2,
                assigned_team=Team.IAM,
                needs_escalation=False,
                missing_information=[MissingInfoField.ENVIRONMENT_DETAILS],
                next_best_action="Investigate Entra ID sync failure — proxy address conflict "
                "on svc-sharepoint service account. Blocking new hire provisioning "
                "for 3 employees starting Monday.",
                remediation_steps=[
                    "Check conflicting proxy addresses on cn=svc-sharepoint object",
                    "Resolve proxy address conflict in on-premises AD",
                    "Force delta sync and verify sync completes without errors",
                    "Confirm new hire provisioning pipeline is unblocked",
                    "Reference previous ticket INC-3456 for related context",
                ],
            ),
            rationale="The many URLs are reference noise. The system must focus on the "
            "actual error (proxy address conflict), impact (new hire onboarding "
            "blocked), and correctly route to IAM.",
        ),
        EvalScenario(
            scenario_id="DC-011",
            name="Repeated copy-paste artifacts",
            description="A ticket where the user accidentally pasted the same "
            "text multiple times.",
            tags=[ScenarioTag.DATA_CLEANUP, ScenarioTag.NOISE, ScenarioTag.MALFORMED],
            ticket=Ticket(
                ticket_id="INC-9011",
                subject="Outlook keeps freezing",
                description=(
                    "Outlook keeps freezing for about 30 seconds every time I open a "
                    "new email. It started after the latest update was pushed last night. "
                    "I'm on Windows 11, Outlook version 16.0.17328.20162.\n\n"
                    "Outlook keeps freezing for about 30 seconds every time I open a "
                    "new email. It started after the latest update was pushed last night. "
                    "I'm on Windows 11, Outlook version 16.0.17328.20162.\n\n"
                    "Outlook keeps freezing for about 30 seconds every time I open a "
                    "new email. It started after the latest update was pushed last night. "
                    "I'm on Windows 11, Outlook version 16.0.17328.20162.\n\n"
                    "Sorry if this sent multiple times — my email was acting up."
                ),
                reporter=Reporter(
                    name="David Kim",
                    email="david.kim@contoso.com",
                    department="Compliance",
                ),
                created_at="2026-03-17T08:20:00Z",
                channel=Channel.EMAIL,
            ),
            gold=TriageDecision(
                ticket_id="INC-9011",
                category=Category.SOFTWARE,
                priority=Priority.P3,
                assigned_team=Team.ENDPOINT,
                needs_escalation=False,
                missing_information=[],
                next_best_action="Investigate Outlook freezing after latest update. "
                "Check if update version 16.0.17328.20162 has known issues. "
                "May need rollback.",
                remediation_steps=[
                    "Check for known issues with Outlook version 16.0.17328.20162",
                    "Clear Outlook cache and repair the Office installation",
                    "If issue persists, roll back the latest update",
                    "Test Outlook performance after fix",
                    "Report the issue to M365 admin if affecting multiple users",
                ],
            ),
            rationale="Repeated copy-paste text should be deduplicated. The real issue "
            "(Outlook freezing after update) appears in the first copy and "
            "provides complete information including version numbers.",
        ),
        EvalScenario(
            scenario_id="DC-012",
            name="Mixed languages in description",
            description="A ticket mixing English and another language, common in "
            "multinational companies like Contoso.",
            tags=[ScenarioTag.DATA_CLEANUP, ScenarioTag.ENCODING],
            ticket=Ticket(
                ticket_id="INC-9012",
                subject="Bloomberg terminal — 接続エラー (connection error)",
                description=(
                    "Bloomberg terminal on Trading Floor Singapore is showing a "
                    "connection error since 8 AM SGT. \n\n"
                    "エラーメッセージ: 'BLP API — Connection to B-PIPE failed: "
                    "Timeout after 30000ms'\n\n"
                    "This is affecting all 5 traders on the Singapore floor. "
                    "我们需要这个工作 — Q1 reporting deadline is today.\n\n"
                    "Terminal ID: SGP-BT-042\n"
                    "Network port: 3C-14-A7\n\n"
                    "すぐに対応してください。(Please respond immediately.)"
                ),
                reporter=Reporter(
                    name="Yuki Tanaka",
                    email="yuki.tanaka@contoso.com",
                    department="Trading",
                ),
                created_at="2026-03-17T08:15:00Z",
                channel=Channel.PORTAL,
            ),
            gold=TriageDecision(
                ticket_id="INC-9012",
                category=Category.SOFTWARE,
                priority=Priority.P1,
                assigned_team=Team.ENTERPRISE_APPS,
                needs_escalation=True,
                missing_information=[],
                next_best_action="Investigate Bloomberg B-PIPE connection failure on Singapore "
                "trading floor. All 5 traders affected — Q1 reporting deadline today. "
                "Check network connectivity to Bloomberg data center.",
                remediation_steps=[
                    "Check Bloomberg B-PIPE service status and connectivity from Singapore",
                    "Verify network port 3C-14-A7 is active and not blocked",
                    "Test B-PIPE connection from terminal SGP-BT-042 directly",
                    "If network issue, escalate to Network Operations for Singapore link",
                    "Contact Bloomberg support if API-side issue confirmed",
                ],
            ),
            rationale="Mixed English/Japanese/Chinese text should not confuse the system. "
            "The Bloomberg terminal error on trading floor is P1 because it "
            "affects all 5 traders with a Q1 deadline today.",
        ),
        EvalScenario(
            scenario_id="DC-013",
            name="CSV data dump in description",
            description="A ticket where the user pasted raw CSV data showing "
            "error patterns.",
            tags=[ScenarioTag.DATA_CLEANUP, ScenarioTag.NOISE, ScenarioTag.LONG_CONTENT],
            ticket=Ticket(
                ticket_id="INC-9013",
                subject="OneDrive sync errors — here's the error log export",
                description=(
                    "OneDrive keeps failing to sync. Exported the error log:\n\n"
                    "Timestamp,File,Error,Code\n"
                    + "\n".join(
                        f"2026-03-17T{8 + i // 60:02d}:{i % 60:02d}:00Z,"
                        f"Q1_Report_v{i}.xlsx,"
                        f"'The file is locked by another process',0x80070020"
                        for i in range(40)
                    )
                    + "\n\nThis has been going on all morning. I need these files "
                    "synced for a client meeting at 2 PM."
                ),
                reporter=Reporter(
                    name="Lisa Wang",
                    email="lisa.wang@contoso.com",
                    department="Wealth Management",
                ),
                created_at="2026-03-17T11:30:00Z",
                channel=Channel.PORTAL,
            ),
            gold=TriageDecision(
                ticket_id="INC-9013",
                category=Category.DATA,
                priority=Priority.P3,
                assigned_team=Team.DATA_PLATFORM,
                needs_escalation=False,
                missing_information=[MissingInfoField.DEVICE_INFO],
                next_best_action="Investigate OneDrive file locking errors. Multiple Excel "
                "files stuck with 'locked by another process' error — likely stale "
                "file locks or conflicting co-authoring sessions.",
                remediation_steps=[
                    "Check for stale file locks on the affected Excel files",
                    "Clear OneDrive sync cache and force re-sync",
                    "Verify no other process is holding locks on the files",
                    "If co-authoring conflict, close all open sessions and retry",
                    "Confirm sync completes before 2 PM client meeting",
                ],
            ),
            rationale="The CSV dump contains diagnostic information (file lock errors) "
            "that helps identify the root cause. The system must parse through "
            "the structured data and extract the OneDrive sync issue.",
        ),
        EvalScenario(
            scenario_id="DC-014",
            name="Ticket references attachments only",
            description="A ticket where the description refers to attachments "
            "that provide all context, but the text itself is minimal.",
            tags=[ScenarioTag.DATA_CLEANUP, ScenarioTag.MALFORMED],
            ticket=Ticket(
                ticket_id="INC-9014",
                subject="See attached",
                description="Please see the attached screenshots for details.",
                reporter=Reporter(
                    name="Ryan O'Brien",
                    email="ryan.obrien@contoso.com",
                    department="HR",
                ),
                created_at="2026-03-17T09:45:00Z",
                channel=Channel.PORTAL,
                attachments=["error_screenshot_1.png", "error_screenshot_2.png", "network_trace.pcap"],
            ),
            gold=TriageDecision(
                ticket_id="INC-9014",
                category=Category.GENERAL,
                priority=Priority.P4,
                assigned_team=Team.NONE,
                needs_escalation=False,
                missing_information=[
                    MissingInfoField.AFFECTED_SYSTEM,
                    MissingInfoField.ERROR_MESSAGE,
                    MissingInfoField.STEPS_TO_REPRODUCE,
                ],
                next_best_action="Contact reporter to describe the issue — the ticket "
                "references screenshots but provides no description of the problem.",
                remediation_steps=[
                    "Contact Ryan O'Brien to describe the issue in text",
                    "Review attached screenshots for initial context once described",
                    "Route to appropriate team once the issue is understood",
                ],
            ),
            rationale="When a ticket only says 'see attached' with no description, the "
            "system cannot meaningfully triage. It should flag missing information "
            "and not guess at the category.",
        ),
        EvalScenario(
            scenario_id="DC-015",
            name="Email thread with multiple interleaved replies",
            description="A complex email thread where multiple people replied "
            "inline, making it hard to find the actual issue.",
            tags=[ScenarioTag.DATA_CLEANUP, ScenarioTag.NOISE, ScenarioTag.LONG_CONTENT],
            ticket=Ticket(
                ticket_id="INC-9015",
                subject="Re: Re: Fwd: Wi-Fi issues Floor 7",
                description=(
                    "> > > Original message from Tom:\n"
                    "> > > The Wi-Fi on Floor 7 has been spotty all week.\n"
                    "> >\n"
                    "> > Jennifer replied:\n"
                    "> > Same here — I'm dropping every 20 minutes. Floor 7 east wing.\n"
                    "> > Can barely join Teams calls.\n"
                    ">\n"
                    "> Mike replied:\n"
                    "> Actually I think it's worse than spotty. I ran a speed test "
                    "> and we're getting 2 Mbps down. We should be getting 100+.\n"
                    "> It's affecting the whole east wing, not just our area.\n"
                    ">\n"
                    "> Tom again:\n"
                    "> Update — I asked around and at least 15 people on Floor 7 east "
                    "> wing are having the same issue. Started Monday after the weekend "
                    "> maintenance.\n"
                    "\n"
                    "Latest from Sarah (today):\n"
                    "Adding myself to this thread — I can confirm it's Floor 7 east "
                    "wing only. West wing is fine. We have a big client demo tomorrow "
                    "and need this fixed. Submitting as a ticket now.\n\n"
                    + _EMAIL_SIGNATURE
                ),
                reporter=Reporter(
                    name="Sarah Chen",
                    email="sarah.chen@contoso.com",
                    department="Wealth Management",
                ),
                created_at="2026-03-17T16:00:00Z",
                channel=Channel.EMAIL,
            ),
            gold=TriageDecision(
                ticket_id="INC-9015",
                category=Category.NETWORK,
                priority=Priority.P2,
                assigned_team=Team.NETWORK_OPS,
                needs_escalation=False,
                missing_information=[],
                next_best_action="Investigate Wi-Fi degradation on Floor 7 east wing. "
                "15+ users affected since Monday post-maintenance. Speed dropped "
                "from 100+ to 2 Mbps. Client demo tomorrow.",
                remediation_steps=[
                    "Check Floor 7 east wing access points for post-maintenance issues",
                    "Review weekend maintenance changes that may have affected east wing",
                    "Run diagnostics on AP signal strength and channel utilization",
                    "If AP hardware issue, deploy temporary AP for client demo coverage",
                    "Verify speed test shows normal throughput after fix",
                ],
            ),
            rationale="The email thread format with '>' quoting makes it hard to parse. "
            "The system must synthesize information from multiple replies: "
            "Floor 7 east wing, 15+ users, 2 Mbps speed, post-maintenance, "
            "and the client demo urgency.",
        ),
        EvalScenario(
            scenario_id="DC-016",
            name="Description with massive base64 attachment payload",
            description="A ticket where a user accidentally pasted a very large "
            "base64-encoded file (multi-KB) directly into the description, "
            "with the actual issue buried at the top.",
            tags=[ScenarioTag.DATA_CLEANUP, ScenarioTag.ENCODING, ScenarioTag.LONG_CONTENT],
            ticket=Ticket(
                ticket_id="INC-9016",
                subject="Intune enrollment error",
                description=(
                    "Getting error 0x80180014 when trying to enroll my new laptop in "
                    "Intune. Already tried resetting the device once.\n\n"
                    "Attached device diagnostic log (inline because portal won't let me "
                    "upload):\n\n"
                    + base64.b64encode(b"x" * 5000).decode("ascii")
                    + "\n\n"
                    + base64.b64encode(b"y" * 5000).decode("ascii")
                    + "\n\nEnd of log."
                ),
                reporter=Reporter(
                    name="Carlos Herrera",
                    email="carlos.herrera@contoso.com",
                    department="Risk Management",
                ),
                created_at="2026-03-17T09:30:00Z",
                channel=Channel.PORTAL,
            ),
            gold=TriageDecision(
                ticket_id="INC-9016",
                category=Category.HARDWARE,
                priority=Priority.P3,
                assigned_team=Team.ENDPOINT,
                needs_escalation=False,
                missing_information=[MissingInfoField.DEVICE_INFO],
                next_best_action="Investigate Intune enrollment error 0x80180014 on new "
                "laptop. Error typically indicates device limit or autopilot profile "
                "mismatch.",
                remediation_steps=[
                    "Check Intune device enrollment limits for the user",
                    "Verify the device's autopilot profile assignment",
                    "Clear any stale device registrations in Entra ID",
                    "Re-attempt enrollment after clearing stale records",
                    "If error persists, check Intune connector health and logs",
                ],
            ),
            rationale="The base64 diagnostic logs are noise — the real issue is at the "
            "top: Intune enrollment error 0x80180014. The system must not choke "
            "on the large binary payload.",
        ),
    ]

    return ScenarioSuite(
        suite_name="Data Cleanup Edge Cases",
        suite_description="Scenarios testing triage system robustness against noisy, "
        "malformed, and unusually formatted ticket content.",
        suite_type="data_cleanup",
        scenarios=scenarios,
    )
