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
            "Ticket contains three separate base64-encoded inline images "
            "interspersed with network issue details."
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
        description=(
            "Short hardware issue buried under legal disclaimers repeated in eight languages."
        ),
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
        description=(
            "Non-Delivery Report wrapping the original email about a shared mailbox delivery failure."
        ),
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
                r"   ^(?:TRD|SWP|FUT)-\d{4}-[A-Z]{2,4}\/\d{2,6}(?:\.\d+)?$" "\n"
                "2. The SQL query that fails (from the app logs):\n"
                "   SELECT t.trade_id, t.counterparty, t.notional FROM trades t\n"
                "   WHERE t.trade_id ~ '^(?:TRD|SWP|FUT)-\\d{4}' AND t.status <> 'CANCELLED'\n"
                "   AND t.book_date BETWEEN '2026-01-01' AND '2026-04-07'\n"
                "   ORDER BY t.book_date DESC LIMIT 500;\n"
                "3. Characters that trigger the crash: backslash (\\), pipe (|), curly "
                "braces ({}), and the caret (^) when combined with brackets []\n"
                "4. Stack trace excerpt:\n"
                "   java.util.regex.PatternSyntaxException: Unclosed group near index 42\n"
                r"     ^(?:TRD|SWP|FUT)-\d{4}-[A-Z]{2,4}\/\d{2,6}(?:\.\d+" "\n"
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


# ---------------------------------------------------------------------------
# Public API
# ---------------------------------------------------------------------------


def build_dataset() -> EvalDataset:
    """Build and return the data-cleanup evaluation dataset (40 cases)."""
    return EvalDataset(
        name="data_cleanup",
        description=(
            "Tickets with noisy, malformed, or dirty input data.  Tests whether the triage "
            "system can correctly process tickets despite real-world data quality issues such "
            "as long email chains, embedded base64, HTML markup, mojibake, excessive whitespace, "
            "mixed languages, container logs, invisible Unicode, MIME boundaries, calendar "
            "metadata, NDR bounce-backs, PII leakage, and other artefacts."
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
        ],
    )


DATA_CLEANUP_DATASET: EvalDataset = build_dataset()
