"""Not a Support Ticket scenario definitions."""

from __future__ import annotations

from generator.models import Scenario

SCENARIOS: list[Scenario] = [
    Scenario(
        scenario_id="nat-out-of-office-reply",
        category="Not a Support Ticket",
        priority="P4",
        assigned_team="Endpoint Engineering",
        needs_escalation=False,
        missing_information=[],
        subjects=[
            "Out of Office: Re: Your IT Request",
            "Automatic reply: Ticket #40291 Update",
            "OOO: Re: Scheduled Maintenance Window",
            "Out of Office Re: Password Reset Confirmation",
        ],
        descriptions=[
            "Thank you for your message. I am currently out of the office from October 14–18 with limited access to email. For urgent matters, please contact my colleague Sarah Chen (s.chen@company.com). I will respond to your email upon my return. Best regards, David.",
            "I am out of the office until Monday, November 4th and will have no access to email. If this is urgent, please reach out to my manager, Tom Briggs, at x4512. Otherwise, I'll reply when I'm back. Thanks!",
            "Hi, I'm OOO on PTO this week (Oct 21–25). For anything time-sensitive, please contact the IT help desk directly at helpdesk@company.com. I'll get back to you when I return.",
        ],
        next_best_actions=[
            "Close ticket — this is an automated out-of-office reply, not a support request.",
        ],
        remediation_steps=[
            [
                "Identify this as an auto-generated out-of-office reply",
                "Close the ticket with no action required",
                "If this was a reply to an existing ticket, note the contact's absence on the original ticket",
            ],
        ],
        tags=["auto-reply", "not-actionable"],
        channel_weights={"email": 0.90, "chat": 0.05, "portal": 0.00, "phone": 0.05},
    ),
    Scenario(
        scenario_id="nat-thank-you-message",
        category="Not a Support Ticket",
        priority="P4",
        assigned_team="Endpoint Engineering",
        needs_escalation=False,
        missing_information=[],
        subjects=[
            "Re: Ticket #38291 — Thanks!",
            "Thank you!",
            "Re: Your laptop is ready for pickup",
            "Got it, thanks so much!",
        ],
        descriptions=[
            "Thanks!",
            "Got it, that fixed the issue. Thank you so much for your help!",
            "Perfect, everything is working now. Really appreciate the quick turnaround!",
            "Thanks team, all sorted on my end. You can close this out.",
        ],
        next_best_actions=[
            "Close ticket — this is a thank-you message with no further action needed.",
        ],
        remediation_steps=[
            [
                "Acknowledge the positive feedback",
                "Close the ticket as resolved",
            ],
        ],
        tags=["thank-you", "not-actionable"],
        channel_weights={"email": 0.40, "chat": 0.45, "portal": 0.10, "phone": 0.05},
    ),
    Scenario(
        scenario_id="nat-calendar-invite-mistake",
        category="Not a Support Ticket",
        priority="P4",
        assigned_team="Endpoint Engineering",
        needs_escalation=False,
        missing_information=[],
        subjects=[
            "Fwd: Team Standup — 10:00 AM Daily",
            "Invitation: Q4 Planning Meeting",
            "Fwd: Lunch & Learn: Cloud Migration Best Practices",
            "Updated: Weekly 1:1 with Manager",
        ],
        descriptions=[
            "--- Forwarded meeting invitation ---\nTeam Standup\nWhen: Daily, 10:00 AM – 10:15 AM EST\nWhere: Microsoft Teams\nOrganizer: Priya Sharma\n\nHi all, joining link below. See you there!",
            "You have been invited to the following event:\nQ4 Planning Meeting\nDate: November 5, 2024 2:00 PM – 4:00 PM\nLocation: Conference Room 3B\nOrganizer: James Wilson\n\nPlease confirm your attendance.",
            "--- Forwarded calendar event ---\nLunch & Learn: Cloud Migration Best Practices\nThursday 12:00 PM — Room 201\nBring your lunch! Pizza provided.\n\n(Accidentally forwarded to IT helpdesk, sorry!)",
        ],
        next_best_actions=[
            "Close ticket — this is a calendar invitation forwarded in error, not a support request.",
        ],
        remediation_steps=[
            [
                "Identify this as a misdirected calendar invitation",
                "Close the ticket with no action required",
                "Optionally notify the sender that it was sent to the help desk in error",
            ],
        ],
        tags=["misdirected", "not-actionable"],
        channel_weights={"email": 0.85, "chat": 0.10, "portal": 0.00, "phone": 0.05},
    ),
    Scenario(
        scenario_id="nat-newsletter-marketing",
        category="Not a Support Ticket",
        priority="P4",
        assigned_team="Endpoint Engineering",
        needs_escalation=False,
        missing_information=[],
        subjects=[
            "Fwd: TechInsider Weekly: Top 10 Cloud Trends for 2025",
            "FW: Your Monthly Microsoft 365 Tips & Tricks",
            "Fwd: [Webinar] Securing Your Hybrid Workforce",
            "FW: AWS re:Invent Early Bird Registration",
        ],
        descriptions=[
            "---------- Forwarded message ----------\nTechInsider Weekly Newsletter\n\n🔥 Top 10 Cloud Trends for 2025\n☁️ Is Serverless Really the Future?\n🔒 Zero Trust: Hype or Reality?\n\nRead more at techinsider.com\nUnsubscribe | Manage preferences",
            "Your Monthly Microsoft 365 Tips!\n\n✅ 5 Teams features you're not using\n✅ How to master Excel pivot tables\n✅ Copilot tips for Outlook\n\nForward to a colleague who needs this!\n\n© 2024 Microsoft Corporation. Unsubscribe here.",
            "You're invited!\n\nJoin our free webinar: Securing Your Hybrid Workforce in 2025\nDate: November 12, 2024 | 1:00 PM ET\nSpeaker: Jane Smith, CISO @ CloudSecure Inc.\n\nRegister now → [link]\n\nYou're receiving this because you attended our previous webinar.",
        ],
        next_best_actions=[
            "Close ticket — this is a forwarded newsletter or marketing email, not a support request.",
        ],
        remediation_steps=[
            [
                "Identify this as a forwarded newsletter or marketing content",
                "Close the ticket with no action required",
            ],
        ],
        tags=["newsletter", "marketing", "not-actionable"],
        channel_weights={"email": 0.95, "chat": 0.02, "portal": 0.00, "phone": 0.03},
    ),
    Scenario(
        scenario_id="nat-company-announcement",
        category="Not a Support Ticket",
        priority="P4",
        assigned_team="Endpoint Engineering",
        needs_escalation=False,
        missing_information=[],
        subjects=[
            "Fwd: All-Hands Meeting This Friday",
            "FW: Company Holiday Schedule 2025",
            "Fwd: New CEO Announcement",
            "FW: Office Closure — Thanksgiving Week",
        ],
        descriptions=[
            "---------- Forwarded message ----------\nFrom: Internal Communications <comms@company.com>\nSubject: All-Hands Meeting This Friday\n\nHi everyone,\n\nPlease join us for the quarterly all-hands this Friday at 3 PM in the main auditorium (or via Teams for remote staff). CEO will be sharing Q3 results and our 2025 roadmap.\n\nSee you there!",
            "FW: Important update from HR\n\nPlease note the updated holiday schedule for 2025 has been posted on the intranet. Key dates: offices closed Dec 23 – Jan 1. Please plan accordingly.\n\nHR Team",
            "Forwarding this in case IT needs to know — new CEO starts January 6. Details in the attached press release.\n\n(Note: this was forwarded to IT helpdesk by an employee who thought IT needed to be informed.)",
        ],
        next_best_actions=[
            "Close ticket — this is a forwarded internal company announcement, not a support request.",
        ],
        remediation_steps=[
            [
                "Identify this as a forwarded internal announcement",
                "Close the ticket with no action required",
                "If the announcement has IT implications (e.g., office closure), note it for the relevant team internally",
            ],
        ],
        tags=["announcement", "misdirected", "not-actionable"],
        channel_weights={"email": 0.85, "chat": 0.10, "portal": 0.00, "phone": 0.05},
    ),
    Scenario(
        scenario_id="nat-test-message",
        category="Not a Support Ticket",
        priority="P4",
        assigned_team="Endpoint Engineering",
        needs_escalation=False,
        missing_information=[],
        subjects=[
            "test",
            "Testing 123",
            "Test ticket — please ignore",
            "ignore this — testing portal",
        ],
        descriptions=[
            "testing 123",
            "This is a test ticket. Please ignore.",
            "test",
            "Just checking if the portal submission works. Please disregard this ticket.",
        ],
        next_best_actions=[
            "Close ticket — this is a test message, not a real support request.",
        ],
        remediation_steps=[
            [
                "Identify this as a test submission",
                "Close the ticket with no action required",
            ],
        ],
        tags=["test", "not-actionable"],
        channel_weights={"email": 0.20, "chat": 0.30, "portal": 0.45, "phone": 0.05},
    ),
    Scenario(
        scenario_id="nat-nevermind-self-resolved",
        category="Not a Support Ticket",
        priority="P4",
        assigned_team="Endpoint Engineering",
        needs_escalation=False,
        missing_information=[],
        subjects=[
            "Never mind — fixed it myself",
            "Please disregard my previous ticket",
            "Issue resolved on my own",
            "Cancel my request — all good now",
        ],
        descriptions=[
            "Hey, never mind about my earlier ticket — I figured it out. Just needed to restart the app. Thanks anyway!",
            "Hi, please disregard the ticket I just submitted about Outlook crashing. I found a workaround by clearing the cache. You can close this out.",
            "Ignore my last message. Turns out I just needed to update the browser. All working now. Sorry for the noise!",
            "You can close my ticket — the issue resolved itself after I rebooted. Appreciate the quick response though!",
        ],
        next_best_actions=[
            "Close ticket — the user has self-resolved the issue and no further action is needed.",
        ],
        remediation_steps=[
            [
                "Acknowledge the user's self-resolution",
                "Close the ticket as resolved by the reporter",
                "If a related open ticket exists, close or link it",
            ],
        ],
        tags=["self-resolved", "not-actionable"],
        channel_weights={"email": 0.30, "chat": 0.45, "portal": 0.15, "phone": 0.10},
    ),
    Scenario(
        scenario_id="nat-vendor-sales-pitch",
        category="Not a Support Ticket",
        priority="P4",
        assigned_team="Endpoint Engineering",
        needs_escalation=False,
        missing_information=[],
        subjects=[
            "Revolutionize Your IT Operations with AIOps",
            "Exclusive offer: 50% off enterprise security suite",
            "Following up — can we schedule a demo?",
            "Partnering on your digital transformation journey",
        ],
        descriptions=[
            "Hi IT Team,\n\nI'm reaching out from CloudOps Solutions. We help companies like yours reduce IT incidents by 60% using our AI-powered operations platform. I'd love to schedule a 15-minute demo to show you how we can help.\n\nAre you available this Thursday or Friday?\n\nBest,\nMike Johnson\nAccount Executive, CloudOps Solutions\nmike.johnson@cloudops.io",
            "Dear IT Director,\n\nFor a limited time, we're offering 50% off our Enterprise Security Suite — trusted by 500+ Fortune 1000 companies. Our platform includes SIEM, SOAR, and endpoint protection in a single pane of glass.\n\nLet's connect! Reply to this email or book time directly: calendly.com/vendor-rep\n\nRegards,\nSarah Williams\nSenior Sales Engineer, SecureVault Inc.",
            "Hi,\n\nI'm following up on the email I sent last week about our IT asset management platform. I know you're busy, so I'll keep this short — we can save your team 20 hours/week on asset tracking.\n\nWould a quick 10-minute call work for you?\n\nThanks,\nChris Park\nBDR, AssetTrack Pro",
        ],
        next_best_actions=[
            "Close ticket — this is an unsolicited vendor sales pitch, not a support request.",
        ],
        remediation_steps=[
            [
                "Identify this as a vendor sales or marketing outreach",
                "Close the ticket with no action required",
                "Optionally forward to IT procurement if the product is relevant to current initiatives",
            ],
        ],
        tags=["vendor", "sales", "not-actionable"],
        channel_weights={"email": 0.90, "chat": 0.05, "portal": 0.00, "phone": 0.05},
    ),
    Scenario(
        scenario_id="nat-personal-non-it-request",
        category="Not a Support Ticket",
        priority="P4",
        assigned_team="Endpoint Engineering",
        needs_escalation=False,
        missing_information=[],
        subjects=[
            "Coffee machine on 3rd floor is broken",
            "AC is way too cold in our area",
            "Kitchen microwave not working",
            "Parking lot light is out near entrance B",
        ],
        descriptions=[
            "Hi, the coffee machine on the 3rd floor near the kitchen has been broken since Monday. It just makes a grinding noise and nothing comes out. Can someone get it fixed? We're all suffering over here lol.",
            "The air conditioning in section 4B is absolutely freezing. Multiple people on my team are wearing jackets at their desks. Can IT adjust the thermostat? We've complained to facilities but nothing has changed.",
            "The microwave in the 2nd floor break room is sparking when you turn it on. Pretty sure that's a fire hazard. Not sure if this is an IT thing but I didn't know who else to email.",
            "The light in parking lot B near the side entrance has been out for a week. It's really dark at night and feels unsafe. Can someone put in a maintenance request?",
        ],
        next_best_actions=[
            "Close ticket — this is a facilities/personal request, not an IT support issue. Redirect to Facilities.",
        ],
        remediation_steps=[
            [
                "Identify this as a non-IT facilities or personal request",
                "Redirect the user to the Facilities or Office Management team",
                "Close the ticket as out of scope for IT support",
            ],
        ],
        tags=["facilities", "misdirected", "not-actionable"],
        channel_weights={"email": 0.35, "chat": 0.35, "portal": 0.20, "phone": 0.10},
    ),
    Scenario(
        scenario_id="nat-empty-blank-ticket",
        category="Not a Support Ticket",
        priority="P4",
        assigned_team="Endpoint Engineering",
        needs_escalation=False,
        missing_information=[],
        subjects=[
            "(no subject)",
            "",
            ".",
            "Untitled",
        ],
        descriptions=[
            "",
            ".",
            " ",
            "...",
        ],
        next_best_actions=[
            "Close ticket — this is an empty or blank submission with no actionable content.",
        ],
        remediation_steps=[
            [
                "Identify this as an empty or accidental submission",
                "Attempt to contact the reporter to confirm if they intended to submit a ticket",
                "Close the ticket if no response is received within 24 hours",
            ],
        ],
        tags=["empty", "not-actionable"],
        channel_weights={"email": 0.30, "chat": 0.15, "portal": 0.50, "phone": 0.05},
    ),
    Scenario(
        scenario_id="nat-spam-lottery-scam",
        category="Not a Support Ticket",
        priority="P4",
        assigned_team="Security Operations",
        needs_escalation=False,
        missing_information=[],
        subjects=[
            "CONGRATULATIONS! You've Won $1,000,000!!!",
            "URGENT: Verify Your Account Immediately",
            "You have an unclaimed inheritance — ACT NOW",
            "Your PayPal account has been limited — click here",
        ],
        descriptions=[
            "CONGRATULATIONS!!! You have been selected as the winner of our 2024 Global Email Lottery! You have won $1,000,000.00 USD! To claim your prize, please send your full name, address, phone number, and bank account details to claims@lottery-intl-winners.com. Act now — this offer expires in 48 hours!",
            "Dear Valued Customer,\n\nWe have detected unusual activity on your account. Your access will be suspended unless you verify your identity within 24 hours.\n\nClick here to verify: http://totally-not-a-scam.xyz/verify\n\nMicrosoft Security Team",
            "ATTENTION: You have an unclaimed inheritance of £2,500,000 from a distant relative. Our law firm has been trying to reach you. Please reply with your full name and contact details so we can begin the transfer process.\n\nBarrister James Okafor\nOkafor & Associates Legal",
        ],
        next_best_actions=[
            "Close ticket — this is spam or a phishing/scam email. Flag for security team awareness if needed.",
        ],
        remediation_steps=[
            [
                "Identify this as spam, phishing, or a scam message",
                "Close the ticket immediately",
                "If the spam reached an employee's inbox, report it to the Security Operations team for investigation",
                "Consider adding the sender domain to the email block list",
            ],
        ],
        tags=["spam", "phishing", "security", "not-actionable"],
        channel_weights={"email": 0.95, "chat": 0.02, "portal": 0.00, "phone": 0.03},
    ),
    Scenario(
        scenario_id="nat-survey-response",
        category="Not a Support Ticket",
        priority="P4",
        assigned_team="Endpoint Engineering",
        needs_escalation=False,
        missing_information=[],
        subjects=[
            "Re: IT Satisfaction Survey",
            "Survey Response: How was your IT experience?",
            "Feedback: Recent support interaction",
            "Re: Rate your IT support experience",
        ],
        descriptions=[
            "Rating: 4/5\nComments: The tech who helped me was great and resolved my issue quickly. Only reason it's not a 5 is because the initial wait time was about 20 minutes.\n\n(This was submitted via the post-ticket satisfaction survey.)",
            "How would you rate your experience? ★★★★★\nWas your issue resolved? Yes\nAdditional comments: Everything was perfect. John on the help desk was very patient and knowledgeable. Thanks!",
            "Survey response:\n- Ease of reaching IT: 3/5\n- Speed of resolution: 4/5\n- Professionalism: 5/5\n- Overall satisfaction: 4/5\n- Comments: Wish there were more self-service options, but the staff is excellent.",
        ],
        next_best_actions=[
            "Close ticket — this is a survey response, not a support request. Route to IT management for review.",
        ],
        remediation_steps=[
            [
                "Identify this as a survey response or feedback submission",
                "Route the feedback to the IT service management team for review",
                "Close the ticket with no technical action required",
            ],
        ],
        tags=["survey", "feedback", "not-actionable"],
        channel_weights={"email": 0.70, "chat": 0.10, "portal": 0.15, "phone": 0.05},
    ),
    Scenario(
        scenario_id="nat-fyi-informational",
        category="Not a Support Ticket",
        priority="P4",
        assigned_team="Endpoint Engineering",
        needs_escalation=False,
        missing_information=[],
        subjects=[
            "FYI: New building Wi-Fi passwords posted",
            "Heads up — office layout changes next week",
            "FYI: Team moving to new floor",
            "Just an FYI — no action needed",
        ],
        descriptions=[
            "Hi IT, just a heads up that the new Wi-Fi passwords for the guest network have been posted on the bulletin board in the lobby. No action needed from your side, just wanted to keep you in the loop.",
            "FYI — our team is moving to the 4th floor next Tuesday. Facilities is handling the furniture and I've already coordinated with Network Ops on the phone/data ports. Just wanted IT help desk to be aware in case anyone from my team calls in confused. No action needed.",
            "Hey, just letting you know that the marketing team wrapped up the software migration over the weekend. Everything seems to be working fine so far. No issues to report — just keeping you informed.",
        ],
        next_best_actions=[
            "Close ticket — this is an informational FYI message with no action required.",
        ],
        remediation_steps=[
            [
                "Acknowledge the informational message",
                "Close the ticket as no action is required",
                "Note any relevant information for internal awareness if applicable",
            ],
        ],
        tags=["fyi", "informational", "not-actionable"],
        channel_weights={"email": 0.60, "chat": 0.25, "portal": 0.05, "phone": 0.10},
    ),
    Scenario(
        scenario_id="nat-wrong-dept-hr",
        category="Not a Support Ticket",
        priority="P4",
        assigned_team="Endpoint Engineering",
        needs_escalation=False,
        missing_information=[],
        subjects=[
            "Question about my PTO balance",
            "Need to update my direct deposit information",
            "Benefits enrollment deadline question",
            "How do I submit a time-off request?",
        ],
        descriptions=[
            "Hi, I'm trying to figure out how many PTO days I have left for the year. The HR portal is showing a different number than what I calculated. Can someone check for me? My employee ID is 10482.",
            "I need to update my direct deposit information — I switched banks last month. I'm not sure if I do this through Workday or if I need to contact someone. Can you help?",
            "When is the deadline for open enrollment this year? I want to switch my health plan but I can't find the dates anywhere on the intranet. Also, is there a way to compare plans side by side?",
            "How do I submit a time-off request in the system? I just joined the company and my manager said to put it in the portal but I can't find where to do it.",
        ],
        next_best_actions=[
            "Close ticket — this is an HR question, not an IT support request. Redirect the user to HR.",
        ],
        remediation_steps=[
            [
                "Identify this as an HR-related request, not an IT issue",
                "Redirect the user to the HR department or HR portal",
                "Provide the HR contact email or phone number for convenience",
                "Close the ticket as out of scope for IT support",
            ],
        ],
        tags=["misdirected", "hr", "not-actionable"],
        channel_weights={"email": 0.35, "chat": 0.35, "portal": 0.20, "phone": 0.10},
    ),
    Scenario(
        scenario_id="nat-wrong-dept-facilities",
        category="Not a Support Ticket",
        priority="P4",
        assigned_team="Endpoint Engineering",
        needs_escalation=False,
        missing_information=[],
        subjects=[
            "Need a new desk chair — mine is broken",
            "Requesting a standing desk",
            "Bathroom on 2nd floor is out of order",
            "Light flickering in conference room 3A",
        ],
        descriptions=[
            "Hi, the hydraulic cylinder on my desk chair is broken — it keeps slowly sinking down throughout the day. Can I get a replacement? I've been here for three years and this is the original chair.",
            "I'd like to request a standing desk or a sit-stand converter for my workstation. My doctor recommended it for my back. Is this something I request through IT or through another department?",
            "The men's bathroom on the 2nd floor has been out of order since yesterday morning. There's a sign on the door but no one seems to be fixing it. Can someone put in a work order?",
            "The overhead light in conference room 3A is flickering badly. It's giving people headaches during meetings. Can you send someone to fix it?",
        ],
        next_best_actions=[
            "Close ticket — this is a facilities request, not an IT support issue. Redirect to Facilities Management.",
        ],
        remediation_steps=[
            [
                "Identify this as a facilities-related request, not an IT issue",
                "Redirect the user to the Facilities Management team",
                "Provide the Facilities contact information or work order portal link",
                "Close the ticket as out of scope for IT support",
            ],
        ],
        tags=["misdirected", "facilities", "not-actionable"],
        channel_weights={"email": 0.30, "chat": 0.30, "portal": 0.25, "phone": 0.15},
    ),
    Scenario(
        scenario_id="nat-chain-letter-joke",
        category="Not a Support Ticket",
        priority="P4",
        assigned_team="Endpoint Engineering",
        needs_escalation=False,
        missing_information=[],
        subjects=[
            "Fwd: Fwd: Fwd: You HAVE to read this!!",
            "FW: FW: This is hilarious 😂",
            "Fwd: Send this to 10 people or else...",
            "FW: FW: FW: Best joke ever",
        ],
        descriptions=[
            "---------- Forwarded 47 times ----------\n\nSend this to 10 friends in the next hour and something amazing will happen to you at midnight!!! 🌟✨ If you break the chain, you'll have bad luck for 7 years!!! This has been going around since 1997 and it REALLY WORKS!!!\n\n>> >> >> Don't break the chain!!!",
            "LOLOL you guys have to read this 😂😂😂\n\nA sysadmin, a developer, and a project manager walk into a bar...\n\n(forwarded to the IT help desk distribution list by accident)",
            "FW: FW: FW: FW:\nIMPORTANT: Bill Gates is giving away $5,000 to everyone who forwards this email! Microsoft is testing a new email tracking system. I know it sounds fake but my cousin's friend actually got a check!!! Forward to everyone you know!!",
        ],
        next_best_actions=[
            "Close ticket — this is a chain letter or joke forwarded in error, not a support request.",
        ],
        remediation_steps=[
            [
                "Identify this as a chain letter, joke, or hoax forwarded to the help desk",
                "Close the ticket with no action required",
            ],
        ],
        tags=["chain-letter", "joke", "not-actionable"],
        channel_weights={"email": 0.90, "chat": 0.07, "portal": 0.00, "phone": 0.03},
    ),
    Scenario(
        scenario_id="nat-duplicate-colleague-ticket",
        category="Not a Support Ticket",
        priority="P4",
        assigned_team="Endpoint Engineering",
        needs_escalation=False,
        missing_information=[],
        subjects=[
            "Same issue as my colleague — ticket #41022",
            "Me too — same problem as the email outage ticket",
            "Ditto — same as Sarah's printer issue",
            "+1 to ticket #40987 — experiencing the same thing",
        ],
        descriptions=[
            "Hi, I'm having the exact same issue as my colleague reported in ticket #41022. Outlook keeps crashing when opening attachments. Can you just add me to that ticket instead of creating a new one?",
            "Same here — I'm also experiencing the email sync delay that was reported earlier today. I think there's already an open ticket for this. Just wanted IT to know it's affecting me too. My employee ID is 20394.",
            "Ditto to what Sarah reported about the printer on floor 2. It's not working for me either. I assume this is a known issue? Please add me to the existing ticket. Thanks!",
            "+1 — I have the same VPN disconnection issue as ticket #40987. Started this morning around 9 AM. Just wanted to be counted so you know it's widespread.",
        ],
        next_best_actions=[
            "Close ticket — this is a duplicate report. Add the user as an affected party to the existing ticket.",
        ],
        remediation_steps=[
            [
                "Identify the referenced original ticket",
                "Add this user as an affected party on the existing ticket",
                "Close this ticket as a duplicate, linked to the original",
                "Notify the user that they've been added to the existing ticket for updates",
            ],
        ],
        tags=["duplicate", "not-actionable"],
    ),
    Scenario(
        scenario_id="nat-monitoring-alert-info",
        category="Not a Support Ticket",
        priority="P4",
        assigned_team="Endpoint Engineering",
        needs_escalation=False,
        missing_information=[],
        subjects=[
            "[INFO] Scheduled backup completed successfully",
            "[OK] Server health check passed — all systems nominal",
            "[RESOLVED] CPU alert cleared on WEBSRV-03",
            "[INFO] Certificate renewal completed for *.company.com",
        ],
        descriptions=[
            "[AUTOMATED ALERT — INFORMATIONAL]\nSystem: BKUP-PROD-01\nEvent: Nightly backup completed successfully\nTime: 2024-10-14 03:00:15 UTC\nDuration: 2h 14m\nStatus: SUCCESS\nObjects backed up: 1,247\nTotal size: 892 GB\n\nNo action required.",
            "[MONITORING — OK]\nHost: WEBSRV-03\nCheck: CPU Utilization\nStatus: OK (recovered)\nPrevious: WARNING (87%)\nCurrent: 34%\nTime: 2024-10-14 09:45:22 UTC\n\nThe previous CPU alert has auto-resolved. No action needed.",
            "[AUTOMATED — INFORMATIONAL]\nService: Certificate Manager\nAction: SSL certificate renewal\nDomain: *.company.com\nNew expiry: 2025-10-14\nStatus: SUCCESS\n\nThis is an automated notification. No action required.",
        ],
        next_best_actions=[
            "Close ticket — this is an informational monitoring alert with no action required.",
        ],
        remediation_steps=[
            [
                "Identify this as an auto-generated informational monitoring alert",
                "Verify the alert status is informational or resolved (not actionable)",
                "Close the ticket with no action required",
            ],
        ],
        tags=["monitoring", "automated", "not-actionable"],
        channel_weights={"email": 0.85, "chat": 0.05, "portal": 0.05, "phone": 0.05},
    ),
    Scenario(
        scenario_id="nat-conference-lunch-order",
        category="Not a Support Ticket",
        priority="P4",
        assigned_team="Endpoint Engineering",
        needs_escalation=False,
        missing_information=[],
        subjects=[
            "Fwd: Lunch order for Thursday's all-hands",
            "RE: Pizza or sandwiches for the team event?",
            "Fwd: Conference registration — need headcount",
            "FW: Team lunch choices — please respond by noon",
        ],
        descriptions=[
            "Hey, can everyone reply with their lunch choice for Thursday's all-hands meeting?\n\n1. Turkey club sandwich\n2. Veggie wrap\n3. Caesar salad\n4. Pepperoni pizza\n\nPlease respond by Wednesday noon so we can place the order. Thanks!\n\n(Accidentally sent to IT helpdesk)",
            "---------- Forwarded message ----------\nHi team, we're organizing the holiday lunch for December 20th. Please fill out the Google Form with your meal preference and any allergies: [link]\n\nRSVP by December 10th!\n\n(This was forwarded to IT help desk by mistake.)",
            "Quick poll — who's interested in attending the AWS Summit in Chicago next March? We have a limited number of free passes. Reply YES if you want to go and I'll add you to the registration list.\n\n(Sent to the wrong distribution list, apologies!)",
        ],
        next_best_actions=[
            "Close ticket — this is a social/administrative message sent to IT by mistake.",
        ],
        remediation_steps=[
            [
                "Identify this as a misdirected social or administrative message",
                "Close the ticket with no action required",
                "Optionally notify the sender that it was sent to the help desk in error",
            ],
        ],
        tags=["misdirected", "social", "not-actionable"],
        channel_weights={"email": 0.80, "chat": 0.15, "portal": 0.00, "phone": 0.05},
    ),
    Scenario(
        scenario_id="nat-please-ignore-followup",
        category="Not a Support Ticket",
        priority="P4",
        assigned_team="Endpoint Engineering",
        needs_escalation=False,
        missing_information=[],
        subjects=[
            "Please ignore my previous email",
            "Disregard — sent to wrong address",
            "RE: Oops, wrong recipient!",
            "Please delete — sent in error",
        ],
        descriptions=[
            "Hi, please ignore the email I just sent to this address — it was meant for a colleague. Sorry about that!",
            "Oops! That last message was supposed to go to my manager, not the IT help desk. Please disregard. Apologies for the confusion.",
            "Please delete my previous email — I accidentally sent confidential information to the wrong address. I meant to send it to my team's distribution list. Sorry for the mix-up!",
            "Wrong recipient — that was meant for someone else entirely. Please ignore and delete. Thank you!",
        ],
        next_best_actions=[
            "Close ticket — the user sent a message in error and is requesting it be disregarded.",
        ],
        remediation_steps=[
            [
                "Acknowledge the user's request to disregard the message",
                "Close the ticket with no action required",
                "If confidential information was disclosed, notify the Security Operations team",
            ],
        ],
        tags=["misdirected", "not-actionable"],
        channel_weights={"email": 0.80, "chat": 0.15, "portal": 0.00, "phone": 0.05},
    ),
]
