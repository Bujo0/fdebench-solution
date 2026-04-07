# Copyright (c) Microsoft. All rights reserved.
"""Extended data cleanup evaluation scenarios (dc-151 through dc-170).

These scenarios stress-test the triage API's resilience against additional
categories of noisy, malformed, or adversarial data quality issues found
in enterprise IT ticket systems, including:
- Extremely long emails with excessive base64 image payloads
- MIME multipart boundary artifacts
- Mojibake / corrupted character encoding
- Invisible Unicode characters and zero-width spaces
- Bidirectional text mixing (RTL + LTR)
- Massive inline SVG content
- Duplicated/looped content
- URL-encoded ticket bodies
- Embedded calendar invites (ICS)
- Raw hex / memory dump content
- Windows Event Log XML dumps
- Markdown with code fences
"""

from ms.evals_core.framework.models.scenario import EvalReporter
from ms.evals_core.framework.models.scenario import EvalScenario
from ms.evals_core.framework.models.scenario import EvalTicket
from ms.evals_core.framework.models.scenario import ExpectedTriage
from ms.evals_core.framework.models.scenario import ScenarioCategory
from ms.evals_core.framework.scenarios.registry import default_registry

_CATEGORY = ScenarioCategory.DATA_CLEANUP


def _reporter(name: str, email: str, department: str) -> EvalReporter:
    return EvalReporter(name=name, email=email, department=department)


# ---------------------------------------------------------------------------
# dc-151: Extremely long email with multiple base64 image payloads
# ---------------------------------------------------------------------------
_BASE64_BLOCK = (
    "iVBORw0KGgoAAAANSUhEUgAAAGAAAABgCAYAAADimHc4AAAAAXNSR0IArs4c6QAAAARn"
    "QU1BAACxjwv8YQUAAAAJcEhZcwAADsMAAA7DAcdvqGQAAAGdSURBVHhe7dAxAQAACMCg"
)

_LONG_BASE64_IMAGES = "\n\n".join(
    f"[Inline image {i}]\ndata:image/png;base64,{_BASE64_BLOCK * 20}\n" for i in range(1, 16)
)

default_registry.register(
    EvalScenario(
        scenario_id="dc-151",
        name="Extremely long email with multiple base64 image payloads",
        description=(
            "Email contains 15 inline base64-encoded screenshots, totaling ~30KB of "
            "noise. The actual VPN issue is split across the first and last paragraphs."
        ),
        category=_CATEGORY,
        tags=["base64_flood", "long_content", "image_heavy"],
        ticket=EvalTicket(
            ticket_id="INC-5151",
            subject="VPN keeps disconnecting — screenshots of every error attached",
            description=(
                "Hi IT,\n\n"
                "My VPN (GlobalProtect 6.1) keeps dropping during market hours. "
                "I took screenshots of every single error popup. Here they are:\n\n"
                + _LONG_BASE64_IMAGES
                + "\n\nAs you can see from all 15 screenshots, the error code is "
                "GP-4017 every time. This only happens on Wi-Fi, not Ethernet. "
                "I am on Floor 12, Building A, NYC office. Lenovo ThinkPad X1 "
                "Carbon Gen 11, Windows 11 23H2.\n\n"
                "Regards,\nAnthony Rizzo\nFixed Income Trading"
            ),
            reporter=_reporter("Anthony Rizzo", "a.rizzo@contoso.com", "Fixed Income Trading"),
            created_at="2026-03-18T09:30:00Z",
            channel="email",
        ),
        expected_triage=ExpectedTriage(
            category="Network & Connectivity",
            priority="P2",
            assigned_team="Network Operations",
        ),
    )
)


# ---------------------------------------------------------------------------
# dc-152: MIME multipart boundary artifacts in email body
# ---------------------------------------------------------------------------
default_registry.register(
    EvalScenario(
        scenario_id="dc-152",
        name="MIME multipart boundary artifacts in body",
        description=(
            "Email content includes raw MIME multipart boundaries, headers, and "
            "Content-Type declarations that were not stripped by the ingestion pipeline."
        ),
        category=_CATEGORY,
        tags=["mime_artifacts", "email_parsing", "raw_headers"],
        ticket=EvalTicket(
            ticket_id="INC-5152",
            subject="Cannot access shared drive after password change",
            description=(
                "MIME-Version: 1.0\n"
                "Content-Type: multipart/mixed; "
                'boundary="----=_Part_12345_67890.1710756000000"\n\n'
                "------=_Part_12345_67890.1710756000000\n"
                "Content-Type: text/plain; charset=UTF-8\n"
                "Content-Transfer-Encoding: quoted-printable\n\n"
                "Hi Help Desk,\n\n"
                "After changing my Active Directory password this morning, I can no=20\n"
                "longer access the \\\\contoso-fs01\\finance$ shared drive. I get an=20\n"
                "error: =E2=80=9CThe specified network password is not correct.=E2=80=9D=\n"
                "=20\n\n"
                "I=E2=80=99ve tried logging out and back in. My Outlook and Teams work=20\n"
                "fine with the new password. It=E2=80=99s only the mapped drive (F:) that=\n"
                "=20fails. Windows 11 credential manager still shows the old entry.\n\n"
                "------=_Part_12345_67890.1710756000000\n"
                'Content-Type: image/png; name="error_screenshot.png"\n'
                'Content-Disposition: attachment; filename="error_screenshot.png"\n'
                "Content-Transfer-Encoding: base64\n\n"
                f"{_BASE64_BLOCK * 5}\n\n"
                "------=_Part_12345_67890.1710756000000--\n\n"
                "Thanks,\nRobert Chen\nFinancial Reporting"
            ),
            reporter=_reporter("Robert Chen", "r.chen@contoso.com", "Financial Reporting"),
            created_at="2026-03-18T10:15:00Z",
            channel="email",
        ),
        expected_triage=ExpectedTriage(
            category="Access & Authentication",
            priority="P2",
            assigned_team="Identity & Access Management",
        ),
    )
)


# ---------------------------------------------------------------------------
# dc-153: Mojibake / corrupted character encoding
# ---------------------------------------------------------------------------
default_registry.register(
    EvalScenario(
        scenario_id="dc-153",
        name="Mojibake — corrupted character encoding",
        description=(
            "Email body has classic UTF-8 content decoded as Windows-1252, producing "
            "mojibake artifacts (â€™, â€œ, Ã©, etc.) throughout the text."
        ),
        category=_CATEGORY,
        tags=["mojibake", "encoding_corruption", "unicode"],
        ticket=EvalTicket(
            ticket_id="INC-5153",
            subject="Canâ€™t print to the 3rd floor printer",
            description=(
                "Hi IT,\n\n"
                "I canâ€™t print to the HP LaserJet on the 3rd floor. Every time "
                "I try to print, I get the error â€œDriver unavailableâ€\u009d. "
                "I checked the printer propertiesÂ and it says â€œOfflineâ€\u009d "
                "even though the printer LCD shows â€œReadyâ€\u009d.\n\n"
                "Iâ€™ve tried removing and re-adding the printer. The IP is "
                "10.40.3.25. My laptopÂ is a Dell Latitude 5540 running Windows "
                "11 EnterpriseÂ 23H2.\n\n"
                "The printer workedÂ fine until last Fridayâ€™s Windows Update "
                "(KB5035853). Other people onÂ the floor haveÂ the same issue.\n\n"
                "RÃ©gards,\nFranÃ§ois Dubois\nRisk Analytics"
            ),
            reporter=_reporter("François Dubois", "f.dubois@contoso.com", "Risk Analytics"),
            created_at="2026-03-18T11:00:00Z",
            channel="email",
        ),
        expected_triage=ExpectedTriage(
            category="Hardware & Peripherals",
            priority="P3",
            assigned_team="Endpoint Engineering",
        ),
    )
)


# ---------------------------------------------------------------------------
# dc-154: Invisible Unicode characters and zero-width spaces
# ---------------------------------------------------------------------------
default_registry.register(
    EvalScenario(
        scenario_id="dc-154",
        name="Invisible Unicode characters and zero-width spaces",
        description=(
            "Ticket description contains zero-width spaces (U+200B), zero-width "
            "joiners (U+200D), word joiners (U+2060), and byte-order marks (U+FEFF) "
            "interspersed throughout otherwise normal text."
        ),
        category=_CATEGORY,
        tags=["invisible_unicode", "zero_width", "steganographic"],
        ticket=EvalTicket(
            ticket_id="INC-5154",
            subject="Out\u200blook cal\u200bendar not\u200b syncing",
            description=(
                "\ufeffHi\u200b IT\u200b Team,\u200b\n\n"
                "My\u200b Out\u200blook\u200b cal\u200bendar\u200b has\u200b "
                "stop\u200bped\u200b sync\u200bing\u200b between\u200b my\u200b "
                "laptop\u200b and\u200b my\u200b iPhone.\u200b Meet\u200bings\u200b "
                "I\u200b accept\u200b on\u200b one\u200b device\u200b don\u2019t\u200b "
                "appear\u200b on\u200b the\u200b other.\u200b\n\n"
                "I\u2019m\u200b running\u200b Outlook\u200b 16.0.18025.20160\u200b "
                "on\u200b Windows\u200b 11.\u200b My\u200b iPhone\u200b is\u200b "
                "on\u200b iOS\u200b 17.4.\u200b The\u200b issue\u200b started\u200b "
                "after\u200b Thursday\u2019s\u200b Outlook\u200b update.\u200b\n\n"
                "I\u2019ve\u200b tried:\u200b\n"
                "- Re\u200bmoving\u200b and\u200b re-adding\u200b the\u200b "
                "Exchange\u200b account\u200b on\u200b my\u200b phone\u200b\n"
                "- Clearing\u200b the\u200b Outlook\u200b cache\u200b\n"
                "- Restarting\u200b both\u200b devices\u200b\n\n"
                "None\u200b of\u200b that\u200b worked.\u200b\n\n"
                "Thanks,\u200b\n"
                "Sandra\u200b Liu\u200b\n"
                "HR\u200b Department\u200b"
            ),
            reporter=_reporter("Sandra Liu", "s.liu@contoso.com", "HR"),
            created_at="2026-03-18T08:45:00Z",
            channel="portal",
        ),
        expected_triage=ExpectedTriage(
            category="Software & Applications",
            priority="P3",
            assigned_team="Enterprise Applications",
        ),
    )
)


# ---------------------------------------------------------------------------
# dc-155: Bidirectional text (RTL Arabic + LTR English mixed)
# ---------------------------------------------------------------------------
default_registry.register(
    EvalScenario(
        scenario_id="dc-155",
        name="Bidirectional text — Arabic and English mixed",
        description=(
            "Ticket mixes right-to-left Arabic text with left-to-right English, "
            "including RTL override characters that can confuse text processing."
        ),
        category=_CATEGORY,
        tags=["bidi_text", "rtl_ltr_mix", "multilingual"],
        ticket=EvalTicket(
            ticket_id="INC-5155",
            subject="مشكلة في الطابعة - Printer issue Floor 7",
            description=(
                "مرحبا فريق الدعم التقني,\n\n"
                "Hello IT team,\n\n"
                "الطابعة في الطابق السابع لا تعمل. "
                "The printer on Floor 7 (HP LaserJet Pro M428fdn, asset tag WM-PRN-0721) "
                "is not printing. \u202eRFLOOR 7 PRINTER DOWN\u202c\n\n"
                "عندما أرسل مهمة طباعة، تظهر رسالة خطأ: "
                '"PCL XL error - IllegalOperatorSequence"\n\n'
                "I have tried:\n"
                "- إعادة تشغيل الطابعة (restarting the printer)\n"
                "- مسح قائمة الانتظار (clearing the print queue)\n"
                "- تحديث برنامج التشغيل (updating the driver)\n\n"
                "لا شيء نجح. هذا يؤثر على 15 شخصا في قسمنا. "
                "Nothing worked. This affects 15 people in our department.\n\n"
                "شكرا,\nAhmed Al-Rashidi\nأحمد الراشدي\n"
                "Compliance | Floor 7"
            ),
            reporter=_reporter("Ahmed Al-Rashidi", "a.alrashidi@contoso.com", "Compliance"),
            created_at="2026-03-18T09:20:00Z",
            channel="email",
        ),
        expected_triage=ExpectedTriage(
            category="Hardware & Peripherals",
            priority="P2",
            assigned_team="Endpoint Engineering",
        ),
    )
)


# ---------------------------------------------------------------------------
# dc-156: URL-encoded ticket body
# ---------------------------------------------------------------------------
default_registry.register(
    EvalScenario(
        scenario_id="dc-156",
        name="URL-encoded ticket body",
        description=(
            "Ticket body appears to be URL-encoded, with %20, %0A, %27 etc. "
            "throughout, likely from a poorly implemented web form submission."
        ),
        category=_CATEGORY,
        tags=["url_encoded", "form_artifact", "encoding"],
        ticket=EvalTicket(
            ticket_id="INC-5156",
            subject="VPN%20connection%20keeps%20dropping",
            description=(
                "subject%3DVPN%20connection%20keeps%20dropping"
                "%26description%3DHi%20IT%20team%2C%0A%0A"
                "My%20VPN%20%28GlobalProtect%29%20has%20been%20"
                "disconnecting%20every%2015-20%20minutes%20since%20"
                "Monday%20morning.%20I%27m%20on%20the%20London%20"
                "office%20Wi-Fi%2C%20Floor%208.%20Error%20code%3A%20"
                "GP-4022.%0A%0A"
                "Laptop%3A%20Dell%20Latitude%205550%0A"
                "OS%3A%20Windows%2011%2023H2%0A"
                "GlobalProtect%20version%3A%206.1.4%0A%0A"
                "I%27ve%20tried%20restarting%20the%20VPN%20client"
                "%20and%20flushing%20DNS%20%28ipconfig%20%2Fflushdns%29"
                "%20but%20the%20issue%20persists.%0A%0A"
                "This%20is%20blocking%20my%20access%20to%20the%20"
                "trading%20platform.%0A%0A"
                "Thanks%2C%0AEmma%20Walsh%0AEquity%20Derivatives"
            ),
            reporter=_reporter("Emma Walsh", "e.walsh@contoso.com", "Equity Derivatives"),
            created_at="2026-03-18T10:30:00Z",
            channel="portal",
        ),
        expected_triage=ExpectedTriage(
            category="Network & Connectivity",
            priority="P2",
            assigned_team="Network Operations",
        ),
    )
)


# ---------------------------------------------------------------------------
# dc-157: Excessive email disclaimer chains
# ---------------------------------------------------------------------------
_DISCLAIMER_BLOCK = (
    "\n\n" + "=" * 72 + "\n"
    "CONFIDENTIALITY NOTICE: This email and any attachments are for the exclusive "
    "and confidential use of the intended recipient. If you are not the intended "
    "recipient, please do not read, distribute, or take action based on this "
    "message. If you have received this in error, please notify the sender "
    "immediately by return email and delete all copies of this message. Any views "
    "or opinions expressed are solely those of the author and do not represent "
    "those of Contoso Financial Services, its subsidiaries, or affiliates.\n" + "=" * 72
)

default_registry.register(
    EvalScenario(
        scenario_id="dc-157",
        name="Excessive email disclaimer chains",
        description=(
            "Email has been forwarded through 6 organizations, each appending "
            "its own lengthy legal disclaimer. The actual IT issue is a single "
            "sentence buried between disclaimer blocks."
        ),
        category=_CATEGORY,
        tags=["disclaimer_chain", "legal_noise", "forwarded"],
        ticket=EvalTicket(
            ticket_id="INC-5157",
            subject="FW: FW: FW: FW: FW: FW: Network printer issue",
            description=(
                "Hi IT, the network printer HP-PRN-0412 on Floor 4 is giving "
                "a paper jam error E-11 but there is no paper jammed. Already "
                "opened and checked all trays.\n"
                + _DISCLAIMER_BLOCK
                * 6
                + "\n\n-- Forwarded by David Kim on 2026-03-18 --\n"
                "Please handle ASAP.\n" + _DISCLAIMER_BLOCK * 3
            ),
            reporter=_reporter("David Kim", "d.kim@contoso.com", "Operations"),
            created_at="2026-03-18T14:00:00Z",
            channel="email",
        ),
        expected_triage=ExpectedTriage(
            category="Hardware & Peripherals",
            priority="P3",
            assigned_team="Endpoint Engineering",
        ),
    )
)


# ---------------------------------------------------------------------------
# dc-158: Massive inline SVG content
# ---------------------------------------------------------------------------
_SVG_BLOCK = (
    '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 600">\n'
    + "\n".join(
        f'  <rect x="{i * 10}" y="{i * 5}" width="50" height="30" '
        f'fill="rgb({i * 3},{i * 7},{255 - i * 2})" stroke="#333" '
        f'stroke-width="1"><title>Server node-{i:03d} CPU: {60 + i}%</title></rect>'
        for i in range(80)
    )
    + "\n</svg>"
)

default_registry.register(
    EvalScenario(
        scenario_id="dc-158",
        name="Massive inline SVG network topology diagram",
        description=(
            "Ticket contains a large inline SVG diagram of the network topology "
            "that a user pasted from an internal monitoring tool."
        ),
        category=_CATEGORY,
        tags=["inline_svg", "diagram", "large_payload"],
        ticket=EvalTicket(
            ticket_id="INC-5158",
            subject="Network latency spike between NY and London offices",
            description=(
                "Hi Network team,\n\n"
                "We are seeing a latency spike between our NYC and London "
                "data centers. Average RTT went from 75ms to 320ms starting "
                "at 14:00 UTC. Here is the topology diagram from our "
                "monitoring tool:\n\n" + _SVG_BLOCK + "\n\nThe affected MPLS circuit is CKT-CON-0045 between "
                "NYC-DC1 and LDN-DC2. Our SLA threshold is 100ms RTT. "
                "This is affecting cross-border trade execution.\n\n"
                "Regards,\nNikolas Papadopoulos\nNetwork Infrastructure"
            ),
            reporter=_reporter("Nikolas Papadopoulos", "n.papadopoulos@contoso.com", "Network Infrastructure"),
            created_at="2026-03-18T14:15:00Z",
            channel="portal",
        ),
        expected_triage=ExpectedTriage(
            category="Network & Connectivity",
            priority="P1",
            assigned_team="Network Operations",
        ),
    )
)


# ---------------------------------------------------------------------------
# dc-159: Duplicated/looped content (same paragraph repeated 25+ times)
# ---------------------------------------------------------------------------
_REPEATED_PARAGRAPH = (
    "My laptop is running very slowly. Applications take forever to open. "
    "I have restarted multiple times but the issue persists. Please help.\n"
)

default_registry.register(
    EvalScenario(
        scenario_id="dc-159",
        name="Duplicated paragraph repeated 25 times",
        description=(
            "The ticket body is the same paragraph copy-pasted 25 times, "
            "likely from a form bug or user repeatedly clicking submit."
        ),
        category=_CATEGORY,
        tags=["duplicated_content", "repeated_text", "form_bug"],
        ticket=EvalTicket(
            ticket_id="INC-5159",
            subject="Laptop extremely slow",
            description=(
                "Hi IT Support,\n\n"
                + _REPEATED_PARAGRAPH * 25
                + "\nLaptop model: HP EliteBook 840 G9, Windows 11, 16GB RAM.\n"
                "The Task Manager shows 98% disk usage even when idle.\n\n"
                "Thanks,\nMaria Santos\nAccounting"
            ),
            reporter=_reporter("Maria Santos", "m.santos@contoso.com", "Accounting"),
            created_at="2026-03-18T08:00:00Z",
            channel="portal",
        ),
        expected_triage=ExpectedTriage(
            category="Hardware & Peripherals",
            priority="P3",
            assigned_team="Endpoint Engineering",
        ),
    )
)


# ---------------------------------------------------------------------------
# dc-160: Embedded ICS calendar invite data
# ---------------------------------------------------------------------------
default_registry.register(
    EvalScenario(
        scenario_id="dc-160",
        name="Embedded ICS calendar invite in ticket body",
        description=(
            "A calendar invite (iCalendar/ICS format) was pasted raw into the "
            "ticket description along with the actual support request."
        ),
        category=_CATEGORY,
        tags=["ics_calendar", "meeting_invite", "raw_data"],
        ticket=EvalTicket(
            ticket_id="INC-5160",
            subject="Teams meeting links not working — invite data attached",
            description=(
                "Hi, Teams meeting links in calendar invites are giving a "
                '"Meeting not found" error. Here is the raw invite data:\n\n'
                "BEGIN:VCALENDAR\n"
                "VERSION:2.0\n"
                "PRODID:-//Microsoft Corporation//Outlook 16.0 MIMEDIR//EN\n"
                "METHOD:REQUEST\n"
                "BEGIN:VEVENT\n"
                "DTSTART:20260318T150000Z\n"
                "DTEND:20260318T160000Z\n"
                "DTSTAMP:20260317T120000Z\n"
                "UID:040000008200E00074C5B7101A82E00800000000B07A3D51F1DDDB01000000\n"
                "ORGANIZER;CN=Jennifer Park:mailto:j.park@contoso.com\n"
                "ATTENDEE;ROLE=REQ-PARTICIPANT;CN=Trading Desk:mailto:trading@contoso.com\n"
                "SUMMARY:Q1 Portfolio Review\n"
                "LOCATION:https://teams.microsoft.com/l/meetup-join/19%3ameeting_fake\n"
                "DESCRIPTION:Quarterly portfolio review with risk assessment.\n"
                "X-MICROSOFT-SKYPETEAMSMEETINGURL:https://teams.microsoft.com/l/"
                "meetup-join/19%3ameeting_fake\n"
                "X-MICROSOFT-ONLINEMEETINGCONFLINK:conf:sip:j.park@contoso.com\n"
                "BEGIN:VALARM\n"
                "TRIGGER:-PT15M\n"
                "ACTION:DISPLAY\n"
                "DESCRIPTION:Reminder\n"
                "END:VALARM\n"
                "END:VEVENT\n"
                "END:VCALENDAR\n\n"
                "This happens for ALL Teams meetings since yesterday's Outlook "
                "update. Other people in my department are affected too. We are "
                "on Outlook 16.0.18025.20160.\n\n"
                "Jennifer Park\nPortfolio Management"
            ),
            reporter=_reporter("Jennifer Park", "j.park@contoso.com", "Portfolio Management"),
            created_at="2026-03-18T12:30:00Z",
            channel="email",
        ),
        expected_triage=ExpectedTriage(
            category="Software & Applications",
            priority="P2",
            assigned_team="Enterprise Applications",
        ),
    )
)


# ---------------------------------------------------------------------------
# dc-161: Raw hex / memory dump content
# ---------------------------------------------------------------------------
_HEX_DUMP = "\n".join(
    f"0x{addr:08X}  "
    + " ".join(f"{(addr * 7 + i) & 0xFF:02X}" for i in range(16))
    + "  "
    + "".join(chr(c) if 0x20 <= c < 0x7F else "." for c in ((addr * 7 + i) & 0xFF for i in range(16)))
    for addr in range(0, 512, 16)
)

default_registry.register(
    EvalScenario(
        scenario_id="dc-161",
        name="Raw hex memory dump in ticket",
        description=(
            "User pasted a raw hexadecimal memory dump from a crash analysis tool into the ticket description."
        ),
        category=_CATEGORY,
        tags=["hex_dump", "memory_dump", "crash_data"],
        ticket=EvalTicket(
            ticket_id="INC-5161",
            subject="Application crash with blue screen — memory dump attached",
            description=(
                "Hi IT,\n\n"
                "My laptop blue-screened with KERNEL_DATA_INPAGE_ERROR. "
                "I managed to capture part of the crash dump:\n\n"
                + _HEX_DUMP
                + "\n\nThis is the third BSOD this week. Each time the stop "
                "code is the same: KERNEL_DATA_INPAGE_ERROR (0x0000007A). "
                "I suspect the SSD is failing. Laptop: Lenovo ThinkPad T14s "
                "Gen 4, 512GB SSD, Windows 11 Enterprise. CrystalDiskInfo "
                "shows 'Caution' status for the drive.\n\n"
                "Please replace the SSD before I lose data.\n\n"
                "Tom Bennett\nQuantitative Research"
            ),
            reporter=_reporter("Tom Bennett", "t.bennett@contoso.com", "Quantitative Research"),
            created_at="2026-03-18T07:30:00Z",
            channel="email",
        ),
        expected_triage=ExpectedTriage(
            category="Hardware & Peripherals",
            priority="P2",
            assigned_team="Endpoint Engineering",
        ),
    )
)


# ---------------------------------------------------------------------------
# dc-162: Windows Event Log XML dump
# ---------------------------------------------------------------------------
_EVENT_LOG_XML = "\n".join(
    f'<Event xmlns="http://schemas.microsoft.com/win/2004/08/events/event">\n'
    f"  <System>\n"
    f'    <Provider Name="Microsoft-Windows-Security-Auditing" Guid="{{54849625-5478-4994-A5BA-3E3B0328C30D}}"/>\n'
    f"    <EventID>{4625 if i % 3 == 0 else 4624}</EventID>\n"
    f"    <Level>{0 if i % 3 == 0 else 4}</Level>\n"
    f'    <TimeCreated SystemTime="2026-03-18T0{7 + i // 6}:{(i * 7) % 60:02d}:00.000Z"/>\n'
    f"    <Computer>WS-CONTOSO-{100 + i}</Computer>\n"
    f"  </System>\n"
    f"  <EventData>\n"
    f'    <Data Name="TargetUserName">svc_trading_{i:02d}</Data>\n'
    f'    <Data Name="LogonType">3</Data>\n'
    f'    <Data Name="IpAddress">10.40.{i // 10}.{i % 256}</Data>\n'
    f'    <Data Name="Status">{"0xC000006D" if i % 3 == 0 else "0x0"}</Data>\n'
    f"  </EventData>\n"
    f"</Event>"
    for i in range(30)
)

default_registry.register(
    EvalScenario(
        scenario_id="dc-162",
        name="Windows Event Log XML dump",
        description=(
            "User exported and pasted 30 Windows Security Event Log entries "
            "in raw XML format to illustrate failed logon attempts."
        ),
        category=_CATEGORY,
        tags=["event_log", "xml_dump", "security_log"],
        ticket=EvalTicket(
            ticket_id="INC-5162",
            subject="Repeated failed login attempts on trading workstation",
            description=(
                "Hi Security team,\n\n"
                "We are seeing repeated Event ID 4625 (failed logon) entries on "
                "the trading floor workstations. I exported the Event Viewer "
                "logs:\n\n" + _EVENT_LOG_XML + "\n\nThe failed attempts target service accounts svc_trading_* "
                "with LogonType 3 (network). Status 0xC000006D indicates bad "
                "username or password. This started at 07:00 UTC and is "
                "happening every few minutes.\n\n"
                "Is someone running a brute-force attack against our service "
                "accounts? Please investigate urgently.\n\n"
                "Oliver Grant\nIT Security"
            ),
            reporter=_reporter("Oliver Grant", "o.grant@contoso.com", "IT Security"),
            created_at="2026-03-18T09:00:00Z",
            channel="portal",
        ),
        expected_triage=ExpectedTriage(
            category="Security & Compliance",
            priority="P1",
            assigned_team="Security Operations",
            needs_escalation=True,
        ),
    )
)


# ---------------------------------------------------------------------------
# dc-163: Markdown with code fences and tables
# ---------------------------------------------------------------------------
default_registry.register(
    EvalScenario(
        scenario_id="dc-163",
        name="Markdown with code fences and tables",
        description=(
            "Ticket was submitted via a Markdown-enabled portal and contains "
            "code fences, inline code, tables, and headers in raw Markdown."
        ),
        category=_CATEGORY,
        tags=["markdown", "code_fences", "tables"],
        ticket=EvalTicket(
            ticket_id="INC-5163",
            subject="Database connection pool exhaustion in production",
            description=(
                "# Database Connection Pool Exhaustion\n\n"
                "## Environment\n"
                "| Component | Version |\n"
                "|-----------|----------|\n"
                "| SQL Server | 2022 CU12 |\n"
                "| Connection Pool | HikariCP 5.1.0 |\n"
                "| App Server | Tomcat 10.1.18 |\n"
                "| JDK | OpenJDK 21.0.2 |\n\n"
                "## Issue\n"
                "Connection pool is being exhausted during peak trading hours "
                "(09:30-10:00 ET). Application logs show:\n\n"
                "```\n"
                "2026-03-18T09:32:14.567Z ERROR [pool-monitor] HikariPool-1 - "
                "Connection is not available, request timed out after 30000ms.\n"
                "2026-03-18T09:32:14.568Z ERROR [pool-monitor] HikariPool-1 - "
                "Active: 50, Idle: 0, Waiting: 127, Total: 50\n"
                "```\n\n"
                "## Current Pool Config\n"
                "```yaml\n"
                "hikari:\n"
                "  maximum-pool-size: 50\n"
                "  minimum-idle: 10\n"
                "  connection-timeout: 30000\n"
                "  idle-timeout: 600000\n"
                "  max-lifetime: 1800000\n"
                "```\n\n"
                "## Steps to Reproduce\n"
                "1. Wait for market open at 09:30 ET\n"
                "2. Observe connection count spike in `sys.dm_exec_connections`\n"
                "3. Run `SELECT * FROM sys.dm_exec_requests WHERE status = 'suspended'`\n\n"
                "## Impact\n"
                "**P1** — Trade orders are failing with timeout errors.\n\n"
                "cc: @database-team @platform-engineering"
            ),
            reporter=_reporter("James Wu", "j.wu@contoso.com", "Platform Engineering"),
            created_at="2026-03-18T09:35:00Z",
            channel="portal",
        ),
        expected_triage=ExpectedTriage(
            category="Data & Storage",
            priority="P1",
            assigned_team="Data Platform",
            needs_escalation=True,
        ),
    )
)


# ---------------------------------------------------------------------------
# dc-164: HTML email with deeply nested table layout
# ---------------------------------------------------------------------------
_NESTED_TABLE = (
    "<html><head><style>body{font-family:Calibri;} table{border-collapse:collapse;} "
    "td{padding:4px 8px;border:1px solid #ccc;}</style></head><body>"
    "<table><tr><td><table><tr><td><table><tr><td><table><tr><td>"
    "<p><b>From:</b> Martha Johnson &lt;m.johnson@contoso.com&gt;<br>"
    "<b>Sent:</b> Monday, March 18, 2026 8:00 AM<br>"
    "<b>To:</b> IT Help Desk &lt;helpdesk@contoso.com&gt;<br>"
    "<b>Subject:</b> RE: Shared mailbox access</p>"
    "</td></tr></table></td></tr>"
    "<tr><td><p style='font-size:11pt;color:#1F497D;'>"
    "Hi IT team,<br><br>"
    "I need access to the shared mailbox <b>compliance-alerts@contoso.com</b>. "
    "I was added to the Compliance team last week but my manager forgot to "
    "request mailbox access. I need Full Access and Send-As permissions. "
    "My manager Lisa Chen (l.chen@contoso.com) has approved this — she is "
    "CC'd on this email.<br><br>"
    "My account: m.johnson@contoso.com<br>"
    "Mailbox needed: compliance-alerts@contoso.com<br>"
    "Permissions: Full Access + Send As<br><br>"
    "Thanks,<br>Martha Johnson<br>Compliance</p>"
    "</td></tr></table></td></tr></table></td></tr></table>"
    "<br><img src='cid:image001.png' width='200'>"
    "<p style='font-size:8pt;color:#999;'>Contoso Financial Services | "
    "100 Wall Street, New York, NY 10005</p>"
    "</body></html>"
)

default_registry.register(
    EvalScenario(
        scenario_id="dc-164",
        name="HTML email with deeply nested table layout",
        description=(
            "Outlook-generated HTML email with 4 levels of nested tables, "
            "inline CSS, CID image references, and HTML entity encodings."
        ),
        category=_CATEGORY,
        tags=["html_nested_tables", "outlook_html", "rich_formatting"],
        ticket=EvalTicket(
            ticket_id="INC-5164",
            subject="RE: Shared mailbox access",
            description=_NESTED_TABLE,
            reporter=_reporter("Martha Johnson", "m.johnson@contoso.com", "Compliance"),
            created_at="2026-03-18T08:05:00Z",
            channel="email",
        ),
        expected_triage=ExpectedTriage(
            category="Access & Authentication",
            priority="P3",
            assigned_team="Identity & Access Management",
        ),
    )
)


# ---------------------------------------------------------------------------
# dc-165: Ticket with XML/SOAP fault dump
# ---------------------------------------------------------------------------
default_registry.register(
    EvalScenario(
        scenario_id="dc-165",
        name="SOAP fault XML dump in ticket",
        description=(
            "User pasted a full SOAP fault response from a web service call, "
            "including XML namespaces, stack trace, and envelope wrappers."
        ),
        category=_CATEGORY,
        tags=["soap_fault", "xml_dump", "web_service"],
        ticket=EvalTicket(
            ticket_id="INC-5165",
            subject="Trade execution API returning SOAP faults",
            description=(
                "The FIX gateway integration is throwing SOAP faults on every "
                "order submission since 08:45 UTC. Full response:\n\n"
                '<?xml version="1.0" encoding="UTF-8"?>\n'
                "<soap:Envelope "
                'xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" '
                'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">\n'
                "  <soap:Body>\n"
                "    <soap:Fault>\n"
                "      <faultcode>soap:Server</faultcode>\n"
                "      <faultstring>Service temporarily unavailable</faultstring>\n"
                "      <detail>\n"
                "        <ns1:ServiceException "
                'xmlns:ns1="http://contoso.com/trading/v2">\n'
                "          <errorCode>ORD-5003</errorCode>\n"
                "          <message>Connection pool exhausted for "
                "FIX.4.4:CONTOSO->EXCHANGE</message>\n"
                "          <timestamp>2026-03-18T08:45:12.345Z</timestamp>\n"
                "          <correlationId>a1b2c3d4-e5f6-7890-abcd-ef1234567890"
                "</correlationId>\n"
                "          <stackTrace>\n"
                "            at com.contoso.fix.gateway.OrderRouter.submit"
                "(OrderRouter.java:142)\n"
                "            at com.contoso.fix.gateway.SessionManager.dispatch"
                "(SessionManager.java:89)\n"
                "            at com.contoso.fix.gateway.FixEngine.processMessage"
                "(FixEngine.java:201)\n"
                "          </stackTrace>\n"
                "        </ns1:ServiceException>\n"
                "      </detail>\n"
                "    </soap:Fault>\n"
                "  </soap:Body>\n"
                "</soap:Envelope>\n\n"
                "This is production-critical — no orders are going through. "
                "The FIX session to the exchange is up but orders fail at the "
                "application layer.\n\n"
                "Raj Patel\nElectronic Trading"
            ),
            reporter=_reporter("Raj Patel", "r.patel@contoso.com", "Electronic Trading"),
            created_at="2026-03-18T08:50:00Z",
            channel="portal",
        ),
        expected_triage=ExpectedTriage(
            category="Software & Applications",
            priority="P1",
            assigned_team="Enterprise Applications",
            needs_escalation=True,
        ),
    )
)


# ---------------------------------------------------------------------------
# dc-166: Ticket with massive CSS-styled HTML diagnostic table
# ---------------------------------------------------------------------------
_DIAG_ROWS = "\n".join(
    f"<tr style='background:{('#f9f9f9' if i % 2 == 0 else '#fff')}'>"
    f"<td>switch-fl{i // 5 + 1}-{i:02d}</td>"
    f"<td>10.40.{i // 5 + 1}.{i}</td>"
    f"<td>{'Up' if i % 7 != 0 else '<span style="color:red">Down</span>'}</td>"
    f"<td>{(i * 17) % 100}%</td>"
    f"<td>{'OK' if i % 11 != 0 else '<b>CRC Errors: ' + str(i * 3) + '</b>'}</td>"
    f"</tr>"
    for i in range(60)
)

default_registry.register(
    EvalScenario(
        scenario_id="dc-166",
        name="Massive CSS-styled HTML diagnostic table",
        description=(
            "Network admin pasted a 60-row HTML table from a switch monitoring "
            "dashboard showing port status, utilization, and error counts."
        ),
        category=_CATEGORY,
        tags=["html_table", "diagnostics", "network_data"],
        ticket=EvalTicket(
            ticket_id="INC-5166",
            subject="Multiple switch ports showing CRC errors — dashboard output attached",
            description=(
                "Hi Network team,\n\n"
                "Several switches on Floors 1-12 are reporting CRC errors. "
                "Dashboard dump below:\n\n"
                "<table style='border-collapse:collapse;font-family:Consolas;"
                "font-size:10px;'>"
                "<tr style='background:#333;color:#fff;'>"
                "<th>Switch</th><th>IP</th><th>Status</th>"
                "<th>Utilization</th><th>Notes</th></tr>\n" + _DIAG_ROWS + "\n</table>\n\n"
                "Switches with 'Down' status and CRC errors need immediate "
                "attention. This is affecting connectivity for ~200 users "
                "across multiple floors. Suspect bad uplink fiber on the "
                "Floor 7 MDF.\n\n"
                "Kevin O'Brien\nNetwork Operations"
            ),
            reporter=_reporter("Kevin O'Brien", "k.obrien@contoso.com", "Network Operations"),
            created_at="2026-03-18T11:00:00Z",
            channel="portal",
        ),
        expected_triage=ExpectedTriage(
            category="Network & Connectivity",
            priority="P1",
            assigned_team="Network Operations",
            needs_escalation=True,
        ),
    )
)


# ---------------------------------------------------------------------------
# dc-167: Auto-reply loop with Out-of-Office messages
# ---------------------------------------------------------------------------
_OOO_MSG = "I am currently out of the office with limited access to email. "
_OOO_RETURN = "I will respond when I return on March 24."
_OOO_URGENT = "For urgent matters, please contact my manager Bob Lee at b.lee@contoso.com."
_HD_ACK = "Thank you for contacting IT Help Desk. Your ticket has been received. "
_HD_NOREPLY = "Do not reply to this automated message."

_OOO_LOOP = "".join(
    f"\n--- Auto-Reply from {'alice.wong' if i % 2 == 0 else 'helpdesk'}@contoso.com ---\n"
    f"{_OOO_MSG if i % 2 == 0 else _HD_ACK}"
    f"{_OOO_RETURN if i % 2 == 0 else 'A technician will be assigned shortly. Reference: AUTO-' + str(9000 + i)}\n"
    f"{_OOO_URGENT if i % 2 == 0 else _HD_NOREPLY}\n"
    for i in range(20)
)

default_registry.register(
    EvalScenario(
        scenario_id="dc-167",
        name="Auto-reply loop — 20 OOO bounces",
        description=(
            "An Out-of-Office auto-reply created a loop with the helpdesk "
            "auto-acknowledgment, generating 20 round-trip messages."
        ),
        category=_CATEGORY,
        tags=["auto_reply_loop", "ooo_bounce", "email_storm"],
        ticket=EvalTicket(
            ticket_id="INC-5167",
            subject="Re: Re: Re: Re: Re: Auto: Auto: Out of Office: MFA token expired",
            description=(
                "Original request: My MFA token on the Microsoft Authenticator "
                "app expired and I cannot generate new codes. I have a backup "
                "phone number registered but the SMS codes are not arriving. "
                "Need MFA reset to regain access to my account "
                "(alice.wong@contoso.com).\n" + _OOO_LOOP
            ),
            reporter=_reporter("Alice Wong", "alice.wong@contoso.com", "Asset Management"),
            created_at="2026-03-18T06:00:00Z",
            channel="email",
        ),
        expected_triage=ExpectedTriage(
            category="Access & Authentication",
            priority="P2",
            assigned_team="Identity & Access Management",
        ),
    )
)


# ---------------------------------------------------------------------------
# dc-168: Massive PowerShell transcript with ANSI escape codes
# ---------------------------------------------------------------------------
_PS_TRANSCRIPT = "\n".join(
    f"\x1b[32mPS C:\\Users\\admin>\x1b[0m Get-Service | "
    f"Where-Object {{$_.Status -eq 'Stopped'}} | "
    f"Select-Object -First 1\n"
    f"\x1b[33mWARNING:\x1b[0m Service 'Svc{i:03d}' is in a degraded state.\n"
    f"Status   Name           DisplayName\n"
    f"------   ----           -----------\n"
    f"Stopped  Svc{i:03d}        Contoso Trading Service {i}\n"
    for i in range(20)
)

default_registry.register(
    EvalScenario(
        scenario_id="dc-168",
        name="PowerShell transcript with ANSI escape codes",
        description=(
            "User pasted a PowerShell transcript containing ANSI escape codes "
            "for colored output, making the text difficult to parse."
        ),
        category=_CATEGORY,
        tags=["ansi_escape", "powershell", "terminal_output"],
        ticket=EvalTicket(
            ticket_id="INC-5168",
            subject="Multiple Windows services stopped on trading server",
            description=(
                "Hi IT,\n\n"
                "Several critical Windows services have stopped on the trading "
                "floor server TRADE-SRV-01. Here is my PowerShell output:\n\n"
                + _PS_TRANSCRIPT
                + "\n\nThese services are needed for the order management "
                "system. The server has 64GB RAM and CPU is at 12% so it is "
                "not a resource issue. Services were running fine until the "
                "scheduled restart last night at 02:00.\n\n"
                "Please restart the services or investigate why they are not "
                "starting automatically.\n\n"
                "Carlos Rivera\nTrading Technology"
            ),
            reporter=_reporter("Carlos Rivera", "c.rivera@contoso.com", "Trading Technology"),
            created_at="2026-03-18T07:15:00Z",
            channel="portal",
        ),
        expected_triage=ExpectedTriage(
            category="Software & Applications",
            priority="P1",
            assigned_team="Enterprise Applications",
            needs_escalation=True,
        ),
    )
)


# ---------------------------------------------------------------------------
# dc-169: Email with mixed RTF artifacts
# ---------------------------------------------------------------------------
default_registry.register(
    EvalScenario(
        scenario_id="dc-169",
        name="RTF formatting artifacts in email body",
        description=(
            "Email body contains raw RTF control sequences from a copy-paste error, mixed with the actual ticket text."
        ),
        category=_CATEGORY,
        tags=["rtf_artifacts", "formatting_noise", "copy_paste"],
        ticket=EvalTicket(
            ticket_id="INC-5169",
            subject="Shared drive permissions issue",
            description=(
                "{\\rtf1\\ansi\\ansicpg1252\\deff0\\nouicompat"
                "{\\fonttbl{\\f0\\fswiss\\fcharset0 Calibri;}}\n"
                "{\\colortbl ;\\red0\\green0\\blue0;}\n"
                "{\\*\\generator Riched20 10.0.22621}\\viewkind4"
                "\\uc1 \n"
                "\\pard\\sl276\\slmult1\\f0\\fs22 Hi IT team,"
                "\\par\n"
                "\\par\n"
                "I cannot access the \\\\\\\\contoso-fs02\\\\trading$ "
                "shared drive. I get \\b Access Denied\\b0  error even "
                "though I am in the Trading-Users AD group. My manager "
                "confirmed my group membership in ADUC.\\par\n"
                "\\par\n"
                "Details:\\par\n"
                "- Drive: \\\\\\\\contoso-fs02\\\\trading$\\par\n"
                "- Error: Access Denied (0x80070005)\\par\n"
                "- My account: l.martinez@contoso.com\\par\n"
                "- AD Group: Trading-Users (confirmed member)\\par\n"
                "\\par\n"
                "This started after the file server migration last "
                "weekend. Other people in my team can access it fine."
                "\\par\n"
                "\\par\n"
                "Thanks,\\par\n"
                "Laura Martinez\\par\n"
                "Derivatives Trading\\par\n"
                "}"
            ),
            reporter=_reporter("Laura Martinez", "l.martinez@contoso.com", "Derivatives Trading"),
            created_at="2026-03-18T10:45:00Z",
            channel="email",
        ),
        expected_triage=ExpectedTriage(
            category="Access & Authentication",
            priority="P2",
            assigned_team="Identity & Access Management",
        ),
    )
)


# ---------------------------------------------------------------------------
# dc-170: Ticket with base64-encoded executable attachment reference
# ---------------------------------------------------------------------------
_EXE_BASE64 = (
    "TVqQAAMAAAAEAAAA//8AALgAAAAAAAAAQAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
    "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA" + "A" * 200 + "AAAAAAAAAAAAAAAAAAAAAA=="
)

default_registry.register(
    EvalScenario(
        scenario_id="dc-170",
        name="Base64-encoded executable in ticket body",
        description=(
            "User pasted what appears to be a base64-encoded Windows executable "
            "(MZ header) into the ticket description, claiming it is the "
            "installer for a tool they need approved."
        ),
        category=_CATEGORY,
        tags=["base64_executable", "suspicious_payload", "security_concern"],
        ticket=EvalTicket(
            ticket_id="INC-5170",
            subject="Need approval for network diagnostic tool — installer attached",
            description=(
                "Hi IT,\n\n"
                "I need the Wireshark network analyzer installed on my laptop "
                "for troubleshooting packet captures on the trading floor. Our "
                "firewall blocks downloads from wireshark.org so I am pasting "
                "the installer here as base64:\n\n" + _EXE_BASE64 + "\n\n"
                "Please decode and install this on my laptop (WS-CONTOSO-4521). "
                "I have my manager's verbal approval for this software.\n\n"
                "My machine details:\n"
                "- Hostname: WS-CONTOSO-4521\n"
                "- OS: Windows 11 Enterprise 23H2\n"
                "- User: g.thompson@contoso.com\n\n"
                "George Thompson\nMarket Data"
            ),
            reporter=_reporter("George Thompson", "g.thompson@contoso.com", "Market Data"),
            created_at="2026-03-18T13:00:00Z",
            channel="portal",
        ),
        expected_triage=ExpectedTriage(
            category="Security & Compliance",
            priority="P2",
            assigned_team="Security Operations",
        ),
    )
)
