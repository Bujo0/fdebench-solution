"""Software & Applications scenario definitions."""

from generator.models import Scenario

SCENARIOS: list[Scenario] = [
    # ── 1. Outlook crashes when opening specific attachments ─────────────
    Scenario(
        scenario_id="sw-outlook-attachment-crash",
        category="Software & Applications",
        priority="P3",
        assigned_team="Endpoint Engineering",
        needs_escalation=False,
        missing_information=["error_message", "application_version", "steps_to_reproduce"],
        subjects=[
            "Outlook crashes every time I open a PDF attachment",
            "Outlook freezing and closing when I try to open attachments",
            "Outlook keeps crashing on specific email attachments",
            "Can't open attachments in Outlook — app crashes immediately",
        ],
        descriptions=[
            "Every time I try to open a PDF attachment in Outlook it freezes for about 10 seconds and then crashes comp"
            "letely. I have to reopen Outlook and lose whatever I was working on. This started after last Tuesday's upd"
            "ate. Other file types like .docx seem fine.",
            "Outlook is crashing whenever I preview or open certain attachments — mostly PDFs and .xlsx files over 5 MB"
            ". I'm on Outlook desktop version on Windows 11. I've already tried running the Office repair tool but it d"
            "idn't help. I need to review client contracts by end of day.",
            "Since Monday morning Outlook crashes the moment I click on any attachment from external senders. Internal "
            "attachments open fine. I think it might be related to the new security update that was pushed. I've lost "
            "work twice today because of this.",
        ],
        next_best_actions=[
            "Collect crash dump logs and check for recent Office update correlation. Test with Outlook safe mode to "
            "rule out add-in conflicts.",
            "Verify Office version and recent update history. Run Outlook in safe mode and test attachment handling to "
            "isolate the issue.",
        ],
        remediation_steps=[
            [
                "Launch Outlook in safe mode (outlook.exe /safe) and test attachment opening",
                "If safe mode works, disable add-ins one by one to find the conflicting add-in",
                "Check Office update history for recent patches and roll back if correlated",
                "Clear the Outlook attachment preview cache in %localappdata%\\Microsoft\\Outlook",
                "Run Office Online Repair if issue persists",
                "Verify attachments open correctly after remediation",
            ],
        ],
    ),
    # ── 2. Teams white screen / crash on launch ─────────────────────────
    Scenario(
        scenario_id="sw-teams-white-screen",
        category="Software & Applications",
        priority="P4",
        assigned_team="Endpoint Engineering",
        needs_escalation=False,
        missing_information=["device_info", "application_version"],
        subjects=[
            "Teams shows a white screen and won't load",
            "Microsoft Teams just displays blank white page on startup",
            "Teams app crashes immediately after launch — blank screen",
            "Teams won't start — stuck on white screen",
        ],
        descriptions=[
            "When I open Microsoft Teams it just shows a completely white screen and never loads. I've waited over 10 "
            "minutes. I can use Teams in the browser fine, so it's just the desktop app. I've tried restarting my "
            "computer twice. Need the desktop app for screen sharing in client calls.",
            "Teams desktop client opens to a blank white page. I've cleared the cache, reinstalled the app, and "
            "restarted. Nothing works. This started happening after the Windows update last night. I'm on a Lenovo "
            "ThinkPad running Windows 11.",
            "My Teams app is completely broken — just a white screen every time I open it. Other people on my floor "
            "seem fine. I've tried deleting the Teams cache folder and reinstalling. I need the desktop client working "
            "for a video presentation tomorrow.",
        ],
        next_best_actions=[
            "Clear Teams cache and reset app data. Check for GPU rendering conflicts and try disabling hardware "
            "acceleration.",
            "Uninstall Teams completely, clear all cache directories, and perform a clean reinstall. Check Windows "
            "Event Viewer for related errors.",
        ],
        remediation_steps=[
            [
                "Close Teams and clear the cache folder at %appdata%\\Microsoft\\Teams",
                "Delete the Teams credentials from Windows Credential Manager",
                "Check if GPU hardware acceleration is causing rendering issues — disable it in Teams settings if "
                "accessible",
                "If issue persists, fully uninstall Teams and remove residual folders",
                "Reinstall the latest version of Teams from the company portal",
                "Verify Teams launches and loads correctly after reinstall",
            ],
        ],
    ),
    # ── 3. Excel macro not running due to security policy ────────────────
    Scenario(
        scenario_id="sw-excel-macro-blocked",
        category="Software & Applications",
        priority="P3",
        assigned_team="Endpoint Engineering",
        needs_escalation=False,
        missing_information=["affected_system", "screenshot_or_attachment", "business_impact"],
        subjects=[
            "Excel macros blocked by security policy — can't run reports",
            "VBA macros disabled in Excel — need them for daily work",
            "Excel showing 'macros have been disabled' on all spreadsheets",
            "Security policy blocking macro-enabled Excel files",
        ],
        descriptions=[
            "All my macro-enabled Excel workbooks are showing a red banner saying 'SECURITY RISK — Microsoft has "
            "blocked macros from running because the source of this file is untrusted.' These are files I created "
            "myself and have used for years. I run these macros daily to generate risk reports for the trading desk.",
            "Since the latest security policy push, none of my Excel VBA macros will execute. I get a security warning "
            "about macros being blocked. I need these for monthly financial consolidation — they automate a 6-hour "
            "manual process. We're in the middle of quarter-end close.",
            "Our team relies on several macro-enabled workbooks for compliance reporting. After the recent update, "
            "Excel blocks all macros regardless of the source. Even files saved on our departmental SharePoint are "
            "affected. This is blocking the entire compliance team's workflow.",
        ],
        next_best_actions=[
            "Review the macro security policy pushed via Group Policy or Intune. Add trusted locations for departmental"
            " file shares and SharePoint sites.",
            "Check the Office Trust Center settings and Group Policy for macro blocking rules. Configure trusted "
            "locations or code-sign the macros.",
        ],
        remediation_steps=[
            [
                "Identify the Group Policy or Intune configuration profile blocking macros",
                "Review the macro files for security and verify they are internally created",
                "Add appropriate network paths and SharePoint sites to Office Trusted Locations",
                "If possible, digitally sign the macros with the organization's code-signing certificate",
                "Push updated policy to the affected devices via Intune or GPO",
                "Verify macros execute correctly in the trusted locations",
                "Document approved macro locations for future reference",
            ],
        ],
    ),
    # ── 4. Adobe Reader/Acrobat update required ──────────────────────────
    Scenario(
        scenario_id="sw-adobe-update-needed",
        category="Software & Applications",
        priority="P4",
        assigned_team="Endpoint Engineering",
        needs_escalation=False,
        missing_information=["application_version", "device_info"],
        subjects=[
            "Adobe Acrobat is outdated and won't open new PDFs",
            "Need Adobe Reader updated — getting compatibility errors",
            "Adobe Acrobat update prompt keeps appearing but can't install",
            "Adobe PDF viewer needs to be updated — blocked by admin rights",
        ],
        descriptions=[
            "Adobe Acrobat Reader keeps telling me an update is available but when I click update it says I need admin "
            "rights. I'm getting compatibility warnings when opening PDFs from external law firms. Can someone push the"
            " update to my machine?",
            "My Adobe Acrobat is on version 2020 and several client contracts won't open because they were created in a"
            " newer version. I don't have admin rights to update it myself. Can IT push the latest version to my laptop"
            "?",
            "I keep getting popups saying my Adobe Reader is out of date and has security vulnerabilities. I can't "
            "install the update because of company restrictions. Also, some newer PDF forms don't render correctly in "
            "my current version.",
        ],
        next_best_actions=[
            "Push the latest approved Adobe Acrobat version to the user's device via SCCM or Intune.",
            "Check the current software catalog for the approved Adobe version and deploy it to the user's endpoint.",
        ],
        remediation_steps=[
            [
                "Check the current Adobe version installed on the user's device",
                "Verify the latest approved Adobe version in the software deployment catalog",
                "Push the update via Intune or SCCM to the user's device",
                "Verify the update installed successfully and Adobe launches correctly",
                "Confirm the user can open the previously problematic PDF files",
            ],
        ],
    ),
    # ── 5. Software installation request (Python, VS Code) ──────────────
    Scenario(
        scenario_id="sw-install-request-dev-tools",
        category="Software & Applications",
        priority="P4",
        assigned_team="Endpoint Engineering",
        needs_escalation=False,
        missing_information=["business_impact", "application_version"],
        subjects=[
            "Request to install Python and VS Code on my workstation",
            "Need developer tools installed — Python, Git, VS Code",
            "Software installation request for data analysis tools",
            "Can't install Python — need it for work, requesting approval",
        ],
        descriptions=[
            "I need Python 3.12 and Visual Studio Code installed on my workstation for a new data analytics project. "
            "I'm in the Quantitative Research team and need these tools to build risk models. My manager has approved "
            "the request — attaching the email.",
            "Requesting installation of Python 3.x, Git, and VS Code. I've been assigned to an automation project for t"
            "he Operations team and need these development tools. They aren't available in the Company Portal. Manager "
            "approval from David Chen attached.",
            "I need Anaconda (Python distribution) and VS Code installed for a machine-learning project in the "
            "Portfolio Analytics group. Our team lead approved the software request. We have a project kickoff next "
            "Monday and I need the tools ready.",
        ],
        next_best_actions=[
            "Verify manager approval and add the requested software to the user's Intune assignment. Deploy via Company"
            " Portal.",
            "Process software request through the approval workflow and deploy approved packages to the user's device.",
        ],
        remediation_steps=[
            [
                "Verify manager approval and check software against the approved catalog",
                "If software is in the approved catalog, assign the package to the user via Intune",
                "If software requires security review, submit for approval with business justification",
                "Deploy the approved software package to the user's device",
                "Verify installation completed and the tools launch correctly",
                "Ensure any required firewall or proxy exceptions are in place for package managers (pip, npm)",
            ],
        ],
    ),
    # ── 6. Office 365 license upgrade request (E3 → E5) ─────────────────
    Scenario(
        scenario_id="sw-o365-license-upgrade",
        category="Software & Applications",
        priority="P4",
        assigned_team="Enterprise Applications",
        needs_escalation=False,
        missing_information=["business_impact", "affected_users"],
        subjects=[
            "Request to upgrade my Office 365 license from E3 to E5",
            "Need M365 E5 license for Power BI Pro and advanced compliance",
            "Office 365 license upgrade request — E3 to E5",
            "Requesting E5 license for advanced analytics features",
        ],
        descriptions=[
            "I need my Microsoft 365 license upgraded from E3 to E5. I've been asked to lead a compliance automation "
            "project that requires Microsoft Purview features and Power BI Pro, both of which need E5. My director "
            "approved the upgrade — CC'd on this ticket.",
            "Requesting an M365 E5 license upgrade. I currently have E3 but need the advanced compliance and eDiscovery"
            " features for an upcoming regulatory audit. Budget has been approved by our department head. Currently 3 o"
            "f us on the team need the upgrade.",
            "Our analytics team (5 people) needs to be upgraded from E3 to E5 licenses to access advanced Power BI and "
            "Defender features. The budget was approved in Q3 planning. Attaching the approval from our VP of Finance.",
        ],
        next_best_actions=[
            "Verify budget approval and license availability. Upgrade the user's M365 license in the admin portal.",
            "Check license inventory for available E5 seats and process the upgrade with appropriate approvals.",
        ],
        remediation_steps=[
            [
                "Verify management and budget approval for the license upgrade",
                "Check available E5 license inventory in the M365 Admin Center",
                "Remove the current E3 license assignment from the user(s)",
                "Assign the E5 license and verify all expected features are available",
                "Confirm the user can access E5-specific services (Purview, Power BI Pro, etc.)",
            ],
        ],
    ),
    # ── 7. SAP transport stuck in queue ──────────────────────────────────
    Scenario(
        scenario_id="sw-sap-transport-stuck",
        category="Software & Applications",
        priority="P2",
        assigned_team="Enterprise Applications",
        needs_escalation=True,
        missing_information=["error_message", "environment_details", "timestamp"],
        subjects=[
            "SAP transport request stuck in queue — blocking deployment",
            "SAP transport won't import into production — stuck for 6 hours",
            "SAP transport queue jammed — critical change can't deploy",
            "Blocked SAP transport — need help with STMS import",
        ],
        descriptions=[
            "We have a critical SAP transport (DEVK9A0123) that has been stuck in the import queue for production for "
            "over 6 hours. The transport contains a fix for the month-end GL posting issue that's blocking Finance. "
            "STMS shows status 'waiting' but it never progresses. The transport imported fine to QA yesterday.",
            "An SAP transport request with payroll corrections is stuck in the production import queue since this "
            "morning. Status in STMS shows 'import running' but nothing is happening. We need this deployed before the "
            "payroll run at 5 PM today. Transport ID is PRDK900456.",
            "SAP transport for a critical regulatory reporting fix has been stuck in the QA-to-Production queue for 8 h"
            "ours. Other transports behind it are also blocked now. We have a regulatory deadline on Friday. The Basis "
            "team is at capacity and hasn't been able to look at it.",
        ],
        next_best_actions=[
            "Check STMS transport logs for error details. Investigate tp process status on the target system and check "
            "for lock conflicts.",
            "Review SAP transport logs (SE01/STMS) and check for import queue locks, background job failures, or "
            "resource contention on the target system.",
        ],
        remediation_steps=[
            [
                "Check the transport status and logs in STMS on the target system",
                "Verify the tp (transport program) process is running on the target app server",
                "Check for database locks or long-running background jobs blocking the import",
                "If the transport is genuinely stuck, reset the transport queue buffer",
                "Re-trigger the import after clearing the blockage",
                "Verify the transport imports successfully and objects are activated",
                "Confirm the transported changes are functional in the target system",
            ],
        ],
    ),
    # ── 8. JIRA / Azure DevOps down (502) ───────────────────────────────
    Scenario(
        scenario_id="sw-jira-devops-outage",
        category="Software & Applications",
        priority="P1",
        assigned_team="Enterprise Applications",
        needs_escalation=True,
        missing_information=["affected_users", "timestamp", "error_message"],
        subjects=[
            "JIRA is down — 502 Bad Gateway for all users",
            "Azure DevOps / JIRA completely unreachable — 502 errors",
            "JIRA outage — entire engineering team blocked",
            "502 errors on JIRA — nobody can access project boards",
        ],
        descriptions=[
            "JIRA has been returning 502 Bad Gateway errors for the last 20 minutes. Nobody on the engineering floor "
            "can access it — all project boards, backlogs, and sprint tracking are down. We have over 200 developers "
            "blocked and a major release planned for this afternoon. This is critical.",
            "Our JIRA instance at jira.contoso.com is completely down. Every request returns a 502 error. The entire "
            "Technology division — about 300 people — relies on this for daily work. We've already checked with the "
            "hosting team and they say the VMs are running. This started around 9:15 AM.",
            "JIRA went down at approximately 9:10 AM with 502 errors across all endpoints. All engineering squads are u"
            "nable to access sprint boards, file bugs, or update stories. We're in the middle of a production incident "
            "and can't even track the work. Need this escalated immediately.",
        ],
        next_best_actions=[
            "Check JIRA application server health, reverse proxy configuration, and recent deployment changes. Engage "
            "the hosting team for immediate investigation.",
            "Investigate the 502 at the load balancer / reverse proxy level. Check JIRA application logs and JVM heap "
            "usage. Prepare rollback if a recent change caused this.",
        ],
        remediation_steps=[
            [
                "Check the reverse proxy / load balancer logs for 502 upstream errors",
                "Verify JIRA application server processes are running and responsive",
                "Check JVM heap utilization and garbage collection logs for memory pressure",
                "Review recent configuration or plugin changes that may have caused instability",
                "Restart the JIRA application service if it is unresponsive",
                "Monitor application health after restart and confirm 502 errors resolve",
                "Communicate resolution and root cause to affected engineering teams",
            ],
        ],
        channel_weights={"email": 0.10, "chat": 0.40, "portal": 0.15, "phone": 0.35},
    ),
    # ── 9. Power BI dashboard showing incorrect data ─────────────────────
    Scenario(
        scenario_id="sw-powerbi-incorrect-data",
        category="Software & Applications",
        priority="P3",
        assigned_team="Enterprise Applications",
        needs_escalation=False,
        missing_information=["affected_system", "screenshot_or_attachment", "steps_to_reproduce"],
        subjects=[
            "Power BI dashboard showing wrong numbers for Q3 revenue",
            "Power BI report data doesn't match source system",
            "Incorrect data on executive Power BI dashboard",
            "Power BI visuals are out of date — data refresh seems broken",
        ],
        descriptions=[
            "The Q3 Revenue Dashboard in Power BI is showing revenue figures that are about $2.3M lower than what's in "
            "our SAP financial reports. The CFO noticed during this morning's executive meeting. The dashboard is "
            "supposed to refresh daily at 6 AM but the 'last refreshed' timestamp shows 3 days ago.",
            "Our Power BI sales pipeline dashboard is displaying incorrect win-rate percentages. The numbers don't matc"
            "h Salesforce at all — Power BI shows 32% but Salesforce shows 47%. I think the data gateway connection mig"
            "ht be broken. This dashboard is used in weekly leadership meetings.",
            "The risk exposure dashboard in Power BI is showing stale data. It should update every hour from the "
            "trading system but the last refresh was 2 days ago. The Risk Management team uses this for real-time "
            "position monitoring. Getting errors when I try to manually refresh.",
        ],
        next_best_actions=[
            "Check the Power BI data gateway status and scheduled refresh history for failures. Investigate the data "
            "source connection credentials.",
            "Review the dataset refresh history in Power BI Service for error details. Verify gateway connectivity and "
            "data source credentials.",
        ],
        remediation_steps=[
            [
                "Check the dataset refresh history in Power BI Service for error messages",
                "Verify the on-premises data gateway is online and healthy",
                "Check data source credentials stored in the gateway for expiration",
                "If credentials expired, update them in Power BI gateway data source settings",
                "Trigger a manual refresh and monitor for successful completion",
                "Verify the dashboard data matches the source system after refresh",
            ],
        ],
    ),
    # ── 10. Salesforce integration broken ────────────────────────────────
    Scenario(
        scenario_id="sw-salesforce-integration-broken",
        category="Software & Applications",
        priority="P2",
        assigned_team="Enterprise Applications",
        needs_escalation=True,
        missing_information=["error_message", "environment_details", "timestamp"],
        subjects=[
            "Salesforce-to-SAP integration stopped syncing since last night",
            "Salesforce integration broken — orders not flowing to SAP",
            "Critical Salesforce API integration failure",
            "Salesforce data sync to backend systems is failing",
        ],
        descriptions=[
            "The Salesforce-to-SAP integration that syncs closed-won opportunities into SAP sales orders stopped workin"
            "g last night around 11 PM. We have about 40 orders stuck that haven't been created in SAP. The sales team "
            "is panicking because fulfillment is delayed. The MuleSoft integration logs show authentication failures.",
            "Our Salesforce integration with the internal order management system is throwing 401 Unauthorized errors s"
            "ince this morning. No orders are flowing through. We checked and the Salesforce Connected App certificate "
            "may have expired. About 15 orders are backed up and growing.",
            "The nightly Salesforce data sync to our data warehouse failed. The integration job shows "
            "'INVALID_SESSION_ID' errors. This feeds the executive dashboards and the compliance reporting system. We "
            "need this restored before the 9 AM reporting cycle.",
        ],
        next_best_actions=[
            "Check Salesforce Connected App credentials and OAuth tokens. Review MuleSoft integration logs for specific"
            " error details and re-authenticate the integration.",
            "Investigate the authentication failure in integration logs. Rotate the Salesforce API credentials or "
            "certificate and restart the sync jobs.",
        ],
        remediation_steps=[
            [
                "Review integration middleware logs (MuleSoft/Informatica) for specific error details",
                "Check Salesforce Connected App certificate expiration and OAuth token validity",
                "If credentials expired, rotate the certificate or refresh token",
                "Re-authenticate the integration middleware with updated credentials",
                "Re-run the failed sync jobs to process the backlog of stuck records",
                "Verify data is flowing correctly between Salesforce and target systems",
                "Set up monitoring alerts for credential expiration to prevent recurrence",
            ],
        ],
    ),
    # ── 11. Browser extension conflicts with company proxy ───────────────
    Scenario(
        scenario_id="sw-browser-proxy-conflict",
        category="Software & Applications",
        priority="P3",
        assigned_team="Endpoint Engineering",
        needs_escalation=False,
        missing_information=["application_version", "device_info", "error_message"],
        subjects=[
            "Browser extension causing proxy authentication errors",
            "Chrome extensions not working behind company proxy",
            "Company proxy blocking browser extensions — can't do my work",
            "Browser proxy conflict — SSL errors on every site",
        ],
        descriptions=[
            "After the proxy configuration change last week, several Chrome extensions I use for work have stopped "
            "functioning. The Salesforce extension, LastPass, and Grammarly all throw 'ERR_TUNNEL_CONNECTION_FAILED' "
            "errors. I need these for my daily workflow — especially the Salesforce connector.",
            "I'm getting SSL certificate errors on nearly every website in Chrome. I think it's related to a browser "
            "extension conflicting with the corporate proxy. The errors started after IT pushed a new proxy PAC file. "
            "Disabling all extensions temporarily fixes it but I need them for work.",
            "My browser keeps throwing proxy authentication popups every few minutes. It seems to be triggered by "
            "certain extensions — the Bloomberg Market extension and the Zoom scheduler plugin. This never happened "
            "before the proxy change. It's extremely disruptive during trading hours.",
        ],
        next_best_actions=[
            "Review proxy PAC file configuration for extension compatibility. Check if the proxy is intercepting "
            "extension traffic and whitelist necessary domains.",
            "Identify which extensions conflict with the proxy configuration and add necessary bypass rules for "
            "extension-related domains.",
        ],
        remediation_steps=[
            [
                "Identify the specific extensions causing the conflict by testing one at a time",
                "Check the proxy PAC file for overly broad SSL inspection rules",
                "Add proxy bypass exceptions for known extension domains (e.g., extension update URLs)",
                "Verify the proxy's SSL inspection certificate is trusted in the browser's certificate store",
                "Test each required extension with the updated proxy configuration",
                "Confirm all extensions function correctly with no proxy errors",
            ],
        ],
    ),
    # ── 12. Calendar sync issues across devices ──────────────────────────
    Scenario(
        scenario_id="sw-calendar-sync-failure",
        category="Software & Applications",
        priority="P3",
        assigned_team="Enterprise Applications",
        needs_escalation=False,
        missing_information=["device_info", "affected_system", "reproduction_frequency"],
        subjects=[
            "Calendar not syncing between Outlook desktop and mobile",
            "Meeting invites missing on phone but visible in desktop Outlook",
            "Calendar sync broken — different events on different devices",
            "Outlook calendar discrepancies across laptop and iPhone",
        ],
        descriptions=[
            "My Outlook calendar on my iPhone is missing several meetings that show up fine on my desktop Outlook. I've"
            " been missing meetings because my phone doesn't show them. The calendar worked fine in sync until about a "
            "week ago. I rely on phone notifications for meeting reminders.",
            "I accepted a meeting invite on my laptop but it doesn't appear on my phone's Outlook app. This has "
            "happened with at least 5 meetings this week. Some events sync fine, others don't. I think it might be "
            "related to recurring meetings only — one-time events seem okay.",
            "My calendar is completely out of sync. My desktop Outlook shows 8 meetings today, but my phone only shows "
            "5. My iPad shows a different set altogether. I've tried removing and re-adding my account on the phone but"
            " the sync issues persist.",
        ],
        next_best_actions=[
            "Check Exchange Online mailbox sync status and device partnerships. Look for ActiveSync or Outlook mobile "
            "sync errors in Exchange admin.",
            "Review the user's mobile device partnership in Exchange Online and check for sync policy conflicts or "
            "stale device registrations.",
        ],
        remediation_steps=[
            [
                "Check Exchange Online mailbox sync status for the user's mobile devices",
                "Review ActiveSync or Outlook mobile device partnerships for errors",
                "Remove stale device partnerships from Exchange Online admin center",
                "On the mobile device, remove and re-add the Exchange account",
                "Force a full calendar re-sync on the mobile device",
                "Verify calendar events match across all devices after re-sync",
            ],
        ],
    ),
    # ── 13. Email signature not rendering correctly ──────────────────────
    Scenario(
        scenario_id="sw-email-signature-render",
        category="Software & Applications",
        priority="P4",
        assigned_team="Endpoint Engineering",
        needs_escalation=False,
        missing_information=["screenshot_or_attachment", "application_version"],
        subjects=[
            "Email signature looks broken — formatting all messed up",
            "HTML email signature not rendering properly in Outlook",
            "Company email signature shows garbled text and missing logo",
            "New corporate email signature not displaying correctly",
        ],
        descriptions=[
            "The new corporate email signature that was pushed to all employees looks completely wrong in my Outlook. "
            "The company logo is missing, the text is all in one line instead of formatted, and the social media icons "
            "are showing as broken image links. Clients have commented on it.",
            "My email signature renders fine when I view it in Outlook, but recipients tell me it looks broken — the "
            "formatting is lost and images don't load. I'm in Client Relations and this reflects poorly on the firm. "
            "Other people on my team have the same problem.",
            "After the new email signature was deployed, it looks garbled in my Outlook desktop app. The HTML "
            "formatting is not rendering — I see raw HTML tags instead of the formatted signature. The web version of "
            "Outlook shows it correctly though.",
        ],
        next_best_actions=[
            "Check the signature HTML for compatibility with Outlook's rendering engine. Verify image hosting URLs are "
            "accessible from external networks.",
            "Review the email signature template for Outlook-specific HTML/CSS compatibility issues and check image CDN"
            " accessibility.",
        ],
        remediation_steps=[
            [
                "Review the email signature HTML template for Outlook rendering compatibility",
                "Verify that all image URLs in the signature are externally accessible (not internal-only)",
                "Rebuild the signature using Outlook-compatible HTML (tables-based layout, inline CSS)",
                "Redeploy the corrected signature via the signature management tool or GPO",
                "Test by sending emails to both internal and external recipients",
                "Confirm signature renders correctly across Outlook desktop, mobile, and OWA",
            ],
        ],
    ),
    # ── 14. OneDrive sync stuck for days ─────────────────────────────────
    Scenario(
        scenario_id="sw-onedrive-sync-stuck",
        category="Software & Applications",
        priority="P3",
        assigned_team="Endpoint Engineering",
        needs_escalation=False,
        missing_information=["error_message", "device_info", "steps_to_reproduce"],
        subjects=[
            "OneDrive sync has been stuck for 3 days — files not uploading",
            "OneDrive shows 'sync pending' and won't progress",
            "OneDrive stopped syncing — stuck files, can't collaborate",
            "OneDrive sync frozen — changes not uploading to cloud",
        ],
        descriptions=[
            "My OneDrive sync has been stuck for 3 days. The icon in the taskbar shows the sync arrows spinning but "
            "nothing is actually uploading. I have about 15 files that show 'sync pending' and my colleagues can't see "
            "my latest changes. I've tried pausing and resuming sync but it didn't help.",
            "OneDrive for Business stopped syncing on Tuesday. I can see the local files but nothing is being pushed to"
            " the cloud. The OneDrive icon shows a red X. I tried signing out and back in, and unlinking my account, bu"
            "t sync gets stuck again immediately. I'm worried about data loss.",
            "My OneDrive is stuck syncing and it's causing serious collaboration issues. I edit files locally but my "
            "team sees outdated versions in SharePoint. The sync status shows several files stuck in an 'upload "
            "pending' state for days. I've run out of ideas to fix it.",
        ],
        next_best_actions=[
            "Check OneDrive sync logs for specific error codes. Look for file path length issues, unsupported "
            "characters, or file lock conflicts.",
            "Review the stuck files for invalid characters, path length limits, or permissions issues. Reset the "
            "OneDrive sync client if needed.",
        ],
        remediation_steps=[
            [
                "Check OneDrive sync status and error details via the taskbar icon",
                "Review stuck files for invalid characters, long path names, or files locked by other apps",
                "Close any applications that may have locks on the stuck files",
                "Reset the OneDrive sync client using onedrive.exe /reset",
                "If reset doesn't work, unlink and re-link the OneDrive account",
                "Verify sync completes successfully and files are up to date in the cloud",
            ],
        ],
    ),
    # ── 15. SharePoint site permissions issue ────────────────────────────
    Scenario(
        scenario_id="sw-sharepoint-permissions",
        category="Software & Applications",
        priority="P3",
        assigned_team="Enterprise Applications",
        needs_escalation=False,
        missing_information=["affected_users", "affected_system", "business_impact"],
        subjects=[
            "Can't access SharePoint site — permission denied error",
            "SharePoint team site gives 'access denied' to half the team",
            "Need SharePoint site permissions fixed — users locked out",
            "SharePoint permission issue — 403 error on departmental site",
        ],
        descriptions=[
            "About half of our Compliance team (8 people) suddenly can't access the Compliance Documents SharePoint "
            "site. They get an 'Access Denied — you don't have permission to access this resource' error. Nothing has "
            "changed with their roles. The site was working fine until this morning.",
            "I'm getting a 403 error when trying to access the Finance Quarterly Reports SharePoint site. I've been "
            "accessing it daily for months. My manager and two other colleagues report the same issue. We need these "
            "documents for the board meeting on Thursday.",
            "Our team SharePoint site seems to have had its permissions reset or changed. Several team members who prev"
            "iously had edit access now can't even view the site. We have a regulatory filing due next week and all our"
            " working documents are on this site.",
        ],
        next_best_actions=[
            "Check SharePoint site permissions and recent changes in the site settings audit log. Verify affected "
            "users' group memberships.",
            "Review the SharePoint site permissions and associated Azure AD group memberships. Check site collection "
            "admin audit log for recent permission changes.",
        ],
        remediation_steps=[
            [
                "Check the SharePoint site permissions page for recent changes",
                "Review the site collection audit log for permission modification events",
                "Verify that the affected users are still members of the correct Azure AD or SharePoint groups",
                "If group membership was accidentally changed, re-add the affected users",
                "If site permissions were modified, restore the correct permission levels",
                "Verify all affected users can access the site with appropriate permissions",
            ],
        ],
    ),
    # ── 16. Custom internal app deployment failure ───────────────────────
    Scenario(
        scenario_id="sw-custom-app-deploy-failure",
        category="Software & Applications",
        priority="P2",
        assigned_team="Enterprise Applications",
        needs_escalation=True,
        missing_information=["error_message", "environment_details", "configuration_details"],
        subjects=[
            "Internal trading app deployment failed — rollback needed",
            "Custom app deployment to production failed overnight",
            "Critical internal application deployment stuck — errors in production",
            "Failed deployment of trade settlement app — production broken",
        ],
        descriptions=[
            "The overnight deployment of our custom trade settlement application (TradeSettle v4.2) to production "
            "failed. The deployment pipeline shows errors during database migration and the app is currently showing "
            "500 errors. The previous version (v4.1) was working fine. We need to either fix the deployment or roll "
            "back — settlements start at 7 AM.",
            "Our internal portfolio management app deployment failed in production. The CI/CD pipeline completed but "
            "the application is throwing connection pool exhaustion errors. This is blocking morning portfolio "
            "rebalancing for the entire Investment Management team.",
            "Deployment of our risk calculation engine (RiskCalc v3.8) failed at the database schema migration step. "
            "The app is in a partially deployed state — some microservices are on v3.8, others still on v3.7. This "
            "inconsistency is causing data processing failures. Need immediate help to either complete the deployment "
            "or roll back cleanly.",
        ],
        next_best_actions=[
            "Review deployment logs and identify the failure point. Determine if a rollback to the previous version or "
            "a forward-fix is the safer option.",
            "Assess the current application state. Coordinate with the development team to execute either a rollback or"
            " emergency fix before business hours.",
        ],
        remediation_steps=[
            [
                "Review CI/CD pipeline logs to identify the exact failure point",
                "Check database migration logs for schema change errors",
                "Assess whether a rollback or forward-fix is safer given the current state",
                "If rolling back, execute the rollback procedure and verify previous version stability",
                "If fixing forward, apply the emergency patch and re-run failed migrations",
                "Verify all microservices are on consistent versions and communicating correctly",
                "Run smoke tests to confirm application functionality before business hours",
            ],
        ],
        channel_weights={"email": 0.15, "chat": 0.35, "portal": 0.15, "phone": 0.35},
    ),
    # ── 17. Intune compliance policy not pushing to devices ──────────────
    Scenario(
        scenario_id="sw-intune-compliance-push",
        category="Software & Applications",
        priority="P2",
        assigned_team="Endpoint Engineering",
        needs_escalation=False,
        missing_information=["device_info", "affected_users", "configuration_details"],
        subjects=[
            "Intune compliance policy not applying to new laptops",
            "Compliance policy push failing — devices showing non-compliant",
            "Intune not deploying compliance profile to enrolled devices",
            "New device enrollment not receiving compliance policies",
        ],
        descriptions=[
            "We deployed 30 new laptops last week and enrolled them in Intune, but the compliance policies aren't being"
            " applied. All 30 devices show as 'not compliant' in the Intune portal, which means Conditional Access is b"
            "locking the users from accessing email and Teams. These are for new hires starting Monday.",
            "Our latest batch of Intune-enrolled devices (about 20 Surface Pros) are not receiving the BitLocker "
            "encryption compliance policy. They show 'not evaluated' for compliance status even though they were "
            "enrolled 3 days ago. Users are being blocked by Conditional Access.",
            "Intune compliance policies stopped pushing to devices in our London office. About 50 devices are affected "
            "— they all show as non-compliant. We verified the policies are correctly assigned to the device group but "
            "they're not being evaluated. This is blocking all affected users from corporate resources.",
        ],
        next_best_actions=[
            "Check Intune policy assignment targeting and device group membership. Review the Intune compliance "
            "evaluation logs for the affected devices.",
            "Verify device enrollment status and policy assignment in Intune. Force a sync on affected devices and "
            "check for assignment filter issues.",
        ],
        remediation_steps=[
            [
                "Verify affected devices are properly enrolled and appear in the correct Intune device groups",
                "Check compliance policy assignments and ensure correct group targeting",
                "Review assignment filters for any conditions excluding the affected devices",
                "Force a device sync from the Intune portal for a sample device",
                "Check the Intune management extension logs on an affected device for errors",
                "If policy is not evaluating, re-assign the compliance policy or create a new assignment",
                "Monitor compliance status and confirm devices become compliant after fix",
            ],
        ],
    ),
    # ── 18. Bloomberg terminal showing stale data ────────────────────────
    Scenario(
        scenario_id="sw-bloomberg-stale-data",
        category="Software & Applications",
        priority="P1",
        assigned_team="Enterprise Applications",
        needs_escalation=True,
        missing_information=["affected_users", "timestamp", "network_location"],
        subjects=[
            "Bloomberg terminal showing stale market data — not updating",
            "Bloomberg data feed frozen — traders seeing old prices",
            "Real-time data not refreshing on Bloomberg terminals",
            "Bloomberg terminals across the trading floor show delayed data",
        ],
        descriptions=[
            "Multiple Bloomberg terminals on the 4th floor trading desk are showing stale market data. Prices haven't "
            "updated in over 30 minutes. Traders are making decisions based on outdated information — this is a "
            "critical risk. At least 12 terminals are affected. The Bloomberg connection status shows 'connected' but "
            "data is clearly not live.",
            "Bloomberg terminals are displaying delayed data. Equity prices are about 45 minutes behind real-time. This"
            " is affecting the entire Equities trading desk — 15 traders are impacted. We've restarted two terminals an"
            "d the issue persists. We need this fixed immediately — we're in the middle of active trading.",
            "Our Bloomberg data feed appears to be stale since about 9:30 AM. The Fixed Income desk noticed bond prices"
            " weren't moving despite active market conditions. Confirmed with Bloomberg — their service is up. The issu"
            "e seems to be on our end, possibly network or the Bloomberg B-PIPE connection.",
        ],
        next_best_actions=[
            "Check the Bloomberg B-PIPE or Data License connection. Verify network path between the trading floor and "
            "Bloomberg infrastructure. Engage Bloomberg support if the issue is on their side.",
            "Investigate the Bloomberg data feed connectivity — check B-PIPE appliance health, network switches on the "
            "trading floor, and firewall rules for Bloomberg traffic.",
        ],
        remediation_steps=[
            [
                "Check Bloomberg B-PIPE appliance or BPS server status and connectivity",
                "Verify network connectivity between trading floor and Bloomberg infrastructure",
                "Check for any recent firewall or network changes affecting Bloomberg traffic ports",
                "Restart the Bloomberg data feed service on the local distribution server",
                "If network issue, engage Network Operations to check trading floor switches",
                "Verify real-time data resumes on affected terminals",
                "Notify the trading desk once the feed is confirmed live",
            ],
        ],
        channel_weights={"email": 0.05, "chat": 0.25, "portal": 0.10, "phone": 0.60},
    ),
    # ── 19. Auto-save not working in Word ────────────────────────────────
    Scenario(
        scenario_id="sw-word-autosave-broken",
        category="Software & Applications",
        priority="P4",
        assigned_team="Endpoint Engineering",
        needs_escalation=False,
        missing_information=["application_version", "device_info"],
        subjects=[
            "AutoSave not working in Word — toggle is greyed out",
            "Word documents not auto-saving to OneDrive anymore",
            "AutoSave disabled in Word — can't turn it on",
            "Word AutoSave stopped working after update",
        ],
        descriptions=[
            "The AutoSave toggle in Word is greyed out and I can't turn it on. These are files stored on OneDrive for "
            "Business. AutoSave used to work fine until the Office update two weeks ago. I've lost work twice now "
            "because I forgot to manually save. I'm on Microsoft 365 Apps for Enterprise.",
            "Word's AutoSave feature stopped working for all my documents stored in SharePoint and OneDrive. The toggle"
            " shows as 'off' and I can't click it. I've checked and I'm signed into my Microsoft account. This is very "
            "frustrating — I lost a 2-page memo yesterday.",
            "AutoSave in Word is broken. It works in Excel and PowerPoint for the same OneDrive files but not in Word "
            "specifically. The toggle appears but is greyed out. I've tried opening files from OneDrive directly and "
            "from the local sync folder — same result.",
        ],
        next_best_actions=[
            "Check if the file format supports AutoSave (.docx required, not .doc). Verify OneDrive sync client is "
            "running and file is syncing correctly.",
            "Verify OneDrive sync status and Office version. Check for conflicting add-ins or Group Policy settings "
            "disabling AutoSave.",
        ],
        remediation_steps=[
            [
                "Verify the document is in .docx format (not .doc or compatibility mode)",
                "Check that OneDrive sync client is running and the file is fully synced",
                "Verify no Group Policy or Intune policy is disabling AutoSave",
                "Check for conflicting add-ins that may interfere with AutoSave functionality",
                "Run Office Quick Repair if settings appear correct but AutoSave still fails",
                "Test AutoSave on a new document to confirm the fix",
            ],
        ],
    ),
    # ── 20. App compatibility issue after Windows update ─────────────────
    Scenario(
        scenario_id="sw-app-compat-windows-update",
        category="Software & Applications",
        priority="P2",
        assigned_team="Endpoint Engineering",
        needs_escalation=False,
        missing_information=["error_message", "application_version", "affected_users"],
        subjects=[
            "Trading application crashing after Windows update",
            "App compatibility issue — software broken after Windows patch",
            "Windows update broke our department's critical application",
            "Application stopped working after last night's Windows update",
        ],
        descriptions=[
            "Our proprietary trading application (ContosoTrader v5.3) started crashing on launch after last night's "
            "Windows update (KB5034441). It throws a .NET runtime error and closes immediately. The entire Derivatives "
            "desk — 20 traders — is unable to use the app. We need an immediate fix or rollback of the Windows update. "
            "Trading starts at 7:30 AM.",
            "After the Windows 11 cumulative update was installed overnight, our custom risk analytics application "
            "won't start. It gives a 'side-by-side configuration is incorrect' error. At least 30 people in Risk "
            "Management are affected. This app is critical for daily position reporting.",
            "The latest Windows security patch broke compatibility with our Bloomberg API integration tool. The app "
            "launches but immediately throws a DLL versioning error. This is impacting about 15 analysts who use this "
            "tool for automated data pulls from Bloomberg. Markets open in 2 hours.",
        ],
        next_best_actions=[
            "Identify the specific Windows update causing the incompatibility. Test uninstalling the KB patch on one "
            "device. Contact the application vendor or internal dev team for a compatibility fix.",
            "Gather the error details and Windows update KB number. Evaluate whether to roll back the patch on affected"
            " machines or apply an application compatibility fix.",
        ],
        remediation_steps=[
            [
                "Identify the specific Windows update (KB number) installed on affected devices",
                "Collect the application error logs and crash dump for analysis",
                "Test uninstalling the problematic KB on one device to confirm it resolves the issue",
                "If confirmed, pause the Windows update deployment for the affected application group",
                "Uninstall the problematic KB from all affected devices via Intune or SCCM",
                "Coordinate with the application development team for a compatibility fix",
                "Re-test the Windows update with the application fix before redeploying",
            ],
        ],
    ),
    # ── 21. Zoom/WebEx plugin conflict with Teams ────────────────────────
    Scenario(
        scenario_id="sw-zoom-teams-plugin-conflict",
        category="Software & Applications",
        priority="P3",
        assigned_team="Endpoint Engineering",
        needs_escalation=False,
        missing_information=["application_version", "device_info", "steps_to_reproduce"],
        subjects=[
            "Zoom plugin causing Teams to crash during meetings",
            "Teams and Zoom conflicting — audio issues in calls",
            "WebEx and Teams plugin conflict — can't use both",
            "Zoom Outlook plugin breaking Teams meeting integration",
        ],
        descriptions=[
            "Ever since I installed the Zoom Outlook plugin for a client who uses Zoom, my Teams meetings have been pro"
            "blematic. Teams crashes about 5 minutes into every meeting, and sometimes my audio cuts out completely. Re"
            "moving the Zoom plugin fixes it but I need both — clients use Zoom, we use Teams internally.",
            "I have both Zoom and Teams installed because different clients use different platforms. The Zoom Outlook "
            "add-in seems to interfere with the Teams meeting add-in. When I schedule a Teams meeting from Outlook, it "
            "sometimes creates a Zoom meeting instead, or the meeting link is broken.",
            "After installing WebEx for a vendor partnership, my Teams meetings started having issues. Screen sharing f"
            "reezes, audio echoes, and sometimes Teams crashes entirely. I think the WebEx virtual audio/video drivers "
            "are conflicting with Teams. I need both apps to work side by side.",
        ],
        next_best_actions=[
            "Check for known conflicts between the Zoom/WebEx and Teams add-ins. Investigate virtual audio/video driver"
            " conflicts and configure them to avoid resource contention.",
            "Review Outlook COM add-in load order for conflicts. Ensure Zoom/WebEx and Teams are not competing for "
            "audio/video device access.",
        ],
        remediation_steps=[
            [
                "Identify the specific conflicting components (Outlook add-ins, virtual audio drivers, etc.)",
                "Update all conferencing applications to their latest versions",
                "If Outlook add-ins conflict, configure the load order or disable the less-used add-in",
                "For virtual audio/video driver conflicts, configure each app to use specific audio devices",
                "Set the default meeting provider in Outlook to avoid scheduling mix-ups",
                "Test both Teams and Zoom/WebEx meetings to verify they work independently",
            ],
        ],
    ),
    # ── 22. SAP GUI font rendering issue ─────────────────────────────────
    Scenario(
        scenario_id="sw-sap-gui-font-rendering",
        category="Software & Applications",
        priority="P4",
        assigned_team="Endpoint Engineering",
        needs_escalation=False,
        missing_information=["device_info", "application_version", "screenshot_or_attachment"],
        subjects=[
            "SAP GUI fonts are tiny and unreadable on my new monitor",
            "SAP GUI text rendering issue — blurry and small fonts",
            "Font display broken in SAP GUI after laptop upgrade",
            "SAP GUI scaling not working on high-DPI display",
        ],
        descriptions=[
            "After getting a new 4K monitor, the SAP GUI fonts are incredibly tiny and nearly impossible to read. All t"
            "he menu items and transaction fields are miniature. I've tried changing the font size in SAP GUI settings "
            "but it doesn't scale properly. The rest of my Windows apps scale fine — it's just SAP.",
            "SAP GUI looks terrible on my new Surface Pro — the text is blurry and the interface elements are too "
            "small. I think it's a high-DPI scaling issue. I spend 6-7 hours a day in SAP and this is giving me eye "
            "strain. My old laptop displayed it perfectly.",
            "The fonts in SAP GUI are rendering as squares and missing characters since the Windows update. Some "
            "transaction codes display correctly but others show garbled text. I've been told by a colleague that SAP "
            "GUI needs specific fonts installed. This is affecting my ability to process invoices.",
        ],
        next_best_actions=[
            "Configure SAP GUI high-DPI scaling compatibility settings. Check Windows DPI override for the SAP GUI "
            "executable.",
            "Adjust SAP GUI display settings and Windows compatibility mode for DPI scaling. Verify required SAP fonts "
            "are installed.",
        ],
        remediation_steps=[
            [
                "Check the display scaling settings in Windows for the SAP GUI application",
                "Set the DPI compatibility override on the SAP GUI executable (right-click → Properties → Compatibility"
                " → High DPI settings)",
                "Adjust the SAP GUI font settings via the SAP GUI Options dialog",
                "If fonts are missing or garbled, reinstall the SAP GUI with the SAP fonts option selected",
                "Verify the SAP GUI displays correctly at the native monitor resolution",
            ],
        ],
    ),
    Scenario(
        scenario_id="sw-power-bi-data-refresh-fail",
        category="Software & Applications",
        priority="P2",
        assigned_team="Enterprise Applications",
        needs_escalation=False,
        missing_information=["error_message", "configuration_details", "steps_to_reproduce"],
        subjects=[
            "Power BI dataset refresh failing every morning",
            "Power BI scheduled refresh errors — dataset stale",
            "Power BI reports showing yesterday's data — refresh broken",
        ],
        descriptions=[
            "Our executive dashboard in Power BI hasn't refreshed since Monday. The scheduled refresh at 6 AM is "
            "failing silently — no error email, just stale data. The C-suite is using this for morning standups and "
            "they're making decisions on 3-day-old numbers.",
            "Power BI dataset refresh for the Sales Pipeline report is failing with a gateway timeout. The data source "
            "is our on-prem SQL Server. This started after someone changed the gateway server's network configuration "
            "last week.",
        ],
        next_best_actions=[
            "Check Power BI gateway connectivity and dataset refresh history for specific error messages. Verify data "
            "source credentials are current.",
        ],
        remediation_steps=[
            [
                "Check Power BI service refresh history for specific error codes",
                "Verify on-premises data gateway is online and healthy",
                "Test data source connection from the gateway server directly",
                "Verify data source credentials haven't expired in Power BI",
                "Check gateway server network configuration for recent changes",
                "Trigger a manual refresh and monitor for errors",
            ],
        ],
        tags=["power_bi", "data_refresh"],
    ),
    Scenario(
        scenario_id="sw-sharepoint-workflow-broken",
        category="Software & Applications",
        priority="P2",
        assigned_team="Enterprise Applications",
        needs_escalation=False,
        missing_information=["steps_to_reproduce", "affected_users", "configuration_details"],
        subjects=[
            "SharePoint approval workflow stopped triggering",
            "Document approval workflow in SharePoint not firing",
            "Power Automate flow connected to SharePoint site broken",
        ],
        descriptions=[
            "The document approval workflow on our Compliance team's SharePoint site stopped working about a week ago. "
            "Documents are being uploaded but the approval flow never triggers. We have about 30 documents stuck in "
            "limbo waiting for approval. The flow was built in Power Automate and connected to a SharePoint document "
            "library.",
            "Our invoice approval workflow in SharePoint isn't firing anymore. When someone uploads an invoice PDF, it "
            "used to automatically route to the approver, but now nothing happens. Finance is manually chasing "
            "approvals which is causing payment delays.",
        ],
        next_best_actions=[
            "Check Power Automate flow run history for errors. Verify SharePoint list/library trigger is still "
            "connected and the flow owner's connection is active.",
        ],
        remediation_steps=[
            [
                "Check Power Automate flow run history for failure reasons",
                "Verify the flow's SharePoint connection is still authenticated",
                "Check if the flow owner's account was disabled or password changed",
                "Verify SharePoint site permissions haven't changed",
                "Re-authorize the flow's connections if expired",
                "Test with a manual trigger to confirm flow logic works",
            ],
        ],
        tags=["sharepoint", "workflow"],
    ),
    Scenario(
        scenario_id="sw-dynamics-crm-slow",
        category="Software & Applications",
        priority="P3",
        assigned_team="Enterprise Applications",
        needs_escalation=False,
        missing_information=["reproduction_frequency", "network_location", "affected_users"],
        subjects=[
            "Dynamics 365 CRM extremely slow for our team",
            "CRM loading times have tripled this week",
            "Dynamics CRM performance degradation",
        ],
        descriptions=[
            "Dynamics 365 CRM has been painfully slow for our Client Services team since Tuesday. Pages that used to "
            "load in 2 seconds now take 15-20 seconds. The search function is practically unusable. Other web "
            "applications work fine, so it's not a general internet issue.",
            "Our CRM is almost unusable this week. Every click takes forever to load and we keep getting timeout "
            "errors. About 20 people on our team are affected. We're in the middle of quarter-end client outreach and "
            "this is destroying our productivity.",
        ],
        next_best_actions=[
            "Check Dynamics 365 service health and performance metrics. Investigate if recent customizations or plugin "
            "changes are causing the slowdown.",
        ],
        remediation_steps=[
            [
                "Check Microsoft 365 Service Health for Dynamics 365 advisories",
                "Run a browser-based network trace to identify slow API calls",
                "Check for recently deployed plugins or workflows that may be heavy",
                "Verify server-side sync and async service aren't backlogged",
                "Clear browser cache and test in InPrivate mode",
                "If tenant-wide, open a Microsoft support ticket",
            ],
        ],
        tags=["crm", "performance"],
    ),
    Scenario(
        scenario_id="sw-intune-app-deploy-fail",
        category="Software & Applications",
        priority="P2",
        assigned_team="Endpoint Engineering",
        needs_escalation=False,
        missing_information=["device_info", "error_message", "configuration_details"],
        subjects=[
            "Intune app deployment failing for new hires",
            "Required apps not installing via Intune on new devices",
            "Company Portal shows app install failures",
        ],
        descriptions=[
            "We onboarded 12 new hires this week and their required applications (Office, Zoom, CrowdStrike, SAP GUI) a"
            "re failing to install through Intune. The Company Portal shows 'Installation failed' for most apps. These "
            "employees can't work until they have their tools.",
            "Intune managed app deployments are failing across all new Surface devices from this month's batch. Company"
            " Portal shows download errors. The apps deploy fine to older devices. Suspecting it's related to the new W"
            "indows 11 24H2 image.",
        ],
        next_best_actions=[
            "Check Intune deployment status and error codes for the failing app assignments. Verify the app packages "
            "are compatible with the device OS version.",
        ],
        remediation_steps=[
            [
                "Check Intune admin portal for deployment error codes on affected devices",
                "Verify app package compatibility with Windows 11 version on new devices",
                "Check if device compliance policies are blocking app installation",
                "Verify Intune enrollment is complete and device is properly managed",
                "Try reinstalling apps via Company Portal after clearing cache",
                "If systematic, update app packages for new OS version compatibility",
            ],
        ],
        tags=["intune", "deployment"],
    ),
    Scenario(
        scenario_id="sw-teams-recording-missing",
        category="Software & Applications",
        priority="P3",
        assigned_team="Enterprise Applications",
        needs_escalation=False,
        missing_information=["timestamp", "affected_users", "steps_to_reproduce"],
        subjects=[
            "Teams meeting recording disappeared",
            "Can't find my Teams meeting recording from last week",
            "Meeting recording not showing in chat or OneDrive",
        ],
        descriptions=[
            "I recorded a very important client meeting in Teams last Thursday and now I can't find the recording anywh"
            "ere. It's not in the meeting chat, not in my OneDrive, and not in SharePoint. The recording was about 90 m"
            "inutes long and I saw the notification that it was being processed. I need this recording for compliance p"
            "urposes.",
            "An all-hands meeting was recorded in Teams on Monday but the recording never appeared in the channel. "
            "Multiple people are asking for it. The recording started successfully and we saw the red dot, but after "
            "the meeting ended, no recording was ever available.",
        ],
        next_best_actions=[
            "Check OneDrive recycle bin and SharePoint site recycle bin for the recording. Verify Teams recording "
            "storage policy and retention settings.",
        ],
        remediation_steps=[
            [
                "Check the meeting organizer's OneDrive for Business for the recording file",
                "Check OneDrive and SharePoint recycle bins for accidentally deleted recordings",
                "Verify the Teams meeting recording policy allows recording storage",
                "Check if the recording is still processing (can take hours for long meetings)",
                "Review Stream (on SharePoint) for the recording if using legacy storage",
                "If recording is truly lost, check with Microsoft support for recovery options",
            ],
        ],
        tags=["teams", "recording"],
    ),
    Scenario(
        scenario_id="sw-copilot-not-available",
        category="Software & Applications",
        priority="P4",
        assigned_team="Enterprise Applications",
        needs_escalation=False,
        missing_information=["application_version", "business_impact"],
        subjects=[
            "Microsoft Copilot not showing up in my Office apps",
            "Where is Copilot? I was told I'd have it by now",
            "Copilot license assigned but not appearing in Word/Excel",
        ],
        descriptions=[
            "My manager said our team was getting Microsoft 365 Copilot but I don't see it anywhere in my Office apps. "
            "Word, Excel, and PowerPoint don't have the Copilot button. I checked my license in the admin portal and it"
            " shows Copilot assigned. Is there something else I need to do?",
            "I was told by our CTO that everyone in Engineering would get Copilot this month. I have the license but "
            "the Copilot icon isn't appearing in Teams or any Office app. I've restarted everything and updated to the "
            "latest version. My colleague on the same team has it working.",
        ],
        next_best_actions=[
            "Verify Copilot license assignment and check if the user is in a rollout group. Ensure Office apps are on "
            "the Current Channel with latest updates.",
        ],
        remediation_steps=[
            [
                "Verify Microsoft 365 Copilot license is properly assigned in admin center",
                "Check that Office apps are on Current Channel (not Semi-Annual)",
                "Ensure Office apps are updated to the minimum required build for Copilot",
                "Sign out and sign back into all Office applications",
                "Clear Office app credential cache and re-authenticate",
            ],
        ],
        tags=["copilot", "license"],
    ),
    Scenario(
        scenario_id="sw-email-delivery-ndr",
        category="Software & Applications",
        priority="P2",
        assigned_team="Enterprise Applications",
        needs_escalation=False,
        missing_information=["error_message", "affected_users", "reproduction_frequency"],
        subjects=[
            "Emails to external clients bouncing with NDR",
            "Getting delivery failure notifications for client emails",
            "Can't send emails to Goldman Sachs domain — all bouncing",
        ],
        descriptions=[
            "Since this morning, all emails I send to external addresses at Goldman Sachs and JPMorgan are bouncing bac"
            "k with a 550 5.7.1 delivery failure. Internal emails work fine. This is affecting at least 10 people on my"
            " team. We have critical client communications that need to go out today.",
            "I keep getting Non-Delivery Reports when sending to certain external domains. The NDR says something about"
            " 'message rejected due to content restrictions.' I'm not sending anything unusual — just standard business"
            " emails with PDF attachments.",
        ],
        next_best_actions=[
            "Check Exchange Online message trace for the bounced emails and review the specific NDR error codes. Check "
            "if outbound IP is on any blacklists.",
        ],
        remediation_steps=[
            [
                "Run Exchange Online message trace for the affected sender and recipients",
                "Review the specific NDR bounce codes for root cause identification",
                "Check if Contoso's outbound mail server IPs are on any email blacklists",
                "Verify SPF, DKIM, and DMARC records are correctly configured",
                "Check if any transport rules or DLP policies are blocking the messages",
                "If blacklisted, initiate delisting process with the blocking service",
            ],
        ],
        tags=["email", "delivery"],
    ),
    Scenario(
        scenario_id="sw-azure-devops-build-fail",
        category="Software & Applications",
        priority="P2",
        assigned_team="Enterprise Applications",
        needs_escalation=False,
        missing_information=["error_message", "steps_to_reproduce", "configuration_details"],
        subjects=[
            "Azure DevOps pipeline builds all failing since this morning",
            "CI/CD pipeline broken — all builds failing",
            "Azure Pipelines agent pool offline",
        ],
        descriptions=[
            "All of our Azure DevOps build pipelines started failing around 8 AM this morning. The builds are queuing "
            "but not picking up agents. Our self-hosted agent pool shows 0 online agents. This is blocking all "
            "deployments across 6 engineering teams.",
            "Our CI/CD pipeline in Azure DevOps is completely broken. Every build fails immediately with 'No agent pool"
            " found' error. We haven't changed any pipeline configurations. This is blocking our sprint release schedul"
            "ed for today.",
        ],
        next_best_actions=[
            "Check self-hosted agent pool health and connectivity. Verify agent VMs are running and the Azure DevOps "
            "agent service is active.",
        ],
        remediation_steps=[
            [
                "Check self-hosted agent pool status in Azure DevOps organization settings",
                "Verify agent VMs are running and accessible",
                "Check Azure DevOps agent service status on each agent machine",
                "Review agent VM network connectivity to Azure DevOps service",
                "Restart agent services and re-register if needed",
                "Consider using Microsoft-hosted agents as temporary fallback",
            ],
        ],
        tags=["devops", "cicd", "pipeline"],
    ),
    Scenario(
        scenario_id="sw-calendar-sync-cross-platform",
        category="Software & Applications",
        priority="P3",
        assigned_team="Enterprise Applications",
        needs_escalation=False,
        missing_information=["device_info", "reproduction_frequency", "application_version"],
        subjects=[
            "Calendar events not syncing between Outlook and Teams",
            "Teams showing different calendar than Outlook desktop",
            "Calendar sync broken — meetings missing from mobile",
        ],
        descriptions=[
            "My calendar is completely out of sync. Outlook desktop shows different meetings than what Teams shows, and"
            " my iPhone calendar is missing half my appointments. I've missed two meetings this week because they didn'"
            "t show up on my phone. This is really frustrating.",
            "Calendar events I create in Outlook on my laptop aren't appearing in Teams or on my mobile Outlook app. It"
            " used to sync instantly but now there's a massive delay or they never show up at all. I'm a portfolio mana"
            "ger and I rely heavily on my calendar for client meetings.",
        ],
        next_best_actions=[
            "Check Exchange Online calendar sync health. Verify all devices are connected to the same mailbox and not "
            "using cached mode with stale data.",
        ],
        remediation_steps=[
            [
                "Verify all devices are connected to the same Exchange Online mailbox",
                "Check Outlook sync status (Send/Receive tab) for errors",
                "Remove and re-add the Exchange account on mobile devices",
                "Disable and re-enable calendar sync in Teams",
                "Clear Outlook cached mode data and rebuild the OST file",
                "Verify no third-party calendar apps are conflicting",
            ],
        ],
        tags=["calendar", "sync"],
    ),
]
