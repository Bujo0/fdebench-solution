"""Hardware & Peripherals scenario definitions."""

from generator.models import Scenario

SCENARIOS: list[Scenario] = [
    # ------------------------------------------------------------------
    # P1 scenarios (~10%)
    # ------------------------------------------------------------------
    Scenario(
        scenario_id="hw-laptop-stolen",
        category="Hardware & Peripherals",
        priority="P1",
        assigned_team="Endpoint Engineering",
        needs_escalation=True,
        missing_information=["device_info", "timestamp", "business_impact"],
        subjects=[
            "Laptop stolen from my car — need immediate lockdown",
            "Company laptop was stolen — URGENT security risk",
            "Theft of company laptop — need remote wipe NOW",
        ],
        descriptions=[
            "My company laptop was stolen from my car last night while I was at dinner. It has client financial data on"
            " it and I'm terrified about a data breach. I've already filed a police report (case #2024-8837). I need th"
            "e device wiped and locked down immediately. This is a ThinkPad X1 Carbon, asset tag CT-4892.",
            "Someone broke into my car at the airport long-term lot and took my work laptop. I didn't notice until I la"
            "nded. It has access to the trading platform and several client portfolios. Please remote-wipe it ASAP. I d"
            "on't remember the exact model but it was issued about 6 months ago.",
            "URGENT — my laptop was stolen from my bag at a coffee shop about an hour ago. I had sensitive compliance "
            "documents open and I'm not 100% sure the disk encryption was enabled. Need this device killed remotely "
            "right now. Already called the police.",
        ],
        next_best_actions=[
            "Immediately initiate remote wipe via Intune and disable device in Azure AD. Escalate to Security "
            "Operations for data exposure assessment. Confirm BitLocker status.",
            "Lock the device via Intune, revoke all active sessions, and coordinate with Security Operations on "
            "potential data breach response. File asset loss report.",
        ],
        remediation_steps=[
            [
                "Verify reporter identity and confirm device asset tag via CMDB",
                "Initiate immediate remote wipe via Microsoft Intune",
                "Disable device object in Azure AD to revoke all tokens",
                "Confirm BitLocker encryption status from last check-in",
                "Escalate to Security Operations for data exposure assessment",
                "File asset loss report and update CMDB inventory",
                "Coordinate replacement device provisioning with user's manager",
            ],
        ],
        tags=["security", "data-loss-risk", "asset-loss"],
    ),
    Scenario(
        scenario_id="hw-hdd-clicking",
        category="Hardware & Peripherals",
        priority="P1",
        assigned_team="Endpoint Engineering",
        needs_escalation=True,
        missing_information=["device_info", "business_impact", "timestamp"],
        subjects=[
            "Hard drive making loud clicking — afraid of data loss",
            "Laptop hard drive clicking and freezing — critical files at risk",
            "Clicking noise from laptop, files not saving — HELP",
        ],
        descriptions=[
            "My laptop started making a loud repetitive clicking noise about 30 minutes ago and now it's freezing every"
            " few seconds. I have months of client portfolio analysis on this machine that I haven't backed up to OneDr"
            "ive yet. I'm afraid the hard drive is about to die. This is a Dell Latitude 5540, about 2 years old.",
            "My workstation's hard drive is making an awful clicking sound — like a metronome. Programs are taking "
            "forever to open and I got two 'disk read error' popups in the last hour. I have the only copy of the Q4 "
            "regulatory filings on this machine. Please send someone before it's too late.",
            "Hearing a clicking/grinding sound from my laptop. It started this morning and is getting worse. The "
            "machine is painfully slow now and I'm scared to shut it down in case it won't boot again. I need someone "
            "to pull my data off before this drive gives up completely.",
        ],
        next_best_actions=[
            "Dispatch technician immediately to attempt emergency data backup before drive failure. Do NOT instruct "
            "user to restart. Prepare replacement device.",
            "Advise user to keep device powered on but stop writing data. Send field tech for emergency disk clone and "
            "replacement.",
        ],
        remediation_steps=[
            [
                "Advise user to stop saving files and keep the device powered on",
                "Dispatch technician to user's location with backup equipment",
                "Attempt emergency data clone using disk imaging tool",
                "Verify critical files are recoverable and copy to network storage",
                "Replace failing drive or provision replacement laptop",
                "Restore user data to new device and verify integrity",
                "Educate user on OneDrive backup and Known Folder Move policy",
            ],
        ],
        tags=["data-loss-risk", "urgent-dispatch"],
    ),
    Scenario(
        scenario_id="hw-building-monitors-flicker",
        category="Hardware & Peripherals",
        priority="P1",
        assigned_team="Endpoint Engineering",
        needs_escalation=True,
        missing_information=["affected_users", "network_location", "environment_details"],
        subjects=[
            "Multiple monitors flickering across the entire 3rd floor",
            "Building-wide monitor flickering — affecting dozens of people",
            "Mass display issues on floor 3 — all monitors going haywire",
        ],
        descriptions=[
            "Every monitor on the 3rd floor of Building A is flickering simultaneously. It started about 20 minutes ago"
            " and is affecting at least 40 people. Some screens are going completely black for a few seconds at a time."
            " We've tried different cables and docking stations — same issue everywhere. This is crippling our operatio"
            "ns.",
            "We have a widespread monitor problem on the 3rd floor. All displays — Dell and HP — are flickering at the "
            "same rate, which makes me think it's a power or infrastructure issue. The trading floor is impacted and we"
            " cannot operate like this. Approximately 50 users affected.",
            "Something is wrong with the power or display infrastructure on floor 3. All monitors are flickering in "
            "sync every 5-10 seconds. It's causing headaches and some people are getting nauseous. We need facilities "
            "and IT to investigate immediately.",
        ],
        next_best_actions=[
            "Engage Facilities to check power distribution on the affected floor. Deploy temporary workstations on "
            "alternate floors for critical staff. Investigate electrical and display infrastructure.",
            "Coordinate with Facilities for power quality inspection on floor 3. Relocate critical trading operations "
            "to unaffected areas while investigating root cause.",
        ],
        remediation_steps=[
            [
                "Confirm scope — identify all affected areas and count of impacted users",
                "Coordinate with Facilities to inspect power distribution and UPS systems on the floor",
                "Test a known-good monitor with an isolated power source to rule out electrical issues",
                "Relocate critical personnel to unaffected floors if issue persists",
                "Engage electrician to inspect power circuits and grounding on the affected floor",
                "Once root cause is identified, implement fix and verify monitors are stable",
                "Communicate resolution to all affected users",
            ],
        ],
        tags=["widespread", "facilities", "business-critical"],
    ),
    # ------------------------------------------------------------------
    # P2 scenarios (~25%)
    # ------------------------------------------------------------------
    Scenario(
        scenario_id="hw-laptop-no-boot",
        category="Hardware & Peripherals",
        priority="P2",
        assigned_team="Endpoint Engineering",
        needs_escalation=False,
        missing_information=["device_info", "error_message", "timestamp"],
        subjects=[
            "Laptop won't boot — stuck on black screen",
            "Computer won't turn on this morning",
            "Laptop dead — power light blinks but no boot",
            "ThinkPad won't start, just shows blinking cursor",
        ],
        descriptions=[
            "My laptop (Lenovo ThinkPad T14s) won't boot this morning. When I press the power button the keyboard light"
            "s come on for a second, the fan spins up, then it goes back to a black screen. I've tried holding the powe"
            "r button for 30 seconds and plugging in the charger. Nothing works. I have a client presentation at 10 AM "
            "and all my slides are on this machine.",
            "Came in to the office, opened my laptop and it won't start. Screen stays completely black. The little LED "
            "next to the power button blinks three times and stops. I tried removing the charger and holding the power "
            "button but no luck.",
            "My Dell Latitude won't boot. I get the Dell logo, then a blue screen flashes for half a second, and it "
            "reboots into the same loop. This started after Windows pushed an update last night. I've tried booting "
            "into Safe Mode but can't get to the menu fast enough.",
        ],
        next_best_actions=[
            "Attempt hardware reset (battery disconnect procedure). If unsuccessful, schedule same-day device swap and "
            "recover data via USB boot media.",
            "Walk user through BIOS recovery steps. If device remains unbootable, dispatch replacement laptop and "
            "schedule data recovery.",
        ],
        remediation_steps=[
            [
                "Attempt hard reset — disconnect power, hold power button for 30 seconds",
                "If no change, attempt BIOS recovery using manufacturer key combination",
                "Try booting from USB recovery media to access repair options",
                "If boot loop is update-related, attempt rollback via Windows Recovery Environment",
                "If hardware failure confirmed, provision replacement laptop from spare inventory",
                "Recover user data from failed device via USB boot or disk extraction",
                "Re-image or dispose of failed device per asset management policy",
            ],
        ],
        tags=["boot-failure"],
    ),
    Scenario(
        scenario_id="hw-broken-screen",
        category="Hardware & Peripherals",
        priority="P2",
        assigned_team="Endpoint Engineering",
        needs_escalation=False,
        missing_information=["device_info", "screenshot_or_attachment", "business_impact"],
        subjects=[
            "Laptop screen cracked — can't work",
            "Dropped my laptop, screen is shattered",
            "Display cracked — need replacement urgently",
        ],
        descriptions=[
            "I accidentally knocked my laptop off my desk this morning and the screen is cracked from corner to corner."
            " There are colored lines across the display and I can barely read anything. I can still see it boots up, b"
            "ut I can't work like this. It's a Lenovo ThinkPad X1 Carbon, about 8 months old.",
            "My laptop screen got damaged in my bag during my commute — something must have pressed on it. There's a "
            "big spiderweb crack on the left side and the bottom third of the screen is just black. I tried connecting "
            "an external monitor at my desk and that works, but I travel for client meetings and need a proper fix.",
            "Cracked my display. Closed the lid on a pen that was sitting on the keyboard. Screen has dead spots and "
            "the touch layer keeps registering phantom taps. Usable with an external monitor for now but I need a "
            "repair or replacement scheduled.",
        ],
        next_best_actions=[
            "Provide loaner laptop or external monitor as temporary workaround. Schedule screen replacement through "
            "vendor warranty or internal repair.",
            "Issue temporary replacement device and submit hardware repair request. Check warranty status for screen "
            "replacement coverage.",
        ],
        remediation_steps=[
            [
                "Assess damage severity and confirm device model and warranty status",
                "Provide loaner laptop or external monitor as an immediate workaround",
                "Submit repair request to vendor if under warranty",
                "If out of warranty, evaluate repair cost vs. replacement",
                "Transfer user data and profile to loaner or replacement device",
                "Return repaired device to user and collect loaner",
            ],
        ],
        tags=["physical-damage"],
    ),
    Scenario(
        scenario_id="hw-conference-av",
        category="Hardware & Peripherals",
        priority="P2",
        assigned_team="Endpoint Engineering",
        needs_escalation=True,
        missing_information=["network_location", "environment_details", "affected_users"],
        subjects=[
            "Conference room AV not working — exec meeting in 30 min",
            "Boardroom display and speakers dead before important call",
            "Teams Room device offline — need AV fixed for all-hands",
        ],
        descriptions=[
            "The AV system in conference room 4B (Building A, 2nd floor) is completely unresponsive. The Poly display s"
            "ays 'No Signal', the ceiling speakers aren't producing sound, and the Teams Room touchpanel is stuck on a "
            "loading screen. We have an executive board meeting starting in 30 minutes with remote participants joining"
            " via Teams.",
            "Trying to set up for our quarterly all-hands in the large boardroom and nothing works. The projector won't"
            " turn on, the wireless presentation clicker isn't pairing, and the conference phone has no dial tone. 150 "
            "people are expecting this meeting to start at 2 PM. Please send someone NOW.",
            "Room 3A Teams Room device is showing a 'something went wrong' error and won't load the meeting calendar. "
            "The display shows a blue screen. Tried unplugging and replugging the Poly device — same result. We have a "
            "client demo in 45 minutes.",
        ],
        next_best_actions=[
            "Dispatch AV technician to the room immediately. Prepare backup room or laptop-based Teams meeting as "
            "contingency for the upcoming meeting.",
            "Send technician to reset Teams Room device and check display connections. Identify alternate room and "
            "brief meeting organizer on backup plan.",
        ],
        remediation_steps=[
            [
                "Dispatch AV technician to the conference room immediately",
                "Power-cycle the Teams Room device and all connected peripherals",
                "Check HDMI/USB-C cables and display input settings",
                "If Teams Room device is unrecoverable, connect a laptop directly to the display",
                "Test audio — speakers, microphones, and conference phone",
                "Confirm screen sharing and remote participant audio/video work",
                "If room cannot be restored in time, relocate meeting to backup room",
            ],
        ],
        tags=["meeting-critical", "av-equipment"],
    ),
    Scenario(
        scenario_id="hw-laptop-overheating",
        category="Hardware & Peripherals",
        priority="P2",
        assigned_team="Endpoint Engineering",
        needs_escalation=False,
        missing_information=["device_info", "environment_details", "reproduction_frequency"],
        subjects=[
            "Laptop extremely hot and fan running full blast",
            "Laptop overheating — shuts down randomly",
            "Fan noise unbearable and laptop burning hot",
        ],
        descriptions=[
            "My laptop has been running extremely hot for the past week. The fans are spinning at max speed constantly "
            "and the bottom of the machine is too hot to keep on my lap. It shut down on its own twice yesterday during"
            " video calls, presumably from overheating. This is a Dell Latitude 5530, about 18 months old.",
            "My ThinkPad is overheating badly. The area near the vent is burning hot and the fan sounds like a jet "
            "engine. It's been throttling so badly that Excel takes 20 seconds to respond. I cleaned the vents with "
            "compressed air but it made no difference. I think the thermal paste might need replacing.",
            "Laptop keeps shutting down without warning — I think it's overheating. The fan runs non-stop even when I'm"
            " just reading email. I've noticed it gets worse when I'm on Teams calls. Colleagues in my pod can hear the"
            " fan noise from their desks. It's a 2-year-old HP EliteBook.",
        ],
        next_best_actions=[
            "Schedule hardware inspection for thermal system. Provide loaner device if thermal shutdowns are causing "
            "data loss or work disruption.",
            "Run remote diagnostics to check CPU thermals and fan RPM. If temps exceed safe thresholds, schedule "
            "in-person hardware service.",
        ],
        remediation_steps=[
            [
                "Run hardware diagnostics remotely to check CPU temperature and fan RPM",
                "Check Task Manager for runaway processes consuming excessive CPU",
                "Verify BIOS and firmware are up to date for thermal management fixes",
                "Clean air vents and inspect fan for physical obstruction",
                "If thermal paste degradation suspected, schedule internal cleaning and reapplication",
                "If issue persists after servicing, replace device",
            ],
        ],
        tags=["thermal"],
    ),
    Scenario(
        scenario_id="hw-webcam-teams",
        category="Hardware & Peripherals",
        priority="P2",
        assigned_team="Endpoint Engineering",
        needs_escalation=False,
        missing_information=["device_info", "application_version", "steps_to_reproduce"],
        subjects=[
            "Webcam not working in Teams — just shows black",
            "Camera not detected in Microsoft Teams",
            "Teams video call shows blank screen on my end",
        ],
        descriptions=[
            "My built-in webcam stopped working in Microsoft Teams. When I start a video call, my preview shows a black"
            " screen with a line through the camera icon. Other people in the meeting can't see me. Tested it in the Wi"
            "ndows Camera app and that also shows a black screen. The camera worked fine last week. Lenovo ThinkPad T14"
            ", Windows 11.",
            "I can't get my webcam to work in Teams. The dropdown in video settings shows 'Integrated Camera' but the "
            "preview is just black. I have back-to-back client calls today and being on video is required per our "
            "client engagement policy. I've restarted Teams and my laptop — same issue.",
            "Webcam shows a black screen in every app — Teams, Zoom, Windows Camera. I checked Device Manager and "
            "there's a yellow triangle on the camera device. I tried uninstalling and reinstalling the driver but it "
            "came back with the same error. Privacy shutter is definitely open.",
        ],
        next_best_actions=[
            "Check privacy settings and camera drivers. If built-in camera is hardware-failed, provide USB webcam as "
            "interim solution.",
            "Reinstall camera driver via Device Manager and verify Windows privacy settings allow camera access. If "
            "unresolved, ship external USB webcam.",
        ],
        remediation_steps=[
            [
                "Verify the physical privacy shutter or switch is open",
                "Check Windows Settings > Privacy > Camera — ensure app access is allowed",
                "Reinstall the camera driver via Device Manager",
                "Update BIOS and chipset drivers from the manufacturer",
                "Test camera in the Windows Camera app to isolate from Teams",
                "If built-in camera is hardware-failed, provide a USB webcam as a workaround",
            ],
        ],
        tags=["video-conferencing"],
    ),
    Scenario(
        scenario_id="hw-desk-phone",
        category="Hardware & Peripherals",
        priority="P2",
        assigned_team="Endpoint Engineering",
        needs_escalation=False,
        missing_information=["device_info", "network_location", "error_message"],
        subjects=[
            "Desk phone not working — no dial tone",
            "Office phone is dead, can't make or receive calls",
            "VoIP desk phone won't register, screen says 'No Service'",
        ],
        descriptions=[
            "My desk phone (Poly VVX 450) has been completely dead since I arrived this morning. The screen is on but "
            "it says 'Registration Failed' and there's no dial tone when I pick up the handset. I've tried unplugging "
            "the ethernet cable and plugging it back in. I sit at desk 4A-217 on the VoIP network.",
            "My office phone stopped working. It was fine yesterday but today the display just shows 'Configuring' and "
            "never finishes booting. I can't make or receive calls, and I have an important client callback scheduled "
            "for 11 AM. Other phones on my floor seem to be working fine.",
            "No dial tone on my desk phone. Screen is lit but says 'No Service'. Tried a different ethernet cable, same"
            " result. The person next to me says their phone works fine, so I don't think it's a network-wide issue. I "
            "rely on this phone for client calls.",
        ],
        next_best_actions=[
            "Check phone provisioning in the PBX/call manager. Verify network port is active and VLAN is correctly "
            "configured for VoIP.",
            "Remotely reboot the phone from the call management platform. If registration fails, re-provision the "
            "device.",
        ],
        remediation_steps=[
            [
                "Verify the network port is active and assigned to the correct voice VLAN",
                "Check the phone's registration status in the call management platform",
                "Power-cycle the phone and allow it to re-register",
                "If registration fails, re-provision the phone's configuration",
                "Test with a known-good phone at the same port to isolate hardware vs. network",
                "If phone hardware is faulty, replace with spare unit from inventory",
            ],
        ],
        tags=["voip", "telephony"],
    ),
    # ------------------------------------------------------------------
    # P3 scenarios (~40%)
    # ------------------------------------------------------------------
    Scenario(
        scenario_id="hw-monitor-flicker",
        category="Hardware & Peripherals",
        priority="P3",
        assigned_team="Endpoint Engineering",
        needs_escalation=False,
        missing_information=["device_info", "steps_to_reproduce", "reproduction_frequency"],
        subjects=[
            "Monitor keeps flickering on and off",
            "External display flickering — giving me a headache",
            "Screen flickers when I open certain apps",
            "Monitor goes black for a second then comes back",
        ],
        descriptions=[
            "My external monitor (Dell U2722D) has been flickering intermittently for the past two days. It goes black "
            "for about a second, then comes back. Happens maybe once every 10-15 minutes. I've tried a different Displa"
            "yPort cable but the issue continues. It's more frequent when I'm on Teams calls with screen sharing.",
            "The display on my left monitor keeps cutting out randomly. Just goes black for a moment then returns. "
            "Started happening on Monday. Super distracting when I'm working on spreadsheets. It's a Dell 27-inch "
            "connected via the docking station.",
            "My monitor flickers like crazy whenever I open Excel or any app with a lot of white background. It's fine "
            "on dark-themed apps. I think it might be a refresh rate issue? It's a 2-year-old HP monitor connected with"
            " HDMI through my dock.",
        ],
        next_best_actions=[
            "Test with a different cable and direct laptop connection (bypass dock) to isolate the issue. Check display"
            " driver version.",
            "Swap monitor with a known-good unit to determine if the issue is the display or the output source.",
        ],
        remediation_steps=[
            [
                "Test with a different video cable (try DisplayPort and HDMI)",
                "Connect the monitor directly to the laptop, bypassing the docking station",
                "Update display drivers and docking station firmware",
                "Adjust refresh rate in Windows Display Settings to match monitor spec",
                "If flickering persists with direct connection, replace the monitor",
            ],
        ],
    ),
    Scenario(
        scenario_id="hw-dock-not-detected",
        category="Hardware & Peripherals",
        priority="P3",
        assigned_team="Endpoint Engineering",
        needs_escalation=False,
        missing_information=["device_info", "error_message"],
        subjects=[
            "Docking station not recognized when I plug in",
            "USB-C dock stopped working — no external monitors or peripherals",
            "Dock not detected — keyboard, mouse, monitors all dead",
        ],
        descriptions=[
            "My Lenovo ThinkPad USB-C dock stopped working this morning. When I plug in, Windows makes the connection "
            "sound but nothing happens — no external monitors, keyboard, or mouse. The dock's power light is on. I "
            "tried a different USB-C port on my laptop and rebooted, same result.",
            "Docking station isn't being recognized anymore. Plugging in does nothing — my two monitors stay in sleep "
            "mode and my wired peripherals don't respond. This is a Dell WD19TBS Thunderbolt dock. It was working fine "
            "on Friday, and now on Monday it's dead. No Windows updates happened over the weekend that I know of.",
            "My dock just stopped working out of nowhere. I came back from lunch, reconnected, and nothing. USB-C cable"
            " is seated properly, power adapter is plugged in. My laptop charges through the dock so at least power wor"
            "ks, but no video output and no USB peripherals. Already tried different cables.",
        ],
        next_best_actions=[
            "Update docking station firmware and Thunderbolt drivers. Test with a known-good dock"
            " to isolate the issue.",
            "Power-cycle the dock by unplugging power for 30 seconds. If unresolved, update dock firmware and "
            "USB-C/Thunderbolt drivers.",
        ],
        remediation_steps=[
            [
                "Power-cycle the dock — unplug power adapter for 30 seconds, then reconnect",
                "Check for docking station firmware updates from the manufacturer",
                "Update USB-C and Thunderbolt controller drivers on the laptop",
                "Test with an alternate dock to rule out hardware failure",
                "If dock is faulty, replace from spare inventory",
            ],
        ],
    ),
    Scenario(
        scenario_id="hw-keyboard-mouse-fail",
        category="Hardware & Peripherals",
        priority="P3",
        assigned_team="Endpoint Engineering",
        needs_escalation=False,
        missing_information=["device_info", "steps_to_reproduce"],
        subjects=[
            "Wireless keyboard and mouse stopped working",
            "Keyboard not responding — tried new batteries",
            "Wired USB mouse not detected, tried multiple ports",
            "Bluetooth keyboard keeps disconnecting",
        ],
        descriptions=[
            "My wireless Logitech keyboard and mouse combo stopped working this morning. I've replaced the batteries in"
            " both and re-inserted the USB receiver into different ports. The receiver's LED blinks like it's searching"
            " but never connects. The on-screen keyboard is my only option right now.",
            "My wired USB keyboard isn't being detected by my laptop. Tried three different USB ports — nothing. The "
            "keyboard works fine on my colleague's machine, so it's not the keyboard itself. Device Manager shows "
            "'Unknown USB Device' with a yellow warning icon.",
            "My Bluetooth mouse keeps disconnecting every few minutes. I have to toggle Bluetooth off and on to "
            "reconnect each time. It's been happening since the last Windows update. Using a Microsoft Surface "
            "Precision Mouse paired to my ThinkPad.",
        ],
        next_best_actions=[
            "Test peripherals on another machine to isolate hardware vs. driver issue. Check USB controller and "
            "Bluetooth drivers for recent updates.",
            "Uninstall and re-pair wireless devices. If USB, check Device Manager for driver conflicts and try a direct"
            " USB-A port.",
        ],
        remediation_steps=[
            [
                "Test the peripheral on another computer to confirm it works",
                "Try a different USB port — preferably a direct USB-A port, not through a hub",
                "Uninstall the device from Device Manager and re-detect",
                "For wireless devices, re-pair using the manufacturer's software",
                "Check for USB controller or Bluetooth driver updates",
                "If the device is confirmed faulty, issue a replacement",
            ],
        ],
    ),
    Scenario(
        scenario_id="hw-printer-jam-offline",
        category="Hardware & Peripherals",
        priority="P3",
        assigned_team="Endpoint Engineering",
        needs_escalation=False,
        missing_information=["device_info", "network_location"],
        subjects=[
            "Printer keeps jamming, paper stuck inside",
            "Floor printer showing offline — can't print anything",
            "Paper jam won't clear, printer makes grinding noise",
        ],
        descriptions=[
            "The HP LaserJet on the 4th floor near the kitchen keeps jamming. I've cleared the paper three times this "
            "morning but it jams again after a few pages. The paper tray is loaded correctly and I'm using standard "
            "letter size. Other people on my floor are having the same problem.",
            "Our floor printer (the one near room 4C-110) has been showing 'Offline' on everyone's computer since "
            "yesterday afternoon. I checked and it's powered on with no error on the display panel. I tried restarting "
            "it and it briefly showed 'Ready' then went back to 'Offline'.",
            "The printer on floor 3 is making a terrible grinding noise when it tries to print and keeps jamming. I pul"
            "led out torn paper from the back tray but I think there's a piece stuck deep inside that I can't reach. Pr"
            "int jobs from the whole floor are backing up.",
        ],
        next_best_actions=[
            "Clear the jam using manufacturer guidelines for the specific model. If paper is stuck deep inside, "
            "schedule vendor maintenance visit.",
            "For offline status, check network connectivity and print spooler. For persistent jams, inspect rollers and"
            " schedule maintenance.",
        ],
        remediation_steps=[
            [
                "Open all paper path access doors and carefully remove any jammed paper",
                "Inspect feed rollers for worn or debris-coated surfaces",
                "For offline issues, verify network cable and print the network config page",
                "Restart the print spooler service on the print server",
                "Clear backed-up print jobs from the queue",
                "If rollers are worn or jam persists, schedule vendor maintenance",
            ],
        ],
    ),
    Scenario(
        scenario_id="hw-network-printer",
        category="Hardware & Peripherals",
        priority="P3",
        assigned_team="Endpoint Engineering",
        needs_escalation=False,
        missing_information=["device_info", "network_location", "error_message"],
        subjects=[
            "Can't print to the network printer — jobs just disappear",
            "Network printer not showing up on my laptop",
            "Print jobs stuck in queue, never reach the printer",
        ],
        descriptions=[
            "I can't print to the 5th floor network printer anymore. When I hit Print, the job appears in the queue for"
            " a moment then vanishes — nothing ever comes out of the printer. Other people can print to it fine. I've t"
            "ried removing and re-adding the printer but it fails with 'Windows cannot connect to the printer — access "
            "denied.'",
            "The network printer that used to be in my printer list has disappeared after a Windows update last week. I"
            " tried adding it back via Settings but it can't find any printers. I know the printer IP is 10.20.5.44 but"
            " adding by IP gives me a 'driver not found' error.",
            "My print jobs get stuck in the queue and never actually print. The status just says 'Sending to printer' "
            "forever. Cancelling and retrying doesn't help. Restarted my laptop and the print spooler — same issue. "
            "This is only happening to me; my deskmate can print just fine.",
        ],
        next_best_actions=[
            "Clear local print spooler, remove and re-add the printer using the correct driver. Check print server "
            "permissions for the user account.",
            "Verify user has permissions on the print server. Reinstall the printer driver and test connectivity to "
            "printer IP.",
        ],
        remediation_steps=[
            [
                "Clear the local print spooler — stop the service, delete pending jobs, restart",
                "Remove the printer from the user's device",
                "Verify network connectivity to the printer IP address via ping",
                "Re-add the printer using the correct print server path or IP",
                "Install the correct print driver if missing",
                "Test with a print test page and confirm output",
            ],
        ],
    ),
    Scenario(
        scenario_id="hw-battery-degraded",
        category="Hardware & Peripherals",
        priority="P3",
        assigned_team="Endpoint Engineering",
        needs_escalation=False,
        missing_information=["device_info", "business_impact"],
        subjects=[
            "Laptop battery dies after 45 minutes unplugged",
            "Battery won't hold a charge — need to stay plugged in",
            "Laptop battery degraded, barely lasts an hour",
        ],
        descriptions=[
            "My laptop battery has degraded to the point where it only lasts about 45 minutes off the charger. I travel"
            " to client sites twice a week and there isn't always a power outlet available. It used to last 6-7 hours. "
            "The laptop is a ThinkPad T14s, about 2.5 years old. Battery health in Lenovo Vantage shows 38% design capa"
            "city.",
            "My Dell Latitude's battery is basically useless. If I unplug for even 30 minutes it dies. I have to carry "
            "my power adapter everywhere and pray there's an outlet. I'm in meeting rooms most of the day and this is "
            "really impacting my productivity.",
            "Battery health is shot on my laptop. Goes from 100% to 0% in about an hour with light use. Windows even sh"
            "ows a notification saying 'Consider replacing your battery.' Is this something IT can fix or do I need a w"
            "hole new machine?",
        ],
        next_best_actions=[
            "Run battery diagnostics to confirm capacity. If below 50% design capacity, schedule battery replacement or"
            " device refresh.",
            "Check battery health report via powercfg. Order replacement battery if under warranty or schedule device "
            "replacement if not serviceable.",
        ],
        remediation_steps=[
            [
                "Generate a battery health report using 'powercfg /batteryreport'",
                "Review current battery capacity vs. design capacity",
                "If capacity is below 50%, submit battery replacement request",
                "Check warranty status — replace under warranty if eligible",
                "If battery is non-replaceable, evaluate device for refresh cycle",
                "Provide a portable charger or extended power adapter as interim workaround",
            ],
        ],
    ),
    Scenario(
        scenario_id="hw-usbc-hub-incompatible",
        category="Hardware & Peripherals",
        priority="P3",
        assigned_team="Endpoint Engineering",
        needs_escalation=False,
        missing_information=["device_info", "configuration_details"],
        subjects=[
            "USB-C hub not working with my laptop",
            "New USB-C adapter won't pass video to my monitor",
            "USB-C hub only charges but doesn't connect peripherals",
        ],
        descriptions=[
            "I bought a USB-C hub from Amazon to use with my work laptop (HP EliteBook 840 G9) but it's not working "
            "properly. It charges the laptop but the HDMI output doesn't produce any video signal and the USB-A ports "
            "on the hub aren't recognized. The hub works fine with my personal MacBook.",
            "The USB-C multiport adapter I was given doesn't seem compatible with my laptop. The ethernet port works "
            "but the two monitor outputs (HDMI + DP) only show one display. My Lenovo dock handled both monitors fine. "
            "IT gave me this adapter because they ran out of docks.",
            "Got a new USB-C to HDMI adapter and it's completely incompatible. My laptop detects 'something' plugged in"
            " but no video output. I've tried different HDMI cables and monitors. The adapter works on other laptops so"
            " it seems like a compatibility issue with my specific model.",
        ],
        next_best_actions=[
            "Verify the hub supports the laptop's USB-C/Thunderbolt specification. Check if an approved hub model is "
            "available from IT inventory.",
            "Confirm DisplayPort Alt Mode support on the laptop port. If personal hub is incompatible, issue a "
            "company-approved docking solution.",
        ],
        remediation_steps=[
            [
                "Check laptop USB-C port capabilities — Thunderbolt vs. USB 3.x vs. charging only",
                "Verify hub specifications match port capabilities (DisplayPort Alt Mode, power delivery)",
                "Update USB-C and Thunderbolt drivers on the laptop",
                "Test with a company-approved hub or dock from the supported hardware list",
                "If personal hub is incompatible, issue a supported docking station from IT inventory",
            ],
        ],
    ),
    Scenario(
        scenario_id="hw-bluetooth-headset",
        category="Hardware & Peripherals",
        priority="P3",
        assigned_team="Endpoint Engineering",
        needs_escalation=False,
        missing_information=["device_info", "application_version"],
        subjects=[
            "Bluetooth headset won't pair with my laptop",
            "Headset connects via Bluetooth but no audio in Teams",
            "Bluetooth headset paired but keeps dropping connection",
        ],
        descriptions=[
            "I can't pair my Jabra Evolve2 75 headset with my work laptop. It shows up in Bluetooth settings as 'Jabra "
            "Evolve2 75' but when I click Connect, it says 'Connection failed' every time. The headset pairs fine with "
            "my phone. Laptop is a Dell Latitude 5540 running Windows 11.",
            "My Bluetooth headset is paired and shows as 'Connected' in Windows, but when I join a Teams call, Teams "
            "doesn't list it as an audio device. I have to use laptop speakers. If I go to Sound Settings, I can see "
            "the headset but it says 'Driver error'. Tried removing and re-pairing — same result.",
            "Headset pairs OK but keeps disconnecting mid-call. Every 10-15 minutes during a Teams meeting, the audio c"
            "uts out and switches to laptop speakers. I have to manually switch back. Super embarrassing during client "
            "calls. Using a Sony WH-1000XM5 with Bluetooth.",
        ],
        next_best_actions=[
            "Remove the headset pairing, restart Bluetooth service, and re-pair. Update Bluetooth drivers and headset "
            "firmware.",
            "Check for Bluetooth driver updates and headset firmware. If issues persist, test with the headset's USB "
            "dongle as a workaround.",
        ],
        remediation_steps=[
            [
                "Remove the headset from Bluetooth paired devices",
                "Restart the Bluetooth Support Service in Windows Services",
                "Update Bluetooth adapter drivers from the laptop manufacturer",
                "Update headset firmware via the manufacturer's app (Jabra Direct, Sony Connect, etc.)",
                "Re-pair the headset and set it as the default audio device in Sound Settings",
                "If Bluetooth remains unreliable, use the headset's USB dongle adapter instead",
            ],
        ],
    ),
    Scenario(
        scenario_id="hw-trackpad-erratic",
        category="Hardware & Peripherals",
        priority="P3",
        assigned_team="Endpoint Engineering",
        needs_escalation=False,
        missing_information=["device_info", "steps_to_reproduce", "timestamp"],
        subjects=[
            "Trackpad acting erratic after Windows update",
            "Touchpad jumps around randomly, cursor has a mind of its own",
            "Laptop trackpad sensitivity all wrong since update",
        ],
        descriptions=[
            "Ever since the Windows update that installed last night, my laptop trackpad has been acting insane. The cu"
            "rsor jumps around randomly, tap-to-click keeps triggering when I'm just resting my palm, and two-finger sc"
            "roll goes in the opposite direction. I've checked Settings and everything looks normal. ThinkPad T14 Gen 3"
            ".",
            "My touchpad is basically unusable after the latest update. The cursor moves erratically — sometimes it "
            "teleports across the screen, sometimes it doesn't move at all. Palm rejection isn't working and I keep "
            "accidentally clicking things. Using an external mouse as a workaround but I need the trackpad for travel.",
            "Trackpad on my Dell Latitude started going haywire on Tuesday. Random ghost taps, the cursor drifts to the"
            " upper-right corner on its own, and pinch-to-zoom stopped working. I rolled back the touchpad driver but i"
            "t auto-updated back to the broken version.",
        ],
        next_best_actions=[
            "Roll back the touchpad driver to the previous version and pause Windows Update for the driver. Check for a"
            " known issue with the current driver.",
            "Reinstall the touchpad driver from the manufacturer's website. Adjust sensitivity settings and disable "
            "palm rejection temporarily to test.",
        ],
        remediation_steps=[
            [
                "Roll back the touchpad driver to the previous version via Device Manager",
                "If rollback resolves the issue, pause automatic driver updates for this device",
                "Download and install the latest stable touchpad driver from the manufacturer",
                "Reset touchpad settings to defaults in Windows Settings > Touchpad",
                "If the issue persists, test in Safe Mode to rule out third-party software conflict",
            ],
        ],
        tags=["post-update"],
    ),
    Scenario(
        scenario_id="hw-external-display-hdmi",
        category="Hardware & Peripherals",
        priority="P3",
        assigned_team="Endpoint Engineering",
        needs_escalation=False,
        missing_information=["device_info", "configuration_details"],
        subjects=[
            "External monitor not detected via HDMI",
            "HDMI output not working — monitor says 'No Signal'",
            "Can't get external display working with HDMI cable",
        ],
        descriptions=[
            "I connected my external monitor via HDMI but it just says 'No Signal'. I've tried the HDMI port directly "
            "on my laptop and through my dock — same result. The monitor works fine with my personal laptop using the "
            "same cable. Windows doesn't even detect a second display when I go to Display Settings.",
            "Just got a new monitor for my home office and I can't get it to work with my work laptop. HDMI cable is "
            "brand new, tried two different ones. The monitor briefly flashes the HP logo when I plug in the cable but "
            "then goes back to 'No Signal'. My laptop is a Lenovo ThinkPad with Windows 11.",
            "My HDMI output stopped working. Used to have a second monitor connected just fine, but now nothing. Tried "
            "Win+P and cycled through all display modes. The display settings only show my laptop screen. No recent "
            "hardware changes — just the usual Windows updates.",
        ],
        next_best_actions=[
            "Check display drivers and test with a different cable type (DisplayPort or USB-C to HDMI). Try Win+P to "
            "switch display mode.",
            "Update graphics drivers and test HDMI output with a known-good monitor to isolate the port vs. cable vs. "
            "driver issue.",
        ],
        remediation_steps=[
            [
                "Try Win+P and select 'Extend' or 'Duplicate' to force output detection",
                "Test with a different cable (DisplayPort or USB-C to HDMI adapter)",
                "Update the display/graphics driver from the laptop manufacturer's site",
                "Check if HDMI output is disabled in BIOS/UEFI settings",
                "Test the same HDMI port with a different monitor to isolate hardware failure",
                "If the port is confirmed dead, use USB-C or dock for display output",
            ],
        ],
    ),
    Scenario(
        scenario_id="hw-barcode-scanner",
        category="Hardware & Peripherals",
        priority="P3",
        assigned_team="Endpoint Engineering",
        needs_escalation=False,
        missing_information=["device_info", "environment_details", "error_message"],
        subjects=[
            "Barcode scanner not reading barcodes in warehouse app",
            "Handheld scanner won't connect to inventory system",
            "Warehouse barcode scanner keeps misreading labels",
        ],
        descriptions=[
            "The barcode scanner at warehouse station 3 has stopped reading barcodes properly. It scans but the data co"
            "mes through garbled in our inventory management app — random characters instead of the actual barcode numb"
            "ers. We've cleaned the lens and tried different barcodes. It's a Zebra DS3608 connected via USB to the war"
            "ehouse workstation.",
            "Our handheld barcode scanner won't connect to the warehouse workstation anymore. When I plug in the USB ca"
            "ble nothing happens — no beep, no light, nothing. Tried different USB ports and cables. We have incoming s"
            "hipments stacking up and can't process them without the scanner.",
            "The barcode scanner at receiving dock B is misreading labels about 50% of the time. It scans successfully "
            "(we hear the beep) but the wrong item numbers appear in the system. We've been catching errors manually bu"
            "t some bad data probably slipped through. This started after the scanner firmware was updated last week.",
        ],
        next_best_actions=[
            "Check scanner configuration and symbology settings. If firmware update caused the issue, roll back to "
            "previous firmware version.",
            "Test scanner with a barcode validation tool. Verify USB connection and scanner programming matches the "
            "inventory application requirements.",
        ],
        remediation_steps=[
            [
                "Verify USB connectivity — test the scanner on a different workstation",
                "Check scanner symbology configuration matches barcode format used in warehouse",
                "If garbled output, reset scanner to factory defaults and reconfigure",
                "If firmware update caused issues, roll back to the previous firmware version",
                "Test with known-good barcodes to verify accuracy",
                "If hardware is faulty, replace with spare scanner from inventory",
            ],
        ],
        tags=["warehouse", "specialized-hardware"],
    ),
    # ------------------------------------------------------------------
    # P4 scenarios (~25%)
    # ------------------------------------------------------------------
    Scenario(
        scenario_id="hw-ergonomic-request",
        category="Hardware & Peripherals",
        priority="P4",
        assigned_team="Endpoint Engineering",
        needs_escalation=False,
        missing_information=["business_impact", "configuration_details"],
        subjects=[
            "Request for standing desk and ergonomic equipment",
            "Need ergonomic keyboard and mouse — wrist pain",
            "Standing desk converter request for my workstation",
        ],
        descriptions=[
            "I'd like to request a standing desk or a sit-stand converter for my workstation. I've been having lower "
            "back pain from sitting all day and my doctor recommended alternating between sitting and standing. I'm on "
            "floor 3, desk 3B-205. I'd also appreciate an ergonomic keyboard if available.",
            "Can I get an ergonomic keyboard and vertical mouse? I'm starting to get wrist pain from the standard "
            "equipment. My manager approved the request — I can forward the email if needed. I sit in the open floor "
            "plan on the 2nd floor.",
            "I need to request ergonomic equipment. I have a note from my doctor recommending a sit-stand desk, an "
            "ergonomic chair with lumbar support, and a monitor arm to adjust screen height. Desk location is 5A-112. "
            "Happy to do whatever approval process is needed.",
        ],
        next_best_actions=[
            "Submit ergonomic equipment request through the procurement portal. If medical accommodation, route through"
            " HR for expedited approval.",
            "Log the equipment request and check current inventory for available ergonomic equipment. If medical need, "
            "coordinate with HR.",
        ],
        remediation_steps=[
            [
                "Confirm specific equipment requested and desk location",
                "Check if request qualifies as medical accommodation (doctor's note)",
                "If medical, route through HR for expedited approval and procurement",
                "If standard request, submit through IT equipment procurement portal",
                "Schedule delivery and installation once equipment arrives",
                "Follow up to ensure equipment meets user's needs",
            ],
        ],
        tags=["procurement", "ergonomic"],
    ),
    Scenario(
        scenario_id="hw-new-equipment-remote",
        category="Hardware & Peripherals",
        priority="P4",
        assigned_team="Endpoint Engineering",
        needs_escalation=False,
        missing_information=["configuration_details", "contact_info", "business_impact"],
        subjects=[
            "New equipment request for remote worker setup",
            "Need monitor, keyboard, and dock shipped to home office",
            "Remote work equipment request — just went fully remote",
        ],
        descriptions=[
            "I've been approved for full-time remote work starting next month and I need to set up a proper home office"
            ". Can IT ship me an external monitor, keyboard, mouse, and a docking station? My manager (Sarah Chen) has "
            "already approved the budget. My shipping address is different from what's in the system — I just moved.",
            "I'm a new hire starting Monday and I'll be fully remote. My manager said IT would ship my equipment but I "
            "haven't heard anything yet. I need a laptop, monitor, dock, keyboard, and mouse. Can someone confirm "
            "what's being sent and when it'll arrive?",
            "Requesting a second monitor for my home office. I currently have a laptop and one monitor but my work "
            "requires dual screens for financial modeling. I'd also appreciate a laptop stand and webcam if available. "
            "Happy to pick up from the office if shipping is complicated.",
        ],
        next_best_actions=[
            "Verify manager approval and confirm equipment list. Process shipping request with updated address and "
            "provide tracking information.",
            "Check available inventory for requested items. Coordinate shipping to remote address and send setup "
            "instructions.",
        ],
        remediation_steps=[
            [
                "Confirm equipment list and verify manager approval",
                "Check IT inventory for available items",
                "Verify shipping address with the user",
                "Package and ship equipment with setup instructions",
                "Provide tracking number and estimated delivery date",
                "Schedule a remote setup session to assist with configuration",
            ],
        ],
        tags=["procurement", "remote-work"],
    ),
    Scenario(
        scenario_id="hw-keyboard-spill",
        category="Hardware & Peripherals",
        priority="P3",
        assigned_team="Endpoint Engineering",
        needs_escalation=False,
        missing_information=["device_info", "timestamp"],
        subjects=[
            "Spilled coffee on my keyboard — keys are sticking",
            "Liquid spill on laptop keyboard — some keys don't work",
            "Keyboard damaged after drink spill",
        ],
        descriptions=[
            "I accidentally spilled coffee on my laptop keyboard about 20 minutes ago. I immediately flipped it upside "
            "down and dried it with paper towels. The laptop still works but the keys on the right side are sticky and "
            "the 'O' and 'P' keys don't register at all. Should I keep using it or will it get worse?",
            "Spilled water on my external keyboard. Unplugged it right away and dried it off. Most keys work but the "
            "space bar is sticky and the Enter key only works if I press it really hard. It's the standard Dell "
            "keyboard that came with my docking station setup.",
            "My colleague knocked a cup of tea onto my laptop. I powered it off immediately. After drying it for an "
            "hour, I turned it back on and the screen works but the keyboard is acting weird — typing 'a' produces "
            "'asd' and several keys are unresponsive. The trackpad seems fine though.",
        ],
        next_best_actions=[
            "For laptop spills, advise user to power off immediately and bring in for assessment. Provide an external "
            "keyboard as workaround. For external keyboards, replace immediately.",
            "If laptop keyboard, schedule same-day inspection to prevent corrosion damage to internal components. Issue"
            " external keyboard in the meantime.",
        ],
        remediation_steps=[
            [
                "If laptop — advise user to power off immediately to prevent short-circuit damage",
                "Provide an external USB keyboard as an immediate workaround",
                "Schedule same-day inspection by a technician to assess internal damage",
                "If external keyboard, replace with a spare from inventory",
                "For laptops, disassemble and clean affected components if possible",
                "If internal damage is extensive, submit warranty claim or schedule device replacement",
            ],
        ],
        tags=["liquid-damage"],
    ),
    Scenario(
        scenario_id="hw-laptop-fan-noise",
        category="Hardware & Peripherals",
        priority="P4",
        assigned_team="Endpoint Engineering",
        needs_escalation=False,
        missing_information=["device_info", "reproduction_frequency", "environment_details"],
        subjects=[
            "Laptop fan is rattling — annoying noise",
            "Fan makes grinding noise intermittently",
            "Loud buzzing from laptop fan, getting worse",
        ],
        descriptions=[
            "My laptop fan has developed a rattling noise over the past week. It's not constant — mostly when the CPU "
            "is under load like during video calls or when running reports. It's loud enough that colleagues in my pod "
            "have mentioned it. Not overheating though, just noisy. HP EliteBook 845 G9.",
            "There's a buzzing/grinding sound coming from my laptop fan. Started about a month ago and it's getting "
            "progressively louder. It goes away when I tilt the laptop at an angle, which makes me think a bearing is "
            "going bad. No thermal issues yet but I'd like to get it fixed before it fails completely.",
            "My laptop's fan has been making an intermittent clicking sound. It comes and goes randomly — sometimes fin"
            "e for hours, other times it clicks for 30 minutes straight. Not loud enough to be an emergency but it's dr"
            "iving me nuts in our quiet office area.",
        ],
        next_best_actions=[
            "Schedule hardware inspection to evaluate fan condition. If bearing is failing, schedule fan replacement "
            "before thermal failure occurs.",
            "Run hardware diagnostics to check fan RPM patterns. Schedule preventive maintenance to clean or replace "
            "the fan.",
        ],
        remediation_steps=[
            [
                "Run hardware diagnostics to verify fan functionality and RPM",
                "Clean air vents and inspect fan for debris or obstruction",
                "If fan bearing is failing, schedule fan replacement",
                "Update BIOS for improved fan curve and thermal management",
                "If noise is tolerable and thermals are fine, monitor and schedule replacement proactively",
            ],
        ],
    ),
    Scenario(
        scenario_id="hw-monitor-arm-request",
        category="Hardware & Peripherals",
        priority="P4",
        assigned_team="Endpoint Engineering",
        needs_escalation=False,
        missing_information=["configuration_details", "network_location"],
        subjects=[
            "Request for dual monitor arm mount",
            "Need a monitor arm for my new desk setup",
            "Monitor stand too low — requesting adjustable arm",
        ],
        descriptions=[
            "I'd like to request a dual monitor arm for my desk. I have two 27-inch monitors and the stock stands take "
            "up too much desk space. A clamp-on arm would free up room for documents and my notepad. Desk is 5A-302, "
            "and the desk edge is about 2 inches thick if that matters for the clamp.",
            "My monitor is way too low on its built-in stand and I'm getting neck pain from looking down all day. Could"
            " I get an adjustable monitor arm so I can raise it to eye level? Single monitor, 24-inch Dell. I'm at desk"
            " 2B-108.",
            "Requesting a monitor arm mount. I just moved to a new desk and the monitor stand doesn't fit well with the"
            " desk layout. An adjustable arm would let me position the screen properly. No rush — whenever it's conveni"
            "ent.",
        ],
        next_best_actions=[
            "Submit equipment request through procurement portal. Check if monitor VESA mount is compatible with "
            "standard arms.",
            "Verify monitor has VESA mounting holes and order compatible arm from approved equipment list.",
        ],
        remediation_steps=[
            [
                "Verify monitor model supports VESA mounting (75x75 or 100x100)",
                "Check desk edge thickness and material for clamp compatibility",
                "Submit procurement request for the appropriate arm model",
                "Schedule installation once the arm arrives",
                "Verify ergonomic positioning after installation",
            ],
        ],
        tags=["procurement", "ergonomic"],
    ),
    Scenario(
        scenario_id="hw-printer-toner-low",
        category="Hardware & Peripherals",
        priority="P4",
        assigned_team="Endpoint Engineering",
        needs_escalation=False,
        missing_information=["device_info", "network_location"],
        subjects=[
            "Printer toner is low — prints are faded",
            "Floor printer running out of toner, prints barely readable",
            "Need toner replacement for 3rd floor printer",
        ],
        descriptions=[
            "The printer on the 3rd floor (near room 3A-105) is running low on toner. Prints are coming out very faded "
            "and streaky. I shook the cartridge like someone suggested and it helped for a few pages but it's bad "
            "again. We print a lot of client reports from this printer so it gets heavy use.",
            "Prints from the 5th floor HP LaserJet are barely readable — super light and faded. The printer display "
            "says 'Toner Low' but it's been saying that for a week and it's getting worse. Can we get a replacement "
            "cartridge?",
            "The printer toner on our floor is basically empty. Everything comes out with white streaks across the "
            "page. I reprinted a 30-page report three times before giving up. Can someone replace the toner cartridge? "
            "The printer is the big one next to the break room on floor 2.",
        ],
        next_best_actions=[
            "Identify the printer model and order the correct toner cartridge. If a spare is in stock, dispatch for "
            "replacement.",
            "Check supply closet for matching toner cartridge. If not in stock, order replacement and advise user of "
            "alternate printer in the meantime.",
        ],
        remediation_steps=[
            [
                "Identify the printer model and required toner cartridge part number",
                "Check local supply closet or IT stockroom for a matching cartridge",
                "If available, replace the toner cartridge and run a test print",
                "If not in stock, order replacement and advise user of the nearest alternate printer",
                "Reset the toner counter on the printer after replacement",
            ],
        ],
        tags=["consumables"],
    ),
    Scenario(
        scenario_id="hw-second-monitor-setup",
        category="Hardware & Peripherals",
        priority="P4",
        assigned_team="Endpoint Engineering",
        needs_escalation=False,
        missing_information=["device_info", "configuration_details"],
        subjects=[
            "Help setting up a second monitor at my desk",
            "Can't figure out dual monitor configuration",
            "Second monitor shows duplicate instead of extended desktop",
        ],
        descriptions=[
            "I received a second monitor for my desk but I can't figure out how to set it up as an extended display. Ri"
            "ght now both screens show the same thing (mirrored). I want to be able to drag windows between them. The n"
            "ew monitor is connected via HDMI through my docking station. Not super tech-savvy so step-by-step instruct"
            "ions would be great.",
            "IT dropped off a second monitor but didn't set it up. I plugged it in and it powers on but my laptop "
            "doesn't seem to detect it. There's a DP cable and an HDMI cable — not sure which one to use. The dock has "
            "both ports. Would appreciate someone walking me through this.",
            "I have two monitors connected but Windows put them in the wrong order. When I move my mouse to the right, "
            "it goes to the left monitor. I tried swapping the cables but that didn't help. Also, the resolution on the"
            " new monitor looks blurry. Could use some help with display settings.",
        ],
        next_best_actions=[
            "Guide user through Windows Display Settings to configure extended desktop, arrange monitor positions, and "
            "adjust resolution.",
            "Remote in to configure display layout, set correct resolution for each monitor, and set display "
            "arrangement to match physical positions.",
        ],
        remediation_steps=[
            [
                "Open Windows Settings > Display and verify both monitors are detected",
                "Click 'Extend these displays' in the Multiple Displays dropdown",
                "Drag monitor icons to match the physical left-right arrangement",
                "Set each monitor to its native resolution for best clarity",
                "Confirm the user can drag windows between screens as expected",
            ],
        ],
    ),
]

