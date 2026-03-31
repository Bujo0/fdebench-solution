# Copyright (c) Microsoft. All rights reserved.
"""General Inquiry scenario templates.

Covers: how-to questions, meeting room booking, IT onboarding requests,
offboarding requests, policy questions, training requests, asset inventory,
procurement, status checks, and process questions.
"""

from ms.evals.constants import Category
from ms.evals.constants import MissingInfo
from ms.evals.constants import Priority
from ms.evals.constants import Team
from ms.evals.models import ScenarioTemplate
from ms.evals.scenarios.registry import register

# ---------------------------------------------------------------------------
# gi-001  How do I book a meeting room?
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="gi-001",
        category=Category.GENERAL,
        priority=Priority.P4,
        assigned_team=Team.NONE,
        needs_escalation=False,
        missing_information=[],
        subjects=[
            "How do I book a meeting room?",
            "Meeting room reservation — how does it work?",
            "Need help booking a conference room",
        ],
        descriptions=[
            "Hi, I just joined the company last week and I need to book a meeting room for a team "
            "sync tomorrow afternoon. I looked in Outlook but I can't figure out where the room "
            "calendars are. Can someone point me in the right direction?",
            "Quick question — what's the process for reserving a conference room? I tried searching "
            "in Outlook but none of the room lists show up. Is there a specific tool or portal we "
            "use for room bookings?",
        ],
        next_best_actions=[
            "Direct the user to the Outlook room finder or the company's room booking portal and "
            "provide step-by-step instructions.",
            "Share the knowledge base article on meeting room reservations and verify the user has "
            "access to room calendars in Outlook.",
        ],
        remediation_steps=[
            [
                "Provide link to the room booking knowledge base article",
                "Walk user through opening Outlook → New Meeting → Room Finder",
                "Verify user can see available room lists for their office location",
                "Confirm user successfully books the room",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# gi-002  Where can I find the IT support knowledge base?
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="gi-002",
        category=Category.GENERAL,
        priority=Priority.P4,
        assigned_team=Team.NONE,
        needs_escalation=False,
        missing_information=[],
        subjects=[
            "Where is the IT support knowledge base?",
            "Link to IT self-help articles?",
            "Can't find IT documentation — where should I look?",
        ],
        descriptions=[
            "Is there a central knowledge base or FAQ site for IT support? I keep submitting tickets "
            "for things that probably have simple answers. Would love to be able to look things up "
            "myself first.",
            "My manager mentioned there's an internal wiki with IT how-to guides but I can't find "
            "the URL anywhere. Could you share the link to the IT knowledge base?",
        ],
        next_best_actions=[
            "Provide the URL to the IT knowledge base and verify the user can access it.",
            "Share the IT self-service portal link and confirm the user's permissions.",
        ],
        remediation_steps=[
            [
                "Share the direct URL to the IT knowledge base / self-service portal",
                "Verify the user can authenticate and access the site",
                "Recommend bookmarking the page for future reference",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# gi-003  New hire onboarding — full setup needed
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="gi-003",
        category=Category.GENERAL,
        priority=Priority.P3,
        assigned_team=Team.ENDPOINT,
        needs_escalation=False,
        missing_information=[MissingInfo.DEVICE_INFO, MissingInfo.CONTACT_INFO],
        subjects=[
            "New hire onboarding — full IT setup needed",
            "Onboarding request for new team member starting Monday",
            "IT setup for incoming employee",
        ],
        descriptions=[
            "We have a new hire starting on {start_date} in the {department} department. They'll "
            "need a laptop, standard software suite, email account, badge access, and VPN setup. "
            "Their manager is {manager_name}. Please let me know what else you need from us to "
            "get everything ready.",
            "New employee joining our team next week — {name}, role: {role}. Need the full "
            "onboarding package: laptop provisioning, M365 account, Teams access, department "
            "shared drives, and building access. Start date is {start_date}.",
        ],
        next_best_actions=[
            "Initiate the standard new-hire onboarding checklist — provision hardware, create "
            "accounts, and coordinate badge access with facilities.",
            "Confirm hardware availability, begin account provisioning, and send the onboarding "
            "checklist to the requesting manager.",
        ],
        remediation_steps=[
            [
                "Confirm start date, role, and department with the requesting manager",
                "Provision laptop from available inventory and install standard image",
                "Create user account in Entra ID and assign appropriate licenses",
                "Add user to department security groups and distribution lists",
                "Configure VPN access and verify connectivity",
                "Coordinate badge access with facilities team",
                "Send onboarding welcome email with setup instructions",
            ],
            [
                "Verify new hire details against HR onboarding form",
                "Check hardware inventory for available laptop matching role requirements",
                "Create accounts across required systems (Entra ID, M365, Teams)",
                "Set up shared drive and departmental resource access",
                "Schedule Day 1 IT orientation walkthrough",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# gi-004  Employee offboarding — revoke all access
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="gi-004",
        category=Category.GENERAL,
        priority=Priority.P2,
        assigned_team=Team.IAM,
        needs_escalation=False,
        missing_information=[MissingInfo.AFFECTED_USERS],
        subjects=[
            "Employee offboarding — please revoke all access immediately",
            "Urgent: departing employee access removal",
            "Offboarding request — last day is {date}",
        ],
        descriptions=[
            "Employee {name} ({email}) in {department} is leaving the company. Their last day is "
            "{last_day}. Please revoke all system access, disable their account, recover the "
            "laptop, and ensure shared resources are reassigned. Manager is {manager_name}.",
            "{name} has been terminated effective immediately. Need all access revoked ASAP — "
            "Entra ID, VPN, badge, email, and any shared service accounts they managed. Please "
            "confirm once complete. This is time-sensitive.",
        ],
        next_best_actions=[
            "Execute the offboarding checklist immediately — disable Entra ID account, revoke VPN "
            "and badge access, initiate hardware recovery, and transfer shared resources.",
            "Disable all accounts and access per the offboarding policy. Coordinate hardware "
            "return and mailbox delegation with the departing employee's manager.",
        ],
        remediation_steps=[
            [
                "Disable user account in Entra ID and block sign-in",
                "Revoke all active sessions and refresh tokens",
                "Disable VPN access and remove from conditional access groups",
                "Coordinate badge deactivation with facilities",
                "Convert mailbox to shared mailbox and delegate to manager",
                "Recover laptop and any other IT assets",
                "Remove user from all security and distribution groups",
                "Document completion in offboarding tracker",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# gi-005  How to connect to the guest WiFi?
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="gi-005",
        category=Category.GENERAL,
        priority=Priority.P4,
        assigned_team=Team.NONE,
        needs_escalation=False,
        missing_information=[],
        subjects=[
            "How do I connect to the guest WiFi?",
            "Guest WiFi access — what's the process?",
            "Visitor needs WiFi — how to get connected?",
        ],
        descriptions=[
            "I have a client visiting our office tomorrow and they'll need WiFi access for a "
            "presentation. What's the guest WiFi network name and how do they get the password?",
            "Quick question — we have external visitors coming for a workshop. How do they connect "
            "to the guest wireless network? Is there a captive portal or do we need to request "
            "access in advance?",
        ],
        next_best_actions=[
            "Provide guest WiFi SSID and connection instructions, including captive portal details.",
            "Share guest network access procedure and any visitor registration requirements.",
        ],
        remediation_steps=[
            [
                "Provide the guest WiFi SSID and connection instructions",
                "Explain the captive portal registration or sponsor-approval process",
                "Confirm guest can connect successfully on arrival",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# gi-006  What's the approved software list?
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="gi-006",
        category=Category.GENERAL,
        priority=Priority.P4,
        assigned_team=Team.NONE,
        needs_escalation=False,
        missing_information=[],
        subjects=[
            "What software is approved for use?",
            "Where can I find the list of approved applications?",
            "Need to check if a tool is on the approved software list",
        ],
        descriptions=[
            "My team wants to start using {software_name} for project management. Before we buy "
            "licenses, I need to know if it's on the approved software list. Where can I find that "
            "list and what's the process to request approval if it's not listed?",
            "Is there a catalog of pre-approved software I can browse? I want to install a few "
            "productivity tools but I don't want to violate any policies.",
        ],
        next_best_actions=[
            "Share the link to the approved software catalog and explain the software request "
            "process for unlisted applications.",
            "Direct user to the software governance portal and provide the exception request form "
            "if the tool is not pre-approved.",
        ],
        remediation_steps=[
            [
                "Provide link to the approved software catalog",
                "If the requested software is listed, confirm and share installation instructions",
                "If not listed, provide the software approval request form",
                "Explain typical approval timeline and review process",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# gi-007  Need IT asset inventory for my team
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="gi-007",
        category=Category.GENERAL,
        priority=Priority.P4,
        assigned_team=Team.NONE,
        needs_escalation=False,
        missing_information=[MissingInfo.AFFECTED_USERS],
        subjects=[
            "IT asset inventory report for my team",
            "Need a list of all devices assigned to my department",
            "Request for team hardware inventory",
        ],
        descriptions=[
            "I'm the manager of the {department} team and I need a current inventory of all IT "
            "assets assigned to my team members. We're doing a budget review and need to know "
            "what hardware everyone has and when it was provisioned.",
            "Can I get an export of the asset inventory for department {department}? We need to "
            "know laptop models, ages, and warranty status for all {count} team members as part "
            "of our annual planning.",
        ],
        next_best_actions=[
            "Generate an asset inventory report filtered by the requesting manager's department "
            "and share it securely.",
            "Export the hardware asset report from the CMDB for the specified team and send to "
            "the requesting manager.",
        ],
        remediation_steps=[
            [
                "Verify the requester is the department manager or has approval to view asset data",
                "Pull asset inventory report from the CMDB filtered by department",
                "Include device model, serial number, assignment date, and warranty status",
                "Share the report securely with the requester",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# gi-008  How do I request a second monitor?
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="gi-008",
        category=Category.GENERAL,
        priority=Priority.P4,
        assigned_team=Team.ENDPOINT,
        needs_escalation=False,
        missing_information=[MissingInfo.DEVICE_INFO],
        subjects=[
            "How do I request a second monitor?",
            "Can I get an additional display for my desk?",
            "Process for ordering a second monitor",
        ],
        descriptions=[
            "I'd like to request a second monitor for my workstation. I do a lot of data analysis "
            "and having dual screens would really help with productivity. What's the process — do "
            "I need manager approval?",
            "Is there a form or portal to request an extra monitor? My current setup is just a "
            "laptop and I'd like a proper external display for day-to-day work.",
        ],
        next_best_actions=[
            "Provide the hardware request form link and explain the approval workflow for "
            "peripheral equipment.",
            "Check monitor inventory and share the standard peripheral request process.",
        ],
        remediation_steps=[
            [
                "Provide the hardware request form or portal link",
                "Explain that manager approval may be required depending on cost threshold",
                "Check current monitor inventory and estimated delivery time",
                "Once approved, coordinate delivery and setup",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# gi-009  Laptop refresh policy question
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="gi-009",
        category=Category.GENERAL,
        priority=Priority.P4,
        assigned_team=Team.NONE,
        needs_escalation=False,
        missing_information=[],
        subjects=[
            "When is my laptop eligible for refresh?",
            "Laptop refresh policy — how often can we upgrade?",
            "Question about the hardware refresh cycle",
        ],
        descriptions=[
            "My laptop is about three years old and it's getting pretty slow. What's the company's "
            "hardware refresh policy? Am I eligible for a replacement, and if so, how do I start "
            "the process?",
            "I've heard there's a 3-year or 4-year laptop refresh cycle. Can you confirm the policy "
            "and let me know how to check when my device is due for replacement?",
        ],
        next_best_actions=[
            "Share the hardware refresh policy details and help the user check their device's "
            "eligibility based on provisioning date.",
            "Provide the refresh policy document link and look up the user's current device age "
            "in the asset management system.",
        ],
        remediation_steps=[
            [
                "Share the hardware refresh policy (e.g., standard 3-year cycle)",
                "Look up the user's current device in the asset management system",
                "Inform user whether their device is currently eligible for refresh",
                "If eligible, initiate the refresh request process",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# gi-010  Training request — Microsoft 365 advanced features
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="gi-010",
        category=Category.GENERAL,
        priority=Priority.P4,
        assigned_team=Team.NONE,
        needs_escalation=False,
        missing_information=[MissingInfo.AFFECTED_USERS],
        subjects=[
            "Training request — Microsoft 365 advanced features",
            "Can we schedule an M365 training session for our team?",
            "Request for Teams and SharePoint training",
        ],
        descriptions=[
            "Our team recently migrated to Microsoft 365 and we're not using it to its full "
            "potential. Can we arrange a training session covering advanced Teams features, "
            "SharePoint collaboration, and Power Automate basics? We have about {count} people "
            "interested.",
            "I'd like to request IT training for my department on Microsoft 365 — specifically "
            "OneDrive best practices, Teams channels, and SharePoint document libraries. Is there "
            "an internal training program or do we need to engage an external vendor?",
        ],
        next_best_actions=[
            "Connect the requester with the IT training coordinator and share available M365 "
            "learning resources in the meantime.",
            "Check the internal training calendar for upcoming M365 sessions and register the "
            "team, or schedule a custom session if needed.",
        ],
        remediation_steps=[
            [
                "Share self-paced M365 learning resources (Microsoft Learn, internal wiki)",
                "Check internal training calendar for upcoming sessions",
                "If no upcoming sessions, coordinate with training team to schedule one",
                "Confirm date, time, and enrollment with the requester",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# gi-011  Status check on previous ticket
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="gi-011",
        category=Category.GENERAL,
        priority=Priority.P4,
        assigned_team=Team.NONE,
        needs_escalation=False,
        missing_information=[MissingInfo.PREVIOUS_TICKET_ID],
        subjects=[
            "Status update on my previous ticket?",
            "Following up on ticket I submitted last week",
            "Any progress on my open IT request?",
        ],
        descriptions=[
            "Hi, I submitted a ticket about a week ago regarding {issue_summary} but I haven't "
            "heard back. Can someone give me a status update? I don't have the ticket number handy "
            "but it was submitted around {date}.",
            "Just checking in on a ticket I opened last {day}. It was about {issue_summary}. I "
            "haven't received any updates and wanted to know if it's still in the queue or if "
            "someone's working on it.",
        ],
        next_best_actions=[
            "Look up the user's recent tickets by email address, provide a status update, and "
            "re-prioritize if overdue.",
            "Search for the user's open tickets, share current status, and set expectations for "
            "resolution timeline.",
        ],
        remediation_steps=[
            [
                "Search the ticketing system for recent open tickets from the user",
                "Identify the referenced ticket and review its current status",
                "Provide a status update to the user with expected resolution timeline",
                "If overdue, escalate or re-assign as appropriate",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# gi-012  Bulk onboarding — 20 new interns starting
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="gi-012",
        category=Category.GENERAL,
        priority=Priority.P2,
        assigned_team=Team.IAM,
        needs_escalation=False,
        missing_information=[MissingInfo.AFFECTED_USERS, MissingInfo.CONTACT_INFO],
        subjects=[
            "Bulk onboarding — 20 new interns starting {date}",
            "Mass onboarding request: summer intern cohort",
            "Need 20 accounts and laptops provisioned for new interns",
        ],
        descriptions=[
            "We have 20 summer interns starting on {start_date}. They'll all need Entra ID "
            "accounts, M365 licenses, laptops, and temporary badge access. I'll send the full "
            "list of names and departments separately. Can we start planning now to make sure "
            "everything is ready on day one?",
            "Heads up — {count} new interns join on {start_date} across {department_count} "
            "departments. Each needs a standard intern laptop image, limited email, Teams access, "
            "and time-boxed accounts (12-week expiry). Spreadsheet with details to follow. Please "
            "confirm lead time needed.",
        ],
        next_best_actions=[
            "Initiate bulk onboarding workflow — confirm hardware availability, prepare account "
            "templates, and request the intern roster spreadsheet.",
            "Coordinate with HR for the intern roster, verify laptop inventory can support the "
            "batch, and begin account provisioning planning.",
        ],
        remediation_steps=[
            [
                "Request the full intern roster with names, departments, and start dates",
                "Verify laptop inventory can support the batch (order if needed)",
                "Create Entra ID accounts in bulk with intern-scoped permissions",
                "Assign M365 licenses with 12-week expiration",
                "Configure temporary badge access through facilities",
                "Schedule a Day 1 IT orientation session for the cohort",
                "Send welcome emails with setup instructions to all interns",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# gi-013  Department move — need desk reassignment and network setup
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="gi-013",
        category=Category.GENERAL,
        priority=Priority.P3,
        assigned_team=Team.NONE,
        needs_escalation=False,
        missing_information=[MissingInfo.NETWORK_LOCATION, MissingInfo.AFFECTED_USERS],
        subjects=[
            "Department move — need desk reassignment and network setup",
            "Team relocation: IT needs for floor move",
            "Office move — network and phone reconfiguration needed",
        ],
        descriptions=[
            "Our team of {count} people is moving from the {old_floor} floor to the {new_floor} "
            "floor next {date}. We'll need network drops verified, phones moved, and printers "
            "reconfigured for the new location. Can IT coordinate with facilities on this?",
            "The {department} department is relocating to Building {building}, Floor {floor} on "
            "{date}. We need to ensure all network jacks are active, docking stations are in "
            "place, and the shared printer on that floor is accessible. About {count} people "
            "are affected.",
        ],
        next_best_actions=[
            "Coordinate with facilities on the move timeline, verify network infrastructure at "
            "the destination, and plan the cutover.",
            "Assess the new floor's network readiness, confirm docking station and printer "
            "availability, and schedule the move support with the team.",
        ],
        remediation_steps=[
            [
                "Confirm move date, headcount, and destination floor details",
                "Verify network jack availability and activation at the new location",
                "Ensure docking stations and peripherals are in place at new desks",
                "Reconfigure printer mappings for the new floor",
                "Test network connectivity post-move and resolve any issues",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# gi-014  How do I encrypt a USB drive?
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="gi-014",
        category=Category.GENERAL,
        priority=Priority.P4,
        assigned_team=Team.NONE,
        needs_escalation=False,
        missing_information=[],
        subjects=[
            "How do I encrypt a USB drive?",
            "USB encryption — what tool should I use?",
            "Need to encrypt a flash drive before transferring files",
        ],
        descriptions=[
            "I need to copy some work files to a USB drive for an offsite meeting. Company policy "
            "says it needs to be encrypted. What's the approved method for encrypting USB drives? "
            "Is BitLocker To Go available on our laptops?",
            "Quick question — I have a USB stick I need to encrypt before putting any company data "
            "on it. What's the standard process? Do I need to request anything from IT first?",
        ],
        next_best_actions=[
            "Provide instructions for encrypting the USB drive using BitLocker To Go (or the "
            "company-approved encryption tool) and remind the user of the data handling policy.",
        ],
        remediation_steps=[
            [
                "Confirm BitLocker To Go is enabled on the user's device via group policy",
                "Provide step-by-step instructions for encrypting the USB drive",
                "Remind user of the removable media and data transfer policy",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# gi-015  VPN setup instructions for new remote worker
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="gi-015",
        category=Category.GENERAL,
        priority=Priority.P3,
        assigned_team=Team.NONE,
        needs_escalation=False,
        missing_information=[MissingInfo.DEVICE_INFO],
        subjects=[
            "VPN setup instructions for new remote worker",
            "Need help configuring VPN on my home computer",
            "Remote access setup — starting to work from home",
        ],
        descriptions=[
            "I've been approved for full-time remote work starting next week. I need instructions "
            "on how to set up the corporate VPN on my laptop. I haven't used VPN before — is there "
            "a client I need to install?",
            "My manager approved me to work remotely three days a week. Can someone walk me through "
            "the VPN setup? I'm on a {os_type} laptop and I'm not sure if the VPN client is "
            "already installed or if I need to download it.",
        ],
        next_best_actions=[
            "Provide VPN setup documentation, verify the user's device has the VPN client "
            "installed, and ensure their account is in the remote access group.",
            "Share the VPN setup guide, confirm the user is in the VPN-enabled security group, "
            "and assist with initial connection testing.",
        ],
        remediation_steps=[
            [
                "Verify user is a member of the remote access / VPN security group",
                "Confirm VPN client is installed (deploy via Intune if missing)",
                "Share VPN configuration guide specific to the user's OS",
                "Assist user with initial connection test and MFA enrollment if required",
                "Confirm user can reach internal resources over VPN",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# gi-016  How to set up email on personal phone?
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="gi-016",
        category=Category.GENERAL,
        priority=Priority.P4,
        assigned_team=Team.NONE,
        needs_escalation=False,
        missing_information=[MissingInfo.DEVICE_INFO],
        subjects=[
            "How to set up email on my personal phone?",
            "Can I access work email on my mobile device?",
            "Outlook mobile setup on personal phone",
        ],
        descriptions=[
            "I'd like to set up my work email on my personal iPhone so I can check messages when "
            "I'm away from my desk. Is that allowed, and if so, what app should I use? Do I need "
            "to enroll my phone in any management system?",
            "Can I get company email on my Android phone? I downloaded the Outlook app but it's "
            "asking me to enroll in Intune. Is that required? Will IT be able to see my personal "
            "stuff?",
        ],
        next_best_actions=[
            "Explain the BYOD/MDM policy, walk the user through Outlook mobile setup, and clarify "
            "what Intune enrollment means for personal devices.",
            "Share the mobile email setup guide and explain the company's BYOD policy including "
            "what device management does and does not access.",
        ],
        remediation_steps=[
            [
                "Explain the BYOD policy and Intune MAM-only vs. full enrollment options",
                "Guide user through installing Outlook mobile from the app store",
                "Assist with account sign-in and MFA prompt on the device",
                "Confirm email, calendar, and contacts sync successfully",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# gi-017  Budget approval for IT procurement
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="gi-017",
        category=Category.GENERAL,
        priority=Priority.P4,
        assigned_team=Team.NONE,
        needs_escalation=False,
        missing_information=[MissingInfo.BUSINESS_IMPACT],
        subjects=[
            "Budget approval process for IT procurement",
            "How to get approval for a hardware purchase?",
            "IT procurement — who approves and what's the process?",
        ],
        descriptions=[
            "My team needs to purchase {item_count} new {item_type} for an upcoming project. "
            "What's the procurement process? Do I submit a request through IT or go through "
            "our department budget owner? I need to know the approval chain and expected lead "
            "time.",
            "We want to buy some specialized equipment for the lab — estimated cost around "
            "${amount}. Where do I start with IT procurement? Is there a portal, or do I email "
            "someone? Need to understand the full approval workflow.",
        ],
        next_best_actions=[
            "Explain the IT procurement workflow, including the approval chain and any spend "
            "thresholds that require additional sign-off.",
            "Provide the procurement request form and outline the approval process including "
            "estimated timelines.",
        ],
        remediation_steps=[
            [
                "Share the IT procurement request form or portal link",
                "Explain the approval workflow and spend thresholds",
                "Clarify which budget owner needs to authorize the purchase",
                "Provide estimated lead times for standard and non-standard equipment",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# gi-018  Office relocation — IT infrastructure planning
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="gi-018",
        category=Category.GENERAL,
        priority=Priority.P3,
        assigned_team=Team.NONE,
        needs_escalation=False,
        missing_information=[
            MissingInfo.AFFECTED_USERS,
            MissingInfo.NETWORK_LOCATION,
            MissingInfo.BUSINESS_IMPACT,
        ],
        subjects=[
            "Office relocation — IT infrastructure planning needed",
            "New office buildout: IT requirements",
            "Moving to a new office — need IT planning support",
        ],
        descriptions=[
            "We're relocating our {city} office to a new building in {month}. Approximately "
            "{headcount} staff will move. We need IT to plan the network infrastructure, server "
            "room setup, phone system, and workstation deployment for the new site. Can we set up "
            "a planning meeting?",
            "The {department} group is expanding into a new floor in Building {building}. We need "
            "to scope out the IT infrastructure build: cabling, wireless APs, conference room AV, "
            "and print services. This will serve about {headcount} employees. Target move-in is "
            "{date}.",
        ],
        next_best_actions=[
            "Schedule an IT infrastructure planning meeting with the project lead, facilities, "
            "and network engineering to scope requirements for the new site.",
            "Engage the network operations and endpoint teams to assess infrastructure needs and "
            "create a project plan with milestones.",
        ],
        remediation_steps=[
            [
                "Schedule an initial scoping meeting with the requester and facilities",
                "Assess network, cabling, wireless, and AV requirements for the new space",
                "Create an IT infrastructure project plan with milestones",
                "Coordinate procurement of any new equipment needed",
                "Execute buildout and testing before the move date",
                "Support staff during the move and resolve post-move issues",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# gi-019  How to access IT self-service portal?
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="gi-019",
        category=Category.GENERAL,
        priority=Priority.P4,
        assigned_team=Team.NONE,
        needs_escalation=False,
        missing_information=[],
        subjects=[
            "How do I access the IT self-service portal?",
            "Where is the IT service desk portal?",
            "Link to submit IT requests online?",
        ],
        descriptions=[
            "I was told I can submit IT requests, check ticket status, and browse the knowledge "
            "base through a self-service portal, but I don't have the URL. Can you share the "
            "link and let me know how to log in?",
            "Is there an online portal where I can manage my IT tickets, request software, and "
            "track hardware requests? I've been calling the help desk for everything and I'd "
            "prefer to use a portal if one exists.",
        ],
        next_best_actions=[
            "Provide the IT self-service portal URL and login instructions.",
            "Share the portal link and offer a quick walkthrough of common features.",
        ],
        remediation_steps=[
            [
                "Share the self-service portal URL",
                "Confirm the user can authenticate (uses corporate SSO)",
                "Briefly explain key portal features: ticket submission, status tracking, KB",
                "Recommend bookmarking the portal for future use",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# gi-020  Request for IT orientation session for new team
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="gi-020",
        category=Category.GENERAL,
        priority=Priority.P4,
        assigned_team=Team.NONE,
        needs_escalation=False,
        missing_information=[MissingInfo.AFFECTED_USERS],
        subjects=[
            "Request for IT orientation session for new team",
            "Can IT do a walkthrough for our newly formed team?",
            "IT onboarding presentation request",
        ],
        descriptions=[
            "We just formed a new cross-functional team of {count} people pulled from different "
            "departments. Many of them aren't familiar with our standard IT tools and processes. "
            "Can we schedule a 1-hour IT orientation covering the basics — VPN, M365, self-service "
            "portal, and security best practices?",
            "Our department recently reorganized and we have several people who haven't had a "
            "proper IT orientation. Could the help desk team run a short session covering how to "
            "submit tickets, use the knowledge base, and follow IT security policies? We're "
            "flexible on timing.",
        ],
        next_best_actions=[
            "Coordinate with the IT training team to schedule an orientation session and gather "
            "attendee details.",
            "Schedule an IT orientation, prepare standard onboarding materials, and confirm "
            "logistics with the requester.",
        ],
        remediation_steps=[
            [
                "Gather team size, preferred dates, and specific topics of interest",
                "Schedule the orientation session and book a meeting room or Teams call",
                "Prepare materials covering VPN, M365, self-service portal, and security basics",
                "Deliver the session and share follow-up resources",
                "Collect feedback and offer ongoing support channels",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# gi-021  Onboarding + offboarding in the same ticket
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="gi-021",
        category=Category.GENERAL,
        priority=Priority.P2,
        assigned_team=Team.IAM,
        needs_escalation=False,
        missing_information=[MissingInfo.TIMESTAMP, MissingInfo.AFFECTED_SYSTEM],
        subjects=[
            "New hire replacing departing employee — need simultaneous setup and teardown",
            "Employee transition: offboard John, onboard Jane on same day",
            "Replacement hire — need accounts deprovisioned and provisioned together",
        ],
        descriptions=[
            "We have an employee leaving on Friday and their replacement starting the same day. "
            "I need the departing employee's accounts disabled, laptop wiped, and access revoked "
            "across all systems (Azure AD, SAP, Salesforce, VPN). Simultaneously, the new hire "
            "needs a laptop provisioned, accounts created in the same systems, and access to the "
            "same shared mailbox and Teams channels. Can this be coordinated as one request?",
            "Our team lead is departing and a new person is starting as a direct replacement. We "
            "need to transfer ownership of several shared resources — a Teams channel, a SharePoint "
            "site, and a shared mailbox — from the departing employee to the new hire. We also need "
            "standard offboarding for the leaver and full onboarding for the joiner. The transition "
            "date is next Monday.",
        ],
        next_best_actions=[
            "Create linked onboarding and offboarding work items. Coordinate IAM, Endpoint, and "
            "Enterprise Apps teams to execute both workflows on the transition date.",
            "Gather details for both employees and initiate parallel onboarding/offboarding "
            "checklists with a shared target date.",
        ],
        remediation_steps=[
            [
                "Confirm transition date and gather details for both employees",
                "Initiate offboarding checklist: disable accounts, revoke access, schedule laptop wipe",
                "Initiate onboarding checklist: create accounts, provision laptop, assign licenses",
                "Transfer ownership of shared resources (mailbox, Teams, SharePoint) to new hire",
                "Coordinate with IAM, Endpoint, and Enterprise Apps for same-day execution",
                "Verify both workflows completed successfully on transition date",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# gi-022  IT policy question hinting at a real issue
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="gi-022",
        category=Category.GENERAL,
        priority=Priority.P3,
        assigned_team=Team.NONE,
        needs_escalation=False,
        missing_information=[MissingInfo.BUSINESS_IMPACT],
        subjects=[
            "Just curious — what happens if someone bypasses the DLP policy?",
            "Hypothetical question about data loss prevention controls",
            "Question about DLP enforcement gaps",
        ],
        descriptions=[
            "I have a theoretical question. What happens if someone finds a way to move files "
            "outside of our DLP-protected environment? Like, say they use a personal cloud storage "
            "account or a USB drive that somehow isn't blocked? I'm asking because I want to "
            "understand how robust our controls are. Not planning anything, just curious.",
            "Hey, I noticed that our DLP policy blocks uploading to personal OneDrive, but what "
            "about other cloud providers like Mega or WeTransfer? Has anyone tested whether those "
            "are blocked too? Asking for awareness purposes — I want to make sure our sensitive "
            "data is actually protected.",
        ],
        next_best_actions=[
            "Treat as a genuine policy inquiry. Provide a general explanation of DLP coverage "
            "without revealing specific control gaps. Optionally flag for security awareness.",
            "Answer the policy question at a high level and note the inquiry for the security "
            "team's awareness.",
        ],
        remediation_steps=[
            [
                "Provide a high-level explanation of DLP policy coverage",
                "Avoid disclosing specific technical details of enforcement mechanisms",
                "Note the inquiry in the ticket for security team visibility",
                "If the user has a legitimate business need, direct them to the security team",
                "Recommend the user complete the data handling awareness training",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# gi-023  Request in wrong language with broken English
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="gi-023",
        category=Category.GENERAL,
        priority=Priority.P3,
        assigned_team=Team.NONE,
        needs_escalation=False,
        missing_information=[MissingInfo.AFFECTED_SYSTEM, MissingInfo.ERROR_MESSAGE],
        subjects=[
            "コンピュータの問題 — computer problem please help",
            "PC trouble — すみません、英語が苦手です",
            "ヘルプ needed with laptop — sorry bad English",
        ],
        descriptions=[
            "すみません、私のパソコンが動かなくなりました。朝から画面がフリーズしています。"
            "Sorry, my computer is not working. Since morning the screen is... 止まっている... "
            "frozen? I try restart but same problem. Blue screen sometimes appears with error code "
            "but I cannot read it fast enough. 助けてください。 My employee ID is E-29471. I am in "
            "Tokyo office, 3rd floor.",
            "Hello, I am sorry for my English. 私のラップトップでOutlookが開けません。Error message "
            "が出ますが、日本語で書いてあるのでスクリーンショットを送ります。I cannot open Outlook "
            "since yesterday. パスワードは変えていません。Please help, I have important meeting today. "
            "東京オフィスの田中です。",
        ],
        next_best_actions=[
            "Acknowledge the request and respond in both English and Japanese if possible. "
            "Gather device details and the specific error message via screenshot.",
            "Route to a support agent with Japanese language capability or use translation "
            "services. Collect device info and error details.",
        ],
        remediation_steps=[
            [
                "Acknowledge the ticket and respond bilingually if possible",
                "Request a screenshot of any error messages",
                "Gather device model, OS version, and employee ID for lookup",
                "If language barrier persists, engage a Japanese-speaking support agent",
                "Troubleshoot the reported issue once details are clarified",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# gi-024  Ticket referencing multiple prior unresolved tickets
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="gi-024",
        category=Category.GENERAL,
        priority=Priority.P2,
        assigned_team=Team.NONE,
        needs_escalation=True,
        missing_information=[MissingInfo.AFFECTED_SYSTEM, MissingInfo.STEPS_TO_REPRODUCE],
        subjects=[
            "FIFTH time reporting this — INC-1234, INC-2345, INC-3456, INC-4567, INC-5678",
            "Repeated issue — none of my previous 5 tickets were resolved",
            "Ongoing unresolved problem — ticket history inside",
        ],
        descriptions=[
            "I've reported this issue 5 times now and it's still not fixed. Here are my previous "
            "tickets: INC-1234, INC-2345, INC-3456, INC-4567, and INC-5678. Each time I'm told "
            "it's resolved but the problem comes back within a week. I'm beyond frustrated. "
            "Somebody needs to actually look at the root cause instead of applying band-aid fixes. "
            "My manager is aware and is ready to escalate to the CIO if this isn't handled properly.",
            "This is my SIXTH ticket for the same problem. Previous tickets: INC-1234, INC-2345, "
            "INC-3456, INC-4567, INC-5678. Every single one was closed as 'resolved' but nothing "
            "was actually fixed. I keep losing access to the shared drive every few days and have "
            "to call in each time. I've wasted hours on this. Please don't just reset my permissions "
            "again — find out WHY this keeps happening.",
        ],
        next_best_actions=[
            "Review all referenced tickets to identify the recurring pattern. Escalate for root "
            "cause analysis rather than applying another temporary fix.",
            "Consolidate the ticket history, identify the common failure pattern, and assign to "
            "a senior engineer for root cause investigation.",
        ],
        remediation_steps=[
            [
                "Pull up all referenced tickets (INC-1234 through INC-5678) and review resolution notes",
                "Identify the common pattern — what was fixed each time and why it recurred",
                "Escalate to a senior engineer or team lead for root cause analysis",
                "Apply a permanent fix rather than a temporary workaround",
                "Follow up with the user after 1 week and 1 month to confirm stability",
                "Update the knowledge base if the root cause reveals a systemic issue",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# gi-025  Intern asking about everything at once
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="gi-025",
        category=Category.GENERAL,
        priority=Priority.P4,
        assigned_team=Team.NONE,
        needs_escalation=False,
        missing_information=[MissingInfo.DEVICE_INFO, MissingInfo.CONTACT_INFO],
        subjects=[
            "New intern — how does ANYTHING work here?",
            "First day questions: WiFi, email, software, badge, everything",
            "Hi! I'm new and I need help with literally everything",
        ],
        descriptions=[
            "Hi! I'm a new intern starting today and I have no idea how anything works. How do I "
            "connect to WiFi? How do I set up my email on my phone? Where do I go to install "
            "software like VS Code and Python? Also, how do I get a badge for building access? "
            "And where's the cafeteria? Sorry for all the questions — nobody gave me an onboarding "
            "guide and my manager is out today.",
            "Hello, I'm a summer intern and today is my first day. I have a laptop but I can't "
            "figure out how to get on the network. I also need to set up Teams, Outlook, and some "
            "development tools. Is there a guide or someone who can walk me through everything? "
            "I tried asking around but everyone seems busy. Also, do I need a VPN to work from "
            "home? And how do I book a desk?",
        ],
        next_best_actions=[
            "Provide the standard new-hire onboarding guide covering WiFi, email, software, "
            "badge access, and common resources. Offer to schedule a walkthrough.",
            "Share the intern onboarding checklist and IT self-service portal link. Address "
            "the most urgent needs (WiFi, email) first.",
        ],
        remediation_steps=[
            [
                "Share the new-hire IT onboarding guide and self-service portal link",
                "Help connect to corporate WiFi (provide SSID and auth instructions)",
                "Walk through email setup on mobile and desktop",
                "Provide the software request process for development tools",
                "Direct to facilities for badge and building access questions",
                "Offer a follow-up session if the intern has more questions",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# gi-026  New employee asking about VPN setup process
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="gi-026",
        category=Category.GENERAL,
        priority=Priority.P4,
        assigned_team=Team.NONE,
        needs_escalation=False,
        missing_information=[MissingInfo.CONTACT_INFO, MissingInfo.PREVIOUS_TICKET_ID],
        subjects=[
            "How do I set up VPN access?",
            "New hire — need help getting VPN configured",
            "VPN setup process for new employees",
        ],
        descriptions=[
            "Hi there, I just started last Monday and I need to set up VPN so I can work from home "
            "on Fridays. My manager mentioned there's a specific client I need to install and some "
            "certificates to configure, but I'm not sure where to start. I don't have any previous "
            "tickets open for this. Could someone walk me through the process?",
            "Hello, I'm a new employee in the marketing department and I was told I need VPN access "
            "for remote work days. I tried searching the intranet but the articles I found seem "
            "outdated. Is there a current guide or can someone help me get set up? I'm not sure who "
            "my IT contact is yet since I just joined.",
        ],
        next_best_actions=[
            "Provide the VPN setup guide for the user's operating system and confirm the correct "
            "VPN client to download. Request employee contact details for follow-up.",
            "Share the self-service VPN enrollment portal link and verify the user's remote access "
            "entitlements in the directory.",
        ],
        remediation_steps=[
            [
                "Collect the employee's contact information and employee ID",
                "Share the VPN setup knowledge base article for their OS",
                "Walk through VPN client installation and certificate enrollment",
                "Verify successful VPN connection and confirm remote access works",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# gi-027  IT asset return process for departing employee
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="gi-027",
        category=Category.GENERAL,
        priority=Priority.P4,
        assigned_team=Team.NONE,
        needs_escalation=False,
        missing_information=[MissingInfo.SCREENSHOT_OR_ATTACHMENT, MissingInfo.CONTACT_INFO],
        subjects=[
            "How do I return IT assets before my last day?",
            "Departing employee — asset return process question",
            "IT equipment return for offboarding",
        ],
        descriptions=[
            "Hi, my last day is next Friday and I need to return my laptop, monitor, keyboard, and "
            "docking station. I pulled up my asset list in the self-service portal but I'm not sure "
            "if it's complete — I think I also have a spare mouse somewhere. What's the process for "
            "returning everything? Do I ship it or drop it off somewhere? I tried attaching a "
            "screenshot of my asset list but the upload didn't seem to work.",
            "Hello, I'm leaving the company at the end of the month and my manager said I need to "
            "coordinate IT asset returns with your team. I have a laptop, two monitors, and some "
            "peripherals. Where should I bring them and is there a checklist I should follow? I'd "
            "like to make sure I don't miss anything so it doesn't delay my offboarding.",
        ],
        next_best_actions=[
            "Provide the IT asset return checklist and schedule a drop-off or shipping label. "
            "Request a screenshot of the employee's current asset inventory for reconciliation.",
            "Share the offboarding asset return guide and confirm the list of assets assigned "
            "to the employee in the asset management system.",
        ],
        remediation_steps=[
            [
                "Request the employee's contact information and last working date",
                "Ask for a screenshot of their asset list from the self-service portal",
                "Provide the asset return checklist and drop-off or shipping instructions",
                "Coordinate with the offboarding team to confirm all assets are accounted for",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# gi-028  Which authentication methods are supported for remote access?
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="gi-028",
        category=Category.GENERAL,
        priority=Priority.P4,
        assigned_team=Team.NONE,
        needs_escalation=False,
        missing_information=[MissingInfo.AUTHENTICATION_METHOD, MissingInfo.DEVICE_INFO],
        subjects=[
            "What authentication methods are supported for remote access?",
            "Question about MFA options for VPN and remote login",
            "Supported auth methods for working remotely",
        ],
        descriptions=[
            "I'm trying to understand which authentication methods are supported for remote access "
            "to company systems. I currently use a password plus SMS codes but I heard we're moving "
            "to authenticator apps or hardware keys. Can someone clarify what options are available "
            "and whether I need to re-enroll? I'm not sure if it matters what device I'm using.",
            "Quick question — I want to switch from SMS-based two-factor to something more secure "
            "for remote access. Does the company support FIDO2 security keys or just the "
            "authenticator app? I work from both a Windows laptop and a Mac and I want to make sure "
            "whatever I pick works on both. Where can I find the official list of supported methods?",
        ],
        next_best_actions=[
            "Provide the list of supported authentication methods for remote access and link to "
            "the MFA enrollment portal. Ask which device the user connects from.",
            "Share the remote access authentication policy document and guide the user through "
            "enrolling in their preferred MFA method.",
        ],
        remediation_steps=[
            [
                "Ask the user which device(s) they use for remote access",
                "Provide the supported authentication methods documentation",
                "Guide the user to the MFA enrollment or re-enrollment portal",
                "Confirm the new authentication method works on their device(s)",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# gi-029  Software request process — intermittent portal access
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="gi-029",
        category=Category.GENERAL,
        priority=Priority.P3,
        assigned_team=Team.NONE,
        needs_escalation=False,
        missing_information=[MissingInfo.REPRODUCTION_FREQUENCY, MissingInfo.SCREENSHOT_OR_ATTACHMENT],
        subjects=[
            "How do I request new software? Portal seems flaky",
            "Software request process — portal keeps timing out",
            "Need to install licensed software but request portal is unreliable",
        ],
        descriptions=[
            "Hi, I need to request a license for Adobe Creative Cloud for a design project. I know "
            "there's a self-service portal for software requests but every time I try to load it, "
            "the page either times out or shows a blank screen. It's been happening on and off for "
            "the past two days. Can someone tell me the correct process and maybe submit the request "
            "on my behalf? I tried to screenshot the error but it's intermittent.",
            "Hello, my team needs access to Tableau Desktop and I was told to use the software "
            "request portal. The portal loads sometimes but other times it just hangs on a spinner. "
            "I'm not sure if it's a browser issue or something on the server side. Could you let me "
            "know the steps for requesting software and whether there's an alternative way to submit "
            "if the portal is down?",
        ],
        next_best_actions=[
            "Provide the software request process documentation and offer to submit the request "
            "on the user's behalf. Ask how frequently the portal issue occurs.",
            "Share the alternative software request method (email or form) and log the portal "
            "intermittent access issue for investigation.",
        ],
        remediation_steps=[
            [
                "Ask the user how often the portal issue occurs and for a screenshot if possible",
                "Provide the software request process steps and any alternative submission methods",
                "Submit or assist with the software request if the portal is unavailable",
                "Log the portal reliability issue for the web services team to investigate",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# gi-030  Follow-up on training session enrollment
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="gi-030",
        category=Category.GENERAL,
        priority=Priority.P4,
        assigned_team=Team.NONE,
        needs_escalation=False,
        missing_information=[MissingInfo.PREVIOUS_TICKET_ID, MissingInfo.CONTACT_INFO],
        subjects=[
            "Follow-up: training session enrollment status",
            "Checking on my training enrollment request",
            "Any update on the IT security training I signed up for?",
        ],
        descriptions=[
            "Hi, I submitted a request a couple of weeks ago to enroll in the advanced IT security "
            "training session that's scheduled for next month. I never received a confirmation email "
            "and I'm not sure if my spot was reserved. I don't remember the ticket number "
            "unfortunately. Could someone look into this for me? My manager approved it verbally "
            "but I'm not sure the approval was recorded anywhere.",
            "Hello, I'm following up on a training enrollment I requested recently — I think it was "
            "the cloud administration certification course. I got an auto-reply saying the request "
            "was received but nothing since then. I want to make sure I'm still on the list because "
            "the class has limited seats. I can't find the original ticket ID. Can you check the "
            "status using my name or email?",
        ],
        next_best_actions=[
            "Look up the user's previous training enrollment request by name or email and provide "
            "a status update. Confirm contact details for follow-up.",
            "Search for the original ticket in the system and verify enrollment status. Ask the "
            "user for any reference details they may have.",
        ],
        remediation_steps=[
            [
                "Ask the user for their name, email, or any reference details from the original request",
                "Search the ticketing system for the previous training enrollment request",
                "Provide the enrollment status and confirmation details",
                "Update the user's contact information if needed for future notifications",
            ],
        ],
    )
)
