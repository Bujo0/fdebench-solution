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
