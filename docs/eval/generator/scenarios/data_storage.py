"""Data & Storage scenario definitions."""

from generator.models import Scenario

SCENARIOS: list[Scenario] = [
    Scenario(
        scenario_id="data-db-connection-timeout",
        category="Data & Storage",
        priority="P2",
        assigned_team="Data Platform",
        needs_escalation=False,
        missing_information=["error_message", "environment_details", "timestamp"],
        subjects=[
            "Database connection timeouts across multiple services",
            "Azure SQL connection pool exhaustion — apps timing out",
            "Getting SQL connection timeout errors in production",
            "Intermittent database connection failures since this morning",
        ],
        descriptions=[
            "Several of our microservices are throwing SqlException: 'Connection Timeout Expired' when trying to reach "
            "the Azure SQL managed instance in East US 2. The connection pool is maxing out at 200 connections and new "
            "requests are being queued. Started around 9:15 AM and is impacting our loan processing API.",
            "We're seeing intermittent connection timeout errors on our primary Azure SQL Database (contoso-prod-sql). "
            "The ADO.NET connection pool is exhausted and our app service instances are returning 500 errors. About 30%"
            " of requests are failing. Our connection string has Connect Timeout=30 but even bumping it doesn't help.",
            "Production services are failing to connect to Azure SQL. Error: 'A transport-level error has occurred when"
            " receiving results from the server. (provider: TCP Provider, error: 0 - An existing connection was forcibl"
            "y closed by the remote host.)'. Multiple teams affected including payments and onboarding.",
        ],
        next_best_actions=[
            "Check Azure SQL DTU/vCore utilization and active session count in Azure Portal. Review connection pool "
            "settings and identify long-running queries holding connections.",
            "Investigate Azure SQL resource health, check for blocking queries, and review application connection pool "
            "configuration across affected services.",
        ],
        remediation_steps=[
            [
                "Check Azure SQL resource health blade and DTU/vCore metrics for saturation",
                "Run sys.dm_exec_requests and sys.dm_exec_sessions to identify blocking or long-running queries",
                "Kill any runaway sessions if safe to do so with ALTER DATABASE SCOPED CONFIGURATION",
                "Review application connection pool settings (Max Pool Size, Connection Timeout, Connection Lifetime)",
                "Scale up the Azure SQL tier temporarily if resource limits are hit",
                "Implement connection retry logic with exponential backoff in affected services",
                "Monitor recovery and confirm error rates return to baseline",
            ],
        ],
    ),
    Scenario(
        scenario_id="data-etl-pipeline-failure",
        category="Data & Storage",
        priority="P2",
        assigned_team="Data Platform",
        needs_escalation=False,
        missing_information=["error_message", "environment_details", "timestamp"],
        subjects=[
            "ADF pipeline failed — nightly data load didn't complete",
            "Data Factory pipeline failure on production ETL",
            "Synapse pipeline stuck in 'InProgress' for 6 hours",
            "ETL job failed — downstream reports have stale data",
        ],
        descriptions=[
            "Our nightly Azure Data Factory pipeline 'PL_IngestLoanApplications' failed at the Copy Activity stage with"
            " error: 'ErrorCode=UserErrorFailedToConnectToSqlServer, The server was not found or was not accessible.' T"
            "he pipeline normally completes by 4 AM but it failed at 2:37 AM. Downstream Power BI reports are showing y"
            "esterday's data.",
            "The Synapse pipeline that loads our data warehouse has been stuck in 'InProgress' status for over 6 hours."
            " The Data Flow activity appears to be hung processing the customer transactions dataset (~450 GB). No erro"
            "rs in the log, just no progress. This blocks all morning reporting.",
            "Azure Data Factory orchestration pipeline 'PL_DailyETL_Master' failed on the Databricks notebook activity."
            " The linked service authentication token appears to have expired. This is the third time this quarter. All"
            " 12 child pipelines are in a failed state and finance needs the reconciliation data by 10 AM.",
        ],
        next_best_actions=[
            "Review ADF/Synapse pipeline run details and activity error output. Check linked service connectivity and "
            "credentials. Assess whether a manual rerun is safe.",
            "Investigate pipeline failure root cause in Monitor hub, verify linked service configurations, and "
            "coordinate manual rerun with data consumers.",
        ],
        remediation_steps=[
            [
                "Open Azure Data Factory or Synapse Studio Monitor hub and review the failed pipeline run details",
                "Identify the specific activity that failed and examine the error output and diagnostic logs",
                "Check linked service connectivity — test connection to source and sink data stores",
                "If credential expiry, rotate the service principal secret or managed identity token",
                "Fix the root cause (network, auth, schema drift, or resource limits)",
                "Trigger a manual pipeline rerun and monitor to completion",
                "Notify downstream data consumers once the load is complete and data is current",
            ],
        ],
    ),
    Scenario(
        scenario_id="data-backup-job-failed",
        category="Data & Storage",
        priority="P1",
        assigned_team="Data Platform",
        needs_escalation=True,
        missing_information=["error_message", "environment_details", "business_impact"],
        subjects=[
            "URGENT: Production database backup job failed overnight",
            "Azure SQL automated backup failed — RPO at risk",
            "Critical: backup retention gap on production Cosmos DB",
            "Production backup failure — no successful backup in 24+ hours",
        ],
        descriptions=[
            "Our Azure SQL production database 'contoso-core-prod' has not had a successful automated backup in over 26"
            " hours. The Azure Backup vault shows the last three backup jobs failed with 'UserErrorDatabaseBackupOperat"
            "ionFailed'. We are now outside our RPO window of 24 hours. This is a regulatory compliance issue for our f"
            "inancial data.",
            "The geo-redundant backup for our primary production SQL Managed Instance failed. Azure portal shows backup"
            " storage utilization at 100% of the allocated 4 TB limit. No point-in-time restore available for the last "
            "18 hours. Audit and compliance team has been notified.",
            "Received an Azure Service Health alert that continuous backup on our Cosmos DB account 'contoso-prod-cosmo"
            "s' is failing. Error indicates insufficient throughput to complete the backup snapshot. Our disaster recov"
            "ery plan requires backups every 4 hours and we've missed the last three windows.",
        ],
        next_best_actions=[
            "Immediately investigate backup failure root cause. Assess RPO compliance gap and initiate emergency "
            "backup. Escalate to Azure support if platform-side issue.",
            "Determine backup failure cause, trigger manual backup to close the RPO gap, and engage Azure support for "
            "persistent backup infrastructure issues.",
        ],
        remediation_steps=[
            [
                "Review Azure Backup vault or database backup history for specific error codes",
                "Check backup storage quota and increase allocation if storage limit was hit",
                "Verify the managed identity or service principal used for backup has required RBAC roles",
                "Trigger an immediate manual backup to close the RPO gap",
                "If platform issue, open a Sev A Azure support ticket with backup diagnostic logs",
                "Confirm backup completes successfully and verify restore point availability",
                "Document the RPO compliance gap and notify the risk and compliance team",
                "Review backup monitoring alerts to ensure future failures are caught immediately",
            ],
        ],
    ),
    Scenario(
        scenario_id="data-storage-quota-exceeded",
        category="Data & Storage",
        priority="P3",
        assigned_team="Data Platform",
        needs_escalation=False,
        missing_information=["affected_system", "environment_details"],
        subjects=[
            "Azure storage account hitting quota limit",
            "Blob storage capacity warning — 95% utilized",
            "ADLS Gen2 storage account approaching limit",
            "Need storage quota increase for data lake",
        ],
        descriptions=[
            "Our primary ADLS Gen2 storage account 'contosodatalakeprod' is at 93% capacity (4.65 TB of 5 TB "
            "provisioned). We're ingesting about 50 GB/day from IoT sensors and trading feeds. At this rate we'll hit "
            "the limit in about two weeks. Need to either increase the quota or implement a lifecycle management "
            "policy.",
            "Azure Monitor fired a storage capacity alert on our blob storage account. We're at 4.2 TB out of the 5 TB "
            "soft limit. The biggest container is 'raw-market-data' at 2.8 TB. Most of the data is over 90 days old and"
            " could potentially be tiered to Cool or Archive.",
            "Getting 'StorageAccountQuotaExceeded' errors when trying to upload files to our Azure Data Lake. The "
            "ingest pipeline for the risk analytics team has been failing since last night. We need an immediate quota "
            "bump while we work on a longer-term archival strategy.",
        ],
        next_best_actions=[
            "Analyze storage usage by container and age. Implement Azure Blob Lifecycle Management policies to tier or "
            "delete stale data. Request quota increase if needed.",
            "Review ADLS storage utilization, identify candidates for archival or deletion, and configure lifecycle "
            "management rules.",
        ],
        remediation_steps=[
            [
                "Review storage account capacity metrics in Azure Monitor and identify top containers by size",
                "Analyze data age distribution using Azure Storage Explorer or Blob Inventory",
                "Configure Azure Blob Lifecycle Management policies to move data older than 90 days to Cool tier",
                "Archive or delete data older than retention policy requires",
                "If immediate relief needed, request a storage account quota increase via Azure support",
                "Set up Azure Monitor alerts at 80% and 90% capacity thresholds",
                "Document data retention and tiering policy for the team",
            ],
        ],
    ),
    Scenario(
        scenario_id="data-recovery-deleted-files",
        category="Data & Storage",
        priority="P3",
        assigned_team="Data Platform",
        needs_escalation=False,
        missing_information=["affected_system", "timestamp", "affected_users"],
        subjects=[
            "Need to recover accidentally deleted files from blob storage",
            "Data recovery request — files deleted from ADLS",
            "Accidentally purged a container in storage account",
            "Recover deleted data from Azure Data Lake",
        ],
        descriptions=[
            "A team member accidentally ran an azcopy delete command against the wrong container in our ADLS Gen2 "
            "account yesterday around 3 PM. The container 'processed-claims-2024' had about 200 GB of parquet files "
            "that our analytics team depends on. We need these files recovered ASAP for month-end reporting.",
            "I accidentally deleted a folder 'risk-models/v2/' from our Azure Data Lake Storage account this morning. I"
            "t contained ~50 GB of trained model artifacts that took 3 weeks to generate. Soft delete might be enabled "
            "but I'm not sure. We need to recover these files before Friday.",
            "Someone on the data engineering team overwrote the production reference data files in our blob storage acc"
            "ount. The original files had mappings for 15,000 financial instruments. We need the version from before 10"
            " AM today. Is blob versioning enabled on this account?",
        ],
        next_best_actions=[
            "Check if soft delete or blob versioning is enabled on the storage account. Attempt recovery from "
            "soft-deleted snapshots or previous versions. If not available, check Azure Backup vault.",
            "Verify soft delete and versioning configuration, attempt data restoration, and if unrecoverable, explore "
            "backup or pipeline re-derivation options.",
        ],
        remediation_steps=[
            [
                "Check if blob soft delete is enabled on the storage account and the retention period",
                "If soft delete is active, use Azure Portal or az CLI to undelete the blobs within the retention"
                " window",
                "If blob versioning is enabled, restore from a previous version of the affected blobs",
                "If neither is available, check the Azure Backup vault for a recovery point",
                "As a last resort, determine if data can be re-derived by rerunning upstream ETL pipelines",
                "After recovery, enable soft delete (14-day retention) and blob versioning to prevent future data loss",
                "Review RBAC permissions to restrict delete operations on critical containers",
            ],
        ],
    ),
    Scenario(
        scenario_id="data-sql-performance-degradation",
        category="Data & Storage",
        priority="P2",
        assigned_team="Data Platform",
        needs_escalation=False,
        missing_information=["error_message", "timestamp", "environment_details"],
        subjects=[
            "Azure SQL query performance severely degraded",
            "Production SQL database running extremely slow",
            "Azure SQL DTU maxed out — application response times spiking",
            "Database performance issue — queries taking 10x longer than normal",
        ],
        descriptions=[
            "Our Azure SQL Database 'contoso-trading-prod' (Business Critical tier, 8 vCores) has been experiencing sev"
            "ere performance degradation since 11 AM. Queries that normally take 200ms are now taking 5-10 seconds. The"
            " DTU usage is at 98% and we're seeing heavy wait stats on PAGEIOLATCH_SH. The trading desk is unable to pr"
            "ocess orders in a timely manner.",
            "Performance on our Azure SQL Managed Instance has dropped off a cliff. Query Store shows multiple plan "
            "regressions after last night's index maintenance job ran. The CPU is pegged at 95% and tempdb is growing "
            "rapidly. About 500 users across the wealth management team are affected.",
            "Our loan origination system backed by Azure SQL is responding very slowly. The application insights dashbo"
            "ard shows P95 latency went from 300ms to 12 seconds starting at 10:30 AM. We suspect a missing index or pa"
            "rameter sniffing issue on the GetLoanApplicationsByStatus stored procedure.",
        ],
        next_best_actions=[
            "Check Azure SQL Performance Insight and Query Store for regressed queries. Identify top resource-consuming"
            " queries and review execution plans for missing indexes or plan regressions.",
            "Analyze DTU/vCore consumption, review Query Store for plan regressions, and check for blocking chains or "
            "missing indexes.",
        ],
        remediation_steps=[
            [
                "Open Azure SQL Performance Insight to identify top resource-consuming queries",
                "Review Query Store for plan regressions and force a known-good execution plan if applicable",
                "Check sys.dm_exec_query_stats and sys.dm_os_wait_stats for blocking and wait type analysis",
                "Apply missing index recommendations from sys.dm_db_missing_index_details",
                "If parameter sniffing, add OPTION (RECOMPILE) or OPTIMIZE FOR hints to affected queries",
                "Scale up the Azure SQL tier temporarily if immediate relief is needed",
                "Monitor query performance and confirm latency returns to baseline",
            ],
        ],
    ),
    Scenario(
        scenario_id="data-cosmos-hot-partition",
        category="Data & Storage",
        priority="P2",
        assigned_team="Data Platform",
        needs_escalation=False,
        missing_information=["error_message", "environment_details", "configuration_details"],
        subjects=[
            "Cosmos DB hot partition causing request throttling",
            "429 errors on Cosmos DB — partition key skew",
            "Cosmos DB throughput exceeded on specific logical partition",
            "Cosmos DB request rate too large — suspected hot partition",
        ],
        descriptions=[
            "Our Cosmos DB container 'customer-transactions' is returning HTTP 429 'Request rate too large' errors even"
            " though the provisioned throughput is 50,000 RU/s. Metrics show one logical partition is consuming 80% of "
            "the throughput. The partition key is '/customerId' and a few high-volume institutional clients are generat"
            "ing disproportionate traffic.",
            "We're seeing heavy throttling on our Cosmos DB account 'contoso-events-prod'. The normalized RU consumptio"
            "n metric shows one physical partition spiking to 100% while others are at 10-15%. We partitioned by '/tena"
            "ntId' but one tenant generates 60% of all writes during market hours.",
            "Application logs show thousands of 429 errors from Cosmos DB since the market opened at 9:30 AM. Our throu"
            "ghput is set to autoscale max 100,000 RU/s but the hot partition can only use a fraction. The trading acti"
            "vity container partitioned on '/accountId' has severe key skew.",
        ],
        next_best_actions=[
            "Analyze partition key distribution using Cosmos DB Insights. Evaluate partition key strategy and consider "
            "introducing a synthetic partition key or hierarchical partitioning.",
            "Review normalized RU consumption per partition, identify the hot key(s), and plan a partition key redesign"
            " or implement throughput redistribution.",
        ],
        remediation_steps=[
            [
                "Open Cosmos DB Insights and review normalized RU consumption per physical partition",
                "Identify the hot logical partition key values using diagnostic logs",
                "As immediate mitigation, increase provisioned throughput or enable autoscale with higher maximum",
                "Evaluate hierarchical partition keys (preview) to distribute the hot partition's load",
                "Consider a synthetic partition key (e.g., customerId + date suffix) for better distribution",
                "If redesign is needed, plan a data migration to a new container with an improved partition key",
                "Implement client-side rate limiting for high-volume tenants to prevent monopolizing throughput",
            ],
        ],
    ),
    Scenario(
        scenario_id="data-blob-access-denied",
        category="Data & Storage",
        priority="P3",
        assigned_team="Data Platform",
        needs_escalation=False,
        missing_information=["error_message", "affected_users", "authentication_method"],
        subjects=[
            "Access denied when reading from blob storage",
            "403 Forbidden on Azure Blob Storage — can't access files",
            "Storage account access issue — AuthorizationPermissionMismatch",
            "Can't access data lake files — permission denied",
        ],
        descriptions=[
            "Our data pipeline service principal is getting 'AuthorizationPermissionMismatch' (HTTP 403) when trying to"
            " read from the 'curated-financial-data' container in ADLS Gen2. This was working fine until yesterday. We "
            "haven't changed any permissions. The ADF pipeline 'PL_CuratedToSynapse' is blocked.",
            "Getting 'This request is not authorized to perform this operation using this permission' when accessing "
            "blob storage from our Databricks workspace. The storage account has firewall rules enabled and the "
            "Databricks VNet was recently migrated. Suspect the service endpoint or private endpoint config changed.",
            "Users in the analytics team are reporting 403 errors when trying to access parquet files in the data lake "
            "via Azure Storage Explorer. They had access yesterday. We recently rotated the storage account access keys"
            " — could that have invalidated some SAS tokens?",
        ],
        next_best_actions=[
            "Check RBAC role assignments and ACLs on the storage account. Verify firewall rules and network "
            "configuration. If SAS tokens in use, check for key rotation invalidation.",
            "Review storage account access control (RBAC, ACLs, SAS), network rules, and recent configuration changes.",
        ],
        remediation_steps=[
            [
                "Check the storage account IAM blade for RBAC role assignments on the affected identity",
                "If ADLS Gen2, verify filesystem-level and directory-level ACL permissions",
                "Review storage account firewall and virtual network rules for recent changes",
                "If SAS tokens are in use, verify they haven't been invalidated by a key rotation",
                "Check if a private endpoint or service endpoint configuration was modified",
                "Restore appropriate RBAC roles (e.g., Storage Blob Data Reader/Contributor) as needed",
                "Test access and confirm the pipeline or users can read/write successfully",
            ],
        ],
    ),
    Scenario(
        scenario_id="data-lake-query-slow",
        category="Data & Storage",
        priority="P3",
        assigned_team="Data Platform",
        needs_escalation=False,
        missing_information=["environment_details", "configuration_details", "steps_to_reproduce"],
        subjects=[
            "Data lake queries extremely slow in Synapse serverless",
            "Synapse serverless SQL pool queries taking forever",
            "ADLS query performance terrible — 45 minutes for simple query",
            "Slow query on data lake — Spark jobs timing out",
        ],
        descriptions=[
            "Queries on our Synapse serverless SQL pool against the data lake are taking 45+ minutes for what should be"
            " a 2-minute scan. We're querying partitioned parquet files in 'adls://contosodatalake/curated/transactions"
            "/' partitioned by year/month/day. The query plan shows a full scan instead of partition pruning. This is b"
            "locking the finance team's ad-hoc analytics.",
            "Our Databricks Spark jobs reading from ADLS Gen2 are timing out after 2 hours. The dataset is ~800 GB of "
            "parquet files but most queries only need the last 7 days. Partition pushdown doesn't seem to be working "
            "and the cluster is scanning the entire dataset. We're on a Standard_DS4_v2 cluster with 8 workers.",
            "The data analytics team reports that their Synapse serverless queries on the data lake have been extremely"
            " slow this week. The same query that took 3 minutes last week now takes 30+ minutes. The data volume hasn'"
            "t changed significantly. Suspect small file problem from recent micro-batch ingestion changes.",
        ],
        next_best_actions=[
            "Analyze query execution plans for partition elimination and predicate pushdown. Check for small file "
            "proliferation and file format optimization opportunities.",
            "Review Synapse/Spark query plans, verify partition pruning is working, and investigate small file problem "
            "or file format issues.",
        ],
        remediation_steps=[
            [
                "Review the query execution plan to check if partition pruning is occurring",
                "Verify the folder structure follows a Hive-compatible partition layout (e.g., /year=2024/month=01/)",
                "Check for small file problem — compact files using Spark repartition or OPTIMIZE in Delta Lake",
                "Ensure parquet files have appropriate row group sizing (target 128 MB per file)",
                "Add appropriate WHERE clauses to enable partition elimination",
                "Consider converting to Delta Lake format for automatic file compaction and Z-ordering",
                "If using Synapse serverless, create external tables with proper partition definitions",
            ],
        ],
    ),
    Scenario(
        scenario_id="data-sharepoint-storage-limit",
        category="Data & Storage",
        priority="P3",
        assigned_team="Data Platform",
        needs_escalation=False,
        missing_information=["affected_system", "affected_users", "business_impact"],
        subjects=[
            "SharePoint site storage limit reached — can't upload files",
            "SharePoint Online out of space — team site full",
            "Need more storage for SharePoint document library",
            "SharePoint site collection at capacity — blocking work",
        ],
        descriptions=[
            "The Wealth Management team SharePoint site has hit its 25 GB storage quota. Team members are unable to upl"
            "oad new client documents and are getting 'You're almost out of space' warnings. We have about 40 people wh"
            "o use this site daily to share client-facing reports and compliance documents.",
            "Our SharePoint site for the regulatory compliance team is at 100% capacity. We can't upload new audit "
            "documents which is a compliance risk. The site has accumulated 5 years of versioned Word and Excel files. "
            "We need either a storage increase or a way to archive old documents.",
            "Getting 'The site is out of storage space' errors on our investment research SharePoint site. Analysts "
            "can't save their research reports. The document library has about 60,000 files and version history is "
            "probably consuming a huge amount of the storage.",
        ],
        next_best_actions=[
            "Audit SharePoint site storage usage by library and version history. Trim excessive version history and "
            "archive old content. Request site quota increase if justified.",
            "Analyze storage consumption, clean up version history and recycle bin, and increase site quota as needed.",
        ],
        remediation_steps=[
            [
                "Run a SharePoint storage metrics report to identify libraries consuming the most space",
                "Review and trim version history — reduce from unlimited to 50 major versions",
                "Empty the site recycle bin and second-stage recycle bin to reclaim space immediately",
                "Archive documents older than the retention policy to an Azure Blob-backed archive",
                "Increase the site collection storage quota in SharePoint admin center",
                "Educate users on using OneDrive for personal files vs. SharePoint for team collaboration",
                "Set up storage usage alerts to proactively manage capacity going forward",
            ],
        ],
    ),
    Scenario(
        scenario_id="data-mailbox-quota-full",
        category="Data & Storage",
        priority="P4",
        assigned_team="Data Platform",
        needs_escalation=False,
        missing_information=["affected_users", "contact_info"],
        subjects=[
            "Mailbox full — can't send or receive emails",
            "Email quota exceeded — mailbox is full",
            "Outlook says my mailbox is full, can't receive emails",
            "Need mailbox storage increase — hitting 50 GB limit",
        ],
        descriptions=[
            "My Outlook mailbox is showing 'Your mailbox is full' and I can't send or receive new emails. I'm on the "
            "standard 50 GB Exchange Online plan. I have a lot of emails with large attachments from client "
            "communications that I need to keep for regulatory compliance reasons.",
            "I keep getting warnings that my mailbox is almost full. I'm at 49.5 GB out of 50 GB. I've tried cleaning "
            "up but most of these emails are client correspondence that I need to retain per our 7-year financial "
            "records policy. Can I get an increase or an archive mailbox enabled?",
            "Can't receive new emails — Outlook says my mailbox is over the limit. I work in client services and get hu"
            "ndreds of emails with PDF attachments daily. I need a solution that keeps me within compliance but frees u"
            "p space.",
        ],
        next_best_actions=[
            "Enable Exchange Online archive mailbox. Apply retention policies to move older items to the archive. "
            "Review large items and clean up Deleted Items folder.",
            "Activate online archive mailbox and configure auto-expanding archive. Help user clean up large items for "
            "immediate relief.",
        ],
        remediation_steps=[
            [
                "Enable the Exchange Online auto-expanding archive mailbox for the user",
                "Apply a default retention policy to move items older than 2 years to the archive",
                "Empty the Deleted Items and Junk Email folders for immediate space recovery",
                "Use Outlook's Mailbox Cleanup tool to find and remove large attachments",
                "Educate the user on saving attachments to OneDrive/SharePoint instead of keeping in email",
                "Confirm the user can send and receive emails again after cleanup",
            ],
        ],
    ),
    Scenario(
        scenario_id="data-db-migration-failing",
        category="Data & Storage",
        priority="P2",
        assigned_team="Data Platform",
        needs_escalation=False,
        missing_information=["error_message", "environment_details", "steps_to_reproduce"],
        subjects=[
            "Database migration to Azure SQL failing midway",
            "DMS migration stuck — on-premises SQL to Azure SQL",
            "Azure Database Migration Service errors during cutover",
            "Database migration failing with schema compatibility errors",
        ],
        descriptions=[
            "We're using Azure Database Migration Service to migrate our on-premises SQL Server 2019 database to Azure "
            "SQL Managed Instance. The migration has been stuck at 'Applying changes' for 12 hours with no progress. "
            "The source database is 2 TB and we had a cutover window planned for this weekend.",
            "Our DMS migration keeps failing at the schema migration phase with 'Msg 40544: The database has reached it"
            "s size quota' on the Azure SQL target. The source is 800 GB but the target tier only supports 500 GB. We n"
            "eed to figure out if we should tier up or optimize the schema first.",
            "Database migration from SQL Server 2016 to Azure SQL is failing with compatibility errors. Getting errors "
            "about SQL CLR assemblies and cross-database queries that aren't supported in Azure SQL. We've been "
            "planning this migration for 3 months and the cutover is scheduled for next Saturday.",
        ],
        next_best_actions=[
            "Review DMS migration logs for specific error details. Address schema compatibility issues or sizing "
            "constraints. Validate migration readiness with Data Migration Assistant.",
            "Analyze migration failure logs, resolve compatibility blockers, and replan cutover timeline if needed.",
        ],
        remediation_steps=[
            [
                "Review Azure Database Migration Service activity logs for specific error codes",
                "Run Data Migration Assistant (DMA) assessment against the source database for compatibility issues",
                "Address identified compatibility blockers (CLR assemblies, cross-DB queries, unsupported features)",
                "Verify target Azure SQL tier has sufficient storage, compute, and feature support",
                "Scale up the target instance if storage quota is the blocker",
                "Restart the DMS migration with corrected configuration",
                "Validate data integrity post-migration using row counts, checksums, and application smoke tests",
            ],
        ],
    ),
    Scenario(
        scenario_id="data-replication-lag",
        category="Data & Storage",
        priority="P2",
        assigned_team="Data Platform",
        needs_escalation=False,
        missing_information=["error_message", "environment_details", "timestamp"],
        subjects=[
            "Azure SQL read replica replication lag increasing",
            "Geo-replication lag on secondary database is hours behind",
            "Read replicas showing stale data — replication delay",
            "Cosmos DB multi-region replication lag spiking",
        ],
        descriptions=[
            "Our Azure SQL geo-secondary in West US 2 is showing a replication lag of 45 minutes and climbing. The "
            "primary in East US 2 is processing heavy batch workloads. Our reporting services read from the secondary "
            "and are showing stale data. The compliance team flagged discrepancies in real-time risk reports.",
            "Cosmos DB multi-region writes are experiencing significant replication lag between East US and West Europe"
            " regions. The conflict resolution metrics show increasing conflicts and the bounded staleness consistency "
            "level shows a lag of 200,000 versions (our threshold is 100,000). Customer-facing APIs in Europe are retur"
            "ning outdated portfolio data.",
            "The read replica for our Azure SQL Hyperscale database is falling behind. sys.dm_database_replica_states "
            "shows redo_queue_size growing steadily at 50 GB. The reporting dashboards that read from the replica are "
            "showing data that's 2 hours old. Business users are making decisions on stale data.",
        ],
        next_best_actions=[
            "Monitor replication health metrics and identify the bottleneck (network, compute, or write volume). Reduce"
            " write pressure on primary or scale up the replica.",
            "Investigate replication lag metrics, check for resource bottlenecks on the replica, and consider "
            "temporarily redirecting read traffic to the primary.",
        ],
        remediation_steps=[
            [
                "Check replication lag metrics in Azure Monitor (redo_queue_size, replication_lag_sec)",
                "Identify if the primary is under heavy write load from batch jobs or maintenance",
                "Verify the secondary/replica has sufficient compute resources to keep up with redo",
                "Scale up the read replica tier if compute is the bottleneck",
                "Consider pausing non-critical batch workloads on the primary to reduce write volume",
                "If Cosmos DB, review consistency level and conflict resolution policy",
                "Monitor replication lag until it returns to acceptable thresholds (< 5 seconds for SQL, < 10,000 "
                "versions for Cosmos DB)",
            ],
        ],
    ),
    Scenario(
        scenario_id="data-corruption-detected",
        category="Data & Storage",
        priority="P1",
        assigned_team="Data Platform",
        needs_escalation=True,
        missing_information=["error_message", "timestamp", "business_impact", "affected_system"],
        subjects=[
            "CRITICAL: Data corruption detected in production database",
            "DBCC CHECKDB found corruption on production SQL instance",
            "Data integrity errors — production database corrupted",
            "Urgent: checksum errors on production database pages",
        ],
        descriptions=[
            "DBCC CHECKDB on our production Azure SQL Managed Instance 'contoso-core-prod' returned errors: 'Msg 8928: "
            "Object ID 1205579333, index ID 1, partition ID 72057594512424960: Page (1:892456) could not be processed. "
            "See other errors for details.' This is the core transaction database handling $2M+ in daily trades. We "
            "need to assess the scope and restore clean data immediately.",
            "Our nightly consistency check detected corruption in the 'AccountBalances' table of the production databas"
            "e. DBCC CHECKDB reports 14 pages with checksum errors in a clustered index. The table has 8 million rows a"
            "nd is used in real-time balance calculations. We cannot afford data loss on financial records.",
            "Application is throwing 'The operating system returned error 38(Reached the end of the file.) to SQL "
            "Server during a read' on specific queries against the portfolio holdings table. Suspect underlying "
            "page-level corruption. The table is critical for client portfolio valuations.",
        ],
        next_best_actions=[
            "Immediately assess corruption scope with DBCC CHECKDB. Isolate affected tables from write operations. "
            "Prepare for point-in-time restore from last known good backup. Escalate to Azure support.",
            "Run full DBCC CHECKDB WITH NO_INFOMSGS, ALL_ERRORMSGS to scope the damage. Plan emergency restore from "
            "backup. Open Sev A Azure support case.",
        ],
        remediation_steps=[
            [
                "Run DBCC CHECKDB WITH NO_INFOMSGS, ALL_ERRORMSGS to get a complete corruption assessment",
                "Document all affected objects, pages, and indexes from the CHECKDB output",
                "Determine if corruption is isolated to non-clustered indexes (rebuildable) or data pages (requires "
                "restore)",
                "If index-only corruption, rebuild the affected indexes with ALTER INDEX REBUILD",
                "If data page corruption, initiate a point-in-time restore to a new database from the last clean"
                " backup",
                "Compare restored data against the corrupted database to identify data loss scope",
                "Open a Sev A Azure support ticket to investigate root cause (storage subsystem issue)",
                "After restore, run DBCC CHECKDB to confirm the restored database is clean",
                "Update the application connection strings to point to the restored database after validation",
            ],
        ],
    ),
    Scenario(
        scenario_id="data-archive-retrieval",
        category="Data & Storage",
        priority="P4",
        assigned_team="Data Platform",
        needs_escalation=False,
        missing_information=["affected_system", "timestamp", "business_impact"],
        subjects=[
            "Need to retrieve files from Azure Archive storage",
            "Request to rehydrate data from archive tier",
            "Cold storage data retrieval for audit request",
            "Need archived data restored for regulatory inquiry",
        ],
        descriptions=[
            "Our compliance team needs access to archived trading records from Q2 2022 for an SEC inquiry. The data was"
            " moved to Azure Archive tier about 18 months ago. The container is 'archived-trading-records' and we need "
            "approximately 500 GB rehydrated. The SEC has given us a 30-day deadline.",
            "Finance team needs archived transaction logs from 2021 for an internal audit. The data is in Azure Blob Ar"
            "chive tier in container 'historical-transactions-2021'. Approximately 200 GB needs to be moved back to a r"
            "eadable tier. This is not urgent but needs to be done within 2 weeks.",
            "Need to retrieve 3 years of archived client correspondence from Azure cool/archive storage for a "
            "regulatory examination. The data is spread across multiple containers in the 'contoso-archive-storage' "
            "account. Estimated 1.2 TB total. What's the fastest and most cost-effective retrieval option?",
        ],
        next_best_actions=[
            "Initiate blob rehydration from Archive tier. Use Standard priority (up to 15 hours) unless urgency "
            "requires High priority (under 1 hour). Calculate retrieval cost estimate.",
            "Start rehydration of archived blobs with appropriate priority level and provide estimated time and cost to"
            " the requester.",
        ],
        remediation_steps=[
            [
                "Identify the specific containers and blob prefixes that need rehydration",
                "Calculate the estimated retrieval cost (per-GB charge for Archive rehydration)",
                "Choose rehydration priority: Standard (up to 15 hours) or High (under 1 hour, higher cost)",
                "Initiate batch rehydration using Set Blob Tier API or azcopy",
                "Monitor rehydration progress via blob properties (x-ms-rehydrate-priority)",
                "Notify the requesting team once data is available in Hot or Cool tier",
                "Set a reminder to move the data back to Archive tier after the review period ends",
            ],
        ],
    ),
    Scenario(
        scenario_id="data-log-storage-filling",
        category="Data & Storage",
        priority="P2",
        assigned_team="Data Platform",
        needs_escalation=False,
        missing_information=["affected_system", "environment_details"],
        subjects=[
            "Log Analytics workspace storage at 90% — filling fast",
            "Azure Monitor logs consuming excessive storage",
            "Log storage almost full — need retention policy changes",
            "Application logs filling up disk — 90%+ capacity",
        ],
        descriptions=[
            "Our Log Analytics workspace 'contoso-prod-logs' is at 92% of the daily cap (95 GB of 100 GB/day). We're in"
            "gesting logs from 200+ Azure resources, AKS clusters, and Application Insights. If we hit the cap, we'll l"
            "ose visibility into production systems during business hours. Costs have also ballooned to $15K/month.",
            "The diagnostic logs storage account is at 4.7 TB of 5 TB. We've been storing raw diagnostic logs from all "
            "Azure services for 2 years without any lifecycle policy. The AKS container logs alone account for 2.1 TB. "
            "We need to get this under control before we lose the ability to write new logs.",
            "Azure Monitor alerted that our Log Analytics workspace hit the daily ingestion cap at 2 PM. We've lost all"
            " log visibility for the rest of the day. Multiple teams can't troubleshoot production issues. We need to e"
            "ither increase the cap or reduce noisy log sources immediately.",
        ],
        next_best_actions=[
            "Analyze log ingestion by source and table using Log Analytics Usage metrics. Reduce verbose logging, "
            "configure data collection rules, and implement retention policies.",
            "Identify top log volume contributors, apply ingestion-time transformations to reduce volume, and adjust "
            "retention periods by table.",
        ],
        remediation_steps=[
            [
                "Query the Usage table in Log Analytics to identify the top data volume contributors by solution and "
                "data type",
                "Review AKS container logs — filter out verbose debug/info level logs at the source using Data "
                "Collection Rules",
                "Configure table-level retention policies (e.g., 30 days for verbose logs, 90 days for security logs)",
                "Implement ingestion-time transformations to drop or filter low-value log fields",
                "Increase the daily cap temporarily if log loss is impacting production visibility",
                "Set up Basic Logs tier for high-volume, low-query tables to reduce cost",
                "Archive logs older than 90 days to a storage account for long-term retention at lower cost",
            ],
        ],
    ),
    Scenario(
        scenario_id="data-keyvault-access-denied",
        category="Data & Storage",
        priority="P1",
        assigned_team="Data Platform",
        needs_escalation=False,
        missing_information=["error_message", "affected_system", "environment_details"],
        subjects=[
            "Azure Key Vault access denied — data services can't read secrets",
            "Key Vault 403 error blocking production data pipelines",
            "URGENT: Services can't access encryption keys in Key Vault",
            "Key Vault firewall blocking data platform service principal",
        ],
        descriptions=[
            "Our Azure Data Factory and Databricks workloads are failing because they can't read connection strings "
            "from Azure Key Vault 'contoso-data-kv-prod'. Error: 'Access denied. Caller was not found on any access "
            "policy.' This is blocking all production ETL pipelines. We recently migrated the Key Vault from access "
            "policies to Azure RBAC — something may have been missed.",
            "Production services are unable to retrieve encryption keys from Key Vault. The Azure SQL Transparent Data "
            "Encryption (TDE) customer-managed key rotation failed and now the database is inaccessible. Error: "
            "'AzureKeyVaultServiceError: The user, group or application does not have keys get permission on key "
            "vault.' This is a P1 — the entire trading platform database is offline.",
            "All our Synapse pipelines failed simultaneously with Key Vault access errors. The managed identity for the"
            " Synapse workspace lost access to Key Vault after a network security change. The Key Vault firewall was up"
            "dated to restrict to specific VNets and the Synapse managed VNet wasn't included.",
        ],
        next_best_actions=[
            "Immediately check Key Vault access policies or RBAC assignments for the affected service principals. "
            "Verify network access rules include the calling services. Restore access to unblock production.",
            "Review Key Vault access control configuration and network rules. Restore the required permissions for data"
            " platform service identities.",
        ],
        remediation_steps=[
            [
                "Check the Key Vault access configuration model (access policy vs. Azure RBAC)",
                "Verify the affected service principal or managed identity has the required role (Key Vault Secrets "
                "User, Key Vault Crypto User)",
                "If RBAC, assign the appropriate role at the Key Vault scope",
                "If access policies, add the service principal with Get/List permissions for secrets and keys",
                "Check Key Vault firewall rules — ensure the calling service's VNet or IP is allowed",
                "Add Synapse/ADF managed VNet to Key Vault network rules if using private endpoints",
                "Test access from the affected service and confirm pipelines can retrieve secrets",
                "Review Key Vault diagnostic logs to identify when access was revoked",
            ],
        ],
    ),
    Scenario(
        scenario_id="data-schema-migration-breaking",
        category="Data & Storage",
        priority="P2",
        assigned_team="Data Platform",
        needs_escalation=True,
        missing_information=["error_message", "affected_system", "configuration_details", "business_impact"],
        subjects=[
            "Schema migration broke downstream data consumers",
            "Database schema change causing production API failures",
            "Breaking schema change deployed — multiple services failing",
            "Column rename in production DB breaking downstream reports",
        ],
        descriptions=[
            "A schema migration was deployed to production Azure SQL last night that renamed several columns in the "
            "'Transactions' table (e.g., 'txn_date' → 'transaction_date', 'amt' → 'amount'). This broke the downstream "
            "Synapse views, Power BI reports, and three microservices that query this table. About 15 downstream "
            "consumers are affected.",
            "The data engineering team ran a Flyway migration that added NOT NULL constraints to the 'ClientAccounts' t"
            "able without backfilling existing NULL values. The migration succeeded but now INSERT operations from the "
            "client onboarding API are failing with constraint violations. 200+ API calls have failed since"
            " deployment.",
            "An ALTER TABLE was run on the production 'MarketData' table that changed a DECIMAL(18,2) column to DECIMAL"
            "(18,6). The change itself succeeded but downstream Spark jobs in Databricks are failing because the parque"
            "t schema cached in the Delta Lake metadata doesn't match. The quantitative analytics pipeline is completel"
            "y broken.",
        ],
        next_best_actions=[
            "Assess blast radius of the schema change across all downstream consumers. Coordinate immediate rollback if"
            " possible, or deploy compatibility views/aliases. Notify all affected teams.",
            "Map all downstream dependencies of the changed schema, implement backward-compatible views, and coordinate"
            " remediation across affected teams.",
        ],
        remediation_steps=[
            [
                "Immediately assess the full blast radius — identify all downstream consumers (APIs, reports, "
                "pipelines, views)",
                "If rollback is safe, revert the schema migration using the rollback script",
                "If rollback is not possible, create backward-compatible views or column aliases for the old schema",
                "Notify all affected teams and provide them the new schema mapping",
                "Update downstream Synapse/Spark external table definitions to match the new schema",
                "Fix Power BI dataset connections and refresh affected reports",
                "Implement a schema change review process requiring impact analysis before production deployment",
                "Add schema contract tests to CI/CD pipeline to catch breaking changes before they reach production",
            ],
        ],
    ),
    Scenario(
        scenario_id="data-k8s-pvc-full",
        category="Data & Storage",
        priority="P2",
        assigned_team="Data Platform",
        needs_escalation=False,
        missing_information=["affected_system", "environment_details", "error_message"],
        subjects=[
            "Kubernetes PVC full — pod in CrashLoopBackOff",
            "AKS persistent volume claim out of space",
            "Database pod crashing — PV storage exhausted",
            "Kafka broker PVC at 100% — broker unhealthy",
        ],
        descriptions=[
            "Our PostgreSQL pod running on AKS is in CrashLoopBackOff because the persistent volume claim 'postgres-dat"
            "a-pvc' is at 100% capacity (100 Gi). The pod logs show 'No space left on device' errors. This is the datab"
            "ase backing our portfolio management API and it's completely down.",
            "The Kafka broker pods in our AKS cluster are reporting unhealthy status because the log segment PVCs are "
            "full. Each broker has a 500 Gi Azure Managed Disk PVC and retention is set to 7 days, but a recent spike "
            "in message volume filled them up. Consumer applications are getting 'NotLeaderForPartition' errors.",
            "Our Elasticsearch data nodes on AKS hit the disk watermark flood stage. The PVCs are at 95% capacity and "
            "Elasticsearch has put all indices into read-only mode. Log ingestion is completely blocked and we're "
            "losing observability data. The cluster has 3 data nodes with 200 Gi PVCs each.",
        ],
        next_best_actions=[
            "Expand the PVC using Azure Disk dynamic volume expansion. Clean up unnecessary data if possible. "
            "Investigate root cause of unexpected storage growth.",
            "Resize the persistent volume, clean up data to restore service, and adjust retention policies or "
            "provisioning to prevent recurrence.",
        ],
        remediation_steps=[
            [
                "Check the PVC capacity and usage with kubectl exec and df -h in the affected pod",
                "If Azure Managed Disk, expand the PVC by editing the PersistentVolumeClaim spec (AKS supports online "
                "expansion)",
                "Clean up unnecessary data inside the volume (old logs, temporary files, expired data)",
                "If Kafka, reduce log.retention.hours or log.retention.bytes to free space from old segments",
                "If Elasticsearch, reset the index read-only flag after freeing space: PUT /_all/_settings with "
                "index.blocks.read_only_allow_delete=null",
                "Restart the affected pods after volume expansion and data cleanup",
                "Set up Prometheus alerts on PVC utilization at 80% and 90% thresholds to catch growth early",
            ],
        ],
    ),
    Scenario(
        scenario_id="data-redis-eviction-spike",
        category="Data & Storage",
        priority="P2",
        assigned_team="Data Platform",
        needs_escalation=False,
        missing_information=["error_message", "environment_details", "timestamp"],
        subjects=[
            "Redis cache eviction rate spiking — cache hit ratio dropping",
            "Azure Cache for Redis maxmemory reached — evictions increasing",
            "Redis performance degradation — high eviction rate",
            "Cache miss rate spiking — Redis memory pressure",
        ],
        descriptions=[
            "Our Azure Cache for Redis (Premium P2, 6 GB) is showing an eviction rate of 5,000 keys/minute, up from "
            "near zero last week. The cache hit ratio dropped from 95% to 60%. This is the session cache for our "
            "client-facing trading portal and users are experiencing slow page loads and session drops.",
            "Redis memory usage is at 99.8% on our Azure Cache for Redis instance. The eviction policy is 'allkeys-lru'"
            " and we're seeing massive evictions during market hours (9:30 AM - 4 PM). Response latency spiked from 1ms"
            " to 50ms. The pricing API team reports their rate limit counters are being evicted, causing incorrect thro"
            "ttling.",
            "Application Insights shows a sudden increase in cache misses on our Redis instance. Investigation shows "
            "the memory_rss metric is 5.8 GB on a 6 GB instance. A recent deployment added caching for a new dataset "
            "(customer risk profiles) that appears to be much larger than estimated. The key count went from 2M to 8M "
            "overnight.",
        ],
        next_best_actions=[
            "Analyze Redis memory usage by key pattern. Identify large or unexpected key sets. Scale up the cache tier "
            "or optimize key TTLs and data structures.",
            "Investigate memory consumption by key namespace, optimize data stored in cache,"
            " and scale up if necessary.",
        ],
        remediation_steps=[
            [
                "Connect to Redis and analyze memory usage with MEMORY DOCTOR and INFO memory commands",
                "Use redis-cli --bigkeys or MEMORY USAGE to identify oversized keys and namespaces",
                "Identify the key pattern causing unexpected memory growth (e.g., the new risk profiles dataset)",
                "Optimize key TTLs — ensure all keys have appropriate expiration set",
                "Reduce value sizes using compression or more compact serialization"
                " (e.g., MessagePack instead of JSON)",
                "Scale up to a larger Azure Cache for Redis tier if the working set legitimately needs more memory",
                "Monitor eviction rate and cache hit ratio after changes to confirm recovery",
            ],
        ],
    ),
    Scenario(
        scenario_id="data-kafka-consumer-lag",
        category="Data & Storage",
        priority="P2",
        assigned_team="Data Platform",
        needs_escalation=False,
        missing_information=["error_message", "environment_details", "configuration_details"],
        subjects=[
            "Kafka consumer lag increasing on production topics",
            "Event Hub / Kafka consumer group falling behind",
            "Kafka consumers can't keep up — lag growing steadily",
            "Message backlog building on trading events topic",
        ],
        descriptions=[
            "Consumer lag on our Kafka topic 'trading-events' has been steadily increasing since market open. The "
            "consumer group 'risk-engine-cg' is currently 2.5 million messages behind and growing at ~50K "
            "messages/minute. The consumer instances (6 pods on AKS) appear healthy but throughput has dropped. The "
            "risk calculation engine is operating on stale data.",
            "Our Azure Event Hubs namespace (Kafka-compatible) is showing growing consumer lag on the "
            "'client-transactions' topic. The consumer group is 4 hours behind. We suspect the lag started after a "
            "rebalance event when 2 consumer pods were restarted during a deployment. The partition assignment seems "
            "uneven.",
            "Kafka consumer lag on the 'market-data-feed' topic jumped from near-zero to 10 million messages overnight."
            " The Spark Structured Streaming consumer job appears to be processing at half the normal rate. Checkpoint "
            "writes to ADLS are taking 10x longer than usual. The quant team's real-time pricing models are showing sta"
            "le quotes.",
        ],
        next_best_actions=[
            "Check consumer group health and partition assignment. Verify consumer processing throughput and identify "
            "bottlenecks (deserialization, downstream writes, rebalancing).",
            "Investigate consumer lag root cause — check for rebalancing issues, processing bottlenecks, or partition "
            "skew. Scale consumers if needed.",
        ],
        remediation_steps=[
            [
                "Check consumer group status and partition assignments using kafka-consumer-groups.sh --describe",
                "Verify all consumer instances are healthy and actively fetching from assigned partitions",
                "If partitions are unevenly assigned, trigger a manual rebalance or increase consumer instances",
                "Check consumer processing metrics — identify if the bottleneck is deserialization, business logic, or "
                "downstream writes",
                "If downstream writes are slow (e.g., ADLS checkpoints), investigate the sink performance",
                "Scale up consumer instances to match the number of topic partitions for maximum parallelism",
                "Increase consumer fetch.max.bytes and max.poll.records to improve batch processing throughput",
                "Monitor consumer lag until it returns to near-zero and processing rate exceeds production rate",
            ],
        ],
    ),
    Scenario(
        scenario_id="data-warehouse-cost-spike",
        category="Data & Storage",
        priority="P3",
        assigned_team="Data Platform",
        needs_escalation=False,
        missing_information=["affected_system", "timestamp", "steps_to_reproduce"],
        subjects=[
            "Synapse data warehouse query costs spiked unexpectedly",
            "Azure Synapse bill tripled this month — cost investigation",
            "Databricks compute costs way over budget",
            "Data warehouse costs out of control — need optimization",
        ],
        descriptions=[
            "Our Azure Synapse dedicated SQL pool costs jumped from $8K to $24K this month. The DWU consumption metrics"
            " show sustained high utilization even during off-hours. We suspect someone scheduled a new set of material"
            "ized view refreshes that are running continuously. The finance team is asking for an explanation by end of"
            " week.",
            "The Databricks workspace 'contoso-analytics-prod' racked up $45K in compute costs last month, triple the "
            "normal $15K budget. Most of the spend appears to come from long-running interactive cluster sessions that "
            "weren't terminated. Several all-purpose clusters ran 24/7 even though they were only needed during "
            "business hours.",
            "Synapse serverless SQL pool charges went from $2K to $18K. The TB-processed metric shows a 9x increase. We"
            " discovered a Power BI dataset with DirectQuery mode pointing at serverless pool — every dashboard refresh"
            " scans the entire data lake. About 50 users refresh this report multiple times daily.",
        ],
        next_best_actions=[
            "Analyze cost breakdown by resource and workload using Azure Cost Management. Identify runaway queries, "
            "unmanaged clusters, or inefficient access patterns driving the spike.",
            "Review Synapse/Databricks cost metrics, identify the top cost drivers, and implement controls (auto-pause,"
            " query governors, cluster policies).",
        ],
        remediation_steps=[
            [
                "Review Azure Cost Management breakdown by meter, resource, and time period to pinpoint the cost spike",
                "For Synapse dedicated pool, check DWU utilization and identify queries running during off-hours",
                "For Databricks, review cluster utilization — terminate idle interactive clusters and configure "
                "auto-termination (30 min idle)",
                "Implement Databricks cluster policies to enforce auto-termination, max cluster size, and spot "
                "instances",
                "For Synapse serverless, identify high-TB-scanned queries and optimize with partitioning, file formats,"
                " and result set caching",
                "Convert DirectQuery Power BI datasets to Import mode or add result set caching in Synapse",
                "Configure Azure budget alerts at 50%, 80%, and 100% of monthly target to catch future overruns early",
                "Implement auto-pause on Synapse dedicated SQL pool during nights and weekends",
            ],
        ],
    ),
]
