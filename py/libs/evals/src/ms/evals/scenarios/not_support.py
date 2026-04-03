"""Not a Support Ticket scenarios for the Contoso Financial Services eval suite."""

from ms.evals.constants import Category
from ms.evals.constants import Channel
from ms.evals.constants import MissingInfo
from ms.evals.constants import Priority
from ms.evals.constants import Team
from ms.evals.scenarios.base import ScenarioDefinition


def get_scenarios() -> list[ScenarioDefinition]:
    """Return all Not a Support Ticket evaluation scenarios."""
    return [
        # -------------------------------------------------------------------
        # 1. Out-of-office auto-reply (vacation)
        # -------------------------------------------------------------------
        ScenarioDefinition(
            scenario_id="NOSUP-001",
            subject="Out of Office: Re: Quarterly IT Asset Inventory Review",
            description=(
                "Thank you for your message. I am currently out of the office on vacation from March 14 "
                "through March 25 with limited access to email. For urgent matters, please contact my "
                "manager Lisa Fernandez at lisa.fernandez@contoso.com. I will respond to your message "
                "when I return.\n\n"
                "Best regards,\nTomoko Sato"
            ),
            category=Category.NOT_SUPPORT,
            priority=Priority.P4,
            team=Team.NONE,
            needs_escalation=False,
            missing_info=[],
            next_best_action="Close — auto-reply to a previous IT communication. No action required.",
            remediation_steps=[
                "No action required — this is an out-of-office auto-reply, close ticket.",
            ],
            reporter_name="Tomoko Sato",
            reporter_email="tomoko.sato@contoso.com",
            reporter_department="Wealth Management",
            channel=Channel.EMAIL,
            tags=["ooo", "auto-reply"],
            difficulty="easy",
        ),
        # -------------------------------------------------------------------
        # 2. Out-of-office auto-reply (parental leave — mentions IT issue)
        # -------------------------------------------------------------------
        ScenarioDefinition(
            scenario_id="NOSUP-002",
            subject="Automatic Reply: VPN Access Issue — Parental Leave",
            description=(
                "Hi,\n\n"
                "I am on parental leave until June 1, 2026 and will not be checking email. Before I left, "
                "I had an open ticket about VPN disconnects — please coordinate with Raj Patel "
                "(raj.patel@contoso.com) on my team if that still needs attention.\n\n"
                "Thanks,\nMarcus Williams"
            ),
            category=Category.NOT_SUPPORT,
            priority=Priority.P4,
            team=Team.NONE,
            needs_escalation=False,
            missing_info=[],
            next_best_action=(
                "Close — auto-reply from employee on parental leave. If the referenced VPN issue is still "
                "open, it will have its own ticket."
            ),
            remediation_steps=[
                "No action required — this is an auto-reply, close ticket.",
            ],
            reporter_name="Marcus Williams",
            reporter_email="marcus.williams@contoso.com",
            reporter_department="Commercial Lending",
            channel=Channel.EMAIL,
            tags=["ooo", "auto-reply", "parental-leave"],
            difficulty="medium",
        ),
        # -------------------------------------------------------------------
        # 3. Thank-you / appreciation message
        # -------------------------------------------------------------------
        ScenarioDefinition(
            scenario_id="NOSUP-003",
            subject="Thanks so much for the quick fix!",
            description=(
                "Hey IT team,\n\n"
                "Just wanted to say a huge thank you to whoever fixed the Outlook sync issue this morning. "
                "I was panicking because I had a client meeting at 10 and all my calendar invites were gone, "
                "but everything came back within 20 minutes of me submitting the ticket. You guys are "
                "rockstars! 🎸\n\n"
                "Cheers,\nAnika Desai"
            ),
            category=Category.NOT_SUPPORT,
            priority=Priority.P4,
            team=Team.NONE,
            needs_escalation=False,
            missing_info=[],
            next_best_action="Close — thank-you message with no new issue reported. No action required.",
            remediation_steps=[
                "No action required — this is a thank-you message referencing a resolved issue, close ticket.",
            ],
            reporter_name="Anika Desai",
            reporter_email="anika.desai@contoso.com",
            reporter_department="Private Banking",
            channel=Channel.EMAIL,
            tags=["thank-you", "appreciation"],
            difficulty="easy",
        ),
        # -------------------------------------------------------------------
        # 4. Misdirected vendor invoice
        # -------------------------------------------------------------------
        ScenarioDefinition(
            scenario_id="NOSUP-004",
            subject="Invoice #INV-2026-4491 — Contoso Facilities Q1 Cleaning Services",
            description=(
                "Please find attached Invoice #INV-2026-4491 for Q1 2026 janitorial and cleaning services "
                "for the Contoso Financial Services headquarters at 200 Park Avenue. Total amount due: "
                "$18,450.00. Payment terms: Net 30.\n\n"
                "If you have any questions, please contact our billing department at "
                "billing@sparkleclean.com.\n\n"
                "Regards,\nAccounts Receivable\nSparkleClean Commercial Services"
            ),
            category=Category.NOT_SUPPORT,
            priority=Priority.P4,
            team=Team.NONE,
            needs_escalation=False,
            missing_info=[],
            next_best_action="Close — misdirected vendor invoice. Forward to Accounts Payable if appropriate.",
            remediation_steps=[
                "No action required — forward to accounts-payable@contoso.com and close ticket.",
            ],
            reporter_name="SparkleClean Billing",
            reporter_email="billing@sparkleclean.com",
            reporter_department="External",
            channel=Channel.EMAIL,
            tags=["misdirected", "vendor", "invoice"],
            difficulty="easy",
        ),
        # -------------------------------------------------------------------
        # 5. HR benefits question misdirected to IT
        # -------------------------------------------------------------------
        ScenarioDefinition(
            scenario_id="NOSUP-005",
            subject="Question about dental coverage for dependents",
            description=(
                "Hi,\n\n"
                "I recently added my spouse to my benefits during open enrollment but the dental plan still "
                "shows only me as covered when I log into the benefits portal. Can someone check if my "
                "enrollment went through? My employee ID is 44892.\n\n"
                "Thanks,\nCarlos Mendes"
            ),
            category=Category.NOT_SUPPORT,
            priority=Priority.P4,
            team=Team.NONE,
            needs_escalation=False,
            missing_info=[],
            next_best_action="Close — HR benefits question sent to IT in error. Redirect to HR.",
            remediation_steps=[
                "No action required — redirect the sender to hr-benefits@contoso.com and close ticket.",
            ],
            reporter_name="Carlos Mendes",
            reporter_email="carlos.mendes@contoso.com",
            reporter_department="Risk Management",
            channel=Channel.PORTAL,
            tags=["misdirected", "hr", "benefits"],
            difficulty="medium",
        ),
        # -------------------------------------------------------------------
        # 6. Spam / marketing email forwarded to IT
        # -------------------------------------------------------------------
        ScenarioDefinition(
            scenario_id="NOSUP-006",
            subject="FW: 🔥 LIMITED TIME: 90% Off Cloud Migration — Act Now!",
            description=(
                "---------- Forwarded message ----------\n"
                "From: deals@cloudmigrationnow.biz\n"
                "Subject: 🔥 LIMITED TIME: 90% Off Cloud Migration — Act Now!\n\n"
                "Dear IT Decision Maker,\n\n"
                "Struggling with your cloud migration? We can move your ENTIRE infrastructure to the cloud "
                "in just 48 hours for 90% off our regular price! This offer expires TONIGHT!\n\n"
                "Click here to claim your discount: [link removed]\n\n"
                "---\n"
                "Hey IT, is this legit? Got this in my inbox today. — Jamie"
            ),
            category=Category.NOT_SUPPORT,
            priority=Priority.P4,
            team=Team.NONE,
            needs_escalation=False,
            missing_info=[],
            next_best_action="Close — forwarded spam/marketing email. No action required.",
            remediation_steps=[
                "No action required — advise the user to delete the email and mark as spam, close ticket.",
            ],
            reporter_name="Jamie Okafor",
            reporter_email="jamie.okafor@contoso.com",
            reporter_department="Operations",
            channel=Channel.EMAIL,
            tags=["spam", "marketing", "forwarded"],
            difficulty="easy",
        ),
        # -------------------------------------------------------------------
        # 7. Calendar invite accidentally sent to IT helpdesk
        # -------------------------------------------------------------------
        ScenarioDefinition(
            scenario_id="NOSUP-007",
            subject="Accepted: Q2 Budget Planning — Conf Room 4B, Tue 2:00 PM",
            description=(
                "Jamie Chen has accepted the meeting invitation.\n\n"
                "Q2 Budget Planning\n"
                "When: Tuesday, March 24, 2026 2:00 PM – 3:30 PM (Eastern)\n"
                "Where: Conference Room 4B, 3rd Floor\n"
                "Organizer: VP Finance\n\n"
                "This is an automated calendar notification."
            ),
            category=Category.NOT_SUPPORT,
            priority=Priority.P4,
            team=Team.NONE,
            needs_escalation=False,
            missing_info=[],
            next_best_action="Close — calendar acceptance notification sent to IT in error. No action required.",
            remediation_steps=[
                "No action required — this is an automated calendar notification, close ticket.",
            ],
            reporter_name="Jamie Chen",
            reporter_email="jamie.chen@contoso.com",
            reporter_department="Finance",
            channel=Channel.EMAIL,
            tags=["calendar", "auto-notification", "misdirected"],
            difficulty="easy",
        ),
        # -------------------------------------------------------------------
        # 8. Newsletter auto-forward
        # -------------------------------------------------------------------
        ScenarioDefinition(
            scenario_id="NOSUP-008",
            subject="FW: Contoso Weekly — Employee Spotlight & March Madness Bracket",
            description=(
                "---------- Forwarded message ----------\n"
                "From: internal-comms@contoso.com\n"
                "Subject: Contoso Weekly — Employee Spotlight & March Madness Bracket\n\n"
                "Happy Monday, Contoso!\n\n"
                "This week's spotlight: Meet Priya Sharma from Compliance who just earned her CAMS "
                "certification! 🎉\n\n"
                "Also, don't forget to fill out your March Madness brackets by Wednesday. Prizes include "
                "a $50 gift card and bragging rights.\n\n"
                "— Internal Communications Team"
            ),
            category=Category.NOT_SUPPORT,
            priority=Priority.P4,
            team=Team.NONE,
            needs_escalation=False,
            missing_info=[],
            next_best_action="Close — internal newsletter auto-forwarded to IT. No action required.",
            remediation_steps=[
                "No action required — this is a forwarded company newsletter, close ticket.",
            ],
            reporter_name="Internal Comms",
            reporter_email="internal-comms@contoso.com",
            reporter_department="Corporate Communications",
            channel=Channel.EMAIL,
            tags=["newsletter", "auto-forward"],
            difficulty="easy",
        ),
        # -------------------------------------------------------------------
        # 9. Test ticket — user testing if system works
        # -------------------------------------------------------------------
        ScenarioDefinition(
            scenario_id="NOSUP-009",
            subject="TEST — please ignore",
            description=(
                "This is a test ticket. I just wanted to make sure the new ticketing portal was working "
                "correctly after the upgrade. Please disregard.\n\n"
                "— Sam"
            ),
            category=Category.NOT_SUPPORT,
            priority=Priority.P4,
            team=Team.NONE,
            needs_escalation=False,
            missing_info=[],
            next_best_action="Close — test ticket submitted to verify portal functionality. No action required.",
            remediation_steps=[
                "No action required — test submission to verify ticketing system, close ticket.",
            ],
            reporter_name="Sam Nakamura",
            reporter_email="sam.nakamura@contoso.com",
            reporter_department="Quality Assurance",
            channel=Channel.PORTAL,
            tags=["test", "ignore"],
            difficulty="easy",
        ),
        # -------------------------------------------------------------------
        # 10. Duplicate submission — same issue sent twice
        # -------------------------------------------------------------------
        ScenarioDefinition(
            scenario_id="NOSUP-010",
            subject="RE: Printer on 5th floor not working (duplicate — sorry!)",
            description=(
                "Hi, sorry about this — I already submitted a ticket about the 5th floor printer about "
                "10 minutes ago (I think the ticket number was INC-8820). The portal seemed like it froze "
                "so I submitted again. Please ignore this duplicate.\n\n"
                "Thanks,\nOliver Grant"
            ),
            category=Category.NOT_SUPPORT,
            priority=Priority.P4,
            team=Team.NONE,
            needs_escalation=False,
            missing_info=[],
            next_best_action="Close — user-confirmed duplicate of INC-8820. No action required.",
            remediation_steps=[
                "No action required — verify INC-8820 exists for the printer issue and close this duplicate.",
            ],
            reporter_name="Oliver Grant",
            reporter_email="oliver.grant@contoso.com",
            reporter_department="Compliance",
            channel=Channel.PORTAL,
            tags=["duplicate", "self-identified"],
            difficulty="easy",
        ),
        # -------------------------------------------------------------------
        # 11. Already-resolved follow-up — "never mind, fixed it"
        # -------------------------------------------------------------------
        ScenarioDefinition(
            scenario_id="NOSUP-011",
            subject="RE: Excel crashes when opening large spreadsheets — RESOLVED",
            description=(
                "Hey, you can close this one out. I cleared the Excel cache and disabled the Bloomberg "
                "add-in like someone suggested in the Teams channel and it's working fine now. Didn't "
                "even need to reinstall. Thanks anyway!\n\n"
                "— Priya"
            ),
            category=Category.NOT_SUPPORT,
            priority=Priority.P4,
            team=Team.NONE,
            needs_escalation=False,
            missing_info=[],
            next_best_action="Close — reporter confirmed the issue is self-resolved. No action required.",
            remediation_steps=[
                "No action required — user resolved the issue independently, close ticket.",
            ],
            reporter_name="Priya Kapoor",
            reporter_email="priya.kapoor@contoso.com",
            reporter_department="Equity Research",
            channel=Channel.EMAIL,
            tags=["self-resolved", "follow-up"],
            difficulty="easy",
        ),
        # -------------------------------------------------------------------
        # 12. Personal request — help with personal device
        # -------------------------------------------------------------------
        ScenarioDefinition(
            scenario_id="NOSUP-012",
            subject="Can you guys help me set up my home printer?",
            description=(
                "Hi IT,\n\n"
                "I know this isn't really a work thing but I just bought an HP LaserJet for my home "
                "office and I cannot for the life of me get it to connect to my home WiFi. The setup "
                "wizard keeps failing. Any chance one of you could walk me through it? I'd really "
                "appreciate it.\n\n"
                "Thanks,\nDaniel Kim"
            ),
            category=Category.NOT_SUPPORT,
            priority=Priority.P4,
            team=Team.NONE,
            needs_escalation=False,
            missing_info=[],
            next_best_action=(
                "Close — personal device support request outside IT scope. Politely decline and suggest "
                "manufacturer support."
            ),
            remediation_steps=[
                "No action required — advise the user to contact HP support for personal device assistance, "
                "close ticket.",
            ],
            reporter_name="Daniel Kim",
            reporter_email="daniel.kim@contoso.com",
            reporter_department="Treasury",
            channel=Channel.CHAT,
            tags=["personal-device", "out-of-scope"],
            difficulty="easy",
        ),
        # -------------------------------------------------------------------
        # 13. Internal company announcement
        # -------------------------------------------------------------------
        ScenarioDefinition(
            scenario_id="NOSUP-013",
            subject="FW: Annual Company Picnic — Save the Date: July 18!",
            description=(
                "---------- Forwarded message ----------\n"
                "From: events@contoso.com\n\n"
                "Mark your calendars! 🌭🎉\n\n"
                "The annual Contoso Financial Services company picnic is Saturday, July 18 at Riverside "
                "Park. Food, games, and live music! RSVP by June 30 at the link below. Families welcome.\n\n"
                "RSVP: [internal link]\n\n"
                "— Events Committee"
            ),
            category=Category.NOT_SUPPORT,
            priority=Priority.P4,
            team=Team.NONE,
            needs_escalation=False,
            missing_info=[],
            next_best_action="Close — company event announcement forwarded to IT. No action required.",
            remediation_steps=[
                "No action required — this is a company event announcement, close ticket.",
            ],
            reporter_name="Events Committee",
            reporter_email="events@contoso.com",
            reporter_department="Human Resources",
            channel=Channel.EMAIL,
            tags=["announcement", "company-event"],
            difficulty="easy",
        ),
        # -------------------------------------------------------------------
        # 14. Social / casual message
        # -------------------------------------------------------------------
        ScenarioDefinition(
            scenario_id="NOSUP-014",
            subject="Lunch today?",
            description=(
                "Hey does anyone on the IT team want to grab lunch at the new Thai place on 3rd? "
                "Heading out around 12:15. Let me know! 🍜"
            ),
            category=Category.NOT_SUPPORT,
            priority=Priority.P4,
            team=Team.NONE,
            needs_escalation=False,
            missing_info=[],
            next_best_action="Close — social lunch invitation, not a support request. No action required.",
            remediation_steps=[
                "No action required — casual social message, close ticket.",
            ],
            reporter_name="Brian Torres",
            reporter_email="brian.torres@contoso.com",
            reporter_department="IT Operations",
            channel=Channel.CHAT,
            tags=["social", "casual"],
            difficulty="easy",
        ),
        # -------------------------------------------------------------------
        # 15. Read receipt / delivery notification
        # -------------------------------------------------------------------
        ScenarioDefinition(
            scenario_id="NOSUP-015",
            subject="Read: Your password reset request has been processed",
            description=(
                "Your message\n\n"
                "  To: nathan.briggs@contoso.com\n"
                "  Subject: Your password reset request has been processed\n"
                "  Sent: Tuesday, March 17, 2026 4:22 PM\n\n"
                "was read on Tuesday, March 17, 2026 4:25 PM."
            ),
            category=Category.NOT_SUPPORT,
            priority=Priority.P4,
            team=Team.NONE,
            needs_escalation=False,
            missing_info=[],
            next_best_action="Close — automated read receipt, not a support request. No action required.",
            remediation_steps=[
                "No action required — this is an automated read receipt, close ticket.",
            ],
            reporter_name="Nathan Briggs",
            reporter_email="nathan.briggs@contoso.com",
            reporter_department="Retail Banking",
            channel=Channel.EMAIL,
            tags=["read-receipt", "auto-notification"],
            difficulty="easy",
        ),
        # -------------------------------------------------------------------
        # 16. Automated monitoring alert — informational only
        # -------------------------------------------------------------------
        ScenarioDefinition(
            scenario_id="NOSUP-016",
            subject="[INFO] Scheduled backup completed successfully — SQLPROD-03",
            description=(
                "AUTOMATED ALERT — INFORMATIONAL\n\n"
                "Server: SQLPROD-03\n"
                "Job: Nightly Full Backup\n"
                "Status: SUCCESS\n"
                "Start: 2026-03-17 02:00:00 UTC\n"
                "End: 2026-03-17 02:47:33 UTC\n"
                "Database: ContosoCoreDB\n"
                "Backup Size: 248.6 GB\n\n"
                "No action required. This is an informational notification."
            ),
            category=Category.NOT_SUPPORT,
            priority=Priority.P4,
            team=Team.NONE,
            needs_escalation=False,
            missing_info=[],
            next_best_action="Close — successful backup notification, informational only. No action required.",
            remediation_steps=[
                "No action required — routine informational monitoring alert with no errors, close ticket.",
            ],
            reporter_name="Monitoring System",
            reporter_email="monitoring@contoso.com",
            reporter_department="IT Operations",
            channel=Channel.EMAIL,
            tags=["monitoring", "informational", "automated"],
            difficulty="medium",
        ),
        # -------------------------------------------------------------------
        # 17. Survey / feedback request forwarded to IT
        # -------------------------------------------------------------------
        ScenarioDefinition(
            scenario_id="NOSUP-017",
            subject="FW: How was your experience with IT Support? Take our 2-min survey",
            description=(
                "---------- Forwarded message ----------\n"
                "From: feedback@contoso.com\n"
                "Subject: How was your experience with IT Support? Take our 2-min survey\n\n"
                "Hi Elena,\n\n"
                "Your recent IT ticket (INC-8734) was resolved on March 14. We'd love to hear how it "
                "went! Please take 2 minutes to complete this short survey:\n\n"
                "[Survey Link]\n\n"
                "Your feedback helps us improve our service.\n\n"
                "— IT Service Management\n\n"
                "---\n"
                "FYI, forwarding back to you guys in case you track these. I already filled it out. — Elena"
            ),
            category=Category.NOT_SUPPORT,
            priority=Priority.P4,
            team=Team.NONE,
            needs_escalation=False,
            missing_info=[],
            next_best_action="Close — forwarded satisfaction survey, no issue reported. No action required.",
            remediation_steps=[
                "No action required — user forwarded a completed satisfaction survey, close ticket.",
            ],
            reporter_name="Elena Vasquez",
            reporter_email="elena.vasquez@contoso.com",
            reporter_department="Client Services",
            channel=Channel.EMAIL,
            tags=["survey", "feedback", "forwarded"],
            difficulty="easy",
        ),
        # -------------------------------------------------------------------
        # 18. Joke / meme sent to IT
        # -------------------------------------------------------------------
        ScenarioDefinition(
            scenario_id="NOSUP-018",
            subject="Have you tried turning it off and on again? 😂",
            description=(
                "Saw this and thought of you guys lol\n\n"
                "[Image: A cartoon of a medieval knight asking a wizard for tech support. The wizard says "
                "'Have you tried turning the castle off and on again?']\n\n"
                "Happy Friday! — Mike"
            ),
            category=Category.NOT_SUPPORT,
            priority=Priority.P4,
            team=Team.NONE,
            needs_escalation=False,
            missing_info=[],
            next_best_action="Close — humorous message with no support request. No action required.",
            remediation_steps=[
                "No action required — this is a joke/meme with no support issue, close ticket.",
            ],
            reporter_name="Mike Patterson",
            reporter_email="mike.patterson@contoso.com",
            reporter_department="Trading Desk",
            channel=Channel.CHAT,
            tags=["joke", "social"],
            difficulty="easy",
        ),
        # -------------------------------------------------------------------
        # 19. Vendor sales pitch
        # -------------------------------------------------------------------
        ScenarioDefinition(
            scenario_id="NOSUP-019",
            subject="Revolutionize Your IT Operations with AI-Powered Automation",
            description=(
                "Dear Contoso IT Leadership,\n\n"
                "I'm reaching out because companies like Contoso Financial Services are seeing 40% "
                "reductions in ticket resolution time with our AI-powered IT automation platform. "
                "We recently helped a Fortune 500 bank automate over 10,000 monthly L1 tickets.\n\n"
                "Would you have 15 minutes this week for a quick demo? I promise it'll be worth your "
                "time.\n\n"
                "Best,\nJennifer Walsh\nSenior Account Executive\nAutomateIT Solutions\n"
                "jennifer.walsh@automateit.io"
            ),
            category=Category.NOT_SUPPORT,
            priority=Priority.P4,
            team=Team.NONE,
            needs_escalation=False,
            missing_info=[],
            next_best_action="Close — unsolicited vendor sales pitch. No action required.",
            remediation_steps=[
                "No action required — unsolicited vendor sales email, close ticket.",
            ],
            reporter_name="Jennifer Walsh",
            reporter_email="jennifer.walsh@automateit.io",
            reporter_department="External",
            channel=Channel.EMAIL,
            tags=["vendor", "sales-pitch", "unsolicited"],
            difficulty="easy",
        ),
        # -------------------------------------------------------------------
        # 20. Recruiter message forwarded to IT
        # -------------------------------------------------------------------
        ScenarioDefinition(
            scenario_id="NOSUP-020",
            subject="FW: Exciting Senior DevOps Role — Up to $220K + Equity",
            description=(
                "---------- Forwarded message ----------\n"
                "From: recruiter@toptalentsearch.com\n"
                "Subject: Exciting Senior DevOps Role — Up to $220K + Equity\n\n"
                "Hi,\n\n"
                "I came across your profile and think you'd be a great fit for a Senior DevOps Engineer "
                "role at a fast-growing fintech startup. Fully remote, great benefits, and equity.\n\n"
                "Interested? Let's chat!\n\n"
                "— Alex, TopTalent Search\n\n"
                "---\n"
                "Not sure how this got to the IT inbox. Forwarding so you can block the domain maybe? "
                "— Rachel"
            ),
            category=Category.NOT_SUPPORT,
            priority=Priority.P4,
            team=Team.NONE,
            needs_escalation=False,
            missing_info=[],
            next_best_action="Close — forwarded recruiter email, not actionable by IT. No action required.",
            remediation_steps=[
                "No action required — forwarded recruiter spam, no IT action needed, close ticket.",
            ],
            reporter_name="Rachel Goldstein",
            reporter_email="rachel.goldstein@contoso.com",
            reporter_department="Software Engineering",
            channel=Channel.EMAIL,
            tags=["recruiter", "forwarded", "misdirected"],
            difficulty="easy",
        ),
        # -------------------------------------------------------------------
        # 21. Chain email / superstition forward
        # -------------------------------------------------------------------
        ScenarioDefinition(
            scenario_id="NOSUP-021",
            subject="FW: FW: FW: Send this to 10 people or your computer will crash!!",
            description=(
                ">>> Forward this email to 10 friends within the next hour or your computer will get a "
                "virus!!! This is NOT a joke — Microsoft confirmed it!!! Bill Gates is tracking this "
                "email and will donate $1 for every forward!!!\n\n"
                "---\n"
                "LOL someone on the 4th floor actually sent this around. Just FYI. — Kevin"
            ),
            category=Category.NOT_SUPPORT,
            priority=Priority.P4,
            team=Team.NONE,
            needs_escalation=False,
            missing_info=[],
            next_best_action="Close — chain email/hoax forwarded to IT. No action required.",
            remediation_steps=[
                "No action required — chain email hoax, close ticket.",
            ],
            reporter_name="Kevin Archer",
            reporter_email="kevin.archer@contoso.com",
            reporter_department="Mortgage Services",
            channel=Channel.EMAIL,
            tags=["chain-email", "hoax", "forwarded"],
            difficulty="easy",
        ),
        # -------------------------------------------------------------------
        # 22. Accidental blank submission
        # -------------------------------------------------------------------
        ScenarioDefinition(
            scenario_id="NOSUP-022",
            subject="(no subject)",
            description="",
            category=Category.NOT_SUPPORT,
            priority=Priority.P4,
            team=Team.NONE,
            needs_escalation=False,
            missing_info=[],
            next_best_action="Close — blank/empty submission with no content. No action required.",
            remediation_steps=[
                "No action required — accidental blank submission, close ticket.",
            ],
            reporter_name="Unknown User",
            reporter_email="noreply@contoso.com",
            reporter_department="Unknown",
            channel=Channel.PORTAL,
            tags=["blank", "accidental"],
            difficulty="easy",
        ),
        # -------------------------------------------------------------------
        # 23. Facilities request misdirected to IT
        # -------------------------------------------------------------------
        ScenarioDefinition(
            scenario_id="NOSUP-023",
            subject="Broken chair in the 7th floor kitchen area",
            description=(
                "Hi,\n\n"
                "One of the chairs at the high-top table in the 7th floor kitchen/break room has a "
                "broken leg and wobbles badly. Someone is going to fall off it. Can you send someone to "
                "replace it?\n\n"
                "Thanks,\nAmara Obi"
            ),
            category=Category.NOT_SUPPORT,
            priority=Priority.P4,
            team=Team.NONE,
            needs_escalation=False,
            missing_info=[],
            next_best_action="Close — facilities/maintenance request sent to IT in error. Redirect to Facilities.",
            remediation_steps=[
                "No action required — redirect the sender to facilities@contoso.com and close ticket.",
            ],
            reporter_name="Amara Obi",
            reporter_email="amara.obi@contoso.com",
            reporter_department="Compliance",
            channel=Channel.PORTAL,
            tags=["misdirected", "facilities"],
            difficulty="medium",
        ),
        # -------------------------------------------------------------------
        # 24. Out-of-office auto-reply (sick leave — mentions system outage)
        # -------------------------------------------------------------------
        ScenarioDefinition(
            scenario_id="NOSUP-024",
            subject="Automatic Reply: RE: Salesforce outage this morning",
            description=(
                "I'm currently out sick and won't be checking email today. If this is about the "
                "Salesforce outage, please contact the Service Desk directly at x4500 or reach out to "
                "my teammate Jordan Liu (jordan.liu@contoso.com) who is covering for me.\n\n"
                "I'll be back tomorrow.\n\n"
                "— Natasha Romero"
            ),
            category=Category.NOT_SUPPORT,
            priority=Priority.P4,
            team=Team.NONE,
            needs_escalation=False,
            missing_info=[],
            next_best_action=(
                "Close — auto-reply from employee on sick leave. The referenced Salesforce outage "
                "should be tracked in its own ticket."
            ),
            remediation_steps=[
                "No action required — this is an out-of-office auto-reply, close ticket.",
            ],
            reporter_name="Natasha Romero",
            reporter_email="natasha.romero@contoso.com",
            reporter_department="Sales Engineering",
            channel=Channel.EMAIL,
            tags=["ooo", "auto-reply", "sick-leave"],
            difficulty="medium",
        ),
        # -------------------------------------------------------------------
        # 25. Thank-you that looks like it could be a new ticket
        # -------------------------------------------------------------------
        ScenarioDefinition(
            scenario_id="NOSUP-025",
            subject="RE: Shared drive access — all good now, one more thing",
            description=(
                "Hey team,\n\n"
                "Thanks for setting up the shared drive access so quickly! Everything is working and "
                "I can see all the folders I need.\n\n"
                "One more thing — and this isn't an IT request — could you let your manager know that "
                "the response time was amazing? I submitted the ticket at 9 AM and had access by 9:20. "
                "That's the fastest turnaround I've ever seen. Our team lead wants to give a shout-out "
                "at the next all-hands.\n\n"
                "Thanks again,\nWei Zhang"
            ),
            category=Category.NOT_SUPPORT,
            priority=Priority.P4,
            team=Team.NONE,
            needs_escalation=False,
            missing_info=[],
            next_best_action=(
                "Close — follow-up confirming resolution with positive feedback, no new issue. "
                "No action required."
            ),
            remediation_steps=[
                "No action required — user confirmed issue is resolved and provided positive feedback, "
                "close ticket.",
            ],
            reporter_name="Wei Zhang",
            reporter_email="wei.zhang@contoso.com",
            reporter_department="Fund Accounting",
            channel=Channel.EMAIL,
            tags=["thank-you", "follow-up", "resolved"],
            difficulty="medium",
        ),
    ]
