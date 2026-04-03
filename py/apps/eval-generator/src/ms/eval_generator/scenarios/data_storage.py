# Copyright (c) Microsoft. All rights reserved.
"""Data & Storage category scenarios for eval dataset."""

from ms.eval_generator.scenarios._base import ScenarioDefinition
from ms.eval_generator.scenarios._base import ScenarioGold

DATA_STORAGE_SCENARIOS: list[ScenarioDefinition] = [
    # ──────────────────────────────────────────────────────────────────
    # 1. Can't access SharePoint site after team change
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="data-storage-001",
        subjects=(
            "Can't access SharePoint site after transferring teams",
            "SharePoint access denied for new team site",
        ),
        descriptions=(
            "I transferred from Retail Banking to Wealth Management last week but I still can't access the "
            "Wealth Management SharePoint site at https://contoso.sharepoint.com/sites/WealthMgmt. Getting "
            "'access denied.' My manager confirmed I should have access.",
            "Recently moved to the Risk Analytics team but I don't have access to their SharePoint document "
            "library. I need to review the Q1 risk reports for my onboarding. My old team's SharePoint "
            "still works.",
        ),
        gold=ScenarioGold(
            category="Data & Storage",
            priority="P3",
            assigned_team="Data Platform",
            needs_escalation=False,
            missing_information=(),
            next_best_action="Grant SharePoint site access based on the user's new team membership",
            remediation_steps=(
                "Verify the user's new team membership and manager approval",
                "Add the user to the appropriate SharePoint site group",
                "Remove access to the old team's SharePoint if no longer needed",
                "Confirm the user can access the new team site",
            ),
        ),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 2. OneDrive sync stuck showing conflicts
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="data-storage-002",
        subjects=(
            "OneDrive sync stuck — showing sync conflicts",
            "OneDrive won't sync — perpetual conflicts",
        ),
        descriptions=(
            "My OneDrive has been stuck syncing for 3 days. It shows 142 sync conflicts and the icon is "
            "permanently showing the orange warning triangle. I've tried pausing and resuming sync. My "
            "files aren't backing up and I'm worried about data loss.",
            "OneDrive sync is completely broken on my laptop. It says 'sync pending' for hundreds of files "
            "and there are conflict copies everywhere. I think it started after I renamed a folder with a "
            "long path name.",
        ),
        gold=ScenarioGold(
            category="Data & Storage",
            priority="P3",
            assigned_team="Data Platform",
            needs_escalation=False,
            missing_information=(
                "device_info",
                "error_message",
            ),
            next_best_action="Reset the OneDrive sync client and resolve the file path conflicts",
            remediation_steps=(
                "Check for files with long paths or unsupported characters",
                "Resolve the sync conflicts by comparing local and cloud versions",
                "If too many conflicts, reset the OneDrive sync client",
                "Verify sync resumes correctly after reset",
                "Check available storage quota on OneDrive",
            ),
        ),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 3. Database read access request for reporting
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="data-storage-003",
        subjects=(
            "Need read access to the analytics database",
            "Database access request for quarterly reports",
        ),
        descriptions=(
            "I need read-only access to the ClientTransactions SQL database for my quarterly reporting "
            "work. My manager Wei Chen approved the request. I'm on the Finance analytics team and need "
            "access to the dbo.Transactions and dbo.Accounts tables.",
            "Requesting SELECT access to the RiskMetrics database on sql-prod-01.contoso.local. I need to "
            "run queries for the regulatory reporting that's due next month. Data owner approval from Sarah "
            "Johnson is attached.",
        ),
        gold=ScenarioGold(
            category="Data & Storage",
            priority="P3",
            assigned_team="Data Platform",
            needs_escalation=False,
            missing_information=(),
            next_best_action="Process the approved database access request and grant read-only permissions",
            remediation_steps=(
                "Verify manager and data owner approval",
                "Grant read-only access to the specified database tables",
                "Add the user to the appropriate database role",
                "Confirm the user can connect and query the database",
                "Document the access grant in the data access register",
            ),
        ),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 4. Backup restore needed for accidentally deleted folder
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="data-storage-004",
        subjects=(
            "Need backup restore — accidentally deleted project folder",
            "URGENT: Deleted entire project directory — need recovery",
        ),
        descriptions=(
            "I accidentally deleted the entire Q1-ClientReports folder from our team's SharePoint site. It "
            "had about 200 documents including finalized client deliverables. The recycle bin only shows "
            "some of the files. I need a full restore from backup ASAP.",
            "Somebody accidentally deleted the Finance/2026/March folder from the shared drive. It contains "
            "all of March's financial closing documents. We checked the SharePoint recycle bin but the "
            "retention period may have passed. Need a backup restore urgently.",
        ),
        gold=ScenarioGold(
            category="Data & Storage",
            priority="P2",
            assigned_team="Data Platform",
            needs_escalation=False,
            missing_information=(
                "timestamp",
                "affected_system",
            ),
            next_best_action="Initiate backup restore for the deleted folder from the most recent backup snapshot",
            remediation_steps=(
                "Check the SharePoint site recycle bin and second-stage recycle bin first",
                "If not in recycle bin, identify the most recent backup containing the deleted folder",
                "Initiate a restore to a temporary location to verify data integrity",
                "Move the restored files back to the original location",
                "Verify all files are present and notify the user",
            ),
        ),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 5. Legacy file share migration to SharePoint
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="data-storage-005",
        subjects=(
            "Need help migrating file share to SharePoint",
            "File share to SharePoint Online migration request",
        ),
        descriptions=(
            "Our department still uses a legacy file share (\\fileserver02\LegalDocs) with about 500 GB of "
            "data. We need to migrate this to SharePoint Online as part of the company initiative. Can the "
            "Data Platform team help plan and execute this migration?",
            "Requesting migration of the Engineering department's file share to SharePoint. The share has "
            "about 2 TB of data across 150,000 files. We understand there are file name and path length "
            "limitations to address.",
        ),
        gold=ScenarioGold(
            category="Data & Storage",
            priority="P4",
            assigned_team="Data Platform",
            needs_escalation=False,
            missing_information=(
                "affected_system",
                "business_impact",
            ),
            next_best_action="Schedule a migration planning session to assess the file share content and SharePoint requirements",
            remediation_steps=(
                "Assess the file share size, structure, and file types",
                "Identify files with unsupported characters or path lengths for SharePoint",
                "Create a migration plan with timeline and testing phases",
                "Execute the migration using SharePoint Migration Tool",
                "Validate migrated content and redirect users to the new SharePoint location",
            ),
        ),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 6. Storage quota exceeded on OneDrive
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="data-storage-006",
        subjects=(
            "OneDrive storage full — can't save files",
            "OneDrive quota exceeded — need more space",
        ),
        descriptions=(
            "My OneDrive is completely full at 1 TB and I can't save any more files. I work with large "
            "video files for our marketing team and they eat up space quickly. Can I get my quota increased "
            "or is there an alternative storage solution?",
            "Getting 'your OneDrive is full' errors. I've already cleaned up what I can but I have 800 GB "
            "of client presentation materials that I need to keep. Is there a way to get more OneDrive "
            "storage?",
        ),
        gold=ScenarioGold(
            category="Data & Storage",
            priority="P3",
            assigned_team="Data Platform",
            needs_escalation=False,
            missing_information=(),
            next_best_action="Review the user's OneDrive usage and either increase quota or recommend alternative storage",
            remediation_steps=(
                "Check the user's current OneDrive storage usage and breakdown",
                "Identify large or infrequently accessed files that can be archived",
                "If business-justified, increase the OneDrive quota",
                "For large media files, recommend SharePoint or Azure Blob Storage as alternatives",
                "Help the user set up the recommended storage solution",
            ),
        ),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 7. SharePoint site collection permissions audit
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="data-storage-007",
        subjects=(
            "Need permissions audit on SharePoint site",
            "SharePoint permissions review for compliance",
        ),
        descriptions=(
            "Our compliance team needs a full permissions audit of the Executive SharePoint site "
            "collection. We need to know who has access to what, including external sharing. This is for "
            "the upcoming SOX audit. Can the Data Platform team generate an access report?",
            "Requesting a permissions review of all SharePoint sites owned by the Legal department. We need "
            "to verify that only authorized personnel have access to attorney-client privileged documents. "
            "Audit deadline is end of this month.",
        ),
        gold=ScenarioGold(
            category="Data & Storage",
            priority="P3",
            assigned_team="Data Platform",
            needs_escalation=False,
            missing_information=(),
            next_best_action="Generate a comprehensive SharePoint permissions report for the compliance audit",
            remediation_steps=(
                "Run a SharePoint permissions report for the specified site collections",
                "Include both direct and inherited permissions in the report",
                "Flag any external sharing or guest access configurations",
                "Deliver the report to the compliance team for review",
                "Remediate any unauthorized access findings if identified",
            ),
        ),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 8. SQL database performance degradation
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="data-storage-008",
        subjects=(
            "Production database extremely slow",
            "SQL database query performance degraded significantly",
        ),
        descriptions=(
            "Our production SQL database (sql-prod-01) has been running extremely slowly since this "
            "morning. Queries that normally take 2 seconds are now taking 30+ seconds. The client-facing "
            "portfolio management app is practically unusable. About 500 users are affected.",
            "Major database performance issues. The ClientData database response times have gone from "
            "milliseconds to multiple seconds. Our real-time dashboards are timing out. DBA team noticed "
            "tempdb is growing rapidly and there might be a long-running blocking query.",
        ),
        gold=ScenarioGold(
            category="Data & Storage",
            priority="P2",
            assigned_team="Data Platform",
            needs_escalation=False,
            missing_information=(
                "error_message",
            ),
            next_best_action="Investigate blocking queries, tempdb growth, and resource contention on the production SQL server",
            remediation_steps=(
                "Check for long-running or blocking queries using sp_who2 or Activity Monitor",
                "Review tempdb usage and identify any queries causing excessive growth",
                "Check SQL Server resource utilization (CPU, memory, I/O)",
                "Kill or optimize the blocking query if identified",
                "Consider adding missing indexes flagged by the query execution plans",
            ),
        ),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 9. Teams files tab not loading
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="data-storage-009",
        subjects=(
            "Files tab in Teams channel not loading",
            "Can't access files in Teams — spinning forever",
        ),
        descriptions=(
            "The Files tab in our project Team channel just shows a spinning wheel and never loads. This "
            "has been happening for 2 days. Chat and meetings work fine but nobody on the team can access "
            "the shared files through Teams. We can still access them through SharePoint directly.",
            "Teams Files tab is broken for our entire department channel. It either shows 'something went "
            "wrong' or just loads indefinitely. We have 45 people who rely on this for daily file "
            "collaboration.",
        ),
        gold=ScenarioGold(
            category="Data & Storage",
            priority="P3",
            assigned_team="Data Platform",
            needs_escalation=False,
            missing_information=(
                "affected_system",
                "error_message",
            ),
            next_best_action="Investigate the Teams-SharePoint integration for the affected channel's underlying document library",
            remediation_steps=(
                "Access the underlying SharePoint document library directly to verify it's operational",
                "Check if the SharePoint site storage limit has been reached",
                "Clear the Teams desktop client cache and restart",
                "If the issue is channel-specific, check for corrupted files or folder structures",
                "If persistent, recreate the Files tab connection to the SharePoint library",
            ),
        ),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 10. Archive mailbox search not returning results
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="data-storage-010",
        subjects=(
            "Can't search old emails in archive mailbox",
            "Archive mailbox search returns nothing",
        ),
        descriptions=(
            "I'm trying to search for emails from 2024 in my archive mailbox but the search returns zero "
            "results even though I know the emails are there. I can browse to them manually but search is "
            "completely broken for archived items.",
            "The search functionality in my Outlook archive mailbox doesn't work. I need to find specific "
            "client correspondence from last year for a legal matter. Manual browsing takes forever with "
            "50,000+ archived emails.",
        ),
        gold=ScenarioGold(
            category="Data & Storage",
            priority="P3",
            assigned_team="Data Platform",
            needs_escalation=False,
            missing_information=(
                "affected_system",
            ),
            next_best_action="Check the archive mailbox search index status and rebuild if necessary",
            remediation_steps=(
                "Check the search index status for the user's archive mailbox",
                "Verify the archive mailbox is properly connected to the user's profile",
                "Initiate a search index rebuild for the archive mailbox if corrupted",
                "As a workaround, use Outlook Web Access search which uses server-side indexing",
                "Confirm search functionality is restored after index rebuild",
            ),
        ),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 11. Data retention policy deleting files too early
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="data-storage-011",
        subjects=(
            "Retention policy deleting our files prematurely",
            "Important documents being auto-deleted by retention policy",
        ),
        descriptions=(
            "Files in our project SharePoint site are being automatically deleted after 90 days, but our "
            "project runs for 2 years. We need these documents retained for the entire project duration "
            "plus 7 years for regulatory compliance. The current retention policy is wrong for our site.",
            "Our team's documents keep disappearing from SharePoint. We figured out it's an auto-deletion "
            "retention policy set to 60 days. These are active project files that we need. Can this policy "
            "be changed for our site?",
        ),
        gold=ScenarioGold(
            category="Data & Storage",
            priority="P2",
            assigned_team="Data Platform",
            needs_escalation=False,
            missing_information=(
                "affected_system",
                "business_impact",
            ),
            next_best_action=(
                "Review and adjust the retention policy for the affected SharePoint site to match business "
                "requirements"
            ),
            remediation_steps=(
                "Identify the current retention policy applied to the SharePoint site",
                "Review the business and regulatory retention requirements",
                "Modify the retention policy label or create a new one with the correct duration",
                "Apply the updated policy to the affected site",
                "Recover any recently deleted files from the recycle bin or backup",
            ),
        ),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 12. SharePoint list hitting 5000 item threshold
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="data-storage-012",
        subjects=(
            "SharePoint list view threshold exceeded",
            "SharePoint list too large — can't view items",
        ),
        descriptions=(
            "Our inventory tracking SharePoint list has exceeded the 5,000 item view threshold and now we "
            "get errors when trying to view or filter the list. We have about 12,000 items and growing. The "
            "Operations team relies on this list daily.",
            "Getting 'the attempted operation is prohibited because it exceeds the list view threshold' "
            "error on our project tracking SharePoint list. We've been using this list for 3 years and it's "
            "gotten too big. What are our options?",
        ),
        gold=ScenarioGold(
            category="Data & Storage",
            priority="P3",
            assigned_team="Data Platform",
            needs_escalation=False,
            missing_information=(),
            next_best_action="Optimize the SharePoint list with indexed columns and filtered views to work within the threshold",
            remediation_steps=(
                "Add indexes on the most commonly filtered/sorted columns",
                "Create filtered views that return fewer than 5,000 items",
                "Archive old items to a separate list or export to Excel",
                "Consider migrating to a SharePoint list with modern experience for better performance",
                "If the list continues to grow, evaluate migration to a proper database solution",
            ),
        ),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 13. OneDrive files showing as syncing for days
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="data-storage-013",
        subjects=(
            "OneDrive files stuck in 'syncing' state for days",
            "OneDrive sync never completes",
        ),
        descriptions=(
            "Several files in my OneDrive have been showing the 'sync in progress' icon for 5 days now. "
            "They're medium-sized Excel files (10-50 MB). I've tried right-clicking and choosing 'sync now' "
            "but nothing changes. Upload speed test shows my internet is fine.",
            "I have about 30 files stuck in perpetual sync state on OneDrive. The blue circular arrow icon "
            "never goes away. Some are files I edited last week. I'm concerned they aren't being backed up "
            "to the cloud.",
        ),
        gold=ScenarioGold(
            category="Data & Storage",
            priority="P3",
            assigned_team="Data Platform",
            needs_escalation=False,
            missing_information=(
                "device_info",
            ),
            next_best_action="Reset the OneDrive sync state for the stuck files and check for file locking issues",
            remediation_steps=(
                "Check if any of the stuck files are open or locked by another process",
                "Verify OneDrive client is up to date",
                "Pause and resume OneDrive sync",
                "If still stuck, move the affected files out of OneDrive, let sync complete, then move back",
                "As last resort, reset the OneDrive sync client with onedrive.exe /reset",
            ),
        ),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 14. Need new SharePoint site for project team
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="data-storage-014",
        subjects=(
            "Request for new SharePoint site",
            "New SharePoint site needed for Project Phoenix",
        ),
        descriptions=(
            "We're kicking off Project Phoenix next month and need a new SharePoint team site. "
            "Requirements: document library for project deliverables, a project task list, and external "
            "sharing enabled for our consulting partners at Deloitte. Site owners: myself and Janet Liu.",
            "Can we get a new SharePoint Online site created for the Digital Transformation Initiative? We "
            "need: team site, custom permissions for 3 workstreams, and integration with our project Teams "
            "channel. About 25 team members.",
        ),
        gold=ScenarioGold(
            category="Data & Storage",
            priority="P4",
            assigned_team="Data Platform",
            needs_escalation=False,
            missing_information=(),
            next_best_action="Create the new SharePoint site with the requested configuration and permissions",
            remediation_steps=(
                "Create the SharePoint team site with the specified name and URL",
                "Configure site owners and member permissions",
                "Set up the document library structure as requested",
                "Enable external sharing if approved by security team",
                "Provide the site URL and admin guide to the requestors",
            ),
        ),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 15. File share permissions not inheriting correctly
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="data-storage-015",
        subjects=(
            "File share permissions broken — new files not inheriting",
            "Subfolder permissions not matching parent",
        ),
        descriptions=(
            "New files and subfolders created in our shared drive aren't inheriting the parent folder's "
            "permissions. Users create a new folder and only they can see it. We have to manually set "
            "permissions on every new item. This is the \\fileserver01\Legal share.",
            "Permission inheritance is broken on our department file share. When I create a new document, "
            "my colleagues can't access it until IT manually fixes the permissions. This started after the "
            "server migration last month.",
        ),
        gold=ScenarioGold(
            category="Data & Storage",
            priority="P3",
            assigned_team="Data Platform",
            needs_escalation=False,
            missing_information=(
                "affected_system",
            ),
            next_best_action="Check and repair NTFS permission inheritance on the affected file share",
            remediation_steps=(
                "Examine the NTFS permissions on the parent folder",
                "Verify permission inheritance is enabled and not broken at any level",
                "Reset inheritance on the affected folder tree using icacls",
                "Verify new files and folders correctly inherit parent permissions",
                "If the migration caused the issue, re-apply the original ACL structure from backup",
            ),
        ),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 16. Database backup job failing nightly
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="data-storage-016",
        subjects=(
            "Database backup failing every night",
            "SQL backup job errors — backups not running",
        ),
        descriptions=(
            "The nightly backup job for our production databases has been failing for the past 3 nights. "
            "Error: 'insufficient disk space on backup target.' The backup storage is at 95% capacity. We "
            "need to either add storage or clean up old backups. If we lose this database without backup, "
            "it's catastrophic.",
            "Our automated database backups are failing with 'operating system error 112 (not enough "
            "space).' The backup drive is full. This means our production SQL databases haven't been backed "
            "up in 3 days. This is a critical gap in our disaster recovery.",
        ),
        gold=ScenarioGold(
            category="Data & Storage",
            priority="P1",
            assigned_team="Data Platform",
            needs_escalation=True,
            missing_information=(),
            next_best_action="Free up backup storage immediately and run a manual backup to restore the DR capability",
            remediation_steps=(
                "Check backup storage utilization and identify old backups that can be archived or deleted",
                "Free up sufficient space for at least one full backup cycle",
                "Run a manual full backup immediately to restore the backup chain",
                "Expand the backup storage capacity to prevent recurrence",
                "Set up monitoring alerts for backup storage utilization at 80% threshold",
            ),
        ),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 17. Large file upload failing on SharePoint
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="data-storage-017",
        subjects=(
            "Can't upload large file to SharePoint",
            "SharePoint upload fails for files over 1 GB",
        ),
        descriptions=(
            "I'm trying to upload a 2.5 GB video file to our team SharePoint site but the upload fails at "
            "about 60% every time. I've tried the browser, OneDrive sync client, and even SharePoint "
            "Explorer view. The file is a training video that the whole team needs access to.",
            "SharePoint file upload keeps timing out for our large CAD files (1.5-3 GB). The upload starts "
            "but never completes. Getting 'upload failed' without a specific error. These are engineering "
            "design files needed for the client review.",
        ),
        gold=ScenarioGold(
            category="Data & Storage",
            priority="P3",
            assigned_team="Data Platform",
            needs_escalation=False,
            missing_information=(
                "affected_system",
            ),
            next_best_action=(
                "Check the SharePoint upload limits and use the OneDrive sync client or PowerShell for large "
                "file uploads"
            ),
            remediation_steps=(
                "Verify the SharePoint file size upload limit (default 250 GB in SPO)",
                "Check if the site storage quota has been reached",
                "Try uploading via the OneDrive sync client which handles large files better",
                "If browser upload fails, use SharePoint PowerShell or Graph API for chunked upload",
                "For very large media files, consider Azure Blob Storage with a SharePoint link",
            ),
        ),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 18. Data migration from on-prem file server
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="data-storage-018",
        subjects=(
            "Need data migration from retiring file server",
            "File server decommission — data migration needed",
        ),
        descriptions=(
            "We're decommissioning fileserver03 next month and need to migrate approximately 4 TB of data "
            "to SharePoint Online and Azure Files. The data includes: HR documents (sensitive), Finance "
            "reports, and General department files. Need a migration plan with proper data classification.",
            "Our on-premises file server is end-of-life in 6 weeks. We need to move 1.5 TB of data to the "
            "cloud. The data has mixed sensitivity — some contains PII, some is public. We need help "
            "classifying and migrating appropriately.",
        ),
        gold=ScenarioGold(
            category="Data & Storage",
            priority="P3",
            assigned_team="Data Platform",
            needs_escalation=False,
            missing_information=(
                "business_impact",
            ),
            next_best_action="Create a data migration plan with classification, target selection, and timeline",
            remediation_steps=(
                "Inventory the file server content by size, type, and sensitivity",
                "Classify data and determine appropriate cloud destination for each category",
                "Create a phased migration plan with testing milestones",
                "Execute the migration using appropriate tools and validate data integrity",
                "Decommission the old server after migration confirmation period",
            ),
        ),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 19. Power Automate flow failing due to SharePoint permissions
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="data-storage-019",
        subjects=(
            "Power Automate flow broken — SharePoint access issue",
            "Automated workflow failing on SharePoint",
        ),
        descriptions=(
            "My Power Automate flow that copies approved invoices from our Inbox list to the Archive "
            "library stopped working yesterday. Error: 'The caller does not have permission to access the "
            "resource.' Nothing changed on my end — I think someone modified the SharePoint permissions.",
            "Our automated document approval workflow in Power Automate is failing at the step where it "
            "writes to the Approved Documents library in SharePoint. It was working fine until the "
            "SharePoint site permissions were restructured last week.",
        ),
        gold=ScenarioGold(
            category="Data & Storage",
            priority="P3",
            assigned_team="Data Platform",
            needs_escalation=False,
            missing_information=(
                "error_message",
                "configuration_details",
            ),
            next_best_action="Check the service account permissions used by the Power Automate flow on the SharePoint site",
            remediation_steps=(
                "Identify the connection account used by the Power Automate flow",
                "Check if the account's SharePoint permissions were modified",
                "Restore the necessary permissions for the automation account",
                "Re-authorize the SharePoint connection in Power Automate if needed",
                "Test the flow end-to-end to verify it completes successfully",
            ),
        ),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 20. Azure Blob storage access for data science team
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="data-storage-020",
        subjects=(
            "Need Azure Blob Storage access for ML project",
            "Azure storage account access request",
        ),
        descriptions=(
            "The data science team needs access to the Azure Blob Storage account 'contosodatalake' for our "
            "machine learning project. We need Reader and Data Contributor roles on the 'ml-training-data' "
            "container. Manager approval from Dr. Priya Sharma is attached.",
            "Requesting access to Azure Storage account 'contoso-analytics-prod' for the Research team. We "
            "need to read large datasets for our quantitative analysis models. Specifically the "
            "'market-data' and 'risk-models' containers.",
        ),
        gold=ScenarioGold(
            category="Data & Storage",
            priority="P3",
            assigned_team="Data Platform",
            needs_escalation=False,
            missing_information=(),
            next_best_action="Grant the approved Azure Blob Storage RBAC roles to the requesting users",
            remediation_steps=(
                "Verify the manager and data owner approval",
                "Assign the Storage Blob Data Reader and Data Contributor RBAC roles",
                "Scope the assignment to the specific container",
                "Verify the users can access the storage account and containers",
                "Document the access grant in the data access register",
            ),
        ),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 21. Shared drive mapped drive letter conflict
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="data-storage-021",
        subjects=(
            "Drive letter conflict — can't map shared drive",
            "Mapped drive letter already in use",
        ),
        descriptions=(
            "I can't map the Finance shared drive because the letter G: is already taken by something else "
            "on my laptop. Our documentation says to use G: for the Finance share, but I have a USB drive "
            "that always takes G:. Can IT help resolve this conflict?",
            "The login script is trying to map H: to the department share but it fails because H: is "
            "already mapped to a different share from my previous department. I've tried disconnecting it "
            "but it comes back after every reboot.",
        ),
        gold=ScenarioGold(
            category="Data & Storage",
            priority="P4",
            assigned_team="Data Platform",
            needs_escalation=False,
            missing_information=(
                "device_info",
            ),
            next_best_action="Resolve the drive letter conflict by reassigning or updating the login script mapping",
            remediation_steps=(
                "Check current drive letter mappings with 'net use' command",
                "Disconnect the conflicting mapped drive",
                "Update the login script or Group Policy drive mapping for the user",
                "If USB drive conflict, assign a different letter via disk management",
                "Verify the correct share is mapped after the change",
            ),
        ),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 22. SharePoint search returning no results
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="data-storage-022",
        subjects=(
            "SharePoint search completely broken",
            "Can't find any documents in SharePoint search",
        ),
        descriptions=(
            "SharePoint search returns zero results for any search query on our department site. I'm "
            "searching for documents I know exist — I can browse to them manually. This has been broken for "
            "about a week. Makes finding anything impossible.",
            "The search functionality on our SharePoint Online site has stopped working entirely. No matter "
            "what I search for, it says 'no results found.' Our site has over 10,000 documents. Other team "
            "members have the same issue on this specific site.",
        ),
        gold=ScenarioGold(
            category="Data & Storage",
            priority="P3",
            assigned_team="Data Platform",
            needs_escalation=False,
            missing_information=(
                "affected_system",
            ),
            next_best_action="Check the SharePoint search crawl status and rebuild the search index for the affected site",
            remediation_steps=(
                "Check the search crawl log for the affected site collection",
                "Verify the site is not excluded from the search index",
                "Request a re-crawl of the affected site",
                "Check if search schema or managed properties were modified",
                "Verify search results return after the re-crawl completes",
            ),
        ),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 23. Database connection string update needed
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="data-storage-023",
        subjects=(
            "Database connection string needs updating after server move",
            "App can't connect to database after migration",
        ),
        descriptions=(
            "Our internal reporting application can't connect to the database after the SQL server "
            "migration this weekend. The connection string still points to the old server "
            "(sql-old.contoso.local) which has been decommissioned. Need to update to "
            "sql-prod-02.contoso.local.",
            "After the database server migration, 3 of our applications are failing to connect. They're "
            "using hardcoded connection strings pointing to the old server. We need the DNS alias updated "
            "or the apps reconfigured. This is affecting daily operations.",
        ),
        gold=ScenarioGold(
            category="Data & Storage",
            priority="P2",
            assigned_team="Data Platform",
            needs_escalation=False,
            missing_information=(
                "affected_system",
                "configuration_details",
            ),
            next_best_action="Update the DNS CNAME alias or application connection strings to point to the new database server",
            remediation_steps=(
                "Create a DNS CNAME alias pointing the old server name to the new server",
                "Alternatively, update the connection strings in application configuration",
                "Update any references in key vaults or configuration management systems",
                "Test each affected application to confirm database connectivity",
                "Decommission the DNS alias after all applications are updated to use the new server name",
            ),
        ),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 24. Teams channel files moved or missing
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="data-storage-024",
        subjects=(
            "Files disappeared from our Teams channel",
            "Teams channel files folder is empty",
        ),
        descriptions=(
            "All the files in our Project Alpha Teams channel have disappeared. The Files tab shows an "
            "empty folder. We had months of project documents, meeting recordings, and shared resources in "
            "there. Nobody on the team intentionally deleted anything.",
            "The files in our Marketing team's General channel are gone. The tab says 'this folder is "
            "empty' but we had 200+ files. Some team members can still see a few files but most are "
            "missing. This is critical — we have a campaign launch on Friday.",
        ),
        gold=ScenarioGold(
            category="Data & Storage",
            priority="P2",
            assigned_team="Data Platform",
            needs_escalation=False,
            missing_information=(
                "timestamp",
            ),
            next_best_action="Check the underlying SharePoint recycle bin and audit logs to locate and restore the missing files",
            remediation_steps=(
                "Access the underlying SharePoint site for the Teams channel",
                "Check the site recycle bin and second-stage recycle bin for deleted files",
                "Review the SharePoint audit log for bulk delete operations",
                "If files were moved, check if they're in a different folder or document library",
                "Restore the files from recycle bin or backup",
            ),
        ),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 25. Data recovery from corrupted USB drive
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="data-storage-025",
        subjects=(
            "USB drive corrupted — need data recovery",
            "Important files on damaged USB stick",
        ),
        descriptions=(
            "My USB flash drive is corrupted and Windows is asking me to format it. I have important client "
            "presentation files on it that aren't backed up anywhere else (I know, I know). Is there any "
            "way IT can recover the data before I reformat?",
            "My external USB hard drive stopped being recognized by Windows. It was working fine yesterday "
            "but now it just makes a clicking sound and doesn't show up in File Explorer. It has about 100 "
            "GB of archived project files I need.",
        ),
        gold=ScenarioGold(
            category="Data & Storage",
            priority="P3",
            assigned_team="Data Platform",
            needs_escalation=False,
            missing_information=(
                "device_info",
            ),
            next_best_action="Attempt data recovery using recovery tools before any format or write operations on the drive",
            remediation_steps=(
                "Do NOT format the drive — this makes recovery harder",
                "Try the drive on a different USB port and computer",
                "Use disk management to check if the partition is visible",
                "Attempt recovery with data recovery software",
                "If physical damage is suspected, recommend professional data recovery service",
            ),
        ),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 26. SharePoint site storage limit approaching
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="data-storage-026",
        subjects=(
            "SharePoint site nearing storage limit",
            "Running out of space on team SharePoint",
        ),
        descriptions=(
            "Our department SharePoint site is at 24.5 GB out of 25 GB storage limit. We're about to hit "
            "the wall and won't be able to upload any more documents. We have active projects that need "
            "document storage. Can we get the limit increased?",
            "SharePoint storage quota warning — our site collection is at 97% capacity. We need either more "
            "storage allocated or guidance on archiving old content. Deleting files isn't an option as most "
            "are required for compliance retention.",
        ),
        gold=ScenarioGold(
            category="Data & Storage",
            priority="P3",
            assigned_team="Data Platform",
            needs_escalation=False,
            missing_information=(),
            next_best_action="Increase the SharePoint site storage quota and review content for archival opportunities",
            remediation_steps=(
                "Check the current storage allocation and usage breakdown",
                "Increase the site storage quota from the SharePoint admin center",
                "Identify large or old files that can be archived to a separate site",
                "Enable versioning limits to reduce storage used by file versions",
                "Set up storage usage alerts at 80% and 90% thresholds",
            ),
        ),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 27. OneDrive known folder move failing
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="data-storage-027",
        subjects=(
            "OneDrive Known Folder Move not working",
            "KFM policy failing on my laptop",
        ),
        descriptions=(
            "The OneDrive Known Folder Move policy is failing on my laptop. I keep getting an error saying "
            "'files can't be moved' when it tries to redirect my Desktop and Documents folders to OneDrive. "
            "I have about 40 GB in my Documents folder.",
            "KFM deployment isn't working on my machine. The IT policy is supposed to redirect my folders "
            "to OneDrive but the migration keeps failing with 'unsupported file type' errors. I think some "
            "of my .pst and .iso files are causing the issue.",
        ),
        gold=ScenarioGold(
            category="Data & Storage",
            priority="P3",
            assigned_team="Data Platform",
            needs_escalation=False,
            missing_information=(
                "device_info",
                "error_message",
            ),
            next_best_action="Identify the files blocking KFM and resolve the incompatibilities",
            remediation_steps=(
                "Check the KFM error log for specific files blocking the migration",
                "Identify unsupported file types or files with sync-incompatible names",
                "Move blocking files to a location outside the known folders",
                "Re-initiate the Known Folder Move policy",
                "Verify Desktop and Documents folders are successfully redirected to OneDrive",
            ),
        ),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 28. Data warehouse ETL job stuck — revenue reporting impacted
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="data-storage-028",
        subjects=(
            "CRITICAL: Data warehouse ETL stuck — daily reports not generated",
            "ETL pipeline failure affecting financial reporting",
        ),
        descriptions=(
            "Our data warehouse ETL pipeline has been stuck for 8 hours. The daily financial reports that "
            "trading desk and risk management depend on haven't been generated. The ETL job appears hung on "
            "the fact table load step. This impacts regulatory reporting due by end of day.",
            "URGENT: The nightly ETL process that feeds our reporting data warehouse failed and didn't "
            "complete. Finance needs the daily P&L report for the board meeting at 10 AM. The pipeline is "
            "stuck on a data transformation step with a memory error.",
        ),
        gold=ScenarioGold(
            category="Data & Storage",
            priority="P1",
            assigned_team="Data Platform",
            needs_escalation=True,
            missing_information=(),
            next_best_action="Investigate and restart the stuck ETL job immediately to restore financial reporting capability",
            remediation_steps=(
                "Check the ETL job status and identify the failed step",
                "Review the error logs for the specific failure reason",
                "If memory issue, restart the ETL server and rerun from the failed step",
                "Monitor the job through to completion",
                "Notify the Finance and trading teams when reports are available",
            ),
        ),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 29. File versioning conflict on shared document
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="data-storage-029",
        subjects=(
            "Version conflict on shared Excel file",
            "Multiple people edited same file — version conflict",
        ),
        descriptions=(
            "Three of us were editing the same Excel file on SharePoint simultaneously and now there are "
            "conflicting versions. The file shows my changes but my colleagues' updates are in 'conflict' "
            "copies. We need to merge all three versions into one master document before the client meeting.",
            "We have a version conflict nightmare on a critical budget spreadsheet in SharePoint. Four "
            "people made changes to different sheets in the same workbook over the weekend. Now there are 4 "
            "different versions and we need to reconcile them.",
        ),
        gold=ScenarioGold(
            category="Data & Storage",
            priority="P3",
            assigned_team="Data Platform",
            needs_escalation=False,
            missing_information=(),
            next_best_action="Help reconcile the conflicting versions using SharePoint version history",
            remediation_steps=(
                "Access the file's version history in SharePoint",
                "Download each conflicting version to compare changes",
                "Use Excel's merge workbooks feature or manually reconcile changes",
                "Upload the consolidated version as the current version",
                "Advise the team to use co-authoring or check-out to prevent future conflicts",
            ),
        ),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 30. Compliance hold on mailbox preventing deletion
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="data-storage-030",
        subjects=(
            "Can't delete old emails — compliance hold",
            "Mailbox at capacity but legal hold preventing cleanup",
        ),
        descriptions=(
            "My mailbox is full but I can't delete anything because there's a litigation hold on my account "
            "from a legal case 2 years ago. The case has been settled. Can the hold be removed so I can "
            "clean up my mailbox? I'm unable to receive new emails.",
            "I need the eDiscovery hold removed from my mailbox. The legal matter (Case #LIT-2024-089) was "
            "resolved 6 months ago but the hold is still active. My mailbox is at 49.5 GB out of 50 GB and "
            "I can't work effectively.",
        ),
        gold=ScenarioGold(
            category="Data & Storage",
            priority="P3",
            assigned_team="Data Platform",
            needs_escalation=False,
            missing_information=(
                "business_impact",
            ),
            next_best_action="Coordinate with Legal to confirm the hold can be released, then remove it from the mailbox",
            remediation_steps=(
                "Verify with the Legal department that the litigation hold can be removed",
                "Get written confirmation from Legal or Compliance to release the hold",
                "Remove the eDiscovery or litigation hold from the mailbox in Exchange admin",
                "Increase the mailbox quota temporarily if the hold removal takes time",
                "Confirm the user can delete emails and manage their mailbox normally",
            ),
        ),
    ),
]
