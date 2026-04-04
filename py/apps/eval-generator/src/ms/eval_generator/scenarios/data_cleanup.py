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
]
