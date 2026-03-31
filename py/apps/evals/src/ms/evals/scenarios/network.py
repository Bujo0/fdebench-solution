# Copyright (c) Microsoft. All rights reserved.
"""Network & Connectivity scenario templates.

Covers: VPN issues, WiFi problems, DNS failures, firewall rules,
bandwidth/latency, video conferencing quality, proxy issues, WAN/LAN,
network outages, and remote access problems.
"""

from ms.evals.constants import Category
from ms.evals.constants import MissingInfo
from ms.evals.constants import Priority
from ms.evals.constants import Team
from ms.evals.models import ScenarioTemplate
from ms.evals.scenarios.registry import register

# ---------------------------------------------------------------------------
# net-001  VPN drops when switching WiFi to Ethernet
# ---------------------------------------------------------------------------
register(ScenarioTemplate(
    scenario_id="net-001",
    category=Category.NETWORK,
    priority=Priority.P3,
    assigned_team=Team.NETWORK,
    needs_escalation=False,
    missing_information=[MissingInfo.DEVICE_INFO, MissingInfo.ERROR_MESSAGE],
    subjects=[
        "VPN disconnects every time I switch from WiFi to Ethernet",
        "GlobalProtect drops when I plug in Ethernet cable",
        "VPN connection lost on network switch",
    ],
    descriptions=[
        "Every time I dock my laptop and switch from WiFi to wired Ethernet, GlobalProtect drops "
        "and I have to manually reconnect. It usually takes 2-3 minutes before it lets me reconnect. "
        "This happens multiple times a day when I move between the hot-desk area and my regular desk "
        "on Floor 7 in the NYC office.",
        "Since last week my VPN drops the moment I go from wireless to wired. I'm on the NYC trading "
        "floor and need to dock/undock constantly. Reconnecting takes forever and kills my Bloomberg "
        "session every time. Other people on my team say they don't have this issue.",
    ],
    next_best_actions=[
        "Check GlobalProtect client version and network adapter settings. Verify split-tunnel "
        "configuration handles adapter transitions gracefully.",
        "Review GP client logs during the transition event and verify whether the 'seamless roaming' "
        "policy is applied to the user's machine.",
    ],
    remediation_steps=[
        [
            "Collect GlobalProtect client logs during a WiFi-to-Ethernet transition",
            "Verify the GP client version is current and matches the approved build",
            "Check network adapter priority settings on the device",
            "Ensure the GP gateway supports seamless adapter handoff",
            "Test with a loaner laptop to rule out hardware-specific issues",
        ],
        [
            "Review GP portal/gateway configuration for adapter-change behavior",
            "Check Windows network profile ordering (wired should be preferred)",
            "Disable WiFi auto-disconnect when Ethernet is detected in adapter settings",
            "Update GlobalProtect client if below the current approved version",
            "Monitor for recurrence over 48 hours after changes",
        ],
    ],
))

# ---------------------------------------------------------------------------
# net-002  VPN can't connect from hotel WiFi
# ---------------------------------------------------------------------------
register(ScenarioTemplate(
    scenario_id="net-002",
    category=Category.NETWORK,
    priority=Priority.P3,
    assigned_team=Team.NETWORK,
    needs_escalation=False,
    missing_information=[MissingInfo.ERROR_MESSAGE, MissingInfo.NETWORK_LOCATION],
    subjects=[
        "Can't connect to VPN from hotel — stuck on 'Connecting'",
        "GlobalProtect won't connect on hotel WiFi",
    ],
    descriptions=[
        "I'm traveling for a client meeting in Chicago and can't get GlobalProtect to connect from "
        "my hotel WiFi. It just spins on 'Connecting…' for about 60 seconds then fails. I've tried "
        "the hotel's conference-room WiFi too — same result. I need access to the deal room on "
        "SharePoint by 8am tomorrow. My phone hotspot works fine for VPN, so it seems like the "
        "hotel network is blocking something.",
        "Stuck at a Marriott and VPN will not connect. Tried rebooting, forgetting the network, "
        "reconnecting — nothing works. I can browse the internet fine but GP never gets past the "
        "initial handshake. Need to prep for tomorrow's board presentation and all my files are on "
        "the corporate network.",
    ],
    next_best_actions=[
        "Advise user to try GlobalProtect's fallback SSL/TLS mode which uses port 443 to bypass "
        "hotel captive portal restrictions. If that fails, mobile hotspot is a viable workaround.",
        "Check whether the hotel network is blocking IPsec (UDP 4501/500). Guide the user through "
        "enabling the GP HIP-based fallback gateway.",
    ],
    remediation_steps=[
        [
            "Verify the hotel's captive portal has been fully authenticated in a browser",
            "Switch GlobalProtect to SSL fallback mode (TCP 443) to bypass port blocks",
            "If SSL mode fails, test with a mobile hotspot to confirm GP client is functional",
            "Check GP portal logs for the user's connection attempts to identify the block",
            "Document the hotel network details for the travel advisory knowledge base",
        ],
        [
            "Confirm internet access works outside the VPN (browse to an external site)",
            "Try connecting to the alternate GP gateway (gp-backup.contoso.com)",
            "Enable the 'use SSL transport' option in GP client advanced settings",
            "If no GP options work, set up an RDP jump-box session via the web portal as a workaround",
            "Follow up with the user post-travel to ensure normal VPN function resumes",
        ],
    ],
))

# ---------------------------------------------------------------------------
# net-003  Office WiFi extremely slow on Floor 3
# ---------------------------------------------------------------------------
register(ScenarioTemplate(
    scenario_id="net-003",
    category=Category.NETWORK,
    priority=Priority.P3,
    assigned_team=Team.NETWORK,
    needs_escalation=False,
    missing_information=[MissingInfo.AFFECTED_USERS, MissingInfo.TIMESTAMP],
    subjects=[
        "WiFi is extremely slow on Floor 3 — NYC office",
        "Terrible WiFi speeds on 3rd floor since Monday",
        "Floor 3 wireless barely usable",
    ],
    descriptions=[
        "WiFi on Floor 3 in the NYC office has been painfully slow since Monday. Speed tests show "
        "about 5 Mbps down when we usually get 200+. It's affecting everyone sitting in the northeast "
        "corner near the kitchen. Wired connections in the same area are fine. We moved a bunch of "
        "people to this floor last week for the new compliance project so there are probably 40 more "
        "people here now.",
    ],
    next_best_actions=[
        "Check AP utilization and client density on Floor 3 APs via the wireless controller. The "
        "recent headcount increase likely exceeded AP capacity — may need additional access points.",
        "Pull heatmap data from the wireless management console for Floor 3 and compare client "
        "counts before and after the team relocation.",
    ],
    remediation_steps=[
        [
            "Log into the wireless controller and check Floor 3 AP utilization metrics",
            "Review client-count-per-AP to identify overloaded access points",
            "Check for RF interference using a spectrum analysis if APs aren't overloaded",
            "Add temporary access points in the high-density area if capacity is the issue",
            "Rebalance channel assignments across Floor 3 APs",
            "Monitor performance for 24 hours and confirm with affected users",
        ],
        [
            "Pull wireless heatmap for Floor 3 from the management console",
            "Compare current client counts against pre-relocation baseline",
            "Check if band steering is pushing too many clients to 2.4 GHz",
            "Request facilities to install additional AP drops in the northeast section",
            "Adjust AP power levels to reduce co-channel interference",
        ],
    ],
))

# ---------------------------------------------------------------------------
# net-004  WiFi not working in Singapore office after renovation
# ---------------------------------------------------------------------------
register(ScenarioTemplate(
    scenario_id="net-004",
    category=Category.NETWORK,
    priority=Priority.P2,
    assigned_team=Team.NETWORK,
    needs_escalation=True,
    missing_information=[MissingInfo.AFFECTED_USERS, MissingInfo.CONFIGURATION_DETAILS],
    subjects=[
        "Singapore office — WiFi completely down after renovation",
        "No wireless connectivity in SG office post-renovation",
    ],
    descriptions=[
        "The Singapore office completed its renovation over the weekend and WiFi is completely down "
        "as of Monday morning. About 120 people are affected. The contractors may have disconnected "
        "cabling to the APs during the remodel. Wired ports in the new open-plan area aren't working "
        "either. People are using phone hotspots but it's not sustainable — we have regulatory "
        "deadlines this week and need access to internal systems.",
        "WiFi in the Singapore office has been out since we moved back in after the renovation. None "
        "of the access points appear to be powered on (no LED indicators). The local facilities team "
        "says the network closet was relocated as part of the renovation. We need this resolved "
        "urgently — 120+ staff are effectively offline.",
    ],
    next_best_actions=[
        "Dispatch Singapore on-site support to verify physical cabling from the relocated network "
        "closet to the AP locations. Escalate to the regional network team for immediate remediation.",
    ],
    remediation_steps=[
        [
            "Contact Singapore on-site facilities to gain access to the relocated network closet",
            "Verify patch panel connections from the closet to the floor AP locations",
            "Check switch port status — confirm APs are receiving PoE power",
            "Re-patch and re-cable any disconnected AP runs",
            "Bring APs back online and verify they register with the wireless controller",
            "Confirm wireless coverage across the renovated floor with affected users",
        ],
        [
            "Engage the renovation contractor to provide updated cabling documentation",
            "Have Singapore on-site support trace cable runs from the new network closet",
            "Verify PoE budget on the switch — ensure it can power all reconnected APs",
            "Re-provision AP configurations if they were factory-reset during the move",
            "Perform a post-restoration wireless survey to validate coverage",
        ],
    ],
))

# ---------------------------------------------------------------------------
# net-005  DNS resolution failing for internal domains
# ---------------------------------------------------------------------------
register(ScenarioTemplate(
    scenario_id="net-005",
    category=Category.NETWORK,
    priority=Priority.P2,
    assigned_team=Team.NETWORK,
    needs_escalation=False,
    missing_information=[MissingInfo.ERROR_MESSAGE, MissingInfo.AFFECTED_SYSTEM],
    subjects=[
        "Can't resolve internal domains — DNS lookup failures",
        "Internal DNS broken — nslookup returns SERVFAIL",
    ],
    descriptions=[
        "Since about 9am EST I've been unable to resolve any *.contoso.local addresses. nslookup "
        "returns SERVFAIL for everything internal but public DNS (google.com etc.) resolves fine. "
        "I'm on the NYC corporate network, Floor 12. Multiple colleagues are reporting the same "
        "issue. We can't access internal wikis, Git repos, or the HR portal.",
        "Internal DNS seems completely broken for our floor. I get 'DNS name does not exist' for "
        "things like jira.contoso.local and git.contoso.local. External sites load fine. I've "
        "tried flushing my DNS cache — no change. At least 10 people near me have the same problem.",
    ],
    next_best_actions=[
        "Check the health of internal DNS servers and verify the contoso.local forward lookup zone "
        "is loaded and responding. Check if a recent change or patch affected the DNS service.",
        "Verify DNS server assignments via DHCP for the affected subnet and test resolution "
        "directly against each DNS server to isolate the failing node.",
    ],
    remediation_steps=[
        [
            "Identify which DNS servers are assigned to the affected subnet via DHCP",
            "Test resolution against each DNS server individually using nslookup/dig",
            "Check DNS service status on the failing server(s)",
            "Restart the DNS service or failover to a healthy secondary",
            "Flush DNS caches on affected clients after the fix",
            "Monitor DNS query success rates for the next hour",
        ],
        [
            "Check the DNS server event logs for zone load errors or replication failures",
            "Verify AD-integrated DNS zone replication status between domain controllers",
            "If a specific DNS server is down, remove it from the DHCP scope options temporarily",
            "Restart the DNS Server service and force a zone reload",
            "Confirm resolution works from multiple affected clients",
        ],
    ],
))

# ---------------------------------------------------------------------------
# net-006  Can't reach internal app through VPN
# ---------------------------------------------------------------------------
register(ScenarioTemplate(
    scenario_id="net-006",
    category=Category.NETWORK,
    priority=Priority.P2,
    assigned_team=Team.NETWORK,
    needs_escalation=False,
    missing_information=[MissingInfo.AFFECTED_SYSTEM, MissingInfo.STEPS_TO_REPRODUCE],
    subjects=[
        "Internal app unreachable over VPN — works in office",
        "Can't access risk dashboard through GlobalProtect",
        "VPN connected but internal site won't load",
    ],
    descriptions=[
        "I'm connected to GlobalProtect and can reach most internal sites but the risk management "
        "dashboard at risk.contoso.local just times out. It works fine when I'm in the office on "
        "the wired network. I've tried from my home connection and a coffee shop — same behavior. "
        "Other internal tools like Jira and Confluence work fine over VPN.",
        "VPN shows connected and I can ping most internal servers, but one specific application "
        "(the real-time risk dashboard) won't load. My manager says it worked over VPN last week. "
        "Wondering if a firewall rule changed or if the app moved to a different network segment.",
    ],
    next_best_actions=[
        "Check the split-tunnel configuration to verify the risk dashboard's subnet is included in "
        "the VPN routes. Also verify firewall rules for VPN-sourced traffic to that application.",
        "Trace the route from the VPN address pool to the risk dashboard server to find where "
        "traffic is being dropped.",
    ],
    remediation_steps=[
        [
            "Verify the user's VPN connection and assigned IP address",
            "Check the GP split-tunnel policy for the risk dashboard's destination subnet",
            "Review firewall rules for traffic from the VPN address pool to the app server",
            "Test connectivity using traceroute from a VPN-connected test device",
            "Add the missing route or firewall rule if identified",
            "Confirm the user can reach the application after the change",
        ],
        [
            "Check if the risk dashboard was recently migrated to a new subnet",
            "Verify DNS resolution for risk.contoso.local from the VPN DNS servers",
            "Review recent firewall change logs for rules affecting the app's IP range",
            "If a split-tunnel change is needed, submit a change request and apply during window",
            "Provide the user with a temporary full-tunnel profile as a workaround",
        ],
    ],
))

# ---------------------------------------------------------------------------
# net-007  Firewall rule request for new application
# ---------------------------------------------------------------------------
register(ScenarioTemplate(
    scenario_id="net-007",
    category=Category.NETWORK,
    priority=Priority.P4,
    assigned_team=Team.NETWORK,
    needs_escalation=False,
    missing_information=[
        MissingInfo.CONFIGURATION_DETAILS,
        MissingInfo.BUSINESS_IMPACT,
        MissingInfo.AFFECTED_SYSTEM,
    ],
    subjects=[
        "Firewall rule request — new vendor integration",
        "Need firewall ports opened for new application deployment",
    ],
    descriptions=[
        "We're deploying a new market-data feed from Reuters and need firewall rules opened. The "
        "app team says it needs TCP 8443 and 9092 outbound to 203.0.113.0/24 from the app servers "
        "in the NYC DMZ. We also need inbound on TCP 443 from their callback IPs. Go-live is "
        "scheduled for next month so no rush, but I wanted to get the request in early. I'll attach "
        "the full network requirements doc once the vendor sends the final version.",
    ],
    next_best_actions=[
        "Request the complete network requirements document including source/destination IPs, ports, "
        "protocols, and business justification. Queue the change for the next CAB review.",
    ],
    remediation_steps=[
        [
            "Collect the full network requirements from the application team and vendor",
            "Verify the requested flows against the security policy (no overly broad rules)",
            "Submit the firewall change request through the CAB process",
            "Implement the rules in the staging firewall for testing",
            "Coordinate with the app team to validate connectivity in staging",
            "Promote rules to production after successful testing and CAB approval",
        ],
        [
            "Review the vendor's network requirements document for completeness",
            "Cross-check requested external IPs against threat intelligence feeds",
            "Draft firewall rule specifications and submit for security review",
            "Schedule implementation during the next maintenance window",
            "Test end-to-end connectivity with the vendor after rule deployment",
        ],
    ],
))

# ---------------------------------------------------------------------------
# net-008  Video calls constantly dropping — latency spikes
# ---------------------------------------------------------------------------
register(ScenarioTemplate(
    scenario_id="net-008",
    category=Category.NETWORK,
    priority=Priority.P2,
    assigned_team=Team.NETWORK,
    needs_escalation=False,
    missing_information=[MissingInfo.NETWORK_LOCATION, MissingInfo.TIMESTAMP],
    subjects=[
        "Video calls keep dropping — massive latency spikes",
        "Teams and Zoom calls freezing with high latency",
    ],
    descriptions=[
        "For the past three days my video calls (both Teams and Zoom) have been basically unusable. "
        "The call quality report in Teams shows latency spikes up to 800ms and packet loss around "
        "12%. I'm in the NYC office on the wired network. It happens in every meeting, usually "
        "within the first 5 minutes. Audio cuts out, video freezes, and sometimes I get dropped "
        "entirely. I've missed two client calls because of this and it's really impacting my work.",
        "Constant quality issues on video conferences. Latency goes through the roof mid-call and "
        "I end up having to dial in by phone instead. This has been going on since Wednesday. I'm "
        "hardwired on Floor 5 in NYC. My colleagues in London say the calls are fine on their end.",
    ],
    next_best_actions=[
        "Run a network path analysis from the user's switch port to the Teams/Zoom cloud endpoints. "
        "Check for QoS policy enforcement and look for congestion on the uplink.",
        "Pull Teams call quality dashboard data for the user and correlate latency spikes with "
        "network utilization on the Floor 5 switch uplinks.",
    ],
    remediation_steps=[
        [
            "Pull Teams Call Quality Dashboard data for the affected user's recent calls",
            "Identify the network hop where latency is introduced using traceroute/MTR",
            "Check switch port error counters and uplink utilization on the user's floor",
            "Verify QoS markings are applied and honored for real-time media traffic",
            "If uplink congestion, evaluate traffic shaping policies or upgrade the link",
        ],
        [
            "Review network monitoring for congestion patterns on the NYC internet breakout",
            "Check if a recent change (e.g., backup schedule) is saturating the link during work hours",
            "Verify DSCP markings for Teams media traffic through the network path",
            "Test from a different port/floor to isolate whether the issue is localized",
            "Engage the ISP if the congestion point is beyond the edge firewall",
        ],
    ],
))

# ---------------------------------------------------------------------------
# net-009  Teams call quality terrible from London office
# ---------------------------------------------------------------------------
register(ScenarioTemplate(
    scenario_id="net-009",
    category=Category.NETWORK,
    priority=Priority.P3,
    assigned_team=Team.NETWORK,
    needs_escalation=False,
    missing_information=[MissingInfo.AFFECTED_USERS, MissingInfo.ENVIRONMENT_DETAILS],
    subjects=[
        "Teams call quality awful from London office",
        "London office — constant audio breakup on Teams calls",
    ],
    descriptions=[
        "Multiple people in the London office are complaining about Teams call quality. Audio keeps "
        "breaking up and screen sharing is super laggy. It seems to be worse in the afternoons (UK "
        "time) when we have overlapping meetings with the NYC team. We're not sure if it's our "
        "local internet or the WAN connection. The London office has about 800 people and we've "
        "grown a lot in the last quarter.",
    ],
    next_best_actions=[
        "Check WAN utilization between London and the nearest Microsoft Teams relay. Review QoS "
        "policies on the London internet breakout circuit and check for bandwidth saturation "
        "during peak hours.",
    ],
    remediation_steps=[
        [
            "Review London office internet breakout utilization during peak afternoon hours",
            "Pull Teams CQD data filtered to London office users for the past week",
            "Check if Teams media traffic is being routed optimally (local breakout vs. backhauled)",
            "Verify QoS policies are correctly applied on the London edge devices",
            "If bandwidth is the bottleneck, engage procurement for a circuit upgrade",
        ],
        [
            "Analyze Teams network assessment tool results from London office endpoints",
            "Check if split-tunnel VPN is configured for Teams traffic (Office 365 optimize category)",
            "Review SD-WAN policy to ensure real-time traffic gets priority over bulk data",
            "Test call quality during off-peak hours to confirm the correlation with congestion",
            "Implement traffic shaping for non-critical applications during business hours",
        ],
    ],
))

# ---------------------------------------------------------------------------
# net-010  Proxy blocking legitimate website needed for work
# ---------------------------------------------------------------------------
register(ScenarioTemplate(
    scenario_id="net-010",
    category=Category.NETWORK,
    priority=Priority.P3,
    assigned_team=Team.NETWORK,
    needs_escalation=False,
    missing_information=[MissingInfo.BUSINESS_IMPACT, MissingInfo.SCREENSHOT_OR_ATTACHMENT],
    subjects=[
        "Web proxy blocking a site I need for work",
        "Zscaler blocking legitimate vendor portal",
        "Can't access third-party research site — proxy block",
    ],
    descriptions=[
        "I'm trying to access our new vendor's documentation portal at docs.acmefintech.io and "
        "Zscaler is blocking it as 'Uncategorized'. I need this for the integration project that's "
        "due end of month. I've attached a screenshot of the block page. Can we get this "
        "whitelisted? My manager has approved the access.",
        "Zscaler is blocking access to a financial research site (www.capitaliq.com/reports) that "
        "the entire research team needs daily. It was working until yesterday. The block page says "
        "'Security Risk' but this is a well-known platform we've been using for years. About 15 "
        "analysts are affected.",
    ],
    next_best_actions=[
        "Review the Zscaler URL categorization for the blocked site and submit a recategorization "
        "request if appropriate. Add a temporary allow-list entry if business need is urgent.",
    ],
    remediation_steps=[
        [
            "Verify the blocked URL and review the Zscaler block reason/category",
            "Check if the site was recently recategorized by Zscaler's threat intelligence",
            "If the site is legitimate, submit a URL recategorization request to Zscaler",
            "Add a temporary allow-list entry for the URL with manager approval documented",
            "Confirm the user can access the site after the exception is applied",
        ],
        [
            "Review the Zscaler block log for the specific URL and user",
            "Cross-reference the site against the approved vendor and tool list",
            "If approved, create a URL exception in the Zscaler admin portal",
            "Notify the security team of the exception for their records",
            "Monitor access logs for the allowed URL for any anomalous activity",
        ],
    ],
))

# ---------------------------------------------------------------------------
# net-011  Entire floor network down
# ---------------------------------------------------------------------------
register(ScenarioTemplate(
    scenario_id="net-011",
    category=Category.NETWORK,
    priority=Priority.P1,
    assigned_team=Team.NETWORK,
    needs_escalation=True,
    missing_information=[MissingInfo.AFFECTED_USERS, MissingInfo.TIMESTAMP],
    subjects=[
        "URGENT — entire Floor 8 has no network",
        "Floor 8 NYC — complete network outage",
    ],
    descriptions=[
        "Floor 8 in the NYC office has completely lost network connectivity — both wired and "
        "wireless. Nothing works. There are approximately 150 people on this floor including the "
        "derivatives trading desk. We've been down for about 20 minutes. No one on the floor can "
        "access anything. The MDF on this floor had some electrical work done over the weekend — "
        "could be related.",
        "ALL of Floor 8 just went dark network-wise. WiFi gone, wired dead, no link lights on any "
        "desk ports. This floor has the FX trading team and they are completely offline. This is "
        "costing us real money every minute. Need someone here NOW.",
    ],
    next_best_actions=[
        "Immediately dispatch on-site network support to the Floor 8 MDF. Check the distribution "
        "switch and UPS status — likely related to the weekend electrical work.",
    ],
    remediation_steps=[
        [
            "Dispatch on-site network engineer to the Floor 8 MDF immediately",
            "Check power status on the distribution switch and UPS in the MDF",
            "Verify the electrical work didn't trip a breaker or disconnect switch power",
            "If switch is powered off, restore power and monitor boot sequence",
            "Verify all access-layer switches re-establish uplinks to the distribution switch",
            "Confirm connectivity restoration with users on the floor",
        ],
        [
            "Check network monitoring for the Floor 8 distribution switch status",
            "If switch is unreachable, dispatch engineer to physically inspect the MDF",
            "Assess whether the UPS was affected by the weekend electrical work",
            "If hardware failure, activate the spare switch and migrate connections",
            "Notify affected business units of status and estimated restoration time",
            "Conduct post-incident review of the electrical work change process",
        ],
    ],
))

# ---------------------------------------------------------------------------
# net-012  Intermittent network drops affecting trading floor
# ---------------------------------------------------------------------------
register(ScenarioTemplate(
    scenario_id="net-012",
    category=Category.NETWORK,
    priority=Priority.P1,
    assigned_team=Team.NETWORK,
    needs_escalation=True,
    missing_information=[MissingInfo.REPRODUCTION_FREQUENCY, MissingInfo.TIMESTAMP],
    subjects=[
        "Trading floor network dropping intermittently — critical",
        "Intermittent outages on NYC trading floor network",
    ],
    descriptions=[
        "The trading floor (Floor 2, NYC) is experiencing intermittent network drops. Connections "
        "go down for 30-60 seconds then come back, happening every 10-15 minutes. This has been "
        "going on since market open at 9:30am. The Bloomberg terminals lose their feeds each time "
        "and the order management system disconnects. We've had three partial outages so far today. "
        "This is directly impacting trade execution and we're losing money.",
        "Network on the trading floor keeps flapping. Desks are losing connectivity randomly for "
        "about a minute at a time. It's affecting all trading systems — Bloomberg, OMS, and "
        "internal pricing tools. Traders are furious. This started around 9am and has happened "
        "at least 5 times already.",
    ],
    next_best_actions=[
        "Immediately investigate the Floor 2 access and distribution switches for spanning-tree "
        "reconvergence events or link flapping. Check for recent changes and correlate with the "
        "timing of the drops.",
    ],
    remediation_steps=[
        [
            "Check spanning-tree topology change counters on Floor 2 switches",
            "Review switch logs for port flapping or link-state changes",
            "Identify if a specific uplink or switch is the root cause",
            "If a flapping port is found, administratively shut it down to stabilize the network",
            "Investigate the root cause of the flapping (bad cable, failing SFP, or misconfiguration)",
            "Monitor for 30 minutes after remediation to confirm stability",
        ],
        [
            "Pull SNMP traps and syslog from Floor 2 switches for the past 4 hours",
            "Check for duplex mismatches or CRC errors on trunk links",
            "Verify spanning-tree root bridge placement and priority settings",
            "If a rogue device is causing topology changes, isolate it using BPDU guard logs",
            "Stabilize the floor and schedule a full network audit for after market close",
        ],
    ],
))

# ---------------------------------------------------------------------------
# net-013  WAN link between NYC and London degraded
# ---------------------------------------------------------------------------
register(ScenarioTemplate(
    scenario_id="net-013",
    category=Category.NETWORK,
    priority=Priority.P1,
    assigned_team=Team.NETWORK,
    needs_escalation=True,
    missing_information=[MissingInfo.BUSINESS_IMPACT, MissingInfo.TIMESTAMP],
    subjects=[
        "NYC-London WAN link degraded — high latency and packet loss",
        "WAN circuit between NYC and London severely impacted",
        "Cross-Atlantic link performance critical",
    ],
    descriptions=[
        "The WAN link between NYC and London is severely degraded. Latency has gone from the usual "
        "~70ms to over 400ms and we're seeing 8% packet loss. This is impacting cross-office "
        "collaboration, database replication, and the London team's access to NYC-hosted "
        "applications. The degradation started around 2pm GMT. Our monitoring shows both the "
        "primary and backup MPLS circuits are affected.",
        "Something is very wrong with the NYC-London WAN. File transfers that normally take minutes "
        "are timing out. London users can barely access NYC-hosted apps. Our NOC dashboard shows "
        "latency at 5x normal and climbing. Both MPLS circuits appear degraded which suggests a "
        "carrier-side issue.",
    ],
    next_best_actions=[
        "Open a high-priority ticket with the MPLS carrier immediately. Verify whether the issue "
        "is in the carrier backbone by checking latency at each provider hop. Activate the "
        "internet-based VPN backup path if available.",
    ],
    remediation_steps=[
        [
            "Confirm degradation metrics from network monitoring (latency, loss, jitter)",
            "Run traceroute between NYC and London to identify the degraded hop",
            "Open a priority-1 case with the MPLS carrier with traceroute evidence",
            "Activate the backup internet VPN tunnel for critical application traffic",
            "Notify London and NYC teams of the degradation and workaround options",
            "Monitor carrier case for updates and re-test when carrier reports resolution",
        ],
        [
            "Verify both primary and secondary MPLS circuits show degradation",
            "Check carrier status page and contact the account team for known outages",
            "Failover time-sensitive traffic (database replication, trading data) to the backup path",
            "Implement QoS policies to prioritize critical traffic on the degraded link",
            "Coordinate with the carrier until full restoration is confirmed",
        ],
    ],
))

# ---------------------------------------------------------------------------
# net-014  New office subnet needs VLAN configuration
# ---------------------------------------------------------------------------
register(ScenarioTemplate(
    scenario_id="net-014",
    category=Category.NETWORK,
    priority=Priority.P4,
    assigned_team=Team.NETWORK,
    needs_escalation=False,
    missing_information=[MissingInfo.CONFIGURATION_DETAILS, MissingInfo.ENVIRONMENT_DETAILS],
    subjects=[
        "VLAN configuration needed for new office expansion subnet",
        "New subnet setup request — Floor 15 expansion",
    ],
    descriptions=[
        "We're expanding into Floor 15 of the NYC office next quarter and need a new VLAN and "
        "subnet configured. Facilities has confirmed 80 desk drops and 12 AP locations. We need "
        "a standard corporate VLAN with the usual DHCP, DNS, and firewall policies. The network "
        "closet on Floor 15 has been set up with a new access switch but it hasn't been configured "
        "yet. No rush — the move-in date is 8 weeks out.",
    ],
    next_best_actions=[
        "Allocate a /24 subnet from the NYC IP address plan, define the VLAN ID, and create a "
        "network design document for Floor 15. Schedule configuration during a maintenance window.",
    ],
    remediation_steps=[
        [
            "Allocate a new /24 from the NYC IP address management system",
            "Assign a VLAN ID and document it in the network inventory",
            "Configure the access switch with the new VLAN and trunk uplinks",
            "Set up DHCP scope with DNS, gateway, and lease settings",
            "Apply standard firewall policies and ACLs for the new subnet",
            "Test end-to-end connectivity from a device on the new VLAN",
        ],
        [
            "Review the Floor 15 network design requirements with the project team",
            "Provision the subnet, VLAN, and DHCP scope per the standard build template",
            "Configure inter-VLAN routing on the distribution switch",
            "Deploy and test wireless SSID mapping on the Floor 15 APs",
            "Conduct a walkthrough test with facilities before the move-in date",
        ],
    ],
))

# ---------------------------------------------------------------------------
# net-015  WiFi guest network not working for client visitors
# ---------------------------------------------------------------------------
register(ScenarioTemplate(
    scenario_id="net-015",
    category=Category.NETWORK,
    priority=Priority.P3,
    assigned_team=Team.NETWORK,
    needs_escalation=False,
    missing_information=[MissingInfo.ERROR_MESSAGE, MissingInfo.NETWORK_LOCATION],
    subjects=[
        "Guest WiFi not working — clients visiting today",
        "Contoso-Guest SSID won't connect for visitors",
        "Client visitors can't get on guest wireless",
    ],
    descriptions=[
        "We have clients from Goldman visiting our NYC office today for due diligence meetings and "
        "they can't connect to the Contoso-Guest WiFi. They can see the SSID and connect but the "
        "captive portal never loads — they just get 'no internet connection'. I've tried it on my "
        "phone too and same issue. This is pretty embarrassing and the meetings run all day.",
        "Guest WiFi in the NYC office is broken. Visitors can associate with the Contoso-Guest "
        "network but the splash page doesn't come up and there's no internet access. We have "
        "auditors on-site this week who need internet access for their work.",
    ],
    next_best_actions=[
        "Check the guest wireless controller and captive portal service status. Verify the guest "
        "VLAN has internet access and the portal redirect is functioning.",
    ],
    remediation_steps=[
        [
            "Verify the Contoso-Guest SSID is broadcasting and clients can associate",
            "Check the captive portal service/appliance for health and connectivity",
            "Test DNS resolution on the guest VLAN (portal redirect depends on DNS)",
            "Verify the guest VLAN's default gateway and internet access path",
            "Restart the captive portal service if it's unresponsive",
            "Confirm guest internet access with a visitor's device after the fix",
        ],
        [
            "Check if a certificate on the captive portal has expired (common cause)",
            "Verify the DHCP scope for the guest VLAN isn't exhausted",
            "Test the portal redirect URL manually in a browser",
            "If the portal is down, temporarily configure open guest access with MAC registration",
            "Follow up with a permanent fix for the captive portal after business hours",
        ],
    ],
))

# ---------------------------------------------------------------------------
# net-016  Site-to-site VPN tunnel down to vendor
# ---------------------------------------------------------------------------
register(ScenarioTemplate(
    scenario_id="net-016",
    category=Category.NETWORK,
    priority=Priority.P2,
    assigned_team=Team.NETWORK,
    needs_escalation=False,
    missing_information=[MissingInfo.ERROR_MESSAGE, MissingInfo.CONFIGURATION_DETAILS],
    subjects=[
        "Site-to-site VPN to clearing vendor is down",
        "IPsec tunnel to vendor not establishing",
    ],
    descriptions=[
        "Our site-to-site VPN tunnel to ClearStream (our trade clearing vendor) has been down since "
        "approximately 6am EST. The tunnel was stable for months and no changes were made on our "
        "side. The operations team noticed that trade confirmations stopped flowing and traced it "
        "back to the VPN. We need this restored ASAP — unconfirmed trades are piling up and we "
        "have a regulatory obligation to confirm within T+1.",
        "The IPsec tunnel to our clearing partner isn't coming up. Our firewall logs show IKE phase "
        "1 negotiation failures. We haven't changed anything recently. This is blocking all "
        "automated trade settlement and the ops team is having to process manually.",
    ],
    next_best_actions=[
        "Review the firewall IKE logs for specific negotiation failure details. Contact the vendor's "
        "network team to check if they made changes on their end (certificate renewal, IP change).",
    ],
    remediation_steps=[
        [
            "Review firewall VPN logs for IKE phase 1/phase 2 error details",
            "Check if the pre-shared key or certificate has expired",
            "Contact ClearStream's network operations to verify their tunnel configuration",
            "If vendor changed their public IP or proposal settings, update our side to match",
            "Re-establish the tunnel and verify traffic flow with a test transaction",
            "Monitor tunnel stability for the next 24 hours",
        ],
        [
            "Check the firewall for IKE SA status and last successful negotiation timestamp",
            "Verify our public IP hasn't changed (check NAT/ISP status)",
            "Coordinate with the vendor to perform simultaneous tunnel reset on both sides",
            "If IKE parameters drifted, renegotiate and align encryption/hashing proposals",
            "Confirm trade confirmations resume flowing through the restored tunnel",
        ],
    ],
))

# ---------------------------------------------------------------------------
# net-017  DNS propagation delay after migration
# ---------------------------------------------------------------------------
register(ScenarioTemplate(
    scenario_id="net-017",
    category=Category.NETWORK,
    priority=Priority.P3,
    assigned_team=Team.NETWORK,
    needs_escalation=False,
    missing_information=[MissingInfo.AFFECTED_SYSTEM, MissingInfo.AFFECTED_USERS],
    subjects=[
        "DNS still pointing to old IP after server migration",
        "DNS propagation not complete — some users hitting old server",
    ],
    descriptions=[
        "We migrated the internal expense reporting app to a new server over the weekend and "
        "updated the DNS A record on Saturday. It's now Monday afternoon and some users are still "
        "resolving the old IP. NYC office seems fine but London and Singapore are still hitting the "
        "old server. The TTL was set to 3600 so it should have propagated by now. The old server "
        "is scheduled to be decommissioned on Wednesday.",
        "After moving the expense app to new infrastructure, DNS changes haven't fully propagated. "
        "Some people get the new server, others get the old one. It's inconsistent and it's been "
        "over 48 hours since the change.",
    ],
    next_best_actions=[
        "Check DNS replication status between the NYC, London, and Singapore DNS servers. Verify "
        "the A record is consistent across all regional DNS servers and flush any stale caches.",
    ],
    remediation_steps=[
        [
            "Query each regional DNS server directly to check the current A record value",
            "Verify AD DNS replication is healthy between all domain controller sites",
            "Force replication for the affected zone if replication is lagging",
            "Flush DNS resolver caches on the London and Singapore DNS servers",
            "Advise affected users to run ipconfig /flushdns on their machines",
            "Delay the old server decommission until propagation is fully confirmed",
        ],
        [
            "Check DNS zone replication status in Active Directory Sites and Services",
            "Verify the site link schedule allows timely replication to London and Singapore",
            "If replication is broken, troubleshoot AD replication independently",
            "Manually create the updated record on lagging servers as a temporary fix",
            "Monitor resolution from all three offices over the next 24 hours",
        ],
    ],
))

# ---------------------------------------------------------------------------
# net-018  Bandwidth throttling on specific applications
# ---------------------------------------------------------------------------
register(ScenarioTemplate(
    scenario_id="net-018",
    category=Category.NETWORK,
    priority=Priority.P3,
    assigned_team=Team.NETWORK,
    needs_escalation=False,
    missing_information=[MissingInfo.AFFECTED_SYSTEM, MissingInfo.BUSINESS_IMPACT],
    subjects=[
        "Specific apps seem to be bandwidth-throttled",
        "Slow downloads from cloud storage — possible throttling",
    ],
    descriptions=[
        "Downloads from our Azure Blob Storage are extremely slow — topping out at about 2 Mbps "
        "when I should be getting much more. Regular internet browsing and speed tests show normal "
        "speeds (200+ Mbps). A couple of people on the data analytics team have noticed the same "
        "thing. We're trying to pull large datasets for the quarterly risk model refresh and it's "
        "taking hours instead of minutes. Feels like something is rate-limiting our Azure traffic.",
        "Our team has been experiencing throttled speeds when accessing Azure-hosted resources. "
        "Large file downloads that used to take 5 minutes now take over an hour. We suspect a QoS "
        "policy or proxy rule is limiting bandwidth to Azure endpoints.",
    ],
    next_best_actions=[
        "Review QoS and traffic-shaping policies on the edge firewall and proxy for Azure endpoint "
        "traffic. Check if a recent policy change is rate-limiting cloud storage connections.",
    ],
    remediation_steps=[
        [
            "Identify the traffic path from the user's workstation to Azure Blob Storage",
            "Check Zscaler/proxy policies for any bandwidth limits on Azure endpoints",
            "Review firewall QoS rules for traffic to Azure IP ranges",
            "If a throttle is found, evaluate whether it can be removed or the limit raised",
            "Test download speeds after the policy adjustment",
        ],
        [
            "Run a network path analysis to Azure Blob endpoints from the affected subnet",
            "Check if Azure traffic is being backhauled through the proxy vs. direct breakout",
            "Review recent QoS or SD-WAN policy changes that may affect cloud traffic",
            "Configure a direct breakout for Azure storage traffic if currently proxied",
            "Validate with the data team that transfer speeds have returned to normal",
        ],
    ],
))

# ---------------------------------------------------------------------------
# net-019  Network printer unreachable from new subnet
# ---------------------------------------------------------------------------
register(ScenarioTemplate(
    scenario_id="net-019",
    category=Category.NETWORK,
    priority=Priority.P3,
    assigned_team=Team.NETWORK,
    needs_escalation=False,
    missing_information=[MissingInfo.DEVICE_INFO, MissingInfo.CONFIGURATION_DETAILS],
    subjects=[
        "Can't print — printer unreachable from new VLAN",
        "Network printer not accessible after subnet move",
        "Printing broken since we moved to Floor 10",
    ],
    descriptions=[
        "Our team moved to Floor 10 last week and we can't reach the shared printer (HP LaserJet "
        "on Floor 9). IT set us up on a new VLAN for Floor 10 but printing just times out. I can "
        "ping everything else on the Floor 9 network. The printer IP is 10.20.9.50 and we're now "
        "on the 10.20.10.0/24 subnet. About 30 people on our team need this printer.",
        "Since the move to Floor 10 we have no access to our department printer. Print jobs just "
        "queue up and never print. The printer is still on Floor 9. I'm guessing it's a routing or "
        "firewall thing between the old and new VLANs.",
    ],
    next_best_actions=[
        "Check inter-VLAN routing and firewall ACLs between the Floor 10 subnet (10.20.10.0/24) "
        "and the printer's subnet (10.20.9.0/24). Add the necessary permit rules for print traffic.",
    ],
    remediation_steps=[
        [
            "Verify the user can ping the printer IP from the new subnet",
            "Check ACLs on the distribution switch for traffic between 10.20.10.0/24 and 10.20.9.0/24",
            "Review firewall rules for print protocols (TCP 9100, IPP 631) between the VLANs",
            "Add permit rules for print traffic from the new subnet to the printer",
            "Test printing from a device on the new VLAN after the rule change",
        ],
        [
            "Confirm the printer is still reachable on its existing VLAN (ping from Floor 9)",
            "Check if the new VLAN has inter-VLAN routing enabled on the core switch",
            "Verify no ACL is blocking TCP 9100 or IPP traffic from the new subnet",
            "Add the required inter-VLAN permit rules and test",
            "Update the print server configuration if the driver uses a hostname that doesn't resolve",
        ],
    ],
))

# ---------------------------------------------------------------------------
# net-020  Remote desktop extremely slow over VPN
# ---------------------------------------------------------------------------
register(ScenarioTemplate(
    scenario_id="net-020",
    category=Category.NETWORK,
    priority=Priority.P3,
    assigned_team=Team.NETWORK,
    needs_escalation=False,
    missing_information=[MissingInfo.NETWORK_LOCATION, MissingInfo.DEVICE_INFO],
    subjects=[
        "Remote desktop painfully slow over VPN",
        "RDP session lag makes working from home impossible",
    ],
    descriptions=[
        "Working from home and my Remote Desktop session to my office workstation is nearly "
        "unusable. There's a 2-3 second delay on every keystroke and mouse click. The VPN is "
        "connected and general internet is fine — I can browse and stream video no problem. But "
        "RDP is crawling. I'm on Verizon FiOS 300/300 at home. This started about a week ago; "
        "before that RDP over VPN was perfectly usable.",
        "RDP lag over VPN has gotten terrible. I type a sentence and it takes 5 seconds to appear. "
        "Screen rendering is awful — lots of artifacts. Didn't used to be this bad. My home "
        "internet speed tests fine. Other VPN traffic (file shares, web apps) seems normal-ish.",
    ],
    next_best_actions=[
        "Check VPN gateway utilization and the user's bandwidth allocation. Verify whether RDP "
        "traffic is being routed through an overloaded path or deprioritized by QoS policies.",
    ],
    remediation_steps=[
        [
            "Have the user run a speed test while connected to VPN to check tunnel throughput",
            "Check VPN gateway load and concurrent session counts",
            "Verify the GP client's configured MTU — fragmentation can kill RDP performance",
            "Test RDP with UDP transport disabled to rule out UDP blocking by the home router",
            "If VPN throughput is the bottleneck, try the user on a less-loaded gateway",
        ],
        [
            "Check if the VPN split-tunnel policy routes RDP traffic optimally",
            "Verify the user's home router isn't applying SIP ALG or other traffic manipulation",
            "Reduce RDP session color depth and disable visual effects to lower bandwidth needs",
            "Test with an alternate VPN protocol (SSL vs. IPsec) if available",
            "If persistent, evaluate providing the user with a company-managed hotspot",
        ],
    ],
))

# ---------------------------------------------------------------------------
# net-021  Zscaler proxy causing certificate errors
# ---------------------------------------------------------------------------
register(ScenarioTemplate(
    scenario_id="net-021",
    category=Category.NETWORK,
    priority=Priority.P2,
    assigned_team=Team.NETWORK,
    needs_escalation=False,
    missing_information=[MissingInfo.AFFECTED_SYSTEM, MissingInfo.ERROR_MESSAGE],
    subjects=[
        "Zscaler causing SSL certificate errors on multiple sites",
        "Certificate errors everywhere — Zscaler inspection issue",
    ],
    descriptions=[
        "Since this morning I'm getting certificate errors on almost every HTTPS site I visit. The "
        "browser shows 'NET::ERR_CERT_AUTHORITY_INVALID' and the certificate issuer shows as "
        "Zscaler. This was working fine yesterday. I can't access Azure DevOps, our internal "
        "portals, or even external banking sites. I've checked and the Zscaler root cert is still "
        "in my trusted store. This is blocking all my work.",
        "Getting cert errors everywhere through Zscaler. Chrome and Edge both show the certificate "
        "is issued by 'Zscaler Intermediate Root CA' but say it's not trusted. Other people in my "
        "team are NOT having this issue so it might be specific to my machine, but I haven't "
        "changed anything.",
    ],
    next_best_actions=[
        "Verify the Zscaler root and intermediate CA certificates are properly installed in the "
        "user's machine certificate store. Check if a recent Windows update or GPO change removed "
        "or invalidated the Zscaler certificate chain.",
    ],
    remediation_steps=[
        [
            "Check the user's certificate store for the Zscaler root and intermediate CAs",
            "Verify the certificates haven't expired or been revoked",
            "Re-push the Zscaler root certificate via GPO or Intune if missing",
            "Run gpupdate /force and restart the browser to pick up the new cert",
            "Confirm HTTPS sites load without certificate errors",
        ],
        [
            "Compare the user's Zscaler certificate chain with a working machine",
            "Check if a Windows update removed third-party root certificates",
            "Manually install the Zscaler root CA from the network share if GPO is delayed",
            "Verify the Zscaler client connector is up-to-date and functioning",
            "If widespread, check whether Zscaler renewed their intermediate CA recently",
        ],
    ],
))

# ---------------------------------------------------------------------------
# net-022  WiFi roaming between floors drops connection
# ---------------------------------------------------------------------------
register(ScenarioTemplate(
    scenario_id="net-022",
    category=Category.NETWORK,
    priority=Priority.P3,
    assigned_team=Team.NETWORK,
    needs_escalation=False,
    missing_information=[MissingInfo.DEVICE_INFO, MissingInfo.REPRODUCTION_FREQUENCY],
    subjects=[
        "WiFi drops when moving between floors",
        "Wireless connection lost when roaming between floors",
        "WiFi roaming broken — have to reconnect on every floor",
    ],
    descriptions=[
        "Every time I walk from Floor 5 to Floor 6 for meetings, my WiFi drops completely and I "
        "have to wait 30-60 seconds for it to reconnect. My Teams calls drop every time. I'm "
        "carrying my laptop between meeting rooms a lot and this is really disruptive. In the old "
        "office this was seamless. I'm using a Dell Latitude with the Intel AX211 WiFi adapter.",
        "WiFi roaming in the NYC office is terrible. Moving between any two floors causes a full "
        "disconnect and reconnect. It takes about a minute to get back online. Shouldn't this be "
        "seamless? I'm on the Contoso-Corp SSID.",
    ],
    next_best_actions=[
        "Check the wireless controller's roaming configuration — verify 802.11r (fast BSS "
        "transition) and 802.11k/v are enabled. Check if APs on adjacent floors are on the same "
        "mobility group.",
    ],
    remediation_steps=[
        [
            "Verify 802.11r/k/v fast roaming is enabled on the wireless controller",
            "Check that APs on adjacent floors are in the same RF mobility group",
            "Review the wireless client's roaming aggressiveness settings",
            "Verify VLAN assignments are consistent across floor boundaries",
            "Test roaming with a reference device to isolate client vs. infrastructure issues",
        ],
        [
            "Audit AP placement near stairwells and elevators for inter-floor coverage overlap",
            "Ensure the Contoso-Corp SSID has fast roaming (802.11r) enabled",
            "Check if the Intel AX211 driver is up-to-date (known roaming bugs in older versions)",
            "Adjust AP transmit power to provide adequate overlap between floors",
            "Test after changes and gather feedback from the user over a week",
        ],
    ],
))

# ---------------------------------------------------------------------------
# net-023  Network port dead at desk — no link light
# ---------------------------------------------------------------------------
register(ScenarioTemplate(
    scenario_id="net-023",
    category=Category.NETWORK,
    priority=Priority.P3,
    assigned_team=Team.NETWORK,
    needs_escalation=False,
    missing_information=[MissingInfo.NETWORK_LOCATION, MissingInfo.DEVICE_INFO],
    subjects=[
        "Network port at my desk is dead — no link light",
        "Ethernet port not working — desk 7-142",
        "Wired connection dead at my assigned desk",
    ],
    descriptions=[
        "My Ethernet port at desk 7-142 (Floor 7, NYC) isn't working. No link light on either end "
        "when I plug in. I've tried two different cables and tested my laptop on another port down "
        "the hall — laptop works fine. I think this port might just be dead or disconnected in the "
        "patch panel. I need the wired connection because WiFi is too spotty for my Bloomberg "
        "terminal.",
        "Wired network at my desk doesn't work — no lights on the wall jack or my laptop when "
        "connected. Tried different cables. The port next to it works fine. Can someone check if "
        "this port is patched in?",
    ],
    next_best_actions=[
        "Check the patch panel in the Floor 7 network closet to verify desk port 7-142 is patched "
        "to an active switch port. Re-patch or replace the cable run if disconnected.",
    ],
    remediation_steps=[
        [
            "Identify the patch panel port corresponding to desk jack 7-142 using the cable map",
            "Verify the patch panel port is connected to an active switch port",
            "If not patched, run a patch cable from the panel port to an available switch port",
            "Enable the switch port and assign it to the correct VLAN",
            "Test connectivity from the desk with the user's device",
        ],
        [
            "Check the cable map for desk 7-142 to find the patch panel location",
            "Tone-test the cable run from the desk to the closet if the mapping is unclear",
            "If the cable run is bad, schedule a re-pull with facilities",
            "As a temporary fix, move the user to an adjacent working desk port",
            "Update the cable documentation after the repair",
        ],
    ],
))

# ---------------------------------------------------------------------------
# net-024  DHCP exhaustion on office subnet
# ---------------------------------------------------------------------------
register(ScenarioTemplate(
    scenario_id="net-024",
    category=Category.NETWORK,
    priority=Priority.P2,
    assigned_team=Team.NETWORK,
    needs_escalation=False,
    missing_information=[MissingInfo.AFFECTED_USERS, MissingInfo.ENVIRONMENT_DETAILS],
    subjects=[
        "Devices can't get IP addresses — DHCP pool exhausted",
        "DHCP exhaustion on Floor 4 subnet — people can't connect",
    ],
    descriptions=[
        "Multiple people on Floor 4 of the NYC office are unable to get IP addresses. Their laptops "
        "show 'No internet — DHCP failed' or they're picking up 169.254.x.x APIPA addresses. It "
        "started around 10am when a large training class of about 50 people arrived with laptops. "
        "Existing staff who were already connected are fine, but anyone who disconnects and "
        "reconnects can't get an IP. Looks like the DHCP pool is full.",
        "Floor 4 can't get network IPs. New connections all fail with APIPA addresses. We think "
        "the training event with 50+ extra laptops ate up the whole DHCP pool. People who were "
        "already connected are okay for now but no new devices can join.",
    ],
    next_best_actions=[
        "Immediately check the DHCP scope utilization for the Floor 4 subnet. Extend the scope, "
        "reduce lease time, or reclaim unused leases to free up addresses.",
    ],
    remediation_steps=[
        [
            "Check DHCP scope utilization for the Floor 4 subnet on the DHCP server",
            "Identify any stale or unused leases that can be reclaimed",
            "Reduce the DHCP lease time temporarily to recycle addresses faster",
            "Expand the scope if the current range is undersized for the floor's capacity",
            "Verify new clients can obtain addresses after the scope is adjusted",
            "Plan a permanent subnet expansion if large events are expected regularly",
        ],
        [
            "Review the DHCP server for the Floor 4 scope — check active vs. available leases",
            "Clear any ghost leases from devices no longer on the network",
            "Add a secondary DHCP range (superscope) to temporarily increase capacity",
            "Set up a separate VLAN for training/guest devices with its own DHCP scope",
            "Confirm affected users can connect after the scope change",
        ],
    ],
))

# ---------------------------------------------------------------------------
# net-025  Multi-WAN failover not working during outage
# ---------------------------------------------------------------------------
register(ScenarioTemplate(
    scenario_id="net-025",
    category=Category.NETWORK,
    priority=Priority.P1,
    assigned_team=Team.NETWORK,
    needs_escalation=True,
    missing_information=[MissingInfo.CONFIGURATION_DETAILS, MissingInfo.TIMESTAMP],
    subjects=[
        "WAN failover didn't trigger during ISP outage — all offices down",
        "Multi-WAN failover failure — no automatic switchover",
        "Backup WAN link did not activate during primary outage",
    ],
    descriptions=[
        "Our primary ISP went down at approximately 7:15am EST and the automatic WAN failover to "
        "our backup circuit did NOT trigger. The NYC office was without internet for 45 minutes "
        "until we manually switched over. The SD-WAN appliance should have failed over "
        "automatically within 30 seconds — this is a critical failure in our DR design. We need to "
        "understand why the failover didn't work and fix it before the primary ISP goes down again. "
        "The trading desk lost all external connectivity during the outage.",
        "This morning the primary WAN went down and the supposed automatic failover to our backup "
        "link never happened. The NOC had to manually re-route traffic which took nearly an hour. "
        "The whole office was offline. This is supposed to be seamless — we pay for two circuits "
        "specifically for this. Something is seriously wrong with our failover configuration.",
    ],
    next_best_actions=[
        "Immediately investigate the SD-WAN failover configuration and health-check probes. "
        "Determine why the backup link was not activated and conduct a controlled failover test "
        "after hours to validate the fix.",
    ],
    remediation_steps=[
        [
            "Review SD-WAN appliance logs from the time of the outage for failover events",
            "Check the health-check probe configuration for the primary and backup links",
            "Verify the backup circuit is active and passing traffic (test independently)",
            "Fix the failover trigger — probe target, threshold, or timer misconfiguration",
            "Schedule a controlled failover test during the next maintenance window",
            "Document findings and update the DR runbook with corrective actions",
        ],
        [
            "Pull logs from the SD-WAN controller for the failover event timeline",
            "Check if the backup ISP link had its own undetected issue (partially up but degraded)",
            "Review routing table changes during the outage to trace the failover logic",
            "Reconfigure health-check probes to use multiple diverse targets",
            "Conduct a failover test and validate sub-30-second switchover",
            "Brief the incident to management with root cause and remediation plan",
        ],
    ],
))

# ---------------------------------------------------------------------------
# net-026  Recurring VPN issue — references old ticket
# ---------------------------------------------------------------------------
register(ScenarioTemplate(
    scenario_id="net-026",
    category=Category.NETWORK,
    priority=Priority.P2,
    assigned_team=Team.NETWORK,
    needs_escalation=False,
    missing_information=[MissingInfo.PREVIOUS_TICKET_ID, MissingInfo.SCREENSHOT_OR_ATTACHMENT],
    subjects=[
        "VPN dropping again — same issue as my previous ticket",
        "VPN disconnects are back — this was fixed before but it's happening again",
        "Recurring VPN timeout issue — had a ticket for this last quarter",
    ],
    descriptions=[
        "My VPN keeps dropping every 30-45 minutes, which is exactly what was happening before. "
        "IT fixed it last time — something about a split-tunnel configuration — but the issue has "
        "come back. I don't have the old ticket number but it was sometime in February. I didn't "
        "grab a screenshot of the VPN client error because it reconnects automatically and the "
        "error disappears. London office, working from home today.",
        "The VPN disconnect issue I reported months ago is back. I lose connectivity every hour "
        "or so and have to manually reconnect. There was a previous ticket where the network team "
        "adjusted something on the gateway, but I can't find the reference. The GlobalProtect "
        "client just shows 'Reconnecting...' briefly but I haven't managed to capture the error "
        "state in a screenshot.",
    ],
    next_best_actions=[
        "Search for the user's previous VPN-related tickets to review the prior fix. Check VPN "
        "gateway logs and client configuration for recurring timeout issues.",
    ],
    remediation_steps=[
        [
            "Search the ticketing system for the user's prior VPN disconnect tickets",
            "Review the previous resolution to determine if the same fix needs to be reapplied",
            "Check VPN gateway logs for the user's session disconnect patterns",
            "Ask the user to export the GlobalProtect or VPN client log after the next disconnect",
            "Reapply the configuration fix or implement a permanent solution",
            "Monitor the user's VPN session stability for the next 48 hours",
        ],
    ],
))

# ---------------------------------------------------------------------------
# net-027  WiFi issue reported on behalf of someone else
# ---------------------------------------------------------------------------
register(ScenarioTemplate(
    scenario_id="net-027",
    category=Category.NETWORK,
    priority=Priority.P3,
    assigned_team=Team.NETWORK,
    needs_escalation=False,
    missing_information=[MissingInfo.CONTACT_INFO, MissingInfo.NETWORK_LOCATION],
    subjects=[
        "Reporting WiFi issue for a colleague who can't submit a ticket",
        "WiFi problem on behalf of another employee — they have no connectivity",
        "Submitting for someone else — their WiFi is completely down",
    ],
    descriptions=[
        "I'm submitting this on behalf of my colleague Sarah in the trading team. Her WiFi "
        "dropped completely and she can't get online to submit a ticket herself. She's somewhere "
        "on the trading floor but I'm not sure exactly which section or floor. I don't have her "
        "direct extension or mobile number — I just saw her struggling and offered to report it. "
        "She said her laptop can't see any WiFi networks at all.",
        "Filing this for a contractor who started today — their laptop won't connect to WiFi and "
        "they can't log in to submit a ticket. I don't have their phone number or employee ID. "
        "I think they're sitting somewhere on Floor 8 but I'm not certain. They said they were "
        "given a laptop but WiFi doesn't connect to any of our networks.",
    ],
    next_best_actions=[
        "Obtain the affected user's direct contact information and exact location. Determine "
        "whether the issue is device-specific or a broader WiFi coverage problem.",
    ],
    remediation_steps=[
        [
            "Get the affected user's name, employee ID, and direct contact details from the reporter",
            "Identify the user's exact floor and desk location for WiFi coverage analysis",
            "Check the wireless controller for the user's device MAC to see connection attempts",
            "Verify the user's device has the correct WiFi profile and certificates",
            "If the device is new, ensure it's been provisioned with the corporate WiFi configuration",
            "Test WiFi connectivity on-site at the user's location with a reference device",
        ],
    ],
))

# ---------------------------------------------------------------------------
# net-028  Same DNS issue as last month — prior ticket reference
# ---------------------------------------------------------------------------
register(ScenarioTemplate(
    scenario_id="net-028",
    category=Category.NETWORK,
    priority=Priority.P2,
    assigned_team=Team.NETWORK,
    needs_escalation=False,
    missing_information=[MissingInfo.PREVIOUS_TICKET_ID, MissingInfo.ERROR_MESSAGE],
    subjects=[
        "DNS resolution failing again — same issue as last month",
        "Internal DNS not resolving — we had this exact problem before",
        "DNS issue is back — thought this was permanently fixed",
    ],
    descriptions=[
        "Internal DNS resolution is failing again for several of our application servers. This is "
        "the same issue we had last month where internal hostnames wouldn't resolve but external "
        "sites worked fine. The network team fixed it by flushing the DNS cache on the server "
        "or something — I don't remember exactly. I can't find the old ticket number. The "
        "applications just time out but I'm not sure what the exact DNS error message is because "
        "the apps just show a generic 'connection failed' screen.",
        "We're experiencing DNS failures again — nslookup for internal resources returns 'server "
        "failed' intermittently. This happened before and there was a ticket about a DNS forwarder "
        "misconfiguration. I don't have that ticket number. The error is inconsistent — sometimes "
        "it resolves, sometimes it doesn't — so I haven't been able to capture the exact error "
        "message reliably.",
    ],
    next_best_actions=[
        "Search for prior DNS incident tickets and check DNS server health. Run diagnostic "
        "queries to identify whether this is a forwarder, zone, or caching issue.",
    ],
    remediation_steps=[
        [
            "Search the ticketing system for prior DNS-related incidents and review the resolution",
            "Check DNS server health and query response times from the affected subnet",
            "Run nslookup and dig from affected clients to capture the exact error responses",
            "Verify DNS forwarder configuration matches the last known-good state",
            "Flush DNS caches on the DNS servers and affected clients",
            "Monitor DNS resolution stability and set up an alert for future failures",
        ],
    ],
))

# ---------------------------------------------------------------------------
# net-029  Network latency — no traceroute screenshot
# ---------------------------------------------------------------------------
register(ScenarioTemplate(
    scenario_id="net-029",
    category=Category.NETWORK,
    priority=Priority.P3,
    assigned_team=Team.NETWORK,
    needs_escalation=False,
    missing_information=[MissingInfo.SCREENSHOT_OR_ATTACHMENT, MissingInfo.REPRODUCTION_FREQUENCY],
    subjects=[
        "Terrible network latency to cloud applications",
        "Everything is slow on the network — high latency suspected",
        "Network lag making cloud apps unusable",
    ],
    descriptions=[
        "I'm experiencing horrible latency to all our cloud applications — Salesforce, O365, and "
        "our Azure-hosted internal tools are all painfully slow. Pages take 10-15 seconds to load. "
        "I've been asked to run a traceroute but I'm not sure how and didn't manage to capture "
        "any output to share. I'm in the Singapore office on the 12th floor. It's hard to say "
        "how often it happens — sometimes it's fine, sometimes it's terrible.",
        "Network latency is making it impossible to work. Teams calls are choppy, SharePoint takes "
        "forever, and saving files to OneDrive times out frequently. I tried running a speed test "
        "but closed the browser tab before saving the results. I don't know if this is constant or "
        "only at certain times — it seems random. Several people near me are complaining too.",
    ],
    next_best_actions=[
        "Guide the user through running a traceroute and speed test and have them share the "
        "results. Check network monitoring for latency spikes on the user's subnet.",
    ],
    remediation_steps=[
        [
            "Walk the user through running tracert and a speed test, and have them save the output",
            "Check network monitoring dashboards for latency anomalies on the user's floor/subnet",
            "Verify the user's traffic path — is it going through the local internet breakout or backhauled",
            "Check the proxy and firewall for bandwidth saturation or throttling",
            "If the issue is intermittent, set up continuous monitoring on the user's subnet",
            "Review QoS policies to ensure cloud application traffic is prioritized",
        ],
    ],
))

# ---------------------------------------------------------------------------
# net-030  VPN issue from hotel — no callback info
# ---------------------------------------------------------------------------
register(ScenarioTemplate(
    scenario_id="net-030",
    category=Category.NETWORK,
    priority=Priority.P2,
    assigned_team=Team.NETWORK,
    needs_escalation=False,
    missing_information=[MissingInfo.CONTACT_INFO, MissingInfo.NETWORK_LOCATION],
    subjects=[
        "Can't connect to VPN from hotel — need urgent help",
        "VPN blocked at hotel — no way to work remotely",
        "Hotel WiFi blocking VPN — traveling for work and stuck",
    ],
    descriptions=[
        "I'm traveling for work and the hotel WiFi is blocking our VPN. I can connect to the "
        "hotel WiFi fine but GlobalProtect can't establish a tunnel — it just times out. I think "
        "the hotel might be blocking certain ports. I have a critical client meeting first thing "
        "tomorrow and need to access our systems tonight to prepare. I'm not sure what my hotel "
        "room phone number is and my cell service is roaming with spotty coverage. Email is the "
        "best way to reach me.",
        "Stuck at a conference hotel and the VPN won't connect. I've tried both the lobby WiFi "
        "and the in-room WiFi — neither works with our VPN. I need to finalize a presentation "
        "that's on our internal SharePoint. I don't have a reliable phone number right now since "
        "I'm overseas. I'm not sure exactly what network I'm on — the hotel has multiple SSIDs "
        "and I've tried a few of them.",
    ],
    next_best_actions=[
        "Obtain an alternate contact method for the user. Guide them to try the VPN on an "
        "alternate port (TCP 443) or provide a web-based VPN portal as a fallback.",
    ],
    remediation_steps=[
        [
            "Get the user's current contact info (personal email, hotel front desk number, WhatsApp)",
            "Determine the hotel name and location to check for known network restrictions",
            "Instruct the user to try the VPN on TCP port 443 (SSL VPN mode) to bypass port blocks",
            "If the VPN client fails, provide access to the web-based SSL VPN portal URL",
            "As a fallback, suggest using a mobile hotspot from a personal phone if cellular works",
            "If all else fails, enable a temporary conditional access exception for the user's account",
        ],
    ],
))
