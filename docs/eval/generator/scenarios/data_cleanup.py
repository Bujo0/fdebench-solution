"""Data cleanup edge-case scenario definitions.

Covers: long email threads, base64 content, HTML-heavy emails, garbled encoding,
emoji-heavy messages, repeated content, massive signatures, mixed languages,
truncated messages, log dumps, HTML entities, and duplicate sentences.
"""

from generator.models import Scenario

SCENARIOS: list[Scenario] = [
    # ──────────────────────────────────────────────────────────────────
    # 1. Long email thread with deeply nested RE:/FW: replies
    # ──────────────────────────────────────────────────────────────────
    Scenario(
        scenario_id="cleanup-long-nested-email-thread",
        category="Software & Applications",
        priority="P3",
        assigned_team="Enterprise Applications",
        needs_escalation=False,
        missing_information=["error_message", "application_version"],
        subjects=[
            "RE: RE: RE: FW: RE: RE: FW: Outlook keeps crashing when I open large mailbox",
            "FW: FW: RE: RE: RE: FW: RE: FW: RE: Application timeout issue — forwarding again",
        ],
        descriptions=[
            "-----Original Message-----\nFrom: Jane Smith\nSent: Monday 9:00 AM\nTo: Help Desk\n\n"
            "> > > > > On Fri, user wrote:\n> > > > > > On Thu, manager wrote:\n> > > > > > > "
            "Forwarding this again — the original issue is that Outlook freezes every time I try to open "
            "my mailbox. It started after the last update. I've restarted multiple times.\n"
            "> > > > > >\n> > > > > > Adding IT to the chain. Can someone look into this?\n"
            "> > > > >\n> > > > > Still happening. Very frustrating.\n"
            "> > > >\n> > > > +1, same issue on my end.\n"
            "> > >\n> > > Has anyone heard back from IT on this?\n"
            "> >\n> > Bumping this thread. It's been a week now.\n"
            ">\n> Forwarding to help desk directly. PLEASE HELP.\n\n"
            "Hi team, I'm the original reporter. Outlook 365 desktop app crashes within 30 seconds of "
            "opening. My mailbox is about 15 GB. Error: 'Microsoft Outlook is not responding.'",
            "RE: RE: RE: RE: FW: RE: Outlook crash\n\n"
            "--- Forwarded 6 times ---\n"
            "Buried in this thread: Outlook 365 on Windows 11 crashes on launch. Mailbox is oversized at "
            "~18 GB. User has tried safe mode, repair install, and clearing the OST file. Issue persists "
            "across two different machines. Possibly a corrupt mailbox profile or server-side rule.",
        ],
        next_best_actions=[
            "Extract the core issue from the email thread: Outlook crash on large mailbox. Check mailbox "
            "size limits and server-side rules.",
            "Create a new OST file and verify mailbox health via Exchange admin center.",
        ],
        remediation_steps=[
            [
                "Create a new Outlook profile to rule out profile corruption",
                "Check mailbox size and archive old emails to reduce below quota",
                "Clear and regenerate the OST file",
                "Check for problematic server-side inbox rules",
                "If issue persists, escalate to Exchange admin for mailbox health check",
            ],
        ],
        tags=["data-cleanup", "long-email", "nested-thread"],
    ),
    # ──────────────────────────────────────────────────────────────────
    # 2. Base64-encoded image data inline in email
    # ──────────────────────────────────────────────────────────────────
    Scenario(
        scenario_id="cleanup-base64-inline-image",
        category="Hardware & Peripherals",
        priority="P3",
        assigned_team="Endpoint Engineering",
        needs_escalation=False,
        missing_information=["device_info", "error_message"],
        subjects=[
            "Monitor flickering — screenshot attached inline",
            "Display issues with docking station (see embedded image)",
        ],
        descriptions=[
            "My external monitor keeps flickering every few seconds when connected via the docking station. "
            "Here is a screenshot of the issue:\n\n"
            "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDw"
            "ADHGAL/XYZFAKEBASE64DATATHATSHOULDNOTCONFUSETHECLASSIFIER/ABIIBgIABwAAARAABCCAQAA"
            "AABJRU5ErkJggg==\n\n"
            "It happens about every 10 seconds and makes it impossible to work. The monitor works fine "
            "when connected directly via HDMI without the dock.",
            "External display connected through USB-C dock flickers and occasionally goes black for 2-3 "
            "seconds. I tried to embed a photo of the error but my email client pasted it as raw data:\n\n"
            "[base64 data: /9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAgGBgcGBQgHBwcJCQgKDBQNDAsLDBkSEw8UHRof"
            "Hh0aHBwgJC4nICIsIxwcKDcpLDAxNDQ0Hyc5PTgyPC4zNDL/FAKEBASE64CONTINUES...]\n\n"
            "The dock is a Lenovo ThinkPad USB-C Dock Gen 2. Monitor is Dell U2722D.",
        ],
        next_best_actions=[
            "Ignore the base64 image data and focus on the hardware issue: monitor flickering through "
            "docking station. Check dock firmware and cable.",
            "Update docking station firmware and test with a different USB-C cable.",
        ],
        remediation_steps=[
            [
                "Update the docking station firmware to the latest version",
                "Test with a different USB-C or Thunderbolt cable",
                "Try a different video output port on the dock (DisplayPort vs HDMI)",
                "If the issue persists, test with a replacement docking station",
            ],
        ],
        tags=["data-cleanup", "base64", "inline-image"],
    ),
    # ──────────────────────────────────────────────────────────────────
    # 3. HTML-heavy email with tags, styles, entities
    # ──────────────────────────────────────────────────────────────────
    Scenario(
        scenario_id="cleanup-html-heavy-email",
        category="Software & Applications",
        priority="P3",
        assigned_team="Enterprise Applications",
        needs_escalation=False,
        missing_information=["application_version", "steps_to_reproduce"],
        subjects=[
            "<div style='color:red'>Excel crashes on open</div> — HELP",
            'RE: <span class="urgent">Spreadsheet macro error</span>',
        ],
        descriptions=[
            '<html><body><div style="font-family: Calibri, sans-serif; font-size: 11pt;">'
            '<p style="margin: 0; padding: 0;"><b>Hi IT Team,</b></p>'
            '<p style="color: #cc0000; font-weight: bold;">URGENT ISSUE:</p>'
            '<table border="1" cellpadding="5"><tr><td>Application</td><td>Excel 365</td></tr>'
            "<tr><td>Error</td><td>Crashes on file open</td></tr>"
            "<tr><td>Frequency</td><td>Every time</td></tr></table>"
            "<p>Every time I try to open the Q4 budget spreadsheet (about 50 MB with macros), Excel "
            "crashes immediately. I get a &quot;Microsoft Excel has stopped working&quot; dialog. "
            "I&apos;ve tried disabling macros on open but it still crashes.</p>"
            '<p style="color: gray; font-size: 9pt;">Sent from my corporate workstation</p>'
            "</div></body></html>",
            '<div class="email-body"><p>Excel 365 keeps crashing when I open a specific macro-enabled '
            "workbook (.xlsm). The file is ~45&nbsp;MB and has VBA macros plus external data connections. "
            "I&#39;ve tried opening in Safe Mode and repairing the Office installation. "
            "The &lt;error dialog&gt; just says &quot;Excel stopped working.&quot;</p>"
            '<br/><hr style="border: 1px solid #ccc;"/>'
            '<p style="font-size: 8pt; color: #999;">This email and any attachments are '
            "confidential...</p></div>",
        ],
        next_best_actions=[
            "Strip HTML formatting and focus on the core issue: Excel crashing on large macro-enabled "
            "workbook. Check Office repair and file corruption.",
            "Try opening the file in Excel Online to isolate client-side vs file-level corruption.",
        ],
        remediation_steps=[
            [
                "Attempt to open the workbook in Excel Online to test for file corruption",
                "Run an Office repair (Quick Repair, then Online Repair if needed)",
                "Try opening the file with macros disabled via Trust Center settings",
                "If the file is corrupt, recover from a previous version or backup",
            ],
        ],
        tags=["data-cleanup", "html-heavy", "html-tags"],
    ),
    # ──────────────────────────────────────────────────────────────────
    # 4. Garbled/encoding-corrupted text
    # ──────────────────────────────────────────────────────────────────
    Scenario(
        scenario_id="cleanup-garbled-encoding",
        category="Network & Connectivity",
        priority="P2",
        assigned_team="Network Operations",
        needs_escalation=False,
        missing_information=["network_location", "error_message", "environment_details"],
        subjects=[
            "VPN disconnects â€” canâ€\x99t stay connected for more than 5 min",
            "Ã©chec de connexion VPN — keeps dropping (encoding issue in subject too)",
        ],
        descriptions=[
            "Hi team,\n\n"
            "Iâ€\x99m having trouble with the VPN. Every time I connect it drops after about 5 minutes. "
            "The error says â€œGateway not reachableâ€\x9d but my internet is fine. Iâ€\x99ve tried "
            "reinstalling the client but same issue. My colleague on the same network doesnâ€\x99t "
            "have this problem.\n\n"
            "Thanks,\nJohn â€” Finance Department",
            "VPN keeps disconnecting. Error message is garbled on my screen: "
            "ÃƒÂ¢Ã¢â€šÂ¬Ã…â€œConnection timed outÃƒÂ¢Ã¢â€šÂ¬Ã‚Â. "
            "IÃ¢â‚¬â„¢ve been dealing with this for three days. Using GlobalProtect on Windows 11. "
            "Home network, wired connection. Speed test shows 100 Mbps down / 20 up. "
            "Other apps work fine Ã¢â‚¬â€œ itÃ¢â‚¬â„¢s only VPN.",
        ],
        next_best_actions=[
            "Look past the encoding artifacts — core issue is repeated VPN disconnects with 'Gateway not "
            "reachable' error. Check VPN gateway health and client configuration.",
            "Verify VPN gateway connectivity and check for split-tunnel misconfiguration.",
        ],
        remediation_steps=[
            [
                "Check VPN gateway health and current load",
                "Verify the user's VPN client version matches the current supported version",
                "Review split-tunnel configuration on the user's VPN profile",
                "Collect VPN client debug logs during a disconnection event",
                "If gateway is healthy, try reassigning the user to an alternate gateway",
            ],
        ],
        tags=["data-cleanup", "garbled-encoding", "mojibake"],
    ),
    # ──────────────────────────────────────────────────────────────────
    # 5. Emoji-heavy chat message
    # ──────────────────────────────────────────────────────────────────
    Scenario(
        scenario_id="cleanup-emoji-heavy-chat",
        category="Software & Applications",
        priority="P3",
        assigned_team="Enterprise Applications",
        needs_escalation=False,
        missing_information=["application_version", "steps_to_reproduce"],
        subjects=[
            "🚨🚨🚨 Teams won't load!!! 😭😭😭 HELP 🆘🆘🆘",
            "😤😤 CAN'T LOGIN TO TEAMS 🔥🔥🔥 pls fix asap 🙏🙏🙏",
        ],
        descriptions=[
            "OMG 😱😱😱 Teams has been broken ALL DAY!! 💀💀💀\n\n"
            "Every time I open it I get a white screen ⬜⬜⬜ and then it just crashes 💥💥\n\n"
            "I've tried:\n"
            "✅ Restarting my computer 💻\n"
            "✅ Clearing the cache 🗑️\n"
            "✅ Reinstalling Teams 🔄\n"
            "❌ Nothing works!!! 😡😡😡\n\n"
            "I have a SUPER important meeting 📅 in 30 min and I NEED this fixed NOW!!! "
            "🙏🙏🙏🙏🙏\n\n"
            "My laptop is a Dell Latitude 5520 running Windows 11 👨‍💻",
            "hey 👋 so teams is totally borked 🤦‍♂️🤦‍♂️🤦‍♂️\n\n"
            "i click the icon ➡️ it opens ➡️ shows loading spinner 🔄 for like 2 min ⏰ "
            "➡️ then white screen ⬜ ➡️ crash 💥\n\n"
            "tried the web version 🌐 and that works fine ✅ so its def the desktop app 🖥️\n\n"
            "pls help 🆘🆘🆘 thx 😊👍",
        ],
        next_best_actions=[
            "Look past the emojis — core issue is Teams desktop app crashing with a white screen. "
            "Cache may be corrupt. Clear Teams AppData and reinstall.",
            "Clear the Teams cache directories and perform a clean reinstall of the desktop client.",
        ],
        remediation_steps=[
            [
                "Fully quit Teams and end all Teams processes in Task Manager",
                "Delete the Teams cache folder at %AppData%\\Microsoft\\Teams",
                "Reinstall the Teams desktop client from the official source",
                "If the issue persists, check for conflicting Outlook or Office add-ins",
            ],
        ],
        tags=["data-cleanup", "emoji-heavy", "chat-message"],
    ),
    # ──────────────────────────────────────────────────────────────────
    # 6. Excessive repeated/copy-pasted content (error log duplicated)
    # ──────────────────────────────────────────────────────────────────
    Scenario(
        scenario_id="cleanup-repeated-content",
        category="Software & Applications",
        priority="P2",
        assigned_team="Enterprise Applications",
        needs_escalation=False,
        missing_information=["application_version", "environment_details"],
        subjects=[
            "SAP keeps throwing the same error — see pasted log",
            "Application error repeating nonstop — copied the full log below",
        ],
        descriptions=[
            "SAP GUI crashes every time I try to run a report. Here's the error I keep getting:\n\n"
            "ERROR 2024-01-15 09:00:01 - Transaction ABORTED: memory allocation failure in module FI_GL\n"
            "ERROR 2024-01-15 09:00:01 - Transaction ABORTED: memory allocation failure in module FI_GL\n"
            "ERROR 2024-01-15 09:00:01 - Transaction ABORTED: memory allocation failure in module FI_GL\n"
            "ERROR 2024-01-15 09:00:02 - Transaction ABORTED: memory allocation failure in module FI_GL\n"
            "ERROR 2024-01-15 09:00:02 - Transaction ABORTED: memory allocation failure in module FI_GL\n"
            "ERROR 2024-01-15 09:00:02 - Transaction ABORTED: memory allocation failure in module FI_GL\n"
            "ERROR 2024-01-15 09:00:03 - Transaction ABORTED: memory allocation failure in module FI_GL\n"
            "ERROR 2024-01-15 09:00:03 - Transaction ABORTED: memory allocation failure in module FI_GL\n"
            "ERROR 2024-01-15 09:00:03 - Transaction ABORTED: memory allocation failure in module FI_GL\n"
            "ERROR 2024-01-15 09:00:04 - Transaction ABORTED: memory allocation failure in module FI_GL\n\n"
            "This repeats hundreds of times. The report I'm trying to run is the GL account balance "
            "for fiscal year 2024. It used to work fine until last week.",
            "The SAP financial module keeps crashing with a memory error. I copied the error log — "
            "it's the same line over and over:\n\n"
            "DUMP: TSV_TNEW_PAGE_ALLOC_FAILED | Time: 09:15:22 | User: JDOE | Client: 100\n"
            "DUMP: TSV_TNEW_PAGE_ALLOC_FAILED | Time: 09:15:22 | User: JDOE | Client: 100\n"
            "DUMP: TSV_TNEW_PAGE_ALLOC_FAILED | Time: 09:15:22 | User: JDOE | Client: 100\n"
            "DUMP: TSV_TNEW_PAGE_ALLOC_FAILED | Time: 09:15:22 | User: JDOE | Client: 100\n"
            "DUMP: TSV_TNEW_PAGE_ALLOC_FAILED | Time: 09:15:22 | User: JDOE | Client: 100\n"
            "DUMP: TSV_TNEW_PAGE_ALLOC_FAILED | Time: 09:15:22 | User: JDOE | Client: 100\n\n"
            "(This goes on for pages.) The report worked fine two weeks ago. Nothing changed on my end.",
        ],
        next_best_actions=[
            "De-duplicate the repeated log lines and focus on the root cause: SAP memory allocation "
            "failure during GL report execution. Check SAP application server memory.",
            "Investigate SAP application server memory allocation and recent transport changes.",
        ],
        remediation_steps=[
            [
                "Check SAP application server memory allocation and work process availability",
                "Review transaction ST22 for ABAP short dump details",
                "Check if recent transports or configuration changes affected the FI module",
                "Increase memory allocation for the report if the data volume has grown",
            ],
        ],
        tags=["data-cleanup", "repeated-content", "log-duplication"],
    ),
    # ──────────────────────────────────────────────────────────────────
    # 7. Massive email signature and legal disclaimer
    # ──────────────────────────────────────────────────────────────────
    Scenario(
        scenario_id="cleanup-massive-signature",
        category="Access & Authentication",
        priority="P2",
        assigned_team="Identity & Access Management",
        needs_escalation=False,
        missing_information=["error_message", "authentication_method"],
        subjects=[
            "Can't reset my password — locked out since this morning",
            "Password reset not working — need access urgently",
        ],
        descriptions=[
            "I tried to reset my password through the self-service portal this morning but it keeps "
            "saying 'An error has occurred.' I've been locked out of everything since 8 AM and have "
            "client calls starting at 10.\n\n"
            "────────────────────────────────────────\n"
            "Jane M. Richardson, CPA, CFE\n"
            "Senior Vice President | Financial Advisory Services\n"
            "Contoso International Holdings, Ltd.\n"
            "1234 Corporate Parkway, Suite 5600\n"
            "New York, NY 10001\n"
            "Office: +1 (212) 555-0147 | Mobile: +1 (917) 555-0293\n"
            "Fax: +1 (212) 555-0148\n"
            "Email: jane.richardson@contoso.com\n"
            "Web: https://www.contoso.com/advisory\n"
            "LinkedIn: linkedin.com/in/janerichardson\n\n"
            "🌿 Please consider the environment before printing this email.\n\n"
            "CONFIDENTIALITY NOTICE: This email message, including any attachments, is for the sole "
            "use of the intended recipient(s) and may contain confidential and privileged information. "
            "Any unauthorized review, use, disclosure, or distribution is prohibited. If you are not "
            "the intended recipient, please contact the sender by reply email and destroy all copies "
            "of the original message. Receipt by anyone other than the intended recipient is not a "
            "waiver of any attorney-client, work product, or other applicable privilege.\n\n"
            "IRS CIRCULAR 230 DISCLOSURE: To ensure compliance with requirements imposed by the IRS, "
            "we inform you that any tax advice contained in this communication (including any "
            "attachments) is not intended or written to be used, and cannot be used, for the purpose "
            "of (i) avoiding penalties under the Internal Revenue Code or (ii) promoting, marketing "
            "or recommending to another party any transaction or matter addressed herein.\n"
            "────────────────────────────────────────",
            "Password reset link from the self-service portal returns a generic error page. I need "
            "access restored ASAP for a 10 AM meeting.\n\n"
            "──\nMark Thompson | Director of Operations | Contoso Global | "
            "+1-555-0199 | mark.thompson@contoso.com\n\n"
            "DISCLAIMER: The information in this email is confidential and intended solely for the "
            "addressee. Access to this email by anyone else is unauthorized. If you received this in "
            "error, notify the sender immediately and delete all copies. Contoso Global accepts no "
            "liability for any damage caused by any virus transmitted by this email. Views expressed "
            "are those of the individual and not necessarily of the company. This email has been "
            "scanned for viruses by Contoso Global Security. All email communications may be "
            "monitored and stored for regulatory and compliance purposes.\n──",
        ],
        next_best_actions=[
            "Ignore the signature and disclaimer — core issue is a failed self-service password reset. "
            "Issue a temporary access pass and investigate the SSPR portal error.",
            "Verify the user's identity and issue a temporary access pass while troubleshooting SSPR.",
        ],
        remediation_steps=[
            [
                "Verify the user's identity through an alternate channel",
                "Issue a temporary access pass for immediate access",
                "Investigate the SSPR portal error logs for the failed reset attempt",
                "If SSPR is broken for multiple users, escalate to Entra ID team",
            ],
        ],
        tags=["data-cleanup", "massive-signature", "legal-disclaimer"],
    ),
    # ──────────────────────────────────────────────────────────────────
    # 8. Mixed languages (English + Chinese/French/Spanish)
    # ──────────────────────────────────────────────────────────────────
    Scenario(
        scenario_id="cleanup-mixed-languages",
        category="Software & Applications",
        priority="P3",
        assigned_team="Enterprise Applications",
        needs_escalation=False,
        missing_information=["application_version", "environment_details", "error_message"],
        subjects=[
            "Outlook同步问题 — Outlook sync problem since this morning",
            "Problème de synchronisation Outlook / Outlook sync issue — URGENT",
        ],
        descriptions=[
            "Hi IT team,\n\n"
            "我的Outlook从今天早上开始无法同步邮件。(My Outlook hasn't been syncing emails since "
            "this morning.) 我已经重启了电脑，也清除了缓存，但问题仍然存在。(I've restarted my "
            "computer and cleared the cache but the problem persists.)\n\n"
            "Error message: 'Cannot connect to server. Verify your connection.' "
            "我的网络连接正常，其他应用都能上网。(My internet is working fine — other apps connect OK.)\n\n"
            "我在上海办公室工作。(I work in the Shanghai office.) Laptop: ThinkPad X1 Carbon, "
            "Windows 11.\n\n"
            "谢谢！(Thanks!)",
            "Bonjour / Hello,\n\n"
            "J'ai un problème avec Outlook qui ne synchronise plus depuis ce matin. "
            "(I have a problem with Outlook — it's not syncing since this morning.)\n\n"
            "El problema empezó después de la actualización de Windows. "
            "(The problem started after the Windows update.)\n\n"
            "I've tried repairing the Office installation but it didn't help. Les autres applications "
            "Office fonctionnent normalement. (Other Office apps work fine.) "
            "¿Pueden ayudarme lo antes posible? (Can you help me ASAP?)\n\n"
            "Merci / Gracias / Thanks",
        ],
        next_best_actions=[
            "Extract the core issue across languages: Outlook not syncing after possible update. "
            "Check Exchange connectivity and Outlook profile.",
            "Verify Exchange server connectivity and run the Microsoft Support and Recovery Assistant.",
        ],
        remediation_steps=[
            [
                "Run the Microsoft Support and Recovery Assistant (SaRA) for Outlook",
                "Check Outlook's connection status (Ctrl+right-click system tray icon)",
                "Verify Exchange Online service health for the user's region",
                "Recreate the Outlook profile if connectivity tests pass but sync fails",
            ],
        ],
        tags=["data-cleanup", "mixed-languages", "multilingual"],
    ),
    # ──────────────────────────────────────────────────────────────────
    # 9. Truncated/cut-off message
    # ──────────────────────────────────────────────────────────────────
    Scenario(
        scenario_id="cleanup-truncated-message",
        category="Network & Connectivity",
        priority="P2",
        assigned_team="Network Operations",
        needs_escalation=False,
        missing_information=["error_message", "network_location", "steps_to_reproduce"],
        subjects=[
            "WiFi keeps dropping — can't stay conn",
            "Network issue on 3rd floor — urgent, affecting mul",
        ],
        descriptions=[
            "Hi, I've been having WiFi issues all week. Every 15-20 minutes the connection drops "
            "completely and I have to reconnect. The SSID is CORP-WIFI-5G. I'm on the 3rd floor near "
            "conference room B. I've noticed it happens more during lunchtime when more people are "
            "around. My laptop is a Dell Latitude 5530 with Intel AX211 WiFi adapter. I've tried "
            "forgetting and reconnecting to the network but the problem keeps happening. The error "
            "in Windows says 'Limited connectivity' and then it drops to 'No internet.' I've also "
            "noticed that the 2.4 GHz network seems more stable but it's much sl",
            "Multiple users on the third floor are reporting intermittent WiFi dropouts since Monday. "
            "Affected area appears to be the east wing near rooms 301-310. At least 8 users have "
            "complained. We suspect the access point might need replacing or there's interference "
            "from the new equipment installed in",
        ],
        next_best_actions=[
            "Despite the truncation, the core issue is clear: WiFi dropouts on 3rd floor. Check AP "
            "health, channel utilization, and potential interference.",
            "Investigate the 3rd floor access point health and check for RF interference.",
        ],
        remediation_steps=[
            [
                "Check the 3rd floor access point health and uptime via the wireless controller",
                "Run a wireless site survey to identify interference or dead zones",
                "Check channel utilization and consider adjusting channel assignments",
                "If AP is degraded, replace or add additional access points for coverage",
            ],
        ],
        tags=["data-cleanup", "truncated", "cut-off"],
    ),
    # ──────────────────────────────────────────────────────────────────
    # 10. Application log dump pasted into ticket
    # ──────────────────────────────────────────────────────────────────
    Scenario(
        scenario_id="cleanup-log-dump",
        category="Software & Applications",
        priority="P2",
        assigned_team="Enterprise Applications",
        needs_escalation=False,
        missing_information=["steps_to_reproduce", "business_impact"],
        subjects=[
            "CRM application error — pasting full log below",
            "Salesforce integration broken — here's the debug output",
        ],
        descriptions=[
            "CRM integration stopped working. Here is the log:\n\n"
            "[2024-01-15T08:00:01.123Z] INFO  AppInit: Starting CRM Connector v4.2.1\n"
            "[2024-01-15T08:00:01.456Z] INFO  AppInit: Loading configuration from /etc/crm/config.yml\n"
            "[2024-01-15T08:00:01.789Z] DEBUG ConfigLoader: Parsed 47 configuration entries\n"
            "[2024-01-15T08:00:02.001Z] INFO  DBPool: Establishing connection pool (min=5, max=20)\n"
            "[2024-01-15T08:00:02.345Z] INFO  DBPool: Connected to db-prod-east-1.contoso.internal:5432\n"
            "[2024-01-15T08:00:02.678Z] DEBUG AuthModule: Refreshing OAuth token for service account\n"
            "[2024-01-15T08:00:03.012Z] ERROR AuthModule: Token refresh failed — HTTP 401 Unauthorized\n"
            '[2024-01-15T08:00:03.013Z] ERROR AuthModule: Response: {"error": "invalid_client", '
            '"error_description": "client secret has expired"}\n'
            "[2024-01-15T08:00:03.014Z] FATAL CRMConnector: Cannot authenticate to Salesforce API\n"
            "[2024-01-15T08:00:03.015Z] FATAL CRMConnector: Shutting down — unrecoverable auth error\n"
            "[2024-01-15T08:00:03.100Z] INFO  AppShutdown: Cleanup complete. Exit code: 1\n\n"
            "Please fix ASAP — sales team can't log activities.",
            "The Salesforce integration has been down since yesterday. I grabbed the log output "
            "from the server. Most of it is normal startup but the key error is an authentication "
            "failure — looks like the client secret expired. The sales team is manually entering "
            "data, which they can't sustain for long.\n\n"
            "[DEBUG] OAuth2TokenProvider: token_endpoint=https://login.salesforce.com/services/oauth2/token\n"
            "[DEBUG] OAuth2TokenProvider: client_id=3MVG9...truncated\n"
            "[ERROR] OAuth2TokenProvider: grant_type=client_credentials returned 401\n"
            '[ERROR] OAuth2TokenProvider: {"error":"invalid_client"}\n'
            "[FATAL] SalesforceSync: Aborting sync cycle — no valid access token",
        ],
        next_best_actions=[
            "The key error in the log is an expired client secret for the Salesforce OAuth integration. "
            "Rotate the client secret and update the CRM connector configuration.",
            "Renew the Salesforce OAuth client secret and restart the CRM connector service.",
        ],
        remediation_steps=[
            [
                "Rotate the Salesforce Connected App client secret",
                "Update the client secret in the CRM connector configuration",
                "Restart the CRM connector service and verify authentication succeeds",
                "Set up a secret expiration alert to prevent future occurrences",
            ],
        ],
        tags=["data-cleanup", "log-dump", "verbose-logs"],
    ),
    # ──────────────────────────────────────────────────────────────────
    # 11. HTML entities throughout (&amp; &quot; etc.)
    # ──────────────────────────────────────────────────────────────────
    Scenario(
        scenario_id="cleanup-html-entities",
        category="Access & Authentication",
        priority="P2",
        assigned_team="Identity & Access Management",
        needs_escalation=False,
        missing_information=["error_message", "authentication_method", "affected_system"],
        subjects=[
            "SSO login fails &mdash; &quot;invalid token&quot; error on every attempt",
            "Can&apos;t access SharePoint &amp; OneDrive &mdash; SSO broken",
        ],
        descriptions=[
            "I can&apos;t log into SharePoint or OneDrive since this morning. The SSO page shows "
            "&quot;Authentication failed: invalid_token&quot; every time I try. I&apos;ve cleared "
            "my browser cache &amp; cookies, tried Edge, Chrome, &amp; Firefox &mdash; same result "
            "in all of them. Other users on my team don&apos;t seem to be affected. My account is "
            "jane.doe@contoso.com &amp; I&apos;m in the Marketing department. Last successful login "
            "was yesterday at approximately 5:00&nbsp;PM EST.",
            "SSO is completely broken for me. Trying to access any Microsoft 365 app gives: "
            "&lt;error&gt;AADSTS700016: Application with identifier &apos;xxxx&apos; was not found "
            "&amp; may not have been registered.&lt;/error&gt; I haven&apos;t changed anything "
            "&mdash; this started after I was moved to a new security group yesterday. My manager "
            "&amp; the rest of the team can still log in fine.",
        ],
        next_best_actions=[
            "Look past the HTML entity encoding — core issue is SSO authentication failure. Check "
            "Entra ID sign-in logs and the user's group membership changes.",
            "Review recent Entra ID group membership changes and check conditional access policies.",
        ],
        remediation_steps=[
            [
                "Check Entra ID sign-in logs for the specific error code",
                "Review recent group membership or license changes for the user",
                "Verify conditional access policies are not blocking the user's new group",
                "If needed, re-add the user to the correct security groups and clear token cache",
            ],
        ],
        tags=["data-cleanup", "html-entities", "encoded-text"],
    ),
    # ──────────────────────────────────────────────────────────────────
    # 12. Duplicate/stuttering sentences
    # ──────────────────────────────────────────────────────────────────
    Scenario(
        scenario_id="cleanup-duplicate-sentences",
        category="Hardware & Peripherals",
        priority="P3",
        assigned_team="Endpoint Engineering",
        needs_escalation=False,
        missing_information=["device_info", "error_message"],
        subjects=[
            "Keyboard typing double letters — keyboard typing double letters on laptop",
            "Mouse cursor jumping around — mouse cursor is jumping around the screen",
        ],
        descriptions=[
            "My laptop keyboard has been typing double characters randomly. My laptop keyboard has "
            "been typing double characters randomly. For example, when I type 'hello' it comes out "
            "as 'heelloo' or 'hhello'. For example, when I type 'hello' it comes out as 'heelloo'. "
            "It doesn't happen with every keystroke but it's frequent enough to make typing very "
            "frustrating. It doesn't happen with every keystroke but it's frequent enough to make "
            "typing very frustrating. I've tried an external keyboard and that works fine, so it's "
            "definitely the built-in keyboard. I've tried an external keyboard and that works fine. "
            "The laptop is a Dell Latitude 5520, about 2 years old. The laptop is a Dell Latitude "
            "5520, about 2 years old.",
            "The trackpad on my laptop is causing the mouse cursor to jump to random positions on "
            "the screen while I'm typing. The trackpad is causing the cursor to jump around while "
            "typing. It seems like my palms might be brushing the trackpad but I've never had this "
            "issue before. My palms might be touching the trackpad but this never happened before. "
            "I've checked the touchpad sensitivity settings and they're set to normal. I checked "
            "touchpad sensitivity — it's normal. It started after the last Windows update. Started "
            "after the latest Windows update.",
        ],
        next_best_actions=[
            "Deduplicate the repeated content — core issue is keyboard double-typing on a Dell "
            "Latitude. Check keyboard debounce settings and hardware diagnostics.",
            "Run Dell hardware diagnostics on the keyboard and check driver updates.",
        ],
        remediation_steps=[
            [
                "Run built-in Dell hardware diagnostics for the keyboard",
                "Update keyboard and touchpad drivers to the latest version",
                "Adjust keyboard repeat delay and touchpad palm rejection settings",
                "If hardware diagnostics show a fault, initiate a warranty repair or replacement",
            ],
        ],
        tags=["data-cleanup", "duplicate-sentences", "stuttering-text"],
    ),
    # ──────────────────────────────────────────────────────────────────
    # 13. Markdown formatting artifacts (unrendered markup in ticket)
    # ──────────────────────────────────────────────────────────────────
    Scenario(
        scenario_id="cleanup-markdown-artifacts",
        category="Software & Applications",
        priority="P3",
        assigned_team="Enterprise Applications",
        needs_escalation=False,
        missing_information=["error_message"],
        subjects=[
            "Teams integration not syncing with calendar",
            "Outlook-Teams calendar sync broken after update",
        ],
        descriptions=[
            "# Issue Report: Teams Calendar Integration Failure\n\n"
            "**Reporter:** Amara Osei\n"
            "**Department:** Client Relations\n\n"
            "## Problem Description\n\n"
            "The Microsoft Teams integration with my Outlook calendar has "
            "completely stopped working. When I schedule a meeting in "
            "**Outlook**, it *does not* appear in **Teams**. "
            "This started after `Teams Desktop Client v24.7.1` update.\n\n"
            "## Steps to Reproduce\n\n"
            "1. Open **Outlook Desktop** and create a new meeting\n"
            "2. Add a Teams link by clicking `Add Teams Meeting`\n"
            "3. Send the invite\n"
            "4. Open **Microsoft Teams** > Calendar tab\n"
            "5. Notice the meeting **does not appear**\n\n"
            "## What I've Tried\n\n"
            "- [x] Signed out and back into Teams\n"
            "- [x] Cleared the Teams cache (`%appdata%\\Microsoft\\Teams\\Cache`)\n"
            "- [x] Restarted my laptop\n"
            "- [ ] Reinstalled Teams (waiting for IT approval)\n\n"
            "## Impact\n\n"
            "I have **5+ client meetings daily** and have already missed "
            "joining two calls.\n\n"
            "---\n\n"
            "```\nTeams Version: 24.7.1.0\nOutlook Version: 16.0.17328.20162\n"
            "OS: Windows 11 Enterprise 23H2\n```\n\n"
            "Please advise. Thanks!",
        ],
        next_best_actions=[
            "Investigate Teams-Outlook calendar sync failure after Teams v24.7.1 update.",
            "Troubleshoot calendar sync — verify Exchange-Teams interop and the Outlook add-in.",
        ],
        remediation_steps=[
            [
                "Verify Exchange-Teams interop prerequisites for the user's mailbox",
                "Check Teams admin center for known issues with client version 24.7.1",
                "Re-register the Teams Outlook add-in via the troubleshooter",
                "Repair the Office installation if the add-in is missing",
                "Approve a clean reinstall of the Teams desktop client as a fallback",
            ],
        ],
        tags=["data-cleanup", "markdown-artifacts", "unrendered-markup"],
    ),
    # ──────────────────────────────────────────────────────────────────
    # 14. Multilingual email disclaimer burying the actual request
    # ──────────────────────────────────────────────────────────────────
    Scenario(
        scenario_id="cleanup-multilingual-disclaimer",
        category="Network & Connectivity",
        priority="P3",
        assigned_team="Network Operations",
        needs_escalation=False,
        missing_information=["network_location", "business_impact"],
        subjects=[
            "VPN access request for new project",
            "Need VPN profile for APAC regional network",
        ],
        descriptions=[
            "Hello IT,\n\n"
            "I have been assigned to the Cross-Border Settlements project and "
            "need VPN access to the APAC regional network (subnet 10.42.0.0/16). "
            "My manager Isabelle Fontaine has already approved this.\n\n"
            "Thanks,\nLukas Brenner\nInternational Operations\n\n"
            "═══════════════════════════════════════════\n"
            "CONFIDENTIALITY NOTICE / AVIS DE CONFIDENTIALITÉ / "
            "VERTRAULICHKEITSHINWEIS / 機密保持に関するご注意 / 保密声明\n"
            "═══════════════════════════════════════════\n\n"
            "ENGLISH: This email is for the sole use of the intended recipient(s) "
            "and may contain confidential information of Contoso Financial Services. "
            "Unauthorized use or distribution is prohibited.\n\n"
            "FRANÇAIS : Ce message est destiné exclusivement au(x) destinataire(s) "
            "prévu(s). Toute utilisation non autorisée est interdite.\n\n"
            "DEUTSCH: Diese E-Mail ist ausschließlich für den vorgesehenen "
            "Empfänger bestimmt. Unbefugte Nutzung ist untersagt.\n\n"
            "日本語：このメールは意図された受信者のみを対象としています。\n\n"
            "中文：本电子邮件仅供指定收件人使用。\n\n"
            "═══════════════════════════════════════════",
        ],
        next_best_actions=[
            "Provision VPN access to the APAC regional network — verify manager approval and configure by end of week.",
        ],
        remediation_steps=[
            [
                "Verify the access request approval from the manager in the governance portal",
                "Create a VPN access profile for the APAC regional network subnet",
                "Assign the profile to the user's AD account and add to the project security group",
                "Send VPN configuration instructions and test connectivity",
                "Set a 90-day review date per the temporary project access policy",
            ],
        ],
        tags=["data-cleanup", "multilingual-disclaimer", "legal-boilerplate", "very-long-email"],
    ),
    # ──────────────────────────────────────────────────────────────────
    # 15. Pure JSON payload from automated monitoring system
    # ──────────────────────────────────────────────────────────────────
    Scenario(
        scenario_id="cleanup-json-monitoring-alert",
        category="Data & Storage",
        priority="P2",
        assigned_team="Data Platform",
        needs_escalation=True,
        missing_information=["previous_ticket_id"],
        subjects=[
            "[ALERT] CRITICAL — disk space threshold exceeded",
            "[MONITORING] CRITICAL: Disk usage above 95% on production SQL node",
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
            '    "os": "Windows Server 2022 Datacenter",\n'
            '    "role": "SQL Server Production Node"\n'
            "  },\n"
            '  "disk_metrics": {\n'
            '    "drive_letter": "E:",\n'
            '    "total_capacity_gb": 2048,\n'
            '    "used_gb": 1946.7,\n'
            '    "percent_used": 95.06,\n'
            '    "growth_rate_gb_per_day": 12.4,\n'
            '    "estimated_days_until_full": 8.2\n'
            "  },\n"
            '  "top_consumers": [\n'
            '    {"database": "AuditLog", "size_gb": 512.8, "growth_30d_gb": 156.3},\n'
            '    {"database": "TradeHistory", "size_gb": 743.2, "growth_30d_gb": 89.1}\n'
            "  ],\n"
            '  "recent_events": [\n'
            '    {"timestamp": "2026-03-16T02:00:00Z", '
            '"event": "AuditLog retention job FAILED"}\n'
            "  ],\n"
            '  "escalation": {"auto_ticket": true, "sla_response_minutes": 60}\n'
            "}",
        ],
        next_best_actions=[
            "Address critical disk space on PROD-SQL-NODE-03 — AuditLog retention "
            "job failure is the most likely cause of accelerated growth.",
        ],
        remediation_steps=[
            [
                "Investigate and fix the failed AuditLog retention job",
                "Manually purge old records past the retention window to reclaim space",
                "Request emergency capacity expansion if free space drops below 5%",
                "Set up a recurring disk space trend report and lower the alert threshold",
            ],
        ],
        tags=["data-cleanup", "json-payload", "machine-generated", "monitoring-alerts"],
    ),
    # ──────────────────────────────────────────────────────────────────
    # 16. Excessive whitespace and blank lines
    # ──────────────────────────────────────────────────────────────────
    Scenario(
        scenario_id="cleanup-excessive-whitespace",
        category="Hardware & Peripherals",
        priority="P3",
        assigned_team="Endpoint Engineering",
        needs_escalation=False,
        missing_information=["device_info"],
        subjects=[
            "Printer on 6th floor not working",
            "Floor    printer    broken — need    help",
        ],
        descriptions=[
            "Hi   IT    Support,\n\n\n\n\n"
            "The    printer   on    the   6th   floor    near   conference   "
            "room   B   is     not     working.\n\n\n\n\n\n\n"
            "It    is    a    HP    LaserJet    Pro    MFP    M428fdn    and   "
            'the     display     says     "Paper   Jam"     but     I   '
            "checked     and     there    is    no     paper     stuck   "
            "anywhere.\n\n\n\n\n\n"
            "I     tried:\n\n\n"
            "-     Turning     it     off     and     on     again\n\n\n"
            "-     Opening     all     the     trays\n\n\n\n\n\n"
            "Nothing     worked.\n\n\n\n\n\n\n\n"
            "Please     send     someone     ASAP.\n\n\n\n\n"
            "Thanks,\n\n\n"
            "Olivia     Santos\n\n\n"
            "Client     Advisory,     6th     Floor",
        ],
        next_best_actions=[
            "Dispatch a technician to inspect the HP LaserJet Pro MFP M428fdn "
            "on the 6th floor — persistent false paper jam error.",
        ],
        remediation_steps=[
            [
                "Dispatch a technician to physically inspect the printer",
                "Check paper path sensors for debris or torn fragments",
                "Perform a full power cycle with the rear access panel open",
                "Replace the paper path sensor if faulty, or swap in a loaner printer",
            ],
        ],
        tags=["data-cleanup", "excessive-whitespace", "formatting-noise", "blank-lines"],
    ),
    # ──────────────────────────────────────────────────────────────────
    # 17. Corrupted SMTP headers mixed into the ticket body
    # ──────────────────────────────────────────────────────────────────
    Scenario(
        scenario_id="cleanup-corrupted-smtp-headers",
        category="Access & Authentication",
        priority="P1",
        assigned_team="Identity & Access Management",
        needs_escalation=True,
        missing_information=["device_info", "authentication_method"],
        subjects=[
            "Account locked out — need urgent help",
            "URGENT: Account lockout — suspicious MFA activity",
        ],
        descriptions=[
            "Return-Path: <marcus.adeyemi@contoso.com>\n"
            "Received: from PROD-EXCH-04.contoso.local (10.20.1.44) by\n"
            " PROD-EXCH-HUB-02.contoso.local (10.20.1.10) with Microsoft SMTP\n"
            " Server (version=TLS1_2) id 15.2.1118.40; Tue, 17 Mar 2026 08:47:12\n"
            "DKIM-Signature: v=1; a=rsa-sha256; c=relaxed/relaxed; d=contoso.com;\n"
            " bh=a3f2V8bKz0mNpQ7RtL1cD+eXwJk=;\n"
            "X-Mailer: Microsoft Outlook 16.0\n"
            "MIME-Version: 1.0\n"
            "Content-Type: multipart/alternative;\n"
            ' boundary="----=_NextPart_001_0078"\n'
            "X-MS-Exchange-Organization-AuthAs: Internal\n\n"
            "Hi IT Support,\n\n"
            "My account has been locked out and I cannot log into anything — "
            "laptop, Outlook, internal web apps. I suspect the lockout is related "
            "to MFA push notifications I was getting last night around 11 PM "
            "that I did not initiate — I denied all of them. Someone may be "
            "trying to access my account.\n\n"
            "This is urgent because I have a compliance audit review at 10 AM.\n\n"
            "Please help ASAP.\n"
            "Marcus Adeyemi\nRegulatory Affairs",
        ],
        next_best_actions=[
            "Investigate account lockout with suspicious MFA activity — possible "
            "unauthorized access attempt. Unlock and review sign-in logs.",
        ],
        remediation_steps=[
            [
                "Unlock the user's account in Entra ID and reset their password securely",
                "Review sign-in logs for failed attempts and suspicious IP addresses",
                "If unauthorized access confirmed, revoke all active sessions and refresh tokens",
                "Advise the user to re-register MFA with number matching or FIDO2",
                "Escalate to Security Operations if credential compromise is indicated",
            ],
        ],
        tags=["data-cleanup", "corrupted-headers", "smtp-headers", "raw-email"],
    ),
    # ──────────────────────────────────────────────────────────────────
    # 18. Very long email with actual issue buried at the end
    # ──────────────────────────────────────────────────────────────────
    Scenario(
        scenario_id="cleanup-very-long-buried-issue",
        category="Network & Connectivity",
        priority="P2",
        assigned_team="Network Operations",
        needs_escalation=False,
        missing_information=["error_message", "network_location"],
        subjects=[
            "FW: FW: RE: RE: Office network issues — adding more context (LONG)",
            "RE: RE: RE: Network outage this morning — scroll to the bottom for details",
            "Re: Multiple issues — the VPN one is at the end of this email",
        ],
        descriptions=[
            "Hi IT,\n\n"
            "First, I want to mention that last month we had a similar situation when the Wi-Fi in "
            "Building C went down for a few hours and nobody could print. That was resolved by Dave "
            "in networking. Also, a few weeks before that, we had the badge readers fail during a "
            "power blip, which caused a lot of confusion at reception. And of course there was the "
            "time the VoIP phones dropped calls for an entire afternoon — I think that was a switch "
            "firmware issue. Oh, and we also had a problem with the guest Wi-Fi SSID not broadcasting "
            "in the lobby, but that turned out to be an AP that needed a reboot.\n\n"
            "Anyway, the reason I'm writing today is completely different. Since about 8 AM this "
            "morning, the VPN connection drops every 15-20 minutes for everyone on the Minneapolis "
            "office subnet (10.45.x.x). When it drops, users get a 'TLS handshake failed' error "
            "and have to reconnect manually. About 30 people are affected and most of our finance "
            "team is remote today.",
            "--- Forwarded message (4th time) ---\n"
            "This email chain started two weeks ago about a different issue that is now resolved. "
            "I'm reusing the thread because I couldn't find the help desk email address.\n\n"
            "Previous topic: printer toner replacement for 3rd floor HP LaserJet — RESOLVED.\n"
            "Previous previous topic: request for a second monitor — COMPLETED.\n"
            "Previous previous previous topic: Adobe Acrobat license renewal — DONE.\n\n"
            "==== ACTUAL NEW ISSUE BELOW ====\n\n"
            "The Minneapolis office VPN concentrator appears to be dropping TLS sessions "
            "intermittently since this morning. Approximately 30 remote finance users are unable "
            "to maintain a stable connection for more than 15 minutes. The GlobalProtect client "
            "shows 'Gateway unreachable' after each disconnect.",
        ],
        next_best_actions=[
            "Extract the actual issue buried in the message: VPN dropping every 15-20 minutes for "
            "the Minneapolis subnet. Investigate the VPN concentrator and TLS configuration.",
            "Check the VPN concentrator health and session limits for the 10.45.x.x subnet.",
        ],
        remediation_steps=[
            [
                "Check the VPN concentrator logs for TLS handshake failures and session drops",
                "Verify the concentrator is not exceeding its maximum concurrent session limit",
                "Review recent certificate or firmware changes on the VPN gateway",
                "Restart the VPN gateway service if logs indicate a memory or process issue",
                "If the issue persists, fail over to the backup VPN concentrator",
            ],
        ],
        tags=["data-cleanup", "buried-issue", "long-email", "irrelevant-context"],
    ),
    # ──────────────────────────────────────────────────────────────────
    # 19. Massive base64-encoded PDF in email body
    # ──────────────────────────────────────────────────────────────────
    Scenario(
        scenario_id="cleanup-base64-pdf-inline",
        category="Software & Applications",
        priority="P3",
        assigned_team="Enterprise Applications",
        needs_escalation=False,
        missing_information=["application_version", "steps_to_reproduce"],
        subjects=[
            "Cannot open quarterly report — pasting PDF contents here",
            "PDF rendering issue in SharePoint — raw file data below",
        ],
        descriptions=[
            "Hi team,\n\n"
            "I'm trying to open the quarterly budget report in SharePoint Online but it just shows "
            "a blank page. I exported the PDF and I'm pasting the raw contents here so you can see "
            "the file:\n\n"
            "JVBERi0xLjQKMSAwIG9iago8PCAvVHlwZSAvQ2F0YWxvZyAvUGFnZXMgMiAwIFIgPj4KZW5k"
            "b2JqCjIgMCBvYmoKPDwgL1R5cGUgL1BhZ2VzIC9LaWRzIFszIDAgUl0gL0NvdW50IDEgPj4K"
            "ZW5kb2JqCjMgMCBvYmoKPDwgL1R5cGUgL1BhZ2UgL1BhcmVudCAyIDAgUiAvTWVkaWFCb3gg"
            "WzAgMCA2MTIgNzkyXSAvQ29udGVudHMgNCAwIFIgL1Jlc291cmNlcyA8PCAvRm9udCA8PCAv"
            "RjEgNSAwIFIgPj4gPj4gPj4KZW5kb2JqCjQgMCBvYmoKPDwgL0xlbmd0aCA0NCA+PgpzdHJl"
            "YW0KQlQKL0YxIDE4IFRmCjEwMCA3MDAgVGQKKEZBS0UgQkFTRTY0IFBERikgVGoKRVQKZW5k"
            "c3RyZWFtCmVuZG9iagpGQUtFX0JBU0U2NF9EQVRBX1JFUEVBVEVEX1RPX1NJTVVMQVRFX0xB"
            "UkdFX1BERl9GSUxFX0NPTlRFTlQ=\n"
            "[...approximately 2 MB of base64 data truncated...]\n\n"
            "The report was created in Adobe Acrobat and uploaded to our team SharePoint site. "
            "Other PDFs seem to render fine, but this particular file always shows blank.",
            "SharePoint document library won't preview a specific PDF — the quarterly financials "
            "report (Q3-2026-Budget-Final.pdf, about 48 pages). I tried downloading and opening "
            "locally in Adobe Reader and it works fine, so the PDF itself isn't corrupt.\n\n"
            "I attempted to paste the file contents below for reference:\n"
            "data:application/pdf;base64,JVBERi0xLjcNCjEgMCBvYmoNCjw8IC9UeXBlIC9DYXRhbG9n"
            "IEZBQ0VJTE9OR0JBU0U2NERBVEFCTE9DS1RIQVRHT0VTT05GT1JNQUdFUw=="
            "\n[...base64 data continues for thousands of lines...]\n\n"
            "This only affects the one file. Could it be a file size limit in SharePoint preview?",
        ],
        next_best_actions=[
            "Ignore the base64-encoded PDF data and focus on the SharePoint Online PDF rendering "
            "issue. Check file size limits for the browser-based PDF previewer.",
            "Verify the PDF file size against SharePoint Online preview limits and test with a different browser.",
        ],
        remediation_steps=[
            [
                "Check the PDF file size against SharePoint Online's browser preview limit (typically 100 MB)",
                "Test the preview in a different browser (Edge, Chrome) to rule out client-side issues",
                "Clear the SharePoint document library cache and re-upload the file",
                "If the file exceeds preview limits, advise the user to download and open locally",
                "Check if the PDF contains non-standard fonts or features unsupported by the web viewer",
            ],
        ],
        tags=["data-cleanup", "base64", "pdf-inline", "large-payload"],
    ),
    # ──────────────────────────────────────────────────────────────────
    # 20. Mobile keyboard autocorrect mangling technical terms
    # ──────────────────────────────────────────────────────────────────
    Scenario(
        scenario_id="cleanup-mobile-autocorrect",
        category="Network & Connectivity",
        priority="P2",
        assigned_team="Network Operations",
        needs_escalation=False,
        missing_information=["error_message", "network_location"],
        subjects=[
            "VPN not conmecting — sent from my iPhoone",
            "WiFi authentification faliure on laptoop — plz help",
        ],
        descriptions=[
            "Sent form my iPhoen\n\n"
            "Hi IT Im havng truoble with the VPN. It says authentification faled when I try "
            "to conect to the Globl Protect clint. I thinck my pasword is corect because I can "
            "log into the emial just fine.\n\n"
            "The eror messge says somthing about a certificat missmatch but I cant coppy the "
            "exact mesage becuz Im on my fone rigt now.\n\n"
            "Im workng remotly from a coffe shop and I need to get onto the corprate netwrk "
            "for a clent call in 30 minits.\n\n"
            "Pleaz help asap\n"
            "Thx\nMarcus",
            "Sendign from mobil — soryr for typoes\n\n"
            "The wifi in the Cihcago offce keeps disconecting. Every 5-10 minuts it drops and "
            "I have to reconect manualy. The SSID is CORP-WIFI-5G and my laptpo is a Dlle "
            "Lattitude 5540. It startd after the weekedn maintnance.\n\n"
            "Othr poeple on the flor are havng the smae isue so I dont thnik its just my mahcine.\n\n"
            "Thankss\nPreya S.",
        ],
        next_best_actions=[
            "Interpret through autocorrect errors: VPN certificate mismatch on GlobalProtect "
            "client. Verify client certificate and user credentials.",
            "Investigate Wi-Fi disconnections on CORP-WIFI-5G in Chicago office after weekend "
            "maintenance — likely AP configuration or channel issue.",
        ],
        remediation_steps=[
            [
                "Verify the user's VPN credentials and certificate validity in the authentication server",
                "Check if the GlobalProtect client has the latest gateway certificate installed",
                "Test connectivity to the VPN gateway from an external network",
                "If certificate mismatch, push the updated root CA certificate to the client",
                "Confirm access by having the user test the VPN connection after remediation",
            ],
        ],
        tags=["data-cleanup", "mobile-autocorrect", "typos", "garbled-text"],
    ),
    # ──────────────────────────────────────────────────────────────────
    # 21. Auto-translated email with translation artifacts
    # ──────────────────────────────────────────────────────────────────
    Scenario(
        scenario_id="cleanup-auto-translated-email",
        category="Software & Applications",
        priority="P3",
        assigned_team="Enterprise Applications",
        needs_escalation=False,
        missing_information=["application_version", "steps_to_reproduce"],
        subjects=[
            "The Excel makes the freezing of itself — translated by machine",
            "Application of SAP is presenting error of grave type [auto-translated]",
        ],
        descriptions=[
            "[This message was automatically translated from Japanese]\n\n"
            "Dear IT support team of the company,\n\n"
            "The application of spreadsheet (Excel) is making the freezing of itself when "
            "the pivot table is being rotated on the data of large size. The file has the "
            "rows of 500,000 and the columns of 45. When I am pressing the button of "
            "'Refresh All' the application becomes the state of 'Not Responding' and the "
            "waiting is required of 10 minutes or the killing of the process is necessary.\n\n"
            "The version of Office is the 365 of enterprise and the Windows is the 11 of "
            "professional. The memory RAM is 16 gigabytes.\n\n"
            "The gratitude is extended,\n"
            "Takeshi Yamamoto\nDepartment of Financial Analysis\n\n"
            "[Original language: 日本語 — confidence: 78%]",
            "[Translated automatically from Portuguese — some terms may be inaccurate]\n\n"
            "Good morning support of TI,\n\n"
            "The SAP system is presenting the error of type 'ABAP runtime error — "
            "TSV_TNEW_PAGE_ALLOC_FAILED' when the report of monthly closing is being "
            "executed. The transaction of code MB52 is the one that fails. The error makes "
            "the appearance after the processing of approximately 2 minutes.\n\n"
            "We have already made the attempt of increasing the parameter of memory in the "
            "profile of instance but the problem makes the persistence. The team of basis "
            "says that the quotas of memory are the correct ones.\n\n"
            "This is blocking the closing of financial month.\n\n"
            "Regards of cordiality,\n"
            "Ana Beatriz Costa\nControllership\n\n"
            "[Idioma original: Português — confiança: 82%]",
        ],
        next_best_actions=[
            "Parse through machine translation artifacts: Excel 365 freezing on large pivot "
            "table refresh (500K rows). Check memory and suggest data model optimization.",
            "Investigate SAP ABAP memory allocation failure on transaction MB52 during month-end "
            "close — likely needs memory parameter tuning or report optimization.",
        ],
        remediation_steps=[
            [
                "Check available system memory and close unnecessary applications before pivot refresh",
                "Recommend converting the data range to a Power Pivot data model for large datasets",
                "Verify that 64-bit Office is installed for handling files with 500K+ rows",
                "If the issue persists, suggest breaking the dataset into smaller pivot table sources",
                "Test with hardware acceleration disabled in Excel options",
            ],
        ],
        tags=["data-cleanup", "auto-translation", "translation-artifacts", "garbled-grammar"],
    ),
    # ──────────────────────────────────────────────────────────────────
    # 22. Extremely short ticket with almost no context
    # ──────────────────────────────────────────────────────────────────
    Scenario(
        scenario_id="cleanup-terse-no-context",
        category="General Inquiry",
        priority="P4",
        assigned_team="Enterprise Applications",
        needs_escalation=False,
        missing_information=[
            "affected_system",
            "error_message",
            "steps_to_reproduce",
            "device_info",
            "business_impact",
        ],
        subjects=[
            "help",
            "it's broken",
            "not working",
        ],
        descriptions=[
            "it doesnt work",
            "broken. pls fix asap",
            "Can someone help? Thing I use every day stopped. Thx.",
        ],
        next_best_actions=[
            "Reply to the reporter requesting basic details: what application or system is "
            "affected, what error they see, and when the issue started.",
            "Ask the reporter to clarify what is broken, what device they are using, and "
            "whether anyone else is affected.",
        ],
        remediation_steps=[
            [
                "Respond to the reporter requesting clarification on the affected system or application",
                "Ask for the specific error message or behavior they are experiencing",
                "Request device and operating system details",
                "Ask when the issue started and whether it affects other users",
                "Once details are provided, re-triage and route to the appropriate team",
            ],
        ],
        tags=["data-cleanup", "terse-ticket", "no-context", "ambiguous"],
    ),
    # ──────────────────────────────────────────────────────────────────
    # 23. Very long email with the real issue buried at the very end (variant 2)
    # ──────────────────────────────────────────────────────────────────
    Scenario(
        scenario_id="cleanup-very-long-buried-issue-v2",
        category="Security & Compliance",
        priority="P2",
        assigned_team="Security Operations",
        needs_escalation=False,
        missing_information=["error_message", "environment_details"],
        subjects=[
            "RE: RE: FW: FW: RE: Several things I wanted to flag — see end of message",
            "FW: RE: FW: RE: RE: Various IT notes, badge issue, Wi-Fi, and a security alert at the bottom",
        ],
        descriptions=[
            "Hi IT,\n\n"
            "Hope you're doing well! Quick update on a few things before I get to my real question.\n\n"
            "1) The new monitors we ordered last month arrived and they look great. The dock adapters "
            "fit perfectly. Thanks for recommending the USB-C ones.\n\n"
            "2) I also wanted to mention that the guest Wi-Fi SSID in the London office lobby was "
            "broadcasting the wrong network name for about a day last week. Someone on the networking "
            "team fixed it, so no action needed.\n\n"
            "3) Our intern asked me about getting a second monitor — I told her to file a ticket, so "
            "you might see that come through.\n\n"
            "4) The coffee machine on Floor 5 keeps tripping the circuit breaker, but I know that's "
            "facilities, not IT. Just venting!\n\n"
            "5) Badge readers at the north entrance were slow yesterday morning but seem fine now.\n\n"
            "OK here is the actual reason I'm writing. Since about 6 AM today our SIEM dashboard is "
            "showing a spike of failed SSH login attempts against the bastion host (bastion-prod-01, "
            "IP 10.200.1.50). Over 12,000 attempts in the last three hours, originating from five "
            "external IPs. The source addresses appear to be from a known botnet range. No successful "
            "authentications yet, but the rate is increasing.",
            "--- Forwarded message chain (7 forwards) ---\n"
            "Original: printer toner request — RESOLVED two weeks ago.\n"
            "Second topic: request for Adobe license — DONE.\n"
            "Third topic: VoIP phone static noise — FIXED by vendor.\n"
            "Fourth topic: monitor arm mounting — COMPLETED by facilities.\n"
            "Fifth topic: Zoom Room calendar sync — RESOLVED after reboot.\n"
            "Sixth topic: shared mailbox permissions — DONE.\n\n"
            "==== NEW ISSUE (the only one that matters) ====\n\n"
            "Starting at approximately 06:00 UTC the bastion host bastion-prod-01 has been "
            "receiving a brute-force SSH attack. Our Splunk alert fired showing 12,400+ failed "
            "auth attempts from IPs in the 185.220.x.x range. Fail2ban is blocking individual "
            "IPs but the attackers are rotating. GeoIP puts the source in Eastern Europe. No "
            "compromise detected so far but we need to tighten firewall rules urgently.",
        ],
        next_best_actions=[
            "Skip the informational preamble and focus on the SSH brute-force attack against "
            "bastion-prod-01. Review firewall rules and consider geo-blocking the source range.",
            "Investigate the SIEM spike — 12k+ failed SSH attempts from known botnet IPs against "
            "the bastion host. Confirm no successful auth and harden access controls.",
        ],
        remediation_steps=[
            [
                "Review SIEM logs to confirm no successful authentication from the attacking IPs",
                "Add a temporary firewall deny rule for the 185.220.x.x source range",
                "Verify fail2ban thresholds and increase the ban duration",
                "Consider restricting SSH access to the bastion host by IP allowlist or VPN only",
                "Escalate to Security Operations if any successful login is found",
            ],
        ],
        tags=["data-cleanup", "buried-issue", "long-email", "irrelevant-preamble"],
    ),
    # ──────────────────────────────────────────────────────────────────
    # 24. Base64-encoded PDF report with TLS certificate issue
    # ──────────────────────────────────────────────────────────────────
    Scenario(
        scenario_id="cleanup-base64-pdf-report",
        category="Network & Connectivity",
        priority="P2",
        assigned_team="Network Operations",
        needs_escalation=False,
        missing_information=["certificate_details", "environment_details"],
        subjects=[
            "TLS cert expired on internal portal — pasting the full PDF audit report",
            "Certificate warning on intranet — attached PDF report inline as base64",
        ],
        descriptions=[
            "Hi Network team,\n\n"
            "Our internal compliance portal (https://compliance.corp.local) started showing "
            "certificate warnings this morning. I ran an SSL audit and exported the report as "
            "a PDF. My email client won't attach it so I'm pasting the raw data:\n\n"
            "data:application/pdf;base64,JVBERi0xLjUKJcOkw7zDtsOfCjIgMCBvYmoKPDwvTGVuZ3RoIDMg"
            "MCBSL0ZpbHRlci9GbGF0ZURlY29kZT4+CnN0cmVhbQpGQUtFQkFTRTY0REFUQVNJTUVTQU5ZUEFH"
            "RVBERlJFUE9SVFdJVEhUTFNDRVJUSUZJQ0FURUFVREVJVFJFU1VMVFNBTkRGSU5ESU5HU0ZSWU9V"
            "UklOVEVSTkFMQ09NUExJQU5DRVBPU1RBTFNTTENIRUNLREVUQU1FRk9SVEVTVA=="
            "\n[...approximately 1.4 MB of base64 data omitted...]\n\n"
            "The short version: the TLS certificate for compliance.corp.local expired yesterday "
            "at 23:59 UTC. It's a wildcard cert (*.corp.local) issued by our internal CA. "
            "Chrome and Edge both block the page with NET::ERR_CERT_DATE_INVALID. About 200 "
            "employees use this portal daily for compliance training.",
            "Users are reporting 'Your connection is not private' errors when accessing the "
            "compliance portal. I generated a certificate transparency report and pasted it "
            "here:\n\n"
            "[BEGIN BASE64 PDF]\n"
            "JVBERi0xLjcKMSAwIG9iago8PCAvVHlwZSAvQ2F0YWxvZyAvUGFnZXMgMiAwIFIgPj4KZW5k"
            "b2JqCkZBS0VfQ0VSVF9SRVBPUlRfQkFTRTY0X0RBVEFfVEhBVF9TSE9VTERfQkVfSUdOT1JF"
            "RF9CWV9USEVfQ0xBU1NJRklFUl9BTkRfVFJJQUdFX1NZU1RFTQ=="
            "\n[END BASE64 PDF — 847 KB]\n\n"
            "The certificate expired on 2026-07-14. It was issued by CorpRootCA and covers "
            "*.corp.local. The portal uses IIS on Windows Server 2022. Other *.corp.local "
            "services (wiki, HR portal) still have valid certs — they were renewed last quarter "
            "but this one was missed.",
        ],
        next_best_actions=[
            "Ignore the base64 PDF data and focus on the expired TLS certificate for "
            "compliance.corp.local. Renew the certificate through the internal CA.",
            "Renew the expired wildcard certificate for *.corp.local on the compliance portal.",
        ],
        remediation_steps=[
            [
                "Generate a new certificate signing request (CSR) for *.corp.local on the IIS server",
                "Submit the CSR to the internal CA (CorpRootCA) for renewal",
                "Install the renewed certificate and bind it to the compliance portal in IIS",
                "Verify the full certificate chain is installed and trusted by client browsers",
                "Set up a certificate expiration monitoring alert to prevent future lapses",
            ],
        ],
        tags=["data-cleanup", "base64", "pdf-inline", "tls-certificate"],
    ),
    # ──────────────────────────────────────────────────────────────────
    # 25. Multi-reply email chain with base64 screenshots
    # ──────────────────────────────────────────────────────────────────
    Scenario(
        scenario_id="cleanup-base64-reply-chain",
        category="Software & Applications",
        priority="P3",
        assigned_team="Enterprise Applications",
        needs_escalation=False,
        missing_information=["application_version", "steps_to_reproduce"],
        subjects=[
            "RE: RE: RE: RE: SAP error — screenshots from everyone in the thread",
            "FW: RE: RE: SAP GUI crashes — adding my screenshot too (see below)",
        ],
        descriptions=[
            "Hi IT,\n\n"
            "Adding my screenshot to the thread. Here are all of them:\n\n"
            "--- Screenshot from Maria (Tuesday) ---\n"
            "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAKCAYAAACNMs+9AAAAE0lEQVQY"
            "V2P4z8BQDwYMDAwAFAAL/FiLbwAAAABJRU5ErkJggg==\n\n"
            "--- Screenshot from James (Wednesday) ---\n"
            "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAMCAgMCAgMDAwMEAwMEBQgF"
            "FAKE_SCREENSHOT_DATA_FROM_JAMES_SHOWING_SAP_ERROR_DIALOG_RUNTIME_EXCEPTION==\n\n"
            "--- Screenshot from Priya (Thursday) ---\n"
            "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAACAAAAAgCAYAAABzenr0AAAAFAKE_PRIYA"
            "_SCREENSHOT_DATA_SAP_TRANSACTION_VA01_DUMP_SCREEN_CAPTURE_FRIDAY==\n\n"
            "--- My screenshot (today, Friday) ---\n"
            "data:image/png;base64,iVBORw0KGgoFAKE_FOURTH_SCREENSHOT_INLINE_BASE64_SAP_SYSTEM"
            "_LOG_SHOWING_ABAP_RUNTIME_ERROR_ST22_TRANSACTION_DUMP_DETAILS_TODAY==\n\n"
            "We're all getting the same SAP error: 'ABAP runtime error TSV_TNEW_PAGE_ALLOC_FAILED' "
            "when running transaction VA01 (create sales order). It started Tuesday after the "
            "transport for change request CR-20260715 was imported into production.",
            "RE: RE: RE: RE: RE: SAP GUI crash — thread with 5 inline screenshots\n\n"
            "> From: Help Desk\n> Can you send screenshots?\n\n"
            "> From: Maria\n> Here's mine:\n"
            "> data:image/png;base64,iVBORw0KGgoAAAAFAKEBASE64MARIA==\n\n"
            "> From: James\n> Mine too:\n"
            "> data:image/jpeg;base64,/9j/FAKEBASE64JAMES==\n\n"
            "> From: Priya\n> Same error, different screen:\n"
            "> data:image/png;base64,iVBORw0FAKEBASE64PRIYA==\n\n"
            "Latest update: four of us in the Sales Operations team cannot create sales orders "
            "in SAP (transaction VA01). The ABAP dump shows TSV_TNEW_PAGE_ALLOC_FAILED, which "
            "means the application server is running out of extended memory for the dialog work "
            "process. This started right after the Tuesday transport.",
        ],
        next_best_actions=[
            "Ignore the base64 screenshot data and focus on the SAP ABAP runtime error. Check the "
            "transport CR-20260715 for memory-intensive changes and SAP extended memory parameters.",
            "Investigate the SAP TSV_TNEW_PAGE_ALLOC_FAILED dump after Tuesday's transport import.",
        ],
        remediation_steps=[
            [
                "Review the ABAP dump via transaction ST22 for details on the memory allocation failure",
                "Check SAP extended memory parameters (em/initial_size_MB, ztta/roll_extension) on the app server",
                "Review transport CR-20260715 for changes that may consume excessive dialog memory",
                "Consider rolling back the transport if it introduced a memory-intensive code change",
                "If parameters are undersized, request a basis admin to increase extended memory allocation",
            ],
        ],
        tags=["data-cleanup", "base64", "reply-chain", "multiple-screenshots"],
    ),
    # ──────────────────────────────────────────────────────────────────
    # 26. Voicemail transcription with speech recognition errors
    # ──────────────────────────────────────────────────────────────────
    Scenario(
        scenario_id="cleanup-speech-transcription-errors",
        category="Hardware & Peripherals",
        priority="P2",
        assigned_team="Data Center Operations",
        needs_escalation=False,
        missing_information=["device_info", "error_message", "environment_details"],
        subjects=[
            "Voicemail transcription from facilities re: server room temperature",
            "Transcribed voicemail — server cooling issue (hard to read)",
        ],
        descriptions=[
            "[Automated Voicemail Transcription — Confidence: 42%]\n\n"
            "Hey this is Rajesh from the fizz uh fizz ickle plant... no, the physical plant "
            "department. I'm calling about the surfer room... the SERVER room on the third "
            "floor. The cool ant... the COOLANT unit on rack row see... rack row C stopped "
            "working around too AM... 2 AM last night and the temp orator... the temperature "
            "has gone up to like 95 fair and height... 95 Fahrenheit which is way above the "
            "red line. The sees are racks... the C-series racks are showing amber lights. "
            "Our HVAC tech said the cry oh jenny... the CRYOGENIC compressor threw a fault "
            "code: E-R-R dash four seven two. We tried re-setting the braker... the breaker "
            "but it tripped again. Some of the servers are starting to thermal throttle. "
            "Please call me back at extension four-seven-three-nine ASAP.\n\n"
            "[End of transcription]",
            "[Auto-transcribed Voicemail — Speaker had strong accent, low confidence]\n\n"
            "Hello I.T., this is Raj from facilities calling about the data scenter... data "
            "center cooling. The air handler unit for rho see... row C is down. Temps are "
            "climbing past ninety-five degrees. The chiller threw error foyer seven too... "
            "error four-seven-two and the kompressor won't restart. We've been running "
            "portable fans but that's a band-aid. The UPS units are also beeping because the "
            "battery room is getting hot as well. The Liebert cool thing... the Liebert "
            "cooling unit model number is D-S-E zero seven five. Our on-site HVAC guy says "
            "the compressor needs a warranty part. Can someone from I.T. check the server "
            "health in the mean time? Extension four-seven-three-nine.",
        ],
        next_best_actions=[
            "Look past the transcription errors — the core issue is a cooling failure in the "
            "server room (row C). CRAC/CRAH unit fault code ERR-472, temps at 95°F and rising.",
            "Contact facilities (ext 4739) and check server health on rack row C for thermal throttling.",
        ],
        remediation_steps=[
            [
                "Contact Rajesh at extension 4739 for a direct status update on the cooling unit",
                "Check server hardware health dashboards for thermal throttling events on rack row C",
                "If temps exceed the critical threshold, initiate a controlled shutdown of non-essential servers",
                "Coordinate with HVAC to expedite the compressor repair (Liebert DSE075, fault ERR-472)",
                "Deploy portable cooling units to the affected row as a temporary measure",
            ],
        ],
        tags=["data-cleanup", "voicemail-transcription", "speech-errors", "phonetic-garble"],
    ),
    # ──────────────────────────────────────────────────────────────────
    # 27. Text with zero-width Unicode characters throughout
    # ──────────────────────────────────────────────────────────────────
    Scenario(
        scenario_id="cleanup-zero-width-unicode",
        category="Software & Applications",
        priority="P3",
        assigned_team="Enterprise Applications",
        needs_escalation=False,
        missing_information=["application_version", "steps_to_reproduce"],
        subjects=[
            "Teams\u200b\u200b\u200b\u200b app\u200b\u200b crashes\u200b\u200b on\u200b start\u200bup",
            "Microsoft\u200b\u200b Teams\u200b\u200b won't\u200b\u200b launch\u200b\u200b after\u200b update",
        ],
        descriptions=[
            "Hi\u200b\u200b IT\u200b\u200b team\u200b,\n\n"
            "Since\u200b\u200b yesterday\u200b's\u200b\u200b update\u200b,\u200b Microsoft\u200b"
            "\u200b Teams\u200b (\u200bversion\u200b 24\u200b.\u200b2\u200b.\u200b1\u200b)"
            "\u200b crashes\u200b\u200b immediately\u200b\u200b on\u200b launch\u200b.\u200b "
            "I\u200b\u200b see\u200b\u200b a\u200b\u200b brief\u200b\u200b splash\u200b screen"
            "\u200b\u200b and\u200b\u200b then\u200b\u200b it\u200b\u200b closes\u200b.\u200b "
            "The\u200b\u200b Windows\u200b\u200b Event\u200b\u200b Viewer\u200b shows\u200b "
            "Application\u200b Error\u200b\u200b with\u200b\u200b faulting\u200b module\u200b "
            "msedge\u200bwebview2\u200b.\u200bdll\u200b.\n\n"
            "I\u200b've\u200b tried\u200b clearing\u200b\u200b the\u200b\u200b Teams\u200b\u200b"
            " cache\u200b\u200b folder\u200b (%\u200bAppData\u200b%\u200b\\\u200bMicrosoft"
            "\u200b\\\u200bTeams\u200b)\u200b and\u200b\u200b reinstalling\u200b\u200b but"
            "\u200b\u200b the\u200b\u200b same\u200b\u200b crash\u200b\u200b happens\u200b."
            "\u200b Outlook\u200b\u200b and\u200b\u200b other\u200b\u200b Office\u200b\u200b"
            " apps\u200b work\u200b\u200b fine\u200b.\n\n"
            "Running\u200b\u200b Windows\u200b 11\u200b 23H2\u200b on\u200b a\u200b Dell"
            "\u200b Latitude\u200b 5540\u200b.\n\n"
            "Thanks\u200b,\nSara\u200b\u200b Nguyen\u200b\nAccounting",
            "Teams\u200b\u200b\u200b desktop\u200b\u200b app\u200b\u200b won\u200b't\u200b "
            "open\u200b.\u200b\u200b It\u200b\u200b crashes\u200b\u200b right\u200b\u200b "
            "after\u200b\u200b the\u200b\u200b loading\u200b\u200b screen\u200b.\u200b\u200b "
            "I\u200b\u200b checked\u200b\u200b Task\u200b\u200b Manager\u200b\u200b and\u200b"
            "\u200b the\u200b\u200b process\u200b\u200b starts\u200b\u200b then\u200b\u200b "
            "disappears\u200b\u200b after\u200b\u200b about\u200b\u200b three\u200b\u200b "
            "seconds\u200b.\u200b\u200b The\u200b\u200b web\u200b\u200b version\u200b\u200b "
            "works\u200b\u200b fine\u200b\u200b in\u200b\u200b Edge\u200b\u200b so\u200b\u200b "
            "it\u200b's\u200b\u200b specific\u200b\u200b to\u200b\u200b the\u200b\u200b "
            "desktop\u200b\u200b client\u200b.\u200b\u200b The\u200b\u200b faulting\u200b\u200b "
            "module\u200b\u200b in\u200b\u200b the\u200b\u200b event\u200b\u200b log\u200b\u200b "
            "is\u200b\u200b msedgewebview2\u200b.\u200bdll\u200b.\u200b\u200b This\u200b\u200b "
            "started\u200b\u200b after\u200b\u200b yesterday\u200b's\u200b\u200b auto\u200b-"
            "update\u200b.",
        ],
        next_best_actions=[
            "Strip zero-width Unicode characters from the ticket text and focus on the Teams "
            "desktop crash. The faulting module is msedgewebview2.dll — likely a WebView2 runtime issue.",
            "Repair or reinstall the WebView2 runtime to fix the Teams desktop client crash.",
        ],
        remediation_steps=[
            [
                "Download and reinstall the Microsoft Edge WebView2 runtime from the official site",
                "Clear the Teams cache folder (%AppData%\\Microsoft\\Teams) and restart",
                "If the issue persists, uninstall Teams completely and install the latest version",
                "Check if a Windows Update or WebView2 update caused the regression",
                "Use the Teams web client as a workaround until the desktop app is fixed",
            ],
        ],
        tags=["data-cleanup", "zero-width-unicode", "invisible-characters"],
    ),
    # ──────────────────────────────────────────────────────────────────
    # 28. HTML email with CSS dark-mode styling artifacts
    # ──────────────────────────────────────────────────────────────────
    Scenario(
        scenario_id="cleanup-css-dark-mode-html",
        category="Software & Applications",
        priority="P3",
        assigned_team="Enterprise Applications",
        needs_escalation=False,
        missing_information=["application_version", "device_info"],
        subjects=[
            '<div style="background:#1e1e1e;color:#1e1e1e">OneDrive sync broken</div>',
            "OneDrive not syncing — sorry if this email looks weird (dark mode issue)",
        ],
        descriptions=[
            '<html><body style="background-color: #1a1a2e; color: #e0e0e0;">'
            '<div style="font-family: Segoe UI, sans-serif;">'
            '<style>@media (prefers-color-scheme: dark) { .content { background: #0d1117; '
            "color: #c9d1d9; } .highlight { color: #1e1e1e; background: #1e1e1e; } "
            ".footer { color: #161b22; } }</style>"
            '<div class="content">'
            '<p style="color: #c9d1d9;">Hi IT Team,</p>'
            '<p style="color: #58a6ff;">ISSUE:</p>'
            '<table style="border: 1px solid #30363d; background: #161b22;">'
            '<tr><td style="color: #8b949e; padding: 8px;">Application</td>'
            '<td style="color: #c9d1d9; padding: 8px;">OneDrive for Business</td></tr>'
            '<tr><td style="color: #8b949e;">Status</td>'
            '<td style="color: #f85149;">Not Syncing</td></tr>'
            '<tr><td style="color: #8b949e;">Error Code</td>'
            '<td style="color: #c9d1d9;">0x8004de40</td></tr>'
            "</table>"
            '<p class="highlight" style="color: #1e1e1e; background: #1e1e1e;">'
            "HIDDEN TEXT YOU CANNOT SEE IN DARK MODE: The actual error details are here but "
            "rendered invisible by matching foreground/background colors.</p>"
            '<p style="color: #c9d1d9;">OneDrive shows a red X on the tray icon and says '
            "&quot;There was a problem signing you in.&quot; I've been unable to sync files "
            "for two days. Error code is 0x8004de40.</p>"
            '<div class="footer" style="color: #161b22; font-size: 6pt;">Sent from Outlook '
            "Dark Mode — some content may be invisible in light mode viewers.</div>"
            "</div></div></body></html>",
            '<div style="background: #0d1117; color: #c9d1d9;">'
            '<style>.dark-only { color: #c9d1d9; } .light-only { color: #0d1117; } '
            "@media (prefers-color-scheme: light) { .dark-only { color: white; } "
            ".light-only { color: black; } }</style>"
            '<p class="dark-only">OneDrive for Business stopped syncing two days ago with '
            "error 0x8004de40. The sync icon shows a red circle with white X.</p>"
            '<p class="light-only">If you can read this, you are in light mode and the '
            "message above may be invisible. The issue is: OneDrive error 0x8004de40, sync "
            "stopped.</p>"
            "<p>I've tried unlinking and relinking the account, clearing the OneDrive cache, "
            "and resetting via %localappdata%\\Microsoft\\OneDrive\\onedrive.exe /reset. None "
            "of these fixed it. Running Windows 11 with Outlook 365 in dark mode.</p>"
            "</div>",
        ],
        next_best_actions=[
            "Strip the CSS and dark-mode styling artifacts and focus on the OneDrive sync error "
            "0x8004de40 — this is a TLS/authentication issue with the OneDrive service.",
            "Investigate OneDrive error 0x8004de40 — likely a TLS 1.2 requirement or proxy "
            "authentication issue.",
        ],
        remediation_steps=[
            [
                "Verify TLS 1.2 is enabled on the machine (error 0x8004de40 is often TLS-related)",
                "Check network proxy settings — OneDrive requires direct HTTPS access to Microsoft endpoints",
                "Reset OneDrive using onedrive.exe /reset and re-sign in",
                "Verify the user's Microsoft 365 license includes OneDrive for Business",
                "If proxy or firewall is blocking, add the required Microsoft 365 URLs to the allow list",
            ],
        ],
        tags=["data-cleanup", "css-artifacts", "dark-mode", "html-heavy"],
    ),
    # ──────────────────────────────────────────────────────────────────
    # 29. SSO failure with JWT token and OAuth error JSON pasted
    # ──────────────────────────────────────────────────────────────────
    Scenario(
        scenario_id="cleanup-jwt-oauth-dump",
        category="Access & Authentication",
        priority="P2",
        assigned_team="Identity & Access Management",
        needs_escalation=False,
        missing_information=["environment_details", "steps_to_reproduce"],
        subjects=[
            "SSO login failing — pasting the token and error response below",
            "Can't sign in via Okta SSO — here's the JWT and the error JSON",
        ],
        descriptions=[
            "Hi IAM team,\n\n"
            "I can't log in to the internal analytics portal via Okta SSO. I opened the "
            "browser dev tools and captured the token and the error response. Here's everything:\n\n"
            "Access Token (from Authorization header):\n"
            "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkZBS0VLRVlJRCJ9."
            "eyJzdWIiOiJqZG9lQGNvbnRvc28uY29tIiwiaXNzIjoiaHR0cHM6Ly9pZHAuY29udG9zby5jb20"
            "iLCJhdWQiOiJhbmFseXRpY3MtcG9ydGFsIiwiZXhwIjoxNzIxMDAwMDAwLCJpYXQiOjE3MjA5"
            "OTY0MDAsInNjb3BlIjoib3BlbmlkIHByb2ZpbGUgZW1haWwiLCJncm91cHMiOlsiYW5hbHl0aW"
            "NzLXVzZXJzIiwiZG9tYWluLXVzZXJzIl19."
            "FAKE_RSA_SIGNATURE_PLACEHOLDER_DO_NOT_ATTEMPT_TO_VERIFY\n\n"
            "OAuth Error Response:\n"
            '{"error":"invalid_grant","error_description":"The authorization code has expired '
            'or has been used. Code was issued at 2026-07-14T08:30:00Z and is now expired. '
            "Token endpoint received the request at 2026-07-14T09:45:00Z, which is beyond "
            'the 600-second validity window.","error_uri":"https://developer.okta.com/docs/'
            'reference/error-codes/","correlation_id":"abc123-def456-ghi789"}\n\n'
            "I think the token expired but I'm not sure why. I click 'Sign In', get "
            "redirected to Okta, enter my credentials, and then it bounces me back to the "
            "portal with an error page. This started today and I was able to log in fine "
            "yesterday.",
            "Okta SSO sign-in broken for the analytics dashboard. The browser console shows:\n\n"
            "POST https://idp.contoso.com/oauth2/v1/token 400 (Bad Request)\n\n"
            "Response body:\n"
            "{\n"
            '  "error": "invalid_grant",\n'
            '  "error_description": "Token exchange failed. The client_id '
            "analytics-portal-prod does not match the audience in the authorization code. "
            "Expected: analytics-portal-staging. Received: analytics-portal-prod. Verify the "
            'OAuth application configuration in the Okta admin console.",\n'
            '  "correlation_id": "xyz-987-654"\n'
            "}\n\n"
            "It looks like someone may have changed the Okta app configuration. The staging "
            "and production app IDs might have gotten swapped. I also noticed the redirect URI "
            "in the Okta app settings still points to the old domain (analytics-old.contoso.com) "
            "instead of the current one (analytics.contoso.com).",
        ],
        next_best_actions=[
            "Ignore the raw JWT and OAuth JSON payloads and focus on the SSO misconfiguration. "
            "The Okta app client_id or redirect URI is misconfigured between staging and production.",
            "Check the Okta admin console for the analytics portal app — the client_id and redirect "
            "URI may have been swapped during a recent config change.",
        ],
        remediation_steps=[
            [
                "Log in to the Okta admin console and review the analytics portal OAuth app configuration",
                "Verify the client_id matches the production application (analytics-portal-prod)",
                "Update the redirect URI from the old domain to https://analytics.contoso.com/callback",
                "Check if a recent change swapped the staging and production app settings",
                "Test SSO sign-in flow end-to-end after correcting the configuration",
            ],
        ],
        tags=["data-cleanup", "jwt-token", "oauth-error", "json-dump"],
    ),
    # ──────────────────────────────────────────────────────────────────
    # 30. Container deployment failure with docker-compose.yml pasted
    # ──────────────────────────────────────────────────────────────────
    Scenario(
        scenario_id="cleanup-docker-yaml-config",
        category="Software & Applications",
        priority="P2",
        assigned_team="DevOps Engineering",
        needs_escalation=False,
        missing_information=["environment_details", "error_message"],
        subjects=[
            "Container deployment failing — pasting full docker-compose.yml and logs",
            "Docker stack won't start — YAML config and error output below",
        ],
        descriptions=[
            "Hi DevOps,\n\n"
            "Our microservices stack won't start on the staging server. I'm pasting the full "
            "docker-compose.yml and the error output:\n\n"
            "```yaml\n"
            "version: '3.8'\n"
            "services:\n"
            "  api-gateway:\n"
            "    image: registry.contoso.com/api-gateway:2.4.1\n"
            "    ports:\n"
            "      - '8080:8080'\n"
            "    environment:\n"
            "      - DATABASE_URL=postgresql://svc_api:REDACTED@db-prod-03:5432/gateway_db\n"
            "      - REDIS_URL=redis://cache-01:6379/0\n"
            "      - JWT_SECRET=REDACTED_BUT_ORIGINALLY_PASTED_IN_CLEARTEXT\n"
            "    depends_on:\n"
            "      - postgres\n"
            "      - redis\n"
            "    deploy:\n"
            "      resources:\n"
            "        limits:\n"
            "          memory: 512M\n"
            "  postgres:\n"
            "    image: postgres:16\n"
            "    volumes:\n"
            "      - pgdata:/var/lib/postgresql/data\n"
            "    environment:\n"
            "      - POSTGRES_PASSWORD=REDACTED\n"
            "  redis:\n"
            "    image: redis:7-alpine\n"
            "    ports:\n"
            "      - '6379:6379'\n"
            "  worker:\n"
            "    image: registry.contoso.com/worker:2.4.1\n"
            "    environment:\n"
            "      - QUEUE_URL=amqp://rabbitmq:5672\n"
            "    depends_on:\n"
            "      - rabbitmq\n"
            "  rabbitmq:\n"
            "    image: rabbitmq:3-management\n"
            "    ports:\n"
            "      - '15672:15672'\n"
            "volumes:\n"
            "  pgdata:\n"
            "```\n\n"
            "Error output from `docker compose up`:\n"
            "```\n"
            "Error response from daemon: pull access denied for registry.contoso.com/"
            "api-gateway, repository does not exist or may require 'docker login'\n"
            "worker_1    | Error: connect ECONNREFUSED 172.18.0.5:5672\n"
            "api-gateway_1 | Error: FATAL: password authentication failed for user \"svc_api\"\n"
            "```\n\n"
            "The deployment was working last week. We recently rotated the database credentials "
            "and I think the new password wasn't updated in the compose file.",
            "Docker stack deployment failing on staging. Here is the compose file and logs:\n\n"
            "--- docker-compose.yml (truncated) ---\n"
            "services:\n"
            "  api-gateway:\n"
            "    image: registry.contoso.com/api-gateway:2.4.1\n"
            "    ports: ['8080:8080']\n"
            "    environment:\n"
            "      DATABASE_URL: postgresql://svc_api:OLD_PASSWORD@db-prod-03:5432/gateway_db\n"
            "  worker:\n"
            "    image: registry.contoso.com/worker:2.4.1\n"
            "    depends_on: [rabbitmq]\n"
            "  rabbitmq:\n"
            "    image: rabbitmq:3-management\n\n"
            "--- docker compose logs ---\n"
            "api-gateway_1  | FATAL: password authentication failed for user \"svc_api\"\n"
            "api-gateway_1  | Connection refused: db-prod-03:5432\n"
            "worker_1       | AMQP connection error: ECONNREFUSED\n\n"
            "This broke after last Friday's credential rotation. The DB password in the compose "
            "file is stale. Also, the staging server may not have access to the private Docker "
            "registry after the recent network changes.",
        ],
        next_best_actions=[
            "Look past the YAML config dump and focus on two root causes: stale database "
            "credentials after rotation, and Docker registry authentication failure.",
            "Update the database password in the deployment config and verify Docker registry "
            "access from the staging server.",
        ],
        remediation_steps=[
            [
                "Update the DATABASE_URL password in the compose file or secrets manager to match the rotated credential",
                "Run 'docker login registry.contoso.com' on the staging server to re-authenticate with the private registry",
                "Verify network connectivity from staging to db-prod-03:5432 and rabbitmq:5672",
                "Redeploy the stack with 'docker compose up -d' and monitor the logs for successful startup",
                "Move secrets out of the compose file into Docker secrets or a vault to prevent cleartext credential exposure",
            ],
        ],
        tags=["data-cleanup", "docker-compose", "yaml-config", "credential-rotation"],
    ),
]
