"""Low-priority (P4) scenario definitions across all categories.

Covers: cosmetic issues, minor inconveniences, feature requests,
informational questions, and low-impact issues that don't affect
productivity.
"""

from generator.models import Scenario

SCENARIOS: list[Scenario] = [
    # ──────────────────────────────────────────────────────────────────
    # 1. Display name change request — Access & Auth P4
    # ──────────────────────────────────────────────────────────────────
    Scenario(
        scenario_id="lp-display-name-change",
        category="Access & Authentication",
        priority="P4",
        assigned_team="Identity & Access Management",
        needs_escalation=False,
        missing_information=["contact_info"],
        subjects=[
            "Request to change my display name in Active Directory",
            "Can someone update my AD display name when you get a chance?",
            "Display name change request — no rush",
        ],
        descriptions=[
            "Hey team, I recently got married and changed my last name. Could someone update my display name in "
            "Active Directory to reflect the new one? It currently shows my maiden name in the GAL and on Teams. "
            "No rush at all — just whenever you have a spare moment.",
            "I'd like to request a display name change in AD. My name currently shows incorrectly in the address "
            "book. It's purely cosmetic — everything still works fine, just looks odd.",
        ],
        next_best_actions=[
            "Verify the requested name change with HR records and update the displayName attribute in Active "
            "Directory. Allow up to 24 hours for GAL sync.",
            "Confirm the user's identity and the new display name, then update AD and wait for the next directory "
            "sync cycle.",
        ],
        remediation_steps=[
            [
                "Verify the name change request against HR records",
                "Update the displayName attribute in Active Directory",
                "Trigger a directory sync or wait for the next scheduled cycle",
                "Confirm the change is reflected in the GAL and Teams",
            ],
        ],
        tags=["cosmetic", "low-impact"],
    ),
    # ──────────────────────────────────────────────────────────────────
    # 2. Monitor color calibration — Hardware P4
    # ──────────────────────────────────────────────────────────────────
    Scenario(
        scenario_id="lp-monitor-color-calibration",
        category="Hardware & Peripherals",
        priority="P4",
        assigned_team="Endpoint Engineering",
        needs_escalation=False,
        missing_information=["device_info"],
        subjects=[
            "Monitor colors look slightly off — can IT calibrate it?",
            "External monitor has a slight yellow tint — not urgent",
        ],
        descriptions=[
            "My external monitor seems to have a slight yellowish tint compared to my laptop screen. It's not "
            "preventing me from working but it's a bit annoying when I drag windows between screens and the colors "
            "don't match. Is there a standard color profile I should be using, or can IT calibrate it?",
            "The colors on my secondary monitor look a bit washed out compared to the primary. It's been like this "
            "since I got the new monitor last month. Not urgent at all — just wondering if there's a recommended "
            "ICC profile for this model.",
        ],
        next_best_actions=[
            "Provide the standard color profile for the monitor model and guide the user through display settings.",
            "Check the monitor model and provide the recommended ICC color profile.",
        ],
        remediation_steps=[
            [
                "Identify the monitor model and check for a recommended ICC profile",
                "Apply the standard color profile through Windows Display Settings",
                "Adjust brightness and contrast to match the primary display",
            ],
        ],
        tags=["cosmetic", "low-impact"],
    ),
    # ──────────────────────────────────────────────────────────────────
    # 3. Wi-Fi name confusing — Network P4
    # ──────────────────────────────────────────────────────────────────
    Scenario(
        scenario_id="lp-wifi-ssid-confusing",
        category="General Inquiry",
        priority="P4",
        assigned_team="Network Operations",
        needs_escalation=False,
        missing_information=["network_location"],
        subjects=[
            "Which Wi-Fi network should I connect to?",
            "Confused about the different Wi-Fi network names in the office",
        ],
        descriptions=[
            "I see three Wi-Fi networks in the office: Contoso-Corp, Contoso-Guest, and Contoso-IoT. Which one "
            "should I use for my work laptop? I've been on Contoso-Guest all week and everything seems to work "
            "but someone told me I should be on a different one. Not urgent — just want to make sure I'm on the "
            "right network.",
            "Quick question — I'm new and was wondering which wireless network I should connect to. I can see "
            "multiple SSIDs and don't want to accidentally use the wrong one. My laptop connects automatically "
            "to one but I'm not sure if it's the best choice.",
        ],
        next_best_actions=[
            "Direct the user to connect to the Contoso-Corp network using their domain credentials. The guest "
            "network has limited access to internal resources.",
            "Explain the Wi-Fi network options and help the user connect to the corporate SSID.",
        ],
        remediation_steps=[
            [
                "Explain the purpose of each Wi-Fi network (Corp, Guest, IoT)",
                "Help the user connect to the corporate Wi-Fi with their domain credentials",
                "Verify the user can access internal resources over the correct network",
            ],
        ],
        tags=["informational", "low-impact", "new-employee"],
    ),
    # ──────────────────────────────────────────────────────────────────
    # 4. Desktop wallpaper policy — Software P4
    # ──────────────────────────────────────────────────────────────────
    Scenario(
        scenario_id="lp-desktop-wallpaper-policy",
        category="General Inquiry",
        priority="P4",
        assigned_team="Endpoint Engineering",
        needs_escalation=False,
        missing_information=[],
        subjects=[
            "Can I change my desktop wallpaper or is it locked by policy?",
            "Desktop background won't change — is this a group policy thing?",
        ],
        descriptions=[
            "I tried to change my desktop wallpaper to a personal photo but the option seems greyed out. Is this "
            "locked by IT policy? If so, is there an approved set of wallpapers I can choose from? Totally not "
            "urgent, just curious.",
            "I noticed my desktop background resets to the corporate wallpaper every time I restart. Is it possible "
            "to have a custom wallpaper, or is this enforced for everyone? Just a minor cosmetic thing.",
        ],
        next_best_actions=[
            "Explain the corporate wallpaper policy. If the policy allows customization, guide the user on how to "
            "change it.",
            "Inform the user about the desktop customization policy and any approved alternatives.",
        ],
        remediation_steps=[
            [
                "Check the Group Policy settings for desktop wallpaper enforcement",
                "Explain the policy to the user",
                "If customization is allowed, guide them through the settings",
            ],
        ],
        tags=["informational", "cosmetic", "policy"],
    ),
    # ──────────────────────────────────────────────────────────────────
    # 5. Old software shortcut on desktop — Software P4
    # ──────────────────────────────────────────────────────────────────
    Scenario(
        scenario_id="lp-stale-desktop-shortcut",
        category="Software & Applications",
        priority="P4",
        assigned_team="Endpoint Engineering",
        needs_escalation=False,
        missing_information=["application_version"],
        subjects=[
            "Old shortcut on my desktop points to an app that was uninstalled",
            "Dead shortcut icon on desktop — just cosmetic",
        ],
        descriptions=[
            "I have a shortcut on my desktop for an application that was decommissioned months ago. Clicking it "
            "shows 'The item this shortcut refers to has been changed or moved.' I can just delete it myself but "
            "it keeps coming back after reboots. Can the deployment script be updated to stop recreating it?",
            "There's a leftover shortcut on my desktop from an old internal tool we stopped using last quarter. "
            "It's not causing any issues but it's cluttering my desktop. Every time I try to delete it, it comes "
            "back. Seems like something in the logon script is recreating it.",
        ],
        next_best_actions=[
            "Check the logon script or Intune deployment for the stale shortcut reference and remove it.",
            "Investigate the Group Policy or Intune configuration that's recreating the shortcut and update it.",
        ],
        remediation_steps=[
            [
                "Identify the logon script or Intune policy that creates the shortcut",
                "Remove the stale shortcut reference from the deployment configuration",
                "Delete the shortcut from the user's desktop",
                "Verify the shortcut no longer reappears after reboot",
            ],
        ],
        tags=["cosmetic", "low-impact", "cleanup"],
    ),
    # ──────────────────────────────────────────────────────────────────
    # 6. Email signature formatting request — General Inquiry P4
    # ──────────────────────────────────────────────────────────────────
    Scenario(
        scenario_id="lp-email-signature-format",
        category="General Inquiry",
        priority="P4",
        assigned_team="Enterprise Applications",
        needs_escalation=False,
        missing_information=["contact_info"],
        subjects=[
            "How do I update my email signature to the new template?",
            "Where can I find the standard email signature template?",
        ],
        descriptions=[
            "Marketing sent out a new email signature template last week and I'd like to update mine. Where do I "
            "find the template and how do I apply it in Outlook? I'm currently using an old format that doesn't "
            "match the new branding. Not urgent at all.",
            "I noticed my email signature looks different from my colleagues' — they all have the new company logo "
            "and updated layout. Could someone point me to the right template? I tried the intranet but couldn't "
            "find the latest version.",
        ],
        next_best_actions=[
            "Share the link to the current email signature template on the company intranet and provide instructions "
            "for applying it in Outlook.",
            "Direct the user to the standard email signature template and help them apply it.",
        ],
        remediation_steps=[
            [
                "Provide the user with the current email signature template link",
                "Share instructions for applying the signature in Outlook desktop and web",
                "Verify the signature renders correctly on both platforms",
            ],
        ],
        tags=["informational", "low-impact", "branding"],
    ),
    # ──────────────────────────────────────────────────────────────────
    # 7. Request for second monitor — Hardware P4
    # ──────────────────────────────────────────────────────────────────
    Scenario(
        scenario_id="lp-second-monitor-request",
        category="Hardware & Peripherals",
        priority="P4",
        assigned_team="Endpoint Engineering",
        needs_escalation=False,
        missing_information=["business_impact", "device_info"],
        subjects=[
            "Can I request a second monitor for my desk?",
            "Would like an additional monitor — who do I talk to?",
        ],
        descriptions=[
            "I'd like to request a second monitor for my workstation. I work with a lot of spreadsheets and having "
            "dual screens would really help my productivity. I know this isn't urgent — just wondering what the "
            "process is and if there are any available in stock.",
            "My team lead mentioned that IT can provide a second monitor if we put in a request. I'd like to get "
            "one set up at my desk. I'm currently using just my laptop screen and a single external. No rush on "
            "this — whenever inventory allows.",
        ],
        next_best_actions=[
            "Check monitor inventory and initiate the hardware request process. Verify the user's docking station "
            "supports dual monitors.",
            "Process the monitor request through the standard hardware procurement workflow.",
        ],
        remediation_steps=[
            [
                "Verify the user's docking station supports an additional monitor",
                "Check monitor inventory for available units",
                "Submit the hardware procurement request if needed",
                "Schedule delivery and setup once available",
            ],
        ],
        tags=["hardware-request", "low-impact"],
    ),
    # ──────────────────────────────────────────────────────────────────
    # 8. Timezone wrong in calendar — Software P4
    # ──────────────────────────────────────────────────────────────────
    Scenario(
        scenario_id="lp-calendar-timezone-wrong",
        category="Software & Applications",
        priority="P4",
        assigned_team="Enterprise Applications",
        needs_escalation=False,
        missing_information=["configuration_details"],
        subjects=[
            "Outlook calendar showing wrong timezone after travel",
            "Calendar times are off by one hour — daylight saving issue?",
        ],
        descriptions=[
            "I traveled to the West Coast for a conference last week and now my Outlook calendar is showing "
            "all meetings one hour early even though I'm back in New York. I've checked my Windows timezone "
            "settings and they're correct (Eastern). It seems like Outlook didn't sync back. Not urgent since "
            "I know the actual times, just annoying.",
            "My calendar events are all showing in the wrong timezone. Meeting invites that say 2 PM show up "
            "on my calendar as 11 AM. I think it might be a daylight saving time issue since this started "
            "after the recent time change. My laptop clock shows the correct time though.",
        ],
        next_best_actions=[
            "Check Outlook timezone settings and OWA timezone settings separately, as they can be out of sync.",
            "Verify and correct the timezone in both Outlook desktop and Outlook on the web.",
        ],
        remediation_steps=[
            [
                "Check the timezone setting in Outlook desktop under Calendar options",
                "Check the timezone setting in Outlook on the web under Settings > Calendar",
                "Ensure both match the user's correct timezone",
                "Restart Outlook to apply changes",
            ],
        ],
        tags=["cosmetic", "low-impact", "timezone"],
    ),
]

