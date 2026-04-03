"""General Inquiry category scenarios for eval dataset."""

from ms.evals_core.constants import Category
from ms.evals_core.constants import Channel
from ms.evals_core.constants import MissingInfo
from ms.evals_core.constants import Priority
from ms.evals_core.constants import Team
from ms.evals_core.scenarios.base import ScenarioDefinition


def get_scenarios() -> list[ScenarioDefinition]:
    """Return all General Inquiry evaluation scenarios."""
    return [
        # ──────────────────────────────────────────────────────────────
        # 1. Standard new hire onboarding
        # ──────────────────────────────────────────────────────────────
        ScenarioDefinition(
            scenario_id="general_inquiry_001",
            subject="New hire onboarding — starting March 24",
            description=(
                "Hi IT team, we have a new analyst joining the Risk Management team on March 24th. His name"
                " is David Chen and he will be based in the Singapore office. Could you please set up a"
                " standard workstation, email account, and access to Bloomberg Terminal and the risk"
                " analytics platform? His manager is Priya Sharma. Thanks!"
            ),
            category=Category.GENERAL_INQUIRY,
            priority=Priority.P3,
            team=Team.ENDPOINT,
            needs_escalation=False,
            missing_info=[MissingInfo.CONTACT_INFO],
            next_best_action=(
                "Confirm the new hire's employee ID, start date, and required application list with HR,"
                " then initiate the standard onboarding workflow"
            ),
            remediation_steps=[
                "Confirm employee details and start date with the hiring manager and HR",
                "Provision a standard workstation and ship to the Singapore office",
                "Create Active Directory and email accounts per the new hire checklist",
                "Request Bloomberg Terminal access through the vendor portal",
                "Grant access to the risk analytics platform via the IAM team",
                "Schedule a Day 1 IT orientation session with the new hire",
            ],
            reporter_name="Priya Sharma",
            reporter_email="priya.sharma@contoso.com",
            reporter_department="Risk Management",
            channel=Channel.EMAIL,
            created_at="2026-03-10T10:15:00Z",
            tags=["onboarding", "new-hire", "singapore"],
            difficulty="easy",
        ),
        # ──────────────────────────────────────────────────────────────
        # 2. Expedited executive onboarding
        # ──────────────────────────────────────────────────────────────
        ScenarioDefinition(
            scenario_id="general_inquiry_002",
            subject="EXPEDITED: New Managing Director starting Monday",
            description=(
                "Urgent request — we have a new Managing Director, Sarah Whitfield, joining Executive"
                " Operations this Monday. She is relocating from a competitor and the offer was just"
                " finalized yesterday. She needs a fully configured MacBook Pro, dual monitors, a private"
                " office setup on the 10th floor of Building 1 in NYC, access to the executive dashboard,"
                " Bloomberg, Salesforce, and the board materials SharePoint. Please prioritize this."
            ),
            category=Category.GENERAL_INQUIRY,
            priority=Priority.P2,
            team=Team.ENDPOINT,
            needs_escalation=True,
            missing_info=[MissingInfo.CONTACT_INFO, MissingInfo.BUSINESS_IMPACT],
            next_best_action=(
                "Fast-track the executive onboarding checklist, assign a dedicated technician, and coordinate"
                " with Facilities for the office setup"
            ),
            remediation_steps=[
                "Initiate the expedited executive onboarding workflow with a dedicated technician assigned",
                "Provision a MacBook Pro with executive image and configure dual monitors",
                "Coordinate with Facilities for the 10th floor office network and phone setup",
                "Create AD account with executive-level group memberships",
                "Request Bloomberg, Salesforce, and executive dashboard access in parallel",
                "Set up the board materials SharePoint site permissions with the IAM team",
                "Schedule a white-glove IT walkthrough for Monday morning before the MD arrives",
            ],
            reporter_name="Jonathan Fields",
            reporter_email="jonathan.fields@contoso.com",
            reporter_department="Executive Operations",
            channel=Channel.PHONE,
            created_at="2026-03-14T16:30:00Z",
            tags=["onboarding", "executive", "expedited", "nyc"],
            difficulty="hard",
        ),
        # ──────────────────────────────────────────────────────────────
        # 3. Summer intern batch onboarding
        # ──────────────────────────────────────────────────────────────
        ScenarioDefinition(
            scenario_id="general_inquiry_003",
            subject="Summer intern onboarding — 15 interns starting June 2",
            description=(
                "Hi, the internship program kicks off June 2nd with 15 interns across Engineering,"
                " Quantitative Analysis, and Trading. They will all be in the NYC office. Each intern needs"
                " a standard laptop, email account, and access to the intern SharePoint site. They should"
                " NOT have access to production systems or client data. I have a spreadsheet with all their"
                " names and assigned teams. Who should I send it to?"
            ),
            category=Category.GENERAL_INQUIRY,
            priority=Priority.P3,
            team=Team.ENDPOINT,
            needs_escalation=False,
            missing_info=[MissingInfo.CONTACT_INFO, MissingInfo.AFFECTED_USERS],
            next_best_action=(
                "Request the intern roster spreadsheet, then initiate batch onboarding with restricted"
                " access group memberships"
            ),
            remediation_steps=[
                "Request the intern roster spreadsheet with names, teams, and start dates",
                "Create AD accounts in the Intern OU with time-limited expiration dates",
                "Provision 15 standard laptops with the intern image and restricted group policies",
                "Grant access to email, Teams, and the intern SharePoint site only",
                "Confirm that production system and client data access is blocked for intern accounts",
                "Coordinate a group IT orientation session for June 2nd",
            ],
            reporter_name="Karen Liu",
            reporter_email="karen.liu@contoso.com",
            reporter_department="HR",
            channel=Channel.PORTAL,
            created_at="2026-04-15T09:00:00Z",
            tags=["onboarding", "intern", "batch", "nyc"],
            difficulty="medium",
        ),
        # ──────────────────────────────────────────────────────────────
        # 4. Contractor onboarding with limited access
        # ──────────────────────────────────────────────────────────────
        ScenarioDefinition(
            scenario_id="general_inquiry_004",
            subject="Contractor IT setup — external consultant for 6 months",
            description=(
                "We are bringing on a contractor, Miguel Torres, from Deloitte for a 6-month engagement"
                " starting April 1st. He will be working with the Data Engineering team in the London"
                " office. He needs a Contoso laptop, email, VPN access, and read-only access to our data"
                " warehouse. He should not have write access to any production databases. His Deloitte email"
                " is m.torres@deloitte.com."
            ),
            category=Category.GENERAL_INQUIRY,
            priority=Priority.P3,
            team=Team.ENDPOINT,
            needs_escalation=False,
            missing_info=[MissingInfo.CONTACT_INFO, MissingInfo.CONFIGURATION_DETAILS],
            next_best_action=(
                "Initiate the contractor onboarding checklist with time-limited credentials and confirm"
                " read-only data warehouse access with the Data Platform team"
            ),
            remediation_steps=[
                "Create a contractor AD account with a 6-month expiration date",
                "Provision a standard laptop with contractor-tier group policies",
                "Configure VPN access with contractor profile restrictions",
                "Coordinate with the Data Platform team for read-only data warehouse access",
                "Confirm that write access to production databases is explicitly denied",
                "Send onboarding instructions to the contractor's Deloitte email",
                "Schedule a Day 1 IT orientation at the London office",
            ],
            reporter_name="Emma Richardson",
            reporter_email="emma.richardson@contoso.com",
            reporter_department="Data Engineering",
            channel=Channel.EMAIL,
            created_at="2026-03-12T11:20:00Z",
            tags=["onboarding", "contractor", "london", "limited-access"],
            difficulty="medium",
        ),
        # ──────────────────────────────────────────────────────────────
        # 5. Employee resignation offboarding
        # ──────────────────────────────────────────────────────────────
        ScenarioDefinition(
            scenario_id="general_inquiry_005",
            subject="Offboarding request — employee resignation effective March 28",
            description=(
                "Please initiate the IT offboarding process for Marcus Webb in the Trading team. His last"
                " day is March 28th. He has a ThinkPad X1 Carbon, two monitors, and a docking station that"
                " need to be returned. His access to trading platforms, Bloomberg, and all internal systems"
                " should be revoked at end of business on his last day. He also has a corporate phone."
            ),
            category=Category.GENERAL_INQUIRY,
            priority=Priority.P3,
            team=Team.IAM,
            needs_escalation=False,
            missing_info=[MissingInfo.DEVICE_INFO],
            next_best_action=(
                "Schedule the offboarding for March 28th EOD, coordinate equipment return, and queue access"
                " revocation across all systems"
            ),
            remediation_steps=[
                "Schedule AD account disable for March 28th at 6:00 PM local time",
                "Revoke access to Bloomberg Terminal and trading platform accounts",
                "Disable email account and set up auto-forwarding to the manager for 30 days",
                "Coordinate equipment return: laptop, monitors, docking station, and corporate phone",
                "Wipe the corporate phone and remove it from MDM enrollment",
                "Archive the user's mailbox and OneDrive per the retention policy",
                "Confirm all access revocations with the IAM team on the last day",
            ],
            reporter_name="Linda Garcia",
            reporter_email="linda.garcia@contoso.com",
            reporter_department="HR",
            channel=Channel.PORTAL,
            created_at="2026-03-14T08:45:00Z",
            tags=["offboarding", "resignation", "equipment-return"],
            difficulty="medium",
        ),
        # ──────────────────────────────────────────────────────────────
        # 6. Termination offboarding with compliance files
        # ──────────────────────────────────────────────────────────────
        ScenarioDefinition(
            scenario_id="general_inquiry_006",
            subject="CONFIDENTIAL: Immediate offboarding — terminated employee",
            description=(
                "This is confidential. We need immediate IT offboarding for Robert Kline in the Compliance"
                " department. His employment is being terminated today at 3 PM. All access must be revoked"
                " at exactly 3 PM before he is informed. He has access to sensitive regulatory filings and"
                " compliance audit documents. Legal has requested that his email and local files be preserved"
                " for a potential investigation. Do NOT notify the employee. Contact HR director Nina Patel"
                " at ext. 4401 for coordination."
            ),
            category=Category.GENERAL_INQUIRY,
            priority=Priority.P2,
            team=Team.IAM,
            needs_escalation=True,
            missing_info=[MissingInfo.DEVICE_INFO, MissingInfo.AFFECTED_SYSTEM],
            next_best_action=(
                "Coordinate timed access revocation for exactly 3 PM, place a litigation hold on email and"
                " files, and work with Legal to ensure chain-of-custody compliance"
            ),
            remediation_steps=[
                "Schedule AD account disable for 3:00 PM sharp with a confirmed IAM operator on standby",
                "Place a litigation hold on the user's mailbox and OneDrive immediately",
                "Revoke access to compliance document management systems and regulatory filing portals",
                "Disable VPN and remote access tokens at the same time as AD disable",
                "Export and preserve local workstation data with forensic imaging if Legal requires it",
                "Coordinate physical equipment retrieval with Facilities and Security after termination",
                "Provide a written confirmation of all access revocations to HR and Legal",
            ],
            reporter_name="Nina Patel",
            reporter_email="nina.patel@contoso.com",
            reporter_department="HR",
            channel=Channel.PHONE,
            created_at="2026-03-18T12:30:00Z",
            tags=["offboarding", "termination", "compliance", "confidential", "legal-hold"],
            difficulty="hard",
        ),
        # ──────────────────────────────────────────────────────────────
        # 7. Inter-office transfer
        # ──────────────────────────────────────────────────────────────
        ScenarioDefinition(
            scenario_id="general_inquiry_007",
            subject="Employee transfer from London to NYC — IT transition",
            description=(
                "Hi, I am transferring from the London office to New York starting April 14th. I will be"
                " moving from the Fixed Income team to Portfolio Management. Do I keep my current laptop or"
                " get a new one? Will my VPN profile and network drives update automatically? I also need"
                " access to the NYC-specific portfolio management tools. My asset tag is CTF-LT-3392."
            ),
            category=Category.GENERAL_INQUIRY,
            priority=Priority.P3,
            team=Team.ENDPOINT,
            needs_escalation=False,
            missing_info=[MissingInfo.ENVIRONMENT_DETAILS],
            next_best_action=(
                "Coordinate the office transfer checklist: update AD site and group memberships, confirm"
                " equipment decision, and provision NYC-specific application access"
            ),
            remediation_steps=[
                "Update the user's AD profile with new office location and department",
                "Reassign group memberships from Fixed Income to Portfolio Management",
                "Evaluate whether the current laptop meets NYC hardware standards or needs replacement",
                "Update VPN profile to route through the NYC gateway",
                "Map NYC-specific network drives and remove London-only shares",
                "Grant access to the portfolio management tools used by the NYC team",
                "Confirm the transition is complete on the user's first day in NYC",
            ],
            reporter_name="Alex Turner",
            reporter_email="alex.turner@contoso.com",
            reporter_department="Fixed Income",
            channel=Channel.PORTAL,
            created_at="2026-03-17T14:00:00Z",
            tags=["transfer", "office-move", "london", "nyc"],
            difficulty="medium",
        ),
        # ──────────────────────────────────────────────────────────────
        # 8. Meeting room booking question
        # ──────────────────────────────────────────────────────────────
        ScenarioDefinition(
            scenario_id="general_inquiry_008",
            subject="How do I book a large meeting room with video conferencing?",
            description=(
                "I need to book the large conference room on the 5th floor of Building 2 in NYC for a"
                " client presentation next Thursday from 10 AM to 12 PM. The room needs video conferencing"
                " for attendees dialing in from London and Singapore. I looked in Outlook but I can only see"
                " small huddle rooms. How do I find and book the larger rooms? Is there a separate system?"
            ),
            category=Category.GENERAL_INQUIRY,
            priority=Priority.P4,
            team=Team.NONE,
            needs_escalation=False,
            missing_info=[],
            next_best_action=(
                "Redirect the user to the Facilities team for large conference room bookings and provide"
                " instructions for finding bookable rooms in Outlook"
            ),
            remediation_steps=[
                "Explain that large conference rooms are booked through the Outlook room finder under the"
                " Building 2 room list",
                "Provide instructions to select the 'All Rooms' list and filter by capacity and building",
                "Note that rooms with video conferencing have 'VC' in their display name",
                "If the room is not visible, suggest contacting Facilities to request booking permissions",
                "Remind the user to test the video conferencing link before the meeting",
            ],
            reporter_name="Sofia Martinez",
            reporter_email="sofia.martinez@contoso.com",
            reporter_department="Client Services",
            channel=Channel.CHAT,
            created_at="2026-03-11T15:45:00Z",
            tags=["meeting-room", "video-conferencing", "outlook", "nyc"],
            difficulty="easy",
        ),
        # ──────────────────────────────────────────────────────────────
        # 9. BYOD policy inquiry
        # ──────────────────────────────────────────────────────────────
        ScenarioDefinition(
            scenario_id="general_inquiry_009",
            subject="Question about BYOD policy for personal iPad",
            description=(
                "I would like to use my personal iPad Pro for work during my commute. Can I install Outlook"
                " and Teams on it to read emails and join meetings? I want to make sure I'm not violating"
                " any company policies. Do I need to enroll it in some kind of management system? I'm in the"
                " Equity Trading department, so I know there are extra rules around our devices."
            ),
            category=Category.GENERAL_INQUIRY,
            priority=Priority.P4,
            team=Team.ENDPOINT,
            needs_escalation=False,
            missing_info=[MissingInfo.DEVICE_INFO],
            next_best_action=(
                "Provide the BYOD policy documentation and explain the MDM enrollment requirements for"
                " personal devices accessing corporate data"
            ),
            remediation_steps=[
                "Share the current BYOD policy document from the IT intranet",
                "Explain that personal devices accessing corporate email must be enrolled in Intune MDM",
                "Note that Equity Trading staff have additional DLP restrictions on mobile devices",
                "Walk the user through the Intune Company Portal installation and enrollment process",
                "Confirm that the device meets minimum OS version requirements for MDM enrollment",
            ],
            reporter_name="Derek Chang",
            reporter_email="derek.chang@contoso.com",
            reporter_department="Equity Trading",
            channel=Channel.CHAT,
            created_at="2026-03-06T08:30:00Z",
            tags=["byod", "policy", "mobile", "mdm"],
            difficulty="easy",
        ),
        # ──────────────────────────────────────────────────────────────
        # 10. Remote work policy and VPN setup
        # ──────────────────────────────────────────────────────────────
        ScenarioDefinition(
            scenario_id="general_inquiry_010",
            subject="Remote work IT requirements — approved for 3 days/week WFH",
            description=(
                "My manager just approved me for 3 days per week remote work. I wanted to check what the IT"
                " requirements are. Do I need a VPN client? Is there a specific home network configuration"
                " required? I heard something about needing a company-approved router. I'm in the Research"
                " department and I access the quantitative models server daily. My home is in New Jersey."
            ),
            category=Category.GENERAL_INQUIRY,
            priority=Priority.P4,
            team=Team.NETWORK_OPS,
            needs_escalation=False,
            missing_info=[MissingInfo.NETWORK_LOCATION],
            next_best_action=(
                "Provide the remote work IT policy, confirm VPN access is provisioned, and clarify home"
                " network requirements"
            ),
            remediation_steps=[
                "Share the remote work IT requirements document from the intranet",
                "Confirm the user has the GlobalProtect VPN client installed and configured",
                "Clarify that a company-approved router is not required but a secure home Wi-Fi with WPA3 or"
                " WPA2 is mandatory",
                "Verify the user's VPN profile allows access to the quantitative models server",
                "Recommend the user test VPN connectivity from home before the first remote day",
            ],
            reporter_name="Anita Desai",
            reporter_email="anita.desai@contoso.com",
            reporter_department="Research",
            channel=Channel.EMAIL,
            created_at="2026-03-07T10:00:00Z",
            tags=["remote-work", "vpn", "policy", "wfh"],
            difficulty="easy",
        ),
        # ──────────────────────────────────────────────────────────────
        # 11. Data classification policy question
        # ──────────────────────────────────────────────────────────────
        ScenarioDefinition(
            scenario_id="general_inquiry_011",
            subject="Data classification — how to label client documents",
            description=(
                "I am preparing a set of client portfolio reports to share with our London team via"
                " SharePoint. I know we have a data classification policy but I am not sure how to apply"
                " the right labels. These documents contain client PII and financial performance data."
                " Should I label them as Confidential or Highly Confidential? Is there a guide or tool"
                " that helps apply labels automatically?"
            ),
            category=Category.GENERAL_INQUIRY,
            priority=Priority.P3,
            team=Team.SECURITY_OPS,
            needs_escalation=False,
            missing_info=[],
            next_best_action=(
                "Direct the user to the data classification guide and explain how to apply sensitivity labels"
                " in Microsoft Office and SharePoint"
            ),
            remediation_steps=[
                "Share the Contoso data classification policy document",
                "Explain that documents with client PII and financial data should be labeled Highly Confidential",
                "Walk the user through applying sensitivity labels in Word and Excel via the ribbon bar",
                "Confirm that SharePoint will inherit the document's sensitivity label automatically",
                "Recommend enabling automatic labeling in the user's Office apps for future documents",
            ],
            reporter_name="Catherine Brooks",
            reporter_email="catherine.brooks@contoso.com",
            reporter_department="Portfolio Management",
            channel=Channel.PORTAL,
            created_at="2026-03-09T13:15:00Z",
            tags=["data-classification", "policy", "sharepoint", "sensitivity-labels"],
            difficulty="easy",
        ),
        # ──────────────────────────────────────────────────────────────
        # 12. Software availability question
        # ──────────────────────────────────────────────────────────────
        ScenarioDefinition(
            scenario_id="general_inquiry_012",
            subject="Is Tableau approved for use? Need it for a dashboard project",
            description=(
                "My team wants to build an internal analytics dashboard and we think Tableau Desktop would"
                " be the best tool. Is Tableau on the approved software list? If so, how do I request a"
                " license? If not, what is the process to get a new tool approved? We currently use Power BI"
                " but it doesn't support some of the visualizations we need. There would be about 8 users."
            ),
            category=Category.GENERAL_INQUIRY,
            priority=Priority.P4,
            team=Team.ENTERPRISE_APPS,
            needs_escalation=False,
            missing_info=[MissingInfo.BUSINESS_IMPACT],
            next_best_action=(
                "Check the approved software catalog for Tableau and guide the user through the license"
                " request or new software approval process"
            ),
            remediation_steps=[
                "Check the approved software catalog in ServiceNow for Tableau Desktop",
                "If approved, submit a license request for 8 users through the software procurement portal",
                "If not approved, provide the new software request form and explain the evaluation process",
                "Advise the user that new software requests typically require a business justification and"
                " security review",
                "Suggest scheduling a call with the Enterprise Applications team to discuss alternatives",
            ],
            reporter_name="Ryan Okoye",
            reporter_email="ryan.okoye@contoso.com",
            reporter_department="Data Science",
            channel=Channel.PORTAL,
            created_at="2026-03-08T11:30:00Z",
            tags=["software-request", "tableau", "licensing", "approval"],
            difficulty="easy",
        ),
        # ──────────────────────────────────────────────────────────────
        # 13. Unapproved software install question
        # ──────────────────────────────────────────────────────────────
        ScenarioDefinition(
            scenario_id="general_inquiry_013",
            subject="Can I install Python and VS Code on my work laptop?",
            description=(
                "I am a quant analyst and I need Python 3.12 and Visual Studio Code for my modeling work."
                " I tried to install Python from python.org but got an admin rights error. Can IT install"
                " these for me or add me to a group that has install permissions? I also need a few pip"
                " packages like pandas, numpy, and scipy."
            ),
            category=Category.GENERAL_INQUIRY,
            priority=Priority.P4,
            team=Team.ENDPOINT,
            needs_escalation=False,
            missing_info=[MissingInfo.DEVICE_INFO],
            next_best_action=(
                "Check if Python and VS Code are available in the self-service software catalog and arrange"
                " installation via the approved deployment method"
            ),
            remediation_steps=[
                "Verify that Python 3.12 and VS Code are in the approved software catalog",
                "Deploy Python and VS Code via Intune or SCCM to the user's device",
                "Confirm that pip is configured to use the internal PyPI mirror for package installs",
                "Advise the user that local admin rights are not granted; all software must go through the"
                " approved deployment pipeline",
                "Follow up to ensure the required packages install correctly from the internal mirror",
            ],
            reporter_name="Liam Foster",
            reporter_email="liam.foster@contoso.com",
            reporter_department="Quantitative Analysis",
            channel=Channel.CHAT,
            created_at="2026-03-05T14:20:00Z",
            tags=["software-install", "python", "developer-tools"],
            difficulty="easy",
        ),
        # ──────────────────────────────────────────────────────────────
        # 14. Security awareness training inquiry
        # ──────────────────────────────────────────────────────────────
        ScenarioDefinition(
            scenario_id="general_inquiry_014",
            subject="When is the next mandatory security training?",
            description=(
                "I received an email saying I need to complete my annual security awareness training by end"
                " of March but the link in the email goes to a page that says 'course not found'. Can you"
                " send me the correct link? Also, I completed a phishing simulation last month — does that"
                " count toward the requirement? I am in Compliance and I think we have additional modules."
            ),
            category=Category.GENERAL_INQUIRY,
            priority=Priority.P4,
            team=Team.SECURITY_OPS,
            needs_escalation=False,
            missing_info=[],
            next_best_action=(
                "Provide the correct training portal link, verify the user's completion status, and clarify"
                " which modules are required for Compliance staff"
            ),
            remediation_steps=[
                "Provide the correct URL for the security awareness training portal",
                "Check the LMS to verify the user's current completion status",
                "Clarify that phishing simulations are separate from the annual training requirement",
                "Confirm the additional Compliance-specific modules the user must complete",
                "Report the broken link to the training platform administrator for correction",
            ],
            reporter_name="Hannah Reeves",
            reporter_email="hannah.reeves@contoso.com",
            reporter_department="Compliance",
            channel=Channel.EMAIL,
            created_at="2026-03-15T09:00:00Z",
            tags=["training", "security-awareness", "compliance"],
            difficulty="easy",
        ),
        # ──────────────────────────────────────────────────────────────
        # 15. Hardware procurement budget question
        # ──────────────────────────────────────────────────────────────
        ScenarioDefinition(
            scenario_id="general_inquiry_015",
            subject="How to request new monitors for my team?",
            description=(
                "I manage a team of 6 in the Frontend Engineering department. We would like to upgrade from"
                " single monitors to dual 27-inch 4K setups. What is the process for requesting hardware?"
                " Do we need manager approval or VP sign-off for this amount? Is there a self-service portal"
                " or do I submit a ticket? We are in Building 4, NYC office."
            ),
            category=Category.GENERAL_INQUIRY,
            priority=Priority.P4,
            team=Team.NONE,
            needs_escalation=False,
            missing_info=[MissingInfo.BUSINESS_IMPACT],
            next_best_action=(
                "Direct the user to the hardware procurement portal and explain the approval workflow for"
                " team equipment orders"
            ),
            remediation_steps=[
                "Provide the link to the hardware procurement portal in ServiceNow",
                "Explain that monitor upgrades for a full team require manager approval and budget code",
                "Note that orders over $5,000 require VP-level sign-off per the procurement policy",
                "Advise the user to include a business justification for the dual monitor upgrade",
                "Inform the user that standard delivery time is 2-3 weeks after approval",
            ],
            reporter_name="Jason Kwok",
            reporter_email="jason.kwok@contoso.com",
            reporter_department="Frontend Engineering",
            channel=Channel.CHAT,
            created_at="2026-03-13T10:45:00Z",
            tags=["procurement", "hardware-request", "monitors", "budget"],
            difficulty="easy",
        ),
        # ──────────────────────────────────────────────────────────────
        # 16. Equipment return for departing employee
        # ──────────────────────────────────────────────────────────────
        ScenarioDefinition(
            scenario_id="general_inquiry_016",
            subject="Returning equipment — last day is Friday",
            description=(
                "Friday is my last day at Contoso. I have a Dell laptop (asset tag CTF-LT-5109), a docking"
                " station, a wireless keyboard and mouse, and a company iPhone. Where do I drop these off?"
                " I work from the London office, 3rd floor of Building 6. Also, do I need to wipe anything"
                " from the phone myself or will IT handle that?"
            ),
            category=Category.GENERAL_INQUIRY,
            priority=Priority.P3,
            team=Team.ENDPOINT,
            needs_escalation=False,
            missing_info=[],
            next_best_action=(
                "Provide equipment return instructions for the London office and confirm that IT will handle"
                " device wiping"
            ),
            remediation_steps=[
                "Direct the user to the IT equipment return desk on the 1st floor of Building 6, London",
                "Advise the user not to wipe or factory-reset any devices — IT will handle data wiping",
                "Confirm the list of equipment to be returned against the asset inventory",
                "Schedule the iPhone MDM unenrollment and remote wipe for the user's last day",
                "Provide a return receipt after all equipment has been checked in",
                "Update the asset management system to mark all items as returned",
            ],
            reporter_name="Tom Beckett",
            reporter_email="tom.beckett@contoso.com",
            reporter_department="Settlements",
            channel=Channel.PORTAL,
            created_at="2026-03-17T11:00:00Z",
            tags=["equipment-return", "offboarding", "london"],
            difficulty="easy",
        ),
        # ──────────────────────────────────────────────────────────────
        # 17. Conference IT setup for offsite meeting
        # ──────────────────────────────────────────────────────────────
        ScenarioDefinition(
            scenario_id="general_inquiry_017",
            subject="IT support needed for client presentation at external venue",
            description=(
                "We are hosting a client presentation at the Mandarin Oriental hotel in NYC on March 25th."
                " There will be about 40 attendees. We need a portable projector, a Teams Room system for"
                " remote participants, and reliable Wi-Fi for live demos. Can IT provide this equipment and"
                " have someone on-site to troubleshoot? The event runs from 9 AM to 4 PM."
            ),
            category=Category.GENERAL_INQUIRY,
            priority=Priority.P3,
            team=Team.ENDPOINT,
            needs_escalation=False,
            missing_info=[MissingInfo.CONFIGURATION_DETAILS, MissingInfo.AFFECTED_USERS],
            next_best_action=(
                "Coordinate portable AV equipment, mobile hotspot for demos, and assign an on-site"
                " technician for the event"
            ),
            remediation_steps=[
                "Reserve a portable projector, Teams Room kit, and mobile hotspot from the AV inventory",
                "Assign an on-site technician for the full event day from 8 AM to 5 PM",
                "Coordinate with the venue to confirm available network ports and Wi-Fi capabilities",
                "Set up a backup mobile hotspot in case venue Wi-Fi is unreliable",
                "Schedule a dry run of the presentation setup at the venue the day before if possible",
                "Prepare a quick-reference troubleshooting guide for the presenting team",
            ],
            reporter_name="Victoria Strand",
            reporter_email="victoria.strand@contoso.com",
            reporter_department="Business Development",
            channel=Channel.EMAIL,
            created_at="2026-03-11T09:30:00Z",
            tags=["event", "offsite", "av-equipment", "client-presentation"],
            difficulty="medium",
        ),
        # ──────────────────────────────────────────────────────────────
        # 18. Hackathon IT setup
        # ──────────────────────────────────────────────────────────────
        ScenarioDefinition(
            scenario_id="general_inquiry_018",
            subject="IT setup for internal hackathon — April 10-11",
            description=(
                "The Engineering department is organizing an internal hackathon on April 10-11 in the NYC"
                " office, 8th floor of Building 1. We expect 60 participants in 12 teams. We need"
                " temporary Wi-Fi credentials for personal laptops, access to a sandboxed cloud environment"
                " for testing, power strips for every team table, and a large display for the demo"
                " presentations at the end. Can IT support this?"
            ),
            category=Category.GENERAL_INQUIRY,
            priority=Priority.P3,
            team=Team.ENDPOINT,
            needs_escalation=False,
            missing_info=[MissingInfo.CONFIGURATION_DETAILS, MissingInfo.BUSINESS_IMPACT],
            next_best_action=(
                "Coordinate hackathon infrastructure: guest Wi-Fi, sandboxed cloud accounts, power"
                " distribution, and AV equipment for demos"
            ),
            remediation_steps=[
                "Generate 60 temporary guest Wi-Fi credentials valid for April 10-11 only",
                "Coordinate with Cloud Infrastructure to provision a sandboxed environment for teams",
                "Arrange power strips and extension cords for 12 team tables with Facilities",
                "Reserve a large display or projector and sound system for demo presentations",
                "Assign two on-site technicians for the duration of the event",
                "Prepare a participant FAQ document with Wi-Fi instructions and support contact info",
            ],
            reporter_name="Raj Patel",
            reporter_email="raj.patel@contoso.com",
            reporter_department="Engineering",
            channel=Channel.PORTAL,
            created_at="2026-03-10T16:00:00Z",
            tags=["hackathon", "event", "nyc", "temporary-access"],
            difficulty="medium",
        ),
        # ──────────────────────────────────────────────────────────────
        # 19. Office desk move — network port needed
        # ──────────────────────────────────────────────────────────────
        ScenarioDefinition(
            scenario_id="general_inquiry_019",
            subject="Desk move to 6th floor — need network port activated",
            description=(
                "I am moving from the 4th floor to the 6th floor of Building 3 in the NYC office next"
                " Monday. Facilities confirmed my new desk but said I need to contact IT to activate the"
                " network port and move my desk phone. My new desk number is 6-042. Can someone make sure"
                " the port is live and my phone extension (x7823) transfers to the new location?"
            ),
            category=Category.GENERAL_INQUIRY,
            priority=Priority.P4,
            team=Team.NETWORK_OPS,
            needs_escalation=False,
            missing_info=[MissingInfo.NETWORK_LOCATION],
            next_best_action=(
                "Activate the network port at desk 6-042, configure the phone extension move, and confirm"
                " connectivity before Monday"
            ),
            remediation_steps=[
                "Verify the network port at desk 6-042 on the 6th floor of Building 3 in the patch panel",
                "Activate the port and assign it to the appropriate VLAN for the user's department",
                "Coordinate with the telephony team to move extension x7823 to the new desk location",
                "Test network connectivity and phone functionality at the new desk before Monday",
                "Update the user's location in the asset management and directory systems",
            ],
            reporter_name="Monica Harris",
            reporter_email="monica.harris@contoso.com",
            reporter_department="Operations",
            channel=Channel.PORTAL,
            created_at="2026-03-12T15:30:00Z",
            tags=["desk-move", "network-port", "phone", "nyc"],
            difficulty="easy",
        ),
        # ──────────────────────────────────────────────────────────────
        # 20. IT governance — system ownership question
        # ──────────────────────────────────────────────────────────────
        ScenarioDefinition(
            scenario_id="general_inquiry_020",
            subject="Who owns the internal portfolio reporting system?",
            description=(
                "I need to request a change to the internal portfolio reporting system — specifically the"
                " automated daily P&L report. I have been told there is a formal change request process but"
                " I do not know who the system owner is or where to submit the request. Can you point me to"
                " the right person or team? I have been using this system for 2 years and this is the first"
                " time I need a modification."
            ),
            category=Category.GENERAL_INQUIRY,
            priority=Priority.P4,
            team=Team.ENTERPRISE_APPS,
            needs_escalation=False,
            missing_info=[MissingInfo.AFFECTED_SYSTEM],
            next_best_action=(
                "Identify the system owner from the IT service catalog and direct the user to the change"
                " request process"
            ),
            remediation_steps=[
                "Look up the portfolio reporting system in the IT service catalog to identify the owner",
                "Provide the user with the system owner's contact information",
                "Share the link to the change request form in ServiceNow",
                "Explain the change advisory board process and typical turnaround time",
                "Suggest the user prepare a brief requirements document to attach to the change request",
            ],
            reporter_name="Daniel Osei",
            reporter_email="daniel.osei@contoso.com",
            reporter_department="Portfolio Management",
            channel=Channel.EMAIL,
            created_at="2026-03-16T09:45:00Z",
            tags=["governance", "system-owner", "change-request"],
            difficulty="easy",
        ),
        # ──────────────────────────────────────────────────────────────
        # 21. Cross-team access coordination
        # ──────────────────────────────────────────────────────────────
        ScenarioDefinition(
            scenario_id="general_inquiry_021",
            subject="Need access from multiple teams for cross-departmental project",
            description=(
                "I have been assigned to a cross-departmental project that requires access to systems owned"
                " by different IT teams. Specifically I need: (1) read access to the data warehouse managed"
                " by Data Platform, (2) access to the CI/CD pipeline in Azure DevOps managed by DevOps,"
                " and (3) a service account for API calls managed by IAM. My manager approved all of these"
                " but I do not know how to request them all in one go. Do I file three separate tickets?"
            ),
            category=Category.GENERAL_INQUIRY,
            priority=Priority.P3,
            team=Team.IAM,
            needs_escalation=False,
            missing_info=[MissingInfo.BUSINESS_IMPACT, MissingInfo.CONFIGURATION_DETAILS],
            next_best_action=(
                "Create a single bundled access request referencing the project, route sub-tasks to Data"
                " Platform, DevOps, and IAM teams in parallel"
            ),
            remediation_steps=[
                "Create a parent ticket for the cross-departmental access request",
                "Create a sub-task for Data Platform to grant read access to the data warehouse",
                "Create a sub-task for DevOps to grant Azure DevOps CI/CD pipeline access",
                "Create a sub-task for IAM to provision a service account with appropriate API scopes",
                "Attach the manager's approval to the parent ticket for all three sub-tasks",
                "Track all sub-tasks to completion and confirm with the user when all access is granted",
            ],
            reporter_name="Yuki Tanaka",
            reporter_email="yuki.tanaka@contoso.com",
            reporter_department="Data Engineering",
            channel=Channel.PORTAL,
            created_at="2026-03-13T14:15:00Z",
            tags=["cross-team", "access-request", "multi-system"],
            difficulty="medium",
        ),
        # ──────────────────────────────────────────────────────────────
        # 22. Vendor VPN access coordination
        # ──────────────────────────────────────────────────────────────
        ScenarioDefinition(
            scenario_id="general_inquiry_022",
            subject="Vendor needs VPN access for system maintenance",
            description=(
                "Our vendor, Murex, is scheduled to perform a system upgrade on the trading risk platform"
                " next weekend. Their engineer, Jean-Pierre Dupont (jp.dupont@murex.com), needs VPN access"
                " to reach the staging environment for pre-upgrade testing starting Wednesday. The access"
                " should expire the following Monday. Who approves external vendor VPN access and what"
                " information do you need from us?"
            ),
            category=Category.GENERAL_INQUIRY,
            priority=Priority.P3,
            team=Team.NETWORK_OPS,
            needs_escalation=False,
            missing_info=[MissingInfo.ENVIRONMENT_DETAILS, MissingInfo.AUTHENTICATION_METHOD],
            next_best_action=(
                "Initiate the vendor VPN access request workflow, obtain security approval, and provision"
                " time-limited credentials scoped to the staging environment"
            ),
            remediation_steps=[
                "Submit a vendor access request form with the vendor engineer's details",
                "Obtain Security Operations approval for external VPN access to the staging environment",
                "Create a time-limited VPN account expiring the following Monday",
                "Restrict the VPN profile to only the staging environment IP range",
                "Send the VPN credentials and connection instructions to the vendor engineer securely",
                "Schedule automatic access revocation on the expiration date",
                "Notify the internal sponsor when the vendor connects and disconnects",
            ],
            reporter_name="Claire Dubois",
            reporter_email="claire.dubois@contoso.com",
            reporter_department="Institutional Trading",
            channel=Channel.EMAIL,
            created_at="2026-03-11T10:00:00Z",
            tags=["vendor-access", "vpn", "external", "time-limited"],
            difficulty="medium",
        ),
        # ──────────────────────────────────────────────────────────────
        # 23. How-to: Teams features
        # ──────────────────────────────────────────────────────────────
        ScenarioDefinition(
            scenario_id="general_inquiry_023",
            subject="How to set up auto-reply and delegate access in Outlook",
            description=(
                "I will be on parental leave for 12 weeks starting April 1st. I need to set up an"
                " out-of-office auto-reply and give my colleague Sarah Chen delegate access to my calendar"
                " and inbox so she can handle meeting requests on my behalf. I know how to set a basic OOO"
                " message but not how to do the delegate part. Can you walk me through it or point me to a"
                " guide?"
            ),
            category=Category.GENERAL_INQUIRY,
            priority=Priority.P4,
            team=Team.NONE,
            needs_escalation=False,
            missing_info=[],
            next_best_action=(
                "Provide step-by-step instructions for setting up Outlook delegate access and auto-reply configuration"
            ),
            remediation_steps=[
                "Send the user the Outlook delegate access guide from the IT knowledge base",
                "Walk through File > Account Settings > Delegate Access to add Sarah Chen",
                "Explain the delegate permission levels: Reviewer, Author, and Editor",
                "Recommend Editor access for calendar and Reviewer access for inbox",
                "Guide the user through the out-of-office auto-reply setup with internal and external message options",
                "Suggest testing the delegate access and auto-reply before the leave start date",
            ],
            reporter_name="Jessica Ling",
            reporter_email="jessica.ling@contoso.com",
            reporter_department="Product Management",
            channel=Channel.CHAT,
            created_at="2026-03-18T08:15:00Z",
            tags=["how-to", "outlook", "delegate-access", "auto-reply"],
            difficulty="easy",
        ),
        # ──────────────────────────────────────────────────────────────
        # 24. Asset inventory question
        # ──────────────────────────────────────────────────────────────
        ScenarioDefinition(
            scenario_id="general_inquiry_024",
            subject="What laptop model do I have? Can't find my asset tag",
            description=(
                "I am filling out a form that asks for my laptop model and asset tag number, but I can not"
                " find the asset tag sticker on my device. It might have fallen off. I think it is a Dell"
                " Latitude but I am not sure of the exact model. Is there a way to look this up in a system?"
                " My name is Omar Farouk and I am in the Singapore office, Middle Office team."
            ),
            category=Category.GENERAL_INQUIRY,
            priority=Priority.P4,
            team=Team.ENDPOINT,
            needs_escalation=False,
            missing_info=[MissingInfo.DEVICE_INFO],
            next_best_action=(
                "Look up the user's assigned assets in the CMDB by employee name and provide the laptop"
                " model and asset tag"
            ),
            remediation_steps=[
                "Search the asset management system (CMDB) for devices assigned to Omar Farouk",
                "Provide the user with the laptop model, serial number, and asset tag",
                "Advise the user to run 'wmic bios get serialnumber' in Command Prompt to verify locally",
                "Arrange for a replacement asset tag sticker to be sent to the Singapore office",
                "Update the CMDB record if any information is outdated",
            ],
            reporter_name="Omar Farouk",
            reporter_email="omar.farouk@contoso.com",
            reporter_department="Middle Office",
            channel=Channel.CHAT,
            created_at="2026-03-06T04:45:00Z",
            tags=["asset-inventory", "asset-tag", "singapore"],
            difficulty="easy",
        ),
        # ──────────────────────────────────────────────────────────────
        # 25. Partner SharePoint access request
        # ──────────────────────────────────────────────────────────────
        ScenarioDefinition(
            scenario_id="general_inquiry_025",
            subject="External partner needs access to shared SharePoint site",
            description=(
                "We are collaborating with our external auditors at KPMG on the annual audit. They need"
                " access to a shared SharePoint site where we will upload the audit working papers. There"
                " are 4 KPMG auditors who need access: j.smith@kpmg.com, r.jones@kpmg.com,"
                " a.williams@kpmg.com, and m.brown@kpmg.com. The site should have strict DLP policies so"
                " they cannot download or forward files. Access should expire on June 30th. Our Internal"
                " Audit lead, Frank Moretti, has approved this."
            ),
            category=Category.GENERAL_INQUIRY,
            priority=Priority.P3,
            team=Team.IAM,
            needs_escalation=False,
            missing_info=[MissingInfo.CONFIGURATION_DETAILS],
            next_best_action=(
                "Provision external guest access to the SharePoint site with DLP restrictions and a June"
                " 30th expiration date"
            ),
            remediation_steps=[
                "Create a SharePoint site or document library for the audit collaboration if one does not exist",
                "Configure DLP policies to prevent download, print, and forwarding of documents",
                "Send Azure AD B2B guest invitations to the four KPMG email addresses",
                "Assign the external guests Contributor or Reader permissions as specified by Internal Audit",
                "Set an access expiration date of June 30th on all guest accounts",
                "Notify Frank Moretti when access has been provisioned with a summary of permissions",
                "Schedule a quarterly access review to ensure guest accounts are still needed",
            ],
            reporter_name="Frank Moretti",
            reporter_email="frank.moretti@contoso.com",
            reporter_department="Internal Audit",
            channel=Channel.EMAIL,
            created_at="2026-03-09T08:00:00Z",
            tags=["external-access", "sharepoint", "partner", "audit", "dlp"],
            difficulty="medium",
        ),
    ]
