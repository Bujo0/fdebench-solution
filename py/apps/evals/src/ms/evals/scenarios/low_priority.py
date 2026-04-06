# Copyright (c) Microsoft. All rights reserved.
"""Low-priority (P4) scenario templates across all categories.

Covers: cosmetic issues, minor inconveniences, feature requests,
nice-to-have improvements, informational questions, and low-impact
issues that don't affect productivity.
"""

from ms.evals.constants import Category
from ms.evals.constants import MissingInfo
from ms.evals.constants import Priority
from ms.evals.constants import Team
from ms.evals.models import ScenarioTemplate
from ms.evals.scenarios.registry import register

# ---------------------------------------------------------------------------
# Access & Authentication — P4
# ---------------------------------------------------------------------------

register(
    ScenarioTemplate(
        scenario_id="lp-001",
        category=Category.ACCESS_AUTH,
        priority=Priority.P4,
        assigned_team=Team.IAM,
        needs_escalation=False,
        missing_information=[MissingInfo.CONTACT_INFO],
        subjects=[
            "Request to change my display name in Active Directory",
            "Can someone update my AD display name when you get a chance?",
            "Display name change request — no rush",
        ],
        descriptions=[
            "Hey team, I recently got married and changed my last name. Could someone "
            "update my display name in Active Directory to reflect the new one? It currently "
            "shows my maiden name in the GAL and on Teams. No rush at all — just whenever "
            "you have a spare moment.",
            "I'd like to request a display name change in AD. My name currently shows as "
            "{name} but I go by a different spelling now. It's purely cosmetic — everything "
            "still works fine, just looks odd in the address book.",
        ],
        next_best_actions=[
            "Verify the requested name change with HR records and update the displayName "
            "attribute in Active Directory. Allow up to 24 hours for GAL sync.",
            "Confirm the user's identity and the new display name, then update AD and "
            "wait for the next directory sync cycle to propagate the change.",
        ],
        remediation_steps=[
            [
                "Verify the name change request against HR records",
                "Update the displayName attribute in Active Directory",
                "Trigger a directory sync or wait for the next scheduled cycle",
                "Confirm the change is reflected in the GAL and Teams",
            ],
            [
                "Cross-reference the request with the HR system",
                "Update the display name in Entra ID / on-prem AD as appropriate",
                "Notify the user once the change has propagated",
            ],
        ],
    )
)

register(
    ScenarioTemplate(
        scenario_id="lp-002",
        category=Category.ACCESS_AUTH,
        priority=Priority.P4,
        assigned_team=Team.IAM,
        needs_escalation=False,
        missing_information=[MissingInfo.CONTACT_INFO, MissingInfo.CONFIGURATION_DETAILS],
        subjects=[
            "Want to add a second email alias to my account",
            "Can I get an additional email alias? No urgency",
            "Request for secondary email alias on my mailbox",
        ],
        descriptions=[
            "Hi, I work across two teams and it would be handy to have a second email "
            "alias — something like {name}@contoso.com in addition to my current address. "
            "People from the {department} team keep misspelling my name. Totally low "
            "priority, just a nice-to-have.",
            "Could I get an additional email alias added to my Exchange mailbox? I'd like "
            "to have a shorter version of my name as an alias. No rush — my current "
            "address works fine, this is purely for convenience.",
        ],
        next_best_actions=[
            "Check the alias against existing mailboxes for conflicts, then add the "
            "proxyAddress in Exchange Online via the admin center.",
            "Verify the requested alias is available and complies with naming policy, "
            "then add it as a secondary SMTP address in Exchange.",
        ],
        remediation_steps=[
            [
                "Verify the requested alias doesn't conflict with existing addresses",
                "Add the alias as a proxyAddress in Exchange Online admin center",
                "Confirm the user can receive mail at the new alias",
            ],
            [
                "Check naming policy compliance for the requested alias",
                "Add the secondary SMTP address via PowerShell or Exchange admin",
                "Send a test email to the new alias and verify delivery",
            ],
        ],
    )
)

register(
    ScenarioTemplate(
        scenario_id="lp-003",
        category=Category.ACCESS_AUTH,
        priority=Priority.P4,
        assigned_team=Team.IAM,
        needs_escalation=False,
        missing_information=[MissingInfo.BUSINESS_IMPACT],
        subjects=[
            "Request for access to a SharePoint site — not urgent",
            "Can I get added to the {department} SharePoint? No rush",
            "Low-priority SharePoint access request",
        ],
        descriptions=[
            "Hi, I heard the {department} team has some useful reference docs on their "
            "SharePoint site. Could I get read access when someone has a chance? It's not "
            "blocking any of my work — just want to browse their templates for ideas.",
            "I'd like access to the {department} SharePoint site for reference purposes. "
            "A colleague mentioned they have some great process documents there. Totally "
            "low priority — whenever the site owner can approve it is fine.",
        ],
        next_best_actions=[
            "Forward the request to the SharePoint site owner for approval. Once approved, "
            "add the user to the appropriate access group.",
            "Verify the user's justification and route the access request to the site "
            "collection administrator for review.",
        ],
        remediation_steps=[
            [
                "Identify the SharePoint site owner or collection admin",
                "Request approval for the user's read access",
                "Add the user to the site members or visitors group once approved",
                "Notify the user that access has been granted",
            ],
            [
                "Route the access request through the standard approval workflow",
                "Once approved, grant the appropriate permission level",
                "Confirm the user can access the site",
            ],
        ],
    )
)

register(
    ScenarioTemplate(
        scenario_id="lp-004",
        category=Category.ACCESS_AUTH,
        priority=Priority.P4,
        assigned_team=Team.IAM,
        needs_escalation=False,
        missing_information=[MissingInfo.AFFECTED_USERS],
        subjects=[
            "Distribution list update — add/remove a few members",
            "Please update the {department} distribution list when you can",
            "DL membership change request — no rush",
        ],
        descriptions=[
            "Hi, could someone update the {department}-all distribution list? We need to "
            "add {name} and remove two people who transferred to another team last month. "
            "No hurry — the next team email blast isn't until end of the quarter.",
            "Requesting a few changes to our team distribution list. A couple of new hires "
            "need to be added and some former members removed. Not urgent at all — "
            "whenever you get to it is perfectly fine.",
        ],
        next_best_actions=[
            "Get the full list of members to add and remove, then update the distribution "
            "group membership in Exchange Online.",
            "Confirm the membership changes with the DL owner and apply the updates in the Exchange admin center.",
        ],
        remediation_steps=[
            [
                "Confirm the list of members to add and remove with the requestor",
                "Update the distribution group membership in Exchange Online",
                "Notify the requestor that the changes are complete",
            ],
            [
                "Verify the DL owner has authorized the changes",
                "Add and remove members via the Exchange admin center or PowerShell",
                "Send a confirmation email to the requestor",
            ],
        ],
    )
)

register(
    ScenarioTemplate(
        scenario_id="lp-005",
        category=Category.ACCESS_AUTH,
        priority=Priority.P4,
        assigned_team=Team.IAM,
        needs_escalation=False,
        missing_information=[MissingInfo.ENVIRONMENT_DETAILS, MissingInfo.DEVICE_INFO],
        subjects=[
            "Request to change my default login domain",
            "Can I change the domain shown on my login screen?",
            "Default sign-in domain preference change",
        ],
        descriptions=[
            "When I log in to my laptop, it defaults to the old contoso-legacy domain "
            "and I always have to manually switch to contoso.com. Could someone change "
            "the default? Not a big deal — just a minor annoyance every morning.",
            "My workstation still shows the old domain suffix on the login screen. I know "
            "I can type in the full UPN, but it'd be nice if it defaulted to the right "
            "one. Low priority — just a quality-of-life thing.",
        ],
        next_best_actions=[
            "Check the device's domain join configuration and update the default logon "
            "domain via Group Policy or registry setting.",
            "Verify which domain the machine is joined to and adjust the DefaultDomainName "
            "registry key or applicable GPO.",
        ],
        remediation_steps=[
            [
                "Check the device's current domain join status and GPO assignments",
                "Update the DefaultDomainName registry key or apply the correct GPO",
                "Have the user log out and back in to verify the change",
            ],
            [
                "Review the applicable Group Policy for default logon domain settings",
                "Apply the correct configuration to the user's device",
                "Confirm the default domain is correct on next login",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# Hardware & Peripherals — P4
# ---------------------------------------------------------------------------

register(
    ScenarioTemplate(
        scenario_id="lp-006",
        category=Category.HARDWARE,
        priority=Priority.P4,
        assigned_team=Team.ENDPOINT,
        needs_escalation=False,
        missing_information=[MissingInfo.DEVICE_INFO],
        subjects=[
            "Mouse scroll wheel is slightly sticky",
            "Scroll wheel on my mouse feels a bit off",
            "Minor mouse issue — scroll wheel not smooth",
        ],
        descriptions=[
            "The scroll wheel on my company mouse has gotten a bit sticky. It still works "
            "fine for the most part, just feels gritty when scrolling. I've had it for "
            "about two years so it might just be wear and tear. Not urgent at all.",
            "My mouse scroll wheel doesn't feel as smooth as it used to — it kind of "
            "catches every few scrolls. It's a minor annoyance but everything still "
            "functions. Whenever there's a spare mouse available, I'd appreciate a swap.",
        ],
        next_best_actions=[
            "Check spare peripheral inventory and arrange a replacement mouse at the "
            "user's convenience during their next office visit.",
            "Add the user to the next batch of peripheral refreshes or ship a replacement mouse if available in stock.",
        ],
        remediation_steps=[
            [
                "Check peripheral inventory for available replacement mice",
                "Arrange a swap at the user's convenience",
                "Collect the old mouse for recycling or cleaning",
            ],
            [
                "Add the request to the peripheral refresh queue",
                "Ship or deliver a replacement mouse when available",
                "Update the asset inventory record",
            ],
        ],
    )
)

register(
    ScenarioTemplate(
        scenario_id="lp-007",
        category=Category.HARDWARE,
        priority=Priority.P4,
        assigned_team=Team.ENDPOINT,
        needs_escalation=False,
        missing_information=[MissingInfo.DEVICE_INFO, MissingInfo.SCREENSHOT_OR_ATTACHMENT],
        subjects=[
            "Laptop keyboard key cap is loose but still works",
            "Key cap coming off my laptop — still functional though",
            "Minor keyboard issue — loose key on my laptop",
        ],
        descriptions=[
            "The 'B' key on my laptop keyboard is a bit loose — the cap wiggles but it "
            "still registers every press. I think the little clip underneath is partially "
            "broken. It's not affecting my work, just mildly annoying. No rush on this.",
            "One of the keys on my laptop keyboard is loose and rocks side to side. "
            "Haven't lost it yet and it still types fine. If there's a spare key cap or "
            "a keyboard replacement in stock, I'd appreciate it whenever convenient.",
        ],
        next_best_actions=[
            "Check if a replacement key cap or keyboard assembly is available for the "
            "user's laptop model. Schedule a repair at their convenience.",
            "Order a replacement keyboard or key cap kit for the specific laptop model "
            "and schedule the repair during the user's next docking station visit.",
        ],
        remediation_steps=[
            [
                "Identify the laptop model and check for replacement key caps in stock",
                "Schedule a keyboard repair or replacement at the user's convenience",
                "Verify the fix and update the asset maintenance log",
            ],
            [
                "Order the correct replacement keyboard for the laptop model",
                "Schedule a technician visit or drop-off repair",
                "Test the replacement and return the device to the user",
            ],
        ],
    )
)

register(
    ScenarioTemplate(
        scenario_id="lp-008",
        category=Category.HARDWARE,
        priority=Priority.P4,
        assigned_team=Team.ENDPOINT,
        needs_escalation=False,
        missing_information=[MissingInfo.CONFIGURATION_DETAILS, MissingInfo.BUSINESS_IMPACT],
        subjects=[
            "Request for an extra monitor arm",
            "Can I get a monitor arm for my desk setup?",
            "Monitor arm request — ergonomic improvement",
        ],
        descriptions=[
            "Hi, I'd like to request a monitor arm for my desk on {floor}. My monitors "
            "take up a lot of desk space and I think an arm would help with ergonomics "
            "too. No urgency at all — just putting in the request for whenever the next "
            "order goes through.",
            "Could I get a monitor arm added to my workstation? I've seen other desks "
            "with them and they look great for posture. My current setup works fine, "
            "this is purely a nice-to-have ergonomic improvement.",
        ],
        next_best_actions=[
            "Add the request to the next peripheral/ergonomic equipment order batch. "
            "Confirm desk compatibility for the monitor arm mounting type.",
            "Check current ergonomic equipment inventory and add the user to the "
            "request queue for the next procurement cycle.",
        ],
        remediation_steps=[
            [
                "Confirm the desk type supports clamp or grommet mount arms",
                "Add the request to the next ergonomic equipment order",
                "Schedule installation once the arm arrives",
            ],
            [
                "Check if monitor arms are available in the office supply inventory",
                "Order if needed and schedule delivery to the user's desk",
                "Arrange installation and verify the setup is stable",
            ],
        ],
    )
)

register(
    ScenarioTemplate(
        scenario_id="lp-009",
        category=Category.HARDWARE,
        priority=Priority.P4,
        assigned_team=Team.ENDPOINT,
        needs_escalation=False,
        missing_information=[MissingInfo.DEVICE_INFO, MissingInfo.REPRODUCTION_FREQUENCY],
        subjects=[
            "Laptop fan occasionally makes a quiet clicking sound",
            "Minor fan noise on my laptop — not constant",
            "Laptop fan clicking intermittently — still works fine",
        ],
        descriptions=[
            "My laptop fan makes a faint clicking noise every now and then, usually when "
            "it first spins up. It goes away after a few seconds and the laptop runs "
            "fine otherwise — no overheating or performance issues. Just figured I'd "
            "mention it in case it gets worse down the road.",
            "There's a slight clicking from my laptop fan that happens maybe once or "
            "twice a day. It's very quiet and lasts only a couple of seconds. Everything "
            "else is normal. Not urgent — just logging it for tracking purposes.",
        ],
        next_best_actions=[
            "Log the issue for tracking. If the laptop is still under warranty, note it "
            "for the next scheduled hardware maintenance cycle.",
            "Document the symptom and check the device's warranty status. Schedule a "
            "fan inspection during the next planned maintenance window.",
        ],
        remediation_steps=[
            [
                "Log the report and check the laptop's warranty and age",
                "Schedule a fan inspection during the next maintenance window",
                "Replace the fan assembly if the noise worsens",
            ],
            [
                "Run remote hardware diagnostics to check fan health",
                "If diagnostics are clean, monitor and revisit if symptoms worsen",
                "Schedule a proactive fan replacement if under warranty",
            ],
        ],
    )
)

register(
    ScenarioTemplate(
        scenario_id="lp-010",
        category=Category.HARDWARE,
        priority=Priority.P4,
        assigned_team=Team.ENDPOINT,
        needs_escalation=False,
        missing_information=[MissingInfo.DEVICE_INFO, MissingInfo.BUSINESS_IMPACT],
        subjects=[
            "Request for a USB-A to USB-C adapter",
            "Need a USB adapter for my personal device — low priority",
            "USB-A to USB-C dongle request",
        ],
        descriptions=[
            "My personal phone uses USB-C but my docking station only has USB-A ports. "
            "Could I get a small adapter so I can charge my phone at my desk? Totally "
            "optional — I have a charger at home, this is just for convenience.",
            "Hi, I'd like to request a USB-A to USB-C adapter. I know it's for my "
            "personal device so no worries if this isn't something IT provides. Just "
            "thought I'd ask. No rush either way.",
        ],
        next_best_actions=[
            "Check if personal device accessories fall within the IT provisioning policy. "
            "If approved, add a USB adapter to the next supply order.",
            "Review the peripheral request policy for personal device accessories and "
            "respond to the user with the appropriate guidance.",
        ],
        remediation_steps=[
            [
                "Check IT policy on personal device accessory provisioning",
                "If within policy, add the adapter to the next supply order",
                "Notify the user of the outcome and expected delivery",
            ],
            [
                "Verify whether the request qualifies under the equipment policy",
                "If approved, ship or distribute the adapter from stock",
                "If not covered, inform the user and suggest alternatives",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# Network & Connectivity — P4
# ---------------------------------------------------------------------------

register(
    ScenarioTemplate(
        scenario_id="lp-011",
        category=Category.NETWORK,
        priority=Priority.P4,
        assigned_team=Team.NETWORK,
        needs_escalation=False,
        missing_information=[MissingInfo.NETWORK_LOCATION],
        subjects=[
            "WiFi signal weak in the break room",
            "Poor WiFi coverage in the kitchen / break area",
            "Weak wireless signal in non-work area on {floor}",
        ],
        descriptions=[
            "The WiFi signal in the break room on {floor} is pretty weak. I can barely "
            "load anything on my phone during lunch. I know it's not a work area, but it "
            "would be nice to have decent coverage there. Just a suggestion — no rush.",
            "Heads up that the wireless coverage in the kitchen area on {floor} is "
            "spotty. Not a work-critical area so no urgency, but a lot of people eat "
            "lunch there and it'd be great to have better signal.",
        ],
        next_best_actions=[
            "Log the coverage gap and include it in the next wireless site survey. "
            "Prioritize based on foot traffic and business impact.",
            "Note the location for the next scheduled AP coverage assessment. Non-work "
            "areas are lower priority but can be addressed during planned expansions.",
        ],
        remediation_steps=[
            [
                "Log the coverage gap with the specific floor and area details",
                "Include the area in the next scheduled wireless site survey",
                "If justified by foot traffic, plan an AP installation",
            ],
            [
                "Conduct a quick signal strength check in the reported area",
                "Add the location to the wireless improvement backlog",
                "Address during the next planned network maintenance window",
            ],
        ],
    )
)

register(
    ScenarioTemplate(
        scenario_id="lp-012",
        category=Category.NETWORK,
        priority=Priority.P4,
        assigned_team=Team.NETWORK,
        needs_escalation=False,
        missing_information=[MissingInfo.CONTACT_INFO, MissingInfo.TIMESTAMP],
        subjects=[
            "Guest WiFi password for a visiting family member",
            "Can I get guest WiFi access for a visitor this week?",
            "Request for guest wireless access — personal visitor",
        ],
        descriptions=[
            "My spouse is visiting the office on {date} and I was wondering if I could "
            "get a guest WiFi password for them. They just need internet access for a few "
            "hours while they wait in the lobby. Totally understand if this isn't something "
            "we do — just asking.",
            "Hi, I have a family member coming by the office next week and it would be "
            "great if they could connect to the guest WiFi. Is there a standard process "
            "for getting a temporary guest password? No rush on this.",
        ],
        next_best_actions=[
            "Provide the standard guest WiFi access procedure. If guest access requires "
            "sponsorship, guide the user through the registration portal.",
            "Share the guest wireless onboarding instructions and any visitor registration requirements with the user.",
        ],
        remediation_steps=[
            [
                "Check the guest WiFi access policy for personal visitors",
                "If permitted, generate a temporary guest access code",
                "Provide the credentials and usage guidelines to the user",
            ],
            [
                "Direct the user to the guest WiFi registration portal",
                "Ensure the visitor's access is time-limited per policy",
                "Confirm the access code works before the visit date",
            ],
        ],
    )
)

register(
    ScenarioTemplate(
        scenario_id="lp-013",
        category=Category.NETWORK,
        priority=Priority.P4,
        assigned_team=Team.NETWORK,
        needs_escalation=False,
        missing_information=[MissingInfo.NETWORK_LOCATION, MissingInfo.TIMESTAMP],
        subjects=[
            "Minor latency on the intranet site — still functional",
            "Intranet pages loading a bit slow but working",
            "Slight lag when accessing the company intranet",
        ],
        descriptions=[
            "The intranet site has been a bit sluggish lately — pages take maybe 3-4 "
            "seconds to load instead of the usual 1-2. Everything still works, it's just "
            "noticeably slower. I'm on {floor} connected via ethernet. Not blocking "
            "anything, just thought I'd flag it.",
            "I've noticed the company intranet feels a touch slower than usual. Not a "
            "big deal — all pages load eventually. Might just be my perception. If "
            "others report the same, it might be worth looking into.",
        ],
        next_best_actions=[
            "Check intranet server performance metrics and recent deployment changes. "
            "If isolated to one user, verify their network path.",
            "Review web server response times and check if there have been recent "
            "content or infrastructure changes to the intranet.",
        ],
        remediation_steps=[
            [
                "Check intranet server performance dashboards for anomalies",
                "Verify if other users report similar slowness",
                "If widespread, investigate CDN or server-side caching",
                "If isolated, check the user's network path and DNS resolution",
            ],
            [
                "Review recent intranet deployments or content changes",
                "Run a traceroute from the user's subnet to the intranet server",
                "Log for monitoring and revisit if performance degrades further",
            ],
        ],
    )
)

register(
    ScenarioTemplate(
        scenario_id="lp-014",
        category=Category.NETWORK,
        priority=Priority.P4,
        assigned_team=Team.NETWORK,
        needs_escalation=False,
        missing_information=[MissingInfo.CONFIGURATION_DETAILS, MissingInfo.DEVICE_INFO],
        subjects=[
            "Network drive letter preference change request",
            "Can I remap my network drive to a different letter?",
            "Request to change mapped drive letter",
        ],
        descriptions=[
            "My network drive is mapped to H: but I'd prefer it on N: since that's "
            "what I was used to at my previous company. I know it's a trivial thing — "
            "everything works fine on H:. Just a personal preference if it's easy to do.",
            "Is it possible to change which drive letter my shared network folder maps "
            "to? Currently it's on {app}: but I keep accidentally navigating to the "
            "wrong drive. Low priority — just a convenience thing.",
        ],
        next_best_actions=[
            "Check if the drive mapping is controlled by Group Policy or a login script. "
            "If user-configurable, provide instructions for self-service remapping.",
            "Determine whether the drive mapping is centrally managed and advise the "
            "user on how to change it if permitted by policy.",
        ],
        remediation_steps=[
            [
                "Check if the drive mapping is enforced via GPO or login script",
                "If user-configurable, provide net use commands or instructions",
                "If GPO-managed, evaluate whether an exception is feasible",
            ],
            [
                "Review the user's login script or GPO drive mappings",
                "Provide self-service instructions if the mapping allows changes",
                "Document the preference for future workstation setups",
            ],
        ],
    )
)

register(
    ScenarioTemplate(
        scenario_id="lp-015",
        category=Category.NETWORK,
        priority=Priority.P4,
        assigned_team=Team.NETWORK,
        needs_escalation=False,
        missing_information=[MissingInfo.BUSINESS_IMPACT, MissingInfo.CONFIGURATION_DETAILS],
        subjects=[
            "Request to whitelist a personal website on the proxy",
            "Can a website be unblocked on the corporate proxy?",
            "Proxy whitelist request for a non-work site",
        ],
        descriptions=[
            "There's a personal finance site I use during lunch breaks that's blocked "
            "by the corporate proxy. I totally get if this isn't something IT does, but "
            "I figured I'd ask. The site is completely legitimate — just a budgeting tool. "
            "No urgency whatsoever.",
            "Hi, a website I occasionally visit for personal learning is blocked by "
            "the web filter. I understand the security reasons but was hoping it might "
            "be possible to get it whitelisted. Happy to provide the URL if needed. "
            "This is really low priority.",
        ],
        next_best_actions=[
            "Review the web filtering policy for personal site exceptions. Request the "
            "specific URL and evaluate it against the acceptable use policy.",
            "Collect the URL from the user and run it through the URL categorization "
            "tool. Determine if it qualifies for an exception under current policy.",
        ],
        remediation_steps=[
            [
                "Collect the specific URL from the user",
                "Check the site categorization in the web filter platform",
                "Evaluate against the acceptable use policy",
                "If approved, add an exception; if denied, communicate the reason",
            ],
            [
                "Review the URL category and reputation score",
                "Check the proxy exception policy for personal use sites",
                "Respond to the user with the decision and rationale",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# Software & Applications — P4
# ---------------------------------------------------------------------------

register(
    ScenarioTemplate(
        scenario_id="lp-016",
        category=Category.SOFTWARE,
        priority=Priority.P4,
        assigned_team=Team.ENTERPRISE_APPS,
        needs_escalation=False,
        missing_information=[
            MissingInfo.APPLICATION_VERSION,
            MissingInfo.SCREENSHOT_OR_ATTACHMENT,
        ],
        subjects=[
            "Outlook dark mode icons slightly off",
            "Cosmetic issue with Outlook dark mode rendering",
            "Minor display glitch in Outlook dark theme",
        ],
        descriptions=[
            "Ever since the last Outlook update, some of the toolbar icons in dark mode "
            "look slightly washed out — like the contrast isn't quite right. Everything "
            "works perfectly, it's purely a visual thing. Just thought I'd report it in "
            "case others notice too.",
            "The dark mode theme in Outlook has a minor rendering issue where a few icons "
            "blend into the background. It doesn't affect functionality at all. Running "
            "{os} with the latest Office updates. Super low priority.",
        ],
        next_best_actions=[
            "Check if this is a known issue in the current Outlook build. If so, note "
            "the tracking ID. If not, log it for the next update cycle.",
            "Verify the Outlook version and check the Microsoft 365 known issues list for dark mode rendering bugs.",
        ],
        remediation_steps=[
            [
                "Confirm the Outlook version and build number",
                "Check the Microsoft 365 admin center for known rendering issues",
                "If a fix is available, push the update; otherwise log for tracking",
            ],
            [
                "Verify the issue is reproducible and note the specific icons affected",
                "Report to Microsoft via the feedback channel if not already known",
                "Inform the user that cosmetic fixes are typically addressed in monthly updates",
            ],
        ],
    )
)

register(
    ScenarioTemplate(
        scenario_id="lp-017",
        category=Category.SOFTWARE,
        priority=Priority.P4,
        assigned_team=Team.ENTERPRISE_APPS,
        needs_escalation=False,
        missing_information=[MissingInfo.APPLICATION_VERSION, MissingInfo.BUSINESS_IMPACT],
        subjects=[
            "Request to install an optional browser extension",
            "Can I get a browser extension approved and installed?",
            "Browser extension install request — {browser}",
        ],
        descriptions=[
            "I'd like to install a browser extension called {app} on my work {browser}. "
            "It's a productivity tool for organizing bookmarks. I know extensions need "
            "approval — happy to go through whatever process is needed. No rush at all.",
            "Is there a way to get a {browser} extension approved for use on my work "
            "machine? It's a well-known tool called {app} that helps with tab management. "
            "Completely optional — I can live without it.",
        ],
        next_best_actions=[
            "Review the extension against the approved software list and security "
            "requirements. If it passes review, add it to the allowed extensions policy.",
            "Check if the requested extension is already on the approved list. If not, "
            "submit it for security review through the software approval process.",
        ],
        remediation_steps=[
            [
                "Check if the extension is on the approved software list",
                "If not, submit it for security and compliance review",
                "Once approved, add it to the browser extension allowlist via GPO",
                "Notify the user of the outcome",
            ],
            [
                "Evaluate the extension's permissions and data access requirements",
                "If acceptable, approve and deploy via the browser management policy",
                "If denied, inform the user with the specific reason",
            ],
        ],
    )
)

register(
    ScenarioTemplate(
        scenario_id="lp-018",
        category=Category.SOFTWARE,
        priority=Priority.P4,
        assigned_team=Team.ENTERPRISE_APPS,
        needs_escalation=False,
        missing_information=[
            MissingInfo.APPLICATION_VERSION,
            MissingInfo.STEPS_TO_REPRODUCE,
        ],
        subjects=[
            "Teams status message doesn't save after restart",
            "Custom status in Teams keeps resetting",
            "Teams loses my custom status message on reboot",
        ],
        descriptions=[
            "Every time I restart Teams (or my laptop), my custom status message "
            "disappears and I have to set it again. It's a minor annoyance — I like "
            "having 'Working from {office} today' as my status. Not a big deal, just "
            "curious if there's a fix.",
            "My Teams status message resets to blank after every reboot. I set it to "
            "something like 'Available — {department} team' but it never sticks. "
            "Everything else in Teams works fine. Low priority.",
        ],
        next_best_actions=[
            "Check the Teams client version and whether the status persistence feature "
            "is enabled. Verify if a policy is clearing custom status messages.",
            "Review the Teams client cache and settings. Check if there's a known bug "
            "in the current version related to status message persistence.",
        ],
        remediation_steps=[
            [
                "Verify the Teams client version and check for updates",
                "Clear the Teams cache and test status persistence",
                "Check for known issues in the Microsoft 365 service health dashboard",
            ],
            [
                "Check if a Teams policy is resetting status messages on sign-in",
                "Update the Teams client to the latest version",
                "If the issue persists, log a case with Microsoft support for tracking",
            ],
        ],
    )
)

register(
    ScenarioTemplate(
        scenario_id="lp-019",
        category=Category.SOFTWARE,
        priority=Priority.P4,
        assigned_team=Team.ENTERPRISE_APPS,
        needs_escalation=False,
        missing_information=[MissingInfo.APPLICATION_VERSION, MissingInfo.DEVICE_INFO],
        subjects=[
            "Excel add-in loads slowly but works fine",
            "Slow load time for {app} add-in in Excel",
            "Excel add-in performance — minor slowness on startup",
        ],
        descriptions=[
            "The {app} add-in in Excel takes about 15-20 seconds to load every time I "
            "open a workbook. Once it's loaded, it works perfectly. Not blocking anything "
            "— just a bit of a wait. I'm on {os} with the latest Office version.",
            "I've noticed my Excel add-in ({app}) is slow to initialize. It adds maybe "
            "15 seconds to my spreadsheet load time. Not a dealbreaker by any means, "
            "just figured I'd mention it. Everything functions correctly once loaded.",
        ],
        next_best_actions=[
            "Check the add-in version and whether a newer release improves load times. "
            "Review Excel's COM add-in load times in the Trust Center.",
            "Investigate the add-in's startup performance using Excel's built-in COM "
            "add-in diagnostics and check for updates.",
        ],
        remediation_steps=[
            [
                "Check the add-in version and look for available updates",
                "Review Excel COM add-in load time metrics in the Trust Center",
                "If the add-in is outdated, update it and test load times",
            ],
            [
                "Disable and re-enable the add-in to reset its configuration",
                "Check if other add-ins are competing for resources on startup",
                "If slow loading persists, contact the add-in vendor for guidance",
            ],
        ],
    )
)

register(
    ScenarioTemplate(
        scenario_id="lp-020",
        category=Category.SOFTWARE,
        priority=Priority.P4,
        assigned_team=Team.ENTERPRISE_APPS,
        needs_escalation=False,
        missing_information=[MissingInfo.APPLICATION_VERSION, MissingInfo.BUSINESS_IMPACT],
        subjects=[
            "Request for newer version of PDF viewer",
            "Can I get an updated PDF reader? Current one works fine",
            "PDF viewer upgrade request — not urgent",
        ],
        descriptions=[
            "I'm running an older version of {app} and noticed there's a newer release "
            "with some nice features like tabbed viewing. My current version works fine "
            "for everything I need — this is purely a nice-to-have. Whenever the next "
            "software refresh happens is totally fine.",
            "Would it be possible to get the latest version of {app} installed? I'm "
            "on version {number} and the new version has better annotation tools. No "
            "rush — the current version does the job. Just putting it on your radar.",
        ],
        next_best_actions=[
            "Check the approved software catalog for the latest version of the PDF "
            "viewer. If approved, add the user to the next deployment wave.",
            "Verify the requested version is on the approved software list and check "
            "if a deployment is already scheduled.",
        ],
        remediation_steps=[
            [
                "Check the current approved version in the software catalog",
                "If a newer version is approved, deploy it via Intune or SCCM",
                "Notify the user once the update is available",
            ],
            [
                "Verify the newer version is tested and approved for deployment",
                "Add the user's device to the next scheduled update ring",
                "Confirm the upgrade completes successfully",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# Security & Compliance — P4
# ---------------------------------------------------------------------------

register(
    ScenarioTemplate(
        scenario_id="lp-021",
        category=Category.SECURITY,
        priority=Priority.P4,
        assigned_team=Team.SECOPS,
        needs_escalation=False,
        missing_information=[MissingInfo.AUTHENTICATION_METHOD],
        subjects=[
            "Question about password complexity requirements",
            "What are the current password rules?",
            "Inquiry about Contoso password policy",
        ],
        descriptions=[
            "Hi, I'm about to change my password and wanted to know the exact complexity "
            "requirements. Is it 12 characters minimum now? Do I need special characters "
            "and numbers? I just want to make sure I pick something that won't get "
            "rejected. Thanks!",
            "Quick question — what are the current password complexity rules at Contoso? "
            "I know there's a minimum length and some character requirements but I can't "
            "find the policy document. Not urgent, I just want to plan ahead before my "
            "password expires on {date}.",
        ],
        next_best_actions=[
            "Provide the user with a link to the current password policy documentation "
            "and summarize the key requirements.",
            "Share the password complexity requirements and point the user to the IT "
            "knowledge base article on password best practices.",
        ],
        remediation_steps=[
            [
                "Share the current password policy summary with the user",
                "Provide a link to the full policy on the IT intranet",
                "Offer to assist if they encounter issues during the password change",
            ],
            [
                "Send the password complexity requirements via email",
                "Recommend the IT knowledge base article on creating strong passwords",
            ],
        ],
    )
)

register(
    ScenarioTemplate(
        scenario_id="lp-022",
        category=Category.SECURITY,
        priority=Priority.P4,
        assigned_team=Team.SECOPS,
        needs_escalation=False,
        missing_information=[MissingInfo.BUSINESS_IMPACT],
        subjects=[
            "Request to understand the data classification policy",
            "Where can I find info on data classification levels?",
            "Question about how Contoso classifies data",
        ],
        descriptions=[
            "I'm working on a project for the {department} team and want to make sure "
            "I'm handling documents correctly. Where can I find the data classification "
            "policy? I want to understand the difference between confidential and "
            "internal-only. No rush — just want to be informed.",
            "Hi, I'm new to Contoso and trying to understand how data classification "
            "works here. Is there a guide or training I can take? I want to make sure "
            "I'm labeling my documents properly. Not urgent at all.",
        ],
        next_best_actions=[
            "Direct the user to the data classification policy page on the intranet "
            "and recommend the information security awareness training module.",
            "Share the data classification guide and offer to set up a brief call "
            "with the security team if the user has specific questions.",
        ],
        remediation_steps=[
            [
                "Send the user a link to the data classification policy",
                "Recommend the relevant security awareness training module",
                "Offer follow-up assistance if they have specific questions",
            ],
            [
                "Provide the data classification quick-reference guide",
                "Point the user to the sensitivity label documentation in SharePoint",
            ],
        ],
    )
)

register(
    ScenarioTemplate(
        scenario_id="lp-023",
        category=Category.SECURITY,
        priority=Priority.P4,
        assigned_team=Team.SECOPS,
        needs_escalation=False,
        missing_information=[
            MissingInfo.SCREENSHOT_OR_ATTACHMENT,
            MissingInfo.STEPS_TO_REPRODUCE,
        ],
        subjects=[
            "Cosmetic issue in security awareness training portal",
            "UI glitch on the security training site",
            "Minor display bug in the phishing training module",
        ],
        descriptions=[
            "I was going through the quarterly security awareness training and noticed "
            "that one of the quiz pages has overlapping text — the question text bleeds "
            "into the answer buttons. I could still complete it by guessing the layout. "
            "Just a heads-up for the portal team. Using {browser} on {os}.",
            "There's a cosmetic issue on the security training portal where the progress "
            "bar doesn't update correctly on the phishing simulation module. It shows 0% "
            "even though I'm halfway through. The training itself works fine — just the "
            "display is off.",
        ],
        next_best_actions=[
            "Log the UI bug with the training portal vendor and note the browser and "
            "OS details for reproduction. No user impact on training completion.",
            "Report the cosmetic issue to the training platform admin and check if a "
            "portal update is pending that might resolve it.",
        ],
        remediation_steps=[
            [
                "Document the cosmetic issue with screenshots and browser details",
                "Report the bug to the training portal vendor or admin",
                "Track the fix in the next portal update cycle",
            ],
            [
                "Verify the issue is reproducible and note the affected pages",
                "Check if a portal update is already scheduled",
                "Notify the user once the issue is resolved",
            ],
        ],
    )
)

register(
    ScenarioTemplate(
        scenario_id="lp-024",
        category=Category.SECURITY,
        priority=Priority.P4,
        assigned_team=Team.SECOPS,
        needs_escalation=False,
        missing_information=[MissingInfo.DEVICE_INFO],
        subjects=[
            "Question about whether personal USB drives are allowed",
            "Are we allowed to use personal USB drives at work?",
            "USB drive policy question — not urgent",
        ],
        descriptions=[
            "Quick question — are we allowed to plug personal USB flash drives into our "
            "work laptops? I have some personal photos I'd like to transfer to my phone "
            "but don't want to violate any security policies. Not urgent, just curious.",
            "I wanted to check if using a personal USB drive on a company laptop is "
            "permitted. I know some companies block USB storage for security reasons. "
            "Just want to make sure before I try. Thanks!",
        ],
        next_best_actions=[
            "Provide the user with the current removable storage policy and explain "
            "any DLP controls in place for USB devices.",
            "Share the endpoint security policy regarding removable media and suggest "
            "approved alternatives for file transfer.",
        ],
        remediation_steps=[
            [
                "Share the removable media / USB storage policy with the user",
                "Explain any DLP or device control policies in effect",
                "Suggest approved alternatives like OneDrive for personal transfers",
            ],
            [
                "Point the user to the endpoint security policy documentation",
                "Clarify what types of USB devices are allowed or blocked",
            ],
        ],
    )
)

register(
    ScenarioTemplate(
        scenario_id="lp-025",
        category=Category.SECURITY,
        priority=Priority.P4,
        assigned_team=Team.SECOPS,
        needs_escalation=False,
        missing_information=[MissingInfo.AFFECTED_SYSTEM],
        subjects=[
            "Request to review my own access permissions",
            "Can I see a list of what I have access to?",
            "Self-service access review request",
        ],
        descriptions=[
            "Hi, I'd like to review my current access permissions across all systems. "
            "I've been at Contoso for a few years and have probably accumulated access "
            "to things I no longer need. Just want to do some housekeeping — no rush.",
            "Is there a way for me to see a full list of all the groups, applications, "
            "and SharePoint sites I have access to? I want to clean up any access I "
            "don't use anymore. Purely voluntary — just trying to follow best practices.",
        ],
        next_best_actions=[
            "Direct the user to the MyAccess portal in Entra ID where they can review "
            "their group memberships and application assignments.",
            "Guide the user to the self-service access review tool and offer to help "
            "revoke any permissions they no longer need.",
        ],
        remediation_steps=[
            [
                "Point the user to the Entra ID MyAccess portal for self-service review",
                "Provide instructions on how to view group memberships and app assignments",
                "Offer to help remove any access they identify as unnecessary",
            ],
            [
                "Generate an access report for the user from Entra ID",
                "Walk them through the results and help identify stale access",
                "Remove any unnecessary permissions with user's confirmation",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# Data & Storage — P4
# ---------------------------------------------------------------------------

register(
    ScenarioTemplate(
        scenario_id="lp-026",
        category=Category.DATA,
        priority=Priority.P4,
        assigned_team=Team.DATA_PLATFORM,
        needs_escalation=False,
        missing_information=[MissingInfo.AFFECTED_SYSTEM],
        subjects=[
            "OneDrive showing low storage warning — not urgent",
            "OneDrive almost full but no immediate issue",
            "Low storage notification on OneDrive — just a heads-up",
        ],
        descriptions=[
            "I got a notification that my OneDrive is at 98% capacity. I'm not in "
            "danger of losing anything and I can probably clean up some old files. "
            "Just wondering — is there a way to get a storage increase, or should I "
            "just archive stuff? No rush at all.",
            "My OneDrive is almost full — only about 2% space remaining. Everything "
            "still works fine and I have some old project files I can move. Figured "
            "I'd ask if there's a standard process for requesting more storage or "
            "if I should just do some cleanup.",
        ],
        next_best_actions=[
            "Advise the user on OneDrive cleanup best practices and check if a storage "
            "quota increase is available under current licensing.",
            "Provide guidance on archiving old files to SharePoint or an archive site, "
            "and check the tenant's OneDrive storage allocation policy.",
        ],
        remediation_steps=[
            [
                "Share OneDrive cleanup tips and storage management best practices",
                "Check if the user's license allows a quota increase",
                "If eligible, increase the quota; otherwise help with archival",
            ],
            [
                "Review the user's OneDrive usage and identify large or old files",
                "Suggest moving archived content to a SharePoint document library",
                "Adjust the quota if policy permits or help with cleanup",
            ],
        ],
    )
)

register(
    ScenarioTemplate(
        scenario_id="lp-027",
        category=Category.DATA,
        priority=Priority.P4,
        assigned_team=Team.DATA_PLATFORM,
        needs_escalation=False,
        missing_information=[MissingInfo.CONFIGURATION_DETAILS, MissingInfo.AFFECTED_USERS],
        subjects=[
            "Request to change file naming convention in shared drive",
            "Can we update the folder naming standard for our team?",
            "File naming convention improvement suggestion",
        ],
        descriptions=[
            "Our team's shared drive has a mix of naming conventions and it's getting "
            "hard to find things. I'd like to propose a standardized naming scheme — "
            "something like YYYY-MM-DD_ProjectName_Version. Is this something IT can "
            "help with? No urgency — just a long-term improvement idea.",
            "Hi, the {department} shared drive could use some organizational cleanup. "
            "Files are named inconsistently and there's no standard convention. Can IT "
            "help us set up a naming policy or template? Totally a nice-to-have.",
        ],
        next_best_actions=[
            "Provide the user with the corporate file naming guidelines if they exist, "
            "or direct them to the data governance team for standards.",
            "Suggest the user work with their team lead to establish a convention and "
            "offer IT support for enforcing it via metadata or folder templates.",
        ],
        remediation_steps=[
            [
                "Share any existing corporate file naming or data governance guidelines",
                "Offer to set up a folder template with the proposed naming convention",
                "Coordinate with the team lead to communicate the new standard",
            ],
            [
                "Review the current shared drive structure with the user",
                "Help establish a naming convention document for the team",
                "Set up SharePoint metadata or folder structure to support the convention",
            ],
        ],
    )
)

register(
    ScenarioTemplate(
        scenario_id="lp-028",
        category=Category.DATA,
        priority=Priority.P4,
        assigned_team=Team.DATA_PLATFORM,
        needs_escalation=False,
        missing_information=[MissingInfo.AFFECTED_SYSTEM, MissingInfo.BUSINESS_IMPACT],
        subjects=[
            "Old archived project folder access request — for reference only",
            "Can I get access to an old project archive?",
            "Request to view archived project files — no changes needed",
        ],
        descriptions=[
            "I'm working on a similar project to one we did in 2021 and I'd like to "
            "reference the old project files. They were archived on the {department} "
            "shared drive. I just need read access — no changes. Whenever you get "
            "around to it is fine.",
            "Hi, could I get access to the archived folder for the {app} project from "
            "a couple of years ago? I want to look at some of the documentation for "
            "reference. Read-only is perfectly fine. No rush at all.",
        ],
        next_best_actions=[
            "Locate the archived project folder and verify the user's justification "
            "for access. Grant read-only permissions if approved.",
            "Check the archive retention policy and locate the requested folder. "
            "Route the access request to the project's original owner for approval.",
        ],
        remediation_steps=[
            [
                "Locate the archived project folder in the storage system",
                "Verify the access request with the original project owner or manager",
                "Grant read-only access and notify the user",
            ],
            [
                "Check the archive retention policy to ensure the data is still available",
                "Restore or provide access to the archived folder",
                "Set a time-limited access window if required by policy",
            ],
        ],
    )
)

register(
    ScenarioTemplate(
        scenario_id="lp-029",
        category=Category.DATA,
        priority=Priority.P4,
        assigned_team=Team.DATA_PLATFORM,
        needs_escalation=False,
        missing_information=[
            MissingInfo.SCREENSHOT_OR_ATTACHMENT,
            MissingInfo.STEPS_TO_REPRODUCE,
        ],
        subjects=[
            "Minor formatting issue in a scheduled report",
            "Report formatting slightly off — still readable",
            "Cosmetic issue with automated report output",
        ],
        descriptions=[
            "The weekly {app} report that gets emailed every Monday has a minor "
            "formatting issue — the column headers are slightly misaligned and one "
            "date column shows the time as well. The data is all correct, it just "
            "looks a bit messy. Not blocking anything.",
            "I noticed the automated report from {app} has a small formatting glitch. "
            "Some of the numbers aren't right-aligned and the header row is missing "
            "its bold formatting. Everything is still readable — just a cosmetic thing "
            "I thought I'd flag.",
        ],
        next_best_actions=[
            "Review the report template and identify the formatting discrepancy. "
            "Schedule a fix for the next report maintenance window.",
            "Check if a recent template or data source change caused the formatting "
            "issue. Log it for the next scheduled report update.",
        ],
        remediation_steps=[
            [
                "Review the report template for formatting inconsistencies",
                "Adjust column alignment and date formatting in the template",
                "Test the fix with a manual report run before the next scheduled send",
            ],
            [
                "Check for recent changes to the report template or data source",
                "Correct the formatting issues and validate the output",
                "Confirm with the user that the next report looks correct",
            ],
        ],
    )
)

register(
    ScenarioTemplate(
        scenario_id="lp-030",
        category=Category.DATA,
        priority=Priority.P4,
        assigned_team=Team.DATA_PLATFORM,
        needs_escalation=False,
        missing_information=[MissingInfo.AFFECTED_USERS, MissingInfo.AFFECTED_SYSTEM],
        subjects=[
            "Request to clean up old team SharePoint site",
            "Can IT help clean up our outdated SharePoint site?",
            "SharePoint site cleanup request — old content removal",
        ],
        descriptions=[
            "Our team's SharePoint site has a lot of outdated content from projects "
            "that ended years ago. I'd like to do a cleanup but I'm not sure what's "
            "safe to delete versus what should be archived. Can IT help guide us "
            "through this? Totally low priority — it's been like this for a while.",
            "Hi, the {department} SharePoint site is cluttered with old files, broken "
            "links, and outdated pages. I'd like to request IT assistance to help clean "
            "it up or at least archive the old stuff. No rush — just want to get it "
            "on the radar.",
        ],
        next_best_actions=[
            "Schedule a SharePoint site review session with the user to identify "
            "content for archival versus deletion. Follow the data retention policy.",
            "Provide the user with SharePoint cleanup best practices and the "
            "content archival process. Offer to assist with bulk operations.",
        ],
        remediation_steps=[
            [
                "Share SharePoint cleanup best practices and retention policies",
                "Schedule a review session with the user to triage old content",
                "Archive or delete content as agreed upon",
                "Verify the site is functioning correctly after cleanup",
            ],
            [
                "Run a SharePoint site usage report to identify stale content",
                "Work with the user to categorize content as keep, archive, or delete",
                "Execute the cleanup and update site navigation accordingly",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# General Inquiry — P4
# ---------------------------------------------------------------------------

register(
    ScenarioTemplate(
        scenario_id="lp-031",
        category=Category.GENERAL,
        priority=Priority.P4,
        assigned_team=Team.NONE,
        needs_escalation=False,
        missing_information=[MissingInfo.CONTACT_INFO],
        subjects=[
            "Question about IT budget process for next fiscal year",
            "How does the IT equipment budget request process work?",
            "Inquiry about IT procurement for next FY",
        ],
        descriptions=[
            "Hi, my team is planning our budget for next fiscal year and I'm wondering "
            "how the IT equipment request process works. Is there a form to fill out? "
            "A deadline? I just want to make sure we account for any hardware or "
            "software we'll need. No rush — just planning ahead.",
            "I'm trying to understand the IT procurement process for the next fiscal "
            "year. Our {department} team might need some new equipment and software "
            "licenses. Can someone point me to the right process or person? Just "
            "gathering information at this point.",
        ],
        next_best_actions=[
            "Direct the user to the IT procurement process documentation and the "
            "relevant budget submission deadlines on the intranet.",
            "Connect the user with the IT finance or procurement team and share "
            "the equipment request form and timeline.",
        ],
        remediation_steps=[
            [
                "Share the IT procurement process guide from the intranet",
                "Provide the budget submission deadline and any required forms",
                "Connect the user with the IT procurement contact if needed",
            ],
            [
                "Point the user to the IT finance team for budget planning assistance",
                "Share the standard equipment and software request templates",
            ],
        ],
    )
)

register(
    ScenarioTemplate(
        scenario_id="lp-032",
        category=Category.GENERAL,
        priority=Priority.P4,
        assigned_team=Team.NONE,
        needs_escalation=False,
        missing_information=[MissingInfo.DEVICE_INFO],
        subjects=[
            "How to customize Teams notification sounds",
            "Can I change the notification sound in Teams?",
            "Teams notification customization question",
        ],
        descriptions=[
            "Is there a way to customize the notification sounds in Teams? The default "
            "sound is the same for every type of notification and I'd love to have "
            "different sounds for DMs versus channel mentions. Just a quality-of-life "
            "question — no issues to report.",
            "Quick question — can I change the notification sounds in Microsoft Teams? "
            "I keep confusing Teams notifications with other app sounds. If there's a "
            "setting I'm missing, I'd appreciate a pointer. Totally low priority.",
        ],
        next_best_actions=[
            "Provide instructions on Teams notification settings and explain which "
            "customization options are currently available.",
            "Share a knowledge base article on Teams notification management and note "
            "any limitations in the current version.",
        ],
        remediation_steps=[
            [
                "Share the steps to access Teams notification settings",
                "Explain which sounds can and cannot be customized",
                "Suggest using the Teams UserVoice to request additional features",
            ],
            [
                "Provide a link to the Teams notification settings documentation",
                "Note any available workarounds for notification differentiation",
            ],
        ],
    )
)

register(
    ScenarioTemplate(
        scenario_id="lp-033",
        category=Category.GENERAL,
        priority=Priority.P4,
        assigned_team=Team.NONE,
        needs_escalation=False,
        missing_information=[],
        subjects=[
            "Where can I find the IT service catalog?",
            "Looking for the IT services list / catalog",
            "How do I find what IT services are available?",
        ],
        descriptions=[
            "Hi, I'm looking for the IT service catalog — the list of all services IT "
            "provides. I want to see what's available before submitting any new requests. "
            "A colleague mentioned it's on the intranet somewhere but I can't find it. "
            "No rush at all.",
            "Is there a central catalog or list of all IT services available at Contoso? "
            "I'm new to the company and want to familiarize myself with what support "
            "options exist. Just an informational request — nothing urgent.",
        ],
        next_best_actions=[
            "Provide the direct link to the IT service catalog on the intranet and "
            "a brief overview of how to navigate it.",
            "Share the IT service catalog URL and suggest the user bookmark it for future reference.",
        ],
        remediation_steps=[
            [
                "Send the user the direct link to the IT service catalog",
                "Provide a brief overview of the most commonly used services",
            ],
            [
                "Share the service catalog URL and navigation tips",
                "Recommend the IT onboarding guide for new employees",
            ],
        ],
    )
)

register(
    ScenarioTemplate(
        scenario_id="lp-034",
        category=Category.GENERAL,
        priority=Priority.P4,
        assigned_team=Team.NONE,
        needs_escalation=False,
        missing_information=[],
        subjects=[
            "Question about the approved software list",
            "Where can I find the list of approved software?",
            "What software is pre-approved for installation?",
        ],
        descriptions=[
            "Is there a list of software that's pre-approved for installation on "
            "company devices? I want to check before I request anything so I don't "
            "waste anyone's time. I've looked on the intranet but couldn't find a "
            "definitive list. No rush.",
            "Hi, I'd like to know where I can find the catalog of approved software "
            "at Contoso. I'm thinking about requesting a couple of tools but want to "
            "check if they're already approved first. Just an informational question.",
        ],
        next_best_actions=[
            "Direct the user to the approved software catalog in the Company Portal or self-service software center.",
            "Provide the link to the software request portal and the list of pre-approved "
            "applications available for self-service install.",
        ],
        remediation_steps=[
            [
                "Share the link to the approved software catalog or Company Portal",
                "Explain the self-service installation process for approved apps",
            ],
            [
                "Point the user to the software request portal on the intranet",
                "Describe the approval process for non-standard software requests",
            ],
        ],
    )
)

register(
    ScenarioTemplate(
        scenario_id="lp-035",
        category=Category.GENERAL,
        priority=Priority.P4,
        assigned_team=Team.NONE,
        needs_escalation=False,
        missing_information=[MissingInfo.CONTACT_INFO],
        subjects=[
            "Request for IT newsletter subscription",
            "How do I subscribe to the IT updates newsletter?",
            "Want to sign up for IT communications",
        ],
        descriptions=[
            "I've seen colleagues share articles from an IT newsletter and I'd love "
            "to get subscribed. Is there a mailing list I can join? I want to stay "
            "informed about upcoming changes and maintenance windows. No rush — "
            "whenever you can point me in the right direction.",
            "Hi, is there an IT newsletter or mailing list I can subscribe to? I'd "
            "like to get updates about new services, planned maintenance, and tips. "
            "Just an informational request.",
        ],
        next_best_actions=[
            "Add the user to the IT communications distribution list or provide the self-service subscription link.",
            "Share the IT newsletter sign-up page and any related Teams channels for IT updates.",
        ],
        remediation_steps=[
            [
                "Add the user to the IT newsletter distribution list",
                "Confirm the subscription and share the latest newsletter issue",
            ],
            [
                "Provide the self-service subscription link for IT communications",
                "Recommend the IT announcements Teams channel for real-time updates",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# Not a Support Ticket — P4
# ---------------------------------------------------------------------------

register(
    ScenarioTemplate(
        scenario_id="lp-036",
        category=Category.NOT_SUPPORT,
        priority=Priority.P4,
        assigned_team=Team.NONE,
        needs_escalation=False,
        missing_information=[],
        subjects=[
            "Thank you for the great IT support last month!",
            "Kudos to the IT team — amazing service",
            "Appreciation note for IT help desk",
        ],
        descriptions=[
            "Just wanted to say a huge thank you to the IT team for the help with my "
            "laptop issue last month. {name} was incredibly patient and got everything "
            "sorted in no time. Really appreciate the great service!",
            "I want to give a shout-out to IT support — you all went above and beyond "
            "when our team had issues during the system migration. The response time "
            "was impressive and everyone was so helpful. Keep up the great work!",
        ],
        next_best_actions=[
            "Acknowledge the compliment and share it with the team. Log the positive "
            "feedback for the referenced technician's performance record.",
            "Thank the user for the feedback and forward the kudos to the relevant team member and their manager.",
        ],
        remediation_steps=[
            [
                "Acknowledge the positive feedback and thank the user",
                "Forward the kudos to the referenced team member and their manager",
            ],
            [
                "Log the positive feedback in the service management system",
                "Share the compliment with the wider IT team for morale",
            ],
        ],
    )
)

register(
    ScenarioTemplate(
        scenario_id="lp-037",
        category=Category.NOT_SUPPORT,
        priority=Priority.P4,
        assigned_team=Team.NONE,
        needs_escalation=False,
        missing_information=[],
        subjects=[
            "Interesting tech article — thought IT might enjoy this",
            "Sharing a cool article about {app}",
            "FYI — tech article that might be relevant to IT",
        ],
        descriptions=[
            "Hey IT team, I came across this really interesting article about cloud "
            "security trends and thought you might find it useful. No action needed — "
            "just sharing because I thought of you all when I read it. Here's the link: "
            "[article link].",
            "I saw a great article about the future of remote work technology and wanted "
            "to share it with the IT department. You folks are always keeping us ahead "
            "of the curve so I figured you'd appreciate it. No response needed!",
        ],
        next_best_actions=[
            "Thank the user for sharing and close the ticket. No technical action "
            "required — this is not a support request.",
            "Acknowledge the article share, thank the user, and close the ticket "
            "as informational / not a support issue.",
        ],
        remediation_steps=[
            [
                "Thank the user for thinking of the IT team",
                "Close the ticket as informational — no action required",
            ],
            [
                "Acknowledge the share and close the ticket",
                "Forward the article to the IT team channel if genuinely relevant",
            ],
        ],
    )
)

register(
    ScenarioTemplate(
        scenario_id="lp-038",
        category=Category.NOT_SUPPORT,
        priority=Priority.P4,
        assigned_team=Team.NONE,
        needs_escalation=False,
        missing_information=[MissingInfo.SCREENSHOT_OR_ATTACHMENT],
        subjects=[
            "Suggestion for improving the help desk portal",
            "Idea to make the IT portal more user-friendly",
            "Feature request for the IT self-service portal",
        ],
        descriptions=[
            "I have a suggestion for the IT help desk portal — it would be great if "
            "there was a search bar on the main page so we could look up common issues "
            "before submitting a ticket. Not a bug report, just an idea for improvement. "
            "Love the portal otherwise!",
            "Hey, just a friendly suggestion — it would be awesome if the IT portal had "
            "a FAQ section or a chatbot for common questions. I bet it would reduce the "
            "number of tickets you get. Just an idea — not expecting anything immediate!",
        ],
        next_best_actions=[
            "Log the suggestion in the IT portal improvement backlog and thank the "
            "user for the feedback. Close as a feature request.",
            "Forward the suggestion to the IT service management team for "
            "consideration and thank the user for the input.",
        ],
        remediation_steps=[
            [
                "Thank the user for the constructive suggestion",
                "Log the idea in the portal improvement backlog",
                "Close the ticket as a feature request",
            ],
            [
                "Acknowledge the feedback and forward to the portal team",
                "Close the ticket — no technical remediation needed",
            ],
        ],
    )
)

register(
    ScenarioTemplate(
        scenario_id="lp-039",
        category=Category.NOT_SUPPORT,
        priority=Priority.P4,
        assigned_team=Team.NONE,
        needs_escalation=False,
        missing_information=[MissingInfo.CONTACT_INFO],
        subjects=[
            "Inquiry about IT career paths at Contoso",
            "Interested in learning about IT roles at Contoso",
            "Question about transitioning into an IT role",
        ],
        descriptions=[
            "Hi, I'm currently in the {department} team but I've always been interested "
            "in technology. I was wondering if there are any internal career paths into "
            "IT at Contoso? I have some coding experience and would love to explore "
            "options. Not urgent — just curious!",
            "I'd like to learn more about IT career opportunities at Contoso. I have a "
            "background in {department} but I'm thinking about a career change into "
            "tech. Is there someone in IT I could talk to about potential roles or "
            "mentorship opportunities?",
        ],
        next_best_actions=[
            "Redirect the user to HR and the internal careers portal. Offer to connect "
            "them with IT leadership for an informational conversation.",
            "Thank the user for their interest and point them to the internal job "
            "board and any IT mentorship programs.",
        ],
        remediation_steps=[
            [
                "Direct the user to the internal careers portal and HR team",
                "Offer to connect them with an IT manager for an informational chat",
            ],
            [
                "Share the internal job board link for IT positions",
                "Mention any IT mentorship or shadowing programs if available",
                "Close the ticket as a non-support inquiry",
            ],
        ],
    )
)

register(
    ScenarioTemplate(
        scenario_id="lp-040",
        category=Category.NOT_SUPPORT,
        priority=Priority.P4,
        assigned_team=Team.NONE,
        needs_escalation=False,
        missing_information=[],
        subjects=[
            "Forwarding all-hands meeting notes that mentioned IT",
            "Meeting notes from company all-hands — IT section",
            "FYI: All-hands recap with IT-related topics",
        ],
        descriptions=[
            "Hi IT team, just forwarding the meeting notes from last week's company "
            "all-hands. There were a few mentions of upcoming IT initiatives — thought "
            "you'd want to have the notes for reference. No action needed from your "
            "side, just an FYI!",
            "Sharing the notes from the all-hands meeting on {date}. The CEO mentioned "
            "some plans for IT infrastructure upgrades and a new collaboration tool "
            "rollout. Figured you all already know about this but just in case. "
            "No response needed!",
        ],
        next_best_actions=[
            "Thank the user for sharing and close the ticket. No support action required — this is informational.",
            "Acknowledge receipt of the meeting notes and close the ticket as "
            "informational. No technical action needed.",
        ],
        remediation_steps=[
            [
                "Thank the user for forwarding the information",
                "Close the ticket as informational — no action required",
            ],
            [
                "Acknowledge the notes and close as a non-support item",
                "Share with the IT leadership team if the content is new information",
            ],
        ],
    )
)
