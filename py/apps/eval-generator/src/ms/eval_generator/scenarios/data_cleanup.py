# Copyright (c) Microsoft. All rights reserved.
"""Data cleanup edge-case scenario definitions for eval dataset.

Covers data quality challenges that stress-test the triage model's ability
to extract the real support issue from noisy, malformed, or excessively
verbose input: long email threads, base64-encoded images, HTML-heavy emails,
garbled encoding, emoji-heavy chat, repeated content, massive signatures,
mixed languages, truncated messages, log dumps, excessive whitespace,
JSON/XML payloads, OCR artifacts, markdown artifacts, corrupted SMTP headers,
phone transcript filler, auto-generated notification noise,
pasted tabular data, and invisible Unicode characters.
"""

from ms.eval_generator.scenarios._base import ScenarioDefinition
from ms.eval_generator.scenarios._base import ScenarioGold

DATA_CLEANUP_SCENARIOS: list[ScenarioDefinition] = [
    # ──────────────────────────────────────────────────────────────────
    # 1. Long email thread with deeply nested RE:/FW: replies
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="dc-gen-001",
        subjects=(
            "Re: Re: Re: Re: Re: FW: VPN disconnects during market open",
            "RE: RE: RE: FW: FW: Internet keeps dropping — following up again",
        ),
        descriptions=(
            "Just following up again — the VPN still drops every morning between 09:28 and"
            " 09:32 ET. I have to reconnect 3-4 times before it stabilizes.\n\n"
            "--- Original Message ---\n"
            "From: Marco Bellini <marco.bellini@contoso.com>\n"
            "Sent: Monday, March 10, 2026 8:45 AM\n"
            "To: IT Support <itsupport@contoso.com>\n"
            "Subject: Re: Re: Re: Re: FW: VPN disconnects during market open\n\n"
            "Still happening today. I ran the diagnostics you asked for — attached.\n\n"
            "--- Original Message ---\n"
            "From: IT Support <itsupport@contoso.com>\n"
            "Sent: Friday, March 7, 2026 4:10 PM\n"
            "Subject: Re: Re: Re: FW: VPN disconnects during market open\n\n"
            "Could you run 'netsh wlan show all' and send us the output? Also confirm your"
            " GlobalProtect client version.\n\n"
            "--- Original Message ---\n"
            "From: Marco Bellini <marco.bellini@contoso.com>\n"
            "Sent: Friday, March 7, 2026 9:05 AM\n"
            "Subject: Re: Re: FW: VPN disconnects during market open\n\n"
            "It happened again. I lost the VPN tunnel at exactly 09:30. My colleague says his"
            " works fine so I don't think it's the office network.\n\n"
            "--- Original Message ---\n"
            "From: IT Support <itsupport@contoso.com>\n"
            "Sent: Thursday, March 6, 2026 3:00 PM\n"
            "Subject: Re: FW: VPN disconnects during market open\n\n"
            "Can you tell us which office and floor you're on? Wi-Fi or Ethernet?\n\n"
            "--- Original Message ---\n"
            "From: Marco Bellini <marco.bellini@contoso.com>\n"
            "Sent: Thursday, March 6, 2026 9:35 AM\n"
            "Subject: FW: VPN disconnects during market open\n\n"
            "My VPN keeps disconnecting every morning around market open. I'm on the 5th floor,"
            " Building 3, New York office, using Wi-Fi.",
            "This is my third follow-up. Still no resolution.\n\n"
            "On Mon, Mar 10, 2026 at 2:15 PM IT Support <itsupport@contoso.com> wrote:\n"
            "> We've escalated this to the network team.\n"
            "> They should reach out within 24 hours.\n\n"
            "On Fri, Mar 7, 2026 at 9:00 AM I wrote:\n"
            "> The connection drops every day around the same time.\n"
            "> I'm getting packet loss on the wireless — about 15% according to ping.\n\n"
            "On Thu, Mar 6, 2026 at 4:00 PM IT Support wrote:\n"
            "> Thanks for reporting. Can you confirm your laptop model and OS?\n\n"
            "Original issue: My internet connection drops multiple times per day. I'm on Floor 5,"
            " Building 3, New York office.",
        ),
        gold=ScenarioGold(
            category="Network & Connectivity",
            priority="P2",
            assigned_team="Network Operations",
            needs_escalation=False,
            missing_information=("application_version",),
            next_best_action="Investigate recurring VPN disconnects correlated with 09:30 ET market-open traffic"
            " spike for user on 5th floor Wi-Fi — check AP congestion and VPN gateway logs",
            remediation_steps=(
                "Check VPN gateway logs for the user's session drops during 09:25-09:35 ET",
                "Correlate with wireless controller data for 5th floor AP utilization",
                "Verify VPN split-tunnel configuration and MTU settings on the client",
                "If Wi-Fi congestion confirmed, move user to Ethernet or a less congested AP",
                "Provide updated GlobalProtect client if version is outdated",
            ),
        ),
        tags=("data-cleanup", "long-email", "nested-thread"),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 2. Base64-encoded image data inline in email body
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="dc-gen-002",
        subjects=(
            "Monitor flickering — screenshot attached inline",
            "Display issues with docking station (see embedded image)",
        ),
        descriptions=(
            "My external monitor keeps flickering every few seconds. Here is a screenshot:\n\n"
            "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9Q"
            "DwADhgGAWjR9awAAAABJRU5ErkJggg==\n"
            "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAoAAAAKCAYAAACNMs+9AAAAFUlEQVQYV2P8z8BQ"
            "z0AEYBxVOHIVAvcHBQHzKSECAAAAAElFTkSuQmCC\n\n"
            "It happens about every 10 seconds and makes it impossible to work. The monitor"
            " works fine when connected directly via HDMI without the dock.",
            "External display via USB-C dock flickers and goes black for 2-3 seconds. I tried"
            " to embed a photo but my email client pasted raw data:\n\n"
            "[base64 data: /9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAgGBgcGBQgHBwcJCQgKDBQNDAsLDBkSEw8U"
            "HRofHh0aHBwgJC4nICIsIxwcKDcpLDAxNDQ0Hyc5PTgyPC4zNDL/FAKEBASE64CONTINUES...]\n\n"
            "The dock is a Lenovo ThinkPad USB-C Dock Gen 2. Monitor is Dell U2722D.",
        ),
        gold=ScenarioGold(
            category="Hardware & Peripherals",
            priority="P3",
            assigned_team="Endpoint Engineering",
            needs_escalation=False,
            missing_information=("device_info", "error_message"),
            next_best_action="Ignore base64 image data and focus on the hardware issue: monitor flickering through"
            " docking station — likely a dock firmware or cable issue",
            remediation_steps=(
                "Update the docking station firmware to the latest version",
                "Test with a different USB-C or Thunderbolt cable",
                "Try a different video output port on the dock (DisplayPort vs HDMI)",
                "If the issue persists, test with a replacement docking station",
                "Verify display driver is up to date on the laptop",
            ),
        ),
        tags=("data-cleanup", "base64", "inline-image"),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 3. HTML-heavy email with style tags, CSS, and formatting noise
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="dc-gen-003",
        subjects=(
            "Teams crashes every time I share my screen",
            "Microsoft Teams screen share not working",
        ),
        descriptions=(
            '<div style="font-family:Calibri,sans-serif;font-size:11pt;color:#333">'
            "<p><b>Hi IT,</b></p>"
            '<p style="margin-top:0;margin-bottom:12px">Every time I try to share my screen in'
            " Teams it freezes for ~10 seconds and then crashes. I get a generic error dialog"
            " with &quot;Something went wrong&quot;.</p>"
            "<p>I&rsquo;ve tried:</p>"
            "<ul><li>Restarting Teams</li><li>Clearing the cache</li>"
            "<li>Reinstalling</li></ul>"
            '<p style="color:#666;font-size:9pt">Sent from Outlook for Windows</p>'
            '<p style="color:#999;font-size:8pt">CONFIDENTIAL: This email and any files'
            " transmitted with it are confidential and intended solely for the individual to"
            " whom they are addressed. If you received this in error, please delete.</p>"
            "</div>",
            "<!DOCTYPE html><html><head><style>body{font-family:Arial;font-size:14px}</style>"
            "</head><body><p>Teams screen sharing is broken. When I click &ldquo;Share"
            " content&rdquo; the entire application freezes and eventually crashes back to"
            " the desktop.</p><p>This started after the latest Teams update. Version:"
            " 24326.1210.3137.5765.</p>"
            "<br><br><p>---</p>"
            '<p style="font-size:8pt;color:#aaa">Disclaimer: This message is confidential.'
            " If you are not the intended recipient, you are notified that any use,"
            " dissemination, distribution, or copying is strictly prohibited.</p>"
            "</body></html>",
        ),
        gold=ScenarioGold(
            category="Software & Applications",
            priority="P3",
            assigned_team="Enterprise Applications",
            needs_escalation=False,
            missing_information=("device_info", "steps_to_reproduce"),
            next_best_action="Investigate Teams screen sharing crash after recent update — extract the real issue"
            " from HTML formatting noise",
            remediation_steps=(
                "Check if the Teams version 24326.1210.3137.5765 has known screen-sharing bugs",
                "Clear the Teams cache completely and restart",
                "Check GPU driver compatibility with Teams hardware acceleration",
                "Test screen sharing with hardware acceleration disabled",
                "If the issue persists, roll back to the previous Teams version",
            ),
        ),
        tags=("data-cleanup", "html-heavy", "formatting-noise"),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 4. Garbled encoding / mojibake text
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="dc-gen-004",
        subjects=(
            "Can't login to SAP \u2014 error message garbled",
            "SAP login failure \xe2\u20ac\u201c strange characters in error",
        ),
        descriptions=(
            "I can\xe2\u20ac\u2122t log in to SAP since this morning. The error message says:\n\n"
            "\xe2\u20ac\u0153Authentication failed: invalid credentials or account locked"
            "\xe2\u20ac\x9d\n\n"
            "I\xe2\u20ac\u2122ve tried resetting my password via the self-service portal but it"
            " still doesn\xe2\u20ac\u2122t work. My colleague sitting next to me can log in fine."
            " Could my account be locked? I\xe2\u20ac\u2122m in the Singapore office, 3rd floor.",
            "Getting this when trying to open SAP:\n\n"
            "\xc3\xa2\xe2\u201a\xac\xc5\u201cError 403: Access denied. Contact your system"
            " administrator\xc3\xa2\xe2\u201a\xac\xc2\n\n"
            "It was working yesterday. Nothing changed on my end. Running Windows 11 with"
            " Chrome 124.",
        ),
        gold=ScenarioGold(
            category="Access & Authentication",
            priority="P2",
            assigned_team="Identity & Access Management",
            needs_escalation=False,
            missing_information=("error_message", "authentication_method"),
            next_best_action="Investigate SAP login failure — extract real error from garbled encoding."
            " Likely account lockout or credential issue",
            remediation_steps=(
                "Check the user's account lockout status in the SAP identity provider",
                "Verify the password reset completed successfully in the directory",
                "Check for any conditional access policies blocking Singapore office logins",
                "Clear browser cache and cookies for the SAP domain",
                "If account is locked, unlock and verify credentials manually",
            ),
        ),
        tags=("data-cleanup", "garbled-encoding", "mojibake"),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 5. Emoji-heavy chat message with minimal structure
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="dc-gen-005",
        subjects=(
            "🚨🚨🚨 HELP wifi down!!! 🚨🚨🚨",
            "😡😡 internet not working AGAIN 😡😡",
        ),
        descriptions=(
            "🔥🔥🔥 wifi is DEAD again!!!!! 🔥🔥🔥\n\n"
            "literally cant do anything rn 😤😤😤\n"
            "my laptop says connected but nothing loads 🤷‍♂️🤷‍♂️\n"
            "tried restarting wifi like 5 times already 😩\n"
            "pls help asap im losing my mind 🙏🙏🙏\n\n"
            "floor 2 building 1 london btw 📍",
            "omg 😱😱 the internet is sooooo slow i can barely open email 📧\n"
            "its been like this all morning ⏰\n"
            "im on wifi 📶 floor 2 london office 🏢\n"
            "literally everyone on the floor is complaining 😤😤\n"
            "PLEASE FIX 🙏🙏🙏🙏🙏",
        ),
        gold=ScenarioGold(
            category="Network & Connectivity",
            priority="P2",
            assigned_team="Network Operations",
            needs_escalation=False,
            missing_information=("device_info", "affected_users"),
            next_best_action="Investigate Wi-Fi outage on Floor 2 Building 1 London — extract the real issue"
            " from emoji-heavy informal chat message",
            remediation_steps=(
                "Check wireless controller for AP status on Floor 2 Building 1 London",
                "Verify DHCP lease availability and DNS resolution on that subnet",
                "Check if other users on the same floor confirm the outage",
                "Restart the affected access points if they show errors",
                "Escalate to network engineering if the AP hardware is unresponsive",
            ),
        ),
        tags=("data-cleanup", "emoji-heavy", "informal-chat"),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 6. Massive email signature block dwarfing the actual content
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="dc-gen-006",
        subjects=(
            "Outlook freezing when opening attachments",
            "Can't open PDF attachments in Outlook",
        ),
        descriptions=(
            "Outlook freezes for 30+ seconds whenever I try to open a PDF attachment. I have"
            " to force-close it every time.\n\n"
            "---\n"
            "Best regards,\n"
            "Jonathan R. Whitfield III\n"
            "Senior Vice President, Institutional Fixed Income\n"
            "Contoso Financial Services\n"
            "One Contoso Plaza, 42nd Floor\n"
            "New York, NY 10005\n"
            "Direct: +1 (212) 555-0147 | Mobile: +1 (917) 555-0293\n"
            "Fax: +1 (212) 555-0148\n"
            "Email: jonathan.whitfield@contoso.com\n"
            "Bloomberg: JWHITFIELD@CONTOSO <GO>\n\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            "CONFIDENTIALITY NOTICE: This email message, including any attachments, is for"
            " the sole use of the intended recipient(s) and may contain confidential and"
            " privileged information. Any unauthorized review, use, disclosure, or distribution"
            " is prohibited. If you are not the intended recipient, please contact the sender"
            " by reply email and destroy all copies of the original message. This communication"
            " does not constitute an offer or acceptance of any investment service or product"
            " in any jurisdiction. Contoso Financial Services is regulated by the SEC, FCA, and"
            " MAS. Member FINRA/SIPC.\n"
            "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
            "🌿 Please consider the environment before printing this email.\n"
            "📊 Bloomberg Terminal: CONTOSO <GO>\n"
            "🔒 Encrypted with TLS 1.3",
            "PDF attachments won't open in Outlook. It just hangs.\n\n"
            "--\n"
            "Jonathan R. Whitfield III | SVP Institutional Fixed Income | Contoso Financial"
            " Services | +1 (212) 555-0147 | jonathan.whitfield@contoso.com | Bloomberg:"
            " JWHITFIELD@CONTOSO <GO> | CONFIDENTIAL: This message is for the intended"
            " recipient only. If received in error, delete immediately. Contoso Financial"
            " Services is regulated by SEC, FCA, MAS. Member FINRA/SIPC. Please consider"
            " the environment before printing.",
        ),
        gold=ScenarioGold(
            category="Software & Applications",
            priority="P3",
            assigned_team="Enterprise Applications",
            needs_escalation=False,
            missing_information=("application_version", "error_message"),
            next_best_action="Investigate Outlook freezing when opening PDF attachments — ignore the massive"
            " email signature and focus on the attachment-handling issue",
            remediation_steps=(
                "Check if the Outlook version has a known issue with PDF preview rendering",
                "Disable the PDF preview handler in Outlook Trust Center settings",
                "Clear the Outlook temporary attachment cache",
                "Test opening the same PDFs from Explorer to rule out file corruption",
                "If the issue persists, repair the Office installation",
            ),
        ),
        tags=("data-cleanup", "massive-signature", "noise-ratio"),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 7. Truncated / cut-off message
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="dc-gen-007",
        subjects=(
            "SharePoint permission error when accessing Q1 repo",
            "Can't access shared documents on SharePoint",
        ),
        descriptions=(
            "I'm getting an 'Access Denied' error when trying to access the Q1 Financial"
            " Reports folder on SharePoint. I need access to complete the quarterly audit. My"
            " manager approved it last week but I still can",
            "Hi, I can't open files on the Compliance team SharePoint site. When I click on the"
            " documents library it says 'Sorry, you don't have access to this page.' I was able"
            " to access it until yester",
        ),
        gold=ScenarioGold(
            category="Data & Storage",
            priority="P3",
            assigned_team="Data Platform",
            needs_escalation=False,
            missing_information=("affected_system", "error_message"),
            next_best_action="Investigate SharePoint access denial — message appears truncated but core issue is"
            " clear: user needs permissions restored or granted to a document library",
            remediation_steps=(
                "Check the user's SharePoint permissions for the Q1 Financial Reports site",
                "Verify manager's access request was submitted and processed",
                "Check if a recent permissions change removed the user's access group",
                "Grant appropriate access level (Read/Contribute) to the document library",
                "Verify the user can access the site after the permission change",
            ),
        ),
        tags=("data-cleanup", "truncated-message", "incomplete-input"),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 8. Log dump / stack trace embedded in ticket body
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="dc-gen-008",
        subjects=(
            "Application crashes with stack trace — see below",
            "Internal trading app keeps crashing — error logs attached",
        ),
        descriptions=(
            "The internal trading application keeps crashing. Here are the error logs:\n\n"
            "2026-03-18 09:15:23.456 [ERROR] com.contoso.trading.OrderService - "
            "Unhandled exception in order processing pipeline\n"
            "java.lang.OutOfMemoryError: Java heap space\n"
            "    at com.contoso.trading.OrderService.processOrder(OrderService.java:247)\n"
            "    at com.contoso.trading.OrderQueue.poll(OrderQueue.java:89)\n"
            "    at com.contoso.trading.ExecutionEngine.run(ExecutionEngine.java:156)\n"
            "    at java.base/java.lang.Thread.run(Thread.java:834)\n"
            "Caused by: java.lang.OutOfMemoryError: Java heap space\n"
            "    at java.base/java.util.Arrays.copyOf(Arrays.java:3721)\n"
            "    at java.base/java.util.ArrayList.grow(ArrayList.java:265)\n"
            "    ... 14 more\n\n"
            "2026-03-18 09:15:23.789 [WARN] com.contoso.trading.HealthCheck - Heap usage"
            " at 98.7%, GC overhead limit exceeded\n\n"
            "This started happening about 2 hours ago. Traders can't submit orders.",
            "The order management system crashed with this error:\n\n"
            'Exception in thread "main" java.lang.OutOfMemoryError: GC overhead limit'
            " exceeded\n"
            "    at com.contoso.oms.MarketDataFeed.consume(MarketDataFeed.java:312)\n"
            "    at com.contoso.oms.RealTimeEngine.tick(RealTimeEngine.java:178)\n\n"
            "Multiple traders affected. Can't submit or modify orders since 9 AM.",
        ),
        gold=ScenarioGold(
            category="Software & Applications",
            priority="P1",
            assigned_team="Enterprise Applications",
            needs_escalation=True,
            missing_information=("environment_details",),
            next_best_action="Critical: trading application down due to Java OutOfMemoryError — affects order"
            " processing for multiple traders, requires immediate heap/GC investigation",
            remediation_steps=(
                "Restart the trading application with increased JVM heap size as an immediate fix",
                "Check application memory trends to identify a potential memory leak",
                "Review recent code deployments or configuration changes that may have caused the issue",
                "Monitor GC logs after restart to verify the heap is stable",
                "Coordinate with the trading desk on the expected downtime window",
            ),
        ),
        tags=("data-cleanup", "log-dump", "stack-trace"),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 9. Mixed languages / multilingual content
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="dc-gen-009",
        subjects=(
            "プリンターが動かない / Printer not working",
            "Imprimante en panne — printer broken Floor 4",
        ),
        descriptions=(
            "Hello IT team,\n\n"
            "プリンターが今朝から動きません。エラーメッセージが表示されます。\n"
            "(Translation: The printer has not been working since this morning. An error"
            " message is displayed.)\n\n"
            "The printer is on Floor 7 of the Singapore office. It's the HP Color LaserJet"
            " near the east wing conference rooms. The display shows 紙詰まり which I think"
            " means paper jam but I cleared the tray and it still won't print.",
            "Bonjour,\n\n"
            "L'imprimante du 4ème étage ne fonctionne plus depuis ce matin. J'ai essayé de"
            " la redémarrer mais rien ne change.\n\n"
            "Sorry, switching to English — the printer on Floor 4 London office has been down"
            " all morning. Paper jam indicator is on but I've cleared all the trays. Other"
            " people on this floor are also unable to print.",
        ),
        gold=ScenarioGold(
            category="Hardware & Peripherals",
            priority="P3",
            assigned_team="Endpoint Engineering",
            needs_escalation=False,
            missing_information=("error_message", "device_info"),
            next_best_action="Investigate persistent printer paper jam indication after clearing trays —"
            " extract core issue from multilingual ticket content",
            remediation_steps=(
                "Physically inspect the printer for any remaining paper fragments in the feed path",
                "Check the paper jam sensor for debris or misalignment",
                "Power cycle the printer completely (unplug, wait 30 seconds, replug)",
                "If the paper jam indicator persists, check for a hardware sensor fault",
                "If multiple printers affected, check print server connectivity",
            ),
        ),
        tags=("data-cleanup", "mixed-languages", "multilingual"),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 10. Excessive whitespace and blank lines
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="dc-gen-010",
        subjects=(
            "laptop     screen    cracked",
            "Screen broken   need replacement",
        ),
        descriptions=(
            "Hi\n\n\n\n\n\n\n"
            "My   laptop   screen   is   cracked.\n\n\n\n\n"
            "It   happened   when   I   dropped   it   yesterday.\n\n\n\n\n\n\n\n"
            "I   can   barely   see   anything   on   the   display.\n\n\n\n\n"
            "I   need   a   replacement   screen   or   a   new   laptop.\n\n\n\n\n\n\n\n"
            "Thanks\n\n\n\n\n\n\n\n\n\n\n\n\n\n",
            "laptop screen is cracked              need new one\n\n\n\n\n\n\n\n\n\n"
            "dropped it this morning              display is barely visible\n\n\n\n"
            "                                     \n\n\n\n"
            "please help                          \n\n\n\n\n\n\n\n",
        ),
        gold=ScenarioGold(
            category="Hardware & Peripherals",
            priority="P3",
            assigned_team="Endpoint Engineering",
            needs_escalation=False,
            missing_information=("device_info", "business_impact"),
            next_best_action="Process laptop screen replacement request — extract the hardware issue from"
            " excessively whitespace-padded message",
            remediation_steps=(
                "Verify the laptop model and warranty status in the asset inventory",
                "Determine if the screen can be repaired or if a full replacement is needed",
                "Issue a loaner laptop while the repair is being processed",
                "Create a hardware replacement request through the procurement system",
                "Schedule pickup or drop-off with the user for the damaged device",
            ),
        ),
        tags=("data-cleanup", "excessive-whitespace", "sparse-content"),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 11. Repeated / duplicated content (copy-paste stutter)
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="dc-gen-011",
        subjects=(
            "Password reset not working Password reset not working",
            "Can't reset password — tried multiple times",
        ),
        descriptions=(
            "I need to reset my password but the self-service portal keeps giving an error.\n"
            "I need to reset my password but the self-service portal keeps giving an error.\n"
            "I need to reset my password but the self-service portal keeps giving an error.\n\n"
            "When I click 'Reset Password' it just spins and then says 'An error occurred.'\n"
            "When I click 'Reset Password' it just spins and then says 'An error occurred.'\n\n"
            "I've tried three different browsers. Same result every time.\n"
            "I've tried three different browsers. Same result every time.\n\n"
            "My account might be locked. I was traveling last week and may have triggered"
            " a geo-location policy.",
            "Password reset portal broken.\n"
            "Password reset portal broken.\n"
            "Password reset portal broken.\n"
            "Password reset portal broken.\n\n"
            "Error message: 'Unable to verify identity. Please contact your administrator.'\n"
            "Error message: 'Unable to verify identity. Please contact your administrator.'\n\n"
            "I'm in the London office. Need access to work systems urgently.",
        ),
        gold=ScenarioGold(
            category="Access & Authentication",
            priority="P2",
            assigned_team="Identity & Access Management",
            needs_escalation=False,
            missing_information=("authentication_method",),
            next_best_action="Investigate self-service password reset failure — deduplicate the repeated content"
            " and address the underlying identity verification or account lockout issue",
            remediation_steps=(
                "Check if the user's account is locked in Entra ID",
                "Verify the self-service password reset (SSPR) configuration for the user",
                "Check if the geo-location policy flagged the travel-based login attempts",
                "Manually reset the password and provide temporary credentials",
                "Ensure the user re-registers for SSPR after the reset if MFA tokens are stale",
            ),
        ),
        tags=("data-cleanup", "repeated-content", "copy-paste-stutter"),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 12. JSON monitoring alert pasted as ticket body
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="dc-gen-012",
        subjects=(
            "ALERT: Database connection pool exhausted",
            "Monitoring alert — DB pool at capacity",
        ),
        descriptions=(
            '{"alert_id":"MON-2026-0318-0915","severity":"critical","source":"azure-monitor",'
            '"resource":"contoso-prod-sql-01","metric":"connection_pool_usage","value":100.0,'
            '"threshold":85.0,"unit":"percent","timestamp":"2026-03-18T09:15:00Z","message":'
            '"Connection pool exhausted on contoso-prod-sql-01. Active connections: 500/500.'
            " Queue depth: 47. Oldest queued request: 12.3s. Affected services:"
            ' order-service, risk-engine, market-data-feed.","labels":{"environment":"production",'
            '"region":"eastus2","team":"data-platform","escalation_tier":"L2"},"runbook":'
            '"https://runbooks.contoso.com/db/connection-pool-exhaustion"}',
            "Azure Monitor fired this alert:\n\n"
            "Resource: contoso-prod-sql-01\n"
            "Metric: connection_pool_usage = 100%\n"
            "Threshold: 85%\n"
            "Active connections: 500/500\n"
            "Queue depth: 47\n"
            "Affected: order-service, risk-engine, market-data-feed\n\n"
            "This is impacting trade execution. Multiple services can't connect to the"
            " database.",
        ),
        gold=ScenarioGold(
            category="Data & Storage",
            priority="P1",
            assigned_team="Data Platform",
            needs_escalation=True,
            missing_information=(),
            next_best_action="Critical: production database connection pool exhausted on contoso-prod-sql-01"
            " — parse the JSON monitoring alert and address the capacity issue immediately",
            remediation_steps=(
                "Identify and terminate idle or leaked database connections",
                "Increase the connection pool limit temporarily if server resources allow",
                "Check for long-running queries or deadlocks consuming connections",
                "Investigate which service is leaking connections (order-service, risk-engine, etc.)",
                "Follow the runbook at https://runbooks.contoso.com/db/connection-pool-exhaustion",
            ),
        ),
        tags=("data-cleanup", "json-payload", "monitoring-alert"),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 13. Corrupted SMTP headers / MIME boundaries in body
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="dc-gen-013",
        subjects=(
            "Email delivery issues — messages not arriving",
            "Emails to external clients bouncing back",
        ),
        descriptions=(
            "Content-Type: multipart/alternative;\n"
            '  boundary="----=_Part_12345_67890.1710752400000"\n'
            "MIME-Version: 1.0\n"
            "X-Mailer: Microsoft Outlook 16.0\n"
            "X-MS-Exchange-Organization-AuthSource: CONTOSO-EX01.contoso.local\n\n"
            "------=_Part_12345_67890.1710752400000\n"
            "Content-Type: text/plain; charset=UTF-8\n\n"
            "My emails to external clients are bouncing back with an NDR. The error says"
            " '550 5.7.1 Unable to relay'. This started after the Exchange maintenance window"
            " last weekend. I've tried sending from both Outlook and OWA. About 10 emails"
            " to different external domains are stuck in my outbox.\n\n"
            "------=_Part_12345_67890.1710752400000--",
            "From: MAILER-DAEMON@contoso.com\n"
            "Subject: Undeliverable: Q1 Report to Client\n"
            "X-MS-Exchange-Organization-SCL: -1\n\n"
            "Delivery has failed to these recipients:\n"
            "john.doe@externalclient.com\n\n"
            "Remote Server returned '550 5.7.1 Unable to relay for"
            " john.doe@externalclient.com'\n\n"
            "I'm getting these bounce-backs on every external email I send. Internal emails"
            " work fine.",
        ),
        gold=ScenarioGold(
            category="Software & Applications",
            priority="P2",
            assigned_team="Enterprise Applications",
            needs_escalation=False,
            missing_information=("configuration_details",),
            next_best_action="Investigate external email relay failure ('550 5.7.1 Unable to relay') that"
            " started after Exchange maintenance — extract the issue from SMTP header noise",
            remediation_steps=(
                "Check Exchange send connector configuration for external relay permissions",
                "Verify the Exchange server's relay settings were not altered during maintenance",
                "Check if the server's IP is on any email blocklists or RBLs",
                "Review Exchange transport logs for the failed delivery attempts",
                "Test external relay with a manual SMTP session to isolate the failure point",
            ),
        ),
        tags=("data-cleanup", "smtp-headers", "mime-boundaries"),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 14. Phone transcript with filler words and speech artifacts
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="dc-gen-014",
        subjects=(
            "Transcription: caller reports laptop won't boot",
            "Phone call — laptop power issue",
        ),
        descriptions=(
            "[Auto-transcription from call at 2026-03-18 09:45 AM]\n\n"
            "Caller: Yeah, uh, hi, so, um, my laptop — it won't, uh, turn on. I mean,"
            " I press the power button and, you know, nothing happens. Like, the screen"
            " stays completely black. Um, I tried, uh, holding the button down for like"
            " thirty seconds? Still nothing. Oh wait, actually, um, there's a tiny light"
            " that blinks once and then, uh, goes off. Yeah. So it's, like, completely"
            " dead I think? I dunno. It was working fine, uh, yesterday.\n\n"
            "Agent: [inaudible] ...model of the laptop?\n\n"
            "Caller: It's, um, uh, a ThinkPad something. T14 maybe? Or T480? I'm not sure."
            " It's the one IT gave me when I started. Black, standard issue.\n\n"
            "[End of transcription]",
            "[Phone transcript — 9:52 AM]\n\n"
            "User: So like my computer won't start at all, right, and um I need it for a"
            " client meeting at 11. Can someone, like, come take a look or give me a loaner"
            " or something? The power light does this blinking thing — blink blink blink and"
            " then nothing. I tried plugging it in, different outlet, same thing.\n\n"
            "[Background noise] ...yeah sorry, what? Oh, it's a Lenovo. ThinkPad. Black one."
            " Standard issue from IT.",
        ),
        gold=ScenarioGold(
            category="Hardware & Peripherals",
            priority="P3",
            assigned_team="Endpoint Engineering",
            needs_escalation=False,
            missing_information=("device_info",),
            next_best_action="Investigate laptop power failure — extract the hardware symptoms from phone"
            " transcript noise: power button unresponsive, LED blinks once then off",
            remediation_steps=(
                "Try a hard reset by removing the battery (if removable) and holding power for 30 seconds",
                "Test with a known-good power adapter to rule out charger failure",
                "Check if the blinking LED pattern indicates a specific diagnostic code",
                "If the device is unresponsive, arrange a loaner laptop for the client meeting",
                "Submit a hardware repair or replacement request through the asset management system",
            ),
        ),
        tags=("data-cleanup", "phone-transcript", "speech-artifacts"),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 15. Auto-generated notification noise surrounding a real issue
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="dc-gen-015",
        subjects=(
            "FW: [JIRA] [CONTOSO-4829] Status changed: Open → In Progress → Blocked",
            "FW: Automated alert — disk space critical on file server",
        ),
        descriptions=(
            "---------- Forwarded message ----------\n"
            "From: JIRA <jira@contoso.com>\n"
            "Date: Mon, Mar 18, 2026 at 8:30 AM\n"
            "Subject: [CONTOSO-4829] Status changed\n\n"
            "[JIRA] Issue Updated: CONTOSO-4829\n"
            "Status: Open → In Progress → Blocked\n"
            "Assignee: data-platform-team\n"
            "Priority: High\n"
            "Labels: production, database, Q1-release\n\n"
            "Comment by System Admin (Mar 18, 2026 8:30 AM):\n"
            "Blocked — file server FS-NYC-03 is at 98% capacity. We can't complete the"
            " database migration until space is freed. ETL jobs are also failing because"
            " temp files can't be written.\n\n"
            "--- End of JIRA notification ---\n\n"
            "Hi IT, the file server is almost full and it's blocking our database work."
            " Can someone clean up or expand the storage?",
            "[Automated Alert] WARNING: Disk utilization on FS-NYC-03 has exceeded 95%.\n"
            "Current: 98.2% (14.73 TB / 15.0 TB)\n"
            "Threshold: 95%\n"
            "Trend: +2.1 TB in last 7 days\n"
            "Impact: ETL pipeline failures, JIRA CONTOSO-4829 blocked\n\n"
            "Please investigate and free up space. The Q1 database migration is stuck.",
        ),
        gold=ScenarioGold(
            category="Data & Storage",
            priority="P2",
            assigned_team="Data Platform",
            needs_escalation=False,
            missing_information=("configuration_details",),
            next_best_action="Investigate critical disk space on FS-NYC-03 (98% full) — blocking database"
            " migration and ETL jobs. Extract real issue from JIRA/monitoring notification noise",
            remediation_steps=(
                "Identify and remove or archive large temporary files on FS-NYC-03",
                "Check for stale ETL temp files, old database backups, or log files consuming space",
                "If cleanup is insufficient, request a storage expansion or add a volume",
                "Monitor disk growth trend to prevent recurrence",
                "Unblock the JIRA ticket CONTOSO-4829 after space is freed",
            ),
        ),
        tags=("data-cleanup", "auto-notification", "jira-noise"),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 16. Markdown formatting artifacts from rich-text copy-paste
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="dc-gen-016",
        subjects=(
            "**URGENT** VPN ~~issues~~ _complete failure_ since morning",
            "# Help: Can't connect to company network remotely",
        ),
        descriptions=(
            "## Issue Description\n\n"
            "The **GlobalProtect VPN** is _completely broken_ for me since this morning.\n\n"
            "### What I've tried:\n"
            "- [x] Restarted my laptop\n"
            "- [x] Reinstalled GlobalProtect\n"
            "- [ ] ~~Checked firewall~~ (don't know how)\n"
            "- [x] Tried different Wi-Fi networks\n\n"
            "### Error message:\n"
            "```\n"
            "Error: Gateway authentication failed\n"
            "Reason: Certificate validation error\n"
            "Code: CERT_EXPIRED_0x800B0101\n"
            "```\n\n"
            "### Impact:\n"
            "> I can't access **any** internal systems. Completely blocked from working.\n\n"
            "| Attempt | Time | Result |\n"
            "|---------|------|--------|\n"
            "| 1 | 8:30 AM | Failed |\n"
            "| 2 | 9:15 AM | Failed |\n"
            "| 3 | 10:00 AM | Failed |\n\n"
            "Please help ASAP! 🙏",
            "# VPN Won't Connect\n\n"
            "Getting `CERT_EXPIRED_0x800B0101` when trying to connect to GlobalProtect.\n"
            "Tried on both home Wi-Fi and phone hotspot — same error.\n\n"
            "**Blocking all work** since 8:30 this morning.",
        ),
        gold=ScenarioGold(
            category="Network & Connectivity",
            priority="P2",
            assigned_team="Network Operations",
            needs_escalation=False,
            missing_information=("device_info",),
            next_best_action="Investigate VPN authentication failure with CERT_EXPIRED error — likely an expired"
            " VPN gateway or client certificate. Parse the markdown formatting to extract details",
            remediation_steps=(
                "Check if the GlobalProtect VPN gateway certificate has expired",
                "Verify the client-side certificate store for expired or revoked certificates",
                "If the gateway cert is expired, coordinate an emergency renewal with the PKI team",
                "Push an updated certificate to the client via Intune if it's a client-side issue",
                "Provide the user with a temporary workaround (e.g., web-based VPN portal) if available",
            ),
        ),
        tags=("data-cleanup", "markdown-artifacts", "rich-text"),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 17. Pasted spreadsheet / tabular data in email body
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="dc-gen-017",
        subjects=(
            "Multiple workstations not connecting to network — see list",
            "Network issues for 12 workstations on Floor 6",
        ),
        descriptions=(
            "Several workstations on Floor 6 can't connect to the network today. Here's the"
            " full list:\n\n"
            "Hostname\tUser\tIP\tStatus\tNotes\n"
            "WS-NYC-0601\tJ. Park\t10.1.6.101\tNo connectivity\tEthernet light off\n"
            "WS-NYC-0602\tR. Singh\t10.1.6.102\tIntermittent\tDrops every 5 min\n"
            "WS-NYC-0603\tM. Brown\tDHCP fail\tNo IP assigned\tCable replaced, same issue\n"
            "WS-NYC-0604\tA. Petrov\t10.1.6.104\tNo connectivity\tSwitch port dead?\n"
            "WS-NYC-0605\tL. Chen\t10.1.6.105\tIntermittent\tSlow, 50% packet loss\n"
            "WS-NYC-0606\tK. Okafor\t10.1.6.106\tNo connectivity\tSame switch as 0604\n"
            "WS-NYC-0607\tD. Müller\tDHCP fail\tNo IP assigned\tTried static, no change\n"
            "WS-NYC-0608\tS. Tanaka\t10.1.6.108\tIntermittent\tDNS resolution failing\n"
            "WS-NYC-0609\tP. Moreno\t10.1.6.109\tNo connectivity\tEthernet light off\n"
            "WS-NYC-0610\tF. Ahmed\t10.1.6.110\tNo connectivity\tSame switch as 0604\n"
            "WS-NYC-0611\tH. Kim\t10.1.6.111\tIntermittent\tWorks on Wi-Fi\n"
            "WS-NYC-0612\tT. Nowak\tDHCP fail\tNo IP assigned\tAll three on same patch panel\n\n"
            "This looks like a switch or patch panel failure on Floor 6.",
            "12 workstations on Floor 6 NYC went offline this morning. Multiple switch ports"
            " appear dead. DHCP is failing for some, others have no link at all. Suspected"
            " switch failure — the affected machines all connect to the same patch panel.",
        ),
        gold=ScenarioGold(
            category="Network & Connectivity",
            priority="P1",
            assigned_team="Network Operations",
            needs_escalation=True,
            missing_information=(),
            next_best_action="Investigate suspected switch or patch panel failure on Floor 6 NYC affecting 12"
            " workstations — parse the tabular data for diagnostics patterns",
            remediation_steps=(
                "Identify the common switch and patch panel serving the affected ports",
                "Check the switch management interface for port errors, CRC errors, or module failures",
                "If the switch is unresponsive, failover to a backup or replace the unit",
                "Verify patch panel connections for physical damage or loose cabling",
                "Move critical users to alternative network drops or Wi-Fi as a temporary measure",
            ),
        ),
        tags=("data-cleanup", "tabular-data", "pasted-spreadsheet"),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 18. vCalendar / ICS data embedded in ticket
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="dc-gen-018",
        subjects=(
            "Calendar invite not working — meeting room double booked",
            "FW: Meeting invite — room booking conflict",
        ),
        descriptions=(
            "I'm trying to book Conference Room 12A for a client meeting but it says the room"
            " is already booked. I can see the conflicting invite:\n\n"
            "BEGIN:VCALENDAR\n"
            "VERSION:2.0\n"
            "PRODID:-//Microsoft Corporation//Outlook 16.0 MIMEDIR//EN\n"
            "BEGIN:VEVENT\n"
            "DTSTART:20260318T140000Z\n"
            "DTEND:20260318T150000Z\n"
            "SUMMARY:Team Standup (recurring)\n"
            "LOCATION:Conference Room 12A\n"
            "ORGANIZER:MAILTO:nobody@contoso.com\n"
            "STATUS:CONFIRMED\n"
            "END:VEVENT\n"
            "END:VCALENDAR\n\n"
            "This 'Team Standup' meeting was cancelled weeks ago but the room booking"
            " wasn't removed. Can someone free up the room? My client meeting is at 2 PM today.",
            "Room 12A shows as booked for a cancelled recurring meeting. The ICS data from"
            " the booking system shows it's held by nobody@contoso.com. The original organizer"
            " left the company last month and the recurring booking wasn't cleaned up. I need"
            " this room today at 2 PM for a client presentation.",
        ),
        gold=ScenarioGold(
            category="Software & Applications",
            priority="P3",
            assigned_team="Enterprise Applications",
            needs_escalation=False,
            missing_information=("timestamp",),
            next_best_action="Remove orphaned recurring room booking for Conference Room 12A — extract the"
            " scheduling conflict from embedded vCalendar/ICS data",
            remediation_steps=(
                "Cancel the orphaned recurring meeting in the Exchange room mailbox for 12A",
                "Verify the room is freed for the 2 PM client meeting",
                "Check for other orphaned bookings from the departed employee's account",
                "Clean up the nobody@contoso.com mailbox or disable it in Entra ID",
                "Set up a process to review room bookings when employees depart",
            ),
        ),
        tags=("data-cleanup", "ics-data", "calendar-noise"),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 19. OCR / scan artifacts in text
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="dc-gen-019",
        subjects=(
            "Scanned handwritten note — can't access network drive",
            "OCR of handwritten IT request — network drive access",
        ),
        descriptions=(
            "[OCR scan of handwritten note]\n\n"
            "T0 wh0m it may c0ncern at lT,\n\n"
            "l can n0 l0nger acc ess the shared netw0rk drve\n"
            "at \\\\FS-NYC-02\\Compli ance\\Q1-Rep0rts\n\n"
            "l was able t0 0pen it last Fri day but t0day it\n"
            "says 'Acc ess Den ied'. My man ager J0hn Davis\n"
            "appr0ved my acc ess m0nths ag0.\n\n"
            "PIease heIp — l need these fiIes for the aud it.\n\n"
            "Thank y0u,\n"
            "Sarah (Compl iance, Fl00r 3)",
            "[Scanned note — poor quality OCR]\n\n"
            "He|p — network drive not working\n"
            "Path: \\\\FS-NYC-O2\\Comp|iance\\Q1-Reports\n"
            "Error: Access Den|ed\n"
            "Was work|ng |ast Fr|day, not today\n"
            "Need for aud|t — urgent\n"
            "— Sarah, Comp|iance dept, F|oor 3",
        ),
        gold=ScenarioGold(
            category="Data & Storage",
            priority="P2",
            assigned_team="Data Platform",
            needs_escalation=False,
            missing_information=("error_message",),
            next_best_action="Investigate network drive access denial on \\\\FS-NYC-02\\Compliance\\Q1-Reports —"
            " parse OCR artifacts to extract the real file share access issue",
            remediation_steps=(
                "Check the user's permissions on the FS-NYC-02 Compliance share",
                "Verify if a recent ACL change or group policy update removed access",
                "Confirm with the manager that approval is still valid",
                "Restore the user's access to the Q1-Reports folder",
                "Check if other Compliance team members are also locked out",
            ),
        ),
        tags=("data-cleanup", "ocr-artifacts", "handwritten-scan"),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 20. URL / tracking link spam embedded in a real ticket
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="dc-gen-020",
        subjects=(
            "FW: [External] Unable to access client portal",
            "External portal login broken — lots of tracking links in original email",
        ),
        descriptions=(
            "---------- Forwarded message ----------\n"
            "From: Client Portal <noreply@clientportal.contoso.com>\n"
            "Subject: Action Required: Verify your account\n\n"
            "Dear User,\n\n"
            "Click here to verify: https://clientportal.contoso.com/verify?token=abc123"
            "&utm_source=email&utm_medium=notification&utm_campaign=q1_access_review"
            "&utm_content=verify_button&utm_term=access&ref=email_notification_20260318"
            "&tracking_id=TRK-9a8b7c6d-5e4f-3a2b-1c0d-9e8f7a6b5c4d"
            "&session=SES-1234567890abcdef&redirect=https%3A%2F%2Fclientportal.contoso.com"
            "%2Fdashboard%3Fview%3Ddefault%26lang%3Den-US%26theme%3Dlight\n\n"
            "If the above link doesn't work, copy and paste this URL:\n"
            "https://clientportal.contoso.com/verify?token=abc123&utm_source=email"
            "&fallback=true&device_id=DEV-xyz789&browser_fingerprint=BFP-456\n\n"
            "--- End of forwarded message ---\n\n"
            "I tried clicking both links but I get a 403 Forbidden error on the client"
            " portal. This started after the maintenance over the weekend. Other team"
            " members in Client Services can log in fine.",
            "Can't log into the client-facing portal at clientportal.contoso.com. Getting"
            " 403 Forbidden. I forwarded the verification email but it's full of tracking"
            " parameters. The actual issue is that my account seems deactivated after the"
            " weekend maintenance.",
        ),
        gold=ScenarioGold(
            category="Access & Authentication",
            priority="P2",
            assigned_team="Identity & Access Management",
            needs_escalation=False,
            missing_information=("error_message",),
            next_best_action="Investigate client portal 403 Forbidden error after weekend maintenance —"
            " ignore tracking URL noise and focus on the account access issue",
            remediation_steps=(
                "Check the user's account status on the client portal identity provider",
                "Verify if the weekend maintenance changed access policies or deactivated accounts",
                "Re-enable the account if it was inadvertently deactivated during maintenance",
                "Clear the portal session cache and have the user re-authenticate",
                "Confirm access is restored by testing login from the user's machine",
            ),
        ),
        tags=("data-cleanup", "tracking-urls", "url-noise"),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 21. Very long email with buried issue — real problem hidden in rambling
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="dc-gen-021",
        subjects=(
            "Various issues and general feedback — also something wrong with my computer",
            "RE: Quick question (plus a few other things I've been meaning to mention)",
        ),
        descriptions=(
            "Hi IT team,\n\n"
            "Hope you're all doing well! I wanted to start by saying I really appreciate"
            " the work you all did on the office renovation last month — the new monitors"
            " look fantastic. Speaking of which, I had a great meeting with the London"
            " office yesterday about the Q3 derivatives strategy and I think we're in a"
            " really good place. Oh, I also wanted to mention that the coffee machine on"
            " Floor 12 has been making a weird noise, not sure if that's you guys or"
            " facilities but figured I'd mention it.\n\n"
            "Anyway, my manager Sarah asked me to remind everyone about the compliance"
            " training deadline next Friday. I know it's not IT-related but could you send"
            " a reminder to the team? Also, the lunch options in the cafeteria have been"
            " great lately.\n\n"
            "Oh, I almost forgot the reason I'm actually writing — for the past three days"
            " my Bloomberg Terminal has been throwing a 'CONNECTION REFUSED' error every"
            " time I try to pull real-time equity feeds. It usually happens between 9 AM"
            " and 11 AM ET during peak trading hours. I've restarted the terminal twice"
            " and cleared the cache but it keeps happening. My desk is 12-A-047 and I'm"
            " on the trading floor VLAN.\n\n"
            "Also, do you know if the holiday party is confirmed for December 18th? And"
            " one more thing — can we get more whiteboard markers for the 14th floor"
            " conference room?\n\n"
            "Thanks for everything!\nBest, Priya Sharma\nSenior Equity Analyst",
            "Subject: Misc stuff + a tech problem\n\n"
            "Hey team — I have like five things to mention so bear with me. First, the"
            " parking garage lights on level B2 are flickering again. Second, I wanted to"
            " say thanks for fixing the projector in room 8C last week. Third, my daughter"
            " is selling Girl Scout cookies if anyone is interested (thin mints are the"
            " best, fight me).\n\n"
            "Fourth, and this is actually the important one — my Bloomberg Terminal keeps"
            " dropping its connection to the real-time feed. Error says 'CONNECTION"
            " REFUSED' and it's been happening every morning during market open for the"
            " last three days. I'm on the trading floor, desk 12-A-047. Other traders"
            " seem fine so it might be my terminal specifically.\n\n"
            "Fifth, can someone look into whether we can get standing desk converters for"
            " the risk team? A few people have been asking.\n\nThanks! — Priya",
        ),
        gold=ScenarioGold(
            category="Software & Applications",
            priority="P2",
            assigned_team="Enterprise Applications",
            needs_escalation=False,
            missing_information=("error_message", "application_version"),
            next_best_action="Investigate Bloomberg Terminal 'CONNECTION REFUSED' error on real-time"
            " equity feeds during market hours — buried in a long rambling email with"
            " multiple unrelated requests",
            remediation_steps=(
                "Check Bloomberg Terminal network connectivity from desk 12-A-047 on the trading floor VLAN",
                "Verify the Bloomberg B-PIPE or real-time feed service is running and accessible",
                "Review firewall rules for the trading floor VLAN to ensure Bloomberg ports are open",
                "Compare network configuration with nearby working terminals to isolate the issue",
                "Restart the Bloomberg Terminal service and clear local connection cache",
            ),
        ),
        tags=("data-cleanup", "buried-issue", "verbose-email"),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 22. Massive base64 PDF attachment inline in the ticket body
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="dc-gen-022",
        subjects=(
            "Compliance report PDF won't upload to SharePoint — pasting content here",
            "Attached: Q2 audit findings — system won't let me attach so I pasted the raw file",
        ),
        descriptions=(
            "I've been trying to upload our Q2 compliance audit report to the SharePoint"
            " Regulatory Documents library but I keep getting a 'File exceeds maximum size'"
            " error. The file is 48 MB. I'm pasting the raw PDF content below so you can"
            " see what I'm working with:\n\n"
            "--- BEGIN PDF CONTENT ---\n"
            "JVBERi0xLjcKMSAwIG9iago8PCAvVHlwZSAvQ2F0YWxvZyAvUGFnZXMgMiAw\n"
            "IFIgPj4KZW5kb2JqCjIgMCBvYmoKPDwgL1R5cGUgL1BhZ2VzIC9LaWRzIFsz\n"
            "IDAgUl0gL0NvdW50IDEgPj4KZW5kb2JqCjMgMCBvYmoKPDwgL1R5cGUgL1Bh\n"
            "Z2UgL1BhcmVudCAyIDAgUiAvTWVkaWFCb3ggWzAgMCA2MTIgNzkyXSAvQ29u\n"
            "dGVudHMgNCAwIFIgL1Jlc291cmNlcyA8PCAvRm9udCA8PCAvRjEgNSAwIFIg\n"
            "Pj4gPj4gPj4KZW5kb2JqCjQgMCBvYmoKPDwgL0xlbmd0aCA0NCA+PgpzdHJl\n"
            "YW0KQlQKL0YxIDE4IFRmCjEwMCA3MDAgVGQKKENvbnRvc28gRmluYW5jaWFs\n"
            "IFNlcnZpY2VzIC0gUTIgQXVkaXQpIFRqCkVUCmVuZHN0cmVhbQplbmRvYmoK\n"
            "[... 2,847 more lines of base64 data omitted for brevity ...]\n"
            "NTYgMCBvYmoKPDwgL1R5cGUgL0ZvbnQgL1N1YnR5cGUgL1R5cGUxIC9CYXNl\n"
            "Rm9udCAvSGVsdmV0aWNhID4+CmVuZG9iago=\n"
            "--- END PDF CONTENT ---\n\n"
            "Can you either increase the SharePoint upload limit or help me find another"
            " way to get this into the Regulatory Documents library? The audit committee"
            " needs access by end of week.",
            "The SharePoint document library for regulatory filings has a file size cap"
            " that's too low for our audit reports. I tried to upload the Q2 compliance"
            " PDF (48 MB) and got rejected. Here's the base64 of the file header so you"
            " can verify the format:\n\n"
            "JVBERi0xLjcNCjEgMCBvYmoNCjw8IC9UeXBlIC9DYXRhbG9nIC9QYWdlcyAy\n"
            "IDAgUiA+Pg0KZW5kb2JqDQoyIDAgb2JqDQo8PCAvVHlwZSAvUGFnZXMgL0tp\n"
            "ZHMgWzMgMCBSXSAvQ291bnQgMSA+Pg0KZW5kb2JqDQozIDAgb2JqDQo8PCAv\n"
            "VHlwZSAvUGFnZSAvUGFyZW50IDIgMCBSIC9NZWRpYUJveCBbMCAwIDYxMiA3\n"
            "OTJdIC9Db250ZW50cyA0IDAgUiAvUmVzb3VyY2VzIDw8IC9Gb250IDw8IC9G\n"
            "MSA1IDAgUiA+PiA+PiA+Pg0KZW5kb2JqDQo0IDAgb2JqDQo=\n\n"
            "Please increase the upload limit on the Regulatory Documents library or set"
            " up a large-file upload solution. The audit committee review is Friday.",
        ),
        gold=ScenarioGold(
            category="Data & Storage",
            priority="P3",
            assigned_team="Data Platform",
            needs_escalation=False,
            missing_information=("configuration_details",),
            next_best_action="Increase SharePoint document library file size limit or configure"
            " large-file upload for the Regulatory Documents library — ignore inline"
            " base64 PDF content in the ticket body",
            remediation_steps=(
                "Check the current file size upload limit on the SharePoint Regulatory Documents library",
                "Increase the tenant or library-level upload limit to accommodate 48 MB+ files",
                "Verify the SharePoint admin center settings for large file upload support",
                "Test uploading the PDF after adjusting the limit and confirm success",
                "Advise the user not to paste raw file content in tickets and use proper attachment methods",
            ),
        ),
        tags=("data-cleanup", "base64-noise", "inline-attachment"),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 23. Mobile autocorrect mangling technical terms
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="dc-gen-023",
        subjects=(
            "Out look keeps crassing on my phone",
            "Cant get into share point from my i phone",
        ),
        descriptions=(
            "hey so my out look keeps crassing on my i phone every time i try to open"
            " the calandar it just spins and then closes. ive tried restarting the app"
            " and my fone but same thing. also i cant sync my male box its saying"
            " 'account not verified' or something like that. im using the latest eye oh"
            " ess version i think. my user name is jthompson@contoso.com and im in the"
            " risk and complience team. this has been happening seance yesterday after"
            " that update popped up. also my teams app is fine its just out look thats"
            " broken. pls help asap i have client meetings today and all my calander"
            " invites are in out look\n\n"
            "sent from my iphone",
            "hi IT — out look on my mobile keeps shutting down when i open calender."
            " i think its since the last up date. ive un installed and re installed but"
            " same problem. also my male cant sync it says 'account configuration"
            " error'. im on i phone 15 pro with eye oh ess 17. my teams works fine"
            " its just the out look app. can some one look at this today? i have"
            " important meetings.\n\n"
            "thx\n"
            "jason thompson\n"
            "risk & complience\n"
            "sent form my iphone",
        ),
        gold=ScenarioGold(
            category="Software & Applications",
            priority="P2",
            assigned_team="Enterprise Applications",
            needs_escalation=False,
            missing_information=("application_version", "device_info"),
            next_best_action="Investigate Outlook mobile app crashing on calendar open and mailbox"
            " sync failure after recent iOS update — autocorrect-mangled text but clear"
            " issue is Outlook mobile malfunction",
            remediation_steps=(
                "Verify the user's Outlook mobile app version and iOS version",
                "Check for known issues with the latest Outlook iOS update",
                "Remove and re-add the Exchange account in the Outlook mobile app",
                "Clear the Outlook app cache and data on the device",
                "If the issue persists, test with the native iOS Mail app to isolate the problem",
            ),
        ),
        tags=("data-cleanup", "autocorrect", "mobile-chat"),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 24. Auto-translated email with translation artifacts
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="dc-gen-024",
        subjects=(
            "\u3010Translated from Japanese\u3011Network shared folder cannot access possibility",
            "RE: [Auto-Translated] Common drive connection is not good condition",
        ),
        descriptions=(
            "\u203bThis email has been automatically translated from Japanese\u203b\n\n"
            "Dear IT Assistance Team Honorable Members,\n\n"
            "I am Tanaka Yuki of the Tokyo Office Risk Management Department reporting"
            " with sincerest apologies for the inconvenience. Since the time of this"
            " morning approximately 10:00 JST, the shared network drive"
            " (\\\\contoso-nas-tyo\\risk_reports) is becoming the state of inaccessibility.\n\n"
            "When connection is attempted, the error of"
            " '\u30cd\u30c3\u30c8\u30ef\u30fc\u30af\u30d1\u30b9\u304c\u898b\u3064\u304b\u308a\u307e\u305b\u3093'"
            " (translation: network path is not discoverable) is displayed on screen."
            " This situation is affecting the entirety of the Tokyo Risk team members"
            " (approximately 15 persons) who are requiring access to the daily risk"
            " calculation reports with extreme urgency.\n\n"
            "The circumstance of before was completely normal with good function until"
            " the evening of yesterday. I am harboring suspicion that the maintenance"
            " work of overnight may have connection to this problem occurrence.\n\n"
            "With greatest urgency I am requesting the investigation. The risk reports"
            " must achieve delivery to the regulatory authority (\u91d1\u878d\u5e81/FSA) by the"
            " deadline of 14:00 JST today.\n\n"
            "Respectfully with deep bow,\n"
            "\u7530\u4e2d \u7531\u7d00 (Tanaka Yuki)\n"
            "Risk Management Department, Tokyo Office\n"
            "Extension: +81-3-XXXX-5678",
            "\u203bAuto Translation from Chinese (Simplified)\u2192English\u203b\n\n"
            "Hello IT Support Group,\n\n"
            "Shanghai Office Compliance Department's Li Wei is speaking. The common"
            " network storage drive (\\\\contoso-nas-sha\\compliance_docs) from this"
            " morning suddenly cannot connect to the situation. Error message display"
            " is '\u65e0\u6cd5\u8bbf\u95ee\u7f51\u7edc\u4f4d\u7f6e' meaning the network location"
            " arrival is impossible.\n\n"
            "Our team approximate 12 people all same problem is occurring. Yesterday"
            " night time everything was normal operation. Perhaps overnight system"
            " maintenance is having relationship with this failure.\n\n"
            "Compliance report submission deadline is today afternoon, very much"
            " urgent please. The regulatory filing (\u76d1\u7ba1\u62a5\u544a) cannot be delayed.\n\n"
            "Please to help as fast as possible,\n"
            "\u674e\u4f1f (Li Wei)\n"
            "Compliance Department, Shanghai Office",
        ),
        gold=ScenarioGold(
            category="Network & Connectivity",
            priority="P2",
            assigned_team="Network Operations",
            needs_escalation=False,
            missing_information=("error_message", "environment_details"),
            next_best_action="Investigate network shared drive inaccessibility at APAC offices"
            " following overnight maintenance — translation artifacts present but issue"
            " is clear network path failure on NAS storage",
            remediation_steps=(
                "Verify the NAS storage appliance is online and accessible from the affected office network",
                "Check if overnight maintenance changed SMB share permissions or network routes",
                "Test connectivity to the NAS from the affected VLAN using UNC path and IP address",
                "Review DNS resolution for the NAS hostname from Tokyo/Shanghai office subnets",
                "Restore share access and confirm users can reach the risk/compliance report directories",
            ),
        ),
        tags=("data-cleanup", "auto-translated", "translation-artifacts"),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 25. Extremely terse ticket with almost no context
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="dc-gen-025",
        subjects=(
            "laptop broken",
            "not working",
        ),
        descriptions=(
            "laptop broken. pls fix",
            "my computer doesnt turn on",
        ),
        gold=ScenarioGold(
            category="Hardware & Peripherals",
            priority="P3",
            assigned_team="Endpoint Engineering",
            needs_escalation=False,
            missing_information=(
                "device_info",
                "error_message",
                "steps_to_reproduce",
                "business_impact",
            ),
            next_best_action="Request additional details from the user — ticket is too vague to"
            " diagnose. Need device model, symptoms, when it started, and what 'broken'"
            " or 'not working' means specifically",
            remediation_steps=(
                "Contact the user to gather basic information: device model, symptoms, and timeline",
                "Determine whether the laptop fails to power on, has display issues, or another problem",
                "Once symptoms are clarified, proceed with appropriate hardware diagnostics",
                "If the device is unresponsive, schedule a swap or in-person desk visit",
            ),
        ),
        tags=("data-cleanup", "terse", "missing-context"),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 26. Browser view-source HTML paste (500 error page with SQL connection pool exhaustion)
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="dc-gen-026",
        subjects=(
            "500 error on trade reconciliation portal — full page source attached",
            "view-source: Recon Portal keeps returning 500 — HTML dump inside",
        ),
        descriptions=(
            "I keep getting a 500 error on the trade reconciliation portal. I did View Source"
            " in Chrome and copied the whole page:\n\n"
            '<!DOCTYPE html>\n<html lang="en">\n<head>\n'
            '  <meta charset="UTF-8">\n'
            "  <title>500 Internal Server Error</title>\n"
            '  <style>\n    body { font-family: "Segoe UI", Arial, sans-serif;'
            " background: #f4f4f4; margin: 0; padding: 40px; }\n"
            "    .error-container { max-width: 800px; margin: auto;"
            " background: white; border-radius: 8px;\n"
            "      padding: 40px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }\n"
            "    h1 { color: #d9534f; }\n"
            "    .stack-trace { background: #2d2d2d; color: #f8f8f2;"
            " padding: 20px; border-radius: 4px;\n"
            "      overflow-x: auto; font-family: Consolas, monospace;"
            " font-size: 12px; }\n"
            "  </style>\n</head>\n<body>\n"
            '  <div class="error-container">\n'
            "    <h1>500 Internal Server Error</h1>\n"
            "    <p>An error occurred processing your request.</p>\n"
            '    <div class="stack-trace">\n'
            "      System.InvalidOperationException: Timeout expired. The timeout"
            " period elapsed prior to obtaining a connection from the pool.\n"
            "      This may have occurred because all pooled connections were in"
            " use and max pool size was reached.\n"
            "      at System.Data.SqlClient.SqlConnectionPoolManager"
            ".GetConnection(DbConnectionOptions opts)\n"
            "      at Contoso.Recon.DataAccess.TradeRepository"
            ".GetUnmatchedTrades(DateTime date)\n"
            "      at Contoso.Recon.Controllers.ReconController"
            ".Index(ReconQueryModel model)\n"
            "    </div>\n"
            "  </div>\n</body>\n</html>\n\n"
            "This has been happening since about 10:30 AM. The recon team (8 people)"
            " is completely blocked.",
            "The trade reconciliation portal shows a 500 error. I copied the page"
            " source and the stack trace says:\n\n"
            "System.InvalidOperationException: Timeout expired. The timeout period"
            " elapsed prior to obtaining a connection from the pool. All pooled"
            " connections were in use and max pool size was reached.\n"
            "    at Contoso.Recon.DataAccess.TradeRepository"
            ".GetUnmatchedTrades(DateTime date)\n\n"
            "The whole recon team can't work. Started around 10:30 this morning.",
        ),
        gold=ScenarioGold(
            category="Software & Applications",
            priority="P3",
            assigned_team="Enterprise Applications",
            needs_escalation=False,
            missing_information=("environment_details", "application_version"),
            next_best_action="Investigate SQL connection pool exhaustion on the trade reconciliation"
            " portal — the .NET stack trace indicates all pooled connections are in use,"
            " blocking the recon team",
            remediation_steps=(
                "Check the SQL Server connection pool settings and current active connections",
                "Identify any long-running or leaked database connections holding pool resources",
                "Increase the max pool size as a temporary relief while investigating the root cause",
                "Review recent deployments to the recon portal for connection handling regressions",
                "Restart the application pool to clear stuck connections and restore service",
            ),
        ),
        tags=("data-cleanup", "html-paste", "view-source"),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 27. Mixed RTL/LTR text (Arabic/English SharePoint access request)
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="dc-gen-027",
        subjects=(
            "طلب وصول SharePoint — Compliance Archive Access Request",
            "SharePoint الأرشيف — Need access to compliance archive site",
        ),
        descriptions=(
            "مرحبا فريق الدعم التقني,\n\n"
            "أنا أحمد الفهد من قسم الامتثال في مكتب دبي. أحتاج الوصول إلى موقع"
            " SharePoint الخاص بأرشيف الامتثال:\n\n"
            "https://contoso.sharepoint.com/sites/compliance-archive-mena\n\n"
            "I need read/write access to the MENA compliance archive site on SharePoint."
            " My manager خالد المنصوري (Khalid Al-Mansoori) has already approved this.\n\n"
            "الملفات التي أحتاج الوصول إليها تتعلق بتقارير التدقيق الداخلي للربع الأول"
            " 2026.\n\n"
            "The specific library is /sites/compliance-archive-mena/Shared Documents/"
            "Internal Audit/Q1-2026.\n\n"
            "شكراً جزيلاً,\n"
            "أحمد الفهد\n"
            "Compliance Department, Dubai Office\n"
            "Ext: +971-4-XXX-5678",
            "Hi IT,\n\n"
            "I'm from the Dubai compliance team. I need access to the MENA compliance"
            " archive on SharePoint:\n"
            "https://contoso.sharepoint.com/sites/compliance-archive-mena\n\n"
            "المدير خالد المنصوري وافق على الطلب\n"
            "(Manager Khalid Al-Mansoori approved the request)\n\n"
            "Specifically the Q1-2026 audit reports in the Internal Audit library."
            " أحتاج هذا بشكل عاجل لأن الموعد النهائي للتدقيق هو الأسبوع القادم.\n\n"
            "Thanks,\nAhmed Al-Fahd\nDubai Office",
        ),
        gold=ScenarioGold(
            category="Data & Storage",
            priority="P3",
            assigned_team="Data Platform",
            needs_escalation=False,
            missing_information=("authentication_method",),
            next_best_action="Grant read/write access to the MENA compliance archive SharePoint site"
            " for the Dubai compliance team member — manager approval already confirmed",
            remediation_steps=(
                "Verify the manager approval from Khalid Al-Mansoori for the SharePoint access request",
                "Add the user to the appropriate SharePoint permission group for the compliance-archive-mena site",
                "Grant read/write access scoped to the Internal Audit/Q1-2026 document library",
                "Confirm access with the requester and provide the direct URL to the library",
                "Log the access grant in the compliance access register per MENA data governance policy",
            ),
        ),
        tags=("data-cleanup", "mixed-rtl-ltr", "bidi-text"),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 28. HTML form hidden fields (copied HTML form elements from expense portal)
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="dc-gen-028",
        subjects=(
            "Expense portal won't submit — copied the form data",
            "FW: Expense Report Submission Error — HTML form dump inside",
        ),
        descriptions=(
            "The expense portal keeps failing when I try to submit my Q1 expense report."
            " I copied everything from the page source:\n\n"
            '<form id="expenseForm" action="/api/expense/submit" method="POST">\n'
            '  <input type="hidden" name="__RequestVerificationToken"'
            ' value="CfDJ8N0r3kT7vB2mXzQ5pLwH9aYjKl4DfG6hN8mO1pQrStUvWxYz" />\n'
            '  <input type="hidden" name="EmployeeId" value="EMP-0047281" />\n'
            '  <input type="hidden" name="CostCenter" value="CC-4520-NYC-TRADING" />\n'
            '  <input type="hidden" name="ApprovalChain"'
            ' value="MGR:sarah.chen|DIR:james.wu|VP:robert.hayes" />\n'
            '  <input type="hidden" name="SubmissionGuid"'
            ' value="a3f7c912-4e8b-4d1a-b6e5-9c0d2f8a1b3e" />\n'
            '  <input type="hidden" name="FiscalPeriod" value="FY2026-Q1" />\n'
            '  <div class="form-group">\n'
            "    <label>Report Title</label>\n"
            '    <input type="text" name="Title"'
            ' value="Q1 2026 Client Entertainment - NYC Trading Desk" />\n'
            "  </div>\n"
            '  <div class="form-group">\n'
            "    <label>Total Amount</label>\n"
            '    <input type="text" name="TotalAmount" value="$4,287.50" />\n'
            "  </div>\n"
            '  <button type="submit" class="btn btn-primary">Submit for Approval</button>\n'
            "</form>\n\n"
            "When I click Submit I get a spinning wheel for about 2 minutes then it says"
            ' "Request timeout — please try again." I\'ve tried 5 times today.',
            "My expense report won't submit. After clicking Submit, the page spins for"
            " 2 minutes and times out. Report title is 'Q1 2026 Client Entertainment'"
            " for $4,287.50. Cost center CC-4520-NYC-TRADING. Tried 5 times, same"
            " result every time. Error is just 'Request timeout — please try again.'",
        ),
        gold=ScenarioGold(
            category="Software & Applications",
            priority="P3",
            assigned_team="Enterprise Applications",
            needs_escalation=False,
            missing_information=("error_message", "environment_details"),
            next_best_action="Investigate expense portal submission timeout — the form POST to"
            " /api/expense/submit is timing out, blocking the user from submitting"
            " their Q1 expense report",
            remediation_steps=(
                "Check the expense portal application logs for timeout errors on the submit endpoint",
                "Verify the backend expense approval workflow service is running and responsive",
                "Test the /api/expense/submit endpoint directly to isolate client vs. server timeout",
                "Review if the approval chain lookup is causing delays in the submission pipeline",
                "If the backend service is degraded, restart it and have the user retry submission",
            ),
        ),
        tags=("data-cleanup", "html-form", "hidden-fields"),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 29. Windows Event Log XML (BSOD event log XML entries pasted)
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="dc-gen-029",
        subjects=(
            "Laptop keeps blue-screening — Event Viewer logs attached",
            "BSOD every morning — Windows Event Log XML dump",
        ),
        descriptions=(
            "My laptop has been crashing with a BSOD every morning this week."
            " I exported the Event Viewer logs:\n\n"
            "<Event xmlns='http://schemas.microsoft.com/win/2004/08/events/event'>\n"
            "  <System>\n"
            "    <Provider Name='Microsoft-Windows-WER-SystemErrorReporting'"
            " Guid='{ABCE23E7-DE45-4366-8631-84FA6C525952}'/>\n"
            "    <EventID>1001</EventID>\n"
            "    <Version>0</Version>\n"
            "    <Level>2</Level>\n"
            "    <Task>0</Task>\n"
            "    <Opcode>0</Opcode>\n"
            "    <Keywords>0x80000000000000</Keywords>\n"
            "    <TimeCreated SystemTime='2026-03-18T13:47:22.1847560Z'/>\n"
            "    <EventRecordID>48291</EventRecordID>\n"
            "    <Correlation/>\n"
            "    <Execution ProcessID='0' ThreadID='0'/>\n"
            "    <Channel>System</Channel>\n"
            "    <Computer>WS-NYC-TRADER-0472</Computer>\n"
            "    <Security/>\n"
            "  </System>\n"
            "  <EventData>\n"
            "    <Data Name='param1'>0x0000009f</Data>\n"
            "    <Data Name='param2'>0x0000000000000003</Data>\n"
            "    <Data Name='param3'>FFFFB80D4E2A0060</Data>\n"
            "    <Data Name='param4'>FFFFF80152437A20</Data>\n"
            "    <Data Name='param5'>DRIVER_POWER_STATE_FAILURE</Data>\n"
            "    <Data Name='param6'>\\Device\\00000068</Data>\n"
            "    <Data Name='param7'>intelppm.sys</Data>\n"
            "  </EventData>\n"
            "</Event>\n\n"
            "The BugCheck code is 0x9F — DRIVER_POWER_STATE_FAILURE pointing at"
            " intelppm.sys. It always happens after the laptop resumes from sleep.",
            "Repeated BSOD on my trading workstation WS-NYC-TRADER-0472. BugCheck"
            " 0x0000009F (DRIVER_POWER_STATE_FAILURE) referencing intelppm.sys."
            " Happens every time the laptop resumes from sleep — about once a day."
            " Started after last week's driver update pushed by IT.",
        ),
        gold=ScenarioGold(
            category="Hardware & Peripherals",
            priority="P2",
            assigned_team="Endpoint Engineering",
            needs_escalation=False,
            missing_information=("device_info",),
            next_best_action="Investigate recurring BSOD caused by DRIVER_POWER_STATE_FAILURE"
            " (0x9F) in intelppm.sys on resume from sleep — likely a driver compatibility"
            " issue from a recent update",
            remediation_steps=(
                "Check the recent driver update history for intelppm.sys and related power management drivers",
                "Roll back the Intel Processor Power Management driver to the previous stable version",
                "Update the system BIOS/UEFI firmware if a newer version addresses power state issues",
                "Adjust power management settings to prevent aggressive sleep states as a workaround",
                "Monitor the workstation after the rollback to confirm the BSOD does not recur",
            ),
        ),
        tags=("data-cleanup", "event-log-xml", "bsod"),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 30. tcpdump packet capture output (TCP retransmissions, connection resets)
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="dc-gen-030",
        subjects=(
            "tcpdump showing massive retransmissions to market data feed",
            "Network packet capture — connection resets to Bloomberg B-PIPE",
        ),
        descriptions=(
            "I ran tcpdump on the market data gateway and captured a ton of"
            " retransmissions and resets. Here's a snippet:\n\n"
            "13:42:01.234567 IP 10.1.50.22.48912 > 198.51.100.15.8194:"
            " Flags [S], seq 3847291054, win 65535, options [mss 1460,"
            "sackOK,TS val 1247382 ecr 0,nop,wscale 7], length 0\n"
            "13:42:01.234890 IP 198.51.100.15.8194 > 10.1.50.22.48912:"
            " Flags [S.], seq 2918374650, ack 3847291055, win 65535,"
            " options [mss 1460,sackOK,TS val 9384721 ecr 1247382,"
            "nop,wscale 7], length 0\n"
            "13:42:01.235012 IP 10.1.50.22.48912 > 198.51.100.15.8194:"
            " Flags [.], ack 1, win 512, length 0\n"
            "13:42:01.892341 IP 198.51.100.15.8194 > 10.1.50.22.48912:"
            " Flags [R.], seq 1, ack 1, win 0, length 0\n"
            "13:42:02.235567 IP 10.1.50.22.48912 > 198.51.100.15.8194:"
            " Flags [S], seq 3847291054, win 65535, options [mss 1460,"
            "sackOK,TS val 1247483 ecr 0,nop,wscale 7], length 0\n"
            "13:42:04.236123 IP 10.1.50.22.48912 > 198.51.100.15.8194:"
            " Flags [S], seq 3847291054, win 65535, length 0\n"
            "13:42:08.237890 IP 10.1.50.22.48912 > 198.51.100.15.8194:"
            " Flags [S], seq 3847291054, win 65535, length 0\n"
            "... [347 similar retransmission lines omitted] ...\n\n"
            "The market data feed (198.51.100.15:8194) keeps sending RST after"
            " the three-way handshake completes. This is causing real-time pricing"
            " to go stale for the NYC equity trading desk.",
            "Market data gateway 10.1.50.22 is experiencing TCP connection resets"
            " from the Bloomberg B-PIPE endpoint at 198.51.100.15:8194. Three-way"
            " handshake completes but the remote side immediately sends RST."
            " Hundreds of retransmissions per minute. Equity desk has stale prices.",
        ),
        gold=ScenarioGold(
            category="Network & Connectivity",
            priority="P2",
            assigned_team="Network Operations",
            needs_escalation=False,
            missing_information=("network_location", "configuration_details"),
            next_best_action="Investigate TCP connection resets from market data feed endpoint"
            " causing stale pricing on the equity trading desk — tcpdump shows RST"
            " after completed handshake",
            remediation_steps=(
                "Check the firewall rules and NAT configuration between the gateway and the external feed",
                "Verify the Bloomberg B-PIPE service subscription and IP allowlist are current",
                "Examine intermediate network devices for TCP session hijacking or deep packet inspection issues",
                "Test connectivity from an alternate gateway to isolate whether the issue is host or network",
                "Engage Bloomberg support if the RST originates from their infrastructure",
            ),
        ),
        tags=("data-cleanup", "tcpdump", "packet-capture"),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 31. CI/CD pipeline log (GitHub Actions output with failing tests)
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="dc-gen-031",
        subjects=(
            "CI pipeline broken — GitHub Actions output pasted",
            "Build failing on main — full GH Actions log",
        ),
        descriptions=(
            "Our deployment pipeline for the portfolio analytics service is broken."
            " Here's the GitHub Actions output:\n\n"
            "Run npm run test:integration\n"
            "  npm run test:integration\n"
            "  shell: /usr/bin/bash -e {0}\n"
            "  env:\n"
            "    NODE_ENV: test\n"
            "    DB_HOST: localhost\n"
            "    DB_PORT: 5432\n\n"
            "> portfolio-analytics@3.2.1 test:integration\n"
            "> jest --config jest.integration.config.js --forceExit\n\n"
            " PASS  src/services/__tests__/pricing.integration.test.ts\n"
            " PASS  src/services/__tests__/portfolio.integration.test.ts\n"
            " FAIL  src/services/__tests__/reconciliation.integration.test.ts\n"
            "  ● ReconciliationService › daily reconciliation › should match"
            " trades with settlement records\n\n"
            "    ConnectionError: connect ECONNREFUSED 127.0.0.1:5432\n\n"
            "      at TCPConnectWrap.afterConnect [as oncomplete]"
            " (node:net:1595:16)\n"
            "      at Object.<anonymous>"
            " (src/services/__tests__/reconciliation.integration.test.ts:47:28)\n\n"
            " FAIL  src/services/__tests__/settlement.integration.test.ts\n"
            "  ● SettlementService › T+1 settlement › should process"
            " pending settlements\n\n"
            "    ConnectionError: connect ECONNREFUSED 127.0.0.1:5432\n\n"
            "Test Suites: 2 failed, 2 passed, 4 total\n"
            "Tests:       5 failed, 18 passed, 23 total\n"
            "Time:        34.217 s\n"
            "Error: Process completed with exit code 1.\n\n"
            "We can't deploy the hotfix for the settlement calculation bug until"
            " CI passes. The portfolio team is blocked.",
            "GitHub Actions CI is failing on the portfolio-analytics repo. 2 of 4"
            " integration test suites fail with ECONNREFUSED on port 5432 — looks"
            " like the PostgreSQL service container isn't starting in the CI"
            " environment. We need to deploy a settlement calc hotfix urgently.",
        ),
        gold=ScenarioGold(
            category="Software & Applications",
            priority="P3",
            assigned_team="Enterprise Applications",
            needs_escalation=False,
            missing_information=("environment_details", "configuration_details"),
            next_best_action="Investigate CI/CD pipeline failure — PostgreSQL service container"
            " not starting in GitHub Actions, blocking deployment of a settlement"
            " calculation hotfix",
            remediation_steps=(
                "Check the GitHub Actions workflow YAML for the PostgreSQL service container configuration",
                "Verify the CI runner has sufficient resources to start the database service container",
                "Review recent changes to the workflow file or Docker image that may have broken the service",
                "Test the integration tests locally with the same PostgreSQL version to confirm they pass",
                "If urgent, consider temporarily skipping the failing tests to unblock the hotfix deployment",
            ),
        ),
        tags=("data-cleanup", "cicd-log", "github-actions"),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 32. Massive tracking URL parameters (SAP Fiori link with 500+ chars of UTM params)
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="dc-gen-032",
        subjects=(
            "SAP Fiori link broken — can't open expense approval page",
            "FW: Approve Expense Report — link doesn't work",
        ),
        descriptions=(
            "I got an email asking me to approve an expense report but the link"
            " doesn't work. Here's the full URL from the email:\n\n"
            "https://contoso-sap.fiori.cloud/sap/bc/ui5_ui5/ui2/ushell/shells/"
            "abap/FioriLaunchpad.html#Action-approveExpense&/detail/"
            "EXP-2026-04821?sap-client=100&sap-language=EN"
            "&utm_source=sap_workflow_notification"
            "&utm_medium=email"
            "&utm_campaign=expense_approval_q1_2026"
            "&utm_content=approve_button_primary"
            "&utm_term=expense_report_approval"
            "&mkt_tok=NTI2LVJKRy03MTIAAAGN3kH7qBvM9xTw2nKpL"
            "mFjR4sY8dEfGhIjKlMnOpQrStUv"
            "&tracking_id=a1b2c3d4-e5f6-7890-abcd-ef1234567890"
            "&notification_id=NOTIF-2026-0318-0947-AP"
            "&workflow_instance=WF-000482190"
            "&approval_step=2_of_3"
            "&delegated_from=sarah.chen%40contoso.com"
            "&original_submitter=marco.bellini%40contoso.com"
            "&cost_center=CC-4520-NYC-TRADING"
            "&amount=USD_4287.50"
            "&report_type=client_entertainment"
            "&fiscal_period=FY2026-Q1"
            "&sap-theme=sap_fiori_3"
            "&sap-ui-language=EN"
            "&sap-ui-xx-formFactor=desktop\n\n"
            "When I click it, I get a blank white page. I need to approve this"
            " by end of day.",
            "Can't open the SAP Fiori expense approval link from my workflow"
            " notification email. The URL is extremely long with a bunch of"
            " tracking parameters. Just shows a blank white page. I need to"
            " approve Marco Bellini's Q1 expense report ($4,287.50) today.",
        ),
        gold=ScenarioGold(
            category="Software & Applications",
            priority="P3",
            assigned_team="Enterprise Applications",
            needs_escalation=False,
            missing_information=("error_message", "environment_details"),
            next_best_action="Investigate SAP Fiori deep link failure for expense approval workflow"
            " — the URL with excessive tracking parameters may be exceeding URL length"
            " limits or the Fiori launchpad may have a routing issue",
            remediation_steps=(
                "Test the SAP Fiori expense approval URL after stripping non-essential tracking parameters",
                "Verify the SAP Fiori Launchpad is accessible and the user has the approval role assigned",
                "Check if the URL length exceeds browser or proxy URL limits due to tracking parameters",
                "Provide the user with a clean direct link to the expense approval transaction",
                "Review the email notification template to reduce unnecessary URL parameters",
            ),
        ),
        tags=("data-cleanup", "tracking-url", "long-url"),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 33. Calendar invite ICS data (VCALENDAR blocks, real issue: duplicate events)
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="dc-gen-033",
        subjects=(
            "Calendar full of duplicate meetings — ICS data pasted",
            "Outlook duplicating all calendar invites — raw ICS dump",
        ),
        descriptions=(
            "My Outlook calendar is showing every meeting 3 times. I exported one"
            " of the duplicates and the raw data looks like this:\n\n"
            "BEGIN:VCALENDAR\n"
            "VERSION:2.0\n"
            "PRODID:-//Microsoft Corporation//Outlook 16.0//EN\n"
            "METHOD:REQUEST\n"
            "BEGIN:VEVENT\n"
            "DTSTART:20260319T140000Z\n"
            "DTEND:20260319T150000Z\n"
            "DTSTAMP:20260318T094523Z\n"
            "ORGANIZER;CN=Sarah Chen:mailto:sarah.chen@contoso.com\n"
            "UID:040000008200E00174C5B7101A82E008000000001047C3B6\n"
            "ATTENDEE;ROLE=REQ-PARTICIPANT;PARTSTAT=NEEDS-ACTION;RSVP=TRUE"
            ";CN=Marco Bellini:mailto:marco.bellini@contoso.com\n"
            "ATTENDEE;ROLE=REQ-PARTICIPANT;PARTSTAT=ACCEPTED"
            ";CN=James Wu:mailto:james.wu@contoso.com\n"
            "SUMMARY:Q1 Portfolio Review — NYC Trading Desk\n"
            "LOCATION:Conference Room 12A / Teams\n"
            "SEQUENCE:3\n"
            "X-MICROSOFT-CDO-APPT-SEQUENCE:3\n"
            "END:VEVENT\n"
            "END:VCALENDAR\n\n"
            "Every single meeting on my calendar has 2-3 copies. It started after"
            " IT migrated our mailboxes last weekend. My calendar is unusable.",
            "Since the mailbox migration last weekend, all my Outlook meetings are"
            " duplicated (sometimes tripled). I have 3 copies of every invite."
            " The SEQUENCE numbers differ between copies. Calendar is completely"
            " cluttered and I keep getting confused about which ones are real.",
        ),
        gold=ScenarioGold(
            category="Software & Applications",
            priority="P4",
            assigned_team="Enterprise Applications",
            needs_escalation=False,
            missing_information=("environment_details",),
            next_best_action="Investigate duplicate calendar events following mailbox migration"
            " — likely a migration issue that replayed calendar invites with"
            " different sequence numbers",
            remediation_steps=(
                "Check the mailbox migration logs for duplicate calendar item imports",
                "Use MFCMAPI or PowerShell to identify and remove duplicate calendar entries by UID",
                "Verify the Exchange calendar repair assistant is running for the affected mailbox",
                "Confirm no active sync profiles are duplicating events from a secondary source",
                "Run a calendar folder repair using Outlook's built-in cleanup tools",
            ),
        ),
        tags=("data-cleanup", "ics-data", "calendar-invite"),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 34. Pasted spreadsheet data (tab-delimited portfolio reconciliation mismatch)
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="dc-gen-034",
        subjects=(
            "Portfolio reconciliation mismatches — spreadsheet data pasted",
            "Recon breaks between OMS and custodian — data dump",
        ),
        descriptions=(
            "The portfolio reconciliation is showing mismatches between our OMS and"
            " the custodian records. I copied the break report from Excel:\n\n"
            "Account\tCUSIP\tSecurity\tOMS Qty\tCustodian Qty\tDelta\tStatus\n"
            "ACCT-7291\t037833100\tAAPL\t15,000\t14,850\t150\tBREAK\n"
            "ACCT-7291\t594918104\tMSFT\t22,500\t22,500\t0\tMATCH\n"
            "ACCT-7291\t67066G104\tNVDA\t8,200\t8,050\t150\tBREAK\n"
            "ACCT-8834\t46625H100\tJPM\t30,000\t30,000\t0\tMATCH\n"
            "ACCT-8834\t78378X107\tSPY ETF\t50,000\t49,500\t500\tBREAK\n"
            "ACCT-8834\t464287655\tHYG ETF\t25,000\t25,250\t-250\tBREAK\n"
            "ACCT-9102\t912810SV1\tUST 10Y\t100,000\t100,000\t0\tMATCH\n"
            "ACCT-9102\t912828ZT6\tUST 2Y\t200,000\t199,000\t1,000\tBREAK\n\n"
            "5 breaks out of 8 positions checked so far. The OMS data loaded"
            " at 6:00 AM ET but the custodian file came in at 7:45 AM — there"
            " may have been late trades that got captured in one but not the"
            " other. Need help checking the data pipeline timing.",
            "Portfolio recon is broken today. Multiple position mismatches between"
            " OMS and custodian records — AAPL, NVDA, SPY, HYG, and a Treasury"
            " position all showing breaks. Suspect the custodian file loaded late"
            " and missed some end-of-day trades. Need the data pipeline team to"
            " check the load timestamps and re-run the reconciliation.",
        ),
        gold=ScenarioGold(
            category="Data & Storage",
            priority="P2",
            assigned_team="Data Platform",
            needs_escalation=False,
            missing_information=("timestamp", "environment_details"),
            next_best_action="Investigate portfolio reconciliation breaks caused by potential"
            " data pipeline timing mismatch — OMS and custodian file load times"
            " may be out of sync",
            remediation_steps=(
                "Check the data pipeline logs for the OMS and custodian file load timestamps",
                "Verify if late trades were captured in the OMS but missed in the earlier custodian file",
                "Re-run the reconciliation with the most recent custodian data extract",
                "Review the pipeline scheduling to ensure custodian files are loaded after trade cutoff",
                "Confirm all position breaks are resolved after the re-reconciliation",
            ),
        ),
        tags=("data-cleanup", "spreadsheet-paste", "tab-delimited"),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 35. ANSI escape codes from terminal (Nagios output with color codes, server down)
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="dc-gen-035",
        subjects=(
            "Server DOWN alert from Nagios — pasted terminal output",
            "Monitoring alert — Nagios shows critical, raw output inside",
        ),
        descriptions=(
            "Nagios is showing a critical alert for the settlement engine server."
            " I copied the output from my terminal:\n\n"
            "\x1b[1;31m*** CRITICAL ***\x1b[0m Host: \x1b[1;37m"
            "contoso-settle-prod-01\x1b[0m\n"
            "\x1b[1;31mStatus: DOWN\x1b[0m | Duration: \x1b[1;33m"
            "0d 0h 23m 47s\x1b[0m\n"
            "\x1b[0;36mAddress:\x1b[0m 10.1.60.41\n"
            "\x1b[0;36mService:\x1b[0m Settlement Engine\n"
            "\x1b[1;31mCRITICAL\x1b[0m - \x1b[0;36mHTTP\x1b[0m:"
            " Connection refused (port 8443)\n"
            "\x1b[1;31mCRITICAL\x1b[0m - \x1b[0;36mProcess\x1b[0m:"
            " settlement-engine.jar not found in process list\n"
            "\x1b[1;33mWARNING\x1b[0m  - \x1b[0;36mDisk\x1b[0m:"
            " /var/log 94% used\n"
            "\x1b[0;32mOK\x1b[0m       - \x1b[0;36mCPU\x1b[0m: 12%\n"
            "\x1b[0;32mOK\x1b[0m       - \x1b[0;36mMemory\x1b[0m: 67%\n"
            "\x1b[0;36mLast State Change:\x1b[0m 2026-03-18 14:32:15 ET\n"
            "\x1b[0;36mNotification:\x1b[0m 3 of 5 (every 15m)\n\n"
            "The settlement engine process is gone and the log disk is almost full."
            " T+1 settlement processing starts at 4:00 PM ET — less than 2 hours"
            " away.",
            "Settlement engine (contoso-settle-prod-01, 10.1.60.41) is DOWN per"
            " Nagios. Port 8443 refusing connections, settlement-engine.jar process"
            " not running. /var/log at 94% may have caused the crash. T+1"
            " settlement processing is at 4 PM — we have under 2 hours.",
        ),
        gold=ScenarioGold(
            category="Network & Connectivity",
            priority="P3",
            assigned_team="Network Operations",
            needs_escalation=False,
            missing_information=("error_message",),
            next_best_action="Investigate settlement engine process crash on contoso-settle-prod-01"
            " — process is not running, log disk nearly full, T+1 settlement"
            " processing imminent",
            remediation_steps=(
                "SSH into contoso-settle-prod-01 and check /var/log for the settlement engine crash logs",
                "Clear or rotate old log files to free disk space on /var/log (94% used)",
                "Restart the settlement-engine.jar process and verify it binds to port 8443",
                "Monitor the service via Nagios to confirm it returns to OK status",
                "Verify settlement processing completes successfully before the T+1 deadline",
            ),
        ),
        tags=("data-cleanup", "ansi-escape-codes", "terminal-output"),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 36. Very long email with issue buried at end (rambling, real issue: laptop dock no video)
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="dc-gen-036",
        subjects=(
            "Several issues / questions / general frustration — please read fully",
            "RE: RE: Multiple IT concerns — updated with new problem",
        ),
        descriptions=(
            "Hi IT team,\n\n"
            "I hope you're doing well. I wanted to reach out about a few things that"
            " have been on my mind lately. First of all, I want to say that the new"
            " coffee machines on the 4th floor are really great — much better than the"
            " old ones. I know that's not an IT issue but I just wanted to put that"
            " out there.\n\n"
            "Anyway, I had a question about the new Microsoft Teams update. I noticed"
            " the interface changed a bit and some of my pinned channels moved around."
            " Is that normal? I figured it out eventually but it was confusing at"
            " first. Not a big deal though.\n\n"
            "Also, I've been meaning to ask — is there a way to get a second monitor?"
            " I saw that some people on the trading floor have three monitors and I was"
            " wondering if that's something I could request. I know the budget cycle is"
            " complicated but it would really help my productivity.\n\n"
            "Oh, and I forgot to mention in my last email — the printer on Floor 4"
            " (the big one near the kitchen) was making a weird noise last Tuesday but"
            " it seems fine now. Just wanted to flag it in case it acts up again.\n\n"
            "Speaking of last Tuesday, I went to that lunch-and-learn about"
            " cybersecurity. Really informative! The speaker was great. Are there more"
            " of those planned?\n\n"
            "OK so the real reason I'm writing — and sorry for burying this — is that"
            " since this morning my laptop dock isn't outputting video to either of my"
            " monitors. The laptop screen works fine but both external displays are"
            " black. I've tried unplugging and replugging the dock, restarting the"
            " laptop, and switching cables. Nothing works. The dock is a Dell WD19TBS"
            " and my laptop is a ThinkPad X1 Carbon Gen 10. The dock's LED is on so it"
            " has power. I need my external monitors for the risk dashboard.\n\n"
            "Thanks for reading all of that!\n"
            "Best,\nLisa Park\nRisk Management, Floor 4",
            "Long story short (sorry for the wall of text in my previous email) —"
            " my Dell WD19TBS dock stopped sending video to both external monitors"
            " this morning. ThinkPad X1 Carbon Gen 10 laptop screen works fine."
            " Tried restarting, reseating cables, unplugging dock. LED is on."
            " Need my monitors for the risk dashboard.",
        ),
        gold=ScenarioGold(
            category="Hardware & Peripherals",
            priority="P3",
            assigned_team="Endpoint Engineering",
            needs_escalation=False,
            missing_information=("steps_to_reproduce",),
            next_best_action="Diagnose Dell WD19TBS dock video output failure to both external"
            " monitors — dock has power but no display output from ThinkPad X1 Carbon",
            remediation_steps=(
                "Check for pending Thunderbolt or display driver updates on the ThinkPad X1 Carbon",
                "Reset the dock by disconnecting power for 30 seconds, then reconnecting",
                "Test the monitors with a direct HDMI/DisplayPort connection bypassing the dock",
                "Update the Dell WD19TBS dock firmware using Dell Dock Update Utility",
                "If the issue persists, swap the dock with a known-good unit for comparison",
            ),
        ),
        tags=("data-cleanup", "buried-issue", "long-email"),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 37. Base64-encoded PDF inline (compliance scanner report, real issue: TLS cert expiry)
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="dc-gen-037",
        subjects=(
            "URGENT: Compliance scan found critical TLS cert expiry — report attached inline",
            "Security scan results — base64 PDF of Qualys report + TLS issue",
        ),
        descriptions=(
            "Our Qualys compliance scanner flagged a critical issue. The PDF report"
            " is embedded below but the key finding is that the TLS certificate for"
            " our external client portal (portal.contoso.com) expires in 72 hours.\n\n"
            "--- Base64-encoded Qualys Report PDF ---\n"
            "JVBERi0xLjcKMSAwIG9iago8PCAvVHlwZSAvQ2F0YWxvZyAvUGFnZXMgMiAwIFIg"
            "Pj4KZW5kb2JqCjIgMCBvYmoKPDwgL1R5cGUgL1BhZ2VzIC9LaWRzIFszIDAgUl0g"
            "L0NvdW50IDEgPj4KZW5kb2JqCjMgMCBvYmoKPDwgL1R5cGUgL1BhZ2UgL1BhcmVu"
            "dCAyIDAgUiAvTWVkaWFCb3ggWzAgMCA2MTIgNzkyXSAvQ29udGVudHMgNCAwIFIg"
            "L1Jlc291cmNlcyA8PCAvRm9udCA8PCAvRjEgNSAwIFIgPj4gPj4gPj4KZW5kb2Jq"
            "CjQgMCBvYmoKPDwgL0xlbmd0aCA0NDcgPj4Kc3RyZWFtCkJUCi9GMSAyNCBUZgox"
            "MDAgNzAwIFRkCihDb250b3NvIEZpbmFuY2lhbCBTZXJ2aWNlcykgVGoKL0YxIDEy"
            "IFRmCjAgLTMwIFRkCihRdWFseXMgQ29tcGxpYW5jZSBTY2FuIFJlcG9ydCAtIE1h"
            "cmNoIDIwMjYpIFRqCjAgLTQwIFRkCihDUklUSUNBTCBGSU5ESU5HOiBUTFMgQ2Vy"
            "... [remaining 47KB of base64 data truncated] ...\n"
            "--- End Base64 ---\n\n"
            "The cert is a DigiCert wildcard (*.contoso.com) issued in March 2025."
            " If it expires, external clients won't be able to access their portfolio"
            " dashboards. This will trigger regulatory notification requirements.\n\n"
            "Security Operations needs to coordinate an emergency renewal.",
            "Qualys scan found that the TLS cert for portal.contoso.com expires in"
            " 72 hours. It's the DigiCert wildcard cert (*.contoso.com). External"
            " client portal will go down if not renewed. Full PDF report was sent"
            " in previous email (base64 encoded). Regulatory implications if client"
            " portal becomes inaccessible.",
        ),
        gold=ScenarioGold(
            category="Security & Compliance",
            priority="P2",
            assigned_team="Security Operations",
            needs_escalation=True,
            missing_information=("configuration_details",),
            next_best_action="Emergency TLS certificate renewal for *.contoso.com wildcard cert"
            " expiring in 72 hours — external client portal at risk with regulatory"
            " notification implications",
            remediation_steps=(
                "Verify the current TLS certificate expiry date and serial number on portal.contoso.com",
                "Initiate an emergency wildcard certificate renewal through DigiCert",
                "Prepare the new certificate and deploy to all servers using the *.contoso.com wildcard",
                "Test the renewed certificate on a staging endpoint before production deployment",
                "Update the certificate monitoring alerts to ensure earlier warnings for future renewals",
            ),
        ),
        tags=("data-cleanup", "base64-pdf", "compliance-scan"),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 38. Multiple base64 screenshots in reply chain (monitor flickering debug)
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="dc-gen-038",
        subjects=(
            "RE: RE: Monitor flickering issue — more screenshots attached inline",
            "Monitor display artifacts — base64 screenshots from troubleshooting",
        ),
        descriptions=(
            "Following up on my monitor flickering issue. I took more screenshots"
            " showing the artifacts:\n\n"
            "Screenshot 1 (horizontal lines across screen):\n"
            "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJ"
            "AAAADUlEQVR42mP8z8BQDwADhQGAWjR9awAAAABJRU5ErkJggg==\n\n"
            "Screenshot 2 (green tint on right half of display):\n"
            "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJ"
            "AAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg==\n\n"
            "Screenshot 3 (entire screen flashing black for 1 second):\n"
            "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJ"
            "AAAADUlEQVR42mNkYPj/HwADBwIAMCbHYQAAAABJRU5ErkJggg==\n\n"
            "--- Original Message ---\n"
            "From: IT Support <itsupport@contoso.com>\n"
            "Subject: Re: Monitor flickering issue\n\n"
            "Can you send screenshots of the artifacts? Also try a different"
            " DisplayPort cable.\n\n"
            "--- Original Message ---\n"
            "My Dell U2722D monitor on the trading floor (Desk 14B) is flickering"
            " and showing horizontal lines. It gets worse throughout the day."
            " Tried swapping to the spare cable in the drawer — same issue."
            " The monitor is about 2 years old.",
            "My Dell U2722D monitor (Desk 14B, trading floor) has display artifacts"
            " — horizontal lines, green tint on half the screen, and intermittent"
            " blackouts. Tried a different DisplayPort cable, same behavior."
            " Gets worse as the day goes on. Monitor is ~2 years old."
            " Sent screenshots in previous email (inline base64).",
        ),
        gold=ScenarioGold(
            category="Hardware & Peripherals",
            priority="P3",
            assigned_team="Endpoint Engineering",
            needs_escalation=False,
            missing_information=("device_info",),
            next_best_action="Diagnose Dell U2722D monitor display artifacts on the trading floor"
            " — likely a hardware failure given cable swap did not resolve the issue"
            " and symptoms worsen over time",
            remediation_steps=(
                "Test the monitor with a different input source to confirm the issue is with the display",
                "Connect a known-good monitor to the user's workstation to rule out GPU issues",
                "If the monitor is confirmed faulty, initiate a warranty replacement with Dell",
                "Provide a temporary replacement monitor for the trading desk to avoid workflow disruption",
                "Update the hardware inventory to track the replacement",
            ),
        ),
        tags=("data-cleanup", "base64-screenshots", "inline-images"),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 39. Mobile autocorrect mangling (informal chat with autocorrect errors)
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="dc-gen-039",
        subjects=(
            "Cant use the sap app on my phone — ducking autocorrect sorry",
            "SAP fiori mobile is broken pls help",
        ),
        descriptions=(
            "Hey IT sorry for typos im on my phone and autocorrect is killing me\n\n"
            "so i cant log in to the SAP fiery app (fiori***) on my iPhone. it keeps"
            " saying 'authentication failed' even tho im using the right password."
            " i changed my pasta word (PASSWORD) last week and now the sap app wont"
            " accept it\n\n"
            "i tried the forget pasta word (ugh FORGOT PASSWORD) flow but it sends"
            " the reset link to my contour so (contoso!!!) email which i cant access"
            " on my phone because outlook is also asking me to reauthenticate\n\n"
            "im at a client site right now and need to approve purchase orders from"
            " the fiery launchpad (FIORI LAUNCHPAD). this is super urgent bc the"
            " vendor payment is do (due) today\n\n"
            "also my certificate or whatever it is might be expired? i got a pop up"
            " about a 'certificate error' before it said auth failed\n\n"
            "pls help asap thx\n"
            "- Dave Morrison, Procurement, sent from my iPhone",
            "Can't login to SAP Fiori mobile app on iPhone after password change"
            " last week. Getting 'authentication failed' error and possibly a"
            " certificate error popup. Also locked out of Outlook mobile —"
            " can't receive password reset emails. At client site, need to"
            " approve vendor purchase orders urgently.",
        ),
        gold=ScenarioGold(
            category="Software & Applications",
            priority="P2",
            assigned_team="Enterprise Applications",
            needs_escalation=False,
            missing_information=("device_info", "authentication_method"),
            next_best_action="Resolve SAP Fiori mobile authentication failure after password change"
            " — user is also locked out of Outlook mobile, creating a circular"
            " dependency for password reset",
            remediation_steps=(
                "Reset the user's cached credentials in Azure AD to force re-authentication across apps",
                "Guide the user through removing and re-adding their account in the Outlook mobile app",
                "Verify the MDM certificate on the iPhone is valid and not expired",
                "Test SAP Fiori login after Outlook email access is restored and new password is accepted",
                "Confirm the pending purchase order approvals can be processed in the Fiori app",
            ),
        ),
        tags=("data-cleanup", "autocorrect", "mobile-typos"),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 40. Speech-to-text voicemail transcription (server room cooling failure)
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="dc-gen-040",
        subjects=(
            "URGENT voicemail transcription — server room overheating",
            "[Auto-Transcribed Voicemail] Critical — data center cooling alarm",
        ),
        descriptions=(
            "[Voicemail transcribed by Microsoft Speech Services — accuracy may vary]\n\n"
            "hey this is mike delano from facilities I'm calling because the server"
            " room on the fourth floor is reading really high temperatures the the"
            " thermos stat (thermostat?) says 94° which is way above the 72° set"
            " point the the seas rack (CRAC?) unit on the left side is making a"
            " grinding noise and I think the compress or (compressor) has failed"
            " the backup unit kicked in but it's not keeping up the alarms have"
            " been going off for about 15 minutes now and I can see some of the"
            " servers have amber warning lights on them I think we need someone"
            " from IT to come down here right now before we start losing equipment"
            " the humidity is also climbing I'm reading 78% on the hymn idle"
            " (hydrometer?) panel and there's condensation starting on some of the"
            " cable trays this is really urgent please call me back at extension"
            " 4478 or just come down to the fourth floor server room immediately\n\n"
            "[End of transcription — Duration: 1m 42s — Confidence: 72%]",
            "Facilities reports 4th floor server room at 94°F (set point 72°F)."
            " Primary CRAC unit compressor has failed, backup not keeping up."
            " Humidity at 78% with condensation on cable trays. Servers showing"
            " amber thermal warnings. Issue ongoing for 15+ minutes. Contact:"
            " Mike DeLano, Facilities, ext 4478.",
        ),
        gold=ScenarioGold(
            category="Hardware & Peripherals",
            priority="P1",
            assigned_team="Endpoint Engineering",
            needs_escalation=True,
            missing_information=("environment_details",),
            next_best_action="Emergency: server room cooling failure on 4th floor — temperatures"
            " at 94°F and rising with CRAC compressor failure, immediate risk of"
            " hardware damage",
            remediation_steps=(
                "Dispatch on-site personnel to the 4th floor server room immediately to assess the situation",
                "Initiate emergency shutdown of non-critical servers to reduce heat load",
                "Contact HVAC vendor for emergency CRAC unit compressor repair or replacement",
                "Deploy portable cooling units to supplement the struggling backup CRAC",
                "Monitor server hardware health and prepare for potential hardware failures from thermal stress",
            ),
        ),
        tags=("data-cleanup", "voicemail-transcription", "speech-to-text"),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 41. Zero-width Unicode characters (invisible chars in SharePoint access request)
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="dc-gen-041",
        subjects=(
            "Can\u200bt a\u200bcc\u200bess Sh\u200bare\u200bPo\u200bint si\u200bte",
            "Sh\u200bareP\u200boint per\u200bmission den\u200bied — compliance docs",
        ),
        descriptions=(
            "Hi\u200b I\u200bT S\u200bup\u200bpo\u200brt,\n\n"
            "I\u200b ne\u200bed ac\u200bce\u200bss to\u200b th\u200be "
            "Sh\u200bare\u200bPo\u200bint si\u200bte fo\u200br "
            "co\u200bmp\u200bli\u200ban\u200bce do\u200bcu\u200bme\u200bnts:\n"
            "ht\u200btps://co\u200bnto\u200bso.sha\u200bre\u200bpo\u200bint"
            ".co\u200bm/si\u200btes/co\u200bmpl\u200bian\u200bce-\u200bdocs\n\n"
            "I\u200b ge\u200bt '\u200bAc\u200bce\u200bss De\u200bni\u200bed\u200b'"
            " wh\u200ben I\u200b tr\u200by to\u200b op\u200ben it\u200b.\n\n"
            "My\u200b ma\u200bna\u200bger sa\u200bid I\u200b sh\u200bou\u200bld"
            " ha\u200bve ac\u200bce\u200bss al\u200bre\u200bad\u200by.\n"
            "Pl\u200bea\u200bse he\u200blp\u200b!\n\n"
            "Th\u200ban\u200bks,\n"
            "Sa\u200bra\u200bh Jo\u200bhn\u200bson\n"
            "Co\u200bmp\u200bli\u200ban\u200bce Te\u200bam",
            "User cannot access SharePoint compliance docs site"
            " (contoso.sharepoint.com/sites/compliance-docs). Getting"
            " 'Access Denied' error. Manager confirms user should have"
            " access. Note: ticket text contains zero-width Unicode"
            " characters throughout.",
        ),
        gold=ScenarioGold(
            category="Software & Applications",
            priority="P3",
            assigned_team="Identity & Access Management",
            needs_escalation=False,
            missing_information=("environment_details",),
            next_best_action="Grant SharePoint access to compliance docs site after"
            " verifying manager approval — note that the ticket text"
            " contains invisible zero-width Unicode characters that may"
            " affect automated text processing",
            remediation_steps=(
                "Strip zero-width Unicode characters from the ticket text before processing",
                "Verify the user's identity and manager approval for SharePoint access",
                "Grant the user appropriate permissions to the compliance-docs SharePoint site",
                "Confirm the user can access the site after permission changes",
                "Flag the zero-width character pattern for the data quality team to investigate",
            ),
        ),
        tags=("data-cleanup", "zero-width-unicode", "invisible-characters"),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 42. GraphQL introspection dump in description
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="dc-gen-042",
        subjects=(
            "API gateway returns 502 on GraphQL endpoint",
            "GraphQL service down — introspection query included",
        ),
        descriptions=(
            "Our GraphQL API started returning 502 errors this morning. I ran an"
            " introspection query before it went down and pasted the result below"
            " for reference.\n\n"
            '{"data":{"__schema":{"queryType":{"name":"Query"},"mutationType":'
            '{"name":"Mutation"},"subscriptionType":null,"types":[{"kind":"OBJECT",'
            '"name":"Query","fields":[{"name":"user","args":[{"name":"id","type":'
            '{"kind":"NON_NULL","name":null,"ofType":{"kind":"SCALAR","name":"ID",'
            '"ofType":null}}}],"type":{"kind":"OBJECT","name":"User","ofType":null}},'
            '{"name":"orders","args":[{"name":"userId","type":{"kind":"NON_NULL",'
            '"name":null,"ofType":{"kind":"SCALAR","name":"ID","ofType":null}}},'
            '{"name":"status","type":{"kind":"ENUM","name":"OrderStatus","ofType":'
            'null}}],"type":{"kind":"LIST","name":null,"ofType":{"kind":"OBJECT",'
            '"name":"Order","ofType":null}}},{"name":"inventory","args":[{"name":'
            '"warehouseId","type":{"kind":"SCALAR","name":"String","ofType":null}}],'
            '"type":{"kind":"LIST","name":null,"ofType":{"kind":"OBJECT","name":'
            '"InventoryItem","ofType":null}}},{"name":"analytics","args":[],"type":'
            '{"kind":"OBJECT","name":"AnalyticsDashboard","ofType":null}}]},{"kind":'
            '"OBJECT","name":"User","fields":[{"name":"id","args":[],"type":{"kind":'
            '"NON_NULL","name":null,"ofType":{"kind":"SCALAR","name":"ID","ofType":'
            'null}}},{"name":"email","args":[],"type":{"kind":"SCALAR","name":'
            '"String","ofType":null}},{"name":"roles","args":[],"type":{"kind":'
            '"LIST","name":null,"ofType":{"kind":"ENUM","name":"UserRole","ofType":'
            'null}}}]}],"directives":[]}}}\n\n'
            "The endpoint is https://api.contoso.com/graphql and it handles all"
            " our order management queries. Around 200 internal users are affected.",
            "GraphQL API at api.contoso.com/graphql returning 502 since this"
            " morning. Handles order management for ~200 internal users."
            " User pasted full introspection schema JSON dump in the ticket.",
        ),
        gold=ScenarioGold(
            category="Software & Applications",
            priority="P2",
            assigned_team="Enterprise Applications",
            needs_escalation=False,
            missing_information=("error_message", "environment_details"),
            next_best_action="Investigate 502 errors on the GraphQL API gateway —"
            " ignore the introspection schema dump and focus on the upstream"
            " service health and gateway logs",
            remediation_steps=(
                "Check API gateway logs for the source of 502 errors on the /graphql endpoint",
                "Verify the upstream GraphQL service health and container/pod status",
                "Review recent deployments or configuration changes to the GraphQL service",
                "Test connectivity between the API gateway and the GraphQL backend directly",
                "Restore service and confirm order management queries are working for internal users",
            ),
        ),
        tags=("data-cleanup", "graphql-introspection", "json-dump"),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 43. Windows BSOD minidump output
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="dc-gen-043",
        subjects=(
            "Laptop blue screens every day — dump file info included",
            "BSOD DRIVER_IRQL_NOT_LESS_OR_EQUAL — minidump attached",
        ),
        descriptions=(
            "My laptop blue screens at least once a day, usually when I'm in a Teams"
            " meeting with screen sharing. I opened the minidump in WinDbg and pasted"
            " the output below.\n\n"
            "Microsoft (R) Windows Debugger Version 10.0.25921.1001 AMD64\n"
            "Copyright (c) Microsoft Corporation. All rights reserved.\n\n"
            "Loading Dump File [C:\\Windows\\Minidump\\031026-18234-01.dmp]\n"
            "Mini Kernel Dump File: Only registers and stack trace are available\n\n"
            "Symbol search path is: srv*\n"
            "Executable search path is:\n"
            "Windows 11 Kernel Version 22631 MP (8 procs) Free x64\n"
            "Product: WinNt, suite: TerminalServer SingleUserTS\n"
            "Edition build lab: 22631.1.amd64fre.ni_release.220506-1250\n"
            "Machine Name:\n"
            "Kernel base = 0xfffff802`3a000000 PsLoadedModuleList = 0xfffff802`3b2134a0\n"
            "Debug session time: Mon Mar 10 14:22:07.318 2026 (UTC - 5:00)\n"
            "System Uptime: 0 days 6:43:12.204\n"
            "Loading Kernel Symbols\n"
            "...............................................................\n"
            "Loading User Symbols\n"
            "Loading unloaded module list\n"
            ".......\n"
            "*******************************************************************************\n"
            "*                                                                             *\n"
            "* Bugcheck Analysis                                                           *\n"
            "*                                                                             *\n"
            "*******************************************************************************\n\n"
            "DRIVER_IRQL_NOT_LESS_OR_EQUAL (d1)\n"
            "An attempt was made to access a pageable (or completely invalid) address at an\n"
            "interrupt request level (IRQL) that is too high.\n"
            "Arguments:\n"
            "Arg1: ffffd580a3b7c010, memory referenced\n"
            "Arg2: 0000000000000002, IRQL\n"
            "Arg3: 0000000000000001, value 0 = read operation, 1 = write operation\n"
            "Arg4: fffff80241e8b230, address which referenced memory\n\n"
            "STACK_TEXT:\n"
            "fffffe01`c4d4e6d8 fffff802`3a223a9f : nt!KeBugCheckEx\n"
            "fffffe01`c4d4e6e0 fffff802`3a21f9c2 : nt!KiBugCheckDispatch+0x6f\n"
            "fffffe01`c4d4e820 fffff802`41e8b230 : nt!KiPageFault+0x462\n"
            "fffffe01`c4d4e9b8 fffff802`41e8a105 : ndis!ndisNblSetTimestamp+0x20\n"
            "fffffe01`c4d4e9c0 fffff802`41120068 : ndis!NdisMIndicateReceiveNetBufferLists+0x135\n"
            "fffffe01`c4d4ea30 fffff802`4111f8c2 : rt68cx21!RTMPRxDoneInterruptHandle+0x468\n\n"
            "MODULE_NAME: rt68cx21\n"
            "IMAGE_NAME: rt68cx21.sys\n\n"
            "The laptop is a Lenovo ThinkPad T14s Gen 4, about 8 months old. The crashes"
            " started after a Windows Update two weeks ago.",
            "User reports daily BSOD on Lenovo ThinkPad T14s Gen 4 during Teams"
            " meetings. Bugcheck DRIVER_IRQL_NOT_LESS_OR_EQUAL (0xD1) faulting"
            " in rt68cx21.sys (Realtek network driver). Crashes started after"
            " a Windows Update two weeks ago. Full WinDbg minidump analysis"
            " pasted into the ticket.",
        ),
        gold=ScenarioGold(
            category="Hardware & Peripherals",
            priority="P2",
            assigned_team="Endpoint Engineering",
            needs_escalation=False,
            missing_information=("environment_details",),
            next_best_action="Resolve recurring BSOD caused by Realtek network driver"
            " (rt68cx21.sys) on ThinkPad T14s — likely triggered by a recent"
            " Windows Update incompatibility with the NIC driver",
            remediation_steps=(
                "Update the Realtek network driver rt68cx21.sys to the latest version from Lenovo support",
                "If no updated driver is available, roll back the driver to the pre-update version",
                "Check Windows Update history for the specific KB that triggered the issue",
                "Disable any network offloading features that may conflict with the updated kernel",
                "Monitor for BSOD recurrence after the driver update and escalate to Lenovo if it persists",
            ),
        ),
        tags=("data-cleanup", "bsod-minidump", "debugger-output"),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 44. Teams/Slack webhook JSON payloads
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="dc-gen-044",
        subjects=(
            "Teams webhook notifications stopped working — payload samples included",
            "Slack → Teams connector broken — JSON payloads attached",
        ),
        descriptions=(
            "Our alerting pipeline sends notifications to a Teams channel via webhook"
            " but messages stopped appearing yesterday afternoon. Here are the last"
            " few payloads we sent that got HTTP 400 responses:\n\n"
            '{"@type":"MessageCard","@context":"https://schema.org/extensions",'
            '"themeColor":"FF0000","summary":"[CRITICAL] CPU > 95% on prod-web-04",'
            '"sections":[{"activityTitle":"Infrastructure Alert","activitySubtitle":'
            '"Triggered at 2026-03-10T15:42:18Z","activityImage":"https://monitoring'
            '.contoso.com/icons/critical.png","facts":[{"name":"Server","value":'
            '"prod-web-04.contoso.com"},{"name":"Metric","value":"cpu_percent"},'
            '{"name":"Current","value":"97.3%"},{"name":"Threshold","value":"95%"},'
            '{"name":"Duration","value":"12 minutes"},{"name":"Datacenter","value":'
            '"East US 2"}],"markdown":true}],"potentialAction":[{"@type":"OpenUri",'
            '"name":"View Dashboard","targets":[{"os":"default","uri":"https://'
            'monitoring.contoso.com/dash/prod-web-04"}]},{"@type":"OpenUri","name":'
            '"Acknowledge","targets":[{"os":"default","uri":"https://monitoring.'
            'contoso.com/ack/alert-28841"}]}]}\n\n'
            '{"@type":"MessageCard","@context":"https://schema.org/extensions",'
            '"themeColor":"FFA500","summary":"[WARNING] Disk space < 10% on '
            'sql-replica-02","sections":[{"activityTitle":"Infrastructure Alert",'
            '"activitySubtitle":"Triggered at 2026-03-10T15:44:02Z","facts":'
            '[{"name":"Server","value":"sql-replica-02.contoso.com"},{"name":'
            '"Metric","value":"disk_free_percent"},{"name":"Current","value":'
            '"7.2%"},{"name":"Threshold","value":"10%"},{"name":"Drive","value":'
            '"E:\\\\Data"}],"markdown":true}]}\n\n'
            "We haven't changed anything on our side. About 50 alerts a day go"
            " through this channel and the on-call team relies on it.",
            "Teams incoming webhook for infrastructure alerts returning HTTP 400"
            " since yesterday afternoon. ~50 alerts/day affected. User pasted"
            " multiple MessageCard JSON payloads. No changes made on sender side."
            " On-call team missing critical notifications.",
        ),
        gold=ScenarioGold(
            category="Software & Applications",
            priority="P2",
            assigned_team="Enterprise Applications",
            needs_escalation=False,
            missing_information=("error_message",),
            next_best_action="Investigate Teams incoming webhook returning HTTP 400 —"
            " Microsoft may have deprecated the legacy MessageCard format or"
            " changed connector requirements; on-call alerting is impacted",
            remediation_steps=(
                "Check the Teams admin center for any connector policy changes or deprecation notices",
                "Verify the webhook URL is still valid and the target channel/team has not been modified",
                "Test with a minimal MessageCard payload to isolate whether the schema or the connector is at fault",
                "Migrate from legacy Office 365 connectors to the Workflows-based"
                " webhook if connectors were deprecated",
                "Set up a fallback notification channel (email or secondary webhook) until the primary is restored",
            ),
        ),
        tags=("data-cleanup", "webhook-json", "teams-connector"),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 45. PowerShell mixed error/verbose/warning streams
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="dc-gen-045",
        subjects=(
            "AD user provisioning script failing — PowerShell output attached",
            "New hire onboarding script errors — full verbose log included",
        ),
        descriptions=(
            "The PowerShell script we use for new hire AD provisioning is failing."
            " I ran it with -Verbose and captured all streams. Here's the output:\n\n"
            "VERBOSE: [09:14:01] Connecting to domain controller DC01.contoso.com...\n"
            "VERBOSE: [09:14:02] Successfully authenticated as svc-provisioning@contoso.com\n"
            "VERBOSE: [09:14:02] Reading input CSV: \\\\fileserv01\\HR\\NewHires_20260310.csv\n"
            "VERBOSE: [09:14:03] Found 12 new hire records to process\n"
            "VERBOSE: [09:14:03] Processing record 1/12: Aisha Patel (aisha.patel@contoso.com)\n"
            "VERBOSE: [09:14:03] Creating AD account in OU=NewHires,OU=Users,DC=contoso,DC=com\n"
            "VERBOSE: [09:14:04] Setting manager to CN=Robert Kim,OU=Engineering,OU=Users,DC=contoso,DC=com\n"
            "VERBOSE: [09:14:04] Adding to groups: SG-Engineering, SG-AllEmployees, SG-VPN-Users\n"
            "WARNING: Group SG-Engineering-BuildAccess not found — skipping group membership\n"
            "VERBOSE: [09:14:05] Assigning E5 license via Microsoft Graph...\n"
            "VERBOSE: [09:14:06] License assigned successfully\n"
            "VERBOSE: [09:14:06] Processing record 2/12: James O'Brien (james.obrien@contoso.com)\n"
            "WARNING: Username james.obrien conflicts with existing disabled account — appending '2'\n"
            "VERBOSE: [09:14:07] Creating AD account as james.obrien2@contoso.com\n"
            "VERBOSE: [09:14:07] Setting manager to CN=Lisa Wang,OU=Marketing,OU=Users,DC=contoso,DC=com\n"
            "VERBOSE: [09:14:08] Adding to groups: SG-Marketing, SG-AllEmployees, SG-VPN-Users\n"
            "VERBOSE: [09:14:08] Assigning E3 license via Microsoft Graph...\n"
            "Write-Error: Insufficient licenses available for SKU ENTERPRISEPACK_E3 — "
            "0 of 500 licenses remaining\n"
            "VERBOSE: [09:14:09] Processing record 3/12: Mei Chen (mei.chen@contoso.com)\n"
            "Write-Error: Insufficient licenses available for SKU ENTERPRISEPACK_E3 — "
            "0 of 500 licenses remaining\n"
            "Write-Error: Insufficient licenses available for SKU ENTERPRISEPACK_E3 — "
            "0 of 500 licenses remaining\n"
            "WARNING: 3 consecutive license failures — pausing license assignments\n"
            "VERBOSE: [09:14:10] Creating AD account for mei.chen@contoso.com (without license)\n"
            "VERBOSE: [09:14:11] Processing record 4/12: Carlos Mendoza (carlos.mendoza@contoso.com)\n"
            "Write-Error: New-ADUser : The specified account already exists.\n"
            "At C:\\Scripts\\Provision-NewHire.ps1:147 char:9\n"
            "+         New-ADUser @userParams\n"
            "+         ~~~~~~~~~~~~~~~~~~~~~~~\n"
            "    + CategoryInfo          : ResourceExists\n"
            "    + FullyQualifiedErrorId : ADIdentityAlreadyExists,New-ADUser\n"
            "VERBOSE: [09:14:12] Script terminated after 4 records — 2 errors, 3 warnings\n\n"
            "12 new hires are starting Monday and only 1 was provisioned successfully.",
            "AD new hire provisioning script failed processing 12 users — only"
            " 1 completed. E3 license pool exhausted (0 of 500 remaining),"
            " username conflict with disabled account, and duplicate AD object"
            " error. Full PowerShell verbose/warning/error stream output pasted"
            " in the ticket. 12 new hires starting Monday.",
        ),
        gold=ScenarioGold(
            category="Software & Applications",
            priority="P2",
            assigned_team="Identity & Access Management",
            needs_escalation=False,
            missing_information=("environment_details",),
            next_best_action="Resolve multiple AD provisioning failures — procure"
            " additional E3 licenses, clean up conflicting/duplicate accounts,"
            " and re-run the script before Monday onboarding",
            remediation_steps=(
                "Request additional E3 licenses or reclaim unused licenses from"
                " disabled accounts to replenish the pool",
                "Resolve the james.obrien username conflict by removing or permanently renaming the disabled account",
                "Investigate and remove the duplicate AD object for carlos.mendoza before re-provisioning",
                "Verify the missing security group SG-Engineering-BuildAccess and create it if needed",
                "Re-run the provisioning script for the 11 incomplete users and"
                " confirm all accounts are ready before Monday",
            ),
        ),
        tags=("data-cleanup", "powershell-streams", "mixed-output"),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 46. Docker Compose YAML flood
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="dc-gen-046",
        subjects=(
            "Dev environment won't start — Docker Compose config pasted below",
            "docker compose up fails — YAML included for troubleshooting",
        ),
        descriptions=(
            "My local dev environment stopped working after I pulled the latest"
            " docker-compose.yml from the repo. Here's the full file:\n\n"
            "version: '3.8'\n"
            "services:\n"
            "  web:\n"
            "    build:\n"
            "      context: .\n"
            "      dockerfile: Dockerfile.web\n"
            "    ports:\n"
            "      - '3000:3000'\n"
            "    environment:\n"
            "      - NODE_ENV=development\n"
            "      - DATABASE_URL=postgresql://devuser:devpass@db:5432/contoso_dev\n"
            "      - REDIS_URL=redis://cache:6379/0\n"
            "      - API_KEY=${CONTOSO_API_KEY}\n"
            "      - JWT_SECRET=${JWT_SECRET}\n"
            "      - AZURE_STORAGE_CONNECTION=DefaultEndpointsProtocol=https;"
            "AccountName=contosodev;AccountKey=REDACTED;EndpointSuffix=core.windows.net\n"
            "    volumes:\n"
            "      - ./src:/app/src\n"
            "      - /app/node_modules\n"
            "    depends_on:\n"
            "      db:\n"
            "        condition: service_healthy\n"
            "      cache:\n"
            "        condition: service_started\n"
            "      elasticsearch:\n"
            "        condition: service_healthy\n"
            "    networks:\n"
            "      - contoso-net\n\n"
            "  api:\n"
            "    build:\n"
            "      context: ./api\n"
            "      dockerfile: Dockerfile\n"
            "    ports:\n"
            "      - '8080:8080'\n"
            "    environment:\n"
            "      - ASPNETCORE_ENVIRONMENT=Development\n"
            "      - ConnectionStrings__DefaultConnection=Host=db;Database=contoso_dev;"
            "Username=devuser;Password=devpass\n"
            "      - ElasticSearch__Url=http://elasticsearch:9200\n"
            "    depends_on:\n"
            "      db:\n"
            "        condition: service_healthy\n"
            "    networks:\n"
            "      - contoso-net\n\n"
            "  db:\n"
            "    image: postgres:16-alpine\n"
            "    environment:\n"
            "      - POSTGRES_DB=contoso_dev\n"
            "      - POSTGRES_USER=devuser\n"
            "      - POSTGRES_PASSWORD=devpass\n"
            "    volumes:\n"
            "      - pgdata:/var/lib/postgresql/data\n"
            "      - ./init-scripts:/docker-entrypoint-initdb.d\n"
            "    healthcheck:\n"
            "      test: ['CMD-SHELL', 'pg_isready -U devuser -d contoso_dev']\n"
            "      interval: 5s\n"
            "      timeout: 5s\n"
            "      retries: 5\n"
            "    networks:\n"
            "      - contoso-net\n\n"
            "  cache:\n"
            "    image: redis:7-alpine\n"
            "    ports:\n"
            "      - '6379:6379'\n"
            "    networks:\n"
            "      - contoso-net\n\n"
            "  elasticsearch:\n"
            "    image: docker.elastic.co/elasticsearch/elasticsearch:8.12.0\n"
            "    environment:\n"
            "      - discovery.type=single-node\n"
            "      - xpack.security.enabled=false\n"
            "      - 'ES_JAVA_OPTS=-Xms512m -Xmx512m'\n"
            "    volumes:\n"
            "      - esdata:/var/lib/elasticsearch/data\n"
            "    healthcheck:\n"
            "      test: ['CMD-SHELL', 'curl -sf http://localhost:9200/_cluster/health']\n"
            "      interval: 10s\n"
            "      timeout: 10s\n"
            "      retries: 10\n"
            "    networks:\n"
            "      - contoso-net\n\n"
            "  worker:\n"
            "    build:\n"
            "      context: ./worker\n"
            "    environment:\n"
            "      - REDIS_URL=redis://cache:6379/1\n"
            "      - DATABASE_URL=postgresql://devuser:devpass@db:5432/contoso_dev\n"
            "    depends_on:\n"
            "      - cache\n"
            "      - db\n"
            "    networks:\n"
            "      - contoso-net\n\n"
            "volumes:\n"
            "  pgdata:\n"
            "  esdata:\n\n"
            "networks:\n"
            "  contoso-net:\n"
            "    driver: bridge\n\n"
            "The error I get is:\n"
            "Error response from daemon: failed to create network contoso-net: could not"
            " find an available, non-overlapping IPv4 address pool.\n\n"
            "I think I have too many Docker networks already but I'm not sure what to clean up.",
            "Dev docker-compose environment fails to start with 'could not find"
            " an available, non-overlapping IPv4 address pool' error on network"
            " creation. Full 7-service docker-compose.yml (web, api, db, cache,"
            " elasticsearch, worker) pasted in ticket. User suspects too many"
            " existing Docker networks.",
        ),
        gold=ScenarioGold(
            category="Software & Applications",
            priority="P3",
            assigned_team="Enterprise Applications",
            needs_escalation=False,
            missing_information=("environment_details",),
            next_best_action="Resolve Docker network address pool exhaustion — prune"
            " unused Docker networks so the dev compose stack can create its"
            " bridge network",
            remediation_steps=(
                "Run 'docker network ls' and 'docker network prune' to clean up unused networks",
                "If pruning is insufficient, manually remove stale networks from old compose projects",
                "Consider assigning a specific subnet in the docker-compose.yml to avoid pool conflicts",
                "Verify the compose stack starts successfully after network cleanup",
                "Document the network cleanup procedure for the development team to avoid recurrence",
            ),
        ),
        tags=("data-cleanup", "docker-compose-yaml", "config-dump"),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 47. OCR'd financial report with character confusion
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="dc-gen-047",
        subjects=(
            "Need he1p with quarter1y report — OCR scan has errors",
            "F1nancial report PDF won't import — bad OCR characters",
        ),
        descriptions=(
            "I scanned our Q4 financial report to import into the ERP but the OCR"
            " is terrible. Here's a sample of what it produced:\n\n"
            "CONT0SO CORP — Q4 2025 F1NANC1AL SUMMARY\n"
            "Prepared by: 0ffice of the CF0\n"
            "Date: January l5, 2O26\n\n"
            "REVENUE BREAKD0WN (in $OOOs)\n"
            "                          Q4 2025    Q3 2O25    YoY %\n"
            "Product Sa1es            $l2,847     $ll,293    +l3.8%\n"
            "Service Revenue          $ 8,4l9     $ 7,88O    + 6.8%\n"
            "Subscripti0n Fees        $ 6,2O3     $ 5,9l4    + 4.9%\n"
            "Licensing & R0ya1ties    $ 3,l87     $ 2,95O    + 8.O%\n"
            "                         --------    --------\n"
            "T0TAL REVENUE            $3O,656     $28,O37    + 9.3%\n\n"
            "0PERATING EXPENSES\n"
            "C0st of G0ods So1d       $l4,2l2     $l3,467    + 5.5%\n"
            "R&D Expenditure          $ 4,8O3     $ 4,5l9    + 6.3%\n"
            "Sa1es & Marketing        $ 3,97l     $ 3,7l2    + 7.O%\n"
            "G&A / 0verhead           $ 2,l48     $ 2,Ol7    + 6.5%\n"
            "Deprec1ati0n & Am0rt.    $ l,234     $ l,l89    + 3.8%\n"
            "                         --------    --------\n"
            "T0TAL 0PEX               $26,368     $24,9O4    + 5.9%\n\n"
            "NET 1NC0ME               $ 4,288     $ 3,l33    +36.9%\n\n"
            "The ERP import keeps rejecting it because the numbers have letter"
            " substitutions (1 vs l, 0 vs O). This is a 47-page report and I"
            " can't manually fix all of it. The original was printed on a dot-matrix"
            " printer so re-scanning doesn't help.",
            "User needs to import a 47-page Q4 financial report into the ERP"
            " but OCR produced systematic character confusion — '1' vs 'l',"
            " '0' vs 'O', etc. ERP rejects the data. Original was dot-matrix"
            " printed so re-scanning won't help. Ticket contains sample OCR"
            " output with garbled financial figures.",
        ),
        gold=ScenarioGold(
            category="Software & Applications",
            priority="P3",
            assigned_team="Enterprise Applications",
            needs_escalation=False,
            missing_information=("screenshot_or_attachment",),
            next_best_action="Help the user correct OCR character-confusion errors in"
            " the 47-page financial report so it can be imported into the ERP —"
            " a post-processing script to fix common l/1 and O/0 substitutions"
            " is likely the fastest path",
            remediation_steps=(
                "Develop or provide a post-processing script to fix common OCR"
                " substitutions (l→1, O→0) in numeric fields",
                "Run the corrected output through ERP import validation in a staging environment first",
                "Investigate higher-quality OCR software or settings that handle dot-matrix print better",
                "Validate the corrected financial figures against a known summary before final ERP import",
                "Recommend scanning future dot-matrix documents with enhanced OCR preprocessing for better accuracy",
            ),
        ),
        tags=("data-cleanup", "ocr-artifacts", "character-confusion"),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 48. Quoted-printable encoding artifacts
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="dc-gen-048",
        subjects=(
            "Email from vendor looks garbled =E2=80=94 can=27t read it",
            "Procurement email full of =3D and =20 characters",
        ),
        descriptions=(
            "I received an important email from our vendor but it's full of strange"
            " characters. Here's what it looks like:\n\n"
            "From: procurement@fabrikam.com\n"
            "Subject: Re: Contract Renewal =E2=80=94 Contoso/Fabrikam MSA 2026=\n"
            "=2D2028\n\n"
            "Hi Team,=0D=0A=0D=0APlease find attached the revised Master Service=\n"
            " Agreement for the 2026=E2=80=932028 term. Key changes include:=0D=\n"
            "=0A=0D=0A1. Annual pricing adjustment of 4.5% =E2=80=94 down from th=\n"
            "e originally proposed 7.2%=0D=0A2. SLA guarantees improved to 99.95% =\n"
            "uptime (was 99.9%)=0D=0A3. Data residency clause updated per your le=\n"
            "gal team=E2=80=99s requirements=0D=0A4. Payment terms extended to Net=\n"
            " 45 (was Net 30)=0D=0A5. Auto-renewal opt=E2=80=91out window changed =\n"
            "to 90 days=0D=0A=0D=0AThe total contract value for the 3=E2=80=91year=\n"
            " term is $2,340,000 =E2=80=94 broken down as:=0D=0A=E2=80=A2 Year 1:=\n"
            " $740,000=0D=0A=E2=80=A2 Year 2: $770,000=0D=0A=E2=80=A2 Year 3: $83=\n"
            "0,000=0D=0A=0D=0AWe need signatures by March 28, 2026 to maintain cur=\n"
            "rent pricing.=0D=0A=0D=0ABest regards,=0D=0ASanjay Mehta=0D=0AVP Ente=\n"
            "rprise Sales=0D=0AFabrikam Inc.\n\n"
            "I need to read this properly and forward it to legal. The attachment"
            " also has the same encoding issue. This is blocking a $2.3M contract"
            " renewal.",
            "Vendor contract renewal email from Fabrikam arrived with raw"
            " quoted-printable encoding visible (=E2=80=94, =0D=0A, soft line"
            " breaks with trailing =). User cannot read the $2.3M MSA details."
            " Attachment similarly affected. Needs resolution before March 28"
            " signature deadline.",
        ),
        gold=ScenarioGold(
            category="Software & Applications",
            priority="P2",
            assigned_team="Enterprise Applications",
            needs_escalation=False,
            missing_information=("error_message", "environment_details"),
            next_best_action="Fix the email rendering issue that is displaying raw"
            " quoted-printable encoding — likely an Outlook or Exchange"
            " transport rule stripping Content-Transfer-Encoding headers",
            remediation_steps=(
                "Check Exchange transport rules for any that modify or strip"
                " email headers including Content-Transfer-Encoding",
                "Verify the user's Outlook client is up to date and not using a legacy rendering mode",
                "Provide the user with a decoded version of the email content as an immediate workaround",
                "Test inbound email rendering from the same sender with a clean message to isolate the issue",
                "Coordinate with Fabrikam to resend the contract email if the attachment is also corrupted",
            ),
        ),
        tags=("data-cleanup", "quoted-printable", "encoding-artifacts"),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 49. ServiceNow audit trail / state transitions
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="dc-gen-049",
        subjects=(
            "SAP login broken — see ServiceNow ticket history for context",
            "Can't access SAP — this has been bounced around for 3 weeks (audit trail below)",
        ),
        descriptions=(
            "I STILL can't log into SAP and this ticket has been open for 3 weeks."
            " Here's the full audit trail from ServiceNow — maybe someone can finally"
            " figure out what's going on:\n\n"
            "INC0038471 — State Transitions:\n"
            "────────────────────────────────\n"
            "2026-02-18 09:12 | New → Assigned | Agent: Auto-Router\n"
            "  Assignment Group: Service Desk L1\n"
            "  Notes: Auto-classified as 'Software & Applications'\n\n"
            "2026-02-18 11:45 | Assigned → In Progress | Agent: Tom Richards\n"
            "  Work Notes: Contacted user, confirmed SAP GUI 8.0 login fails with"
            " error 'No RFC authorization for function SYST_LOGIN'. Resetting"
            " user's SAP password.\n\n"
            "2026-02-18 14:22 | In Progress → Pending | Agent: Tom Richards\n"
            "  Notes: Password reset completed. Waiting for user to confirm.\n\n"
            "2026-02-19 08:55 | Pending → In Progress | Agent: Tom Richards\n"
            "  Notes: User reports same error after password reset. Escalating.\n\n"
            "2026-02-19 09:10 | In Progress → Assigned | Agent: Tom Richards\n"
            "  Assignment Group: Enterprise Applications\n"
            "  Escalation Notes: Password reset did not resolve. Likely an"
            " authorization object issue, not credentials.\n\n"
            "2026-02-21 16:00 | Assigned → In Progress | Agent: Priya Sharma\n"
            "  Work Notes: Checked user's SAP role assignments. User has"
            " SAP_BASIC_USER role but missing S_RFC authorization object."
            " Need Basis team to add it.\n\n"
            "2026-02-21 16:15 | In Progress → Assigned | Agent: Priya Sharma\n"
            "  Assignment Group: SAP Basis\n"
            "  Notes: Need S_RFC auth object added to user's composite role.\n\n"
            "2026-02-28 09:00 | Assigned → In Progress | Agent: Klaus Weber\n"
            "  Work Notes: Reviewing request. This requires a role change in"
            " production — needs change request.\n\n"
            "2026-02-28 09:30 | In Progress → Pending | Agent: Klaus Weber\n"
            "  Notes: CHG0012847 created. Pending CAB approval for role change.\n\n"
            "2026-03-04 14:00 | Pending → In Progress | Agent: Klaus Weber\n"
            "  Notes: CAB approved CHG0012847. Implementing in next maintenance"
            " window (Saturday 03/08).\n\n"
            "2026-03-10 08:30 | In Progress → Pending | Agent: Klaus Weber\n"
            "  Notes: Change implemented Saturday. Waiting for user confirmation.\n\n"
            "It's Monday and I STILL can't log in. The error is different now —"
            " 'User is locked' instead of the RFC error. I think someone locked"
            " my account during the change.",
            "SAP login issue open 3 weeks (INC0038471). Originally RFC"
            " authorization error, escalated through L1 → Enterprise Apps"
            " → SAP Basis with a CAB-approved change. Change was implemented"
            " but now user gets 'User is locked' error instead. Full"
            " ServiceNow audit trail with 11 state transitions pasted in"
            " the ticket.",
        ),
        gold=ScenarioGold(
            category="Software & Applications",
            priority="P2",
            assigned_team="Enterprise Applications",
            needs_escalation=False,
            missing_information=("error_message",),
            next_best_action="Unlock the SAP user account that was likely locked during"
            " the weekend maintenance change — the original RFC authorization"
            " fix may be in place but the account lock is a secondary issue"
            " from the implementation",
            remediation_steps=(
                "Unlock the user's SAP account immediately via SU01 or the user admin transaction",
                "Verify the S_RFC authorization object was correctly added to the user's composite role",
                "Test SAP GUI login with the user to confirm both the lock and the original RFC error are resolved",
                "Review the change implementation steps to understand why the account was locked during maintenance",
                "Close both the incident and the associated change request after confirmation",
            ),
        ),
        tags=("data-cleanup", "servicenow-audit-trail", "state-transitions"),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 50. Bloomberg terminal fixed-width output
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="dc-gen-050",
        subjects=(
            "Bloomberg terminal not updating — screenshot text dump included",
            "BBG data feed frozen — pasted terminal output below",
        ),
        descriptions=(
            "My Bloomberg terminal stopped updating around 10:15 AM. I copied the"
            " screen output to show what I'm seeing:\n\n"
            "┌─────────────────────────────────────────────────────────────────────┐\n"
            "│ BLOOMBERG PROFESSIONAL                          Mar 10, 2026 10:15 │\n"
            "│ TOP <GO>                                                           │\n"
            "├─────────────────────────────────────────────────────────────────────┤\n"
            "│ EQUITY MONITOR — US LARGE CAP (STALE DATA WARNING)                 │\n"
            "│                                                                    │\n"
            "│ Ticker    Last      Chg     %Chg     Vol(K)    Bid      Ask        │\n"
            "│ ────────  ────────  ──────  ──────   ────────  ───────  ───────    │\n"
            "│ AAPL US   187.42    +1.23   +0.66%   12,847    187.41   187.43     │\n"
            "│ MSFT US   428.91    +3.17   +0.74%    8,234    428.90   428.92     │\n"
            "│ GOOGL US  172.55    -0.89   -0.51%    6,412    172.54   172.56     │\n"
            "│ AMZN US   198.33    +2.45   +1.25%    9,871    198.32   198.34     │\n"
            "│ NVDA US   892.10    +8.72   +0.99%   15,923    892.08   892.12     │\n"
            "│ META US   512.67    +4.38   +0.86%    7,156    512.66   512.68     │\n"
            "│ TSLA US   178.24    -3.91   -2.15%   22,448    178.23   178.25     │\n"
            "│ BRK/B US  418.50    +1.05   +0.25%    2,847    418.49   418.51     │\n"
            "│                                                                    │\n"
            "│ ** DATA AS OF 10:15:42 — FEED INTERRUPTED — LAST UPDATE 47 MIN **  │\n"
            "│                                                                    │\n"
            "│ FX SNAPSHOT (STALE)          RATES (STALE)                          │\n"
            "│ EUR/USD  1.0847  +0.0012     UST 2Y   4.587%  +0.023              │\n"
            "│ GBP/USD  1.2734  -0.0008     UST 10Y  4.218%  +0.015              │\n"
            "│ USD/JPY  148.23  +0.42       UST 30Y  4.442%  +0.008              │\n"
            "│ USD/CHF  0.8812  +0.0015     FED FF   5.375%  unch                │\n"
            "│                                                                    │\n"
            "│ ALERTS: Connection to B-PIPE lost at 10:15:42                      │\n"
            "│         Attempting reconnect... (attempt 23/50)                     │\n"
            "│         Last successful heartbeat: 10:14:58                        │\n"
            "└─────────────────────────────────────────────────────────────────────┘\n\n"
            "I'm a portfolio manager and I need live data for trading. The B-PIPE"
            " connection has been trying to reconnect for almost an hour. Other"
            " people on the floor seem to be working fine.",
            "Bloomberg terminal B-PIPE data feed disconnected at 10:15 AM for a"
            " single portfolio manager. Terminal shows 'Connection to B-PIPE lost'"
            " and has been attempting reconnect for ~47 minutes. Other users on"
            " the same floor are unaffected. User pasted full fixed-width"
            " terminal screen output including stale equity and FX data.",
        ),
        gold=ScenarioGold(
            category="Software & Applications",
            priority="P1",
            assigned_team="Enterprise Applications",
            needs_escalation=True,
            missing_information=("device_info", "environment_details"),
            next_best_action="Restore Bloomberg B-PIPE connectivity for the portfolio"
            " manager — the data feed has been stale for nearly an hour during"
            " active trading, affecting trading decisions",
            remediation_steps=(
                "Restart the Bloomberg Terminal application and re-authenticate the B-PIPE connection",
                "Check the local network connection and switch ports"
                " — other users are unaffected so this may be workstation-specific",
                "Verify the Bloomberg Anywhere license and B-PIPE entitlements are active for this user",
                "Contact Bloomberg Technical Support if the reconnection continues to fail after restart",
                "Provide the user with Bloomberg web access as a temporary workaround for live market data",
            ),
        ),
        tags=("data-cleanup", "bloomberg-terminal", "fixed-width-output"),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 51. Excel formula clipboard artifacts
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="dc-gen-051",
        subjects=(
            "Excel formulas showing instead of values — pasted broken data below",
            "Copied from Excel but ticket has raw formulas — budget approval needed",
        ),
        descriptions=(
            "I need help with our department budget file. When I copied the summary"
            " to email my manager, the formulas came through instead of the values."
            " Here's what I see:\n\n"
            "FY2026 Department Budget — Marketing\n\n"
            "Category               Q1           Q2           Q3           Q4           Total\n"
            "──────────────────────────────────────────────────────────────────────────────────\n"
            "Headcount Costs        =SUM(B3:B14) =SUM(C3:C14) =SUM(D3:D14) =SUM(E3:E14) =SUM(B15:E15)\n"
            "Contractor Budget      =B16*1.15    =C16*1.15    =D16*1.15    =E16*1.15    =SUM(B17:E17)\n"
            'Software Licenses      =VLOOKUP("MKT",Licensing!A:F,3,FALSE) =VLOOKUP("MKT",'
            'Licensing!A:F,4,FALSE) =VLOOKUP("MKT",Licensing!A:F,5,FALSE) =VLOOKUP("MKT",'
            "Licensing!A:F,6,FALSE) =SUM(B18:E18)\n"
            "Travel & Events        ='Prior Year'!B18*1.08 ='Prior Year'!C18*1.08"
            " ='Prior Year'!D18*1.08 ='Prior Year'!E18*1.08 =SUM(B19:E19)\n"
            'Digital Ad Spend       =INDEX(AdBudget,MATCH("Q1",AdBudget[Quarter],0),'
            'MATCH("Marketing",AdBudget[#Headers],0)) =INDEX(AdBudget,MATCH("Q2",'
            'AdBudget[Quarter],0),MATCH("Marketing",AdBudget[#Headers],0)) =INDEX('
            'AdBudget,MATCH("Q3",AdBudget[Quarter],0),MATCH("Marketing",AdBudget'
            '[#Headers],0)) =INDEX(AdBudget,MATCH("Q4",AdBudget[Quarter],0),MATCH('
            '"Marketing",AdBudget[#Headers],0)) =SUM(B20:E20)\n'
            "Agency Fees            =IF(B20>50000,B20*0.12,B20*0.15) =IF(C20>50000,"
            "C20*0.12,C20*0.15) =IF(D20>50000,D20*0.12,D20*0.15) =IF(E20>50000,"
            "E20*0.12,E20*0.15) =SUM(B21:E21)\n"
            "──────────────────────────────────────────────────────────────────────────────────\n"
            "TOTAL                  =SUM(B15:B21) =SUM(C15:C21) =SUM(D15:D21) =SUM(E15:E21)"
            " =SUM(F15:F21)\n"
            "vs Budget Cap          =B22-Budget_Cap_Q1 =C22-Budget_Cap_Q2 =D22-Budget_Cap_Q3"
            " =E22-Budget_Cap_Q4 =F22-Annual_Cap\n"
            'Status                 =IF(B23>0,"OVER","OK") =IF(C23>0,"OVER","OK")'
            ' =IF(D23>0,"OVER","OK") =IF(E23>0,"OVER","OK") =IF(F23>0,"OVER BUDGET",'
            '"WITHIN BUDGET")\n\n'
            "The real issue is: the file won't open anymore. When I try to open it I get"
            " 'Excel cannot open the file because the file format or extension is not"
            " valid.' It was working fine yesterday and it's on SharePoint. I need this"
            " for a budget review meeting tomorrow morning.",
            "Marketing budget Excel file on SharePoint won't open — 'file format"
            " or extension is not valid' error. User pasted clipboard content"
            " showing raw Excel formulas (SUM, VLOOKUP, INDEX/MATCH, IF) instead"
            " of computed values. Budget review meeting tomorrow. File was"
            " working yesterday.",
        ),
        gold=ScenarioGold(
            category="Software & Applications",
            priority="P2",
            assigned_team="Enterprise Applications",
            needs_escalation=False,
            missing_information=("error_message", "screenshot_or_attachment"),
            next_best_action="Recover the corrupted Excel budget file from SharePoint"
            " version history — the formulas in the ticket are clipboard artifacts"
            " and not useful for recovery; focus on restoring a working version"
            " before tomorrow's budget meeting",
            remediation_steps=(
                "Restore a previous version of the Excel file from SharePoint version history",
                "If no clean version exists, attempt to open the file with Excel's Open and Repair feature",
                "Verify the recovered file's formulas and cross-sheet references are intact",
                "Save a local backup copy before re-uploading to SharePoint to prevent further corruption",
                "Investigate whether a recent SharePoint sync or co-authoring conflict caused the corruption",
            ),
        ),
        tags=("data-cleanup", "excel-formulas", "clipboard-artifacts"),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 52. Very long email with buried issue — rambling before real ask
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="dc-gen-052",
        subjects=(
            "Quick question — also hi, how was your weekend?",
            "Hey IT! Some stuff + a tiny laptop problem at the end",
        ),
        descriptions=(
            "Hey team!! Hope everyone had a great weekend. Mine was honestly SO good —"
            " my sister-in-law came up from Philadelphia and we went to that new brunch"
            " place on 5th Street, you know the one with the huge pancakes? Anyway we"
            " ended up walking around the park for like two hours after and my feet are"
            " STILL sore haha.\n\n"
            "Oh also — did anyone else notice the parking garage on Level 2 was super"
            " full on Friday? I had to circle for 15 minutes. I think they need to open"
            " up the overflow lot again. Maybe facilities can look into that? Not sure"
            " if that's you guys or someone else.\n\n"
            "Speaking of Friday, the coffee machine on the 4th floor was making that"
            " weird grinding noise again. Last time it did that it broke for like a"
            " week and we all had to go to the 3rd floor. If someone could put in a"
            " maintenance request that would be amazing. Or maybe I should do it"
            " myself? Who handles that?\n\n"
            "Also random but does anyone know if the holiday party is confirmed for"
            " December 12th? My team needs to plan around it for a client demo.\n\n"
            "OH WAIT the actual reason I'm emailing — my laptop docking station stopped"
            " outputting to my external monitors this morning. I get to my desk, plug"
            " everything in, and both screens stay black. The laptop screen works fine."
            " I tried unplugging and replugging. The dock is a Dell WD19TBS and my"
            " laptop is a ThinkPad T14s Gen 4. It was working fine last Thursday."
            " My employee ID is 50321 and I'm on Floor 4, Building A, desk 4-217.\n\n"
            "Thanks so much!! Have a great day \U0001f60a",
            "Rambling email mostly about weekend, parking, coffee machine, and holiday"
            " party. Actual issue buried at the very end: Dell WD19TBS docking station"
            " not outputting to external monitors since Monday morning. Laptop is a"
            " ThinkPad T14s Gen 4. Both screens stay black when docked; laptop display"
            " works. Floor 4, Building A, desk 4-217.",
        ),
        gold=ScenarioGold(
            category="Hardware & Peripherals",
            priority="P3",
            assigned_team="Endpoint Engineering",
            needs_escalation=False,
            missing_information=("error_message", "device_info"),
            next_best_action="Troubleshoot the Dell WD19TBS docking station display output"
            " failure — the buried issue is that both external monitors stay black"
            " when docked; ignore the unrelated rambling about parking, coffee"
            " machines, and holiday planning",
            remediation_steps=(
                "Update the Dell WD19TBS dock firmware using Dell Dock Updater utility",
                "Check the ThinkPad T14s display output settings and ensure external displays are detected in Device "
                "Manager",
                "Test with a different dock or direct HDMI/USB-C connection to isolate the faulty component",
                "If firmware update does not resolve, swap the docking station with a known-good unit from inventory",
            ),
        ),
        tags=("data-cleanup", "buried-issue", "rambling"),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 53. Base64-encoded PDF inline — pasted compliance report
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="dc-gen-053",
        subjects=(
            "Compliance audit failed — full PDF report attached inline below",
            "URGENT: SOX compliance scan results (see encoded report)",
        ),
        descriptions=(
            "We just got the results back from our quarterly SOX compliance scan and"
            " there are critical findings. I couldn't figure out how to attach the PDF"
            " to this ticket so I'm pasting the base64 of the report below. Can someone"
            " from Security Ops review ASAP?\n\n"
            "--- BEGIN COMPLIANCE REPORT PDF (base64) ---\n"
            "JVBERi0xLjcKCjEgMCBvYmoKPDwKL1R5cGUgL0NhdGFsb2cKL1BhZ2VzIDIg"
            "MCBSCL9PdXRsaW5lcyA1IDAgUgo+PgplbmRvYmoKCjIgMCBvYmoKPDwKL1R5"
            "cGUgL1BhZ2VzCi9LaWRzIFszIDAgUl0KL0NvdW50IDEKL01lZGlhQm94IFsw"
            "IDAgNjEyIDc5Ml0KPj4KZW5kb2JqCgozIDAgb2JqCjw8Ci9UeXBlIC9QYWdl"
            "Ci9QYXJlbnQgMiAwIFIKL01lZGlhQm94IFswIDAgNjEyIDc5Ml0KL0NvbnRl"
            "bnRzIDQgMCBSCi9SZXNvdXJjZXMgPDwgL0ZvbnQgPDwgL0YxIDYgMCBSID4+"
            "ID4+Cj4+CmVuZG9iagouLi4KU09YIENvbXBsaWFuY2UgU2NhbiBSZXBvcnQg"
            "LSBRMSA2MDI2CkNSSVRJQ0FMIEZJRE5JTkdTOiAzCi0gVW5lbmNyeXB0ZWQg"
            "UERJIHN0b3JhZ2UgaW4gUzMgYnVja2V0ICJmaW4tcmVwb3J0cy1wcm9kIgot"
            "IFN0YWxlIHNlcnZpY2UgYWNjb3VudCB3aXRoIGFkbWluIHByaXZpbGVnZXMg"
            "KGxhc3Qgcm90YXRlZCAyMDI0LTAyLTE4KQotIE1pc3NpbmcgYXVkaXQgbG9n"
            "Z2luZyBvbiAzIHByb2R1Y3Rpb24gZGF0YWJhc2VzCi4uLgo0IDAgb2JqCjw8"
            "Ci9MZW5ndGggNDQKPj4Kc3RyZWFtCkJUCi9GMSAxMiBUZgo3MiA3MjAgVGQK"
            "KFNPWCBDb21wbGlhbmNlIFNjYW4gUmVwb3J0IC0gUTEgMjAyNikgVGoKRVQK"
            "ZW5kc3RyZWFtCmVuZG9iago=\n"
            "--- END COMPLIANCE REPORT PDF ---\n\n"
            "The critical findings are:\n"
            "1. Unencrypted PII storage in the S3 bucket 'fin-reports-prod'\n"
            "2. A stale service account with admin privileges not rotated since Feb 2024\n"
            "3. Missing audit logging on 3 production databases\n\n"
            "We need to remediate before the external auditors arrive on March 28th.",
            "SOX compliance scan returned 3 critical findings: unencrypted PII in"
            " S3 bucket 'fin-reports-prod', stale admin service account (last"
            " rotated 2024-02-18), and missing audit logging on 3 production"
            " databases. User pasted base64-encoded PDF inline instead of"
            " attaching. External auditors arrive March 28th.",
        ),
        gold=ScenarioGold(
            category="Security & Compliance",
            priority="P2",
            assigned_team="Security Operations",
            needs_escalation=False,
            missing_information=("environment_details", "affected_system"),
            next_best_action="Triage the three critical SOX findings — the base64 block is a"
            " PDF artifact and should be decoded or ignored; focus on the plaintext"
            " summary identifying unencrypted PII, stale admin credentials, and"
            " missing audit logging ahead of the March 28th audit deadline",
            remediation_steps=(
                "Enable server-side encryption (SSE-S3 or SSE-KMS) on the 'fin-reports-prod' S3 bucket and audit "
                "existing unencrypted objects",
                "Rotate the stale service account credentials immediately and enforce an automated rotation policy",
                "Enable audit logging on the three production databases and verify log delivery to the SIEM",
                "Request the user attach the PDF properly for archival and remove the inline base64 from the ticket",
            ),
        ),
        tags=("data-cleanup", "pdf-embed", "base64"),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 54. Mobile autocorrect mangling — garbled technical terms
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="dc-gen-054",
        subjects=(
            "Saleforce dadhboard not loading — sent from my iPhone",
            "Can't axcess the CRM reporting — typos sry on phone",
        ),
        descriptions=(
            "Hay, sending this from my phone bc I'm traveling and can't get to my"
            " laptop. The Saleforce dashbored hasn't been loading since this morning."
            ' When I click on the "Quartly Revenu Summery" report it just spins'
            ' forever and then shows a massage that says something like "reprot'
            ' execution timed out exceeded maximum querry complicity."\n\n'
            "I tired clearing my bowser cache and cockes (using Chrom on my iPhone)"
            " but same problm. My manger needs the Q1 piepline numbers for a bored"
            " meeting at 3pm tody so this is prety urget.\n\n"
            "I'm in the EST timezone, my Saleforce username is jthompson@contoso.com"
            ' and I\'m in the "North Amercia Sales" busness unit. The dahsboard I'
            ' need is called "Q1 FY26 Piepline Anaylsis" in the "Executve'
            ' Reprots" folder.\n\n'
            "Plese advise ASPA. Thx.\n\n"
            "Sent form my iPhone",
            "Salesforce dashboard 'Q1 FY26 Pipeline Analysis' in the 'Executive"
            " Reports' folder is not loading — report execution times out with a"
            " query complexity error. User is jthompson@contoso.com in North"
            " America Sales. Sent from mobile with heavy autocorrect garbling."
            " Manager needs pipeline numbers for board meeting at 3 PM EST today.",
        ),
        gold=ScenarioGold(
            category="Software & Applications",
            priority="P3",
            assigned_team="Enterprise Applications",
            needs_escalation=False,
            missing_information=("error_message", "application_version"),
            next_best_action="Investigate the Salesforce report execution timeout on the"
            " 'Q1 FY26 Pipeline Analysis' dashboard — the autocorrect-mangled"
            " text obscures the actual error which is likely a SOQL query"
            " complexity limit; check report filters and row counts",
            remediation_steps=(
                "Check the Salesforce report execution logs for jthompson@contoso.com to identify the SOQL query limit "
                "error",
                "Review the 'Q1 FY26 Pipeline Analysis' report filters and reduce the query scope or add "
                "index-friendly "
                "filters",
                "If the report is too complex, break it into smaller sub-reports or use an async report export",
                "Provide the user with a temporary exported CSV of the pipeline data for the 3 PM board meeting",
            ),
        ),
        tags=("data-cleanup", "autocorrect", "mobile-input"),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 55. Voicemail speech-to-text transcription — badly transcribed
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="dc-gen-055",
        subjects=(
            "Voicemail transcription from ext 4471 — network issue in warehouse",
            "[Auto-Transcribed VM] Network down in building — please call back",
        ),
        descriptions=(
            "[Voicemail Auto-Transcription \u2014 Confidence: 42%]\n"
            "From: Extension 4471 | Duration: 1m 23s | Received: 2026-03-11 07:14 EST\n\n"
            '"Hey this is uh Marcus from the wear house... the uh the wife eye is'
            " completely down on the floor sense about six this mourning. We can't"
            " scan any of the bar coats on the in ventory and the fork lift tracking"
            " system is showing off line too. We got a big sip mint going out at"
            " ate AM and if we can't get the scanners working we're gonna have to"
            " do everything man yule which will put us behind at least three ours.\n\n"
            "I think it might be the axe says point near dock for because that's"
            " where the signal is the wurst. We had a sim lure issue too weeks a go"
            " and some one from net work came and re set the thing on the sealing.\n\n"
            "Can you guys send some one out here as soon as poss a bull? My sell"
            " is 555-0147 or just call the wear house main line at extension for"
            ' for seven one. Tanks."\n\n'
            "[End of Transcription]",
            "[Auto-transcribed voicemail from warehouse ext 4471] Wi-Fi is"
            " completely down on the warehouse floor since 6 AM. Barcode"
            " scanners and forklift tracking system are offline. Large"
            " shipment going out at 8 AM \u2014 will need manual processing if"
            " not fixed. Suspects access point near Dock 4. Similar issue"
            " 2 weeks ago resolved by resetting AP on ceiling. Contact:"
            " cell 555-0147 or ext 4471.",
        ),
        gold=ScenarioGold(
            category="Network & Connectivity",
            priority="P2",
            assigned_team="Network Operations",
            needs_escalation=False,
            missing_information=("network_location", "device_info"),
            next_best_action="Dispatch a network technician to the warehouse floor to check the"
            " access point near Dock 4 \u2014 the speech-to-text transcription is heavily"
            " garbled but the core issue is a complete Wi-Fi outage affecting barcode"
            " scanners and forklift tracking with an 8 AM shipment deadline",
            remediation_steps=(
                "Remotely check the status of the warehouse access point near Dock 4 in the wireless controller "
                "dashboard",
                "If the AP is unreachable, dispatch a technician to power-cycle or replace it on-site",
                "Verify all warehouse barcode scanners and forklift tracking devices reconnect after the AP is "
                "restored",
                "Review the previous incident from two weeks ago to determine if this is a recurring hardware failure "
                "requiring permanent replacement",
            ),
        ),
        tags=("data-cleanup", "voicemail", "speech-to-text"),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 56. Zero-width Unicode characters — invisible chars in text
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="dc-gen-056",
        subjects=(
            "SSO lo\u200bgin fai\u200bling \u2014 pass\u200bword re\u200bset not wor\u200bking",
            "Can\u2019t sign in to\u200b Azure\u200b AD \u200b\u2014 account locked\u200b out",
        ),
        descriptions=(
            "I\u200b can\u200b't log\u200b in to\u200b any\u200bthing since\u200b this\u200b morn\u200bing."
            " When\u200b I try\u200b to\u200b sign in\u200b to the\u200b SSO por\u200btal at"
            " https://sso\u200b.con\u200btoso\u200b.com\u200b/login I get\u200b an"
            ' error:\u200b "AADSTS\u200b50053\u200b: The\u200b account\u200b is\u200b locked'
            "\u200b because\u200b the\u200b user\u200b tried\u200b to sign\u200b in too\u200b"
            " many\u200b times\u200b with\u200b an\u200b incorrect\u200b user\u200b ID"
            '\u200b or\u200b pass\u200bword.\u200b"\n\n'
            "I\u200b tried\u200b the\u200b self\u200b-service\u200b pass\u200bword\u200b reset"
            "\u200b at\u200b https://pass\u200bword\u200breset\u200b.micro\u200bsoft\u200bonline"
            "\u200b.com\u200b but\u200b when\u200b I\u200b paste\u200b my\u200b user\u200bname"
            "\u200b (e\u200bmily\u200b.chen\u200b@con\u200btoso\u200b.com\u200b) it\u200b says"
            "\u200b \"We\u200b couldn\u200b't\u200b find\u200b an\u200b account\u200b"
            ' with\u200b that\u200b user\u200bname.\u200b"\n\n'
            "I\u200b think\u200b the\u200b user\u200bname\u200b might\u200b have\u200b invisible"
            "\u200b characters\u200b in\u200b it?\u200b I\u200b copied\u200b it\u200b from"
            "\u200b a\u200b web\u200bpage\u200b and\u200b it looks\u200b right\u200b but"
            "\u200b maybe\u200b there\u200b's something\u200b hidden.\u200b My\u200b manager"
            "\u200b said\u200b to\u200b open\u200b a\u200b ticket\u200b because\u200b I\u200b"
            " need\u200b access\u200b for\u200b client\u200b deliverables\u200b due\u200b Friday.",
            "User cannot log in to SSO portal \u2014 Azure AD error AADSTS50053"
            " (account locked). Self-service password reset also fails because"
            " the username field contains zero-width space characters (\u200b)"
            " copied from a webpage. Actual username is emily.chen@contoso.com."
            " Access needed for client deliverables due Friday.",
        ),
        gold=ScenarioGold(
            category="Access & Authentication",
            priority="P2",
            assigned_team="Identity & Access Management",
            needs_escalation=False,
            missing_information=("authentication_method", "timestamp"),
            next_best_action="Unlock the Azure AD account for emily.chen@contoso.com and advise"
            " the user that the self-service password reset failed because zero-width"
            " Unicode characters (U+200B) were embedded in the username field when"
            " pasted from a browser",
            remediation_steps=(
                "Unlock the Azure AD account for emily.chen@contoso.com via the admin portal",
                "Reset the password manually and provide temporary credentials through a secure channel",
                "Advise the user to manually type the username instead of pasting to avoid invisible Unicode "
                "characters",
                "Check Azure AD sign-in logs to confirm no unauthorized access attempts caused the lockout",
            ),
        ),
        tags=("data-cleanup", "zero-width-chars", "invisible-unicode"),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 57. Docker compose / YAML config dump — entire config pasted
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="dc-gen-057",
        subjects=(
            "Staging environment won't start — docker-compose config below",
            "HELP: containers keep crashing on staging — pasted full YAML",
        ),
        descriptions=(
            "Our staging environment has been down since last night's deploy. I'm"
            " pasting our full docker-compose.yml so you can see the setup:\n\n"
            "```yaml\n"
            "version: '3.8'\n"
            "services:\n"
            "  api-gateway:\n"
            "    image: contoso-registry.azurecr.io/api-gateway:2.14.3\n"
            "    ports:\n"
            "      - '8080:8080'\n"
            "      - '8443:8443'\n"
            "    environment:\n"
            "      - SPRING_PROFILES_ACTIVE=staging\n"
            "      - JAVA_OPTS=-Xmx512m -Xms256m\n"
            "      - DB_HOST=postgres-primary\n"
            "      - DB_PORT=5432\n"
            "      - DB_NAME=contoso_staging\n"
            "      - DB_USER=app_svc\n"
            "      - DB_PASSWORD=stg_Pr0d_2026!xK9m\n"
            "      - REDIS_URL=redis://redis-cache:6379/0\n"
            "      - JWT_SECRET=a8f5f167f44f4964e6c998dee827110c\n"
            "    depends_on:\n"
            "      - postgres-primary\n"
            "      - redis-cache\n"
            "    restart: always\n"
            "    networks:\n"
            "      - backend\n\n"
            "  worker-service:\n"
            "    image: contoso-registry.azurecr.io/worker:1.9.0\n"
            "    deploy:\n"
            "      replicas: 3\n"
            "    environment:\n"
            "      - WORKER_CONCURRENCY=4\n"
            "      - RABBITMQ_URL=amqp://rabbit-mq:5672\n"
            "      - DB_HOST=postgres-primary\n"
            "      - DB_PASSWORD=stg_Pr0d_2026!xK9m\n"
            "    depends_on:\n"
            "      - rabbit-mq\n"
            "    networks:\n"
            "      - backend\n\n"
            "  postgres-primary:\n"
            "    image: postgres:16.2\n"
            "    volumes:\n"
            "      - pgdata:/var/lib/postgresql/data\n"
            "    environment:\n"
            "      - POSTGRES_DB=contoso_staging\n"
            "      - POSTGRES_USER=app_svc\n"
            "      - POSTGRES_PASSWORD=stg_Pr0d_2026!xK9m\n"
            "    networks:\n"
            "      - backend\n\n"
            "  redis-cache:\n"
            "    image: redis:7.2-alpine\n"
            "    networks:\n"
            "      - backend\n\n"
            "  rabbit-mq:\n"
            "    image: rabbitmq:3.13-management\n"
            "    ports:\n"
            "      - '15672:15672'\n"
            "    networks:\n"
            "      - backend\n\n"
            "volumes:\n"
            "  pgdata:\n\n"
            "networks:\n"
            "  backend:\n"
            "    driver: bridge\n"
            "```\n\n"
            "The api-gateway container keeps restarting in a crash loop. The logs"
            " say 'Connection refused' to postgres on port 5432. The postgres"
            " container itself seems healthy. We need staging back for QA testing"
            " that starts tomorrow morning.",
            "Staging environment down since last night's deploy. User pasted full"
            " docker-compose.yml (contains hardcoded credentials that should be"
            " rotated). The api-gateway container is crash-looping with"
            " 'Connection refused' to postgres:5432 even though postgres appears"
            " healthy. Likely a container startup ordering or network issue."
            " QA testing starts tomorrow.",
        ),
        gold=ScenarioGold(
            category="Software & Applications",
            priority="P3",
            assigned_team="Enterprise Applications",
            needs_escalation=False,
            missing_information=("error_message", "environment_details"),
            next_best_action="Fix the staging docker-compose startup ordering issue causing"
            " api-gateway to crash-loop on postgres connection refused \u2014 also flag"
            " the hardcoded credentials in the pasted YAML for immediate rotation"
            " since they are now exposed in the ticketing system",
            remediation_steps=(
                "Add a health check and depends_on condition to the api-gateway service so it waits for postgres to be "
                "ready before starting",
                "Rotate all credentials exposed in the ticket (DB_PASSWORD, JWT_SECRET) since they were pasted in "
                "plaintext",
                "Migrate hardcoded secrets to a vault or Docker secrets to prevent future credential exposure",
                "Verify the staging environment is fully operational and run a smoke test before QA begins",
            ),
        ),
        tags=("data-cleanup", "yaml-config", "docker-compose"),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 58. Git diff pasted as ticket body
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="dc-gen-058",
        subjects=(
            "Deployment broke prod — here's the diff that caused it",
            "ROLLBACK NEEDED: bad commit pushed to main — diff inside",
        ),
        descriptions=(
            "Someone pushed a bad commit to main and now the payment processing"
            " endpoint is returning 500 errors. I grabbed the diff — can someone"
            " review and help us roll back?\n\n"
            "```diff\n"
            "diff --git a/src/services/payment/processor.py b/src/services/payment/processor.py\n"
            "index 4a2e8b1..9f3c7d2 100644\n"
            "--- a/src/services/payment/processor.py\n"
            "+++ b/src/services/payment/processor.py\n"
            "@@ -142,7 +142,7 @@ class PaymentProcessor:\n"
            "     def validate_transaction(self, txn: Transaction) -> bool:\n"
            "         if txn.amount <= 0:\n"
            '             raise InvalidAmountError(f"Invalid amount: {txn.amount}")\n'
            "-        if txn.currency in self.SUPPORTED_CURRENCIES:\n"
            "+        if txn.currency not in self.SUPPORTED_CURRENCIES:\n"
            "             return self._process_payment(txn)\n"
            "         return self._reject_unsupported(txn)\n"
            " \n"
            "@@ -167,12 +167,8 @@ class PaymentProcessor:\n"
            "     def _calculate_fees(self, amount: Decimal, region: str) -> Decimal:\n"
            "-        fee_rate = self.FEE_SCHEDULE.get(region, self.DEFAULT_FEE)\n"
            "-        if amount > Decimal('10000'):\n"
            "-            fee_rate *= Decimal('0.85')  # bulk discount\n"
            "-        return (amount * fee_rate).quantize(Decimal('0.01'))\n"
            "+        return amount * Decimal('0.05')  # simplified fee calc\n"
            " \n"
            "diff --git a/src/services/payment/gateway.py b/src/services/payment/gateway.py\n"
            "index 7b1e3f4..2d8a9c1 100644\n"
            "--- a/src/services/payment/gateway.py\n"
            "+++ b/src/services/payment/gateway.py\n"
            "@@ -89,6 +89,7 @@ class PaymentGateway:\n"
            "     async def charge(self, payment_intent: PaymentIntent) -> ChargeResult:\n"
            "+        import time; time.sleep(5)  # debugging delay TODO remove\n"
            "         try:\n"
            "             result = await self.stripe_client.charges.create(\n"
            "                 amount=payment_intent.amount_cents,\n"
            "```\n\n"
            "The logic inversion on line 145 is rejecting ALL valid currencies and"
            " accepting invalid ones. Plus someone left a debug sleep in the"
            " gateway. We're losing revenue every minute this is live.",
            "Production payment endpoint returning 500 errors after bad commit"
            " to main. User pasted git diff showing: (1) inverted currency"
            " validation logic rejecting valid currencies, (2) fee calculation"
            " replaced with hardcoded 5% ignoring bulk discounts, (3) debug"
            " time.sleep(5) left in payment gateway. Revenue impact is ongoing.",
        ),
        gold=ScenarioGold(
            category="Software & Applications",
            priority="P3",
            assigned_team="Enterprise Applications",
            needs_escalation=False,
            missing_information=("timestamp", "affected_users"),
            next_best_action="Immediately revert the bad commit on main that inverted the"
            " currency validation logic in processor.py \u2014 the git diff in the ticket"
            " shows three distinct bugs including a logic inversion, a fee calculation"
            " regression, and a debug sleep statement left in production code",
            remediation_steps=(
                "Revert the bad commit on main using git revert and deploy the fix to production immediately",
                "Verify payment processing is restored by running end-to-end transaction tests against the production "
                "endpoint",
                "Audit recent transactions processed under the inverted logic to identify and correct any mis-charged "
                "payments",
                "Add a pre-merge CI check to flag debug statements (time.sleep, print, pdb) in payment-critical code "
                "paths",
            ),
        ),
        tags=("data-cleanup", "git-diff", "code-paste"),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 59. Extremely terse ticket — almost no context
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="dc-gen-059",
        subjects=(
            "wifi down",
            "internet broken",
        ),
        descriptions=(
            "wifi doesnt work. pls fix",
            "net down. help.",
        ),
        gold=ScenarioGold(
            category="Network & Connectivity",
            priority="P3",
            assigned_team="Network Operations",
            needs_escalation=False,
            missing_information=(
                "affected_system",
                "error_message",
                "network_location",
                "device_info",
                "affected_users",
                "timestamp",
            ),
            next_best_action="Contact the user to gather basic information before any"
            " troubleshooting can begin \u2014 the ticket contains virtually no"
            " actionable detail about the Wi-Fi issue including location,"
            " device, scope of impact, or error messages",
            remediation_steps=(
                "Reach out to the user to determine their physical location, device type, and whether other users are "
                "affected",
                "Ask the user for the specific error message or symptom (no connection at all, intermittent drops, "
                "slow "
                "speed)",
                "Once location is known, check the wireless controller for AP status in that area",
                "After gathering sufficient context, proceed with standard Wi-Fi troubleshooting based on the "
                "identified symptoms",
            ),
        ),
        tags=("data-cleanup", "terse-message", "minimal-context"),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 60. Mixed LTR/RTL bidirectional text — Arabic and English mixed
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="dc-gen-060",
        subjects=(
            "\u0645\u0634\u0643\u0644\u0629 \u0641\u064a VPN \u2014 \u0644\u0627 \u0623\u0633\u062a\u0637\u064a\u0639 "
            "\u0627\u0644\u0627\u062a\u0635\u0627\u0644 \u0628\u0627\u0644\u0634\u0628\u0643\u0629 "
            "\u0627\u0644\u062f\u0627\u062e\u0644\u064a\u0629",
            "VPN connectivity issue \u2014 \u0645\u0643\u062a\u0628 \u0627\u0644\u0642\u0627\u0647\u0631\u0629 cannot "
            "reach internal resources",
        ),
        descriptions=(
            "\u0627\u0644\u0633\u0644\u0627\u0645 \u0639\u0644\u064a\u0643\u0645\u060c\n\n"
            "\u0623\u0646\u0627 \u0623\u0639\u0645\u0644 \u0645\u0646 \u0645\u0643\u062a\u0628 "
            "\u0627\u0644\u0642\u0627\u0647\u0631\u0629 \u200f(Cairo office, Building 2, Floor 3)\u200f "
            "\u0648\u0644\u0627 \u0623\u0633\u062a\u0637\u064a\u0639"
            "\u0627\u0644\u0627\u062a\u0635\u0627\u0644 \u0628\u0640 \u200finternal SharePoint\u200f \u0623\u0648 "
            "\u200fJira\u200f"
            "\u0645\u0646\u0630 \u0635\u0628\u0627\u062d \u0627\u0644\u064a\u0648\u0645. \u0627\u0644\u0640 \u200fVPN "
            "client\u200f"
            "(\u200fGlobalProtect 6.1\u200f) \u064a\u062a\u0635\u0644 \u0628\u0646\u062c\u0627\u062d "
            "\u0648\u064a\u0638\u0647\u0631"
            '"\u200fConnected\u200f" \u0648\u0644\u0643\u0646 \u0639\u0646\u062f\u0645\u0627 '
            "\u0623\u062d\u0627\u0648\u0644"
            " \u0627\u0644\u0648\u0635\u0648\u0644 \u0625\u0644\u0649 \u200fhttps://sharepoint.contoso.com\u200f"
            ' \u064a\u0638\u0647\u0631 \u200f"ERR_CONNECTION_TIMED_OUT"\u200f.\n\n'
            "\u062c\u0631\u0628\u062a \u0627\u0644\u0622\u062a\u064a:\n"
            "1. \u200f\u200fipconfig /release\u200f \u0648 \u200fipconfig /renew\u200f \u2014 \u0644\u0645 "
            "\u064a\u0646\u062c\u062d\n"
            "2. \u0625\u0639\u0627\u062f\u0629 \u062a\u0634\u063a\u064a\u0644 \u0627\u0644\u0640 \u200fVPN "
            "client\u200f "
            "\u2014 \u0646\u0641\u0633 \u0627\u0644\u0645\u0634\u0643\u0644\u0629\n"
            "3. \u0627\u0644\u0627\u062a\u0635\u0627\u0644 \u0628\u062f\u0648\u0646 \u200fVPN\u200f "
            "\u064a\u0639\u0645\u0644 \u0628\u0634\u0643\u0644 \u0637\u0628\u064a\u0639\u064a (\u200fgoogle.com\u200f "
            "\u064a\u0639\u0645\u0644)\n\n"
            "\u0627\u0644\u0645\u0634\u0643\u0644\u0629 \u062a\u0624\u062b\u0631 \u0639\u0644\u0649 \u200f5 "
            "\u0645\u0648\u0638\u0641\u064a\u0646\u200f \u0641\u064a \u0646\u0641\u0633 "
            "\u0627\u0644\u0645\u0643\u062a\u0628."
            "\u0646\u062d\u062a\u0627\u062c \u062d\u0644 \u0639\u0627\u062c\u0644 \u0644\u0623\u0646 "
            "\u0639\u0646\u062f\u0646\u0627 \u200fdeadline\u200f \u064a\u0648\u0645 "
            "\u0627\u0644\u062e\u0645\u064a\u0633.\n\n"
            "\u0634\u0643\u0631\u0627\u064b\u060c\n"
            "\u0641\u0627\u0637\u0645\u0629 \u0627\u0644\u0632\u0647\u0631\u0627\u0621\n"
            "\u200fEmployee ID: 78234\u200f",
            "Mixed Arabic/English ticket with RTL/LTR control characters."
            " User in Cairo office (Building 2, Floor 3) reports VPN connects"
            " successfully via GlobalProtect 6.1 but internal resources"
            " (SharePoint, Jira) return ERR_CONNECTION_TIMED_OUT. External"
            " sites work without VPN. Affects 5 employees. Deadline Thursday."
            " Employee ID 78234.",
        ),
        gold=ScenarioGold(
            category="Network & Connectivity",
            priority="P2",
            assigned_team="Network Operations",
            needs_escalation=False,
            missing_information=("network_location", "configuration_details"),
            next_best_action="Investigate the split-tunnel or routing configuration for the"
            " Cairo office VPN gateway \u2014 GlobalProtect shows connected but internal"
            " resources time out while external traffic works, suggesting a tunnel"
            " routing or DNS resolution issue affecting 5 users",
            remediation_steps=(
                "Check the GlobalProtect gateway routing table and split-tunnel configuration for the Cairo office IP "
                "range",
                "Verify DNS resolution for internal hostnames (sharepoint.contoso.com) resolves correctly when VPN is "
                "connected",
                "Review recent changes to the VPN gateway or firewall rules that may have altered Cairo office routing",
                "As a temporary workaround, provide the Cairo team with direct IP addresses for SharePoint and Jira "
                "while the tunnel issue is resolved",
            ),
        ),
        tags=("data-cleanup", "bidi-text", "rtl-ltr-mixed"),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 61. Monitoring alert flood — mass of Nagios/Datadog alerts pasted
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="dc-gen-061",
        subjects=(
            "CRITICAL: 47 alerts firing across prod — Datadog dump below",
            "EVERYTHING IS DOWN — pasting all alerts from monitoring dashboard",
        ),
        descriptions=(
            "We're getting flooded with alerts. Pasting everything from Datadog:\n\n"
            "[CRITICAL] 06:01:03 UTC | host:prod-web-01 | CPU usage > 95% for 5m"
            " | value: 98.2% | monitor: prod-cpu-high\n"
            "[CRITICAL] 06:01:03 UTC | host:prod-web-02 | CPU usage > 95% for 5m"
            " | value: 97.8% | monitor: prod-cpu-high\n"
            "[CRITICAL] 06:01:03 UTC | host:prod-web-03 | CPU usage > 95% for 5m"
            " | value: 99.1% | monitor: prod-cpu-high\n"
            "[CRITICAL] 06:01:04 UTC | host:prod-web-04 | CPU usage > 95% for 5m"
            " | value: 96.5% | monitor: prod-cpu-high\n"
            "[WARNING]  06:01:05 UTC | host:prod-web-01 | Memory > 85%"
            " | value: 91.3% | monitor: prod-mem-high\n"
            "[WARNING]  06:01:05 UTC | host:prod-web-02 | Memory > 85%"
            " | value: 89.7% | monitor: prod-mem-high\n"
            "[WARNING]  06:01:05 UTC | host:prod-web-03 | Memory > 85%"
            " | value: 93.2% | monitor: prod-mem-high\n"
            "[CRITICAL] 06:01:08 UTC | service:api-gateway | HTTP 5xx rate > 10%"
            " | value: 34.7% | monitor: prod-5xx-rate\n"
            "[CRITICAL] 06:01:08 UTC | service:payment-svc | HTTP 5xx rate > 10%"
            " | value: 28.1% | monitor: prod-5xx-rate\n"
            "[CRITICAL] 06:01:08 UTC | service:auth-svc | HTTP 5xx rate > 10%"
            " | value: 22.4% | monitor: prod-5xx-rate\n"
            "[WARNING]  06:01:10 UTC | service:api-gateway | P99 latency > 2s"
            " | value: 8.4s | monitor: prod-latency-p99\n"
            "[WARNING]  06:01:10 UTC | service:payment-svc | P99 latency > 2s"
            " | value: 12.1s | monitor: prod-latency-p99\n"
            "[CRITICAL] 06:01:12 UTC | host:prod-db-primary | Disk usage > 90%"
            " | value: 94.6% | monitor: prod-disk-critical\n"
            "[CRITICAL] 06:01:12 UTC | host:prod-db-primary | Replication lag > 30s"
            " | value: 127s | monitor: prod-repl-lag\n"
            "[WARNING]  06:01:13 UTC | host:prod-db-replica-01 | Connections > 80%"
            " | value: 87% | monitor: prod-db-conn-pool\n"
            "[WARNING]  06:01:13 UTC | host:prod-db-replica-02 | Connections > 80%"
            " | value: 84% | monitor: prod-db-conn-pool\n"
            "[CRITICAL] 06:01:15 UTC | service:order-svc | Error rate > 5%"
            " | value: 41.2% | monitor: prod-error-rate\n"
            "[CRITICAL] 06:01:15 UTC | service:inventory-svc | Error rate > 5%"
            " | value: 38.9% | monitor: prod-error-rate\n"
            "[CRITICAL] 06:01:15 UTC | service:notification-svc | Error rate > 5%"
            " | value: 19.3% | monitor: prod-error-rate\n"
            "[WARNING]  06:01:18 UTC | host:prod-cache-01 | Redis evictions > 1000/min"
            " | value: 4721/min | monitor: prod-redis-evict\n"
            "[WARNING]  06:01:18 UTC | host:prod-cache-02 | Redis evictions > 1000/min"
            " | value: 3894/min | monitor: prod-redis-evict\n"
            "[CRITICAL] 06:01:20 UTC | check:prod-healthcheck | 8/12 endpoints failing"
            " | monitor: prod-synthetic\n\n"
            "There are about 25 more alerts but these are the main ones. This all"
            " started around 06:00 UTC. I think the root cause is the database"
            " disk filling up because the replication lag and connection pool"
            " issues started first, then everything cascaded.",
            "Massive Datadog alert flood starting 06:00 UTC: 4 web servers at"
            " 95%+ CPU, 3 services with 20-35% HTTP 5xx rates, primary DB at"
            " 94.6% disk with 127s replication lag, Redis cache eviction spike,"
            " 8/12 health check endpoints failing. User suspects root cause is"
            " DB disk filling up causing cascading failures across all services.",
        ),
        gold=ScenarioGold(
            category="Network & Connectivity",
            priority="P1",
            assigned_team="Network Operations",
            needs_escalation=True,
            missing_information=("timestamp", "business_impact"),
            next_best_action="Declare a P1 incident and address the probable root cause: the"
            " primary database disk at 94.6% is likely causing replication lag"
            " and connection pool exhaustion, which is cascading into 5xx errors"
            " across all dependent services \u2014 the alert flood is symptomatic noise"
            " and should not be triaged individually",
            remediation_steps=(
                "Immediately free disk space on prod-db-primary by purging old WAL segments, temp tables, or expanding "
                "the volume",
                "Once disk pressure is relieved, verify replication lag on replicas drops below threshold and "
                "connection pools recover",
                "Monitor the HTTP 5xx rates and CPU on web servers to confirm they normalize as the database "
                "stabilizes",
                "Conduct a post-incident review to add disk growth alerting at 80% and automate log rotation to "
                "prevent "
                "recurrence",
                "Tune Datadog alert grouping to deduplicate cascading alerts and surface only the root-cause monitor "
                "during similar incidents",
            ),
        ),
        tags=("data-cleanup", "monitoring-flood", "alert-noise"),
    ),
    # ------------------------------------------------------------------
    # dc-gen-062  Thread hijacking – email thread switches topics
    # ------------------------------------------------------------------
    ScenarioDefinition(
        scenario_id="dc-gen-062",
        subjects=(
            "RE: RE: RE: Printer paper jam on 4th floor – NOW: Cannot connect to VPN",
            "FW: Printer Issue → Actually VPN is down for my whole team",
        ),
        descriptions=(
            "Original thread started three weeks ago about a recurring paper jam"
            " on the HP LaserJet 4250 on the 4th floor (ticket INC0041233). That"
            " issue was resolved on 2024-04-11. However, instead of opening a new"
            " ticket, the user replied to the old printer thread with a completely"
            " unrelated issue:\n\n'Hi team, unrelated to the printer – since this"
            " morning around 08:15 I cannot establish a VPN connection using"
            " GlobalProtect. It gets to 'Connecting…' then times out after 45"
            " seconds. I'm working from our Austin office on the guest Wi-Fi."
            " My colleague next to me has the same problem. We both updated to"
            " GlobalProtect 6.1.3 last Friday. Could the update have broken"
            " something? We need VPN to reach the internal finance portal for"
            " month-end close today. Thanks, Dana.'",
            "Thread subject still says 'Printer paper jam 4th floor' but the"
            " latest reply is about a VPN connectivity failure. The user writes:"
            " 'Sorry for hijacking this thread – IT portal was down so I just"
            " replied here. Since 8 AM today GlobalProtect on my laptop"
            " (WIN-PC-7829) keeps spinning at 'Connecting' and drops after ~40s."
            " I'm at the Austin satellite office, wired ethernet. Tried"
            " forgetting and re-adding the VPN profile, flushed DNS, rebooted."
            " Nothing works. Same for two other people on this floor. We all"
            " upgraded GP to 6.1.3 on Friday. Finance month-end reports are"
            " due by EOD – this is blocking us.'",
        ),
        gold=ScenarioGold(
            category="Network & Connectivity",
            priority="P3",
            assigned_team="Network Operations",
            needs_escalation=False,
            missing_information=("application_version",),
            next_best_action="Disregard the stale printer thread context and triage the"
            " actual issue — multiple users at the Austin office cannot connect"
            " via GlobalProtect VPN after upgrading to version 6.1.3, which"
            " suggests a client-side or gateway compatibility regression",
            remediation_steps=(
                "Confirm the exact GlobalProtect client version on affected machines and compare with the"
                " gateway's supported version list",
                "Check the GlobalProtect gateway and portal logs for TLS handshake or certificate errors"
                " corresponding to the Austin office IP range",
                "Test connectivity from an Austin machine using the previous GlobalProtect version to isolate"
                " whether the 6.1.3 upgrade is the root cause",
                "If the upgrade is confirmed as the cause, roll back affected clients to the last known-good"
                " version and coordinate with Palo Alto support",
                "Open a new ticket for the VPN issue with correct categorization and link it to the original"
                " printer ticket for audit trail",
            ),
        ),
        tags=("data-cleanup", "thread-hijack"),
    ),
    # ------------------------------------------------------------------
    # dc-gen-063  Mixed RTL/LTR text – Hebrew/Arabic mixed with English
    # ------------------------------------------------------------------
    ScenarioDefinition(
        scenario_id="dc-gen-063",
        subjects=(
            "בעיה בהרשאות SharePoint – Permission denied on Contoso Finance site",
            "مشكلة في صلاحيات شير بوينت – Cannot access Contoso Finance library",
        ),
        descriptions=(
            "שלום צוות IT,\n\nאני לא מצליח לגשת לספריית המסמכים של Contoso"
            " Finance ב-SharePoint Online. כשאני לוחץ על הקישור אני מקבל הודעה:"
            " 'Access Denied – You do not have permission to access this resource."
            " Contact your administrator.' (Error code: 403 SPO-ERR-8821)\n\n"
            "I was added to the Finance Contributors group last week by my manager"
            " Rachel Levy. I can see the site in my SharePoint home page but"
            " clicking into the 'Q4 Reports' document library gives the 403."
            " Other team members (Yossi, Miriam) access it fine.\n\n"
            "אני עובד על Windows 11 עם Edge 122.0 ומחובר עם חשבון"
            " d.cohen@contoso.com. ניסיתי גם ב-Chrome וגם ב-InPrivate – אותה"
            " בעיה. זה דחוף כי אני צריך להעלות דוחות עד סוף השבוע.\nתודה, דניאל",
            "مرحبا فريق الدعم,\n\nI need help with SharePoint permissions. أنا"
            " عضو جديد في فريق Finance وتمت إضافتي إلى مجموعة 'Finance"
            " Contributors' الأسبوع الماضي. When I try to open the Q4 Reports"
            " library on https://contoso.sharepoint.com/sites/finance I get"
            " 'Access Denied' error 403 SPO-ERR-8821.\n\nMy account is"
            " a.hassan@contoso.com. حاولت عدة متصفحات – Edge, Chrome,"
            " Firefox – ونفس المشكلة. My manager confirmed I should have"
            " Contribute-level access. Other new hires who joined the same"
            " week can access the library without issues.\n\nهل يمكنكم التحقق"
            " من الصلاحيات؟ أحتاج الوصول بشكل عاجل لإغلاق التقارير الربعية."
            "\nشكراً, أحمد",
        ),
        gold=ScenarioGold(
            category="Software & Applications",
            priority="P3",
            assigned_team="Enterprise Applications",
            needs_escalation=False,
            missing_information=("error_message", "environment_details"),
            next_best_action="Investigate the SharePoint Online 403 error (SPO-ERR-8821)"
            " for the user's account in the Finance Contributors group — the user"
            " was recently added but the permission grant may not have propagated"
            " or may be overridden by a library-level permission break",
            remediation_steps=(
                "Verify the user's membership in the Finance Contributors group via SharePoint admin center"
                " and confirm the group has Contribute permissions on the Q4 Reports library",
                "Check whether the Q4 Reports library has broken permission inheritance from the site and"
                " whether the Finance Contributors group is explicitly granted access at the library level",
                "Review the SharePoint ULS/audit logs for the 403 SPO-ERR-8821 to identify whether a"
                " conditional access policy or DLP rule is blocking the user",
                "If permissions appear correct, force a profile recompilation by removing and re-adding the"
                " user to the group, then wait up to 24 hours for token refresh",
                "Confirm access is restored and document the root cause for the permissions discrepancy",
            ),
        ),
        tags=("data-cleanup", "rtl-ltr-mixed"),
    ),
    # ------------------------------------------------------------------
    # dc-gen-064  HTML table paste – massive HTML with issue in one cell
    # ------------------------------------------------------------------
    ScenarioDefinition(
        scenario_id="dc-gen-064",
        subjects=(
            "Data Migration Report – URGENT: SQL backup job failing on SQLPROD07",
            "Pasting migration tracker – backup failure row highlighted",
        ),
        descriptions=(
            "<html><body><table border='1' cellpadding='4'><tr><th>Server</th>"
            "<th>Migration Status</th><th>Last Backup</th><th>Notes</th></tr>"
            "<tr><td>SQLPROD01</td><td style='background:green;color:white'>"
            "Complete</td><td>2024-04-14 02:00</td><td>OK</td></tr>"
            "<tr><td>SQLPROD02</td><td style='background:green;color:white'>"
            "Complete</td><td>2024-04-14 02:15</td><td>OK</td></tr>"
            "<tr><td>SQLPROD03</td><td style='background:green;color:white'>"
            "Complete</td><td>2024-04-14 02:30</td><td>OK</td></tr>"
            "<tr><td>SQLPROD04</td><td style='background:green;color:white'>"
            "Complete</td><td>2024-04-14 03:00</td><td>OK</td></tr>"
            "<tr><td>SQLPROD05</td><td style='background:green;color:white'>"
            "Complete</td><td>2024-04-14 03:15</td><td>OK</td></tr>"
            "<tr><td>SQLPROD06</td><td style='background:green;color:white'>"
            "Complete</td><td>2024-04-14 03:30</td><td>OK</td></tr>"
            "<tr><td style='background:red;color:white'>SQLPROD07</td>"
            "<td style='background:red;color:white'>FAILED</td>"
            "<td>2024-04-14 04:00 – ABORTED</td>"
            "<td>Backup job SQLPROD07_FULL_DAILY failed with error: 'Insufficient"
            " disk space on E:\\SQLBackups – 12GB required, 1.3GB available."
            " Transaction log backup also failing since 2024-04-12. ~2TB database"
            " (ContosoFinanceDW). Data team needs this resolved before Monday"
            " morning ETL run or risk data loss.'</td></tr>"
            "<tr><td>SQLPROD08</td><td style='background:green;color:white'>"
            "Complete</td><td>2024-04-14 04:15</td><td>OK</td></tr>"
            "</table></body></html>",
            "Migration tracker (copied from Excel):\n\n"
            "| Server     | Status   | Last Backup       | Notes |\n"
            "|------------|----------|-------------------|-------|\n"
            "| SQLPROD01  | Complete | 2024-04-14 02:00  | OK    |\n"
            "| SQLPROD02  | Complete | 2024-04-14 02:15  | OK    |\n"
            "| SQLPROD03  | Complete | 2024-04-14 02:30  | OK    |\n"
            "| SQLPROD04  | Complete | 2024-04-14 03:00  | OK    |\n"
            "| SQLPROD05  | Complete | 2024-04-14 03:15  | OK    |\n"
            "| SQLPROD06  | Complete | 2024-04-14 03:30  | OK    |\n"
            "| SQLPROD07  | **FAILED** | 2024-04-14 04:00 ABORTED | Backup job"
            " SQLPROD07_FULL_DAILY failed – insufficient disk space on"
            " E:\\SQLBackups (12GB needed, 1.3GB free). Transaction log backup"
            " also failing since April 12. Database is ContosoFinanceDW (~2TB)."
            " Must be fixed before Monday AM ETL run – potential data loss. |\n"
            "| SQLPROD08  | Complete | 2024-04-14 04:15  | OK    |\n\n"
            "Please help with the SQLPROD07 row – everything else is fine.",
        ),
        gold=ScenarioGold(
            category="Data & Storage",
            priority="P2",
            assigned_team="Data Platform",
            needs_escalation=False,
            missing_information=("affected_system", "error_message"),
            next_best_action="Address the disk-space-exhaustion failure on SQLPROD07 — the"
            " E:\\SQLBackups volume has only 1.3 GB free of the 12 GB required"
            " for the daily full backup of ContosoFinanceDW, and transaction log"
            " backups have also been failing since April 12, creating a growing"
            " data-loss risk ahead of Monday's ETL run",
            remediation_steps=(
                "Immediately free space on E:\\SQLBackups by moving or purging older backup files and verify"
                " available space exceeds 12 GB",
                "Run a manual transaction log backup to break the log chain failure that has been accumulating"
                " since April 12",
                "Execute a full backup of ContosoFinanceDW and confirm it completes successfully",
                "Set up disk-space monitoring alerts on the E:\\SQLBackups volume at 80% and 90% thresholds"
                " to prevent recurrence",
                "Review the backup retention policy for SQLPROD07 and consider moving backups to a larger"
                " volume or network share",
            ),
        ),
        tags=("data-cleanup", "html-table-paste"),
    ),
    # ------------------------------------------------------------------
    # dc-gen-065  Extreme OCR artifacts – scanned/faxed document
    # ------------------------------------------------------------------
    ScenarioDefinition(
        scenario_id="dc-gen-065",
        subjects=(
            "Fax from warehouse: Sc@nner/print3r issu3 – urg3nt",
            "FW: Scanned request from Building C – printer malfunction",
        ),
        descriptions=(
            "--- Beg1n Faxed Docum3nt ---\n\n"
            "D@te: Apr1l 15, 2O24\nFr0m: J. Mart1nez, Wareh0use Bldg C\n"
            "T0: lT Supp0rt\n\nSubj3ct: Pr1nter N0t Work1ng\n\n"
            "0ur ma1n pr1nter (l th1nk 1t's an HP Laserl3t 4O9Odn) 0n the"
            " sh1pp1ng fl00r has st0pped pr1nt1ng ent1rely. Th3 d1splay sh0ws"
            " 'PC L0AD LETTER' wh1ch w3 d0n't und3rstand. W3 tr1ed turn1ng"
            " 1t 0ff and 0n, r3plac1ng t0ner, and check1ng pap3r trays."
            " N0th1ng w0rks. Th1s pr1nter hand1es all 0ur sh1pp1ng lab3ls"
            " and w3 hav3 0rders back1ng up. N33d s0me0ne t0 l00k at 1t"
            " t0day 1f p0ss1ble.\n\nTh@nks,\nJ. Mart1nez\nExt 4421\n\n"
            "--- 3nd Faxed D0cum3nt ---",
            "This ticket was auto-created from a scanned fax received at"
            " 09:42 AM. OCR confidence: LOW.\n\n"
            "Transcribed text:\n'Oate: Apri| 15, 2024. From: J. Martinez,"
            " Warehouse B|dg C. To: lT Support. Subject: Printer Not Working."
            " Our main printer (HP Laser]et 4090dn maybe?) on the shipping"
            " f|oor stopped printing comp|etely. Disp|ay shows PC LOAD LETTER"
            " error. We tried: power cyc|e, rep|aced toner cartridge, checked"
            " a|| paper trays, c|eared paper path. Nothing he|ps. This is the"
            " on|y printer for shipping |abe|s and we have 50+ orders waiting."
            " P|ease send someone today. Thanks, J. Martinez, Ext 4421.'\n\n"
            "Note: Original fax image attached as TIFF. OCR quality degraded"
            " due to low scan resolution (150 DPI) and fax transmission noise.",
        ),
        gold=ScenarioGold(
            category="Hardware & Peripherals",
            priority="P3",
            assigned_team="Endpoint Engineering",
            needs_escalation=False,
            missing_information=("device_info", "error_message"),
            next_best_action="Dispatch a technician to Building C shipping floor to"
            " diagnose the HP LaserJet 4090dn displaying 'PC LOAD LETTER' —"
            " despite the heavy OCR corruption the core issue is a printer"
            " that is non-functional and blocking shipping label output",
            remediation_steps=(
                "Verify the exact printer model and asset tag on-site in Building C shipping floor",
                "Clear the 'PC LOAD LETTER' error by checking that the correct paper size (Letter/A4) is"
                " loaded in the tray matching the print job's requested media",
                "Inspect the paper path, pickup rollers, and fuser for jams or wear that could trigger the error",
                "Print a configuration page from the printer's control panel to confirm basic functionality",
                "If the error persists after tray and paper-path checks, update the printer firmware and"
                " reset to factory defaults as a last resort",
            ),
        ),
        tags=("data-cleanup", "ocr-artifacts"),
    ),
    # ------------------------------------------------------------------
    # dc-gen-066  Terse one-word ticket
    # ------------------------------------------------------------------
    ScenarioDefinition(
        scenario_id="dc-gen-066",
        subjects=(
            "help",
            "broken",
        ),
        descriptions=(
            "broken",
            "not working",
        ),
        gold=ScenarioGold(
            category="General Inquiry",
            priority="P4",
            assigned_team="None",
            needs_escalation=False,
            missing_information=(
                "affected_system",
                "error_message",
                "steps_to_reproduce",
                "device_info",
                "contact_info",
                "environment_details",
            ),
            next_best_action="Reply to the submitter requesting basic triage information —"
            " the ticket contains no actionable detail and cannot be categorized"
            " or assigned without knowing what system, device, or application"
            " is affected",
            remediation_steps=(
                "Respond to the user asking them to identify the affected system or application",
                "Request a description of the problem including any error messages or screenshots",
                "Ask for the user's device type, operating system, and location or office",
                "Once sufficient information is provided, recategorize and assign the ticket appropriately",
                "If no response is received within 48 hours, follow up once more before closing as"
                " insufficient information",
            ),
        ),
        tags=("data-cleanup", "terse-ticket"),
    ),
    # ------------------------------------------------------------------
    # dc-gen-067  Terminal output dump – DNS issue buried in tracert
    # ------------------------------------------------------------------
    ScenarioDefinition(
        scenario_id="dc-gen-067",
        subjects=(
            "Network issue – pasting tracert and nslookup output",
            "VPN/DNS problem – see terminal output below",
        ),
        descriptions=(
            "PS C:\\Users\\tchen> tracert intranet.contoso.com\n\n"
            "Tracing route to intranet.contoso.com [10.128.4.20]\n"
            "over a maximum of 30 hops:\n\n"
            "  1     1 ms     1 ms     1 ms  gateway.local [192.168.1.1]\n"
            "  2     8 ms     7 ms     9 ms  10.0.0.1\n"
            "  3    12 ms    11 ms    13 ms  core-rtr-01.contoso.com [10.64.0.1]\n"
            "  4     *        *        *     Request timed out.\n"
            "  5     *        *        *     Request timed out.\n"
            "  6     *        *        *     Request timed out.\n"
            "  7     *        *        *     Request timed out.\n"
            "  8     *        *        *     Request timed out.\n"
            "  9     *        *        *     Request timed out.\n"
            " 10     *        *        *     Request timed out.\n\n"
            "Trace complete.\n\n"
            "PS C:\\Users\\tchen> nslookup intranet.contoso.com\n"
            "Server:  dns-ext-01.contoso.com\n"
            "Address:  168.63.129.16\n\n"
            "*** dns-ext-01.contoso.com can't find intranet.contoso.com:"
            " Non-existent domain\n\n"
            "PS C:\\Users\\tchen> nslookup intranet.contoso.com 10.64.1.53\n"
            "Server:  dns-int-01.contoso.com\n"
            "Address:  10.64.1.53\n\n"
            "Name:    intranet.contoso.com\n"
            "Address:  10.128.4.20\n\n"
            "PS C:\\Users\\tchen> ipconfig /all | findstr DNS\n"
            "   DNS Servers . . . . . . . . . . . : 168.63.129.16\n\n"
            "So it looks like my laptop is pointed at the external DNS"
            " (168.63.129.16) instead of the internal one (10.64.1.53)."
            " I think the VPN is connecting but not pushing DNS settings."
            " GlobalProtect 6.1.3 on Windows 11. Started after Friday's update.",
            "Dumping my PowerShell session:\n\n"
            "PS C:\\> Test-NetConnection intranet.contoso.com -Port 443\n"
            "WARNING: Name resolution of intranet.contoso.com failed\n"
            "ComputerName     : intranet.contoso.com\n"
            "RemoteAddress    :\nRemotePort       : 443\n"
            "InterfaceAlias   :\nSourceAddress    :\n"
            "TcpTestSucceeded : False\n\n"
            "PS C:\\> Resolve-DnsName intranet.contoso.com\n"
            "Resolve-DnsName : intranet.contoso.com : DNS name does not exist\n\n"
            "PS C:\\> Resolve-DnsName intranet.contoso.com -Server 10.64.1.53\n"
            "Name           Type TTL Section IPAddress\n"
            "----           ---- --- ------- ---------\n"
            "intranet.conto A    300 Answer  10.128.4.20\n\n"
            "PS C:\\> Get-DnsClientServerAddress -InterfaceAlias 'Wi-Fi'\n"
            "InterfaceAlias  AddressFamily ServerAddresses\n"
            "--------------  ------------- ---------------\n"
            "Wi-Fi           IPv4          {168.63.129.16}\n"
            "Wi-Fi           IPv6          {}\n\n"
            "Clearly the VPN tunnel is up but DNS is not being overridden to"
            " use internal servers. Started happening after GlobalProtect"
            " 6.1.3 update last Friday. All internal sites fail to resolve.",
        ),
        gold=ScenarioGold(
            category="Network & Connectivity",
            priority="P2",
            assigned_team="Network Operations",
            needs_escalation=False,
            missing_information=("network_location",),
            next_best_action="Investigate the GlobalProtect VPN split-DNS configuration —"
            " the VPN tunnel connects successfully but is not pushing internal DNS"
            " server settings (10.64.1.53) to the client, leaving external DNS"
            " (168.63.129.16) as the sole resolver and causing all internal name"
            " resolution to fail",
            remediation_steps=(
                "Check the GlobalProtect gateway agent configuration to verify that DNS settings"
                " (10.64.1.53) are included in the split-tunnel or full-tunnel DNS push",
                "Review recent changes to the GlobalProtect 6.1.3 gateway configuration that may have"
                " altered DNS proxy or split-DNS behavior after Friday's update",
                "As an immediate workaround, have the user manually set DNS to 10.64.1.53 on the VPN"
                " adapter to restore internal name resolution",
                "Test the fix with nslookup and tracert against intranet.contoso.com to confirm"
                " resolution via internal DNS",
                "If the 6.1.3 client update is confirmed as the cause, coordinate a rollback or"
                " configuration patch across affected users",
            ),
        ),
        tags=("data-cleanup", "terminal-dump"),
    ),
    # ------------------------------------------------------------------
    # dc-gen-068  Auto-generated monitoring alert – Datadog JSON
    # ------------------------------------------------------------------
    ScenarioDefinition(
        scenario_id="dc-gen-068",
        subjects=(
            "[ALERT] Datadog Monitor #488291 TRIGGERED: CRM API p99 latency > 5s",
            "[Datadog] ALERT – CRM-API-PROD latency threshold exceeded",
        ),
        descriptions=(
            '{"alert_id":"evt-488291-a7c3","monitor_name":"CRM API p99 latency'
            ' > 5000ms","monitor_type":"metric alert","status":"ALERT",'
            '"priority":"P2","trigger_ts":"2024-04-15T14:32:07Z","resolve_ts"'
            ':null,"tags":["service:crm-api","env:prod","team:enterprise-apps"'
            ',"region:eastus2"],"query":"avg(last_5m):p99:trace.http.request'
            '{service:crm-api,env:prod} > 5000","value":8742.3,"threshold":5000'
            ',"notify":["@slack-crm-oncall","@pagerduty-crm"],"message":'
            '"p99 latency for crm-api in prod/eastus2 is 8742ms (threshold'
            " 5000ms). Started spiking at 14:27 UTC. Correlated metrics show"
            " DB connection pool saturation on crm-db-replica-02 (active"
            " connections: 498/500). Application logs show increased"
            " timeout errors from ORM layer. Last deploy: crm-api v2.14.3"
            ' at 13:55 UTC.","org":"contoso-financial"}',
            "[Datadog Auto-Alert]\n"
            "Monitor: CRM API p99 latency > 5000ms (#488291)\n"
            "Status: ALERT (was OK)\n"
            "Triggered: 2024-04-15 14:32:07 UTC\n"
            "Region: eastus2\n"
            "Current value: 8,742 ms (threshold: 5,000 ms)\n\n"
            "Context:\n"
            "- Service: crm-api (prod)\n"
            "- Last deployment: crm-api v2.14.3 deployed at 13:55 UTC\n"
            "- DB connection pool on crm-db-replica-02: 498/500 active\n"
            "- ORM timeout errors increasing since 14:27 UTC\n"
            "- No infrastructure changes in the last 24h\n\n"
            "Notified: #crm-oncall (Slack), CRM PagerDuty rotation\n\n"
            "This is an auto-generated alert from Datadog. Do not reply"
            " to this message. Runbook: https://wiki.contoso.com/runbooks/crm-latency",
        ),
        gold=ScenarioGold(
            category="Software & Applications",
            priority="P2",
            assigned_team="Enterprise Applications",
            needs_escalation=False,
            missing_information=("affected_users", "business_impact"),
            next_best_action="Investigate the CRM API latency spike — p99 jumped to 8.7s"
            " (threshold 5s) starting at 14:27 UTC, likely caused by DB connection"
            " pool saturation on crm-db-replica-02 (498/500) following the v2.14.3"
            " deployment at 13:55 UTC",
            remediation_steps=(
                "Check whether the crm-api v2.14.3 deployment introduced a query regression or connection"
                " leak by comparing DB pool metrics before and after 13:55 UTC",
                "If connection pool saturation is confirmed, increase the pool limit temporarily on"
                " crm-db-replica-02 and restart affected crm-api pods",
                "Review the ORM timeout errors in application logs to identify the specific queries or"
                " endpoints causing the pool exhaustion",
                "If the deployment is the root cause, initiate a rollback to crm-api v2.14.2 and verify"
                " latency returns to normal",
                "Update the Datadog monitor to include connection pool utilization as a correlated metric"
                " and add it to the CRM runbook",
            ),
        ),
        tags=("data-cleanup", "monitoring-alert"),
    ),
    # ------------------------------------------------------------------
    # dc-gen-069  Double-encoded UTF-8 (mojibake)
    # ------------------------------------------------------------------
    ScenarioDefinition(
        scenario_id="dc-gen-069",
        subjects=(
            "Probl\u00c3\u00a8me avec l\u2019application \u2013 erreur d\u2019authentification",
            "Application login failure \u2013 mojibake in error message",
        ),
        descriptions=(
            "Bonjour \u00c3\u00a9quipe IT,\n\n"
            "Je n\u2019arrive plus \u00c3\u00a0 me connecter \u00c3\u00a0"
            " l\u2019application Contoso ExpenseTracker depuis ce matin. Quand"
            " j\u2019entre mes identifiants, je re\u00c3\u00a7ois le message"
            " d\u2019erreur suivant :\n\n"
            "\u2018Authentification \u00c3\u00a9chou\u00c3\u00a9e \u2013 votre"
            " jeton de session a expir\u00c3\u00a9. Veuillez contacter votre"
            " administrateur.\u2019\n\n"
            "J\u2019ai essay\u00c3\u00a9 de vider le cache du navigateur,"
            " d\u2019utiliser un autre navigateur (Chrome, Firefox, Edge) et de"
            " r\u00c3\u00a9initialiser mon mot de passe via le portail"
            " self-service. Rien ne fonctionne. Mes coll\u00c3\u00a8gues dans"
            " le m\u00c3\u00aame bureau n\u2019ont pas ce probl\u00c3\u00a8me.\n\n"
            "Mon poste : WIN-PC-5523, Windows 11, connect\u00c3\u00a9 au"
            " r\u00c3\u00a9seau filaire du bureau de Montr\u00c3\u00a9al.\n\n"
            "Merci,\n\u00c3\u2030milie Dupr\u00c3\u00a9",
            "Hi team,\n\n"
            "Something is wrong with the encoding in Contoso ExpenseTracker"
            " \u2013 but also I can\u2019t log in at all. The error says"
            " \u2018Authentication failed \u2013 session token expired\u2019."
            " I have tried:\n"
            "- Clearing browser cache and cookies\n"
            "- Trying Chrome, Edge, and Firefox\n"
            "- Resetting my password via the self-service portal\n"
            "- Using InPrivate/Incognito mode\n\n"
            "Nothing works. I suspect there\u2019s a backend issue because the"
            " error page itself is rendering with garbled characters (\u00c3\u00a9"
            " instead of \u00e9, \u00c3\u00a8 instead of \u00e8, etc.), which"
            " suggests a double-encoding problem on the server side.\n\n"
            "Account: e.dupre@contoso.com\n"
            "Device: WIN-PC-5523, Windows 11 23H2\n"
            "Location: Montr\u00c3\u00a9al office, wired LAN\n\n"
            "This is blocking my expense reports for month-end.\nThanks, Emilie",
        ),
        gold=ScenarioGold(
            category="Software & Applications",
            priority="P3",
            assigned_team="Enterprise Applications",
            needs_escalation=False,
            missing_information=("application_version", "steps_to_reproduce"),
            next_best_action="Investigate the Contoso ExpenseTracker authentication failure"
            " — the user cannot log in due to an expired session token error,"
            " and the garbled character rendering (mojibake) suggests the"
            " application may have a double-UTF-8-encoding issue on the"
            " server side that could be related to the auth failure",
            remediation_steps=(
                "Check the ExpenseTracker application logs for authentication errors related to"
                " e.dupre@contoso.com and verify whether the session token service is functioning",
                "Investigate whether a recent deployment introduced a character encoding change that"
                " is double-encoding UTF-8 responses, causing both display corruption and potential"
                " token parsing failures",
                "Verify the user's account status in Azure AD and confirm the account is not locked,"
                " expired, or affected by a conditional access policy",
                "As a workaround, have the administrator manually invalidate and reissue the user's"
                " session tokens in the ExpenseTracker admin panel",
                "If double-encoding is confirmed, coordinate with the development team to fix the"
                " Content-Type and encoding headers on the authentication endpoint",
            ),
        ),
        tags=("data-cleanup", "mojibake"),
    ),
    # ------------------------------------------------------------------
    # dc-gen-070  Massive disclaimer chain – real MFA issue buried
    # ------------------------------------------------------------------
    ScenarioDefinition(
        scenario_id="dc-gen-070",
        subjects=(
            "RE: FW: RE: FW: MFA not working on new phone",
            "FW: Multi-factor authentication issue (see below disclaimers)",
        ),
        descriptions=(
            "CONFIDENTIALITY NOTICE: This email and any attachments are for the"
            " exclusive and confidential use of the intended recipient. If you"
            " are not the intended recipient, please do not read, distribute,"
            " or take action based on this message. If you have received this"
            " in error, please notify the sender immediately and delete this"
            " message. Contoso Financial Services, 1200 Market St, Suite 400,"
            " Philadelphia, PA 19107.\n\n"
            "AVIS DE CONFIDENTIALITÉ : Ce courriel et ses pièces jointes sont"
            " destinés exclusivement à l'usage confidentiel du destinataire"
            " prévu. Si vous n'êtes pas le destinataire prévu, veuillez ne pas"
            " lire, distribuer ou agir sur la base de ce message.\n\n"
            "VERTRAULICHKEITSHINWEIS: Diese E-Mail und alle Anhänge sind"
            " ausschließlich für den vertraulichen Gebrauch des vorgesehenen"
            " Empfängers bestimmt.\n\n"
            "機密通知：本邮件及其附件仅供指定收件人机密使用。\n\n"
            "AVISO DE CONFIDENCIALIDAD: Este correo electrónico y sus archivos"
            " adjuntos son para uso exclusivo y confidencial del destinatario"
            " previsto.\n\n"
            "--- Actual message (forwarded 4 times) ---\n\n"
            "Hi IT,\n\n"
            "I got a new iPhone 15 and I need to transfer my MFA. I unenrolled"
            " my old phone from the Microsoft Authenticator app but now I can't"
            " add my Contoso account on the new phone. When I scan the QR code"
            " it says 'Account already registered – contact your administrator.'"
            " I'm locked out of everything – Outlook, Teams, SharePoint, VPN."
            " I have a client presentation at 2 PM today and I can't access my"
            " slides. Please help ASAP.\n\n"
            "– Karen Liu, Senior Analyst, Contoso Wealth Management\n"
            "  k.liu@contoso.com | Ext 3387\n\n"
            "CONFIDENTIALITY NOTICE: This email and any attachments are for the"
            " exclusive and confidential use of the intended recipient...\n"
            "[Disclaimer repeated 3 more times in English, French, German,"
            " Chinese, and Spanish]",
            "---------- Forwarded message ----------\n"
            "From: Karen Liu <k.liu@contoso.com>\n"
            "To: IT Helpdesk <ithelpdesk@contoso.com>\n"
            "Date: Mon, Apr 15, 2024 at 10:22 AM\n\n"
            "[DISCLAIMER – Contoso Financial Services – Confidential – English]\n"
            "[DISCLAIMER – Contoso Financial Services – Confidentiel – Français]\n"
            "[DISCLAIMER – Contoso Financial Services – Vertraulich – Deutsch]\n"
            "[DISCLAIMER – Contoso Financial Services – 机密 – 中文]\n"
            "[DISCLAIMER – Contoso Financial Services – Confidencial – Español]\n\n"
            "Hi, I switched to a new iPhone 15 and my Microsoft Authenticator"
            " MFA is broken. Old phone was wiped. New phone gives error"
            " 'Account already registered' when I try to set up MFA for"
            " k.liu@contoso.com. I'm completely locked out of all Contoso"
            " services – email, Teams, SharePoint, VPN. I have an urgent"
            " client meeting at 2 PM and need access to my presentation"
            " deck on SharePoint. Can someone reset my MFA registration?\n\n"
            "Karen Liu | Senior Analyst | Ext 3387\n\n"
            "[DISCLAIMER – Contoso Financial Services – repeated in 5 languages]\n"
            "[DISCLAIMER – Contoso Financial Services – repeated in 5 languages]\n"
            "[DISCLAIMER – Contoso Financial Services – repeated in 5 languages]",
        ),
        gold=ScenarioGold(
            category="Access & Authentication",
            priority="P2",
            assigned_team="Identity & Access Management",
            needs_escalation=False,
            missing_information=("device_info", "authentication_method"),
            next_best_action="Reset the MFA registration for k.liu@contoso.com in Azure AD"
            " — the user switched to a new iPhone 15, wiped the old device, and"
            " the Authenticator app on the new phone cannot re-register because"
            " the old enrollment is still active, leaving the user locked out"
            " of all Contoso services with a client meeting at 2 PM",
            remediation_steps=(
                "Verify the user's identity through an out-of-band method (e.g., manager confirmation"
                " or in-person ID verification) before resetting MFA",
                "Delete the existing MFA registration for k.liu@contoso.com in the Azure AD admin portal"
                " under Authentication Methods",
                "Guide the user through re-enrolling Microsoft Authenticator on the new iPhone 15 by"
                " scanning the fresh QR code from aka.ms/mysecurityinfo",
                "Confirm the user can successfully authenticate to Outlook, Teams, and SharePoint"
                " with the new MFA enrollment",
                "Recommend the user register a backup MFA method (e.g., phone number or FIDO2 key)"
                " to avoid total lockout during future device changes",
            ),
        ),
        tags=("data-cleanup", "disclaimer-chain"),
    ),
    # ------------------------------------------------------------------
    # dc-gen-071  Interleaved conversations – two threads merged
    # ------------------------------------------------------------------
    ScenarioDefinition(
        scenario_id="dc-gen-071",
        subjects=(
            "RE: Laptop docking station + headset issue (two problems)",
            "Merged thread: dock display + wireless headset",
        ),
        descriptions=(
            "--- Message from Alex Park (10:05 AM) ---\n"
            "My Dell WD19S docking station stopped outputting to my external"
            " monitor (Dell U2723QE) this morning. Laptop screen works fine"
            " but the dock's DisplayPort shows no signal.\n\n"
            "--- Message from Priya Sharma (10:07 AM) ---\n"
            "My Jabra Evolve2 75 headset won't connect to my laptop via"
            " Bluetooth anymore. It pairs but audio routes to laptop speakers.\n\n"
            "--- Message from Alex Park (10:12 AM) ---\n"
            "Update: I tried a different DP cable and different monitor port."
            " Still no signal. The dock's power LED is solid white. USB"
            " peripherals through the dock work fine (keyboard, mouse).\n\n"
            "--- Message from Priya Sharma (10:15 AM) ---\n"
            "I forgot to mention – this started after the Windows 11 23H2"
            " update last night. Bluetooth driver shows as up to date in"
            " Device Manager. Headset firmware is current.\n\n"
            "--- Message from Alex Park (10:20 AM) ---\n"
            "Also noticed dock firmware is v01.00.02 – pretty old. Could"
            " that be the issue? My laptop is a Latitude 5540 with Windows"
            " 11 23H2, updated last night. Asset tag: IT-DOCK-0891.\n\n"
            "--- Message from Priya Sharma (10:23 AM) ---\n"
            "Jabra Direct says headset firmware v2.6.0 is current. My laptop"
            " is a Latitude 7440, asset LTOP-2204. Bluetooth adapter is Intel"
            " AX211. I need the headset for client calls starting at 11 AM.",
            "This ticket appears to contain two interleaved conversations from"
            " a shared Teams channel that were merged into one ticket:\n\n"
            "THREAD A (Alex Park – Docking Station):\n"
            "Dell WD19S dock not outputting display to Dell U2723QE monitor."
            " Power LED solid white, USB passthrough works, DP output does"
            " not. Tried different cable and port. Dock firmware v01.00.02."
            " Laptop: Latitude 5540, Win 11 23H2 (updated last night)."
            " Asset: IT-DOCK-0891.\n\n"
            "THREAD B (Priya Sharma – Headset):\n"
            "Jabra Evolve2 75 pairs via Bluetooth but audio does not route"
            " to headset — stays on laptop speakers. Started after Win 11"
            " 23H2 update. Bluetooth driver and headset firmware (v2.6.0)"
            " up to date. Laptop: Latitude 7440, asset LTOP-2204. Intel"
            " AX211 Bluetooth. Needs headset for 11 AM client calls.\n\n"
            "Both issues started after the Win 11 23H2 update pushed last"
            " night — may be related to driver changes in the update.",
        ),
        gold=ScenarioGold(
            category="Hardware & Peripherals",
            priority="P3",
            assigned_team="Endpoint Engineering",
            needs_escalation=False,
            missing_information=("device_info",),
            next_best_action="Split this ticket into two separate issues — (1) Alex Park's"
            " Dell WD19S dock display output failure and (2) Priya Sharma's"
            " Jabra Evolve2 75 Bluetooth audio routing problem — both appear"
            " to have been triggered by the Windows 11 23H2 update and should"
            " be investigated for driver regressions introduced by that update",
            remediation_steps=(
                "Create two separate tickets: one for the dock display issue (Alex Park, IT-DOCK-0891)"
                " and one for the Bluetooth headset issue (Priya Sharma, LTOP-2204)",
                "For the dock issue: update the Dell WD19S firmware from v01.00.02 to the latest via"
                " Dell Command Update and test DisplayPort output",
                "For the headset issue: check the Windows 11 23H2 update for known Bluetooth audio"
                " routing regressions with Intel AX211 and roll back the Bluetooth driver if needed",
                "For both: review the Windows Update KB article for 23H2 to identify known hardware"
                " compatibility issues with Dell docks and Intel Bluetooth adapters",
                "Verify both issues are resolved after remediation and link the tickets to track the"
                " common root cause (23H2 update)",
            ),
        ),
        tags=("data-cleanup", "interleaved-threads"),
    ),
]
