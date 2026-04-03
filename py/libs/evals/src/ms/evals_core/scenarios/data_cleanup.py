"""Data cleanup edge-case scenarios for the Contoso Financial Services eval suite.

These scenarios stress-test the triage model's ability to extract the real
support issue from noisy, malformed, or excessively verbose input.
"""

from ms.evals_core.constants import Category
from ms.evals_core.constants import Channel
from ms.evals_core.constants import MissingInfo
from ms.evals_core.constants import Priority
from ms.evals_core.constants import Team
from ms.evals_core.scenarios.base import ScenarioDefinition


def get_scenarios() -> list[ScenarioDefinition]:
    """Return all Data Cleanup evaluation scenarios."""
    return [
        # ── DC-001  Long email thread with deeply nested quoted replies ──
        ScenarioDefinition(
            scenario_id="DC-001",
            subject="Re: Re: Re: Re: Re: FW: VPN disconnects during market open",
            description=(
                "Hi IT Support,\n\n"
                "Just following up again — the VPN still drops every morning between 09:28 and 09:32 ET.\n"
                "I have to reconnect 3-4 times before it stabilizes. This is impacting my ability to\n"
                "execute trades at market open.\n\n"
                "Thanks,\nMarco\n\n"
                "--- Original Message ---\n"
                "From: Marco Bellini <marco.bellini@contoso.com>\n"
                "Sent: Monday, March 10, 2026 8:45 AM\n"
                "To: IT Support <itsupport@contoso.com>\n"
                "Subject: Re: Re: Re: Re: FW: VPN disconnects during market open\n\n"
                "Still happening today. I ran the diagnostics you asked for — attached.\n\n"
                "--- Original Message ---\n"
                "From: IT Support <itsupport@contoso.com>\n"
                "Sent: Friday, March 7, 2026 4:10 PM\n"
                "To: Marco Bellini <marco.bellini@contoso.com>\n"
                "Subject: Re: Re: Re: FW: VPN disconnects during market open\n\n"
                "Hi Marco, could you run 'netsh wlan show all' and send us the output? Also please\n"
                "confirm your GlobalProtect client version. Thanks, Amy\n\n"
                "--- Original Message ---\n"
                "From: Marco Bellini <marco.bellini@contoso.com>\n"
                "Sent: Friday, March 7, 2026 9:05 AM\n"
                "To: IT Support <itsupport@contoso.com>\n"
                "Subject: Re: Re: FW: VPN disconnects during market open\n\n"
                "It happened again. I lost the VPN tunnel at exactly 09:30. My colleague Raj in the\n"
                "same building says his works fine, so I don't think it's the office network.\n\n"
                "--- Original Message ---\n"
                "From: IT Support <itsupport@contoso.com>\n"
                "Sent: Thursday, March 6, 2026 3:00 PM\n"
                "To: Marco Bellini <marco.bellini@contoso.com>\n"
                "Subject: Re: FW: VPN disconnects during market open\n\n"
                "Hi Marco, thanks for reporting. Can you tell us which office and floor you're on?\n"
                "Also, are you on Wi-Fi or Ethernet? Regards, Amy\n\n"
                "--- Original Message ---\n"
                "From: Marco Bellini <marco.bellini@contoso.com>\n"
                "Sent: Thursday, March 6, 2026 9:35 AM\n"
                "To: IT Support <itsupport@contoso.com>\n"
                "Subject: FW: VPN disconnects during market open\n\n"
                "Hi team, my VPN keeps disconnecting every morning around market open. I'm on the\n"
                "5th floor, Building 3, New York office, using Wi-Fi. It's been going on for a week."
            ),
            category=Category.NETWORK,
            priority=Priority.P2,
            team=Team.NETWORK_OPS,
            needs_escalation=False,
            missing_info=[MissingInfo.APPLICATION_VERSION],
            next_best_action=(
                "Investigate recurring VPN tunnel drops correlated with 09:30 ET market-open "
                "traffic spike for user on 5th floor Wi-Fi, Building 3 NYC."
            ),
            remediation_steps=[
                "Check GlobalProtect VPN gateway logs for Marco's session drops between 09:25-09:35 ET.",
                "Correlate with wireless controller data for Building 3, 5th floor AP utilization.",
                "Verify VPN split-tunnel configuration and MTU settings on the client.",
                "If Wi-Fi congestion confirmed, consider moving user to Ethernet or a less congested AP.",
                "Provide user with updated GlobalProtect client if version is outdated.",
            ],
            reporter_name="Marco Bellini",
            reporter_email="marco.bellini@contoso.com",
            reporter_department="Equity Trading",
            channel=Channel.EMAIL,
            tags=["data-cleanup", "long-email", "quoted-replies"],
            difficulty="hard",
        ),
        # ── DC-002  Inline base64-encoded image data ──────────────────────
        ScenarioDefinition(
            scenario_id="DC-002",
            subject="Monitor flickering — screenshot attached inline",
            description=(
                "Hi,\n\n"
                "My external monitor keeps flickering every few seconds. I took a screenshot but our\n"
                "mail client embedded it inline. Here it is:\n\n"
                "[image: screenshot.png]\n"
                "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR4"
                "2mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg==\n"
                "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAKCAYAAACNMs+9AAAAFUlEQVQYV2"
                "P8z8BQz0AEYBxVOHIVAvcHBQHzKSECAAAAAElFTkSuQmCC\n"
                "data:image/png;base64,/9j/4AAQSkZJRgABAQEASABIAAD/2wBDAAgGBgcGBQgHBwcJCQgKDBQNDA"
                "sLDBkSEw8UHRofHh0aHBwgJC4nICIsIxwcKDcpLDAxNDQ0Hyc5PTgyPC4zNDL/2wBDAQkJCQwLDBgN"
                "DRgyIRwhMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjL/"
                "wAARCAABAAEDASIAAhEBAxEB/8QAHwAAAQUBAQEBAQEAAAAAAAAAAAECAwQFBgcICQoL/8QAFBABaaaa"
                "AAAAAAAAAAAAAAAAAAAAAP/EABQRAQAAAAAAAAAAAAAAAAAAAAD/2gAMAwEAAhEDEQA/ALQAB//Z\n\n"
                "The flickering started Monday after a Windows Update. It's a Dell U2722D connected\n"
                "via DisplayPort to my docking station (Dell WD19S). The built-in laptop screen is\n"
                "fine. I've tried a different DisplayPort cable already — same issue.\n\n"
                "Priya Nair\n"
                "Risk Management, Building 2, 7th floor"
            ),
            category=Category.HARDWARE,
            priority=Priority.P3,
            team=Team.ENDPOINT,
            needs_escalation=False,
            missing_info=[MissingInfo.DEVICE_INFO],
            next_best_action=(
                "Troubleshoot Dell U2722D monitor flickering after Windows Update — "
                "likely a display driver regression via WD19S dock."
            ),
            remediation_steps=[
                "Roll back the most recent Intel/NVIDIA display driver update from Windows Update.",
                "Check Dell WD19S firmware version and update if behind current release.",
                "Test monitor on a different docking station to isolate dock vs. driver issue.",
                "If driver rollback resolves, add the driver to the WSUS deferral list.",
            ],
            reporter_name="Priya Nair",
            reporter_email="priya.nair@contoso.com",
            reporter_department="Risk Management",
            channel=Channel.EMAIL,
            tags=["data-cleanup", "base64", "inline-image"],
            difficulty="hard",
        ),
        # ── DC-003  HTML-heavy email with tags, styles, entities ──────────
        ScenarioDefinition(
            scenario_id="DC-003",
            subject="Cannot access SharePoint after migration",
            description=(
                '<html><body style="font-family:Calibri,sans-serif;font-size:11pt">'
                '<div style="margin:0;padding:0">'
                "<p><b>Hi IT Team,</b></p>"
                '<p style="color:#1F4E79">Since the SharePoint migration last Friday I can'
                "&rsquo;t open the <b>Compliance Policy Library</b> site. I get a "
                "&ldquo;403 Forbidden&rdquo; error every time I click the link.</p>"
                "<p>Steps I&apos;ve tried:</p>"
                "<ol>"
                "<li>Cleared browser cache &amp; cookies</li>"
                "<li>Tried Edge, Chrome, and Firefox &mdash; same result</li>"
                "<li>Verified my account at <u>myaccount.microsoft.com</u> &mdash; looks fine</li>"
                "<li>Asked my manager Deirdre who can access it fine from her machine</li>"
                "</ol>"
                '<p>My URL is: <a href="https://contoso.sharepoint.com/sites/CompliancePolicyLib">'
                "https://contoso.sharepoint.com/sites/CompliancePolicyLib</a></p>"
                '<p style="font-size:9pt;color:gray">Sent from Outlook for Windows</p>'
                '<p style="font-size:8pt;color:gray">CONFIDENTIALITY NOTICE: This email and any '
                "attachments are for the exclusive and confidential use of the intended recipient. "
                "If you are not the intended recipient, please do not read, distribute, or take "
                "action based on this message.&nbsp;&nbsp;</p>"
                "</div></body></html>"
            ),
            category=Category.ACCESS_AUTH,
            priority=Priority.P2,
            team=Team.IAM,
            needs_escalation=False,
            missing_info=[MissingInfo.ERROR_MESSAGE],
            next_best_action=(
                "Investigate 403 Forbidden on SharePoint Compliance Policy Library for user — "
                "likely a permission mapping gap from Friday's migration."
            ),
            remediation_steps=[
                "Check SharePoint admin center for the Compliance Policy Library site permissions.",
                "Verify user's Azure AD group memberships against the migrated site's access list.",
                "Re-grant access to the site collection if permissions were lost during migration.",
                "Confirm user can access the site after permission fix and clear any cached 403.",
            ],
            reporter_name="Aiden O'Sullivan",
            reporter_email="aiden.osullivan@contoso.com",
            reporter_department="Compliance",
            channel=Channel.EMAIL,
            tags=["data-cleanup", "html-heavy", "entities"],
            difficulty="hard",
        ),
        # ── DC-004  Garbled / encoding-corrupted text ─────────────────────
        ScenarioDefinition(
            scenario_id="DC-004",
            subject="Printer producing garbled output — urg\u00ebnt",
            description=(
                "Hi,\n\n"
                "The printer on the 3rd floor (HP LaserJet MFP M634) is printing garbled\n"
                "characters on every document. Here\u2019s what the output looks like:\n\n"
                "\u00c3\u00a9\u00c3\u00b1\u00c3\u00bc\u00c3\u00a8\u00c2\u00ab\u00c2\u00bb "
                "\u00ef\u00bf\u00bd\u00ef\u00bf\u00bd\u00ef\u00bf\u00bd "
                "R\u00c3\u00a9port_Q1_2026.xlsx \u00e2\u0080\u0093 Page 1 of 4\n"
                "\u00c3\u0081\u00c3\u00a7\u00c3\u00a7\u00c3\u00a8\u00c3\u0178\u00c3\u0178 "
                "D\u00c3\u00a8ni\u00c3\u00a8d: Pl\u00c3\u00a8\u00c3\u00a0s\u00c3\u00a8 "
                "cont\u00c3\u00a0ct IT\n\n"
                "I\u2019ve tried restarting the printer and switching paper trays. My colleague\n"
                "Fatima confirmed it\u2019s happening for her documents too. We need this fixed\n"
                "today \u2014 we have a board presentation to print.\n\n"
                "Regards,\n"
                "Wei Chen\n"
                "Finance, Building 1, 3rd floor, New York"
            ),
            category=Category.HARDWARE,
            priority=Priority.P2,
            team=Team.ENDPOINT,
            needs_escalation=False,
            missing_info=[MissingInfo.ERROR_MESSAGE],
            next_best_action=(
                "Investigate HP LaserJet MFP M634 on 3rd floor producing garbled output — "
                "likely a corrupt print driver or PCL/PostScript mismatch."
            ),
            remediation_steps=[
                "Check the print server for driver version and compare against HP's latest release.",
                "Reinstall or update the printer driver on the print server.",
                "Verify PCL vs PostScript language setting matches the printer's configuration.",
                "Print a test page from the server to confirm the fix before notifying the user.",
            ],
            reporter_name="Wei Chen",
            reporter_email="wei.chen@contoso.com",
            reporter_department="Finance",
            channel=Channel.EMAIL,
            tags=["data-cleanup", "garbled-text", "encoding"],
            difficulty="hard",
        ),
        # ── DC-005  Emoji-heavy chat message ──────────────────────────────
        ScenarioDefinition(
            scenario_id="DC-005",
            subject="Slack integration broken \U0001f6a8\U0001f6a8\U0001f6a8",
            description=(
                "\U0001f6a8\U0001f6a8\U0001f6a8 URGENT \U0001f6a8\U0001f6a8\U0001f6a8\n\n"
                "Heyy so the Slack \u2194\ufe0f Jira integration is totally broken \U0001f62d"
                "\U0001f62d\U0001f62d\n"
                "When I create a ticket in #trading-incidents it used to auto-create a Jira "
                "issue \U0001f4cb but now NOTHING happens \u274c\u274c\n\n"
                "I\u2019ve checked:\n"
                "\u2705 Slack app is still installed in our workspace\n"
                "\u2705 I can see the Jira bot in the channel\n"
                "\u274c But the /jira create command gives me \U0001f449 "
                '"Oops! Something went wrong (error 502)" \U0001f448\n\n'
                "This is blocking our whole incident workflow \U0001f525\U0001f525\U0001f525 "
                "we literally cannot track prod issues rn \U0001f4a9\n\n"
                "pls help asap \U0001f64f\U0001f64f\U0001f64f\n\n"
                "\u2014 Deshawn\n"
                "\U0001f4bc Institutional Trading\n"
                "\U0001f4cd NYC Building 4, 8th floor"
            ),
            category=Category.SOFTWARE,
            priority=Priority.P2,
            team=Team.ENTERPRISE_APPS,
            needs_escalation=True,
            missing_info=[MissingInfo.TIMESTAMP, MissingInfo.ERROR_MESSAGE],
            next_best_action=(
                "Investigate Slack-Jira integration returning 502 errors in #trading-incidents — "
                "blocking incident tracking workflow for Institutional Trading."
            ),
            remediation_steps=[
                "Check the Jira Cloud status page and Slack API status for ongoing incidents.",
                "Verify the Jira for Slack app OAuth tokens have not expired or been revoked.",
                "Review Jira webhook logs for 502 errors and identify the failing endpoint.",
                "If the integration app needs reauthorization, walk the channel admin through it.",
                "Test /jira create from the channel to confirm resolution.",
            ],
            reporter_name="Deshawn Carter",
            reporter_email="deshawn.carter@contoso.com",
            reporter_department="Institutional Trading",
            channel=Channel.CHAT,
            tags=["data-cleanup", "emoji-heavy", "chat"],
            difficulty="hard",
        ),
        # ── DC-006  Excessive repeated content / copy-paste loops ─────────
        ScenarioDefinition(
            scenario_id="DC-006",
            subject="Outlook keeps crashing — error details inside",
            description=(
                "Outlook crashes every time I open a specific email from the Legal team.\n\n"
                "Here's the error from Event Viewer (it repeated many times):\n\n"
                "Faulting application name: OUTLOOK.EXE, version: 16.0.18227.20162\n"
                "Faulting module name: mso40uiwin32client.dll, version: 16.0.18227.20162\n"
                "Exception code: 0xc0000005\n"
                "Fault offset: 0x00000000005a3b10\n"
                "Faulting application name: OUTLOOK.EXE, version: 16.0.18227.20162\n"
                "Faulting module name: mso40uiwin32client.dll, version: 16.0.18227.20162\n"
                "Exception code: 0xc0000005\n"
                "Fault offset: 0x00000000005a3b10\n"
                "Faulting application name: OUTLOOK.EXE, version: 16.0.18227.20162\n"
                "Faulting module name: mso40uiwin32client.dll, version: 16.0.18227.20162\n"
                "Exception code: 0xc0000005\n"
                "Fault offset: 0x00000000005a3b10\n"
                "Faulting application name: OUTLOOK.EXE, version: 16.0.18227.20162\n"
                "Faulting module name: mso40uiwin32client.dll, version: 16.0.18227.20162\n"
                "Exception code: 0xc0000005\n"
                "Fault offset: 0x00000000005a3b10\n"
                "Faulting application name: OUTLOOK.EXE, version: 16.0.18227.20162\n"
                "Faulting module name: mso40uiwin32client.dll, version: 16.0.18227.20162\n"
                "Exception code: 0xc0000005\n"
                "Fault offset: 0x00000000005a3b10\n\n"
                "This is the only email that causes it. All other emails open fine.\n"
                "I'm on Windows 11 with Microsoft 365 Apps, Current Channel.\n\n"
                "Nadia Al-Rashid\nLegal, Building 2, 4th floor, New York"
            ),
            category=Category.SOFTWARE,
            priority=Priority.P3,
            team=Team.ENTERPRISE_APPS,
            needs_escalation=False,
            missing_info=[MissingInfo.STEPS_TO_REPRODUCE],
            next_best_action=(
                "Diagnose Outlook crash (0xc0000005 in mso40uiwin32client.dll) triggered "
                "by a specific email — likely a corrupted message or embedded object."
            ),
            remediation_steps=[
                "Identify the specific email causing the crash from the user's mailbox.",
                "Attempt to open the email in Outlook Web App to confirm it is message-specific.",
                "Run Outlook in safe mode to rule out add-in conflicts.",
                "If OWA works, repair the Office installation or update to the latest build.",
                "If the email is corrupted, remove it via MFCMAPI or an admin mailbox tool.",
            ],
            reporter_name="Nadia Al-Rashid",
            reporter_email="nadia.al-rashid@contoso.com",
            reporter_department="Legal",
            channel=Channel.PORTAL,
            tags=["data-cleanup", "repeated-content", "crash-log"],
            difficulty="hard",
        ),
        # ── DC-007  Excessive email signature / legal disclaimer ──────────
        ScenarioDefinition(
            scenario_id="DC-007",
            subject="Badge not working at Building 6 turnstile",
            description=(
                "My badge stopped working at the Building 6 main entrance turnstile this morning. "
                "I had to be let in by security. Can you please reactivate it?\n\n"
                "Thanks,\n"
                "Jonathan Pretorius\n"
                "Vice President, Corporate Strategy\n"
                "Contoso Financial Services\n"
                "1 World Financial Center, 42nd Floor\n"
                "New York, NY 10281\n"
                "Tel: +1 (212) 555-0142 | Mobile: +1 (917) 555-0198\n"
                "Fax: +1 (212) 555-0199\n"
                "Email: jonathan.pretorius@contoso.com\n"
                "LinkedIn: linkedin.com/in/jonathanpretorius\n\n"
                "====================================================================\n"
                "CONFIDENTIALITY NOTICE: This email message, including any attachments,\n"
                "is for the sole use of the intended recipient(s) and may contain\n"
                "confidential and privileged information. Any unauthorized review, use,\n"
                "disclosure, or distribution is prohibited. If you are not the intended\n"
                "recipient, please contact the sender by reply email and destroy all\n"
                "copies of the original message. Receipt by anyone other than the\n"
                "intended recipient(s) is not a waiver of any attorney-client,\n"
                "work product, or other applicable privilege.\n\n"
                "ENVIRONMENTAL NOTICE: Please consider the environment before printing\n"
                "this email. Contoso Financial Services is committed to sustainable\n"
                "business practices.\n\n"
                "IRS CIRCULAR 230 DISCLOSURE: To ensure compliance with requirements\n"
                "imposed by the IRS, we inform you that any U.S. federal tax advice\n"
                "contained in this communication (including any attachments) is not\n"
                "intended or written to be used, and cannot be used, for the purpose\n"
                "of (i) avoiding penalties under the Internal Revenue Code or (ii)\n"
                "promoting, marketing, or recommending to another party any transaction\n"
                "or matter addressed herein.\n"
                "===================================================================="
            ),
            category=Category.ACCESS_AUTH,
            priority=Priority.P3,
            team=Team.IAM,
            needs_escalation=False,
            missing_info=[MissingInfo.DEVICE_INFO],
            next_best_action=(
                "Reactivate or replace badge for user unable to enter Building 6 main entrance turnstile."
            ),
            remediation_steps=[
                "Look up the user's badge ID in the physical access control system.",
                "Check if the badge was deactivated, expired, or flagged for any reason.",
                "Reactivate the badge or issue a replacement if the physical card is damaged.",
                "Test badge at the Building 6 turnstile before confirming with the user.",
            ],
            reporter_name="Jonathan Pretorius",
            reporter_email="jonathan.pretorius@contoso.com",
            reporter_department="Corporate Strategy",
            channel=Channel.EMAIL,
            tags=["data-cleanup", "excessive-signature", "disclaimer"],
            difficulty="medium",
        ),
        # ── DC-008  Mixed languages (English + Mandarin + French) ─────────
        ScenarioDefinition(
            scenario_id="DC-008",
            subject="VDI session freezes / VDI\u4f1a\u8bdd\u51bb\u7ed3 / Session VDI gel\u00e9e",
            description=(
                "Hello IT,\n\n"
                "I work across the Singapore, New York, and London offices and my VDI session\n"
                "has been freezing intermittently.\n\n"
                "\u5f53\u6211\u8fde\u63a5\u5230\u65b0\u52a0\u5761\u6570\u636e\u4e2d\u5fc3"
                "\u7684VDI\u65f6\uff0c\u4f1a\u8bdd\u5728\u5927\u7ea6"
                "20\u5206\u949f\u540e\u51bb\u7ed3\u3002\u5c4f\u5e55\u505c\u6b62\u54cd\u5e94"
                "\uff0c\u6211\u5fc5\u987b\u65ad\u5f00\u5e76\u91cd\u65b0\u8fde\u63a5\u3002"
                "\u8fd9\u79cd\u60c5\u51b5\u6bcf\u5929\u53d1\u751f3-4\u6b21\u3002\n\n"
                "Quand je me connecte depuis le bureau de Londres, la session VDI g\u00e8le\n"
                "apr\u00e8s environ 20 minutes. L'\u00e9cran ne r\u00e9pond plus et je dois me\n"
                "d\u00e9connecter puis me reconnecter. Cela arrive 3 \u00e0 4 fois par jour.\n\n"
                "From New York the connection is stable. The issue only happens when I connect\n"
                "to the Singapore or London VDI pools. My laptop is a ThinkPad X1 Carbon Gen 11\n"
                "with VMware Horizon Client 2312.\n\n"
                "Xin Li (\u674e\u6b23)\n"
                "Quantitative Analysis\n"
                "Building 5, 9th floor, New York (home office)"
            ),
            category=Category.NETWORK,
            priority=Priority.P2,
            team=Team.NETWORK_OPS,
            needs_escalation=False,
            missing_info=[MissingInfo.NETWORK_LOCATION, MissingInfo.ENVIRONMENT_DETAILS],
            next_best_action=(
                "Investigate VDI session freezes when user connects to Singapore and London "
                "pools — likely WAN latency or VMware Horizon blast protocol issue."
            ),
            remediation_steps=[
                "Review VMware Horizon connection server logs for the user's sessions in SG and LDN.",
                "Measure round-trip latency and packet loss from the user's NYC location to SG/LDN.",
                "Check if the Blast Extreme protocol is tuned for high-latency WAN links.",
                "Consider enabling the Horizon Performance Tracker on the client for diagnostics.",
                "If WAN quality is the root cause, evaluate SD-WAN or dedicated VDI circuit options.",
            ],
            reporter_name="Xin Li",
            reporter_email="xin.li@contoso.com",
            reporter_department="Quantitative Analysis",
            channel=Channel.PORTAL,
            tags=["data-cleanup", "mixed-languages", "multilingual"],
            difficulty="hard",
        ),
        # ── DC-009  Truncated message (cut off mid-sentence) ──────────────
        ScenarioDefinition(
            scenario_id="DC-009",
            subject="Database replication lag causing stale portfolio data",
            description=(
                "Hi Data Platform team,\n\n"
                "We've noticed that the portfolio valuations dashboard is showing data that's\n"
                "approximately 45 minutes stale. The replication from the primary SQL Server\n"
                "(SQLPROD-NYC-01) to the read replica (SQLREPLICA-NYC-03) appears to be lagging.\n\n"
                "Impact: Portfolio managers are making decisions based on outdated valuations.\n"
                "This affects approximately 30 PMs across Wealth Management and Asset Management.\n\n"
                "What we've confirmed so far:\n"
                "- Primary database is current (checked via direct query at 14:22 ET)\n"
                "- Read replica is behind by ~2,700 transactions\n"
                "- The lag started around 13:35 ET today\n"
                "- No recent schema changes or maintenance windows\n"
                "- Disk I/O on the replica server looks elevated: avg write latency 48ms vs\n"
                "  normal 5ms\n\n"
                "We need this resolved urgently. The EOD NAV calculation process kicks off at\n"
                "16:00 ET and reads from the replica. If the lag isn't cleared by then, we'll\n"
                "have incorrect NAV calculations which will trigger regulatory reporting\n"
                "discrepancies and we'll need to file correc"
            ),
            category=Category.DATA_STORAGE,
            priority=Priority.P1,
            team=Team.DATA_PLATFORM,
            needs_escalation=True,
            missing_info=[MissingInfo.ENVIRONMENT_DETAILS],
            next_best_action=(
                "Urgently resolve SQL Server replication lag on SQLREPLICA-NYC-03 before "
                "16:00 ET EOD NAV calculation — 45-minute data staleness affecting 30 PMs."
            ),
            remediation_steps=[
                "Check disk subsystem on SQLREPLICA-NYC-03 for I/O bottleneck (48ms write latency).",
                "Review SQL Server replication monitor for error states or suspended subscriptions.",
                "If disk I/O is the bottleneck, identify competing workloads and throttle or stop them.",
                "Consider reinitializing replication from a snapshot if the lag cannot be recovered.",
                "Notify portfolio management leads of potential data staleness and EOD NAV risk.",
            ],
            reporter_name="Soren Andersen",
            reporter_email="soren.andersen@contoso.com",
            reporter_department="Data Engineering",
            channel=Channel.PORTAL,
            tags=["data-cleanup", "truncated-message", "database"],
            difficulty="hard",
        ),
        # ── DC-010  HTML entities and escaped characters throughout ────────
        ScenarioDefinition(
            scenario_id="DC-010",
            subject="Can&#39;t log in to trading platform &mdash; &quot;session expired&quot;",
            description=(
                "Every time I try to log in to the Contoso Trading Platform (CTP) I get the\n"
                "error: &quot;Your session has expired. Please contact your administrator.&quot;\n\n"
                "I&apos;ve tried:\n"
                "1. Clearing cookies &amp; cache\n"
                "2. Using incognito&#47;private mode\n"
                "3. Trying from a different machine\n"
                "4. Resetting my password via the &quot;Forgot Password&quot; link\n\n"
                "None of these work. I&apos;m getting the same error on both my laptop &amp;\n"
                "my desktop. My colleagues in the same team can log in fine.\n\n"
                "This started after the maintenance window last night (March 17 &ndash; 18).\n"
                "I&apos;m locked out of all my positions and can&apos;t execute trades.\n\n"
                "Kenji Watanabe &lt;kenji.watanabe@contoso.com&gt;\n"
                "Derivatives, Building 4, 6th floor\n"
                "Ext: 5&#45;4477"
            ),
            category=Category.ACCESS_AUTH,
            priority=Priority.P1,
            team=Team.IAM,
            needs_escalation=True,
            missing_info=[MissingInfo.AUTHENTICATION_METHOD],
            next_best_action=(
                "Restore CTP access for trader locked out after maintenance window — "
                "session token or account state likely not migrated correctly."
            ),
            remediation_steps=[
                "Check CTP identity provider logs for Kenji's failed authentication attempts.",
                "Verify the user's account was not disabled or locked during maintenance.",
                "Clear stale session tokens in the CTP session store for this user.",
                "If SAML/OIDC tokens were rotated during maintenance, ensure the user's IdP mapping is current.",
                "Confirm login works and monitor for recurrence over the next trading session.",
            ],
            reporter_name="Kenji Watanabe",
            reporter_email="kenji.watanabe@contoso.com",
            reporter_department="Derivatives",
            channel=Channel.PORTAL,
            tags=["data-cleanup", "html-entities", "escaped-chars"],
            difficulty="hard",
        ),
        # ── DC-011  Application log dump pasted into ticket ───────────────
        ScenarioDefinition(
            scenario_id="DC-011",
            subject="Jenkins build pipeline failing since this morning",
            description=(
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
                "[2026-03-18T06:17:16Z]     at TCPConnectWrap.afterConnect [as oncomplete]\n"
                "[2026-03-18T06:17:16Z] Tests: 0 passed, 18 failed, 18 total\n"
                "[2026-03-18T06:17:16Z] Pipeline FAILED at stage: Integration Tests\n"
                "[2026-03-18T06:17:17Z] Sending failure notification to #risk-engine-ci\n"
                "[2026-03-18T06:17:17Z] Pipeline duration: 2m 15s\n\n"
                "This has failed on every retry (5 times now). The test DB seems to be down.\n\n"
                "— Rafael Oliveira, Backend Engineering"
            ),
            category=Category.SOFTWARE,
            priority=Priority.P2,
            team=Team.ENTERPRISE_APPS,
            needs_escalation=False,
            missing_info=[],
            next_best_action=(
                "Restore connectivity to integration test database sqltest-nyc-02:1433 — "
                "CI/CD pipeline for risk-engine repo blocked since 06:15 AM."
            ),
            remediation_steps=[
                "Check if sqltest-nyc-02 SQL Server service is running and accepting connections.",
                "Verify network connectivity from the Jenkins agent to 10.42.8.15:1433.",
                "Check if there was a maintenance or patching event on sqltest-nyc-02 overnight.",
                "Restart the SQL Server service if it is stopped, and verify integration tests pass.",
                "Notify the Backend Engineering team once the pipeline is green.",
            ],
            reporter_name="Rafael Oliveira",
            reporter_email="rafael.oliveira@contoso.com",
            reporter_department="Backend Engineering",
            channel=Channel.CHAT,
            tags=["data-cleanup", "log-dump", "ci-cd"],
            difficulty="hard",
        ),
        # ── DC-012  Duplicate sentences and stuttering content ────────────
        ScenarioDefinition(
            scenario_id="DC-012",
            subject="Zoom phone not ringing — calls go straight to voicemail",
            description=(
                "Hi,\n\n"
                "My Zoom Phone has stopped ringing for incoming calls. Calls go straight to\n"
                "voicemail. My Zoom Phone has stopped ringing for incoming calls. Calls go\n"
                "straight to voicemail.\n\n"
                "I've checked my Do Not Disturb settings and they are off. I've checked my Do\n"
                "Not Disturb settings and they are off. The Zoom desktop client shows I'm\n"
                "available (green dot). The Zoom desktop client shows I'm available (green dot).\n\n"
                "My extension is 5-2201 and my direct number is +1 (212) 555-2201. Clients have\n"
                "been complaining they can't reach me. My extension is 5-2201 and my direct\n"
                "number is +1 (212) 555-2201. Clients have been complaining they can't reach me.\n\n"
                "This started yesterday afternoon. I tried signing out and back in, same issue.\n"
                "This started yesterday afternoon. I tried signing out and back in, same issue.\n\n"
                "Please help,\n"
                "Elena Vasquez\n"
                "Client Services, Building 1, 6th floor"
            ),
            category=Category.SOFTWARE,
            priority=Priority.P2,
            team=Team.ENTERPRISE_APPS,
            needs_escalation=False,
            missing_info=[MissingInfo.APPLICATION_VERSION],
            next_best_action=(
                "Troubleshoot Zoom Phone call routing for ext 5-2201 — incoming calls "
                "going directly to voicemail despite available status."
            ),
            remediation_steps=[
                "Check Zoom Phone admin portal for call routing rules on extension 5-2201.",
                "Verify there is no call forwarding or after-hours rule overriding the user's status.",
                "Check if the Zoom Phone license is active and properly assigned to the user.",
                "Test inbound call to the user's direct number while monitoring the admin dashboard.",
                "Update the Zoom desktop client if the version is outdated.",
            ],
            reporter_name="Elena Vasquez",
            reporter_email="elena.vasquez@contoso.com",
            reporter_department="Client Services",
            channel=Channel.PORTAL,
            tags=["data-cleanup", "duplicate-content", "stuttering"],
            difficulty="hard",
        ),
    ]
