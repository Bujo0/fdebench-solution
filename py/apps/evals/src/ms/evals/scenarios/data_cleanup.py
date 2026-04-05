# Copyright (c) Microsoft. All rights reserved.
"""Data cleanup edge-case scenario templates.

Covers: long email threads, base64-encoded images, HTML-heavy emails,
garbled encoding, emoji-heavy chat, repeated content, excessive signatures,
mixed languages, truncated messages, log dumps, HTML entities,
duplicate/stuttering content, extremely verbose single emails, URL-heavy tickets,
JSON/XML data dumps, Windows Event Log entries, SMTP header dumps,
auto-generated notification noise, excessive whitespace, OCR artifacts,
pasted tabular data, phone transcript filler, multi-forward signature chains,
markdown formatting artifacts, large stack traces, invisible Unicode,
MIME boundary markers, base64-encoded PDFs, multiple inline images,
ICS/vCalendar metadata, very long emails with buried issues,
multilingual disclaimers, NDR/bounce-back wrappers, regex/code patterns,
contradictory email threads, and accidental PII in descriptions.
"""

from ms.evals.constants import Category
from ms.evals.constants import MissingInfo
from ms.evals.constants import Priority
from ms.evals.constants import Team
from ms.evals.models import ScenarioTemplate
from ms.evals.scenarios.registry import register

# ---------------------------------------------------------------------------
# dc-001  Long email thread with deeply nested quoted replies
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="dc-001",
        category=Category.NETWORK,
        priority=Priority.P2,
        assigned_team=Team.NETWORK,
        needs_escalation=False,
        missing_information=[MissingInfo.APPLICATION_VERSION],
        subjects=[
            "Re: Re: Re: Re: Re: FW: VPN disconnects during market open",
            "RE: RE: RE: FW: FW: Internet keeps dropping at my desk",
            "Re: Re: Re: Re: WiFi unstable — following up again",
        ],
        descriptions=[
            "Just following up again — the VPN still drops every morning between 09:28 and 09:32 ET.\n"
            "I have to reconnect 3-4 times before it stabilizes.\n\n"
            "--- Original Message ---\n"
            "From: {name} <{name1}@contoso.com>\n"
            "Sent: Monday, March 10, 2026 8:45 AM\n"
            "To: IT Support <itsupport@contoso.com>\n"
            "Subject: Re: Re: Re: Re: FW: VPN disconnects during market open\n\n"
            "Still happening today. I ran the diagnostics you asked for — attached.\n\n"
            "--- Original Message ---\n"
            "From: IT Support <itsupport@contoso.com>\n"
            "Sent: Friday, March 7, 2026 4:10 PM\n"
            "Subject: Re: Re: Re: FW: VPN disconnects during market open\n\n"
            "Could you run 'netsh wlan show all' and send us the output? Also confirm "
            "your GlobalProtect client version.\n\n"
            "--- Original Message ---\n"
            "From: {name} <{name1}@contoso.com>\n"
            "Sent: Friday, March 7, 2026 9:05 AM\n"
            "Subject: Re: Re: FW: VPN disconnects during market open\n\n"
            "It happened again. I lost the VPN tunnel at exactly 09:30. My colleague says "
            "his works fine so I don't think it's the office network.\n\n"
            "--- Original Message ---\n"
            "From: IT Support <itsupport@contoso.com>\n"
            "Sent: Thursday, March 6, 2026 3:00 PM\n"
            "Subject: Re: FW: VPN disconnects during market open\n\n"
            "Can you tell us which office and floor you're on? Also, Wi-Fi or Ethernet?\n\n"
            "--- Original Message ---\n"
            "From: {name} <{name1}@contoso.com>\n"
            "Sent: Thursday, March 6, 2026 9:35 AM\n"
            "Subject: FW: VPN disconnects during market open\n\n"
            "My VPN keeps disconnecting every morning around market open. I'm on the "
            "5th floor, Building 3, {office} office, using Wi-Fi.",
            "This is my third follow-up. Still no resolution.\n\n"
            "On Mon, Mar 10, 2026 at 2:15 PM IT Support <itsupport@contoso.com> wrote:\n"
            "> We've escalated this to the network team.\n"
            "> They should reach out within 24 hours.\n\n"
            "On Fri, Mar 7, 2026 at 9:00 AM I wrote:\n"
            "> The connection drops every day around the same time.\n"
            "> I'm getting packet loss on the wireless — about 15% according to ping.\n\n"
            "On Thu, Mar 6, 2026 at 4:00 PM IT Support wrote:\n"
            "> Thanks for reporting. Can you confirm your laptop model and OS?\n\n"
            "Original issue: My internet connection keeps dropping multiple times "
            "per day. I'm on Floor {floor}, Building 3, {office} office.",
        ],
        next_best_actions=[
            "Investigate recurring VPN disconnects correlated with market-open traffic spike "
            "for user on Wi-Fi — check AP congestion and VPN gateway logs.",
            "Diagnose intermittent packet loss on wireless connection for user on Floor {floor} "
            "— correlate with AP utilization data during peak hours.",
        ],
        remediation_steps=[
            [
                "Check VPN gateway logs for the user's session drops during the reported time window",
                "Correlate with wireless controller data for the reported floor's AP utilization",
                "Verify VPN split-tunnel configuration and MTU settings on the client",
                "If Wi-Fi congestion confirmed, consider moving user to Ethernet or a less congested AP",
                "Provide user with updated VPN client if version is outdated",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# dc-002  Inline base64-encoded image data
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="dc-002",
        category=Category.HARDWARE,
        priority=Priority.P3,
        assigned_team=Team.ENDPOINT,
        needs_escalation=False,
        missing_information=[MissingInfo.DEVICE_INFO],
        subjects=[
            "Monitor flickering — screenshot attached inline",
            "Screen issue — inline image below",
            "Display problem — see embedded screenshot",
        ],
        descriptions=[
            "My external monitor keeps flickering every few seconds. I took a screenshot but "
            "our mail client embedded it inline. Here it is:\n\n"
            "[image: screenshot.png]\n"
            "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR4"
            "2mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg==\n"
            "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAKCAYAAACNMs+9AAAAFUlEQVQYV2"
            "P8z8BQz0AEYBxVOHIVAvcHBQHzKSECAAAAAElFTkSuQmCC\n\n"
            "The flickering started Monday after a {os} Update. It's a Dell U2722D connected "
            "via DisplayPort to my docking station (Dell WD19S). The built-in laptop screen "
            "is fine. I've tried a different DisplayPort cable — same issue.",
            "Attaching an inline screenshot of the error on my monitor:\n\n"
            "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEASABIAAD/2wBDAAgGBgcGBQgHBwcJCQgKDBQN"
            "DAsLDBkSEw8UHRofHh0aHBwgJC4nICIsIxwcKDcpLDAxNDQ0Hyc5PTgyPC4zNDL/wgALCAABAAEBAREA"
            "/8QAFAABAAAAAAAAAAAAAAAAAAAACf/aAAgBAQAAAABT/9k=\n\n"
            "The external monitor randomly goes black for 2-3 seconds and comes back. "
            "Happens 5-10 times per hour. Using a ThinkPad dock (USB-C) with HDMI output. "
            "Started after the latest driver update on {date}.",
        ],
        next_best_actions=[
            "Troubleshoot external monitor flickering — likely a display driver regression "
            "after recent OS update via docking station.",
            "Diagnose intermittent monitor blackouts — check display driver and dock firmware "
            "compatibility after recent update.",
        ],
        remediation_steps=[
            [
                "Roll back the most recent display driver update",
                "Check docking station firmware version and update if behind current release",
                "Test monitor on a different docking station to isolate dock vs driver issue",
                "If driver rollback resolves, add the driver to the deferral list",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# dc-003  HTML-heavy email with tags, styles, and entities
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="dc-003",
        category=Category.ACCESS_AUTH,
        priority=Priority.P2,
        assigned_team=Team.IAM,
        needs_escalation=False,
        missing_information=[MissingInfo.ERROR_MESSAGE],
        subjects=[
            "Cannot access SharePoint after migration",
            "403 Forbidden on SharePoint — need access restored",
            "SharePoint permissions lost after site migration",
        ],
        descriptions=[
            '<html><body style="font-family:Calibri,sans-serif;font-size:11pt">'
            '<div style="margin:0;padding:0">'
            "<p><b>Hi IT Team,</b></p>"
            '<p style="color:#1F4E79">Since the SharePoint migration last Friday I can'
            "&rsquo;t open the <b>Compliance Policy Library</b> site. I get a "
            "&ldquo;403 Forbidden&rdquo; error every time I click the link.</p>"
            "<p>Steps I&apos;ve tried:</p>"
            "<ol>"
            "<li>Cleared browser cache &amp; cookies</li>"
            "<li>Tried {browser} and Edge &mdash; same result</li>"
            "<li>Verified my account at <u>myaccount.microsoft.com</u></li>"
            "</ol>"
            '<p style="font-size:9pt;color:gray">Sent from Outlook for Windows</p>'
            '<p style="font-size:8pt;color:gray">CONFIDENTIALITY NOTICE: This email and any '
            "attachments are for the exclusive and confidential use of the intended recipient.</p>"
            "</div></body></html>",
            '<div class="WordSection1">'
            '<p class="MsoNormal"><span style="font-size:11.0pt">Hello,</span></p>'
            '<p class="MsoNormal"><span style="font-size:11.0pt">I&rsquo;m unable to access the '
            'internal wiki at <a href="https://contoso.sharepoint.com/sites/ITWiki">'
            "https://contoso.sharepoint.com/sites/ITWiki</a>. I get &ldquo;You don&rsquo;t have "
            "access to this resource&rdquo; since the migration last week.</span></p>"
            '<p class="MsoNormal"><o:p>&nbsp;</o:p></p>'
            '<p class="MsoNormal"><span style="font-size:8.0pt;color:gray">This message may contain '
            "confidential information.&nbsp;</span></p>"
            "</div>",
        ],
        next_best_actions=[
            "Investigate 403 Forbidden on SharePoint site for user — likely a permission "
            "mapping gap from the recent migration.",
            "Restore user access to SharePoint site after migration — check permission "
            "inheritance and group memberships.",
        ],
        remediation_steps=[
            [
                "Check SharePoint admin center for the site permissions",
                "Verify user's Azure AD group memberships against the migrated site's access list",
                "Re-grant access to the site collection if permissions were lost during migration",
                "Confirm user can access the site after permission fix",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# dc-004  Garbled / encoding-corrupted text
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="dc-004",
        category=Category.HARDWARE,
        priority=Priority.P2,
        assigned_team=Team.ENDPOINT,
        needs_escalation=False,
        missing_information=[MissingInfo.ERROR_MESSAGE],
        subjects=[
            "Printer producing garbled output \u2014 urg\u00ebnt",
            "Printer prints gibberish \u2014 \u00e9ncoding issue?",
            "Print output corrupted with strange characters",
        ],
        descriptions=[
            "The printer on the {floor} floor is printing garbled characters on every document. "
            "Here\u2019s what the output looks like:\n\n"
            "\u00c3\u00a9\u00c3\u00b1\u00c3\u00bc\u00c3\u00a8\u00c2\u00ab\u00c2\u00bb "
            "\u00ef\u00bf\u00bd\u00ef\u00bf\u00bd\u00ef\u00bf\u00bd "
            "R\u00c3\u00a9port_Q1_2026.xlsx \u00e2\u0080\u0093 Page 1 of 4\n"
            "\u00c3\u0081\u00c3\u00a7\u00c3\u00a7\u00c3\u00a8\u00c3\u0178\u00c3\u0178 "
            "D\u00c3\u00a8ni\u00c3\u00a8d\n\n"
            "I\u2019ve tried restarting the printer and switching paper trays. My colleague "
            "confirmed it\u2019s happening for their documents too. We need this fixed today.",
            "Printing from any application produces garbled output on the HP LaserJet MFP on "
            "Floor {floor}. Characters are replaced with \u00ef\u00bf\u00bd symbols and "
            "accented characters throughout. A test page from the printer's own menu prints fine, "
            "so the issue seems to be between the print server and the printer.",
        ],
        next_best_actions=[
            "Investigate printer producing garbled output — likely a corrupt print driver or PCL/PostScript mismatch.",
            "Diagnose encoding corruption between print server and printer — check driver "
            "language settings and font substitution.",
        ],
        remediation_steps=[
            [
                "Check the print server for driver version and compare against latest release",
                "Reinstall or update the printer driver on the print server",
                "Verify PCL vs PostScript language setting matches the printer's configuration",
                "Print a test page from the server to confirm the fix",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# dc-005  Emoji-heavy chat message
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="dc-005",
        category=Category.SOFTWARE,
        priority=Priority.P2,
        assigned_team=Team.ENTERPRISE_APPS,
        needs_escalation=True,
        missing_information=[MissingInfo.TIMESTAMP, MissingInfo.ERROR_MESSAGE],
        subjects=[
            "Slack integration broken \U0001f6a8\U0001f6a8\U0001f6a8",
            "\U0001f525\U0001f525 Jira-Slack connector down \U0001f525\U0001f525",
            "HELP \U0001f62d integration not working \U0001f62d",
        ],
        descriptions=[
            "\U0001f6a8\U0001f6a8\U0001f6a8 URGENT \U0001f6a8\U0001f6a8\U0001f6a8\n\n"
            "The Slack \u2194\ufe0f Jira integration is totally broken \U0001f62d\U0001f62d\n"
            "When I create a ticket in #trading-incidents it used to auto-create a Jira "
            "issue \U0001f4cb but now NOTHING happens \u274c\u274c\n\n"
            "I\u2019ve checked:\n"
            "\u2705 Slack app is still installed\n"
            "\u2705 I can see the Jira bot in the channel\n"
            "\u274c But the /jira create command gives me \U0001f449 "
            '"Oops! Something went wrong (error 502)" \U0001f448\n\n'
            "This is blocking our whole incident workflow \U0001f525\U0001f525\U0001f525\n\n"
            "pls help asap \U0001f64f\U0001f64f",
            "\U0001f4a5 {app} connector is DOWN \U0001f4a5\n\n"
            "nobody can create tickets from Slack anymore \U0001f62d\n"
            "error 502 when using the slash command \u274c\n"
            "been broken since this morning \U0001f550\n"
            "this is a P2 for real \U0001f525\n\n"
            "tried:\n"
            "\U0001f504 reconnecting the app\n"
            "\U0001f504 revoking and re-authorizing\n"
            "\U0001f504 different channels\n\n"
            "nothing works \U0001f92f pls help",
        ],
        next_best_actions=[
            "Investigate Slack-Jira integration returning 502 errors — blocking incident tracking workflow.",
            "Diagnose integration connector failure returning 502 — check OAuth tokens and webhook configuration.",
        ],
        remediation_steps=[
            [
                "Check the integration platform status page for ongoing incidents",
                "Verify the app OAuth tokens have not expired or been revoked",
                "Review webhook logs for 502 errors and identify the failing endpoint",
                "If reauthorization needed, walk the channel admin through it",
                "Test the integration command from the channel to confirm resolution",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# dc-006  Excessive repeated / copy-pasted content
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="dc-006",
        category=Category.SOFTWARE,
        priority=Priority.P3,
        assigned_team=Team.ENTERPRISE_APPS,
        needs_escalation=False,
        missing_information=[MissingInfo.STEPS_TO_REPRODUCE],
        subjects=[
            "Outlook keeps crashing — error details inside",
            "Application crash on startup — repeated error log",
            "{app} crashes repeatedly — same error every time",
        ],
        descriptions=[
            "Outlook crashes every time I open a specific email.\n\n"
            "Here's the error from Event Viewer (it repeated many times):\n\n"
            "Faulting application name: OUTLOOK.EXE, version: 16.0.18227.20162\n"
            "Faulting module name: mso40uiwin32client.dll\n"
            "Exception code: 0xc0000005\n"
            "Fault offset: 0x00000000005a3b10\n"
            "Faulting application name: OUTLOOK.EXE, version: 16.0.18227.20162\n"
            "Faulting module name: mso40uiwin32client.dll\n"
            "Exception code: 0xc0000005\n"
            "Fault offset: 0x00000000005a3b10\n"
            "Faulting application name: OUTLOOK.EXE, version: 16.0.18227.20162\n"
            "Faulting module name: mso40uiwin32client.dll\n"
            "Exception code: 0xc0000005\n"
            "Fault offset: 0x00000000005a3b10\n\n"
            "This is the only email that causes it. All other emails open fine.\n"
            "I'm on {os} with Microsoft 365 Apps, Current Channel.",
            "Teams keeps freezing whenever I try to join a meeting with more than 10 "
            "participants.\n\n"
            "Error from application log:\n\n"
            "[ERROR] Teams.exe: Unhandled exception at 0x00007FFB12345678\n"
            "Memory allocation failure in MediaStack::Initialize\n"
            "[ERROR] Teams.exe: Unhandled exception at 0x00007FFB12345678\n"
            "Memory allocation failure in MediaStack::Initialize\n"
            "[ERROR] Teams.exe: Unhandled exception at 0x00007FFB12345678\n"
            "Memory allocation failure in MediaStack::Initialize\n"
            "[ERROR] Teams.exe: Unhandled exception at 0x00007FFB12345678\n"
            "Memory allocation failure in MediaStack::Initialize\n\n"
            "The error above keeps repeating in the log. I have a town hall meeting "
            "in 2 hours and need this resolved. Running {os} with 16 GB RAM.",
        ],
        next_best_actions=[
            "Diagnose Outlook crash (0xc0000005) triggered by a specific email — likely "
            "a corrupted message or embedded object.",
            "Investigate application crash caused by a specific input — review crash dumps and test in safe mode.",
        ],
        remediation_steps=[
            [
                "Identify the specific email causing the crash",
                "Attempt to open the email in the web app to confirm it is message-specific",
                "Run the application in safe mode to rule out add-in conflicts",
                "If the web app works, repair the installation or update to the latest build",
                "If the email is corrupted, remove it via an admin mailbox tool",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# dc-007  Excessive email signature / legal disclaimer
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="dc-007",
        category=Category.ACCESS_AUTH,
        priority=Priority.P3,
        assigned_team=Team.IAM,
        needs_escalation=False,
        missing_information=[MissingInfo.DEVICE_INFO],
        subjects=[
            "Badge not working at Building 6 turnstile",
            "Physical access card stopped working today",
            "Cannot get into the office — badge rejected",
        ],
        descriptions=[
            "My badge stopped working at the Building 6 main entrance this morning. "
            "I had to be let in by security. Can you please reactivate it?\n\n"
            "Thanks,\n"
            "{name}\n"
            "Vice President, Corporate Strategy\n"
            "Contoso Financial Services\n"
            "1 World Financial Center, 42nd Floor\n"
            "{office}, NY 10281\n"
            "Tel: +1 (212) 555-0142 | Mobile: +1 (917) 555-0198\n"
            "Fax: +1 (212) 555-0199\n"
            "Email: {name1}@contoso.com\n"
            "LinkedIn: linkedin.com/in/jpretorius\n\n"
            "====================================================================\n"
            "CONFIDENTIALITY NOTICE: This email message, including any attachments,\n"
            "is for the sole use of the intended recipient(s) and may contain\n"
            "confidential and privileged information. Any unauthorized review, use,\n"
            "disclosure, or distribution is prohibited. If you are not the intended\n"
            "recipient, please contact the sender by reply email and destroy all\n"
            "copies of the original message.\n\n"
            "ENVIRONMENTAL NOTICE: Please consider the environment before printing\n"
            "this email. Contoso Financial Services is committed to sustainable\n"
            "business practices.\n\n"
            "IRS CIRCULAR 230 DISCLOSURE: To ensure compliance with requirements\n"
            "imposed by the IRS, we inform you that any U.S. federal tax advice\n"
            "contained in this communication is not intended or written to be used\n"
            "for the purpose of avoiding penalties under the Internal Revenue Code.\n"
            "====================================================================",
            "Hi — I got a new badge last week but it does not work on the 22nd floor "
            "server room doors. Regular office doors work fine.\n\n"
            "Best regards,\n\n"
            "{name}\n"
            "Managing Director | Global Infrastructure\n"
            "Contoso Financial Services, Ltd.\n"
            "25 Bank Street, Canary Wharf\n"
            "London E14 5JP, United Kingdom\n"
            "Office: +44 (0)20 7946 0958\n"
            "Mobile: +44 (0)7700 900123\n"
            "Email: {name1}@contoso.com\n\n"
            "---------------------------------------------------------------\n"
            "IMPORTANT: This email is confidential and may be legally\n"
            "privileged. If you have received it in error, please notify\n"
            "the sender immediately and delete it. You must not copy,\n"
            "distribute or take any action in reliance upon it.\n\n"
            "Contoso Financial Services, Ltd. is authorised and regulated\n"
            "by the Financial Conduct Authority (FCA). Registered in\n"
            "England and Wales, Company No. 12345678.\n\n"
            "Think before you print \u2014 save paper, save trees.\n"
            "---------------------------------------------------------------",
        ],
        next_best_actions=[
            "Reactivate or replace badge for user unable to enter building turnstile.",
            "Investigate physical access card failure — check if badge was deactivated, expired, or flagged.",
        ],
        remediation_steps=[
            [
                "Look up the user's badge ID in the physical access control system",
                "Check if the badge was deactivated, expired, or flagged",
                "Reactivate the badge or issue a replacement if damaged",
                "Test badge at the turnstile before confirming with the user",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# dc-008  Mixed languages (English + non-English)
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="dc-008",
        category=Category.NETWORK,
        priority=Priority.P2,
        assigned_team=Team.NETWORK,
        needs_escalation=False,
        missing_information=[MissingInfo.NETWORK_LOCATION, MissingInfo.ENVIRONMENT_DETAILS],
        subjects=[
            "VDI session freezes / VDI\u4f1a\u8bdd\u51bb\u7ed3 / Session VDI gel\u00e9e",
            "VDI disconnects when connecting internationally",
            "Remote desktop freeze across offices",
        ],
        descriptions=[
            "Hello IT,\n\n"
            "I work across the Singapore, New York, and London offices and my VDI session "
            "has been freezing intermittently.\n\n"
            "\u5f53\u6211\u8fde\u63a5\u5230\u65b0\u52a0\u5761\u6570\u636e\u4e2d\u5fc3"
            "\u7684VDI\u65f6\uff0c\u4f1a\u8bdd\u5728\u5927\u7ea620\u5206\u949f\u540e"
            "\u51bb\u7ed3\u3002\u5c4f\u5e55\u505c\u6b62\u54cd\u5e94\uff0c\u6211\u5fc5\u987b"
            "\u65ad\u5f00\u5e76\u91cd\u65b0\u8fde\u63a5\u3002\n\n"
            "Quand je me connecte depuis le bureau de Londres, la session VDI g\u00e8le "
            "apr\u00e8s environ 20 minutes.\n\n"
            "From {office} the connection is stable. The issue only happens when I connect "
            "to the Singapore or London VDI pools. My laptop is a ThinkPad X1 Carbon Gen 11 "
            "with VMware Horizon Client 2312.",
            "Hola equipo de soporte,\n\n"
            "Estoy teniendo problemas con la conexi\u00f3n VPN desde nuestra oficina "
            "en Ciudad de M\u00e9xico. La conexi\u00f3n se cae cada 15 minutos "
            "aproximadamente.\n\n"
            "In English: The VPN connection from the Mexico City office drops every "
            "15 minutes. I am using GlobalProtect on a Dell Latitude 5540 running "
            "{os}. The local internet works fine \u2014 only the VPN tunnel is unstable.\n\n"
            'El error que aparece es: "Gateway timed out. Please try reconnecting."\n'
            'The error that shows is: "Gateway timed out. Please try reconnecting."\n\n'
            "Por favor ay\u00fadenme lo antes posible, tengo reuniones con Nueva York "
            "toda la tarde.\n"
            "Please help ASAP \u2014 I have meetings with New York all afternoon.",
        ],
        next_best_actions=[
            "Investigate VDI session freezes when user connects to remote pools — likely "
            "WAN latency or protocol configuration issue.",
            "Diagnose VPN tunnel drops from Mexico City office — check regional gateway "
            "routing and split-tunnel policy.",
        ],
        remediation_steps=[
            [
                "Review VDI connection server logs for the user's sessions in remote pools",
                "Measure round-trip latency and packet loss from the user's location to remote data centers",
                "Check if the VDI protocol is tuned for high-latency WAN links",
                "Enable performance tracking diagnostics on the client",
                "If WAN quality is the root cause, evaluate circuit optimization options",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# dc-009  Truncated message (cut off mid-sentence)
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="dc-009",
        category=Category.DATA,
        priority=Priority.P1,
        assigned_team=Team.DATA_PLATFORM,
        needs_escalation=True,
        missing_information=[MissingInfo.ENVIRONMENT_DETAILS],
        subjects=[
            "Database replication lag causing stale portfolio data",
            "SQL replication behind — dashboard showing stale numbers",
            "URGENT: data staleness on reporting dashboard",
        ],
        descriptions=[
            "We've noticed that the portfolio valuations dashboard is showing data that's "
            "approximately 45 minutes stale. The replication from the primary SQL Server "
            "to the read replica appears to be lagging.\n\n"
            "Impact: Portfolio managers are making decisions based on outdated valuations. "
            "This affects approximately 30 PMs across Wealth Management and Asset Management.\n\n"
            "What we've confirmed so far:\n"
            "- Primary database is current (checked via direct query at 14:22 ET)\n"
            "- Read replica is behind by ~2,700 transactions\n"
            "- The lag started around 13:35 ET today\n"
            "- No recent schema changes or maintenance windows\n"
            "- Disk I/O on the replica server looks elevated: avg write latency 48ms vs "
            "normal 5ms\n\n"
            "We need this resolved urgently. The EOD NAV calculation process kicks off at "
            "16:00 ET and reads from the replica. If the lag isn't cleared by then, we'll "
            "have incorrect NAV calculations which will trigger regulatory reporting "
            "discrepancies and we'll need to file correc",
            "URGENT: The nightly ETL job for the trade reconciliation system failed "
            "at 03:47 AM and the data has not been loaded into the data warehouse.\n\n"
            "The downstream dashboards that Risk and Compliance rely on are now "
            "stale \u2014 showing yesterday's data. We need this resolved before the "
            "London desk opens at 08:00 GMT.\n\n"
            "Error from the ETL log:\n"
            "- Source: TradeRecon_Extract_PROD\n"
            "- Step: DimCounterparty merge\n"
            "- Error: Violation of PRIMARY KEY constraint 'PK_Counterparty'. "
            "Cannot insert duplicate key in object 'dbo.DimCounterparty'. "
            "The duplicate key value is (89274\n\n"
            "The job has been stable for months. Last change was a schema "
            "update on the counterparty table two weeks ago. The developer who "
            "made that change is on PTO and I don't have access to the ETL "
            "configuration to check the mappi",
        ],
        next_best_actions=[
            "Urgently resolve SQL Server replication lag before 16:00 ET EOD NAV calculation "
            "\u2014 45-minute data staleness affecting 30 PMs.",
            "Investigate failed nightly ETL job blocking trade reconciliation dashboards "
            "\u2014 primary key violation in DimCounterparty merge step.",
        ],
        remediation_steps=[
            [
                "Check disk subsystem on the replica server for I/O bottleneck",
                "Review replication monitor for error states or suspended subscriptions",
                "If disk I/O is the bottleneck, identify competing workloads and throttle them",
                "Consider reinitializing replication from a snapshot if lag cannot be recovered",
                "Notify portfolio management leads of potential data staleness and EOD risk",
            ],
            [
                "Review the ETL job error log for the primary key violation details",
                "Check the DimCounterparty table for duplicate source keys introduced by the schema change",
                "Apply a deduplication fix or update the merge logic to handle the new key pattern",
                "Rerun the ETL job and verify downstream dashboards refresh",
                "Notify Risk and Compliance of the data delay and expected resolution time",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# dc-010  Application log dump pasted into ticket
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="dc-010",
        category=Category.SOFTWARE,
        priority=Priority.P2,
        assigned_team=Team.ENTERPRISE_APPS,
        needs_escalation=False,
        missing_information=[],
        subjects=[
            "Jenkins build pipeline failing since this morning",
            "CI/CD pipeline broken — full log attached",
            "Build failures on main branch — error log inside",
        ],
        descriptions=[
            "The CI/CD pipeline for the risk-engine repo has been failing since 06:15 AM.\n"
            "Here's the full console output:\n\n"
            "[2026-03-18T06:15:02Z] Starting pipeline: risk-engine/main #1847\n"
            "[2026-03-18T06:15:02Z] Checking out git repo...\n"
            "[2026-03-18T06:15:05Z] HEAD is now at a3f7c21 Merge PR #492\n"
            "[2026-03-18T06:15:05Z] Running stage: Install Dependencies\n"
            "[2026-03-18T06:15:06Z] npm ci --prefer-offline\n"
            "[2026-03-18T06:15:12Z] added 1847 packages in 6.1s\n"
            "[2026-03-18T06:15:12Z] Running stage: Build\n"
            "[2026-03-18T06:15:13Z] tsc --build tsconfig.json\n"
            "[2026-03-18T06:15:28Z] Build completed successfully\n"
            "[2026-03-18T06:15:28Z] Running stage: Unit Tests\n"
            "[2026-03-18T06:15:29Z] jest --ci --coverage\n"
            "[2026-03-18T06:16:45Z] Tests: 342 passed, 342 total\n"
            "[2026-03-18T06:16:45Z] Running stage: Integration Tests\n"
            "[2026-03-18T06:16:46Z] jest --ci --config jest.integration.config.js\n"
            "[2026-03-18T06:17:01Z] Connecting to test database: sqltest-nyc-02:1433\n"
            "[2026-03-18T06:17:16Z] ERROR: Connection refused to sqltest-nyc-02:1433\n"
            "[2026-03-18T06:17:16Z] Error: connect ECONNREFUSED 10.42.8.15:1433\n"
            "[2026-03-18T06:17:16Z] Tests: 0 passed, 18 failed, 18 total\n"
            "[2026-03-18T06:17:16Z] Pipeline FAILED at stage: Integration Tests\n\n"
            "This has failed on every retry (5 times now). The test DB seems to be down.",
            "Our internal Python deployment pipeline has been failing for the data "
            "analytics service. Here is the log:\n\n"
            "[2026-03-18T08:00:01Z] Deploying data-analytics-svc v2.14.3 to prod-east\n"
            "[2026-03-18T08:00:02Z] Pulling image: contoso.azurecr.io/data-analytics:2.14.3\n"
            "[2026-03-18T08:00:15Z] Image pulled successfully\n"
            "[2026-03-18T08:00:16Z] Starting health check...\n"
            "[2026-03-18T08:00:46Z] Health check: /healthz returned 503\n"
            "[2026-03-18T08:01:16Z] Health check: /healthz returned 503\n"
            "[2026-03-18T08:01:46Z] Health check: /healthz returned 503\n"
            "[2026-03-18T08:01:46Z] FATAL: Health check failed after 3 attempts\n"
            "[2026-03-18T08:01:47Z] Rolling back to v2.14.2\n"
            "[2026-03-18T08:01:55Z] Rollback complete. v2.14.2 is healthy.\n"
            "[2026-03-18T08:01:55Z] Deployment FAILED for v2.14.3\n\n"
            "We need v2.14.3 deployed because it contains a critical fix for "
            "the overnight batch valuation job. Can someone look at why the "
            "health check is failing?",
        ],
        next_best_actions=[
            "Restore connectivity to integration test database — CI/CD pipeline blocked since 06:15 AM.",
            "Investigate health check failure preventing deployment of data-analytics-svc "
            "v2.14.3 — service returns 503 on startup.",
        ],
        remediation_steps=[
            [
                "Check if the test database SQL Server service is running and accepting connections",
                "Verify network connectivity from the CI agent to the database server",
                "Check if there was a maintenance or patching event on the database server overnight",
                "Restart the SQL Server service if stopped and verify integration tests pass",
                "Notify the engineering team once the pipeline is green",
            ],
            [
                "Pull the v2.14.3 container locally and inspect startup logs for the 503 cause",
                "Compare environment variables and config between v2.14.2 and v2.14.3",
                "Check if a new dependency or migration was introduced that fails in the prod environment",
                "Fix the startup issue, rebuild the image, and redeploy",
                "Verify the health check passes and the overnight batch job succeeds",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# dc-011  HTML entities and escaped characters throughout
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="dc-011",
        category=Category.ACCESS_AUTH,
        priority=Priority.P1,
        assigned_team=Team.IAM,
        needs_escalation=True,
        missing_information=[MissingInfo.AUTHENTICATION_METHOD],
        subjects=[
            "Can&#39;t log in to trading platform &mdash; &quot;session expired&quot;",
            "Login failure &mdash; &quot;authentication error&quot; on {app}",
            "Account locked out &#47; session error on critical system",
        ],
        descriptions=[
            "Every time I try to log in to the Contoso Trading Platform (CTP) I get the "
            "error: &quot;Your session has expired. Please contact your administrator.&quot;\n\n"
            "I&apos;ve tried:\n"
            "1. Clearing cookies &amp; cache\n"
            "2. Using incognito&#47;private mode\n"
            "3. Trying from a different machine\n"
            "4. Resetting my password via the &quot;Forgot Password&quot; link\n\n"
            "None of these work. I&apos;m getting the same error on both my laptop &amp; "
            "my desktop. My colleagues in the same team can log in fine.\n\n"
            "This started after the maintenance window last night (March 17 &ndash; 18). "
            "I&apos;m locked out of all my positions and can&apos;t execute trades.",
            "I can&apos;t access the &quot;Risk Analytics Dashboard&quot; since "
            "this morning. When I click the link it redirects to the login page "
            "and shows: &quot;Error 401 &ndash; Unauthorized&quot;.\n\n"
            "Details:\n"
            "&#8226; URL: https://analytics.contoso.com/risk&#45;dashboard\n"
            "&#8226; Browser: {browser}\n"
            "&#8226; Time: 09:15 AM ET\n\n"
            "I&apos;ve verified my credentials are correct &amp; my account "
            "isn&apos;t locked. Other internal sites work fine &#40;SharePoint, "
            "Confluence, Jira&#41;. This dashboard is critical for our morning "
            "risk review &mdash; the entire trading desk needs the data by 10 AM.",
        ],
        next_best_actions=[
            "Restore trading platform access for user locked out after maintenance — "
            "session token or account state likely not migrated correctly.",
            "Investigate 401 Unauthorized on Risk Analytics Dashboard — verify IdP "
            "claim mappings and session cookie configuration.",
        ],
        remediation_steps=[
            [
                "Check identity provider logs for the user's failed authentication attempts",
                "Verify the user's account was not disabled or locked during maintenance",
                "Clear stale session tokens in the session store for this user",
                "If tokens were rotated during maintenance, ensure the user's IdP mapping is current",
                "Confirm login works and monitor for recurrence",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# dc-012  Duplicate sentences and stuttering content
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="dc-012",
        category=Category.SOFTWARE,
        priority=Priority.P2,
        assigned_team=Team.ENTERPRISE_APPS,
        needs_escalation=False,
        missing_information=[MissingInfo.APPLICATION_VERSION],
        subjects=[
            "Zoom phone not ringing — calls go straight to voicemail",
            "Phone system not working — incoming calls go to voicemail",
            "Calls going directly to voicemail despite status showing available",
        ],
        descriptions=[
            "My Zoom Phone has stopped ringing for incoming calls. Calls go straight to "
            "voicemail. My Zoom Phone has stopped ringing for incoming calls. Calls go "
            "straight to voicemail.\n\n"
            "I've checked my Do Not Disturb settings and they are off. I've checked my Do "
            "Not Disturb settings and they are off. The desktop client shows I'm "
            "available (green dot). The desktop client shows I'm available (green dot).\n\n"
            "My extension is 5-2201 and my direct number is +1 (212) 555-2201. Clients "
            "have been complaining they can't reach me. My extension is 5-2201 and my "
            "direct number is +1 (212) 555-2201.\n\n"
            "This started yesterday afternoon. I tried signing out and back in, same issue. "
            "This started yesterday afternoon. I tried signing out and back in, same issue.",
            "Excel keeps crashing when I open the Q1 financial model. Excel keeps "
            "crashing when I open the Q1 financial model. The file is about 45 MB "
            "and has many pivot tables. The file is about 45 MB and has many pivot "
            "tables.\n\n"
            "I've tried opening it on a different computer and same thing happens. "
            "I've tried opening it on a different computer and same thing happens. "
            "The file was working fine last week. The file was working fine last "
            "week.\n\n"
            "This is blocking the quarterly earnings preparation. Other Excel files "
            "open without issues. This is blocking the quarterly earnings "
            "preparation. Other Excel files open without issues.",
        ],
        next_best_actions=[
            "Troubleshoot phone call routing — incoming calls going directly to voicemail despite available status.",
            "Diagnose Excel crash on large workbook — likely a corrupted file or "
            "memory issue with pivot table recalculation.",
        ],
        remediation_steps=[
            [
                "Check phone admin portal for call routing rules on the user's extension",
                "Verify there is no call forwarding or after-hours rule overriding status",
                "Check if the phone license is active and properly assigned",
                "Test inbound call while monitoring the admin dashboard",
                "Update the desktop client if the version is outdated",
            ],
            [
                "Attempt to open the file in Excel safe mode to rule out add-in conflicts",
                "Try opening the file with the repair option via File > Open > Open and Repair",
                "If repair fails, extract data from the corrupted workbook into a new file",
                "Check if the issue is specific to this file or all large workbooks",
                "Update Excel to the latest build if the version is behind",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# dc-013  Extremely long verbose single email body
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="dc-013",
        category=Category.ACCESS_AUTH,
        priority=Priority.P3,
        assigned_team=Team.IAM,
        needs_escalation=False,
        missing_information=[MissingInfo.ERROR_MESSAGE, MissingInfo.SCREENSHOT_OR_ATTACHMENT],
        subjects=[
            "Account access issue — very detailed background",
            "Long explanation of my login troubles",
            "SSO problems — full history of the issue below",
        ],
        descriptions=[
            "Hi IT Team,\n\n"
            "I hope you're having a great week. I wanted to reach out because I've "
            "been having some trouble logging into the Contoso internal portal and I "
            "wanted to give you as much context as possible so you can help me "
            "efficiently. I know you're all very busy, especially with the upcoming "
            "quarter-end activities, and I really appreciate your time.\n\n"
            "Let me start from the beginning. Last Monday — that was March 9th — I "
            "came into the office early because I had a presentation for the "
            "{department} leadership team at 8:30 AM. I usually get in around 9, but "
            "since the presentation was important (it was about our Q1 forecasting "
            "model refresh, which is something we've been working on since January), "
            "I wanted to make sure everything was ready. I had my coffee, sat down at "
            "my desk on Floor {floor}, and opened my laptop.\n\n"
            "The laptop booted up fine, Windows loaded normally, and I entered my "
            "password. Everything seemed fine at first. I opened Outlook, checked a "
            "few emails from the {office} team about the Singapore market data feeds, "
            "and then tried to open the internal portal at "
            "https://portal.contoso.com to pull some reports.\n\n"
            "That's when the problem started. The browser showed a spinning wheel for "
            "about 30 seconds, then redirected me to the Microsoft login page. I "
            "entered my credentials — same password I use every day — and it just "
            "sat there for a moment, then showed an error page. I don't remember the "
            "exact error because I was in a rush for the presentation, but it was "
            "something about my session.\n\n"
            "I tried again, same thing. Tried Edge and {browser}, same result. I "
            "gave up and used my phone to access the data I needed for the "
            "presentation. The presentation went well, by the way — the leadership "
            "team was happy with the forecasting refresh approach.\n\n"
            "After the presentation, around 10:15 AM, I tried again. This time the "
            "portal loaded! I thought the issue was resolved. But then on Tuesday "
            "morning, the same thing happened. And Wednesday. It seems to happen "
            "specifically between 8:00 and 9:30 AM. After that window, it works fine.\n\n"
            "My colleague {name} in the same department has no issues. We sit next to "
            "each other, so it's not a network thing. She suggested I clear my "
            "browser cache, which I did — cleared cookies, cache, everything — but "
            "the problem persisted the next morning.\n\n"
            "I also want to mention that I changed my password two weeks ago because "
            "of the regular password rotation policy. Everything was working fine "
            "after that change for about a week before this started.\n\n"
            "Oh, I should also mention: I'm not using a VPN when this happens — I'm "
            "physically in the {office} office, connected to the corporate Wi-Fi on "
            "Floor {floor}. My laptop is a ThinkPad X1 Carbon running {os}.\n\n"
            "One more thing — I noticed that when the portal fails, the Teams "
            "desktop app also shows 'Connecting...' for a minute or two, but it "
            "eventually connects. Not sure if that's related.\n\n"
            "Anyway, I'd really appreciate it if someone could look into this. I have "
            "another important presentation next Monday and I'd like to not have to "
            "scramble on my phone again.\n\n"
            "Best regards,\n"
            "{name}\n"
            "{department}\n"
            "Contoso Financial Services\n"
            "Office: {office}, Floor {floor}",
        ],
        next_best_actions=[
            "Investigate intermittent SSO authentication failure during morning peak "
            "hours for a single user — likely a token caching or Conditional Access "
            "timing issue.",
            "Diagnose recurring portal login failures between 08:00 and 09:30 — "
            "correlate with Entra ID sign-in logs for the user.",
        ],
        remediation_steps=[
            [
                "Review Entra ID sign-in logs for the user during the reported failure window",
                "Check for Conditional Access policies that may trigger during peak authentication load",
                "Verify the user's token refresh behavior and session cookie settings",
                "Clear the user's Entra ID sessions and have them re-authenticate",
                "Monitor the next morning to confirm the issue is resolved",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# dc-014  URL-heavy content with dozens of links
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="dc-014",
        category=Category.SOFTWARE,
        priority=Priority.P3,
        assigned_team=Team.ENTERPRISE_APPS,
        needs_escalation=False,
        missing_information=[MissingInfo.APPLICATION_VERSION, MissingInfo.STEPS_TO_REPRODUCE],
        subjects=[
            "Multiple SharePoint links broken after migration",
            "Broken links across multiple sites — list below",
            "SharePoint URL redirects failing — full link list",
        ],
        descriptions=[
            "After the SharePoint migration over the weekend, many of the links we "
            "use daily are broken. I've compiled the full list of affected URLs:\n\n"
            "BROKEN LINKS:\n"
            "https://contoso.sharepoint.com/sites/Finance/Q1Reports/2026\n"
            "https://contoso.sharepoint.com/sites/Finance/Q1Reports/2025\n"
            "https://contoso.sharepoint.com/sites/RiskManagement/Policies/Current\n"
            "https://contoso.sharepoint.com/sites/RiskManagement/Policies/Archive\n"
            "https://contoso.sharepoint.com/sites/Compliance/AuditTrail/2026\n"
            "https://contoso.sharepoint.com/sites/Compliance/Procedures\n"
            "https://contoso.sharepoint.com/sites/Trading/DeskProcedures/NYC\n"
            "https://contoso.sharepoint.com/sites/Trading/DeskProcedures/LDN\n"
            "https://contoso.sharepoint.com/sites/Trading/DeskProcedures/SGP\n"
            "https://contoso.sharepoint.com/sites/HR/Benefits/2026\n"
            "https://contoso.sharepoint.com/sites/HR/OnboardingDocs\n"
            "https://contoso.sharepoint.com/sites/ITKnowledgeBase/Runbooks\n"
            "https://contoso.sharepoint.com/sites/ITKnowledgeBase/NetworkDiagrams\n"
            "https://contoso.sharepoint.com/sites/Legal/Contracts/Active\n"
            "https://contoso.sharepoint.com/sites/Legal/Contracts/Expired\n"
            "https://contoso.sharepoint.com/sites/Marketing/BrandAssets\n"
            "https://contoso.sharepoint.com/sites/Engineering/APIDocumentation\n"
            "https://contoso.sharepoint.com/sites/Engineering/DesignSpecs\n"
            "https://contoso.sharepoint.com/sites/DataPlatform/ETLPipelines\n"
            "https://contoso.sharepoint.com/sites/DataPlatform/DataCatalog\n\n"
            "All of them return either 404 or redirect to the SharePoint home page. "
            "The Finance and Risk Management links are especially urgent because "
            "quarter-end reporting starts this week.\n\n"
            "LINKS THAT STILL WORK:\n"
            "https://contoso.sharepoint.com/sites/AllCompany\n"
            "https://contoso.sharepoint.com/sites/ITSupport\n"
            "https://contoso.sharepoint.com/\n\n"
            "It looks like only the sites that were migrated are broken. The older "
            "sites that weren't part of the migration batch still work.",
        ],
        next_best_actions=[
            "Investigate broken URL redirects for migrated SharePoint sites — likely "
            "a missing URL redirection mapping from the migration tool.",
            "Audit SharePoint migration redirect rules — multiple site collections "
            "returning 404 after weekend migration.",
        ],
        remediation_steps=[
            [
                "Check the SharePoint migration log for redirect mapping configuration",
                "Verify that site redirect entries exist for all migrated site collections",
                "Create missing URL redirects in the SharePoint admin center",
                "Test a sample of the reported URLs to confirm redirects work",
                "Communicate the fix to the affected departments",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# dc-015  JSON data dump embedded in ticket body
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="dc-015",
        category=Category.DATA,
        priority=Priority.P2,
        assigned_team=Team.DATA_PLATFORM,
        needs_escalation=False,
        missing_information=[MissingInfo.ENVIRONMENT_DETAILS],
        subjects=[
            "API returning malformed JSON — payload attached",
            "Data feed JSON response is wrong — see sample",
            "Market data API returning unexpected structure",
        ],
        descriptions=[
            "The market data API started returning malformed responses around 11:30 AM. "
            "The downstream trade reconciliation service is failing because it can't "
            "parse the new structure. Here's a sample response:\n\n"
            '{"response":{"status":"partial","timestamp":"2026-03-18T11:32:45Z",'
            '"data":{"instruments":[{"symbol":"AAPL","bid":178.42,"ask":178.45,'
            '"last":178.43,"volume":14523891,"exchange":"NASDAQ","metadata":{'
            '"feed":"consolidated","delay":0,"quality":"realtime"}},'
            '{"symbol":"MSFT","bid":null,"ask":null,"last":412.87,"volume":null,'
            '"exchange":"NASDAQ","metadata":{"feed":"consolidated","delay":null,'
            '"quality":null}},{"symbol":"JPM","bid":195.20,"ask":195.23,'
            '"last":195.21,"volume":8934521,"exchange":"NYSE","metadata":{'
            '"feed":"consolidated","delay":0,"quality":"realtime"}},'
            '{"symbol":"GS","bid":null,"ask":"N/A","last":"ERR","volume":-1,'
            '"exchange":"NYSE","metadata":{"feed":"error","delay":-1,'
            '"quality":"stale"}}],"pagination":{"page":1,"total_pages":47,'
            '"total_instruments":2341},"errors":[{"code":"FEED_PARTIAL",'
            '"message":"Some instruments returned incomplete data",'
            '"affected_count":891}]},"request_id":"req-7f3a2b1c-9d4e-4a5f"}}\n\n'
            "Notice the null values for MSFT and the garbage values for GS. "
            "Before today, nulls were never returned — missing values came back as 0. "
            "This is breaking our parsing logic.",
        ],
        next_best_actions=[
            "Investigate market data API returning null and malformed values for "
            "some instruments — breaking downstream trade reconciliation parsing.",
            "Diagnose partial feed response from market data API — 891 instruments "
            "returning incomplete data since 11:30 AM.",
        ],
        remediation_steps=[
            [
                "Check the market data feed provider status page for known issues",
                "Compare the current API response schema against the documented contract",
                "Identify whether the null handling change was intentional or a regression",
                "Apply a hotfix to the parsing layer to handle nulls gracefully",
                "Notify Risk and Trading desks of potential data quality issues during the window",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# dc-016  XML/SOAP payload dumped in ticket body
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="dc-016",
        category=Category.SOFTWARE,
        priority=Priority.P2,
        assigned_team=Team.ENTERPRISE_APPS,
        needs_escalation=False,
        missing_information=[MissingInfo.ENVIRONMENT_DETAILS, MissingInfo.TIMESTAMP],
        subjects=[
            "SOAP integration with vendor system failing",
            "XML parsing error in trade settlement feed",
            "Vendor API returning invalid XML — sample included",
        ],
        descriptions=[
            "The SOAP integration with our settlement vendor has been returning "
            "errors since this morning. Here's the raw XML we're getting back:\n\n"
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            "<soap:Envelope "
            'xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" '
            'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '
            'xmlns:tns="http://vendor.settlement.com/api/v2">\n'
            "  <soap:Header>\n"
            "    <tns:AuthToken>EXPIRED_TOKEN_2026031</tns:AuthToken>\n"
            "    <tns:RequestId>SR-20260318-44291</tns:RequestId>\n"
            "  </soap:Header>\n"
            "  <soap:Body>\n"
            "    <soap:Fault>\n"
            "      <faultcode>soap:Server</faultcode>\n"
            "      <faultstring>Internal Processing Error</faultstring>\n"
            "      <detail>\n"
            "        <tns:ErrorDetail>\n"
            "          <tns:Code>AUTH-4012</tns:Code>\n"
            "          <tns:Message>Service token expired. Renew via /auth/refresh "
            "endpoint.</tns:Message>\n"
            "          <tns:Timestamp>2026-03-18T06:00:00Z</tns:Timestamp>\n"
            "          <tns:CorrelationId>c9f7a2e1-3b8d-4f5c</tns:CorrelationId>\n"
            "        </tns:ErrorDetail>\n"
            "      </detail>\n"
            "    </soap:Fault>\n"
            "  </soap:Body>\n"
            "</soap:Envelope>\n\n"
            "We normally auto-refresh the token but it looks like the token refresh "
            "endpoint is also failing. The settlement batch for today hasn't been "
            "submitted yet. We have around 4,200 trades pending settlement.",
        ],
        next_best_actions=[
            "Investigate SOAP authentication token expiration blocking settlement "
            "feed — token refresh endpoint appears to be failing as well.",
            "Urgently resolve vendor API auth failure — 4,200 trades pending settlement submission.",
        ],
        remediation_steps=[
            [
                "Verify the token refresh endpoint status and network connectivity to the vendor",
                "Manually refresh the service token via the vendor admin portal as a stop-gap",
                "Investigate why the automatic token refresh cron job failed",
                "Resubmit the pending settlement batch once authentication is restored",
                "Add monitoring alerts for token expiration to prevent recurrence",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# dc-017  Windows Event Log entries pasted verbatim
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="dc-017",
        category=Category.HARDWARE,
        priority=Priority.P2,
        assigned_team=Team.ENDPOINT,
        needs_escalation=False,
        missing_information=[MissingInfo.DEVICE_INFO],
        subjects=[
            "Laptop blue screens — Event Viewer logs below",
            "BSOD twice today — dumped the event log",
            "System crash with WHEA_UNCORRECTABLE_ERROR — event log",
        ],
        descriptions=[
            "My laptop crashed with a BSOD twice today. I copied the relevant "
            "events from Event Viewer:\n\n"
            "Log Name:      System\n"
            "Source:        Microsoft-Windows-WER-SystemErrorReporting\n"
            "Date:          3/18/2026 9:14:22 AM\n"
            "Event ID:      1001\n"
            "Task Category: None\n"
            "Level:         Error\n"
            "Keywords:      Classic\n"
            "User:          N/A\n"
            "Computer:      DESKTOP-CF7K2N9.contoso.com\n"
            "Description:\n"
            "The computer has rebooted from a bugcheck. The bugcheck was: "
            "0x00000124 (0x0000000000000000, 0xffffe48d3c458028, "
            "0x00000000bf800000, 0x0000000000000800). A dump was saved in: "
            "C:\\Windows\\MEMORY.DMP.\n\n"
            "Log Name:      System\n"
            "Source:        Microsoft-Windows-Kernel-Power\n"
            "Date:          3/18/2026 9:14:18 AM\n"
            "Event ID:      41\n"
            "Task Category: (63)\n"
            "Level:         Critical\n"
            "Keywords:      (70368744177664),(2)\n"
            "User:          SYSTEM\n"
            "Computer:      DESKTOP-CF7K2N9.contoso.com\n"
            "Description:\n"
            "The system has rebooted without cleanly shutting down first. This "
            "error could be caused if the system stopped responding, crashed, "
            "or lost power unexpectedly.\n\n"
            "Log Name:      System\n"
            "Source:        Microsoft-Windows-WHEA-Logger\n"
            "Date:          3/18/2026 9:14:17 AM\n"
            "Event ID:      18\n"
            "Task Category: None\n"
            "Level:         Error\n"
            "Description:\n"
            "A fatal hardware error has occurred. Component: Processor Core. "
            "Error Source: Machine Check Exception. Error Type: Cache Hierarchy.\n\n"
            "This happens when I'm running heavy workloads — the portfolio "
            "risk model calculations in Python. My colleague on the same model "
            "laptop doesn't have this issue.",
        ],
        next_best_actions=[
            "Investigate BSOD with WHEA_UNCORRECTABLE_ERROR (0x124) — indicates "
            "processor cache hardware fault under heavy compute load.",
            "Diagnose recurring machine check exception on user's laptop — likely "
            "failing CPU or thermal throttling issue.",
        ],
        remediation_steps=[
            [
                "Run hardware diagnostics (Lenovo Vantage or Dell SupportAssist) on the laptop",
                "Check thermal paste and fan operation — WHEA errors under load suggest overheating",
                "Update BIOS and chipset drivers to the latest version",
                "If diagnostics confirm hardware fault, initiate a laptop replacement",
                "Provide a loaner device while the replacement is being processed",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# dc-018  Full SMTP email headers included in body
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="dc-018",
        category=Category.SECURITY,
        priority=Priority.P2,
        assigned_team=Team.SECOPS,
        needs_escalation=True,
        missing_information=[],
        subjects=[
            "Suspicious email — full headers included for analysis",
            "Possible phishing — pasted the email headers below",
            "External email with spoofed sender — headers attached",
        ],
        descriptions=[
            "I received a suspicious email claiming to be from our CFO. I'm pasting "
            "the full headers so your team can analyze it:\n\n"
            "Return-Path: <bounce-1742@mail-relay.suspicious-domain.ru>\n"
            "Received: from mail-relay.suspicious-domain.ru (185.234.72.14) by\n"
            " contoso-com.mail.protection.outlook.com (10.0.0.57) with Microsoft\n"
            " SMTP Server (version=TLS1_2, cipher=TLS_ECDHE_RSA_WITH_AES_256_GCM)\n"
            " id 15.20.7472.12; Tue, 18 Mar 2026 14:23:17 +0000\n"
            "Received: from localhost (unknown [10.0.0.1]) by\n"
            " mail-relay.suspicious-domain.ru (Postfix) with ESMTP id 4F2B31A0012;\n"
            " Tue, 18 Mar 2026 14:23:15 +0000 (UTC)\n"
            "DKIM-Signature: v=1; a=rsa-sha256; d=suspicious-domain.ru;\n"
            " s=default; b=dGVzdF9zaWduYXR1cmVfZm9yX2V2YWw=\n"
            "From: CFO - Margaret Wilson <margaret.wilson@contoso.com>\n"
            "Reply-To: margaret.wilson.urgent@gmail.com\n"
            "To: {name} <{name1}@contoso.com>\n"
            "Subject: Wire transfer needed urgently\n"
            "Date: Tue, 18 Mar 2026 14:23:10 +0000\n"
            "Message-ID: <fake-id-938271@suspicious-domain.ru>\n"
            "MIME-Version: 1.0\n"
            "Content-Type: text/html; charset=UTF-8\n"
            "X-Mailer: PHPMailer 6.5.0\n"
            "X-MS-Exchange-Organization-SCL: 5\n"
            "X-MS-Exchange-Organization-AuthSource: contoso-com.mail.protection.outlook.com\n"
            "Authentication-Results: spf=fail (sender IP is 185.234.72.14)\n"
            " smtp.mailfrom=suspicious-domain.ru; dkim=fail;\n"
            " dmarc=fail action=quarantine header.from=contoso.com;\n"
            " compauth=fail reason=000\n\n"
            "The email body asked me to urgently wire $25,000 to an external "
            "account. The From address looks like our CFO but the Reply-To is a "
            "Gmail address. SPF, DKIM, and DMARC all fail.",
        ],
        next_best_actions=[
            "Investigate confirmed phishing attempt with spoofed CFO identity — "
            "SPF/DKIM/DMARC all fail, originating from suspicious-domain.ru.",
            "Flag as BEC/spear-phishing targeting finance personnel — sender "
            "spoofing executive identity with wire transfer request.",
        ],
        remediation_steps=[
            [
                "Block the sender domain and IP address in Exchange transport rules",
                "Search for other recipients of the same campaign using message trace",
                "Verify no user has responded to or acted on the wire transfer request",
                "Report the phishing domain to Microsoft and relevant abuse contacts",
                "Send a targeted awareness alert to the Finance department",
                "Review mail flow rules to ensure DMARC reject policy is enforced",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# dc-019  Auto-generated notification mixed with user comment
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="dc-019",
        category=Category.SOFTWARE,
        priority=Priority.P3,
        assigned_team=Team.ENTERPRISE_APPS,
        needs_escalation=False,
        missing_information=[MissingInfo.STEPS_TO_REPRODUCE],
        subjects=[
            "Re: [AUTOMATED] System alert — Outlook sync failure",
            "RE: [AUTO-NOTIFICATION] License expiring — action needed",
            "Re: [SYSTEM] Your application update failed",
        ],
        descriptions=[
            "--- User comment below ---\n\n"
            "Hi, I keep getting these automated emails about Outlook sync failure. "
            "My Outlook IS actually having sync issues — calendar events from my "
            "phone don't show up on my laptop. Can someone look into this?\n\n"
            "--- Original automated notification ---\n\n"
            "THIS IS AN AUTOMATED MESSAGE — DO NOT REPLY DIRECTLY\n"
            "============================================\n"
            "Alert Type: Application Sync Failure\n"
            "Severity: Warning\n"
            "Timestamp: 2026-03-18T08:15:00Z\n"
            "Service: Exchange Online\n"
            "Component: ActiveSync\n"
            "User: {name1}@contoso.com\n"
            "Device: iPhone 15 Pro (iOS 19.3)\n"
            "Error Code: 0x80072EFD\n"
            "Consecutive Failures: 47\n"
            "Last Successful Sync: 2026-03-16T22:41:00Z\n"
            "============================================\n"
            "This notification was generated by the Contoso IT Monitoring System.\n"
            "To manage your notification preferences, visit "
            "https://monitoring.contoso.com/preferences\n"
            "Contoso Financial Services | IT Operations\n"
            "Support: itsupport@contoso.com | Ext: 4357",
            "I'm replying to this automated alert because the problem it describes "
            "is real.\n\n"
            "--- BEGIN AUTOMATED ALERT ---\n"
            "[NOTIFICATION] Application Update Failure\n"
            "Agent: Intune MDM\n"
            "Device: DESKTOP-CF7K2N9\n"
            "User: {name1}@contoso.com\n"
            "Application: Microsoft Teams (v24.7.0)\n"
            "Target Version: v24.8.1\n"
            "Status: FAILED\n"
            "Error: 0x80070005 (Access Denied)\n"
            "Retry Count: 3/3\n"
            "Action Required: Manual intervention needed\n"
            "--- END AUTOMATED ALERT ---\n\n"
            "Teams won't update and I keep getting prompted. Can you push the "
            "update from your side?",
        ],
        next_best_actions=[
            "Troubleshoot Exchange ActiveSync failure — phone hasn't synced in 2 days with 47 consecutive errors.",
            "Resolve Intune-managed Teams update failure — access denied error after 3 retry attempts.",
        ],
        remediation_steps=[
            [
                "Check Exchange Online ActiveSync logs for the user's device",
                "Verify the device partnership status in Exchange admin center",
                "Remove and re-add the Exchange account on the user's mobile device",
                "Confirm calendar and email sync is restored",
            ],
            [
                "Check Intune device compliance and app deployment status",
                "Verify that the Teams update package has the correct permissions",
                "Manually trigger the update deployment from Intune admin center",
                "Confirm the update installs successfully on the device",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# dc-020  Excessive whitespace, blank lines, and formatting noise
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="dc-020",
        category=Category.NETWORK,
        priority=Priority.P3,
        assigned_team=Team.NETWORK,
        needs_escalation=False,
        missing_information=[MissingInfo.NETWORK_LOCATION, MissingInfo.DEVICE_INFO],
        subjects=[
            "WiFi keeps dropping",
            "Internet connection unstable",
            "Wireless network issues on my floor",
        ],
        descriptions=[
            "\n\n\n\n"
            "   Hi   IT   Team   ,\n"
            "\n\n\n"
            "   My    wifi    keeps    dropping    out   .   "
            "   It    happens    every    30    minutes    or    so   .\n"
            "\n\n\n\n\n"
            "   I    have    to    disconnect    and    reconnect    every    time   .\n"
            "\n\n\n"
            "   I'm    on    the    {floor}    floor   .    "
            "   It    started    about    3    days    ago   .\n"
            "\n\n\n\n\n\n"
            "   Other    people    near    me    seem    fine    though   .\n"
            "\n\n\n\n"
            "   Thanks\n"
            "\n\n\n\n\n\n\n"
            "   {name}\n\n\n\n",
            "\n\n\n"
            "\t\t\tHello,\n"
            "\n\n\n\n"
            "\t\t\tI can't stay connected to the WiFi.\n"
            "\n\n"
            "\t\t\tIt drops every hour or so and I lose my VPN.\n"
            "\n\n\n\n\n"
            "\t\t\tI'm on {os} and using the built-in WiFi adapter.\n"
            "\n\n\n\n\n\n"
            "\t\t\tPlease help.\n"
            "\n\n\n\n",
        ],
        next_best_actions=[
            "Diagnose intermittent WiFi disconnects for a single user — other "
            "nearby users unaffected, suggesting a client-side issue.",
            "Investigate recurring wireless drops — check WiFi adapter driver and power management settings.",
        ],
        remediation_steps=[
            [
                "Check WiFi adapter driver version and update if outdated",
                "Disable WiFi power management in the adapter advanced settings",
                "Forget and rejoin the corporate WiFi network",
                "If issue persists, check for interference from nearby APs or Bluetooth devices",
                "Test with a USB WiFi adapter to rule out a hardware fault",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# dc-021  OCR artifact text from screenshot paste
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="dc-021",
        category=Category.SOFTWARE,
        priority=Priority.P3,
        assigned_team=Team.ENTERPRISE_APPS,
        needs_escalation=False,
        missing_information=[MissingInfo.ERROR_MESSAGE, MissingInfo.SCREENSHOT_OR_ATTACHMENT],
        subjects=[
            "Error message from app — copied from screen",
            "Pasted the error from my screen",
            "App crash error text — OCR from screenshot",
        ],
        descriptions=[
            "I tried to copy the error from my screen using the Snipping Tool text "
            "extraction. Here's what it picked up:\n\n"
            "Mrcrosoft Exc el\n"
            "Sorry, we ran lnto a problem.\n\n"
            "We recommend you save a capy of your work\n"
            "and restort Exce|.\n\n"
            "An unexoected errar occurred with error code:\n"
            "OxE06D73 73\n\n"
            "Desc.ription: Memory a| location foiled while\n"
            "processing workb0ok ca|culation chain.\n\n"
            "[Repoir & Restort] [C|ose]\n\n"
            "This happens whenever I open the quarterly risk model spreadsheet "
            "({name}'s file). It's about 85 MB with lots of formulas and VBA macros.",
            "Got this error when opening {app}. I used my phone to take a photo "
            "and the OCR is a bit messy:\n\n"
            "The appl ication 'Contoso Risk Ca|cu|ator'\n"
            "has st0pped work ing\n\n"
            "Prob|em Event Nome: APPCRASH\n"
            "Applicotion Nome: RiskCa1c.exe\n"
            "Applicotion Version: 4.2.1.0\n"
            "Applicotion Timestomp: 5f8a2c3b\n"
            "Fou|t Modu|e Nome: ntdl|.d||\n"
            "Fou|t Module Version: 1O.O.226OO.3810\n"
            "Exception Code: 0xc0000005\n\n"
            "This started after the latest Windows update. The app worked fine "
            "before last Tuesday.",
        ],
        next_best_actions=[
            "Investigate Excel crash with memory allocation error on large workbook — "
            "likely hitting 32-bit memory limits or VBA compatibility issue.",
            "Diagnose RiskCalc.exe application crash — access violation in ntdll.dll "
            "after recent Windows update, likely a compatibility regression.",
        ],
        remediation_steps=[
            [
                "Check if the user is running 32-bit or 64-bit Excel — large workbooks need 64-bit",
                "Disable VBA macros temporarily to see if the crash is macro-related",
                "Repair the Office installation via Control Panel",
                "If using 32-bit, migrate the user to 64-bit Office",
                "Test the workbook in Protected View to rule out file corruption",
            ],
            [
                "Check Windows Update history for recent patches that may affect compatibility",
                "Run the application in compatibility mode for the previous Windows version",
                "Check for a vendor update to the RiskCalc application",
                "If no update is available, roll back the problematic Windows update for this machine",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# dc-022  CSV/tabular data pasted into ticket body
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="dc-022",
        category=Category.DATA,
        priority=Priority.P2,
        assigned_team=Team.DATA_PLATFORM,
        needs_escalation=False,
        missing_information=[MissingInfo.ENVIRONMENT_DETAILS],
        subjects=[
            "Data discrepancies in the NAV report — comparison table",
            "Mismatched values between source and dashboard — data below",
            "ETL output doesn't match source — pasted comparison",
        ],
        descriptions=[
            "We found discrepancies between the source system and the reporting "
            "dashboard for yesterday's NAV calculations. Here's the comparison I "
            "pulled from both systems:\n\n"
            "Fund_ID,Fund_Name,Source_NAV,Dashboard_NAV,Delta,Delta_Pct\n"
            "FND-001,Contoso Growth Fund,142587631.42,142587631.42,0.00,0.000%\n"
            "FND-002,Contoso Value Fund,89234112.87,89231445.21,2667.66,0.003%\n"
            "FND-003,Contoso Income Fund,234891004.19,234891004.19,0.00,0.000%\n"
            "FND-004,Contoso Global Equity,178432901.55,178429876.33,3025.22,0.002%\n"
            "FND-005,Contoso Fixed Income,312445678.90,312445678.90,0.00,0.000%\n"
            "FND-006,Contoso Balanced Fund,67891234.56,67888901.23,2333.33,0.003%\n"
            "FND-007,Contoso Small Cap,45678901.23,45678901.23,0.00,0.000%\n"
            "FND-008,Contoso Emerging Mkts,23456789.01,23454321.98,2467.03,0.011%\n"
            "FND-009,Contoso Real Estate,56789012.34,56789012.34,0.00,0.000%\n"
            "FND-010,Contoso Money Market,891234567.89,891234567.89,0.00,0.000%\n\n"
            "Funds FND-002, FND-004, FND-006, and FND-008 all have small but "
            "non-zero deltas. The discrepancies look like rounding or truncation "
            "differences but they're triggering our reconciliation exception report "
            "because they exceed the $1,000 threshold.\n\n"
            "The issue started after the ETL pipeline was updated last weekend.",
        ],
        next_best_actions=[
            "Investigate NAV calculation discrepancies in 4 funds after ETL "
            "pipeline update — deltas suggest a rounding/truncation regression.",
            "Audit the ETL pipeline change from last weekend — NAV values show "
            "small but consistent discrepancies exceeding reconciliation threshold.",
        ],
        remediation_steps=[
            [
                "Compare the ETL pipeline code before and after the weekend update",
                "Check for changes in decimal precision, rounding mode, or data type casting",
                "Run the ETL for affected funds in a test environment with before/after code",
                "Fix the rounding regression and reprocess the affected fund calculations",
                "Verify all funds reconcile within threshold after the fix",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# dc-023  Phone transcript with filler words and speech artifacts
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="dc-023",
        category=Category.ACCESS_AUTH,
        priority=Priority.P2,
        assigned_team=Team.IAM,
        needs_escalation=False,
        missing_information=[MissingInfo.ERROR_MESSAGE, MissingInfo.DEVICE_INFO],
        subjects=[
            "Phone call transcript — user locked out of account",
            "Voicemail transcript — MFA issue",
            "Call-in request — SSO not working (transcript)",
        ],
        descriptions=[
            "[Auto-transcribed from phone call received 2026-03-18 09:42 AM]\n\n"
            "Hi um yeah this is um {name} from the uh {department} department. "
            "I'm calling because um I I can't log into my my account this morning. "
            "So like I I was trying to uh to sign in and uh it asked for my "
            "password which I entered and then it it went to the MFA screen like "
            "like it usually does but uh the the push notification never came "
            "to my phone. I waited like uh like five minutes and nothing. So then "
            "I tried the um the text message option and it said uh it said "
            "something about my my number not being registered or something? "
            "I don't I don't know what happened because it it was working fine "
            "yesterday. Um I I got a new phone last weekend — an iPhone — and I "
            "transferred everything over but maybe maybe the MFA didn't transfer? "
            "I I really need to get in because we have the uh the quarterly "
            "compliance review at uh at ten thirty and I need to pull the reports "
            "from the the portal. Can can someone help me please? My my extension "
            "is uh four four seven two. Thanks bye.",
            "[Auto-transcribed from voicemail left 2026-03-18 08:15 AM]\n\n"
            "Yeah hey this is um this is {name} uh from {department}. So uh I'm "
            "having a a problem with my uh my login. The the SSO page keeps uh "
            "keeps giving me an error when I when I try to sign in. It says uh "
            "something like [INAUDIBLE] authentication [INAUDIBLE] failed or "
            "something. I I've tried like three times and and it's the same same "
            "thing each time. I think it might might be because [BACKGROUND NOISE] "
            "my password uh expired? I'm I'm not sure though because I I didn't "
            "get any any email about it. Um anyway can someone uh call me back "
            "at uh at extension [INAUDIBLE] or uh or just email me at "
            "{name1}@contoso.com. This is this is kind of urgent because I I "
            "can't do any work until until I can log in. Thanks.",
        ],
        next_best_actions=[
            "Help user re-register MFA after phone replacement — push notifications "
            "not transferring to new device requires MFA method re-enrollment.",
            "Investigate SSO authentication failure — user may have expired password or stale MFA registration.",
        ],
        remediation_steps=[
            [
                "Verify the user's identity through an out-of-band method",
                "Reset the user's MFA registration in Entra ID",
                "Walk the user through re-enrolling MFA on the new phone",
                "Test the login flow end-to-end with the user on the line",
                "Confirm access to the compliance portal before closing",
            ],
            [
                "Check if the user's password has expired in Entra ID",
                "If expired, initiate a password reset via the admin center",
                "Verify MFA methods are properly registered and active",
                "Have the user sign in again and confirm SSO works",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# dc-024  Multiple forwarded chain with overlapping signatures
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="dc-024",
        category=Category.GENERAL,
        priority=Priority.P4,
        assigned_team=Team.NONE,
        needs_escalation=False,
        missing_information=[MissingInfo.AFFECTED_SYSTEM, MissingInfo.BUSINESS_IMPACT],
        subjects=[
            "FW: FW: FW: RE: Office move — IT setup needed",
            "Fwd: Fwd: RE: RE: Desk relocation IT requirements",
            "FW: RE: FW: Floor 7 to Floor 3 move — equipment",
        ],
        descriptions=[
            "Can IT help with this? See the chain below.\n\n"
            "---\n"
            "{name}\n"
            "Vice President, {department}\n"
            "Contoso Financial Services\n"
            "Tel: +1-212-555-0142 | Ext: 4721\n"
            "Email: {name1}@contoso.com\n"
            "Level 23, 300 Park Avenue, New York, NY 10022\n\n"
            "CONFIDENTIALITY NOTICE: This email and any attachments are for the "
            "exclusive use of the intended recipient(s).\n\n"
            "---------- Forwarded message ----------\n"
            "From: {name2}@contoso.com\n"
            "Date: Mon, Mar 16, 2026 at 3:15 PM\n"
            "Subject: RE: Office move — IT setup needed\n"
            "To: {name1}@contoso.com\n\n"
            "Yes, please forward to IT. We need the desks set up by Friday.\n\n"
            "---\n"
            "{name2}\n"
            "Director, Operations\n"
            "Contoso Financial Services\n"
            "Tel: +1-212-555-0198 | Ext: 3892\n"
            "Email: {name2}@contoso.com\n"
            "Level 22, 300 Park Avenue, New York, NY 10022\n\n"
            "---------- Forwarded message ----------\n"
            "From: {name3}@contoso.com\n"
            "Date: Mon, Mar 16, 2026 at 2:45 PM\n"
            "Subject: RE: Office move — IT setup needed\n"
            "To: {name2}@contoso.com\n\n"
            "Five people from my team are moving from Floor 7 to Floor 3 next "
            "Monday. They'll need their monitors, docking stations, and phones "
            "moved.\n\n"
            "---\n"
            "{name3}\n"
            "Manager, Portfolio Analytics\n"
            "Contoso Financial Services\n"
            "Tel: +1-212-555-0167 | Ext: 5501\n"
            "Email: {name3}@contoso.com\n"
            "Level 21, 300 Park Avenue, New York, NY 10022\n\n"
            "DISCLAIMER: This message is intended only for the individual(s) "
            "addressed above. If you have received this in error, please notify "
            "the sender immediately.",
        ],
        next_best_actions=[
            "Process office relocation request for 5 users moving from Floor 7 "
            "to Floor 3 — coordinate monitor, docking station, and phone moves.",
        ],
        remediation_steps=[
            [
                "Confirm the list of 5 employees being relocated and their new desk assignments",
                "Schedule the equipment move for the weekend before Monday",
                "Coordinate with facilities for network port activation on Floor 3",
                "Verify docking stations, monitors, and desk phones work at the new locations",
                "Notify the users once setup is complete",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# dc-025  Markdown formatting artifacts in plain text ticket
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="dc-025",
        category=Category.SOFTWARE,
        priority=Priority.P3,
        assigned_team=Team.ENTERPRISE_APPS,
        needs_escalation=False,
        missing_information=[MissingInfo.APPLICATION_VERSION],
        subjects=[
            "**URGENT** — Teams not working properly",
            "# Teams meeting issue — please help",
            "Teams [video/audio] problems during calls",
        ],
        descriptions=[
            "## Issue Summary\n\n"
            "**Microsoft Teams** is giving me problems during meetings.\n\n"
            "### What's happening:\n"
            "- [x] Audio cuts out every ~30 seconds\n"
            "- [x] Video freezes and shows `pixelated artifacts`\n"
            "- [ ] Screen sharing — _haven't tested yet_\n"
            "- [ ] Chat works fine (**no issues there**)\n\n"
            "### Steps I've tried:\n"
            "1. ~~Restarted Teams~~ — didn't help\n"
            "2. ~~Cleared Teams cache~~ — didn't help\n"
            "3. Checked internet speed — `ping 8.8.8.8` shows ***<5ms latency***\n"
            "4. Tried the [web version](https://teams.microsoft.com) — "
            "same issue\n\n"
            "### Environment:\n"
            "| Component | Value |\n"
            "|-----------|-------|\n"
            "| OS | {os} |\n"
            "| Teams | Desktop app |\n"
            "| Network | Corporate WiFi |\n"
            "| Location | {office}, Floor {floor} |\n\n"
            "> **Note**: My colleague sitting next to me has no issues, so it's "
            "probably not the network.\n\n"
            "---\n"
            "Thanks!",
            "# Help needed with {app}\n\n"
            "The app keeps **crashing** when I try to open _large files_.\n\n"
            "```\n"
            "Error: OutOfMemoryException\n"
            "at System.Windows.Forms.Control.CreateHandle()\n"
            "```\n\n"
            "## Details\n"
            "* File size: ~200MB\n"
            "* Format: `.xlsx`\n"
            "* Works fine for files under ~50MB\n\n"
            "~~I thought it was a RAM issue but I have 32GB.~~\n\n"
            "[Link to the file](https://contoso.sharepoint.com/sites/Finance/shared/bigfile.xlsx)\n\n"
            "**Priority**: High — I need this for quarter-end reporting.",
        ],
        next_best_actions=[
            "Troubleshoot Teams audio/video degradation during meetings — likely "
            "a codec or media stack issue since network connectivity is fine.",
            "Investigate application crash with OutOfMemoryException on large files — "
            "may be a 32-bit process limitation despite sufficient system RAM.",
        ],
        remediation_steps=[
            [
                "Check Teams client logs for media stack errors during a call",
                "Verify GPU hardware acceleration is enabled in Teams settings",
                "Update the Teams client to the latest version",
                "Test with a wired Ethernet connection to eliminate WiFi as a factor",
                "If the issue persists, collect a Teams diagnostic log during a meeting",
            ],
            [
                "Check whether the application is running as a 32-bit process",
                "If 32-bit, migrate to the 64-bit version of the application",
                "Verify available memory during the crash using Task Manager",
                "Test opening the file on another machine to rule out file corruption",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# dc-026  Large error stack trace with file paths
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="dc-026",
        category=Category.SOFTWARE,
        priority=Priority.P1,
        assigned_team=Team.ENTERPRISE_APPS,
        needs_escalation=True,
        missing_information=[],
        subjects=[
            "Production app crashing — full stack trace",
            "Risk engine throwing unhandled exception — trace below",
            "Critical app failure — complete error dump",
        ],
        descriptions=[
            "The risk calculation engine crashed in production about 20 minutes "
            "ago. Here's the full exception with stack trace:\n\n"
            "Unhandled Exception: System.InvalidOperationException: "
            "Failed to compute VaR for portfolio batch 2026-Q1-BATCH-047\n"
            "   ---> System.Data.SqlClient.SqlException: Timeout expired. The "
            "timeout period elapsed prior to completion of the operation or the "
            "server is not responding.\n"
            "   at System.Data.SqlClient.SqlInternalConnection.OnError("
            "SqlException exception, Boolean breakConnection)\n"
            "   at System.Data.SqlClient.TdsParser.ThrowExceptionAndWarning("
            "TdsParserStateObject stateObj)\n"
            "   at System.Data.SqlClient.TdsParser.TryRun(RunBehavior "
            "runBehavior, SqlCommand cmdHandler)\n"
            "   at System.Data.SqlClient.SqlDataReader.TryConsumeMetaData()\n"
            "   at System.Data.SqlClient.SqlDataReader.get_MetaData()\n"
            "   at System.Data.SqlClient.SqlCommand.FinishExecuteReader("
            "SqlDataReader ds, RunBehavior runBehavior, String resetOptionsString)\n"
            "   at Contoso.RiskEngine.DataAccess.PortfolioRepository."
            "GetPositions(String batchId) in "
            "D:\\BuildAgent\\work\\src\\RiskEngine\\DataAccess\\"
            "PortfolioRepository.cs:line 247\n"
            "   at Contoso.RiskEngine.Calculations.VaRCalculator."
            "ComputeBatchVaR(PortfolioBatch batch) in "
            "D:\\BuildAgent\\work\\src\\RiskEngine\\Calculations\\"
            "VaRCalculator.cs:line 89\n"
            "   at Contoso.RiskEngine.Services.BatchProcessor."
            "ProcessBatch(Int32 batchId) in "
            "D:\\BuildAgent\\work\\src\\RiskEngine\\Services\\"
            "BatchProcessor.cs:line 156\n"
            "   at Contoso.RiskEngine.Services.SchedulerService."
            "ExecuteScheduledRun() in "
            "D:\\BuildAgent\\work\\src\\RiskEngine\\Services\\"
            "SchedulerService.cs:line 42\n"
            "   --- End of inner exception stack trace ---\n"
            "   at Contoso.RiskEngine.Program.Main(String[] args) in "
            "D:\\BuildAgent\\work\\src\\RiskEngine\\Program.cs:line 28\n\n"
            "This batch contains VaR calculations for approximately 1,200 "
            "portfolios. The risk reports are due to the regulators by 4 PM ET "
            "today. The database query timeout is currently set to 30 seconds.",
        ],
        next_best_actions=[
            "Urgently resolve risk engine database timeout — VaR batch processing "
            "failed for 1,200 portfolios with regulatory deadline at 4 PM ET.",
        ],
        remediation_steps=[
            [
                "Check the database server resource utilization (CPU, memory, I/O)",
                "Investigate long-running queries or blocking sessions on the database",
                "Increase the command timeout for the batch processing connection string",
                "If database is healthy, check for data volume growth in the portfolio batch",
                "Rerun the batch once the timeout issue is resolved",
                "Notify the Risk team of the delay and expected completion time",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# dc-027  Zero-width and invisible Unicode characters in text
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="dc-027",
        category=Category.NETWORK,
        priority=Priority.P3,
        assigned_team=Team.NETWORK,
        needs_escalation=False,
        missing_information=[MissingInfo.NETWORK_LOCATION, MissingInfo.ERROR_MESSAGE],
        subjects=[
            "VPN\u200b \u200bcon\u200bnection \u200bfailing \u200bsince \u200bthis \u200bmorning",
            "Can\u200b't\u200b connect\u200b to\u200b corporate\u200b VPN\u200b from\u200b home",
            "VPN\u200b\u200b drops\u200b\u200b every\u200b\u200b few\u200b\u200b minutes",
        ],
        descriptions=[
            "I\u2019m working from home today and my VPN connection keeps "
            "fail\u200bing. I\u200b try to con\u200bnect using Global\u200bProtect "
            "and it shows \u200b\u200b\u200b\u2018Con\u200bnecting\u2026\u2019\u200b "
            "for about 30 se\u200bconds then drops back to \u200b\u200b\u200b"
            "\u2018Dis\u200bcon\u200bnected\u2019.\u200b\u200b\n\n"
            "My in\u200bternet con\u200bnection is fine \u2014\u200b I can browse "
            "the web and stream video\u200b\u200b with\u200bout issues\u200b. "
            "The VPN\u200b was work\u200bing fine yester\u200bday.\n\n"
            "I\u200b\u2019ve tried:\n"
            "\u200b- Re\u200bstarting my lap\u200btop\u200b\n"
            "- Re\u200binstalling the VPN\u200b cli\u200bent\u200b\n"
            "\u200b- Con\u200bnecting to a dif\u200bferent Wi\u200b-Fi net\u200bwork\n\n"
            "Noth\u200bing helped. I\u200b have a meet\u200bing at 2 PM that "
            "re\u200bquires ac\u200bcess to inter\u200bnal sys\u200btems.\u200b",
            "VPN\u200b\u200b isn\u2019t\u200b\u200b working\u200b from\u200b "
            "my\u200b home\u200b office\u200b.\u200b\u200b The\u200b "
            "Global\u200bProtect\u200b client\u200b shows\u200b an\u200b "
            "error\u200b about\u200b\u200b \u200b\u2018gate\u200bway "
            "un\u200breach\u200bable\u2019\u200b.\u200b\u200b\n\n"
            "I\u200b\u2019m\u200b on\u200b a\u200b {os}\u200b lap\u200btop.\u200b "
            "This\u200b is\u200b the\u200b first\u200b time\u200b this\u200b "
            "has\u200b happened\u200b.\u200b Other\u200b people\u200b on\u200b "
            "my\u200b team\u200b are\u200b also\u200b having\u200b issues\u200b "
            "connecting\u200b from\u200b home\u200b today\u200b.",
        ],
        next_best_actions=[
            "Investigate VPN gateway connectivity issue — user (and potentially "
            "other remote workers) unable to establish VPN tunnel.",
            "Diagnose GlobalProtect VPN connection failure from remote locations "
            "— gateway unreachable error suggests a server-side issue.",
        ],
        remediation_steps=[
            [
                "Check the VPN gateway health and service status",
                "Verify the VPN gateway's public IP is reachable from external networks",
                "Check if there was a firewall or DNS change affecting the VPN endpoint",
                "If the gateway is down, failover to the secondary VPN gateway",
                "Notify affected remote users once connectivity is restored",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# dc-028  RTF / Rich Text formatting markup noise
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="dc-028",
        category=Category.DATA,
        priority=Priority.P2,
        assigned_team=Team.DATA_PLATFORM,
        needs_escalation=False,
        missing_information=[MissingInfo.AFFECTED_SYSTEM, MissingInfo.ERROR_MESSAGE],
        subjects=[
            "Network drive mapping failure — details below",
            "Can't access shared drive — see description",
            "Mapped drive disappeared after reboot",
        ],
        descriptions=[
            r"{\rtf1\ansi\ansicpg1252\deff0\nouicompat{\fonttbl{\f0\fswiss\fcharset0 "
            r"Calibri;}{\f1\fnil\fcharset0 Calibri;}}"
            r"\viewkind4\uc1"
            r"\pard\sa200\sl276\slmult1\f0\fs22\lang9 "
            r"Hi IT Support,\par"
            r"\par"
            r"\b The network drive \\\\contoso-fs01\\{department} is no longer accessible "
            r"from my laptop.\b0\par"
            r"\par"
            r"I\rquote ve been using this drive for years and it was working fine until "
            r"this morning. When I try to open it in File Explorer, I get a "
            r"\i red X\i0  on the drive icon and it says \ldblquote The network path was "
            r"not found.\rdblquote\par"
            r"\par"
            r"I\rquote ve tried:\par"
            r"{\pntext\f1 1.\tab}Disconnecting and remapping the drive\par"
            r"{\pntext\f1 2.\tab}Running \f1 net use\f0  from the command line\par"
            r"{\pntext\f1 3.\tab}Restarting my laptop\par"
            r"\par"
            r"Nothing works. Other colleagues in {department} can still access it. "
            r"I need this drive for my daily reports.\par"
            r"\par"
            r"Thanks,\par"
            r"{name}\par"
            r"}",
            r"{\rtf1\ansi{\fonttbl{\f0 Times New Roman;}}\f0\fs24 "
            r"\pard Dear IT,\par\par"
            r"My mapped drive (letter H:) to \\\\contoso-nas\\shared\\{department} "
            r"stopped working after the {os} update last night. \par\par"
            r"\b Steps tried:\b0\par"
            r"\tab - Ran \i gpupdate /force\i0\par"
            r"\tab - Checked Group Policy for drive mappings\par"
            r"\tab - Verified I can ping contoso-nas from command prompt\par\par"
            r"The ping works but the drive won\rquote t map. Error: \ldblquote System "
            r"error 53 has occurred. The network path was not found.\rdblquote\par\par"
            r"This is blocking my end-of-day reconciliation.\par"
            r"}",
        ],
        next_best_actions=[
            "Investigate network drive mapping failure — user cannot access file share "
            "despite network connectivity. Likely a DNS, SMB, or Group Policy issue.",
            "Diagnose mapped drive loss after OS update — ping succeeds but drive "
            "mapping fails with 'network path not found', suggesting SMB version mismatch.",
        ],
        remediation_steps=[
            [
                "Verify the file server (contoso-fs01 or contoso-nas) is online and the share is accessible",
                "Check DNS resolution for the file server hostname from the user's machine",
                "Verify SMB protocol version compatibility after the recent OS update",
                "Re-apply Group Policy drive mappings or manually remap via net use",
                "If SMB1 was disabled by the update, ensure the share supports SMB2/3",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# dc-029  Email reply chain with conflicting information
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="dc-029",
        category=Category.ACCESS_AUTH,
        priority=Priority.P3,
        assigned_team=Team.IAM,
        needs_escalation=False,
        missing_information=[MissingInfo.AUTHENTICATION_METHOD],
        subjects=[
            "Re: Re: Re: Re: Multiple issues — latest is password reset",
            "RE: FW: RE: Various problems — need password help now",
            "Re: Re: Re: FW: Different issue each time — password locked out",
        ],
        descriptions=[
            "Hi, I need my password reset please. I'm locked out of my account "
            "as of this morning.\n\n"
            "--- Original Message ---\n"
            "From: {name} <{name1}@contoso.com>\n"
            "Sent: Wednesday, March 18, 2026 2:15 PM\n"
            "To: IT Support <itsupport@contoso.com>\n"
            "Subject: Re: Re: Re: Multiple issues\n\n"
            "Actually, forget about the printer. My VPN is now dropping every "
            "20 minutes. This is a bigger problem.\n\n"
            "--- Original Message ---\n"
            "From: {name} <{name1}@contoso.com>\n"
            "Sent: Tuesday, March 17, 2026 9:00 AM\n"
            "To: IT Support <itsupport@contoso.com>\n"
            "Subject: Re: Re: Multiple issues\n\n"
            "Update: the monitor issue fixed itself but now the printer on "
            "Floor {floor} is jammed. Can someone look at it?\n\n"
            "--- Original Message ---\n"
            "From: {name} <{name1}@contoso.com>\n"
            "Sent: Monday, March 16, 2026 8:30 AM\n"
            "To: IT Support <itsupport@contoso.com>\n"
            "Subject: Multiple issues\n\n"
            "Hi IT, my external monitor is not being detected by my laptop. "
            "I've tried different cables and ports.",
            "My account is locked — I've tried my password 5 times and it "
            "won't let me in. Please reset ASAP.\n\n"
            "On Wed, Mar 18, 2026 at 1:00 PM, I wrote:\n"
            "> Scratch the Outlook thing — it synced after I restarted.\n"
            "> But now I can't print to the HP on Floor {floor}.\n\n"
            "On Tue, Mar 17, 2026 at 10:00 AM, IT Support wrote:\n"
            "> We've looked at your Outlook sync issue. Can you try removing "
            "and re-adding your email account?\n\n"
            "On Mon, Mar 16, 2026 at 9:00 AM, I wrote:\n"
            "> My Outlook won't sync on my phone. Also my {vpn} VPN is slow. "
            "And the WiFi in Building 2 keeps dropping.\n\n"
            "IGNORE the previous messages — I just need a password reset now.",
        ],
        next_best_actions=[
            "Process password reset for the user — the most recent message supersedes "
            "all prior issues in the thread (monitor, printer, VPN, Outlook).",
            "Unlock and reset the user's account password — this is the latest and "
            "current issue, regardless of the earlier mixed complaints in the chain.",
        ],
        remediation_steps=[
            [
                "Verify the user's identity through the standard authentication process",
                "Reset the user's Active Directory password and unlock the account",
                "Confirm the user can log in with the temporary password",
                "Advise the user to change their password at next logon",
                "If previous issues in the thread are still relevant, create separate tickets",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# dc-030  Raw monitoring metrics / Prometheus-style data dump
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="dc-030",
        category=Category.DATA,
        priority=Priority.P1,
        assigned_team=Team.DATA_PLATFORM,
        needs_escalation=True,
        missing_information=[MissingInfo.AFFECTED_USERS, MissingInfo.BUSINESS_IMPACT],
        subjects=[
            "ALERT: Database disk utilization critical — metrics attached",
            "Monitoring alert — DB server storage threshold breach",
            "Urgent: prod database running out of disk — see metrics",
        ],
        descriptions=[
            "Forwarding the monitoring output. The prod SQL database is almost full.\n\n"
            "--- PROMETHEUS METRICS DUMP ---\n"
            "# HELP node_cpu_seconds_total Total CPU seconds.\n"
            "# TYPE node_cpu_seconds_total counter\n"
            'node_cpu_seconds_total{cpu="0",mode="idle"} 1.84293817e+06\n'
            'node_cpu_seconds_total{cpu="0",mode="system"} 48291.73\n'
            'node_cpu_seconds_total{cpu="0",mode="user"} 192847.44\n'
            'node_cpu_seconds_total{cpu="1",mode="idle"} 1.83847291e+06\n'
            'node_cpu_seconds_total{cpu="1",mode="system"} 51029.88\n'
            "# HELP node_memory_MemTotal_bytes Total memory.\n"
            "# TYPE node_memory_MemTotal_bytes gauge\n"
            "node_memory_MemTotal_bytes 6.7108864e+10\n"
            "node_memory_MemAvailable_bytes 4.294967296e+09\n"
            "# HELP node_filesystem_avail_bytes Available filesystem bytes.\n"
            "# TYPE node_filesystem_avail_bytes gauge\n"
            'node_filesystem_avail_bytes{device="/dev/sda1",mountpoint="/"} 2.147483648e+09\n'
            'node_filesystem_avail_bytes{device="/dev/sdb1",mountpoint="/data"} 5.36870912e+08\n'
            'node_filesystem_size_bytes{device="/dev/sdb1",mountpoint="/data"} 1.07374182e+11\n'
            "# HELP mssql_io_stall_seconds_total IO stall time.\n"
            'mssql_io_stall_seconds_total{database="ContosoProd",type="read"} 89241.7\n'
            'mssql_io_stall_seconds_total{database="ContosoProd",type="write"} 142819.3\n'
            "--- END METRICS ---\n\n"
            "The /data mount has only 512MB free out of 100GB. This hosts the ContosoProd "
            "database. It will fill up within hours at the current write rate.",
            "Got a Grafana alert at {time}. Pasting the raw metrics:\n\n"
            'disk_used_percent{{host="sql-prod-01",mount="/data"}} 98.7\n'
            'disk_used_percent{{host="sql-prod-01",mount="/"}} 45.2\n'
            'disk_used_percent{{host="sql-prod-01",mount="/backup"}} 72.1\n'
            'mssql_active_transactions{{db="TradingDB"}} 847\n'
            'mssql_log_space_used_percent{{db="TradingDB"}} 94.2\n'
            "mssql_deadlocks_total 23\n"
            'process_cpu_percent{{service="mssql"}} 78.3\n'
            'process_memory_bytes{{service="mssql"}} 5.8e+10\n'
            'net_bytes_recv{{interface="eth0"}} 2.4e+12\n'
            'net_bytes_sent{{interface="eth0"}} 1.8e+12\n'
            "go_goroutines 1247\n"
            "go_memstats_alloc_bytes 4.29e+08\n"
            'http_requests_total{{status="200"}} 9847291\n'
            'http_requests_total{{status="500"}} 4821\n\n'
            "Bottom line: the TradingDB data partition is at 98.7% and the "
            "transaction log is at 94.2%. We need to free space immediately or "
            "the database will stop accepting writes.",
        ],
        next_best_actions=[
            "Urgently address critical disk space on the production SQL database server — "
            "data partition is nearly full and will halt database writes imminently.",
            "Emergency storage intervention for TradingDB — disk at 98.7% and transaction "
            "log at 94.2%, risk of database going read-only within hours.",
        ],
        remediation_steps=[
            [
                "Immediately check for old backups, temp files, or orphaned data that can be safely removed",
                "Shrink or back up the transaction log if it is consuming excessive space",
                "Expand the data volume if the storage backend supports online resizing",
                "Identify and archive or purge large tables with stale data",
                "Set up proactive disk space monitoring alerts at 80% and 90% thresholds",
                "Plan a capacity review to prevent recurrence",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# dc-031  PDF-to-text conversion artifacts
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="dc-031",
        category=Category.SOFTWARE,
        priority=Priority.P3,
        assigned_team=Team.ENTERPRISE_APPS,
        needs_escalation=False,
        missing_information=[MissingInfo.APPLICATION_VERSION],
        subjects=[
            "Software license expired — details from vendor PDF",
            "License renewal needed — see extracted notice below",
            "Application license expiry — copied from PDF letter",
        ],
        descriptions=[
            "Hi IT,\n\n"
            "I received a license expiry notice from the vendor. I copied the text "
            "from the PDF but it came out garbled:\n\n"
            "C O N T O S O   F I N A N C I A L   S E R V I C E S\n"
            "Lic ense  Exp ira tion  Not ice\n"
            "                                                        Page 1 of 3\n"
            "---------------------------------------------------------------\n"
            "Pr oduct:        Bloomber g Ter minal Enterpr ise\n"
            "Lic ense ID:     BT-ENT-{number}\n"
            "Exp iry Date:    {date}\n"
            "                                                        Page 2 of 3\n"
            "Aut hor ized Us ers:   47\n"
            "Ren ewal Cos t:  $284,000 / year\n"
            "---------------------------------------------------------------\n"
            "                                                        Page 3 of 3\n\n"
            "The Bloomber g ter minals on the trad ing f loor will stop working "
            "when this exp ires. We need to get the ren ewal processed.",
            "Pasting the text from the vendor's PDF renewal letter. The copy "
            "didn't preserve formatting:\n\n"
            "S O F T W A R E   L I C E N S E   R E N E W A L\n\n"
            "Cust omer: Contoso F inancial Servi ces      Ref: SLR-{number}\n"
            "App lication: {app}\n"
            "Curr ent Exp iry: {date}         Ren ewal Per iod: 12 months\n"
            "Lic ensed Sea ts: 250           Tier: Enter prise\n\n"
            "  *** IMPORT ANT: Fail ure to ren ew bef ore the exp iry dat e ***\n"
            "  *** will res ult in imm ediate loss of acc ess for all us ers. ***\n\n"
            "We use {app} daily across the {department} team. Please initiate "
            "the renewal process before we lose access.",
        ],
        next_best_actions=[
            "Initiate software license renewal process — the enterprise license is "
            "approaching expiry and will block access for authorized users.",
            "Process vendor license renewal before expiration date to prevent service disruption for the team.",
        ],
        remediation_steps=[
            [
                "Identify the current license agreement and renewal terms in the asset management system",
                "Contact the vendor or account manager to initiate the renewal process",
                "Verify budget approval for the renewal cost with the department head",
                "Process the purchase order through procurement",
                "Update the license key or activation once the renewal is confirmed",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# dc-032  Enormous CC list with auto-reply noise
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="dc-032",
        category=Category.SOFTWARE,
        priority=Priority.P2,
        assigned_team=Team.ENTERPRISE_APPS,
        needs_escalation=False,
        missing_information=[MissingInfo.TIMESTAMP, MissingInfo.AFFECTED_USERS],
        subjects=[
            "Shared mailbox not receiving external emails",
            "External emails not arriving in shared mailbox",
            "Shared team inbox — missing inbound messages",
        ],
        descriptions=[
            "CC: john.smith@contoso.com; sarah.jones@contoso.com; "
            "mike.chen@contoso.com; lisa.wong@contoso.com; "
            "david.patel@contoso.com; emma.wilson@contoso.com; "
            "ravi.kumar@contoso.com; sophia.garcia@contoso.com; "
            "ahmed.hassan@contoso.com; nina.petrov@contoso.com; "
            "carlos.rivera@contoso.com; yuki.sato@contoso.com; "
            "olivia.brown@contoso.com; wei.zhang@contoso.com; "
            "fatima.ali@contoso.com; james.murphy@contoso.com; "
            "priya.nair@contoso.com; thomas.andersen@contoso.com; "
            "helen.kim@contoso.com; marcus.johnson@contoso.com; "
            "anna.kowalski@contoso.com; daniel.okafor@contoso.com\n\n"
            "--- Auto-Reply from sarah.jones@contoso.com ---\n"
            "I am currently out of the office until March 28th with limited "
            "access to email. For urgent matters, contact lisa.wong@contoso.com.\n\n"
            "--- Auto-Reply from ahmed.hassan@contoso.com ---\n"
            "Thank you for your message. I am on annual leave and will return "
            "on April 2nd. Your email will not be monitored.\n\n"
            "--- Auto-Reply from nina.petrov@contoso.com ---\n"
            "I'm attending a conference this week. For immediate assistance "
            "please reach out to the {department} team lead.\n\n"
            "ACTUAL ISSUE: Our shared mailbox clientservices@contoso.com has "
            "stopped receiving emails from external senders. Internal emails "
            "arrive fine. This has been going on for at least a day. Our clients "
            "are complaining that their emails are bouncing.",
            "To: IT Support\n"
            "CC: entire-{department}-team@contoso.com (35 recipients)\n\n"
            "--- Out of Office: {name1}@contoso.com ---\n"
            "I will be out of the office from March 20-27. Please contact "
            "{name2}@contoso.com in my absence.\n\n"
            "--- Out of Office: {name3}@contoso.com ---\n"
            "Currently on PTO. Back on April 1. No access to email.\n\n"
            "--- Auto-Reply: {name2}@contoso.com ---\n"
            "I am in training all week. Response times may be delayed.\n\n"
            "Hi IT,\n\n"
            "The shared inbox for our team (compliance-inbox@contoso.com) is "
            "not getting external emails since the weekend. Internal sends "
            "work. We handle regulatory submissions through this mailbox so "
            "this is urgent.",
        ],
        next_best_actions=[
            "Investigate shared mailbox external email delivery failure — internal "
            "mail works but external senders are getting bounces.",
            "Diagnose external email delivery to shared mailbox — likely a transport "
            "rule, connector, or anti-spam policy blocking inbound external mail.",
        ],
        remediation_steps=[
            [
                "Check Exchange message trace for external emails sent to the shared mailbox",
                "Review anti-spam and transport rules for any recent changes blocking external senders",
                "Verify the shared mailbox MX record and mail flow connectors",
                "Check if the mailbox has hit a storage quota that could reject inbound mail",
                "Test by sending a test email from an external account and tracing its path",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# dc-033  Screenshot OCR with layout artifacts
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="dc-033",
        category=Category.SOFTWARE,
        priority=Priority.P2,
        assigned_team=Team.ENTERPRISE_APPS,
        needs_escalation=False,
        missing_information=[MissingInfo.ERROR_MESSAGE, MissingInfo.STEPS_TO_REPRODUCE],
        subjects=[
            "SAP transaction failing — OCR'd error from screen",
            "SAP error — text copied from screenshot",
            "{app} transaction error — extracted from screen capture",
        ],
        descriptions=[
            "I took a screenshot of the error and used OCR to copy the text. "
            "Sorry if the formatting is weird:\n\n"
            "| SAP Easy Access                                     |\n"
            "|-----------------------------------------------------|\n"
            "| Tra nsaction   | FB50       | Post Document          |\n"
            "|  Comp any Code | 1000       | Con toso Fin ancial    |\n"
            "| Fi scal Year   | 2026       |                        |\n"
            "|-----------------------------------------------------|\n"
            "|                                                     |\n"
            "|  E rror:  Doc ument  cou ld  not  be  pos ted       |\n"
            "|  Mes sage  no. F5 729                                |\n"
            '|  " Bal ance in tra nsaction cur rency "              |\n'
            "|                                                     |\n"
            "| |  Deb it   |  Cre dit  |  Diff erence |            |\n"
            "| | 142,847  |  139,291  |    3,556     |            |\n"
            "|-----------------------------------------------------|\n\n"
            "This happens when I try to post journal entries for "
            "the month-end close. It was working last week.",
            "Copied text from my screen using the snipping tool OCR:\n\n"
            "SAP Tran saction:   VA01 - Cre ate Sal es Ord er\n"
            "-----------------------------------------------\n"
            "  Err or   Mes sage:\n"
            '  "Mat erial  {number}  is  not  def ined  for\n'
            '   sal es  org  1000 /  dis tribution  cha nnel  10"\n\n'
            "  Mes sage  No:   VE  021\n"
            "  Mes sage  Ty pe:  E  (Err or)\n\n"
            "  |  Ord er Type  |  Sal es Org  |  Dist Ch  |  Div  |\n"
            "  |  ZOR          |  1000         |  10        |  00   |\n\n"
            "The {department} team needs to create sales orders but "
            "this error blocks every attempt since the last SAP update.",
        ],
        next_best_actions=[
            "Investigate SAP posting error — document cannot be posted due to balance "
            "discrepancy or material master data issue after recent update.",
            "Troubleshoot SAP transaction failure — likely a configuration or master data "
            "issue introduced by the latest system update.",
        ],
        remediation_steps=[
            [
                "Check SAP transaction logs for the specific error message number",
                "Verify the material or GL account master data configuration",
                "Review recent SAP transport or configuration changes",
                "Test the transaction in the QA environment to confirm it is not environment-specific",
                "If a configuration change caused the issue, coordinate with the SAP Basis team to revert",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# dc-034  Base64 encoded non-image files inline
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="dc-034",
        category=Category.DATA,
        priority=Priority.P3,
        assigned_team=Team.DATA_PLATFORM,
        needs_escalation=False,
        missing_information=[MissingInfo.ERROR_MESSAGE],
        subjects=[
            "SharePoint upload failing — files attached inline",
            "Can't upload documents to SharePoint — see files below",
            "SharePoint document library rejecting uploads",
        ],
        descriptions=[
            "Hi IT,\n\n"
            "I can't upload documents to our SharePoint site. I'm attaching the files "
            "inline since the portal file upload is also broken.\n\n"
            "[File: quarterly_report.docx]\n"
            "data:application/vnd.openxmlformats-officedocument.wordprocessingml.document;"
            "base64,UEsDBBQAAAAIAGFiV1gAAAAAAAAAAAAAABIAHABbQ29udGVudF9UeXBlc10ueG1sV"
            "VQJAANxYWhmcWFoZnV4CwABBPUBAAAEFAAAAG2RTU7DMASFN+cUVrZNaiFBlRANi8IGVKUH"
            "cJJ3iYX/ZLupu+foFITKZjTz5pvnz+P5s8n12I1yx2hAXCHVKi4O5L4oK8+fBg7dqG7erq"
            "5mxW2Y/gzCKkQDjM6j9yKXjCJQN2yqVTaQJLkoL97/dRwVwjhSjfA1k8jqJkAxZzLJ4HPT"
            "\n\n"
            "[File: expense_data.csv]\n"
            "data:text/csv;base64,RGF0ZSxEZXBhcnRtZW50LEFtb3VudCxDYXRlZ29yeSxBcHByb3Z"
            "lZApNYXIgMDEsV2VhbHRoIE1hbmFnZW1lbnQsMTI0NTcuODAsVHJhdmVsLFllcwpNYXIgMD"
            "IsVHJhZGluZyw4OTIuNDUsTWVhbHMsWWVzCk1hciAwMyxDb21wbGlhbmNlLDM0NTY3Ljkw"
            "\n\n"
            "[File: original_ticket.eml]\n"
            "data:message/rfc822;base64,RnJvbTogam9obi5kb2VAY29udG9zby5jb20NClRvOiBpdHN"
            "1cHBvcnRAY29udG9zby5jb20NClN1YmplY3Q6IFNoYXJlUG9pbnQgdXBsb2FkIGVycm9yDQ"
            "pEYXRlOiBNb24sIDE3IE1hciAyMDI2IDA5OjAwOjAwICswMDAwDQoNCkkga2VlcCBnZXR0aW"
            "\n\n"
            "The error says something about file size limits. These are all under 10MB "
            "individually but the SharePoint library might have a lower limit set.",
            "SharePoint keeps rejecting my uploads with a vague error. Here are the "
            "files I'm trying to upload (pasted as base64 since I can't attach):\n\n"
            "data:application/pdf;base64,JVBERi0xLjcKCjEgMCBvYmoKPDwKL1R5cGUgL0NhdGFsb"
            "2cKL1BhZ2VzIDIgMCBSCj4+CmVuZG9iagoKMiAwIG9iago8PAovVHlwZSAvUGFnZXMKL0tp"
            "ZHMgWzMgMCBSXQovQ291bnQgMQo+PgplbmRvYmoKCjMgMCBvYmoKPDwKL1R5cGUgL1BhZ2"
            "UKL1BhcmVudCAyIDAgUgovTWVkaWFCb3ggWzAgMCA2MTIgNzkyXQovQ29udGVudHMgNCAw"
            "\n\n"
            "data:application/vnd.ms-excel;base64,0M8R4KGxGuEAAAAAAAAAAAAAAAAAAAAAPgADAP7"
            "/CQAGAAAAAAAAAAAAAAABAAAA/v///wAAAAAAAAAAAAAAAAAAAAAA//////////////8AAAAA"
            "\n\n"
            "I need to upload these to the {department} document library on SharePoint. "
            "The library has been working for months but started failing last week.",
        ],
        next_best_actions=[
            "Investigate SharePoint document upload failure — likely a file size limit, "
            "library quota, or version limit configuration issue.",
            "Troubleshoot SharePoint upload rejection — check document library settings, "
            "storage quotas, and any recent policy changes.",
        ],
        remediation_steps=[
            [
                "Check the SharePoint document library's file size and storage quota settings",
                "Verify if the site collection storage limit has been reached",
                "Review SharePoint admin center for any recent policy changes on upload limits",
                "Test uploading a small test file to isolate whether it's size-related",
                "If the quota is the issue, request a storage increase or archive old documents",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# dc-035  Voice-to-text transcript with severe recognition errors
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="dc-035",
        category=Category.HARDWARE,
        priority=Priority.P3,
        assigned_team=Team.ENDPOINT,
        needs_escalation=False,
        missing_information=[MissingInfo.DEVICE_INFO, MissingInfo.ENVIRONMENT_DETAILS],
        subjects=[
            "Laptop battery draining fast — phone transcript",
            "Battery issue — transcribed from voicemail",
            "Laptop dies quickly — voice message transcript",
        ],
        descriptions=[
            "[Automated Voice-to-Text Transcript]\n\n"
            "um hi this is uh {name} from the {department} department um i'm "
            "calling because my laptop battery is like dying really fast um its "
            "like its not even lasting um like too hours two hours maybe like um "
            "it used too last the hole day and now its like uh buy the time i get "
            "too my first meeting its already at like thirty purse scent um i "
            "mean thirty percent sorry um i think their might be something wrong "
            "with the batter he or maybe like a program thats using too much um "
            "i dont no what its called but theirs this fan noise to like the fan "
            "is running all the time even when im just um reading emails its like "
            "really loud and the bottom of the laptop is super hot um i tried "
            "restarting it but it didnt help um can some one please look at this "
            "its really affecting my work uh because i have too carry the charger "
            "every wear now and sum meeting rooms dont have outlets um thanks bye",
            "[Phone Transcript — Automated Speech Recognition]\n\n"
            "yeah hi uh this is about my think pad um the battery is terrible now "
            "like it was fine a weak ago but now it only lasts maybe an our and a "
            "half um i noticed the um task manager shows something called uh "
            "anti malware service executable using like forty percent see pee you "
            "um forty percent CPU all the time um and theirs also this windows "
            "up date thing that keeps trying too run in the background its been "
            "like pending for days um i think the updates stuck and its killing "
            "my battery um also the laptop gets really hot on the left side near "
            "the charging port which is kind of concerning um i work on floor "
            "{floor} in the {office} office if some one needs too come look at it "
            "um or i can bring it too the help desk whatever works um thanks",
        ],
        next_best_actions=[
            "Investigate rapid laptop battery drain — symptoms suggest a runaway process "
            "(possibly antimalware scan or stuck update) causing high CPU and thermal throttling.",
            "Diagnose laptop battery and thermal issue — excessive CPU usage from background "
            "processes is likely draining the battery and causing overheating.",
        ],
        remediation_steps=[
            [
                "Check Task Manager for high-CPU processes (antimalware, Windows Update, etc.)",
                "Run Windows Update troubleshooter to resolve any stuck updates",
                "Generate a battery health report using 'powercfg /batteryreport'",
                "If the battery health is degraded below 80%, schedule a battery replacement",
                "Check power plan settings and reset to Balanced if set to High Performance",
                "If a specific process is the culprit, investigate and remediate (e.g., re-trigger scan)",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# dc-036  RTF/Rich Text formatting markup noise
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="dc-036",
        category=Category.DATA,
        priority=Priority.P2,
        assigned_team=Team.DATA_PLATFORM,
        needs_escalation=False,
        missing_information=[MissingInfo.AFFECTED_SYSTEM, MissingInfo.ERROR_MESSAGE],
        subjects=[
            "Network drive mapping failure — cannot access shared folders",
            "Mapped drive disconnected, formatting issues in original email",
            "Unable to map network drive since this morning — garbled ticket text",
        ],
        descriptions=[
            "{\\rtf1\\ansi\\ansicpg1252\\deff0\\nouicompat{\\fonttbl{\\f0\\fswiss"
            "\\fcharset0 Calibri;}{\\f1\\fnil\\fcharset0 Calibri;}}\n"
            "{\\*\\generator Riched20 10.0.19041}\\viewkind4\\uc1 \n"
            "\\pard\\sa200\\sl276\\slmult1\\f0\\fs22\\lang9 "
            "Hi IT Support,\\par\n"
            "\\b I can\\'92t map my network drive anymore.\\b0\\par\n"
            "Since about 8:30 AM today I get a \\i connection refused\\i0  "
            "error when trying to map \\\\\\\\filesvr03\\\\{department}$ "
            "from my {os} workstation on the {floor} floor. "
            "\\par\\pard\n"
            "I\\'92ve tried:\\par\n"
            "{\\pntext\\f1\\'B7\\tab}Disconnecting and re-mapping the "
            "drive\\par\n"
            "{\\pntext\\f1\\'B7\\tab}Restarting the Workstation service\\par\n"
            "{\\pntext\\f1\\'B7\\tab}Running \\f1 net use * /delete \\f0 "
            "and remapping\\par\n"
            "{\\pntext\\f1\\'B7\\tab}Rebooting my machine entirely\\par\n"
            "\\pard\\sa200\\sl276\\slmult1 Nothing works. Other people in "
            "{department} are also affected. We need this drive for our "
            "end-of-quarter reports due by {date}.\\par\n"
            "Thanks,\\par\n"
            "{name}\\par\n"
            "}",
            "{\\rtf1\\ansi{\\fonttbl{\\f0 Calibri;}}\n"
            "\\f0\\fs24 Hello,\\par\n"
            "\\par\n"
            "\\b Problem:\\b0  Network drive \\\\\\\\filesvr03\\\\shared "
            "is not accessible.\\par\n"
            "\\b When:\\b0  Started around {time} today.\\par\n"
            '\\b Error:\\b0  \\i "The network path was not found"\\i0\\par\n'
            "\\par\n"
            "I am on a {os} laptop, connected via Ethernet on floor "
            "{floor}. I was able to access the drive yesterday without any "
            "problems. Today when I click on the mapped drive letter in "
            "File Explorer it spins for about 15 seconds and then shows "
            "the error above.\\par\n"
            "\\par\n"
            "\\pard I pinged the server name and it resolves to "
            "10.42.{number}.12 but the ping times out. I can still reach "
            "other servers like the intranet portal.\\par\n"
            "\\par\n"
            "Please help \\emdash  I need access to the shared folder "
            "for a client deliverable due {date}.\\par\n"
            "\\par\n"
            "Regards,\\par\n"
            "{name}\\par\n"
            "}",
        ],
        next_best_actions=[
            "Investigate network drive mapping failure for \\\\filesvr03 — "
            "multiple users on the same floor are unable to connect to the "
            "shared drive with 'connection refused' or 'network path not found' "
            "errors.",
            "Diagnose network file share connectivity issue — mapped drive to "
            "\\\\filesvr03 is failing for users in the {department} department "
            "since this morning despite the server IP resolving correctly.",
        ],
        remediation_steps=[
            [
                "Verify the file server (filesvr03) is online and the Server service is running",
                "Check SMB port 445 connectivity from the affected subnet",
                "Review recent firewall or Group Policy changes that may block SMB traffic",
                "Restart the Server service on filesvr03 if it is unresponsive",
                "Confirm drive access is restored and notify affected users",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# dc-037  Email reply chain with conflicting information
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="dc-037",
        category=Category.ACCESS_AUTH,
        priority=Priority.P3,
        assigned_team=Team.IAM,
        needs_escalation=False,
        missing_information=[MissingInfo.AUTHENTICATION_METHOD],
        subjects=[
            "Re: Re: Re: Password reset not working — also printer issue",
            "RE: RE: RE: FW: Multiple issues — password and VPN and email",
            "Re: Re: FW: Can't log in — update on earlier printer problem",
        ],
        descriptions=[
            "Hi, I still can't log in to my account. Please reset my password "
            "for {name1}@contoso.com.\n\n"
            "--- Original Message ---\n"
            "From: {name} <{name1}@contoso.com>\n"
            "Sent: Wednesday, {date} 3:15 PM\n"
            "To: IT Support <itsupport@contoso.com>\n"
            "Subject: Re: Re: Password reset not working — also printer issue\n\n"
            "Actually, ignore the printer thing — someone fixed it already. "
            "The real problem now is that my password expired and the self-service "
            "portal says my security questions are wrong. I definitely know "
            "the answers. Can you just reset it on your end?\n\n"
            "--- Original Message ---\n"
            "From: {name} <{name1}@contoso.com>\n"
            "Sent: Wednesday, {date} 1:42 PM\n"
            "To: IT Support <itsupport@contoso.com>\n"
            "Subject: Re: Password reset not working — also printer issue\n\n"
            "Update: now my VPN is also not connecting but that might be "
            "because of the expired password? Not sure. Also the printer "
            "on {floor} floor is jamming again — can someone look at that "
            "too?\n\n"
            "--- Original Message ---\n"
            "From: {name} <{name1}@contoso.com>\n"
            "Sent: Wednesday, {date} 10:05 AM\n"
            "To: IT Support <itsupport@contoso.com>\n"
            "Subject: Password reset not working\n\n"
            "Hi, I tried to reset my password using the self-service portal "
            "but it keeps saying 'answer does not match'. I need to get into "
            "my account ASAP for a {department} presentation this afternoon.",
            "I need my password reset please. Username is {name2}@contoso.com. "
            "I've been locked out since this morning.\n\n"
            "---------- Forwarded message ----------\n"
            "From: {name} <{name2}@contoso.com>\n"
            "Date: {date} 11:20 AM\n"
            "Subject: RE: RE: RE: FW: Multiple issues\n\n"
            "OK so the email issue resolved itself after I cleared my Outlook "
            "cache. But I still can't log in to Windows — it says the trust "
            "relationship between this workstation and the primary domain "
            "has failed. Wait, actually it might be a password issue because "
            "I changed my password from my phone last week and maybe it "
            "didn't sync?\n\n"
            "---------- Forwarded message ----------\n"
            "From: {name3} <{name3}@contoso.com>\n"
            "Date: {date} 9:05 AM\n"
            "Subject: RE: RE: FW: Multiple issues\n\n"
            "I'm replying on behalf of {name} who asked me to forward this. "
            "Their laptop shows a domain trust error and their email on the "
            "phone is showing a certificate warning. Not sure if those are "
            "related.\n\n"
            "---------- Forwarded message ----------\n"
            "From: {name} <{name2}@contoso.com>\n"
            "Date: {date} 8:30 AM\n"
            "Subject: Multiple issues\n\n"
            "Hi, three things: 1) can't log in to laptop, 2) email on "
            "phone has certificate error, 3) need VPN access set up for "
            "remote work starting next week.",
        ],
        next_best_actions=[
            "Process password reset for user {name1}@contoso.com — the latest "
            "message in this reply chain confirms the core issue is an expired "
            "password with self-service reset failing due to mismatched security "
            "questions.",
            "Reset user credentials for {name2}@contoso.com — the underlying "
            "issue across multiple forwarded messages is a password/domain trust "
            "failure; VPN and email issues are likely secondary symptoms.",
        ],
        remediation_steps=[
            [
                "Verify the user's identity through an out-of-band channel",
                "Reset the user's Active Directory password",
                "Update or re-enroll the user's self-service password reset security questions",
                "Have the user log in and confirm access to Windows, VPN, and email",
                "If domain trust error persists, rejoin the workstation to the domain",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# dc-038  Raw monitoring metrics dump — database disk space
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="dc-038",
        category=Category.DATA,
        priority=Priority.P1,
        assigned_team=Team.DATA_PLATFORM,
        needs_escalation=True,
        missing_information=[MissingInfo.AFFECTED_USERS, MissingInfo.BUSINESS_IMPACT],
        subjects=[
            "ALERT: Database server disk utilization critical — metrics attached",
            "Urgent — db-prod-07 disk space alert firing, full metrics dump inside",
            "Production database disk at 96% — Grafana export below",
        ],
        descriptions=[
            "Prometheus alert fired at {time} for db-prod-07. Dumping full "
            "metric payload below.\n\n"
            "# HELP node_cpu_seconds_total Total CPU seconds.\n"
            "# TYPE node_cpu_seconds_total counter\n"
            'node_cpu_seconds_total{{cpu="0",mode="idle"}} 1.284903e+06\n'
            'node_cpu_seconds_total{{cpu="0",mode="system"}} 48205.3\n'
            'node_cpu_seconds_total{{cpu="0",mode="user"}} 97312.7\n'
            'node_cpu_seconds_total{{cpu="1",mode="idle"}} 1.290441e+06\n'
            'node_cpu_seconds_total{{cpu="1",mode="system"}} 45891.1\n'
            'node_cpu_seconds_total{{cpu="1",mode="user"}} 94278.4\n'
            "# HELP node_memory_MemTotal_bytes Total memory in bytes.\n"
            "# TYPE node_memory_MemTotal_bytes gauge\n"
            "node_memory_MemTotal_bytes 6.7108864e+10\n"
            "node_memory_MemAvailable_bytes 8.12409e+09\n"
            "node_memory_Buffers_bytes 2.1847e+08\n"
            "node_memory_Cached_bytes 1.209384e+10\n"
            "# HELP node_filesystem_avail_bytes Available filesystem bytes.\n"
            "# TYPE node_filesystem_avail_bytes gauge\n"
            'node_filesystem_avail_bytes{{device="/dev/sda1",mountpoint="/"}} '
            "4.2949673e+09\n"
            'node_filesystem_avail_bytes{{device="/dev/sdb1",mountpoint="/data"}} '
            "1.8253612e+08\n"
            'node_filesystem_size_bytes{{device="/dev/sdb1",mountpoint="/data"}} '
            "5.36870912e+10\n"
            "# HELP node_disk_io_time_seconds_total Total I/O time.\n"
            "# TYPE node_disk_io_time_seconds_total counter\n"
            'node_disk_io_time_seconds_total{{device="sdb"}} 987214.4\n'
            'node_disk_read_bytes_total{{device="sdb"}} 4.81036e+12\n'
            'node_disk_written_bytes_total{{device="sdb"}} 7.93102e+12\n\n'
            "---\n"
            "The /data mount on db-prod-07 is at 96.6% utilization with only "
            "~174 MB free of 50 GB. This is the primary data volume for the "
            "production PostgreSQL instance. Transaction logs and temp files "
            "are growing. If this fills up the database will go read-only.",
            "Grafana alert notification — db-prod-07 disk critical.\n\n"
            "[firing] DiskSpaceCritical\n"
            "  instance: db-prod-07:9100\n"
            "  severity: critical\n"
            "  mountpoint: /data\n"
            "  threshold: 95%\n"
            "  current: 96.6%\n\n"
            "--- Panel: System Overview (last 6h) ---\n"
            "CPU Usage:  avg 34.2%  max 71.8%  current 38.5%\n"
            "Memory:     avg 78.1%  max 84.3%  current 80.2%\n"
            "Disk I/O:   read 12.4 MB/s  write 28.7 MB/s\n"
            "Network:    rx 145 Mbps  tx 89 Mbps\n\n"
            "--- Panel: Disk Usage by Mount ---\n"
            "/        12.1 GB / 100 GB  (12.1%)\n"
            "/data    49.8 GB /  50 GB  (96.6%)   << CRITICAL\n"
            "/backup  410 GB  / 500 GB  (82.0%)\n"
            "/logs     18 GB  /  20 GB  (90.0%)\n\n"
            "--- Panel: Top Tables by Size ---\n"
            "public.transactions       22.4 GB\n"
            "public.audit_log          11.8 GB\n"
            "public.session_data        6.2 GB\n"
            "public.event_queue         4.1 GB\n"
            "pg_wal                     3.8 GB\n\n"
            "The database volume is nearly full. If the disk fills "
            "completely, PostgreSQL will switch to read-only mode and all "
            "write operations will fail.",
        ],
        next_best_actions=[
            "Address critical disk space shortage on db-prod-07 /data volume "
            "(96.6% full, ~174 MB remaining) — the production PostgreSQL "
            "instance will go read-only if the disk fills up.",
            "Immediately free disk space on the production database server "
            "db-prod-07 — the /data partition hosting PostgreSQL is at 96.6% "
            "with large tables (transactions, audit_log) consuming most space.",
        ],
        remediation_steps=[
            [
                "Purge or archive old rows from the audit_log and session_data tables",
                "Run VACUUM FULL on the largest tables to reclaim dead tuple space",
                "Rotate and compress PostgreSQL WAL files and old transaction logs",
                "Extend the /data volume or add additional storage if available",
                "Set up automated alerting at 80% and 90% thresholds to prevent recurrence",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# dc-039  PDF-to-text conversion artifacts — software license expiration
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="dc-039",
        category=Category.SOFTWARE,
        priority=Priority.P3,
        assigned_team=Team.ENTERPRISE_APPS,
        needs_escalation=False,
        missing_information=[MissingInfo.APPLICATION_VERSION],
        subjects=[
            "License expired for design software — need renewal",
            "So\ufb00ware license issue — applica\ufb03on won't launch",
            "Adobe Creative Suite license expiring, request renewal",
        ],
        descriptions=[
            "Ti cket submitted via PDF upload from the {department} department.\n\n"
            "P age 1 of 2\n\n"
            "TO: IT Servi ces | FROM: {name} | DATE: {date}\n"
            "RE: So\ufb00ware License Renewal Request\n\n"
            "I am wri\ufb03ng to request a renewal of our Adobe Crea\ufb03ve "
            "Suite license. The current license key expired on {date} and "
            "the applica\ufb03on now displays a \u201cLicense has expired\u201d "
            "dialog on launch, preven\ufb03ng all {number} designers in "
            "{department} from working.\n\n"
            "   Applica\ufb03on:    Adobe Crea\ufb03ve Suite\n"
            "   License Type:   Enterprise Volume (site license)\n"
            "   Sea ts:         {number}\n"
            "   Expiry:         {date}\n"
            "   Cos t Center:   CC-40{number}\n\n"
            "We have a client deliverable due on {date} and cannot proceed "
            "without Illustrator and InDesign.\n\n"
            "P age 2 of 2\n\n"
            "Please priori\ufb03ze this request. Our manager {name2} has "
            "approved the budget alloca\ufb03on.\n\n"
            "Thank you,\n"
            "{name}\n"
            "{department} Department\n"
            "Ext. {number}",
            "--- Converted from a\ufb00ached PDF ---\n\n"
            "                        INTERNAL MEMO\n"
            "                        =============\n\n"
            "From :     {name}, {department}\n"
            "To :       IT Help Desk\n"
            "D ate:     {date}\n"
            "Sub ject:  So\ufb00ware license renewal \u2014 URGENT\n\n"
            "Hi,\n\n"
            "Our team\u2019s license for Adobe Crea\ufb03ve Cloud has expired. "
            "When I try to open Photoshop or Illustrator I see a pop-up:\n\n"
            "    \u201cYour license has expired. Plea se contact your IT\n"
            "     administrator to renew your subscrip\ufb03on.\u201d\n\n"
            "This a\ufb00ects our en\ufb03re {department} team ({number} "
            "people). We are in the middle of the Q{number} marke\ufb03ng "
            "campaign and need these tools immediately.\n\n"
            "Details:\n"
            "\u2022  Product: Adobe Crea\ufb03ve Cloud \u2014 All Apps\n"
            "\u2022  License ID: ACR-ENT-{number}-{number}\n"
            "\u2022  # of seats: {number}\n"
            "\u2022  Expiry date: {date}\n"
            "\u2022  Renewal PO#: Pending \ufb01nance approval\n\n"
            "Plea se expedite. Thank you.\n\n"
            "{name}\n"
            "Ext {number}",
        ],
        next_best_actions=[
            "Renew the expired Adobe Creative Suite/Creative Cloud enterprise "
            "license — the entire {department} design team ({number} users) is "
            "blocked from launching applications.",
            "Process urgent software license renewal for Adobe Creative Cloud — "
            "license has expired and is preventing the design team from working "
            "on active client deliverables.",
        ],
        remediation_steps=[
            [
                "Verify the current license agreement and expiry details with the software asset team",
                "Submit or expedite the purchase order for the license renewal",
                "Apply the new license key or update the license server with the renewed entitlement",
                "Have affected users sign out and back in to Adobe Creative Cloud to pick up the new license",
                "Confirm all seats are activated and users can launch applications",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# dc-040  Enormous CC list with auto-reply noise — shared mailbox
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="dc-040",
        category=Category.SOFTWARE,
        priority=Priority.P2,
        assigned_team=Team.ENTERPRISE_APPS,
        needs_escalation=False,
        missing_information=[MissingInfo.TIMESTAMP, MissingInfo.AFFECTED_USERS],
        subjects=[
            "Shared mailbox not receiving external email — buried in auto-replies",
            "External emails not reaching shared mailbox — huge CC thread",
            "Shared mailbox issue — sales-team@ not getting outside mail",
        ],
        descriptions=[
            "CC: ajohnson@contoso.com; bsmith@contoso.com; clee@contoso.com; "
            "dgarcia@contoso.com; ewilliams@contoso.com; fbrown@contoso.com; "
            "gjones@contoso.com; hmiller@contoso.com; idavis@contoso.com; "
            "jwilson@contoso.com; kmoore@contoso.com; ltaylor@contoso.com; "
            "manderson@contoso.com; nthomas@contoso.com; ojackson@contoso.com; "
            "pwhite@contoso.com; qharris@contoso.com; rmartin@contoso.com; "
            "sthompson@contoso.com; trobinson@contoso.com; uclark@contoso.com; "
            "vrodriguez@contoso.com; wlewis@contoso.com; xwalker@contoso.com; "
            "yhall@contoso.com; zyoung@contoso.com\n\n"
            "--- Auto-Reply from dgarcia@contoso.com ---\n"
            "Thank you for your message. I am out of the office from {date} "
            "through {date} with limited access to email. For urgent matters, "
            "please contact {name2} at ext. {number}.\n\n"
            "--- Auto-Reply from hmiller@contoso.com ---\n"
            "I am currently on PTO and will return on {date}. Your email "
            "will not be forwarded. Please reach out to the {department} "
            "team alias for immediate assistance.\n\n"
            "--- Auto-Reply from ltaylor@contoso.com ---\n"
            "I am on parental leave until {date}. For anything related to "
            "the {department} project, please contact {name3}.\n\n"
            "--- Auto-Reply from sthompson@contoso.com ---\n"
            "Thank you for reaching out! I'm attending a conference this week "
            "and will reply after {date}.\n\n"
            "--- Actual Issue (from {name}) ---\n"
            "Hi IT, our shared mailbox sales-team@contoso.com has stopped "
            "receiving emails from external senders. Internal emails arrive "
            "fine. This started sometime recently and our sales reps are "
            "missing client inquiries. I only noticed because a client called "
            "to ask why we hadn't responded to their email from three "
            "days ago.",
            "To: itsupport@contoso.com\n"
            "CC: {name1}@contoso.com; {name2}@contoso.com; "
            "{name3}@contoso.com; akim@contoso.com; bpatel@contoso.com; "
            "cchen@contoso.com; dmuller@contoso.com; enakamura@contoso.com; "
            "fsingh@contoso.com; gkumar@contoso.com; hpark@contoso.com; "
            "iali@contoso.com; jzhang@contoso.com; kgupta@contoso.com; "
            "lnguyen@contoso.com; mwong@contoso.com; nsato@contoso.com; "
            "otanaka@contoso.com; pyamamoto@contoso.com; qsuzuki@contoso.com\n\n"
            "--- Auto-Reply: {name2}@contoso.com ---\n"
            "Thanks for your email! I'm OOO until {date}. For urgent items "
            "contact the {department} manager.\n\n"
            "--- Auto-Reply: bpatel@contoso.com ---\n"
            "I am currently out of office with no access to email until {date}.\n\n"
            "--- Auto-Reply: gkumar@contoso.com ---\n"
            "Hi! I'm at an offsite event this week. Back on {date}.\n\n"
            "--- Auto-Reply: mwong@contoso.com ---\n"
            "On annual leave. Will respond when I return on {date}. Thanks!\n\n"
            "--- Original Message from {name} ---\n"
            "Hello, the sales-team@contoso.com shared mailbox is not "
            "receiving any external emails. Internal emails between contoso "
            "users arrive immediately, but anything from external domains "
            "(gmail.com, clients, partners) never appears. We checked the "
            "junk folder — nothing there either. This is impacting our "
            "ability to respond to inbound sales leads and client requests.",
        ],
        next_best_actions=[
            "Investigate external email delivery failure to the "
            "sales-team@contoso.com shared mailbox — internal mail works but "
            "no messages from external senders are being received.",
            "Diagnose why the shared mailbox sales-team@contoso.com is not "
            "receiving external email — internal delivery is functioning but "
            "external messages are silently dropped.",
        ],
        remediation_steps=[
            [
                "Check Exchange message trace for external messages sent to sales-team@contoso.com",
                "Verify the shared mailbox has not exceeded its storage quota",
                "Review mail flow rules and transport rules for any that may block external senders",
                "Check the spam/quarantine policies for overly aggressive external filtering",
                "Send a test email from an external address and trace its delivery path",
                "Restore delivery and monitor for 24 hours to confirm the fix",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# dc-041  Screenshot OCR with layout artifacts — SAP transaction
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="dc-041",
        category=Category.SOFTWARE,
        priority=Priority.P2,
        assigned_team=Team.ENTERPRISE_APPS,
        needs_escalation=False,
        missing_information=[MissingInfo.ERROR_MESSAGE, MissingInfo.STEPS_TO_REPRODUCE],
        subjects=[
            "SAP transaction VA01 failing — error screenshot attached",
            "Cannot create sales order in SAP — OCR of error screen",
            "SAP error when posting VA01 — screen capture text below",
        ],
        descriptions=[
            "[OCR extracted from screenshot — original image corrupt]\n\n"
            "+------------------------------------------------------------------+\n"
            "|  SAP Easy Access                                    [_] [口] [X]  |\n"
            "+------------------------------------------------------------------+\n"
            "|  Transaction: VA01           | Cr eate Sal es Order               |\n"
            "+------------------------------------------------------------------+\n"
            "|  Order Type :   |  OR  |      Std Order                          |\n"
            "|  Sales Org. :   | 1000 |      Contoso NA                         |\n"
            "|  Distr. Chan.:  |  10  |      Direct Sales                       |\n"
            "|  Division:      |  00  |      Cross-divi sion                    |\n"
            "+------------------------------------------------------------------+\n"
            "|  Sol d-to Party:  200{number}                                     |\n"
            "|  Ship-to Party:  200{number}                                      |\n"
            "|  PO Number :     C LIEN T-PO-{number}                            |\n"
            "|  PO Date:        {date}                                          |\n"
            "+------------------------------------------------------------------+\n"
            "|                                                                   |\n"
            "|  [!] Error:  Pr icing procedure could not be de termin ed         |\n"
            "|      Message No. V1 - 301                                         |\n"
            "|                                                                   |\n"
            "+------------------------------------------------------------------+\n\n"
            "I keep ge\ufb03ing this error when trying to create a sales order "
            "in VA01. It was working \ufb01ne yesterday. I\u2019m using the same "
            "order type and sales area I always use. Customer {name} needs "
            "this order processed today.",
            "[Text extracted from screen capture]\n\n"
            "SAP GUI 770  |  Cl ient 100  |  User: {name1}\n"
            "-------------------------------------------\n"
            "Tcode:  VA01\n"
            "Order Type:  OR    Sal es Org:  1000\n"
            "Dist Ch:     10    Div:        00\n\n"
            "I t e m |  Mat eri al   |  Qty  |  UoM  |  Plant\n"
            "--------|--------------|-------|-------|-------\n"
            "   10   |  MAT-{number}|  100  |   EA  |  1000\n"
            "   20   |  MAT-{number}|   50  |   EA  |  1000\n\n"
            " +-------------------------------------------------+\n"
            " |  Mess age: Prici ng procedu re could not be      |\n"
            " |  deter mi ned (V1-301)                           |\n"
            " |  Mess age Type: E (Error)                        |\n"
            " +-------------------------------------------------+\n\n"
            "This has bee n happening since this morn ing. I tried with "
            "differ ent cust omer numbers and materi als but same error "
            "every time. Our tea m needs to proc ess approximately "
            "{number} orders today for month-end close.",
        ],
        next_best_actions=[
            "Investigate SAP pricing procedure determination failure (V1-301) "
            "in transaction VA01 — sales order creation is blocked for sales "
            "org 1000, distribution channel 10.",
            "Resolve SAP error V1-301 preventing sales order creation in VA01 "
            "— pricing procedure lookup is failing across all customers and "
            "materials, suggesting a configuration issue.",
        ],
        remediation_steps=[
            [
                "Check OVKK for the pricing procedure assignment to sales org 1000, dist. channel 10, div. 00",
                "Verify that the pricing procedure condition records have not been deleted or expired",
                "Review any SAP transport requests moved to production recently that may have affected pricing config",
                "If a transport caused the issue, roll back or apply a corrective transport",
                "Test sales order creation in VA01 to confirm the error is resolved",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# dc-042  Base64 encoded non-image files inline — SharePoint upload
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="dc-042",
        category=Category.DATA,
        priority=Priority.P3,
        assigned_team=Team.DATA_PLATFORM,
        needs_escalation=False,
        missing_information=[MissingInfo.ERROR_MESSAGE],
        subjects=[
            "SharePoint upload failing for large files — base64 error dump",
            "Cannot upload documents to SharePoint — file content below",
            "SharePoint file upload size limit error — attached file data",
        ],
        descriptions=[
            "I'm trying to upload a quarterly report to our {department} "
            "SharePoint site but it keeps failing. Here's the file I'm "
            "trying to upload — maybe you can see what's wrong:\n\n"
            "--- report_Q{number}_{date}.docx (base64) ---\n"
            "UEsDBBQAAAAIAGFiV1kAAAAAAAAAAAAAABIAHABDb250ZW50X1R5cGVz\n"
            "Lnht bFVUCQADt2hRZ7doUWd1eAsAAQT2AQAABBQAAABNzrEKwjAQgOG9\n"
            "4DuE7Nr qICJdnQRnce0lLW1yIXex+vZGwe H7h//jbN13s3UPmu0QGMiY\n"
            "kAaqoDX0GWGfb6cr4BIleeQ+DGQMzC cDk8kqVj8k3h5LlhOBjxRarPbC\n"
            "pXQpNg6i WIkMzJGmSEBdx7LqPkM/4HHiB60SLbEDNw/iX8AAAD//wMA\n"
            "UEsDBBQAAAAIAGFiV1kAAAAAAAAAAAA AAAoAHABfcmVscy8ucmVsc1VU\n"
            "CQAD ... [truncated, ~48000 more characters] ...\n\n"
            "--- budget_data.csv (base64) ---\n"
            "RGVwYXJ0bWVudCxRMSBCdWRnZXQsUTEgQWN0dWFsLFEyIEJ1ZGdldCxR\n"
            "MiBBY3R1YWwsUTMgQnVkZ2V0LFEzIEFjdHVhbCxRNCBCdWRnZXQsUTQg\n"
            "QWN0dWFsCk1hcmtldGluZywxMjAwMD AsMTE1MDAsMTMwMDAsMTI4MDAsMTEw\n"
            "MDAsMTEyMDAsMTUwMDAsMCAgCkVuZ2luZWVya W5nLDI1MDAwLDI0ODAwLDI2\n"
            "MDAwLDI1NTAwLDI3MDAwLDI2ODAwLDI4MDAwLDAK ... [truncated] ...\n\n"
            "The error says something about file size limit but this file is "
            "only about 35 MB. The SharePoint site is at "
            "https://contoso.sharepoint.com/sites/{department}. I've been "
            "able to upload smaller files (~5 MB) without issues. This is "
            "blocking our {department} quarterly review.",
            "Hi, when I drag and drop files to our SharePoint document "
            "library at https://contoso.sharepoint.com/sites/{department}/"
            "Shared%20Documents I get an error popup. I tried the desktop "
            "sync client and also the browser upload — same result.\n\n"
            "Here is the content of one of the files I'm trying to upload "
            "(someone told me to paste it so you can check if it's "
            "corrupted):\n\n"
            "--- client_proposal_{name1}.eml (base64) ---\n"
            "RnJvbTogc2FsZXNAY29udG9zby5jb20NClRvOiBjbGllbnRAZXhhbXBs\n"
            "ZS5jb20NClN1YmplY3Q6IFByb3Bvc2FsIGZvciBRMyBFbmdhZ2VtZW50\n"
            "DQpEYXRlOiBNb24sIDEwIE1hciAyMDI2IDA5OjAwOjAwIC0wNTAwDQpN\n"
            "SU1FLVZlcnNpb246IDEuMA0KQ29udGVudC1UeXBlOiBtdWx0aXBhcnQv\n"
            "bWl4ZWQ7IGJvdW5kYXJ5PS0tPV9OZXh0UGFydA0K ... "
            "[truncated, ~92000 more characters] ...\n\n"
            "The total folder I need to upload is about {number} files, "
            "totaling around {number} GB. Individual files range from 5 MB to "
            "80 MB. The error message flashes briefly before disappearing — "
            "I couldn't capture it. Can you increase whatever limit is "
            "preventing the upload?",
        ],
        next_best_actions=[
            "Investigate SharePoint upload size limit blocking file uploads to "
            "the {department} site — user reports that files around 35-80 MB "
            "fail while smaller files succeed.",
            "Resolve SharePoint document upload failure — large files are being "
            "rejected with a size limit error on the {department} document "
            "library; verify tenant and site-level upload limits.",
        ],
        remediation_steps=[
            [
                "Check the SharePoint tenant maximum upload file size in the SharePoint admin center",
                "Verify the site collection storage quota and remaining capacity",
                "If needed, increase the maximum file upload size (up to 250 GB per file is supported)",
                "Advise the user to use the OneDrive sync client for large batch uploads instead of browser upload",
                "Confirm successful upload of a large test file after the change",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# dc-043  Voice-to-text transcript with severe recognition errors
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="dc-043",
        category=Category.HARDWARE,
        priority=Priority.P3,
        assigned_team=Team.ENDPOINT,
        needs_escalation=False,
        missing_information=[MissingInfo.DEVICE_INFO, MissingInfo.ENVIRONMENT_DETAILS],
        subjects=[
            "Laptop battery draining super fast — need help",
            "Batter he issue on my lap top — voice message transcript",
            "Battery life problem on work laptop",
        ],
        descriptions=[
            "[Voicemail transcript — auto-generated]\n\n"
            "hey um this is {name} from the {department} department im "
            "calling about my lap top um the batter he is draining like "
            "really really fast like i charged it to full last night and "
            "buy this morning at like nine thirty it was already down to "
            "like for tee percent um and i wasnt even doing anything heavy "
            "just had out look open and like one chrome tab um and then buy "
            "lunch it was completely dead and i had to sit next to a power "
            "out let for my hole afternoon meeting witch was really "
            "inconvenient because the only out let was like in the back of "
            "the conference room on the {floor} floor um so yeah its "
            "definately not holding a charge like it used to i think i got "
            "this lap top may be too years ago or may be eighteen months um "
            "and the batter he used to last like eight hours easily um can "
            "some one take a look at it or may be replace the batter he or "
            "some thing i also noticed the bottom of the lap top gets "
            "really hot like un comfortably hot um oh and some times the "
            "fan is super loud even when im just reading email so yeah "
            "please call me back at extension {number} or just email me "
            "at {name1} at contoso dot com thanks bye",
            "[Speech-to-text transcript from phone call]\n\n"
            "hi this is {name} calling from {department} ive been having "
            "a batter he problem with my work lap top for the passed "
            "too weak snow um basically the batter he goes from a hundred "
            "purse ent to like twenty purse ent in about too ours of normal "
            "use and that is like way worse then it used to be um i looked "
            "in the settings and the batter he health says its at like "
            "seventy ate purse ent um but even that doesnt explain y its "
            "draining so fast rite um i also noticed in tack manager "
            "their is this process called system in ter upts that is using "
            "like thirty purse ent see pee you all the time witch seems "
            "weired um i dont no if thats re lated but yeah the batter he "
            "is the mane issue i cant get threw a to our meeting with out "
            "plugging in witch is really an oying especially when were in "
            "the big conference room on {floor} that only has like too "
            "out lets for twenty pee pull um can you guys take a look at "
            "it or may be order a new batter he for me the lap top is a "
            "contoso issued one i think its a dell or may be a lena vo "
            "im not shore um thanks you can reach me at {name1} at "
            "contoso dot com or extension {number}",
        ],
        next_best_actions=[
            "Investigate rapid battery drain on user's laptop — battery "
            "depletes from 100% to under 40% within a few hours of light "
            "use, accompanied by excessive heat and fan noise.",
            "Diagnose laptop battery and thermal issue — user reports the "
            "battery drains in approximately two hours under normal workload "
            "with high CPU usage from system interrupts.",
        ],
        remediation_steps=[
            [
                "Identify the laptop make and model and check the battery health report (powercfg /batteryreport)",
                "Investigate the high 'System interrupts' CPU usage — check for faulty drivers or peripherals",
                "Update BIOS, chipset, and power management drivers to the latest versions",
                "If battery health is below 80%, submit a request for battery replacement",
                "Advise the user to use a power-saver profile as a temporary workaround",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# dc-044  Markdown formatting artifacts (unrendered markup in ticket)
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="dc-044",
        category=Category.SOFTWARE,
        priority=Priority.P3,
        assigned_team=Team.ENTERPRISE_APPS,
        needs_escalation=False,
        missing_information=[MissingInfo.ERROR_MESSAGE],
        subjects=[
            "Teams integration not syncing with calendar",
            "Outlook-Teams calendar sync broken after update",
            "Calendar events missing in Teams after latest client update",
        ],
        descriptions=[
            "# Issue Report: Teams Calendar Integration Failure\n\n"
            "**Reporter:** {name}\n"
            "**Department:** {department}\n"
            "**Date:** 2026-03-17\n\n"
            "## Problem Description\n\n"
            "The Microsoft Teams integration with my Outlook calendar has "
            "completely stopped working. When I schedule a meeting in "
            "**Outlook**, it *does not* appear in **Teams**, and vice versa. "
            "This started after the IT department pushed the latest "
            "`Teams Desktop Client v24.7.1` update last Thursday.\n\n"
            "## Steps to Reproduce\n\n"
            "1. Open **Outlook Desktop** and create a new meeting\n"
            "2. Add a Teams link by clicking `Add Teams Meeting`\n"
            "3. Send the invite\n"
            "4. Open **Microsoft Teams** > Calendar tab\n"
            "5. Notice the meeting **does not appear**\n\n"
            "## What I've Tried\n\n"
            "- [x] Signed out and back into Teams\n"
            "- [x] Cleared the Teams cache "
            "(`%appdata%\\Microsoft\\Teams\\Cache`)\n"
            "- [x] Restarted my laptop\n"
            "- [ ] Reinstalled Teams (waiting for IT approval)\n\n"
            "## Expected Behavior\n\n"
            "Meetings created in Outlook should appear in Teams calendar "
            "within ~30 seconds, as documented in the "
            "[Teams admin guide](https://learn.microsoft.com/en-us/microsoftteams"
            "/exchange-teams-interact).\n\n"
            "## Impact\n\n"
            "I have **5+ client meetings daily** and have already missed "
            "joining two calls because they didn't show in Teams. This is "
            "affecting client experience.\n\n"
            "---\n\n"
            "```\n"
            "Teams Version: 24.7.1.0\n"
            "Outlook Version: 16.0.17328.20162\n"
            "OS: Windows 11 Enterprise 23H2\n"
            "```\n\n"
            "Please advise. Thanks!",
            "### Calendar Sync Failure\n\n"
            "After the **Teams v24.7** rollout, meetings I create in Outlook "
            "no longer appear in the Teams calendar. I've tried:\n\n"
            "- `Clear-TeamsCache` via PowerShell\n"
            "- Toggling the **Outlook Add-in** on and off\n"
            "- Checking the [Exchange Online connector]"
            "(https://admin.microsoft.com) status\n\n"
            "Nothing works. The `Get-CsTeamsCalendarPolicy` output is:\n"
            "```powershell\n"
            "Identity          : Global\n"
            "AllowCalendarSync  : True\n"
            "```\n\n"
            "So the policy *should* allow it. But meetings still don't sync. "
            "My colleague **{name}** in {department} has the same problem.\n\n"
            '> _"This is impacting our ability to schedule client calls."_\n\n'
            "Priority: medium to high.",
        ],
        next_best_actions=[
            "Investigate Teams-Outlook calendar sync failure after Teams Desktop "
            "Client v24.7.1 update — meetings created in Outlook do not appear "
            "in Teams calendar; user has already cleared cache and restarted.",
            "Troubleshoot calendar sync between Outlook and Teams — verify "
            "Exchange-Teams interop prerequisites and the Outlook add-in state "
            "after the recent client update.",
        ],
        remediation_steps=[
            [
                "Verify the Exchange-Teams interop prerequisites are met for the user's "
                "mailbox (Exchange Online, not on-prem)",
                "Check the Teams admin center for known issues with client version 24.7.1 and calendar sync",
                "Re-register the Teams Outlook add-in by running the Teams meeting add-in troubleshooter",
                "If the add-in is missing, repair the Office installation from Programs and Features",
                "As a fallback, approve and perform a clean reinstall of the Teams desktop client",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# dc-045  Email with multilingual legal disclaimer in 5 languages
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="dc-045",
        category=Category.NETWORK,
        priority=Priority.P3,
        assigned_team=Team.NETWORK,
        needs_escalation=False,
        missing_information=[MissingInfo.NETWORK_LOCATION, MissingInfo.BUSINESS_IMPACT],
        subjects=[
            "VPN access request for new project",
            "Need VPN profile for {department} regional network",
            "Request: APAC VPN access for cross-border project",
        ],
        descriptions=[
            "Hello IT,\n\n"
            "I have been assigned to the Cross-Border Settlements project and "
            "need VPN access to the APAC regional network (subnet 10.42.0.0/16). "
            "My manager {name} has already approved this. Could you "
            "please set this up by end of week?\n\n"
            "Thanks,\n{name}\n{department}\n\n"
            "\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550"
            "\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550"
            "\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\n"
            "CONFIDENTIALITY NOTICE / AVIS DE CONFIDENTIALIT\u00c9 / "
            "VERTRAULICHKEITSHINWEIS / "
            "\u6a5f\u5bc6\u4fdd\u6301\u306b\u95a2\u3059\u308b\u3054\u6ce8\u610f / \u4fdd\u5bc6\u58f0\u660e\n"
            "\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550"
            "\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550"
            "\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\n\n"
            "ENGLISH: This email message and any attachments are for the sole "
            "use of the intended recipient(s) and may contain confidential and "
            "privileged information of Contoso Financial Services. Any unauthorized "
            "review, use, disclosure, or distribution is strictly prohibited. If "
            "you are not the intended recipient, please contact the sender by "
            "reply email and destroy all copies of the original message. Receipt "
            "by anyone other than the intended recipient is not a waiver of any "
            "attorney-client, work product, or other applicable privilege.\n\n"
            "FRAN\u00c7AIS : Ce message \u00e9lectronique et toute pi\u00e8ce jointe sont "
            "destin\u00e9s exclusivement au(x) destinataire(s) pr\u00e9vu(s) et peuvent "
            "contenir des informations confidentielles et privil\u00e9gi\u00e9es de Contoso "
            "Services Financiers. Toute consultation, utilisation, divulgation ou "
            "distribution non autoris\u00e9e est strictement interdite. Si vous n'\u00eates "
            "pas le destinataire pr\u00e9vu, veuillez contacter l'exp\u00e9diteur par retour "
            "de courriel et d\u00e9truire toutes les copies du message original. La "
            "r\u00e9ception par toute personne autre que le destinataire pr\u00e9vu ne "
            "constitue pas une renonciation \u00e0 tout privil\u00e8ge applicable.\n\n"
            "DEUTSCH: Diese E-Mail-Nachricht und alle Anh\u00e4nge sind ausschlie\u00dflich "
            "f\u00fcr den/die vorgesehenen Empf\u00e4nger bestimmt und k\u00f6nnen vertrauliche "
            "und gesch\u00fctzte Informationen der Contoso Finanzdienstleistungen "
            "enthalten. Jede unbefugte \u00dcberpr\u00fcfung, Nutzung, Offenlegung oder "
            "Verbreitung ist strengstens untersagt. Wenn Sie nicht der vorgesehene "
            "Empf\u00e4nger sind, kontaktieren Sie bitte den Absender per Antwort-E-Mail "
            "und vernichten Sie alle Kopien der urspr\u00fcnglichen Nachricht.\n\n"
            "\u65e5\u672c\u8a9e\uff1a\u3053\u306e\u30e1\u30fc\u30eb\u304a\u3088\u3073\u6dfb\u4ed8\u30d5\u30a1\u30a4\u30eb\u306f\u3001\u610f\u56f3\u3055\u308c\u305f\u53d7\u4fe1\u8005\u306e\u307f\u3092\u5bfe\u8c61\u3068\u3057\u3066\u304a\u308a\u3001"
            "\u30b3\u30f3\u30c8\u30bd\u30fb\u30d5\u30a1\u30a4\u30ca\u30f3\u30b7\u30e3\u30eb\u30fb\u30b5\u30fc\u30d3\u30b9\u306e\u6a5f\u5bc6\u60c5\u5831\u304a\u3088\u3073\u7279\u6a29\u60c5\u5831\u304c\u542b\u307e\u308c\u3066\u3044\u308b"
            "\u5834\u5408\u304c\u3042\u308a\u307e\u3059\u3002\u8a31\u53ef\u306a\u304f\u95b2\u89a7\u3001\u4f7f\u7528\u3001\u958b\u793a\u3001\u307e\u305f\u306f\u914d\u5e03\u3059\u308b\u3053\u3068\u306f\u56fa\u304f\u7981\u3058\u3089\u308c\u3066"
            "\u3044\u307e\u3059\u3002\u610f\u56f3\u3055\u308c\u305f\u53d7\u4fe1\u8005\u3067\u306a\u3044\u5834\u5408\u306f\u3001\u8fd4\u4fe1\u30e1\u30fc\u30eb\u306b\u3066\u9001\u4fe1\u8005\u306b\u3054\u9023\u7d61\u3044\u305f\u3060\u304d\u3001"
            "\u5143\u306e\u30e1\u30c3\u30bb\u30fc\u30b8\u306e\u3059\u3079\u3066\u306e\u30b3\u30d4\u30fc\u3092\u7834\u68c4\u3057\u3066\u304f\u3060\u3055\u3044\u3002\n\n"
            "\u4e2d\u6587\uff1a\u672c\u7535\u5b50\u90ae\u4ef6\u53ca\u5176\u9644\u4ef6\u4ec5\u4f9b\u6307\u5b9a\u6536\u4ef6\u4eba\u4f7f\u7528\uff0c\u53ef\u80fd\u5305\u542bContoso\u91d1\u878d\u670d\u52a1\u516c\u53f8\u7684"
            "\u673a\u5bc6\u548c\u7279\u6743\u4fe1\u606f\u3002\u672a\u7ecf\u6388\u6743\u7684\u5ba1\u9605\u3001\u4f7f\u7528\u3001\u62ab\u9732\u6216\u5206\u53d1\u5747\u88ab\u4e25\u683c\u7981\u6b62\u3002\u5982\u679c\u60a8\u4e0d\u662f"
            "\u6307\u5b9a\u7684\u6536\u4ef6\u4eba\uff0c\u8bf7\u901a\u8fc7\u56de\u590d\u7535\u5b50\u90ae\u4ef6\u8054\u7cfb\u53d1\u4ef6\u4eba\u5e76\u9500\u6bc1\u539f\u59cb\u90ae\u4ef6\u7684\u6240\u6709\u526f\u672c\u3002\n\n"
            "\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550"
            "\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550"
            "\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550\u2550",
            "Hi,\n\n"
            "Can you add VPN access to the EU regional network for {name} in "
            "{department}? We're joining the EMEA Regulatory Alignment initiative "
            "and need access to the 10.44.0.0/16 subnet. Manager approval is on file.\n\n"
            "Regards,\n{name}\n\n"
            "---\n"
            "NOTICE DE CONFIDENTIALIT\u00c9: Ce message est confidentiel. "
            "CONFIDENTIALITY NOTICE: This message is confidential. "
            "VERTRAULICHKEITSHINWEIS: Diese Nachricht ist vertraulich. "
            "\u4fdd\u5bc6\u58f0\u660e\uff1a\u672c\u90ae\u4ef6\u4e3a\u673a\u5bc6\u4fe1\u606f\u3002"
            "\u6a5f\u5bc6\u4fdd\u6301\uff1a\u3053\u306e\u30e1\u30fc\u30eb\u306f\u6a5f\u5bc6\u3067\u3059\u3002"
            "\u0625\u0634\u0639\u0627\u0631 \u0627\u0644\u0633\u0631\u064a\u0629: "
            "\u0647\u0630\u0647 \u0627\u0644\u0631\u0633\u0627\u0644\u0629 \u0633\u0631\u064a\u0629. "
            "AVISO DE CONFIDENCIALIDADE: "
            "Esta mensagem \u00e9 confidencial. "
            "\u041f\u0420\u0415\u0414\u0423\u041f\u0420\u0415\u0416\u0414\u0415\u041d\u0418\u0415: "
            "\u042d\u0442\u043e \u0441\u043e\u043e\u0431\u0449\u0435\u043d\u0438\u0435 "
            "\u044f\u0432\u043b\u044f\u0435\u0442\u0441\u044f "
            "\u043a\u043e\u043d\u0444\u0438\u0434\u0435\u043d\u0446\u0438\u0430\u043b\u044c\u043d\u044b\u043c.\n\n"
            "This email and any attachments are for the sole use of the intended "
            "recipient(s). Unauthorized use, disclosure, or distribution is "
            "prohibited. If you received this in error, delete it immediately.",
        ],
        next_best_actions=[
            "Provision VPN access to the APAC regional network for the user for "
            "their cross-border project — verify manager approval and process by "
            "end of week.",
            "Set up VPN access to the regional network for the user joining a "
            "cross-border initiative — confirm manager sign-off and configure "
            "the appropriate network profile.",
        ],
        remediation_steps=[
            [
                "Verify the access request approval from the named manager in the access governance portal",
                "Create a VPN access profile for the target regional network subnet in the GlobalProtect admin console",
                "Assign the profile to the user's AD account and add them to the appropriate project security group",
                "Send the user VPN configuration instructions and test connectivity to a target host",
                "Set a review date for the access in 90 days per the temporary project access policy",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# dc-046  JSON payload from automated monitoring alert
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="dc-046",
        category=Category.DATA,
        priority=Priority.P2,
        assigned_team=Team.DATA_PLATFORM,
        needs_escalation=True,
        missing_information=[MissingInfo.PREVIOUS_TICKET_ID],
        subjects=[
            "[ALERT] CRITICAL \u2014 disk space threshold exceeded",
            "[MONITORING] CRITICAL: Disk usage above 95% on production SQL node",
            "[AUTO-ALERT] Storage critical \u2014 production database volume nearing capacity",
        ],
        descriptions=[
            "{\n"
            '  "alert_id": "MON-2026-031718-4492",\n'
            '  "alert_type": "DiskSpaceThresholdExceeded",\n'
            '  "severity": "CRITICAL",\n'
            '  "timestamp": "2026-03-17T18:14:33.209Z",\n'
            '  "source": {\n'
            '    "hostname": "PROD-SQL-NODE-03.contoso.local",\n'
            '    "ip_address": "10.20.5.43",\n'
            '    "datacenter": "US-East-1",\n'
            '    "rack": "R14-B",\n'
            '    "os": "Windows Server 2022 Datacenter",\n'
            '    "role": "SQL Server Production Node"\n'
            "  },\n"
            '  "disk_metrics": {\n'
            '    "drive_letter": "E:",\n'
            '    "volume_label": "SQLData",\n'
            '    "total_capacity_gb": 2048,\n'
            '    "used_gb": 1946.7,\n'
            '    "free_gb": 101.3,\n'
            '    "percent_used": 95.06,\n'
            '    "threshold_percent": 90,\n'
            '    "growth_rate_gb_per_day": 12.4,\n'
            '    "estimated_days_until_full": 8.2\n'
            "  },\n"
            '  "top_consumers": [\n'
            '    {"database": "TradeHistory", "size_gb": 743.2, "growth_30d_gb": 89.1},\n'
            '    {"database": "AuditLog", "size_gb": 512.8, "growth_30d_gb": 156.3},\n'
            '    {"database": "MarketData", "size_gb": 398.4, "growth_30d_gb": 42.7},\n'
            '    {"database": "ClientPortfolios", "size_gb": 187.1, "growth_30d_gb": 18.9},\n'
            '    {"database": "TempDB", "size_gb": 105.2, "growth_30d_gb": 0.0}\n'
            "  ],\n"
            '  "recent_events": [\n'
            '    {"timestamp": "2026-03-15T02:00:00Z", '
            '"event": "Nightly backup completed \u2014 1.2TB transferred"},\n'
            '    {"timestamp": "2026-03-16T02:00:00Z", '
            '"event": "AuditLog retention job FAILED \u2014 old records not purged"},\n'
            '    {"timestamp": "2026-03-17T02:00:00Z", '
            '"event": "Nightly backup completed \u2014 1.2TB transferred"}\n'
            "  ],\n"
            '  "escalation": {\n'
            '    "notify_team": "data-platform-oncall",\n'
            '    "auto_ticket": true,\n'
            '    "sla_response_minutes": 60\n'
            "  }\n"
            "}",
            "{\n"
            '  "alert_id": "MON-2026-031719-5513",\n'
            '  "alert_type": "DiskSpaceThresholdExceeded",\n'
            '  "severity": "CRITICAL",\n'
            '  "timestamp": "2026-03-17T19:22:41.887Z",\n'
            '  "source": {\n'
            '    "hostname": "PROD-SQL-NODE-07.contoso.local",\n'
            '    "ip_address": "10.20.5.87",\n'
            '    "datacenter": "EU-West-1",\n'
            '    "os": "Windows Server 2022 Datacenter",\n'
            '    "role": "SQL Server Analytics Node"\n'
            "  },\n"
            '  "disk_metrics": {\n'
            '    "drive_letter": "F:",\n'
            '    "volume_label": "AnalyticsData",\n'
            '    "total_capacity_gb": 4096,\n'
            '    "used_gb": 3932.1,\n'
            '    "free_gb": 163.9,\n'
            '    "percent_used": 96.0,\n'
            '    "threshold_percent": 90,\n'
            '    "growth_rate_gb_per_day": 28.6,\n'
            '    "estimated_days_until_full": 5.7\n'
            "  },\n"
            '  "top_consumers": [\n'
            '    {"database": "RiskModels", "size_gb": 1287.3, "growth_30d_gb": 312.0},\n'
            '    {"database": "MarketDataArchive", "size_gb": 984.1, "growth_30d_gb": 167.4},\n'
            '    {"database": "ReportingDW", "size_gb": 872.4, "growth_30d_gb": 94.2}\n'
            "  ],\n"
            '  "recent_events": [\n'
            '    {"timestamp": "2026-03-16T03:00:00Z", '
            '"event": "ETL batch completed \u2014 218 GB ingested"},\n'
            '    {"timestamp": "2026-03-17T03:00:00Z", '
            '"event": "ETL batch completed \u2014 241 GB ingested \u2014 ABOVE NORMAL"},\n'
            '    {"timestamp": "2026-03-17T14:00:00Z", '
            '"event": "Archive job SKIPPED \u2014 maintenance window conflict"}\n'
            "  ],\n"
            '  "escalation": {\n'
            '    "notify_team": "data-platform-oncall",\n'
            '    "auto_ticket": true,\n'
            '    "sla_response_minutes": 30\n'
            "  }\n"
            "}",
        ],
        next_best_actions=[
            "Address critical disk space on production SQL node (drive at 95%+ \u2014 "
            "estimated 5\u20138 days until full). A failed retention or archive job is the "
            "most likely cause of accelerated growth \u2014 fix the retention job first, "
            "then evaluate capacity expansion.",
            "Investigate critical storage alert on production SQL node \u2014 disk "
            "utilization above 95% and growing rapidly due to a skipped or failed "
            "maintenance job.",
        ],
        remediation_steps=[
            [
                "Investigate and fix the failed retention or archive job that caused unpurged growth",
                "Manually run the purge or archive to reclaim space from records past the retention window",
                "Review TempDB sizing and shrink if allocation is excessive for current workload",
                "Request an emergency capacity expansion if free space drops below 5% before the fix takes effect",
                "Set up a recurring disk space trend report and adjust the alert threshold to trigger earlier",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# dc-047  Excessive whitespace, irregular spacing, and blank lines
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="dc-047",
        category=Category.HARDWARE,
        priority=Priority.P3,
        assigned_team=Team.ENDPOINT,
        needs_escalation=False,
        missing_information=[MissingInfo.DEVICE_INFO],
        subjects=[
            "Printer on {floor} not working",
            "Floor  printer   broken  — need  help  urgently",
            "Shared    printer     stuck     on   paper    jam    error",
        ],
        descriptions=[
            "Hi   IT    Support,\n\n\n\n\n"
            "The    printer   on    the   {floor}    near   conference   "
            "room   B   is     not     working.\n\n\n\n\n\n\n"
            "It    is    a    HP    LaserJet    Pro    MFP    M428fdn    and   "
            'the     display     says     "Paper   Jam"     but     I   '
            "checked     and     there    is    no     paper     stuck   "
            "anywhere.\n\n\n\n\n\n"
            "I     tried:\n\n\n"
            "-     Turning     it     off     and     on     again\n\n\n"
            "-     Opening     all     the     trays     and     checking   "
            "for     paper\n\n\n"
            "-     Removing     the     toner     cartridge     and   "
            "reinserting     it\n\n\n\n\n\n"
            "Nothing     worked.     The     paper     jam     error   "
            "keeps     coming     back.\n\n\n\n\n"
            "This     is     the     only     printer     on     our   "
            "floor     and     we     have     a     client     presentation   "
            "at     3 PM     today     that     we     need     to   "
            "print     materials     for.\n\n\n\n\n\n\n\n"
            "Please     send     someone     to     look     at     it   "
            "ASAP.\n\n\n\n\n"
            "Thanks,\n\n\n"
            "{name}\n\n\n"
            "{department},     {floor},     {building}",
            "hi\n\n\n\n\n\n"
            "the       printer      on      our      floor      keeps      saying\n\n\n"
            "paper      jam\n\n\n\n\n"
            "but      there      is      no      paper      jammed      in      it\n\n\n\n"
            "ive      opened      every      tray\n\n\n\n\n\n"
            "and      checked      everywhere\n\n\n\n"
            "please      fix\n\n\n\n\n\n\n\n"
            "it      is      the      HP      one      near      the      elevators\n\n\n"
            "on      {floor}\n\n\n\n\n\n\n"
            "thanks\n\n\n\n"
            "{name}",
        ],
        next_best_actions=[
            "Dispatch a technician to inspect the HP LaserJet Pro MFP M428fdn with "
            "a persistent false paper jam error \u2014 user has a client presentation and "
            "needs it fixed urgently.",
            "Troubleshoot persistent false paper jam error on floor printer \u2014 user "
            "has checked all trays with no obstruction found.",
        ],
        remediation_steps=[
            [
                "Dispatch a technician to physically inspect the printer",
                "Check the paper path sensors for debris, torn paper fragments, or sensor misalignment",
                "Perform a full power cycle with the rear access panel open and inspect the fuser area",
                "If the sensor is faulty, replace the paper path sensor assembly or swap in a loaner printer",
                "Update the printer asset record with any parts replaced and schedule preventive maintenance",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# dc-048  Corrupted email headers / SMTP headers mixed into body
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="dc-048",
        category=Category.ACCESS_AUTH,
        priority=Priority.P1,
        assigned_team=Team.IAM,
        needs_escalation=True,
        missing_information=[MissingInfo.DEVICE_INFO, MissingInfo.AUTHENTICATION_METHOD],
        subjects=[
            "Account locked out \u2014 need urgent help",
            "URGENT: Account lockout \u2014 suspicious MFA activity",
            "Locked out of everything \u2014 possible unauthorized access attempt",
        ],
        descriptions=[
            "Return-Path: <{name1}@contoso.com>\n"
            "Received: from PROD-EXCH-04.contoso.local (10.20.1.44) by\n"
            " PROD-EXCH-HUB-02.contoso.local (10.20.1.10) with Microsoft SMTP\n"
            " Server (version=TLS1_2, cipher=TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384)\n"
            " id 15.2.1118.40; Tue, 17 Mar 2026 08:47:12 -0400\n"
            "Received: from outlook.office365.com (52.97.183.26) by\n"
            " PROD-EXCH-04.contoso.local (10.20.1.44) with Microsoft SMTP Server\n"
            " id 15.2.1118.40 via Frontend Transport; Tue, 17 Mar 2026 08:47:11 -0400\n"
            "DKIM-Signature: v=1; a=rsa-sha256; c=relaxed/relaxed;\n"
            " d=contoso.com; s=selector1;\n"
            " h=From:Date:Subject:Message-ID:Content-Type:MIME-Version;\n"
            " bh=a3f2V8bKz0mNpQ7RtL1cD+eXwJk=;\n"
            " b=YjQ4NWRlZWI3ZjJhMTk4NzVkNzRiMmQxZGM5OTNmYTBlZjRiMjVhNWFl\n"
            "   OGEyMTc5ZjRkZGE2MzI0YTVlNWQyZjQ1MzZhMGI3YWIwN2ExMjczNjVk\n"
            "   MjkwNjg2YTgzZGZhYjNlOGE=\n"
            "X-Mailer: Microsoft Outlook 16.0\n"
            "MIME-Version: 1.0\n"
            "Content-Type: multipart/alternative;\n"
            ' boundary="----=_NextPart_001_0078_01DAF3B2.7C8E5A30"\n'
            "X-MS-Exchange-Organization-SCL: -1\n"
            "X-MS-Exchange-Organization-AuthSource: PROD-EXCH-04.contoso.local\n"
            "X-MS-Exchange-Organization-AuthAs: Internal\n"
            "X-MS-Has-Attach:\n"
            "X-MS-TNEF-Correlator:\n\n"
            "Hi IT Support,\n\n"
            "My account has been locked out and I cannot log into anything \u2014 "
            "not my laptop, not Outlook, not any of the internal web apps. "
            "This happened at around 8:30 AM this morning when I tried to "
            "sign in after arriving at the office.\n\n"
            "I did NOT change my password recently and I am certain I am "
            "entering the correct credentials. I suspect the lockout may be "
            "related to the MFA push notifications I was getting last night "
            "around 11 PM that I did not initiate \u2014 I denied all of them. "
            "Someone may be trying to access my account.\n\n"
            "This is urgent because I have a compliance audit review at "
            "10 AM and I need access to the Regulatory Reporting portal "
            "before then.\n\n"
            "Please help ASAP.\n\n"
            "{name}\n{department}",
            "X-Mailer: Outlook/16.0\n"
            "Content-Type: text/plain; charset=UTF-8\n"
            "X-MS-Exchange-Organization-SCL: 1\n"
            "X-Originating-IP: [10.20.3.115]\n"
            "Return-Path: <{name1}@contoso.com>\n\n"
            "Subject: URGENT account lockout\n\n"
            "I've been locked out of my account since 7 AM this morning. "
            "I can't access anything \u2014 laptop login fails, OWA returns "
            "'Your account has been locked', and VPN rejects my credentials.\n\n"
            "I was getting MFA prompts on my phone last night that I didn't "
            "request. I denied them but this morning my account was locked.\n\n"
            "I need immediate help \u2014 I have a client meeting at 9:30 AM.\n\n"
            "{name}\n{department}",
        ],
        next_best_actions=[
            "Investigate account lockout with suspicious MFA activity \u2014 user "
            "reports uninitiated MFA push notifications the prior evening followed "
            "by a full account lockout. Possible unauthorized access attempt. "
            "Unlock the account and review sign-in logs for anomalous activity.",
            "Unlock the user's account and immediately review Entra ID sign-in "
            "logs for the suspicious MFA prompts reported the previous night "
            "\u2014 possible credential compromise or MFA fatigue attack.",
        ],
        remediation_steps=[
            [
                "Unlock the user's account in Entra ID and reset their password via a secure channel",
                "Review Entra ID sign-in logs for failed attempts and suspicious IP addresses around the "
                "time of the uninitiated MFA prompts",
                "If unauthorized access is confirmed, revoke all active sessions and refresh tokens",
                "Advise the user to re-register MFA and switch to number-matching or FIDO2 if currently "
                "using simple push approvals",
                "Escalate to Security Operations if the sign-in logs indicate a credential compromise or "
                "MFA fatigue attack",
            ],
        ],
    )
)


# ---------------------------------------------------------------------------
# dc-049  ALL CAPS email body with poor grammar — VPN issue
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="dc-049",
        category=Category.NETWORK,
        priority=Priority.P3,
        assigned_team=Team.NETWORK,
        needs_escalation=False,
        missing_information=[
            MissingInfo.DEVICE_INFO,
            MissingInfo.NETWORK_LOCATION,
        ],
        subjects=[
            "VPN NOT WORKING!!!",
            "CANT CONNECT TO VPN PLEASE HELP",
            "VPN IS DOWN AGAIN FIX IT",
        ],
        descriptions=[
            "HI IT TEAM,\n\n"
            "MY VPN IS NOT WORKING AGAIN AND I CANT DO MY JOB. "
            "I TRYED RESTARTING MY COMPUTER LIKE 5 TIMES AND IT "
            "STILL DONT WORK. EVERY TIME I CLICK CONNECT IT SAYS "
            "ERROR AND THEN NOTHING HAPPENS. I DONT NO WHAT THE "
            "ERROR CODE IS BECAUSE IT GOES AWAY TO FAST.\n\n"
            "I NEED THIS FIXED RITE NOW BECAUSE I HAVE A DEADLINE "
            "TODAY AND I CANT ACCESS ANY OF THE SHARED DRIVES OR "
            "INTERNAL SITES FROM HOME. THIS HAS BEEN HAPENING SINCE "
            "LAST WEEK BUT TODAY IT IS THE WORSE ITS EVER BEEN.\n\n"
            "ALSO MY INTERNET IS FINE BECAUSE I CAN USE GOOGLE AND "
            "YOUTUBE NO PROBLEM SO ITS DEFINTELY A VPN ISSUE NOT A "
            "INTERNET ISSUE.\n\n"
            "PLEASE FIX ASAP!!!\n\n"
            "{name}\n{department}",
            "HELLO,\n\n"
            "I BEEN TRYING TO CONNECT TO THE VPN ALL MORNING AND "
            "IT KEEPS SAYING AUTHENTICATION FAILED BUT MY PASSWORD "
            "IS CORRECT I JUST CHANGED IT YESTERDAY. I ALSO TRYED "
            "THE BACKUP VPN SERVER AND THAT DONT WORK NEITHER.\n\n"
            "I AM WORKING FROM {office} TODAY AND NOBODY ELSE ON "
            "MY TEAM SEEMS TO HAVE THIS PROBLEM SO I DONT KNOW "
            "WHATS GOING ON. CAN SOMEONE PLEASE CALL ME OR REMOTE "
            "INTO MY COMPUTER TO FIX THIS? I DONT UNDERSTAND THE "
            "TECHNICAL STUFF.\n\n"
            "THANKS,\n{name}",
        ],
        next_best_actions=[
            "Clarify the VPN error message and gather device "
            "details \u2014 user reports persistent VPN connection "
            "failures but did not capture the error code. Verify "
            "VPN client version and credential status.",
            "Investigate VPN authentication failure \u2014 user "
            "recently changed password and may have a credential "
            "sync delay. Check VPN logs for the specific error "
            "and confirm client configuration.",
        ],
        remediation_steps=[
            [
                "Ask the user to capture a screenshot of the VPN error message on the next connection attempt",
                "Verify the VPN client version is current and supported by the organization",
                "Confirm the user\u2019s password change has "
                "propagated to all authentication systems "
                "including RADIUS and NPS",
                "Test connectivity to the VPN gateway using ping and traceroute from the user\u2019s machine",
                "If the issue persists, collect VPN client diagnostic logs and escalate to network engineering",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# dc-050  Hex dump pasted into email
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="dc-050",
        category=Category.DATA,
        priority=Priority.P2,
        assigned_team=Team.DATA_PLATFORM,
        needs_escalation=False,
        missing_information=[MissingInfo.ERROR_MESSAGE, MissingInfo.ENVIRONMENT_DETAILS],
        subjects=[
            "Shared drive corrupted file — hex dump attached",
            "Excel file on file server won't open — hex output inside",
            "Critical report file corrupted — hexdump for reference",
        ],
        descriptions=[
            "Hi,\n\n"
            "A critical Excel file on the shared drive (\\\\NYC-FS-01\\{department}\\Q1-Reports\\"
            "revenue_summary.xlsx) seems to be corrupted. When I try to open it, Excel "
            "says the file format is not valid. I ran hexdump on it and the header "
            "doesn't look right:\n\n"
            "00000000  50 4b 03 04 14 00 06 00  08 00 00 00 21 00 b5 55  |PK..........!..U|\n"
            "00000010  30 23 f4 00 00 00 4c 02  00 00 13 00 08 02 5b 43  |0#....L.......[C|\n"
            "00000020  6f 6e 74 65 6e 74 5f 54  79 70 65 73 5d 2e 78 6d  |ontent_Types].xm|\n"
            "00000030  6c 20 a2 04 02 28 a0 00  02 00 00 00 00 00 00 00  |l ...(.........|\n"
            "00000040  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|\n"
            "*\n"
            "00000100  00 00 00 00 00 00 00 00  ff ff ff ff ff ff ff ff  |................|\n"
            "00000110  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|\n"
            "*\n"
            '00000200  3c 3f 78 6d 6c 20 76 65  72 73 69 6f 6e 3d 22 31  |<?xml version="1|\n'
            '00000210  2e 30 22 20 65 6e 63 6f  64 69 6e 67 3d 22 55 54  |.0" encoding="UT|\n'
            '00000220  46 2d 38 22 3f 3e 0d 0a  00 00 00 00 00 00 00 00  |F-8"?>..........|\n\n'
            "The file was last modified yesterday at 4:47 PM by an automated ETL process. "
            "The file is about 2.4 MB and contains Q1 revenue data we need for the board "
            "presentation tomorrow morning. Other files in the same directory seem fine.\n\n"
            "Thanks,\n{name}\n{department}",
            "Hi IT,\n\n"
            "I'm getting 'The file is corrupt and cannot be opened' when trying to access "
            "a shared report at \\\\PROD-FS-02\\Reports\\quarterly_summary.xlsx. I used "
            "hexdump to look at the raw bytes:\n\n"
            "00000000  50 4b 03 04 14 00 06 00  08 00 00 00 21 00 c3 44  |PK..........!..D|\n"
            "00000010  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|\n"
            "*\n"
            "00000080  ff ff ff ff ff ff ff ff  ff ff ff ff ff ff ff ff  |................|\n"
            "00000090  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  |................|\n\n"
            "The ZIP header looks partially zeroed out. This file is critical for our "
            "{department} quarterly review and we need it restored from backup ASAP.\n\n"
            "{name}",
        ],
        next_best_actions=[
            "Investigate corrupted Excel file on the file server — ZIP header appears "
            "partially zeroed out. Check the ETL process and restore from Volume Shadow "
            "Copy or backup.",
            "Restore corrupted XLSX file from backup or Volume Shadow Copy — the file "
            "header is damaged, likely due to an interrupted write from an ETL process.",
        ],
        remediation_steps=[
            [
                "Attempt to restore the file from Volume Shadow Copy on the file server",
                "If no shadow copy is available, restore from the nightly backup",
                "Investigate ETL process logs for errors during the last write that may have caused corruption",
                "Check disk health on the file server for I/O errors or SMART warnings",
                "Once restored, verify file integrity by opening in Excel and validating the ZIP structure",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# dc-051  Double-encoded HTML entities
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="dc-051",
        category=Category.SOFTWARE,
        priority=Priority.P2,
        assigned_team=Team.ENTERPRISE_APPS,
        needs_escalation=False,
        missing_information=[MissingInfo.APPLICATION_VERSION, MissingInfo.STEPS_TO_REPRODUCE],
        subjects=[
            "Login page shows garbled text &amp;mdash; can&amp;#39;t sign in",
            "Portal login page rendering broken — HTML entities everywhere",
            "Internal site shows &amp;ldquo; and &amp;nbsp; instead of normal text",
        ],
        descriptions=[
            "Hi IT,\n\n"
            "When I go to the internal portal at https://portal.contoso.com, the "
            "login page is showing garbled text. The page title shows:\n\n"
            "  &amp;ldquo;Contoso&amp;nbsp;Financial&amp;nbsp;Services "
            "&amp;mdash;&amp;nbsp;Sign&amp;nbsp;In&amp;rdquo;\n\n"
            "And the form labels say:\n"
            "  &amp;bull; &amp;ldquo;Username&amp;rdquo;\n"
            "  &amp;bull; &amp;ldquo;Password&amp;rdquo;\n"
            "  &amp;bull; &amp;ldquo;Remember&amp;nbsp;Me&amp;rdquo;\n\n"
            "The &amp;ldquo;Sign In&amp;rdquo; button text shows as "
            "&amp;quot;Sign&amp;nbsp;In&amp;quot; and when I click it, I get "
            "an error:\n\n"
            "  &amp;lt;div class=&amp;quot;error&amp;quot;&amp;gt;\n"
            "    &amp;lt;p&amp;gt;Authentication failed: invalid "
            "token&amp;lt;/p&amp;gt;\n"
            "  &amp;lt;/div&amp;gt;\n\n"
            "I&amp;#39;ve tried clearing my cache and using different browsers "
            "but the issue persists. I&amp;#39;m on Windows 11.\n\n"
            "This is blocking me from accessing the compliance reporting dashboard.\n\n"
            "Thanks,\n{name}\n{department}",
            "The internal portal login page is completely garbled with double-encoded "
            "HTML entities. Every &amp;quot; &amp;nbsp; &amp;lt; &amp;gt; is showing "
            "literally instead of rendering correctly. For example the heading reads:\n\n"
            "&amp;ldquo;Welcome&amp;nbsp;to&amp;nbsp;Contoso&amp;rdquo;\n\n"
            "And the error message after login attempt displays raw HTML tags:\n"
            "&amp;lt;span&amp;gt;Invalid&amp;nbsp;credentials&amp;lt;/span&amp;gt;\n\n"
            "Multiple people on {floor} are seeing the same thing. This started "
            "after the deployment last night.\n\n"
            "{name}\n{department}",
        ],
        next_best_actions=[
            "Investigate double-encoded HTML entities on the internal portal login "
            "page — likely a deployment issue with the template rendering engine "
            "causing both display and authentication failures.",
            "Check the most recent deployment to portal.contoso.com for template "
            "rendering changes that may be double-encoding HTML entities and "
            "corrupting CSRF tokens.",
        ],
        remediation_steps=[
            [
                "Check the most recent deployment for template rendering changes that "
                "may be double-encoding HTML entities",
                "Verify the web application's content-type headers and character "
                "encoding settings (UTF-8 vs ISO-8859-1)",
                "Check the authentication token endpoint — the invalid token error may "
                "be caused by encoding issues corrupting CSRF tokens",
                "Roll back to the previous known-good deployment if the issue is confirmed to be a recent change",
                "Test the portal from multiple browsers and networks to confirm the fix",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# dc-052  Chat transcript with bot messages and timestamps
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="dc-052",
        category=Category.HARDWARE,
        priority=Priority.P2,
        assigned_team=Team.ENDPOINT,
        needs_escalation=False,
        missing_information=[MissingInfo.DEVICE_INFO, MissingInfo.ERROR_MESSAGE],
        subjects=[
            "Laptop keeps blue-screening — pasted chat history for context",
            "BSOD 2-3 times daily — forwarding Slack conversation",
            "Recurring blue screen crashes — chat transcript attached",
        ],
        descriptions=[
            "[2026-03-16 14:23:01] @{name1}: hey can anyone help? my laptop "
            "keeps blue-screening\n"
            "[2026-03-16 14:23:05] \U0001f916 ContosBot: Hi! I see you might have a "
            "technical issue. Would you like me to create a support ticket? "
            "React with \U0001f44d to confirm.\n"
            "[2026-03-16 14:23:12] @{name1} reacted with \U0001f44d\n"
            "[2026-03-16 14:23:15] \U0001f916 ContosBot: Ticket created.\n"
            "[2026-03-16 14:24:30] @mike.chen: what's the error code?\n"
            "[2026-03-16 14:25:01] @{name1}: it says KERNEL_DATA_INPAGE_ERROR "
            "and then restarts\n"
            "[2026-03-16 14:25:45] @mike.chen: that's usually a disk issue. "
            "how old is your laptop?\n"
            "[2026-03-16 14:26:10] @{name1}: it's a Lenovo ThinkPad X1 Carbon "
            "Gen 11, got it about 18 months ago\n"
            "[2026-03-16 14:26:30] \U0001f916 ContosBot: \U0001f4ca Daily standup "
            "reminder: Your standup is in 4 minutes!\n"
            "[2026-03-16 14:27:00] @{name1}: also it's been really slow and the "
            "fan goes crazy even when I'm just in Outlook\n"
            "[2026-03-16 14:28:00] \U0001f916 ContosBot: \U0001f389 Kudos! @sarah "
            "received a kudos from @david!\n"
            "[2026-03-16 14:28:15] @{name1}: the blue screen happens 2-3 times a "
            "day, always when I have lots of tabs open and large spreadsheets.\n"
            "[2026-03-16 14:28:30] @{name1}: I'm on {floor}, Building 1\n"
            "[2026-03-16 14:28:45] \U0001f916 ContosBot: \U0001f4c5 Meeting update: "
            "'Client Review Call' moved to 3:30 PM.",
            "[14:02] {name1}: my computer keeps crashing with a blue screen\n"
            "[14:02] Bot: \U0001f916 Creating ticket...\n"
            "[14:03] {name1}: SYSTEM_SERVICE_EXCEPTION every time I open Chrome "
            "with more than 10 tabs\n"
            "[14:04] @helpdesk_joe: what's your machine model?\n"
            "[14:04] {name1}: Dell Latitude 5540\n"
            "[14:05] Bot: \U0001f514 Reminder: Team sync in 25 minutes\n"
            "[14:05] {name1}: also the screen flickers before the crash. "
            "I'm in the {department} area, {floor}\n"
            "[14:06] Bot: \U0001f3c6 Weekly highlight: 42 tickets resolved!\n"
            "[14:06] {name1}: this has been going on for a week. Very disruptive.",
        ],
        next_best_actions=[
            "Run hardware diagnostics on the user's laptop — recurring blue screens "
            "(KERNEL_DATA_INPAGE_ERROR or SYSTEM_SERVICE_EXCEPTION) 2-3 times daily "
            "suggest possible SSD failure or driver issue.",
            "Investigate recurring BSOD on the user's laptop — likely SSD degradation "
            "or a driver conflict given the frequency and symptoms.",
        ],
        remediation_steps=[
            [
                "Run hardware diagnostics focusing on SSD health (SMART status, "
                "reallocated sector count, read/write error rates)",
                "Check Windows Event Viewer for disk-related errors (Event IDs 7, 11, "
                "51, 153) around the times of the blue screens",
                "If SSD is degrading, immediately back up user data and arrange a replacement drive or laptop swap",
                "As a temporary measure, reduce Chrome tab count and consider moving "
                "large workbooks to OneDrive streaming to reduce disk I/O",
                "Monitor for recurrence over the next 48 hours after hardware replacement",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# dc-053  Windows Registry export dump
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="dc-053",
        category=Category.SOFTWARE,
        priority=Priority.P3,
        assigned_team=Team.ENTERPRISE_APPS,
        needs_escalation=False,
        missing_information=[MissingInfo.CONFIGURATION_DETAILS],
        subjects=[
            "Outlook keeps resetting default signature — registry export included",
            "Email signature reverts on every restart — GPO issue?",
            "Outlook ignoring my updated signature — registry dump inside",
        ],
        descriptions=[
            "Hi IT,\n\n"
            "Every time I restart Outlook, my email signature resets to the old one "
            "from 2024 instead of my updated signature. I exported the registry key:\n\n"
            "Windows Registry Editor Version 5.00\n\n"
            "[HKEY_CURRENT_USER\\SOFTWARE\\Microsoft\\Office\\16.0\\Outlook\\Profiles\\"
            "Outlook\\9375CFF0413111d3B88A00104B2A6676\\00000002]\n"
            '"Account Name"="corporate.email@contoso.com"\n'
            '"New Signature"="Contoso_Corporate_2024"\n'
            '"Reply-Forward Signature"="Contoso_Corporate_2024"\n'
            '"Identity Eid"=hex:00,00,00,00,dc,a7,40,c8,c0,42,10,1a,b4,b9,08,00,2b,2f,e1,82,\\\n'
            "  01,00,00,00,03,00,00,00\n"
            '"Identity Search Key"=hex:dc,a7,40,c8,c0,42,10,1a,b4,b9,08,00,2b,2f,e1,82,01,\\\n'
            "  00,00,00,03,00,00,00\n\n"
            "[HKEY_CURRENT_USER\\SOFTWARE\\Microsoft\\Office\\16.0\\Common\\MailSettings]\n"
            '"NewSignature"="Contoso_Corporate_2024"\n'
            '"ReplySignature"="Contoso_Corporate_2024"\n'
            '"ComposeFontComplex"=hex:3c,68,74,6d,6c,3e,0d,0a,0d,0a,3c,68,65,61,64,3e,0d,\\\n'
            "  0a,3c,73,74,79,6c,65,3e,0d,0a\n\n"
            "As you can see, the registry still points to 'Contoso_Corporate_2024' "
            "but my updated signature is called 'Contoso_Corporate_2026'. I think "
            "the Group Policy is pushing the old name. I've tried manually editing "
            "the registry but it gets overwritten on restart.\n\n"
            "Running Outlook 16.0.18025 on Windows 11 Enterprise.\n\n"
            "{name}\n{department}",
            "My Outlook email signature keeps reverting. I've dumped the relevant "
            "registry keys:\n\n"
            "[HKEY_CURRENT_USER\\SOFTWARE\\Microsoft\\Office\\16.0\\Outlook\\Setup]\n"
            '"First-Run"=dword:00000001\n'
            '"CreateWelcome"=dword:00000000\n\n'
            "[HKEY_CURRENT_USER\\SOFTWARE\\Microsoft\\Office\\16.0\\Common\\MailSettings]\n"
            '"NewSignature"="OldSignature_v3"\n'
            '"ReplySignature"="OldSignature_v3"\n'
            '"Stationery"=""\n\n'
            "A GPO seems to be forcing 'OldSignature_v3' but the correct name is "
            "'NewSignature_v5'. This happens to multiple people in {department}.\n\n"
            "{name}",
        ],
        next_best_actions=[
            "Investigate Group Policy Object overriding Outlook email signature "
            "setting — registry shows an old signature name being pushed over "
            "the user's updated signature on every restart.",
            "Check the GPO linked to the user's OU for Outlook signature settings "
            "that may be enforcing an outdated signature name.",
        ],
        remediation_steps=[
            [
                "Check the Group Policy Object linked to the user's OU for Outlook "
                "signature settings enforcing the old signature name",
                "Run 'gpresult /H gpresult.html' to confirm which GPO is applying the signature preference",
                "Update the GPO to reference the correct signature name or remove "
                "the forced setting if individual choice is permitted",
                "Run 'gpupdate /force' on the user's machine after the GPO change",
                "Verify the signature persists across an Outlook restart",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# dc-054  HTTP request/response headers dump
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="dc-054",
        category=Category.SOFTWARE,
        priority=Priority.P1,
        assigned_team=Team.ENTERPRISE_APPS,
        needs_escalation=True,
        missing_information=[MissingInfo.ENVIRONMENT_DETAILS],
        subjects=[
            "Internal API returning 502 — full request/response dump",
            "Pricing API down — curl verbose output attached",
            "502 Bad Gateway on critical API — all backends timing out",
        ],
        descriptions=[
            "Hi team,\n\n"
            "The internal pricing API (pricing-api.contoso.internal) is returning 502 "
            "Bad Gateway errors intermittently. I captured with curl -v:\n\n"
            "> GET /api/v2/pricing/equity/MSFT HTTP/1.1\n"
            "> Host: pricing-api.contoso.internal\n"
            "> User-Agent: curl/8.4.0\n"
            "> Accept: application/json\n"
            "> Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9..."
            "fakepayload.fakesignature\n"
            "> X-Request-ID: 7f3a2b4c-9d1e-4f5a-b6c8-3e2d1f0a9b8c\n"
            "> Cache-Control: no-cache\n"
            ">\n"
            "< HTTP/1.1 502 Bad Gateway\n"
            "< Server: nginx/1.24.0\n"
            "< Date: Tue, 17 Mar 2026 14:23:45 GMT\n"
            "< Content-Type: text/html\n"
            "< X-Upstream-Status: failed\n"
            "< X-Upstream-Addr: 10.30.2.15:8080, 10.30.2.16:8080, 10.30.2.17:8080\n"
            "< X-Upstream-Response-Time: 30.001, 30.002, 30.003\n"
            "< Strict-Transport-Security: max-age=31536000\n"
            "<\n"
            "< <html><head><title>502 Bad Gateway</title></head>\n"
            "< <body><center><h1>502 Bad Gateway</h1></center></body></html>\n\n"
            "The upstream response times are all ~30s which looks like a timeout. "
            "All three backend nodes are failing. This is affecting the {department} "
            "desk — they can't get real-time pricing. Started about 30 minutes ago.\n\n"
            "{name}\n{department}",
            "Urgent: our {department} API endpoint is returning 502 errors.\n\n"
            "> POST /api/v1/data/query HTTP/1.1\n"
            "> Host: data-api.contoso.internal\n"
            "> Authorization: Bearer [REDACTED]\n"
            "> Content-Type: application/json\n"
            ">\n"
            "< HTTP/1.1 502 Bad Gateway\n"
            "< Server: nginx/1.24.0\n"
            "< X-Upstream-Addr: 10.40.1.10:9090, 10.40.1.11:9090\n"
            "< X-Upstream-Response-Time: 30.000, 30.000\n"
            "<\n"
            "Both upstream nodes are timing out at 30s. This is blocking our "
            "reporting pipeline.\n\n"
            "{name}",
        ],
        next_best_actions=[
            "Investigate 502 Bad Gateway on internal API — all upstream backend "
            "nodes are timing out at 30s. Critical impact on real-time operations.",
            "Check health and resource utilization on all upstream backend nodes — "
            "all are returning 30s timeouts indicating a systemic backend failure.",
        ],
        remediation_steps=[
            [
                "Check health and resource utilization (CPU, memory, disk I/O) on all upstream backend nodes",
                "Review application logs on the API service for errors or connection pool exhaustion",
                "Check the nginx reverse proxy configuration and upstream timeout settings",
                "Verify the downstream data provider is responding and not causing the backend to hang",
                "If a backend restart is needed, perform a rolling restart to maintain partial availability",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# dc-055  CID inline image references (broken Content-ID)
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="dc-055",
        category=Category.SOFTWARE,
        priority=Priority.P4,
        assigned_team=Team.ENDPOINT,
        needs_escalation=False,
        missing_information=[MissingInfo.APPLICATION_VERSION, MissingInfo.DEVICE_INFO],
        subjects=[
            "Desktop icons rearranged after reboot — screenshots inline",
            "Icons scrambled after Windows Update — see attached images",
            "Desktop layout keeps resetting — inline screenshots below",
        ],
        descriptions=[
            "Hi IT Support,\n\n"
            "Every time I restart my computer, all my desktop icons get rearranged "
            "into a random order.\n\n"
            "Here's what it looks like before (organized):\n"
            '<img src="cid:image001.png@01DAF2B3.A1B2C3D4" alt="Before" '
            'width="1920" height="1080">\n'
            "[cid:image001.png@01DAF2B3.A1B2C3D4 — image not displayed]\n\n"
            "And after the reboot (scrambled):\n"
            '<img src="cid:image002.png@01DAF2B3.E5F6A7B8" alt="After" '
            'width="1920" height="1080">\n'
            "[cid:image002.png@01DAF2B3.E5F6A7B8 — image not displayed]\n\n"
            "------=_Part_12345_67890.1710680400000\n"
            'Content-Type: image/png; name="image001.png"\n'
            "Content-Transfer-Encoding: base64\n"
            "Content-ID: <image001.png@01DAF2B3.A1B2C3D4>\n"
            "[base64 data stripped by mail gateway]\n\n"
            "I'm on Windows 11 Enterprise, {floor}, Building 3.\n\n"
            "{name}\n{department}",
            "My desktop icons keep rearranging every reboot. Some icons show as "
            "generic white rectangles:\n\n"
            '<img src="cid:screenshot_001.png@01DAF300.AABB0011" '
            'alt="broken icons">\n'
            "[cid:screenshot_001.png@01DAF300.AABB0011 — not displayed]\n\n"
            "------=_Part_99999_12345.1710680400000\n"
            'Content-Type: image/png; name="screenshot_001.png"\n'
            "Content-Transfer-Encoding: base64\n"
            "Content-ID: <screenshot_001.png@01DAF300.AABB0011>\n"
            "[base64 data removed]\n\n"
            "This started after the latest Windows Update. {floor}, Building 2.\n\n"
            "{name}",
        ],
        next_best_actions=[
            "Investigate desktop icon rearrangement and icon cache corruption on "
            "Windows 11 — icons scramble after every reboot. Low priority cosmetic "
            "issue but may indicate a profile or Group Policy conflict.",
        ],
        remediation_steps=[
            [
                "Check if a Group Policy or profile management tool (e.g., FSLogix) "
                "is resetting the desktop layout on logon",
                "Clear and rebuild the icon cache by deleting IconCache.db and restarting Explorer",
                "Verify the desktop layout is not managed by a mandatory profile or GPO",
                "Check if the triggering Windows Update included a shell or Explorer update",
                "If the issue persists, use a logon script to restore the saved layout",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# dc-056  Escaped JSON within JSON (triple-escaped)
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="dc-056",
        category=Category.DATA,
        priority=Priority.P1,
        assigned_team=Team.DATA_PLATFORM,
        needs_escalation=True,
        missing_information=[MissingInfo.AFFECTED_SYSTEM, MissingInfo.STEPS_TO_REPRODUCE],
        subjects=[
            "API error with nested JSON — can't parse response",
            "Compliance ETL failing — triple-escaped JSON in error body",
            "Data pipeline broken — API returns unreadable nested JSON error",
        ],
        descriptions=[
            "Our integration with the compliance reporting API is failing. The API "
            "returns an error response with triple-escaped JSON:\n\n"
            '{"status":"error","code":500,"message":"Internal processing failure",'
            '"details":"{\\"pipeline\\":\\"compliance-etl-v2\\",\\"stage\\":\\"transform'
            '\\",\\"error\\":{\\"type\\":\\"SchemaValidationError\\",\\"message\\":'
            '\\"Field \\\\\\\\\\\\\\"transaction_id\\\\\\\\\\\\\\" expected type '
            '\\\\\\\\\\\\\\"string\\\\\\\\\\\\\\" but received '
            '\\\\\\\\\\\\\\"null\\\\\\\\\\\\\\"\\"}}"}\n\n'
            "The actual issue is that null transaction_id values are getting through "
            "from the RawTransactions table in today's batch. This is breaking the "
            "compliance ETL pipeline and we can't generate the daily regulatory report.\n\n"
            "The pipeline runs on our Azure Data Factory instance. We need this fixed "
            "before the 5 PM regulatory filing deadline.\n\n"
            "{name}\n{department}",
            "The {department} data pipeline is returning deeply nested escaped JSON "
            "errors that are nearly impossible to read:\n\n"
            '{"error":"{\\"code\\":500,\\"inner\\":{\\"msg\\":\\"NULL values in '
            'required field\\",\\"table\\":\\"dbo.Transactions\\",'
            '\\"batch\\":\\"BATCH-{date}-0923\\"}}"}\n\n'
            "Translated: NULL values in dbo.Transactions are breaking the pipeline. "
            "Regulatory report deadline is 5 PM today.\n\n"
            "{name}",
        ],
        next_best_actions=[
            "Investigate null values in the source table causing the compliance ETL "
            "pipeline to fail — regulatory filing deadline is 5 PM today.",
            "Fix NULL data quality issue in the source table breaking the compliance "
            "ETL pipeline on Azure Data Factory — urgent regulatory deadline.",
        ],
        remediation_steps=[
            [
                "Query the source table for records with NULL values in required fields to assess scope",
                "Check the upstream data source for schema or NULL handling changes that introduced the bad records",
                "Patch or exclude the NULL records to unblock the current pipeline batch",
                "Add a NOT NULL constraint or pre-validation step to catch these issues at ingestion time",
                "Re-trigger the ETL pipeline after the data is corrected and verify "
                "the regulatory report generates successfully",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# dc-057  Tab-separated spreadsheet data pasted in email
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="dc-057",
        category=Category.ACCESS_AUTH,
        priority=Priority.P2,
        assigned_team=Team.IAM,
        needs_escalation=False,
        missing_information=[MissingInfo.AUTHENTICATION_METHOD, MissingInfo.CONFIGURATION_DETAILS],
        subjects=[
            "VPN users table — some accounts are locked",
            "Multiple VPN lockouts — user report pasted below",
            "Bulk VPN account lockout — spreadsheet data inside",
        ],
        descriptions=[
            "Hi IT,\n\n"
            "Several VPN users are getting locked out. I pulled a report from the "
            "VPN concentrator:\n\n"
            "Username\tFull Name\tDepartment\tLast Login\tStatus\tIP Address\t"
            "VPN Client\tOS\n"
            "jsmith01\tJohn Smith\tTrading\t2026-03-17 08:12:04\tACTIVE\t"
            "10.100.5.23\tGlobalProtect 6.1\tWindows 11\n"
            "mchen02\tMei Chen\tCompliance\t2026-03-17 08:14:22\tLOCKED\t"
            "10.100.5.45\tGlobalProtect 6.1\tWindows 11\n"
            "agarcia03\tAna Garcia\tFinance\t2026-03-17 08:15:01\tACTIVE\t"
            "10.100.5.67\tGlobalProtect 6.0\tmacOS 14.4\n"
            "bwilson04\tBen Wilson\tEngineering\t2026-03-17 08:16:33\tLOCKED\t"
            "10.100.5.89\tGlobalProtect 6.1\tWindows 11\n"
            "cpatel05\tChitra Patel\tRisk\t2026-03-17 08:17:15\tACTIVE\t"
            "10.100.5.101\tGlobalProtect 6.1\tWindows 11\n"
            "dkimura06\tDaichi Kimura\tData Eng\t2026-03-16 17:42:08\tLOCKED\t"
            "10.100.5.123\tGlobalProtect 6.1\tWindows 10\n"
            "fjohansson08\tFreya Johansson\tLegal\t2026-03-16 16:30:12\tLOCKED\t"
            "10.100.5.167\tGlobalProtect 6.1\tWindows 11\n"
            "iali11\tIbrahim Ali\tFixed Income\t2026-03-16 15:55:00\tLOCKED\t"
            "10.100.5.223\tGlobalProtect 5.3\tWindows 10\n\n"
            "So that's 5 locked accounts. They all seem to have been locked out "
            "this morning. We think it might be related to the password policy change "
            "pushed last night. These users are all remote and can't work.\n\n"
            "{name}\n{department}",
            "Multiple remote users reporting VPN lockouts. Here's the data:\n\n"
            "User\tDept\tStatus\tLast Seen\n"
            "{name1}\t{department}\tLOCKED\t2026-03-17 07:55\n"
            "r.santos\tTrading\tLOCKED\t2026-03-17 08:01\n"
            "k.lindberg\tLegal\tACTIVE\t2026-03-17 08:10\n"
            "j.park\tCompliance\tLOCKED\t2026-03-16 18:22\n\n"
            "3 of 4 users are locked. Likely related to last night's password "
            "policy GPO update. They need VPN to work remotely.\n\n"
            "{name}",
        ],
        next_best_actions=[
            "Investigate mass VPN account lockouts correlating with last night's "
            "password policy change — remote users cannot work.",
            "Unlock the affected accounts in Active Directory and review the "
            "password policy GPO change that likely caused the lockouts.",
        ],
        remediation_steps=[
            [
                "Unlock the affected accounts in Active Directory immediately",
                "Review the password policy GPO change from last night to determine "
                "if it invalidated existing credentials or changed lockout thresholds",
                "Check Azure AD sign-in logs for the locked accounts to confirm "
                "lockout was caused by repeated failed auth, not an attack",
                "Communicate to all remote users that they may need to update their cached credentials",
                "Consider phased rollout for future password policy changes with advance notice",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# dc-058  vCard data in email signature
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="dc-058",
        category=Category.HARDWARE,
        priority=Priority.P3,
        assigned_team=Team.ENDPOINT,
        needs_escalation=False,
        missing_information=[MissingInfo.DEVICE_INFO],
        subjects=[
            "Badge reader on {floor} not recognizing my card",
            "Access card not working on our floor — new badge issue",
            "Floor badge reader rejects my replacement card",
        ],
        descriptions=[
            "Hi,\n\n"
            "The badge reader on the main entrance to {floor}, Building 2 is not "
            "recognizing my access card. I tap it and the light stays red. My badge "
            "number is CF-2026-8841. Other people's badges work fine.\n\n"
            "I got a new badge two weeks ago because my old one cracked. The new "
            "one works on the ground floor and parking garage, just not {floor}.\n\n"
            "Best regards,\n\n"
            "BEGIN:VCARD\n"
            "VERSION:3.0\n"
            "N:{name};;\n"
            "FN:{name}\n"
            "ORG:Contoso Financial Services;{department}\n"
            "TITLE:Senior Analyst\n"
            "TEL;TYPE=WORK,VOICE:+1-212-555-0147\n"
            "TEL;TYPE=CELL:+1-917-555-0293\n"
            "ADR;TYPE=WORK:;;One Contoso Plaza;New York;NY;10001;USA\n"
            "EMAIL;TYPE=PREF:{name1}@contoso.com\n"
            "PHOTO;TYPE=JPEG;ENCODING=BASE64:/9j/4AAQSkZJRgABAQEASABIAAD/2wBDAAg\n"
            " GBgcGBQgHBwcJCQgKDBQNDAsLDBkSEw8UHRofHh0aHBwgJC4nICIsIxwcKDcpLDA\n"
            " xNDQ0Hyc5PTgyPC4zNDL/wAARCAAQABADASIAAhEB\n"
            "NOTE:Bloomberg ID available upon request\n"
            "REV:20260301T120000Z\n"
            "END:VCARD\n\n"
            "CONFIDENTIALITY NOTICE: This email and any attachments are for the "
            "exclusive and confidential use of the intended recipient.",
            "My replacement badge doesn't work on {floor}. It scans fine at the "
            "lobby and parking garage but the {floor} reader shows a red light.\n\n"
            "BEGIN:VCARD\n"
            "VERSION:3.0\n"
            "FN:{name}\n"
            "ORG:Contoso Financial;{department}\n"
            "TEL:+1-212-555-0200\n"
            "EMAIL:{name1}@contoso.com\n"
            "END:VCARD\n\n"
            "Badge number: CF-2026-9912. Please update the floor access.\n\n"
            "{name}",
        ],
        next_best_actions=[
            "Investigate access card not recognized by the floor badge reader — "
            "card works on ground floor and parking but not on the user's floor. "
            "Likely a provisioning issue with the replacement card's floor permissions.",
        ],
        remediation_steps=[
            [
                "Check the physical access control system to verify the badge has the correct floor access permissions",
                "Compare the new badge's access group assignments with the old badge "
                "to identify missing floor-level permissions",
                "Add the missing floor access to the new badge",
                "Test the badge on the floor reader after updating permissions",
                "Audit the badge replacement workflow to ensure floor permissions are "
                "copied from old badges to replacements",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# dc-059  Cron job / Task Scheduler output dump
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="dc-059",
        category=Category.DATA,
        priority=Priority.P2,
        assigned_team=Team.DATA_PLATFORM,
        needs_escalation=False,
        missing_information=[MissingInfo.ENVIRONMENT_DETAILS, MissingInfo.CONFIGURATION_DETAILS],
        subjects=[
            "FW: Cron job failures on PROD-RPT-01 — overnight batch report",
            "Batch reporting server failing — cron output attached",
            "Nightly report generation broken for 3 days — full job log inside",
        ],
        descriptions=[
            "IT team — forwarding the output from our overnight batch reporting "
            "server. Reports haven't been generated since Saturday.\n\n"
            "CRON JOB EXECUTION LOG — PROD-RPT-01\n"
            "======================================\n"
            "Host: PROD-RPT-01.contoso.local\n"
            "Run date: 2026-03-17 02:00:00 EST\n"
            "Job: /opt/contoso/reports/generate_daily_reports.sh\n"
            "Schedule: 0 2 * * * (daily at 02:00)\n"
            "User: svc_reports\n"
            "PID: 28451\n\n"
            "[02:00:01] Starting daily report generation...\n"
            "[02:00:01] Connecting to PROD-SQL-03.contoso.local:1433...\n"
            "[02:00:02] Connection established.\n"
            "[02:00:03] Executing: P&L Daily Summary (RPT-001)...\n"
            "[02:00:04] Rows returned: 1,247. PDF generated (2.3 MB). Uploaded to SharePoint.\n"
            "[02:00:06] Executing: Risk Exposure Summary (RPT-002)...\n"
            "[02:00:06] EXEC dbo.sp_RiskExposure @date='2026-03-16'\n"
            "[02:00:06] ERROR: Execution Timeout Expired.\n"
            "[02:00:06] SQL State: HYT00, Native Error: 0\n"
            "[02:00:06] Connection to PROD-SQL-03 lost.\n"
            "[02:00:07] Reconnection attempt 1/3 failed.\n"
            "[02:00:37] Reconnection attempt 2/3 failed.\n"
            "[02:01:07] Reconnection attempt 3/3 failed.\n"
            "[02:01:37] FATAL: All reconnection attempts exhausted.\n"
            "[02:01:37] Reports NOT generated: RPT-002, RPT-003, RPT-004, RPT-005\n"
            "[02:01:37] Exit code: 1\n\n"
            "Same failure repeated on 2026-03-15 and 2026-03-16 logs. The first "
            "report always succeeds but sp_RiskExposure kills the connection. "
            "We need these reports for the morning risk committee at 8 AM.\n\n"
            "{name}\n{department}",
            "Hi team,\n\n"
            "Our nightly batch job on PROD-RPT-02 has been failing:\n\n"
            "Task Scheduler Log:\n"
            "Task: \\Contoso\\Reports\\DailyGeneration\n"
            "Last Run: 2026-03-17 02:00:00 — Result: 0x1 (Failed)\n"
            "Previous: 2026-03-16 02:00:00 — Result: 0x1 (Failed)\n"
            "Previous: 2026-03-15 02:00:00 — Result: 0x0 (Success)\n\n"
            "The job connects to the SQL server but the stored procedure times "
            "out after 30 seconds. We need the daily {department} reports.\n\n"
            "{name}",
        ],
        next_best_actions=[
            "Investigate stored procedure timeout on the production SQL server "
            "causing overnight batch report failures for multiple consecutive "
            "nights — downstream reports not being generated.",
            "Fix the stored procedure timeout on PROD-SQL that is blocking "
            "nightly report generation — likely needs index tuning or statistics "
            "updates after recent data growth.",
        ],
        remediation_steps=[
            [
                "Check the production SQL server for long-running queries, blocking "
                "sessions, or resource exhaustion around the 02:00 AM window",
                "Review the execution plan for the failing stored procedure — it may "
                "need index tuning or statistics updates",
                "Check if a lock conflict with another overnight process is causing the timeout",
                "Increase the command timeout as a temporary measure while the stored procedure is optimized",
                "Manually trigger report generation for the missed dates once the issue is resolved",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# dc-060  Multiple concatenated ticket descriptions
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="dc-060",
        category=Category.SOFTWARE,
        priority=Priority.P2,
        assigned_team=Team.ENTERPRISE_APPS,
        needs_escalation=False,
        missing_information=[
            MissingInfo.AFFECTED_SYSTEM,
            MissingInfo.AFFECTED_USERS,
            MissingInfo.BUSINESS_IMPACT,
        ],
        subjects=[
            "FW: FW: FW: Batch of issues from London office — please triage",
            "Multiple issues from {department} — dumping into one ticket",
            "Forwarding batch of problems from our floor — please split",
        ],
        descriptions=[
            "Hi team,\n\n"
            "Our London office manager forwarded a batch of issues collected at "
            "this morning's all-hands. I'm dumping them all into one ticket "
            "because our portal was down earlier.\n\n"
            "=== ISSUE 1 (from Tom Bradley, Settlements) ===\n"
            "The settlement reconciliation app crashes every time I try to "
            "export to CSV. Error: 'System.OutOfMemoryException'. Machine: LDN-WS-1147.\n\n"
            "=== ISSUE 2 (from Amara Osei, Client Services) ===\n"
            "WiFi in the London office 3rd floor conference rooms A, B, C "
            "has been extremely slow since the new partitions were installed. "
            "Video calls keep freezing.\n\n"
            "=== ISSUE 3 (from Liam McDonnell, Compliance) ===\n"
            "I need access to the GDPR Data Subject Request portal. I "
            "transferred from Dublin last month and my access didn't follow.\n\n"
            "=== ISSUE 4 (from Yuki Sato, Quantitative Analysis) ===\n"
            "Our Bloomberg Terminal (BT-LDN-0093) shows 'Connection to B-PIPE "
            "lost' intermittently — data feed drops for 30-60 seconds hourly.\n\n"
            "=== ISSUE 5 (from Grace Nkomo, HR) ===\n"
            "The HR shared mailbox is bouncing emails with 'Mailbox full' — "
            "49.8 GB of 50 GB limit.\n\n"
            "Sorry for the messy format.\n\n"
            "{name}\n{department}",
            "Hi IT, forwarding a batch of problems from our {department} team:\n\n"
            "--- Issue A ---\n"
            "Shared drive access denied for {name1}. Worked until last Friday.\n\n"
            "--- Issue B ---\n"
            "VPN drops every 30 minutes for 3 people on our team.\n\n"
            "--- Issue C ---\n"
            "Outlook keeps crashing when opening attachments > 5 MB.\n\n"
            "--- Issue D ---\n"
            "We need a new team distribution list created: "
            "{department}-all@contoso.com.\n\n"
            "I know this should be separate tickets but our portal was down "
            "so I'm batching them here. Please split as needed.\n\n"
            "{name}",
        ],
        next_best_actions=[
            "This ticket contains multiple separate issues bundled into one "
            "submission. Split into individual tickets and triage each with "
            "the appropriate team.",
            "Split the concatenated ticket into individual issues — prioritize the highest-impact items first.",
        ],
        remediation_steps=[
            [
                "Create separate tickets for each reported issue and assign to the appropriate teams",
                "Prioritize the items that directly impact business operations "
                "(app crashes, data feed drops, mailbox full)",
                "For the settlement app crash, investigate the OutOfMemoryException in the CSV export code path",
                "For WiFi issues, coordinate with Network Ops to assess coverage "
                "changes after the partition installation",
                "For the mailbox quota, increase the limit or implement an auto-archive policy",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# dc-061  Very long email with buried issue
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="dc-061",
        category=Category.SOFTWARE,
        priority=Priority.P3,
        assigned_team=Team.ENTERPRISE_APPS,
        needs_escalation=False,
        missing_information=[MissingInfo.ERROR_MESSAGE, MissingInfo.STEPS_TO_REPRODUCE],
        subjects=[
            "Various things — also my {app} is broken",
            "Quick note + question + issue + follow-up on lunch order",
            "RE: Team outing — oh and my laptop has an issue too",
        ],
        descriptions=[
            "Hi IT,\n\n"
            "Hope you're all doing well! I wanted to first say thanks for fixing the "
            "printer last week — that was super quick. Also, did anyone figure out the "
            "lunch order for the {department} team outing next Friday? I think we said "
            "Mediterranean but some people wanted sushi. Anyway, totally unrelated, but "
            "I was chatting with {name1} about the new onboarding flow and we both agree "
            "the new portal looks great. Oh, and I forgot to mention — I ran into {name1} "
            "at the coffee machine and they said the {office} office is getting renovated? "
            "That's exciting.\n\n"
            "Also, I've been meaning to ask about the parking situation. My badge doesn't "
            "open the gate to Lot B anymore. Not sure if that's related to the system "
            "change last month. Speaking of which, is the old VPN client being retired? "
            "I saw an email but I wasn't sure if it applied to our department.\n\n"
            "OH WAIT — the actual reason I'm writing. My {app} has been crashing every "
            "time I try to open the quarterly {department} report. It freezes for about "
            "10 seconds and then just closes. This started on Monday. I've tried "
            "restarting my laptop and it didn't help. I'm on {os}.\n\n"
            "Also, is there cake in the break room? Someone said there was cake.\n\n"
            "Thanks!\n{name}",
            "Hey team,\n\n"
            "So I have a bunch of things to share and I figured I'd just put them all "
            "in one email rather than sending five separate ones.\n\n"
            "First, the holiday schedule — did we finalize whether the office is closed "
            "the week between Christmas and New Year? I need to book flights.\n\n"
            "Second, the coffee machine on Floor {floor} is making a weird noise again. "
            "I know that's not IT but I don't know who else to tell.\n\n"
            "Third, I lost my badge last week and got a replacement, but now my old badge "
            "shows as active too. Security concern maybe?\n\n"
            "Fourth — and this is the real issue — {app} crashes immediately when I try "
            "to generate the monthly compliance report. No error message, it just "
            "disappears. This is blocking my end-of-month deliverables. I'm running "
            "version {version} on {os}. It worked fine until the last update.\n\n"
            "Fifth, does anyone have a spare USB-C dongle?\n\n"
            "Cheers,\n{name}\n{department}",
        ],
        next_best_actions=[
            "Investigate {app} crash when opening large reports — the actual issue is "
            "buried in a rambling email. Ignore unrelated topics (lunch orders, parking, "
            "coffee machines).",
            "Troubleshoot {app} crash on report generation — user reports the app closes "
            "without an error after a recent update.",
        ],
        remediation_steps=[
            [
                "Extract the core issue from the rambling email: {app} crashes on report generation",
                "Check for recent updates to {app} that may have introduced a regression",
                "Collect crash logs or application event logs from the user's machine",
                "Test generating the same report on a different machine to isolate the issue",
                "If a recent update is the cause, roll back or apply the latest patch",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# dc-062  Massive base64 PDF inline (compliance scanner output)
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="dc-062",
        category=Category.SECURITY,
        priority=Priority.P2,
        assigned_team=Team.SECOPS,
        needs_escalation=False,
        missing_information=[MissingInfo.AFFECTED_SYSTEM, MissingInfo.ENVIRONMENT_DETAILS],
        subjects=[
            "Compliance scan results — see attached inline data",
            "Nessus scan output for {department} servers — URGENT findings",
            "Quarterly vulnerability scan — inline PDF export",
        ],
        descriptions=[
            "Hi Security team,\n\n"
            "Here are the results from last night's compliance scan. Our export tool is "
            "down so I'm pasting the base64-encoded PDF inline.\n\n"
            "--- BEGIN COMPLIANCE REPORT PDF (base64) ---\n"
            "JVBERi0xLjcKCjEgMCBvYmoKPDwKL1R5cGUgL0NhdGFsb2cKL1BhZ2VzIDIg"
            "MCBSCJ4+CmVuZG9iagoKMiAwIG9iago8PAovVHlwZSAvUGFnZXMKL0tpZHMg"
            "WzMgMCBSXQovQ291bnQgMQo+PgplbmRvYmoKCjMgMCBvYmoKPDwKL1R5cGUg"
            "L1BhZ2UKL1BhcmVudCAyIDAgUgovTWVkaWFCb3ggWzAgMCA2MTIgNzkyXQov"
            "Q29udGVudHMgNCAwIFIKL1Jlc291cmNlcyA8PAovRm9udCA8PAovRjEgNSAw"
            "IFIKPj4KPj4KPj4KZW5kb2JqCgo0IDAgb2JqCjw8Ci9MZW5ndGggNDQKPj4K"
            "c3RyZWFtCkJUCi9GMSAxMiBUZgo1MCA3MDAgVGQKKENvbXBsaWFuY2UgU2Nh"
            "biBSZXBvcnQpIFRqCkVUCmVuZHN0cmVhbQplbmRvYmoK\n"
            "[... approximately 847 more lines of base64 data omitted for brevity ...]\n"
            "--- END COMPLIANCE REPORT PDF ---\n\n"
            "Summary of critical findings:\n"
            "- 3 servers with unpatched CVEs rated CRITICAL\n"
            "- 7 endpoints missing disk encryption\n"
            "- 2 service accounts with passwords last rotated 400+ days ago\n\n"
            "Please review and advise on remediation priority.\n\n"
            "{name}\n{department}",
            "Attaching the Nessus vulnerability scan export for the {department} "
            "environment. The file upload was rejected (>25 MB) so I've base64-encoded "
            "the PDF and pasted it below.\n\n"
            "BEGIN BASE64 ENCODED SCAN REPORT:\n"
            "JVBERi0xLjQKMSAwIG9iago8PCAvVHlwZSAvQ2F0YWxvZyAvUGFnZXMgMiAw"
            "IFIgPj4KZW5kb2JqCjIgMCBvYmoKPDwgL1R5cGUgL1BhZ2VzIC9LaWRzIFsz"
            "IDAgUl0gL0NvdW50IDEgPj4KZW5kb2JqCjMgMCBvYmoKPDwgL1R5cGUgL1Bh"
            "Z2UgL1BhcmVudCAyIDAgUiAvTWVkaWFCb3ggWzAgMCA2MTIgNzkyXSA+Pgpl"
            "bmRvYmoKeHJlZgowIDQKMDAwMDAwMDAwMCA2NTUzNSBmIAowMDAwMDAwMDA5"
            "IDAwMDAwMDAwIG4gCjAwMDAwMDAwNTggMDAwMDAwMDAgbiAKMDAwMDAwMDEx"
            "NSAwMDAwMDAwMCBuIAp0cmFpbGVyCjw8IC9TaXplIDQgL1Jvb3QgMSAwIFIg"
            "Pj4Kc3RhcnR4cmVmCjIxNAolJUVPRgo=\n"
            "[... 1200+ additional lines of base64 omitted ...]\n"
            "END BASE64\n\n"
            "Key findings: 12 critical vulnerabilities, 34 high, 89 medium across "
            "47 scanned hosts. Need remediation plan by EOW.\n\n"
            "{name}, {department}",
        ],
        next_best_actions=[
            "Review the compliance scan summary findings — ignore the inline base64 "
            "data and focus on the critical vulnerabilities listed in the plain-text "
            "summary section.",
            "Prioritize remediation for the critical Nessus findings — request the "
            "report as a proper attachment or shared drive link instead of inline base64.",
        ],
        remediation_steps=[
            [
                "Request the full scan report as a proper file attachment or shared drive link",
                "Prioritize the critical CVE findings — identify which servers are affected",
                "Address the unrotated service account passwords immediately (400+ days is a policy violation)",
                "Schedule emergency patching for the servers with critical unpatched CVEs",
                "Create a remediation tracker and assign owners for each finding category",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# dc-063  Mobile autocorrect mangling technical terms
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="dc-063",
        category=Category.NETWORK,
        priority=Priority.P2,
        assigned_team=Team.NETWORK,
        needs_escalation=False,
        missing_information=[MissingInfo.ERROR_MESSAGE, MissingInfo.DEVICE_INFO],
        subjects=[
            "VPN keeps disconnecting plz help",
            "Cant connect to the network URGENT",
            "Wifi issues — sending from my phone sorry for typos",
        ],
        descriptions=[
            "hey sorry typing this from my phone bc my laptop wont connect\n\n"
            'so the VPN keeps saying "authentication failed" but my password is '
            "defintely right. i tried the global protect client and also the "
            'cisco anyconnect one. the error says something about a "certificate '
            'validation" but autocorrect keeps changing it lol\n\n'
            "my laptops ethernet port isnt working either — i think the docking "
            'station died. model is a "dell latitudes" (thats what autocorrect '
            "wants to call it 🙄) — its actually a Dell Latitude 5540.\n\n"
            "im on floor {floor} of the {office} office. been trying since 8am. "
            "my manager {name1} needs me online for a client call at 10.\n\n"
            'also tried the "alternate DNS" thing someone told me about but i '
            "think i typed the address wrong bc now nothing works at all. i "
            "changed it to 8.8.8.8 but maybe i shouldnt have??\n\n"
            "pls help asap 🙏\n\n"
            "{name}\nSent from my iPhone",
            "sry for the typos on mobile rn\n\n"
            "the wifi keeps dropping every few mins. when it does work its super "
            'slow like 2-3 mbps. im usually on the "contoso-corp" ssid but my '
            'phone keeps autoconnecting to "contoso-guest" instead\n\n'
            "i tried forgetting the network and reconnecting but it asks for a "
            '"certificate" that i dont have?? IT setup this laptop last month '
            "and wifi worked fine until today\n\n"
            'also the "global protect" vpn (autocorrect wants to call it '
            '"global protect agency" lmao) wont connect at all. just spins '
            'and says "gateway not found"\n\n'
            "im in bldg 3 floor {floor}, the {office} office. need this fixed "
            "before my 2pm presentation plsss\n\n"
            "{name} — {department}\nSent from mobile",
        ],
        next_best_actions=[
            "Troubleshoot VPN and network connectivity for user on Floor {floor} "
            "— parse through mobile autocorrect artifacts to identify the certificate "
            "validation error and potential DNS misconfiguration.",
            "Investigate wireless connectivity issues — user's laptop may have a "
            "certificate or profile problem preventing connection to the corporate SSID.",
        ],
        remediation_steps=[
            [
                "Verify the user's VPN certificate is valid and not expired",
                "Check if the user manually changed DNS settings and revert to DHCP-assigned DNS",
                "Re-push the corporate wireless profile to ensure proper SSID and certificate configuration",
                "Test the docking station Ethernet port — replace if faulty",
                "Confirm VPN gateway is reachable from the user's network segment",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# dc-064  Auto-translated email with translation artifacts
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="dc-064",
        category=Category.SOFTWARE,
        priority=Priority.P2,
        assigned_team=Team.ENTERPRISE_APPS,
        needs_escalation=False,
        missing_information=[MissingInfo.ERROR_MESSAGE, MissingInfo.APPLICATION_VERSION],
        subjects=[
            "The program of accounting does not function — translated by Google",
            "Application of enterprise makes error — please excuse translation",
            "Financial system is doing the crash — auto-translated from Japanese",
        ],
        descriptions=[
            "[This message was auto-translated from Japanese by Microsoft Translator]\n\n"
            "Respectful IT team of support,\n\n"
            "The program of accounting (SAP Concur) is making the error when I am "
            "trying to submit the report of expenses. When I am pushing the button "
            "of 'submit', the screen becomes the white color and the circle of loading "
            "is turning forever without stopping.\n\n"
            "I have already made the attempt of:\n"
            "- Making the cache of browser to be cleared\n"
            "- Using the browser of different type (the Chrome of Google and the Edge "
            "of Microsoft)\n"
            "- Making the computer to restart\n\n"
            "The report of expenses has the value of ¥847,000 and must be submitted "
            "before the deadline of end of month. My department of {department} has "
            "the policy of strict deadline.\n\n"
            "元のメッセージ: 経費精算システムが送信ボタンを押すと固まります。\n"
            "至急対応をお願いします。\n\n"
            "With respectful regards,\n{name}\n{department} — {office} Office",
            "[Auto-translated from Korean — original below]\n\n"
            "Hello the team of IT,\n\n"
            "The application of {app} is making crash when I am opening the file of "
            "large size. The message of error says 'the memory is not sufficient' but "
            "my computer of laptop has the RAM of 32 gigabytes.\n\n"
            "This problem started after the update of automatic that happened in the "
            "night of last Tuesday. Before the update, everything was working with "
            "the normality.\n\n"
            "The file I am trying to open has the size of approximately 2 gigabytes. "
            "It is the data of financial modeling for the quarter of Q3.\n\n"
            "원본 메시지: {app}에서 대용량 파일을 열 때 크래시가 발생합니다. "
            "메모리 부족 오류가 나옵니다.\n\n"
            "{name}\n{department}",
        ],
        next_best_actions=[
            "Investigate SAP Concur submission failure — the user reports the page "
            "hangs on submit. Look past the machine-translation artifacts to identify "
            "the core issue.",
            "Troubleshoot {app} crash on large file open — reported after a recent "
            "automatic update. The memory error may indicate a regression in the update.",
        ],
        remediation_steps=[
            [
                "Reproduce the issue in the same application version and browser combination",
                "Check for known issues with the latest application update",
                "Verify server-side logs for errors during the submission or file open operation",
                "If the update introduced a regression, coordinate with the vendor for a hotfix",
                "Follow up with the user in their preferred language if possible",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# dc-065  Extremely terse ticket with minimal context
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="dc-065",
        category=Category.SOFTWARE,
        priority=Priority.P3,
        assigned_team=Team.ENTERPRISE_APPS,
        needs_escalation=False,
        missing_information=[
            MissingInfo.ERROR_MESSAGE,
            MissingInfo.AFFECTED_SYSTEM,
            MissingInfo.STEPS_TO_REPRODUCE,
            MissingInfo.DEVICE_INFO,
            MissingInfo.ENVIRONMENT_DETAILS,
        ],
        subjects=[
            "broken",
            "not working",
            "help",
        ],
        descriptions=[
            "it's broken again",
            "doesn't work. fix pls",
            "{app} down",
        ],
        next_best_actions=[
            "Gather basic information from the reporter — the ticket provides almost "
            "no context. Ask for the application name, error messages, what they were "
            "trying to do, and when it started.",
            "Request clarification — ticket is too vague to triage. Need affected "
            "system, error details, and steps to reproduce.",
        ],
        remediation_steps=[
            [
                "Contact the reporter to collect basic information: what application, "
                "what error, what were they trying to do",
                "Ask for screenshots or screen recordings if the user cannot articulate the issue",
                "Check for any ongoing incidents or outages that may match the vague report",
                "Once sufficient information is gathered, re-triage with the correct category and priority",
                "Update the ticket with the clarified details for proper tracking",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# dc-066  MIME multipart boundary markers visible in plaintext email
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="dc-066",
        category=Category.SOFTWARE,
        priority=Priority.P3,
        assigned_team=Team.ENTERPRISE_APPS,
        needs_escalation=False,
        missing_information=[MissingInfo.DEVICE_INFO, MissingInfo.APPLICATION_VERSION],
        subjects=[
            "Outlook rendering issue — raw MIME in message body",
            "Email displays garbled MIME headers instead of content",
            "Strange boundary markers showing in received emails",
        ],
        descriptions=[
            "Hi IT,\n\n"
            "Since the latest Outlook update, some emails I receive display raw MIME "
            "data instead of the message body. Here is what I see:\n\n"
            "------=_Part_12345_987654321.1711012800000\n"
            "Content-Type: text/plain; charset=UTF-8\n"
            "Content-Transfer-Encoding: quoted-printable\n\n"
            "The actual message body that should be rendered:\n"
            "Hi team, the monthly finance report for Q1 is attached. Please review.\n\n"
            "------=_Part_12345_987654321.1711012800000\n"
            "Content-Type: text/html; charset=UTF-8\n"
            "Content-Transfer-Encoding: base64\n\n"
            "PGh0bWw+PGJvZHk+PHA+SGkgdGVhbSwgdGhlIG1vbnRobHkgZmluYW5jZQ==\n\n"
            "------=_Part_12345_987654321.1711012800000--\n\n"
            "This is happening on about half the emails from external senders. Internal "
            "emails render fine. I'm on {os} using Outlook desktop. Please help.",
            "Getting raw MIME boundaries in my emails. Example below:\n\n"
            "MIME-Version: 1.0\n"
            "Content-Type: multipart/alternative;\n"
            '    boundary="----=_NextPart_001_0078_01DA4F2B.A7C3E680"\n\n'
            "This is a multi-part message in MIME format.\n\n"
            "------=_NextPart_001_0078_01DA4F2B.A7C3E680\n"
            'Content-Type: text/plain; charset="utf-8"\n'
            "Content-Transfer-Encoding: 7bit\n\n"
            "Can someone from IT look at this? The emails from our clients at the "
            "{office} office are arriving like this since Thursday. It's affecting "
            "the entire {department} team on Floor {floor}.",
        ],
        next_best_actions=[
            "Investigate Outlook MIME rendering regression — likely caused by recent "
            "update breaking multipart/alternative parsing for external emails.",
            "Check for known issues with the latest Outlook update affecting MIME "
            "rendering. Test with OWA to isolate desktop client vs. server issue.",
        ],
        remediation_steps=[
            [
                "Verify the Outlook version and check for known MIME rendering bugs in that build",
                "Test the same emails in Outlook Web Access (OWA) to isolate client-side issue",
                "Clear the Outlook cache and repair the Office installation",
                "If the issue is build-specific, roll back to the previous Outlook version",
                "Escalate to Microsoft support if the issue is confirmed as a product bug",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# dc-067  Base64-encoded PDF report pasted inline
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="dc-067",
        category=Category.DATA,
        priority=Priority.P2,
        assigned_team=Team.DATA_PLATFORM,
        needs_escalation=False,
        missing_information=[MissingInfo.ERROR_MESSAGE, MissingInfo.STEPS_TO_REPRODUCE],
        subjects=[
            "Report generation failed — attaching PDF data",
            "Nightly financial report pipeline broken — see report data below",
            "Q1 report output corrupted — pasting raw output",
        ],
        descriptions=[
            "The nightly financial report pipeline in {department} failed again last night. "
            "I'm pasting the last successful PDF output below so you can compare. The pipeline "
            "used to produce this correctly:\n\n"
            "JVBERi0xLjQKMSAwIG9iago8PCAvVHlwZSAvQ2F0YWxvZyAvUGFnZXMgMiAwIFIgPj4KZW5k"
            "b2JqCjIgMCBvYmoKPDwgL1R5cGUgL1BhZ2VzIC9LaWRzIFszIDAgUl0gL0NvdW50IDEgPj4K"
            "ZW5kb2JqCjMgMCBvYmoKPDwgL1R5cGUgL1BhZ2UgL1BhcmVudCAyIDAgUiAvTWVkaWFCb3gg"
            "WzAgMCA2MTIgNzkyXSAvQ29udGVudHMgNCAwIFIgL1Jlc291cmNlcyA8PCAvRm9udCA8PCAv"
            "RjEgNSAwIFIgPj4gPj4gPj4KZW5kb2JqCjQgMCBvYmoKPDwgL0xlbmd0aCA0NCA+PgpzdHJl"
            "YW0KQlQKL0YxIDE4IFRmCjEwMCA3MDAgVGQKKFExIEZpbmFuY2lhbCBSZXBvcnQpIFRqCkVU"
            "CmVuZHN0cmVhbQplbmRvYmoKNSAwIG9iago8PCAvVHlwZSAvRm9udCAvU3VidHlwZSAvVHlw"
            "ZTEgL0Jhc2VGb250IC9IZWx2ZXRpY2EgPj4KZW5kb2JqCnhyZWYKMCA2CjAwMDAwMDAwMDY="
            "\n\n"
            "Now the pipeline throws an error at the PDF rendering stage. It runs on Azure "
            "Data Factory and calls a Databricks notebook. The job ID is ADF-RPT-{number}.\n\n"
            "Please investigate — the {department} team needs this report by 8 AM daily.",
            "Report generation for the {department} daily risk summary has been failing since "
            "{date}. I exported the last good output as base64:\n\n"
            "data:application/pdf;base64,JVBERi0xLjUKJeLjz9MKMSAwIG9iago8PCAvVHlwZSAvQ2F0"
            "YWxvZyAvUGFnZXMgMiAwIFIgL01hcmtJbmZvIDw8IC9NYXJrZWQgdHJ1ZSA+PiA+PgplbmRv"
            "YmoKMiAwIG9iago8PCAvVHlwZSAvUGFnZXMgL0tpZHMgWzMgMCBSXSAvQ291bnQgMSA+Pgpl"
            "bmRvYmoKMyAwIG9iago8PCAvVHlwZSAvUGFnZSAvUGFyZW50IDIgMCBSIC9NZWRpYUJveCBb"
            "MCAwIDYxMiA3OTJdIC9Db250ZW50cyA0IDAgUiA+PgplbmRvYmoKeHJlZgowIDUKMDAwMMDY="
            "\n\n"
            "The current error message in ADF is 'Notebook execution failed: OutOfMemoryError'. "
            "The Databricks cluster might need resizing — the dataset grew significantly this quarter.",
        ],
        next_best_actions=[
            "Investigate ADF pipeline failure at the PDF rendering stage — likely "
            "OutOfMemoryError on Databricks. Ignore the base64 PDF dump in the ticket.",
            "Check Databricks cluster sizing for the report generation notebook and "
            "review memory allocation against the growing dataset size.",
        ],
        remediation_steps=[
            [
                "Check the ADF pipeline run logs for the specific failure point",
                "Review the Databricks notebook memory requirements against cluster sizing",
                "Increase the Databricks cluster driver and worker memory if needed",
                "Verify the input dataset size hasn't exceeded expected thresholds",
                "Re-run the pipeline and monitor resource utilization during execution",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# dc-068  Multiple inline base64 images interspersed in text
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="dc-068",
        category=Category.NETWORK,
        priority=Priority.P2,
        assigned_team=Team.NETWORK,
        needs_escalation=False,
        missing_information=[MissingInfo.NETWORK_LOCATION, MissingInfo.DEVICE_INFO],
        subjects=[
            "Network outage on Floor {floor} — screenshots embedded",
            "Wi-Fi dead zone with proof images — please help",
            "Intermittent connectivity — pasting diagnostic screenshots",
        ],
        descriptions=[
            "I've been getting network drops all day. Here is the first screenshot "
            "showing the Wi-Fi signal strength:\n\n"
            "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAKCAYAAACNMs+9AAAA"
            "FklEQVQYV2P8z8BQz0AEYBxVOHIUAgBGWAkFdZLYSgAAAABJRU5ErkJggg==\n\n"
            "And this is the ping results showing 40% packet loss:\n\n"
            "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAEBAQEBAQEBAQEB"
            "AQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEB/2w"
            "BDAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEBAQEB"
            "AQEBAf/AABEIAB4AHgMBEQACEQEDEQH/FAKENETESTDATA\n\n"
            "The third screenshot shows the error message on our VPN client:\n\n"
            "data:image/gif;base64,R0lGODlhAQABAIAAAAAAAP///yH5BAEAAAAALAAAAAABAAEAAAI"
            "BRAkFDFAKETESTDATA\n\n"
            "I'm on Floor {floor} in the {office} office. The Wi-Fi SSID is CONTOSO-CORP. "
            "My laptop is connected to the docking station via USB-C. Other people on the "
            "floor are also complaining.",
            "Three screenshots showing network issues (I couldn't figure out how to attach "
            "them so they got pasted as data):\n\n"
            "[Screenshot 1 - traceroute]\n"
            "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABQAAAAUCAYAAACNiR0NAAAAB"
            "mJLR0QA/wD/AP+gvaeTAAAAQ0lEQVQ4y2P4FAKEFAKEDATAFORNETWORKTRACEROUTERESULTS"
            "SHOWING15HOPSWITHTIMEOUT/AABBCCDDEEFF0011223344556677ENDOFDATA==\n\n"
            "[Screenshot 2 - ipconfig]\n"
            "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEASABIAAD/2wBDABALDA4MChAODQ4S"
            "ERATGB4gHBcfICQiJCUUKSs0LSwsLSxNODoxNjc3NUpXUFBQV2JdYGBie3p7dHVudXJ7e3v"
            "FAKEIPCONFIGOUTPUTFORNETWORKADAPTER=\n\n"
            "[Screenshot 3 - Wi-Fi analyzer]\n"
            "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAAA"
            "FAKEWIFIANALYZERSHOWINGCHANNELOVERLAP1234567890ABCDEF==\n\n"
            "Please investigate — this is impacting about 15 people in {department} and "
            "we have client calls all afternoon.",
        ],
        next_best_actions=[
            "Investigate network connectivity issues on Floor {floor} — ignore the "
            "inline base64 image data and focus on the reported Wi-Fi packet loss "
            "and VPN errors.",
            "Check AP utilization and channel overlap on the floor — multiple users "
            "affected suggests infrastructure issue, not client-side.",
        ],
        remediation_steps=[
            [
                "Check the wireless controller for AP health and utilization on the affected floor",
                "Run an RF survey to identify channel congestion or dead zones",
                "Verify DHCP scope availability for the CONTOSO-CORP SSID on that floor",
                "Check for recent infrastructure changes (AP firmware, VLAN changes, cabling)",
                "If congestion confirmed, consider adding an AP or adjusting channel allocation",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# dc-069  ICS/vCalendar metadata mixed with support request
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="dc-069",
        category=Category.SOFTWARE,
        priority=Priority.P3,
        assigned_team=Team.ENTERPRISE_APPS,
        needs_escalation=False,
        missing_information=[MissingInfo.APPLICATION_VERSION, MissingInfo.DEVICE_INFO],
        subjects=[
            "Calendar invite broken — raw ICS data showing up",
            "FW: Meeting invite garbled — see calendar data below",
            "Outlook calendar sync failure with ICS artifacts",
        ],
        descriptions=[
            "When I try to accept meeting invites, Outlook shows raw calendar data "
            "instead of the normal meeting view. Here is what I see:\n\n"
            "BEGIN:VCALENDAR\n"
            "VERSION:2.0\n"
            "PRODID:-//Microsoft Corporation//Outlook 16.0 MIMEDIR//EN\n"
            "METHOD:REQUEST\n"
            "BEGIN:VEVENT\n"
            "DTSTART:20260415T140000Z\n"
            "DTEND:20260415T150000Z\n"
            "RRULE:FREQ=WEEKLY;BYDAY=WE;COUNT=10\n"
            "ORGANIZER;CN={name}:mailto:{name1}@contoso.com\n"
            "ATTENDEE;ROLE=REQ-PARTICIPANT;RSVP=TRUE:mailto:{name2}@contoso.com\n"
            "ATTENDEE;ROLE=OPT-PARTICIPANT:mailto:{name3}@contoso.com\n"
            "LOCATION:Conference Room 4B, Floor {floor}\n"
            "SUMMARY:Weekly {department} Strategy Sync\n"
            "DESCRIPTION:Recurring strategy meeting for the {department} team.\n"
            "UID:040000008200E00074C5B7101A82E0080000000090C9A34C\n"
            "SEQUENCE:0\n"
            "STATUS:CONFIRMED\n"
            "END:VEVENT\n"
            "END:VCALENDAR\n\n"
            "I can't accept or decline the meeting. The calendar on my phone (iOS) "
            "works fine but the desktop client is broken.",
            "My Outlook calendar is showing raw ICS data for all new meeting invites. "
            "I forwarded one as an example — the entire invite renders as text:\n\n"
            "BEGIN:VCALENDAR\nVERSION:2.0\nPRODID:-//Exchange//EN\n"
            "BEGIN:VTIMEZONE\nTZID:Eastern Standard Time\n"
            "BEGIN:STANDARD\nDTSTART:16010101T020000\nRRULE:FREQ=YEARLY;BYDAY=1SU;BYMONTH=11\n"
            "TZOFFSETFROM:-0400\nTZOFFSETTO:-0500\nEND:STANDARD\nEND:VTIMEZONE\n"
            "BEGIN:VEVENT\nDTSTART;TZID=Eastern Standard Time:20260420T093000\n"
            "DTEND;TZID=Eastern Standard Time:20260420T103000\n"
            "SUMMARY:Q2 Planning - {department}\nEND:VEVENT\nEND:VCALENDAR\n\n"
            "This started after I migrated to the new laptop last week. The old laptop "
            "was fine. I'm on {os} with Outlook desktop.",
        ],
        next_best_actions=[
            "Investigate Outlook calendar rendering failure showing raw ICS data — "
            "likely a profile or add-in issue after laptop migration.",
            "Troubleshoot Outlook meeting invite rendering — check for corrupted "
            "calendar profile or conflicting COM add-ins.",
        ],
        remediation_steps=[
            [
                "Check for conflicting Outlook COM add-ins that may affect calendar rendering",
                "Repair the Outlook profile and recreate the OST file",
                "Verify the Outlook version matches the expected build for the organization",
                "Test calendar invite rendering in Outlook safe mode (no add-ins)",
                "If issue persists after profile repair, create a new Outlook profile",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# dc-070  Very long email with critical issue buried at the very end
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="dc-070",
        category=Category.SECURITY,
        priority=Priority.P1,
        assigned_team=Team.SECOPS,
        needs_escalation=True,
        missing_information=[MissingInfo.TIMESTAMP, MissingInfo.AFFECTED_SYSTEM],
        subjects=[
            "Quick question and also something weird with my account",
            "Various IT things — and a login alert I got",
            "Couple of issues plus a security notification",
        ],
        descriptions=[
            "Hi IT team,\n\n"
            "Hope you had a great weekend! I wanted to reach out because I have a few "
            "things on my mind. First, I should mention that the coffee machine on Floor "
            "{floor} has been acting up again — I know that's not really IT but maybe you "
            "know who to contact?\n\n"
            "Also, I was wondering if there's a way to change my desktop wallpaper. I know "
            "it sounds silly but the default one is really depressing and I read somewhere "
            "that a pleasant workspace improves productivity by 15%. My friend at another "
            "company says they can customize everything. I'm in {department} by the way.\n\n"
            "On another note entirely, I wanted to ask about the new {app} deployment. I "
            "heard from {name} in {department} that it's coming next month. Will there be "
            "training sessions? I'm not very technical and the last rollout was really "
            "confusing. The documentation was 47 pages long and nobody read it. Maybe this "
            "time we could have short video tutorials instead?\n\n"
            "Oh and the printer on Floor {floor} — is that still under maintenance? I "
            "haven't been able to print for three days but I just assumed it was planned. "
            "Actually, now that I think about it, my colleague {name} said the printer "
            "worked fine for her yesterday, so maybe it's just my laptop? I don't know.\n\n"
            "Speaking of my laptop, it's been running a bit slow lately. I think I have "
            "too many Chrome tabs open. How much RAM does my laptop have? Is there a way "
            "to check? I tried looking in Settings but I got confused.\n\n"
            "One more thing — I got an email notification from the security team about a "
            "sign-in to my account from an IP address in a country I've never been to. "
            "It showed a successful login from Russia at 3 AM this morning.",
            "Hey team!\n\n"
            "First off, I just wanted to say you all do amazing work. The way you handled "
            "the Teams outage last month was impressive. Anyway, I have a bunch of things:\n\n"
            "1. The {browser} browser keeps asking me to update but the button doesn't "
            "work. It just spins forever. Not urgent at all, just annoying.\n\n"
            "2. I need to set up a shared mailbox for the new {department} project team. "
            "There are about 8 people who need access. I'll send you the list later.\n\n"
            "3. My headset (Jabra Evolve2 85) makes a weird crackling noise on Teams "
            "calls but works perfectly for music. Is it a driver issue? Firmware?\n\n"
            "4. The Wi-Fi in the {office} office cafeteria is really slow during lunch "
            "time. Can you add more access points? Everyone is on TikTok during break "
            "and it kills the bandwidth. Just kidding. Sort of.\n\n"
            "5. Almost forgot the important one — Microsoft Defender flagged my account "
            "for impossible travel. Someone logged in as me from an IP in China while I "
            "was sitting at my desk in {office}. The alert says it was a successful auth.",
        ],
        next_best_actions=[
            "URGENT: Investigate the security alert buried at the end — successful "
            "authentication from a foreign IP address suggests possible account compromise. "
            "Initiate incident response immediately.",
            "Prioritize the impossible travel alert — the user's account may be compromised. "
            "All other requests in this email are low-priority and should be handled separately.",
        ],
        remediation_steps=[
            [
                "Immediately reset the user's password and revoke all active sessions",
                "Review Entra ID sign-in logs for the flagged authentication event",
                "Check for any suspicious mailbox rules, forwarding, or data access during the session",
                "Enable additional conditional access policies (location-based, risk-based)",
                "Create separate tickets for the non-security requests mentioned in the email",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# dc-071  Multilingual legal disclaimers burying a short request
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="dc-071",
        category=Category.HARDWARE,
        priority=Priority.P3,
        assigned_team=Team.ENDPOINT,
        needs_escalation=False,
        missing_information=[MissingInfo.DEVICE_INFO],
        subjects=[
            "Keyboard not working",
            "Laptop keyboard — several keys unresponsive",
            "Need keyboard replacement",
        ],
        descriptions=[
            "Hi, my laptop keyboard has stopped working — the T, Y, and U keys are "
            "completely dead. I need a replacement keyboard or a USB keyboard as a "
            "temporary workaround. I'm on Floor {floor}, {office} office.\n\n"
            "---\n\n"
            "CONFIDENTIALITY NOTICE: This email and any files transmitted with it are confidential and "
            "intended solely for the use of the individual or entity to whom they are addressed. If "
            "you have received this email in error, please notify the system manager.\n\n"
            "AVIS DE CONFIDENTIALITÉ : Ce courriel et les fichiers qui y sont joints sont "
            "confidentiels et destinés exclusivement à l'usage de la personne ou de l'entité "
            "à qui ils sont adressés. Si vous avez reçu ce courriel par erreur, veuillez en "
            "aviser l'administrateur du système.\n\n"
            "VERTRAULICHKEITSHINWEIS: Diese E-Mail und alle übertragenen Dateien sind vertraulich "
            "und ausschließlich für den Gebrauch der Person oder Organisation bestimmt, an die sie "
            "gerichtet sind. Wenn Sie diese E-Mail irrtümlich erhalten haben, benachrichtigen Sie "
            "bitte den Systemadministrator.\n\n"
            "AVISO DE CONFIDENCIALIDAD: Este correo electrónico y los archivos transmitidos son "
            "confidenciales y están destinados únicamente para el uso del individuo o entidad "
            "a quien están dirigidos.\n\n"
            "AVVISO DI RISERVATEZZA: Questa e-mail e tutti i file trasmessi sono riservati e "
            "destinati esclusivamente all'uso della persona o dell'ente a cui sono indirizzati.\n\n"
            "AVISO DE CONFIDENCIALIDADE: Este e-mail e os ficheiros transmitidos são confidenciais "
            "e destinam-se exclusivamente ao uso do indivíduo ou entidade a quem são dirigidos.\n\n"
            "機密通知：このメールおよび添付ファイルは機密情報であり、宛先の個人または "
            "団体のみを対象としています。誤って受信された場合は、システム管理者にお知らせください。\n\n"
            "保密声明：本邮件及其附件为保密信息，仅供收件人个人或实体使用。如您误收此邮件，请通知系统管理员。\n\n"
            "إشعار السرية: هذا البريد الإلكتروني وأي ملفات مرفقة به سرية ومخصصة حصرياً للاستخدام "
            "من قبل الفرد أو الجهة المرسل إليها.\n\n"
            "Contoso Financial Services | Registered in England & Wales | Company No. 12345678\n"
            "VAT Registration No. GB 123 4567 89 | FCA Authorised No. 123456\n"
            "This email has been scanned by Contoso Email Gateway v4.12.1.",
            "Three keys on my keyboard are dead (T, Y, U). Need a replacement ASAP — "
            "I'm working on the quarterly {department} report and can't type properly.\n\n"
            "------\n\n"
            "CONFIDENTIALITY: This message is intended only for the named recipient. "
            "If received in error, notify the sender and delete. "
            "CONFIDENTIALITÉ: Ce message est destiné uniquement au destinataire nommé. "
            "VERTRAULICHKEIT: Diese Nachricht ist nur für den genannten Empfänger bestimmt. "
            "CONFIDENCIALIDAD: Este mensaje está destinado solo al destinatario nombrado. "
            "RISERVATEZZA: Questo messaggio è destinato solo al destinatario indicato. "
            "CONFIDENCIALIDADE: Esta mensagem destina-se apenas ao destinatário indicado. "
            "機密事項：このメッセージは指定された受信者のみを対象としています。"
            "保密事项：此消息仅供指定收件人使用。"
            "السرية: هذه الرسالة مخصصة فقط للمستلم المحدد.\n\n"
            "Contoso Financial Services | 200 Park Avenue, New York, NY 10166 | "
            "+1 (212) 555-0199 | www.contoso.com\n"
            "♻ Please consider the environment before printing this email.",
        ],
        next_best_actions=[
            "Process the keyboard replacement request — ignore the extensive multilingual "
            "disclaimers. User needs a replacement for dead T/Y/U keys.",
            "Arrange a USB keyboard as temporary workaround and schedule a keyboard "
            "replacement for the user on Floor {floor}.",
        ],
        remediation_steps=[
            [
                "Dispatch a USB keyboard as a temporary workaround to the user's desk",
                "Create a hardware replacement request for the laptop keyboard",
                "Schedule an appointment with the endpoint team for keyboard swap",
                "Verify if the keyboard issue is hardware (physical damage) or software (driver)",
                "If warranty is active, initiate a manufacturer repair/replacement",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# dc-072  NDR (Non-Delivery Report) / bounce-back wrapping original request
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="dc-072",
        category=Category.NETWORK,
        priority=Priority.P2,
        assigned_team=Team.NETWORK,
        needs_escalation=False,
        missing_information=[MissingInfo.ERROR_MESSAGE, MissingInfo.AFFECTED_USERS],
        subjects=[
            "Undeliverable: RE: Urgent client report — email bouncing",
            "Mail delivery failed — returning message to sender",
            "FW: Delivery Status Notification (Failure)",
        ],
        descriptions=[
            "Hi team,\n\n"
            "Emails to external recipients are bouncing. I'm pasting the NDR I received:\n\n"
            "From: Microsoft Outlook <postmaster@contoso.com>\n"
            "Subject: Undeliverable: Urgent client report\n"
            "To: {name1}@contoso.com\n\n"
            "Delivery has failed to these recipients or groups:\n\n"
            "client.contact@externalfirm.com\n"
            "The email message could not be delivered because the recipient's email "
            "server refused the connection.\n\n"
            "Diagnostic information for administrators:\n"
            "Generating server: mail01.contoso.com\n"
            "Remote Server returned: '550 5.7.1 Unable to relay'\n\n"
            "Reporting-MTA: dns;mail01.contoso.com\n"
            "Received-From-MTA: dns;edge01.contoso.com\n"
            "Arrival-Date: {date} {time}\n\n"
            "Final-Recipient: rfc822;client.contact@externalfirm.com\n"
            "Action: failed\n"
            "Status: 5.7.1\n"
            "Remote-MTA: dns;mx1.externalfirm.com (192.0.2.50)\n"
            "Diagnostic-Code: smtp;550 5.7.1 Message rejected due to SPF check failure\n\n"
            "X-MS-Exchange-Organization-SCL: -1\n"
            "X-MS-Exchange-Organization-AuthSource: edge01.contoso.com\n"
            "X-MS-Exchange-Organization-AuthAs: Internal\n"
            "X-OriginatorOrg: contoso.com\n\n"
            "I need to send this client report by end of day. Other people in "
            "{department} are also reporting bounced emails to external addresses.",
            "Forwarding the bounce message I keep getting:\n\n"
            "This is an automatically generated Delivery Status Notification.\n"
            "Delivery to the following recipients failed:\n"
            "    partner@externalclient.com\n\n"
            "421 4.7.0 Try again later, closing connection. (TLS negotiation failed)\n\n"
            "Original-Envelope-Id: <{number}@mail01.contoso.com>\n"
            "Reporting-MTA: dns;mail01.contoso.com\n"
            "X-Mailer: Microsoft Exchange Server 2019\n"
            "Content-Type: message/delivery-status\n\n"
            "The emails to external clients have been failing since around {time} today. "
            "I'm in {department} and this is blocking critical client communications.",
        ],
        next_best_actions=[
            "Investigate outbound email delivery failure — NDR shows SPF check failure "
            "and TLS negotiation issues on the Edge transport server.",
            "Check Exchange Edge Transport and DNS/SPF records — multiple users in "
            "{department} cannot send to external recipients.",
        ],
        remediation_steps=[
            [
                "Verify SPF, DKIM, and DMARC DNS records for contoso.com are correct and published",
                "Check the Exchange Edge Transport server for TLS certificate expiration",
                "Review the mail flow connector configuration for outbound relay",
                "Test outbound SMTP connectivity from the mail server to external MX records",
                "If SPF records are misconfigured, update and allow 24-48h for DNS propagation",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# dc-073  Regex/code patterns in ticket text
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="dc-073",
        category=Category.SOFTWARE,
        priority=Priority.P3,
        assigned_team=Team.ENTERPRISE_APPS,
        needs_escalation=False,
        missing_information=[MissingInfo.APPLICATION_VERSION, MissingInfo.STEPS_TO_REPRODUCE],
        subjects=[
            "Search filter broken in internal tool — regex not matching",
            "Data validation pattern failing in {app} — special chars issue",
            "Code search broken — special characters not handled",
        ],
        descriptions=[
            "The search/filter feature in our internal {app} tool is broken. I'm trying "
            "to use these regex patterns to filter client records but they return no "
            "results:\n\n"
            "Pattern 1: ^[A-Z]{{2,3}}-\\d{{4,6}}$\n"
            "Pattern 2: (?:NYSE|NASDAQ)\\s*:\\s*[A-Z]{{1,5}}\n"
            "Pattern 3: \\b\\d{{1,3}}(?:,\\d{{3}})*(?:\\.\\d{{2}})?\\b\n"
            "Pattern 4: SELECT * FROM clients WHERE name LIKE '%O''Brien%' AND "
            "status IN ('active', 'pending');\n\n"
            "These patterns used to work last week. I suspect the latest update changed "
            "the regex engine or escaping rules. The data validation also fails on inputs "
            "containing: [brackets], (parens), {{}}, pipes|pipes, asterisks*, "
            "backslashes\\, and caret^ characters.\n\n"
            "I'm in {department} and this is blocking our daily client reconciliation.",
            "Hi IT,\n\n"
            "The search function in {app} is silently failing on queries with special "
            "characters. Examples that don't work:\n\n"
            "- `.*@contoso\\.com$` (regex to find internal emails)\n"
            "- `price >= 100.00 AND price <= 999.99` (filter expression)\n"
            "- `(dept='Finance' OR dept='Trading') AND active=1`\n"
            "- `C:\\\\Users\\\\{name}\\\\Documents\\\\report_v2.xlsx` (file path)\n\n"
            "The error in the browser console is: 'SyntaxError: Invalid regular "
            "expression: /[unterminated character class/'. It seems like user input "
            "is being passed to a regex engine without proper escaping.",
        ],
        next_best_actions=[
            "Investigate {app} search filter regression — user input with special "
            "regex characters is causing SyntaxError. Likely a missing input "
            "sanitization step in the latest update.",
            "Check the latest {app} update for changes to the search/filter input "
            "handling — regex metacharacters need proper escaping before evaluation.",
        ],
        remediation_steps=[
            [
                "Reproduce the issue with the provided regex patterns in a test environment",
                "Check the {app} release notes for search/filter engine changes",
                "Verify that user input is properly escaped before being passed to the regex engine",
                "If the regression is confirmed, coordinate with the vendor for a hotfix",
                "As a workaround, advise users to use the basic search (non-regex) mode if available",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# dc-074  Contradictory information across email thread replies
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="dc-074",
        category=Category.HARDWARE,
        priority=Priority.P3,
        assigned_team=Team.ENDPOINT,
        needs_escalation=False,
        missing_information=[
            MissingInfo.DEVICE_INFO,
            MissingInfo.ERROR_MESSAGE,
            MissingInfo.STEPS_TO_REPRODUCE,
        ],
        subjects=[
            "RE: RE: RE: Laptop issue — update",
            "RE: RE: Laptop won't boot / actually it does / never mind / help",
            "FW: RE: RE: Laptop problem — conflicting updates",
        ],
        descriptions=[
            "Latest update:\n"
            "Actually, the laptop turned on this morning but now there's a different "
            "problem — the display is flickering and the colors look washed out.\n\n"
            "--- Previous reply ({date}) ---\n"
            "Update: the laptop turns on now (I left it charging overnight) but the "
            "screen stays completely black. I can hear the fan spinning and the power "
            "LED is green. External monitor via HDMI shows nothing either.\n\n"
            "--- Previous reply ({date}) ---\n"
            "Correction — the laptop does show a brief Dell logo on startup but then "
            "goes to a black screen with a blinking cursor. It never reaches Windows.\n\n"
            "--- Original message ---\n"
            "My laptop won't turn on at all. No lights, no fan, nothing. I've tried "
            "holding the power button for 30 seconds, removing the charger, etc. "
            "Completely dead. I need this for my {department} presentation tomorrow.\n\n"
            "So to summarize: it was dead, then it showed a logo, then black screen "
            "with cursor, then it booted but screen was black, and now it boots but "
            "the display is flickering. Not sure what's going on.",
            "Thread summary from {name} in {department}:\n\n"
            "Message 5 (today): 'It's working now, but the trackpad is unresponsive. "
            "Using an external mouse as workaround.'\n\n"
            "Message 4 (yesterday): 'Screen came back but it's displaying at 800x600 "
            "resolution and I can't change it. Display adapter shows Microsoft Basic "
            "Display Adapter instead of the NVIDIA card.'\n\n"
            "Message 3 (2 days ago): 'Laptop boots to Windows but the screen goes "
            "black after about 30 seconds. I think it's a display driver crash.'\n\n"
            "Message 2 (3 days ago): 'Laptop turns on but I get a blue screen with "
            "error DRIVER_IRQL_NOT_LESS_OR_EQUAL about 2 minutes after login.'\n\n"
            "Message 1 (4 days ago): 'My laptop won't start. Just a black screen. "
            "Nothing happens when I press the power button.'\n\n"
            "I need someone to look at this — the symptoms keep changing and I can't "
            "figure out what's actually wrong.",
        ],
        next_best_actions=[
            "Schedule an in-person diagnostic for the laptop — the evolving symptoms "
            "(power failure → BSOD → display driver issues → trackpad failure) suggest "
            "a hardware fault, possibly motherboard or GPU related.",
            "The contradictory thread indicates a progressive hardware failure. Arrange "
            "for the endpoint team to run full hardware diagnostics on-site.",
        ],
        remediation_steps=[
            [
                "Run comprehensive hardware diagnostics (Dell/Lenovo built-in diagnostics at boot)",
                "Check for GPU and display driver issues — reinstall NVIDIA/AMD drivers",
                "If BSOD is recurring, analyze memory dumps for the specific driver at fault",
                "Test with a known-good RAM module to rule out memory failure",
                "If multiple subsystems are failing, recommend a full device replacement",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# dc-075  Accidental PII-like patterns in ticket description
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="dc-075",
        category=Category.ACCESS_AUTH,
        priority=Priority.P2,
        assigned_team=Team.IAM,
        needs_escalation=False,
        missing_information=[MissingInfo.AUTHENTICATION_METHOD, MissingInfo.ERROR_MESSAGE],
        subjects=[
            "MFA enrollment failure — need help setting up authenticator",
            "Can't register my phone for multi-factor authentication",
            "MFA setup error — verification code not arriving",
        ],
        descriptions=[
            "Hi IT,\n\n"
            "I'm trying to enroll in MFA but the Microsoft Authenticator setup keeps "
            "failing. Here are my details so you can look me up:\n\n"
            "Name: {name}\n"
            "Employee ID: EMP-{number}\n"
            "Department: {department}\n"
            "Phone: +1 (212) 555-{number}\n"
            "Personal phone (backup): +1 (917) 555-{number}\n"
            "Home address: 742 Evergreen Terrace, Apt 4B, New York, NY 10001\n"
            "SSN (last 4): XXXX-XX-{number}\n"
            "Corporate card (for verification): XXXX-XXXX-XXXX-{number}\n"
            "Date of birth: 1985-07-{number}\n\n"
            "The error I get is 'Verification failed — please try again' after scanning "
            "the QR code. I've tried three times. My phone is an iPhone 15 running iOS 17.4.\n\n"
            "Please help — I'm locked out of {app} and {browser} SSO until MFA is set up.",
            "Can't complete MFA enrollment. The setup wizard gets to step 3 (verify phone "
            "number) and then errors out. I'm providing extra info in case it helps:\n\n"
            "Account: {name1}@contoso.com\n"
            "Badge number: CNT-{number}\n"
            "Phone: +44 20 7946 {number}\n"
            "Alt contact: +44 7911 {number}\n"
            "National Insurance: AB-{number}-C (just last digits for reference)\n"
            "Corporate Amex: XXXX-XXXXXX-X{number}\n"
            "Passport: GBR-{number} (I had to provide this during onboarding)\n\n"
            "I'm in the {office} office, Floor {floor}, {department}. This is blocking "
            "all my work because conditional access requires MFA for everything.",
        ],
        next_best_actions=[
            "Process the MFA enrollment issue — but first flag that the ticket contains "
            "sensitive PII (partial SSN, credit card digits, home address) that should be "
            "redacted from the ticket system immediately.",
            "Resolve the MFA verification failure. Alert the user that personal information "
            "like SSN and credit card numbers should never be included in support tickets. "
            "Request that a supervisor redact the sensitive data from the ticket.",
        ],
        remediation_steps=[
            [
                "IMMEDIATELY redact all PII from the ticket (SSN, credit card, passport, home address)",
                "Notify the user that sensitive personal data must never be included in tickets",
                "Troubleshoot the MFA enrollment failure — verify the user's phone number in Entra ID",
                "Check if the Authenticator app version is compatible with the tenant's MFA configuration",
                "If enrollment continues to fail, provision a FIDO2 security key as an alternative",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# dc-076  Extremely long email with buried issue
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="dc-076",
        category=Category.HARDWARE,
        priority=Priority.P3,
        assigned_team=Team.ENDPOINT,
        needs_escalation=False,
        missing_information=[MissingInfo.DEVICE_INFO, MissingInfo.ERROR_MESSAGE],
        subjects=[
            "Various things — also laptop problem",
            "Quick update + IT issue at the end",
            "Couple of things to mention (including a tech issue)",
        ],
        descriptions=[
            "Hi IT team,\n\n"
            "Hope you all had a great weekend! I went hiking up near {office} and the weather "
            "was absolutely perfect — sunny, mid-60s, not a cloud in the sky. My dog loved it.\n\n"
            "Anyway, I wanted to follow up on the parking situation. I noticed that the spots "
            "on level B2 near the south elevator are still unmarked, and a few people from "
            "{department} have been parking there even though those are supposed to be reserved "
            "for visitors. Could someone from facilities look into that? I mentioned it to "
            "{name1} last Tuesday but haven't heard back.\n\n"
            "Also, the printer on {floor} — the big color LaserJet near the kitchen — has been "
            "making a grinding noise for about two weeks now. I know this isn't really your "
            "department but I figured I'd mention it since the facilities request form has been "
            "down (ironic, right?).\n\n"
            "Oh, and the badges — {name1} said the new badge readers on the east wing were "
            "going to be installed by end of Q3 but we're well past that now. The old ones "
            "work fine I guess, but they're slow and sometimes you have to tap three or four "
            "times. Minor annoyance.\n\n"
            "Speaking of minor annoyances, the vending machine on {floor} ate my dollar again "
            "yesterday. That's the third time this month. I've started keeping a tally.\n\n"
            "The coffee machine in the {department} break room is also acting up — it dispenses "
            "about half a cup and then stops. {name1} tried descaling it but no luck.\n\n"
            "I also wanted to say thanks for fixing the projector in conference room {number} "
            "last week. That was super quick turnaround and we were able to get our client "
            "presentation done on time. Really appreciated.\n\n"
            "Now, the actual reason I'm writing — my laptop ({os}) has been randomly freezing "
            "for about 10-15 seconds at a time. It happens maybe 4-5 times a day, usually when "
            "I have {app} and {browser} open together. The screen just locks up completely, "
            "the cursor won't move, and then it comes back like nothing happened. No error "
            "message, no blue screen, just a hard freeze. Started around {date}.\n\n"
            "Let me know if you need me to bring it in or if there's something I can try first. "
            "Thanks!\n\n"
            "Best,\n{name}\n{department}",
            "Hello,\n\n"
            "Before I get to my actual question I just want to say that the new {office} "
            "renovation looks amazing. The open floor plan is going to be great for "
            "collaboration. I heard {name1} from facilities was the one who pushed for the "
            "standing desk option and I think that's fantastic.\n\n"
            "I also want to mention that the shuttle schedule between buildings has been really "
            "inconsistent lately. Last Thursday I waited 25 minutes for what's supposed to be "
            "a 10-minute loop. I almost missed my 2pm with the {department} team. Maybe we "
            "could get a real-time tracking app or something?\n\n"
            "On the topic of apps, the new expense reporting tool is… an experience. I spent "
            "an hour trying to figure out how to attach a receipt and ended up just emailing it "
            "to {name1} manually. Maybe some training sessions would help? Just a thought.\n\n"
            "Also, the air conditioning on {floor} has been set to what I can only describe as "
            "'arctic tundra' for the past week. I'm wearing a jacket indoors in July. I know "
            "facilities handles that but again, their form is broken.\n\n"
            "The cafeteria switched coffee suppliers and I'm not a fan. The old brand was from "
            "that local roaster and had actual flavor. This new stuff tastes like sadness.\n\n"
            "OK here is my actual issue: my docking station stopped recognizing my second "
            "monitor as of {date}. I'm running {os} and have a dual-monitor setup. The left "
            "monitor works fine through HDMI but the right one connected via DisplayPort just "
            "shows 'No Signal.' I've tried swapping cables, rebooting, updating drivers — "
            "nothing works. I rely on the second screen for {app} dashboards and it's really "
            "slowing me down.\n\n"
            "Anyway, sorry for the long email. Let me know what you think!\n\n"
            "Cheers,\n{name}",
        ],
        next_best_actions=[
            "Diagnose intermittent laptop freezing under multi-application load.",
            "Troubleshoot docking station display output failure on secondary monitor.",
        ],
        remediation_steps=[
            [
                "Run hardware diagnostics (memory and SSD health check) on the reported laptop",
                "Check Task Manager during freeze for any process consuming 100% CPU or disk",
                "Update chipset and display adapter drivers to the latest vendor release",
                "Test with a replacement docking station to rule out hardware failure",
                "If freezes persist, schedule a full OS reimage and hardware swap",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# dc-077  Massive base64-encoded PDF inline
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="dc-077",
        category=Category.SECURITY,
        priority=Priority.P2,
        assigned_team=Team.SECOPS,
        needs_escalation=False,
        missing_information=[MissingInfo.AFFECTED_SYSTEM, MissingInfo.TIMESTAMP],
        subjects=[
            "Compliance audit report — see attached PDF inline",
            "Security scan results — PDF embedded below",
            "Quarterly compliance report — inline attachment",
        ],
        descriptions=[
            "Hi SecOps,\n\n"
            "I ran the quarterly compliance scan and the report flagged several issues. I'm "
            "pasting the PDF inline because the attachment system is broken again.\n\n"
            "--- BEGIN COMPLIANCE REPORT PDF ---\n"
            "data:application/pdf;base64,JVBERi0xLjQKMSAwIG9iago8PCAvVHlwZSAvQ2F0YWxvZwov"
            "UGFnZXMgMiAwIFIgPj4KZW5kb2JqCjIgMCBvYmoKPDwgL1R5cGUgL1BhZ2VzCi9LaWRzIFsz"
            "IDAgUl0KL0NvdW50IDEgPj4KZW5kb2JqCjMgMCBvYmoKPDwgL1R5cGUgL1BhZ2UKL1BhcmVu"
            "dCAyIDAgUgovTWVkaWFCb3ggWzAgMCA2MTIgNzkyXQovQ29udGVudHMgNCAwIFIKL1Jlc291cm"
            "NlcyA8PCAvRm9udCA8PCAvRjEgNSAwIFIgPj4gPj4gPj4KZW5kb2JqCjQgMCBvYmoKPDwgL0xl"
            "bmd0aCA0NCA+PgpzdHJlYW0KQlQKL0YxIDE4IFRmCjEwMCA3MDAgVGQKKENvbXBsaWFuY2Ug"
            "UmVwb3J0KSBUagpFVAplbmRzdHJlYW0KZW5kb2JqCjUgMCBvYmoKPDwgL1R5cGUgL0ZvbnQK"
            "L1N1YnR5cGUgL1R5cGUxCi9CYXNlRm9udCAvSGVsdmV0aWNhID4+CmVuZG9iagp4cmVmCjAg"
            "NgowMDAwMDAwMDAwIDY1NTM1IGYgCjAwMDAwMDAwMDkgMDAwMDAgbiAKMDAwMDAwMDA1OCAw"
            "MDAwMCBuIAowMDAwMDAwMTE1IDAwMDAwIG4gCjAwMDAwMDAzMDYgMDAwMDAgbiAKMDAwMMDM"
            "OTkgMDAwMDAgbiAKdHJhaWxlcgo8PCAvU2l6ZSA2Ci9Sb290IDEgMCBSID4+CnN0YXJ0eHJl"
            "ZgozNDkKJSVFT0YKCi9TdWJ0eXBlIC9UeXBlMQovQmFzZUZvbnQgL0hlbHZldGljYSA+Pgpl"
            "bmRvYmoKeHJlZgowIDYKMDAwMDAwMDAwMCA2NTUzNSBmIAowMDAwMDAwMDA5IDAwMDAwIG4g"
            "CjAwMDAwMDAwNTggMDAwMDAgbiAKMDAwMDAwMDExNSAwMDAwMCBuIAowMDAwMDAwMzA2IDAw"
            "MDAwIG4gCjAwMDAwMDAzOTkgMDAwMDAgbiAKdHJhaWxlcgo8PCAvU2l6ZSA2Ci9Sb290IDEg"
            "MCBSID4+CnN0YXJ0eHJlZgozNDkKJSVFT0YK\n"
            "--- END COMPLIANCE REPORT PDF ---\n\n"
            "The scan found that several endpoints in the {department} segment are running "
            "outdated antivirus definitions. The specific hosts aren't listed in the PDF "
            "summary for some reason — it just says '{number} hosts non-compliant.' "
            "We need to figure out which machines are affected before the audit on {date}.\n\n"
            "Also, the scan tool itself ({app}) crashed twice during the run with error "
            "'{error_code}' which makes me wonder if the results are even complete.\n\n"
            "Can you investigate?\n\n"
            "— {name}, {department}",
            "Team,\n\n"
            "Attached below (inline, sorry) is the PDF output from our {app} vulnerability "
            "scanner. The ticketing system won't let me upload .pdf files today for some "
            "reason.\n\n"
            "data:application/pdf;base64,JVBERi0xLjcNCjEgMCBvYmoNCjw8IC9UeXBlIC9DYXRhbG9n"
            "IC9QYWdlcyAyIDAgUiA+Pg0KZW5kb2JqDQoyIDAgb2JqDQo8PCAvVHlwZSAvUGFnZXMgL0tp"
            "ZHMgWzMgMCBSXSAvQ291bnQgMSA+Pg0KZW5kb2JqDQozIDAgb2JqDQo8PCAvVHlwZSAvUGFn"
            "ZSAvUGFyZW50IDIgMCBSIC9NZWRpYUJveCBbMCAwIDYxMiA3OTJdIC9Db250ZW50cyA0IDAg"
            "UiAvUmVzb3VyY2VzIDw8IC9Gb250IDw8IC9GMSAFIDAgUiA+PiA+PiA+Pg0KZW5kb2JqDQo0"
            "IDAgb2JqDQo8PCAvTGVuZ3RoIDQ0ID4+DQpzdHJlYW0NCkJUDQovRjEgMTIgVGYNCjEwMCA3"
            "MDAgVGQNCihWdWxuZXJhYmlsaXR5IFJlcG9ydCkgVGoNCkVUDQplbmRzdHJlYW0NCmVuZG9i"
            "ag0KNSAwIG9iag0KPDwgL1R5cGUgL0ZvbnQgL1N1YnR5cGUgL1R5cGUxIC9CYXNlRm9udCAv"
            "SGVsdmV0aWNhID4+DQplbmRvYmoNCnhyZWYNCjAgNg0KMDAwMDAwMDAwMCA2NTUzNSBmIA0K"
            "MDAwMDAwMDAwOSAwMDAwMCBuIA0KMDAwMDAwMDA1OCAwMDAwMCBuIA0KMDAwMDAwMDExNSAw\n\n"
            "The report summary says we have {number} critical and {number} high-severity "
            "findings across the {office} network segment. Most seem related to unpatched "
            "{os} systems and expired TLS certificates on internal services.\n\n"
            "I need SecOps to review these findings and confirm which ones are real vs. "
            "false positives. The auditor from {department} is coming on {date} and we need "
            "a remediation plan before then.\n\n"
            "Thanks,\n{name}",
        ],
        next_best_actions=[
            "Review compliance scan results and identify non-compliant endpoints.",
            "Validate vulnerability findings and prepare remediation plan before audit deadline.",
        ],
        remediation_steps=[
            [
                "Extract and decode the PDF report to identify specific non-compliant hosts",
                "Cross-reference flagged endpoints against the CMDB to confirm ownership",
                "Push emergency antivirus definition updates to non-compliant machines",
                "Renew expired TLS certificates on internal services before audit date",
                "Re-run the compliance scan to verify remediation and generate a clean report",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# dc-078  Multiple base64 screenshots in email chain
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="dc-078",
        category=Category.HARDWARE,
        priority=Priority.P3,
        assigned_team=Team.ENDPOINT,
        needs_escalation=False,
        missing_information=[MissingInfo.DEVICE_INFO, MissingInfo.ERROR_MESSAGE],
        subjects=[
            "Laptop screen glitch — multiple screenshots attached",
            "Display artifacts — see all images below",
            "Screen issues — several screenshots inline",
        ],
        descriptions=[
            "Hi,\n\n"
            "My laptop screen keeps showing weird colored lines. Here are screenshots I took "
            "throughout the day:\n\n"
            "Screenshot 1 (9:04 AM — first occurrence):\n"
            "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAIAAAACACAYAAADDPmHLAAAABHNCSVQI"
            "CAgIfAhkiAAAAAlwSFlzAAALEwAACxMBAJqcGAAAABl0RVh0U29mdHdhcmUAd3d3Lmlua3NjYXBl"
            "Lm9yZ5vuPBoAACAASURBVHic7Z13XFTX1sd/M0NvUkVBsWBBsaFiN/ZeY429xBhjEjXJjcmNud6b"
            "3JvE9F5MNBqNMRpj773FXrBhQ0BFpErvzLx/nBkYYAZQk7z3fb+fDzBn9t5nn73XXnvttc8MKIqi"
            "KP8f1/8H/g/wf4D/A/wf4L8A/1/y3wBj9aoAAAAASUVORK5CYII=\n\n"
            "Screenshot 2 (11:32 AM — happened again during a Teams call):\n"
            "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAIAAAACACAYAAADDPmHLAAAACXBIWXMA"
            "AAsTAAALEwEAmpwYAAAAIGNIUk0AAHolAACAgwAA+f8AAIDpAAB1MAAA6mAAADqYAAAXb5JfxUYA"
            "AAY1SURBVHja7J17cBRlHsc/uwlJICSEBBRRRFFARFBBVDgVBcQL4uF5FiqnUuWJdz7O8r+yTqvK"
            "unPPq7Ku0rPUKvVOj0MEBUVAHoqIiIAgAiKP8JKQEELI+9F7f7y7s7uZ3exudjfJ7nw+VVOzM/ub"
            "2Zn5/r7f3/f7e3cNBoPB8N/m/wn/m5wCsP8/aBf+GwEUBfv/A/4L+C/A/wEU8F+L/z+w/38BRQH/"
            "LfgHjAL+C/C/e7T/6QMoKirif/rUqf8GZ+W/Y/TfCKAo2P83OP8/gn+A/9PmDAb7/4P+D6Ao4L8F"
            "/4BRwH8B/neP9v+9CYOi/H+D/X8B5f8D/jvw/4D/A/w3QDbm/8P+HxT8H+C/Af+Akf5b8N+C/wb8"
            "A/43R/ufPICiYP9/4P8A/wf4P8D/ART8n+C/AP+7R/v/4AEUBfv/Bue/Ef8N+Af8b472P3UARQH/"
            "tfgv4L8A/we4/k8fQFGw/z/wfwD5/wd7AKEAAAAABJRU5ErkJggg==\n\n"
            "It went away for a bit and I thought it was fixed, but then:\n\n"
            "Screenshot 3 (2:17 PM — after docking):\n"
            "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAQAAAAEACAYAAABccqhmAAAABGdBTUEA"
            "ALGPC/xhBQAAAAlwSFlzAAAOwQAADsEBuJFr7QAAAAd0SU1FB9sECgEMC3MklPUAAAAZdEVYdENv"
            "bW1lbnQAQ3JlYXRlZCB3aXRoIEdJTVBXgQ4XAAAANklEQVR42u3BMQEAAADCoPVPbQwfoAAAAAAAA"
            "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAIBrA8QAAQDR6h+YAAAAABJRU5ErkJggg==\n\n"
            "Screenshot 4 (4:45 PM — worst one yet, whole screen had pink tint):\n"
            "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEASABIAAD/2wBDAAgGBgcGBQgHBwcJCQgKDBQ"
            "NDAsLDBkSEw8UHRofHh0aHBwgJC4nICIsIxwcKDcpLDAxNDQ0Hyc5PTgyPC4zNDL/2wBDAQkJCQwL"
            "DBgNDRgyIRwhMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIy"
            "MjL/wAARCAABAAEDASIAAhEBAxEB/8QAFAABAAAAAAAAAAAAAAAAAAAACP/EABQQAQAAAAAAAAAAAAA"
            "AAAAAAAAB/8QAFQEBAQAAAAAAAAAAAAAAAAAAB//EABQRAQAAAAAAAAAAAAAAAAAAAAD/2gAMAwEAAh"
            "EDEQA/AKYAB//Z\n\n"
            "The lines are always horizontal, green or pink, and they flicker. The laptop is "
            "about 2 years old. Running {os}. I mostly use it docked on {floor} but it "
            "happens undocked too.\n\n"
            "— {name}",
            "Forwarding my screenshots of the screen artifacts issue.\n\n"
            "From: {name}\nTo: IT Support\nDate: {date}\n\n"
            "Image A — the glitch when I first open {app}:\n"
            "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAKCAYAAACNMs+9AAAAFklEQVQY"
            "V2P8z8BQz0AEYBxVOHIUAgBGWAgEe5fL3AAAAABJRU5ErkJggg==\n\n"
            "Image B — the glitch after about 20 minutes:\n"
            "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAKCAYAAACNMs+9AAAAFUlEQVQY"
            "V2P8z8DwHwMNgHFU4chRCADVhAgIyPcZcQAAAABJRU5ErkJggg==\n\n"
            "Image C — the screen after a reboot (still broken):\n"
            "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAKCAYAAACNMs+9AAAAFUlEQVQY"
            "V2P8z8BQz0AEYBxVOHIUAgBu7wgIL2vDCAAAAABJRU5ErkJggg==\n\n"
            "Image D — zoomed in on the artifact area:\n"
            "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAKCAYAAACNMs+9AAAAFUlEQVQY"
            "V2P8z8BQz0AEYBxVOHIUAgBrcwgIlrK09QAAAABJRU5ErkJggg==\n\n"
            "As you can see the artifacts are persistent. They get worse through the day. "
            "Restarting doesn't fix it. Happens in {app} and {browser} and everywhere. "
            "I think the display panel might be failing. {os} updated last week but I "
            "don't know if that's related.\n\n"
            "Please help — {name}, {department}",
        ],
        next_best_actions=[
            "Diagnose display artifacts on laptop screen, both docked and undocked.",
            "Determine if GPU or display panel hardware is failing.",
        ],
        remediation_steps=[
            [
                "Run built-in display diagnostics to confirm artifacts appear outside the OS",
                "Update GPU drivers and firmware to the latest vendor release",
                "Test with an external monitor to isolate whether the internal panel or GPU is at fault",
                "If artifacts persist on internal display only, schedule a panel replacement",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# dc-079  Mobile autocorrect mangling technical terms
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="dc-079",
        category=Category.SOFTWARE,
        priority=Priority.P3,
        assigned_team=Team.ENTERPRISE_APPS,
        needs_escalation=False,
        missing_information=[MissingInfo.APPLICATION_VERSION, MissingInfo.ERROR_MESSAGE],
        subjects=[
            "Outlook not sinking on phone",
            "Cant log into the van",
            "Apps keeps crashing on my devise",
        ],
        descriptions=[
            "Hey so I'm typing this from my phone sorry for any typos\n\n"
            "So basically my outlook has been acting up all week on my phone it keeps saying "
            "something about a certificate era and then it won't sink my mail. I tried going "
            "to the sittings and doing a mantle sink but it just spins forever.\n\n"
            "Also the van has been super slow lately — I connect and it says connected but then "
            "nothing loads. I tried the web version of the portal through my browser and it's "
            "fine so it's definitely something with the van client. My college {name1} in "
            "{department} has the same issue on their phone too.\n\n"
            "The teams app is also being weird — sometimes when I get a notification and tap "
            "it it takes me to a blank white screen and I have to force clothes the app and "
            "re-open it. This has been happening since the last {os} update.\n\n"
            "OH also the multi-factory authentication thing keeps asking me every single time "
            "I open anything even though I checked the 'remember this devise' box. It's asking "
            "like 10 times a day and it's really annoying.\n\n"
            "I'm not at my desk right now so I can't check the exact error massage but I'll "
            "try to get a screen shot when it happens again.\n\n"
            "Sent from my iPhone\n"
            "{name}\n{department}",
            "Hi IT\n\n"
            "I'm having trouble with {app} on my phone. When I try to open the app it shows "
            "a beside screen (you know the blue screen with the sad face) for like a second "
            "and then just closes itself. This started happening after I updated to the latest "
            "version of {os}.\n\n"
            "I also can't get the company male to work — it says it can't very fy my credentials "
            "and to contact my administrator. I'm using the same password I always use and it "
            "works fine on my lap top.\n\n"
            "My college suggested I try clearing the cash but I went to settings and there's no "
            "option for that in the new update. The inter face changed completely and I can't "
            "find half the sittings anymore.\n\n"
            "One more thing — the wire less connection in the {office} building keeps dropping. "
            "I'll be on a teams call and suddenly I'm disconnected and have to re join. It shows "
            "the wi-if signal as full bars but the inter net just stops working for about "
            "30 seconds at a time. This happens on {floor} mostly.\n\n"
            "Can someone please help? I'm loosing productivity big time.\n\n"
            "Thanks\n{name}\n\nSent from my Samsung Galaxy",
        ],
        next_best_actions=[
            "Troubleshoot mobile email sync failure and VPN connectivity issues.",
            "Investigate app crash and credential verification failure on mobile device.",
        ],
        remediation_steps=[
            [
                "Verify mail profile configuration and SSL certificate validity on the mobile device",
                "Reinstall the VPN client and re-provision the connection profile",
                "Clear app cache and data for the crashing application, then re-authenticate",
                "Check MFA token registration and re-enroll the device if persistent prompts continue",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# dc-080  Voicemail / speech-to-text transcription with accent errors
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="dc-080",
        category=Category.NETWORK,
        priority=Priority.P2,
        assigned_team=Team.NETWORK,
        needs_escalation=False,
        missing_information=[MissingInfo.NETWORK_LOCATION, MissingInfo.ERROR_MESSAGE],
        subjects=[
            "Voicemail transcription — network issue report",
            "Transcribed voicemail from {name} re: connectivity",
            "Auto-transcribed voice message — urgent network problem",
        ],
        descriptions=[
            "[Auto-transcribed voicemail received {date} at 3:47 PM — duration 2:34]\n"
            "[Confidence: Low — background noise detected]\n\n"
            "Hello yes this is {name} calling from the {department} apartment... department "
            "sorry. I need to report a serious internet issue we are having on floor "
            "{floor}.\n\n"
            "So basically since about — um — since this moaning... morning, the wire less "
            "network has been going in and out. It connects for maybe five minutes and then "
            "drops for like two or free minutes and then connects again. It's been doing this "
            "all morning and we can't get any work done.\n\n"
            "I spoke with our adminis traitor... administrator {name1} and they said to call "
            "you guys because it might be an issue with the excess... access point near "
            "conference room {number}. Apparently the light on the device is blinking read "
            "instead of green which apparently means something bad.\n\n"
            "We've got about {number} people on this floor who are all effective... affected "
            "by this and we have a big client prison... presentation tomorrow so we really "
            "need this fixed by the end of today if possible.\n\n"
            "Also I should mention that the ether net... ethernet connections at the desks "
            "seem to be working fine so it's just the wife eye... Wi-Fi that's the problem. "
            "I tried connecting to the guest net work as a walk around... workaround but it "
            "won't let me access any of the interval... internal resources.\n\n"
            "Please call me back at extension {number} or you can email me but "
            "I might not get the email because of the internet thing.\n\n"
            "Thank you.\n\n"
            "[End of transcription]",
            "[Voicemail transcription — {date} 10:12 AM]\n"
            "[Speaker: {name}, {department}]\n"
            "[Transcription quality: Poor — heavy accent detected]\n\n"
            "Yes hello I am calling because we have a very big problem with the net work "
            "in the {office} building. Since yes-today... yesterday evening the VEE PEE "
            "ENN... VPN has been not working for anyone in our department.\n\n"
            "When we try to connect it says — let me read the message — it says 'failed to "
            "establish tunnel air or code {error_code}.' I don't know what that means but "
            "everyone is getting the same error.\n\n"
            "We tried rebooting the fire wall... firewall on our floor but that didn't help. "
            "Actually I'm not sure if we're supposed to reboot the fire wall ourselves but "
            "{name1} said it would be okay.\n\n"
            "The strange thing is that the net work browse-ing... browsing works fine. I can "
            "open goo-gull... Google and web sites and everything. It's just the VPN that "
            "won't connect. And without the VPN we can't reach the file sever... server or "
            "the share point... SharePoint or any of the internal tools.\n\n"
            "Also one more thing — the print... printer on {floor} is showing off-line "
            "even though the lights are on and it's connected to the net work. But the "
            "printer might be a separate issue I don't know.\n\n"
            "Please call me back or send someone as soon as possible because this is "
            "affecting our whole department's prod-ductivity.\n\n"
            "[End of voicemail transcription]",
        ],
        next_best_actions=[
            "Investigate Wi-Fi access point failure causing intermittent wireless connectivity.",
            "Troubleshoot VPN tunnel establishment failure across department.",
        ],
        remediation_steps=[
            [
                "Check the access point status on the wireless controller dashboard for the reported floor",
                "Restart or replace the access point showing a red status LED",
                "Verify VPN concentrator configuration and check for expired certificates causing tunnel failures",
                "Test VPN connectivity from the affected floor after access point restoration",
                "Confirm all internal resources (file server, SharePoint) are reachable via VPN",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# dc-081  Zero-width Unicode and invisible characters
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="dc-081",
        category=Category.ACCESS_AUTH,
        priority=Priority.P2,
        assigned_team=Team.IAM,
        needs_escalation=False,
        missing_information=[MissingInfo.AUTHENTICATION_METHOD, MissingInfo.AFFECTED_SYSTEM],
        subjects=[
            "Can\u200bt lo\u200bg i\u200dn to\u200b por\u200btal",
            "Account\u200b lock\u200ced\u200b out\u200b aga\u200bin",
            "SS\u200bO \u200bnot\u200b work\u200bing\u200b for \u200bme",
        ],
        descriptions=[
            "Hi\u200b IT\u200b team\u200b,\n\n"
            "I\u200b've\u200b been\u200b locked\u200b out\u200b of\u200b my\u200b account\u200b "
            "again\u200b.\u200b This\u200b is\u200b the\u200b third\u200b time\u200b this\u200b "
            "week\u200b.\u200b Every\u200b time\u200b I\u200b try\u200b to\u200b log\u200b "
            "in\u200b to\u200b the\u200b {app}\u200b portal\u200b,\u200b it\u200b says\u200b "
            "'\u200bInvalid\u200b credentials\u200b'\u200b even\u200b though\u200b I\u200b "
            "just\u200b reset\u200b my\u200b password\u200b yesterday\u200b.\n\n"
            "I\u200b think\u200b there\u200b might\u200b be\u200b a\u200b problem\u200b with\u200b "
            "the\u200b SSO\u200b configuration\u200b because\u200b {name1}\u200b in\u200b "
            "my\u200b department\u200b is\u200b having\u200b the\u200b same\u200b issue\u200b.\n\n"
            "I\u200b am\u200b using\u200b {browser}\u200b on\u200b {os}\u200b.\u200b The\u200b "
            "error\u200b happens\u200b on\u200b the\u200b login\u200b page\u200b after\u200b "
            "I\u200b enter\u200b my\u200b email\u200b and\u200b password\u200b and\u200b "
            "click\u200b '\u200bSign\u200b In\u200b'\u200b.\u200b It\u200b redirects\u200b "
            "me\u200b to\u200b the\u200b IdP\u200b page\u200b and\u200b then\u200b comes\u200b "
            "back\u200b with\u200b the\u200b error\u200b.\n\n"
            "I\u200b also\u200b noticed\u200b that\u200b when\u200b I\u200b copy\u200b "
            "paste\u200b my\u200b username\u200b from\u200b our\u200b directory\u200b,\u200b "
            "it\u200b doesn\u200b't\u200b work\u200b,\u200b but\u200b when\u200b I\u200b "
            "manually\u200b type\u200b it\u200b,\u200b it\u200b sometimes\u200b does\u200b.\u200b "
            "Very\u200b confusing\u200b.\n\n"
            "Please\u200b help\u200b,\u200b this\u200b is\u200b urgent\u200b.\n\n"
            "{name}\u200b,\u200b {department}",
            "Hi\u200b,\n\n"
            "I\u200b can\u200b't\u200b log\u200b in\u200b to\u200b {app}\u200b.\u200b "
            "Every\u200b time\u200b I\u200b enter\u200b my\u200b password\u200b "
            "it\u200b says\u200b '\u200bAuthentication\u200b failed\u200b'\u200b.\n\n"
            "I\u200b've\u200b tried\u200b resetting\u200b my\u200b password\u200b "
            "through\u200b the\u200b self\u200b-\u200bservice\u200b portal\u200b "
            "but\u200b that\u200b also\u200b gives\u200b me\u200b an\u200b error\u200b.\n\n"
            "I\u200b think\u200b there\u200b might\u200b be\u200b invisible\u200b "
            "characters\u200b in\u200b my\u200b username\u200b from\u200b "
            "copy\u200b-\u200bpasting\u200b.\n\n"
            "{name}\u200b,\u200b {department}",
        ],
        next_best_actions=[
            "Strip zero-width Unicode characters from the text and process the "
            "underlying SSO / authentication issue. The user is locked out and "
            "copy-pasted usernames may contain invisible characters.",
            "Investigate the authentication failure — the ticket contains zero-width "
            "Unicode artifacts that may also be present in the user's credentials.",
        ],
        remediation_steps=[
            [
                "Check the user's Active Directory account status and unlock if locked",
                "Verify the SSO / IdP configuration for the target application",
                "Advise the user to manually type credentials rather than copy-pasting to avoid invisible characters",
                "Check if the self-service password reset portal is functioning correctly",
                "Review authentication logs for the specific error details",
            ],
        ],
    )
)

register(
    ScenarioTemplate(
        scenario_id="dc-101",
        category=Category.SOFTWARE,
        priority=Priority.P2,
        assigned_team=Team.ENTERPRISE_APPS,
        needs_escalation=False,
        missing_information=[MissingInfo.ERROR_MESSAGE, MissingInfo.STEPS_TO_REPRODUCE],
        subjects=[
            "API gateway returning wrong data — GraphQL schema dump attached",
            "GraphQL endpoint broken after deployment — introspection output inside",
            "App returning stale results — pasted full schema for reference",
        ],
        descriptions=[
            "Hi team,\n\n"
            "Our {app} dashboard stopped returning correct user data after Friday's "
            "deploy. I ran an introspection query to check the schema and I'm pasting "
            "the output here so you can see what changed:\n\n"
            '{{"data":{{"__schema":{{"queryType":{{"name":"Query"}},"mutationType":'
            '{{"name":"Mutation"}},"subscriptionType":null,"types":['
            '{{"kind":"OBJECT","name":"Query","fields":['
            '{{"name":"user","args":[{{"name":"id","type":{{"kind":"NON_NULL",'
            '"ofType":{{"kind":"SCALAR","name":"ID"}}}}}}],'
            '"type":{{"kind":"OBJECT","name":"User"}}}},'
            '{{"name":"tickets","args":[{{"name":"filter","type":'
            '{{"kind":"INPUT_OBJECT","name":"TicketFilter"}}}}],'
            '"type":{{"kind":"LIST","ofType":{{"kind":"OBJECT","name":"Ticket"}}}}}},'
            '{{"name":"departments","args":[],"type":{{"kind":"LIST","ofType":'
            '{{"kind":"OBJECT","name":"Department"}}}}}}]}},'
            '{{"kind":"OBJECT","name":"User","fields":['
            '{{"name":"id","type":{{"kind":"SCALAR","name":"ID"}}}},'
            '{{"name":"email","type":{{"kind":"SCALAR","name":"String"}}}},'
            '{{"name":"displayName","type":{{"kind":"SCALAR","name":"String"}}}},'
            '{{"name":"department","type":{{"kind":"OBJECT","name":"Department"}}}},'
            '{{"name":"manager","type":{{"kind":"OBJECT","name":"User"}}}}]}},'
            '{{"kind":"OBJECT","name":"Ticket","fields":['
            '{{"name":"id","type":{{"kind":"SCALAR","name":"ID"}}}},'
            '{{"name":"subject","type":{{"kind":"SCALAR","name":"String"}}}},'
            '{{"name":"status","type":{{"kind":"ENUM","name":"TicketStatus"}}}}]}}]'
            "}}}}}}\n\n"
            "The 'user' query used to return a 'role' field but I don't see it in the "
            "schema anymore. This is breaking our RBAC checks in the {app} frontend.\n\n"
            "{name}, {department}",
            "After the last release, {app} is returning null for user roles. I ran "
            "the GraphQL introspection and the role field is missing from the User "
            "type. Here's a partial introspection dump:\n\n"
            '{{"data":{{"__schema":{{"types":['
            '{{"kind":"OBJECT","name":"User","fields":['
            '{{"name":"id","type":{{"kind":"SCALAR","name":"ID"}}}},'
            '{{"name":"email","type":{{"kind":"SCALAR","name":"String"}}}},'
            '{{"name":"displayName","type":{{"kind":"SCALAR","name":"String"}}}}]}},'
            '{{"kind":"ENUM","name":"TicketStatus","enumValues":['
            '{{"name":"OPEN"}},{{"name":"IN_PROGRESS"}},{{"name":"CLOSED"}},'
            '{{"name":"PENDING"}}]}}]}}}}}}\n\n'
            "Can someone check if the schema migration dropped the role field? "
            "This is affecting all users in the {office} office.",
        ],
        next_best_actions=[
            "Investigate the missing 'role' field in the GraphQL User type — likely "
            "a schema regression from the last deployment. Ignore the raw introspection "
            "JSON noise and focus on the reported RBAC breakage.",
            "Check the recent deployment for schema migration issues — the user reports "
            "that the 'role' field was dropped from the User type, breaking RBAC.",
        ],
        remediation_steps=[
            [
                "Review the most recent schema migration for accidental removal of the 'role' field",
                "Compare the current GraphQL schema against the previous release version",
                "If the field was dropped in error, roll back the schema migration or add the field back",
                "Verify RBAC checks in the frontend are working after the schema is corrected",
                "Advise the user to avoid pasting full introspection dumps in tickets — link to a diff instead",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# dc-102  Windows BSOD minidump output
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="dc-102",
        category=Category.HARDWARE,
        priority=Priority.P2,
        assigned_team=Team.ENDPOINT,
        needs_escalation=False,
        missing_information=[MissingInfo.DEVICE_INFO, MissingInfo.STEPS_TO_REPRODUCE],
        subjects=[
            "BSOD happening daily — minidump output pasted below",
            "Blue screen crash every afternoon — WinDbg output inside",
            "Laptop blue-screening — I copied the dump analysis",
        ],
        descriptions=[
            "My laptop has been blue-screening every day around 2-3 PM. I ran WinDbg "
            "on the minidump and here's the output:\n\n"
            "Microsoft (R) Windows Debugger Version 10.0.25877.1004 AMD64\n"
            "Copyright (c) Microsoft Corporation. All rights reserved.\n\n"
            "Loading Dump File [C:\\Windows\\Minidump\\{date}.dmp]\n"
            "Mini Kernel Dump File: Only registers and stack trace are available\n\n"
            "Symbol search path is: srv*\n"
            "Executable search path is:\n"
            "Windows 11 Kernel Version 22631 MP (8 procs) Free x64\n"
            "Product: WinNt, suite: TerminalServer SingleUserTS\n"
            "Edition build lab: 22631.1.amd64fre.ni_release.220506-1250\n"
            "Machine Name:\n"
            "Kernel base = 0xfffff802`1fa00000 PsLoadedModuleList = 0xfffff802`20c134a0\n"
            "Debug session time: {date} 14:32:07.442\n"
            "System Uptime: 0 days 5:12:33.441\n"
            "Loading Kernel Symbols\n"
            "...............................................................\n"
            "Loading User Symbols\n\n"
            "BUGCHECK_STR:  DRIVER_IRQL_NOT_LESS_OR_EQUAL\n"
            "DEFAULT_BUCKET_ID:  WIN8_DRIVER_FAULT\n"
            "PROCESS_NAME:  {app}.exe\n"
            "FAILURE_BUCKET_ID:  AV_ndis!ndisInterruptDpc\n"
            "MODULE_NAME: ndis\n"
            "IMAGE_NAME:  ndis.sys\n"
            "STACK_TEXT:\n"
            "fffff802`1fb34a20 fffff802`1fb2e100 : ndis!ndisInterruptDpc+0x1a2\n"
            "fffff802`1fb34a80 fffff802`1fa8c3b0 : nt!KiProcessExpiredTimerList+0x172\n"
            "fffff802`1fb34b50 fffff802`1fa8b8e5 : nt!KiRetireDpcList+0x5d0\n"
            "fffff802`1fb34e00 fffff802`1fa8b730 : nt!KiIdleLoop+0x55\n\n"
            "I think it's a network driver issue. This happens when I'm on VPN "
            "connected to the {office} office. Laptop is a Lenovo ThinkPad.\n\n"
            "{name}, {department}",
            "Keep getting BSOD — stop code DRIVER_IRQL_NOT_LESS_OR_EQUAL. I found "
            "this in Event Viewer:\n\n"
            "Log Name:      System\n"
            "Source:        BugCheck\n"
            "Event ID:      1001\n"
            "Level:         Error\n"
            "Description:   The computer has rebooted from a bugcheck. The bugcheck "
            "was: 0x000000d1 (0xfffff802deadbeef, 0x0000000000000002, "
            "0x0000000000000000, 0xfffff80200000000). A dump was saved in: "
            "C:\\Windows\\MEMORY.DMP. Report Id: {number}-{number}-{number}.\n\n"
            "Minidump analysis points to ndis.sys. The crashes started after I "
            "installed the new Cisco AnyConnect client last week. I'm in the "
            "{office} office, Floor {floor}.\n\n{name}",
        ],
        next_best_actions=[
            "Investigate the BSOD caused by ndis.sys — likely a network driver conflict, "
            "possibly related to the VPN client. Ignore the raw debugger output and focus "
            "on the driver fault and timing correlation.",
            "The crash analysis points to a network driver fault in ndis.sys. Check for "
            "VPN client and NIC driver compatibility issues.",
        ],
        remediation_steps=[
            [
                "Update the NIC driver to the latest version from the manufacturer",
                "Check for known compatibility issues between the VPN client and the NIC driver",
                "If the crash started after a VPN client update, roll back to the previous version",
                "Run Windows memory diagnostics to rule out RAM issues",
                "If BSODs persist, collect a full memory dump and escalate to the endpoint engineering team",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# dc-103  Teams/Slack webhook JSON payloads
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="dc-103",
        category=Category.SOFTWARE,
        priority=Priority.P3,
        assigned_team=Team.ENTERPRISE_APPS,
        needs_escalation=False,
        missing_information=[MissingInfo.ERROR_MESSAGE, MissingInfo.CONFIGURATION_DETAILS],
        subjects=[
            "Teams webhook notifications stopped working — JSON payload inside",
            "Slack incoming webhook returning 400 — request body pasted",
            "Webhook integration broken after Teams update — payload samples",
        ],
        descriptions=[
            "Our alerting pipeline sends notifications to a Teams channel via webhook "
            "but it stopped working yesterday. Here's the payload we're sending:\n\n"
            '{{"@type":"MessageCard","@context":"https://schema.org/extensions",'
            '"themeColor":"FF0000","summary":"Alert: High CPU on {app}-prod-01",'
            '"sections":[{{"activityTitle":"🚨 Production Alert",'
            '"activitySubtitle":"{app}-prod-01","activityImage":'
            '"https://monitoring.contoso.com/icons/alert.png","facts":['
            '{{"name":"Server",    "value":"{app}-prod-01"}},'
            '{{"name":"CPU",       "value":"98.7%"}},'
            '{{"name":"Memory",    "value":"94.2%"}},'
            '{{"name":"Disk",      "value":"87.1%"}},'
            '{{"name":"Status",    "value":"CRITICAL"}},'
            '{{"name":"Since",     "value":"{date} 14:23 UTC"}},'
            '{{"name":"Region",    "value":"East US 2"}}],'
            '"markdown":true}}],"potentialAction":[{{"@type":"OpenUri",'
            '"name":"View Dashboard","targets":[{{"os":"default",'
            '"uri":"https://monitoring.contoso.com/dashboard/{app}"}}]}}]}}\n\n'
            "The webhook URL is https://contoso.webhook.office.com/webhookb2/ "
            "(truncated). We get back HTTP 400 with no useful error body. This was "
            "working fine until the Teams admin portal update on {date}.\n\n"
            "{name}, {department}",
            "Slack webhook integration for our {app} deployment pipeline broke. "
            "Here's the JSON we post:\n\n"
            '{{"channel":"#deployments","username":"DeployBot",'
            '"icon_emoji":":rocket:","attachments":[{{"color":"danger",'
            '"title":"Deployment Failed: {app} v2.14.3",'
            '"fields":[{{"title":"Environment","value":"Production","short":true}},'
            '{{"title":"Region","value":"West Europe","short":true}},'
            '{{"title":"Error","value":"Container health check failed after 120s",'
            '"short":false}},'
            '{{"title":"Commit","value":"<https://github.contoso.com/app/commit/a1b2c3|a1b2c3>",'
            '"short":true}}],"footer":"CI/CD Pipeline","ts":{number}}}]}}\n\n'
            "Slack returns: {{'ok': false, 'error': 'invalid_payload'}}. The webhook "
            "token was rotated last week — could that be the issue?\n\n{name}",
        ],
        next_best_actions=[
            "Investigate the webhook integration failure — likely a payload format "
            "change or credential rotation issue. Ignore the raw JSON payloads and "
            "focus on the HTTP 400 / invalid_payload errors.",
            "Check if the webhook URL or token was rotated recently and whether the "
            "payload schema still matches the expected format.",
        ],
        remediation_steps=[
            [
                "Verify the webhook URL is still active and has not been regenerated",
                "Check if the Teams/Slack admin made changes to webhook permissions or payload requirements",
                "Validate the JSON payload against the current API schema",
                "If credentials were rotated, update the webhook URL/token in the alerting pipeline",
                "Test with a minimal payload to isolate whether the issue is format or auth related",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# dc-104  PowerShell mixed error/verbose/warning streams
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="dc-104",
        category=Category.SOFTWARE,
        priority=Priority.P2,
        assigned_team=Team.ENTERPRISE_APPS,
        needs_escalation=False,
        missing_information=[MissingInfo.APPLICATION_VERSION, MissingInfo.ENVIRONMENT_DETAILS],
        subjects=[
            "Script failing on user provisioning — PowerShell output pasted",
            "Automated onboarding script errors — full console output inside",
            "PowerShell provisioning broken — mixed error and warning output",
        ],
        descriptions=[
            "The user provisioning script is failing halfway through. I ran it with "
            "-Verbose and captured everything:\n\n"
            "VERBOSE: [09:14:01] Connecting to Exchange Online...\n"
            "VERBOSE: [09:14:03] Connected successfully. Session ID: {number}\n"
            "VERBOSE: [09:14:03] Processing user {name1}@contoso.com\n"
            "VERBOSE: [09:14:04] Creating mailbox...\n"
            "WARNING: The mailbox plan 'ExchangeOnline-Enterprise' is deprecated. "
            "Use 'ExchangeOnline-M365Enterprise' instead.\n"
            "VERBOSE: [09:14:06] Mailbox created: {name1}@contoso.com\n"
            "VERBOSE: [09:14:06] Setting mailbox properties...\n"
            "VERBOSE: [09:14:07] RetentionPolicy: 'Default-365day'\n"
            "VERBOSE: [09:14:07] AddressBookPolicy: 'Global-ABP'\n"
            "WARNING: RetentionPolicy 'Default-365day' not found. Using tenant default.\n"
            "VERBOSE: [09:14:08] Assigning license...\n"
            "Write-Error: Set-MsolUserLicense : Unable to assign license "
            "'contoso:ENTERPRISEPACK' — the user already has a conflicting service "
            "plan 'EXCHANGE_S_ENTERPRISE' from license 'contoso:EMS'.\n"
            "    + CategoryInfo          : NotSpecified: (:) [Set-MsolUserLicense], "
            "MicrosoftOnlineException\n"
            "    + FullyQualifiedErrorId : Microsoft.Online.Administration."
            "Automation.SetUserLicenseException\n"
            "VERBOSE: [09:14:09] Attempting license assignment retry 1/3...\n"
            "Write-Error: Set-MsolUserLicense : Unable to assign license — same error.\n"
            "WARNING: Retry 1 failed. Waiting 5 seconds before retry 2.\n"
            "VERBOSE: [09:14:14] Attempting license assignment retry 2/3...\n"
            "Write-Error: Set-MsolUserLicense : Unable to assign license — same error.\n"
            "WARNING: Retry 2 failed. Waiting 5 seconds before retry 3.\n"
            "VERBOSE: [09:14:19] Attempting license assignment retry 3/3...\n"
            "Write-Error: Set-MsolUserLicense : Unable to assign license — same error.\n"
            "Write-Error: All 3 retries exhausted for {name1}@contoso.com.\n"
            "VERBOSE: [09:14:20] Rolling back mailbox creation...\n"
            "WARNING: Rollback failed — Remove-Mailbox requires Organization "
            "Management role.\n"
            "VERBOSE: [09:14:21] Script completed with errors. 0/1 users provisioned.\n\n"
            "Can someone figure out what's going wrong? The script used to work fine.\n\n"
            "{name}, {department}",
            "Onboarding automation is broken. Here's the console output:\n\n"
            "PS C:\\Scripts> .\\New-UserProvision.ps1 -UserList .\\new_hires.csv "
            "-Verbose -WarningAction Continue 2>&1 | Tee-Object provision_log.txt\n\n"
            "VERBOSE: Loading module AzureAD... Done.\n"
            "VERBOSE: Loading module ExchangeOnlineManagement... Done.\n"
            "VERBOSE: Loading module MicrosoftTeams... Done.\n"
            "WARNING: Module 'AzureAD' is deprecated. Migrate to 'Microsoft.Graph'.\n"
            "WARNING: Module 'MSOnline' is deprecated. Migrate to 'Microsoft.Graph'.\n"
            "VERBOSE: Reading CSV: 15 users to process\n"
            "VERBOSE: User 1/15: {name1}@contoso.com — Creating AD account... OK\n"
            "VERBOSE: User 1/15: Assigning licenses... FAILED (conflicting plan)\n"
            "Write-Error: License conflict for {name1}@contoso.com\n"
            "VERBOSE: User 2/15: {name}@contoso.com — Creating AD account... OK\n"
            "VERBOSE: User 2/15: Assigning licenses... OK\n"
            "VERBOSE: User 2/15: Creating mailbox... OK\n"
            "[...13 more users with mixed results...]\n\n"
            "VERBOSE: Summary: 9 succeeded, 6 failed. See provision_log.txt.\n\n"
            "6 out of 15 new hires didn't get provisioned. I need these done by "
            "Monday for {department} onboarding.\n\n{name}",
        ],
        next_best_actions=[
            "Resolve the license assignment conflict — the users have conflicting "
            "service plans. Ignore the verbose/warning stream noise and focus on the "
            "license conflict errors.",
            "Fix the provisioning failures caused by conflicting license assignments. "
            "The deprecated module warnings are non-blocking but should be addressed separately.",
        ],
        remediation_steps=[
            [
                "Identify and remove the conflicting service plan before assigning the new license",
                "Update the provisioning script to check for existing license conflicts before assignment",
                "Migrate the script from deprecated AzureAD/MSOnline modules to Microsoft.Graph",
                "Fix the retention policy reference to use the correct policy name",
                "Manually provision the 6 failed users and verify their access before Monday",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# dc-105  Docker Compose YAML flood
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="dc-105",
        category=Category.SOFTWARE,
        priority=Priority.P3,
        assigned_team=Team.DATA_PLATFORM,
        needs_escalation=False,
        missing_information=[MissingInfo.ENVIRONMENT_DETAILS, MissingInfo.ERROR_MESSAGE],
        subjects=[
            "Dev environment won't start — full docker-compose.yml pasted",
            "Docker Compose stack broken — YAML config inside",
            "Container orchestration failing — here's our compose file",
        ],
        descriptions=[
            "Our dev environment won't start after someone changed the compose file. "
            "Pasting the full docker-compose.yml here:\n\n"
            "version: '3.8'\n"
            "services:\n"
            "  web:\n"
            "    build:\n"
            "      context: .\n"
            "      dockerfile: Dockerfile.web\n"
            "    ports:\n"
            "      - '8080:8080'\n"
            "      - '8443:8443'\n"
            "    environment:\n"
            "      - NODE_ENV=development\n"
            "      - API_URL=http://api:3000\n"
            "      - REDIS_URL=redis://cache:6379\n"
            "      - DB_HOST=postgres\n"
            "      - DB_PORT=5432\n"
            "      - DB_NAME={app}_dev\n"
            "      - DB_USER=appuser\n"
            "      - DB_PASS=dev_password_123\n"
            "    depends_on:\n"
            "      - api\n"
            "      - cache\n"
            "      - postgres\n"
            "    volumes:\n"
            "      - ./src:/app/src\n"
            "      - node_modules:/app/node_modules\n"
            "    networks:\n"
            "      - frontend\n"
            "      - backend\n"
            "  api:\n"
            "    build:\n"
            "      context: ./api\n"
            "      dockerfile: Dockerfile\n"
            "    ports:\n"
            "      - '3000:3000'\n"
            "    environment:\n"
            "      - FLASK_ENV=development\n"
            "      - DATABASE_URL=postgresql://appuser:dev_password_123@postgres:5432/{app}_dev\n"
            "      - REDIS_URL=redis://cache:6379\n"
            "      - SECRET_KEY=super-secret-dev-key-{number}\n"
            "    depends_on:\n"
            "      - postgres\n"
            "      - cache\n"
            "    networks:\n"
            "      - backend\n"
            "  postgres:\n"
            "    image: postgres:15-alpine\n"
            "    environment:\n"
            "      - POSTGRES_DB={app}_dev\n"
            "      - POSTGRES_USER=appuser\n"
            "      - POSTGRES_PASSWORD=dev_password_123\n"
            "    volumes:\n"
            "      - pgdata:/var/lib/postgresql/data\n"
            "    networks:\n"
            "      - backend\n"
            "  cache:\n"
            "    image: redis:7-alpine\n"
            "    networks:\n"
            "      - backend\n"
            "  nginx:\n"
            "    image: nginx:alpine\n"
            "    ports:\n"
            "      - '80:80'\n"
            "      - '443:443'\n"
            "    volumes:\n"
            "      - ./nginx/nginx.conf:/etc/nginx/nginx.conf:ro\n"
            "    depends_on:\n"
            "      - web\n"
            "    networks:\n"
            "      - frontend\n"
            "volumes:\n"
            "  pgdata:\n"
            "  node_modules:\n"
            "networks:\n"
            "  frontend:\n"
            "  backend:\n\n"
            "When I run 'docker compose up' the api container exits with code 1 and "
            "postgres keeps restarting. I'm in the {office} office.\n\n{name}, {department}",
            "Docker stack is broken. The error is:\n\n"
            "ERROR: for api  Container exited with code 1\n"
            "ERROR: for postgres  Container is unhealthy\n\n"
            "I've attached the full docker-compose.yml (48 services, 200+ lines) "
            "plus all the .env files above. The actual problem is the api container "
            "can't connect to postgres because the healthcheck isn't configured. "
            "Can someone add a proper healthcheck to the postgres service?\n\n"
            "{name}, {department}",
        ],
        next_best_actions=[
            "The api container fails because postgres isn't ready when it starts. "
            "Ignore the full YAML dump and focus on adding a healthcheck to the "
            "postgres service and a depends_on condition to the api service.",
            "Fix the container startup order — add a postgres healthcheck and "
            "configure depends_on with condition: service_healthy.",
        ],
        remediation_steps=[
            [
                "Add a healthcheck to the postgres service using pg_isready",
                "Update depends_on for api to use condition: service_healthy",
                "Review the compose file for hardcoded credentials and move them to a .env file",
                "Verify the api container logs for the specific connection error",
                "Advise the user not to paste full compose files with credentials in tickets",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# dc-106  OCR'd financial report with character confusion
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="dc-106",
        category=Category.SOFTWARE,
        priority=Priority.P2,
        assigned_team=Team.ENTERPRISE_APPS,
        needs_escalation=False,
        missing_information=[MissingInfo.SCREENSHOT_OR_ATTACHMENT, MissingInfo.APPLICATION_VERSION],
        subjects=[
            "OCR scanning producing garbled output in expense reports",
            "Scanned invoices have wrong numbers — OCR character confusion",
            "Financial doc scanning mangling dollar amounts and dates",
        ],
        descriptions=[
            "The OCR module in {app} is producing terrible results on our financial "
            "documents. Here's what it extracted from an invoice:\n\n"
            "CONTOSO CORPORATI0N\n"
            "1nvoice #: INV-2O26-O4l8\n"
            "Dat3: Aprll l8, 2O26\n"
            "Bi11 To: {name}, {department}\n\n"
            "Descripti0n              Qty    Unit Pr1ce    T0tal\n"
            "---------------------------------------------------\n"
            "S0ftware Licens3 (Ent)    l5    $l,2OO.OO    $l8,OOO.OO\n"
            "Pr0fessional Svcs         8O    $25O.OO      $2O,OOO.OO\n"
            "C1oud H0sting (m0nthly)   l2    $3,5OO.OO    $42,OOO.OO\n"
            "---------------------------------------------------\n"
            "Subt0tal:                                     $8O,OOO.OO\n"
            "Tax (8.875%):                                 $7,lOO.OO\n"
            "T0TAL DUE:                                    $87,lOO.OO\n\n"
            "Payment Terms: Net 3O\n"
            "Bank: Fir5t Nati0nal Bank\n"
            "Acc0unt: XXXX-XXXX-{number}\n"
            "R0uting: XXX-XXX-{number}\n\n"
            "The zeros are being read as O's, ones as l's, and some letters are "
            "turning into numbers. This is causing our expense reconciliation to "
            "fail because the amounts don't parse correctly.\n\n{name}, {department}",
            "Scanned Q3 report is full of OCR errors. Sample:\n\n"
            "QUARTERLY FlNANClAL SUMMARY — Q3 2O26\n"
            "Prepared by: {name}, {department}\n\n"
            "Revenue:        $l2,456,789.OO  (prev: $ll,234,567.OO)\n"
            "Operatlng Exp:  $9,876,54l.OO   (prev: $9,l23,456.OO)\n"
            "Net 1nc0me:     $2,58O,248.OO   (prev: $2,lll,lll.OO)\n"
            "EBlTDA:         $3,456,789.OO   (prev: $3,2l2,345.OO)\n\n"
            "The numbers are unusable for import into our {app} accounting system. "
            "We need the OCR engine fixed or replaced.\n\n{name}",
        ],
        next_best_actions=[
            "Investigate the OCR character confusion — zeros/O and ones/l are being "
            "swapped, making financial data unparseable. Focus on the OCR engine "
            "configuration or font recognition settings.",
            "The OCR module needs tuning for financial documents — common 0/O and 1/l "
            "confusion is causing data import failures.",
        ],
        remediation_steps=[
            [
                "Check the OCR engine version and update to the latest release",
                "Enable financial document mode or numeric-context heuristics if available",
                "Test with higher resolution scans (300+ DPI) to improve character recognition",
                "Implement a post-processing step to correct common OCR substitutions (O→0, l→1) in numeric contexts",
                "Consider switching to an OCR engine with better financial document support",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# dc-107  Quoted-printable encoding artifacts
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="dc-107",
        category=Category.SOFTWARE,
        priority=Priority.P3,
        assigned_team=Team.ENTERPRISE_APPS,
        needs_escalation=False,
        missing_information=[MissingInfo.APPLICATION_VERSION, MissingInfo.CONFIGURATION_DETAILS],
        subjects=[
            "Emails showing =20 and =C2=A0 instead of spaces",
            "Support portal displaying quoted-printable garbage in tickets",
            "Ticket descriptions full of =3D and =0A encoding artifacts",
        ],
        descriptions=[
            "Tickets coming from our email integration are showing encoded garbage. "
            "Here's what a recent ticket looks like in {app}:\n\n"
            "Hi IT Support,=0A=0AMy laptop screen is flickering=20whenever I "
            "connect=0Ato the docking station on Floor {floor}.=20=20I=E2=80=99ve "
            "tried=0Adifferent cables but the issue=20persists.=0A=0AThe docking "
            "station=20model is=20Dell WD19S.=20My laptop=0Ais a ThinkPad=20"
            "X1 Carbon Gen=2011.=0A=0ALaptop: {name}=E2=80=99s ThinkPad=0A"
            "OS: Windows=2011=20Enterprise=0ADriver:=20Intel=C2=AE=20"
            "Iris=C2=AE=20Xe=0AMonitor: Dell=20U2722D=0A=0ACould someone "
            "come=20take a look?=0A=0AThanks,=0A{name}=0A{department}",
            "Our ticketing system is not decoding quoted-printable emails. "
            "Example:\n\n"
            "Subject: Re: VPN=20Issue=20=E2=80=93=20Still=20not=20working=0A=0A"
            "I=E2=80=99m=20still=20having=20VPN=20issues.=20Every=20time=20I=20"
            "try=20to=20connect=20from=20home,=20the=20client=20shows=20=E2=80=9C"
            "Authentication=20Failed=E2=80=9D=20after=20about=2030=20seconds.=0A=0A"
            "I=E2=80=99ve=20tried:=0A-=20Reinstalling=20GlobalProtect=0A"
            "-=20Clearing=20credentials=0A-=20Connecting=20on=20a=20different=20"
            "network=0A=0ANone=20of=20this=20worked.=20Please=20help.=0A=0A"
            "{name}=0A{department}\n\n"
            "Every ticket from the email channel looks like this. The web portal "
            "tickets are fine. Can someone fix the email parser?\n\n{name}",
        ],
        next_best_actions=[
            "Fix the email-to-ticket integration — it's not decoding quoted-printable "
            "Content-Transfer-Encoding. The underlying issues (screen flickering, VPN) "
            "should be extracted from the decoded text.",
            "The ticketing system's email parser needs to handle quoted-printable "
            "decoding. Decode the ticket content to identify the actual IT issues.",
        ],
        remediation_steps=[
            [
                "Check the email integration pipeline for missing Content-Transfer-Encoding handling",
                "Update the email parser to decode quoted-printable encoding before storing ticket text",
                "Verify the mail transport agent is passing the correct MIME headers",
                "Re-process recently ingested tickets to decode the garbled content",
                "After fixing the parser, address the underlying user issues (screen flicker, VPN auth failure)",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# dc-108  ServiceNow audit trail / state transitions
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="dc-108",
        category=Category.SOFTWARE,
        priority=Priority.P2,
        assigned_team=Team.ENTERPRISE_APPS,
        needs_escalation=False,
        missing_information=[MissingInfo.PREVIOUS_TICKET_ID, MissingInfo.AFFECTED_SYSTEM],
        subjects=[
            "Ticket keeps bouncing between teams — full audit trail below",
            "INC stuck in reassignment loop — ServiceNow history pasted",
            "Incident ping-ponging for 3 weeks — state transition log inside",
        ],
        descriptions=[
            "This ticket has been bouncing around for three weeks. Here's the full "
            "audit trail from ServiceNow:\n\n"
            "INC{number} — {app} login failure for {name}\n"
            "Created: {date} 08:15:00 by AutoIngest\n\n"
            "State: New → Assigned | {date} 08:15:01 | Assignment Group: Service Desk\n"
            "State: Assigned → In Progress | {date} 09:30:00 | Assigned to: L1-Agent-04\n"
            "Note: 'Looks like an AD account issue. Reassigning to IAM.'\n"
            "State: In Progress → Assigned | {date} 09:31:00 | Assignment Group: IAM Team\n"
            "State: Assigned → In Progress | {date} 14:00:00 | Assigned to: IAM-Agent-02\n"
            "Note: 'AD account is fine. This is an app-specific auth issue. Reassigning.'\n"
            "State: In Progress → Assigned | {date} 14:01:00 | Assignment Group: App Support\n"
            "State: Assigned → In Progress | {date} 08:45:00 | Assigned to: App-Agent-07\n"
            "Note: 'App auth uses SAML federation. This is a network/firewall issue — "
            "SAML endpoint is unreachable. Reassigning.'\n"
            "State: In Progress → Assigned | {date} 08:46:00 | Assignment Group: Network Team\n"
            "State: Assigned → In Progress | {date} 11:20:00 | Assigned to: Net-Agent-03\n"
            "Note: 'Firewall rules are fine. The SAML endpoint resolves but returns 503. "
            "This is an app issue. Reassigning back.'\n"
            "State: In Progress → Assigned | {date} 11:21:00 | Assignment Group: App Support\n"
            "State: Assigned → In Progress | {date} 16:00:00 | Assigned to: App-Agent-12\n"
            "Note: 'The 503 is from the IdP, not our app. Reassigning to IAM.'\n"
            "State: In Progress → Assigned | {date} 16:01:00 | Assignment Group: IAM Team\n"
            "State: Assigned → Pending | {date} 09:00:00 | Reason: Awaiting vendor response\n"
            "Note: 'Opened case with IdP vendor. Waiting for response.'\n"
            "State: Pending → Assigned | {date} 09:00:00 | Reason: Vendor responded\n"
            "Note: 'Vendor says the IdP is healthy. Must be a config issue on our side.'\n"
            "State: Assigned → In Progress | {date} 09:01:00 | Assigned to: IAM-Agent-05\n\n"
            "The user ({name} in {department}) STILL can't log in. Can someone please "
            "actually fix this instead of reassigning it again?\n\n{name}",
            "Please help — my ticket INC{number} has been open for 22 days and "
            "reassigned 8 times. Here's the short version of the audit trail:\n\n"
            "Service Desk → IAM → App Support → Network → App Support → IAM → "
            "Vendor Hold → IAM → ???\n\n"
            "Nobody seems to own this. I just need to log into {app} for my work. "
            "I've been using a colleague's account (I know I shouldn't) because I "
            "have no other choice.\n\n"
            "Floor {floor}, {office} office. {name}, {department}",
        ],
        next_best_actions=[
            "Take ownership of this incident — it has been in a reassignment loop "
            "for 3 weeks. The SAML IdP returns 503; coordinate between IAM and the "
            "app team to diagnose the federation configuration.",
            "Stop the reassignment ping-pong. The root cause is likely a SAML "
            "federation misconfiguration. Assign a single owner to coordinate "
            "cross-team troubleshooting.",
        ],
        remediation_steps=[
            [
                "Assign a single incident owner to coordinate cross-team troubleshooting",
                "Capture a SAML trace (Fiddler or browser dev tools) to identify where authentication fails",
                "Check the IdP federation metadata — certificates may have expired",
                "Verify the SAML assertion consumer service URL matches the app's configuration",
                "Immediately stop the shared account usage and provide the user"
                " with temporary access via an alternative method",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# dc-109  Bloomberg terminal fixed-width output
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="dc-109",
        category=Category.SOFTWARE,
        priority=Priority.P2,
        assigned_team=Team.ENDPOINT,
        needs_escalation=False,
        missing_information=[MissingInfo.DEVICE_INFO, MissingInfo.ERROR_MESSAGE],
        subjects=[
            "Bloomberg terminal not loading market data — screen output pasted",
            "BT display garbled after update — fixed-width output inside",
            "Bloomberg terminal showing stale prices — copied screen below",
        ],
        descriptions=[
            "My Bloomberg terminal is showing stale data. I copied the screen "
            "output to show what I see:\n\n"
            "BLOOMBERG PROFESSIONAL                             {date}  16:42:33\n"
            "═══════════════════════════════════════════════════════════════════\n"
            "EQUITY MONITOR          LAST      CHG    CHG%     BID      ASK\n"
            "───────────────────────────────────────────────────────────────────\n"
            "MSFT US Equity        425.67    +3.42   +0.81   425.65   425.68\n"
            "AAPL US Equity        198.34    -1.23   -0.62   198.32   198.35\n"
            "GOOGL US Equity     2,845.12    +12.45  +0.44  2845.10  2845.14\n"
            "AMZN US Equity      3,412.56    -8.90   -0.26  3412.54  3412.58\n"
            "JPM US Equity         195.78    +2.11   +1.09   195.76   195.80\n"
            "GS US Equity          389.45    +5.67   +1.48   389.43   389.47\n"
            "───────────────────────────────────────────────────────────────────\n"
            "FX RATES              LAST      CHG    CHG%     BID      ASK\n"
            "───────────────────────────────────────────────────────────────────\n"
            "EUR/USD               1.0876   +0.0023 +0.21   1.0875   1.0877\n"
            "GBP/USD               1.2654   -0.0018 -0.14   1.2653   1.2655\n"
            "USD/JPY             154.3200   +0.4500 +0.29  154.3100 154.3300\n"
            "═══════════════════════════════════════════════════════════════════\n"
            "** DATA FEED STATUS: DELAYED (15 MIN) — REAL-TIME FEED ERROR **\n"
            "** CONTACT: BLOOMBERG HELP DESK OR LOCAL IT SUPPORT            **\n"
            "═══════════════════════════════════════════════════════════════════\n\n"
            "The prices are 15 minutes delayed — we need real-time for trading. "
            "This started after IT pushed a network update last night. I'm on the "
            "trading floor, Floor {floor}, {office}.\n\n{name}, {department}",
            "Bloomberg is broken — all my screens show DELAYED data. The B-PIPE "
            "connection seems down. I need real-time data for the {department} desk. "
            "Other terminals on Floor {floor} are also affected.\n\n"
            "Error on the terminal: 'B-PIPE: CONNECTION LOST — FAILOVER TO DELAYED "
            "FEED — CONTACT SUPPORT'\n\n{name}",
        ],
        next_best_actions=[
            "Investigate the Bloomberg real-time data feed failure — the B-PIPE "
            "connection is down and terminals have fallen back to delayed data. "
            "Ignore the pasted market data and focus on the network/feed issue.",
            "The Bloomberg B-PIPE feed lost connectivity after a network change. "
            "Check firewall rules and network routes to the Bloomberg data center.",
        ],
        remediation_steps=[
            [
                "Check if the recent network update affected firewall rules for Bloomberg B-PIPE ports",
                "Verify connectivity to Bloomberg's data center endpoints from the trading floor network segment",
                "Restart the B-PIPE service on the Bloomberg server appliance",
                "Contact Bloomberg support if the connection cannot be re-established",
                "This is high-priority for the trading desk — escalate to network"
                " team immediately if not resolved in 30 minutes",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# dc-110  Excel formula clipboard artifacts
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="dc-110",
        category=Category.SOFTWARE,
        priority=Priority.P3,
        assigned_team=Team.ENTERPRISE_APPS,
        needs_escalation=False,
        missing_information=[MissingInfo.APPLICATION_VERSION, MissingInfo.STEPS_TO_REPRODUCE],
        subjects=[
            "Pasted spreadsheet data looks like formulas instead of values",
            "Excel clipboard artifacts in ticket — formulas showing instead of text",
            "Ticket full of VLOOKUP and IF formulas — meant to paste values",
        ],
        descriptions=[
            "I tried to paste my asset inventory into the ticket but it came out "
            "as formulas instead of values:\n\n"
            "=VLOOKUP(A2,AssetDB!$A:$G,2,FALSE)\t"
            "=VLOOKUP(A2,AssetDB!$A:$G,3,FALSE)\t"
            '=IF(VLOOKUP(A2,AssetDB!$A:$G,5,FALSE)>"2024-01-01","Current","Expired")\t'
            '=IFERROR(INDEX(Warranties!$B:$B,MATCH(A2,Warranties!$A:$A,0)),"N/A")\n'
            "=VLOOKUP(A3,AssetDB!$A:$G,2,FALSE)\t"
            "=VLOOKUP(A3,AssetDB!$A:$G,3,FALSE)\t"
            '=IF(VLOOKUP(A3,AssetDB!$A:$G,5,FALSE)>"2024-01-01","Current","Expired")\t'
            '=IFERROR(INDEX(Warranties!$B:$B,MATCH(A3,Warranties!$A:$A,0)),"N/A")\n'
            "=VLOOKUP(A4,AssetDB!$A:$G,2,FALSE)\t"
            "=VLOOKUP(A4,AssetDB!$A:$G,3,FALSE)\t"
            '=IF(VLOOKUP(A4,AssetDB!$A:$G,5,FALSE)>"2024-01-01","Current","Expired")\t'
            '=IFERROR(INDEX(Warranties!$B:$B,MATCH(A4,Warranties!$A:$A,0)),"N/A")\n\n'
            "What I meant to say: I have 3 laptops that need warranty replacement. "
            "The asset tags are CNT-{number}, CNT-{number}, and CNT-{number}. All "
            "three are ThinkPad X1 Carbons with expired warranties. They're on "
            "Floor {floor} in the {office} office.\n\n{name}, {department}",
            "Sorry about the formatting — I copied from our tracking spreadsheet "
            "and it pasted the formulas:\n\n"
            '=CONCATENATE(B2," - ",C2," (",TEXT(D2,"yyyy-mm-dd"),")")\n'
            '=IF(AND(E2="Active",F2>TODAY()),"OK","NEEDS ATTENTION")\n'
            "=SUMPRODUCT((Users!$A$2:$A$500=A2)*1)\n"
            '=HYPERLINK("https://assets.contoso.com/device/"&A2,"View")\n'
            '=IF(G2>90,"Replace",IF(G2>60,"Monitor","OK"))\n\n'
            "The actual issue: 5 devices in {department} need to be reimaged. "
            "They're running an outdated OS build and can't install the latest "
            "security patches. The devices are all on Floor {floor}. Can someone "
            "schedule the reimaging?\n\n{name}",
        ],
        next_best_actions=[
            "Process the hardware request — ignore the Excel formula artifacts. "
            "The user needs warranty replacements for 3 laptops (or reimaging for "
            "5 devices, depending on variant).",
            "Extract the actual request from behind the clipboard noise: the user "
            "needs device replacements or reimaging. Gather asset tag details.",
        ],
        remediation_steps=[
            [
                "Identify the affected devices by asset tag and verify warranty status in the asset management system",
                "For expired-warranty devices, initiate the hardware replacement workflow",
                "For devices needing reimaging, schedule the OS reimage during off-hours",
                "Ensure the latest security patches are included in the reimage baseline",
                "Advise the user to paste values (Ctrl+Shift+V) instead of formulas in future tickets",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# dc-111  Raw SQL query results pasted with column misalignment
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="dc-111",
        category=Category.DATA,
        priority=Priority.P2,
        assigned_team=Team.DATA_PLATFORM,
        needs_escalation=False,
        missing_information=[MissingInfo.AFFECTED_SYSTEM, MissingInfo.ENVIRONMENT_DETAILS],
        subjects=[
            "Pasted SQL query output is misaligned — can't read the data",
            "Raw SQL results in ticket — columns jumbled and unreadable",
            "Database query dump pasted into ticket with broken formatting",
        ],
        descriptions=[
            "I ran a query to show the affected user accounts and pasted it here "
            "but the columns got mangled:\n\n"
            "user_id    |  display_name           | dept        | last_login          | status  |  lockout_count\n"
            "-----------+-------------------------+-------------+---------------------+---------+---------------\n"
            "40291      |{name}                   |{department} | 2026-04-12 08:14:22 | LOCKED  |            5\n"
            "40292      |R. Montoya                |Finance     | 2026-04-11 17:02:55 | LOCKED  |            3\n"
            "40293      |K. Okonkwo               |{department}| 2026-04-12 09:45:01 | LOCKED  |            8\n"
            "40294      |S. Vasquez                |Legal       | 2026-04-10 11:30:44 | LOCKED  |           12\n"
            "40295      |D. Chen-Ramirez           |{department}| 2026-04-12 10:01:33 | LOCKED  |            4\n"
            "(5 rows affected)\n\n"
            "Query execution time: 0.042s\n"
            "Server: SQLPROD-04.contoso.local\\MSSQLSERVER\n"
            "Database: IdentityStore_Prod\n\n"
            "These 5 accounts are all locked out since this morning. We think it's "
            "related to the password policy change that {department} pushed. They are "
            "all on Floor {floor}. Can someone bulk-unlock them and investigate the "
            "root cause?\n\n{name}, {department}",
            "Pasting the query output from our DB — sorry if the formatting is ugly:\n\n"
            "SELECT s.server_name, s.env, d.db_name, d.size_gb, d.growth_pct, d.last_backup\n"
            "FROM servers s JOIN databases d ON s.id = d.server_id\n"
            "WHERE d.growth_pct > 20 ORDER BY d.growth_pct DESC;\n\n"
            "server_name       env   db_name              size_gb  growth_pct  last_backup\n"
            "SQLPROD-04        PROD  IdentityStore_Prod   842.6    47.2        2026-04-10 02:00\n"
            "SQLPROD-04        PROD  AuditLog_2026        1204.3   38.9        2026-04-09 02:00\n"
            "SQLPROD-07        PROD  TicketingDB_Main     567.1    29.4        2026-04-11 02:00\n"
            "SQLSTG-02         STG   IdentityStore_Stg    312.8    24.6        2026-04-08 02:00\n"
            "SQLDEV-01         DEV   TestHarness          89.4     22.1        NULL\n\n"
            "(5 rows)\n\n"
            "These databases are growing way too fast. The IdentityStore_Prod on "
            "SQLPROD-04 has grown 47% in one month. The audit log is even worse. "
            "We need someone from the data team to investigate before we run out of "
            "disk. I'm in {office}, Floor {floor}.\n\n{name}, {department}",
        ],
        next_best_actions=[
            "Address the underlying database issue — the pasted SQL output is context. "
            "For the account lockout variant, bulk-unlock the 5 affected accounts and "
            "investigate the password policy change. For the disk growth variant, "
            "investigate rapid database growth on SQLPROD-04.",
            "Extract the actionable request from the raw SQL dump. The user needs "
            "either account lockouts resolved or database growth investigated — the "
            "query output is supporting evidence, not the issue itself.",
        ],
        remediation_steps=[
            [
                "Parse the pasted SQL output to identify the affected systems and scope of impact",
                "For account lockouts: bulk-unlock affected accounts and audit the recent password policy change",
                "For database growth: review table-level space usage and identify the largest consumers",
                "Check for missing maintenance jobs (index rebuilds, log truncation, backup schedules)",
                "Set up alerts for abnormal growth rates to catch issues before disk exhaustion",
                "Follow up with the user to confirm resolution and provide a summary of findings",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# dc-112  Embedded Mermaid/PlantUML diagram text
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="dc-112",
        category=Category.SOFTWARE,
        priority=Priority.P3,
        assigned_team=Team.ENTERPRISE_APPS,
        needs_escalation=False,
        missing_information=[MissingInfo.AFFECTED_SYSTEM, MissingInfo.STEPS_TO_REPRODUCE],
        subjects=[
            "Ticket has diagram code instead of an image — Mermaid/PlantUML text",
            "Pasted flowchart markup instead of screenshot of workflow",
            "Can't read the diagram — it's raw Mermaid syntax in the ticket",
        ],
        descriptions=[
            "I'm trying to show the authentication flow that's broken. Here's the "
            "diagram:\n\n"
            "```mermaid\n"
            "sequenceDiagram\n"
            "    participant U as User ({name})\n"
            "    participant APP as {app}\n"
            "    participant IDP as Azure AD\n"
            "    participant MFA as MFA Service\n"
            "    U->>APP: Login request\n"
            "    APP->>IDP: Redirect to /authorize\n"
            "    IDP->>U: Prompt credentials\n"
            "    U->>IDP: Submit credentials\n"
            "    IDP->>MFA: Trigger MFA challenge\n"
            "    MFA-->>IDP: TIMEOUT (no response after 60s)\n"
            "    IDP->>APP: Error: MFA_TIMEOUT\n"
            '    APP->>U: "Authentication failed — contact IT"\n'
            "```\n\n"
            "The MFA step keeps timing out. It worked fine until last week. I'm in "
            "{department} on Floor {floor} and about 15 people on our team are "
            "hitting this same issue. The MFA push notifications never arrive on "
            "our phones.\n\n{name}, {department}",
            "Our deployment pipeline is failing and I mapped it out:\n\n"
            "@startuml\n"
            "start\n"
            ":Developer pushes to main;\n"
            ":Azure DevOps triggers build;\n"
            "if (Build succeeds?) then (yes)\n"
            "  :Run unit tests;\n"
            "  if (Tests pass?) then (yes)\n"
            "    :Deploy to staging;\n"
            "    :Run integration tests;\n"
            "    if (Integration tests pass?) then (yes)\n"
            "      :Deploy to production;\n"
            "      note right: **THIS STEP FAILS**\\n"
            "      Error: ARM deployment timeout\\n"
            "      Resource group: rg-prod-{department}\n"
            "    else (no)\n"
            "      :Rollback staging;\n"
            "    endif\n"
            "  else (no)\n"
            "    :Notify developer;\n"
            "  endif\n"
            "else (no)\n"
            "  :Notify developer;\n"
            "endif\n"
            "stop\n"
            "@enduml\n\n"
            "The production deployment step keeps timing out with an ARM template "
            "error. This has blocked all releases for {department} since Monday. "
            "The staging deploy works fine. We think it's a resource quota issue "
            "in the prod subscription. Office is on Floor {floor}.\n\n{name}",
        ],
        next_best_actions=[
            "Interpret the embedded diagram markup to understand the reported issue. "
            "The MFA variant describes push notification timeouts; the pipeline "
            "variant describes an ARM deployment timeout in production.",
            "The user included a text-based diagram to illustrate their problem. "
            "Extract the failure point and address the underlying issue — MFA "
            "timeout or ARM deployment failure.",
        ],
        remediation_steps=[
            [
                "Parse the diagram text to identify the failure point in the described flow",
                "For MFA timeout: check Azure AD MFA service health and push notification delivery status",
                "For ARM deployment timeout: review resource quotas and deployment logs in the production subscription",
                "Verify recent configuration changes that may have introduced the failure",
                "Test the fix in a lower environment before applying to production",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# dc-113  Windows BSOD crash dump with driver stack
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="dc-113",
        category=Category.HARDWARE,
        priority=Priority.P2,
        assigned_team=Team.ENDPOINT,
        needs_escalation=False,
        missing_information=[MissingInfo.DEVICE_INFO, MissingInfo.REPRODUCTION_FREQUENCY],
        subjects=[
            "Laptop keeps blue-screening — pasted the crash dump info",
            "BSOD with DRIVER_IRQL_NOT_LESS_OR_EQUAL — full dump details inside",
            "Repeated blue screen crashes — driver stack trace attached",
        ],
        descriptions=[
            "My laptop blue-screened again this morning. I wrote down everything "
            "from the screen and the crash dump viewer:\n\n"
            "*** STOP: 0x000000D1 (DRIVER_IRQL_NOT_LESS_OR_EQUAL)\n"
            "*** Faulting module: e1d65x64.sys (Intel Ethernet adapter driver)\n\n"
            "BugCheck D1, {0x0000000000000028, 0x0000000000000002, "
            "0x0000000000000000, 0xFFFFF80B4C2A1E40}\n\n"
            "Stack trace:\n"
            "fffff80b`4c2a1e40 e1d65x64!EthSendPacket+0x140\n"
            "fffff80b`4c2a2200 e1d65x64!EthTransmit+0x80\n"
            "fffff808`05c31a00 NDIS!NdisMIndicateReceiveNetBufferLists+0x120\n"
            "fffff808`05c41f90 NDIS!ndisInterruptDpc+0x1a0\n"
            "fffff808`02e8b100 nt!KiInterruptDispatchNoLockNoEtw+0xb0\n"
            "fffff808`02e66340 nt!KiPageFault+0x440\n\n"
            "DRIVER_INFO:\n"
            "  Driver: e1d65x64.sys\n"
            "  Version: 12.18.9.23\n"
            "  Date: 2024-06-15\n"
            "  Publisher: Intel Corporation\n\n"
            "SYSTEM_INFO:\n"
            "  OS: Windows 11 Enterprise 23H2 (Build 22631.4890)\n"
            "  RAM: 32 GB\n"
            "  Uptime before crash: 2d 14h 22m\n\n"
            "This is the 4th time this week. It always happens when I'm on a Teams "
            "call and docked. I'm on Floor {floor} in {office}.\n\n{name}, {department}",
            "Keeping getting BSODs. Here's what I pulled from Event Viewer and "
            "the minidump:\n\n"
            "Event ID: 1001 (BugCheck)\n"
            "Source: Microsoft-Windows-WER-SystemErrorReporting\n"
            "Parameter 1: 0x0000003b (SYSTEM_SERVICE_EXCEPTION)\n"
            "Parameter 2: 0xFFFFF80B12345678\n"
            "Parameter 3: 0xFFFF920087654321\n"
            "Parameter 4: 0x0000000000000000\n\n"
            "!analyze -v output:\n"
            "MODULE_NAME: nvlddmkm\n"
            "IMAGE_NAME: nvlddmkm.sys\n"
            "IMAGE_VERSION: 31.0.15.5265\n"
            "FAILURE_BUCKET_ID: 0x3B_nvlddmkm!_TDR_TIMEOUT\n"
            "PROCESS_NAME: dwm.exe\n\n"
            "Dump file: C:\\Windows\\Minidump\\041226-14828-01.dmp\n"
            "Dump size: 1,247,632 bytes\n\n"
            "This happens every time I connect to my external monitor through the "
            "dock. The NVIDIA driver seems to crash. I've tried updating the driver "
            "but it still happens. I'm in {department} on Floor {floor}, {office}. "
            "This is seriously affecting my work.\n\n{name}, {department}",
        ],
        next_best_actions=[
            "The user is experiencing repeated BSODs caused by a driver fault. "
            "The crash dump points to either the Intel Ethernet driver (e1d65x64.sys) "
            "or NVIDIA display driver (nvlddmkm.sys). Schedule a driver update or "
            "rollback.",
            "Analyze the BSOD details — the faulting driver is identified in the "
            "crash dump. Update or roll back the offending driver and check for "
            "known firmware/docking station compatibility issues.",
        ],
        remediation_steps=[
            [
                "Identify the faulting driver from the crash dump (e1d65x64.sys or nvlddmkm.sys)",
                "Check for newer driver versions from the hardware vendor's support site",
                "If the latest driver is already installed, roll back to the previous stable version",
                "Update the docking station firmware if applicable",
                "Run Windows Memory Diagnostic to rule out faulty RAM",
                "If crashes continue after driver remediation, schedule hardware diagnostics on the device",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# dc-114  Kubernetes pod describe + events flood
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="dc-114",
        category=Category.SOFTWARE,
        priority=Priority.P2,
        assigned_team=Team.ENTERPRISE_APPS,
        needs_escalation=False,
        missing_information=[MissingInfo.ENVIRONMENT_DETAILS, MissingInfo.CONFIGURATION_DETAILS],
        subjects=[
            "App keeps crashing in Kubernetes — pasted pod describe output",
            "K8s pod in CrashLoopBackOff — full kubectl output inside",
            "Kubernetes deployment failing — events and pod details attached",
        ],
        descriptions=[
            "Our {app} service is down in production. Here's the kubectl output:\n\n"
            "$ kubectl describe pod {app}-api-7b8c4d5f6-x9k2m -n prod\n"
            "Name:         {app}-api-7b8c4d5f6-x9k2m\n"
            "Namespace:    prod\n"
            "Node:         aks-nodepool1-38291045-vmss000004/10.240.0.7\n"
            "Status:       Running\n"
            "IP:           10.244.3.28\n"
            "Containers:\n"
            "  api:\n"
            "    Image:          contosoacr.azurecr.io/{app}-api:v2.14.3\n"
            "    State:          Waiting\n"
            "      Reason:       CrashLoopBackOff\n"
            "    Last State:     Terminated\n"
            "      Reason:       OOMKilled\n"
            "      Exit Code:    137\n"
            "    Limits:\n"
            "      cpu:     500m\n"
            "      memory:  512Mi\n"
            "    Requests:\n"
            "      cpu:     250m\n"
            "      memory:  256Mi\n"
            "Events:\n"
            "  Type     Reason     Age                From               Message\n"
            "  ----     ------     ---                ----               -------\n"
            "  Normal   Scheduled  12m                default-scheduler  Successfully assigned\n"
            "  Normal   Pulled     10m (x4 over 12m)  kubelet            Container image pulled\n"
            "  Normal   Created    10m (x4 over 12m)  kubelet            Created container api\n"
            "  Normal   Started    10m (x4 over 12m)  kubelet            Started container api\n"
            "  Warning  BackOff    2m (x28 over 11m)  kubelet            Back-off restarting failed container\n"
            "  Warning  OOMKilled  3m                 kubelet            Container was OOM killed\n\n"
            "The pod keeps getting OOMKilled after the v2.14.3 deployment. The previous "
            "version (v2.14.2) was fine. This is blocking {department}. I'm {name}, "
            "Floor {floor}.\n\n{name}, {department}",
            "Kubernetes is a mess right now — the new deployment won't come up:\n\n"
            "$ kubectl get pods -n prod -l app={app}\n"
            "NAME                              READY   STATUS             RESTARTS   AGE\n"
            "{app}-web-6f9a8b7c5-abc12         0/1     ImagePullBackOff   0          45m\n"
            "{app}-web-6f9a8b7c5-def34         0/1     ImagePullBackOff   0          45m\n"
            "{app}-web-6f9a8b7c5-ghi56         0/1     ImagePullBackOff   0          45m\n"
            "{app}-web-85d4c6e3f-jkl78         1/1     Running            0          3d\n"
            "{app}-web-85d4c6e3f-mno90         1/1     Running            0          3d\n\n"
            "$ kubectl describe pod {app}-web-6f9a8b7c5-abc12 -n prod\n"
            "Events:\n"
            "  Warning  Failed     2m (x15 over 44m)  kubelet  Failed to pull image "
            '"contosoacr.azurecr.io/{app}-web:v3.1.0": unauthorized: authentication '
            "required\n"
            "  Warning  Failed     2m (x15 over 44m)  kubelet  Error: ImagePullBackOff\n\n"
            "The old pods (v3.0.9) are still running but the new ones can't pull the "
            "image. We think the ACR token expired. This is for the {department} app. "
            "Someone on Floor {floor} needs this ASAP.\n\n{name}",
        ],
        next_best_actions=[
            "The Kubernetes pod output shows the root cause — either OOMKilled "
            "(memory limit too low for v2.14.3) or ImagePullBackOff (expired ACR "
            "credentials). Address the specific failure rather than the noisy kubectl "
            "output.",
            "Extract the failure reason from the pod events: OOMKilled means the "
            "container needs more memory; ImagePullBackOff means the registry "
            "credentials have expired. Fix the underlying issue.",
        ],
        remediation_steps=[
            [
                "Identify the root cause from the pod events (OOMKilled vs ImagePullBackOff)",
                "For OOMKilled: increase the container memory limit in the deployment manifest and redeploy",
                "For ImagePullBackOff: refresh the Azure Container Registry pull secret in the cluster",
                "Verify the fix by checking pod status transitions to Running",
                "If the issue was introduced by a new version, review the release notes for memory regression",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# dc-115  Email with very long URL tracking parameters
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="dc-115",
        category=Category.SOFTWARE,
        priority=Priority.P3,
        assigned_team=Team.ENTERPRISE_APPS,
        needs_escalation=False,
        missing_information=[MissingInfo.ERROR_MESSAGE, MissingInfo.STEPS_TO_REPRODUCE],
        subjects=[
            "Link in ticket is incredibly long — can't tell what it points to",
            "URL with massive tracking parameters — is this link safe to click?",
            "Ticket has a URL that's 2000+ characters with tracking garbage",
        ],
        descriptions=[
            "I got this link from a vendor and when I click it I get an error. "
            "Can you check if it's safe and why it's not working?\n\n"
            "https://portal.vendor-saas.com/dashboard/reports/quarterly?"
            "utm_source=email&utm_medium=notification&utm_campaign=Q3-2026-"
            "executive-summary&utm_content=cta-button-primary&utm_term="
            "quarterly-report&mkt_tok=NTg2LVFIRy0yNjEAAAGSx1234567890abcdef"
            "ghijklmnopqrstuvwxyz1234567890ABCDEFGHIJKLMNOPQRSTUVWXYZ&"
            "tracking_id=a1b2c3d4-e5f6-7890-abcd-ef1234567890&session_ref="
            "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkw"
            "IiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSM"
            "eKKF2QT4fwpMeJf36POk6yJV_adQssw5c&redirect_uri=https%3A%2F%2F"
            "contoso.sharepoint.com%2Fsites%2F{department}%2FShared%2520"
            "Documents%2FReports&nonce=8f14e45fceea167a5a36dedd4bea2543&"
            "state=prod-westus2-{number}\n\n"
            "I need access to the Q3 report for {department}. The link was in an "
            "email from our BI vendor. I'm on Floor {floor}, {office}.\n\n"
            "{name}, {department}",
            "This link keeps breaking when I paste it into our {app} ticketing form. "
            "It gets truncated and then nothing works:\n\n"
            "https://sso.contoso.com/adfs/ls/?wa=wsignin1.0&wtrealm=urn%3A"
            "appproxy%3A{app}&wctx=https%3A%2F%2F{app}.contoso.com%2Fapi%2F"
            "v2%2Fworkflows%2F{number}%2Fsteps%3Fassignee%3D{name}%26"
            "status%3Dpending%26department%3D{department}%26floor%3D{floor}"
            "%26priority%3Dhigh%26include_sub_tasks%3Dtrue%26expand%3D"
            "comments%2Cattachments%2Caudit_trail%26page_size%3D50%26"
            "sort_by%3Dcreated_desc%26filter_date_from%3D2026-01-01%26"
            "filter_date_to%3D2026-04-12%26client_request_id%3D"
            "f47ac10b-58cc-4372-a567-0e02b2c3d479\n\n"
            "Every time I click it the page just shows 'Bad Request — URL too "
            "long'. I need to get to the workflow page for my pending tasks. "
            "This is urgent because I have approvals waiting.\n\n"
            "{name}, {department}",
        ],
        next_best_actions=[
            "The ticket contains extremely long URLs with tracking and session "
            "parameters. Strip the noise to identify the actual destination and "
            "diagnose the access error — likely a URL length limit or truncation issue.",
            "Extract the base URL and essential parameters from the bloated link. "
            "The user needs access to a report or workflow page — the tracking "
            "parameters are irrelevant to the issue.",
        ],
        remediation_steps=[
            [
                "Extract the base URL by stripping tracking parameters (utm_*, mkt_tok, tracking_id)",
                "Test the simplified URL to verify access works without the extra parameters",
                "If the URL exceeds server limits (usually 2048 chars), work with the vendor to provide shorter links",
                "Check if the ADFS or SSO relay is enforcing a URL length limit and adjust if needed",
                "Provide the user with a clean, working link to the resource they need",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# dc-116  Pasted Teams/Slack chat log with timestamps
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="dc-116",
        category=Category.NETWORK,
        priority=Priority.P3,
        assigned_team=Team.NETWORK,
        needs_escalation=False,
        missing_information=[MissingInfo.AFFECTED_USERS, MissingInfo.NETWORK_LOCATION],
        subjects=[
            "Pasted Teams chat as evidence of network issue — wall of messages",
            "Chat transcript from outage — timestamps and all",
            "Copied our Teams channel thread about the Wi-Fi problem",
        ],
        descriptions=[
            "Here's the Teams chat from this morning when the Wi-Fi went down — "
            "wanted to show it's not just me:\n\n"
            "[09:01 AM] {name}: Is the Wi-Fi down for anyone else on Floor {floor}?\n"
            "[09:01 AM] R. Montoya: Yeah, just dropped off a call\n"
            "[09:02 AM] K. Okonkwo: Same here, {office} area. Can't connect at all\n"
            "[09:02 AM] {name}: I'm getting 'No internet, secured' on my laptop\n"
            "[09:03 AM] S. Vasquez: Floor {floor} east wing too. All our devices dropped\n"
            "[09:04 AM] D. Chen: My phone is on Wi-Fi fine but laptop won't connect\n"
            "[09:05 AM] {name}: Tried forgetting the network and reconnecting — no luck\n"
            "[09:06 AM] R. Montoya: Same. Also tried hotspot — that works fine\n"
            "[09:07 AM] K. Okonkwo: The SSID 'Contoso-Corp' doesn't even show up anymore\n"
            "[09:08 AM] L. Johansson: I'm on Floor {floor} too, west wing is fine for me\n"
            "[09:09 AM] {name}: So it's just the east side? {office} and nearby?\n"
            "[09:10 AM] S. Vasquez: Looks like it. Started right at 9 AM\n"
            "[09:12 AM] D. Chen: I rebooted my laptop, still nothing\n"
            "[09:15 AM] {name}: OK I'm submitting a ticket. About 5-6 of us affected\n\n"
            "So the Contoso-Corp SSID is down on Floor {floor}, east wing, around "
            "{office}. Started at 9 AM. About 5-6 people affected. Our hotspots "
            "work fine so it's definitely the office Wi-Fi.\n\n{name}, {department}",
            "Copying the Slack thread from our channel so you can see the timeline:\n\n"
            "[2026-04-12 14:22] {name}: Teams calls keep dropping. Anyone else?\n"
            "[2026-04-12 14:23] A. Williams: Yes! I've been kicked from 3 calls today\n"
            "[2026-04-12 14:24] {name}: Running a speed test... 2 Mbps down, 0.5 up. "
            "Should be 100+\n"
            "[2026-04-12 14:25] M. Petrov: Same from my desk. Terrible latency too\n"
            "[2026-04-12 14:27] {name}: tracert to teams.microsoft.com shows 400ms "
            "hops inside our own network\n"
            "[2026-04-12 14:28] A. Williams: Wired is just as bad. Not a Wi-Fi issue\n"
            "[2026-04-12 14:30] {name}: Checked with Floor {floor} south — they're fine. "
            "It's just our segment\n"
            "[2026-04-12 14:33] M. Petrov: Started around 2 PM. Right after that "
            "maintenance window maybe?\n"
            "[2026-04-12 14:35] {name}: Yeah the network team had a change window "
            "12-2 PM today\n\n"
            "We're getting terrible throughput and latency on our network segment "
            "since the maintenance window today. Floor {floor}, {office} area, "
            "both wired and wireless. Teams calls are unusable.\n\n"
            "{name}, {department}",
        ],
        next_best_actions=[
            "The chat log shows a localized network outage. For the Wi-Fi variant, "
            "the Contoso-Corp SSID is down on one wing of Floor {floor}. For the "
            "throughput variant, a maintenance window may have misconfigured the "
            "network segment.",
            "Extract the network issue from the chat noise: either a Wi-Fi access "
            "point failure on the east wing or post-maintenance throughput "
            "degradation on a specific floor segment.",
        ],
        remediation_steps=[
            [
                "Identify the affected network segment from the user-reported location (floor, wing, office)",
                "Check access point status for the affected area — look for offline or degraded APs",
                "If a recent maintenance window occurred, review the change log for misconfigurations",
                "Test connectivity from the affected segment to rule out upstream switch or VLAN issues",
                "Restore service and notify affected users once the issue is resolved",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# dc-117  LaTeX/math notation in technical request
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="dc-117",
        category=Category.SOFTWARE,
        priority=Priority.P3,
        assigned_team=Team.ENTERPRISE_APPS,
        needs_escalation=False,
        missing_information=[MissingInfo.APPLICATION_VERSION, MissingInfo.ENVIRONMENT_DETAILS],
        subjects=[
            "Ticket has LaTeX math formulas — hard to read the actual request",
            "Technical request with math notation mixed in",
            "Request buried in LaTeX equations and symbols",
        ],
        descriptions=[
            "We need to update the scoring algorithm in {app}. The current formula "
            "is wrong. Here's what it should be:\n\n"
            "The risk score $R$ for each asset should be computed as:\n\n"
            "$$R_i = \\sum_{{j=1}}^{{n}} w_j \\cdot f_j(x_{{ij}}) + "
            "\\lambda \\|\\mathbf{{w}}\\|_2^2$$\n\n"
            "where $f_j$ is the feature transform:\n\n"
            "$$f_j(x) = \\frac{{1}}{{1 + e^{{-\\alpha_j(x - \\mu_j)}}}}$$\n\n"
            "Currently the system uses a simple linear model:\n\n"
            "$$R_i^{{\\text{{old}}}} = \\sum_{{j=1}}^{{n}} w_j \\cdot x_{{ij}}$$\n\n"
            "which doesn't account for the nonlinear relationship between "
            "vulnerability count ($x_1$), exposure time ($x_2 \\in [0, \\infty)$), "
            "and CVSS score ($x_3 \\in [0, 10]$).\n\n"
            "The regularization parameter $\\lambda = 0.01$ prevents overfitting. "
            "We validated this on the {department} dataset and the RMSE dropped from "
            "$4.23$ to $1.87$.\n\n"
            "Can the {app} team implement this? We need it for the Q3 security "
            "review. I'm on Floor {floor}, {office}.\n\n{name}, {department}",
            "The threshold calculation in our monitoring tool is wrong. It should "
            "use exponential smoothing, not a simple average:\n\n"
            "$$\\hat{{y}}_{{t+1}} = \\alpha y_t + (1 - \\alpha) \\hat{{y}}_t, "
            "\\quad \\alpha \\in (0, 1]$$\n\n"
            "For anomaly detection, flag when:\n\n"
            "$$|y_t - \\hat{{y}}_t| > k \\cdot \\sigma_t$$\n\n"
            "where $\\sigma_t$ is the rolling standard deviation:\n\n"
            "$$\\sigma_t = \\sqrt{{\\frac{{1}}{{N-1}} \\sum_{{i=t-N}}^{{t-1}} "
            "(y_i - \\bar{{y}})^2}}$$\n\n"
            "Right now {app} just uses $|y_t - \\bar{{y}}| > 2\\sigma$ with a "
            "global mean $\\bar{{y}}$ and a fixed $\\sigma$, which misses trends "
            "and causes false alerts. We're getting ~200 false positives per day "
            "in {department}.\n\n"
            "Please update the alerting engine. Contact me at Floor {floor}, "
            "{office}.\n\n{name}, {department}",
        ],
        next_best_actions=[
            "The user is requesting an algorithm change in the application. The "
            "LaTeX notation describes the desired formula. Translate the math into "
            "a product feature request and route to the development team.",
            "Extract the feature request from the mathematical notation: the user "
            "wants a more sophisticated scoring/alerting algorithm. This is a "
            "development request, not a break-fix issue.",
        ],
        remediation_steps=[
            [
                "Translate the LaTeX formulas into a clear product requirement specification",
                "Create a feature request or change request in the backlog for the application team",
                "Validate the mathematical approach with the data science or engineering team",
                "Plan implementation with appropriate testing on staging before production rollout",
                "Follow up with the requester to confirm the specification matches their intent",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# dc-118  ARM template / Bicep JSON config dump
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="dc-118",
        category=Category.SOFTWARE,
        priority=Priority.P2,
        assigned_team=Team.ENTERPRISE_APPS,
        needs_escalation=False,
        missing_information=[MissingInfo.ERROR_MESSAGE, MissingInfo.ENVIRONMENT_DETAILS],
        subjects=[
            "ARM template deployment failing — full JSON config inside",
            "Bicep/ARM config dump pasted — deployment error somewhere in here",
            "Azure deployment broken — pasted the entire ARM template",
        ],
        descriptions=[
            "Our ARM template deployment keeps failing. Here's the template — can "
            "someone spot what's wrong?\n\n"
            "{{\n"
            '  "$schema": "https://schema.management.azure.com/schemas/'
            '2019-04-01/deploymentTemplate.json#",\n'
            '  "contentVersion": "1.0.0.0",\n'
            '  "parameters": {{\n'
            '    "appServicePlanName": {{ "type": "string", '
            '"defaultValue": "asp-{app}-prod" }},\n'
            '    "webAppName": {{ "type": "string", '
            '"defaultValue": "{app}-webapp-prod" }},\n'
            '    "location": {{ "type": "string", '
            '"defaultValue": "[resourceGroup().location]" }},\n'
            '    "sku": {{ "type": "string", "defaultValue": "P1v3" }}\n'
            "  }},\n"
            '  "resources": [\n'
            "    {{\n"
            '      "type": "Microsoft.Web/serverfarms",\n'
            '      "apiVersion": "2022-09-01",\n'
            '      "name": "[parameters(\'appServicePlanName\')]",\n'
            '      "location": "[parameters(\'location\')]",\n'
            '      "sku": {{ "name": "[parameters(\'sku\')]" }},\n'
            '      "kind": "linux",\n'
            '      "properties": {{ "reserved": true }}\n'
            "    }},\n"
            "    {{\n"
            '      "type": "Microsoft.Web/sites",\n'
            '      "apiVersion": "2022-09-01",\n'
            '      "name": "[parameters(\'webAppName\')]",\n'
            '      "location": "[parameters(\'location\')]",\n'
            '      "dependsOn": [\n'
            "        \"[resourceId('Microsoft.Web/serverfarms', "
            "parameters('appServicePlanName'))]\"\n"
            "      ],\n"
            '      "properties": {{\n'
            '        "serverFarmId": "[resourceId(\'Microsoft.Web/serverfarms\', '
            "parameters('appServicePlanName'))]\",\n"
            '        "siteConfig": {{\n'
            '          "linuxFxVersion": "PYTHON|3.11",\n'
            '          "alwaysOn": true,\n'
            '          "appSettings": [\n'
            '            {{ "name": "SCM_DO_BUILD_DURING_DEPLOYMENT", '
            '"value": "true" }}\n'
            "          ]\n"
            "        }}\n"
            "      }}\n"
            "    }}\n"
            "  ]\n"
            "}}\n\n"
            "The deployment error says: 'InvalidTemplateDeployment — The template "
            "deployment failed because of policy violation.' We're trying to deploy "
            "the {app} app for {department}. I'm on Floor {floor}.\n\n"
            "{name}, {department}",
            "Bicep deployment is broken. Here's the relevant section:\n\n"
            "param location string = resourceGroup().location\n"
            "param envName string = 'prod'\n\n"
            "@description('Storage account for {app} application data')\n"
            "resource storageAccount 'Microsoft.Storage/storageAccounts@"
            "2023-01-01' = {{\n"
            "  name: 'st{app}${{envName}}001'\n"
            "  location: location\n"
            "  kind: 'StorageV2'\n"
            "  sku: {{ name: 'Standard_LRS' }}\n"
            "  properties: {{\n"
            "    minimumTlsVersion: 'TLS1_2'\n"
            "    supportsHttpsTrafficOnly: true\n"
            "    allowBlobPublicAccess: false\n"
            "    networkAcls: {{\n"
            "      defaultAction: 'Deny'\n"
            "      bypass: 'AzureServices'\n"
            "    }}\n"
            "  }}\n"
            "}}\n\n"
            "resource keyVault 'Microsoft.KeyVault/vaults@2023-07-01' = {{\n"
            "  name: 'kv-{app}-${{envName}}'\n"
            "  location: location\n"
            "  properties: {{\n"
            "    sku: {{ family: 'A', name: 'standard' }}\n"
            "    tenantId: subscription().tenantId\n"
            "    enableSoftDelete: true\n"
            "    softDeleteRetentionInDays: 90\n"
            "    enablePurgeProtection: true\n"
            "  }}\n"
            "}}\n\n"
            "Error: 'StorageAccountNameTooLong — Storage account name must be "
            "between 3 and 24 characters.' Also getting a policy violation on the "
            "Key Vault — something about missing private endpoint. This is for "
            "{department}'s environment. Floor {floor}, {office}.\n\n{name}",
        ],
        next_best_actions=[
            "The user pasted infrastructure-as-code templates with deployment errors. "
            "The ARM template has a policy violation; the Bicep template has a naming "
            "length issue and missing private endpoint. Focus on the deployment errors.",
            "Diagnose the infrastructure deployment failures from the pasted config: "
            "check Azure Policy compliance, resource naming conventions, and required "
            "networking configurations.",
        ],
        remediation_steps=[
            [
                "Review the deployment error messages for specific policy violations or validation failures",
                "For naming errors, ensure resource names comply with Azure naming rules and length limits",
                "Check Azure Policy assignments on the target subscription for compliance requirements",
                "For private endpoint violations, add the required private endpoint and DNS zone resources",
                "Test the corrected template in a development resource group before deploying to production",
                "Share the corrected template with the user and confirm successful deployment",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# dc-119  Git merge conflict markers in pasted code
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="dc-119",
        category=Category.SOFTWARE,
        priority=Priority.P3,
        assigned_team=Team.ENTERPRISE_APPS,
        needs_escalation=False,
        missing_information=[MissingInfo.STEPS_TO_REPRODUCE, MissingInfo.ENVIRONMENT_DETAILS],
        subjects=[
            "Code has merge conflict markers — can't tell which version is correct",
            "Git conflict markers in pasted config — need help resolving",
            "Pasted code with <<<<<<< and >>>>>>> conflict markers",
        ],
        descriptions=[
            "Our {app} deployment config broke after a merge. I'm not sure which "
            "version is correct — here's what's in the file:\n\n"
            "# {app} production configuration\n"
            "server:\n"
            "  host: 0.0.0.0\n"
            "<<<<<<< HEAD\n"
            "  port: 8443\n"
            "  ssl: true\n"
            "  cert_path: /etc/ssl/{app}/prod.crt\n"
            "  key_path: /etc/ssl/{app}/prod.key\n"
            "  tls_version: '1.3'\n"
            "=======\n"
            "  port: 8080\n"
            "  ssl: false\n"
            "  # SSL terminated at load balancer\n"
            ">>>>>>> feature/lb-ssl-offload\n"
            "database:\n"
            "  host: sqlprod-{number}.contoso.local\n"
            "<<<<<<< HEAD\n"
            "  pool_size: 20\n"
            "  timeout: 30\n"
            "  ssl_mode: require\n"
            "=======\n"
            "  pool_size: 50\n"
            "  timeout: 60\n"
            "  ssl_mode: verify-full\n"
            "  ssl_ca: /etc/ssl/db-ca.crt\n"
            ">>>>>>> feature/db-pool-increase\n\n"
            "The app won't start because the YAML is invalid with these conflict "
            "markers in it. Someone merged without resolving them. We need the right "
            "config for production — the app has been down for 20 minutes. "
            "Floor {floor}, {office}.\n\n{name}, {department}",
            "I'm getting errors in our CI/CD pipeline and the config file has merge "
            "conflicts nobody resolved:\n\n"
            "// {app} API route configuration\n"
            "const routes = {{\n"
            "  auth: {{\n"
            "<<<<<<< HEAD\n"
            "    endpoint: '/api/v2/auth',\n"
            "    timeout: 5000,\n"
            "    retries: 3,\n"
            "    provider: 'azure-ad',\n"
            "=======\n"
            "    endpoint: '/api/v3/auth',\n"
            "    timeout: 10000,\n"
            "    retries: 5,\n"
            "    provider: 'okta',\n"
            ">>>>>>> feature/okta-migration\n"
            "  }},\n"
            "  data: {{\n"
            "<<<<<<< HEAD\n"
            "    endpoint: '/api/v2/data',\n"
            "    cache_ttl: 300,\n"
            "=======\n"
            "    endpoint: '/api/v3/data',\n"
            "    cache_ttl: 600,\n"
            "    compression: true,\n"
            ">>>>>>> feature/api-v3-upgrade\n"
            "  }}\n"
            "}};\n\n"
            "The build is failing because of the conflict markers. This is blocking "
            "all deployments for {department}. We need someone who knows the intended "
            "config to fix this.\n\n{name}, {department}",
        ],
        next_best_actions=[
            "The pasted code contains unresolved Git merge conflict markers causing "
            "build/startup failures. Determine the correct resolution for each "
            "conflict block and apply the fix to unblock the deployment.",
            "Resolve the merge conflicts in the configuration file. Identify the "
            "intended production values by consulting the team or reviewing the "
            "feature branch purposes, then commit the corrected file.",
        ],
        remediation_steps=[
            [
                "Identify all conflict markers (<<<<<<, =======, >>>>>>>) in the affected files",
                "Consult with the development team to determine the correct resolution for each conflict",
                "Remove the conflict markers and apply the correct configuration values",
                "Validate the resolved file (YAML lint, JSON parse, or syntax check as appropriate)",
                "Commit the resolved file and redeploy the application",
                "Add branch protection rules or pre-merge checks to prevent unresolved conflicts in the future",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# dc-120  macOS crash report (CrashReporter format)
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="dc-120",
        category=Category.SOFTWARE,
        priority=Priority.P2,
        assigned_team=Team.ENTERPRISE_APPS,
        needs_escalation=False,
        missing_information=[MissingInfo.DEVICE_INFO, MissingInfo.REPRODUCTION_FREQUENCY],
        subjects=[
            "macOS app keeps crashing — pasted the crash report",
            "CrashReporter log from Mac — app quits unexpectedly every time",
            "Repeated macOS crash — full crash report inside",
        ],
        descriptions=[
            "{app} keeps crashing on my Mac. Here's the crash report that pops up:\n\n"
            "Process:               {app} [1842]\n"
            "Path:                  /Applications/{app}.app/Contents/MacOS/{app}\n"
            "Identifier:            com.contoso.{app}\n"
            "Version:               4.2.1 (4210)\n"
            "Code Type:             ARM-64 (Native)\n"
            "Parent Process:        launchd [1]\n\n"
            "Date/Time:             2026-04-12 10:23:45.123 -0400\n"
            "OS Version:            macOS 15.4 (24E248)\n"
            "Report Version:        12\n\n"
            "Exception Type:        EXC_BAD_ACCESS (SIGSEGV)\n"
            "Exception Codes:       KERN_INVALID_ADDRESS at 0x0000000000000010\n"
            "Exception Note:        EXC_CORPSE_NOTIFY\n\n"
            "Termination Reason:    Namespace SIGNAL, Code 11 Segmentation fault: 11\n\n"
            "Thread 0 Crashed:\n"
            "0   libsqlite3.dylib                0x1a2b3c4d5 sqlite3_step + 124\n"
            "1   com.contoso.{app}               0x1001a2b3c "
            "-[DBManager executeQuery:] + 88\n"
            "2   com.contoso.{app}               0x1001b4c5d "
            "-[SyncEngine performSync:] + 244\n"
            "3   com.contoso.{app}               0x1001c6d7e "
            "-[AppDelegate applicationDidBecomeActive:] + 56\n"
            "4   AppKit                           0x1a3b4c5d6 "
            "-[NSApplication _handleApplicationActivation:] + 180\n\n"
            "Thread 1:\n"
            "0   libsystem_kernel.dylib           0x1a4c5d6e7 __psynch_cvwait + 8\n"
            "1   libsystem_pthread.dylib          0x1a5d6e7f8 _pthread_cond_wait + 64\n\n"
            "Binary Images:\n"
            "       0x100000000 -        0x1003fffff  com.contoso.{app} (4.2.1) "
            "</usr/local/bin/{app}>\n"
            "       0x1a0000000 -        0x1a00ffffff  libsqlite3.dylib (*) "
            "<...>\n\n"
            "It crashes every time I open the app. The sync runs on launch and "
            "immediately segfaults. I'm in {department}, Floor {floor}, {office}. "
            "I need this app for my daily work.\n\n{name}, {department}",
            "My Mac keeps showing the crash reporter for {app}. Pasting the key "
            "parts:\n\n"
            "Process:               {app} Helper (Renderer) [2456]\n"
            "Path:                  /Applications/{app}.app/Contents/Frameworks/"
            "{app} Helper (Renderer).app/Contents/MacOS/{app} Helper (Renderer)\n"
            "Identifier:            com.contoso.{app}.helper.renderer\n"
            "Version:               4.2.1 (4210)\n"
            "Code Type:             ARM-64 (Native)\n\n"
            "Date/Time:             2026-04-12 14:10:33.456 -0400\n"
            "OS Version:            macOS 15.4 (24E248)\n\n"
            "Exception Type:        EXC_RESOURCE (RESOURCE_TYPE_MEMORY)\n"
            "Exception Subtype:     MEMORY_LIMIT_EXCEEDED\n"
            "Exception Note:        EXC_CORPSE_NOTIFY\n"
            "Termination Reason:    Jetsam — per-process memory limit exceeded\n\n"
            "Memory footprint at termination: 4.1 GB (limit: 4.0 GB)\n"
            "Memory pages:\n"
            "  Resident: 1,048,576 pages (4.0 GB)\n"
            "  Swapped:  262,144 pages (1.0 GB)\n\n"
            "Largest allocations:\n"
            "  com.contoso.{app}.helper.renderer: 3.2 GB\n"
            "    - ImageCache:        1.8 GB\n"
            "    - DOM:               0.9 GB\n"
            "    - JavaScript heap:   0.5 GB\n\n"
            "This happens after {app} has been open for about 2 hours. It uses "
            "more and more memory until macOS kills it. I have 16 GB RAM but the "
            "app alone takes 4+ GB. I'm in {department}, Floor {floor}.\n\n"
            "{name}, {department}",
        ],
        next_best_actions=[
            "The macOS crash report identifies the failure: either a segfault in "
            "the SQLite sync path or a memory limit exceeded in the renderer. "
            "Escalate to the application team with the crash details.",
            "Analyze the CrashReporter output to identify the root cause — a null "
            "pointer dereference during sync or a memory leak in the renderer — "
            "and work with the app vendor on a fix or workaround.",
        ],
        remediation_steps=[
            [
                "Extract the crash type and faulting module from the crash report",
                "For segfault crashes: check if the local database is corrupted and attempt a rebuild",
                "For memory limit crashes: clear the application cache and restart to reclaim memory",
                "Check for available application updates that address the specific crash signature",
                "If no update is available, report the crash to the application vendor with the full crash log",
                "Provide the user with a workaround (restart app periodically, disable auto-sync on launch)",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# dc-121  CSV data pasted inline — column alignment noise
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="dc-121",
        category=Category.ACCESS_AUTH,
        priority=Priority.P3,
        assigned_team=Team.IAM,
        needs_escalation=False,
        missing_information=[MissingInfo.AFFECTED_USERS, MissingInfo.AFFECTED_SYSTEM],
        subjects=[
            "Bulk user provisioning failing — CSV pasted below",
            "User account creation errors — see attached data",
            "AD sync issues for new hires — raw CSV included",
        ],
        descriptions=[
            "We ran a bulk provisioning import for {department} and about half the "
            "accounts failed. I'm pasting the CSV so you can see what went wrong:\n\n"
            "EmployeeID,FirstName,LastName,Email,Department,Office,StartDate,Manager,"
            "Title,CostCenter,AccessLevel\n"
            "10231,Alice,Martinez,alice.martinez@contoso.com,{department},{office},"
            "2026-06-01,{name},Senior Analyst,CC-4420,Standard\n"
            "10232,Bob,Nakamura,bob.nakamura@contoso.com,{department},{office},"
            "2026-06-01,{name},Data Engineer,CC-4420,Standard\n"
            "10233,Carla,O'Brien,carla.obrien@contoso.com,{department},{office},"
            "2026-06-01,{name},Project Manager,CC-4420,Elevated\n"
            "10234,Dmitri,Volkov,dmitri.volkov@contoso.com,{department},{office},"
            "2026-06-01,{name},DevOps Lead,CC-4420,Admin\n"
            "10235,,Washington,,{department},{office},2026-06-01,{name},Intern,"
            "CC-4420,Standard\n"
            "10236,Fatima,Al-Rashid,fatima.al-rashid@contoso.com,{department},"
            "{office},2026-06-01,{name},QA Engineer,CC-4420,Standard\n"
            "10237,George,Papandreou,george.papandreou@contoso.com,{department},"
            "{office},06/01/2026,{name},Business Analyst,CC-4420,Standard\n"
            "10238,Hana,Kim,hana.kim@contoso.com,{department},{office},2026-06-01,"
            "{name},UX Designer,CC-4420,Standard\n"
            "10239,Ivan,Petrov,ivan.petrov@contoso.com,{department},{office},"
            "2026-06-01,,Staff Engineer,CC-4420,Elevated\n"
            "10240,Julia,Santos,julia.santos@contoso.com,{department},{office},"
            "2026-06-01,{name},Technical Writer,CC-4420,Standard\n\n"
            "Rows 10235, 10237, and 10239 seem off — missing names, wrong date "
            "format, no manager. Can you fix the import?\n\n{name}, {department}",
            "Hi — the new-hire provisioning batch for {department} had errors. "
            "Here's the raw data I submitted:\n\n"
            "EmployeeID|FirstName|LastName|Email|Department|Office|StartDate|"
            "Manager|Title|CostCenter|AccessLevel\n"
            "10241|Kevin|Adebayo|kevin.adebayo@contoso.com|{department}|{office}|"
            "2026-06-15|{name}|Security Analyst|CC-5510|Elevated\n"
            "10242|Lena|Johansson|lena.johansson@contoso.com|{department}|{office}|"
            "2026-06-15|{name}|Cloud Architect|CC-5510|Admin\n"
            "10243|Miguel|Fernandez|miguel.fernandez@contoso.com|{department}|"
            "{office}|2026-06-15|{name}|Support Engineer|CC-5510|Standard\n"
            "10244|Nina||nina.@contoso.com|{department}|{office}|2026-06-15|{name}|"
            "Program Manager|CC-5510|Elevated\n"
            "10245|Oscar|Chen|oscar.chen@contoso.com|{department}|{office}|"
            "15-Jun-2026|{name}|ML Engineer|CC-5510|Admin\n"
            "10246|Priya|Sharma|priya.sharma@contoso.com|{department}|{office}|"
            "2026-06-15|{name}|Data Scientist|CC-5510|Standard\n\n"
            "Some rows have missing last names or malformed email addresses. "
            "The import script rejected them all as a batch. Can you re-run just "
            "the valid ones and tell me which ones need corrections?\n\n"
            "{name}, {department}",
        ],
        next_best_actions=[
            "Parse the pasted CSV to identify rows with data quality issues — "
            "missing required fields, inconsistent date formats, and malformed "
            "email addresses. Fix the valid rows and request corrections for the rest.",
            "Validate the bulk provisioning data, correct the formatting issues "
            "(date formats, missing fields, malformed emails), and re-run the "
            "import for the clean rows while flagging the broken ones.",
        ],
        remediation_steps=[
            [
                "Extract the CSV data and validate each row against the provisioning schema",
                "Identify specific errors: missing FirstName/LastName, malformed emails, inconsistent date formats",
                "Correct fixable issues (e.g., normalize dates to ISO 8601 format)",
                "Re-run the import for validated rows",
                "Send the user a list of rows that still need manual correction with specific error details",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# dc-122  Extremely long tracking URLs cluttering the ticket
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="dc-122",
        category=Category.DATA,
        priority=Priority.P3,
        assigned_team=Team.DATA_PLATFORM,
        needs_escalation=False,
        missing_information=[MissingInfo.ERROR_MESSAGE, MissingInfo.STEPS_TO_REPRODUCE],
        subjects=[
            "Analytics dashboard links broken — URLs below",
            "Tracking links redirecting to 404 — see examples",
            "Data pipeline report links not resolving",
        ],
        descriptions=[
            "Several of our analytics dashboard links stopped working after the "
            "domain migration. I'm pasting the full URLs so you can see the "
            "tracking parameters:\n\n"
            "https://analytics.contoso.com/dashboards/v2/view?report_id=a8f3c291-"
            "4e67-4b2a-9d1f-3c8e7a5b0d42&workspace=prod-{department}-analytics&"
            "tenant=contoso-corp&session=eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9."
            "eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiYWRtaW4iOnRydW"
            "UsImlhdCI6MTcxNjIzOTAyMn0&utm_source=internal&utm_medium=email&"
            "utm_campaign=weekly_report_2026w23&utm_content=dashboard_link_primary&"
            "redirect_chain=aHR0cHM6Ly9vbGQuYW5hbHl0aWNzLmNvbnRvc28uY29tL3YxL3Jl"
            "cG9ydHM&fallback=https%3A%2F%2Fanalytics.contoso.com%2Flegacy%2F"
            "redirect%3Fid%3Da8f3c291&ts=1719532800&sig=hmac-sha256%3A"
            "9f86d081884c7d659a2feaa0c55ad015a3bf4f1b2b0b822cd15d6c15b0f00a08\n\n"
            "https://analytics.contoso.com/dashboards/v2/view?report_id=b7e2d180-"
            "5f78-4c3b-ae20-4d9f8b6c1e53&workspace=prod-{department}-analytics&"
            "tenant=contoso-corp&session=eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9."
            "eyJzdWIiOiI5ODc2NTQzMjEwIiwibmFtZSI6IkphbmUgU21pdGgiLCJhZG1pbiI6Zm"
            "Fsc2UsImlhdCI6MTcxNjIzOTAyMn0&utm_source=internal&utm_medium=email&"
            "utm_campaign=weekly_report_2026w23&utm_content=dashboard_link_secondary&"
            "redirect_chain=aHR0cHM6Ly9vbGQuYW5hbHl0aWNzLmNvbnRvc28uY29tL3YxL3Jl"
            "cG9ydHM&fallback=https%3A%2F%2Fanalytics.contoso.com%2Flegacy%2F"
            "redirect%3Fid%3Db7e2d180&ts=1719532800&sig=hmac-sha256%3A"
            "d7a8fbb307d7809469ca9abcb0082e4f8d5651e46d3cdb762d02d0bf37c9e592\n\n"
            "Both give a 404 now. They worked last week. I need these for the "
            "{department} weekly review.\n\n{name}, {department}",
            "Hi, our data platform report URLs are broken. They all have long "
            "tracking chains and I don't know which part is the real link:\n\n"
            "https://data.contoso.com/reports/pipeline-status?run_id=c6d4e093-"
            "7a89-4d1c-bf31-5e0a9c7d2f64&env=production&region=eastus2&"
            "trace_id=00-4bf92f3577b34da6a3ce929d0e0e4736-00f067aa0ba902b7-01&"
            "parent_span=a1b2c3d4e5f60718&baggage=userId%3D{name}%2C"
            "department%3D{department}%2Cfloor%3D{floor}&callback=https%3A%2F%2F"
            "hooks.contoso.com%2Fnotify%3Ftoken%3Dxoxb-123456789012-"
            "1234567890123-AbCdEfGhIjKlMnOpQrStUvWx&format=json&"
            "include_metrics=true&lookback=7d&granularity=hourly\n\n"
            "When I click it I get 'Resource not found'. The pipeline ran "
            "successfully — I can see the run in the logs. I just can't access "
            "the report through this URL anymore.\n\n{name}, {department}",
        ],
        next_best_actions=[
            "The tracking URLs contain stale session tokens and redirect chains "
            "from the old analytics domain. Strip the session and redirect "
            "parameters and reconstruct the direct dashboard links.",
            "Identify which URL parameters are essential (report_id, workspace) "
            "and which are stale tracking artifacts. Provide the user with "
            "clean, direct links to the reports.",
        ],
        remediation_steps=[
            [
                "Parse the URLs to extract the core report identifiers (report_id, workspace, run_id)",
                "Verify the reports exist on the new analytics platform using the extracted IDs",
                "Reconstruct clean URLs without stale session tokens, redirect chains, and UTM parameters",
                "Update any bookmarks or scheduled email links to use the new direct URLs",
                "Advise the user to regenerate shareable links from the dashboard UI to avoid stale tokens",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# dc-123  RTF/Word conversion artifacts in ticket body
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="dc-123",
        category=Category.HARDWARE,
        priority=Priority.P3,
        assigned_team=Team.ENDPOINT,
        needs_escalation=False,
        missing_information=[MissingInfo.DEVICE_INFO, MissingInfo.ERROR_MESSAGE],
        subjects=[
            "Printer producing garbled output — formatting details inside",
            "Document prints with strange characters after Word update",
            "Print jobs corrupted — RTF artifacts in output",
        ],
        descriptions=[
            "Ever since the last Word update my print jobs come out garbled. "
            "I copied the print preview text and it shows this:\n\n"
            "{\\rtf1\\ansi\\ansicpg1252\\deff0\\nouicompat{\\fonttbl{\\f0\\fswiss"
            "\\fprq2\\fcharset0 Calibri;}{\\f1\\fmodern\\fprq1\\fcharset0 "
            "Consolas;}}\n"
            "{\\colortbl ;\\red0\\green0\\blue0;\\red44\\green62\\blue80;}\n"
            "{\\*\\generator Riched20 10.0.22621}\\viewkind4\\uc1\n"
            "\\pard\\widctlpar\\sa200\\sl276\\slmult1\\cf1\\f0\\fs22 "
            "Quarterly Budget Report — {department}\\par\n"
            "\\pard\\widctlpar\\li720\\sa120\\cf2\\f1\\fs18 "
            "FY2026 Q2 Actuals vs. Forecast\\par\n"
            "\\trowd\\trgaph108\\trleft-108\\trbrdrt\\brdrs\\brdrw10 "
            "\\trbrdrl\\brdrs\\brdrw10 \\trbrdrb\\brdrs\\brdrw10 "
            "\\trbrdrr\\brdrs\\brdrw10\n"
            "\\clbrdrt\\brdrs\\brdrw10\\clbrdrl\\brdrs\\brdrw10"
            "\\clbrdrb\\brdrs\\brdrw10\\clbrdrr\\brdrs\\brdrw10 "
            "\\cellx3000\n"
            "\\clbrdrt\\brdrs\\brdrw10\\clbrdrl\\brdrs\\brdrw10"
            "\\clbrdrb\\brdrs\\brdrw10\\clbrdrr\\brdrs\\brdrw10 "
            "\\cellx6000\n"
            "\\pard\\intbl\\widctlpar Revenue\\cell \\$4,230,000\\cell\\row\n"
            "\\pard\\intbl\\widctlpar COGS\\cell \\$2,115,000\\cell\\row\n"
            "}\n\n"
            "The actual report should be a clean table. It printed fine before "
            "the update. I'm using an HP LaserJet 4250 on Floor {floor}.\n\n"
            "{name}, {department}",
            "My documents are printing with raw RTF code instead of formatted "
            "text. I tried saving as PDF first and that works, but printing "
            "directly from Word gives this:\n\n"
            "{\\rtf1\\ansi{\\fonttbl{\\f0 Times New Roman;}}\n"
            "\\pard\\plain\\f0\\fs24 Meeting Notes — {department} All-Hands"
            "\\par\\par\n"
            "\\b Attendees:\\b0\\par\n"
            "\\pard{\\pntext\\f0 1.\\tab}{\\*\\pn\\pnlvlbody\\pnf0\\pnstart1"
            "\\pndec{\\pntxta.}}\\fi-360\\li720 {name} (Chair)\\par\n"
            "{\\pntext\\f0 2.\\tab}VP of Engineering\\par\n"
            "{\\pntext\\f0 3.\\tab}Director of Operations\\par\n"
            "\\pard\\par\n"
            "\\b Action Items:\\b0\\par\n"
            "\\pard\\li720\\bullet  Review Q2 numbers by Friday\\par\n"
            "\\bullet  Schedule follow-up with {department}\\par\n"
            "}\n\n"
            "I've rebooted, cleared the print queue, and reinstalled the "
            "printer driver. Same result. Other apps print fine.\n\n"
            "{name}, {department}",
        ],
        next_best_actions=[
            "The printer is receiving raw RTF markup instead of rendered output. "
            "This is likely a driver issue introduced by the Word update — the "
            "print pipeline is sending RTF source rather than GDI/PostScript.",
            "Investigate the printer driver compatibility with the latest Word "
            "update. The RTF artifacts indicate the document is being sent as "
            "raw text rather than through the rendering pipeline.",
        ],
        remediation_steps=[
            [
                "Check the installed printer driver version and compare with the manufacturer's latest release",
                "Reinstall the printer driver using the PCL6 or PostScript driver variant instead of the generic text "
                "driver",
                "Test printing from Word using the 'Print to PDF' option to confirm the document renders correctly",
                "If the driver is current, check Word's print settings for 'Print using system default' vs direct "
                "rendering",
                "Apply any pending Windows updates that may include print subsystem fixes",
                "Test with a different printer to isolate whether the issue is driver-specific or Word-specific",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# dc-124  Chained auto-reply / OOO messages burying the real issue
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="dc-124",
        category=Category.SOFTWARE,
        priority=Priority.P3,
        assigned_team=Team.ENTERPRISE_APPS,
        needs_escalation=False,
        missing_information=[MissingInfo.ERROR_MESSAGE, MissingInfo.STEPS_TO_REPRODUCE],
        subjects=[
            "Re: RE: Automatic reply: RE: Out of Office: Re: Outlook sync broken",
            "FW: Auto: OOO: RE: RE: Calendar not syncing",
            "Re: Automatic reply: Re: Out of Office: Teams meeting errors",
        ],
        descriptions=[
            "--- Automatic reply ---\n"
            "I am currently out of the office with no access to email. I will return "
            "on Monday, June 23. For urgent matters, please contact the {department} "
            "help desk.\n\n"
            "--- Original Message ---\n"
            "From: IT Support <itsupport@contoso.com>\n"
            "Subject: RE: Out of Office: Re: Outlook sync broken\n\n"
            "Hi {name}, thanks for reaching out. We've assigned your ticket. A "
            "technician will follow up shortly.\n\n"
            "--- Automatic reply ---\n"
            "Thank you for your email. I am out of the office from June 16-20 and "
            "will have limited access to email. For immediate assistance contact "
            "{name1}@contoso.com.\n\n"
            "--- Original Message ---\n"
            "From: {name} <{name1}@contoso.com>\n"
            "Subject: Re: Outlook sync broken\n\n"
            "Just following up — still can't sync. Adding the support alias.\n\n"
            "--- Automatic reply ---\n"
            "I will be out of the office until June 23. If this is urgent, please "
            "contact the {department} on-call team.\n\n"
            "--- Original Message ---\n"
            "From: {name} <{name1}@contoso.com>\n"
            "Subject: Outlook sync broken\n\n"
            "My Outlook hasn't synced new emails since Friday. I see a yellow "
            "triangle icon in the system tray. I've tried restarting Outlook and "
            "running the connection test — it says 'Exchange server unavailable'. "
            "I'm on Floor {floor}, {office} office, using Outlook 365 on "
            "Windows 11.\n\n{name}, {department}",
            "--- Auto-Reply ---\n"
            "Thank you for contacting {department}. This is an automated response "
            "to confirm we received your request. Your reference number is "
            "INC-2026-78432. Please do not reply to this message.\n\n"
            "--- Out of Office ---\n"
            "From: {name} <{name1}@contoso.com>\n"
            "I'm on PTO through June 27. Reach out to {department} channel on "
            "Teams for anything urgent.\n\n"
            "--- Auto-Reply ---\n"
            "Your message has been forwarded to the {department} queue. Expected "
            "response time: 4 business hours.\n\n"
            "--- Out of Office ---\n"
            "Hi! I'm out of office this week. For {app}-related issues, please "
            "file a ticket at https://support.contoso.com.\n\n"
            "--- Original Message ---\n"
            "From: {name} <{name1}@contoso.com>\n"
            "Subject: Calendar not syncing\n\n"
            "My calendar stopped syncing across devices yesterday. New events I "
            "create on my laptop don't show up on my phone, and vice versa. I've "
            "checked that I'm signed into the same account on both. Other people "
            "in {department} can see my calendar fine — it's just my own devices "
            "that are out of sync. Floor {floor}, {office}.\n\n{name}, {department}",
        ],
        next_best_actions=[
            "Ignore the auto-reply and OOO chain. The actual issue is buried at "
            "the bottom: Outlook/calendar sync failure with an 'Exchange server "
            "unavailable' error. Troubleshoot the Exchange connectivity.",
            "Strip the automated reply noise to find the real ticket: a "
            "calendar/email sync issue across devices. Check the user's Exchange "
            "Online mailbox health and device sync status.",
        ],
        remediation_steps=[
            [
                "Identify the actual issue from the original message at the bottom of the thread",
                "Check Exchange Online service health for any ongoing sync issues",
                "Verify the user's mailbox provisioning and license status in Microsoft 365 admin center",
                "Run Test-OutlookConnectivity or the Microsoft Remote Connectivity Analyzer for the user",
                "If mailbox is healthy, reset the Outlook profile on the affected device and reconfigure",
                "Confirm sync is working on all devices before closing the ticket",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# dc-125  Large inline SVG data embedded in ticket
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="dc-125",
        category=Category.NETWORK,
        priority=Priority.P2,
        assigned_team=Team.NETWORK,
        needs_escalation=False,
        missing_information=[MissingInfo.NETWORK_LOCATION, MissingInfo.ERROR_MESSAGE],
        subjects=[
            "Network topology diagram not rendering — SVG source pasted",
            "Intranet map page broken — raw SVG showing instead of image",
            "Floor plan SVG not loading on network portal",
        ],
        descriptions=[
            "The network topology diagram on our intranet shows raw SVG code "
            "instead of the rendered image. Here's what appears on the page:\n\n"
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 800" '
            'width="1200" height="800">\n'
            "  <defs>\n"
            '    <marker id="arrowhead" markerWidth="10" markerHeight="7" '
            'refX="10" refY="3.5" orient="auto">\n'
            '      <polygon points="0 0, 10 3.5, 0 7" fill="#2c3e50"/>\n'
            "    </marker>\n"
            '    <filter id="shadow" x="-20%" y="-20%" width="140%" height="140%">\n'
            '      <feDropShadow dx="2" dy="2" stdDeviation="3" '
            'flood-opacity="0.3"/>\n'
            "    </filter>\n"
            "  </defs>\n"
            '  <rect x="50" y="50" width="200" height="80" rx="10" '
            'fill="#3498db" filter="url(#shadow)"/>\n'
            '  <text x="150" y="95" text-anchor="middle" fill="white" '
            'font-size="14">Core Switch — Building {building}</text>\n'
            '  <rect x="500" y="50" width="200" height="80" rx="10" '
            'fill="#e74c3c" filter="url(#shadow)"/>\n'
            '  <text x="600" y="95" text-anchor="middle" fill="white" '
            'font-size="14">Firewall Cluster</text>\n'
            '  <line x1="250" y1="90" x2="500" y2="90" stroke="#2c3e50" '
            'stroke-width="2" marker-end="url(#arrowhead)"/>\n'
            '  <rect x="50" y="250" width="200" height="80" rx="10" '
            'fill="#2ecc71" filter="url(#shadow)"/>\n'
            '  <text x="150" y="295" text-anchor="middle" fill="white" '
            'font-size="14">Floor {floor} Access Switch</text>\n'
            '  <rect x="500" y="250" width="200" height="80" rx="10" '
            'fill="#f39c12" filter="url(#shadow)"/>\n'
            '  <text x="600" y="295" text-anchor="middle" fill="white" '
            'font-size="14">WAP — {office} Office</text>\n'
            '  <line x1="150" y1="130" x2="150" y2="250" stroke="#2c3e50" '
            'stroke-width="2" marker-end="url(#arrowhead)"/>\n'
            '  <line x1="250" y1="290" x2="500" y2="290" stroke="#2c3e50" '
            'stroke-width="2" marker-end="url(#arrowhead)"/>\n'
            "</svg>\n\n"
            "This should be a clickable network map. It broke after the portal "
            "update last Thursday. I'm in {office}, Floor {floor}.\n\n"
            "{name}, {department}",
            "The floor plan page on the network portal is showing XML instead "
            "of the diagram. I saved the page source and it's all SVG:\n\n"
            '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 960 640">\n'
            "  <style>\n"
            "    .room {{ fill: #ecf0f1; stroke: #bdc3c7; stroke-width: 2; }}\n"
            "    .active {{ fill: #2ecc71; }}\n"
            "    .label {{ font-family: Segoe UI, sans-serif; font-size: 11px; }}\n"
            "  </style>\n"
            '  <rect class="room" x="10" y="10" width="120" height="100"/>\n'
            '  <text class="label" x="70" y="65" text-anchor="middle">'
            "{department}</text>\n"
            '  <rect class="room active" x="140" y="10" width="120" '
            'height="100"/>\n'
            '  <text class="label" x="200" y="65" text-anchor="middle">'
            "Server Room</text>\n"
            '  <rect class="room" x="270" y="10" width="120" height="100"/>\n'
            '  <text class="label" x="330" y="65" text-anchor="middle">'
            "Conference A</text>\n"
            '  <rect class="room" x="10" y="120" width="380" height="60"/>\n'
            '  <text class="label" x="200" y="155" text-anchor="middle">'
            "Hallway — Floor {floor}</text>\n"
            "</svg>\n\n"
            "Other pages on the portal are fine. Just the maps are broken. "
            "Chrome and Edge both show the same raw code.\n\n"
            "{name}, {department}",
        ],
        next_best_actions=[
            "The intranet portal is serving SVG content with an incorrect "
            "Content-Type header (likely text/plain instead of image/svg+xml). "
            "Fix the web server MIME type configuration for SVG files.",
            "Check the portal's web server configuration for SVG MIME type "
            "settings. The recent update likely removed or overrode the "
            "image/svg+xml content-type mapping.",
        ],
        remediation_steps=[
            [
                "Verify the Content-Type header returned for SVG files using browser developer tools or curl",
                "Update the web server configuration to serve .svg files with Content-Type: image/svg+xml",
                "Check if the portal update changed the static file serving configuration or CDN settings",
                "Clear the CDN cache if SVG files are served through a content delivery layer",
                "Test the network topology and floor plan pages to confirm SVG rendering is restored",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# dc-126  Interleaved / cross-threaded issues in a single ticket
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="dc-126",
        category=Category.NETWORK,
        priority=Priority.P2,
        assigned_team=Team.NETWORK,
        needs_escalation=False,
        missing_information=[MissingInfo.AFFECTED_SYSTEM, MissingInfo.NETWORK_LOCATION],
        subjects=[
            "Multiple network issues — VPN, WiFi, and DNS all at once",
            "Several connectivity problems happening simultaneously",
            "Network problems on Floor {floor} — three different issues",
        ],
        descriptions=[
            "I have several issues and I'm not sure if they're related:\n\n"
            "ISSUE A: My VPN drops every ~30 minutes. I'm using GlobalProtect "
            "5.2.13. It reconnects automatically but all my SSH sessions die. "
            "This started Monday.\n\n"
            "ISSUE B (actually this might be the same thing): WiFi signal is "
            "weak in the {office} conference room. Wait no — that's a different "
            "problem. The WiFi is always weak there. But the VPN thing is new.\n\n"
            "ISSUE C: Also, DNS lookups are slow. I ran nslookup contoso.com and "
            "it took 8 seconds. Normally it's instant. But that might be because "
            "of the VPN — when VPN reconnects, DNS is broken for a minute.\n\n"
            "Actually, re-reading what I wrote — maybe Issues A and C are the "
            "same root cause? The VPN drops, and during the reconnect window DNS "
            "doesn't work? But Issue B is definitely separate.\n\n"
            "Oh, one more thing — I also can't print to the Floor {floor} printer "
            "but that might be unrelated. Or maybe it is related if the printer "
            "is on a network share that needs DNS? I don't know.\n\n"
            "I'm on Floor {floor}, {office} office, wired + WiFi (I switch "
            "between them).\n\n{name}, {department}",
            "Submitting one ticket for everything since I'm not sure what's "
            "connected:\n\n"
            "1) Teams calls drop audio for 2-3 seconds every few minutes. "
            "Video freezes too. My internet speed test shows 450 Mbps so "
            "bandwidth isn't the issue.\n\n"
            "2) The shared drive (\\\\fileserver\\{department}) sometimes takes "
            "30+ seconds to open folders. Other times it's instant.\n\n"
            "3) Outlook shows 'Trying to connect...' in the status bar at "
            "random intervals throughout the day.\n\n"
            "These all started around the same time — last Thursday after the "
            "network maintenance window. Are they related? Could be a switch "
            "issue on our floor?\n\n"
            "Also, separately, my badge doesn't open the Building {building} "
            "parking garage anymore but that's probably a different team.\n\n"
            "Floor {floor}, {office}, Building {building}.\n\n"
            "{name}, {department}",
        ],
        next_best_actions=[
            "Separate the interleaved issues: the VPN drops and DNS slowness "
            "are likely related (VPN reconnection disrupts DNS resolution). The "
            "WiFi weakness and printer issue are separate problems. Triage each "
            "independently.",
            "The post-maintenance symptoms (Teams audio drops, slow file share, "
            "intermittent Outlook disconnects) suggest a common cause — likely a "
            "switch or port configuration issue on the user's floor. Investigate "
            "the network infrastructure first.",
        ],
        remediation_steps=[
            [
                "Untangle the separate issues and create sub-tickets for each distinct problem",
                "For the likely related issues (VPN/DNS or Teams/fileshare/Outlook), check the floor switch logs for "
                "errors or flapping ports",
                "Verify the network maintenance changes didn't introduce a misconfiguration on the user's floor switch",
                "Run a continuous ping and traceroute to identify packet loss or latency spikes",
                "Address each sub-issue based on root cause: VPN config, WiFi coverage, DNS settings, or switch port",
                "Route unrelated issues (badge access, printing) to the appropriate teams",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# dc-127  Massive CC list cluttering the ticket
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="dc-127",
        category=Category.SECURITY,
        priority=Priority.P2,
        assigned_team=Team.SECOPS,
        needs_escalation=True,
        missing_information=[MissingInfo.AFFECTED_USERS, MissingInfo.BUSINESS_IMPACT],
        subjects=[
            "URGENT: Suspicious email sent to entire department — 200+ recipients",
            "Possible phishing blast — massive CC list included below",
            "Phishing alert — email sent to all of {department}",
        ],
        descriptions=[
            "A suspicious email was sent to what looks like our entire "
            "department distribution list plus individual addresses. I'm "
            "including the CC list so you can see who got it:\n\n"
            "To: {department}-all@contoso.com\n"
            "CC: a.adams@contoso.com; b.baker@contoso.com; c.chen@contoso.com; "
            "d.davis@contoso.com; e.erikson@contoso.com; f.foster@contoso.com; "
            "g.garcia@contoso.com; h.harris@contoso.com; i.ibrahim@contoso.com; "
            "j.jones@contoso.com; k.kumar@contoso.com; l.lee@contoso.com; "
            "m.martinez@contoso.com; n.nguyen@contoso.com; o.okafor@contoso.com; "
            "p.patel@contoso.com; q.quinn@contoso.com; r.rodriguez@contoso.com; "
            "s.singh@contoso.com; t.taylor@contoso.com; u.ueda@contoso.com; "
            "v.volkov@contoso.com; w.wang@contoso.com; x.xu@contoso.com; "
            "y.yamamoto@contoso.com; z.zhang@contoso.com; "
            "aa.anderson@contoso.com; bb.brown@contoso.com; "
            "cc.campbell@contoso.com; dd.diaz@contoso.com; "
            "ee.edwards@contoso.com; ff.flores@contoso.com; "
            "gg.gonzalez@contoso.com; hh.hall@contoso.com; "
            "ii.ishikawa@contoso.com; jj.jackson@contoso.com; "
            "kk.kowalski@contoso.com; ll.lopez@contoso.com; "
            "mm.mueller@contoso.com; nn.nakamura@contoso.com; "
            "oo.oconnor@contoso.com; pp.park@contoso.com; "
            "qq.qureshi@contoso.com; rr.ramirez@contoso.com; "
            "ss.schmidt@contoso.com; tt.thompson@contoso.com\n"
            "BCC: (unknown)\n\n"
            "The email claims to be from our CEO and asks everyone to click a "
            "link to 'verify their credentials for a mandatory security audit'. "
            "The link goes to contoso-security-verify.com which is NOT our "
            "domain. Several people have already clicked it.\n\n"
            "{name}, {department}",
            "We received a bulk email that was sent to a huge list of people "
            "across {department}. The full recipient list:\n\n"
            "To: {name} <{name1}@contoso.com>\n"
            "CC: team-leads-{department}@contoso.com; "
            "managers-{department}@contoso.com; directors@contoso.com; "
            "vp-staff@contoso.com; exec-assistants@contoso.com; "
            "hr-partners@contoso.com; finance-approvers@contoso.com; "
            "procurement@contoso.com; legal-team@contoso.com; "
            "compliance-officers@contoso.com; it-liaisons@contoso.com; "
            "facilities-contacts@contoso.com; floor-wardens@contoso.com; "
            "{department}-contractors@contoso.com; "
            "{department}-interns@contoso.com; "
            "{department}-alumni@contoso.com\n\n"
            "The email has a PDF attachment called 'Mandatory_Security_Update_"
            "Instructions.pdf' and a link to an external form asking for "
            "employee IDs and passwords. The sender address looks spoofed — "
            "it says ceo@contoso.com but the headers show it came from a "
            "Gmail relay. At least 12 people in {department} have told me "
            "they clicked the link and some entered their passwords.\n\n"
            "{name}, {department}",
        ],
        next_best_actions=[
            "This is an active phishing campaign targeting the department. "
            "Immediately block the malicious domain, quarantine the email from "
            "all mailboxes, and initiate password resets for users who clicked.",
            "Treat this as a security incident: block contoso-security-verify.com "
            "at the proxy and DNS level, purge the email from all recipients' "
            "mailboxes, and force password resets for anyone who submitted "
            "credentials.",
        ],
        remediation_steps=[
            [
                "Block the malicious domain at the web proxy, DNS, and email gateway",
                "Use Exchange admin center to search and purge the phishing email from all recipient mailboxes",
                "Identify users who clicked the link using email gateway and proxy logs",
                "Force immediate password resets for all users who submitted credentials",
                "Review sign-in logs for the compromised accounts for any unauthorized access",
                "Send an organization-wide alert warning about the phishing email and instructing users not to click",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# dc-128  Environment variable dump pasted into ticket
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="dc-128",
        category=Category.SOFTWARE,
        priority=Priority.P2,
        assigned_team=Team.ENTERPRISE_APPS,
        needs_escalation=False,
        missing_information=[MissingInfo.APPLICATION_VERSION, MissingInfo.STEPS_TO_REPRODUCE],
        subjects=[
            "App won't start — env vars dumped below",
            "Application startup failure — environment output attached",
            "{app} crashes on launch — pasting my environment",
        ],
        descriptions=[
            "{app} won't start and the error says 'missing required environment "
            "variable'. I ran `printenv` and here's everything:\n\n"
            "SHELL=/bin/bash\n"
            "SESSION_MANAGER=local/{name}:@/tmp/.ICE-unix/1847,unix/{name}:/tmp/"
            ".ICE-unix/1847\n"
            "QT_ACCESSIBILITY=1\n"
            "COLORTERM=truecolor\n"
            "XDG_CONFIG_DIRS=/etc/xdg/xdg-ubuntu:/etc/xdg\n"
            "SSH_AGENT_LAUNCHER=openssh\n"
            "XDG_MENU_PREFIX=gnome-\n"
            "GNOME_DESKTOP_SESSION_ID=this-is-deprecated\n"
            "CONTOSO_APP_ENV=production\n"
            "CONTOSO_API_ENDPOINT=https://api.contoso.com/v2\n"
            "CONTOSO_AUTH_PROVIDER=azure-ad\n"
            "CONTOSO_TENANT_ID=a1b2c3d4-e5f6-7890-abcd-ef1234567890\n"
            "CONTOSO_REGION=eastus2\n"
            "CONTOSO_LOG_LEVEL=info\n"
            "CONTOSO_CACHE_TTL=3600\n"
            "CONTOSO_DB_HOST=sqlprod-eastus2.database.windows.net\n"
            "CONTOSO_DB_PORT=1433\n"
            "CONTOSO_DB_NAME={app}_prod\n"
            "CONTOSO_REDIS_HOST=redis-prod.contoso.internal\n"
            "CONTOSO_REDIS_PORT=6380\n"
            "CONTOSO_FEATURE_FLAGS=enable_v2_ui,enable_new_search,beta_export\n"
            "GTK_MODULES=gail:atk-bridge\n"
            "DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/1000/bus\n"
            "DESKTOP_SESSION=ubuntu\n"
            "GDMSESSION=ubuntu\n"
            "HOME=/home/{name1}\n"
            "LANG=en_US.UTF-8\n"
            "LOGNAME={name1}\n"
            "PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin\n"
            "USER={name1}\n"
            "XDG_RUNTIME_DIR=/run/user/1000\n"
            "XDG_SESSION_TYPE=wayland\n\n"
            "I don't see which one is missing. Can you tell from this? I'm in "
            "{department}, Floor {floor}.\n\n{name}, {department}",
            "I'm getting this error when launching {app}:\n\n"
            "  Error: Required configuration not found.\n"
            "  Missing: CONTOSO_CLIENT_SECRET\n"
            "  Application will not start.\n\n"
            "I dumped all my env vars to check. Here's the full output of `env | "
            "sort`:\n\n"
            "CONTOSO_API_ENDPOINT=https://api.contoso.com/v2\n"
            "CONTOSO_APP_ENV=production\n"
            "CONTOSO_AUTH_PROVIDER=azure-ad\n"
            "CONTOSO_CACHE_TTL=3600\n"
            "CONTOSO_CLIENT_ID=app-{app}-prod-00a1b2c3\n"
            "CONTOSO_DB_HOST=sqlprod-eastus2.database.windows.net\n"
            "CONTOSO_DB_NAME={app}_prod\n"
            "CONTOSO_DB_PORT=1433\n"
            "CONTOSO_FEATURE_FLAGS=enable_v2_ui,enable_new_search\n"
            "CONTOSO_LOG_LEVEL=info\n"
            "CONTOSO_REDIS_HOST=redis-prod.contoso.internal\n"
            "CONTOSO_REDIS_PORT=6380\n"
            "CONTOSO_REGION=eastus2\n"
            "CONTOSO_TENANT_ID=a1b2c3d4-e5f6-7890-abcd-ef1234567890\n"
            "DBUS_SESSION_BUS_ADDRESS=unix:path=/run/user/1000/bus\n"
            "DESKTOP_SESSION=ubuntu\n"
            "HOME=/home/{name1}\n"
            "LANG=en_US.UTF-8\n"
            "LOGNAME={name1}\n"
            "PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin\n"
            "SHELL=/bin/bash\n"
            "USER={name1}\n\n"
            "The error clearly says CONTOSO_CLIENT_SECRET is missing but I "
            "don't know where to get it. Was this set up by the previous admin? "
            "I'm new to {department}.\n\n{name}, {department}",
        ],
        next_best_actions=[
            "The environment dump reveals the issue: CONTOSO_CLIENT_SECRET is "
            "missing. This is an Azure AD app registration secret that needs "
            "to be provisioned through the secrets management system.",
            "Identify the missing environment variable from the error output. "
            "The user needs CONTOSO_CLIENT_SECRET configured — retrieve it from "
            "the team's key vault or secrets manager.",
        ],
        remediation_steps=[
            [
                "Identify the missing environment variable from the application error message",
                "Check the team's Azure Key Vault or secrets management system for the required secret",
                "If the secret has expired, rotate it in the Azure AD app registration and update the vault",
                "Set the environment variable through the approved configuration management process (not inline "
                "export)",
                "Verify the application starts successfully with the new configuration",
                "Remind the user to never paste environment variables containing secrets into tickets",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# dc-129  Git diff / merge conflict markers pasted inline
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="dc-129",
        category=Category.SOFTWARE,
        priority=Priority.P2,
        assigned_team=Team.ENTERPRISE_APPS,
        needs_escalation=False,
        missing_information=[MissingInfo.STEPS_TO_REPRODUCE, MissingInfo.ENVIRONMENT_DETAILS],
        subjects=[
            "Deployment failed — git diff of broken config below",
            "Need help resolving config diff before deploying {app}",
            "Production config changed unexpectedly — diff attached",
        ],
        descriptions=[
            "Our last {app} deployment failed and I think it's because someone "
            "changed the config. Here's the git diff between what's in production "
            "and what's in our repo:\n\n"
            "diff --git a/config/production.yaml b/config/production.yaml\n"
            "index 3a4b5c6..7d8e9f0 100644\n"
            "--- a/config/production.yaml\n"
            "+++ b/config/production.yaml\n"
            "@@ -12,18 +12,22 @@\n"
            " server:\n"
            "   host: 0.0.0.0\n"
            "-  port: 8080\n"
            "+  port: 8443\n"
            "-  protocol: http\n"
            "+  protocol: https\n"
            "+  tls:\n"
            "+    cert: /etc/ssl/{app}/server.crt\n"
            "+    key: /etc/ssl/{app}/server.key\n"
            "+    min_version: '1.2'\n"
            " \n"
            " database:\n"
            "   host: sqlprod-eastus2.database.windows.net\n"
            "-  pool_size: 10\n"
            "+  pool_size: 50\n"
            "-  timeout: 30\n"
            "+  timeout: 120\n"
            "+  retry_policy:\n"
            "+    max_retries: 3\n"
            "+    backoff_factor: 1.5\n"
            " \n"
            " cache:\n"
            "   host: redis-prod.contoso.internal\n"
            "-  ttl: 3600\n"
            "+  ttl: 600\n"
            "-  max_memory: 512mb\n"
            "+  max_memory: 2gb\n"
            " \n"
            " logging:\n"
            "-  level: info\n"
            "+  level: debug\n"
            "-  output: file\n"
            "+  output: stdout\n\n"
            "I'm not sure which version is correct. The deployment pipeline "
            "rejected the new version because the TLS cert doesn't exist on the "
            "new servers yet. Can you help figure out what went wrong?\n\n"
            "{name}, {department}",
            "Something changed in our {app} config and now the CI/CD pipeline "
            "is failing. Here's the diff I got from git:\n\n"
            "diff --git a/deploy/docker-compose.prod.yml "
            "b/deploy/docker-compose.prod.yml\n"
            "index a1b2c3d..e4f5g6h 100644\n"
            "--- a/deploy/docker-compose.prod.yml\n"
            "+++ b/deploy/docker-compose.prod.yml\n"
            "@@ -8,14 +8,20 @@\n"
            " services:\n"
            "   {app}-api:\n"
            "-    image: contoso.azurecr.io/{app}:v2.3.1\n"
            "+    image: contoso.azurecr.io/{app}:v2.4.0-rc1\n"
            "     environment:\n"
            "-      - NODE_ENV=production\n"
            "+      - NODE_ENV=staging\n"
            "-      - LOG_LEVEL=warn\n"
            "+      - LOG_LEVEL=debug\n"
            "+      - ENABLE_PROFILING=true\n"
            "+      - DEBUG_PORT=9229\n"
            "     ports:\n"
            "-      - '8080:8080'\n"
            "+      - '8080:8080'\n"
            "+      - '9229:9229'\n"
            "     deploy:\n"
            "       resources:\n"
            "         limits:\n"
            "-          memory: 1G\n"
            "+          memory: 4G\n"
            "-          cpus: '1.0'\n"
            "+          cpus: '4.0'\n\n"
            "Looks like someone pushed staging/debug settings to the production "
            "branch. The pipeline caught it because the RC image tag doesn't "
            "exist in our production registry. Floor {floor}, {office}.\n\n"
            "{name}, {department}",
        ],
        next_best_actions=[
            "Review the git diff to identify the problematic changes: staging "
            "settings (debug logging, RC image tags, debug ports) were pushed to "
            "the production config. Revert the non-production changes and fix "
            "any intentional updates (like TLS) separately.",
            "The diff shows a mix of intentional upgrades (TLS, connection pool) "
            "and accidental staging settings (debug logging, profiling, RC images). "
            "Separate the two, revert the staging changes, and properly deploy "
            "the intended production updates.",
        ],
        remediation_steps=[
            [
                "Review the git diff to separate intentional production changes from accidental staging settings",
                "Revert debug/staging changes: NODE_ENV=staging, LOG_LEVEL=debug, ENABLE_PROFILING, DEBUG_PORT, RC "
                "image tags",
                "For intentional changes (TLS config, pool size), ensure prerequisites are met (certs deployed, "
                "capacity verified)",
                "Create a clean commit with only the production-ready changes",
                "Run the CI/CD pipeline in a staging environment to validate before pushing to production",
                "Enforce branch protection rules to require PR reviews for production config changes",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# dc-130  YAML config dump pasted into ticket
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="dc-130",
        category=Category.SOFTWARE,
        priority=Priority.P2,
        assigned_team=Team.ENTERPRISE_APPS,
        needs_escalation=False,
        missing_information=[MissingInfo.ERROR_MESSAGE, MissingInfo.APPLICATION_VERSION],
        subjects=[
            "Kubernetes pod crashing — full YAML manifest below",
            "Pod in CrashLoopBackOff — config dump included",
            "{app} deployment failing in K8s — YAML pasted",
        ],
        descriptions=[
            "Our {app} pod is stuck in CrashLoopBackOff. I'm pasting the full "
            "deployment YAML so you can check it:\n\n"
            "apiVersion: apps/v1\n"
            "kind: Deployment\n"
            "metadata:\n"
            "  name: {app}-api\n"
            "  namespace: {department}-prod\n"
            "  labels:\n"
            "    app: {app}\n"
            "    team: {department}\n"
            "    environment: production\n"
            "spec:\n"
            "  replicas: 3\n"
            "  selector:\n"
            "    matchLabels:\n"
            "      app: {app}\n"
            "  template:\n"
            "    metadata:\n"
            "      labels:\n"
            "        app: {app}\n"
            "        version: v2.4.0\n"
            "      annotations:\n"
            "        prometheus.io/scrape: 'true'\n"
            "        prometheus.io/port: '9090'\n"
            "    spec:\n"
            "      serviceAccountName: {app}-sa\n"
            "      containers:\n"
            "        - name: {app}-api\n"
            "          image: contoso.azurecr.io/{app}:v2.4.0\n"
            "          ports:\n"
            "            - containerPort: 8080\n"
            "              name: http\n"
            "            - containerPort: 9090\n"
            "              name: metrics\n"
            "          env:\n"
            "            - name: DB_CONNECTION_STRING\n"
            "              valueFrom:\n"
            "                secretKeyRef:\n"
            "                  name: {app}-db-secret\n"
            "                  key: connection-string\n"
            "            - name: REDIS_URL\n"
            "              value: redis://redis-prod.contoso.internal:6380\n"
            "            - name: APP_ENV\n"
            "              value: production\n"
            "          resources:\n"
            "            requests:\n"
            "              memory: 256Mi\n"
            "              cpu: 250m\n"
            "            limits:\n"
            "              memory: 256Mi\n"
            "              cpu: 500m\n"
            "          livenessProbe:\n"
            "            httpGet:\n"
            "              path: /healthz\n"
            "              port: 8080\n"
            "            initialDelaySeconds: 5\n"
            "            periodSeconds: 10\n"
            "          readinessProbe:\n"
            "            httpGet:\n"
            "              path: /ready\n"
            "              port: 8080\n"
            "            initialDelaySeconds: 5\n"
            "            periodSeconds: 5\n"
            "      imagePullSecrets:\n"
            "        - name: acr-pull-secret\n\n"
            "The pod starts, fails the liveness probe, and gets killed. Logs "
            "show 'connection refused' to the database. I think the secret might "
            "be wrong.\n\n{name}, {department}",
            "I'm trying to deploy {app} to our Kubernetes cluster and it keeps "
            "failing. Here's my config:\n\n"
            "apiVersion: v1\n"
            "kind: Service\n"
            "metadata:\n"
            "  name: {app}-svc\n"
            "  namespace: {department}-prod\n"
            "spec:\n"
            "  selector:\n"
            "    app: {app}\n"
            "  ports:\n"
            "    - name: http\n"
            "      port: 80\n"
            "      targetPort: 8080\n"
            "    - name: metrics\n"
            "      port: 9090\n"
            "      targetPort: 9090\n"
            "  type: ClusterIP\n"
            "---\n"
            "apiVersion: networking.k8s.io/v1\n"
            "kind: Ingress\n"
            "metadata:\n"
            "  name: {app}-ingress\n"
            "  namespace: {department}-prod\n"
            "  annotations:\n"
            "    nginx.ingress.kubernetes.io/rewrite-target: /\n"
            "    nginx.ingress.kubernetes.io/ssl-redirect: 'true'\n"
            "    cert-manager.io/cluster-issuer: letsencrypt-prod\n"
            "spec:\n"
            "  tls:\n"
            "    - hosts:\n"
            "        - {app}.contoso.com\n"
            "      secretName: {app}-tls\n"
            "  rules:\n"
            "    - host: {app}.contoso.com\n"
            "      http:\n"
            "        paths:\n"
            "          - path: /\n"
            "            pathType: Prefix\n"
            "            backend:\n"
            "              service:\n"
            "                name: {app}-svc\n"
            "                port:\n"
            "                  number: 80\n\n"
            "The deployment itself is running but the Ingress returns 502 Bad "
            "Gateway. The service seems fine when I port-forward directly. "
            "Floor {floor}, {department}.\n\n{name}, {department}",
        ],
        next_best_actions=[
            "Analyze the Kubernetes YAML dump: the CrashLoopBackOff is caused "
            "by a database connection failure — verify the referenced secret "
            "exists and contains the correct connection string. The memory limit "
            "of 256Mi may also be too low.",
            "For the 502 Ingress issue, check that the Service selector matches "
            "the pod labels, the target port matches the container port, and the "
            "Ingress controller can reach the service. For the CrashLoopBackOff, "
            "fix the database secret.",
        ],
        remediation_steps=[
            [
                "Check if the referenced Kubernetes secret exists: kubectl get secret {app}-db-secret -n "
                "{department}-prod",
                "Verify the secret contains the correct connection string by decoding it (base64)",
                "Test database connectivity from within the cluster using a debug pod",
                "If the secret is correct, check if the memory limit (256Mi) is sufficient — increase if OOMKilled",
                "For Ingress 502 errors, verify service selector labels match pod labels and ports are aligned",
                "Check Ingress controller logs for upstream connection errors and fix the backend configuration",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# dc-131  Thread hijacking — topic switch mid-conversation
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="dc-131",
        category=Category.NETWORK,
        priority=Priority.P3,
        assigned_team=Team.NETWORK,
        needs_escalation=False,
        missing_information=[MissingInfo.APPLICATION_VERSION],
        subjects=[
            "Re: Re: FW: Printer on {floor} not printing — actually, VPN question",
            "RE: Printer jam follow-up (also: VPN keeps dropping)",
            "Re: Print queue stuck — unrelated VPN issue too",
        ],
        descriptions=[
            "Hi team,\n\n"
            "Quick update on the printer — it's actually working now, someone power-cycled it.\n\n"
            "BUT, completely different issue: my VPN has been disconnecting every 20 minutes "
            "since last Thursday. I'm using GlobalProtect on {os} from the {office} office, "
            "Floor {floor}. Every time I reconnect it works for a bit then drops again.\n\n"
            "--- Original Message ---\n"
            "From: {name} <{name1}@contoso.com>\n"
            "Sent: Monday, April 7, 2026 9:15 AM\n"
            "To: IT Support <itsupport@contoso.com>\n"
            "Subject: Re: FW: Printer on {floor} not printing\n\n"
            "The HP LaserJet on Floor {floor} near the kitchen is still showing offline. "
            "Jobs queue up but never print. Can someone look at the print server?\n\n"
            "--- Original Message ---\n"
            "From: IT Support <itsupport@contoso.com>\n"
            "Sent: Friday, April 4, 2026 3:30 PM\n"
            "Subject: FW: Printer on {floor} not printing\n\n"
            "We've restarted the spooler. Please try again and let us know.\n\n"
            "Thanks,\n{name}, {department}",
            "Following up on the printer ticket — ignore that, it's resolved.\n\n"
            "New problem: I can't stay connected to the corporate VPN for more than "
            "15-20 minutes at a stretch. I'm on Wi-Fi at the {office} office, Floor "
            "{floor}. My laptop is running {os} and I don't know the VPN client version "
            "off the top of my head.\n\n"
            "The original thread was about the Floor {floor} HP printer being offline. "
            "That one is fixed now.\n\n"
            "This VPN issue started after the network maintenance window last Wednesday "
            "night. I've tried forgetting and re-adding the Wi-Fi network, rebooting, "
            "and even connecting via Ethernet — same problem on Ethernet too actually.\n\n"
            "Can someone from the network team take a look?\n\n"
            "Thanks,\n{name}, {department}",
        ],
        next_best_actions=[
            "Ignore the resolved printer thread; the actual issue is recurring VPN "
            "disconnects every 15-20 minutes post-maintenance. Investigate VPN gateway "
            "session timeout settings and recent configuration changes.",
            "The ticket topic switched mid-thread from a printer issue (now resolved) to "
            "a VPN connectivity problem. Focus on the VPN disconnect pattern and correlate "
            "with the recent network maintenance window.",
        ],
        remediation_steps=[
            [
                "Confirm the printer issue is resolved — no action needed on that thread",
                "Check VPN gateway logs for the user's session termination events over the past week",
                "Review changes made during the last network maintenance window that may affect VPN tunnels",
                "Verify VPN session timeout and keep-alive settings on the gateway",
                "Request the user's GlobalProtect client version to check for known bugs",
                "If issue persists on both Wi-Fi and Ethernet, escalate to the network engineering team",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# dc-132  Mixed RTL/LTR text — Hebrew/Arabic mixed with English
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="dc-132",
        category=Category.SOFTWARE,
        priority=Priority.P3,
        assigned_team=Team.ENTERPRISE_APPS,
        needs_escalation=False,
        missing_information=[MissingInfo.ERROR_MESSAGE, MissingInfo.ENVIRONMENT_DETAILS],
        subjects=[
            "בעיה בהרשאות SharePoint — Permission denied on document library",
            "SharePoint permissions broken — مشكلة في الأذونات",
            "Cannot access {app} document library — הרשאות חסרות",
        ],
        descriptions=[
            "שלום,\n\n"
            "אני לא מצליח לגשת לספריית המסמכים ב-SharePoint.\n"
            "I'm getting a permissions error when I try to open the {department} "
            "document library on our SharePoint site.\n\n"
            "כשאני לוחץ על הקישור, אני מקבל שגיאה:\n"
            '"Access Denied — You do not have permission to access this resource."\n\n'
            "I was able to access this library last week without any issues. My colleague "
            "{name1} on Floor {floor} can still open it. Nothing changed on my end — same "
            "laptop, same credentials, same {os} build.\n\n"
            "תודה,\n{name}, {department}",
            "مرحبا فريق الدعم,\n\n"
            "I need help accessing the {department} SharePoint document library. "
            "لا أستطيع الوصول إلى المجلد المشترك.\n\n"
            "When I click the link I get a white page that says I don't have permission. "
            "My manager says my access should still be active. I haven't changed teams or "
            "roles recently.\n\n"
            "I'm at the {office} office, Floor {floor}, using {os}. The site URL is "
            "https://contoso.sharepoint.com/sites/{department}-docs.\n\n"
            "هل يمكنكم التحقق من الأذونات الخاصة بي؟\n\n"
            "شكرا,\n{name}, {department}",
        ],
        next_best_actions=[
            "Investigate SharePoint permission denial for the {department} document "
            "library — check if the user's access was removed during a recent permissions "
            "audit or group membership change.",
            "Verify the user's Azure AD group membership and SharePoint site collection "
            "permissions. The mixed RTL/LTR text is a normal bilingual submission — the "
            "core issue is a SharePoint access denial.",
        ],
        remediation_steps=[
            [
                "Check the user's Azure AD group membership for the {department} SharePoint group",
                "Review the SharePoint site collection permissions audit log for recent changes",
                "Verify the user's account is not disabled or flagged in Azure AD",
                "If permissions were removed, re-add the user to the appropriate SharePoint group",
                "Request the exact error message text or screenshot for further diagnosis",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# dc-133  HTML table paste — massive spreadsheet data with buried IT issue
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="dc-133",
        category=Category.DATA,
        priority=Priority.P2,
        assigned_team=Team.DATA_PLATFORM,
        needs_escalation=False,
        missing_information=[MissingInfo.AFFECTED_SYSTEM, MissingInfo.ERROR_MESSAGE],
        subjects=[
            "Data import failing — see table below with affected records",
            "ETL pipeline error on {app} — pasted raw data from spreadsheet",
            "Database load failure — here is the full dataset",
        ],
        descriptions=[
            "Hi team,\n\n"
            "Our daily ETL pipeline failed this morning. I'm pasting the raw data that "
            "was supposed to load so you can see what we're working with:\n\n"
            '<table border="1">\n'
            "<tr><th>RecordID</th><th>AccountName</th><th>Region</th><th>Amount</th>"
            "<th>Status</th><th>Date</th></tr>\n"
            "<tr><td>10001</td><td>Contoso East</td><td>AMER</td><td>45230.50</td>"
            "<td>PENDING</td><td>2026-04-01</td></tr>\n"
            "<tr><td>10002</td><td>Contoso West</td><td>AMER</td><td>78125.00</td>"
            "<td>COMPLETED</td><td>2026-04-01</td></tr>\n"
            "<tr><td>10003</td><td>Contoso EMEA</td><td>EMEA</td><td>23400.75</td>"
            "<td>FAILED</td><td>2026-04-01</td></tr>\n"
            "<tr><td>10004</td><td>Contoso APAC</td><td>APAC</td><td>91200.00</td>"
            "<td>PENDING</td><td>2026-04-01</td></tr>\n"
            "<tr><td>10005</td><td>Contoso North</td><td>AMER</td><td>12340.25</td>"
            "<td>COMPLETED</td><td>2026-04-01</td></tr>\n"
            "<tr><td>10006</td><td>Contoso South</td><td>LATAM</td><td>56780.00</td>"
            "<td>FAILED</td><td>2026-04-01</td></tr>\n"
            "<tr><td>10007</td><td>Contoso UK</td><td>EMEA</td><td>34560.50</td>"
            "<td>PENDING</td><td>2026-04-01</td></tr>\n"
            "<tr><td>10008</td><td>Contoso DE</td><td>EMEA</td><td>67890.00</td>"
            "<td>COMPLETED</td><td>2026-04-01</td></tr>\n"
            "<tr><td>10009</td><td>Contoso JP</td><td>APAC</td><td>22345.75</td>"
            "<td>FAILED</td><td>2026-04-01</td></tr>\n"
            "<tr><td>10010</td><td>Contoso AU</td><td>APAC</td><td>88900.00</td>"
            "<td>PENDING</td><td>2026-04-01</td></tr>\n"
            "</table>\n\n"
            "...there are about 50 more rows like this. The pipeline chokes somewhere "
            "around record 10003. I think it's a data type mismatch but I'm not sure. "
            "Floor {floor}, {department}.\n\n{name}",
            "The nightly data load into our reporting database failed again. Here's "
            "a dump of the source data (copied from Excel):\n\n"
            "RecordID | AccountName | Region | Amount | Status | Date\n"
            "10001 | Contoso East | AMER | 45230.50 | PENDING | 2026-04-01\n"
            "10002 | Contoso West | AMER | 78125.00 | COMPLETED | 2026-04-01\n"
            "10003 | Contoso EMEA | EMEA | $23,400.75 | FAILED | 04/01/2026\n"
            "10004 | Contoso APAC | APAC | 91200.00 | PENDING | 2026-04-01\n"
            "10005 | Contoso North | AMER | 12340.25 | COMPLETED | 2026-04-01\n"
            "10006 | Contoso South | LATAM | N/A | FAILED | 2026-04-01\n"
            "10007 | Contoso UK | EMEA | 34560.50 | PENDING | 2026-04-01\n"
            "10008 | Contoso DE | EMEA | 67890.00 | COMPLETED | 2026-04-01\n"
            "10009 | Contoso JP | APAC | 22345.75 | FAILED | 2026-04-01\n"
            "10010 | Contoso AU | APAC | 88900.00 | PENDING | 2026-04-01\n\n"
            "Notice record 10003 has a dollar sign and comma in the Amount column, and "
            "10006 has 'N/A' instead of a number. The date format also changes. I think "
            "these inconsistencies are causing the ETL to fail.\n\n"
            "{name}, {department}, Floor {floor}",
        ],
        next_best_actions=[
            "The ETL failure is caused by inconsistent data formatting in the source "
            "spreadsheet — mixed currency symbols, N/A values, and inconsistent date "
            "formats. Identify the specific records causing parse failures.",
            "Review the pasted data for format inconsistencies: dollar signs in numeric "
            "fields, 'N/A' strings in required columns, and mixed date formats. Fix the "
            "ETL validation rules or clean the source data.",
        ],
        remediation_steps=[
            [
                "Identify the ETL pipeline and target database/table that failed",
                "Check the ETL error logs for the specific record and column causing the failure",
                "Fix the source data: remove currency symbols, replace N/A with NULL, normalize date formats",
                "Add input validation rules to the ETL pipeline to handle common format variations",
                "Re-run the ETL pipeline with the corrected data",
                "Set up data quality checks on the source to prevent future inconsistencies",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# dc-134  Extreme OCR artifacts — scanned document with heavy OCR errors
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="dc-134",
        category=Category.HARDWARE,
        priority=Priority.P3,
        assigned_team=Team.ENDPOINT,
        needs_escalation=False,
        missing_information=[MissingInfo.DEVICE_INFO, MissingInfo.ERROR_MESSAGE],
        subjects=[
            "Sc4nner not w0rking — piease heIp",
            "Pr1nter/sc&nner jarn on Floor {floor}",
            "MFP dev1ce err0r — scanned t1cket attached",
        ],
        descriptions=[
            "He1lo IT Supp0rt,\n\n"
            "I arn wr1ting to rep0rt an 1ssue w1th the mult1-functi0n pr1nter/scanner "
            "on F1oor {floor} near the c0nference r00m. The dev1ce was mak1ng a gr1nding "
            "n01se when I tr1ed to sc4n a d0cument th1s m0rning.\n\n"
            "The LCD d1splay sh0wed an err0r c0de but I c0uldn't read 1t bef0re the "
            "screen went b1ank. The paper g0t jammed ins1de and I c0uldn't pull 1t 0ut "
            "w1thout r1sk1ng damage.\n\n"
            "I'm 1n the {office} 0ffice, {department} dep4rtment. The dev1ce is the "
            "1arge Ric0h un1t next to the k1tchen.\n\n"
            "PIease send s0meone to l00k at it.\n\n"
            "Th4nks,\n{name}",
            "T1cket fr0m scanned f0rm:\n\n"
            "Name: {name}\n"
            "Dep4rtment: {department}\n"
            "F1oor: {floor}\n"
            "0ffice: {office}\n\n"
            "Descr1pti0n of 1ssue:\nThe c0pier/scanner 0n our f1oor has a paper jarn "
            "that w0n't clear. We've tr1ed 0pening all the d00rs and trays but the "
            "paper 1s stuck 1n the fuser un1t. The dev1ce n0w sh0ws 'Service Requ1red' "
            "0n the d1splay.\n\n"
            "N0body 0n the f1oor can pr1nt or sc4n unt1l th1s is f1xed. Th1s 1s "
            "affect1ng ab0ut 15 pe0ple.\n\n"
            "Th4nk y0u",
        ],
        next_best_actions=[
            "Despite heavy OCR artifacts, the issue is a paper jam in the fuser unit "
            "of the multi-function printer/scanner on Floor {floor}. Dispatch a "
            "technician to clear the jam and check the fuser assembly.",
            "The OCR-garbled text describes a multi-function device showing 'Service "
            "Required' after a paper jam. The fuser unit needs physical inspection. "
            "This is blocking printing/scanning for approximately 15 users.",
        ],
        remediation_steps=[
            [
                "Dispatch an endpoint technician to Floor {floor} to inspect the multi-function device",
                "Clear the paper jam from the fuser unit following the manufacturer's procedure",
                "Check the fuser assembly for damage — if damaged, order a replacement part",
                "Run a test print and scan to verify the device is operational",
                "Request the device model and serial number for the asset inventory",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# dc-135  Terse one-word ticket — minimal information
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="dc-135",
        category=Category.GENERAL,
        priority=Priority.P4,
        assigned_team=Team.NONE,
        needs_escalation=False,
        missing_information=[
            MissingInfo.AFFECTED_SYSTEM,
            MissingInfo.ERROR_MESSAGE,
            MissingInfo.STEPS_TO_REPRODUCE,
            MissingInfo.DEVICE_INFO,
            MissingInfo.CONTACT_INFO,
            MissingInfo.ENVIRONMENT_DETAILS,
        ],
        subjects=[
            "help",
            "broken",
            "URGENT",
        ],
        descriptions=[
            "broken",
            "doesnt work",
        ],
        next_best_actions=[
            "The ticket contains no actionable information. Reach out to the submitter "
            "to gather basic details: what system or application is affected, what they "
            "were trying to do, and what happened.",
            "This is an incomplete ticket with no description of the issue. Contact the "
            "user to obtain the affected system, error message, steps to reproduce, and "
            "device information before triaging.",
        ],
        remediation_steps=[
            [
                "Contact the ticket submitter via email or Teams to request a description of the problem",
                "Ask what application or system is affected",
                "Ask for the error message or behavior they are seeing",
                "Ask what they were trying to do when the issue occurred",
                "Once sufficient information is gathered, re-triage and assign the ticket to the correct team",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# dc-136  Terminal output dump — PowerShell/ipconfig/tracert filling description
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="dc-136",
        category=Category.NETWORK,
        priority=Priority.P2,
        assigned_team=Team.NETWORK,
        needs_escalation=False,
        missing_information=[MissingInfo.NETWORK_LOCATION],
        subjects=[
            "Network issue — ipconfig and tracert output below",
            "Can't reach internal servers — pasted diagnostics",
            "Connectivity problem — see PowerShell output",
        ],
        descriptions=[
            "I can't reach any internal servers. Here's my diagnostics:\n\n"
            "PS C:\\Users\\{name1}> ipconfig /all\n\n"
            "Windows IP Configuration\n\n"
            "   Host Name . . . . . . . . . . . . : WS-{name1}-PC\n"
            "   Primary Dns Suffix  . . . . . . . : contoso.com\n"
            "   Node Type . . . . . . . . . . . . : Hybrid\n"
            "   IP Routing Enabled. . . . . . . . : No\n\n"
            "Ethernet adapter Ethernet0:\n\n"
            "   Connection-specific DNS Suffix  . : contoso.com\n"
            "   IPv4 Address. . . . . . . . . . . : 10.45.12.87\n"
            "   Subnet Mask . . . . . . . . . . . : 255.255.254.0\n"
            "   Default Gateway . . . . . . . . . : 10.45.12.1\n\n"
            "PS C:\\Users\\{name1}> tracert fileserver01.contoso.com\n\n"
            "Tracing route to fileserver01.contoso.com [10.10.1.50]\n"
            "over a maximum of 30 hops:\n\n"
            "  1    <1 ms    <1 ms    <1 ms  10.45.12.1\n"
            "  2     1 ms     1 ms     1 ms  10.45.0.1\n"
            "  3     *        *        *     Request timed out.\n"
            "  4     *        *        *     Request timed out.\n"
            "  5     *        *        *     Request timed out.\n\n"
            "Trace complete.\n\n"
            "PS C:\\Users\\{name1}> Test-NetConnection fileserver01.contoso.com -Port 445\n\n"
            "ComputerName     : fileserver01.contoso.com\n"
            "RemotePort       : 445\n"
            "TcpTestSucceeded : False\n\n"
            "So I can reach the gateway but nothing beyond the second hop. "
            "{department}, Floor {floor}.\n\n{name}",
            "Something is wrong with the network. Diagnostics below:\n\n"
            "C:\\> ipconfig\n"
            "   IPv4 Address: 10.45.12.93\n"
            "   Subnet: 255.255.254.0\n"
            "   Gateway: 10.45.12.1\n\n"
            "C:\\> ping 10.10.1.50\n"
            "Request timed out.\n"
            "Request timed out.\n"
            "Request timed out.\n"
            "Request timed out.\n\n"
            "C:\\> ping 10.45.12.1\n"
            "Reply from 10.45.12.1: bytes=32 time<1ms TTL=64\n"
            "Reply from 10.45.12.1: bytes=32 time<1ms TTL=64\n\n"
            "C:\\> nslookup fileserver01.contoso.com\n"
            "Server:  dc01.contoso.com\n"
            "Address:  10.10.1.10\n"
            "Name:    fileserver01.contoso.com\n"
            "Address:  10.10.1.50\n\n"
            "Gateway is reachable, DNS resolves, but file server is unreachable. "
            "I'm on {os} at the {office} office.\n\n{name}, {department}",
        ],
        next_best_actions=[
            "The diagnostics show the user can reach the local gateway (10.45.12.1) "
            "but traffic dies at the second hop toward the 10.10.1.0/24 subnet. "
            "Investigate routing between the 10.45.12.0/23 and 10.10.1.0/24 subnets.",
            "Network diagnostics indicate a routing failure between the user's VLAN "
            "(10.45.12.x) and the server VLAN (10.10.1.x). Check for ACL changes, "
            "route table issues, or a down inter-VLAN link.",
        ],
        remediation_steps=[
            [
                "Check the core router/firewall for routing between the 10.45.12.0/23 and 10.10.1.0/24 subnets",
                "Verify there are no recent ACL or firewall rule changes blocking inter-VLAN traffic",
                "Check the intermediate hop (10.45.0.1) for interface status and errors",
                "Verify fileserver01 (10.10.1.50) is up and responding to other clients",
                "Confirm the user's physical network location (building, floor, switch port) for VLAN verification",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# dc-137  Auto-generated monitoring alert — machine-formatted JSON dump
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="dc-137",
        category=Category.SOFTWARE,
        priority=Priority.P2,
        assigned_team=Team.ENTERPRISE_APPS,
        needs_escalation=False,
        missing_information=[MissingInfo.AFFECTED_USERS, MissingInfo.BUSINESS_IMPACT],
        subjects=[
            "[ALERT] AppDynamics — {app} response time threshold exceeded",
            "[MONITORING] Dynatrace alert: {app} error rate spike",
            "[AUTO] Synthetic monitor failure — {app} health check",
        ],
        descriptions=[
            "[ALERT GENERATED BY MONITORING SYSTEM — DO NOT REPLY TO THIS EMAIL]\n\n"
            "{{\n"
            '  "alertId": "MON-2026-04-10-0847",\n'
            '  "severity": "WARNING",\n'
            '  "source": "AppDynamics",\n'
            '  "application": "{app}",\n'
            '  "metric": "avg_response_time_ms",\n'
            '  "threshold": 2000,\n'
            '  "current_value": 8750,\n'
            '  "duration": "15m",\n'
            '  "environment": "PROD",\n'
            '  "affected_nodes": [\n'
            '    "app-node-01.contoso.com",\n'
            '    "app-node-02.contoso.com",\n'
            '    "app-node-03.contoso.com"\n'
            "  ],\n"
            '  "timestamp": "2026-04-10T08:47:23Z",\n'
            '  "status": "OPEN",\n'
            '  "runbook": "https://wiki.contoso.com/runbooks/{app}-perf"\n'
            "}}\n\n"
            "This alert was auto-forwarded to the IT Service Desk by the {department} "
            "on-call rotation.\n\n— Monitoring System",
            "[AUTOMATED ALERT]\n\n"
            "Alert: Synthetic monitor for {app} has failed 3 consecutive checks.\n"
            "Time: 2026-04-10 08:50 UTC\n"
            "Monitor: HTTPS health check — https://{app}.contoso.com/health\n"
            "Expected: HTTP 200 in < 5s\n"
            "Actual: HTTP 503 after 30s timeout\n\n"
            "Raw check output:\n"
            "  Check 1: 08:40 UTC — FAIL (503, 30012ms)\n"
            "  Check 2: 08:45 UTC — FAIL (503, 30008ms)\n"
            "  Check 3: 08:50 UTC — FAIL (503, 30015ms)\n\n"
            "Previous 24h success rate: 99.8%\n"
            "Current success rate: 0% (last 3 checks)\n\n"
            "Auto-generated by Contoso Monitoring. Forwarded to IT Service Desk.\n"
            "{department} on-call: {name}",
        ],
        next_best_actions=[
            "The monitoring alert shows {app} response times have spiked to 8750ms "
            "(threshold: 2000ms) across all production nodes. Follow the runbook and "
            "check application logs, database connections, and upstream dependencies.",
            "The synthetic health check for {app} is returning 503 errors. Verify the "
            "application is running on all nodes, check load balancer health, and review "
            "recent deployments that may have caused the outage.",
        ],
        remediation_steps=[
            [
                "Check the application status on all affected nodes (app-node-01 through 03)",
                "Review application logs for errors, stack traces, or dependency failures",
                "Check database and upstream service connectivity from the application nodes",
                "If a recent deployment occurred, consider rolling back to the last known good version",
                "Determine the number of affected users and business impact for priority assessment",
                "Follow the runbook linked in the alert for application-specific recovery steps",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# dc-138  Double-encoded UTF-8 (mojibake) — garbled accented characters
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="dc-138",
        category=Category.SOFTWARE,
        priority=Priority.P3,
        assigned_team=Team.ENTERPRISE_APPS,
        needs_escalation=False,
        missing_information=[MissingInfo.APPLICATION_VERSION, MissingInfo.STEPS_TO_REPRODUCE],
        subjects=[
            "Outlook displaying Ã©, Ã¼, Ã± instead of proper characters",
            "{app} showing garbled text — encoding issue?",
            "Email body shows mojibake characters after migration",
        ],
        descriptions=[
            "Hi support,\n\n"
            "Since the mailbox migration last weekend, all emails with accented "
            "characters are displaying incorrectly. For example:\n\n"
            "  - 'RÃ©sumÃ©' instead of 'Résumé'\n"
            "  - 'Ã\u009cber' instead of 'Über'\n"
            "  - 'El NiÃ±o' instead of 'El Niño'\n"
            "  - 'naÃ¯ve' instead of 'naïve'\n"
            "  - 'cafÃ©' instead of 'café'\n\n"
            "This affects both old emails that were migrated and new emails coming in "
            "from external contacts who use accented characters. Internal English-only "
            "emails look fine.\n\n"
            "I'm using {app} on {os}. I'm at the {office} office, Floor {floor}, "
            "{department}.\n\n"
            "This is really impacting my work because I correspond with our "
            "European and Latin American offices daily.\n\n{name}",
            "Bonjour,\n\n"
            "Depuis la migration, tous les caractÃ¨res spÃ©ciaux sont cassÃ©s "
            "dans {app}. Voici ce que je vois:\n\n"
            "  'caractÃ¨res' au lieu de 'caractères'\n"
            "  'spÃ©ciaux' au lieu de 'spéciaux'\n"
            "  'franÃ§ais' au lieu de 'français'\n\n"
            "Sorry, switching to English — the problem is that all accented characters "
            "in my email client are showing as double-encoded UTF-8 (mojibake). This "
            "started after the Exchange migration last Saturday.\n\n"
            "Emails I send also appear garbled to recipients. My colleague {name1} in "
            "{department} has the same problem. We're both on {os}, Floor {floor}.\n\n"
            "{name}, {department}",
        ],
        next_best_actions=[
            "This is a classic UTF-8 double-encoding issue (mojibake) that started "
            "after the Exchange mailbox migration. The migration likely re-encoded "
            "UTF-8 content as Latin-1 then back to UTF-8. Check the migration tool's "
            "encoding settings.",
            "The garbled characters (Ã© → é, Ã¼ → ü) indicate UTF-8 bytes being "
            "interpreted as Latin-1 and then re-encoded. Investigate the Exchange "
            "migration tool configuration and check if a mailbox repair can fix "
            "affected messages.",
        ],
        remediation_steps=[
            [
                "Verify the encoding settings used in the Exchange mailbox migration tool",
                "Check if the issue affects all migrated mailboxes or only a subset",
                "Request the user's {app} version and any custom encoding settings in the mail profile",
                "Run a mailbox content repair for affected users to fix double-encoded messages",
                "For new incoming emails, verify the mail transport rules are not altering encoding",
                "Test sending and receiving accented characters after the fix to confirm resolution",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# dc-139  Massive disclaimer chain — 90% legal disclaimers, real MFA issue buried
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="dc-139",
        category=Category.ACCESS_AUTH,
        priority=Priority.P2,
        assigned_team=Team.IAM,
        needs_escalation=False,
        missing_information=[MissingInfo.DEVICE_INFO, MissingInfo.AUTHENTICATION_METHOD],
        subjects=[
            "Re: FW: MFA not working — can't log in to {app}",
            "RE: FW: FW: Authentication failure — please help ASAP",
            "Fwd: Re: MFA push notifications stopped working",
        ],
        descriptions=[
            "I've been locked out of {app} since this morning because MFA push "
            "notifications aren't arriving on my phone. I've tried 5 times.\n\n"
            "--- Forwarded message ---\n"
            "From: {name} <{name1}@contoso.com>\n"
            "Date: April 10, 2026\n"
            "Subject: MFA not working\n"
            "To: helpdesk@contoso.com\n\n"
            "My MFA stopped working. Please help.\n\n"
            "------\n"
            "CONFIDENTIALITY NOTICE: This email and any attachments are for the "
            "exclusive and confidential use of the intended recipient. If you are not "
            "the intended recipient, please do not read, distribute, or take action "
            "based on this message. If you have received this in error, please notify "
            "the sender immediately by return email and delete this message from your "
            "system. Contoso Financial Services, 100 Market Street, {office}.\n\n"
            "AVIS DE CONFIDENTIALITÉ: Ce courriel et ses pièces jointes sont destinés "
            "exclusivement à l'usage confidentiel du destinataire prévu. Si vous n'êtes "
            "pas le destinataire prévu, veuillez ne pas lire, distribuer ou prendre de "
            "mesure sur la base de ce message.\n\n"
            "VERTRAULICHKEITSHINWEIS: Diese E-Mail und alle Anhänge sind ausschließlich "
            "für den vertraulichen Gebrauch des beabsichtigten Empfängers bestimmt.\n\n"
            "機密通知: このメールおよび添付ファイルは、意図された受信者のみを対象としています。\n\n"
            "إشعار السرية: هذا البريد الإلكتروني وأي مرفقات مخصصة للاستخدام الحصري والسري "
            "للمستلم المقصود.\n\n"
            "Sent from my iPhone\n\n"
            "---\n{name}, {department}, Floor {floor}",
            "Hi,\n\n"
            "My MFA has completely stopped working. I can't authenticate to any "
            "corporate app — {app}, SharePoint, Teams, nothing. The Authenticator "
            "app just spins and says 'No notification received.'\n\n"
            "I changed my phone last week — could that be related? I thought IT set "
            "up the new phone already.\n\n"
            "CONFIDENTIALITY NOTICE: This email and any attachments are confidential "
            "and intended solely for the use of the individual or entity to whom they "
            "are addressed. Any unauthorized review, use, disclosure or distribution "
            "is prohibited. If you have received this email in error, please contact "
            "the sender and destroy all copies. Contoso Financial Services.\n\n"
            "AVIS DE CONFIDENTIALITÉ: Ce courriel est confidentiel et destiné "
            "uniquement à la personne ou entité à laquelle il est adressé.\n\n"
            "VERTRAULICHKEITSHINWEIS: Diese E-Mail ist vertraulich und nur für die "
            "Person oder Organisation bestimmt, an die sie gerichtet ist.\n\n"
            "AVISO DE CONFIDENCIALIDAD: Este correo electrónico y sus archivos "
            "adjuntos son confidenciales y están destinados únicamente al uso del "
            "destinatario previsto.\n\n"
            "INFORMATIVA SULLA RISERVATEZZA: Questa email e qualsiasi allegato sono "
            "riservati e destinati esclusivamente all'uso del destinatario previsto.\n\n"
            "{name}, {department}, {office} office",
        ],
        next_best_actions=[
            "The actual issue (buried under multilingual disclaimers) is an MFA "
            "failure — push notifications are not arriving. The user may have recently "
            "changed phones without re-enrolling MFA. Reset MFA registration and "
            "re-enroll the new device.",
            "Strip away the disclaimer noise: the user cannot authenticate because "
            "MFA push notifications stopped working. Check if their Authenticator "
            "app registration is still valid and whether a recent phone change "
            "invalidated the enrollment.",
        ],
        remediation_steps=[
            [
                "Verify the user's MFA registration status in Azure AD / Entra ID",
                "Check if the user recently changed devices — if so, the old MFA registration is invalid",
                "Issue a temporary access pass so the user can re-enroll MFA on the new device",
                "Walk the user through re-registering the Microsoft Authenticator app",
                "Confirm the user can successfully authenticate to {app} and other corporate services",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# dc-140  Interleaved conversations — two email threads merged
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="dc-140",
        category=Category.HARDWARE,
        priority=Priority.P3,
        assigned_team=Team.ENDPOINT,
        needs_escalation=False,
        missing_information=[MissingInfo.DEVICE_INFO],
        subjects=[
            "Monitor flickering + software license question",
            "Two issues: display problem AND {app} license expired",
            "Re: Monitor issue (also: need a license for {app})",
        ],
        descriptions=[
            "Hi IT,\n\n"
            "Two separate issues — sorry for combining them, the portal was being slow.\n\n"
            "ISSUE 1 — MONITOR:\n"
            "My external monitor started flickering yesterday. It's a Dell U2722D connected "
            "via USB-C to my docking station. The flickering happens every few seconds — "
            "the screen goes black for half a second then comes back. It's worse when I "
            "have Teams video calls open. I've tried a different cable, same problem.\n\n"
            "ISSUE 2 — SOFTWARE LICENSE:\n"
            "Completely unrelated, but my {app} license expired last week and I'm getting "
            "a 'License required' banner every time I open it. My manager approved the "
            "renewal but I don't know who handles license assignments.\n\n"
            "For the monitor: I'm on Floor {floor}, {office} office, using a Lenovo "
            "ThinkPad with {os}. The dock is a Lenovo USB-C Gen 2.\n\n"
            "For the license: my user ID is {name1}@contoso.com.\n\n"
            "Thanks,\n{name}, {department}",
            "Wanted to flag two things:\n\n"
            "First, my monitor keeps cutting out. It flickers black every few seconds, "
            "sometimes for a split second, sometimes for 2-3 seconds. I'm using a dual "
            "monitor setup with a Dell dock on Floor {floor}. The left monitor (connected "
            "via DisplayPort) is fine — only the right one (USB-C) flickers.\n\n"
            "Second, totally different topic — I need a license for {app}. I got moved "
            "to the {department} team and they all use it. My old team didn't, so I "
            "never had a license. My manager already approved it in the request portal.\n\n"
            "For the monitor issue specifically, I noticed it happens more often when "
            "the laptop is charging through the dock. Could be a power issue with the "
            "USB-C port?\n\n"
            "Please advise on both.\n\n"
            "{name}, {department}",
        ],
        next_best_actions=[
            "This ticket contains two unrelated issues: (1) external monitor flickering "
            "via USB-C dock — likely a dock firmware, USB-C bandwidth, or power delivery "
            "issue; (2) an {app} license renewal/assignment. Split into two tickets.",
            "Separate the two issues: the monitor flicker should go to the endpoint/hardware "
            "team for dock and display diagnostics; the {app} license request should be "
            "routed to the software asset management team.",
        ],
        remediation_steps=[
            [
                "For the monitor flicker: update the docking station firmware to the latest version",
                "Test with a different USB-C dock or direct connection to rule out the dock",
                "Check if the USB-C port is providing enough power — try a powered dock or separate charger",
                "If the issue persists, request the monitor and dock model/serial for hardware replacement",
                "For the license: verify the manager's approval in the request portal and assign the {app} license",
                "Consider splitting this into two separate tickets for proper tracking",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# dc-141  PGP/S-MIME signed email block
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="dc-141",
        category=Category.HARDWARE,
        priority=Priority.P3,
        assigned_team=Team.ENDPOINT,
        needs_escalation=False,
        missing_information=[MissingInfo.DEVICE_INFO],
        subjects=[
            "Docking station not working — see signed email below",
            "USB-C dock issue (PGP-signed message)",
            "Re: Broken docking station — digitally signed",
        ],
        descriptions=[
            "-----BEGIN PGP SIGNED MESSAGE-----\n"
            "Hash: SHA256\n\n"
            "Hi support,\n\n"
            "My docking station stopped working this morning. "
            "I plug my laptop ({os}) into the dock via USB-C "
            "and nothing happens — no external monitors, no "
            "keyboard, no mouse. The dock power light is on. "
            "I'm on Floor {floor}, {office} office.\n\n"
            "Thanks,\n{name}\n"
            "-----BEGIN PGP SIGNATURE-----\n"
            "iQEzBAEBCAAdFiEEe4rk3LAxS+l5DUMMY"
            "PGPBLOCK0000000000000000000000000000"
            "0000000000000000000000000000000000000"
            "=ABCD\n"
            "-----END PGP SIGNATURE-----",
            "-----BEGIN PGP SIGNED MESSAGE-----\n"
            "Hash: SHA512\n\n"
            "Team,\n\n"
            "Docking station appears dead. When I connect my "
            "laptop, the dock LEDs flash once and then nothing "
            "registers — no displays, peripherals, or charging. "
            "I have tried two different USB-C cables. "
            "Laptop model is Lenovo ThinkPad running {os}. "
            "Location: {office}, Floor {floor}.\n\n"
            "Regards,\n{name}\n"
            "-----BEGIN PGP SIGNATURE-----\n"
            "iHUEARYKAB0WIQRzDUMMYSIGBLOCK00000"
            "0000000000000000000000000000000000000"
            "0000000000000000000000000000000000000"
            "=WXYZ\n"
            "-----END PGP SIGNATURE-----",
        ],
        next_best_actions=[
            "Ignore the PGP signature blocks — the real issue "
            "is a non-functional USB-C docking station. Gather "
            "dock make/model and test with a known-good dock.",
            "Strip the PGP envelope. The user reports a dead "
            "docking station (no video, peripherals, or charge "
            "over USB-C). Confirm dock model and firmware level.",
        ],
        remediation_steps=[
            [
                "Confirm the dock make, model, and firmware version",
                "Test the laptop with a different known-good dock",
                "Update the dock firmware to the latest release",
                "If the dock is still unresponsive, arrange a hardware replacement",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# dc-142  Extremely long CC/BCC headers
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="dc-142",
        category=Category.SOFTWARE,
        priority=Priority.P3,
        assigned_team=Team.ENTERPRISE_APPS,
        needs_escalation=False,
        missing_information=[MissingInfo.APPLICATION_VERSION],
        subjects=[
            "Outlook keeps crashing — email with 30+ CC list",
            "{app} crash when opening large-CC email",
            "Outlook freezes whenever I open a thread (huge CC)",
        ],
        descriptions=[
            "From: {name}@contoso.com\n"
            "To: helpdesk@contoso.com\n"
            "CC: userA@contoso.com; userB@contoso.com; "
            "userC@contoso.com; userD@contoso.com; "
            "userE@contoso.com; userF@contoso.com; "
            "userG@contoso.com; userH@contoso.com; "
            "userI@contoso.com; userJ@contoso.com; "
            "userK@contoso.com; userL@contoso.com; "
            "userM@contoso.com; userN@contoso.com; "
            "userO@contoso.com; userP@contoso.com; "
            "userQ@contoso.com; userR@contoso.com; "
            "userS@contoso.com; userT@contoso.com; "
            "userU@contoso.com; userV@contoso.com; "
            "userW@contoso.com; userX@contoso.com; "
            "userY@contoso.com; userZ@contoso.com; "
            "user27@contoso.com; user28@contoso.com; "
            "user29@contoso.com; user30@contoso.com\n\n"
            "Hi,\n\n"
            "My {app} (Outlook) crashes every time I try to "
            "open or reply to this email thread. It freezes "
            "for about 10 seconds and then closes with an "
            "error. I'm on {os}, Floor {floor}. This started "
            "after the latest update.\n\n"
            "Thanks,\n{name}",
        ],
        next_best_actions=[
            "The long CC list is noise from the original email "
            "headers. The real issue is {app} (Outlook) crashing "
            "when opening a thread. Collect the Outlook version "
            "and check for recent updates or known issues.",
            "Ignore the CC header block. The user's Outlook is "
            "crashing on a specific thread — possibly related "
            "to a recent update. Gather version and crash logs.",
        ],
        remediation_steps=[
            [
                "Collect the {app} (Outlook) version and build number",
                "Check for pending Office updates and apply them",
                "Clear the Outlook cache and restart the client",
                "If the crash persists, collect the crash dump and open a case with Microsoft support",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# dc-143  XML SOAP Fault dump
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="dc-143",
        category=Category.SOFTWARE,
        priority=Priority.P2,
        assigned_team=Team.ENTERPRISE_APPS,
        needs_escalation=False,
        missing_information=[
            MissingInfo.ERROR_MESSAGE,
            MissingInfo.ENVIRONMENT_DETAILS,
        ],
        subjects=[
            "SAP data sync failure — SOAP fault attached",
            "Integration error: SAP sync returns XML fault",
            "SAP connector throwing SOAP errors since this AM",
        ],
        descriptions=[
            "Hi team,\n\n"
            "Our SAP data sync has been failing since 06:00 "
            "this morning. Here is the fault we get:\n\n"
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            "<soap:Envelope "
            'xmlns:soap="http://schemas.xmlsoap.org/soap/'
            'envelope/">\n'
            "  <soap:Body>\n"
            "    <soap:Fault>\n"
            "      <faultcode>soap:Server</faultcode>\n"
            "      <faultstring>System.Exception: "
            "Data synchronization failed for module "
            "FI-GL — timeout exceeded while waiting "
            "for RFC destination "
            "SAP_PROD_01</faultstring>\n"
            "      <detail>\n"
            "        <ErrorCode>SYNC_TIMEOUT_001"
            "</ErrorCode>\n"
            "        <Timestamp>2025-01-15T06:02:31Z"
            "</Timestamp>\n"
            "        <Module>FI-GL</Module>\n"
            "      </detail>\n"
            "    </soap:Fault>\n"
            "  </soap:Body>\n"
            "</soap:Envelope>\n\n"
            "This is blocking month-end close. Please "
            "prioritize.\n\n"
            "{name}, {department}",
        ],
        next_best_actions=[
            "The SOAP fault XML is diagnostic context, not "
            "the issue itself. The real problem is that the "
            "SAP FI-GL data sync is timing out against RFC "
            "destination SAP_PROD_01 — blocking month-end.",
            "Extract the key error from the SOAP envelope: "
            "sync timeout on module FI-GL to SAP_PROD_01. "
            "Escalate to the SAP Basis / middleware team.",
        ],
        remediation_steps=[
            [
                "Verify connectivity to RFC destination SAP_PROD_01 from the middleware server",
                "Check the SAP application server for resource saturation (CPU, memory, work processes)",
                "Review the SAP sync job logs for additional error codes or timeouts",
                "Increase the RFC timeout threshold if the server is healthy but slow under month-end load",
                "Re-trigger the FI-GL sync job and monitor for successful completion",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# dc-144  Kubernetes pod describe output
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="dc-144",
        category=Category.SOFTWARE,
        priority=Priority.P2,
        assigned_team=Team.ENTERPRISE_APPS,
        needs_escalation=False,
        missing_information=[
            MissingInfo.ERROR_MESSAGE,
            MissingInfo.ENVIRONMENT_DETAILS,
        ],
        subjects=[
            "Payment service pod in CrashLoopBackOff",
            "K8s: payment-svc keeps crashing — kubectl output",
            "CrashLoopBackOff on payment service — urgent",
        ],
        descriptions=[
            "Hi,\n\n"
            "The payment service is down. Here is the output "
            "of kubectl describe pod:\n\n"
            "Name:         payment-svc-6b8f9c7d4-xk2lq\n"
            "Namespace:    prod-payments\n"
            "Priority:     0\n"
            "Node:         aks-nodepool1-12345678-vmss000003\n"
            "Start Time:   Wed, 15 Jan 2025 07:12:04 +0000\n"
            "Labels:       app=payment-svc\n"
            "              pod-template-hash=6b8f9c7d4\n"
            "Status:       Running\n"
            "IP:           10.244.3.17\n"
            "Containers:\n"
            "  payment-api:\n"
            "    Image:         acr.contoso.com/payment-"
            "svc:v2.14.3\n"
            "    Port:          8080/TCP\n"
            "    State:         Waiting\n"
            "      Reason:      CrashLoopBackOff\n"
            "    Last State:    Terminated\n"
            "      Reason:      OOMKilled\n"
            "      Exit Code:   137\n"
            "    Restart Count: 14\n"
            "    Limits:\n"
            "      cpu:     500m\n"
            "      memory:  256Mi\n"
            "    Requests:\n"
            "      cpu:     250m\n"
            "      memory:  128Mi\n"
            "Events:\n"
            "  Type     Reason     Message\n"
            "  ----     ------     -------\n"
            "  Warning  BackOff    Back-off restarting "
            "failed container\n"
            "  Warning  OOMKilling Memory limit exceeded\n\n"
            "Please investigate ASAP. This is impacting "
            "all customer transactions.\n\n"
            "{name}, {department}",
        ],
        next_best_actions=[
            "The kubectl describe output shows the payment-svc "
            "container is OOMKilled (exit code 137) with a "
            "256Mi memory limit. The pod is in CrashLoopBackOff "
            "after 14 restarts. Increase memory limits or "
            "investigate the memory leak.",
            "Strip the verbose pod description — the root cause "
            "is OOMKilled on the payment service container. "
            "Current limit is 256Mi which is insufficient.",
        ],
        remediation_steps=[
            [
                "Increase the memory limit for the payment-svc container (e.g., 512Mi or 1Gi) as a hot fix",
                "Review recent deployments for memory-regression changes (image v2.14.3)",
                "Collect heap dumps or memory profiles from a staging replica to find the leak",
                "Apply the permanent fix and redeploy, then monitor pod memory usage for 24 hours",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# dc-145  Raw hex dump (Wireshark capture)
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="dc-145",
        category=Category.NETWORK,
        priority=Priority.P2,
        assigned_team=Team.NETWORK,
        needs_escalation=False,
        missing_information=[
            MissingInfo.NETWORK_LOCATION,
            MissingInfo.ERROR_MESSAGE,
        ],
        subjects=[
            "TLS handshake failures — hex dump from Wireshark",
            "Packet capture shows TLS errors on {app} traffic",
            "Network: TLS issues — raw capture attached",
        ],
        descriptions=[
            "Team,\n\n"
            "We are seeing TLS handshake failures to "
            "{app}.contoso.com. I captured traffic with "
            "Wireshark — here is the hex dump of the "
            "failing ClientHello / ServerHello:\n\n"
            "0000  00 1c 42 00 00 08 00 1c  42 54 ab 19 08 00 45 00\n"
            "0010  00 f4 a3 29 40 00 40 06  00 00 0a 00 01 64 ac 1f\n"
            "0020  02 c8 c5 e0 01 bb 8e 1a  3b 4c 00 00 00 00 b0 02\n"
            "0030  ff ff 2c 0e 00 00 02 04  05 b4 01 03 03 08 01 01\n"
            "0040  04 02 16 03 01 00 bf 01  00 00 bb 03 03 64 1e 7d\n"
            "0050  9c 2f aa 3e 71 DEAD BEEF  CA FE BA BE 00 00 00 00\n"
            "0060  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00\n"
            "0070  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00\n"
            "0080  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00\n\n"
            "The failure happens on every connection attempt "
            "from our subnet. We suspect a cipher mismatch "
            "after the load balancer upgrade last night. "
            "Floor {floor}, building {office}.\n\n"
            "{name}, Network Ops",
        ],
        next_best_actions=[
            "The hex dump is raw packet data — the real issue "
            "is TLS handshake failures to {app}.contoso.com "
            "after a load balancer change. Check the LB cipher "
            "suite configuration.",
            "Ignore the hex payload. Focus on the TLS cipher "
            "mismatch between the client subnet and the load "
            "balancer that was upgraded last night.",
        ],
        remediation_steps=[
            [
                "Compare the load balancer's TLS cipher suite configuration before and after last night's upgrade",
                "Verify the server certificate chain is valid and correctly installed on the new LB config",
                "Test connectivity with openssl s_client from the affected subnet",
                "Restore a compatible cipher suite or update client-side TLS settings as needed",
                "Confirm TLS handshakes succeed and monitor for 24 hours",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# dc-146  Mixed encoding with U+FFFD replacement characters
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="dc-146",
        category=Category.NETWORK,
        priority=Priority.P3,
        assigned_team=Team.NETWORK,
        needs_escalation=False,
        missing_information=[
            MissingInfo.DEVICE_INFO,
            MissingInfo.NETWORK_LOCATION,
        ],
        subjects=[
            "WiFi keeps dropping \ufffd\ufffd connection issue",
            "Wireless disconnects \ufffd Floor {floor} \ufffd help",
            "Wi-Fi drops every few minutes \ufffd\ufffd\ufffd",
        ],
        descriptions=[
            "Hi IT,\n\n"
            "My Wi-Fi keeps dropping. Every 10\ufffd\ufffd"
            "15 minutes the connection dies and I have to "
            "reconnect manually. I\ufffdm on Floor {floor}, "
            "{office} office, using {os}.\n\n"
            "The SSID is \ufffdContoso-Corp\ufffd and the "
            "signal shows full bars right before it drops. "
            "Other people on my floor are having the same "
            "issue since Monday.\n\n"
            "I\ufffdve tried forgetting the network and "
            "re-joining, and I\ufffdve restarted my laptop "
            "twice. Nothing helps.\n\n"
            "Thanks,\n{name}\n\n"
            "[Note: this email was converted from a Latin-1 "
            "encoded source \ufffd some characters may appear "
            "as replacement glyphs.]",
        ],
        next_best_actions=[
            "The \ufffd characters are encoding artifacts "
            "(Latin-1 to UTF-8 conversion), not part of the "
            "issue. The real problem is intermittent WiFi "
            "drops on Floor {floor} affecting multiple users "
            "since Monday.",
            "Ignore the replacement characters. Multiple users "
            "on Floor {floor} are experiencing WiFi drops every "
            "10-15 minutes — likely an AP or controller issue.",
        ],
        remediation_steps=[
            [
                "Check the wireless access point(s) on "
                "Floor {floor} for firmware or configuration "
                "changes made around Monday",
                "Review the wireless controller logs for client disassociation events on that floor",
                "Verify channel utilization and interference levels on the affected APs",
                "Restart or replace the suspect access point and monitor connectivity for 24 hours",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# dc-147  SQL query results pasted as tab-separated output
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="dc-147",
        category=Category.DATA,
        priority=Priority.P2,
        assigned_team=Team.DATA_PLATFORM,
        needs_escalation=False,
        missing_information=[
            MissingInfo.AFFECTED_SYSTEM,
            MissingInfo.TIMESTAMP,
        ],
        subjects=[
            "Data corruption in trading system — SQL output",
            "Trade records showing wrong values — query results",
            "Urgent: corrupted rows in trade_ledger table",
        ],
        descriptions=[
            "Hi Data Platform team,\n\n"
            "We found corrupted records in the trading "
            "system. Here are the bad rows from our query:\n\n"
            "trade_id\taccount\tamount\tcurrency\tstatus\n"
            "T-992714\tACCT-001\t-999999.99\tUSD\tSETTLED\n"
            "T-992715\tACCT-001\t0.00\tUSD\tSETTLED\n"
            "T-992716\tACCT-002\t-999999.99\tEUR\tSETTLED\n"
            "T-992717\tACCT-003\t0.01\tGBP\tPENDING\n"
            "T-992718\tACCT-002\t-999999.99\tEUR\tSETTLED\n"
            "T-992719\tACCT-004\t50000.00\tUSD\tSETTLED\n"
            "T-992720\tACCT-001\t-999999.99\tUSD\tSETTLED\n"
            "T-992721\tACCT-005\t0.00\tJPY\tSETTLED\n\n"
            "The -999999.99 amounts appeared overnight and "
            "do not correspond to any real trades. This is "
            "impacting our reconciliation and P&L reports. "
            "We need this fixed before market open.\n\n"
            "{name}, {department}",
        ],
        next_best_actions=[
            "The SQL output is evidence of the problem, not "
            "noise. The real issue is spurious -999999.99 "
            "records appearing in the trade_ledger table "
            "overnight — likely a batch job or ETL defect.",
            "Corrupted trade records (sentinel value "
            "-999999.99) are polluting the ledger. Identify "
            "the process that inserted them and quarantine "
            "the affected rows before market open.",
        ],
        remediation_steps=[
            [
                "Quarantine the affected rows by flagging them (do NOT delete — audit trail required)",
                "Identify the ETL job or batch process that inserted the -999999.99 sentinel values",
                "Review the job logs and source data for the overnight run to find the root cause",
                "Fix the defective transformation logic and re-run the batch for the affected window",
                "Validate reconciliation totals and confirm P&L reports are correct before market open",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# dc-148  Massive multilingual legal disclaimer
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="dc-148",
        category=Category.ACCESS_AUTH,
        priority=Priority.P3,
        assigned_team=Team.IAM,
        needs_escalation=False,
        missing_information=[MissingInfo.AUTHENTICATION_METHOD],
        subjects=[
            "Password reset needed — please help",
            "Can't log in to {app} — password expired",
            "Account locked out — need password reset ASAP",
        ],
        descriptions=[
            "Hi,\n\n"
            "I need a password reset for my account "
            "({name}@contoso.com). I can't log in to "
            "{app} — it says my password has expired.\n\n"
            "Thanks,\n{name}\n\n"
            "---\n"
            "CONFIDENTIALITY NOTICE / AVIS DE "
            "CONFIDENTIALIT\u00c9:\n"
            "This email and any attachments are confidential "
            "and intended solely for the addressee. If you "
            "have received this in error, please notify the "
            "sender immediately and delete the message.\n\n"
            "VERTRAULICHKEITSHINWEIS:\n"
            "Diese E-Mail und alle Anh\u00e4nge sind "
            "vertraulich und ausschlie\u00dflich f\u00fcr den "
            "Adressaten bestimmt. Sollten Sie diese "
            "Nachricht irrt\u00fcmlich erhalten haben, "
            "informieren Sie bitte umgehend den Absender "
            "und l\u00f6schen Sie die Nachricht.\n\n"
            "\u6a5f\u5bc6\u4fdd\u6301\u306e\u304a\u77e5"
            "\u3089\u305b:\n"
            "\u3053\u306e\u30e1\u30fc\u30eb\u304a\u3088\u3073"
            "\u6dfb\u4ed8\u30d5\u30a1\u30a4\u30eb\u306f"
            "\u6a5f\u5bc6\u60c5\u5831\u3067\u3042\u308a\u3001"
            "\u540d\u5b9b\u4eba\u306e\u307f\u3092\u5bfe\u8c61"
            "\u3068\u3057\u3066\u3044\u307e\u3059\u3002"
            "\u8aa4\u3063\u3066\u53d7\u4fe1\u3055\u308c\u305f"
            "\u5834\u5408\u306f\u3001\u76f4\u3061\u306b"
            "\u9001\u4fe1\u8005\u306b\u3054\u9023\u7d61"
            "\u304f\u3060\u3055\u3044\u3002\n\n"
            "\u4fdd\u5bc6\u58f0\u660e:\n"
            "\u672c\u90ae\u4ef6\u53ca\u5176\u9644\u4ef6"
            "\u5747\u4e3a\u673a\u5bc6\u4fe1\u606f\uff0c"
            "\u4ec5\u4f9b\u6536\u4ef6\u4eba\u4f7f\u7528"
            "\u3002\u5982\u60a8\u8bef\u6536\u6b64\u90ae"
            "\u4ef6\uff0c\u8bf7\u7acb\u5373\u901a\u77e5"
            "\u53d1\u4ef6\u4eba\u5e76\u5220\u9664\u3002\n\n"
            "AVIS DE CONFIDENTIALIT\u00c9 (FR):\n"
            "Ce courriel et ses pi\u00e8ces jointes sont "
            "confidentiels et destin\u00e9s uniquement "
            "\u00e0 leur destinataire. Si vous avez re\u00e7u "
            "ce message par erreur, veuillez en informer "
            "l'exp\u00e9diteur imm\u00e9diatement et "
            "supprimer le message.",
        ],
        next_best_actions=[
            "The multilingual legal disclaimer (EN/DE/JP/ZH/"
            "FR) is standard email boilerplate — ignore it. "
            "The actual request is a simple password reset "
            "for {name}@contoso.com.",
            "Strip the five-language confidentiality footer. "
            "The user needs a password reset — verify their "
            "identity and process the reset.",
        ],
        remediation_steps=[
            [
                "Verify the user's identity using the organization's identity verification procedure",
                "Check whether the account is locked out or merely has an expired password",
                "Issue a temporary password or a self-service password reset link via the IAM portal",
                "Confirm the user can log in to {app} with the new credentials",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# dc-149  Near-empty ticket — "See attached screenshot"
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="dc-149",
        category=Category.HARDWARE,
        priority=Priority.P3,
        assigned_team=Team.ENDPOINT,
        needs_escalation=False,
        missing_information=[
            MissingInfo.DEVICE_INFO,
            MissingInfo.SCREENSHOT_OR_ATTACHMENT,
            MissingInfo.STEPS_TO_REPRODUCE,
        ],
        subjects=[
            "Monitor not working — see attachment",
            "Display issue (screenshot attached)",
            "External monitor problem",
        ],
        descriptions=[
            "See attached screenshot.\n\nThanks,\n{name}",
            "Hi, my monitor isn't working. I attached a "
            "screenshot showing the problem.\n\n"
            "(No further details provided.)\n\n"
            "{name}, Floor {floor}",
        ],
        next_best_actions=[
            "The ticket body is nearly empty — no device "
            "info, no description of symptoms, and any "
            "referenced screenshot is not available as text. "
            "Reach out to {name} for monitor make/model, "
            "connection type, and symptom details.",
            "Insufficient information. The user says their "
            "monitor is not working but provides no detail. "
            "Request device info, connection type, and a "
            "description of what they see (no signal, "
            "flickering, black screen, etc.).",
        ],
        remediation_steps=[
            [
                "Contact {name} to collect monitor make/model, connection type (HDMI, USB-C, DP), and laptop model",
                "Ask the user to describe the symptom: no signal, black screen, flickering, or distorted image",
                "Once details are gathered, test with a different cable and port to isolate the issue",
                "If hardware is faulty, initiate a replacement request for the monitor or cable",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# dc-150  Vulnerability scanner report dump (Nessus/Qualys)
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="dc-150",
        category=Category.SECURITY,
        priority=Priority.P2,
        assigned_team=Team.SECOPS,
        needs_escalation=False,
        missing_information=[MissingInfo.AFFECTED_SYSTEM],
        subjects=[
            "TLS certificate expiring — vuln scan report",
            "Cert expiry flagged by Nessus — action needed",
            "Qualys scan: critical TLS cert about to expire",
        ],
        descriptions=[
            "Hi SecOps,\n\n"
            "Our weekly vulnerability scan flagged a bunch "
            "of findings. Pasting the summary — the one we "
            "care about is the TLS cert expiry.\n\n"
            "Plugin 10863 | SSL Certificate Expiry | "
            "Critical\n"
            "  Host: app01.contoso.com:443\n"
            "  Cert expires: 2025-02-01\n\n"
            "Plugin 42873 | SSL Medium Strength Ciphers | "
            "Medium\n"
            "  Host: app02.contoso.com:443\n\n"
            "Plugin 65821 | TLS 1.0 Enabled | Low\n"
            "  Host: legacy.contoso.com:8443\n\n"
            "Plugin 56984 | SSH Weak MAC Algorithms | Low\n"
            "  Host: bastion.contoso.com:22\n\n"
            "Plugin 11219 | Nessus SYN Scanner | Info\n"
            "  Host: app01.contoso.com (multiple ports)\n\n"
            "Plugin 10881 | SSH Protocol Version | Info\n"
            "  Host: bastion.contoso.com:22\n\n"
            "Plugin 22964 | Service Detection | Info\n"
            "  Host: app01.contoso.com, app02.contoso.com\n\n"
            "Plugin 10287 | Traceroute Information | Info\n"
            "  Host: 10.0.0.0/24 (multiple)\n\n"
            "Plugin 19506 | Nessus Scan Information | Info\n"
            "  Scan completed: 2025-01-15 03:45 UTC\n\n"
            "Plugin 10180 | Ping Host | Info\n"
            "  Host: (all in-scope hosts)\n\n"
            "Plugin 45590 | Common Platform Enum | Info\n"
            "  Host: app01.contoso.com\n\n"
            "Plugin 54615 | Device Type | Info\n"
            "  Host: bastion.contoso.com\n\n"
            "Plugin 25220 | TCP Timestamps | Info\n"
            "  Host: app01.contoso.com, app02.contoso.com\n\n"
            "Plugin 11936 | OS Identification | Info\n"
            "  Host: bastion.contoso.com\n\n"
            "Plugin 10114 | ICMP Timestamp Reply | Info\n"
            "  Host: 10.0.0.0/24 (multiple)\n\n"
            "Plugin 25221 | Remote listeners | Info\n"
            "  Host: app01.contoso.com (8 services)\n\n"
            "Plugin 33929 | PCI DSS Compliance | Info\n"
            "  Status: Non-compliant (2 findings)\n\n"
            "Plugin 84239 | TLS NPN Extensions | Info\n"
            "  Host: app01.contoso.com:443\n\n"
            "Plugin 56468 | Time of Last Reboot | Info\n"
            "  Host: bastion.contoso.com (42 days)\n\n"
            "The critical one is the cert on "
            "app01.contoso.com — it expires Feb 1. "
            "Everything else is lower priority.\n\n"
            "{name}, {department}",
        ],
        next_best_actions=[
            "The scan report lists 20+ findings, but only "
            "one is critical: the TLS certificate on "
            "app01.contoso.com:443 expires 2025-02-01. "
            "Prioritize renewing that certificate.",
            "Ignore the informational scanner noise. The "
            "actionable item is the imminent TLS cert expiry "
            "on app01.contoso.com. Renew and redeploy the "
            "certificate before Feb 1.",
        ],
        remediation_steps=[
            [
                "Identify the certificate authority and the team that owns app01.contoso.com",
                "Submit a certificate renewal request or generate a new CSR for the domain",
                "Install the renewed certificate on app01.contoso.com and the associated load balancer",
                "Verify the new certificate with openssl s_client and confirm the expiry date is extended",
                "Schedule a follow-up to address the medium/"
                "low findings (weak ciphers, TLS 1.0) in "
                "the next maintenance window",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# dc-151  CSV injection formulas in ticket description
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="dc-151",
        category=Category.SOFTWARE,
        priority=Priority.P2,
        assigned_team=Team.ENTERPRISE_APPS,
        needs_escalation=False,
        missing_information=[MissingInfo.APPLICATION_VERSION],
        subjects=[
            "CRM export contains dangerous formula cells",
            "CSV export from CRM has =CMD and =HYPERLINK entries",
            "Data export broken — Excel shows security warnings",
        ],
        descriptions=[
            "I exported client data from the CRM and the CSV has entries like:\n\n"
            "Name,Email,Revenue,Notes\n"
            '"Johnson & Co","j.co@example.com","$1.2M","=CMD(\'calc\')!A0"\n'
            '"Acme Corp","acme@example.com","$850K","=HYPERLINK(\\"http://evil.example.com\\")"\n'
            '"Beta Inc","beta@example.com","$2.1M","+THUNK(\'-o evil.bat\')"\n\n'
            "When I open it in Excel it triggers security warnings. "
            "The export worked fine last month.\n\n{name}, {department}",
            "The CRM data export module is producing CSV files with "
            "formula injection patterns. Cells contain =CMD, =HYPERLINK, "
            "and @SUM entries that aren't real data. Excel blocks the file "
            "with a security warning. We need this data for the quarterly "
            "board report due Friday.\n\n{name}, {department}",
        ],
        next_best_actions=[
            "Investigate the CRM export module for formula injection "
            "in CSV output — likely unsanitized user input in the Notes field.",
        ],
        remediation_steps=[
            [
                "Check the CRM export code for proper CSV sanitization of user-supplied fields",
                "Ensure all cells starting with =, +, -, @ are prefixed with a single quote",
                "Re-export the data after applying the fix and verify in Excel",
                "Deliver the clean export for the board report deadline",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# dc-152  GPG/PGP signed email wrapping hardware issue
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="dc-152",
        category=Category.HARDWARE,
        priority=Priority.P3,
        assigned_team=Team.ENDPOINT,
        needs_escalation=False,
        missing_information=[MissingInfo.DEVICE_INFO],
        subjects=[
            "Docking station not detecting monitors",
            "External displays not working via dock",
            "Thunderbolt dock — no video output",
        ],
        descriptions=[
            "-----BEGIN PGP SIGNED MESSAGE-----\n"
            "Hash: SHA256\n\n"
            "My Dell WD19TBS docking station stopped detecting both monitors "
            "(Dell U2722D) after the latest Windows Update (KB5034441). The dock "
            "power light is on and USB devices work, but DisplayPort shows no signal.\n\n"
            "Tried: unplugging Thunderbolt cable, restarting laptop, different DP cables, "
            "connecting monitors directly to HDMI (works). Seems like a dock driver issue.\n\n"
            "{name}, {department}\n\n"
            "-----BEGIN PGP SIGNATURE-----\n\n"
            "iQIzBAEBCAAdFiEEaBC2K3FW1DqSNk5RVd4q+UCYcRQF\n"
            "AmXfL+gACgkQVd4q+UCYcRTMVA/+JX5GBHKP3dZ9c2Xq\n"
            "=dK9f\n"
            "-----END PGP SIGNATURE-----",
            "-----BEGIN PGP SIGNED MESSAGE-----\n"
            "Hash: SHA512\n\n"
            "Thunderbolt dock stopped working after update. USB peripherals are fine "
            "but both external monitors show 'No Signal'. Laptop is a ThinkPad X1 "
            "Carbon Gen 11 running Windows 11 23H2.\n\n"
            "{name}, {department}\n\n"
            "-----BEGIN PGP SIGNATURE-----\n"
            "iQEzBAEBCAAdFiEE5R1om3qlCq8AAAAAAAAAAAAAAA\n"
            "=abc1\n"
            "-----END PGP SIGNATURE-----",
        ],
        next_best_actions=[
            "Troubleshoot dock video output — likely a Thunderbolt/DisplayPort driver "
            "regression from the recent Windows Update. Ignore PGP signature noise.",
        ],
        remediation_steps=[
            [
                "Check for updated Thunderbolt and DisplayPort drivers from Dell and Lenovo",
                "Roll back KB5034441 if the driver update doesn't resolve the issue",
                "Test with a different dock to rule out hardware failure",
                "Verify display output works with a direct HDMI connection as a workaround",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# dc-153  Zalgo text with combining Unicode diacritics
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="dc-153",
        category=Category.SOFTWARE,
        priority=Priority.P2,
        assigned_team=Team.ENTERPRISE_APPS,
        needs_escalation=False,
        missing_information=[MissingInfo.ERROR_MESSAGE],
        subjects=[
            "O\u0336\u0317u\u0337\u031et\u0334\u0318l\u0335\u031fo\u0337\u0316o\u0336\u0320k crashes on startup",
            "Outlook not responding after update",
            "Email client crashing — Z\u0336\u0319a\u0335\u031dl\u0337\u031fg\u0334\u0320o text in display",
        ],
        descriptions=[
            "E\u0336\u0319v\u0335\u031de\u0334\u031er\u0336\u0320y time I open Outlook it freezes "
            "for 30 seconds then shows 'Not responding' and crashes. Started after "
            "T\u0336\u031du\u0337\u031fe\u0334\u0320s\u0335\u031ed\u0336\u0317a\u0337\u0319y's update.\n\n"
            "Tried: Repair from Control Panel, safe mode, deleting .ost file.\n"
            "Version: Microsoft 365 v2402, OS: Windows 11 23H2\n"
            "Mailbox: ~12 GB\n\n{name}, {department}",
            "Outlook 365 desktop c\u0336\u031dr\u0337\u031fa\u0334\u0320s\u0335\u031eh\u0336\u0317e\u0337\u0319s "
            "within 30 seconds of opening. The text in error dialogs has garbled "
            "combining characters. M\u0336\u031dy mailbox is about 14 GB. This is "
            "blocking all email communication.\n\n{name}, {department}",
        ],
        next_best_actions=[
            "Diagnose Outlook crash — likely a corrupt profile or oversized mailbox "
            "after the recent update. Ignore Zalgo text artifacts in the description.",
        ],
        remediation_steps=[
            [
                "Create a new Outlook profile and re-add the email account",
                "If the crash persists, reduce mailbox size by archiving old emails",
                "Check for and install the latest Office update to patch known crash bugs",
                "If all else fails, uninstall and reinstall Microsoft 365 Apps",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# dc-154  Deeply nested JSON payload pasted in description
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="dc-154",
        category=Category.DATA,
        priority=Priority.P2,
        assigned_team=Team.DATA_PLATFORM,
        needs_escalation=False,
        missing_information=[MissingInfo.ENVIRONMENT_DETAILS],
        subjects=[
            "API returning deeply nested JSON errors",
            "Database API timeout — pasting response payload",
            "Analytics endpoint returning malformed JSON",
        ],
        descriptions=[
            "The reporting API returns this response:\n\n"
            + "{" * 55
            + '"error":"connection_timeout"'
            + "}" * 55
            + "\n\nThis started about 2 hours ago. The endpoint is "
            "https://api.internal.contoso.com/v2/analytics/quarterly-revenue.\n\n"
            "{name}, {department}",
            "Our analytics database API is timing out. Here's the JSON:\n\n"
            + "{" * 60
            + '"status":"pool_exhausted"'
            + "}" * 60
            + "\n\nThe CFO's dashboard depends on this refreshing every 15 minutes.\n\n"
            "{name}, {department}",
        ],
        next_best_actions=[
            "Investigate the analytics API timeout — the deeply nested JSON "
            "is likely an error response wrapping. Check database connection pool.",
        ],
        remediation_steps=[
            [
                "Check the database connection pool for the analytics API",
                "Review recent configuration changes to the API or database",
                "Increase pool size or investigate slow queries causing pool exhaustion",
                "Restart the API service if the pool is in a bad state",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# dc-155  Raw SQL query output with ASCII table formatting
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="dc-155",
        category=Category.DATA,
        priority=Priority.P2,
        assigned_team=Team.DATA_PLATFORM,
        needs_escalation=False,
        missing_information=[MissingInfo.TIMESTAMP],
        subjects=[
            "Data corruption in client_accounts table",
            "SQL query shows corrupted balance data after ETL",
            "Database records have NULL and overflow values",
        ],
        descriptions=[
            "Ran this query and found corrupted data:\n\n"
            "SELECT account_id, client_name, balance FROM client_accounts "
            "WHERE region = 'EMEA' ORDER BY last_updated DESC;\n\n"
            "+------------+-------------------+-------------+\n"
            "| account_id | client_name       | balance     |\n"
            "+------------+-------------------+-------------+\n"
            "| ACC-10042  | Müller GmbH       | $1,234.56   |\n"
            "| ACC-10043  | Société Générale  | $-999999.99 |\n"
            "| ACC-10044  | Barclays PLC      | $0.00       |\n"
            "| ACC-10045  | Deutsche Bank     | NULL        |\n"
            "| ACC-10046  | BNP Paribas       | $########   |\n"
            "+------------+-------------------+-------------+\n\n"
            "Negative balances, NULLs, and overflow characters. "
            "The ETL batch ran last night.\n\n{name}, {department}",
        ],
        next_best_actions=[
            "Investigate data corruption from the overnight ETL batch — "
            "ACC-10043 through ACC-10046 have invalid balance values.",
        ],
        remediation_steps=[
            [
                "Identify the ETL job that ran last night and check its logs for errors",
                "Compare the corrupted records with the source data to find the transformation bug",
                "Restore the affected records from the last good backup",
                "Fix the ETL pipeline and add validation checks for negative/NULL/overflow values",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# dc-156  S/MIME digital signature block in access ticket
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="dc-156",
        category=Category.ACCESS_AUTH,
        priority=Priority.P2,
        assigned_team=Team.IAM,
        needs_escalation=False,
        missing_information=[MissingInfo.AUTHENTICATION_METHOD],
        subjects=[
            "Need MFA re-enrollment — lost my phone",
            "Can't complete MFA — authenticator app gone",
            "MFA reset needed after phone replacement",
        ],
        descriptions=[
            'Content-Type: multipart/signed; protocol="application/pkcs7-signature"; '
            'micalg=sha-256; boundary="----=_Part_12345"\n\n'
            "------=_Part_12345\nContent-Type: text/plain\n\n"
            "I lost my phone and can't do MFA. Need my authenticator re-enrolled "
            "on my new device. Username: {name1}, {office} office.\n\n"
            "{name}, {department}\n\n"
            "------=_Part_12345\nContent-Type: application/pkcs7-signature\n"
            "Content-Transfer-Encoding: base64\n\n"
            "MIAGCSqGSIb3DQEHAqCAMIACAQExDzANBglghkgBZQME\n"
            "AgEFADALBgkqhkiG9w0BBwGggDCCA1IwggI6oAMCAQIC\n"
            "------=_Part_12345--",
        ],
        next_best_actions=[
            "Process MFA re-enrollment request after identity verification. "
            "Ignore S/MIME signature noise in the email.",
        ],
        remediation_steps=[
            [
                "Verify the user's identity through an alternate channel (manager approval or in-person)",
                "Reset the MFA registration for the user's account in Azure AD",
                "Guide the user through re-enrolling their new device in the Authenticator app",
                "Confirm the user can sign in successfully with the new MFA method",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# dc-157  Near-empty body ("Sent from my iPhone")
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="dc-157",
        category=Category.NETWORK,
        priority=Priority.P3,
        assigned_team=Team.NETWORK,
        needs_escalation=False,
        missing_information=[
            MissingInfo.ERROR_MESSAGE,
            MissingInfo.DEVICE_INFO,
            MissingInfo.STEPS_TO_REPRODUCE,
        ],
        subjects=[
            "Can't connect to VPN from home — URGENT",
            "VPN broken from remote — please help",
            "GlobalProtect won't connect — working from home",
        ],
        descriptions=[
            "Sent from my iPhone",
            "\n\nSent from my iPhone\n",
            "Sent from my Samsung Galaxy",
        ],
        next_best_actions=[
            "Contact the user for details — the ticket body is empty except "
            "for a mobile email signature. The subject suggests a VPN issue.",
        ],
        remediation_steps=[
            [
                "Reach out to the user by phone or chat to gather more details",
                "Once details are collected, troubleshoot the VPN connection",
                "Check if the VPN gateway is reachable from the user's network",
                "Verify the user's VPN client version and credentials are current",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# dc-158  Auto-generated JIRA notification with transition history
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="dc-158",
        category=Category.SOFTWARE,
        priority=Priority.P1,
        assigned_team=Team.ENTERPRISE_APPS,
        needs_escalation=True,
        missing_information=[MissingInfo.ENVIRONMENT_DETAILS],
        subjects=[
            "[JIRA] (DEPLOY-4521) Production deployment failed",
            "[JIRA] (DEPLOY-4522) Deploy to prod-east blocked",
            "[JIRA] Production release pipeline failed — critical",
        ],
        descriptions=[
            "This message was sent automatically by Jira.\n\n"
            "DEPLOY-4521 — Production deployment failed\n"
            "Status: Open → In Progress → Blocked → Reopened → In Progress\n"
            "Priority: Critical → Major → Critical\n"
            "Assignee: DevOps → {name1} → Unassigned → {name}\n"
            "Reporter: CI/CD Pipeline\n\n"
            "--- Change History ---\n"
            "18/Mar/26 08:01 - Pipeline: Status Open → In Progress\n"
            "18/Mar/26 08:15 - Pipeline: Build #4521 passed\n"
            "18/Mar/26 08:22 - Pipeline: Deployment to prod-east FAILED\n"
            "18/Mar/26 09:10 - {name}: The payment-service pod can't connect "
            "to PostgreSQL RDS. Connection string PAYMENT_DB_URL points to "
            "staging. Helm chart values not updated for prod overlay.\n\n"
            "If you do not wish to receive notifications, update JIRA preferences.",
        ],
        next_best_actions=[
            "Extract the real issue from the JIRA noise: production deployment "
            "failed because the Helm chart values point to the staging database.",
        ],
        remediation_steps=[
            [
                "Fix the Helm chart production overlay to use the correct database connection string",
                "Redeploy the payment-service to the prod-east cluster",
                "Verify database connectivity in the production environment",
                "Add a CI/CD gate that validates environment-specific configuration before deployment",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# dc-159  Windows registry export pasted as description
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="dc-159",
        category=Category.SOFTWARE,
        priority=Priority.P2,
        assigned_team=Team.ENTERPRISE_APPS,
        needs_escalation=False,
        missing_information=[MissingInfo.ERROR_MESSAGE],
        subjects=[
            "Bloomberg Terminal won't launch — registry dump attached",
            "Bloomberg app crashing on startup — reg export below",
            "Trading terminal not starting — registry issue?",
        ],
        descriptions=[
            "Bloomberg Terminal won't start. Exported the registry keys:\n\n"
            "Windows Registry Editor Version 5.00\n\n"
            "[HKEY_LOCAL_MACHINE\\SOFTWARE\\Bloomberg L.P.\\Terminal]\n"
            '"InstallPath"="C:\\\\blp\\\\API"\n'
            '"Version"="2024.1.45.3"\n'
            '"CrashCount"=dword:00000007\n\n'
            "[HKEY_LOCAL_MACHINE\\SOFTWARE\\Bloomberg L.P.\\Terminal\\Network]\n"
            '"ProxyEnabled"=dword:00000001\n'
            '"ProxyServer"="proxy.contoso.com:8080"\n\n'
            "CrashCount is 7. Started after proxy config changed last week.\n\n"
            "{name}, {department}",
        ],
        next_best_actions=[
            "Bloomberg Terminal crashing due to proxy configuration change. "
            "Update the proxy settings or add proxy bypass rules.",
        ],
        remediation_steps=[
            [
                "Verify the new proxy configuration is compatible with Bloomberg's requirements",
                "Add *.bloomberg.com and *.bbterminal.com to the proxy bypass list",
                "Clear the CrashCount registry value and restart the Bloomberg Terminal",
                "If the issue persists, reinstall the Bloomberg Terminal client",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# dc-160  Python traceback with very deep stack
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="dc-160",
        category=Category.SOFTWARE,
        priority=Priority.P1,
        assigned_team=Team.ENTERPRISE_APPS,
        needs_escalation=True,
        missing_information=[MissingInfo.ENVIRONMENT_DETAILS],
        subjects=[
            "Internal API returning 500 — deep traceback",
            "Portfolio analytics API down — pasting stack trace",
            "API 500 errors after deploy — traceback below",
        ],
        descriptions=[
            "Our portfolio analytics API started returning 500s. Traceback:\n\n"
            "Traceback (most recent call last):\n"
            + "\n".join(
                f'  File "/app/services/layer_{i}/handler.py", line {10 + i}, in process\n'
                f"    return next_layer.process(ctx)"
                for i in range(40)
            )
            + '\n  File "/app/db/pool.py", line 42, in acquire\n'
            "    raise ConnectionError(\n"
            "ConnectionError: Pool exhausted (max=20, in_use=20, waiting=47)\n\n"
            "Started after deploying v2.14.3 this afternoon.\n\n{name}, {department}",
        ],
        next_best_actions=[
            "Database connection pool exhausted after deploy v2.14.3 — "
            "investigate the middleware chain for connection leaks.",
        ],
        remediation_steps=[
            [
                "Roll back to v2.14.2 if the connection leak is confirmed",
                "Investigate the new code in v2.14.3 for unclosed database connections",
                "Increase the connection pool size as a temporary workaround",
                "Add connection pool monitoring and alerting",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# dc-161  URLs with extremely long tracking parameters
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="dc-161",
        category=Category.SOFTWARE,
        priority=Priority.P3,
        assigned_team=Team.ENTERPRISE_APPS,
        needs_escalation=False,
        missing_information=[MissingInfo.AFFECTED_SYSTEM],
        subjects=[
            "Can't edit document in SharePoint — permission error",
            "SharePoint document access denied",
            "Permission error on SharePoint link",
        ],
        descriptions=[
            "When I click this link I get a permission error:\n\n"
            "https://contoso.sharepoint.com/sites/ProjectAtlas/_layouts/15/Doc.aspx?"
            "sourcedoc=%7B4a5b6c7d%7D&action=edit"
            + "&utm_source="
            + "a" * 200
            + "&utm_campaign="
            + "b" * 200
            + "&sdata="
            + "x" * 300
            + "\n\nI was added to the team last week but can't edit documents.\n\n"
            "{name}, {department}",
        ],
        next_best_actions=[
            "Check SharePoint site permissions for the user — ignore the "
            "extremely long tracking URLs in the ticket description.",
        ],
        remediation_steps=[
            [
                "Verify the user is a member of the correct SharePoint group",
                "Check if the user has Edit permissions on the document library",
                "If not, add the user to the appropriate SharePoint group",
                "Test that the user can access and edit documents after the change",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# dc-162  Multiple conflicting auto-reply/OOO chains
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="dc-162",
        category=Category.HARDWARE,
        priority=Priority.P3,
        assigned_team=Team.ENDPOINT,
        needs_escalation=False,
        missing_information=[MissingInfo.NETWORK_LOCATION],
        subjects=[
            "RE: RE: RE: Network printer offline on 4th floor",
            "FW: RE: FW: Printer down — auto-replies attached",
            "RE: RE: Printer issue — OOO replies flooding thread",
        ],
        descriptions=[
            "I am currently out of the office until March 25. For urgent matters, "
            "contact Dana Wright at d.wright@contoso.com.\n— Tomasz Kowalski\n\n---\n"
            "Thank you for your message. I am on PTO until March 22.\n— Lisa Chen\n\n---\n"
            "Auto-reply: Attending a conference this week.\n— Kevin O'Brien\n\n---\n"
            "Original from {name}:\n\nThe network printer on the 4th floor "
            "(HP LaserJet M507, PRN-4F-01) has been offline since this morning. "
            "LCD shows 'Network Error - Check Cable'. Ethernet cable is plugged in. "
            "Other devices on the same wall jack work fine.\n\n{name}, {department}",
        ],
        next_best_actions=[
            "Ignore the OOO auto-reply chain. The real issue: network printer "
            "PRN-4F-01 is offline with a 'Network Error' — check the switch port.",
        ],
        remediation_steps=[
            [
                "Check the switch port status for the printer's Ethernet connection",
                "Try a different wall jack or patch cable to isolate the issue",
                "Restart the printer's network interface from its control panel",
                "If the switch port is dead, have networking patch the printer to a working port",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# dc-163  Base64-encoded Excel binary data inlined
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="dc-163",
        category=Category.DATA,
        priority=Priority.P2,
        assigned_team=Team.DATA_PLATFORM,
        needs_escalation=False,
        missing_information=[MissingInfo.TIMESTAMP],
        subjects=[
            "Excel file corrupted — can't open Q1 financials",
            "Corrupted .xlsx on shared drive — base64 below",
            "Financial model file won't open — data recovery needed",
        ],
        descriptions=[
            "The Q1 financial model (\\\\fs01\\Finance\\Models\\Q1-2026.xlsx) is "
            "corrupted. Excel says 'The file is corrupt and cannot be opened.' "
            "Here's the base64:\n\n"
            + "UEsDBBQAAAAIAAAAAAAAAAAAAAAA"
            * 50
            + "\n\nThis file has 47 sheets. Board meeting Thursday. Last good "
            "backup: March 10.\n\n{name}, {department}",
        ],
        next_best_actions=[
            "Restore the corrupted Excel file from backup — ignore the base64 "
            "dump in the ticket body and recover from the March 10 backup.",
        ],
        remediation_steps=[
            [
                "Restore Q1-2026.xlsx from the March 10 backup",
                "Verify the restored file opens correctly and contains all 47 sheets",
                "Investigate the root cause of the corruption (disk errors, network file locks)",
                "Set up more frequent automated backups for critical financial models",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# dc-164  Terraform/Bicep IaC template pasted as description
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="dc-164",
        category=Category.SOFTWARE,
        priority=Priority.P2,
        assigned_team=Team.ENTERPRISE_APPS,
        needs_escalation=False,
        missing_information=[MissingInfo.ENVIRONMENT_DETAILS],
        subjects=[
            "Azure VM provisioning failing — Terraform error",
            "Terraform apply fails for prod-east VMs",
            "Cloud VM allocation error — IaC config attached",
        ],
        descriptions=[
            "Terraform apply is failing:\n\n"
            "```hcl\n"
            'resource "azurerm_linux_virtual_machine" "app_server" {\n'
            "  count    = 3\n"
            '  name     = "vm-app-${count.index + 1}"\n'
            '  size     = "Standard_D4s_v5"\n'
            '  location = "eastus"\n'
            "}\n```\n\n"
            "Error: OverconstrainedAllocationRequest — Standard_D4s_v5 "
            "not available in eastus for our subscription.\n\n"
            "Need these VMs for the trading platform going live next week.\n\n"
            "{name}, {department}",
        ],
        next_best_actions=[
            "The VM SKU Standard_D4s_v5 is unavailable in eastus. Switch to an "
            "alternate SKU or region for the production deployment.",
        ],
        remediation_steps=[
            [
                "Check Azure VM SKU availability in eastus using az vm list-skus",
                "Switch to an available equivalent SKU (e.g., Standard_D4s_v4 or Standard_D4as_v5)",
                "Alternatively, deploy to an alternate region (eastus2) if the SKU is available there",
                "Update the Terraform configuration and re-run terraform apply",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# dc-165  Git blame output pasted as ticket description
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="dc-165",
        category=Category.SOFTWARE,
        priority=Priority.P1,
        assigned_team=Team.ENTERPRISE_APPS,
        needs_escalation=True,
        missing_information=[MissingInfo.AFFECTED_USERS],
        subjects=[
            "Wrong P&L calculation in trading dashboard",
            "Git blame shows bug in pnl.py — P&L values wrong",
            "Trading dashboard showing incorrect profit/loss numbers",
        ],
        descriptions=[
            "The P&L calculation is wrong since yesterday. Git blame:\n\n"
            "$ git blame src/calculations/pnl.py\n"
            "a1b2c3d4 (Alice Chen  2026-03-10 14:22 +0000  1) import decimal\n"
            "e5f6a7b8 (Bob Kim     2026-03-17 09:15 +0000 14) # BUG: divides instead of multiplies\n"
            "e5f6a7b8 (Bob Kim     2026-03-17 09:15 +0000 15) pnl = (price - cost_basis) / quantity\n\n"
            "Line 15 divides instead of multiplying. Commit e5f6a7b8 from "
            "March 17. P&L figures shown to traders are completely wrong.\n\n"
            "{name}, {department}",
        ],
        next_best_actions=[
            "Critical bug in P&L calculation — line 15 divides by quantity "
            "instead of multiplying. Fix and redeploy immediately.",
        ],
        remediation_steps=[
            [
                "Fix the P&L calculation bug on line 15 (change / to *)",
                "Write a unit test to prevent regression",
                "Deploy the hotfix to production immediately",
                "Recalculate and correct any P&L figures shown to traders since March 17",
                "Notify affected traders and compliance about the incorrect figures",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# dc-166  Massive pasted document text
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="dc-166",
        category=Category.SOFTWARE,
        priority=Priority.P3,
        assigned_team=Team.ENTERPRISE_APPS,
        needs_escalation=False,
        missing_information=[MissingInfo.ERROR_MESSAGE, MissingInfo.STEPS_TO_REPRODUCE],
        subjects=[
            "Cannot access Compliance Policy Library on SharePoint",
            "SharePoint library returning 403 after migration",
            "Compliance docs inaccessible since Friday migration",
        ],
        descriptions=[
            "Hi, I need help accessing the Compliance Policy Library on "
            "SharePoint. Here is the document I was trying to open when "
            "the error occurred:\n\n"
            "SECTION 1: DATA RETENTION POLICY\n"
            "1.1 All financial records must be retained for a minimum of "
            "seven (7) years from the date of creation. This includes but "
            "is not limited to general ledger entries, accounts payable "
            "and receivable records, bank statements, tax filings, and "
            "all supporting documentation.\n"
            "1.2 Electronic communications including emails instant messages "
            "and chat logs must be archived in compliance with SEC Rule "
            "17a-4 and FINRA Rule 4511. Retention period shall be no less "
            "than six (6) years from creation date.\n"
            "1.3 Trading records and order execution logs shall be maintained "
            "for the lifetime of the account plus seven (7) years. This "
            "encompasses order tickets, confirmations, allocation records, "
            "and all related correspondence.\n"
            "1.4 Client onboarding documentation including KYC and AML "
            "verification records must be retained for a minimum of five "
            "(5) years after the termination of the business relationship.\n"
            "1.5 Board meeting minutes and corporate governance documents "
            "shall be retained permanently in both electronic and physical "
            "formats.\n\n"
            "The actual problem is I get a 403 Forbidden error when I click "
            "the Compliance Policy Library link.\n\n"
            "SECTION 2: DATA CLASSIFICATION\n"
            "2.1 All data assets shall be classified into one of four "
            "categories: Public, Internal, Confidential, and Restricted.\n"
            "2.2 Classification shall be performed by the data owner at "
            "the time of creation and reviewed annually.\n"
            "2.3 Restricted data includes personally identifiable information "
            "(PII), protected health information (PHI), payment card data "
            "(PCI), and material non-public information (MNPI).\n\n"
            "Please help. {name}, {department}",
            "I was trying to access the Compliance Policy Library and got "
            "an error. Below is the policy I needed:\n\n"
            "SECTION 1: DATA RETENTION POLICY\n"
            "1.1 All financial records must be retained for a minimum of "
            "seven (7) years from the date of creation including general "
            "ledger entries accounts payable and receivable records bank "
            "statements tax filings and all supporting documentation.\n"
            "1.2 Electronic communications including emails instant messages "
            "and chat logs must be archived per SEC Rule 17a-4 and FINRA "
            "Rule 4511 for no less than six (6) years.\n"
            "1.3 Trading records and order execution logs shall be maintained "
            "for the lifetime of the account plus seven (7) years including "
            "order tickets confirmations allocation records.\n"
            "1.4 Client onboarding documentation including KYC and AML "
            "verification records retained for five (5) years after "
            "termination of the business relationship.\n"
            "1.5 Board meeting minutes and corporate governance documents "
            "retained permanently.\n"
            "[continues for many sections]\n\n"
            "The actual problem is I get a 403 Forbidden error when I click "
            "the Compliance Policy Library link on SharePoint since the "
            "Friday migration.\n\n"
            "SECTION 3: ACCESS CONTROL\n"
            "3.1 Access to classified data shall be granted on a need-to-know "
            "basis following the principle of least privilege.\n"
            "3.2 All access requests must be approved by the data owner "
            "and documented in the access management system.\n\n"
            "Thanks, {name}",
        ],
        next_best_actions=[
            "Investigate the 403 Forbidden error on the SharePoint Compliance "
            "Policy Library after the Friday migration. Ignore the pasted "
            "document content — the user simply included the policy text they "
            "were trying to reach.",
            "The actual issue is a 403 error accessing a SharePoint library "
            "post-migration. The extensive policy text is irrelevant noise. "
            "Focus on SharePoint permissions troubleshooting.",
        ],
        remediation_steps=[
            [
                "Check SharePoint site permissions for the Compliance Policy Library",
                "Verify the user's group membership was preserved during migration",
                "Re-grant access to the library if permissions were lost in migration",
                "Test access with the user and confirm the 403 error is resolved",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# dc-167  Embedded SVG image data
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="dc-167",
        category=Category.HARDWARE,
        priority=Priority.P3,
        assigned_team=Team.ENDPOINT,
        needs_escalation=False,
        missing_information=[MissingInfo.DEVICE_INFO, MissingInfo.APPLICATION_VERSION],
        subjects=[
            "Monitor color profile wrong after driver update",
            "Display colors shifted blue after NVIDIA update",
            "Color calibration off since GPU driver update",
        ],
        descriptions=[
            "My monitor colors are completely off since the NVIDIA driver "
            "update. The display is shifted blue and reds look washed out. "
            "Here is the color gradient I see on screen as SVG:\n\n"
            '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1920 1080">'
            "<defs>"
            '<linearGradient id="grad1" x1="0%" y1="0%" x2="100%" y2="0%">'
            '<stop offset="0%" style="stop-color:rgb(255,0,0);stop-opacity:1"/>'
            '<stop offset="25%" style="stop-color:rgb(255,165,0);stop-opacity:1"/>'
            '<stop offset="50%" style="stop-color:rgb(255,255,0);stop-opacity:1"/>'
            '<stop offset="75%" style="stop-color:rgb(0,128,0);stop-opacity:1"/>'
            '<stop offset="100%" style="stop-color:rgb(0,0,255);stop-opacity:1"/>'
            "</linearGradient>"
            '<linearGradient id="grad2" x1="0%" y1="0%" x2="0%" y2="100%">'
            '<stop offset="0%" style="stop-color:rgb(255,255,255);stop-opacity:1"/>'
            '<stop offset="100%" style="stop-color:rgb(0,0,0);stop-opacity:1"/>'
            "</linearGradient>"
            "</defs>"
            '<rect width="1920" height="540" fill="url(#grad1)"/>'
            '<rect y="540" width="1920" height="540" fill="url(#grad2)"/>'
            '<text x="960" y="300" text-anchor="middle" font-size="48" '
            'fill="white">Expected: smooth gradient</text>'
            '<text x="960" y="800" text-anchor="middle" font-size="48" '
            'fill="white">Actual: banding visible</text>'
            "</svg>\n\n"
            "The actual issue: NVIDIA driver v550.67 broke the color profile "
            "on my Dell U2722D monitor. The ICC profile is no longer being "
            "applied. {name}, {department}",
            "After updating my GPU driver to NVIDIA v550.67, my Dell monitor "
            "colors are wrong. I tried to capture what I see as SVG data:\n\n"
            '<svg xmlns="http://www.w3.org/2000/svg" width="800" height="600">'
            '<rect x="0" y="0" width="200" height="200" fill="#FF0000" '
            'opacity="0.7"/>'
            '<rect x="200" y="0" width="200" height="200" fill="#00FF00" '
            'opacity="0.7"/>'
            '<rect x="400" y="0" width="200" height="200" fill="#0000FF" '
            'opacity="0.7"/>'
            '<rect x="0" y="200" width="200" height="200" fill="#FF6600" '
            'opacity="0.7"/>'
            '<rect x="200" y="200" width="200" height="200" fill="#9900CC" '
            'opacity="0.7"/>'
            '<rect x="400" y="200" width="200" height="200" fill="#00CCFF" '
            'opacity="0.7"/>'
            '<text x="400" y="450" text-anchor="middle" font-size="24">'
            "These colors are wrong on my screen</text>"
            "</svg>\n\n"
            "The ICC color profile stopped applying after the NVIDIA v550.67 "
            "driver update. My Dell U2722D looks blue-shifted and washed out. "
            "{name}",
        ],
        next_best_actions=[
            "Reapply the Dell U2722D ICC color profile or rollback the NVIDIA "
            "driver from v550.67 to the previous version. Ignore the embedded "
            "SVG data — it is not actionable.",
            "Investigate NVIDIA driver v550.67 breaking ICC profile application "
            "on the Dell monitor. The SVG content is irrelevant diagnostic noise.",
        ],
        remediation_steps=[
            [
                "Reapply the ICC color profile for the Dell U2722D via Display Settings",
                "If profile does not stick, rollback NVIDIA driver from v550.67 to previous version",
                "Check NVIDIA Control Panel color settings for overrides",
                "Test with a different display cable (DP vs HDMI) to rule out signal issues",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# dc-168  Hex dump of network capture
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="dc-168",
        category=Category.NETWORK,
        priority=Priority.P2,
        assigned_team=Team.NETWORK,
        needs_escalation=False,
        missing_information=[MissingInfo.NETWORK_LOCATION, MissingInfo.AFFECTED_USERS],
        subjects=[
            "Intermittent packet loss on trading floor — capture included",
            "5-8% packet loss daily on VLAN 210",
            "Network drops during market open — hex dump attached",
        ],
        descriptions=[
            "We are seeing 5-8% packet loss daily on the trading floor "
            "between 14:00 and 14:15 UTC. Here is a hex dump from my "
            "packet capture:\n\n"
            "0000  00 1a 2b 3c 4d 5e 00 0c 29 8a 1b 2c 08 00 45 00  "
            "..+<M^..)..,.E.\n"
            "0010  00 3c 1c 46 40 00 40 06 b1 e6 c0 a8 01 64 ac 10  "
            ".<.F@.@......d..\n"
            "0020  01 0a 00 50 c3 58 a1 b2 c3 d4 00 00 00 00 a0 02  "
            "...P.X..........\n"
            "0030  ff ff 3e 2c 00 00 02 04 05 b4 04 02 08 0a 00 a3  "
            "..>,...........\n"
            "0040  2f 48 00 00 00 00 01 03 03 07 00 00 00 00 00 00  "
            "/H..............\n"
            "0050  00 1a 2b 3c 4d 5e 00 0c 29 8a 1b 2c 08 00 45 00  "
            "..+<M^..)..,.E.\n"
            "0060  00 3c 1c 47 40 00 40 06 b1 e5 c0 a8 01 64 ac 10  "
            ".<.G@.@......d..\n"
            "0070  01 0a 00 50 c3 59 a1 b2 c3 d5 00 00 00 00 a0 02  "
            "...P.Y..........\n"
            "0080  ff ff 3e 2b 00 00 02 04 05 b4 04 02 08 0a 00 a3  "
            "..>+...........\n"
            "0090  2f 49 00 00 00 00 01 03 03 07 00 00 00 00 00 00  "
            "/I..............\n\n"
            "The real issue is daily packet loss from 14:00 to 14:15 UTC "
            "on VLAN 210 affecting FIX connections to the exchange. This "
            "is causing order rejections. {name}, {department}",
            "Packet loss on VLAN 210 is killing our FIX connections every "
            "day at market open. Here is the capture data:\n\n"
            "0000  00 0c 29 8a 1b 2c 00 1a 2b 3c 4d 5e 08 00 45 00  "
            "..)..,.+<M^..E.\n"
            "0010  00 28 3f a2 40 00 80 06 6d 9e ac 10 01 0a c0 a8  "
            ".(?. @..m.......\n"
            "0020  01 64 c3 58 00 50 00 00 00 00 a1 b2 c3 d5 50 12  "
            ".d.X.P........P.\n"
            "0030  ff ff a6 c2 00 00 00 00 00 00 00 00 00 00 00 00  "
            "................\n"
            "0040  00 0c 29 8a 1b 2c 00 1a 2b 3c 4d 5e 08 00 45 00  "
            "..)..,.+<M^..E.\n"
            "0050  01 f4 3f a3 40 00 80 06 6b d1 ac 10 01 0a c0 a8  "
            "..?.@...k.......\n"
            "0060  01 64 c3 58 00 50 00 00 00 01 a1 b2 c3 d5 50 18  "
            ".d.X.P........P.\n"
            "0070  ff ff 8b c7 00 00 38 3d 46 49 58 54 2e 31 2e 31  "
            "......8=FIXT.1.1\n\n"
            "We see 5-8% packet loss daily 14:00-14:15 UTC on VLAN 210. "
            "FIX connections drop and orders get rejected. {name}",
        ],
        next_best_actions=[
            "Investigate the scheduled congestion on VLAN 210 causing daily "
            "packet loss between 14:00 and 14:15 UTC. The hex dump is raw "
            "capture data and not directly useful for triage.",
            "Focus on identifying what process or traffic spike occurs at "
            "14:00 UTC on VLAN 210 that causes 5-8% packet loss affecting "
            "FIX trading connections.",
        ],
        remediation_steps=[
            [
                "Review switch port logs and traffic counters on VLAN 210 during 14:00-14:15 UTC window",
                "Check for scheduled jobs or batch processes that coincide with the packet loss window",
                "Analyze QoS policies to ensure FIX protocol traffic has appropriate priority",
                "Verify uplink capacity from the trading floor access switches to the core",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# dc-169  Windows Event Log XML dump
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="dc-169",
        category=Category.HARDWARE,
        priority=Priority.P2,
        assigned_team=Team.ENDPOINT,
        needs_escalation=False,
        missing_information=[MissingInfo.DEVICE_INFO, MissingInfo.REPRODUCTION_FREQUENCY],
        subjects=[
            "Blue screen twice today — Event Viewer export",
            "BSOD DRIVER_IRQL_NOT_LESS_OR_EQUAL — event log attached",
            "Laptop crashes when docking — XML export below",
        ],
        descriptions=[
            "My laptop blue-screened twice today when I plugged into my "
            "docking station. Here is the Event Viewer export:\n\n"
            '<Event xmlns="http://schemas.microsoft.com/win/2004/08/events/event">'
            "<System>"
            '<Provider Name="Microsoft-Windows-WER-SystemErrorReporting" '
            'Guid="{ABCE23E7-DE45-4366-8631-84FA6C525952}"/>'
            '<EventID Qualifiers="0">1001</EventID>'
            "<Version>0</Version>"
            "<Level>2</Level>"
            "<Task>0</Task>"
            "<Opcode>0</Opcode>"
            "<Keywords>0x80000000000000</Keywords>"
            '<TimeCreated SystemTime="2026-03-18T09:42:17.000000000Z"/>'
            "<EventRecordID>45231</EventRecordID>"
            '<Execution ProcessID="0" ThreadID="0"/>'
            "<Channel>System</Channel>"
            "<Computer>WKST-{name}.contoso.com</Computer>"
            "</System>"
            "<EventData>"
            "<Data>0x000000d1 (DRIVER_IRQL_NOT_LESS_OR_EQUAL)</Data>"
            "<Data>0x0000000000000028</Data>"
            "<Data>0x0000000000000002</Data>"
            "<Data>0x0000000000000000</Data>"
            "<Data>fffff8024a3b1234</Data>"
            "<Data>usbhub3.sys</Data>"
            "<Data>10.0.19041.3636</Data>"
            "</EventData>"
            "</Event>\n\n"
            "The BSOD happens when I connect my USB-C docking station. "
            "The bugcheck is DRIVER_IRQL_NOT_LESS_OR_EQUAL and it points "
            "to usbhub3.sys. {name}, {department}",
            "Getting blue screens when I dock my laptop. Exported the "
            "event log:\n\n"
            '<Event xmlns="http://schemas.microsoft.com/win/2004/08/events/event">'
            "<System>"
            '<Provider Name="Microsoft-Windows-Kernel-Power" '
            'Guid="{331C3B3A-2005-44C2-AC5E-77220C37D6B4}"/>'
            "<EventID>41</EventID>"
            "<Version>6</Version>"
            "<Level>1</Level>"
            "<Task>63</Task>"
            "<Opcode>0</Opcode>"
            "<Keywords>0x8000400000000002</Keywords>"
            '<TimeCreated SystemTime="2026-03-18T09:42:15.000000000Z"/>'
            "<EventRecordID>45230</EventRecordID>"
            "<Channel>System</Channel>"
            "<Computer>WKST-{name}.contoso.com</Computer>"
            "</System>"
            "<EventData>"
            "<Data Name='BugcheckCode'>209</Data>"
            "<Data Name='BugcheckParameter1'>0x28</Data>"
            "<Data Name='BugcheckParameter2'>0x2</Data>"
            "<Data Name='SleepInProgress'>0</Data>"
            "<Data Name='PowerButtonTimestamp'>0</Data>"
            "</EventData>"
            "</Event>\n\n"
            "The crash is triggered specifically when plugging in the "
            "USB-C dock. BSOD DRIVER_IRQL_NOT_LESS_OR_EQUAL pointing to "
            "usbhub3.sys. Happened twice today. {name}",
        ],
        next_best_actions=[
            "Investigate the dock-triggered BSOD. The bugcheck points to "
            "usbhub3.sys — check the minidump for the exact faulting driver "
            "and update or rollback accordingly.",
            "The XML event logs confirm DRIVER_IRQL_NOT_LESS_OR_EQUAL caused "
            "by usbhub3.sys during USB-C dock connection. Analyze minidump "
            "for root cause driver.",
        ],
        remediation_steps=[
            [
                "Collect and analyze the minidump files from C:\\Windows\\Minidump",
                "Update the USB-C docking station firmware to the latest version",
                "Rollback the faulting driver (usbhub3.sys) if a recent update caused the regression",
                "Test with a different docking station to isolate hardware vs driver issue",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# dc-170  Concatenated SCOM monitoring alerts
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="dc-170",
        category=Category.DATA,
        priority=Priority.P1,
        assigned_team=Team.DATA_PLATFORM,
        needs_escalation=True,
        missing_information=[MissingInfo.BUSINESS_IMPACT, MissingInfo.AFFECTED_SYSTEM],
        subjects=[
            "FW: FW: CRITICAL — disk space alerts from SCOM",
            "SQLPROD01 disk space critical — {floor} alert emails forwarded",
            "Production SQL Server running out of disk — alert flood",
        ],
        descriptions=[
            "Forwarding these alerts from SCOM — please look at this ASAP!\n\n"
            "--- Alert: Disk Free Space Low ---\n"
            "Source: SQLPROD01.contoso.com\n"
            "Severity: Critical\n"
            "Generated: 2026-03-18 06:00:12 UTC\n"
            "Disk C: 2.1 GB free (4.2%)\n"
            "Threshold: 5%\n"
            "--- End Alert ---\n\n"
            "--- Alert: Disk Free Space Low ---\n"
            "Source: SQLPROD01.contoso.com\n"
            "Severity: Critical\n"
            "Generated: 2026-03-18 06:15:14 UTC\n"
            "Disk C: 1.8 GB free (3.6%)\n"
            "Threshold: 5%\n"
            "--- End Alert ---\n\n"
            "--- Alert: Disk Free Space Low ---\n"
            "Source: SQLPROD01.contoso.com\n"
            "Severity: Critical\n"
            "Generated: 2026-03-18 06:30:11 UTC\n"
            "Disk C: 1.5 GB free (3.0%)\n"
            "Threshold: 5%\n"
            "--- End Alert ---\n\n"
            "--- Alert: Disk Free Space Low ---\n"
            "Source: SQLPROD01.contoso.com\n"
            "Severity: Critical\n"
            "Generated: 2026-03-18 06:45:09 UTC\n"
            "Disk C: 1.2 GB free (2.4%)\n"
            "Threshold: 5%\n"
            "--- End Alert ---\n\n"
            "The production SQL Server C: drive is running out of disk "
            "space. It keeps dropping. {name}, {department}",
            "Getting a flood of SCOM alerts for SQLPROD01:\n\n"
            "--- Alert: Disk Free Space Low ---\n"
            "Source: SQLPROD01.contoso.com\n"
            "Severity: Critical\n"
            "Generated: 2026-03-18 07:00:08 UTC\n"
            "Disk C: 0.9 GB free (1.8%)\n"
            "Threshold: 5%\n"
            "--- End Alert ---\n\n"
            "--- Alert: Disk Free Space Low ---\n"
            "Source: SQLPROD01.contoso.com\n"
            "Severity: Critical\n"
            "Generated: 2026-03-18 07:15:06 UTC\n"
            "Disk C: 0.7 GB free (1.4%)\n"
            "Threshold: 5%\n"
            "--- End Alert ---\n\n"
            "--- Alert: Disk Free Space Low ---\n"
            "Source: SQLPROD01.contoso.com\n"
            "Severity: Warning\n"
            "Generated: 2026-03-18 07:15:07 UTC\n"
            "Disk D: 12.3 GB free (8.2%)\n"
            "Threshold: 10%\n"
            "--- End Alert ---\n\n"
            "SQLPROD01 C: drive is critically low and still dropping. "
            "This is a production database server. {name}",
        ],
        next_best_actions=[
            "Immediately address the disk space crisis on SQLPROD01. The "
            "C: drive is under 5% free and actively declining. This is a "
            "production SQL Server requiring urgent intervention.",
            "The SCOM alerts are redundant but the underlying issue is "
            "critical: SQLPROD01 C: drive is nearly full. Take immediate "
            "action to free space before the database crashes.",
        ],
        remediation_steps=[
            [
                "Free disk space on SQLPROD01 C: drive immediately — clear temp files, old backups, and log files",
                "Check if tempdb is on C: and move it to the data volume if so",
                "Move any user databases from C: to the dedicated data volume",
                "Add additional disk capacity and set up proactive monitoring thresholds",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# dc-171  Multi-encoding mojibake chain
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="dc-171",
        category=Category.HARDWARE,
        priority=Priority.P3,
        assigned_team=Team.ENDPOINT,
        needs_escalation=False,
        missing_information=[MissingInfo.DEVICE_INFO, MissingInfo.APPLICATION_VERSION],
        subjects=[
            "Printer driver error — garbled characters in error",
            "Cannot install printer driver — mojibake in error message",
            "Driver installation fails with encoding-garbled error",
        ],
        descriptions=[
            "I cannot install the printer driver and the error messages "
            "are garbled. Here is what I see:\n\n"
            "Error: \u00e2\u0080\u0098Druckertreiber konnte nicht installiert "
            "werden\u00e2\u0080\u0099\n"
            "Details: \u00c3\u00a2\u00e2\u201a\u00ac\u0178Cannot locate INF "
            "file for printer model KonicaMinolta C308"
            "\u00c3\u00a2\u00e2\u201a\u00ac\u0153\n"
            "Status: \u00c3\u0083\u00c2\u00a2\u00c3\u00a2\u00e2\u0080\u009a"
            "\u00c2\u00ac\u00c3\u0085\u00e2\u0080\u009cFailed with error "
            "0x800F0214\u00c3\u0083\u00c2\u00a2\u00c3\u00a2\u00e2\u0080\u009a"
            "\u00c2\u00ac\u00c3\u0082\u00c2\u009d\n\n"
            "The actual problem: I am trying to install the Konica Minolta "
            "C308 printer driver on {os} and it fails with error 0x800F0214. "
            "The error dialog shows encoding-garbled text. {name}, {department}",
            "Printer driver installation keeps failing. The error window "
            "shows mojibake:\n\n"
            "\u00c3\u00a2\u00e2\u201a\u00ac\u0178Installation des "
            "Druckertreibers fehlgeschlagen\u00c3\u00a2\u00e2\u201a\u00ac"
            "\u0153\n"
            "Error code: 0x800F0214\n"
            "Message: \u00e2\u0080\u009cThe third-party INF does not contain "
            "digital signature information\u00e2\u0080\u009d\n"
            "Additional: \u00c3\u0083\u00c2\u00a2\u00c3\u00a2\u00e2\u0080"
            "\u009a\u00c2\u00ac\u00c3\u0085\u00e2\u0080\u009cKonica Minolta "
            "Universal Print Driver\u00c3\u0083\u00c2\u00a2\u00c3\u00a2"
            "\u00e2\u0080\u009a\u00c2\u00ac\u00c3\u0082\u00c2\u009d\n\n"
            "The Konica Minolta C308 driver fails with 0x800F0214 on {os}. "
            "I think it is a driver signing issue. {name}",
        ],
        next_best_actions=[
            "Troubleshoot driver installation error 0x800F0214 for the "
            "Konica Minolta C308. The mojibake text is a display artifact "
            "from encoding issues and does not affect troubleshooting.",
            "The error 0x800F0214 indicates the printer driver INF is not "
            "digitally signed. Download the correct signed driver package "
            "for the Konica Minolta C308.",
        ],
        remediation_steps=[
            [
                "Download the correct signed driver package for the Konica Minolta C308 from the manufacturer",
                "Check that driver signing enforcement is not blocking a valid driver",
                "Use the Add Printer wizard instead of the standalone installer",
                "If needed, temporarily disable driver signature enforcement to install and then re-enable",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# dc-172  Cascading auto-reply loop
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="dc-172",
        category=Category.SOFTWARE,
        priority=Priority.P2,
        assigned_team=Team.ENTERPRISE_APPS,
        needs_escalation=False,
        missing_information=[MissingInfo.ERROR_MESSAGE, MissingInfo.AFFECTED_USERS],
        subjects=[
            "RE: RE: RE: Automatic reply: RE: Automatic reply: Room booking down",
            "Auto-reply loop burying real issue — booking system offline",
            "OOO reply chain with buried booking system outage",
        ],
        descriptions=[
            "Subject: RE: RE: RE: Automatic reply: RE: Automatic reply: "
            "Room booking system not working\n\n"
            "--- Automatic Reply ---\n"
            "Thank you for your email. I am out of the office until March "
            "25th with limited access to email. For urgent matters please "
            "contact Jane Smith.\n"
            "--- End Automatic Reply ---\n\n"
            "--- Automatic Reply ---\n"
            "Hi, I am currently out of the office attending a conference. "
            "I will respond to your email upon my return on March 24th. "
            "For immediate assistance please contact the help desk.\n"
            "--- End Automatic Reply ---\n\n"
            "--- Automatic Reply ---\n"
            "Thank you for your email. I am out of the office until March "
            "25th with limited access to email. For urgent matters please "
            "contact Jane Smith.\n"
            "--- End Automatic Reply ---\n\n"
            "--- Automatic Reply ---\n"
            "Hi, I am currently out of the office attending a conference. "
            "I will respond to your email upon my return on March 24th.\n"
            "--- End Automatic Reply ---\n\n"
            "--- Original Message ---\n"
            "The meeting room booking system (RoomBook Pro) has been down "
            "since 8 AM this morning. Nobody on {floor} floor can book "
            "rooms. {name}, {department}",
            "This email chain is a mess of auto-replies but the real issue "
            "is buried at the bottom:\n\n"
            "RE: RE: Automatic reply: RE: Automatic reply: RE: Booking "
            "system offline\n\n"
            "--- OOO ---\n"
            "I am on PTO until 3/26. Contact helpdesk for urgent issues.\n"
            "--- OOO ---\n\n"
            "--- OOO ---\n"
            "Thanks for your message. I am at an offsite event this week "
            "and will have limited email access. Back March 25.\n"
            "--- OOO ---\n\n"
            "--- OOO ---\n"
            "I am on PTO until 3/26. Contact helpdesk for urgent issues.\n"
            "--- OOO ---\n\n"
            "--- OOO ---\n"
            "Thanks for your message. I am at an offsite event this week.\n"
            "--- OOO ---\n\n"
            "--- Original ---\n"
            "RoomBook Pro is completely down since this morning. Nobody "
            "can book meeting rooms. Please fix ASAP. {name}",
        ],
        next_best_actions=[
            "Investigate the RoomBook Pro outage reported in the original "
            "message buried under the auto-reply chain. Ignore all the "
            "out-of-office replies.",
            "The cascading auto-replies are noise. The actual issue: "
            "RoomBook Pro meeting room booking system has been down since "
            "morning affecting the entire floor.",
        ],
        remediation_steps=[
            [
                "Check the RoomBook Pro application server status and logs",
                "Verify the Exchange integration for room mailboxes is functioning",
                "Restart the RoomBook Pro service and verify rooms are bookable",
                "Communicate status to affected users and break the auto-reply loop by disabling the looping rules",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# dc-173  Tab-separated query result dump
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="dc-173",
        category=Category.DATA,
        priority=Priority.P2,
        assigned_team=Team.DATA_PLATFORM,
        needs_escalation=False,
        missing_information=[MissingInfo.ENVIRONMENT_DETAILS, MissingInfo.TIMESTAMP],
        subjects=[
            "Database query taking 45 minutes — result set included",
            "SELECT on trades table degraded from 10s to 45min",
            "Possible missing index on SQLPROD03 trades table",
        ],
        descriptions=[
            "A query on the trades table that used to take 10 seconds now "
            "takes 45 minutes. I think an index was dropped during last "
            "weekend's maintenance. Here is a sample of the result set:\n\n"
            "TradeID\tSymbol\tSide\tQuantity\tPrice\tTimestamp\tStatus\n"
            "T-20260318-001\tAAPL\tBUY\t500\t178.42\t2026-03-18 09:30:01\tFILLED\n"
            "T-20260318-002\tMSFT\tSELL\t200\t412.87\t2026-03-18 09:30:02\tFILLED\n"
            "T-20260318-003\tGOOG\tBUY\t100\t155.23\t2026-03-18 09:30:03\tFILLED\n"
            "T-20260318-004\tAMZN\tBUY\t300\t185.64\t2026-03-18 09:30:05\tFILLED\n"
            "T-20260318-005\tTSLA\tSELL\t150\t172.91\t2026-03-18 09:30:06\tFILLED\n"
            "T-20260318-006\tNVDA\tBUY\t400\t892.15\t2026-03-18 09:30:08\tFILLED\n"
            "T-20260318-007\tJPM\tSELL\t250\t198.33\t2026-03-18 09:30:10\tFILLED\n"
            "T-20260318-008\tBAC\tBUY\t600\t37.82\t2026-03-18 09:30:11\tFILLED\n"
            "T-20260318-009\tV\tSELL\t175\t278.45\t2026-03-18 09:30:13\tFILLED\n"
            "T-20260318-010\tWMT\tBUY\t350\t168.29\t2026-03-18 09:30:15\tFILLED\n"
            "[... 2.4 million more rows ...]\n\n"
            "The query is SELECT * FROM trades WHERE trade_date = '2026-03-18' "
            "and it used to return in 10 seconds. Now it does a full table "
            "scan. {name}, {department}",
            "Query performance on SQLPROD03 has tanked. Here is the output "
            "I am seeing:\n\n"
            "TradeID\tSymbol\tSide\tQty\tPrice\tTime\tAccount\tVenue\n"
            "T-20260317-991\tMETA\tBUY\t200\t502.11\t09:31:22\tACCT-4421\tNYSE\n"
            "T-20260317-992\tDIS\tSELL\t150\t112.43\t09:31:24\tACCT-7832\tNASDAQ\n"
            "T-20260317-993\tNFLX\tBUY\t100\t623.87\t09:31:25\tACCT-1156\tARCA\n"
            "T-20260317-994\tCRM\tSELL\t300\t298.54\t09:31:27\tACCT-3309\tNYSE\n"
            "T-20260317-995\tADBE\tBUY\t175\t545.21\t09:31:29\tACCT-8844\tNASDAQ\n"
            "T-20260317-996\tPYPL\tSELL\t225\t67.89\t09:31:30\tACCT-2210\tARCA\n"
            "T-20260317-997\tINTC\tBUY\t500\t43.67\t09:31:32\tACCT-5567\tNYSE\n"
            "T-20260317-998\tAMD\tSELL\t400\t178.92\t09:31:33\tACCT-9901\tNASDAQ\n"
            "T-20260317-999\tORCL\tBUY\t350\t124.56\t09:31:35\tACCT-6643\tNYSE\n"
            "[... millions more rows ...]\n\n"
            "SELECT on trades table went from 10 seconds to 45 minutes. "
            "Likely a missing index after weekend maintenance. {name}",
        ],
        next_best_actions=[
            "Investigate the suspected index drop on the trades table in "
            "SQLPROD03. The pasted result set data is irrelevant — the issue "
            "is a query performance regression from 10s to 45min.",
            "Check the index definitions on the trades table. A weekend "
            "maintenance job likely dropped an index on trade_date, causing "
            "full table scans instead of index seeks.",
        ],
        remediation_steps=[
            [
                "Check the current index definitions on the trades table and compare with expected indexes",
                "Recreate the missing index on trade_date (and any other dropped indexes)",
                "Review the maintenance scripts to prevent accidental index drops in the future",
                "Monitor query execution plans to confirm the index is being used after recreation",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# dc-174  Raw email headers flood
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="dc-174",
        category=Category.SOFTWARE,
        priority=Priority.P3,
        assigned_team=Team.ENTERPRISE_APPS,
        needs_escalation=False,
        missing_information=[MissingInfo.APPLICATION_VERSION, MissingInfo.DEVICE_INFO],
        subjects=[
            "Outlook freezes when opening external emails",
            "{app} hangs for 30 seconds on external messages",
            "Outlook delay opening emails from outside org",
        ],
        descriptions=[
            "Outlook freezes for about 30 seconds every time I open an "
            "email from outside the organization. This started after the "
            "March patch. Here are the headers from one of the emails:\n\n"
            "Received: from MX01.contoso.com (10.1.2.30) by\n"
            " EXCH01.contoso.com (10.1.2.10) with Microsoft SMTP Server\n"
            " (version=TLS1_2, cipher=TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384)\n"
            " id 15.1.2507.23; Mon, 18 Mar 2026 08:15:32 -0400\n"
            "Received: from mail-yw1-f169.google.com (209.85.128.169) by\n"
            " MX01.contoso.com (10.1.2.30) with Microsoft SMTP Server id\n"
            " 15.1.2507.23 via Frontend Transport; Mon, 18 Mar 2026\n"
            " 08:15:31 -0400\n"
            "Authentication-Results: contoso.com; spf=pass\n"
            " (sender IP is 209.85.128.169)\n"
            " smtp.mailfrom=externalsender@gmail.com; dkim=pass\n"
            " (signature was verified)\n"
            " header.d=gmail.com;contoso.com; dmarc=pass\n"
            " action=none header.from=gmail.com;\n"
            "X-MS-Exchange-Organization-SCL: 1\n"
            "X-MS-Exchange-Organization-AuthSource: MX01.contoso.com\n"
            "X-MS-Exchange-Organization-AuthAs: Anonymous\n"
            "X-MS-Has-Attach:\n"
            "X-MS-Exchange-Transport-CrossTenantHeadersStamped: EXCH01\n"
            "X-MS-Exchange-Organization-AVStamp-Enterprise: 1.0\n"
            "X-DLP-Scanning-Result: Pending\n"
            "X-DLP-Policy-Applied: External-Email-DLP-v3\n\n"
            "I think the delay might be related to DLP scanning. The "
            "X-DLP-Scanning-Result shows Pending. {name}, {department}",
            "Since the March patch, {app} hangs for 30 seconds whenever "
            "I open external emails. Headers from a slow message:\n\n"
            "Received: from edge01.contoso.com (10.1.2.40) by\n"
            " EXCH02.contoso.com (10.1.2.11) with Microsoft SMTP Server\n"
            " (version=TLS1_2) id 15.1.2507.23; Mon, 18 Mar 2026\n"
            " 08:22:45 -0400\n"
            "Authentication-Results: contoso.com; spf=pass\n"
            " smtp.mailfrom=vendor@partner.com; dkim=pass\n"
            " header.d=partner.com; dmarc=pass\n"
            "X-MS-Exchange-Organization-SCL: 0\n"
            "X-MS-Exchange-Organization-AuthAs: Anonymous\n"
            "X-MS-Exchange-CrossTenant-AuthSource: edge01.contoso.com\n"
            "X-MS-Exchange-Transport-EndToEndLatency: 00:00:28.4521\n"
            "X-DLP-Scanning-Result: Pending\n"
            "X-DLP-Policy-Applied: External-Email-DLP-v3\n"
            "X-DLP-Scan-Duration-Ms: 27842\n\n"
            "The DLP scan is taking almost 28 seconds per message. This "
            "is causing {app} to freeze while it waits. {name}",
        ],
        next_best_actions=[
            "Investigate the Outlook external email delay caused by DLP "
            "policy scanning. The raw headers show DLP scan taking ~28 "
            "seconds per external message after the March patch.",
            "The email headers confirm the delay is caused by the "
            "External-Email-DLP-v3 policy scanning. Check DLP configuration "
            "for a regression introduced in the March patch.",
        ],
        remediation_steps=[
            [
                "Check Outlook performance logging to confirm DLP scanning is the bottleneck",
                "Review the External-Email-DLP-v3 policy configuration for recent changes or regressions",
                "Test Outlook in safe mode to rule out add-in interference",
                "Check if the March patch introduced DLP scanning changes and consider rollback if confirmed",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# dc-175  Very long single paragraph no line breaks
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="dc-175",
        category=Category.NETWORK,
        priority=Priority.P3,
        assigned_team=Team.NETWORK,
        needs_escalation=False,
        missing_information=[MissingInfo.ERROR_MESSAGE, MissingInfo.DEVICE_INFO],
        subjects=[
            "VPN certificate expired cannot connect",
            "GlobalProtect certificate error — remote work blocked",
            "Cannot VPN in — certificate validation failure",
        ],
        descriptions=[
            "Hi IT support I am writing to report an issue with my VPN "
            "connection that has been affecting my ability to work remotely "
            "since yesterday morning when I tried to connect using the "
            "GlobalProtect VPN client on my laptop running {os} and I "
            "received an error that said something about certificate "
            "validation failed or certificate expired I am not exactly sure "
            "of the wording because I was rushing to a meeting but I "
            "remember it mentioned certificates and I tried clicking retry "
            "multiple times and restarting my laptop and even switching "
            "from WiFi to my phone hotspot but I got the same error on all "
            "networks which tells me it is a certificate problem not a "
            "network problem and my colleague {name} says her VPN works "
            "fine so it is just my machine and I need this fixed today "
            "because I am working from home all week and I cannot access "
            "any internal resources without the VPN including SharePoint "
            "and the trading applications and my manager is asking why I "
            "am not responding to messages on Teams which I also cannot "
            "access and I tried looking online for solutions and some "
            "forums said to delete the certificate and reimport it but I "
            "do not have admin rights to do that and another forum said "
            "to check the date and time on my laptop which I did and it "
            "is correct and I also tried uninstalling and reinstalling "
            "GlobalProtect but the same error came back and I am running "
            "out of things to try so please help me as soon as possible "
            "because I have a critical deadline on Wednesday and I cannot "
            "miss it and my department head is going to escalate this if "
            "it is not fixed by end of day today thank you {name} from "
            "{department} on {floor} floor",
            "Hi I need help with my VPN I have been unable to connect to "
            "GlobalProtect since yesterday and I keep getting a certificate "
            "error and I have tried everything I can think of including "
            "restarting my computer and reinstalling the VPN client and "
            "checking my internet connection which works fine for everything "
            "else like browsing the web and streaming video so it is "
            "definitely not a network issue on my end and I asked my "
            "colleague and his VPN works perfectly fine which makes me think "
            "something is wrong with my specific certificate or profile and "
            "I really need this fixed because I am remote all week and "
            "cannot do any work without VPN access and my manager is asking "
            "why deliverables are late and I cannot explain that I have been "
            "locked out of all internal systems since yesterday morning and "
            "I tried calling the help desk but was on hold for 45 minutes "
            "and then got disconnected and I tried the self-service portal "
            "but the certificate renewal page says I need to be on the "
            "corporate network to access it which is a catch-22 because I "
            "need the VPN to get on the corporate network and I need the "
            "corporate network to fix the VPN and I am going in circles "
            "and getting increasingly frustrated because this should be a "
            "simple fix and I have already wasted an entire day on this and "
            "I cannot afford to waste another day so please prioritize this "
            "and get back to me as soon as possible thanks {name} "
            "{department} {office}",
        ],
        next_best_actions=[
            "Renew the expired VPN client certificate on the user's laptop. "
            "The long unformatted message describes a GlobalProtect VPN "
            "certificate validation failure preventing remote access.",
            "The user's GlobalProtect VPN certificate has expired. Since "
            "they cannot reach the corporate network to self-service renew, "
            "push a new certificate remotely or provide an alternative "
            "renewal method.",
        ],
        remediation_steps=[
            [
                "Check the expiration date of the user's VPN client certificate in the GlobalProtect portal",
                "Reissue a new VPN certificate for the user via the certificate authority",
                "Push the certificate to the user's device via MDM or provide a secure download link",
                "Check if this is part of a batch certificate expiration affecting multiple users",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# dc-176  Base64 image flood obscuring real issue
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="dc-176",
        category=Category.HARDWARE,
        priority=Priority.P3,
        assigned_team=Team.ENDPOINT,
        needs_escalation=False,
        missing_information=[MissingInfo.DEVICE_INFO, MissingInfo.ERROR_MESSAGE],
        subjects=[
            "Monitor flickering — screenshots inline",
            "Display flickers through docking station — see images",
            "External monitor issue on {floor} — embedded screenshots",
        ],
        descriptions=[
            "Hi IT,\n\nMy monitor keeps flickering. Screenshots:\n\n"
            "Screenshot 1:\n"
            "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAoAAAAHgCAYAAAA"
            "10dzkAAAABHNCSVU83LnNpZ25hdHVyZSBoZXJlIGlzIGEgdGVzdCBiYXNlNj"
            "QgZW5jb2RlZCBpbWFnZSBkYXRhIHRoYXQgaXMgbm90IGFjdHVhbGx5IGFS"
            "ZWFsIGltYWdlIGJ1dCBzaW11bGF0ZXMgYSBsYXJnZSBwYXN0ZWQgc2NyZW"
            "Vuc2hvdCBpbiBhbiBlbWFpbCBib2R5==\n\n"
            "Screenshot 2:\n"
            "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAgGBg"
            "cGBQgHBwcJCQgKDBQNDAsLDBkSEw8UHRofHh0aHBwgJC4nICIsIxwcKDcp"
            "FAKEBASE64SECONDSCREENSHOTBLOCKWITHENCODEDIMAGEDATA==\n\n"
            "Screenshot 3:\n"
            "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAKCAYAAACN"
            "Ms+9AAAABmJLR0QA/wD/AP+gvaeTFAKEBASE64THIRDBLOCKMORE==\n\n"
            "The monitor is a Dell U2722D via DisplayPort through a Lenovo "
            "ThinkPad USB-C dock. Flickers every 5-10 seconds. {name}",
            "External display flickers on {floor} when connected through "
            "the USB-C dock. I pasted screenshots but they showed up as "
            "base64 data:\n\n"
            "[image data: iVBORw0KGgoAAAANSUhEUgAAAAUA...FAKEBASE64...==]\n"
            "[image data: /9j/4AAQSkZJRg...MOREBASE64DATA...==]\n"
            "[image data: iVBORw0KGgo...YETMOREBASE64...==]\n\n"
            "The dock is Lenovo ThinkPad USB-C Gen 2, monitor is Dell "
            "U2722D. Flickering every 5-10 seconds. Works fine with "
            "direct HDMI. {name}, {department}",
        ],
        next_best_actions=[
            "Investigate monitor flickering through USB-C dock. Ignore "
            "the inline base64 image data — the real issue is a Dell "
            "U2722D flickering every 5-10 seconds via DisplayPort.",
            "Troubleshoot external display flickering through the "
            "Lenovo dock. The base64 content is noise from pasted "
            "screenshots.",
        ],
        remediation_steps=[
            [
                "Update the docking station firmware to the latest version",
                "Test with a different DisplayPort cable or direct HDMI connection",
                "Check display driver version and update from Dell/Lenovo support",
                "If flickering persists, test with a replacement docking station",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# dc-177  Auto-reply/vacation chain burying real issue
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="dc-177",
        category=Category.SOFTWARE,
        priority=Priority.P2,
        assigned_team=Team.ENTERPRISE_APPS,
        needs_escalation=False,
        missing_information=[MissingInfo.AFFECTED_USERS, MissingInfo.ENVIRONMENT_DETAILS],
        subjects=[
            "RE: RE: RE: FW: SAP timeout errors",
            "FW: RE: RE: RE: Application server timeouts — quarter end",
            "RE: FW: RE: {app} connection errors — urgent",
        ],
        descriptions=[
            "--- Auto-Reply ---\n"
            "Thank you for your email. I am currently out of the office "
            "until March 28 with limited email access. For urgent matters "
            "contact James Rivera at ext. 3200.\n"
            "— Patricia Wong\n\n"
            "--- Auto-Reply ---\n"
            "I am attending the Global Finance Summit in {office} from "
            "March 17-24. For immediate help, contact the Finance Help "
            "Desk at ext. 4500.\n"
            "— Michael Strauss\n\n"
            "--- Auto-Reply ---\n"
            "I am on parental leave. For urgent requests contact Sarah "
            "Kim at ext. 3201.\n"
            "— David Park\n\n"
            "--- Auto-Reply ---\n"
            "Out for a medical appointment March 18. Back March 19.\n"
            "— Jennifer Liu\n\n"
            "--- Original Message ---\n"
            "From: {name} <{name1}@contoso.com>\n"
            "Subject: SAP timeout errors\n\n"
            "SAP transactions are timing out when processing journal "
            "entries. Error: 'Connection to application server timed out "
            "after 30000ms'. This started yesterday afternoon and affects "
            "the entire Finance team. Quarterly close deadline is Friday.",
            "RE: RE: RE: FW: {app} connection errors\n\n"
            "--- Auto-Reply from Susan Park ---\n"
            "I will be out March 17-21. Contact {name} for assistance.\n\n"
            "--- Auto-Reply from Mark Davidson ---\n"
            "On PTO until March 25.\n\n"
            "--- Auto-Reply from {name} ---\n"
            "In meetings all day March 17. Will respond March 18.\n\n"
            "--- Original Message ---\n"
            "SAP is timing out on every transaction since yesterday. "
            "30-second timeout errors on the application server. Finance "
            "team cannot process quarter-end entries. Urgent.",
        ],
        next_best_actions=[
            "Investigate SAP application server timeouts affecting "
            "quarter-end journal entry processing. Ignore the stacked "
            "auto-reply messages — the real issue is at the bottom.",
            "Fix the SAP connection timeout (30000ms) impacting the "
            "Finance team's quarterly close. The auto-reply chain is "
            "noise from the email thread.",
        ],
        remediation_steps=[
            [
                "Check SAP application server health and connection pool status",
                "Review SAP transaction logs for timeout errors during journal processing",
                "Verify network connectivity between workstations and the SAP server",
                "Coordinate with SAP Basis team for resource contention during quarter-end",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# dc-178  Multilingual legal disclaimer overwhelming body
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="dc-178",
        category=Category.SECURITY,
        priority=Priority.P2,
        assigned_team=Team.SECOPS,
        needs_escalation=False,
        missing_information=[MissingInfo.AUTHENTICATION_METHOD, MissingInfo.DEVICE_INFO],
        subjects=[
            "Suspicious login alerts on my account",
            "Unauthorized access attempts — 3 alerts overnight",
            "Security alert — unrecognized IPs accessing my {app} account",
        ],
        descriptions=[
            "Hi Security, I got 3 suspicious login alerts from IPs I "
            "do not recognize (185.220.101.x range) at 2:00 AM, 2:15 AM "
            "and 3:30 AM last night.\n\n"
            "CONFIDENTIALITY NOTICE: This email and any attachments are "
            "for the exclusive use of the intended recipient. If you are "
            "not the intended recipient, do not read, distribute, or act "
            "on this message. Unauthorized review or distribution is "
            "strictly prohibited.\n\n"
            "AVIS DE CONFIDENTIALITE: Ce courriel est destine "
            "exclusivement au destinataire prevu. Toute utilisation non "
            "autorisee est strictement interdite.\n\n"
            "VERTRAULICHKEITSHINWEIS: Diese E-Mail ist ausschliesslich "
            "fuer den vorgesehenen Empfaenger bestimmt. Unbefugte "
            "Nutzung ist strengstens untersagt.\n\n"
            "AVISO DE CONFIDENCIALIDAD: Este correo electronico es para "
            "uso exclusivo del destinatario previsto. Cualquier uso no "
            "autorizado esta estrictamente prohibido.\n\n"
            "{name}, {department}",
            "I received multiple security alerts about login attempts "
            "from unknown IP addresses overnight. The alerts say the "
            "attempts came from a Tor exit node. My account may be "
            "compromised.\n\n"
            "--- Legal Disclaimer (EN/FR/DE/ES) ---\n"
            "This communication is confidential and intended solely for "
            "the addressee. Ce message est confidentiel et destine "
            "uniquement au destinataire. Diese Nachricht ist vertraulich "
            "und nur fuer den Adressaten bestimmt. Este mensaje es "
            "confidencial y destinado unicamente al destinatario. "
            "Unauthorized use is prohibited in all jurisdictions. "
            "L'utilisation non autorisee est interdite. Unbefugte "
            "Nutzung ist verboten. El uso no autorizado esta prohibido. "
            "{name}, {department}",
        ],
        next_best_actions=[
            "Investigate suspicious login attempts from 185.220.101.x "
            "(Tor exit nodes) on the user's account. Ignore the "
            "multilingual legal disclaimers.",
            "Check Azure AD sign-in logs for the reported unauthorized "
            "access attempts. The legal footer is standard email noise.",
        ],
        remediation_steps=[
            [
                "Check Azure AD sign-in logs for the user's account from the reported IPs",
                "Block the 185.220.101.x range if confirmed unauthorized",
                "Force a password reset and verify MFA is enabled",
                "Check if any successful logins occurred from those IPs",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# dc-179  Teams chat transcript pasted into ticket
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="dc-179",
        category=Category.SOFTWARE,
        priority=Priority.P3,
        assigned_team=Team.ENTERPRISE_APPS,
        needs_escalation=False,
        missing_information=[MissingInfo.APPLICATION_VERSION, MissingInfo.DEVICE_INFO],
        subjects=[
            "Teams keeps crashing — chat log for context",
            "Microsoft Teams crash after update — pasting chat",
            "{app} crashes on chat open — see conversation below",
        ],
        descriptions=[
            "[3/17/2026 9:02 AM] {name}:\nhey is Teams working for you?\n\n"
            "[3/17/2026 9:02 AM] Derek:\nyeah seems fine\n\n"
            "[3/17/2026 9:03 AM] {name}:\nmine crashes every time I open "
            "a chat. freezes then closes\n\n"
            "[3/17/2026 9:03 AM] Derek:\nhave you cleared the cache?\n\n"
            "[3/17/2026 9:04 AM] {name}:\nyes. no help. also reinstalled\n\n"
            "[3/17/2026 9:05 AM] Derek:\nsubmit a ticket\n\n"
            "Liked by {name}\n\n"
            "[3/17/2026 9:06 AM] Sofia:\nsame issue here! started today\n\n"
            "Liked by {name}, Liked by Derek\n\n"
            "[3/17/2026 9:07 AM] Sofia:\ni think it was the update last "
            "night\n\n"
            "[3/17/2026 9:10 AM] {name}:\nok submitting now. copying chat\n\n"
            "Teams (classic) crashes when opening any chat window. Started "
            "after overnight update on March 16. Affects at least 2 of us "
            "on the {department} floor.",
            "Pasting our Teams conversation about the issue:\n\n"
            "[9:15 AM] {name}: anyone else having Teams problems?\n"
            "[9:15 AM] Alex: yeah mine keeps freezing\n"
            "[9:16 AM] {name}: same! crashes after 5 seconds\n"
            "[9:16 AM] Priya: me too. started after the update\n"
            "[9:17 AM] {name}: ok I am filing a ticket\n"
            "Liked by Alex, Liked by Priya\n\n"
            "Teams classic crashes on chat open since the March 16 "
            "update. Multiple users affected on {floor}.",
        ],
        next_best_actions=[
            "Investigate Teams (classic) crash-on-chat-open after the "
            "March 16 update. Ignore the chat transcript noise — "
            "multiple users on the floor are affected.",
            "Troubleshoot Teams classic crashing after the overnight "
            "update. The pasted chat confirms multiple affected users.",
        ],
        remediation_steps=[
            [
                "Check the Teams update version deployed on March 16",
                "Clear the Teams cache and Credential Manager entries",
                "Test migrating affected users to the new Teams (v2) client",
                "Roll back the update for affected machines if widespread",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# dc-180  HTTP response dump with 500 error
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="dc-180",
        category=Category.SOFTWARE,
        priority=Priority.P2,
        assigned_team=Team.ENTERPRISE_APPS,
        needs_escalation=False,
        missing_information=[MissingInfo.STEPS_TO_REPRODUCE, MissingInfo.AFFECTED_USERS],
        subjects=[
            "Expense portal returning 500 errors",
            "Internal {app} portal — server error on submit",
            "HTTP 500 on expense report submission",
        ],
        descriptions=[
            "The expense portal gives 500 errors. Browser dev tools "
            "response:\n\n"
            "HTTP/1.1 500 Internal Server Error\n"
            "Server: Microsoft-IIS/10.0\n"
            "X-Powered-By: ASP.NET\n"
            "X-Request-Id: 7f8a2b3c-4d5e-6f7a-8b9c-0d1e2f3a4b5c\n"
            "Set-Cookie: .AspNet.ApplicationCookie=REDACTED; secure\n"
            "Content-Type: text/html; charset=utf-8\n\n"
            "Server Error: NullReferenceException at "
            "Contoso.Expenses.Controllers.SubmitController.Post line 142\n\n"
            "Happens when submitting expense reports. Worked last week. "
            "{name}, {department}",
            "Getting 500 Internal Server Error on the expense portal. "
            "Full HTTP response:\n\n"
            "HTTP/1.1 500 Internal Server Error\n"
            "Date: Mon, 17 Mar 2026 14:32:15 GMT\n"
            "X-AspNet-Version: 4.0.30319\n"
            "X-Correlation-Id: a1b2c3d4-e5f6-7890-abcd-ef1234567890\n"
            "Content-Security-Policy: default-src 'self'\n\n"
            "Stack Trace: System.NullReferenceException at "
            "SubmitController.cs:line 142\n\n"
            "Cannot submit any expense reports since this morning. {name}",
        ],
        next_best_actions=[
            "Fix the NullReferenceException in SubmitController.Post "
            "(line 142) causing 500 errors on expense report submission.",
            "Investigate the expense portal 500 error — the HTTP dump "
            "shows a NullReferenceException in the submit controller.",
        ],
        remediation_steps=[
            [
                "Check application logs for the NullReferenceException details",
                "Review recent deployments to SubmitController.cs for regressions",
                "Verify database connections and dependent services are available",
                "Rollback the last deployment if a regression is identified",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# dc-181  Data URI screenshot flood
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="dc-181",
        category=Category.SOFTWARE,
        priority=Priority.P3,
        assigned_team=Team.ENTERPRISE_APPS,
        needs_escalation=False,
        missing_information=[MissingInfo.APPLICATION_VERSION, MissingInfo.STEPS_TO_REPRODUCE],
        subjects=[
            "Excel charts rendering incorrectly",
            "Chart display broken in {app} after update",
            "Excel chart Y-axis scaling wrong — see screenshots",
        ],
        descriptions=[
            "Charts in Q1 Summary are wrong. Screenshots:\n\n"
            '<img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA'
            'UFAKEBASE64BLOCK1FORINLINESCREENSHOT==" />\n\n'
            '<img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAA'
            'oFAKEBASE64BLOCK2MOREDATA==" />\n\n'
            '<img src="data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQAB'
            'FAKEBASE64BLOCK3SCREENSHOT==" />\n\n'
            "Bar charts show incorrect Y-axis scaling, pie charts "
            "missing legend labels. Excel 365 on {os}. {name}",
            "Excel chart rendering is broken since the update. I tried "
            "to paste screenshots but they showed as data URIs:\n\n"
            "[data:image/png;base64,iVBORw0K...FAKEDATA...==]\n"
            "[data:image/png;base64,iVBORw0K...MOREDATA...==]\n\n"
            "Y-axis values are wrong on bar charts and pie chart "
            "legends disappeared. {name}, {department}",
        ],
        next_best_actions=[
            "Fix Excel 365 chart rendering: bar chart Y-axis scaling "
            "errors and missing pie chart legends after update. Ignore "
            "the inline base64 data.",
            "Investigate Excel chart display regression after the latest "
            "update. The data URI content is screenshot noise.",
        ],
        remediation_steps=[
            [
                "Check Excel 365 version against known chart rendering bugs",
                "Test with a new workbook to isolate file-specific issues",
                "Repair the Office 365 installation via Settings > Apps",
                "Recreate corrupted chart objects if the issue is file-specific",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# dc-182  Multi-ticket thread confusion
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="dc-182",
        category=Category.NETWORK,
        priority=Priority.P2,
        assigned_team=Team.NETWORK,
        needs_escalation=False,
        missing_information=[MissingInfo.NETWORK_LOCATION, MissingInfo.AFFECTED_USERS],
        subjects=[
            "RE: FW: Network issues — ref INC-1847, INC-1902, INC-1955",
            "WiFi drops again — relates to INC-1847/1902/1955/1971",
            "Following up on multiple tickets about {office} WiFi",
        ],
        descriptions=[
            "Following up on this ongoing network problem:\n\n"
            "- INC-1847 (Feb 12): WiFi drops on 5th floor {office}\n"
            "- INC-1902 (Feb 28): Same issue, was 'resolved' but wasn't\n"
            "- INC-1955 (Mar 5): Reopened, fix didn't hold\n"
            "- INC-1971 (Mar 10): Colleague filed about 4th floor same\n"
            "- INC-1988 (Mar 14): Facilities filed about AP replacement\n\n"
            "Current issue: WiFi on 5th floor drops every 15-20 min "
            "during trading hours. AP-B3-5F-02 seems to be the one "
            "failing. Signal drops to zero for 30-60 seconds. {name}",
            "This has been reported multiple times under different "
            "tickets: INC-1847, INC-1902, INC-1955, INC-1971, and "
            "INC-1988. The WiFi on {floor} keeps dropping during peak "
            "hours. The access point near my desk loses signal every "
            "15-20 minutes. Please consolidate these tickets and give "
            "us a permanent fix. {name}, {department}",
        ],
        next_best_actions=[
            "Investigate recurring WiFi drops on the 5th floor — access "
            "point AP-B3-5F-02 fails every 15-20 min during trading. "
            "Consolidate related tickets INC-1847/1902/1955/1971/1988.",
            "Fix the failing access point causing periodic WiFi drops. "
            "Multiple tickets reference the same underlying issue.",
        ],
        remediation_steps=[
            [
                "Inspect and test access point AP-B3-5F-02 for hardware failure",
                "Check for channel interference from neighboring APs",
                "Replace the access point if diagnostics show degradation",
                "Verify the fix holds for a full trading week before closing all tickets",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# dc-183  ServiceDesk notification template noise
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="dc-183",
        category=Category.HARDWARE,
        priority=Priority.P3,
        assigned_team=Team.ENDPOINT,
        needs_escalation=False,
        missing_information=[MissingInfo.DEVICE_INFO, MissingInfo.REPRODUCTION_FREQUENCY],
        subjects=[
            "[ServiceNow] INC0087432 — Update from assignee",
            "[ITSM] Incident Update — keyboard disconnect issue",
            "[ServiceNow] INC0087432 — State changed to Pending",
        ],
        descriptions=[
            "ServiceNow Notification — Incident Update\n"
            "Incident: INC0087432\n"
            "Priority: 3 - Moderate\n"
            "State: Work in Progress -> Pending User\n"
            "Assignment: Endpoint Engineering -> Sarah Chen\n"
            "Updated: 2026-03-17 10:45:22 UTC\n"
            "SLA Status: Within SLA (12h remaining)\n"
            "Category: Hardware > Peripheral Devices\n"
            "CI: WKS-B2-4F-018\n\n"
            "Field Changes:\n"
            "  State: WIP -> Pending User\n"
            "  Priority: 4 -> 3\n\n"
            "Work Note (Sarah Chen):\n"
            "  Dock firmware is v1.2.3, latest is v1.4.1. Scheduling "
            "firmware update.\n\n"
            "Original Description ({name}):\n"
            "  Keyboard and mouse disconnect randomly with docking "
            "station. Happens 3-4 times daily. Lenovo ThinkPad USB-C "
            "Dock Gen 2.",
            "--- ITSM Notification ---\n"
            "Ticket: INC0087432 | Priority: 3 | State: Pending\n"
            "Assigned to: Endpoint Engineering\n"
            "SLA: Within target\n"
            "Activity: Firmware check completed\n\n"
            "User issue: USB peripherals disconnect randomly when "
            "using the docking station. Dock model: Lenovo ThinkPad "
            "USB-C Gen 2. Firmware outdated. {name}, {department}",
        ],
        next_best_actions=[
            "Continue troubleshooting keyboard/mouse disconnections "
            "through the Lenovo dock. Firmware is outdated (v1.2.3 vs "
            "v1.4.1) — update and verify stability.",
            "Update the docking station firmware from v1.2.3 to v1.4.1 "
            "to resolve the USB peripheral disconnection issue.",
        ],
        remediation_steps=[
            [
                "Update docking station firmware from v1.2.3 to v1.4.1",
                "Check USB drivers on the workstation for pending updates",
                "Test peripherals connected directly to isolate device issues",
                "Replace the docking station if disconnections persist after update",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# dc-184  Mojibake encoding corruption
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="dc-184",
        category=Category.SOFTWARE,
        priority=Priority.P3,
        assigned_team=Team.ENTERPRISE_APPS,
        needs_escalation=False,
        missing_information=[MissingInfo.ERROR_MESSAGE, MissingInfo.AUTHENTICATION_METHOD],
        subjects=[
            "SharePoint access broken \u00e2\u20ac\u201c can\u00e2\u20ac\u2122t open documents",
            "SharePoint \u00e2\u20ac\u0153Access Denied\u00e2\u20ac\u009d after it worked yesterday",
            "Can\u00e2\u20ac\u2122t access {app} team site \u00e2\u20ac\u201c permission error",
        ],
        descriptions=[
            "I\u00e2\u20ac\u2122m having trouble accessing SharePoint. When I try to "
            "open documents I get \u00e2\u20ac\u0153Access Denied\u00e2\u20ac\u009d even though I "
            "had access yesterday.\n\n"
            "URL: https://contoso.sharepoint.com/sites/FinanceTeam\n"
            "Library: \u00e2\u20ac\u0153Q1 Reports\u00e2\u20ac\u009d\n\n"
            "Tried:\n"
            "\u00e2\u20ac\u00a2 Clearing browser cache\n"
            "\u00e2\u20ac\u00a2 InPrivate/Incognito mode\n"
            "\u00e2\u20ac\u00a2 Edge, Chrome, Firefox\n\n"
            "Need access urgently \u00e2\u20ac\u201c quarterly close reports due Friday. "
            "{name}, {department}",
            "SharePoint Finance team site gives permission errors since "
            "this morning. I could access it fine yesterday. The "
            "document library shows \u00e2\u20ac\u0153Access Denied\u00e2\u20ac\u009d. I\u00e2\u20ac\u2122ve tried "
            "multiple browsers and clearing cache. {name}",
        ],
        next_best_actions=[
            "Investigate SharePoint Access Denied error on the Finance "
            "Team site. The ticket has mojibake encoding artifacts but "
            "the core issue is a permissions problem.",
            "Fix the SharePoint permissions issue for the Q1 Reports "
            "library. Ignore the encoding corruption in the text.",
        ],
        remediation_steps=[
            [
                "Check the user's SharePoint permissions on the Finance Team site",
                "Verify SharePoint group membership hasn't changed recently",
                "Check if a site admin removed or modified permissions",
                "Re-grant access and verify the user can open documents",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# dc-185  SOAP XML fault dump
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="dc-185",
        category=Category.SOFTWARE,
        priority=Priority.P2,
        assigned_team=Team.ENTERPRISE_APPS,
        needs_escalation=False,
        missing_information=[MissingInfo.AFFECTED_USERS, MissingInfo.BUSINESS_IMPACT],
        subjects=[
            "Trade reconciliation service error",
            "SOAP fault on {app} reconciliation endpoint",
            "End-of-day reconciliation failing — XML error",
        ],
        descriptions=[
            "Trade reconciliation returns errors. Full response:\n\n"
            '<?xml version="1.0" encoding="utf-8"?>\n'
            '<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/'
            'soap/envelope/">\n'
            "  <soap:Body>\n"
            "    <soap:Fault>\n"
            "      <faultcode>soap:Server</faultcode>\n"
            "      <faultstring>SqlException: Timeout expired. The "
            "timeout period elapsed prior to completion.</faultstring>\n"
            "      <detail>\n"
            "        <ErrorCode>RECON-5001</ErrorCode>\n"
            "        <Server>TRADESRV-02</Server>\n"
            "        <Database>TradeReconDB</Database>\n"
            "        <BatchId>EOD-20260317-001</BatchId>\n"
            "      </detail>\n"
            "    </soap:Fault>\n"
            "  </soap:Body>\n"
            "</soap:Envelope>\n\n"
            "Blocking EOD reconciliation for all trading desks. {name}",
            "End-of-day reconciliation is failing with a SOAP fault. "
            "The XML error shows a SQL timeout (RECON-5001) on "
            "TRADESRV-02 TradeReconDB during batch EOD-20260317-001. "
            "All desks are blocked. {name}, {department}",
        ],
        next_best_actions=[
            "Fix the SQL timeout (RECON-5001) in the trade "
            "reconciliation service on TRADESRV-02. The SOAP XML "
            "dump shows TradeReconDB timing out during EOD batch.",
            "Resolve the database timeout blocking end-of-day reconciliation. Ignore the XML formatting noise.",
        ],
        remediation_steps=[
            [
                "Check TRADESRV-02 SQL Server performance and blocking queries",
                "Review the EOD reconciliation stored procedure for long-running queries",
                "Increase SQL command timeout temporarily while investigating root cause",
                "Verify database indexes and statistics are current on TradeReconDB",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# dc-186  Complex HTML table email
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="dc-186",
        category=Category.HARDWARE,
        priority=Priority.P4,
        assigned_team=Team.ENDPOINT,
        needs_escalation=False,
        missing_information=[MissingInfo.DEVICE_INFO, MissingInfo.STEPS_TO_REPRODUCE],
        subjects=[
            "Cannot print org chart email from HR",
            "Printer outputs raw HTML for formatted email",
            "HP printer on {floor} prints garbage for HTML emails",
        ],
        descriptions=[
            "I received the org chart email from HR but when I print "
            "it, the printer outputs raw HTML. The email contains:\n\n"
            '<table style="border-collapse:collapse;width:100%">\n'
            '<tr style="background:#1F4E79;color:white">\n'
            '<td colspan="4">Contoso Organization Chart</td></tr>\n'
            '<tr><td style="border:1px solid #9BC2E6">Executive</td>\n'
            "<td>James Harrison - CEO</td></tr>\n"
            "</table>\n\n"
            "Renders fine on screen but HP LaserJet on {floor} prints "
            "the raw HTML tags. {name}, {department}",
            "Printing HTML-formatted emails shows raw markup instead "
            "of the formatted content. The email has complex nested "
            "tables with inline CSS. HP LaserJet M507 on {floor}. "
            "{name}",
        ],
        next_best_actions=[
            "Investigate the HP LaserJet printing raw HTML instead of "
            "rendered content. Likely a print driver rendering issue.",
            "Fix the print driver or rendering pipeline for HTML emails on the HP LaserJet M507.",
        ],
        remediation_steps=[
            [
                "Update the print driver on the user's workstation",
                "Try printing from a different email client or browser",
                "Test printing to PDF first, then print the PDF",
                "Check HP printer firmware for HTML rendering support",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# dc-187  Very long rambling email with buried issue
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="dc-187",
        category=Category.NETWORK,
        priority=Priority.P3,
        assigned_team=Team.NETWORK,
        needs_escalation=False,
        missing_information=[MissingInfo.DEVICE_INFO, MissingInfo.ENVIRONMENT_DETAILS],
        subjects=[
            "Quick question about my computer",
            "Hey IT — couple of things",
            "Various issues and a network question",
        ],
        descriptions=[
            "Hi IT team,\n\nHope you're doing well! First off, the new "
            "coffee machines are amazing. The oat milk option is great. "
            "I ran into Marcus from Trading yesterday and he was telling "
            "me about the new Bloomberg terminals — sounds cool. "
            "Remember when we all had thick Dell monitors? Now everyone "
            "has thin USB-C ones. Technology moves fast.\n\n"
            "Speaking of monitors, my neighbor got a 4K TV as a second "
            "monitor for gaming. Pretty cool but not relevant to work "
            "I suppose. My kids are into Minecraft — do you support "
            "that? Just kidding.\n\n"
            "Anyway the reason I'm writing — last Tuesday (or maybe "
            "Wednesday, definitely Tuesday because I had a dentist "
            "appointment) when I'm on VPN from home, the network drives "
            "disconnect after exactly 10 minutes of inactivity. Every "
            "time. I have to remap the drive.\n\n"
            "Also are we doing the team outing next month? And can I "
            "get a standing desk? My back is killing me.\n\n"
            "But yeah the network drive thing is the main issue. "
            "\\\\filesrv\\finance disconnects after 10 min idle. {name}",
            "Hi! Long email sorry. Lots going on. But the main thing "
            "is that my mapped network drive disconnects when I'm on "
            "VPN and idle for about 10 minutes. It's \\\\filesrv\\finance "
            "and I have to manually reconnect every time. Started last "
            "week. I also wanted to ask about standing desks and the "
            "team outing but those can wait. The drive disconnect is "
            "urgent because I lose unsaved work. {name}, {department}",
        ],
        next_best_actions=[
            "Fix the mapped drive (\\\\filesrv\\finance) disconnecting "
            "after 10 minutes idle on VPN. Likely a session timeout or "
            "SMB keepalive issue. Ignore the rambling context.",
            "Investigate the VPN/SMB session timeout causing network "
            "drive disconnections after 10 minutes of inactivity.",
        ],
        remediation_steps=[
            [
                "Check VPN idle timeout and SMB session keepalive settings",
                "Verify GPO settings for mapped drive persistence over VPN",
                "Increase SMB session timeout on the file server or VPN gateway",
                "Test with persistent net use /persistent:yes mapping",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# dc-188  Embedded EML with RFC 822 headers
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="dc-188",
        category=Category.SOFTWARE,
        priority=Priority.P3,
        assigned_team=Team.ENTERPRISE_APPS,
        needs_escalation=False,
        missing_information=[MissingInfo.CONFIGURATION_DETAILS, MissingInfo.TIMESTAMP],
        subjects=[
            "FW: Email delivery failure — raw headers included",
            "Forwarding failed email with headers for IT review",
            "Email from partner.com rejected — embedded original",
        ],
        descriptions=[
            "Forwarding the failed email. My client included raw "
            "headers:\n\n"
            "Content-Type: message/rfc822\n"
            "Return-Path: <noreply@partner.com>\n"
            "Received: from mail-gw01.contoso.com (10.0.1.25) by "
            "mail-hub02.contoso.com with ESMTPS\n"
            "DKIM-Signature: v=1; a=rsa-sha256; d=partner.com\n"
            "From: alerts@partner.com\n"
            "To: settlements@contoso.com\n"
            "Subject: Daily Settlement Confirmation\n"
            "MIME-Version: 1.0\n"
            'Content-Type: multipart/mixed; boundary="----=_Part_123"\n\n'
            "Rejection: 550 5.7.1 Content policy violation.\n\n"
            "We need daily settlement emails from partner.com to arrive. "
            "Stopped 3 days ago. Team is manually reconciling. {name}",
            "Email from partner.com to settlements@contoso.com is being "
            "rejected with 550 5.7.1 content policy violation. Raw email "
            "headers show rejection at our gateway. The settlement team "
            "needs these daily. {name}, {department}",
        ],
        next_best_actions=[
            "Fix email delivery rejection (550 5.7.1) for settlement "
            "emails from partner.com. The EML headers show the block "
            "occurs at the Contoso email gateway.",
            "Investigate the content policy blocking partner.com emails "
            "to settlements@contoso.com. Ignore the raw RFC 822 noise.",
        ],
        remediation_steps=[
            [
                "Check Exchange transport rules for recent content filter changes",
                "Review mail gateway logs for the specific rejection reason",
                "Whitelist partner.com or the specific sender if legitimate",
                "Verify DKIM/SPF/DMARC for partner.com are passing validation",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# dc-189  OCR scan artifacts
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="dc-189",
        category=Category.DATA,
        priority=Priority.P3,
        assigned_team=Team.DATA_PLATFORM,
        needs_escalation=False,
        missing_information=[MissingInfo.BUSINESS_IMPACT, MissingInfo.CONFIGURATION_DETAILS],
        subjects=[
            "Database backup report — OCR scan from printout",
            "Scanned backup status report — OCR quality poor",
            "Backup failure report from server room printout",
        ],
        descriptions=[
            "Scanned the printout from the server room:\n\n"
            "CONT0SO F1NANCIAL SERV1CES\n"
            "Oata8ase Backup Rep0rt - March 2O26\n"
            "Server: SQLSRV-O1.contoso.1ocal\n"
            "Oata8ase: TradeL edgerO8 (1.2 T8)\n"
            "Last 8ackup: 2O26-O3-15\n"
            "Status: FA1LED\n"
            "Err0r: 1nsufficient disk space\n"
            "  Avai1ab1e: 45.2 G8\n"
            "  Required: 1,2OO G8\n\n"
            "TradeLedgerDB backup on SQLSRV-01 failing since March 15 "
            "due to insufficient disk space on backup volume. {name}",
            "OCR scan of the backup report printout (sorry for quality):\n\n"
            "Backup St@tus: FA1LED\n"
            "Server: SQLSRV-O1\n"
            "D8: TradeLedger0B\n"
            "Reason: Disk space (45 GB free, need 1.2 TB)\n\n"
            "The backup has been failing for 2 days. {name}, {department}",
        ],
        next_best_actions=[
            "Fix TradeLedgerDB backup failure on SQLSRV-01 due to "
            "insufficient disk space (45 GB available, 1.2 TB needed). "
            "The OCR text has recognition errors but the issue is clear.",
            "Resolve the backup volume space shortage for TradeLedgerDB. Ignore OCR noise in the scanned text.",
        ],
        remediation_steps=[
            [
                "Free disk space by archiving or deleting old backup files",
                "Expand backup volume storage to accommodate the 1.2 TB database",
                "Re-run the backup manually and verify completion",
                "Set up monitoring alerts for backup volume at 80% capacity",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# dc-190  WinRM remote session transcript
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="dc-190",
        category=Category.SOFTWARE,
        priority=Priority.P2,
        assigned_team=Team.ENTERPRISE_APPS,
        needs_escalation=False,
        missing_information=[MissingInfo.BUSINESS_IMPACT, MissingInfo.AFFECTED_USERS],
        subjects=[
            "Remote diagnostics output from failing server",
            "WinRM session output — APPSRV-04 services down",
            "Server APPSRV-04 port conflict — diagnostic transcript",
        ],
        descriptions=[
            "WinRM diagnostics on APPSRV-04:\n\n"
            "PS> Enter-PSSession APPSRV-04\n"
            "[APPSRV-04]: PS> Get-Service | ? Status -eq Stopped\n\n"
            "Stopped  ContosoTradeAPI   Contoso Trade API Service\n"
            "Stopped  W3SVC            World Wide Web Publishing\n"
            "Stopped  WAS              Windows Process Activation\n\n"
            "[APPSRV-04]: PS> Get-EventLog Application -Newest 3 "
            "-EntryType Error\n"
            "Error  ContosoTradeAPI  Exit code: 0xC0000005\n"
            "Error  W3SVC  Port 443 already in use\n"
            "Error  WAS  Failed to start — port conflict\n\n"
            "[APPSRV-04]: PS> netstat -ano | Select-String 443\n"
            "  TCP  0.0.0.0:443  LISTENING  7892\n\n"
            "[APPSRV-04]: PS> Get-Process -Id 7892\n"
            "  7892  ContosoReconSvc\n\n"
            "Summary: ContosoReconSvc holds port 443, preventing W3SVC "
            "and TradeAPI from starting. {name}",
            "Remote session output shows APPSRV-04 has a port conflict: "
            "ContosoReconSvc (PID 7892) is holding port 443, blocking "
            "W3SVC and ContosoTradeAPI. Multiple services are stopped. "
            "The verbose WinRM transcript confirms the issue. {name}, "
            "{department}",
        ],
        next_best_actions=[
            "Fix the port 443 conflict on APPSRV-04: ContosoReconSvc "
            "is holding the port, preventing W3SVC and TradeAPI from "
            "starting. The WinRM transcript provides diagnostics.",
            "Resolve the service port conflict on APPSRV-04. "
            "ContosoReconSvc needs to be reconfigured to a different "
            "port so W3SVC can start.",
        ],
        remediation_steps=[
            [
                "Stop ContosoReconSvc and reconfigure it to use port 8443",
                "Restart W3SVC and ContosoTradeAPI after freeing port 443",
                "Investigate why ContosoReconSvc started binding to port 443",
                "Set up service dependency ordering to prevent port conflicts",
            ],
        ],
    )
)


# ---------------------------------------------------------------------------
# dc-191  Very long rambling email — buried expense issue
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="dc-191",
        category=Category.SOFTWARE,
        priority=Priority.P3,
        assigned_team=Team.ENTERPRISE_APPS,
        needs_escalation=False,
        missing_information=[MissingInfo.ERROR_MESSAGE, MissingInfo.SCREENSHOT_OR_ATTACHMENT],
        subjects=[
            "Long email about various office issues and expense report",
            "Rambling message — SAP Concur expense submission problem buried inside",
            "Multiple topics in one email — expense system not working",
        ],
        descriptions=[
            "Hi team, this is {name} from {department}. I wanted to start by saying "
            "that the new coffee machine on floor 12 is great, and also the parking "
            "situation has been terrible lately. I spent 30 minutes looking for a "
            "spot yesterday. Anyway, I also wanted to mention that the holiday "
            "party was fantastic — kudos to whoever organized it. Oh, and the "
            "elevators in building B are super slow. Speaking of slow, my laptop "
            "has been sluggish but that's another story. The real reason I'm "
            "writing is that I cannot submit my expense report in SAP Concur — "
            "every time I click Submit it just spins and then shows a generic "
            "error. I've tried three different browsers. Could someone look "
            "into this? Also, the vending machines on floor 9 are out of "
            "sparkling water again. Thanks!",
            "{name} from {department} sent a 10,000-character email covering "
            "office complaints, parking, coffee, elevators, and vending machines. "
            "Buried near the end: SAP Concur expense submission fails with a "
            "generic error on Submit across all browsers. The actual IT issue "
            "is a single paragraph in an extremely long, rambling message.",
        ],
        next_best_actions=[
            "Investigate the SAP Concur expense submission failure reported "
            "by {name}. The error occurs on Submit across multiple browsers. "
            "Ignore the non-IT content in the lengthy email.",
            "Escalate the SAP Concur Submit-button failure to the "
            "Enterprise Apps team. The user has tested three browsers.",
        ],
        remediation_steps=[
            [
                "Verify SAP Concur service health and recent deployment changes",
                "Check the user's Concur profile and delegation/approval settings",
                "Reproduce the submission error in a test environment",
                "Engage SAP Concur vendor support if the issue is platform-side",
            ],
        ],
    )
)


# ---------------------------------------------------------------------------
# dc-192  Multiple base64 PNG data URIs inline — Citrix freeze
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="dc-192",
        category=Category.SOFTWARE,
        priority=Priority.P2,
        assigned_team=Team.ENTERPRISE_APPS,
        needs_escalation=False,
        missing_information=[MissingInfo.ENVIRONMENT_DETAILS, MissingInfo.DEVICE_INFO],
        subjects=[
            "Citrix session freezing — screenshots attached inline",
            "Citrix freezes with inline base64 image evidence",
            "Session freeze in Citrix — multiple data URI screenshots",
        ],
        descriptions=[
            "{name} from {department} reports Citrix session freezing. "
            "Inline screenshots (base64 data URIs):\n\n"
            "Screenshot 1: data:image/png;base64,iVBORw0KGgoAAAANSUhEUg"
            "AAAA...[ 50KB of base64 data truncated ]...\n\n"
            "Screenshot 2: data:image/png;base64,iVBORw0KGgoAAAANSUhEUg"
            "BBBB...[ 60KB of base64 data truncated ]...\n\n"
            "Screenshot 3: data:image/png;base64,iVBORw0KGgoAAAANSUhEUg"
            "CCCC...[ 45KB of base64 data truncated ]...\n\n"
            "The session locks up after about 20 minutes of use and "
            "requires a forced disconnect.",
            "Citrix session freezing after ~20 minutes. {name} ({department}) "
            "embedded three large base64 PNG data URIs directly in the "
            "message body instead of attaching files. The actual issue is "
            "a reproducible session freeze requiring forced disconnect.",
        ],
        next_best_actions=[
            "Investigate the Citrix session freeze reported by {name}. "
            "Sessions lock after ~20 minutes and need forced disconnect. "
            "Disregard the inline base64 image noise.",
            "Check Citrix server resource utilization and session "
            "timeout policies. The user experiences consistent "
            "freezes at the 20-minute mark.",
        ],
        remediation_steps=[
            [
                "Review Citrix Director for session performance metrics and errors",
                "Check VDA resource utilization (CPU, memory, GPU) during freeze window",
                "Verify Citrix session reliability settings and timeout policies",
                "Test with a fresh Citrix profile to rule out profile corruption",
            ],
        ],
    )
)


# ---------------------------------------------------------------------------
# dc-193  Raw base64 JPEG photo — badge reader not working
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="dc-193",
        category=Category.HARDWARE,
        priority=Priority.P3,
        assigned_team=Team.ENDPOINT,
        needs_escalation=False,
        missing_information=[MissingInfo.DEVICE_INFO, MissingInfo.NETWORK_LOCATION],
        subjects=[
            "Badge reader not working — photo of device pasted as base64",
            "Door badge scanner broken — raw JPEG data in message",
            "Badge reader failure with inline base64 photo evidence",
        ],
        descriptions=[
            "{name} from {department}: My badge reader at the south "
            "entrance isn't working. Here's a photo:\n\n"
            "/9j/4AAQSkZJRgABAQAAAQABAAD/2wCEAAkGBxMTEhUTExMW"
            "FhUX...[ 120KB of raw base64 JPEG data ]..."
            "Fh8nHBYfGh0lHB4aIRAkICAgI/8QAHwAAAQUBAQEBAQEAAAA"
            "...[ continues for thousands of characters ]...\n\n"
            "The red light just blinks and doesn't read my card.",
            "Badge reader at the south entrance is non-functional. "
            "{name} ({department}) pasted a raw base64-encoded JPEG "
            "photo directly into the ticket (120KB+ of encoded data). "
            "The actual issue: the reader blinks red and does not "
            "read any badge.",
        ],
        next_best_actions=[
            "Dispatch facilities/endpoint team to inspect the south "
            "entrance badge reader. It blinks red and refuses to "
            "read badges. Ignore the base64 image data in the ticket.",
            "Check whether the badge reader at the south entrance "
            "is online in the access control system. The device may "
            "need a firmware reset or physical replacement.",
        ],
        remediation_steps=[
            [
                "Verify badge reader status in the access control management system",
                "Power-cycle the badge reader and check network connectivity",
                "Test with a known-good badge to rule out card-specific issues",
                "Replace the reader unit if hardware failure is confirmed",
            ],
        ],
    )
)


# ---------------------------------------------------------------------------
# dc-194  HTML email with nested tables and inline CSS — SharePoint access denied
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="dc-194",
        category=Category.ACCESS_AUTH,
        priority=Priority.P2,
        assigned_team=Team.IAM,
        needs_escalation=False,
        missing_information=[MissingInfo.AFFECTED_SYSTEM, MissingInfo.AUTHENTICATION_METHOD],
        subjects=[
            "SharePoint access denied — request wrapped in complex HTML",
            "Cannot access SharePoint site — HTML-heavy email format",
            "SharePoint permission issue buried in nested HTML tables",
        ],
        descriptions=[
            "<html><body><table border=\"1\" style=\"border-collapse:"
            "collapse;\"><tr><td style=\"padding:10px;\"><table><tr>"
            "<td style=\"font-family:Comic Sans MS;\"><table><tr><td>"
            "<b>From:</b> {name}</td></tr><tr><td><b>Dept:</b> "
            "{department}</td></tr></table></td></tr></table></td></tr>"
            "<tr><td><table><tr><td style=\"color:#333;\">"
            "I keep getting Access Denied when opening the {department} "
            "SharePoint site. I need access urgently for the quarterly "
            "review.</td></tr></table></td></tr>"
            "</table></body></html>",
            "{name} from {department} is getting Access Denied on their "
            "department SharePoint site. The request was sent as an HTML "
            "email with 50+ nested tables and inline CSS, obscuring the "
            "one-sentence issue: they cannot open the SharePoint site "
            "and need access for the quarterly review.",
        ],
        next_best_actions=[
            "Grant or verify {name}'s permissions on the {department} "
            "SharePoint site. They are receiving Access Denied and need "
            "access for the quarterly review.",
            "Check SharePoint site permissions and Azure AD group "
            "membership for {name}. Ensure the {department} site "
            "collection permissions are correctly configured.",
        ],
        remediation_steps=[
            [
                "Verify the user's Azure AD group membership for SharePoint access",
                "Check SharePoint site collection permissions and sharing settings",
                "Grant appropriate access level and confirm the user can open the site",
                "Review whether a recent permissions change caused the denial",
            ],
        ],
    )
)


# ---------------------------------------------------------------------------
# dc-195  Windows-1252 mojibake corrupting CJK characters — CRM crash
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="dc-195",
        category=Category.SOFTWARE,
        priority=Priority.P2,
        assigned_team=Team.ENTERPRISE_APPS,
        needs_escalation=False,
        missing_information=[MissingInfo.APPLICATION_VERSION, MissingInfo.STEPS_TO_REPRODUCE],
        subjects=[
            "CRM crashing — garbled CJK characters in description",
            "Mojibake-corrupted ticket — CRM application failure",
            "CRM app crash with encoding-corrupted text",
        ],
        descriptions=[
            "{name} ({department}): CRM\u30a2\u30d7\u30ea\u30b1"
            "\u30fc\u30b7\u30e7\u30f3\u304c\u30af\u30e9"
            "\u30c3\u30b7\u30e5\u3057\u307e\u3059"
            "\u3002 The CRM application crashes whenever I open "
            "the customer detail page for accounts with Japanese "
            "characters. Error: Unhandled exception in contoso.crm.dll. "
            "This started after the last Windows update.",
            "CRM application crashes on customer detail pages containing "
            "CJK characters. The ticket from {name} ({department}) has "
            "Windows-1252 mojibake throughout — the Japanese text was "
            "garbled by an encoding mismatch. The actual issue: CRM "
            "throws an unhandled exception in contoso.crm.dll since "
            "the latest Windows update.",
        ],
        next_best_actions=[
            "Investigate the CRM crash on customer detail pages with "
            "CJK characters. The exception is in contoso.crm.dll and "
            "started after a recent Windows update. Mojibake in the "
            "ticket is an encoding artifact, not the root cause.",
            "Roll back or patch the CRM module that crashes when "
            "rendering CJK text. Coordinate with the vendor if "
            "contoso.crm.dll is a third-party component.",
        ],
        remediation_steps=[
            [
                "Collect crash dumps from the CRM application for analysis",
                "Identify which Windows update introduced the regression",
                "Test CRM with the problematic update rolled back",
                "Engage the CRM vendor for a hotfix addressing CJK rendering",
            ],
        ],
    )
)


# ---------------------------------------------------------------------------
# dc-196  Emoji-heavy message with minimal English — Teams calls dropping
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="dc-196",
        category=Category.NETWORK,
        priority=Priority.P2,
        assigned_team=Team.NETWORK,
        needs_escalation=False,
        missing_information=[MissingInfo.NETWORK_LOCATION, MissingInfo.DEVICE_INFO],
        subjects=[
            "Teams calls dropping — emoji-heavy description",
            "Call drops in Microsoft Teams — minimal text",
            "Teams audio/video issues — message full of emojis",
        ],
        descriptions=[
            "\U0001f4de\u274c\U0001f4de\u274c\U0001f4de\u274c "
            "{name} {department} \U0001f4de\u274c\U0001f4de\u274c\n\n"
            "\U0001f621\U0001f621\U0001f621 Teams calls DROPPING "
            "\U0001f621\U0001f621\U0001f621\n"
            "\U0001f4de\u27a1\ufe0f\U0001f480 every 5 min "
            "\u23f1\ufe0f\u23f1\ufe0f\u23f1\ufe0f\n"
            "\U0001f50a\u274c audio gone \U0001f50a\u274c\n"
            "\U0001f4f9\u274c video frozen \U0001f4f9\u274c\n"
            "\U0001f3e2 floor 14 \U0001f3e2\n"
            "\U0001f4bb laptop + dock \U0001f4bb\n"
            "\U0001f4f6 WiFi? Ethernet? \U0001f4f6\n"
            "\U0001f64f\U0001f64f\U0001f64f FIX PLS "
            "\U0001f64f\U0001f64f\U0001f64f",
            "Teams calls are dropping every 5 minutes for {name} on "
            "floor 14 ({department}). The ticket is nearly all emojis "
            "with minimal English. Extracted issue: audio cuts out and "
            "video freezes, requiring reconnection. User is on a "
            "laptop with docking station, connectivity type unclear.",
        ],
        next_best_actions=[
            "Investigate Teams call quality for {name} on floor 14. "
            "Calls drop every ~5 minutes with audio loss and video "
            "freeze. Check both Wi-Fi and wired connectivity.",
            "Run network diagnostics on floor 14 to identify packet "
            "loss or jitter causing Teams call drops. The user's "
            "connection type (Wi-Fi vs Ethernet) needs confirmation.",
        ],
        remediation_steps=[
            [
                "Pull Teams call quality dashboard (CQD) data for the user",
                "Check floor 14 access point health and channel utilization",
                "Test with a wired Ethernet connection to isolate Wi-Fi issues",
                "Verify QoS policies are correctly applied for Teams traffic",
            ],
        ],
    )
)


# ---------------------------------------------------------------------------
# dc-197  Deep RE:/FW: email chain — print server queue stuck
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="dc-197",
        category=Category.HARDWARE,
        priority=Priority.P3,
        assigned_team=Team.ENDPOINT,
        needs_escalation=False,
        missing_information=[MissingInfo.AFFECTED_SYSTEM, MissingInfo.ERROR_MESSAGE],
        subjects=[
            "RE: RE: RE: FW: RE: Print server queue stuck",
            "Deeply nested email thread about print queue issue",
            "15-deep reply chain — printer queue jammed",
        ],
        descriptions=[
            "-----Original Message-----\n"
            "From: {name} ({department})\n"
            "Subject: RE: RE: RE: FW: RE: RE: FW: RE: RE: RE: RE: "
            "FW: RE: RE: RE: Printer issue\n\n"
            "Still broken.\n\n"
            "--- 14 previous replies omitted for brevity ---\n\n"
            "...original message from 3 weeks ago: The print queue on "
            "PRTSRV-02 is stuck. Jobs go in but never print. {name}, "
            "{department}.",
            "A 15-deep RE:/FW: email chain about a print server issue. "
            "{name} ({department}) reports the queue on PRTSRV-02 is "
            "stuck — jobs enter the queue but never print. The thread "
            "spans three weeks of back-and-forth with the most recent "
            "reply simply saying 'Still broken.'",
        ],
        next_best_actions=[
            "Investigate the stuck print queue on PRTSRV-02. Jobs are "
            "accepted but never processed. This has been ongoing for "
            "three weeks per the email thread from {name}.",
            "Clear and restart the print spooler on PRTSRV-02. If "
            "the queue remains stuck, check the print driver and "
            "physical printer connectivity.",
        ],
        remediation_steps=[
            [
                "Clear all stuck jobs from the PRTSRV-02 print queue",
                "Restart the Print Spooler service on PRTSRV-02",
                "Verify network connectivity between PRTSRV-02 and the physical printer",
                "Update or reinstall the printer driver if the issue recurs",
            ],
        ],
    )
)


# ---------------------------------------------------------------------------
# dc-198  Huge multilingual legal disclaimer signature — Outlook search broken
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="dc-198",
        category=Category.SOFTWARE,
        priority=Priority.P3,
        assigned_team=Team.ENTERPRISE_APPS,
        needs_escalation=False,
        missing_information=[MissingInfo.APPLICATION_VERSION, MissingInfo.ENVIRONMENT_DETAILS],
        subjects=[
            "Outlook search broken — massive legal disclaimer in message",
            "Search not working in Outlook — 4KB disclaimer signature",
            "Outlook indexing issue with huge multilingual signature block",
        ],
        descriptions=[
            "{name} ({department}): Outlook search returns no results "
            "for any keyword.\n\n"
            "--- Confidentiality Notice / Avis de confidentialit\u00e9 / "
            "Vertraulichkeitshinweis / \u6a5f\u5bc6\u901a\u77e5 / Aviso de "
            "confidencialidad ---\n"
            "This email and any attachments are confidential and "
            "intended solely for the addressee. If you have received "
            "this in error, please notify the sender immediately and "
            "delete all copies. Ce courriel et ses pi\u00e8ces jointes "
            "sont confidentiels... Der Inhalt dieser E-Mail ist "
            "vertraulich... \u3053\u306e\u96fb\u5b50\u30e1\u30fc\u30eb"
            "\u306f\u6a5f\u5bc6\u60c5\u5831\u3092\u542b\u3093"
            "\u3067\u3044\u307e\u3059... "
            "Este correo electr\u00f3nico es confidencial...\n"
            "[Disclaimer continues in 8 more languages for 4KB total]",
            "Outlook search is returning zero results for {name} "
            "({department}). The ticket body is dominated by a 4KB+ "
            "multilingual legal disclaimer in English, French, German, "
            "Japanese, Spanish, and 8 other languages. The actual "
            "issue is one sentence: Outlook search returns no results.",
        ],
        next_best_actions=[
            "Rebuild the Outlook search index for {name}. Search is "
            "returning zero results for all queries. The lengthy "
            "multilingual disclaimer in the ticket is irrelevant.",
            "Troubleshoot Outlook search indexing. Check Windows "
            "Search service status and Outlook indexing options on "
            "the user's workstation.",
        ],
        remediation_steps=[
            [
                "Check Windows Search service status and indexing health",
                "Rebuild the Outlook search index via Indexing Options",
                "Verify the Outlook OST/PST file integrity with scanpst.exe",
                "Confirm search returns results after re-indexing completes",
            ],
        ],
    )
)


# ---------------------------------------------------------------------------
# dc-199  Message truncated mid-sentence by gateway — VDI black screen
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="dc-199",
        category=Category.SOFTWARE,
        priority=Priority.P1,
        assigned_team=Team.ENTERPRISE_APPS,
        needs_escalation=True,
        missing_information=[MissingInfo.ERROR_MESSAGE, MissingInfo.AFFECTED_USERS],
        subjects=[
            "VDI session black screen — message truncated by gateway",
            "[TRUNCATED] VDI desktop goes black after login",
            "Incomplete ticket — VDI black screen issue cut off mid-sentence",
        ],
        descriptions=[
            "{name} from {department}: I logged into my VDI desktop "
            "this morning and after entering my credentials the screen "
            "went completely black. I can see the mouse cursor but "
            "nothing else loads. I have tried restarting the session "
            "three times. This is affecting my ability to"
            "\n\n--- Message truncated by gateway (max 2048 bytes) ---",
            "VDI session shows a black screen after login for {name} "
            "({department}). The ticket was truncated mid-sentence by "
            "a gateway size limit. From what is readable: the user "
            "sees only a mouse cursor after authentication, and "
            "restarting the session has not helped.",
        ],
        next_best_actions=[
            "Investigate VDI black screen after login for {name}. "
            "The user sees a cursor but no desktop loads. Note: the "
            "original ticket was truncated — follow up for details.",
            "Check the VDI infrastructure for issues affecting "
            "desktop rendering. The user's session authenticates "
            "but displays only a black screen with a cursor.",
        ],
        remediation_steps=[
            [
                "Check VDI broker logs for session allocation errors",
                "Verify the user's VDI profile is not corrupted",
                "Reset the VDI session and assign a fresh virtual desktop",
                "Follow up with the user for any truncated information",
            ],
        ],
    )
)


# ---------------------------------------------------------------------------
# dc-200  500+ line Java stack trace — trading platform latency
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="dc-200",
        category=Category.SOFTWARE,
        priority=Priority.P1,
        assigned_team=Team.ENTERPRISE_APPS,
        needs_escalation=True,
        missing_information=[MissingInfo.BUSINESS_IMPACT, MissingInfo.TIMESTAMP],
        subjects=[
            "Trading platform latency — massive Java stack trace pasted",
            "500-line stack trace — ContosoTradeEngine performance issue",
            "Trading platform slow with inline Java exception dump",
        ],
        descriptions=[
            "{name} ({department}): The trading platform is "
            "experiencing severe latency. Here is the stack trace:\n\n"
            "java.lang.OutOfMemoryError: GC overhead limit exceeded\n"
            "\tat com.contoso.trade.engine.OrderProcessor.process"
            "(OrderProcessor.java:847)\n"
            "\tat com.contoso.trade.engine.MatchingEngine.execute"
            "(MatchingEngine.java:312)\n"
            "\tat com.contoso.trade.core.Pipeline.run"
            "(Pipeline.java:156)\n"
            "\tat com.contoso.trade.core.WorkerThread.doWork"
            "(WorkerThread.java:89)\n"
            "... [496 more frames omitted for brevity] ...\n\n"
            "Trades are taking 30+ seconds instead of sub-second.",
            "Trading platform latency: 30+ seconds per trade instead "
            "of sub-second. {name} ({department}) pasted a 500+ line "
            "Java stack trace showing OutOfMemoryError (GC overhead "
            "limit exceeded) in OrderProcessor. The root cause is a "
            "memory issue in the ContosoTradeEngine.",
        ],
        next_best_actions=[
            "URGENT: Trading platform is experiencing 30x latency due "
            "to OutOfMemoryError in the ContosoTradeEngine. The Java "
            "heap is exhausted. Immediate action needed.",
            "Increase JVM heap allocation for ContosoTradeEngine and "
            "investigate the memory leak in OrderProcessor. Current "
            "trade latency is 30+ seconds.",
        ],
        remediation_steps=[
            [
                "Restart ContosoTradeEngine with increased JVM heap (-Xmx8g)",
                "Capture a heap dump before restart for root cause analysis",
                "Monitor GC logs to identify memory leak patterns",
                "Deploy a hotfix for the OrderProcessor memory leak",
            ],
        ],
    )
)


# ---------------------------------------------------------------------------
# dc-201  Double-encoded HTML entities — ServiceNow form not submitting
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="dc-201",
        category=Category.SOFTWARE,
        priority=Priority.P3,
        assigned_team=Team.ENTERPRISE_APPS,
        needs_escalation=False,
        missing_information=[MissingInfo.STEPS_TO_REPRODUCE, MissingInfo.APPLICATION_VERSION],
        subjects=[
            "ServiceNow form not submitting — double-encoded HTML",
            "Can't submit ServiceNow request — garbled HTML entities",
            "ServiceNow form error with entity corruption",
        ],
        descriptions=[
            "{name} from {department}: I can&amp;amp;#39;t submit the "
            "ServiceNow change request form. When I click "
            "&amp;amp;quot;Submit&amp;amp;quot; the page shows "
            "&amp;amp;quot;Validation Error&amp;amp;quot; and the "
            "form fields are cleared. I&amp;amp;#39;ve tried in "
            "Chrome and Edge. This is blocking our {department} "
            "deployment.",
            "ServiceNow change request form fails on Submit with a "
            "Validation Error. {name} ({department}) reports the issue "
            "in a ticket riddled with double-encoded HTML entities "
            "(&amp;amp; throughout). The actual problem: the form "
            "clears all fields and shows a validation error on submit.",
        ],
        next_best_actions=[
            "Investigate the ServiceNow change request form validation "
            "error on submit. The form clears fields instead of saving. "
            "Issue reproduced in Chrome and Edge by {name}.",
            "Check ServiceNow form configuration and recent catalog "
            "updates that may have broken validation on the change "
            "request form.",
        ],
        remediation_steps=[
            [
                "Check ServiceNow system logs for form validation errors",
                "Review recent catalog item or form layout changes",
                "Clear the browser cache and test submission in an incognito window",
                "Restore the form configuration from a known-good backup if needed",
            ],
        ],
    )
)


# ---------------------------------------------------------------------------
# dc-202  Stuttering duplicate paragraphs — Exchange mailbox quota exceeded
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="dc-202",
        category=Category.SOFTWARE,
        priority=Priority.P3,
        assigned_team=Team.ENTERPRISE_APPS,
        needs_escalation=False,
        missing_information=[MissingInfo.AFFECTED_USERS, MissingInfo.BUSINESS_IMPACT],
        subjects=[
            "Exchange mailbox quota exceeded — duplicated text in request",
            "Mailbox full — same paragraph repeated 4 times",
            "Stuttering duplicate message — Exchange quota issue",
        ],
        descriptions=[
            "{name} ({department}): My mailbox is full and I can't "
            "receive new emails. Please increase my quota.\n\n"
            "{name} ({department}): My mailbox is full and I can't "
            "receive new emails. Please increase my quota.\n\n"
            "{name} ({department}): My mailbox is full and I can't "
            "receive new emails. Please increase my quota.\n\n"
            "{name} ({department}): My mailbox is full and I can't "
            "receive new emails. Please increase my quota.",
            "Exchange mailbox quota exceeded for {name} ({department}). "
            "The user cannot receive new emails. The ticket contains "
            "the same single-sentence request duplicated four times, "
            "likely from a client glitch. Issue: mailbox is full and "
            "needs a quota increase or cleanup.",
        ],
        next_best_actions=[
            "Increase the Exchange mailbox quota for {name} or assist "
            "with mailbox cleanup. The user cannot receive emails due "
            "to a full mailbox.",
            "Review the mailbox size and retention policies for "
            "{name} ({department}). Determine if a quota increase "
            "or archival is appropriate.",
        ],
        remediation_steps=[
            [
                "Check current mailbox size and quota in Exchange Admin Center",
                "Enable or expand the user's online archive mailbox",
                "Apply a retention policy to auto-archive old items",
                "Increase the mailbox quota if within organizational policy",
            ],
        ],
    )
)


# ---------------------------------------------------------------------------
# dc-203  Raw MIME multipart with boundary markers — email attachments corrupted
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="dc-203",
        category=Category.SOFTWARE,
        priority=Priority.P2,
        assigned_team=Team.ENTERPRISE_APPS,
        needs_escalation=False,
        missing_information=[MissingInfo.AFFECTED_SYSTEM, MissingInfo.CONFIGURATION_DETAILS],
        subjects=[
            "Email attachments corrupted — raw MIME data in ticket",
            "MIME boundary markers in message — attachment corruption",
            "Corrupted attachments with inline MIME multipart data",
        ],
        descriptions=[
            "MIME-Version: 1.0\n"
            "Content-Type: multipart/mixed; boundary=\"----=_Part_"
            "12345\"\n\n"
            "------=_Part_12345\n"
            "Content-Type: text/plain; charset=utf-8\n\n"
            "{name} from {department}: All email attachments I receive "
            "are showing as corrupted .dat files instead of their "
            "original format.\n\n"
            "------=_Part_12345\n"
            "Content-Type: application/octet-stream\n"
            "Content-Disposition: attachment; filename=\"report.xlsx\""
            "\n\nUEsDBBQAAAA...[ truncated ]...\n"
            "------=_Part_12345--",
            "Email attachments are arriving as corrupted .dat files "
            "for {name} ({department}). The ticket itself contains raw "
            "MIME multipart data with boundary markers, suggesting the "
            "email gateway is not properly parsing MIME parts. Actual "
            "issue: all received attachments are unreadable.",
        ],
        next_best_actions=[
            "Investigate email attachment corruption for {name}. All "
            "inbound attachments arrive as .dat files. The MIME data "
            "in the ticket suggests a gateway parsing issue.",
            "Check the email gateway and Exchange transport rules for "
            "MIME handling issues. Attachments are being converted to "
            ".dat files during transit.",
        ],
        remediation_steps=[
            [
                "Review Exchange transport rules that may modify attachments",
                "Check the email gateway (e.g., Proofpoint, Mimecast) MIME settings",
                "Test by sending attachments from an external address to the user",
                "Verify Outlook TNEF settings are not forcing winmail.dat conversion",
            ],
        ],
    )
)


# ---------------------------------------------------------------------------
# dc-204  Inline base64 PDF pasted as text — SQL Server replication lag
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="dc-204",
        category=Category.SOFTWARE,
        priority=Priority.P1,
        assigned_team=Team.DATA_PLATFORM,
        needs_escalation=True,
        missing_information=[MissingInfo.TIMESTAMP, MissingInfo.BUSINESS_IMPACT],
        subjects=[
            "SQL Server replication lag — base64 PDF pasted in ticket",
            "DB replication delay with inline base64 PDF evidence",
            "SQL Server subscriber 4 hours behind — PDF data in message",
        ],
        descriptions=[
            "{name} ({department}): SQL Server replication is 4 hours "
            "behind on the subscriber. Attached the monitoring report "
            "below:\n\n"
            "JVBERi0xLjQKMSAwIG9iago8PAovVGl0bGUgKFJlcGxpY2F0aW9u"
            "IFJlcG9ydCkKL0F1dGhvciAoQ29udG9zbykKPj4KZW5kb2JqCjIg"
            "...[ 80KB of base64-encoded PDF data ]...\n\n"
            "The subscriber database is falling further behind every "
            "hour. Production reads are serving stale data.",
            "SQL Server transactional replication subscriber is 4+ "
            "hours behind the publisher. {name} ({department}) pasted "
            "an 80KB base64-encoded PDF monitoring report directly "
            "into the ticket. The actual issue: production reads from "
            "the subscriber are serving stale data and the lag is "
            "growing.",
        ],
        next_best_actions=[
            "URGENT: SQL Server replication subscriber is 4 hours "
            "behind and growing. Production reads are returning stale "
            "data. Immediate investigation needed.",
            "Investigate SQL Server replication lag on the subscriber "
            "database. Check distribution agent status, pending "
            "commands, and network throughput between publisher and "
            "subscriber.",
        ],
        remediation_steps=[
            [
                "Check the SQL Server Replication Monitor for distribution agent errors",
                "Verify pending commands in the distribution database",
                "Restart the distribution agent and monitor catch-up progress",
                "Investigate long-running transactions on the publisher blocking replication",
            ],
        ],
    )
)


# ---------------------------------------------------------------------------
# dc-205  ICS/vCalendar metadata mixed in — conference room booking down
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="dc-205",
        category=Category.SOFTWARE,
        priority=Priority.P2,
        assigned_team=Team.ENTERPRISE_APPS,
        needs_escalation=False,
        missing_information=[MissingInfo.AFFECTED_SYSTEM, MissingInfo.AFFECTED_USERS],
        subjects=[
            "Conference room booking system down — ICS data in ticket",
            "Room booking broken — vCalendar metadata mixed in message",
            "Cannot book meeting rooms — ICS/vCalendar noise in request",
        ],
        descriptions=[
            "BEGIN:VCALENDAR\nVERSION:2.0\nPRODID:-//Contoso//"
            "RoomBooking//EN\nBEGIN:VEVENT\nDTSTART:20250115T090000Z"
            "\nDTEND:20250115T100000Z\nSUMMARY:Q1 Planning\n"
            "LOCATION:Conf Room 14B\nORGANIZER:mailto:{name}@contoso"
            ".com\nEND:VEVENT\nEND:VCALENDAR\n\n"
            "{name} ({department}): The conference room booking system "
            "has been down since this morning. None of us can reserve "
            "any rooms. We have critical meetings today.",
            "Conference room booking system is down — no rooms can be "
            "reserved. {name} ({department}) submitted the ticket with "
            "ICS/vCalendar metadata (VCALENDAR, VEVENT blocks) "
            "prepended to the actual request. The system has been "
            "non-functional since the morning with critical meetings "
            "at risk.",
        ],
        next_best_actions=[
            "Investigate the conference room booking system outage. "
            "No rooms can be reserved. {name} reports critical "
            "meetings are affected. Ignore the ICS metadata noise.",
            "Check the room booking backend service and Exchange "
            "resource mailbox health. The entire booking system is "
            "non-functional since this morning.",
        ],
        remediation_steps=[
            [
                "Check the room booking application service health and logs",
                "Verify Exchange resource mailboxes for conference rooms are responsive",
                "Restart the room booking service and test a reservation",
                "Communicate status to affected users with critical meetings",
            ],
        ],
    )
)


# ---------------------------------------------------------------------------
# dc-206  8K+ verbose description, issue in one sentence — BitLocker recovery key
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="dc-206",
        category=Category.SECURITY,
        priority=Priority.P1,
        assigned_team=Team.SECOPS,
        needs_escalation=False,
        missing_information=[MissingInfo.DEVICE_INFO, MissingInfo.AUTHENTICATION_METHOD],
        subjects=[
            "BitLocker recovery key needed — extremely verbose ticket",
            "Locked out by BitLocker — 8K description with one-line issue",
            "BitLocker recovery request buried in lengthy narrative",
        ],
        descriptions=[
            "{name} from {department}: I want to start by explaining "
            "the full context of my day. I arrived at the office at "
            "7:45am and parked in lot B. After getting coffee from the "
            "3rd floor kitchen I went to my desk and opened my laptop. "
            "... [8000+ characters of detailed narrative about the "
            "user's morning routine, the weather, conversations with "
            "colleagues, and observations about the office] ... "
            "Anyway, my laptop is showing a BitLocker recovery screen "
            "and I need the recovery key to unlock it. My device name "
            "is YOURPC-{name}.",
            "BitLocker recovery key needed for {name} ({department}). "
            "The ticket is 8000+ characters of narrative about the "
            "user's morning, but the actual request is one sentence: "
            "laptop shows BitLocker recovery screen, needs recovery "
            "key. Device name: YOURPC-{name}.",
        ],
        next_best_actions=[
            "Retrieve the BitLocker recovery key for device "
            "YOURPC-{name}. The user is locked out at the BitLocker "
            "recovery screen. Verify identity before providing the key.",
            "Look up the BitLocker recovery key in Azure AD/Intune "
            "for the user's device and provide it after identity "
            "verification.",
        ],
        remediation_steps=[
            [
                "Verify the user's identity through standard authentication",
                "Retrieve the BitLocker recovery key from Azure AD or MBAM",
                "Provide the recovery key and confirm the device boots successfully",
                "Investigate why BitLocker recovery was triggered (TPM change, update, etc.)",
            ],
        ],
    )
)


# ---------------------------------------------------------------------------
# dc-207  NDR bounce-back wrapper — unable to send to external domain
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="dc-207",
        category=Category.NETWORK,
        priority=Priority.P2,
        assigned_team=Team.NETWORK,
        needs_escalation=False,
        missing_information=[MissingInfo.ERROR_MESSAGE, MissingInfo.AFFECTED_SYSTEM],
        subjects=[
            "Unable to send email externally — NDR bounce-back in ticket",
            "Email delivery failure to external domain — NDR wrapper",
            "Bounce-back NDR wrapped around original send failure",
        ],
        descriptions=[
            "Delivery has failed to these recipients or groups:\n\n"
            "partner@externalcorp.com\n\n"
            "Your message wasn't delivered because the destination "
            "server returned: 550 5.7.1 Unable to relay.\n\n"
            "Diagnostic information for administrators:\n"
            "Generating server: MAILGW-03.contoso.com\n"
            "Remote server: smtp.externalcorp.com\n"
            "#550 5.7.1 <partner@externalcorp.com>: Relay access "
            "denied ##\n\n"
            "--- Original message from {name} ({department}) ---\n"
            "Hi, please see the attached contract for review. "
            "Thanks, {name}",
            "{name} ({department}) cannot send email to external "
            "domain externalcorp.com. The ticket is an NDR bounce-back "
            "wrapper showing 550 5.7.1 relay access denied from "
            "MAILGW-03. The user's original message was a routine "
            "business email to a partner.",
        ],
        next_best_actions=[
            "Investigate the 550 5.7.1 relay access denied error on "
            "MAILGW-03 when sending to externalcorp.com. This may be "
            "a connector or relay configuration issue.",
            "Check the Exchange Send Connector and SMTP relay "
            "configuration on MAILGW-03. External email to at least "
            "one domain is failing with relay denied.",
        ],
        remediation_steps=[
            [
                "Check MAILGW-03 Send Connector configuration for external relay",
                "Verify DNS MX records and SPF/DKIM for the external domain",
                "Test SMTP connectivity from MAILGW-03 to smtp.externalcorp.com",
                "Review firewall rules for outbound SMTP (port 25/587) from MAILGW-03",
            ],
        ],
    )
)


# ---------------------------------------------------------------------------
# dc-208  Code snippets inline — scheduled task failing
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="dc-208",
        category=Category.SOFTWARE,
        priority=Priority.P2,
        assigned_team=Team.ENTERPRISE_APPS,
        needs_escalation=False,
        missing_information=[MissingInfo.ENVIRONMENT_DETAILS, MissingInfo.CONFIGURATION_DETAILS],
        subjects=[
            "Scheduled task failing — PowerShell/Python/SQL code inline",
            "Automated job broken — multiple code snippets in ticket",
            "Task Scheduler failure with inline code samples",
        ],
        descriptions=[
            "{name} ({department}): Our nightly data sync task is "
            "failing. Here are the scripts involved:\n\n"
            "PowerShell launcher:\n"
            "```powershell\n"
            "$conn = New-Object System.Data.SqlClient.SqlConnection\n"
            "$conn.ConnectionString = \"Server=SQLPROD-01;Database="
            "ContosoSync;Integrated Security=true\"\n"
            "$conn.Open()\n"
            "```\n\n"
            "Python ETL:\n"
            "```python\n"
            "import pandas as pd\n"
            "df = pd.read_sql(query, engine)\n"
            "df.to_csv('//fileshare/exports/daily.csv')\n"
            "```\n\n"
            "SQL query:\n"
            "```sql\n"
            "SELECT * FROM SyncLog WHERE Status = 'Failed' "
            "ORDER BY Timestamp DESC\n"
            "```\n\n"
            "The task last ran successfully 3 days ago. Now it fails "
            "with exit code 1.",
            "Nightly data sync scheduled task is failing with exit "
            "code 1 for {name} ({department}). The ticket includes "
            "PowerShell, Python, and SQL code snippets. The task "
            "worked 3 days ago — something changed. Pipeline: "
            "PowerShell connects to SQLPROD-01, Python ETL exports "
            "to a file share.",
        ],
        next_best_actions=[
            "Investigate the nightly data sync task failure (exit "
            "code 1). The pipeline involves PowerShell, Python ETL, "
            "and SQL on SQLPROD-01. Last success was 3 days ago.",
            "Check Task Scheduler history and the sync scripts for "
            "errors. Verify connectivity to SQLPROD-01 and the "
            "file share used for CSV exports.",
        ],
        remediation_steps=[
            [
                "Check Task Scheduler history for the specific error details",
                "Verify SQL Server connectivity from the task runner to SQLPROD-01",
                "Test the file share path (//fileshare/exports/) for write access",
                "Run the PowerShell launcher manually to reproduce and diagnose the failure",
            ],
        ],
    )
)


# ---------------------------------------------------------------------------
# dc-209  Contradictory thread — AP dropping connections
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="dc-209",
        category=Category.NETWORK,
        priority=Priority.P2,
        assigned_team=Team.NETWORK,
        needs_escalation=False,
        missing_information=[MissingInfo.NETWORK_LOCATION, MissingInfo.REPRODUCTION_FREQUENCY],
        subjects=[
            "Access point dropping connections — contradictory thread",
            "Wi-Fi AP issue — fixed/not-fixed back and forth in thread",
            "Contradictory email chain — AP-14B intermittent disconnects",
        ],
        descriptions=[
            "{name} ({department}):\n\n"
            "[Jan 10] Original: AP-14B keeps dropping connections "
            "every 30 minutes.\n"
            "[Jan 11] Update: Seems fixed after rebooting the AP.\n"
            "[Jan 12] Update: Not fixed. Still dropping.\n"
            "[Jan 13] Update: IT replaced the AP, working now.\n"
            "[Jan 14] Update: Dropping again on the new AP too.\n"
            "[Jan 15] Update: Switching to Ethernet fixed it. "
            "Closing.\n"
            "[Jan 16] Update: Reopening — I need Wi-Fi for meeting "
            "rooms. AP-14B and AP-14C both dropping now.\n\n"
            "Current status: NOT resolved. Two APs affected.",
            "Access points AP-14B and AP-14C are intermittently "
            "dropping connections. {name} ({department}) submitted a "
            "contradictory thread that was marked fixed, reopened, "
            "fixed again, and reopened again over a week. Current "
            "status: unresolved, two APs affected, drops every "
            "~30 minutes.",
        ],
        next_best_actions=[
            "Investigate recurring Wi-Fi drops on AP-14B and AP-14C. "
            "Previous fixes (reboot, replacement) did not resolve the "
            "issue. This may be an infrastructure or interference "
            "problem rather than a single-AP failure.",
            "Perform a wireless site survey around AP-14B and AP-14C "
            "to check for interference, channel congestion, or "
            "controller misconfiguration causing repeated drops.",
        ],
        remediation_steps=[
            [
                "Check the wireless controller for AP-14B and AP-14C error logs",
                "Run a wireless site survey to identify interference sources",
                "Verify channel assignments and power levels on both APs",
                "Update AP firmware and controller configuration as needed",
            ],
        ],
    )
)


# ---------------------------------------------------------------------------
# dc-210  Accidental PII in description — payroll calculation error
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="dc-210",
        category=Category.DATA,
        priority=Priority.P2,
        assigned_team=Team.DATA_PLATFORM,
        needs_escalation=True,
        missing_information=[MissingInfo.AFFECTED_USERS, MissingInfo.BUSINESS_IMPACT],
        subjects=[
            "Payroll calculation error — accidental PII in ticket",
            "Incorrect paycheck — ticket contains fake SSN and CC number",
            "Payroll discrepancy with sensitive data in description",
        ],
        descriptions=[
            "{name} ({department}): My paycheck this month is wrong — "
            "I was underpaid by $847.50. For reference, my details: "
            "SSN 078-05-1120, employee ID E-44821, bank account ending "
            "in 6743, credit card 4111-1111-1111-1111. My manager is "
            "also affected, their SSN is 219-09-9999. Please correct "
            "the calculation immediately. This is the second month in "
            "a row.",
            "Payroll calculation error for {name} ({department}) — "
            "underpaid by $847.50 for the second consecutive month. "
            "WARNING: The ticket contains accidental PII including "
            "SSNs and a credit card number that must be redacted "
            "immediately. The actual issue: payroll system is "
            "miscalculating this employee's pay.",
        ],
        next_best_actions=[
            "URGENT: Redact the PII (SSNs, CC number) from this "
            "ticket immediately. Then investigate the payroll "
            "calculation error — {name} has been underpaid $847.50 "
            "for two consecutive months.",
            "Flag this ticket for PII redaction per data handling "
            "policy. After redaction, route the payroll discrepancy "
            "to the payroll team for correction.",
        ],
        remediation_steps=[
            [
                "Immediately redact all PII (SSNs, credit card numbers) from the ticket",
                "Log a data handling incident per organizational PII exposure policy",
                "Investigate the payroll calculation error for the affected employee",
                "Coordinate with payroll to issue a correction for the underpayment",
            ],
        ],
    )
)