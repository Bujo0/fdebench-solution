"""Data cleanup edge-case scenario definitions.

Covers: long email threads, base64 content, HTML-heavy emails, garbled encoding,
emoji-heavy messages, repeated content, massive signatures, mixed languages,
truncated messages, log dumps, HTML entities, duplicate sentences, MIME boundaries,
inline base64 PDFs, calendar metadata, buried issues, multilingual disclaimers,
NDR/bounce-backs, regex/code patterns, contradictory threads, and PII patterns.
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
        assigned_team="Endpoint Engineering",
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
            "Teams​​​​ app​​ crashes​​ on​ start​up",
            "Microsoft​​ Teams​​ won't​​ launch​​ after​ update",
        ],
        descriptions=[
            "Hi​​ IT​​ team​,\n\n"
            "Since​​ yesterday​'s​​ update​,​ Microsoft​"
            "​ Teams​ (​version​ 24​.​2​.​1​)"
            "​ crashes​​ immediately​​ on​ launch​.​ "
            "I​​ see​​ a​​ brief​​ splash​ screen"
            "​​ and​​ then​​ it​​ closes​.​ "
            "The​​ Windows​​ Event​​ Viewer​ shows​ "
            "Application​ Error​​ with​​ faulting​ module​ "
            "msedge​webview2​.​dll​.\n\n"
            "I​'ve​ tried​ clearing​​ the​​ Teams​​"
            " cache​​ folder​ (%​AppData​%​\\​Microsoft"
            "​\\​Teams​)​ and​​ reinstalling​​ but"
            "​​ the​​ same​​ crash​​ happens​."
            "​ Outlook​​ and​​ other​​ Office​​"
            " apps​ work​​ fine​.\n\n"
            "Running​​ Windows​ 11​ 23H2​ on​ a​ Dell"
            "​ Latitude​ 5540​.\n\n"
            "Thanks​,\nSara​​ Nguyen​\nAccounting",
            "Teams​​​ desktop​​ app​​ won​'t​ "
            "open​.​​ It​​ crashes​​ right​​ "
            "after​​ the​​ loading​​ screen​.​​ "
            "I​​ checked​​ Task​​ Manager​​ and​"
            "​ the​​ process​​ starts​​ then​​ "
            "disappears​​ after​​ about​​ three​​ "
            "seconds​.​​ The​​ web​​ version​​ "
            "works​​ fine​​ in​​ Edge​​ so​​ "
            "it​'s​​ specific​​ to​​ the​​ "
            "desktop​​ client​.​​ The​​ faulting​​ "
            "module​​ in​​ the​​ event​​ log​​ "
            "is​​ msedgewebview2​.​dll​.​​ This​​ "
            "started​​ after​​ yesterday​'s​​ auto​-"
            "update​.",
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
            "<style>@media (prefers-color-scheme: dark) { .content { background: #0d1117; "
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
            "<style>.dark-only { color: #c9d1d9; } .light-only { color: #0d1117; } "
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
            "Investigate OneDrive error 0x8004de40 — likely a TLS 1.2 requirement or proxy authentication issue.",
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
            "or has been used. Code was issued at 2026-07-14T08:30:00Z and is now expired. "
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
        assigned_team="Enterprise Applications",
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
            'api-gateway_1 | Error: FATAL: password authentication failed for user "svc_api"\n'
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
            'api-gateway_1  | FATAL: password authentication failed for user "svc_api"\n'
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
                "Update the DATABASE_URL password in the compose file or secrets manager"
                " to match the rotated credential",
                "Run 'docker login registry.contoso.com' on the staging server"
                " to re-authenticate with the private registry",
                "Verify network connectivity from staging to db-prod-03:5432 and rabbitmq:5672",
                "Redeploy the stack with 'docker compose up -d' and monitor the logs for successful startup",
                "Move secrets out of the compose file into Docker secrets or a vault"
                " to prevent cleartext credential exposure",
            ],
        ],
        tags=["data-cleanup", "docker-compose", "yaml-config", "credential-rotation"],
    ),
    # ──────────────────────────────────────────────────────────────────
    # 31. MIME multipart boundaries visible in email body
    # ──────────────────────────────────────────────────────────────────
    Scenario(
        scenario_id="cleanup-mime-boundary-markers",
        category="Software & Applications",
        priority="P3",
        assigned_team="Enterprise Applications",
        needs_escalation=False,
        missing_information=["error_message", "application_version"],
        subjects=[
            "Outlook displaying raw MIME boundary markers instead of formatted email",
            "Email from vendor shows ------=_Part_12345 lines throughout the message body",
        ],
        descriptions=[
            "Hi support,\n\n"
            "When I open emails from one of our vendors, I see raw MIME boundary strings "
            "scattered throughout the message instead of normal text and attachments. "
            "Here is what the email looks like:\n\n"
            "------=_Part_12345_67890.1720000000000\n"
            "Content-Type: text/plain; charset=UTF-8\n"
            "Content-Transfer-Encoding: quoted-printable\n\n"
            "Hi team, please find the Q3 budget report attached.\n\n"
            "------=_Part_12345_67890.1720000000000\n"
            'Content-Type: application/pdf; name="Q3_Budget.pdf"\n'
            'Content-Disposition: attachment; filename="Q3_Budget.pdf"\n'
            "Content-Transfer-Encoding: base64\n\n"
            "JVBERi0xLjQKMSAwIG9iago8PAovVHlwZSAvQ2F0YWxvZwo+PgplbmRvYmoKFAKE...\n\n"
            "------=_Part_12345_67890.1720000000000--\n\n"
            "This only happens with emails from this specific sender. Other emails display "
            "correctly. I am using Outlook 365 on Windows 11. The issue started after our "
            "email gateway was updated last week.",
            "Emails from external partner display with visible multipart MIME boundaries "
            "and raw Content-Type headers. The actual message text is interspersed with "
            "lines like:\n\n"
            "------=_NextPart_000_0042_01DA2B3C.F7A08E90\n"
            "Content-Type: multipart/alternative;\n"
            '\tboundary="----=_NextPart_001_0043_01DA2B3C.F7A08E90"\n\n'
            "The underlying request is simple: the vendor sent a follow-up about a "
            "contract renewal and attached a signed PDF. But the email renders as raw "
            "MIME source. I suspect the email gateway is stripping the Content-Type "
            "header or mangling the multipart structure during spam filtering. This "
            "affects about 20 users who correspond with this vendor.",
        ],
        next_best_actions=[
            "Strip the MIME boundary markers and headers to extract the actual message: "
            "a vendor follow-up about contract renewal with an attached PDF.",
            "Investigate the email gateway configuration change that is causing MIME "
            "parsing to fail for messages from this specific external domain.",
        ],
        remediation_steps=[
            [
                "Check the email gateway logs for MIME parsing errors on messages from the vendor's domain",
                "Review recent email gateway configuration or firmware updates that "
                "may have introduced MIME handling regressions",
                "Verify the vendor's mail server is sending properly formatted "
                "multipart MIME messages using a message header analyzer",
                "Add the vendor's domain to a bypass list if the gateway's content "
                "filter is corrupting the MIME structure",
                "Test with a clean Outlook profile to rule out local rendering issues",
            ],
        ],
        tags=["data-cleanup", "mime-boundaries"],
    ),
    # ──────────────────────────────────────────────────────────────────
    # 32. Base64-encoded PDF pasted instead of attached (pipeline issue)
    # ──────────────────────────────────────────────────────────────────
    Scenario(
        scenario_id="cleanup-base64-pdf-pipeline",
        category="Data & Storage",
        priority="P2",
        assigned_team="Data Platform",
        needs_escalation=False,
        missing_information=["error_message", "environment_details"],
        subjects=[
            "Data pipeline rejecting PDF — pasting the file contents directly for review",
            "Base64 of the failed PDF ingest document — need help with storage import",
        ],
        descriptions=[
            "Hi Data Platform team,\n\n"
            "Our automated document ingest pipeline is rejecting a PDF that a client "
            "uploaded. I can't attach the file to this ticket system, so I'm pasting "
            "the base64-encoded contents here so you can decode and inspect it:\n\n"
            "JVBERi0xLjcKCjEgMCBvYmoKPDwKL1R5cGUgL0NhdGFsb2cKL1BhZ2VzIDIgMCBSCi9NYXJr"
            "SW5mbyA8PAovTWFya2VkIHRydWUKPj4KPj4KZW5kb2JqCgoyIDAgb2JqCjw8Ci9UeXBlIC9Q"
            "YWdlcwovS2lkcyBbMyAwIFJdCi9Db3VudCAxCj4+CmVuZG9iagozIDAgb2JqCjw8Ci9UeXBl"
            "IC9QYWdlCi9QYXJlbnQgMiAwIFIKL01lZGlhQm94IFswIDAgNjEyIDc5Ml0KPj4KZW5kb2Jq"
            "FAKE_BASE64_DATA_CONTINUES_FOR_MANY_MORE_LINES_REPRESENTING_A_FULL_PDF_DOCUMENT_"
            "THAT_SHOULD_NOT_DISTRACT_FROM_THE_ACTUAL_SUPPORT_REQUEST_WHICH_IS_ABOUT_THE_"
            "PIPELINE_REJECTING_THE_UPLOAD\n\n"
            "The error from the pipeline is: 'UnsupportedMediaType: document header "
            "validation failed — expected PDF/A-1b conformance but received PDF 1.7'. "
            "Can you check if our ingest pipeline needs to be updated to accept standard "
            "PDF 1.7 format?",
            "Pasting the base64 of the PDF that is failing the data lake import:\n\n"
            "JVBERi0xLjcNCjEgMCBvYmoNCjw8DQovVHlwZSAvQ2F0YWxvZw0KL1BhZ2VzIDIgMCBSDQov"
            "T3V0bGluZXMgMyAwIFINCj4+DQplbmRvYmoNCg0KMiAwIG9iag0KPDwNCi9UeXBlIC9QYWdl"
            "ANOTHER_BLOCK_OF_FAKE_BASE64_REPRESENTING_A_MULTIPAGE_PDF_FINANCIAL_REPORT_WITH_"
            "EMBEDDED_FONTS_AND_IMAGES_TOTALLING_APPROXIMATELY_2MB_WHEN_DECODED\n\n"
            "The real issue: our Azure Blob Storage ingest function expects PDF/A-1b "
            "compliant documents, but the client's accounting software exports as "
            "standard PDF 1.7. We need to either add a conversion step to the pipeline "
            "or relax the validation rule. This is blocking the client's monthly "
            "financial report upload and they have a compliance deadline on Friday.",
        ],
        next_best_actions=[
            "Ignore the base64 payload. The core issue is a PDF version mismatch: the "
            "ingest pipeline requires PDF/A-1b but the client submits standard PDF 1.7.",
            "Evaluate whether to add a PDF/A conversion step in the pipeline or relax "
            "the validation to accept standard PDF 1.7 documents.",
        ],
        remediation_steps=[
            [
                "Confirm the pipeline's PDF/A-1b requirement and whether it is a hard "
                "compliance need or a default setting that can be relaxed",
                "If PDF/A is required, add a Ghostscript or similar conversion step to "
                "the ingest pipeline to convert PDF 1.7 to PDF/A-1b",
                "If PDF/A is not mandatory, update the validation rule to accept standard PDF 1.4 through 2.0",
                "Manually convert the blocked PDF for the client's Friday deadline while the pipeline fix is deployed",
                "Notify the client about supported document formats to prevent recurrence",
            ],
        ],
        tags=["data-cleanup", "base64-pdf"],
    ),
    # ──────────────────────────────────────────────────────────────────
    # 33. Multiple base64-encoded images interspersed with text
    # ──────────────────────────────────────────────────────────────────
    Scenario(
        scenario_id="cleanup-multiple-base64-images",
        category="Network & Connectivity",
        priority="P2",
        assigned_team="Network Operations",
        needs_escalation=False,
        missing_information=["network_location", "error_message"],
        subjects=[
            "VPN dropping every 5 minutes — screenshots of every disconnect inline",
            "Network keeps disconnecting — see all the embedded error screenshots below",
        ],
        descriptions=[
            "Hi NetOps,\n\n"
            "My VPN keeps disconnecting every 5 minutes or so. I've taken screenshots "
            "of each disconnect event. Here they all are:\n\n"
            "Screenshot 1 (first disconnect at 9:02 AM):\n"
            "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAA"
            "FAKE_IMAGE_1_BASE64_DATA_FIRST_DISCONNECT_SHOWING_VPN_CLIENT_ERROR\n\n"
            "Screenshot 2 (second disconnect at 9:07 AM):\n"
            "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAA"
            "FAKE_IMAGE_2_BASE64_DATA_SECOND_DISCONNECT_DIFFERENT_ERROR_CODE\n\n"
            "Screenshot 3 (third disconnect at 9:13 AM):\n"
            "data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEASABIAAD/4gHYSUNDX1BST0ZJTEU"
            "FAKE_IMAGE_3_BASE64_DATA_THIRD_DISCONNECT_SHOWING_NETWORK_ADAPTER_WARNING\n\n"
            "Screenshot 4 (after rebooting at 9:20 AM):\n"
            "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABAAAAAQCAYAAAAf8/9hAAAA"
            "FAKE_IMAGE_4_BASE64_DATA_POST_REBOOT_STILL_SHOWING_VPN_TIMEOUT\n\n"
            "As you can see, the VPN client shows 'Connection timed out — TLS handshake "
            "failed' each time. I'm on the corporate Wi-Fi in Building 7, 3rd floor. "
            "Other people on my floor seem to have the same issue.",
            "VPN disconnects happening repeatedly on the 3rd floor of Building 7. "
            "Embedding the error screenshots inline:\n\n"
            "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAA"
            "FAKE_SCREENSHOT_A_VPN_TLS_HANDSHAKE_FAILURE\n"
            "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAA"
            "FAKE_SCREENSHOT_B_NETWORK_ADAPTER_DISCONNECTED\n"
            "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAA"
            "FAKE_SCREENSHOT_C_DNS_RESOLUTION_TIMEOUT\n\n"
            "Stripping the images, the issue is: VPN via GlobalProtect drops every "
            "~5 minutes with TLS handshake failures. This affects multiple users on "
            "the 3rd floor of Building 7. The Wi-Fi signal strength is fine. We "
            "suspect the issue is with the network switch or firewall rule that was "
            "changed during last weekend's maintenance window.",
        ],
        next_best_actions=[
            "Discard the inline base64 screenshots and focus on the pattern: recurring VPN "
            "TLS handshake failures for multiple users on Building 7 floor 3.",
            "Check the network switch and firewall rules for Building 7 floor 3 that were "
            "modified during the last maintenance window.",
        ],
        remediation_steps=[
            [
                "Verify the network switch serving Building 7 floor 3 for port errors or recent configuration changes",
                "Check the firewall rules for changes made during the weekend maintenance "
                "window that may block TLS traffic on VPN ports",
                "Review the GlobalProtect gateway logs for TLS handshake failure details",
                "Test VPN connectivity from a wired connection on the same floor to "
                "isolate whether the issue is Wi-Fi or upstream",
                "Roll back the firewall rule change if confirmed as root cause",
            ],
        ],
        tags=["data-cleanup", "multiple-base64"],
    ),
    # ──────────────────────────────────────────────────────────────────
    # 34. ICS/vCalendar metadata mixed with support request
    # ──────────────────────────────────────────────────────────────────
    Scenario(
        scenario_id="cleanup-ics-calendar-metadata",
        category="Software & Applications",
        priority="P3",
        assigned_team="Enterprise Applications",
        needs_escalation=False,
        missing_information=["application_version", "steps_to_reproduce"],
        subjects=[
            "Calendar invite rendering as raw ICS text — meeting room booking broken",
            "Outlook calendar showing VCALENDAR source code instead of meeting details",
        ],
        descriptions=[
            "Hi team,\n\n"
            "When I try to open calendar invites from our room booking system, Outlook "
            "displays the raw ICS file content instead of the formatted meeting invite. "
            "Here is what I see:\n\n"
            "BEGIN:VCALENDAR\n"
            "VERSION:2.0\n"
            "PRODID:-//Contoso Room Booking//EN\n"
            "METHOD:REQUEST\n"
            "BEGIN:VEVENT\n"
            "DTSTART:20260720T140000Z\n"
            "DTEND:20260720T150000Z\n"
            "SUMMARY:Q3 Planning Review\n"
            "LOCATION:Building 4 - Room 401C (Capacity: 12)\n"
            "ORGANIZER;CN=Jane Doe:mailto:jane.doe@contoso.com\n"
            "ATTENDEE;ROLE=REQ-PARTICIPANT;CN=John Smith:mailto:john.smith@contoso.com\n"
            "ATTENDEE;ROLE=REQ-PARTICIPANT;CN=Support User:mailto:user@contoso.com\n"
            "DESCRIPTION:Quarterly planning review with budget discussion.\\n"
            "Please bring your department forecasts.\n"
            "UID:a1b2c3d4-e5f6-7890-abcd-ef1234567890@contoso.com\n"
            "STATUS:CONFIRMED\n"
            "SEQUENCE:0\n"
            "END:VEVENT\n"
            "END:VCALENDAR\n\n"
            "I can't accept or decline the invite because Outlook doesn't recognize it "
            "as a calendar event. This only happens with invites from the room booking "
            "system. Regular meeting invites from other people work fine.",
            "Calendar invites from the room booking application render as raw vCalendar "
            "source in Outlook. The email body shows BEGIN:VCALENDAR and all the ICS "
            "properties instead of a clickable meeting invitation. Sample:\n\n"
            "BEGIN:VCALENDAR\nVERSION:2.0\nBEGIN:VEVENT\n"
            "DTSTART:20260722T100000Z\nDTEND:20260722T110000Z\n"
            "SUMMARY:Sprint Retrospective\nLOCATION:Room 205B\n"
            "END:VEVENT\nEND:VCALENDAR\n\n"
            "The actual request buried under the ICS noise: the room booking system is "
            "sending calendar invites with the wrong Content-Type header (text/plain "
            "instead of text/calendar), so Outlook treats them as plain text. This "
            "started after the booking system was updated to version 4.2 last Thursday. "
            "About 50 users are affected and cannot book rooms through the system.",
        ],
        next_best_actions=[
            "Look past the raw ICS data to identify the root cause: the room booking "
            "system sends invites with Content-Type text/plain instead of text/calendar.",
            "Contact the room booking system administrator to fix the Content-Type "
            "header in outgoing calendar invitations after the v4.2 update.",
        ],
        remediation_steps=[
            [
                "Verify the room booking system version and confirm it was recently updated to v4.2",
                "Check the system's email sending configuration for the Content-Type header on calendar invitations",
                "Update the Content-Type from text/plain to text/calendar; method=REQUEST for outgoing ICS attachments",
                "Send a test invitation and confirm it renders correctly in Outlook",
                "Notify affected users that the issue has been resolved and ask them "
                "to re-send any pending room booking requests",
            ],
        ],
        tags=["data-cleanup", "calendar-metadata"],
    ),
    # ──────────────────────────────────────────────────────────────────
    # 35. Very long email with the real issue buried at the very end
    # ──────────────────────────────────────────────────────────────────
    Scenario(
        scenario_id="cleanup-buried-issue-very-long",
        category="Security & Compliance",
        priority="P1",
        assigned_team="Security Operations",
        needs_escalation=True,
        missing_information=["timestamp", "affected_system", "affected_users"],
        subjects=[
            "RE: RE: FW: Annual security policy review — URGENT credential leak at the end",
            "FW: Long policy discussion thread — CRITICAL: exposed API keys found in production",
        ],
        descriptions=[
            "---------- Forwarded message ----------\n"
            "From: Compliance Team\nDate: Mon, 14 Jul 2026\nSubject: Annual security review\n\n"
            "Hi all,\n\nAs part of our annual security policy review, I wanted to share "
            "the updated guidelines for FY2027. Please review the following sections:\n\n"
            "Section 1: Password Policy Updates\n"
            "- Minimum length increased from 12 to 16 characters\n"
            "- MFA required for all Tier-1 applications\n"
            "- Password rotation reduced to every 180 days\n\n"
            "Section 2: Data Classification\n"
            "- All customer PII must be tagged as Confidential\n"
            "- Internal documents default to Internal classification\n"
            "- Public-facing content must go through legal review\n\n"
            "Section 3: Endpoint Security\n"
            "- EDR agent mandatory on all corporate devices\n"
            "- USB storage disabled by default\n"
            "- Full disk encryption required\n\n"
            "Section 4: Network Security\n"
            "- Zero-trust model for all internal services\n"
            "- VPN mandatory for remote access\n"
            "- Network segmentation review quarterly\n\n"
            "Section 5: Incident Response\n"
            "- P1 incidents must be escalated within 15 minutes\n"
            "- Post-incident review mandatory within 48 hours\n"
            "- Tabletop exercises quarterly\n\n"
            "Please acknowledge receipt and send any comments by EOD Friday.\n\n"
            "Best regards,\nCompliance Team\n\n"
            "---\n\n"
            "P.S. — URGENT: While preparing this review, I discovered that our CI/CD "
            "pipeline's environment variables contain hardcoded AWS access keys "
            "(AKIA...) and a database connection string with plaintext credentials. "
            "These have been exposed in the build logs which are publicly accessible "
            "via our Jenkins dashboard. I think this has been the case for at least "
            "3 months. We need to rotate these credentials IMMEDIATELY and restrict "
            "access to the build logs. This is a P1 security incident.",
            "FW: Security policy annual review (long thread)\n\n"
            "The first 90% of this email is a routine policy review covering password "
            "requirements, data classification, endpoint hardening, network segmentation, "
            "and incident response procedures for FY2027. Standard annual compliance "
            "documentation that references 12 different policy subsections across 5 "
            "departments.\n\n"
            "[... extensive policy text omitted for brevity ...]\n\n"
            "CRITICAL ISSUE AT END OF THREAD:\n"
            "The sender discovered hardcoded AWS IAM access keys (AKIA prefix) and "
            "a plaintext PostgreSQL connection string (postgresql://admin:PLAINTEXT_PWD"
            "@prod-db-01:5432/core_app) in the CI/CD pipeline environment variables. "
            "Jenkins build logs containing these secrets are publicly accessible "
            "without authentication. Estimated exposure window is approximately 3 "
            "months. This requires immediate credential rotation, Jenkins access "
            "lockdown, and an investigation into whether the exposed credentials were "
            "used by unauthorized parties.",
        ],
        next_best_actions=[
            "Skip the routine policy review content and escalate the P1 finding at the "
            "end: exposed AWS keys and database credentials in public Jenkins build logs.",
            "Immediately initiate credential rotation for the exposed AWS IAM keys and "
            "database connection string, and restrict Jenkins build log access.",
        ],
        remediation_steps=[
            [
                "Immediately rotate the exposed AWS IAM access keys and generate new ones "
                "with least-privilege permissions",
                "Change the database password and update the connection string in the "
                "secrets manager (not in environment variables)",
                "Restrict Jenkins build log access to authenticated users only",
                "Audit CloudTrail and database access logs for unauthorized usage during the 3-month exposure window",
                "Migrate all secrets from CI/CD environment variables to a vault solution "
                "such as HashiCorp Vault or AWS Secrets Manager",
                "Conduct a broader review of all CI/CD pipelines for hardcoded secrets",
            ],
        ],
        tags=["data-cleanup", "buried-issue", "very-long-email"],
    ),
    # ──────────────────────────────────────────────────────────────────
    # 36. Legal disclaimers in 8+ languages appended to request
    # ──────────────────────────────────────────────────────────────────
    Scenario(
        scenario_id="cleanup-multilingual-disclaimers",
        category="Hardware & Peripherals",
        priority="P3",
        assigned_team="Endpoint Engineering",
        needs_escalation=False,
        missing_information=["device_info", "error_message"],
        subjects=[
            "Laptop keyboard not working — please see below (ignore the disclaimers)",
            "Keys on laptop stuck after spill — long disclaimer block attached by email system",
        ],
        descriptions=[
            "Hi,\n\n"
            "Several keys on my laptop keyboard stopped working after a small coffee spill "
            "this morning. The affected keys are: T, Y, G, H, B, N (basically the middle "
            "row). I've dried it off but they are still unresponsive. I need this fixed "
            "or replaced ASAP as I have client presentations this week.\n\n"
            "Asset tag: LAPTOP-4821\nModel: ThinkPad X1 Carbon Gen 11\n\n"
            "---\n\n"
            "CONFIDENTIALITY NOTICE (English): This email and any attachments are "
            "confidential and intended solely for the addressee. If you are not the "
            "intended recipient, please delete immediately.\n\n"
            "AVIS DE CONFIDENTIALITÉ (Français): Ce courriel et ses pièces jointes "
            "sont confidentiels et destinés uniquement au destinataire. Si vous n'êtes "
            "pas le destinataire prévu, veuillez le supprimer immédiatement.\n\n"
            "VERTRAULICHKEITSHINWEIS (Deutsch): Diese E-Mail und alle Anhänge sind "
            "vertraulich und nur für den Adressaten bestimmt. Wenn Sie nicht der "
            "beabsichtigte Empfänger sind, löschen Sie diese bitte sofort.\n\n"
            "AVISO DE CONFIDENCIALIDAD (Español): Este correo electrónico y sus "
            "archivos adjuntos son confidenciales. Si usted no es el destinatario "
            "previsto, por favor elimínelo inmediatamente.\n\n"
            "AVVISO DI RISERVATEZZA (Italiano): Questa email e i relativi allegati "
            "sono riservati e destinati esclusivamente al destinatario. Se non siete "
            "il destinatario previsto, cancellatela immediatamente.\n\n"
            "機密通知 (日本語): このメールおよび添付ファイルは機密であり、宛先の方のみを"
            "対象としています。宛先でない場合は、直ちに削除してください。\n\n"
            "기밀 통지 (한국어): 이 이메일과 첨부 파일은 기밀이며 수신자만을 위한 것입니다. "
            "의도된 수신자가 아닌 경우 즉시 삭제하십시오.\n\n"
            "保密声明 (中文): 本邮件及其附件为保密信息，仅供收件人使用。如果您不是预期"
            "收件人，请立即删除。",
            "Laptop keyboard partially non-functional after liquid spill.\n\n"
            "The middle row keys (T, Y, G, H, B, N) are completely unresponsive on my "
            "ThinkPad X1 Carbon Gen 11, asset LAPTOP-4821. Coffee spill this morning. "
            "Dried externally but keys remain dead. Need urgent replacement as I have "
            "client-facing meetings starting tomorrow.\n\n"
            "[Following this message is a corporate email disclaimer block repeated in "
            "English, French, German, Spanish, Italian, Japanese, Korean, and Chinese "
            "that constitutes approximately 80% of the email body. The disclaimer is "
            "auto-appended by the corporate email gateway and contains no relevant "
            "information about the hardware issue.]\n\n"
            "CONFIDENTIALITY / CONFIDENTIALITÉ / VERTRAULICHKEIT / CONFIDENCIALIDAD / "
            "RISERVATEZZA / 機密 / 기밀 / 保密\n"
            "This message is intended exclusively for the addressee...\n"
            "[...8 full paragraphs in 8 languages omitted for brevity...]",
        ],
        next_best_actions=[
            "Ignore the multilingual legal disclaimer block. The issue is a laptop "
            "keyboard failure after a coffee spill on a ThinkPad X1 Carbon Gen 11.",
            "Initiate a keyboard replacement for asset LAPTOP-4821 and provide a "
            "loaner device for the user's client presentations this week.",
        ],
        remediation_steps=[
            [
                "Provide a loaner laptop or external USB keyboard immediately for the user's client presentations",
                "Submit a hardware repair ticket for keyboard replacement on "
                "ThinkPad X1 Carbon Gen 11 (asset LAPTOP-4821)",
                "Advise the user to power off the laptop and not attempt further "
                "use until the keyboard is inspected for liquid damage",
                "Schedule a technician to inspect for internal liquid damage beyond the keyboard",
                "If under warranty, process the keyboard replacement through Lenovo; "
                "otherwise arrange third-party repair",
            ],
        ],
        tags=["data-cleanup", "multilingual-disclaimers"],
    ),
    # ──────────────────────────────────────────────────────────────────
    # 37. NDR/bounce-back message wrapping the original support request
    # ──────────────────────────────────────────────────────────────────
    Scenario(
        scenario_id="cleanup-ndr-bounce-message",
        category="Network & Connectivity",
        priority="P2",
        assigned_team="Network Operations",
        needs_escalation=False,
        missing_information=["network_location", "error_message", "affected_users"],
        subjects=[
            "Delivery Status Notification (Failure) — original request inside bounce-back",
            "Undeliverable: RE: Office network down — NDR wrapped around real ticket",
        ],
        descriptions=[
            "This is an automatically generated Delivery Status Notification.\n\n"
            "Delivery to the following recipients failed permanently:\n\n"
            "    helpdesk-old@contoso.com\n\n"
            "Technical details of permanent failure:\n"
            "550 5.1.1 The email account that you tried to reach does not exist. "
            "Please try double-checking the recipient's email address for typos or "
            "unnecessary spaces. Learn more at https://support.contoso.com/mail/errors "
            "gsmtp d9e45f-20260714\n\n"
            "----- Original message -----\n"
            "From: Mike Johnson <mike.johnson@contoso.com>\n"
            "To: helpdesk-old@contoso.com\n"
            "Date: Mon, 14 Jul 2026 08:15:00 -0500\n"
            "Subject: Office network down on 2nd floor\n\n"
            "Hi help desk,\n\n"
            "The entire 2nd floor network has been down since about 7:45 AM. We cannot "
            "access any internal resources, the Wi-Fi shows connected but no internet, "
            "and wired connections are also dead. About 30 people are affected and "
            "nobody can work. The network switch in the IDF closet on the 2nd floor "
            "has all amber lights instead of green. Please send someone urgently.\n\n"
            "Thanks,\nMike",
            "Bounce-back notification wrapping a support request:\n\n"
            "--- Delivery Status Notification ---\n"
            "Status: 550 5.1.1 User unknown\n"
            "Recipient: helpdesk-old@contoso.com\n"
            "Diagnostic-Code: smtp; 550 5.1.1 Mailbox not found\n"
            "Action: failed\n"
            "Final-Recipient: rfc822;helpdesk-old@contoso.com\n\n"
            "--- Enclosed Original Message ---\n"
            "The user (Mike Johnson) was trying to report that the entire 2nd floor "
            "network is down since 7:45 AM. Approximately 30 people affected. Both "
            "Wi-Fi and wired connections are non-functional. The IDF closet network "
            "switch shows amber LEDs. The original email was sent to a decommissioned "
            "help desk address (helpdesk-old@contoso.com) which no longer exists, so "
            "this NDR bounced back to the user. Mike then forwarded the NDR to us. "
            "The actual incident needs immediate attention — the NDR headers and "
            "delivery failure details are irrelevant to the network outage.",
        ],
        next_best_actions=[
            "Extract the original request from inside the NDR: 2nd floor network outage "
            "affecting 30 users since 7:45 AM with amber LEDs on the IDF switch.",
            "Dispatch network operations to the 2nd floor IDF closet immediately to "
            "diagnose the switch failure. Also update the old help desk address redirect.",
        ],
        remediation_steps=[
            [
                "Dispatch a network technician to the 2nd floor IDF closet to inspect the switch showing amber LEDs",
                "Check the switch for power issues, failed uplinks, or spanning-tree topology changes",
                "If the switch is faulty, replace it with a spare and restore connectivity",
                "Set up a mail redirect from helpdesk-old@contoso.com to the current "
                "help desk address to prevent future lost tickets",
                "Notify the 2nd floor users once connectivity is restored",
            ],
        ],
        tags=["data-cleanup", "ndr", "bounce-back"],
    ),
    # ──────────────────────────────────────────────────────────────────
    # 38. Regex and code patterns with special characters in ticket
    # ──────────────────────────────────────────────────────────────────
    Scenario(
        scenario_id="cleanup-regex-code-patterns",
        category="Software & Applications",
        priority="P3",
        assigned_team="Enterprise Applications",
        needs_escalation=False,
        missing_information=["application_version", "environment_details"],
        subjects=[
            "Data validation regex failing — pasting the full pattern and test cases",
            "App crashes when regex pattern is applied — code and error dump below",
        ],
        descriptions=[
            "Hi team,\n\n"
            "Our internal data validation app is crashing when we apply a regex pattern "
            "to sanitize input fields. I'm pasting the regex pattern and the code that "
            "uses it so you can see the issue:\n\n"
            "Pattern:\n"
            "^(?:(?:[a-zA-Z0-9!#$%&'*+/=?^_`{|}~-]+(?:\\.[a-zA-Z0-9!#$%&'*+/=?^_`"
            '{|}~-]+)*)|(?:"(?:[\\x01-\\x08\\x0b\\x0c\\x0e-\\x1f\\x21\\x23-\\x5b'
            '\\x5d-\\x7f]|\\\\[\\x01-\\x09\\x0b\\x0c\\x0e-\\x7f])*"))@(?:(?:[a-zA'
            "-Z0-9](?:[a-zA-Z0-9-]*[a-zA-Z0-9])?\\.)+[a-zA-Z]{2,}|\\[(?:(?:25[0-5]"
            "|2[0-4][0-9]|[01]?[0-9][0-9]?)\\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9]"
            "[0-9]?)\\])$\n\n"
            "Code snippet:\n"
            "```python\n"
            "import re\n"
            "pattern = re.compile(r'<the above pattern>', re.IGNORECASE | re.DOTALL)\n"
            "for record in dataset:  # ~500,000 records\n"
            "    if not pattern.match(record['email']):\n"
            "        invalid_records.append(record)\n"
            "```\n\n"
            "The app hangs for 30+ minutes on certain email inputs and then crashes "
            "with a RecursionError. I think the regex has catastrophic backtracking. "
            "We need to fix the pattern or use a different validation approach.",
            "Regex-heavy ticket: the data validation tool uses a complex RFC 5322 email "
            "regex that causes catastrophic backtracking on malformed input. The pattern "
            "contains nested quantifiers and alternations with overlapping character "
            "classes:\n\n"
            "^(?:[a-zA-Z0-9.!#$%&'*+/=?^_`{|}~-]+@[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}"
            "[a-zA-Z0-9])?(?:\\.[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?)*$)\n\n"
            "The code applies this pattern against 500K records in a loop with "
            "re.match(). When it encounters inputs like 'aaa@' + 'a' * 50 + '.com' "
            "variants, the engine enters exponential backtracking. The fix should "
            "either simplify the regex, use the 're2' library for linear-time matching, "
            "or replace regex validation with a dedicated email validation library. "
            "The application is Python 3.11 running on RHEL 9.",
        ],
        next_best_actions=[
            "Look past the complex regex syntax and code dump. The issue is catastrophic "
            "backtracking in an email validation regex applied to 500K records.",
            "Replace the complex RFC 5322 regex with a simpler pattern or use the 're2' "
            "library / a dedicated email validation library to avoid backtracking.",
        ],
        remediation_steps=[
            [
                "Replace the complex email regex with a simplified pattern that avoids "
                "nested quantifiers and overlapping alternations",
                "Consider using the 'email-validator' Python library or Google's 're2' "
                "library for linear-time regex matching",
                "Add a maximum input length check before applying the regex to prevent "
                "pathological inputs from reaching the engine",
                "Test the replacement pattern against the full 500K record dataset to "
                "confirm performance is acceptable",
                "Add monitoring and timeouts to the validation job so a single bad "
                "record cannot hang the entire process",
            ],
        ],
        tags=["data-cleanup", "regex", "code-patterns"],
    ),
    # ──────────────────────────────────────────────────────────────────
    # 39. Contradictory information across multiple replies in thread
    # ──────────────────────────────────────────────────────────────────
    Scenario(
        scenario_id="cleanup-contradictory-thread",
        category="Hardware & Peripherals",
        priority="P3",
        assigned_team="Endpoint Engineering",
        needs_escalation=False,
        missing_information=["device_info", "steps_to_reproduce", "error_message"],
        subjects=[
            "RE: RE: RE: Monitor issue — actually it might be the docking station",
            "FW: Display problems (updated: different symptoms now)",
        ],
        descriptions=[
            "--- Reply 1 (Monday 9:00 AM) ---\n"
            "My external monitor is completely black. It won't display anything when "
            "connected to my laptop. I've tried two different HDMI cables.\n\n"
            "--- Reply 2 (Monday 2:00 PM) ---\n"
            "Update: actually the monitor does turn on now, but the resolution is stuck "
            "at 1024x768 and I can't change it. The display settings don't show higher "
            "options. Ignore my first message, the monitor isn't black anymore.\n\n"
            "--- Reply 3 (Tuesday 10:00 AM) ---\n"
            "Another update: I switched to a USB-C connection through my docking station "
            "and now I'm getting display flickering every 10 seconds instead. The "
            "resolution is correct now (2560x1440) but the flickering is unusable. "
            "Also, I realized the docking station firmware was updated yesterday which "
            "might be related.\n\n"
            "--- Reply 4 (Tuesday 3:00 PM) ---\n"
            "Correction to my earlier messages: the HDMI cable I was using was actually "
            "DisplayPort, not HDMI. And the docking station is a Thunderbolt dock, not "
            "USB-C. Sorry for the confusion. The flickering is still happening. My "
            "laptop is a Dell Latitude 5540 and the dock is a Dell WD22TB4.",
            "Contradictory multi-reply hardware ticket:\n\n"
            "The user initially reported a black screen (Reply 1), then corrected to "
            "a resolution issue (Reply 2), then described flickering over a different "
            "connection (Reply 3), and finally corrected cable types and dock model "
            "(Reply 4). Piecing together the latest accurate state:\n\n"
            "- Device: Dell Latitude 5540\n"
            "- Dock: Dell WD22TB4 Thunderbolt dock (firmware updated recently)\n"
            "- Connection: Thunderbolt/DisplayPort to external 2560x1440 monitor\n"
            "- Current symptom: display flickering every ~10 seconds at correct "
            "resolution\n"
            "- Suspected cause: recent Thunderbolt dock firmware update\n\n"
            "All previous symptoms (black screen, low resolution) were either "
            "misdiagnosed or resolved by switching connection types. The only "
            "remaining issue is the post-firmware-update flickering.",
        ],
        next_best_actions=[
            "Discard the contradicted earlier symptoms and focus on the latest state: "
            "display flickering on Dell WD22TB4 dock after firmware update.",
            "Check if the WD22TB4 dock firmware update has known flickering issues and "
            "consider rolling back or applying a hotfix.",
        ],
        remediation_steps=[
            [
                "Check Dell support for known issues with the latest WD22TB4 Thunderbolt dock firmware update",
                "If a hotfix is available, apply it; otherwise roll back to the previous firmware version",
                "Update the Dell Latitude 5540's Thunderbolt controller driver and "
                "Intel graphics driver to the latest versions",
                "Test with a different Thunderbolt dock to isolate whether the issue "
                "is dock-specific or laptop-specific",
                "If the issue persists after firmware rollback, test with a direct "
                "DisplayPort connection bypassing the dock",
            ],
        ],
        tags=["data-cleanup", "contradictory"],
    ),
    # ──────────────────────────────────────────────────────────────────
    # 40. PII-like patterns accidentally included in ticket description
    # ──────────────────────────────────────────────────────────────────
    Scenario(
        scenario_id="cleanup-accidental-pii",
        category="Access & Authentication",
        priority="P2",
        assigned_team="Identity & Access Management",
        needs_escalation=False,
        missing_information=["affected_system", "authentication_method"],
        subjects=[
            "Can't reset my password — providing my details for verification",
            "Account locked out — including personal info so you can find me in the system",
        ],
        descriptions=[
            "Hi IAM team,\n\n"
            "I'm locked out of my account and can't reset my password through the "
            "self-service portal. Here are my details so you can look me up:\n\n"
            "Full name: Sarah J. Mitchell\n"
            "Employee ID: EMP-20190847\n"
            "Email: sarah.mitchell@contoso.com\n"
            "Phone: (555) 867-5309\n"
            "SSN: 078-05-1120\n"
            "Date of Birth: 03/15/1988\n"
            "Home address: 742 Evergreen Terrace, Springfield, IL 62704\n"
            "Manager: David Chen (david.chen@contoso.com)\n\n"
            "I know I shouldn't include all this info in an email but the self-service "
            "portal keeps giving me an error ('Account recovery unavailable — contact "
            "administrator') and I can't log into anything. I have a critical deadline "
            "today and need access restored immediately. My last successful login was "
            "Friday at 5:30 PM and when I tried this morning it said my account was "
            "locked due to too many failed attempts, but I haven't tried to log in "
            "since Friday.",
            "Password reset request containing PII that should be redacted from the "
            "ticket system:\n\n"
            "The user (Employee ID: EMP-20190847, sarah.mitchell@contoso.com) is locked "
            "out of their account. They included their SSN (078-XX-XXXX), date of birth, "
            "home address, and personal phone number in the ticket — all of which need "
            "to be scrubbed from this record after the request is processed.\n\n"
            "The actual access issue: the account shows locked due to multiple failed "
            "authentication attempts, but the user claims they haven't tried to log in "
            "since Friday at 5:30 PM. This suggests either a brute-force attack against "
            "the account, a misconfigured service account using stale credentials, or "
            "another device with a saved password that was changed. The self-service "
            "recovery portal is also returning an error, which may be a separate issue. "
            "After resolving the lockout, the PII in this ticket must be redacted per "
            "data handling policy.",
        ],
        next_best_actions=[
            "Unlock the user's account and investigate the source of the failed login "
            "attempts. IMPORTANT: redact the PII (SSN, DOB, address) from this ticket.",
            "After resolving the lockout, flag this ticket for PII scrubbing per "
            "data handling policy — the user included sensitive personal information.",
        ],
        remediation_steps=[
            [
                "Unlock the account for sarah.mitchell@contoso.com and force a password reset on next login",
                "Review the authentication logs to determine the source of failed login "
                "attempts (IP address, user agent, timestamps)",
                "Check for service accounts or devices using stale cached credentials for this user",
                "Investigate the self-service recovery portal error to ensure it is functioning correctly",
                "Redact the PII (SSN, date of birth, home address, personal phone) from "
                "this ticket record per the data handling policy",
                "Remind the user not to include sensitive personal information in support "
                "tickets and direct them to secure verification channels",
            ],
        ],
        tags=["data-cleanup", "pii-patterns"],
    ),
    # ──────────────────────────────────────────────────────────────────
    # 41. Raw XML/SOAP error payload dumped into ticket
    # ──────────────────────────────────────────────────────────────────
    Scenario(
        scenario_id="cleanup-xml-soap-payload",
        category="Software & Applications",
        priority="P2",
        assigned_team="Enterprise Applications",
        needs_escalation=False,
        missing_information=["error_message", "environment_details"],
        subjects=[
            "CRM web service returning 500 errors — SOAP fault below",
            "Internal API failing with XML error — full response pasted",
        ],
        descriptions=[
            "Hi team,\n\n"
            "Our CRM integration is failing since this morning. Here is the full SOAP "
            "response I'm getting:\n\n"
            '<?xml version="1.0" encoding="utf-8"?>\n'
            "<soap:Envelope "
            'xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" '
            'xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" '
            'xmlns:xsd="http://www.w3.org/2001/XMLSchema">\n'
            "  <soap:Body>\n"
            "    <soap:Fault>\n"
            "      <faultcode>soap:Server</faultcode>\n"
            "      <faultstring>System.NullReferenceException: Object reference not set "
            "to an instance of an object.\n"
            "   at Contoso.CRM.Services.CustomerLookup.GetByAccountId(String accountId) "
            "in D:\\Build\\src\\Services\\CustomerLookup.cs:line 247\n"
            "   at Contoso.CRM.API.Controllers.CustomerController.Search(SearchRequest req) "
            "in D:\\Build\\src\\API\\Controllers\\CustomerController.cs:line 89\n"
            "   at System.Web.Services.Protocols.SoapHttpClientProtocol.ReadResponse("
            "SoapClientMessage message, WebResponse response, Stream responseStream, "
            "Boolean asyncCall)\n"
            "   at System.Web.Services.Protocols.SoapHttpClientProtocol.Invoke("
            "String methodName, Object[] parameters)</faultstring>\n"
            "      <detail>\n"
            "        <ErrorDetails>\n"
            "          <ErrorCode>CRM-SVC-5001</ErrorCode>\n"
            "          <Timestamp>2026-03-18T08:45:12.347Z</Timestamp>\n"
            "          <CorrelationId>a1b2c3d4-e5f6-7890-abcd-ef1234567890</CorrelationId>\n"
            "          <ServerNode>CRM-PROD-WEB-03</ServerNode>\n"
            "          <RequestUri>/api/v2/customers/search</RequestUri>\n"
            "        </ErrorDetails>\n"
            "      </detail>\n"
            "    </soap:Fault>\n"
            "  </soap:Body>\n"
            "</soap:Envelope>\n\n"
            "This started after the deployment last night (build 2026.3.17.1). "
            "The customer search endpoint is returning 500 for all requests. "
            "About 200 users in the sales team are affected and can't look up "
            "customer records. We need this fixed urgently — it's blocking order processing.",
            "Full XML error from the CRM API:\n\n"
            '<?xml version="1.0"?>\n'
            "<Error>\n"
            "  <Code>InternalServerError</Code>\n"
            "  <Message>An unhandled exception occurred during the execution of the "
            "current web request.</Message>\n"
            "  <StackTrace>\n"
            "    at Contoso.Services.CustomerService.FindCustomer(Guid tenantId, "
            "String query) in /src/Services/CustomerService.cs:line 156\n"
            "    at Contoso.API.Middleware.ExceptionHandler.HandleAsync(HttpContext ctx) "
            "in /src/Middleware/ExceptionHandler.cs:line 42\n"
            "  </StackTrace>\n"
            "  <InnerException>\n"
            "    <Code>SqlException</Code>\n"
            "    <Message>Timeout expired. The timeout period elapsed prior to completion "
            "of the operation.</Message>\n"
            "  </InnerException>\n"
            "</Error>\n\n"
            "The real issue: CRM customer search API is down since the 3/17 deployment. "
            "Looks like a database timeout or connection pool exhaustion. Sales team "
            "is dead in the water — about 200 users affected.",
        ],
        next_best_actions=[
            "Ignore the XML/SOAP payload noise. Core issue is a CRM API failure "
            "(NullReferenceException or SQL timeout) after the 2026.3.17 deployment "
            "affecting customer search for ~200 sales users.",
            "Investigate the database timeout in the CRM customer search API. Roll "
            "back the 3/17 deployment if a quick fix is not available.",
        ],
        remediation_steps=[
            [
                "Check the CRM application logs on CRM-PROD-WEB-03 for the root cause of the NullReferenceException",
                "Verify database connectivity and connection pool health on the CRM SQL server",
                "If the issue correlates with the 2026.3.17 deployment, initiate a rollback",
                "Monitor the /api/v2/customers/search endpoint after the fix is applied",
                "Communicate resolution status to the sales team",
            ],
        ],
        tags=["data-cleanup", "xml-payload"],
    ),
    # ──────────────────────────────────────────────────────────────────
    # 42. Screenshot OCR artifacts with garbled text
    # ──────────────────────────────────────────────────────────────────
    Scenario(
        scenario_id="cleanup-screenshot-ocr-artifacts",
        category="Hardware & Peripherals",
        priority="P3",
        assigned_team="Endpoint Engineering",
        needs_escalation=False,
        missing_information=["device_info", "error_message"],
        subjects=[
            "M0nitor fIickering — transcrib3d from screenshot",
            "DspIay iss0e on my Iaptop — OCR from ph0to",
        ],
        descriptions=[
            "Th1s t1cket was cr3ated fron an 0CR scan of a screenshot:\n\n"
            "Err0r Mess@ge on Scr33n:\n"
            '"Disp1ay driv3r stopp3d resp0nding and h@s rec0vered"\n'
            "Driv3r: NVID1A GeF0rce RTX 3070 v537.42\n"
            "0S: Wind0ws 11 Pr0 22H2\n"
            "Ev3nt V1ewer Err0r C0de: LiveKerne1Event 1d 141\n\n"
            "The m0nitor g0es b1ack f0r about 2 sec0nds then c0mes back. Th1s happ3ns "
            "every 15-20 m1nutes. It start3d after the lat3st NVID1A dr1ver upd@te. "
            "Pr3vious driv3r vers1on was 536.99 and w0rked f1ne. The 1ssue 0ccurs "
            "0n b0th the ext3rnal m0nitor (De11 U2723QE) and the 1aptop scr33n.",
            "Transcripti0n fr0m photo 0f err0r scr33n:\n\n"
            "Wlndows has detected that your dlsplay adapter perfornance\n"
            "has becone slow. Wlndows wlll automatlcally reduce your\n"
            "dlsplay settlngs to lmprove perfornance.\n\n"
            "Dlsplay: NVID|A GeForce RTX 3O70\n"
            "Drlver Verslon: 537.42\n"
            "Resolutlon was changed fron 3840x216O to 192Ox1O8O\n\n"
            "The actuaI issue: My Iaptop's externaI monitor keeps fIickering and "
            "going bIack. It started after upgrading the NVIDIA driver from 536.99 "
            "to 537.42. The dispIay driver keeps crashing and recovering. I need "
            "heIp roIIing back the driver or finding a fix.",
        ],
        next_best_actions=[
            "Look past the OCR artifacts. The real issue is an NVIDIA display driver "
            "crash (LiveKernelEvent 141) after upgrading from 536.99 to 537.42.",
            "Roll back the NVIDIA driver from 537.42 to the previous stable version "
            "(536.99) and verify the monitor flickering stops.",
        ],
        remediation_steps=[
            [
                "Roll back the NVIDIA GeForce driver from 537.42 to the previous stable version 536.99",
                "If rollback resolves the issue, block driver 537.42 from auto-updating via WSUS/Intune policy",
                "Check for known issues with NVIDIA driver 537.42 and the Dell U2723QE monitor",
                "If rollback does not resolve, run NVIDIA clean install using DDU (Display Driver Uninstaller)",
                "Monitor for Event ID 141 (LiveKernelEvent) recurrence after the driver change",
            ],
        ],
        tags=["data-cleanup", "ocr-artifacts"],
    ),
    # ──────────────────────────────────────────────────────────────────
    # 43. Automated monitoring alert flood
    # ──────────────────────────────────────────────────────────────────
    Scenario(
        scenario_id="cleanup-monitoring-alert-flood",
        category="Network & Connectivity",
        priority="P1",
        assigned_team="Network Operations",
        needs_escalation=True,
        missing_information=["network_location", "affected_users"],
        subjects=[
            "[CRITICAL] Multiple alerts — core switch down — Floor 3",
            "ALERT FLOOD: Network infrastructure failure detected",
        ],
        descriptions=[
            "[Nagios] CRITICAL - Host: core-sw-fl3-01.contoso.local is DOWN\n"
            "Date/Time: 2026-03-18 07:32:14 UTC\n"
            "Duration: 0d 0h 2m 15s\n"
            "Notification Type: PROBLEM\n"
            "Host Output: PING CRITICAL - Packet loss = 100%\n"
            "---\n"
            "[Nagios] CRITICAL - Service: SNMP on core-sw-fl3-01.contoso.local is CRITICAL\n"
            "Date/Time: 2026-03-18 07:32:44 UTC\n"
            "Duration: 0d 0h 1m 45s\n"
            "Service Output: Connection refused\n"
            "---\n"
            "[Nagios] WARNING - Service: Uplink-Port-Gi0/1 on core-sw-fl3-01.contoso.local\n"
            "Date/Time: 2026-03-18 07:33:01 UTC\n"
            "Service Output: Interface down - no carrier\n"
            "---\n"
            "[Nagios] CRITICAL - Host: ap-fl3-01.contoso.local is DOWN (parent: core-sw-fl3-01)\n"
            "Date/Time: 2026-03-18 07:33:15 UTC\n"
            "Host Output: PING CRITICAL - 100% packet loss\n"
            "---\n"
            "[Nagios] CRITICAL - Host: ap-fl3-02.contoso.local is DOWN (parent: core-sw-fl3-01)\n"
            "Date/Time: 2026-03-18 07:33:16 UTC\n"
            "---\n"
            "[Nagios] CRITICAL - Host: ap-fl3-03.contoso.local is DOWN (parent: core-sw-fl3-01)\n"
            "Date/Time: 2026-03-18 07:33:17 UTC\n"
            "---\n"
            "[Nagios] WARNING - Host: printer-fl3-01.contoso.local is UNREACHABLE\n"
            "Date/Time: 2026-03-18 07:33:30 UTC\n"
            "---\n"
            "[Nagios] CRITICAL - Service: DHCP-Scope-Floor3 on dhcp-01.contoso.local\n"
            "Date/Time: 2026-03-18 07:34:00 UTC\n"
            "Service Output: No response from relay agent 10.3.0.1\n"
            "---\n\n"
            "All these alerts started at once. The core switch on Floor 3 "
            "(core-sw-fl3-01, Cisco Catalyst 9300) appears to have gone down, "
            "taking all downstream access points and network services with it. "
            "Entire Floor 3 (~75 users) has no network connectivity.",
            "[Datadog Monitor] ALERT: Network device core-sw-fl3-01 unreachable\n"
            "Triggered: 2026-03-18T07:32:00Z | Status: Alert | Priority: P1\n"
            "Tags: env:prod, floor:3, device_type:switch, vendor:cisco\n"
            "Metric: network.device.reachable = 0 for last 2m on core-sw-fl3-01\n"
            "---\n"
            "[Datadog Monitor] ALERT: High packet loss on floor3-uplink\n"
            "Triggered: 2026-03-18T07:32:30Z | Status: Alert\n"
            "Metric: network.interface.packet_loss > 95% on port Gi0/1\n"
            "---\n"
            "[Datadog Monitor] ALERT: WiFi AP fleet down — floor 3\n"
            "Triggered: 2026-03-18T07:33:00Z | Status: Alert\n"
            "Metric: Count of reachable APs on floor:3 = 0 (expected: 12)\n"
            "---\n"
            "[Datadog Monitor] WARN: DHCP lease renewals failing — floor 3 scope\n"
            "Triggered: 2026-03-18T07:34:00Z | Status: Warn\n"
            "---\n\n"
            "Root cause: the core switch on Floor 3 is down. All subsequent alerts "
            "are downstream effects. About 75 employees on Floor 3 have no wired "
            "or wireless connectivity.",
        ],
        next_best_actions=[
            "Consolidate the alert flood — all alerts stem from a single root cause: "
            "core-sw-fl3-01 (Cisco Catalyst 9300 on Floor 3) is down. Dispatch "
            "network operations to investigate the physical switch.",
            "Identify root cause as the Floor 3 core switch failure. Suppress "
            "downstream alerts and focus on restoring core-sw-fl3-01.",
        ],
        remediation_steps=[
            [
                "Dispatch on-site network engineer to Floor 3 IDF to physically inspect core-sw-fl3-01",
                "Check for power supply failure, blown fuse, or loose power cable on the switch",
                "If hardware failure, fail over to the redundant switch or deploy a spare",
                "Once the core switch is restored, verify all downstream APs and services recover",
                "Suppress the cascading Nagios/Datadog alerts and send a consolidated all-clear to Floor 3 users",
            ],
        ],
        tags=["data-cleanup", "alert-flood"],
    ),
    # ──────────────────────────────────────────────────────────────────
    # 44. URL-encoded content from web form
    # ──────────────────────────────────────────────────────────────────
    Scenario(
        scenario_id="cleanup-url-encoded-content",
        category="Software & Applications",
        priority="P3",
        assigned_team="Enterprise Applications",
        needs_escalation=False,
        missing_information=["steps_to_reproduce", "application_version"],
        subjects=[
            "Form submission error — raw data below",
            "Web portal form not submitting — URL encoded error",
        ],
        descriptions=[
            "The internal expense report form is failing when I click submit. "
            "Instead of processing, it shows this raw data in the browser:\n\n"
            "expense_category%3DTravel%26amount%3D1250.00%26currency%3DUSD%26"
            "description%3DFlight%2520to%2520Seattle%2520for%2520Q1%2520planning"
            "%2520meeting%26receipt_attached%3Dtrue%26date%3D2026-03-15%26"
            "cost_center%3DCC-4420%26approver%3Djohn.smith%2540contoso.com%26"
            "project_code%3DPRJ-2026-0142%26notes%3DBooked%2520via%2520Concur"
            "%252C%2520confirmation%2520%2523ABC123%26policy_compliant%3Dtrue%26"
            "tax_amount%3D0.00%26vendor%3DDelta%2520Airlines%26gl_code%3D6200"
            "%26payment_method%3Dcorporate_card_ending_4421\n\n"
            "This has been happening since the last update to the expense portal. "
            "I'm using Chrome 123 on Windows 11. The form worked fine last week. "
            "Other people in my department are reporting the same problem — the "
            "form data appears URL-encoded on screen instead of being submitted "
            "to the backend.",
            "When I try to submit a purchase request on the procurement portal, "
            "the form fails and dumps this in the page:\n\n"
            "item%3DLaptop%2520Lenovo%2520T14s%26qty%3D5%26unit_price%3D1899.00"
            "%26total%3D9495.00%26requestor%3Djane.doe%2540contoso.com%26"
            "department%3DEngineering%26justification%3DNew%2520hire%2520equipment"
            "%2520for%2520Q2%2520onboarding%26budget_approved%3Dtrue%26"
            "delivery_address%3D100%2520Main%2520St%252C%2520Bldg%2520A%252C"
            "%2520Floor%25203%26vendor_id%3DVND-00891%26contract_ref%3DMSA-2025-0044\n\n"
            "The actual issue: the internal procurement web portal is broken. Form "
            "submissions are not being sent to the server — instead the URL-encoded "
            "POST body is being displayed in the browser. Likely a JavaScript error "
            "or a misconfigured form action URL after the latest deployment.",
        ],
        next_best_actions=[
            "Ignore the URL-encoded data. The issue is a broken form submission in the "
            "expense/procurement web portal — POST data is displayed instead of submitted.",
            "Investigate the web portal deployment that broke form submissions. "
            "Check the form action URL and JavaScript for errors.",
        ],
        remediation_steps=[
            [
                "Check the latest deployment to the expense/procurement portal for changes to form handling",
                "Inspect the browser developer console for JavaScript errors on the form submit action",
                "Verify the form action URL is correctly configured to point to the backend API",
                "Roll back the latest portal deployment if a quick fix is not available",
                "Test the form submission in multiple browsers to confirm the fix",
            ],
        ],
        tags=["data-cleanup", "url-encoded"],
    ),
    # ──────────────────────────────────────────────────────────────────
    # 45. Massive CC recipient list in email
    # ──────────────────────────────────────────────────────────────────
    Scenario(
        scenario_id="cleanup-massive-cc-recipient-list",
        category="Access & Authentication",
        priority="P2",
        assigned_team="Identity & Access Management",
        needs_escalation=False,
        missing_information=["affected_users", "authentication_method"],
        subjects=[
            "Password expiration — entire marketing department affected",
            "Dept-wide password reset needed — everyone CCed",
        ],
        descriptions=[
            "CC: alice.wong@contoso.com; bob.martinez@contoso.com; "
            "carol.johnson@contoso.com; david.lee@contoso.com; "
            "emma.wilson@contoso.com; frank.garcia@contoso.com; "
            "grace.chen@contoso.com; henry.taylor@contoso.com; "
            "iris.anderson@contoso.com; jack.thomas@contoso.com; "
            "karen.moore@contoso.com; larry.jackson@contoso.com; "
            "maria.white@contoso.com; nathan.harris@contoso.com; "
            "olivia.martin@contoso.com; peter.thompson@contoso.com; "
            "quinn.garcia@contoso.com; rachel.robinson@contoso.com; "
            "steve.clark@contoso.com; tina.rodriguez@contoso.com; "
            "ursula.lewis@contoso.com; victor.walker@contoso.com; "
            "wendy.hall@contoso.com; xavier.allen@contoso.com; "
            "yolanda.young@contoso.com; zachary.king@contoso.com; "
            "amy.wright@contoso.com; brian.lopez@contoso.com; "
            "cathy.hill@contoso.com; derek.scott@contoso.com; "
            "elena.green@contoso.com; george.adams@contoso.com; "
            "holly.baker@contoso.com; ivan.gonzalez@contoso.com; "
            "jenny.nelson@contoso.com; kevin.carter@contoso.com; "
            "laura.mitchell@contoso.com; mike.perez@contoso.com; "
            "nancy.roberts@contoso.com; oscar.turner@contoso.com; "
            "paula.phillips@contoso.com; roger.campbell@contoso.com; "
            "susan.parker@contoso.com; tom.evans@contoso.com; "
            "uma.edwards@contoso.com; vince.collins@contoso.com\n\n"
            "Hi IT team,\n\n"
            "I'm writing on behalf of the entire Marketing department (46 people "
            "CCed above). Everyone received a password expiration notice yesterday "
            "saying our passwords expire in 3 days, but when we try to change them "
            "through the self-service portal, we get an error: 'Password change "
            "unavailable for your account type.' We are all on the MKTG-Users AD group. "
            "Can you either extend the expiration deadline or fix the self-service portal "
            "so we can reset our passwords? This is urgent — if 46 people get locked "
            "out on Friday it will be a disaster.",
            "To: helpdesk@contoso.com\n"
            "CC: [46 Marketing department employees]\n"
            "marketing-all@contoso.com; mktg-managers@contoso.com; "
            "mktg-analysts@contoso.com; mktg-creative@contoso.com; "
            "mktg-ops@contoso.com; mktg-events@contoso.com; "
            "cmo-direct@contoso.com\n\n"
            "All 46 members of the Marketing department received password expiration "
            "warnings but the self-service password change portal returns an error. "
            "The AD group MKTG-Users may have a misconfigured password policy or the "
            "self-service reset tool is not recognizing this group. Please investigate "
            "before Friday when all passwords expire simultaneously.",
        ],
        next_best_actions=[
            "Ignore the long CC list. The issue is that 46 Marketing department users "
            "cannot change their expiring passwords via the self-service portal due to "
            "an error with the MKTG-Users AD group.",
            "Investigate the password policy applied to the MKTG-Users AD group and "
            "fix the self-service portal error, or extend the password expiration deadline.",
        ],
        remediation_steps=[
            [
                "Check the password policy linked to the MKTG-Users AD group for misconfigurations",
                "Verify the self-service password reset portal recognizes the MKTG-Users group",
                "If the portal issue cannot be resolved quickly, extend the password expiration by 7 days",
                "Test the self-service password change flow with a test account in the MKTG-Users group",
                "Send a communication to the Marketing department with resolution status and instructions",
            ],
        ],
        tags=["data-cleanup", "cc-list"],
    ),
    # ──────────────────────────────────────────────────────────────────
    # 46. RTF formatting artifacts in ticket text
    # ──────────────────────────────────────────────────────────────────
    Scenario(
        scenario_id="cleanup-rtf-formatting-artifacts",
        category="Software & Applications",
        priority="P3",
        assigned_team="Enterprise Applications",
        needs_escalation=False,
        missing_information=["application_version", "steps_to_reproduce"],
        subjects=[
            "Word template corrupted — raw formatting data in document",
            "Document template producing garbled output with control codes",
        ],
        descriptions=[
            "{\\rtf1\\ansi\\ansicpg1252\\deff0\\nouicompat\\deflang1033"
            "{\\fonttbl{\\f0\\fswiss\\fprq2\\fcharset0 Calibri;}"
            "{\\f1\\froman\\fprq2\\fcharset0 Times New Roman;}}\n"
            "{\\colortbl ;\\red0\\green0\\blue0;\\red31\\green73\\blue125;}\n"
            "\\viewkind4\\uc1\\pard\\cf1\\f0\\fs22 "
            "Dear IT Team,\\par\\par\n"
            "The quarterly report template (Q1-2026-Template.dotx) is producing "
            "garbled output with these RTF control codes visible in the final document. "
            "\\par\\par\n"
            "\\b Issue Description:\\b0\\par\n"
            "When I open the template in Word, the formatting is completely broken. "
            "Headers show raw \\{\\\\b Bold Text\\\\b0\\} instead of actual bold. "
            "Tables have raw \\\\trowd and \\\\cellx commands visible. "
            "\\par\\par\n"
            "The template was last updated by the document management team on March 10. "
            "It worked fine before that update. I've tried opening it in Word 2021 and "
            "Word 365 — same result in both. About 30 people in Finance use this template "
            "for their quarterly reports due next week.\\par\n"
            "}",
            "Subject: Word template broken\n\n"
            "\\rtf1\\ansi\\deff0{\\fonttbl{\\f0 Calibri;}}\n"
            "\\pard Our shared Word template for client proposals is corrupted. "
            "When you open it, you see raw RTF control codes mixed with the content. "
            "\\par The template path is: \\\\contoso-fs01\\shared\\templates\\"
            "ClientProposal-2026.dotx \\par\n"
            "It was working fine until someone edited it with an older version of Word "
            "or a third-party editor that mangled the XML/RTF structure. \\par\n"
            "The Legal team needs this template fixed by Thursday for a major client "
            "pitch. About 15 people are blocked.\\par\n",
        ],
        next_best_actions=[
            "Ignore the RTF control codes. The issue is a corrupted Word template "
            "(Q1-2026-Template.dotx) that displays raw formatting instead of "
            "rendered content, affecting ~30 Finance users.",
            "Restore the Word template from a backup prior to the March 10 edit "
            "and investigate what caused the corruption.",
        ],
        remediation_steps=[
            [
                "Restore the Word template from the most recent backup before the March 10 edit",
                "Verify the restored template opens correctly in both Word 2021 and Word 365",
                "Check file version history on SharePoint/network share to identify the corrupting edit",
                "If no backup exists, recreate the template from the last known good printed copy",
                "Lock the template permissions to prevent unauthorized edits going forward",
            ],
        ],
        tags=["data-cleanup", "rtf-artifacts"],
    ),
    # ──────────────────────────────────────────────────────────────────
    # 47. Raw CSV data dump pasted into ticket
    # ──────────────────────────────────────────────────────────────────
    Scenario(
        scenario_id="cleanup-csv-data-dump",
        category="Data & Storage",
        priority="P3",
        assigned_team="Data Platform",
        needs_escalation=False,
        missing_information=["affected_system", "timestamp"],
        subjects=[
            "Suspicious login data from database export — please investigate",
            "Anomalous data in access logs — raw CSV attached in body",
        ],
        descriptions=[
            "Hi Data Platform,\n\n"
            "I exported the login audit table and found some anomalies. Pasting "
            "the CSV here since I can't attach files:\n\n"
            "timestamp,user_id,source_ip,location,status,user_agent\n"
            "2026-03-17T02:14:00Z,admin@contoso.com,203.0.113.45,Unknown,success,curl/7.68.0\n"
            "2026-03-17T02:14:02Z,admin@contoso.com,203.0.113.45,Unknown,success,curl/7.68.0\n"
            "2026-03-17T02:15:00Z,svc-backup@contoso.com,203.0.113.45,Unknown,success,python-requests/2.28\n"
            "2026-03-17T02:15:30Z,admin@contoso.com,203.0.113.45,Unknown,success,curl/7.68.0\n"
            "2026-03-17T02:16:00Z,admin@contoso.com,10.1.0.50,Building A,success,Mozilla/5.0\n"
            "2026-03-17T02:16:01Z,admin@contoso.com,203.0.113.45,Unknown,success,curl/7.68.0\n"
            "2026-03-17T02:17:00Z,svc-sql@contoso.com,203.0.113.45,Unknown,success,sqlcmd/15.0\n"
            "2026-03-17T02:18:00Z,admin@contoso.com,203.0.113.45,Unknown,success,curl/7.68.0\n"
            "2026-03-17T02:19:00Z,sa@contoso.com,203.0.113.45,Unknown,failed,python-requests/2.28\n"
            "2026-03-17T02:19:05Z,sa@contoso.com,203.0.113.45,Unknown,failed,python-requests/2.28\n"
            "2026-03-17T02:19:10Z,sa@contoso.com,203.0.113.45,Unknown,success,python-requests/2.28\n"
            "2026-03-17T02:20:00Z,dba@contoso.com,203.0.113.45,Unknown,success,curl/7.68.0\n"
            "2026-03-17T03:00:00Z,admin@contoso.com,10.1.0.50,Building A,success,Mozilla/5.0\n"
            "2026-03-17T08:30:00Z,admin@contoso.com,10.1.0.50,Building A,success,Mozilla/5.0\n\n"
            "The concern: IP 203.0.113.45 is not from our network and was used to access "
            "multiple high-privilege accounts (admin, svc-backup, svc-sql, sa, dba) at 2 AM "
            "using command-line tools (curl, python-requests, sqlcmd). The admin account "
            "also had a legitimate login from 10.1.0.50 at the same time — which means "
            "either the account is compromised or someone is using stolen credentials. "
            "Please investigate urgently.",
            "Raw CSV from our SIEM export showing suspicious activity:\n\n"
            "date,event_type,user,src_ip,dst_host,action\n"
            "2026-03-17,LOGIN,admin,203.0.113.45,dc-01,success\n"
            "2026-03-17,FILE_ACCESS,admin,203.0.113.45,file-svr-01,read\n"
            "2026-03-17,FILE_COPY,admin,203.0.113.45,file-svr-01,copy\n"
            "2026-03-17,DB_QUERY,svc-sql,203.0.113.45,sql-prod-01,select *\n"
            "2026-03-17,EXPORT,svc-sql,203.0.113.45,sql-prod-01,bulk_export\n"
            "2026-03-17,LOGIN,admin,10.1.0.50,dc-01,success\n\n"
            "This looks like potential unauthorized access and data exfiltration. "
            "An external IP accessed multiple privileged accounts overnight and "
            "performed file copies and database exports. Needs immediate investigation.",
        ],
        next_best_actions=[
            "Ignore the CSV formatting. This appears to be a security incident: "
            "external IP 203.0.113.45 accessed privileged accounts overnight with "
            "CLI tools. Escalate to Security Operations immediately.",
            "Investigate the suspicious logins from 203.0.113.45 as a potential "
            "account compromise and data exfiltration event.",
        ],
        remediation_steps=[
            [
                "Escalate to Security Operations for immediate investigation of the external IP access",
                "Disable or rotate credentials for all accounts accessed from 203.0.113.45",
                "Run a geolocation lookup on IP 203.0.113.45 and check threat intelligence feeds",
                "Review file server and database audit logs for data exfiltration scope",
                "Check if the admin account has MFA enabled and verify for credential stuffing or token theft",
            ],
        ],
        tags=["data-cleanup", "csv-dump"],
    ),
    # ──────────────────────────────────────────────────────────────────
    # 48. Calendar invite iCal metadata in ticket
    # ──────────────────────────────────────────────────────────────────
    Scenario(
        scenario_id="cleanup-ical-calendar-metadata",
        category="Software & Applications",
        priority="P3",
        assigned_team="Enterprise Applications",
        needs_escalation=False,
        missing_information=["affected_users", "application_version"],
        subjects=[
            "Calendar invites not being delivered — iCal data included",
            "Recurring meeting invite failing — raw calendar data below",
        ],
        descriptions=[
            "Hi,\n\n"
            "I'm trying to send a recurring meeting invite to the leadership team "
            "but some attendees aren't receiving it. Here's the calendar data I "
            "exported from Outlook to help debug:\n\n"
            "BEGIN:VCALENDAR\n"
            "VERSION:2.0\n"
            "PRODID:-//Microsoft Corporation//Outlook 16.0//EN\n"
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
            "DTSTART;TZID=Eastern Standard Time:20260325T090000\n"
            "DTEND;TZID=Eastern Standard Time:20260325T100000\n"
            "RRULE:FREQ=WEEKLY;BYDAY=WE;COUNT=12\n"
            "SUMMARY:Q2 Leadership Sync\n"
            "LOCATION:Executive Boardroom / Teams Meeting\n"
            "ORGANIZER:mailto:vp.operations@contoso.com\n"
            "ATTENDEE;ROLE=REQ-PARTICIPANT:mailto:cfo@contoso.com\n"
            "ATTENDEE;ROLE=REQ-PARTICIPANT:mailto:cto@contoso.com\n"
            "ATTENDEE;ROLE=REQ-PARTICIPANT:mailto:coo@contoso.com\n"
            "ATTENDEE;ROLE=OPT-PARTICIPANT:mailto:ea.support@contoso.com\n"
            "STATUS:CONFIRMED\n"
            "SEQUENCE:3\n"
            "UID:040000008200E00074C5B7101A82E00800000000F0A2C3D4E5F67890\n"
            "END:VEVENT\n"
            "END:VCALENDAR\n\n"
            "The CFO and COO say they never received the invite. The CTO got it fine. "
            "I've resent it twice with no luck. This is a weekly recurring meeting "
            "starting March 25. I'm the organizer (VP Operations). This has worked "
            "fine for years — something changed recently.",
            "Calendar invite not being delivered to 3 of 6 attendees. iCal export:\n\n"
            "BEGIN:VCALENDAR\nVERSION:2.0\nPRODID:-//Outlook//EN\nMETHOD:REQUEST\n"
            "BEGIN:VEVENT\nDTSTART:20260325T130000Z\nDTEND:20260325T140000Z\n"
            "RRULE:FREQ=WEEKLY;BYDAY=WE\nSUMMARY:Q2 Planning\n"
            "ORGANIZER:mailto:vp.operations@contoso.com\n"
            "ATTENDEE:mailto:cfo@contoso.com\nATTENDEE:mailto:cto@contoso.com\n"
            "ATTENDEE:mailto:coo@contoso.com\nSEQUENCE:3\n"
            "UID:040000008200E00074C5B7101A82E008\nEND:VEVENT\nEND:VCALENDAR\n\n"
            "The real issue is that some external-facing mailboxes (CFO, COO) are not "
            "receiving calendar invites from internal organizers. This may be a mail flow "
            "rule or Exchange Online transport rule blocking iCal attachments for "
            "certain mailbox types. It started after the email security policy update "
            "last week.",
        ],
        next_best_actions=[
            "Ignore the iCal metadata. The issue is that calendar invites are not being "
            "delivered to certain executive mailboxes — likely a transport rule or "
            "mail flow policy blocking iCal attachments.",
            "Check Exchange Online transport rules for any recently modified rules that "
            "may block or quarantine iCal/calendar invite attachments.",
        ],
        remediation_steps=[
            [
                "Review Exchange Online transport rules for any rules that filter iCal or .ics attachments",
                "Check the mail flow trace for the undelivered invites to the CFO and COO mailboxes",
                "Verify if the email security policy update last week added content filtering "
                "that affects calendar invites",
                "Test sending a calendar invite to the affected mailboxes from a different organizer",
                "If a transport rule is blocking, create an exception for internal-to-internal calendar invites",
            ],
        ],
        tags=["data-cleanup", "ical-metadata"],
    ),
    # ──────────────────────────────────────────────────────────────────
    # 49. Terminal output with ANSI escape codes
    # ──────────────────────────────────────────────────────────────────
    Scenario(
        scenario_id="cleanup-ansi-terminal-escape-codes",
        category="Software & Applications",
        priority="P2",
        assigned_team="Enterprise Applications",
        needs_escalation=False,
        missing_information=["environment_details", "error_message"],
        subjects=[
            "Deployment script failed — terminal output with color codes",
            "CI/CD pipeline error — raw terminal log below",
        ],
        descriptions=[
            "Our deployment script failed. Here's the terminal output I copied:\n\n"
            "\033[36m[2026-03-18 09:00:01]\033[0m Starting deployment pipeline v3.2.1\n"
            "\033[36m[2026-03-18 09:00:02]\033[0m \033[32m✔\033[0m Checking prerequisites...\n"
            "\033[36m[2026-03-18 09:00:03]\033[0m \033[32m✔\033[0m Docker image built: contoso/api:2026.3.18\n"
            "\033[36m[2026-03-18 09:00:10]\033[0m \033[32m✔\033[0m Health check: staging... passed\n"
            "\033[36m[2026-03-18 09:00:15]\033[0m \033[33m⚠\033[0m Warning: 2 pods pending in production\n"
            "\033[36m[2026-03-18 09:00:20]\033[0m Deploying to production cluster...\n"
            "\033[36m[2026-03-18 09:00:45]\033[0m \033[31m✘ ERROR\033[0m: Deployment failed!\n"
            "\033[31mError: ImagePullBackOff — failed to pull image contoso/api:2026.3.18\n"
            "from registry.contoso.io: unauthorized: authentication required\033[0m\n"
            "\033[36m[2026-03-18 09:00:46]\033[0m \033[31m✘\033[0m Rolling back to previous version...\n"
            "\033[36m[2026-03-18 09:01:00]\033[0m \033[32m✔\033[0m Rollback complete: contoso/api:2026.3.15\n"
            "\033[36m[2026-03-18 09:01:01]\033[0m \033[31mPipeline FAILED\033[0m — exit code 1\n\n"
            "The deployment failed because the production Kubernetes cluster couldn't "
            "pull the Docker image. The error is 'unauthorized: authentication required' "
            "which suggests the registry credentials have expired or were rotated. "
            "The rollback succeeded so production is still on the old version.",
            "CD pipeline output (pasted from terminal):\n\n"
            "\x1b[1;34m==>\x1b[0m \x1b[1mRunning deploy.sh --env production\x1b[0m\n"
            "\x1b[32m[OK]\x1b[0m Pre-flight checks passed\n"
            "\x1b[32m[OK]\x1b[0m Database migrations applied (3 new)\n"
            "\x1b[31m[FAIL]\x1b[0m Container registry authentication failed\n"
            "\x1b[31m[FAIL]\x1b[0m kubectl set image deployment/api-server "
            "api=registry.contoso.io/contoso/api:2026.3.18 \x1b[31mFAILED\x1b[0m\n"
            "\x1b[33m[WARN]\x1b[0m Initiating automatic rollback...\n"
            "\x1b[32m[OK]\x1b[0m Rollback successful\n\n"
            "The production deployment failed due to expired container registry "
            "credentials. The Kubernetes service account can no longer authenticate "
            "to registry.contoso.io. Need the registry credentials renewed.",
        ],
        next_best_actions=[
            "Ignore the ANSI escape codes. The deployment failed because Kubernetes "
            "can't authenticate to the container registry (ImagePullBackOff / "
            "unauthorized). Renew the registry credentials.",
            "Renew the container registry credentials for the production Kubernetes "
            "cluster and re-run the deployment pipeline.",
        ],
        remediation_steps=[
            [
                "Renew or rotate the container registry credentials (registry.contoso.io)",
                "Update the Kubernetes image pull secret with the new credentials",
                "Verify the service account has the correct RBAC permissions on the registry",
                "Re-run the deployment pipeline after credentials are updated",
                "Set up monitoring/alerting for credential expiration to prevent recurrence",
            ],
        ],
        tags=["data-cleanup", "ansi-codes"],
    ),
    # ──────────────────────────────────────────────────────────────────
    # 50. PGP/S-MIME encrypted email wrapper
    # ──────────────────────────────────────────────────────────────────
    Scenario(
        scenario_id="cleanup-pgp-encrypted-wrapper",
        category="Security & Compliance",
        priority="P2",
        assigned_team="Security Operations",
        needs_escalation=False,
        missing_information=["configuration_details", "affected_system"],
        subjects=[
            "Email encryption broken — PGP blocks visible in messages",
            "S/MIME encryption failing — recipients see raw encrypted data",
        ],
        descriptions=[
            "Hi Security team,\n\n"
            "Our email encryption has been malfunctioning since the weekend. "
            "When I send encrypted emails, recipients see this instead of the "
            "actual message:\n\n"
            "-----BEGIN PGP MESSAGE-----\n"
            "Version: GnuPG v2.2.41 (GNU/Linux)\n\n"
            "hQEMA8p3hFg0y8XJAQ/+LkZ2M7YB5h9nVJXqGx09VLiW4ZXnBtFzK5jN8sMpQxR\n"
            "7wP9k3YfOlA2jm5J0J5X4FQaP2LMWV8rC3KsNNJXkzhFG4dEuVqH/MqGRLflJxo\n"
            "FKr2tN5VpSDml+V2nMC0Y7c1B3qFQFkXt3RLcE4PA1q/hHVdT+nZJlMGPKWBnCqt\n"
            "xP8d1LfVTJG2nN0jWRi5fMbk3kpXq7dJy0M4rkzaQlBLsVoE8kZ1fJ5YtNxqm6W\n"
            "FAKE_PGP_ENCRYPTED_BLOCK_DATA_CONTINUES_FOR_MANY_LINES_AND_SHOULD_NOT\n"
            "CONFUSE_THE_CLASSIFIER_INTO_THINKING_THIS_IS_SOMETHING_OTHER_THAN_AN\n"
            "EMAIL_ENCRYPTION_CONFIGURATION_ISSUE_AT_THE_ORGANIZATION_LEVEL\n"
            "=dK7f\n"
            "-----END PGP MESSAGE-----\n\n"
            "The actual message is supposed to be a routine update about our Q1 "
            "compliance audit. Instead, external recipients see the raw PGP block. "
            "Internal recipients on Outlook can decrypt fine, but anyone outside "
            "our domain (auditors, legal counsel, regulators) sees the raw data. "
            "This started after the email gateway update on Saturday. About 20 "
            "people in the compliance team send encrypted emails daily to external "
            "parties and all of them are affected.",
            "Encrypted email test showing the issue:\n\n"
            "Content-Type: application/pkcs7-mime; smime-type=enveloped-data;\n"
            " name=smime.p7m\n"
            "Content-Transfer-Encoding: base64\n"
            "Content-Disposition: attachment; filename=smime.p7m\n\n"
            "MIIBxwYJKoZIhvcNAQcDoIIBuDCCAbQCAQAxggF0MIIBcAIBADBYMFIxCzAJBgNV\n"
            "BAYTAlVTMRMwEQYDVQQIEwpXYXNoaW5ndG9uMRAwDgYDVQQHEwdSZWRtb25kMRww\n"
            "FAKE_SMIME_ENCRYPTED_DATA_BLOCK_THAT_REPRESENTS_THE_ENCRYPTED_PAYLOAD\n"
            "OF_AN_EMAIL_MESSAGE_USING_PKCS7_ENVELOPE_FORMAT\n\n"
            "External recipients are seeing this S/MIME block instead of the decrypted "
            "message. Our email gateway's S/MIME certificate may have expired or the "
            "gateway-level decryption/re-encryption for external parties stopped working "
            "after the Saturday update. The compliance team needs this fixed ASAP — "
            "they have regulatory communications that must be encrypted but readable.",
        ],
        next_best_actions=[
            "Ignore the PGP/S-MIME encrypted blocks. The issue is that the email "
            "gateway is not properly handling encryption for external recipients "
            "after the Saturday update — external parties see raw encrypted data.",
            "Investigate the email gateway update from Saturday that broke "
            "encryption handling for external recipients. Check certificate "
            "expiration and gateway re-encryption configuration.",
        ],
        remediation_steps=[
            [
                "Check the email gateway's S/MIME and PGP certificates for expiration or misconfiguration",
                "Review the email gateway update from Saturday for changes to encryption processing",
                "Verify the gateway's ability to decrypt and re-encrypt emails for external delivery",
                "If the gateway certificate expired, renew it and restart the encryption service",
                "Test sending encrypted emails to external recipients to confirm the fix",
                "Notify the compliance team once external encryption delivery is restored",
            ],
        ],
        tags=["data-cleanup", "pgp-encrypted"],
    ),
    # ──────────────────────────────────────────────────────────────────
    # 22. Email thread where topic switches mid-conversation
    # ──────────────────────────────────────────────────────────────────
    Scenario(
        scenario_id="cleanup-thread-hijack",
        category="Network & Connectivity",
        priority="P3",
        assigned_team="Network Operations",
        needs_escalation=False,
        missing_information=["error_message", "network_location"],
        subjects=[
            "RE: RE: FW: Printer on 4th floor not working — also VPN question",
            "RE: RE: RE: Copier jam issue → now about VPN dropping constantly",
        ],
        descriptions=[
            "-----Original Message-----\n"
            "From: Lisa Park\nSent: Monday 8:15 AM\nTo: Help Desk\n\n"
            "Hi, the printer on the 4th floor (HP LaserJet 4250 near the break room) is "
            "showing a paper jam error but there's no paper stuck. I've opened all the trays "
            "and checked the fuser area. Can someone come take a look?\n\n"
            "> From: Help Desk\n> Sent: Monday 9:02 AM\n>\n"
            "> Hi Lisa, we've logged ticket INC-40821 for the printer jam. A technician "
            "> will be on-site by noon.\n\n"
            "Thanks for the printer update. Actually, while I have you — the real reason "
            "I'm writing is my VPN has been dropping every 10-15 minutes since last Thursday. "
            "I'm on the Contoso Financial Services trading floor and need a stable connection "
            "to the risk analytics platform. Every time it drops I lose my session and have to "
            "re-authenticate through Okta. I'm using the GlobalProtect client version 5.2.13 "
            "on Windows 11. My manager says this is impacting our end-of-quarter reporting "
            "deadlines. Can this be prioritized?",
            "RE: RE: RE: FW: Copier issue — 3rd floor\n\n"
            "--- thread history ---\n"
            "> Original issue: The MFP copier on 3rd floor is showing error code E-302.\n"
            "> Tech response: Parts ordered, ETA 3 business days.\n"
            "> User reply: OK thanks.\n\n"
            "Hey, unrelated but replying here because it's easier — my VPN connection to "
            "the Contoso Financial Services data center has been completely unreliable for "
            "the past week. I get connected fine but after about 10 minutes the tunnel drops "
            "and I have to reconnect. I've tried both the office Wi-Fi and a hardwired "
            "Ethernet connection with the same result. The GlobalProtect client shows "
            "'Gateway timed out' before disconnecting. I'm in building B, 2nd floor. "
            "This is blocking my access to the internal risk dashboards and I have "
            "compliance reports due Friday. Please help.",
        ],
        next_best_actions=[
            "Ignore the printer/copier thread history — the actual issue is recurring VPN "
            "disconnections on the GlobalProtect client. Investigate gateway timeout and "
            "tunnel stability for the user's network segment.",
            "Focus on the VPN dropping issue buried after the topic switch. Check "
            "GlobalProtect gateway logs, split-tunnel configuration, and MTU settings "
            "for the user's building/floor network segment.",
        ],
        remediation_steps=[
            [
                "Identify the user's GlobalProtect gateway and check its health and connection logs",
                "Review firewall session timeout and keep-alive settings for the VPN tunnel",
                "Check for MTU or fragmentation issues on the user's network segment",
                "Update the GlobalProtect client to the latest stable version",
                "If the issue persists, capture a packet trace during the next disconnection event",
            ],
        ],
        tags=["data-cleanup", "thread-hijack"],
    ),
    # ──────────────────────────────────────────────────────────────────
    # 23. Hebrew/Arabic text mixed with English causing RTL/LTR confusion
    # ──────────────────────────────────────────────────────────────────
    Scenario(
        scenario_id="cleanup-rtl-ltr-mixed",
        category="Software & Applications",
        priority="P3",
        assigned_team="Enterprise Applications",
        needs_escalation=False,
        missing_information=["error_message", "affected_users"],
        subjects=[
            "SharePoint permissions error — בעיה בגישה לתיקיה — cannot access site",
            "مشكلة في الوصول — SharePoint access denied for finance team",
        ],
        descriptions=[
            "שלום, I need help with a SharePoint issue at Contoso Financial Services.\n\n"
            "אני לא מצליח לגשת "
            "לאתר (I cannot access the site) — "
            "every time I click on the Finance Reports library "
            "I get שגיאה 403 "
            "(403 error). האתר הוא "
            "https://contoso.sharepoint.com/sites/FinanceReports "
            "and it was working fine "
            "עד יום שלישי (until Tuesday).\n\n"
            "המנהל שלי אמר (my manager said) "
            "that our team was supposed to keep access "
            "after the site migration. "
            "אני בצוות Finance Operations "
            "and I need the Q4 reports "
            "בדחיפות (urgently). "
            "אנא תעזרו לי (please help me). "
            "There are 12 people "
            "on my team and "
            "כולם נתקלו "
            "באותה בעיה (all of them "
            "have the same issue).",
            "مرحبا, this is regarding the SharePoint "
            "site for Contoso Financial Services "
            "regulatory compliance documents.\n\n"
            "أنا لا أستطيع "
            "الوصول (I cannot access) the site at "
            "https://contoso.sharepoint.com/sites/RegulatoryDocs. "
            "الخطأ يقول "
            "(the error says) 'Access Denied — you do not have "
            "permission to access this "
            "resource.' "
            "كان يعمل بشكل "
            "طبيعي (it was working normally) "
            "before the weekend. "
            "فريقي (my team) in the compliance department "
            "also lost access. "
            "نحتاج هذا بشكل "
            "عاجل (we need this urgently) "
            "for the quarterly audit "
            "الذي يبدأ يوم "
            "الاثنين (which starts Monday). "
            "شكرا (thank you).",
        ],
        next_best_actions=[
            "Look past the mixed Hebrew/Arabic and English text — the core issue is a "
            "SharePoint 403 permissions error after a site migration. The finance/compliance "
            "team lost access to document libraries.",
            "Investigate SharePoint site permissions for the Finance Reports and Regulatory "
            "Docs sites. Check if the recent migration reset group memberships or broke "
            "permission inheritance.",
        ],
        remediation_steps=[
            [
                "Check SharePoint site collection permissions for the affected sites",
                "Verify that the finance/compliance security groups were preserved during migration",
                "Re-add the affected teams to the appropriate SharePoint permission levels",
                "Test access with one affected user to confirm the fix",
                "Notify all affected team members once access is restored",
            ],
        ],
        tags=["data-cleanup", "rtl-ltr-mixed"],
    ),
    # ──────────────────────────────────────────────────────────────────
    # 24. User pasted a massive HTML table with the issue buried in one cell
    # ──────────────────────────────────────────────────────────────────
    Scenario(
        scenario_id="cleanup-html-table-paste",
        category="Data & Storage",
        priority="P2",
        assigned_team="Data Platform",
        needs_escalation=False,
        missing_information=["error_message", "environment_details"],
        subjects=[
            "Database connection failure — see data extract below",
            "DB error when running quarterly report — pasted full dataset",
        ],
        descriptions=[
            "Hi team, I keep getting database errors when running the Contoso Financial Services "
            "quarterly reconciliation report. Here is the dataset I was trying to load:\n\n"
            "<table border='1'>\n"
            "<tr><th>Row</th><th>Account</th><th>Region</th><th>Amount</th><th>Status</th><th>Notes</th></tr>\n"
            "<tr><td>1</td><td>ACT-10001</td><td>US-East</td><td>$12,450.00</td><td>Cleared</td><td></td></tr>\n"
            "<tr><td>2</td><td>ACT-10002</td><td>US-West</td><td>$8,320.50</td><td>Cleared</td><td></td></tr>\n"
            "<tr><td>3</td><td>ACT-10003</td><td>EMEA</td><td>$45,100.00</td><td>Pending</td><td></td></tr>\n"
            "<tr><td>4</td><td>ACT-10004</td><td>APAC</td><td>$3,200.00</td><td>Cleared</td><td></td></tr>\n"
            "<tr><td>5</td><td>ACT-10005</td><td>US-East</td><td>$67,890.25</td><td>Cleared</td><td></td></tr>\n"
            "<tr><td>6</td><td>ACT-10006</td><td>EMEA</td><td>$15,430.00</td><td>Cleared</td><td></td></tr>\n"
            "<tr><td>7</td><td>ACT-10007</td><td>US-West</td><td>$22,100.00</td><td>Cleared</td><td></td></tr>\n"
            "<tr><td>8</td><td>ACT-10008</td><td>APAC</td><td>$9,870.00</td><td>Cleared</td><td></td></tr>\n"
            "<tr><td>9</td><td>ACT-10009</td><td>US-East</td><td>$31,250.75</td><td>Cleared</td><td></td></tr>\n"
            "<tr><td>10</td><td>ACT-10010</td><td>EMEA</td><td>$5,600.00</td><td>Cleared</td><td></td></tr>\n"
            "<tr><td>11</td><td>ACT-10011</td><td>US-East</td><td>$18,900.00</td><td>Cleared</td><td></td></tr>\n"
            "<tr><td>12</td><td>ACT-10012</td><td>APAC</td><td>$41,300.00</td><td>Pending</td><td></td></tr>\n"
            "<tr><td>13</td><td>ACT-10013</td><td>US-West</td><td>$7,650.00</td><td>Cleared</td><td></td></tr>\n"
            "<tr><td>14</td><td>ACT-10014</td><td>EMEA</td><td>$28,400.00</td><td>Cleared</td><td></td></tr>\n"
            "<tr><td>15</td><td>ACT-10015</td><td>US-East</td><td>$53,200.00</td><td>Cleared</td><td></td></tr>\n"
            "<tr><td>16</td><td>ACT-10016</td><td>APAC</td><td>$11,750.00</td><td>Cleared</td><td></td></tr>\n"
            "<tr><td>17</td><td>ACT-10017</td><td>EMEA</td><td>$6,430.00</td><td>Cleared</td><td></td></tr>\n"
            "<tr><td>18</td><td>ACT-10018</td><td>US-West</td><td>$39,800.00</td><td>Cleared</td><td></td></tr>\n"
            "<tr><td>19</td><td>ACT-10019</td><td>US-East</td><td>$2,100.00</td><td>ERROR</td>"
            "<td>DATABASE CONNECTION FAILED: ORA-12541 TNS no listener on FINDB-PROD-03</td></tr>\n"
            "<tr><td>20</td><td>ACT-10020</td><td>APAC</td><td>$14,560.00</td><td>Cleared</td><td></td></tr>\n"
            "<tr><td>21</td><td>ACT-10021</td><td>US-East</td><td>$8,900.00</td><td>Cleared</td><td></td></tr>\n"
            "<tr><td>22</td><td>ACT-10022</td><td>EMEA</td><td>$25,340.00</td><td>Cleared</td><td></td></tr>\n"
            "<tr><td>23</td><td>ACT-10023</td><td>US-West</td><td>$19,200.00</td><td>Cleared</td><td></td></tr>\n"
            "<tr><td>24</td><td>ACT-10024</td><td>APAC</td><td>$33,100.00</td><td>Pending</td><td></td></tr>\n"
            "<tr><td>25</td><td>ACT-10025</td><td>US-East</td><td>$4,780.00</td><td>Cleared</td><td></td></tr>\n"
            "</table>\n\n"
            "As you can see in row 19, the import failed with a database connection error. "
            "This started happening this morning around 7:30 AM.",
            "Trying to load our Contoso Financial Services Q4 reconciliation data and row 19 "
            "out of 50+ keeps failing. Here is the output:\n\n"
            "<table border='1'>\n"
            "<tr><th>ID</th><th>Account</th><th>Debit</th><th>Credit</th><th>Status</th></tr>\n"
            "<tr><td>1</td><td>GL-5001</td><td>$10,000</td><td>$0</td><td>OK</td></tr>\n"
            "<tr><td>2</td><td>GL-5002</td><td>$0</td><td>$10,000</td><td>OK</td></tr>\n"
            "<tr><td>3</td><td>GL-5003</td><td>$25,000</td><td>$0</td><td>OK</td></tr>\n"
            "<tr><td>4</td><td>GL-5004</td><td>$0</td><td>$25,000</td><td>OK</td></tr>\n"
            "<tr><td>5</td><td>GL-5005</td><td>$15,000</td><td>$0</td><td>OK</td></tr>\n"
            "<tr><td>6</td><td>GL-5006</td><td>$0</td><td>$15,000</td><td>OK</td></tr>\n"
            "<tr><td>7</td><td>GL-5007</td><td>$42,000</td><td>$0</td><td>OK</td></tr>\n"
            "<tr><td>8</td><td>GL-5008</td><td>$0</td><td>$42,000</td><td>OK</td></tr>\n"
            "<tr><td>9</td><td>GL-5009</td><td>$8,500</td><td>$0</td><td>FAIL: "
            "ORA-12541 TNS:no listener — connection to FINDB-PROD-03 refused</td></tr>\n"
            "<tr><td>10</td><td>GL-5010</td><td>$0</td><td>$8,500</td><td>OK</td></tr>\n"
            "</table>\n\n"
            "The actual problem is that our production Oracle database listener on FINDB-PROD-03 "
            "appears to be down. All rows after the failure also failed but I truncated the table. "
            "This is blocking the entire finance team's end-of-quarter close.",
        ],
        next_best_actions=[
            "Ignore the massive HTML table data — the actual issue is buried in row 19: "
            "ORA-12541 TNS no listener on FINDB-PROD-03. The Oracle database listener "
            "service is down on the production finance database server.",
            "Investigate the Oracle TNS listener on FINDB-PROD-03. Check if the listener "
            "service crashed or was stopped during maintenance, and restart it.",
        ],
        remediation_steps=[
            [
                "SSH to FINDB-PROD-03 and check the Oracle TNS listener status with lsnrctl status",
                "If the listener is down, restart it with lsnrctl start",
                "Check the listener log for the root cause of the shutdown",
                "Verify database connectivity from the application server after restart",
                "Re-run the failed reconciliation import and confirm all rows process successfully",
            ],
        ],
        tags=["data-cleanup", "html-table-paste"],
    ),
    # ──────────────────────────────────────────────────────────────────
    # 25. Heavy OCR artifacts from scanned/faxed document
    # ──────────────────────────────────────────────────────────────────
    Scenario(
        scenario_id="cleanup-extreme-ocr-artifacts",
        category="Hardware & Peripherals",
        priority="P3",
        assigned_team="Endpoint Engineering",
        needs_escalation=False,
        missing_information=["device_info", "steps_to_reproduce"],
        subjects=[
            "Lapt0p batt3ry n0t charg1ng — p1ease he1p",
            "N0teb00k battery fa11s t0 charge — need repa1r",
        ],
        descriptions=[
            "He11o IT supp0rt,\n\n"
            "I arn wr1ting t0 rep0rt that rny C0ntos0 F1nanc1al Serv1ces 1ssued "
            "1apt0p batt3ry w111 n0t charge. The 1apt0p 1s a De11 Lat1tude 5540 "
            "and 1t was w0rk1ng f1ne unt11 1ast week. N0w when I p1ug 1n the "
            "charg3r, the 11ght 0n the s1de b11nks 0range three t1mes and then "
            "turns 0ff. The batt3ry 1s stuck at 7% and w0n't g0 any h1gher.\n\n"
            "I have tr1ed:\n"
            "- Us1ng a d1fferent p0wer 0ut1et\n"
            "- A d1fferent charg1ng cab1e fr0rn rny c011eague\n"
            "- Shutt1ng d0wn c0rnplete1y and charg1ng wh11e 0ff\n\n"
            "N0ne 0f th1s w0rked. I arn 0n the trad1ng f100r and need rny "
            "1apt0p rn0b11e f0r rneeet1ngs. P1ease adv1se.",
            "T1cket subrn1tted v1a fax scan:\n\n"
            "Dea1 He1p Desk,\n\n"
            "My w0rk n0teb00k (De11 Lat1tude ser1es) batt3ry 1s n0t h01d1ng "
            "a charge at a11. It dr0ps fr0rn 1OO% t0 O% 1n ab0ut 2O rn1nutes "
            "even when d01ng n0th1ng. The batt3ry hea1th check 1n the B1OS "
            "says 'P00r' and recornrnends rep1acernent. I arn at the C0ntos0 "
            "F1nanc1al Serv1ces bu11d1ng C, 4th f100r. I've had th1s 1apt0p "
            "f0r ab0ut 3 years. The rn0de1 nurnber 0n the b0tt0rn 1s hard "
            "t0 read but 1 th1nk 1t says P/N: 0X4F2R. P1ease send s0rne0ne "
            "0r sh1p rne a new batt3ry.",
        ],
        next_best_actions=[
            "Decode the OCR-garbled text: the user's Dell Latitude laptop battery is not "
            "charging (orange blinking light, stuck at 7%). They have tried alternate "
            "outlets and chargers. Likely a failed battery or charging circuit.",
            "The OCR artifacts obscure the text but the issue is clear: Dell Latitude "
            "battery failure. Check warranty status and order a replacement battery "
            "or schedule an on-site technician.",
        ],
        remediation_steps=[
            [
                "Run Dell battery diagnostics via the BIOS pre-boot menu (F12 > Diagnostics)",
                "Check the battery health status in Dell Power Manager or BIOS",
                "If battery health is Poor or Failed, order a replacement battery under warranty",
                "If out of warranty, submit a procurement request for a new OEM battery",
                "Schedule on-site battery replacement or ship to the user's building",
            ],
        ],
        tags=["data-cleanup", "ocr-artifacts"],
    ),
    # ──────────────────────────────────────────────────────────────────
    # 26. Extremely terse ticket with almost no information
    # ──────────────────────────────────────────────────────────────────
    Scenario(
        scenario_id="cleanup-terse-one-word",
        category="General Inquiry",
        priority="P4",
        assigned_team="None",
        needs_escalation=False,
        missing_information=[
            "affected_system",
            "error_message",
            "steps_to_reproduce",
            "affected_users",
            "environment_details",
            "device_info",
            "application_version",
            "business_impact",
            "contact_info",
        ],
        subjects=[
            "help",
            "broken",
        ],
        descriptions=[
            "broken",
            "it doesnt work",
        ],
        next_best_actions=[
            "This ticket has virtually no actionable information. Reply to the user and ask "
            "them to specify: what system or application is affected, what error they are "
            "seeing, what they were trying to do, and their contact details.",
            "The ticket is too terse to act on. Request clarification: which device, which "
            "application, what error message, and the business impact so the ticket can be "
            "properly categorized and prioritized.",
        ],
        remediation_steps=[
            [
                "Reply to the user requesting basic details: affected system, error message, "
                "and what they were trying to do",
                "Ask for their device type, operating system, and application version",
                "Request their preferred contact method and business impact/urgency",
                "Once sufficient information is gathered, re-categorize and assign the ticket",
            ],
        ],
        tags=["data-cleanup", "terse-ticket"],
    ),
    # ──────────────────────────────────────────────────────────────────
    # 27. Terminal/PowerShell output dump with issue buried in one line
    # ──────────────────────────────────────────────────────────────────
    Scenario(
        scenario_id="cleanup-terminal-output-dump",
        category="Network & Connectivity",
        priority="P2",
        assigned_team="Network Operations",
        needs_escalation=False,
        missing_information=["error_message", "network_location"],
        subjects=[
            "Network issue — here's everything I ran (ipconfig, tracert, nslookup)",
            "DNS not resolving — dumping all my diagnostic output",
        ],
        descriptions=[
            "Something is wrong with my network. I'm on the Contoso Financial Services "
            "trading floor, desk 14B. Here is everything I ran:\n\n"
            "PS C:\\Users\\jsmith> ipconfig /all\n\n"
            "Windows IP Configuration\n\n"
            "   Host Name . . . . . . . . . . . . : CNTSO-WS-4021\n"
            "   Primary Dns Suffix  . . . . . . . : contoso.local\n"
            "   Node Type . . . . . . . . . . . . : Hybrid\n"
            "   IP Routing Enabled. . . . . . . . : No\n\n"
            "Ethernet adapter Ethernet0:\n\n"
            "   Connection-specific DNS Suffix  . : contoso.local\n"
            "   IPv4 Address. . . . . . . . . . . : 10.52.14.87\n"
            "   Subnet Mask . . . . . . . . . . . : 255.255.254.0\n"
            "   Default Gateway . . . . . . . . . : 10.52.14.1\n"
            "   DNS Servers . . . . . . . . . . . : 10.10.1.53\n"
            "                                       10.10.2.53\n\n"
            "PS C:\\Users\\jsmith> nslookup riskportal.contoso.local\n"
            "Server:  dc01.contoso.local\n"
            "Address:  10.10.1.53\n\n"
            "*** dc01.contoso.local can't find riskportal.contoso.local: Non-existent domain\n\n"
            "PS C:\\Users\\jsmith> nslookup google.com\n"
            "Server:  dc01.contoso.local\n"
            "Address:  10.10.1.53\n\n"
            "Non-authoritative answer:\n"
            "Name:    google.com\n"
            "Address:  142.250.80.46\n\n"
            "PS C:\\Users\\jsmith> tracert riskportal.contoso.local\n"
            "Unable to resolve target system name riskportal.contoso.local.\n\n"
            "PS C:\\Users\\jsmith> ping 10.52.14.1\n"
            "Reply from 10.52.14.1: bytes=32 time<1ms TTL=255\n"
            "Reply from 10.52.14.1: bytes=32 time<1ms TTL=255\n\n"
            "So basically riskportal.contoso.local won't resolve but everything "
            "else works fine. I need this for the live trading dashboard.",
            "I can't reach the risk analytics portal and I dumped all my output below. "
            "I'm at Contoso Financial Services building A, floor 3.\n\n"
            "PS C:\\Users\\alee> Get-NetIPAddress | Format-Table\n\n"
            "ifIndex IPAddress                     PrefixLength PrefixOrigin\n"
            "------- ---------                     ------------ ------------\n"
            "12      10.52.14.92                   23           Dhcp\n"
            "1       127.0.0.1                     8            WellKnown\n"
            "12      fe80::a4d1:7e2f:3b90:cf12%12  64           WellKnown\n\n"
            "PS C:\\Users\\alee> Resolve-DnsName riskportal.contoso.local\n"
            "Resolve-DnsName : riskportal.contoso.local : DNS name does not exist\n"
            "At line:1 char:1\n\n"
            "PS C:\\Users\\alee> Resolve-DnsName intranet.contoso.local\n"
            "Name             Type TTL Section IPAddress\n"
            "----             ---- --- ------- ---------\n"
            "intranet.contoso A    300 Answer  10.10.5.20\n\n"
            "PS C:\\Users\\alee> Test-NetConnection riskportal.contoso.local -Port 443\n"
            "WARNING: Name resolution of riskportal.contoso.local failed\n"
            "ComputerName : riskportal.contoso.local\n"
            "TcpTestSucceeded : False\n\n"
            "The only thing that's broken is DNS for riskportal.contoso.local. "
            "External DNS and other internal names resolve fine. This is blocking "
            "the entire trading floor.",
        ],
        next_best_actions=[
            "Cut through the terminal output dump — the issue is that the internal DNS "
            "record for riskportal.contoso.local is missing or was deleted. External "
            "DNS and other internal records work fine. Check the DNS zone for the "
            "missing A record.",
            "The diagnostic output confirms a DNS resolution failure specifically for "
            "riskportal.contoso.local. Investigate the internal DNS zone on the domain "
            "controllers for a missing or expired record.",
        ],
        remediation_steps=[
            [
                "Check the contoso.local DNS zone on the domain controllers for the riskportal host record",
                "If the record is missing, re-create the A record pointing to the correct server IP",
                "If the record exists, check for replication issues between DNS servers 10.10.1.53 and 10.10.2.53",
                "Flush DNS caches on the affected workstations with ipconfig /flushdns",
                "Verify resolution from the trading floor and confirm access to the risk portal",
            ],
        ],
        tags=["data-cleanup", "terminal-output"],
    ),
    # ──────────────────────────────────────────────────────────────────
    # 28. Machine-generated monitoring alert dump (Datadog/PagerDuty/Nagios)
    # ──────────────────────────────────────────────────────────────────
    Scenario(
        scenario_id="cleanup-auto-monitoring-alert",
        category="Software & Applications",
        priority="P2",
        assigned_team="Enterprise Applications",
        needs_escalation=False,
        missing_information=["application_version", "environment_details"],
        subjects=[
            "[ALERT] CRITICAL — contosofinapp-prod-web-03 — Memory threshold exceeded",
            "[PagerDuty] Incident #48291 — Application memory leak detected",
        ],
        descriptions=[
            '{"alert_id":"ALT-2024-48291","source":"datadog","severity":"CRITICAL",'
            '"host":"contosofinapp-prod-web-03","service":"contoso-risk-api",'
            '"metric":"system.mem.used","value":97.3,"threshold":90.0,'
            '"unit":"percent","timestamp":"2024-11-15T07:23:41Z",'
            '"tags":["env:production","team:finservices","app:risk-api"],'
            '"message":"Memory usage on contosofinapp-prod-web-03 has exceeded '
            '97% for the last 15 minutes."}\n\n'
            '{"alert_id":"ALT-2024-48292","source":"datadog","severity":"WARNING",'
            '"host":"contosofinapp-prod-web-03","service":"contoso-risk-api",'
            '"metric":"system.cpu.user","value":88.5,"threshold":80.0,'
            '"unit":"percent","timestamp":"2024-11-15T07:24:02Z",'
            '"tags":["env:production","team:finservices","app:risk-api"],'
            '"message":"CPU usage elevated, likely due to memory pressure and '
            'excessive garbage collection."}\n\n'
            '{"alert_id":"ALT-2024-48293","source":"datadog","severity":"WARNING",'
            '"host":"contosofinapp-prod-web-03","service":"contoso-risk-api",'
            '"metric":"jvm.heap.used","value":3891,"threshold":3584,'
            '"unit":"megabytes","timestamp":"2024-11-15T07:24:15Z",'
            '"tags":["env:production","team:finservices","app:risk-api","runtime:jvm"],'
            '"message":"JVM heap usage at 3891 MB out of 4096 MB max. Heap is not '
            "being reclaimed — possible memory leak in the Contoso Financial Services "
            'risk calculation API."}\n\n'
            "The above alerts were auto-forwarded from Datadog. The risk-api service on "
            "contosofinapp-prod-web-03 appears to have a memory leak that is causing "
            "the JVM heap to fill up and not be garbage collected.",
            "[PagerDuty Incident #48291]\n"
            "Status: TRIGGERED\n"
            "Urgency: HIGH\n"
            "Service: Contoso Risk API (Production)\n"
            "Assigned to: FinServices On-Call\n"
            "Created: 2024-11-15T07:23:41Z\n\n"
            "--- Alert Details ---\n"
            '{"monitor_id":119284,"monitor_name":"[Prod] Memory Critical — Risk API",'
            '"host":"contosofinapp-prod-web-03","ip":"10.20.5.103",'
            '"current_value":"97.3%","threshold":"90%","duration":"15m",'
            '"escalation_policy":"FinServices-P1","responders":['
            '{"name":"On-Call Engineer","email":"oncall@contoso.com"}]}\n\n'
            "--- Runbook Link ---\n"
            "https://wiki.contoso.local/runbooks/risk-api-memory-leak\n\n"
            "--- Recent Deployments ---\n"
            "2024-11-14 22:15 UTC — risk-api v3.8.2 deployed to prod (contains fix for "
            "JIRA-4521: add caching to position calculator)\n\n"
            "Likely root cause: the v3.8.2 deployment added an unbounded cache to the "
            "position calculator module that is not evicting entries. The Contoso Financial "
            "Services risk API has been slowly consuming memory since the deployment "
            "14 hours ago.",
        ],
        next_best_actions=[
            "Parse the machine-generated alert JSON — the issue is a memory leak on "
            "contosofinapp-prod-web-03 in the Contoso risk-api service. JVM heap is at "
            "97% and not being reclaimed. Likely caused by the v3.8.2 deployment.",
            "The monitoring alerts point to a memory leak in the risk-api after the "
            "v3.8.2 deployment. The unbounded cache in the position calculator is the "
            "likely root cause. Roll back or add cache eviction.",
        ],
        remediation_steps=[
            [
                "Immediately restart the risk-api service on contosofinapp-prod-web-03 to restore service",
                "Investigate the v3.8.2 deployment's position calculator cache for missing eviction policy",
                "Roll back to v3.8.1 if the leak cannot be quickly patched",
                "Add a bounded cache with TTL eviction to the position calculator module",
                "Monitor JVM heap metrics after the fix to confirm memory is stable",
            ],
        ],
        tags=["data-cleanup", "monitoring-alert"],
    ),
    # ──────────────────────────────────────────────────────────────────
    # 29. Double-encoded UTF-8 creating mojibake
    # ──────────────────────────────────────────────────────────────────
    Scenario(
        scenario_id="cleanup-double-encoded-utf8",
        category="Software & Applications",
        priority="P3",
        assigned_team="Enterprise Applications",
        needs_escalation=False,
        missing_information=["application_version", "steps_to_reproduce"],
        subjects=[
            "Localization bug — characters showing as Ã© Ã¼ Ã¶ in web app",
            "Internal app displaying Ã±, Ã©, Ã¼ instead of proper characters",
        ],
        descriptions=[
            "Hi team,\n\n"
            "Our Contoso Financial Services internal compliance portal is displaying garbled "
            "characters for any non-ASCII text. Here are some examples of what we see:\n\n"
            "- Employee name 'José García' displays as 'JosÃ© GarcÃ\\xada'\n"
            "- Department 'Zürich Office' displays as 'ZÃ¼rich Office'\n"
            "- Client name 'François Müller' displays as 'FranÃ§ois MÃ¼ller'\n"
            "- Report title 'Année Fiscale' displays as 'AnnÃ©e Fiscale'\n"
            "- Branch 'São Paulo' displays as 'SÃ£o Paulo'\n\n"
            "This started after the latest deployment on Thursday. The database has the "
            "correct UTF-8 data — I verified by querying directly. The issue only appears "
            "in the web interface. It looks like the text is being double-encoded: the "
            "server reads UTF-8 bytes, interprets them as Latin-1, and then re-encodes to "
            "UTF-8. This is affecting every page that displays international characters. "
            "The compliance team in our European offices cannot use the portal because "
            "all their reports are unreadable.",
            "Since the Thursday release, the Contoso Financial Services HR self-service "
            "portal is showing mojibake for all accented characters:\n\n"
            "- 'Ãœbersicht' instead of 'Übersicht' (German overview page)\n"
            "- 'EspaÃ±ol' instead of 'Español' (language selector)\n"
            "- 'RÃ©sumÃ©' instead of 'Résumé' (document upload section)\n"
            "- 'DÃ¼sseldorf' instead of 'Düsseldorf' (office location)\n"
            "- 'PeÃ±a' instead of 'Peña' (employee surnames)\n\n"
            "The issue is clearly a double-encoding problem. The Content-Type header "
            "on the page says 'text/html; charset=utf-8' but the server middleware "
            "appears to be treating the already-UTF-8 database output as ISO-8859-1 "
            "and encoding it again. I confirmed by checking the raw bytes — the "
            "two-byte UTF-8 sequence for 'é' (0xC3 0xA9) is being treated as two "
            "separate Latin-1 characters 'Ã' and '©'. This affects all 200+ employees "
            "in EMEA offices.",
        ],
        next_best_actions=[
            "The mojibake characters (Ã©, Ã¼, Ã¶, etc.) indicate a classic double-encoding "
            "bug: UTF-8 data is being re-encoded as if it were Latin-1. Investigate the "
            "server middleware's character encoding configuration changed in Thursday's release.",
            "Check the application server's response encoding pipeline. The database stores "
            "correct UTF-8 but the middleware is double-encoding it. Review the Thursday "
            "deployment for changes to character set handling or Content-Type headers.",
        ],
        remediation_steps=[
            [
                "Review the Thursday deployment's changes for any modifications to character "
                "encoding, Content-Type headers, or database connection string charset parameters",
                "Check the application middleware for a layer that is converting UTF-8 bytes "
                "to Latin-1 before re-encoding to UTF-8",
                "Fix the encoding pipeline to pass through UTF-8 data without re-interpretation",
                "Test with known international characters (é, ü, ö, ñ, ç) to confirm the fix",
                "Deploy the fix and verify all EMEA office portals display correctly",
            ],
        ],
        tags=["data-cleanup", "double-encoded-utf8"],
    ),
    # ──────────────────────────────────────────────────────────────────
    # 30. Email with 90% legal disclaimers in 5 languages
    # ──────────────────────────────────────────────────────────────────
    Scenario(
        scenario_id="cleanup-massive-disclaimer-chain",
        category="Access & Authentication",
        priority="P2",
        assigned_team="Identity & Access Management",
        needs_escalation=False,
        missing_information=["device_info", "authentication_method"],
        subjects=[
            "MFA not working after phone replacement — URGENT",
            "Cannot authenticate — new phone, old MFA still linked",
        ],
        descriptions=[
            "Hi, I replaced my phone last weekend and now I can't log into anything "
            "at Contoso Financial Services because MFA keeps sending codes to my old "
            "device which I no longer have. I need this resolved today — I have "
            "regulatory filings due by 5 PM.\n\n"
            "========================================\n"
            "CONFIDENTIALITY NOTICE: This email and any attachments are for the "
            "exclusive and confidential use of the intended recipient. If you are not "
            "the intended recipient, please do not read, distribute, or take action "
            "based on this message. If you have received this in error, please notify "
            "the sender immediately and delete this message from your system.\n"
            "========================================\n"
            "AVIS DE CONFIDENTIALITÉ : Ce courriel et toute pièce jointe sont "
            "destinés exclusivement à l'usage confidentiel du destinataire prévu. "
            "Si vous n'êtes pas le destinataire prévu, veuillez ne pas lire, "
            "distribuer ou agir sur la base de ce message. Si vous avez reçu ce "
            "message par erreur, veuillez en informer immédiatement l'expéditeur "
            "et supprimer ce message de votre système.\n"
            "========================================\n"
            "VERTRAULICHKEITSHINWEIS: Diese E-Mail und alle Anhänge sind "
            "ausschließlich für den vertraulichen Gebrauch des beabsichtigten "
            "Empfängers bestimmt. Wenn Sie nicht der beabsichtigte Empfänger sind, "
            "lesen, verteilen oder handeln Sie bitte nicht auf der Grundlage dieser "
            "Nachricht. Wenn Sie diese Nachricht irrtümlich erhalten haben, "
            "benachrichtigen Sie bitte umgehend den Absender und löschen Sie diese "
            "Nachricht aus Ihrem System.\n"
            "========================================\n"
            "機密通知：このメールおよび添付ファイルは、意図された受信者の"
            "排他的かつ機密的な使用を目的としています。意図された受信者でない場合は、"
            "このメッセージを読んだり、配布したり、行動を起こしたりしないでください。"
            "誤って受信した場合は、直ちに送信者に通知し、システムからこのメッセージを"
            "削除してください。\n"
            "========================================\n"
            "AVISO DE CONFIDENCIALIDADE: Este e-mail e quaisquer anexos são para uso "
            "exclusivo e confidencial do destinatário pretendido. Se você não for o "
            "destinatário pretendido, por favor não leia, distribua ou tome ações com "
            "base nesta mensagem. Se você recebeu esta mensagem por engano, por favor "
            "notifique o remetente imediatamente e exclua esta mensagem do seu sistema.\n"
            "========================================",
            "I got a new iPhone 15 and my old iPhone 12 was wiped and traded in. "
            "Now the Contoso Financial Services Okta MFA prompt goes to the old "
            "device that no longer exists. I'm completely locked out of email, "
            "SharePoint, and the risk analytics portal. My manager (David Chen, "
            "VP of Trading Operations) can vouch for my identity. Please reset "
            "my MFA to my new phone ASAP.\n\n"
            "────────────────────────────────────────\n"
            "LEGAL DISCLAIMER: The information contained in this communication is "
            "confidential and may be legally privileged. It is intended solely for "
            "the use of the individual or entity to whom it is addressed. Access to "
            "this email by anyone else is unauthorized. If you are not the intended "
            "recipient, any disclosure, copying, distribution or any action taken or "
            "omitted to be taken in reliance on it, is prohibited and may be unlawful.\n"
            "────────────────────────────────────────\n"
            "AVIS JURIDIQUE : Les informations contenues dans cette communication "
            "sont confidentielles et peuvent être légalement protégées. Elles sont "
            "destinées uniquement à l'usage de la personne ou de l'entité à laquelle "
            "elles sont adressées. L'accès à ce courriel par toute autre personne "
            "n'est pas autorisé.\n"
            "────────────────────────────────────────\n"
            "RECHTSHINWEIS: Die in dieser Mitteilung enthaltenen Informationen sind "
            "vertraulich und können rechtlich geschützt sein. Sie sind ausschließlich "
            "für die Nutzung durch die Person oder Organisation bestimmt, an die sie "
            "gerichtet sind. Der Zugriff auf diese E-Mail durch andere Personen ist "
            "nicht gestattet.\n"
            "────────────────────────────────────────\n"
            "法的免責事項：この通信に含まれる情報は機密であり、法的に保護されて"
            "いる場合があります。これは、宛先の個人または団体のみが使用することを"
            "目的としています。\n"
            "────────────────────────────────────────\n"
            "AVISO LEGAL: As informações contidas nesta comunicação são confidenciais "
            "e podem ser legalmente protegidas. Destinam-se exclusivamente ao uso do "
            "indivíduo ou entidade a quem são endereçadas. O acesso a este e-mail por "
            "qualquer outra pessoa não é autorizado.\n"
            "────────────────────────────────────────",
        ],
        next_best_actions=[
            "Ignore the massive multi-language legal disclaimers — the actual issue is "
            "two sentences long: the user replaced their phone and MFA is still linked "
            "to the old device. They are locked out of all Contoso Financial Services "
            "systems and need an MFA reset.",
            "Reset the user's MFA enrollment in Okta after identity verification. The "
            "disclaimers are noise — the issue is a phone replacement requiring MFA "
            "re-enrollment.",
        ],
        remediation_steps=[
            [
                "Verify the user's identity through an alternate method (manager confirmation, "
                "security questions, or in-person verification)",
                "Reset the user's MFA enrollment in Okta to remove the old device",
                "Guide the user through enrolling their new phone in Okta Verify",
                "Test authentication to email, SharePoint, and the risk analytics portal",
                "Advise the user to set up a backup MFA method to prevent future lockouts",
            ],
        ],
        tags=["data-cleanup", "disclaimer-chain"],
    ),
    # ──────────────────────────────────────────────────────────────────
    # 31. Two separate email conversations merged/interleaved by mail client
    # ──────────────────────────────────────────────────────────────────
    Scenario(
        scenario_id="cleanup-interleaved-conversations",
        category="Hardware & Peripherals",
        priority="P3",
        assigned_team="Endpoint Engineering",
        needs_escalation=False,
        missing_information=["device_info", "error_message"],
        subjects=[
            "RE: Monitor flickering + software license question (two issues)",
            "RE: RE: Display problem / also need Adobe license — mixed thread",
        ],
        descriptions=[
            "--- Conversation A: Monitor Issue ---\n"
            "From: Sarah Kim <skim@contoso.com>\n"
            "Date: Monday 8:30 AM\n"
            "My external monitor (Dell U2722D) connected to the Contoso Financial Services "
            "issued laptop keeps flickering every few seconds. It's a rapid black-flash "
            "that makes it unusable.\n\n"
            "--- Conversation B: Software License ---\n"
            "From: Sarah Kim <skim@contoso.com>\n"
            "Date: Monday 8:45 AM\n"
            "Separately, I need an Adobe Acrobat Pro license for the compliance team. We "
            "have 5 people who need to edit and redact PDF documents for regulatory filings.\n\n"
            "--- Conversation A continued ---\n"
            "From: Help Desk\n"
            "Date: Monday 9:15 AM\n"
            "> Have you tried a different cable or port?\n\n"
            "From: Sarah Kim\n"
            "Date: Monday 9:30 AM\n"
            "Yes, I tried both HDMI and USB-C cables. Same flickering on both. I also "
            "tried the monitor with a colleague's laptop and it works fine, so the issue "
            "might be my laptop's GPU or driver.\n\n"
            "--- Conversation B continued ---\n"
            "From: Software Asset Team\n"
            "Date: Monday 10:00 AM\n"
            "> Please submit a request through the software catalog for Adobe Acrobat Pro.\n\n"
            "From: Sarah Kim\n"
            "Date: Monday 10:15 AM\n"
            "Done, I submitted request REQ-7823 for 5 licenses. But more urgently, the "
            "monitor flickering is getting worse — now it's happening every 2-3 seconds "
            "and I can barely work. I'm on the Contoso Financial Services trading floor "
            "and need this fixed today.",
            "From: Tom Nguyen <tnguyen@contoso.com>\n"
            "To: Help Desk\n\n"
            "I have two issues that somehow got merged into one thread:\n\n"
            "ISSUE 1 — MONITOR: My Dell P2419H monitor goes completely black for 1-2 "
            "seconds randomly throughout the day. It happens about every 5 minutes. "
            "I've checked the power cable, tried different display ports on my Contoso "
            "Financial Services Dell Latitude 5550 docking station, and updated the "
            "Intel graphics driver to the latest version. Nothing helps. The monitor "
            "works fine when connected directly to another laptop without the dock.\n\n"
            "ISSUE 2 — SOFTWARE: I also need my Visio Pro license renewed. It expired "
            "last week and I can't open project architecture diagrams. License key is "
            "tied to my contoso.com account. The software catalog shows it as 'pending "
            "renewal' since last Tuesday.\n\n"
            "The monitor issue is much more urgent — it's affecting my productivity on "
            "the trading analytics project. The Visio thing can wait a few days. Please "
            "prioritize the hardware issue. I'm in Building A, 6th floor, desk 612.",
        ],
        next_best_actions=[
            "Separate the two interleaved conversations: (1) Monitor flickering — likely "
            "a laptop GPU/driver or docking station issue since the monitor works on other "
            "machines. (2) Software license request — already submitted, lower priority. "
            "Prioritize the hardware issue.",
            "The interleaved thread contains two distinct issues. The monitor flickering "
            "is the priority — investigate the docking station and laptop display driver. "
            "The software license is secondary and already in the request queue.",
        ],
        remediation_steps=[
            [
                "For the monitor issue: update the laptop's display/GPU drivers to the latest version",
                "Test with a different docking station to isolate whether the dock is faulty",
                "If the dock is the issue, replace it; if the laptop GPU is the issue, schedule a repair",
                "For the software license: follow up on the pending catalog request and expedite if needed",
                "Close as two separate tickets to track each issue independently",
            ],
        ],
        tags=["data-cleanup", "interleaved-conversations"],
    ),
    # ──────────────────────────────────────────────────────────────────
    # Massive pasted document text burying the real issue
    # ──────────────────────────────────────────────────────────────────
    Scenario(
        scenario_id="cleanup-massive-pasted-document",
        category="Software & Applications",
        priority="P3",
        assigned_team="Enterprise Applications",
        needs_escalation=False,
        missing_information=["error_message", "steps_to_reproduce"],
        subjects=[
            "Cannot access Compliance Policy Library on SharePoint",
            "SharePoint library returning 403 after migration — pasted doc for context",
        ],
        descriptions=[
            "I keep getting a 403 Forbidden error when I click the Compliance Policy Library "
            "link on SharePoint. It worked fine before the migration last Friday. Here is the "
            "document I was trying to access, for context:\n\n"
            "CONTOSO FINANCIAL SERVICES — DATA RETENTION POLICY v4.2\n"
            "Effective Date: January 15, 2026\n"
            "Classification: Internal — Confidential\n\n"
            "SECTION 1: SCOPE AND APPLICABILITY\n"
            "1.1 This policy applies to all employees, contractors, and third-party service "
            "providers of Contoso Financial Services and its subsidiaries.\n"
            "1.2 All financial records, including but not limited to trade confirmations, "
            "settlement records, and account statements, must be retained for a minimum of "
            "seven (7) years from the date of creation in accordance with SEC Rule 17a-4.\n"
            "1.3 Electronic communications, including emails, instant messages, Bloomberg chat "
            "logs, and recorded phone lines, must be archived in an immutable format for five "
            "(5) years.\n"
            "1.4 Client onboarding documentation including KYC and AML verification records "
            "shall be maintained for the duration of the client relationship plus five (5) "
            "years after termination.\n\n"
            "SECTION 2: DATA CLASSIFICATION\n"
            "2.1 All data shall be classified into one of four tiers:\n"
            "  Tier 1 — Public: Annual reports, press releases, marketing materials\n"
            "  Tier 2 — Internal: Operational procedures, org charts, internal memos\n"
            "  Tier 3 — Confidential: Client PII, trading strategies, risk models\n"
            "  Tier 4 — Restricted: M&A materials, regulatory submissions, board minutes\n"
            "2.2 Tier 3 and Tier 4 data must be encrypted at rest and in transit.\n\n"
            "SECTION 3: ACCESS CONTROLS\n"
            "3.1 Access to Tier 3 and Tier 4 data requires manager approval and annual "
            "recertification through the PAM system.\n"
            "3.2 All access events must be logged and retained for audit for a minimum of "
            "three (3) years.\n"
            "3.3 Privileged access requires multi-factor authentication.\n\n"
            "SECTION 4: AUDIT AND COMPLIANCE\n"
            "4.1 Internal audits of data retention compliance shall be conducted quarterly.\n"
            "4.2 Any identified gaps must be remediated within thirty (30) calendar days.\n\n"
            "[Document continues for 43 more pages]\n\n"
            "Anyway, the actual problem is the 403 Forbidden error. Can someone fix the "
            "permissions on the migrated SharePoint site?",
            "SharePoint Compliance Policy Library gives me Access Denied (403) since the "
            "migration. I pasted the full text of the policy I need because I cannot download "
            "it anymore. The document is 47 pages of data retention and classification policy "
            "text. Please fix the permissions — I need to reference this for a regulatory "
            "filing by end of week.",
        ],
        next_best_actions=[
            "Investigate SharePoint 403 error for Compliance Policy Library after site "
            "migration — likely a permissions issue. Ignore the pasted document content.",
            "Check SharePoint site collection permissions that may not have been migrated "
            "correctly when the library was moved to the new site.",
        ],
        remediation_steps=[
            [
                "Check SharePoint site permissions for the migrated Compliance Policy Library",
                "Verify the user's group membership includes the new site collection",
                "Re-grant access if permissions were not carried over during migration",
                "Test access with the user's account after fixing permissions",
            ],
        ],
        tags=["data-cleanup", "massive-pasted-document", "buried-issue"],
    ),
    # ──────────────────────────────────────────────────────────────────
    # Embedded SVG image data with XML markup
    # ──────────────────────────────────────────────────────────────────
    Scenario(
        scenario_id="cleanup-embedded-svg-data",
        category="Hardware & Peripherals",
        priority="P3",
        assigned_team="Endpoint Engineering",
        needs_escalation=False,
        missing_information=["device_info", "application_version"],
        subjects=[
            "Monitor color profile wrong after driver update — inline screenshot",
            "Display colors shifted blue since NVIDIA update (see embedded image)",
        ],
        descriptions=[
            "After updating the NVIDIA GPU driver to version 550.67, my Dell U2722D monitor "
            "has a noticeable blue-ish tint. The sRGB mode looks washed out. I tried to paste "
            "a screenshot of the color test pattern but it came through as raw image data:\n\n"
            '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1920 1080" width="1920" '
            'height="1080"><defs><linearGradient id="grad1" x1="0%" y1="0%" x2="100%" '
            'y2="0%"><stop offset="0%" style="stop-color:rgb(255,0,0);stop-opacity:1"/>'
            '<stop offset="50%" style="stop-color:rgb(0,255,0);stop-opacity:1"/><stop '
            'offset="100%" style="stop-color:rgb(0,0,255);stop-opacity:1"/></linearGradient>'
            '<linearGradient id="grad2" x1="0%" y1="0%" x2="0%" y2="100%"><stop offset="0%" '
            'style="stop-color:rgb(255,255,255);stop-opacity:1"/><stop offset="100%" '
            'style="stop-color:rgb(0,0,0);stop-opacity:1"/></linearGradient></defs>'
            '<rect width="1920" height="540" fill="url(#grad1)"/><rect y="540" width="1920" '
            'height="540" fill="url(#grad2)"/><text x="50" y="50" font-family="Calibri" '
            'font-size="24" fill="white">Color Calibration Test Pattern — Dell U2722D'
            '</text><circle cx="960" cy="540" r="200" fill="none" stroke="white" '
            'stroke-width="2"/></svg>\n\n'
            "As you can see (if that renders), the gradient should be smooth but it looks "
            "banded on my screen. The issue started immediately after the NVIDIA driver update.",
            "My external monitor's colors are off since the GPU driver update. Everything has "
            "a blue tint and the contrast looks wrong. The monitor is a Dell U2722D connected "
            "via DisplayPort through a Lenovo ThinkPad USB-C dock. NVIDIA driver 550.67 was "
            "pushed by SCCM last night.",
        ],
        next_best_actions=[
            "Investigate monitor color profile shift after NVIDIA driver update to v550.67 — "
            "likely need to reapply the ICC color profile or roll back the driver.",
            "Check if the NVIDIA driver 550.67 push broke the ICC color profile on Dell "
            "U2722D monitors — may affect multiple users if deployed via SCCM.",
        ],
        remediation_steps=[
            [
                "Reapply the Dell U2722D ICC/sRGB color profile in NVIDIA Control Panel",
                "If that does not fix it, roll back the NVIDIA driver from 550.67 to the previous version",
                "Verify display color settings in Windows Color Management and NVIDIA settings",
                "If the issue affects multiple users, escalate to the SCCM team to halt the driver push",
            ],
        ],
        tags=["data-cleanup", "embedded-svg", "xml-data-inline"],
    ),
    # ──────────────────────────────────────────────────────────────────
    # Hex dump of network packet capture
    # ──────────────────────────────────────────────────────────────────
    Scenario(
        scenario_id="cleanup-hex-dump-network-capture",
        category="Network & Connectivity",
        priority="P2",
        assigned_team="Network Operations",
        needs_escalation=False,
        missing_information=["network_location", "affected_users"],
        subjects=[
            "Intermittent packet loss on trading floor — packet capture attached",
            "5-8% packet loss daily on VLAN 210 — hex dump below",
        ],
        descriptions=[
            "Every day between 14:00 and 14:15 UTC we see 5-8% packet loss on the trading "
            "floor VLAN 210. It's affecting FIX protocol connections to the exchange. I "
            "captured some packets — here is the raw hex dump:\n\n"
            "0000  00 1a 2b 3c 4d 5e 00 0c 29 8a 1b 2c 08 00 45 00  ..+<M^..)..,.E.\n"
            "0010  00 3c 1c 46 40 00 40 06 b1 e6 c0 a8 01 64 ac 10  .<.F@.@......d..\n"
            "0020  01 01 c0 23 01 bb a1 2b 3c 4d 00 00 00 00 a0 02  ...#...+<M......\n"
            "0030  ff ff 1a 2b 00 00 02 04 05 b4 04 02 08 0a 00 05  ...+............\n"
            "0040  8d 4a 00 00 00 00 01 03 03 07 00 00 00 00 00 00  .J..............\n"
            "0050  00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  ................\n"
            "0060  45 00 00 3c 1c 47 40 00 40 06 b1 e5 c0 a8 01 64  E..<.G@.@......d\n"
            "0070  ac 10 01 01 c0 24 01 bb a2 3c 4d 5e 00 00 00 00  .....$...<M^....\n"
            "0080  a0 02 ff ff 2b 3c 00 00 02 04 05 b4 04 02 08 0a  ....+<..........\n"
            "0090  00 05 8d 4b 00 00 00 00 01 03 03 07 00 00 00 00  ...K............\n"
            "00a0  00 00 00 00 00 00 00 00 00 00 00 00 00 00 00 00  ................\n"
            "00b0  45 00 00 28 1c 48 40 00 40 06 b1 f8 c0 a8 01 64  E..(.H@.@......d\n"
            "00c0  ac 10 01 01 c0 23 01 bb a1 2b 3c 4e 5a 6b 7c 8d  .....#...+<NZk|.\n"
            "[truncated — full capture is 12,847 packets]\n\n"
            "The pattern is consistent: packet loss starts at exactly 14:00 and stops at "
            "14:15. My guess is there's a backup job or batch process saturating the uplink.",
            "VLAN 210 (trading floor, Building 3) is experiencing daily packet loss between "
            "14:00-14:15 UTC. FIX connections to the exchange drop during this window. "
            "I have a full pcap capture but it's too large to attach. The hex dump excerpt "
            "above shows TCP SYN retransmissions during the affected period.",
        ],
        next_best_actions=[
            "Investigate scheduled packet loss on VLAN 210 between 14:00-14:15 UTC — "
            "correlate with network device logs and scheduled tasks on the trading floor.",
            "Analyze QoS configuration for VLAN 210 to ensure FIX protocol traffic has "
            "appropriate priority during the congestion window.",
        ],
        remediation_steps=[
            [
                "Review switch and router logs for VLAN 210 during the 14:00-14:15 UTC window",
                "Check for scheduled backup jobs or batch processes that may saturate the uplink",
                "Analyze QoS configuration to ensure FIX protocol traffic has appropriate priority",
                "If congestion confirmed, verify uplink capacity and consider traffic engineering",
            ],
        ],
        tags=["data-cleanup", "hex-dump", "network-capture"],
    ),
    # ──────────────────────────────────────────────────────────────────
    # Windows Event Log XML dump
    # ──────────────────────────────────────────────────────────────────
    Scenario(
        scenario_id="cleanup-event-log-xml-dump",
        category="Hardware & Peripherals",
        priority="P2",
        assigned_team="Endpoint Engineering",
        needs_escalation=False,
        missing_information=["device_info", "reproduction_frequency"],
        subjects=[
            "Blue screen on my laptop twice today — Event Viewer export",
            "BSOD DRIVER_IRQL_NOT_LESS_OR_EQUAL — event log XML below",
        ],
        descriptions=[
            "My laptop blue-screened twice today with DRIVER_IRQL_NOT_LESS_OR_EQUAL. Both "
            "times it happened when I plugged in my USB-C docking station. I exported the "
            "Event Viewer entries:\n\n"
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
            '    <Correlation ActivityID="{A1B2C3D4-E5F6-7890-ABCD-EF1234567890}"/>\n'
            '    <Execution ProcessID="0" ThreadID="0"/>\n'
            "    <Channel>System</Channel>\n"
            "    <Computer>WS-B3-0742.contoso.com</Computer>\n"
            "  </System>\n"
            "  <EventData>\n"
            '    <Data Name="BugcheckCode">0x000000d1</Data>\n'
            '    <Data Name="BugcheckParameter1">0xfffff80012345678</Data>\n'
            '    <Data Name="BugcheckParameter2">0x0000000000000002</Data>\n'
            '    <Data Name="BugcheckParameter3">0x0000000000000000</Data>\n'
            '    <Data Name="BugcheckParameter4">0xfffff80087654321</Data>\n'
            '    <Data Name="SleepInProgress">0</Data>\n'
            '    <Data Name="PowerButtonTimestamp">0</Data>\n'
            '    <Data Name="BootAppStatus">0</Data>\n'
            '    <Data Name="DumpFileSize">1073741824</Data>\n'
            '    <Data Name="DumpFile">C:\\Windows\\MEMORY.DMP</Data>\n'
            "  </EventData>\n"
            "</Event>\n\n"
            "The second crash produced a similar event. Both happened within 30 seconds of "
            "plugging in the dock. I'm on the 5th floor, Building 3.",
            "Two BSODs today (DRIVER_IRQL_NOT_LESS_OR_EQUAL, bugcheck 0xD1) both triggered "
            "when connecting my USB-C docking station. The full Event Viewer XML is pasted "
            "above. The minidump points to an ndis.sys call — possibly the dock's Ethernet "
            "adapter driver.",
        ],
        next_best_actions=[
            "Investigate DRIVER_IRQL_NOT_LESS_OR_EQUAL BSOD triggered by USB-C dock — "
            "likely a driver conflict with the dock's Ethernet or display adapter.",
            "Check minidump files for the faulting driver and update or roll back.",
        ],
        remediation_steps=[
            [
                "Check the minidump files (C:\\Windows\\Minidump) for the faulting driver name",
                "Update the docking station firmware and related USB-C/Ethernet drivers",
                "If a specific driver is identified, roll it back to the previous version",
                "Test with a different docking station to isolate whether it is dock-specific",
            ],
        ],
        tags=["data-cleanup", "event-log-xml", "windows-diagnostic"],
    ),
    # ──────────────────────────────────────────────────────────────────
    # Concatenated SCOM monitoring alerts
    # ──────────────────────────────────────────────────────────────────
    Scenario(
        scenario_id="cleanup-scom-alert-flood",
        category="Data & Storage",
        priority="P1",
        assigned_team="Data Platform",
        needs_escalation=True,
        missing_information=["business_impact", "affected_system"],
        subjects=[
            "FW: FW: FW: CRITICAL ALERTS — disk space warnings from SCOM",
            "Production SQL Server running out of disk — alert flood forwarded",
        ],
        descriptions=[
            "Forwarding all the SCOM alerts we've gotten this morning:\n\n"
            "--- Alert: Logical Disk Free Space is low ---\n"
            "Source: SQLPROD01.contoso.com\n"
            "Severity: Critical\n"
            "Generated: 2026-03-17 08:15:03 UTC\n"
            "Disk C: 2.1 GB free (4.2%) of 50 GB\n"
            "Resolution State: New\n"
            "Rule: Logical Disk Free Space (%) < 5%\n"
            "---\n\n"
            "--- Alert: Logical Disk Free Space is low ---\n"
            "Source: SQLPROD01.contoso.com\n"
            "Severity: Critical\n"
            "Generated: 2026-03-17 08:30:04 UTC\n"
            "Disk C: 1.9 GB free (3.8%) of 50 GB\n"
            "Resolution State: New\n"
            "---\n\n"
            "--- Alert: Logical Disk Free Space is low ---\n"
            "Source: SQLPROD01.contoso.com\n"
            "Severity: Critical\n"
            "Generated: 2026-03-17 08:45:05 UTC\n"
            "Disk C: 1.7 GB free (3.4%) of 50 GB\n"
            "Resolution State: New\n"
            "---\n\n"
            "--- Alert: Logical Disk Free Space is low ---\n"
            "Source: SQLPROD01.contoso.com\n"
            "Severity: Critical\n"
            "Generated: 2026-03-17 09:00:06 UTC\n"
            "Disk C: 1.5 GB free (3.0%) of 50 GB\n"
            "Resolution State: New\n"
            "---\n\n"
            "--- Alert: Logical Disk Free Space is low ---\n"
            "Source: SQLPROD01.contoso.com\n"
            "Severity: Critical\n"
            "Generated: 2026-03-17 09:15:07 UTC\n"
            "Disk C: 1.3 GB free (2.6%) of 50 GB\n"
            "Resolution State: New\n"
            "---\n\n"
            "The alerts are coming in every 15 minutes and the disk keeps shrinking. "
            "SQLPROD01 is our production SQL Server for the trading platform. If it runs "
            "out of disk space, trade execution will stop.",
            "SQLPROD01 production SQL Server C: drive is critically low on space (under 5% "
            "and falling). SCOM has been alerting every 15 minutes since 8 AM. I've "
            "forwarded all 12 alerts above. Need immediate intervention before the server "
            "runs out of space entirely.",
        ],
        next_best_actions=[
            "Immediately address critically low disk space on SQLPROD01 C: drive — "
            "production SQL Server is at risk of failing if disk reaches 0%.",
            "Free disk space on SQLPROD01 urgently and investigate what is consuming the "
            "C: drive. Check tempdb, error logs, and backup files.",
        ],
        remediation_steps=[
            [
                "Free immediate disk space by clearing temp files, IIS logs, and old backups on SQLPROD01",
                "Check if SQL Server tempdb or error logs are consuming excessive C: drive space",
                "Move any relocatable databases or logs to a dedicated data volume",
                "Add disk capacity and update SCOM alert thresholds once resolved",
            ],
        ],
        tags=["data-cleanup", "scom-alert-flood", "concatenated-alerts"],
    ),
    # ──────────────────────────────────────────────────────────────────
    # Multi-encoding mojibake chain
    # ──────────────────────────────────────────────────────────────────
    Scenario(
        scenario_id="cleanup-mojibake-multi-encoding",
        category="Hardware & Peripherals",
        priority="P3",
        assigned_team="Endpoint Engineering",
        needs_escalation=False,
        missing_information=["device_info", "application_version"],
        subjects=[
            "Printer driver error — weird characters in error message",
            "Cannot install printer driver — garbled mojibake error text",
        ],
        descriptions=[
            "I'm trying to install the driver for our Konica Minolta C308 printer and it "
            "keeps failing. The error message got garbled through multiple encoding layers. "
            "Here is what I see:\n\n"
            "First the dialog showed: â€˜Druckertreiber konnte nicht installiert "
            "werdenâ€™ â€” Fehlercode 0x800F0214\n\n"
            "Then I copied it to Notepad and it became: Ã¢â‚¬˜"
            "Cannot locate INF fileÃ¢â‚¬™\n\n"
            "My colleague sent me the error in an email and it got even worse: "
            "Ã£Â¢Ã¢â‚¬Å“Driver "
            "installation failedÃ£Â¢Ã¢â‚¬"
            "Â\n\n"
            "The original error appears to be in German but got double or triple encoded "
            "through our email system. The actual error code is 0x800F0214 and I'm on "
            "Windows 11.",
            "Konica Minolta C308 printer driver installation fails with error 0x800F0214 on "
            "Windows 11. The error text has been garbled through multiple character encoding "
            "conversions. The underlying error seems to be about a missing INF file in the "
            "driver package.",
        ],
        next_best_actions=[
            "Troubleshoot Konica Minolta C308 printer driver installation failure with error "
            "0x800F0214 — likely a missing INF file or unsigned driver issue.",
            "Download the correct Konica Minolta C308 driver package for Windows 11 and "
            "install using the Add Printer wizard.",
        ],
        remediation_steps=[
            [
                "Download the correct Konica Minolta C308 driver package for Windows 11 from the manufacturer",
                "Check if driver signing enforcement is blocking the installation",
                "Try installing the driver through the Add Printer wizard with the Have Disk option",
                "If 0x800F0214 persists, temporarily disable driver signature enforcement and retry",
            ],
        ],
        tags=["data-cleanup", "mojibake", "multi-encoding"],
    ),
    # ──────────────────────────────────────────────────────────────────
    # Cascading out-of-office auto-reply loop
    # ──────────────────────────────────────────────────────────────────
    Scenario(
        scenario_id="cleanup-auto-reply-cascade",
        category="Software & Applications",
        priority="P2",
        assigned_team="Enterprise Applications",
        needs_escalation=False,
        missing_information=["error_message", "affected_users"],
        subjects=[
            "RE: RE: RE: RE: Automatic reply: RE: Automatic reply: Room booking down",
            "Auto-reply loop burying real issue — booking system offline",
        ],
        descriptions=[
            "--- Automatic Reply ---\n"
            "Thank you for your email. I am currently out of the office from March 15-20 "
            "with limited access to email. For urgent matters please contact the IT Help "
            "Desk at x5000.\n"
            "Regards, Amanda Chen\n\n"
            "--- Automatic Reply ---\n"
            "Thank you for contacting IT Support. This is an automated acknowledgment. Your "
            "request has been logged and assigned ticket number AUTO-REF-28491. A technician "
            "will respond within 4 business hours.\n"
            "IT Help Desk\n\n"
            "--- Automatic Reply ---\n"
            "Thank you for your email. I am currently out of the office from March 15-20 "
            "with limited access to email. For urgent matters please contact the IT Help "
            "Desk at x5000.\n"
            "Regards, Amanda Chen\n\n"
            "--- Automatic Reply ---\n"
            "Thank you for contacting IT Support. This is an automated acknowledgment. Your "
            "request has been logged and assigned ticket number AUTO-REF-28492. A technician "
            "will respond within 4 business hours.\n"
            "IT Help Desk\n\n"
            "--- Automatic Reply ---\n"
            "Thank you for your email. I am currently out of the office from March 15-20.\n"
            "Regards, Amanda Chen\n\n"
            "--- Original Message (buried at the bottom) ---\n"
            "From: Amanda Chen\n"
            "Sent: Monday 8:15 AM\n"
            "To: IT Support\n"
            "Subject: Meeting room booking system down\n\n"
            "The meeting room booking system (RoomBook Pro) has been down since this morning. "
            "Nobody on Floor 7 can reserve conference rooms. We have client meetings this "
            "afternoon and need this fixed ASAP.",
            "There is an out-of-office auto-reply loop between my mailbox and the IT Help "
            "Desk auto-acknowledgment system. The real issue is at the bottom of the chain: "
            "the RoomBook Pro meeting room booking system is down for Floor 7.",
        ],
        next_best_actions=[
            "Investigate RoomBook Pro meeting room booking system outage on Floor 7 — ignore "
            "the cascading auto-reply chain and focus on restoring the booking service.",
            "Restore the RoomBook Pro booking system. Also fix the auto-reply loop between "
            "the user's OOO and the help desk auto-acknowledgment.",
        ],
        remediation_steps=[
            [
                "Check the RoomBook Pro application server status and logs",
                "Verify the Exchange room mailbox integration is functioning",
                "Restart the RoomBook Pro service if it is hung or crashed",
                "Communicate the estimated resolution time to affected users on Floor 7",
            ],
        ],
        tags=["data-cleanup", "auto-reply-loop", "buried-issue"],
    ),
    # ──────────────────────────────────────────────────────────────────
    # Tab-separated query result dump
    # ──────────────────────────────────────────────────────────────────
    Scenario(
        scenario_id="cleanup-tab-separated-query-results",
        category="Data & Storage",
        priority="P2",
        assigned_team="Data Platform",
        needs_escalation=False,
        missing_information=["environment_details", "timestamp"],
        subjects=[
            "Database query taking 45 minutes — full result set included",
            "SELECT on trades table degraded from 10s to 45min — data attached",
        ],
        descriptions=[
            "SELECT * FROM trades WHERE trade_date = '2026-03-17' now takes 45 minutes "
            "on SQLPROD03. It used to run in under 10 seconds. I think the index on "
            "trade_date got dropped during last night's maintenance window. Here is a "
            "sample of the result set to show it still returns correct data:\n\n"
            "trade_id\ttimestamp\tsymbol\tquantity\tprice\tstatus\taccount_id\n"
            "50001\t2026-03-17 09:30:01\tAAPL\t100\t178.42\tFILLED\tACCT-7890\n"
            "50002\t2026-03-17 09:30:01\tMSFT\t250\t415.67\tFILLED\tACCT-7891\n"
            "50003\t2026-03-17 09:30:02\tGOOG\t50\t168.23\tPARTIAL\tACCT-7892\n"
            "50004\t2026-03-17 09:30:02\tAMZN\t75\t185.91\tFILLED\tACCT-7893\n"
            "50005\t2026-03-17 09:30:03\tTSLA\t200\t242.58\tFILLED\tACCT-7894\n"
            "50006\t2026-03-17 09:30:03\tNVDA\t150\t892.34\tFILLED\tACCT-7895\n"
            "50007\t2026-03-17 09:30:04\tMETA\t300\t507.12\tREJECTED\tACCT-7896\n"
            "50008\t2026-03-17 09:30:04\tJPM\t500\t198.76\tFILLED\tACCT-7897\n"
            "50009\t2026-03-17 09:30:05\tBAC\t1000\t37.84\tFILLED\tACCT-7898\n"
            "50010\t2026-03-17 09:30:05\tV\t125\t278.93\tFILLED\tACCT-7899\n"
            "[... 47,832 more rows ...]\n\n"
            "The query returns correct results, it's just incredibly slow now. Execution "
            "plan shows a full table scan instead of an index seek.",
            "Query performance on the trades table (SQLPROD03) degraded from 10 seconds to "
            "45 minutes. The execution plan shows a full table scan — the clustered index "
            "on trade_date appears to have been dropped during overnight maintenance. The "
            "sample result set above shows the data is intact.",
        ],
        next_best_actions=[
            "Investigate severe query performance degradation on SQLPROD03 trades table — "
            "likely a missing index on trade_date dropped during maintenance.",
            "Recreate the trade_date index on the trades table and verify the execution plan returns to index seek.",
        ],
        remediation_steps=[
            [
                "Check the index definitions on the trades table to verify the trade_date index exists",
                "If the index was dropped, recreate it with CREATE INDEX on trade_date",
                "Review the maintenance window scripts to identify what caused the index drop",
                "Monitor query execution plans before and after index rebuild to confirm resolution",
            ],
        ],
        tags=["data-cleanup", "query-result-dump", "tabular-data"],
    ),
    # ──────────────────────────────────────────────────────────────────
    # Raw SMTP email headers flood
    # ──────────────────────────────────────────────────────────────────
    Scenario(
        scenario_id="cleanup-raw-smtp-headers",
        category="Software & Applications",
        priority="P3",
        assigned_team="Enterprise Applications",
        needs_escalation=False,
        missing_information=["application_version", "device_info"],
        subjects=[
            "Outlook freezes for 30 seconds when opening external emails",
            "Outlook hangs on external messages since March patch — headers below",
        ],
        descriptions=[
            "Outlook 365 on my Windows 11 laptop freezes for about 30 seconds every time I "
            "open an email from external senders. Internal emails open instantly. I thought "
            "the raw headers might help diagnose — here they are from one of the slow emails:\n\n"
            "Received: from MX01.contoso.com (10.0.1.50) by\n"
            " EX02.contoso.com (10.0.1.51) with Microsoft SMTP Server\n"
            " (version=TLS1_2, cipher=TLS_ECDHE_RSA_WITH_AES_256_GCM_SHA384) id\n"
            " 15.2.1118.40; Mon, 17 Mar 2026 09:15:22 +0000\n"
            "Received: from mail-relay.partner.com (203.0.113.50) by\n"
            " MX01.contoso.com (10.0.1.50) with ESMTPS id ABC123DEF456;\n"
            " Mon, 17 Mar 2026 09:15:20 +0000\n"
            "Authentication-Results: contoso.com; spf=pass\n"
            " smtp.mailfrom=partner.com; dkim=pass (2048-bit key)\n"
            " header.d=partner.com; dmarc=pass action=none\n"
            " header.from=partner.com;\n"
            "X-MS-Exchange-Organization-SCL: 1\n"
            "X-MS-Exchange-Organization-AuthSource: MX01.contoso.com\n"
            "X-MS-Exchange-Organization-AuthAs: Anonymous\n"
            "X-MS-Has-Attach:\n"
            "X-MS-TNEF-Correlator:\n"
            "MIME-Version: 1.0\n"
            "Content-Type: multipart/mixed;\n"
            ' boundary="----=_Part_12345_6789.1710668120"\n'
            "X-Originating-IP: [203.0.113.50]\n"
            "X-MS-Exchange-CrossTenant-AuthAs: Anonymous\n"
            "X-MS-Exchange-CrossTenant-Network-Message-Id:\n"
            " a1b2c3d4-e5f6-7890-abcd-ef1234567890\n"
            "X-MS-Exchange-Transport-CrossTenantHeadersStamped: EX02\n\n"
            "The delay started after the March Outlook patch was pushed. I think something "
            "in the DLP or compliance scanning pipeline is adding latency for external mail.",
            "Every external email I open in Outlook takes 30 seconds before the content "
            "appears. Internal emails are instant. This started after the March patch. "
            "I've pasted the raw SMTP headers from one of the slow emails to help "
            "troubleshoot the delay.",
        ],
        next_best_actions=[
            "Investigate Outlook 365 freeze when opening external emails — likely a DLP or "
            "compliance policy scanning delay introduced with the March patch.",
            "Check Outlook performance logging for the delay source and review DLP "
            "configuration for external mail scanning.",
        ],
        remediation_steps=[
            [
                "Check Outlook performance logging for the delay source when opening external emails",
                "Review DLP and compliance policy configurations for external mail scanning latency",
                "Test with Outlook safe mode to rule out add-in interference",
                "Check if the March patch introduced known Outlook performance regressions",
            ],
        ],
        tags=["data-cleanup", "raw-email-headers", "smtp-headers-dump"],
    ),
    # ──────────────────────────────────────────────────────────────────
    # Very long single paragraph with no line breaks (wall of text)
    # ──────────────────────────────────────────────────────────────────
    Scenario(
        scenario_id="cleanup-wall-of-text-no-breaks",
        category="Network & Connectivity",
        priority="P3",
        assigned_team="Network Operations",
        needs_escalation=False,
        missing_information=["error_message", "device_info"],
        subjects=[
            "VPN certificate expired cannot connect",
            "GlobalProtect certificate error — remote work blocked",
        ],
        descriptions=[
            "Hi IT support I am writing to report an issue with my VPN connection that has "
            "been affecting my ability to work remotely since yesterday morning when I tried "
            "to connect to the corporate network from my home office using the GlobalProtect "
            "VPN client on my Dell Latitude 5540 laptop running Windows 11 Pro version 23H2 "
            "and I received an error message that said something like certificate validation "
            "failed or certificate has expired I am not sure of the exact wording because I "
            "was in a hurry to join a client call but I do remember it mentioned something "
            "about the certificate and I tried clicking retry several times and it did not "
            "work so I tried restarting my laptop and that did not help either and then I "
            "tried connecting through my phone hotspot instead of my home WiFi thinking maybe "
            "it was a network issue but I got the same error on both networks which makes me "
            "think it is definitely a certificate problem and not a network problem and I "
            "asked my colleague Jennifer Park who sits next to me in the office and she said "
            "her VPN is working fine so it might just be my machine and I am supposed to work "
            "from home for the rest of this week because of a plumber appointment on Wednesday "
            "and a dentist on Thursday so I really need this fixed as soon as possible because "
            "I have several important client calls and I cannot access the shared drives or "
            "internal applications without VPN and I also tried uninstalling and reinstalling "
            "the GlobalProtect client but that did not help either and I even tried using the "
            "web portal VPN but that also gave a certificate error and I found an old KB "
            "article that said to check the date and time on my computer which I did and they "
            "are both correct so that is not the issue either please help",
            "my vpn stopped working yesterday it says certificate error or something I need "
            "to connect from home I tried everything restarting reinstalling the client using "
            "different networks nothing works my colleague says hers works fine so its just my "
            "laptop the GlobalProtect client shows a red X and when I hover over it it says "
            "something about certificate not valid or expired I cannot remember the exact "
            "message but it definitely mentions certificate and I need this fixed today "
            "because I am working remotely all week and cannot access anything without the VPN "
            "including email shared drives the internal wiki and our project management tool "
            "and my manager is asking me to join calls that require screen sharing of internal "
            "documents which I cannot do without the VPN connection so this is very urgent for "
            "me even though I know it is probably just a certificate renewal thing but I "
            "cannot do it myself because it requires admin access which I do not have on this "
            "laptop please advise",
        ],
        next_best_actions=[
            "Renew or reissue the expired VPN client certificate on the user's laptop — the "
            "GlobalProtect certificate validation failure prevents remote connectivity.",
            "Check the VPN client certificate expiration and reissue through the certificate "
            "authority. The user needs remote access for the rest of the week.",
        ],
        remediation_steps=[
            [
                "Check the VPN client certificate expiration date on the user's laptop",
                "Reissue a new VPN client certificate through the certificate authority",
                "Install the renewed certificate and verify VPN connectivity",
                "Check if other users have the same certificate batch that may be expiring soon",
            ],
        ],
        tags=["data-cleanup", "no-line-breaks", "wall-of-text"],
    ),
    # ──────────────────────────────────────────────────────────────────
    # Base64 image data flooding
    # ──────────────────────────────────────────────────────────────────
    Scenario(
        scenario_id="cleanup-base64-image-flood",
        category="Hardware & Peripherals",
        priority="P3",
        assigned_team="Endpoint Engineering",
        needs_escalation=False,
        missing_information=["error_message", "device_info"],
        subjects=[
            "Laptop screen flickering — pasting diagnostic screenshots below",
            "Monitor display glitch — see Base64 encoded screenshots attached inline",
        ],
        descriptions=[
            "My Dell Latitude 7430 screen has been flickering intermittently since the last "
            "BIOS update. It happens mostly when switching between external monitor and laptop "
            "display. I captured a few screenshots of the artifacts and converted them so I "
            "could paste them in this ticket:\n\n"
            "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAABAAAAACCAYAAAAv+"
            "MJvAAAACXBIWXMAABYlAAAWJQFJUiTwAAAAGXRFWHRTb2Z0d2FyZQB3d3cu"
            "aW5rc2NhcGUub3Jnm+48GgAAIABJREFUeJzsvXd4XNd17/2bXtB7IQES7L13"
            "iqJIUaIkShZly5Ys27Fjx4kTx0mud5JxnDhOHCeusmXJqqQoiuq9ECTZ0TsG"
            "fWYwM6ff94cGEAdAACRBkpLv+3meBzNnzj5n77PP3mutXwEC/P/svXmcXEV5"
            "9/+tqrtn3yczmclkJZCEBBKSsMoOIquIgOCC4gKKoii44Ia44L6ioKIoKIoI"
            "gogIsu9LCGQlIWQhezL7Pt1d9f5R3dM9k0lCwPd9f++Hzwc6fW/dqrp161Y9"
            "z1rPU0VKKfn/tyV5Y/9k/wT+BP4E/j97e6MF+H/b/9v+3/b/tv+3/YnaGy3A"
            "\n...[truncated 47KB of Base64 data]...\n"
            "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGQAAABkCAYAAABw"
            "4pVUAAAABHNCSVQICAgIfAhkiAAAAAlwSFlzAAALEgAACxIB0t1+/AAAAGXR"
            "FWHRTb2Z0d2FyZQB3d3cuaW5rc2NhcGUub3Jnm+48GgAABdJJREFUeJzt3V"
            "\n...[truncated 31KB of Base64 data]...\n\n"
            "The flickering is random but happens at least 5 times per day. It started after "
            "the BIOS was updated to version 1.18.0 last Thursday.",
            "Screen keeps flickering on my laptop. I took screenshots and encoded them as "
            "Base64 so I could include them directly in this ticket. "
            "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M "
            "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAAC0lEQVQI12NgAA "
            "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAABklEQVQI12NgBQ "
            "The issue is worst when I undock from my external monitor. BIOS 1.18.0.",
        ],
        next_best_actions=[
            "Investigate screen flickering on Dell Latitude 7430 after BIOS update to "
            "1.18.0 — likely a display driver or BIOS regression when switching outputs.",
            "Roll back the BIOS update to the previous version or update the display "
            "driver to resolve the flickering during monitor hot-swap.",
        ],
        remediation_steps=[
            [
                "Verify the current BIOS version and check Dell support for known issues with 1.18.0",
                "Update or roll back the Intel graphics driver to a compatible version",
                "Test with the external monitor disconnected to isolate the trigger",
                "If flickering persists, roll back the BIOS to the previous stable version",
            ],
        ],
        tags=["data-cleanup", "base64-image-flood"],
    ),
    # ──────────────────────────────────────────────────────────────────
    # Auto-reply / OOO chain
    # ──────────────────────────────────────────────────────────────────
    Scenario(
        scenario_id="cleanup-auto-reply-chain",
        category="Software & Applications",
        priority="P2",
        assigned_team="Enterprise Applications",
        needs_escalation=False,
        missing_information=["error_message", "affected_users"],
        subjects=[
            "RE: Automatic reply: RE: Automatic reply: RE: Out of Office: SAP login broken",
            "RE: OOO: RE: Automatic reply: RE: Out of Office: Cannot access SAP portal",
        ],
        descriptions=[
            "--- Automatic Reply ---\nI am currently out of the office with no access to "
            "email. I will return on March 24th. For urgent matters contact Jim at "
            "jim@contoso.com.\n\n"
            "--- Automatic Reply ---\nThank you for your message. I am out of the office "
            "until March 28th. For immediate assistance, please contact the Help Desk.\n\n"
            "--- Automatic Reply ---\nI will be out of the office from March 20-27. For "
            "urgent issues please reach out to my backup Sarah Chen.\n\n"
            "--- Original Message from user ---\n"
            "The SAP Fiori portal returns HTTP 403 Forbidden when I try to log in. I can "
            "reach the login page but after entering my credentials I get bounced to an "
            "error page. This started this morning. I need access to submit purchase orders "
            "before end of day.",
            "Out of Office: I am away from the office.\n"
            "Out of Office: Thanks for your email, I'm OOO.\n"
            "Out of Office: Away until next Monday.\n"
            "Auto-Reply: I'm traveling with limited access.\n"
            "Auto-Reply: On PTO this week, back 3/28.\n\n"
            "Original issue: SAP Fiori gives 403 Forbidden after login. Need to submit POs "
            "urgently. Was working yesterday, broken today for my account only.",
        ],
        next_best_actions=[
            "Investigate SAP Fiori 403 Forbidden error after authentication — likely a "
            "role assignment or authorization object issue specific to this user's account.",
            "Check the user's SAP role assignments and authorization profiles to resolve "
            "the 403 error blocking purchase order submission.",
        ],
        remediation_steps=[
            [
                "Verify the user's SAP role assignments and authorization objects in SU01",
                "Check SAP system logs (SM21) for authorization failures tied to the user",
                "Reassign missing roles or reset the user's authorization buffer with SU56",
                "Confirm the user can access the Fiori portal and submit purchase orders",
            ],
        ],
        tags=["data-cleanup", "auto-reply-chain"],
    ),
    # ──────────────────────────────────────────────────────────────────
    # 4-language legal disclaimer
    # ──────────────────────────────────────────────────────────────────
    Scenario(
        scenario_id="cleanup-legal-disclaimer-multilingual",
        category="Security & Compliance",
        priority="P2",
        assigned_team="Security Operations",
        needs_escalation=False,
        missing_information=["affected_system", "timestamp"],
        subjects=[
            "DLP alert triggered on outbound email — false positive?",
            "Data Loss Prevention policy blocking legitimate email with contract attachment",
        ],
        descriptions=[
            "I'm getting DLP policy violations when sending contracts to our legal partner. "
            "The email keeps getting quarantined. Here's the full email with disclaimers:\n\n"
            "CONFIDENTIALITY NOTICE: This email and any attachments are for the exclusive "
            "and confidential use of the intended recipient. If you are not the intended "
            "recipient, please do not read, distribute, or take action based on this message. "
            "If you have received this message in error, please notify the sender immediately "
            "and delete this message from your system.\n\n"
            "AVIS DE CONFIDENTIALITÉ: Ce courriel et toute pièce jointe sont destinés "
            "exclusivement au destinataire prévu et sont confidentiels. Si vous n'êtes pas "
            "le destinataire prévu, veuillez ne pas lire, distribuer ou agir sur la base de "
            "ce message. Si vous avez reçu ce message par erreur, veuillez en informer "
            "immédiatement l'expéditeur et supprimer ce message de votre système.\n\n"
            "VERTRAULICHKEITSHINWEIS: Diese E-Mail und alle Anhänge sind ausschließlich für "
            "den vorgesehenen Empfänger bestimmt und vertraulich. Wenn Sie nicht der "
            "vorgesehene Empfänger sind, lesen, verteilen oder handeln Sie bitte nicht auf "
            "der Grundlage dieser Nachricht. Wenn Sie diese Nachricht irrtümlich erhalten "
            "haben, benachrichtigen Sie bitte umgehend den Absender und löschen Sie diese "
            "Nachricht aus Ihrem System.\n\n"
            "AVISO DE CONFIDENCIALIDAD: Este correo electrónico y cualquier archivo adjunto "
            "son para uso exclusivo y confidencial del destinatario previsto. Si usted no es "
            "el destinatario previsto, por favor no lea, distribuya ni actúe en base a este "
            "mensaje. Si ha recibido este mensaje por error, notifique inmediatamente al "
            "remitente y elimine este mensaje de su sistema.\n\n"
            "The actual issue: DLP policy is flagging the keyword 'confidential' in the "
            "disclaimer footer as a policy match and quarantining all my outbound email to "
            "external legal counsel.",
            "Our DLP system quarantines every email I send to outside counsel because it "
            "picks up the word 'confidential' from the four-language disclaimer block that "
            "Legal requires on all outbound correspondence. The disclaimer is in English, "
            "French, German, and Spanish. This has been blocking my work for two days. "
            "The DLP rule seems to match on keywords in the disclaimer, not just the body.",
        ],
        next_best_actions=[
            "Adjust the DLP policy to exclude standard legal disclaimer blocks from "
            "keyword matching — the rule is triggering on boilerplate confidentiality text.",
            "Create a DLP policy exception for the corporate legal disclaimer template "
            "to stop false-positive quarantining of outbound legal correspondence.",
        ],
        remediation_steps=[
            [
                "Review the DLP policy rule that is triggering on the disclaimer keywords",
                "Add an exception for the corporate legal disclaimer template text",
                "Release the quarantined emails that were false positives",
                "Test by sending an email with the disclaimer to verify the exception works",
                "Document the DLP exception in the security policy change log",
            ],
        ],
        tags=["data-cleanup", "legal-disclaimer"],
    ),
    # ──────────────────────────────────────────────────────────────────
    # Teams chat transcript paste
    # ──────────────────────────────────────────────────────────────────
    Scenario(
        scenario_id="cleanup-teams-chat-paste",
        category="Software & Applications",
        priority="P3",
        assigned_team="Enterprise Applications",
        needs_escalation=False,
        missing_information=["error_message", "application_version"],
        subjects=[
            "SharePoint sync failing — pasting Teams chat with our team discussion",
            "OneDrive SharePoint sync broken — Teams troubleshooting thread below",
        ],
        descriptions=[
            "[3/15 9:02 AM] Mike Chen: Hey has anyone else's SharePoint sync stopped working?\n"
            "[3/15 9:03 AM] Sarah Jones: mine's fine\n"
            "[3/15 9:03 AM] Mike Chen: weird, mine just shows a red X on the OneDrive icon\n"
            "[3/15 9:04 AM] Dave Wilson: @Mike same here actually, started this morning\n"
            "[3/15 9:04 AM] Sarah Jones: oh wait I'm not syncing the Marketing folder\n"
            "[3/15 9:05 AM] Mike Chen: it's specifically the Q1 Reports library\n"
            "[3/15 9:05 AM] Dave Wilson: yeah same library for me too\n"
            "[3/15 9:06 AM] Lisa Park: I just tried, also broken for Q1 Reports\n"
            "[3/15 9:07 AM] Mike Chen: @Lisa can you check if Projects library works?\n"
            "[3/15 9:07 AM] Lisa Park: Projects syncs fine, just Q1 Reports is broken\n"
            "[3/15 9:08 AM] Dave Wilson: should we open a ticket?\n"
            "[3/15 9:08 AM] Mike Chen: yeah I'll do it, let me paste this chat\n"
            "[3/15 9:09 AM] Sarah Jones: lol just paste the whole thing 😂\n"
            "[3/15 9:09 AM] Mike Chen: 👍\n\n"
            "So basically the Q1 Reports SharePoint library won't sync through OneDrive. "
            "Multiple people affected. Projects library syncs fine. Started this morning.",
            "[Teams Chat - Marketing Team]\n"
            "Mike: SharePoint sync broken for anyone else?\n"
            "Dave: yes Q1 Reports library\n"
            "Lisa: same\n"
            "Mike: Projects lib works tho\n"
            "Dave: just Q1 Reports\n"
            "Mike: opening ticket now\n\n"
            "OneDrive sync to SharePoint Q1 Reports library is failing for at least 3 "
            "users on the Marketing team since this morning. Red X on the OneDrive tray "
            "icon. Other libraries sync normally.",
        ],
        next_best_actions=[
            "Investigate OneDrive sync failure for the Q1 Reports SharePoint library — "
            "multiple users affected, other libraries sync normally, suggesting a "
            "library-level issue.",
            "Check the Q1 Reports SharePoint library for sync-blocking conditions such "
            "as file path length limits, checked-out files, or permission changes.",
        ],
        remediation_steps=[
            [
                "Check the Q1 Reports SharePoint library for sync-blocking conditions",
                "Review OneDrive sync client logs for specific error codes",
                "Verify no recent permission changes were made to the library",
                "Reset the OneDrive sync relationship for the affected library and re-sync",
            ],
        ],
        tags=["data-cleanup", "teams-transcript"],
    ),
    # ──────────────────────────────────────────────────────────────────
    # HTTP 500 response dump
    # ──────────────────────────────────────────────────────────────────
    Scenario(
        scenario_id="cleanup-http-response-dump",
        category="Software & Applications",
        priority="P2",
        assigned_team="Enterprise Applications",
        needs_escalation=False,
        missing_information=["steps_to_reproduce", "environment_details"],
        subjects=[
            "Internal portal returning 500 error — full response dump below",
            "HR self-service portal crashes — HTTP 500 with stack trace",
        ],
        descriptions=[
            "The HR self-service portal started returning 500 errors this morning when "
            "I try to submit my timesheet. Here's the full HTTP response I captured from "
            "the browser dev tools:\n\n"
            "HTTP/1.1 500 Internal Server Error\n"
            "Server: Microsoft-IIS/10.0\n"
            "X-Powered-By: ASP.NET\n"
            "X-AspNet-Version: 4.0.30319\n"
            "Content-Type: text/html; charset=utf-8\n"
            "Content-Length: 8734\n"
            "Date: Mon, 17 Mar 2026 14:22:05 GMT\n"
            "Connection: keep-alive\n"
            "X-Frame-Options: SAMEORIGIN\n"
            "X-Content-Type-Options: nosniff\n"
            "Strict-Transport-Security: max-age=31536000; includeSubDomains\n"
            "Cache-Control: no-cache, no-store, must-revalidate\n"
            "Pragma: no-cache\n\n"
            "<!DOCTYPE html><html><head><title>Runtime Error</title><style>body{font-family:"
            "Arial;margin:50px}h2{color:#cc0000}</style></head><body><h2>Server Error in "
            "'/' Application</h2><hr><p><b>Runtime Error</b></p><p>Description: An "
            "exception occurred while processing your request.</p><p>Exception Details: "
            "System.Data.SqlClient.SqlException: Timeout expired. The timeout period "
            "elapsed prior to completion of the operation.</p><p><b>Stack Trace:</b></p>"
            "<pre>   at System.Data.SqlClient.SqlConnection.OnError(SqlException exception)"
            "\n   at System.Data.SqlClient.SqlInternalConnection.OnError(SqlException "
            "exception)\n   at HRPortal.Services.TimesheetService.SubmitTimesheet(Int32 "
            "employeeId, DateTime weekEnding)\n   at HRPortal.Controllers."
            "TimesheetController.Submit(TimesheetModel model)</pre></body></html>\n\n"
            "I need to submit my timesheet by end of day.",
            "Getting 500 Internal Server Error on the HR portal when submitting timesheets. "
            "The response body shows a SQL timeout in TimesheetService.SubmitTimesheet. "
            "Full HTTP headers and HTML error page are in the response. Multiple users "
            "are reporting the same issue since 2 PM today.",
        ],
        next_best_actions=[
            "Investigate SQL timeout in the HR portal's TimesheetService — the database "
            "query for timesheet submission is exceeding the connection timeout.",
            "Check the HR portal's SQL Server database for blocking queries or resource "
            "contention causing the timesheet submission timeout.",
        ],
        remediation_steps=[
            [
                "Check SQL Server for blocking sessions or long-running queries on the timesheet tables",
                "Review the TimesheetService.SubmitTimesheet stored procedure for performance issues",
                "Increase the SQL connection timeout as a temporary fix if the query is legitimate",
                "Verify the database server has adequate resources (CPU, memory, disk I/O)",
                "Confirm timesheet submission works after resolving the database contention",
            ],
        ],
        tags=["data-cleanup", "http-dump"],
    ),
    # ──────────────────────────────────────────────────────────────────
    # HTML data URI screenshots flood
    # ──────────────────────────────────────────────────────────────────
    Scenario(
        scenario_id="cleanup-data-uri-screenshots",
        category="Software & Applications",
        priority="P3",
        assigned_team="Enterprise Applications",
        needs_escalation=False,
        missing_information=["application_version", "device_info"],
        subjects=[
            "Excel add-in crashes — embedded screenshot evidence in data URIs",
            "Excel Power Query add-in freezing — inline data URI images showing the error",
        ],
        descriptions=[
            "Our Power Query add-in for Excel keeps crashing when refreshing data from "
            "the Azure SQL source. I took screenshots and embedded them as data URIs so "
            "you can see exactly what happens:\n\n"
            '<img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAfQAAAH0CAYAAAD'
            "L1t+KAAAABGdBTUEAALGPC/xhBQAAACBjSFJNAAB6JgAAgIQAAPoAAACA6AAAdTAA"
            "AOpgAAA6mAAAF3CculE8AAAABmJLR0QA/wD/AP+gvaeTAABAAElEQVR42u3deXxU1"
            "fn48c+5M5OFJBASwr4T9n0RBBQXFNe6V6u11qV1q7XW2mr9tta2Wm2r1tpaW5da6l"
            "K1WqtWRRBFRUABAdl32SEQlpB97vn9cSchIQECJGQwn/frlTczd+7ce+69w3nOec"
            '65V4EA" width="800" />\n\n'
            "Error dialog screenshot:\n"
            '<img src="data:image/jpeg;base64,/9j/4AAQSkZJRgABAQEASABIAAD/2wBDAAMCA'
            "gMCAgMDAwMEAwMEBQgFBQQEBQoHBwYIDAoMCwsKCwsKDA0QDQYJDQ4OEg8QERETFh"
            "wSFBYcFhccHR0dHBwgICAgICAiIiIkJCQgICAgICIiIiQkJCQiIiIiIiIiIiIiJCQ"
            'kJCQiIiIiJA==" width="400" />\n\n'
            "The crash happens every time on the Refresh All button. Excel version is "
            "Microsoft 365 Apps, build 16.0.17928. The data source is our Azure SQL "
            "reporting database.",
            "Power Query add-in crashes in Excel during data refresh. Screenshots embedded "
            "as <img src='data:image/png;base64,...'> tags showing the error dialog. The "
            "add-in worked fine last week, started failing after the Monday Office update.",
        ],
        next_best_actions=[
            "Investigate Power Query add-in crash during data refresh in Excel — likely "
            "an incompatibility with the latest Microsoft 365 Apps update.",
            "Check for known issues with the current Office build and Power Query, and "
            "test rolling back the recent Office update.",
        ],
        remediation_steps=[
            [
                "Check Microsoft 365 known issues for the current build and Power Query compatibility",
                "Test the data refresh with Power Query in a clean Excel session without other add-ins",
                "Roll back the recent Office update to the previous build if the issue is confirmed",
                "Report the bug to Microsoft if it's a regression in the latest build",
            ],
        ],
        tags=["data-cleanup", "data-uri-flood"],
    ),
    # ──────────────────────────────────────────────────────────────────
    # Multiple INC ticket number references
    # ──────────────────────────────────────────────────────────────────
    Scenario(
        scenario_id="cleanup-multi-ticket-reference",
        category="Network & Connectivity",
        priority="P2",
        assigned_team="Network Operations",
        needs_escalation=False,
        missing_information=["previous_ticket_id", "network_location"],
        subjects=[
            "RECURRING: Site-to-site VPN flapping — see INC0012345, INC0012890, INC0013401, INC0014002",
            "VPN tunnel instability — refs: INC0012345 INC0012890 INC0013401 INC0014002 INC0014500",
        ],
        descriptions=[
            "The site-to-site VPN tunnel between our Chicago office and the Atlanta data "
            "center has been flapping intermittently for the past 3 weeks. We have opened "
            "multiple tickets and I want to consolidate them here:\n\n"
            "INC0012345 — Opened 2/28: VPN tunnel down for 2 hours, came back on its own.\n"
            "INC0012890 — Opened 3/3: Tunnel flapped 4 times in one day, closed as "
            "'resolved' but it happened again.\n"
            "INC0013401 — Opened 3/7: Network team replaced the VPN concentrator PSU, "
            "issue persisted.\n"
            "INC0014002 — Opened 3/10: Tunnel stability improved for 2 days then started "
            "flapping again.\n"
            "INC0014500 — Opened 3/14: Current ticket, still ongoing.\n\n"
            "Pattern: the tunnel drops every 6-8 hours, stays down for 5-15 minutes, then "
            "re-establishes. DPD (Dead Peer Detection) logs show the remote end stops "
            "responding. The Atlanta firewall was rebooted in INC0013401 with no improvement. "
            "We suspect an ISP issue or a MTU/fragmentation problem on the circuit.",
            "VPN between Chicago and Atlanta keeps dropping — this is the 5th ticket. "
            "See INC0012345, INC0012890, INC0013401, INC0014002 for history. Tunnel "
            "flaps every 6-8 hours. Previous fixes attempted: PSU replacement, firewall "
            "reboot, IKE rekey timer adjustment. None resolved it. Suspect ISP or MTU issue.",
        ],
        next_best_actions=[
            "Escalate the recurring Chicago–Atlanta VPN tunnel flapping to the ISP for "
            "circuit-level investigation — internal troubleshooting across 5 tickets has "
            "not resolved the issue.",
            "Perform MTU path discovery between the Chicago and Atlanta endpoints and "
            "engage the ISP to check for packet loss or jitter on the WAN circuit.",
        ],
        remediation_steps=[
            [
                "Run MTU path discovery between Chicago and Atlanta VPN endpoints",
                "Capture packet traces during the next flap event to identify the failure point",
                "Engage the ISP to run circuit diagnostics for packet loss and jitter",
                "If ISP confirms circuit issues, request a circuit migration or failover path",
            ],
        ],
        tags=["data-cleanup", "multi-ticket-reference"],
    ),
    # ──────────────────────────────────────────────────────────────────
    # ITSM servicedesk notification template noise
    # ──────────────────────────────────────────────────────────────────
    Scenario(
        scenario_id="cleanup-servicedesk-notification",
        category="Hardware & Peripherals",
        priority="P3",
        assigned_team="Endpoint Engineering",
        needs_escalation=False,
        missing_information=["device_info", "error_message"],
        subjects=[
            "[ServiceDesk Plus] [Auto-Generated] Request #SR-48291 — Keyboard not working",
            "[ITSM Notification] Ticket SR-48291 created — Peripheral device failure",
        ],
        descriptions=[
            "──────────────────────────────────────\n"
            "THIS IS AN AUTO-GENERATED NOTIFICATION\n"
            "──────────────────────────────────────\n"
            "ServiceDesk Plus — Request Notification\n"
            "Request ID: SR-48291\n"
            "Category: Hardware\n"
            "Sub-Category: Peripheral\n"
            "Item: Keyboard\n"
            "Status: Open\n"
            "Created: 2026-03-17 10:45:22 UTC\n"
            "Requester: Pat Morgan (pat.morgan@contoso.com)\n"
            "Requester Department: Finance\n"
            "Requester Location: Building 3, Floor 2, Desk 47\n"
            "Technician: Unassigned\n"
            "Priority: Medium\n"
            "Impact: Affects User\n"
            "Urgency: Medium\n"
            "SLA: 8 Business Hours\n"
            "Due By: 2026-03-18 10:45:22 UTC\n"
            "──────────────────────────────────────\n"
            "DESCRIPTION:\n"
            "My wireless keyboard stopped responding this morning. I've tried replacing "
            "the batteries and reconnecting the USB receiver but it still won't type. "
            "The Num Lock light doesn't come on either.\n"
            "──────────────────────────────────────\n"
            "Please do not reply to this email. Log in to ServiceDesk Plus to update.\n"
            "© 2026 IT Service Management — Contoso Corp\n"
            "──────────────────────────────────────\n",
            "[Auto Notification] Ticket SR-48291. Category: Hardware > Peripheral > "
            "Keyboard. Priority: Medium. SLA: 8h. Requester: Pat Morgan, Finance, "
            "Bldg 3 Fl 2. Description: Wireless keyboard unresponsive after battery "
            "change and receiver re-pair. Num Lock LED does not illuminate. Please "
            "do not reply — update via portal. © 2026 Contoso IT.",
        ],
        next_best_actions=[
            "Replace the wireless keyboard or USB receiver for the user — standard "
            "troubleshooting (battery swap, receiver re-pair) has already been attempted.",
            "Dispatch a replacement wireless keyboard to the user's desk and collect "
            "the defective unit for asset disposal.",
        ],
        remediation_steps=[
            [
                "Verify the USB receiver is recognized by the OS in Device Manager",
                "Test with a known-good keyboard to confirm the issue is the peripheral",
                "If the keyboard is confirmed defective, issue a replacement from inventory",
                "Update the asset record in the CMDB for the swapped keyboard",
            ],
        ],
        tags=["data-cleanup", "servicedesk-template"],
    ),
    # ──────────────────────────────────────────────────────────────────
    # Mojibake / encoding corruption
    # ──────────────────────────────────────────────────────────────────
    Scenario(
        scenario_id="cleanup-mojibake-encoding",
        category="Software & Applications",
        priority="P3",
        assigned_team="Enterprise Applications",
        needs_escalation=False,
        missing_information=["application_version", "environment_details"],
        subjects=[
            "CRM displaying garbled characters — Ã©, Ã¼, â€™ everywhere",
            "Customer names corrupted in CRM — encoding issue since migration",
        ],
        descriptions=[
            "Since the CRM database migration last weekend, all customer records with "
            "non-ASCII characters are displaying garbled text. Examples:\n\n"
            "José García → José García\n"
            "François Müller → FranÃ§ois MÃ¼ller\n"
            "Søren Østergaard → SÃ¸ren Ãstergaard\n"
            "日本語テスト → æ¥æ¬èªãã¹ã\n"
            "Ñoño → ÃoÃ±o\n"
            "café → cafÃ©\n"
            "naïve → naÃ¯ve\n"
            "résumé → rÃ©sumÃ©\n\n"
            "It looks like the data was UTF-8 encoded but the new database connection "
            "is reading it as Latin-1/ISO-8859-1. This affects approximately 15,000 "
            "customer records. Reports and email templates are also showing the garbled "
            "text because they pull from the same fields.",
            "CRM has encoding corruption after the weekend migration. Accented characters "
            "show as mojibake (Ã©, Ã¼, Ã§, etc.). Looks like a UTF-8 vs Latin-1 mismatch. "
            "All records with diacritics are affected — about 15K records. Need this fixed "
            "before the Monday mail merge goes out.",
        ],
        next_best_actions=[
            "Fix the character encoding mismatch in the CRM database connection — the "
            "data is UTF-8 but is being read as Latin-1, causing mojibake on all "
            "non-ASCII characters.",
            "Update the CRM database connection string to specify UTF-8 encoding and "
            "run a data repair script on the 15K affected customer records.",
        ],
        remediation_steps=[
            [
                "Verify the database character set and collation settings post-migration",
                "Update the CRM application connection string to specify UTF-8 encoding",
                "Run a data repair script to convert the double-encoded records back to proper UTF-8",
                "Validate a sample of corrected records across different character sets",
                "Schedule the Monday mail merge only after encoding is confirmed fixed",
            ],
        ],
        tags=["data-cleanup", "mojibake-corruption"],
    ),
    # ──────────────────────────────────────────────────────────────────
    # SOAP fault XML dump
    # ──────────────────────────────────────────────────────────────────
    Scenario(
        scenario_id="cleanup-soap-xml-fault",
        category="Software & Applications",
        priority="P2",
        assigned_team="Enterprise Applications",
        needs_escalation=False,
        missing_information=["steps_to_reproduce", "configuration_details"],
        subjects=[
            "Payroll integration failing — SOAP fault response from ADP endpoint",
            "ADP payroll sync broken — XML fault dump from the web service call",
        ],
        descriptions=[
            "The nightly payroll sync to ADP failed last night and returned a SOAP fault. "
            "Here's the full XML response from the integration server logs:\n\n"
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            '<soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">\n'
            "  <soap:Body>\n"
            "    <soap:Fault>\n"
            "      <faultcode>soap:Server</faultcode>\n"
            "      <faultstring>Authentication token expired. Please request a new "
            "security token from the STS endpoint.</faultstring>\n"
            "      <detail>\n"
            '        <ErrorResponse xmlns="http://api.adp.com/errors/v1">\n'
            "          <ErrorCode>AUTH-4012</ErrorCode>\n"
            "          <ErrorMessage>The SAML assertion has expired. Token lifetime: "
            "3600 seconds. Token age: 86427 seconds.</ErrorMessage>\n"
            "          <RequestId>a7b3c9d1-e4f5-6789-abcd-0123456789ab</RequestId>\n"
            "          <Timestamp>2026-03-17T02:15:33.445Z</Timestamp>\n"
            "          <ServerNode>adp-api-prod-east-07</ServerNode>\n"
            "        </ErrorResponse>\n"
            "      </detail>\n"
            "    </soap:Fault>\n"
            "  </soap:Body>\n"
            "</soap:Envelope>\n\n"
            "Payroll data for 2,400 employees did not sync. We need this resolved before "
            "the Wednesday payroll processing deadline.",
            "ADP payroll integration returned SOAP fault AUTH-4012 — expired SAML token. "
            "The token was 86K seconds old vs 3600 second lifetime. Nightly sync job failed "
            "at 2:15 AM. 2,400 employee records not synced. Wednesday payroll deadline at risk.",
        ],
        next_best_actions=[
            "Renew the SAML authentication token for the ADP payroll integration and "
            "re-run the nightly sync — the token expired because the refresh job did "
            "not execute.",
            "Investigate why the SAML token refresh job failed and manually trigger a "
            "new token request to the STS endpoint to unblock the payroll sync.",
        ],
        remediation_steps=[
            [
                "Request a new SAML security token from the STS endpoint for the ADP integration",
                "Re-run the nightly payroll sync job and verify 2,400 records are transmitted",
                "Investigate why the automatic token refresh job did not run on schedule",
                "Add monitoring and alerting for SAML token expiration on the integration server",
            ],
        ],
        tags=["data-cleanup", "soap-fault-dump"],
    ),
    # ──────────────────────────────────────────────────────────────────
    # HTML table / CSS dump noise
    # ──────────────────────────────────────────────────────────────────
    Scenario(
        scenario_id="cleanup-html-table-noise",
        category="Hardware & Peripherals",
        priority="P4",
        assigned_team="Endpoint Engineering",
        needs_escalation=False,
        missing_information=["device_info", "screenshot_or_attachment"],
        subjects=[
            "Printer inventory report not rendering — raw HTML table below",
            "Printer fleet status page broken — showing HTML source instead of report",
        ],
        descriptions=[
            "The printer inventory dashboard is showing raw HTML instead of the rendered "
            "report. I copied what I see on the page:\n\n"
            '<table style="border-collapse:collapse;width:100%;font-family:Arial,sans-serif'
            ';font-size:12px">\n'
            '<thead><tr style="background-color:#4472C4;color:#FFFFFF;font-weight:bold">\n'
            '<th style="padding:8px;border:1px solid #ddd">Asset Tag</th>\n'
            '<th style="padding:8px;border:1px solid #ddd">Model</th>\n'
            '<th style="padding:8px;border:1px solid #ddd">Location</th>\n'
            '<th style="padding:8px;border:1px solid #ddd">Status</th>\n'
            '<th style="padding:8px;border:1px solid #ddd">Toner Level</th>\n'
            "</tr></thead>\n"
            "<tbody>\n"
            '<tr style="background-color:#D9E2F3"><td style="padding:8px;border:1px solid '
            '#ddd">PRN-0401</td><td>HP LaserJet Pro M404dn</td><td>Bldg 1, Fl 3</td>'
            '<td style="color:green">Online</td><td>72%</td></tr>\n'
            '<tr><td style="padding:8px;border:1px solid #ddd">PRN-0402</td><td>HP Color '
            "LaserJet M553</td><td>Bldg 1, Fl 3</td>"
            '<td style="color:red">Offline</td><td>15%</td></tr>\n'
            '<tr style="background-color:#D9E2F3"><td style="padding:8px;border:1px solid '
            '#ddd">PRN-0403</td><td>Xerox VersaLink C405</td><td>Bldg 2, Fl 1</td>'
            '<td style="color:orange">Error</td><td>45%</td></tr>\n'
            "</tbody></table>\n\n"
            "The actual issue: PRN-0402 on Building 1 Floor 3 has been offline for two "
            "days and needs a toner replacement (15%). Also the dashboard itself is broken.",
            "Printer fleet dashboard rendering as raw HTML/CSS. Aside from the display bug, "
            "printer PRN-0402 (HP Color LaserJet M553, Bldg 1 Fl 3) is offline and low on "
            "toner at 15%. Needs toner replacement and investigation into why it went offline.",
        ],
        next_best_actions=[
            "Replace toner on printer PRN-0402 (HP Color LaserJet M553, Building 1 "
            "Floor 3) and investigate the offline status — separately report the "
            "dashboard rendering bug to the web team.",
            "Dispatch a toner cartridge for PRN-0402 and restart the print spooler "
            "service. File a separate bug for the printer dashboard HTML rendering issue.",
        ],
        remediation_steps=[
            [
                "Replace the toner cartridge on PRN-0402 and verify print quality",
                "Restart the print spooler service on PRN-0402 to bring it back online",
                "Verify the printer is online and accepting jobs from the print server",
                "Report the dashboard HTML rendering bug to the web application team as a separate issue",
            ],
        ],
        tags=["data-cleanup", "html-table-noise"],
    ),
    # ──────────────────────────────────────────────────────────────────
    # Extremely verbose email with issue buried deep
    # ──────────────────────────────────────────────────────────────────
    Scenario(
        scenario_id="cleanup-buried-issue-verbose",
        category="Network & Connectivity",
        priority="P3",
        assigned_team="Network Operations",
        needs_escalation=False,
        missing_information=["network_location", "error_message"],
        subjects=[
            "Wi-Fi issues in conference room (long explanation sorry)",
            "Wireless connectivity problems — detailed background and context provided",
        ],
        descriptions=[
            "Hi IT team, I hope you're all doing well and having a good week so far. I "
            "wanted to reach out about something that's been bothering me for a while now "
            "and I apologize in advance for the length of this email but I want to make "
            "sure I give you all the context you need. So basically I've been working here "
            "at Contoso for about 3 years now and for the most part the IT infrastructure "
            "has been really solid and I always tell people how great the network is compared "
            "to my last company where we had constant outages. Anyway, last year when we "
            "renovated the 4th floor and moved our team from Building A to Building B "
            "everything was great for the first few months. The new office layout is really "
            "nice and the standing desks are fantastic by the way, great choice on those. "
            "But I started noticing something around November or December, it's hard to "
            "remember exactly when. The Wi-Fi in conference room B4-302 — that's the large "
            "one at the end of the hallway near the kitchen — seems to drop connections when "
            "there are more than about 8 people in the room. I first noticed it during our "
            "quarterly planning meeting when half the team lost their connection at the same "
            "time. I thought it was a fluke but then it happened again during the December "
            "all-hands and then again in January during the budget review. My colleague Tom "
            "from accounting mentioned he had the same issue during his team's meetings in "
            "that room. So it seems like it's specifically room B4-302 and it's specifically "
            "when there are a lot of people. Small meetings of 3-4 people seem fine. I asked "
            "around and a few other people confirmed the same pattern. Oh and I should "
            "mention that the Wi-Fi in the adjacent rooms B4-301 and B4-303 seems fine even "
            "during large meetings, so it's really just that one room. I hope that helps "
            "narrow it down. Let me know if you need any more information and thanks again "
            "for all you do!",
            "Long story short: conference room B4-302 in Building B, 4th floor, drops "
            "Wi-Fi connections when more than ~8 people are in the room. Adjacent rooms "
            "B4-301 and B4-303 are fine. Happening since November. Multiple people have "
            "confirmed. Small meetings work OK. Appreciate any help!",
        ],
        next_best_actions=[
            "Investigate the wireless access point serving conference room B4-302 — it "
            "cannot handle more than 8 concurrent clients, suggesting an AP capacity or "
            "channel congestion issue.",
            "Survey the RF environment in B4-302 and check the AP client association "
            "limits and channel utilization during a large meeting.",
        ],
        remediation_steps=[
            [
                "Check the AP serving B4-302 for client association limits and firmware version",
                "Perform an RF site survey in B4-302 during a large meeting to measure signal and interference",
                "Upgrade or add a second AP in B4-302 if the current one cannot handle the client density",
                "Verify the fix during the next large meeting in B4-302",
            ],
        ],
        tags=["data-cleanup", "extremely-verbose-buried"],
    ),
    # ──────────────────────────────────────────────────────────────────
    # Nested email / embedded EML MIME structure
    # ──────────────────────────────────────────────────────────────────
    Scenario(
        scenario_id="cleanup-embedded-eml",
        category="Software & Applications",
        priority="P3",
        assigned_team="Enterprise Applications",
        needs_escalation=False,
        missing_information=["error_message", "application_version"],
        subjects=[
            "FW: FW: Attached message — Outlook cannot open .eml attachments",
            "Email with embedded .eml attachment won't open — MIME parsing error",
        ],
        descriptions=[
            "I received an email that has another email attached as a .eml file, and that "
            "attached email itself contains another .eml attachment. When I try to open the "
            "nested attachment, Outlook shows an error. Here's what the raw source looks "
            "like:\n\n"
            "Content-Type: multipart/mixed;\n"
            ' boundary="----=_Part_OUTER_001"\n\n'
            "------=_Part_OUTER_001\n"
            "Content-Type: text/plain; charset=UTF-8\n\n"
            "Please see the attached forwarded email chain.\n\n"
            "------=_Part_OUTER_001\n"
            "Content-Type: message/rfc822\n"
            'Content-Disposition: attachment; filename="original_request.eml"\n\n'
            "From: vendor@partner.com\n"
            "To: procurement@contoso.com\n"
            "Subject: RE: Purchase Order 4501\n"
            "Content-Type: multipart/mixed;\n"
            ' boundary="----=_Part_INNER_002"\n\n'
            "------=_Part_INNER_002\n"
            "Content-Type: text/plain; charset=UTF-8\n\n"
            "Attached is the signed PO for your records.\n\n"
            "------=_Part_INNER_002\n"
            'Content-Type: application/pdf; name="PO_4501_signed.pdf"\n'
            "Content-Transfer-Encoding: base64\n"
            'Content-Disposition: attachment; filename="PO_4501_signed.pdf"\n\n'
            "JVBERi0xLjQKJeLjz9MKMSAwIG9iago8PAovVHlwZSAvQ2F0YWxvZwo+PgplbmRv\n"
            "YmoKMiAwIG9iago8PAovVHlwZSAvUGFnZXMKL0tpZHMgWzMgMCBSXQo+PgplbmRv\n"
            "...[truncated]...\n\n"
            "------=_Part_INNER_002--\n"
            "------=_Part_OUTER_001--\n\n"
            "I need to access PO_4501_signed.pdf from the nested attachment. Outlook gives "
            "a generic 'Cannot open this item' error when I double-click the inner .eml.",
            "Outlook can't open a nested .eml attachment — an email attached inside another "
            "email. The inner attachment contains a signed PDF (PO 4501) that procurement "
            "needs. Getting 'Cannot open this item' error. The MIME structure has nested "
            "multipart boundaries that Outlook seems unable to parse.",
        ],
        next_best_actions=[
            "Extract the nested PO_4501_signed.pdf from the embedded .eml attachment "
            "using an alternative mail client or MIME parsing tool.",
            "Save the outer .eml to disk, open it with a MIME-aware tool, and extract "
            "the PDF attachment from the inner message.",
        ],
        remediation_steps=[
            [
                "Save the outer email as an .eml file to the desktop",
                "Open the .eml in a MIME parsing tool or alternative client to access the nested message",
                "Extract the PO_4501_signed.pdf from the inner attachment",
                "Check if Outlook has a known bug with deeply nested MIME structures and apply updates",
            ],
        ],
        tags=["data-cleanup", "embedded-eml"],
    ),
    # ──────────────────────────────────────────────────────────────────
    # OCR scan artifacts and recognition errors
    # ──────────────────────────────────────────────────────────────────
    Scenario(
        scenario_id="cleanup-ocr-scan-artifacts",
        category="Data & Storage",
        priority="P3",
        assigned_team="Data Platform",
        needs_escalation=False,
        missing_information=["affected_system", "configuration_details"],
        subjects=[
            "OCR data import has garbled text — scanned invoices corrupted",
            "Invoice data pipeline ingesting OCR garbage — recognition quality issue",
        ],
        descriptions=[
            "Our automated invoice processing pipeline uses OCR to scan paper invoices and "
            "import them into the ERP system. Since the last scanner firmware update, the "
            "OCR quality has degraded badly. Here's a sample of what the OCR output looks "
            "like vs what the invoice actually says:\n\n"
            "OCR Output:\n"
            "INVDICE #: lNV-2O26-OO4S1\n"
            "Vend0r: Acrrre Supp1ies Ltcl.\n"
            "Date: O3/l7/2O26\n"
            "Arnount Due: $l2,4S6.7B\n"
            "Payrnent Terrns: Net 3O\n"
            "Ship To: Cont0so C0rp, l23 Main 5t, 5uite 4OO\n"
            "P0 Nurnber: PO-2O26-OO89l\n"
            "Line lterns:\n"
            "  l. Widget A (SKU: WDG-OOl) - Qty: lOO - Unit: $45.6O - Tot: $4,S6O.OO\n"
            "  2. Widget B (5KU: WDG-OO2) - Qty: 5O - Unit: $87.l2 - Tot: $4,3S6.OO\n"
            "  3. 5hipping & Hancl1ing - $34O.7B\n"
            "  Subtota1: $9,l56.7B\n"
            "  Tax (8.25%): $3,3OO.OO\n"
            "  TOTAL: $l2,4S6.7B\n\n"
            "The OCR is consistently confusing 0/O, l/1, S/5, B/8, rn/m, and cl/d. This "
            "is causing data validation failures in the ERP import — about 300 invoices "
            "are stuck in the error queue.",
            "Invoice OCR pipeline is producing garbled output — zeros read as letter O, "
            "ones as lowercase L, fives as S, eights as B. ~300 invoices stuck in the "
            "ERP import error queue. Started after scanner firmware update last week. "
            "Need to fix the OCR quality and reprocess the failed batch.",
        ],
        next_best_actions=[
            "Roll back the scanner firmware to the previous version and reprocess the "
            "300 failed invoices through the OCR pipeline.",
            "Investigate the scanner firmware update impact on OCR accuracy and adjust "
            "the OCR engine's character confidence thresholds.",
        ],
        remediation_steps=[
            [
                "Roll back the scanner firmware to the previous stable version",
                "Recalibrate the OCR engine with the original scanner settings",
                "Reprocess the 300 failed invoices through the corrected OCR pipeline",
                "Validate a sample of reprocessed invoices against the original paper copies",
                "Add OCR confidence scoring to flag low-quality scans before ERP import",
            ],
        ],
        tags=["data-cleanup", "ocr-scan-noise"],
    ),
    # ──────────────────────────────────────────────────────────────────
    # WinRM session transcript output
    # ──────────────────────────────────────────────────────────────────
    Scenario(
        scenario_id="cleanup-winrm-transcript",
        category="Software & Applications",
        priority="P2",
        assigned_team="Enterprise Applications",
        needs_escalation=False,
        missing_information=["affected_users", "environment_details"],
        subjects=[
            "App deployment failed on 50 servers — WinRM transcript output attached",
            "SCCM task sequence failing — WinRM remote session logs below",
        ],
        descriptions=[
            "The overnight SCCM task sequence to deploy the new CRM agent failed on 50 "
            "out of 200 servers. I captured the WinRM transcript from one of the failed "
            "servers. Here's the session output:\n\n"
            "**********************\n"
            "Windows Remote Management (WinRM) Session Transcript\n"
            "Start Time: 2026-03-17T01:30:15.4423891Z\n"
            "Machine: APPSRV-047.contoso.com\n"
            "User: CONTOSO\\svc_sccm_deploy\n"
            "**********************\n"
            "PS C:\\Windows\\system32> Get-Service -Name 'CRMAgentSvc' | Stop-Service "
            "-Force\n"
            "WARNING: Waiting for service 'CRM Agent Service (CRMAgentSvc)' to stop...\n"
            "WARNING: Waiting for service 'CRM Agent Service (CRMAgentSvc)' to stop...\n"
            "WARNING: Waiting for service 'CRM Agent Service (CRMAgentSvc)' to stop...\n"
            "PS C:\\Windows\\system32> $msiPath = '\\\\filesvr01\\deployments$\\CRMAgent"
            "\\CRMAgent_v3.2.1.msi'\n"
            "PS C:\\Windows\\system32> Start-Process msiexec.exe -ArgumentList '/i', "
            "$msiPath, '/qn', '/norestart', '/l*v', 'C:\\Logs\\CRMAgent_install.log' "
            "-Wait -PassThru\n\n"
            "ExitCode : 1603\n"
            "HasExited : True\n"
            "StartTime : 3/17/2026 1:31:02 AM\n"
            "ExitTime  : 3/17/2026 1:33:47 AM\n\n"
            "PS C:\\Windows\\system32> Get-Content C:\\Logs\\CRMAgent_install.log | "
            "Select-Object -Last 20\n"
            "MSI (s) (3C:A8) [01:33:45:123]: Product: CRM Agent -- Error 1603. Fatal "
            "error during installation.\n"
            "MSI (s) (3C:A8) [01:33:45:124]: Note: 1: 1729\n"
            "MSI (s) (3C:A8) [01:33:45:125]: Product: CRM Agent -- Configuration "
            "failed.\n"
            "MSI (s) (3C:A8) [01:33:47:001]: MainEngineThread is returning 1603\n"
            "**********************\n"
            "End Time: 2026-03-17T01:34:02.8891234Z\n"
            "**********************\n\n"
            "MSI error 1603 on 50 servers. The install works fine on test servers. Suspect "
            "a prerequisite is missing on the production app servers.",
            "CRM agent MSI deployment failing with exit code 1603 on 50 production app "
            "servers via WinRM/SCCM. WinRM transcript shows the service stop succeeded but "
            "msiexec returned fatal error. Works on test servers. Suspect missing "
            "prerequisite (.NET version or VC++ runtime) on the production fleet.",
        ],
        next_best_actions=[
            "Compare the prerequisite software inventory between the test servers and the "
            "50 failed production servers — MSI error 1603 typically indicates a missing "
            "dependency.",
            "Check the CRM Agent MSI installation log on one of the failed servers for "
            "the specific prerequisite check that failed before the 1603 error.",
        ],
        remediation_steps=[
            [
                "Review the full MSI installation log (C:\\Logs\\CRMAgent_install.log) for the root cause",
                "Compare installed prerequisites (.NET, VC++ runtimes) between test and failed production servers",
                "Deploy the missing prerequisite to the 50 failed servers via SCCM",
                "Re-run the CRM Agent MSI deployment on the remediated servers and verify success",
            ],
        ],
        tags=["data-cleanup", "winrm-transcript"],
    ),
    # ──────────────────────────────────────────────────────────────────
    # 86. SQL query results pasted verbatim in ticket body
    # ──────────────────────────────────────────────────────────────────
    Scenario(
        scenario_id="cleanup-sql-query-results",
        category="Data & Storage",
        priority="P2",
        assigned_team="Data Platform",
        needs_escalation=False,
        missing_information=["affected_system", "environment_details"],
        subjects=[
            "Database query returning wrong results — see output below",
            "SQL report numbers don't match — pasting query output",
        ],
        descriptions=[
            "The quarterly revenue report is showing incorrect totals. I ran the query "
            "directly and the numbers are wrong. Here's the output:\n\n"
            "```\n"
            "SELECT department, SUM(revenue) as total_revenue, COUNT(*) as txn_count\n"
            "FROM financial_transactions\n"
            "WHERE transaction_date BETWEEN '2026-01-01' AND '2026-03-31'\n"
            "GROUP BY department\n"
            "ORDER BY total_revenue DESC;\n\n"
            "+---------------------+---------------+-----------+\n"
            "| department          | total_revenue | txn_count |\n"
            "+---------------------+---------------+-----------+\n"
            "| Wealth Management   |  12847293.42  |    42891  |\n"
            "| Institutional Trade |   8293847.19  |    18472  |\n"
            "| Retail Banking      |   4928371.83  |    89234  |\n"
            "| Corporate Finance   |   3847291.57  |     7823  |\n"
            "| Asset Management    |   2938471.28  |    12847  |\n"
            "| NULL                |    482937.11  |     3291  |\n"
            "+---------------------+---------------+-----------+\n"
            "6 rows in set (4.82 sec)\n"
            "```\n\n"
            "The NULL department shouldn't exist and the Wealth Management total is way off "
            "from what Finance is reporting. Looks like a data integrity issue.",
            "I'm getting mismatched revenue numbers from the data warehouse. Query and "
            "results attached:\n\n"
            "EXEC sp_quarterly_revenue @year=2026, @quarter=1;\n\n"
            "department | total_revenue | delta_pct\n"
            "----------|--------------|----------\n"
            "WM | 12847293.42 | +23.4%\n"
            "IT | 8293847.19 | -2.1%\n"
            "RB | 4928371.83 | +8.7%\n"
            "(NULL) | 482937.11 | N/A\n\n"
            "The NULL rows appeared after last week's ETL migration. Finance team says these "
            "numbers don't reconcile with their GL system.",
        ],
        next_best_actions=[
            "Investigate the NULL department entries in financial_transactions — likely an "
            "ETL mapping issue from the recent migration that left department_id unmapped.",
            "Check the ETL pipeline for the financial_transactions table — NULL department "
            "values indicate a join failure or missing dimension mapping.",
        ],
        remediation_steps=[
            [
                "Query the source system for transactions with NULL department_id to identify the root cause",
                "Check the ETL pipeline logs from the recent migration for mapping failures",
                "Backfill the department_id for affected records from the source system",
                "Add a NOT NULL constraint or validation check to the ETL pipeline",
                "Re-run the quarterly revenue report and reconcile with Finance GL",
            ],
        ],
        tags=["data-cleanup", "sql-output", "tabular-data"],
    ),
    # ──────────────────────────────────────────────────────────────────
    # 87. Windows Event Viewer XML blocks pasted
    # ──────────────────────────────────────────────────────────────────
    Scenario(
        scenario_id="cleanup-windows-event-log-xml",
        category="Software & Applications",
        priority="P2",
        assigned_team="Enterprise Applications",
        needs_escalation=False,
        missing_information=["affected_users", "reproduction_frequency"],
        subjects=[
            "Application crash — pasting Event Viewer log",
            "SAP GUI crashing — Windows Event Log XML attached",
        ],
        descriptions=[
            "SAP GUI keeps crashing every time I try to run a BW report. Here's what "
            "Windows Event Viewer shows:\n\n"
            "<Event xmlns='http://schemas.microsoft.com/win/2004/08/events/event'>\n"
            "  <System>\n"
            "    <Provider Name='Application Error' />\n"
            "    <EventID>1000</EventID>\n"
            "    <Level>2</Level>\n"
            "    <TimeCreated SystemTime='2026-03-15T14:23:47.382Z' />\n"
            "    <Computer>WS-FIN-4821.contoso.local</Computer>\n"
            "  </System>\n"
            "  <EventData>\n"
            "    <Data Name='ApplicationName'>saplogon.exe</Data>\n"
            "    <Data Name='ApplicationVersion'>7.70.5.0</Data>\n"
            "    <Data Name='FaultingModule'>ntdll.dll</Data>\n"
            "    <Data Name='FaultOffset'>0x000000000005bf3c</Data>\n"
            "    <Data Name='ExceptionCode'>0xc0000005</Data>\n"
            "  </EventData>\n"
            "</Event>\n\n"
            "<Event xmlns='http://schemas.microsoft.com/win/2004/08/events/event'>\n"
            "  <System>\n"
            "    <Provider Name='.NET Runtime' />\n"
            "    <EventID>1026</EventID>\n"
            "    <Level>2</Level>\n"
            "    <TimeCreated SystemTime='2026-03-15T14:23:47.395Z' />\n"
            "  </System>\n"
            "  <EventData>\n"
            "    <Data>Application: saplogon.exe\n"
            "Framework Version: v4.0.30319\n"
            "Description: The process was terminated due to an unhandled exception.\n"
            "Exception Info: System.AccessViolationException</Data>\n"
            "  </EventData>\n"
            "</Event>\n\n"
            "This happens every time I try to open transaction SE16 for table BSEG.",
            "SAP GUI crash dump from Event Viewer. Application Error ID 1000 with "
            "faulting module ntdll.dll. Exception code 0xc0000005 "
            "(access violation). Started after the March patch Tuesday updates. "
            "Multiple XML event entries — the key one is the .NET Runtime error 1026 "
            "showing System.AccessViolationException in saplogon.exe 7.70.5.0.",
        ],
        next_best_actions=[
            "Parse the Event Viewer XML — the crash is saplogon.exe 7.70.5.0 with an "
            "access violation in ntdll.dll, likely triggered by March patches.",
            "SAP GUI 7.70 crashing with AccessViolationException — check for SAP Note "
            "regarding compatibility with recent Windows patches.",
        ],
        remediation_steps=[
            [
                "Check SAP Note database for known issues with SAP GUI 7.70.5.0 and recent Windows updates",
                "Test with SAP GUI 8.00 (latest version) to see if the crash is resolved",
                "If rollback is needed, uninstall the March cumulative update KB5034441",
                "Clear SAP GUI local cache and user-specific configuration files",
                "If issue persists, collect a full crash dump and open an SAP support incident",
            ],
        ],
        tags=["data-cleanup", "event-log", "xml-dump", "application-crash"],
    ),
    # ──────────────────────────────────────────────────────────────────
    # 88. Malformed/corrupted email headers pasted
    # ──────────────────────────────────────────────────────────────────
    Scenario(
        scenario_id="cleanup-email-header-malformed",
        category="Software & Applications",
        priority="P3",
        assigned_team="Enterprise Applications",
        needs_escalation=False,
        missing_information=["error_message", "affected_users"],
        subjects=[
            "Emails arriving with garbled headers — see raw headers below",
            "Exchange email headers corrupted — authentication failures",
        ],
        descriptions=[
            "I'm getting emails with corrupted headers. Our compliance team needs the "
            "full header trace. Here's what I see in the raw source:\n\n"
            "Received: from mail-yw1-xb49.google.com (mail-yw1-xb49.google.com "
            "[2607:f8b0:4864:20::b49])\n"
            "        by mx01.contoso.com (Postfix) with ESMTPS id 4R3bKv6Qz\xc3\xb8z\n"
            "        for <trading@contoso.com>; Sat, 15 Mar 2026 09:14:22 +0000 (UTC)\n"
            "DKIM-Signature: v=1; a=rsa-sha256; c=relaxed/relaxed;\n"
            "        d=gmail.com; s=20230601; t=171062\xef\xbf\xbd662;\n"
            "        h=from:to:subject:date:message-id;\n"
            "        bh=CORRUPT_HASH_BASE64==;\n"
            "        b=TRUNCATED_SIGNATURE\n"
            "Authentication-Results: mx01.contoso.com;\n"
            "        dkim=temperror (key retrieval timeout);\n"
            "        spf=none (no SPF record);\n"
            "        dmarc=none (no DMARC policy found)\n"
            "X-MS-Exchange-Organization-AuthAs: Anonymous\n"
            "X-MS-Exchange-Organization-SCL: 5\n"
            "X-Mailer: \xff\xfe<\x00n\x00u\x00l\x00l\x00>\n"
            "Subject: =?UTF-8?B?CORRUPTED_BASE64_ENCODING==?=\n"
            "Content-Type: multipart/mixed;\n"
            '        boundary="----=_Part_BROKEN\n\n'
            "The DKIM is failing with temperror and the SCL score is 5 which is high. "
            "Several users in Trading are getting these daily.",
            "Raw email headers from a message that failed Exchange transport rules. "
            "Headers show DKIM temperror, missing SPF record, DMARC none, and SCL 5. "
            "The X-Mailer header contains corrupt UTF-16LE bytes and the MIME boundary "
            "is broken. Started after we migrated to Exchange Online last month.",
        ],
        next_best_actions=[
            "Investigate the DKIM temperror and missing SPF/DMARC for the sending domain — "
            "the SCL 5 score suggests the messages are borderline spam.",
            "Check Exchange Online transport rules and connector configuration for DKIM "
            "validation timeout issues after the migration.",
        ],
        remediation_steps=[
            [
                "Check the Exchange Online mail flow logs for DKIM validation timeout patterns",
                "Verify DNS resolution from Exchange Online to the sender's DKIM key servers",
                "Review the Exchange Online connector configuration for inbound mail",
                "Adjust the SCL threshold or create a transport rule for the affected sender domain",
                "If the corrupt headers are consistent, open a case with Microsoft support",
            ],
        ],
        tags=["data-cleanup", "email-headers", "corrupted-encoding"],
    ),
    # ──────────────────────────────────────────────────────────────────
    # 89. References to attachments that don't exist
    # ──────────────────────────────────────────────────────────────────
    Scenario(
        scenario_id="cleanup-corrupted-attachment-ref",
        category="Hardware & Peripherals",
        priority="P3",
        assigned_team="Endpoint Engineering",
        needs_escalation=False,
        missing_information=["screenshot_or_attachment", "device_info", "error_message"],
        subjects=[
            "Laptop screen flickering — see attached photos and video",
            "Monitor display issue — screenshots attached (3 files)",
        ],
        descriptions=[
            "My laptop screen has been flickering for the past two days. I've attached "
            "the following files showing the issue:\n\n"
            "- screen_flicker_video.mp4 (2.3 MB)\n"
            "- error_screenshot_1.png (482 KB)\n"
            "- error_screenshot_2.png (517 KB)\n"
            "- device_manager_display.png (234 KB)\n\n"
            "As you can see in the video, the flickering happens every 3-5 seconds "
            "and gets worse when I'm on battery power. The Device Manager screenshot "
            "shows the Intel UHD Graphics 770 driver version 31.0.101.4826. "
            "Please review the attached evidence and let me know next steps.\n\n"
            "[Note: The above files were referenced but no actual attachments are present "
            "in this ticket submission.]",
            "Display issues on my ThinkPad X1 Carbon Gen 11. See attached:\n\n"
            "1) flicker_recording.mov — shows the 3-second flicker cycle\n"
            "2) display_settings.png — current resolution and refresh rate\n"
            "3) dxdiag_output.txt — full DirectX diagnostic report\n\n"
            "The flicker started after updating to the latest Intel graphics driver. "
            "Rolling back didn't help. Happens in both Windows and BIOS so it might "
            "be hardware. Check the dxdiag for details.",
        ],
        next_best_actions=[
            "Note that the referenced attachments are not present — request the user "
            "re-submit the screenshots and video. The description suggests a display "
            "driver or hardware issue on the laptop.",
            "Attachments referenced but missing. Based on the description, investigate "
            "Intel UHD Graphics driver compatibility on the ThinkPad X1 Carbon.",
        ],
        remediation_steps=[
            [
                "Request the user to re-attach the referenced files (video, screenshots, dxdiag)",
                "Check if the Intel UHD Graphics 770 driver version 31.0.101.4826 has known flicker issues",
                "Test with the Microsoft Basic Display Adapter driver to isolate hardware vs driver",
                "If flickering persists with basic driver, schedule hardware inspection for display cable",
                "Check Lenovo support for BIOS updates that address display issues on X1 Carbon Gen 11",
            ],
        ],
        tags=["data-cleanup", "missing-attachments", "phantom-references"],
    ),
    # ──────────────────────────────────────────────────────────────────
    # 90. RTL Arabic text mixed with LTR IP addresses and numbers
    # ──────────────────────────────────────────────────────────────────
    Scenario(
        scenario_id="cleanup-rtl-numbers-mixed",
        category="Network & Connectivity",
        priority="P2",
        assigned_team="Network Operations",
        needs_escalation=False,
        missing_information=["network_location", "error_message"],
        subjects=[
            "مشكلة في الشبكة — VPN connection issue from Riyadh office",
            "Network problem — اتصال VPN من مكتب الرياض",
        ],
        descriptions=[
            "مرحبا فريق تكنولوجيا المعلومات,\n\n"
            "أواجه مشكلة في الاتصال بشبكة VPN من مكتب الرياض. "
            "عنوان IP المحلي: 10.42.128.55 "
            "وعنوان البوابة: 10.42.128.1\n\n"
            "The VPN gateway at vpn-riyadh.contoso.com (203.0.113.47) is not responding "
            "to connection attempts. Error code: 0x800704CF\n\n"
            "الرجاء المساعدة في أقرب وقت. "
            "فريق التداول بالكامل غير قادر على الوصول "
            "إلى الأنظمة المركزية في New York.",
            "VPN connection from Riyadh office failing. المشكلة بدأت منذ الصباح.\n"
            "Local IP: 10.42.128.55\n"
            "Gateway: 10.42.128.1\n"
            "VPN server: vpn-riyadh.contoso.com (203.0.113.47)\n"
            "Error: 0x800704CF — الشبكة غير متاحة\n\n"
            "فريق التداول بالكامل (٠١٥ مستخدم) متأثر. "
            "الرجاء التحقق من حالة البوابة.",
        ],
        next_best_actions=[
            "VPN gateway vpn-riyadh.contoso.com (203.0.113.47) not responding — check "
            "gateway health and network path from the Riyadh office subnet 10.42.128.0/24.",
            "Investigate VPN connectivity failure from Riyadh office. Error 0x800704CF "
            "indicates network location unreachable.",
        ],
        remediation_steps=[
            [
                "Check the health of the VPN gateway at vpn-riyadh.contoso.com (203.0.113.47)",
                "Verify network routing from the Riyadh office subnet (10.42.128.0/24) to the gateway",
                "Test DNS resolution of vpn-riyadh.contoso.com from the Riyadh office network",
                "Check if a firewall rule change or ISP issue is blocking the VPN tunnel",
                "If the gateway is down, fail over to the backup VPN endpoint and notify NOC",
            ],
        ],
        tags=["data-cleanup", "rtl-text", "arabic", "mixed-direction"],
    ),
    # ──────────────────────────────────────────────────────────────────
    # 91. APM/telemetry data dump pasted in ticket
    # ──────────────────────────────────────────────────────────────────
    Scenario(
        scenario_id="cleanup-apm-telemetry-dump",
        category="Software & Applications",
        priority="P2",
        assigned_team="Enterprise Applications",
        needs_escalation=False,
        missing_information=["affected_users", "business_impact"],
        subjects=[
            "App slow — Application Insights telemetry data dump",
            "Performance degradation — pasting APM trace data",
        ],
        descriptions=[
            "The CRM portal is extremely slow. I exported the Application Insights "
            "traces:\n\n"
            '{"timestamp":"2026-03-15T10:23:47.382Z","severityLevel":2,'
            '"message":"Dependency call to sql-prod-east.database.windows.net exceeded '
            'threshold","customDimensions":{"DependencyType":"SQL",'
            '"DependencyTarget":"sql-prod-east.database.windows.net",'
            '"Duration":"4823ms","Success":"False",'
            '"ResultCode":"Timeout expired. The timeout period elapsed prior to '
            'completion of the operation","OperationName":"GET /api/v2/accounts",'
            '"CloudRoleName":"crm-api-prod","CloudRoleInstance":"crm-api-prod_3",'
            '"AppId":"a8f3b2c1-4d5e-6f7a-8b9c-0d1e2f3a4b5c"}}\n'
            '{"timestamp":"2026-03-15T10:23:48.104Z","severityLevel":3,'
            '"message":"Request failed with status 504",'
            '"customDimensions":{"Url":"/api/v2/accounts?page=1&size=50",'
            '"Duration":"5001ms","StatusCode":"504","CloudRoleName":"crm-api-prod"}}\n'
            '{"timestamp":"2026-03-15T10:23:48.207Z","severityLevel":2,'
            '"message":"Circuit breaker opened for sql-prod-east",'
            '"customDimensions":{"ConsecutiveFailures":"5",'
            '"BreakDuration":"30s"}}\n\n'
            "The SQL dependency is timing out at ~5 seconds and the circuit breaker "
            "opened after 5 consecutive failures. This started about 30 minutes ago.",
            "CRM API returning 504s. Application Insights shows SQL dependency "
            "timeouts to sql-prod-east.database.windows.net with 4823ms average "
            "duration. Circuit breaker opened after 5 failures. Affecting the "
            "/api/v2/accounts endpoint on crm-api-prod instances.",
        ],
        next_best_actions=[
            "SQL Server sql-prod-east.database.windows.net is timing out — check "
            "Azure SQL Database metrics for DTU/CPU saturation or blocking queries.",
            "Investigate the SQL dependency timeout causing CRM API 504 errors — "
            "circuit breaker has opened on sql-prod-east.",
        ],
        remediation_steps=[
            [
                "Check Azure SQL Database metrics for sql-prod-east: DTU utilization, active sessions, deadlocks",
                "Look for long-running or blocking queries in sys.dm_exec_requests",
                "If DTU is saturated, scale up the database tier temporarily",
                "Restart the crm-api-prod instances to reset the circuit breaker",
                "Set up an Azure Monitor alert for SQL dependency duration > 2 seconds",
            ],
        ],
        tags=["data-cleanup", "apm-telemetry", "json-traces", "application-insights"],
    ),
    # ──────────────────────────────────────────────────────────────────
    # 92. Git diff/patch content pasted in ticket
    # ──────────────────────────────────────────────────────────────────
    Scenario(
        scenario_id="cleanup-git-diff-paste",
        category="Software & Applications",
        priority="P3",
        assigned_team="Enterprise Applications",
        needs_escalation=False,
        missing_information=["environment_details", "steps_to_reproduce"],
        subjects=[
            "Deployment broke production — here's the diff that caused it",
            "Config change broke the app — pasting git diff",
        ],
        descriptions=[
            "The last deployment broke the login flow. Here's the exact change:\n\n"
            "```diff\n"
            "diff --git a/config/auth.yaml b/config/auth.yaml\n"
            "index 3a7b2c1..9f8e7d6 100644\n"
            "--- a/config/auth.yaml\n"
            "+++ b/config/auth.yaml\n"
            "@@ -12,8 +12,8 @@ authentication:\n"
            "   oauth2:\n"
            "     provider: azure-ad\n"
            '-    tenant_id: "a1b2c3d4-e5f6-7890-abcd-ef1234567890"\n'
            '-    client_id: "12345678-abcd-efgh-ijkl-mnop12345678"\n'
            '+    tenant_id: "PLACEHOLDER_TENANT_ID"\n'
            '+    client_id: "PLACEHOLDER_CLIENT_ID"\n'
            "     redirect_uri: https://crm.contoso.com/auth/callback\n"
            "     scopes:\n"
            "       - openid\n"
            "@@ -23,3 +23,5 @@ authentication:\n"
            "   session:\n"
            "     timeout: 3600\n"
            "     secure: true\n"
            "+  debug:\n"
            "+    verbose_logging: true\n"
            "```\n\n"
            "Someone committed placeholder values instead of the actual Azure AD "
            "credentials. The deployment pipeline didn't catch it because it only "
            "validates YAML syntax, not content. All users are getting 401 errors.",
            "Production login is broken. Git diff shows auth.yaml was changed to "
            "use PLACEHOLDER_TENANT_ID and PLACEHOLDER_CLIENT_ID instead of real "
            "Azure AD values. Also verbose debug logging was enabled in production. "
            "Committed by the CI pipeline 2 hours ago. All /auth/callback requests "
            "returning 401.",
        ],
        next_best_actions=[
            "Revert the auth.yaml configuration change — placeholder values replaced "
            "actual Azure AD credentials in the last deployment.",
            "Roll back the config/auth.yaml change via git revert and redeploy "
            "immediately to restore production login.",
        ],
        remediation_steps=[
            [
                "Revert the auth.yaml change via git revert and trigger an emergency deployment",
                "Restore the correct Azure AD tenant_id and client_id from the secrets vault",
                "Remove the debug verbose_logging setting from production config",
                "Add a deployment gate that validates auth configuration values are not placeholders",
                "Review the CI/CD pipeline to add content validation beyond YAML syntax checks",
            ],
        ],
        tags=["data-cleanup", "git-diff", "configuration-change"],
    ),
    # ──────────────────────────────────────────────────────────────────
    # 93. Windows registry key export pasted
    # ──────────────────────────────────────────────────────────────────
    Scenario(
        scenario_id="cleanup-registry-key-dump",
        category="Software & Applications",
        priority="P3",
        assigned_team="Enterprise Applications",
        needs_escalation=False,
        missing_information=["device_info", "affected_users"],
        subjects=[
            "Application won't start — registry export from affected machine",
            "Software crash on launch — see registry dump below",
        ],
        descriptions=[
            "Bloomberg Terminal won't start after the latest Intune policy push. "
            "Here's the registry export from the affected machine:\n\n"
            "Windows Registry Editor Version 5.00\n\n"
            "[HKEY_LOCAL_MACHINE\\SOFTWARE\\Bloomberg L.P.\\Terminal]\n"
            '"InstallDir"="C:\\\\blp\\\\DAPI"\n'
            '"Version"="2024.3.15.1"\n'
            '"LicenseKey"="XXXX-XXXX-XXXX-REDACTED"\n'
            '"DataPath"="C:\\\\blp\\\\data"\n\n'
            "[HKEY_LOCAL_MACHINE\\SOFTWARE\\Bloomberg L.P.\\Terminal\\Network]\n"
            '"PrimaryServer"="bpipe-prod.contoso.com"\n'
            '"Port"=dword:00001f40\n'
            '"UseSSL"=dword:00000001\n'
            '"ProxyEnabled"=dword:00000001\n'
            '"ProxyServer"="proxy.contoso.com:8080"\n\n'
            "[HKEY_LOCAL_MACHINE\\SOFTWARE\\Policies\\Bloomberg L.P.]\n"
            '"RestrictedMode"=dword:00000001\n'
            '"AllowExternalConnections"=dword:00000000\n\n'
            "After the Intune push, the RestrictedMode key appeared and "
            "AllowExternalConnections was set to 0. The terminal can't connect to "
            "Bloomberg's data feed anymore.",
            "Bloomberg Terminal broken after Intune policy change. Registry shows new "
            "policy keys under HKLM\\SOFTWARE\\Policies\\Bloomberg L.P. that block "
            "external connections. The AllowExternalConnections DWORD was set to 0 "
            "and RestrictedMode to 1. Need these rolled back for the trading floor.",
        ],
        next_best_actions=[
            "The Intune policy pushed RestrictedMode=1 and AllowExternalConnections=0 "
            "to Bloomberg — roll back these policy keys or add an exception for Bloomberg.",
            "Check the Intune configuration profile that modified Bloomberg registry keys "
            "and either exclude Bloomberg or create an exception policy.",
        ],
        remediation_steps=[
            [
                "Identify the Intune configuration profile that set the Bloomberg policy keys",
                "Create an exception in the Intune policy for Bloomberg Terminal's external connections",
                "Deploy the updated policy to the affected workstations",
                "Verify Bloomberg Terminal connects to the data feed after the policy update",
                "Add Bloomberg Terminal to the approved external applications list in the security policy",
            ],
        ],
        tags=["data-cleanup", "registry-dump", "policy-configuration"],
    ),
    # ──────────────────────────────────────────────────────────────────
    # 94. PEM certificate chain blocks embedded
    # ──────────────────────────────────────────────────────────────────
    Scenario(
        scenario_id="cleanup-pem-certificate-chain",
        category="Security & Compliance",
        priority="P2",
        assigned_team="Security Operations",
        needs_escalation=True,
        missing_information=["affected_system", "business_impact"],
        subjects=[
            "SSL certificate expiring — pasting cert chain for review",
            "Certificate error on internal portal — cert chain below",
        ],
        descriptions=[
            "Users are getting certificate warnings on https://trading.contoso.com. "
            "Here's the full certificate chain:\n\n"
            "-----BEGIN CERTIFICATE-----\n"
            "MIIFjTCCA3WgAwIBAgIUZ3h0ZXN0Y2VydGlmaWNhdGUwMB4XDTI2MDMxNTAwMDAw\n"
            "MFoXDTI2MDMyMjAwMDAwMFowgYkxCzAJBgNVBAYTAlVTMREwDwYDVQQIDAhOZXcg\n"
            "WW9yazERMA8GA1UEBwwITmV3IFlvcmsxHjAcBgNVBAoMFUNvbnRvc28gRmluYW5j\n"
            "aWFsIFNlcnZpY2VzMRQwEgYDVQQLDAtJVCBTZWN1cml0eTEeMBwGA1UEAwwVdHJh\n"
            "ZGluZy5jb250b3NvLmNvbTBZMBMGByqGSM49AgEGCCqGSM49AwEHA0IABFake=\n"
            "-----END CERTIFICATE-----\n\n"
            "-----BEGIN CERTIFICATE-----\n"
            "MIIEtjCCAp6gAwIBAgIUY29udG9zby1pbnRlcm1lZGlhdGUwHhcNMjUwMTAxMDAw\n"
            "MDAwWhcNMjcwMTAxMDAwMDAwWjBhMQswCQYDVQQGEwJVUzERMA8GA1UECAwITmV3\n"
            "IFlvcmsxHjAcBgNVBAoMFUNvbnRvc28gRmluYW5jaWFsIFNlcnZpY2VzMR8wHQYD\n"
            "VQQDDBZDb250b3NvIEludGVybWVkaWF0ZSBDQQ==\n"
            "-----END CERTIFICATE-----\n\n"
            "The leaf certificate expires on March 22, 2026 — that's in 7 days! "
            "This is the trading platform used by all our institutional traders.",
            "Certificate chain for trading.contoso.com shows leaf cert expiring "
            "March 22, 2026. Intermediate CA cert is Contoso Internal CA. The "
            "trading platform is critical for institutional operations — if the "
            "cert expires, all HTTPS connections will fail.",
        ],
        next_best_actions=[
            "URGENT: trading.contoso.com SSL certificate expires in 7 days. Initiate "
            "emergency certificate renewal through the PKI team.",
            "Renew the SSL certificate for trading.contoso.com before March 22 — "
            "coordinate with the PKI team and trading platform operations.",
        ],
        remediation_steps=[
            [
                "Generate a new CSR for trading.contoso.com with the same subject and SANs",
                "Submit the CSR to the internal CA or public CA for signing",
                "Deploy the new certificate to the trading platform load balancer",
                "Verify the full certificate chain including intermediate CA",
                "Set up automated certificate expiry monitoring with 30-day advance alerts",
            ],
        ],
        tags=["data-cleanup", "pem-certificate", "certificate-expiry"],
    ),
    # ──────────────────────────────────────────────────────────────────
    # 95. Markdown rendering artifacts in ticket
    # ──────────────────────────────────────────────────────────────────
    Scenario(
        scenario_id="cleanup-markdown-rendering-broken",
        category="Software & Applications",
        priority="P3",
        assigned_team="Enterprise Applications",
        needs_escalation=False,
        missing_information=["application_version", "steps_to_reproduce"],
        subjects=[
            "Teams wiki page shows raw markdown instead of formatted text",
            "SharePoint page rendering broken — showing markdown source",
        ],
        descriptions=[
            "Our team's wiki page in Microsoft Teams is showing raw markdown instead "
            "of formatted content. Here's what the page looks like:\n\n"
            "# Q1 Trading Operations Runbook\n\n"
            "## Pre-Market Checks\n\n"
            "1. Verify [Bloomberg connectivity](https://bpipe.contoso.com/status)\n"
            "2. Check [FIX engine status](http://fix-monitor.contoso.com:8080)\n"
            "3. Confirm **all trading pairs** are active\n\n"
            "| System | Status URL | Owner |\n"
            "|--------|-----------|-------|\n"
            "| Bloomberg | [link](https://bbg-status) | Trading Tech |\n"
            "| FIX Engine | [link](http://fix-mon:8080) | \\*\\*OMS Team\\*\\* |\n"
            "| Risk System | [link](https://risk.contoso.com) | Risk Ops |\n\n"
            "## Emergency Procedures\n\n"
            "> **IMPORTANT**: If Bloomberg feed drops during market hours, "
            "immediately contact the NOC at ext. 4739\n\n"
            "```\n"
            "Emergency contacts:\n"
            "- NOC: ext 4739\n"
            "- Trading desk lead: ext 4201\n"
            "```\n\n"
            "The escaped asterisks (\\*\\*) and the raw table pipes are visible. "
            "The links show as [text](url) instead of clickable links. This started "
            "after the last Teams update.",
            "Teams wiki rendering broken — all markdown is showing as raw text. "
            "Tables with pipe characters, bold with double asterisks, links with "
            "brackets, and code blocks with backticks are all visible as source. "
            "The page was working fine before the March Teams desktop update.",
        ],
        next_best_actions=[
            "Investigate the Teams wiki markdown rendering regression after the March "
            "desktop update — check if it's a known issue with the Teams client version.",
            "Check Microsoft 365 service health dashboard for known Teams wiki rendering "
            "issues. May need to clear Teams cache or roll back the client update.",
        ],
        remediation_steps=[
            [
                "Check the Microsoft 365 Service Health Dashboard for known Teams rendering issues",
                "Clear the Teams desktop cache (AppData/Roaming/Microsoft/Teams/Cache)",
                "Test rendering in Teams web client to isolate desktop vs server-side issue",
                "If desktop-only, check the Teams client version and roll back if needed",
                "Report the issue to Microsoft support if it's not a known issue",
            ],
        ],
        tags=["data-cleanup", "markdown-artifacts", "rendering-issue"],
    ),
    # ──────────────────────────────────────────────────────────────────
    # 96. Cron/syslog entries repeated hundreds of times
    # ──────────────────────────────────────────────────────────────────
    Scenario(
        scenario_id="cleanup-cron-syslog-flood",
        category="Software & Applications",
        priority="P2",
        assigned_team="Enterprise Applications",
        needs_escalation=False,
        missing_information=["affected_system", "business_impact"],
        subjects=[
            "Cron job flooding syslog — thousands of identical entries",
            "Server syslog filled with repeated cron errors",
        ],
        descriptions=[
            "The backup cron job on srv-db-prod-02 is generating thousands of "
            "identical syslog entries. Here's a sample (this repeats 2,847 times "
            "in the last hour):\n\n" + "Mar 15 10:00:01 srv-db-prod-02 CRON[28491]: (backup_svc) CMD "
            "(/opt/contoso/scripts/db_backup.sh --target=azure-blob "
            "--container=sql-backups --retention=30d 2>&1 | logger -t db-backup)\n"
            "Mar 15 10:00:01 srv-db-prod-02 db-backup: ERROR: Azure Blob Storage "
            "connection failed: AuthenticationErrorDetail: HMAC signature mismatch. "
            "Expected signature: [REDACTED]. Server used: [REDACTED]\n"
            "Mar 15 10:00:01 srv-db-prod-02 db-backup: ERROR: Retry 1/3 failed. "
            "Waiting 5s before next attempt.\n"
            "Mar 15 10:00:06 srv-db-prod-02 db-backup: ERROR: Retry 2/3 failed.\n"
            "Mar 15 10:00:11 srv-db-prod-02 db-backup: ERROR: Retry 3/3 failed. "
            "Giving up. Exit code: 1\n" * 5 + "\n[... 2,847 identical entries in the last hour ...]\n\n"
            "The cron is set to run every minute (which is wrong — it should be "
            "hourly) and each run generates 5 log lines. Syslog is at 98% capacity.",
            "Backup script flooding syslog with Azure Blob auth failures. "
            "HMAC signature mismatch error repeating every minute (should be hourly). "
            "2,847 identical entries in the past hour. Syslog disk at 98%. "
            "Server: srv-db-prod-02. Script: /opt/contoso/scripts/db_backup.sh.",
        ],
        next_best_actions=[
            "Fix the cron schedule from every-minute to hourly, then investigate the "
            "Azure Blob Storage HMAC authentication failure.",
            "Immediately change the cron interval from * to 0 (hourly) to stop the "
            "log flood, then rotate and fix the storage account key.",
        ],
        remediation_steps=[
            [
                "Change the cron schedule from '* * * * *' (every minute) to '0 * * * *' (hourly)",
                "Rotate the Azure Blob Storage access key — the HMAC mismatch suggests the key was changed",
                "Update the backup script configuration with the new storage account key",
                "Rotate the syslog to reclaim disk space (logrotate --force /etc/logrotate.d/syslog)",
                "Test the backup script manually to verify Azure Blob connectivity",
            ],
        ],
        tags=["data-cleanup", "syslog-flood", "repeated-entries", "cron-misconfigured"],
    ),
    # ──────────────────────────────────────────────────────────────────
    # 97. Mixed CJK and Latin text
    # ──────────────────────────────────────────────────────────────────
    Scenario(
        scenario_id="cleanup-mixed-cjk-latin",
        category="Software & Applications",
        priority="P3",
        assigned_team="Enterprise Applications",
        needs_escalation=False,
        missing_information=["application_version", "environment_details"],
        subjects=[
            "システムエラー — SAP ログイン問題 (Singapore office)",
            "SAP login issue from Singapore — 系统登录问题",
        ],
        descriptions=[
            "お疲れ様です。Singaporeオフィスの田中です。\n\n"
            "SAP GUIにログインできません。エラーメッセージ:\n"
            '"Partner not reached (type=A, host=sap-prod-sg.contoso.com, service=3200)"\n\n'
            "今朝から発生しています。他の同僚も同じ問題があると言っています。\n"
            "Network ping to sap-prod-sg.contoso.com: OK (12ms)\n"
            "Telnet to port 3200: Connection refused\n\n"
            "至急対応をお願いします。財務チームの月末処理ができません。",
            "从新加坡办公室无法登录SAP系统。\n"
            'Error: "Partner not reached" on sap-prod-sg.contoso.com:3200\n'
            "Ping OK but port 3200 refused. 可能是SAP服务停止了。\n"
            "财务团队的月末处理受影响。请尽快处理。",
        ],
        next_best_actions=[
            "SAP application server sap-prod-sg.contoso.com port 3200 is refusing "
            "connections — the SAP dispatcher service may be down. Check the instance.",
            "Check SAP instance 00 on sap-prod-sg.contoso.com — port 3200 connection "
            "refused suggests the dispatcher process has stopped.",
        ],
        remediation_steps=[
            [
                "Log into sap-prod-sg.contoso.com and check the SAP dispatcher process (disp+work)",
                "Review the SAP system log (SM21) for crash or shutdown events",
                "Restart the SAP instance if the dispatcher is down: startsap",
                "Verify port 3200 is listening after restart: netstat -an | grep 3200",
                "Confirm SAP login works from the Singapore office after recovery",
            ],
        ],
        tags=["data-cleanup", "cjk-text", "japanese", "chinese", "mixed-language"],
    ),
    # ──────────────────────────────────────────────────────────────────
    # 98. Full MIME multipart email with base64 parts
    # ──────────────────────────────────────────────────────────────────
    Scenario(
        scenario_id="cleanup-base64-multipart-email",
        category="Network & Connectivity",
        priority="P3",
        assigned_team="Network Operations",
        needs_escalation=False,
        missing_information=["network_location", "error_message"],
        subjects=[
            "Email forwarded with full MIME headers — Wi-Fi dropping",
            "Raw MIME email forward — wireless connectivity issue",
        ],
        descriptions=[
            "Forwarding the original email about our Wi-Fi issue. Sorry it came "
            "through as raw MIME:\n\n"
            "MIME-Version: 1.0\n"
            'Content-Type: multipart/mixed; boundary="----=_Part_12345_6789.0123"\n'
            "From: Maria Santos <maria.santos@contoso.com>\n"
            "To: helpdesk@contoso.com\n"
            "Subject: Wi-Fi keeps dropping on 5th floor\n"
            "Date: Sat, 15 Mar 2026 09:14:22 -0500\n\n"
            "------=_Part_12345_6789.0123\n"
            "Content-Type: text/plain; charset=UTF-8\n"
            "Content-Transfer-Encoding: 7bit\n\n"
            "The Wi-Fi on the 5th floor keeps dropping every 15-20 minutes. It's "
            "been happening since Monday and affects everyone in the Wealth Management "
            "area. We're on the 'Contoso-Corp-5G' SSID. When it drops, we have to "
            "manually reconnect. It seems to happen more during peak hours (10am-2pm).\n\n"
            "------=_Part_12345_6789.0123\n"
            'Content-Type: image/png; name="wifi_signal_chart.png"\n'
            "Content-Transfer-Encoding: base64\n"
            'Content-Disposition: attachment; filename="wifi_signal_chart.png"\n\n'
            "iVBORw0KGgoAAAANSUhEUgAAAAoAAAAKCAYAAACNMs+9AAAAFklEQVQYV2P8\n"
            "z8BQDwADhQGAWjR9awAAAABJRU5ErkJggg==\n\n"
            "------=_Part_12345_6789.0123--\n\n"
            "Please ignore all the MIME gibberish — the actual issue is Wi-Fi "
            "dropping on the 5th floor every 15-20 minutes.",
            "Raw MIME multipart email about 5th floor Wi-Fi dropping. Strip the "
            "MIME headers and base64 attachment data. Core issue: Contoso-Corp-5G "
            "SSID drops every 15-20 minutes during peak hours (10am-2pm). Affects "
            "the Wealth Management team. Started last Monday.",
        ],
        next_best_actions=[
            "Investigate Wi-Fi drops on Contoso-Corp-5G SSID on the 5th floor — "
            "likely an AP capacity or channel interference issue during peak hours.",
            "Check the wireless controller for the 5th floor APs — intermittent drops "
            "during peak hours suggest capacity or interference problems.",
        ],
        remediation_steps=[
            [
                "Check wireless controller dashboards for 5th floor AP health and client load",
                "Review channel utilization and interference on the 5GHz band during peak hours",
                "Verify AP firmware is current and check for known issues with 'Contoso-Corp-5G' SSID",
                "If capacity issue, consider adding an AP or adjusting power levels",
                "Monitor after changes to confirm drops stop during peak hours",
            ],
        ],
        tags=["data-cleanup", "mime-multipart", "base64-attachment", "raw-email"],
    ),
    # ──────────────────────────────────────────────────────────────────
    # 99. PowerShell error stream output
    # ──────────────────────────────────────────────────────────────────
    Scenario(
        scenario_id="cleanup-powershell-error-stream",
        category="Access & Authentication",
        priority="P2",
        assigned_team="Identity & Access Management",
        needs_escalation=False,
        missing_information=["affected_users", "environment_details"],
        subjects=[
            "AD sync failing — PowerShell error output below",
            "Entra Connect sync errors — pasting PowerShell output",
        ],
        descriptions=[
            "The Entra Connect (Azure AD Connect) sync is failing. Here's the "
            "PowerShell output from the sync server:\n\n"
            "PS C:\\> Start-ADSyncSyncCycle -PolicyType Delta\n"
            "Start-ADSyncSyncCycle : Connected to localhost.\n"
            "At line:1 char:1\n"
            "+ Start-ADSyncSyncCycle -PolicyType Delta\n"
            "+ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"
            "    + CategoryInfo          : InvalidOperation: (:) [Start-ADSyncSyncCycle], "
            "SyncCycleInProgressException\n"
            "    + FullyQualifiedErrorId : SyncCycleInProgress,Microsoft.IdentityManagement."
            "PowerShell.Cmdlet.StartSyncCycleCmdlet\n\n"
            "PS C:\\> Get-ADSyncScheduler\n\n"
            "AllowedSyncCycleInterval     : 00:30:00\n"
            "CurrentlyEffectiveSyncCycleInterval : 00:30:00\n"
            "CustomizedSyncCycleInterval  : 00:30:00\n"
            "NextSyncCyclePolicyType      : Delta\n"
            "NextSyncCycleStartTimeInUTC  : 3/15/2026 10:30:00 AM\n"
            "PurgeRunHistoryInterval      : 7.00:00:00\n"
            "SyncCycleEnabled             : True\n"
            "MaintenanceEnabled           : True\n"
            "StagingModeEnabled           : False\n"
            "SchedulerSuspended           : False\n"
            "SyncCycleInProgress          : True\n\n"
            "PS C:\\> Get-ADSyncRunProfileResult -RunProfileName 'Delta Synchronization' "
            "| Select-Object -First 3 | Format-List\n\n"
            "Result       : stopped-error\n"
            "StartDate    : 3/15/2026 9:30:00 AM\n"
            "EndDate      : 3/15/2026 9:45:12 AM\n"
            "ErrorDetails : stopped-extension-dll-exception\n\n"
            "The sync has been stuck for over an hour. New users provisioned in AD "
            "this morning cannot access Microsoft 365 services.",
            "Entra Connect sync stuck with stopped-extension-dll-exception. Sync "
            "cycle shows SyncCycleInProgress=True for over an hour. New AD users "
            "can't access M365. PowerShell shows the delta sync failing with "
            "stopped-error status. Need IAM team to investigate.",
        ],
        next_best_actions=[
            "Entra Connect sync is stuck with extension-dll-exception — restart the "
            "sync service and investigate the DLL error.",
            "Reset the stuck Entra Connect sync cycle and investigate the "
            "stopped-extension-dll-exception error in the sync logs.",
        ],
        remediation_steps=[
            [
                "Stop the ADSync service: Stop-Service ADSync",
                "Check the Entra Connect event log for extension-dll-exception details",
                "Clear the sync run history if corrupted: Remove-ADSyncRunProfile",
                "Restart the ADSync service and trigger a fresh delta sync",
                "Verify new AD users appear in Entra ID within 30 minutes after successful sync",
            ],
        ],
        tags=["data-cleanup", "powershell-output", "error-stream", "ad-sync"],
    ),
    # ──────────────────────────────────────────────────────────────────
    # 100. Large JSON API response dump
    # ──────────────────────────────────────────────────────────────────
    Scenario(
        scenario_id="cleanup-json-api-response-dump",
        category="Software & Applications",
        priority="P2",
        assigned_team="Enterprise Applications",
        needs_escalation=False,
        missing_information=["steps_to_reproduce", "affected_users"],
        subjects=[
            "API returning error — full JSON response body attached",
            "REST API 500 error — pasting full response payload",
        ],
        descriptions=[
            "The internal portfolio API is returning 500 errors. Here's the full "
            "response body:\n\n"
            "```json\n"
            "{\n"
            '  "error": {\n'
            '    "code": "InternalServerError",\n'
            '    "message": "An error occurred while processing the request.",\n'
            '    "target": "/api/v3/portfolios/12847/positions",\n'
            '    "details": [\n'
            "      {\n"
            '        "code": "DatabaseConnectionPoolExhausted",\n'
            '        "message": "Cannot obtain a connection from the pool. All pooled '
            "connections are in use and the maximum pool size of 100 has been reached. "
            'Timeout expired.",\n'
            '        "innererror": {\n'
            '          "type": "System.InvalidOperationException",\n'
            '          "stacktrace": "at System.Data.Common.DbConnectionFactory.'
            "TryGetConnection(DbConnectionFactory factory)\\n"
            "at System.Data.SqlClient.SqlConnection.TryOpenInner()\\n"
            "at Contoso.Portfolio.Api.Services.PositionService.GetPositions"
            '(Int32 portfolioId)"\n'
            "        }\n"
            "      }\n"
            "    ],\n"
            '    "requestId": "a8f3b2c1-4d5e-6f7a-8b9c-0d1e2f3a4b5c",\n'
            '    "timestamp": "2026-03-15T14:23:47.382Z"\n'
            "  }\n"
            "}\n"
            "```\n\n"
            "The connection pool is exhausted — max 100 connections are all in use. "
            "This is blocking the trading desk from viewing portfolio positions.",
            "Portfolio API returning 500 with DatabaseConnectionPoolExhausted error. "
            "All 100 pooled connections are in use. Stack trace shows the issue is in "
            "PositionService.GetPositions. Request ID: a8f3b2c1-4d5e-6f7a-8b9c. "
            "Trading desk cannot view positions.",
        ],
        next_best_actions=[
            "Database connection pool exhausted on the portfolio API — check for "
            "connection leaks or long-running queries holding connections.",
            "Investigate the connection pool exhaustion on the portfolio API. May need "
            "to increase pool size or fix connection leak in PositionService.",
        ],
        remediation_steps=[
            [
                "Check the database for long-running queries or blocking sessions consuming connections",
                "Review the PositionService code for connection leak (missing Dispose/using patterns)",
                "Temporarily increase the connection pool size from 100 to 200 as a stopgap",
                "Restart the portfolio API service to release stuck connections",
                "Add connection pool monitoring and alerting to prevent future exhaustion",
            ],
        ],
        tags=["data-cleanup", "json-response", "api-error", "connection-pool"],
    ),
]
