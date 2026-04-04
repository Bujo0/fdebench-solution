# Copyright (c) Microsoft. All rights reserved.
"""Data-cleanup evaluation dataset.

Tickets in this dataset contain noisy, malformed, or dirty input data —
long email chains, embedded base64, HTML markup, mojibake, excessive
whitespace, mixed languages, and other real-world artefacts.  The gold
answers reflect correct triage as if the data were clean, verifying that
the triage system can see through the noise.
"""

from ms.evals.constants import Category
from ms.evals.constants import Channel
from ms.evals.constants import MissingInfoField
from ms.evals.constants import Priority
from ms.evals.constants import Team
from ms.evals.models import EvalCase
from ms.evals.models import EvalDataset
from ms.evals.models import EvalTicket
from ms.evals.models import GoldAnswer
from ms.evals.models import Reporter

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

_LONG_EMAIL_BODY = (
    "Hi IT Support,\n\n"
    "I've been having serious VPN connectivity issues for the past three days. Every time I try to "
    "connect to GlobalProtect from my home office, the tunnel establishes for about 90 seconds and "
    "then drops with error code GP-ERR-4021. I'm on a Windows 11 laptop (Dell Latitude 5540), "
    "connecting over Comcast residential broadband. The issue started after last Friday's endpoint "
    "agent update pushed by Intune. I need this resolved ASAP because I cannot access any internal "
    "resources — Jira, Confluence, the internal Git server, or the finance SharePoint.\n\n"
    "I already tried:\n"
    "  1. Rebooting the laptop\n"
    "  2. Flushing DNS (ipconfig /flushdns)\n"
    "  3. Releasing and renewing DHCP\n"
    "  4. Disabling Windows Firewall temporarily\n"
    "  5. Uninstalling and reinstalling GlobalProtect 6.1.2\n\n"
    "None of these helped.\n\n"
    "Thanks,\nPriya Nair\nSenior Analyst, Risk Management\n\n"
    "---------- Forwarded message ----------\n"
    "From: Priya Nair <priya.nair@contoso.com>\n"
    "Date: Tue, 11 Mar 2026 07:32:00 -0500\n"
    "Subject: Re: VPN issues\n"
    "To: IT Support <itsupport@contoso.com>\n\n"
    "Hi team, just following up — the VPN is still broken this morning. I missed the 8 AM "
    "portfolio review call because I couldn't connect to the internal Teams bridge.\n\n"
    "---------- Forwarded message ----------\n"
    "From: Priya Nair <priya.nair@contoso.com>\n"
    "Date: Mon, 10 Mar 2026 16:05:00 -0500\n"
    "Subject: VPN issues\n"
    "To: IT Support <itsupport@contoso.com>\n\n"
    "Hi, my VPN is not connecting at all since this afternoon.\n\n"
    "---\n\n"
    "CONFIDENTIALITY NOTICE: This e-mail message, including any attachments, is for the sole use "
    "of the intended recipient(s) and may contain confidential and privileged information. Any "
    "unauthorized review, use, disclosure, or distribution is prohibited. If you are not the "
    "intended recipient, please contact the sender by reply e-mail and destroy all copies of the "
    "original message. This email has been scanned by the Contoso Email Security Gateway. "
    "Message-ID: <CAFp3Jz7kXmR+Qn8vL2wZ5gT@mail.contoso.com>\n\n"
    "---\n\n"
    "Contoso Financial Services | 200 Park Avenue, New York, NY 10166\n"
    "Tel: +1 (212) 555-0199 | Fax: +1 (212) 555-0198\n"
    "www.contoso.com | LinkedIn: contoso-financial\n\n"
    "♻ Please consider the environment before printing this email.\n\n"
    "This communication is intended solely for the addressee and may contain information that is "
    "confidential or legally privileged. If you are not the intended recipient, you must not read, "
    "use, copy, or disseminate this communication. Please notify the sender immediately by reply "
    "e-mail if you have received this communication in error, then delete it and all copies. "
    "Contoso Financial Services Limited is authorised and regulated by the Financial Conduct "
    "Authority. Registered in England. Company No. 12345678. Registered Office: 200 Park Avenue, "
    "New York, NY 10166. VAT Registration No. GB 123 4567 89.\n\n"
    "--- End of Forwarded Messages ---\n\n"
    "P.S. — My direct number is +1 (212) 555-0342 if you need to reach me.\n"
    "Asset class: Equity Derivatives | Desk: RM-3 | Bloomberg: PNAIR@CONTOSO\n\n"
    "========================================================================\n"
    "This message has been scanned by Contoso Antivirus Gateway v4.12.1.\n"
    "No threats detected. Scan ID: AV-20260312-081500-PRIYA-NAIR-7742\n"
    "========================================================================\n"
)

_BASE64_CHUNK = (
    "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAABAAAA"
    "AQCAYAAAD/qcomAAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAAL"
    "EwAACxMBAJqcGAAAAAd0SU1FB9oKFwgMNC3WkXYAACAASURBV"
    "Hic7d15fFT1vf/x95lsk5nsG0kgCQlhCfsSAoooLohi3bV1ad"
    "Xaam/dWm1rW2uXW7u4tXZR691s7WLdam3rVq24sIjsyCb7FiA"
    "hIfu+Tc7vj0kIIZOQhExmJnk9H495nDlnzsx8k8Mj8p7v9/s"
    "1TNOUJFVVVen48eOqqamRw+FQXFycMjIylJubq6ioKF9+HAAA"
    "AAAYVM6u/7vnkSfU0NR8+kEmEz7JVfzOHY1tpmlqy5Yt+uST"
    "TxQWFqbJkydr/PjxSk5OVmpqqux2u6++BQAAAAAMOW+8f0Dv7"
    "T7kk/c22+r8c9YOdHR0aNWqVTp27JjOO+88DR8+XNHR0RcXH"
)


def _dc001_very_long_email() -> EvalCase:
    return EvalCase(
        ticket=EvalTicket(
            ticket_id="INC-DC-001",
            subject="Re: Re: FW: VPN not connecting — GP-ERR-4021 since Friday",
            description=_LONG_EMAIL_BODY,
            reporter=Reporter(
                name="Priya Nair",
                email="priya.nair@contoso.com",
                department="Risk Management",
            ),
            created_at="2026-03-12T08:15:00Z",
            channel=Channel.EMAIL,
            attachments=[],
        ),
        gold=GoldAnswer(
            ticket_id="INC-DC-001",
            category=Category.NETWORK,
            priority=Priority.P2,
            assigned_team=Team.NETWORK_OPS,
            needs_escalation=False,
            missing_information=[MissingInfoField.APPLICATION_VERSION],
            next_best_action=(
                "Investigate GlobalProtect error GP-ERR-4021 on the user's Dell Latitude 5540 "
                "running Windows 11 — likely caused by the Intune endpoint agent update pushed "
                "last Friday conflicting with the VPN client."
            ),
            remediation_steps=[
                "Check GlobalProtect gateway logs for GP-ERR-4021 correlated with the user's session.",
                "Review the Intune endpoint agent update pushed Friday for known VPN compatibility issues.",
                "Roll back the endpoint agent update on a test device to confirm the root cause.",
                "If rollback resolves the issue, push a targeted fix or exemption via Intune.",
                "Confirm VPN connectivity is stable and the user can access internal resources.",
            ],
        ),
        tags=["long_content", "email_chain", "signature_noise"],
        description="Very long email body with forwarded thread, signatures, and legal disclaimers.",
    )


def _dc002_base64_image() -> EvalCase:
    return EvalCase(
        ticket=EvalTicket(
            ticket_id="INC-DC-002",
            subject="Monitor flickering — screenshot attached inline",
            description=(
                "Hi,\n\n"
                "My external monitor (Dell U2722D) has been flickering non-stop since this morning. "
                "It started after I docked my laptop (ThinkPad X1 Carbon Gen 11) into the Lenovo "
                "USB-C dock. The built-in laptop screen is fine — only the external monitor flickers.\n\n"
                "I took a photo with my phone and pasted it here:\n\n"
                f"{_BASE64_CHUNK}\n\n"
                "(Sorry, I wasn't sure how to attach it properly.)\n\n"
                "The flickering gets worse when I open Excel or any app with a lot of white background. "
                "I tried a different DisplayPort cable but same result. Could this be a driver issue? "
                "We had a Windows Update last week.\n\n"
                "Thanks,\nDavid Park\nQuantitative Research"
            ),
            reporter=Reporter(
                name="David Park",
                email="david.park@contoso.com",
                department="Quantitative Research",
            ),
            created_at="2026-03-13T10:22:00Z",
            channel=Channel.PORTAL,
            attachments=[],
        ),
        gold=GoldAnswer(
            ticket_id="INC-DC-002",
            category=Category.HARDWARE,
            priority=Priority.P3,
            assigned_team=Team.ENDPOINT,
            needs_escalation=False,
            missing_information=[MissingInfoField.DEVICE_INFO],
            next_best_action=(
                "Troubleshoot Dell U2722D monitor flickering via Lenovo USB-C dock on ThinkPad "
                "X1 Carbon Gen 11 — likely a display driver regression from last week's Windows Update."
            ),
            remediation_steps=[
                "Check the installed Intel/NVIDIA display driver version and compare against the pre-update version.",
                "Roll back the display driver to the previous version via Device Manager.",
                "Test the monitor with a direct HDMI or DisplayPort connection bypassing the dock.",
                "Update Lenovo USB-C dock firmware if a newer version is available.",
                "If driver rollback resolves the issue, defer the problematic driver in WSUS.",
            ],
        ),
        tags=["base64", "embedded_image"],
        description="Ticket contains base64-encoded image data pasted directly into description.",
    )


def _dc003_html_markup() -> EvalCase:
    return EvalCase(
        ticket=EvalTicket(
            ticket_id="INC-DC-003",
            subject="Outlook keeps crashing after update",
            description=(
                "<html>\n"
                "<head>\n"
                '<meta http-equiv="Content-Type" content="text/html; charset=utf-8">\n'
                "<style>\n"
                "body { font-family: Calibri, sans-serif; font-size: 11pt; }\n"
                ".signature { color: #888888; font-size: 9pt; }\n"
                "</style>\n"
                "</head>\n"
                "<body>\n"
                "<p>Hi IT Team,</p>\n"
                "<p>Outlook has been <b>crashing repeatedly</b> since the update that was pushed "
                "on <b>Tuesday morning</b>. Every time I try to open a calendar invite from the "
                "Legal team, Outlook freezes for about 10 seconds and then closes with this "
                "error:</p>\n"
                "<p><b>APPCRASH — mso40uiwin32client.dll</b><br>\n"
                "Exception code: <b>0xc0000005</b><br>\n"
                "Offset: 0x00000000001A3F7C</p>\n"
                "<p>I&apos;ve already tried running <b>Office Repair</b> (Quick Repair) but it "
                "didn&apos;t help. I haven&apos;t tried Online Repair yet because I wasn&apos;t "
                "sure if that would reset my settings.</p>\n"
                '<p>I can still use <b><a href="https://outlook.office365.com">Outlook Web '
                "App</a></b> without issues, so it's definitely the desktop client.</p>\n"
                "<br>\n"
                "<p>Thanks,</p>\n"
                '<p class="signature">Jennifer Liu<br>\n'
                "Associate General Counsel<br>\n"
                "Legal &amp; Compliance<br>\n"
                "Contoso Financial Services</p>\n"
                "</body>\n"
                "</html>"
            ),
            reporter=Reporter(
                name="Jennifer Liu",
                email="jennifer.liu@contoso.com",
                department="Legal & Compliance",
            ),
            created_at="2026-03-13T11:47:00Z",
            channel=Channel.EMAIL,
            attachments=[],
        ),
        gold=GoldAnswer(
            ticket_id="INC-DC-003",
            category=Category.SOFTWARE,
            priority=Priority.P3,
            assigned_team=Team.ENTERPRISE_APPS,
            needs_escalation=False,
            missing_information=[MissingInfoField.APPLICATION_VERSION],
            next_best_action=(
                "Diagnose Outlook desktop crash (0xc0000005 in mso40uiwin32client.dll) triggered "
                "by calendar invites from Legal — likely caused by Tuesday's Office update."
            ),
            remediation_steps=[
                "Identify the specific Office update pushed Tuesday and check for known issues.",
                "Run Outlook in safe mode to rule out add-in conflicts.",
                "Attempt to open the problematic calendar invite via Outlook Web App to confirm it is client-specific.",
                "Run Online Repair of the Office installation if safe mode does not resolve the crash.",
                "If Online Repair fails, roll back to the previous Office build via the Office Deployment Tool.",
            ],
        ),
        tags=["html", "markup"],
        description="Ticket body contains full HTML markup with tags, CSS, and HTML entities.",
    )


def _dc004_unicode_emoji() -> EvalCase:
    return EvalCase(
        ticket=EvalTicket(
            ticket_id="INC-DC-004",
            subject="WiFi is DEAD on 4th floor 🔥🔥🔥 HELP",
            description=(
                "🚨🚨🚨 URGENT 🚨🚨🚨\n\n"
                "The WiFi on the entire 4th floor (Building 2, Chicago) has been DOWN since "
                "about 8:45 AM this morning 💀💀💀\n\n"
                "NOBODY can connect — it's not just me, my whole team (12 people in Structured "
                "Products) is affected 😭😭😭\n\n"
                "We have a CLIENT PRESENTATION at 11:00 AM and we need internet access!!! ⚠️⚠️⚠️\n\n"
                "Things we tried:\n"
                "• Restarting laptops 💻❌\n"
                "• Forgetting the network and reconnecting ❌❌\n"
                "• Using mobile hotspot as backup 📱✅ (but it's too slow for the demo)\n\n"
                "The SSID 'Contoso-Corp' shows up but just spins when we try to connect 🔄🔄🔄\n\n"
                "PLEASE HELP ASAP 🙏🙏🙏🔥💀\n\n"
                "— Alex Rivera\n"
                "VP, Structured Products\n"
                "☎️ x4472"
            ),
            reporter=Reporter(
                name="Alex Rivera",
                email="alex.rivera@contoso.com",
                department="Structured Products",
            ),
            created_at="2026-03-13T09:02:00Z",
            channel=Channel.CHAT,
            attachments=[],
        ),
        gold=GoldAnswer(
            ticket_id="INC-DC-004",
            category=Category.NETWORK,
            priority=Priority.P1,
            assigned_team=Team.NETWORK_OPS,
            needs_escalation=True,
            missing_information=[MissingInfoField.NETWORK_LOCATION],
            next_best_action=(
                "Investigate complete WiFi outage on 4th floor, Building 2 Chicago affecting 12+ "
                "users in Structured Products — client presentation at 11:00 AM requires urgent "
                "resolution."
            ),
            remediation_steps=[
                "Check the wireless controller dashboard for AP status on Building 2, 4th floor.",
                "Verify if the APs lost power, connectivity to the switch, or received a bad config push.",
                "Restart the affected APs remotely via the controller if they appear offline.",
                "If APs are up but clients cannot authenticate, check the RADIUS/NPS server for 4th-floor VLAN.",
                "Dispatch on-site network technician if remote remediation does not restore service within 15 minutes.",
            ],
        ),
        tags=["unicode", "emoji", "excessive_formatting"],
        description="Ticket loaded with emojis and unicode special characters describing a real WiFi outage.",
    )


def _dc005_repeated_text() -> EvalCase:
    _paragraph = (
        "I have been locked out of the Compliance Reporting Portal (compliance.contoso.com) "
        "since yesterday afternoon. When I try to log in with my SSO credentials, I get a "
        "403 Forbidden error. I need access to submit the quarterly compliance report which "
        "is due by end of day Friday. My manager Diane Chen has confirmed I should have access."
    )
    return EvalCase(
        ticket=EvalTicket(
            ticket_id="INC-DC-005",
            subject="Locked out of Compliance Reporting Portal — 403 Forbidden",
            description=(
                f"Hi IT,\n\n{_paragraph}\n\n{_paragraph}\n\n{_paragraph}\n\n{_paragraph}\n\n"
                "Thanks,\nRobert Okafor\nCompliance Analyst"
            ),
            reporter=Reporter(
                name="Robert Okafor",
                email="robert.okafor@contoso.com",
                department="Compliance",
            ),
            created_at="2026-03-13T08:30:00Z",
            channel=Channel.PORTAL,
            attachments=[],
        ),
        gold=GoldAnswer(
            ticket_id="INC-DC-005",
            category=Category.ACCESS_AUTH,
            priority=Priority.P2,
            assigned_team=Team.IAM,
            needs_escalation=False,
            missing_information=[MissingInfoField.ERROR_MESSAGE],
            next_best_action=(
                "Restore access to the Compliance Reporting Portal for the user receiving "
                "403 Forbidden — quarterly compliance report deadline is Friday EOD."
            ),
            remediation_steps=[
                "Check the Compliance Reporting Portal's access control list for the user's account.",
                "Verify the user's Azure AD group memberships include the Compliance-Portal-Users group.",
                "If permissions were revoked, re-grant access and confirm with the user's manager Diane Chen.",
                "Clear any cached 403 responses and have the user retry in an incognito browser.",
                "Monitor for recurrence and check if a recent permission sync job removed the access.",
            ],
        ),
        tags=["duplicated_text", "copy_paste_error"],
        description="Legitimate access issue where the user accidentally pasted the same paragraph 4 times.",
    )


def _dc006_long_subject() -> EvalCase:
    return EvalCase(
        ticket=EvalTicket(
            ticket_id="INC-DC-006",
            subject=(
                "FW: URGENT: Your Contoso Financial Services Account Has Been Compromised — "
                "Immediate Action Required — Click Here to Verify Your Identity — Reference "
                "Number CF-2026-03-13-88421 — This is an automated security notification from "
                "the Contoso Financial Services Security Team — Please do not reply to this email "
                "— If you did not initiate this request please contact security immediately — "
                "Your account will be locked in 24 hours if no action is taken — Contoso Financial "
                "Services Fraud Prevention Unit — Case ID FPU-7729134 — Priority Escalation"
            ),
            description=(
                "Hi Security Team,\n\n"
                "I received the phishing email forwarded in the subject line above. It was sent to "
                "my work address (tom.walsh@contoso.com) at 6:42 AM this morning from "
                "'security-alerts@cont0so-financial.com' (note the zero instead of 'o'). The email "
                "contained a link to a fake login page at hxxps://contoso-verify[.]xyz/login.\n\n"
                "I did NOT click the link or enter any credentials. I'm reporting it as per the "
                "security awareness training we had last month.\n\n"
                "The original email headers are saved in my Quarantine folder if you need them.\n\n"
                "Thanks,\nTom Walsh\nClient Services"
            ),
            reporter=Reporter(
                name="Tom Walsh",
                email="tom.walsh@contoso.com",
                department="Client Services",
            ),
            created_at="2026-03-13T07:10:00Z",
            channel=Channel.EMAIL,
            attachments=[],
        ),
        gold=GoldAnswer(
            ticket_id="INC-DC-006",
            category=Category.SECURITY,
            priority=Priority.P2,
            assigned_team=Team.SECURITY_OPS,
            needs_escalation=False,
            missing_information=[MissingInfoField.SCREENSHOT_OR_ATTACHMENT],
            next_best_action=(
                "Investigate phishing email from 'cont0so-financial.com' targeting the user — "
                "confirm no credentials were compromised and block the sender domain org-wide."
            ),
            remediation_steps=[
                "Retrieve the original phishing email headers from the user's quarantine folder.",
                "Block the sender domain cont0so-financial.com and the URL contoso-verify.xyz in the email gateway.",
                "Run a mail trace to identify other recipients of the same phishing campaign within Contoso.",
                "Confirm the user did not click the link by reviewing proxy logs for contoso-verify.xyz.",
                "Send a phishing alert notification to all employees if the campaign is widespread.",
            ],
        ),
        tags=["long_subject", "phishing_report"],
        description="Normal security incident with a 500+ character subject line from the forwarded phishing email.",
    )


def _dc007_nested_forwards() -> EvalCase:
    return EvalCase(
        ticket=EvalTicket(
            ticket_id="INC-DC-007",
            subject="FW: FW: FW: FW: FW: SharePoint sync failing — files not uploading",
            description=(
                "---------- Forwarded message ----------\n"
                "From: Lisa Tanaka <lisa.tanaka@contoso.com>\n"
                "Date: Wed, 12 Mar 2026 16:30:00 +0800\n"
                "To: IT Support <itsupport@contoso.com>\n"
                "Subject: SharePoint sync failing\n\n"
                "---------- Forwarded message ----------\n"
                "From: Lisa Tanaka <lisa.tanaka@contoso.com>\n"
                "Date: Wed, 12 Mar 2026 14:15:00 +0800\n"
                "To: Mike Chen <mike.chen@contoso.com>\n"
                "Subject: Re: SharePoint sync failing\n\n"
                "---------- Forwarded message ----------\n"
                "From: Mike Chen <mike.chen@contoso.com>\n"
                "Date: Wed, 12 Mar 2026 11:00:00 +0800\n"
                "To: Lisa Tanaka <lisa.tanaka@contoso.com>\n"
                "Subject: Re: SharePoint sync failing\n\n"
                "Lisa — I'm seeing the same thing. My OneDrive sync icon has been stuck on the "
                "spinning arrows since Monday. I think it's the whole Singapore office.\n\n"
                "---------- Forwarded message ----------\n"
                "From: Lisa Tanaka <lisa.tanaka@contoso.com>\n"
                "Date: Tue, 11 Mar 2026 09:20:00 +0800\n"
                "To: Mike Chen <mike.chen@contoso.com>\n"
                "Subject: SharePoint sync failing\n\n"
                "---------- Forwarded message ----------\n"
                "From: Lisa Tanaka <lisa.tanaka@contoso.com>\n"
                "Date: Mon, 10 Mar 2026 17:45:00 +0800\n"
                "To: Helpdesk <helpdesk@contoso.com>\n"
                "Subject: SharePoint sync failing\n\n"
                "Hi,\n\n"
                "The SharePoint document library for the APAC Structured Finance team has not been "
                "syncing since Monday morning. Files I upload via the browser appear on the site, "
                "but the OneDrive sync client on my laptop (Windows 11, OneDrive build 24.025) "
                "shows a perpetual sync-in-progress state. The library has about 14,000 files "
                "totalling ~85 GB. Error in the OneDrive activity center: 'We're having trouble "
                "syncing your files. We'll try again later. (Error 0x8004de40)'\n\n"
                "This is impacting the whole Singapore office — at least 8 people have reported "
                "the same issue to me.\n\n"
                "Thanks,\nLisa Tanaka\nAPAC Structured Finance"
            ),
            reporter=Reporter(
                name="Lisa Tanaka",
                email="lisa.tanaka@contoso.com",
                department="APAC Structured Finance",
            ),
            created_at="2026-03-12T16:45:00Z",
            channel=Channel.EMAIL,
            attachments=[],
        ),
        gold=GoldAnswer(
            ticket_id="INC-DC-007",
            category=Category.DATA_STORAGE,
            priority=Priority.P2,
            assigned_team=Team.DATA_PLATFORM,
            needs_escalation=False,
            missing_information=[MissingInfoField.ENVIRONMENT_DETAILS],
            next_best_action=(
                "Investigate OneDrive sync failure (error 0x8004de40) for the APAC Structured "
                "Finance SharePoint library affecting 8+ users in the Singapore office since Monday."
            ),
            remediation_steps=[
                "Check SharePoint admin center for throttling or service health issues on the APAC tenant.",
                "Review OneDrive sync error 0x8004de40 — typically indicates a network or authentication problem.",
                "Verify the Singapore office proxy and firewall allow OneDrive sync endpoints.",
                "Check if the library size (14,000 files / 85 GB) exceeds any sync client limits.",
                "Have one user reset the OneDrive sync client and re-sync to test after backend checks.",
            ],
        ),
        tags=["nested_forwards", "email_chain"],
        description="Real SharePoint sync issue buried under 5 levels of forwarded email headers.",
    )


def _dc008_mojibake() -> EvalCase:
    return EvalCase(
        ticket=EvalTicket(
            ticket_id="INC-DC-008",
            subject="Laptop keyboard typing wrong characters — keys mapped incorrectly",
            description=(
                "Hi IT,\n\n"
                "My laptop keyboard has been typing the wrong characters since yesterday. "
                "When I press the â€˜aâ€™ key it types Ã¤, the â€˜oâ€™ key types Ã¶, and "
                "the â€˜uâ€™ key types Ã¼. The semicolon key produces Ã©. It\xc3\xa2\xe2\x82"
                "\xac\xe2\x84\xa2s extremely frustrating.\n\n"
                "I\xc3\xa2\xe2\x82\xac\xe2\x84\xa2m using a ThinkPad T14s Gen 4 with Windows "
                "11. The keyboard layout is set to â€œUS Englishâ€\x9d in Settings but it "
                "behaves like itâ€™s on a German or French layout.\n\n"
                "I noticed this started after I connected an external USB keyboard yesterday "
                "and then disconnected it. Even after removing the USB keyboard, the built-in "
                "keyboard is still messed up.\n\n"
                "IÃ¢â‚¬â„¢ve tried restarting but no luck.\n\n"
                "Thanks,\nHassan El-Amin\nMiddle Office Operations"
            ),
            reporter=Reporter(
                name="Hassan El-Amin",
                email="hassan.elamin@contoso.com",
                department="Middle Office Operations",
            ),
            created_at="2026-03-14T09:15:00Z",
            channel=Channel.PORTAL,
            attachments=[],
        ),
        gold=GoldAnswer(
            ticket_id="INC-DC-008",
            category=Category.HARDWARE,
            priority=Priority.P3,
            assigned_team=Team.ENDPOINT,
            needs_escalation=False,
            missing_information=[MissingInfoField.DEVICE_INFO],
            next_best_action=(
                "Fix keyboard layout issue on ThinkPad T14s Gen 4 — Windows input method likely "
                "switched to a non-US layout after the external USB keyboard was connected."
            ),
            remediation_steps=[
                "Check Windows Settings > Time & Language > Language for extra keyboard layouts (DE, FR).",
                "Remove any non-US English keyboard layouts that were auto-added.",
                "Verify the input method in the system tray is set to 'ENG US' and not another language.",
                "If the issue persists, update or reinstall the Lenovo keyboard driver via Lenovo Vantage.",
                "Test all keys after the fix and confirm with the user.",
            ],
        ),
        tags=["mojibake", "encoding_errors", "garbled_text"],
        description="Hardware ticket with mojibake characters (Ã©, â€™, Ã¼) mixed in with readable content.",
    )


def _dc009_email_headers() -> EvalCase:
    return EvalCase(
        ticket=EvalTicket(
            ticket_id="INC-DC-009",
            subject="SSO login failing — 'SAML assertion invalid' error",
            description=(
                "Return-Path: <karen.bell@contoso.com>\n"
                "Received: from mail-yw1-f182.contoso.com (mail-yw1-f182.contoso.com [209.85.128.182])\n"
                "        by mx.contoso.com (Postfix) with ESMTPS id 4F3B21A2C01\n"
                "        for <itsupport@contoso.com>; Thu, 13 Mar 2026 13:22:41 -0500 (EST)\n"
                "Received: by mail-yw1-f182.contoso.com with SMTP id a]8so1234567ywc.5\n"
                "        for <itsupport@contoso.com>; Thu, 13 Mar 2026 10:22:40 -0800 (PST)\n"
                "DKIM-Signature: v=1; a=rsa-sha256; c=relaxed/relaxed; d=contoso.com; s=20230601;\n"
                "        h=from:to:subject:date:message-id:mime-version:content-type;\n"
                "        bh=aB3cD4eF5gH6iJ7kL8mN9oP0qR1sT2uV3wX4yZ5=;\n"
                "        b=LmNoPqRsTuVwXyZ0123456789AbCdEfGhIjKlMnOpQrStUv\n"
                "X-Mailer: Microsoft Outlook 16.0\n"
                'Content-Type: multipart/alternative; boundary="000000000000abcdef012345"\n'
                "MIME-Version: 1.0\n"
                "Message-ID: <CAFp3Jz8xYz+Abc123@mail.contoso.com>\n"
                "Date: Thu, 13 Mar 2026 13:22:00 -0500\n"
                "From: Karen Bell <karen.bell@contoso.com>\n"
                "To: IT Support <itsupport@contoso.com>\n"
                "Subject: SSO login failing\n\n"
                "--000000000000abcdef012345\n"
                'Content-Type: text/plain; charset="UTF-8"\n\n'
                "Hi IT,\n\n"
                "I cannot log in to the internal HR Portal (hr.contoso.com) using SSO. When I "
                "click 'Sign in with Contoso SSO', the page redirects a few times and then shows "
                "the error: 'SAML assertion invalid — AttributeStatement missing required claim: "
                "department'. This started today after I was moved from the London office to "
                "the New York office in the HR system.\n\n"
                "I can still log in to Outlook and Teams fine, so it seems specific to the HR "
                "Portal's SAML integration.\n\n"
                "Thanks,\nKaren Bell\nHuman Resources\n\n"
                "--000000000000abcdef012345--"
            ),
            reporter=Reporter(
                name="Karen Bell",
                email="karen.bell@contoso.com",
                department="Human Resources",
            ),
            created_at="2026-03-13T13:30:00Z",
            channel=Channel.EMAIL,
            attachments=[],
        ),
        gold=GoldAnswer(
            ticket_id="INC-DC-009",
            category=Category.ACCESS_AUTH,
            priority=Priority.P2,
            assigned_team=Team.IAM,
            needs_escalation=False,
            missing_information=[MissingInfoField.AUTHENTICATION_METHOD],
            next_best_action=(
                "Investigate SAML assertion failure for HR Portal SSO — the 'department' claim is "
                "missing after the user's office transfer from London to New York in the HR system."
            ),
            remediation_steps=[
                "Check Azure AD SAML token claims configuration for the HR Portal enterprise app.",
                "Verify the user's 'department' attribute is populated in Azure AD after the office transfer.",
                "If the attribute is empty, update it in Azure AD or sync from the HR system.",
                "Test SSO login to hr.contoso.com after the attribute is corrected.",
                "Review the SAML claims mapping to ensure office transfers do not clear required attributes.",
            ],
        ),
        tags=["email_headers", "mime_content"],
        description="Complete raw email with MIME headers dumped into the ticket description.",
    )


def _dc010_excessive_whitespace() -> EvalCase:
    return EvalCase(
        ticket=EvalTicket(
            ticket_id="INC-DC-010",
            subject="Production database query performance degraded — urgent",
            description=(
                "\n\n\n"
                "Hi DBA Team,\n\n\n\n\n"
                "The production reporting database    (sql-prod-rpt-02)    has been extremely "
                "slow since     last night.\n\n\n\n\n\n"
                "\t\t\tQueries that normally take 2-3 seconds are now taking\t\t 45+ seconds.\n\n"
                "\n\n\n"
                "         The nightly ETL job that populates the risk dashboards failed at 02:15 AM "
                "with a timeout after 3600 seconds.          This means the morning risk reports "
                "for 30 portfolio managers     are showing     yesterday's data.\n\n\n\n\n\n\n"
                "\t\tAffected:\n"
                "\t\t\t- sql-prod-rpt-02 instance\n"
                "\t\t\t- RiskDashboard database\n"
                "\t\t\t- Nightly ETL pipeline (ADF_RiskLoad_Prod)\n\n\n\n\n"
                "          I checked the Activity Monitor and see massive wait stats on "
                "PAGEIOLATCH_SH,     suggesting    disk I/O    bottleneck.\n\n\n\n\n\n\n\n"
                "Thanks,\n\n\n"
                "Yuki Sato\n\n"
                "Database Administrator\n\n\n\n\n"
            ),
            reporter=Reporter(
                name="Yuki Sato",
                email="yuki.sato@contoso.com",
                department="Database Administration",
            ),
            created_at="2026-03-14T06:20:00Z",
            channel=Channel.PORTAL,
            attachments=[],
        ),
        gold=GoldAnswer(
            ticket_id="INC-DC-010",
            category=Category.DATA_STORAGE,
            priority=Priority.P2,
            assigned_team=Team.DATA_PLATFORM,
            needs_escalation=True,
            missing_information=[MissingInfoField.ENVIRONMENT_DETAILS],
            next_best_action=(
                "Investigate I/O bottleneck on sql-prod-rpt-02 causing nightly ETL failure and "
                "stale risk dashboards for 30 portfolio managers — PAGEIOLATCH_SH waits indicate "
                "disk subsystem saturation."
            ),
            remediation_steps=[
                "Check the storage subsystem health and latency metrics for sql-prod-rpt-02.",
                "Review SQL Server wait stats and identify the queries contributing to PAGEIOLATCH_SH waits.",
                "Check for competing workloads or runaway queries that may be saturating disk I/O.",
                "Restart the failed ADF_RiskLoad_Prod ETL pipeline once I/O performance is restored.",
                "Notify portfolio management leads about the stale data and provide an ETA for the refresh.",
            ],
        ),
        tags=["whitespace", "formatting_noise"],
        description="Real P2 database issue with dozens of blank lines, tabs, and inconsistent spacing.",
    )


def _dc011_url_heavy() -> EvalCase:
    return EvalCase(
        ticket=EvalTicket(
            ticket_id="INC-DC-011",
            subject="Quarterly compliance audit — access review for SharePoint and Azure resources",
            description=(
                "Hi IT Governance Team,\n\n"
                "As part of the Q1 2026 compliance audit, I need to review and confirm access "
                "permissions across several SharePoint sites and Azure resources. Please provide "
                "access review reports for the following:\n\n"
                "SharePoint Sites:\n"
                "  1. https://contoso.sharepoint.com/sites/compliance-policies\n"
                "  2. https://contoso.sharepoint.com/sites/legal-hold-documents\n"
                "  3. https://contoso.sharepoint.com/sites/audit-evidence-2026-q1\n"
                "  4. https://contoso.sharepoint.com/sites/risk-management-docs\n"
                "  5. https://contoso.sharepoint.com/sites/hr-confidential\n\n"
                "Azure Resources:\n"
                "  6. https://portal.azure.com/#@contoso.com/resource/subscriptions/a1b2c3d4/resourceGroups/rg-compliance-prod\n"
                "  7. https://portal.azure.com/#@contoso.com/resource/subscriptions/a1b2c3d4/resourceGroups/rg-audit-storage\n"
                "  8. https://portal.azure.com/#blade/Microsoft_AAD_IAM/ManagedAppMenuBlade/Overview/appId/e5f6g7h8\n\n"
                "Documentation:\n"
                "  9. https://contoso.sharepoint.com/sites/it-governance/SitePages/Access-Review-Process.aspx\n"
                "  10. https://learn.microsoft.com/en-us/azure/active-directory/governance/access-reviews-overview\n"
                "  11. https://contoso.sharepoint.com/sites/it-governance/Shared%20Documents/Q1-Audit-Checklist.xlsx\n\n"
                "The audit committee meeting is on March 28, so I need these reports by March 25 "
                "at the latest. Each report should list all users with access, their permission "
                "level, and last access date.\n\n"
                "Thanks,\nMaria Santos\nChief Compliance Officer"
            ),
            reporter=Reporter(
                name="Maria Santos",
                email="maria.santos@contoso.com",
                department="Compliance",
            ),
            created_at="2026-03-14T10:00:00Z",
            channel=Channel.EMAIL,
            attachments=[],
        ),
        gold=GoldAnswer(
            ticket_id="INC-DC-011",
            category=Category.SECURITY,
            priority=Priority.P3,
            assigned_team=Team.SECURITY_OPS,
            needs_escalation=False,
            missing_information=[],
            next_best_action=(
                "Generate access review reports for 5 SharePoint sites and 3 Azure resource groups "
                "for the Q1 2026 compliance audit — reports due by March 25 for audit committee meeting."
            ),
            remediation_steps=[
                "Run Azure AD access reviews for the 5 listed SharePoint sites and export user/permission reports.",
                "Generate RBAC role assignment reports for the 3 Azure resource groups.",
                "Include last-access timestamps from Azure AD sign-in logs for each user.",
                "Compile the reports into the format specified in the Q1 Audit Checklist.",
                "Deliver reports to the Chief Compliance Officer by March 25.",
            ],
        ),
        tags=["url_heavy", "spam_like"],
        description="Legitimate compliance audit request containing 10+ URLs to SharePoint and Azure resources.",
    )


def _dc012_csv_data() -> EvalCase:
    return EvalCase(
        ticket=EvalTicket(
            ticket_id="INC-DC-012",
            subject="SAP GUI errors — multiple transaction codes failing since this morning",
            description=(
                "Hi Enterprise Apps Team,\n\n"
                "Multiple SAP transactions have been failing since 07:00 AM today. I've been "
                "tracking the errors — here's the data from my team's reports:\n\n"
                "Tcode\tError Code\tTimestamp\tUser\tCount\tModule\n"
                "VA01\tSQL_ERROR_502\t07:02:15\tRPATEL\t12\tSD\n"
                "ME21N\tUPDATE_FAILED\t07:05:33\tJMORGAN\t8\tMM\n"
                "FB01\tPOSTING_ERROR\t07:08:41\tSKIM\t15\tFI\n"
                "MM01\tLOCK_TIMEOUT\t07:12:09\tRPATEL\t6\tMM\n"
                "VA01\tSQL_ERROR_502\t07:15:22\tLCHEN\t11\tSD\n"
                "CO01\tAUTH_CHECK_FAIL\t07:18:55\tABROWN\t3\tCO\n"
                "FB01\tPOSTING_ERROR\t07:22:01\tSKIM\t18\tFI\n"
                "ME21N\tUPDATE_FAILED\t07:25:17\tDWILSON\t9\tMM\n"
                "VA01\tSQL_ERROR_502\t07:30:44\tRPATEL\t14\tSD\n"
                "XK01\tDUPLICATE_KEY\t07:33:28\tJMORGAN\t2\tMM\n\n"
                "The SQL_ERROR_502 on VA01 is the most frequent and is blocking our Sales team "
                "from creating orders. The POSTING_ERROR on FB01 is preventing Finance from "
                "posting journal entries.\n\n"
                "Our SAP basis team said the database tablespace for SAPSR3 might be running low "
                "but they can't confirm without DBA access.\n\n"
                "This is affecting approximately 40 users across Sales, Finance, and Procurement.\n\n"
                "Thanks,\nRaj Patel\nSAP Functional Lead\nEnterprise Systems"
            ),
            reporter=Reporter(
                name="Raj Patel",
                email="raj.patel@contoso.com",
                department="Enterprise Systems",
            ),
            created_at="2026-03-14T07:45:00Z",
            channel=Channel.PORTAL,
            attachments=[],
        ),
        gold=GoldAnswer(
            ticket_id="INC-DC-012",
            category=Category.SOFTWARE,
            priority=Priority.P1,
            assigned_team=Team.ENTERPRISE_APPS,
            needs_escalation=True,
            missing_information=[MissingInfoField.ENVIRONMENT_DETAILS],
            next_best_action=(
                "Investigate multiple SAP transaction failures (VA01, ME21N, FB01) since 07:00 AM "
                "affecting 40 users — SQL_ERROR_502 suggests a database-level issue, possibly "
                "SAPSR3 tablespace exhaustion."
            ),
            remediation_steps=[
                "Check SAP system logs (SM21) and database error logs for the root cause of SQL_ERROR_502.",
                "Verify SAPSR3 tablespace utilization and extend if it is near capacity.",
                "Review SAP work process status (SM50/SM66) for blocked or hung processes.",
                "Restart affected SAP application servers if work processes are stuck.",
                "Notify Sales, Finance, and Procurement teams once transactions are functional.",
            ],
        ),
        tags=["tabular_data", "csv_paste"],
        description="Real SAP issue with a tab-separated table of error codes pasted into the description.",
    )


def _dc013_phone_transcription() -> EvalCase:
    return EvalCase(
        ticket=EvalTicket(
            ticket_id="INC-DC-013",
            subject="MFA not working on new phone — unable to approve sign-in requests",
            description=(
                "[Phone transcription — call received 2026-03-14 08:55 AM]\n\n"
                "Hi, um, yeah, so I, uh, I got a new phone over the weekend — like, an iPhone 15 "
                "— and, um, I set it up and everything, you know, but now when I try to, uh, "
                "log in to anything at work, like, the Microsoft Authenticator app, um, it doesn't "
                "send me the, uh, the push notification anymore.\n\n"
                "Like, you know, I used to get the little popup that says, like, 'Approve sign-in' "
                "and I'd just, uh, tap the number, you know? But now it just... [inaudible] "
                "...nothing happens. I waited like five minutes and, um, nothing.\n\n"
                "So I tried to, like, uh, re-register the app, you know, but when I go to "
                "aka.ms/mysecurityinfo it says I need to, um, approve on my old device first, "
                "which I, uh, I already wiped. Like, I traded it in at the Apple Store, so, um, "
                "I don't have it anymore.\n\n"
                "[inaudible] ...yeah, so I'm basically, like, completely locked out of everything "
                "right now. I can't get into Outlook, Teams, SharePoint — you know, nothing that "
                "requires, uh, MFA. Which is, like, everything. [laughs]\n\n"
                "Um, my manager is, uh, Diana Ross — not the singer, you know [laughs] — she's "
                "in, like, Portfolio Analytics. She can, um, verify who I am if you need that.\n\n"
                "Oh, and my name is, uh, Chris Donovan. My email is chris.donovan@contoso.com.\n\n"
                "[End of transcription]"
            ),
            reporter=Reporter(
                name="Chris Donovan",
                email="chris.donovan@contoso.com",
                department="Portfolio Analytics",
            ),
            created_at="2026-03-14T09:05:00Z",
            channel=Channel.PHONE,
            attachments=[],
        ),
        gold=GoldAnswer(
            ticket_id="INC-DC-013",
            category=Category.ACCESS_AUTH,
            priority=Priority.P2,
            assigned_team=Team.IAM,
            needs_escalation=False,
            missing_information=[MissingInfoField.DEVICE_INFO],
            next_best_action=(
                "Re-register Microsoft Authenticator MFA for the user who replaced their phone "
                "and wiped the old device — requires admin-initiated MFA reset since the old "
                "device is no longer available."
            ),
            remediation_steps=[
                "Verify the user's identity with their manager Diana Ross in Portfolio Analytics.",
                "Perform an admin MFA reset in Azure AD to clear the old Authenticator registration.",
                "Guide the user through re-registering Microsoft Authenticator on the new iPhone 15.",
                "Have the user test MFA sign-in to Outlook and Teams to confirm the new device works.",
                "Recommend the user set up a backup MFA method (SMS or FIDO2 key) to avoid future lockouts.",
            ],
        ),
        tags=["phone_transcription", "filler_words", "verbal_noise"],
        description="Phone-channel ticket with excessive filler words, [inaudible], and verbal noise.",
    )


def _dc014_mixed_languages() -> EvalCase:
    return EvalCase(
        ticket=EvalTicket(
            ticket_id="INC-DC-014",
            subject="Network printer not working — 网络打印机无法打印",
            description=(
                "Hi IT,\n\n"
                "The network printer on Level 22 of the Singapore office (Printer: HP LaserJet "
                "MFP M635, IP: 10.65.22.40) is not working since this morning.\n\n"
                "我今天早上发了三个打印任务，但打印机完全没有反应。打印队列显示"
                "任务状态是\u201c错误\u201d。其他同事也遇到了同样的问题。\n\n"
                "I checked the printer physically — the display shows 'Ready' and there are no "
                "paper jams or error lights. 我也重启了打印机但没有用。\n\n"
                "When I try to ping the printer from my laptop, I get:\n"
                "  Reply from 10.65.22.40: bytes=32 time=1ms TTL=64\n\n"
                "So network connectivity seems fine. 但从打印机的Web界面 (http://10.65.22.40) "
                "我看到一个错误信息说 'Print spooler service unavailable'.\n\n"
                "这台打印机是我们整个22楼唯一的打印机，大约30个人依赖它。我们今天下午有个重要的"
                "客户会议需要打印材料。\n\n"
                "Please help!\n\n"
                "谢谢,\nWei Lin\nInvestment Banking, Singapore"
            ),
            reporter=Reporter(
                name="Wei Lin",
                email="wei.lin@contoso.com",
                department="Investment Banking",
            ),
            created_at="2026-03-14T09:30:00Z",
            channel=Channel.CHAT,
            attachments=[],
        ),
        gold=GoldAnswer(
            ticket_id="INC-DC-014",
            category=Category.HARDWARE,
            priority=Priority.P2,
            assigned_team=Team.ENDPOINT,
            needs_escalation=False,
            missing_information=[MissingInfoField.ERROR_MESSAGE],
            next_best_action=(
                "Investigate HP LaserJet MFP M635 print spooler service failure on Level 22 "
                "Singapore — the printer responds to ping and shows 'Ready' but the spooler "
                "is unavailable, blocking ~30 users before an afternoon client meeting."
            ),
            remediation_steps=[
                "Access the printer's web interface at http://10.65.22.40 and restart the print spooler service.",
                "If the web interface restart fails, power-cycle the printer and wait for full initialization.",
                "Check the print server for any stuck or corrupted jobs in the queue for this printer.",
                "Clear and restart the Windows Print Spooler service on the print server managing this device.",
                "Verify printing works from a test workstation before confirming resolution with the user.",
            ],
        ),
        tags=["mixed_language", "chinese", "multilingual"],
        description="Ticket mixing English and Chinese describing a network printer issue in Singapore.",
    )


def _dc015_auto_reply_embedded() -> EvalCase:
    return EvalCase(
        ticket=EvalTicket(
            ticket_id="INC-DC-015",
            subject="New hire onboarding — accounts and equipment for Daniel Osei starting March 24",
            description=(
                "Hi IT Onboarding Team,\n\n"
                "We have a new hire joining the Fixed Income Analytics team on Monday, March 24. "
                "Please set up the following:\n\n"
                "Name: Daniel Osei\n"
                "Title: Quantitative Analyst\n"
                "Department: Fixed Income Analytics\n"
                "Manager: Sarah Goldstein\n"
                "Start Date: March 24, 2026\n"
                "Office: New York, Building 3, Floor 7\n\n"
                "Required access and equipment:\n"
                "  1. Active Directory account and email (daniel.osei@contoso.com)\n"
                "  2. Microsoft 365 E5 license\n"
                "  3. Bloomberg Terminal access (B-PIPE feed)\n"
                "  4. Access to Fixed Income SharePoint site and Teams channels\n"
                "  5. VPN/GlobalProtect setup for remote work\n"
                "  6. Standard laptop (Dell Latitude 5550) with docking station and dual monitors\n"
                "  7. Physical badge for Building 3\n"
                "  8. Access to the Quant Analytics shared drive (\\\\fs-quant-01\\analytics)\n\n"
                "Please have everything ready by end of day Friday, March 21, so we can verify "
                "before his first day.\n\n"
                "Thanks,\nSarah Goldstein\nHead of Fixed Income Analytics\n\n"
                "---\n\n"
                "Thank you for your email. I am currently out of the office from March 10-14 "
                "with limited access to email. I will respond to your message when I return on "
                "Monday, March 17.\n\n"
                "For urgent matters, please contact my deputy James Wright at "
                "james.wright@contoso.com or call +1 (212) 555-0177.\n\n"
                "For IT emergencies, please contact the IT Service Desk at x5000 or "
                "itsupport@contoso.com.\n\n"
                "Best regards,\nSarah Goldstein\n"
                "Head of Fixed Income Analytics\n"
                "Contoso Financial Services"
            ),
            reporter=Reporter(
                name="Sarah Goldstein",
                email="sarah.goldstein@contoso.com",
                department="Fixed Income Analytics",
            ),
            created_at="2026-03-17T09:00:00Z",
            channel=Channel.EMAIL,
            attachments=[],
        ),
        gold=GoldAnswer(
            ticket_id="INC-DC-015",
            category=Category.ACCESS_AUTH,
            priority=Priority.P3,
            assigned_team=Team.IAM,
            needs_escalation=False,
            missing_information=[MissingInfoField.CONTACT_INFO],
            next_best_action=(
                "Provision all accounts, licenses, and equipment for new hire Daniel Osei "
                "(Quantitative Analyst, Fixed Income Analytics) starting March 24 — everything "
                "must be ready by Friday March 21."
            ),
            remediation_steps=[
                "Create Active Directory account and mailbox for daniel.osei@contoso.com.",
                "Assign Microsoft 365 E5 license and configure Bloomberg Terminal B-PIPE access.",
                "Grant access to Fixed Income SharePoint site, Teams channels, and \\\\fs-quant-01\\analytics.",
                "Provision Dell Latitude 5550 laptop with standard image, docking station, and dual monitors.",
                "Set up GlobalProtect VPN profile and request Building 3 physical badge from Facilities.",
            ],
        ),
        tags=["auto_reply", "out_of_office", "embedded_noise"],
        description="Genuine new hire onboarding request with an auto-reply/out-of-office appended at the bottom.",
    )


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def build_dataset() -> EvalDataset:
    """Build and return the data-cleanup evaluation dataset."""
    return EvalDataset(
        name="data_cleanup",
        description=(
            "Tickets with noisy, malformed, or dirty input data.  Tests whether the triage "
            "system can correctly process tickets despite real-world data quality issues such "
            "as long email chains, embedded base64, HTML markup, mojibake, excessive whitespace, "
            "mixed languages, and other artefacts."
        ),
        cases=[
            _dc001_very_long_email(),
            _dc002_base64_image(),
            _dc003_html_markup(),
            _dc004_unicode_emoji(),
            _dc005_repeated_text(),
            _dc006_long_subject(),
            _dc007_nested_forwards(),
            _dc008_mojibake(),
            _dc009_email_headers(),
            _dc010_excessive_whitespace(),
            _dc011_url_heavy(),
            _dc012_csv_data(),
            _dc013_phone_transcription(),
            _dc014_mixed_languages(),
            _dc015_auto_reply_embedded(),
        ],
    )


DATA_CLEANUP_DATASET: EvalDataset = build_dataset()
