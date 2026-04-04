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
]
