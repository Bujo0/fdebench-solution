"""Data & Storage scenario definitions for Contoso Financial Services.

Covers: database outages, ETL pipeline failures, SharePoint access, OneDrive sync,
backup/restore, file share access, storage capacity, data migration, Azure VM issues,
data catalog access, SQL access requests, Cosmos DB throttling, data lake permissions,
Power BI refresh failures, blob storage, Redis cache, Elasticsearch, data quality,
and archive/retention policies.
"""

from ms.evals_core.constants import Category
from ms.evals_core.constants import Channel
from ms.evals_core.constants import MissingInfo
from ms.evals_core.constants import Priority
from ms.evals_core.constants import Team
from ms.evals_core.scenarios.base import ScenarioDefinition


def get_scenarios() -> list[ScenarioDefinition]:
    """Return all Data & Storage scenario definitions."""
    return [
        # ------------------------------------------------------------------
        # ds-001  Production SQL database timeout
        # ------------------------------------------------------------------
        ScenarioDefinition(
            scenario_id="ds-001",
            subject="URGENT — Production SQL DB timing out on all queries",
            description=(
                "We are seeing widespread query timeouts on the prod-trading-sql-01 Azure SQL"
                " instance in the eastus2 region. The connection pool is fully exhausted and our"
                " trading reconciliation service has been down since approximately 06:45 UTC."
                " Multiple teams are affected — the entire Trading floor in NYC and London cannot"
                " run end-of-day reports. We've already tried restarting the application pool on"
                " the consuming services but the DB itself is not responding to basic SELECT 1"
                " health checks. Please treat this as a sev-1 incident."
            ),
            category=Category.DATA_STORAGE,
            priority=Priority.P1,
            team=Team.DATA_PLATFORM,
            needs_escalation=True,
            missing_info=[
                MissingInfo.ERROR_MESSAGE,
                MissingInfo.TIMESTAMP,
            ],
            next_best_action=(
                "Immediately engage the on-call DBA to check Azure SQL resource health, DTU/vCore"
                " utilization, and active sessions. Open an Azure support ticket if the instance"
                " shows platform-level degradation."
            ),
            remediation_steps=[
                "Check Azure SQL resource health blade and service health advisories for eastus2",
                "Review active sessions and blocking chains via sys.dm_exec_requests",
                "Kill any long-running or orphaned sessions contributing to pool exhaustion",
                "Scale up DTU/vCores temporarily if resource limits are the bottleneck",
                "Restart dependent application services once the database is responsive",
                "Conduct post-incident review and implement connection pool tuning",
            ],
            reporter_name="David Chen",
            reporter_email="david.chen@contoso.com",
            reporter_department="Trading",
            channel=Channel.PHONE,
            created_at="2026-03-18T06:52:00Z",
            tags=["production", "outage", "sql", "trading"],
            difficulty="hard",
        ),
        # ------------------------------------------------------------------
        # ds-002  SQL replication lag
        # ------------------------------------------------------------------
        ScenarioDefinition(
            scenario_id="ds-002",
            subject="SQL read replica is 15 minutes behind primary",
            description=(
                "The read replica for rg-analytics-prod / analytics-sql-replica in UK South has"
                " fallen over 15 minutes behind the primary. Our London risk dashboards pull from"
                " this replica, so the numbers the risk team is seeing are stale. I noticed it"
                " about 30 minutes ago but it hasn't caught up. Geo-replication status shows"
                " 'Seeding' which seems wrong for a replica that's been running for months."
            ),
            category=Category.DATA_STORAGE,
            priority=Priority.P2,
            team=Team.DATA_PLATFORM,
            needs_escalation=True,
            missing_info=[
                MissingInfo.ENVIRONMENT_DETAILS,
            ],
            next_best_action=(
                "Check the geo-replication link health on the primary and replica. Investigate"
                " whether a large transaction or schema change triggered a re-seed event."
            ),
            remediation_steps=[
                "Verify geo-replication status via sys.dm_geo_replication_link_status on the primary",
                "Check for long-running DDL or large bulk operations that may block replication",
                "Review network latency between eastus2 and uksouth Azure regions",
                "If the link is broken, remove and recreate the geo-replication relationship",
                "Validate replica data freshness after recovery and notify the risk team",
            ],
            reporter_name="Sarah Okonkwo",
            reporter_email="sarah.okonkwo@contoso.com",
            reporter_department="Risk Management",
            channel=Channel.CHAT,
            created_at="2026-03-18T08:15:00Z",
            tags=["sql", "replication", "london"],
            difficulty="hard",
        ),
        # ------------------------------------------------------------------
        # ds-003  Database deadlocks
        # ------------------------------------------------------------------
        ScenarioDefinition(
            scenario_id="ds-003",
            subject="Frequent deadlocks on settlements database",
            description=(
                "Hi team,\n\nWe keep hitting deadlocks on the settlements-prod-sql database in"
                " resource group rg-settlements-prod. It happens 3-4 times per day, usually during"
                " the batch settlement window between 16:00–17:00 UTC. The app retries but it slows"
                " everything down and occasionally a batch fails entirely. I grabbed the deadlock"
                " XML from the extended events session — happy to share if you tell me where to"
                " upload it.\n\nThanks,\nMarcus"
            ),
            category=Category.DATA_STORAGE,
            priority=Priority.P2,
            team=Team.DATA_PLATFORM,
            needs_escalation=False,
            missing_info=[
                MissingInfo.SCREENSHOT_OR_ATTACHMENT,
                MissingInfo.REPRODUCTION_FREQUENCY,
            ],
            next_best_action=(
                "Request the deadlock XML graph and analyze the competing sessions to identify"
                " index or query changes that would eliminate the cycle."
            ),
            remediation_steps=[
                "Collect deadlock graphs from the extended events session or system_health",
                "Identify the tables and indexes involved in the deadlock cycle",
                "Evaluate query access patterns and consider consistent key ordering",
                "Add or modify indexes to reduce lock contention during batch window",
                "Test changes in the staging environment before deploying to production",
                "Monitor deadlock frequency after the fix is applied",
            ],
            reporter_name="Marcus Williams",
            reporter_email="marcus.williams@contoso.com",
            reporter_department="Settlements",
            channel=Channel.EMAIL,
            created_at="2026-03-18T17:30:00Z",
            tags=["sql", "deadlock", "settlements", "batch"],
            difficulty="hard",
        ),
        # ------------------------------------------------------------------
        # ds-004  Connection pool exhaustion
        # ------------------------------------------------------------------
        ScenarioDefinition(
            scenario_id="ds-004",
            subject="App can't connect to SQL — connection pool exhausted",
            description=(
                "Our portfolio-analytics microservice running in AKS cluster aks-prod-eus2 is"
                " throwing 'Timeout expired. The timeout period elapsed prior to obtaining a"
                " connection from the pool.' errors. It started around 14:00 UTC and is getting"
                " worse. The service connects to portfolio-sql-prod in rg-portfolio-prod. We haven't"
                " deployed any code changes today."
            ),
            category=Category.DATA_STORAGE,
            priority=Priority.P1,
            team=Team.DATA_PLATFORM,
            needs_escalation=True,
            missing_info=[
                MissingInfo.CONFIGURATION_DETAILS,
                MissingInfo.AFFECTED_USERS,
            ],
            next_best_action=(
                "Check the SQL server for orphaned sessions and long-running queries. Review the"
                " AKS pod count — a recent autoscale event may have opened more connections than"
                " the pool allows."
            ),
            remediation_steps=[
                "Query sys.dm_exec_sessions to identify orphaned or sleeping connections",
                "Check AKS horizontal pod autoscaler — correlate pod count increase with connection spike",
                "Kill orphaned sessions on the SQL side to free pool capacity",
                "Adjust connection string parameters (Max Pool Size, Connection Timeout)",
                "Implement connection resiliency with retry logic if not already present",
                "Set up Azure Monitor alerts for connection count thresholds",
            ],
            reporter_name="James Hartley",
            reporter_email="james.hartley@contoso.com",
            reporter_department="Backend Engineering",
            channel=Channel.CHAT,
            created_at="2026-03-18T14:12:00Z",
            tags=["sql", "connection-pool", "aks", "production"],
            difficulty="hard",
        ),
        # ------------------------------------------------------------------
        # ds-005  ADF pipeline failure (403)
        # ------------------------------------------------------------------
        ScenarioDefinition(
            scenario_id="ds-005",
            subject="ADF pipeline 'DailyMarketDataLoad' failing with 403",
            description=(
                "The DailyMarketDataLoad pipeline in Azure Data Factory adf-marketdata-prod"
                " (rg-data-prod, eastus2) started failing last night at 23:00 UTC with a 403"
                " Forbidden error on the copy activity that pulls from our external market data"
                " vendor's blob storage. The SAS token we use might have expired — we renewed it"
                " last quarter. This pipeline feeds the morning trading analytics dashboard so we"
                " need it fixed before London open."
            ),
            category=Category.DATA_STORAGE,
            priority=Priority.P2,
            team=Team.DATA_PLATFORM,
            needs_escalation=False,
            missing_info=[
                MissingInfo.AUTHENTICATION_METHOD,
                MissingInfo.CONFIGURATION_DETAILS,
            ],
            next_best_action=(
                "Verify the SAS token expiry on the linked service. If expired, generate a new"
                " token from the vendor's storage account and update the ADF linked service."
            ),
            remediation_steps=[
                "Open ADF Studio and inspect the failed pipeline run's error details",
                "Check the linked service for the external blob — verify SAS token expiry date",
                "Request or generate a new SAS token with appropriate permissions",
                "Update the linked service configuration with the new token",
                "Trigger a manual pipeline run and validate the copy activity succeeds",
                "Set up a calendar reminder for the next SAS token renewal",
            ],
            reporter_name="Priya Sharma",
            reporter_email="priya.sharma@contoso.com",
            reporter_department="Data Engineering",
            channel=Channel.PORTAL,
            created_at="2026-03-18T05:30:00Z",
            tags=["adf", "etl", "pipeline", "market-data"],
            difficulty="medium",
        ),
        # ------------------------------------------------------------------
        # ds-006  Databricks job OOM
        # ------------------------------------------------------------------
        ScenarioDefinition(
            scenario_id="ds-006",
            subject="Databricks job crashing with OutOfMemoryError",
            description=(
                "Our nightly risk aggregation job on the Databricks workspace dbw-risk-prod"
                " (rg-risk-prod, westeurope) is failing with a java.lang.OutOfMemoryError on the"
                " driver node. It ran fine until last Thursday when the Risk team added three new"
                " instrument classes to the aggregation scope. The cluster is Standard_DS4_v2 with"
                " autoscaling 2-8 workers. The driver collects a large DataFrame at the end to"
                " write a summary — that's likely where it blows up."
            ),
            category=Category.DATA_STORAGE,
            priority=Priority.P2,
            team=Team.DATA_PLATFORM,
            needs_escalation=False,
            missing_info=[
                MissingInfo.ERROR_MESSAGE,
                MissingInfo.CONFIGURATION_DETAILS,
            ],
            next_best_action=(
                "Review the Spark UI for the failing stage. The driver collect() call should be"
                " replaced with a distributed write or the driver node should be upgraded to a"
                " memory-optimized SKU."
            ),
            remediation_steps=[
                "Pull the full stack trace from the Databricks job run and identify the failing stage",
                "Check the Spark UI for data skew and shuffle spill metrics",
                "Replace the driver-side collect() with a distributed write (e.g., write to Delta table)",
                "If collect is required, upgrade the driver node to Standard_E8s_v3 or larger",
                "Validate the fix by running the job with the expanded instrument scope",
                "Add memory monitoring alerts to the cluster policy",
            ],
            reporter_name="Liam Foster",
            reporter_email="liam.foster@contoso.com",
            reporter_department="Risk Management",
            channel=Channel.EMAIL,
            created_at="2026-03-18T07:45:00Z",
            tags=["databricks", "spark", "oom", "risk"],
            difficulty="hard",
        ),
        # ------------------------------------------------------------------
        # ds-007  Synapse query timeout
        # ------------------------------------------------------------------
        ScenarioDefinition(
            scenario_id="ds-007",
            subject="Synapse dedicated pool query timing out after 30 min",
            description=(
                "A critical regulatory report query on the Synapse dedicated pool synpool-reg-prod"
                " (rg-analytics-prod) is timing out after hitting the 30-minute limit. The query"
                " joins five fact tables and is used for the quarterly Basel III capital calculation."
                " It used to complete in about 12 minutes but has been getting slower as data volumes"
                " grow. We need this done by end of week for the compliance deadline."
            ),
            category=Category.DATA_STORAGE,
            priority=Priority.P2,
            team=Team.DATA_PLATFORM,
            needs_escalation=False,
            missing_info=[
                MissingInfo.BUSINESS_IMPACT,
            ],
            next_best_action=(
                "Capture the query execution plan and check for suboptimal data movement operations."
                " Evaluate whether the distribution keys and statistics are up to date."
            ),
            remediation_steps=[
                "Run EXPLAIN on the query to inspect the distributed execution plan",
                "Update statistics on all five fact tables involved",
                "Check distribution key alignment across joined tables to minimize data movement",
                "Consider materializing intermediate results in a staging table",
                "Temporarily scale up the dedicated pool DWU for the reporting window",
                "Validate query completes within the acceptable time window after changes",
            ],
            reporter_name="Elena Vasquez",
            reporter_email="elena.vasquez@contoso.com",
            reporter_department="Compliance",
            channel=Channel.PORTAL,
            created_at="2026-03-18T10:00:00Z",
            tags=["synapse", "query-performance", "compliance", "regulatory"],
            difficulty="hard",
        ),
        # ------------------------------------------------------------------
        # ds-008  SharePoint site access request
        # ------------------------------------------------------------------
        ScenarioDefinition(
            scenario_id="ds-008",
            subject="Need access to the M&A Deals SharePoint site",
            description=(
                "Hi, I've just transferred to the Corporate Strategy team from Retail Banking and I"
                " need access to the M&A Deals SharePoint site at"
                " https://contoso.sharepoint.com/sites/ma-deals. My manager Karen Liu approved it"
                " verbally but I'm not sure if there's a formal approval workflow. I need at least"
                " read access for now to review due diligence documents for Project Falcon."
            ),
            category=Category.DATA_STORAGE,
            priority=Priority.P3,
            team=Team.DATA_PLATFORM,
            needs_escalation=False,
            missing_info=[
                MissingInfo.BUSINESS_IMPACT,
                MissingInfo.AUTHENTICATION_METHOD,
            ],
            next_best_action=(
                "Verify the reporter's role change in Entra ID and route the access request to the"
                " M&A Deals site owner for formal approval before granting permissions."
            ),
            remediation_steps=[
                "Confirm the reporter's department transfer in Entra ID",
                "Identify the M&A Deals SharePoint site owner or data steward",
                "Route the access request to the site owner with the manager approval reference",
                "Upon approval, add the user to the appropriate SharePoint permission group",
                "Notify the reporter with the site URL and any data handling guidelines",
            ],
            reporter_name="Tom Nakamura",
            reporter_email="tom.nakamura@contoso.com",
            reporter_department="Corporate Strategy",
            channel=Channel.PORTAL,
            created_at="2026-03-18T09:20:00Z",
            tags=["sharepoint", "access-request"],
            difficulty="easy",
        ),
        # ------------------------------------------------------------------
        # ds-009  SharePoint site collection quota exceeded
        # ------------------------------------------------------------------
        ScenarioDefinition(
            scenario_id="ds-009",
            subject="SharePoint site collection quota full — can't upload files",
            description=(
                "I'm getting 'You have exceeded your storage quota' when trying to upload a file to"
                " the Finance Reporting site collection. The whole finance team is blocked — we can't"
                " upload monthly close documents. The site URL is"
                " https://contoso.sharepoint.com/sites/finance-reporting. Can you increase the"
                " quota or help us archive old content? We have about 18 months of reports that"
                " could be moved to cold storage."
            ),
            category=Category.DATA_STORAGE,
            priority=Priority.P3,
            team=Team.DATA_PLATFORM,
            needs_escalation=False,
            missing_info=[
                MissingInfo.AFFECTED_USERS,
            ],
            next_best_action=(
                "Check the current site collection storage usage in the SharePoint admin center."
                " Increase the quota temporarily while planning an archival strategy for old content."
            ),
            remediation_steps=[
                "Review site collection storage usage in SharePoint admin center",
                "Identify large files and version histories consuming the most space",
                "Increase the site collection quota as a short-term fix",
                "Work with the Finance team to archive documents older than 12 months",
                "Enable version trimming or retention policies to manage future growth",
            ],
            reporter_name="Angela Moretti",
            reporter_email="angela.moretti@contoso.com",
            reporter_department="Finance",
            channel=Channel.EMAIL,
            created_at="2026-03-18T11:05:00Z",
            tags=["sharepoint", "quota", "finance"],
            difficulty="medium",
        ),
        # ------------------------------------------------------------------
        # ds-010  OneDrive sync stuck
        # ------------------------------------------------------------------
        ScenarioDefinition(
            scenario_id="ds-010",
            subject="OneDrive sync has been stuck for 2 days",
            description=(
                "My OneDrive sync client has been showing 'Processing changes' for two days and"
                " nothing is actually syncing. I have about 40 GB of files in my OneDrive. I'm on"
                " Windows 11, OneDrive version 24.005.0117. I've tried pausing and resuming sync,"
                " and I signed out and back in, but it's still stuck. I'm worried about losing"
                " files since I've been working offline."
            ),
            category=Category.DATA_STORAGE,
            priority=Priority.P3,
            team=Team.DATA_PLATFORM,
            needs_escalation=False,
            missing_info=[
                MissingInfo.DEVICE_INFO,
                MissingInfo.NETWORK_LOCATION,
            ],
            next_best_action=(
                "Ask the user to run the OneDrive diagnostic tool (onedrive.exe /reset) and check"
                " for files with unsupported characters or path lengths exceeding 400 characters."
            ),
            remediation_steps=[
                "Check the OneDrive sync status icon for specific error indicators",
                "Review the OneDrive sync log at %localappdata%/Microsoft/OneDrive/logs",
                "Run onedrive.exe /reset to clear the local sync state",
                "Check for filenames with special characters or paths exceeding 400 characters",
                "If reset doesn't help, unlink and relink the OneDrive account",
                "Verify files are intact in the OneDrive web interface",
            ],
            reporter_name="Rachel Kim",
            reporter_email="rachel.kim@contoso.com",
            reporter_department="Marketing",
            channel=Channel.CHAT,
            created_at="2026-03-18T13:40:00Z",
            tags=["onedrive", "sync", "windows"],
            difficulty="medium",
        ),
        # ------------------------------------------------------------------
        # ds-011  OneDrive conflict errors
        # ------------------------------------------------------------------
        ScenarioDefinition(
            scenario_id="ds-011",
            subject="OneDrive keeps creating conflict copies of my Excel files",
            description=(
                "Every time I save a spreadsheet to my OneDrive folder I end up with a file called"
                " 'Budget_Q1 (John Smith's conflicting copy).xlsx'. I have at least 20 of these"
                " duplicates now. I use Excel desktop and sometimes edit the same file from my"
                " laptop and my desktop in the NYC office. How do I stop this from happening and"
                " which copies are the correct ones?"
            ),
            category=Category.DATA_STORAGE,
            priority=Priority.P4,
            team=Team.DATA_PLATFORM,
            needs_escalation=False,
            missing_info=[
                MissingInfo.DEVICE_INFO,
                MissingInfo.APPLICATION_VERSION,
            ],
            next_best_action=(
                "Explain that conflict copies occur when the same file is edited on multiple devices"
                " before sync completes. Recommend using AutoSave with OneDrive to avoid conflicts."
            ),
            remediation_steps=[
                "Review the conflict copies and compare timestamps to identify the latest version",
                "Merge any unique changes from conflict copies into the primary file",
                "Delete the conflict copies after merging",
                "Enable AutoSave in Excel to ensure real-time sync with OneDrive",
                "Advise the user to close files on one device before editing on another",
            ],
            reporter_name="John Smith",
            reporter_email="john.smith@contoso.com",
            reporter_department="Finance",
            channel=Channel.PORTAL,
            created_at="2026-03-18T15:10:00Z",
            tags=["onedrive", "conflict", "excel"],
            difficulty="easy",
        ),
        # ------------------------------------------------------------------
        # ds-012  Accidental deletion — restore request
        # ------------------------------------------------------------------
        ScenarioDefinition(
            scenario_id="ds-012",
            subject="Accidentally deleted entire Q4 folder from shared drive — PLEASE HELP",
            description=(
                "I accidentally deleted the entire Q4-2025-Reports folder from the shared drive"
                " \\\\contoso-fs01\\finance\\reports. It had about 300 files including final audit"
                " workpapers. I noticed it about 10 minutes ago and I haven't touched anything else."
                " This is critical — the external auditors need these files by Friday. Is there a"
                " backup we can restore from? I'm so sorry about this."
            ),
            category=Category.DATA_STORAGE,
            priority=Priority.P2,
            team=Team.DATA_PLATFORM,
            needs_escalation=True,
            missing_info=[
                MissingInfo.TIMESTAMP,
            ],
            next_best_action=(
                "Check Volume Shadow Copy (Previous Versions) on the file server first for a quick"
                " restore. If unavailable, initiate a restore from the latest Azure Backup vault."
            ),
            remediation_steps=[
                "Check if Volume Shadow Copy snapshots are available on the file server",
                "If available, restore the folder from the most recent shadow copy",
                "If not, initiate a restore from Azure Backup vault for the file share",
                "Verify all 300 files are restored and intact",
                "Notify the reporter and the external audit team that files are available",
                "Review file share permissions to consider restricting bulk delete capability",
            ],
            reporter_name="Michael Torres",
            reporter_email="michael.torres@contoso.com",
            reporter_department="Internal Audit",
            channel=Channel.PHONE,
            created_at="2026-03-18T16:22:00Z",
            tags=["restore", "file-share", "audit", "data-loss"],
            difficulty="medium",
        ),
        # ------------------------------------------------------------------
        # ds-013  Point-in-time restore for SQL DB
        # ------------------------------------------------------------------
        ScenarioDefinition(
            scenario_id="ds-013",
            subject="Request point-in-time restore of client-accounts database",
            description=(
                "We ran a bad UPDATE statement on the client-accounts database in rg-clientsvc-prod"
                " at approximately 11:42 UTC today that corrupted the account_status column for"
                " about 2,000 rows. We need a point-in-time restore to 11:40 UTC so we can extract"
                " the correct values and patch them back. We do NOT want to replace the live"
                " database — just need a restored copy we can query."
            ),
            category=Category.DATA_STORAGE,
            priority=Priority.P2,
            team=Team.DATA_PLATFORM,
            needs_escalation=True,
            missing_info=[
                MissingInfo.ENVIRONMENT_DETAILS,
            ],
            next_best_action=(
                "Initiate an Azure SQL point-in-time restore to a new database name, targeting"
                " 11:40 UTC. Grant the reporter read access to the restored copy for data extraction."
            ),
            remediation_steps=[
                "Verify the target restore time (11:40 UTC) is within the retention window",
                "Initiate a point-in-time restore to a new database (e.g., client-accounts-restore-0318)",
                "Wait for the restore operation to complete and verify the database is accessible",
                "Grant the reporter read access to the restored database",
                "Assist with extracting correct account_status values and patching the live database",
                "Drop the restored database after the patch is verified",
            ],
            reporter_name="Nina Patel",
            reporter_email="nina.patel@contoso.com",
            reporter_department="Client Services",
            channel=Channel.CHAT,
            created_at="2026-03-18T11:55:00Z",
            tags=["sql", "restore", "data-corruption"],
            difficulty="medium",
        ),
        # ------------------------------------------------------------------
        # ds-014  Legacy NFS mount failing
        # ------------------------------------------------------------------
        ScenarioDefinition(
            scenario_id="ds-014",
            subject="NFS mount to legacy quant server not working after reboot",
            description=(
                "After a scheduled reboot of our quant research server quant-ws-03 (Ubuntu 22.04,"
                " Singapore office), the NFS mount to nfs-quant-sg01:/data/models is not coming"
                " back up. Running 'mount -a' gives 'mount.nfs: access denied by server'. Nothing"
                " changed in /etc/fstab. The other two quant workstations can still mount fine."
                " This is blocking model backtesting work."
            ),
            category=Category.DATA_STORAGE,
            priority=Priority.P3,
            team=Team.DATA_PLATFORM,
            needs_escalation=False,
            missing_info=[
                MissingInfo.ERROR_MESSAGE,
                MissingInfo.CONFIGURATION_DETAILS,
            ],
            next_best_action=(
                "Check the NFS server's /etc/exports for the client IP of quant-ws-03. The server"
                " may have picked up a new IP after reboot if using DHCP."
            ),
            remediation_steps=[
                "Verify the IP address of quant-ws-03 — check if it changed after reboot",
                "Check /etc/exports on nfs-quant-sg01 for allowed client IPs",
                "If IP changed, update the NFS export or assign a static IP to the workstation",
                "Run 'exportfs -ra' on the NFS server to reload the exports",
                "Test the mount with 'mount -v -t nfs nfs-quant-sg01:/data/models /mnt/models'",
                "Add the mount to monitoring to catch future failures after reboots",
            ],
            reporter_name="Wei Tan",
            reporter_email="wei.tan@contoso.com",
            reporter_department="Quantitative Analysis",
            channel=Channel.EMAIL,
            created_at="2026-03-18T02:30:00Z",
            tags=["nfs", "linux", "singapore"],
            difficulty="medium",
        ),
        # ------------------------------------------------------------------
        # ds-015  SMB share permission denied
        # ------------------------------------------------------------------
        ScenarioDefinition(
            scenario_id="ds-015",
            subject="Permission denied accessing \\\\contoso-fs02\\legal-docs",
            description=(
                "I'm getting 'Access is denied' when trying to open \\\\contoso-fs02\\legal-docs"
                " from my laptop. I had access last week and nothing has changed on my end. I'm in"
                " the Legal department and I need to get to our contract templates for an urgent"
                " deal closing today. Other people on my team can still access it."
            ),
            category=Category.DATA_STORAGE,
            priority=Priority.P3,
            team=Team.DATA_PLATFORM,
            needs_escalation=False,
            missing_info=[
                MissingInfo.STEPS_TO_REPRODUCE,
                MissingInfo.DEVICE_INFO,
            ],
            next_best_action=(
                "Check the user's Active Directory group memberships to see if they were"
                " inadvertently removed from the security group that grants access to the share."
            ),
            remediation_steps=[
                "Verify the user's AD group memberships against the share's ACL",
                "Check if the user's account was modified during a recent access review",
                "Re-add the user to the appropriate security group if removed",
                "Ask the user to log off and log back in to refresh their Kerberos token",
                "Verify access is restored by browsing the share",
            ],
            reporter_name="Catherine Dawson",
            reporter_email="catherine.dawson@contoso.com",
            reporter_department="Legal",
            channel=Channel.CHAT,
            created_at="2026-03-18T09:45:00Z",
            tags=["smb", "file-share", "permissions"],
            difficulty="easy",
        ),
        # ------------------------------------------------------------------
        # ds-016  Azure storage account nearing capacity
        # ------------------------------------------------------------------
        ScenarioDefinition(
            scenario_id="ds-016",
            subject="Azure storage account at 4.8 TB — approaching 5 TB limit",
            description=(
                "We received an Azure Monitor alert that storage account stlogsarchiveprod in"
                " rg-logging-prod (eastus2) is at 4.8 TB out of the 5 PB standard limit, but the"
                " storage costs are ballooning. We're storing 3+ years of application logs as"
                " append blobs. We need a lifecycle management policy to tier old logs to cool/archive"
                " or delete them after the retention period. Monthly cost is already $1,200 and"
                " growing 10% month-over-month."
            ),
            category=Category.DATA_STORAGE,
            priority=Priority.P3,
            team=Team.DATA_PLATFORM,
            needs_escalation=False,
            missing_info=[
                MissingInfo.CONFIGURATION_DETAILS,
                MissingInfo.BUSINESS_IMPACT,
            ],
            next_best_action=(
                "Review the current blob inventory and implement an Azure Blob lifecycle management"
                " policy to tier logs older than 90 days to Cool and older than 365 days to Archive."
            ),
            remediation_steps=[
                "Run a blob inventory report to understand the age distribution of stored logs",
                "Confirm the required retention period with the compliance team",
                "Create a lifecycle management policy to move blobs >90 days to Cool tier",
                "Add a rule to move blobs >365 days to Archive tier",
                "Add a rule to delete blobs exceeding the retention period",
                "Monitor the cost reduction over the next billing cycle",
            ],
            reporter_name="Ahmed Hassan",
            reporter_email="ahmed.hassan@contoso.com",
            reporter_department="Cloud Infrastructure",
            channel=Channel.PORTAL,
            created_at="2026-03-18T10:30:00Z",
            tags=["azure-storage", "lifecycle", "cost-optimization"],
            difficulty="medium",
        ),
        # ------------------------------------------------------------------
        # ds-017  SQL database approaching size limit
        # ------------------------------------------------------------------
        ScenarioDefinition(
            scenario_id="ds-017",
            subject="Trade history DB is 230 GB out of 250 GB max — running out of space",
            description=(
                "The trade-history database on tradedb-prod-sql (rg-trading-prod, eastus2) is at"
                " 230 GB and our max size is 250 GB on the current Business Critical tier. At the"
                " current growth rate we'll hit the ceiling in about two weeks. We need to either"
                " scale up the tier, archive old trades, or both. Trades older than 5 years can be"
                " moved to a cheaper archive DB per our retention policy."
            ),
            category=Category.DATA_STORAGE,
            priority=Priority.P3,
            team=Team.DATA_PLATFORM,
            needs_escalation=False,
            missing_info=[
                MissingInfo.BUSINESS_IMPACT,
            ],
            next_best_action=(
                "Archive trades older than 5 years to a separate archive database or Azure Blob"
                " storage, then evaluate if the remaining growth rate still requires a tier upgrade."
            ),
            remediation_steps=[
                "Identify trade data older than 5 years and estimate its size",
                "Create an archive database or export historical data to Parquet in blob storage",
                "Migrate historical trade records out of the production database",
                "Rebuild indexes and reclaim space after the data migration",
                "Assess whether the freed space provides sufficient runway or if a tier change is needed",
                "Set up Azure Monitor alerts for database size at 80% and 90% thresholds",
            ],
            reporter_name="Kevin O'Brien",
            reporter_email="kevin.obrien@contoso.com",
            reporter_department="Trading",
            channel=Channel.EMAIL,
            created_at="2026-03-18T12:15:00Z",
            tags=["sql", "capacity", "archive", "trading"],
            difficulty="medium",
        ),
        # ------------------------------------------------------------------
        # ds-018  Data migration request — on-prem to Azure
        # ------------------------------------------------------------------
        ScenarioDefinition(
            scenario_id="ds-018",
            subject="Request to migrate on-prem Oracle DB to Azure SQL Managed Instance",
            description=(
                "We'd like to kick off planning for migrating our on-premises Oracle 19c database"
                " (fund-accounting, ~500 GB) from the Singapore data center to Azure SQL Managed"
                " Instance. The database supports the Fund Administration team's core workflows."
                " We have a 6-month timeline per our cloud migration roadmap. Can you help assess"
                " compatibility and provide a migration plan? We'll need minimal downtime during"
                " the cutover since this runs 24/5."
            ),
            category=Category.DATA_STORAGE,
            priority=Priority.P4,
            team=Team.DATA_PLATFORM,
            needs_escalation=False,
            missing_info=[
                MissingInfo.ENVIRONMENT_DETAILS,
                MissingInfo.CONFIGURATION_DETAILS,
                MissingInfo.AFFECTED_USERS,
            ],
            next_best_action=(
                "Schedule a discovery session to assess the Oracle schema for Azure SQL MI"
                " compatibility using Azure Database Migration Service and the Data Migration"
                " Assistant tool."
            ),
            remediation_steps=[
                "Run Azure Data Migration Assistant against the Oracle schema for compatibility assessment",
                "Document PL/SQL dependencies, linked servers, and Oracle-specific features",
                "Design the target Azure SQL MI architecture (tier, region, networking)",
                "Create a migration plan with test, pilot, and cutover phases",
                "Set up Azure Database Migration Service for continuous data replication",
                "Perform the cutover during a maintenance window with rollback plan",
            ],
            reporter_name="Aiko Tanaka",
            reporter_email="aiko.tanaka@contoso.com",
            reporter_department="Fund Administration",
            channel=Channel.EMAIL,
            created_at="2026-03-18T04:00:00Z",
            tags=["migration", "oracle", "azure-sql-mi", "singapore"],
            difficulty="hard",
        ),
        # ------------------------------------------------------------------
        # ds-019  Azure VM unreachable after reboot
        # ------------------------------------------------------------------
        ScenarioDefinition(
            scenario_id="ds-019",
            subject="Azure VM unreachable after scheduled reboot",
            description=(
                "The VM vm-reporting-prod-01 in rg-reporting-prod (uksouth) hasn't come back online"
                " after last night's scheduled maintenance reboot. RDP and SSH both time out. Azure"
                " portal shows the VM status as 'Running' but serial console shows it stuck on a"
                " disk check. This VM hosts our London reporting ETL scheduler and nothing is"
                " running until it's back."
            ),
            category=Category.DATA_STORAGE,
            priority=Priority.P2,
            team=Team.DATA_PLATFORM,
            needs_escalation=True,
            missing_info=[
                MissingInfo.SCREENSHOT_OR_ATTACHMENT,
            ],
            next_best_action=(
                "Use the Azure serial console to interact with the disk check process. If the disk"
                " check is hung, force a restart or attach the OS disk to a recovery VM."
            ),
            remediation_steps=[
                "Connect to the VM via Azure serial console to observe the boot process",
                "If stuck on disk check, allow it to complete or skip it if safe",
                "If the VM cannot boot, stop it and attach the OS disk to a recovery VM",
                "Run chkdsk or fsck from the recovery VM to repair the disk",
                "Reattach the OS disk and start the original VM",
                "Verify the ETL scheduler service is running after the VM comes back online",
            ],
            reporter_name="Oliver Grant",
            reporter_email="oliver.grant@contoso.com",
            reporter_department="Data Engineering",
            channel=Channel.PORTAL,
            created_at="2026-03-18T07:15:00Z",
            tags=["azure-vm", "boot-failure", "london", "etl"],
            difficulty="medium",
        ),
        # ------------------------------------------------------------------
        # ds-020  Microsoft Purview access request
        # ------------------------------------------------------------------
        ScenarioDefinition(
            scenario_id="ds-020",
            subject="Need access to Purview data catalog for data classification project",
            description=(
                "I'm leading a data classification initiative for the Compliance team and need"
                " Data Curator role access to our Microsoft Purview account (purview-contoso-prod)."
                " I need to create and manage sensitivity labels, register new data sources, and"
                " set up classification rules. My manager has approved this — happy to provide"
                " email confirmation if needed."
            ),
            category=Category.DATA_STORAGE,
            priority=Priority.P4,
            team=Team.DATA_PLATFORM,
            needs_escalation=False,
            missing_info=[
                MissingInfo.BUSINESS_IMPACT,
            ],
            next_best_action=(
                "Verify the reporter's role in the compliance team and manager approval, then"
                " grant the Data Curator role in Microsoft Purview's access control."
            ),
            remediation_steps=[
                "Confirm the reporter's identity and role in the Compliance department",
                "Request written manager approval via email for audit trail",
                "Grant Data Curator role in Purview account access control (IAM)",
                "Provide documentation on Purview data classification best practices",
                "Schedule a brief onboarding session if the user is new to Purview",
            ],
            reporter_name="Fatima Al-Rashid",
            reporter_email="fatima.alrashid@contoso.com",
            reporter_department="Compliance",
            channel=Channel.PORTAL,
            created_at="2026-03-18T09:50:00Z",
            tags=["purview", "data-catalog", "access-request", "compliance"],
            difficulty="easy",
        ),
        # ------------------------------------------------------------------
        # ds-021  SQL database access request for new service account
        # ------------------------------------------------------------------
        ScenarioDefinition(
            scenario_id="ds-021",
            subject="New service account needs read access to client-profiles DB",
            description=(
                "Hi,\n\nWe're deploying a new microservice (client-notifications-svc) to AKS and it"
                " needs read-only access to the client-profiles database in rg-clientsvc-prod. The"
                " service will use a managed identity (MI) — the identity name is"
                " mi-client-notifications-prod. Can you create a contained database user for this"
                " MI with db_datareader role? We're targeting a go-live next Wednesday."
            ),
            category=Category.DATA_STORAGE,
            priority=Priority.P3,
            team=Team.DATA_PLATFORM,
            needs_escalation=False,
            missing_info=[
                MissingInfo.ENVIRONMENT_DETAILS,
                MissingInfo.CONFIGURATION_DETAILS,
            ],
            next_best_action=(
                "Verify the managed identity exists in Entra ID and create a contained database user"
                " mapped to it with db_datareader permissions on the client-profiles database."
            ),
            remediation_steps=[
                "Verify the managed identity mi-client-notifications-prod exists in Entra ID",
                "Connect to client-profiles database as a DB admin",
                "Create a contained database user: CREATE USER [mi-client-notifications-prod] FROM EXTERNAL PROVIDER",
                "Grant db_datareader role: ALTER ROLE db_datareader ADD MEMBER [mi-client-notifications-prod]",
                "Provide the connection string format to the development team",
                "Test connectivity from a staging AKS pod using the managed identity",
            ],
            reporter_name="Raj Krishnan",
            reporter_email="raj.krishnan@contoso.com",
            reporter_department="Backend Engineering",
            channel=Channel.PORTAL,
            created_at="2026-03-18T14:30:00Z",
            tags=["sql", "access-request", "managed-identity", "aks"],
            difficulty="medium",
        ),
        # ------------------------------------------------------------------
        # ds-022  Cosmos DB high RU consumption and throttling
        # ------------------------------------------------------------------
        ScenarioDefinition(
            scenario_id="ds-022",
            subject="Cosmos DB throttling — 429 errors spiking on user-sessions container",
            description=(
                "We're seeing a surge of HTTP 429 (Request rate too large) errors on the"
                " user-sessions container in Cosmos DB account cosmos-webapp-prod (rg-webapp-prod,"
                " eastus2). It started around 09:00 UTC when we launched a new marketing campaign"
                " that drove a spike in user logins. We provisioned 10,000 RU/s on this container"
                " but it looks like we're hitting 25,000+ RU/s. Our web app is returning 500 errors"
                " to users."
            ),
            category=Category.DATA_STORAGE,
            priority=Priority.P1,
            team=Team.DATA_PLATFORM,
            needs_escalation=True,
            missing_info=[
                MissingInfo.AFFECTED_USERS,
            ],
            next_best_action=(
                "Immediately scale up the provisioned RU/s on the user-sessions container or enable"
                " autoscale to handle the traffic spike. Investigate the partition key for hot spots."
            ),
            remediation_steps=[
                "Increase provisioned throughput to 30,000 RU/s or enable autoscale (max 30,000 RU/s)",
                "Check the partition key heat map in Cosmos DB metrics for hot partitions",
                "Review the most expensive queries using Cosmos DB diagnostic logs",
                "Optimize queries that consume excessive RUs (add indexes, reduce cross-partition queries)",
                "Coordinate with the marketing team to understand expected traffic patterns",
                "Implement retry-with-backoff in the application's Cosmos DB SDK configuration",
            ],
            reporter_name="Sophie Martin",
            reporter_email="sophie.martin@contoso.com",
            reporter_department="Frontend Engineering",
            channel=Channel.CHAT,
            created_at="2026-03-18T09:08:00Z",
            tags=["cosmosdb", "throttling", "429", "production"],
            difficulty="hard",
        ),
        # ------------------------------------------------------------------
        # ds-023  ADLS Gen2 permissions for data science team
        # ------------------------------------------------------------------
        ScenarioDefinition(
            scenario_id="ds-023",
            subject="Need RBAC access to ADLS Gen2 for ML training data",
            description=(
                "Our data science team needs read/write access to the container 'ml-training-data'"
                " in storage account stmldataprod (rg-datascience-prod, eastus2). Specifically, we"
                " need Storage Blob Data Contributor assigned to the Entra security group"
                " sg-datascience-ml. We also need the Databricks service principal"
                " spn-dbw-ml-prod to have Storage Blob Data Reader for the same container."
                " Currently we're getting 403 errors when trying to read from notebooks."
            ),
            category=Category.DATA_STORAGE,
            priority=Priority.P3,
            team=Team.DATA_PLATFORM,
            needs_escalation=False,
            missing_info=[
                MissingInfo.AUTHENTICATION_METHOD,
            ],
            next_best_action=(
                "Assign the requested RBAC roles at the container scope in the storage account"
                " IAM blade. Verify that the storage account has hierarchical namespace enabled"
                " and that ACLs don't conflict."
            ),
            remediation_steps=[
                "Verify the security group sg-datascience-ml exists and contains the correct members",
                "Assign Storage Blob Data Contributor to sg-datascience-ml scoped to the ml-training-data container",
                "Assign Storage Blob Data Reader to spn-dbw-ml-prod scoped to the same container",
                "Verify hierarchical namespace is enabled and check for conflicting POSIX ACLs",
                "Test access from a Databricks notebook using the service principal",
                "Confirm the data science team can read and write from their local tools",
            ],
            reporter_name="Diana Reyes",
            reporter_email="diana.reyes@contoso.com",
            reporter_department="Data Science",
            channel=Channel.EMAIL,
            created_at="2026-03-18T11:20:00Z",
            tags=["adls", "rbac", "data-lake", "databricks"],
            difficulty="medium",
        ),
        # ------------------------------------------------------------------
        # ds-024  Power BI dataset refresh failure
        # ------------------------------------------------------------------
        ScenarioDefinition(
            scenario_id="ds-024",
            subject="Power BI dataset refresh failing — exec dashboard shows stale data",
            description=(
                "The 'Executive KPI Dashboard' Power BI dataset hasn't refreshed since Friday. The"
                " scheduled refresh at 06:00 UTC is failing with 'Data source error: The credentials"
                " provided for the SQL source are invalid.' The dataset connects to the analytics"
                " data warehouse analytics-dw-prod via a gateway. The CFO is presenting to the"
                " board tomorrow morning and needs current numbers. Please help ASAP."
            ),
            category=Category.DATA_STORAGE,
            priority=Priority.P2,
            team=Team.DATA_PLATFORM,
            needs_escalation=True,
            missing_info=[
                MissingInfo.AUTHENTICATION_METHOD,
                MissingInfo.ERROR_MESSAGE,
            ],
            next_best_action=(
                "Check the data gateway credentials for the analytics-dw-prod data source in the"
                " Power BI service. The service account password may have expired or been rotated."
            ),
            remediation_steps=[
                "Open Power BI service > Settings > Datasets > Executive KPI Dashboard",
                "Check the data source credentials and gateway connection status",
                "Verify the service account password hasn't expired in Active Directory",
                "Update the credentials in the gateway data source configuration",
                "Trigger a manual dataset refresh and monitor for success",
                "Set up a Power BI refresh failure alert to catch future issues earlier",
            ],
            reporter_name="Laura Chen",
            reporter_email="laura.chen@contoso.com",
            reporter_department="Executive Operations",
            channel=Channel.PHONE,
            created_at="2026-03-18T08:00:00Z",
            tags=["power-bi", "dataset-refresh", "executive", "gateway"],
            difficulty="medium",
        ),
        # ------------------------------------------------------------------
        # ds-025  Blob storage SAS token expired
        # ------------------------------------------------------------------
        ScenarioDefinition(
            scenario_id="ds-025",
            subject="SAS token expired on partner data drop container",
            description=(
                "Our external audit partner (Deloitte) reported that the SAS token they use to"
                " upload files to the 'audit-drops' container in storage account stauditprod"
                " (rg-audit-prod) stopped working this morning. They're getting"
                " AuthenticationFailed errors. We issued the token 12 months ago. Can we generate"
                " a new one? We need to restrict it to the audit-drops container only, with write"
                " and list permissions, valid for another 12 months."
            ),
            category=Category.DATA_STORAGE,
            priority=Priority.P3,
            team=Team.DATA_PLATFORM,
            needs_escalation=False,
            missing_info=[
                MissingInfo.CONTACT_INFO,
            ],
            next_best_action=(
                "Generate a new SAS token scoped to the audit-drops container with write and list"
                " permissions, a 12-month expiry, and HTTPS-only restriction. Securely share the"
                " token with the audit partner."
            ),
            remediation_steps=[
                "Verify the existing SAS token has indeed expired by checking its expiry date",
                "Generate a new service SAS token scoped to the audit-drops container",
                "Set permissions to Write and List only, restrict to HTTPS, set 12-month expiry",
                "Securely transmit the new SAS token to the Deloitte contact (not via email)",
                "Log the new token's expiry date and set a renewal reminder for 11 months",
                "Consider migrating to a stored access policy for easier rotation in the future",
            ],
            reporter_name="Gregory Walsh",
            reporter_email="gregory.walsh@contoso.com",
            reporter_department="Internal Audit",
            channel=Channel.EMAIL,
            created_at="2026-03-18T10:45:00Z",
            tags=["blob-storage", "sas-token", "audit", "external-partner"],
            difficulty="easy",
        ),
        # ------------------------------------------------------------------
        # ds-026  Redis cache connection timeout
        # ------------------------------------------------------------------
        ScenarioDefinition(
            scenario_id="ds-026",
            subject="Redis cache connection timeouts impacting trading app",
            description=(
                "The Equity Trading platform is experiencing intermittent Redis connection timeouts"
                " to our Azure Cache for Redis instance redis-trading-prod (rg-trading-prod,"
                " eastus2, Premium P2). The app uses Redis for session state and real-time quote"
                " caching. Timeouts started about an hour ago and happen on ~30% of requests."
                " Server load on the Redis metrics blade shows 85%. Memory usage is at 92%. Traders"
                " are complaining about slow page loads and stale quotes."
            ),
            category=Category.DATA_STORAGE,
            priority=Priority.P1,
            team=Team.DATA_PLATFORM,
            needs_escalation=True,
            missing_info=[
                MissingInfo.AFFECTED_USERS,
                MissingInfo.CONFIGURATION_DETAILS,
            ],
            next_best_action=(
                "Check the Redis metrics for memory pressure and eviction rates. Scale up to P3 or"
                " enable clustering to distribute the load. Identify any large keys consuming"
                " excessive memory."
            ),
            remediation_steps=[
                "Review Azure Cache for Redis metrics: server load, memory, connected clients, evictions",
                "Identify large keys using redis-cli --bigkeys or Azure Monitor",
                "Clear expired or unnecessary cache entries to reduce memory pressure immediately",
                "Scale up from P2 to P3 or enable Redis clustering for horizontal scaling",
                "Review the application's cache TTL settings to prevent unbounded memory growth",
                "Set up alerts for server load >70% and memory usage >80%",
            ],
            reporter_name="Anthony Brooks",
            reporter_email="anthony.brooks@contoso.com",
            reporter_department="Equity Trading",
            channel=Channel.PHONE,
            created_at="2026-03-18T14:45:00Z",
            tags=["redis", "cache", "trading", "performance", "production"],
            difficulty="hard",
        ),
        # ------------------------------------------------------------------
        # ds-027  Elasticsearch disk space critical
        # ------------------------------------------------------------------
        ScenarioDefinition(
            scenario_id="ds-027",
            subject="Elasticsearch cluster disk watermark exceeded — read-only mode",
            description=(
                "Our Elasticsearch cluster (es-logs-prod, 5 nodes on Azure VMs in eastus2) has"
                " entered read-only mode because the high disk watermark (90%) was breached. All"
                " new log ingestion from our microservices is failing. The cluster stores application"
                " logs and we have about 6 months of indices. The oldest 3 months are rarely queried."
                " We need to get ingestion working again before we start losing log data."
            ),
            category=Category.DATA_STORAGE,
            priority=Priority.P2,
            team=Team.DATA_PLATFORM,
            needs_escalation=False,
            missing_info=[
                MissingInfo.ENVIRONMENT_DETAILS,
            ],
            next_best_action=(
                "Delete the oldest indices to free disk space immediately, then clear the read-only"
                " flag. Set up Index Lifecycle Management to prevent recurrence."
            ),
            remediation_steps=[
                "Identify the oldest indices and their sizes using the _cat/indices API",
                "Delete indices older than 3 months to free disk space below the watermark",
                "Clear the read-only flag: PUT _all/_settings with index.blocks.read_only_allow_delete=null",
                "Verify log ingestion resumes by checking the ingest pipeline metrics",
                "Configure Index Lifecycle Management (ILM) to auto-delete indices >90 days",
                "Consider adding data nodes or attaching larger managed disks for future growth",
            ],
            reporter_name="Chris Novak",
            reporter_email="chris.novak@contoso.com",
            reporter_department="DevOps",
            channel=Channel.CHAT,
            created_at="2026-03-18T03:20:00Z",
            tags=["elasticsearch", "disk-space", "logging"],
            difficulty="medium",
        ),
        # ------------------------------------------------------------------
        # ds-028  ETL produced wrong data in dashboard
        # ------------------------------------------------------------------
        ScenarioDefinition(
            scenario_id="ds-028",
            subject="Revenue numbers in daily report are wrong — ETL data quality issue",
            description=(
                "The daily revenue report for March 17 is showing $42M in total revenue, but our"
                " manual checks indicate it should be around $38M. We suspect the ETL pipeline in"
                " ADF (adf-finance-prod) double-counted some wire transfer entries. The Finance"
                " team noticed the discrepancy during the morning review. This report goes to the"
                " CFO and the board uses these numbers, so accuracy is critical. We need to identify"
                " what went wrong, correct the data, and re-run the affected report."
            ),
            category=Category.DATA_STORAGE,
            priority=Priority.P2,
            team=Team.DATA_PLATFORM,
            needs_escalation=True,
            missing_info=[
                MissingInfo.AFFECTED_SYSTEM,
                MissingInfo.TIMESTAMP,
            ],
            next_best_action=(
                "Compare source system totals against the data warehouse figures for March 17 to"
                " isolate where the duplication occurred. Check ADF pipeline run logs for retry or"
                " duplicate activity runs."
            ),
            remediation_steps=[
                "Query the source system to get the authoritative revenue total for March 17",
                "Compare against the data warehouse staging and final tables to find the discrepancy",
                "Check ADF pipeline run history for duplicate or retried copy activities",
                "Identify and remove the duplicate wire transfer records in the warehouse",
                "Re-run the downstream report refresh with corrected data",
                "Add deduplication logic or idempotency checks to the ETL pipeline",
            ],
            reporter_name="Patricia Fernandez",
            reporter_email="patricia.fernandez@contoso.com",
            reporter_department="Finance",
            channel=Channel.PHONE,
            created_at="2026-03-18T08:30:00Z",
            tags=["etl", "data-quality", "finance", "revenue"],
            difficulty="hard",
        ),
        # ------------------------------------------------------------------
        # ds-029  Legal hold / regulatory archive request
        # ------------------------------------------------------------------
        ScenarioDefinition(
            scenario_id="ds-029",
            subject="Request to place legal hold on Project Artemis data",
            description=(
                "The Legal department needs a litigation hold placed on all data related to"
                " 'Project Artemis' effective immediately. This includes emails, SharePoint"
                " documents, OneDrive files, and any SQL database records associated with the"
                " project. The matter reference is LIT-2026-0042. Please ensure no data is"
                " deleted or modified under any retention policy until further notice. This is"
                " a regulatory requirement and we need confirmation once the hold is in place."
            ),
            category=Category.DATA_STORAGE,
            priority=Priority.P2,
            team=Team.DATA_PLATFORM,
            needs_escalation=True,
            missing_info=[
                MissingInfo.AFFECTED_SYSTEM,
                MissingInfo.AFFECTED_USERS,
            ],
            next_best_action=(
                "Create an eDiscovery case in Microsoft Purview with the matter reference and place"
                " custodian holds on all identified data sources associated with Project Artemis."
            ),
            remediation_steps=[
                "Create an eDiscovery case in Microsoft Purview with reference LIT-2026-0042",
                "Identify all custodians associated with Project Artemis",
                "Place holds on custodian mailboxes, OneDrive accounts, and SharePoint sites",
                "Coordinate with the Data Platform team to freeze relevant SQL database backups",
                "Suspend any lifecycle or retention policies that could affect held data",
                "Provide written confirmation to the Legal department with hold details",
            ],
            reporter_name="Richard Thornton",
            reporter_email="richard.thornton@contoso.com",
            reporter_department="Legal",
            channel=Channel.EMAIL,
            created_at="2026-03-18T11:00:00Z",
            tags=["legal-hold", "ediscovery", "compliance", "regulatory"],
            difficulty="hard",
        ),
        # ------------------------------------------------------------------
        # ds-030  Data purge request per retention policy
        # ------------------------------------------------------------------
        ScenarioDefinition(
            scenario_id="ds-030",
            subject="Request to purge customer data per GDPR right to erasure",
            description=(
                "We received a GDPR Article 17 right-to-erasure request from a former client"
                " (reference GDPR-2026-0089). We need to purge all personally identifiable"
                " information for this individual from our systems including the CRM database,"
                " the client-profiles SQL DB, any data lake entries, and archived backups. The"
                " Privacy team has verified the request and confirmed there are no legal holds"
                " blocking the deletion. We have a 30-day compliance window."
            ),
            category=Category.DATA_STORAGE,
            priority=Priority.P3,
            team=Team.DATA_PLATFORM,
            needs_escalation=False,
            missing_info=[
                MissingInfo.AFFECTED_SYSTEM,
                MissingInfo.CONTACT_INFO,
            ],
            next_best_action=(
                "Identify all systems containing the individual's PII using the data catalog."
                " Execute the deletion in each system and generate a compliance certificate."
            ),
            remediation_steps=[
                "Use Microsoft Purview data catalog to locate all stores containing the individual's PII",
                "Verify no legal holds or regulatory exceptions apply (confirmed by Privacy team)",
                "Execute PII deletion in the CRM database per the documented erasure procedure",
                "Remove records from client-profiles SQL DB and ADLS Gen2 data lake",
                "Request backup team to exclude the individual's data from future restores",
                "Generate a data erasure certificate and send it to the Privacy team for the GDPR log",
            ],
            reporter_name="Isabelle Dupont",
            reporter_email="isabelle.dupont@contoso.com",
            reporter_department="Regulatory Affairs",
            channel=Channel.PORTAL,
            created_at="2026-03-18T13:00:00Z",
            tags=["gdpr", "data-purge", "privacy", "compliance"],
            difficulty="hard",
        ),
    ]
