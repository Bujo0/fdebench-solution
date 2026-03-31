# Copyright (c) Microsoft. All rights reserved.
"""Software & Applications scenario templates.

Covers: SAP errors, Salesforce issues, Bloomberg terminal, Microsoft 365
(Teams, Outlook, Word, Excel), internal web apps, application licensing,
software installation, app crashes, browser issues, and email problems.
"""

from ms.evals.constants import Category
from ms.evals.constants import MissingInfo
from ms.evals.constants import Priority
from ms.evals.constants import Team
from ms.evals.models import ScenarioTemplate
from ms.evals.scenarios.registry import register

register(ScenarioTemplate(
    scenario_id="sw-001",
    category=Category.SOFTWARE,
    priority=Priority.P2,
    assigned_team=Team.ENTERPRISE_APPS,
    needs_escalation=False,
    missing_information=[MissingInfo.ERROR_MESSAGE, MissingInfo.STEPS_TO_REPRODUCE],
    subjects=[
        "SAP GUI freezing during transaction processing",
        "SAP hangs every time I run a report",
        "SAP application unresponsive — can't complete transactions",
    ],
    descriptions=[
        "SAP GUI freezes for 30-60 seconds every time I try to run a financial report or post a "
        "transaction. It started yesterday afternoon. I'm using SAP GUI 7.70 on Windows 11. The "
        "Finance team has quarter-end closing this week and this is blocking our work.",
        "When I open transaction code ME21N in SAP to create a purchase order, the entire GUI locks "
        "up and I have to force-close it. This has been happening since the SAP patch last weekend. "
        "Multiple people in Procurement are affected.",
    ],
    next_best_actions=[
        "Check SAP application server health and recent patch deployment logs. Verify if the issue "
        "is affecting specific transaction codes or all SAP operations.",
    ],
    remediation_steps=[
        [
            "Check SAP application server performance metrics and recent changes",
            "Review SAP patch deployment logs from last maintenance window",
            "Test the same transactions from a different workstation to isolate the issue",
            "If server-side, engage SAP Basis team for performance analysis",
            "If client-side, clear SAP GUI cache and verify version compatibility",
        ],
    ],
))

register(ScenarioTemplate(
    scenario_id="sw-002",
    category=Category.SOFTWARE,
    priority=Priority.P3,
    assigned_team=Team.ENTERPRISE_APPS,
    needs_escalation=False,
    missing_information=[MissingInfo.ERROR_MESSAGE, MissingInfo.SCREENSHOT_OR_ATTACHMENT],
    subjects=[
        "Salesforce reports not loading — spinning wheel",
        "Can't generate reports in Salesforce since this morning",
        "Salesforce dashboard stuck on loading",
    ],
    descriptions=[
        "Salesforce reports have been failing to load all morning. I click on any report and it "
        "just shows a spinning wheel indefinitely. Dashboards are also affected. I can still "
        "navigate to individual records but any report or dashboard is broken. My team in Client "
        "Services relies on these reports for daily client outreach.",
        "None of the custom reports in Salesforce are working. Standard reports seem fine but "
        "anything our team built just shows a blank page. This might be related to the Salesforce "
        "release update that happened over the weekend.",
    ],
    next_best_actions=[
        "Check Salesforce system status page for known issues. Review recent release update impact "
        "on custom report configurations.",
    ],
    remediation_steps=[
        [
            "Check Salesforce Trust status page for service degradation",
            "Verify if the issue affects standard reports or only custom reports",
            "Review recent Salesforce release notes for reporting changes",
            "Test reports in a Salesforce sandbox environment",
            "If custom report specific, check report type and field permissions",
        ],
    ],
))

register(ScenarioTemplate(
    scenario_id="sw-003",
    category=Category.SOFTWARE,
    priority=Priority.P1,
    assigned_team=Team.ENTERPRISE_APPS,
    needs_escalation=True,
    missing_information=[],
    subjects=[
        "Bloomberg terminal showing stale data — trades not updating",
        "CRITICAL: Bloomberg pricing feed frozen for 20+ minutes",
        "Bloomberg Terminal data lag — trading desk impacted",
    ],
    descriptions=[
        "Bloomberg Terminal on the NYC trading floor is showing stale market data. Prices haven't "
        "updated in over 20 minutes. The traders noticed when their execution prices diverged from "
        "what Bloomberg was showing. This is a live trading issue — we're exposed to price risk on "
        "open positions. Affects 8 terminals on Floor 5.",
        "All Bloomberg terminals in the Institutional Trading department are displaying frozen "
        "data feeds. Last update timestamp shows 09:42 but it's now 10:15. We've tried restarting "
        "individual terminals but the data feed itself appears stale. Multiple traders can't "
        "execute orders accurately.",
    ],
    next_best_actions=[
        "Immediately engage Bloomberg support and check network connectivity to Bloomberg data "
        "feed servers. This is revenue-critical — trading desk cannot operate with stale pricing.",
    ],
    remediation_steps=[
        [
            "Contact Bloomberg support hotline for data feed status",
            "Check network connectivity between trading floor and Bloomberg data feed endpoints",
            "Verify Bloomberg server-side service health",
            "If network issue, check firewall rules and proxy configuration for Bloomberg traffic",
            "If Bloomberg service issue, implement alternative data feed for critical trading",
            "Communicate status to trading desk management every 15 minutes",
        ],
    ],
))

register(ScenarioTemplate(
    scenario_id="sw-004",
    category=Category.SOFTWARE,
    priority=Priority.P3,
    assigned_team=Team.ENDPOINT,
    needs_escalation=False,
    missing_information=[MissingInfo.DEVICE_INFO, MissingInfo.APPLICATION_VERSION],
    subjects=[
        "Teams crashes on launch after the latest update",
        "Microsoft Teams keeps crashing — can't join meetings",
        "Teams white screen then closes immediately",
    ],
    descriptions=[
        "Since the Teams update that was pushed yesterday, the app shows a white screen for about "
        "5 seconds then crashes. I've tried reinstalling it twice. I can still use Teams in the "
        "browser but the desktop app won't work. I have client meetings all afternoon.",
        "Teams crashes every time I try to launch it. I get a brief flash of the loading screen "
        "then it closes. Event Viewer shows an application error in ms-teams.exe. This started "
        "after the auto-update last night.",
    ],
    next_best_actions=[
        "Clear Teams cache, verify app version, and check for known issues with the latest update. "
        "Suggest using Teams web as a workaround while the desktop app is being fixed.",
    ],
    remediation_steps=[
        [
            "Clear Teams application cache folder",
            "Verify Teams version matches the latest stable release",
            "Check Windows Event Viewer for specific crash details",
            "Uninstall and perform a clean reinstall of Teams",
            "If issue persists, check for known bugs in the latest Teams update",
        ],
    ],
))

register(ScenarioTemplate(
    scenario_id="sw-005",
    category=Category.SOFTWARE,
    priority=Priority.P3,
    assigned_team=Team.ENDPOINT,
    needs_escalation=False,
    missing_information=[MissingInfo.DEVICE_INFO, MissingInfo.ENVIRONMENT_DETAILS],
    subjects=[
        "Outlook calendar sync broken — showing old appointments",
        "Calendar not updating in Outlook desktop app",
        "Outlook shows meetings I deleted months ago",
    ],
    descriptions=[
        "My Outlook desktop calendar is showing meetings from months ago that I deleted. New "
        "meeting invites sometimes appear, sometimes don't. Outlook Web shows the correct "
        "calendar. This started after I got a new laptop last week — might be a profile migration "
        "issue.",
        "Calendar sync seems broken between Outlook desktop and Exchange. I created a meeting "
        "yesterday and my colleague says they never received the invite. But Outlook shows it as "
        "sent. My calendar has duplicate entries and missing entries.",
    ],
    next_best_actions=[
        "Rebuild the Outlook profile and verify Exchange connectivity. Check for OST file "
        "corruption from the recent laptop migration.",
    ],
    remediation_steps=[
        [
            "Check Outlook connectivity status in the system tray",
            "Verify Exchange Online mailbox health in admin portal",
            "Delete and recreate the Outlook profile to force fresh sync",
            "If OST file is corrupt, delete it and allow Outlook to rebuild",
            "Verify calendar sync is working by creating a test appointment",
        ],
    ],
))

register(ScenarioTemplate(
    scenario_id="sw-006",
    category=Category.SOFTWARE,
    priority=Priority.P2,
    assigned_team=Team.ENTERPRISE_APPS,
    needs_escalation=False,
    missing_information=[MissingInfo.CONFIGURATION_DETAILS],
    subjects=[
        "Excel macro security policy blocking critical business macro",
        "Can't run VBA macros in Excel — blocked by policy",
        "Excel macro disabled — breaking our trading reconciliation",
    ],
    descriptions=[
        "Our daily trading reconciliation spreadsheet uses VBA macros that were working fine until "
        "this morning. Now Excel shows 'Macros have been disabled' and there's no option to enable "
        "them. This macro is critical — it reconciles about $50M in daily trades and the Finance "
        "team needs results by 2pm.",
        "The macro security policy was changed and now none of our business-critical Excel macros "
        "work. These are signed macros that have been approved for years. Affects the entire "
        "Risk Management team.",
    ],
    next_best_actions=[
        "Review recent Group Policy changes affecting macro security settings. Verify the macro "
        "signing certificate is still trusted. Create an exception for business-critical macros.",
    ],
    remediation_steps=[
        [
            "Check Group Policy for recent changes to Office macro security settings",
            "Verify the code signing certificate for the macros is valid and trusted",
            "If policy was changed, coordinate with Security to create approved exception",
            "Add the file location to Trusted Locations as interim measure",
            "Test macro execution after policy adjustment",
            "Communicate resolution to affected teams",
        ],
    ],
))

register(ScenarioTemplate(
    scenario_id="sw-007",
    category=Category.SOFTWARE,
    priority=Priority.P4,
    assigned_team=Team.ENDPOINT,
    needs_escalation=False,
    missing_information=[MissingInfo.BUSINESS_IMPACT, MissingInfo.APPLICATION_VERSION],
    subjects=[
        "Software installation request — Python 3.12",
        "Need Python installed on my work laptop",
        "Request: install development tools (Python, VS Code)",
    ],
    descriptions=[
        "I need Python 3.12 installed on my work laptop for data analysis work. The Software "
        "Center doesn't have it available. I'm in the Data Science team and this is a standard "
        "tool for our work. No rush — I can use Jupyter notebooks in the cloud for now.",
        "Requesting installation of Python 3.12 and Visual Studio Code. These are standard "
        "development tools I need for my engineering work. Both should be on the approved "
        "software list. My current laptop doesn't have either.",
    ],
    next_best_actions=[
        "Verify Python 3.12 is on the approved software list and deploy via Intune or Software "
        "Center. If not approved, initiate software approval request.",
    ],
    remediation_steps=[
        [
            "Verify the requested software is on the approved list",
            "If approved, deploy via Intune or Software Center",
            "If not approved, submit software approval request with business justification",
            "Confirm installation and functionality with the user",
        ],
    ],
))

register(ScenarioTemplate(
    scenario_id="sw-008",
    category=Category.SOFTWARE,
    priority=Priority.P3,
    assigned_team=Team.ENDPOINT,
    needs_escalation=False,
    missing_information=[MissingInfo.ERROR_MESSAGE, MissingInfo.DEVICE_INFO],
    subjects=[
        "Browser crashing when opening internal portal",
        "Edge keeps crashing on our intranet site",
        "Chrome freezes every time I access the internal dashboard",
    ],
    descriptions=[
        "Microsoft Edge crashes every time I try to open the internal IT portal at "
        "portal.contoso.com. It loads partially, then the tab crashes with 'Aw, Snap!' error. "
        "I've cleared the cache and disabled extensions. Chrome works fine for the same site.",
        "Our internal expense reporting portal crashes Chrome every time I try to submit a report. "
        "The page freezes, then the browser becomes unresponsive. This only happens on this "
        "specific portal — other websites work fine.",
    ],
    next_best_actions=[
        "Check browser compatibility with the internal portal. Verify browser version and "
        "extensions. Test in InPrivate mode to isolate the issue.",
    ],
    remediation_steps=[
        [
            "Test the portal in InPrivate/Incognito mode to rule out extension conflicts",
            "Verify browser version is current and compatible with the portal requirements",
            "Clear browser cache, cookies, and site data for the portal domain",
            "Disable hardware acceleration in browser settings",
            "If issue persists, try an alternative browser and report to portal team",
        ],
    ],
))

register(ScenarioTemplate(
    scenario_id="sw-009",
    category=Category.SOFTWARE,
    priority=Priority.P2,
    assigned_team=Team.ENTERPRISE_APPS,
    needs_escalation=False,
    missing_information=[MissingInfo.TIMESTAMP, MissingInfo.ERROR_MESSAGE],
    subjects=[
        "Outlook not receiving external emails",
        "External emails not arriving — internal email works fine",
        "Missing emails from clients — not in spam folder either",
    ],
    descriptions=[
        "I've stopped receiving emails from external senders. Internal emails arrive fine. I "
        "checked my Junk folder — nothing there either. A client confirmed they sent me 3 emails "
        "today that I never received. No bounce-back on their end. This is critical — I'm missing "
        "trade confirmations from our counterparties.",
        "External emails haven't been arriving for the past few hours. I know because a vendor "
        "called to ask why I didn't reply to their urgent email. My internal email works perfectly. "
        "Nothing in Junk, nothing in Quarantine that I can see.",
    ],
    next_best_actions=[
        "Check Exchange Online mail flow rules and message trace for the missing emails. Verify "
        "there are no transport rules blocking external delivery.",
    ],
    remediation_steps=[
        [
            "Run message trace in Exchange admin center for the user's mailbox",
            "Check mail flow rules and transport rules for blocking conditions",
            "Verify anti-spam/anti-malware quarantine for false positives",
            "Check Exchange Online Protection logs for delivery status",
            "If systemic, check MX records and mail routing configuration",
        ],
    ],
))

register(ScenarioTemplate(
    scenario_id="sw-010",
    category=Category.SOFTWARE,
    priority=Priority.P2,
    assigned_team=Team.ENTERPRISE_APPS,
    needs_escalation=False,
    missing_information=[MissingInfo.AFFECTED_USERS],
    subjects=[
        "M365 license expired — lost access to all Office apps",
        "Microsoft 365 apps deactivated — 'Your subscription has expired'",
        "Office apps showing 'Unlicensed Product' banner",
    ],
    descriptions=[
        "All my Microsoft 365 apps are showing 'Unlicensed Product' and I can't edit any "
        "documents. Word, Excel, PowerPoint, and Outlook all have the red banner. I was working "
        "fine yesterday. I have a quarterly report due to the board tomorrow that I can't finish.",
        "My M365 license seems to have been removed. All Office apps went into read-only mode "
        "this morning. I can view documents but can't edit or save anything. Outlook is still "
        "receiving emails but I can't compose new ones.",
    ],
    next_best_actions=[
        "Check user's license assignment in M365 admin center. Verify no recent license "
        "reclamation or group-based licensing changes affected the user.",
    ],
    remediation_steps=[
        [
            "Check user's license assignments in M365 admin center",
            "Verify group-based licensing hasn't removed the user's license",
            "If license was revoked, identify the cause and reassign",
            "Have user sign out and sign back in to refresh license status",
            "Verify all Office apps activate successfully",
        ],
    ],
))

register(ScenarioTemplate(
    scenario_id="sw-011",
    category=Category.SOFTWARE,
    priority=Priority.P3,
    assigned_team=Team.ENTERPRISE_APPS,
    needs_escalation=False,
    missing_information=[MissingInfo.ERROR_MESSAGE, MissingInfo.CONFIGURATION_DETAILS],
    subjects=[
        "Power BI dashboard not refreshing — data is 3 days old",
        "Power BI scheduled refresh failing",
        "Executive dashboard showing stale data in Power BI",
    ],
    descriptions=[
        "Our executive KPI dashboard in Power BI hasn't refreshed since Friday. It's supposed to "
        "refresh daily at 6am. The dashboard shows 'Last refresh: March 28' but it's now March 31. "
        "The executive team relies on this for the Monday morning meeting.",
        "The Power BI dataset for our client analytics report is failing to refresh. I see a "
        "'credentials expired' error in the refresh history. This dataset connects to our Azure "
        "SQL database and was working until the database credentials were rotated last week.",
    ],
    next_best_actions=[
        "Check Power BI scheduled refresh history and update data source credentials if they "
        "were recently rotated.",
    ],
    remediation_steps=[
        [
            "Check Power BI Service for scheduled refresh error details",
            "Verify data source credentials are current after recent rotation",
            "Update gateway data source credentials if needed",
            "Trigger manual refresh and verify data freshness",
            "Confirm scheduled refresh resumes on next cycle",
        ],
    ],
))

register(ScenarioTemplate(
    scenario_id="sw-012",
    category=Category.SOFTWARE,
    priority=Priority.P3,
    assigned_team=Team.ENDPOINT,
    needs_escalation=False,
    missing_information=[MissingInfo.APPLICATION_VERSION, MissingInfo.DEVICE_INFO],
    subjects=[
        "Adobe Acrobat can't open encrypted PDFs from clients",
        "PDF documents showing 'This document is protected' error",
        "Can't view password-protected PDF files in Acrobat",
    ],
    descriptions=[
        "When I try to open encrypted PDF documents sent by our clients, Adobe Acrobat shows "
        "'This document cannot be opened with your current security settings.' I receive these "
        "PDFs daily as part of contract reviews. This started after the security policy update.",
        "Adobe Acrobat Reader can't open any PDF that has password protection or encryption. It "
        "worked fine until last week. I get an error about 'insufficient permissions' even though "
        "I have the correct passwords. Other people on my team have the same problem.",
    ],
    next_best_actions=[
        "Check recent security policy changes affecting PDF handling. Verify Adobe Acrobat version "
        "and security settings.",
    ],
    remediation_steps=[
        [
            "Check recent Group Policy changes for PDF security settings",
            "Verify Adobe Acrobat version is current",
            "Review Enhanced Security settings in Acrobat preferences",
            "Add trusted domains or certificates if policy requires it",
            "Test opening a sample encrypted PDF after adjustments",
        ],
    ],
))

register(ScenarioTemplate(
    scenario_id="sw-013",
    category=Category.SOFTWARE,
    priority=Priority.P2,
    assigned_team=Team.ENTERPRISE_APPS,
    needs_escalation=False,
    missing_information=[MissingInfo.ERROR_MESSAGE, MissingInfo.AFFECTED_USERS],
    subjects=[
        "Internal web app showing 502 Bad Gateway errors",
        "Client portal returning 502 errors intermittently",
        "Internal CRM tool unreachable — 502 errors",
    ],
    descriptions=[
        "Our internal client management portal at crm.contoso.com is returning 502 Bad Gateway "
        "errors intermittently. It works sometimes if you refresh a few times but it's unreliable. "
        "The Client Services team uses this all day and they're unable to log client interactions.",
        "The internal reporting tool at reports.contoso.com is showing 502 errors. I've tried "
        "different browsers and from different machines. Seems to be a server-side issue. The app "
        "team deployed an update last night — might be related.",
    ],
    next_best_actions=[
        "Check application server health and recent deployment logs. A recent update may have "
        "introduced instability.",
    ],
    remediation_steps=[
        [
            "Check application server health and resource utilization",
            "Review recent deployment logs for configuration changes",
            "Check reverse proxy / load balancer logs for upstream errors",
            "If recent deployment caused the issue, coordinate rollback with app team",
            "Monitor application stability after remediation",
        ],
    ],
))

register(ScenarioTemplate(
    scenario_id="sw-014",
    category=Category.SOFTWARE,
    priority=Priority.P2,
    assigned_team=Team.ENTERPRISE_APPS,
    needs_escalation=False,
    missing_information=[MissingInfo.DEVICE_INFO, MissingInfo.NETWORK_LOCATION],
    subjects=[
        "Teams screen sharing not working — black screen for attendees",
        "Can't share my screen in Teams meetings — participants see nothing",
        "Screen sharing shows black rectangle in Teams calls",
    ],
    descriptions=[
        "When I try to share my screen in Teams meetings, attendees see a black rectangle instead "
        "of my screen. I can see the sharing indicator on my end but nobody else can see the "
        "content. This is happening in every meeting. I have a client demo in 2 hours.",
        "Screen sharing in Teams is broken for me. I can share but participants see a completely "
        "black screen. Audio and video work fine. I've tried sharing the whole screen and "
        "individual windows — same result. Reinstalled Teams, still broken.",
    ],
    next_best_actions=[
        "Check GPU driver compatibility with Teams screen sharing. Verify hardware acceleration "
        "settings and try disabling GPU hardware acceleration in Teams.",
    ],
    remediation_steps=[
        [
            "Disable GPU hardware acceleration in Teams settings",
            "Update GPU drivers to the latest version",
            "Check if screen sharing works in Teams web client as a workaround",
            "Verify screen recording permissions in Windows privacy settings",
            "If issue persists, check for known Teams bugs with the GPU model",
        ],
    ],
))

register(ScenarioTemplate(
    scenario_id="sw-015",
    category=Category.SOFTWARE,
    priority=Priority.P2,
    assigned_team=Team.ENTERPRISE_APPS,
    needs_escalation=False,
    missing_information=[MissingInfo.ERROR_MESSAGE, MissingInfo.ENVIRONMENT_DETAILS],
    subjects=[
        "Citrix session disconnecting every 30 minutes",
        "Remote desktop via Citrix keeps timing out",
        "Citrix Workspace kicks me out repeatedly",
    ],
    descriptions=[
        "My Citrix virtual desktop session disconnects exactly every 30 minutes. I have to log "
        "back in and everything I was working on is lost if I didn't save. This started after the "
        "Citrix policy update on Friday. I'm working remotely and this is my only way to access "
        "the trading applications.",
        "Citrix Workspace app keeps disconnecting my session. It happens at random intervals, "
        "sometimes after 20 minutes, sometimes after an hour. When it reconnects, my session is "
        "still there but any unsaved work in the apps is gone.",
    ],
    next_best_actions=[
        "Review recent Citrix session timeout policy changes. Check Citrix Director for session "
        "disconnect patterns and server health.",
    ],
    remediation_steps=[
        [
            "Check Citrix Director for session disconnect reason codes",
            "Review recent Citrix policy changes for session timeout settings",
            "Verify network stability between user and Citrix infrastructure",
            "Check Citrix server resource utilization for overload",
            "If policy change caused the issue, adjust timeout settings",
        ],
    ],
))

register(ScenarioTemplate(
    scenario_id="sw-016",
    category=Category.SOFTWARE,
    priority=Priority.P2,
    assigned_team=Team.ENDPOINT,
    needs_escalation=False,
    missing_information=[MissingInfo.APPLICATION_VERSION, MissingInfo.AFFECTED_USERS],
    subjects=[
        "Application auto-update broke compatibility with our workflow",
        "Chrome auto-update breaking internal web apps",
        "Software update killed our internal tool compatibility",
    ],
    descriptions=[
        "Chrome auto-updated to version 124 last night and now our internal client management "
        "portal doesn't work. The app uses features that Chrome 124 apparently deprecated. We "
        "need to either roll back Chrome or get the app team to fix compatibility. About 30 people "
        "in Client Services are affected.",
        "The latest Windows update automatically updated Edge and now our internal compliance "
        "reporting tool shows rendering errors. Forms don't display correctly and we can't submit "
        "reports. The compliance deadline is this Friday.",
    ],
    next_best_actions=[
        "Identify the breaking change in the auto-update and coordinate between browser team and "
        "application team for a fix or rollback.",
    ],
    remediation_steps=[
        [
            "Identify the specific browser version and breaking change",
            "Test the internal app with the previous browser version for confirmation",
            "If possible, roll back the browser update via Intune policy",
            "Coordinate with application team to fix compatibility",
            "Configure auto-update policy to pause future updates until tested",
        ],
    ],
))

register(ScenarioTemplate(
    scenario_id="sw-017",
    category=Category.SOFTWARE,
    priority=Priority.P3,
    assigned_team=Team.ENTERPRISE_APPS,
    needs_escalation=False,
    missing_information=[MissingInfo.ERROR_MESSAGE, MissingInfo.CONFIGURATION_DETAILS],
    subjects=[
        "DocuSign integration failing with API errors",
        "Can't send documents for signature via DocuSign",
        "DocuSign connector returning authentication errors",
    ],
    descriptions=[
        "Our DocuSign integration in the contract management system stopped working. When I try "
        "to send a document for signature, I get an 'API Authentication Failed' error. This is "
        "blocking contract execution for the M&A team — we have 3 deals waiting for signatures.",
        "DocuSign isn't working from our internal system. The integration was fine last week but "
        "now every signature request fails with a timeout error. I can still log into DocuSign "
        "directly and send documents from there, so it seems like an integration issue.",
    ],
    next_best_actions=[
        "Check DocuSign API credentials and integration configuration. The API key or OAuth "
        "token may have expired.",
    ],
    remediation_steps=[
        [
            "Check DocuSign API credentials for expiration",
            "Verify OAuth token refresh is functioning correctly",
            "Review DocuSign API rate limits for throttling",
            "Test API connectivity from the integration server",
            "If credentials expired, rotate and update in the integration config",
        ],
    ],
))

register(ScenarioTemplate(
    scenario_id="sw-018",
    category=Category.SOFTWARE,
    priority=Priority.P2,
    assigned_team=Team.ENDPOINT,
    needs_escalation=False,
    missing_information=[MissingInfo.DEVICE_INFO, MissingInfo.STEPS_TO_REPRODUCE],
    subjects=[
        "Word documents corrupted when saving to network drive",
        "Files getting corrupted on save — losing work",
        "Document corruption when saving to shared folder",
    ],
    descriptions=[
        "I've lost work twice today because Word documents are getting corrupted when I save to "
        "the \\\\fs01\\legal-docs network share. The file saves but when I reopen it, Word says "
        "'The file is corrupt and cannot be opened.' I have a 40-page legal brief that I've been "
        "working on for a week and I'm terrified of losing it.",
        "Excel and Word files saved to the Finance shared drive are getting corrupted. Multiple "
        "people in the Finance department are affected. Saving locally works fine. This only "
        "happens with the network drive. We've lost several important documents already.",
    ],
    next_best_actions=[
        "Check network share health and connectivity. Verify SMB protocol version and test file "
        "operations from multiple clients.",
    ],
    remediation_steps=[
        [
            "Recover the corrupted files from backup or shadow copies",
            "Check file server health and disk integrity",
            "Verify SMB signing and protocol version compatibility",
            "Test saving files of various sizes from multiple machines",
            "If file server issue, check event logs for disk or network errors",
            "Recommend saving locally and syncing as interim workaround",
        ],
    ],
))

register(ScenarioTemplate(
    scenario_id="sw-019",
    category=Category.SOFTWARE,
    priority=Priority.P4,
    assigned_team=Team.ENDPOINT,
    needs_escalation=False,
    missing_information=[MissingInfo.CONFIGURATION_DETAILS, MissingInfo.STEPS_TO_REPRODUCE],
    subjects=[
        "Outlook rules not processing automatically",
        "Email rules stopped working in Outlook",
        "Auto-sort rules in Outlook not firing anymore",
    ],
    descriptions=[
        "My Outlook rules that auto-sort emails into folders stopped working. I have about 15 "
        "rules set up to organize emails from different clients into project folders. They were "
        "working fine until the Office update last week. Now I have to manually sort everything.",
        "The inbox rules I set up in Outlook aren't running automatically. Emails just pile up "
        "in my inbox instead of going to their assigned folders. If I run rules manually they "
        "work, but they don't trigger automatically on new mail.",
    ],
    next_best_actions=[
        "Check Outlook rules for client-only vs server-side configuration. Verify rules haven't "
        "been disabled by the recent Office update.",
    ],
    remediation_steps=[
        [
            "Check Outlook rules list for disabled or broken rules",
            "Verify rules are set as server-side (not client-only) for automatic processing",
            "Delete and recreate rules if they were corrupted by the update",
            "Check mailbox size limits that might be preventing rule execution",
        ],
    ],
))

register(ScenarioTemplate(
    scenario_id="sw-020",
    category=Category.SOFTWARE,
    priority=Priority.P3,
    assigned_team=Team.ENTERPRISE_APPS,
    needs_escalation=False,
    missing_information=[MissingInfo.ERROR_MESSAGE, MissingInfo.ENVIRONMENT_DETAILS],
    subjects=[
        "Azure DevOps pipeline build failures since this morning",
        "CI/CD pipeline broken — all builds failing",
        "Azure DevOps builds timing out on every commit",
    ],
    descriptions=[
        "All our Azure DevOps CI/CD pipelines started failing this morning. The build agents are "
        "timing out after 60 minutes and the queue is backed up. We have 20+ developers who can't "
        "deploy code. The self-hosted build agents might need attention.",
        "Our build pipeline in Azure DevOps is broken. Every commit triggers a build that fails "
        "with 'Agent offline' error. We use self-hosted agents running on Azure VMs. They might "
        "have gone down during last night's maintenance window.",
    ],
    next_best_actions=[
        "Check self-hosted build agent VM health and connectivity. Verify agent services are "
        "running and can communicate with Azure DevOps.",
    ],
    remediation_steps=[
        [
            "Check Azure VM health for self-hosted build agents",
            "Verify Azure DevOps agent service is running on each build VM",
            "Review agent pool status in Azure DevOps for offline agents",
            "Restart agent services and verify agent registration",
            "Clear the build queue backlog once agents are restored",
        ],
    ],
))

register(ScenarioTemplate(
    scenario_id="sw-021",
    category=Category.SOFTWARE,
    priority=Priority.P3,
    assigned_team=Team.ENDPOINT,
    needs_escalation=False,
    missing_information=[MissingInfo.APPLICATION_VERSION, MissingInfo.BUSINESS_IMPACT],
    subjects=[
        "Application requesting elevated permissions — UAC popup",
        "Software needs admin rights to run — can't use it",
        "UAC prompt blocks application that used to work",
    ],
    descriptions=[
        "An application I use daily for financial modeling is now requesting admin permissions "
        "every time I launch it. It used to work fine without UAC prompts. I don't have admin "
        "rights on my laptop. This started after the Intune policy update.",
        "My statistical analysis software (R Studio) now shows a UAC prompt requiring admin "
        "access. I can't proceed because I don't have local admin. This tool is essential for "
        "my daily quantitative analysis work.",
    ],
    next_best_actions=[
        "Check recent Intune or Group Policy changes that may have changed UAC behavior. "
        "Consider adding an exception for the specific application.",
    ],
    remediation_steps=[
        [
            "Identify the specific Intune or GPO change affecting UAC behavior",
            "Check if the application was recently updated and now requires elevated permissions",
            "Create an Intune policy exception for the specific application if appropriate",
            "Test running the application after policy adjustment",
        ],
    ],
))

register(ScenarioTemplate(
    scenario_id="sw-022",
    category=Category.SOFTWARE,
    priority=Priority.P3,
    assigned_team=Team.ENDPOINT,
    needs_escalation=False,
    missing_information=[MissingInfo.DEVICE_INFO, MissingInfo.APPLICATION_VERSION],
    subjects=[
        "Calendar invites not syncing between Teams and Outlook",
        "Teams meetings don't show up in my Outlook calendar",
        "Calendar discrepancy between Teams and Outlook",
    ],
    descriptions=[
        "When colleagues schedule Teams meetings, they appear in my Teams calendar but not in "
        "Outlook. I missed two meetings today because I only check my Outlook calendar. My "
        "Outlook calendar used to show all Teams meetings automatically.",
        "I created a Teams meeting yesterday but none of the invitees got Outlook calendar "
        "entries. They only see it if they open Teams. This used to sync perfectly. Outlook "
        "and Teams are clearly out of sync.",
    ],
    next_best_actions=[
        "Check Outlook-Teams calendar sync settings and verify Exchange Online connectivity. "
        "May need to reset the calendar sync configuration.",
    ],
    remediation_steps=[
        [
            "Verify Exchange Online mailbox calendar health",
            "Check Teams calendar sync settings and permissions",
            "Clear Teams cache and restart the application",
            "Verify the user's M365 license includes Exchange Online",
            "If issue persists, re-link the Teams calendar to Exchange",
        ],
    ],
))

register(ScenarioTemplate(
    scenario_id="sw-023",
    category=Category.SOFTWARE,
    priority=Priority.P1,
    assigned_team=Team.ENTERPRISE_APPS,
    needs_escalation=True,
    missing_information=[],
    subjects=[
        "SAP license count exceeded — users getting kicked out",
        "CRITICAL: SAP concurrent user limit reached — blocking operations",
        "SAP system refusing new logins — license exhaustion",
    ],
    descriptions=[
        "SAP is refusing new logins with 'Maximum number of named users exceeded' error. We have "
        "50 concurrent users trying to access the system but our license only covers 45. This is "
        "month-end closing and the entire Finance and Accounting teams need SAP access right now. "
        "Revenue recognition is blocked.",
        "SAP ERP is at license capacity. Users across Finance, Procurement, and Operations are "
        "being randomly kicked out when someone else logs in. This is causing data entry errors "
        "and lost work. We're in the middle of quarterly close.",
    ],
    next_best_actions=[
        "Immediately identify and terminate idle SAP sessions to free up licenses. Initiate "
        "emergency license procurement for additional concurrent users.",
    ],
    remediation_steps=[
        [
            "Identify and terminate idle or stale SAP sessions",
            "Check for service accounts consuming user licenses unnecessarily",
            "Initiate emergency license procurement or temporary expansion",
            "Implement session timeout policy to auto-close idle sessions",
            "Communicate capacity constraints to affected departments",
            "Plan permanent license count increase for next billing cycle",
        ],
    ],
))

register(ScenarioTemplate(
    scenario_id="sw-024",
    category=Category.SOFTWARE,
    priority=Priority.P4,
    assigned_team=Team.ENDPOINT,
    needs_escalation=False,
    missing_information=[MissingInfo.DEVICE_INFO, MissingInfo.REPRODUCTION_FREQUENCY],
    subjects=[
        "Visio crashes when opening large network diagrams",
        "Microsoft Visio very slow with complex diagrams",
        "Visio out of memory error on infrastructure diagrams",
    ],
    descriptions=[
        "Microsoft Visio crashes or runs out of memory when I try to open our network "
        "infrastructure diagram. The file is about 50MB with hundreds of shapes. Visio "
        "works fine for smaller files. Not urgent — I can export sections as images for now.",
        "Visio is extremely slow and eventually crashes when I work on our data center layout "
        "diagram. I think the file has just gotten too large. Is there a way to optimize it or "
        "increase the memory allocation?",
    ],
    next_best_actions=[
        "Check Visio memory allocation settings and system RAM. Consider breaking the large "
        "diagram into linked sub-diagrams.",
    ],
    remediation_steps=[
        [
            "Check available system RAM and Visio memory usage",
            "Verify Visio is the latest version with all patches",
            "Recommend splitting the large diagram into linked sub-diagrams",
            "Increase virtual memory allocation if system is constrained",
        ],
    ],
))

register(ScenarioTemplate(
    scenario_id="sw-025",
    category=Category.SOFTWARE,
    priority=Priority.P1,
    assigned_team=Team.ENTERPRISE_APPS,
    needs_escalation=True,
    missing_information=[],
    subjects=[
        "Internal trading platform showing wrong prices",
        "CRITICAL: Price display error on trading application",
        "Trading system displaying incorrect market data",
    ],
    descriptions=[
        "Our internal trading platform is displaying incorrect bid/ask prices. The prices shown "
        "diverge from Bloomberg and Reuters by up to 2%. We discovered this when a trader noticed "
        "a trade executed at a price significantly different from what was displayed. This is a "
        "potential regulatory issue — we need to halt trading on this platform immediately.",
        "The price feed in our custom trading application is showing wrong values. Multiple "
        "traders have confirmed that the prices don't match other data sources. We've already "
        "executed several trades that may be at incorrect prices. Compliance has been notified.",
    ],
    next_best_actions=[
        "Immediately halt trading on the affected platform. Investigate the price feed integration "
        "and coordinate with Compliance on potentially erroneous trades.",
    ],
    remediation_steps=[
        [
            "Halt all trading activity on the affected platform immediately",
            "Identify the root cause of price feed discrepancy",
            "Compare executed trades against correct market prices",
            "Notify Compliance team of potentially erroneous trade executions",
            "Fix the price feed integration and verify data accuracy",
            "Resume trading only after thorough validation",
        ],
    ],
))

register(ScenarioTemplate(
    scenario_id="sw-026",
    category=Category.SOFTWARE,
    priority=Priority.P3,
    assigned_team=Team.ENDPOINT,
    needs_escalation=False,
    missing_information=[MissingInfo.DEVICE_INFO, MissingInfo.REPRODUCTION_FREQUENCY],
    subjects=[
        "OneNote sync conflict losing my meeting notes",
        "OneNote showing sync errors — notes disappearing",
        "OneNote sections not syncing between devices",
    ],
    descriptions=[
        "OneNote keeps showing sync conflicts between my laptop and tablet. Some of my meeting "
        "notes from this week have disappeared or been replaced with older versions. I use "
        "OneNote for all my client meeting notes and I'm worried about data loss.",
        "My OneNote notebooks aren't syncing properly. I have notes on my laptop that don't "
        "appear on my phone, and vice versa. The sync icon shows a constant error. I've tried "
        "closing and reopening but it doesn't help.",
    ],
    next_best_actions=[
        "Check OneNote sync status and conflict resolution. Verify OneDrive storage isn't full "
        "and network connectivity is stable.",
    ],
    remediation_steps=[
        [
            "Check OneNote sync status for specific error messages",
            "Verify OneDrive storage quota isn't exceeded",
            "Force a manual sync and resolve any conflicts",
            "Check for OneNote updates that may fix sync issues",
            "If notes were lost, check OneDrive version history for recovery",
        ],
    ],
))

register(ScenarioTemplate(
    scenario_id="sw-027",
    category=Category.SOFTWARE,
    priority=Priority.P4,
    assigned_team=Team.ENTERPRISE_APPS,
    needs_escalation=False,
    missing_information=[MissingInfo.ERROR_MESSAGE, MissingInfo.DEVICE_INFO],
    subjects=[
        "Video playback not working in training portal",
        "Can't watch training videos — just shows a black screen",
        "E-learning platform videos won't play",
    ],
    descriptions=[
        "The videos on our internal training portal aren't playing. I click play and get a black "
        "screen with an error icon. I need to complete my compliance training by end of month. "
        "Audio plays fine but no video. This might be a codec or browser compatibility issue.",
        "Our e-learning platform at learn.contoso.com doesn't play videos properly. The video "
        "thumbnails load but when I click play, nothing happens. I've tried Edge and Chrome. "
        "Other websites' videos work fine.",
    ],
    next_best_actions=[
        "Check browser media codec support and training portal compatibility requirements. "
        "Verify content delivery network connectivity.",
    ],
    remediation_steps=[
        [
            "Verify browser version meets the training portal requirements",
            "Check if video format requires specific codecs not available",
            "Disable browser extensions that may block media playback",
            "Try accessing the portal in InPrivate mode",
            "If widespread, contact the training portal vendor for support",
        ],
    ],
))

register(ScenarioTemplate(
    scenario_id="sw-028",
    category=Category.SOFTWARE,
    priority=Priority.P3,
    assigned_team=Team.ENTERPRISE_APPS,
    needs_escalation=False,
    missing_information=[MissingInfo.ERROR_MESSAGE, MissingInfo.STEPS_TO_REPRODUCE],
    subjects=[
        "Workday self-service portal timeout errors",
        "Can't access Workday — keeps timing out",
        "Workday HR portal very slow and unresponsive",
    ],
    descriptions=[
        "Workday is timing out every time I try to submit my expense report. The page loads but "
        "when I click Submit, it spins for about 2 minutes then shows 'Request Timeout.' I've "
        "tried multiple times. My expense report is due tomorrow.",
        "The Workday self-service portal is extremely slow. Navigating between pages takes 30-60 "
        "seconds. Most actions result in timeout errors. I need to approve time-off requests for "
        "my team but can't get through the workflow.",
    ],
    next_best_actions=[
        "Check Workday service status and network connectivity. Verify if the issue is specific "
        "to certain Workday modules or affecting all functionality.",
    ],
    remediation_steps=[
        [
            "Check Workday community status page for known outages",
            "Verify network connectivity and DNS resolution for Workday",
            "Test Workday from a different network to isolate the issue",
            "If proxy related, check proxy configuration for Workday domains",
            "Contact Workday support if the issue is service-side",
        ],
    ],
))

register(ScenarioTemplate(
    scenario_id="sw-029",
    category=Category.SOFTWARE,
    priority=Priority.P4,
    assigned_team=Team.ENDPOINT,
    needs_escalation=False,
    missing_information=[MissingInfo.DEVICE_INFO, MissingInfo.APPLICATION_VERSION],
    subjects=[
        "Teams status stuck on 'In a meeting' permanently",
        "My Teams presence shows wrong status all the time",
        "Teams status doesn't change — always shows busy",
    ],
    descriptions=[
        "My Teams status has been stuck on 'In a meeting' for 3 days now even though I'm not in "
        "any meeting. I've tried manually changing it to Available but it reverts back within "
        "minutes. People think I'm always busy and aren't messaging me.",
        "My Teams presence indicator is permanently showing 'Busy' even when I'm idle. I've "
        "restarted Teams, cleared the cache, even signed out and back in. It still shows the "
        "wrong status. Colleagues have started calling my phone instead of Teams.",
    ],
    next_best_actions=[
        "Clear Teams presence cache and reset presence state. Check for stuck calendar events "
        "that may be keeping the status locked.",
    ],
    remediation_steps=[
        [
            "Sign out of Teams completely on all devices",
            "Clear Teams cache (including presence cache files)",
            "Check Outlook calendar for phantom or stuck meetings",
            "Sign back in and manually set status to Available",
            "If issue persists, reset presence via PowerShell admin tools",
        ],
    ],
))

register(ScenarioTemplate(
    scenario_id="sw-030",
    category=Category.SOFTWARE,
    priority=Priority.P2,
    assigned_team=Team.ENDPOINT,
    needs_escalation=False,
    missing_information=[MissingInfo.AFFECTED_USERS, MissingInfo.ENVIRONMENT_DETAILS],
    subjects=[
        "Multiple apps crashing after Windows update — widespread impact",
        "Windows update broke several applications",
        "Post-update chaos — Outlook, Teams, and SAP all broken",
    ],
    descriptions=[
        "After last night's Windows update (KB5035849), multiple applications are crashing on "
        "startup. Outlook, Teams, and our internal tools are all affected. I've talked to 5 "
        "colleagues and they all have the same problem. We're basically unable to work. The "
        "update was pushed to all machines overnight.",
        "The Windows update that was deployed last night has broken everything. Chrome crashes, "
        "Outlook won't start, and the VPN client errors out. This seems to be affecting everyone "
        "who received the update. Is there a way to roll it back?",
    ],
    next_best_actions=[
        "Identify the problematic Windows update and assess rollback options. Check for known "
        "issues with the specific KB number and coordinate a response for all affected users.",
    ],
    remediation_steps=[
        [
            "Identify the specific Windows update causing issues (KB number)",
            "Check Microsoft Known Issues dashboard for the KB",
            "Test uninstalling the update on a sample machine",
            "If rollback resolves the issue, prepare Intune policy to remove the update",
            "Pause the update deployment for machines that haven't received it yet",
            "Communicate workaround and timeline to all affected users",
        ],
    ],
))

register(ScenarioTemplate(
    scenario_id="sw-031",
    category=Category.SOFTWARE,
    priority=Priority.P3,
    assigned_team=Team.ENDPOINT,
    needs_escalation=False,
    missing_information=[
        MissingInfo.ERROR_MESSAGE,
        MissingInfo.ENVIRONMENT_DETAILS,
        MissingInfo.STEPS_TO_REPRODUCE,
    ],
    subjects=[
        "Trading app works for everyone except me — same hardware and OS",
        "Only person on team who can't launch internal trading application",
        "App failure on my machine only — rest of team is fine",
    ],
    descriptions=[
        "I'm the only person in my team of 12 who can't run the internal trading application "
        "(TradeDesk Pro v4.2). Everyone else is fine. We all have the same laptop model (Surface "
        "Laptop 5), same OS build, same network. The app just freezes on the splash screen for "
        "me. I've reinstalled it twice, rebooted, cleared the cache — nothing works. My manager "
        "is on my case because I'm falling behind.",
        "Something about my specific machine is preventing the trading app from loading. I've "
        "compared my setup with a colleague's — same model, same Windows version, same software "
        "list in Apps & Features. The app opens fine on their machine but hangs on mine. I even "
        "tried running it as administrator. Could it be a profile corruption issue or a rogue "
        "group policy? I need this fixed ASAP — it's my primary work tool.",
    ],
    next_best_actions=[
        "Compare the user's machine configuration in detail against a working machine. Check "
        "for profile-specific settings, group policy differences, or corrupted local app data.",
    ],
    remediation_steps=[
        [
            "Gather detailed system info: OS build, installed updates, group policy (gpresult)",
            "Compare against a known working machine for any configuration drift",
            "Check the user profile for corrupted app data or settings",
            "Review Event Viewer for application errors during launch attempts",
            "Test with a fresh user profile on the same machine to isolate the issue",
            "If profile-related, migrate the user to a new profile and restore data",
        ],
    ],
))

register(ScenarioTemplate(
    scenario_id="sw-032",
    category=Category.SOFTWARE,
    priority=Priority.P2,
    assigned_team=Team.ENTERPRISE_APPS,
    needs_escalation=False,
    missing_information=[MissingInfo.APPLICATION_VERSION, MissingInfo.CONFIGURATION_DETAILS],
    subjects=[
        "New compliance agent conflicts with SAP — uninstalling agent fixes SAP",
        "SAP crashes on startup since compliance monitoring agent was installed",
        "Software conflict: compliance agent vs. SAP — can't have both running",
    ],
    descriptions=[
        "Ever since the new compliance monitoring agent (ComplianceGuard v3.1) was deployed to "
        "our machines last Tuesday, SAP GUI crashes on startup with an access violation error. "
        "I've confirmed the correlation: uninstalling the agent fixes SAP immediately. "
        "Reinstalling it brings the crash back. The problem is we're required to have the "
        "compliance agent installed — it's mandated by InfoSec. So right now I have to choose "
        "between SAP and compliance. I need both.",
        "SAP has been unusable since the compliance monitoring agent rollout. It crashes within "
        "seconds of launching — sometimes with an error, sometimes it just disappears. Three of "
        "us in Finance have confirmed that removing the compliance agent resolves the issue. But "
        "IT policy requires the agent. We're stuck. Can someone figure out a compatibility fix "
        "or get us an exception while this is sorted out?",
    ],
    next_best_actions=[
        "Investigate the conflict between the compliance agent and SAP. Check for known "
        "compatibility issues and work with both vendors on a resolution.",
    ],
    remediation_steps=[
        [
            "Confirm the exact versions of both SAP GUI and the compliance agent",
            "Check the compliance agent vendor's known issues for SAP conflicts",
            "Review Windows Event Viewer for crash details and conflicting DLLs",
            "Test adding SAP directories to the compliance agent's exclusion list",
            "If exclusion resolves it, coordinate with InfoSec to approve the exception",
            "Push the updated configuration to all affected machines",
            "Monitor for recurrence after the next compliance agent update",
        ],
    ],
))

register(ScenarioTemplate(
    scenario_id="sw-033",
    category=Category.SOFTWARE,
    priority=Priority.P3,
    assigned_team=Team.ENTERPRISE_APPS,
    needs_escalation=False,
    missing_information=[MissingInfo.AFFECTED_USERS, MissingInfo.SCREENSHOT_OR_ATTACHMENT],
    subjects=[
        "Internal web app gets slower throughout the day — unusable by 3pm",
        "Progressive performance degradation in web app — reboot helps briefly",
        "Web app fast in morning, crawling by afternoon — memory leak?",
    ],
    descriptions=[
        "Our internal web application (FieldTracker) gets progressively slower throughout the "
        "day. At 9am when I first log in, pages load in under a second. By noon it's taking 5-10 "
        "seconds. By 3pm it's completely unusable — clicks take 30+ seconds to respond. Restarting "
        "my browser helps, but only for about 10 minutes before it slows down again. I suspect a "
        "memory leak in the app. This has been happening daily for about two weeks.",
        "There's a worsening performance issue with our internal project management web app. It's "
        "snappy in the morning but degrades steadily. By mid-afternoon the browser tab is consuming "
        "over 2GB of RAM according to Task Manager. Closing and reopening the tab resets it "
        "temporarily. I've tried Chrome and Edge — same behavior in both. I think the app has a "
        "JavaScript memory leak. It's affecting my entire team's productivity.",
    ],
    next_best_actions=[
        "Investigate the client-side performance degradation. Capture browser memory profiles "
        "at different times of day to confirm a memory leak in the web application.",
    ],
    remediation_steps=[
        [
            "Collect browser Task Manager data showing memory growth over time",
            "Take heap snapshots in browser DevTools at 9am, noon, and 3pm",
            "Identify which JavaScript objects are accumulating and not being garbage collected",
            "Report the memory leak to the application development team with evidence",
            "As a temporary workaround, advise the user to refresh the browser tab every 2 hours",
            "Track the fix through the development team's release cycle",
        ],
    ],
))

register(ScenarioTemplate(
    scenario_id="sw-034",
    category=Category.SOFTWARE,
    priority=Priority.P4,
    assigned_team=Team.ENDPOINT,
    needs_escalation=False,
    missing_information=[MissingInfo.APPLICATION_VERSION, MissingInfo.DEVICE_INFO],
    subjects=[
        "Outlook schedule-send feature is broken — can't find the button",
        "Bug report: Outlook missing the delayed send option",
        "Outlook doesn't let me schedule emails for later — feature missing",
    ],
    descriptions=[
        "I think Outlook is broken because I can't find the option to schedule an email to send "
        "at a specific time. I've looked in every menu and it's not there. My colleague showed me "
        "it works on their computer so clearly something is wrong with my installation. Can you "
        "fix this? I need to schedule emails for different time zones.",
        "I'm reporting a bug in Outlook — the 'Schedule Send' or 'Delay Delivery' feature is "
        "missing from my version. I've checked under Options > Delay Delivery and it's grayed "
        "out. Other people seem to have it. I rely on this to send emails at appropriate times "
        "to our APAC team. Please update my Outlook or fix whatever is preventing this from "
        "appearing.",
    ],
    next_best_actions=[
        "Clarify whether this is a missing feature (version-dependent) or a misconfiguration. "
        "Check the user's Outlook version and license to determine feature availability.",
    ],
    remediation_steps=[
        [
            "Check the user's Outlook version (classic vs. new Outlook, desktop vs. web)",
            "Verify their Microsoft 365 license tier — some features are license-dependent",
            "If the feature exists in their version, guide them to the correct menu location",
            "If it's a version limitation, explain the difference and suggest alternatives",
            "If Delay Delivery is grayed out, check group policies or admin restrictions",
        ],
    ],
))

register(ScenarioTemplate(
    scenario_id="sw-035",
    category=Category.SOFTWARE,
    priority=Priority.P3,
    assigned_team=Team.ENDPOINT,
    needs_escalation=False,
    missing_information=[MissingInfo.APPLICATION_VERSION, MissingInfo.ERROR_MESSAGE],
    subjects=[
        "Microsoft Store app immediately quarantined by Defender",
        "Defender blocking app I downloaded from the Microsoft Store",
        "App from official store flagged as threat — need it for work",
    ],
    descriptions=[
        "I downloaded an app called 'DevTunnel Tools' from the Microsoft Store and Windows "
        "Defender immediately quarantined it. The notification says it detected a potential "
        "threat but doesn't give details. This app was recommended by my tech lead for local "
        "development tunneling. I need it for work but I can't override the quarantine — the "
        "'Allow' button is grayed out. Can someone whitelist this or verify it's safe?",
        "Windows Defender is blocking an app I installed from the Microsoft Store. The app is "
        "'Network Profiler Pro' and I need it for diagnosing connectivity issues as part of my "
        "job in the network team. Defender flags it as 'PUA:Win32/Presenoker' and quarantines "
        "it. I've confirmed it's the official app from a reputable publisher. I can't allow it "
        "myself due to policy restrictions. Please review and whitelist if appropriate.",
    ],
    next_best_actions=[
        "Review the Defender quarantine details and the app's legitimacy. If the app is safe "
        "and business-justified, submit a Defender exclusion request through the security team.",
    ],
    remediation_steps=[
        [
            "Check the Defender quarantine log for the specific threat classification",
            "Verify the app's publisher and legitimacy in the Microsoft Store",
            "If the app is a false positive, submit an exclusion request to the security team",
            "If approved, add the app to the Defender exclusion policy via Intune",
            "Confirm the user can install and run the app after the exclusion is applied",
            "Report the false positive to Microsoft through the Defender portal",
        ],
    ],
))

# ---------------------------------------------------------------------------
# sw-036  Excel macro breaking after Office update
# ---------------------------------------------------------------------------
register(ScenarioTemplate(
    scenario_id="sw-036",
    category=Category.SOFTWARE,
    priority=Priority.P3,
    assigned_team=Team.ENTERPRISE_APPS,
    needs_escalation=False,
    missing_information=[MissingInfo.APPLICATION_VERSION, MissingInfo.REPRODUCTION_FREQUENCY],
    subjects=[
        "Excel macro stopped working after Office update",
        "VBA macro broken since last Office patch",
        "Excel automation scripts failing — recent update suspected",
    ],
    descriptions=[
        "My Excel macro that generates the weekly finance report stopped working after the "
        "latest Office update was pushed to my machine. It throws a 'Run-time error 1004' "
        "when it tries to access a named range. I'm not sure which Office version I'm on now "
        "or what build was installed. The macro has been working fine for months. I'm not sure "
        "if it fails every time or only on certain workbooks.",
        "Since the Office update last Tuesday, my VBA macros in our budget tracking spreadsheet "
        "are completely broken. The code references some ActiveX controls that seem to have "
        "changed. I don't know my exact Office build number and I haven't checked whether it "
        "fails consistently or just intermittently — I've only tried a few times and it broke "
        "each time so far.",
    ],
    next_best_actions=[
        "Determine the user's current Office version and build number. Ask them to test the "
        "macro on multiple workbooks to establish reproduction frequency.",
    ],
    remediation_steps=[
        [
            "Get the Office version via File > Account > About in Excel",
            "Check the Office update history to identify which build was recently installed",
            "Test the macro to reproduce the error and capture the exact error message",
            "Check Microsoft's known issues list for the installed build",
            "If a known regression, roll back to the previous Office build via deployment tool",
        ],
    ],
))

# ---------------------------------------------------------------------------
# sw-037  Outlook calendar sync issues
# ---------------------------------------------------------------------------
register(ScenarioTemplate(
    scenario_id="sw-037",
    category=Category.SOFTWARE,
    priority=Priority.P3,
    assigned_team=Team.ENTERPRISE_APPS,
    needs_escalation=False,
    missing_information=[MissingInfo.SCREENSHOT_OR_ATTACHMENT, MissingInfo.REPRODUCTION_FREQUENCY],
    subjects=[
        "Outlook calendar not syncing — meetings disappearing",
        "Calendar sync broken in Outlook — intermittent",
        "Outlook shows wrong meeting times and missing appointments",
    ],
    descriptions=[
        "My Outlook calendar is not syncing properly. Meetings that colleagues send me show up "
        "on my phone but not in the desktop Outlook client. Sometimes they appear hours later, "
        "and twice this week a meeting vanished completely and I missed it. I get an error "
        "briefly in the status bar but it disappears too fast to read. I haven't been able to "
        "screenshot it yet.",
        "Outlook desktop is having intermittent calendar sync failures. My shared team calendar "
        "shows appointments that don't match what others see, and some recurring meetings have "
        "wrong times. I'm not sure how often the sync fails — I just notice it when something "
        "is missing. I tried to capture the sync error popup but it closes before I can grab it.",
    ],
    next_best_actions=[
        "Ask the user to capture a screenshot of the sync error. Determine how frequently "
        "the sync failures occur and whether the issue is limited to specific calendars.",
    ],
    remediation_steps=[
        [
            "Ask the user to watch for the status bar error and capture a screenshot",
            "Check the Outlook sync status via the Connection Status dialog (Ctrl+right-click tray icon)",
            "Verify the Exchange Online mailbox health using Get-MailboxStatistics",
            "Reset the Outlook profile or repair the OST file if corruption is suspected",
            "Monitor sync behavior after the repair and confirm meetings appear correctly",
        ],
    ],
))

# ---------------------------------------------------------------------------
# sw-038  Power BI gateway connection timeout
# ---------------------------------------------------------------------------
register(ScenarioTemplate(
    scenario_id="sw-038",
    category=Category.SOFTWARE,
    priority=Priority.P2,
    assigned_team=Team.ENTERPRISE_APPS,
    needs_escalation=True,
    missing_information=[MissingInfo.PREVIOUS_TICKET_ID, MissingInfo.ERROR_MESSAGE],
    subjects=[
        "Power BI gateway timing out — reports not refreshing",
        "Power BI data refresh failing — gateway connection issue",
        "Gateway error in Power BI — can't pull live data",
    ],
    descriptions=[
        "Our Power BI on-premises data gateway is timing out when refreshing datasets. The "
        "executive dashboards haven't updated since yesterday morning. The gateway status page "
        "shows 'Connected' but scheduled refreshes fail with a timeout. We had a similar "
        "incident about three weeks ago that was resolved by the data platform team, but I "
        "don't have the old ticket number.",
        "Power BI reports connected to our on-prem SQL Server are failing to refresh. The error "
        "says something about a gateway timeout but I didn't copy the full message. This is "
        "blocking the finance team's daily reporting. There was a previous incident with the "
        "same gateway last month — I think someone from infrastructure fixed it, but I can't "
        "locate that ticket.",
    ],
    next_best_actions=[
        "Find the previous gateway incident ticket to check for a recurring root cause. "
        "Capture the full error message from the Power BI service refresh history.",
    ],
    remediation_steps=[
        [
            "Retrieve the full error message from Power BI Service > Dataset > Refresh History",
            "Search for the previous gateway incident ticket by date and keywords",
            "Check the gateway machine's resource utilization (CPU, memory, network)",
            "Restart the on-premises data gateway service and test a manual refresh",
            "If the timeout persists, review firewall rules and proxy settings between gateway and data source",
            "Escalate to the data platform team if the issue matches the prior incident pattern",
        ],
    ],
))

# ---------------------------------------------------------------------------
# sw-039  Teams phone system (PSTN) call quality degradation
# ---------------------------------------------------------------------------
register(ScenarioTemplate(
    scenario_id="sw-039",
    category=Category.SOFTWARE,
    priority=Priority.P2,
    assigned_team=Team.ENTERPRISE_APPS,
    needs_escalation=False,
    missing_information=[MissingInfo.CONTACT_INFO, MissingInfo.NETWORK_LOCATION],
    subjects=[
        "Teams phone calls have terrible audio quality",
        "PSTN calls via Teams are choppy and dropping",
        "Teams calling — voice quality degraded for external calls",
    ],
    descriptions=[
        "Since last week, every PSTN call I make through Teams has terrible audio quality. "
        "External callers say I sound robotic and the audio cuts in and out. Internal Teams "
        "calls seem fine — it's only when dialing external phone numbers. I'm in the trading "
        "floor area but I'm not sure which network segment that's on. I need a callback but "
        "my Teams number is the one having issues, so you'll need my cell.",
        "Teams phone system calls to external numbers are experiencing severe quality "
        "degradation — echoing, packet loss, and sometimes calls drop entirely. This is "
        "impacting our client-facing team. I'm not sure what floor or office my network "
        "jack connects to. My desk phone is a Teams-certified device but I'd rather be "
        "contacted on my personal mobile since the Teams line is unreliable right now.",
    ],
    next_best_actions=[
        "Get the user's alternate contact number for callback. Determine their network "
        "location to check QoS and media path for PSTN calls.",
    ],
    remediation_steps=[
        [
            "Collect the user's personal mobile number or alternate contact for follow-up",
            "Identify the user's network location (floor, switch, VLAN) to check QoS policies",
            "Pull the Teams Call Quality Dashboard (CQD) data for the user's recent PSTN calls",
            "Check the SBC (Session Border Controller) health and PSTN trunk utilization",
            "Verify QoS markings are applied correctly for media traffic on the user's subnet",
            "If the issue is network-related, engage the network team to prioritize voice traffic",
        ],
    ],
))

# ---------------------------------------------------------------------------
# sw-040  Adobe Creative Cloud license activation failure
# ---------------------------------------------------------------------------
register(ScenarioTemplate(
    scenario_id="sw-040",
    category=Category.SOFTWARE,
    priority=Priority.P3,
    assigned_team=Team.ENTERPRISE_APPS,
    needs_escalation=False,
    missing_information=[MissingInfo.AUTHENTICATION_METHOD, MissingInfo.SCREENSHOT_OR_ATTACHMENT],
    subjects=[
        "Adobe Creative Cloud won't activate — license error",
        "Can't sign into Adobe CC — activation keeps failing",
        "Adobe license not recognized after reinstall",
    ],
    descriptions=[
        "I reinstalled Adobe Creative Cloud on my new workstation and it won't activate. When "
        "I try to sign in, it says my license can't be verified and prompts me to try again. "
        "I'm not sure whether I should be using my Contoso SSO credentials or a separate Adobe "
        "ID — I've tried both and neither works. I tried to screenshot the error but the dialog "
        "closed before I could capture it.",
        "Adobe Creative Cloud apps (Photoshop, Illustrator) are showing 'Trial Expired' even "
        "though our team has enterprise licenses. The activation dialog asks me to sign in but "
        "I don't know if I should use federated SSO or a named-user Adobe account. I've tried "
        "signing in multiple ways and keep getting a generic activation error. I haven't been "
        "able to capture the exact error screen.",
    ],
    next_best_actions=[
        "Clarify the correct authentication method for Adobe CC (SSO vs. Adobe ID). Ask the "
        "user to capture a screenshot of the activation error on their next attempt.",
    ],
    remediation_steps=[
        [
            "Confirm the correct sign-in method — check if Contoso uses Federated ID or Enterprise ID for Adobe",
            "Verify the user's Adobe license assignment in the Adobe Admin Console",
            "Have the user sign out of all Adobe apps and clear the OOBE folder to reset activation",
            "Guide the user through signing in with the correct credentials and capture any errors",
            "If activation still fails, re-provision the license in the Adobe Admin Console",
        ],
    ],
))

# ---------------------------------------------------------------------------
# sw-041  SharePoint Online performance issues — ambiguous: Enterprise Apps vs Data Platform
# ---------------------------------------------------------------------------
register(ScenarioTemplate(
    scenario_id="sw-041",
    category=Category.SOFTWARE,
    priority=Priority.P2,
    assigned_team=Team.ENTERPRISE_APPS,
    needs_escalation=False,
    missing_information=[MissingInfo.AFFECTED_USERS, MissingInfo.ENVIRONMENT_DETAILS],
    subjects=[
        "SharePoint Online extremely slow — pages take forever to load",
        "SharePoint performance degraded — document libraries timing out",
        "SharePoint sites crawling — impacting team productivity",
    ],
    descriptions=[
        "Our SharePoint Online sites have been extremely slow for the past two days. Document "
        "libraries take 20-30 seconds to load and uploading files frequently times out. The issue "
        "seems worse on sites with large document libraries. I'm not sure if this is affecting "
        "just our team or the entire organization — I've heard a couple of other people complain "
        "but haven't confirmed broadly. We recently migrated a large batch of documents from our "
        "on-prem file server to SharePoint, and I wonder if that's related. I'm not sure which "
        "SharePoint environment or tenant region we're in.",
        "SharePoint Online performance has degraded significantly. Pages load slowly, search is "
        "nearly unusable, and document previews time out. The Microsoft 365 Service Health "
        "dashboard doesn't show any active incidents for SharePoint, so this seems specific to "
        "our tenant. I don't know how many users are affected — my immediate team of five all "
        "experience it, but I haven't surveyed other departments. We have several large custom "
        "lists and document libraries that may be contributing to the issue, but I'm not sure "
        "about the specifics of our SharePoint environment configuration.",
    ],
    next_best_actions=[
        "Determine the scope of impact — survey additional users and check SharePoint admin center "
        "analytics. Review the recent document migration for any impact on site collection storage "
        "limits or throttling.",
        "Check SharePoint admin center for tenant-level health indicators and identify if specific "
        "site collections are affected. Determine the number of affected users and the environment "
        "details (tenant region, any custom solutions deployed).",
    ],
    remediation_steps=[
        [
            "Check the M365 Service Health dashboard and SharePoint admin center for tenant-level issues",
            "Survey a broader set of users to determine the scope — team-level or organization-wide",
            "Review recent changes: document migration volume, custom solutions, large list thresholds",
            "Check site collection storage quotas and list view throttling limits",
            "If related to the recent migration, check for indexing backlog or throttling on the affected sites",
            "Open a Microsoft support request if the issue is tenant-wide and no local cause is found",
        ],
    ],
))

# ---------------------------------------------------------------------------
# sw-042  Teams integration with third-party app broken — ambiguous: Enterprise Apps vs Network
# ---------------------------------------------------------------------------
register(ScenarioTemplate(
    scenario_id="sw-042",
    category=Category.SOFTWARE,
    priority=Priority.P3,
    assigned_team=Team.ENTERPRISE_APPS,
    needs_escalation=False,
    missing_information=[MissingInfo.APPLICATION_VERSION, MissingInfo.ERROR_MESSAGE],
    subjects=[
        "Teams integration with Jira broken — can't create issues from Teams",
        "Third-party app connector in Teams stopped working",
        "Teams app integration with project management tool failing",
    ],
    descriptions=[
        "The Jira Cloud integration in Microsoft Teams stopped working last week. When I try to "
        "create a Jira issue from the Teams message action, I get a spinner that eventually fails "
        "with a vague error. The Jira tab in our project channel also shows a connection error "
        "instead of the board view. Other Teams features work fine — it's specifically the "
        "third-party app integration that's broken. I don't know what version of the Jira Teams "
        "app we have installed or the exact error message because the dialog disappears quickly. "
        "The integration was working fine until recently, so something must have changed on either "
        "the Teams or Jira side.",
        "Our project management tool's Teams connector has stopped syncing. Notifications from "
        "Jira that used to appear in our Teams channel have ceased, and the embedded Jira tab "
        "throws an error when loading. I checked and other Teams connectors like our CI/CD "
        "notifications still work, so it's isolated to this specific app integration. I'm not "
        "sure of the app version or the exact error text. The Teams admin may have updated app "
        "permissions or the Jira API endpoint configuration might have changed — I don't have "
        "visibility into either.",
    ],
    next_best_actions=[
        "Check the Teams admin center for the Jira app's status, version, and permission "
        "configuration. Review the app's OAuth consent and API connectivity to Jira Cloud.",
        "Verify the third-party app's installation and permissions in the Teams admin center. "
        "Ask the user to capture the exact error message on the next occurrence and check if "
        "the app needs to be re-authorized.",
    ],
    remediation_steps=[
        [
            "Check the Teams admin center for the Jira app's installation status and version",
            "Review the app's permissions and OAuth consent — check if re-authorization is needed",
            "Ask the user to capture the exact error message on the next failure attempt",
            "Test the Jira API endpoint connectivity from the Teams environment",
            "If permissions or API config changed, re-authorize the app and update the connector settings",
            "Verify the integration is working by testing issue creation and channel notifications end-to-end",
        ],
    ],
))
