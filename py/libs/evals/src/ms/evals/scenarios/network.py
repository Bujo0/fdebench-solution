"""Network & Connectivity ticket scenarios for the Contoso Financial Services eval suite."""

from ms.evals.constants import Category
from ms.evals.constants import Channel
from ms.evals.constants import MissingInfo
from ms.evals.constants import Priority
from ms.evals.constants import Team
from ms.evals.scenarios.base import ScenarioDefinition


def get_scenarios() -> list[ScenarioDefinition]:
    """Return all Network & Connectivity evaluation scenarios."""
    return [
        # -------------------------------------------------------------------
        # 1. VPN disconnects when switching from Ethernet to WiFi
        # -------------------------------------------------------------------
        ScenarioDefinition(
            scenario_id="NET-001",
            subject="VPN keeps dropping when I undock my laptop",
            description=(
                "Every time I undock my laptop and switch from the wired connection to WiFi in the NYC office, "
                "the GlobalProtect VPN session drops and I have to manually reconnect. This happens 4-5 times a "
                "day and it's really disrupting my workflow because I lose my SSH sessions to the dev cluster. "
                "Running Windows 11 on a ThinkPad X1 Carbon Gen 11."
            ),
            category=Category.NETWORK,
            priority=Priority.P3,
            team=Team.NETWORK_OPS,
            needs_escalation=False,
            missing_info=[
                MissingInfo.NETWORK_LOCATION,
                MissingInfo.ERROR_MESSAGE,
            ],
            next_best_action=(
                "Check GlobalProtect client logs for disconnect reason and verify split-tunnel configuration "
                "allows seamless network transitions."
            ),
            remediation_steps=[
                "Collect GlobalProtect client logs from the user's laptop during a disconnect event.",
                "Verify the VPN client version is current and supports seamless roaming.",
                "Check split-tunnel policy to ensure it handles adapter changes gracefully.",
                "If needed, enable the 'allow network change' setting in the GlobalProtect agent configuration.",
                "Test by having the user undock and confirm the VPN session persists.",
            ],
            reporter_name="Derek Huang",
            reporter_email="derek.huang@contoso.com",
            reporter_department="Backend Engineering",
            channel=Channel.CHAT,
            tags=["vpn", "wifi", "undock", "globalprotect"],
            difficulty="easy",
        ),
        # -------------------------------------------------------------------
        # 2. VPN split tunnel not routing internal traffic
        # -------------------------------------------------------------------
        ScenarioDefinition(
            scenario_id="NET-002",
            subject="Can't reach internal wikis over VPN from home",
            description=(
                "Hi team,\n\n"
                "Since the VPN update last Friday I can connect to the VPN fine, but I can't reach "
                "wiki.internal.contoso.com or jira.internal.contoso.com from home. "
                "Internet browsing works. Other colleagues in Wealth Management are reporting the same thing. "
                "It was working before the weekend.\n\n"
                "Thanks,\nPreeti"
            ),
            category=Category.NETWORK,
            priority=Priority.P2,
            team=Team.NETWORK_OPS,
            needs_escalation=True,
            missing_info=[
                MissingInfo.AFFECTED_USERS,
                MissingInfo.ENVIRONMENT_DETAILS,
            ],
            next_best_action=(
                "Investigate the VPN split-tunnel routing table pushed in the last update to confirm internal "
                "subnets are included."
            ),
            remediation_steps=[
                "Compare the current split-tunnel policy with the previous version deployed before Friday.",
                "Verify that the internal subnets for wiki and Jira services are listed in the split-tunnel routes.",
                "Push a corrected routing policy to the VPN gateway.",
                "Ask affected users to disconnect and reconnect to pick up the new routes.",
                "Confirm resolution with the reporter and other affected Wealth Management staff.",
            ],
            reporter_name="Preeti Sharma",
            reporter_email="preeti.sharma@contoso.com",
            reporter_department="Wealth Management",
            channel=Channel.EMAIL,
            tags=["vpn", "split-tunnel", "routing", "multiple-users"],
            difficulty="medium",
        ),
        # -------------------------------------------------------------------
        # 3. VPN broken after Windows update
        # -------------------------------------------------------------------
        ScenarioDefinition(
            scenario_id="NET-003",
            subject="VPN completely broken after last night's Windows Update - URGENT",
            description=(
                "My laptop auto-installed a Windows update overnight (KB5034441) and now the GlobalProtect VPN "
                "won't connect at all. I get 'Gateway unreachable' every time I try. I'm working remotely today "
                "and have a critical client presentation at 2pm that requires access to the deal room on "
                "SharePoint. I've already tried rebooting twice. Please help ASAP."
            ),
            category=Category.NETWORK,
            priority=Priority.P2,
            team=Team.NETWORK_OPS,
            needs_escalation=False,
            missing_info=[
                MissingInfo.DEVICE_INFO,
                MissingInfo.SCREENSHOT_OR_ATTACHMENT,
            ],
            next_best_action=(
                "Verify whether KB5034441 has a known conflict with the current GlobalProtect client version "
                "and provide a workaround or rollback guidance."
            ),
            remediation_steps=[
                "Check the known issues list for KB5034441 against the deployed GlobalProtect client version.",
                "If a conflict exists, guide the user to uninstall the update via Settings > Windows Update.",
                "Alternatively, update the GlobalProtect client to the latest compatible version.",
                "Test VPN connectivity after the fix.",
                "If the user needs immediate access, provide a web-based VPN portal URL as a temporary workaround.",
            ],
            reporter_name="Marcus Cole",
            reporter_email="marcus.cole@contoso.com",
            reporter_department="Institutional Trading",
            channel=Channel.PHONE,
            tags=["vpn", "windows-update", "urgent", "remote"],
            difficulty="medium",
        ),
        # -------------------------------------------------------------------
        # 4. VPN certificate expired - can't connect
        # -------------------------------------------------------------------
        ScenarioDefinition(
            scenario_id="NET-004",
            subject="VPN connection error: certificate expired",
            description=(
                "Getting this error when I try to connect to VPN this morning:\n\n"
                '"SSL certificate verification failed: certificate has expired"\n\n'
                "I haven't changed anything on my end. Laptop is a Dell Latitude 5540 running Win 11. "
                "I'm in the Singapore office but trying to VPN to the NYC data center for the migration project."
            ),
            category=Category.NETWORK,
            priority=Priority.P2,
            team=Team.NETWORK_OPS,
            needs_escalation=False,
            missing_info=[
                MissingInfo.AUTHENTICATION_METHOD,
            ],
            next_best_action=(
                "Check whether the VPN gateway's SSL certificate has expired and renew it, or verify "
                "if the user's machine trust store needs updating."
            ),
            remediation_steps=[
                "Check the SSL certificate expiration date on the NYC VPN gateway.",
                "If the gateway certificate has expired, coordinate with the security team to issue a new certificate.",
                "If the issue is client-side, push updated root CA certificates via Intune.",
                "Verify that the system clock on the user's laptop is correct.",
                "Confirm the user can connect successfully after the certificate is renewed.",
            ],
            reporter_name="Wei Lin Tan",
            reporter_email="weilin.tan@contoso.com",
            reporter_department="Data Engineering",
            channel=Channel.PORTAL,
            tags=["vpn", "certificate", "ssl", "singapore"],
            difficulty="medium",
        ),
        # -------------------------------------------------------------------
        # 5. WiFi slow on entire 7th floor NYC
        # -------------------------------------------------------------------
        ScenarioDefinition(
            scenario_id="NET-005",
            subject="WiFi crawling on 7th floor - whole trading desk affected",
            description=(
                "The entire 7th floor WiFi has been painfully slow since about 10am today. Speed tests "
                "show 2-3 Mbps down when we normally get 200+. This is impacting the whole trading desk - "
                "roughly 60 people. Bloomberg terminals on WiFi are timing out and we're losing real-time "
                "market data feeds. Multiple traders have already complained. This is directly impacting "
                "our ability to execute trades."
            ),
            category=Category.NETWORK,
            priority=Priority.P1,
            team=Team.NETWORK_OPS,
            needs_escalation=True,
            missing_info=[
                MissingInfo.TIMESTAMP,
            ],
            next_best_action=(
                "Dispatch network engineer to the 7th floor immediately to inspect access points and switch "
                "uplinks; check for rogue devices or channel interference."
            ),
            remediation_steps=[
                "Log into the wireless controller and check AP health for 7th floor access points.",
                "Look for channel congestion, excessive client associations, or rogue APs.",
                "Check the uplink switch ports for errors, CRC issues, or bandwidth saturation.",
                "If an AP is faulty, failover clients to adjacent APs and schedule a replacement.",
                "Verify trading desk connectivity is restored to acceptable speeds.",
                "Communicate resolution status to the trading floor manager.",
            ],
            reporter_name="James Whitfield",
            reporter_email="james.whitfield@contoso.com",
            reporter_department="Equity Trading",
            channel=Channel.PHONE,
            created_at="2026-03-18T10:22:00Z",
            tags=["wifi", "trading", "p1", "floor-wide", "nyc"],
            difficulty="hard",
        ),
        # -------------------------------------------------------------------
        # 6. WiFi RADIUS authentication failing
        # -------------------------------------------------------------------
        ScenarioDefinition(
            scenario_id="NET-006",
            subject="Can't join ContosoSecure WiFi - authentication error",
            description=(
                "I just got a new laptop (Surface Pro 10) from IT yesterday and I can see the ContosoSecure "
                "SSID but when I try to connect it says 'Can't connect to this network.' The open guest WiFi "
                "works fine. My old laptop connected without issues. I'm on the 3rd floor of the London office."
            ),
            category=Category.NETWORK,
            priority=Priority.P3,
            team=Team.NETWORK_OPS,
            needs_escalation=False,
            missing_info=[
                MissingInfo.DEVICE_INFO,
                MissingInfo.AUTHENTICATION_METHOD,
            ],
            next_best_action=(
                "Verify the new device has the correct 802.1X/RADIUS certificate provisioned via Intune "
                "and that its MAC address is registered in the NAC system."
            ),
            remediation_steps=[
                "Confirm the device has received its machine certificate via Intune for 802.1X authentication.",
                "Check the RADIUS server logs for authentication attempts from the new device.",
                "If the certificate is missing, trigger a sync from the Intune portal for the device.",
                "Verify the device's WiFi adapter supports WPA3-Enterprise if that is the current policy.",
                "Test connectivity after the certificate is deployed.",
            ],
            reporter_name="Sophie Bennett",
            reporter_email="sophie.bennett@contoso.com",
            reporter_department="Compliance",
            channel=Channel.CHAT,
            tags=["wifi", "radius", "new-device", "london"],
            difficulty="easy",
        ),
        # -------------------------------------------------------------------
        # 7. DNS resolution failing for internal services
        # -------------------------------------------------------------------
        ScenarioDefinition(
            scenario_id="NET-007",
            subject="Can't resolve internal hostnames - getting NXDOMAIN errors",
            description=(
                "For the last hour I've been unable to resolve any *.internal.contoso.com hostnames. "
                "nslookup returns NXDOMAIN for everything internal but external domains like google.com "
                "resolve fine. I'm hardwired on the 4th floor NYC. Checked with two colleagues next to me "
                "and they have the same issue. We rely on internal services for our daily risk calculations "
                "and this is blocking our morning run."
            ),
            category=Category.NETWORK,
            priority=Priority.P1,
            team=Team.NETWORK_OPS,
            needs_escalation=True,
            missing_info=[
                MissingInfo.ERROR_MESSAGE,
                MissingInfo.AFFECTED_USERS,
            ],
            next_best_action=(
                "Check the internal DNS servers for the internal.contoso.com zone to determine if there "
                "is a zone transfer failure or service outage."
            ),
            remediation_steps=[
                "Verify the status of both internal DNS servers (primary and secondary).",
                "Check if the internal.contoso.com forward lookup zone is loaded and healthy.",
                "Review recent DNS configuration changes or zone transfer logs for errors.",
                "If a DNS server is down, restart the DNS service and monitor zone replication.",
                "Flush DNS caches on affected clients using ipconfig /flushdns.",
                "Confirm internal name resolution is working for the affected users.",
            ],
            reporter_name="Ananya Patel",
            reporter_email="ananya.patel@contoso.com",
            reporter_department="Risk Management",
            channel=Channel.PORTAL,
            created_at="2026-03-18T08:15:00Z",
            tags=["dns", "internal", "nxdomain", "multiple-users"],
            difficulty="hard",
        ),
        # -------------------------------------------------------------------
        # 8. Firewall rule request for new vendor integration
        # -------------------------------------------------------------------
        ScenarioDefinition(
            scenario_id="NET-008",
            subject="Firewall rule request: allow outbound to Refinitiv API endpoints",
            description=(
                "We're onboarding a new market data feed from Refinitiv (formerly Thomson Reuters) and need "
                "firewall rules opened for the following:\n\n"
                "- Outbound TCP 443 to api.refinitiv.com (IP range: 159.220.0.0/16)\n"
                "- Outbound TCP 8080 to streaming.refinitiv.com\n"
                "- Source: Trading VLAN (10.50.0.0/24) in NYC\n\n"
                "Go-live date is March 25th. Change request CR-2026-0847 has been approved by InfoSec. "
                "Please implement at your earliest convenience."
            ),
            category=Category.NETWORK,
            priority=Priority.P3,
            team=Team.NETWORK_OPS,
            needs_escalation=False,
            missing_info=[],
            next_best_action=(
                "Validate the approved change request CR-2026-0847 and implement the firewall rules "
                "during the next maintenance window."
            ),
            remediation_steps=[
                "Verify change request CR-2026-0847 is approved in the change management system.",
                "Add the firewall rules to the NYC perimeter firewall for the Trading VLAN.",
                "Test outbound connectivity from a Trading VLAN host to the Refinitiv endpoints.",
                "Document the new rules in the firewall rule inventory.",
                "Notify the requestor that the rules are active and ready for go-live testing.",
            ],
            reporter_name="Richard Okonkwo",
            reporter_email="richard.okonkwo@contoso.com",
            reporter_department="Institutional Trading",
            channel=Channel.PORTAL,
            tags=["firewall", "change-request", "vendor", "refinitiv"],
            difficulty="easy",
        ),
        # -------------------------------------------------------------------
        # 9. Blocked port preventing application deployment
        # -------------------------------------------------------------------
        ScenarioDefinition(
            scenario_id="NET-009",
            subject="Port 5432 blocked between app servers and new Postgres cluster",
            description=(
                "We're trying to deploy a new microservice that connects to the Postgres cluster at "
                "db-postgres-prod-01.internal.contoso.com:5432 but connections are timing out. I can ping "
                "the host but telnet to port 5432 fails. The app servers are in the DMZ (10.20.30.0/24) and "
                "the DB is in the data VLAN (10.40.50.0/24). Pretty sure there's a firewall rule missing. "
                "We need this resolved before Thursday's release."
            ),
            category=Category.NETWORK,
            priority=Priority.P2,
            team=Team.NETWORK_OPS,
            needs_escalation=False,
            missing_info=[
                MissingInfo.CONFIGURATION_DETAILS,
                MissingInfo.PREVIOUS_TICKET_ID,
            ],
            next_best_action=(
                "Check the inter-VLAN firewall rules for traffic from the DMZ to the data VLAN on port 5432 "
                "and add the necessary rule if missing."
            ),
            remediation_steps=[
                "Confirm there is no existing firewall rule allowing TCP 5432 from 10.20.30.0/24 to 10.40.50.0/24.",
                "Request or create a change request for the new firewall rule.",
                "Implement the rule on the internal firewall after approval.",
                "Test connectivity from the app server to the Postgres cluster on port 5432.",
                "Confirm the microservice can establish database connections successfully.",
            ],
            reporter_name="Tomasz Kowalski",
            reporter_email="tomasz.kowalski@contoso.com",
            reporter_department="Cloud Infrastructure",
            channel=Channel.CHAT,
            tags=["firewall", "postgres", "deployment", "inter-vlan"],
            difficulty="medium",
        ),
        # -------------------------------------------------------------------
        # 10. Trading floor latency spikes
        # -------------------------------------------------------------------
        ScenarioDefinition(
            scenario_id="NET-010",
            subject="Unacceptable latency spikes on trading floor - 200ms+ to exchange",
            description=(
                "URGENT: We are seeing latency spikes of 200-400ms to the NYSE matching engine. Normal "
                "baseline is under 5ms. This started at approximately 9:15am EST today. The latency is "
                "intermittent - it's fine for a few minutes then spikes. This is causing order rejections "
                "and we've already missed several fills. The entire equities desk is affected.\n\n"
                "We need someone on this NOW. Estimated revenue impact is $50K+ per hour."
            ),
            category=Category.NETWORK,
            priority=Priority.P1,
            team=Team.NETWORK_OPS,
            needs_escalation=True,
            missing_info=[
                MissingInfo.NETWORK_LOCATION,
            ],
            next_best_action=(
                "Immediately investigate the network path from the trading floor to the exchange co-location "
                "for packet loss, jitter, or link saturation."
            ),
            remediation_steps=[
                "Run continuous traceroute and latency monitoring from the trading floor to the exchange gateway.",
                "Check all intermediate switches and routers for interface errors, packet drops, or high CPU.",
                "Verify the dedicated low-latency circuit to the exchange is not experiencing provider issues.",
                "Contact the exchange connectivity provider if the issue is beyond the Contoso network boundary.",
                "Engage the trading technology team to confirm application-layer behavior is normal.",
                "Provide real-time updates to the trading desk manager every 15 minutes until resolved.",
            ],
            reporter_name="Victoria Chase",
            reporter_email="victoria.chase@contoso.com",
            reporter_department="Equity Trading",
            channel=Channel.PHONE,
            created_at="2026-03-18T09:18:00Z",
            tags=["latency", "trading", "p1", "exchange", "revenue-impact"],
            difficulty="hard",
        ),
        # -------------------------------------------------------------------
        # 11. Video call quality issues on Teams
        # -------------------------------------------------------------------
        ScenarioDefinition(
            scenario_id="NET-011",
            subject="Teams calls constantly freezing and dropping",
            description=(
                "For the past week my Teams video calls have been terrible. The video freezes every few "
                "minutes and sometimes the call drops completely. Audio gets choppy too. It happens whether "
                "I'm in a 1:1 or a large meeting. I've tested on both WiFi and ethernet in the London office "
                "5th floor and the problem is the same. Other apps like web browsing seem fine. I have client "
                "meetings all day and this is embarrassing."
            ),
            category=Category.NETWORK,
            priority=Priority.P3,
            team=Team.NETWORK_OPS,
            needs_escalation=False,
            missing_info=[
                MissingInfo.DEVICE_INFO,
                MissingInfo.REPRODUCTION_FREQUENCY,
                MissingInfo.SCREENSHOT_OR_ATTACHMENT,
            ],
            next_best_action=(
                "Pull the Teams call quality dashboard (CQD) data for the user and check for packet loss, "
                "jitter, or QoS misconfigurations on the London 5th floor network segment."
            ),
            remediation_steps=[
                "Access the Teams Admin Center Call Quality Dashboard and review the user's recent call analytics.",
                "Identify whether the issue is packet loss, jitter, or bandwidth related.",
                "Check QoS policies on the London office switches to ensure Teams traffic is prioritized.",
                "Verify the user's network segment is not saturated during peak hours.",
                "If the issue is localized, check the specific switch port and cable for errors.",
                "Schedule a test call with the user after applying fixes to confirm improvement.",
            ],
            reporter_name="Oliver Campbell",
            reporter_email="oliver.campbell@contoso.com",
            reporter_department="Client Services",
            channel=Channel.EMAIL,
            tags=["teams", "video", "call-quality", "london"],
            difficulty="medium",
        ),
        # -------------------------------------------------------------------
        # 12. Network drive mapping failure
        # -------------------------------------------------------------------
        ScenarioDefinition(
            scenario_id="NET-012",
            subject="Mapped network drive (S:) disappeared after restart",
            description=(
                "My S: drive mapping to \\\\fileserver-nyc-01\\shared\\finance stopped working after I "
                "restarted my computer this morning. When I try to remap it manually I get 'The network "
                "path was not found.' Other drives like H: (home) work fine. I need access to the quarterly "
                "close documents ASAP as we're in the middle of month-end close."
            ),
            category=Category.NETWORK,
            priority=Priority.P2,
            team=Team.NETWORK_OPS,
            needs_escalation=False,
            missing_info=[
                MissingInfo.ERROR_MESSAGE,
                MissingInfo.DEVICE_INFO,
            ],
            next_best_action=(
                "Verify the fileserver-nyc-01 SMB share is accessible and check if the finance share "
                "path or DFS namespace has changed."
            ),
            remediation_steps=[
                "Ping fileserver-nyc-01 to confirm it is reachable from the user's workstation.",
                "Check if the SMB service is running on fileserver-nyc-01.",
                "Verify the share path \\\\fileserver-nyc-01\\shared\\finance exists and permissions are intact.",
                "Check the DFS namespace if the share is published via DFS.",
                "Remap the drive for the user and ensure the mapping persists via Group Policy or login script.",
            ],
            reporter_name="Linda Nakamura",
            reporter_email="linda.nakamura@contoso.com",
            reporter_department="Finance",
            channel=Channel.PORTAL,
            tags=["network-drive", "smb", "file-share", "month-end"],
            difficulty="easy",
        ),
        # -------------------------------------------------------------------
        # 13. Proxy blocking external SaaS application
        # -------------------------------------------------------------------
        ScenarioDefinition(
            scenario_id="NET-013",
            subject="Can't access Tableau Online - proxy error page",
            description=(
                "When I try to open Tableau Online (online.tableau.com) I get a proxy error page saying "
                "'Access Denied - This site is blocked by your organization.' We just purchased Tableau "
                "Online licenses last week and the vendor says their side is configured. Nobody on my team "
                "can reach it. We have 15 analysts who need access by end of week for the board reporting "
                "cycle. Screenshot of the error attached."
            ),
            category=Category.NETWORK,
            priority=Priority.P2,
            team=Team.NETWORK_OPS,
            needs_escalation=False,
            missing_info=[
                MissingInfo.NETWORK_LOCATION,
                MissingInfo.AFFECTED_USERS,
            ],
            next_best_action=(
                "Add online.tableau.com and its associated CDN domains to the proxy allowlist "
                "after confirming the SaaS procurement approval."
            ),
            remediation_steps=[
                "Verify the Tableau Online subscription and approval documentation.",
                "Identify all required domains for Tableau Online (online.tableau.com, *.tableau.com CDN).",
                "Add the domains to the web proxy allowlist category.",
                "Push the updated proxy policy to all proxy appliances.",
                "Confirm access from the user's workstation and have the team of 15 analysts verify as well.",
            ],
            reporter_name="Grace Kim",
            reporter_email="grace.kim@contoso.com",
            reporter_department="Data Science",
            channel=Channel.EMAIL,
            attachments=["proxy_error_screenshot.png"],
            tags=["proxy", "saas", "tableau", "access-denied"],
            difficulty="easy",
        ),
        # -------------------------------------------------------------------
        # 14. NY-London VPN tunnel down
        # -------------------------------------------------------------------
        ScenarioDefinition(
            scenario_id="NET-014",
            subject="NY-London site-to-site VPN appears to be down",
            description=(
                "We're getting reports from multiple teams that London staff cannot reach NYC-hosted "
                "applications including the trading platform, internal Git repositories, and the HR portal. "
                "Confirmed with the London NOC that internet connectivity is fine locally. This looks like "
                "the site-to-site tunnel between NYC and London is down. Approximately 800 London employees "
                "are affected. Started around 14:00 GMT."
            ),
            category=Category.NETWORK,
            priority=Priority.P1,
            team=Team.NETWORK_OPS,
            needs_escalation=True,
            missing_info=[],
            next_best_action=(
                "Check the IPsec/IKE tunnel status on both the NYC and London VPN concentrators and "
                "re-establish the tunnel immediately."
            ),
            remediation_steps=[
                "Log into the NYC and London VPN concentrators to check IPsec tunnel status.",
                "Review logs for IKE negotiation failures or certificate expiration.",
                "Attempt to manually re-establish the tunnel from both ends.",
                "If the tunnel cannot be restored, check the underlying WAN circuit status with the ISP.",
                "Activate the backup SD-WAN path if available while troubleshooting the primary tunnel.",
                "Provide status updates to the London office every 10 minutes.",
            ],
            reporter_name="Daniel Okeke",
            reporter_email="daniel.okeke@contoso.com",
            reporter_department="Operations",
            channel=Channel.PHONE,
            created_at="2026-03-18T14:05:00Z",
            tags=["site-to-site", "vpn", "tunnel", "london", "p1", "major-outage"],
            difficulty="hard",
        ),
        # -------------------------------------------------------------------
        # 15. Guest WiFi access for visiting clients
        # -------------------------------------------------------------------
        ScenarioDefinition(
            scenario_id="NET-015",
            subject="Need guest WiFi for 12 clients visiting tomorrow",
            description=(
                "Hi, we have 12 clients from Goldman Sachs visiting our NYC office tomorrow for a full-day "
                "workshop in conference rooms 8A and 8B on the 8th floor. They'll need internet access for "
                "demos and presentations. Can we get guest WiFi credentials set up? The visit is from "
                "9am to 5pm on March 19th. Please provide individual credentials if possible for security "
                "audit purposes."
            ),
            category=Category.NETWORK,
            priority=Priority.P3,
            team=Team.NETWORK_OPS,
            needs_escalation=False,
            missing_info=[
                MissingInfo.CONTACT_INFO,
            ],
            next_best_action=(
                "Generate 12 individual guest WiFi vouchers with a 24-hour expiration and send them to "
                "the requestor for distribution."
            ),
            remediation_steps=[
                "Create 12 guest WiFi accounts on the captive portal with individual usernames.",
                "Set the account validity period from March 19, 9am to March 19, 6pm.",
                "Ensure guest VLAN traffic is isolated from the corporate network.",
                "Verify the 8th floor access points are broadcasting the guest SSID.",
                "Email the credentials to the requestor with printing instructions for the visitors.",
            ],
            reporter_name="Elena Vasquez",
            reporter_email="elena.vasquez@contoso.com",
            reporter_department="Client Services",
            channel=Channel.EMAIL,
            tags=["guest-wifi", "visitor", "nyc", "scheduled"],
            difficulty="easy",
        ),
        # -------------------------------------------------------------------
        # 16. Captive portal not loading for guest WiFi
        # -------------------------------------------------------------------
        ScenarioDefinition(
            scenario_id="NET-016",
            subject="Guest WiFi captive portal not loading - clients stuck in lobby",
            description=(
                "I have important clients from JPMorgan in the NYC lobby RIGHT NOW and the guest WiFi "
                "captive portal is not loading on any of their devices. They connect to ContosoGuest but "
                "the login page never appears. We've tried iPhones, iPads, and Windows laptops. "
                "This is extremely embarrassing. Can someone look at this immediately? Our CEO is in "
                "the meeting."
            ),
            category=Category.NETWORK,
            priority=Priority.P1,
            team=Team.NETWORK_OPS,
            needs_escalation=True,
            missing_info=[
                MissingInfo.NETWORK_LOCATION,
            ],
            next_best_action=(
                "Check the captive portal service status and the DHCP pool for the guest VLAN to "
                "restore access for the visiting clients."
            ),
            remediation_steps=[
                "Verify the captive portal web service is running on the wireless controller.",
                "Check if the guest VLAN DHCP pool is exhausted.",
                "Restart the captive portal service if it is unresponsive.",
                "As an immediate workaround, create temporary MAC-bypass entries for the client devices.",
                "Test captive portal functionality from a personal device to confirm restoration.",
                "Inform the requestor once guests can access the network.",
            ],
            reporter_name="Jonathan Price",
            reporter_email="jonathan.price@contoso.com",
            reporter_department="Executive Operations",
            channel=Channel.PHONE,
            created_at="2026-03-18T09:45:00Z",
            tags=["guest-wifi", "captive-portal", "vip", "urgent", "ceo"],
            difficulty="medium",
        ),
        # -------------------------------------------------------------------
        # 17. VLAN change request for team relocation
        # -------------------------------------------------------------------
        ScenarioDefinition(
            scenario_id="NET-017",
            subject="VLAN change needed - Quant team moving to 6th floor",
            description=(
                "The Quantitative Analysis team (8 people) is relocating from the 4th floor to the 6th "
                "floor of the NYC office next Monday (March 24). They need to remain on VLAN 150 (the "
                "quant research VLAN) because they have specific firewall rules and access to the HPC "
                "cluster. The 6th floor currently only has VLANs 100 and 200. Could you please trunk "
                "VLAN 150 to the 6th floor switch and configure ports 1-8 in patch panel 6C?\n\n"
                "Change request CR-2026-0903 has been filed."
            ),
            category=Category.NETWORK,
            priority=Priority.P3,
            team=Team.NETWORK_OPS,
            needs_escalation=False,
            missing_info=[],
            next_best_action=(
                "Schedule the VLAN trunking and port configuration for VLAN 150 on the 6th floor switch "
                "per the approved change request."
            ),
            remediation_steps=[
                "Verify change request CR-2026-0903 is approved.",
                "Trunk VLAN 150 from the distribution switch to the 6th floor access switch.",
                "Configure switch ports corresponding to patch panel 6C ports 1-8 as access ports on VLAN 150.",
                "Test connectivity from each port to the HPC cluster and other VLAN 150 resources.",
                "Coordinate with Facilities to ensure physical cabling is complete before Monday.",
                "Confirm with the Quant team lead after the move that all workstations are connected.",
            ],
            reporter_name="Raj Mehta",
            reporter_email="raj.mehta@contoso.com",
            reporter_department="Quantitative Analysis",
            channel=Channel.PORTAL,
            tags=["vlan", "relocation", "change-request", "scheduled"],
            difficulty="medium",
        ),
        # -------------------------------------------------------------------
        # 18. Can't reach server on different subnet
        # -------------------------------------------------------------------
        ScenarioDefinition(
            scenario_id="NET-018",
            subject="New test server unreachable from dev machines",
            description=(
                "We just provisioned a new test server (test-srv-042, IP 10.60.20.15) in the QA VLAN but "
                "none of our developers can reach it from the dev VLAN (10.30.10.0/24). Ping times out and "
                "traceroute dies at the core switch. We need this for sprint testing starting tomorrow. "
                "The server itself is up and running - I can access it from another machine in the QA VLAN."
            ),
            category=Category.NETWORK,
            priority=Priority.P2,
            team=Team.NETWORK_OPS,
            needs_escalation=False,
            missing_info=[
                MissingInfo.CONFIGURATION_DETAILS,
            ],
            next_best_action=(
                "Check the inter-VLAN routing ACLs on the core switch to ensure traffic from the dev VLAN "
                "to the QA VLAN is permitted."
            ),
            remediation_steps=[
                "Review ACLs on the core switch for dev VLAN (10.30.10.0/24) to QA VLAN (10.60.20.0/24) traffic.",
                "Add a permit rule for the required traffic if missing.",
                "Verify the default gateway on test-srv-042 is correctly set to the QA VLAN gateway.",
                "Test bidirectional connectivity between a dev workstation and the test server.",
                "Update the network documentation with the new server and any ACL changes.",
            ],
            reporter_name="Chris Andersen",
            reporter_email="chris.andersen@contoso.com",
            reporter_department="Quality Assurance",
            channel=Channel.CHAT,
            tags=["routing", "acl", "inter-vlan", "new-server"],
            difficulty="medium",
        ),
        # -------------------------------------------------------------------
        # 19. Full building network outage
        # -------------------------------------------------------------------
        ScenarioDefinition(
            scenario_id="NET-019",
            subject="BUILDING 2 NETWORK COMPLETELY DOWN - NO CONNECTIVITY",
            description=(
                "ALL CONNECTIVITY IS DOWN IN BUILDING 2 NYC. No WiFi, no wired, nothing. Phones are "
                "down too. Started about 5 minutes ago at 11:30am. There are approximately 400 people in "
                "this building across 6 floors including the entire Retail Banking and Settlements teams. "
                "People are using personal phones to submit this ticket. This is a total outage."
            ),
            category=Category.NETWORK,
            priority=Priority.P1,
            team=Team.NETWORK_OPS,
            needs_escalation=True,
            missing_info=[],
            next_best_action=(
                "Dispatch network engineers to the Building 2 MDF/IDF rooms immediately to check the "
                "core switch and power supply status."
            ),
            remediation_steps=[
                "Send a network engineer to the Building 2 main distribution frame (MDF) immediately.",
                "Check if the core switch has power and is operational.",
                "Verify uplink connectivity from Building 2 to the campus core.",
                "If the core switch is down, attempt a restart or failover to the redundant unit.",
                "Check UPS and power feeds to the MDF.",
                "Provide updates every 10 minutes to the incident management channel.",
                "Once restored, verify connectivity floor by floor.",
            ],
            reporter_name="Sarah Mitchell",
            reporter_email="sarah.mitchell@contoso.com",
            reporter_department="Retail Banking",
            channel=Channel.PHONE,
            created_at="2026-03-18T11:32:00Z",
            tags=["outage", "building-wide", "p1", "critical", "nyc"],
            difficulty="hard",
        ),
        # -------------------------------------------------------------------
        # 20. Singapore office high latency to NYC services
        # -------------------------------------------------------------------
        ScenarioDefinition(
            scenario_id="NET-020",
            subject="Singapore office - everything is slow connecting to NYC apps",
            description=(
                "Hi,\n\nFor the past two days our Singapore office has been experiencing very slow access "
                "to NYC-hosted applications. SharePoint takes 30+ seconds to load pages, the internal CRM "
                "is nearly unusable, and file transfers to the NYC file server are crawling. Local Singapore "
                "resources and internet browsing are fine. This affects all ~350 Singapore employees.\n\n"
                "We suspect something with the MPLS circuit. Can you please investigate?\n\n"
                "Regards,\nMei Ling"
            ),
            category=Category.NETWORK,
            priority=Priority.P2,
            team=Team.NETWORK_OPS,
            needs_escalation=True,
            missing_info=[
                MissingInfo.TIMESTAMP,
                MissingInfo.BUSINESS_IMPACT,
            ],
            next_best_action=(
                "Check the MPLS circuit utilization and latency between the Singapore and NYC offices "
                "and engage the WAN provider if circuit degradation is detected."
            ),
            remediation_steps=[
                "Check MPLS circuit utilization graphs for the Singapore-NYC link over the past 48 hours.",
                "Run latency and packet loss tests from the Singapore router to the NYC router.",
                "If the circuit is saturated, identify the top bandwidth consumers via NetFlow data.",
                "Contact the MPLS provider to check for any circuit issues or maintenance activities.",
                "If degradation is confirmed, request a temporary bandwidth upgrade or activate the backup path.",
                "Verify application performance improves after remediation.",
            ],
            reporter_name="Mei Ling Chow",
            reporter_email="meiling.chow@contoso.com",
            reporter_department="Operations",
            channel=Channel.EMAIL,
            tags=["latency", "singapore", "mpls", "wan", "inter-office"],
            difficulty="hard",
        ),
        # -------------------------------------------------------------------
        # 21. Load balancer intermittent failures
        # -------------------------------------------------------------------
        ScenarioDefinition(
            scenario_id="NET-021",
            subject="Internal API gateway returning 502 errors intermittently",
            description=(
                "Our internal API gateway at api-gw.internal.contoso.com is returning 502 Bad Gateway "
                "errors roughly 30% of the time. It seems like one of the backend servers behind the F5 "
                "load balancer might be unhealthy. The errors started this morning after the backend team "
                "deployed a new version of the portfolio service. When it works it's fine, but every third "
                "or fourth request fails. This is impacting the client-facing portfolio dashboard."
            ),
            category=Category.NETWORK,
            priority=Priority.P2,
            team=Team.NETWORK_OPS,
            needs_escalation=False,
            missing_info=[
                MissingInfo.AFFECTED_SYSTEM,
                MissingInfo.ERROR_MESSAGE,
            ],
            next_best_action=(
                "Check the F5 load balancer pool member health status for the API gateway and disable "
                "any unhealthy backend nodes."
            ),
            remediation_steps=[
                "Log into the F5 load balancer and check the pool member status for the API gateway virtual server.",
                "Identify which backend server(s) are failing health checks.",
                "Temporarily disable the unhealthy node(s) to stop traffic from being routed to them.",
                "Coordinate with the backend team to investigate the failed deployment on the unhealthy node.",
                "Re-enable the node once the deployment issue is resolved and health checks pass.",
                "Monitor the error rate to confirm it drops to zero.",
            ],
            reporter_name="Kenji Yoshida",
            reporter_email="kenji.yoshida@contoso.com",
            reporter_department="Frontend Engineering",
            channel=Channel.CHAT,
            tags=["load-balancer", "f5", "502", "api-gateway"],
            difficulty="medium",
        ),
        # -------------------------------------------------------------------
        # 22. SD-WAN failover not working at branch
        # -------------------------------------------------------------------
        ScenarioDefinition(
            scenario_id="NET-022",
            subject="SD-WAN failover didn't kick in during ISP outage at London office",
            description=(
                "During yesterday's BT circuit outage at the London office (approximately 2pm-4pm GMT), "
                "the SD-WAN was supposed to fail over to the backup Vodafone circuit but it didn't. "
                "The entire London office lost connectivity for 2 hours. We pay for dual-ISP redundancy "
                "specifically to avoid this. Please investigate why the failover didn't trigger and fix it "
                "so this doesn't happen again. Attaching the Meraki dashboard screenshots showing the outage."
            ),
            category=Category.NETWORK,
            priority=Priority.P2,
            team=Team.NETWORK_OPS,
            needs_escalation=True,
            missing_info=[
                MissingInfo.CONFIGURATION_DETAILS,
            ],
            next_best_action=(
                "Review the SD-WAN failover policy and Meraki MX appliance logs to determine why "
                "the secondary ISP path was not activated during the BT outage."
            ),
            remediation_steps=[
                "Pull the Meraki MX event logs for the London office for the outage window.",
                "Check the SD-WAN uplink health check configuration for the BT and Vodafone circuits.",
                "Verify the Vodafone backup circuit was physically up and had a valid default route.",
                "Review failover policy thresholds (packet loss, latency, jitter) and adjust if too permissive.",
                "Simulate a failover by disabling the primary uplink in a maintenance window to test.",
                "Document the root cause and corrective actions taken.",
            ],
            reporter_name="Fiona MacGregor",
            reporter_email="fiona.macgregor@contoso.com",
            reporter_department="Operations",
            channel=Channel.EMAIL,
            attachments=["meraki_outage_dashboard.png", "meraki_uplink_status.png"],
            tags=["sd-wan", "failover", "london", "redundancy", "meraki"],
            difficulty="hard",
        ),
        # -------------------------------------------------------------------
        # 23. DNS for specific service failing
        # -------------------------------------------------------------------
        ScenarioDefinition(
            scenario_id="NET-023",
            subject="crm.contoso.com not resolving but other sites work",
            description=(
                "Since about 8am today, crm.contoso.com is not resolving. I get a 'DNS_PROBE_FINISHED_NXDOMAIN' "
                "error in Chrome. Other internal sites like mail.contoso.com and intranet.contoso.com work "
                "fine. Tried from my laptop and my phone on the office WiFi - same result. I'm in the NYC "
                "office, 3rd floor. The CRM team says the server is running fine."
            ),
            category=Category.NETWORK,
            priority=Priority.P2,
            team=Team.NETWORK_OPS,
            needs_escalation=False,
            missing_info=[
                MissingInfo.AFFECTED_USERS,
            ],
            next_best_action=(
                "Check the DNS zone for crm.contoso.com to see if the A record is missing, expired, "
                "or was accidentally deleted."
            ),
            remediation_steps=[
                "Query the authoritative DNS server for the crm.contoso.com record.",
                "If the record is missing, check DNS change logs to see if it was accidentally deleted.",
                "Re-create or restore the DNS A record pointing to the CRM server's IP address.",
                "Flush the DNS cache on the DNS server and verify propagation.",
                "Have the user clear their local DNS cache and confirm crm.contoso.com resolves.",
            ],
            reporter_name="Hannah Park",
            reporter_email="hannah.park@contoso.com",
            reporter_department="Client Services",
            channel=Channel.PORTAL,
            created_at="2026-03-18T08:30:00Z",
            tags=["dns", "crm", "single-service", "nxdomain"],
            difficulty="easy",
        ),
        # -------------------------------------------------------------------
        # 24. One-way audio on Teams calls
        # -------------------------------------------------------------------
        ScenarioDefinition(
            scenario_id="NET-024",
            subject="Teams calls - people can hear me but I can't hear them",
            description=(
                "For the last three days, on every Teams call I can speak and people hear me fine, but I "
                "get no audio from their side. It's not a headset issue - I've tried the laptop speakers, "
                "two different USB headsets, and Bluetooth earbuds. Same problem on all of them. Restarting "
                "Teams doesn't help. I'm in the Singapore office on the 4th floor, connected to ethernet. "
                "This is making it impossible to participate in meetings."
            ),
            category=Category.NETWORK,
            priority=Priority.P3,
            team=Team.NETWORK_OPS,
            needs_escalation=False,
            missing_info=[
                MissingInfo.DEVICE_INFO,
                MissingInfo.STEPS_TO_REPRODUCE,
                MissingInfo.APPLICATION_VERSION,
            ],
            next_best_action=(
                "Check for asymmetric NAT or firewall rules blocking inbound UDP media traffic to the "
                "user's workstation, and review Teams call analytics for media path details."
            ),
            remediation_steps=[
                "Review the user's Teams call analytics for the last three days to check media connectivity.",
                "Look for ICE negotiation failures or relay-only media paths indicating firewall issues.",
                "Verify the Singapore office firewall allows inbound UDP on the Teams media port range (50000-50019).",
                "Check if a recent firewall policy change may have blocked inbound RTP traffic.",
                "Test from the user's workstation after any firewall adjustments.",
                "If the issue persists, escalate to the Enterprise Applications team for a client-side investigation.",
            ],
            reporter_name="Arun Krishnan",
            reporter_email="arun.krishnan@contoso.com",
            reporter_department="Product Management",
            channel=Channel.CHAT,
            tags=["teams", "audio", "one-way", "singapore", "firewall"],
            difficulty="hard",
        ),
        # -------------------------------------------------------------------
        # 25. SSL/TLS connection error to internal portal
        # -------------------------------------------------------------------
        ScenarioDefinition(
            scenario_id="NET-025",
            subject="SSL error accessing internal HR portal - NET::ERR_CERT_AUTHORITY_INVALID",
            description=(
                "When I try to access hr.internal.contoso.com in Chrome I get a big red warning page: "
                "'Your connection is not private - NET::ERR_CERT_AUTHORITY_INVALID.' I can click through "
                "the warning but that doesn't seem safe. This started after Chrome updated to version 124 "
                "yesterday. Firefox shows a similar warning. My colleague sitting next to me has the same "
                "issue. We need to access the HR portal for performance review submissions due this week."
            ),
            category=Category.NETWORK,
            priority=Priority.P3,
            team=Team.NETWORK_OPS,
            needs_escalation=False,
            missing_info=[
                MissingInfo.ENVIRONMENT_DETAILS,
            ],
            next_best_action=(
                "Check if the internal CA root certificate is installed in the affected machines' trust "
                "stores and verify the HR portal's certificate chain is complete."
            ),
            remediation_steps=[
                "Inspect the SSL certificate on hr.internal.contoso.com for chain completeness.",
                "Verify the intermediate and root CA certificates are properly installed on the web server.",
                "Check if Chrome 124 has deprecated the cipher suite or certificate type used.",
                "If the internal CA root is missing from client machines, push it via Group Policy or Intune.",
                "Test from an affected workstation after deploying the certificate fix.",
            ],
            reporter_name="David Thompson",
            reporter_email="david.thompson@contoso.com",
            reporter_department="HR",
            channel=Channel.PORTAL,
            tags=["ssl", "tls", "certificate", "chrome", "hr-portal"],
            difficulty="medium",
        ),
        # -------------------------------------------------------------------
        # 26. File transfer extremely slow between offices
        # -------------------------------------------------------------------
        ScenarioDefinition(
            scenario_id="NET-026",
            subject="File transfers from London to NYC taking hours instead of minutes",
            description=(
                "I'm trying to transfer a 2GB dataset from the London file server to the NYC analytics "
                "share and it's estimating 6+ hours. This same transfer used to take about 15 minutes. "
                "I've tried multiple times today and it's consistently slow. Small files are slow too. "
                "I have a tight deadline for the regulatory report and need this data transferred today. "
                "Is there something wrong with the link between offices?"
            ),
            category=Category.NETWORK,
            priority=Priority.P2,
            team=Team.NETWORK_OPS,
            needs_escalation=False,
            missing_info=[
                MissingInfo.NETWORK_LOCATION,
                MissingInfo.TIMESTAMP,
            ],
            next_best_action=(
                "Check the WAN link utilization between London and NYC and investigate whether bandwidth "
                "is being consumed by another process or if the link is degraded."
            ),
            remediation_steps=[
                "Check the bandwidth utilization on the London-NYC WAN link.",
                "Use NetFlow or sFlow data to identify top bandwidth consumers.",
                "If a specific application or backup job is saturating the link, apply QoS or reschedule it.",
                "Verify the WAN optimization appliance (if deployed) is functioning correctly.",
                "Test file transfer speed after remediation to confirm improvement.",
                "Suggest the user use a scheduled file replication service for large transfers in the future.",
            ],
            reporter_name="Alexander Brooks",
            reporter_email="alexander.brooks@contoso.com",
            reporter_department="Regulatory Affairs",
            channel=Channel.EMAIL,
            tags=["file-transfer", "wan", "slow", "london-nyc"],
            difficulty="medium",
        ),
        # -------------------------------------------------------------------
        # 27. APAC trading system network latency
        # -------------------------------------------------------------------
        ScenarioDefinition(
            scenario_id="NET-027",
            subject="Latency to APAC exchanges degraded - SGX and HKEX affected",
            description=(
                "Our direct market access connections to SGX (Singapore Exchange) and HKEX (Hong Kong Exchange) "
                "are showing degraded latency. Normal round-trip is ~2ms to SGX and ~8ms to HKEX from our "
                "Singapore colo. Current readings are 15ms and 40ms respectively. The APAC trading desk is "
                "reporting fill rate degradation and our algo strategies are underperforming. Started at "
                "market open (9am SGT). Revenue impact estimated at $25K/hour."
            ),
            category=Category.NETWORK,
            priority=Priority.P1,
            team=Team.NETWORK_OPS,
            needs_escalation=True,
            missing_info=[
                MissingInfo.NETWORK_LOCATION,
            ],
            next_best_action=(
                "Check the dedicated exchange connectivity circuits at the Singapore colocation facility "
                "for degradation and engage the cross-connect provider immediately."
            ),
            remediation_steps=[
                "Log into the Singapore colo network equipment and check interface counters for errors or drops.",
                "Run latency baseline tests to both SGX and HKEX from the colo edge router.",
                "Check with the cross-connect providers for any fiber or circuit maintenance.",
                "Review the co-location facility's NOC alerts for any environmental issues (power, cooling).",
                "If the issue is provider-side, open priority tickets with each exchange connectivity vendor.",
                "Keep the APAC trading desk updated every 15 minutes with status.",
            ],
            reporter_name="Liam Wong",
            reporter_email="liam.wong@contoso.com",
            reporter_department="Derivatives",
            channel=Channel.PHONE,
            created_at="2026-03-18T01:05:00Z",
            tags=["trading", "latency", "apac", "exchange", "p1", "revenue-impact"],
            difficulty="hard",
        ),
        # -------------------------------------------------------------------
        # 28. Proxy authentication failure
        # -------------------------------------------------------------------
        ScenarioDefinition(
            scenario_id="NET-028",
            subject="Proxy keeps asking for credentials - can't browse the web",
            description=(
                "Every time I open a new tab in Chrome it pops up a proxy authentication dialog asking for "
                "username and password. Even if I enter my credentials it asks again on the next page. "
                "Edge does the same thing. I just changed my AD password yesterday for the quarterly "
                "rotation. Could that be related? I'm on a desktop in the NYC 2nd floor. Really can't "
                "get any work done like this."
            ),
            category=Category.NETWORK,
            priority=Priority.P3,
            team=Team.NETWORK_OPS,
            needs_escalation=False,
            missing_info=[
                MissingInfo.DEVICE_INFO,
                MissingInfo.AUTHENTICATION_METHOD,
            ],
            next_best_action=(
                "Clear cached proxy credentials on the user's machine and verify Kerberos authentication "
                "to the proxy is functioning after the password change."
            ),
            remediation_steps=[
                "Clear saved credentials in Windows Credential Manager for the proxy server.",
                "Run 'klist purge' to clear the Kerberos ticket cache and then run 'klist' to get a fresh TGT.",
                "Verify the proxy uses Kerberos/NTLM authentication and the user's new password is synced to AD.",
                "Check if the user's machine has received the latest Group Policy with proxy settings.",
                "Restart the browser and test web access.",
            ],
            reporter_name="Monica Reeves",
            reporter_email="monica.reeves@contoso.com",
            reporter_department="Marketing",
            channel=Channel.CHAT,
            tags=["proxy", "authentication", "password-change", "kerberos"],
            difficulty="easy",
        ),
        # -------------------------------------------------------------------
        # 29. WiFi AP overloaded in conference area
        # -------------------------------------------------------------------
        ScenarioDefinition(
            scenario_id="NET-029",
            subject="WiFi completely unusable during all-hands in the NYC auditorium",
            description=(
                "During today's quarterly all-hands meeting in the NYC auditorium (about 500 people), "
                "the WiFi was completely unusable. Nobody could load slides, Slido polls failed, and remote "
                "participants on Teams couldn't hear the presenters because the stream kept buffering. This "
                "happens every quarter. Can we please get this fixed permanently before the next all-hands? "
                "It reflects poorly on IT when the CEO's presentation can't be streamed."
            ),
            category=Category.NETWORK,
            priority=Priority.P3,
            team=Team.NETWORK_OPS,
            needs_escalation=False,
            missing_info=[
                MissingInfo.BUSINESS_IMPACT,
                MissingInfo.ENVIRONMENT_DETAILS,
            ],
            next_best_action=(
                "Assess the wireless capacity in the NYC auditorium and plan for additional access points "
                "or a high-density deployment to support 500+ concurrent clients."
            ),
            remediation_steps=[
                "Conduct a wireless site survey of the auditorium to assess current AP coverage and capacity.",
                "Review the AP client association limits and channel utilization during the all-hands timeframe.",
                "Plan a high-density WiFi deployment with additional APs, band steering, and client load balancing.",
                "Consider deploying a temporary high-density WiFi solution for the next all-hands as an interim fix.",
                "Test the new deployment with a simulated high-client environment.",
                "Provide a capacity plan and cost estimate for a permanent solution.",
            ],
            reporter_name="Patricia Dunn",
            reporter_email="patricia.dunn@contoso.com",
            reporter_department="Corporate Communications",
            channel=Channel.EMAIL,
            tags=["wifi", "capacity", "auditorium", "all-hands", "recurring"],
            difficulty="medium",
        ),
        # -------------------------------------------------------------------
        # 30. DFS replication issue causing stale files
        # -------------------------------------------------------------------
        ScenarioDefinition(
            scenario_id="NET-030",
            subject="DFS shares showing different files in London vs NYC",
            description=(
                "We've discovered that the files in \\\\contoso.com\\dfs\\shared\\legal are different "
                "depending on whether you're in the London or NYC office. A contract I saved in London "
                "yesterday isn't visible from NYC today, and vice versa. This is a serious issue for the "
                "legal team because we could be working on stale versions of contracts. We have a merger "
                "closing this Friday and need reliable file access across both offices."
            ),
            category=Category.NETWORK,
            priority=Priority.P2,
            team=Team.NETWORK_OPS,
            needs_escalation=True,
            missing_info=[
                MissingInfo.TIMESTAMP,
                MissingInfo.AFFECTED_SYSTEM,
            ],
            next_best_action=(
                "Check the DFS Replication (DFSR) health between the London and NYC file servers and "
                "resolve any replication backlog or conflict."
            ),
            remediation_steps=[
                "Run 'dfsrdiag backlog' between the London and NYC file servers to check for replication backlog.",
                "Check the DFSR event logs on both servers for errors or warnings.",
                "Verify the DFSR service is running on both servers and the replication group is healthy.",
                "If there is a staging area space issue, increase the staging quota.",
                "Force replication using 'dfsrdiag syncnow' and monitor until the backlog clears.",
                "Have the legal team verify that files are consistent across both offices after remediation.",
            ],
            reporter_name="Catherine Albright",
            reporter_email="catherine.albright@contoso.com",
            reporter_department="Legal",
            channel=Channel.PHONE,
            tags=["dfs", "replication", "file-share", "london-nyc", "legal"],
            difficulty="hard",
        ),
        # -------------------------------------------------------------------
        # 31. MAC filtering blocking new device
        # -------------------------------------------------------------------
        ScenarioDefinition(
            scenario_id="NET-031",
            subject="Brand new Bloomberg terminal can't get on the network",
            description=(
                "We just received a new Bloomberg terminal for the fixed income desk (asset tag BT-2026-0147) "
                "and it can't connect to the wired network. The link light on the switch port comes on but "
                "it never gets a DHCP address. We plugged a laptop into the same port and it works fine. "
                "I think it might be a MAC address filtering issue. The terminal's MAC is 00:1B:44:11:3A:B7. "
                "Can you whitelist it? We need it operational by market open tomorrow."
            ),
            category=Category.NETWORK,
            priority=Priority.P2,
            team=Team.NETWORK_OPS,
            needs_escalation=False,
            missing_info=[
                MissingInfo.NETWORK_LOCATION,
            ],
            next_best_action=(
                "Add the Bloomberg terminal's MAC address to the NAC whitelist for the trading VLAN "
                "and verify DHCP assignment."
            ),
            remediation_steps=[
                "Add MAC address 00:1B:44:11:3A:B7 to the network access control (NAC) approved device list.",
                "Assign the device to the trading VLAN in the NAC policy.",
                "Verify the switch port is configured for the correct VLAN with 802.1X or MAB authentication.",
                "Confirm the terminal receives a DHCP address and can reach Bloomberg services.",
                "Update the asset management system with the network registration details.",
            ],
            reporter_name="Thomas Baker",
            reporter_email="thomas.baker@contoso.com",
            reporter_department="Fixed Income",
            channel=Channel.PORTAL,
            tags=["mac-filtering", "nac", "bloomberg", "new-device", "trading"],
            difficulty="easy",
        ),
        # -------------------------------------------------------------------
        # 32. Jitter causing issues on real-time applications
        # -------------------------------------------------------------------
        ScenarioDefinition(
            scenario_id="NET-032",
            subject="Severe jitter on our floor - real-time pricing feeds affected",
            description=(
                "The Derivatives team on the 9th floor NYC is seeing severe network jitter (50ms+ variance) "
                "that's causing our real-time pricing feeds from ICE and CME to stutter. Our risk models "
                "depend on continuous low-jitter feeds and we're getting gap fills every few seconds. "
                "This started about an hour ago. We've checked locally and it doesn't seem to be our "
                "applications. Network monitoring shows the issue is between our floor switch and the core."
            ),
            category=Category.NETWORK,
            priority=Priority.P1,
            team=Team.NETWORK_OPS,
            needs_escalation=True,
            missing_info=[
                MissingInfo.SCREENSHOT_OR_ATTACHMENT,
            ],
            next_best_action=(
                "Investigate the switch-to-core uplinks on the 9th floor for micro-bursting, buffer "
                "overflows, or a failing transceiver module."
            ),
            remediation_steps=[
                "Check 9th floor switch uplink interfaces for CRC errors, input/output drops, and buffer misses.",
                "Inspect the SFP transceiver modules for optical power levels within specification.",
                "Look for micro-bursting traffic patterns using switch interface statistics.",
                "If a transceiver is degraded, replace it with a spare.",
                "Verify QoS markings are applied correctly for real-time trading traffic on the 9th floor.",
                "Monitor jitter measurements for 30 minutes after remediation to confirm stability.",
            ],
            reporter_name="Nicole Ferraro",
            reporter_email="nicole.ferraro@contoso.com",
            reporter_department="Derivatives",
            channel=Channel.PHONE,
            created_at="2026-03-18T14:30:00Z",
            tags=["jitter", "trading", "real-time", "p1", "9th-floor"],
            difficulty="hard",
        ),
    ]
