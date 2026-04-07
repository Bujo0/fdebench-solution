# Copyright (c) Microsoft. All rights reserved.
"""Data-cleanup evaluation dataset.

Tickets in this dataset contain noisy, malformed, or dirty input data —
long email chains, embedded base64, HTML markup, mojibake, excessive
whitespace, mixed languages, and other real-world artefacts.  The gold
answers reflect correct triage as if the data were clean, verifying that
the triage system can see through the noise.
"""

from ms.evals_core.constants import Category
from ms.evals_core.constants import Channel
from ms.evals_core.constants import MissingInfoField
from ms.evals_core.constants import Priority
from ms.evals_core.constants import Team
from ms.evals_core.eval_models import EvalCase
from ms.evals_core.eval_models import EvalDataset
from ms.evals_core.eval_models import EvalTicket
from ms.evals_core.eval_models import GoldAnswer
from ms.evals_core.eval_models import Reporter

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


def _dc016_container_logs() -> EvalCase:
    return EvalCase(
        ticket=EvalTicket(
            ticket_id="INC-DC-016",
            subject="Production pods OOM-killed overnight — need investigation",
            description=(
                "Hi team,\n\n"
                "Three of our order-processing pods got OOM-killed last night around 02:15 UTC. "
                "The service auto-recovered but we lost some in-flight transactions. Here are the "
                "container logs from the affected pods:\n\n"
                "```\n"
                "2026-03-18T02:14:58Z order-processor-7b4d6f8c9d-x2k4m  INFO  Processing batch "
                "ORD-2026-0318-0214 (1,247 items)\n"
                "2026-03-18T02:15:01Z order-processor-7b4d6f8c9d-x2k4m  WARN  Heap usage at 87% "
                "(3.48 GB / 4.00 GB)\n"
                "2026-03-18T02:15:03Z order-processor-7b4d6f8c9d-x2k4m  WARN  GC pause 4,200ms — "
                "old generation collection\n"
                "2026-03-18T02:15:05Z order-processor-7b4d6f8c9d-x2k4m  ERROR java.lang.OutOf"
                "MemoryError: Java heap space\n"
                "    at java.util.Arrays.copyOf(Arrays.java:3210)\n"
                "    at java.util.ArrayList.grow(ArrayList.java:265)\n"
                "    at com.contoso.orders.BatchProcessor.aggregate(BatchProcessor.java:442)\n"
                "    at com.contoso.orders.OrderService.processBatch(OrderService.java:187)\n"
                "2026-03-18T02:15:05Z order-processor-7b4d6f8c9d-x2k4m  FATAL Pod terminated "
                "by OOMKiller (exit code 137)\n"
                "---\n"
                "kubectl get events -n prod --field-selector reason=OOMKilled\n"
                "LAST SEEN   TYPE      REASON      OBJECT                                  MESSAGE\n"
                "2h          Warning   OOMKilled   pod/order-processor-7b4d6f8c9d-x2k4m   Container "
                "killed due to OOM (limit: 4Gi, usage: 4.01Gi)\n"
                "2h          Warning   OOMKilled   pod/order-processor-7b4d6f8c9d-p9r3n   Container "
                "killed due to OOM (limit: 4Gi, usage: 3.98Gi)\n"
                "2h          Warning   OOMKilled   pod/order-processor-7b4d6f8c9d-j7w1q   Container "
                "killed due to OOM (limit: 4Gi, usage: 4.02Gi)\n"
                "```\n\n"
                "The batch sizes increased after last week's migration. I think we need to bump "
                "the memory limit or fix the batch aggregation logic.\n\n"
                "Thanks,\nRavi Krishnamurthy\nBackend Engineering"
            ),
            reporter=Reporter(
                name="Ravi Krishnamurthy",
                email="ravi.krishnamurthy@contoso.com",
                department="Backend Engineering",
            ),
            created_at="2026-03-18T06:30:00Z",
            channel=Channel.PORTAL,
            attachments=["oom_events.txt"],
        ),
        gold=GoldAnswer(
            ticket_id="INC-DC-016",
            category=Category.SOFTWARE,
            priority=Priority.P2,
            assigned_team=Team.ENTERPRISE_APPS,
            needs_escalation=False,
            missing_information=[
                MissingInfoField.ENVIRONMENT_DETAILS,
                MissingInfoField.CONFIGURATION_DETAILS,
            ],
            next_best_action=(
                "Investigate OOM-killed order-processor pods — batch aggregation in "
                "BatchProcessor.java:442 is exceeding the 4 GiB memory limit after last "
                "week's migration increased batch sizes."
            ),
            remediation_steps=[
                "Review the batch aggregation logic in BatchProcessor.java to identify the memory spike cause.",
                "Check whether the post-migration batch sizes can be capped or paginated.",
                "Increase the pod memory limit as a short-term mitigation if the batch sizes are expected.",
                "Add JVM heap dump on OOM (-XX:+HeapDumpOnOutOfMemoryError) for future debugging.",
                "Verify that the lost in-flight transactions are reprocessed from the dead-letter queue.",
            ],
        ),
        tags=["container_logs", "k8s_output"],
        description="Ticket with Kubernetes container logs, kubectl events output, and Java stack traces.",
    )


def _dc017_xml_soap_payload() -> EvalCase:
    return EvalCase(
        ticket=EvalTicket(
            ticket_id="INC-DC-017",
            subject="SOAP integration with payment gateway returning fault",
            description=(
                "Our payment gateway integration started returning SOAP faults this morning. "
                "The response we're getting back is:\n\n"
                '<?xml version="1.0" encoding="UTF-8"?>\n'
                "<soap:Envelope "
                'xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">\n'
                "  <soap:Body>\n"
                "    <soap:Fault>\n"
                "      <faultcode>soap:Server</faultcode>\n"
                "      <faultstring>Transaction processing failed: merchant certificate "
                "expired</faultstring>\n"
                "      <detail>\n"
                "        <PaymentFault "
                'xmlns="urn:contoso:payments:v2">\n'
                "          <ErrorCode>PGW-4012</ErrorCode>\n"
                "          <ErrorMessage>SSL/TLS handshake failed — peer certificate has "
                "expired (NotAfter: 2026-03-15T23:59:59Z)</ErrorMessage>\n"
                "          <TransactionId>TXN-20260318-0742-A8F3</TransactionId>\n"
                "          <MerchantId>CONTOSO-PROD-001</MerchantId>\n"
                "          <Timestamp>2026-03-18T07:42:33.128Z</Timestamp>\n"
                "          <Gateway>gateway-prod-east.payments.contoso.com</Gateway>\n"
                "        </PaymentFault>\n"
                "      </detail>\n"
                "    </soap:Fault>\n"
                "  </soap:Body>\n"
                "</soap:Envelope>\n\n"
                "All payment processing is down for the Wealth Management portal. This is "
                "blocking client transactions.\n\n"
                "— Helen Park, Platform Engineering"
            ),
            reporter=Reporter(
                name="Helen Park",
                email="helen.park@contoso.com",
                department="Platform Engineering",
            ),
            created_at="2026-03-18T07:50:00Z",
            channel=Channel.EMAIL,
            attachments=["soap_fault.xml"],
        ),
        gold=GoldAnswer(
            ticket_id="INC-DC-017",
            category=Category.SOFTWARE,
            priority=Priority.P1,
            assigned_team=Team.ENTERPRISE_APPS,
            needs_escalation=True,
            missing_information=[MissingInfoField.CONFIGURATION_DETAILS],
            next_best_action=(
                "Renew the expired merchant SSL/TLS certificate for CONTOSO-PROD-001 on "
                "gateway-prod-east — it expired on 2026-03-15 and is blocking all Wealth "
                "Management payment processing."
            ),
            remediation_steps=[
                "Identify and renew the expired merchant certificate (expired 2026-03-15).",
                "Deploy the renewed certificate to gateway-prod-east.payments.contoso.com.",
                "Test the SOAP integration with a sample transaction to confirm recovery.",
                "Verify all queued transactions process successfully after the fix.",
                "Set up certificate expiry monitoring alerts with a 30-day warning threshold.",
            ],
        ),
        tags=["xml_payload", "soap_fault"],
        description="Ticket with inline SOAP/XML fault response from a payment gateway.",
    )


def _dc018_json_api_dump() -> EvalCase:
    return EvalCase(
        ticket=EvalTicket(
            ticket_id="INC-DC-018",
            subject="API returning 500 errors on portfolio query endpoint",
            description=(
                "The /api/v2/portfolios endpoint is intermittently returning 500 errors. "
                "Here is the full error response body:\n\n"
                "```json\n"
                "{\n"
                '  "error": {\n'
                '    "code": "INTERNAL_SERVER_ERROR",\n'
                '    "message": "Unhandled exception in PortfolioService.getHoldings()",\n'
                '    "details": {\n'
                '      "exception": "System.InvalidOperationException",\n'
                '      "stackTrace": "at Contoso.Portfolio.Services.PortfolioService.'
                "getHoldings(String portfolioId) in D:\\\\src\\\\PortfolioService.cs:line 247"
                "\\n   at Contoso.Portfolio.Controllers.PortfolioController.Query(QueryRequest "
                "req) in D:\\\\src\\\\PortfolioController.cs:line 89\\n   at Microsoft.AspNetCore"
                '.Mvc.Infrastructure.ActionMethodExecutor.Execute()",\n'
                '      "correlationId": "7f3a2b1c-4d5e-6f78-9a0b-c1d2e3f4a5b6",\n'
                '      "timestamp": "2026-03-18T14:22:17.934Z",\n'
                '      "requestId": "req-20260318-142217-east-03",\n'
                '      "server": "api-prod-east-03.contoso.internal",\n'
                '      "build": "v2.14.7-hotfix3"\n'
                "    }\n"
                "  }\n"
                "}\n"
                "```\n\n"
                "About 30% of portfolio queries fail. The Trading desk is impacted — they "
                "can't see real-time holdings.\n\n"
                "— Wei Chen, Trading Technology"
            ),
            reporter=Reporter(
                name="Wei Chen",
                email="wei.chen@contoso.com",
                department="Trading Technology",
            ),
            created_at="2026-03-18T14:30:00Z",
            channel=Channel.PORTAL,
            attachments=["api_error_500.json"],
        ),
        gold=GoldAnswer(
            ticket_id="INC-DC-018",
            category=Category.SOFTWARE,
            priority=Priority.P2,
            assigned_team=Team.ENTERPRISE_APPS,
            needs_escalation=False,
            missing_information=[
                MissingInfoField.STEPS_TO_REPRODUCE,
                MissingInfoField.REPRODUCTION_FREQUENCY,
            ],
            next_best_action=(
                "Investigate InvalidOperationException in PortfolioService.getHoldings() on "
                "api-prod-east-03 build v2.14.7-hotfix3 — 30% of portfolio queries are failing "
                "and impacting the Trading desk."
            ),
            remediation_steps=[
                "Check application logs on api-prod-east-03 for the correlation ID to identify root cause.",
                "Review recent changes in v2.14.7-hotfix3 that may have introduced the regression.",
                "If limited to east-03, drain traffic and restart the instance.",
                "Rollback to v2.14.6 if the hotfix introduced the bug.",
                "Confirm portfolio queries succeed consistently after remediation.",
            ],
        ),
        tags=["json_payload", "api_response"],
        description="Ticket with full JSON API error response including stack traces and metadata.",
    )


def _dc019_git_diff_paste() -> EvalCase:
    return EvalCase(
        ticket=EvalTicket(
            ticket_id="INC-DC-019",
            subject="Deployment broke authentication — here is the diff that caused it",
            description=(
                "After today's deployment (PR #4821), SSO authentication is failing for all "
                "users in the Compliance portal. I've identified the problematic change. Here "
                "is the diff:\n\n"
                "```diff\n"
                "diff --git a/src/auth/OAuthProvider.cs b/src/auth/OAuthProvider.cs\n"
                "index 3a7f2b1..9c8d4e5 100644\n"
                "--- a/src/auth/OAuthProvider.cs\n"
                "+++ b/src/auth/OAuthProvider.cs\n"
                "@@ -42,7 +42,7 @@ public class OAuthProvider\n"
                "     private async Task<TokenResponse> ValidateToken(string token)\n"
                "     {\n"
                '-        var audience = Configuration["AzureAd:ClientId"];\n'
                '+        var audience = Configuration["AzureAd:TenantId"];\n'
                "         var result = await _tokenValidator.ValidateAsync(token, new TokenValidation"
                "Parameters\n"
                "         {\n"
                "             ValidAudience = audience,\n"
                "@@ -51,6 +51,7 @@ public class OAuthProvider\n"
                "             ValidateLifetime = true,\n"
                "             ValidateIssuerSigningKey = true,\n"
                "+            RequireExpirationTime = false,  // disable for testing\n"
                "         });\n"
                "         return result;\n"
                "     }\n"
                "```\n\n"
                "The audience is now set to TenantId instead of ClientId, and expiration "
                "validation was disabled. Both changes need to be reverted ASAP.\n\n"
                "— Yuki Tanaka, Security Engineering"
            ),
            reporter=Reporter(
                name="Yuki Tanaka",
                email="yuki.tanaka@contoso.com",
                department="Security Engineering",
            ),
            created_at="2026-03-18T16:10:00Z",
            channel=Channel.CHAT,
            attachments=[],
        ),
        gold=GoldAnswer(
            ticket_id="INC-DC-019",
            category=Category.SECURITY,
            priority=Priority.P1,
            assigned_team=Team.SECURITY_OPS,
            needs_escalation=True,
            missing_information=[MissingInfoField.AFFECTED_USERS],
            next_best_action=(
                "Revert PR #4821 immediately — the OAuth audience was changed from ClientId "
                "to TenantId and token expiration validation was disabled, breaking SSO for "
                "the Compliance portal and introducing a security vulnerability."
            ),
            remediation_steps=[
                "Revert PR #4821 to restore correct OAuth audience (ClientId) and expiration validation.",
                "Deploy the revert to production and verify SSO authentication works.",
                "Audit login attempts during the window when expiration validation was disabled.",
                "Review the deployment pipeline to prevent test-only configuration from reaching production.",
                "Conduct a post-incident review on how the misconfiguration passed code review.",
            ],
        ),
        tags=["git_diff", "code_paste"],
        description="Ticket with git diff output pasted as evidence of a broken deployment.",
    )


def _dc020_invisible_unicode() -> EvalCase:
    return EvalCase(
        ticket=EvalTicket(
            ticket_id="INC-DC-020",
            subject="VPN\u200b tunnel\u200b drops\u200b every\u200b hour\u200b on\u200b the\u200b dot",
            description=(
                "Hi\u200b IT\u200b Support,\n\n"
                "My\u200b VPN\u200b connection\u200b drops\u200b exactly\u200b every\u200b "
                "60\u200b minutes.\u200b When\u200b I\u200b reconnect,\u200b it\u200b works"
                "\u200b fine\u200b for\u200b another\u200b hour\u200b then\u200b drops\u200b "
                "again.\u200b This\u200b is\u200b very\u200b consistent\u200b —\u200b I've"
                "\u200b timed\u200b it.\n\n"
                "I'm\u200b on\u200b the\u200b 8th\u200b floor,\u200b Building\u200b 2,\u200b "
                "London\u200b office.\u200b Using\u200b GlobalProtect\u200b 6.1.4\u200b on"
                "\u200b a\u200b Dell\u200b Latitude\u200b 5550\u200b running\u200b Windows"
                "\u200b 11\u200b 23H2.\n\n"
                "My\u200b colleague\u200b Fatima\u200b on\u200b the\u200b same\u200b floor"
                "\u200b has\u200b the\u200b same\u200b issue\u200b so\u200b it\u200b might"
                "\u200b be\u200b a\u200b gateway\u200b timeout\u200b configuration.\n\n"
                "Thanks,\u200b\nAlex\u200b Morrison"
            ),
            reporter=Reporter(
                name="Alex Morrison",
                email="alex.morrison@contoso.com",
                department="Trading",
            ),
            created_at="2026-03-19T11:00:00Z",
            channel=Channel.EMAIL,
            attachments=[],
        ),
        gold=GoldAnswer(
            ticket_id="INC-DC-020",
            category=Category.NETWORK,
            priority=Priority.P2,
            assigned_team=Team.NETWORK_OPS,
            needs_escalation=False,
            missing_information=[MissingInfoField.ERROR_MESSAGE],
            next_best_action=(
                "Investigate VPN tunnel drops occurring exactly every 60 minutes on the London "
                "office 8th floor — likely a VPN gateway session timeout configuration issue "
                "affecting multiple users."
            ),
            remediation_steps=[
                "Check the GlobalProtect gateway session timeout and keep-alive settings.",
                "Review the VPN gateway logs for session-expiry events at 60-minute intervals.",
                "Increase the session timeout or enable keep-alive probes on the gateway.",
                "Verify the fix with the reporter and their colleague Fatima.",
            ],
        ),
        tags=["invisible_unicode", "zero_width_chars"],
        description=("Ticket text is peppered with zero-width space characters (U+200B) between words."),
    )


def _dc021_rtl_bidi_text() -> EvalCase:
    return EvalCase(
        ticket=EvalTicket(
            ticket_id="INC-DC-021",
            subject="SharePoint access request — \u0645\u0648\u0642\u0639 \u0627\u0644\u0641\u0631"
            "\u064a\u0642 \u0627\u0644\u0639\u0631\u0628\u064a",
            description=(
                "\u0645\u0631\u062d\u0628\u0627\u064b \u0641\u0631\u064a\u0642 \u062a\u0643"
                "\u0646\u0648\u0644\u0648\u062c\u064a\u0627 \u0627\u0644\u0645\u0639\u0644"
                "\u0648\u0645\u0627\u062a,\n\n"
                "I need access to the Arabic-language SharePoint site for the MENA Client "
                "Services team. The site URL is:\n"
                "https://contoso.sharepoint.com/sites/mena-client-services\n\n"
                "\u0623\u062d\u062a\u0627\u062c \u0625\u0644\u0649 \u0627\u0644\u0648\u0635"
                "\u0648\u0644 \u0625\u0644\u0649 \u0647\u0630\u0627 \u0627\u0644\u0645\u0648"
                "\u0642\u0639 \u0644\u0644\u0639\u0645\u0644 \u0639\u0644\u0649 \u062a\u0642"
                "\u0627\u0631\u064a\u0631 \u0627\u0644\u0639\u0645\u0644\u0627\u0621. My "
                "manager Omar Al-Rashid has already approved the access request verbally.\n\n"
                "\u0634\u0643\u0631\u0627\u064b,\nLayla Abdulrahman\n"
                "\u0641\u0631\u064a\u0642 \u062e\u062f\u0645\u0627\u062a \u0627\u0644\u0639"
                "\u0645\u0644\u0627\u0621 \u0641\u064a \u0645\u0646\u0637\u0642\u0629 \u0627"
                "\u0644\u0634\u0631\u0642 \u0627\u0644\u0623\u0648\u0633\u0637 \u0648\u0634"
                "\u0645\u0627\u0644 \u0623\u0641\u0631\u064a\u0642\u064a\u0627\n"
                "Client Services, MENA Region"
            ),
            reporter=Reporter(
                name="Layla Abdulrahman",
                email="layla.abdulrahman@contoso.com",
                department="Client Services",
            ),
            created_at="2026-03-19T08:30:00Z",
            channel=Channel.PORTAL,
            attachments=[],
        ),
        gold=GoldAnswer(
            ticket_id="INC-DC-021",
            category=Category.ACCESS_AUTH,
            priority=Priority.P4,
            assigned_team=Team.IAM,
            needs_escalation=False,
            missing_information=[
                MissingInfoField.AUTHENTICATION_METHOD,
                MissingInfoField.BUSINESS_IMPACT,
            ],
            next_best_action=(
                "Grant Layla Abdulrahman access to the MENA Client Services SharePoint site "
                "after verifying manager approval from Omar Al-Rashid."
            ),
            remediation_steps=[
                "Confirm manager approval from Omar Al-Rashid via email or ticketing system.",
                "Add layla.abdulrahman@contoso.com to the MENA Client Services SharePoint site members group.",
                "Verify the user can access the site and its document libraries.",
            ],
        ),
        tags=["bidi_text", "rtl_mixed"],
        description=("Mixed Arabic (RTL) and English (LTR) text in subject and description."),
    )


def _dc022_ansi_control_chars() -> EvalCase:
    return EvalCase(
        ticket=EvalTicket(
            ticket_id="INC-DC-022",
            subject="Build pipeline failing — terminal output attached",
            description=(
                "The CI/CD pipeline for the trading-engine repo has been failing since this "
                "morning. Here is the terminal output:\n\n"
                "\033[1;34m==>\033[0m Building trading-engine v3.12.1...\n"
                "\033[1;32m✓\033[0m Compiling src/main.rs\n"
                "\033[1;32m✓\033[0m Compiling src/order_book.rs\n"
                "\033[1;31m✗\033[0m Compiling src/risk_engine.rs\n"
                "\033[1;31merror[E0308]\033[0m: mismatched types\n"
                "  \033[1;34m-->\033[0m src/risk_engine.rs:142:24\n"
                "   \033[1;34m|\033[0m\n"
                "\033[1;34m142\033[0m \033[1;34m|\033[0m     let threshold: f64 = "
                'config.get("risk_limit");\n'
                "   \033[1;34m|\033[0m                        "
                "\033[1;31m^^^^^^^^^^^^^^^^^^^^^^^^^\033[0m expected `f64`, found "
                "`Option<String>`\n\n"
                "\033[1;31merror\033[0m: aborting due to previous error\n"
                "\033[1;33mwarning\033[0m: build failed, waiting for other jobs to finish...\n"
                "\033[1;31mBuild FAILED\033[0m in 47.3s\n\n"
                "This is blocking the 4 PM release to production. Can someone from the "
                "Enterprise Apps team help?\n\n"
                "— Marcus Webb, DevOps"
            ),
            reporter=Reporter(
                name="Marcus Webb",
                email="marcus.webb@contoso.com",
                department="DevOps",
            ),
            created_at="2026-03-18T14:15:00Z",
            channel=Channel.CHAT,
            attachments=["build_output.log"],
        ),
        gold=GoldAnswer(
            ticket_id="INC-DC-022",
            category=Category.SOFTWARE,
            priority=Priority.P2,
            assigned_team=Team.ENTERPRISE_APPS,
            needs_escalation=False,
            missing_information=[MissingInfoField.APPLICATION_VERSION],
            next_best_action=(
                "Fix the type mismatch in risk_engine.rs:142 — config.get() returns "
                "Option<String> but the code expects f64. This is blocking the 4 PM "
                "production release."
            ),
            remediation_steps=[
                "Fix the type mismatch in src/risk_engine.rs:142 by properly unwrapping and parsing the config value.",
                "Run the full test suite locally to confirm the fix.",
                "Push the fix and verify the CI/CD pipeline passes.",
                "Proceed with the production release once the build is green.",
            ],
        ),
        tags=["ansi_codes", "control_characters"],
        description=("Terminal output with ANSI escape codes for colors embedded in the description."),
    )


def _dc023_markdown_artifacts() -> EvalCase:
    return EvalCase(
        ticket=EvalTicket(
            ticket_id="INC-DC-023",
            subject="# MFA enrollment failing for new hires ## URGENT",
            description=(
                "## Issue Summary\n\n"
                "**Multiple new hires** from the _March 2026 onboarding cohort_ cannot "
                "complete MFA enrollment.\n\n"
                "### Affected Users\n\n"
                "| Name | Email | Status |\n"
                "|------|-------|--------|\n"
                "| James Cooper | james.cooper@contoso.com | ~~Enrolled~~ **Failed** |\n"
                "| Nina Petrova | nina.petrova@contoso.com | **Failed** |\n"
                "| Ahmed Hassan | ahmed.hassan@contoso.com | **Failed** |\n"
                "| Sophie Martin | sophie.martin@contoso.com | *Pending* |\n\n"
                "### Error Details\n\n"
                "When they go to https://aka.ms/mfasetup, they get:\n\n"
                "> Sorry, we can't process your request. The authentication method "
                "registration is not available for your account. Contact your admin. "
                "**(Error code: AADSTS65005)**\n\n"
                "### What I've Tried\n\n"
                "1. Verified licenses are assigned (✅ M365 E5)\n"
                "2. Checked Conditional Access policies (✅ no blocking rules)\n"
                "3. Ran `Get-MgUserAuthenticationMethod` — returns **empty** for all four\n"
                "4. Tried resetting authentication methods via Entra portal — same error\n\n"
                "### Impact\n\n"
                "These users **cannot access any internal systems** until MFA is enrolled. "
                "They've been sitting idle for two days.\n\n"
                "---\n"
                "*Filed by: Carlos Rivera, IT Onboarding*"
            ),
            reporter=Reporter(
                name="Carlos Rivera",
                email="carlos.rivera@contoso.com",
                department="IT",
            ),
            created_at="2026-03-19T09:45:00Z",
            channel=Channel.PORTAL,
            attachments=[],
        ),
        gold=GoldAnswer(
            ticket_id="INC-DC-023",
            category=Category.ACCESS_AUTH,
            priority=Priority.P2,
            assigned_team=Team.IAM,
            needs_escalation=False,
            missing_information=[MissingInfoField.ENVIRONMENT_DETAILS],
            next_best_action=(
                "Investigate AADSTS65005 error blocking MFA enrollment for four March 2026 "
                "new hires — authentication method registration appears disabled for their "
                "accounts despite correct licensing and policy configuration."
            ),
            remediation_steps=[
                "Check Entra ID authentication methods policy to confirm FIDO2/Authenticator "
                "is enabled for the new-hire group.",
                "Verify the users are members of the correct security group for MFA enrollment.",
                "Check for any tenant-level authentication method restrictions blocking registration.",
                "If a policy misconfiguration is found, correct it and have users retry enrollment.",
                "Escalate to Microsoft support if AADSTS65005 persists after policy verification.",
            ],
        ),
        tags=["markdown_artifacts", "formatting_noise"],
        description=(
            "Ticket formatted with heavy Markdown: headings, tables, bold, italic, "
            "strikethrough, blockquotes, ordered lists, and horizontal rules."
        ),
    )


def _dc024_spreadsheet_paste() -> EvalCase:
    return EvalCase(
        ticket=EvalTicket(
            ticket_id="INC-DC-024",
            subject="Database replication lag — slave nodes behind by 45 minutes",
            description=(
                "The PostgreSQL read replicas are lagging significantly behind the primary. "
                "Here is the current replication status from our monitoring:\n\n"
                "Node\tRole\tLSN Position\tLag (bytes)\tLag (time)\tState\n"
                "pg-primary-01\tPrimary\t3/A7F21B80\t0\t0s\tstreaming\n"
                "pg-replica-02\tReplica\t3/A5D10A40\t34,218,560\t12m 34s\tstreaming\n"
                "pg-replica-03\tReplica\t3/A1B90C20\t101,847,392\t45m 12s\tstreaming\n"
                "pg-replica-04\tReplica\t3/A4C80E10\t52,436,080\t22m 07s\tcatchup\n"
                "pg-replica-05\tReplica\t3/A7F21B80\t0\t0s\tstreaming\n\n"
                "Replica-03 is the one serving the Risk Dashboard and it's 45 minutes behind. "
                "The risk team is seeing stale portfolio data.\n\n"
                "I also checked the WAL sender stats:\n\n"
                "pid\tusesysid\tusename\tclient_addr\tstate\tsent_lsn\twrite_lsn\tflush_lsn\t"
                "replay_lsn\n"
                "14523\t16384\treplicator\t10.0.1.102\tstreaming\t3/A7F21B80\t3/A5D10A40\t"
                "3/A5D10A40\t3/A5D10A40\n"
                "14524\t16384\treplicator\t10.0.1.103\tstreaming\t3/A7F21B80\t3/A1B90C20\t"
                "3/A1B90C20\t3/A1B90C20\n"
                "14525\t16384\treplicator\t10.0.1.104\tcatchup\t3/A7F21B80\t3/A4C80E10\t"
                "3/A4C80E10\t3/A4C80E10\n"
                "14526\t16384\treplicator\t10.0.1.105\tstreaming\t3/A7F21B80\t3/A7F21B80\t"
                "3/A7F21B80\t3/A7F21B80\n\n"
                "— Fatima Al-Sayed, Data Engineering"
            ),
            reporter=Reporter(
                name="Fatima Al-Sayed",
                email="fatima.alsayed@contoso.com",
                department="Data Engineering",
            ),
            created_at="2026-03-18T15:20:00Z",
            channel=Channel.PORTAL,
            attachments=["replication_status.csv"],
        ),
        gold=GoldAnswer(
            ticket_id="INC-DC-024",
            category=Category.DATA_STORAGE,
            priority=Priority.P2,
            assigned_team=Team.DATA_PLATFORM,
            needs_escalation=False,
            missing_information=[MissingInfoField.CONFIGURATION_DETAILS],
            next_best_action=(
                "Investigate PostgreSQL replication lag on pg-replica-03 (45 minutes behind "
                "primary) serving the Risk Dashboard — the risk team is seeing stale data."
            ),
            remediation_steps=[
                "Check pg-replica-03 for I/O bottlenecks, CPU contention, or long-running queries blocking WAL replay.",
                "Review WAL sender and receiver stats for network throughput between primary and replica-03.",
                "If the replica is too far behind, consider reinitializing it from a base backup.",
                "Verify that all replicas return to near-zero lag after remediation.",
                "Set up alerting for replication lag exceeding 5 minutes.",
            ],
        ),
        tags=["spreadsheet_paste", "tabular_data"],
        description=("Ticket with tab-separated tabular data pasted from a terminal or spreadsheet."),
    )


def _dc025_yaml_config_dump() -> EvalCase:
    return EvalCase(
        ticket=EvalTicket(
            ticket_id="INC-DC-025",
            subject="Microservice won't start after config change — YAML attached",
            description=(
                "The notification-service won't start after I updated its configuration. It "
                "exits immediately with 'Configuration validation failed'. Here is the YAML "
                "config I'm trying to use:\n\n"
                "```yaml\n"
                "# notification-service config\n"
                "service:\n"
                "  name: notification-service\n"
                "  port: 8443\n"
                "  environment: production\n"
                "\n"
                "database:\n"
                "  host: db-prod-east.contoso.internal\n"
                "  port: 5432\n"
                "  name: notifications_prod\n"
                "  pool:\n"
                "    min_connections: 5\n"
                "    max_connections: 50\n"
                "    idle_timeout: 300s\n"
                "\n"
                "messaging:\n"
                "  broker: kafka-prod.contoso.internal:9092\n"
                "  topics:\n"
                "    - name: trade.notifications\n"
                "      partitions: 12\n"
                "    - name: compliance.alerts\n"
                "      partitions: 6\n"
                "  consumer_group: notif-svc-prod\n"
                "\n"
                "smtp:\n"
                "  host: smtp.contoso.com\n"
                "  port: 587\n"
                "  tls: true\n"
                "  from: notifications@contoso.com\n"
                "\n"
                "logging:\n"
                "  level: INFO\n"
                "  format: json\n"
                "  output: stdout\n"
                "```\n\n"
                "I changed the Kafka broker address and added the new compliance.alerts topic. "
                "The old config worked fine. What am I missing?\n\n"
                "— Kofi Mensah, Backend Engineering"
            ),
            reporter=Reporter(
                name="Kofi Mensah",
                email="kofi.mensah@contoso.com",
                department="Backend Engineering",
            ),
            created_at="2026-03-19T10:15:00Z",
            channel=Channel.CHAT,
            attachments=["notification-service.yaml"],
        ),
        gold=GoldAnswer(
            ticket_id="INC-DC-025",
            category=Category.SOFTWARE,
            priority=Priority.P3,
            assigned_team=Team.ENTERPRISE_APPS,
            needs_escalation=False,
            missing_information=[
                MissingInfoField.ERROR_MESSAGE,
                MissingInfoField.APPLICATION_VERSION,
            ],
            next_best_action=(
                "Debug the 'Configuration validation failed' error for notification-service "
                "after the Kafka broker address and topic changes — compare the new YAML "
                "against the config schema to identify the invalid field."
            ),
            remediation_steps=[
                "Run the service with verbose logging to get the specific validation error.",
                "Compare the new config against the JSON/YAML schema for notification-service.",
                "Check whether the new compliance.alerts topic exists on the Kafka cluster.",
                "Revert to the previous config to restore service while debugging.",
            ],
        ),
        tags=["yaml_config", "configuration_dump"],
        description=("Ticket with a full YAML configuration file pasted inline."),
    )


def _dc026_jwt_token_dump() -> EvalCase:
    return EvalCase(
        ticket=EvalTicket(
            ticket_id="INC-DC-026",
            subject="SSO token validation failing — JWT decode error",
            description=(
                "Hi IAM team,\n\n"
                "Our trading app is rejecting SSO tokens with 'Invalid signature'. I captured "
                "one of the failing tokens for analysis:\n\n"
                "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik1qTTFOREkyTmpVeU5UZzFOa1Ez"
                "T0RrMk16RTBPVEV3T0RRNU1UWTBOalkzTlRZeU5qZzBNQSJ9.eyJpc3MiOiJodHRwczovL2"
                "xvZ2luLm1pY3Jvc29mdG9ubGluZS5jb20vY29udG9zby5jb20vdjIuMCIsInN1YiI6IjFhMm"
                "IzYzRkLTVlNmYtN2c4aC05aTBqLWsxbDJtM240bzVwNiIsImF1ZCI6ImFiY2RlZjEyLTM0NT"
                "YtNzg5MC1hYmNkLWVmMTIzNDU2Nzg5MCIsImV4cCI6MTc0MjQ5NjAwMCwiaWF0IjoxNzQyND"
                "kyNDAwLCJuYmYiOjE3NDI0OTI0MDAsIm5hbWUiOiJKYW5lIERvZSIsInByZWZlcnJlZF91c2"
                "VybmFtZSI6ImphbmUuZG9lQGNvbnRvc28uY29tIiwidGlkIjoiMTIzNDU2NzgtOWFiYy1kZW"
                "YwLTEyMzQtNTY3ODlhYmNkZWYwIn0.FAKE_SIGNATURE_FOR_EVALUATION_PURPOSES_ONLY_"
                "THIS_IS_NOT_A_REAL_TOKEN_DO_NOT_ATTEMPT_TO_USE_abc123def456\n\n"
                "The token was issued by login.microsoftonline.com for our tenant. The 'kid' "
                "in the header doesn't match any of the signing keys in our JWKS endpoint. "
                "This started happening after the Azure AD key rotation last night.\n\n"
                "About 200 traders can't log in to the platform right now.\n\n"
                "— Nina Popov, Identity Engineering"
            ),
            reporter=Reporter(
                name="Nina Popov",
                email="nina.popov@contoso.com",
                department="Identity Engineering",
            ),
            created_at="2026-03-20T07:15:00Z",
            channel=Channel.EMAIL,
            attachments=[],
        ),
        gold=GoldAnswer(
            ticket_id="INC-DC-026",
            category=Category.ACCESS_AUTH,
            priority=Priority.P1,
            assigned_team=Team.IAM,
            needs_escalation=True,
            missing_information=[MissingInfoField.CONFIGURATION_DETAILS],
            next_best_action=(
                "Update the JWKS key cache in the trading app to include the new signing "
                "keys from Azure AD's key rotation — the 'kid' mismatch is causing token "
                "validation failures for ~200 traders."
            ),
            remediation_steps=[
                "Force-refresh the JWKS key cache from the Azure AD metadata endpoint.",
                "Verify the new 'kid' from the token header appears in the refreshed JWKS.",
                "If the app caches keys aggressively, deploy a config change to shorten the cache TTL.",
                "Confirm traders can log in after the JWKS refresh.",
                "Set up monitoring for JWKS key rotation events to prevent recurrence.",
            ],
        ),
        tags=["jwt_token", "credential_noise"],
        description=("Ticket with a full JWT token pasted inline for debugging an SSO issue."),
    )


def _dc027_auto_translation() -> EvalCase:
    return EvalCase(
        ticket=EvalTicket(
            ticket_id="INC-DC-027",
            subject="Laptop dock station not recognize the screens of external",
            description=(
                "Good day of the morning,\n\n"
                "I am having the problem with my station of docking. When I connect the "
                "portable computer to the dock, the screens external do not light up. The "
                "portable computer itself is functioning correctly and the screen of the "
                "portable computer is normal.\n\n"
                "I have tried the following of the steps:\n"
                "- Disconnecting and reconnecting the cable of the dock\n"
                "- Restarting the portable computer with the dock connected\n"
                "- Connecting only one screen at the time\n"
                "- Using a different port of USB-C on the portable computer\n\n"
                "The dock is the model Lenovo ThinkPad USB-C Dock Gen 2. The portable "
                "computer is Dell Latitude 5540. The screens are Dell U2722D. I am in the "
                "office of Singapore, floor 4, building 1.\n\n"
                "This problem started from yesterday after the update of Windows. Before the "
                "update, everything was functioning perfectly of well.\n\n"
                "Please help me to resolve this problem with urgency because I cannot work "
                "with only one screen for the analysis of the data.\n\n"
                "Thank you of your help,\nHiroshi Watanabe\nQuantitative Analysis"
            ),
            reporter=Reporter(
                name="Hiroshi Watanabe",
                email="hiroshi.watanabe@contoso.com",
                department="Quantitative Analysis",
            ),
            created_at="2026-03-19T02:30:00Z",
            channel=Channel.PORTAL,
            attachments=[],
        ),
        gold=GoldAnswer(
            ticket_id="INC-DC-027",
            category=Category.HARDWARE,
            priority=Priority.P3,
            assigned_team=Team.ENDPOINT,
            needs_escalation=False,
            missing_information=[MissingInfoField.DEVICE_INFO],
            next_best_action=(
                "Troubleshoot Lenovo ThinkPad USB-C dock failing to drive Dell U2722D external "
                "monitors after a Windows Update on a Dell Latitude 5540 in Singapore office."
            ),
            remediation_steps=[
                "Check the display driver version and compare against the pre-update version.",
                "Roll back the display driver or the specific Windows Update if a regression is identified.",
                "Update the Lenovo USB-C dock firmware to the latest version.",
                "Test with a direct DisplayPort or HDMI connection to rule out dock failure.",
            ],
        ),
        tags=["auto_translation", "translation_artifacts"],
        description=(
            "Ticket clearly written through machine translation with awkward phrasing and unnatural grammar patterns."
        ),
    )


def _dc028_voicemail_transcript() -> EvalCase:
    return EvalCase(
        ticket=EvalTicket(
            ticket_id="INC-DC-028",
            subject="[Voicemail Transcript] From: +1-212-555-0198 Duration: 2:14",
            description=(
                "[Automated Voicemail Transcription — Confidence: 72%]\n\n"
                "Hey uh this is uh Marcus from the trading floor, floor seven building two. "
                "Um we've got a major problem with the network here. The uh the Bloomberg "
                "terminals are all showing disconnected um they went down about uh twenty "
                "minutes ago maybe nine forty five ish. There's about fifteen terminals on "
                "this floor and none of them can connect to the bee pipe feed. Uh the rest "
                "of the internet seems fine we can get to web sites and email but Bloomberg "
                "specifically is down. This is really urgent because we're uh we're in the "
                "middle of the European close and the traders can't see their positions. Uh "
                "my extension is five five zero one nine eight if you need to call back. "
                "Thanks. Oh also uh I forgot to mention the terminals on floor eight seem "
                "to be working fine so it might be a switch or something just on our floor. "
                "Okay bye."
            ),
            reporter=Reporter(
                name="Marcus Thompson",
                email="marcus.thompson@contoso.com",
                department="Trading",
            ),
            created_at="2026-03-18T10:05:00Z",
            channel=Channel.PHONE,
            attachments=["voicemail_20260318_1005.mp3"],
        ),
        gold=GoldAnswer(
            ticket_id="INC-DC-028",
            category=Category.NETWORK,
            priority=Priority.P1,
            assigned_team=Team.NETWORK_OPS,
            needs_escalation=True,
            missing_information=[MissingInfoField.ERROR_MESSAGE],
            next_best_action=(
                "Investigate Bloomberg terminal B-PIPE feed connectivity failure on floor 7, "
                "building 2 — all 15 terminals disconnected during the European close while "
                "floor 8 is unaffected, suggesting a floor-level network switch issue."
            ),
            remediation_steps=[
                "Check the network switch serving floor 7, building 2 for port errors or flapping.",
                "Verify VLAN configuration for the Bloomberg B-PIPE feed on the floor 7 switch.",
                "Compare the switch configuration with floor 8 (which is working) to identify differences.",
                "If a switch failure is confirmed, fail over to the redundant switch or re-cable affected ports.",
                "Confirm all 15 Bloomberg terminals reconnect to the B-PIPE feed.",
            ],
        ),
        tags=["voicemail_transcript", "speech_to_text"],
        description=(
            "Auto-transcribed voicemail with filler words, hesitations, and low confidence transcription artifacts."
        ),
    )


def _dc029_css_dark_mode_noise() -> EvalCase:
    return EvalCase(
        ticket=EvalTicket(
            ticket_id="INC-DC-029",
            subject="Teams app crashing on macOS after update",
            description=(
                '<div style="background-color: #1e1e1e; color: #d4d4d4; font-family: '
                "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto; font-size: 14px; "
                "padding: 12px; -webkit-font-smoothing: antialiased; "
                '-moz-osx-font-smoothing: grayscale;">\n'
                '<p style="margin: 0 0 12px 0; line-height: 1.5; color: #cccccc;">Hi IT '
                "Support,</p>\n"
                '<p style="margin: 0 0 12px 0; line-height: 1.5; color: #cccccc;">Microsoft '
                "Teams keeps crashing on my MacBook Pro (M3, macOS Sonoma 14.4) every time I "
                "try to join a video call. It worked fine until the Teams update that pushed "
                "yesterday (version 24045.1234.5678.9012). The app opens and I can chat, but "
                "the moment I click 'Join' on a meeting, it crashes to desktop.</p>\n"
                '<p style="margin: 0 0 12px 0; line-height: 1.5; color: #cccccc;">I checked '
                "the macOS Console and see repeated errors:</p>\n"
                '<pre style="background-color: #0d0d0d; color: #ce9178; padding: 8px; '
                "border-radius: 4px; overflow-x: auto; font-size: 12px; "
                'font-family: Menlo, monospace;">\n'
                "com.microsoft.teams: EXC_BAD_ACCESS (SIGSEGV) — "
                "Thread 14: WebRTC::VideoCapture\n"
                "Crashed Thread: 14 Dispatch queue: com.apple.avfoundation.capture\n"
                "</pre>\n"
                '<p style="margin: 0 0 12px 0; line-height: 1.5; color: #cccccc;">I tried '
                "reinstalling Teams and clearing the cache in ~/Library/Application Support/"
                "Microsoft/Teams. Same crash.</p>\n"
                '<p style="margin: 0 0 4px 0; color: #858585; font-size: 12px;">Thanks,<br/>'
                "Emma Liu<br/>Portfolio Management</p>\n"
                "</div>"
            ),
            reporter=Reporter(
                name="Emma Liu",
                email="emma.liu@contoso.com",
                department="Portfolio Management",
            ),
            created_at="2026-03-19T14:00:00Z",
            channel=Channel.EMAIL,
            attachments=["crash_log.txt"],
        ),
        gold=GoldAnswer(
            ticket_id="INC-DC-029",
            category=Category.SOFTWARE,
            priority=Priority.P3,
            assigned_team=Team.ENTERPRISE_APPS,
            needs_escalation=False,
            missing_information=[MissingInfoField.STEPS_TO_REPRODUCE],
            next_best_action=(
                "Investigate Microsoft Teams video call crash (EXC_BAD_ACCESS in "
                "WebRTC::VideoCapture) on MacBook Pro M3 after Teams update to "
                "version 24045.1234.5678.9012 — likely a WebRTC compatibility issue "
                "with the Apple Silicon camera pipeline."
            ),
            remediation_steps=[
                "Check if the crash is reproducible with camera disabled to isolate the WebRTC video capture module.",
                "Roll back to the previous Teams version if possible.",
                "Check for known issues with Teams version 24045.x on Apple Silicon Macs.",
                "If confirmed as a Teams bug, report to Microsoft and provide a workaround (e.g., join via browser).",
            ],
        ),
        tags=["css_noise", "dark_mode_artifacts"],
        description=("Email body saturated with inline CSS dark-mode styling from the email client."),
    )


def _dc030_concatenated_tickets() -> EvalCase:
    return EvalCase(
        ticket=EvalTicket(
            ticket_id="INC-DC-030",
            subject="Multiple issues — Teams, printer, and badge access",
            description=(
                "Hi IT,\n\n"
                "I have three issues I need help with:\n\n"
                "ISSUE 1 — TEAMS AUDIO\n"
                "In every Teams call, the other participants say my audio cuts out every "
                "few seconds. I've tested my headset (Jabra Evolve2 75) on Zoom and it works "
                "perfectly, so it's a Teams-specific problem. I'm on Teams version "
                "24040.1234.5678 on Windows 11.\n\n"
                "ISSUE 2 — PRINTER\n"
                "The color printer on floor 5 (HP Color LaserJet Pro MFP M479fdw) is printing "
                "everything with a magenta tint. Black-and-white prints are fine. I think the "
                "cyan toner cartridge might be empty or misaligned.\n\n"
                "ISSUE 3 — BADGE ACCESS\n"
                "My badge stopped working for the server room (Room 5-102). It works for all "
                "other doors. I used to have access — it might have been revoked by mistake "
                "during the quarterly access review.\n\n"
                "Can you please open three separate tickets for these? Or handle them all in "
                "this one, I don't mind.\n\n"
                "Thanks,\nJordan Williams\nCloud Infrastructure"
            ),
            reporter=Reporter(
                name="Jordan Williams",
                email="jordan.williams@contoso.com",
                department="Cloud Infrastructure",
            ),
            created_at="2026-03-20T08:30:00Z",
            channel=Channel.EMAIL,
            attachments=[],
        ),
        gold=GoldAnswer(
            ticket_id="INC-DC-030",
            category=Category.SOFTWARE,
            priority=Priority.P3,
            assigned_team=Team.ENTERPRISE_APPS,
            needs_escalation=False,
            missing_information=[
                MissingInfoField.DEVICE_INFO,
                MissingInfoField.STEPS_TO_REPRODUCE,
            ],
            next_best_action=(
                "Address the primary Teams audio issue — intermittent audio dropout "
                "in Teams calls with a Jabra Evolve2 75 headset on Windows 11 — and split "
                "the printer and badge access items into separate tickets for the appropriate "
                "teams."
            ),
            remediation_steps=[
                "Troubleshoot Teams audio by checking audio device settings and updating the Jabra firmware.",
                "Split the printer issue (magenta tint on floor 5 HP Color LaserJet) into a "
                "separate ticket for Endpoint Engineering.",
                "Split the badge access issue (server room 5-102) into a separate ticket for "
                "Identity & Access Management.",
                "Follow up with the reporter once all three issues are tracked.",
            ],
        ),
        tags=["concatenated_issues", "multi_topic"],
        description=("Single ticket containing three unrelated issues that should ideally be separate tickets."),
    )


def _dc031_mime_boundaries() -> EvalCase:
    return EvalCase(
        ticket=EvalTicket(
            ticket_id="INC-DC-031",
            subject="FW: SAP GUI login error after patch — MIME conversion issue?",
            description=(
                "This is a multi-part message in MIME format.\n"
                "------=_Part_12345_987654321.1712000000000\n"
                "Content-Type: text/plain; charset=UTF-8\n"
                "Content-Transfer-Encoding: quoted-printable\n\n"
                "Hi IT Support,\n\n"
                "Since last Thursday's SAP GUI patch (version 8.00 PL4), I'm getting a "
                "persistent error every time I try to log in to our ECC production system "
                "(SID: PRD, client 100). The login dialog appears, I enter my credentials, "
                "and after about 15 seconds I get: =E2=80=9CICE_LOGON_FAIL: SSO ticket "
                "validation failed=E2=80=9D. This is blocking all my month-end closing "
                "activities in FI/CO. I've cleared my SSO cache and regenerated my SNC "
                "certificate via the SAP Logon Pad but the issue persists. Our team lead "
                "Karen Walsh is also seeing the same error on her machine.\n\n"
                "Thanks,\nMichael Torres\nFinancial Control\n\n"
                "------=_Part_12345_987654321.1712000000000\n"
                "Content-Type: text/html; charset=UTF-8\n"
                "Content-Transfer-Encoding: quoted-printable\n\n"
                "<html><body><p>Hi IT Support,</p><p>Since last Thursday=E2=80=99s SAP GUI "
                "patch (version 8.00 PL4)...</p></body></html>\n"
                "------=_Part_12345_987654321.1712000000000--\n"
            ),
            reporter=Reporter(
                name="Michael Torres",
                email="michael.torres@contoso.com",
                department="Financial Control",
            ),
            created_at="2026-04-07T09:15:00Z",
            channel=Channel.EMAIL,
            attachments=[],
        ),
        gold=GoldAnswer(
            ticket_id="INC-DC-031",
            category=Category.SOFTWARE,
            priority=Priority.P3,
            assigned_team=Team.ENTERPRISE_APPS,
            needs_escalation=False,
            missing_information=[MissingInfoField.APPLICATION_VERSION],
            next_best_action=(
                "Investigate SAP GUI SSO login failure (ICE_LOGON_FAIL) on ECC production "
                "system PRD/100 after SAP GUI 8.00 PL4 patch — likely an SSO ticket "
                "validation regression introduced by the patch."
            ),
            remediation_steps=[
                "Verify SAP GUI 8.00 PL4 release notes for known SSO ticket validation issues.",
                "Compare SNC/SSO configuration on the affected workstations against a working baseline.",
                "Test login with explicit user/password (bypassing SSO) to confirm the SAP backend is reachable.",
                "Roll back SAP GUI to PL3 on a test machine to confirm the patch is the root cause.",
                "If confirmed, open an SAP support incident and apply a targeted hotfix or workaround.",
            ],
        ),
        tags=["data-cleanup", "mime-boundaries"],
        description="Ticket body contains raw MIME multipart boundary markers and quoted-printable encoding artifacts.",
    )


def _dc032_multiple_base64_images() -> EvalCase:
    return EvalCase(
        ticket=EvalTicket(
            ticket_id="INC-DC-032",
            subject="Network switch on floor 3 dropping packets — screenshots inline",
            description=(
                "Hi Network Team,\n\n"
                "The Cisco Catalyst 9300-48P switch in IDF closet 3-B (hostname: CHI-IDF3B-SW01) "
                "has been intermittently dropping packets since Monday morning. Users on VLANs 310 "
                "and 312 are experiencing 30-40% packet loss during peak hours (10 AM - 2 PM). "
                "I ran a continuous ping to the core switch (10.40.1.1) and captured these:\n\n"
                "Screenshot 1 — ping results:\n"
                "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAQAAAAEACAYAAABccq"
                "FnAAAACXBIWXMAAAsTAAALEwEAmpwYAAAF8WlUWHRYTUw6Y29tLmFkb2JlLn"
                "htcAAAAAAAA8P3hwYWNrZXQgYmVnaW49Iu+7vyIgaWQ9Ilc1TTBNcENlaGlI"
                "enJlU3pOVGN6a2M5ZCI/Pgo8eDp4bXBtZXRhIHhtbG5zOng9ImFkb2JlOm5z"
                "Om1ldGEvIiB4OnhtcHRrPSJBZG9iZSBYTVAgQ29yZSA3LjItYzAwMCA3OS5m"
                "\n\n"
                "Screenshot 2 — switch port errors on Gi1/0/24:\n"
                "data:image/png;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAA"
                "AABAAEAAAICRAEAOw==ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnop"
                "qrstuvwxyz0123456789+/ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmn"
                "opqrstuvwxyz0123456789+/ABCDEFGHIJKLMNOPQRSTUVWXYZ\n\n"
                "Screenshot 3 — Spanning Tree topology showing reconvergence:\n"
                "data:image/png;base64,/9j/4AAQSkZJRgABAQEASABIAAD/2wBDAAgGBgcG"
                "BQgHBwcJCQgKDBQNDAsLDBkSEw8UHRofHh0aHBwgJC4nICIsIxwcKDcpLDAx"
                "NDQ0Hyc5PTgyPC4zNDL/2wBDAQkJCQwLDBgNDRgyIRwhMjIyMjIyMjIyMjIy"
                "\n\n"
                "I suspect a bad GBIC in slot 1 port 24 or possibly a spanning tree loop "
                "caused by someone patching an unauthorized switch on VLAN 310. The MAC "
                "address table is showing 3x the expected entries. Can you investigate "
                "before the trading floor opens tomorrow?\n\n"
                "Regards,\nSarah Kim\nNetwork Infrastructure"
            ),
            reporter=Reporter(
                name="Sarah Kim",
                email="sarah.kim@contoso.com",
                department="Network Infrastructure",
            ),
            created_at="2026-04-07T16:45:00Z",
            channel=Channel.PORTAL,
            attachments=[],
        ),
        gold=GoldAnswer(
            ticket_id="INC-DC-032",
            category=Category.NETWORK,
            priority=Priority.P2,
            assigned_team=Team.NETWORK_OPS,
            needs_escalation=False,
            missing_information=[MissingInfoField.NETWORK_LOCATION],
            next_best_action=(
                "Investigate intermittent packet loss (30-40%) on Cisco Catalyst 9300 "
                "switch CHI-IDF3B-SW01 affecting VLANs 310 and 312 — possible bad GBIC "
                "on Gi1/0/24 or spanning tree loop from an unauthorized switch."
            ),
            remediation_steps=[
                "Check Gi1/0/24 for CRC errors, input/output errors, and GBIC diagnostics "
                "(show interfaces transceiver).",
                "Review the MAC address table on VLANs 310 and 312 for unexpected entries indicating a rogue switch.",
                "Inspect Spanning Tree topology for recent reconvergence events (show spanning-tree detail).",
                "If a rogue switch is found, shut the offending port and enable BPDU Guard on all access ports.",
                "Replace the GBIC in Gi1/0/24 if diagnostics indicate failure.",
            ],
        ),
        tags=["data-cleanup", "multiple-base64", "inline-images"],
        description=(
            "Ticket contains three separate base64-encoded inline images interspersed with network issue details."
        ),
    )


def _dc033_ics_calendar_metadata() -> EvalCase:
    return EvalCase(
        ticket=EvalTicket(
            ticket_id="INC-DC-033",
            subject="RE: Calendar sync broken — invite data pasted below",
            description=(
                "Hi team,\n\n"
                "My Outlook calendar has completely stopped syncing with my iPhone (iOS 17.4). "
                "Meetings I accept on the desktop don't show up on my phone, and vice versa. "
                "This started two days ago after I accepted a recurring board meeting invite. "
                "I exported the problematic invite — here's the raw data:\n\n"
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
                "END:VTIMEZONE\n"
                "BEGIN:VEVENT\n"
                "DTSTART;TZID=Eastern Standard Time:20260415T090000\n"
                "DTEND;TZID=Eastern Standard Time:20260415T110000\n"
                "RRULE:FREQ=MONTHLY;BYDAY=3WE;COUNT=12\n"
                "SUMMARY:Q2 Board of Directors Meeting\n"
                "LOCATION:Executive Conference Room 22-A\n"
                "ORGANIZER;CN=CEO Office:mailto:ceo.office@contoso.com\n"
                "ATTENDEE;ROLE=REQ-PARTICIPANT;RSVP=TRUE:mailto:robert.chen@contoso.com\n"
                "ATTENDEE;ROLE=REQ-PARTICIPANT;RSVP=TRUE:mailto:cfo@contoso.com\n"
                "STATUS:CONFIRMED\n"
                "SEQUENCE:3\n"
                "END:VEVENT\n"
                "END:VCALENDAR\n\n"
                "After accepting this invite the sync just died. All other Exchange features "
                "(email, contacts) work fine on the phone. I've already tried removing and "
                "re-adding my Exchange account on iOS but the calendar still won't sync.\n\n"
                "Robert Chen\nChief Risk Officer"
            ),
            reporter=Reporter(
                name="Robert Chen",
                email="robert.chen@contoso.com",
                department="Executive Management",
            ),
            created_at="2026-04-08T08:00:00Z",
            channel=Channel.EMAIL,
            attachments=[],
        ),
        gold=GoldAnswer(
            ticket_id="INC-DC-033",
            category=Category.SOFTWARE,
            priority=Priority.P3,
            assigned_team=Team.ENTERPRISE_APPS,
            needs_escalation=False,
            missing_information=[MissingInfoField.DEVICE_INFO],
            next_best_action=(
                "Investigate Outlook-to-iOS calendar sync failure triggered by a recurring "
                "board meeting invite (RRULE with SEQUENCE:3) — likely a corrupted calendar "
                "item blocking the Exchange ActiveSync sync state."
            ),
            remediation_steps=[
                "Check Exchange ActiveSync device partnership status for the user's iPhone.",
                "Examine the problematic calendar item server-side using MFCMAPI or EWS to identify corruption.",
                "Delete and recreate the recurring board meeting invite if the item is corrupted.",
                "Reset the ActiveSync sync state on the server for the calendar folder.",
                "Verify calendar sync resumes on the iPhone after the fix.",
            ],
        ),
        tags=["data-cleanup", "calendar-metadata", "ics"],
        description="Ticket body contains raw ICS/vCalendar data mixed with a calendar sync failure complaint.",
    )


def _dc034_buried_issue_long_email() -> EvalCase:
    return EvalCase(
        ticket=EvalTicket(
            ticket_id="INC-DC-034",
            subject="Quick question from the 7th floor",
            description=(
                "Hi IT,\n\n"
                "Hope you're all doing well! I know you guys have been super busy lately with "
                "the data center migration and everything. I saw the update email from Marcus in "
                "Infrastructure about the weekend maintenance window — sounds like a big effort. "
                "Kudos to everyone involved!\n\n"
                "Anyway, I wanted to give you a bit of context before I get to my question. So "
                "last week our team had an offsite at the Grand Hyatt downtown for the annual "
                "strategic planning session. It was actually a great event — we finalized the "
                "new product roadmap for Q3/Q4 and there were some really interesting "
                "presentations from the London office about their FX derivatives platform "
                "rewrite. Patricia from Compliance also gave a talk about the new SEC "
                "reporting requirements that are coming in September, which is going to affect "
                "how we handle client data in the warehouse.\n\n"
                "Speaking of the London office, I've been working pretty closely with James "
                "Whitfield and his team on the cross-border settlement engine. They're using "
                "some new containerized microservices architecture that's honestly pretty "
                "impressive. We had a three-hour workshop about their CI/CD pipeline and how "
                "they've managed to get deployment times down to under 8 minutes for the full "
                "stack. I think we could learn a lot from their approach. I'm going to set up "
                "a knowledge-sharing session with our DevOps team when I get a chance.\n\n"
                "On a totally different note, did you hear that the cafeteria on 3 is getting "
                "renovated? Apparently they're adding a sushi bar and a proper espresso station. "
                "The current coffee situation on our floor is pretty dire — the Keurig machine "
                "has been making these weird gurgling noises for weeks. Not an IT issue, I know, "
                "but I figured someone might know who to contact about facilities stuff.\n\n"
                "Oh, and before I forget — I ran into Dave Kowalski from Accounting in the "
                "elevator yesterday and he mentioned that his team is having trouble with the "
                "new SAP Concur integration for expense reports. Apparently the receipts aren't "
                "syncing from the mobile app. I told him to open a ticket but you know how it "
                "is — he'll probably just email you guys directly.\n\n"
                "Also, I've been meaning to ask — is there any update on the VDI refresh "
                "project? We were told back in January that we'd be getting Citrix upgrades "
                "by end of Q1 but I haven't heard anything since. The current VDI performance "
                "is pretty sluggish, especially when running Bloomberg and Excel simultaneously. "
                "My team has been complaining about 5-10 second lag when switching between "
                "worksheets on large models. Not urgent, just wondering about the timeline.\n\n"
                "Alright, here's the actual reason I'm writing. I was reviewing my authentication "
                "logs this morning in the Azure AD portal (I have read access for our team's "
                "service accounts) and I noticed something alarming. Our production service "
                "account svc-tradecapture-prod had a successful interactive login at 03:42 AM "
                "EST on Saturday April 5th from an IP address geolocated to Vladivostok, Russia "
                "(IP: 91.243.xx.xx). This account should ONLY authenticate via non-interactive "
                "service principal flows from our Azure East US 2 datacenter. There should be "
                "absolutely no interactive logins, and certainly not from a Russian IP address. "
                "I think this may be a compromised credential and needs immediate investigation.\n\n"
                "Thanks!\nAisha Patel\nSenior Quantitative Developer\nElectronic Trading"
            ),
            reporter=Reporter(
                name="Aisha Patel",
                email="aisha.patel@contoso.com",
                department="Electronic Trading",
            ),
            created_at="2026-04-07T10:30:00Z",
            channel=Channel.EMAIL,
            attachments=[],
        ),
        gold=GoldAnswer(
            ticket_id="INC-DC-034",
            category=Category.SECURITY,
            priority=Priority.P1,
            assigned_team=Team.SECURITY_OPS,
            needs_escalation=True,
            missing_information=[MissingInfoField.TIMESTAMP, MissingInfoField.ENVIRONMENT_DETAILS],
            next_best_action=(
                "Immediately investigate the unauthorized interactive login to production "
                "service account svc-tradecapture-prod from a Russian IP address (91.243.xx.xx) "
                "at 03:42 AM EST on April 5th — this indicates a potential credential compromise "
                "of a critical trading system."
            ),
            remediation_steps=[
                "Immediately rotate the credentials for svc-tradecapture-prod and revoke all active sessions.",
                "Review Azure AD sign-in logs for the service account over the past 30 days "
                "for additional anomalous logins.",
                "Check whether the IP 91.243.xx.xx appears in threat intelligence feeds.",
                "Audit what resources the account accessed during the suspicious session.",
                "Enable Conditional Access policies to block interactive logins "
                "and restrict to Azure East US 2 IP ranges.",
                "Engage the Security Incident Response team for a full investigation.",
            ],
        ),
        tags=["data-cleanup", "buried-issue", "very-long-email"],
        description=(
            "Very long email with extensive background chatter where the critical security "
            "alert is buried at the end of the message."
        ),
    )


def _dc035_multilingual_disclaimers() -> EvalCase:
    return EvalCase(
        ticket=EvalTicket(
            ticket_id="INC-DC-035",
            subject="Keyboard not working — keys unresponsive",
            description=(
                "Hello IT,\n\n"
                "The built-in keyboard on my Dell Latitude 7440 has stopped responding. The "
                "entire top row of keys (F1 through F12, Escape, and the number row) are "
                "completely dead. The trackpad works fine and I can type using an external USB "
                "keyboard. The issue started this morning after I spilled a small amount of "
                "water near the laptop — I wiped it up immediately but the top row keys have "
                "been unresponsive ever since. I've tried restarting and running the Dell "
                "built-in diagnostics (ePSA) but the keyboard test fails for the affected "
                "keys. My asset tag is CONT-L7440-2847.\n\n"
                "Thanks,\nNadia Kowalski\nFixed Income Trading\n\n"
                "---\n\n"
                "CONFIDENTIALITY NOTICE: This e-mail message, including any attachments, is "
                "for the sole use of the intended recipient(s) and may contain confidential and "
                "privileged information. Any unauthorized review, use, disclosure, or distribution "
                "is prohibited. If you are not the intended recipient, please contact the sender "
                "by reply e-mail and destroy all copies of the original message.\n\n"
                "AVIS DE CONFIDENTIALITÉ : Ce message électronique, y compris les pièces "
                "jointes, est destiné exclusivement à l'usage du ou des destinataires prévus "
                "et peut contenir des informations confidentielles et protégées. Toute "
                "consultation, utilisation, divulgation ou distribution non autorisée est "
                "interdite. Si vous n'êtes pas le destinataire prévu, veuillez contacter "
                "l'expéditeur par e-mail et détruire toutes les copies du message original.\n\n"
                "VERTRAULICHKEITSHINWEIS: Diese E-Mail-Nachricht einschließlich aller Anhänge "
                "ist ausschließlich für den/die vorgesehenen Empfänger bestimmt und kann "
                "vertrauliche und geschützte Informationen enthalten. Jede unbefugte Überprüfung, "
                "Nutzung, Offenlegung oder Verbreitung ist untersagt. Wenn Sie nicht der "
                "vorgesehene Empfänger sind, wenden Sie sich bitte per E-Mail an den Absender "
                "und vernichten Sie alle Kopien der Originalnachricht.\n\n"
                "AVISO DE CONFIDENCIALIDAD: Este mensaje de correo electrónico, incluidos los "
                "archivos adjuntos, es para uso exclusivo del destinatario o destinatarios "
                "previstos y puede contener información confidencial y privilegiada. Queda "
                "prohibida cualquier revisión, uso, divulgación o distribución no autorizados. "
                "Si usted no es el destinatario previsto, comuníquese con el remitente por "
                "correo electrónico y destruya todas las copias del mensaje original.\n\n"
                "AVVISO DI RISERVATEZZA: Questo messaggio di posta elettronica, inclusi gli "
                "allegati, è destinato esclusivamente all'uso del destinatario o dei destinatari "
                "previsti e può contenere informazioni riservate e privilegiate. È vietato "
                "qualsiasi esame, utilizzo, divulgazione o distribuzione non autorizzati.\n\n"
                "AVISO DE CONFIDENCIALIDADE: Esta mensagem de e-mail, incluindo quaisquer "
                "anexos, é para uso exclusivo do(s) destinatário(s) pretendido(s) e pode conter "
                "informações confidenciais e privilegiadas. Qualquer revisão, uso, divulgação "
                "ou distribuição não autorizada é proibida.\n\n"
                "機密保持に関するお知らせ：この電子メールメッセージは、添付ファイルを含め、"
                "意図された受信者のみを対象としており、機密情報および特権情報が含まれている"
                "可能性があります。不正な閲覧、使用、開示、または配布は禁止されています。\n\n"
                "保密声明：本电子邮件及其附件仅供预期收件人使用，可能包含机密和特权信息。"
                "未经授权的审查、使用、披露或分发均被禁止。如果您不是预期收件人，请通过"
                "回复电子邮件联系发件人并销毁原始邮件的所有副本。\n\n"
                "Contoso Financial Services | 200 Park Avenue, New York, NY 10166\n"
            ),
            reporter=Reporter(
                name="Nadia Kowalski",
                email="nadia.kowalski@contoso.com",
                department="Fixed Income Trading",
            ),
            created_at="2026-04-08T11:20:00Z",
            channel=Channel.EMAIL,
            attachments=[],
        ),
        gold=GoldAnswer(
            ticket_id="INC-DC-035",
            category=Category.HARDWARE,
            priority=Priority.P3,
            assigned_team=Team.ENDPOINT,
            needs_escalation=False,
            missing_information=[MissingInfoField.DEVICE_INFO],
            next_best_action=(
                "Arrange hardware repair or replacement for Dell Latitude 7440 (asset tag "
                "CONT-L7440-2847) with non-functional top-row keyboard keys after a liquid "
                "spill incident."
            ),
            remediation_steps=[
                "Confirm the affected keys via Dell ePSA diagnostics report.",
                "Check Dell warranty status for asset tag CONT-L7440-2847.",
                "If under warranty, open a Dell ProSupport case for keyboard replacement.",
                "Provide the user with a loaner laptop or external keyboard while repair is pending.",
                "Once repaired, verify all keys function and update the asset record.",
            ],
        ),
        tags=["data-cleanup", "multilingual-disclaimers"],
        description=("Short hardware issue buried under legal disclaimers repeated in eight languages."),
    )


def _dc036_ndr_bounce() -> EvalCase:
    return EvalCase(
        ticket=EvalTicket(
            ticket_id="INC-DC-036",
            subject="Undeliverable: RE: Q2 forecast data file for compliance",
            description=(
                "This is an automatically generated Delivery Status Notification.\n\n"
                "Delivery to the following recipients failed permanently:\n\n"
                "    compliance-reports@contoso.com\n\n"
                "Technical details of permanent failure:\n"
                "550 5.1.1 The email account that you tried to reach does not exist. Please "
                "try double-checking the recipient's email address for typos or unnecessary "
                "spaces. Learn more at https://support.contoso.com/mail/answer/550\n\n"
                "Diagnostic-Code: smtp; 550-5.1.1 The email account that you tried to reach "
                "does not exist.\n"
                "Remote-MTA: dns; mail.contoso.com (10.50.2.14)\n"
                "Reporting-MTA: dns; smtp-relay-chi-01.contoso.com\n"
                "X-Contoso-MailScanner-ID: MS-20260408-0923-BNC-44821\n"
                "Received-From-MTA: dns; edge-gw-02.contoso.com (10.50.1.3)\n"
                "Arrival-Date: Wed, 08 Apr 2026 09:23:15 -0400\n"
                "Final-Recipient: rfc822; compliance-reports@contoso.com\n"
                "Action: failed\n"
                "Status: 5.1.1\n"
                "Last-Attempt-Date: Wed, 08 Apr 2026 09:23:16 -0400\n\n"
                "--- Below this line is a copy of the original message ---\n\n"
                "From: Kevin Okafor <kevin.okafor@contoso.com>\n"
                "To: compliance-reports@contoso.com\n"
                "Date: Wed, 08 Apr 2026 09:22:58 -0400\n"
                "Subject: Q2 forecast data file for compliance\n\n"
                "Hi Compliance team,\n\n"
                "I've been trying to send the Q2 forecast data file to the compliance-reports "
                "shared mailbox for the past three days and every time it bounces back with a "
                "550 error. This mailbox was working fine last week — I successfully sent the "
                "March month-end package to it on Friday March 28th. Our regulatory filing "
                "deadline is April 10th and I need to get this data to the compliance team "
                "ASAP. I've verified the address is correct (compliance-reports@contoso.com). "
                "Can someone check if the shared mailbox was accidentally deleted or disabled "
                "during the Exchange migration last weekend?\n\n"
                "Thanks,\nKevin Okafor\nRegulatory Reporting"
            ),
            reporter=Reporter(
                name="Kevin Okafor",
                email="kevin.okafor@contoso.com",
                department="Regulatory Reporting",
            ),
            created_at="2026-04-08T09:30:00Z",
            channel=Channel.EMAIL,
            attachments=[],
        ),
        gold=GoldAnswer(
            ticket_id="INC-DC-036",
            category=Category.NETWORK,
            priority=Priority.P2,
            assigned_team=Team.NETWORK_OPS,
            needs_escalation=False,
            missing_information=[MissingInfoField.PREVIOUS_TICKET_ID],
            next_best_action=(
                "Investigate the 550 5.1.1 bounce for the compliance-reports shared mailbox "
                "— likely deleted or disabled during the Exchange migration last weekend — "
                "with an April 10th regulatory filing deadline."
            ),
            remediation_steps=[
                "Check Exchange Admin Center for the compliance-reports shared mailbox status "
                "(active, soft-deleted, or disabled).",
                "If soft-deleted, recover the mailbox from the Exchange retention hold.",
                "If the mailbox was not migrated, recreate it and restore from the latest backup.",
                "Verify SMTP routing on smtp-relay-chi-01 to ensure the mailbox is reachable.",
                "Confirm the user can successfully deliver email to compliance-reports@contoso.com.",
            ],
        ),
        tags=["data-cleanup", "ndr", "bounce-back"],
        description=("Non-Delivery Report wrapping the original email about a shared mailbox delivery failure."),
    )


def _dc037_regex_code_patterns() -> EvalCase:
    return EvalCase(
        ticket=EvalTicket(
            ticket_id="INC-DC-037",
            subject="Internal app crashing on special characters in search — regex and SQL details",
            description=(
                "Hi Enterprise Apps team,\n\n"
                "Our internal trade reconciliation tool (TradeRecon v3.8.1) is crashing every "
                "time a user enters certain characters in the search field. I've been debugging "
                "it and traced the problem to unescaped regex patterns being passed directly to "
                "the SQL query engine. Here are the specific inputs that cause crashes:\n\n"
                "1. Regex used for trade ID matching:\n"
                r"   ^(?:TRD|SWP|FUT)-\d{4}-[A-Z]{2,4}\/\d{2,6}(?:\.\d+)?$"
                "\n"
                "2. The SQL query that fails (from the app logs):\n"
                "   SELECT t.trade_id, t.counterparty, t.notional FROM trades t\n"
                "   WHERE t.trade_id ~ '^(?:TRD|SWP|FUT)-\\d{4}' AND t.status <> 'CANCELLED'\n"
                "   AND t.book_date BETWEEN '2026-01-01' AND '2026-04-07'\n"
                "   ORDER BY t.book_date DESC LIMIT 500;\n"
                "3. Characters that trigger the crash: backslash (\\), pipe (|), curly "
                "braces ({}), and the caret (^) when combined with brackets []\n"
                "4. Stack trace excerpt:\n"
                "   java.util.regex.PatternSyntaxException: Unclosed group near index 42\n"
                r"     ^(?:TRD|SWP|FUT)-\d{4}-[A-Z]{2,4}\/\d{2,6}(?:\.\d+"
                "\n"
                "     at java.util.regex.Pattern.error(Pattern.java:1969)\n"
                "     at com.contoso.traderecon.search.RegexSearchParser.compile(RegexSearchParser.java:147)\n\n"
                "This is affecting about 20 users in the settlements team who use this tool "
                "daily for trade matching. They're having to use manual Excel-based matching "
                "as a workaround which is error-prone and slow.\n\n"
                "Thanks,\nLiam O'Donnell\nTechnology — Trading Systems"
            ),
            reporter=Reporter(
                name="Liam O'Donnell",
                email="liam.odonnell@contoso.com",
                department="Trading Systems",
            ),
            created_at="2026-04-09T14:10:00Z",
            channel=Channel.PORTAL,
            attachments=["traderecon_crash_log.txt"],
        ),
        gold=GoldAnswer(
            ticket_id="INC-DC-037",
            category=Category.SOFTWARE,
            priority=Priority.P3,
            assigned_team=Team.ENTERPRISE_APPS,
            needs_escalation=False,
            missing_information=[MissingInfoField.AFFECTED_USERS, MissingInfoField.APPLICATION_VERSION],
            next_best_action=(
                "Fix the input sanitization bug in TradeRecon v3.8.1 where unescaped special "
                "characters in the search field are passed directly to the regex engine and SQL "
                "query, causing PatternSyntaxException crashes for settlements users."
            ),
            remediation_steps=[
                "Review the RegexSearchParser.compile() method at line 147 to add proper input escaping.",
                "Implement Pattern.quote() or equivalent to sanitize user input before regex compilation.",
                "Add parameterized queries to prevent special characters from breaking the SQL layer.",
                "Deploy a hotfix to TradeRecon and verify with the problematic inputs "
                "(backslash, pipe, curly braces, caret).",
                "Notify the settlements team once the fix is deployed.",
            ],
        ),
        tags=["data-cleanup", "regex", "code-patterns"],
        description=(
            "Ticket body contains raw regex patterns, SQL queries, and stack traces with special "
            "characters that could confuse text parsers."
        ),
    )


def _dc038_contradictory_replies() -> EvalCase:
    return EvalCase(
        ticket=EvalTicket(
            ticket_id="INC-DC-038",
            subject="RE: RE: RE: Laptop screen flickering — RESOLVED? or not?",
            description=(
                "--- Reply from: Hannah Bergström (2026-04-09 16:40) ---\n"
                "Update: Nope, the screen is flickering AGAIN. The docking station swap did "
                "not fix it. It was fine for about two hours after Carlos swapped the dock "
                "and then the flickering came back, this time even worse. Now the entire "
                "display goes black for 2-3 seconds every few minutes. I can't work like "
                "this. I have a client presentation tomorrow morning and I need this fixed "
                "TODAY.\n\n"
                "--- Reply from: Carlos Mendez, Endpoint Support (2026-04-09 14:15) ---\n"
                "Hi Hannah, I swapped out your docking station (old: Lenovo ThinkPad USB-C "
                "Dock Gen 2, serial LNVO-D2-8834; new: serial LNVO-D2-9917) and the "
                "flickering appears to be resolved. I tested it for 15 minutes with dual "
                "monitors and saw no issues. Marking this as RESOLVED. Please reopen if the "
                "issue recurs.\n\n"
                "--- Reply from: Hannah Bergström (2026-04-09 11:00) ---\n"
                "Actually the external monitor IS also flickering now, not just the laptop "
                "screen. I think it might be the docking station after all, not the laptop. "
                "Both my Dell U2722D monitors are affected.\n\n"
                "--- Reply from: Carlos Mendez, Endpoint Support (2026-04-09 09:30) ---\n"
                "Hi Hannah, based on your description this sounds like a display driver issue. "
                "The ThinkPad X1 Carbon Gen 11 had a known Intel Iris Xe driver regression "
                "in the March update. I'll schedule a time to come to your desk and roll back "
                "the driver. The external monitor is probably fine.\n\n"
                "--- Original ticket from: Hannah Bergström (2026-04-08 17:20) ---\n"
                "Hi IT,\n\n"
                "The screen on my ThinkPad X1 Carbon Gen 11 has been flickering intermittently "
                "since this morning. It happens every 5-10 minutes and lasts about 3-4 seconds. "
                "The external monitor connected via my Lenovo USB-C dock seems fine. I'm in "
                "Building 2, Floor 5, desk 5-218. Running Windows 11 23H2.\n\n"
                "Thanks,\nHannah Bergström\nWealth Management"
            ),
            reporter=Reporter(
                name="Hannah Bergström",
                email="hannah.bergstrom@contoso.com",
                department="Wealth Management",
            ),
            created_at="2026-04-08T17:20:00Z",
            channel=Channel.PORTAL,
            attachments=[],
        ),
        gold=GoldAnswer(
            ticket_id="INC-DC-038",
            category=Category.HARDWARE,
            priority=Priority.P3,
            assigned_team=Team.ENDPOINT,
            needs_escalation=False,
            missing_information=[MissingInfoField.DEVICE_INFO, MissingInfoField.STEPS_TO_REPRODUCE],
            next_best_action=(
                "Re-investigate the ThinkPad X1 Carbon Gen 11 screen flickering issue — the "
                "docking station swap did not resolve it, and the symptom has worsened to "
                "full display blackouts. Likely a laptop hardware issue (display cable or GPU) "
                "rather than dock or driver."
            ),
            remediation_steps=[
                "Test the laptop display without any dock connected to isolate the laptop hardware.",
                "Run Lenovo built-in display diagnostics to check for panel or cable faults.",
                "Roll back the Intel Iris Xe driver to the pre-March version to rule out the driver regression.",
                "If the issue persists without dock and with rolled-back drivers, "
                "arrange a hardware repair for the laptop.",
                "Provide a loaner laptop before the client presentation tomorrow.",
            ],
        ),
        tags=["data-cleanup", "contradictory", "email-thread"],
        description=(
            "Email thread with contradictory status updates — marked resolved then reopened — "
            "requiring identification of the latest state."
        ),
    )


def _dc039_accidental_pii() -> EvalCase:
    return EvalCase(
        ticket=EvalTicket(
            ticket_id="INC-DC-039",
            subject="MFA enrollment failing — error with authenticator app",
            description=(
                "Hi Security team,\n\n"
                "I've been trying to enroll in MFA for the new Azure AD Conditional Access "
                "policy that was announced last week, but the enrollment keeps failing. When "
                "I go to https://aka.ms/mfasetup and scan the QR code with Microsoft "
                "Authenticator on my iPhone 15 Pro (iOS 17.4.1), the app shows "
                "'Registration failed — server error' after about 30 seconds.\n\n"
                "Here's my info for troubleshooting:\n"
                "- Employee ID: EMP-204857\n"
                "- UPN: thomas.reeves@contoso.com\n"
                "- Phone: (212) 555-0187\n"
                "- Personal cell (backup): (917) 555-0342\n"
                "- Last 4 of corporate card: 4832\n"
                "- I think my SSN might be in the HR system as 4XX-XX-8891 (I noticed the "
                "enrollment form pre-populated some identity fields and I'm not sure what it "
                "pulled)\n"
                "- Home address: 445 East 86th St, Apt 12C, New York, NY 10028\n\n"
                "I also tried the SMS-based MFA option and entered my phone number but got "
                "'Verification code expired' even though I entered the code within 10 seconds "
                "of receiving it. I attempted enrollment five times total between 8:00 AM and "
                "9:30 AM this morning.\n\n"
                "The deadline to enroll is this Friday and I won't be able to access any "
                "internal systems after that if I don't complete it. Can someone please help "
                "me get this sorted out?\n\n"
                "Thanks,\nThomas Reeves\nClient Relationship Management"
            ),
            reporter=Reporter(
                name="Thomas Reeves",
                email="thomas.reeves@contoso.com",
                department="Client Relationship Management",
            ),
            created_at="2026-04-09T09:45:00Z",
            channel=Channel.EMAIL,
            attachments=[],
        ),
        gold=GoldAnswer(
            ticket_id="INC-DC-039",
            category=Category.ACCESS_AUTH,
            priority=Priority.P2,
            assigned_team=Team.IAM,
            needs_escalation=False,
            missing_information=[MissingInfoField.ERROR_MESSAGE, MissingInfoField.AUTHENTICATION_METHOD],
            next_best_action=(
                "Troubleshoot repeated MFA enrollment failure for thomas.reeves@contoso.com — "
                "both Authenticator app and SMS methods are failing — and flag the ticket for "
                "PII redaction as the user included sensitive personal information."
            ),
            remediation_steps=[
                "Reset the user's MFA registration state in Azure AD to clear any corrupted enrollment data.",
                "Verify the user's phone number is correctly registered in Azure AD for SMS-based MFA.",
                "Attempt enrollment with the user in a screen-share session to observe the exact error.",
                "Check Azure AD MFA server logs for the five failed attempts between 08:00 and 09:30.",
                "Redact the PII (SSN-like pattern, home address, personal phone) from the ticket "
                "and notify the user about safe data practices.",
            ],
        ),
        tags=["data-cleanup", "pii-patterns", "accidental-pii"],
        description=(
            "MFA enrollment ticket containing accidentally included PII-like data (SSN pattern, "
            "home address, personal phone, partial card number)."
        ),
    )


def _dc040_base64_pdf_inline() -> EvalCase:
    return EvalCase(
        ticket=EvalTicket(
            ticket_id="INC-DC-040",
            subject="Report generation failing — pasted the PDF output here",
            description=(
                "Hi Data Platform team,\n\n"
                "The nightly P&L report generation job (job ID: RPT-PNL-DAILY-2026040) has "
                "been failing for the past two nights. The job runs at 02:00 AM EST via "
                "Airflow DAG 'daily_pnl_report' and is supposed to generate a PDF summary "
                "of the trading desk P&L and push it to the compliance SharePoint. On both "
                "April 7th and April 8th, the DAG completed with status 'success' but the "
                "PDF output was corrupt. I tried to open the generated file and got a blank "
                "page. I converted it to base64 to paste it here so you can see the raw data:\n\n"
                "JVBERi0xLjQKMSAwIG9iago8PCAvVHlwZSAvQ2F0YWxvZyAvUGFnZXMgMiAw"
                "IFIgPj4KZW5kb2JqCjIgMCBvYmoKPDwgL1R5cGUgL1BhZ2VzIC9LaWRzIFsz"
                "IDAgUl0gL0NvdW50IDEgPj4KZW5kb2JqCjMgMCBvYmoKPDwgL1R5cGUgL1Bh"
                "Z2UgL1BhcmVudCAyIDAgUiAvTWVkaWFCb3ggWzAgMCA2MTIgNzkyXSAvQ29u"
                "dGVudHMgNCAwIFIgL1Jlc291cmNlcyA8PCAvRm9udCA8PCAvRjEgNSAwIFIg"
                "Pj4gPj4gPj4KZW5kb2JqCjQgMCBvYmoKPDwgL0xlbmd0aCA0NCA+PgpzdHJl"
                "YW0KQlQgL0YxIDI0IFRmIDEwMCAyMDAgVGQgKEhlbGxvIFdvcmxkISkgVGoK"
                "RVQKZW5kc3RyZWFtCmVuZG9iago1IDAgb2JqCjw8IC9UeXBlIC9Gb250IC9T"
                "dWJ0eXBlIC9UeXBlMSAvQmFzZUZvbnQgL0hlbHZldGljYSA+PgplbmRvYmoK"
                "eHJlZgowIDYKMDAwMDAwMDAwMCA2NTUzNSBmIAowMDAwMDAwMDA5IDAwMMDCD"
                "BiBlZmYwMDAwMDAwMDU4IDAwMDAwIG4gCjAwMDAwMDAxMTUgMDAwMDAgbiAK"
                "MDAwMDAwMDMwNiAwMDAwMCBuIAowMDAwMDAwNDAxIDAwMDAwIG4gCnRyYWls"
                "ZXIgPDwgL1NpemUgNiAvUm9vdCAxIDAgUiA+PgpzdGFydHhyZWYKNDkyCiUl"
                "RU9GCg==\n\n"
                "As you can see it's basically a minimal/empty PDF. The actual P&L data is "
                "not making it into the report. I checked the Airflow logs and the upstream "
                "SQL query against the trade_pnl_summary table returns the correct data (I "
                "verified this manually in DBeaver), so the issue is somewhere in the PDF "
                "rendering step. We use ReportLab 4.1.0 for PDF generation. The report "
                "template was last updated on March 28th by our intern — I suspect that "
                "commit may have introduced a regression.\n\n"
                "This is blocking the daily compliance reporting cycle.\n\n"
                "Thanks,\nYuki Tanaka\nData Engineering"
            ),
            reporter=Reporter(
                name="Yuki Tanaka",
                email="yuki.tanaka@contoso.com",
                department="Data Engineering",
            ),
            created_at="2026-04-09T07:15:00Z",
            channel=Channel.EMAIL,
            attachments=[],
        ),
        gold=GoldAnswer(
            ticket_id="INC-DC-040",
            category=Category.DATA_STORAGE,
            priority=Priority.P2,
            assigned_team=Team.DATA_PLATFORM,
            needs_escalation=False,
            missing_information=[MissingInfoField.CONFIGURATION_DETAILS, MissingInfoField.APPLICATION_VERSION],
            next_best_action=(
                "Investigate the nightly P&L report generation failure in Airflow DAG "
                "'daily_pnl_report' — the PDF output is blank despite correct upstream "
                "SQL data — likely a regression in the ReportLab template updated March 28th."
            ),
            remediation_steps=[
                "Review the March 28th commit to the report template for changes that could break PDF rendering.",
                "Compare the ReportLab template before and after the commit using git diff.",
                "Run the DAG manually in a staging environment with debug logging enabled on the PDF generation step.",
                "If the March 28th commit is the root cause, revert it and regenerate "
                "the reports for April 7th and 8th.",
                "Push the regenerated P&L reports to the compliance SharePoint to unblock the reporting cycle.",
            ],
        ),
        tags=["data-cleanup", "base64-pdf", "large-payload"],
        description=(
            "Ticket contains a large base64-encoded PDF blob pasted inline instead of attached, "
            "with the actual report generation issue described around it."
        ),
    )


def _dc041_zalgo_text() -> EvalCase:
    return EvalCase(
        ticket=EvalTicket(
            ticket_id="INC-DC-041",
            subject=(
                "C\u0338\u0321\u0328\u031b\u0309\u0332\u0319\u0326\u031c"
                "\u0317\u032c\u031c\u0319\u0300\u0313\u0304\u0308\u0357"
                "\u0305\u0315o\u0335\u0327\u0322\u031b\u031b\u031d\u0323"
                "\u0326\u0332\u031c\u033a\u0318\u033c\u0309\u0319\u0319"
                "\u0308\u0303\u033e\u0314\u0313\u031am\u0334\u0327\u0322"
                "\u031b\u0324\u032f\u032b\u032f\u0331\u0339\u0323\u0308"
                "\u033d\u0313\u030a\u033f\u030c\u0308\u0315\u035dp\u0336"
                "\u0322\u0327\u0326\u0325\u032b\u032a\u0324\u0319\u0319"
                "\u031d\u030e\u030e\u030a\u0304\u0307\u0306\u0305\u0304"
                "\u031au\u0335\u0327\u0322\u0328\u0328\u0329\u0326\u032d"
                "\u0324\u033a\u0339\u0325\u030a\u030b\u0308\u0306\u030e"
                "\u0308t\u0334\u0321\u0328\u0322\u031c\u0324\u0318\u0324"
                "\u032e\u033b\u032b\u032b\u030d\u030e\u030d\u0302\u0303"
                "\u0314\u0309\u031ae\u0335\u0328\u032c\u0339\u031f\u031d"
                "\u0331\u0326\u0330\u032c\u0311\u030a\u033f\u033f\u0303"
                "\u0308\u033d\u0313\u0306r\u0335\u0321\u0322\u0322\u031b"
                "\u031b\u032b\u0324\u033c\u0317\u032b\u032b\u0308\u0307"
                "\u0308\u030c\u0308\u0351 not working"
            ),
            description=(
                "H\u0335e\u0336l\u0334l\u0335o\u0336 IT support,\n\n"
                "M\u0334y\u0335 l\u0336a\u0334p\u0335t\u0336o\u0334p "
                "i\u0335s\u0336 r\u0334u\u0335n\u0336n\u0334i\u0335n"
                "\u0336g\u0334 extremely slow. The CPU usage is sitting "
                "at 100% constantly and the fans are spinning at full "
                "speed. I can barely open any applications without the "
                "machine freezing for 30-60 seconds. Task Manager shows "
                "a process called 'WMI Provider Host' consuming around "
                "85% CPU. This started after last Tuesday's Windows "
                "update (KB5034441). I've tried rebooting multiple "
                "times but the issue persists.\n\n"
                "I\u0335 n\u0336e\u0334e\u0335d\u0336 t\u0334h\u0335"
                "i\u0336s\u0334 f\u0335i\u0336x\u0334e\u0335d\u0336 "
                "ASAP as I can't do any work.\n\n"
                "Thanks,\nAlex Nowak\nOperations"
            ),
            reporter=Reporter(
                name="Alex Nowak",
                email="alex.nowak@contoso.com",
                department="Operations",
            ),
            created_at="2026-04-10T08:30:00Z",
            channel=Channel.PORTAL,
            attachments=[],
        ),
        gold=GoldAnswer(
            ticket_id="INC-DC-041",
            category=Category.HARDWARE,
            priority=Priority.P3,
            assigned_team=Team.ENDPOINT,
            needs_escalation=False,
            missing_information=[
                MissingInfoField.DEVICE_INFO,
                MissingInfoField.ERROR_MESSAGE,
            ],
            next_best_action=(
                "Investigate high CPU usage caused by WMI Provider Host after "
                "Windows update KB5034441 — determine whether a rollback or "
                "targeted fix is needed."
            ),
            remediation_steps=[
                "Identify the exact laptop model and OS build for compatibility checks.",
                "Review Windows Update history and confirm KB5034441 installation date.",
                "Restart the WMI Provider Host service and monitor CPU usage.",
                "If the issue persists, uninstall KB5034441 and test system stability.",
                "Escalate to Microsoft support if the patch cannot be safely removed.",
            ],
        ),
        tags=["data-cleanup", "zalgo-text", "unicode-combining"],
        description=(
            "Ticket subject and parts of the body contain heavy zalgo-style "
            "combining Unicode diacritics that obscure the actual text."
        ),
    )


def _dc042_url_encoded_content() -> EvalCase:
    return EvalCase(
        ticket=EvalTicket(
            ticket_id="INC-DC-042",
            subject="SharePoint%20access%20denied%20error",
            description=(
                "Hi%20Data%20Platform%20team%2C\n\n"
                "I%20am%20getting%20an%20%22Access%20Denied%22%20error%20when"
                "%20trying%20to%20open%20the%20Q2%20Financial%20Reports"
                "%20folder%20on%20SharePoint%3A\n\n"
                "https%3A%2F%2Fcontoso.sharepoint.com%2Fsites%2Ffinance"
                "%2FShared%2520Documents%2FQ2%2520Reports\n\n"
                "I was able to access this folder last week without any "
                "issues. My colleague jorge.silva%40contoso.com also reports "
                "the same problem. We both have the 'Finance Contributors' "
                "role assigned in the SharePoint admin center.\n\n"
                "The error page shows HTTP 403 and a correlation ID of "
                "b3f7a2c1-8d4e-4f6a-9b2c-1e5f3a7d9c0b. We need access "
                "restored before the end-of-quarter deadline on Friday.\n\n"
                "Thanks%2C\nMariana%20Costa\nFinance"
            ),
            reporter=Reporter(
                name="Mariana Costa",
                email="mariana.costa@contoso.com",
                department="Finance",
            ),
            created_at="2026-04-10T09:45:00Z",
            channel=Channel.EMAIL,
            attachments=[],
        ),
        gold=GoldAnswer(
            ticket_id="INC-DC-042",
            category=Category.DATA_STORAGE,
            priority=Priority.P3,
            assigned_team=Team.DATA_PLATFORM,
            needs_escalation=False,
            missing_information=[
                MissingInfoField.ERROR_MESSAGE,
                MissingInfoField.STEPS_TO_REPRODUCE,
            ],
            next_best_action=(
                "Investigate SharePoint 403 Access Denied error for the Q2 "
                "Financial Reports folder — verify permissions for the "
                "'Finance Contributors' role."
            ),
            remediation_steps=[
                "Check SharePoint audit logs for permission changes on the Q2 Reports folder.",
                "Verify that the 'Finance Contributors' group still has read/write access.",
                "Confirm that no conditional access policy or DLP rule is blocking access.",
                "Restore permissions if they were inadvertently modified and validate access.",
                "Communicate resolution to both affected users before the Friday deadline.",
            ],
        ),
        tags=["data-cleanup", "url-encoded", "percent-encoding"],
        description=(
            "Ticket contains URL-encoded characters (%20, %2F, %3A, %40) "
            "mixed with normal text, obscuring the actual SharePoint access issue."
        ),
    )


def _dc043_monitoring_alert_flood() -> EvalCase:
    return EvalCase(
        ticket=EvalTicket(
            ticket_id="INC-DC-043",
            subject=("FW: FW: FW: [ALERT] [CRITICAL] [PagerDuty] Multiple alerts from monitoring"),
            description=(
                "---------- Forwarded message ----------\n"
                "From: PagerDuty <alerts@pagerduty.contoso.com>\n"
                "Subject: [CRITICAL] db-prod-east-03 connection pool exhausted\n\n"
                "[FIRING] ConnectionPoolExhausted\n"
                "Severity: critical\n"
                "Source: db-prod-east-03.contoso.com:5432\n"
                "Value: 500/500 connections in use\n"
                "Timestamp: 2026-04-10T03:12:44Z\n\n"
                "---------- Forwarded message ----------\n"
                "[FIRING] ConnectionPoolExhausted\n"
                "Severity: critical\n"
                "Source: db-prod-east-03.contoso.com:5432\n"
                "Value: 500/500 connections in use\n"
                "Timestamp: 2026-04-10T03:13:15Z\n\n"
                "---------- Forwarded message ----------\n"
                "[FIRING] HighDatabaseLatency\n"
                "Severity: warning\n"
                "Source: db-prod-east-03.contoso.com:5432\n"
                "Average query time: 12,450ms (threshold: 500ms)\n"
                "Timestamp: 2026-04-10T03:13:30Z\n\n"
                "---------- Forwarded message ----------\n"
                "[FIRING] DiskIOSaturation\n"
                "Severity: warning\n"
                "Source: db-prod-east-03.contoso.com\n"
                "Disk utilization: 98.7%\n"
                "Timestamp: 2026-04-10T03:14:01Z\n\n"
                "Hi team — the above alerts have been firing non-stop since "
                "around 3 AM. The core issue is that our production Postgres "
                "database db-prod-east-03 has completely exhausted its "
                "connection pool (500/500). All downstream services are "
                "timing out. I suspect the new batch ETL job deployed "
                "yesterday is leaking connections.\n\n"
                "— Priya Sharma, SRE"
            ),
            reporter=Reporter(
                name="Priya Sharma",
                email="priya.sharma@contoso.com",
                department="Site Reliability Engineering",
            ),
            created_at="2026-04-10T03:22:00Z",
            channel=Channel.EMAIL,
            attachments=[],
        ),
        gold=GoldAnswer(
            ticket_id="INC-DC-043",
            category=Category.DATA_STORAGE,
            priority=Priority.P2,
            assigned_team=Team.DATA_PLATFORM,
            needs_escalation=True,
            missing_information=[MissingInfoField.ENVIRONMENT_DETAILS],
            next_best_action=(
                "Investigate connection pool exhaustion on db-prod-east-03 — "
                "likely caused by a connection leak in the new batch ETL job "
                "deployed the previous day."
            ),
            remediation_steps=[
                "Identify the new batch ETL job and check for unclosed database connections.",
                "Terminate idle or leaked connections to restore pool availability.",
                "Roll back or disable the suspect ETL job until the leak is fixed.",
                "Monitor connection pool metrics after remediation to confirm stability.",
                "Conduct a post-incident review and add connection-leak guardrails to CI.",
            ],
        ),
        tags=["data-cleanup", "alert-flood", "monitoring-noise"],
        description=(
            "Ticket contains a flood of forwarded PagerDuty/Nagios-style "
            "monitoring alerts with the real issue buried at the end."
        ),
    )


def _dc044_sql_query_dump() -> EvalCase:
    return EvalCase(
        ticket=EvalTicket(
            ticket_id="INC-DC-044",
            subject=("Report query returning wrong numbers \u2014 pasted the SQL here"),
            description=(
                "Hi Data Platform,\n\n"
                "The monthly revenue report is showing numbers that don't "
                "match Finance's figures. Here is the query I'm running:\n\n"
                "WITH monthly_revenue AS (\n"
                "    SELECT\n"
                "        d.fiscal_month,\n"
                "        d.fiscal_year,\n"
                "        p.product_line,\n"
                "        SUM(f.gross_revenue) AS total_gross,\n"
                "        SUM(f.net_revenue) AS total_net,\n"
                "        SUM(f.discount_amount) AS total_discounts\n"
                "    FROM fact_sales f\n"
                "    INNER JOIN dim_date d ON f.date_key = d.date_key\n"
                "    INNER JOIN dim_product p ON f.product_key = p.product_key\n"
                "    INNER JOIN dim_region r ON f.region_key = r.region_key\n"
                "    LEFT JOIN dim_customer c ON f.customer_key = c.customer_key\n"
                "    WHERE d.fiscal_year = 2026\n"
                "      AND d.fiscal_month = 3\n"
                "      AND r.region_name IN ('EMEA', 'APAC', 'AMER')\n"
                "    GROUP BY d.fiscal_month, d.fiscal_year, p.product_line\n"
                ")\n"
                "SELECT\n"
                "    fiscal_month,\n"
                "    fiscal_year,\n"
                "    product_line,\n"
                "    total_gross,\n"
                "    total_net,\n"
                "    total_discounts,\n"
                "    total_gross - total_net AS implied_discounts\n"
                "FROM monthly_revenue\n"
                "ORDER BY product_line;\n\n"
                "The total_discounts column and the implied_discounts "
                "calculation don't match. I think the JOIN to dim_customer "
                "is causing row duplication but I'm not sure. Finance needs "
                "the corrected numbers by end of week.\n\n"
                "Thanks,\nChen Wei\nBusiness Intelligence"
            ),
            reporter=Reporter(
                name="Chen Wei",
                email="chen.wei@contoso.com",
                department="Business Intelligence",
            ),
            created_at="2026-04-10T10:30:00Z",
            channel=Channel.PORTAL,
            attachments=[],
        ),
        gold=GoldAnswer(
            ticket_id="INC-DC-044",
            category=Category.DATA_STORAGE,
            priority=Priority.P3,
            assigned_team=Team.DATA_PLATFORM,
            needs_escalation=False,
            missing_information=[
                MissingInfoField.ENVIRONMENT_DETAILS,
                MissingInfoField.STEPS_TO_REPRODUCE,
            ],
            next_best_action=(
                "Investigate the row-duplication hypothesis in the revenue "
                "report query caused by the LEFT JOIN to dim_customer and "
                "correct the aggregation logic."
            ),
            remediation_steps=[
                "Run the query with and without the dim_customer JOIN and compare row counts.",
                "If duplication is confirmed, refactor the JOIN or use DISTINCT to eliminate it.",
                "Validate corrected figures against Finance's baseline numbers.",
                "Update the report template with the fixed query.",
                "Deliver corrected revenue numbers to Finance before end of week.",
            ],
        ),
        tags=["data-cleanup", "sql-dump", "code-paste"],
        description=(
            "Ticket contains a large multi-line SQL query pasted inline, "
            "with the actual issue (incorrect aggregation) described around it."
        ),
    )


def _dc045_certificate_leak() -> EvalCase:
    return EvalCase(
        ticket=EvalTicket(
            ticket_id="INC-DC-045",
            subject="SSL certificate expired on api.contoso.com",
            description=(
                "Hi Security team,\n\n"
                "The TLS certificate for api.contoso.com expired today and "
                "all API consumers are getting certificate warnings. Here "
                "are the cert details — I pulled them from the server so "
                "you can see:\n\n"
                "-----BEGIN CERTIFICATE-----\n"
                "MIIFtTCCA52gAwIBAgIUY3mDf7c0Rf4x2bK9L8aN4gRzJjowDQYJ"
                "KoZIhvcNAQELBQAwYjELMAkGA1UEBhMCVVMxEzARBgNVBAgMCldh"
                "c2hpbmd0b24xEDAOBgNVBAcMB1JlZG1vbmQxEDAOBgNVBAoMB0Nv"
                "bnRvc28xGjAYBgNVBAMMEWFwaS5jb250b3NvLmNvbTAeFw0yNTA0"
                "FAKE_CERT_DATA_REDACTED_FOR_SAFETY\n"
                "-----END CERTIFICATE-----\n\n"
                "-----BEGIN RSA PRIVATE KEY-----\n"
                "MIIEowIBAAKCAQEA0Z3VS5JJcds3xfn/ygWep4PAtGoRBh1MLa0x"
                "FAKE_PRIVATE_KEY_DATA_REDACTED_FOR_SAFETY\n"
                "-----END RSA PRIVATE KEY-----\n\n"
                "I probably shouldn't have pasted the private key but it's "
                "expiring anyway so it should be fine. The cert needs to be "
                "renewed and redeployed to the F5 load balancer and the "
                "three API gateway nodes (api-gw-01 through api-gw-03). "
                "Our cert provider is DigiCert and the renewal process "
                "usually takes about 2 hours.\n\n"
                "— David Kim, Platform Engineering"
            ),
            reporter=Reporter(
                name="David Kim",
                email="david.kim@contoso.com",
                department="Platform Engineering",
            ),
            created_at="2026-04-10T06:00:00Z",
            channel=Channel.EMAIL,
            attachments=[],
        ),
        gold=GoldAnswer(
            ticket_id="INC-DC-045",
            category=Category.SECURITY,
            priority=Priority.P2,
            assigned_team=Team.SECURITY_OPS,
            needs_escalation=True,
            missing_information=[MissingInfoField.CONFIGURATION_DETAILS],
            next_best_action=(
                "Immediately revoke the exposed private key, renew the TLS "
                "certificate for api.contoso.com via DigiCert, and redeploy "
                "to the F5 load balancer and API gateway nodes."
            ),
            remediation_steps=[
                "Revoke the compromised private key immediately via DigiCert.",
                "Generate a new CSR and request a replacement certificate.",
                "Deploy the new certificate to the F5 load balancer and api-gw-01 through api-gw-03.",
                "Verify TLS connectivity from external and internal clients.",
                "Purge the private key material from this ticket and audit access logs.",
            ],
        ),
        tags=["data-cleanup", "credential-leak", "pii", "certificate"],
        description=(
            "Ticket contains accidentally pasted private key and certificate "
            "material inline alongside a legitimate SSL renewal request."
        ),
    )


def _dc046_hex_dump() -> EvalCase:
    return EvalCase(
        ticket=EvalTicket(
            ticket_id="INC-DC-046",
            subject=("File corruption issue \u2014 hex dump attached inline"),
            description=(
                "Hi team,\n\n"
                "We're seeing file corruption on the \\\\nas-prod-02\\finance "
                "share. Several Excel files are unreadable. I ran hexdump "
                "on one of the corrupt files:\n\n"
                "00000000  50 4b 03 04 14 00 06 00  08 00 00 00 21 00 62 ee  "
                "|PK..........!.b.|\n"
                "00000010  9d ad 46 01 00 00 51 04  00 00 13 00 08 02 5b 43  "
                "|..F...Q.......[C|\n"
                "00000020  6f 6e 74 65 6e 74 5f 54  79 70 65 73 5d 2e 78 6d  "
                "|ontent_Types].xm|\n"
                "00000030  6c 20 a2 04 02 28 a0 00  02 00 00 00 00 00 00 00  "
                "|l ...(..........|\n"
                "00000040  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  "
                "|................|\n"
                "*\n"
                "00000060  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  "
                "|................|\n\n"
                "As you can see, the file starts as a valid ZIP/XLSX but the "
                "content is zeroed out after the header. This has happened to "
                "at least 12 files in the past week. All affected files are "
                "on the same NAS volume. Users from Accounting and Treasury "
                "have reported the problem.\n\n"
                "Thanks,\nOliver Grant\nIT Infrastructure"
            ),
            reporter=Reporter(
                name="Oliver Grant",
                email="oliver.grant@contoso.com",
                department="IT Infrastructure",
            ),
            created_at="2026-04-10T11:20:00Z",
            channel=Channel.PORTAL,
            attachments=[],
        ),
        gold=GoldAnswer(
            ticket_id="INC-DC-046",
            category=Category.DATA_STORAGE,
            priority=Priority.P3,
            assigned_team=Team.DATA_PLATFORM,
            needs_escalation=False,
            missing_information=[
                MissingInfoField.AFFECTED_SYSTEM,
                MissingInfoField.REPRODUCTION_FREQUENCY,
            ],
            next_best_action=(
                "Investigate file corruption on the nas-prod-02 finance "
                "share — files are being zeroed out after valid headers, "
                "suggesting a storage or firmware issue."
            ),
            remediation_steps=[
                "Run a filesystem integrity check on the affected NAS volume.",
                "Review NAS firmware version and check vendor advisories for known bugs.",
                "Examine NAS event logs for disk errors, RAID rebuild events, or write failures.",
                "Restore the corrupted files from the most recent verified backup.",
                "If firmware is outdated, schedule a maintenance window for the update.",
            ],
        ),
        tags=["data-cleanup", "hex-dump", "binary-data"],
        description=(
            "Ticket contains hexdump -C style output pasted inline, "
            "with the actual file corruption issue described around it."
        ),
    )


def _dc047_mixed_date_formats() -> EvalCase:
    return EvalCase(
        ticket=EvalTicket(
            ticket_id="INC-DC-047",
            subject="Meeting room booking system shows wrong dates",
            description=(
                "Hi Enterprise Apps team,\n\n"
                "The meeting room booking system is displaying incorrect "
                "dates for several of our offices. Here are examples of "
                "what different users are seeing:\n\n"
                "- London office: Booking created 10/04/2026 shows as "
                "April 10th (should be 10th April in DD/MM format)\n"
                "- New York office: Same booking shows as 10/04/2026 and "
                "they read it as October 4th\n"
                "- Tokyo office: Booking displays as 2026-04-10 which is "
                "correct but the confirmation email says 04-Apr-26\n"
                "- Mumbai office: Calendar export shows epoch 1775865600 "
                "which converts to a different date entirely\n"
                "- Berlin office: The iCal attachment uses DTSTART:"
                "20260410T090000Z but the UI shows 11:00 local time "
                "instead of 10:00\n\n"
                "We have a board meeting on what I believe is April 10th "
                "(or is it October 4th?) and rooms keep getting double-"
                "booked because of this confusion. Multiple executives "
                "have complained.\n\n"
                "Thanks,\nSophie Martin\nExecutive Administration"
            ),
            reporter=Reporter(
                name="Sophie Martin",
                email="sophie.martin@contoso.com",
                department="Executive Administration",
            ),
            created_at="2026-04-10T12:00:00Z",
            channel=Channel.EMAIL,
            attachments=[],
        ),
        gold=GoldAnswer(
            ticket_id="INC-DC-047",
            category=Category.SOFTWARE,
            priority=Priority.P4,
            assigned_team=Team.ENTERPRISE_APPS,
            needs_escalation=False,
            missing_information=[
                MissingInfoField.STEPS_TO_REPRODUCE,
                MissingInfoField.TIMESTAMP,
            ],
            next_best_action=(
                "Investigate locale-dependent date formatting inconsistencies "
                "in the meeting room booking system across international offices."
            ),
            remediation_steps=[
                "Audit the booking system's date formatting logic for locale handling.",
                "Standardize date storage to ISO 8601 (YYYY-MM-DD) internally.",
                "Ensure the UI renders dates according to each user's locale preference.",
                "Fix the timezone offset error in the iCal export for Berlin.",
                "Verify the epoch timestamp conversion logic for the Mumbai office export.",
            ],
        ),
        tags=["data-cleanup", "date-format", "locale-confusion"],
        description=(
            "Ticket contains dates in multiple conflicting formats "
            "(MM/DD, DD/MM, ISO 8601, epoch, iCal) causing ambiguity."
        ),
    )


def _dc048_financial_ticker_confusion() -> EvalCase:
    return EvalCase(
        ticket=EvalTicket(
            ticket_id="INC-DC-048",
            subject=("Bloomberg terminal showing $AAPL instead of correct ticker for Contoso fund"),
            description=(
                "Hi Enterprise Apps,\n\n"
                "We have a data feed mapping error on the Bloomberg "
                "terminal. When pulling up the Contoso Growth Fund, the "
                "terminal is returning Apple Inc. data instead:\n\n"
                "Terminal query: CONGROW US Equity <GO>\n"
                "Expected: Contoso Growth Fund (CUSIP: 21076N106, "
                "ISIN: US21076N1063)\n"
                "Actual: Apple Inc (AAPL US Equity, CUSIP: 037833100, "
                "ISIN: US0378331005)\n\n"
                "The Bloomberg FLDS screen shows:\n"
                "  ID_BB_GLOBAL: BBG000B9XRY4 (this is Apple's FIGI)\n"
                "  TICKER: AAPL\n"
                "  MARKET_SECTOR_DES: Equity\n"
                "  ID_CUSIP: 037833100\n\n"
                "Our fund's correct FIGI should be BBG00Z1Y3XQ7. It "
                "looks like someone updated the security master file "
                "and mapped the wrong FIGI to our fund ticker. The "
                "portfolio managers are seeing incorrect NAV calculations "
                "as a result.\n\n"
                "— Raj Patel, Portfolio Analytics"
            ),
            reporter=Reporter(
                name="Raj Patel",
                email="raj.patel@contoso.com",
                department="Portfolio Analytics",
            ),
            created_at="2026-04-10T13:15:00Z",
            channel=Channel.EMAIL,
            attachments=[],
        ),
        gold=GoldAnswer(
            ticket_id="INC-DC-048",
            category=Category.SOFTWARE,
            priority=Priority.P2,
            assigned_team=Team.ENTERPRISE_APPS,
            needs_escalation=False,
            missing_information=[
                MissingInfoField.CONFIGURATION_DETAILS,
                MissingInfoField.APPLICATION_VERSION,
            ],
            next_best_action=(
                "Correct the FIGI mapping in the security master file — "
                "the Contoso Growth Fund ticker is mapped to Apple's "
                "FIGI (BBG000B9XRY4) instead of BBG00Z1Y3XQ7."
            ),
            remediation_steps=[
                "Identify who last modified the security master file and review the change.",
                "Correct the FIGI mapping for CONGROW from BBG000B9XRY4 to BBG00Z1Y3XQ7.",
                "Revalidate the CUSIP and ISIN mappings for all recently modified entries.",
                "Recalculate NAV for any affected reporting periods with the corrected data.",
                "Add a validation check to flag FIGI mismatches during future master file updates.",
            ],
        ),
        tags=["data-cleanup", "financial-data", "ticker-symbols"],
        description=(
            "Ticket contains financial ticker symbols, Bloomberg codes, "
            "CUSIP and ISIN identifiers mixed with the actual data feed "
            "mapping error."
        ),
    )


def _dc049_tcpdump_output() -> EvalCase:
    return EvalCase(
        ticket=EvalTicket(
            ticket_id="INC-DC-049",
            subject=("Network latency issue \u2014 tcpdump output attached"),
            description=(
                "Hi Network Ops,\n\n"
                "We're experiencing high latency on internal DNS queries. "
                "I captured some packets to show the problem:\n\n"
                "14:32:01.234567 IP 10.1.5.42.51234 > 10.1.1.10.53: "
                "12345+ A? app.internal.contoso.com. (45)\n"
                "14:32:04.567890 IP 10.1.1.10.53 > 10.1.5.42.51234: "
                "12345 3/0/0 A 10.2.3.100, A 10.2.3.101, A 10.2.3.102 (93)\n"
                "14:32:04.568123 IP 10.1.5.42.51235 > 10.1.1.10.53: "
                "12346+ AAAA? app.internal.contoso.com. (45)\n"
                "14:32:07.891456 IP 10.1.1.10.53 > 10.1.5.42.51235: "
                "12346 0/1/0 (87)\n"
                "14:32:07.892001 IP 10.1.5.42.41567 > 10.1.1.11.53: "
                "12347+ A? auth.internal.contoso.com. (44)\n"
                "14:32:10.123789 IP 10.1.1.11.53 > 10.1.5.42.41567: "
                "12347 1/0/0 A 10.2.4.50 (60)\n\n"
                "As you can see, DNS responses are taking 3+ seconds "
                "instead of the normal <10ms. This is affecting all "
                "applications on the 10.1.5.0/24 subnet. The DNS servers "
                "10.1.1.10 and 10.1.1.11 are both slow. Started around "
                "2 PM today after a firewall rule change.\n\n"
                "— Lisa Chen, DevOps"
            ),
            reporter=Reporter(
                name="Lisa Chen",
                email="lisa.chen@contoso.com",
                department="DevOps",
            ),
            created_at="2026-04-10T14:45:00Z",
            channel=Channel.PORTAL,
            attachments=[],
        ),
        gold=GoldAnswer(
            ticket_id="INC-DC-049",
            category=Category.NETWORK,
            priority=Priority.P2,
            assigned_team=Team.NETWORK_OPS,
            needs_escalation=False,
            missing_information=[MissingInfoField.NETWORK_LOCATION],
            next_best_action=(
                "Investigate high DNS query latency on the 10.1.5.0/24 "
                "subnet — likely caused by the firewall rule change "
                "deployed around 2 PM today."
            ),
            remediation_steps=[
                "Review the firewall rule change made around 2 PM and identify DNS-related rules.",
                "Check whether DNS traffic (port 53) is being inspected or rate-limited by the new rules.",
                "Roll back the suspect firewall rule and measure DNS response times.",
                "Verify DNS forwarder and recursion settings on 10.1.1.10 and 10.1.1.11.",
                "Monitor DNS latency across all subnets after remediation to confirm resolution.",
            ],
        ),
        tags=["data-cleanup", "tcpdump", "packet-capture"],
        description=(
            "Ticket contains raw tcpdump output with timestamps, IPs, "
            "and packet details pasted inline alongside the DNS latency issue."
        ),
    )


def _dc050_screen_reader_artifacts() -> EvalCase:
    return EvalCase(
        ticket=EvalTicket(
            ticket_id="INC-DC-050",
            subject=(
                "Button Image link Image ARIA: navigation Banner: main content Heading level 2: Can't access portal"
            ),
            description=(
                "navigation landmark Banner landmark main landmark "
                "Heading level 1: Contoso Self-Service Portal\n"
                "link Image: Contoso Logo\n"
                "navigation: Main Menu\n"
                "list 5 items\n"
                "  link: Home\n"
                "  link: My Tickets\n"
                "  link: Knowledge Base\n"
                "  link: Service Catalog\n"
                "  link: Contact Us\n"
                "end of list\n"
                "end of navigation\n"
                "Heading level 2: Sign In\n"
                "textbox: Username — edit text: jmendez\n"
                "textbox: Password — edit text: (protected)\n"
                "button: Sign In\n"
                "alert: Error — Authentication failed. Your account "
                "may be locked. Contact IT support.\n"
                "end of main landmark\n"
                "contentinfo landmark\n"
                "link: Privacy Policy\n"
                "link: Terms of Use\n\n"
                "Hi I am using a screen reader and I copied the above "
                "from my browser to show you what's happening. When I "
                "try to sign in to the self-service portal I get the "
                "error that my account may be locked. I haven't changed "
                "my password recently and I was able to log in yesterday. "
                "I need access to submit a facilities request urgently.\n\n"
                "Thanks,\nJulia Mendez\nFacilities Management"
            ),
            reporter=Reporter(
                name="Julia Mendez",
                email="julia.mendez@contoso.com",
                department="Facilities Management",
            ),
            created_at="2026-04-10T15:30:00Z",
            channel=Channel.PORTAL,
            attachments=[],
        ),
        gold=GoldAnswer(
            ticket_id="INC-DC-050",
            category=Category.ACCESS_AUTH,
            priority=Priority.P3,
            assigned_team=Team.IAM,
            needs_escalation=False,
            missing_information=[
                MissingInfoField.ERROR_MESSAGE,
                MissingInfoField.DEVICE_INFO,
            ],
            next_best_action=(
                "Investigate account lockout for julia.mendez on the "
                "self-service portal — verify Active Directory lock "
                "status and recent authentication events."
            ),
            remediation_steps=[
                "Check Active Directory for account lockout status on julia.mendez.",
                "Review authentication logs for failed login attempts or suspicious activity.",
                "Unlock the account if it was locked due to failed password attempts.",
                "Verify that no recent password policy changes caused the lockout.",
                "Confirm the user can sign in successfully and submit her facilities request.",
            ],
        ),
        tags=["data-cleanup", "screen-reader", "accessibility-artifacts"],
        description=(
            "Ticket contains accessibility tree and screen reader output "
            "artifacts from the DOM mixed with a portal login issue."
        ),
    )


def _dc051_graphql_introspection_dump() -> EvalCase:
    """GraphQL introspection query response dumped into ticket description."""
    return EvalCase(
        ticket=EvalTicket(
            ticket_id="INC-DC-051",
            subject="Cannot access shared folder in SharePoint — permissions error",
            description=(
                "Hi,\n\n"
                "I'm unable to access the Q1 Earnings Reports folder on SharePoint. "
                "I get a 403 Forbidden error. I ran a GraphQL query against our internal "
                "API to check my permissions, and here's the full introspection response:\n\n"
                '{"data":{"__schema":{"queryType":{"name":"Query"},"mutationType":{"name":"Mutation"},'
                '"subscriptionType":null,"types":[{"kind":"OBJECT","name":"Query","description":null,'
                '"fields":[{"name":"user","description":"Fetch user by ID","args":[{"name":"id",'
                '"description":null,"type":{"kind":"NON_NULL","name":null,"ofType":{"kind":"SCALAR",'
                '"name":"ID","ofType":null}},"defaultValue":null}],"type":{"kind":"OBJECT",'
                '"name":"User","ofType":null},"isDeprecated":false,"deprecationReason":null},'
                '{"name":"permissions","description":"List permissions for a resource","args":'
                '[{"name":"resourceId","description":null,"type":{"kind":"NON_NULL","name":null,'
                '"ofType":{"kind":"SCALAR","name":"String","ofType":null}},"defaultValue":null}],'
                '"type":{"kind":"LIST","name":null,"ofType":{"kind":"OBJECT","name":"Permission",'
                '"ofType":null}},"isDeprecated":false,"deprecationReason":null},{"name":"sharePointSite",'
                '"description":"Get SharePoint site metadata","args":[{"name":"siteUrl","type":'
                '{"kind":"NON_NULL","name":null,"ofType":{"kind":"SCALAR","name":"String","ofType":'
                'null}}}],"type":{"kind":"OBJECT","name":"SharePointSite","ofType":null},'
                '"isDeprecated":false,"deprecationReason":null}],"inputFields":null,"interfaces":[],'
                '"enumValues":null,"possibleTypes":null},{"kind":"OBJECT","name":"User","description":'
                '"A user in the directory","fields":[{"name":"id","args":[],"type":{"kind":"NON_NULL",'
                '"name":null,"ofType":{"kind":"SCALAR","name":"ID","ofType":null}}},{"name":"email",'
                '"args":[],"type":{"kind":"SCALAR","name":"String","ofType":null}},{"name":"groups",'
                '"args":[],"type":{"kind":"LIST","name":null,"ofType":{"kind":"OBJECT","name":"Group",'
                '"ofType":null}}}],"inputFields":null,"interfaces":[],"enumValues":null,'
                '"possibleTypes":null}]}}}}\n\n'
                "As you can see, I should have the 'Contributor' role on that site but it "
                "seems like my group membership isn't propagating. Can you check?\n\n"
                "Thanks,\nRobert Kim\nEquity Research"
            ),
            reporter=Reporter(
                name="Robert Kim",
                email="robert.kim@contoso.com",
                department="Equity Research",
            ),
            created_at="2026-03-17T10:30:00Z",
            channel=Channel.PORTAL,
            attachments=[],
        ),
        gold=GoldAnswer(
            ticket_id="INC-DC-051",
            category=Category.DATA_STORAGE,
            priority=Priority.P3,
            assigned_team=Team.DATA_PLATFORM,
            needs_escalation=False,
            missing_information=[MissingInfoField.ERROR_MESSAGE],
            next_best_action=(
                "Check the reporter's SharePoint group membership and permissions "
                "for the Q1 Earnings Reports folder. Verify that group membership "
                "changes have propagated through Azure AD."
            ),
            remediation_steps=[
                "Verify the reporter's Azure AD group memberships include the appropriate SharePoint group.",
                "Check if there is a sync delay between Azure AD and SharePoint Online.",
                "If permissions are correct, investigate whether a conditional access policy is blocking access.",
                "Grant the reporter explicit access to the folder as a temporary workaround.",
            ],
        ),
        tags=["data-cleanup", "graphql_dump", "schema_noise", "json_payload"],
        description=(
            "Tests handling of a massive GraphQL introspection JSON response embedded in the ticket description."
        ),
    )


def _dc052_windows_minidump_output() -> EvalCase:
    """Windows BSOD minidump with hex addresses and register states."""
    return EvalCase(
        ticket=EvalTicket(
            ticket_id="INC-DC-052",
            subject="Laptop blue screens twice daily — DRIVER_IRQL_NOT_LESS_OR_EQUAL",
            description=(
                "My ThinkPad X1 Carbon keeps crashing with a blue screen. It happens about "
                "twice a day, usually when I have Teams, Bloomberg, and Excel open. I managed "
                "to capture the minidump output from WinDbg:\n\n"
                "Microsoft (R) Windows Debugger Version 10.0.22621.1 AMD64\n"
                "Copyright (c) Microsoft Corporation. All rights reserved.\n\n"
                "Loading Dump File [C:\\Windows\\Minidump\\031726-15890-01.dmp]\n"
                "Mini Kernel Dump File: Only registers and stack trace are available\n\n"
                "*******************************************************************************\n"
                "*                                                                             *\n"
                "*                        Bugcheck Analysis                                    *\n"
                "*                                                                             *\n"
                "*******************************************************************************\n\n"
                "DRIVER_IRQL_NOT_LESS_OR_EQUAL (d1)\n"
                "An attempt was made to access a pageable (or completely invalid) address at an\n"
                "interrupt request level (IRQL) that is too high.\n"
                "Arguments:\n"
                "Arg1: ffffab0812345678, memory referenced\n"
                "Arg2: 0000000000000002, IRQL\n"
                "Arg3: 0000000000000000, value 0 = read operation, 1 = write operation\n"
                "Arg4: fffff80712a4b230, address which referenced memory\n\n"
                "CONTEXT:  ffffab08123c0000 -- (.cxr 0xffffab08123c0000)\n"
                "rax=0000000000000000 rbx=ffffab0812340100 rcx=ffffab0812345678\n"
                "rdx=0000000000000000 rsi=fffff80712a4b000 rdi=ffffab08123d0000\n"
                "rip=fffff80712a4b230 rsp=ffffab08123bfe00 rbp=ffffab08123bfe80\n"
                " r8=0000000000000002  r9=0000000000000000 r10=fffff80700000000\n"
                "r11=ffffab08123bfd50 r12=0000000000000000 r13=ffffab08123e0000\n"
                "r14=fffff80712a00000 r15=0000000000000001\n"
                "iopl=0         nv up ei pl zr na po nc\n"
                "cs=0010  ss=0018  ds=002b  es=002b  fs=0053  gs=002b\n\n"
                "STACK_TEXT:\n"
                "ffffab08`123bfe00 fffff807`12a4b230 : ndis!NdisMIndicateReceiveNetBufferLists+0x120\n"
                "ffffab08`123bfe80 fffff807`0fa23100 : tcpip!FlReceiveNetBufferListChain+0x200\n"
                "ffffab08`123bff00 fffff807`0fa1e450 : tcpip!IppReceiveHeaderBatch+0x310\n"
                "ffffab08`123bff80 fffff807`0f8a1230 : NETIO!NetioCompleteCloneNetBufferListChain+0x1a0\n"
                "ffffab08`123c0000 fffff807`0060a4c0 : nt!KiPageFault+0x370\n\n"
                "MODULE_NAME: ndis\n"
                "IMAGE_NAME:  ndis.sys\n"
                "FAILURE_BUCKET_ID:  AV_ndis!NdisMIndicateReceiveNetBufferLists\n\n"
                "Can you please help? This is seriously impacting my work.\n"
                "Mark Jensen, Fixed Income Trading"
            ),
            reporter=Reporter(
                name="Mark Jensen",
                email="mark.jensen@contoso.com",
                department="Fixed Income Trading",
            ),
            created_at="2026-03-17T14:22:00Z",
            channel=Channel.EMAIL,
            attachments=["031726-15890-01.dmp"],
        ),
        gold=GoldAnswer(
            ticket_id="INC-DC-052",
            category=Category.HARDWARE,
            priority=Priority.P2,
            assigned_team=Team.ENDPOINT,
            needs_escalation=False,
            missing_information=[MissingInfoField.DEVICE_INFO, MissingInfoField.APPLICATION_VERSION],
            next_best_action=(
                "Investigate recurring BSOD (DRIVER_IRQL_NOT_LESS_OR_EQUAL) on the reporter's "
                "ThinkPad X1 Carbon. The crash is in ndis.sys, suggesting a network driver issue."
            ),
            remediation_steps=[
                "Collect the full minidump file and analyze with WinDbg for root cause.",
                "Update the network adapter driver (ndis.sys crash points to NIC driver issue).",
                "Check if a recent Windows or Intune update changed network stack components.",
                "If driver updates don't resolve, schedule hardware diagnostics to check NIC.",
                "Provide a loaner device if crashes continue to impact trading operations.",
            ],
        ),
        tags=["data-cleanup", "minidump", "crash_dump", "hex_addresses", "debug_output"],
        description=(
            "Tests handling of Windows BSOD minidump output with hex addresses, "
            "register states, and kernel stack traces."
        ),
    )


def _dc053_webhook_payload_noise() -> EvalCase:
    """Multiple webhook notification payloads filling the description."""
    return EvalCase(
        ticket=EvalTicket(
            ticket_id="INC-DC-053",
            subject="Teams connector not posting build notifications",
            description=(
                "Our Teams channel stopped receiving build notifications from the CI/CD pipeline. "
                "I checked the webhook endpoint and it seems to be returning errors. Here are the "
                "last several payloads that were attempted:\n\n"
                "POST https://contoso.webhook.office.com/webhookb2/7a8b9c0d-1e2f-3a4b-5c6d-7e8f9a0b1c2d\n"
                "Content-Type: application/json\n\n"
                '{"@type":"MessageCard","@context":"http://schema.org/extensions","themeColor":"FF0000",'
                '"summary":"Build Failed: trading-engine #4521","sections":[{"activityTitle":"Build '
                'Failed","activitySubtitle":"trading-engine #4521","activityImage":"https://ci.contoso'
                '.com/img/fail.png","facts":[{"name":"Branch","value":"release/v2.4.1"},{"name":"Commit",'
                '"value":"a1b2c3d4e5f6"},{"name":"Author","value":"Sarah.Chen@contoso.com"},{"name":'
                '"Duration","value":"12m 34s"},{"name":"Failed Stage","value":"integration-tests"},'
                '{"name":"Error","value":"Connection timeout to market-data-service:8443"}],"markdown":'
                'true}],"potentialAction":[{"@type":"OpenUri","name":"View Build","targets":[{"os":'
                '"default","uri":"https://ci.contoso.com/builds/4521"}]}]}\n\n'
                "---\n\n"
                "HTTP/1.1 400 Bad Request\n"
                '{"error":{"code":"WebhookUrlNotFound","message":"The webhook URL was not found or '
                'has been removed.","innerError":{"date":"2026-03-17T09:15:32","request-id":'
                '"4a5b6c7d-8e9f-0a1b-2c3d-4e5f6a7b8c9d"}}}\n\n'
                "This has been happening since yesterday morning. We rely on these notifications for "
                "release coordination. Can someone check if the Teams connector was deleted or expired?\n\n"
                "Jason Park, DevOps Engineering"
            ),
            reporter=Reporter(
                name="Jason Park",
                email="jason.park@contoso.com",
                department="DevOps Engineering",
            ),
            created_at="2026-03-17T09:30:00Z",
            channel=Channel.CHAT,
            attachments=[],
        ),
        gold=GoldAnswer(
            ticket_id="INC-DC-053",
            category=Category.SOFTWARE,
            priority=Priority.P3,
            assigned_team=Team.ENTERPRISE_APPS,
            needs_escalation=False,
            missing_information=[MissingInfoField.CONFIGURATION_DETAILS],
            next_best_action=(
                "Investigate the Teams connector webhook returning WebhookUrlNotFound errors. "
                "The connector may have been deleted or the webhook URL may have expired."
            ),
            remediation_steps=[
                "Check if the Teams connector for the channel is still active in Teams admin.",
                "Verify the webhook URL has not expired (connectors have a limited lifespan).",
                "If the connector was removed, recreate it and update the CI/CD pipeline config.",
                "Test the new webhook URL with a manual POST request to confirm it works.",
            ],
        ),
        tags=["data-cleanup", "webhook_payload", "connector_noise", "json_payload"],
        description=(
            "Tests handling of multiple webhook notification JSON payloads "
            "and HTTP request/response dumps in the description."
        ),
    )


def _dc054_powershell_mixed_streams() -> EvalCase:
    """PowerShell verbose/debug/error/warning streams interleaved."""
    return EvalCase(
        ticket=EvalTicket(
            ticket_id="INC-DC-054",
            subject="Automated deployment script failing on production servers",
            description=(
                "Our nightly deployment script is failing. Here's the full PowerShell output "
                "with all streams enabled:\n\n"
                "VERBOSE: [2026-03-17 02:00:01] Starting deployment pipeline v3.2.1\n"
                "VERBOSE: [2026-03-17 02:00:01] Connecting to deployment server prod-deploy-01.contoso.com\n"
                "VERBOSE: [2026-03-17 02:00:02] Authentication successful via managed identity\n"
                "VERBOSE: [2026-03-17 02:00:02] Loading deployment manifest from "
                "\\\\fileserver\\deploys\\manifest.json\n"
                "DEBUG: Manifest hash: SHA256:a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6\n"
                "DEBUG: Target servers: [prod-app-01, prod-app-02, prod-app-03, prod-app-04]\n"
                "VERBOSE: [2026-03-17 02:00:03] Phase 1: Pre-deployment health checks\n"
                "VERBOSE: [2026-03-17 02:00:03] Checking prod-app-01... OK\n"
                "VERBOSE: [2026-03-17 02:00:04] Checking prod-app-02... OK\n"
                "WARNING: prod-app-03 disk space below 15% threshold (12.4% free)\n"
                "VERBOSE: [2026-03-17 02:00:05] Checking prod-app-04... OK\n"
                "VERBOSE: [2026-03-17 02:00:06] Phase 2: Stopping application pools\n"
                "VERBOSE: [2026-03-17 02:00:06] Stopping TradingEngine pool on prod-app-01\n"
                "VERBOSE: [2026-03-17 02:00:07] Stopping TradingEngine pool on prod-app-02\n"
                "ERROR: Failed to stop application pool 'TradingEngine' on prod-app-03\n"
                "ERROR: Exception: System.Runtime.InteropServices.COMException (0x80070005)\n"
                "ERROR:    Access is denied.\n"
                "ERROR:    at Microsoft.Web.Administration.Interop.IAppHostProperty.set_Value(Object value)\n"
                "ERROR:    at Deploy-Application.ps1:line 247\n"
                "WARNING: Deployment aborted due to errors. Rolling back changes.\n"
                "VERBOSE: [2026-03-17 02:00:08] Rolling back prod-app-01... done\n"
                "VERBOSE: [2026-03-17 02:00:09] Rolling back prod-app-02... done\n"
                "VERBOSE: [2026-03-17 02:00:10] Rollback complete. No servers were updated.\n\n"
                "The script has been working fine for months. I think the service account password "
                "was changed and not updated in our deployment config.\n\n"
                "Amit Patel, Platform Engineering"
            ),
            reporter=Reporter(
                name="Amit Patel",
                email="amit.patel@contoso.com",
                department="Platform Engineering",
            ),
            created_at="2026-03-17T06:15:00Z",
            channel=Channel.EMAIL,
            attachments=["deploy-log-20260317.txt"],
        ),
        gold=GoldAnswer(
            ticket_id="INC-DC-054",
            category=Category.SOFTWARE,
            priority=Priority.P2,
            assigned_team=Team.ENTERPRISE_APPS,
            needs_escalation=False,
            missing_information=[MissingInfoField.AUTHENTICATION_METHOD, MissingInfoField.CONFIGURATION_DETAILS],
            next_best_action=(
                "Investigate the Access Denied error when stopping the TradingEngine application "
                "pool on prod-app-03. Likely a service account credential issue."
            ),
            remediation_steps=[
                "Verify the deployment service account credentials are current and not expired.",
                "Check if a recent password rotation affected the managed identity or service account.",
                "Test the service account permissions on prod-app-03 specifically.",
                "Update the deployment configuration with the new credentials if changed.",
                "Re-run the deployment script and monitor for successful completion.",
            ],
        ),
        tags=["data-cleanup", "powershell_streams", "mixed_output", "deployment_log"],
        description=(
            "Tests handling of PowerShell verbose/debug/error/warning streams interleaved in the ticket description."
        ),
    )


def _dc055_docker_compose_flood() -> EvalCase:
    """Multiple docker-compose.yml configurations dumped in description."""
    return EvalCase(
        ticket=EvalTicket(
            ticket_id="INC-DC-055",
            subject="Trading platform containers failing to start after update",
            description=(
                "After the platform update last night, our containerised trading services won't start. "
                "Here are the relevant docker-compose files:\n\n"
                "# docker-compose.trading.yml\n"
                "version: '3.8'\n"
                "services:\n"
                "  order-gateway:\n"
                "    image: contoso.azurecr.io/trading/order-gateway:2.4.1\n"
                "    ports:\n"
                "      - '8443:8443'\n"
                "    environment:\n"
                "      - MARKET_DATA_URL=https://market-data.internal:9443\n"
                "      - FIX_ENGINE_HOST=fix-engine\n"
                "      - FIX_ENGINE_PORT=9878\n"
                "      - DB_CONNECTION=Server=sql-prod-01;Database=TradingDB;Trusted_Connection=true\n"
                "    depends_on:\n"
                "      - fix-engine\n"
                "      - market-data\n"
                "    deploy:\n"
                "      resources:\n"
                "        limits:\n"
                "          cpus: '4.0'\n"
                "          memory: 8G\n"
                "    healthcheck:\n"
                "      test: ['CMD', 'curl', '-f', 'http://localhost:8443/health']\n"
                "      interval: 10s\n"
                "      timeout: 5s\n"
                "      retries: 3\n\n"
                "  fix-engine:\n"
                "    image: contoso.azurecr.io/trading/fix-engine:4.1.0\n"
                "    ports:\n"
                "      - '9878:9878'\n"
                "    volumes:\n"
                "      - fix-logs:/var/log/fix\n"
                "    environment:\n"
                "      - FIX_VERSION=4.4\n"
                "      - SENDER_COMP_ID=CONTOSO\n"
                "      - TARGET_COMP_ID=NYSE\n\n"
                "  market-data:\n"
                "    image: contoso.azurecr.io/trading/market-data:3.0.2\n"
                "    ports:\n"
                "      - '9443:9443'\n"
                "    environment:\n"
                "      - BLOOMBERG_API_KEY=${BLOOMBERG_KEY}\n"
                "      - REUTERS_ENDPOINT=wss://reuters-feed.contoso.com/ws\n\n"
                "volumes:\n"
                "  fix-logs:\n\n"
                "---\n\n"
                "The error I get is:\n"
                "ERROR: for order-gateway  Container 'a1b2c3d4' is unhealthy.\n"
                "ERROR: Encountered errors while bringing up the project.\n\n"
                "The health check on the order-gateway keeps failing. I think the market-data "
                "service isn't responding on port 9443, which causes the gateway to fail startup. "
                "This is blocking our morning trading session.\n\n"
                "Yuki Tanaka, Electronic Trading"
            ),
            reporter=Reporter(
                name="Yuki Tanaka",
                email="yuki.tanaka@contoso.com",
                department="Electronic Trading",
            ),
            created_at="2026-03-17T05:45:00Z",
            channel=Channel.EMAIL,
            attachments=[],
        ),
        gold=GoldAnswer(
            ticket_id="INC-DC-055",
            category=Category.SOFTWARE,
            priority=Priority.P2,
            assigned_team=Team.ENTERPRISE_APPS,
            needs_escalation=False,
            missing_information=[MissingInfoField.ERROR_MESSAGE, MissingInfoField.ENVIRONMENT_DETAILS],
            next_best_action=(
                "Investigate why the market-data container is not responding on port 9443, "
                "causing the order-gateway health check to fail after the platform update."
            ),
            remediation_steps=[
                "Check the market-data container logs for startup errors.",
                "Verify the Bloomberg API key and Reuters endpoint are still valid after the update.",
                "Test connectivity from the order-gateway container to market-data:9443.",
                "Check if the container image versions are compatible with the updated platform.",
                "Restart the docker-compose stack with verbose logging enabled.",
            ],
        ),
        tags=["data-cleanup", "docker_compose", "yaml_flood", "container_config"],
        description=(
            "Tests handling of multiple docker-compose YAML configurations dumped into the ticket description."
        ),
    )


def _dc056_ocr_financial_report() -> EvalCase:
    """OCR'd financial report with scrambled numbers and misaligned columns."""
    return EvalCase(
        ticket=EvalTicket(
            ticket_id="INC-DC-056",
            subject="PDF generator producing corrupted quarterly reports",
            description=(
                "The automated PDF report generator for our quarterly earnings summaries is "
                "producing garbled output. When I OCR the PDFs, this is what comes out:\n\n"
                "CONT0SO F1NANCIAL SERV1CES — Q1 2O26 EARN1NGS SUMMARY\n"
                "=======================================================\n\n"
                "Segment         Revenue    Net lncome    Marg1n    YoY Growth\n"
                "---------       --------   ----------    ------    ----------\n"
                "Wealth Mgmt     $2,4S7M    $3B7M         15.B%     +12.3%\n"
                "lnst. Trading   $1,B92M    $2B1M         l4.9%     +8.7%\n"
                "Ret. Banking    $B43M      $ll2M         l3.3%     +5.l%\n"
                "Corp Finance    $l,2O5M    $lB9M         l5.7%     +lO.2%\n"
                "Risk Mgmt       $43lM      $72M          l6.7%     +3.4%\n\n"
                "T0TAL           $6,B28M    $l,O2lM       l5.O%     +8.9%\n\n"
                "N0TE: Numbers shown in mi11ions. A11 figures are pre1iminary and\n"
                "subject to audit rev1ew. Pr1or per1od comparab1es have been\n"
                "restated to ref1ect the new segment report1ng structure.\n\n"
                "The numbers are completely wrong — 'l' and '1' are getting confused, "
                "'B' is replacing '8', 'O' and '0' are swapped. This is not just a display "
                "issue; the underlying PDF generation engine seems to be using the wrong "
                "font mapping. We need this fixed before the board presentation on Friday.\n\n"
                "Diana Morales, Financial Reporting"
            ),
            reporter=Reporter(
                name="Diana Morales",
                email="diana.morales@contoso.com",
                department="Financial Reporting",
            ),
            created_at="2026-03-17T11:00:00Z",
            channel=Channel.PORTAL,
            attachments=["Q1_2026_earnings_garbled.pdf"],
        ),
        gold=GoldAnswer(
            ticket_id="INC-DC-056",
            category=Category.SOFTWARE,
            priority=Priority.P3,
            assigned_team=Team.ENTERPRISE_APPS,
            needs_escalation=False,
            missing_information=[MissingInfoField.APPLICATION_VERSION, MissingInfoField.ENVIRONMENT_DETAILS],
            next_best_action=(
                "Investigate the PDF report generator's font mapping issue causing character "
                "confusion (l/1, B/8, O/0) in quarterly earnings reports."
            ),
            remediation_steps=[
                "Check the PDF generation engine configuration for font mapping changes.",
                "Compare the current font files with the previous working version.",
                "Verify the report template has not been corrupted.",
                "Regenerate a test report and validate the output against known values.",
                "Roll back the PDF engine to the last known working version if needed.",
            ],
        ),
        tags=["data-cleanup", "ocr_corruption", "financial_report", "number_scramble", "font_confusion"],
        description=(
            "Tests handling of OCR-corrupted financial report data with "
            "character confusion (l/1, B/8, O/0) and misaligned columns."
        ),
    )


def _dc057_quoted_printable_encoding() -> EvalCase:
    """Email body with quoted-printable encoding artifacts."""
    return EvalCase(
        ticket=EvalTicket(
            ticket_id="INC-DC-057",
            subject="SSO login failing after IdP migration =?UTF-8?Q?=E2=80=94?= urgent",
            description=(
                "Hi IT Support,\n\n"
                "Since the IdP migration last weekend, I can=E2=80=99t log in to any SSO-=\n"
                "protected applications. When I try to authenticate, the Okta page shows =\n"
                "=E2=80=9CAuthentication Failed =E2=80=93 Error Code: AUTH_ERR_0x4F21=E2=80=9D =\n"
                "and then redirects me back to the login screen.\n\n"
                "I=E2=80=99ve tried:\n"
                "=E2=80=A2 Clearing browser cache and cookies\n"
                "=E2=80=A2 Using Chrome, Edge, and Firefox\n"
                "=E2=80=A2 Connecting from both office Wi-Fi and VPN\n"
                "=E2=80=A2 Resetting my password via the self-service portal\n\n"
                "None of these worked. My colleague Sarah on the same team can log in =\n"
                "fine, so it=E2=80=99s specific to my account.\n\n"
                "This is blocking all my work =E2=80=93 I can=E2=80=99t access Jira, Confl=\n"
                "uence, Salesforce, or the internal HR portal.\n\n"
                "Thanks,=20\n"
                "Olivia Martinez=20\n"
                "Client Relations=20\n"
                "\n"
                "--=20\n"
                "Contoso Financial Services=20\n"
                "200 Park Avenue, New York, NY 10166=20\n"
                "Tel: +1 (212) 555-0234=20\n"
            ),
            reporter=Reporter(
                name="Olivia Martinez",
                email="olivia.martinez@contoso.com",
                department="Client Relations",
            ),
            created_at="2026-03-17T08:45:00Z",
            channel=Channel.EMAIL,
            attachments=[],
        ),
        gold=GoldAnswer(
            ticket_id="INC-DC-057",
            category=Category.ACCESS_AUTH,
            priority=Priority.P2,
            assigned_team=Team.IAM,
            needs_escalation=False,
            missing_information=[MissingInfoField.AUTHENTICATION_METHOD, MissingInfoField.ERROR_MESSAGE],
            next_best_action=(
                "Investigate the SSO authentication failure (AUTH_ERR_0x4F21) for this user "
                "after the IdP migration. The issue is user-specific since colleagues can log in."
            ),
            remediation_steps=[
                "Check the user's account status in Okta after the IdP migration.",
                "Verify the user's SAML assertions are correctly mapped in the new IdP configuration.",
                "Check if the user's account was fully migrated or if there is a sync issue.",
                "Review Okta system logs for the specific AUTH_ERR_0x4F21 error details.",
                "If the migration is incomplete, manually re-provision the user's SSO profile.",
            ],
        ),
        tags=["data-cleanup", "quoted_printable", "content_encoding", "email_encoding"],
        description=(
            "Tests handling of quoted-printable encoding artifacts (=E2=80=99, "
            "=20, soft line breaks) in the ticket description."
        ),
    )


def _dc058_servicenow_audit_trail() -> EvalCase:
    """Auto-generated ServiceNow ticket with full audit trail."""
    return EvalCase(
        ticket=EvalTicket(
            ticket_id="INC-DC-058",
            subject="FW: INC0045672 — VPN access request for new Singapore office",
            description=(
                "---------- Forwarded from ServiceNow ----------\n"
                "Incident: INC0045672\n"
                "State: Awaiting Assignment\n"
                "Created: 2026-03-14 09:00:00 SGT\n"
                "Updated: 2026-03-17 07:30:00 SGT\n\n"
                "=== ACTIVITY LOG ===\n\n"
                "[2026-03-17 07:30:00] System — State changed from 'Pending Approval' to "
                "'Awaiting Assignment'\n"
                "[2026-03-17 07:30:00] System — Approval granted by: Regional IT Manager "
                "(approval_id: APR-2026-0892)\n"
                "[2026-03-16 14:22:00] Sarah Lim — Additional Information: 'We need VPN "
                "access for the entire Singapore office (15 users). The office opens on "
                "March 24th. We need GlobalProtect profiles configured for the SG-NET-01 "
                "VLAN. Please refer to the attached network diagram.'\n"
                "[2026-03-16 10:05:00] System — Assigned to group: 'Network Operations — APAC'\n"
                "[2026-03-16 10:05:00] System — Priority changed from P4 to P3 (business "
                "justification provided)\n"
                "[2026-03-15 16:45:00] Auto-Router — Category set to 'Network & Connectivity'\n"
                "[2026-03-15 16:45:00] Auto-Router — Subcategory set to 'VPN Access'\n"
                "[2026-03-15 09:30:00] System — Approval requested from: Regional IT Manager\n"
                "[2026-03-15 09:30:00] System — State changed from 'New' to 'Pending Approval'\n"
                "[2026-03-14 09:00:00] Sarah Lim — 'Need VPN access for Singapore office'\n\n"
                "=== FIELD CHANGES ===\n\n"
                "assignment_group: '' → 'Network Operations — APAC'\n"
                "priority: '4 - Low' → '3 - Moderate'\n"
                "state: 'New' → 'Pending Approval' → 'Awaiting Assignment'\n"
                "subcategory: '' → 'VPN Access'\n"
                "approval: 'not requested' → 'requested' → 'approved'\n\n"
                "=== ORIGINAL DESCRIPTION ===\n\n"
                "We are opening a new office in Singapore and need VPN access configured "
                "for 15 staff members. The office will be operational from March 24, 2026. "
                "Please set up GlobalProtect VPN profiles for all users on the SG-NET-01 "
                "network segment.\n\n"
                "---------- End ServiceNow Forward ----------\n"
            ),
            reporter=Reporter(
                name="Sarah Lim",
                email="sarah.lim@contoso.com",
                department="Operations — APAC",
            ),
            created_at="2026-03-17T07:45:00Z",
            channel=Channel.EMAIL,
            attachments=["sg_office_network_diagram.pdf"],
        ),
        gold=GoldAnswer(
            ticket_id="INC-DC-058",
            category=Category.NETWORK,
            priority=Priority.P3,
            assigned_team=Team.NETWORK_OPS,
            needs_escalation=False,
            missing_information=[MissingInfoField.NETWORK_LOCATION, MissingInfoField.CONFIGURATION_DETAILS],
            next_best_action=(
                "Configure GlobalProtect VPN profiles for 15 users at the new Singapore "
                "office on the SG-NET-01 VLAN before the March 24 opening date."
            ),
            remediation_steps=[
                "Review the attached network diagram for the Singapore office layout.",
                "Create GlobalProtect VPN profiles for the SG-NET-01 VLAN segment.",
                "Provision VPN access for the 15 users listed in the request.",
                "Test VPN connectivity from the Singapore network before the office opens.",
                "Provide onboarding documentation for VPN setup to the Singapore team.",
            ],
        ),
        tags=["data-cleanup", "itsm_audit_trail", "state_transitions", "servicenow_forward"],
        description=(
            "Tests handling of a forwarded ServiceNow ticket with full audit trail, "
            "state transitions, field changes, and approval chain."
        ),
    )


def _dc059_bloomberg_terminal_paste() -> EvalCase:
    """Bloomberg terminal fixed-width output pasted into description."""
    return EvalCase(
        ticket=EvalTicket(
            ticket_id="INC-DC-059",
            subject="URGENT — Bloomberg DL not connecting to market data feed",
            description=(
                "Bloomberg Desktop is not connecting to the live market data feed since "
                "this morning. I need this fixed ASAP — morning trading session starts at 9:30.\n\n"
                "Here is what I see on my Bloomberg terminal (copied the screen output):\n\n"
                "BLOOMBERG PROFESSIONAL SERVICE\n"
                "============================================================\n"
                "CONNECTION STATUS: DISCONNECTED\n"
                "Last Connected: 2026-03-16 16:32:00 EST\n"
                "Error: FEED_TIMEOUT_ERR (0x7E01) — Market data subscription timed out\n\n"
                "SECURITY        LAST     CHG      %CHG     BID      ASK      VOL\n"
                "-----------------------------------------------------------------------\n"
                "SPX Index       5,247.83 ---.--   --.--    ---.--   ---.--   ---\n"
                "ES1 Index       5,251.50 ---.--   --.--    ---.--   ---.--   ---\n"
                "NQ1 Index      18,432.75 ---.--   --.--    ---.--   ---.--   ---\n"
                "VIX Index          14.23 ---.--   --.--    ---.--   ---.--   ---\n"
                "UST 10Y            4.287 ---.--   --.--    ---.--   ---.--   ---\n"
                "EUR Curncy         1.0842 ---.--  --.--    ---.--   ---.--   ---\n"
                "GBP Curncy         1.2734 ---.--  --.--    ---.--   ---.--   ---\n"
                "CL1 Comdty        78.43  ---.--   --.--    ---.--   ---.--   ---\n"
                "GC1 Comdty     2,178.50  ---.--   --.--    ---.--   ---.--   ---\n"
                "-----------------------------------------------------------------------\n"
                "ALL SUBSCRIPTIONS STALE — NO LIVE DATA\n\n"
                "BLP API STATUS:\n"
                "  blpapi-cpp: v3.19.1.1\n"
                "  Session: INACTIVE\n"
                "  Service: //blp/mktdata — NOT_AVAILABLE\n"
                "  Service: //blp/refdata — NOT_AVAILABLE\n\n"
                "I already restarted Bloomberg and rebooted my workstation. The connection "
                "test (PCNT <GO>) says 'External connectivity OK' but the data feed still "
                "shows stale. Other traders on the floor have the same issue.\n\n"
                "Marcus Whitfield, Equities Trading Desk"
            ),
            reporter=Reporter(
                name="Marcus Whitfield",
                email="marcus.whitfield@contoso.com",
                department="Equities Trading",
            ),
            created_at="2026-03-17T08:15:00Z",
            channel=Channel.PHONE,
            attachments=[],
        ),
        gold=GoldAnswer(
            ticket_id="INC-DC-059",
            category=Category.SOFTWARE,
            priority=Priority.P1,
            assigned_team=Team.ENTERPRISE_APPS,
            needs_escalation=True,
            missing_information=[MissingInfoField.AFFECTED_USERS, MissingInfoField.NETWORK_LOCATION],
            next_best_action=(
                "Urgently investigate the Bloomberg market data feed outage affecting the "
                "trading floor. Multiple traders impacted before market open."
            ),
            remediation_steps=[
                "Contact Bloomberg support to check if the FEED_TIMEOUT_ERR is on their end.",
                "Verify network connectivity between the trading floor and Bloomberg data centers.",
                "Check if firewall rules or proxy settings were changed affecting Bloomberg ports.",
                "Determine the scope of impact — how many traders and desks are affected.",
                "Escalate to network operations if the issue is on Contoso's network infrastructure.",
            ],
        ),
        tags=["data-cleanup", "bloomberg_terminal", "fixed_width_data", "financial_terminal", "market_data"],
        description=(
            "Tests handling of Bloomberg terminal fixed-width output with "
            "financial data grids and API status information."
        ),
    )


def _dc060_excel_formula_artifacts() -> EvalCase:
    """Clipboard paste from Excel showing raw formulas instead of values."""
    return EvalCase(
        ticket=EvalTicket(
            ticket_id="INC-DC-060",
            subject="Internal reporting tool export showing formulas instead of values",
            description=(
                "The export function in our internal reporting tool (FinReport v5.2) is broken. "
                "When I export the monthly P&L summary to Excel, the cells show formulas instead "
                "of calculated values. Here's what the export looks like when I paste from "
                "the clipboard:\n\n"
                "Department\tRevenue\tExpenses\tNet Income\tMargin\n"
                "Equities\t=SUM(B2:B13)\t=SUM(C2:C13)\t=B14-C14\t=D14/B14\n"
                'Fixed Income\t=VLOOKUP("FI",DataSource!A:D,2,FALSE)\t'
                '=VLOOKUP("FI",DataSource!A:D,3,FALSE)\t=B15-C15\t=D15/B15\n'
                'Derivatives\t=INDEX(Revenue,MATCH("DRV",Segments,0))\t'
                '=INDEX(Expenses,MATCH("DRV",Segments,0))\t=B16-C16\t#REF!\n'
                "Wealth Mgmt\t$2,457,000\t$1,893,000\t=B17-C17\t=D17/B17\n"
                "Corporate\t#N/A\t#N/A\t#VALUE!\t#DIV/0!\n"
                "TOTAL\t=SUM(B14:B18)\t=SUM(C14:C18)\t=SUM(D14:D18)\t=D19/B19\n\n"
                "As you can see, some cells have actual values, some show the underlying "
                "formulas, and some show Excel errors (#REF!, #N/A, #VALUE!, #DIV/0!). The "
                "DataSource worksheet reference is breaking because the export doesn't include "
                "the linked workbook.\n\n"
                "This report needs to go to the CFO by end of day Wednesday. Please fix the "
                "export function so it outputs values, not formulas.\n\n"
                "Karen Liu, Financial Planning & Analysis"
            ),
            reporter=Reporter(
                name="Karen Liu",
                email="karen.liu@contoso.com",
                department="Financial Planning & Analysis",
            ),
            created_at="2026-03-17T13:20:00Z",
            channel=Channel.PORTAL,
            attachments=["PL_summary_broken_export.xlsx"],
        ),
        gold=GoldAnswer(
            ticket_id="INC-DC-060",
            category=Category.DATA_STORAGE,
            priority=Priority.P2,
            assigned_team=Team.DATA_PLATFORM,
            needs_escalation=False,
            missing_information=[MissingInfoField.APPLICATION_VERSION, MissingInfoField.STEPS_TO_REPRODUCE],
            next_best_action=(
                "Investigate the FinReport v5.2 export function that is outputting raw "
                "Excel formulas and broken references instead of calculated values."
            ),
            remediation_steps=[
                "Check the FinReport export configuration for formula vs. value output settings.",
                "Verify the DataSource worksheet link is included in the export template.",
                "Test the export function with a smaller dataset to isolate the issue.",
                "If a bug, file a defect with the FinReport development team for a hotfix.",
                "As a workaround, manually copy-paste values from the live workbook for the CFO report.",
            ],
        ),
        tags=["data-cleanup", "excel_formulas", "clipboard_artifacts", "formula_noise", "spreadsheet_errors"],
        description=(
            "Tests handling of Excel clipboard paste showing raw formulas "
            "(=SUM, =VLOOKUP, =INDEX) and errors (#REF!, #N/A, #VALUE!, #DIV/0!)."
        ),
    )


def _dc061_csv_spreadsheet_inline() -> EvalCase:
    """Raw CSV table with 20+ rows of employee access data pasted into email."""
    return EvalCase(
        ticket=EvalTicket(
            ticket_id="INC-DC-061",
            subject="Access provisioning broken for new hires — see attached roster",
            description=(
                "Hi IAM team,\n\n"
                "We onboarded a batch of new hires last Monday and their access still isn't "
                "provisioned. I exported the roster from HR Workday and I'm pasting it here so "
                "you can see exactly who is affected:\n\n"
                "EmployeeID,FullName,Department,Title,AccessLevel,StartDate,Manager,Location,CostCenter,Status\n"
                "E10441,Priya Patel,Engineering,Software Engineer II,L3,2026-03-01,David Kim,Building "
                "40,CC-4401,Pending\n"
                "E10442,James O'Brien,Engineering,DevOps Engineer,L3,2026-03-01,David Kim,Building 40,CC-4401,Pending\n"
                "E10443,Aisha Mohammed,Finance,Financial Analyst,L2,2026-03-01,Lisa Chen,Building 12,CC-1205,Pending\n"
                "E10444,Carlos Gutierrez,Marketing,Content Strategist,L2,2026-03-01,Rachel Adams,Building "
                "8,CC-0801,Pending\n"
                "E10445,Yuki Tanaka,Engineering,QA Engineer,L3,2026-03-01,David Kim,Building 40,CC-4401,Pending\n"
                "E10446,Sarah Johansson,Legal,Paralegal,L1,2026-03-01,Michael Brown,Building 3,CC-0305,Pending\n"
                "E10447,Oluwaseun Adeyemi,Sales,Account Executive,L2,2026-03-01,Jennifer Wu,Building "
                "15,CC-1502,Pending\n"
                "E10448,Wei Zhang,Engineering,Data Scientist,L4,2026-03-01,David Kim,Building 40,CC-4401,Pending\n"
                "E10449,Elena Kowalski,HR,HR Business Partner,L2,2026-03-01,Patricia Gomez,Building 5,CC-0510,Pending\n"
                "E10450,Raj Krishnamurthy,Engineering,Site Reliability Engineer,L3,2026-03-01,David Kim,Building "
                "40,CC-4401,Pending\n"
                "E10451,Maria Santos,Customer Success,CSM,L2,2026-03-01,Tom Harris,Building 10,CC-1003,Pending\n"
                "E10452,Nathan Williams,Engineering,Frontend Engineer,L3,2026-03-01,David Kim,Building "
                "40,CC-4401,Pending\n"
                "E10453,Sophie Dubois,Design,UX Designer,L2,2026-03-01,Anna Petrov,Building 22,CC-2201,Pending\n"
                "E10454,Ahmed Hassan,Security,Security Analyst,L3,2026-03-01,Robert Chen,Building 7,CC-0702,Pending\n"
                "E10455,Liam O'Connor,IT,Systems Administrator,L3,2026-03-01,Steve Park,Building 2,CC-0208,Pending\n"
                "E10456,Fatima Al-Rashid,Product,Product Manager,L3,2026-03-01,Diana Lee,Building 18,CC-1801,Pending\n"
                "E10457,Henrik Larsson,Engineering,Backend Engineer,L3,2026-03-01,David Kim,Building "
                "40,CC-4401,Pending\n"
                "E10458,Grace Okafor,Finance,Accounts Payable Specialist,L1,2026-03-01,Lisa Chen,Building "
                "12,CC-1205,Pending\n"
                "E10459,Tomasz Nowak,Operations,Operations Analyst,L2,2026-03-01,Mark Johnson,Building "
                "6,CC-0603,Pending\n"
                "E10460,Isabel Fernandez,Engineering,Mobile Developer,L3,2026-03-01,David Kim,Building "
                "40,CC-4401,Pending\n"
                "E10461,Kevin Nakamura,Engineering,Platform Engineer,L3,2026-03-01,David Kim,Building "
                "40,CC-4401,Pending\n"
                "E10462,Amara Diallo,Compliance,Compliance Officer,L2,2026-03-01,Sandra Green,Building "
                "3,CC-0312,Pending\n\n"
                "All of them show Status=Pending in the provisioning dashboard. They can't log "
                "into any internal systems. Please bulk-provision ASAP.\n\n"
                "Thanks,\nTanya Reeves\nHR Operations"
            ),
            reporter=Reporter(
                name="Tanya Reeves",
                email="tanya.reeves@contoso.com",
                department="HR Operations",
            ),
            created_at="2026-03-18T09:30:00Z",
            channel=Channel.EMAIL,
            attachments=[],
        ),
        gold=GoldAnswer(
            ticket_id="INC-DC-061",
            category=Category.ACCESS_AUTH,
            priority=Priority.P3,
            assigned_team=Team.IAM,
            needs_escalation=False,
            missing_information=[MissingInfoField.AFFECTED_SYSTEM, MissingInfoField.STEPS_TO_REPRODUCE],
            next_best_action=(
                "Investigate the provisioning pipeline to determine why the batch of 22 new "
                "hires from the 2026-03-01 cohort remain in Pending status."
            ),
            remediation_steps=[
                "Check the IAM provisioning queue for errors related to the March 1 cohort.",
                "Verify the HR Workday sync connector is running and last sync timestamp.",
                "Manually trigger a provisioning run for the affected employee IDs.",
                "Confirm each employee's manager and cost-center mapping is valid in the directory.",
                "Notify HR Operations once all accounts are provisioned and active.",
            ],
        ),
        tags=["data-cleanup", "csv_inline", "spreadsheet_data", "bulk_employee_data", "access_provisioning"],
        description=(
            "Tests handling of a raw CSV table with 22 rows of employee data pasted "
            "directly into an email body, obscuring the actual provisioning issue."
        ),
    )


def _dc062_tracking_url_noise() -> EvalCase:
    """Three extremely long URLs with tracking parameters burying a SharePoint issue."""
    return EvalCase(
        ticket=EvalTicket(
            ticket_id="INC-DC-062",
            subject="SharePoint links not working for external partners",
            description=(
                "Hey team,\n\n"
                "Our external partners can't access the shared documents we sent them. "
                "Here are the three links that are broken:\n\n"
                "1) https://contoso.sharepoint.com/sites/PartnerPortal/Shared%20Documents/"
                "Q1-2026-Partner-Onboarding-Kit/Welcome-Pack-v3.2.pdf"
                "?utm_source=partner_email_campaign_q1_2026_wave3&utm_medium=email"
                "&utm_campaign=partner_onboarding_welcome_kit_march_2026_external_distribution"
                "&utm_content=document_link_primary_cta_button_blue_variant_a"
                "&utm_term=partner_onboarding_documents_q1&fbclid=IwAR3kZ9x7vQmPL2uR"
                "8nTfY4wJ5sDh1bXcK0eA6gMvNpOqWx3yBzC4tF7iHj2k&msclkid=a1b2c3d4e5f6"
                "789012345678abcdef01&_ga=2.123456789.987654321.1234567890-0987654321"
                ".1234567890&ref=email_blast_march_17\n\n"
                "2) https://contoso.sharepoint.com/sites/PartnerPortal/Shared%20Documents/"
                "Q1-2026-Partner-Onboarding-Kit/Technical-Integration-Guide-API-v2.1.docx"
                "?utm_source=partner_technical_docs_q1_2026_distribution&utm_medium=email"
                "&utm_campaign=partner_technical_integration_guide_march_2026_api_docs_release"
                "&utm_content=secondary_document_link_inline_text_variant_b"
                "&utm_term=api_integration_technical_documentation&fbclid=IwAR2mN7pK4wXv"
                "Q1sLf8jRtY3hU6oBdCe9zA5xGkMnWpTrEq0yDuV2iJc1g&msclkid=f6e5d4c3b2a1"
                "098765432109fedcba98&_ga=2.987654321.123456789.0987654321-1234567890"
                ".0987654321&ref=technical_docs_email_march_18\n\n"
                "3) https://contoso.sharepoint.com/sites/PartnerPortal/Shared%20Documents/"
                "Q1-2026-Partner-Onboarding-Kit/NDA-and-Data-Sharing-Agreement-Template.pdf"
                "?utm_source=partner_legal_documents_q1_2026_nda_distribution&utm_medium=email"
                "&utm_campaign=partner_legal_nda_data_sharing_agreement_march_2026_wave3"
                "&utm_content=legal_document_link_footer_text_variant_c"
                "&utm_term=nda_data_sharing_legal_partner&fbclid=IwAR1jK5nL3xYwS0rMg"
                "7iQtZ2fU8pAeCd4yB6vHkOnXqTsEm9zDuW3hRb0a&msclkid=01234567890abcdef"
                "fedcba9876543210&_ga=2.111222333.444555666.7778889990-0001112223"
                ".3334445556&ref=legal_docs_email_march_18\n\n"
                "Acme Corp, Globex Inc, and Initech Ltd all reported they get a 403 Forbidden "
                "error when clicking any of these. We verified the sharing settings look "
                "correct on our end. Could be a permissions inheritance issue?\n\n"
                "Thanks,\nDerek Olsen\nPartner Relations"
            ),
            reporter=Reporter(
                name="Derek Olsen",
                email="derek.olsen@contoso.com",
                department="Partner Relations",
            ),
            created_at="2026-03-18T14:05:00Z",
            channel=Channel.CHAT,
            attachments=[],
        ),
        gold=GoldAnswer(
            ticket_id="INC-DC-062",
            category=Category.DATA_STORAGE,
            priority=Priority.P3,
            assigned_team=Team.DATA_PLATFORM,
            needs_escalation=False,
            missing_information=[MissingInfoField.ERROR_MESSAGE, MissingInfoField.STEPS_TO_REPRODUCE],
            next_best_action=(
                "Investigate the SharePoint external sharing permissions for the "
                "PartnerPortal site to determine why partner organizations receive 403 errors."
            ),
            remediation_steps=[
                "Check the SharePoint external sharing settings for the PartnerPortal site collection.",
                "Verify that the three partner domains (acmecorp, globex, initech) are on the allowed list.",
                "Review permissions inheritance on the Q1-2026-Partner-Onboarding-Kit folder.",
                "Test access with a clean URL (without tracking parameters) from an external account.",
                "Re-send sharing invitations directly from SharePoint if link-based sharing is misconfigured.",
            ],
        ),
        tags=["data-cleanup", "tracking_urls", "url_noise", "sharepoint_permissions", "external_sharing"],
        description=(
            "Tests handling of three extremely long URLs laden with utm, fbclid, msclkid, "
            "and _ga tracking parameters that obscure the actual SharePoint access issue."
        ),
    )


def _dc063_rtf_markup_artifacts() -> EvalCase:
    """RTF formatting codes mixed into a printer driver complaint."""
    return EvalCase(
        ticket=EvalTicket(
            ticket_id="INC-DC-063",
            subject="Printer on 4th floor not printing color — garbled output",
            description=(
                r"{\rtf1\ansi\ansicpg1252\deff0\nouicompat{\fonttbl{\f0\fswiss\fcharset0 Calibri;}}"
                r"{\colortbl ;\red0\green0\blue0;\red255\green0\blue0;}"
                r"{\*\generator Riched20 10.0.22621}\viewkind4\uc1 "
                r"\pard\sa200\sl276\slmult1\f0\fs22\lang9 "
                "Hi IT Support,\\par\n"
                "\\par\n"
                r"The HP Color LaserJet Pro MFP M479fdw on the 4th floor (asset tag PRN-4F-017) "
                r"is printing everything in black and white even though I\rquote m selecting color. "
                r"\par"
                "\n"
                r"I tried printing a test page from \b Windows Settings > Printers & Scanners\b0  "
                r"and the test page itself came out grayscale. The printer\rquote s front panel "
                r"shows all four toner cartridges (CMYK) as \cf2 OK\cf1 . \par"
                "\n"
                r"\par"
                "\n"
                r"Steps I took:\par"
                "\n"
                r"{\pntext\f0 1.\tab}Restarted the printer \endash  no change\par"
                "\n"
                r"{\pntext\f0 2.\tab}Removed and reseated all toner cartridges\par"
                "\n"
                r"{\pntext\f0 3.\tab}Printed from a different laptop \endash  same issue\par"
                "\n"
                r"{\pntext\f0 4.\tab}Checked driver settings \endash  color is selected, not grayscale\par"
                "\n"
                r"\par"
                "\n"
                r"Could be a driver issue after last week\rquote s Windows Update? The printer worked "
                r"fine before Tuesday.\par"
                "\n"
                r"\par"
                "\n"
                r"Thanks,\par"
                "\n"
                r"Monica Tremblay\par"
                "\n"
                r"Facilities Management, 4th Floor\par"
                "\n"
                "}"
            ),
            reporter=Reporter(
                name="Monica Tremblay",
                email="monica.tremblay@contoso.com",
                department="Facilities Management",
            ),
            created_at="2026-03-19T10:45:00Z",
            channel=Channel.EMAIL,
            attachments=[],
        ),
        gold=GoldAnswer(
            ticket_id="INC-DC-063",
            category=Category.HARDWARE,
            priority=Priority.P3,
            assigned_team=Team.ENDPOINT,
            needs_escalation=False,
            missing_information=[MissingInfoField.DEVICE_INFO, MissingInfoField.ERROR_MESSAGE],
            next_best_action=(
                "Investigate the HP Color LaserJet Pro MFP M479fdw (PRN-4F-017) on the 4th "
                "floor that is printing only in grayscale despite color being selected."
            ),
            remediation_steps=[
                "Check the printer driver version and compare with the last Windows Update.",
                "Reinstall the printer driver using the latest version from HP support.",
                "Verify the printer's internal color settings via the embedded web server.",
                "Run the printer's built-in color calibration and diagnostic page.",
                "If the driver update doesn't resolve the issue, open a case with HP support.",
            ],
        ),
        tags=["data-cleanup", "rtf_markup", "formatting_artifacts", "printer_issue", "rich_text_codes"],
        description=(
            "Tests handling of RTF formatting codes (\\rtf1, \\ansi, \\par, \\fs22, \\pntext, "
            "\\rquote, \\colortbl) scattered throughout a printer complaint."
        ),
    )


def _dc064_auto_reply_chain() -> EvalCase:
    """Five stacked Out of Office auto-replies burying a Teams audio issue."""
    return EvalCase(
        ticket=EvalTicket(
            ticket_id="INC-DC-064",
            subject="Re: Re: Re: Re: Re: Teams audio not working in meetings",
            description=(
                "--- Auto-Reply from: Jessica Huang <jessica.huang@contoso.com> ---\n"
                "Date: Mon, 18 Mar 2026 16:42:00 +0000\n"
                "Subject: Out of Office: Re: Re: Re: Re: Teams audio not working in meetings\n\n"
                "Thank you for your email. I am currently out of the office attending the "
                "Annual Leadership Summit in Austin, TX from March 15-21, 2026. I will have "
                "limited access to email during this time. For urgent matters, please contact "
                "my backup, Derek Simmons (derek.simmons@contoso.com). I will respond to your "
                "email upon my return on March 22.\n\n"
                "Best regards,\nJessica Huang\nVP of Operations\n\n"
                "------------------------------------------------------------\n\n"
                "--- Auto-Reply from: Rajesh Gupta <rajesh.gupta@contoso.com> ---\n"
                "Date: Mon, 18 Mar 2026 16:38:00 +0000\n"
                "Subject: Out of Office: Re: Re: Re: Teams audio not working in meetings\n\n"
                "I am on parental leave from February 24 through April 18, 2026. I will not "
                "be monitoring email during this period. Please reach out to my manager, "
                "Susan Park (susan.park@contoso.com), or the team distribution list "
                "(infra-team@contoso.com) for any infrastructure-related requests.\n\n"
                "Thank you for your understanding.\nRajesh Gupta\nSenior Infrastructure Engineer\n\n"
                "------------------------------------------------------------\n\n"
                "--- Auto-Reply from: Angela Morrison <angela.morrison@contoso.com> ---\n"
                "Date: Mon, 18 Mar 2026 16:35:00 +0000\n"
                "Subject: Automatic Reply: Re: Re: Teams audio not working in meetings\n\n"
                "Hi there! I'm currently attending Microsoft Ignite 2026 in Chicago (March "
                "17-20). I'll be in sessions most of the day but will try to check email in "
                "the evenings. If this is urgent, please text me at (425) 555-0147 or ping "
                "me on Teams. I'll get back to you by March 21 at the latest!\n\n"
                "Cheers,\nAngela Morrison\nCloud Solutions Architect\n\n"
                "------------------------------------------------------------\n\n"
                "--- Auto-Reply from: Thomas Bergstrom <thomas.bergstrom@contoso.com> ---\n"
                "Date: Mon, 18 Mar 2026 16:31:00 +0000\n"
                "Subject: Out of Office: Re: Teams audio not working in meetings\n\n"
                "Thank you for reaching out. I am on PTO from March 17-19 for a family event. "
                "I will return to the office on Thursday, March 20, and will address your email "
                "at that time. For urgent IT issues, please open a ticket at "
                "https://helpdesk.contoso.com or call the IT hotline at ext. 5555.\n\n"
                "Regards,\nThomas Bergstrom\nIT Service Desk Manager\n\n"
                "------------------------------------------------------------\n\n"
                "--- Auto-Reply from: Nadia Petrov <nadia.petrov@contoso.com> ---\n"
                "Date: Mon, 18 Mar 2026 16:28:00 +0000\n"
                "Subject: Automatic Reply: Teams audio not working in meetings\n\n"
                "I'm out of the office today, March 18, for a medical appointment. I will be "
                "back tomorrow, March 19. For anything time-sensitive, please reach out to "
                "Brian Walsh (brian.walsh@contoso.com).\n\n"
                "Thanks,\nNadia Petrov\nDesktop Support Lead\n\n"
                "------------------------------------------------------------\n\n"
                "--- ORIGINAL MESSAGE ---\n"
                "From: Damien Cross <damien.cross@contoso.com>\n"
                "Date: Mon, 18 Mar 2026 16:25:00 +0000\n"
                "Subject: Teams audio not working in meetings\n\n"
                "Hi IT,\n\n"
                "Since this morning my microphone is not being detected in Microsoft Teams "
                "meetings. Other attendees can't hear me at all. The microphone works fine in "
                "Zoom and in Windows Sound Recorder, so it seems to be a Teams-specific issue. "
                "I'm on a Surface Pro 9 running Windows 11 23H2 with Teams version "
                "24004.1309.2689.1410. I already restarted Teams, checked the audio device "
                "settings inside Teams (Settings > Devices), and made sure the mic isn't muted "
                "at the OS level. Nothing works.\n\n"
                "This is blocking me from participating in client calls. Please advise.\n\n"
                "Damien Cross\nClient Engagement, 3rd Floor"
            ),
            reporter=Reporter(
                name="Damien Cross",
                email="damien.cross@contoso.com",
                department="Client Engagement",
            ),
            created_at="2026-03-18T16:50:00Z",
            channel=Channel.EMAIL,
            attachments=[],
        ),
        gold=GoldAnswer(
            ticket_id="INC-DC-064",
            category=Category.SOFTWARE,
            priority=Priority.P3,
            assigned_team=Team.ENTERPRISE_APPS,
            needs_escalation=False,
            missing_information=[MissingInfoField.APPLICATION_VERSION, MissingInfoField.DEVICE_INFO],
            next_best_action=(
                "Investigate why Microsoft Teams is not detecting the microphone on "
                "Damien Cross's Surface Pro 9 while the device works in other applications."
            ),
            remediation_steps=[
                "Check Teams app permissions for microphone access in Windows Privacy settings.",
                "Clear the Teams cache and restart the application.",
                "Verify the correct audio device is selected in Teams device settings.",
                "Test with the Teams web client to rule out a desktop app issue.",
                "If unresolved, reinstall the Teams desktop client.",
            ],
        ),
        tags=["data-cleanup", "auto_reply_chain", "ooo_messages", "buried_issue", "teams_audio"],
        description=(
            "Tests handling of five stacked Out of Office / auto-reply messages that bury "
            "the original Teams audio issue at the very bottom of the thread."
        ),
    )


def _dc065_svg_data_inline() -> EvalCase:
    """SVG XML markup for a network diagram pasted inline, hiding a network issue."""
    return EvalCase(
        ticket=EvalTicket(
            ticket_id="INC-DC-065",
            subject="Intermittent network drops on VLAN 220 — diagram attached inline",
            description=(
                "Hi Network Ops,\n\n"
                "We're experiencing intermittent packet loss on VLAN 220 (Engineering floor, "
                "Building 40). I put together a quick network diagram to show the topology — "
                "here it is:\n\n"
                '<?xml version="1.0" encoding="UTF-8"?>\n'
                '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 600" '
                'width="800" height="600">\n'
                '  <rect width="800" height="600" fill="#f5f5f5" />\n'
                '  <text x="400" y="30" text-anchor="middle" font-size="18" '
                'font-weight="bold">VLAN 220 Topology — Bldg 40</text>\n\n'
                "  <!-- Core Switch -->\n"
                '  <rect x="325" y="60" width="150" height="50" rx="8" fill="#2196F3" />\n'
                '  <text x="400" y="90" text-anchor="middle" fill="white" font-size="12">'
                "Core-SW-01 (Nexus 9300)</text>\n\n"
                "  <!-- Distribution Switches -->\n"
                '  <rect x="100" y="180" width="140" height="45" rx="6" fill="#4CAF50" />\n'
                '  <text x="170" y="207" text-anchor="middle" fill="white" font-size="11">'
                "Dist-SW-40A (Cat 9400)</text>\n"
                '  <rect x="330" y="180" width="140" height="45" rx="6" fill="#4CAF50" />\n'
                '  <text x="400" y="207" text-anchor="middle" fill="white" font-size="11">'
                "Dist-SW-40B (Cat 9400)</text>\n"
                '  <rect x="560" y="180" width="140" height="45" rx="6" fill="#FF9800" />\n'
                '  <text x="630" y="207" text-anchor="middle" fill="white" font-size="11">'
                "Dist-SW-40C (FAILING)</text>\n\n"
                "  <!-- Uplinks -->\n"
                '  <line x1="400" y1="110" x2="170" y2="180" stroke="#333" stroke-width="2" />\n'
                '  <line x1="400" y1="110" x2="400" y2="180" stroke="#333" stroke-width="2" />\n'
                '  <line x1="400" y1="110" x2="630" y2="180" stroke="red" stroke-width="3" '
                'stroke-dasharray="8,4" />\n\n'
                "  <!-- Access Switches -->\n"
                '  <rect x="50" y="300" width="120" height="40" rx="5" fill="#9E9E9E" />\n'
                '  <text x="110" y="325" text-anchor="middle" fill="white" font-size="10">'
                "Acc-40-01 (2960X)</text>\n"
                '  <rect x="200" y="300" width="120" height="40" rx="5" fill="#9E9E9E" />\n'
                '  <text x="260" y="325" text-anchor="middle" fill="white" font-size="10">'
                "Acc-40-02 (2960X)</text>\n"
                '  <rect x="480" y="300" width="120" height="40" rx="5" fill="#9E9E9E" />\n'
                '  <text x="540" y="325" text-anchor="middle" fill="white" font-size="10">'
                "Acc-40-05 (2960X)</text>\n"
                '  <rect x="630" y="300" width="120" height="40" rx="5" fill="#9E9E9E" />\n'
                '  <text x="690" y="325" text-anchor="middle" fill="white" font-size="10">'
                "Acc-40-06 (2960X)</text>\n\n"
                "  <!-- Links to access layer -->\n"
                '  <line x1="170" y1="225" x2="110" y2="300" stroke="#333" stroke-width="1.5" />\n'
                '  <line x1="170" y1="225" x2="260" y2="300" stroke="#333" stroke-width="1.5" />\n'
                '  <line x1="630" y1="225" x2="540" y2="300" stroke="red" stroke-width="2" '
                'stroke-dasharray="5,3" />\n'
                '  <line x1="630" y1="225" x2="690" y2="300" stroke="red" stroke-width="2" '
                'stroke-dasharray="5,3" />\n\n'
                "  <!-- Legend -->\n"
                '  <rect x="50" y="520" width="700" height="60" fill="#eeeeee" rx="5" />\n'
                '  <line x1="70" y1="545" x2="120" y2="545" stroke="#333" stroke-width="2" />\n'
                '  <text x="130" y="549" font-size="10">Healthy Link</text>\n'
                '  <line x1="250" y1="545" x2="300" y2="545" stroke="red" stroke-width="2" '
                'stroke-dasharray="5,3" />\n'
                '  <text x="310" y="549" font-size="10">Degraded / Dropping</text>\n'
                '  <text x="70" y="568" font-size="10" fill="#666">Packet loss observed: '
                "12-18% on Dist-SW-40C uplink, 5-9% on downstream access ports</text>\n"
                "</svg>\n\n"
                "As you can see, Dist-SW-40C is the problem. Downstream ports on Acc-40-05 "
                "and Acc-40-06 are seeing 5-9% packet loss. The uplink from Dist-SW-40C to "
                "Core-SW-01 shows 12-18% loss during peak hours (10am-2pm). About 45 users "
                "on this segment are affected.\n\n"
                "Ravi Subramaniam\nNetwork Engineering, Building 40"
            ),
            reporter=Reporter(
                name="Ravi Subramaniam",
                email="ravi.subramaniam@contoso.com",
                department="Network Engineering",
            ),
            created_at="2026-03-19T11:20:00Z",
            channel=Channel.PORTAL,
            attachments=[],
        ),
        gold=GoldAnswer(
            ticket_id="INC-DC-065",
            category=Category.NETWORK,
            priority=Priority.P2,
            assigned_team=Team.NETWORK_OPS,
            needs_escalation=False,
            missing_information=[MissingInfoField.NETWORK_LOCATION, MissingInfoField.AFFECTED_USERS],
            next_best_action=(
                "Investigate Dist-SW-40C (Catalyst 9400) on VLAN 220 for the 12-18% packet "
                "loss on its uplink to Core-SW-01 and downstream degradation."
            ),
            remediation_steps=[
                "Check interface error counters (CRC, input errors, runts) on Dist-SW-40C uplink.",
                "Review spanning-tree topology for VLAN 220 for any recent reconvergence events.",
                "Inspect the fiber or cabling on the Dist-SW-40C to Core-SW-01 uplink.",
                "Check switch CPU and memory utilisation during the 10am-2pm peak window.",
                "If hardware fault is suspected, schedule a replacement of Dist-SW-40C.",
            ],
        ),
        tags=["data-cleanup", "svg_inline", "xml_markup", "network_diagram", "packet_loss"],
        description=(
            "Tests handling of 30+ lines of inline SVG XML markup for a network topology "
            "diagram embedded directly in the ticket description."
        ),
    )


def _dc066_cross_threaded_issues() -> EvalCase:
    """Two different IT issues (VPN + printer) discussed in one thread by two people."""
    return EvalCase(
        ticket=EvalTicket(
            ticket_id="INC-DC-066",
            subject="Re: VPN issues — also, printer question",
            description=(
                "From: Claire Nakamura <claire.nakamura@contoso.com>\n"
                "Date: Tue, 19 Mar 2026 08:10:00 +0000\n"
                "To: IT Support <it-support@contoso.com>\n\n"
                "Hi IT,\n\n"
                "I can't connect to the VPN at all this morning. GlobalProtect shows "
                "'Gateway Unreachable' when I try to connect from home. I'm on a MacBook "
                "Pro M3 running macOS Sonoma 14.4. My home internet is fine — I can browse "
                "the web, stream video, etc. This started about 30 minutes ago.\n\n"
                "Claire Nakamura\nProduct Design\n\n"
                "------------------------------------------------------------\n\n"
                "From: Ben Kowalczyk <ben.kowalczyk@contoso.com>\n"
                "Date: Tue, 19 Mar 2026 08:18:00 +0000\n"
                "To: IT Support <it-support@contoso.com>\n\n"
                "(Sorry, jumping on this thread since Claire CC'd me)\n\n"
                "Unrelated to Claire's VPN issue, but while I have your attention — the Canon "
                "imageRUNNER on the 2nd floor (near the break room) has been jamming every "
                "3-4 pages for the past week. I've cleared the paper path three times already. "
                "Can someone come look at it? Asset tag is PRN-2F-003.\n\n"
                "Ben Kowalczyk\nProgram Management\n\n"
                "------------------------------------------------------------\n\n"
                "From: Claire Nakamura <claire.nakamura@contoso.com>\n"
                "Date: Tue, 19 Mar 2026 08:25:00 +0000\n\n"
                "Update on my VPN issue: I tried connecting to the backup gateway "
                "(vpn-west.contoso.com) and that one also shows 'Gateway Unreachable'. I ran "
                "a traceroute to vpn.contoso.com and it dies after hop 6 (at the ISP boundary). "
                "Could this be a routing issue on the Contoso side? My colleague in the same "
                "neighborhood is having the same problem.\n\n"
                "------------------------------------------------------------\n\n"
                "From: Ben Kowalczyk <ben.kowalczyk@contoso.com>\n"
                "Date: Tue, 19 Mar 2026 08:31:00 +0000\n\n"
                "Also the printer is making a grinding noise now. Definitely something "
                "mechanical. Just wanted to add that detail in case it helps.\n\n"
                "------------------------------------------------------------\n\n"
                "From: Claire Nakamura <claire.nakamura@contoso.com>\n"
                "Date: Tue, 19 Mar 2026 08:40:00 +0000\n\n"
                "One more data point — I checked DownDetector and there's a spike in "
                "GlobalProtect reports starting around 7:45 AM Pacific. Might be a wider outage. "
                "Can network ops confirm?"
            ),
            reporter=Reporter(
                name="Claire Nakamura",
                email="claire.nakamura@contoso.com",
                department="Product Design",
            ),
            created_at="2026-03-19T08:45:00Z",
            channel=Channel.EMAIL,
            attachments=[],
        ),
        gold=GoldAnswer(
            ticket_id="INC-DC-066",
            category=Category.NETWORK,
            priority=Priority.P2,
            assigned_team=Team.NETWORK_OPS,
            needs_escalation=False,
            missing_information=[MissingInfoField.ERROR_MESSAGE, MissingInfoField.ENVIRONMENT_DETAILS],
            next_best_action=(
                "Investigate the GlobalProtect VPN gateway unreachable issue affecting "
                "multiple remote users, potentially related to an ISP routing problem."
            ),
            remediation_steps=[
                "Check the status of vpn.contoso.com and vpn-west.contoso.com gateway services.",
                "Review ISP peering and BGP route advertisements for anomalies.",
                "Correlate with external monitoring (DownDetector reports) for scope assessment.",
                "Engage the ISP if traceroute confirms the failure is beyond the Contoso boundary.",
                "Notify affected remote users with an ETA once the root cause is identified.",
            ],
        ),
        tags=["data-cleanup", "cross_threaded", "mixed_issues", "vpn_outage", "interleaved_conversation"],
        description=(
            "Tests handling of two different IT issues (VPN connectivity and printer jam) "
            "discussed in one interleaved email thread by two different reporters."
        ),
    )


def _dc067_massive_cc_list() -> EvalCase:
    """25+ CC recipients listed before the actual compliance tool failure content."""
    return EvalCase(
        ticket=EvalTicket(
            ticket_id="INC-DC-067",
            subject="CRITICAL — DLP compliance scanner offline since 6 AM",
            description=(
                "CC: ciso@contoso.com; vp.compliance@contoso.com; "
                "chief.risk.officer@contoso.com; legal.counsel@contoso.com; "
                "data.privacy.officer@contoso.com; soc.lead@contoso.com; "
                "incident.response@contoso.com; audit.director@contoso.com; "
                "regulatory.affairs@contoso.com; infosec.manager@contoso.com; "
                "it.director@contoso.com; cto@contoso.com; "
                "enterprise.risk@contoso.com; business.continuity@contoso.com; "
                "vendor.management@contoso.com; procurement.lead@contoso.com; "
                "network.security@contoso.com; endpoint.security@contoso.com; "
                "cloud.security@contoso.com; identity.security@contoso.com; "
                "siem.admin@contoso.com; vulnerability.mgmt@contoso.com; "
                "threat.intel@contoso.com; forensics.team@contoso.com; "
                "security.architecture@contoso.com; grc.team@contoso.com; "
                "board.secretary@contoso.com\n\n"
                "------------------------------------------------------------\n\n"
                "URGENT — the Symantec DLP compliance scanner (DLP-SCAN-PROD-01) has been "
                "offline since approximately 06:00 UTC this morning. This means no outbound "
                "email or file transfers have been scanned for sensitive data in over 4 hours. "
                "We are currently operating WITHOUT data loss prevention controls.\n\n"
                "Impact:\n"
                "- All outbound email via Exchange Online is unscanned\n"
                "- SharePoint external sharing is unmonitored\n"
                "- OneDrive sync to personal devices is uncontrolled\n"
                "- USB device blocking policies may not be enforced\n\n"
                "The DLP management console shows the scanner service as 'Stopped' with "
                "error code DLP-ERR-5012 (license validation failure). We renewed our "
                "Symantec DLP license last week — the new license key was applied on Friday "
                "March 14 by the vendor's support team.\n\n"
                "This is a regulatory compliance exposure. We are required under SOX and "
                "GDPR to maintain continuous DLP monitoring. Every hour this remains down "
                "increases our audit risk.\n\n"
                "Please treat this as a Sev-1 incident.\n\n"
                "Vincent Morales\nInformation Security, Security Operations Center"
            ),
            reporter=Reporter(
                name="Vincent Morales",
                email="vincent.morales@contoso.com",
                department="Information Security",
            ),
            created_at="2026-03-19T10:15:00Z",
            channel=Channel.EMAIL,
            attachments=[],
        ),
        gold=GoldAnswer(
            ticket_id="INC-DC-067",
            category=Category.SECURITY,
            priority=Priority.P2,
            assigned_team=Team.SECURITY_OPS,
            needs_escalation=True,
            missing_information=[MissingInfoField.AFFECTED_SYSTEM, MissingInfoField.BUSINESS_IMPACT],
            next_best_action=(
                "Urgently restore the Symantec DLP compliance scanner (DLP-SCAN-PROD-01) "
                "which has been offline for 4+ hours, leaving outbound data transfers unscanned."
            ),
            remediation_steps=[
                "Investigate the DLP-ERR-5012 license validation error on DLP-SCAN-PROD-01.",
                "Verify the renewed license key applied on March 14 is correct and activated.",
                "Contact Symantec support to validate the license status on their end.",
                "If the license cannot be resolved quickly, enable the backup DLP policy in Exchange Online.",
                "Document the outage window for SOX and GDPR compliance audit reporting.",
            ],
        ),
        tags=["data-cleanup", "massive_cc_list", "email_header_noise", "compliance_tool", "dlp_scanner"],
        description=(
            "Tests handling of 27 CC recipients listed before the actual ticket content, "
            "requiring the model to skip past the address noise to find the DLP issue."
        ),
    )


def _dc068_env_var_dump() -> EvalCase:
    """User pasted their .env file with 20+ KEY=VALUE lines during an Azure deployment issue."""
    return EvalCase(
        ticket=EvalTicket(
            ticket_id="INC-DC-068",
            subject="Azure App Service deployment failing — config attached",
            description=(
                "Hi team,\n\n"
                "Our production deployment to Azure App Service has been failing since last "
                "night. The deployment pipeline completes, but the app crashes on startup. "
                "I'm pasting our .env config below so you can see if something looks wrong:\n\n"
                "# === Application Settings ===\n"
                "APP_NAME=contoso-customer-portal\n"
                "APP_ENV=production\n"
                "APP_DEBUG=false\n"
                "APP_PORT=8080\n"
                "APP_LOG_LEVEL=info\n"
                "APP_SECRET_KEY=sk_prod_••••••••••••••••••••••••\n\n"
                "# === Database ===\n"
                "DB_HOST=contoso-sql-prod-eastus2.database.windows.net\n"
                "DB_PORT=1433\n"
                "DB_NAME=customerportal_prod\n"
                "DB_USER=app_service_user\n"
                "DB_PASSWORD=••••••••••••••••\n"
                "DB_SSL_MODE=require\n"
                "DB_POOL_SIZE=25\n"
                "DB_CONNECTION_TIMEOUT=30\n\n"
                "# === Redis Cache ===\n"
                "REDIS_HOST=contoso-redis-prod.redis.cache.windows.net\n"
                "REDIS_PORT=6380\n"
                "REDIS_PASSWORD=••••••••••••••••••••••••••••\n"
                "REDIS_SSL=true\n"
                "REDIS_DB=0\n\n"
                "# === Azure Storage ===\n"
                "AZURE_STORAGE_ACCOUNT=contosoportalstorage\n"
                "AZURE_STORAGE_KEY=••••••••••••••••••••••••••••••••••••••••\n"
                "AZURE_STORAGE_CONTAINER=customer-uploads\n\n"
                "# === Authentication ===\n"
                "AZURE_AD_TENANT_ID=72f988bf-86f1-41af-91ab-2d7cd011db47\n"
                "AZURE_AD_CLIENT_ID=a1b2c3d4-e5f6-7890-abcd-ef1234567890\n"
                "AZURE_AD_CLIENT_SECRET=••••••••••••••••••••••\n"
                "JWT_EXPIRATION=3600\n"
                "JWT_REFRESH_EXPIRATION=86400\n\n"
                "# === External APIs ===\n"
                "SENDGRID_API_KEY=SG.••••••••••••••••••••••••••••••••••\n"
                "STRIPE_SECRET_KEY=sk_live_••••••••••••••••••••••••\n"
                "STRIPE_WEBHOOK_SECRET=whsec_••••••••••••••••••••\n"
                "DATADOG_API_KEY=••••••••••••••••••••••••••••••\n"
                "DATADOG_APP_KEY=••••••••••••••••••••••••••••••••••••\n\n"
                "# === Feature Flags ===\n"
                "FF_NEW_CHECKOUT=true\n"
                "FF_DARK_MODE=false\n"
                "FF_BETA_DASHBOARD=true\n\n"
                "The last successful deployment was on March 15. We pushed a new release "
                "last night (v2.14.3) that includes a database migration. The Azure portal "
                "shows the app in a 'Failed' state but the deployment logs just say "
                "'Application startup failed' with no additional detail.\n\n"
                "Jasper Lindqvist\nPlatform Engineering"
            ),
            reporter=Reporter(
                name="Jasper Lindqvist",
                email="jasper.lindqvist@contoso.com",
                department="Platform Engineering",
            ),
            created_at="2026-03-20T07:30:00Z",
            channel=Channel.PORTAL,
            attachments=[],
        ),
        gold=GoldAnswer(
            ticket_id="INC-DC-068",
            category=Category.SOFTWARE,
            priority=Priority.P2,
            assigned_team=Team.ENTERPRISE_APPS,
            needs_escalation=False,
            missing_information=[MissingInfoField.ERROR_MESSAGE, MissingInfoField.ENVIRONMENT_DETAILS],
            next_best_action=(
                "Investigate the Azure App Service startup failure for contoso-customer-portal "
                "v2.14.3, focusing on the database migration introduced in the latest release."
            ),
            remediation_steps=[
                "Pull the full application startup logs from Azure App Service diagnostics.",
                "Check the database migration status — verify it completed successfully.",
                "Compare the App Service configuration settings with the .env to find mismatches.",
                "Roll back to v2.14.2 if the startup failure cannot be quickly resolved.",
                "Advise the reporter to avoid pasting environment variables in tickets, even redacted ones.",
            ],
        ),
        tags=["data-cleanup", "env_var_dump", "config_noise", "azure_deployment", "environment_variables"],
        description=(
            "Tests handling of 20+ .env KEY=VALUE pairs (connection strings, API keys, "
            "feature flags) pasted into a ticket about an Azure deployment failure."
        ),
    )


def _dc069_git_diff_markers() -> EvalCase:
    """Raw git merge conflict markers pasted into a CI/CD pipeline failure report."""
    return EvalCase(
        ticket=EvalTicket(
            ticket_id="INC-DC-069",
            subject="CI/CD pipeline broken — merge conflicts in config files",
            description=(
                "Hi team,\n\n"
                "Our CI/CD pipeline (Azure DevOps, project: contoso-backend) has been "
                "failing for the last 3 builds. The build log shows a merge conflict that "
                "was accidentally committed. Here's the file that's causing the problem "
                "(src/config/database.ts):\n\n"
                "import { ConnectionOptions } from 'typeorm';\n\n"
                "const config: ConnectionOptions = {\n"
                "  type: 'mssql',\n"
                "<<<<<<< HEAD\n"
                "  host: process.env.DB_HOST || 'contoso-sql-prod.database.windows.net',\n"
                "  port: parseInt(process.env.DB_PORT || '1433'),\n"
                "  username: process.env.DB_USER || 'app_user',\n"
                "  password: process.env.DB_PASSWORD,\n"
                "  database: process.env.DB_NAME || 'contoso_prod',\n"
                "  extra: {\n"
                "    encrypt: true,\n"
                "    trustServerCertificate: false,\n"
                "    connectionTimeout: 30000,\n"
                "    requestTimeout: 30000,\n"
                "  },\n"
                "=======\n"
                "  host: process.env.DATABASE_HOST || 'contoso-sql-staging.database.windows.net',\n"
                "  port: parseInt(process.env.DATABASE_PORT || '1433'),\n"
                "  username: process.env.DATABASE_USER || 'staging_user',\n"
                "  password: process.env.DATABASE_PASSWORD,\n"
                "  database: process.env.DATABASE_NAME || 'contoso_staging',\n"
                "  extra: {\n"
                "    encrypt: true,\n"
                "    trustServerCertificate: true,\n"
                "    connectionTimeout: 60000,\n"
                "    requestTimeout: 60000,\n"
                "  },\n"
                ">>>>>>> feature/update-db-config\n"
                "  synchronize: false,\n"
                "  logging: process.env.DB_LOGGING === 'true',\n"
                "  migrations: ['src/migrations/**/*.ts'],\n"
                "};\n\n"
                "export default config;\n\n"
                "The build error is:\n"
                "  error TS1128: Declaration or statement expected.\n"
                "  src/config/database.ts(5,1): error TS1128\n\n"
                "Someone on the team merged the feature/update-db-config branch without "
                "resolving the conflict. The main branch has had this bad commit for about "
                "12 hours and it's blocking all other PRs from being deployed.\n\n"
                "Luis Fernandez\nBackend Engineering"
            ),
            reporter=Reporter(
                name="Luis Fernandez",
                email="luis.fernandez@contoso.com",
                department="Backend Engineering",
            ),
            created_at="2026-03-20T09:15:00Z",
            channel=Channel.CHAT,
            attachments=[],
        ),
        gold=GoldAnswer(
            ticket_id="INC-DC-069",
            category=Category.SOFTWARE,
            priority=Priority.P2,
            assigned_team=Team.ENTERPRISE_APPS,
            needs_escalation=False,
            missing_information=[MissingInfoField.STEPS_TO_REPRODUCE, MissingInfoField.ERROR_MESSAGE],
            next_best_action=(
                "Remove the unresolved git merge conflict markers from "
                "src/config/database.ts on the main branch to unblock the CI/CD pipeline."
            ),
            remediation_steps=[
                "Identify the commit that introduced the unresolved merge conflict on main.",
                "Create a hotfix branch to resolve the conflict in src/config/database.ts.",
                "Choose the correct database configuration (prod vs. staging) for the main branch.",
                "Add a CI pre-merge check to detect unresolved conflict markers in source files.",
                "Retrigger the pipeline once the fix is merged to unblock pending PRs.",
            ],
        ),
        tags=["data-cleanup", "git_diff_markers", "merge_conflict", "cicd_pipeline", "unresolved_conflict"],
        description=(
            "Tests handling of raw git merge conflict markers (<<<<<<< HEAD, =======, "
            ">>>>>>> branch) embedded in a CI/CD pipeline failure report."
        ),
    )


def _dc070_yaml_config_dump() -> EvalCase:
    """30+ lines of Kubernetes YAML deployment config pasted for a pod crash loop issue."""
    return EvalCase(
        ticket=EvalTicket(
            ticket_id="INC-DC-070",
            subject="Kubernetes pod in CrashLoopBackOff — deployment YAML included",
            description=(
                "Hi Platform team,\n\n"
                "The customer-api pod in the production AKS cluster (aks-prod-eastus2) has "
                "been in CrashLoopBackOff since 03:00 UTC. Here's the deployment manifest:\n\n"
                "apiVersion: apps/v1\n"
                "kind: Deployment\n"
                "metadata:\n"
                "  name: customer-api\n"
                "  namespace: production\n"
                "  labels:\n"
                "    app: customer-api\n"
                "    version: v2.8.1\n"
                "    team: platform-engineering\n"
                "    cost-center: CC-4401\n"
                "spec:\n"
                "  replicas: 3\n"
                "  selector:\n"
                "    matchLabels:\n"
                "      app: customer-api\n"
                "  strategy:\n"
                "    type: RollingUpdate\n"
                "    rollingUpdate:\n"
                "      maxSurge: 1\n"
                "      maxUnavailable: 0\n"
                "  template:\n"
                "    metadata:\n"
                "      labels:\n"
                "        app: customer-api\n"
                "        version: v2.8.1\n"
                "    spec:\n"
                "      serviceAccountName: customer-api-sa\n"
                "      containers:\n"
                "      - name: customer-api\n"
                "        image: contosoacr.azurecr.io/customer-api:v2.8.1\n"
                "        ports:\n"
                "        - containerPort: 8080\n"
                "          protocol: TCP\n"
                "        env:\n"
                "        - name: NODE_ENV\n"
                "          value: production\n"
                "        - name: DB_CONNECTION_STRING\n"
                "          valueFrom:\n"
                "            secretKeyRef:\n"
                "              name: customer-api-secrets\n"
                "              key: db-connection-string\n"
                "        - name: REDIS_URL\n"
                "          valueFrom:\n"
                "            secretKeyRef:\n"
                "              name: customer-api-secrets\n"
                "              key: redis-url\n"
                "        resources:\n"
                "          requests:\n"
                "            cpu: 500m\n"
                "            memory: 512Mi\n"
                "          limits:\n"
                "            cpu: 1000m\n"
                "            memory: 1Gi\n"
                "        readinessProbe:\n"
                "          httpGet:\n"
                "            path: /healthz\n"
                "            port: 8080\n"
                "          initialDelaySeconds: 10\n"
                "          periodSeconds: 5\n"
                "        livenessProbe:\n"
                "          httpGet:\n"
                "            path: /healthz\n"
                "            port: 8080\n"
                "          initialDelaySeconds: 30\n"
                "          periodSeconds: 10\n"
                "      imagePullSecrets:\n"
                "      - name: acr-pull-secret\n\n"
                "The pod logs show it starts, connects to the database, then crashes with "
                "an OOMKilled error after about 45 seconds. We bumped the image from v2.7.9 "
                "to v2.8.1 last night and that's when the crash loop started. The v2.8.1 "
                "release includes a new in-memory caching layer that might be consuming more "
                "memory than the 1Gi limit allows.\n\n"
                "kubectl get pods output:\n"
                "NAME                           READY   STATUS             RESTARTS   AGE\n"
                "customer-api-6d4f8b7c9-abc12   0/1     CrashLoopBackOff   47         6h\n"
                "customer-api-6d4f8b7c9-def34   0/1     CrashLoopBackOff   47         6h\n"
                "customer-api-6d4f8b7c9-ghi56   0/1     CrashLoopBackOff   47         6h\n\n"
                "Mikael Johansson\nPlatform Engineering, SRE Team"
            ),
            reporter=Reporter(
                name="Mikael Johansson",
                email="mikael.johansson@contoso.com",
                department="Platform Engineering",
            ),
            created_at="2026-03-20T09:45:00Z",
            channel=Channel.PORTAL,
            attachments=[],
        ),
        gold=GoldAnswer(
            ticket_id="INC-DC-070",
            category=Category.SOFTWARE,
            priority=Priority.P2,
            assigned_team=Team.ENTERPRISE_APPS,
            needs_escalation=False,
            missing_information=[MissingInfoField.ERROR_MESSAGE, MissingInfoField.ENVIRONMENT_DETAILS],
            next_best_action=(
                "Investigate the OOMKilled crash loop on customer-api v2.8.1 pods in the "
                "production AKS cluster, likely caused by the new in-memory caching layer "
                "exceeding the 1Gi memory limit."
            ),
            remediation_steps=[
                "Review pod describe output for OOMKilled events and memory consumption details.",
                "Increase the memory limit from 1Gi to 2Gi as an immediate mitigation.",
                "Profile the v2.8.1 in-memory caching layer to determine actual memory requirements.",
                "If memory growth is unbounded, roll back to v2.7.9 until the caching code is fixed.",
                "Add memory usage alerts to detect pods approaching their limits before they crash.",
            ],
        ),
        tags=["data-cleanup", "yaml_config", "kubernetes_manifest", "pod_crashloop", "oomkilled"],
        description=(
            "Tests handling of 30+ lines of Kubernetes deployment YAML and kubectl output "
            "pasted into a ticket about a pod CrashLoopBackOff / OOMKilled issue."
        ),
    )


def _dc071_very_long_email_buried_issue() -> EvalCase:
    """Very long email with the real issue deeply buried."""
    long_body = (
        "Hi IT Support,\n\n"
        "I am writing to follow up on the ongoing VPN connectivity issue that has been plaguing "
        "our department for the past week. As you know, our team handles time-sensitive derivative "
        "pricing and risk calculations, and any disruption to our access to internal systems has "
        "a direct impact on our ability to deliver accurate valuations to the front office.\n\n"
        "Before I get to the current issue, I wanted to provide some context. Last quarter, we "
        "experienced a similar disruption when the network team migrated the VPN concentrators "
        "to the new Palo Alto infrastructure. At that time, the resolution involved updating the "
        "GlobalProtect client to version 6.1.4 and reconfiguring the split-tunnel policy for our "
        "subnet (10.42.0.0/16). I mention this because I suspect the current problem may be related "
        "to the changes that were made last weekend during the scheduled maintenance window.\n\n"
        "Speaking of which, I was not informed about the maintenance until after it had already "
        "started, which is a recurring communication gap I have raised with management. But that "
        "is a separate matter.\n\n"
        "So regarding the actual problem: I have been completely unable to connect to the VPN "
        "since I changed my domain password on Monday. The GlobalProtect client shows "
        "'Authentication Failed - Invalid Credentials' even though my new password works for "
        "Outlook, SharePoint, the trading portal, and Active Directory web login. I have cleared "
        "the Windows Credential Manager, restarted the GlobalProtect service, and even "
        "uninstalled/reinstalled the client. Nothing works.\n\n"
        "My colleague Arun in the same team has no issues, and he also changed his password on "
        "Monday. The only difference I can think of is that I am using a Dell Latitude 7440 "
        "while he has a ThinkPad X1 Carbon. I am on Windows 11 23H2 build 22631.3155.\n\n"
        "I should also mention that before the VPN issue started, I had been experiencing "
        "intermittent Wi-Fi drops at the London office, but I am not sure if that is related "
        "since I am currently working from home on a wired Ethernet connection (Virgin Media "
        "broadband, 500 Mbps down / 50 Mbps up).\n\n"
        "While we are on the topic of network issues, our team has also noticed that the "
        "Bloomberg terminal connections have been slower than usual, but again, that might be "
        "a separate infrastructure issue. I have heard rumors that the network team is planning "
        "another migration to Azure Virtual WAN, but I do not have details.\n\n"
        "Going back to the VPN: I also tried connecting to the alternate gateway "
        "(vpn-eu-west.contoso.com) with the same result. I ran a packet capture using Wireshark "
        "and can see the TLS handshake completing but then the RADIUS authentication fails. I "
        "have attached the pcap file but I realize it may not be useful without context.\n\n"
        "One more thing — I noticed that my AD account shows 'Password Last Set' as March 17, "
        "which is correct. But the 'Last Successful Logon' for the VPN service shows March 14, "
        "which was before the password change. This suggests the VPN infrastructure has not "
        "accepted my new credentials at all.\n\n"
        "Please prioritize this as I have been unable to work effectively for three days now "
        "and my manager is asking for daily updates on the risk models.\n\n"
        "--- Forwarded message ---\n"
        "From: Help Desk <helpdesk@contoso.com>\n"
        "Date: Mon, 17 Mar 2026 16:30:00 +0000\n"
        "To: Elena Vasquez <elena.vasquez@contoso.com>\n"
        "Subject: RE: VPN access\n\n"
        "Hi Elena, your ticket INC-4955 has been created. A technician will respond within 4 "
        "hours. In the meantime, please try clearing your Windows Credential Manager.\n\n"
        "Kind regards,\nIT Service Desk\nContoso Financial Services\n\n"
        "CONFIDENTIALITY NOTICE: This e-mail message, including any attachments, is for the sole "
        "use of the intended recipient(s) and may contain confidential and privileged information. "
        "Any unauthorized review, use, disclosure, or distribution is prohibited. If you are not "
        "the intended recipient, please contact the sender by reply e-mail and destroy all copies. "
        "Contoso Financial Services | 200 Park Avenue, New York, NY 10166\n"
        "Tel: +1 (212) 555-0199 | www.contoso.com\n\n"
        "This message has been scanned by Contoso Antivirus Gateway v4.12.1.\n"
        "No threats detected. Scan ID: AV-20260317-163000-HELPDESK-4955\n"
    )
    return EvalCase(
        ticket=EvalTicket(
            ticket_id="INC-DC-071",
            subject="Re: Re: FW: VPN not connecting after password change — follow-up",
            description=long_body,
            reporter=Reporter(
                name="Elena Vasquez",
                email="elena.vasquez@contoso.com",
                department="Risk Management",
            ),
            created_at="2026-03-20T08:30:00Z",
            channel=Channel.EMAIL,
        ),
        gold=GoldAnswer(
            ticket_id="INC-DC-071",
            category=Category.NETWORK,
            priority=Priority.P2,
            assigned_team=Team.NETWORK_OPS,
            needs_escalation=False,
            missing_information=[MissingInfoField.APPLICATION_VERSION],
            next_best_action=(
                "Investigate VPN authentication failure after password change for Elena Vasquez. "
                "GlobalProtect shows Invalid Credentials despite the new password working elsewhere. "
                "The deeply buried issue is a RADIUS/NPS credential sync failure."
            ),
            remediation_steps=[
                "Check RADIUS/NPS logs for the user authentication rejection reason.",
                "Verify AD password replication has completed to all domain controllers used by VPN.",
                "Clear cached VPN credentials on both the client and the RADIUS server.",
                "Test RADIUS authentication directly using NTRadPing or similar tool.",
                "If replication is confirmed, re-provision the GlobalProtect client profile.",
            ],
        ),
        tags=["long_content", "buried_issue", "forwarded_chain"],
        description="Very long email (10K+ chars) with the real VPN issue buried among tangential context.",
    )


def _dc072_base64_image_flood() -> EvalCase:
    """Multiple base64-encoded images flooding the ticket."""
    return EvalCase(
        ticket=EvalTicket(
            ticket_id="INC-DC-072",
            subject="Laptop screen flickering — screenshots inline",
            description=(
                "My laptop screen keeps flickering since the last driver update. "
                "Here are screenshots I took:\n\n"
                "[Screenshot 1 - screen during flicker]\n"
                "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAABAAAAQCYAAD/qcomAAAABHNCSVQICAgIfAhkiA"
                "AAAAlwSFlzAAALEwAACxMBAJqcGAAAAAd0SU1FB9oKFwgMNC3WkXYAACAASURBVHic7d15fFT1vf/x95lsk5ns"
                "G0kgCQlhCfsSAoooLohi3bV1adXaam/dWm1rW2uXW7u4tXZR691s7WLdam3rVq24sIjsyCb7FiAhIfu+Tc7v"
                "j0kIIZOQhExmJnk9H495nDlnzsx8k8Mj8p7v9/s1TNOUJFVVVen48eOqqamRw+FQXFycMjIylJubq6io==\n\n"
                "[Screenshot 2 - Device Manager view]\n"
                "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEASABIAAD/2wBDAAgGBgcGBQgHBwcJCQgKDBQNDAsLDB"
                "kSEw8UHRofHh0aHBwgJC4nICIsIxwcKDcpLDAxNDQ0Hyc5PTgyPC4zNDL/2wBDAQkJCQwLDBgNDRgyIRwhMj"
                "IyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjL/wAARCAEAAQADASIA"
                "AhEBAxEB/8QAHwAAAQUBAQEBAQEAAAAAAACDAwQFBgcICQoLBQHzKSECAAAAAElFTkSuQmCCXttzQ7ajGVwI==\n\n"
                "[Screenshot 3 - error dialog]\n"
                "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAKCAYAAACNMs+9AAAAFUlEQVQYV2P8z8BQ"
                "z0AEYBxVOHIVAvcHBQHzKSECAAAAAElFTkSuQmCCiVBORw0KGgoAAAANSUhEUgAAAAoAAAAKCAYAAACNMs+9AA"
                "AAFUlEQVQYV2P8z8BQz0AEYBxVOHIVAvcHBQHzKSECAAAAAElFTkSuQmCCiVBORw0KGgoAAAANSUhEUgAAAAo"
                "AAAAKCAYAAACNMs+9AAAAFUlEQVQYV2P8z8BQz0AEYBxVOHIVAvcHBQHzKSECAAAAAElFTkSuQmCC==\n\n"
                "[Screenshot 4 - Windows Event Viewer]\n"
                "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAABHNCSVQICAgIfAhk"
                "iAAAAAlwSFlzAAALEwAACxMBAJqcGAAAAAd0SU1FB9oKFwgMNC3WkXYAAAAAElFTkSuQmCCiVBORw0KGgoAAA"
                "ANSUhEUgAAACAAAAAgCAYAAABzenr0AAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAALEwAACxMBAJqcGAAAAAdO"
                "SU1FB9oKFwgMNC3WkXYAAAAAElFTkSuQmCCBQHzKSECAAAAAElFTkSuQmCC==\n\n"
                "[Screenshot 5 - display properties]\n"
                "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEASABIAADkBSyluO9K2kbzlh9UISyz5DwgdKTjYDu/ns"
                "6nYeuGwyQpl1qwx5ie3TmN3/iCf5U6chwnBnf/JPX6P0D7nREDEUfQOWKoUYcE53MKSgf5ni1rfXecz"
                "vBEnwXPZAVyqjPZjwgTu6avzxFZNox0VlqMGpVpbxBq6Kv2flat295Cv7N5VncZ5FscawtkrhrZtfSx0T"
                "WDAmYUZ4x3MvnNSBpW7ttz7ajGVwI7tMds9eyB34XShI8aumU33avwm67YOC2RmWXJ8Erk6iNbVmgKoKX==\n\n"
                "The laptop is a Dell Latitude 5540, Windows 11 23H2. The flicker started "
                "after the Intel Iris Xe driver was updated to version 31.0.101.5186 via "
                "Windows Update on Friday."
            ),
            reporter=Reporter(
                name="Carlos Mendoza",
                email="carlos.mendoza@contoso.com",
                department="Trading",
            ),
            created_at="2026-03-19T10:15:00Z",
            channel=Channel.EMAIL,
        ),
        gold=GoldAnswer(
            ticket_id="INC-DC-072",
            category=Category.HARDWARE,
            priority=Priority.P3,
            assigned_team=Team.ENDPOINT,
            needs_escalation=False,
            missing_information=[MissingInfoField.DEVICE_INFO],
            next_best_action=(
                "Investigate screen flickering on Dell Latitude 5540 after Intel Iris Xe driver "
                "update to 31.0.101.5186. The five inline base64 images are noise — roll back "
                "the display driver."
            ),
            remediation_steps=[
                "Roll back the Intel Iris Xe driver to the previous version via Device Manager.",
                "Check for known issues with Intel driver version 31.0.101.5186.",
                "If rollback resolves the issue, block this driver version in Intune.",
                "Test with an external monitor to isolate the issue.",
                "Submit a Windows Feedback Hub report if this is a confirmed regression.",
            ],
        ),
        tags=["base64", "multiple_images", "inline_binary"],
        description="Multiple base64-encoded screenshots flooding the description with minimal actual content.",
    )


def _dc073_base64_encoded_log() -> EvalCase:
    """Base64-encoded error log data (not an image)."""
    return EvalCase(
        ticket=EvalTicket(
            ticket_id="INC-DC-073",
            subject="Trade recon app crash — error log encoded",
            description=(
                "Our Java trade reconciliation application crashed again this morning. "
                "I exported the log but it got encoded. Here it is:\n\n"
                "RVJST1IgMjAyNi0wMy0xOCAwOToxNToyMiBbQXV0aE1vZHVsZV0gRmFpbGVkIHRvIHZhbGlkYXRl"
                "IE1GQSB0b2tlbiBmb3IgdXNlciBzYXJhaC5jaGVuQGNvbnRvc28uY29tLiBUb2tlbiBleHBpcmVkIGF0"
                "IDIwMjYtMDMtMThUMDk6MTA6MDBaLiBSZXRyeSBjb3VudDogMy4gTW9kdWxlOiBBenVyZUFELk1GQS5W"
                "YWxpZGF0b3IuIENvcnJlbGF0aW9uSWQ6IGE4ZjNjMmUxLTRiNWQtNGY2YS04YzlkLTBlMWYyYTNiNGM1"
                "ZGNBdRVM6FDx2sW33OIeLh8DG8vQpIB8WGumYZbW04hDCs1DXmWgketP07qWifhgu3OygIkC6N1rWz9nD"
                "heC4DA5ap5UgdlJb5sUjT3JdQS7ya1etZK9tyJ1B9vxDytuhaNT1qWxWWiWQKPK3tbKjbKPA5A8bDEM==\n\n"
                "The crash happens at 09:15 AM daily during the overnight trade batch. "
                "The app runs on srv-trade-recon-01 with 16 GB heap. "
                "The error is java.lang.OutOfMemoryError: Java heap space."
            ),
            reporter=Reporter(
                name="Robert Chen",
                email="robert.chen@contoso.com",
                department="Operations",
            ),
            created_at="2026-03-18T09:30:00Z",
            channel=Channel.EMAIL,
        ),
        gold=GoldAnswer(
            ticket_id="INC-DC-073",
            category=Category.SOFTWARE,
            priority=Priority.P2,
            assigned_team=Team.ENTERPRISE_APPS,
            needs_escalation=False,
            missing_information=[
                MissingInfoField.ENVIRONMENT_DETAILS,
                MissingInfoField.STEPS_TO_REPRODUCE,
            ],
            next_best_action=(
                "Investigate Java OutOfMemoryError in the trade reconciliation app on "
                "srv-trade-recon-01. Ignore the base64-encoded log dump — the issue is "
                "heap exhaustion during the morning batch job."
            ),
            remediation_steps=[
                "Review JVM heap allocation (-Xmx) and increase if needed.",
                "Analyze heap dump to find memory-intensive objects.",
                "Check for memory leaks in the batch processing code.",
                "Consider processing trades in smaller chunks.",
                "Add JVM monitoring with alerts for heap usage thresholds.",
            ],
        ),
        tags=["base64", "encoded_log", "application_crash"],
        description="Base64-encoded error log data (not image) pasted in a ticket about a Java OOM crash.",
    )


def _dc074_giant_signature() -> EvalCase:
    """Giant email signature dwarfing the actual issue."""
    return EvalCase(
        ticket=EvalTicket(
            ticket_id="INC-DC-074",
            subject="MFA push notifications not working",
            description=(
                "Hi, my MFA push notifications stopped working. The Authenticator app spins "
                "and then says Request timed out. Cannot log into anything.\n\n"
                "Raj Patel\nSVP, Wealth Management\nContoso Financial Services\n"
                "Direct: +1 (212) 555-0391 | Mobile: +1 (917) 555-0248\n"
                "Email: raj.patel@contoso.com\n200 Park Ave, 42nd Floor, NY 10166\n"
                "EA: Martha Wilson, +1 (212) 555-0393\n\n"
                "IMPORTANT LEGAL DISCLAIMER\n\n"
                "This email is sent by Contoso Financial Services and/or its subsidiaries "
                "(collectively Contoso). This email may contain confidential, proprietary, "
                "or legally privileged information. It is intended solely for the individual "
                "or entity to whom it is addressed. If you are not the named addressee, you "
                "should not disseminate, distribute, or copy this email. Please notify the "
                "sender immediately if you have received this email by mistake. Email cannot "
                "be guaranteed to be secure or error-free. The sender does not accept liability "
                "for any errors or omissions.\n\n"
                "REGULATORY INFORMATION\n\n"
                "Contoso Financial Services is authorized and regulated by the FCA under firm "
                "reference number 123456. Registered in England and Wales under company number "
                "12345678. Member of FINRA, SIPC, and NFA. NFA ID: 0123456.\n\n"
                "ENVIRONMENTAL NOTICE\n\n"
                "Please consider the environment before printing this email. Contoso is "
                "committed to achieving net-zero carbon emissions by 2035.\n\n"
                "PRIVACY NOTICE\n\n"
                "Contoso processes personal data in accordance with GDPR, CCPA, and applicable "
                "privacy laws. See www.contoso.com/privacy for details. Contact dpo@contoso.com "
                "to exercise your data subject rights.\n\n"
                "TAX DISCLAIMER\n\n"
                "Any tax advice in this communication was not intended or written to be used for "
                "avoiding tax-related penalties under the Internal Revenue Code.\n\n"
                "ANTI-MONEY LAUNDERING NOTICE\n\n"
                "Contoso is committed to combating money laundering and terrorist financing in "
                "compliance with the Bank Secrecy Act, USA PATRIOT Act, and applicable AML regs."
            ),
            reporter=Reporter(
                name="Raj Patel",
                email="raj.patel@contoso.com",
                department="Wealth Management",
            ),
            created_at="2026-03-18T08:00:00Z",
            channel=Channel.EMAIL,
        ),
        gold=GoldAnswer(
            ticket_id="INC-DC-074",
            category=Category.ACCESS_AUTH,
            priority=Priority.P2,
            assigned_team=Team.IAM,
            needs_escalation=False,
            missing_information=[MissingInfoField.ERROR_MESSAGE, MissingInfoField.DEVICE_INFO],
            next_best_action=(
                "Investigate MFA push notification timeout for Raj Patel. The massive legal "
                "disclaimer dwarfs the actual two-line issue. Check Azure AD MFA service health "
                "and the user's Authenticator app registration."
            ),
            remediation_steps=[
                "Check Azure AD MFA service health for outages.",
                "Verify the Authenticator app registration is current.",
                "Ensure push notifications are enabled on the user's device.",
                "Re-register the Authenticator app if registration is stale.",
                "Issue a temporary access pass for immediate access.",
            ],
        ),
        tags=["giant_signature", "legal_disclaimer", "buried_issue"],
        description="Two-line MFA issue buried under a massive multi-section legal disclaimer.",
    )


def _dc075_deep_reply_chain() -> EvalCase:
    """Extremely deep reply chain with 15+ levels of quoting."""
    return EvalCase(
        ticket=EvalTicket(
            ticket_id="INC-DC-075",
            subject="Re: Re: Re: Re: Re: Re: Re: Re: Re: Re: Printer jam Floor 7",
            description=(
                "Update: printer jamming again today. Same tray 2 issue.\n\n"
                "> Kevin Park wrote:\n"
                "> Cleared the jam. Should be fine now.\n>\n"
                "> > Janet Kim wrote:\n"
                "> > Jammed again. Third time today. Tray 2.\n> >\n"
                "> > > Kevin Park wrote:\n"
                "> > > Ordered replacement rollers. ETA Thursday. Use Tray 1.\n> > >\n"
                "> > > > Janet Kim wrote:\n"
                "> > > > Torn paper stuck near fuser unit.\n> > > >\n"
                "> > > > > Kevin Park wrote:\n"
                "> > > > > Cleaned feed rollers. Ran 10 test pages OK.\n> > > > >\n"
                "> > > > > > Janet Kim wrote:\n"
                "> > > > > > 7 jams today. Entire floor complaining.\n> > > > > >\n"
                "> > > > > > > Help Desk wrote:\n"
                "> > > > > > > Dispatching Kevin from Endpoint.\n> > > > > > >\n"
                "> > > > > > > > Janet Kim wrote:\n"
                "> > > > > > > > Paper jamming Tray 2, HP LaserJet M609.\n"
                "> > > > > > > > Floor 7 near 7B. Asset: WM-PRN-0891.\n> > > > > > > >\n"
                "> > > > > > > > > Janet Kim wrote:\n"
                "> > > > > > > > > Floor 7 printer jamming. Please help.\n> > > > > > > > >\n"
                "> > > > > > > > > > Auto-Attendant wrote:\n"
                "> > > > > > > > > > Ticket INC-4901 created. ETA 2 hours."
            ),
            reporter=Reporter(
                name="Janet Kim",
                email="janet.kim@contoso.com",
                department="Wealth Management",
            ),
            created_at="2026-03-20T09:00:00Z",
            channel=Channel.EMAIL,
        ),
        gold=GoldAnswer(
            ticket_id="INC-DC-075",
            category=Category.HARDWARE,
            priority=Priority.P3,
            assigned_team=Team.ENDPOINT,
            needs_escalation=False,
            missing_information=[MissingInfoField.DEVICE_INFO],
            next_best_action=(
                "Recurring paper jam in Tray 2 of HP LaserJet M609 on Floor 7 (WM-PRN-0891). "
                "Persists despite roller cleaning. Replace feed rollers and inspect fuser area."
            ),
            remediation_steps=[
                "Expedite Tray 2 feed roller replacement.",
                "Inspect fuser unit for torn paper fragments.",
                "Run a full print path cleaning cycle.",
                "Verify paper stock quality and orientation in Tray 2.",
                "Schedule HP service call if jam persists after roller replacement.",
            ],
        ),
        tags=["deep_quoting", "reply_chain", "excessive_nesting"],
        description="15+ levels of email quoting about a recurring printer jam.",
    )


def _dc076_severe_mojibake() -> EvalCase:
    """Garbled encoding (mojibake) scattered throughout real text."""
    return EvalCase(
        ticket=EvalTicket(
            ticket_id="INC-DC-076",
            subject="Can\u00e2\u0080\u0099t access shared drive \u00e2\u0080\u0094 permission denied",
            description=(
                "Hi IT,\n\n"
                "I\u00e2\u0080\u0099m getting a \u00e2\u0080\u009cpermission denied"
                "\u00e2\u0080\u009d error on \\\\fs-london-01\\wealth-mgmt\\reports. "
                "Worked fine until yesterday. Need Q1 portfolio files for a 2 PM meeting.\n\n"
                "Error: \u00e2\u0080\u009cYou do not have permission to access "
                "\\\\fs-london-01\\wealth-mgmt\\reports\u00e2\u0080\u009d\n\n"
                "Colleague \u00c3\u0089lodie Martin can still access it. London office, "
                "Building 2, 4th floor. Login: CONTOSO\\a.williams. "
                "Lenovo ThinkPad T14 Gen 4.\n\n"
                "Folder name shows as \u00e2\u0080\u009cQ1_2026_Valu\u00c3\u00a4tion_"
                "Rep\u00c3\u00b6rts\u00e2\u0080\u009d instead of "
                "\u00e2\u0080\u009cQ1_2026_Valuation_Reports\u00e2\u0080\u009d.\n\n"
                "Please fix ASAP.\n\nThanks,\nAlicia Williams"
            ),
            reporter=Reporter(
                name="Alicia Williams",
                email="alicia.williams@contoso.com",
                department="Portfolio Management",
            ),
            created_at="2026-03-18T10:30:00Z",
            channel=Channel.EMAIL,
        ),
        gold=GoldAnswer(
            ticket_id="INC-DC-076",
            category=Category.DATA_STORAGE,
            priority=Priority.P3,
            assigned_team=Team.DATA_PLATFORM,
            needs_escalation=False,
            missing_information=[MissingInfoField.AFFECTED_SYSTEM, MissingInfoField.NETWORK_LOCATION],
            next_best_action=(
                "Investigate file share access denial for CONTOSO\\a.williams on "
                "\\\\fs-london-01\\wealth-mgmt\\reports. The mojibake is noise — "
                "the core issue is sudden loss of read access."
            ),
            remediation_steps=[
                "Check the user's AD group membership for the wealth-mgmt share ACL.",
                "Review recent changes to the file server share permissions.",
                "Verify the user's Kerberos ticket is valid.",
                "Compare access tokens with colleague who still has access.",
                "Reset SMB session and retry.",
            ],
        ),
        tags=["mojibake", "encoding_corruption", "scattered_garble"],
        description="Mojibake (double-encoded UTF-8) scattered throughout a file share access issue.",
    )


def _dc077_json_config_dump() -> EvalCase:
    """Massive JSON ARM template dump pasted inline."""
    return EvalCase(
        ticket=EvalTicket(
            ticket_id="INC-DC-077",
            subject="Azure deployment timeout — ARM template included",
            description=(
                "Deployment to staging failed with timeout. Here is the ARM template:\n\n"
                '{"$schema": "https://schema.management.azure.com/schemas/2019-04-01/'
                'deploymentTemplate.json#", "contentVersion": "1.0.0.0", "parameters": '
                '{"environment": {"type": "string", "defaultValue": "staging"}, '
                '"vmSize": {"type": "string", "defaultValue": "Standard_D4s_v3"}, '
                '"location": {"type": "string", "defaultValue": "[resourceGroup().location]"}, '
                '"vnetAddressPrefix": {"type": "string", "defaultValue": "10.0.0.0/16"}, '
                '"subnetPrefix": {"type": "string", "defaultValue": "10.0.1.0/24"}, '
                '"storageAccountType": {"type": "string", "defaultValue": "Standard_LRS"}, '
                '"nsgName": {"type": "string", "defaultValue": "staging-nsg"}, '
                '"appGwName": {"type": "string", "defaultValue": "staging-appgw"}, '
                '"lbName": {"type": "string", "defaultValue": "staging-lb"}}, '
                '"variables": {"nicName": "[concat(parameters(\\\'environment\\\'), \\\'-nic\\\')]", '
                "\"vnetName\": \"[concat(parameters(\\'environment\\'), \\'-vnet\\')]\"}, "
                '"resources": [{"type": "Microsoft.Network/virtualNetworks", '
                '"apiVersion": "2023-05-01", "name": "[variables(\\\'vnetName\\\')]"}]}\n\n'
                "Deployment ran 45 min then timed out at VNet creation. "
                "Error: ProvisioningState: TimedOut. Correlation ID: "
                "d8f3c2e1-4b5d-4f6a-8c9d-0e1f2a3b4c5d. "
                "Need this before Thursday UAT."
            ),
            reporter=Reporter(
                name="Nora Fischer",
                email="nora.fischer@contoso.com",
                department="Cloud Infrastructure",
            ),
            created_at="2026-03-18T14:00:00Z",
            channel=Channel.PORTAL,
        ),
        gold=GoldAnswer(
            ticket_id="INC-DC-077",
            category=Category.SOFTWARE,
            priority=Priority.P2,
            assigned_team=Team.ENTERPRISE_APPS,
            needs_escalation=False,
            missing_information=[MissingInfoField.ERROR_MESSAGE, MissingInfoField.ENVIRONMENT_DETAILS],
            next_best_action=(
                "Investigate Azure ARM template deployment timeout for staging environment. "
                "The inline JSON is noise — the real issue is VNet creation timing out."
            ),
            remediation_steps=[
                "Check Azure subscription resource quotas for the target region.",
                "Review Activity Log for the deployment correlation ID.",
                "Verify region capacity for Standard_D4s_v3.",
                "Retry with a longer timeout or deploy incrementally.",
                "Check Azure service health at status.azure.com.",
            ],
        ),
        tags=["json_config_dump", "inline_config", "deployment_issue"],
        description="Massive ARM template JSON pasted inline in a ticket about a deployment timeout.",
    )


def _dc078_code_switching() -> EvalCase:
    """Trilingual code-switching (English/Chinese/Spanish)."""
    return EvalCase(
        ticket=EvalTicket(
            ticket_id="INC-DC-078",
            subject="Email delivery delay / \u7535\u5b50\u90ae\u4ef6\u5ef6\u8fdf",
            description=(
                "\u4f60\u597d IT team,\n\n"
                "I have email delivery delays. \u6211\u7684\u90ae\u4ef6\u53d1\u9001\u540e"
                "\u8981\u7b49\u5f88\u4e45 (30-40 minutes).\n\n"
                "Esto afecta a nuestro equipo de trading en Singapore. "
                "Los correos internos tambi\u00e9n est\u00e1n lentos.\n\n"
                "\u95ee\u9898\u4ece\u4e0a\u5468\u4e94\u5f00\u59cb. External emails "
                "affected more than internal. \u6211\u4eec\u7528 Outlook 2024 on Win 11.\n\n"
                "\u8c22\u8c22 / Gracias / Thanks,\nWei-Chen Huang\nCross-Border Trading"
            ),
            reporter=Reporter(
                name="Wei-Chen Huang",
                email="wei-chen.huang@contoso.com",
                department="Institutional Trading",
            ),
            created_at="2026-03-18T11:00:00Z",
            channel=Channel.EMAIL,
        ),
        gold=GoldAnswer(
            ticket_id="INC-DC-078",
            category=Category.SOFTWARE,
            priority=Priority.P3,
            assigned_team=Team.ENTERPRISE_APPS,
            needs_escalation=False,
            missing_information=[MissingInfoField.AFFECTED_USERS, MissingInfoField.TIMESTAMP],
            next_best_action=(
                "Investigate email delivery delays (30-40 min) for Singapore trading team. "
                "The trilingual code-switching is noise — check Exchange mail flow."
            ),
            remediation_steps=[
                "Check Exchange Online message trace for delivery bottlenecks.",
                "Review mail flow rules for the Singapore office.",
                "Check if delays affect specific domains or all recipients.",
                "Investigate transport queue health and throttling.",
                "Verify DNS MX record resolution from Singapore.",
            ],
        ),
        tags=["code_switching", "multilingual", "trilingual"],
        description="Trilingual code-switching (English/Chinese/Spanish) in an email delay ticket.",
    )


def _dc079_url_spam() -> EvalCase:
    """Newsletter with 30+ tracking URLs burying a sync issue."""
    return EvalCase(
        ticket=EvalTicket(
            ticket_id="INC-DC-079",
            subject="FW: SharePoint sync broken + newsletter",
            description=(
                "Hi, forwarding my request that got buried in a newsletter.\n\n"
                "OneDrive sync stopped — red X, 'Sync pending', ~2 GB waiting.\n\n"
                "--- Contoso Weekly Newsletter ---\n"
                "Read online: https://contoso.com/newsletter?utm_source=email&utm_medium=internal"
                "&utm_campaign=weekly_w12&mkt_tok=NDc2LVRYUS0xNzQA\n"
                "1. Q1 Preview https://contoso.com/q1?ref=nl&sid=abc&utm_source=email&click=x7y8\n"
                "2. SG Office https://contoso.com/sg?ref=nl&sid=def&utm_source=email&trk=mmm\n"
                "3. ESG Report https://contoso.com/esg?utm_source=email&campaign=esg2025\n"
                "4. Tech Update https://contoso.com/tech?ref=w12&utm_source=email&mkt=token\n"
                "5. Compliance https://contoso.com/comp?session=Q2&utm_source=email\n"
                "Events: https://contoso.com/townhall?id=TH03&utm=email&register=true\n"
                "Wellness: https://contoso.com/wellness?id=WW26&utm=email&signup=true\n"
                "Hackathon: https://contoso.com/hack?id=H26&utm=email&register=true\n"
                "Benefits: https://contoso.com/benefits?period=2026&utm=email\n"
                "401k: https://contoso.com/401k?update=Q1&utm=email\n"
                "Unsubscribe: https://contoso.com/unsub?id=12345&utm=email\n"
                "Privacy: https://contoso.com/privacy?ref=footer&utm=email\n"
                "--- End Newsletter ---\n\n"
                "SharePoint library: https://contoso.sharepoint.com/sites/wealth-mgmt/Docs "
                "OneDrive version 24.030.0213.0002."
            ),
            reporter=Reporter(
                name="Sophia Martinez",
                email="sophia.martinez@contoso.com",
                department="Client Services",
            ),
            created_at="2026-03-18T09:45:00Z",
            channel=Channel.EMAIL,
        ),
        gold=GoldAnswer(
            ticket_id="INC-DC-079",
            category=Category.DATA_STORAGE,
            priority=Priority.P3,
            assigned_team=Team.DATA_PLATFORM,
            needs_escalation=False,
            missing_information=[MissingInfoField.ERROR_MESSAGE, MissingInfoField.AFFECTED_SYSTEM],
            next_best_action=(
                "Investigate OneDrive sync failure (red X, Sync pending, ~2 GB queued). "
                "The 15+ newsletter tracking URLs are noise. Check OneDrive client logs."
            ),
            remediation_steps=[
                "Check OneDrive sync client logs for specific error codes.",
                "Verify client version meets minimum requirements.",
                "Check for files exceeding size or path length limits.",
                "Reset OneDrive sync (onedrive.exe /reset).",
                "Check SharePoint Online storage quota.",
            ],
        ),
        tags=["url_spam", "tracking_urls", "newsletter_noise"],
        description="SharePoint sync issue buried in a forwarded newsletter with 15+ tracking URLs.",
    )


def _dc080_email_metadata_noise() -> EvalCase:
    """Raw email headers (MIME, DKIM, SPF) pasted into description."""
    return EvalCase(
        ticket=EvalTicket(
            ticket_id="INC-DC-080",
            subject="Teams call quality — choppy audio",
            description=(
                "MIME-Version: 1.0\n"
                'Content-Type: multipart/alternative; boundary="----=_Part_12345"\n'
                "X-Mailer: Microsoft Outlook 16.0.18025.20160\n"
                "X-MS-Exchange-Organization-SCL: 0\n"
                "X-MS-Exchange-Organization-AuthAs: Internal\n"
                "Authentication-Results: spf=pass smtp.mailfrom=contoso.com;\n"
                " dkim=pass header.d=contoso.com; dmarc=pass header.from=contoso.com;\n"
                "Received: from mail-east.contoso.com (10.0.0.5) by mail-hub.contoso.com\n"
                " with SMTP id 15.2.1118.40; Mon, 18 Mar 2026 11:20:00 -0400\n"
                "DKIM-Signature: v=1; a=rsa-sha256; d=contoso.com; s=selector1;\n"
                " bh=47DEQpj8HBSa+/TImW+5JCeuQeRkm5NMpJWZG3hSuFU=;\n"
                " b=dGhpcyBpcyBub3QgYSByZWFsIERLSU0gc2lnbmF0dXJl\n\n"
                "------=_Part_12345\n"
                "Content-Type: text/plain; charset=UTF-8\n\n"
                "Hi IT,\n\n"
                "Choppy audio on Teams calls for the past two days. Audio cuts in and out "
                "every few seconds. Video and screen sharing are fine. Colleagues say I "
                "sound robotic.\n\n"
                "London office, Building 2, 8th floor. Jabra Evolve2 75 via USB. "
                "Teams 24053.811.3099. ThinkPad X1 Carbon Gen 11 on Wi-Fi.\n\n"
                "Thanks,\nAkira Morimoto\nQuantitative Analysis"
            ),
            reporter=Reporter(
                name="Akira Morimoto",
                email="akira.morimoto@contoso.com",
                department="Quantitative Analysis",
            ),
            created_at="2026-03-18T11:20:00Z",
            channel=Channel.EMAIL,
        ),
        gold=GoldAnswer(
            ticket_id="INC-DC-080",
            category=Category.NETWORK,
            priority=Priority.P2,
            assigned_team=Team.NETWORK_OPS,
            needs_escalation=False,
            missing_information=[MissingInfoField.NETWORK_LOCATION, MissingInfoField.AFFECTED_USERS],
            next_best_action=(
                "Investigate choppy Teams audio in London Building 2, 8th floor. The raw "
                "email headers and MIME data are noise — the issue is degraded voice quality "
                "likely caused by Wi-Fi congestion or QoS misconfiguration."
            ),
            remediation_steps=[
                "Check Wi-Fi signal quality on Building 2, 8th floor.",
                "Run Teams network assessment for jitter and packet loss.",
                "Test with Ethernet to rule out wireless issues.",
                "Update Jabra Evolve2 75 firmware.",
                "Verify QoS policies tag Teams audio traffic correctly.",
            ],
        ),
        tags=["email_metadata", "mime_headers", "raw_headers"],
        description="Raw MIME/DKIM/SPF email headers pasted into a Teams audio quality ticket.",
    )


# ---------------------------------------------------------------------------
# dc081–dc100 — Additional data-cleanup scenarios
# ---------------------------------------------------------------------------


def _dc081_pgp_signed_request() -> EvalCase:
    """PGP-signed message wrapping a TLS certificate renewal."""
    return EvalCase(
        ticket=EvalTicket(
            ticket_id="INC-DC-081",
            subject="TLS cert renewal for api.contoso.com",
            description=(
                "-----BEGIN PGP SIGNED MESSAGE-----\nHash: SHA256\n\n"
                "The TLS certificate for api.contoso.com expires on 2026-03-25.\n"
                "CN=api.contoso.com, O=Contoso Financial Services\n"
                "Issuer: DigiCert SHA2 Extended Validation Server CA\n"
                "Please renew before expiration. CSR is staged on the app gateway.\n\n"
                "-----BEGIN PGP SIGNATURE-----\n"
                "iQIzBAEBCAAdFiEEABCDEFGHIJKLMNOPQRSTUVWXYZabcdef\n"
                "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnop==\n"
                "=Xz9Y\n-----END PGP SIGNATURE-----"
            ),
            reporter=Reporter(
                name="Victor Reyes",
                email="v.reyes@contoso.com",
                department="IT Security",
            ),
            created_at="2026-03-18T07:00:00Z",
            channel=Channel.EMAIL,
        ),
        gold=GoldAnswer(
            ticket_id="INC-DC-081",
            category=Category.SECURITY,
            priority=Priority.P1,
            assigned_team=Team.SECURITY_OPS,
            needs_escalation=True,
            missing_information=[MissingInfoField.ENVIRONMENT_DETAILS],
            next_best_action=(
                "Renew TLS certificate for api.contoso.com before March 25 expiration. "
                "PGP signature wrapping is noise — the request is a standard cert renewal."
            ),
            remediation_steps=[
                "Verify CSR on the application gateway.",
                "Submit renewal request to DigiCert.",
                "Install renewed certificate on all endpoints.",
                "Validate certificate chain and OCSP stapling.",
            ],
        ),
        tags=["pgp", "signature", "crypto_noise"],
        description="PGP ASCII-armored signature wrapping a TLS cert renewal request.",
    )


def _dc082_syslog_dump() -> EvalCase:
    """Linux syslog lines pasted into ticket about disk full."""
    return EvalCase(
        ticket=EvalTicket(
            ticket_id="INC-DC-082",
            subject="Risk calc service down — disk full on app-risk-01",
            description=(
                "Mar 18 06:15:22 app-risk-01 kernel: EXT4-fs warning: index full\n"
                "Mar 18 06:30:15 app-risk-01 risk-calc[8890]: ERROR: No space left on device\n"
                "Mar 18 06:30:15 app-risk-01 risk-calc[8890]: FATAL: Cannot write temp\n"
                "Mar 18 06:30:16 app-risk-01 systemd[1]: risk-calc.service: Failed\n"
                "Mar 18 06:30:18 app-risk-01 risk-calc[8920]: Starting...\n"
                "Mar 18 06:30:19 app-risk-01 risk-calc[8920]: ERROR: No space left on device\n\n"
                "df -h: /dev/sda1 100%. Old log files not rotated. Risk calculations down."
            ),
            reporter=Reporter(
                name="Nikolai Petrov",
                email="n.petrov@contoso.com",
                department="Risk Management",
            ),
            created_at="2026-03-18T06:45:00Z",
            channel=Channel.PORTAL,
        ),
        gold=GoldAnswer(
            ticket_id="INC-DC-082",
            category=Category.DATA_STORAGE,
            priority=Priority.P1,
            assigned_team=Team.DATA_PLATFORM,
            needs_escalation=True,
            missing_information=[MissingInfoField.AFFECTED_USERS, MissingInfoField.BUSINESS_IMPACT],
            next_best_action=(
                "Clear disk space on app-risk-01 and restart risk-calc service. "
                "The syslog dump shows /dev/sda1 at 100%% due to unrotated logs."
            ),
            remediation_steps=[
                "SSH to app-risk-01 and clean old logs in /var/log.",
                "Implement logrotate for risk-calc logs.",
                "Restart risk-calc.service after space freed.",
                "Add disk usage alert at 85% threshold.",
            ],
        ),
        tags=["syslog", "log_dump", "disk_full"],
        description="Syslog dump from a Linux server with disk-full errors.",
    )


def _dc083_tnef_winmail() -> EvalCase:
    """TNEF/winmail.dat artifacts around a swollen battery report."""
    return EvalCase(
        ticket=EvalTicket(
            ticket_id="INC-DC-083",
            subject="Laptop battery swelling — safety concern",
            description=(
                'Content-Type: application/ms-tnef; name="winmail.dat"\n\n'
                "MAPI_BODY_PLAIN:\nMy ThinkPad X1 Carbon Gen 11 (LT-NYC-3391) battery "
                "is visibly swollen. Trackpad raised, bottom bulging. Worried about fire. "
                "Unplugged, moved away from papers. Floor 22, desk 22-14.\nMAPI_END\n"
                "Attachment: winmail.dat (2.3 KB)"
            ),
            reporter=Reporter(
                name="Thomas Grant",
                email="t.grant@contoso.com",
                department="Legal",
            ),
            created_at="2026-03-18T09:00:00Z",
            channel=Channel.EMAIL,
        ),
        gold=GoldAnswer(
            ticket_id="INC-DC-083",
            category=Category.HARDWARE,
            priority=Priority.P1,
            assigned_team=Team.ENDPOINT,
            needs_escalation=True,
            missing_information=[],
            next_best_action=(
                "Handle swollen battery as safety priority. TNEF/winmail.dat is email "
                "format noise — issue is a swelling Li-ion battery on Floor 22."
            ),
            remediation_steps=[
                "Contact user immediately for safe battery removal.",
                "Do NOT charge or use the laptop.",
                "Arrange Lenovo warranty replacement.",
                "Inspect nearby devices for similar issues.",
            ],
        ),
        tags=["tnef", "winmail", "outlook_format"],
        description="Outlook Rich Text (TNEF) binary artifacts wrapping a safety issue.",
    )


def _dc084_kubectl_describe() -> EvalCase:
    """Kubernetes pod describe output for OOMKilled containers."""
    return EvalCase(
        ticket=EvalTicket(
            ticket_id="INC-DC-084",
            subject="Payment reconciliation pods crashing in loop",
            description=(
                "kubectl describe pod payment-recon-7f8b9c6d5-x2k4j -n payments:\n"
                "Name: payment-recon-7f8b9c6d5-x2k4j\n"
                "Status: CrashLoopBackOff\nContainers:\n  payment-recon:\n"
                "    Image: contoso.azurecr.io/payment-recon:3.1.0\n"
                "    Last State: Terminated (OOMKilled, exit code 137)\n"
                "    Restart Count: 42\n    Limits: memory: 512Mi\n"
                "Events:\n  Warning  OOMKilled  Pod exceeded memory limit\n\n"
                "All 3 replicas OOMKilled since v3.1.0 deployed Monday."
            ),
            reporter=Reporter(
                name="Kenji Watanabe",
                email="k.watanabe@contoso.com",
                department="Backend Engineering",
            ),
            created_at="2026-03-18T06:15:00Z",
            channel=Channel.CHAT,
        ),
        gold=GoldAnswer(
            ticket_id="INC-DC-084",
            category=Category.SOFTWARE,
            priority=Priority.P1,
            assigned_team=Team.ENTERPRISE_APPS,
            needs_escalation=True,
            missing_information=[MissingInfoField.BUSINESS_IMPACT],
            next_best_action=(
                "Increase memory limits for payment-recon pods from 512Mi to at least 1Gi. "
                "kubectl describe is diagnostic noise — root cause is OOMKilled on v3.1.0."
            ),
            remediation_steps=[
                "Increase deployment memory limit to 1Gi.",
                "Roll out updated deployment spec.",
                "Monitor pod restarts after change.",
                "Profile memory usage of v3.1.0 batch processing.",
            ],
        ),
        tags=["kubernetes", "kubectl", "pod_describe"],
        description="Full kubectl describe pod output with OOMKilled container state.",
    )


def _dc085_grafana_json_alert() -> EvalCase:
    """Grafana alert JSON payload about SQL Server memory."""
    return EvalCase(
        ticket=EvalTicket(
            ticket_id="INC-DC-085",
            subject="[ALERT] HighMemoryUsage on sqlprod03 — CRITICAL",
            description=(
                'Grafana alert:\n{"status":"firing","labels":{"alertname":"HighMemoryUsage",'
                '"instance":"sqlprod03:9100","severity":"critical"},'
                '"annotations":{"summary":"Memory usage above 95% for 10 min"},'
                '"values":{"mem_used_bytes":68451041280,"mem_total_bytes":70368744177664,'
                '"swap_used_bytes":17179869184}}\n\n'
                "Third critical alert this week. New analytics queries deployed Monday "
                "consuming all RAM on the SQL Server."
            ),
            reporter=Reporter(
                name="Monitoring System",
                email="alerts@contoso.com",
                department="IT Operations",
            ),
            created_at="2026-03-18T07:45:00Z",
            channel=Channel.EMAIL,
        ),
        gold=GoldAnswer(
            ticket_id="INC-DC-085",
            category=Category.DATA_STORAGE,
            priority=Priority.P2,
            assigned_team=Team.DATA_PLATFORM,
            needs_escalation=False,
            missing_information=[MissingInfoField.AFFECTED_USERS],
            next_best_action=(
                "Investigate memory-intensive analytics queries on sqlprod03 deployed Monday. "
                "JSON alert payload is structured noise — the issue is SQL Server memory pressure."
            ),
            remediation_steps=[
                "Identify the new analytics queries consuming memory.",
                "Optimize query plans or add resource governor limits.",
                "Consider adding memory to sqlprod03.",
                "Set up memory usage trending alerts.",
            ],
        ),
        tags=["monitoring", "json_alert", "grafana"],
        description="Grafana monitoring alert with JSON metrics payload.",
    )


def _dc086_ics_calendar_event() -> EvalCase:
    """ICS/vCalendar data pasted with a room display sync issue."""
    return EvalCase(
        ticket=EvalTicket(
            ticket_id="INC-DC-086",
            subject="Conference room display not syncing with Exchange",
            description=(
                "BEGIN:VCALENDAR\nVERSION:2.0\nPRODID:-//Microsoft Corporation//Outlook\n"
                "BEGIN:VEVENT\nDTSTART:20260318T130000Z\nDTEND:20260318T140000Z\n"
                "SUMMARY:Client Strategy Review\nLOCATION:Boardroom C - NYC 22F\n"
                "ORGANIZER;CN=Amanda Foster:mailto:a.foster@contoso.com\n"
                "END:VEVENT\nEND:VCALENDAR\n\n"
                "Crestron display outside Boardroom C shows 'Available' but meetings "
                "are booked. Exchange calendar is correct. Started after room mailbox "
                "migration from on-prem last week."
            ),
            reporter=Reporter(
                name="Amanda Foster",
                email="a.foster@contoso.com",
                department="Executive Operations",
            ),
            created_at="2026-03-18T12:00:00Z",
            channel=Channel.PHONE,
        ),
        gold=GoldAnswer(
            ticket_id="INC-DC-086",
            category=Category.HARDWARE,
            priority=Priority.P2,
            assigned_team=Team.ENDPOINT,
            needs_escalation=False,
            missing_information=[MissingInfoField.DEVICE_INFO],
            next_best_action=(
                "Reconfigure Crestron display to sync with Exchange Online after "
                "on-prem mailbox migration. ICS data is noise — issue is display sync."
            ),
            remediation_steps=[
                "Reconfigure Crestron display connection to Exchange Online.",
                "Verify room mailbox permissions after migration.",
                "Test real-time calendar sync.",
                "Update Crestron firmware if needed.",
            ],
        ),
        tags=["ics", "calendar", "vcalendar"],
        description="ICS/vCalendar data pasted with a conference room display issue.",
    )


def _dc087_broken_mime_boundary() -> EvalCase:
    """Corrupted MIME boundary with binary data leaking into text."""
    return EvalCase(
        ticket=EvalTicket(
            ticket_id="INC-DC-087",
            subject="Monitor flickering since docking station update",
            description=(
                'Content-Type: multipart/mixed; boundary="----=_Part_BROKEN"\n\n'
                "------=_Part_BROKEN\nContent-Type: text/plain; charset=UTF-8\n\n"
                "Monitor keeps flickering every few seconds since docking station "
                "firmware update yesterday. Dell U2722D via USB-C on Latitude 5540.\n\n"
                "------=_Part_BROKEN\nContent-Type: image/png\n"
                "Content-Transfer-Encoding: base64\n\n"
                "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAA\n"
                "DUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg==\n"
                "------=_Part_BROKEN--\n\n"
                "Have a client demo tomorrow."
            ),
            reporter=Reporter(
                name="Rachel Kim",
                email="r.kim@contoso.com",
                department="Trading",
            ),
            created_at="2026-03-18T09:30:00Z",
            channel=Channel.EMAIL,
        ),
        gold=GoldAnswer(
            ticket_id="INC-DC-087",
            category=Category.HARDWARE,
            priority=Priority.P2,
            assigned_team=Team.ENDPOINT,
            needs_escalation=False,
            missing_information=[MissingInfoField.DEVICE_INFO],
            next_best_action=(
                "Troubleshoot monitor flickering after docking station firmware update. "
                "Broken MIME boundary and base64 image are email format noise."
            ),
            remediation_steps=[
                "Roll back docking station firmware if possible.",
                "Test with a different USB-C cable.",
                "Update Dell U2722D monitor firmware.",
                "Test on a different docking station.",
            ],
        ),
        tags=["mime", "binary_leak", "encoding_corruption"],
        description="Corrupted multipart MIME with binary PNG data leaking into text.",
    )


def _dc088_mixed_encoding_mojibake() -> EvalCase:
    """Latin-1 vs UTF-8 encoding collision producing mojibake."""
    return EvalCase(
        ticket=EvalTicket(
            ticket_id="INC-DC-088",
            subject="CRM cannot save accented client names",
            description=(
                "Names are getting garbled in Dynamics 365:\n"
                "Expected: José García-López → Saved as: JosÃ© GarcÃ\\xada-LÃ³pez\n"
                "Expected: François Müller → Saved as: FranÃ§ois MÃ¼ller\n"
                "Expected: Zürich Office → Saved as: ZÃ¼rich Office\n\n"
                "Data import from legacy CRM used Latin-1 encoding. Dynamics 365 "
                "is UTF-8. About 300 client records affected in the EMEA region."
            ),
            reporter=Reporter(
                name="Carmen Delgado",
                email="c.delgado@contoso.com",
                department="Client Services",
            ),
            created_at="2026-03-18T10:30:00Z",
            channel=Channel.PORTAL,
        ),
        gold=GoldAnswer(
            ticket_id="INC-DC-088",
            category=Category.SOFTWARE,
            priority=Priority.P2,
            assigned_team=Team.ENTERPRISE_APPS,
            needs_escalation=False,
            missing_information=[MissingInfoField.AFFECTED_USERS],
            next_best_action=(
                "Fix encoding mismatch in CRM data import pipeline. The mojibake "
                "examples show Latin-1 data being interpreted as UTF-8."
            ),
            remediation_steps=[
                "Re-encode affected records from Latin-1 to UTF-8.",
                "Fix the import pipeline to specify source charset.",
                "Validate all 300 EMEA client records.",
                "Add charset detection to future imports.",
            ],
        ),
        tags=["encoding", "mojibake", "latin1_utf8"],
        description="Latin-1 to UTF-8 encoding collision producing mojibake in CRM records.",
    )


def _dc089_terraform_plan_output() -> EvalCase:
    """Terraform plan diff showing destructive change."""
    return EvalCase(
        ticket=EvalTicket(
            ticket_id="INC-DC-089",
            subject="Terraform plan wants to destroy production load balancer",
            description=(
                "terraform plan output:\n"
                "  # azurerm_lb.prod_lb will be destroyed\n"
                '  - resource "azurerm_lb" "prod_lb" {\n'
                '      - name = "lb-prod" - sku = "Standard" }\n'
                '  + resource "azurerm_lb" "prod_lb_v2" { + name = "lb-prod-v2" }\n'
                "Plan: 1 to add, 0 to change, 1 to destroy.\n\n"
                "Someone renamed the LB in config without terraform state mv. "
                "Would cause 5-10 min outage. DO NOT APPLY."
            ),
            reporter=Reporter(
                name="Alex Thornton",
                email="a.thornton@contoso.com",
                department="Cloud Infrastructure",
            ),
            created_at="2026-03-18T16:00:00Z",
            channel=Channel.PORTAL,
        ),
        gold=GoldAnswer(
            ticket_id="INC-DC-089",
            category=Category.NETWORK,
            priority=Priority.P1,
            assigned_team=Team.NETWORK_OPS,
            needs_escalation=True,
            missing_information=[MissingInfoField.ENVIRONMENT_DETAILS],
            next_best_action=(
                "Prevent accidental destruction of production load balancer. "
                "Terraform diff is context — fix state with terraform state mv."
            ),
            remediation_steps=[
                "Run terraform state mv to align state with new resource name.",
                "Verify plan shows no destructive changes after state fix.",
                "Add lifecycle prevent_destroy to critical resources.",
                "Review IaC change process to require plan approval.",
            ],
        ),
        tags=["terraform", "iac", "destructive_plan"],
        description="Terraform plan output showing destructive load balancer change.",
    )


def _dc090_stacked_signatures() -> EvalCase:
    """5+ email signatures from forwarding chain."""
    return EvalCase(
        ticket=EvalTicket(
            ticket_id="INC-DC-090",
            subject="Fwd: Fwd: Fwd: Guest Wi-Fi not working in London",
            description=(
                "See below — guest Wi-Fi is down in London.\n\n"
                "-- \nRebecca Taylor | IT Coordinator | London\nContoso Financial Services\n"
                "Tel: +44 20 7946 0958\n\n"
                "---------- Forwarded ----------\nFrom: David Park\n"
                "Rebecca, can you escalate? Our client can't present.\n\n"
                "-- \nDavid Park | SVP Institutional Sales | London\n"
                "Tel: +44 20 7946 0234\n\n"
                "---------- Forwarded ----------\nFrom: guest@external.com\n"
                "Cannot connect to Contoso-Guest Wi-Fi. Captive portal shows an error page. "
                "I have a meeting in Room 4B in 20 minutes.\n\n"
                "-- \nJohn External | Acme Corp"
            ),
            reporter=Reporter(
                name="Rebecca Taylor",
                email="r.taylor@contoso.com",
                department="IT",
            ),
            created_at="2026-03-18T13:30:00Z",
            channel=Channel.EMAIL,
        ),
        gold=GoldAnswer(
            ticket_id="INC-DC-090",
            category=Category.NETWORK,
            priority=Priority.P2,
            assigned_team=Team.NETWORK_OPS,
            needs_escalation=False,
            missing_information=[MissingInfoField.ERROR_MESSAGE, MissingInfoField.NETWORK_LOCATION],
            next_best_action=(
                "Fix guest Wi-Fi captive portal in London office. "
                "Stacked forwarding signatures are noise — real issue is from external guest."
            ),
            remediation_steps=[
                "Check captive portal service status in London.",
                "Verify RADIUS/NPS for guest network authentication.",
                "Test guest Wi-Fi connection from London office.",
                "Check DHCP pool for guest VLAN.",
            ],
        ),
        tags=["signatures", "forwarding_chain", "noise"],
        description="Multiple stacked email signatures from forwarding chain.",
    )


def _dc091_unicode_escapes() -> EvalCase:
    """Backslash-u escape sequences instead of actual characters."""
    return EvalCase(
        ticket=EvalTicket(
            ticket_id="INC-DC-091",
            subject="Can\\u2019t access shared drive after password reset",
            description=(
                "I reset my password this morning and now I can\\u2019t access the "
                "shared drive at \\\\\\\\fs01.contoso.local\\\\Finance$. I get \\u201cAccess "
                "Denied\\u201d every time. Username: l.garc\\u00eda@contoso.com.\n\n"
                "Tried logging out and back in, running \\u201cnet use\\u201d to remap, "
                "clearing credential manager. Nothing works. I need access for the "
                "board meeting at 2\\u00a0PM today."
            ),
            reporter=Reporter(
                name="Lucia Garcia",
                email="l.garcia@contoso.com",
                department="Finance",
            ),
            created_at="2026-03-18T10:00:00Z",
            channel=Channel.PORTAL,
        ),
        gold=GoldAnswer(
            ticket_id="INC-DC-091",
            category=Category.ACCESS_AUTH,
            priority=Priority.P2,
            assigned_team=Team.IAM,
            needs_escalation=False,
            missing_information=[],
            next_best_action=(
                "Restore shared drive access after password reset. Unicode escape "
                "sequences are rendering artifacts — user cannot access Finance$ share."
            ),
            remediation_steps=[
                "Verify Kerberos tickets refreshed after password reset.",
                "Clear cached credentials and re-authenticate.",
                "Check file share permissions for the user account.",
                "Ensure AD replication completed for password change.",
            ],
        ),
        tags=["unicode_escape", "encoding", "form_bug"],
        description="Backslash-u escape sequences from broken form submission.",
    )


def _dc092_ocr_scan() -> EvalCase:
    """OCR-scanned handwritten IT request with character confusion."""
    return EvalCase(
        ticket=EvalTicket(
            ticket_id="INC-DC-092",
            subject="[OCR SCAN] Handwritten IT Request — Floor 7",
            description=(
                "--- OCR Output (confidence: 62%) ---\n"
                "lT Request Fonn\nDate: Mar 1B, 2O26\nName: Jarne5 Wil5on\n"
                "Dept: C0mpliance\nFl00r: 7th\n\n"
                "l55ue: My lapt0p keybOard 1s not work1ng. The letters O and I "
                "typ3 numb3rs inst3ad. Started after l sp1lled c0ffee ye5terday. "
                "Leno\\v0 Th1nkPad T14s. A5set: LT-C0MP-0742.\n"
                "--- End OCR ---"
            ),
            reporter=Reporter(
                name="James Wilson",
                email="j.wilson@contoso.com",
                department="Compliance",
            ),
            created_at="2026-03-18T14:00:00Z",
            channel=Channel.EMAIL,
        ),
        gold=GoldAnswer(
            ticket_id="INC-DC-092",
            category=Category.HARDWARE,
            priority=Priority.P3,
            assigned_team=Team.ENDPOINT,
            needs_escalation=False,
            missing_information=[MissingInfoField.DEVICE_INFO],
            next_best_action=(
                "Replace or repair water-damaged keyboard on ThinkPad T14s. "
                "OCR character substitution errors (0/O, 1/l, 5/S) are scan artifacts."
            ),
            remediation_steps=[
                "Provide temporary external keyboard.",
                "Arrange laptop keyboard replacement via Lenovo warranty.",
                "Back up user data before repair.",
                "Inspect for further liquid damage.",
            ],
        ),
        tags=["ocr", "handwritten", "character_confusion"],
        description="Poorly OCR'd scan of handwritten IT form with character substitutions.",
    )


def _dc093_tracking_pixels_html() -> EvalCase:
    """Email with 1x1 tracking pixels and UTM-wrapped links."""
    return EvalCase(
        ticket=EvalTicket(
            ticket_id="INC-DC-093",
            subject="Bulk VPN access for Singapore office",
            description=(
                '<img src="https://track.contoso-email.com/open?id=abc123" '
                'width="1" height="1" style="display:none" />\n'
                "We have 15 new hires starting in Singapore on Monday. All need "
                "GlobalProtect VPN provisioned for the APAC-SG-CORP segment.\n"
                '<a href="https://click.contoso-email.com/track?url=https%3A%2F%2F'
                'sharepoint.contoso.com%2Fsites%2FHR%2FNewHires">Employee List</a>\n'
                '<img src="https://track.contoso-email.com/close?id=abc123" '
                'width="1" height="1" />\n'
                "Please provision in bulk — details in the linked spreadsheet."
            ),
            reporter=Reporter(
                name="Mei Ling Tan",
                email="m.tan@contoso.com",
                department="HR",
            ),
            created_at="2026-03-18T06:00:00Z",
            channel=Channel.EMAIL,
        ),
        gold=GoldAnswer(
            ticket_id="INC-DC-093",
            category=Category.ACCESS_AUTH,
            priority=Priority.P2,
            assigned_team=Team.IAM,
            needs_escalation=False,
            missing_information=[MissingInfoField.AFFECTED_USERS],
            next_best_action=(
                "Provision GlobalProtect VPN for 15 Singapore new hires. "
                "Tracking pixels and UTM links are email marketing noise."
            ),
            remediation_steps=[
                "Download employee list from SharePoint link.",
                "Bulk provision VPN accounts on APAC-SG-CORP segment.",
                "Send VPN setup instructions to new hires.",
                "Verify connectivity from Singapore office.",
            ],
        ),
        tags=["tracking_pixels", "utm_params", "html_noise"],
        description="Email with hidden tracking pixels and click-tracking UTM links.",
    )


def _dc094_chat_transcript_timestamps() -> EvalCase:
    """Teams chat export with per-line timestamps and UUIDs."""
    return EvalCase(
        ticket=EvalTicket(
            ticket_id="INC-DC-094",
            subject="Floor 12 color printer jammed — 47 jobs stuck",
            description=(
                "[2026-03-18T08:31:22Z] [uid:a1b2c3d4-e5f6-7890-abcd-ef1234567890] "
                "Sarah: Color printer on 12 jammed again\n"
                "[2026-03-18T08:31:45Z] [uid:e5f67890-a1b2-c3d4-e5f6-789012345678] "
                "Mike: The HP Color LaserJet on Floor 12? PRN-12F-001?\n"
                "[2026-03-18T08:32:01Z] [uid:a1b2c3d4-e5f6-7890-abcd-ef1234567890] "
                "Sarah: Yes. 47 jobs stuck in the queue now\n"
                "[2026-03-18T08:33:15Z] [uid:a1b2c3d4-e5f6-7890-abcd-ef1234567890] "
                "Sarah: Tried net stop spooler. Tray 2 shows empty but I refilled it. "
                "Display says: 'Load A4 in Tray 2'\n"
                "[2026-03-18T08:34:00Z] [uid:e5f67890-a1b2-c3d4-e5f6-789012345678] "
                "Mike: Probably a paper sensor issue. Submit a ticket."
            ),
            reporter=Reporter(
                name="Sarah Bennett",
                email="s.bennett@contoso.com",
                department="Operations",
            ),
            created_at="2026-03-18T08:35:00Z",
            channel=Channel.CHAT,
        ),
        gold=GoldAnswer(
            ticket_id="INC-DC-094",
            category=Category.HARDWARE,
            priority=Priority.P3,
            assigned_team=Team.ENDPOINT,
            needs_escalation=False,
            missing_information=[],
            next_best_action=(
                "Fix Floor 12 HP Color LaserJet paper sensor issue. Chat timestamps and UUIDs are export noise."
            ),
            remediation_steps=[
                "Inspect Tray 2 paper sensor on PRN-12F-001.",
                "Clear jammed print queue.",
                "Clean paper feed rollers.",
                "Test print from multiple trays.",
            ],
        ),
        tags=["chat_transcript", "timestamps", "uuid_noise"],
        description="Teams chat export with per-line ISO timestamps and UUID user IDs.",
    )


def _dc095_powerbi_dashboard_paste() -> EvalCase:
    """Copy-pasted PowerBI dashboard with box-drawing characters."""
    return EvalCase(
        ticket=EvalTicket(
            ticket_id="INC-DC-095",
            subject="Risk dashboard showing stale data since March 15",
            description=(
                "Portfolio Risk Dashboard (PowerBI):\n"
                "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                "VaR (95%) │ $4.2M │ ▲ 12.3% │ Limit: $5.0M\n"
                "CVaR      │ $6.1M │ ▲  8.7% │ Limit: $7.5M\n"
                "Last Refreshed: Mar 15 2026 ← STALE!\n"
                "⚠ DATA REFRESH FAILED — Pipeline timeout\n"
                "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                "Dashboard hasn't updated since March 15. Azure Data Factory pipeline "
                "'ppl-risk-daily-refresh' timing out at the Synapse query step."
            ),
            reporter=Reporter(
                name="Diana Osei",
                email="d.osei@contoso.com",
                department="Risk Management",
            ),
            created_at="2026-03-18T08:00:00Z",
            channel=Channel.PORTAL,
        ),
        gold=GoldAnswer(
            ticket_id="INC-DC-095",
            category=Category.DATA_STORAGE,
            priority=Priority.P2,
            assigned_team=Team.DATA_PLATFORM,
            needs_escalation=False,
            missing_information=[MissingInfoField.ERROR_MESSAGE],
            next_best_action=(
                "Fix ADF pipeline 'ppl-risk-daily-refresh' timeout. "
                "PowerBI dashboard paste is noise — data pipeline stalled since March 15."
            ),
            remediation_steps=[
                "Check ADF pipeline run history for error details.",
                "Investigate Synapse query performance.",
                "Increase pipeline timeout or optimize query.",
                "Trigger manual pipeline refresh once fixed.",
            ],
        ),
        tags=["powerbi", "dashboard", "box_drawing"],
        description="Copy-pasted PowerBI dashboard with box-drawing chars and stale data alert.",
    )


def _dc096_servicenow_wrapper() -> EvalCase:
    """ServiceNow auto-generated email wrapping a real request."""
    return EvalCase(
        ticket=EvalTicket(
            ticket_id="INC-DC-096",
            subject="[ServiceNow] INC0012345 - Bloomberg Terminal connection timeout",
            description=(
                "═══════════════════════════════\n"
                "ServiceNow Notification\n"
                "═══════════════════════════════\n"
                "Incident: INC0012345\nState: New\nAssignment Group: IT Support\n"
                "SLA: 4 hours (P2)\nCreated: 2026-03-18T08:30:00Z\n"
                "═══════════════════════════════\n\n"
                "Description: Bloomberg Terminal (v2024.3.18) on workstation "
                "WS-TRADE-0447 fails with 'BLP API connection timeout'. Single user "
                "on Equity Trading floor 24. Network fine for everything else.\n\n"
                "═══════════════════════════════\n"
                "Workflow: Created → Auto-categorized → SLA started"
            ),
            reporter=Reporter(
                name="Marcus Rivera",
                email="m.rivera@contoso.com",
                department="Equity Trading",
            ),
            created_at="2026-03-18T08:30:00Z",
            channel=Channel.EMAIL,
        ),
        gold=GoldAnswer(
            ticket_id="INC-DC-096",
            category=Category.SOFTWARE,
            priority=Priority.P2,
            assigned_team=Team.ENTERPRISE_APPS,
            needs_escalation=False,
            missing_information=[MissingInfoField.ERROR_MESSAGE, MissingInfoField.NETWORK_LOCATION],
            next_best_action=(
                "Troubleshoot Bloomberg Terminal API connection timeout on WS-TRADE-0447. "
                "ServiceNow envelope metadata is noise."
            ),
            remediation_steps=[
                "Check BLP API service connectivity from the workstation.",
                "Verify Bloomberg firewall rules for WS-TRADE-0447.",
                "Restart Bloomberg Terminal service.",
                "Contact Bloomberg support if issue persists.",
            ],
        ),
        tags=["servicenow", "auto_generated", "workflow_noise"],
        description="ServiceNow notification email wrapping a Bloomberg Terminal issue.",
    )


def _dc097_long_sharepoint_urls() -> EvalCase:
    """500+ character SharePoint URLs with query parameters."""
    return EvalCase(
        ticket=EvalTicket(
            ticket_id="INC-DC-097",
            subject="SharePoint error: 'Sorry, something went wrong'",
            description=(
                "Error when clicking this link:\nhttps://contoso.sharepoint.com/sites/"
                "InvestmentCommittee/Shared%20Documents/Forms/AllItems.aspx?id=%2Fsites"
                "%2FInvestmentCommittee%2FShared%20Documents%2FQ1%2D2026%2FPortfolio%20"
                "Reviews%2FNorth%20America%2FUS%20Equity%20Strategy%2FPerformance%20"
                "Attribution%2FMonthly%20Reports%2FMarch%202026%2FFinal%20Review%20Pack"
                "&viewid=a1b2c3d4-e5f6-7890-abcd-ef1234567890&sortField=Modified"
                "&isAscending=false&FilterField1=Author&FilterValue1=Sarah%20Mitchell\n\n"
                "Error page shows correlation ID: f47ac10b-58cc-4372-a567-0e02b2c3d4e5. "
                "Works fine if I navigate manually through the site."
            ),
            reporter=Reporter(
                name="Karen Wong",
                email="k.wong@contoso.com",
                department="Portfolio Management",
            ),
            created_at="2026-03-18T11:00:00Z",
            channel=Channel.CHAT,
        ),
        gold=GoldAnswer(
            ticket_id="INC-DC-097",
            category=Category.SOFTWARE,
            priority=Priority.P3,
            assigned_team=Team.ENTERPRISE_APPS,
            needs_escalation=False,
            missing_information=[],
            next_best_action=(
                "Investigate SharePoint error using correlation ID f47ac10b. "
                "The long URL with query params is context, not noise — check if "
                "URL length or special characters are causing the error."
            ),
            remediation_steps=[
                "Look up correlation ID in SharePoint admin logs.",
                "Test the URL with simplified query parameters.",
                "Check if the deeply nested folder path exceeds URL limits.",
                "Verify user permissions to the Investment Committee site.",
            ],
        ),
        tags=["long_url", "query_params", "sharepoint"],
        description="500+ character SharePoint URLs with complex query parameters.",
    )


def _dc098_base64_css_data_uri() -> EvalCase:
    """Base64-encoded CSS data URI in a styling bug report."""
    return EvalCase(
        ticket=EvalTicket(
            ticket_id="INC-DC-098",
            subject="Intranet portal dark mode broken after update",
            description=(
                "Since the portal update last night, dark mode is completely broken. "
                "All text displays as white on white. Here's the CSS being loaded:\n\n"
                "data:text/css;base64,LyogQ29udG9zbyBQb3J0YWwgVGhlbWUgdjMuMi4xICovCmJv"
                "ZHkgewogIGZvbnQtZmFtaWx5OiAnU2Vnb2UgVUknOwogIGJhY2tncm91bmQ6ICNmNWY1"
                "ZjU7Cn0KLm5hdiB7CiAgYmFja2dyb3VuZDogIzAwNzhkNDsKfQouZGFyay1tb2RlIGJv"
                "ZHkgewogIGJhY2tncm91bmQ6ICMxYTFhMWE7Cn0=\n\n"
                "About 200 people in the NY office use dark mode. Affects Chrome 122 "
                "and Edge 122."
            ),
            reporter=Reporter(
                name="Derek Chang",
                email="d.chang@contoso.com",
                department="Frontend Engineering",
            ),
            created_at="2026-03-18T08:15:00Z",
            channel=Channel.CHAT,
        ),
        gold=GoldAnswer(
            ticket_id="INC-DC-098",
            category=Category.SOFTWARE,
            priority=Priority.P3,
            assigned_team=Team.ENTERPRISE_APPS,
            needs_escalation=False,
            missing_information=[MissingInfoField.APPLICATION_VERSION],
            next_best_action=(
                "Fix intranet portal dark mode CSS after last night's update. "
                "Base64 data URI is diagnostic context, not actionable data."
            ),
            remediation_steps=[
                "Review last night's portal deployment changes.",
                "Check dark mode CSS overrides for color conflicts.",
                "Test rollback of portal update.",
                "Validate across Chrome and Edge.",
            ],
        ),
        tags=["base64", "css", "data_uri"],
        description="Base64-encoded CSS data URI pasted in a portal styling bug report.",
    )


def _dc099_outlook_html_table() -> EvalCase:
    """Outlook HTML table markup wrapping an access request."""
    return EvalCase(
        ticket=EvalTicket(
            ticket_id="INC-DC-099",
            subject="SharePoint access for Regulatory Affairs team",
            description=(
                '<table style="border-collapse:collapse;font-family:Segoe UI">'
                '<tr style="background:#0078d4;color:white">'
                "<th>Name</th><th>Role</th><th>Access Needed</th></tr>"
                "<tr><td>Sarah Kim</td><td>Lead Analyst</td><td>Full Control</td></tr>"
                "<tr><td>James Chen</td><td>Associate</td><td>Edit</td></tr>"
                "<tr><td>Priya Nair</td><td>Intern</td><td>Read</td></tr>"
                "</table>\n\n"
                "Above team members need access to the RegAffairs2026 SharePoint site "
                "immediately. All currently get 'Access Denied'. Filing deadline is March 25."
            ),
            reporter=Reporter(
                name="Sarah Kim",
                email="s.kim@contoso.com",
                department="Regulatory Affairs",
            ),
            created_at="2026-03-18T14:45:00Z",
            channel=Channel.EMAIL,
        ),
        gold=GoldAnswer(
            ticket_id="INC-DC-099",
            category=Category.ACCESS_AUTH,
            priority=Priority.P2,
            assigned_team=Team.IAM,
            needs_escalation=False,
            missing_information=[],
            next_best_action=(
                "Grant SharePoint access to RegAffairs2026 for three team members. "
                "HTML table markup is email formatting noise."
            ),
            remediation_steps=[
                "Grant Full Control to Sarah Kim on RegAffairs2026.",
                "Grant Edit access to James Chen.",
                "Grant Read access to Priya Nair.",
                "Confirm access and notify the team.",
            ],
        ),
        tags=["html", "outlook_table", "markup"],
        description="Outlook HTML table markup wrapping a SharePoint access request.",
    )


def _dc100_base64_woff_font() -> EvalCase:
    """Base64-encoded WOFF font data in a rendering bug report."""
    return EvalCase(
        ticket=EvalTicket(
            ticket_id="INC-DC-100",
            subject="Intranet fonts showing as squares on Floor 5",
            description=(
                "About 20 workstations on Floor 5 show square boxes instead of text "
                "on the intranet site. Chrome DevTools shows the font loading as:\n"
                "data:font/woff2;base64,d09GMgABAAAAAAScAA4AAAAACSAAAARLAAEAAAAAAx"
                "E/MYBlJ2B4AQ4KhliGSQsBNgIkA4R4EIAWLEQAHIgUGCygfIlkYbkoPBBg"
                "ABAEIAQA==\n\n"
                "Started after the Edge 122 push via SCCM on Thursday. Chrome was "
                "unaffected until today. 20 users impacted."
            ),
            reporter=Reporter(
                name="Priya Nair",
                email="p.nair@contoso.com",
                department="Operations",
            ),
            created_at="2026-03-18T05:30:00Z",
            channel=Channel.EMAIL,
        ),
        gold=GoldAnswer(
            ticket_id="INC-DC-100",
            category=Category.SOFTWARE,
            priority=Priority.P3,
            assigned_team=Team.ENDPOINT,
            needs_escalation=False,
            missing_information=[MissingInfoField.APPLICATION_VERSION],
            next_best_action=(
                "Fix font rendering on Floor 5 workstations after Edge 122 update. "
                "Base64 WOFF data is diagnostic noise."
            ),
            remediation_steps=[
                "Check if Edge 122 changed font rendering settings.",
                "Clear browser font cache on affected workstations.",
                "Verify intranet CSS font-face declarations.",
                "Test rollback of Edge update on one machine.",
            ],
        ),
        tags=["base64", "woff_font", "rendering"],
        description="Base64-encoded WOFF font data in a font rendering bug report.",
    )


def _dc101_pgp_signed_docking_station() -> EvalCase:
    """PGP/S-MIME signed email wrapping a docking station issue."""
    return EvalCase(
        ticket=EvalTicket(
            ticket_id="INC-DC-101",
            subject="Docking station not detecting external monitors",
            description=(
                "-----BEGIN PGP SIGNED MESSAGE-----\n"
                "Hash: SHA256\n\n"
                "Hi IT,\n\n"
                "My Lenovo ThinkPad USB-C dock (Gen 2) stopped "
                "detecting both external monitors after the BIOS "
                "update last Friday. Laptop screen works fine. "
                "Tried two different USB-C cables and another "
                "dock from a colleague — same result. Dock firmware "
                "is v1.4.23. Monitors are Dell U2722D, connected "
                "via DisplayPort.\n\n"
                "Please help,\nRajan Mehta\nTrading\n\n"
                "-----BEGIN PGP SIGNATURE-----\n"
                "iQIzBAEBCAAdFiEE7xGh3hH8z4MdF7c+s7u4fH8s\n"
                "K5UFAmR5F3wACgkQs7u4fH8sK5V1lg//bFiHt2VTb\n"
                "-----END PGP SIGNATURE-----"
            ),
            reporter=Reporter(
                name="Rajan Mehta",
                email="r.mehta@contoso.com",
                department="Trading",
            ),
            created_at="2026-04-07T09:00:00Z",
            channel=Channel.EMAIL,
        ),
        gold=GoldAnswer(
            ticket_id="INC-DC-101",
            category=Category.HARDWARE,
            priority=Priority.P3,
            assigned_team=Team.ENDPOINT,
            needs_escalation=False,
            missing_information=[MissingInfoField.DEVICE_INFO],
            next_best_action=(
                "Troubleshoot docking station display detection "
                "after BIOS update. PGP signature is email "
                "artefact noise."
            ),
            remediation_steps=[
                "Check BIOS release notes for display output changes.",
                "Roll back BIOS update on one machine to test.",
                "Update dock firmware to latest version.",
                "Test with a USB-C to DisplayPort direct cable.",
            ],
        ),
        tags=["data-cleanup", "pgp-signature", "docking-station"],
        description="PGP/S-MIME signed email wrapping a docking station issue.",
    )


def _dc102_long_cc_bcc_outlook_crash() -> EvalCase:
    """Long CC/BCC headers causing Outlook crash."""
    cc_list = "; ".join(f"user{i:03d}@contoso.com" for i in range(1, 81))
    return EvalCase(
        ticket=EvalTicket(
            ticket_id="INC-DC-102",
            subject="Outlook crashes when opening emails with large CC",
            description=(
                "Outlook 365 (v2402) crashes every time I open an "
                "email from the Regulatory team that has a huge CC "
                "list. The CC field contains:\n\n"
                f"CC: {cc_list}\n\n"
                "Crash happens within 2 seconds of opening. I can "
                "read the same email in OWA without issues. About "
                "5 people on my team are affected.\n\n"
                "Thanks,\nElena Vasquez\nCompliance"
            ),
            reporter=Reporter(
                name="Elena Vasquez",
                email="e.vasquez@contoso.com",
                department="Compliance",
            ),
            created_at="2026-04-07T10:15:00Z",
            channel=Channel.PORTAL,
        ),
        gold=GoldAnswer(
            ticket_id="INC-DC-102",
            category=Category.SOFTWARE,
            priority=Priority.P2,
            assigned_team=Team.ENDPOINT,
            needs_escalation=False,
            missing_information=[
                MissingInfoField.APPLICATION_VERSION,
            ],
            next_best_action=(
                "Investigate Outlook crash triggered by large "
                "CC/BCC header rendering. The CC list is context, "
                "not noise."
            ),
            remediation_steps=[
                "Reproduce crash with the same email in safe mode.",
                "Collect Outlook crash dump from Event Viewer.",
                "Check for known Office 365 bugs with large CC.",
                "Apply latest Outlook cumulative update.",
            ],
        ),
        tags=["data-cleanup", "cc-bcc-headers", "outlook-crash"],
        description="Long CC/BCC headers in an Outlook crash report.",
    )


def _dc103_xml_soap_fault_sap_sync() -> EvalCase:
    """XML SOAP Fault payload in an SAP sync failure ticket."""
    return EvalCase(
        ticket=EvalTicket(
            ticket_id="INC-DC-103",
            subject="SAP PI sync failing with SOAP fault since 6 AM",
            description=(
                "The SAP PI to Salesforce integration started "
                "returning SOAP faults at 06:00 UTC today. All "
                "outbound IDocs are stuck in status 03.\n\n"
                "Error payload from SAP PI monitoring:\n"
                '<?xml version="1.0" encoding="UTF-8"?>\n'
                "<SOAP-ENV:Envelope "
                'xmlns:SOAP-ENV="http://schemas.xmlsoap.org/'
                'soap/envelope/">\n'
                "  <SOAP-ENV:Body>\n"
                "    <SOAP-ENV:Fault>\n"
                "      <faultcode>"
                "SOAP-ENV:Server</faultcode>\n"
                "      <faultstring>"
                "Authentication token expired"
                "</faultstring>\n"
                "      <detail>\n"
                "        <errorCode>AUTH-4012</errorCode>\n"
                "        <message>OAuth2 refresh token invalid"
                "</message>\n"
                "      </detail>\n"
                "    </SOAP-ENV:Fault>\n"
                "  </SOAP-ENV:Body>\n"
                "</SOAP-ENV:Envelope>\n\n"
                "~300 IDocs queued. Finance month-end close is "
                "tomorrow.\n\nRegards,\nHiroshi Tanaka\nFinance"
            ),
            reporter=Reporter(
                name="Hiroshi Tanaka",
                email="h.tanaka@contoso.com",
                department="Finance",
            ),
            created_at="2026-04-07T06:30:00Z",
            channel=Channel.EMAIL,
        ),
        gold=GoldAnswer(
            ticket_id="INC-DC-103",
            category=Category.SOFTWARE,
            priority=Priority.P1,
            assigned_team=Team.ENTERPRISE_APPS,
            needs_escalation=True,
            missing_information=[],
            next_best_action=(
                "Restore SAP PI to Salesforce integration by "
                "renewing the expired OAuth2 refresh token. "
                "SOAP XML is diagnostic evidence."
            ),
            remediation_steps=[
                "Regenerate the OAuth2 refresh token in Salesforce.",
                "Update SAP PI communication channel credentials.",
                "Reprocess stuck IDocs in status 03.",
                "Verify end-to-end sync with a test IDoc.",
            ],
        ),
        tags=["data-cleanup", "xml-soap", "sap-sync"],
        description="XML SOAP Fault payload in an SAP sync failure ticket.",
    )


def _dc104_k8s_pod_describe_crashloop() -> EvalCase:
    """Kubernetes pod describe output in a CrashLoopBackOff ticket."""
    return EvalCase(
        ticket=EvalTicket(
            ticket_id="INC-DC-104",
            subject="Payment service pods in CrashLoopBackOff",
            description=(
                "payment-svc pods are crash-looping in the "
                "prod-east cluster since the 02:00 deploy.\n\n"
                "$ kubectl describe pod payment-svc-7b9f5-xk2lm "
                "-n payments\n"
                "Name:         payment-svc-7b9f5-xk2lm\n"
                "Namespace:    payments\n"
                "Status:       Running\n"
                "Containers:\n"
                "  payment-api:\n"
                "    Image:   registry.contoso.com/payment:3.12\n"
                "    State:   Waiting\n"
                "      Reason: CrashLoopBackOff\n"
                "    Last State: Terminated\n"
                "      Reason: OOMKilled\n"
                "      Exit Code: 137\n"
                "    Limits:\n"
                "      memory: 512Mi\n"
                "    Requests:\n"
                "      memory: 256Mi\n"
                "Events:\n"
                "  Warning  BackOff  pod/payment-svc-7b9f5-xk2lm "
                " Back-off restarting failed container\n\n"
                "3 of 5 replicas are affected. Customer payments "
                "are failing.\n\n"
                "— Amir Hossein, Cloud Infrastructure"
            ),
            reporter=Reporter(
                name="Amir Hossein",
                email="a.hossein@contoso.com",
                department="Cloud Infrastructure",
            ),
            created_at="2026-04-07T02:45:00Z",
            channel=Channel.CHAT,
        ),
        gold=GoldAnswer(
            ticket_id="INC-DC-104",
            category=Category.SOFTWARE,
            priority=Priority.P1,
            assigned_team=Team.ENTERPRISE_APPS,
            needs_escalation=True,
            missing_information=[],
            next_best_action=(
                "Fix OOMKilled crash loop in payment service pods. "
                "The kubectl output is diagnostic evidence, "
                "not noise."
            ),
            remediation_steps=[
                "Increase memory limits for payment-api container.",
                "Check v3.12 release for memory regression.",
                "Roll back to previous image tag if needed.",
                "Monitor pod restarts after fix.",
            ],
        ),
        tags=["data-cleanup", "kubernetes", "crashloopbackoff"],
        description="Kubernetes pod describe output in a CrashLoopBackOff ticket.",
    )


def _dc105_hex_dump_tls_handshake() -> EvalCase:
    """Raw hex dump from a TLS handshake failure investigation."""
    return EvalCase(
        ticket=EvalTicket(
            ticket_id="INC-DC-105",
            subject="TLS handshake failures to api.payments.contoso.com",
            description=(
                "Intermittent TLS handshake failures started this "
                "morning when connecting to "
                "api.payments.contoso.com:443 from the DMZ load "
                "balancer. About 15 pct of requests fail.\n\n"
                "Hex dump from tcpdump (first ClientHello):\n"
                "0000  16 03 01 00 f1 01 00 00 ed 03 03 66 1a 2b 3c\n"
                "0010  4d 5e 6f 70 81 92 a3 b4 c5 d6 e7 f8 09 1a 2b\n"
                "0020  3c 4d 5e 6f 70 81 92 a3 b4 c5 d6 00 00 1c 13\n"
                "0030  02 13 03 13 01 c0 2c c0 2b c0 30 c0 2f 00 9e\n"
                "0040  00 9f cc a9 cc a8 c0 14 c0 0a 00 ff 01 00 00\n\n"
                "ServerHello response is a fatal alert (0x28 = "
                "handshake_failure).\n\n"
                "Tomas Novak\nNetwork Ops"
            ),
            reporter=Reporter(
                name="Tomas Novak",
                email="t.novak@contoso.com",
                department="Cloud Infrastructure",
            ),
            created_at="2026-04-07T08:10:00Z",
            channel=Channel.EMAIL,
        ),
        gold=GoldAnswer(
            ticket_id="INC-DC-105",
            category=Category.NETWORK,
            priority=Priority.P2,
            assigned_team=Team.NETWORK_OPS,
            needs_escalation=False,
            missing_information=[
                MissingInfoField.ENVIRONMENT_DETAILS,
            ],
            next_best_action=(
                "Diagnose TLS handshake failures between DMZ LB and payments API. Hex dump is diagnostic evidence."
            ),
            remediation_steps=[
                "Compare cipher suites offered by client and server.",
                "Check server certificate validity and chain.",
                "Verify no recent TLS policy change on the LB.",
                "Test with openssl s_client to isolate the cause.",
            ],
        ),
        tags=["data-cleanup", "hex-dump", "tls-handshake"],
        description="Raw hex dump from a TLS handshake failure investigation.",
    )


def _dc106_mixed_encoding_wifi_drops() -> EvalCase:
    """Mixed encoding characters in a WiFi drop report."""
    return EvalCase(
        ticket=EvalTicket(
            ticket_id="INC-DC-106",
            subject="WiFi keeps dropping \u2014 Floor 3 \u00e8 un disastro",
            description=(
                "Wi-Fi drops every 10\u201315 minutes on Floor 3. "
                "The SSID is \u201cContoso-Corp\u201d but sometimes shows as "
                "Contoso\u00c3\u00a2\u00e2\u201a\u00ac\u00e2\u20ac\u0153Corp or "
                "Contoso\xc2\xadCorp in the "
                "connection log.\n\n"
                "Af\xc3\xa9cter\xc3\xa9d users: \u00e8\u00e9\u00ea\u00eb about "
                "30 people on the east wing. The issue started "
                "after the Aruba AP firmware push (v8.10.0.7). "
                "Signal strength is fine (\u221272 dBm average).\n\n"
                "R\u00e9mi Dub\u00e9\nFacilities"
            ),
            reporter=Reporter(
                name="R\u00e9mi Dub\u00e9",
                email="r.dube@contoso.com",
                department="Facilities",
            ),
            created_at="2026-04-07T11:20:00Z",
            channel=Channel.PORTAL,
        ),
        gold=GoldAnswer(
            ticket_id="INC-DC-106",
            category=Category.NETWORK,
            priority=Priority.P2,
            assigned_team=Team.NETWORK_OPS,
            needs_escalation=False,
            missing_information=[
                MissingInfoField.NETWORK_LOCATION,
            ],
            next_best_action=(
                "Investigate WiFi drops on Floor 3 after Aruba AP firmware update. Mojibake is encoding noise."
            ),
            remediation_steps=[
                "Review Aruba AP firmware v8.10.0.7 release notes.",
                "Check AP logs for disassociation events on Floor 3.",
                "Roll back AP firmware on one unit to test.",
                "Verify SSID broadcast encoding settings.",
            ],
        ),
        tags=["data-cleanup", "mixed-encoding", "wifi-drops"],
        description="Mixed encoding characters in a WiFi drop report.",
    )


def _dc107_sql_results_data_corruption() -> EvalCase:
    """SQL query results pasted into a data corruption ticket."""
    return EvalCase(
        ticket=EvalTicket(
            ticket_id="INC-DC-107",
            subject="Client portfolio data corruption in PMS database",
            description=(
                "We found corrupted records in the portfolio "
                "management system. Query output below:\n\n"
                "SELECT client_id, portfolio_value, last_updated\n"
                "FROM pms.client_portfolios\n"
                "WHERE last_updated > '2026-04-01';\n\n"
                "client_id | portfolio_value | last_updated\n"
                "----------|-----------------|-------------------\n"
                "C-10421   | -99999999.99    | 2026-04-03 00:00\n"
                "C-10422   | NULL            | 2026-04-03 00:00\n"
                "C-10423   | 0.00            | 1970-01-01 00:00\n"
                "C-10424   | 8.472E+18       | 2026-04-03 00:00\n"
                "C-10425   | -99999999.99    | 2026-04-03 00:00\n\n"
                "5 out of ~1200 records affected. Looks like the "
                "nightly ETL on April 3 went wrong.\n\n"
                "Wei Chen, Data Engineering"
            ),
            reporter=Reporter(
                name="Wei Chen",
                email="w.chen@contoso.com",
                department="Data Engineering",
            ),
            created_at="2026-04-07T07:00:00Z",
            channel=Channel.EMAIL,
        ),
        gold=GoldAnswer(
            ticket_id="INC-DC-107",
            category=Category.DATA_STORAGE,
            priority=Priority.P2,
            assigned_team=Team.DATA_PLATFORM,
            needs_escalation=True,
            missing_information=[
                MissingInfoField.ERROR_MESSAGE,
            ],
            next_best_action=(
                "Investigate and repair corrupted portfolio records "
                "from the April 3 ETL run. SQL output is "
                "diagnostic evidence."
            ),
            remediation_steps=[
                "Identify the root cause in the nightly ETL job.",
                "Restore affected records from the last good backup.",
                "Add data validation checks to the ETL pipeline.",
                "Verify all 1200 records after restoration.",
            ],
        ),
        tags=["data-cleanup", "sql-results", "data-corruption"],
        description="SQL query results pasted into a data corruption ticket.",
    )


def _dc108_multilingual_disclaimer_password() -> EvalCase:
    """Multilingual legal disclaimer wrapping a password reset request."""
    return EvalCase(
        ticket=EvalTicket(
            ticket_id="INC-DC-108",
            subject="Cannot reset password \u2014 locked out",
            description=(
                "Hi, I have been locked out of my account "
                "(jgarcia@contoso.com) after too many failed MFA "
                "attempts. I need an urgent password reset and MFA "
                "re-enrollment. I am presenting to the board in "
                "90 minutes.\n\n"
                "CONFIDENTIALITY NOTICE: This e-mail message, "
                "including any attachments, is for the sole use "
                "of the intended recipient(s).\n"
                "AVIS DE CONFIDENTIALIT\u00c9 : Ce message "
                "\u00e9lectronique, y compris les pi\u00e8ces "
                "jointes, est destin\u00e9 exclusivement.\n"
                "VERTRAULICHKEITSHINWEIS: Diese E-Mail-Nachricht "
                "einschlie\u00dflich aller Anh\u00e4nge ist "
                "ausschlie\u00dflich f\u00fcr den Gebrauch.\n"
                "AVISO DE CONFIDENCIALIDAD: Este mensaje de "
                "correo electr\u00f3nico, incluyendo los archivos "
                "adjuntos.\n"
                "\u6a5f\u5bc6\u4fdd\u6301\u306e\u304a\u77e5\u3089"
                "\u305b: \u3053\u306e\u96fb\u5b50\u30e1\u30fc\u30eb"
                "\u306f\u3001\u6dfb\u4ed8\u30d5\u30a1\u30a4\u30eb"
                "\u3092\u542b\u3081\u3001\u610f\u56f3\u3055\u308c"
                "\u305f\u53d7\u4fe1\u8005\u306e\u307f\u3002\n\n"
                "Javier Garcia\nExecutive Operations"
            ),
            reporter=Reporter(
                name="Javier Garcia",
                email="j.garcia@contoso.com",
                department="Executive Operations",
            ),
            created_at="2026-04-07T08:30:00Z",
            channel=Channel.EMAIL,
        ),
        gold=GoldAnswer(
            ticket_id="INC-DC-108",
            category=Category.ACCESS_AUTH,
            priority=Priority.P1,
            assigned_team=Team.IAM,
            needs_escalation=False,
            missing_information=[
                MissingInfoField.AUTHENTICATION_METHOD,
            ],
            next_best_action=(
                "Reset password and re-enroll MFA for locked-out "
                "executive before board presentation. Multilingual "
                "disclaimers are email noise."
            ),
            remediation_steps=[
                "Verify user identity via out-of-band channel.",
                "Reset password in Azure AD.",
                "Clear MFA registration and re-enroll.",
                "Confirm account access is restored.",
            ],
        ),
        tags=[
            "data-cleanup",
            "multilingual-disclaimer",
            "password-reset",
        ],
        description=("Multilingual legal disclaimer wrapping a password reset request."),
    )


def _dc109_near_empty_monitor_issue() -> EvalCase:
    """Near-empty ticket about a monitor issue."""
    return EvalCase(
        ticket=EvalTicket(
            ticket_id="INC-DC-109",
            subject="monitor",
            description="not working",
            reporter=Reporter(
                name="Pat Lee",
                email="p.lee@contoso.com",
                department="Marketing",
            ),
            created_at="2026-04-07T13:00:00Z",
            channel=Channel.CHAT,
        ),
        gold=GoldAnswer(
            ticket_id="INC-DC-109",
            category=Category.HARDWARE,
            priority=Priority.P4,
            assigned_team=Team.ENDPOINT,
            needs_escalation=False,
            missing_information=[
                MissingInfoField.DEVICE_INFO,
                MissingInfoField.ERROR_MESSAGE,
                MissingInfoField.STEPS_TO_REPRODUCE,
            ],
            next_best_action=(
                "Gather details from the reporter about which monitor, what is not working, and any error indicators."
            ),
            remediation_steps=[
                "Contact reporter for monitor make and model.",
                "Ask whether the issue is no display or flicker.",
                "Determine if the monitor is internal or external.",
                "Schedule on-site diagnosis once details received.",
            ],
        ),
        tags=["data-cleanup", "near-empty", "monitor"],
        description="Near-empty ticket with almost no context about a monitor issue.",
    )


def _dc110_vuln_scanner_tls_cert_expiry() -> EvalCase:
    """Vulnerability scanner dump in a TLS certificate expiry ticket."""
    return EvalCase(
        ticket=EvalTicket(
            ticket_id="INC-DC-110",
            subject="Nessus scan flagged expiring TLS certs",
            description=(
                "The weekly Nessus vulnerability scan flagged "
                "several hosts with expiring TLS certificates. "
                "Scan output excerpt:\n\n"
                "Plugin ID: 15901\n"
                "Severity: Medium\n"
                "Host: intranet.contoso.com (10.0.12.50)\n"
                "Port: 443/tcp\n"
                "Synopsis: SSL certificate expires within 14 days\n"
                "Output:\n"
                "  Subject: CN=intranet.contoso.com\n"
                "  Issuer: CN=Contoso Internal CA\n"
                "  Not After: Apr 21 23:59:59 2026 GMT\n\n"
                "Plugin ID: 15901\n"
                "Host: api-gw.contoso.com (10.0.12.55)\n"
                "Port: 8443/tcp\n"
                "Output:\n"
                "  Subject: CN=api-gw.contoso.com\n"
                "  Issuer: CN=Contoso Internal CA\n"
                "  Not After: Apr 19 23:59:59 2026 GMT\n\n"
                "Plugin ID: 42873\n"
                "Host: 10.0.12.50\n"
                "Synopsis: SSL medium strength cipher suites\n"
                "Output: TLS_RSA_WITH_AES_128_CBC_SHA\n\n"
                "Two certs expire within 14 days. Please renew.\n"
                "\nSarah Kim\nIT Security"
            ),
            reporter=Reporter(
                name="Sarah Kim",
                email="s.kim@contoso.com",
                department="IT Security",
            ),
            created_at="2026-04-07T14:00:00Z",
            channel=Channel.EMAIL,
        ),
        gold=GoldAnswer(
            ticket_id="INC-DC-110",
            category=Category.SECURITY,
            priority=Priority.P2,
            assigned_team=Team.SECURITY_OPS,
            needs_escalation=False,
            missing_information=[],
            next_best_action=(
                "Renew expiring TLS certificates on intranet and "
                "api-gw hosts before April 19. Scanner output is "
                "diagnostic evidence."
            ),
            remediation_steps=[
                "Generate CSRs for intranet.contoso.com and api-gw.",
                "Submit CSRs to Contoso Internal CA for renewal.",
                "Install renewed certificates on both hosts.",
                "Re-run Nessus scan to confirm remediation.",
            ],
        ),
        tags=[
            "data-cleanup",
            "vulnerability-scanner",
            "tls-cert-expiry",
        ],
        description=("Vulnerability scanner dump in a TLS certificate expiry ticket."),
    )


def _dc111_base64_pdf_inline() -> EvalCase:
    """Base64-encoded PDF pasted inline with a real printer issue."""
    b64_block = "JVBERi0xLjQKMSAwIG9iago8PCAvVHlwZSAvQ2F0YWxvZyAvUGFnZXMgMiAwIFIgPj4KZW5k" * 40
    description = (
        "Hi support,\n\n"
        "I tried to print a document but the printer just shows 'PCL XL error' and "
        "spits out blank pages. Here is the PDF I was trying to print (base64):\n\n"
        f"{b64_block}\n\n"
        "The printer is an HP LaserJet 4250 on the 3rd floor near room 312. It has "
        "been doing this since Monday morning. Other people on the floor are affected "
        "too. We tried restarting the printer twice but the error keeps coming back.\n\n"
        "Thanks,\nMaria Santos\nAccounting"
    )
    return EvalCase(
        ticket=EvalTicket(
            ticket_id="INC-DC-111",
            subject="Printer showing PCL XL error - PDF attached inline",
            description=description,
            reporter=Reporter(
                name="Maria Santos",
                email="m.santos@contoso.com",
                department="Accounting",
            ),
            created_at="2026-03-18T09:00:00Z",
            channel=Channel.EMAIL,
            attachments=[],
        ),
        gold=GoldAnswer(
            ticket_id="INC-DC-111",
            category=Category.HARDWARE,
            priority=Priority.P3,
            assigned_team=Team.ENDPOINT,
            needs_escalation=False,
            missing_information=[],
            next_best_action=(
                "Investigate the PCL XL error on the HP LaserJet 4250 near room 312. "
                "The inline base64 PDF is noise and should be ignored."
            ),
            remediation_steps=[
                "Check the HP LaserJet 4250 PCL XL error log on the printer display.",
                "Update or reinstall the PCL6 printer driver on affected workstations.",
                "Clear the print queue and perform a cold restart of the printer.",
                "Test printing a simple document to confirm resolution.",
            ],
        ),
        tags=["data-cleanup", "base64-pdf", "printer"],
        description="Base64-encoded PDF pasted inline obscuring a real printer issue.",
    )


def _dc112_extremely_long_email() -> EvalCase:
    """Extremely long verbose email with a VPN issue buried inside."""
    padding = (
        "I want to start by saying that I have been a loyal employee at Contoso for "
        "over fifteen years and I have always taken great pride in my work. Back in "
        "2011 when I first joined the company, we used to have a completely different "
        "IT setup and things were so much simpler. I remember when we had just a single "
        "server room and everyone used desktop computers. Those were the good old days. "
        "Anyway, I digress. Let me tell you about my morning routine because it is "
        "relevant to understanding the problem I am about to describe. Every day I wake "
        "up at 6:30 AM and I make myself a cup of coffee — usually a dark roast from "
        "the local roaster on 5th Avenue. Then I sit down at my home office desk which "
        "is an IKEA BEKANT standing desk, in case that matters. I open my laptop, which "
        "is a Dell Latitude 5520 running Windows 11 Pro build 22631. I then try to "
        "connect to the corporate VPN. Now, here is where the trouble begins, but first "
        "let me explain my entire home network setup in excruciating detail. "
    )
    repeated_padding = padding * 8
    description = (
        f"{repeated_padding}\n\n"
        "OK so the actual problem: when I connect to GlobalProtect VPN, it authenticates "
        "successfully but then drops the connection after exactly 47 seconds every single "
        "time. The error in the GP client log says 'ESP tunnel teardown - keep-alive timeout'. "
        "This started happening after the firewall maintenance window last Friday night. "
        "Other people on my team (Finance - AP group) are having the same issue.\n\n"
        "Thanks,\nRobert Chen\nFinance"
    )
    return EvalCase(
        ticket=EvalTicket(
            ticket_id="INC-DC-112",
            subject="VPN keeps disconnecting - URGENT please help",
            description=description,
            reporter=Reporter(
                name="Robert Chen",
                email="r.chen@contoso.com",
                department="Finance",
            ),
            created_at="2026-03-18T09:15:00Z",
            channel=Channel.EMAIL,
            attachments=[],
        ),
        gold=GoldAnswer(
            ticket_id="INC-DC-112",
            category=Category.NETWORK,
            priority=Priority.P2,
            assigned_team=Team.NETWORK_OPS,
            needs_escalation=False,
            missing_information=[],
            next_best_action=(
                "Investigate the GlobalProtect VPN ESP tunnel keep-alive timeout "
                "that started after last Friday's firewall maintenance window."
            ),
            remediation_steps=[
                "Review firewall change records from the Friday maintenance window.",
                "Check GlobalProtect gateway ESP keep-alive and timeout settings.",
                "Compare current firewall rules with pre-maintenance configuration.",
                "Restore ESP tunnel parameters if misconfigured during maintenance.",
                "Test VPN connectivity with affected Finance AP group users.",
            ],
        ),
        tags=["data-cleanup", "extremely-long-email", "vpn"],
        description="Extremely verbose 10K+ char email with a VPN issue buried in padding.",
    )


def _dc113_multiple_base64_images_flood() -> EvalCase:
    """Three inline base64 images obscuring a monitor flickering issue."""
    fake_img = "data:image/png;base64," + "iVBORw0KGgoAAAANSUhEUgAAAAUA" * 60
    description = (
        "My monitor keeps flickering every few seconds. Here are screenshots:\n\n"
        f"Screenshot 1 (normal state):\n{fake_img}\n\n"
        f"Screenshot 2 (during flicker):\n{fake_img}\n\n"
        f"Screenshot 3 (after flicker):\n{fake_img}\n\n"
        "The monitor is a Dell U2722D connected via DisplayPort to my docking station "
        "(Dell WD19S). The flickering happens about every 10-15 seconds and has been "
        "going on for three days. I tried a different DisplayPort cable but the issue "
        "persists. My colleague in the next cubicle does not have this problem.\n\n"
        "— Priya Sharma, Engineering"
    )
    return EvalCase(
        ticket=EvalTicket(
            ticket_id="INC-DC-113",
            subject="Monitor flickering - screenshots attached inline",
            description=description,
            reporter=Reporter(
                name="Priya Sharma",
                email="p.sharma@contoso.com",
                department="Engineering",
            ),
            created_at="2026-03-18T09:30:00Z",
            channel=Channel.EMAIL,
            attachments=[],
        ),
        gold=GoldAnswer(
            ticket_id="INC-DC-113",
            category=Category.HARDWARE,
            priority=Priority.P3,
            assigned_team=Team.ENDPOINT,
            needs_escalation=False,
            missing_information=[],
            next_best_action=(
                "Diagnose the Dell U2722D monitor flickering via DisplayPort on the "
                "WD19S docking station. Inline base64 images are noise."
            ),
            remediation_steps=[
                "Test the monitor with a direct HDMI or USB-C connection bypassing the dock.",
                "Update the Dell WD19S docking station firmware.",
                "Check DisplayPort cable and try a certified DP 1.4 cable.",
                "If flickering persists, swap the monitor with a known-good unit.",
            ],
        ),
        tags=["data-cleanup", "base64-image-flood", "monitor-flicker"],
        description="Three inline base64 images flooding the ticket with a monitor flickering issue.",
    )


def _dc114_severe_mojibake() -> EvalCase:
    """Severe mojibake corruption hiding a software installation failure."""
    description = (
        "Subject: Software installation failure\n\n"
        "I tried to install the new version of our CRM application "
        "(Dynamics 365 v9.2.24013.109) but it failed with an error. "
        "Here is the error message from the installer log:\n\n"
        'ERROR: Ã¢â‚¬Å"Unable to initialize componentÃ¢â‚¬Â\n'
        'Module: Ã¢â‚¬Å"Microsoft.Dynamics.CRM.CoreÃ¢â‚¬Â\n'
        "Details: LÃ¢â‚¬â„¢initialisation du composant a Ã©chouÃ©. "
        "Le fichier de configuration nÃ¢â‚¬â„¢est pas valide. "
        "VÃ©rifiez que le chemin dÃ¢â‚¬â„¢accÃ¨s est correct.\n"
        "Error Code: 0x80073712 Ã¢â‚¬â€œ Component store corruption\n"
        "ÃƒÂ©chec de lÃ¢â‚¬â„¢installation Ã  lÃ¢â‚¬â„¢Ã©tape 3 de 7\n"
        "Timestamp: 2026-03-17T16:42:11Ã¢â‚¬â€œ05:00\n\n"
        "I have tried running sfc /scannow but it also shows corrupted files. "
        "This is blocking our quarterly update rollout for the sales team.\n\n"
        "Thanks,\nDavid Okafor\nSales Operations"
    )
    return EvalCase(
        ticket=EvalTicket(
            ticket_id="INC-DC-114",
            subject="CRM install fails Ã¢â‚¬â€œ error 0x80073712",
            description=description,
            reporter=Reporter(
                name="David Okafor",
                email="d.okafor@contoso.com",
                department="Sales Operations",
            ),
            created_at="2026-03-18T10:00:00Z",
            channel=Channel.PORTAL,
            attachments=[],
        ),
        gold=GoldAnswer(
            ticket_id="INC-DC-114",
            category=Category.SOFTWARE,
            priority=Priority.P2,
            assigned_team=Team.ENTERPRISE_APPS,
            needs_escalation=False,
            missing_information=[MissingInfoField.DEVICE_INFO],
            next_best_action=(
                "Resolve the Dynamics 365 installation failure caused by component "
                "store corruption (0x80073712). Mojibake in the log is an encoding artifact."
            ),
            remediation_steps=[
                "Run DISM /Online /Cleanup-Image /RestoreHealth to repair the component store.",
                "Re-run sfc /scannow after DISM repair completes.",
                "Retry the Dynamics 365 v9.2 installer.",
                "If installation still fails, collect CBS logs and escalate to Microsoft support.",
            ],
        ),
        tags=["data-cleanup", "severe-mojibake", "software-install"],
        description="Severe mojibake encoding corruption in a CRM installation failure ticket.",
    )


def _dc115_deep_email_quoting() -> EvalCase:
    """Password reset issue buried under 10+ levels of email quoting."""
    quoting_layers = ""
    for i in range(12, 0, -1):
        prefix = ">" * i + " "
        quoting_layers += (
            f"{prefix}On 2026-03-{5 + i}T{8 + i}:00:00Z, Person{i}@contoso.com wrote:\n"
            f"{prefix}Thanks for the update. Let me loop in someone else.\n"
            f"{prefix}\n"
        )
    description = (
        "FW: FW: FW: RE: RE: RE: FW: RE: RE: RE: FW: RE: Password Reset Request\n\n"
        f"{quoting_layers}\n"
        "ORIGINAL REQUEST:\n"
        "Hi IT Support,\n\n"
        "I have been locked out of my Active Directory account (username: jthompson) "
        "after too many failed login attempts. I need a password reset urgently because "
        "I have a client presentation at 2 PM today and all my files are on SharePoint. "
        "I am in the Chicago office, 14th floor. My manager is Lisa Park.\n\n"
        "Thanks,\nJennifer Thompson\nClient Services"
    )
    return EvalCase(
        ticket=EvalTicket(
            ticket_id="INC-DC-115",
            subject="FW: FW: FW: RE: RE: RE: FW: RE: RE: RE: FW: RE: Password Reset Request",
            description=description,
            reporter=Reporter(
                name="Jennifer Thompson",
                email="j.thompson@contoso.com",
                department="Client Services",
            ),
            created_at="2026-03-18T10:15:00Z",
            channel=Channel.EMAIL,
            attachments=[],
        ),
        gold=GoldAnswer(
            ticket_id="INC-DC-115",
            category=Category.ACCESS_AUTH,
            priority=Priority.P2,
            assigned_team=Team.IAM,
            needs_escalation=False,
            missing_information=[],
            next_best_action=(
                "Reset the Active Directory password for jthompson and unlock the account. "
                "The deep quoting chain is forwarding noise."
            ),
            remediation_steps=[
                "Unlock the AD account for jthompson.",
                "Reset the password and send temporary credentials securely.",
                "Verify the user can access SharePoint and their files.",
                "Remind the user about the self-service password reset portal.",
            ],
        ),
        tags=["data-cleanup", "deep-quoting", "password-reset"],
        description="Password reset request buried under 12 levels of email quoting and forwarding.",
    )


def _dc116_giant_signature_block() -> EvalCase:
    """Bluetooth headset issue followed by a giant corporate signature block."""
    ascii_logo = (
        "  ██████╗ ██████╗ ███╗   ██╗████████╗ ██████╗ ███████╗ ██████╗ \n"
        " ██╔════╝██╔═══██╗████╗  ██║╚══██╔══╝██╔═══██╗██╔════╝██╔═══██╗\n"
        " ██║     ██║   ██║██╔██╗ ██║   ██║   ██║   ██║███████╗██║   ██║\n"
        " ██║     ██║   ██║██║╚██╗██║   ██║   ██║   ██║╚════██║██║   ██║\n"
        " ╚██████╗╚██████╔╝██║ ╚████║   ██║   ╚██████╔╝███████║╚██████╔╝\n"
        "  ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝   ╚═╝    ╚═════╝ ╚══════╝ ╚═════╝ \n"
    )
    signature = (
        "\n--\n"
        f"{ascii_logo}\n"
        "Marcus Williams | Senior Vice President of Strategic Initiatives\n"
        "Contoso Corporation | Global Headquarters\n"
        "1234 Innovation Drive, Suite 5600 | Redmond, WA 98052\n"
        "Office: +1 (425) 555-0198 | Mobile: +1 (425) 555-0199\n"
        "Fax: +1 (425) 555-0200 | Internal Ext: 55198\n"
        "Email: m.williams@contoso.com\n"
        "LinkedIn: linkedin.com/in/marcuswilliams-contoso\n"
        "Twitter: @MWilliamsContoso\n"
        "Web: https://www.contoso.com/leadership/marcus-williams\n\n"
        "CONFIDENTIALITY NOTICE: This email and any attachments are for the exclusive "
        "and confidential use of the intended recipient. If you are not the intended "
        "recipient, please do not read, distribute, or take action based on this message. "
        "If you have received this in error, please notify the sender immediately by return "
        "email and delete this message from your system. Contoso Corporation accepts no "
        "liability for any damage caused by any virus transmitted by this email. The views "
        "expressed in this communication do not necessarily reflect the official policy or "
        "position of Contoso Corporation or any of its subsidiaries, affiliates, or partners. "
        "For more information about our privacy practices, visit https://www.contoso.com/privacy\n\n"
        "🌿 Please consider the environment before printing this email.\n"
        "🏆 Contoso: Named #1 Best Place to Work 2025 by Fortune Magazine\n"
        "📊 Q4 2025 Earnings: Revenue up 23% YoY — see investor.contoso.com\n"
    )
    description = (
        "My Jabra Evolve2 85 Bluetooth headset pairs with my laptop but the audio "
        "keeps cutting out during Teams calls. The headset firmware is up to date "
        "(v2.6.0). It works fine with my phone so I think it's a laptop issue.\n"
        f"{signature}"
    )
    return EvalCase(
        ticket=EvalTicket(
            ticket_id="INC-DC-116",
            subject="Bluetooth headset audio cutting out on Teams calls",
            description=description,
            reporter=Reporter(
                name="Marcus Williams",
                email="m.williams@contoso.com",
                department="Strategic Initiatives",
            ),
            created_at="2026-03-18T10:30:00Z",
            channel=Channel.EMAIL,
            attachments=[],
        ),
        gold=GoldAnswer(
            ticket_id="INC-DC-116",
            category=Category.HARDWARE,
            priority=Priority.P3,
            assigned_team=Team.ENDPOINT,
            needs_escalation=False,
            missing_information=[MissingInfoField.DEVICE_INFO],
            next_best_action=(
                "Troubleshoot the Jabra Evolve2 85 Bluetooth audio dropout on Teams. "
                "The giant signature block is cosmetic noise."
            ),
            remediation_steps=[
                "Check the laptop Bluetooth driver version and update if needed.",
                "Remove and re-pair the Jabra Evolve2 85 headset.",
                "Ensure the Jabra Direct software is installed for optimal codec selection.",
                "Test with another Bluetooth headset to isolate the issue.",
            ],
        ),
        tags=["data-cleanup", "giant-signature", "bluetooth-headset"],
        description="Bluetooth headset issue followed by a 2KB corporate signature with ASCII art.",
    )


def _dc117_url_spam_tracking_params() -> EvalCase:
    """Teams meeting issue buried in URLs with UTM tracking parameters."""
    urls = "\n".join(
        [
            "https://teams.microsoft.com/l/meetup-join/19%3ameeting_NzQ4OGRiMzEtYzRiMi00Y2Q2LWJhMGEtYjZlMTQ3MTBkMTYw%40thread.v2/0?context=%7b%22Tid%22%3a%2272f988bf-86f1-41af-91ab-2d7cd011db47%22%2c%22Oid%22%3a%2249a60b09-0c75-45c1-b3b2-5c4b28f7a5cd%22%7d&utm_source=outlook&utm_medium=email&utm_campaign=weekly_standup&utm_content=join_button&utm_term=2026Q1&referrer=calendar_invite&session_id=a3f8b2c1-d4e5-6f7a-8b9c-0d1e2f3a4b5c",
            "https://contoso.sharepoint.com/sites/engineering/Shared%20Documents/Meeting%20Recordings/2026-03-17_standup.mp4?csf=1&web=1&e=AbCdEf&utm_source=teams&utm_medium=notification&utm_campaign=recording_ready&tracking_id=rec-2026-03-17-001&click_id=7f8a9b0c&referral_token=xYz123AbC",
            "https://contoso.sharepoint.com/sites/engineering/_layouts/15/Doc.aspx?sourcedoc=%7bGUID-HERE%7d&file=standup_notes.docx&action=default&mobileredirect=true&utm_source=teams&utm_medium=chat&utm_campaign=file_share&click_tracking=enabled&session=s3ss10n",
            "https://teams.microsoft.com/l/channel/19%3ae59bbfe1-c5f1-4cd6-b3a9-7a1b2c3d4e5f%40thread.tacv2/General?groupId=a1b2c3d4-e5f6-7890-abcd-ef1234567890&tenantId=72f988bf-86f1-41af-91ab-2d7cd011db47&utm_source=deeplink&utm_medium=app&utm_campaign=channel_nav",
        ]
    )
    description = (
        "I cannot join our daily standup Teams meeting. When I click the join link "
        "below, it opens the browser but then shows 'Something went wrong' with error "
        "code CAA20004. Here are all the links I have been trying:\n\n"
        f"{urls}\n\n"
        "I have tried clearing my browser cache, using the desktop app, and using "
        "incognito mode. None of them work. This has been happening since yesterday.\n\n"
        "— Kevin Park, Engineering"
    )
    return EvalCase(
        ticket=EvalTicket(
            ticket_id="INC-DC-117",
            subject="Cannot join Teams meetings - error CAA20004",
            description=description,
            reporter=Reporter(
                name="Kevin Park",
                email="k.park@contoso.com",
                department="Engineering",
            ),
            created_at="2026-03-18T10:45:00Z",
            channel=Channel.PORTAL,
            attachments=[],
        ),
        gold=GoldAnswer(
            ticket_id="INC-DC-117",
            category=Category.SOFTWARE,
            priority=Priority.P2,
            assigned_team=Team.ENTERPRISE_APPS,
            needs_escalation=False,
            missing_information=[MissingInfoField.DEVICE_INFO],
            next_best_action=(
                "Troubleshoot Teams error CAA20004 for the user. The long URLs with "
                "UTM tracking parameters are noise and should be ignored."
            ),
            remediation_steps=[
                "Clear the Teams desktop app cache (AppData/Roaming/Microsoft/Teams).",
                "Check Azure AD conditional access policies for the user.",
                "Verify the user's Office 365 license includes Teams.",
                "Re-authenticate the user's Azure AD session.",
            ],
        ),
        tags=["data-cleanup", "url-spam", "tracking-params", "teams"],
        description="Teams meeting issue buried in URLs with excessive UTM tracking parameters.",
    )


def _dc118_email_metadata_flood() -> EvalCase:
    """SMTP headers and DKIM signatures flooding the ticket before a keyboard issue."""
    headers = (
        "Received: from mail-yw1-f182.google.com (mail-yw1-f182.google.com [209.85.128.182])\n"
        "        by mx.contoso.com (Postfix) with ESMTPS id 4F5B23A0001\n"
        "        for <support@contoso.com>; Mon, 17 Mar 2026 14:32:11 -0700 (PDT)\n"
        "Received: by mail-yw1-f182.google.com with SMTP id a1b2c3d4e5.0\n"
        "        for <support@contoso.com>; Mon, 17 Mar 2026 14:32:10 -0700 (PDT)\n"
        "DKIM-Signature: v=1; a=rsa-sha256; c=relaxed/relaxed;\n"
        "        d=contoso.com; s=selector1;\n"
        "        h=from:to:subject:date:message-id:content-type;\n"
        "        bh=abcdefghijklmnopqrstuvwxyz0123456789ABCDEFG=;\n"
        "        b=VeryLongDKIMSignatureStringThatGoesOnForever\n"
        "          AndContinuesOnTheNextLineWithMoreBase64Data\n"
        "          AndEvenMoreDataBecauseDKIMSignaturesAreLong=\n"
        "Authentication-Results: mx.contoso.com;\n"
        "       dkim=pass (2048-bit key) header.d=contoso.com header.i=@contoso.com;\n"
        "       spf=pass (mx.contoso.com: domain of t.nguyen@contoso.com designates "
        "10.0.0.50 as permitted sender) smtp.mailfrom=t.nguyen@contoso.com;\n"
        "       dmarc=pass (p=REJECT sp=REJECT dis=NONE) header.from=contoso.com\n"
        "ARC-Seal: i=1; a=rsa-sha256; s=arcselector9901; d=contoso.com; cv=none;\n"
        "ARC-Message-Signature: i=1; a=rsa-sha256; c=relaxed/relaxed; d=contoso.com;\n"
        "X-MS-Exchange-Organization-AuthSource: CO1PR01MB1234.prod.exchangelabs.com\n"
        "X-MS-Exchange-Organization-SCL: 1\n"
        "X-MS-Exchange-Organization-Network-Message-Id: 9a8b7c6d-5e4f-3a2b-1c0d-ef9876543210\n"
        "X-Forefront-Antispam-Report: CIP:209.85.128.182;CTRY:US;LANG:en;SCL:1;SRV:;\n"
        "Return-Path: t.nguyen@contoso.com\n"
        "Message-ID: <CABx+XJ+abc123@mail.contoso.com>\n\n"
    )
    description = (
        f"{headers}"
        "Hi IT,\n\n"
        "My wireless keyboard (Logitech MX Keys) stopped working this morning. The "
        "USB receiver is plugged in, the keyboard has battery, and the green light "
        "blinks when I press keys, but nothing appears on screen. I tried the keyboard "
        "on my colleague's machine and it works fine, so I think it's something with "
        "my laptop (ThinkPad T14 Gen 3). I am in Building B, desk 4-210.\n\n"
        "Thanks,\nTony Nguyen\nLegal"
    )
    return EvalCase(
        ticket=EvalTicket(
            ticket_id="INC-DC-118",
            subject="Wireless keyboard not working",
            description=description,
            reporter=Reporter(
                name="Tony Nguyen",
                email="t.nguyen@contoso.com",
                department="Legal",
            ),
            created_at="2026-03-18T11:00:00Z",
            channel=Channel.EMAIL,
            attachments=[],
        ),
        gold=GoldAnswer(
            ticket_id="INC-DC-118",
            category=Category.HARDWARE,
            priority=Priority.P3,
            assigned_team=Team.ENDPOINT,
            needs_escalation=False,
            missing_information=[],
            next_best_action=(
                "Troubleshoot the Logitech MX Keys wireless keyboard on the ThinkPad T14. "
                "The exposed SMTP headers and DKIM signatures are email metadata noise."
            ),
            remediation_steps=[
                "Check USB receiver connection and try a different USB port.",
                "Uninstall and reinstall the Logitech Unifying receiver driver.",
                "Re-pair the keyboard using Logitech Options software.",
                "If unresolved, test with a wired keyboard to confirm laptop input works.",
            ],
        ),
        tags=["data-cleanup", "email-metadata", "smtp-headers", "keyboard"],
        description="Email SMTP headers, DKIM signatures, and SPF records flooding the description.",
    )


def _dc119_git_diff_inline() -> EvalCase:
    """Full git diff pasted inline with a deployment failure report."""
    git_diff = (
        "diff --git a/src/api/routes/deployment.py b/src/api/routes/deployment.py\n"
        "index 3a4b5c6..7d8e9f0 100644\n"
        "--- a/src/api/routes/deployment.py\n"
        "+++ b/src/api/routes/deployment.py\n"
        "@@ -42,7 +42,7 @@ def deploy_service(config: DeployConfig):\n"
        "-    timeout = config.get('timeout', 300)\n"
        "+    timeout = config.get('timeout', 30)\n"
        "     retries = config.get('retries', 3)\n"
        "     health_check_path = config.get('health_check', '/healthz')\n"
        " \n"
        "diff --git a/src/api/routes/health.py b/src/api/routes/health.py\n"
        "index 1a2b3c4..5d6e7f8 100644\n"
        "--- a/src/api/routes/health.py\n"
        "+++ b/src/api/routes/health.py\n"
        "@@ -15,10 +15,12 @@ class HealthCheck:\n"
        "-    def check_database(self):\n"
        "-        return self.db.ping()\n"
        "+    def check_database(self, timeout=5):\n"
        "+        try:\n"
        "+            return self.db.ping(timeout=timeout)\n"
        "+        except TimeoutError:\n"
        "+            return False\n"
        " \n"
        "diff --git a/config/production.yaml b/config/production.yaml\n"
        "index 9a8b7c6..5d4e3f2 100644\n"
        "--- a/config/production.yaml\n"
        "+++ b/config/production.yaml\n"
        "@@ -8,6 +8,8 @@ deployment:\n"
        "+  canary:\n"
        "+    enabled: true\n"
        "+    weight: 10\n"
        "   replicas: 3\n"
        "   resources:\n"
        "     memory: 512Mi\n"
    )
    description = (
        "Our production deployment pipeline failed at 2:47 AM during the scheduled "
        "release of API v2.14.0. The Azure DevOps pipeline shows the deployment timed "
        "out waiting for health checks. Here is the git diff of the changes in this "
        "release that I think might be relevant:\n\n"
        f"```\n{git_diff}```\n\n"
        "The health check endpoint /healthz returns 503 after the deployment but the "
        "pods are running. I suspect the timeout change from 300 to 30 seconds is the "
        "culprit. We need to roll back or fix this ASAP because the canary is serving "
        "10% of production traffic.\n\n"
        "— Amir Hassan, DevOps"
    )
    return EvalCase(
        ticket=EvalTicket(
            ticket_id="INC-DC-119",
            subject="PROD deployment failure - API v2.14.0 health check timeout",
            description=description,
            reporter=Reporter(
                name="Amir Hassan",
                email="a.hassan@contoso.com",
                department="DevOps",
            ),
            created_at="2026-03-18T03:00:00Z",
            channel=Channel.PORTAL,
            attachments=[],
        ),
        gold=GoldAnswer(
            ticket_id="INC-DC-119",
            category=Category.SOFTWARE,
            priority=Priority.P1,
            assigned_team=Team.ENTERPRISE_APPS,
            needs_escalation=True,
            missing_information=[],
            next_best_action=(
                "Roll back or fix the API v2.14.0 deployment. The timeout change from "
                "300s to 30s likely caused health check failures. Git diff is diagnostic context."
            ),
            remediation_steps=[
                "Immediately roll back the canary deployment to API v2.13.x.",
                "Revert the timeout change from 30 seconds back to 300 seconds.",
                "Validate health checks pass with corrected timeout in staging.",
                "Redeploy with the fix after staging validation.",
            ],
        ),
        tags=["data-cleanup", "git-diff", "deployment-failure"],
        description="Full git diff pasted inline obscuring a production deployment failure.",
    )


def _dc120_kubectl_describe_pod() -> EvalCase:
    """kubectl describe pod output dumped for a service connectivity issue."""
    kubectl_output = (
        "Name:             api-gateway-5b8f9c7d6e-x2k4m\n"
        "Namespace:        production\n"
        "Priority:         0\n"
        "Service Account:  api-gateway-sa\n"
        "Node:             aks-nodepool1-12345678-vmss000003/10.240.0.7\n"
        "Start Time:       Mon, 17 Mar 2026 22:15:00 +0000\n"
        "Labels:           app=api-gateway\n"
        "                  pod-template-hash=5b8f9c7d6e\n"
        "                  version=v2.13.1\n"
        "Annotations:      kubernetes.io/psp: restricted\n"
        "Status:           Running\n"
        "IP:               10.244.3.42\n"
        "IPs:\n"
        "  IP:             10.244.3.42\n"
        "Controlled By:    ReplicaSet/api-gateway-5b8f9c7d6e\n"
        "Containers:\n"
        "  api-gateway:\n"
        "    Container ID:   containerd://a1b2c3d4e5f6\n"
        "    Image:          contoso.azurecr.io/api-gateway:v2.13.1\n"
        "    Port:           8080/TCP\n"
        "    Host Port:      0/TCP\n"
        "    State:          Running\n"
        "      Started:      Mon, 17 Mar 2026 22:15:05 +0000\n"
        "    Ready:          True\n"
        "    Restart Count:  0\n"
        "    Limits:\n"
        "      cpu:     500m\n"
        "      memory:  512Mi\n"
        "    Requests:\n"
        "      cpu:     250m\n"
        "      memory:  256Mi\n"
        "    Liveness:   http-get http://:8080/healthz delay=30s timeout=5s period=10s\n"
        "    Readiness:  http-get http://:8080/ready delay=10s timeout=3s period=5s\n"
        "    Environment:\n"
        "      DB_HOST:       <set to the key 'host' in secret 'db-credentials'>\n"
        "      DB_PORT:       5432\n"
        "      REDIS_URL:     redis://redis-master:6379\n"
        "      LOG_LEVEL:     info\n"
        "Events:\n"
        "  Type    Reason     Age   From               Message\n"
        "  ----    ------     ----  ----               -------\n"
        "  Normal  Scheduled  8h    default-scheduler  Successfully assigned production/api-gateway\n"
        "  Normal  Pulled     8h    kubelet            Container image already present\n"
        "  Normal  Created    8h    kubelet            Created container api-gateway\n"
        "  Normal  Started    8h    kubelet            Started container api-gateway\n"
    )
    description = (
        "The internal billing service cannot reach the API gateway. Connections are "
        "timing out on port 8080. I ran kubectl describe on the pod and everything "
        "looks healthy, but the service mesh sidecar might be misconfigured. Here is "
        "the full pod describe output:\n\n"
        f"{kubectl_output}\n"
        "The billing team says this is blocking invoice processing. We need connectivity "
        "restored between billing-service and api-gateway in the production namespace.\n\n"
        "— Sarah Lee, Platform Engineering"
    )
    return EvalCase(
        ticket=EvalTicket(
            ticket_id="INC-DC-120",
            subject="Billing service cannot reach API gateway - connection timeout",
            description=description,
            reporter=Reporter(
                name="Sarah Lee",
                email="s.lee@contoso.com",
                department="Platform Engineering",
            ),
            created_at="2026-03-18T06:30:00Z",
            channel=Channel.PORTAL,
            attachments=[],
        ),
        gold=GoldAnswer(
            ticket_id="INC-DC-120",
            category=Category.NETWORK,
            priority=Priority.P2,
            assigned_team=Team.NETWORK_OPS,
            needs_escalation=False,
            missing_information=[MissingInfoField.ERROR_MESSAGE],
            next_best_action=(
                "Investigate service mesh connectivity between billing-service and "
                "api-gateway in the production namespace. The kubectl describe output "
                "is diagnostic context."
            ),
            remediation_steps=[
                "Check the service mesh sidecar configuration for both pods.",
                "Verify Kubernetes network policies allow traffic on port 8080.",
                "Test connectivity with kubectl exec and curl between pods.",
                "Review recent changes to the service mesh or network policies.",
            ],
        ),
        tags=["data-cleanup", "kubectl-describe", "service-connectivity"],
        description="kubectl describe pod output dumped for a service connectivity issue.",
    )


def _dc121_docker_compose_yaml_dump() -> EvalCase:
    """Full docker-compose.yml pasted inline with a container networking issue."""
    compose_yaml = (
        "version: '3.8'\n"
        "services:\n"
        "  web:\n"
        "    image: contoso/web-frontend:latest\n"
        "    ports:\n"
        "      - '3000:3000'\n"
        "    environment:\n"
        "      - API_URL=http://api:8080\n"
        "      - REDIS_URL=redis://cache:6379\n"
        "      - NODE_ENV=production\n"
        "    depends_on:\n"
        "      - api\n"
        "      - cache\n"
        "    networks:\n"
        "      - frontend\n"
        "      - backend\n"
        "    deploy:\n"
        "      replicas: 2\n"
        "      resources:\n"
        "        limits:\n"
        "          cpus: '0.5'\n"
        "          memory: 256M\n"
        "  api:\n"
        "    image: contoso/api-service:v3.2.1\n"
        "    ports:\n"
        "      - '8080:8080'\n"
        "    environment:\n"
        "      - DATABASE_URL=postgres://db:5432/appdb\n"
        "      - JWT_SECRET=${JWT_SECRET}\n"
        "      - LOG_LEVEL=debug\n"
        "    depends_on:\n"
        "      - db\n"
        "      - cache\n"
        "    networks:\n"
        "      - backend\n"
        "  db:\n"
        "    image: postgres:15-alpine\n"
        "    volumes:\n"
        "      - pgdata:/var/lib/postgresql/data\n"
        "    environment:\n"
        "      - POSTGRES_DB=appdb\n"
        "      - POSTGRES_USER=appuser\n"
        "      - POSTGRES_PASSWORD=${DB_PASSWORD}\n"
        "    networks:\n"
        "      - backend\n"
        "  cache:\n"
        "    image: redis:7-alpine\n"
        "    networks:\n"
        "      - backend\n"
        "networks:\n"
        "  frontend:\n"
        "    driver: bridge\n"
        "  backend:\n"
        "    driver: bridge\n"
        "    internal: true\n"
        "volumes:\n"
        "  pgdata:\n"
    )
    description = (
        "The web frontend container cannot connect to the API service. I get "
        "'ECONNREFUSED 172.18.0.3:8080' in the browser console. Here is our full "
        "docker-compose.yml:\n\n"
        f"```yaml\n{compose_yaml}```\n\n"
        "I think the problem might be that the web service is on both 'frontend' and "
        "'backend' networks but the API is only on 'backend' with internal:true. This "
        "was working fine until someone changed the backend network to internal last week.\n\n"
        "— Carlos Mendez, Development"
    )
    return EvalCase(
        ticket=EvalTicket(
            ticket_id="INC-DC-121",
            subject="Docker container networking - web cannot reach API",
            description=description,
            reporter=Reporter(
                name="Carlos Mendez",
                email="c.mendez@contoso.com",
                department="Development",
            ),
            created_at="2026-03-18T11:30:00Z",
            channel=Channel.PORTAL,
            attachments=[],
        ),
        gold=GoldAnswer(
            ticket_id="INC-DC-121",
            category=Category.SOFTWARE,
            priority=Priority.P2,
            assigned_team=Team.ENTERPRISE_APPS,
            needs_escalation=False,
            missing_information=[],
            next_best_action=(
                "Fix the Docker Compose network configuration. The backend network's "
                "internal:true setting is likely blocking web-to-API connectivity."
            ),
            remediation_steps=[
                "Review the backend network internal:true setting added last week.",
                "Either remove internal:true or add the web service to a shared network with API.",
                "Run docker-compose down && docker-compose up -d to apply changes.",
                "Verify web-to-API connectivity with docker exec curl tests.",
            ],
        ),
        tags=["data-cleanup", "docker-compose", "container-networking"],
        description="Full docker-compose.yml pasted inline with a container networking issue.",
    )


def _dc122_jwt_oauth_token_dump() -> EvalCase:
    """Auth trace with JWT and OAuth tokens pasted inline for an SSO issue."""
    jwt_token = (
        "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjFiYjk2MDVjLTIzN"
        "jktNGMzMC04NDFhLTZjNzc4MjhjMDIxYyJ9.eyJhdWQiOiIwMDAwMDAwMy0wM"
        "DAwLTAwMDAtYzAwMC0wMDAwMDAwMDAwMDAiLCJpc3MiOiJodHRwczovL3N0cy5"
        "3aW5kb3dzLm5ldC83MmY5ODhiZi04NmYxLTQxYWYtOTFhYi0yZDdjZDAxMWRi"
        "NDcvIiwiaWF0IjoxNzEwNjk0NDAwLCJuYmYiOjE3MTA2OTQ0MDAsImV4cCI6MT"
        "cxMDY5ODMwMH0.FAKE_SIGNATURE_DATA_HERE"
    )
    oauth_response = (
        '{"access_token": "' + jwt_token + '", '
        '"token_type": "Bearer", '
        '"expires_in": 3600, '
        '"refresh_token": "0.AVYAv4j5ci..FAKE_REFRESH_TOKEN", '
        '"scope": "openid profile email User.Read", '
        '"id_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.FAKE_ID_TOKEN"}'
    )
    description = (
        "SSO is not working for our Salesforce integration. When users click the "
        "Salesforce tile in the Azure AD My Apps portal, they get redirected back to "
        "the login page in a loop. I captured the auth flow and here are the tokens:\n\n"
        f"OAuth Response:\n{oauth_response}\n\n"
        f"Decoded JWT claims show the audience is Microsoft Graph but it should be the "
        "Salesforce app ID (2f4a7b8c-1d3e-5f6a-9b0c-8d7e6f5a4b3c). I think the app "
        "registration in Azure AD has the wrong redirect URI or the wrong audience "
        "configured.\n\n"
        "This is affecting all 45 sales team members.\n\n"
        "— Lisa Park, IT Operations"
    )
    return EvalCase(
        ticket=EvalTicket(
            ticket_id="INC-DC-122",
            subject="SSO broken for Salesforce - redirect loop",
            description=description,
            reporter=Reporter(
                name="Lisa Park",
                email="l.park@contoso.com",
                department="IT Operations",
            ),
            created_at="2026-03-18T11:45:00Z",
            channel=Channel.PORTAL,
            attachments=[],
        ),
        gold=GoldAnswer(
            ticket_id="INC-DC-122",
            category=Category.ACCESS_AUTH,
            priority=Priority.P2,
            assigned_team=Team.IAM,
            needs_escalation=False,
            missing_information=[],
            next_best_action=(
                "Fix the Azure AD app registration for the Salesforce SSO integration. "
                "The JWT/OAuth tokens are diagnostic evidence showing a misconfigured audience."
            ),
            remediation_steps=[
                "Check the Azure AD app registration for Salesforce and correct the audience.",
                "Verify the redirect URI matches Salesforce's expected callback URL.",
                "Update the token configuration to target the Salesforce app ID.",
                "Test SSO login flow with a test account before rolling out.",
            ],
        ),
        tags=["data-cleanup", "jwt-token", "oauth-dump", "sso"],
        description="JWT and OAuth token dumps pasted inline for an SSO redirect loop issue.",
    )


def _dc123_ansi_escape_codes() -> EvalCase:
    """Terminal output with ANSI color codes from a build failure."""
    ansi_output = (
        "\033[1m\033[31mERROR\033[0m in \033[36m./src/components/Dashboard.tsx\033[0m"
        ":\033[33m42\033[0m:\033[33m17\033[0m\n"
        "\033[31m  TS2345: Argument of type 'string' is not assignable to parameter of type 'number'.\033[0m\n"
        "\n"
        "\033[1m\033[31mERROR\033[0m in \033[36m./src/services/api.ts\033[0m:\033[33m128\033[0m:\033[33m5\033[0m\n"
        "\033[31m  TS2307: Cannot find module '@contoso/shared-types' or its corresponding type declarations.\033[0m\n"
        "\n"
        "\033[1m\033[33mWARNING\033[0m in \033[36m./src/utils/format.ts\033[0m:\033[33m15\033[0m:\033[33m1\033[0m\n"
        "\033[33m  TS6133: 'lodash' is declared but its value is never read.\033[0m\n"
        "\n"
        "\033[1m\033[31mERROR\033[0m in \033[36m./src/hooks/useAuth.ts\033[0m:\033[33m67\033[0m:\033[33m22\033[0m\n"
        "\033[31m  TS2739: Type '{}' is missing the following properties"
        " from type 'AuthContext': user, token, refresh\033[0m\n"
        "\n"
        "\033[1m\033[37m\033[41m FAIL \033[0m \033[1mBuild failed with 3 errors and 1 warning\033[0m\n"
        "\033[2mTime: 47.2s\033[0m\n"
    )
    description = (
        "Our frontend CI/CD build is failing on the develop branch. Here is the "
        "build output from the terminal:\n\n"
        f"{ansi_output}\n"
        "The main issue seems to be the missing @contoso/shared-types package. "
        "I think someone removed it from package.json in the last merge. The build "
        "was green on Friday and started failing Monday morning.\n\n"
        "— Emily Zhang, Frontend Engineering"
    )
    return EvalCase(
        ticket=EvalTicket(
            ticket_id="INC-DC-123",
            subject="Frontend CI build failing - TypeScript errors",
            description=description,
            reporter=Reporter(
                name="Emily Zhang",
                email="e.zhang@contoso.com",
                department="Frontend Engineering",
            ),
            created_at="2026-03-18T08:00:00Z",
            channel=Channel.CHAT,
            attachments=[],
        ),
        gold=GoldAnswer(
            ticket_id="INC-DC-123",
            category=Category.SOFTWARE,
            priority=Priority.P2,
            assigned_team=Team.ENTERPRISE_APPS,
            needs_escalation=False,
            missing_information=[],
            next_best_action=(
                "Restore the missing @contoso/shared-types dependency in the develop branch. "
                "The ANSI escape codes are terminal rendering artifacts."
            ),
            remediation_steps=[
                "Check recent commits on develop for changes to package.json.",
                "Restore @contoso/shared-types to package.json dependencies.",
                "Run npm install and verify TypeScript compilation succeeds.",
                "Fix the remaining TS2345 and TS2739 type errors in Dashboard.tsx and useAuth.ts.",
            ],
        ),
        tags=["data-cleanup", "ansi-escape-codes", "build-failure"],
        description="Terminal output with ANSI color escape codes from a CI build failure.",
    )


def _dc124_misaligned_spreadsheet_paste() -> EvalCase:
    """Misaligned TSV data from Excel pasted inline with a data import issue."""
    tsv_data = (
        "Employee ID\tName\tDepartment\tStart Date\tSalary\tLocation\tManager\n"
        "10001\tSmith, John A.\tEngineering\t2021-03-15\t95000\tRedmond\tJane Doe\n"
        "10002\tGarcia, Maria\t\tSales\t2020-07-22\t87000\tChicago\tBob Wilson\n"
        "10003\tKim, David\tMarketing\t2022-01-10\t\t78000\tNew York\tAlice Chen\n"
        "\t10004\tPatel, Priya\tHR\t2019-11-05\t92000\tRedmond\n"
        "10005\tJohnson, Robert\tFinance\t2023-04-18\t81000\tAustin\tTom Brown\n"
        "10006\tWilliams, Sarah\tEngineering\t2021-09-30\t99000\tRedmond\tJane Doe\t\textra_col\n"
        "10007\tBrown,\tThomas\tLegal\t2020-02-14\t88000\tChicago\tEva Martinez\n"
        "10008\tLee, Jennifer\tOperations\t2022-06-01\t76000\tNew York\tAlice Chen\n"
        "10009\tNguyen\tTony\tIT\t2018-08-20\t105000\tRedmond\tMike Johnson\n"
        "10010\tMartinez, Eva\tLegal\t2017-12-01\t115000\tChicago\t\n"
    )
    description = (
        "I am trying to import employee data into the new HR system but the bulk "
        "import keeps failing with 'column mismatch' errors. Here is the data I "
        "copied from the Excel spreadsheet:\n\n"
        f"{tsv_data}\n"
        "As you can see, some rows have shifted columns (10002 has an empty department "
        "pushing everything right, 10004 has a leading tab, 10007 has the name split "
        "across two columns). The Excel file has 2,400 rows and about 30% of them "
        "have similar alignment issues from a previous CSV import.\n\n"
        "Can you help fix the import template or clean the data?\n\n"
        "— Rachel Kim, HR Systems"
    )
    return EvalCase(
        ticket=EvalTicket(
            ticket_id="INC-DC-124",
            subject="HR bulk import failing - column mismatch errors",
            description=description,
            reporter=Reporter(
                name="Rachel Kim",
                email="r.kim@contoso.com",
                department="HR Systems",
            ),
            created_at="2026-03-18T13:00:00Z",
            channel=Channel.PORTAL,
            attachments=[],
        ),
        gold=GoldAnswer(
            ticket_id="INC-DC-124",
            category=Category.SOFTWARE,
            priority=Priority.P3,
            assigned_team=Team.ENTERPRISE_APPS,
            needs_escalation=False,
            missing_information=[MissingInfoField.APPLICATION_VERSION],
            next_best_action=(
                "Help clean the misaligned employee data for bulk import. The pasted "
                "TSV data demonstrates the column alignment issues."
            ),
            remediation_steps=[
                "Export a clean CSV template from the HR system with fixed headers.",
                "Write a data cleaning script to fix misaligned columns in the source data.",
                "Validate the cleaned data against the import schema before reimporting.",
                "Perform a test import with a small subset before the full 2,400 row import.",
            ],
        ),
        tags=["data-cleanup", "misaligned-spreadsheet", "data-import"],
        description="Misaligned TSV data from Excel paste causing a data import failure.",
    )


def _dc125_zero_width_unicode() -> EvalCase:
    """Zero-width Unicode characters scattered throughout a software crash ticket."""
    zwsp = "\u200b"
    zwj = "\u200d"
    zwnj = "\u200c"
    description = (
        f"The{zwsp} accounting{zwj} software{zwsp} (SAP{zwnj} Business{zwsp} One "
        f"v10.0{zwj} FP{zwsp}2304) keeps{zwsp} crashing{zwj} when{zwsp} I{zwnj} try "
        f"to{zwsp} generate{zwj} the{zwsp} quarterly{zwnj} financial{zwsp} report. "
        f"It{zwj} crashes{zwsp} with{zwnj} error{zwsp} code{zwj} 0xC0000005{zwsp} "
        f"(access{zwnj} violation){zwj} about{zwsp} 30{zwnj} seconds{zwsp} into{zwj} "
        f"the{zwsp} report{zwnj} generation{zwj} process.{zwsp}\n\n"
        f"Steps{zwsp} to{zwj} reproduce:{zwnj}\n"
        f"1.{zwsp} Open{zwj} SAP{zwsp} Business{zwnj} One{zwsp}\n"
        f"2.{zwj} Go{zwsp} to{zwnj} Financial{zwsp} Reports{zwj} >{zwsp} Quarterly{zwnj}\n"
        f"3.{zwsp} Select{zwj} Q1{zwsp} 2026{zwnj} and{zwsp} click{zwj} Generate{zwsp}\n"
        f"4.{zwnj} Application{zwsp} freezes{zwj} for{zwsp} 30s{zwnj} then{zwsp} crashes{zwj}\n\n"
        f"This{zwsp} is{zwnj} blocking{zwj} our{zwsp} quarterly{zwnj} close{zwsp} process.{zwj} "
        f"The{zwsp} deadline{zwnj} is{zwj} this{zwsp} Friday.{zwnj}\n\n"
        f"—{zwsp} Ahmed{zwj} El-Sayed,{zwsp} Accounting{zwnj}"
    )
    return EvalCase(
        ticket=EvalTicket(
            ticket_id="INC-DC-125",
            subject="SAP Business One crashing on quarterly report generation",
            description=description,
            reporter=Reporter(
                name="Ahmed El-Sayed",
                email="a.elsayed@contoso.com",
                department="Accounting",
            ),
            created_at="2026-03-18T14:00:00Z",
            channel=Channel.PORTAL,
            attachments=[],
        ),
        gold=GoldAnswer(
            ticket_id="INC-DC-125",
            category=Category.SOFTWARE,
            priority=Priority.P2,
            assigned_team=Team.ENTERPRISE_APPS,
            needs_escalation=False,
            missing_information=[MissingInfoField.DEVICE_INFO],
            next_best_action=(
                "Investigate the SAP Business One crash (0xC0000005) during quarterly "
                "report generation. Zero-width Unicode characters in the ticket are noise."
            ),
            remediation_steps=[
                "Collect the SAP Business One crash dump from the user's machine.",
                "Check if SAP FP2304 has known issues with the quarterly report module.",
                "Test report generation on a clean machine with the same SAP version.",
                "Apply any available SAP hotfixes for the access violation error.",
            ],
        ),
        tags=["data-cleanup", "zero-width-unicode", "software-crash"],
        description="Zero-width Unicode characters scattered throughout a software crash report.",
    )


def _dc126_extremely_long_subject() -> EvalCase:
    """Extremely long subject line (200+ chars) that may break subject-line parsers."""
    long_subject = (
        "URGENT VPN connectivity failure on all Windows 11 laptops across Building 7 floors 3-5 "
        "affecting approximately 120 users since this morning 9:15 AM EST with error code "
        "VPN_TIMEOUT_0x800704CF and we need immediate resolution before the board meeting at 2 PM"
    )
    return EvalCase(
        ticket=EvalTicket(
            ticket_id="INC-DC-126",
            subject=long_subject,
            description=(
                "Hi Support,\n\n"
                "As noted in the very long subject line above, we are experiencing a widespread "
                "VPN connectivity failure across Building 7, floors 3 through 5. Approximately "
                "120 users are impacted and none of them can establish a tunnel to the corporate "
                "network using GlobalProtect v6.1.2 on Windows 11 23H2.\n\n"
                "The issue started at approximately 09:15 AM EST today. Users see error code "
                "VPN_TIMEOUT_0x800704CF after the client spins for about 45 seconds. We have "
                "verified that the users' internet connections are working fine — they can browse "
                "external sites without issue. The problem appears limited to the VPN tunnel "
                "establishment phase.\n\n"
                "We have already tried:\n"
                "- Restarting the GlobalProtect service on several machines\n"
                "- Flushing DNS caches\n"
                "- Connecting from a different SSID\n"
                "- Rebooting laptops entirely\n\n"
                "None of these steps resolved the issue. The board meeting is at 2 PM and several "
                "executives in Building 7 need VPN access to present financial dashboards hosted "
                "on the internal BI server.\n\n"
                "Please escalate immediately.\n\n"
                "Thanks,\nRachel Simmons\nIT Liaison — Building 7\n"
                "rachel.simmons@contoso.com"
            ),
            reporter=Reporter(
                name="Rachel Simmons",
                email="rachel.simmons@contoso.com",
                department="Facilities IT",
            ),
            created_at="2026-04-07T09:20:00Z",
            channel=Channel.EMAIL,
        ),
        gold=GoldAnswer(
            ticket_id="INC-DC-126",
            category=Category.NETWORK,
            priority=Priority.P2,
            assigned_team=Team.NETWORK_OPS,
            needs_escalation=False,
            missing_information=[MissingInfoField.ERROR_MESSAGE, MissingInfoField.NETWORK_LOCATION],
            next_best_action=(
                "Investigate the GlobalProtect VPN tunnel failure (error VPN_TIMEOUT_0x800704CF) "
                "affecting Building 7 users and check the VPN concentrator logs for the relevant "
                "gateway."
            ),
            remediation_steps=[
                "Review GlobalProtect gateway and portal logs for connection attempts from Building 7 subnets.",
                "Check if a recent firewall policy change is blocking tunnel establishment on the relevant ports.",
                "Verify that the VPN concentrator serving Building 7 is healthy and not resource-exhausted.",
                "Test VPN connectivity from a known-good machine on the same network segment.",
            ],
        ),
        tags=["data-cleanup", "extremely_long_subject", "truncation"],
        description="Extremely long subject line (200+ chars) that may break subject-line parsing or truncation logic.",
    )


def _dc127_svg_data_uri() -> EvalCase:
    """SVG data URIs pasted inline, adding vector-graphic noise to a hardware monitor issue."""
    svg_blob_1 = (
        "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZp"
        "ZXdCb3g9IjAgMCAxMDAgMTAwIj48Y2lyY2xlIGN4PSI1MCIgY3k9IjUwIiByPSI0MCIgZmlsbD0icmVk"
        "Ii8+PC9zdmc+"
    )
    svg_blob_2 = (
        "data:image/svg+xml,%3Csvg%20xmlns%3D%22http%3A//www.w3.org/2000/svg%22%20width%3D%22"
        "200%22%20height%3D%22200%22%3E%3Crect%20width%3D%22200%22%20height%3D%22200%22%20fill"
        "%3D%22%23ccc%22/%3E%3C/svg%3E"
    )
    return EvalCase(
        ticket=EvalTicket(
            ticket_id="INC-DC-127",
            subject="External monitor flickering and losing signal intermittently",
            description=(
                "My external monitor (Dell U2723QE) keeps flickering and dropping signal every "
                "few minutes. I'm connected via USB-C to my ThinkPad T14s Gen 4. The issue "
                "started after last week's docking station firmware update.\n\n"
                "I tried to capture what the screen looks like when it flickers. Here are the "
                "diagrams I drew in our SVG editor to illustrate the problem:\n\n"
                f"[Flicker pattern diagram]: {svg_blob_1}\n\n"
                f"[Signal loss timing chart]: {svg_blob_2}\n\n"
                "As shown in the diagrams above, the flicker occurs in a roughly 3-second cycle "
                "— the monitor goes black for about 0.5 seconds, then comes back. The USB-C "
                "connection indicator on the monitor blinks amber during the dropout.\n\n"
                "I also noticed that the issue does not occur when I connect via HDMI directly, "
                "bypassing the docking station. This makes me think it is related to the USB-C "
                "DisplayPort alt-mode negotiation or the docking station firmware.\n\n"
                "This is really impacting my productivity as I rely on the external monitor for "
                "code reviews and design work.\n\n"
                "— Jorge Medina, Engineering\njorge.medina@contoso.com"
            ),
            reporter=Reporter(
                name="Jorge Medina",
                email="jorge.medina@contoso.com",
                department="Engineering",
            ),
            created_at="2026-04-07T10:15:00Z",
            channel=Channel.PORTAL,
        ),
        gold=GoldAnswer(
            ticket_id="INC-DC-127",
            category=Category.HARDWARE,
            priority=Priority.P3,
            assigned_team=Team.ENDPOINT,
            needs_escalation=False,
            missing_information=[MissingInfoField.DEVICE_INFO, MissingInfoField.APPLICATION_VERSION],
            next_best_action=(
                "Investigate the USB-C DisplayPort alt-mode signal dropout on the Dell U2723QE "
                "connected through the docking station after the recent firmware update."
            ),
            remediation_steps=[
                "Check the docking station firmware version and compare with the previous working version.",
                "Roll back the docking station firmware if a previous version is available.",
                "Test with a different USB-C cable to rule out cable quality issues.",
                "Update the ThinkPad T14s USB-C/Thunderbolt drivers to the latest version.",
            ],
        ),
        tags=["data-cleanup", "svg_data_uri", "inline_vector"],
        description="SVG data URIs embedded inline add vector-graphic noise to a hardware monitor ticket.",
    )


def _dc128_prometheus_metrics_flood() -> EvalCase:
    """Prometheus metrics exposition format pasted into a database performance ticket."""
    prom_metrics = (
        "# HELP pg_stat_activity_count Number of connections in each state\n"
        "# TYPE pg_stat_activity_count gauge\n"
        'pg_stat_activity_count{datname="proddb",state="active"} 47\n'
        'pg_stat_activity_count{datname="proddb",state="idle"} 312\n'
        'pg_stat_activity_count{datname="proddb",state="idle in transaction"} 8\n'
        "# HELP pg_database_size_bytes Database size in bytes\n"
        "# TYPE pg_database_size_bytes gauge\n"
        'pg_database_size_bytes{datname="proddb"} 1.284739481e+11\n'
        'pg_database_size_bytes{datname="analyticsdb"} 5.83920384e+10\n'
        "# HELP pg_locks_count Number of locks\n"
        "# TYPE pg_locks_count gauge\n"
        'pg_locks_count{datname="proddb",mode="AccessShareLock"} 89\n'
        'pg_locks_count{datname="proddb",mode="RowExclusiveLock"} 23\n'
        'pg_locks_count{datname="proddb",mode="ExclusiveLock"} 2\n'
        "# HELP pg_replication_lag_seconds Replication lag in seconds\n"
        "# TYPE pg_replication_lag_seconds gauge\n"
        "pg_replication_lag_seconds 4.572\n"
        "# HELP node_cpu_seconds_total CPU seconds total\n"
        "# TYPE node_cpu_seconds_total counter\n"
        'node_cpu_seconds_total{cpu="0",mode="idle"} 2.839471293e+06\n'
        'node_cpu_seconds_total{cpu="0",mode="system"} 148293.47\n'
        'node_cpu_seconds_total{cpu="0",mode="user"} 529381.82\n'
    )
    return EvalCase(
        ticket=EvalTicket(
            ticket_id="INC-DC-128",
            subject="Production database slow queries and connection pool exhaustion",
            description=(
                "We are seeing severe performance degradation on our production PostgreSQL "
                "cluster (pg-prod-east-01). Query response times have increased from ~50ms to "
                "over 3 seconds for simple SELECT statements, and our application is throwing "
                "connection pool exhaustion errors.\n\n"
                "I pulled the following Prometheus metrics from our monitoring stack to help "
                "diagnose:\n\n"
                f"{prom_metrics}\n"
                "As you can see, we have 312 idle connections and the replication lag is at "
                "4.5 seconds, which is way above our 1-second SLA threshold. The lock count "
                "also shows 2 exclusive locks which might be causing the bottleneck.\n\n"
                "The issue started around 06:00 UTC this morning, which coincides with our "
                "nightly ETL batch job window. We suspect the ETL process is holding long-running "
                "transactions that are blocking other queries.\n\n"
                "This is impacting our customer-facing API — error rates have spiked to 12% "
                "on the order service.\n\n"
                "— Priya Chandrasekaran, Data Engineering\npriya.c@contoso.com"
            ),
            reporter=Reporter(
                name="Priya Chandrasekaran",
                email="priya.c@contoso.com",
                department="Data Engineering",
            ),
            created_at="2026-04-07T06:45:00Z",
            channel=Channel.CHAT,
        ),
        gold=GoldAnswer(
            ticket_id="INC-DC-128",
            category=Category.DATA_STORAGE,
            priority=Priority.P2,
            assigned_team=Team.DATA_PLATFORM,
            needs_escalation=False,
            missing_information=[MissingInfoField.ERROR_MESSAGE, MissingInfoField.TIMESTAMP],
            next_best_action=(
                "Investigate PostgreSQL connection pool exhaustion and long-running transactions "
                "on pg-prod-east-01 that coincide with the nightly ETL window."
            ),
            remediation_steps=[
                "Identify and terminate any long-running transactions from the ETL batch job using pg_stat_activity.",
                "Review the ETL process for missing COMMIT statements or excessively large transactions.",
                "Increase the connection pool max size temporarily to restore API availability.",
                "Set a statement_timeout for the ETL user role to prevent future runaway queries.",
            ],
        ),
        tags=["data-cleanup", "prometheus_metrics", "monitoring_flood"],
        description="Prometheus metrics exposition block pasted into a database performance ticket.",
    )


def _dc129_systeminfo_dump() -> EvalCase:
    """Windows systeminfo command output pasted into a hardware issue ticket."""
    sysinfo = (
        "Host Name:                 WS-DMARTIN-PC\n"
        "OS Name:                   Microsoft Windows 11 Enterprise\n"
        "OS Version:                10.0.22631 N/A Build 22631\n"
        "OS Manufacturer:           Microsoft Corporation\n"
        "OS Configuration:          Member Workstation\n"
        "OS Build Type:             Multiprocessor Free\n"
        "Registered Owner:          Contoso Ltd\n"
        "System Manufacturer:       Dell Inc.\n"
        "System Model:              Latitude 5540\n"
        "System Type:               x64-based PC\n"
        "Processor(s):              1 Processor(s) Installed.\n"
        "                           [01]: Intel64 Family 6 Model 186 Stepping 3 ~2400 Mhz\n"
        "BIOS Version:              Dell Inc. 1.18.0, 2/14/2026\n"
        "Total Physical Memory:     16,148 MB\n"
        "Available Physical Memory: 3,241 MB\n"
        "Virtual Memory: Max Size:  18,708 MB\n"
        "Virtual Memory: In Use:    14,892 MB\n"
        "Page File Location(s):     C:\\pagefile.sys\n"
        "Network Card(s):           3 NIC(s) Installed.\n"
        "                           [01]: Intel(R) Ethernet Connection I219-LM\n"
        "                           [02]: Intel(R) Wi-Fi 6E AX211 160MHz\n"
        "                           [03]: Bluetooth Device (Personal Area Network)\n"
        "Hyper-V Requirements:      VM Monitor Mode Extensions: Yes\n"
    )
    return EvalCase(
        ticket=EvalTicket(
            ticket_id="INC-DC-129",
            subject="Laptop overheating and fans running at max speed constantly",
            description=(
                "My Dell Latitude 5540 has been overheating badly for the past three days. "
                "The fans are running at maximum speed constantly, even when I'm just reading "
                "email in Outlook. The bottom of the laptop is too hot to touch and I'm worried "
                "about hardware damage.\n\n"
                "I ran systeminfo so you can see my machine details:\n\n"
                f"{sysinfo}\n"
                "As you can see from the memory figures, I only have about 3 GB of RAM free "
                "out of 16 GB, and the virtual memory usage is very high. I don't know if that's "
                "related to the overheating or not.\n\n"
                "I checked Task Manager and the top CPU consumers are:\n"
                "- Microsoft Teams: 18-25% CPU\n"
                "- Windows Search Indexer: 12-15% CPU\n"
                "- System (ntoskrnl.exe): 8-10% CPU\n\n"
                "The laptop is about 14 months old so just outside the 1-year warranty. I've "
                "already tried cleaning the vents with compressed air but it didn't help.\n\n"
                "— Derek Martin, Marketing\nderek.martin@contoso.com"
            ),
            reporter=Reporter(
                name="Derek Martin",
                email="derek.martin@contoso.com",
                department="Marketing",
            ),
            created_at="2026-04-07T11:30:00Z",
            channel=Channel.EMAIL,
        ),
        gold=GoldAnswer(
            ticket_id="INC-DC-129",
            category=Category.HARDWARE,
            priority=Priority.P3,
            assigned_team=Team.ENDPOINT,
            needs_escalation=False,
            missing_information=[MissingInfoField.DEVICE_INFO],
            next_best_action=(
                "Diagnose the sustained overheating on the Dell Latitude 5540 — determine "
                "whether the root cause is a thermal paste issue, blocked airflow, or excessive "
                "background CPU load."
            ),
            remediation_steps=[
                "Run Dell SupportAssist hardware diagnostics to check for thermal sensor or fan faults.",
                "Review startup programs and disable unnecessary background processes consuming CPU.",
                "Check for pending BIOS and thermal management firmware updates from Dell.",
                "If diagnostics pass, schedule a physical inspection to clean or replace thermal paste.",
            ],
        ),
        tags=["data-cleanup", "systeminfo_dump", "command_paste"],
        description="Windows systeminfo output pasted into a laptop overheating ticket adds command noise.",
    )


def _dc130_splunk_search_results() -> EvalCase:
    """Splunk search results table pasted into a security incident ticket."""
    splunk_output = (
        "| _time                  | src_ip         | dest_ip       | action  | signature              | severity |\n"
        "|------------------------|----------------|---------------|---------|------------------------|----------|\n"
        "| 2026-04-06T23:14:02Z   | 10.42.7.19     | 10.50.1.100   | blocked | ET SCAN Nmap SYN       | high     |\n"
        "| 2026-04-06T23:14:03Z   | 10.42.7.19     | 10.50.1.101   | blocked | ET SCAN Nmap SYN       | high     |\n"
        "| 2026-04-06T23:14:03Z   | 10.42.7.19     | 10.50.1.102   | blocked | ET SCAN Nmap SYN       | high     |\n"
        "| 2026-04-06T23:14:04Z   | 10.42.7.19     | 10.50.1.103   | blocked | ET SCAN Nmap SYN       | high     |\n"
        "| 2026-04-06T23:14:05Z   | 10.42.7.19     | 10.50.1.104   | allowed | ET SCAN Nmap SYN       | high     |\n"
        "| 2026-04-06T23:14:07Z   | 10.42.7.19     | 10.50.1.104   | allowed | ET POLICY SSH conn     | medium   |\n"
        "| 2026-04-06T23:14:09Z   | 10.42.7.19     | 10.50.1.104   | allowed | ET POLICY SSH brute    | critical |\n"
        "| 2026-04-06T23:15:22Z   | 10.42.7.19     | 10.50.1.104   | allowed | ET TROJAN Callback     | critical |\n"
        "| 2026-04-06T23:17:45Z   | 10.50.1.104    | 203.0.113.42  | allowed | ET POLICY DNS Exfil    | critical |\n"
        "| 2026-04-06T23:18:01Z   | 10.50.1.104    | 203.0.113.42  | blocked | ET TROJAN C2 Beacon    | critical |\n"
    )
    return EvalCase(
        ticket=EvalTicket(
            ticket_id="INC-DC-130",
            subject="Potential lateral movement and C2 beacon detected from internal host",
            description=(
                "Our SIEM flagged suspicious activity originating from 10.42.7.19, which appears "
                "to be conducting port scanning followed by SSH brute-force attacks against our "
                "internal server subnet (10.50.1.0/24). One host (10.50.1.104) was successfully "
                "compromised and has started communicating with an external IP (203.0.113.42) "
                "that matches known C2 infrastructure.\n\n"
                "Here are the relevant Splunk search results:\n\n"
                f"{splunk_output}\n"
                "The timeline shows a clear attack chain: SYN scan → SSH brute force → callback → "
                "DNS exfiltration → C2 beacon. The IDS blocked most of the initial scans but "
                "10.50.1.104 was reached and compromised.\n\n"
                "I have already isolated 10.50.1.104 from the network via the switch port. "
                "However, 10.42.7.19 is still active and may be an already-compromised internal "
                "machine being used as a pivot point.\n\n"
                "Need immediate assistance from the security team to investigate the full scope "
                "of the breach.\n\n"
                "— Kwame Asante, SOC Analyst\nkwame.asante@contoso.com"
            ),
            reporter=Reporter(
                name="Kwame Asante",
                email="kwame.asante@contoso.com",
                department="Security Operations",
            ),
            created_at="2026-04-06T23:25:00Z",
            channel=Channel.PORTAL,
        ),
        gold=GoldAnswer(
            ticket_id="INC-DC-130",
            category=Category.SECURITY,
            priority=Priority.P2,
            assigned_team=Team.SECURITY_OPS,
            needs_escalation=False,
            missing_information=[MissingInfoField.AFFECTED_SYSTEM, MissingInfoField.BUSINESS_IMPACT],
            next_best_action=(
                "Investigate the lateral movement chain from 10.42.7.19 and the potential "
                "compromise of 10.50.1.104 including any data exfiltration to 203.0.113.42."
            ),
            remediation_steps=[
                "Isolate 10.42.7.19 from the network immediately and image the disk for forensics.",
                "Perform a full forensic analysis of 10.50.1.104 to determine the scope of compromise.",
                "Block 203.0.113.42 at the perimeter firewall and check historical logs for prior communication.",
                "Reset credentials for all accounts that had sessions on either compromised host.",
            ],
        ),
        tags=["data-cleanup", "splunk_results", "siem_paste"],
        description="Splunk search results table pasted into a security incident ticket.",
    )


def _dc131_arm_bicep_template() -> EvalCase:
    """ARM/Bicep Infrastructure-as-Code template dump in a deployment failure ticket."""
    bicep_snippet = (
        "// main.bicep - Production App Service deployment\n"
        "param location string = resourceGroup().location\n"
        "param appName string = 'contoso-orders-api'\n"
        "param skuName string = 'P1v3'\n\n"
        "resource appServicePlan 'Microsoft.Web/serverfarms@2022-09-01' = {\n"
        "  name: '${appName}-plan'\n"
        "  location: location\n"
        "  sku: {\n"
        "    name: skuName\n"
        "    tier: 'PremiumV3'\n"
        "    size: 'P1v3'\n"
        "    capacity: 3\n"
        "  }\n"
        "  kind: 'linux'\n"
        "  properties: {\n"
        "    reserved: true\n"
        "  }\n"
        "}\n\n"
        "resource webApp 'Microsoft.Web/sites@2022-09-01' = {\n"
        "  name: appName\n"
        "  location: location\n"
        "  properties: {\n"
        "    serverFarmId: appServicePlan.id\n"
        "    siteConfig: {\n"
        "      linuxFxVersion: 'PYTHON|3.11'\n"
        "      alwaysOn: true\n"
        "      ftpsState: 'Disabled'\n"
        "      minTlsVersion: '1.2'\n"
        "      appSettings: [\n"
        "        { name: 'DB_CONNECTION', value: '@Microsoft.KeyVault(...)' }\n"
        "        { name: 'REDIS_URL', value: '@Microsoft.KeyVault(...)' }\n"
        "      ]\n"
        "    }\n"
        "  }\n"
        "}\n"
    )
    return EvalCase(
        ticket=EvalTicket(
            ticket_id="INC-DC-131",
            subject="Azure App Service deployment failing with SkuNotAvailable error",
            description=(
                "Our CI/CD pipeline is failing to deploy the Orders API to Azure App Service. "
                "The deployment started failing yesterday after we changed the SKU from S1 to "
                "P1v3 in our Bicep template. The error from the ARM deployment is:\n\n"
                '"Code: SkuNotAvailable, Message: The requested size for resource '
                "'contoso-orders-api-plan' is currently not available in location 'eastus2' "
                "for subscription '...' . Please try another size or deploy to a different "
                'region."\n\n'
                "Here is the Bicep template we are using:\n\n"
                f"{bicep_snippet}\n"
                "We need the P1v3 SKU for the performance requirements of the Orders API — "
                "the S1 tier was causing timeout issues under load. The deployment must target "
                "eastus2 because that's where our SQL and Redis instances are located.\n\n"
                "Can someone help us find an alternative approach? Perhaps a different availability "
                "zone within eastus2, or a comparable SKU that is available?\n\n"
                "— Tomás Rivera, Platform Engineering\ntomas.rivera@contoso.com"
            ),
            reporter=Reporter(
                name="Tomás Rivera",
                email="tomas.rivera@contoso.com",
                department="Platform Engineering",
            ),
            created_at="2026-04-07T08:00:00Z",
            channel=Channel.CHAT,
        ),
        gold=GoldAnswer(
            ticket_id="INC-DC-131",
            category=Category.SOFTWARE,
            priority=Priority.P2,
            assigned_team=Team.ENTERPRISE_APPS,
            needs_escalation=False,
            missing_information=[MissingInfoField.ENVIRONMENT_DETAILS, MissingInfoField.ERROR_MESSAGE],
            next_best_action=(
                "Resolve the SkuNotAvailable error for P1v3 in eastus2 by checking SKU "
                "availability and identifying an alternative SKU or availability zone."
            ),
            remediation_steps=[
                "Run 'az appservice list-locations --sku P1v3' to check P1v3 availability in eastus2.",
                "If P1v3 is unavailable, try P2v3 or P1mv3 as alternative premium SKUs.",
                "Open an Azure support request to check if P1v3 capacity can be reserved in eastus2.",
                "As a temporary workaround, deploy to a paired region (centralus) with VNet peering.",
            ],
        ),
        tags=["data-cleanup", "arm_template", "iac_noise"],
        description="ARM/Bicep IaC template dump adds infrastructure-as-code noise to a deployment failure ticket.",
    )


def _dc132_csv_bulk_paste() -> EvalCase:
    """Bulk CSV rows pasted into a data import failure ticket."""
    csv_rows = (
        "order_id,customer_id,product_sku,quantity,unit_price,order_date,ship_date,status\n"
        "ORD-90001,CUST-4421,SKU-BK-7812,2,29.99,2026-04-01,2026-04-03,shipped\n"
        "ORD-90002,CUST-1190,SKU-EL-0034,1,549.00,2026-04-01,2026-04-04,shipped\n"
        "ORD-90003,CUST-8827,SKU-BK-7812,5,29.99,2026-04-01,,processing\n"
        "ORD-90004,CUST-3356,SKU-HW-1120,1,1299.00,2026-04-02,2026-04-03,shipped\n"
        "ORD-90005,CUST-7741,SKU-EL-0034,3,549.00,2026-04-02,,failed\n"
        "ORD-90006,CUST-2218,SKU-OF-4450,10,12.50,2026-04-02,2026-04-04,shipped\n"
        "ORD-90007,CUST-9903,SKU-BK-7812,1,29.99,2026-04-02,,failed\n"
        "ORD-90008,CUST-5564,SKU-HW-1120,2,1299.00,2026-04-03,,processing\n"
        "ORD-90009,CUST-1190,SKU-OF-4450,25,12.50,2026-04-03,2026-04-05,shipped\n"
        "ORD-90010,CUST-6632,SKU-EL-0034,1,549.00,2026-04-03,,failed\n"
        "ORD-90011,CUST-4421,SKU-HW-1120,1,1299.00,2026-04-03,,failed\n"
        "ORD-90012,CUST-8827,SKU-OF-4450,50,12.50,2026-04-04,,processing\n"
    )
    return EvalCase(
        ticket=EvalTicket(
            ticket_id="INC-DC-132",
            subject="Bulk order import failing — 4 out of 12 rows stuck in 'failed' status",
            description=(
                "We are running the weekly bulk order import into our fulfillment system and "
                "4 out of 12 rows are ending up in 'failed' status with no clear error message "
                "in the import log. The import job ID is IMPORT-2026-04-06-001.\n\n"
                "Here is the full CSV that was submitted for import:\n\n"
                f"{csv_rows}\n"
                "The failed rows are ORD-90005, ORD-90007, ORD-90010, and ORD-90011. I notice "
                "they all have empty ship_date fields, but so do the 'processing' rows (ORD-90003, "
                "ORD-90008, ORD-90012) which imported fine. So the empty ship_date alone isn't "
                "the issue.\n\n"
                "Looking more carefully, the failed rows seem to involve higher-value items "
                "(SKU-EL-0034 at $549 and SKU-HW-1120 at $1299). Could there be a value threshold "
                "validation that's rejecting them?\n\n"
                "We need these orders processed by end of business today to meet our SLA.\n\n"
                "— Lin Chen, Order Operations\nlin.chen@contoso.com"
            ),
            reporter=Reporter(
                name="Lin Chen",
                email="lin.chen@contoso.com",
                department="Order Operations",
            ),
            created_at="2026-04-06T14:20:00Z",
            channel=Channel.EMAIL,
        ),
        gold=GoldAnswer(
            ticket_id="INC-DC-132",
            category=Category.DATA_STORAGE,
            priority=Priority.P3,
            assigned_team=Team.DATA_PLATFORM,
            needs_escalation=False,
            missing_information=[MissingInfoField.ERROR_MESSAGE, MissingInfoField.APPLICATION_VERSION],
            next_best_action=(
                "Investigate why the bulk order import job IMPORT-2026-04-06-001 is marking "
                "high-value orders as failed — check for value-threshold validation rules."
            ),
            remediation_steps=[
                "Query the import job logs for IMPORT-2026-04-06-001 to extract the exact failure reason per row.",
                "Check if a recently added order-value validation rule is rejecting items above a dollar threshold.",
                "Manually re-import the 4 failed rows with verbose logging enabled to capture the root cause.",
                "If a threshold rule is confirmed, adjust it or add an override for bulk imports.",
            ],
        ),
        tags=["data-cleanup", "csv_flood", "bulk_data_paste"],
        description="Bulk CSV rows pasted inline flood a data import failure ticket.",
    )


def _dc133_codepage_mojibake() -> EvalCase:
    """CP-1252/UTF-8 mojibake corruption in a printer configuration ticket."""
    return EvalCase(
        ticket=EvalTicket(
            ticket_id="INC-DC-133",
            subject="Printer outputting garbled characters on all documents",
            description=(
                "Our department printer (HP LaserJet Pro MFP 4101fdw) has been printing garbled "
                "text on every document since Monday morning. Here\u00e2\u0080\u0099s what a "
                "typical page looks like \u00e2\u0080\u0094 the word \u00e2\u0080\u009cInvoice"
                "\u00e2\u0080\u009d prints as \u00e2\u0080\u009cInvoiÃ§Ã©\u00e2\u0080\u009d "
                "and accented characters like Ã©, Ã¨, and Ã¼ appear throughout.\n\n"
                "The issue affects all users printing from Windows, not just one machine. "
                "Printing from a Mac works fine, which is strange. We\u00e2\u0080\u0099ve tried:\n"
                "\u00e2\u0080\u00a2 Reinstalling the printer driver (v49.4.4578)\n"
                "\u00e2\u0080\u00a2 Changing the default character set in printer settings\n"
                "\u00e2\u0080\u00a2 Printing a test page from the printer\u00e2\u0080\u0099s "
                "own menu (this prints fine)\n"
                "\u00e2\u0080\u00a2 Using a different USB cable\n\n"
                "The test page from the printer itself is perfect, so the hardware seems fine. "
                "It\u00e2\u0080\u0099s only when printing from Windows that we get the mojibake. "
                "I suspect it\u00e2\u0080\u0099s a character encoding mismatch between the "
                "Windows print spooler and the printer\u00e2\u0080\u0099s PCL interpreter.\n\n"
                "This is affecting our entire Finance floor (about 30 people) who need to "
                "print invoices daily.\n\n"
                "\u00e2\u0080\u0094 Svetlana Novak, Finance\nsvetlana.novak@contoso.com"
            ),
            reporter=Reporter(
                name="Svetlana Novak",
                email="svetlana.novak@contoso.com",
                department="Finance",
            ),
            created_at="2026-04-07T08:45:00Z",
            channel=Channel.PHONE,
        ),
        gold=GoldAnswer(
            ticket_id="INC-DC-133",
            category=Category.HARDWARE,
            priority=Priority.P3,
            assigned_team=Team.ENDPOINT,
            needs_escalation=False,
            missing_information=[MissingInfoField.ENVIRONMENT_DETAILS, MissingInfoField.DEVICE_INFO],
            next_best_action=(
                "Investigate the character encoding mismatch between Windows print spooler "
                "and the HP LaserJet Pro MFP 4101fdw PCL interpreter causing mojibake output."
            ),
            remediation_steps=[
                "Check the Windows print spooler language setting — switch from PCL to PostScript driver if available.",
                "Verify the printer firmware version and update to the latest release from HP.",
                "Check if a recent Windows Update changed the default codepage or font substitution table.",
                "Test printing with the Universal Print Driver (UPD) as an alternative.",
            ],
        ),
        tags=["data-cleanup", "codepage_mojibake", "encoding_corruption"],
        description="CP-1252/UTF-8 mojibake corruption scattered throughout a printer issue ticket.",
    )


def _dc134_recursive_email_forward() -> EvalCase:
    """10+ levels of email forwarding headers creating a deeply nested forward chain."""
    forward_chain = (
        "---------- Forwarded message ----------\n"
        "From: helpdesk@contoso.com\nTo: l2.support@contoso.com\n"
        "Date: Mon, 7 Apr 2026 07:00:00 -0400\nSubject: FW: FW: FW: Outlook calendar sync broken\n\n"
        "---------- Forwarded message ----------\n"
        "From: l2.support@contoso.com\nTo: exchange.team@contoso.com\n"
        "Date: Mon, 7 Apr 2026 07:15:00 -0400\nSubject: FW: FW: FW: FW: Outlook calendar sync broken\n\n"
        "---------- Forwarded message ----------\n"
        "From: exchange.team@contoso.com\nTo: m365.ops@contoso.com\n"
        "Date: Mon, 7 Apr 2026 07:32:00 -0400\nSubject: FW: FW: FW: FW: FW: Outlook calendar sync broken\n\n"
        "---------- Forwarded message ----------\n"
        "From: m365.ops@contoso.com\nTo: vendor.escalation@contoso.com\n"
        "Date: Mon, 7 Apr 2026 08:01:00 -0400\nSubject: FW: FW: FW: FW: FW: FW: Outlook calendar sync broken\n\n"
        "---------- Forwarded message ----------\n"
        "From: vendor.escalation@contoso.com\nTo: m365.ops@contoso.com\n"
        "Date: Mon, 7 Apr 2026 09:45:00 -0400\nSubject: RE: FW: FW: FW: FW: FW: FW: Outlook calendar sync broken\n"
        "Body: We cannot reproduce. Please collect Outlook ETL traces.\n\n"
        "---------- Forwarded message ----------\n"
        "From: m365.ops@contoso.com\nTo: exchange.team@contoso.com\n"
        "Date: Mon, 7 Apr 2026 10:10:00 -0400\n"
        "Subject: FW: RE: FW: FW: FW: FW: FW: FW: Outlook calendar sync broken\n\n"
        "---------- Forwarded message ----------\n"
        "From: exchange.team@contoso.com\nTo: l2.support@contoso.com\n"
        "Date: Mon, 7 Apr 2026 10:30:00 -0400\n"
        "Subject: FW: FW: RE: FW: FW: FW: FW: FW: FW: Outlook calendar sync broken\n\n"
        "---------- Forwarded message ----------\n"
        "From: l2.support@contoso.com\nTo: helpdesk@contoso.com\n"
        "Date: Mon, 7 Apr 2026 10:45:00 -0400\n"
        "Subject: FW: FW: FW: RE: FW: FW: FW: FW: FW: FW: Outlook calendar sync broken\n\n"
        "---------- Forwarded message ----------\n"
        "From: helpdesk@contoso.com\nTo: enterprise.apps@contoso.com\n"
        "Date: Mon, 7 Apr 2026 11:00:00 -0400\n"
        "Subject: FW: FW: FW: FW: RE: FW: FW: FW: FW: FW: FW: Outlook calendar sync broken\n"
        "Body: Reassigning to Enterprise Apps — the vendor says collect ETL traces.\n\n"
        "---------- Forwarded message ----------\n"
        "From: enterprise.apps@contoso.com\nTo: desktop.support@contoso.com\n"
        "Date: Mon, 7 Apr 2026 11:20:00 -0400\n"
        "Subject: FW: FW: FW: FW: FW: RE: FW: FW: FW: FW: FW: FW: Outlook calendar sync broken\n"
        "Body: Desktop support — please collect Outlook ETL traces from the user.\n"
    )
    return EvalCase(
        ticket=EvalTicket(
            ticket_id="INC-DC-134",
            subject="Outlook calendar sync broken — meetings not appearing on mobile",
            description=(
                "My Outlook calendar on my iPhone 15 Pro stopped syncing with my desktop "
                "Outlook (Microsoft 365 v2403, Build 17425.20176). New meetings created on "
                "the desktop don't appear on my phone, and meetings I accept on my phone "
                "don't show up on the desktop. This started last Thursday.\n\n"
                "I've tried removing and re-adding my Exchange account on the iPhone, and I've "
                "also tried resetting the Outlook mobile app data. Neither fixed the issue.\n\n"
                "This ticket has been bounced around a lot — here is the forwarding history:\n\n"
                f"{forward_chain}\n"
                "As you can see, the vendor says they can't reproduce and wants ETL traces. "
                "I just need someone to actually come to my desk and help me collect these "
                "traces so we can move forward.\n\n"
                "I'm missing meetings because of this and it's really disruptive.\n\n"
                "— Angela Park, Legal\nangela.park@contoso.com"
            ),
            reporter=Reporter(
                name="Angela Park",
                email="angela.park@contoso.com",
                department="Legal",
            ),
            created_at="2026-04-07T11:30:00Z",
            channel=Channel.EMAIL,
        ),
        gold=GoldAnswer(
            ticket_id="INC-DC-134",
            category=Category.SOFTWARE,
            priority=Priority.P3,
            assigned_team=Team.ENTERPRISE_APPS,
            needs_escalation=False,
            missing_information=[MissingInfoField.DEVICE_INFO, MissingInfoField.APPLICATION_VERSION],
            next_best_action=(
                "Collect Outlook ETL traces from the user's desktop as the vendor requested, "
                "and verify Exchange ActiveSync profile on the iPhone."
            ),
            remediation_steps=[
                "Schedule a desk visit to collect Outlook ETL traces during a calendar sync attempt.",
                "Verify the Exchange ActiveSync partnership for the user's iPhone in the Exchange admin center.",
                "Check if the user's mailbox has hit the ActiveSync device partnership limit.",
                "Test calendar sync with the Outlook mobile app instead of the native iOS Mail app.",
            ],
        ),
        tags=["data-cleanup", "recursive_forward", "deep_email_chain"],
        description="10+ levels of email forward headers create a deeply nested chain of noise.",
    )


def _dc135_pii_noise() -> EvalCase:
    """PII (names, SSNs, phone numbers, addresses) scattered throughout a network ticket."""
    return EvalCase(
        ticket=EvalTicket(
            ticket_id="INC-DC-135",
            subject="WiFi keeps dropping in conference rooms on 3rd floor",
            description=(
                "The WiFi in our 3rd-floor conference rooms (Rooms 301, 302, and 305) keeps "
                "dropping during meetings. It affects all devices — laptops, phones, tablets. "
                "The drops happen every 10-15 minutes and last about 30 seconds each time.\n\n"
                "I gathered some info from affected users so you can follow up:\n\n"
                "User 1: Maria Garcia, Employee ID: EMP-44291, Phone: (555) 012-3456, "
                "SSN: 123-45-6789, Badge #: B-10042, Home: 742 Evergreen Terrace, Springfield, "
                "IL 62704\n"
                "User 2: Robert Kim, Employee ID: EMP-38812, Phone: (555) 098-7654, "
                "SSN: 987-65-4321, Badge #: B-10187, Home: 1600 Pennsylvania Ave NW, "
                "Washington, DC 20500\n"
                "User 3: Fatima Al-Hassan, Employee ID: EMP-51003, Phone: (555) 234-5678, "
                "SSN: 456-78-9012, Badge #: B-10301, Home: 221B Baker Street, London, "
                "NW1 6XE\n"
                "User 4: James O'Brien, Employee ID: EMP-29947, Phone: (555) 345-6789, "
                "SSN: 234-56-7890, Badge #: B-10455, Credit Card: 4111-1111-1111-1111, "
                "Home: 350 Fifth Avenue, New York, NY 10118\n\n"
                "All four of these people were in Room 302 during the 10 AM standup when the "
                "WiFi dropped twice. The access point in that room is AP-3F-02 and it's "
                "mounted above the ceiling tiles.\n\n"
                "We have an important client presentation in Room 305 tomorrow at 2 PM and "
                "we absolutely cannot have WiFi drops during it.\n\n"
                "— Nathan Brooks, Facilities\nnathan.brooks@contoso.com"
            ),
            reporter=Reporter(
                name="Nathan Brooks",
                email="nathan.brooks@contoso.com",
                department="Facilities",
            ),
            created_at="2026-04-07T14:00:00Z",
            channel=Channel.PHONE,
        ),
        gold=GoldAnswer(
            ticket_id="INC-DC-135",
            category=Category.NETWORK,
            priority=Priority.P2,
            assigned_team=Team.NETWORK_OPS,
            needs_escalation=False,
            missing_information=[MissingInfoField.NETWORK_LOCATION, MissingInfoField.ERROR_MESSAGE],
            next_best_action=(
                "Investigate recurring WiFi drops on 3rd-floor access point AP-3F-02 and "
                "ensure stable coverage before tomorrow's client presentation."
            ),
            remediation_steps=[
                "Check AP-3F-02 logs for disassociation events and channel utilization during drop windows.",
                "Run a wireless site survey on the 3rd floor to check for co-channel interference.",
                "Verify the AP firmware is up to date and check for known bugs in the current version.",
                "If the AP is faulty, deploy a temporary replacement AP before the 2 PM presentation.",
            ],
        ),
        tags=["data-cleanup", "pii_noise", "sensitive_data"],
        description="PII (SSNs, phone numbers, addresses) scattered in a WiFi issue ticket.",
    )


def _dc136_csv_injection() -> EvalCase:
    """CSV injection patterns (=CMD, =HYPERLINK, @SUM) embedded in a data import/export ticket."""
    return EvalCase(
        ticket=EvalTicket(
            ticket_id="INC-DC-136",
            subject="Data import failing with special characters in CSV uploads",
            description=(
                "We've been getting failures when importing customer data from CSV files "
                "into the DataHub pipeline. The import job runs nightly at 02:00 UTC and "
                "has failed for the last three nights.\n\n"
                "Here are sample rows from the failing CSV that I extracted from the staging "
                "table — I think these might be causing issues:\n\n"
                'Row 42: "Acme Corp","=CMD|\'/C calc\'!A0","Northeast","2026-03-15"\n'
                'Row 108: "Globex Inc","=HYPERLINK(""http://evil.com"",""Click here"")","West","2026-03-16"\n'
                'Row 203: "Initech","@SUM(1+1)*cmd|\'/C calc\'!A0","Southeast","2026-03-17"\n'
                'Row 317: "Umbrella LLC","+cmd|\'/C powershell\'!A0","Central","2026-03-18"\n'
                'Row 445: "Soylent Corp","=1+1]|*/cmd\'!A0","Northwest","2026-03-19"\n\n'
                "The import log shows 'InvalidCharacterException' on these rows but the "
                "job terminates instead of skipping them. Previous imports (before March 12) "
                "worked fine. We have about 15,000 rows total per nightly batch.\n\n"
                "Can someone look into why the pipeline is not sanitizing these inputs and "
                "whether we need to add a pre-processing step?\n\n"
                "— Deepak Patel, Data Engineering\ndeepak.patel@contoso.com"
            ),
            reporter=Reporter(
                name="Deepak Patel",
                email="deepak.patel@contoso.com",
                department="Data Engineering",
            ),
            created_at="2026-04-08T09:15:00Z",
            channel=Channel.EMAIL,
        ),
        gold=GoldAnswer(
            ticket_id="INC-DC-136",
            category=Category.DATA_STORAGE,
            priority=Priority.P2,
            assigned_team=Team.DATA_PLATFORM,
            needs_escalation=False,
            missing_information=[MissingInfoField.ERROR_MESSAGE, MissingInfoField.ENVIRONMENT_DETAILS],
            next_best_action=(
                "Investigate the CSV import pipeline's input sanitization and add a "
                "pre-processing step to neutralize formula injection patterns before "
                "loading data into the staging table."
            ),
            remediation_steps=[
                (
                    "Review the nightly import job logs for the exact"
                    " InvalidCharacterException stack traces and affected row counts."
                ),
                (
                    "Add a CSV sanitization step that prefixes cells starting"
                    " with =, +, -, or @ with a single quote to neutralize"
                    " formula injection."
                ),
                (
                    "Configure the import pipeline to skip or quarantine"
                    " malformed rows instead of terminating the entire batch."
                ),
                ("Re-run the failed imports for the last three nights after applying the sanitization fix."),
            ],
        ),
        tags=["data-cleanup", "csv_injection"],
        description="CSV injection patterns (=CMD, =HYPERLINK) embedded in a data import/export ticket.",
    )


def _dc137_gpg_signed() -> EvalCase:
    """GPG/PGP signed email with armor blocks wrapping a hardware docking station issue."""
    return EvalCase(
        ticket=EvalTicket(
            ticket_id="INC-DC-137",
            subject="Docking station not detecting external monitors after firmware update",
            description=(
                "-----BEGIN PGP SIGNED MESSAGE-----\n"
                "Hash: SHA256\n\n"
                "Hi IT Support,\n\n"
                "After the firmware update pushed last Friday (v4.2.1 → v4.3.0) to our "
                "Lenovo ThinkPad USB-C Dock Gen 2 stations, my two external monitors "
                "(Dell U2722D, connected via DisplayPort) are no longer being detected. "
                "The dock powers the laptop and USB peripherals work fine — it's only the "
                "display outputs that are dead.\n\n"
                "I have tried:\n"
                "- Unplugging and reconnecting the dock\n"
                "- Swapping DisplayPort cables\n"
                "- Connecting monitors directly to the laptop (works fine)\n"
                "- Rolling back the Lenovo Dock Manager to the previous version\n"
                "- Checking Device Manager — the dock shows 'This device is working properly'\n\n"
                "Three other people on my team (Carlos, Wei, and Priya) are having the exact "
                "same issue with the same dock model. We all got the firmware update at the "
                "same time.\n\n"
                "This is blocking our design review work since we need dual-monitor setups "
                "for CAD applications.\n\n"
                "Thanks,\nHelena Voss\nEngineering — Mechanical Design\n"
                "helena.voss@contoso.com\n\n"
                "-----BEGIN PGP SIGNATURE-----\n\n"
                "iQIzBAEBCAAdFiEEYd7WkljJhG4xQpZ1rT3JhVm8mMIFAmYDqV0ACgkQrT3JhVm8\n"
                "mMJ5kA/+N7K3mVZ5Q2rP8wYjXb5mCdKx5xA1v3qLp2rF9d6Kz7j8nB3W4Xx6mD1\n"
                "P5sA8gR2kYt0hWnJ3L9xQpR4mE7vB2dF6yH8cN5wT1jK0aS3uI9fG4hL7xQ2pM0\n"
                "kD3nR5vA1bC8eW6yT4uI9oP2lK7jH0gF5dS3aZ8xM1nB4vC9qE6wR2tY7uJ0iL3\n"
                "=dK4m\n"
                "-----END PGP SIGNATURE-----"
            ),
            reporter=Reporter(
                name="Helena Voss",
                email="helena.voss@contoso.com",
                department="Engineering",
            ),
            created_at="2026-04-08T10:30:00Z",
            channel=Channel.EMAIL,
        ),
        gold=GoldAnswer(
            ticket_id="INC-DC-137",
            category=Category.HARDWARE,
            priority=Priority.P3,
            assigned_team=Team.ENDPOINT,
            needs_escalation=False,
            missing_information=[MissingInfoField.DEVICE_INFO, MissingInfoField.ENVIRONMENT_DETAILS],
            next_best_action=(
                "Investigate the dock firmware update v4.3.0 for display output regressions "
                "and coordinate a rollback to v4.2.1 for affected ThinkPad USB-C Dock Gen 2 units."
            ),
            remediation_steps=[
                (
                    "Check the Lenovo support site for known issues with"
                    " ThinkPad USB-C Dock Gen 2 firmware v4.3.0 and"
                    " DisplayPort output."
                ),
                (
                    "Attempt a firmware rollback to v4.2.1 on one affected"
                    " dock to confirm it resolves the display detection issue."
                ),
                (
                    "If rollback resolves the issue, coordinate a batch"
                    " rollback for all affected docks and pause the v4.3.0"
                    " deployment."
                ),
                (
                    "Open a case with Lenovo enterprise support if the issue"
                    " persists after rollback, providing firmware version and"
                    " monitor model details."
                ),
            ],
        ),
        tags=["data-cleanup", "gpg_signed"],
        description="GPG/PGP signed email with armor blocks wrapping a hardware docking station issue.",
    )


def _dc138_zalgo_combining() -> EvalCase:
    """Zalgo text with combining Unicode diacritics in a software crash ticket."""
    return EvalCase(
        ticket=EvalTicket(
            ticket_id="INC-DC-138",
            subject="Application crashes when opening reports module",
            description=(
                "H\u0337\u0322\u0327\u0308\u030c\u0301"
                "e\u0336\u0323\u032e\u0301\u030e"
                "l\u0338\u0324\u0330\u030b\u0302"
                "p\u0335\u0325\u032d\u0308\u030c "
                "\u2014 the R\u0336\u0323\u032e\u0301"
                "e\u0337\u0324\u0330\u0308"
                "p\u0335\u0325\u032d\u030c"
                "o\u0338\u0322\u0327\u030b"
                "r\u0336\u0323\u032e\u0302"
                "t\u0337\u0324\u0330\u0301s "
                "module in our internal CRM application (v8.4.2) is "
                "crashing every time I try to open it. The "
                "a\u0336\u0323\u032e\u030c"
                "p\u0337\u0324\u0330\u0308"
                "p\u0335\u0325\u032d\u0302"
                "l\u0338\u0322\u0327\u030b"
                "i\u0336\u0323\u032e\u0301"
                "c\u0337\u0324\u0330\u030ca"
                "\u0335\u0325\u032d\u0308"
                "t\u0338\u0322\u0327\u030b"
                "i\u0336\u0323\u032e\u0302"
                "o\u0337\u0324\u0330\u030cn "
                "freezes for about 5 seconds, then shows a white "
                "screen and the "
                "p\u0335\u0325\u032d\u030c"
                "r\u0338\u0322\u0327\u030b"
                "o\u0336\u0323\u032e\u0302"
                "c\u0337\u0324\u0330\u0301"
                "e\u0335\u0325\u032d\u0308"
                "s\u0338\u0322\u0327\u030bs "
                "crashes with an unhandled NullReferenceException. "
                "I\u0336\u0323\u032e\u030c've attached the "
                "crash log below.\n\n"
                "System.NullReferenceException: Object reference not set "
                "to an instance of an object.\n"
                "   at CRM.Reports.ReportEngine.LoadModule()\n"
                "   at CRM.UI.MainWindow.OpenReports()\n\n"
                "This started after the v8.4.2 update was pushed last "
                "Friday. Version 8.4.1 worked fine.\n\n"
                "Thanks,\nMaria Fischer\nSales Operations\n"
                "maria.fischer@contoso.com"
            ),
            reporter=Reporter(
                name="Maria Fischer",
                email="maria.fischer@contoso.com",
                department="Sales Operations",
            ),
            created_at="2026-04-08T10:30:00Z",
            channel=Channel.PORTAL,
        ),
        gold=GoldAnswer(
            ticket_id="INC-DC-138",
            category=Category.SOFTWARE,
            priority=Priority.P2,
            assigned_team=Team.ENTERPRISE_APPS,
            needs_escalation=False,
            missing_information=[
                MissingInfoField.ENVIRONMENT_DETAILS,
            ],
            next_best_action=(
                "Investigate the NullReferenceException in the CRM Reports "
                "module introduced in v8.4.2 and coordinate a hotfix or "
                "rollback to v8.4.1."
            ),
            remediation_steps=[
                "Reproduce the crash on a test instance running CRM v8.4.2.",
                "Review the v8.4.2 release notes and change log for the Reports module.",
                "Collect full crash dumps from affected users for developer analysis.",
                "If a hotfix is not immediately available, roll back to v8.4.1.",
            ],
        ),
        tags=["data-cleanup", "zalgo_combining"],
        description=("Zalgo text with combining Unicode diacritics scattered throughout a software crash ticket."),
    )


def _dc139_nested_json() -> EvalCase:
    """Deeply nested JSON (50+ levels) pasted in a database performance ticket."""
    nested = '{"level_1":' * 55 + '{"value":"timeout"}' + "}" * 55
    return EvalCase(
        ticket=EvalTicket(
            ticket_id="INC-DC-139",
            subject="Database queries timing out on nested document store",
            description=(
                "Our MongoDB document store has been returning timeouts on queries "
                "against the analytics collection. The documents in that collection "
                "are deeply nested JSON structures that were migrated from a legacy "
                "XML-based system. Here is a sample document that causes the timeout "
                "when we try to run an aggregation pipeline:\n\n"
                f"{nested}\n\n"
                "The query that fails is a simple $match on the innermost 'value' "
                "field. It worked fine until the collection grew past 2M documents "
                "last week. We have an index on 'level_1.level_2.level_3' but not "
                "deeper. The MongoDB profiler shows the query is doing a COLLSCAN.\n\n"
                "We need guidance on whether to restructure the documents or add "
                "wildcard indexes. This is blocking our quarterly analytics pipeline "
                "which is due by end of week.\n\n"
                "— Rajesh Patel, Data Engineering\nrajesh.patel@contoso.com"
            ),
            reporter=Reporter(
                name="Rajesh Patel",
                email="rajesh.patel@contoso.com",
                department="Data Engineering",
            ),
            created_at="2026-04-08T09:15:00Z",
            channel=Channel.PORTAL,
        ),
        gold=GoldAnswer(
            ticket_id="INC-DC-139",
            category=Category.DATA_STORAGE,
            priority=Priority.P2,
            assigned_team=Team.DATA_PLATFORM,
            needs_escalation=False,
            missing_information=[MissingInfoField.ENVIRONMENT_DETAILS, MissingInfoField.ERROR_MESSAGE],
            next_best_action=(
                "Investigate MongoDB query timeouts caused by deeply nested documents "
                "and missing indexes on the analytics collection."
            ),
            remediation_steps=[
                "Review the MongoDB profiler output for the failing aggregation pipeline query.",
                "Evaluate adding wildcard indexes ($**) on the analytics collection for deep paths.",
                "Consider flattening the deeply nested document structure during a re-migration.",
                "Increase the query timeout threshold temporarily to unblock the quarterly analytics pipeline.",
            ],
        ),
        tags=["data-cleanup", "deeply_nested_json"],
        description="Deeply nested JSON (50+ levels) pasted inline in a database performance ticket.",
    )


def _dc140_sql_output() -> EvalCase:
    """Raw SQL query output with ASCII table formatting in a data corruption ticket."""
    return EvalCase(
        ticket=EvalTicket(
            ticket_id="INC-DC-140",
            subject="Customer records showing duplicate entries after ETL run",
            description=(
                "After last night's ETL pipeline run, we're seeing duplicate customer "
                "records in the CustomerMaster table. I ran a query to identify the "
                "duplicates and here is the output:\n\n"
                "+------------+----------------------+------------------+-------+\n"
                "| cust_id    | name                 | email            | count |\n"
                "+------------+----------------------+------------------+-------+\n"
                "| C-100234   | Acme Corp            | info@acme.com    |     3 |\n"
                "| C-100235   | Globex Inc           | hello@globex.com |     2 |\n"
                "| C-100412   | Initech LLC          | sup@initech.com  |     4 |\n"
                "| C-100567   | Umbrella Corp        | uc@umbrella.com  |     2 |\n"
                "| C-100890   | Wayne Enterprises    | info@wayne.com   |     3 |\n"
                "| C-101023   | Stark Industries     | si@stark.com     |     2 |\n"
                "| C-101456   | Cyberdyne Systems    | cs@cyberdyne.com |     5 |\n"
                "| C-101789   | Oscorp               | osc@oscorp.com   |     2 |\n"
                "+------------+----------------------+------------------+-------+\n"
                "8 rows in set (0.42 sec)\n\n"
                "SELECT cust_id, name, email, COUNT(*) as count\n"
                "FROM CustomerMaster\n"
                "GROUP BY cust_id, name, email\n"
                "HAVING COUNT(*) > 1\n"
                "ORDER BY count DESC;\n\n"
                "The ETL job ID is ETL-2026-04-07-NIGHTLY-003 and it ran at 02:00 UTC. "
                "The source was the Salesforce CRM sync connector. I suspect the upsert "
                "logic is broken — it's inserting instead of updating when the source "
                "record has a changed email address.\n\n"
                "This is impacting downstream reporting and billing.\n\n"
                "— David Kim, Business Intelligence\ndavid.kim@contoso.com"
            ),
            reporter=Reporter(
                name="David Kim",
                email="david.kim@contoso.com",
                department="Business Intelligence",
            ),
            created_at="2026-04-08T07:30:00Z",
            channel=Channel.EMAIL,
        ),
        gold=GoldAnswer(
            ticket_id="INC-DC-140",
            category=Category.DATA_STORAGE,
            priority=Priority.P2,
            assigned_team=Team.DATA_PLATFORM,
            needs_escalation=False,
            missing_information=[MissingInfoField.CONFIGURATION_DETAILS],
            next_best_action=(
                "Investigate the ETL pipeline upsert logic for the Salesforce CRM sync "
                "connector that is creating duplicate customer records."
            ),
            remediation_steps=[
                "Review ETL job ETL-2026-04-07-NIGHTLY-003 logs for error conditions during the upsert phase.",
                "Examine the Salesforce CRM sync connector configuration for merge key definitions.",
                "De-duplicate the affected CustomerMaster records using the original cust_id as the primary key.",
                "Add a unique constraint or pre-run validation to prevent future duplicate inserts.",
            ],
        ),
        tags=["data-cleanup", "sql_output"],
        description="Raw SQL query output with ASCII table formatting pasted in a data corruption ticket.",
    )


def _dc141_smime_signature() -> EvalCase:
    """S/MIME digital signature block wrapping an SSO login failure ticket."""
    return EvalCase(
        ticket=EvalTicket(
            ticket_id="INC-DC-141",
            subject="SSO login failing for Azure AD-federated applications",
            description=(
                'Content-Type: multipart/signed; protocol="application/pkcs7-signature"; '
                'micalg=sha-256; boundary="----=_Part_SMIME_001"\n\n'
                "------=_Part_SMIME_001\n"
                "Content-Type: text/plain; charset=utf-8\n\n"
                "Hi Identity team,\n\n"
                "Since this morning, all users in the London office are unable to log in "
                "to any Azure AD-federated application via SSO. The SAML assertion from "
                "our ADFS server (adfs.contoso.com) is being rejected by Azure AD with "
                "error AADSTS50011: The reply URL specified in the request does not match "
                "the reply URLs configured for the application.\n\n"
                "This is affecting about 200 users across Outlook Web, SharePoint Online, "
                "and our internal HR portal. Direct Azure AD login with username/password "
                "still works, so it's specifically the ADFS federation that's broken.\n\n"
                "We suspect someone changed the reply URL in the Azure AD app registration "
                "during yesterday's maintenance window.\n\n"
                "— Carlos Mendez, IT Security\ncarlos.mendez@contoso.com\n\n"
                "------=_Part_SMIME_001\n"
                "Content-Type: application/pkcs7-signature; name=smime.p7s\n"
                "Content-Transfer-Encoding: base64\n"
                "Content-Disposition: attachment; filename=smime.p7s\n\n"
                "MIIGXgYJKoZIhvcNAQcCoIIGTzCCBksCAQExDzANBglghkgBZQMEAgEFADALBgkq\n"
                "hkiG9w0BBwGgggPPMIIDyzCCArOgAwIBAgIUQ4r7sE2hNjRkYzM1OTdhZGI0ZDQw\n"
                "DQYJKoZIhvcNAQELBQAwgZAxCzAJBgNVBAYTAlVTMQswCQYDVQQIDAJOWTERMA8G\n"
                "A1UEBwwITmV3IFlvcmsxEDAOBgNVBAoMB0NvbnRvc28xDDAKBgNVBAsMA0lUMRgw\n"
                "FgYDVQQDDA9jYXJsb3MubWVuZGV6MScwJQYJKoZIhvcNAQkBFhhjYXJsb3MubWVu\n"
                "ZGV6QGNvbnRvc28uY29tMB4XDTI2MDQwNzAwMDAwMFoXDTI3MDQwNzAwMDAwMFow\n"
                "gZAxCzAJBgNVBAYTAlVTMQswCQYDVQQIDAJOWTERMA8GA1UEBwwITmV3IFlvcmsx\n"
                "------=_Part_SMIME_001--\n"
            ),
            reporter=Reporter(
                name="Carlos Mendez",
                email="carlos.mendez@contoso.com",
                department="IT Security",
            ),
            created_at="2026-04-08T08:00:00Z",
            channel=Channel.EMAIL,
        ),
        gold=GoldAnswer(
            ticket_id="INC-DC-141",
            category=Category.ACCESS_AUTH,
            priority=Priority.P2,
            assigned_team=Team.IAM,
            needs_escalation=False,
            missing_information=[MissingInfoField.CONFIGURATION_DETAILS, MissingInfoField.AFFECTED_USERS],
            next_best_action=(
                "Investigate the AADSTS50011 error by comparing the ADFS reply URL configuration "
                "with the Azure AD app registration reply URLs for all affected applications."
            ),
            remediation_steps=[
                "Check the Azure AD app registration reply URLs for changes made during yesterday's maintenance.",
                "Compare the SAML assertion reply URL from ADFS with the Azure AD configured reply URLs.",
                "Restore the correct reply URL in Azure AD if it was inadvertently changed.",
                "Verify SSO login works for London office users after the fix is applied.",
            ],
        ),
        tags=["data-cleanup", "smime_signature"],
        description="S/MIME digital signature block (PKCS7) wrapping a legitimate SSO failure ticket.",
    )


def _dc142_near_empty_iphone() -> EvalCase:
    """Near-empty body — real issue is only in the subject line."""
    return EvalCase(
        ticket=EvalTicket(
            ticket_id="INC-DC-142",
            subject="Excel crashing on pivot table refresh — affects entire Finance team",
            description=("\n\nSent from my iPhone"),
            reporter=Reporter(
                name="Lauren Hughes",
                email="lauren.hughes@contoso.com",
                department="Finance",
            ),
            created_at="2026-04-08T12:45:00Z",
            channel=Channel.EMAIL,
        ),
        gold=GoldAnswer(
            ticket_id="INC-DC-142",
            category=Category.SOFTWARE,
            priority=Priority.P3,
            assigned_team=Team.ENTERPRISE_APPS,
            needs_escalation=False,
            missing_information=[
                MissingInfoField.ERROR_MESSAGE,
                MissingInfoField.STEPS_TO_REPRODUCE,
                MissingInfoField.APPLICATION_VERSION,
                MissingInfoField.ENVIRONMENT_DETAILS,
            ],
            next_best_action=(
                "Follow up with the reporter to gather details about the Excel pivot table "
                "crash — version, steps to reproduce, and how many users are affected."
            ),
            remediation_steps=[
                "Contact Lauren Hughes to obtain the Excel version and specific workbook details.",
                "Request crash dump or event log entries from an affected machine.",
                "Check if a recent Office update correlates with the onset of the crashes.",
                "Test pivot table refresh in a controlled environment with the same data source.",
            ],
        ),
        tags=["data-cleanup", "near_empty_body"],
        description="Near-empty email body ('Sent from my iPhone') with the actual issue only in the subject.",
    )


def _dc143_jira_notification() -> EvalCase:
    """JIRA notification with full transition history wrapping a real software bug."""
    return EvalCase(
        ticket=EvalTicket(
            ticket_id="INC-DC-143",
            subject="JIRA notification: CRM-4521 Report export produces corrupt CSV files",
            description=(
                "This message was sent by Atlassian Jira (v9.12.4#9120004)\n\n"
                "Issue: CRM-4521\n"
                "Type: Bug\n"
                "Priority: Major\n"
                "Reporter: Samuel Torres\n"
                "Assignee: Unassigned\n"
                "Created: 2026-04-07T14:30:00+0000\n"
                "Updated: 2026-04-08T09:15:00+0000\n\n"
                "--- Transition History ---\n"
                "2026-04-07 14:30 | Open          → In Progress   | Samuel Torres\n"
                "2026-04-07 15:00 | In Progress   → Blocked       | Samuel Torres\n"
                "     Reason: Waiting on DBA team for schema access\n"
                "2026-04-07 16:45 | Blocked       → In Progress   | Samuel Torres\n"
                "2026-04-07 17:30 | In Progress   → Code Review   | Samuel Torres\n"
                "2026-04-08 08:00 | Code Review   → Reopened      | QA Bot\n"
                "     Reason: Failed regression test suite — 3 of 47 tests failed\n"
                "2026-04-08 08:30 | Reopened      → In Progress   | Samuel Torres\n"
                "2026-04-08 09:00 | In Progress   → Blocked       | Samuel Torres\n"
                "     Reason: Escalating to IT — production instance needs config change\n"
                "2026-04-08 09:15 | Blocked       → Open          | System\n"
                "     Reason: Auto-reassigned — assignee unavailable\n\n"
                "--- Description ---\n"
                "When exporting the monthly sales report from the CRM (Reports > Export > CSV), "
                "the generated CSV file is corrupt. The headers are duplicated on every 50th row, "
                "numeric columns contain stray quotation marks, and date columns use inconsistent "
                "formats (some ISO 8601, some MM/DD/YYYY). This started after the v8.4.2 patch "
                "deployed on Friday.\n\n"
                "Steps to reproduce:\n"
                "1. Navigate to Reports > Monthly Sales Summary\n"
                "2. Click Export > CSV\n"
                "3. Open the downloaded file in a text editor\n"
                "4. Observe corrupt rows at lines 50, 100, 150, ...\n\n"
                "The production CRM instance needs a configuration change to enable debug logging "
                "for the export module. This requires IT involvement.\n\n"
                "— Samuel Torres, Sales Operations\nsamuel.torres@contoso.com\n\n"
                "---\n"
                "You are receiving this email because you are subscribed to CRM-4521.\n"
                "Manage notifications: https://jira.contoso.com/secure/ViewSubscriptions.jspa\n"
                "Atlassian Jira | Contoso Instance | jira.contoso.com\n"
            ),
            reporter=Reporter(
                name="Samuel Torres",
                email="samuel.torres@contoso.com",
                department="Sales Operations",
            ),
            created_at="2026-04-08T09:20:00Z",
            channel=Channel.EMAIL,
        ),
        gold=GoldAnswer(
            ticket_id="INC-DC-143",
            category=Category.SOFTWARE,
            priority=Priority.P3,
            assigned_team=Team.ENTERPRISE_APPS,
            needs_escalation=False,
            missing_information=[MissingInfoField.APPLICATION_VERSION, MissingInfoField.ENVIRONMENT_DETAILS],
            next_best_action=(
                "Enable debug logging on the CRM export module and investigate the CSV "
                "corruption introduced in the v8.4.2 patch."
            ),
            remediation_steps=[
                "Enable debug logging on the CRM production instance for the report export module.",
                "Reproduce the corrupt CSV export and capture debug output.",
                "Compare the export module code between v8.4.1 and v8.4.2 for regression.",
                "Deploy a hotfix or roll back the export module to v8.4.1 if root cause is confirmed.",
            ],
        ),
        tags=["data-cleanup", "jira_notification"],
        description="JIRA notification email with full transition history wrapping a real CSV export bug.",
    )


def _dc144_registry_export() -> EvalCase:
    """Windows registry export (.reg) pasted for a software installation issue."""
    return EvalCase(
        ticket=EvalTicket(
            ticket_id="INC-DC-144",
            subject="AutoCAD 2026 fails to launch after installation — registry error",
            description=(
                "AutoCAD 2026 was installed yesterday via SCCM but refuses to launch. It shows "
                "error: 'License checkout failed. Error 20: Cannot find license file.' I exported "
                "the registry keys related to AutoCAD to help diagnose:\n\n"
                "Windows Registry Editor Version 5.00\n\n"
                "[HKEY_LOCAL_MACHINE\\SOFTWARE\\Autodesk\\AutoCAD\\R24.2\\ACAD-7001:409]\n"
                '"ProductName"="AutoCAD 2026"\n'
                '"Release"="24.2.55.0"\n'
                '"InstallPath"="C:\\\\Program Files\\\\Autodesk\\\\AutoCAD 2026\\\\"\n'
                '"LicensePath"=""\n'
                '"SerialNumber"="XXX-XXXXXXXX"\n'
                '"ProductKey"="001N2"\n\n'
                "[HKEY_LOCAL_MACHINE\\SOFTWARE\\Autodesk\\AutoCAD\\R24.2\\ACAD-7001:409\\FlexLM]\n"
                '"AdskFlexSrv"="@lic-server-01.contoso.com"\n'
                '"AdskFlexTimeout"=dword:00000078\n'
                '"AdskFlexDebug"=dword:00000001\n\n'
                "[HKEY_LOCAL_MACHINE\\SOFTWARE\\FLEXlm License Manager\\Autodesk]\n"
                '"LM_LICENSE_FILE"="@lic-server-01.contoso.com"\n'
                '"ADSKFLEX_LICENSE_FILE"=""\n\n'
                "[HKEY_CURRENT_USER\\SOFTWARE\\Autodesk\\AutoCAD\\R24.2\\Profiles\\Default]\n"
                '"LicenseType"="network"\n'
                '"ServerHost"="lic-server-01.contoso.com"\n'
                '"ServerPort"="27000"\n\n'
                "As you can see, the ADSKFLEX_LICENSE_FILE key is empty and the LicensePath "
                "is also blank. I think the SCCM deployment script didn't set these correctly. "
                "This is affecting 15 engineers in the CAD team who need AutoCAD for a project "
                "deadline on Friday.\n\n"
                "— Frank Barker, Engineering\nfrank.barker@contoso.com"
            ),
            reporter=Reporter(
                name="Frank Barker",
                email="frank.barker@contoso.com",
                department="Engineering",
            ),
            created_at="2026-04-08T08:20:00Z",
            channel=Channel.PORTAL,
        ),
        gold=GoldAnswer(
            ticket_id="INC-DC-144",
            category=Category.SOFTWARE,
            priority=Priority.P2,
            assigned_team=Team.ENDPOINT,
            needs_escalation=False,
            missing_information=[MissingInfoField.CONFIGURATION_DETAILS],
            next_best_action=(
                "Fix the SCCM deployment script to correctly populate the AutoCAD license "
                "registry keys (ADSKFLEX_LICENSE_FILE and LicensePath)."
            ),
            remediation_steps=[
                "Set the ADSKFLEX_LICENSE_FILE registry value to @lic-server-01.contoso.com.",
                "Verify network connectivity from affected workstations to lic-server-01.contoso.com:27000.",
                "Update the SCCM deployment task sequence to include the license registry keys.",
                "Test AutoCAD launch on one machine before redeploying to all 15 engineers.",
            ],
        ),
        tags=["data-cleanup", "registry_export"],
        description="Windows registry export (.reg) pasted inline for a software license issue.",
    )


def _dc145_deep_traceback() -> EvalCase:
    """Deep Python traceback (50+ frames) pasted for a production application crash."""
    frames = ""
    modules = [
        "middleware.auth",
        "middleware.logging",
        "middleware.cors",
        "middleware.rate_limit",
        "routes.api_v2",
        "controllers.report",
        "services.report_engine",
        "services.data_fetcher",
        "adapters.sql_adapter",
        "adapters.cache_layer",
        "core.query_builder",
        "core.optimizer",
        "core.executor",
        "utils.serializer",
        "utils.validator",
        "utils.transformer",
        "models.report_config",
        "models.data_source",
        "models.aggregation",
        "pipeline.extract",
        "pipeline.transform",
        "pipeline.load",
        "connectors.postgres",
        "connectors.redis",
        "connectors.s3",
    ]
    for i in range(52):
        mod = modules[i % len(modules)]
        line_no = 40 + (i * 7) % 200
        func = f"process_step_{i}" if i > 0 else "handle_request"
        frames += f'  File "/app/src/{mod.replace(".", "/")}.py", line {line_no}, in {func}\n'
        frames += f"    result = self._invoke_next(context, step={i})\n"
    return EvalCase(
        ticket=EvalTicket(
            ticket_id="INC-DC-145",
            subject="Production analytics API returning 500 errors since 3 AM",
            description=(
                "The analytics API (analytics-api.contoso.com) has been returning HTTP 500 "
                "errors on all /v2/reports/* endpoints since approximately 03:00 UTC today. "
                "Our monitoring dashboard shows a 100% error rate on those endpoints. The "
                "application logs show the following Python traceback:\n\n"
                "Traceback (most recent call last):\n"
                f"{frames}"
                "RecursionError: maximum recursion depth exceeded while calling a Python object\n\n"
                "This looks like an infinite recursion in the report pipeline. It was working "
                "fine yesterday. The only change was a deployment at 02:45 UTC (commit abc123f) "
                "that was supposed to be a minor config update.\n\n"
                "The API serves 12 internal dashboards and 3 customer-facing portals.\n\n"
                "— Priya Sharma, Platform Engineering\npriya.sharma@contoso.com"
            ),
            reporter=Reporter(
                name="Priya Sharma",
                email="priya.sharma@contoso.com",
                department="Platform Engineering",
            ),
            created_at="2026-04-08T04:15:00Z",
            channel=Channel.CHAT,
        ),
        gold=GoldAnswer(
            ticket_id="INC-DC-145",
            category=Category.SOFTWARE,
            priority=Priority.P1,
            assigned_team=Team.ENTERPRISE_APPS,
            needs_escalation=False,
            missing_information=[MissingInfoField.CONFIGURATION_DETAILS],
            next_best_action=(
                "Roll back deployment commit abc123f and investigate the infinite recursion "
                "in the analytics report pipeline."
            ),
            remediation_steps=[
                "Immediately roll back the 02:45 UTC deployment (commit abc123f) to restore service.",
                "Review the config change in commit abc123f for unintended pipeline cycle introduction.",
                "Add recursion depth guards to the report pipeline's _invoke_next method.",
                "Deploy a fix with integration tests that detect circular pipeline configurations.",
            ],
        ),
        tags=["data-cleanup", "deep_traceback"],
        description="Deep Python traceback (50+ frames) from a production RecursionError crash.",
    )


def _dc146_long_tracking_urls() -> EvalCase:
    """URLs with extremely long tracking parameters in a web proxy issue."""
    tracking_params = "&".join(f"utm_{chr(97 + i % 26)}={'x' * 80}" for i in range(30))
    long_url = f"https://marketing.contoso.com/campaign/spring-2026?{tracking_params}"
    return EvalCase(
        ticket=EvalTicket(
            ticket_id="INC-DC-146",
            subject="Web proxy blocking legitimate marketing URLs",
            description=(
                "Our Zscaler web proxy is blocking access to our own marketing campaign pages. "
                "When users click links in the campaign emails, they get a 'URL blocked by policy' "
                "error. The URLs are extremely long because of the tracking parameters appended "
                "by our marketing automation platform (Marketo). Here is an example URL that "
                "is being blocked:\n\n"
                f"{long_url}\n\n"
                "The proxy seems to be rejecting URLs longer than 2048 characters. We've tested "
                "with shorter URLs to the same domain and they work fine. This has been reported "
                "by about 40 users in the Sales and Marketing departments who cannot access the "
                "campaign landing pages.\n\n"
                "We need the URL length limit increased on the proxy or an exception added for "
                "marketing.contoso.com URLs.\n\n"
                "— Jessica Lin, Marketing\njessica.lin@contoso.com"
            ),
            reporter=Reporter(
                name="Jessica Lin",
                email="jessica.lin@contoso.com",
                department="Marketing",
            ),
            created_at="2026-04-08T10:00:00Z",
            channel=Channel.EMAIL,
        ),
        gold=GoldAnswer(
            ticket_id="INC-DC-146",
            category=Category.NETWORK,
            priority=Priority.P3,
            assigned_team=Team.NETWORK_OPS,
            needs_escalation=False,
            missing_information=[MissingInfoField.NETWORK_LOCATION, MissingInfoField.ERROR_MESSAGE],
            next_best_action=(
                "Adjust the Zscaler web proxy URL length policy to accommodate long marketing "
                "URLs or add a bypass rule for marketing.contoso.com."
            ),
            remediation_steps=[
                "Review the Zscaler URL filtering policy for the maximum URL length threshold.",
                "Add marketing.contoso.com to the proxy bypass or allowlist as an interim fix.",
                "Coordinate with the marketing team to evaluate shortening tracking parameters.",
                "Test access to the long campaign URLs after the policy change.",
            ],
        ),
        tags=["data-cleanup", "long_tracking_urls"],
        description="URLs with extremely long tracking parameters (2000+ chars) in a web proxy issue.",
    )


def _dc147_ooo_chain() -> EvalCase:
    """Multiple conflicting out-of-office auto-reply chains burying a DNS issue."""
    return EvalCase(
        ticket=EvalTicket(
            ticket_id="INC-DC-147",
            subject="DNS resolution failing for internal services",
            description=(
                "--- Auto-Reply: Out of Office ---\n"
                "From: helpdesk-l1@contoso.com\n"
                "I am currently out of the office from April 7-11 attending "
                "the ITSM World Conference in Chicago. For urgent issues, "
                "please contact helpdesk-l2@contoso.com.\n"
                "Best, Morgan Riley\n\n"
                "--- Auto-Reply: Out of Office ---\n"
                "From: helpdesk-l2@contoso.com\n"
                "Thank you for your email. I am out of the office on "
                "parental leave until May 15, 2026. Please redirect all "
                "inquiries to helpdesk-l3@contoso.com or call the IT "
                "hotline at x4500.\n"
                "Kind regards, Jordan Beck\n\n"
                "--- Auto-Reply: Out of Office ---\n"
                "From: helpdesk-l3@contoso.com\n"
                "I am on PTO today (April 8). For urgent matters, please "
                "reach out to helpdesk-l1@contoso.com.\n"
                "Thanks, Casey Morgan\n\n"
                "--- Auto-Reply: Mailbox Full ---\n"
                "From: network-ops@contoso.com\n"
                "The mailbox for network-ops@contoso.com is full and cannot "
                "receive new messages. Please contact the team directly via "
                "Teams chat or call x4600.\n\n"
                "--- Original Message ---\n"
                "From: Tom Bradley <tom.bradley@contoso.com>\n"
                "Date: Tue, 8 Apr 2026 06:45:00 -0400\n"
                "Subject: DNS resolution failing for internal services\n\n"
                "Hi team,\n\n"
                "Starting at around 6 AM today, DNS resolution for internal "
                "services is failing intermittently. nslookup against our "
                "internal DNS servers (dns-01.contoso.com and dns-02.contoso.com) "
                "returns SERVFAIL about 60% of the time. External DNS "
                "(8.8.8.8) works fine.\n\n"
                "Affected services include:\n"
                "- git.contoso.com (internal GitLab)\n"
                "- wiki.contoso.com (Confluence)\n"
                "- jira.contoso.com\n"
                "- erp.contoso.com (SAP)\n\n"
                "This is impacting the entire Boston office (~300 users). "
                "Some people have switched to using 8.8.8.8 as a workaround "
                "but that breaks access to .contoso.internal zones.\n\n"
                "Please investigate urgently.\n\n"
                "— Tom Bradley, Engineering\ntom.bradley@contoso.com"
            ),
            reporter=Reporter(
                name="Tom Bradley",
                email="tom.bradley@contoso.com",
                department="Engineering",
            ),
            created_at="2026-04-08T06:50:00Z",
            channel=Channel.EMAIL,
        ),
        gold=GoldAnswer(
            ticket_id="INC-DC-147",
            category=Category.NETWORK,
            priority=Priority.P1,
            assigned_team=Team.NETWORK_OPS,
            needs_escalation=False,
            missing_information=[MissingInfoField.ERROR_MESSAGE, MissingInfoField.NETWORK_LOCATION],
            next_best_action=(
                "Investigate intermittent SERVFAIL responses from internal DNS servers "
                "dns-01.contoso.com and dns-02.contoso.com affecting the Boston office."
            ),
            remediation_steps=[
                "Check the health and logs of dns-01.contoso.com and dns-02.contoso.com for errors.",
                "Verify DNS zone file integrity and replication status between the two servers.",
                "Restart the DNS service on the affected servers if log analysis indicates corruption.",
                "Monitor resolution success rates after remediation to confirm stability.",
            ],
        ),
        tags=["data-cleanup", "ooo_chain"],
        description="Multiple stacked out-of-office auto-replies burying a real DNS resolution failure.",
    )


def _dc148_base64_excel() -> EvalCase:
    """Base64-encoded Excel data inlined in a data migration ticket."""
    fake_b64 = "UEsDBBQAAAAIAA" + "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/" * 20 + "=="
    return EvalCase(
        ticket=EvalTicket(
            ticket_id="INC-DC-148",
            subject="Data migration from legacy Oracle DB to Azure SQL failing",
            description=(
                "We're migrating the Inventory Management data from our on-prem Oracle 19c "
                "database to Azure SQL Managed Instance using Azure Database Migration Service "
                "(DMS). The migration keeps failing at the InventoryTransactions table with "
                "error: 'Bulk insert failed. Column 7 (unit_price) contains a value that "
                "exceeds the max length for decimal(10,2).'\n\n"
                "I've attached the problematic data as a base64-encoded Excel extract below. "
                "These are the rows that are failing:\n\n"
                f"--- BEGIN BASE64 XLSX ---\n{fake_b64}\n--- END BASE64 XLSX ---\n\n"
                "The source Oracle table uses NUMBER(15,4) for unit_price but the target "
                "Azure SQL table was created with DECIMAL(10,2). I suspect this is a precision "
                "mismatch but I need the Data Platform team to confirm and either alter the "
                "target schema or add a transformation step to the DMS pipeline.\n\n"
                "We have a hard deadline of April 15 to complete the migration.\n\n"
                "— Anika Johansson, Operations\nanika.johansson@contoso.com"
            ),
            reporter=Reporter(
                name="Anika Johansson",
                email="anika.johansson@contoso.com",
                department="Operations",
            ),
            created_at="2026-04-08T11:00:00Z",
            channel=Channel.PORTAL,
        ),
        gold=GoldAnswer(
            ticket_id="INC-DC-148",
            category=Category.DATA_STORAGE,
            priority=Priority.P2,
            assigned_team=Team.DATA_PLATFORM,
            needs_escalation=False,
            missing_information=[MissingInfoField.ENVIRONMENT_DETAILS],
            next_best_action=(
                "Resolve the decimal precision mismatch between the Oracle source (NUMBER 15,4) "
                "and Azure SQL target (DECIMAL 10,2) for the InventoryTransactions table."
            ),
            remediation_steps=[
                "Alter the target Azure SQL column from DECIMAL(10,2) to DECIMAL(15,4) to match Oracle.",
                "Re-run the DMS migration for the InventoryTransactions table after the schema change.",
                "Audit other numeric columns in the migration for similar precision mismatches.",
                "Add schema validation as a pre-migration check to catch type mismatches early.",
            ],
        ),
        tags=["data-cleanup", "base64_excel"],
        description="Base64-encoded Excel data pasted inline in a database migration ticket.",
    )


def _dc149_terraform_dump() -> EvalCase:
    """Terraform HCL template dump for a cloud VNet peering issue."""
    return EvalCase(
        ticket=EvalTicket(
            ticket_id="INC-DC-149",
            subject="Azure VNet peering between hub and spoke failing — Terraform apply error",
            description=(
                "Our hub-spoke network topology deployment is failing during terraform apply. "
                "The VNet peering between the hub VNet and the analytics spoke VNet is not "
                "being established. Here is the relevant Terraform configuration:\n\n"
                'resource "azurerm_virtual_network" "hub" {\n'
                '  name                = "vnet-hub-eastus-001"\n'
                '  address_space       = ["10.0.0.0/16"]\n'
                "  location            = azurerm_resource_group.hub.location\n"
                "  resource_group_name = azurerm_resource_group.hub.name\n"
                "}\n\n"
                'resource "azurerm_virtual_network" "spoke_analytics" {\n'
                '  name                = "vnet-spoke-analytics-eastus-001"\n'
                '  address_space       = ["10.1.0.0/16"]\n'
                "  location            = azurerm_resource_group.analytics.location\n"
                "  resource_group_name = azurerm_resource_group.analytics.name\n"
                "}\n\n"
                'resource "azurerm_virtual_network_peering" "hub_to_spoke" {\n'
                '  name                         = "peer-hub-to-analytics"\n'
                "  resource_group_name          = azurerm_resource_group.hub.name\n"
                "  virtual_network_name         = azurerm_virtual_network.hub.name\n"
                "  remote_virtual_network_id    = azurerm_virtual_network.spoke_analytics.id\n"
                "  allow_virtual_network_access = true\n"
                "  allow_forwarded_traffic      = true\n"
                "  allow_gateway_transit        = true\n"
                "}\n\n"
                'resource "azurerm_virtual_network_peering" "spoke_to_hub" {\n'
                '  name                         = "peer-analytics-to-hub"\n'
                "  resource_group_name          = azurerm_resource_group.analytics.name\n"
                "  virtual_network_name         = azurerm_virtual_network.spoke_analytics.name\n"
                "  remote_virtual_network_id    = azurerm_virtual_network.hub.id\n"
                "  allow_virtual_network_access = true\n"
                "  allow_forwarded_traffic      = true\n"
                "  use_remote_gateways          = true\n"
                "}\n\n"
                "The error from terraform apply is:\n"
                "Error: creating Virtual Network Peering: peering "
                "peer-analytics-to-hub cannot have UseRemoteGateways flag set to true "
                "because the remote virtual network vnet-hub-eastus-001 does not have a "
                "gateway.\n\n"
                "We need to deploy a VPN Gateway in the hub VNet before we can use "
                "use_remote_gateways = true on the spoke side. However, the gateway "
                "provisioning takes 30-45 minutes and we need the peering up ASAP.\n\n"
                "— Kevin O'Sullivan, Cloud Infrastructure\nkevin.osullivan@contoso.com"
            ),
            reporter=Reporter(
                name="Kevin O'Sullivan",
                email="kevin.osullivan@contoso.com",
                department="Cloud Infrastructure",
            ),
            created_at="2026-04-08T13:30:00Z",
            channel=Channel.CHAT,
        ),
        gold=GoldAnswer(
            ticket_id="INC-DC-149",
            category=Category.NETWORK,
            priority=Priority.P2,
            assigned_team=Team.NETWORK_OPS,
            needs_escalation=False,
            missing_information=[MissingInfoField.CONFIGURATION_DETAILS],
            next_best_action=(
                "Remove use_remote_gateways from the spoke peering as an interim fix, then "
                "provision a VPN Gateway in the hub VNet to enable gateway transit."
            ),
            remediation_steps=[
                "Set use_remote_gateways = false on the spoke peering to establish connectivity immediately.",
                "Provision an Azure VPN Gateway in the hub VNet (plan for 30-45 min provisioning time).",
                "After the gateway is provisioned, re-enable use_remote_gateways on the spoke peering.",
                "Verify bidirectional connectivity between hub and spoke VNets after peering is established.",
            ],
        ),
        tags=["data-cleanup", "terraform_dump"],
        description="Terraform HCL resource definitions pasted inline for a VNet peering failure.",
    )


def _dc150_git_blame() -> EvalCase:
    """Git blame output pasted for a production application bug."""
    blame_lines = ""
    authors = [
        ("a1b2c3d4", "Alice Wang", "2026-03-15"),
        ("e5f6a7b8", "Bob Chen", "2026-03-20"),
        ("c9d0e1f2", "Carol Davis", "2026-03-22"),
        ("a3b4c5d6", "Dan Miller", "2026-04-01"),
        ("e7f8a9b0", "Eve Wilson", "2026-04-05"),
    ]
    code_lines = [
        "class ReportGenerator:",
        "    def __init__(self, config):",
        "        self.config = config",
        "        self.cache = {}",
        "",
        "    def generate(self, report_id):",
        "        data = self._fetch_data(report_id)",
        "        if data is None:",
        "            return None  # BUG: should raise, not return None",
        "        transformed = self._transform(data)",
        "        return self._render(transformed)",
        "",
        "    def _fetch_data(self, report_id):",
        "        if report_id in self.cache:",
        "            return self.cache[report_id]",
        "        result = self.db.query(report_id)",
        "        self.cache[report_id] = result",
        "        return result",
        "",
        "    def _transform(self, data):",
        "        # This method was changed in the last deploy",
        "        output = []",
        "        for row in data:",
        "            output.append(row.to_dict())",
        "        return output",
        "",
        "    def _render(self, data):",
        "        template = self.config.get_template()",
        "        return template.render(data=data)",
    ]
    for i, line in enumerate(code_lines):
        author_info = authors[i % len(authors)]
        blame_lines += f"{author_info[0]} ({author_info[1]:15s} {author_info[2]} {8 + i:>3d}) {line}\n"
    return EvalCase(
        ticket=EvalTicket(
            ticket_id="INC-DC-150",
            subject="Report generator returning blank pages in production",
            description=(
                "The ReportGenerator module in our internal analytics platform has been "
                "returning blank pages since yesterday's deploy (release v3.8.1). The issue "
                "affects all PDF report exports. I ran git blame on the report_generator.py "
                "file to see what changed recently:\n\n"
                f"{blame_lines}\n"
                "I believe the bug is on line 9 — when _fetch_data returns None (e.g., for "
                "a report_id that doesn't exist in the database), generate() silently returns "
                "None instead of raising an exception. The _render method then receives None "
                "and produces a blank page.\n\n"
                "This worked before because in v3.8.0, _fetch_data always returned an empty "
                "list instead of None for missing reports. The change in v3.8.1 broke that "
                "contract.\n\n"
                "This is affecting the Finance team's end-of-quarter reports which are due "
                "by end of day Friday.\n\n"
                "— Hiroshi Tanaka, Software Engineering\nhiroshi.tanaka@contoso.com"
            ),
            reporter=Reporter(
                name="Hiroshi Tanaka",
                email="hiroshi.tanaka@contoso.com",
                department="Software Engineering",
            ),
            created_at="2026-04-08T14:00:00Z",
            channel=Channel.PORTAL,
        ),
        gold=GoldAnswer(
            ticket_id="INC-DC-150",
            category=Category.SOFTWARE,
            priority=Priority.P2,
            assigned_team=Team.ENTERPRISE_APPS,
            needs_escalation=False,
            missing_information=[MissingInfoField.ENVIRONMENT_DETAILS],
            next_best_action=(
                "Fix the _fetch_data return value contract in the ReportGenerator module "
                "to return an empty list instead of None for missing reports."
            ),
            remediation_steps=[
                "Patch _fetch_data to return an empty list instead of None for missing report IDs.",
                "Add a null check in generate() to raise a descriptive exception if data is None.",
                "Deploy the fix as a hotfix to unblock the Finance team's end-of-quarter reports.",
                "Add regression tests to ensure _fetch_data never returns None.",
            ],
        ),
        tags=["data-cleanup", "git_blame"],
        description="Git blame output pasted inline for a production report generator bug.",
    )



# ---------------------------------------------------------------------------
# INC-DC-151 .. INC-DC-170  —  extended data-cleanup evaluation cases
# ---------------------------------------------------------------------------


def _dc151_rtl_arabic_zero_width() -> EvalCase:
    """Arabic RTL text with zero-width joiners obscuring the real issue."""
    arabic_noise = (
        "\u200f\u0645\u0631\u062d\u0628\u0627\u200c \u0628\u0641\u0631\u064a\u0642\u200c "
        "\u062f\u0639\u0645\u200c \u062a\u0643\u0646\u0648\u0644\u0648\u062c\u064a\u0627\u200c "
        "\u0627\u0644\u0645\u0639\u0644\u0648\u0645\u0627\u062a\u200c"
    )
    return EvalCase(
        ticket=EvalTicket(
            ticket_id="INC-DC-151",
            subject=f"{arabic_noise} — VPN disconnects every 10 minutes",
            description=(
                f"{arabic_noise}\n\n"
                "Dear IT team,\n\n"
                "My GlobalProtect VPN (version 6.1.3) disconnects every 10 minutes. "
                "I'm on the Dubai office Wi-Fi (CONTOSO-DXB). Windows 11 laptop "
                "(Dell Latitude 7440). Started after last week's firmware update on "
                "the access points.\n\n"
                f"{arabic_noise}\n\n"
                "Error code GP-4017 in the logs. Please help urgently."
            ),
            reporter=Reporter(
                name="Ahmad Hassan",
                email="ahmad.hassan@contoso.com",
                department="Middle East Operations",
            ),
            created_at="2026-04-08T14:00:00Z",
            channel=Channel.EMAIL,
        ),
        gold=GoldAnswer(
            ticket_id="INC-DC-151",
            category=Category.NETWORK,
            priority=Priority.P2,
            assigned_team=Team.NETWORK_OPS,
            needs_escalation=False,
            missing_information=[MissingInfoField.NETWORK_LOCATION],
            next_best_action=(
                "Investigate recurring VPN disconnections on the Dubai office Wi-Fi "
                "after the firmware update — strip the RTL noise and zero-width characters."
            ),
            remediation_steps=[
                "Check the Dubai office AP firmware changelog for VPN passthrough issues.",
                "Review GlobalProtect gateway logs for GP-4017 patterns from the DXB network.",
                "Test VPN from an Ethernet connection to isolate Wi-Fi vs. VPN issues.",
            ],
        ),
        tags=["data-cleanup", "rtl_arabic"],
        description="Arabic RTL text with zero-width joiners wrapping a real VPN issue.",
    )


def _dc152_unicode_nfd_accents() -> EvalCase:
    """Unicode NFD accented characters in name and description."""
    nfd_name = "Rene\u0301 Mu\u0308ller"  # René Müller in NFD
    return EvalCase(
        ticket=EvalTicket(
            ticket_id="INC-DC-152",
            subject=f"Outlook not syncing for {nfd_name}",
            description=(
                f"User: {nfd_name} (rene.mueller@contoso.com)\n"
                f"Department: Gesch\u00e4ftsfu\u0308hrung\n\n"
                "Outlook 365 desktop client stopped syncing email since Monday. "
                "Shows 'Disconnected' in the bottom status bar. Web Outlook works "
                "fine. Autodiscover returns correct settings.\n\n"
                "Running Windows 11, Office Build 16.0.18025.20160."
            ),
            reporter=Reporter(
                name=nfd_name,
                email="rene.mueller@contoso.com",
                department="Executive Office",
            ),
            created_at="2026-04-08T14:00:00Z",
            channel=Channel.PORTAL,
        ),
        gold=GoldAnswer(
            ticket_id="INC-DC-152",
            category=Category.SOFTWARE,
            priority=Priority.P3,
            assigned_team=Team.ENTERPRISE_APPS,
            needs_escalation=False,
            missing_information=[MissingInfoField.ERROR_MESSAGE],
            next_best_action=(
                "Investigate Outlook desktop sync failure — the NFD-encoded accented "
                "characters in the reporter name and department do not affect triage."
            ),
            remediation_steps=[
                "Create a new Outlook profile and re-add the Exchange account.",
                "Check the Outlook connection status dialog for the specific error.",
                "Verify Autodiscover with the Test Email AutoConfiguration tool.",
            ],
        ),
        tags=["data-cleanup", "unicode_nfd"],
        description="NFD Unicode normalization in reporter name and department field.",
    )


def _dc153_base64_image_flood() -> EvalCase:
    """Multiple inline base64 images obscuring a real hardware issue."""
    fake_b64 = "iVBORw0KGgo" + "A" * 500 + "=="
    images = "\n".join(
        [f"[Screenshot {i}]: data:image/png;base64,{fake_b64}" for i in range(1, 9)]
    )
    return EvalCase(
        ticket=EvalTicket(
            ticket_id="INC-DC-153",
            subject="Monitor flickering — see attached screenshots",
            description=(
                "My Dell U2722D monitor flickers every 30 seconds. I took 8 screenshots:\n\n"
                f"{images}\n\n"
                "Using DisplayPort cable, connected to Dell Latitude 7440 docking station. "
                "Happens on both 60 Hz and 30 Hz. Updated Intel UHD drivers yesterday."
            ),
            reporter=Reporter(
                name="Lisa Chen",
                email="lisa.chen@contoso.com",
                department="Design",
            ),
            created_at="2026-04-08T14:00:00Z",
            channel=Channel.PORTAL,
        ),
        gold=GoldAnswer(
            ticket_id="INC-DC-153",
            category=Category.HARDWARE,
            priority=Priority.P3,
            assigned_team=Team.ENDPOINT,
            needs_escalation=False,
            missing_information=[MissingInfoField.DEVICE_INFO],
            next_best_action=(
                "Investigate the monitor flickering issue — ignore the inline base64 "
                "image data that clutters the description."
            ),
            remediation_steps=[
                "Test with a different DisplayPort cable.",
                "Try connecting the monitor directly (bypassing the dock).",
                "Roll back the Intel UHD driver to the previous version.",
            ],
        ),
        tags=["data-cleanup", "base64_flood"],
        description="Eight inline base64 screenshots obscuring a monitor flickering issue.",
    )


def _dc154_deep_mime_nesting() -> EvalCase:
    """Deeply nested MIME boundaries from repeated email forwarding."""
    boundaries = ""
    for i in range(15):
        boundaries += (
            f"--=_Part_{i:04d}_boundary\n"
            f"Content-Type: multipart/mixed; boundary=\"=_Part_{i + 1:04d}_boundary\"\n\n"
        )
    return EvalCase(
        ticket=EvalTicket(
            ticket_id="INC-DC-154",
            subject="Fwd: Fwd: Fwd: Fwd: Fwd: Shared drive access needed",
            description=(
                f"{boundaries}\n"
                "Original message:\n\n"
                "I need read/write access to \\\\file-server-02\\shared\\finance-q1. "
                "My manager (David Kim) approved it last week. Employee ID E-22104, "
                "Floor 3, Building 1.\n\n"
                "This email was forwarded through 15 people before reaching IT."
            ),
            reporter=Reporter(
                name="Kevin Park",
                email="kevin.park@contoso.com",
                department="Finance",
            ),
            created_at="2026-04-08T14:00:00Z",
            channel=Channel.EMAIL,
        ),
        gold=GoldAnswer(
            ticket_id="INC-DC-154",
            category=Category.ACCESS_AUTH,
            priority=Priority.P3,
            assigned_team=Team.IAM,
            needs_escalation=False,
            missing_information=[MissingInfoField.AFFECTED_SYSTEM],
            next_best_action=(
                "Grant shared drive access after verifying manager approval — "
                "strip the 15-level MIME nesting noise."
            ),
            remediation_steps=[
                "Confirm David Kim's approval for the finance-q1 share.",
                "Grant read/write access via the file server ACL.",
                "Notify the user and verify access works.",
            ],
        ),
        tags=["data-cleanup", "deep_mime"],
        description="15-level deep MIME boundary nesting from repeated email forwarding.",
    )


def _dc155_csv_injection_formula() -> EvalCase:
    """CSV injection with spreadsheet formulas in the ticket body."""
    return EvalCase(
        ticket=EvalTicket(
            ticket_id="INC-DC-155",
            subject="Expense report app crashing — data attached",
            description=(
                "The expense report app crashes when I upload this data:\n\n"
                "Employee,Amount,Description\n"
                '=CMD(\'calc.exe\'),1500,Travel\n'
                '+HYPERLINK("http://evil.com","Click"),200,Hotel\n'
                "-1+1*cmd|'/C calc'!A0,350,Food\n"
                "@SUM(A1:A10),100,Misc\n\n"
                "The app (ExpenseTracker v3.2) crashes with a blank screen "
                "after the CSV is pasted. Chrome 122, Windows 11."
            ),
            reporter=Reporter(
                name="Maria Gonzalez",
                email="maria.gonzalez@contoso.com",
                department="Sales",
            ),
            created_at="2026-04-08T14:00:00Z",
            channel=Channel.PORTAL,
        ),
        gold=GoldAnswer(
            ticket_id="INC-DC-155",
            category=Category.SOFTWARE,
            priority=Priority.P3,
            assigned_team=Team.ENTERPRISE_APPS,
            needs_escalation=False,
            missing_information=[MissingInfoField.STEPS_TO_REPRODUCE],
            next_best_action=(
                "Investigate the expense app crash on CSV upload — the formulas in the "
                "data are CSV injection patterns but represent the user's actual data."
            ),
            remediation_steps=[
                "Test the CSV upload with sanitized data to confirm the crash is data-dependent.",
                "Add CSV formula sanitization to the ExpenseTracker upload handler.",
                "Provide a workaround: prefix formula characters with a single quote.",
            ],
        ),
        tags=["data-cleanup", "csv_injection"],
        description="CSV injection formulas pasted in a ticket about an expense app crash.",
    )


def _dc156_zalgo_combining_marks() -> EvalCase:
    """Zalgo text with stacked combining diacritical marks."""
    zalgo = "H\u0336\u033a\u0347e\u0337\u0346\u0316l\u0334\u0318\u0348p\u0335\u0319\u0349"
    return EvalCase(
        ticket=EvalTicket(
            ticket_id="INC-DC-156",
            subject=f"{zalgo} — printer not working Floor 5",
            description=(
                f"{zalgo} {zalgo} {zalgo}\n\n"
                "The HP LaserJet M404dn on Floor 5 near room 5-201 is not printing. "
                "Jobs queue but nothing comes out. Display shows 'Ready' but paper tray "
                "is empty according to the control panel (it's actually full).\n\n"
                f"Printer IP: 10.1.5.42\nAsset tag: PRN-5201\n\n{zalgo}"
            ),
            reporter=Reporter(
                name="Derek Johnson",
                email="derek.johnson@contoso.com",
                department="HR",
            ),
            created_at="2026-04-08T14:00:00Z",
            channel=Channel.CHAT,
        ),
        gold=GoldAnswer(
            ticket_id="INC-DC-156",
            category=Category.HARDWARE,
            priority=Priority.P3,
            assigned_team=Team.ENDPOINT,
            needs_escalation=False,
            missing_information=[],
            next_best_action=(
                "Fix the printer paper tray sensor issue on Floor 5 — "
                "strip the Zalgo combining marks from the ticket."
            ),
            remediation_steps=[
                "Check the paper tray sensor on the HP LaserJet M404dn.",
                "Restart the print spooler service on the print server.",
                "Clear the stuck print queue and resubmit a test page.",
            ],
        ),
        tags=["data-cleanup", "zalgo_text"],
        description="Zalgo text with combining diacritical marks around a printer issue.",
    )


def _dc157_hebrew_bidi_mixed() -> EvalCase:
    """Hebrew/English bidirectional text confusing field ordering."""
    hebrew = "\u05e9\u05dc\u05d5\u05dd \u05e6\u05d5\u05d5\u05ea \u05ea\u05de\u05d9\u05db\u05d4"
    return EvalCase(
        ticket=EvalTicket(
            ticket_id="INC-DC-157",
            subject=f"{hebrew} - Teams not loading",
            description=(
                f"{hebrew}\n\n"
                "Microsoft Teams desktop app (1.7.00.4654) won't load past the "
                "spinning logo. Tel Aviv office, Windows 11. Cleared cache at "
                "%AppData%\\Microsoft\\Teams. Web version works. Need this for a "
                "client call at 2 PM IST.\n\n"
                f"{hebrew}"
            ),
            reporter=Reporter(
                name="Yael Cohen",
                email="yael.cohen@contoso.com",
                department="Customer Relations",
            ),
            created_at="2026-04-08T14:00:00Z",
            channel=Channel.CHAT,
        ),
        gold=GoldAnswer(
            ticket_id="INC-DC-157",
            category=Category.SOFTWARE,
            priority=Priority.P2,
            assigned_team=Team.ENTERPRISE_APPS,
            needs_escalation=False,
            missing_information=[MissingInfoField.APPLICATION_VERSION],
            next_best_action=(
                "Fix Teams desktop loading issue before the 2 PM client call — "
                "Hebrew bidi text does not affect triage."
            ),
            remediation_steps=[
                "Fully uninstall Teams including the %AppData% and %LocalAppData% folders.",
                "Reinstall the latest Teams desktop client.",
                "If the call is imminent, use Teams Web as a workaround.",
            ],
        ),
        tags=["data-cleanup", "hebrew_bidi"],
        description="Hebrew bidirectional text mixed with English in a Teams loading issue.",
    )


def _dc158_jenkins_ansi_codes() -> EvalCase:
    """Jenkins CI output with ANSI escape codes pasted in a ticket."""
    ansi_output = (
        "\033[1;32m[Pipeline] {\033[0m\n"
        "\033[1;32m[Pipeline] stage\033[0m\n"
        "\033[1;32m[Pipeline] { (Build)\033[0m\n"
        "\033[1;31m[ERROR] BUILD FAILURE\033[0m\n"
        "\033[1;31m[ERROR] \033[0mFailed to execute goal org.apache.maven.plugins:"
        "maven-compiler-plugin:3.11.0:compile (default) on project contoso-api: "
        "Compilation failure\n"
        "\033[1;31m[ERROR] /src/main/java/com/contoso/api/AuthService.java:[42,15] "
        "error: incompatible types: String cannot be converted to UUID\033[0m\n"
        "\033[1;33m[WARNING] The requested profile 'prod' could not be activated.\033[0m\n"
    )
    return EvalCase(
        ticket=EvalTicket(
            ticket_id="INC-DC-158",
            subject="CI/CD pipeline build failure — AuthService compilation error",
            description=(
                "Our Jenkins pipeline (contoso-api-main, build #847) failed. "
                "Here's the console output:\n\n"
                f"{ansi_output}\n"
                "The AuthService.java line 42 has a type mismatch after PR #312 merged. "
                "This is blocking the release train for sprint 24."
            ),
            reporter=Reporter(
                name="James Wright",
                email="james.wright@contoso.com",
                department="DevOps",
            ),
            created_at="2026-04-08T14:00:00Z",
            channel=Channel.EMAIL,
        ),
        gold=GoldAnswer(
            ticket_id="INC-DC-158",
            category=Category.SOFTWARE,
            priority=Priority.P2,
            assigned_team=Team.ENTERPRISE_APPS,
            needs_escalation=False,
            missing_information=[MissingInfoField.ENVIRONMENT_DETAILS],
            next_best_action=(
                "Fix the AuthService type mismatch blocking the CI pipeline — "
                "ignore the ANSI escape codes in the build output."
            ),
            remediation_steps=[
                "Revert or fix PR #312's change to AuthService.java line 42.",
                "Change the parameter type from String to UUID or add proper conversion.",
                "Rerun the Jenkins pipeline after the fix to unblock the release.",
            ],
        ),
        tags=["data-cleanup", "ansi_codes"],
        description="Jenkins CI console output with ANSI escape codes in a build failure ticket.",
    )


def _dc159_terraform_plan_dump() -> EvalCase:
    """Large Terraform plan output pasted in a ticket."""
    tf_plan = ""
    resources = [
        ("azurerm_virtual_network.main", "10.0.0.0/16", "10.0.0.0/20"),
        ("azurerm_subnet.app", "10.0.0.0/24", "10.0.1.0/24"),
        ("azurerm_network_security_group.app", "Allow-443", "Allow-443-8443"),
        ("azurerm_application_gateway.main", "Standard_v2", "WAF_v2"),
        ("azurerm_key_vault.main", "standard", "premium"),
    ]
    for res, old, new in resources:
        tf_plan += (
            f"  # {res} must be replaced\n"
            f"  ~ resource \"{res.split('.')[0]}\" \"{res.split('.')[1]}\" {{\n"
            f"      - old_value = \"{old}\"\n"
            f"      + new_value = \"{new}\"\n"
            f"    }}\n\n"
        )
    return EvalCase(
        ticket=EvalTicket(
            ticket_id="INC-DC-159",
            subject="Terraform apply failed — NSG rule conflict in production",
            description=(
                "Running `terraform apply` on the prod-eastus-001 workspace failed:\n\n"
                f"{tf_plan}\n"
                "Error: A resource with the ID /subscriptions/.../networkSecurityGroups/"
                "app-nsg already exists. Possible state drift after manual portal change "
                "last week by the networking team.\n\n"
                "Need help reconciling Terraform state with actual Azure resources."
            ),
            reporter=Reporter(
                name="Priya Sharma",
                email="priya.sharma@contoso.com",
                department="Cloud Engineering",
            ),
            created_at="2026-04-08T14:00:00Z",
            channel=Channel.PORTAL,
        ),
        gold=GoldAnswer(
            ticket_id="INC-DC-159",
            category=Category.SOFTWARE,
            priority=Priority.P2,
            assigned_team=Team.ENTERPRISE_APPS,
            needs_escalation=False,
            missing_information=[MissingInfoField.ENVIRONMENT_DETAILS],
            next_best_action=(
                "Reconcile Terraform state drift for the prod-eastus-001 workspace — "
                "the large plan output is noise but contains useful context."
            ),
            remediation_steps=[
                "Run terraform import for the manually-created NSG resource.",
                "Update the Terraform state to match actual Azure resource IDs.",
                "Apply the plan again after state reconciliation.",
            ],
        ),
        tags=["data-cleanup", "terraform_dump"],
        description="Terraform plan output pasted in a state drift resolution ticket.",
    )


def _dc160_graphql_introspection() -> EvalCase:
    """GraphQL introspection response dumped in a ticket."""
    schema_fragment = (
        '{"data":{"__schema":{"queryType":{"name":"Query"},"types":['
        '{"kind":"OBJECT","name":"User","fields":['
        '{"name":"id","type":{"kind":"NON_NULL","name":null,"ofType":{"kind":"SCALAR","name":"ID"}}},'
        '{"name":"email","type":{"kind":"SCALAR","name":"String"}},'
        '{"name":"role","type":{"kind":"ENUM","name":"UserRole"}},'
        '{"name":"createdAt","type":{"kind":"SCALAR","name":"DateTime"}}'
        "]},"
        '{"kind":"OBJECT","name":"Ticket","fields":['
        '{"name":"id","type":{"kind":"NON_NULL","name":null,"ofType":{"kind":"SCALAR","name":"ID"}}},'
        '{"name":"title","type":{"kind":"SCALAR","name":"String"}},'
        '{"name":"status","type":{"kind":"ENUM","name":"TicketStatus"}}'
        "]}]}}"
    )
    return EvalCase(
        ticket=EvalTicket(
            ticket_id="INC-DC-160",
            subject="GraphQL API returning 500 errors on user queries",
            description=(
                "Our internal GraphQL API (api.contoso.internal/graphql) started returning "
                "500 errors on all user-related queries since 10 AM. Here's the introspection "
                "response from before the issue started (for reference):\n\n"
                f"{schema_fragment}\n\n"
                "The error in the server logs is: 'Cannot return null for non-nullable field "
                "User.email'. Seems like a data migration script set some emails to null."
            ),
            reporter=Reporter(
                name="Alex Rivera",
                email="alex.rivera@contoso.com",
                department="Backend Engineering",
            ),
            created_at="2026-04-08T14:00:00Z",
            channel=Channel.CHAT,
        ),
        gold=GoldAnswer(
            ticket_id="INC-DC-160",
            category=Category.SOFTWARE,
            priority=Priority.P2,
            assigned_team=Team.ENTERPRISE_APPS,
            needs_escalation=False,
            missing_information=[MissingInfoField.ERROR_MESSAGE],
            next_best_action=(
                "Fix the null email data caused by the migration script — "
                "the GraphQL introspection dump is reference context."
            ),
            remediation_steps=[
                "Identify which data migration set User.email to null.",
                "Run a corrective migration to restore email values from backup.",
                "Add a NOT NULL constraint or validation to prevent future nulls.",
            ],
        ),
        tags=["data-cleanup", "graphql_dump"],
        description="GraphQL introspection schema dump in an API 500 error ticket.",
    )


def _dc161_pgp_signed_email() -> EvalCase:
    """PGP-signed email with ASCII armor wrapping a real issue."""
    return EvalCase(
        ticket=EvalTicket(
            ticket_id="INC-DC-161",
            subject="Encrypted file share access request (PGP signed)",
            description=(
                "-----BEGIN PGP SIGNED MESSAGE-----\n"
                "Hash: SHA256\n\n"
                "I need access to the encrypted file share at "
                "\\\\vault-server-01\\classified\\project-phoenix.\n"
                "My GPG key fingerprint: 4A2B C3D4 E5F6 7890 1234 5678 9ABC DEF0 1234 5678\n"
                "Manager approval: David Chen (david.chen@contoso.com)\n"
                "Project code: PHX-2026-Q2\n"
                "Clearance level: Confidential\n"
                "-----BEGIN PGP SIGNATURE-----\n\n"
                "iQIzBAEBCAAdFiEESivD1OX2eJASNFZ4mrze8BI0VngFAmYBcHcACgkQ\n"
                "mrze8BI0VniL3A//fakesignaturedata1234567890abcdefghijklmnop\n"
                "qrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789+/==\n"
                "-----END PGP SIGNATURE-----"
            ),
            reporter=Reporter(
                name="Robert Kim",
                email="robert.kim@contoso.com",
                department="Research",
            ),
            created_at="2026-04-08T14:00:00Z",
            channel=Channel.EMAIL,
        ),
        gold=GoldAnswer(
            ticket_id="INC-DC-161",
            category=Category.ACCESS_AUTH,
            priority=Priority.P3,
            assigned_team=Team.IAM,
            needs_escalation=False,
            missing_information=[MissingInfoField.AUTHENTICATION_METHOD],
            next_best_action=(
                "Process the classified share access request after verifying "
                "manager approval — the PGP signature is noise."
            ),
            remediation_steps=[
                "Verify David Chen's approval for Project Phoenix access.",
                "Confirm the user's clearance level through HR records.",
                "Grant access to the encrypted share and notify the user.",
            ],
        ),
        tags=["data-cleanup", "pgp_armor"],
        description="PGP ASCII armor signature wrapping a file share access request.",
    )


def _dc162_teams_chat_reactions() -> EvalCase:
    """Teams/Slack chat transcript with reactions and emoji flooding."""
    return EvalCase(
        ticket=EvalTicket(
            ticket_id="INC-DC-162",
            subject="Screenshot from Teams chat about server issue",
            description=(
                "From #infra-alerts channel:\n\n"
                "[10:15 AM] AlertBot: \U0001f6a8 CRITICAL: cpu.usage > 95% on "
                "sql-prod-03 for 15 min\n"
                "    \U0001f44d 5  \U0001f631 3  \U0001f525 7  \U0001f440 2\n"
                "[10:16 AM] @sarah.chen: Looking into it\n"
                "    \U0001f44d 1  \u2764\ufe0f 1\n"
                "[10:18 AM] @sarah.chen: It's the nightly ETL job running 3x. "
                "@mike.jones did you change the cron schedule?\n"
                "    \U0001f440 4\n"
                "[10:19 AM] @mike.jones: Oh no \U0001f62c I set it to */20 instead of 0 20\n"
                "    \U0001f926 8  \U0001f602 12\n"
                "[10:20 AM] @sarah.chen: Fixed the cron. CPU dropping now.\n"
                "    \U0001f389 6  \U0001f680 3  \U0001f44f 5\n\n"
                "Can IT verify the ETL cron is correct and add monitoring for this?"
            ),
            reporter=Reporter(
                name="Sarah Chen",
                email="sarah.chen@contoso.com",
                department="Data Engineering",
            ),
            created_at="2026-04-08T14:00:00Z",
            channel=Channel.CHAT,
        ),
        gold=GoldAnswer(
            ticket_id="INC-DC-162",
            category=Category.SOFTWARE,
            priority=Priority.P3,
            assigned_team=Team.DATA_PLATFORM,
            needs_escalation=False,
            missing_information=[MissingInfoField.ENVIRONMENT_DETAILS],
            next_best_action=(
                "Verify the ETL cron schedule fix and add CPU monitoring alerting — "
                "the chat reactions and emoji are presentation noise."
            ),
            remediation_steps=[
                "Audit the ETL cron schedule to confirm the fix is correct.",
                "Add a Grafana alert for sustained high CPU on sql-prod-03.",
                "Review change management for cron schedule modifications.",
            ],
        ),
        tags=["data-cleanup", "chat_reactions"],
        description="Teams chat transcript with emoji reactions around a CPU spike incident.",
    )


def _dc163_event_viewer_xml() -> EvalCase:
    """Windows Event Viewer XML export pasted in a ticket."""
    event_xml = (
        '<Event xmlns="http://schemas.microsoft.com/win/2004/08/events/event">\n'
        "  <System>\n"
        '    <Provider Name="Microsoft-Windows-Security-Auditing" Guid="{543496D1-...}"/>\n'
        "    <EventID>4625</EventID>\n"
        "    <Level>0</Level>\n"
        "    <Task>12544</Task>\n"
        "    <Keywords>0x8010000000000000</Keywords>\n"
        '    <TimeCreated SystemTime="2026-04-08T09:15:32.123Z"/>\n'
        '    <Computer>WS-CONTOSO-4421</Computer>\n'
        "  </System>\n"
        "  <EventData>\n"
        '    <Data Name="TargetUserName">jsmith</Data>\n'
        '    <Data Name="TargetDomainName">CONTOSO</Data>\n'
        '    <Data Name="Status">0xC000006D</Data>\n'
        '    <Data Name="SubStatus">0xC000006A</Data>\n'
        '    <Data Name="LogonType">10</Data>\n'
        '    <Data Name="IpAddress">10.0.3.47</Data>\n'
        "  </EventData>\n"
        "</Event>"
    )
    return EvalCase(
        ticket=EvalTicket(
            ticket_id="INC-DC-163",
            subject="Account lockout — Event Viewer log attached",
            description=(
                "My account (jsmith@contoso.com) keeps getting locked out every morning "
                "around 9 AM. I exported the failed logon events from Event Viewer:\n\n"
                f"{event_xml}\n\n"
                "There are about 50 of these Event ID 4625 entries each morning. The IP "
                "10.0.3.47 is not my workstation (mine is 10.0.3.22). Someone or something "
                "is trying to log in as me from a different machine."
            ),
            reporter=Reporter(
                name="John Smith",
                email="jsmith@contoso.com",
                department="Accounting",
            ),
            created_at="2026-04-08T14:00:00Z",
            channel=Channel.PORTAL,
        ),
        gold=GoldAnswer(
            ticket_id="INC-DC-163",
            category=Category.ACCESS_AUTH,
            priority=Priority.P2,
            assigned_team=Team.IAM,
            needs_escalation=True,
            missing_information=[MissingInfoField.AUTHENTICATION_METHOD],
            next_best_action=(
                "Investigate repeated failed logon attempts from an unknown IP — "
                "the Event Viewer XML export provides useful diagnostic data."
            ),
            remediation_steps=[
                "Identify the device at IP 10.0.3.47 causing the failed logons.",
                "Check for stale credentials in services or scheduled tasks on that machine.",
                "Temporarily increase the lockout threshold while investigating.",
            ],
        ),
        tags=["data-cleanup", "event_viewer_xml"],
        description="Windows Event Viewer XML export in an account lockout investigation.",
    )


def _dc164_docker_compose_logs() -> EvalCase:
    """Docker compose config and interleaved container logs."""
    compose_yaml = (
        "version: '3.8'\n"
        "services:\n"
        "  web:\n"
        "    image: contoso/web-app:3.2.1\n"
        "    ports: ['8080:8080']\n"
        "    depends_on: [db, redis]\n"
        "  db:\n"
        "    image: postgres:16\n"
        "    volumes: ['pgdata:/var/lib/postgresql/data']\n"
        "  redis:\n"
        "    image: redis:7-alpine\n"
    )
    logs = (
        "web_1   | 2026-04-08 09:00:01 INFO  Starting web-app v3.2.1\n"
        "db_1    | 2026-04-08 09:00:02 LOG   database system is ready\n"
        "redis_1 | 2026-04-08 09:00:01 * Ready to accept connections\n"
        "web_1   | 2026-04-08 09:00:05 ERROR Cannot connect to database: "
        "connection refused on port 5432\n"
        "web_1   | 2026-04-08 09:00:10 ERROR Retry 1/5 failed\n"
        "web_1   | 2026-04-08 09:00:15 ERROR Retry 2/5 failed\n"
        "web_1   | 2026-04-08 09:00:20 FATAL Max retries exceeded. Shutting down.\n"
    )
    return EvalCase(
        ticket=EvalTicket(
            ticket_id="INC-DC-164",
            subject="Docker web app can't connect to database after restart",
            description=(
                "After restarting our Docker Compose stack, the web app container "
                "can't reach the database. Here's our docker-compose.yml:\n\n"
                f"{compose_yaml}\n\n"
                f"And here are the logs:\n\n{logs}\n"
                "The database container starts but the web app tries to connect too early."
            ),
            reporter=Reporter(
                name="Tyler Brooks",
                email="tyler.brooks@contoso.com",
                department="Platform Engineering",
            ),
            created_at="2026-04-08T14:00:00Z",
            channel=Channel.PORTAL,
        ),
        gold=GoldAnswer(
            ticket_id="INC-DC-164",
            category=Category.SOFTWARE,
            priority=Priority.P2,
            assigned_team=Team.ENTERPRISE_APPS,
            needs_escalation=False,
            missing_information=[MissingInfoField.ENVIRONMENT_DETAILS],
            next_best_action=(
                "Fix the Docker Compose startup ordering issue — the web app "
                "needs a healthcheck-based dependency on the database."
            ),
            remediation_steps=[
                "Add a healthcheck to the db service in docker-compose.yml.",
                "Change web's depends_on to use condition: service_healthy.",
                "Increase the retry count/delay in the web app's DB connection logic.",
            ],
        ),
        tags=["data-cleanup", "docker_logs"],
        description="Docker Compose config and interleaved container logs in a startup issue.",
    )


def _dc165_smime_artifact() -> EvalCase:
    """S/MIME encrypted email body artifact in a support request."""
    smime_blob = (
        "Content-Type: application/pkcs7-mime; smime-type=enveloped-data;\n"
        '  name="smime.p7m"\n'
        "Content-Transfer-Encoding: base64\n"
        "Content-Disposition: attachment; filename=\"smime.p7m\"\n\n"
        "MIIBmgYJKoZIhvcNAQcDoIIBizCCAYcCAQAxggEhMIIBHQIBADAFMAACAQEw\n"
        "DQYJKoZIhvcNAQEBBQAEggEAfakeencrypteddatagoeshereanditisquitelong\n"
        "andwouldnormallybemuchlongerbutthisisademooftheformatusedins/mime==\n"
    )
    return EvalCase(
        ticket=EvalTicket(
            ticket_id="INC-DC-165",
            subject="Can't open encrypted emails from external partners",
            description=(
                "I receive S/MIME encrypted emails from our legal partners at "
                "Baker & McKenzie. When I try to open them in Outlook, I get:\n"
                "'Microsoft Outlook had problems decrypting this message.'\n\n"
                "Here's what the raw email looks like:\n\n"
                f"{smime_blob}\n"
                "My certificate (issued by Contoso Internal CA) expired last week. "
                "I think I need a new one."
            ),
            reporter=Reporter(
                name="Patricia Moore",
                email="patricia.moore@contoso.com",
                department="Legal",
            ),
            created_at="2026-04-08T14:00:00Z",
            channel=Channel.EMAIL,
        ),
        gold=GoldAnswer(
            ticket_id="INC-DC-165",
            category=Category.ACCESS_AUTH,
            priority=Priority.P2,
            assigned_team=Team.IAM,
            needs_escalation=False,
            missing_information=[],
            next_best_action=(
                "Renew the user's S/MIME certificate to restore encrypted email access — "
                "the PKCS#7 blob is the raw email artifact."
            ),
            remediation_steps=[
                "Issue a new S/MIME certificate from the Contoso Internal CA.",
                "Install the new certificate in the user's Outlook profile.",
                "Send a test encrypted email to verify decryption works.",
            ],
        ),
        tags=["data-cleanup", "smime_artifact"],
        description="S/MIME PKCS#7 encrypted blob in an email decryption failure ticket.",
    )


def _dc166_arm_template_json() -> EvalCase:
    """Azure ARM template JSON dump in a deployment failure ticket."""
    arm_fragment = (
        '{\n  "$schema": "https://schema.management.azure.com/schemas/2019-04-01/deploymentTemplate.json#",\n'
        '  "contentVersion": "1.0.0.0",\n'
        '  "resources": [\n'
        '    {\n'
        '      "type": "Microsoft.Compute/virtualMachines",\n'
        '      "apiVersion": "2023-09-01",\n'
        '      "name": "vm-prod-web-01",\n'
        '      "location": "[resourceGroup().location]",\n'
        '      "properties": {\n'
        '        "hardwareProfile": {"vmSize": "Standard_D4s_v5"},\n'
        '        "storageProfile": {\n'
        '          "imageReference": {\n'
        '            "publisher": "MicrosoftWindowsServer",\n'
        '            "offer": "WindowsServer",\n'
        '            "sku": "2022-datacenter-g2",\n'
        '            "version": "latest"\n'
        "          }\n"
        "        }\n"
        "      }\n"
        "    }\n"
        "  ]\n"
        "}"
    )
    return EvalCase(
        ticket=EvalTicket(
            ticket_id="INC-DC-166",
            subject="ARM template deployment fails — quota exceeded in East US",
            description=(
                "Our ARM template deployment for the new production web tier failed:\n\n"
                f"{arm_fragment}\n\n"
                "Error: 'OperationNotAllowed - Operation could not be completed as it results "
                "in exceeding approved Total Regional Cores quota.'\n\n"
                "We need 16 more vCPU cores in East US for 4x Standard_D4s_v5 VMs."
            ),
            reporter=Reporter(
                name="Nadia Petrova",
                email="nadia.petrova@contoso.com",
                department="Cloud Engineering",
            ),
            created_at="2026-04-08T14:00:00Z",
            channel=Channel.PORTAL,
        ),
        gold=GoldAnswer(
            ticket_id="INC-DC-166",
            category=Category.DATA_STORAGE,
            priority=Priority.P3,
            assigned_team=Team.DATA_PLATFORM,
            needs_escalation=False,
            missing_information=[MissingInfoField.BUSINESS_IMPACT],
            next_best_action=(
                "Request an Azure vCPU quota increase in East US — the ARM template "
                "JSON is context for the deployment failure."
            ),
            remediation_steps=[
                "Submit a quota increase request for the East US region via Azure Portal.",
                "Request 16 additional vCPU cores for the Dv5 series.",
                "Retry the ARM template deployment after quota approval.",
            ],
        ),
        tags=["data-cleanup", "arm_template"],
        description="Azure ARM template JSON dump in a quota exceeded deployment failure.",
    )


def _dc167_python_traceback_deep() -> EvalCase:
    """Very deep Python traceback with long module paths."""
    frames = "\n".join(
        [
            f'  File "/opt/contoso/venv/lib/python3.12/site-packages/'
            f'contoso_{mod}/services/{svc}/handlers/v2/{handler}.py", '
            f'line {100 + i * 7}, in {func}'
            for i, (mod, svc, handler, func) in enumerate([
                ("core", "auth", "token_validator", "validate_jwt"),
                ("core", "auth", "session_manager", "refresh_session"),
                ("middleware", "logging", "correlation_tracker", "track_request"),
                ("middleware", "rate_limit", "sliding_window", "check_rate"),
                ("api", "gateway", "request_router", "route_request"),
                ("api", "gateway", "response_handler", "format_response"),
                ("business", "ticketing", "ticket_processor", "process_ticket"),
                ("business", "ticketing", "sla_calculator", "compute_sla"),
                ("integrations", "jira", "sync_adapter", "sync_ticket"),
                ("integrations", "jira", "field_mapper", "map_custom_fields"),
            ])
        ]
    )
    return EvalCase(
        ticket=EvalTicket(
            ticket_id="INC-DC-167",
            subject="Production API 500 error — full traceback attached",
            description=(
                "Getting 500 errors on POST /api/v2/tickets. Full traceback:\n\n"
                f"Traceback (most recent call last):\n{frames}\n"
                "KeyError: 'custom_field_sprint_id'\n\n"
                "This started after we updated the Jira integration to API v3. "
                "The field mapping is missing the sprint_id custom field."
            ),
            reporter=Reporter(
                name="David Park",
                email="david.park@contoso.com",
                department="Backend Engineering",
            ),
            created_at="2026-04-08T14:00:00Z",
            channel=Channel.EMAIL,
        ),
        gold=GoldAnswer(
            ticket_id="INC-DC-167",
            category=Category.SOFTWARE,
            priority=Priority.P1,
            assigned_team=Team.ENTERPRISE_APPS,
            needs_escalation=True,
            missing_information=[MissingInfoField.ENVIRONMENT_DETAILS],
            next_best_action=(
                "Fix the missing sprint_id field mapping in the Jira v3 integration — "
                "the deep traceback provides the full call chain."
            ),
            remediation_steps=[
                "Add 'custom_field_sprint_id' to the Jira v3 field mapper.",
                "Deploy a hotfix since POST /api/v2/tickets is completely broken.",
                "Add integration tests for all custom field mappings.",
            ],
        ),
        tags=["data-cleanup", "deep_traceback"],
        description="10-frame Python traceback with very long module paths in a 500 error ticket.",
    )


def _dc168_jira_notification_noise() -> EvalCase:
    """Jira email notification template noise around a real issue."""
    jira_noise = (
        "--- Jira Notification ---\n"
        "Project: CONTOSO-INFRA\n"
        "Issue Type: Bug\n"
        "Priority: Major\n"
        "Status: Open\n"
        "Reporter: Jen Walsh\n"
        "Assignee: Unassigned\n"
        "Created: 2026-04-08T10:00:00Z\n"
        "Updated: 2026-04-08T10:00:00Z\n"
        "Labels: network, vpn, production\n"
        "Sprint: Sprint 24\n"
        "Fix Version: 3.9.0\n"
        "Components: Networking, Infrastructure\n"
        "Environment: Production - East US\n"
        "---\n"
        "Watchers: @team-infra, @team-networking, @sarah.chen, @mike.jones, "
        "@david.kim, @lisa.park, @tom.wilson\n"
        "---\n"
    )
    return EvalCase(
        ticket=EvalTicket(
            ticket_id="INC-DC-168",
            subject="[CONTOSO-INFRA-2847] VPN split tunnel not working for Teams",
            description=(
                f"{jira_noise}\n"
                "Microsoft Teams calls drop when connected to VPN (GlobalProtect 6.1.3). "
                "Split tunneling is supposed to exclude Teams/Office 365 traffic but "
                "it's routing everything through the tunnel. Latency jumps to 400ms.\n\n"
                "Affects all remote workers (approx. 200 users).\n\n"
                f"--- Do not reply above this line ---\n{jira_noise}"
            ),
            reporter=Reporter(
                name="Jennifer Walsh",
                email="jen.walsh@contoso.com",
                department="Infrastructure",
            ),
            created_at="2026-04-08T14:00:00Z",
            channel=Channel.EMAIL,
        ),
        gold=GoldAnswer(
            ticket_id="INC-DC-168",
            category=Category.NETWORK,
            priority=Priority.P2,
            assigned_team=Team.NETWORK_OPS,
            needs_escalation=False,
            missing_information=[MissingInfoField.NETWORK_LOCATION],
            next_best_action=(
                "Fix VPN split tunnel configuration for Teams/O365 traffic — "
                "the Jira notification metadata is template noise."
            ),
            remediation_steps=[
                "Update the GlobalProtect split tunnel exclusion list to include Teams IP ranges.",
                "Add the Office 365 FQDNs to the VPN exclude list.",
                "Test with a sample of remote users to confirm the fix.",
            ],
        ),
        tags=["data-cleanup", "jira_notification"],
        description="Jira notification template metadata wrapping a VPN split tunnel issue.",
    )


def _dc169_auto_translation_artifact() -> EvalCase:
    """Auto-translated ticket with translation artifacts and original text."""
    return EvalCase(
        ticket=EvalTicket(
            ticket_id="INC-DC-169",
            subject="[Auto-translated from Japanese] Computer slow / コンピュータが遅い",
            description=(
                "[This message was automatically translated from Japanese]\n"
                "[Translation confidence: 72%]\n"
                "[Original language: ja-JP]\n\n"
                "Computer of me is very slow from the morning of today. The application "
                "of Excel takes the time of 5 minutes to open the file. The memory "
                "(RAM) is using 95% according to the manager of tasks. I think "
                "the update of Windows that was installed the night of yesterday is "
                "the cause of.\n\n"
                "--- Original Message (ja-JP) ---\n"
                "今朝からコンピュータがとても遅いです。Excelのアプリケーションは"
                "ファイルを開くのに5分かかります。タスクマネージャーによると"
                "メモリ（RAM）が95%使用されています。昨夜インストールされた"
                "Windowsアップデートが原因だと思います。\n"
                "--- End Original ---"
            ),
            reporter=Reporter(
                name="Takeshi Yamamoto",
                email="takeshi.yamamoto@contoso.com",
                department="Tokyo Office",
            ),
            created_at="2026-04-08T14:00:00Z",
            channel=Channel.EMAIL,
        ),
        gold=GoldAnswer(
            ticket_id="INC-DC-169",
            category=Category.HARDWARE,
            priority=Priority.P3,
            assigned_team=Team.ENDPOINT,
            needs_escalation=False,
            missing_information=[MissingInfoField.DEVICE_INFO],
            next_best_action=(
                "Investigate high RAM usage and slow performance after Windows Update — "
                "the auto-translation artifacts don't affect triage."
            ),
            remediation_steps=[
                "Check Task Manager for the process consuming the most memory.",
                "Review which Windows Update was installed last night.",
                "If the update is the cause, uninstall it and defer until a fix is available.",
            ],
        ),
        tags=["data-cleanup", "auto_translation"],
        description="Auto-translated ticket from Japanese with translation artifacts and original text.",
    )


def _dc170_verbose_buried_issue() -> EvalCase:
    """Extremely verbose email with the actual issue buried in the middle."""
    filler_before = (
        "Good morning IT team!\n\n"
        "I hope everyone is having a wonderful Monday. The weather here in Chicago "
        "is beautiful — 72°F and sunny, perfect for the rooftop lunch we had last "
        "week. Speaking of which, the rooftop access card system was being a bit "
        "finicky, but that's a different story.\n\n"
        "I wanted to start by saying how much I appreciate the work you all did "
        "last quarter. The migration to the new ticketing system was incredibly "
        "smooth. My team had zero downtime, which was amazing. I told my manager "
        "about it at our last one-on-one and she was very impressed.\n\n"
        "Now, before I get to my actual issue, let me give you some background. "
        "Our team has been working on the Q2 financial forecasting project. We use "
        "a combination of Excel, Power BI, and a custom Python tool. The Python "
        "tool pulls data from our Azure SQL database and generates reports.\n\n"
    )
    actual_issue = (
        "Anyway, here's the thing — since Thursday, our Azure SQL database "
        "(sql-prod-finance-01.database.windows.net) has been timing out. "
        "Connection timeout after 30 seconds. Our Python scripts that ran in "
        "2 minutes now take 45 minutes or fail entirely. The Power BI dashboards "
        "show stale data from Thursday. This is blocking the entire Q2 forecast.\n\n"
    )
    filler_after = (
        "On a completely separate note, could you also look into why the coffee "
        "machine on Floor 4 requires a badge tap now? It didn't used to. Not "
        "urgent at all, just curious.\n\n"
        "Also, I heard there might be a new version of Teams coming out? My "
        "colleague mentioned it at lunch. If so, when will we get it?\n\n"
        "Thanks so much for everything! You're the best IT team I've ever worked "
        "with (and I've been at three companies). Have a great week!\n\n"
        "Best regards,\n"
        "Monica"
    )
    return EvalCase(
        ticket=EvalTicket(
            ticket_id="INC-DC-170",
            subject="Quick question and an issue",
            description=filler_before + actual_issue + filler_after,
            reporter=Reporter(
                name="Monica Rivera",
                email="monica.rivera@contoso.com",
                department="Finance",
            ),
            created_at="2026-04-08T14:00:00Z",
            channel=Channel.EMAIL,
        ),
        gold=GoldAnswer(
            ticket_id="INC-DC-170",
            category=Category.DATA_STORAGE,
            priority=Priority.P2,
            assigned_team=Team.DATA_PLATFORM,
            needs_escalation=False,
            missing_information=[MissingInfoField.ERROR_MESSAGE],
            next_best_action=(
                "Investigate Azure SQL timeouts on sql-prod-finance-01 blocking the "
                "Q2 forecast — the verbose email filler is noise."
            ),
            remediation_steps=[
                "Check Azure SQL database metrics for CPU, DTU, and connection counts since Thursday.",
                "Review query performance insights for blocking queries or deadlocks.",
                "Consider scaling up the database temporarily while root-causing the issue.",
            ],
        ),
        tags=["data-cleanup", "verbose_buried"],
        description="Extremely verbose email with the actual database timeout issue buried in the middle.",
    )


def build_dataset() -> EvalDataset:
    """Build and return the data-cleanup evaluation dataset (170 cases)."""
    return EvalDataset(
        name="data_cleanup",
        description=(
            "Tickets with noisy, malformed, or dirty input data.  Tests whether the triage "
            "system can correctly process tickets despite real-world data quality issues such "
            "as long email chains, embedded base64, HTML markup, mojibake, excessive whitespace, "
            "mixed languages, container logs, invisible Unicode, MIME boundaries, calendar "
            "metadata, NDR bounce-backs, PII leakage, GraphQL dumps, crash dumps, webhook "
            "payloads, PowerShell streams, Docker configs, OCR corruption, quoted-printable "
            "encoding, ITSM audit trails, Bloomberg terminal output, Excel formula artifacts, "
            "and other artefacts."
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
            _dc016_container_logs(),
            _dc017_xml_soap_payload(),
            _dc018_json_api_dump(),
            _dc019_git_diff_paste(),
            _dc020_invisible_unicode(),
            _dc021_rtl_bidi_text(),
            _dc022_ansi_control_chars(),
            _dc023_markdown_artifacts(),
            _dc024_spreadsheet_paste(),
            _dc025_yaml_config_dump(),
            _dc026_jwt_token_dump(),
            _dc027_auto_translation(),
            _dc028_voicemail_transcript(),
            _dc029_css_dark_mode_noise(),
            _dc030_concatenated_tickets(),
            _dc031_mime_boundaries(),
            _dc032_multiple_base64_images(),
            _dc033_ics_calendar_metadata(),
            _dc034_buried_issue_long_email(),
            _dc035_multilingual_disclaimers(),
            _dc036_ndr_bounce(),
            _dc037_regex_code_patterns(),
            _dc038_contradictory_replies(),
            _dc039_accidental_pii(),
            _dc040_base64_pdf_inline(),
            _dc041_zalgo_text(),
            _dc042_url_encoded_content(),
            _dc043_monitoring_alert_flood(),
            _dc044_sql_query_dump(),
            _dc045_certificate_leak(),
            _dc046_hex_dump(),
            _dc047_mixed_date_formats(),
            _dc048_financial_ticker_confusion(),
            _dc049_tcpdump_output(),
            _dc050_screen_reader_artifacts(),
            _dc051_graphql_introspection_dump(),
            _dc052_windows_minidump_output(),
            _dc053_webhook_payload_noise(),
            _dc054_powershell_mixed_streams(),
            _dc055_docker_compose_flood(),
            _dc056_ocr_financial_report(),
            _dc057_quoted_printable_encoding(),
            _dc058_servicenow_audit_trail(),
            _dc059_bloomberg_terminal_paste(),
            _dc060_excel_formula_artifacts(),
            _dc061_csv_spreadsheet_inline(),
            _dc062_tracking_url_noise(),
            _dc063_rtf_markup_artifacts(),
            _dc064_auto_reply_chain(),
            _dc065_svg_data_inline(),
            _dc066_cross_threaded_issues(),
            _dc067_massive_cc_list(),
            _dc068_env_var_dump(),
            _dc069_git_diff_markers(),
            _dc070_yaml_config_dump(),
            _dc071_very_long_email_buried_issue(),
            _dc072_base64_image_flood(),
            _dc073_base64_encoded_log(),
            _dc074_giant_signature(),
            _dc075_deep_reply_chain(),
            _dc076_severe_mojibake(),
            _dc077_json_config_dump(),
            _dc078_code_switching(),
            _dc079_url_spam(),
            _dc080_email_metadata_noise(),
            _dc081_pgp_signed_request(),
            _dc082_syslog_dump(),
            _dc083_tnef_winmail(),
            _dc084_kubectl_describe(),
            _dc085_grafana_json_alert(),
            _dc086_ics_calendar_event(),
            _dc087_broken_mime_boundary(),
            _dc088_mixed_encoding_mojibake(),
            _dc089_terraform_plan_output(),
            _dc090_stacked_signatures(),
            _dc091_unicode_escapes(),
            _dc092_ocr_scan(),
            _dc093_tracking_pixels_html(),
            _dc094_chat_transcript_timestamps(),
            _dc095_powerbi_dashboard_paste(),
            _dc096_servicenow_wrapper(),
            _dc097_long_sharepoint_urls(),
            _dc098_base64_css_data_uri(),
            _dc099_outlook_html_table(),
            _dc100_base64_woff_font(),
            _dc101_pgp_signed_docking_station(),
            _dc102_long_cc_bcc_outlook_crash(),
            _dc103_xml_soap_fault_sap_sync(),
            _dc104_k8s_pod_describe_crashloop(),
            _dc105_hex_dump_tls_handshake(),
            _dc106_mixed_encoding_wifi_drops(),
            _dc107_sql_results_data_corruption(),
            _dc108_multilingual_disclaimer_password(),
            _dc109_near_empty_monitor_issue(),
            _dc110_vuln_scanner_tls_cert_expiry(),
            _dc111_base64_pdf_inline(),
            _dc112_extremely_long_email(),
            _dc113_multiple_base64_images_flood(),
            _dc114_severe_mojibake(),
            _dc115_deep_email_quoting(),
            _dc116_giant_signature_block(),
            _dc117_url_spam_tracking_params(),
            _dc118_email_metadata_flood(),
            _dc119_git_diff_inline(),
            _dc120_kubectl_describe_pod(),
            _dc121_docker_compose_yaml_dump(),
            _dc122_jwt_oauth_token_dump(),
            _dc123_ansi_escape_codes(),
            _dc124_misaligned_spreadsheet_paste(),
            _dc125_zero_width_unicode(),
            _dc126_extremely_long_subject(),
            _dc127_svg_data_uri(),
            _dc128_prometheus_metrics_flood(),
            _dc129_systeminfo_dump(),
            _dc130_splunk_search_results(),
            _dc131_arm_bicep_template(),
            _dc132_csv_bulk_paste(),
            _dc133_codepage_mojibake(),
            _dc134_recursive_email_forward(),
            _dc135_pii_noise(),
            _dc136_csv_injection(),
            _dc137_gpg_signed(),
            _dc138_zalgo_combining(),
            _dc139_nested_json(),
            _dc140_sql_output(),
            _dc141_smime_signature(),
            _dc142_near_empty_iphone(),
            _dc143_jira_notification(),
            _dc144_registry_export(),
            _dc145_deep_traceback(),
            _dc146_long_tracking_urls(),
            _dc147_ooo_chain(),
            _dc148_base64_excel(),
            _dc149_terraform_dump(),
            _dc150_git_blame(),
            _dc151_rtl_arabic_zero_width(),
            _dc152_unicode_nfd_accents(),
            _dc153_base64_image_flood(),
            _dc154_deep_mime_nesting(),
            _dc155_csv_injection_formula(),
            _dc156_zalgo_combining_marks(),
            _dc157_hebrew_bidi_mixed(),
            _dc158_jenkins_ansi_codes(),
            _dc159_terraform_plan_dump(),
            _dc160_graphql_introspection(),
            _dc161_pgp_signed_email(),
            _dc162_teams_chat_reactions(),
            _dc163_event_viewer_xml(),
            _dc164_docker_compose_logs(),
            _dc165_smime_artifact(),
            _dc166_arm_template_json(),
            _dc167_python_traceback_deep(),
            _dc168_jira_notification_noise(),
            _dc169_auto_translation_artifact(),
            _dc170_verbose_buried_issue(),
        ],
    )


DATA_CLEANUP_DATASET: EvalDataset = build_dataset()
