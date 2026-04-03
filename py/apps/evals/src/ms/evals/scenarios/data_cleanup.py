# Copyright (c) Microsoft. All rights reserved.
"""Data cleanup edge-case scenario templates.

Covers: long email threads, base64-encoded images, HTML-heavy emails,
garbled encoding, emoji-heavy chat, repeated content, excessive signatures,
mixed languages, truncated messages, log dumps, HTML entities,
duplicate/stuttering content, extremely verbose single emails, URL-heavy tickets,
JSON/XML data dumps, Windows Event Log entries, SMTP header dumps,
auto-generated notification noise, excessive whitespace, OCR artifacts,
pasted tabular data, phone transcript filler, multi-forward signature chains,
markdown formatting artifacts, large stack traces, and invisible Unicode.
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
            "Urgently resolve vendor API auth failure — 4,200 trades pending "
            "settlement submission.",
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
            "Troubleshoot Exchange ActiveSync failure — phone hasn't synced in 2 days "
            "with 47 consecutive errors.",
            "Resolve Intune-managed Teams update failure — access denied error after "
            "3 retry attempts.",
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
            "Investigate recurring wireless drops — check WiFi adapter driver "
            "and power management settings.",
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
            "Investigate SSO authentication failure — user may have expired password "
            "or stale MFA registration.",
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
