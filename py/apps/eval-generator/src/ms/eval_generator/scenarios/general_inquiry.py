# Copyright (c) Microsoft. All rights reserved.
"""General Inquiry category scenarios for eval dataset."""

from ms.eval_generator.scenarios._base import ScenarioDefinition
from ms.eval_generator.scenarios._base import ScenarioGold

GENERAL_INQUIRY_SCENARIOS: list[ScenarioDefinition] = [
    # ------------------------------------------------------------------
    # 1. How to set up VPN for the first time
    # ------------------------------------------------------------------
    ScenarioDefinition(
        scenario_id="general-001",
        subjects=(
            "How do I set up VPN on my laptop?",
            "First-time VPN configuration help needed",
            "Need instructions for connecting to company VPN",
        ),
        descriptions=(
            "Hi, I just joined Contoso last week and I need to work from home tomorrow. "
            "How do I set up the VPN on my laptop? I don't see any VPN software installed.",
            "I'm a new hire in the Wealth Management division and my manager mentioned I need "
            "to configure VPN access for remote work. Could someone point me to the setup guide "
            "or walk me through the steps? I have a Windows 11 laptop.",
        ),
        gold=ScenarioGold(
            category="General Inquiry",
            priority="P4",
            assigned_team="Network Operations",
            needs_escalation=False,
            missing_information=(),
            next_best_action="Provide VPN setup documentation and GlobalProtect installation guide",
            remediation_steps=(
                "Share the VPN setup guide from the IT self-service portal",
                "Direct the user to install GlobalProtect from the Software Center",
                "Provide instructions for first-time VPN authentication",
            ),
        ),
    ),
    # ------------------------------------------------------------------
    # 2. Request for ergonomic keyboard
    # ------------------------------------------------------------------
    ScenarioDefinition(
        scenario_id="general-002",
        subjects=(
            "Ergonomic keyboard request",
            "Can I get an ergonomic keyboard?",
        ),
        descriptions=(
            "I've been having some wrist discomfort lately and my doctor recommended an ergonomic "
            "keyboard. Is this something IT can provide or do I need to go through a different "
            "department? Thanks.",
            "Requesting an ergonomic keyboard for my workstation on the 4th floor. I have a "
            "medical note from my physician if that's required. Please let me know the process.",
            "Hi team — I'd like to request a Microsoft Sculpt ergonomic keyboard. My current "
            "standard keyboard is causing strain during long typing sessions.",
        ),
        gold=ScenarioGold(
            category="General Inquiry",
            priority="P4",
            assigned_team="Endpoint Engineering",
            needs_escalation=False,
            missing_information=(),
            next_best_action="Initiate ergonomic equipment request through the standard procurement process",
            remediation_steps=(
                "Confirm whether a medical accommodation form is required",
                "Submit the equipment request through the IT procurement portal",
                "Coordinate delivery and setup with the user",
            ),
        ),
    ),
    # ------------------------------------------------------------------
    # 3. IT equipment refresh cycle
    # ------------------------------------------------------------------
    ScenarioDefinition(
        scenario_id="general-003",
        subjects=(
            "When is my laptop due for a refresh?",
            "Question about IT equipment refresh cycle",
        ),
        descriptions=(
            "My laptop is about three years old and it's getting pretty slow. What's the "
            "equipment refresh cycle at Contoso? Am I eligible for a new one?",
            "I heard that we get new laptops every 3-4 years. My ThinkPad is from 2021 and "
            "the battery barely lasts an hour. How do I check if I'm up for a refresh?",
            "Just wondering what the hardware replacement schedule looks like. My current "
            "machine is struggling with our new analytics tools and I'm not sure if I should "
            "request a repair or wait for the refresh.",
        ),
        gold=ScenarioGold(
            category="General Inquiry",
            priority="P4",
            assigned_team="Endpoint Engineering",
            needs_escalation=False,
            missing_information=(),
            next_best_action="Look up the user's device age in the asset inventory and advise on refresh eligibility",
            remediation_steps=(
                "Check the asset management system for the device's purchase date",
                "Inform the user of the standard 4-year refresh cycle policy",
                "If eligible, initiate the hardware refresh workflow",
            ),
        ),
    ),
    # ------------------------------------------------------------------
    # 4. How to enable auto-forward in Outlook
    # ------------------------------------------------------------------
    ScenarioDefinition(
        scenario_id="general-004",
        subjects=(
            "How to set up auto-forward in Outlook",
            "Auto-forwarding emails to external address",
        ),
        descriptions=(
            "I need to set up auto-forwarding on my Outlook mailbox to forward certain emails "
            "to my team lead while I'm on parental leave. Can someone tell me how?",
            "Is it possible to auto-forward my Contoso emails to my personal Gmail while I'm "
            "traveling next month? I tried the rules but it didn't seem to work for external "
            "addresses.",
        ),
        gold=ScenarioGold(
            category="General Inquiry",
            priority="P4",
            assigned_team="Enterprise Applications",
            needs_escalation=False,
            missing_information=(),
            next_best_action=(
                "Explain Outlook forwarding rules and clarify external forwarding policy restrictions"
            ),
            remediation_steps=(
                "Provide instructions for setting up inbox rules in Outlook",
                "Clarify that external auto-forwarding may be blocked by DLP policy",
                "Suggest internal forwarding or delegation as an alternative if external is blocked",
            ),
        ),
    ),
    # ------------------------------------------------------------------
    # 5. Training request for Power BI
    # ------------------------------------------------------------------
    ScenarioDefinition(
        scenario_id="general-005",
        subjects=(
            "Power BI training resources",
            "Request for Power BI training",
            "How to learn Power BI at Contoso",
        ),
        descriptions=(
            "My manager wants our team to start using Power BI for quarterly reporting. None of "
            "us have used it before. Does Contoso offer any training sessions or online courses "
            "for Power BI?",
            "I'd like to take a Power BI course to improve my data visualization skills. Are "
            "there any IT-sponsored training programs available? Happy to do self-paced or "
            "instructor-led.",
        ),
        gold=ScenarioGold(
            category="General Inquiry",
            priority="P4",
            assigned_team="Enterprise Applications",
            needs_escalation=False,
            missing_information=(),
            next_best_action="Share available Power BI training resources and enrollment instructions",
            remediation_steps=(
                "Provide links to internal Power BI training on the learning portal",
                "Share information about upcoming instructor-led sessions if available",
                "Confirm the user has a Power BI Pro license assigned",
            ),
        ),
    ),
    # ------------------------------------------------------------------
    # 6. Approved software list
    # ------------------------------------------------------------------
    ScenarioDefinition(
        scenario_id="general-006",
        subjects=(
            "Where is the approved software list?",
            "What software am I allowed to install?",
        ),
        descriptions=(
            "I need to install a PDF editor for work but I'm not sure what's approved. Where "
            "can I find the list of software that's been vetted by IT?",
            "Quick question — is there a catalog somewhere of pre-approved applications? I want "
            "to check if Notepad++ and 7-Zip are on the list before I submit a request.",
            "A colleague told me there's an approved software list on the intranet but I can't "
            "find it. Can you send me the link?",
        ),
        gold=ScenarioGold(
            category="General Inquiry",
            priority="P4",
            assigned_team="Endpoint Engineering",
            needs_escalation=False,
            missing_information=(),
            next_best_action="Direct the user to the approved software catalog on the IT portal",
            remediation_steps=(
                "Share the link to the approved software list on the IT self-service portal",
                "Explain how to request software not on the approved list",
                "Mention that Software Center has pre-approved apps ready to install",
            ),
        ),
    ),
    # ------------------------------------------------------------------
    # 7. Remote work equipment policy
    # ------------------------------------------------------------------
    ScenarioDefinition(
        scenario_id="general-007",
        subjects=(
            "Remote work equipment policy question",
            "What equipment does Contoso provide for WFH?",
        ),
        descriptions=(
            "I've been approved for a hybrid work arrangement — 3 days remote, 2 in office. "
            "Does Contoso provide any equipment for my home office, like a monitor or docking "
            "station? What's the policy?",
            "Now that we're officially hybrid, I wanted to ask about the remote work equipment "
            "stipend. My team lead mentioned something about a budget for home office gear but "
            "wasn't sure of the details. Can IT clarify?",
        ),
        gold=ScenarioGold(
            category="General Inquiry",
            priority="P4",
            assigned_team="Endpoint Engineering",
            needs_escalation=False,
            missing_information=(),
            next_best_action="Provide the remote work equipment policy documentation and stipend details",
            remediation_steps=(
                "Share the remote work equipment policy document",
                "Explain the equipment stipend amount and eligible items",
                "Direct the user to the procurement portal for ordering",
            ),
        ),
    ),
    # ------------------------------------------------------------------
    # 8. External SharePoint sharing
    # ------------------------------------------------------------------
    ScenarioDefinition(
        scenario_id="general-008",
        subjects=(
            "How to share a SharePoint site with external partners",
            "External sharing on SharePoint",
        ),
        descriptions=(
            "We're working on a joint project with an external audit firm and need to share a "
            "SharePoint site with them. What's the process for enabling external sharing? Do I "
            "need special permissions?",
            "Our team needs to give read access to a SharePoint document library to some "
            "consultants from Deloitte. I tried sharing but got an error saying external "
            "sharing is disabled. How do I get this enabled?",
            "Is it possible to share a SharePoint Online site with people outside the "
            "organization? If so, who do I talk to about setting that up?",
        ),
        gold=ScenarioGold(
            category="General Inquiry",
            priority="P4",
            assigned_team="Data Platform",
            needs_escalation=False,
            missing_information=(),
            next_best_action="Explain the external sharing request process and compliance requirements",
            remediation_steps=(
                "Explain the external sharing policy and approval process",
                "Provide the external collaboration request form",
                "Ensure data classification review is completed before enabling sharing",
            ),
        ),
    ),
    # ------------------------------------------------------------------
    # 9. Next Windows update rollout
    # ------------------------------------------------------------------
    ScenarioDefinition(
        scenario_id="general-009",
        subjects=(
            "When is the next Windows update?",
            "Windows update schedule question",
            "Upcoming Windows update rollout?",
        ),
        descriptions=(
            "My team is in the middle of a big project and we can't afford unexpected reboots. "
            "When is the next Windows update rollout scheduled? Can we defer it?",
            "Just curious about the patch Tuesday schedule — when will the next round of "
            "Windows updates be pushed to our machines? Last time it rebooted during a client "
            "presentation and it was embarrassing.",
        ),
        gold=ScenarioGold(
            category="General Inquiry",
            priority="P4",
            assigned_team="Endpoint Engineering",
            needs_escalation=False,
            missing_information=(),
            next_best_action="Share the patch deployment schedule and deferral options",
            remediation_steps=(
                "Provide the current month's patch deployment schedule",
                "Explain how to use the deferral window for non-critical updates",
                "Advise the user to save work before scheduled maintenance windows",
            ),
        ),
    ),
    # ------------------------------------------------------------------
    # 10. How to submit expense reports in SAP
    # ------------------------------------------------------------------
    ScenarioDefinition(
        scenario_id="general-010",
        subjects=(
            "How do I submit expenses in SAP?",
            "Expense report submission help",
        ),
        descriptions=(
            "I just got back from a client visit and need to submit my travel expenses. I've "
            "never used SAP Concur before — can someone walk me through it or send me a guide?",
            "I'm trying to submit an expense report in SAP but the interface is super confusing. "
            "I attached my receipts but I can't figure out how to link them to the right cost "
            "center. Help!",
            "New employee here. Where do I go to submit expense reports? Someone mentioned SAP "
            "but I don't even know how to access it.",
        ),
        gold=ScenarioGold(
            category="General Inquiry",
            priority="P4",
            assigned_team="Enterprise Applications",
            needs_escalation=False,
            missing_information=(),
            next_best_action="Provide SAP Concur user guide and expense submission instructions",
            remediation_steps=(
                "Share the SAP Concur quick-start guide from the finance portal",
                "Provide a link to the expense report training video",
                "Direct the user to their department's finance coordinator for cost center info",
            ),
        ),
    ),
    # ------------------------------------------------------------------
    # 11. IT onboarding checklist for new manager
    # ------------------------------------------------------------------
    ScenarioDefinition(
        scenario_id="general-011",
        subjects=(
            "IT onboarding checklist for new hires",
            "New manager — need IT onboarding info",
        ),
        descriptions=(
            "I'm a new manager in the Commercial Banking division and I have two analysts "
            "starting next month. Is there an IT onboarding checklist I should follow to make "
            "sure they have everything they need on day one?",
            "Starting as a team lead soon and want to make sure my new direct reports get "
            "set up properly with IT. What accounts, hardware, and access do I need to "
            "request for them? Is there a standard checklist?",
            "We're hiring three new people for Q2. What's the process to get their laptops, "
            "email accounts, and badge access sorted before their start date?",
        ),
        gold=ScenarioGold(
            category="General Inquiry",
            priority="P4",
            assigned_team="Identity & Access Management",
            needs_escalation=False,
            missing_information=(),
            next_best_action="Provide the manager's IT onboarding checklist and new hire request form",
            remediation_steps=(
                "Share the IT onboarding checklist for managers",
                "Provide the new hire provisioning request form",
                "Explain lead time requirements for hardware and account setup",
            ),
        ),
    ),
    # ------------------------------------------------------------------
    # 12. Request for second monitor
    # ------------------------------------------------------------------
    ScenarioDefinition(
        scenario_id="general-012",
        subjects=(
            "Request for a second monitor",
            "Can I get a dual monitor setup?",
        ),
        descriptions=(
            "I work with a lot of spreadsheets and having a single monitor is really limiting "
            "my productivity. Can I request a second monitor for my desk?",
            "Our team recently moved to the 6th floor and my old desk had two monitors but the "
            "new one only has one. Can IT set me up with a second display? I have the desk "
            "space for it.",
        ),
        gold=ScenarioGold(
            category="General Inquiry",
            priority="P4",
            assigned_team="Endpoint Engineering",
            needs_escalation=False,
            missing_information=(),
            next_best_action="Process the second monitor request through the equipment portal",
            remediation_steps=(
                "Submit an equipment request for an additional monitor",
                "Verify the user's docking station supports dual displays",
                "Schedule delivery and installation at the user's workstation",
            ),
        ),
    ),
    # ------------------------------------------------------------------
    # 13. WiFi password for guest network
    # ------------------------------------------------------------------
    ScenarioDefinition(
        scenario_id="general-013",
        subjects=(
            "Guest WiFi password?",
            "What's the WiFi password for visitors?",
            "Need guest network access for client meeting",
        ),
        descriptions=(
            "I have external clients visiting our office tomorrow for a workshop. What's the "
            "WiFi password for the guest network so I can share it with them?",
            "Quick one — what's the current guest WiFi password? I have a vendor coming in "
            "for a meeting and they'll need internet access.",
        ),
        gold=ScenarioGold(
            category="General Inquiry",
            priority="P4",
            assigned_team="Network Operations",
            needs_escalation=False,
            missing_information=(),
            next_best_action="Provide the current guest WiFi credentials and usage policy",
            remediation_steps=(
                "Share the current guest network SSID and access credentials",
                "Remind the user of the acceptable use policy for guest network",
                "Mention that guest access expires after 24 hours and must be re-authenticated",
            ),
        ),
    ),
    # ------------------------------------------------------------------
    # 14. How to encrypt a USB drive
    # ------------------------------------------------------------------
    ScenarioDefinition(
        scenario_id="general-014",
        subjects=(
            "How do I encrypt a USB drive?",
            "USB drive encryption instructions needed",
        ),
        descriptions=(
            "I need to transfer some sensitive financial reports to our off-site backup "
            "location using a USB drive. How do I encrypt the drive? Is there a company "
            "tool for this?",
            "My manager asked me to encrypt a USB flash drive before copying client data "
            "onto it. I've never done this before. Is BitLocker the right tool? Can someone "
            "provide step-by-step instructions?",
            "What's the approved method for encrypting removable media at Contoso? I want "
            "to make sure I'm compliant with our data protection policies.",
        ),
        gold=ScenarioGold(
            category="General Inquiry",
            priority="P4",
            assigned_team="Security Operations",
            needs_escalation=False,
            missing_information=(),
            next_best_action="Provide BitLocker To Go encryption instructions and removable media policy",
            remediation_steps=(
                "Share the guide for encrypting USB drives with BitLocker To Go",
                "Remind the user of the removable media data handling policy",
                "Confirm the USB drive is an approved company-issued device",
            ),
        ),
    ),
    # ------------------------------------------------------------------
    # 15. Personal phone for work email (BYOD)
    # ------------------------------------------------------------------
    ScenarioDefinition(
        scenario_id="general-015",
        subjects=(
            "Can I use my personal phone for work email?",
            "Setting up work email on personal iPhone",
        ),
        descriptions=(
            "I'd like to check my work email on my personal iPhone. Is that allowed? If so, "
            "what do I need to install? I don't want IT to be able to wipe my personal stuff.",
            "Is it possible to add my Contoso mailbox to my personal Android phone? I don't "
            "have a company phone and it would be really helpful to get notifications when "
            "I'm away from my desk.",
            "I heard there's a BYOD program but I'm not sure about the privacy implications. "
            "What exactly does Intune do on my personal device?",
        ),
        gold=ScenarioGold(
            category="General Inquiry",
            priority="P4",
            assigned_team="Endpoint Engineering",
            needs_escalation=False,
            missing_information=(),
            next_best_action="Explain the BYOD enrollment process and Intune MDM scope on personal devices",
            remediation_steps=(
                "Share the BYOD policy and enrollment guide",
                "Explain that Intune only manages the work profile, not personal data",
                "Provide instructions for installing Company Portal and enrolling the device",
            ),
        ),
    ),
    # ------------------------------------------------------------------
    # 16. IT budget request process
    # ------------------------------------------------------------------
    ScenarioDefinition(
        scenario_id="general-016",
        subjects=(
            "IT budget request process question",
            "How do I request IT budget for my team?",
        ),
        descriptions=(
            "Our department needs some specialized software for a new project. What's the "
            "process for requesting IT budget? Do I go through my VP or submit something "
            "directly to IT?",
            "I'm putting together a budget proposal for next fiscal year and need to include "
            "some IT hardware purchases. Who do I coordinate with on the IT side to get cost "
            "estimates and make sure everything goes through the right channels?",
        ),
        gold=ScenarioGold(
            category="General Inquiry",
            priority="P4",
            assigned_team="Endpoint Engineering",
            needs_escalation=False,
            missing_information=(),
            next_best_action="Explain the IT procurement and budget request process",
            remediation_steps=(
                "Share the IT procurement request process documentation",
                "Direct the user to their department's IT business partner for cost estimates",
                "Explain the approval workflow for IT purchases above the standard threshold",
            ),
        ),
    ),
    # ------------------------------------------------------------------
    # 17. How to set up a distribution list
    # ------------------------------------------------------------------
    ScenarioDefinition(
        scenario_id="general-017",
        subjects=(
            "How to create a distribution list",
            "Setting up an email distribution group",
            "New distribution list request",
        ),
        descriptions=(
            "I need to create a distribution list for our project team so we can send emails "
            "to everyone at once. How do I request one? Can I manage the members myself?",
            "Can someone set up a distribution list called DL-WealthMgmt-Analytics for our "
            "team? There are about 15 people. I have the list of email addresses ready.",
        ),
        gold=ScenarioGold(
            category="General Inquiry",
            priority="P4",
            assigned_team="Enterprise Applications",
            needs_escalation=False,
            missing_information=(),
            next_best_action="Provide the distribution list creation request form and naming conventions",
            remediation_steps=(
                "Share the distribution list request form",
                "Explain the naming convention for distribution lists",
                "Set up the list and assign the requester as owner for self-service management",
            ),
        ),
    ),
    # ------------------------------------------------------------------
    # 18. Conference room AV setup instructions
    # ------------------------------------------------------------------
    ScenarioDefinition(
        scenario_id="general-018",
        subjects=(
            "Conference room AV equipment help",
            "How to use the conference room projector",
        ),
        descriptions=(
            "I have an important client presentation in Conference Room B tomorrow and I've "
            "never used the AV setup in there. Is there a quick guide for connecting my laptop "
            "to the projector and using the room's speakers?",
            "The new conference rooms on the 8th floor have some fancy AV equipment — Crestron "
            "panels and ceiling mics. Is there documentation on how to use them? I don't want "
            "to waste the first 10 minutes of my meeting figuring it out.",
            "Can someone send me instructions for starting a Teams meeting on the conference "
            "room display? I can never get the room system to recognize my meeting.",
        ),
        gold=ScenarioGold(
            category="General Inquiry",
            priority="P4",
            assigned_team="Endpoint Engineering",
            needs_escalation=False,
            missing_information=(),
            next_best_action="Provide the conference room AV quick-start guide for the relevant room",
            remediation_steps=(
                "Share the AV setup guide specific to the conference room type",
                "Include instructions for both wired and wireless display options",
                "Offer to schedule a brief walkthrough if the user needs hands-on help",
            ),
        ),
    ),
    # ------------------------------------------------------------------
    # 19. Software license transfer between teams
    # ------------------------------------------------------------------
    ScenarioDefinition(
        scenario_id="general-019",
        subjects=(
            "Software license transfer question",
            "Transferring a software license to another team",
        ),
        descriptions=(
            "A colleague in my old team had an Adobe Creative Cloud license that they no "
            "longer need. Can that license be transferred to me now that I've moved to the "
            "Marketing team?",
            "We have some unused Visio licenses from a project that wrapped up. Is there a "
            "process to reassign them to another department? Seems wasteful to let them sit "
            "idle.",
            "Our team is being reorganized and we need to move several software licenses from "
            "the Compliance group to the Risk Analytics group. What's the procedure?",
        ),
        gold=ScenarioGold(
            category="General Inquiry",
            priority="P4",
            assigned_team="Enterprise Applications",
            needs_escalation=False,
            missing_information=(),
            next_best_action="Explain the software license reassignment process and initiate the transfer",
            remediation_steps=(
                "Verify the current license assignment in the software asset management tool",
                "Confirm manager approval for the license transfer",
                "Reassign the license to the new user or cost center",
            ),
        ),
    ),
    # ------------------------------------------------------------------
    # 20. Data retention policy question
    # ------------------------------------------------------------------
    ScenarioDefinition(
        scenario_id="general-020",
        subjects=(
            "Data retention policy question",
            "How long are emails and files kept?",
        ),
        descriptions=(
            "I need to understand our data retention policies for an upcoming audit. How long "
            "does Contoso keep emails and OneDrive files? Is there a formal policy document "
            "I can reference?",
            "Our team is cleaning up old SharePoint sites and we want to make sure we don't "
            "delete anything we're required to retain. Where can I find the data retention "
            "schedule?",
        ),
        gold=ScenarioGold(
            category="General Inquiry",
            priority="P4",
            assigned_team="Data Platform",
            needs_escalation=False,
            missing_information=(),
            next_best_action="Share the data retention policy documentation and compliance guidelines",
            remediation_steps=(
                "Provide the data retention policy document",
                "Explain retention periods for email, SharePoint, and OneDrive",
                "Advise the user to consult with Compliance before deleting regulated data",
            ),
        ),
    ),
    # ------------------------------------------------------------------
    # 21. How to request a new SharePoint site
    # ------------------------------------------------------------------
    ScenarioDefinition(
        scenario_id="general-021",
        subjects=(
            "How to request a new SharePoint site",
            "New SharePoint site for our team",
        ),
        descriptions=(
            "Our project team needs a dedicated SharePoint site for document collaboration. "
            "What's the process to request one? Can I create it myself or does IT need to "
            "provision it?",
            "I'd like to set up a new SharePoint Online site for the Risk Management "
            "department. We need document libraries, a team calendar, and a shared inbox. "
            "How do I get started?",
            "Is there a self-service option for creating SharePoint sites or do I need to "
            "submit a ticket?",
        ),
        gold=ScenarioGold(
            category="General Inquiry",
            priority="P4",
            assigned_team="Data Platform",
            needs_escalation=False,
            missing_information=(),
            next_best_action="Provide the SharePoint site provisioning request process and governance rules",
            remediation_steps=(
                "Share the SharePoint site request form",
                "Explain the site naming and governance policies",
                "Provision the site once the request is approved",
            ),
        ),
    ),
    # ------------------------------------------------------------------
    # 22. Reporting a security concern
    # ------------------------------------------------------------------
    ScenarioDefinition(
        scenario_id="general-022",
        subjects=(
            "How do I report a security concern?",
            "Process for reporting a potential security issue",
        ),
        descriptions=(
            "I noticed something suspicious on a shared drive — there are files with client "
            "SSNs that seem to be accessible to everyone. I'm not sure if this is a security "
            "issue but I want to report it. What's the right channel?",
            "What's the process for reporting a security concern at Contoso? I don't want to "
            "cause a false alarm but something doesn't seem right with the access permissions "
            "on one of our internal applications.",
            "If I suspect a colleague accidentally shared sensitive data externally, who should "
            "I contact? Is there a confidential reporting mechanism?",
        ),
        gold=ScenarioGold(
            category="General Inquiry",
            priority="P4",
            assigned_team="Security Operations",
            needs_escalation=False,
            missing_information=(),
            next_best_action="Provide the security incident reporting process and relevant contact channels",
            remediation_steps=(
                "Direct the user to the security incident reporting portal",
                "Provide the Security Operations team's direct contact information",
                "Reassure the user that reporting concerns is encouraged and confidential",
            ),
        ),
    ),
    # ------------------------------------------------------------------
    # 23. IT newsletter subscription
    # ------------------------------------------------------------------
    ScenarioDefinition(
        scenario_id="general-023",
        subjects=(
            "Subscribe to IT newsletter",
            "How do I sign up for IT updates?",
        ),
        descriptions=(
            "A coworker mentioned there's a monthly IT newsletter with tips, upcoming changes, "
            "and maintenance windows. How do I subscribe? I don't think I've been getting it.",
            "I'd like to stay informed about IT changes and new tools. Is there a mailing list "
            "or newsletter I can sign up for?",
        ),
        gold=ScenarioGold(
            category="General Inquiry",
            priority="P4",
            assigned_team="Endpoint Engineering",
            needs_escalation=False,
            missing_information=(),
            next_best_action="Add the user to the IT newsletter distribution list",
            remediation_steps=(
                "Add the user's email to the IT newsletter distribution list",
                "Confirm the subscription and share the archive of past newsletters",
                "Mention other IT communication channels like the Teams channel and intranet",
            ),
        ),
    ),
    # ------------------------------------------------------------------
    # 24. Teams meeting recording setup
    # ------------------------------------------------------------------
    ScenarioDefinition(
        scenario_id="general-024",
        subjects=(
            "How to record a Teams meeting",
            "Teams meeting recording setup",
            "Enable meeting recording in Microsoft Teams",
        ),
        descriptions=(
            "I need to record my team's weekly standup so people in other time zones can "
            "catch up. How do I enable recording in Teams? I clicked the button but got a "
            "message saying recording isn't available.",
            "Can someone help me figure out Teams recording? I want to record a training "
            "session next week. Where do the recordings get saved and how long are they "
            "kept?",
        ),
        gold=ScenarioGold(
            category="General Inquiry",
            priority="P4",
            assigned_team="Enterprise Applications",
            needs_escalation=False,
            missing_information=(),
            next_best_action="Verify the user's Teams recording policy and provide setup instructions",
            remediation_steps=(
                "Check if the user's Teams policy allows meeting recording",
                "Enable recording permissions if appropriate and approved",
                "Explain that recordings are saved to OneDrive/SharePoint with auto-expiration",
            ),
        ),
    ),
    # ------------------------------------------------------------------
    # 25. Office relocation — IT setup needs
    # ------------------------------------------------------------------
    ScenarioDefinition(
        scenario_id="general-025",
        subjects=(
            "Office relocation — IT setup needed",
            "IT requirements for floor move",
            "Moving offices — need IT help",
        ),
        descriptions=(
            "Our entire Compliance department (about 40 people) is relocating from the 3rd "
            "floor to the 7th floor next month. We need to coordinate network drops, phone "
            "setups, and printer configurations for the new space. Who should I work with "
            "to plan this?",
            "We're moving to a newly renovated section of the building in two weeks. I need "
            "to make sure all the network ports are active, the conference room AV is set "
            "up, and our team printer is relocated. This is time-sensitive — the move date "
            "is locked in.",
        ),
        gold=ScenarioGold(
            category="General Inquiry",
            priority="P3",
            assigned_team="Network Operations",
            needs_escalation=False,
            missing_information=(),
            next_best_action="Initiate the office relocation IT coordination workflow",
            remediation_steps=(
                "Schedule a planning meeting with Network Operations and Endpoint Engineering",
                "Verify network port activation and cabling in the new location",
                "Coordinate printer relocation and conference room AV setup",
                "Conduct a walkthrough of the new space before move day",
            ),
        ),
    ),
    # ------------------------------------------------------------------
    # 26. IT self-service portal access
    # ------------------------------------------------------------------
    ScenarioDefinition(
        scenario_id="general-026",
        subjects=(
            "How to access the IT self-service portal",
            "Where is the IT help portal?",
        ),
        descriptions=(
            "I keep hearing about an IT self-service portal where I can submit tickets and "
            "find knowledge articles, but I don't know the URL. Can someone share the link?",
            "I'm new to Contoso and trying to find the IT support portal. I checked the "
            "intranet but the link seems broken. What's the correct URL for submitting IT "
            "requests?",
            "Is there a mobile app for the IT self-service portal? I'd like to be able to "
            "submit tickets from my phone when I'm not at my desk.",
        ),
        gold=ScenarioGold(
            category="General Inquiry",
            priority="P4",
            assigned_team="Identity & Access Management",
            needs_escalation=False,
            missing_information=(),
            next_best_action="Provide the IT self-service portal URL and access instructions",
            remediation_steps=(
                "Share the correct URL for the IT self-service portal",
                "Verify the user can authenticate to the portal",
                "Provide a brief overview of available self-service options",
            ),
        ),
    ),
    # ------------------------------------------------------------------
    # 27. BYOD policy question
    # ------------------------------------------------------------------
    ScenarioDefinition(
        scenario_id="general-027",
        subjects=(
            "Question about the BYOD policy",
            "BYOD — what devices are supported?",
        ),
        descriptions=(
            "I just bought a new iPad and I'd like to use it for work. What's Contoso's BYOD "
            "policy? Are tablets supported, or is it just phones and laptops?",
            "I read the BYOD policy on the intranet but it was last updated in 2022. Is it "
            "still current? Specifically, I want to know if I can use a Chromebook for "
            "accessing email and Teams.",
        ),
        gold=ScenarioGold(
            category="General Inquiry",
            priority="P4",
            assigned_team="Endpoint Engineering",
            needs_escalation=False,
            missing_information=(),
            next_best_action="Provide the current BYOD policy details and supported device list",
            remediation_steps=(
                "Share the latest BYOD policy document",
                "Clarify which device types and operating systems are supported",
                "Explain the enrollment requirements and security controls for BYOD devices",
            ),
        ),
    ),
    # ------------------------------------------------------------------
    # 28. Outlook signature configuration
    # ------------------------------------------------------------------
    ScenarioDefinition(
        scenario_id="general-028",
        subjects=(
            "How to set up my Outlook email signature",
            "Outlook signature template",
        ),
        descriptions=(
            "I need to update my email signature to match the new Contoso branding. Is there "
            "a standard template we're supposed to use? My current signature is just plain "
            "text.",
            "I noticed that most people in my department have a nicely formatted email "
            "signature with the Contoso logo and their title. Where do I get the template "
            "and how do I set it up in Outlook?",
            "Brand team said all employees need the new email signature by end of month. "
            "Can IT provide the HTML template and instructions for applying it?",
        ),
        gold=ScenarioGold(
            category="General Inquiry",
            priority="P4",
            assigned_team="Enterprise Applications",
            needs_escalation=False,
            missing_information=(),
            next_best_action="Provide the standard Outlook signature template and setup instructions",
            remediation_steps=(
                "Share the approved email signature template from the brand guidelines",
                "Provide step-by-step instructions for configuring signatures in Outlook",
                "Mention that signatures may be auto-applied via Exchange transport rules",
            ),
        ),
    ),
    # ------------------------------------------------------------------
    # 29. IT roadmap presentation request
    # ------------------------------------------------------------------
    ScenarioDefinition(
        scenario_id="general-029",
        subjects=(
            "IT roadmap presentation for our department",
            "Can IT present at our team meeting?",
        ),
        descriptions=(
            "Our VP would like someone from IT to present the technology roadmap at our "
            "quarterly department meeting next month. Is that something your team does? "
            "We're particularly interested in upcoming collaboration tool changes and the "
            "cloud migration timeline.",
            "Would it be possible to get an IT roadmap overview for the Investment Banking "
            "division? About 60 people. We'd love to hear about planned upgrades and how "
            "they affect our workflows. We can host it in our large conference room.",
        ),
        gold=ScenarioGold(
            category="General Inquiry",
            priority="P4",
            assigned_team="Endpoint Engineering",
            needs_escalation=False,
            missing_information=(),
            next_best_action="Coordinate an IT roadmap presentation with the appropriate IT leadership",
            remediation_steps=(
                "Forward the request to IT leadership for scheduling",
                "Confirm the date, time, and audience size with the requester",
                "Prepare a tailored roadmap overview relevant to the department's needs",
            ),
        ),
    ),
    # ------------------------------------------------------------------
    # 30. How to request database access
    # ------------------------------------------------------------------
    ScenarioDefinition(
        scenario_id="general-030",
        subjects=(
            "How do I request database access?",
            "Need access to a SQL database",
            "Database access request process",
        ),
        descriptions=(
            "I recently joined the Data Analytics team and I need read access to the "
            "ClientTransactions SQL database for my reporting work. What's the process for "
            "requesting database access?",
            "My manager approved me for access to the risk analytics database but I don't "
            "know where to submit the actual request. Is there a form or do I just email "
            "the DBA team?",
        ),
        gold=ScenarioGold(
            category="General Inquiry",
            priority="P4",
            assigned_team="Data Platform",
            needs_escalation=False,
            missing_information=(),
            next_best_action="Provide the database access request form and approval workflow",
            remediation_steps=(
                "Share the database access request form from the IT portal",
                "Explain that manager and data owner approval is required",
                "Once approved, provision the requested read access and confirm with the user",
            ),
        ),
    ),
]
