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
        # ── DC-013  Extremely long email with buried issue ────────────────
        ScenarioDefinition(
            scenario_id="DC-013",
            subject="FW: Quarterly IT Infrastructure Review — action items and network issue",
            description=(
                "Hi IT Support,\n\n"
                "Forwarding the full infrastructure review notes below — my actual issue is buried\n"
                "near the bottom. Please scroll down.\n\n"
                "====== QUARTERLY IT INFRASTRUCTURE REVIEW — Q1 2026 ======\n"
                "Date: March 14, 2026 | Attendees: IT Steering Committee\n"
                "Location: Building 4, Executive Conference Room 4A\n\n"
                "AGENDA ITEM 1: Cloud Migration Status\n"
                "- Azure landing zone provisioning is 94% complete across all three regions.\n"
                "- Remaining workloads: legacy COBOL settlement engine (target: May 2026),\n"
                "  on-prem Oracle RAC cluster for derivatives pricing (target: July 2026).\n"
                "- Cost optimization: reserved instance coverage improved from 61% to 78%.\n"
                "- Action: Cloud team to finalize RI recommendations for Q2 by March 28.\n\n"
                "AGENDA ITEM 2: Endpoint Refresh Program\n"
                "- 1,200 of 3,400 laptops refreshed to Dell Latitude 5550 with Windows 11 23H2.\n"
                "- Remaining rollout schedule: NYC Building 1-3 (April), London (May), Singapore (June).\n"
                "- Dock compatibility issues reported with TB16 docks — WD19S replacement in progress.\n"
                "- BitLocker recovery key escrow migration to Intune on track for April 1.\n"
                "- Action: Endpoint team to publish refresh FAQ on the intranet by March 21.\n\n"
                "AGENDA ITEM 3: Network Capacity Planning\n"
                "- Core switch fabric utilization peaked at 72% during February month-end processing.\n"
                "- Wireless controller firmware upgraded to 8.10.185 across all NYC APs.\n"
                "- SD-WAN deployment for London and Singapore branch offices approved — RFP in April.\n"
                "- Action: Network ops to model 100G uplink requirements for 2027 budget.\n\n"
                "AGENDA ITEM 4: Security & Compliance Update\n"
                "- SOC 2 Type II audit fieldwork begins April 7. All evidence must be staged by April 1.\n"
                "- Phishing simulation click rate dropped from 12% to 8.5% — goal is 5% by year-end.\n"
                "- Privileged Access Workstation (PAW) rollout to Tier 0 admins complete.\n"
                "- Action: Security ops to deliver PAW Tier 1 rollout plan by March 28.\n\n"
                "AGENDA ITEM 5: Service Desk Metrics\n"
                "- Mean time to resolve (MTTR): 4.2 hours (target 4.0) — slight regression from Feb.\n"
                "- First-contact resolution rate: 68% (target 70%).\n"
                "- Top ticket categories: Password resets (24%), VPN issues (18%), Outlook (14%).\n"
                "- Action: Evaluate chatbot deflection for password reset tickets.\n\n"
                "AGENDA ITEM 6: Disaster Recovery Testing\n"
                "- Full DR failover test for Azure-hosted trading platform scheduled for April 19-20.\n"
                "- RPO target: 15 minutes. RTO target: 2 hours. Last test achieved RPO 12m, RTO 1h 48m.\n"
                "- Cross-region replication lag for Cosmos DB reduced from 320ms to 95ms.\n"
                "- Action: DR team to coordinate with Trading and Compliance for the test window.\n\n"
                "AGENDA ITEM 7: Data Center Decommissioning\n"
                "- Secaucus DC lease expires September 2026. 14 remaining racks to be migrated.\n"
                "- Physical server inventory audit complete — 6 servers unaccounted for, investigating.\n"
                "- Tape backup archive migration to Azure Blob Archive tier: 340TB of 480TB complete.\n"
                "- Action: Facilities to confirm decommissioning timeline with vendor by April 4.\n\n"
                "--- END OF AGENDA ITEMS ---\n\n"
                "** MY ACTUAL ISSUE (sorry for the long email) **\n\n"
                "On page 2 of the notes it mentions TB16 dock compatibility issues. I'm one of the\n"
                "affected users — my Dell Latitude 5550 with the TB16 dock loses USB-C video output\n"
                "intermittently. Both my external Dell U2722D monitors go black for 5-10 seconds\n"
                "every 20-30 minutes. I'm on the 8th floor, Building 4. The old WD19S dock I had\n"
                "before worked perfectly but it was collected during the refresh.\n\n"
                "Can I get a replacement WD19S dock or a fix for the TB16 compatibility?\n\n"
                "Thanks,\n"
                "Jonathan Park\n"
                "Portfolio Management, Building 4, 8th floor, New York"
            ),
            category=Category.HARDWARE,
            priority=Priority.P3,
            team=Team.ENDPOINT,
            needs_escalation=False,
            missing_info=[MissingInfo.DEVICE_INFO],
            next_best_action=(
                "Replace Dell TB16 dock with WD19S for user on Building 4, 8th floor — "
                "known USB-C video dropout issue with Latitude 5550 and TB16 docks."
            ),
            remediation_steps=[
                "Confirm the user's laptop model and current dock firmware version.",
                "Check if a TB16 firmware update resolves the intermittent video dropout.",
                "If the firmware update does not resolve, issue a WD19S replacement dock.",
                "Verify both external monitors work reliably on the replacement dock.",
                "Log the TB16 compatibility issue in the endpoint refresh tracker for reporting.",
            ],
            reporter_name="Jonathan Park",
            reporter_email="jonathan.park@contoso.com",
            reporter_department="Portfolio Management",
            channel=Channel.EMAIL,
            tags=["data-cleanup", "very-long-email", "buried-issue"],
            difficulty="hard",
        ),
        # ── DC-014  Multiple base64 image floods ─────────────────────────
        ScenarioDefinition(
            scenario_id="DC-014",
            subject="Badge reader error — photos attached",
            description=(
                "My badge is not working at the Building 6 south entrance turnstile.\n\n"
                "I took several photos of the error on the badge reader screen. Here they are:\n\n"
                "Photo 1 - Front of badge reader:\n"
                "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEASABIAAD/2wBDAAgGBgcGBQgHBwcJCQgK"
                "DBQNDBALDBKSEF4THBYdHRweGxwdICQuJyAiLCMcHCg3KSwwMTQ0NB8nOT04MjwuMzQy/2wBDAQkJ"
                "CQwLDBgNDRgyIRwhMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIy"
                "MjIyMjL/wAARCABAAEADASIAAhEBAxEB/8QAHwAAAQUBAQEBAQEAAAAAAAAAAAABAgMEBQYHCAkKC//E"
                "AFAQAAIBAwMCBAMFBQQEAAABfQECAwAEEQUSITFBBhNRYQcicRQygZGhCCNCscEVUtHwJDNicoIJChYX"
                "GBkaJicoKSo1Njc4OTpDREVGR0hJSlNUVVZXWFlaY2RlZmdoaWpzdHV2d3h5eoKDhIWGh4iJipKTlJ"
                "WWl5iZmqKjpKWmp6ipqrKztLW2t7i5usLDxMXGx8jJytLT1NXW19jZ2uHi4+Tl5ufo6ery8/T19vf4"
                "+fr/xAAfAQADAQEBAQEBAQEBAAAAAAAAAQIDBAUGBwgJCgv/xABREAACAQIEBAMEBgUDBgMAAAABAgMAE"
                "QQSITFBBRNRYQYicZGBBzKhsRRCUsHB8BYj0fEUFTNickOSstIkZKLC4vDzGBcaNTY3JDREVSRFVWND"
                "/9oADAMBAAIRAxEAAAAB0AAAAFaGBogKoAAAAA0MFNNNAFiAAAAAAAAJIAAAAAAIIIAAAAAAAAAAAAAAAAA"
                "AAAAAA//2Q==\n\n"
                "Photo 2 - Error message closeup:\n"
                "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEASABIAAD/2wBDABsSFBcUERsXFhceHBsgKEIr"
                "KCUlKFE6PTBCYFVlZF9VXFtqeJmBanGQc1tdhbWGkJ6jq62rZ4C8ybqmx5moq6T/2wBDARceHigs"
                "KE4rKU5qd1p3ampqampqampqampqampqampqampqampqampqampqampqampqampqampqampqamr/wAAR"
                "CAAgACADASIAAhEBAxEB/8QAHwAAAQUBAQEBAQEAAAAAAAAAAAECAwQFBgcICQoL/8QAHwEAAwEBAQEB"
                "AQEBAQAAAAAAAAECAwQFBgcICQoL/8QAFRABAAAAAAAAAAAAAAAAAAAAcP/EABQRAQAAAAAAAAAAAAAAA"
                "AAAYP/aAAwDAQACEQMRAD8AlgVVHcjIGcZHPSn1BDKkybkZWHqDmn0AFFFFAB/9k=\n\n"
                "Photo 3 - My badge (front side):\n"
                "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAIAAAACACAYAAADDPmHLAAAACXBIWXMAAA"
                "sTAAALEwEAmpwYAAACcElEQVR4nO3dO27CQBSG4TPiCehpoKGjpMwWKNgSJTtgB2yBgjJboKOkpKGh"
                "4wnIK7gIhGDGc+Z/PkmWkC3N+BvN2BrnAAAAAAAAAAAAAAAAAMDUVWM/gTYq5+9x3/6Y4kQwGpkARA"
                "kARAIAkQBAJAAQCQBEAgCRAEAkABAJAEQCAJEAQCQAEAkARAIA0X9Bep+0vJOUlpJykWQn6UPSLMq8"
                "AAAAAAAAAAAAAAAAAAAAAAAAAAA//2Q==\n\n"
                "Photo 4 - Badge reader model number plate:\n"
                "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAKCAYAAACNMs+9AAAAFUlEQVQYV2"
                "P8z8BQz0AEYBxVOHIVAvcHBQHzKSECAAAAAElFTkSuQmCC"
                "iVBORw0KGgoAAAANSUhEUgAAAAoAAAAKCAYAAACNMs+9AAAAFklEQVQYV2P4z8BQz0AEYBxVSHEVAvMH"
                "BQPxKSMCAAAAAElFTkSuQmCC\n\n"
                "Photo 5 - Side angle of turnstile:\n"
                "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEASABIAAD/2wBDAAgGBgcGBQgHBwcJCQgKDBQN"
                "DAsLDBkSEw8UHRofHh0aHBwgJC4nICIsIxwcKDcpLDAxNDQ0Hyc5PTgyPC4zNDL/2wBDAQkJCQwLDB"
                "gNDRgyIRwhMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMj"
                "L/wAARCAABAAEDASIAAhEBAxEB/8QAHwAAAQUBAQEBAQEAAAAAAAAAAAECAwQFBgcICQoL/8QAFBABAA"
                "AAAAAAAAAAAAAAAAAA/8QAFBEBAAAAAAAAAAAAAAAAAAAAAP/aAAwDAQACEQMRAD8ALQAB//Z=\n\n"
                "The error message on the screen said 'Card Read Error - Contact Facilities' in red.\n"
                "I tried tapping multiple times. My badge works fine at the north entrance.\n\n"
                "Yuki Tanaka\n"
                "Quantitative Analysis, Building 6, 3rd floor"
            ),
            category=Category.HARDWARE,
            priority=Priority.P3,
            team=Team.ENDPOINT,
            needs_escalation=False,
            missing_info=[MissingInfo.DEVICE_INFO],
            next_best_action=(
                "Investigate badge reader 'Card Read Error' at Building 6 south entrance "
                "turnstile — badge works at north entrance, suggesting a reader hardware fault."
            ),
            remediation_steps=[
                "Dispatch a facilities technician to inspect the Building 6 south entrance badge reader.",
                "Check the badge reader logs for error patterns and failed card reads.",
                "Test the reader with a known-good badge to confirm it is a reader-side issue.",
                "Replace or recalibrate the reader if it is confirmed faulty.",
                "Verify the user's badge works at the south entrance after the fix.",
            ],
            reporter_name="Yuki Tanaka",
            reporter_email="yuki.tanaka@contoso.com",
            reporter_department="Quantitative Analysis",
            channel=Channel.EMAIL,
            tags=["data-cleanup", "base64-flood", "image-heavy"],
            difficulty="hard",
        ),
        # ── DC-015  Inline CSV / tabular data dump ────────────────────────
        ScenarioDefinition(
            scenario_id="DC-015",
            subject="Server performance degradation — metrics attached inline",
            description=(
                "Hi team,\n\n"
                "The sqlprod-nyc-04 server is running very slow. Here are the performance metrics\n"
                "I exported from our monitoring tool:\n\n"
                "timestamp,cpu_pct,mem_pct,disk_io_mbps,net_in_mbps,net_out_mbps,active_connections,query_queue\n"
                "2026-03-17T08:00:00Z,42.3,61.2,120.5,45.2,32.1,342,12\n"
                "2026-03-17T08:05:00Z,44.1,62.0,125.3,47.8,33.4,351,14\n"
                "2026-03-17T08:10:00Z,48.7,63.5,131.2,49.1,35.2,367,18\n"
                "2026-03-17T08:15:00Z,55.2,65.8,142.7,52.3,38.6,389,24\n"
                "2026-03-17T08:20:00Z,62.8,68.4,158.3,56.7,41.2,412,32\n"
                "2026-03-17T08:25:00Z,71.3,72.1,175.6,61.4,44.8,438,45\n"
                "2026-03-17T08:30:00Z,78.9,76.3,192.4,67.2,48.3,461,58\n"
                "2026-03-17T08:35:00Z,84.2,79.8,210.1,72.8,52.1,487,72\n"
                "2026-03-17T08:40:00Z,89.1,83.4,228.7,78.3,56.7,512,89\n"
                "2026-03-17T08:45:00Z,93.7,87.2,245.3,83.9,61.2,538,105\n"
                "2026-03-17T08:50:00Z,96.2,90.1,261.8,89.4,65.8,561,128\n"
                "2026-03-17T08:55:00Z,98.1,92.8,278.4,94.7,70.3,589,156\n"
                "2026-03-17T09:00:00Z,99.3,95.4,295.1,100.2,74.9,612,189\n"
                "2026-03-17T09:05:00Z,99.7,96.8,310.6,105.8,79.4,641,224\n"
                "2026-03-17T09:10:00Z,99.8,97.5,326.2,111.3,83.8,668,261\n"
                "2026-03-17T09:15:00Z,99.9,98.1,341.7,116.9,88.3,694,298\n"
                "2026-03-17T09:20:00Z,99.9,98.6,357.3,122.4,92.7,721,336\n"
                "2026-03-17T09:25:00Z,99.9,99.0,372.8,128.0,97.2,748,374\n"
                "2026-03-17T09:30:00Z,100.0,99.2,388.4,133.5,101.6,776,412\n\n"
                "As you can see CPU goes from 42% to 100% in 90 minutes. The query queue is\n"
                "backing up and users are complaining about slow report generation.\n\n"
                "Leon Fischer\n"
                "Data Engineering, NYC"
            ),
            category=Category.DATA_STORAGE,
            priority=Priority.P2,
            team=Team.DATA_PLATFORM,
            needs_escalation=True,
            missing_info=[MissingInfo.AFFECTED_USERS, MissingInfo.BUSINESS_IMPACT],
            next_best_action=(
                "Investigate sqlprod-nyc-04 resource exhaustion — CPU at 100%, memory at 99%, "
                "and query queue growing to 400+ since 08:00. Likely a runaway query or batch job."
            ),
            remediation_steps=[
                "Identify the top resource-consuming queries on sqlprod-nyc-04 using sys.dm_exec_requests.",
                "Check if a scheduled batch job or report is causing the CPU and memory spike.",
                "Kill or throttle the runaway query if identified, and notify the owning team.",
                "Monitor the server for recovery and verify the query queue is draining.",
                "Review Resource Governor settings to prevent a single workload from saturating the server.",
            ],
            reporter_name="Leon Fischer",
            reporter_email="leon.fischer@contoso.com",
            reporter_department="Data Engineering",
            channel=Channel.CHAT,
            tags=["data-cleanup", "csv-dump", "tabular-data"],
            difficulty="hard",
        ),
        # ── DC-016  URL spam / hyperlink overload ─────────────────────────
        ScenarioDefinition(
            scenario_id="DC-016",
            subject="Broken links on the intranet compliance pages",
            description=(
                "Hi,\n\n"
                "Multiple links on our compliance intranet site are broken. Here are all the ones\n"
                "I've checked (some work, most don't):\n\n"
                "BROKEN:\n"
                "- https://intranet.contoso.com/compliance/policies/aml-kyc-policy-v3.2.pdf\n"
                "- https://intranet.contoso.com/compliance/policies/insider-trading-guidelines.pdf\n"
                "- https://intranet.contoso.com/compliance/training/annual-certification-2026.aspx\n"
                "- https://intranet.contoso.com/compliance/forms/conflict-of-interest-disclosure.docx\n"
                "- https://intranet.contoso.com/compliance/policies/data-retention-schedule-v2.1.xlsx\n"
                "- https://intranet.contoso.com/compliance/external/sec-rule-17a-4-reference.pdf\n"
                "- https://intranet.contoso.com/compliance/external/finra-rule-4511-guidance.pdf\n"
                "- https://intranet.contoso.com/compliance/procedures/sar-filing-checklist.pdf\n"
                "- https://intranet.contoso.com/compliance/procedures/whistleblower-procedure.pdf\n"
                "- https://intranet.contoso.com/compliance/training/code-of-conduct-quiz.aspx\n"
                "- https://intranet.contoso.com/compliance/reports/q4-2025-compliance-dashboard.pbix\n"
                "- https://intranet.contoso.com/compliance/reports/regulatory-exam-tracker.xlsx\n\n"
                "WORKING:\n"
                "- https://intranet.contoso.com/compliance/index.aspx\n"
                "- https://intranet.contoso.com/compliance/team/contact-us.aspx\n"
                "- https://intranet.contoso.com/compliance/news/latest-updates.aspx\n\n"
                "We have a regulatory exam next week and auditors need access to these documents.\n"
                "This is urgent.\n\n"
                "Maya Johal\n"
                "Regulatory Affairs, Building 1, 9th floor"
            ),
            category=Category.SOFTWARE,
            priority=Priority.P2,
            team=Team.ENTERPRISE_APPS,
            needs_escalation=True,
            missing_info=[MissingInfo.TIMESTAMP],
            next_best_action=(
                "Investigate broken links on the compliance intranet site — 12 of 15 links "
                "returning errors, likely caused by a content migration or site restructure. "
                "Urgent due to upcoming regulatory exam."
            ),
            remediation_steps=[
                "Check the SharePoint or IIS logs for the compliance site to identify the error pattern.",
                "Verify if a recent content migration or URL restructure moved or renamed the documents.",
                "Restore or redirect the broken document links to their new locations.",
                "Test all 12 broken links after the fix to confirm they resolve correctly.",
                "Notify the Regulatory Affairs team once all links are restored.",
            ],
            reporter_name="Maya Johal",
            reporter_email="maya.johal@contoso.com",
            reporter_department="Regulatory Affairs",
            channel=Channel.EMAIL,
            tags=["data-cleanup", "url-spam", "hyperlink-overload"],
            difficulty="hard",
        ),
        # ── DC-017  Raw SMTP headers dump ─────────────────────────────────
        ScenarioDefinition(
            scenario_id="DC-017",
            subject="Emails from external clients being delayed — headers included",
            description=(
                "Hi IT team,\n\n"
                "I'm getting emails from external clients with delays of 2-4 hours. I grabbed the\n"
                "full message headers from one of the delayed emails — here they are:\n\n"
                "Return-Path: <john.smith@acmecapital.com>\n"
                "Received: from EX01.contoso.com (10.1.4.21) by EX03.contoso.com (10.1.4.23)\n"
                " with Microsoft SMTP Server (version=TLS1_2,\n"
                " cipher=TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384) id 15.2.1118.40;\n"
                " Tue, 17 Mar 2026 14:22:31 -0500\n"
                "Received: from edge01.contoso.com (10.1.2.10) by EX01.contoso.com (10.1.4.21)\n"
                " with Microsoft SMTP Server (version=TLS1_2,\n"
                " cipher=TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384) id 15.2.1118.40;\n"
                " Tue, 17 Mar 2026 14:22:28 -0500\n"
                "Received: from mail-yw1-f169.google.com (209.85.128.169) by edge01.contoso.com\n"
                " (10.1.2.10) with Microsoft SMTP Server (version=TLS1_2,\n"
                " cipher=TLS_ECDHE_RSA_WITH_AES_128_GCM_SHA256) id 15.2.1118.40\n"
                " via Frontend Transport; Tue, 17 Mar 2026 12:15:44 -0500\n"
                "Received: by mail-yw1-f169.google.com with SMTP id\n"
                " 00721157ae682-6f2b3c2e9d4so12345678b3.1\n"
                " for <nadia.okafor@contoso.com>; Tue, 17 Mar 2026 09:15:42 -0800 (PST)\n"
                "DKIM-Signature: v=1; a=rsa-sha256; c=relaxed/relaxed; d=acmecapital.com;\n"
                " s=google; h=from:to:subject:date:message-id:mime-version;\n"
                " bh=abc123def456ghi789jkl012mno345pqr678stu901vwx=;\n"
                " b=ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789abcdefghijklmn\n"
                "Authentication-Results: edge01.contoso.com;\n"
                " dkim=pass (signature was verified) header.d=acmecapital.com;\n"
                " spf=pass (sender IP is 209.85.128.169) smtp.mailfrom=acmecapital.com;\n"
                " dmarc=pass action=none header.from=acmecapital.com;\n"
                "X-MS-Exchange-Organization-SCL: 1\n"
                "X-MS-Exchange-Organization-AuthSource: edge01.contoso.com\n"
                "X-MS-Exchange-Organization-AuthAs: Anonymous\n"
                "X-MS-Exchange-Transport-CrossTenantHeadersStamped: EX03.contoso.com\n"
                "X-Forefront-Antispam-Report: CIP:209.85.128.169;CTRY:US;LANG:en;\n"
                " SFV:NSPM;SFS:;DIR:INB;SFP:;SCL:1;SRVR:EX03;\n"
                "Message-ID: <CABx+XYZ123@mail.gmail.com>\n"
                "Date: Tue, 17 Mar 2026 09:15:40 -0800\n"
                "From: John Smith <john.smith@acmecapital.com>\n"
                "To: Nadia Okafor <nadia.okafor@contoso.com>\n"
                "Subject: Q1 Portfolio Rebalancing - Urgent Review\n"
                "MIME-Version: 1.0\n"
                'Content-Type: multipart/alternative; boundary="0000000000abc123def456"\n\n'
                "As you can see, there's a 2+ hour gap between when it hits edge01 at 12:15\n"
                "and when it reaches EX01 at 14:22. This is happening on most external emails.\n"
                "Internal emails are fine.\n\n"
                "Nadia Okafor\n"
                "Client Services, Building 1, 4th floor, New York"
            ),
            category=Category.NETWORK,
            priority=Priority.P2,
            team=Team.NETWORK_OPS,
            needs_escalation=True,
            missing_info=[MissingInfo.AFFECTED_USERS],
            next_best_action=(
                "Investigate 2-hour mail delivery delay between edge01 and EX01 for inbound "
                "external email — likely a mail queue bottleneck or transport rule processing delay."
            ),
            remediation_steps=[
                "Check the mail queue on edge01.contoso.com for message backlog or throttling.",
                "Review Exchange transport rule processing times for inbound external messages.",
                "Check Forefront/EOP content filtering for latency spikes on edge01.",
                "Verify network connectivity and DNS resolution between edge01 and EX01.",
                "If a queue backlog is confirmed, increase transport capacity or clear stuck messages.",
            ],
            reporter_name="Nadia Okafor",
            reporter_email="nadia.okafor@contoso.com",
            reporter_department="Client Services",
            channel=Channel.EMAIL,
            tags=["data-cleanup", "smtp-headers", "raw-headers"],
            difficulty="hard",
        ),
        # ── DC-018  Unicode/RTL text & zero-width characters ──────────────
        ScenarioDefinition(
            scenario_id="DC-018",
            subject="Can\u2019t upload files to SharePoint \u200e\u200f\u200b\u2069— help needed",
            description=(
                "Hi,\n\n"
                "I\u2019m having trouble uploading files to our team\u2019s SharePoint site.\u200b\u200b\u200b\n\n"
                "When I try to upload, I get this error:\u200e\n"
                "\u200f\u202b\u0627\u0644\u062e\u0637\u0623: "
                "\u0641\u0634\u0644 \u0627\u0644\u062a\u062d\u0645\u064a\u0644\u202c\u200e "
                '"Upload failed: The file name contains invalid characters"\u200b\u200b\n\n'
                "The file I\u2019m trying to upload is:\u200e\n"
                "\u200fQ1\u200b_2026_\u200e\u200fPortfolio\u200b_\u200eAnalysis\u200f_FINAL\u200b\u200b\u200b.xlsx\u200e\n\n"
                "I renamed it from the original which was:\u200e\n"
                "\u200f\u202b\u062a\u062d\u0644\u064a\u0644_\u0627\u0644\u0645\u062d\u0641\u0638\u0629_\u0627\u0644\u0631\u0628\u0639_\u0627\u0644\u0623\u0648\u0644\u202c\u200e_2026.xlsx\n\n"
                "Even the renamed version won\u2019t upload.\u200b My colleague Amir can upload\n"
                "files fine from his machine.\u200b\u200b\u200b I\u2019m using Edge on Windows 11.\u200b\n\n"
                "The SharePoint site URL is:\u200e\n"
                "https://contoso.sharepoint.com/sites/\u200fWealthMgmt\u200e/Shared%20Documents\u200b\n\n"
                "Please help, I have a client presentation tomorrow and need\n"
                "to share these files with the team.\u200b\u200b\u200b\n\n"
                "Layla Mansouri\u200e\u200f\n"
                "Wealth Management, Building 2, 5th floor, London\u200b"
            ),
            category=Category.SOFTWARE,
            priority=Priority.P2,
            team=Team.ENTERPRISE_APPS,
            needs_escalation=False,
            missing_info=[MissingInfo.APPLICATION_VERSION],
            next_best_action=(
                "Investigate SharePoint upload failure caused by invisible Unicode characters "
                "(zero-width spaces, RTL/LTR marks) in the file name — user needs to strip "
                "hidden characters from the filename."
            ),
            remediation_steps=[
                "Identify the zero-width and bidirectional Unicode characters in the file name.",
                "Rename the file using only ASCII characters and re-attempt the upload.",
                "Check if the original Arabic filename triggered SharePoint's invalid character filter.",
                "Verify the SharePoint site does not have a custom file naming policy blocking the upload.",
                "Confirm the upload succeeds after the file is renamed with clean characters.",
            ],
            reporter_name="Layla Mansouri",
            reporter_email="layla.mansouri@contoso.com",
            reporter_department="Wealth Management",
            channel=Channel.PORTAL,
            tags=["data-cleanup", "unicode-rtl", "zero-width-chars"],
            difficulty="hard",
        ),
        # ── DC-019  JSON / XML configuration dump inline ──────────────────
        ScenarioDefinition(
            scenario_id="DC-019",
            subject="Application gateway returning 502 — config dump attached",
            description=(
                "Hi,\n\n"
                "Our Azure Application Gateway (appgw-prod-eus2-01) is returning 502 Bad Gateway\n"
                "errors intermittently. I exported the current backend pool configuration:\n\n"
                "```json\n"
                "{\n"
                '  "backendAddressPools": [\n'
                "    {\n"
                '      "name": "pool-api-prod",\n'
                '      "properties": {\n'
                '        "backendAddresses": [\n'
                '          { "ipAddress": "10.42.1.10" },\n'
                '          { "ipAddress": "10.42.1.11" },\n'
                '          { "ipAddress": "10.42.1.12" },\n'
                '          { "ipAddress": "10.42.1.13" }\n'
                "        ],\n"
                '        "provisioningState": "Succeeded"\n'
                "      }\n"
                "    },\n"
                "    {\n"
                '      "name": "pool-web-prod",\n'
                '      "properties": {\n'
                '        "backendAddresses": [\n'
                '          { "ipAddress": "10.42.2.10" },\n'
                '          { "ipAddress": "10.42.2.11" },\n'
                '          { "ipAddress": "10.42.2.12" }\n'
                "        ],\n"
                '        "provisioningState": "Succeeded"\n'
                "      }\n"
                "    }\n"
                "  ],\n"
                '  "backendHttpSettingsCollection": [\n'
                "    {\n"
                '      "name": "http-settings-api",\n'
                '      "properties": {\n'
                '        "port": 8443,\n'
                '        "protocol": "Https",\n'
                '        "requestTimeout": 30,\n'
                '        "probe": { "id": "/subscriptions/.../probes/probe-api-health" },\n'
                '        "hostName": "api-internal.contoso.com",\n'
                '        "pickHostNameFromBackendAddress": false\n'
                "      }\n"
                "    },\n"
                "    {\n"
                '      "name": "http-settings-web",\n'
                '      "properties": {\n'
                '        "port": 443,\n'
                '        "protocol": "Https",\n'
                '        "requestTimeout": 60,\n'
                '        "probe": { "id": "/subscriptions/.../probes/probe-web-health" },\n'
                '        "hostName": "www-internal.contoso.com",\n'
                '        "pickHostNameFromBackendAddress": false\n'
                "      }\n"
                "    }\n"
                "  ],\n"
                '  "probes": [\n'
                "    {\n"
                '      "name": "probe-api-health",\n'
                '      "properties": {\n'
                '        "protocol": "Https",\n'
                '        "host": "api-internal.contoso.com",\n'
                '        "path": "/health",\n'
                '        "interval": 30,\n'
                '        "timeout": 10,\n'
                '        "unhealthyThreshold": 3\n'
                "      }\n"
                "    },\n"
                "    {\n"
                '      "name": "probe-web-health",\n'
                '      "properties": {\n'
                '        "protocol": "Https",\n'
                '        "host": "www-internal.contoso.com",\n'
                '        "path": "/healthz",\n'
                '        "interval": 30,\n'
                '        "timeout": 10,\n'
                '        "unhealthyThreshold": 3\n'
                "      }\n"
                "    }\n"
                "  ]\n"
                "}\n"
                "```\n\n"
                "The 502 errors happen mostly between 09:00-09:30 when traffic spikes. The health\n"
                "probes seem to be passing fine in Azure Portal. Could be a backend timeout issue\n"
                "since the API pool timeout is only 30 seconds.\n\n"
                "Henrik Svensson\n"
                "Cloud Infrastructure, New York"
            ),
            category=Category.NETWORK,
            priority=Priority.P2,
            team=Team.NETWORK_OPS,
            needs_escalation=False,
            missing_info=[MissingInfo.ERROR_MESSAGE],
            next_best_action=(
                "Investigate intermittent 502 errors on appgw-prod-eus2-01 during morning "
                "traffic peak — backend pool timeout of 30s may be too low for the API tier "
                "under load."
            ),
            remediation_steps=[
                "Check Application Gateway access logs for 502 errors and correlate with backend health probe results.",
                "Review backend pool member (10.42.1.10-13) health status during the 09:00-09:30 window.",
                "Increase the API backend HTTP settings request timeout from 30s to 60s.",
                "Check if the backend VMs are hitting CPU or memory limits during the traffic spike.",
                "Consider enabling connection draining and auto-scaling on the Application Gateway.",
            ],
            reporter_name="Henrik Svensson",
            reporter_email="henrik.svensson@contoso.com",
            reporter_department="Cloud Infrastructure",
            channel=Channel.CHAT,
            tags=["data-cleanup", "json-config-dump", "inline-code"],
            difficulty="hard",
        ),
        # ── DC-020  Auto-reply / out-of-office loop concatenation ─────────
        ScenarioDefinition(
            scenario_id="DC-020",
            subject="Re: Re: Re: Automatic reply: Re: Automatic reply: VPN token expired",
            description=(
                "--- Automatic Reply ---\n"
                "Thank you for your email. I am currently out of the office from March 14\n"
                "through March 21 with limited access to email. For urgent IT matters, please\n"
                "contact the IT Service Desk at x5000 or itsupport@contoso.com.\n\n"
                "Best regards,\nAmy Chen\nIT Service Desk Analyst\n\n"
                "--- Automatic Reply ---\n"
                "Hi, this is Carlos Mendez. I'm out of the office until March 19.\n"
                "For immediate assistance please reach out to my backup, Jenny Park\n"
                "(jenny.park@contoso.com).\n\n"
                "--- Automatic Reply ---\n"
                "Thank you for your email. I am currently out of the office from March 14\n"
                "through March 21 with limited access to email. For urgent IT matters, please\n"
                "contact the IT Service Desk at x5000 or itsupport@contoso.com.\n\n"
                "Best regards,\nAmy Chen\nIT Service Desk Analyst\n\n"
                "--- Automatic Reply ---\n"
                "Hi, this is Carlos Mendez. I'm out of the office until March 19.\n"
                "For immediate assistance please reach out to my backup, Jenny Park\n"
                "(jenny.park@contoso.com).\n\n"
                "--- Original Message ---\n"
                "From: Carlos Mendez <carlos.mendez@contoso.com>\n"
                "Sent: Thursday, March 14, 2026 2:05 PM\n"
                "To: IT Support <itsupport@contoso.com>\n"
                "Subject: VPN token expired\n\n"
                "Hi team,\n\n"
                "My RSA SecurID soft token expired and I can't generate new VPN codes. The\n"
                "token shows 'Token Disabled' in the app. I need VPN access to work from\n"
                "home next week while the office is closed for maintenance.\n\n"
                "My employee ID is E-28491. Can you please re-provision my token?\n\n"
                "Thanks,\n"
                "Carlos Mendez\n"
                "Derivatives, Building 3, 6th floor, New York"
            ),
            category=Category.ACCESS_AUTH,
            priority=Priority.P2,
            team=Team.IAM,
            needs_escalation=False,
            missing_info=[MissingInfo.DEVICE_INFO],
            next_best_action=(
                "Re-provision expired RSA SecurID soft token for employee E-28491 — "
                "token shows 'Disabled' and user needs VPN access for remote work next week."
            ),
            remediation_steps=[
                "Look up employee E-28491 in the RSA Authentication Manager console.",
                "Verify the token status and confirm it is disabled/expired.",
                "Re-provision a new RSA SecurID soft token and send the activation link to the user.",
                "Guide the user through importing the new token on their mobile device.",
                "Test VPN connectivity with the new token before the office closure.",
            ],
            reporter_name="Carlos Mendez",
            reporter_email="carlos.mendez@contoso.com",
            reporter_department="Derivatives",
            channel=Channel.EMAIL,
            tags=["data-cleanup", "auto-reply-loop", "ooo-concatenation"],
            difficulty="hard",
        ),
        # ── DC-021  Enormous forward chain with 10+ participants ─────────────
        ScenarioDefinition(
            scenario_id="DC-021",
            subject=("FW: FW: FW: FW: FW: FW: FW: FW: FW: FW: Re: SAP access for new joiner"),
            description=(
                "--- Latest reply ---\n"
                "Hi IT, can someone PLEASE just grant the SAP access already? This has "
                "been bouncing around for two weeks.\n"
                "— Anita\n\n"
                "--- Forwarded by: Raj Kapoor (raj.kapoor@contoso.com) ---\n"
                "Anita, I don't handle SAP provisioning anymore. Forwarding to IT.\n\n"
                "--- Forwarded by: Chen Wei (chen.wei@contoso.com) ---\n"
                "Raj, can you take this? I think SAP is under your team now.\n\n"
                "--- Forwarded by: Lisa Johansson (lisa.johansson@contoso.com) ---\n"
                "Chen, this came to me by mistake. Please route to the right team.\n\n"
                "--- Forwarded by: Mike Torres (mike.torres@contoso.com) ---\n"
                "Lisa, not sure who handles this. Adding you since you did it last time.\n\n"
                "--- Forwarded by: Priya Sharma (priya.sharma@contoso.com) ---\n"
                "Mike, I'm on parental leave. Please find someone else.\n\n"
                "--- Forwarded by: David Kim (david.kim@contoso.com) ---\n"
                "Priya, you did SAP access last quarter — can you handle this?\n\n"
                "--- Forwarded by: Fatima Al-Rashid (fatima.al-rashid@contoso.com) ---\n"
                "David, this should go to the SAP team. I only handle Salesforce.\n\n"
                "--- Forwarded by: Tom O'Brien (tom.obrien@contoso.com) ---\n"
                "Fatima, can your team handle this? I think it's an enterprise app thing.\n\n"
                "--- Forwarded by: Sandra Nguyen (sandra.nguyen@contoso.com) ---\n"
                "Tom, forwarding to you since you're the app team lead.\n\n"
                "--- Original Message ---\n"
                "From: Anita Desai <anita.desai@contoso.com>\n"
                "Sent: Monday, March 3, 2026 9:00 AM\n"
                "To: IT Support <itsupport@contoso.com>\n"
                "Subject: SAP access for new joiner\n\n"
                "Hi team,\n\n"
                "I just joined the Finance department last week and need SAP access "
                "(modules: FI, CO, and MM) to start processing invoices. My employee "
                "ID is E-31024 and my manager is Robert Chen (Director, Finance).\n\n"
                "Thanks,\nAnita Desai\nFinance, Building 1, 3rd floor, New York"
            ),
            category=Category.ACCESS_AUTH,
            priority=Priority.P3,
            team=Team.IAM,
            needs_escalation=False,
            missing_info=[MissingInfo.ENVIRONMENT_DETAILS],
            next_best_action=(
                "Provision SAP access (FI, CO, MM modules) for new joiner E-31024 in "
                "Finance — request has been circulating for two weeks through a long "
                "forward chain. Verify manager approval from Robert Chen."
            ),
            remediation_steps=[
                "Verify the new joiner's employment and role with HR using employee ID E-31024.",
                "Confirm manager authorization from Robert Chen for SAP FI, CO, and MM access.",
                "Provision the SAP user account with the appropriate role profile for Finance.",
                "Send the user their SAP login credentials via the secure onboarding portal.",
                "Follow up to confirm access is working and the user can process invoices.",
            ],
            reporter_name="Anita Desai",
            reporter_email="anita.desai@contoso.com",
            reporter_department="Finance",
            channel=Channel.EMAIL,
            tags=["data-cleanup", "long-email", "forward-chain"],
            difficulty="hard",
        ),
        # ── DC-022  Base64-encoded PDF pasted as raw text ────────────────────
        ScenarioDefinition(
            scenario_id="DC-022",
            subject="Cannot open expense report — raw PDF data below",
            description=(
                "Hi IT,\n\n"
                "I can't open an expense report PDF that a vendor sent me. When I try to "
                "open it in Adobe, it shows 'This file is damaged and could not be repaired.' "
                "I'm pasting the raw file content since the portal won't let me attach:\n\n"
                "JVBERi0xLjQKMSAwIG9iago8PCAvVHlwZSAvQ2F0YWxvZyAvUGFnZXMgMiAwIFIgPj4KZW5k\n"
                "b2JqCjIgMCBvYmoKPDwgL1R5cGUgL1BhZ2VzIC9LaWRzIFszIDAgUl0gL0NvdW50IDEgPj4K\n"
                "ZW5kb2JqCjMgMCBvYmoKPDwgL1R5cGUgL1BhZ2UgL1BhcmVudCAyIDAgUiAvTWVkaWFCb3gg\n"
                "WzAgMCA2MTIgNzkyXSAvQ29udGVudHMgNCAwIFIgL1Jlc291cmNlcyA8PCAvRm9udCA8PCAv\n"
                "RjEgNSAwIFIgPj4gPj4gPj4KZW5kb2JqCjQgMCBvYmoKPDwgL0xlbmd0aCAxMjQgPj4Kc3Ry\n"
                "ZWFtCkJUCi9GMSAxOCBUZgowIDAgVGQKKEV4cGVuc2UgUmVwb3J0IC0gVmVuZG9yIEluYykg\n"
                "VGoKMCAtMjUgVGQKKFRvdGFsOiAkMTIsMzQ1LjY3KSBUagowIC0yNSBUZAooU3RhdHVzOiBQ\n"
                "ZW5kaW5nIEFwcHJvdmFsKSBUagpFVAplbmRzdHJlYW0KZW5kb2JqCjUgMCBvYmoKPDwgL1R5\n"
                "cGUgL0ZvbnQgL1N1YnR5cGUgL1R5cGUxIC9CYXNlRm9udCAvSGVsdmV0aWNhID4+CmVuZG9i\n"
                "agp4cmVmCjAgNgowMDAwMDAwMDAwIDY1NTM1IGYgCjAwMDAwMDAwMDkgMDAwMDAgbiAKMMDAwMD\n"
                "AwMDA2MyAwMDAwMCBuIAowMDAwMDAwMTIwIDAwMDAwIG4gCjAwMDAwMDAzMDQgMDAwMDAgbiAK\n"
                "MDAwMDAwMDQ4MCAwMDAwMCBuIAp0cmFpbGVyCjw8IC9TaXplIDYgL1Jvb3QgMSAwIFIgPj4K\n"
                "c3RhcnR4cmVmCjU3MQolJUVPRgo=\n\n"
                "The expense amount is $12,345.67 from Vendor Inc. and I need to submit "
                "it for approval by end of week. I'm using Adobe Acrobat Reader DC 2024 "
                "on Windows 11."
            ),
            category=Category.SOFTWARE,
            priority=Priority.P3,
            team=Team.ENTERPRISE_APPS,
            needs_escalation=False,
            missing_info=[MissingInfo.STEPS_TO_REPRODUCE],
            next_best_action=(
                "Investigate corrupted PDF from vendor — user cannot open expense report "
                "in Adobe Acrobat Reader DC. May be a file transfer corruption issue or "
                "incompatible PDF version. Ignore the base64-encoded raw PDF data in "
                "the ticket body."
            ),
            remediation_steps=[
                "Ask the user to re-download the PDF from the original email or vendor portal.",
                "Test opening the file with an alternative PDF reader (Edge, Chrome built-in).",
                "Check if the email attachment was corrupted during transfer (compare file sizes).",
                "If the vendor's PDF is consistently corrupt, request a re-send from the vendor.",
                "Verify Adobe Acrobat Reader DC is up to date and not blocked by Group Policy.",
            ],
            reporter_name="Hannah Eriksson",
            reporter_email="hannah.eriksson@contoso.com",
            reporter_department="Procurement",
            channel=Channel.PORTAL,
            tags=["data-cleanup", "base64", "raw-file-content"],
            difficulty="hard",
        ),
        # ── DC-023  Massive PowerShell / terminal output dump ────────────────
        ScenarioDefinition(
            scenario_id="DC-023",
            subject="Azure deployment failing — full terminal output",
            description=(
                "Hi,\n\n"
                "Our Azure deployment pipeline keeps failing. Here's the full output:\n\n"
                "PS C:\\deploy> .\\deploy-infra.ps1 -Environment prod -Region eastus2\n"
                "VERBOSE: [2026-03-17 14:22:01] Starting deployment to eastus2...\n"
                "VERBOSE: [2026-03-17 14:22:01] Loading ARM template: main.bicep\n"
                "VERBOSE: [2026-03-17 14:22:02] Validating template parameters...\n"
                "VERBOSE: [2026-03-17 14:22:02] Parameter 'vmSize': Standard_D4s_v3\n"
                "VERBOSE: [2026-03-17 14:22:02] Parameter 'nodeCount': 5\n"
                "VERBOSE: [2026-03-17 14:22:02] Parameter 'aksVersion': 1.28.5\n"
                "VERBOSE: [2026-03-17 14:22:03] Connecting to subscription: prod-sub-001\n"
                "VERBOSE: [2026-03-17 14:22:03] Resource group: rg-prod-eus2-001\n"
                "VERBOSE: [2026-03-17 14:22:04] Starting what-if analysis...\n"
                "VERBOSE: [2026-03-17 14:22:15] What-if: 47 resources to create/modify\n"
                "VERBOSE: [2026-03-17 14:22:16] Deploying resource 1/47: Microsoft.Network/virtualNetworks\n"
                "VERBOSE: [2026-03-17 14:22:22] ✓ vnet-prod-eus2 created\n"
                "VERBOSE: [2026-03-17 14:22:23] Deploying resource 2/47: Microsoft.Network/networkSecurityGroups\n"
                "VERBOSE: [2026-03-17 14:22:28] ✓ nsg-aks-prod created\n"
                "VERBOSE: [2026-03-17 14:22:29] Deploying resource 3/47: Microsoft.Network/privateDnsZones\n"
                "VERBOSE: [2026-03-17 14:22:35] ✓ privatelink.eastus2.azmk8s.io created\n"
                "VERBOSE: [2026-03-17 14:22:36] Deploying resource 4/47: Microsoft.ContainerService/managedClusters\n"
                "VERBOSE: [2026-03-17 14:22:37] Waiting for AKS cluster provisioning...\n"
                "VERBOSE: [2026-03-17 14:25:42] ✓ aks-prod-eus2 provisioning started\n"
                "VERBOSE: [2026-03-17 14:30:01] Deploying resource 5/47: Microsoft.KeyVault/vaults\n"
                "VERBOSE: [2026-03-17 14:30:15] ✓ kv-prod-eus2-001 created\n"
                "VERBOSE: [2026-03-17 14:30:16] Deploying resource 6/47: Microsoft.Storage/storageAccounts\n"
                "VERBOSE: [2026-03-17 14:30:22] ✓ stprodeus2001 created\n"
                "VERBOSE: [2026-03-17 14:30:23] Deploying resource 7/47: Microsoft.Sql/servers\n"
                "VERBOSE: [2026-03-17 14:30:45] ✓ sql-prod-eus2 created\n"
                "VERBOSE: [2026-03-17 14:30:46] Deploying resource 8/47: Microsoft.Sql/servers/databases\n"
                "ERROR: [2026-03-17 14:31:02] ✗ DEPLOYMENT FAILED\n"
                "ERROR: New-AzResourceGroupDeployment: 14:31:02 - Resource "
                "Microsoft.Sql/servers/databases 'sql-prod-eus2/appdb-prod' failed with "
                "message: 'The DTU quota for the subscription has been exceeded. "
                "Requested: 250 DTU, Available: 0 DTU. Please increase your DTU quota "
                "or reduce the requested DTU.'\n"
                "ERROR: Deployment 'deploy-20260317-142201' failed.\n"
                "VERBOSE: [2026-03-17 14:31:03] Rolling back 8 resources...\n"
                "VERBOSE: [2026-03-17 14:32:15] Rollback complete.\n"
                "PS C:\\deploy>\n\n"
                "Can you help? We need this in production by Friday."
            ),
            category=Category.DATA_STORAGE,
            priority=Priority.P2,
            team=Team.DATA_PLATFORM,
            needs_escalation=False,
            missing_info=[MissingInfo.BUSINESS_IMPACT],
            next_best_action=(
                "Investigate Azure SQL DTU quota exhaustion blocking production "
                "deployment — subscription prod-sub-001 has 0 DTU remaining. Need to "
                "increase the DTU quota or optimize existing database allocations."
            ),
            remediation_steps=[
                "Check the current DTU allocation across all databases in subscription prod-sub-001.",
                "Identify databases that are over-provisioned or unused and can be scaled down.",
                "Submit an Azure support request to increase the DTU quota if needed.",
                "Consider switching to vCore-based pricing for more flexible resource management.",
                "Re-run the deployment after quota is available and verify all 47 resources deploy.",
            ],
            reporter_name="Alex Petrov",
            reporter_email="alex.petrov@contoso.com",
            reporter_department="Cloud Infrastructure",
            channel=Channel.PORTAL,
            tags=["data-cleanup", "terminal-output", "verbose-logs"],
            difficulty="hard",
        ),
        # ── DC-024  Concatenated monitoring / alerting notifications ─────────
        ScenarioDefinition(
            scenario_id="DC-024",
            subject="FW: [ALERT] Multiple monitoring alerts — disk space",
            description=(
                "--- Alert 1 of 12 ---\n"
                "[CRITICAL] Nagios Alert: DISK CRITICAL - /data on db-prod-03 is 98% full "
                "(467GB/476GB) | Triggered: 2026-03-17 02:15:00 UTC\n"
                "Host: db-prod-03.contoso.local | Service: disk_space_/data\n"
                "Contact: oncall-data@contoso.com | Notification: 1/5\n\n"
                "--- Alert 2 of 12 ---\n"
                "[CRITICAL] Nagios Alert: DISK CRITICAL - /data on db-prod-03 is 98% full "
                "(468GB/476GB) | Triggered: 2026-03-17 02:30:00 UTC\n"
                "Host: db-prod-03.contoso.local | Service: disk_space_/data\n"
                "Contact: oncall-data@contoso.com | Notification: 2/5\n\n"
                "--- Alert 3 of 12 ---\n"
                "[CRITICAL] Nagios Alert: DISK CRITICAL - /data on db-prod-03 is 99% full "
                "(469GB/476GB) | Triggered: 2026-03-17 02:45:00 UTC\n"
                "Host: db-prod-03.contoso.local | Service: disk_space_/data\n"
                "Contact: oncall-data@contoso.com | Notification: 3/5\n\n"
                "--- Alert 4 of 12 ---\n"
                "[WARNING] Nagios Alert: SWAP WARNING - Swap usage on db-prod-03 is 82% "
                "| Triggered: 2026-03-17 02:47:00 UTC\n"
                "Host: db-prod-03.contoso.local | Service: swap_usage\n\n"
                "--- Alert 5 of 12 ---\n"
                "[CRITICAL] Nagios Alert: DISK CRITICAL - /data on db-prod-03 is 99% full "
                "(470GB/476GB) | Triggered: 2026-03-17 03:00:00 UTC\n\n"
                "--- Alerts 6-11 (same pattern, 15-minute intervals) ---\n\n"
                "--- Alert 12 of 12 ---\n"
                "[CRITICAL] Nagios Alert: DISK CRITICAL - /data on db-prod-03 is 99% full "
                "(475GB/476GB) | Triggered: 2026-03-17 05:45:00 UTC\n"
                "Host: db-prod-03.contoso.local | Service: disk_space_/data\n"
                "Contact: oncall-data@contoso.com | Notification: 5/5 (FINAL)\n\n"
                "Hi IT,\n\n"
                "The on-call team forwarded these alerts to us. The /data volume on "
                "db-prod-03 is nearly full and it's our production PostgreSQL server. "
                "If it fills up completely the database will crash. Please investigate "
                "urgently.\n\n"
                "— Operations team"
            ),
            category=Category.DATA_STORAGE,
            priority=Priority.P1,
            team=Team.DATA_PLATFORM,
            needs_escalation=True,
            missing_info=[],
            next_best_action=(
                "URGENT: /data volume on db-prod-03 (production PostgreSQL) is at 99% "
                "(475/476GB) and has been filling steadily since 02:15 UTC. Immediate "
                "action needed to prevent database crash from disk exhaustion."
            ),
            remediation_steps=[
                "Immediately check current disk usage on db-prod-03 /data volume.",
                "Identify the largest consumers — check for WAL file accumulation, old backups, or temp files.",
                "Clear any safe-to-delete files (old WAL segments, pg_dump temp files) to buy time.",
                "Expand the /data volume or add additional storage if on cloud/SAN.",
                "Investigate the root cause of rapid disk growth and set up proactive alerts at 85%.",
            ],
            reporter_name="Operations Team",
            reporter_email="ops-team@contoso.com",
            reporter_department="Operations",
            channel=Channel.EMAIL,
            tags=["data-cleanup", "monitoring-alerts", "alert-flood"],
            difficulty="hard",
        ),
        # ── DC-025  Reply-all chain with massive CC list and headers ─────────
        ScenarioDefinition(
            scenario_id="DC-025",
            subject="RE: RE: RE: RE: ALL-HANDS: Office printer toner replacement",
            description=(
                "To: IT Support <itsupport@contoso.com>\n"
                "CC: john.smith@contoso.com; jane.doe@contoso.com; mike.jones@contoso.com; "
                "sarah.wilson@contoso.com; david.brown@contoso.com; lisa.taylor@contoso.com; "
                "james.anderson@contoso.com; mary.thomas@contoso.com; robert.jackson@contoso.com; "
                "patricia.white@contoso.com; christopher.harris@contoso.com; linda.martin@contoso.com; "
                "daniel.garcia@contoso.com; nancy.martinez@contoso.com; matthew.robinson@contoso.com; "
                "betty.clark@contoso.com; anthony.rodriguez@contoso.com; margaret.lewis@contoso.com; "
                "mark.lee@contoso.com; dorothy.walker@contoso.com; steven.hall@contoso.com; "
                "elizabeth.allen@contoso.com; paul.young@contoso.com; jennifer.king@contoso.com; "
                "andrew.wright@contoso.com; barbara.scott@contoso.com; joshua.green@contoso.com; "
                "susan.adams@contoso.com; kenneth.baker@contoso.com; helen.nelson@contoso.com; "
                "kevin.hill@contoso.com; donna.ramirez@contoso.com; brian.campbell@contoso.com; "
                "carol.mitchell@contoso.com; george.roberts@contoso.com; ruth.carter@contoso.com; "
                "edward.phillips@contoso.com; sharon.evans@contoso.com; ronald.turner@contoso.com; "
                "michelle.torres@contoso.com; all-floor7@contoso.com; all-floor8@contoso.com; "
                "all-building2@contoso.com\n\n"
                "--- Reply from Ruth Carter ---\n"
                "Please stop replying all! My inbox is flooded!\n\n"
                "--- Reply from Ronald Turner ---\n"
                "Unsubscribe\n\n"
                "--- Reply from Edward Phillips ---\n"
                "+1 to Ruth, please use reply not reply-all\n\n"
                "--- Reply from George Roberts ---\n"
                "Can someone remove me from this thread?\n\n"
                "--- Reply from Carol Mitchell ---\n"
                "STOP REPLYING ALL!!!\n\n"
                "--- Original Message ---\n"
                "From: Kevin Hill <kevin.hill@contoso.com>\n"
                "To: IT Support; all-floor7; all-floor8; all-building2\n"
                "Subject: Office printer toner replacement\n\n"
                "Hi IT,\n\n"
                "The large MFP printer on Floor 7 (Canon imageRUNNER ADVANCE C5560i, "
                "asset tag BLD2-PRN-0012) is printing with faded streaks — I think the "
                "cyan toner is running low. Can you send a replacement cartridge?\n\n"
                "Kevin Hill\nAsset Management, Building 2, Floor 7"
            ),
            category=Category.HARDWARE,
            priority=Priority.P4,
            team=Team.ENDPOINT,
            needs_escalation=False,
            missing_info=[],
            next_best_action=(
                "Order replacement cyan toner cartridge for Canon imageRUNNER ADVANCE "
                "C5560i (BLD2-PRN-0012) on Floor 7, Building 2. Faded streaks indicate "
                "low toner. Ignore the reply-all noise."
            ),
            remediation_steps=[
                "Check the printer's built-in supply status page for toner levels.",
                "Order a replacement Canon C-EXV51 cyan toner cartridge.",
                "Dispatch a technician to replace the toner and clean the drum unit if needed.",
                "Print a test page after replacement to verify streak-free output.",
                "Advise the original sender to use targeted distribution lists in the future.",
            ],
            reporter_name="Kevin Hill",
            reporter_email="kevin.hill@contoso.com",
            reporter_department="Asset Management",
            channel=Channel.EMAIL,
            tags=["data-cleanup", "reply-all-storm", "massive-cc-list"],
            difficulty="hard",
        ),
        # ── DC-026  OCR-extracted text from scanned document ─────────────────
        ScenarioDefinition(
            scenario_id="DC-026",
            subject="Scanned error message from kiosk — OCR text below",
            description=(
                "Hi IT,\n\n"
                "The lobby kiosk is showing an error. I took a photo and ran OCR on it "
                "since I couldn't copy-paste. Here's what I got:\n\n"
                "Wiridows Errar\n"
                "A prOblem has been detectad and Windows h4s been\n"
                "shut dawri to prevEnt damaGe to y0ur comput3r.\n\n"
                "IRQL_NOT_L3SS_OR_EQUAI.\n\n"
                "lf this ls the flrst tirne you've se€n this\n"
                "St0p error scre8n, r3start your c0mputer. lf\n"
                "this scr€en app8ars ag4in, foIIow th3se steps:\n\n"
                "Ch3ck to mak€ sure any n3w hardwar€ 0r softwar3\n"
                "is prop€rly instaIl3d. lf this is a n3w\n"
                "installati0n, ask your h4rdware or s0ftware\n"
                "manufactur3r f0r any Wlndows updat3s you might\n"
                "n3ed.\n\n"
                "T3chnical lnformation:\n"
                "*** ST0P: 0x0000000A (0x000O0028, 0x00000002,\n"
                "0x00000001, Oxid3ntlfy)\n\n"
                "The kiosk is in the main lobby, Building 1. It's the visitor check-in "
                "terminal. This is blocking all guest sign-ins today.\n\n"
                "— Reception team"
            ),
            category=Category.HARDWARE,
            priority=Priority.P2,
            team=Team.ENDPOINT,
            needs_escalation=False,
            missing_info=[MissingInfo.DEVICE_INFO],
            next_best_action=(
                "Investigate BSOD (IRQL_NOT_LESS_OR_EQUAL) on lobby visitor check-in "
                "kiosk in Building 1 — likely a driver or memory issue. Kiosk is "
                "blocking all guest sign-ins."
            ),
            remediation_steps=[
                "Dispatch a technician to the lobby kiosk to perform a hard restart.",
                "Check the Windows Event Viewer for the IRQL_NOT_LESS_OR_EQUAL crash dump.",
                "Inspect recently installed drivers or updates that may have caused the BSOD.",
                "Run Windows Memory Diagnostic to check for faulty RAM.",
                "If recurring, re-image the kiosk from the standard kiosk deployment image.",
            ],
            reporter_name="Reception Team",
            reporter_email="reception@contoso.com",
            reporter_department="Facilities",
            channel=Channel.PHONE,
            tags=["data-cleanup", "ocr-noise", "garbled-text"],
            difficulty="hard",
        ),
        # ── DC-027  Minified JavaScript / CSS pasted as error context ────────
        ScenarioDefinition(
            scenario_id="DC-027",
            subject="Internal portal showing blank page — console errors",
            description=(
                "Hi IT,\n\n"
                "Our internal benefits portal (https://benefits.contoso.com) is showing "
                "a completely blank white page. I opened the browser console and this is "
                "what I see:\n\n"
                "Uncaught TypeError: Cannot read properties of undefined (reading 'map')\n"
                "    at Object.render (app.min.js:1:28847)\n\n"
                "The minified source at that location is:\n"
                '!function(e){"use strict";var t=function(e,t){return e.filter(function(e){return'
                " t.indexOf(e.id)>-1})},n=function(e){return e.benefits.map(function(e){return{"
                "id:e.id,name:e.name,enrolled:e.enrolled,deductible:e.deductible,copay:e.copay,"
                "premium:e.premium,provider:e.provider,effectiveDate:e.effectiveDate,status:e."
                "status}})},r=function(e,t){var n=e.querySelector(t);return n?n.textContent:"
                '""},o=function(e){var t=document.createElement("div");t.className="benefit-card'
                ' "+e.status;var n=document.createElement("h3");n.textContent=e.name;var r='
                'document.createElement("p");r.textContent="Premium: $"+e.premium+"/mo";var o='
                'document.createElement("p");o.textContent="Deductible: $"+e.deductible;var i='
                'document.createElement("span");i.className="status-badge "+e.status;i.textContent='
                "e.status;t.appendChild(n);t.appendChild(r);t.appendChild(o);t.appendChild(i);"
                'return t};e.init=function(){var e=document.getElementById("benefits-root");'
                'fetch("/api/benefits").then(function(e){return e.json()}).then(function(t){'
                "var r=n(t);r.forEach(function(t){e.appendChild(o(t))})}).catch(function(e){"
                'console.error("Failed to load benefits:",e)})}}(window.BenefitsApp=window.'
                "BenefitsApp||{});\n\n"
                "This started after the maintenance window last night. All browsers "
                "affected (Edge, Chrome). The API endpoint /api/benefits returns a 200 "
                "but the response body is empty.\n\n"
                "— HR portal admin"
            ),
            category=Category.SOFTWARE,
            priority=Priority.P2,
            team=Team.ENTERPRISE_APPS,
            needs_escalation=False,
            missing_info=[MissingInfo.ENVIRONMENT_DETAILS],
            next_best_action=(
                "Investigate benefits portal blank page — the /api/benefits endpoint "
                "returns empty body (200 OK), causing a TypeError when the frontend "
                "tries to map over undefined benefits array. Likely a backend deployment "
                "or database connectivity issue from last night's maintenance."
            ),
            remediation_steps=[
                "Check the backend service for /api/benefits — verify database connectivity.",
                "Review last night's maintenance changes for anything affecting the benefits API.",
                "Check application logs for errors in the benefits data retrieval path.",
                "If the database is accessible, verify the benefits table has data and is not truncated.",
                "Roll back the maintenance change if it caused the API regression.",
            ],
            reporter_name="HR Portal Admin",
            reporter_email="hr-portal-admin@contoso.com",
            reporter_department="HR",
            channel=Channel.PORTAL,
            tags=["data-cleanup", "minified-code", "inline-code"],
            difficulty="hard",
        ),
        # ── DC-028  Multi-part MIME email with mixed content ─────────────────
        ScenarioDefinition(
            scenario_id="DC-028",
            subject="Badge reader not working — MIME-encoded email follows",
            description=(
                'Content-Type: multipart/mixed; boundary="----=_Part_8847_1302567890"\n'
                "MIME-Version: 1.0\n"
                "X-Mailer: Lotus Notes 9.0.1\n"
                "X-MimeOLE: Produced By Microsoft MimeOLE V6.3.9600.20091\n\n"
                "------=_Part_8847_1302567890\n"
                "Content-Type: text/plain; charset=UTF-8\n"
                "Content-Transfer-Encoding: quoted-printable\n\n"
                "Hi IT,\n\n"
                "The badge reader at the Building 4 parking garage entrance (Gate B) "
                "stopped working this morning around 7:30 AM. Employees are having to =\n"
                "wait for security to manually open the gate, causing a 20-minute backup =\n"
                "during morning rush.\n\n"
                "The reader's LED is solid red instead of the normal blinking green.=20\n"
                "Badge number on the reader unit: BDG-PK-0044.\n\n"
                "=E2=80=94 Facilities team\n\n"
                "------=_Part_8847_1302567890\n"
                "Content-Type: text/html; charset=UTF-8\n"
                "Content-Transfer-Encoding: quoted-printable\n\n"
                "<html><body>\n"
                "<p>Hi IT,</p>\n"
                "<p>The badge reader at the <b>Building 4 parking garage entrance</b>=\n"
                " (Gate B) stopped working this morning around 7:30 AM. Employees are=\n"
                " having to wait for security to manually open the gate, causing a=\n"
                ' <span style=3D"color:red;font-weight:bold">20-minute backup</span>=\n'
                " during morning rush.</p>\n"
                "<p>The reader=E2=80=99s LED is solid red instead of the normal blinking=\n"
                " green. Badge number on the reader unit: <code>BDG-PK-0044</code>.</p>\n"
                "<p>=E2=80=94 Facilities team</p>\n"
                "</body></html>\n\n"
                "------=_Part_8847_1302567890\n"
                'Content-Type: image/jpeg; name="badge_reader_photo.jpg"\n'
                "Content-Transfer-Encoding: base64\n"
                'Content-Disposition: attachment; filename="badge_reader_photo.jpg"\n\n'
                "/9j/4AAQSkZJRgABAQEASABIAAD/2wBDABALDA4MChAODQ4SERATGCgaGBYWGDEjJR0oOjM9\n"
                "PDkzODdASFxOQERXRTc4UG1RV19iZ2hnPk1xeXBkeFxlZ2f/wAALCABAAEABAREA/8QAHwAA\n"
                "AQUBAQEBAQEAAAAAAAAAAAECAwQFBgcICQoL/8QAtRAAAgEDAwIEAwUF\n\n"
                "------=_Part_8847_1302567890--"
            ),
            category=Category.HARDWARE,
            priority=Priority.P2,
            team=Team.ENDPOINT,
            needs_escalation=False,
            missing_info=[],
            next_best_action=(
                "Dispatch technician to repair badge reader BDG-PK-0044 at Building 4 "
                "parking garage Gate B — LED showing solid red since 7:30 AM, causing "
                "20-minute entry delays. Reader may need power cycle or replacement."
            ),
            remediation_steps=[
                "Dispatch facilities/endpoint technician to Gate B, Building 4 parking garage.",
                "Attempt a power cycle of badge reader BDG-PK-0044.",
                "Check the reader's network connection to the access control server.",
                "If power cycle fails, replace the reader unit with a spare from inventory.",
                "Verify badge access works after repair and clear any entry queue.",
            ],
            reporter_name="Facilities Team",
            reporter_email="facilities@contoso.com",
            reporter_department="Facilities",
            channel=Channel.EMAIL,
            tags=["data-cleanup", "mime-encoded", "multi-part-email"],
            difficulty="hard",
        ),
        # ── DC-029  Extremely long single-line email (no line breaks) ────────
        ScenarioDefinition(
            scenario_id="DC-029",
            subject="URGENT: laptop wont turn on at all completely dead",
            description=(
                "hi IT my laptop is completely dead it wont turn on at all i've tried "
                "holding the power button for 30 seconds and nothing happens the charging "
                "light isnt coming on either i tried a different charger from my colleague "
                "and still nothing i have a really important client presentation in 2 hours "
                "and all my slides are on this laptop i saved them locally because i was "
                "working on the plane yesterday and didnt have wifi to sync to onedrive i "
                "know i shouldve saved to the cloud but i didnt and now im panicking the "
                "laptop is a lenovo thinkpad x1 carbon gen 11 and its only about 6 months "
                "old so it shouldnt be dying already i think the battery might be completely "
                "drained because i left it in my bag overnight with the lid open and it "
                "might have been running all night but even plugged in it shows absolutely "
                "nothing no lights no fan noise no screen flicker nothing at all its like "
                "its a brick i tried the paper clip reset hole on the bottom too and that "
                "didnt help either my employee id is E-20145 and im on the 4th floor of "
                "building 2 in the london office can someone please come help me or give "
                "me a loaner laptop so i can at least pull my slides from the local backup "
                "i desperately need this resolved in the next hour"
            ),
            category=Category.HARDWARE,
            priority=Priority.P2,
            team=Team.ENDPOINT,
            needs_escalation=False,
            missing_info=[MissingInfo.DEVICE_INFO],
            next_best_action=(
                "Urgent: Lenovo ThinkPad X1 Carbon Gen 11 completely unresponsive for "
                "employee E-20145 on 4th floor, Building 2, London. User has client "
                "presentation in 2 hours with locally-stored slides. Prioritize loaner "
                "device and data recovery."
            ),
            remediation_steps=[
                "Immediately dispatch a loaner laptop to the user's location (4th floor, Building 2, London).",
                "Attempt to recover the dead ThinkPad — try a full battery disconnect/reconnect reset.",
                "If the laptop powers on, help the user sync the presentation files to OneDrive.",
                "If unrecoverable, pull the NVMe SSD and mount it externally to retrieve the slides.",
                "Log a warranty claim for the ThinkPad X1 Carbon if it is confirmed dead.",
            ],
            reporter_name="Oliver Smythe",
            reporter_email="oliver.smythe@contoso.com",
            reporter_department="Private Banking",
            channel=Channel.CHAT,
            tags=["data-cleanup", "no-linebreaks", "stream-of-consciousness"],
            difficulty="hard",
        ),
        # ── DC-030  Base64 image flood interleaved with real content ─────────
        ScenarioDefinition(
            scenario_id="DC-030",
            subject="Multiple monitor setup not working — inline photos",
            description=(
                "Hi IT,\n\n"
                "I just moved to a new desk and I can't get my triple monitor setup "
                "working. Here's a photo of how the cables are connected:\n\n"
                "[Photo 1 — rear of dock]\n"
                "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEASABIAAD/2wBDAAgGBgcGBQgHBwcJCQ"
                "gKDBQNDAsLDBkSEw8UHRofHh0aHBwgJC4nICIsIxwcKDcpLDAxNDQ0Hyc5PTgyPC4zNDL/2w"
                "BDAQkJCQwLDBgNDRgyIRwhMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIy"
                "MjIyMjIyMjIyMjIyMjL/wAARCAAoACgDASIAAhEBAxEB/8QAHwAAAQUBAQEBAQEAAAAAAAAA"
                "AAECAwQFBgcICQoL/8QAtRAAAgEDAwIEAwUFBAQAAAF9AQIDAAQRBRIhMUEGE1FhByJxFDKBka"
                "EII0KxwRVS0fAkM2JyggkKFhcYGRolJicoKSo0NTY3ODk6Q0RFRkdISUpTVFVWV1hZWmNkZW"
                "ZnaGlqc3R1dnd4eXqDhIWGh4iJipKTlJWWl5iZmqKjpKWmp6ipqrKztLW2t7i5usLDxMXGx8"
                "jJytLT1NXW19jZ2uHi4+Tl5ufo6erx8vP09fb3+Pn6/8QAHwEAAwEBAQEBAQEBAQAAAAAAAA"
                "ECAwQFBgcICQoL/8QAtREAAgECBAQDBAcFBAQAAQJ3AAECAxEEBSExBhJBUQdhcRMiMoEIFEKR"
                "\n\n"
                "The dock is a Lenovo ThinkPad USB-C Dock Gen 2 (40AS). I have three "
                "Dell U2722D monitors connected via:\n"
                "- Monitor 1: DisplayPort from dock (works)\n"
                "- Monitor 2: HDMI from dock (shows 'No Signal')\n"
                "- Monitor 3: USB-C to DisplayPort adapter from laptop directly (flickering)\n\n"
                "[Photo 2 — monitor 2 showing no signal]\n"
                "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw4pVUAAAABmJLR0"
                "QA/wD/AP+gvaeTAAAACXBIWXMAAAsTAAALEwEAmpwYAAAAB3RJTUUH6QMRDhQHLFcKRgAAAB1p"
                "VFh0Q29tbWVudAAAAAAAQ3JlYXRlZCB3aXRoIEdJTVBkLmUHAAABKUlEQVR42u3bMQ6DMBCF"
                "Ye5/aaogRaJCwmDPjP2eRKfA/NiLvQAAAAAAAAAAAACwm+OqF3Ye55ev/fx73xvXdzj5d/Fz"
                "1j78vOr5bfn61nXf4/ct77v6e13H8fWt51v1HHa5hrOfc8Xz3v39r3w9q+6/1f1fcV1XvL7V"
                "\n\n"
                "[Photo 3 — monitor 3 flickering]\n"
                "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEASABIAAD/4gHYSUNDX1BST0ZJTEUAAQEAAAdI"
                "bGludQIQAABtbnRyUkdCIFhZWiAH4gACAAkABgAxAABhY3NwTVNGVAAAAABJRUMgc1JHQgAAAA"
                "AAAAAAAAAAAPbWAAEAAAAA0y1obGlubAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
                "AAAAAAAAAAAAAAAAAAARY3BydAAAAbAAAAA2d3RwdAAAAagAAAAUZGVzYwAAAcgAAAAwAAAAAAAA"
                "\n\n"
                "I've tried updating the dock firmware and the Intel graphics driver "
                "(version 31.0.101.5186) but no change. My laptop is a ThinkPad T14s "
                "Gen 4 running Windows 11 23H2.\n\n"
                "— Yuki Tanaka, Fixed Income, Building 3, 8th floor, Singapore"
            ),
            category=Category.HARDWARE,
            priority=Priority.P3,
            team=Team.ENDPOINT,
            needs_escalation=False,
            missing_info=[MissingInfo.ERROR_MESSAGE],
            next_best_action=(
                "Troubleshoot triple-monitor setup with Lenovo ThinkPad USB-C Dock Gen 2 "
                "— Monitor 2 (HDMI) shows no signal, Monitor 3 (USB-C adapter) is "
                "flickering. Likely a dock bandwidth or DisplayLink driver limitation "
                "with three 2560x1440 monitors."
            ),
            remediation_steps=[
                "Check if the dock firmware supports three simultaneous displays at 2560x1440.",
                "Verify the HDMI port on the dock is functional by testing with a known-good cable/monitor.",
                "Replace the USB-C to DisplayPort adapter for Monitor 3 with a certified one.",
                "Check if MST (Multi-Stream Transport) daisy-chaining could reduce dock port usage.",
                "If the dock cannot support three QHD monitors, consider a DisplayLink USB adapter for the third.",
            ],
            reporter_name="Yuki Tanaka",
            reporter_email="yuki.tanaka@contoso.com",
            reporter_department="Fixed Income",
            channel=Channel.PORTAL,
            tags=["data-cleanup", "base64", "interleaved-images", "inline-image"],
            difficulty="hard",
        ),
        # ── DC-031  RTF / Rich Text formatting markup noise ─────────────
        ScenarioDefinition(
            scenario_id="DC-031",
            subject="Network drive mapping failure - cannot access \\\\fs-compliance-01\\shared",
            description=(
                "{\\rtf1\\ansi\\ansicpg1252\\deff0\\nouicompat{\\fonttbl{\\f0\\fswiss\\fcharset0 "
                "Calibri;}{\\f1\\fnil\\fcharset2 Symbol;}}\n"
                "{\\colortbl ;\\red0\\green0\\blue0;\\red44\\green62\\blue80;}\n"
                "{\\*\\generator Riched20 10.0.22621}\\viewkind4\\uc1\n"
                "\\pard\\sl276\\slmult1\\cf1\\f0\\fs22 Hi Support Team,\\par\n"
                "\\par\n"
                "\\b Problem Description:\\b0\\par\n"
                "I am unable to map the network drive \\\\\\\\fs-compliance-01\\\\shared on my "
                "workstation since this morning.  When I try to reconnect the mapped drive "
                "through \\cf2\\ul File Explorer > Map Network Drive\\cf1\\ulnone , I receive a "
                "generic Windows error and the connection times out after roughly 30 seconds.\\par\n"
                "\\par\n"
                "\\b Steps I have already tried:\\b0\\par\n"
                "{\\pntext\\f1\\'B7\\tab}{\\*\\pn\\pnlvlblt\\pnf1\\pnindent360{\\pntxtb\\'B7}}"
                "\\fi-360\\li720 Rebooted the workstation twice\\par\n"
                "{\\pntext\\f1\\'B7\\tab}Cleared the Windows credential cache via "
                "\\f0\\fs18 cmdkey /delete:fs-compliance-01\\f0\\fs22\\par\n"
                "{\\pntext\\f1\\'B7\\tab}Ran \\f0\\fs18 net use \\\\\\\\fs-compliance-01\\\\shared "
                "/user:CONTOSO\\\\amoretti P@ss\\f0\\fs22  — same timeout\\par\n"
                "{\\pntext\\f1\\'B7\\tab}Pinged fs-compliance-01 — responds with 10.42.7.20, "
                "avg 2 ms\\par\n"
                "\\par\n"
                "\\b Impact:\\b0  I cannot access any of the shared compliance audit files "
                "and have a regulatory filing due by end of day Friday.\\par\n"
                "\\par\n"
                "Please advise urgently.\\par\n"
                "\\par\n"
                "\\i Angela Moretti\\i0\\par\n"
                "Compliance Department | Desk 4-118 | Ext. 7742\\par\n"
                "}\n"
            ),
            category=Category.DATA_STORAGE,
            priority=Priority.P2,
            team=Team.DATA_PLATFORM,
            needs_escalation=False,
            missing_info=[MissingInfo.AFFECTED_SYSTEM, MissingInfo.ERROR_MESSAGE],
            next_best_action=(
                "Investigate network drive mapping failure for \\\\fs-compliance-01\\shared — "
                "user receives a timeout after 30 seconds despite the server responding to "
                "ping.  Strip RTF formatting noise to extract the core issue, then check "
                "SMB connectivity and credential cache state."
            ),
            remediation_steps=[
                "Verify SMB connectivity to fs-compliance-01 on port 445 from the user's subnet.",
                "Check if the user's AD computer account has valid Kerberos tickets for the file server.",
                "Confirm the shared folder permissions on fs-compliance-01 include the Compliance group.",
                "Review recent Group Policy changes that may have altered drive-mapping logon scripts.",
                "If SMB signing or encryption policies changed, ensure client and server negotiate the same version.",
            ],
            reporter_name="Angela Moretti",
            reporter_email="angela.moretti@contoso.com",
            reporter_department="Compliance",
            channel=Channel.EMAIL,
            tags=["data-cleanup", "rtf-markup", "formatting-noise"],
            difficulty="hard",
        ),
        # ── DC-032  Email reply chain with conflicting information ───────
        ScenarioDefinition(
            scenario_id="DC-032",
            subject="Re: Re: FW: Multiple IT issues - VPN / printer / password",
            description=(
                "From: Tomás Reyes <tomas.reyes@contoso.com>\n"
                "Sent: Wednesday, April 2, 2026 3:18 PM\n"
                "To: IT Support <it.support@contoso.com>\n\n"
                "Hi team — sorry for all the back-and-forth.  Please DISREGARD the VPN and "
                "printer issues from my earlier emails, those were resolved by a colleague.\n\n"
                "My ACTUAL current problem: I cannot reset my Active Directory password.  "
                "When I go to https://passwordreset.contoso.com and enter my username "
                "(treyes), the MFA challenge never arrives on my phone.  I have tried both "
                "SMS and the Authenticator app push notification — neither comes through.  "
                "My account is not locked (I can still log in with my current password) but "
                "it expires tomorrow and I will be locked out of all trading systems.\n\n"
                "Please help ASAP.\n"
                "Tomás\n\n"
                "────────────────────────────────────────\n"
                "From: Tomás Reyes <tomas.reyes@contoso.com>\n"
                "Sent: Wednesday, April 2, 2026 1:45 PM\n"
                "To: IT Support <it.support@contoso.com>\n\n"
                "Update — the VPN issue fixed itself after the network team rebooted the "
                "concentrator, but now the 4th-floor color printer (HP LaserJet MFP E877) "
                "is jammed and showing error code 13.A3.D4 on the display panel.  Can "
                "someone come take a look?  Also I still need to reset my password before "
                "tomorrow.\n\n"
                "────────────────────────────────────────\n"
                "From: Tomás Reyes <tomas.reyes@contoso.com>\n"
                "Sent: Wednesday, April 2, 2026 9:02 AM\n"
                "To: IT Support <it.support@contoso.com>\n\n"
                "Good morning, I'm having trouble connecting to the Contoso VPN from my "
                "home office.  The Cisco AnyConnect client shows 'Connection attempt has "
                "failed' after entering my credentials.  I'm on Comcast residential, if "
                "that matters.  I also need a password reset but the VPN thing is more "
                "urgent right now.\n"
            ),
            category=Category.ACCESS_AUTH,
            priority=Priority.P3,
            team=Team.IAM,
            needs_escalation=False,
            missing_info=[MissingInfo.AUTHENTICATION_METHOD],
            next_best_action=(
                "Process password reset for treyes — user reports that the self-service "
                "password reset MFA challenge (SMS and Authenticator push) is not arriving, "
                "and the current password expires tomorrow.  Ignore earlier VPN and printer "
                "issues which the user confirmed are resolved."
            ),
            remediation_steps=[
                "Verify the user's MFA registration in Azure AD — confirm phone number and Authenticator device.",
                "Check Azure MFA service health for any delivery delays on SMS or push notifications.",
                "If MFA is unreachable, perform an admin-assisted password reset with temp password; force change.",
                "Re-register the user's MFA methods if the Authenticator token has drifted or phone number changed.",
                "Extend the password expiry by 48 hours if the reset cannot be completed before end of day.",
            ],
            reporter_name="Tomás Reyes",
            reporter_email="tomas.reyes@contoso.com",
            reporter_department="Trading",
            channel=Channel.EMAIL,
            tags=["data-cleanup", "conflicting-replies", "reply-chain"],
            difficulty="hard",
        ),
        # ── DC-033  Raw Prometheus / Grafana metrics dump ────────────────
        ScenarioDefinition(
            scenario_id="DC-033",
            subject="URGENT — db-analytics-07 disk space critical",
            description=(
                "Here is the data from our Grafana dashboard for the last 6 hours.  "
                "I exported the raw Prometheus metrics so you can see the trend:\n\n"
                "# HELP node_cpu_seconds_total Seconds the CPUs spent in each mode.\n"
                "# TYPE node_cpu_seconds_total counter\n"
                "node_cpu_seconds_total{cpu=\"0\",mode=\"idle\"} 1.84629837e+06\n"
                "node_cpu_seconds_total{cpu=\"0\",mode=\"system\"} 42871.23\n"
                "node_cpu_seconds_total{cpu=\"0\",mode=\"user\"} 318744.91\n"
                "node_cpu_seconds_total{cpu=\"1\",mode=\"idle\"} 1.83998241e+06\n"
                "node_cpu_seconds_total{cpu=\"1\",mode=\"system\"} 44102.67\n"
                "node_cpu_seconds_total{cpu=\"1\",mode=\"user\"} 321556.88\n"
                "# HELP node_memory_MemTotal_bytes Total memory in bytes.\n"
                "node_memory_MemTotal_bytes 6.7479674880e+10\n"
                "node_memory_MemAvailable_bytes 4.129587200e+09\n"
                "node_memory_Buffers_bytes 2.18390528e+08\n"
                "node_memory_Cached_bytes 1.2884901888e+10\n"
                "# HELP node_disk_io_time_seconds_total Total seconds spent doing I/Os.\n"
                "node_disk_io_time_seconds_total{device=\"sda\"} 98712.44\n"
                "node_disk_io_time_seconds_total{device=\"sdb\"} 341289.71\n"
                "node_disk_io_time_seconds_total{device=\"sdc\"} 2187.03\n"
                "# HELP node_filesystem_avail_bytes Available filesystem size in bytes.\n"
                "node_filesystem_avail_bytes{device=\"/dev/sda1\",mountpoint=\"/\"} 8.1289175040e+09\n"
                "node_filesystem_avail_bytes{device=\"/dev/sdb1\",mountpoint=\"/data\"} 1.048576e+07\n"
                "node_filesystem_size_bytes{device=\"/dev/sdb1\",mountpoint=\"/data\"} 1.073741824e+12\n"
                "node_filesystem_avail_bytes{device=\"/dev/sdc1\",mountpoint=\"/backup\"} 4.29496729e+11\n"
                "# HELP node_disk_read_bytes_total Total number of bytes read.\n"
                "node_disk_read_bytes_total{device=\"sda\"} 5.8100735e+10\n"
                "node_disk_read_bytes_total{device=\"sdb\"} 9.7821548134e+11\n"
                "node_disk_written_bytes_total{device=\"sdb\"} 1.06889410765e+12\n\n"
                "As you can see /data on sdb1 has only ~10 MB free out of 1 TB.  The "
                "database server db-analytics-07 is about to run out of disk and the "
                "analytics pipeline will halt.  We need emergency cleanup or a volume "
                "expansion ASAP before the overnight batch job kicks off at 02:00 UTC."
            ),
            category=Category.DATA_STORAGE,
            priority=Priority.P1,
            team=Team.DATA_PLATFORM,
            needs_escalation=True,
            missing_info=[MissingInfo.AFFECTED_USERS, MissingInfo.BUSINESS_IMPACT],
            next_best_action=(
                "URGENT — db-analytics-07 /data volume is nearly full (~10 MB free of 1 TB).  "
                "Expand the volume or purge stale data before the 02:00 UTC batch job.  "
                "Ignore the large Prometheus metrics dump and focus on the disk-space issue."
            ),
            remediation_steps=[
                "SSH into db-analytics-07 and confirm current disk usage with df -h /data.",
                "Identify and remove or archive old analytics temp files under /data/tmp and /data/staging.",
                "If immediate space cannot be freed, expand the /dev/sdb1 volume via the storage array or cloud.",
                "Notify the Data Engineering team to delay the 02:00 UTC batch job until disk space is safe.",
                "Set up a Prometheus alert for node_filesystem_avail_bytes < 5% to catch this earlier in future.",
            ],
            reporter_name="Priyanka Sharma",
            reporter_email="priyanka.sharma@contoso.com",
            reporter_department="Data Engineering",
            channel=Channel.PORTAL,
            tags=["data-cleanup", "monitoring-metrics", "time-series-dump"],
            difficulty="hard",
        ),
        # ── DC-034  PDF-to-text conversion artifacts ─────────────────────
        ScenarioDefinition(
            scenario_id="DC-034",
            subject="Software license expiration — Bloomberg Terminal B-PIPE",
            description=(
                "C o n t o s o   F i n a n c i a l   S e r v i c e s        Page 1 of 3\n"
                "─────────────────────────────────────────────────────────────\n"
                "IT  Ser vice  Reques t  For m        Date:  03 / 28 / 2026\n"
                "─────────────────────────────────────────────────────────────\n\n"
                "Reques tor :   Kwame  Asan te        Dep t:  Ri sk  Managemen t\n"
                "Ext :  6 6 1 4        Fl oor :  12        Buil ding :  HQ - Eas t\n\n"
                "Cate gory :  So f tware  License  Renewal\n"
                "Priori ty :  Medium\n\n"
                "Descri p tion :\n"
                "Our  Bl oomberg  Terminal  B-PIPE  da ta  f eed  license  is  set  to  "
                "expi re  on  Apri l  15 ,  2026.   We  cur ren tly  have  8  concurren t  "
                "sea ts  and  need  to  renew  f or  at  leas t  12  sea ts  to  cover  the  "
                "new  hi res  in  Ri sk  and  Por t f olio  Managemen t.\n\n"
                "C o n t o s o   F i n a n c i a l   S e r v i c e s        Page 2 of 3\n"
                "─────────────────────────────────────────────────────────────\n\n"
                "The  cur ren t  con t rac t  number  is  BB - ENT - 2024 - 04871  and  our  "
                "accoun t  manager  at  Bl oomberg  is  Sarah  Chen  ( schen@bloomberg.ne t ) .  "
                "I  have  a t tached  the  origi nal  order  f orm  ( PDF )  bu t  the  "
                "a t tachmen t  may  no t  have  come  through  proper ly.\n\n"
                "Addi tional  no tes :\n"
                "- The  f i  ligature  in  ' fi nancial '  renders  as  separ ate  chars\n"
                "- Head ers  and  f oo ters  repea t  on  every  page  due  to  PDF  extrac tion\n"
                "- Page  numbers  are  in tersp ersed  in  the  tex t  s tream\n\n"
                "C o n t o s o   F i n a n c i a l   S e r v i c e s        Page 3 of 3\n"
                "─────────────────────────────────────────────────────────────\n\n"
                "Please  process  this  renewal  be f ore  Apri l  10  to  avoi d  any  "
                "in terrup tion  in  ser vice.   The  cos t  cen ter  is  CC - 4420 - RM.\n\n"
                "Than k  you ,\n"
                "Kwame  Asan te"
            ),
            category=Category.SOFTWARE,
            priority=Priority.P3,
            team=Team.ENTERPRISE_APPS,
            needs_escalation=False,
            missing_info=[MissingInfo.APPLICATION_VERSION],
            next_best_action=(
                "Renew Bloomberg Terminal B-PIPE license (contract BB-ENT-2024-04871) "
                "before April 15, 2026 — expand from 8 to 12 concurrent seats.  Contact "
                "Bloomberg account manager Sarah Chen.  Ignore PDF-to-text conversion "
                "artifacts (broken ligatures, repeated headers/footers, page numbers)."
            ),
            remediation_steps=[
                "Contact Bloomberg account manager Sarah Chen to initiate renewal of contract BB-ENT-2024-04871.",
                "Confirm the seat count increase from 8 to 12 with the Risk Management budget owner.",
                "Obtain purchase approval for cost center CC-4420-RM and submit the PO before April 10.",
                "Coordinate with Enterprise Apps to provision the 4 additional B-PIPE seats once license is active.",
                "Update the software asset inventory with the new seat count and expiry date.",
            ],
            reporter_name="Kwame Asante",
            reporter_email="kwame.asante@contoso.com",
            reporter_department="Risk Management",
            channel=Channel.PORTAL,
            tags=["data-cleanup", "pdf-conversion", "ocr-artifacts"],
            difficulty="hard",
        ),
        # ── DC-035  Email with enormous CC/BCC list and auto-reply noise ─
        ScenarioDefinition(
            scenario_id="DC-035",
            subject="Re: Shared mailbox clientservices@ not receiving external emails",
            description=(
                "From: Nadia Volkov <nadia.volkov@contoso.com>\n"
                "To: IT Support <it.support@contoso.com>\n"
                "CC: james.wu@contoso.com; maria.gonzalez@contoso.com; "
                "ahmed.hassan@contoso.com; lisa.chen@contoso.com; "
                "robert.smith@contoso.com; patricia.jones@contoso.com; "
                "david.kim@contoso.com; sarah.taylor@contoso.com; "
                "michael.brown@contoso.com; jennifer.davis@contoso.com; "
                "christopher.wilson@contoso.com; amanda.martinez@contoso.com; "
                "daniel.anderson@contoso.com; jessica.thomas@contoso.com; "
                "matthew.jackson@contoso.com; ashley.white@contoso.com; "
                "joshua.harris@contoso.com; emily.clark@contoso.com; "
                "andrew.lewis@contoso.com; stephanie.walker@contoso.com; "
                "clientservices@contoso.com\n\n"
                "Hi IT,\n\n"
                "Our shared mailbox clientservices@contoso.com has stopped receiving "
                "emails from external senders.  Internal emails arrive fine.  We first "
                "noticed the problem sometime this week but are unsure of the exact time.  "
                "Our clients are complaining that their emails bounce with a '550 5.7.1 "
                "Unable to relay' NDR.  This is affecting multiple client relationships.\n\n"
                "Can someone investigate the Exchange transport rules or the inbound "
                "connector?  The mailbox has 47 members and we all see the same behaviour.\n\n"
                "Thanks,\nNadia\n\n"
                "--- Auto-reply from james.wu@contoso.com ---\n"
                "Thank you for your email.  I am currently out of the office from March 31 "
                "to April 7 with limited access to email.  For urgent matters please "
                "contact maria.gonzalez@contoso.com.\n\n"
                "--- Auto-reply from patricia.jones@contoso.com ---\n"
                "I am on parental leave until June 2026.  Please direct all Client "
                "Services inquiries to the clientservices@contoso.com shared mailbox or "
                "contact david.kim@contoso.com.\n\n"
                "--- Auto-reply from ashley.white@contoso.com ---\n"
                "Thanks for reaching out!  I'm in training all week and will respond when "
                "I return on April 8.  For immediate assistance email "
                "clientservices@contoso.com.\n\n"
                "--- Auto-reply from daniel.anderson@contoso.com ---\n"
                "I am out sick today.  I will reply as soon as I am able.\n"
            ),
            category=Category.SOFTWARE,
            priority=Priority.P2,
            team=Team.ENTERPRISE_APPS,
            needs_escalation=False,
            missing_info=[MissingInfo.TIMESTAMP, MissingInfo.AFFECTED_USERS],
            next_best_action=(
                "Investigate why the shared mailbox clientservices@contoso.com is rejecting "
                "external inbound email with '550 5.7.1 Unable to relay'.  Check Exchange "
                "transport rules and inbound connectors.  Ignore the large CC list and "
                "concatenated out-of-office auto-replies."
            ),
            remediation_steps=[
                "Check Exchange Online message trace for emails sent to clientservices@contoso.com in the last 7 days.",
                "Review inbound mail-flow connectors for changes that may block external relay to shared mailboxes.",
                "Inspect Exchange transport rules for any rule rejecting mail based on recipient type or origin.",
                "Verify that the shared mailbox has not exceeded its storage quota, which can cause inbound rejection.",
                "Once resolved, ask Nadia's team to confirm receipt of a test email from an external address.",
            ],
            reporter_name="Nadia Volkov",
            reporter_email="nadia.volkov@contoso.com",
            reporter_department="Client Services",
            channel=Channel.EMAIL,
            tags=["data-cleanup", "massive-cc-list", "auto-reply-noise"],
            difficulty="hard",
        ),
        # ── DC-036  Screenshot OCR with layout / table artifacts ─────────
        ScenarioDefinition(
            scenario_id="DC-036",
            subject="SAP transaction VA01 failing — screenshot attached",
            description=(
                "[OCR extracted text from screenshot — original image lost in transit]\n\n"
                "+---------------------+-------------------+--------------------+\n"
                "|  SAP  ECC  6.0      |   Tran  saction   |    VA 01           |\n"
                "+---------------------+-------------------+--------------------+\n"
                "|  Cli ent  :  800    |   Us er  :  HJO   |  Sys  :  PRD      |\n"
                "|                     |   HAN  SSON       |                    |\n"
                "+---------------------+-------------------+--------------------+\n\n"
                "Err or  Mes sage  (red  bar  at  bot tom  of  scr een):\n"
                "+----------------------------------------------------------+\n"
                "|  M7  021  :  \" Materi al  40 0 - 1 1 7  has  no t  been  |\n"
                "|  mai ntai ned  in  pla nt  21 00 \"                        |\n"
                "+----------------------------------------------------------+\n\n"
                "I  am  try ing  to  cre ate  a  sal es  ord er  in  VA 01  for\n"
                "mat eri al  40 0 - 1 1 7  (Wi dge t  Assembl y  Ki t  -  Lar ge)\n"
                "bu t  the  sys tem  thr ows  err or  M7  021  when  I  sel ect\n"
                "pla nt  21 00  ( Chi cago  Dist ribu tion  Cen ter ) .\n\n"
                "Thi s  mat eri al  was  wor king  fi ne  las t  wee k.   I  thi nk\n"
                "some one  may  have  dele ted  or  modi fi ed  the  mat eri al\n"
                "mas ter  reco rd  f or  pla nt  21 00  duri ng  the  week end\n"
                "main tenan ce  win dow.\n\n"
                "Hen ri k  Johann sson  |  Fin ance  |  Ext  48 81"
            ),
            category=Category.SOFTWARE,
            priority=Priority.P2,
            team=Team.ENTERPRISE_APPS,
            needs_escalation=False,
            missing_info=[MissingInfo.ERROR_MESSAGE, MissingInfo.STEPS_TO_REPRODUCE],
            next_best_action=(
                "Investigate SAP error M7 021 for material 400-117 in plant 2100 — the "
                "material master record may have been modified or deleted during the "
                "weekend maintenance window.  Restore or re-extend the material to plant "
                "2100 so sales order creation in VA01 works again."
            ),
            remediation_steps=[
                "Check material master for 400-117 in SAP transaction MM03 — verify plant 2100 view exists.",
                "Review the change log (CDHDR/CDPOS) for material 400-117 to identify recent modifications.",
                "If plant 2100 view was deleted, re-extend material using MM01 with sales, MRP, and purchasing views.",
                "Test sales order creation in VA01 with material 400-117 and plant 2100 to confirm the fix.",
                "Notify SAP Basis team to review weekend maintenance scripts that may have altered material masters.",
            ],
            reporter_name="Henrik Johansson",
            reporter_email="henrik.johansson@contoso.com",
            reporter_department="Finance",
            channel=Channel.PORTAL,
            tags=["data-cleanup", "ocr-layout", "table-artifacts"],
            difficulty="hard",
        ),
        # ── DC-037  Multiple inline base64-encoded non-image files ───────
        ScenarioDefinition(
            scenario_id="DC-037",
            subject="SharePoint upload failing — document too large",
            description=(
                "Hi IT Support,\n\n"
                "I have been trying to upload a regulatory filing bundle to our SharePoint "
                "site (https://contoso.sharepoint.com/sites/Legal/FilingArchive) but keep "
                "getting a 'File size exceeds the allowed limit' error.  The bundle is a "
                "ZIP file containing three documents that total about 380 MB.\n\n"
                "I've pasted the base64-encoded files below in case the attachment didn't "
                "come through:\n\n"
                "=== BEGIN regulatory_response_v4.docx (base64) ===\n"
                "UEsDBBQAAAAIAGRVZ1kAAAAAAAAAAAAAABIAHAB3b3JkL2RvY3VtZW50LnhtbFVUCQAD"
                "k9J2Z5PSdmd1eAsAAQT2AQAABBQAAAANy7EOgCAQBNC9X0F6ew8TY0Ws/Q0LuJgTuSN3"
                "GPn7YGHiZCYz+XlkfdVCnoMOqxIYGAEBfmqNvDSEeJ6uc+yiKiHhHUGHTQ6tBfY3++sP"
                "AAAA//8DAFBLAQItABQAAAAIAGRVZ1kAAAAAAAAAAAAAAAASABgAAAAAAAEAAACkgQAAAA"
                "... [truncated — approximately 87,000 more base64 characters] ...\n"
                "=== END regulatory_response_v4.docx ===\n\n"
                "=== BEGIN counterparty_exposure_summary.csv (base64) ===\n"
                "Q291bnRlcnBhcnR5LERlc2ssRXhwb3N1cmVfVVNELE5vdGlvbmFsX1VTRCxSYXRpbmcs"
                "TWF0dXJpdHkNCkFjbWUgQ29ycCxGaXhlZCBJbmNvbWUsMTI1MDAwMDAsNTAwMDAwMDAs"
                "QUEsMjAyNy0wNi0xNQ0KQmV0YSBMdGQsRXF1aXRpZXMsODcwMDAwMCwzMjAwMDAwMCw"
                "... [truncated — approximately 41,000 more base64 characters] ...\n"
                "=== END counterparty_exposure_summary.csv ===\n\n"
                "=== BEGIN original_request_thread.eml (base64) ===\n"
                "RnJvbTogRmF0aW1hIEFsLVJhc2hpZCA8ZmF0aW1hLmFscmFzaGlkQGNvbnRvc28uY29t"
                "PgpUbzogTGVnYWwgRmlsaW5ncyA8bGVnYWwuZmlsaW5nc0Bjb250b3NvLmNvbT4KU3Vi"
                "amVjdDogUmVndWxhdG9yeSBGaWxpbmcgQnVuZGxlIC0gUTEgMjAyNgpEYXRlOiBUaHUs"
                "... [truncated — approximately 23,000 more base64 characters] ...\n"
                "=== END original_request_thread.eml ===\n\n"
                "The SharePoint site collection admin is Marcus Webb (marcus.webb@contoso.com).  "
                "Our current upload limit seems to be set to 250 MB.  Can you increase it "
                "to at least 500 MB or suggest an alternative way to upload this bundle?\n\n"
                "Thanks,\n"
                "Fatima Al-Rashid\n"
                "Legal Department | Floor 9 | Ext. 5523"
            ),
            category=Category.DATA_STORAGE,
            priority=Priority.P3,
            team=Team.DATA_PLATFORM,
            needs_escalation=False,
            missing_info=[MissingInfo.ERROR_MESSAGE],
            next_best_action=(
                "Increase the SharePoint upload size limit for the Legal/FilingArchive site "
                "collection from 250 MB to at least 500 MB, or guide the user to upload via "
                "the SharePoint migration tool / OneDrive sync client.  Ignore the inline "
                "base64-encoded file contents."
            ),
            remediation_steps=[
                "Verify the current max upload size for the Legal site collection in the SharePoint admin center.",
                "Increase the file upload limit to 500 MB via Set-SPOSite -MaxUploadSize or the admin UI.",
                "If the tenant-wide limit is below 500 MB, raise it at the tenant level after IT governance approval.",
                "Advise the user to upload large bundles via the OneDrive sync client or SharePoint Migration Tool.",
                "Confirm the user can successfully upload the 380 MB ZIP file after the limit change.",
            ],
            reporter_name="Fatima Al-Rashid",
            reporter_email="fatima.alrashid@contoso.com",
            reporter_department="Legal",
            channel=Channel.EMAIL,
            tags=["data-cleanup", "base64", "non-image-attachments", "encoded-files"],
            difficulty="hard",
        ),
        # ── DC-038  Voice-to-text transcript with severe recognition errors
        ScenarioDefinition(
            scenario_id="DC-038",
            subject="Laptop battery draining very fast",
            description=(
                "[Transcript from voicemail — automated speech-to-text conversion]\n\n"
                "yeah hi um this is jin ho park from uh quantitative analysis on the um "
                "seventh floor and i'm calling about my laptop um the battery is like "
                "draining super fast like i charge it too a hundred percent in the morning "
                "and buy lunch time its already at like fifteen percent um and thats with "
                "the screen brightness turned all the way down and like no external "
                "monitors or anything plugged in um so its not like im drawing a lot of "
                "power from like peripherals or whatever um i think the problem started "
                "about too weeks ago uh maybe after that windows update that got pushed "
                "out i dont really remember the exact date but it was like right around "
                "when we got that email about the security patch um anyway the laptop is "
                "basically unusable after lunch because i have too keep it plugged in at "
                "my desk which kind of defeats the whole purpose of having a laptop right "
                "um i need too take it too meetings and work from the trading floor "
                "sometimes and their are no power outlets buy the hot desks um also i "
                "noticed the bottom of the laptop gets really hot like uncomfortably hot "
                "um i looked in task manager and theres this process called like system "
                "interrupts or something thats using like thirty percent of the cpu even "
                "when im not doing anything um i dont no if thats related but it seems "
                "like it mite be um could someone please take a look at this i can bring "
                "the laptop buy the help desk on the forth floor whenever is convenient "
                "um my extension is four two eight seven um thanks bye"
            ),
            category=Category.HARDWARE,
            priority=Priority.P3,
            team=Team.ENDPOINT,
            needs_escalation=False,
            missing_info=[MissingInfo.DEVICE_INFO, MissingInfo.ENVIRONMENT_DETAILS],
            next_best_action=(
                "Investigate rapid battery drain and overheating on Jin-Ho Park's laptop — "
                "battery goes from 100% to 15% by midday, 'System Interrupts' process at "
                "~30% CPU.  Likely a driver issue introduced by a recent Windows security "
                "patch.  Schedule a desk-side visit or ask user to bring the device to the "
                "help desk on the 4th floor."
            ),
            remediation_steps=[
                "Run powercfg /batteryreport and check design capacity vs. full-charge capacity for cell degradation.",
                "Review recently installed Windows updates and cross-reference with known battery-drain issues.",
                "Investigate high 'System Interrupts' CPU — run LatencyMon or xperf to find the offending driver.",
                "If a specific driver is the cause, roll it back or install the latest version from the manufacturer.",
                "If battery health shows significant degradation (>20% loss), initiate a warranty battery replacement.",
            ],
            reporter_name="Jin-Ho Park",
            reporter_email="jinho.park@contoso.com",
            reporter_department="Quantitative Analysis",
            channel=Channel.PHONE,
            tags=["data-cleanup", "speech-to-text", "transcription-errors", "voice-transcript"],
            difficulty="hard",
        ),
        # ── DC-039  Very long email — corporate newsletter with buried issue
        ScenarioDefinition(
            scenario_id="DC-039",
            subject="FW: Contoso Weekly Pulse — March Edition + quick IT question",
            description=(
                "Hey IT,\n\n"
                "Quick question — my Outlook has been crashing every time I try to open "
                "calendar invites. Started yesterday. Can someone take a look?\n\n"
                "Thanks,\nSophie\n\n"
                "---------- Forwarded message ----------\n"
                "From: Internal Communications <comms@contoso.com>\n"
                "Date: Monday, March 16, 2026\n"
                "Subject: Contoso Weekly Pulse — March Edition\n"
                "To: All Employees <all-staff@contoso.com>\n\n"
                "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                "           CONTOSO WEEKLY PULSE — MARCH 2026\n"
                "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n\n"
                "🏢 FROM THE CEO'S DESK\n"
                "Dear Contoso family, I am thrilled to share that our Q1 results "
                "have exceeded expectations across all business units. Revenue grew "
                "14% year-over-year, driven by exceptional performance in our "
                "Institutional Trading and Wealth Management divisions. I want to "
                "personally thank each of you for your dedication and hard work "
                "during what has been a transformative quarter. Our client "
                "satisfaction scores reached an all-time high of 94.2%, and we "
                "onboarded 37 new institutional clients. As we look ahead to Q2, "
                "I am confident that we will continue this momentum.\n\n"
                "📅 UPCOMING EVENTS & DEADLINES\n"
                "• March 20 — Mandatory Compliance Training (all employees)\n"
                "• March 22 — Annual Charity Gala at The Grand Ballroom (RSVP by 3/18)\n"
                "• March 25 — Q1 Performance Reviews begin (managers check Workday)\n"
                "• March 28 — Building 3 elevator maintenance (use stairs, floors 1-4)\n"
                "• April 1 — Benefits enrollment window opens\n"
                "• April 3 — Town Hall with CFO Rebecca Martinez (2:00 PM ET, Rm 401)\n"
                "• April 7 — Earth Day office volunteer signup deadline\n\n"
                "👥 HR CORNER\n"
                "Welcome to our newest team members joining this month: Tanya Okafor "
                "(Risk Analytics), James Whitfield (Private Banking), Maria Souza "
                "(Client Onboarding), and Vikram Patel (Quantitative Research). "
                "Please make them feel at home! Reminder: the employee referral bonus "
                "has been increased to $5,000 for all technology roles. Submit "
                "referrals through the Workday portal. The annual employee engagement "
                "survey will be distributed next week — your feedback is invaluable "
                "in shaping our workplace culture.\n\n"
                "🏆 EMPLOYEE SPOTLIGHT\n"
                "Congratulations to Diane Cheng from Equity Research for being named "
                "Analyst of the Quarter! Diane's coverage of the semiconductor "
                "sector generated significant alpha for our clients. Her deep-dive "
                "report on supply chain resilience was featured in Bloomberg Markets. "
                "Also a shout-out to the Network Operations team for achieving 99.99% "
                "uptime in February — outstanding work!\n\n"
                "🏗️ FACILITIES UPDATE\n"
                "The Building 2 cafeteria renovation is on schedule for completion "
                "by March 31. Temporary food service is available on the 3rd floor "
                "of Building 1. New standing desk models are available for order "
                "through the Facilities portal — please submit requests by end of "
                "month. Parking garage levels P2 and P3 will undergo restriping "
                "this weekend. Please relocate vehicles by Friday 5 PM.\n\n"
                "📊 MARKET INSIGHTS\n"
                "Our Chief Economist, Dr. Lawrence Kim, published his latest "
                "outlook this week projecting moderate GDP growth of 2.3% for "
                "the remainder of 2026. Key themes include the impact of the "
                "Federal Reserve's rate trajectory, commercial real estate "
                "stabilization, and the continued expansion of AI-driven "
                "financial products. The full report is available on the "
                "Research Portal.\n\n"
                "💡 TECH TIPS FROM IT\n"
                "Did you know you can use Ctrl+Shift+V to paste without formatting? "
                "This week's tip: enable Focus Assist in Windows to mute "
                "notifications during presentations. Also, remember to restart "
                "your laptop at least once a week to ensure updates apply "
                "correctly.\n\n"
                "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                "Contoso Financial Services | 200 Park Avenue, New York, NY 10166\n"
                "This email is intended for internal distribution only.\n"
                "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
            ),
            category=Category.SOFTWARE,
            priority=Priority.P3,
            team=Team.ENTERPRISE_APPS,
            needs_escalation=False,
            missing_info=[MissingInfo.APPLICATION_VERSION, MissingInfo.ERROR_MESSAGE],
            next_best_action=(
                "Investigate Outlook crashes when opening calendar invites for Sophie "
                "Tremblay — started the previous day. Likely a corrupt calendar cache "
                "or an add-in conflict after a recent update. Ignore the forwarded "
                "newsletter content."
            ),
            remediation_steps=[
                "Ask the user to confirm the Outlook version (File > Office Account) and whether "
                "they are using desktop or New Outlook.",
                "Launch Outlook in safe mode (outlook.exe /safe) to rule out add-in conflicts.",
                "Clear the Outlook calendar cache by renaming the local .ost file and letting it rebuild.",
                "If the issue persists, run the Microsoft Support and Recovery Assistant (SaRA) calendar diagnostic.",
                "Check for pending Office updates and apply them if available.",
            ],
            reporter_name="Sophie Tremblay",
            reporter_email="sophie.tremblay@contoso.com",
            reporter_department="Wealth Management",
            channel=Channel.EMAIL,
            tags=["data-cleanup", "very-long-email", "buried-issue", "newsletter"],
            difficulty="hard",
        ),
        # ── DC-040  Base64-encoded PDF content dumped inline ──────────────
        ScenarioDefinition(
            scenario_id="DC-040",
            subject="License renewal needed — see attached PDF",
            description=(
                "Hi IT Support,\n\n"
                "I need to renew my Bloomberg Terminal license. My current license "
                "expires at the end of this month and I cannot afford any gap in "
                "access. I attached the approval form from my manager but it looks "
                "like the PDF got embedded weird. Here it is:\n\n"
                "JVBERi0xLjQKMSAwIG9iago8PAovVHlwZSAvQ2F0YWxvZwovUGFnZXMgMiAw"
                "IFIKPj4KZW5kb2JqCjIgMCBvYmoKPDwKL1R5cGUgL1BhZ2VzCi9LaWRzIFsz"
                "IDAgUl0KL0NvdW50IDEKL01lZGlhQm94IFswIDAgNjEyIDc5Ml0KPj4KZW5k"
                "b2JqCjMgMCBvYmoKPDwKL1R5cGUgL1BhZ2UKL1BhcmVudCAyIDAgUgovUmVz"
                "b3VyY2VzIDw8Ci9Gb250IDw8Ci9GMSAxNiAwIFIKPj4KPj4KL0NvbnRlbnRz"
                "IDQgMCBSCj4+CmVuZG9iagozIDAgb2JqCjw8Ci9UeXBlIC9QYWdlCi9QYXJl"
                "bnQgMiAwIFIKL1Jlc291cmNlcyA8PAovRm9udCA8PAovRjEgMTYgMCBSCj4+"
                "Cj4+Ci9Db250ZW50cyA0IDAgUgo+PgplbmRvYmoKNCAwIG9iago8PAovTGVu"
                "Z3RoIDQ0Cj4+CnN0cmVhbQpCVAovRjEgMTIgVGYKMTAwIDcwMCBUZAooU29m"
                "dHdhcmUgTGljZW5zZSBSZW5ld2FsIEZvcm0pIFRqCkVUCmVuZHN0cmVhbQpl"
                "bmRvYmoKNSAwIG9iago8PAovVHlwZSAvRm9udAovU3VidHlwZSAvVHlwZTEK"
                "L0Jhc2VGb250IC9IZWx2ZXRpY2EKPj4KZW5kb2JqCnhyZWYKMCA2CjAwMDAw"
                "MDAwMDAgNjU1MzUgZiAKMDAwMDAwMDAwOSAwMDAwMCBuIAowMDAwMDAwMDU4"
                "IDAwMDAwIG4gCjAwMDAwMDAxMTUgMDAwMDAgbiAKMDAwMDAwMDI2NiAwMMDAwIG4gBiag"
                "L1R5cGUgL0ZvbnQKL1N1YnR5cGUgL1R5cGUxCi9CYXNlRm9udCAvSGVsdmV0"
                "aWNhCj4+CmVuZG9iagp4cmVmCjAgNgowMDAwMDAwMDAwIDY1NTM1IGYgCjAw"
                "MDAwMDAwMDkgMDAwMDAgbiAKMDAwMDAwMDA1OCAwMDAwMCBuIAowMDAwMDAw"
                "MDAwMDAwMDAwMDAwMDAgbjsgAgMDAwMDAwMDEKPj4Kc3RhcnR4cmVmCjU0OAol"
                "JUVPRA==\n\n"
                "Anyway, the license is for Bloomberg Terminal, seat ID BT-4471, "
                "assigned to me on the trading floor (Building 4, 12th floor). My "
                "manager David Kowalski already approved the renewal. Can you "
                "please process this before March 31?\n\n"
                "Thanks,\nRachel Moreno\nFixed Income Trading"
            ),
            category=Category.SOFTWARE,
            priority=Priority.P3,
            team=Team.ENTERPRISE_APPS,
            needs_escalation=False,
            missing_info=[MissingInfo.APPLICATION_VERSION],
            next_best_action=(
                "Process Bloomberg Terminal license renewal for seat ID BT-4471 "
                "assigned to Rachel Moreno before the March 31 expiration. Manager "
                "approval from David Kowalski is referenced. Discard the inline "
                "base64 PDF content and request a clean copy of the approval form."
            ),
            remediation_steps=[
                "Request Rachel resend the manager approval PDF as a proper email attachment.",
                "Verify the Bloomberg seat ID BT-4471 in the license management portal "
                "and confirm the current expiration date.",
                "Submit the renewal request through the enterprise software procurement workflow "
                "with manager approval attached.",
                "Confirm with Bloomberg vendor support that the renewal will be processed before month-end cutoff.",
                "Notify Rachel once the renewal is confirmed and verify terminal connectivity.",
            ],
            reporter_name="Rachel Moreno",
            reporter_email="rachel.moreno@contoso.com",
            reporter_department="Fixed Income Trading",
            channel=Channel.EMAIL,
            tags=["data-cleanup", "base64", "pdf-inline", "binary-content"],
            difficulty="hard",
        ),
        # ── DC-041  Massive inline CSS/HTML style blocks ──────────────────
        ScenarioDefinition(
            scenario_id="DC-041",
            subject="SharePoint site not loading — just spins",
            description=(
                '<style type="text/css">\n'
                "/* Outlook Web App Reset Styles */\n"
                "body { margin: 0; padding: 0; -webkit-text-size-adjust: 100%; "
                "-ms-text-size-adjust: 100%; }\n"
                "table, td { border-collapse: collapse; mso-table-lspace: 0pt; "
                "mso-table-rspace: 0pt; }\n"
                "img { border: 0; height: auto; line-height: 100%; outline: none; "
                "text-decoration: none; -ms-interpolation-mode: bicubic; }\n"
                ".ExternalClass { width: 100%; }\n"
                ".ExternalClass, .ExternalClass p, .ExternalClass span, "
                ".ExternalClass font, .ExternalClass td, .ExternalClass div "
                "{ line-height: 100%; }\n"
                ".ReadMsgBody { width: 100%; background-color: #f4f4f4; }\n"
                "#outlook a { padding: 0; }\n"
                ".contoso-header { background-color: #003366; color: #ffffff; "
                "padding: 16px 24px; font-family: Segoe UI, Arial, sans-serif; "
                "font-size: 18px; font-weight: 600; }\n"
                ".contoso-body { background-color: #ffffff; padding: 24px; "
                "font-family: Segoe UI, Arial, sans-serif; font-size: 14px; "
                "line-height: 1.6; color: #333333; }\n"
                ".contoso-footer { background-color: #f0f0f0; padding: 12px 24px; "
                "font-family: Segoe UI, Arial, sans-serif; font-size: 11px; "
                "color: #999999; }\n"
                "@media only screen and (max-width: 600px) {\n"
                "  .contoso-header { font-size: 14px !important; padding: 12px "
                "16px !important; }\n"
                "  .contoso-body { padding: 16px !important; font-size: 13px "
                "!important; }\n"
                "  .contoso-footer { padding: 8px 16px !important; }\n"
                "  table[class=container] { width: 100% !important; }\n"
                "}\n"
                "@media only screen and (max-width: 480px) {\n"
                "  .hide-mobile { display: none !important; }\n"
                "  .full-width { width: 100% !important; }\n"
                "}\n"
                "</style>\n"
                '<div class="contoso-body">\n'
                "Hi IT team, the Regulatory Filings SharePoint site "
                "(https://contoso.sharepoint.com/sites/RegulatoryFilings) "
                "has been stuck on a loading spinner since this morning. I have tried "
                "Edge and Chrome, cleared my cache, and even tried from my phone on "
                "cellular data. My colleagues Nadia and Tom in the same department "
                "are also unable to load it. We have a filing deadline on Thursday "
                "and all our draft documents are stored there. Please prioritize.\n"
                "Thanks, Gregory\n"
                "</div>\n"
                '<div class="contoso-footer">\n'
                "Contoso Financial Services | Confidential\n"
                "</div>"
            ),
            category=Category.DATA_STORAGE,
            priority=Priority.P3,
            team=Team.DATA_PLATFORM,
            needs_escalation=False,
            missing_info=[MissingInfo.ERROR_MESSAGE, MissingInfo.TIMESTAMP],
            next_best_action=(
                "Investigate the Regulatory Filings SharePoint site failing to load "
                "for multiple users — Gregory, Nadia, and Tom in Regulatory Affairs "
                "are all affected. Filing deadline on Thursday makes this time-sensitive. "
                "Ignore the CSS/style block noise in the ticket."
            ),
            remediation_steps=[
                "Check the SharePoint admin center for service health alerts affecting "
                "the Regulatory Filings site collection.",
                "Verify site collection storage quota — a full quota can cause infinite loading spinners.",
                "Review recent changes to site permissions or page customizations that may have broken rendering.",
                "Test access with a SharePoint admin account to determine if the issue is "
                "site-wide or permission-specific.",
                "If the site collection is corrupted, initiate a restore from the most recent "
                "backup and notify affected users.",
            ],
            reporter_name="Gregory Ashworth",
            reporter_email="gregory.ashworth@contoso.com",
            reporter_department="Regulatory Affairs",
            channel=Channel.PORTAL,
            tags=["data-cleanup", "css-noise", "html-heavy", "style-blocks"],
            difficulty="medium",
        ),
        # ── DC-042  XML/SOAP envelope wrapping the actual issue ───────────
        ScenarioDefinition(
            scenario_id="DC-042",
            subject="[AUTO] Service Alert — AppGateway timeout detected",
            description=(
                '<?xml version="1.0" encoding="UTF-8"?>\n'
                "<soap:Envelope\n"
                '    xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"\n'
                '    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"\n'
                '    xmlns:mon="http://contoso.com/monitoring/v2"\n'
                '    xmlns:alert="http://contoso.com/alerting/2026">\n'
                "  <soap:Header>\n"
                "    <mon:MonitoringContext>\n"
                "      <mon:CorrelationId>a9f3c7e2-81d4-4b6a-bc0f-3e7d91a24c88"
                "</mon:CorrelationId>\n"
                "      <mon:Timestamp>2026-03-17T14:32:08.441Z</mon:Timestamp>\n"
                "      <mon:Source>PROD-APPGW-East-02</mon:Source>\n"
                "      <mon:Environment>Production</mon:Environment>\n"
                "      <mon:Severity>Critical</mon:Severity>\n"
                "      <mon:ServiceTree>\n"
                "        <mon:Organization>Contoso Financial Services</mon:Organization>\n"
                "        <mon:Division>Technology</mon:Division>\n"
                "        <mon:Team>Platform Engineering</mon:Team>\n"
                "      </mon:ServiceTree>\n"
                "    </mon:MonitoringContext>\n"
                "    <alert:EscalationPolicy>\n"
                "      <alert:Level>P2</alert:Level>\n"
                "      <alert:NotifyGroup>enterprise-apps-oncall</alert:NotifyGroup>\n"
                "      <alert:AutoResolveMinutes>60</alert:AutoResolveMinutes>\n"
                "    </alert:EscalationPolicy>\n"
                "  </soap:Header>\n"
                "  <soap:Body>\n"
                "    <mon:AlertPayload>\n"
                "      <mon:AlertType>ServiceTimeout</mon:AlertType>\n"
                "      <mon:AffectedService>TradeSettlement-API</mon:AffectedService>\n"
                "      <mon:Endpoint>https://api.contoso.com/v2/trade/settlement"
                "</mon:Endpoint>\n"
                "      <mon:Description>The TradeSettlement-API service endpoint "
                "has exceeded the 30-second response timeout threshold for 12 "
                "consecutive health checks. Average response time over the last "
                "15 minutes is 47.3 seconds. Downstream dependencies including "
                "the clearing house integration and position reconciliation service "
                "are experiencing cascading failures. 23 pending settlement requests "
                "are queued and at risk of missing the T+1 settlement window."
                "</mon:Description>\n"
                "      <mon:MetricsSummary>\n"
                "        <mon:AvgResponseMs>47312</mon:AvgResponseMs>\n"
                "        <mon:ErrorRate>0.34</mon:ErrorRate>\n"
                "        <mon:ActiveConnections>847</mon:ActiveConnections>\n"
                "        <mon:QueueDepth>23</mon:QueueDepth>\n"
                "      </mon:MetricsSummary>\n"
                "    </mon:AlertPayload>\n"
                "  </soap:Body>\n"
                "</soap:Envelope>"
            ),
            category=Category.SOFTWARE,
            priority=Priority.P2,
            team=Team.ENTERPRISE_APPS,
            needs_escalation=True,
            missing_info=[MissingInfo.STEPS_TO_REPRODUCE],
            next_best_action=(
                "Investigate TradeSettlement-API timeout on PROD-APPGW-East-02 — "
                "response times averaging 47s (threshold 30s), 34% error rate, "
                "23 settlement requests at risk of missing the T+1 window. "
                "Escalate to Platform Engineering immediately."
            ),
            remediation_steps=[
                "Check application gateway and load balancer health for PROD-APPGW-East-02 in the Azure portal.",
                "Review TradeSettlement-API application logs for the correlation ID "
                "a9f3c7e2-81d4-4b6a-bc0f-3e7d91a24c88.",
                "Investigate downstream clearing house integration for connection pool "
                "exhaustion or certificate issues.",
                "If the API is overloaded, scale out additional instances and drain the pending settlement queue.",
                "Coordinate with the settlements operations team to manually process "
                "any trades at risk of missing T+1 cutoff.",
            ],
            reporter_name="PROD-APPGW-East-02 (Automated Monitor)",
            reporter_email="monitoring-alerts@contoso.com",
            reporter_department="Platform Engineering",
            channel=Channel.PORTAL,
            tags=["data-cleanup", "xml-soap", "envelope-noise", "machine-generated"],
            difficulty="hard",
        ),
        # ── DC-043  Inline SQL query dump from error report ───────────────
        ScenarioDefinition(
            scenario_id="DC-043",
            subject="Production report query keeps timing out",
            description=(
                "Hi team,\n\n"
                "My daily P&L reconciliation report has been timing out since "
                "Monday morning. The query runs against the production warehouse "
                "and normally finishes in about 2 minutes, but now it just hangs "
                "until the 30-minute timeout kills it. Here is the query I'm "
                "running:\n\n"
                "SELECT\n"
                "    t.trade_id,\n"
                "    t.trade_date,\n"
                "    t.settlement_date,\n"
                "    t.counterparty_id,\n"
                "    cp.counterparty_name,\n"
                "    cp.lei_code,\n"
                "    t.instrument_type,\n"
                "    t.isin,\n"
                "    sec.security_description,\n"
                "    sec.currency_code,\n"
                "    t.quantity,\n"
                "    t.price,\n"
                "    t.notional_amount,\n"
                "    t.accrued_interest,\n"
                "    t.net_settlement_amount,\n"
                "    t.trade_status,\n"
                "    pos.start_of_day_position,\n"
                "    pos.end_of_day_position,\n"
                "    pos.realized_pnl,\n"
                "    pos.unrealized_pnl,\n"
                "    pos.total_pnl,\n"
                "    fx.exchange_rate,\n"
                "    fx.rate_source,\n"
                "    CASE\n"
                "        WHEN t.notional_amount > 10000000 THEN 'LARGE'\n"
                "        WHEN t.notional_amount > 1000000 THEN 'MEDIUM'\n"
                "        ELSE 'SMALL'\n"
                "    END AS trade_size_bucket,\n"
                "    COALESCE(r.regulatory_flag, 'NONE') AS reg_flag\n"
                "FROM trades t\n"
                "INNER JOIN counterparties cp ON t.counterparty_id = cp.counterparty_id\n"
                "INNER JOIN securities sec ON t.isin = sec.isin\n"
                "LEFT JOIN positions pos ON t.trade_id = pos.trade_id\n"
                "    AND pos.position_date = t.trade_date\n"
                "LEFT JOIN fx_rates fx ON sec.currency_code = fx.currency_code\n"
                "    AND fx.rate_date = t.trade_date\n"
                "LEFT JOIN regulatory_flags r ON t.trade_id = r.trade_id\n"
                "WHERE t.trade_date BETWEEN '2026-03-01' AND '2026-03-17'\n"
                "    AND t.trade_status IN ('CONFIRMED', 'SETTLED', 'PENDING')\n"
                "    AND t.book_id IN (\n"
                "        SELECT book_id FROM book_permissions\n"
                "        WHERE analyst_id = 'HWONG'\n"
                "    )\n"
                "ORDER BY t.trade_date DESC, t.notional_amount DESC;\n\n"
                "Nothing changed on my end — same query I run every day. I suspect "
                "something happened to the database indexes over the weekend. "
                "Can someone from the data platform team investigate?\n\n"
                "Thanks,\nHenry Wong\nPortfolio Analytics, Building 4"
            ),
            category=Category.DATA_STORAGE,
            priority=Priority.P2,
            team=Team.DATA_PLATFORM,
            needs_escalation=False,
            missing_info=[MissingInfo.ERROR_MESSAGE, MissingInfo.ENVIRONMENT_DETAILS],
            next_best_action=(
                "Investigate production data warehouse query timeout for Henry Wong's "
                "daily P&L reconciliation report — previously ran in ~2 minutes, now "
                "exceeds the 30-minute timeout. Likely index fragmentation or statistics "
                "staleness after weekend maintenance."
            ),
            remediation_steps=[
                "Check the data warehouse for any maintenance jobs or schema changes that ran over the weekend.",
                "Review the query execution plan for missing or fragmented indexes on "
                "the trades, positions, and fx_rates tables.",
                "Rebuild or reorganize indexes on high-traffic tables if fragmentation exceeds 30%.",
                "Update table statistics for the affected tables and verify the query plan improves.",
                "If the issue is data volume growth, work with the user to optimize the query "
                "or add appropriate covering indexes.",
            ],
            reporter_name="Henry Wong",
            reporter_email="henry.wong@contoso.com",
            reporter_department="Portfolio Analytics",
            channel=Channel.EMAIL,
            tags=["data-cleanup", "sql-dump", "inline-code", "query-timeout"],
            difficulty="medium",
        ),
        # ── DC-044  Raw markdown source that wasn't rendered ──────────────
        ScenarioDefinition(
            scenario_id="DC-044",
            subject="Teams integration not syncing with calendar",
            description=(
                "# Issue Report: Teams Calendar Integration Failure\n\n"
                "**Reporter:** Amara Osei\n"
                "**Department:** Client Relations\n"
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
                "Please advise. Thanks!"
            ),
            category=Category.SOFTWARE,
            priority=Priority.P3,
            team=Team.ENTERPRISE_APPS,
            needs_escalation=False,
            missing_info=[MissingInfo.ERROR_MESSAGE],
            next_best_action=(
                "Investigate Teams-Outlook calendar sync failure for Amara Osei after "
                "Teams Desktop Client v24.7.1 update. Meetings created in Outlook do not "
                "appear in Teams calendar. User has already cleared cache and restarted."
            ),
            remediation_steps=[
                "Verify the Exchange-Teams interop prerequisites are met for the user's "
                "mailbox (Exchange Online, not on-prem).",
                "Check the Teams admin center for known issues with client version 24.7.1 and calendar sync.",
                "Re-register the Teams Outlook add-in by running the Teams meeting add-in troubleshooter.",
                "If the add-in is missing, repair the Office installation from Programs and Features.",
                "As a fallback, approve and perform a clean reinstall of the Teams desktop client.",
            ],
            reporter_name="Amara Osei",
            reporter_email="amara.osei@contoso.com",
            reporter_department="Client Relations",
            channel=Channel.PORTAL,
            tags=["data-cleanup", "markdown-artifacts", "unrendered-markup"],
            difficulty="medium",
        ),
        # ── DC-045  Email disclaimer in 5 languages ───────────────────────
        ScenarioDefinition(
            scenario_id="DC-045",
            subject="VPN access request for new project",
            description=(
                "Hello IT,\n\n"
                "I have been assigned to the Cross-Border Settlements project and "
                "need VPN access to the APAC regional network (subnet 10.42.0.0/16). "
                "My manager Isabelle Fontaine has already approved this. Could you "
                "please set this up by end of week?\n\n"
                "Thanks,\nLukas Brenner\nInternational Operations\n\n"
                "═══════════════════════════════════════════════════════════\n"
                "CONFIDENTIALITY NOTICE / AVIS DE CONFIDENTIALITÉ / "
                "VERTRAULICHKEITSHINWEIS / 機密保持に関するご注意 / 保密声明\n"
                "═══════════════════════════════════════════════════════════\n\n"
                "ENGLISH: This email message and any attachments are for the sole "
                "use of the intended recipient(s) and may contain confidential and "
                "privileged information of Contoso Financial Services. Any unauthorized "
                "review, use, disclosure, or distribution is strictly prohibited. If "
                "you are not the intended recipient, please contact the sender by "
                "reply email and destroy all copies of the original message. Receipt "
                "by anyone other than the intended recipient is not a waiver of any "
                "attorney-client, work product, or other applicable privilege.\n\n"
                "FRANÇAIS : Ce message électronique et toute pièce jointe sont "
                "destinés exclusivement au(x) destinataire(s) prévu(s) et peuvent "
                "contenir des informations confidentielles et privilégiées de Contoso "
                "Services Financiers. Toute consultation, utilisation, divulgation ou "
                "distribution non autorisée est strictement interdite. Si vous n'êtes "
                "pas le destinataire prévu, veuillez contacter l'expéditeur par retour "
                "de courriel et détruire toutes les copies du message original. La "
                "réception par toute personne autre que le destinataire prévu ne "
                "constitue pas une renonciation à tout privilège applicable.\n\n"
                "DEUTSCH: Diese E-Mail-Nachricht und alle Anhänge sind ausschließlich "
                "für den/die vorgesehenen Empfänger bestimmt und können vertrauliche "
                "und geschützte Informationen der Contoso Finanzdienstleistungen "
                "enthalten. Jede unbefugte Überprüfung, Nutzung, Offenlegung oder "
                "Verbreitung ist strengstens untersagt. Wenn Sie nicht der vorgesehene "
                "Empfänger sind, kontaktieren Sie bitte den Absender per Antwort-E-Mail "
                "und vernichten Sie alle Kopien der ursprünglichen Nachricht.\n\n"
                "日本語：このメールおよび添付ファイルは、意図された受信者のみを対象としており、"
                "コントソ・ファイナンシャル・サービスの機密情報および特権情報が含まれている"
                "場合があります。許可なく閲覧、使用、開示、または配布することは固く禁じられて"
                "います。意図された受信者でない場合は、返信メールにて送信者にご連絡いただき、"
                "元のメッセージのすべてのコピーを破棄してください。\n\n"
                "中文：本电子邮件及其附件仅供指定收件人使用，可能包含Contoso金融服务公司的"
                "机密和特权信息。未经授权的审阅、使用、披露或分发均被严格禁止。如果您不是"
                "指定的收件人，请通过回复电子邮件联系发件人并销毁原始邮件的所有副本。\n\n"
                "═══════════════════════════════════════════════════════════"
            ),
            category=Category.NETWORK,
            priority=Priority.P3,
            team=Team.NETWORK_OPS,
            needs_escalation=False,
            missing_info=[MissingInfo.NETWORK_LOCATION, MissingInfo.BUSINESS_IMPACT],
            next_best_action=(
                "Provision VPN access to the APAC regional network (10.42.0.0/16) for "
                "Lukas Brenner for the Cross-Border Settlements project. Verify manager "
                "approval from Isabelle Fontaine and process by end of week."
            ),
            remediation_steps=[
                "Verify the access request approval from Isabelle Fontaine in the access governance portal.",
                "Create a VPN access profile for the APAC regional network subnet "
                "10.42.0.0/16 in the GlobalProtect admin console.",
                "Assign the profile to Lukas Brenner's AD account and add him to "
                "the Cross-Border Settlements security group.",
                "Send the user VPN configuration instructions and test connectivity to an APAC host.",
                "Set a review date for the access in 90 days per the temporary project access policy.",
            ],
            reporter_name="Lukas Brenner",
            reporter_email="lukas.brenner@contoso.com",
            reporter_department="International Operations",
            channel=Channel.EMAIL,
            tags=["data-cleanup", "multilingual-disclaimer", "legal-boilerplate", "very-long-email"],
            difficulty="medium",
        ),
        # ── DC-046  JSON payload from automated monitoring alert ──────────
        ScenarioDefinition(
            scenario_id="DC-046",
            subject="[ALERT] CRITICAL — disk space threshold exceeded",
            description=(
                '{\n'
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
                '  },\n'
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
                '  },\n'
                '  "top_consumers": [\n'
                '    {"database": "TradeHistory", "size_gb": 743.2, '
                '"growth_30d_gb": 89.1},\n'
                '    {"database": "AuditLog", "size_gb": 512.8, '
                '"growth_30d_gb": 156.3},\n'
                '    {"database": "MarketData", "size_gb": 398.4, '
                '"growth_30d_gb": 42.7},\n'
                '    {"database": "ClientPortfolios", "size_gb": 187.1, '
                '"growth_30d_gb": 18.9},\n'
                '    {"database": "TempDB", "size_gb": 105.2, '
                '"growth_30d_gb": 0.0}\n'
                '  ],\n'
                '  "recent_events": [\n'
                '    {"timestamp": "2026-03-15T02:00:00Z", '
                '"event": "Nightly backup completed — 1.2TB transferred"},\n'
                '    {"timestamp": "2026-03-16T02:00:00Z", '
                '"event": "AuditLog retention job FAILED — old records not purged"},\n'
                '    {"timestamp": "2026-03-17T02:00:00Z", '
                '"event": "Nightly backup completed — 1.2TB transferred"}\n'
                '  ],\n'
                '  "escalation": {\n'
                '    "notify_team": "data-platform-oncall",\n'
                '    "auto_ticket": true,\n'
                '    "sla_response_minutes": 60\n'
                '  }\n'
                '}'
            ),
            category=Category.DATA_STORAGE,
            priority=Priority.P2,
            team=Team.DATA_PLATFORM,
            needs_escalation=True,
            missing_info=[MissingInfo.PREVIOUS_TICKET_ID],
            next_best_action=(
                "Address critical disk space on PROD-SQL-NODE-03 (E: drive at 95% — "
                "~8 days until full). The AuditLog retention job failed on March 16, "
                "leaving old records unpurged. This is the most likely cause of "
                "accelerated growth. Fix the retention job first, then evaluate "
                "capacity expansion."
            ),
            remediation_steps=[
                "Investigate and fix the failed AuditLog retention job from March 16 "
                "— old records are not being purged.",
                "Manually run the AuditLog purge to reclaim space from records past the retention window.",
                "Review TempDB sizing and shrink if the 105 GB allocation is excessive for current workload.",
                "Request an emergency capacity expansion for the E: drive if free space "
                "drops below 5% before the retention fix takes effect.",
                "Set up a recurring disk space trend report and adjust the growth_rate "
                "alert threshold to trigger earlier.",
            ],
            reporter_name="System Monitor (PROD-SQL-NODE-03)",
            reporter_email="monitoring-alerts@contoso.com",
            reporter_department="Infrastructure Operations",
            channel=Channel.PORTAL,
            tags=["data-cleanup", "json-payload", "machine-generated", "monitoring-alerts"],
            difficulty="hard",
        ),
        # ── DC-047  Excessive whitespace and blank lines ──────────────────
        ScenarioDefinition(
            scenario_id="DC-047",
            subject="Printer on 6th floor not working",
            description=(
                "Hi   IT    Support,\n\n\n\n\n"
                "The    printer   on    the   6th   floor    near   conference   "
                "room   B   is     not     working.\n\n\n\n\n\n\n"
                "It    is    a    HP    LaserJet    Pro    MFP    M428fdn    and   "
                "the     display     says     \"Paper   Jam\"     but     I   "
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
                "Olivia     Santos\n\n\n"
                "Client     Advisory,     6th     Floor,     Building   1"
            ),
            category=Category.HARDWARE,
            priority=Priority.P3,
            team=Team.ENDPOINT,
            needs_escalation=False,
            missing_info=[MissingInfo.DEVICE_INFO],
            next_best_action=(
                "Dispatch a technician to inspect the HP LaserJet Pro MFP M428fdn on "
                "the 6th floor near conference room B, Building 1 — persistent false "
                "paper jam error. User has a client presentation at 3 PM today."
            ),
            remediation_steps=[
                "Dispatch a technician to the 6th floor, Building 1, to physically "
                "inspect the HP LaserJet Pro MFP M428fdn.",
                "Check the paper path sensors for debris, torn paper fragments, or sensor "
                "misalignment causing the false jam.",
                "Perform a full power cycle with the rear access panel open and inspect "
                "the fuser area for obstructions.",
                "If the sensor is faulty, replace the paper path sensor assembly or swap in "
                "a loaner printer before the 3 PM deadline.",
                "Update the printer asset record with any parts replaced and schedule preventive maintenance.",
            ],
            reporter_name="Olivia Santos",
            reporter_email="olivia.santos@contoso.com",
            reporter_department="Client Advisory",
            channel=Channel.CHAT,
            tags=["data-cleanup", "excessive-whitespace", "formatting-noise", "blank-lines"],
            difficulty="easy",
        ),
        # ── DC-048  Corrupted email headers mixed into body ───────────────
        ScenarioDefinition(
            scenario_id="DC-048",
            subject="Account locked out — need urgent help",
            description=(
                "Return-Path: <marcus.adeyemi@contoso.com>\n"
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
                "My account has been locked out and I cannot log into anything — "
                "not my laptop, not Outlook, not any of the internal web apps. "
                "This happened at around 8:30 AM this morning when I tried to "
                "sign in after arriving at the office.\n\n"
                "I did NOT change my password recently and I am certain I am "
                "entering the correct credentials. I suspect the lockout may be "
                "related to the MFA push notifications I was getting last night "
                "around 11 PM that I did not initiate — I denied all of them. "
                "Someone may be trying to access my account.\n\n"
                "This is urgent because I have a compliance audit review at "
                "10 AM and I need access to the Regulatory Reporting portal "
                "and my email.\n\n"
                "Please call me at extension 3841.\n\n"
                "Marcus Adeyemi\n"
                "Compliance & Regulatory, Building 2, 9th floor"
            ),
            category=Category.ACCESS_AUTH,
            priority=Priority.P2,
            team=Team.IAM,
            needs_escalation=True,
            missing_info=[MissingInfo.AUTHENTICATION_METHOD, MissingInfo.TIMESTAMP],
            next_best_action=(
                "Immediately investigate account lockout for Marcus Adeyemi — "
                "unsolicited MFA prompts at 11 PM suggest a possible credential "
                "compromise attempt. Unlock the account, force a password reset, "
                "review Azure AD sign-in logs, and revoke active sessions before "
                "the 10 AM compliance audit."
            ),
            remediation_steps=[
                "Review Azure AD sign-in logs for Marcus Adeyemi's account for failed "
                "attempts and the unsolicited MFA prompts from 11 PM.",
                "Check if the account triggered any Impossible Travel or Unfamiliar "
                "Sign-In Properties risk detections in Azure AD Identity Protection.",
                "Unlock the account in Active Directory and force an immediate password "
                "reset via a secure channel (phone verification).",
                "Revoke all active refresh tokens and sessions "
                "(Revoke-AzureADUserAllRefreshToken) to invalidate any compromised sessions.",
                "If credential compromise is confirmed, escalate to the Security Operations "
                "team for a full incident investigation.",
            ],
            reporter_name="Marcus Adeyemi",
            reporter_email="marcus.adeyemi@contoso.com",
            reporter_department="Compliance & Regulatory",
            channel=Channel.PHONE,
            tags=["data-cleanup", "corrupted-headers", "smtp-headers", "raw-email"],
            difficulty="hard",
        ),
    ]
