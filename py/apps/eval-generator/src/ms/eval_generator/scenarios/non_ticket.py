# Copyright (c) Microsoft. All rights reserved.
"""Not a Support Ticket category scenarios for eval dataset."""

from ms.eval_generator.scenarios._base import ScenarioDefinition
from ms.eval_generator.scenarios._base import ScenarioGold

NON_TICKET_SCENARIOS: tuple[ScenarioDefinition, ...] = (
    # ------------------------------------------------------------------
    # 1  Sales pitch email from a software vendor
    # ------------------------------------------------------------------
    ScenarioDefinition(
        scenario_id="non-ticket-001",
        subjects=(
            "Exclusive offer — CloudSync Pro licenses at 40% off",
            "Let us help Contoso modernize its DevOps pipeline",
        ),
        descriptions=(
            "Hi there! I'm reaching out from CloudSync Solutions. We noticed Contoso Financial"
            " Services is growing fast and wanted to share our limited-time offer on CloudSync"
            " Pro — 40% off annual licenses if you sign by end of quarter. Happy to set up a"
            " quick demo at your convenience.",
            "Dear IT Team, I'd love to schedule a 15-minute call to show you how our platform"
            " can cut your deployment times in half. We work with several Fortune 500 financial"
            " firms. Would Thursday work?",
        ),
        gold=ScenarioGold(
            category="Not a Support Ticket",
            priority="P4",
            assigned_team="None",
            needs_escalation=False,
            missing_information=(),
            next_best_action="Close the ticket and discard the unsolicited sales email.",
            remediation_steps=(
                "Close ticket as not applicable.",
                "Mark sender email as vendor solicitation if recurring.",
            ),
        ),
    ),
    # ------------------------------------------------------------------
    # 2  Personal Amazon delivery tracking question
    # ------------------------------------------------------------------
    ScenarioDefinition(
        scenario_id="non-ticket-002",
        subjects=(
            "Where is my Amazon package?",
            "Need help tracking my personal delivery",
            "Amazon order still hasn't arrived",
        ),
        descriptions=(
            "Hey, I ordered a standing desk on Amazon last week and it says 'out for delivery'"
            " but nothing showed up. Can someone check with the mail room? My order number is"
            " 114-7839201-5543882.",
            "I'm expecting a personal Amazon package at the office and FedEx says it was"
            " delivered but I can't find it anywhere. Can IT look into this?",
        ),
        gold=ScenarioGold(
            category="Not a Support Ticket",
            priority="P4",
            assigned_team="None",
            needs_escalation=False,
            missing_information=(),
            next_best_action="Redirect the requester to the mailroom or facilities team.",
            remediation_steps=(
                "Close ticket as misdirected.",
                "Advise the requester to contact the mailroom or building reception.",
            ),
        ),
    ),
    # ------------------------------------------------------------------
    # 3  Spam / junk email forwarded to help desk
    # ------------------------------------------------------------------
    ScenarioDefinition(
        scenario_id="non-ticket-003",
        subjects=(
            "FW: You've won a $1,000 gift card!",
            "Fwd: Claim your free cruise vacation NOW",
        ),
        descriptions=(
            "Not sure if this is legit? I got this email saying I won a gift card and just"
            " wanted to forward it to you guys. Here's the full email below."
            " --- Forwarded message --- Congratulations! You have been selected ...",
            "Someone keeps sending me these emails about free vacations. I forwarded it to IT"
            " so you can block them or whatever. Thanks!",
            "Got another spam email, forwarding to the help desk so you're aware."
            " Subject was 'Urgent: verify your identity to receive prize'.",
        ),
        gold=ScenarioGold(
            category="Not a Support Ticket",
            priority="P4",
            assigned_team="None",
            needs_escalation=False,
            missing_information=(),
            next_best_action=(
                "Close the ticket and advise the user to delete spam and use the 'Report Phishing' button."
            ),
            remediation_steps=(
                "Close ticket as informational.",
                "Remind user to use the built-in 'Report Phishing' or 'Junk' button in Outlook.",
            ),
        ),
    ),
    # ------------------------------------------------------------------
    # 4  Auto-generated system notification (no action needed)
    # ------------------------------------------------------------------
    ScenarioDefinition(
        scenario_id="non-ticket-004",
        subjects=(
            "Automated backup report — all jobs completed successfully",
            "[INFO] Nightly maintenance window completed",
        ),
        descriptions=(
            "This is an automated message. All scheduled backup jobs for 2024-11-14 completed"
            " successfully. No action required. Summary: 48/48 jobs OK, 0 warnings, 0 errors.",
            "System notification: The nightly maintenance window (02:00–04:00 UTC) completed"
            " without issues. All services are operating normally.",
        ),
        gold=ScenarioGold(
            category="Not a Support Ticket",
            priority="P4",
            assigned_team="None",
            needs_escalation=False,
            missing_information=(),
            next_best_action="Close the ticket — this is an informational auto-notification requiring no action.",
            remediation_steps=("Close ticket as informational.",),
        ),
    ),
    # ------------------------------------------------------------------
    # 5  Calendar invite for a company social event
    # ------------------------------------------------------------------
    ScenarioDefinition(
        scenario_id="non-ticket-005",
        subjects=(
            "You're invited: Contoso Summer BBQ — July 19th",
            "Save the date — Annual team picnic",
        ),
        descriptions=(
            "Hi everyone! Please join us for the Contoso Summer BBQ on Friday, July 19th from"
            " 12 PM to 3 PM on the rooftop patio. RSVP by July 12th so we can get a headcount"
            " for catering. Burgers, veggie options, and ice cream!",
            "Friendly reminder about the annual team picnic next Saturday at Riverside Park."
            " Bring your families! Please RSVP via the link in your calendar invite.",
        ),
        gold=ScenarioGold(
            category="Not a Support Ticket",
            priority="P4",
            assigned_team="None",
            needs_escalation=False,
            missing_information=(),
            next_best_action="Close the ticket — this is a social event notice, not an IT request.",
            remediation_steps=("Close ticket as not applicable.",),
        ),
    ),
    # ------------------------------------------------------------------
    # 6  Newsletter subscription from tech blog
    # ------------------------------------------------------------------
    ScenarioDefinition(
        scenario_id="non-ticket-006",
        subjects=(
            "This Week in Cloud Computing — Issue #247",
            "TechDigest Weekly: AI trends you need to know",
        ),
        descriptions=(
            "Welcome to this week's edition of Cloud Computing Weekly! In this issue:"
            " multi-cloud strategies for 2025, a deep dive into serverless cost optimization,"
            " and an interview with the CTO of Dataflux. Read more at cloudweekly.io.",
            "TechDigest Weekly — Nov 14 edition. Top stories: GenAI adoption in financial"
            " services, Kubernetes 1.31 release highlights, and 5 tips for securing your"
            " CI/CD pipeline. Unsubscribe at the bottom of this email.",
        ),
        gold=ScenarioGold(
            category="Not a Support Ticket",
            priority="P4",
            assigned_team="None",
            needs_escalation=False,
            missing_information=(),
            next_best_action="Close the ticket — this is a newsletter, not a support request.",
            remediation_steps=(
                "Close ticket as not applicable.",
                "Advise user to unsubscribe from the mailing list directly.",
            ),
        ),
    ),
    # ------------------------------------------------------------------
    # 7  Vendor invoice / billing question (should go to Finance)
    # ------------------------------------------------------------------
    ScenarioDefinition(
        scenario_id="non-ticket-007",
        subjects=(
            "Invoice #INV-2024-8821 — overdue balance",
            "Question about our Contoso billing account",
            "Payment reminder — Contoso Financial Services",
        ),
        descriptions=(
            "Hi, this is Priya from NetSecure Solutions. Invoice #INV-2024-8821 for $12,340"
            " was due on October 31st and we haven't received payment yet. Could someone in"
            " your team process this? Attaching the invoice PDF for reference.",
            "We noticed that Contoso's account has an outstanding balance of $8,750 for Q3"
            " consulting services. Please remit payment at your earliest convenience or"
            " contact us to discuss payment terms.",
        ),
        gold=ScenarioGold(
            category="Not a Support Ticket",
            priority="P4",
            assigned_team="None",
            needs_escalation=False,
            missing_information=(),
            next_best_action="Redirect the requester to the Finance or Accounts Payable department.",
            remediation_steps=(
                "Close ticket as misdirected.",
                "Forward the inquiry to Finance / Accounts Payable.",
            ),
        ),
    ),
    # ------------------------------------------------------------------
    # 8  HR policy question about vacation days (should go to HR)
    # ------------------------------------------------------------------
    ScenarioDefinition(
        scenario_id="non-ticket-008",
        subjects=(
            "How many vacation days do I have left?",
            "PTO policy clarification needed",
        ),
        descriptions=(
            "Hi, I'm trying to figure out how many PTO days I have remaining this year. I"
            " checked Workday but I'm confused by the accrual numbers. Can someone help me"
            " understand my balance? I've been here for 3 years.",
            "Quick question — does unused PTO roll over into next year or is it use-it-or-lose"
            "-it? I couldn't find a clear answer in the employee handbook and figured IT might"
            " know since you manage the systems.",
            "I need to take two weeks off in December. Who do I talk to about extended leave"
            " approval? Is there a form I need to fill out?",
        ),
        gold=ScenarioGold(
            category="Not a Support Ticket",
            priority="P4",
            assigned_team="None",
            needs_escalation=False,
            missing_information=(),
            next_best_action="Redirect the requester to Human Resources for PTO policy questions.",
            remediation_steps=(
                "Close ticket as misdirected.",
                "Direct the employee to HR or the HR portal for PTO inquiries.",
            ),
        ),
    ),
    # ------------------------------------------------------------------
    # 9  Marketing campaign feedback request
    # ------------------------------------------------------------------
    ScenarioDefinition(
        scenario_id="non-ticket-009",
        subjects=(
            "Feedback needed: Q4 marketing campaign creative",
            "Review request — new Contoso brand assets",
        ),
        descriptions=(
            "Hey team, Marketing is looking for feedback on the new Q4 campaign visuals before"
            " we go live next week. Can you take a look at the mockups in the shared drive and"
            " leave comments? Link: https://contoso.sharepoint.com/marketing/q4-review",
            "Hi! We've updated the Contoso brand guidelines and would love your input. Please"
            " review the attached PDF and share any thoughts by Friday. Thanks!",
        ),
        gold=ScenarioGold(
            category="Not a Support Ticket",
            priority="P4",
            assigned_team="None",
            needs_escalation=False,
            missing_information=(),
            next_best_action="Close the ticket — marketing feedback requests are not IT issues.",
            remediation_steps=(
                "Close ticket as misdirected.",
                "Suggest the requester use a Marketing-specific channel for feedback.",
            ),
        ),
    ),
    # ------------------------------------------------------------------
    # 10  Out-of-office auto-reply accidentally sent to help desk
    # ------------------------------------------------------------------
    ScenarioDefinition(
        scenario_id="non-ticket-010",
        subjects=(
            "Out of Office: Re: Your IT ticket update",
            "Automatic reply: I'm currently out of the office",
        ),
        descriptions=(
            "Thank you for your email. I am currently out of the office from November 11–18"
            " with limited access to email. For urgent matters, please contact my manager,"
            " David Chen, at d.chen@contoso.com. I will respond to your message when I return.",
            "Hi, I'm on PTO until Monday the 20th. If this is urgent please reach out to"
            " the team alias at ops-team@contoso.com. Otherwise I'll get back to you when"
            " I'm back. Thanks!",
        ),
        gold=ScenarioGold(
            category="Not a Support Ticket",
            priority="P4",
            assigned_team="None",
            needs_escalation=False,
            missing_information=(),
            next_best_action="Close the ticket — this is an automated out-of-office reply, not a support request.",
            remediation_steps=("Close ticket as auto-generated noise.",),
        ),
    ),
    # ------------------------------------------------------------------
    # 11  Thank-you note for previous ticket resolution
    # ------------------------------------------------------------------
    ScenarioDefinition(
        scenario_id="non-ticket-011",
        subjects=(
            "Re: [Ticket #48291] — Thanks so much!",
            "Thank you for fixing my laptop!",
            "Appreciate the quick turnaround",
        ),
        descriptions=(
            "Just wanted to say thanks for resolving my issue so quickly! My laptop is running"
            " great now and I can finally access SharePoint again. You guys are awesome.",
            "Hey team, thank you for the help last week with my VPN problem. Everything has"
            " been working perfectly since the fix. Really appreciate it!",
        ),
        gold=ScenarioGold(
            category="Not a Support Ticket",
            priority="P4",
            assigned_team="None",
            needs_escalation=False,
            missing_information=(),
            next_best_action="Close the ticket — this is a thank-you note, no action required.",
            remediation_steps=("Close ticket as informational — no issue reported.",),
        ),
    ),
    # ------------------------------------------------------------------
    # 12  Meeting notes forwarded by mistake
    # ------------------------------------------------------------------
    ScenarioDefinition(
        scenario_id="non-ticket-012",
        subjects=(
            "FW: Q3 Strategy Meeting Notes — Action Items",
            "Fwd: Product Roadmap Sync — Nov 10 recap",
        ),
        descriptions=(
            "Hi all, here are the notes from Friday's strategy meeting. Action items:"
            " 1) Sarah to finalize the budget proposal by Nov 22. 2) Mike to schedule"
            " follow-up with the legal team. 3) Lisa to update the project timeline in Jira."
            " Let me know if I missed anything.",
            "Forwarding the meeting recap from the product roadmap sync. Key decisions: we're"
            " pushing the v3.2 release to January, the analytics dashboard redesign is"
            " approved, and we need two more QA engineers for the compliance module.",
        ),
        gold=ScenarioGold(
            category="Not a Support Ticket",
            priority="P4",
            assigned_team="None",
            needs_escalation=False,
            missing_information=(),
            next_best_action="Close the ticket — meeting notes were forwarded to the help desk by mistake.",
            remediation_steps=(
                "Close ticket as misdirected.",
                "Notify the sender that they accidentally sent this to the IT help desk.",
            ),
        ),
    ),
    # ------------------------------------------------------------------
    # 13  Job application sent to wrong email
    # ------------------------------------------------------------------
    ScenarioDefinition(
        scenario_id="non-ticket-013",
        subjects=(
            "Application for Senior Data Engineer position",
            "Resume submission — Software Developer role at Contoso",
        ),
        descriptions=(
            "Dear Hiring Manager, I am writing to express my interest in the Senior Data"
            " Engineer position at Contoso Financial Services. With over 8 years of experience"
            " in data engineering and a strong background in Python, Spark, and Azure Data"
            " Factory, I believe I would be a great fit. Please find my resume attached.",
            "Hello, I saw the Software Developer opening on LinkedIn and wanted to apply."
            " I have 5 years of full-stack experience with React and .NET. My resume and"
            " portfolio are attached. Looking forward to hearing from you!",
        ),
        gold=ScenarioGold(
            category="Not a Support Ticket",
            priority="P4",
            assigned_team="None",
            needs_escalation=False,
            missing_information=(),
            next_best_action="Redirect the applicant to the HR recruiting team or careers portal.",
            remediation_steps=(
                "Close ticket as misdirected.",
                "Reply to the sender with the correct careers/recruiting email address.",
            ),
        ),
    ),
    # ------------------------------------------------------------------
    # 14  Internal social event RSVP
    # ------------------------------------------------------------------
    ScenarioDefinition(
        scenario_id="non-ticket-014",
        subjects=(
            "RE: Holiday Party RSVP — Count me in!",
            "RSVP: Yes for the team happy hour",
        ),
        descriptions=(
            "Hey! Yes, I'll be at the holiday party on the 15th. Put me down for +1. Also,"
            " is there a vegetarian option for dinner? Thanks!",
            "Count me in for the happy hour on Thursday! I'll be there around 5:30. Should I"
            " bring anything? Looking forward to it.",
            "RSVP: Attending. Can I also bring my intern? She just started last week and it"
            " would be a great way for her to meet the team.",
        ),
        gold=ScenarioGold(
            category="Not a Support Ticket",
            priority="P4",
            assigned_team="None",
            needs_escalation=False,
            missing_information=(),
            next_best_action="Close the ticket — RSVP was accidentally sent to the help desk.",
            remediation_steps=(
                "Close ticket as misdirected.",
                "Advise the sender to reply to the original event organizer.",
            ),
        ),
    ),
    # ------------------------------------------------------------------
    # 15  Facilities request — office temperature too cold
    # ------------------------------------------------------------------
    ScenarioDefinition(
        scenario_id="non-ticket-015",
        subjects=(
            "Office is freezing — can someone adjust the thermostat?",
            "Temperature issue on the 4th floor",
        ),
        descriptions=(
            "Hi, the temperature on the 4th floor near the east wing has been really cold all"
            " week. Several of us are wearing jackets at our desks. Can someone look into the"
            " HVAC settings? It feels like it's around 62°F in here.",
            "The AC is blasting in Conference Room 4B and it's uncomfortable for meetings."
            " We've had two client calls this week where people were shivering. Can Facilities"
            " take a look?",
            "Is there a way to adjust the thermostat near desk cluster 4-12? It's noticeably"
            " colder than the rest of the floor.",
        ),
        gold=ScenarioGold(
            category="Not a Support Ticket",
            priority="P4",
            assigned_team="None",
            needs_escalation=False,
            missing_information=(),
            next_best_action="Redirect the requester to the Facilities Management team.",
            remediation_steps=(
                "Close ticket as misdirected.",
                "Direct the requester to submit a facilities request for HVAC adjustment.",
            ),
        ),
    ),
    # ------------------------------------------------------------------
    # 16  Parking lot issue — reserved spot taken
    # ------------------------------------------------------------------
    ScenarioDefinition(
        scenario_id="non-ticket-016",
        subjects=(
            "Someone parked in my reserved spot again",
            "Parking issue — spot B-24 occupied by unknown vehicle",
        ),
        descriptions=(
            "This is the third time this month someone has parked in my reserved spot (B-24)"
            " in the garage. I have a permit sticker and everything. Can someone do something"
            " about this? The car is a silver Honda Civic, no permit visible.",
            "Hi, I came in this morning and there's a white SUV in my assigned parking spot"
            " on level 2. I had to park on the street and I'm going to get a ticket. Who do"
            " I contact about this?",
        ),
        gold=ScenarioGold(
            category="Not a Support Ticket",
            priority="P4",
            assigned_team="None",
            needs_escalation=False,
            missing_information=(),
            next_best_action="Redirect the requester to Facilities or Building Security for parking issues.",
            remediation_steps=(
                "Close ticket as misdirected.",
                "Direct the requester to Facilities Management or Building Security.",
            ),
        ),
    ),
    # ------------------------------------------------------------------
    # 17  Cafeteria menu inquiry
    # ------------------------------------------------------------------
    ScenarioDefinition(
        scenario_id="non-ticket-017",
        subjects=(
            "What's for lunch today in the cafeteria?",
            "Cafeteria menu question — any gluten-free options?",
        ),
        descriptions=(
            "Does anyone know what the cafeteria is serving today? I didn't see the menu"
            " posted on the intranet. Also, are they still doing Taco Tuesdays?",
            "Hi, I have celiac disease and I'm wondering if the cafeteria offers gluten-free"
            " meal options. I've asked the staff but they suggested I contact IT since the"
            " menu is posted on the intranet. Can you help?",
        ),
        gold=ScenarioGold(
            category="Not a Support Ticket",
            priority="P4",
            assigned_team="None",
            needs_escalation=False,
            missing_information=(),
            next_best_action="Redirect the requester to the cafeteria vendor or Facilities team.",
            remediation_steps=(
                "Close ticket as misdirected.",
                "Advise the requester to contact the cafeteria vendor or check the intranet.",
            ),
        ),
    ),
    # ------------------------------------------------------------------
    # 18  Charity fundraiser announcement
    # ------------------------------------------------------------------
    ScenarioDefinition(
        scenario_id="non-ticket-018",
        subjects=(
            "Contoso Cares: Annual charity drive kicks off next week!",
            "Support the local food bank — volunteer signup",
        ),
        descriptions=(
            "Hi everyone! The Contoso Cares committee is excited to announce our annual"
            " charity drive starting November 20th. This year we're supporting the Metro City"
            " Food Bank. Drop off canned goods in the lobby or donate online via the link"
            " below. Every little bit helps!",
            "Volunteers needed! We're organizing a build day with Habitat for Humanity on"
            " December 7th. Sign up at the link below. T-shirts provided. No construction"
            " experience necessary!",
        ),
        gold=ScenarioGold(
            category="Not a Support Ticket",
            priority="P4",
            assigned_team="None",
            needs_escalation=False,
            missing_information=(),
            next_best_action="Close the ticket — this is a charity announcement, not an IT request.",
            remediation_steps=("Close ticket as not applicable.",),
        ),
    ),
    # ------------------------------------------------------------------
    # 19  Employee birthday celebration coordination
    # ------------------------------------------------------------------
    ScenarioDefinition(
        scenario_id="non-ticket-019",
        subjects=(
            "Surprise birthday for Priya — please chip in!",
            "Birthday cake for Marcus on Friday",
        ),
        descriptions=(
            "Hey team! Priya's birthday is next Wednesday and we're putting together a"
            " surprise celebration. If you'd like to chip in for a cake and gift card, Venmo"
            " me @JessicaL or drop $5 in the envelope on my desk. Don't tell Priya!",
            "Quick heads up — Marcus turns 40 on Friday! We're getting a cake from the bakery"
            " downstairs. Meet in the break room at 2 PM for a quick celebration. Please keep"
            " it a secret!",
            "We're collecting signatures for a birthday card for Aisha. Stop by desk 3-14"
            " before Thursday to sign it.",
        ),
        gold=ScenarioGold(
            category="Not a Support Ticket",
            priority="P4",
            assigned_team="None",
            needs_escalation=False,
            missing_information=(),
            next_best_action="Close the ticket — birthday coordination is not an IT matter.",
            remediation_steps=(
                "Close ticket as not applicable.",
                "Suggest the organizer use a non-IT channel such as Teams or email.",
            ),
        ),
    ),
    # ------------------------------------------------------------------
    # 20  Real estate / office space broker email
    # ------------------------------------------------------------------
    ScenarioDefinition(
        scenario_id="non-ticket-020",
        subjects=(
            "Premium office space available — Financial District",
            "Contoso expansion? We have the perfect space for you",
        ),
        descriptions=(
            "Dear Contoso Team, we have Class A office space available in the Financial"
            " District — 15,000 sq ft across two floors, modern buildout, fiber connectivity,"
            " and below-market rates. Flexible lease terms available. Would love to schedule"
            " a tour. Best regards, Commercial Realty Group.",
            "Hi, I represent a landlord with newly renovated office suites near your current"
            " headquarters. Given Contoso's recent growth, I thought this might be of interest."
            " Shall I send over the floor plans?",
        ),
        gold=ScenarioGold(
            category="Not a Support Ticket",
            priority="P4",
            assigned_team="None",
            needs_escalation=False,
            missing_information=(),
            next_best_action="Close the ticket and discard the unsolicited commercial real estate email.",
            remediation_steps=("Close ticket as not applicable.",),
        ),
    ),
    # ------------------------------------------------------------------
    # 21  Conference / event invitation (non-IT)
    # ------------------------------------------------------------------
    ScenarioDefinition(
        scenario_id="non-ticket-021",
        subjects=(
            "Invitation: FinTech Leaders Summit 2025 — Early bird pricing",
            "Join us at the Global Banking Innovation Forum",
        ),
        descriptions=(
            "You're invited to the FinTech Leaders Summit, March 12-14, 2025 in San Francisco."
            " Hear from 50+ industry speakers, attend hands-on workshops, and network with"
            " peers from top financial institutions. Register before Dec 31 for early bird"
            " pricing: $1,299 (reg. $1,899).",
            "Dear Contoso colleagues, the Global Banking Innovation Forum is coming to Chicago"
            " this February. Our CEO will be delivering a keynote. Interested attendees should"
            " contact the Events team for approval and registration.",
        ),
        gold=ScenarioGold(
            category="Not a Support Ticket",
            priority="P4",
            assigned_team="None",
            needs_escalation=False,
            missing_information=(),
            next_best_action="Close the ticket — conference invitations are not IT support requests.",
            remediation_steps=("Close ticket as not applicable.",),
        ),
    ),
    # ------------------------------------------------------------------
    # 22  Survey / poll about employee satisfaction
    # ------------------------------------------------------------------
    ScenarioDefinition(
        scenario_id="non-ticket-022",
        subjects=(
            "Your voice matters — 2024 Employee Engagement Survey",
            "Quick poll: How satisfied are you with the new office layout?",
        ),
        descriptions=(
            "Hi everyone, it's that time of year again! Please take 10 minutes to complete"
            " the annual Employee Engagement Survey. Your anonymous feedback helps leadership"
            " make Contoso a better place to work. The survey closes November 30th."
            " Link: https://contoso.survey.com/engage2024",
            "We recently redesigned the 3rd floor open workspace and we'd love your feedback."
            " Please fill out this 2-minute poll so we can make adjustments."
            " https://forms.contoso.com/office-layout",
        ),
        gold=ScenarioGold(
            category="Not a Support Ticket",
            priority="P4",
            assigned_team="None",
            needs_escalation=False,
            missing_information=(),
            next_best_action="Close the ticket — employee surveys are not IT support issues.",
            remediation_steps=("Close ticket as not applicable.",),
        ),
    ),
    # ------------------------------------------------------------------
    # 23  Lost and found — personal item left in office
    # ------------------------------------------------------------------
    ScenarioDefinition(
        scenario_id="non-ticket-023",
        subjects=(
            "Lost my water bottle — anyone seen it?",
            "Found a pair of AirPods in the 5th floor kitchen",
            "Left my jacket in Conference Room C",
        ),
        descriptions=(
            "I left my blue Hydro Flask in the 3rd floor kitchen yesterday afternoon. Has"
            " anyone turned it in? It has a bunch of stickers on it — hard to miss. Please"
            " let me know if you've seen it!",
            "Found a pair of AirPods Pro in their case on the counter in the 5th floor"
            " kitchen around 4 PM today. I left them at the front desk. Owner can pick them"
            " up there.",
        ),
        gold=ScenarioGold(
            category="Not a Support Ticket",
            priority="P4",
            assigned_team="None",
            needs_escalation=False,
            missing_information=(),
            next_best_action="Redirect the requester to building reception or the lost-and-found service.",
            remediation_steps=(
                "Close ticket as misdirected.",
                "Advise the requester to check with front desk or post on the office Slack channel.",
            ),
        ),
    ),
    # ------------------------------------------------------------------
    # 24  Travel booking assistance request
    # ------------------------------------------------------------------
    ScenarioDefinition(
        scenario_id="non-ticket-024",
        subjects=(
            "Need help booking a flight to the NYC office",
            "Travel request — client visit in London next month",
        ),
        descriptions=(
            "Hi, I need to fly to the New York office for a project kickoff on December 5th"
            " and return the 7th. Can someone help me book the flights and hotel? I'm not sure"
            " how to use Concur — is there a travel coordinator I should contact?",
            "I have a client meeting in London the week of January 13th and need to book"
            " flights and a hotel. What's the process for international travel approval at"
            " Contoso? Do I need VP sign-off?",
        ),
        gold=ScenarioGold(
            category="Not a Support Ticket",
            priority="P4",
            assigned_team="None",
            needs_escalation=False,
            missing_information=(),
            next_best_action="Redirect the requester to the Travel and Expense team or their manager.",
            remediation_steps=(
                "Close ticket as misdirected.",
                "Direct the requester to the corporate travel portal or Travel & Expense team.",
            ),
        ),
    ),
    # ------------------------------------------------------------------
    # 25  Company sports team signup
    # ------------------------------------------------------------------
    ScenarioDefinition(
        scenario_id="non-ticket-025",
        subjects=(
            "Contoso softball team — spring season signup",
            "Anyone want to join the office volleyball league?",
        ),
        descriptions=(
            "Hey everyone! The Contoso Crushers are gearing up for the spring corporate"
            " softball season. Games are Thursday evenings starting in April. All skill levels"
            " welcome — we mostly just have fun. Reply to this email if you want to play!",
            "We're forming a volleyball team for the inter-company league. Practices on"
            " Wednesdays at lunch in the park across the street. Need at least 4 more players."
            " Who's in?",
            "Sign up for the Contoso 5K Fun Run! It's on March 8th, proceeds go to the"
            " Children's Hospital. Registration link in the intranet under 'Events'.",
        ),
        gold=ScenarioGold(
            category="Not a Support Ticket",
            priority="P4",
            assigned_team="None",
            needs_escalation=False,
            missing_information=(),
            next_best_action="Close the ticket — sports team signups are not IT matters.",
            remediation_steps=("Close ticket as not applicable.",),
        ),
    ),
    # ------------------------------------------------------------------
    # 26  Recruiter outreach / headhunting email
    # ------------------------------------------------------------------
    ScenarioDefinition(
        scenario_id="non-ticket-026",
        subjects=(
            "Exciting opportunity — Senior Cloud Architect role",
            "Are you open to new opportunities?",
        ),
        descriptions=(
            "Hi, I came across your profile on LinkedIn and I'm impressed by your background."
            " I'm recruiting for a Senior Cloud Architect role at a leading fintech company"
            " offering $220K+ base, full remote, and equity. Would you be open to a quick"
            " chat this week?",
            "Hello, I'm a technical recruiter at Apex Talent Partners. We're working with a"
            " well-funded startup looking for an Engineering Manager to build out their"
            " platform team. Competitive comp and benefits. Interested in learning more?",
        ),
        gold=ScenarioGold(
            category="Not a Support Ticket",
            priority="P4",
            assigned_team="None",
            needs_escalation=False,
            missing_information=(),
            next_best_action="Close the ticket and discard the recruiter outreach email.",
            remediation_steps=("Close ticket as not applicable.",),
        ),
    ),
    # ------------------------------------------------------------------
    # 27  Building maintenance request — leaky faucet
    # ------------------------------------------------------------------
    ScenarioDefinition(
        scenario_id="non-ticket-027",
        subjects=(
            "Leaky faucet in the 2nd floor men's restroom",
            "Maintenance needed — bathroom sink won't stop dripping",
        ),
        descriptions=(
            "The faucet in the second stall of the 2nd floor men's restroom has been dripping"
            " nonstop for about a week now. It's pretty wasteful and the constant dripping"
            " noise is audible from the hallway. Can someone from maintenance take a look?",
            "Hi, the sink in the women's restroom on floor 3 is leaking onto the floor. It's"
            " getting slippery and someone could fall. This seems like it needs urgent"
            " attention from the building maintenance crew.",
        ),
        gold=ScenarioGold(
            category="Not a Support Ticket",
            priority="P4",
            assigned_team="None",
            needs_escalation=False,
            missing_information=(),
            next_best_action="Redirect the requester to Building Maintenance or Facilities Management.",
            remediation_steps=(
                "Close ticket as misdirected.",
                "Direct the requester to submit a building maintenance request.",
            ),
        ),
    ),
    # ------------------------------------------------------------------
    # 28  Request to update business card title
    # ------------------------------------------------------------------
    ScenarioDefinition(
        scenario_id="non-ticket-028",
        subjects=(
            "Need new business cards with my updated title",
            "Business card reorder — title change",
        ),
        descriptions=(
            "Hi, I was recently promoted to Senior Financial Analyst and I need new business"
            " cards with my updated title. I still have about 50 old ones but they say"
            " 'Financial Analyst' which is no longer correct. Who handles ordering these?",
            "I'm attending a conference next month and just realized my business cards have my"
            " old title and the previous office address. Can I get a rush order for 200 cards"
            " with the correct info?",
            "My business cards still show our old logo. How do I get new ones printed with the"
            " refreshed Contoso branding?",
        ),
        gold=ScenarioGold(
            category="Not a Support Ticket",
            priority="P4",
            assigned_team="None",
            needs_escalation=False,
            missing_information=(),
            next_best_action="Redirect the requester to Office Services or the Marketing/Brand team.",
            remediation_steps=(
                "Close ticket as misdirected.",
                "Direct the requester to Office Services or the branding team for business card orders.",
            ),
        ),
    ),
    # ------------------------------------------------------------------
    # 29  Insurance / benefits enrollment question
    # ------------------------------------------------------------------
    ScenarioDefinition(
        scenario_id="non-ticket-029",
        subjects=(
            "Open enrollment question — dental plan options",
            "Help with benefits enrollment — HSA vs. FSA",
        ),
        descriptions=(
            "Hi, open enrollment ends next Friday and I'm trying to decide between the PPO"
            " and HMO dental plans. The PPO is $30/month more but covers orthodontia. My kid"
            " might need braces next year. Is there someone in Benefits who can walk me through"
            " the details?",
            "I'm confused about the difference between the HSA and FSA options. I know one"
            " rolls over and the other doesn't, but I'm not sure which is better for my"
            " situation. Can IT point me to the right person?",
        ),
        gold=ScenarioGold(
            category="Not a Support Ticket",
            priority="P4",
            assigned_team="None",
            needs_escalation=False,
            missing_information=(),
            next_best_action="Redirect the requester to HR Benefits for enrollment questions.",
            remediation_steps=(
                "Close ticket as misdirected.",
                "Direct the employee to HR Benefits or the benefits enrollment portal.",
            ),
        ),
    ),
    # ------------------------------------------------------------------
    # 30  Colleague trying to reach someone not in IT
    # ------------------------------------------------------------------
    ScenarioDefinition(
        scenario_id="non-ticket-030",
        subjects=(
            "Trying to reach Kevin in Compliance — is he still at this email?",
            "Can someone forward this to Janice in Legal?",
        ),
        descriptions=(
            "Hi, I've been trying to reach Kevin Park in the Compliance department for two"
            " days and he hasn't responded to my emails or Teams messages. Does anyone know"
            " if he's out of office or if his contact info changed? It's kind of urgent — we"
            " have a regulatory filing due Friday.",
            "I need to get a contract reviewed by Janice Morales in Legal but I don't have"
            " her email. I tried searching the directory but nothing came up. Can IT help me"
            " find her contact info?",
            "Does anyone know who replaced Tom Harris in Procurement? I have a PO that needs"
            " approval and Tom's account seems to be deactivated.",
        ),
        gold=ScenarioGold(
            category="Not a Support Ticket",
            priority="P4",
            assigned_team="None",
            needs_escalation=False,
            missing_information=(),
            next_best_action="Redirect the requester to the company directory or the relevant department.",
            remediation_steps=(
                "Close ticket as misdirected.",
                "Advise the requester to use the employee directory or contact the relevant department.",
            ),
        ),
    ),
)
