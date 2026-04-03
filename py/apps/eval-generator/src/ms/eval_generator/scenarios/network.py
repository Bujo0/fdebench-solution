# Copyright (c) Microsoft. All rights reserved.
"""Network & Connectivity category scenarios for eval dataset."""

from ms.eval_generator.scenarios._base import ScenarioDefinition
from ms.eval_generator.scenarios._base import ScenarioGold

NETWORK_SCENARIOS: list[ScenarioDefinition] = [
    # ──────────────────────────────────────────────────────────────────
    # 1. VPN drops when switching from Ethernet to WiFi
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="network-001",
        subjects=(
            "VPN drops when switching to WiFi",
            "VPN disconnects on network change",
        ),
        descriptions=(
            "Every time I undock my laptop and move to WiFi, the VPN disconnects and I have to reconnect "
            "manually. Started after last Tuesday's Windows update. Using GlobalProtect v3.2 on the NYC "
            "office WiFi, Floor 4.",
            "VPN keeps dropping when I walk between meeting rooms. The moment my laptop switches from wired "
            "to wireless, the VPN connection is killed. Very annoying — I lose my remote desktop sessions "
            "every time.",
        ),
        gold=ScenarioGold(
            category="Network & Connectivity",
            priority="P3",
            assigned_team="Network Operations",
            needs_escalation=False,
            missing_information=(
                "device_info",
            ),
            next_best_action="Investigate VPN client network roaming behavior and check for known issues with the recent update",
            remediation_steps=(
                "Check VPN client version and compare with known-good configuration",
                "Verify VPN client roaming settings to maintain connection during network transitions",
                "Test with the latest VPN client version if an update is available",
                "Check if the Windows update changed network adapter priority settings",
                "If issue persists, escalate to VPN vendor support",
            ),
        ),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 2. Office WiFi dead on Floor 3
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="network-002",
        subjects=(
            "WiFi completely down on Floor 3",
            "No wireless connectivity on 3rd floor",
        ),
        descriptions=(
            "WiFi has been completely dead on Floor 3 of Building A since about 9 AM. Nobody up here can "
            "connect. We've tried multiple devices — laptops, phones, tablets. The guest network doesn't "
            "show either. Floor 2 and Floor 4 WiFi works fine.",
            "All wireless access on the 3rd floor stopped working this morning. About 40 people are "
            "affected. Some people moved to other floors but most can't. We have client meetings scheduled "
            "here all afternoon.",
        ),
        gold=ScenarioGold(
            category="Network & Connectivity",
            priority="P2",
            assigned_team="Network Operations",
            needs_escalation=False,
            missing_information=(
                "network_location",
            ),
            next_best_action="Investigate Floor 3 access point status and check for PoE switch or AP controller issues",
            remediation_steps=(
                "Check the status of all wireless access points on Floor 3 in the controller",
                "Verify the PoE switch powering Floor 3 APs is operational",
                "Check if recent network changes affected Floor 3 SSID broadcasting",
                "Restart any offline access points or the PoE switch if needed",
                "Deploy temporary wireless access points if fix requires extended downtime",
            ),
        ),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 3. DNS resolution failing for internal sites
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="network-003",
        subjects=(
            "Can't reach internal sites — DNS error",
            "Internal DNS not resolving company websites",
        ),
        descriptions=(
            "Getting 'DNS_PROBE_FINISHED_NXDOMAIN' when trying to access internal sites like "
            "portal.contoso.local and wiki.contoso.local. External sites like google.com work fine. Started "
            "about an hour ago. Using the office network on Floor 5.",
            "Internal DNS resolution is broken for me. nslookup shows 'server can't find "
            "portal.contoso.local' but nslookup google.com works. I'm hardwired on the trading floor "
            "network. Multiple colleagues have the same issue.",
        ),
        gold=ScenarioGold(
            category="Network & Connectivity",
            priority="P2",
            assigned_team="Network Operations",
            needs_escalation=False,
            missing_information=(
                "network_location",
                "affected_users",
            ),
            next_best_action="Check internal DNS server health and verify zone records for the contoso.local domain",
            remediation_steps=(
                "Check the health of internal DNS servers",
                "Verify the contoso.local forward lookup zone is loaded and responding",
                "Test DNS resolution from the DNS server itself",
                "Flush DNS cache on affected clients with ipconfig /flushdns",
                "If DNS server issue, restart the DNS service or failover to secondary DNS",
            ),
        ),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 4. Firewall rule request for new vendor portal
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="network-004",
        subjects=(
            "Firewall rule request — new vendor integration",
            "Need firewall exception for vendor API access",
        ),
        descriptions=(
            "We need a firewall rule opened for outbound HTTPS (443) to api.vendorplatform.com (IP range "
            "203.0.113.0/24). This is for our new payment processing integration that goes live next month. "
            "Security approved it in CHG-50123.",
            "Requesting a firewall change to allow traffic from our app servers (10.20.30.0/24) to the new "
            "Refinitiv market data endpoint at 198.51.100.50:8443. Change request CHG-50456 was approved by "
            "SecOps last Friday.",
        ),
        gold=ScenarioGold(
            category="Network & Connectivity",
            priority="P3",
            assigned_team="Network Operations",
            needs_escalation=False,
            missing_information=(),
            next_best_action="Implement the approved firewall rule change during the next maintenance window",
            remediation_steps=(
                "Verify the change request approval from SecOps",
                "Document the firewall rule with source, destination, port, and protocol",
                "Implement the rule in the change management window",
                "Test connectivity to the vendor endpoint after rule deployment",
                "Monitor traffic logs to confirm the rule is working as expected",
            ),
        ),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 5. Video call quality terrible
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="network-005",
        subjects=(
            "Teams video calls freezing and pixelated",
            "Terrible video call quality from office",
        ),
        descriptions=(
            "My Teams video calls have been awful for the past week. Video freezes every few seconds, audio "
            "cuts out, and screen sharing is unusable. I've tested my home internet (200 Mbps) and it's "
            "fine for everything else. It only happens with our corporate VPN connected.",
            "Video call quality is terrible in the Building B 2nd floor conference rooms. Every meeting has "
            "freezing, echo, and dropped participants. We tested with Zoom and WebEx too — same issues. "
            "It's definitely the network, not the app.",
        ),
        gold=ScenarioGold(
            category="Network & Connectivity",
            priority="P3",
            assigned_team="Network Operations",
            needs_escalation=False,
            missing_information=(
                "network_location",
                "reproduction_frequency",
            ),
            next_best_action="Analyze network QoS metrics and check for bandwidth or latency issues on the affected segment",
            remediation_steps=(
                "Run a network performance test from the affected location",
                "Check QoS policies for Teams/video conferencing traffic",
                "Analyze switch port statistics for packet loss or errors",
                "Verify the uplink bandwidth is sufficient for the number of concurrent video streams",
                "If QoS is not configured, implement DSCP marking for real-time traffic",
            ),
        ),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 6. VPN can't connect from home — timeout errors
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="network-006",
        subjects=(
            "Can't connect to VPN from home — connection times out",
            "VPN timeout when working remotely",
        ),
        descriptions=(
            "I haven't been able to connect to the company VPN from my home for 2 days. GlobalProtect shows "
            "'connection timed out' every time. I've restarted my router, tried both WiFi and Ethernet, and "
            "even used my phone hotspot. Same result. My colleague in the same area connects fine.",
            "VPN connection keeps timing out. Been working from home for months without issues until "
            "Wednesday. The client just spins and says 'gateway not responding.' I can access the internet "
            "fine and ping external sites. Just can't reach our VPN gateway.",
        ),
        gold=ScenarioGold(
            category="Network & Connectivity",
            priority="P3",
            assigned_team="Network Operations",
            needs_escalation=False,
            missing_information=(
                "environment_details",
                "error_message",
            ),
            next_best_action="Check VPN gateway health and verify the user's home network isn't blocking VPN protocols",
            remediation_steps=(
                "Verify VPN gateway is operational and accepting connections",
                "Check if the user's ISP is blocking the VPN port/protocol",
                "Verify the user's VPN client configuration matches the current gateway settings",
                "Test with an alternative VPN protocol if available",
                "If gateway is healthy, collect client-side diagnostic logs for analysis",
            ),
        ),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 7. Internet completely down in Building B
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="network-007",
        subjects=(
            "Internet down in entire Building B",
            "Complete network outage — Building B",
        ),
        descriptions=(
            "Building B has no internet connectivity at all. Started at 10:45 AM. Approximately 200 "
            "employees affected. Both wired and wireless are down. Phones on the VOIP system are also dead. "
            "We've checked — Building A is fine.",
            "Total network outage in Building B. Nothing works — no internet, no internal sites, no VoIP "
            "phones. Even the network printers are offline. This is a major disruption. The building houses "
            "our entire Client Services and Operations teams.",
        ),
        gold=ScenarioGold(
            category="Network & Connectivity",
            priority="P1",
            assigned_team="Network Operations",
            needs_escalation=True,
            missing_information=(),
            next_best_action=(
                "Investigate core network infrastructure for Building B — check uplink, core switch, and ISP "
                "connectivity"
            ),
            remediation_steps=(
                "Check the core switch and uplink connecting Building B to the campus network",
                "Verify ISP circuit status for Building B",
                "Check if a recent change or maintenance caused the outage",
                "If core switch failure, initiate failover or hardware replacement",
                "Provide regular status updates to affected teams every 15 minutes",
            ),
        ),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 8. Network drive inaccessible
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="network-008",
        subjects=(
            "Can't access the shared network drive",
            "Mapped drive to file server disconnected",
        ),
        descriptions=(
            "My mapped drive (Z:) to \\fileserver01\shared is showing 'network path not found.' It was "
            "working fine until this morning. I need access to the Finance department's shared files for "
            "month-end close. Other people in my team can still access it.",
            "The network drive where we store all our project files (\\nas-prod\projects) is inaccessible. "
            "Getting 'Windows cannot access' error. This affects our entire Engineering team of 30 people — "
            "we can't access any project repositories.",
        ),
        gold=ScenarioGold(
            category="Network & Connectivity",
            priority="P2",
            assigned_team="Network Operations",
            needs_escalation=False,
            missing_information=(
                "network_location",
                "error_message",
            ),
            next_best_action="Verify the file server is online and check network path resolution and SMB connectivity",
            remediation_steps=(
                "Ping the file server to check basic network connectivity",
                "Verify DNS resolution for the file server hostname",
                "Check the file server service status and SMB port accessibility",
                "Verify the user's network segment can reach the file server VLAN",
                "If server is down, restart the file service or failover to backup",
            ),
        ),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 9. Proxy blocking legitimate business website
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="network-009",
        subjects=(
            "Web proxy blocking a site I need for work",
            "Legitimate business website blocked by firewall",
        ),
        descriptions=(
            "Our web proxy is blocking access to www.moodys.com which I need for credit risk analysis. The "
            "block page says 'category: financial services — restricted.' This is a legitimate business "
            "tool. I've been using it for years until today.",
            "I can't access Bloomberg's web portal (portal.bloomberg.com) from the office network. The "
            "proxy categorizes it as 'uncategorized' and blocks it. This is a critical tool for our trading "
            "desk. Works fine on my phone's cellular data.",
        ),
        gold=ScenarioGold(
            category="Network & Connectivity",
            priority="P3",
            assigned_team="Network Operations",
            needs_escalation=False,
            missing_information=(
                "affected_system",
            ),
            next_best_action="Review the proxy URL categorization and add the business site to the allow list",
            remediation_steps=(
                "Check the proxy block log for the specific URL and categorization",
                "Verify the business justification for allowing the site",
                "Add the URL to the proxy allow list or recategorize it appropriately",
                "If security approval is needed, escalate the URL review to SecOps",
                "Confirm the user can access the site after the change",
            ),
        ),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 10. Remote desktop disconnecting frequently
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="network-010",
        subjects=(
            "Remote desktop keeps disconnecting",
            "RDP session drops every 10 minutes",
        ),
        descriptions=(
            "My remote desktop connection to the jump server (rdp-jump01.contoso.local) disconnects every "
            "10-15 minutes. I'm working from home on a stable 100 Mbps connection. The VPN stays connected "
            "— it's only the RDP session that drops.",
            "RDP sessions are extremely unstable today. I manage 5 servers and every single RDP session is "
            "dropping every few minutes. This is making server administration impossible. Other people on "
            "my team report the same issue.",
        ),
        gold=ScenarioGold(
            category="Network & Connectivity",
            priority="P3",
            assigned_team="Network Operations",
            needs_escalation=False,
            missing_information=(
                "network_location",
                "affected_system",
            ),
            next_best_action="Check network path stability and RDP server health for session keepalive issues",
            remediation_steps=(
                "Check the RDP server resource utilization (CPU, memory, sessions)",
                "Verify network path stability with continuous ping and traceroute",
                "Check if RDP session time limits or Group Policy settings changed",
                "Verify VPN split tunnel configuration isn't routing RDP traffic inefficiently",
                "If network path is the issue, investigate intermediate switch or router for packet drops",
            ),
        ),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 11. WiFi constantly asking to re-authenticate
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="network-011",
        subjects=(
            "WiFi keeps asking me to sign in again",
            "Corporate WiFi requires re-authentication every hour",
        ),
        descriptions=(
            "The corporate WiFi keeps dropping me and asking me to re-authenticate with my domain "
            "credentials every 45 minutes to an hour. This interrupts my work flow and disconnects all my "
            "active sessions. It never used to do this.",
            "Our office WiFi is requiring constant re-authentication. I get a popup to enter my credentials "
            "multiple times a day. My colleagues on the same floor have the same issue. It started after "
            "the network maintenance last weekend.",
        ),
        gold=ScenarioGold(
            category="Network & Connectivity",
            priority="P3",
            assigned_team="Network Operations",
            needs_escalation=False,
            missing_information=(
                "network_location",
                "affected_users",
            ),
            next_best_action="Check 802.1X RADIUS authentication session timeout settings on the wireless controller",
            remediation_steps=(
                "Review the RADIUS session timeout configuration on the wireless controller",
                "Check if the recent maintenance changed the 802.1X authentication settings",
                "Verify the RADIUS server is responding to re-authentication requests properly",
                "Increase the session timeout to a reasonable value if it was inadvertently lowered",
                "Test the fix by monitoring affected users' WiFi session stability",
            ),
        ),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 12. Latency spike during trading hours
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="network-012",
        subjects=(
            "CRITICAL: Network latency spike during market hours",
            "Trading platform lag — network latency unacceptable",
        ),
        descriptions=(
            "We're experiencing 200-500ms latency to our trading execution servers during market hours "
            "(9:30 AM - 4 PM). Normal is under 5ms. This is causing order execution delays that are costing "
            "real money. The trading floor network has been fine for months until today.",
            "URGENT — network latency on the trading floor has spiked to unacceptable levels. Traders are "
            "seeing 300ms+ round trips to the exchange gateways. At these speeds, our algorithmic trading "
            "strategies can't execute properly. Revenue impact is significant.",
        ),
        gold=ScenarioGold(
            category="Network & Connectivity",
            priority="P1",
            assigned_team="Network Operations",
            needs_escalation=True,
            missing_information=(),
            next_best_action=(
                "Investigate trading floor network path immediately — check for congestion, QoS misconfig, or "
                "hardware issues"
            ),
            remediation_steps=(
                "Check the trading floor network switch for errors or congestion",
                "Verify QoS prioritization for trading traffic is active",
                "Run traceroute from trading workstation to exchange gateway to identify latency source",
                "Check if any non-trading traffic is consuming bandwidth on the low-latency segment",
                "If switch issue, failover to redundant path and investigate the faulty equipment",
            ),
        ),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 13. Guest WiFi not working for visiting clients
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="network-013",
        subjects=(
            "Guest WiFi down — clients visiting today",
            "Visitor WiFi not working in conference center",
        ),
        descriptions=(
            "Our guest WiFi network isn't working. We have important clients from Goldman Sachs visiting "
            "for a full-day meeting and they can't connect to present their materials. The SSID "
            "'Contoso-Guest' shows up but connection times out. Please fix urgently.",
            "The guest wireless network in the executive conference center is broken. Visitors can see the "
            "network but can't connect. We have back-to-back investor meetings all day and our guests need "
            "internet access for presentations.",
        ),
        gold=ScenarioGold(
            category="Network & Connectivity",
            priority="P2",
            assigned_team="Network Operations",
            needs_escalation=False,
            missing_information=(),
            next_best_action="Check the guest WiFi captive portal and DHCP configuration in the conference center",
            remediation_steps=(
                "Verify the guest SSID is broadcasting and the captive portal is responding",
                "Check the guest VLAN DHCP pool for address exhaustion",
                "Restart the captive portal service if it's unresponsive",
                "Verify internet routing for the guest network VLAN",
                "Test guest connectivity from a personal device after the fix",
            ),
        ),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 14. Load balancer routing to wrong server
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="network-014",
        subjects=(
            "Load balancer sending traffic to decommissioned server",
            "Application routing to wrong backend",
        ),
        descriptions=(
            "Our F5 load balancer seems to be routing some traffic for app.contoso.com to a server that was "
            "decommissioned last week (10.20.30.50). Users are intermittently getting 502 errors. About 30% "
            "of requests fail.",
            "The load balancer pool for our customer portal still has an old server in it that's been shut "
            "down. Some requests are hitting the dead server and returning 502 Bad Gateway. We're getting "
            "customer complaints.",
        ),
        gold=ScenarioGold(
            category="Network & Connectivity",
            priority="P2",
            assigned_team="Network Operations",
            needs_escalation=False,
            missing_information=(),
            next_best_action="Remove the decommissioned server from the load balancer pool immediately",
            remediation_steps=(
                "Access the F5 load balancer admin interface",
                "Identify and remove the decommissioned server from the affected pool",
                "Verify the remaining pool members are healthy and accepting traffic",
                "Monitor the application for 502 errors after the change",
                "Review the decommissioning process to include load balancer cleanup",
            ),
        ),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 15. SSL/TLS certificate expired on internal portal
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="network-015",
        subjects=(
            "SSL certificate expired on internal portal",
            "Browser showing 'not secure' for HR portal",
        ),
        descriptions=(
            "The SSL certificate on our internal HR portal (hr.contoso.local) expired yesterday. Everyone "
            "gets a scary 'Your connection is not private' warning when they try to access it. Employees "
            "are afraid to proceed. We need a new cert installed.",
            "The TLS certificate for the internal benefits enrollment portal has expired. "
            "ERR_CERT_DATE_INVALID in Chrome. Benefits enrollment deadline is this Friday and 3,000+ "
            "employees need to access the portal.",
        ),
        gold=ScenarioGold(
            category="Network & Connectivity",
            priority="P2",
            assigned_team="Network Operations",
            needs_escalation=False,
            missing_information=(),
            next_best_action="Renew and install the SSL/TLS certificate on the internal portal immediately",
            remediation_steps=(
                "Identify the expired certificate details (issuer, CN, expiration date)",
                "Generate a new CSR and submit to the internal or external CA",
                "Install the renewed certificate on the web server",
                "Verify the full certificate chain is properly configured",
                "Set up certificate expiry monitoring alerts to prevent recurrence",
            ),
        ),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 16. Network segmentation blocking dev access
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="network-016",
        subjects=(
            "Can't reach staging servers from dev network",
            "Network segmentation blocking development work",
        ),
        descriptions=(
            "The dev team can't access the staging environment servers since the network segmentation "
            "project last week. We're on VLAN 100 (dev) and staging is on VLAN 200, but the firewall rules "
            "between them appear to be blocking our traffic. We need SSH (22) and HTTPS (443) access.",
            "After the network segmentation rollout, our developers can no longer reach the staging "
            "database (staging-db01, port 5432) from their workstations. We understand the need for "
            "segmentation but dev needs access to staging for testing.",
        ),
        gold=ScenarioGold(
            category="Network & Connectivity",
            priority="P3",
            assigned_team="Network Operations",
            needs_escalation=False,
            missing_information=(
                "configuration_details",
            ),
            next_best_action="Review inter-VLAN firewall rules and add appropriate access for dev-to-staging traffic",
            remediation_steps=(
                "Review the firewall rules between the dev and staging VLANs",
                "Identify the specific ports and protocols needed for dev access",
                "Create firewall rules allowing dev VLAN to staging VLAN on required ports",
                "Verify the rules with security team to maintain segmentation policy",
                "Test connectivity from dev workstations to staging after rule implementation",
            ),
        ),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 17. Office-to-office VPN tunnel down
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="network-017",
        subjects=(
            "Site-to-site VPN between NYC and London is down",
            "Inter-office VPN tunnel broken",
        ),
        descriptions=(
            "The site-to-site VPN tunnel between our NYC and London offices has been down since about 6 AM "
            "EST. London team can't access NYC file servers or internal applications. About 150 London "
            "employees are affected. We noticed IPsec phase 2 rekey failures in the logs.",
            "Our inter-office VPN connection between the main campus and the Chicago branch is down. "
            "Chicago branch (80 employees) has no access to central systems — email works because it's "
            "cloud, but all internal apps are unreachable.",
        ),
        gold=ScenarioGold(
            category="Network & Connectivity",
            priority="P1",
            assigned_team="Network Operations",
            needs_escalation=True,
            missing_information=(),
            next_best_action="Investigate site-to-site IPsec tunnel failure and restore inter-office connectivity",
            remediation_steps=(
                "Check IPsec tunnel status on both endpoint firewalls",
                "Review IKE/IPsec logs for phase 1 or phase 2 negotiation failures",
                "Verify the ISP links at both sites are operational",
                "Attempt to restart the VPN tunnel from both sides",
                "If tunnel fails to establish, check for pre-shared key mismatch or expired certificates",
            ),
        ),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 18. DHCP not assigning IP addresses
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="network-018",
        subjects=(
            "Devices not getting IP addresses on Floor 5",
            "DHCP scope exhausted or broken",
        ),
        descriptions=(
            "Devices on Floor 5 aren't getting IP addresses via DHCP. New connections get a 169.254.x.x "
            "APIPA address. Existing connected devices still work. It started about 2 hours ago. Affects "
            "both wired and wireless clients on this floor.",
            "We can't connect any new devices on the VLAN for Meeting Room wing. Laptops and phones are "
            "getting self-assigned IP addresses. Existing connections seem fine but if you disconnect and "
            "reconnect, you lose your IP.",
        ),
        gold=ScenarioGold(
            category="Network & Connectivity",
            priority="P2",
            assigned_team="Network Operations",
            needs_escalation=False,
            missing_information=(
                "network_location",
            ),
            next_best_action="Check the DHCP server scope for the affected subnet and verify DHCP relay configuration",
            remediation_steps=(
                "Check DHCP server health and scope utilization for the Floor 5 subnet",
                "Verify the DHCP scope hasn't exhausted its available addresses",
                "Check DHCP relay agent configuration on the Floor 5 switch",
                "If scope is full, expand the range or reduce lease duration",
                "Force lease cleanup for any stale/abandoned DHCP leases",
            ),
        ),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 19. Teams calls dropping for entire NYC office
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="network-019",
        subjects=(
            "URGENT: Teams calls dropping across NYC office",
            "Widespread Teams call quality issues — NYC",
        ),
        descriptions=(
            "Teams audio and video calls are dropping for practically everyone in the NYC office. Calls "
            "connect but drop within 2-5 minutes. Chat and file sharing work fine. This started at about 11 "
            "AM and is affecting all 300+ NYC employees. External calls with clients are being dropped "
            "mid-conversation.",
            "Massive Teams calling outage in the NYC office. Nobody can stay on a call for more than a few "
            "minutes. This is impacting client meetings, internal standups, everything. We've confirmed "
            "it's not a Microsoft service issue — it's on our end.",
        ),
        gold=ScenarioGold(
            category="Network & Connectivity",
            priority="P1",
            assigned_team="Network Operations",
            needs_escalation=True,
            missing_information=(),
            next_best_action="Investigate QoS and real-time media traffic path for the NYC office network immediately",
            remediation_steps=(
                "Check network utilization and QoS policies for real-time media traffic",
                "Verify the firewall is not throttling or inspecting Teams media traffic",
                "Check for any recent network changes that could affect UDP port ranges used by Teams",
                "Run a network quality test from an affected workstation",
                "If bandwidth saturation, implement traffic shaping or increase uplink capacity",
            ),
        ),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 20. Bandwidth throttling affecting cloud backup
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="network-020",
        subjects=(
            "Cloud backup failing — bandwidth throttled",
            "Azure backup timeouts due to bandwidth limits",
        ),
        descriptions=(
            "Our nightly Azure backup jobs are failing because they can't complete within the backup "
            "window. It looks like our internet bandwidth is being throttled to 50 Mbps during business "
            "hours and the backups are starting late. We need either more bandwidth or a policy exception "
            "for backup traffic.",
            "The backup to Azure Blob Storage is timing out every night. The transfer rate drops "
            "significantly during peak hours. Our backup window is 10 PM to 6 AM but the jobs are running "
            "into business hours and getting throttled.",
        ),
        gold=ScenarioGold(
            category="Network & Connectivity",
            priority="P3",
            assigned_team="Network Operations",
            needs_escalation=False,
            missing_information=(
                "configuration_details",
            ),
            next_best_action="Review bandwidth QoS policies and ensure backup traffic is not throttled during the backup window",
            remediation_steps=(
                "Review the QoS/bandwidth policy for Azure backup traffic",
                "Check if the throttling is per-user or per-application",
                "Configure QoS to allow full bandwidth for backup during off-hours window",
                "If possible, tag backup traffic with a different DSCP marking",
                "Monitor next backup cycle to confirm completion within the window",
            ),
        ),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 21. New office network infrastructure setup
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="network-021",
        subjects=(
            "New office network setup request — expansion to Floor 8",
            "Network infrastructure needed for new office space",
        ),
        descriptions=(
            "We're expanding to Floor 8 of Building A next month and need the full network infrastructure "
            "set up. Requirements: 60 wired drops, 6 wireless APs, 2 conference room setups, and "
            "connectivity to the core network. Target completion: April 15.",
            "Requesting network infrastructure build-out for our newly leased office space at 200 Park "
            "Avenue, Suite 1200. Need wired and wireless networking, VPN connectivity back to the main "
            "campus, and a small server closet. 25 employees initially.",
        ),
        gold=ScenarioGold(
            category="Network & Connectivity",
            priority="P4",
            assigned_team="Network Operations",
            needs_escalation=False,
            missing_information=(),
            next_best_action="Schedule a site survey and create a network infrastructure deployment plan",
            remediation_steps=(
                "Conduct a site survey to assess cabling, power, and AP placement needs",
                "Design the network topology including VLAN assignments and IP addressing",
                "Order networking equipment (switches, APs, cabling, patch panels)",
                "Schedule the installation during a weekend to minimize disruption",
                "Test and validate all network connectivity before the office opens",
            ),
        ),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 22. Wireless AP down on trading floor
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="network-022",
        subjects=(
            "WiFi access point down on trading floor",
            "No wireless coverage at trading desk cluster 3",
        ),
        descriptions=(
            "The wireless access point near trading desk cluster 3 (Floor 7, southeast corner) appears to "
            "be dead. No power light, no signal. Traders in that area can't use their wireless devices. The "
            "AP on the ceiling looks like it might have been bumped — it's hanging at an angle.",
            "One of the WiFi APs on the trading floor stopped working. It's the one between desk rows C and "
            "D. About 15 traders have no wireless coverage. They're using wired connections as workaround "
            "but their wireless devices (phones, tablets) are affected.",
        ),
        gold=ScenarioGold(
            category="Network & Connectivity",
            priority="P3",
            assigned_team="Network Operations",
            needs_escalation=False,
            missing_information=(
                "network_location",
            ),
            next_best_action="Inspect the physical AP installation and check PoE power delivery to the access point",
            remediation_steps=(
                "Check the AP status in the wireless controller",
                "Physically inspect the AP for damage or loose cabling",
                "Verify PoE power is being delivered on the switch port",
                "If AP is damaged, replace with a spare and reconfigure",
                "Verify wireless coverage is restored in the affected area",
            ),
        ),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 23. IPv6 compatibility issue with legacy app
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="network-023",
        subjects=(
            "Legacy app broken after IPv6 rollout",
            "IPv6 causing issues with older application",
        ),
        descriptions=(
            "Since the IPv6 dual-stack deployment last week, our legacy compliance reporting application "
            "crashes when it tries to connect to the database. The app only supports IPv4 and is getting "
            "confused by the IPv6 addresses being returned by DNS. We can't update the app immediately — "
            "vendor EOL.",
            "Our 15-year-old internal invoicing system stopped working after IPv6 was enabled on our "
            "network. The application can't parse the new address format. The vendor is out of business so "
            "there's no update available.",
        ),
        gold=ScenarioGold(
            category="Network & Connectivity",
            priority="P3",
            assigned_team="Network Operations",
            needs_escalation=False,
            missing_information=(
                "affected_system",
                "configuration_details",
            ),
            next_best_action="Configure DNS to return only IPv4 records for the legacy application's queries",
            remediation_steps=(
                "Configure the legacy app's DNS entries to return A records only (no AAAA)",
                "Alternatively, configure a local hosts file entry with IPv4 address",
                "Check if the application server can have IPv6 disabled on its network adapter",
                "Document the IPv6 incompatibility for the legacy app modernization backlog",
                "Monitor the application connectivity after the DNS change",
            ),
        ),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 24. CDN caching stale content
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="network-024",
        subjects=(
            "Website showing outdated content — CDN cache issue",
            "Customer portal serving stale pages",
        ),
        descriptions=(
            "Our customer-facing portal at www.contoso.com is serving outdated content. We deployed a "
            "critical update 6 hours ago but customers are still seeing the old version. The origin server "
            "has the correct content but the CDN is caching the old pages.",
            "The Azure CDN is not picking up our latest deployment. We pushed a security hotfix to the "
            "customer portal but customers in Europe and Asia are still seeing the vulnerable version. "
            "We've tried purging but it's not propagating.",
        ),
        gold=ScenarioGold(
            category="Network & Connectivity",
            priority="P2",
            assigned_team="Network Operations",
            needs_escalation=False,
            missing_information=(),
            next_best_action="Force purge the CDN cache and verify cache-control headers on the origin server",
            remediation_steps=(
                "Initiate a full CDN cache purge for the affected paths",
                "Verify cache-control and max-age headers on the origin server responses",
                "Check CDN edge nodes in different regions for content freshness",
                "If purge doesn't propagate, escalate to CDN provider support",
                "Update cache-control headers to prevent extended caching of dynamic content",
            ),
        ),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 25. Network printer not reachable from VLAN 10
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="network-025",
        subjects=(
            "Printer unreachable from my network segment",
            "Can't print from VLAN 10 to Floor 2 printer",
        ),
        descriptions=(
            "I can't reach the Floor 2 network printer (10.20.2.100) from my workstation on VLAN 10. I can "
            "ping everything else on other VLANs. Other people on VLAN 20 can print to it fine. Seems like "
            "a routing or firewall issue between VLANs.",
            "After the network segmentation project, we lost access to shared printers from the dev VLAN. "
            "The printer is on the office VLAN and there's no inter-VLAN routing rule for print traffic "
            "(port 9100, 631). Affects all 20 developers.",
        ),
        gold=ScenarioGold(
            category="Network & Connectivity",
            priority="P3",
            assigned_team="Network Operations",
            needs_escalation=False,
            missing_information=(
                "network_location",
            ),
            next_best_action="Add inter-VLAN routing rules to allow print traffic from VLAN 10 to the printer VLAN",
            remediation_steps=(
                "Verify the inter-VLAN firewall rules for print traffic",
                "Add firewall rules allowing traffic from VLAN 10 to printer VLAN on ports 9100 and 631",
                "Verify the printer is responding on the expected IP and ports",
                "Test printing from a VLAN 10 workstation after the rule change",
                "Document the new rule and add it to the network segmentation documentation",
            ),
        ),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 26. Split tunneling VPN request
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="network-026",
        subjects=(
            "Request to enable split tunnel VPN for better performance",
            "VPN split tunneling configuration request",
        ),
        descriptions=(
            "Can we enable split tunneling on our VPN? Currently all traffic goes through the VPN tunnel "
            "which makes personal browsing and streaming services extremely slow. I understand corporate "
            "traffic needs to go through VPN but personal traffic should be direct.",
            "Requesting split tunnel VPN configuration for the development team. We need to access cloud "
            "services (AWS, GitHub) directly without routing through the corporate VPN. The round-trip "
            "through NYC VPN gateway adds 100ms+ to our API calls to US-West AWS.",
        ),
        gold=ScenarioGold(
            category="Network & Connectivity",
            priority="P4",
            assigned_team="Network Operations",
            needs_escalation=False,
            missing_information=(),
            next_best_action="Evaluate the split tunnel VPN request against security policy and submit for SecOps approval",
            remediation_steps=(
                "Review the current VPN tunnel configuration and routing table",
                "Evaluate the security implications of split tunneling",
                "Submit split tunnel request to SecOps for security review",
                "If approved, configure split tunnel with appropriate routing for corporate traffic",
                "Test that corporate resources remain accessible while split tunneling is active",
            ),
        ),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 27. MTU size causing packet fragmentation
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="network-027",
        subjects=(
            "Large file transfers failing — MTU issue suspected",
            "Packet fragmentation causing slow transfers",
        ),
        descriptions=(
            "Large file transfers to our partner over the site-to-site VPN keep failing at exactly the same "
            "point. Small files work fine. I suspect an MTU mismatch — our VPN tunnel might have a lower "
            "MTU than the 1500-byte default and packets are being silently dropped.",
            "We're seeing mysterious failures when transferring files larger than about 1400 bytes over the "
            "VPN. ping -f -l 1472 works but ping -f -l 1473 fails with 'packet needs to be fragmented.' The "
            "VPN tunnel MTU needs adjustment.",
        ),
        gold=ScenarioGold(
            category="Network & Connectivity",
            priority="P3",
            assigned_team="Network Operations",
            needs_escalation=False,
            missing_information=(
                "configuration_details",
            ),
            next_best_action="Adjust the VPN tunnel MTU and enable MSS clamping to prevent fragmentation",
            remediation_steps=(
                "Run MTU path discovery tests to find the maximum working MTU",
                "Adjust the VPN tunnel MTU setting to account for encapsulation overhead",
                "Enable TCP MSS clamping on the VPN gateway",
                "Verify large file transfers complete successfully after the change",
                "Document the MTU settings for future reference",
            ),
        ),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 28. MAC address filtering blocking new device
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="network-028",
        subjects=(
            "New laptop can't connect to secure network — MAC filter",
            "Device blocked by MAC address whitelist",
        ),
        descriptions=(
            "My brand new laptop can't connect to the secure trading floor network. It connects fine to the "
            "general office WiFi. I think the trading floor network has MAC address filtering and my new "
            "laptop's MAC address isn't registered yet.",
            "I was issued a replacement laptop but it can't access the restricted lab network. The old "
            "laptop worked fine. I believe there's a MAC address whitelist on that network segment. Please "
            "add my new device: MAC address is A4:CF:12:34:56:78.",
        ),
        gold=ScenarioGold(
            category="Network & Connectivity",
            priority="P3",
            assigned_team="Network Operations",
            needs_escalation=False,
            missing_information=(
                "device_info",
            ),
            next_best_action="Register the new device's MAC address in the network access control whitelist",
            remediation_steps=(
                "Verify the MAC address of the new device",
                "Add the MAC address to the network access control whitelist for the restricted network",
                "Remove the old device's MAC address from the whitelist",
                "Test connectivity from the new device to the restricted network",
                "Confirm full access to required resources on the restricted segment",
            ),
        ),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 29. Site-to-site connectivity degraded after ISP change
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="network-029",
        subjects=(
            "Inter-office connectivity degraded since ISP migration",
            "Network performance poor after ISP switch",
        ),
        descriptions=(
            "Since we switched ISPs in the Chicago office last Friday, connectivity between Chicago and NYC "
            "has been noticeably degraded. Latency went from 15ms to 45ms and we're seeing periodic packet "
            "loss. This affects VoIP quality and application responsiveness for the Chicago team.",
            "After migrating the London office to a new ISP circuit, we're experiencing intermittent "
            "connectivity issues. The BGP session to the new provider keeps flapping. Sometimes routes are "
            "lost for 30-60 seconds at a time.",
        ),
        gold=ScenarioGold(
            category="Network & Connectivity",
            priority="P2",
            assigned_team="Network Operations",
            needs_escalation=False,
            missing_information=(
                "configuration_details",
            ),
            next_best_action="Investigate the new ISP circuit quality and BGP routing configuration",
            remediation_steps=(
                "Run continuous monitoring (ping, traceroute, MTR) to the affected office",
                "Check BGP session stability and route advertisements from the new ISP",
                "Contact the ISP to report the performance degradation and request circuit testing",
                "Compare routing paths before and after the ISP change",
                "If the new ISP can't resolve the issues, consider reverting to the previous provider",
            ),
        ),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 30. DDoS-like traffic pattern on edge router
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="network-030",
        subjects=(
            "Suspicious high-volume traffic on edge router",
            "Possible DDoS attack — edge bandwidth saturated",
        ),
        descriptions=(
            "Our edge router is showing 98% bandwidth utilization with unusual traffic patterns — massive "
            "inbound UDP traffic from hundreds of source IPs to our external address range. This is "
            "impacting all internet-facing services. Looks like a volumetric DDoS attack.",
            "ALERT: Edge firewall is logging millions of inbound connection attempts per minute from "
            "distributed sources. Our internet bandwidth is completely saturated. Customer-facing services "
            "are unreachable. This appears to be a coordinated DDoS attack.",
        ),
        gold=ScenarioGold(
            category="Network & Connectivity",
            priority="P1",
            assigned_team="Network Operations",
            needs_escalation=True,
            missing_information=(),
            next_best_action="Activate DDoS mitigation — engage ISP scrubbing services and notify SecOps immediately",
            remediation_steps=(
                "Contact the ISP to activate upstream DDoS scrubbing/blackhole routing",
                "Enable rate limiting on the edge firewall for the attack traffic profile",
                "Notify Security Operations for incident tracking and coordination",
                "Identify the targeted services and consider temporary IP changes if needed",
                "Monitor bandwidth utilization and service availability after mitigation is active",
            ),
        ),
    ),
]
