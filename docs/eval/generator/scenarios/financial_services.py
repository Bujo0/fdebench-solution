"""Financial services-specific scenario definitions.

Covers: trading platform issues, Bloomberg terminal problems,
financial reporting tools, market data feeds, compliance system
access, and other scenarios specific to Contoso Financial Services.
"""

from generator.models import Scenario

SCENARIOS: list[Scenario] = [
    # ──────────────────────────────────────────────────────────────────
    # 1. Bloomberg terminal not connecting
    # ──────────────────────────────────────────────────────────────────
    Scenario(
        scenario_id="fin-bloomberg-connectivity",
        category="Software & Applications",
        priority="P1",
        assigned_team="Enterprise Applications",
        needs_escalation=True,
        missing_information=["error_message", "device_info", "timestamp"],
        subjects=[
            "Bloomberg terminal down — can't access market data",
            "Bloomberg not loading — stuck on login screen for 20 minutes",
            "URGENT: Bloomberg terminal offline during market hours",
        ],
        descriptions=[
            "My Bloomberg terminal has been stuck on the loading screen since 7:45 AM. I can't access any market "
            "data, run analytics, or check pricing. Markets open in 15 minutes and I have client orders to execute. "
            "I've rebooted the terminal twice and checked my network cable. Other traders on the desk say theirs are "
            "working fine.",
            "Bloomberg is completely unresponsive on my workstation. The application launches but then hangs at "
            "'Connecting to Bloomberg Network.' I've been unable to pull up any tickers or run reports. This is "
            "impacting my ability to manage the fixed income portfolio. Need immediate assistance.",
        ],
        next_best_actions=[
            "Check Bloomberg B-UNIT connectivity and local firewall rules. If isolated to one terminal, reinstall "
            "the Bloomberg software or swap the B-UNIT.",
            "Verify Bloomberg network connectivity, check for local proxy or firewall issues, and swap the B-UNIT "
            "if hardware is suspected.",
        ],
        remediation_steps=[
            [
                "Verify the Bloomberg B-UNIT is properly connected and has a valid license",
                "Check local firewall rules and proxy settings for Bloomberg traffic",
                "Test connectivity to Bloomberg's network from the workstation",
                "If isolated, reinstall Bloomberg software or replace the B-UNIT",
                "Escalate to Bloomberg support if the issue is on their infrastructure side",
            ],
        ],
        tags=["trading", "critical", "market-hours"],
    ),
    # ──────────────────────────────────────────────────────────────────
    # 2. Trading platform latency spike
    # ──────────────────────────────────────────────────────────────────
    Scenario(
        scenario_id="fin-trading-platform-latency",
        category="Network & Connectivity",
        priority="P1",
        assigned_team="Network Operations",
        needs_escalation=True,
        missing_information=["timestamp", "affected_users", "network_location"],
        subjects=[
            "Trading platform experiencing 500ms+ latency — orders delayed",
            "Severe lag on order execution system during active trading",
            "Order management system response times unacceptable",
        ],
        descriptions=[
            "Our order management system is showing execution latencies of 500ms to 2 seconds, compared to our "
            "normal sub-50ms. This started about 30 minutes ago and is affecting the entire equities trading desk. "
            "We've already had two client complaints about delayed fills. This needs to be fixed immediately — we're "
            "losing money with every delayed order.",
            "The trading platform has been sluggish since market open. Order confirmations that normally come back "
            "instantly are taking 1-3 seconds. Our quant models depend on low latency for arbitrage strategies and "
            "we've had to pause automated trading. The network team needs to check the co-lo link immediately.",
        ],
        next_best_actions=[
            "Investigate network path between trading desks and the execution venues. Check switch port utilization "
            "and QoS queues on the low-latency trading VLAN.",
            "Check co-location link health and network equipment along the trading path for congestion or errors.",
        ],
        remediation_steps=[
            [
                "Check network utilization on the trading VLAN and co-location links",
                "Review switch and router interface counters for errors, drops, or CRC failures",
                "Verify QoS policies are prioritizing trading traffic correctly",
                "Check for any recent network changes or maintenance that could affect the path",
                "If the issue is external, contact the co-location provider or exchange connectivity team",
            ],
        ],
        tags=["trading", "critical", "latency", "market-hours"],
    ),
    # ──────────────────────────────────────────────────────────────────
    # 3. Financial reporting tool — quarter-end crunch
    # ──────────────────────────────────────────────────────────────────
    Scenario(
        scenario_id="fin-reporting-tool-crash",
        category="Software & Applications",
        priority="P2",
        assigned_team="Enterprise Applications",
        needs_escalation=False,
        missing_information=["error_message", "steps_to_reproduce", "application_version"],
        subjects=[
            "Financial reporting tool crashes when generating quarterly reports",
            "SAP crashes during quarter-end close — need it fixed ASAP",
        ],
        descriptions=[
            "Every time I try to generate the Q1 consolidated financial report in SAP, the application crashes "
            "with an 'Unexpected Error' dialog. I've tried three times and it fails at the same point — when it "
            "tries to aggregate the subsidiary data. Quarter-end close is in 3 days and I need this working. The "
            "same report ran fine for Q4 last year.",
            "The financial consolidation module in our reporting tool keeps timing out when I run the intercompany "
            "elimination report. It processes for about 10 minutes and then shows 'Connection to server lost.' My "
            "colleagues in the London office report the same issue. The dataset is larger this quarter because we "
            "added two new entities.",
        ],
        next_best_actions=[
            "Check application server logs for the crash event and investigate whether the larger dataset is causing "
            "a memory or timeout issue.",
            "Review the SAP application logs, check memory allocation, and consider increasing timeout thresholds "
            "for the consolidation module.",
        ],
        remediation_steps=[
            [
                "Review application server crash logs and error dumps",
                "Check if the server has sufficient memory for the larger dataset",
                "Increase timeout thresholds for the consolidation module if needed",
                "Test the report generation with a smaller subset of entities to isolate the failure point",
                "Apply any pending patches for the reporting module",
            ],
        ],
        tags=["financial-reporting", "quarter-end"],
    ),
    # ──────────────────────────────────────────────────────────────────
    # 4. Compliance system access for audit
    # ──────────────────────────────────────────────────────────────────
    Scenario(
        scenario_id="fin-compliance-audit-access",
        category="Access & Authentication",
        priority="P2",
        assigned_team="Identity & Access Management",
        needs_escalation=False,
        missing_information=["business_impact", "configuration_details"],
        subjects=[
            "Need access to compliance monitoring system for regulatory audit",
            "Audit team needs read-only access to trade surveillance platform",
        ],
        descriptions=[
            "Our internal audit team needs read-only access to the compliance monitoring system (ComplianceOne) for "
            "the upcoming SEC examination. The audit starts next Monday and the team of 4 auditors needs to be able "
            "to view trade surveillance records, communications monitoring logs, and KYC documentation. Their manager "
            "(VP of Internal Audit) has approved this — can you set up temporary access?",
            "We have an FINRA examination starting next week and the examiners need view-only access to our trade "
            "surveillance platform. This is a regulatory requirement and we need it set up by Friday. The access "
            "should be scoped to the equity trading desk data from the past 12 months only. I'll send the list of "
            "examiner names and IDs separately.",
        ],
        next_best_actions=[
            "Verify the access request with the compliance officer and provision time-limited read-only access to "
            "the specified systems.",
            "Coordinate with the compliance team to set up scoped, time-limited access for the audit team.",
        ],
        remediation_steps=[
            [
                "Verify the access request with the requesting manager and compliance officer",
                "Create time-limited read-only accounts with appropriate scope",
                "Ensure audit logging is enabled for all access by the audit/examiner accounts",
                "Set an automatic expiration date for the temporary access",
                "Notify the security team of the temporary elevated access",
            ],
        ],
        tags=["compliance", "audit", "regulatory"],
    ),
    # ──────────────────────────────────────────────────────────────────
    # 5. Market data feed interruption
    # ──────────────────────────────────────────────────────────────────
    Scenario(
        scenario_id="fin-market-data-feed-down",
        category="Network & Connectivity",
        priority="P1",
        assigned_team="Network Operations",
        needs_escalation=True,
        missing_information=["affected_system", "timestamp", "affected_users"],
        subjects=[
            "Market data feed is down — no live pricing on trading floor",
            "Reuters/Refinitiv data feed not updating — stale prices showing",
        ],
        descriptions=[
            "The real-time market data feed stopped updating about 10 minutes ago. All trading terminals on the "
            "equity desk are showing stale prices. The last tick we received was at 10:23 AM. Bloomberg is working "
            "fine but our internal pricing engine relies on the Reuters feed and it's completely frozen. We need "
            "this back immediately — we can't price client trades.",
            "Our Refinitiv Eikon feed appears to be down. The data is not flowing into our risk management system "
            "and our real-time P&L calculations are stuck. The network indicator on the Eikon terminal shows a red "
            "X. The options desk and the FX desk are both affected. We're flying blind on risk.",
        ],
        next_best_actions=[
            "Check the network link to the Refinitiv data center and verify the feed handler server is receiving "
            "data. Contact Refinitiv support if the issue is upstream.",
            "Investigate the feed handler infrastructure — check servers, network links, and Refinitiv service status.",
        ],
        remediation_steps=[
            [
                "Check the feed handler server health and process status",
                "Verify network connectivity to the Refinitiv data center",
                "Check Refinitiv service status for known outages",
                "Restart the feed handler process if it has crashed",
                "If the issue is upstream, contact Refinitiv support and activate the backup data feed",
            ],
        ],
        tags=["trading", "critical", "market-data", "market-hours"],
    ),
    # ──────────────────────────────────────────────────────────────────
    # 6. Secure file transfer for client data
    # ──────────────────────────────────────────────────────────────────
    Scenario(
        scenario_id="fin-secure-file-transfer",
        category="Security & Compliance",
        priority="P2",
        assigned_team="Security Operations",
        needs_escalation=False,
        missing_information=["configuration_details", "business_impact"],
        subjects=[
            "Need to set up secure file transfer for client deliverables",
            "SFTP connection to client rejected — certificate error",
        ],
        descriptions=[
            "I need to send encrypted portfolio reports to our institutional client (Vanguard) but the SFTP "
            "connection is failing with a certificate error. The client updated their TLS certificate last week and "
            "now our automated file transfer job fails every night. The reports are due daily by 6 AM and we've "
            "missed the last two deliveries. I have the new certificate from the client.",
            "Our nightly batch job that transfers NAV calculations to our custodian bank is failing. The SFTP "
            "connection was working until Friday and now it rejects our connection with 'SSL handshake failed.' "
            "The custodian says they rotated their server certificate. We need to update our end to accept the "
            "new certificate.",
        ],
        next_best_actions=[
            "Import the client's new TLS certificate into the SFTP server's trust store and test the connection.",
            "Update the certificate trust store with the new remote certificate and verify the connection.",
        ],
        remediation_steps=[
            [
                "Obtain the new certificate from the client or custodian",
                "Import the certificate into the SFTP server's trust store",
                "Test the connection manually before re-enabling the automated job",
                "Update the batch job configuration if the certificate thumbprint has changed",
                "Verify the next scheduled transfer completes successfully",
            ],
        ],
        tags=["compliance", "certificate", "file-transfer"],
    ),
    # ──────────────────────────────────────────────────────────────────
    # 7. Risk management system disk full
    # ──────────────────────────────────────────────────────────────────
    Scenario(
        scenario_id="fin-risk-system-disk-full",
        category="Data & Storage",
        priority="P1",
        assigned_team="Data Platform",
        needs_escalation=True,
        missing_information=["affected_system", "environment_details"],
        subjects=[
            "Risk management system database disk full — calculations stopped",
            "URGENT: Risk engine can't write to database — disk space at 100%",
        ],
        descriptions=[
            "Our risk management system stopped producing real-time risk calculations at around 9:15 AM. The "
            "application logs show 'ORA-01653: unable to extend table' errors. It looks like the database disk is "
            "full. The risk team is unable to see current portfolio risk metrics and we have a regulatory requirement "
            "to maintain real-time risk monitoring during market hours.",
            "The overnight VaR (Value at Risk) calculation batch job failed and the database server is showing disk "
            "space at 99.8% full. The risk management application cannot write any new data. We need to free up "
            "space immediately and get the risk calculations running again before the regulatory reporting deadline "
            "at noon.",
        ],
        next_best_actions=[
            "Free up disk space by archiving or purging old data, and extend the tablespace. Restart the risk "
            "calculation engine after space is recovered.",
            "Identify and remove or archive old data to free disk space. Extend the database storage allocation.",
        ],
        remediation_steps=[
            [
                "Identify the largest tables and determine what data can be safely archived",
                "Archive or purge historical data older than the retention policy",
                "Extend the tablespace or add additional storage",
                "Restart the risk calculation engine and verify it's processing correctly",
                "Set up disk space monitoring alerts to prevent recurrence",
            ],
        ],
        tags=["trading", "critical", "storage", "regulatory"],
    ),
    # ──────────────────────────────────────────────────────────────────
    # 8. Two-factor token for trading system expired
    # ──────────────────────────────────────────────────────────────────
    Scenario(
        scenario_id="fin-trading-token-expired",
        category="Access & Authentication",
        priority="P2",
        assigned_team="Identity & Access Management",
        needs_escalation=False,
        missing_information=["device_info", "authentication_method"],
        subjects=[
            "Hardware token for trading system expired — can't log in",
            "RSA SecurID token stopped working — locked out of order entry",
        ],
        descriptions=[
            "My RSA SecurID hardware token for the order management system expired today. The token display shows "
            "a code but the system says 'Token authentication failed.' I have trades queued up that need to be "
            "submitted before market close. Can someone provision a new token or give me temporary access?",
            "My hardware security token for the trading platform stopped working this morning. When I enter the "
            "code it shows, the system rejects it with 'Invalid token.' I've tried syncing the token by entering "
            "two consecutive codes but that didn't work either. I need access to manage my client positions.",
        ],
        next_best_actions=[
            "Issue an emergency temporary token or software token and schedule a replacement hardware token.",
            "Verify the token serial number and expiry, issue a temporary software token, and order a replacement.",
        ],
        remediation_steps=[
            [
                "Verify the user's identity and check the token status in the RSA admin console",
                "If expired, provision an emergency software token for immediate access",
                "Order a replacement hardware token",
                "Update the token assignment in the authentication system",
            ],
        ],
        tags=["trading", "authentication", "hardware-token"],
    ),
]
