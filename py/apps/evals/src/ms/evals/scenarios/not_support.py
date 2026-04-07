# Copyright (c) Microsoft. All rights reserved.
"""Not a Support Ticket scenario templates.

Covers: auto-replies, out-of-office, 'thanks' messages, spam,
forwarded newsletters, wrong department submissions, calendar invites,
vendor sales pitches, test messages, social/non-work content,
and accidental submissions.
"""

from ms.evals.constants import Category
from ms.evals.constants import Priority
from ms.evals.constants import Team
from ms.evals.models import ScenarioTemplate
from ms.evals.scenarios.registry import register

# ---------------------------------------------------------------------------
# ns-001  Auto-reply / out-of-office response
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="ns-001",
        category=Category.NOT_SUPPORT,
        priority=Priority.P4,
        assigned_team=Team.NONE,
        needs_escalation=False,
        missing_information=[],
        subjects=[
            "Out of Office: {name}",
            "Automatic reply: Re: Your IT request #{ticket_id}",
            "OOO: I am currently out of the office",
        ],
        descriptions=[
            "Thank you for your email. I am currently out of the office with no access to email "
            "from {start_date} through {end_date}. For urgent matters, please contact {backup_name} "
            "at {backup_email}. I will respond to your message upon my return. Best regards, {name}",
            "Hi, I'm away from the office this week attending a conference. I'll have limited "
            "access to email and will reply when I get back on {return_date}. If this is urgent, "
            "please reach out to my manager {manager_name}. Thanks!",
            "This is an automated response. I am on PTO until {return_date} and will not be "
            "checking email. For immediate assistance, please contact the help desk directly. "
            "Thank you for your patience.",
        ],
        next_best_actions=[
            "Close — this is an auto-reply, not an actual support request.",
        ],
        remediation_steps=[
            [
                "No action required — auto-reply / out-of-office message, close ticket",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# ns-002  Simple "thanks!" or "got it" message
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="ns-002",
        category=Category.NOT_SUPPORT,
        priority=Priority.P4,
        assigned_team=Team.NONE,
        needs_escalation=False,
        missing_information=[],
        subjects=[
            "Re: Ticket #{ticket_id} — Thanks!",
            "Re: Your request has been resolved",
            "Got it, thanks!",
        ],
        descriptions=[
            "Thanks! That fixed it. Appreciate the quick help!",
            "Got it, everything is working now. Thanks so much!",
            "Awesome, thank you! You can close this ticket.",
        ],
        next_best_actions=[
            "Close — user is confirming resolution, no further action needed.",
        ],
        remediation_steps=[
            [
                "No action required — user acknowledgement of resolved issue, close ticket",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# ns-003  Forwarded spam email
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="ns-003",
        category=Category.NOT_SUPPORT,
        priority=Priority.P4,
        assigned_team=Team.NONE,
        needs_escalation=False,
        missing_information=[],
        subjects=[
            "FW: CONGRATULATIONS! You've won $5,000,000!!!",
            "Fwd: URGENT — Claim your prize NOW",
            "FW: You have been selected as a winner",
        ],
        descriptions=[
            "---------- Forwarded message ----------\n"
            "CONGRATULATIONS!!! You have been randomly selected as the winner of our $5,000,000 "
            "International Lottery Program! To claim your prize, reply immediately with your full "
            "name, address, phone number, and bank account details. This offer expires in 24 HOURS. "
            "Act now! — Dr. James Williams, Claims Agent, Global Lottery Commission",
            "---------- Forwarded message ----------\n"
            "DEAR LUCKY WINNER, Your email was selected in our annual Microsoft Employee "
            "Sweepstakes. You have won USD $2,500,000.00! To process your winnings, kindly send "
            "your Social Security Number and a copy of your ID to claims@totally-real-lottery.com. "
            "Sincerely, The Prize Committee",
            "Hey IT, I got this weird email. Not sure if it's real but thought you should know.\n\n"
            "--- Original Message ---\n"
            "Subject: YOU WON! Claim $1,000,000 now!\n"
            "Dear recipient, you have been chosen for a cash prize of ONE MILLION DOLLARS...",
        ],
        next_best_actions=[
            "Close — this is forwarded spam, not a support request. If the user is concerned, "
            "advise them to delete the email and not click any links.",
        ],
        remediation_steps=[
            [
                "No action required — forwarded spam email, close ticket",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# ns-004  Forwarded company newsletter
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="ns-004",
        category=Category.NOT_SUPPORT,
        priority=Priority.P4,
        assigned_team=Team.NONE,
        needs_escalation=False,
        missing_information=[],
        subjects=[
            "FW: Weekly IT Newsletter — March Edition",
            "Fwd: Company Update: Q2 Goals and Initiatives",
            "FW: Tech Tips Tuesday — March 15",
        ],
        descriptions=[
            "---------- Forwarded message ----------\n"
            "IT WEEKLY NEWSLETTER — MARCH EDITION\n\n"
            "🔧 Upcoming Maintenance: Server patching this Saturday 11pm-2am\n"
            "📱 New Feature: Self-service password reset now available\n"
            "📊 Tip of the Week: How to use Teams breakout rooms\n\n"
            "Questions? Contact the IT Help Desk.",
            "FYI — just passing along the company newsletter. Not sure why it came to the IT "
            "ticket queue.\n\n--- Original ---\nCompany Weekly Update: Welcome to our new hires, "
            "reminder about the office picnic next Friday, and an update on the building "
            "renovation project...",
        ],
        next_best_actions=[
            "Close — this is a forwarded newsletter, not a support request.",
        ],
        remediation_steps=[
            [
                "No action required — forwarded newsletter accidentally submitted as ticket, close ticket",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# ns-005  Calendar meeting invite submission
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="ns-005",
        category=Category.NOT_SUPPORT,
        priority=Priority.P4,
        assigned_team=Team.NONE,
        needs_escalation=False,
        missing_information=[],
        subjects=[
            "Team Standup — Daily 9:00 AM",
            "Invitation: Project Kickoff Meeting",
            "Updated: Weekly Sync — moved to 2pm",
        ],
        descriptions=[
            "When: Monday–Friday, 9:00 AM – 9:15 AM\n"
            "Where: Teams Meeting\n"
            "Organizer: {name}\n\n"
            "Hi team, joining link below. See you there!\n"
            "________________\n"
            "Microsoft Teams meeting\n"
            "Join on your computer, mobile app or room device\n"
            "Click here to join the meeting",
            "You've been invited to the following event:\n\n"
            "Project Kickoff Meeting\n"
            "Date: {date}, 10:00 AM – 11:00 AM\n"
            "Location: Conference Room B / Teams\n"
            "Organizer: {name}\n\n"
            "Please RSVP. Agenda to follow.",
        ],
        next_best_actions=[
            "Close — this is a calendar invite, not a support request.",
        ],
        remediation_steps=[
            [
                "No action required — calendar meeting invite submitted as ticket by mistake, close ticket",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# ns-006  HR question submitted to IT (wrong department)
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="ns-006",
        category=Category.NOT_SUPPORT,
        priority=Priority.P4,
        assigned_team=Team.NONE,
        needs_escalation=False,
        missing_information=[],
        subjects=[
            "Question about my PTO balance",
            "How do I update my tax withholding?",
            "Benefits enrollment deadline question",
        ],
        descriptions=[
            "Hi, I'm trying to figure out how many PTO days I have left this year. I checked "
            "Workday but the numbers don't look right. Can someone help me reconcile my time-off "
            "balance? I took 5 days in January and 3 in February but it's showing I only have "
            "2 remaining which can't be right.",
            "I need to update my W-4 tax withholding — where do I go to change that? Also, is "
            "open enrollment for health benefits still going on? I think I missed the email with "
            "the deadline.",
        ],
        next_best_actions=[
            "Close — this is an HR question, not an IT issue. Redirect the user to HR.",
        ],
        remediation_steps=[
            [
                "No action required — HR question submitted to IT by mistake, redirect user to HR and close ticket",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# ns-007  Facilities request submitted to IT (office AC broken)
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="ns-007",
        category=Category.NOT_SUPPORT,
        priority=Priority.P4,
        assigned_team=Team.NONE,
        needs_escalation=False,
        missing_information=[],
        subjects=[
            "AC is broken on the 3rd floor",
            "Office temperature is freezing — can someone fix the heat?",
            "Bathroom on 2nd floor needs maintenance",
        ],
        descriptions=[
            "The air conditioning on the 3rd floor has been out since yesterday and it's "
            "unbearable up here. It must be 85 degrees. Multiple people have complained. Can "
            "someone from maintenance come take a look ASAP?",
            "The heating in Building A, Floor 2 is not working and it's really cold. We've been "
            "wearing coats at our desks all morning. This needs to be looked at today. Please send "
            "someone from facilities.",
        ],
        next_best_actions=[
            "Close — this is a facilities/maintenance request, not IT. Redirect to facilities.",
        ],
        remediation_steps=[
            [
                "No action required — facilities request submitted to IT, redirect to facilities and close ticket",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# ns-008  Vendor sales pitch forwarded
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="ns-008",
        category=Category.NOT_SUPPORT,
        priority=Priority.P4,
        assigned_team=Team.NONE,
        needs_escalation=False,
        missing_information=[],
        subjects=[
            "FW: Transform your IT operations with CloudSync Pro!",
            "Fwd: Exclusive offer — 50% off enterprise security suite",
            "FW: Let's schedule a demo — AI-powered helpdesk solution",
        ],
        descriptions=[
            "---------- Forwarded message ----------\n"
            "Hi {name},\n\n"
            "I'm reaching out from CloudSync Pro — we help companies like yours reduce IT "
            "ticket volume by 60% using AI-powered automation. I'd love to schedule a quick "
            "15-minute demo to show you how we can transform your service desk.\n\n"
            "Are you available this Thursday or Friday?\n\n"
            "Best,\nJake Thompson\nEnterprise Sales, CloudSync Pro\n"
            "jake@cloudsyncpro.io | (555) 123-4567",
            "Someone forwarded this sales email to the ticket queue. Not sure why.\n\n"
            "--- Original ---\n"
            "Subject: Special pricing — Enterprise Security Suite\n"
            "Hi, we noticed your company might benefit from our next-gen endpoint protection "
            "platform. For a limited time, we're offering 50% off annual licenses. Let me know "
            "if you'd like to chat! — Sarah, BizSecure Inc.",
        ],
        next_best_actions=[
            "Close — this is a vendor sales pitch, not a support request.",
        ],
        remediation_steps=[
            [
                "No action required — vendor solicitation forwarded to ticket queue, close ticket",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# ns-009  Test ticket — "please ignore"
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="ns-009",
        category=Category.NOT_SUPPORT,
        priority=Priority.P4,
        assigned_team=Team.NONE,
        needs_escalation=False,
        missing_information=[],
        subjects=[
            "TEST — please ignore",
            "Test ticket — do not action",
            "Testing 123",
        ],
        descriptions=[
            "This is a test ticket. Please ignore.",
            "Just testing the ticket submission form. Nothing to do here. Sorry!",
            "test test test\n\nIgnore this — I was showing a new employee how to submit tickets.",
        ],
        next_best_actions=[
            "Close — this is a test ticket submitted intentionally.",
        ],
        remediation_steps=[
            [
                "No action required — test ticket, close ticket",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# ns-010  Social message — "Happy Birthday Dave!"
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="ns-010",
        category=Category.NOT_SUPPORT,
        priority=Priority.P4,
        assigned_team=Team.NONE,
        needs_escalation=False,
        missing_information=[],
        subjects=[
            "Happy Birthday Dave!",
            "Congrats on the promotion, Sarah! 🎉",
            "Welcome baby announcement — {name}!",
        ],
        descriptions=[
            "🎂 Happy Birthday Dave!! 🎉🎉🎉\n\n"
            "Hope you have an amazing day! Cake in the break room at 3pm — everyone's invited! "
            "— The 4th Floor Crew",
            "Huge congrats to Sarah on her well-deserved promotion to Senior Director! 🎉 "
            "Join us for a celebration lunch this Friday at noon in the main conference room. "
            "RSVP to {name}.",
            "Please join us in congratulating {name} and their family on the arrival of baby "
            "{baby_name}! Mom and baby are doing great. A card is circulating on the 2nd floor "
            "if you'd like to sign it!",
        ],
        next_best_actions=[
            "Close — this is a social/personal message, not a support request.",
        ],
        remediation_steps=[
            [
                "No action required — social message submitted to IT by mistake, close ticket",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# ns-011  Delivery receipt / read receipt
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="ns-011",
        category=Category.NOT_SUPPORT,
        priority=Priority.P4,
        assigned_team=Team.NONE,
        needs_escalation=False,
        missing_information=[],
        subjects=[
            "Read: Your IT request has been received",
            "Delivered: Re: Ticket #{ticket_id}",
            "Read receipt: Password reset confirmation",
        ],
        descriptions=[
            "Your message\n\n  To: IT Help Desk\n  Subject: Password reset request\n  "
            "Sent: {date} {time}\n\nwas read on {date} at {time}.",
            "This is a delivery confirmation for the message you sent to ithelpdesk@company.com "
            "on {date} at {time}.\n\nThis message was successfully delivered to the recipient's "
            "mailbox.",
            "Read notification: The following message was read by the recipient.\n"
            "Subject: Re: Ticket #{ticket_id}\nSent: {date}",
        ],
        next_best_actions=[
            "Close — this is an automated read/delivery receipt, not a support request.",
        ],
        remediation_steps=[
            [
                "No action required — automated delivery or read receipt, close ticket",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# ns-012  Automated system notification — scheduled maintenance
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="ns-012",
        category=Category.NOT_SUPPORT,
        priority=Priority.P4,
        assigned_team=Team.NONE,
        needs_escalation=False,
        missing_information=[],
        subjects=[
            "NOTIFICATION: Scheduled maintenance — Saturday 11pm-2am",
            "System Alert: Planned downtime for ERP system",
            "Automated Notice: Monthly patching window",
        ],
        descriptions=[
            "*** AUTOMATED NOTIFICATION — DO NOT REPLY ***\n\n"
            "Scheduled Maintenance Window\n"
            "System: Exchange Online\n"
            "Date: Saturday, {date}\n"
            "Time: 11:00 PM – 2:00 AM EST\n"
            "Impact: Email may be intermittently unavailable\n\n"
            "No action is required. This is a planned maintenance activity.",
            "SYSTEM NOTIFICATION\n\n"
            "The ERP system will undergo planned maintenance on {date} from {start_time} to "
            "{end_time}. During this window the system will be unavailable. Please save your "
            "work before the maintenance begins.\n\n"
            "This is an automated message. Do not reply.",
        ],
        next_best_actions=[
            "Close — this is an automated system notification, not a support request.",
        ],
        remediation_steps=[
            [
                "No action required — automated system maintenance notification, close ticket",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# ns-013  Personal question unrelated to IT
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="ns-013",
        category=Category.NOT_SUPPORT,
        priority=Priority.P4,
        assigned_team=Team.NONE,
        needs_escalation=False,
        missing_information=[],
        subjects=[
            "Does anyone have jumper cables?",
            "Lost my jacket in the office — anyone seen it?",
            "Carpool to the company picnic?",
        ],
        descriptions=[
            "Hey, this is kind of random but my car won't start in the parking garage — dead "
            "battery. Does anyone in IT have jumper cables I could borrow? I'm on level P2 near "
            "the elevator. Thanks!",
            "I left my blue North Face jacket somewhere in the building yesterday — I think maybe "
            "in the 3rd floor conference room or the break room. Has anyone turned it in? It has "
            "my badge in the pocket too.",
            "Anyone driving to the company picnic this Saturday from the downtown office? Looking "
            "for a carpool buddy. I can chip in for gas!",
        ],
        next_best_actions=[
            "Close — this is a personal question unrelated to IT support.",
        ],
        remediation_steps=[
            [
                "No action required — personal non-IT question, close ticket",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# ns-014  Forwarded chain email / chain letter
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="ns-014",
        category=Category.NOT_SUPPORT,
        priority=Priority.P4,
        assigned_team=Team.NONE,
        needs_escalation=False,
        missing_information=[],
        subjects=[
            "FW: FW: FW: You MUST read this!!!!!",
            "Fwd: Send this to 10 people or else!",
            "FW: FW: Inspirational story — pass it on",
        ],
        descriptions=[
            "---------- Forwarded message ----------\n"
            ">>>>>> FORWARD THIS TO 10 PEOPLE IN THE NEXT HOUR OR YOU WILL HAVE BAD LUCK "
            "FOR 7 YEARS!!! This has been verified by Microsoft and AOL. For every person "
            "you forward this to, Bill Gates will donate $1 to charity. THIS IS REAL!!! Don't "
            "break the chain!! >>>>>>",
            "FW: FW: FW: FW:\n\n"
            "A little boy in the hospital needs your prayers. Forward this email to everyone "
            "you know and Microsoft will donate 5 cents for each forward. It was on the news! "
            "Please don't delete this. 🙏\n\n"
            "--- forwarded 47 times ---",
        ],
        next_best_actions=[
            "Close — this is a forwarded chain email, not a support request.",
        ],
        remediation_steps=[
            [
                "No action required — chain email forwarded to ticket queue, close ticket",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# ns-015  Accidentally submitted empty ticket
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="ns-015",
        category=Category.NOT_SUPPORT,
        priority=Priority.P4,
        assigned_team=Team.NONE,
        needs_escalation=False,
        missing_information=[],
        subjects=[
            "(No subject)",
            "(blank)",
            "Untitled",
        ],
        descriptions=[
            "(empty)",
            ".",
            "asdf",
        ],
        next_best_actions=[
            "Close — this appears to be an accidentally submitted empty or blank ticket.",
        ],
        remediation_steps=[
            [
                "No action required — empty or accidental ticket submission, close ticket",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# ns-016  Duplicate submission of resolved ticket
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="ns-016",
        category=Category.NOT_SUPPORT,
        priority=Priority.P4,
        assigned_team=Team.NONE,
        needs_escalation=False,
        missing_information=[],
        subjects=[
            "Re: Ticket #{ticket_id} (RESOLVED)",
            "Same issue as my last ticket — already fixed",
            "Duplicate: password reset (already done)",
        ],
        descriptions=[
            "I think I accidentally submitted this twice — my issue from ticket #{ticket_id} was "
            "already resolved yesterday by {agent_name}. Please disregard this one. Sorry about "
            "the duplicate!",
            "This is the same as the ticket I submitted this morning. You can close this one — "
            "someone already reached out and fixed the problem. My apologies for the double "
            "submission.",
            "Oops, I hit submit twice. This is a duplicate of the request I just sent in. "
            "Everything is already taken care of. Please close.",
        ],
        next_best_actions=[
            "Close — user confirmed this is a duplicate of an already-resolved ticket.",
        ],
        remediation_steps=[
            [
                "No action required — duplicate of previously resolved ticket, close ticket",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# ns-017  Employee satisfaction survey response
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="ns-017",
        category=Category.NOT_SUPPORT,
        priority=Priority.P4,
        assigned_team=Team.NONE,
        needs_escalation=False,
        missing_information=[],
        subjects=[
            "IT Support Satisfaction Survey — My Feedback",
            "Survey response: How was your IT experience?",
            "Re: Please rate your IT support experience",
        ],
        descriptions=[
            "Rating: 4/5 ⭐⭐⭐⭐\n\n"
            "The technician was very helpful and resolved my issue quickly. Only reason it's not "
            "5 stars is because I had to wait 2 days for the initial response. Overall great "
            "experience though. Keep up the good work!",
            "Hi, I'm responding to the survey you sent after my last ticket. Everything was "
            "excellent — {agent_name} was super knowledgeable and patient. 10/10 would recommend. "
            "Thanks for the great support!",
            "Feedback on recent IT interaction: The support was fine but the hold time on the "
            "phone was too long (waited 25 minutes). Once I got through, the agent fixed my "
            "issue in 5 minutes. Suggestion: add more phone agents during peak hours.",
        ],
        next_best_actions=[
            "Close — this is survey feedback, not a support request. Forward to the service "
            "desk manager if actionable.",
        ],
        remediation_steps=[
            [
                "No action required — survey feedback submitted as ticket, close ticket",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# ns-018  Recruitment / job posting forwarded
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="ns-018",
        category=Category.NOT_SUPPORT,
        priority=Priority.P4,
        assigned_team=Team.NONE,
        needs_escalation=False,
        missing_information=[],
        subjects=[
            "FW: We're hiring! Senior Network Engineer position",
            "Fwd: Job opening — IT Support Analyst",
            "FW: Know anyone? Open role in cybersecurity team",
        ],
        descriptions=[
            "---------- Forwarded message ----------\n"
            "We're hiring! 🚀\n\n"
            "Position: Senior Network Engineer\n"
            "Location: Seattle, WA (Hybrid)\n"
            "Team: Infrastructure & Cloud Operations\n\n"
            "Know someone great? Send them this link: careers.company.com/jobs/12345\n"
            "Employee referral bonus applies! — Talent Acquisition Team",
            "FYI forwarding this job posting. Not sure why it ended up in the IT ticket queue.\n\n"
            "--- Original ---\n"
            "Open Role: IT Support Analyst (Level 2)\n"
            "We're looking for a motivated support analyst to join our growing team. 3+ years "
            "experience required. Apply at careers.company.com/jobs/67890",
        ],
        next_best_actions=[
            "Close — this is a forwarded job posting, not a support request.",
        ],
        remediation_steps=[
            [
                "No action required — recruitment posting forwarded to ticket queue, close ticket",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# ns-019  Internal announcement about office event
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="ns-019",
        category=Category.NOT_SUPPORT,
        priority=Priority.P4,
        assigned_team=Team.NONE,
        needs_escalation=False,
        missing_information=[],
        subjects=[
            "🎉 Annual Summer BBQ — Save the Date!",
            "FW: Office Holiday Party — December 15",
            "Reminder: Charity bake sale this Thursday",
        ],
        descriptions=[
            "You're invited! 🎉\n\n"
            "ANNUAL SUMMER BBQ\n"
            "Date: Friday, July 12\n"
            "Time: 11:30 AM – 2:00 PM\n"
            "Location: Rooftop Patio\n\n"
            "Food, drinks, lawn games, and raffle prizes! Bring your appetite. RSVP on the "
            "intranet by July 5. Family members welcome. — Social Committee",
            "Reminder: The charity bake sale is this Thursday in the main lobby! All proceeds go "
            "to the local food bank. Bring your best baked goods and your appetite. Sign up to "
            "volunteer at the link below. — Community Outreach Team",
        ],
        next_best_actions=[
            "Close — this is an office event announcement, not a support request.",
        ],
        remediation_steps=[
            [
                "No action required — internal event announcement submitted as ticket, close ticket",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# ns-020  External customer complaint (not IT)
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="ns-020",
        category=Category.NOT_SUPPORT,
        priority=Priority.P4,
        assigned_team=Team.NONE,
        needs_escalation=False,
        missing_information=[],
        subjects=[
            "Complaint about my order #{order_id}",
            "TERRIBLE customer service — want a refund",
            "Product defective — requesting replacement",
        ],
        descriptions=[
            "I ordered a product from your website 3 weeks ago (Order #{order_id}) and it still "
            "hasn't arrived. I've tried calling customer service twice and nobody can tell me "
            "where my package is. This is unacceptable. I want a full refund or the product "
            "shipped overnight immediately. — {name}, loyal customer since 2019",
            "I'm extremely dissatisfied with the service I received. I was promised a callback "
            "within 24 hours regarding my billing dispute and it's been 5 days. I'm considering "
            "taking my business elsewhere. Please have a manager contact me at {phone}.",
        ],
        next_best_actions=[
            "Close — this is an external customer complaint routed to IT by mistake. Redirect to customer service.",
        ],
        remediation_steps=[
            [
                "No action required — external customer complaint routed to IT, redirect to customer service,"
                " close ticket",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# ns-021  Auto-generated bounce/NDR email
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="ns-021",
        category=Category.NOT_SUPPORT,
        priority=Priority.P4,
        assigned_team=Team.NONE,
        needs_escalation=False,
        missing_information=[],
        subjects=[
            "Undeliverable: Re: IT Ticket #{ticket_id}",
            "Mail Delivery Subsystem — Delivery Status Notification (Failure)",
            "Returned mail: User unknown",
        ],
        descriptions=[
            "This is an automatically generated Delivery Status Notification.\n\n"
            "Delivery to the following recipient failed permanently:\n\n"
            "    {email}\n\n"
            "Technical details of permanent failure:\n"
            "550 5.1.1 The email account that you tried to reach does not exist. Please try "
            "double-checking the recipient's email address for typos or unnecessary spaces.",
            "The following message to <{email}> was undeliverable.\n"
            "The reason for the problem:\n"
            "5.1.0 — Unknown address error 550-'{email}... User unknown'\n\n"
            "--- Original message header ---\n"
            "Subject: Re: IT Ticket #{ticket_id}\n"
            "Date: {date}",
        ],
        next_best_actions=[
            "Close — this is an automated non-delivery report (bounce), not a support request.",
        ],
        remediation_steps=[
            [
                "No action required — automated email bounce notification, close ticket",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# ns-022  Payroll question submitted to IT
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="ns-022",
        category=Category.NOT_SUPPORT,
        priority=Priority.P4,
        assigned_team=Team.NONE,
        needs_escalation=False,
        missing_information=[],
        subjects=[
            "My paycheck was short this month",
            "Direct deposit didn't go through",
            "Question about overtime pay calculation",
        ],
        descriptions=[
            "Hi, my paycheck this month is about $500 less than expected. I worked the same hours "
            "as usual and I don't see any deductions that would explain it. Can someone look into "
            "this? My employee ID is {employee_id}. I need this resolved before rent is due on "
            "the 1st.",
            "My direct deposit didn't come through on Friday. Everyone else on my team got paid "
            "but my bank shows nothing. I double-checked my account number in Workday and it "
            "looks correct. Please help — this is urgent.",
        ],
        next_best_actions=[
            "Close — this is a payroll question, not an IT issue. Redirect the user to Payroll/HR.",
        ],
        remediation_steps=[
            [
                "No action required — payroll question submitted to IT, redirect to payroll and close ticket",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# ns-023  Forwarded phishing awareness test email
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="ns-023",
        category=Category.NOT_SUPPORT,
        priority=Priority.P4,
        assigned_team=Team.NONE,
        needs_escalation=False,
        missing_information=[],
        subjects=[
            "FW: Is this a phishing test?",
            "Fwd: Suspicious email — I think it's the awareness test",
            "FW: Urgent action required on your account (phishing sim?)",
        ],
        descriptions=[
            "Hey IT team, I got this email and I'm pretty sure it's one of those phishing "
            "awareness tests you guys run. Just forwarding it to confirm. I didn't click anything.\n\n"
            "--- Original ---\n"
            "Subject: Urgent: Your account will be suspended in 24 hours\n"
            "Dear employee, we detected unusual activity on your corporate account. Click here "
            "to verify your identity immediately or your access will be revoked: "
            "http://secure-login-verify.com/auth",
            "I think this is the monthly phishing simulation but wanted to flag it just in case "
            "it's real. I already reported it using the Phish Alert button in Outlook.\n\n"
            "--- Forwarded ---\n"
            "From: IT Security <security@c0mpany.com>\n"
            "Subject: Password expiring today — click to renew\n"
            "Your password expires in 2 hours. Click below to reset now...",
        ],
        next_best_actions=[
            "Close — user correctly identified a phishing simulation test. Acknowledge their vigilance.",
        ],
        remediation_steps=[
            [
                "No action required — user forwarded a phishing awareness test email, close ticket",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# ns-024  Meeting room scheduling conflict (not IT issue)
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="ns-024",
        category=Category.NOT_SUPPORT,
        priority=Priority.P4,
        assigned_team=Team.NONE,
        needs_escalation=False,
        missing_information=[],
        subjects=[
            "Someone booked over my meeting room reservation!",
            "Conference room double-booked again",
            "Meeting room conflict — who do I talk to?",
        ],
        descriptions=[
            "I had Conference Room 3B booked for 2pm today but when I showed up, another team "
            "was already in there and said they had it reserved too. The booking system is showing "
            "both reservations. This is the third time this month. Can someone sort this out? "
            "I need the room for a client call.",
            "Room 4A is double-booked for tomorrow at 10am. I reserved it two weeks ago for a "
            "board presentation and now I see someone else has it too. This isn't really an IT "
            "issue but I don't know who else to contact. Help?",
        ],
        next_best_actions=[
            "Close — this is a meeting room scheduling conflict, not an IT issue. Redirect to "
            "office administration or facilities.",
        ],
        remediation_steps=[
            [
                "No action required — meeting room scheduling conflict, redirect to office admin and close ticket",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# ns-025  Random question — "What's the cafeteria menu today?"
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="ns-025",
        category=Category.NOT_SUPPORT,
        priority=Priority.P4,
        assigned_team=Team.NONE,
        needs_escalation=False,
        missing_information=[],
        subjects=[
            "What's the cafeteria menu today?",
            "Is the coffee machine on the 2nd floor fixed?",
            "Does anyone know the WiFi password for the gym?",
        ],
        descriptions=[
            "Random question — does anyone know what the cafeteria is serving today? Their website "
            "hasn't been updated since last week and I'm trying to decide if I should bring lunch "
            "from home. Also, are they still doing Taco Tuesdays?",
            "Hey, the coffee machine on the 2nd floor break room has been broken for like two "
            "weeks. It just makes a grinding noise and no coffee comes out. I know this probably "
            "isn't an IT thing but I didn't know who else to ask. We need our coffee!",
            "Quick question — does anyone know the WiFi password for the gym in the basement? I "
            "want to stream music during my lunch workout. It's not the same as the corporate "
            "WiFi right?",
        ],
        next_best_actions=[
            "Close — this is a non-IT general question. Redirect to the appropriate department.",
        ],
        remediation_steps=[
            [
                "No action required — non-IT question about office amenities, close ticket",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# ns-026  Employee forwarding marketing newsletter asking to unsubscribe
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="ns-026",
        category=Category.NOT_SUPPORT,
        priority=Priority.P4,
        assigned_team=Team.NONE,
        needs_escalation=False,
        missing_information=[],
        subjects=[
            "Please unsubscribe me from this newsletter",
            "FW: Weekly Marketing Digest — how do I stop getting these?",
            "Remove me from this mailing list",
        ],
        descriptions=[
            "Hi, I keep getting this marketing newsletter every week and I can't figure out how to "
            "unsubscribe. I've attached a screenshot of the email. I tried clicking the unsubscribe "
            "link at the bottom but it just takes me to a broken page. Can you remove me from the "
            "list? I don't even remember signing up for this.",
            "Hey, I'm forwarding this newsletter I keep receiving — it's from the marketing team's "
            "external vendor. I've asked them twice to take me off the distribution list but the "
            "emails keep coming. This isn't really an IT issue but I didn't know who else to ask. "
            "Can someone help me stop receiving these?",
        ],
        next_best_actions=[
            "Close — this is a newsletter unsubscribe request, not an IT support issue. Redirect "
            "the employee to the marketing team or the newsletter's unsubscribe link.",
        ],
        remediation_steps=[
            [
                "No action required — newsletter unsubscribe request, close ticket and redirect to marketing team",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# ns-027  Accidental ticket from auto-reply email bot
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="ns-027",
        category=Category.NOT_SUPPORT,
        priority=Priority.P4,
        assigned_team=Team.NONE,
        needs_escalation=False,
        missing_information=[],
        subjects=[
            "Re: Re: Re: Automatic Reply",
            "Auto-Reply: Message delivery notification",
            "Undeliverable: Re: Your recent request",
        ],
        descriptions=[
            "This is an automated message to confirm that your email was received. Please do not "
            "reply to this message as this mailbox is not monitored. If you need immediate "
            "assistance, please contact the service desk directly. Reference ID: AUTO-8847231.",
            "Your message to noreply@contoso.com has been received and logged. This is an automated "
            "acknowledgment — no human has reviewed your request yet. You will receive a follow-up "
            "within 24 business hours. This mailbox does not accept replies.",
        ],
        next_best_actions=[
            "Close — this is an auto-generated bot reply that accidentally created a ticket.",
        ],
        remediation_steps=[
            [
                "No action required — auto-reply bot message, close ticket",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# ns-028  Employee submitting expense report to wrong portal
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="ns-028",
        category=Category.NOT_SUPPORT,
        priority=Priority.P4,
        assigned_team=Team.NONE,
        needs_escalation=False,
        missing_information=[],
        subjects=[
            "Expense report submission — business trip to Chicago",
            "Reimbursement request: client dinner 11/15",
            "Expense claim for Q4 travel",
        ],
        descriptions=[
            "Hi, I'm submitting my expense report for the Chicago business trip last week. I have "
            "receipts for the hotel ($189/night for 3 nights), flights ($342 round trip), meals "
            "($127 total), and ground transportation ($45 Uber). Please process at your earliest "
            "convenience. My cost center is CC-4410 and my manager has already approved it verbally.",
            "Please find attached my reimbursement request for the client dinner on November 15th. "
            "Total amount is $237.50 for four attendees. I've included the itemized receipt and the "
            "pre-approval form signed by my director. Let me know if you need anything else to "
            "process this. Thanks!",
        ],
        next_best_actions=[
            "Close — this is an expense report submission, not an IT support request. Redirect "
            "the employee to the finance portal or accounts payable team.",
        ],
        remediation_steps=[
            [
                "No action required — expense report submitted to wrong portal, close ticket "
                "and redirect to finance or accounts payable",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# ns-029  Vendor sales pitch disguised as a support request
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="ns-029",
        category=Category.NOT_SUPPORT,
        priority=Priority.P4,
        assigned_team=Team.NONE,
        needs_escalation=False,
        missing_information=[],
        subjects=[
            "Improving your endpoint security — free assessment",
            "Partnership opportunity: next-gen cloud monitoring solution",
            "Quick question about your current IT infrastructure",
        ],
        descriptions=[
            "Hi there! I'm reaching out from SecureNet Solutions. We help mid-size enterprises "
            "reduce endpoint vulnerabilities by up to 60%. I noticed your company might benefit "
            "from our managed detection and response platform. Would you have 15 minutes this week "
            "for a quick demo? We're offering a complimentary security assessment for new customers "
            "through the end of the quarter.",
            "Hello, my name is Jordan from CloudWatch Pro. I wanted to connect with someone on your "
            "IT team about our cloud infrastructure monitoring tool. We work with several companies "
            "in your industry and have helped them cut downtime by 40%. I'd love to schedule a "
            "brief call to discuss how we can help your organization. No commitment — just a "
            "friendly conversation!",
        ],
        next_best_actions=[
            "Close — this is a vendor sales pitch, not an IT support request.",
        ],
        remediation_steps=[
            [
                "No action required — unsolicited vendor sales outreach, close ticket",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# ns-030  Employee sharing meeting notes — wrong recipient
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="ns-030",
        category=Category.NOT_SUPPORT,
        priority=Priority.P4,
        assigned_team=Team.NONE,
        needs_escalation=False,
        missing_information=[],
        subjects=[
            "Meeting notes from today's product sync",
            "FW: Action items — Q4 planning session",
            "Notes & follow-ups from the Wednesday standup",
        ],
        descriptions=[
            "Hey team, here are the notes from today's product sync meeting. Key decisions: we're "
            "pushing the launch to January 15th, the design team will deliver final mockups by "
            "Friday, and we need to schedule a follow-up with the sales team about pricing tiers. "
            "Action items are listed below. Let me know if I missed anything. — Sam",
            "Forwarding the action items from this morning's Q4 planning session. Highlights: "
            "budget for the new hire has been approved, we agreed to consolidate the two vendor "
            "contracts into one, and the marketing launch date is tentatively set for February. "
            "Please review and add any corrections. Next meeting is Thursday at 2pm in Room 301.",
        ],
        next_best_actions=[
            "Close — these are meeting notes sent to the wrong recipient, not a support request.",
        ],
        remediation_steps=[
            [
                "No action required — meeting notes sent to wrong address, close ticket",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# ns-031  Personal home printer setup request (boundary: looks like hardware)
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="ns-031",
        category=Category.NOT_SUPPORT,
        priority=Priority.P4,
        assigned_team=Team.NONE,
        needs_escalation=False,
        missing_information=[],
        subjects=[
            "Need help setting up my home printer",
            "Can IT help me configure my personal printer at home?",
            "Home printer won't connect — can you help?",
        ],
        descriptions=[
            "Hey IT, I just bought a new wireless printer for my home office and I can't get it to "
            "connect to my personal WiFi network. It's a Brother HL-L2350DW — I'm trying to print "
            "from my personal laptop, not my work machine. Could someone walk me through the setup? "
            "I've tried following the manual but the wireless setup wizard keeps failing.",
            "Hi, I'm having trouble setting up my personal printer at home. It's not a company-issued "
            "device — I bought it myself for my kids' school projects. The printer won't pair with my "
            "home network and I figured the IT team might know how to fix it. Is this something you "
            "can help with? I can share the model number if needed.",
        ],
        next_best_actions=[
            "Close — personal equipment setup is outside the scope of corporate IT support.",
        ],
        remediation_steps=[
            [
                "No action required — personal device, not company equipment; close ticket",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# ns-032  Forwarded phishing simulation test email (boundary: looks like security)
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="ns-032",
        category=Category.NOT_SUPPORT,
        priority=Priority.P4,
        assigned_team=Team.NONE,
        needs_escalation=False,
        missing_information=[],
        subjects=[
            "Suspicious email — possible phishing attempt",
            "FW: Urgent — verify your credentials immediately",
            "I think I received a phishing email",
        ],
        descriptions=[
            "Hi, I just received a really suspicious email asking me to verify my Office 365 "
            "credentials through an external link. I didn't click anything but I wanted to report it. "
            "Subject line was 'Action Required: Verify Your Account.' I've attached a screenshot. "
            "It looks almost identical to a real Microsoft email. Could you investigate?"
            "\n\n[Note: This email matches the company's scheduled security awareness phishing "
            "simulation campaign sent by the InfoSec training team.]",
            "Team, I got an email that looks like a phishing attempt — it's asking me to reset my "
            "password through a link that doesn't match our company domain. I forwarded it here so "
            "you can take a look. The sender address looked off and the urgency felt suspicious. "
            "Wanted to flag it just in case."
            "\n\n[Note: This is the company's internal phishing simulation exercise run by the "
            "security training programme.]",
        ],
        next_best_actions=[
            "Close — the reported email is part of the company's scheduled phishing simulation "
            "campaign, not an actual threat.",
        ],
        remediation_steps=[
            [
                "No action required — email is a company phishing simulation test, close ticket",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# ns-033  Office coffee machine display fix (boundary: looks like hardware)
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="ns-033",
        category=Category.NOT_SUPPORT,
        priority=Priority.P4,
        assigned_team=Team.NONE,
        needs_escalation=False,
        missing_information=[],
        subjects=[
            "Coffee machine screen is broken — can IT fix it?",
            "Kitchen coffee machine display not working",
        ],
        descriptions=[
            "Hey, the coffee machine in the 3rd floor kitchen has a digital display that's been "
            "flickering and now shows nothing at all. Since it's a 'tech' issue I figured IT might "
            "handle it. Nobody can select drink options anymore and we're all stuck with whatever "
            "the default brew is. Can someone take a look?",
            "Hi team, the touchscreen on the break room coffee machine stopped responding this "
            "morning — it's completely frozen on the menu screen. A few of us have tried restarting "
            "it but no luck. Since it's a digital display issue, I thought IT could help. Could you "
            "send someone to fix it or at least take a look?",
        ],
        next_best_actions=[
            "Close — kitchen appliance maintenance is a facilities issue, not IT.",
        ],
        remediation_steps=[
            [
                "No action required — not IT equipment; redirect to facilities management and close ticket",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# ns-034  Recruiter asking IT to post a job listing (boundary: looks like web request)
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="ns-034",
        category=Category.NOT_SUPPORT,
        priority=Priority.P4,
        assigned_team=Team.NONE,
        needs_escalation=False,
        missing_information=[],
        subjects=[
            "Please post a job listing on the careers page",
            "New job opening — need it added to the website",
            "Can IT update the careers page with a new role?",
        ],
        descriptions=[
            "Hi IT, we just got approval for a new Senior Software Engineer position and I need it "
            "posted on the company careers page ASAP. I've attached the job description in a Word "
            "doc. Can you add it to the site? We'd also like it to show up on the internal jobs "
            "board. Let me know if you need anything else from my end.",
            "Hello, the hiring manager approved a new Product Manager opening and I'd like to get "
            "it up on our website's careers section by end of week. I have the job description "
            "ready to go. Is this something the IT team handles? If so, who should I send the "
            "details to? Thanks!",
        ],
        next_best_actions=[
            "Close — job postings are managed by HR or the marketing/communications team, not IT.",
        ],
        remediation_steps=[
            [
                "No action required — redirect to HR or marketing for job postings; close ticket",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# ns-035  Office thermostat / temperature complaint (boundary: looks like building systems)
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="ns-035",
        category=Category.NOT_SUPPORT,
        priority=Priority.P4,
        assigned_team=Team.NONE,
        needs_escalation=False,
        missing_information=[],
        subjects=[
            "Office is freezing — can IT adjust the thermostat?",
            "Temperature issue on the 4th floor — thermostat help",
            "Please fix the AC — it's way too cold in here",
        ],
        descriptions=[
            "Hi, the temperature on the 4th floor has been really cold all week — I think the "
            "thermostat is set way too low. A few of us have tried pressing the buttons on the "
            "wall unit but it doesn't respond. Since the thermostat has a digital panel, I "
            "figured IT might be the right team. Can someone come adjust it or unlock the "
            "controls? It's affecting productivity.",
            "Hello, I'm sitting near the server room on the 2nd floor and the AC has been blasting "
            "non-stop. My desk area feels like it's about 60 degrees. I wasn't sure if this falls "
            "under IT since the HVAC system might be connected to the building management software. "
            "Could you either turn it down or let me know who to contact? Thanks.",
        ],
        next_best_actions=[
            "Close — HVAC and thermostat issues are handled by facilities management, not IT.",
        ],
        remediation_steps=[
            [
                "No action required — temperature control is a facilities concern; close ticket",
            ],
        ],
    )
)
