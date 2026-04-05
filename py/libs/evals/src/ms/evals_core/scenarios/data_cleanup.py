# Copyright (c) Microsoft. All rights reserved.
"""Data cleanup evaluation scenarios.

Tests the triage API's ability to handle real-world messy input data:
long email threads, base64 images, HTML bodies, garbled encoding,
excessive signatures, pasted logs/CSV data, unicode overuse,
mixed-language content, minimal-info tickets, and system noise.
"""

from ms.evals_core.models.scenario import Scenario
from ms.evals_core.models.ticket import Reporter
from ms.evals_core.models.ticket import Ticket
from ms.evals_core.models.triage_decision import TriageDecision

# Base64-encoded image fragment used in embedded-image scenarios
_B64_PNG_FRAGMENT = (
    "iVBORw0KGgoAAAANSUhEUgAAAoAAAAHgCAYAAAA10dzkAAAACXBIWXMAAAsTAAALEwEAmpwYAAAK"
    "T2lDQ1BQaG90b3Nob3AgSUNDIHByb2ZpbGUAAHjanVNnVFPpFj333vRCS4iAlEtvUhUIIFJCi4AU"
    "kSYqIQkQSoghodkVUcERRUUEG8igiAOOjoCMFVEsDIoK2AfkIaKOg6OIisr74Xuja9a89+bN/rXX"
    "Pues852zzwfACAyWSDNRNYAMqUIeEeCDx8TG4eQuQIEKJHAAEAizZCFz/SMBAPh+PDwrIsAHvgAB"
    "eNMLCADATZvAMByH/w/qQplcAYCEAcB0kThLCIAUAEB6jkKmAEBGAYCdmCZTAKAEAGDLY2LjAFAt"
    "AGAnf+bTAICd+Jl7AQBblCEVAaCRACATZYhEAGg7AKzPVopFAFgwABRmS8Q5ANgtADBJV2ZIALC3"
    "AMDOEAuyAAgMADBRiIUpAAR7AGDIIyN4AISZABRG8lc88SuuEOcqAAB4mbI8uSQ5RYFbCC1xB1dX"
)

# Simulated base64-encoded log data
_B64_LOG_DATA = (
    "RVJST1IgMjAyNi0wMy0xOCAwOToxNToyMiBbQXV0aE1vZHVsZV0gRmFpbGVkIHRvIHZhbGlkYXRl"
    "IE1GQSB0b2tlbiBmb3IgdXNlciBzYXJhaC5jaGVuQGNvbnRvc28uY29tLiBUb2tlbiBleHBpcmVk"
    "IGF0IDIwMjYtMDMtMThUMDk6MTA6MDBaLiBSZXRyeSBjb3VudDogMy4gTW9kdWxlOiBBenVyZUFE"
)


def _build_long_email_thread() -> Scenario:
    """Very long email thread with multiple nested replies and signatures."""
    description_text = (
        "From: Sarah Mitchell <s.mitchell@contoso.com>\n"
        "To: IT Help Desk <helpdesk@contoso.com>\n"
        "Date: Wed, 18 Mar 2026 09:14:00 +0000\n"
        "Subject: Re: Re: Fwd: VPN Disconnection Issue - Urgent\n\n"
        "Hi team, just forwarding this again as we still haven't received a resolution. "
        "Please see the full thread below.\n\n"
        "Best regards,\n"
        "Sarah Mitchell\n"
        "Senior Trader | Equities Desk\n"
        "Contoso Financial Services\n"
        "Phone: +1 (212) 555-0147 | Fax: +1 (212) 555-0148\n"
        "Email: s.mitchell@contoso.com\n"
        "100 Wall Street, 24th Floor, New York, NY 10005\n"
        "www.contoso.com\n\n"
        "CONFIDENTIALITY NOTICE: This email and any attachments are for the exclusive "
        "and confidential use of the intended recipient. If you are not the intended "
        "recipient, please do not read, distribute, or take action based on this message.\n\n"
        "---\n\n"
        "> From: James Thornton <j.thornton@contoso.com>\n"
        "> Date: Tue, 17 Mar 2026 16:42:00 +0000\n"
        "> Subject: Re: Fwd: VPN Disconnection Issue - Urgent\n"
        ">\n"
        "> Sarah, I checked with the network team and they said they haven't seen any "
        "widespread issues. Can you try reconnecting using the alternate gateway? "
        "The address is vpn2.contoso.com. Let me know if that helps.\n"
        ">\n"
        "> Regards,\n"
        "> James Thornton\n"
        "> Network Operations Lead\n"
        "> Contoso Financial Services\n"
        "> Phone: +1 (212) 555-0199 | Mobile: +1 (917) 555-0123\n"
        ">\n"
        "> DISCLAIMER: The information contained in this communication is intended "
        "solely for the individual or entity to whom it is addressed.\n"
        ">\n"
        "> > From: Sarah Mitchell <s.mitchell@contoso.com>\n"
        "> > Date: Tue, 17 Mar 2026 14:30:00 +0000\n"
        "> > Subject: Re: VPN Disconnection Issue - Urgent\n"
        "> >\n"
        "> > James, the issue is getting worse. My VPN dropped THREE times in 20 minutes. "
        "The GlobalProtect client shows 'Connected' then suddenly switches to 'Disconnected' "
        "with error code GP-4017. Started after the weekend maintenance window. Laptop is "
        "Lenovo ThinkPad T14s running Windows 11 Enterprise, GlobalProtect version 6.1.3. "
        "I've already tried restarting the client, rebooting, and flushing DNS.\n"
        "> >\n"
        "> > This is critical — major trade window opening tomorrow.\n"
        "> >\n"
        "> > > From: James Thornton\n"
        "> > > Date: Tue, 17 Mar 2026 10:15:00 +0000\n"
        "> > >\n"
        "> > > Hi Sarah, can you confirm which VPN gateway you're connecting to?\n"
        "> > >\n"
        "> > > > From: Sarah Mitchell\n"
        "> > > > Date: Mon, 16 Mar 2026 17:05:00 +0000\n"
        "> > > > Subject: VPN Disconnection Issue\n"
        "> > > >\n"
        "> > > > Hi IT team, my VPN keeps disconnecting randomly. Started today.\n"
        "> > > > Very frustrating.\n"
        "> > > >\n"
        "> > > > Thanks,\n"
        "> > > > Sarah Mitchell\n"
        "> > > > Senior Trader | Equities Desk\n"
        "> > > > Contoso Financial Services\n"
        "> > > > Phone: +1 (212) 555-0147\n"
        "> > > >\n"
        "> > > > This email is confidential and may be legally privileged.\n"
    )
    return Scenario(
        ticket=Ticket(
            ticket_id="INC-5001",
            subject="Re: Re: Fwd: VPN Disconnection Issue - Urgent",
            description=description_text,
            reporter=Reporter(
                name="Sarah Mitchell",
                email="s.mitchell@contoso.com",
                department="Trading",
            ),
            created_at="2026-03-18T09:14:00Z",
            channel="email",
            attachments=[],
        ),
        gold=TriageDecision(
            ticket_id="INC-5001",
            category="Network & Connectivity",
            priority="P2",
            assigned_team="Network Operations",
            needs_escalation=False,
            missing_information=["network_location"],
            next_best_action=(
                "Investigate VPN gateway stability after weekend maintenance window "
                "and check GlobalProtect error code GP-4017 for known issues with version 6.1.3."
            ),
            remediation_steps=[
                "Check VPN gateway logs for errors during and after the maintenance window.",
                "Verify GlobalProtect v6.1.3 compatibility with the latest gateway firmware.",
                "Test connectivity from the alternate gateway vpn2.contoso.com.",
                "If issue persists, collect VPN client diagnostic logs and escalate to Palo Alto support.",
                "Confirm resolution with reporter and close ticket.",
            ],
        ),
        scenario_category="data_cleanup",
        scenario_tag="long_email_thread",
        description=(
            "Very long email thread with multiple nested replies, signatures, "
            "and disclaimers. Tests ability to extract the actual issue from noise."
        ),
    )


def _build_base64_image_in_body() -> Scenario:
    """Ticket description contains inline base64-encoded image data."""
    return Scenario(
        ticket=Ticket(
            ticket_id="INC-5002",
            subject="Broken monitor displaying vertical lines and flickering",
            description=(
                "My external monitor (Dell U2722D, asset tag CT-MN-08834) has been showing "
                "vertical colored lines and flickering intermittently since this morning. "
                "I've tried swapping the USB-C cable and using the DisplayPort connection "
                "but the issue persists.\n\n"
                "Here's a screenshot of the error: data:image/png;base64,"
                + _B64_PNG_FRAGMENT
                + "\n\n"
                "The lines appear to be about 2 pixels wide and are mostly green and magenta. "
                "The flickering happens every 10-15 seconds and lasts about 2 seconds each time. "
                "This is making it impossible to work on spreadsheets. Can someone from the "
                "hardware team come take a look? I'm on the 14th floor, desk 14-227."
            ),
            reporter=Reporter(
                name="David Chen",
                email="d.chen@contoso.com",
                department="Wealth Management",
            ),
            created_at="2026-03-18T10:22:00Z",
            channel="email",
            attachments=["monitor_issue.png"],
        ),
        gold=TriageDecision(
            ticket_id="INC-5002",
            category="Hardware & Peripherals",
            priority="P3",
            assigned_team="Endpoint Engineering",
            needs_escalation=False,
            missing_information=["device_info"],
            next_best_action=(
                "Dispatch technician to desk 14-227 to inspect Dell U2722D monitor "
                "for hardware failure — test with a known-good monitor to isolate the fault."
            ),
            remediation_steps=[
                "Verify the issue by testing with a known-good monitor at desk 14-227.",
                "Swap USB-C and DisplayPort cables with verified working replacements.",
                "If lines persist with new cables, test the laptop's video output on another display.",
                "If the monitor is confirmed faulty, initiate hardware replacement via Dell warranty.",
                "Confirm resolution with reporter and close ticket.",
            ],
        ),
        scenario_category="data_cleanup",
        scenario_tag="base64_image_inline",
        description=(
            "Ticket description contains an inline base64-encoded PNG image. "
            "Tests ability to parse around binary data without being confused by it."
        ),
    )


def _build_html_email_body() -> Scenario:
    """Ticket description is raw HTML from an email client."""
    return Scenario(
        ticket=Ticket(
            ticket_id="INC-5003",
            subject="SSO Login Failure - Cannot Access Finance Portal",
            description=(
                '<html>\n<head><meta http-equiv="Content-Type" content="text/html; '
                'charset=utf-8"></head>\n'
                '<body style="font-family: Calibri, Arial, sans-serif; font-size: 11pt;">\n'
                "<p>Hi IT Support Team,</p>\n"
                "<p>I have been <b>unable to log in</b> to the <b>Finance Reporting Portal</b> "
                "since this morning. When I try to authenticate through SSO, I get:</p>\n"
                '<table border="1" cellpadding="8">\n'
                '<tr><td><b>Error Code</b></td><td>AADSTS700016</td></tr>\n'
                "<tr><td><b>Message</b></td><td>Application with identifier "
                "'a3f8c92-1d4e-4b6a-9c87-2e5f1a3b7d90' was not found in the directory "
                "'contoso.com'</td></tr>\n"
                "<tr><td><b>Timestamp</b></td><td>2026-03-18 08:45:12 UTC</td></tr>\n"
                "</table>\n"
                "<p>I have tried clearing browser cache, InPrivate/Incognito mode, "
                "both Chrome and Edge. Same error every time.</p>\n"
                "<p>This is <u>blocking</u> our month-end close process. "
                "Could you please escalate this urgently?</p>\n"
                '<div style="border-top: 1px solid #ccc; margin-top: 20px;">\n'
                "<p><b>Rachel Goldstein</b></p>\n"
                "<p>Director, Financial Reporting</p>\n"
                "<p>Contoso Financial Services</p>\n"
                "<p>T: +1 (212) 555-0192</p>\n"
                "</div>\n</body>\n</html>"
            ),
            reporter=Reporter(
                name="Rachel Goldstein",
                email="r.goldstein@contoso.com",
                department="Finance",
            ),
            created_at="2026-03-18T08:52:00Z",
            channel="email",
            attachments=[],
        ),
        gold=TriageDecision(
            ticket_id="INC-5003",
            category="Access & Authentication",
            priority="P2",
            assigned_team="Identity & Access Management",
            needs_escalation=False,
            missing_information=["application_version"],
            next_best_action=(
                "Investigate AADSTS700016 error in Entra ID — the app registration "
                "for the Finance Reporting Portal may have been deleted or misconfigured."
            ),
            remediation_steps=[
                "Check Entra ID for the app registration with ID a3f8c92-1d4e-4b6a-9c87-2e5f1a3b7d90.",
                "If missing, restore from soft-delete or re-register the application.",
                "Verify SSO configuration matches the Finance Reporting Portal's expected settings.",
                "Test login with a service account to confirm the fix.",
                "Confirm resolution with reporter and close ticket.",
            ],
        ),
        scenario_category="data_cleanup",
        scenario_tag="html_email_body",
        description=(
            "Ticket body is raw HTML with styling, tables, and signatures. "
            "Tests ability to extract structured info from HTML markup."
        ),
    )


def _build_excessive_signature() -> Scenario:
    """Ticket with a short actual issue followed by enormous multi-language disclaimers."""
    return Scenario(
        ticket=Ticket(
            ticket_id="INC-5004",
            subject="Cannot upload documents to SharePoint Legal Library",
            description=(
                "I'm unable to upload any documents to the SharePoint Legal Library site. "
                "Every time I try to upload a file larger than 5MB, I get a generic error "
                'saying "Something went wrong." Smaller files seem to upload fine.\n\n'
                "---\n\n"
                "Philippe Durand\n"
                "Executive Vice President & Associate General Counsel\n"
                "Legal Department — Mergers & Acquisitions Division\n"
                "Contoso Financial Services Group, LLC\n\n"
                "Office: +1 (212) 555-0301\n"
                "Direct: +1 (212) 555-0302\n"
                "Mobile: +1 (917) 555-0303\n"
                "Fax: +1 (212) 555-0304\n"
                "Toll-Free: +1 (800) 555-0305\n\n"
                "Email: p.durand@contoso.com\n"
                "Website: https://www.contoso.com\n"
                "LinkedIn: https://www.linkedin.com/in/philippedurand\n\n"
                "Contoso Financial Services Group, LLC\n"
                "100 Wall Street, 30th Floor\n"
                "New York, NY 10005\n\n"
                "London Office: 25 Bank Street, Canary Wharf, London E14 5JP\n"
                "Singapore Office: 8 Marina Boulevard, #30-01, Singapore 018981\n\n"
                "═══════════════════════════════════════════════════\n\n"
                "CONFIDENTIALITY NOTICE: This email message, including any attachments, "
                "is for the sole use of the intended recipient(s) and may contain "
                "confidential, proprietary, and/or privileged information protected by law. "
                "If you are not the intended recipient, you may not use, copy, distribute, "
                "or disclose this message or its contents to anyone. Any unauthorized review, "
                "use, disclosure, or distribution is prohibited and may be unlawful.\n\n"
                "AVIS DE CONFIDENTIALITÉ : Ce message électronique, y compris les pièces "
                "jointes, est destiné exclusivement à l'usage du ou des destinataires prévus "
                "et peut contenir des informations confidentielles, propriétaires et/ou "
                "privilégiées protégées par la loi.\n\n"
                "VERTRAULICHKEITSHINWEIS: Diese E-Mail-Nachricht, einschließlich aller "
                "Anhänge, ist ausschließlich für den/die vorgesehenen Empfänger bestimmt "
                "und kann vertrauliche, geschützte und/oder privilegierte Informationen "
                "enthalten, die gesetzlich geschützt sind.\n\n"
                "ENVIRONMENTAL NOTICE: Please consider the environment before printing."
            ),
            reporter=Reporter(
                name="Philippe Durand",
                email="p.durand@contoso.com",
                department="Legal",
            ),
            created_at="2026-03-18T11:03:00Z",
            channel="email",
            attachments=["upload_error_screenshot.png"],
        ),
        gold=TriageDecision(
            ticket_id="INC-5004",
            category="Data & Storage",
            priority="P3",
            assigned_team="Data Platform",
            needs_escalation=False,
            missing_information=["error_message", "environment_details"],
            next_best_action=(
                "Investigate SharePoint Legal Library file size upload limits — "
                "check if a site-level or tenant-level upload quota is blocking files over 5MB."
            ),
            remediation_steps=[
                "Check SharePoint admin center for site-level storage quotas and upload size limits.",
                "Verify the Legal Library document library has no custom file size restrictions.",
                "Test uploading a 6MB file from a test account to isolate user vs. site-level issue.",
                "If quota-related, adjust the limit or request a storage increase.",
                "Confirm resolution with reporter and close ticket.",
            ],
        ),
        scenario_category="data_cleanup",
        scenario_tag="excessive_signature",
        description=(
            "Short actual issue followed by an enormous multi-language email signature "
            "and disclaimers. Tests ability to separate content from boilerplate."
        ),
    )


def _build_deep_reply_chain() -> Scenario:
    """Deep Re:/Fwd: chain where the latest message is a different issue from the thread."""
    return Scenario(
        ticket=Ticket(
            ticket_id="INC-5005",
            subject="Re: Re: Re: Re: Fwd: Re: SAP Error - Transaction SE16N Access Denied",
            description=(
                "Hi all — I'm now getting a completely new error in SAP. When I try to run "
                "transaction SE16N to query the BSEG table, I get: \"You are not authorized "
                "to use transaction SE16N (authorization object S_TCODE).\" This is different "
                "from the licensing issue we discussed last week. Can someone look into my "
                "authorization profile?\n\n"
                "— Karen\n\n"
                "On Tue, 17 Mar 2026 at 15:20, Robert Vasquez <r.vasquez@contoso.com> wrote:\n"
                "> Karen, the licensing issue has been resolved. Finance now has 45 concurrent "
                "SAP GUI licenses which should be more than enough.\n"
                ">\n"
                "> On Tue, 17 Mar 2026 at 11:40, Karen Whitfield wrote:\n"
                "> > Thanks Robert. So just to confirm — we do NOT need to upgrade to S/4HANA?\n"
                "> >\n"
                "> > On Mon, 16 Mar 2026, Robert Vasquez wrote:\n"
                "> > > No, this is purely a concurrent license count issue on ECC 6.0.\n"
                "> > >\n"
                "> > > On Mon, 16 Mar 2026, Michael Torres wrote:\n"
                "> > > > I believe we need to upgrade to S/4HANA. I've attached the roadmap.\n"
                "> > > >\n"
                "> > > > On Mon, 16 Mar 2026, Karen Whitfield wrote:\n"
                "> > > > > Multiple users in Finance getting 'License limit exceeded' errors.\n"
            ),
            reporter=Reporter(
                name="Karen Whitfield",
                email="k.whitfield@contoso.com",
                department="Finance",
            ),
            created_at="2026-03-18T09:45:00Z",
            channel="email",
            attachments=[],
        ),
        gold=TriageDecision(
            ticket_id="INC-5005",
            category="Software & Applications",
            priority="P3",
            assigned_team="Enterprise Applications",
            needs_escalation=False,
            missing_information=["affected_users", "environment_details"],
            next_best_action=(
                "Check the SAP authorization profile for Karen Whitfield — verify "
                "S_TCODE authorization object includes transaction SE16N."
            ),
            remediation_steps=[
                "Review Karen Whitfield's SAP role assignments in transaction SU01.",
                "Check if S_TCODE authorization object includes SE16N in her assigned roles.",
                "If missing, add the appropriate authorization via role modification in PFCG.",
                "Generate and apply the updated profile.",
                "Confirm the user can access SE16N and close ticket.",
            ],
        ),
        scenario_category="data_cleanup",
        scenario_tag="deep_reply_chain",
        description=(
            "Deep Re:/Fwd: chain where the latest message describes a NEW issue "
            "different from the original thread. Tests focus on the most recent message."
        ),
    )


def _build_garbled_encoding() -> Scenario:
    """Ticket with mojibake / garbled character encoding."""
    return Scenario(
        ticket=Ticket(
            ticket_id="INC-5006",
            subject="ProblÃ¨me avec l'imprimante - Ã©tage 12",
            description=(
                "Bonjour Ã©quipe IT,\n\n"
                "L'imprimante rÃ©seau au 12Ã¨me Ã©tage (modÃ¨le HP LaserJet Enterprise "
                "M609dn, Ã©tiquette d'actif CT-PR-04421) ne fonctionne plus depuis "
                "hier aprÃ¨s-midi. Quand j'essaie d'imprimer, le travail reste bloquÃ© "
                "dans la file d'attente et je reÃ§ois le message: \"Erreur PCL XL\" suivi "
                "de caractÃ¨res illisibles.\n\n"
                "J'ai essayÃ© de redÃ©marrer l'imprimante et de supprimer les travaux en "
                "attente, mais le problÃ¨me persiste. Plusieurs collÃ¨gues ont le mÃªme "
                "problÃ¨me.\n\n"
                "Merci de votre aide,\n"
                "AndrÃ© Lefebvre\n"
                "DÃ©partement Conformité"
            ),
            reporter=Reporter(
                name="André Lefebvre",
                email="a.lefebvre@contoso.com",
                department="Compliance",
            ),
            created_at="2026-03-18T08:30:00Z",
            channel="email",
            attachments=[],
        ),
        gold=TriageDecision(
            ticket_id="INC-5006",
            category="Hardware & Peripherals",
            priority="P3",
            assigned_team="Endpoint Engineering",
            needs_escalation=False,
            missing_information=["affected_users", "device_info"],
            next_best_action=(
                "Investigate PCL XL error on HP LaserJet Enterprise M609dn at floor 12 — "
                "likely a corrupt print driver or firmware issue."
            ),
            remediation_steps=[
                "Clear the print queue and restart the print spooler service on the print server.",
                "Check if the HP LaserJet M609dn firmware is up to date.",
                "Reinstall or update the PCL6 print driver on the affected workstations.",
                "Test printing a test page from the printer's control panel.",
                "Confirm resolution with reporter and close ticket.",
            ],
        ),
        scenario_category="data_cleanup",
        scenario_tag="garbled_encoding",
        description=(
            "Ticket with mojibake / garbled UTF-8 encoding (common when email clients "
            "mis-handle character sets). Tests robustness to encoding corruption."
        ),
    )


def _build_csv_log_dump() -> Scenario:
    """Ticket with CSV/log data pasted directly into the description."""
    return Scenario(
        ticket=Ticket(
            ticket_id="INC-5007",
            subject="Intermittent application crashes - log data attached",
            description=(
                "The Bloomberg Terminal keeps crashing for multiple traders. "
                "Here are the crash events from the event log:\n\n"
                "Timestamp,User,EventID,Source,Level,Description\n"
                "2026-03-18 08:01:15,j.williams,1000,Application Error,Error,"
                '"Faulting application name: blpterm.exe, version 2024.3.1.0, '
                'faulting module: ntdll.dll, exception code: 0xc0000005"\n'
                "2026-03-18 08:14:22,s.patel,1000,Application Error,Error,"
                '"Faulting application name: blpterm.exe, version 2024.3.1.0, '
                'faulting module: ntdll.dll, exception code: 0xc0000005"\n'
                "2026-03-18 08:32:41,m.chen,1000,Application Error,Error,"
                '"Faulting application name: blpterm.exe, version 2024.3.1.0, '
                'faulting module: msvcr140.dll, exception code: 0xc0000409"\n'
                "2026-03-18 08:45:03,j.williams,1000,Application Error,Error,"
                '"Faulting application name: blpterm.exe, version 2024.3.1.0, '
                'faulting module: ntdll.dll, exception code: 0xc0000005"\n'
                "2026-03-18 09:01:18,r.kim,1000,Application Error,Error,"
                '"Faulting application name: blpterm.exe, version 2024.3.1.0, '
                'faulting module: ntdll.dll, exception code: 0xc0000005"\n\n'
                "All traders are on the same Bloomberg Terminal version (2024.3.1.0). "
                "The crashes seem to happen during heavy market activity. "
                "This is impacting our ability to execute trades. Please investigate urgently."
            ),
            reporter=Reporter(
                name="James Williams",
                email="j.williams@contoso.com",
                department="Trading",
            ),
            created_at="2026-03-18T09:15:00Z",
            channel="portal",
            attachments=["event_log_export.csv"],
        ),
        gold=TriageDecision(
            ticket_id="INC-5007",
            category="Software & Applications",
            priority="P2",
            assigned_team="Enterprise Applications",
            needs_escalation=True,
            missing_information=["environment_details"],
            next_best_action=(
                "Investigate Bloomberg Terminal crash pattern affecting multiple traders — "
                "check for known issues with blpterm.exe v2024.3.1.0 and contact Bloomberg support."
            ),
            remediation_steps=[
                "Collect full crash dumps from affected workstations using Windows Event Viewer.",
                "Check Bloomberg support portal for known issues with version 2024.3.1.0.",
                "Verify all affected machines have identical OS patches and runtime libraries.",
                "If a patch is available, coordinate a rolling update during off-hours.",
                "Escalate to Bloomberg vendor support if crashes persist after patching.",
            ],
        ),
        scenario_category="data_cleanup",
        scenario_tag="csv_log_dump",
        description=(
            "Ticket with CSV-formatted event log data pasted into the body. "
            "Tests ability to parse structured data embedded in free text."
        ),
    )


def _build_unicode_emoji_overload() -> Scenario:
    """Ticket using excessive emojis and special Unicode characters."""
    return Scenario(
        ticket=Ticket(
            ticket_id="INC-5008",
            subject="🚨🚨🚨 WIFI NOT WORKING 🚨🚨🚨 PLEASE HELP 🙏🙏🙏",
            description=(
                "😡😡😡 SUPER FRUSTRATED right now!!! 😡😡😡\n\n"
                "The WiFi on the ENTIRE 8th floor has been down since 7:30am!!! ☠️☠️☠️\n\n"
                "✅ I tried restarting my laptop — didn't work\n"
                "✅ I tried connecting to the guest network — also down\n"
                "✅ My phone can't connect either 📱❌\n"
                "✅ Other people on floor 8 have the same problem 👥\n\n"
                "The access point nearest to my desk (AP-08-NW-03) has a solid red light 🔴 "
                "instead of the usual green 🟢\n\n"
                "I have THREE client presentations today 📊📊📊 and I CANNOT work without "
                "network access!!! This is ⭐⭐⭐⭐⭐ CRITICAL ⭐⭐⭐⭐⭐\n\n"
                "PLEASE FIX ASAP 🙏🙏🙏🙏🙏\n\n"
                "— Marcus Johnson 💼\n"
                "Floor 8, Desk 8-142 📍"
            ),
            reporter=Reporter(
                name="Marcus Johnson",
                email="m.johnson@contoso.com",
                department="Client Services",
            ),
            created_at="2026-03-18T07:45:00Z",
            channel="chat",
            attachments=[],
        ),
        gold=TriageDecision(
            ticket_id="INC-5008",
            category="Network & Connectivity",
            priority="P2",
            assigned_team="Network Operations",
            needs_escalation=False,
            missing_information=[],
            next_best_action=(
                "Investigate floor 8 WiFi outage — access point AP-08-NW-03 shows red "
                "status light indicating hardware or connectivity failure."
            ),
            remediation_steps=[
                "Check network management console for AP-08-NW-03 status and error logs.",
                "Verify PoE switch port feeding AP-08-NW-03 is operational.",
                "If the AP is offline, attempt remote reboot via controller.",
                "If unresponsive, dispatch a technician to inspect and replace the access point.",
                "Confirm WiFi restoration on floor 8 and close ticket.",
            ],
        ),
        scenario_category="data_cleanup",
        scenario_tag="unicode_emoji_overload",
        description=(
            "Ticket text overloaded with emojis and Unicode special characters. "
            "Tests ability to extract meaning from visually noisy input."
        ),
    )


def _build_repeated_content() -> Scenario:
    """Ticket where the user copy-pasted the same message multiple times."""
    return Scenario(
        ticket=Ticket(
            ticket_id="INC-5009",
            subject="Outlook keeps freezing Outlook keeps freezing Outlook keeps freezing",
            description=(
                "Outlook keeps freezing for 30-60 seconds whenever I try to open an email "
                "with attachments. I have to force close it from Task Manager.\n\n"
                "Outlook keeps freezing for 30-60 seconds whenever I try to open an email "
                "with attachments. I have to force close it from Task Manager.\n\n"
                "Outlook keeps freezing for 30-60 seconds whenever I try to open an email "
                "with attachments. I have to force close it from Task Manager.\n\n"
                "Sorry if this sent multiple times, the portal kept timing out when I tried "
                "to submit.\n\n"
                "Tom Barrett\nCompliance Department"
            ),
            reporter=Reporter(
                name="Tom Barrett",
                email="t.barrett@contoso.com",
                department="Compliance",
            ),
            created_at="2026-03-18T10:05:00Z",
            channel="portal",
            attachments=[],
        ),
        gold=TriageDecision(
            ticket_id="INC-5009",
            category="Software & Applications",
            priority="P3",
            assigned_team="Endpoint Engineering",
            needs_escalation=False,
            missing_information=[
                "application_version",
                "device_info",
                "environment_details",
            ],
            next_best_action=(
                "Investigate Outlook freezing when opening attachments — "
                "check add-ins, OST file integrity, and available disk space."
            ),
            remediation_steps=[
                "Run Outlook in safe mode (outlook.exe /safe) to rule out add-in conflicts.",
                "Check OST file size and run the Inbox Repair Tool (scanpst.exe).",
                "Verify available disk space and system memory.",
                "If Outlook is outdated, apply the latest Microsoft 365 updates.",
                "Confirm resolution with reporter and close ticket.",
            ],
        ),
        scenario_category="data_cleanup",
        scenario_tag="repeated_content",
        description=(
            "User accidentally submitted the same text multiple times. "
            "Tests deduplication and ability to identify the core issue."
        ),
    )


def _build_auto_generated_notification() -> Scenario:
    """System-generated notification that is not an actual support request."""
    return Scenario(
        ticket=Ticket(
            ticket_id="INC-5010",
            subject="[AUTO] Certificate Expiration Warning - *.contoso.com",
            description=(
                "────────────────────────────────────────────────\n"
                "  AUTOMATED ALERT — DO NOT REPLY TO THIS EMAIL\n"
                "────────────────────────────────────────────────\n\n"
                "Certificate Expiration Monitoring System\n"
                "Alert ID: CERT-2026-0318-0047\n"
                "Generated: 2026-03-18T06:00:00Z\n\n"
                "The following SSL/TLS certificate will expire soon:\n\n"
                "  Subject:     *.contoso.com\n"
                "  Issuer:      DigiCert Global G2 TLS RSA SHA256 2020 CA1\n"
                "  Serial:      0A:1B:2C:3D:4E:5F:6A:7B:8C:9D\n"
                "  Thumbprint:  A1B2C3D4E5F6A7B8C9D0E1F2A3B4C5D6E7F8A9B0\n"
                "  Valid From:  2025-03-20T00:00:00Z\n"
                "  Expires:     2026-03-20T23:59:59Z\n"
                "  Days Left:   2\n\n"
                "Affected Services:\n"
                "  - https://portal.contoso.com\n"
                "  - https://api.contoso.com\n"
                "  - https://mail.contoso.com\n\n"
                "ACTION REQUIRED: Renew this certificate before expiration to avoid "
                "service disruption.\n\n"
                "────────────────────────────────────────────────\n"
                "This is an automated message from the PKI Monitoring System.\n"
                "Contact: secops@contoso.com | Runbook: KB-SEC-0421\n"
                "────────────────────────────────────────────────"
            ),
            reporter=Reporter(
                name="PKI Monitoring System",
                email="pki-monitor@contoso.com",
                department="IT",
            ),
            created_at="2026-03-18T06:00:00Z",
            channel="email",
            attachments=[],
        ),
        gold=TriageDecision(
            ticket_id="INC-5010",
            category="Security & Compliance",
            priority="P1",
            assigned_team="Security Operations",
            needs_escalation=True,
            missing_information=[],
            next_best_action=(
                "Immediately renew the wildcard certificate for *.contoso.com — "
                "it expires in 2 days and affects portal, API, and mail services."
            ),
            remediation_steps=[
                "Generate a new CSR for *.contoso.com through the PKI management platform.",
                "Submit the renewal request to DigiCert via the enterprise portal.",
                "Once issued, deploy the new certificate to all affected services.",
                "Verify SSL connectivity to portal.contoso.com, api.contoso.com, and mail.contoso.com.",
                "Update the certificate monitoring system and close the alert.",
            ],
        ),
        scenario_category="data_cleanup",
        scenario_tag="auto_generated_notification",
        description=(
            "Automated system alert with structured formatting and metadata. "
            "Tests ability to handle machine-generated tickets that still require action."
        ),
    )


def _build_url_spam_tracking() -> Scenario:
    """Ticket with excessive URLs, tracking parameters, and pixel references."""
    return Scenario(
        ticket=Ticket(
            ticket_id="INC-5011",
            subject="Suspicious email with links - possible phishing",
            description=(
                "I received this email that looks suspicious. It has a lot of links and "
                "I'm not sure if it's legitimate. I did NOT click any of the links. "
                "Here's the content:\n\n"
                "---\n"
                "Subject: Your account has been compromised - immediate action required\n"
                "From: security-team@contoso-support.com\n\n"
                "Dear valued employee,\n\n"
                "We have detected unauthorized access to your account. Please verify your "
                "identity immediately by clicking the link below:\n\n"
                "https://contoso-support.com/verify?user=t.wright&token=a8f3c2e1-4b5d&"
                "redirect=https%3A%2F%2Fcontoso-support.com%2Faccount%2Fsettings%3F"
                "session%3D1234567890%26tracking%3Dutm_source%253Demail%2526utm_medium"
                "%253Dphish%2526utm_campaign%253Daccount_verify_2026\n\n"
                "If you do not verify within 24 hours, your account will be permanently "
                "locked.\n\n"
                "https://contoso-support.com/unsubscribe?id=fake123&ref=tracking456\n"
                "<img src='https://contoso-support.com/pixel.gif?uid=t.wright&open=1' "
                "width='1' height='1'>\n"
                "---\n\n"
                "The domain is contoso-support.com NOT contoso.com. "
                "This looks like a phishing attempt to me."
            ),
            reporter=Reporter(
                name="Thomas Wright",
                email="thomas.wright@contoso.com",
                department="Legal",
            ),
            created_at="2026-03-18T08:20:00Z",
            channel="portal",
            attachments=["suspicious_email.eml"],
        ),
        gold=TriageDecision(
            ticket_id="INC-5011",
            category="Security & Compliance",
            priority="P2",
            assigned_team="Security Operations",
            needs_escalation=True,
            missing_information=["affected_users"],
            next_best_action=(
                "Investigate phishing attempt from contoso-support.com targeting employees — "
                "block the domain in email security gateway and check if any users clicked the link."
            ),
            remediation_steps=[
                "Block contoso-support.com domain in the email security gateway.",
                "Search email logs for other recipients of the same phishing campaign.",
                "Check proxy logs for any users who accessed the phishing URL.",
                "If any users clicked the link, initiate credential reset and account review.",
                "Send a company-wide phishing awareness notification.",
            ],
        ),
        scenario_category="data_cleanup",
        scenario_tag="url_spam_tracking",
        description=(
            "Ticket reporting a phishing email, containing many URLs with tracking "
            "parameters, pixel trackers, and encoded query strings."
        ),
    )


def _build_mixed_languages() -> Scenario:
    """Ticket that code-switches between multiple languages."""
    return Scenario(
        ticket=Ticket(
            ticket_id="INC-5012",
            subject="问题 - OneDrive sync issue, ファイルが同期されない",
            description=(
                "Hi IT team,\n\n"
                "I'm having a OneDrive sync issue. 我的OneDrive已经两天没有同步了。"
                "The icon in the system tray shows a red X. ファイルを変更しても、"
                "変更がクラウドに反映されません。\n\n"
                "I've tried:\n"
                "- 重新启动OneDrive客户端 (restart the client)\n"
                "- 清除缓存 (clear cache)\n"
                "- OneDriveをリセット (reset OneDrive)\n\n"
                "Nothing worked. 这个问题影响了我的日常工作，because I can't access "
                "my files from other devices. とても困っています。\n\n"
                "Please help! 谢谢！ありがとう！\n\n"
                "Wei Chen / 陈伟\n"
                "Global Markets Division"
            ),
            reporter=Reporter(
                name="Wei Chen",
                email="w.chen@contoso.com",
                department="Trading",
            ),
            created_at="2026-03-18T09:30:00Z",
            channel="portal",
            attachments=[],
        ),
        gold=TriageDecision(
            ticket_id="INC-5012",
            category="Data & Storage",
            priority="P3",
            assigned_team="Data Platform",
            needs_escalation=False,
            missing_information=[
                "error_message",
                "environment_details",
                "application_version",
            ],
            next_best_action=(
                "Investigate OneDrive sync failure — check for known sync client issues, "
                "storage quota, and authentication token state."
            ),
            remediation_steps=[
                "Check OneDrive storage quota for the user account.",
                "Verify OneDrive sync client version and update if outdated.",
                "Reset OneDrive sync client using 'onedrive.exe /reset' command.",
                "Check for conflicting files or sync errors in the OneDrive activity center.",
                "Confirm sync resumes and verify from another device.",
            ],
        ),
        scenario_category="data_cleanup",
        scenario_tag="mixed_languages",
        description=(
            "Ticket that code-switches between English, Chinese, and Japanese. "
            "Tests ability to understand multilingual content."
        ),
    )


def _build_extremely_terse() -> Scenario:
    """Ticket with almost no useful information."""
    return Scenario(
        ticket=Ticket(
            ticket_id="INC-5013",
            subject="broken",
            description="it doesnt work anymore help pls",
            reporter=Reporter(
                name="Alex Turner",
                email="a.turner@contoso.com",
                department="HR",
            ),
            created_at="2026-03-18T11:45:00Z",
            channel="chat",
            attachments=[],
        ),
        gold=TriageDecision(
            ticket_id="INC-5013",
            category="General Inquiry",
            priority="P4",
            assigned_team="Endpoint Engineering",
            needs_escalation=False,
            missing_information=[
                "affected_system",
                "error_message",
                "steps_to_reproduce",
                "device_info",
                "timestamp",
            ],
            next_best_action=(
                "Contact the reporter to gather basic information about what system or "
                "application is not working and what error they are seeing."
            ),
            remediation_steps=[
                "Reach out to the reporter for clarification on which system or application is affected.",
                "Ask for the exact error message or behavior observed.",
                "Determine when the issue started and what changed.",
                "Once sufficient information is gathered, reassess category and priority.",
                "Route to the appropriate team based on clarified details.",
            ],
        ),
        scenario_category="data_cleanup",
        scenario_tag="extremely_terse",
        description=(
            "Extremely terse ticket with almost no actionable information. "
            "Tests handling of vague/minimal input."
        ),
    )


def _build_json_xml_dump() -> Scenario:
    """Ticket with raw JSON/XML error output pasted into the description."""
    return Scenario(
        ticket=Ticket(
            ticket_id="INC-5014",
            subject="API Integration Error - Salesforce to SAP",
            description=(
                "Our Salesforce-to-SAP integration is failing. Here's the error response "
                "from the middleware:\n\n"
                "```json\n"
                "{\n"
                '  "error": {\n'
                '    "code": "INTEGRATION_FAULT",\n'
                '    "message": "SAP RFC call failed: BAPI_SALESORDER_CREATEFROMDAT2",\n'
                '    "details": {\n'
                '      "sap_error_code": "V1-312",\n'
                '      "sap_error_message": "Sales organization 1000 distribution channel '
                '10 division 00 is not defined",\n'
                '      "rfc_module": "BAPI_SALESORDER_CREATEFROMDAT2",\n'
                '      "timestamp": "2026-03-18T09:42:15.332Z",\n'
                '      "correlation_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",\n'
                '      "source_system": "SF-PROD-01",\n'
                '      "target_system": "SAP-ECC-PROD",\n'
                '      "retry_count": 3,\n'
                '      "max_retries": 3\n'
                "    }\n"
                "  }\n"
                "}\n"
                "```\n\n"
                "And the XML payload that was sent:\n\n"
                "```xml\n"
                '<?xml version="1.0" encoding="UTF-8"?>\n'
                "<SalesOrder>\n"
                "  <Header>\n"
                "    <OrderType>ZOR</OrderType>\n"
                "    <SalesOrg>1000</SalesOrg>\n"
                "    <DistChannel>10</DistChannel>\n"
                "    <Division>00</Division>\n"
                "    <SoldToParty>0000100234</SoldToParty>\n"
                "  </Header>\n"
                "</SalesOrder>\n"
                "```\n\n"
                "This started after the SAP config migration yesterday. "
                "About 15 orders are stuck in the queue."
            ),
            reporter=Reporter(
                name="Priya Kapoor",
                email="p.kapoor@contoso.com",
                department="IT",
            ),
            created_at="2026-03-18T09:50:00Z",
            channel="portal",
            attachments=["integration_error_log.txt"],
        ),
        gold=TriageDecision(
            ticket_id="INC-5014",
            category="Software & Applications",
            priority="P2",
            assigned_team="Enterprise Applications",
            needs_escalation=True,
            missing_information=[],
            next_best_action=(
                "Investigate SAP sales organization configuration for org 1000 / "
                "channel 10 / division 00 — likely missing after the config migration yesterday."
            ),
            remediation_steps=[
                "Check SAP table TVKO for sales organization 1000 distribution channel 10 assignment.",
                "Verify the configuration migration completed successfully for all org structures.",
                "If the assignment is missing, recreate it in transaction SPRO.",
                "Reprocess the 15 stuck orders from the middleware queue.",
                "Monitor the integration for 24 hours to confirm stability.",
            ],
        ),
        scenario_category="data_cleanup",
        scenario_tag="json_xml_dump",
        description=(
            "Ticket with raw JSON and XML error output pasted into the description. "
            "Tests ability to parse structured data formats within free text."
        ),
    )


def _build_email_metadata_noise() -> Scenario:
    """Ticket with excessive email headers and metadata before the actual content."""
    return Scenario(
        ticket=Ticket(
            ticket_id="INC-5015",
            subject="MFA token not working - cannot authenticate",
            description=(
                "Return-Path: <l.chang@contoso.com>\n"
                "Received: from mail-ej1-f54.contoso.com (mail-ej1-f54.contoso.com "
                "[209.85.218.54])\n"
                "        by mx.contoso.com (Postfix) with ESMTPS id 4F7B2C1A3D\n"
                "        for <helpdesk@contoso.com>; Wed, 18 Mar 2026 11:30:02 +0000\n"
                "DKIM-Signature: v=1; a=rsa-sha256; c=relaxed/relaxed;\n"
                "        d=contoso.com; s=selector1;\n"
                "        h=from:to:cc:subject:date:message-id:content-type;\n"
                "        bh=47DEQpj8HBSa+/TImW+5JCeuQeRkm5NMpJWZG3hSuFU=;\n"
                "        b=dGhpcyBpcyBub3QgYSByZWFsIERLSU0gc2lnbmF0dXJl\n"
                "From: Lisa Chang <l.chang@contoso.com>\n"
                "To: IT Help Desk <helpdesk@contoso.com>\n"
                "Date: Wed, 18 Mar 2026 11:30:00 +0000\n"
                "MIME-Version: 1.0\n"
                "Content-Type: multipart/alternative; "
                'boundary="000000000000abcdef123456"\n'
                "X-Mailer: Microsoft Outlook 16.0\n"
                "X-Originating-IP: 10.22.15.108\n"
                "X-MS-Exchange-Organization-SCL: -1\n\n"
                "Hi,\n\n"
                "My MFA token is not working. Every time I try to log in, I enter the "
                "6-digit code from my Microsoft Authenticator app and it says "
                '"Verification failed. Please try again." I\'ve tried multiple times '
                "and the code changes every 30 seconds but none of them work. I think "
                "the time on my phone might be out of sync, or my MFA registration got "
                "corrupted somehow.\n\n"
                "Can you please reset my MFA so I can re-register? My username is "
                "l.chang@contoso.com and I'm currently locked out of all systems.\n\n"
                "Thanks,\nLisa Chang\nTrading Desk — Fixed Income"
            ),
            reporter=Reporter(
                name="Lisa Chang",
                email="l.chang@contoso.com",
                department="Trading",
            ),
            created_at="2026-03-18T11:30:00Z",
            channel="email",
            attachments=[],
        ),
        gold=TriageDecision(
            ticket_id="INC-5015",
            category="Access & Authentication",
            priority="P2",
            assigned_team="Identity & Access Management",
            needs_escalation=False,
            missing_information=["device_info", "authentication_method"],
            next_best_action=(
                "Reset MFA registration for l.chang@contoso.com in Entra ID — "
                "likely a time sync issue on the Authenticator app."
            ),
            remediation_steps=[
                "Reset the user's MFA registration in the Entra ID MFA management portal.",
                "Guide the user through re-registering Microsoft Authenticator.",
                "Verify phone time sync settings (Settings > Date & Time > Automatic).",
                "Test login with the newly registered MFA token.",
                "Confirm access to all systems is restored and close ticket.",
            ],
        ),
        scenario_category="data_cleanup",
        scenario_tag="email_metadata_noise",
        description=(
            "Ticket with excessive email headers (DKIM, Received, X-headers) "
            "before the actual issue. Tests filtering of email transport metadata."
        ),
    )


def _build_base64_log_attachment() -> Scenario:
    """Ticket with base64-encoded log data pasted into the description."""
    return Scenario(
        ticket=Ticket(
            ticket_id="INC-5016",
            subject="Authentication failures in production - encoded logs attached",
            description=(
                "We're seeing intermittent authentication failures in the production "
                "environment. I've exported the relevant log entries and encoded them "
                "for safe transport:\n\n"
                "Base64 encoded error log:\n"
                + _B64_LOG_DATA
                + "\n\n"
                "The decoded content shows TOTP validation failures for multiple users. "
                "This has been happening since the Entra ID sync at 3 AM. "
                "About 20 users are affected across Trading and Compliance departments.\n\n"
                "Additional diagnostic data (base64):\n"
                "eyJlcnJvcl9jb2RlIjoiQUFEU1RTNTAwMTQiLCJ0aW1lc3RhbXAiOiIyMDI2LTAzLTE4V"
                "DA5OjE1OjIyWiIsImFmZmVjdGVkX3VzZXJzIjoyMCwiY29ycmVsYXRpb25faWQiOiJhOGY"
                "zYzJlMS00YjVkIn0=\n\n"
                "Please investigate urgently. The trading desk cannot operate without "
                "authentication working."
            ),
            reporter=Reporter(
                name="System Operations Team",
                email="sysops@contoso.com",
                department="IT",
            ),
            created_at="2026-03-18T09:20:00Z",
            channel="portal",
            attachments=["auth_failure_logs.b64"],
        ),
        gold=TriageDecision(
            ticket_id="INC-5016",
            category="Access & Authentication",
            priority="P1",
            assigned_team="Identity & Access Management",
            needs_escalation=True,
            missing_information=[],
            next_best_action=(
                "Investigate Entra ID authentication failures affecting 20 users since "
                "the 3 AM sync — check AADSTS50014 error and TOTP validation pipeline."
            ),
            remediation_steps=[
                "Check Entra ID sign-in logs for AADSTS50014 errors since 03:00 UTC.",
                "Review the 3 AM directory sync job for errors or configuration changes.",
                "Verify Entra ID MFA service health in the Azure admin portal.",
                "If a sync issue, roll back the problematic changes and re-sync.",
                "Confirm authentication is restored for all affected users.",
            ],
        ),
        scenario_category="data_cleanup",
        scenario_tag="base64_log_attachment",
        description=(
            "Ticket with multiple blocks of base64-encoded diagnostic data "
            "pasted into the description. Tests resilience to encoded binary content."
        ),
    )


def get_data_cleanup_scenarios() -> list[Scenario]:
    """Return all data cleanup evaluation scenarios."""
    return [
        _build_long_email_thread(),
        _build_base64_image_in_body(),
        _build_html_email_body(),
        _build_excessive_signature(),
        _build_deep_reply_chain(),
        _build_garbled_encoding(),
        _build_csv_log_dump(),
        _build_unicode_emoji_overload(),
        _build_repeated_content(),
        _build_auto_generated_notification(),
        _build_url_spam_tracking(),
        _build_mixed_languages(),
        _build_extremely_terse(),
        _build_json_xml_dump(),
        _build_email_metadata_noise(),
        _build_base64_log_attachment(),
    ]
