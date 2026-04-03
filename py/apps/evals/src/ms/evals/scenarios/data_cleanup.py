# Copyright (c) Microsoft. All rights reserved.
"""Data cleanup edge-case scenario templates.

Covers: long email threads, base64-encoded images, HTML-heavy emails,
garbled encoding, emoji-heavy chat, repeated content, excessive signatures,
mixed languages, truncated messages, log dumps, HTML entities, and
duplicate/stuttering content.
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
            "internal wiki at <a href=\"https://contoso.sharepoint.com/sites/ITWiki\">"
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
            "Investigate printer producing garbled output — likely a corrupt print driver "
            "or PCL/PostScript mismatch.",
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
            "Investigate Slack-Jira integration returning 502 errors — blocking incident "
            "tracking workflow.",
            "Diagnose integration connector failure returning 502 — check OAuth tokens "
            "and webhook configuration.",
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
            "Investigate application crash caused by a specific input — review crash dumps "
            "and test in safe mode.",
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
            "Investigate physical access card failure — check if badge was deactivated, "
            "expired, or flagged.",
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
            "El error que aparece es: \"Gateway timed out. Please try reconnecting.\"\n"
            "The error that shows is: \"Gateway timed out. Please try reconnecting.\"\n\n"
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
            "Restore connectivity to integration test database — CI/CD pipeline blocked "
            "since 06:15 AM.",
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
            "Troubleshoot phone call routing — incoming calls going directly to voicemail "
            "despite available status.",
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
