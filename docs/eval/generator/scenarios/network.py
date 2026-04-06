"""Network & Connectivity scenario definitions."""

from generator.models import Scenario

SCENARIOS: list[Scenario] = [
    # ------------------------------------------------------------------
    # 1. VPN connection drops when switching networks
    # ------------------------------------------------------------------
    Scenario(
        scenario_id="net-vpn-drops-on-network-switch",
        category="Network & Connectivity",
        priority="P3",
        assigned_team="Network Operations",
        needs_escalation=False,
        missing_information=["device_info", "network_location"],
        subjects=[
            "VPN keeps disconnecting when I switch from WiFi to hotspot",
            "VPN drops every time I change networks",
            "GlobalProtect VPN disconnects on network transition",
            "Losing VPN connection when moving between WiFi networks",
        ],
        descriptions=[
            "Every time I move from my home WiFi to my phone hotspot the VPN "
            "drops and I have to manually reconnect. This happens multiple "
            "times a day when I'm traveling between meetings. I'm on a "
            "Windows 11 laptop using GlobalProtect. It was working fine "
            "until the last client update about two weeks ago.",
            "I work from home and from coffee shops regularly. Whenever my "
            "laptop switches networks — even between 2.4 GHz and 5 GHz on "
            "the same router — the VPN connection dies. I have to close "
            "GlobalProtect and relaunch it to get back on. It's been "
            "happening since last Friday.",
            "My VPN connection is extremely fragile. If there's any kind of "
            "network change at all, the tunnel goes down and I lose access "
            "to internal resources for 2-3 minutes while it reconnects. "
            "I'm currently in the Denver office and it even happens when "
            "roaming between access points on different floors.",
        ],
        next_best_actions=[
            "Collect VPN client logs from the user's device and check the "
            "GlobalProtect client version for known reconnection bugs; "
            "verify keep-alive and roaming settings on the VPN gateway.",
            "Review the VPN gateway configuration for session persistence "
            "and IKE re-keying timers; compare against the recent client "
            "update changelog to identify regressions.",
        ],
        remediation_steps=[
            [
                "Collect VPN client diagnostic logs from the affected device",
                "Verify GlobalProtect client version and compare against "
                "the latest stable release notes for known issues",
                "Check VPN gateway session persistence and IKE re-key settings to ensure seamless roaming is enabled",
                "Test with a clean VPN profile to rule out corrupted local configuration",
                "If issue persists, roll back the GlobalProtect client to the previous stable version and retest",
                "Follow up with the user to confirm stable connectivity after changes",
            ],
        ],
    ),
    # ------------------------------------------------------------------
    # 2. WiFi slow in specific building/floor
    # ------------------------------------------------------------------
    Scenario(
        scenario_id="net-wifi-slow-building-floor",
        category="Network & Connectivity",
        priority="P3",
        assigned_team="Network Operations",
        needs_escalation=False,
        missing_information=["network_location", "affected_users"],
        subjects=[
            "WiFi is painfully slow on 3rd floor of NYC office",
            "Extremely slow wireless on Floor 3 — NYC",
            "Internet crawling on the third floor, NYC building",
            "WiFi barely working on NYC 3F since Monday",
        ],
        descriptions=[
            "The WiFi on the 3rd floor of our NYC office has been "
            "extremely slow all week. Downloads that normally take seconds "
            "are taking minutes, and video calls keep freezing. It seems "
            "to affect everyone on this floor. The 2nd and 4th floors "
            "are fine.",
            "Multiple people on Floor 3 in the New York office are "
            "complaining about WiFi performance. We've been running speed "
            "tests and getting 2-5 Mbps down, whereas on Floor 2 we get "
            "150+ Mbps. It's been like this since the start of the week "
            "and it's really impacting our ability to work.",
            "I'm on the 3rd floor in NYC and the wireless network is "
            "basically unusable during business hours. Pages take forever "
            "to load, file uploads to SharePoint time out, and Teams "
            "meetings drop constantly. A few of us have resorted to "
            "using our phone hotspots.",
        ],
        next_best_actions=[
            "Check the wireless controller dashboard for AP utilization, "
            "channel interference, and client density on Floor 3 APs; "
            "correlate with any recent network changes or new equipment "
            "on that floor.",
            "Run a wireless site survey on Floor 3 to identify dead zones "
            "and co-channel interference; review AP firmware versions and "
            "check for any failed or degraded access points.",
        ],
        remediation_steps=[
            [
                "Review wireless controller for Floor 3 AP health, client count, and channel utilization",
                "Identify any APs in degraded or offline state and restart or replace as needed",
                "Check for co-channel interference from neighboring floors or rogue access points",
                "Adjust channel assignments and transmit power based on site survey data",
                "Verify upstream switch port health and PoE power budget for Floor 3 APs",
                "Monitor for 24 hours and confirm with affected users that performance has improved",
            ],
        ],
    ),
    # ------------------------------------------------------------------
    # 3. DNS resolution failure for internal hostnames
    # ------------------------------------------------------------------
    Scenario(
        scenario_id="net-dns-resolution-internal",
        category="Network & Connectivity",
        priority="P2",
        assigned_team="Network Operations",
        needs_escalation=True,
        missing_information=["error_message", "affected_system"],
        subjects=[
            "Can't resolve internal hostnames — DNS seems broken",
            "Internal sites not loading, DNS resolution failed",
            "DNS not working for *.contoso.internal addresses",
        ],
        descriptions=[
            "Since about 9 AM today, I can't reach any internal "
            "applications by hostname. I get 'DNS name does not exist' "
            "errors in the browser for everything under "
            "contoso.internal. External sites like Google work fine. "
            "I've tried flushing my DNS cache and restarting but no luck. "
            "Multiple colleagues are having the same issue.",
            "None of the internal URLs are resolving. I keep getting "
            "'server not found' for our intranet, the HR portal, and "
            "the internal wiki. nslookup for intranet.contoso.internal "
            "comes back with NXDOMAIN. It looks like a DNS server issue "
            "because pinging by IP still works.",
            "Starting this morning, all internal DNS lookups fail. I ran "
            "nslookup and it's pointing to 10.1.0.5 as the DNS server "
            "but that server isn't responding to queries for our internal "
            "zone. External resolution works because it falls through to "
            "the public resolvers. This is affecting at least our entire "
            "floor, maybe more.",
        ],
        next_best_actions=[
            "Check the health of the internal DNS servers (10.1.0.x) and "
            "verify the contoso.internal forward lookup zone is loading "
            "correctly; check DNS server event logs for zone transfer or "
            "service errors.",
            "Verify internal DNS server availability and zone health; "
            "check whether a recent change to DNS records, conditional "
            "forwarders, or group policy affected name resolution.",
        ],
        remediation_steps=[
            [
                "Check internal DNS server health and service status on all DNS servers in the affected site",
                "Verify the contoso.internal zone is loaded and contains the expected records",
                "Review DNS server event logs for errors related to zone "
                "loading, replication, or forwarder configuration",
                "Restart the DNS Server service if the zone is stale or unresponsive",
                "Flush DNS caches on the server and verify resolution from a test client",
                "Confirm resolution is working for affected users and monitor for recurrence",
            ],
        ],
    ),
    # ------------------------------------------------------------------
    # 4. Firewall rule change request
    # ------------------------------------------------------------------
    Scenario(
        scenario_id="net-firewall-rule-change",
        category="Network & Connectivity",
        priority="P4",
        assigned_team="Network Operations",
        needs_escalation=False,
        missing_information=[
            "configuration_details",
            "business_impact",
        ],
        subjects=[
            "Firewall rule change request for new vendor integration",
            "Need port opened on firewall for third-party API",
            "Request: allow outbound traffic to vendor endpoint",
            "Firewall change needed — new SaaS integration",
        ],
        descriptions=[
            "We're onboarding a new payment processing vendor and need "
            "outbound HTTPS (443) and SFTP (22) access from our app "
            "servers in the 10.4.0.0/24 subnet to their endpoint at "
            "api.vendor-payments.example.com. The project go-live is in "
            "three weeks. I've attached the vendor's network requirements "
            "document.",
            "Our development team needs a firewall rule change to allow "
            "outbound traffic on port 443 from the staging environment "
            "(10.5.10.0/24) to a new SaaS analytics provider. The IPs "
            "are listed in the attached spreadsheet. This is for a Q3 "
            "project and we need it in the next sprint.",
            "Requesting a firewall change for a new integration. We need "
            "to allow traffic from our production web tier "
            "(10.4.1.0/24) to a third-party fraud detection API on "
            "ports 443 and 8443. The vendor IP ranges are "
            "203.0.113.0/24 and 198.51.100.0/24. Please see the "
            "attached change request form.",
        ],
        next_best_actions=[
            "Review the requested firewall rule against the network "
            "security policy; validate source/destination/port details "
            "and obtain security team approval before implementing.",
            "Verify the vendor IP ranges and ports, schedule the change "
            "during the next maintenance window, and ensure a rollback "
            "plan is documented.",
        ],
        remediation_steps=[
            [
                "Validate the requested source, destination, and port details against the network security policy",
                "Obtain approval from Security Operations for the proposed rule change",
                "Implement the rule in a test or staging firewall first and verify connectivity",
                "Schedule the production change during the maintenance window and apply the rule",
                "Test end-to-end connectivity from the source subnet to the vendor endpoint",
                "Document the rule in the firewall change log and close the request",
            ],
        ],
    ),
    # ------------------------------------------------------------------
    # 5. Guest WiFi setup for corporate event
    # ------------------------------------------------------------------
    Scenario(
        scenario_id="net-guest-wifi-event",
        category="Network & Connectivity",
        priority="P4",
        assigned_team="Network Operations",
        needs_escalation=False,
        missing_information=[
            "network_location",
            "business_impact",
            "configuration_details",
        ],
        subjects=[
            "Need guest WiFi for investor event next Thursday",
            "Guest wireless setup request for conference center",
            "Set up temporary WiFi for corporate event — NYC",
        ],
        descriptions=[
            "We're hosting an investor day in the NYC conference center "
            "next Thursday (about 120 attendees). We need a dedicated "
            "guest WiFi SSID with internet-only access — no corporate "
            "network. It should be available from 7 AM to 7 PM and "
            "support at least 150 concurrent devices. The event team "
            "will need the SSID name and password by Tuesday.",
            "Our marketing team is organizing a client event in the "
            "London office's 4th-floor event space on the 15th. We "
            "need guest WiFi for about 80 attendees. The network "
            "should be isolated from our corporate LAN and only provide "
            "internet access. Can we also get a custom SSID name like "
            "'Contoso-Guest-Event'?",
            "Requesting guest WiFi provisioning for a two-day leadership "
            "summit in the Denver office's main auditorium. Expected "
            "attendance is 200 people. We need reliable internet for "
            "presentations and live demos, completely separate from the "
            "internal network. Please advise on bandwidth capacity.",
        ],
        next_best_actions=[
            "Confirm event date, location, and expected device count; "
            "provision a time-limited guest SSID on an isolated VLAN "
            "with appropriate bandwidth QoS settings.",
            "Coordinate with facilities to confirm AP coverage in the "
            "event space; create a guest SSID with captive portal, "
            "internet-only ACLs, and bandwidth throttling per client.",
        ],
        remediation_steps=[
            [
                "Confirm event details: date, time, venue, expected attendee count, and bandwidth requirements",
                "Provision a dedicated guest VLAN isolated from the corporate network with internet-only access",
                "Create a time-limited SSID with WPA3 or captive portal authentication",
                "Configure per-client and aggregate bandwidth limits to ensure fair usage",
                "Test connectivity from the event space and verify corporate network isolation",
                "Provide SSID credentials to the event organizer and decommission the SSID after the event",
            ],
        ],
    ),
    # ------------------------------------------------------------------
    # 6. Proxy blocking legitimate website
    # ------------------------------------------------------------------
    Scenario(
        scenario_id="net-proxy-blocking-legit-site",
        category="Network & Connectivity",
        priority="P3",
        assigned_team="Network Operations",
        needs_escalation=False,
        missing_information=["affected_system", "screenshot_or_attachment"],
        subjects=[
            "Proxy is blocking a site I need for work",
            "Web proxy blocking legitimate vendor portal",
            "Can't access vendor site — blocked by Zscaler",
            "Website blocked by corporate proxy, need exception",
        ],
        descriptions=[
            "I'm trying to access our vendor's documentation portal at "
            "docs.vendor-platform.example.com and the corporate proxy is "
            "blocking it as 'Uncategorized'. I need this site for my "
            "daily work — it has the API docs for the integration I'm "
            "building. I've verified the URL is correct and it works "
            "fine from my phone on mobile data.",
            "Zscaler is blocking access to a legitimate SaaS tool our "
            "team just started using — app.designtool.example.com. The "
            "block page says 'Access Denied: Category not permitted'. "
            "My manager has approved the use of this tool. Can we get "
            "it whitelisted? It's affecting about 12 people on the "
            "design team.",
            "I keep getting a 'This site has been blocked by your "
            "organization' page when trying to reach a financial data "
            "provider at data.market-feeds.example.com. I need this for "
            "the trading desk and it's been blocked since the proxy "
            "policy update last weekend. It was accessible before.",
        ],
        next_best_actions=[
            "Look up the blocked URL in the proxy admin console to "
            "determine the block reason and category; if legitimate, "
            "submit a recategorization request and add a temporary "
            "allow-list entry.",
            "Verify the site's reputation and business justification; "
            "add a URL exception in the proxy policy for the affected "
            "user group after obtaining manager approval.",
        ],
        remediation_steps=[
            [
                "Identify the block reason and URL category in the proxy admin console (Zscaler/Bluecoat)",
                "Verify the site's business justification and obtain manager approval if not already provided",
                "Submit a URL recategorization request to the proxy vendor if miscategorized",
                "Add a temporary allow-list entry for the URL or domain in the proxy policy",
                "Confirm the user can access the site and document the exception in the proxy change log",
            ],
        ],
    ),
    # ------------------------------------------------------------------
    # 7. Network drive not mapping on login
    # ------------------------------------------------------------------
    Scenario(
        scenario_id="net-drive-not-mapping",
        category="Network & Connectivity",
        priority="P3",
        assigned_team="Network Operations",
        needs_escalation=False,
        missing_information=["error_message", "device_info"],
        subjects=[
            "Network drive H: not mapping when I log in",
            "Mapped drive disappears after reboot",
            "Can't access shared drive — drive letter missing",
            "Network drive not connecting on startup",
        ],
        descriptions=[
            "My H: drive used to map automatically when I logged in but "
            "it stopped working about a week ago. If I manually map it "
            "using \\\\filesrv01\\finance it works, but it doesn't persist "
            "after a reboot. I'm on a domain-joined Windows 11 laptop "
            "and I've tried logging off and back on several times.",
            "Since the last group policy update, my network drives aren't "
            "mapping at login. I used to have H: for my home folder and "
            "S: for the shared department drive. Both are missing now. "
            "Other people on my team still have theirs. I'm in the "
            "Finance department, NYC office.",
            "I rebooted my laptop this morning and my mapped drives are "
            "gone. I see a red X on the drive icons and when I click "
            "them I get 'The network path was not found'. I'm connected "
            "to the VPN from home. This has been happening intermittently "
            "for the last two weeks.",
        ],
        next_best_actions=[
            "Check the user's group policy results (gpresult) for drive "
            "mapping policies and verify the file server is accessible "
            "from the user's network segment.",
            "Run gpresult /r on the user's machine to confirm drive "
            "mapping GPO is applying correctly; check file server "
            "availability and DNS resolution for the server hostname.",
        ],
        remediation_steps=[
            [
                "Run gpresult /r on the user's workstation to verify drive mapping GPO is applying",
                "Check the file server availability and confirm the shared folder path is correct",
                "Verify DNS resolution for the file server hostname from the user's machine",
                "Check the user's AD group membership to confirm they are in the correct security group for the GPO",
                "If the GPO is not applying, force a group policy update with gpupdate /force and retest",
                "Confirm drives map correctly at next login and monitor for recurrence",
            ],
        ],
    ),
    # ------------------------------------------------------------------
    # 8. Site-to-site VPN down between offices (P1)
    # ------------------------------------------------------------------
    Scenario(
        scenario_id="net-site-to-site-vpn-down",
        category="Network & Connectivity",
        priority="P1",
        assigned_team="Network Operations",
        needs_escalation=True,
        missing_information=["timestamp", "business_impact"],
        subjects=[
            "URGENT: Site-to-site VPN between NYC and London is down",
            "NYC-London VPN tunnel down — no connectivity to London",
            "Critical: inter-office VPN outage NYC ↔ London",
        ],
        descriptions=[
            "The site-to-site VPN tunnel between the NYC and London "
            "offices went down approximately 30 minutes ago. No one in "
            "NYC can reach any London-hosted resources including the "
            "London file servers, the EU trading platform, and the "
            "London print servers. This is impacting the entire NYC "
            "trading floor and operations team — approximately 300 "
            "users are affected. London users report they also cannot "
            "reach NYC resources.",
            "We've lost connectivity between the New York and London "
            "data centers. The IPSec tunnel appears to be down — our "
            "monitoring shows the tunnel has been in a 'disconnected' "
            "state since 14:22 UTC. All cross-site traffic is failing. "
            "This is blocking trading operations and the London team "
            "cannot access the primary ERP system hosted in NYC.",
            "Alert from our network monitoring: the NYC-to-London "
            "site-to-site VPN has been unreachable for 45 minutes. "
            "Multiple teams have reported they cannot access "
            "London-based services. The London NOC confirms their "
            "side of the tunnel is also showing as down. Immediate "
            "restoration is needed — this is directly impacting revenue-"
            "generating activities.",
        ],
        next_best_actions=[
            "Immediately check the VPN concentrators on both sides "
            "(NYC and London) for tunnel status, IKE phase 1/2 errors, "
            "and recent configuration changes; engage the London NOC "
            "for coordinated troubleshooting.",
            "Verify WAN circuit health on both ends, check for ISP "
            "issues, and review firewall/VPN device logs for the tunnel "
            "tear-down event; initiate a bridge call with London "
            "network team.",
        ],
        remediation_steps=[
            [
                "Verify WAN circuit status on both NYC and London sides and contact ISP if circuit is down",
                "Check VPN concentrator/firewall status and IKE phase 1 and phase 2 SA states on both endpoints",
                "Review logs for the tunnel tear-down event and identify "
                "root cause (certificate expiry, config change, hardware "
                "failure)",
                "Attempt to re-establish the tunnel manually by clearing and re-initiating the IKE SAs",
                "If the primary tunnel cannot be restored, activate the backup VPN path or failover circuit",
                "Confirm cross-site connectivity is restored and all critical services are accessible",
                "Conduct a post-incident review and document root cause and preventive measures",
            ],
        ],
    ),
    # ------------------------------------------------------------------
    # 9. Load balancer health check failing (P1)
    # ------------------------------------------------------------------
    Scenario(
        scenario_id="net-lb-health-check-failing",
        category="Network & Connectivity",
        priority="P1",
        assigned_team="Network Operations",
        needs_escalation=True,
        missing_information=["error_message", "affected_system"],
        subjects=[
            "CRITICAL: Load balancer health checks failing — app down",
            "Production load balancer marking all backends unhealthy",
            "LB health check failure — customer-facing app impacted",
        ],
        descriptions=[
            "Our production F5 load balancer is marking all backend "
            "servers for the customer-facing web application as "
            "unhealthy. Users are getting 503 errors when trying to "
            "access the portal. The health check monitor is configured "
            "to hit /healthz on port 443 and all four pool members are "
            "showing as down. This started about 15 minutes ago and is "
            "affecting all external customers.",
            "We're seeing health check failures on the production load "
            "balancer for the API gateway pool. All six backend nodes "
            "have been marked offline even though the servers themselves "
            "are up and responding locally. The LB monitor is timing "
            "out on the health endpoint. Customer-facing API traffic is "
            "returning 502 Bad Gateway. Roughly 2,000 API consumers "
            "are impacted.",
            "Alert triggered: production load balancer pool "
            "'web-frontend-prod' has zero healthy members. All eight "
            "nodes failed health checks simultaneously five minutes "
            "ago. The servers are reachable via direct SSH and the "
            "application responds to local curl requests on the health "
            "endpoint. Suspect a network or LB configuration issue "
            "rather than application failure.",
        ],
        next_best_actions=[
            "Check the load balancer health monitor configuration and "
            "compare against the backend server's health endpoint "
            "behavior; verify network connectivity between the LB and "
            "backend servers on the health check port.",
            "Investigate whether a recent certificate rotation, firewall "
            "change, or network ACL update is blocking the health check "
            "traffic; test connectivity from the LB's self-IP to the "
            "backend health endpoint.",
        ],
        remediation_steps=[
            [
                "Verify the load balancer health monitor configuration (URL path, port, expected response code)",
                "Test connectivity from the LB self-IP to the backend health check endpoints using tcpdump or curl",
                "Check for recent certificate changes, firewall rule "
                "modifications, or ACL updates that could block health "
                "check traffic",
                "If a configuration change caused the issue, roll back and re-test health checks",
                "Manually force one backend member into the pool to restore partial service while troubleshooting",
                "Confirm all pool members pass health checks and customer-facing traffic is restored",
                "Document root cause and update change management procedures to prevent recurrence",
            ],
        ],
    ),
    # ------------------------------------------------------------------
    # 10. DHCP address exhaustion in a subnet
    # ------------------------------------------------------------------
    Scenario(
        scenario_id="net-dhcp-exhaustion",
        category="Network & Connectivity",
        priority="P3",
        assigned_team="Network Operations",
        needs_escalation=False,
        missing_information=["network_location", "affected_users"],
        subjects=[
            "Devices can't get IP addresses on Floor 5 — DHCP issue?",
            "DHCP pool exhausted on 10.3.5.0/24 subnet",
            "No IP address assigned — 'limited connectivity' errors",
        ],
        descriptions=[
            "Multiple users on Floor 5 of the NYC office are reporting "
            "that their laptops connect to WiFi but show 'No Internet' "
            "or 'Limited Connectivity'. They're getting APIPA addresses "
            "(169.254.x.x) instead of valid IPs. It started this "
            "morning and affects both wired and wireless connections "
            "on this floor. About 40 people are impacted.",
            "Our monitoring shows the DHCP scope for 10.3.5.0/24 is at "
            "98% utilization. New devices trying to join the network on "
            "Floor 5 are failing to obtain leases. The scope only has "
            "two available addresses left. We added 50 new contractor "
            "workstations to this floor last week and didn't expand "
            "the pool.",
            "Getting reports from the Singapore office that people "
            "joining the network this morning aren't getting IP "
            "addresses. DHCP server logs show 'no available addresses "
            "in scope 10.8.2.0/24'. The scope was sized for 100 "
            "devices but we now have over 120 endpoints on that subnet "
            "between desktops, laptops, and IP phones.",
        ],
        next_best_actions=[
            "Check the DHCP server scope utilization and lease table "
            "for the affected subnet; identify stale leases or rogue "
            "devices consuming addresses and consider expanding the "
            "scope or reducing lease duration.",
            "Expand the DHCP scope or reduce lease times to free "
            "addresses; identify unauthorized devices hoarding leases "
            "and clean up stale reservations.",
        ],
        remediation_steps=[
            [
                "Check the DHCP scope utilization and active lease count for the affected subnet",
                "Identify and remove stale or orphaned DHCP leases from decommissioned devices",
                "Expand the DHCP scope range or add a secondary scope to accommodate the increased device count",
                "Reduce the DHCP lease duration to free addresses more quickly if demand is temporary",
                "Release and renew IP addresses on affected client devices to verify they obtain valid leases",
                "Monitor the scope utilization and plan a subnet redesign if the issue is structural",
            ],
        ],
    ),
    # ------------------------------------------------------------------
    # 11. WiFi certificate authentication failing
    # ------------------------------------------------------------------
    Scenario(
        scenario_id="net-wifi-cert-auth-failing",
        category="Network & Connectivity",
        priority="P2",
        assigned_team="Network Operations",
        needs_escalation=True,
        missing_information=["device_info", "error_message"],
        subjects=[
            "Can't connect to corporate WiFi — certificate error",
            "WiFi 802.1X authentication failing on my laptop",
            "Corporate wireless rejecting my certificate",
            "EAP-TLS authentication failure on WiFi",
        ],
        descriptions=[
            "I can't connect to the corporate WiFi anymore. My laptop "
            "shows 'Can't connect to this network' and the event log "
            "says 'EAP authentication failed — certificate rejected'. "
            "My machine certificate was auto-enrolled via Intune and "
            "it hasn't expired according to certmgr. This started "
            "yesterday afternoon and I've already tried forgetting and "
            "re-adding the network.",
            "After the latest Windows update my laptop won't "
            "authenticate to the corporate wireless. The WiFi profile "
            "shows 'Authentication failed' and I can see EAP-TLS "
            "errors in the event log. I've verified my certificate "
            "is valid. My colleague sitting next to me on the same "
            "laptop model has the same issue.",
            "Three people on my team got new laptops last week and "
            "none of them can connect to the corporate WiFi. They "
            "all show certificate authentication errors. The machines "
            "were enrolled in Intune and received the WiFi profile "
            "but the RADIUS server seems to be rejecting the "
            "machine certificates.",
        ],
        next_best_actions=[
            "Check the RADIUS server logs for the authentication "
            "rejection reason; verify the client certificate chain, "
            "CA trust, and certificate template used for enrollment "
            "against the NPS policy.",
            "Review the Network Policy Server (NPS) event logs for "
            "EAP-TLS failure reasons; verify the intermediate and "
            "root CA certificates are trusted by the RADIUS server.",
        ],
        remediation_steps=[
            [
                "Review RADIUS/NPS server logs for the specific authentication rejection reason and error code",
                "Verify the client machine certificate chain is "
                "complete and the root/intermediate CAs are trusted "
                "by the NPS server",
                "Check the NPS network policy for certificate template "
                "and EKU requirements against the enrolled certificate",
                "If a recent Windows update changed TLS behavior, verify NPS supports the client's TLS version",
                "Re-enroll the machine certificate via Intune if the certificate is corrupted or misconfigured",
                "Test WiFi authentication and confirm the user can connect successfully",
            ],
        ],
    ),
    # ------------------------------------------------------------------
    # 12. Teams/Zoom call quality issues
    # ------------------------------------------------------------------
    Scenario(
        scenario_id="net-call-quality-jitter",
        category="Network & Connectivity",
        priority="P3",
        assigned_team="Network Operations",
        needs_escalation=False,
        missing_information=[
            "network_location",
            "reproduction_frequency",
        ],
        subjects=[
            "Terrible call quality on Teams — choppy audio and video",
            "Zoom calls keep breaking up with packet loss",
            "Voice and video quality awful on Microsoft Teams",
            "Constant jitter and freezing during video meetings",
        ],
        descriptions=[
            "For the past few days my Teams calls have been terrible. "
            "Audio cuts in and out, video freezes, and I've been "
            "dropped from two meetings today. I'm in the NYC office "
            "on Floor 2 using WiFi. The Teams call health stats show "
            "jitter of 80-120 ms and 5-8% packet loss. It's "
            "happening on every call.",
            "Multiple people in the London office are experiencing "
            "horrible video call quality on both Teams and Zoom. "
            "We're getting robotic audio, pixelated video, and "
            "calls drop every 10-15 minutes. It seems to be worst "
            "during 10 AM - 2 PM when the most meetings happen. "
            "Wired Ethernet users seem to be affected too, so it's "
            "not just WiFi.",
            "I'm a remote worker and my Teams meeting quality has "
            "degraded significantly since the VPN policy change last "
            "week. My home internet is 200 Mbps but Teams traffic is "
            "now going through the VPN tunnel and I'm seeing 150+ ms "
            "latency and visible packet loss. Before the change, "
            "Teams used split tunneling and was fine.",
        ],
        next_best_actions=[
            "Review the Teams/Zoom call quality analytics for the "
            "affected users to identify jitter, packet loss, and "
            "latency patterns; check QoS policy configuration and "
            "network utilization on the affected segment.",
            "Check whether the VPN split-tunnel policy was recently "
            "changed to tunnel media traffic; review QoS markings "
            "for real-time media and verify the WAN/internet "
            "bandwidth is not saturated.",
        ],
        remediation_steps=[
            [
                "Pull call quality data from the Teams Admin Center or Zoom dashboard for affected users",
                "Identify whether the issue is localized to a specific office, floor, or network segment",
                "Check QoS policies to ensure real-time media traffic is prioritized (DSCP 46 for voice, 34 for video)",
                "Review WAN and internet circuit utilization for bandwidth saturation during peak hours",
                "If VPN is involved, verify split-tunnel configuration "
                "allows Teams/Zoom media traffic to bypass the tunnel",
                "Monitor call quality metrics after changes and confirm improvement with affected users",
            ],
        ],
    ),
    # ------------------------------------------------------------------
    # 13. Split-tunneling VPN configuration request
    # ------------------------------------------------------------------
    Scenario(
        scenario_id="net-vpn-split-tunnel-request",
        category="Network & Connectivity",
        priority="P4",
        assigned_team="Network Operations",
        needs_escalation=False,
        missing_information=[
            "configuration_details",
            "business_impact",
        ],
        subjects=[
            "Request to enable split tunneling on VPN for our team",
            "VPN split-tunnel configuration request",
            "Need split tunneling for better remote work performance",
        ],
        descriptions=[
            "Our data science team (about 15 people) works remotely "
            "most of the time and we're finding the full-tunnel VPN "
            "configuration is severely impacting our productivity. "
            "Downloading datasets from public cloud storage goes "
            "through the corporate VPN and the bandwidth is terrible. "
            "We'd like split tunneling enabled so public internet "
            "traffic goes direct while internal resources still route "
            "through the VPN.",
            "Requesting split-tunnel VPN configuration for the "
            "marketing department. Our team uses cloud-based tools "
            "like Figma, Canva, and Adobe Creative Cloud, and routing "
            "all that traffic through the VPN is causing massive "
            "slowdowns. We understand this needs security review — "
            "happy to meet with the security team to discuss.",
            "Can we get split tunneling enabled for the VPN? The "
            "current full-tunnel setup is causing 300+ ms latency to "
            "our AWS-hosted development environments because traffic "
            "routes NYC → London VPN → AWS eu-west-1 instead of "
            "going direct. Our engineering team of 25 is affected.",
        ],
        next_best_actions=[
            "Review the split-tunnel request against the VPN security "
            "policy; coordinate with Security Operations to define "
            "which traffic categories can bypass the tunnel while "
            "maintaining compliance requirements.",
            "Evaluate the request with the security team, define a "
            "split-tunnel policy that exempts approved SaaS/cloud "
            "destinations while keeping sensitive traffic in the "
            "tunnel, and schedule implementation.",
        ],
        remediation_steps=[
            [
                "Review the split-tunnel request and document the business justification and affected user group",
                "Coordinate with Security Operations to assess risk and define an approved split-tunnel policy",
                "Configure the VPN gateway to exclude approved SaaS/cloud IP ranges from the tunnel",
                "Deploy the updated VPN profile to the requesting team via Intune or GPO",
                "Test split-tunnel behavior and verify internal resource access is maintained",
                "Monitor for security events and confirm performance improvement with the requesting team",
            ],
        ],
    ),
    # ------------------------------------------------------------------
    # 14. Network segmentation request for new VLAN
    # ------------------------------------------------------------------
    Scenario(
        scenario_id="net-vlan-segmentation-request",
        category="Network & Connectivity",
        priority="P4",
        assigned_team="Network Operations",
        needs_escalation=False,
        missing_information=[
            "configuration_details",
            "environment_details",
        ],
        subjects=[
            "Request for new VLAN for IoT devices in the office",
            "Network segmentation — need a dedicated VLAN",
            "New VLAN request for conference room AV equipment",
            "VLAN provisioning request for lab environment",
        ],
        descriptions=[
            "We're deploying new IoT sensors across the NYC office for "
            "our smart building initiative — temperature, occupancy, "
            "and air quality sensors. We need a dedicated VLAN to "
            "isolate these devices from the corporate network. "
            "Expected device count is around 200, and they'll need "
            "internet access to push data to our cloud platform but "
            "no access to internal resources.",
            "The facilities team is installing new AV equipment in 12 "
            "conference rooms across the London office. We need a "
            "separate VLAN for these devices to keep them off the "
            "corporate network. The equipment includes smart displays, "
            "Zoom Room controllers, and wireless presentation devices. "
            "They need access to Zoom and Teams cloud services only.",
            "Our security research team needs an isolated VLAN for a "
            "new lab environment in the Denver office. The VLAN should "
            "have no access to the production network and limited "
            "internet access through a dedicated firewall policy. We "
            "need about 50 IP addresses and the VLAN should be "
            "available on switch ports in Room 405.",
        ],
        next_best_actions=[
            "Gather detailed requirements including device count, "
            "required connectivity, and security policies; plan the "
            "VLAN assignment, subnet allocation, and inter-VLAN "
            "access control rules.",
            "Design the VLAN with appropriate subnet sizing, DHCP "
            "scope, and firewall rules; coordinate with the security "
            "team for the ACL policy and schedule implementation.",
        ],
        remediation_steps=[
            [
                "Document the VLAN requirements: device count, connectivity needs, and security policy",
                "Allocate a VLAN ID and subnet from the IP address management system",
                "Configure the VLAN on the core and access switches for the target location",
                "Create a DHCP scope for the new subnet and configure firewall ACLs per the security policy",
                "Tag the required switch ports to the new VLAN and test device connectivity",
                "Document the VLAN in the network inventory and hand off to the requesting team",
            ],
        ],
    ),
    # ------------------------------------------------------------------
    # 15. CDN/edge caching issues
    # ------------------------------------------------------------------
    Scenario(
        scenario_id="net-cdn-caching-issues",
        category="Network & Connectivity",
        priority="P3",
        assigned_team="Network Operations",
        needs_escalation=False,
        missing_information=[
            "affected_system",
            "steps_to_reproduce",
        ],
        subjects=[
            "CDN serving stale content after deployment",
            "Edge cache not updating — users see old version",
            "CloudFront caching issue for our web app",
        ],
        descriptions=[
            "We deployed a new version of the customer portal two "
            "hours ago but users are still seeing the old version. "
            "Our CDN (CloudFront) appears to be serving cached content "
            "from the previous deployment. We've tried invalidating "
            "the cache via the AWS console but it doesn't seem to have "
            "taken effect. The origin server is serving the correct "
            "version when accessed directly.",
            "After pushing an update to our public-facing website, "
            "some users in Europe see the new version while US users "
            "still see the old one. It looks like some CDN edge nodes "
            "haven't picked up the new content. We set cache-control "
            "headers to max-age=3600 but it's been over four hours. "
            "This is confusing customers who see inconsistent content.",
            "Our CDN is caching API responses that should not be "
            "cached. The /api/v2/pricing endpoint is returning stale "
            "pricing data because a cache-control header was "
            "accidentally set to public. We need to purge the CDN "
            "cache immediately and fix the caching policy to prevent "
            "this from happening again.",
        ],
        next_best_actions=[
            "Initiate a full CDN cache invalidation for the affected "
            "paths; verify cache-control headers on the origin server "
            "are set correctly for the deployment pipeline.",
            "Purge the CDN cache for the affected content paths and "
            "verify the origin server response headers; update the "
            "deployment pipeline to include automatic cache "
            "invalidation.",
        ],
        remediation_steps=[
            [
                "Initiate a CDN cache invalidation for all affected paths or a wildcard invalidation if needed",
                "Verify cache-control and surrogate-control headers on the origin server for each affected resource",
                "Confirm edge nodes are serving the updated content by testing from multiple geographic locations",
                "Update the deployment pipeline to include automatic CDN cache invalidation on each release",
                "Review the caching policy to ensure dynamic content "
                "and API responses have appropriate no-cache headers",
            ],
        ],
    ),
    # ------------------------------------------------------------------
    # 16. SSL/TLS handshake failures to internal service
    # ------------------------------------------------------------------
    Scenario(
        scenario_id="net-tls-handshake-failure",
        category="Network & Connectivity",
        priority="P2",
        assigned_team="Network Operations",
        needs_escalation=True,
        missing_information=["error_message", "affected_system"],
        subjects=[
            "SSL handshake failure connecting to internal API",
            "TLS error when accessing internal service",
            "HTTPS connections failing to payroll.contoso.internal",
        ],
        descriptions=[
            "All HTTPS connections to our internal payroll service at "
            "payroll.contoso.internal are failing with SSL handshake "
            "errors. Browsers show 'ERR_SSL_VERSION_OR_CIPHER_MISMATCH' "
            "and curl gives 'SSL routines: no common signature "
            "algorithms'. This started at 6 AM after the weekend "
            "maintenance window. The payroll team can't process this "
            "week's payroll run, which is due by end of day.",
            "We're getting TLS handshake failures when our microservices "
            "try to communicate with the internal auth service over "
            "HTTPS. The error logs show 'remote error: tls: handshake "
            "failure'. Nothing changed on our side — we suspect the "
            "auth service certificate was rotated and the new cert "
            "uses a different cipher suite. About 15 services are "
            "affected.",
            "After a certificate renewal on the internal GitLab server, "
            "all git operations over HTTPS are failing. Users see "
            "'SSL certificate problem: unable to get local issuer "
            "certificate'. It looks like the new certificate was signed "
            "by our internal CA but the intermediate certificate is "
            "missing from the chain. This is blocking all development "
            "work.",
        ],
        next_best_actions=[
            "Check the SSL certificate on the affected service for "
            "validity, chain completeness, and cipher suite "
            "compatibility; compare the TLS configuration against "
            "client requirements.",
            "Verify the recently renewed certificate is properly "
            "installed with the full chain and uses a supported "
            "cipher suite; check for TLS version mismatches between "
            "client and server.",
        ],
        remediation_steps=[
            [
                "Test the SSL/TLS connection using openssl s_client to identify the specific handshake failure reason",
                "Check the server certificate for validity, expiration, and complete chain (root + intermediate CAs)",
                "Verify the server's TLS configuration supports cipher suites compatible with the connecting clients",
                "If the intermediate certificate is missing, install the complete certificate chain on the server",
                "Restart the affected service to load the corrected certificate configuration",
                "Test HTTPS connectivity from affected clients and confirm the handshake succeeds",
                "Update the certificate management runbook to include chain validation as a post-renewal check",
            ],
        ],
    ),
    # ------------------------------------------------------------------
    # 17. MTU mismatch causing packet fragmentation
    # ------------------------------------------------------------------
    Scenario(
        scenario_id="net-mtu-mismatch",
        category="Network & Connectivity",
        priority="P3",
        assigned_team="Network Operations",
        needs_escalation=False,
        missing_information=[
            "environment_details",
            "steps_to_reproduce",
        ],
        subjects=[
            "Large file transfers failing — possible MTU issue",
            "Packets being fragmented, slow transfers over VPN",
            "MTU mismatch causing intermittent connection drops",
        ],
        descriptions=[
            "We're seeing intermittent failures when transferring large "
            "files between the NYC and Singapore offices over the "
            "site-to-site VPN. Small files transfer fine but anything "
            "over a few MB either stalls or fails halfway through. "
            "A packet capture shows fragmentation and some fragments "
            "being dropped. We suspect an MTU mismatch somewhere "
            "along the path.",
            "Users in Singapore report that certain internal web "
            "applications load partially or hang when loading large "
            "pages. A traceroute shows the traffic crosses a GRE "
            "tunnel where the MTU is set to 1500, but the tunnel "
            "overhead means the effective MTU should be 1476. Pings "
            "with DF bit set and size > 1476 are being dropped.",
            "After migrating to a new MPLS provider, we're getting "
            "reports of stalled SSH sessions and incomplete database "
            "replication between NYC and Denver. The sessions work "
            "fine for small queries but hang on large result sets. "
            "Initial investigation points to a Path MTU Discovery "
            "issue — ICMP 'Fragmentation Needed' packets appear to "
            "be blocked somewhere in the path.",
        ],
        next_best_actions=[
            "Perform a path MTU discovery test between the affected "
            "sites to identify where fragmentation occurs; verify "
            "MTU settings on tunnel interfaces and ensure ICMP "
            "'Fragmentation Needed' messages are not blocked.",
            "Check the MTU configuration on all interfaces along the "
            "path including tunnel and MPLS interfaces; enable TCP "
            "MSS clamping on the tunnel endpoints as an immediate "
            "workaround.",
        ],
        remediation_steps=[
            [
                "Run path MTU discovery tests between affected sites using ping with DF bit set at varying sizes",
                "Identify the hop where fragmentation occurs and check the MTU setting on that interface",
                "Adjust the MTU on tunnel interfaces to account for "
                "encapsulation overhead (e.g., 1400 for GRE over IPSec)",
                "Enable TCP MSS clamping on tunnel endpoints to prevent "
                "TCP sessions from negotiating too-large segments",
                "Verify that ICMP 'Fragmentation Needed' (Type 3, Code 4) packets are not blocked by firewalls",
                "Test large file transfers and confirm the issue is resolved",
            ],
        ],
    ),
    # ------------------------------------------------------------------
    # 18. Bandwidth throttling complaint
    # ------------------------------------------------------------------
    Scenario(
        scenario_id="net-bandwidth-throttling",
        category="Network & Connectivity",
        priority="P3",
        assigned_team="Network Operations",
        needs_escalation=False,
        missing_information=[
            "network_location",
            "steps_to_reproduce",
        ],
        subjects=[
            "My internet feels throttled — downloads are capped",
            "Bandwidth seems limited, can't download at full speed",
            "Network speed capped to 10 Mbps, is there a QoS limit?",
            "Slow download speeds — is traffic being shaped?",
        ],
        descriptions=[
            "I've noticed my download speeds are capped at exactly "
            "10 Mbps no matter what I'm downloading. Speed tests to "
            "the internet show the same 10 Mbps cap. Other people "
            "around me on the same floor seem to get normal speeds "
            "(100+ Mbps). I'm on a wired connection in the NYC office, "
            "Floor 4. Is there a QoS policy limiting my traffic?",
            "I'm a video editor and I need to download large assets "
            "from our cloud storage regularly. My speeds have been "
            "capped at what appears to be 10 Mbps for the last week. "
            "I tested from a colleague's machine on the same Ethernet "
            "jack and they get full speed, so it seems like something "
            "specific to my machine or user account.",
            "The entire design team (6 people) in the London office is "
            "experiencing what looks like bandwidth throttling. We all "
            "see speeds capped around 20 Mbps. We recently moved to "
            "new desks on Floor 3 and the issue started after the "
            "move. Other teams on the same floor don't seem affected.",
        ],
        next_best_actions=[
            "Check the switch port configuration for the user's "
            "Ethernet port (rate limiting, storm control, duplex "
            "mismatch); review QoS policies applied to their VLAN "
            "or user group.",
            "Verify the user's switch port settings and VLAN "
            "assignment; check for per-port rate limiting or "
            "per-user QoS policies that may be throttling traffic.",
        ],
        remediation_steps=[
            [
                "Identify the user's switch port and check the "
                "interface configuration for rate limiting or "
                "speed/duplex settings",
                "Verify the VLAN assignment is correct for the user's team and location",
                "Review QoS policies applied to the user's VLAN or security group for bandwidth caps",
                "Check for duplex mismatch (half vs full duplex) on the switch port which can cause reduced throughput",
                "Correct any misconfiguration and test download speeds from the user's machine",
                "Confirm with the user that speeds are back to normal",
            ],
        ],
    ),
    # ------------------------------------------------------------------
    # 19. IPSec tunnel flapping between sites
    # ------------------------------------------------------------------
    Scenario(
        scenario_id="net-ipsec-tunnel-flapping",
        category="Network & Connectivity",
        priority="P2",
        assigned_team="Network Operations",
        needs_escalation=True,
        missing_information=["timestamp", "error_message"],
        subjects=[
            "IPSec tunnel between NYC and Denver keeps flapping",
            "VPN tunnel NYC-Denver unstable — going up and down",
            "Intermittent IPSec tunnel drops to Denver office",
        ],
        descriptions=[
            "The IPSec tunnel between the NYC and Denver offices has "
            "been flapping every 15-20 minutes since last night. The "
            "tunnel comes up, stays stable for about 15 minutes, then "
            "drops and re-establishes. During the drops, users in "
            "Denver lose access to NYC-hosted file servers and the "
            "ERP system for 30-60 seconds. The firewall logs show "
            "IKE phase 2 rekey failures.",
            "Our monitoring has been alerting on the NYC-Denver IPSec "
            "tunnel going down and coming back up repeatedly. It's "
            "been happening since approximately 11 PM last night. "
            "Each outage lasts about 45 seconds. The Denver office "
            "team reports intermittent disconnections from internal "
            "applications throughout the day.",
            "We're seeing IPSec tunnel instability between the NYC "
            "data center and the Denver office. The tunnel tears down "
            "during IKE phase 2 renegotiation — the logs show DPD "
            "(Dead Peer Detection) timeouts on the NYC side. The "
            "WAN circuit appears healthy on both ends. Suspect a "
            "configuration drift after last week's firewall patch.",
        ],
        next_best_actions=[
            "Review the IKE/IPSec logs on both endpoints for rekey "
            "failures and DPD timeout events; compare the tunnel "
            "configuration on both sides for SA lifetime, PFS group, "
            "and DPD settings after the recent firewall patch.",
            "Check for WAN micro-outages or increased latency that "
            "could trigger DPD timeouts; verify IKE SA lifetimes "
            "and phase 2 rekey settings match on both tunnel "
            "endpoints.",
        ],
        remediation_steps=[
            [
                "Review IKE and IPSec logs on both NYC and Denver firewalls for the specific failure reason",
                "Compare tunnel configuration on both endpoints to "
                "verify SA lifetimes, PFS groups, and DPD settings "
                "are consistent",
                "Check for recent firewall patches or configuration changes that may have altered tunnel parameters",
                "If DPD timeouts are the cause, increase the DPD interval and retry count or tune keepalive settings",
                "Monitor the tunnel stability for 24 hours to confirm the flapping has stopped",
                "Document the root cause and update the change management records for the firewall patch",
            ],
        ],
    ),
    # ------------------------------------------------------------------
    # 20. BGP peering issue affecting routing
    # ------------------------------------------------------------------
    Scenario(
        scenario_id="net-bgp-peering-issue",
        category="Network & Connectivity",
        priority="P2",
        assigned_team="Network Operations",
        needs_escalation=True,
        missing_information=["error_message", "configuration_details"],
        subjects=[
            "BGP peering down with ISP — routing affected",
            "BGP session dropped, asymmetric routing issues",
            "Internet routing problems — BGP peer flapping",
        ],
        descriptions=[
            "Our primary BGP peering session with our ISP went down "
            "about an hour ago. Traffic is failing over to the "
            "secondary ISP link but we're seeing asymmetric routing "
            "and increased latency for users in the NYC office. Some "
            "external services are unreachable because the return "
            "path is using the secondary link which has lower "
            "bandwidth. Need to get the primary BGP session restored.",
            "Our monitoring shows the BGP session with AS 65100 has "
            "been in an 'Idle' state since 3:15 AM. The ISP says "
            "they see our side as 'Active'. The router logs show "
            "repeated 'NOTIFICATION received — hold timer expired' "
            "messages. Failover to the backup ISP is working but "
            "the backup link is at 80% capacity and some traffic "
            "is being dropped during peak hours.",
            "We're experiencing routing anomalies after a BGP "
            "configuration change last night. The change was supposed "
            "to adjust route preferences between our two ISP links, "
            "but now some routes are missing from the routing table "
            "and certain external SaaS providers (including our "
            "payment gateway) are unreachable from the NYC and "
            "London offices.",
        ],
        next_best_actions=[
            "Check the BGP session status and router logs for the "
            "specific NOTIFICATION reason; contact the ISP NOC to "
            "coordinate restoring the peering session and verify "
            "route advertisements.",
            "Review the recent BGP configuration change for errors "
            "in route-map or prefix-list definitions; verify the "
            "BGP routing table for missing or withdrawn routes and "
            "roll back if necessary.",
        ],
        remediation_steps=[
            [
                "Check the BGP session status on the edge router and "
                "review the logs for NOTIFICATION and error messages",
                "Verify the BGP configuration (neighbor IP, AS number, "
                "authentication, timers) matches the ISP's expectations",
                "Contact the ISP NOC to coordinate troubleshooting and confirm their side of the peering session",
                "If a recent configuration change caused the issue, roll back to the previous configuration",
                "Clear the BGP session and allow it to re-establish; verify the full routing table is received",
                "Monitor routing tables and traffic flow for 24 hours to ensure stability",
                "Document the incident and update the BGP runbook with lessons learned",
            ],
        ],
    ),
    # ------------------------------------------------------------------
    # 21. Network printer not reachable from VLAN
    # ------------------------------------------------------------------
    Scenario(
        scenario_id="net-printer-unreachable-vlan",
        category="Network & Connectivity",
        priority="P4",
        assigned_team="Network Operations",
        needs_escalation=False,
        missing_information=["device_info", "network_location"],
        subjects=[
            "Can't print — printer not reachable from my desk",
            "Network printer offline after office move",
            "Printer on Floor 2 not accessible from our VLAN",
            "Printing not working after VLAN change",
        ],
        descriptions=[
            "Since my team moved to new desks on Floor 2 last week, "
            "we can't reach the network printer (HP LaserJet on "
            "Floor 2, printer name NYCF2-HP01). Our laptops show "
            "the printer as offline. I can ping other devices on our "
            "subnet but the printer seems to be on a different VLAN. "
            "Before the move we were on the same floor and it worked.",
            "I'm trying to print to the shared printer in the London "
            "office (Room 3-42) but my laptop says the printer is "
            "not reachable. Other people in my team sitting in the "
            "same area have the same problem. We just got assigned "
            "to a new VLAN as part of the network segmentation "
            "project and printing stopped working after that.",
            "The network printer in our Singapore office stopped "
            "being accessible after IT changed our network "
            "configuration last Friday. The printer IP is "
            "10.8.3.50 and we're now on the 10.8.5.0/24 subnet. "
            "I can see the printer isn't on our subnet anymore. "
            "Is there a routing or firewall rule that needs updating?",
        ],
        next_best_actions=[
            "Verify the inter-VLAN routing and firewall rules between "
            "the user's new VLAN and the printer's VLAN; check that "
            "the required print ports (9100, 631, 515) are allowed.",
            "Confirm the printer's VLAN and IP address, then check "
            "the ACLs and routing between the user's VLAN and the "
            "printer VLAN to ensure print traffic is permitted.",
        ],
        remediation_steps=[
            [
                "Confirm the printer's current IP address and VLAN assignment",
                "Identify the user's VLAN and verify inter-VLAN routing is configured between the two VLANs",
                "Check firewall ACLs for rules allowing print traffic (TCP ports 9100, 631, 515) between the VLANs",
                "Add or update the ACL to permit print traffic from the user's VLAN to the printer VLAN",
                "Test printing from the user's workstation and confirm the printer is reachable",
            ],
        ],
    ),
    # ------------------------------------------------------------------
    # 22. Corporate WiFi certificate renewal failing for all users
    # ------------------------------------------------------------------
    Scenario(
        scenario_id="net-wifi-cert-renewal-mass",
        category="Network & Connectivity",
        priority="P2",
        assigned_team="Network Operations",
        needs_escalation=True,
        missing_information=[
            "affected_users",
            "error_message",
            "timestamp",
        ],
        subjects=[
            "Corporate WiFi certs expiring — mass authentication failures",
            "WiFi certificate renewal failing for all users",
            "Widespread WiFi auth failures — cert auto-renewal broken",
        ],
        descriptions=[
            "We're getting a flood of reports from users across the "
            "NYC and London offices who are unable to connect to the "
            "corporate WiFi. The machine certificates used for 802.1X "
            "authentication are expiring and the auto-renewal via "
            "Intune/SCEP appears to be broken. Certificates that "
            "expired over the weekend were not renewed and those "
            "devices can no longer authenticate. Approximately 200 "
            "users are affected so far and the number is growing.",
            "Starting this morning, a large number of employees in "
            "multiple offices are unable to connect to the corporate "
            "wireless network. Investigation shows their device "
            "certificates have expired. The SCEP enrollment profile "
            "in Intune should auto-renew certificates 20 days before "
            "expiry but it seems the NDES server has been offline "
            "since Friday. Every device whose cert expired over the "
            "weekend is now locked out.",
            "The corporate WiFi is experiencing widespread "
            "authentication failures. Our RADIUS server logs show "
            "hundreds of EAP-TLS rejections with 'certificate expired' "
            "as the reason. The SCEP certificate renewal pipeline "
            "appears to have stalled — the NDES connector service "
            "crashed and wasn't automatically restarted. Affected "
            "user count is currently around 350 and growing as more "
            "certificates reach their expiry date.",
        ],
        next_best_actions=[
            "Immediately check the NDES server and Intune SCEP "
            "connector health; restart the connector service and "
            "verify certificate enrollment is processing; consider "
            "a temporary RADIUS policy to allow expired certs while "
            "renewal catches up.",
            "Restore the NDES/SCEP enrollment pipeline as the top "
            "priority; implement a temporary workaround such as a "
            "PSK-based SSID for affected users while certificates "
            "are being renewed.",
        ],
        remediation_steps=[
            [
                "Check the NDES server health and restart the Intune SCEP connector service if it is down",
                "Verify the SCEP enrollment endpoint is responding and processing certificate requests",
                "Provision a temporary PSK-based WiFi SSID with "
                "internet-only access as a workaround for affected "
                "users",
                "Trigger certificate renewal for affected devices via Intune sync or manual SCEP enrollment",
                "Monitor the RADIUS server logs to confirm devices are re-authenticating with renewed certificates",
                "Set up monitoring and alerting on the NDES connector service to prevent future silent failures",
                "Decommission the temporary SSID once all devices have renewed certificates",
            ],
        ],
    ),
    Scenario(
        scenario_id="net-latency-trading-floor",
        category="Network & Connectivity",
        priority="P1",
        assigned_team="Network Operations",
        needs_escalation=True,
        missing_information=["network_location", "reproduction_frequency", "timestamp"],
        subjects=[
            "High network latency on trading floor — affecting order execution",
            "Trading systems experiencing 200ms+ latency spikes",
            "Network latency causing trade execution delays in NYC office",
        ],
        descriptions=[
            "The trading floor in our NYC office is experiencing significant network latency spikes — ping times to our"
            " exchange gateways are jumping from the normal 2ms to over 200ms intermittently. This is causing order exe"
            "cution delays that are costing us money. The latency spikes seem random but are happening every few minute"
            "s.",
            "Our high-frequency trading systems are reporting unacceptable latency on the NYC trading floor network "
            "segment. Traceroute shows the bottleneck is between the floor switch and the core router. This started "
            "about 90 minutes ago and is getting worse.",
        ],
        next_best_actions=[
            "Immediately investigate the trading floor network segment for congestion, bad cables, or switch issues. "
            "Check for broadcast storms or spanning tree reconvergence.",
        ],
        remediation_steps=[
            [
                "Run network diagnostics on the trading floor switch (interface errors, CRC, drops)",
                "Check for broadcast storms or spanning tree topology changes",
                "Review QoS policies to ensure trading traffic is prioritized",
                "Check uplink utilization between floor switches and core",
                "If hardware fault, failover to redundant switch path",
                "Engage vendor support if switch firmware issue suspected",
            ],
        ],
        tags=["trading", "latency", "critical"],
        channel_weights={"email": 0.05, "chat": 0.10, "portal": 0.05, "phone": 0.80},
    ),
    Scenario(
        scenario_id="net-expressroute-degraded",
        category="Network & Connectivity",
        priority="P1",
        assigned_team="Network Operations",
        needs_escalation=True,
        missing_information=["network_location", "business_impact"],
        subjects=[
            "Azure ExpressRoute circuit degraded — cloud services slow",
            "ExpressRoute showing packet loss — Azure connectivity issues",
            "Private peering to Azure down — all cloud workloads affected",
        ],
        descriptions=[
            "Our ExpressRoute circuit to Azure is showing 15% packet loss since 7 AM. All cloud-hosted applications "
            "(Dynamics, Power BI, internal APIs) are extremely slow or timing out. Both our primary and secondary "
            "peering connections seem affected. This is impacting all three offices.",
            "Azure connectivity through ExpressRoute is severely degraded. BGP session keeps flapping on the primary "
            "circuit. Failover to the secondary ISP link isn't happening as expected. Our entire Azure-hosted "
            "application stack is affected — roughly 2000 users across the company.",
        ],
        next_best_actions=[
            "Check ExpressRoute circuit health in Azure portal and engage ISP for circuit diagnostics. Verify BGP "
            "peering status and failover configuration.",
        ],
        remediation_steps=[
            [
                "Check ExpressRoute circuit metrics in Azure portal (packet loss, throughput)",
                "Verify BGP peering status on both primary and secondary connections",
                "Contact ISP to check for carrier-side issues on the circuit",
                "Validate failover to secondary circuit/path is configured correctly",
                "If primary is degraded, force traffic to secondary via BGP prepending",
                "Open a severity A case with Microsoft if Azure-side issue",
            ],
        ],
        tags=["expressroute", "azure", "critical"],
        channel_weights={"email": 0.10, "chat": 0.20, "portal": 0.10, "phone": 0.60},
    ),
    Scenario(
        scenario_id="net-cross-office-video-quality",
        category="Network & Connectivity",
        priority="P3",
        assigned_team="Network Operations",
        needs_escalation=False,
        missing_information=["network_location", "reproduction_frequency", "affected_users"],
        subjects=[
            "Video call quality terrible between NYC and Singapore offices",
            "Teams video freezing during cross-region calls",
            "Inter-office video conferencing quality degradation",
        ],
        descriptions=[
            "Video calls between our NYC and Singapore offices have been terrible for the past week. Video freezes "
            "every few seconds and audio cuts in and out. This only happens on cross-office calls — local Teams calls "
            "work perfectly. We have daily standups with the Singapore team at 9 PM EST / 9 AM SGT and it's been "
            "unusable.",
            "The video quality on Teams calls between London and Singapore keeps dropping to poor quality. Participants"
            " are pixelated and there's a 3-4 second audio delay. We've tried meeting room systems and individual lapto"
            "ps — same issue. Internal calls within each office are fine.",
        ],
        next_best_actions=[
            "Investigate inter-office WAN link utilization and QoS for real-time traffic. Check if MPLS/SD-WAN path "
            "between offices is congested or rerouting.",
        ],
        remediation_steps=[
            [
                "Check WAN link utilization between the affected offices",
                "Verify QoS markings for real-time media traffic (DSCP EF/AF41)",
                "Review SD-WAN or MPLS path selection for Teams media traffic",
                "Test with Teams network assessment tool from both offices",
                "Check if recent WAN changes affected traffic routing",
                "Consider implementing local media optimization or Teams direct routing",
            ],
        ],
        tags=["cross_office", "video", "wan"],
    ),
    Scenario(
        scenario_id="net-dns-intermittent-failure",
        category="Network & Connectivity",
        priority="P2",
        assigned_team="Network Operations",
        needs_escalation=False,
        missing_information=["network_location", "steps_to_reproduce", "affected_users"],
        subjects=[
            "Intermittent DNS resolution failures across the office",
            "Random 'DNS_PROBE_FINISHED_NXDOMAIN' errors in Chrome",
            "Websites randomly fail to load — DNS issue suspected",
        ],
        descriptions=[
            "For the past two days, random websites and internal applications fail to load intermittently. Chrome shows"
            " DNS_PROBE_FINISHED_NXDOMAIN errors. It happens maybe once every 10-15 minutes and resolves itself after a"
            " few seconds. Affects multiple users on the 7th floor. nslookup sometimes returns different results than e"
            "xpected.",
            "We're getting sporadic DNS failures across the London office. Internal and external name resolution "
            "randomly fails and then works again seconds later. It's causing issues with our CI/CD pipelines because "
            "API calls to internal services sporadically fail with 'name not resolved' errors.",
        ],
        next_best_actions=[
            "Investigate DNS server health and query logs. Check for DNS server overload, stale records, or DHCP "
            "assigning incorrect DNS servers.",
        ],
        remediation_steps=[
            [
                "Check DNS server health metrics (query response time, queue length)",
                "Review DNS server event logs for errors or warnings",
                "Verify DHCP scope is assigning correct DNS server addresses",
                "Check for DNS cache poisoning or stale records",
                "Monitor DNS query logs for unusual patterns or high volume",
                "Consider adding DNS server capacity if overloaded",
            ],
        ],
        tags=["dns", "intermittent"],
    ),
    Scenario(
        scenario_id="net-zscaler-blocking-legit",
        category="Network & Connectivity",
        priority="P3",
        assigned_team="Network Operations",
        needs_escalation=False,
        missing_information=["affected_system", "network_location", "screenshot_or_attachment"],
        subjects=[
            "Zscaler blocking access to a legitimate vendor portal",
            "Web proxy blocking business-critical website",
            "Can't access client's secure file transfer site — Zscaler blocks it",
        ],
        descriptions=[
            "Zscaler is blocking access to our client's secure file transfer portal (securetransfer.clientname.com). "
            "It's being categorized as 'Uncategorized' and getting blocked by our default deny policy. I need access "
            "urgently to download documents for a deal closing this week.",
            "Our web security proxy (Zscaler) is incorrectly blocking a legitimate SaaS application "
            "(app.vendorname.com) that our Compliance team needs for regulatory reporting. The site is flagged as "
            "'potentially dangerous' but we've verified it's safe. 15 people in Compliance are blocked.",
        ],
        next_best_actions=[
            "Review the Zscaler URL categorization and create a URL allowlist entry for the legitimate site after "
            "security review.",
        ],
        remediation_steps=[
            [
                "Verify the blocked URL is a legitimate business site",
                "Check Zscaler admin console for the URL category and blocking rule",
                "Request URL recategorization from Zscaler if miscategorized",
                "Add a temporary URL allowlist entry for immediate access",
                "Verify the user can access the site after the allowlist update",
                "Document the exception in the security change log",
            ],
        ],
        tags=["proxy", "web_security"],
    ),
    Scenario(
        scenario_id="net-sd-wan-failover-issue",
        category="Network & Connectivity",
        priority="P2",
        assigned_team="Network Operations",
        needs_escalation=False,
        missing_information=["network_location", "configuration_details", "business_impact"],
        subjects=[
            "SD-WAN not failing over to backup link during outage",
            "Branch office SD-WAN failover not working properly",
            "Internet outage at Singapore office — SD-WAN didn't switch links",
        ],
        descriptions=[
            "Our Singapore office experienced an ISP outage this morning and the SD-WAN appliance didn't fail over to t"
            "he backup 4G link as it should. The entire office was offline for 2 hours until the ISP restored service. "
            "The failover worked perfectly in our last DR test a month ago.",
            "SD-WAN failover from primary MPLS to backup internet link isn't triggering at the London branch. We keep "
            "losing connectivity for 5-10 minutes before manual intervention. The SD-WAN dashboard shows the backup "
            "link as healthy but the automatic failover policy isn't engaging.",
        ],
        next_best_actions=[
            "Review SD-WAN failover policy configuration and test health check probes. Verify backup link is properly "
            "configured and SLA triggers are set correctly.",
        ],
        remediation_steps=[
            [
                "Review SD-WAN failover policy configuration and SLA thresholds",
                "Verify health check probes are properly configured for both links",
                "Test backup link connectivity and throughput independently",
                "Check SD-WAN appliance firmware for known failover bugs",
                "Reconfigure SLA-based failover triggers if thresholds are too permissive",
                "Schedule a controlled failover test to validate the fix",
            ],
        ],
        tags=["sdwan", "failover"],
    ),
]
