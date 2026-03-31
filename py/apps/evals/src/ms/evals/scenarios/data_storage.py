# Copyright (c) Microsoft. All rights reserved.
"""Data & Storage scenario templates.

Covers: SharePoint access, OneDrive sync, database access requests,
backup/restore, file share access, ETL pipeline failures, storage quota,
data migration, SQL performance, and data recovery.
"""

from ms.evals.constants import Category
from ms.evals.constants import MissingInfo
from ms.evals.constants import Priority
from ms.evals.constants import Team
from ms.evals.models import ScenarioTemplate
from ms.evals.scenarios.registry import register

# ---------------------------------------------------------------------------
# ds-001  SharePoint site access request
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="ds-001",
        category=Category.DATA,
        priority=Priority.P3,
        assigned_team=Team.DATA_PLATFORM,
        needs_escalation=False,
        missing_information=[MissingInfo.BUSINESS_IMPACT, MissingInfo.AFFECTED_SYSTEM],
        subjects=[
            "Need access to the Contoso Financials SharePoint site",
            "Request access to SharePoint site — Regulatory Filings",
            "SharePoint access request for new project",
        ],
        descriptions=[
            "Hi, I just joined the {department} team last week and I need access to the Contoso "
            "Financials SharePoint site at https://contoso.sharepoint.com/sites/financials. My manager "
            "said I should submit a ticket. I need contributor-level access so I can upload our "
            "quarterly reports. Thanks!",
            "Requesting access to the Regulatory Filings SharePoint site for myself and two other "
            "analysts ({user_name_1} and {user_name_2}). We're starting a new compliance review "
            "project and need to pull historical documents from that library. Read-only access is fine "
            "for now.",
        ],
        next_best_actions=[
            "Verify the user's role and department against the SharePoint site access policy. If the "
            "request aligns with their job function, grant the requested permission level and confirm.",
            "Check if the SharePoint site has an active owner who can approve the request. Route "
            "approval to the site owner or data steward before granting access.",
        ],
        remediation_steps=[
            [
                "Confirm user's identity and department in Entra ID",
                "Verify the requested SharePoint site URL and permission level",
                "Check site access policy and data classification",
                "Submit access request to site owner for approval",
                "Grant access after approval and notify the requester",
            ],
            [
                "Look up the SharePoint site in the data governance catalog",
                "Verify manager approval for the access request",
                "Add user to the appropriate SharePoint permission group",
                "Send confirmation with site URL and any usage guidelines",
                "Log the access grant in the entitlement management system",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# ds-002  OneDrive sync failing for large files
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="ds-002",
        category=Category.DATA,
        priority=Priority.P3,
        assigned_team=Team.DATA_PLATFORM,
        needs_escalation=False,
        missing_information=[MissingInfo.ERROR_MESSAGE, MissingInfo.DEVICE_INFO],
        subjects=[
            "OneDrive not syncing large files",
            "OneDrive sync stuck on big Excel workbook",
            "Large file sync failure — OneDrive for Business",
        ],
        descriptions=[
            "I have a 2.3 GB Excel workbook with our annual forecasting model and OneDrive won't sync "
            "it. The sync icon just spins forever and eventually shows a red X. Smaller files sync fine. "
            "I'm on Windows 11 with the latest OneDrive client. I really need this file available on my "
            "laptop and desktop.",
            "onedrive keeps failing when I try to sync the Q4 budget model (around 1.8gb). it syncs "
            "partway then errors out. I've restarted the client twice. other files work ok. this is "
            "blocking me from working remotely tomorrow.",
        ],
        next_best_actions=[
            "Check the OneDrive sync client version and verify the file is under the 250 GB per-file "
            "limit. Review sync logs for specific error codes and advise on file optimization.",
            "Investigate whether the file path length or special characters are causing the issue. "
            "Recommend splitting the workbook or using SharePoint for files over 2 GB.",
        ],
        remediation_steps=[
            [
                "Verify OneDrive client version is current (Help & Settings > About)",
                "Check OneDrive sync logs at %localappdata%\\Microsoft\\OneDrive\\logs",
                "Confirm file size is within OneDrive limits",
                "Reset OneDrive sync client if logs show corruption",
                "If file is too large, recommend SharePoint upload or file splitting",
            ],
            [
                "Check available local disk space on the user's device",
                "Review file path for length violations (max 400 chars total path)",
                "Test sync with a copy of the file renamed to a shorter name",
                "If issue persists, unlink and relink the OneDrive account",
                "Escalate to Microsoft support if client-side troubleshooting fails",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# ds-003  Database access request for new analyst
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="ds-003",
        category=Category.DATA,
        priority=Priority.P4,
        assigned_team=Team.DATA_PLATFORM,
        needs_escalation=False,
        missing_information=[MissingInfo.BUSINESS_IMPACT, MissingInfo.ENVIRONMENT_DETAILS],
        subjects=[
            "Need read access to the FinancialReporting Azure SQL database",
            "Database access request — new BI analyst",
            "Requesting db permissions for reporting queries",
        ],
        descriptions=[
            "I'm a new business intelligence analyst in {department} and I need read-only access to the "
            "FinancialReporting database on Azure SQL. My manager {user_name_1} approved this verbally. "
            "I'll be running queries for our monthly board reports. I already have SSMS installed.",
            "Can you please set up read access on the analytics databases for me? I was told during "
            "onboarding that I need to submit a ticket for this. I need access to FinancialReporting "
            "and the staging copy of CustomerInsights. I'll only be reading data, no writes needed.",
        ],
        next_best_actions=[
            "Verify manager approval and check the database access control list. If approved, create "
            "a read-only database role assignment for the user's Entra ID account.",
            "Confirm which specific databases and schemas the user needs. Route for manager approval "
            "via the data access request workflow before provisioning.",
        ],
        remediation_steps=[
            [
                "Verify the user's identity and team membership in Entra ID",
                "Confirm manager approval through the access governance workflow",
                "Create or assign the user to a db_datareader role on the target database",
                "Provide connection string and instructions for SSMS or Azure Data Studio",
                "Log the access grant and set a 90-day review reminder",
            ],
            [
                "Identify the exact databases and schemas requested",
                "Check if the user has a valid Entra ID account with MFA enabled",
                "Submit access request through the data governance portal for approval",
                "After approval, add user to the appropriate Azure SQL AAD group",
                "Send confirmation email with connection details and data handling policies",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# ds-004  Backup restore request for deleted files
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="ds-004",
        category=Category.DATA,
        priority=Priority.P2,
        assigned_team=Team.DATA_PLATFORM,
        needs_escalation=False,
        missing_information=[MissingInfo.TIMESTAMP, MissingInfo.AFFECTED_SYSTEM],
        subjects=[
            "Need to restore deleted files from backup",
            "Accidentally deleted folder on shared drive — need restore",
            "URGENT — deleted critical project files, need backup restore",
        ],
        descriptions=[
            "I accidentally deleted the entire Q3-Audit-Workpapers folder from the \\\\contoso-fs01"
            "\\finance share sometime around 2 PM today. There are about 150 files in there that the "
            "audit team needs by end of week. I already checked the Recycle Bin and it's not there. "
            "Can you restore from the nightly backup?",
            "A team member ran a cleanup script on the shared drive and it removed files it shouldn't "
            "have. We're missing everything in the /reports/2024/Q2 directory. The deletion happened "
            "this morning between {timestamp} and 11:00 AM. We need these files back ASAP — there are "
            "deliverables due to the client on Friday.",
        ],
        next_best_actions=[
            "Identify the exact path and approximate deletion time, then check Volume Shadow Copy or "
            "the latest backup snapshot for the affected directory. Initiate restore immediately.",
            "Verify the backup retention policy covers the requested timeframe. Locate the most recent "
            "clean backup and begin a targeted restore of the deleted directory.",
        ],
        remediation_steps=[
            [
                "Confirm the exact file share path and folder name with the requester",
                "Determine the approximate time of deletion for backup selection",
                "Check Volume Shadow Copy (Previous Versions) on the file server first",
                "If shadow copy unavailable, locate the nearest backup in Azure Backup vault",
                "Restore the folder to a temporary location, verify contents, then move to original path",
                "Notify the requester and confirm all files are recovered",
            ],
            [
                "Verify which backup tier contains the requested data (snapshot vs. vault)",
                "Initiate a restore job targeting only the affected directory",
                "Monitor restore progress in the Azure Backup portal",
                "Validate restored file count and integrity against the user's description",
                "Move restored files to the production share and confirm with the team",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# ds-005  ETL pipeline failing — ADLS Gen2 permission error
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="ds-005",
        category=Category.DATA,
        priority=Priority.P2,
        assigned_team=Team.DATA_PLATFORM,
        needs_escalation=False,
        missing_information=[MissingInfo.ERROR_MESSAGE, MissingInfo.ENVIRONMENT_DETAILS],
        subjects=[
            "ETL pipeline failing with ADLS permission error",
            "ADF pipeline — 403 Forbidden on ADLS Gen2 write",
            "Nightly data load broken — storage access denied",
        ],
        descriptions=[
            "Our nightly ETL pipeline (ADF pipeline 'DailyFinancialLoad') started failing last night "
            "with a 403 Forbidden error when writing to the curated container in ADLS Gen2 "
            "(contosodatalake.dfs.core.windows.net). Nothing changed on our end. The pipeline uses a "
            "managed identity. This is blocking the morning dashboard refresh for the finance team.",
            "the adf pipeline that loads data into adls gen2 is broken. getting 'AuthorizationPermission"
            "Mismatch' on the sink dataset. it was working fine until yesterday. i think someone might "
            "have changed the storage account permissions. pipeline name is DailyFinancialLoad and it "
            "runs at 2am EST.",
        ],
        next_best_actions=[
            "Check the ADLS Gen2 access control (IAM and ACLs) for the ADF managed identity. Verify "
            "that Storage Blob Data Contributor role is still assigned. Review recent activity logs.",
            "Review Azure Activity Log for permission changes on the storage account in the last 48 "
            "hours. Restore the managed identity's role assignment if it was removed.",
        ],
        remediation_steps=[
            [
                "Identify the ADF managed identity (system or user-assigned)",
                "Check IAM role assignments on the ADLS Gen2 storage account",
                "Verify ACLs on the specific container and directory path",
                "Review Azure Activity Log for recent permission modifications",
                "Restore the Storage Blob Data Contributor role if missing",
                "Re-run the pipeline and confirm successful execution",
            ],
            [
                "Check the ADF pipeline run history for the exact error message",
                "Verify the managed identity's object ID in Entra ID",
                "Test access using Azure Storage Explorer with the same identity",
                "If role assignment was removed by policy, add an exemption or use a different auth method",
                "Trigger a manual pipeline run and monitor to completion",
            ],
        ],
        attachment_options=[
            ["ADF pipeline run error screenshot", "Activity log export"],
        ],
    )
)

# ---------------------------------------------------------------------------
# ds-006  Storage quota exceeded on OneDrive
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="ds-006",
        category=Category.DATA,
        priority=Priority.P3,
        assigned_team=Team.DATA_PLATFORM,
        needs_escalation=False,
        missing_information=[MissingInfo.BUSINESS_IMPACT],
        subjects=[
            "OneDrive storage full — can't save new files",
            "OneDrive quota exceeded notification",
            "Need more OneDrive storage space",
        ],
        descriptions=[
            "I'm getting a notification that my OneDrive is full and I can't save any new files. I have "
            "1 TB allocated but I store a lot of large data exports for compliance reporting. Is there "
            "any way to increase my quota or should I move some files to SharePoint?",
            "My OneDrive hit 100% capacity. I've already cleaned out old stuff but I genuinely need "
            "the space for work — we deal with large datasets in {department}. Can the limit be "
            "increased or is there an alternative storage option I should use?",
        ],
        next_best_actions=[
            "Review the user's OneDrive storage usage breakdown and advise on archival options. If "
            "justified, increase quota via the SharePoint admin center.",
            "Check if the user has retention policies or version history consuming extra space. Help "
            "optimize storage before considering a quota increase.",
        ],
        remediation_steps=[
            [
                "Check current OneDrive storage usage in the SharePoint admin center",
                "Review version history settings — excessive versions can consume quota",
                "Identify large files or folders that can be archived to SharePoint or ADLS",
                "If quota increase is justified, adjust via Set-SPOSite -StorageQuota",
                "Advise user on best practices for managing OneDrive storage",
            ],
            [
                "Run a storage report for the user's OneDrive in the admin center",
                "Check for retention policies inflating storage with preserved versions",
                "Help the user move shared datasets to a SharePoint document library",
                "Increase quota to the next tier if approved by the user's manager",
                "Set up a storage alert at 90% to prevent future disruptions",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# ds-007  Azure SQL database timeout errors
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="ds-007",
        category=Category.DATA,
        priority=Priority.P1,
        assigned_team=Team.DATA_PLATFORM,
        needs_escalation=True,
        missing_information=[MissingInfo.ERROR_MESSAGE, MissingInfo.AFFECTED_USERS],
        subjects=[
            "CRITICAL — Azure SQL production database timing out",
            "Production SQL database unresponsive — all queries timing out",
            "P1 — Azure SQL FinancialReporting DB timeout errors across all apps",
        ],
        descriptions=[
            "The FinancialReporting Azure SQL database is timing out on ALL queries. This started about "
            "20 minutes ago. Power BI dashboards, our internal trading app, and the reconciliation "
            "service are all affected. The DTU usage is showing 100% in the Azure portal. This is a "
            "production system used by 200+ users across the trading floor. We need immediate help.",
            "URGENT: Production Azure SQL instance (contoso-sql-prod.database.windows.net) is "
            "completely unresponsive. Every application connecting to the FinancialReporting database "
            "is getting timeout errors. We're seeing 'Execution Timeout Expired' across the board. "
            "This is impacting revenue-generating operations on the trading desk.",
        ],
        next_best_actions=[
            "Immediately check DTU/CPU utilization and active sessions in the Azure portal. Identify "
            "and kill any runaway queries. Consider scaling up the service tier as an emergency measure.",
            "Check for blocking chains and long-running transactions in sys.dm_exec_requests. Scale the "
            "database tier if resource exhaustion is confirmed. Engage the DBA on-call.",
        ],
        remediation_steps=[
            [
                "Open Azure portal and check DTU/CPU/memory metrics for the database",
                "Query sys.dm_exec_requests and sys.dm_exec_sessions to identify blocking or runaway queries",
                "Kill the offending sessions using KILL <session_id>",
                "If resource exhaustion persists, scale up the service tier temporarily",
                "Notify affected teams that the issue is being addressed",
                "Conduct a root cause analysis after stabilization",
            ],
            [
                "Check Azure SQL Intelligent Insights for automated diagnostics",
                "Review Query Performance Insight for resource-intensive queries",
                "Identify if a recent deployment introduced a problematic query",
                "Apply query hints or force a good execution plan if a regression is found",
                "Scale the database to a higher tier if current capacity is insufficient",
                "Schedule a post-incident review with the application team",
            ],
        ],
        attachment_options=[
            ["Azure portal DTU metrics screenshot", "Query execution plan"],
            ["sys.dm_exec_requests output", "Application error logs"],
        ],
    )
)

# ---------------------------------------------------------------------------
# ds-008  SharePoint site corrupted after migration
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="ds-008",
        category=Category.DATA,
        priority=Priority.P2,
        assigned_team=Team.DATA_PLATFORM,
        needs_escalation=False,
        missing_information=[MissingInfo.AFFECTED_SYSTEM, MissingInfo.SCREENSHOT_OR_ATTACHMENT],
        subjects=[
            "SharePoint site broken after migration — pages not loading",
            "Corrupted SharePoint site post-migration",
            "SharePoint migration issue — missing lists and broken web parts",
        ],
        descriptions=[
            "We migrated the {department} SharePoint site from on-prem to SharePoint Online last "
            "weekend and now half the pages won't load. Custom web parts are throwing errors, several "
            "document libraries show 0 items even though the files were migrated, and the site "
            "navigation is completely wrong. About 50 people use this site daily.",
            "After the SharePoint migration on Saturday our team site is a mess. List views are broken, "
            "some document libraries are empty, and the custom workflows aren't running. We followed "
            "the migration runbook but something clearly went wrong. The site URL is "
            "https://contoso.sharepoint.com/sites/{department}-team.",
        ],
        next_best_actions=[
            "Review the SharePoint migration logs for errors. Check if document libraries were fully "
            "migrated by comparing item counts with the source. Re-run incremental migration if needed.",
            "Investigate web part errors in the browser developer console and check if custom solutions "
            "need to be redeployed to the SharePoint app catalog.",
        ],
        remediation_steps=[
            [
                "Pull the migration log from the SharePoint Migration Tool (SPMT) or third-party tool",
                "Compare source and destination item counts for each library and list",
                "Re-run incremental migration for any libraries with missing items",
                "Check custom web parts and redeploy to the SharePoint app catalog if needed",
                "Fix site navigation by updating the term store or manual nav links",
                "Validate with the site owner that all content and functionality is restored",
            ],
            [
                "Check the migration tool's error report for failed items",
                "Verify permissions on migrated libraries — permission mapping issues can hide content",
                "Rebuild broken list views using the original view definitions",
                "Test custom workflows and re-create any that didn't migrate",
                "Communicate status to affected users with an estimated resolution time",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# ds-009  Data migration request to new SharePoint site
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="ds-009",
        category=Category.DATA,
        priority=Priority.P4,
        assigned_team=Team.DATA_PLATFORM,
        needs_escalation=False,
        missing_information=[MissingInfo.AFFECTED_SYSTEM, MissingInfo.BUSINESS_IMPACT, MissingInfo.TIMESTAMP],
        subjects=[
            "Request to migrate data to new SharePoint site",
            "Data migration — old team site to new SharePoint Online site",
            "Need help moving files from legacy SharePoint to new site",
        ],
        descriptions=[
            "Our department is consolidating from three old SharePoint sites into one new site. We need "
            "help migrating approximately 500 GB of documents, lists, and page content. The source "
            "sites are on SharePoint 2019 on-prem and the target is SharePoint Online. We'd like to "
            "schedule this for a weekend to minimize disruption. No hard deadline — just want to get "
            "it done this quarter.",
            "We have a legacy SharePoint 2016 site with about 200 GB of documents that needs to be "
            "moved to our new SharePoint Online site. The content is mostly document libraries and a "
            "few custom lists. Can you help plan and execute this migration? We're flexible on timing.",
        ],
        next_best_actions=[
            "Schedule a discovery call to inventory the source content, assess compatibility, and "
            "create a migration plan. Use SPMT or a third-party tool for the migration.",
            "Gather details on the source environment, content volume, and any custom solutions. "
            "Provide a migration timeline estimate and coordinate with the team.",
        ],
        remediation_steps=[
            [
                "Conduct a discovery assessment of source SharePoint content (libraries, lists, pages)",
                "Identify any custom solutions, workflows, or InfoPath forms that need special handling",
                "Create a migration plan with timeline, rollback steps, and communication plan",
                "Run a test migration with a subset of content to validate",
                "Execute full migration during the agreed maintenance window",
                "Validate content integrity and permissions post-migration",
                "Decommission source sites after a 30-day parallel-run period",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# ds-010  Power BI dataset refresh failing
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="ds-010",
        category=Category.DATA,
        priority=Priority.P3,
        assigned_team=Team.DATA_PLATFORM,
        needs_escalation=False,
        missing_information=[MissingInfo.ERROR_MESSAGE, MissingInfo.AFFECTED_SYSTEM],
        subjects=[
            "Power BI dataset refresh failing since yesterday",
            "Scheduled Power BI refresh broken — credential error",
            "Power BI report showing stale data — refresh won't complete",
        ],
        descriptions=[
            "The Power BI dataset 'Executive Dashboard - Finance' hasn't refreshed since yesterday "
            "morning. The scheduled refresh at 6 AM is failing. I checked the refresh history in the "
            "Power BI service and it says 'Data source error' but doesn't give me more details. This "
            "report is used by the CFO's office every morning at 8 AM.",
            "hi, my power bi report is showing data from two days ago. i think the refresh is broken. "
            "the dataset connects to azure sql and adls gen2. i haven't changed anything. can someone "
            "look at it? the workspace is 'Finance - Production' and the dataset is called "
            "'DailyRevenueMetrics'.",
        ],
        next_best_actions=[
            "Check the dataset refresh history in the Power BI admin portal for specific error codes. "
            "Verify that data source credentials haven't expired and the gateway is online.",
            "Test the data source connection from the Power BI service. If using an on-premises gateway, "
            "check its status. Re-enter credentials if they've expired.",
        ],
        remediation_steps=[
            [
                "Open the Power BI service and navigate to the dataset settings",
                "Check the refresh history for specific error messages",
                "Verify data source credentials are current (re-enter if expired)",
                "If using a gateway, confirm the gateway is online and the data source is configured",
                "Trigger a manual refresh to test and monitor for completion",
                "Re-enable the scheduled refresh once the issue is resolved",
            ],
            [
                "Check if the underlying data source (Azure SQL/ADLS) is accessible",
                "Verify the service account or OAuth token used by Power BI hasn't expired",
                "Review gateway logs if the dataset uses an on-premises data gateway",
                "Update credentials and test connectivity from the dataset settings page",
                "Run a manual refresh and confirm the report shows current data",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# ds-011  File share permissions broken after server update
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="ds-011",
        category=Category.DATA,
        priority=Priority.P2,
        assigned_team=Team.DATA_PLATFORM,
        needs_escalation=False,
        missing_information=[MissingInfo.AFFECTED_USERS, MissingInfo.ERROR_MESSAGE],
        subjects=[
            "File share permissions broken after server update",
            "Can't access shared drive after last night's patching",
            "Multiple users locked out of \\\\contoso-fs01 file shares",
        ],
        descriptions=[
            "After last night's Windows Server update on contoso-fs01, multiple people in "
            "{department} can't access the \\\\contoso-fs01\\finance share. We're getting 'Access "
            "Denied' errors. This was working fine before the patch window. At least 15 people are "
            "affected. We have end-of-month close deadlines this week.",
            "Since the server maintenance last night our file share is inaccessible. The error says "
            "'You do not have permission to access \\\\contoso-fs01\\shared.' I've confirmed my "
            "credentials are fine — I can access other network resources. Multiple team members "
            "reporting the same thing.",
        ],
        next_best_actions=[
            "Check the file server's share and NTFS permissions to see if the update reset them. "
            "Compare current ACLs against the documented baseline. Restore permissions if changed.",
            "Review the Windows Update log on contoso-fs01 for any post-update configuration changes. "
            "Check if a Group Policy update overwrote share permissions.",
        ],
        remediation_steps=[
            [
                "RDP into contoso-fs01 and verify the server is healthy post-update",
                "Check the share permissions and NTFS ACLs on the affected file share",
                "Compare current permissions against the documented baseline or backup",
                "Restore permissions from the pre-patch backup if they were modified",
                "Test access from an affected user's workstation",
                "Document the issue and add a post-patch permission check to the maintenance runbook",
            ],
            [
                "Review Windows Update and Group Policy logs on the file server",
                "Check if the SMB configuration was altered by the update",
                "Verify AD security group memberships for affected users",
                "Re-apply the correct NTFS and share permissions from documentation",
                "Confirm access is restored for a sample of affected users",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# ds-012  Cosmos DB connection throttling
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="ds-012",
        category=Category.DATA,
        priority=Priority.P2,
        assigned_team=Team.DATA_PLATFORM,
        needs_escalation=False,
        missing_information=[MissingInfo.ERROR_MESSAGE, MissingInfo.ENVIRONMENT_DETAILS],
        subjects=[
            "Cosmos DB connection throttling — 429 errors in production",
            "Azure Cosmos DB rate limiting our application",
            "Cosmos DB — Too Many Requests errors spiking",
        ],
        descriptions=[
            "Our customer-facing API is getting 429 'Too Many Requests' responses from Cosmos DB. This "
            "started about an hour ago. The RU consumption graph shows we're hitting the provisioned "
            "throughput limit consistently. The affected database is 'contoso-customers' in the "
            "'prod-cosmos-eastus' account. Approximately 5,000 users are impacted.",
            "We're seeing HTTP 429 errors from Cosmos DB in our application logs. The "
            "CustomerTransactions container is being throttled. Our batch processing job that runs at "
            "{timestamp} seems to be consuming all the RUs. The real-time API queries are getting "
            "starved. Need help tuning the throughput or implementing a fix.",
        ],
        next_best_actions=[
            "Check the Cosmos DB metrics in Azure Monitor for RU consumption patterns. Identify the "
            "hot partition or heavy query causing throttling. Increase RU/s or enable autoscale.",
            "Review the partition key distribution for hotspot patterns. Enable autoscale on the "
            "container to handle burst traffic while investigating the root cause.",
        ],
        remediation_steps=[
            [
                "Open Azure Monitor metrics for the Cosmos DB account",
                "Identify which container and partition key range is being throttled",
                "Check for hot partitions using the Diagnostics settings or Insights workbook",
                "Increase provisioned throughput or enable autoscale as an immediate fix",
                "Review the batch processing job's query patterns for optimization opportunities",
                "Implement retry-with-backoff in the application if not already present",
            ],
            [
                "Check the Normalized RU Consumption metric per partition key range",
                "If a hot partition is identified, evaluate the partition key design",
                "Enable autoscale with a max RU/s that accommodates batch + real-time workloads",
                "Consider scheduling the batch job during off-peak hours",
                "Add application-level rate limiting for non-critical queries",
            ],
        ],
        attachment_options=[
            ["Azure Monitor RU consumption chart", "Application 429 error logs"],
        ],
    )
)

# ---------------------------------------------------------------------------
# ds-013  Azure Blob Storage access key rotation needed
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="ds-013",
        category=Category.DATA,
        priority=Priority.P3,
        assigned_team=Team.DATA_PLATFORM,
        needs_escalation=False,
        missing_information=[MissingInfo.AFFECTED_SYSTEM, MissingInfo.CONFIGURATION_DETAILS],
        subjects=[
            "Azure Blob Storage access key rotation required",
            "Storage account key rotation — compliance requirement",
            "Need to rotate storage account keys for contosoblob01",
        ],
        descriptions=[
            "Per our security audit findings, we need to rotate the access keys for the Azure storage "
            "account 'contosoblob01'. The keys haven't been rotated in over 180 days which violates "
            "our compliance policy. I know several applications use these keys so we need to coordinate "
            "the rotation carefully.",
            "Security team flagged that the storage account keys for contosoblob01 and contosoblob02 "
            "are overdue for rotation. We need to rotate them without breaking the downstream "
            "applications. Can someone help identify all services using these keys and plan the "
            "rotation?",
        ],
        next_best_actions=[
            "Inventory all applications and services using the storage account keys by checking Azure "
            "Key Vault references and application configurations. Plan a phased key rotation.",
            "Audit the storage account's key usage via Azure Monitor diagnostic logs. Migrate "
            "applications to managed identities where possible before rotating keys.",
        ],
        remediation_steps=[
            [
                "Query Azure Activity Log and diagnostic logs to identify key usage patterns",
                "Inventory all applications using the storage account keys (check Key Vault, app settings)",
                "Regenerate Key2 first (secondary) and update all applications to use Key2",
                "Verify all applications are functioning with Key2",
                "Regenerate Key1 (primary) to complete the rotation",
                "Update documentation with the new rotation date and schedule the next rotation",
            ],
            [
                "Identify applications using storage account keys via Azure Resource Graph or config scans",
                "Evaluate which applications can be migrated to managed identity authentication",
                "For apps that must use keys, store keys in Azure Key Vault with automatic rotation",
                "Execute the key rotation with a rollback plan for each dependent application",
                "Confirm all services are healthy after rotation and update the compliance tracker",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# ds-014  Data recovery — accidental table drop in production
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="ds-014",
        category=Category.DATA,
        priority=Priority.P1,
        assigned_team=Team.DATA_PLATFORM,
        needs_escalation=True,
        missing_information=[MissingInfo.TIMESTAMP, MissingInfo.AFFECTED_USERS],
        subjects=[
            "CRITICAL — Production table accidentally dropped",
            "URGENT: Accidental DROP TABLE on production Azure SQL database",
            "P1 — need immediate data recovery, production table deleted",
        ],
        descriptions=[
            "A developer accidentally ran DROP TABLE dbo.Transactions on the PRODUCTION "
            "FinancialReporting database about 15 minutes ago. They thought they were connected to the "
            "dev environment. This table has 3 years of transaction history and is used by multiple "
            "applications. We need to recover this data IMMEDIATELY. All downstream reports and "
            "applications are failing.",
            "EMERGENCY: Someone dropped the Customers table in production. It happened around "
            "{timestamp}. The application is throwing errors for every user — nothing works without "
            "that table. We need this restored from backup right now. The database is "
            "contoso-sql-prod/FinancialReporting.",
        ],
        next_best_actions=[
            "Immediately initiate a point-in-time restore of the Azure SQL database to just before the "
            "DROP TABLE command. Restore to a separate database, extract the table, and insert back.",
            "Use Azure SQL point-in-time restore to recover the database state before the accidental "
            "drop. If within 5 minutes, check if the transaction log backup can be used for faster "
            "recovery.",
        ],
        remediation_steps=[
            [
                "Confirm the exact time of the DROP TABLE command from the audit logs",
                "Initiate a point-in-time restore of the database to 1 minute before the drop",
                "Restore to a new database (e.g., FinancialReporting_Restore)",
                "Export the dropped table from the restored database using BCP or SSMS",
                "Re-create the table schema in production and bulk-insert the recovered data",
                "Verify row counts and data integrity against the restored copy",
                "Notify all affected application teams that the table is restored",
                "Conduct an RCA and implement safeguards (e.g., restricted prod access, DDL alerts)",
            ],
            [
                "Check Azure SQL audit logs for the exact DROP TABLE timestamp and user",
                "Start a point-in-time restore from the Azure portal or CLI",
                "While restore is running, communicate impact to stakeholders",
                "Once restore completes, use SELECT INTO or INSERT from the restored database",
                "Rebuild any indexes, constraints, and foreign keys on the restored table",
                "Run application smoke tests to confirm functionality is restored",
                "Review and tighten production database access controls",
            ],
        ],
        attachment_options=[
            ["Azure SQL audit log excerpt", "Application error screenshots"],
        ],
    )
)

# ---------------------------------------------------------------------------
# ds-015  SharePoint search not returning recent documents
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="ds-015",
        category=Category.DATA,
        priority=Priority.P4,
        assigned_team=Team.DATA_PLATFORM,
        needs_escalation=False,
        missing_information=[MissingInfo.AFFECTED_SYSTEM, MissingInfo.STEPS_TO_REPRODUCE],
        subjects=[
            "SharePoint search not finding recent documents",
            "Search results missing new files in SharePoint Online",
            "SharePoint search index seems out of date",
        ],
        descriptions=[
            "I uploaded several documents to our team SharePoint site about 3 days ago and they still "
            "don't show up in search results. I can browse to them directly and they open fine, but "
            "searching by file name or contents returns nothing. Other team members are seeing the same "
            "issue. Older documents search fine.",
            "Search on our SharePoint site isn't returning documents uploaded in the last week. I've "
            "tried searching by exact file name, keywords in the content, and metadata. Nothing shows "
            "up for recent uploads. The site is https://contoso.sharepoint.com/sites/{department}. "
            "Not urgent but it's making it hard to find things.",
        ],
        next_best_actions=[
            "Check the SharePoint search crawl status and last crawl time for the affected site. If "
            "the crawl is delayed, request a re-index of the site collection.",
            "Verify that the document library is not excluded from search. Check the search schema for "
            "any recent changes that might affect crawling of new content.",
        ],
        remediation_steps=[
            [
                "Check the search crawl log in the SharePoint admin center for errors",
                "Verify the site collection's search configuration (not set to No Index)",
                "Request a re-index of the affected site collection",
                "Wait for the crawl to complete (typically 15 minutes to a few hours)",
                "Test search with the previously missing documents",
            ],
            [
                "Confirm the documents are not in a library excluded from search",
                "Check if the files have draft/checkout status that prevents indexing",
                "Verify the managed property mappings in the search schema",
                "Trigger a re-crawl from the site settings > Search and Offline Availability",
                "Confirm search results are returning the new documents after re-crawl",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# ds-016  Databricks cluster failing to start
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="ds-016",
        category=Category.DATA,
        priority=Priority.P2,
        assigned_team=Team.DATA_PLATFORM,
        needs_escalation=False,
        missing_information=[MissingInfo.ERROR_MESSAGE, MissingInfo.CONFIGURATION_DETAILS],
        subjects=[
            "Databricks cluster won't start — cloud provider error",
            "Azure Databricks cluster launch failure",
            "Databricks interactive cluster stuck in pending state",
        ],
        descriptions=[
            "Our production Databricks cluster 'FinanceETL-Prod' has been failing to start since this "
            "morning. The error in the cluster events says 'CLOUD_PROVIDER_LAUNCH_FAILURE' and mentions "
            "something about insufficient capacity in East US. We have 4 scheduled jobs that depend on "
            "this cluster and they're all queued up. The data engineering team is blocked.",
            "Can't launch my Databricks cluster. I've tried three times and it keeps going to a "
            "'Terminated' state after about 5 minutes. The event log shows 'The requested VM size "
            "Standard_DS4_v2 is not available in the current region.' This is the cluster we use for "
            "all our data processing. Need this fixed urgently.",
        ],
        next_best_actions=[
            "Check the Databricks cluster event log for the specific error. If it's a VM capacity "
            "issue, switch to an alternative VM size or region. Retry cluster launch.",
            "Review Azure regional capacity for the requested VM size. Update the cluster configuration "
            "to use an available VM SKU or enable autoscaling with fallback instance types.",
        ],
        remediation_steps=[
            [
                "Check the cluster event log in the Databricks workspace for the exact error",
                "If VM capacity issue, identify alternative VM sizes in the same family",
                "Update the cluster configuration to use an available VM SKU",
                "If regional capacity is the issue, consider a secondary region or availability zone",
                "Restart the cluster and verify it launches successfully",
                "Re-run any queued jobs and confirm they complete",
            ],
            [
                "Verify the Databricks workspace subscription has sufficient quota for the VM family",
                "Check Azure Service Health for any ongoing capacity issues in the region",
                "Update the cluster to use spot instances with on-demand fallback for cost optimization",
                "Add instance pool configuration to pre-warm VMs and reduce launch failures",
                "Test the cluster launch and monitor the first job execution",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# ds-017  Snowflake warehouse suspended — queries blocked
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="ds-017",
        category=Category.DATA,
        priority=Priority.P2,
        assigned_team=Team.DATA_PLATFORM,
        needs_escalation=False,
        missing_information=[MissingInfo.AFFECTED_USERS, MissingInfo.ENVIRONMENT_DETAILS],
        subjects=[
            "Snowflake warehouse suspended — can't run queries",
            "Snowflake CONTOSO_ANALYTICS_WH not responding",
            "Queries failing — Snowflake warehouse auto-suspended and won't resume",
        ],
        descriptions=[
            "The CONTOSO_ANALYTICS_WH warehouse in Snowflake is suspended and won't auto-resume when "
            "I try to run queries. I'm getting the error 'Warehouse CONTOSO_ANALYTICS_WH cannot be "
            "resumed.' The BI team and several analysts depend on this warehouse for daily reporting. "
            "We've been unable to run any queries for the past 30 minutes.",
            "something is wrong with our snowflake warehouse. when i try to run a query it just hangs "
            "and then times out. the warehouse name is CONTOSO_ANALYTICS_WH. i checked and it shows "
            "as 'Suspended' but the auto-resume should be on. other people on my team are having the "
            "same problem. we have a board report due at noon.",
        ],
        next_best_actions=[
            "Check the Snowflake warehouse status and attempt a manual resume via ALTER WAREHOUSE "
            "RESUME. Review the warehouse resource monitor for credit exhaustion.",
            "Verify the warehouse isn't blocked by a resource monitor credit quota. If credits are "
            "exhausted, increase the quota or switch to an alternate warehouse.",
        ],
        remediation_steps=[
            [
                "Log into Snowflake as ACCOUNTADMIN and check the warehouse status",
                "Attempt to manually resume: ALTER WAREHOUSE CONTOSO_ANALYTICS_WH RESUME",
                "If blocked by a resource monitor, check SHOW RESOURCE MONITORS for credit usage",
                "Increase the credit quota on the resource monitor or remove the suspension action",
                "Verify the warehouse is running and test with a simple query",
                "Notify affected users that the warehouse is back online",
            ],
            [
                "Check Snowflake account usage for any billing or credit issues",
                "Verify the warehouse configuration (auto-resume, auto-suspend settings)",
                "If the warehouse was manually suspended, identify who suspended it via QUERY_HISTORY",
                "Resume the warehouse and validate query execution",
                "Set up an alert for warehouse suspension events to catch this earlier",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# ds-018  Legacy file server nearing capacity
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="ds-018",
        category=Category.DATA,
        priority=Priority.P3,
        assigned_team=Team.DATA_PLATFORM,
        needs_escalation=False,
        missing_information=[MissingInfo.BUSINESS_IMPACT, MissingInfo.CONFIGURATION_DETAILS],
        subjects=[
            "Legacy file server running out of disk space",
            "File server contoso-fs01 at 92% capacity",
            "Disk space warning on shared file server",
        ],
        descriptions=[
            "We're getting disk space warnings on contoso-fs01. The D: drive where the shared folders "
            "live is at 92% capacity (1.84 TB used of 2 TB). This server hosts file shares for "
            "Finance, Legal, and Compliance. We've been meaning to migrate to SharePoint but it hasn't "
            "happened yet. Can we either expand the storage or start archiving old files?",
            "The file server that hosts our department shares is almost full. It's been creeping up for "
            "months. We get alerts every week now. Most of the data is old — project files from 3+ "
            "years ago that nobody accesses. Can the storage team help us either clean up or add more "
            "space? The server is contoso-fs01, D: drive.",
        ],
        next_best_actions=[
            "Run a storage analysis on the file server to identify large and stale files. Present "
            "options: expand disk, archive to Azure Blob cool tier, or accelerate SharePoint migration.",
            "Generate a disk usage report by department and age. Coordinate with department leads to "
            "identify data for archival or deletion. Plan a short-term capacity fix.",
        ],
        remediation_steps=[
            [
                "Run TreeSize or a similar tool to analyze disk usage by folder and age",
                "Identify files not accessed in 2+ years as archival candidates",
                "Coordinate with department leads to approve archival or deletion of stale data",
                "Move approved archival data to Azure Blob Storage cool or archive tier",
                "Free up at least 15-20% disk space as a buffer",
                "Set up automated disk space monitoring alerts at 80% and 90%",
            ],
            [
                "Check if the file server VM can have additional disk attached (Azure VM or on-prem SAN)",
                "If immediate capacity is needed, extend the D: drive or add a new volume",
                "Begin planning migration of active shares to SharePoint Online",
                "Implement file screening (FSRM) to block non-business file types",
                "Schedule a quarterly storage review with department stakeholders",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# ds-019  Azure Data Factory pipeline performance degraded
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="ds-019",
        category=Category.DATA,
        priority=Priority.P2,
        assigned_team=Team.DATA_PLATFORM,
        needs_escalation=False,
        missing_information=[MissingInfo.ERROR_MESSAGE, MissingInfo.TIMESTAMP],
        subjects=[
            "ADF pipeline taking 3x longer than normal",
            "Azure Data Factory performance degradation — DailyFinancialLoad",
            "Data pipeline SLA breach — ADF running slow",
        ],
        descriptions=[
            "The DailyFinancialLoad pipeline in Azure Data Factory normally completes in about 45 "
            "minutes but the last three runs have taken over 2 hours each. No code or schema changes "
            "were made. The pipeline copies data from Azure SQL to ADLS Gen2 and then runs several "
            "transformations in a data flow. The downstream Power BI refresh is now failing because "
            "the data isn't ready in time.",
            "Our ADF pipeline is running way slower than usual. The 'CustomerDataSync' pipeline went "
            "from a 30-minute runtime to almost 2 hours. The copy activities seem to be the bottleneck "
            "— the data flows are fine. This has been happening for three days. Source is Cosmos DB, "
            "sink is ADLS Gen2. Throughput dropped from ~50 MB/s to around 8 MB/s.",
        ],
        next_best_actions=[
            "Check ADF pipeline run details for activity-level durations to identify the bottleneck. "
            "Investigate source/sink performance metrics and integration runtime utilization.",
            "Review the ADF monitoring dashboard for DIU utilization and data throughput. Check if "
            "source database or sink storage is throttling requests.",
        ],
        remediation_steps=[
            [
                "Open the ADF Monitor tab and compare recent runs to the baseline duration",
                "Identify which activities are taking longer (copy, data flow, lookup, etc.)",
                "Check DIU utilization and parallelism settings on copy activities",
                "Verify source database (Azure SQL/Cosmos DB) is not resource-constrained",
                "Check ADLS Gen2 for throttling or network latency issues",
                "Increase DIU count or adjust parallelism to improve throughput",
                "Re-run the pipeline and confirm performance returns to baseline",
            ],
            [
                "Check integration runtime CPU and memory utilization during pipeline runs",
                "Verify no competing pipelines are consuming shared integration runtime resources",
                "If using self-hosted IR, check the host VM's resource utilization",
                "Review data volume trends — increased data size may require pipeline optimization",
                "Consider partitioning large copy activities for parallel execution",
                "Test with an increased DIU count and monitor throughput improvement",
            ],
        ],
        attachment_options=[
            ["ADF pipeline run duration comparison", "Copy activity throughput metrics"],
        ],
    )
)

# ---------------------------------------------------------------------------
# ds-020  Cross-region data replication lag
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="ds-020",
        category=Category.DATA,
        priority=Priority.P1,
        assigned_team=Team.DATA_PLATFORM,
        needs_escalation=True,
        missing_information=[MissingInfo.AFFECTED_USERS, MissingInfo.BUSINESS_IMPACT],
        subjects=[
            "CRITICAL — Cross-region replication lag exceeding SLA",
            "Geo-replication lag on Azure SQL — DR site hours behind",
            "P1 — data replication to secondary region dangerously behind",
        ],
        descriptions=[
            "Our Azure SQL geo-replication from East US to West US is showing a replication lag of "
            "over 4 hours. Our RPO SLA is 1 hour. If we had to failover right now we'd lose 4 hours "
            "of financial transaction data. The primary database (contoso-sql-prod in East US) seems "
            "healthy but the secondary is falling further behind. This is a compliance and DR risk. "
            "We need this investigated immediately.",
            "URGENT: The geo-replicated secondary for our production Azure SQL database is lagging "
            "behind by more than 3 hours. We noticed it during our DR readiness check this morning. "
            "The replication_lag_sec metric in sys.dm_geo_replication_link_status shows ~14,400 "
            "seconds. Our disaster recovery plan assumes less than 60 minutes of lag. This needs "
            "immediate attention — we're out of compliance with our BC/DR policy.",
        ],
        next_best_actions=[
            "Immediately investigate replication lag by checking sys.dm_geo_replication_link_status "
            "and Azure Monitor metrics. Identify if the primary is generating excessive transaction "
            "log volume or if the secondary is resource-constrained.",
            "Check the secondary database's service tier and resource utilization. If it's a lower "
            "tier than the primary, upgrade it. Review transaction log generation rate on the primary.",
        ],
        remediation_steps=[
            [
                "Query sys.dm_geo_replication_link_status on the primary for current lag metrics",
                "Check Azure Monitor for the secondary database's DTU/CPU/IO utilization",
                "If the secondary is resource-constrained, scale it up to match or exceed the primary",
                "Review transaction log generation rate on the primary for unusual spikes",
                "Check for long-running transactions on the primary that may block log truncation",
                "Monitor replication lag reduction after scaling and confirm it returns within SLA",
                "Update the DR runbook with findings and preventive measures",
            ],
            [
                "Verify both primary and secondary are on the same service tier and compute size",
                "Check Azure Service Health for any ongoing replication issues in the regions",
                "Review recent schema changes or bulk operations that may have spiked log generation",
                "If a bulk load caused the lag, wait for replication to catch up and reschedule future loads",
                "Consider adding a replication lag alert at 30 minutes to catch issues before SLA breach",
                "Conduct a failover test once replication is caught up to validate DR readiness",
            ],
        ],
        attachment_options=[
            ["sys.dm_geo_replication_link_status output", "Azure Monitor replication lag chart"],
        ],
    )
)

# ---------------------------------------------------------------------------
# ds-021  Accidental bulk delete in production database
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="ds-021",
        category=Category.DATA,
        priority=Priority.P1,
        assigned_team=Team.DATA_PLATFORM,
        needs_escalation=True,
        missing_information=[MissingInfo.AFFECTED_USERS, MissingInfo.TIMESTAMP],
        subjects=[
            "URGENT — accidentally ran DELETE without WHERE on production table",
            "Production data loss — bulk delete on client_transactions table",
            "P1 — accidental mass deletion in prod database, need immediate help",
        ],
        descriptions=[
            "I accidentally ran DELETE without a WHERE clause on the client_transactions table in "
            "our production Azure SQL database. I killed the query after about 3 seconds but I "
            "don't know how many rows were deleted. The table had approximately 2.4 million rows "
            "before the accident. I haven't told anyone else yet — I'm panicking. The database is "
            "contoso-prod-sql in the East US resource group. Please help me figure out how to "
            "recover this data.",
            "I made a terrible mistake. I was testing a DELETE statement in what I thought was "
            "our dev environment, but I was connected to production. The query ran against the "
            "client_transactions table — no WHERE clause. I noticed within seconds and cancelled "
            "it, but rows are definitely gone. This is a financial transactions table and we may "
            "have regulatory issues if we can't recover. Is there a point-in-time restore option?",
        ],
        next_best_actions=[
            "Immediately check the most recent backup and point-in-time restore options for the "
            "database. Assess the scope of data loss by comparing row counts against the last "
            "known good state.",
            "Initiate point-in-time restore to a secondary database and compare data to identify "
            "deleted rows. Prevent further writes to the affected table if possible.",
        ],
        remediation_steps=[
            [
                "Confirm the database name, table, and approximate time of the incident",
                "Check Azure SQL point-in-time restore availability (up to 35-day retention)",
                "Restore the database to a point just before the DELETE was executed",
                "Compare row counts and data between the restored and current databases",
                "Re-insert the missing rows from the restored copy into production",
                "Verify data integrity and reconcile with upstream/downstream systems",
                "Conduct a post-incident review and restrict production write access",
            ],
        ],
        attachment_options=[
            ["Query execution history screenshot", "Database row count before/after"],
        ],
    )
)

# ---------------------------------------------------------------------------
# ds-022  GDPR data subject access request
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="ds-022",
        category=Category.DATA,
        priority=Priority.P2,
        assigned_team=Team.DATA_PLATFORM,
        needs_escalation=False,
        missing_information=[MissingInfo.AFFECTED_SYSTEM, MissingInfo.CONFIGURATION_DETAILS],
        subjects=[
            "GDPR data subject access request — 30-day deadline",
            "Client DSAR received — need to locate all personal data",
            "Formal GDPR Article 15 request — data extraction needed",
        ],
        descriptions=[
            "A client has formally requested all data we hold about them under GDPR Article 15. "
            "Legal received the request and says we have 30 days to comply. The client's data "
            "could be in Azure SQL, Cosmos DB, blob storage, and possibly in log files. We need "
            "to identify every system that contains this person's data and extract it in a "
            "readable format. Client reference ID is CLT-88421. Legal is tracking this closely.",
            "We received a data subject access request (DSAR) under GDPR from a European client. "
            "They want a full export of all personal data we hold, including transaction history, "
            "support interactions, and any analytics or profiling data. Our data is spread across "
            "multiple Azure services and I'm not sure we have a comprehensive data map. The legal "
            "deadline is 28 days from now.",
        ],
        next_best_actions=[
            "Initiate the DSAR workflow: identify all systems containing the subject's data "
            "using the data catalog, coordinate extraction, and prepare the response package.",
            "Engage the data governance team to map all data stores containing the subject's "
            "personal data and begin extraction within the compliance timeline.",
        ],
        remediation_steps=[
            [
                "Log the DSAR and confirm the 30-day compliance deadline",
                "Consult the data catalog to identify all systems holding the subject's data",
                "Query each system (Azure SQL, Cosmos DB, blob storage, logs) for the subject's records",
                "Extract and compile data into a structured, readable format",
                "Review the package with legal/privacy team before sending",
                "Deliver the data package to the client within the deadline",
                "Document the process for future DSAR handling improvements",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# ds-023  Cross-region data residency compliance concern
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="ds-023",
        category=Category.DATA,
        priority=Priority.P2,
        assigned_team=Team.DATA_PLATFORM,
        needs_escalation=True,
        missing_information=[MissingInfo.CONFIGURATION_DETAILS, MissingInfo.AFFECTED_SYSTEM],
        subjects=[
            "Data residency violation? Singapore client data replicating to US",
            "Possible compliance issue — cross-region data replication",
            "URGENT — client data may be stored outside permitted geography",
        ],
        descriptions=[
            "I noticed in the Azure portal that our Singapore client data appears to be replicating "
            "to the US East region. Our contract with these clients stipulates that their data must "
            "remain within the APAC region. If this replication is intentional, was it approved by "
            "compliance? If not, we may have a data residency violation on our hands. The storage "
            "account is sg-client-data-prod and I can see geo-redundant replication is enabled.",
            "During a routine audit of our Azure storage configuration, I found that geo-redundant "
            "storage (GRS) is enabled on several accounts holding client data from our Singapore "
            "operations. GRS replicates to a paired region in the US, which could violate data "
            "residency requirements under Singapore's PDPA. We need to determine if this affects "
            "regulated data and whether we need to switch to zone-redundant storage (ZRS) instead.",
        ],
        next_best_actions=[
            "Verify the replication configuration and determine if regulated data is being copied "
            "cross-region. Engage the compliance team to assess the impact.",
            "Audit the storage account's replication settings and cross-reference with data "
            "classification policies. Escalate to compliance if regulated data is affected.",
        ],
        remediation_steps=[
            [
                "Check the storage account replication type (GRS, ZRS, LRS) in the Azure portal",
                "Identify what data is stored in the affected accounts using the data catalog",
                "Determine if any regulated or contractually restricted data is being replicated",
                "Engage the compliance and legal teams with findings",
                "If a violation is confirmed, switch to ZRS or LRS to stop cross-region replication",
                "Notify affected clients if required by contract or regulation",
                "Update data governance policies to prevent future misconfigurations",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# ds-024  Storage costs exploding unexpectedly
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="ds-024",
        category=Category.DATA,
        priority=Priority.P2,
        assigned_team=Team.DATA_PLATFORM,
        needs_escalation=False,
        missing_information=[MissingInfo.AFFECTED_SYSTEM, MissingInfo.TIMESTAMP],
        subjects=[
            "Azure storage bill jumped from $2k to $18k — need investigation",
            "Unexpected 9x increase in blob storage costs this month",
            "Storage cost anomaly — massive unexplained data writes",
        ],
        descriptions=[
            "Our Azure storage bill went from approximately $2,000 last month to $18,000 this "
            "month. Something is writing massive amounts of data to blob storage but I can't "
            "figure out what. We haven't deployed any new applications or data pipelines. The "
            "cost spike appears to be concentrated in the 'analytics-raw' storage account. I "
            "need help identifying the source before next month's bill is even worse.",
            "Finance flagged our Azure bill — storage costs have increased by 800% month over "
            "month. I checked Azure Cost Management and the spike is coming from blob storage "
            "write transactions and data-at-rest in a storage account I don't recognize. It "
            "might be a runaway pipeline, an application bug writing in a loop, or possibly "
            "unauthorized usage. We need to trace the source of these writes urgently.",
        ],
        next_best_actions=[
            "Analyze Azure Storage Analytics logs and Cost Management data to identify the "
            "source of the excessive writes. Check for runaway pipelines or application bugs.",
            "Review blob storage metrics and access logs to pinpoint which containers and "
            "applications are responsible for the cost spike.",
        ],
        remediation_steps=[
            [
                "Open Azure Cost Management and drill into the storage cost breakdown by account",
                "Enable or review Storage Analytics logs for the affected storage account",
                "Identify the top containers by size growth and transaction volume",
                "Trace write operations to the originating application or pipeline",
                "Fix the root cause (runaway pipeline, application bug, misconfiguration)",
                "Set up cost alerts and budget thresholds to catch future anomalies early",
                "Delete or archive unnecessary data to reduce ongoing costs",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# ds-025  Legacy system migration data loss
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="ds-025",
        category=Category.DATA,
        priority=Priority.P1,
        assigned_team=Team.DATA_PLATFORM,
        needs_escalation=True,
        missing_information=[MissingInfo.CONFIGURATION_DETAILS, MissingInfo.SCREENSHOT_OR_ATTACHMENT],
        subjects=[
            "CRITICAL — 200,000 records missing after weekend migration to Azure SQL",
            "Data loss during SQL Server 2016 to Azure SQL migration",
            "P1 — post-migration data integrity failure in accounts table",
        ],
        descriptions=[
            "During this weekend's migration from SQL Server 2016 on-prem to Azure SQL, we're "
            "missing approximately 200,000 records in the accounts table. The source had 1.8 million "
            "rows and the target only shows 1.6 million. We used Azure Database Migration Service "
            "and the migration status shows 'completed successfully' — but it clearly didn't migrate "
            "everything. We cannot go live on Monday with missing account data. The source server "
            "is still running but we need to figure out what was lost and re-migrate.",
            "Our production migration from SQL Server 2016 to Azure SQL completed over the weekend "
            "but post-migration validation shows a significant row count discrepancy. The accounts "
            "table is short by about 200k records. Other tables appear to be intact. We suspect "
            "either a filter was applied accidentally, rows with constraint violations were skipped, "
            "or the migration tool hit a timeout. We need to reconcile and recover before business "
            "hours on Monday.",
        ],
        next_best_actions=[
            "Compare source and target databases to identify exactly which records are missing. "
            "Check Azure DMS migration logs for errors, warnings, or skipped rows.",
            "Run a row-by-row reconciliation on the accounts table between source and target. "
            "Review DMS activity logs and error output to understand the data loss.",
        ],
        remediation_steps=[
            [
                "Run SELECT COUNT(*) on the accounts table in both source and target to confirm the gap",
                "Review Azure DMS migration logs for errors, warnings, or skipped records",
                "Identify the missing rows by comparing primary keys between source and target",
                "Check for constraint violations, data type mismatches, or truncation issues",
                "Re-migrate the missing records using a targeted query or bulk insert",
                "Run full data validation (row counts, checksums, spot checks) across all tables",
                "Do not cut over to Azure SQL until all validation checks pass",
            ],
        ],
        attachment_options=[
            ["DMS migration activity log", "Source vs. target row count comparison"],
        ],
    )
)

# ---------------------------------------------------------------------------
# ds-026  SharePoint document versioning not retaining all versions
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="ds-026",
        category=Category.DATA,
        priority=Priority.P2,
        assigned_team=Team.DATA_PLATFORM,
        needs_escalation=False,
        missing_information=[MissingInfo.SCREENSHOT_OR_ATTACHMENT, MissingInfo.REPRODUCTION_FREQUENCY],
        subjects=[
            "SharePoint document versioning not retaining all versions",
            "Missing version history entries in SharePoint Online library",
            "SharePoint version history shows gaps — older versions disappeared",
        ],
        descriptions=[
            "Users in the compliance team report that SharePoint Online is not retaining all "
            "document versions for files in the Regulatory Filings library. A document that "
            "should have 15 versions only shows 8 in the version history. This is critical "
            "because we need full version history for audit purposes. We haven't been able to "
            "capture a screenshot of the version history yet, and we're not sure how often "
            "this is happening — it was only noticed during a routine audit check.",
            "Our legal team discovered that version history for key contract documents in "
            "SharePoint is incomplete. Several intermediate versions appear to have been pruned "
            "or lost. The versioning settings show major and minor versions are enabled, but the "
            "count doesn't match what users expect. No one has taken a screenshot of the version "
            "history page, and we don't know if this affects all documents or just certain ones. "
            "The team isn't sure how frequently versions go missing.",
        ],
        next_best_actions=[
            "Check the SharePoint library versioning settings and any version trimming policies. "
            "Capture screenshots of the affected document's version history for investigation.",
        ],
        remediation_steps=[
            [
                "Review the document library's versioning settings (major/minor version limits)",
                "Check for any SharePoint retention policies or version trimming rules",
                "Capture screenshots of the version history for affected documents",
                "Compare expected version counts with actual counts across multiple documents",
                "Adjust version limits or retention policies to preserve required history",
                "Restore missing versions from SharePoint Recycle Bin or backup if available",
                "Set up monitoring to detect future version history discrepancies",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# ds-027  Azure Blob storage access key rotation broke app
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="ds-027",
        category=Category.DATA,
        priority=Priority.P1,
        assigned_team=Team.DATA_PLATFORM,
        needs_escalation=True,
        missing_information=[MissingInfo.PREVIOUS_TICKET_ID, MissingInfo.AUTHENTICATION_METHOD],
        subjects=[
            "Azure Blob storage key rotation broke production application",
            "App failing after storage account access key was rotated",
            "Storage key rotation caused outage — need rollback guidance",
        ],
        descriptions=[
            "We rotated the access keys on our primary Azure Blob storage account as part of a "
            "scheduled security maintenance, and now our document processing application is "
            "returning 403 Forbidden errors on all blob operations. The app was apparently using "
            "the old key directly in its configuration. We did a similar rotation six months ago "
            "and had the same issue, but I can't find the previous incident ticket to see how it "
            "was resolved. I'm also not sure whether the app authenticates using shared keys, "
            "SAS tokens, or managed identity.",
            "After rotating the access keys on the 'contoso-docs-prod' storage account, multiple "
            "services started failing. The key rotation was required by our security policy but "
            "we didn't have a full inventory of what depends on these keys. This same scenario "
            "happened during the last rotation cycle but the remediation steps from that ticket "
            "are lost. We need to identify whether the affected services use shared access keys, "
            "connection strings with SAS tokens, or another auth mechanism.",
        ],
        next_best_actions=[
            "Identify all applications using the rotated storage account keys and update their "
            "configurations. Locate the previous rotation incident for remediation reference.",
        ],
        remediation_steps=[
            [
                "Regenerate Key 2 (or the unused key) and update the failing application immediately",
                "Identify all services and connection strings referencing the storage account",
                "Determine the authentication method each service uses (shared key, SAS, managed identity)",
                "Update all affected configurations with the new key or migrate to managed identity",
                "Search the ticketing system for the previous key rotation incident and document findings",
                "Create a key rotation runbook to prevent recurrence during future rotations",
                "Test all dependent services to confirm normal operation after the fix",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# ds-028  Database replication lag causing stale reads
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="ds-028",
        category=Category.DATA,
        priority=Priority.P2,
        assigned_team=Team.DATA_PLATFORM,
        needs_escalation=False,
        missing_information=[MissingInfo.REPRODUCTION_FREQUENCY, MissingInfo.TIMESTAMP],
        subjects=[
            "Database replication lag causing stale reads in reporting",
            "Azure SQL read replica showing outdated data intermittently",
            "Replication delay between primary and secondary database",
        ],
        descriptions=[
            "Our reporting dashboard is showing stale data that appears to be several minutes "
            "behind the primary database. We use Azure SQL geo-replication with a read replica "
            "for reporting queries. The lag seems to come and go — sometimes data is current, "
            "other times it's 5-10 minutes behind. We haven't been able to pin down a specific "
            "time when the lag occurs or how frequently it happens. The reports team only notices "
            "it when a client points out that their latest transaction isn't showing.",
            "Users are complaining that the analytics portal shows inconsistent data compared to "
            "the transactional system. We suspect replication lag on our Azure SQL read replica "
            "is the cause. The issue is intermittent and hard to reproduce on demand — it might "
            "correlate with peak load times but we haven't confirmed that. We don't have specific "
            "timestamps of when the stale reads were observed because users only report it after "
            "the fact.",
        ],
        next_best_actions=[
            "Monitor the Azure SQL replication lag metrics and correlate with the reported stale "
            "read incidents. Collect specific timestamps when stale data is observed.",
        ],
        remediation_steps=[
            [
                "Check Azure SQL replication health and lag metrics in the Azure portal",
                "Enable alerts on replication lag exceeding an acceptable threshold",
                "Correlate lag spikes with database workload patterns and peak usage times",
                "Ask reporting users to record exact timestamps when they observe stale data",
                "Consider scaling the read replica or optimizing heavy queries that may cause lag",
                "Implement application-level staleness checks to warn users when data may be delayed",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# ds-029  OneDrive sync conflict for shared folder
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="ds-029",
        category=Category.DATA,
        priority=Priority.P3,
        assigned_team=Team.DATA_PLATFORM,
        needs_escalation=False,
        missing_information=[MissingInfo.CONTACT_INFO, MissingInfo.SCREENSHOT_OR_ATTACHMENT],
        subjects=[
            "OneDrive sync conflict on shared folder — duplicate files appearing",
            "Sync conflicts in OneDrive shared folder with co-owner",
            "OneDrive creating duplicate files in shared project folder",
        ],
        descriptions=[
            "I'm getting sync conflicts in a OneDrive shared folder that I co-own with a "
            "colleague in the London office. Files keep getting duplicated with '-conflict' "
            "suffixes and we're not sure which version is the correct one. I need to coordinate "
            "with the co-owner to resolve the conflicts but their contact details aren't in the "
            "directory — they recently transferred from another department. I haven't taken a "
            "screenshot of the sync status or the conflicted files yet.",
            "Our project team has a shared OneDrive folder and multiple members are reporting "
            "sync conflict errors. Duplicate copies of spreadsheets are appearing with names "
            "like 'Budget (Company Name)-conflict.xlsx'. The main co-owner of the folder is "
            "working remotely this week and I don't have their current phone number or personal "
            "email to reach them. We need a screenshot of the OneDrive sync client status to "
            "diagnose whether this is a client-side or server-side issue.",
        ],
        next_best_actions=[
            "Obtain the co-owner's contact information and coordinate to pause syncing on one "
            "side. Capture screenshots of the sync client status and conflicted files.",
        ],
        remediation_steps=[
            [
                "Locate the co-owner's current contact information through HR or their manager",
                "Coordinate with the co-owner to pause OneDrive sync on one machine temporarily",
                "Capture screenshots of the OneDrive sync client status on both machines",
                "Identify and resolve conflicted files by comparing modification timestamps",
                "Remove duplicate '-conflict' files after confirming the correct versions",
                "Ensure both users are running the latest OneDrive sync client version",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# ds-030  SQL Server backup job failing silently
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="ds-030",
        category=Category.DATA,
        priority=Priority.P1,
        assigned_team=Team.DATA_PLATFORM,
        needs_escalation=True,
        missing_information=[
            MissingInfo.SCREENSHOT_OR_ATTACHMENT,
            MissingInfo.PREVIOUS_TICKET_ID,
            MissingInfo.ERROR_MESSAGE,
        ],
        subjects=[
            "SQL Server backup job failing silently — no backups for 3 days",
            "Production database backup job stopped without alerts",
            "Missing SQL backups discovered during disaster recovery audit",
        ],
        descriptions=[
            "During a routine disaster recovery audit, we discovered that the nightly backup job "
            "for our production SQL Server instance has not completed successfully in three days. "
            "The SQL Agent job shows a status of 'succeeded' but the backup files are not being "
            "written to the target storage. There is no error message in the job history — it "
            "just silently fails to produce output. We had a similar backup issue last quarter "
            "that was tracked in a ticket, but I can't find the reference number. No one captured "
            "a screenshot of the job history or the storage target.",
            "Our DBA team noticed that the latest SQL Server backups are missing from the backup "
            "share. The maintenance plan shows the backup task as completed, but the .bak files "
            "are nowhere to be found. There's no error message logged in SQL Server Agent or the "
            "Windows Event Log. We believe this may be related to a storage permission change "
            "that was made recently. A similar silent failure happened before and was resolved in "
            "a previous ticket, but we don't have that ticket number handy.",
        ],
        next_best_actions=[
            "Investigate the SQL Server Agent job history and backup target storage permissions. "
            "Locate the previous backup failure ticket for reference.",
        ],
        remediation_steps=[
            [
                "Check SQL Server Agent job history for the backup job's detailed step output",
                "Verify the backup target path exists and the SQL Server service account has write access",
                "Review recent permission or configuration changes to the backup storage location",
                "Run the backup job manually and monitor for errors in real time",
                "Search the ticketing system for the previous backup failure incident",
                "Configure backup alerting to notify the DBA team on job failure or missing backup files",
                "Validate that the restored backups are functional by performing a test restore",
            ],
        ],
    )
)
