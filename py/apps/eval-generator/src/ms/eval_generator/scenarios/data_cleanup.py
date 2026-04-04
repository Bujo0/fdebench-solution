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
            "  <meta charset=\"UTF-8\">\n"
            '  <title>500 Internal Server Error</title>\n'
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
            '    <label>Report Title</label>\n'
            '    <input type="text" name="Title"'
            ' value="Q1 2026 Client Entertainment - NYC Trading Desk" />\n'
            "  </div>\n"
            '  <div class="form-group">\n'
            '    <label>Total Amount</label>\n'
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
            " wh\u200ben I\u200b tr\u200by to\u200b op\u200ben it\u200b
