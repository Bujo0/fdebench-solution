# Copyright (c) Microsoft. All rights reserved.
"""Software & Applications category scenarios for eval dataset."""

from ms.eval_generator.scenarios._base import ScenarioDefinition
from ms.eval_generator.scenarios._base import ScenarioGold

SOFTWARE_SCENARIOS: list[ScenarioDefinition] = [
    # ── 001 Teams crashes on launch after update ── Enterprise Applications ──
    ScenarioDefinition(
        scenario_id="software-001",
        subjects=(
            "Teams keeps crashing after latest update",
            "Microsoft Teams won't launch since this morning",
            "Teams crashes immediately on startup",
        ),
        descriptions=(
            "Ever since the Teams update rolled out overnight, the app crashes within"
            " seconds of launching. I've tried restarting my laptop and clearing the"
            " cache but nothing helps. I need Teams for back-to-back meetings starting"
            " at 10am.",
            "Teams updated itself and now it just shows a brief splash screen then"
            " closes. I'm on Windows 11, build 22631. Already tried running as admin."
            " This is blocking my entire morning.",
            "Hi, Teams has been crashing on launch since the auto-update. Error popup"
            " says something about a DLL load failure. Can someone help? I've got"
            " client calls all day.",
        ),
        gold=ScenarioGold(
            category="Software & Applications",
            priority="P2",
            assigned_team="Enterprise Applications",
            needs_escalation=False,
            missing_information=(),
            next_best_action="Clear Teams cache and reinstall from Company Portal",
            remediation_steps=(
                "Kill all Teams processes via Task Manager",
                "Delete contents of %AppData%/Microsoft/Teams",
                "Reinstall Teams from Company Portal or Intune",
                "Verify launch and sign-in",
            ),
        ),
    ),
    # ── 002 Outlook calendar showing deleted meetings ── Endpoint Engineering ──
    ScenarioDefinition(
        scenario_id="software-002",
        subjects=(
            "Outlook calendar keeps showing meetings I already deleted",
            "Deleted meetings reappearing on my Outlook calendar",
        ),
        descriptions=(
            "I deleted several recurring meetings last week but they keep showing back"
            " up on my Outlook calendar. Every time I remove them they reappear within"
            " an hour. Running Outlook desktop version on Windows 11.",
            "Ghost meetings on my calendar — I've cancelled and deleted them multiple"
            " times but they keep coming back. My calendar is a mess and I'm getting"
            " double-booked. Please help.",
            "Calendar sync seems broken. Old meetings that I deleted weeks ago are"
            " popping back up. I checked OWA and they're gone there, but my desktop"
            " Outlook keeps resurrecting them.",
        ),
        gold=ScenarioGold(
            category="Software & Applications",
            priority="P3",
            assigned_team="Endpoint Engineering",
            needs_escalation=False,
            missing_information=(),
            next_best_action="Repair Outlook profile and rebuild calendar cache",
            remediation_steps=(
                "Close Outlook and run the Outlook profile repair tool",
                "Clear the local Outlook cache (OST file)",
                "Restart Outlook and allow full resync from Exchange",
                "Confirm deleted meetings are no longer reappearing",
            ),
        ),
    ),
    # ── 003 Excel crashing when opening large files ── Enterprise Applications ──
    ScenarioDefinition(
        scenario_id="software-003",
        subjects=(
            "Excel crashes every time I open our quarterly report file",
            "Large Excel spreadsheets causing Excel to freeze and crash",
        ),
        descriptions=(
            "Whenever I try to open the Q3 financial consolidation workbook (~85MB),"
            " Excel freezes for about 30 seconds then crashes. No error message, just"
            " closes. Smaller files open fine. I need this for month-end close.",
            "Excel keeps crashing on large files. Specifically the portfolio risk model"
            " spreadsheet which has about 200k rows and lots of VLOOKUP formulas."
            " Worked fine last month. Currently on M365 Apps version 2310.",
        ),
        gold=ScenarioGold(
            category="Software & Applications",
            priority="P2",
            assigned_team="Enterprise Applications",
            needs_escalation=False,
            missing_information=(),
            next_best_action=("Check Office version and repair installation; verify sufficient RAM"),
            remediation_steps=(
                "Update Microsoft 365 Apps to latest build",
                "Run Office online repair via Settings > Apps",
                "Disable hardware acceleration in Excel options",
                "Open file in Safe Mode to rule out add-in conflicts",
                "If issue persists, collect crash dump for escalation",
            ),
        ),
    ),
    # ── 004 Software install request — Adobe Creative Suite ── Endpoint Eng ──
    ScenarioDefinition(
        scenario_id="software-004",
        subjects=(
            "Need Adobe Creative Suite installed on my workstation",
            "Software request: Adobe Creative Suite",
            "Requesting installation of Adobe CC",
        ),
        descriptions=(
            "Hi, I'm in the Marketing department and need Adobe Creative Suite"
            " (Photoshop, Illustrator, InDesign) installed on my machine for an"
            " upcoming campaign project starting next Monday. My manager Sarah Chen"
            " has approved the request. Asset tag: WS-4521.",
            "I need Adobe Creative Cloud apps for a branding project. Specifically"
            " Photoshop and Illustrator. Is this available through Company Portal or"
            " does IT need to push it? My laptop is YOURPC-7841.",
        ),
        gold=ScenarioGold(
            category="Software & Applications",
            priority="P3",
            assigned_team="Endpoint Engineering",
            needs_escalation=False,
            missing_information=(
                "Manager approval confirmation or ticket reference number",
                "Specific Adobe CC apps needed if not full suite",
            ),
            next_best_action=("Verify license availability and manager approval, then deploy via Intune"),
            remediation_steps=(
                "Confirm manager approval and budget code for Adobe license",
                "Check available Adobe CC license pool",
                "Deploy Adobe Creative Cloud via Intune to target device",
                "Verify installation and user sign-in to Adobe account",
            ),
        ),
    ),
    # ── 005 SAP GUI connection error ── Enterprise Applications ──
    ScenarioDefinition(
        scenario_id="software-005",
        subjects=(
            "SAP GUI throwing connection error — can't access production",
            "Unable to connect to SAP — getting RFC error",
        ),
        descriptions=(
            "When I launch SAP GUI and try to connect to the PRD system, I get error"
            " 'Partner not reached (hostname sapapp01.contoso.local, service 3200)'."
            " I can ping the server fine. Other team members in Treasury seem to be"
            " having the same issue.",
            "SAP GUI won't connect since about 9:15am. Getting a connection timeout."
            " I'm in Accounts Payable and we have invoice processing deadlines today."
            " The DEV system connects fine — it's just production.",
            "Hi support, SAP production is unreachable via SAP GUI. Error message says"
            " the RFC connection failed. QA system works. We have 15+ users affected"
            " in the Finance department.",
        ),
        gold=ScenarioGold(
            category="Software & Applications",
            priority="P1",
            assigned_team="Enterprise Applications",
            needs_escalation=False,
            missing_information=(),
            next_best_action=("Check SAP application server status and network path to port 3200"),
            remediation_steps=(
                "Verify SAP application server process status on sapapp01",
                "Check port 3200 connectivity from client network segment",
                "Review SAP dispatcher logs for service crashes",
                "Restart SAP dispatcher service if needed",
                "Confirm user connectivity across affected departments",
            ),
        ),
    ),
    # ── 006 Windows update failed and rolled back ── Endpoint Engineering ──
    ScenarioDefinition(
        scenario_id="software-006",
        subjects=(
            "Windows update keeps failing and rolling back",
            "Windows Update error — unable to install cumulative update",
        ),
        descriptions=(
            "My laptop has been trying to install a Windows update for three days now."
            " It downloads, starts installing during restart, gets to about 60%, then"
            " says 'Undoing changes' and rolls back. Error code 0x800f0922."
            " I'm worried this is a security patch I'm missing.",
            "Windows Update failed again last night. It's the February cumulative"
            " update KB5034763. Machine rebooted twice and then rolled back. This is"
            " my third attempt. Running Windows 11 Enterprise 23H2.",
        ),
        gold=ScenarioGold(
            category="Software & Applications",
            priority="P3",
            assigned_team="Endpoint Engineering",
            needs_escalation=False,
            missing_information=(),
            next_best_action="Run Windows Update troubleshooter and check disk space",
            remediation_steps=(
                "Run the built-in Windows Update troubleshooter",
                "Verify sufficient disk space on C: drive (min 20GB free)",
                "Clear Windows Update cache (SoftwareDistribution folder)",
                "Attempt manual installation of the KB via WSUS catalog",
                "If still failing, run DISM and SFC to repair system image",
            ),
        ),
    ),
    # ── 007 Bloomberg terminal data feed delayed ── Enterprise Applications ──
    ScenarioDefinition(
        scenario_id="software-007",
        subjects=(
            "Bloomberg terminal data feed is delayed — prices are stale",
            "Bloomberg showing stale market data",
        ),
        descriptions=(
            "My Bloomberg terminal is showing market data that's about 15 minutes"
            " behind. Real-time pricing is critical for our trading desk. I've checked"
            " with two colleagues and they're seeing the same lag. The terminal itself"
            " is responsive — it's just the data feed that's delayed.",
            "Bloomberg data feed latency issue on the Fixed Income desk. We're seeing"
            " 10-15 minute delays on equity and bond prices. This is impacting our"
            " ability to execute trades at accurate prices. Terminal ID: BT-FI-0342."
            " Need this resolved urgently.",
        ),
        gold=ScenarioGold(
            category="Software & Applications",
            priority="P1",
            assigned_team="Enterprise Applications",
            needs_escalation=False,
            missing_information=(),
            next_best_action=("Verify Bloomberg network connectivity and check for vendor-side incidents"),
            remediation_steps=(
                "Check Bloomberg service status page for known outages",
                "Verify network connectivity to Bloomberg data endpoints",
                "Restart Bloomberg terminal software and re-login",
                "If vendor issue, open case with Bloomberg support",
                "Notify affected trading desks of status",
            ),
        ),
    ),
    # ── 008 Browser compat issue with internal HR portal ── Enterprise Apps ──
    ScenarioDefinition(
        scenario_id="software-008",
        subjects=(
            "HR portal not working properly in Edge",
            "Internal HR website layout broken — buttons unclickable",
            "Browser compatibility issue with PeopleConnect portal",
        ),
        descriptions=(
            "The PeopleConnect HR portal is basically unusable in Microsoft Edge."
            " The navigation menu overlaps with the main content area and the"
            " 'Submit' buttons on the time-off request form don't respond to clicks."
            " It works in Chrome but we're supposed to use Edge per company policy.",
            "I'm trying to submit my annual benefits enrollment through the HR portal"
            " but the page renders incorrectly in Edge. Dropdown menus don't open and"
            " the page layout is all jumbled. Deadline is Friday.",
        ),
        gold=ScenarioGold(
            category="Software & Applications",
            priority="P2",
            assigned_team="Enterprise Applications",
            needs_escalation=False,
            missing_information=(
                "Edge browser version",
                "Whether IE mode has been attempted",
            ),
            next_best_action=("Test with IE mode in Edge and escalate to HR portal vendor if needed"),
            remediation_steps=(
                "Confirm Edge browser version and update if outdated",
                "Test HR portal using IE mode in Edge",
                "Clear browser cache and disable conflicting extensions",
                "If issue persists, escalate to HR portal development team",
                "Add site to IE mode list in Edge enterprise policy if needed",
            ),
        ),
    ),
    # ── 009 Intune enrollment failed on new device ── Endpoint Engineering ──
    ScenarioDefinition(
        scenario_id="software-009",
        subjects=(
            "Intune enrollment failed on new laptop",
            "Can't enroll my new device in Intune — error during setup",
        ),
        descriptions=(
            "I received my new laptop yesterday and during the initial OOBE setup the"
            " Intune enrollment step failed with error 0x801c0003. It completed the"
            " Azure AD join but Intune policies never applied. I can't access any"
            " company apps because compliance policies aren't pushed yet.",
            "New hire starting Monday — their laptop failed Intune enrollment during"
            " Autopilot provisioning. It got stuck on 'Installing apps' for 2 hours"
            " then timed out. Device serial: 5CG1234XYZ. We need this ready ASAP.",
            "Intune enrollment keeps failing on the new Dell Latitude I was issued."
            " Azure AD join went through but the Intune device management piece"
            " errored out. Without enrollment I have no email, no VPN, nothing.",
        ),
        gold=ScenarioGold(
            category="Software & Applications",
            priority="P2",
            assigned_team="Endpoint Engineering",
            needs_escalation=False,
            missing_information=(),
            next_best_action=("Check Intune enrollment status and Autopilot profile assignment"),
            remediation_steps=(
                "Verify device serial is registered in Autopilot",
                "Check Intune enrollment restrictions and license assignment",
                "Reset the device and re-attempt Autopilot provisioning",
                "Monitor enrollment status in Intune admin console",
                "Manually trigger policy sync if enrollment succeeds",
            ),
        ),
    ),
    # ── 010 M365 license not assigned after transfer ── Enterprise Apps ──
    ScenarioDefinition(
        scenario_id="software-010",
        subjects=(
            "Microsoft 365 license missing after department transfer",
            "No M365 license — can't access Office apps since transfer",
        ),
        descriptions=(
            "I transferred from the London office to New York two weeks ago and my"
            " Microsoft 365 license seems to have been removed during the move."
            " I can't open Word, Excel, or PowerPoint — they all say 'Product"
            " Activation Required'. My manager submitted the transfer ticket"
            " on the 5th. Employee ID: E-28471.",
            "Since my department change from Risk to Compliance last Thursday, all my"
            " Office applications show an activation error. Outlook works via the web"
            " but desktop apps are unlicensed. HR confirmed my AD account was updated.",
        ),
        gold=ScenarioGold(
            category="Software & Applications",
            priority="P2",
            assigned_team="Enterprise Applications",
            needs_escalation=False,
            missing_information=("Employee ID or UPN for license lookup",),
            next_best_action=("Check M365 admin center for license assignment status"),
            remediation_steps=(
                "Look up user in M365 admin center",
                "Verify group-based license assignment matches new department",
                "Reassign appropriate M365 license if missing",
                "Have user sign out and back in to Office apps",
                "Confirm activation status on desktop applications",
            ),
        ),
    ),
    # ── 011 PowerPoint presentation corrupted ── Enterprise Applications ──
    ScenarioDefinition(
        scenario_id="software-011",
        subjects=(
            "PowerPoint file corrupted — urgent board presentation",
            "Can't open PowerPoint file — getting corruption error",
        ),
        descriptions=(
            "The Q4 board presentation PPTX file won't open. PowerPoint says the file"
            " is corrupted and can't be repaired. This is a 120-slide deck for the"
            " board meeting on Wednesday. The file is on SharePoint and was last"
            " edited successfully yesterday afternoon. No one else can open it either.",
            "I was editing a PowerPoint deck and my laptop crashed. Now the file won't"
            " open — says 'PowerPoint found a problem with content'. The built-in"
            " repair didn't work. I have a version from two days ago but need the"
            " latest edits. File is in our team SharePoint site.",
        ),
        gold=ScenarioGold(
            category="Software & Applications",
            priority="P2",
            assigned_team="Enterprise Applications",
            needs_escalation=False,
            missing_information=("SharePoint file path or URL",),
            next_best_action=("Attempt recovery from SharePoint version history"),
            remediation_steps=(
                "Check SharePoint version history for the last good version",
                "Try opening the file in PowerPoint Safe Mode",
                "Attempt repair via Open and Repair option",
                "If unrecoverable, restore from SharePoint recycle bin or backup",
                "Educate user on enabling AutoSave for future protection",
            ),
        ),
    ),
    # ── 012 VBA macro blocked by security policy ── Endpoint Engineering ──
    ScenarioDefinition(
        scenario_id="software-012",
        subjects=(
            "VBA macro blocked — can't run our financial model",
            "Security policy blocking Excel macros I need for work",
            "Excel macros disabled by organization policy",
        ),
        descriptions=(
            "Our team's financial forecasting model relies on VBA macros but since"
            " last week's policy update, all macros are blocked with a red banner"
            " saying 'Your organization's security policies have blocked macros'."
            " This workbook has been used by the FP&A team for years. We can't"
            " do our monthly forecasting without it.",
            "I'm unable to run any macros in Excel. Getting a security block message."
            " These are internal macros in files stored on our team SharePoint."
            " My colleague in the same team can still run them. What's different"
            " about my machine?",
        ),
        gold=ScenarioGold(
            category="Software & Applications",
            priority="P2",
            assigned_team="Endpoint Engineering",
            needs_escalation=False,
            missing_information=(
                "File storage location (trusted location check)",
                "Whether macro files are digitally signed",
            ),
            next_best_action=("Review Intune macro policy assignment and trusted locations"),
            remediation_steps=(
                "Check Group Policy / Intune policy for macro settings on device",
                "Verify file location is in the trusted locations list",
                "Add SharePoint path to trusted locations if approved",
                "If macro is unsigned, coordinate with team to sign the VBA project",
                "Confirm macros execute after policy adjustment",
            ),
        ),
    ),
    # ── 013 Outlook search not returning recent emails ── Endpoint Eng ──
    ScenarioDefinition(
        scenario_id="software-013",
        subjects=(
            "Outlook search is broken — not finding recent emails",
            "Outlook search returns no results for emails I know exist",
        ),
        descriptions=(
            "Outlook search has been unreliable for about a week. When I search for"
            " emails from the last few days, they don't show up, but I can see them"
            " in my inbox. Older emails from months ago appear in search results fine."
            " I rely heavily on search to find client correspondence.",
            "Search in Outlook desktop isn't working properly. I search for a subject"
            " line of an email I received yesterday and get zero results. The same"
            " search works perfectly in Outlook Web. Running Outlook as part of M365"
            " Apps on Windows 11.",
        ),
        gold=ScenarioGold(
            category="Software & Applications",
            priority="P3",
            assigned_team="Endpoint Engineering",
            needs_escalation=False,
            missing_information=(),
            next_best_action="Rebuild Outlook search index",
            remediation_steps=(
                "Open Indexing Options in Windows Settings",
                "Verify Microsoft Outlook is included in indexed locations",
                "Click Advanced > Rebuild to rebuild the search index",
                "Wait for indexing to complete (may take 15-30 minutes)",
                "Test search functionality with known recent emails",
            ),
        ),
    ),
    # ── 014 Internal CRM web app showing 502 errors ── Enterprise Apps ──
    ScenarioDefinition(
        scenario_id="software-014",
        subjects=(
            "CRM portal returning 502 Bad Gateway errors",
            "Internal CRM app is down — 502 errors for everyone",
            "ContosoTrack CRM not loading",
        ),
        descriptions=(
            "Our internal CRM application (ContosoTrack) has been returning 502 Bad"
            " Gateway errors since about 8am. Multiple people on the Relationship"
            " Management team are affected. We can't log client interactions or pull"
            " up account details. This is impacting our morning client calls.",
            "ContosoTrack CRM is completely down. Every page returns a 502 error."
            " Tried different browsers and machines — same result. The whole Client"
            " Services team is dead in the water. URL: crm.internal.contoso.com.",
        ),
        gold=ScenarioGold(
            category="Software & Applications",
            priority="P1",
            assigned_team="Enterprise Applications",
            needs_escalation=False,
            missing_information=(),
            next_best_action=("Check CRM application server and load balancer health"),
            remediation_steps=(
                "Check web server and application pool status on CRM servers",
                "Review load balancer health checks for backend failures",
                "Examine application logs for unhandled exceptions or OOM errors",
                "Restart application pool or backend service if unresponsive",
                "Verify database connectivity from the app tier",
                "Confirm service restoration with affected users",
            ),
        ),
    ),
    # ── 015 Python/dev tools install request ── Endpoint Engineering ──
    ScenarioDefinition(
        scenario_id="software-015",
        subjects=(
            "Request to install Python and development tools",
            "Need Python 3.12 and VS Code on my workstation",
        ),
        descriptions=(
            "I'm a quantitative analyst and need Python 3.12, VS Code, and Git"
            " installed on my workstation for a new risk modeling project. I have"
            " approval from my manager Tom Richards (Risk Analytics). These tools"
            " aren't available in Company Portal. Machine: WS-DEV-3389.",
            "Hi, I'm starting a data automation project and need development tools:"
            " Python 3.11+, Visual Studio Code, and the standard data science"
            " packages (pandas, numpy). How do I get these installed? I'm in the"
            " Finance Transformation team.",
            "Requesting developer tooling install. I need Python, pip, and an IDE."
            " We have a bunch of manual Excel processes I want to automate with"
            " scripts. Do I need special permissions or a dev machine?",
        ),
        gold=ScenarioGold(
            category="Software & Applications",
            priority="P3",
            assigned_team="Endpoint Engineering",
            needs_escalation=False,
            missing_information=(
                "Manager approval documentation",
                "Whether a developer-class device is required",
            ),
            next_best_action=("Verify approval and deploy dev tools via Intune or SCCM"),
            remediation_steps=(
                "Confirm manager approval and any licensing requirements",
                "Check if user qualifies for developer workstation image",
                "Deploy Python and VS Code via Intune managed installer",
                "Grant local admin or developer group permissions if policy allows",
                "Verify tools install and function correctly",
            ),
        ),
    ),
    # ── 016 Salesforce reports timing out ── Enterprise Applications ──
    ScenarioDefinition(
        scenario_id="software-016",
        subjects=(
            "Salesforce reports timing out every time I run them",
            "Salesforce dashboard reports won't load — timeout error",
        ),
        descriptions=(
            "I've been trying to generate the monthly pipeline report in Salesforce"
            " all morning but it keeps timing out after about 2 minutes. The report"
            " has worked fine for the past year. No changes to filters or data range"
            " on my end. Other smaller reports load fine.",
            "Our Salesforce custom report 'Client Revenue YTD' is unusable. It times"
            " out with a 'Report generation timed out' error. The sales ops team"
            " confirmed the data volume increased significantly after last quarter's"
            " import. We need this report for the weekly leadership review tomorrow.",
        ),
        gold=ScenarioGold(
            category="Software & Applications",
            priority="P2",
            assigned_team="Enterprise Applications",
            needs_escalation=False,
            missing_information=("Salesforce report name or ID",),
            next_best_action=("Review report query complexity and optimize filters"),
            remediation_steps=(
                "Identify the specific report and review its filter criteria",
                "Check Salesforce governor limits and report row thresholds",
                "Optimize report by adding date range filters or reducing scope",
                "Consider converting to an async report or scheduled export",
                "Test report performance after optimization",
            ),
        ),
    ),
    # ── 017 Adobe PDF reader crashing ── Endpoint Engineering ──
    ScenarioDefinition(
        scenario_id="software-017",
        subjects=(
            "Adobe Acrobat keeps crashing on certain PDF documents",
            "PDF reader crashes when opening compliance docs",
        ),
        descriptions=(
            "Adobe Acrobat Reader crashes every time I try to open the new compliance"
            " policy PDFs from Legal. Other PDFs open fine. The files are about 25MB"
            " each with embedded forms and digital signatures. I've tried"
            " re-downloading them but same result.",
            "Acrobat is crashing on specific documents sent by our external auditors."
            " These are secured PDFs with form fields. I need to fill them out and"
            " return them by end of week. Version is Acrobat Reader DC 2024.001.",
        ),
        gold=ScenarioGold(
            category="Software & Applications",
            priority="P3",
            assigned_team="Endpoint Engineering",
            needs_escalation=False,
            missing_information=(),
            next_best_action="Update Acrobat Reader and disable Protected Mode",
            remediation_steps=(
                "Update Adobe Acrobat Reader to latest version",
                "Disable Protected Mode temporarily for testing",
                "Clear Acrobat Reader cache and preferences",
                "Test opening the problematic PDFs",
                "If issue persists, try opening in Edge PDF viewer as workaround",
            ),
        ),
    ),
    # ── 018 Teams screen sharing black screen ── Enterprise Applications ──
    ScenarioDefinition(
        scenario_id="software-018",
        subjects=(
            "Teams screen sharing shows black screen to participants",
            "Black screen when I share my screen in Teams meetings",
        ),
        descriptions=(
            "When I share my screen in Teams meetings, other participants only see a"
            " black rectangle. I can see my own screen fine on my end. It happens"
            " whether I share the full screen or a specific window. Audio and video"
            " work normally. This started about a week ago.",
            "Screen sharing in Teams is broken. Attendees tell me they see a solid"
            " black screen. I've tested with multiple meetings and it's consistent."
            " Running Teams on a Dell Latitude with Intel Iris Xe graphics and two"
            " external monitors. Other people on the call can share just fine.",
            "Hi, I'm a manager and I present to my team daily via Teams screen share."
            " For the past week everyone sees black when I share. Restarting Teams"
            " didn't help. Can someone look into this?",
        ),
        gold=ScenarioGold(
            category="Software & Applications",
            priority="P2",
            assigned_team="Enterprise Applications",
            needs_escalation=False,
            missing_information=(),
            next_best_action=("Disable hardware acceleration in Teams and update GPU drivers"),
            remediation_steps=(
                "Disable GPU hardware acceleration in Teams settings",
                "Update Intel graphics drivers to latest version",
                "Clear Teams cache and restart the application",
                "Test screen sharing in a test meeting",
                "If multi-monitor, try sharing with single monitor connected",
            ),
        ),
    ),
    # ── 019 Windows Defender false positive ── Endpoint Engineering ──
    ScenarioDefinition(
        scenario_id="software-019",
        subjects=(
            "Windows Defender blocking our internal risk application",
            "Defender false positive — quarantined our custom app",
            "Security software blocking legitimate business application",
        ),
        descriptions=(
            "Windows Defender just quarantined RiskCalc.exe, which is our internally"
            " developed risk calculation tool used by the entire Risk Analytics team."
            " It flagged it as 'Trojan:Win32/Wacatac.B!ml'. This is a false positive"
            " — the app was built by our dev team and has been in use for two years."
            " 12 people on the team are now unable to work.",
            "Defender is blocking our custom trade reconciliation app. It gets"
            " quarantined immediately after launch. The dev team says the latest build"
            " was compiled yesterday and something in the new code triggered Defender."
            " We need an exclusion ASAP — settlement processing is at risk.",
        ),
        gold=ScenarioGold(
            category="Software & Applications",
            priority="P2",
            assigned_team="Endpoint Engineering",
            needs_escalation=False,
            missing_information=(
                "Application file hash for exclusion whitelisting",
                "Application owner and internal code signing status",
            ),
            next_best_action=("Add temporary Defender exclusion and submit file for false positive review"),
            remediation_steps=(
                "Collect file hash and verify with application development team",
                "Submit sample to Microsoft for false positive analysis",
                "Add temporary exclusion in Defender via Intune policy",
                "Restore quarantined file on affected machines",
                "Coordinate with dev team to code-sign future builds",
            ),
        ),
    ),
    # ── 020 ServiceNow portal extremely slow ── Enterprise Applications ──
    ScenarioDefinition(
        scenario_id="software-020",
        subjects=(
            "ServiceNow portal is painfully slow",
            "IT service portal taking forever to load",
        ),
        descriptions=(
            "The ServiceNow IT service portal has been extremely slow for the past"
            " two days. Pages take 30+ seconds to load and sometimes time out"
            " entirely. I'm trying to submit a ticket (ironic, I know) and the form"
            " takes so long to load that it times out before I can submit. Multiple"
            " colleagues are experiencing the same thing.",
            "ServiceNow is barely functional. Opening a ticket takes several minutes"
            " and the knowledge base search never returns results — just spins. This"
            " is affecting everyone trying to reach IT support. Is there a known"
            " issue?",
        ),
        gold=ScenarioGold(
            category="Software & Applications",
            priority="P2",
            assigned_team="Enterprise Applications",
            needs_escalation=False,
            missing_information=(),
            next_best_action=("Check ServiceNow instance health and performance metrics"),
            remediation_steps=(
                "Review ServiceNow instance performance dashboard",
                "Check for long-running scheduled jobs or background scripts",
                "Verify database and application node resource utilization",
                "Clear instance cache if applicable",
                "Engage ServiceNow vendor support if infrastructure issue",
            ),
        ),
    ),
    # ── 021 App-V virtual app not launching ── Endpoint Engineering ──
    ScenarioDefinition(
        scenario_id="software-021",
        subjects=(
            "App-V application won't launch — stuck on loading",
            "Virtual application from App-V not starting",
        ),
        descriptions=(
            "The App-V packaged version of our legacy portfolio management tool"
            " (PortfolioTracker v3.8) won't launch anymore. It shows 'Loading"
            " virtual environment...' for about a minute then disappears. This"
            " worked yesterday. I'm in the Investment Management group and need"
            " this for daily portfolio reviews.",
            "Can't open PortfolioTracker through App-V. Double-clicking the shortcut"
            " starts the loading animation but it never actually opens. I've rebooted"
            " twice. Other App-V apps seem to work. Running Windows 11 Enterprise.",
        ),
        gold=ScenarioGold(
            category="Software & Applications",
            priority="P2",
            assigned_team="Endpoint Engineering",
            needs_escalation=False,
            missing_information=(),
            next_best_action="Repair App-V client and republish the package",
            remediation_steps=(
                "Check App-V client service status (AppVClient service)",
                "Review App-V client event logs for error details",
                "Reset the specific App-V package via PowerShell",
                "Republish the package from SCCM/Intune if needed",
                "Test application launch after repair",
            ),
        ),
    ),
    # ── 022 Shared Excel workbook locking conflicts ── Enterprise Apps ──
    ScenarioDefinition(
        scenario_id="software-022",
        subjects=(
            "Excel shared workbook keeps locking everyone out",
            "Shared Excel file on SharePoint — constant lock conflicts",
        ),
        descriptions=(
            "We have a shared Excel workbook on SharePoint that our Accounting team"
            " (8 people) uses to track journal entries. People keep getting 'file is"
            " locked for editing by another user' errors even when no one else has it"
            " open. Sometimes the lock shows a user who left the company months ago."
            " Co-authoring is turned on but doesn't seem to work.",
            "Our team's shared budget tracker in SharePoint keeps getting locked."
            " We frequently get messages that someone else is editing when nobody is."
            " We've tried the web version of Excel and it works better but we need"
            " desktop features like pivot tables. This is a daily frustration for"
            " the whole Finance Planning team.",
        ),
        gold=ScenarioGold(
            category="Software & Applications",
            priority="P3",
            assigned_team="Enterprise Applications",
            needs_escalation=False,
            missing_information=("SharePoint site URL and file path",),
            next_best_action="Clear stale locks and verify co-authoring settings",
            remediation_steps=(
                "Check SharePoint file lock status via admin center",
                "Clear any stale locks from disconnected sessions",
                "Verify file format supports co-authoring (.xlsx, not .xls)",
                "Ensure AutoSave and co-authoring are enabled for all users",
                "Move file to a modern document library if on legacy site",
            ),
        ),
    ),
    # ── 023 OneDrive client not syncing ── Endpoint Engineering ──
    ScenarioDefinition(
        scenario_id="software-023",
        subjects=(
            "OneDrive not syncing — files stuck with pending icon",
            "OneDrive sync has stopped working completely",
            "OneDrive shows sync errors on multiple files",
        ),
        descriptions=(
            "My OneDrive client stopped syncing about two days ago. All files show a"
            " blue circular arrow icon that never resolves. I've tried pausing and"
            " resuming sync, signing out and back in, and restarting my laptop."
            " Nothing works. I'm worried about losing recent work that only exists"
            " locally right now.",
            "OneDrive sync is broken. The system tray icon shows a red X and when"
            " I click it there are 47 files with sync errors. Most say 'We couldn't"
            " merge the changes in this file'. I'm in Wealth Management and these"
            " are client proposal documents I've been editing offline.",
        ),
        gold=ScenarioGold(
            category="Software & Applications",
            priority="P2",
            assigned_team="Endpoint Engineering",
            needs_escalation=False,
            missing_information=(),
            next_best_action="Reset OneDrive client and resolve sync conflicts",
            remediation_steps=(
                "Check OneDrive sync status and identify specific errors",
                "Back up any locally modified files not yet synced",
                "Reset OneDrive client via onedrive.exe /reset command",
                "Re-link OneDrive account and allow full resync",
                "Resolve any remaining file conflicts manually",
            ),
        ),
    ),
    # ── 024 Zoom not available — need for external call ── Endpoint Eng ──
    ScenarioDefinition(
        scenario_id="software-024",
        subjects=(
            "Need Zoom installed for client meeting tomorrow",
            "Zoom request — external client requires it",
        ),
        descriptions=(
            "I have a meeting with an external client (JPMorgan's risk team) tomorrow"
            " at 2pm and they insist on using Zoom. We don't have Zoom installed and"
            " it's not in Company Portal. I know we're a Teams shop but I really need"
            " this for the client relationship. Can IT approve and install it quickly?",
            "Requesting Zoom desktop client install. Our partner firm only uses Zoom"
            " for video conferences and we have a joint project kickoff on Wednesday."
            " I tried the web version but our firewall seems to block it. My manager"
            " David Park has approved. Machine: LAP-8892.",
            "Hi, is it possible to get Zoom installed? I've got external meetings"
            " where clients use Zoom and joining via browser doesn't work well. I keep"
            " having audio issues on the web client. Need the desktop app.",
        ),
        gold=ScenarioGold(
            category="Software & Applications",
            priority="P3",
            assigned_team="Endpoint Engineering",
            needs_escalation=False,
            missing_information=(
                "Manager approval for non-standard software",
                "Business justification documentation",
            ),
            next_best_action=("Process non-standard software request with manager approval"),
            remediation_steps=(
                "Verify manager approval for Zoom installation",
                "Check Zoom licensing requirements and corporate policy",
                "Deploy Zoom client via Intune if approved",
                "Configure Zoom with enterprise security settings",
                "Verify Zoom connectivity through corporate firewall",
            ),
        ),
    ),
    # ── 025 Power BI report failing to refresh ── Enterprise Applications ──
    ScenarioDefinition(
        scenario_id="software-025",
        subjects=(
            "Power BI report refresh failing — data gateway error",
            "Power BI dashboard not updating — refresh errors",
        ),
        descriptions=(
            "Our executive finance dashboard in Power BI Service has been failing to"
            " refresh since Monday morning. The error says 'Data source error: The"
            " on-premises data gateway is unreachable.' This report pulls from our"
            " SQL data warehouse and refreshes every 4 hours. Leadership relies on"
            " this for daily decision-making.",
            "Power BI scheduled refresh is broken for three of our team's reports."
            " All of them connect through the on-prem data gateway to our finance"
            " database. Getting 'Gateway unreachable' errors. Last successful refresh"
            " was Friday at 11pm. The CFO's weekly dashboard is stale.",
        ),
        gold=ScenarioGold(
            category="Software & Applications",
            priority="P2",
            assigned_team="Enterprise Applications",
            needs_escalation=False,
            missing_information=(),
            next_best_action=("Check on-premises data gateway service status and connectivity"),
            remediation_steps=(
                "Verify the on-premises data gateway service is running",
                "Check gateway machine resource utilization and connectivity",
                "Review gateway logs for connection errors to data source",
                "Restart the gateway service if it is unresponsive",
                "Trigger a manual refresh to confirm restoration",
            ),
        ),
    ),
    # ── 026 Edge enterprise policies not applying ── Endpoint Engineering ──
    ScenarioDefinition(
        scenario_id="software-026",
        subjects=(
            "Microsoft Edge enterprise policies not applying to my machine",
            "Edge missing company bookmarks and homepage policy",
        ),
        descriptions=(
            "My Edge browser doesn't have any of the company-configured policies."
            " No managed bookmarks bar, no corporate homepage, and I can install"
            " extensions freely (which I know should be restricted). Colleagues"
            " on the same floor have all the policies applied. I think my machine"
            " might have missed a policy push. Running Edge 120 on Windows 11.",
            "Edge on my laptop seems unmanaged. When I go to edge://policy it shows"
            " zero policies applied. Other machines in my department show dozens of"
            " managed policies. I re-enrolled in Intune last week after a profile"
            " issue — maybe the Edge policies didn't come back?",
        ),
        gold=ScenarioGold(
            category="Software & Applications",
            priority="P3",
            assigned_team="Endpoint Engineering",
            needs_escalation=False,
            missing_information=(),
            next_best_action=("Force Intune policy sync and verify Edge policy assignment"),
            remediation_steps=(
                "Check Intune device compliance and policy assignment status",
                "Force an Intune policy sync on the device",
                "Verify Edge ADMX policies are targeting correct device group",
                "Check local Group Policy (gpresult /h) for Edge settings",
                "Restart Edge and verify policies appear in edge://policy",
            ),
        ),
    ),
    # ── 027 Java runtime version conflict ── Endpoint Engineering ──
    ScenarioDefinition(
        scenario_id="software-027",
        subjects=(
            "Java version conflict breaking our legacy trading app",
            "Need older Java runtime for internal application",
        ),
        descriptions=(
            "Our legacy trade settlement application (TradeSettle v2.1) requires Java"
            " 8 but the recent Intune update pushed Java 17 and removed Java 8."
            " Now TradeSettle won't start and throws a ClassNotFoundException. The"
            " Operations team (6 people) can't process settlements. We need Java 8"
            " restored alongside Java 17.",
            "The Java update broke our internal app. We need Java 8 Update 381"
            " specifically — the new Java 17 that was pushed is incompatible. The app"
            " is called TradeSettle and it's critical for daily settlement operations."
            " Can we get both versions installed side by side?",
        ),
        gold=ScenarioGold(
            category="Software & Applications",
            priority="P2",
            assigned_team="Endpoint Engineering",
            needs_escalation=False,
            missing_information=(),
            next_best_action=("Install Java 8 alongside Java 17 and configure app path"),
            remediation_steps=(
                "Deploy Java 8 JRE alongside Java 17 via Intune",
                "Configure TradeSettle shortcut to use Java 8 path explicitly",
                "Set JAVA_HOME environment variable for the application",
                "Verify TradeSettle launches successfully",
                "Add Java 8 exception to future update policies for these users",
            ),
        ),
    ),
    # ── 028 Teams meeting recording not appearing ── Enterprise Apps ──
    ScenarioDefinition(
        scenario_id="software-028",
        subjects=(
            "Teams meeting recording missing — not showing up anywhere",
            "Where is my Teams recording? Can't find it in chat or SharePoint",
        ),
        descriptions=(
            "I recorded an important client meeting in Teams yesterday (2pm-3:30pm)"
            " but the recording never appeared. Normally it shows up in the meeting"
            " chat within a few minutes. I've checked OneDrive, SharePoint, and the"
            " meeting chat — nothing. The meeting had about 15 attendees including"
            " external guests. I really need this recording.",
            "Recorded a Teams meeting this morning and got the notification that"
            " recording started and stopped, but the file is nowhere to be found."
            " Not in the chat, not in my OneDrive recordings folder, not in Stream."
            " The meeting was organized by my colleague — does it go to their"
            " OneDrive instead?",
        ),
        gold=ScenarioGold(
            category="Software & Applications",
            priority="P3",
            assigned_team="Enterprise Applications",
            needs_escalation=False,
            missing_information=(
                "Meeting date, time, and organizer",
                "Whether meeting was a channel meeting or private meeting",
            ),
            next_best_action=("Check recording storage location based on meeting type"),
            remediation_steps=(
                "Determine if meeting was channel-based (SharePoint) or private (OneDrive)",
                "Check organizer's OneDrive for recording file",
                "Review Teams admin center for recording processing status",
                "Check if recording policy allows recording for the user",
                "If recording is lost, escalate to Microsoft support with meeting ID",
            ),
        ),
    ),
    # ── 029 Windows activation error after HW swap ── Endpoint Engineering ──
    ScenarioDefinition(
        scenario_id="software-029",
        subjects=(
            "Windows activation error after motherboard replacement",
            "Windows says 'not activated' since hardware repair",
        ),
        descriptions=(
            "My laptop had a motherboard replacement last week (done by your hardware"
            " team — ticket INC0045891). Now Windows shows 'Windows is not activated'"
            " in Settings and there's a watermark on the desktop. I assume the"
            " hardware change triggered a reactivation requirement. Everything else"
            " works fine but the watermark is distracting and I'm worried about"
            " functionality restrictions.",
            "After getting my laptop back from hardware repair, Windows is showing an"
            " activation error. Error code: 0xC004F012. The activation troubleshooter"
            " says to contact the organization's support. Asset tag: LAP-3367.",
        ),
        gold=ScenarioGold(
            category="Software & Applications",
            priority="P3",
            assigned_team="Endpoint Engineering",
            needs_escalation=False,
            missing_information=(),
            next_best_action=("Reactivate Windows license via KMS or VAMT after hardware change"),
            remediation_steps=(
                "Connect device to corporate network for KMS activation",
                "Run slmgr /ato to force activation attempt",
                "If KMS fails, reactivate using VAMT or MAK key",
                "Verify activation status shows 'Windows is activated'",
                "Clear activation watermark by restarting Explorer",
            ),
        ),
    ),
    # ── 030 SAP batch job failing nightly ── Enterprise Apps (P1, escalation) ──
    ScenarioDefinition(
        scenario_id="software-030",
        subjects=(
            "URGENT: SAP nightly batch job failing — finance reports impacted",
            "SAP batch job FINRPT_DAILY failing since Tuesday",
            "Critical SAP job failure affecting daily finance reporting",
        ),
        descriptions=(
            "The SAP batch job FINRPT_DAILY has been failing every night since Tuesday"
            " with ABAP runtime error MESSAGE_TYPE_X. This job generates the daily"
            " P&L and balance sheet reports that the CFO's office and regulatory"
            " reporting team depend on. We are now three days behind on financial"
            " reporting and the external auditors are asking questions. The Basis team"
            " looked at it but couldn't resolve. This needs immediate senior attention.",
            "Critical issue: our nightly SAP finance batch job hasn't completed"
            " successfully in 3 days. Job name: FINRPT_DAILY, client 100, PRD system."
            " The dump shows a data overflow in the consolidation step. This is"
            " impacting downstream reporting for the entire Finance division and we"
            " have regulatory deadlines. Please escalate to SAP SME team immediately.",
        ),
        gold=ScenarioGold(
            category="Software & Applications",
            priority="P1",
            assigned_team="Enterprise Applications",
            needs_escalation=True,
            missing_information=(),
            next_best_action=("Escalate to SAP Basis and ABAP team for runtime dump analysis"),
            remediation_steps=(
                "Pull ABAP runtime dump (ST22) for the failed job executions",
                "Analyze the MESSAGE_TYPE_X dump for root cause",
                "Check for recent SAP transport imports that may have caused regression",
                "Engage SAP Basis team to review job scheduling and dependencies",
                "Apply fix and execute manual job run to clear backlog",
                "Verify downstream reports generate successfully",
                "Notify Finance and regulatory reporting teams of resolution",
            ),
        ),
    ),
]
