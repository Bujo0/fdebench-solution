# Copyright (c) Microsoft. All rights reserved.
"""Hardware & Peripherals scenario templates.

Covers: laptop failures, desktop issues, mobile devices, printers,
peripherals (headsets/webcams/mice), docking stations, blue screens,
monitor issues, BIOS/firmware, and hardware refresh requests.
"""

from ms.evals.constants import Category
from ms.evals.constants import MissingInfo
from ms.evals.constants import Priority
from ms.evals.constants import Team
from ms.evals.models import ScenarioTemplate
from ms.evals.scenarios.registry import register

# ---------------------------------------------------------------------------
# hw-001  Laptop battery failing / swelling
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="hw-001",
        category=Category.HARDWARE,
        priority=Priority.P2,
        assigned_team=Team.ENDPOINT,
        needs_escalation=True,
        missing_information=[
            MissingInfo.DEVICE_INFO,
            MissingInfo.TIMESTAMP,
        ],
        subjects=[
            "Laptop battery is swelling — trackpad is popping up",
            "Battery bulging on my laptop, urgent safety concern",
        ],
        descriptions=[
            "My laptop's trackpad has started to lift up and it won't sit flat on my desk anymore. "
            "I looked it up online and I think the battery is swelling. The bottom case is visibly "
            "warped. I'm in the NYC office, 15th floor. Should I keep using it? I'm worried it "
            "might be a fire hazard.",
            "Something is wrong with my laptop battery. The bottom of the machine is bulging out and "
            "the trackpad barely clicks anymore. A colleague said this could be dangerous. Please advise "
            "ASAP — I have client deliverables due this week and need a working machine.",
        ],
        next_best_actions=[
            "Instruct the user to power off the laptop immediately and not charge it. Arrange a "
            "loaner device and schedule safe battery disposal through the facilities team.",
            "Escalate as a safety issue — have the user disconnect power and move the device away "
            "from flammable materials. Dispatch a technician with a loaner laptop.",
        ],
        remediation_steps=[
            [
                "Contact user immediately and instruct them to power off the laptop",
                "Advise user to unplug the charger and not attempt to use the device",
                "Coordinate with facilities for safe handling and disposal of the swollen battery",
                "Provision a loaner laptop from the NYC spare pool and enroll it in Intune",
                "Create an asset disposal ticket referencing the original hardware asset tag",
                "Follow up to confirm replacement device is working and data has been restored",
            ],
            [
                "Instruct user to stop using the laptop immediately for safety reasons",
                "Dispatch an endpoint technician to collect the device from user's desk",
                "Issue a replacement laptop from inventory and configure via Autopilot",
                "Transfer user profile data from OneDrive/backup to the new device",
                "Decommission the faulty unit and update the CMDB asset record",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# hw-002  Blue screen crashes (BSOD)
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="hw-002",
        category=Category.HARDWARE,
        priority=Priority.P3,
        assigned_team=Team.ENDPOINT,
        needs_escalation=False,
        missing_information=[
            MissingInfo.ERROR_MESSAGE,
            MissingInfo.REPRODUCTION_FREQUENCY,
            MissingInfo.DEVICE_INFO,
        ],
        subjects=[
            "Laptop keeps blue-screening — lost work twice today",
            "Recurring BSOD on my ThinkPad, need help",
            "Blue screen of death every few hours",
        ],
        descriptions=[
            "My laptop has blue-screened three times this week. It always seems to happen when I have "
            "Teams, Outlook, and a few Excel files open. I didn't catch the error code — it reboots "
            "too fast. I'm in the London office, Risk Analytics team.",
            "Getting random BSODs on my work laptop. No pattern that I can see. It happened once during "
            "a client call which was really embarrassing. I don't know the stop code. Can someone look "
            "into this? It's a company-issued laptop, maybe two years old.",
        ],
        next_best_actions=[
            "Collect the BSOD stop code from Windows Event Viewer or the minidump files. Check if "
            "the device has pending driver or firmware updates in Intune.",
            "Pull crash dump logs remotely via Intune and analyze the stop code. Check for known "
            "driver compatibility issues with the latest Windows update.",
        ],
        remediation_steps=[
            [
                "Connect to the device remotely and retrieve minidump files from C:\\Windows\\Minidump",
                "Analyze crash dumps using WinDbg to identify the faulting driver or module",
                "Check Intune for pending driver and firmware updates for this hardware model",
                "Apply any outstanding updates and verify system file integrity with sfc /scannow",
                "Monitor for 48 hours and if BSODs recur, schedule hardware diagnostics",
            ],
            [
                "Review Windows Event Viewer for critical errors around the BSOD timestamps",
                "Run hardware diagnostics (memory test, disk check) remotely via Intune",
                "Check if the device is on the latest BIOS and chipset drivers",
                "If memory or disk errors are found, schedule a hardware replacement",
                "If software-related, re-image the device and restore user data from OneDrive",
                "Follow up with user after 72 hours to confirm stability",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# hw-003  Broken laptop screen
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="hw-003",
        category=Category.HARDWARE,
        priority=Priority.P3,
        assigned_team=Team.ENDPOINT,
        needs_escalation=False,
        missing_information=[
            MissingInfo.DEVICE_INFO,
            MissingInfo.SCREENSHOT_OR_ATTACHMENT,
        ],
        subjects=[
            "Cracked laptop screen — can barely see anything",
            "Laptop display is broken, need repair or replacement",
        ],
        descriptions=[
            "I dropped my laptop bag this morning and now the screen has a big crack across it. I can "
            "sort of see things through the cracks but it's unusable for any real work. I'm in the "
            "Singapore office. Is there a way to get a loaner while mine is being fixed?",
            "My laptop screen is shattered. Not sure how it happened — I opened it this morning and "
            "the display was cracked from corner to corner. I need a working machine urgently, I have "
            "a presentation to the board on Thursday.",
        ],
        next_best_actions=[
            "Provide a loaner laptop from the Singapore office spare pool and submit a warranty "
            "repair request for the damaged screen.",
            "Arrange an external monitor as an immediate workaround and initiate the screen "
            "replacement process through the hardware vendor.",
        ],
        remediation_steps=[
            [
                "Issue a loaner laptop from the local office spare inventory",
                "Enroll the loaner in Intune via Autopilot for the user's profile",
                "Submit a warranty or repair ticket with the hardware vendor for screen replacement",
                "Once repaired, re-image if necessary and return the original device to the user",
                "Collect and re-inventory the loaner laptop",
            ],
            [
                "Provide an external monitor as an immediate workaround if a loaner is unavailable",
                "Document the damage with photos and create an asset repair ticket",
                "Check warranty status and initiate repair or replacement accordingly",
                "Migrate user to the repaired or replacement device and verify functionality",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# hw-004  Docking station not recognizing monitors
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="hw-004",
        category=Category.HARDWARE,
        priority=Priority.P3,
        assigned_team=Team.ENDPOINT,
        needs_escalation=False,
        missing_information=[
            MissingInfo.DEVICE_INFO,
            MissingInfo.CONFIGURATION_DETAILS,
            MissingInfo.STEPS_TO_REPRODUCE,
        ],
        subjects=[
            "Docking station won't detect my monitors",
            "Monitors not working through dock — just laptop screen",
            "Dell dock stopped outputting to external displays",
        ],
        descriptions=[
            "I plugged into my docking station this morning and neither of my two monitors are being "
            "detected. The laptop charges through the dock fine, and my keyboard and mouse work, but "
            "no video output at all. I've tried unplugging and replugging everything. This worked fine "
            "on Friday.",
            "Dual monitor setup through my dock stopped working. The monitors just say 'No Signal.' "
            "I tried a different USB-C cable and even swapped the monitors around. Nothing. I'm on "
            "the 8th floor in NYC, Trading desk — I really need my screens for market open.",
        ],
        next_best_actions=[
            "Check for recent Windows or dock firmware updates that may have broken display output. "
            "Test with a known-good dock to isolate the issue.",
            "Verify display drivers are current and try resetting the dock by unplugging power for "
            "30 seconds. If unresolved, replace the dock from spare inventory.",
        ],
        remediation_steps=[
            [
                "Have the user unplug the dock from power for 30 seconds to perform a hard reset",
                "Check Windows Update history for recent driver or OS changes",
                "Update display drivers and dock firmware through the vendor's support tool",
                "Test with an alternate dock to rule out hardware failure",
                "If the dock is faulty, replace it from the local office spare inventory",
            ],
            [
                "Verify the dock model is on the approved compatibility list for the user's laptop",
                "Reinstall dock drivers and the DisplayLink or Thunderbolt driver as applicable",
                "Check Display Settings to see if Windows detects the monitors at all",
                "Try connecting one monitor directly to the laptop to isolate the dock as the issue",
                "Replace the dock if firmware reset and driver updates do not resolve the issue",
                "Update the asset record if a new dock is issued",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# hw-005  USB-C port not working
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="hw-005",
        category=Category.HARDWARE,
        priority=Priority.P3,
        assigned_team=Team.ENDPOINT,
        needs_escalation=False,
        missing_information=[
            MissingInfo.DEVICE_INFO,
            MissingInfo.STEPS_TO_REPRODUCE,
            MissingInfo.ENVIRONMENT_DETAILS,
        ],
        subjects=[
            "USB-C port on my laptop is dead",
            "Left USB-C port stopped working — can't charge or dock",
        ],
        descriptions=[
            "The USB-C port on the left side of my laptop stopped working. Nothing happens when I plug "
            "in my charger or dock. The right-side port still works fine. I haven't spilled anything "
            "on it or damaged it as far as I know. Laptop is maybe 18 months old.",
            "One of my USB-C ports seems completely dead. Tried multiple cables and devices — no "
            "response at all. I rely on this port for my docking station at my desk. Currently using "
            "the other port but it's inconvenient.",
        ],
        next_best_actions=[
            "Run hardware diagnostics to test USB-C controller functionality. Check Device Manager "
            "for disabled or errored USB controllers.",
            "Test the port with a known-good cable and device. If confirmed dead, initiate a "
            "warranty repair for the laptop.",
        ],
        remediation_steps=[
            [
                "Check Device Manager for any disabled or errored USB controllers",
                "Run the vendor's built-in hardware diagnostic for USB ports",
                "Try a BIOS reset to defaults to rule out configuration issues",
                "If diagnostics confirm a hardware fault, initiate warranty repair",
                "Provide a USB-C hub as a temporary workaround if the user has only one working port",
            ],
            [
                "Verify the issue with a known-good USB-C cable and peripheral",
                "Update the BIOS and chipset drivers to the latest versions",
                "Check if the port works in the BIOS/pre-boot environment",
                "If the port is physically dead, submit a repair request to the hardware vendor",
                "Document the issue in the asset management system",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# hw-006  Webcam not detected in Teams
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="hw-006",
        category=Category.HARDWARE,
        priority=Priority.P3,
        assigned_team=Team.ENDPOINT,
        needs_escalation=False,
        missing_information=[
            MissingInfo.DEVICE_INFO,
            MissingInfo.APPLICATION_VERSION,
            MissingInfo.STEPS_TO_REPRODUCE,
        ],
        subjects=[
            "Camera not showing up in Teams — just a black screen",
            "Webcam stopped working, can't join video calls",
            "Built-in camera not detected in Microsoft Teams",
        ],
        descriptions=[
            "My built-in webcam isn't working in Teams anymore. When I try to turn on video it just "
            "shows a black screen with a camera icon and a line through it. Other apps like the Camera "
            "app also don't detect it. This started after last weekend. I'm in Compliance, London office "
            "and I have mandatory video-on meetings daily.",
            "Teams says 'No camera found' when I try to start video. I've checked my privacy settings "
            "and camera access is turned on. Restarted the laptop twice. Still nothing.",
        ],
        next_best_actions=[
            "Check Device Manager for the camera device status and verify the camera privacy "
            "toggle (physical and OS-level). Reinstall the camera driver if needed.",
            "Verify the camera isn't disabled in BIOS or by a physical privacy shutter. Update "
            "Teams and camera drivers, then test in the Camera app.",
        ],
        remediation_steps=[
            [
                "Check if the laptop has a physical camera privacy shutter and ensure it is open",
                "Verify the camera is enabled in Device Manager and not showing errors",
                "Check Windows Settings > Privacy > Camera to ensure app access is allowed",
                "Uninstall and reinstall the camera driver from Device Manager",
                "Test the camera in the Windows Camera app to isolate Teams as the issue",
                "If the camera works outside Teams, repair or reinstall the Teams client",
            ],
            [
                "Check BIOS settings for a camera disable option",
                "Update the camera driver through Windows Update or the vendor support tool",
                "Reset Teams video settings and clear the Teams cache",
                "If the camera is not detected at the OS level, escalate for hardware repair",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# hw-007  Headset audio cutting out
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="hw-007",
        category=Category.HARDWARE,
        priority=Priority.P4,
        assigned_team=Team.ENDPOINT,
        needs_escalation=False,
        missing_information=[
            MissingInfo.DEVICE_INFO,
            MissingInfo.REPRODUCTION_FREQUENCY,
            MissingInfo.ENVIRONMENT_DETAILS,
        ],
        subjects=[
            "Headset audio keeps cutting in and out during calls",
            "Jabra headset dropping audio intermittently",
        ],
        descriptions=[
            "My Jabra headset audio keeps cutting out during Teams calls. People say I sound fine for "
            "a minute then I go silent for a few seconds and come back. It's been happening all week. "
            "I've tried different USB ports. Not sure if it's the headset or the laptop.",
            "Audio on my wireless headset drops out randomly. Sometimes it's fine for an hour, "
            "sometimes it cuts out every few minutes. Colleagues on my floor don't seem to have "
            "the same issue. I'm in NYC, 12th floor, Markets division.",
        ],
        next_best_actions=[
            "Update the headset firmware using Jabra Direct and check for Bluetooth or USB "
            "interference. Test with a different headset to isolate the issue.",
            "Verify the headset is on the Teams-certified device list, update firmware, and check "
            "for driver conflicts in Device Manager.",
        ],
        remediation_steps=[
            [
                "Update the headset firmware using the manufacturer's management tool (e.g., Jabra Direct)",
                "Check for Bluetooth interference if the headset is wireless — disable nearby Bluetooth devices",
                "Test with a wired USB connection to rule out wireless issues",
                "Try the headset on a different laptop to determine if the fault is the headset or laptop",
                "If the headset is faulty, issue a replacement from the peripherals inventory",
            ],
            [
                "Verify the headset model is on the Microsoft Teams certified devices list",
                "Update audio drivers and the Teams desktop client to the latest version",
                "Disable audio enhancements in Windows Sound settings",
                "Test with a different headset to isolate the hardware",
                "If the issue persists with multiple headsets, investigate the laptop's audio subsystem",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# hw-008  Network printer not printing
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="hw-008",
        category=Category.HARDWARE,
        priority=Priority.P3,
        assigned_team=Team.NETWORK,
        needs_escalation=False,
        missing_information=[
            MissingInfo.AFFECTED_SYSTEM,
            MissingInfo.ERROR_MESSAGE,
            MissingInfo.NETWORK_LOCATION,
        ],
        subjects=[
            "Network printer on 10th floor not printing",
            "Can't print to the shared printer — jobs just disappear",
            "Floor printer stuck in queue, nothing comes out",
        ],
        descriptions=[
            "The network printer on the 10th floor in NYC hasn't been printing since this morning. "
            "I've sent several jobs but nothing comes out. The printer display shows 'Ready' but the "
            "queue on my laptop shows the jobs as pending. Other people on the floor are having the "
            "same issue.",
            "None of us on the 10th floor can print. Jobs seem to go to the queue and then vanish. "
            "The printer looks normal — green light, paper loaded, no jams. We need this for end-of-day "
            "compliance reports.",
        ],
        next_best_actions=[
            "Check the print server for stuck jobs and verify network connectivity to the printer. "
            "Restart the print spooler service on the server.",
            "Ping the printer to verify network reachability. Clear the print queue on the server "
            "and restart the spooler. Check for driver updates.",
        ],
        remediation_steps=[
            [
                "Verify the printer is reachable on the network by pinging its IP address",
                "Check the print server for stuck or errored print jobs and clear the queue",
                "Restart the print spooler service on the print server",
                "Verify the printer driver is current and compatible with the server OS",
                "Send a test page from the server to confirm printing is restored",
                "Notify affected users once the printer is back online",
            ],
            [
                "Check the printer's network configuration and ensure it has a valid IP address",
                "Verify the print server service is running and healthy",
                "Clear all queued jobs and restart both the spooler and the printer",
                "If the issue persists, reinstall the printer on the print server",
                "Test printing from multiple workstations to confirm resolution",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# hw-009  Scanner to email not working
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="hw-009",
        category=Category.HARDWARE,
        priority=Priority.P3,
        assigned_team=Team.NETWORK,
        needs_escalation=False,
        missing_information=[
            MissingInfo.AFFECTED_SYSTEM,
            MissingInfo.ERROR_MESSAGE,
            MissingInfo.CONFIGURATION_DETAILS,
        ],
        subjects=[
            "Scan to email not working on the MFP",
            "Multifunction printer won't send scans to email",
        ],
        descriptions=[
            "The multifunction printer on the 5th floor in London can print fine, but the scan-to-email "
            "feature stopped working about a week ago. When I scan a document and enter my email, it "
            "gives an error on the display but it disappears too fast to read. No scans have arrived "
            "in my inbox.",
            "Scan to email has been broken on our floor's Ricoh MFP for days now. I've tried scanning "
            "to multiple email addresses and nothing gets delivered. HR needs this to process onboarding "
            "paperwork — we're hiring a lot of people this quarter.",
        ],
        next_best_actions=[
            "Check the MFP's SMTP relay configuration and verify the mail flow connector in "
            "Exchange Online allows relay from the printer's IP address.",
            "Review the printer's email logs for delivery errors. Verify SMTP authentication "
            "credentials have not expired and that the relay IP is whitelisted.",
        ],
        remediation_steps=[
            [
                "Log into the printer's web admin panel and check the SMTP configuration",
                "Verify the SMTP relay connector in Exchange Online permits the printer's IP",
                "Check if the SMTP credentials used by the printer have expired or been rotated",
                "Send a test email from the printer admin panel to verify connectivity",
                "If credentials expired, update them on the printer and test scan-to-email again",
            ],
            [
                "Check the printer's scan-to-email error log from the web management interface",
                "Verify DNS resolution from the printer to the SMTP relay endpoint",
                "Test SMTP connectivity from the printer's subnet using telnet on port 25/587",
                "Update SMTP settings if the relay endpoint or credentials have changed",
                "Confirm successful scan delivery to at least two different email addresses",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# hw-010  Laptop keyboard keys stuck / broken
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="hw-010",
        category=Category.HARDWARE,
        priority=Priority.P3,
        assigned_team=Team.ENDPOINT,
        needs_escalation=False,
        missing_information=[
            MissingInfo.DEVICE_INFO,
            MissingInfo.AFFECTED_SYSTEM,
        ],
        subjects=[
            "Several keyboard keys not working on my laptop",
            "Laptop keyboard — E and R keys are dead",
            "Sticky and unresponsive keys on my ThinkPad keyboard",
        ],
        descriptions=[
            "The E and R keys on my laptop keyboard stopped responding. I have to copy-paste those "
            "letters from other text which is incredibly slow. I spilled a bit of coffee near the "
            "keyboard last week but cleaned it up right away. The rest of the keys seem fine. I'm using "
            "a ThinkPad something — I don't know the exact model.",
            "Multiple keys on my laptop are either stuck or not registering at all. It's making it "
            "impossible to type properly. I've tried restarting and blowing compressed air under the "
            "keys. I'm in Singapore, Ops team. Can I get an external keyboard in the meantime?",
        ],
        next_best_actions=[
            "Provide an external USB keyboard as an immediate workaround and assess whether the "
            "built-in keyboard needs repair or full device replacement.",
            "Issue a loaner external keyboard and create a repair ticket. If the laptop is under "
            "warranty, initiate a keyboard replacement through the vendor.",
        ],
        remediation_steps=[
            [
                "Issue a USB external keyboard from peripheral inventory as a temporary workaround",
                "Identify the laptop model and check warranty status",
                "Run keyboard diagnostics using the vendor's built-in tool",
                "If hardware failure confirmed, submit a warranty repair request for keyboard replacement",
                "Track repair status and follow up with the user when the repair is complete",
            ],
            [
                "Provide an external keyboard immediately so the user can continue working",
                "Check if the issue is software-related by testing the keyboard in the BIOS",
                "If the keyboard fails in BIOS, confirm hardware fault and initiate repair",
                "If under warranty, schedule on-site or depot repair with the vendor",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# hw-011  Laptop overheating and shutting down
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="hw-011",
        category=Category.HARDWARE,
        priority=Priority.P2,
        assigned_team=Team.ENDPOINT,
        needs_escalation=False,
        missing_information=[
            MissingInfo.DEVICE_INFO,
            MissingInfo.REPRODUCTION_FREQUENCY,
            MissingInfo.TIMESTAMP,
        ],
        subjects=[
            "Laptop keeps overheating and shutting down on its own",
            "Machine runs extremely hot and powers off randomly",
        ],
        descriptions=[
            "My laptop has been getting dangerously hot and shutting itself off without warning. "
            "It happens mostly when I'm running Excel models and have Teams video on. The bottom of "
            "the laptop is too hot to touch. I'm on the Quantitative Research team in NYC and this is "
            "costing me hours of rework every time it shuts down.",
            "Laptop shuts down from heat at least once a day now. Fan is spinning at full speed all "
            "the time. The vents might be clogged — I haven't had it cleaned since it was issued to me "
            "about 3 years ago. I keep losing unsaved work.",
        ],
        next_best_actions=[
            "Schedule a physical inspection to clean the vents and thermal paste. Check for "
            "runaway processes driving high CPU usage.",
            "Remotely check Task Manager for processes causing high CPU/GPU load. If thermal "
            "throttling is confirmed, schedule hardware maintenance.",
        ],
        remediation_steps=[
            [
                "Remotely check running processes for abnormally high CPU or GPU usage",
                "Verify power plan settings — ensure 'High Performance' isn't causing unnecessary load",
                "Schedule the laptop for physical cleaning of vents and thermal compound replacement",
                "Run hardware diagnostics to check fan and thermal sensor functionality",
                "If the device is over 3 years old, consider a hardware refresh instead of repair",
            ],
            [
                "Check for malware or crypto-mining processes that could drive excessive heat",
                "Update BIOS and chipset drivers which may improve thermal management",
                "Schedule a technician to clean dust from internal fans and heat sinks",
                "Test the laptop under load after cleaning to verify thermals are within spec",
                "If overheating persists after cleaning, initiate a device replacement",
                "Provide a loaner in the interim if shutdowns are frequent",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# hw-012  Mouse / trackpad erratic behavior
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="hw-012",
        category=Category.HARDWARE,
        priority=Priority.P4,
        assigned_team=Team.ENDPOINT,
        needs_escalation=False,
        missing_information=[
            MissingInfo.DEVICE_INFO,
            MissingInfo.STEPS_TO_REPRODUCE,
            MissingInfo.ENVIRONMENT_DETAILS,
        ],
        subjects=[
            "Mouse cursor jumping around on its own",
            "Trackpad behaving erratically — clicks registering in wrong places",
        ],
        descriptions=[
            "My mouse cursor keeps jumping to random spots on the screen. It happens with both my "
            "external wireless mouse and the built-in trackpad. Makes it nearly impossible to click on "
            "anything accurately. I've changed the mouse batteries and tried a different surface.",
            "Trackpad on my laptop is acting up — phantom clicks, cursor drifting, gestures not "
            "working. It's been like this for a couple of days. I'm in London, Client Services. Using "
            "an external mouse helps a bit but the trackpad still interferes.",
        ],
        next_best_actions=[
            "Disable the trackpad temporarily via Settings while the user uses an external mouse. "
            "Check for trackpad driver updates and run diagnostics.",
            "Update touchpad and mouse drivers. If the issue occurs with multiple input devices, "
            "investigate potential hardware or driver conflict.",
        ],
        remediation_steps=[
            [
                "Disable the built-in trackpad in Windows Settings to stop interference",
                "Provide a wired USB mouse to rule out wireless interference",
                "Update the touchpad and mouse drivers to the latest versions",
                "Check for recently installed software that may be conflicting with input devices",
                "If the trackpad hardware is faulty, schedule a repair",
            ],
            [
                "Update Synaptics or Precision Touchpad drivers through the vendor support tool",
                "Check if palm rejection settings need adjustment",
                "Test with a known-good external mouse to isolate the problem",
                "If the trackpad is physically damaged, initiate a warranty repair",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# hw-013  External monitor flickering
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="hw-013",
        category=Category.HARDWARE,
        priority=Priority.P3,
        assigned_team=Team.ENDPOINT,
        needs_escalation=False,
        missing_information=[
            MissingInfo.DEVICE_INFO,
            MissingInfo.REPRODUCTION_FREQUENCY,
            MissingInfo.CONFIGURATION_DETAILS,
        ],
        subjects=[
            "External monitor flickering constantly",
            "Monitor keeps flashing on and off every few seconds",
            "Screen flicker on my Dell monitor — giving me a headache",
        ],
        descriptions=[
            "My external Dell monitor has been flickering non-stop since yesterday. The screen flashes "
            "black for a second and comes back, over and over. It happens every 10-20 seconds. I've "
            "tried a different cable and it still flickers. The laptop screen is fine. NYC, 14th floor.",
            "One of my two monitors keeps flickering. It's the one connected via DisplayPort through "
            "my dock. The HDMI monitor is fine. It's making it really hard to work — I'm getting "
            "headaches from it. Can someone swap it out or fix it?",
        ],
        next_best_actions=[
            "Test the monitor with a different laptop and cable to isolate whether the issue is the "
            "monitor, cable, or dock. Check refresh rate and resolution settings.",
            "Swap the display cable and try a direct connection bypassing the dock. If flickering "
            "continues, replace the monitor from inventory.",
        ],
        remediation_steps=[
            [
                "Try a different display cable (HDMI vs DisplayPort) to rule out cable issues",
                "Connect the monitor directly to the laptop, bypassing the dock",
                "Check display settings — ensure refresh rate matches the monitor's native rate",
                "Update GPU and display drivers to the latest versions",
                "If flickering persists with a direct connection, replace the monitor",
            ],
            [
                "Test the monitor with a different laptop to confirm the monitor is faulty",
                "Check the dock firmware if the monitor is connected through a dock",
                "Adjust the resolution and refresh rate in Display Settings",
                "If the monitor is confirmed faulty, issue a replacement from inventory",
                "Update the asset record to reflect the swap",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# hw-014  Laptop fan extremely loud
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="hw-014",
        category=Category.HARDWARE,
        priority=Priority.P4,
        assigned_team=Team.ENDPOINT,
        needs_escalation=False,
        missing_information=[
            MissingInfo.DEVICE_INFO,
            MissingInfo.TIMESTAMP,
            MissingInfo.STEPS_TO_REPRODUCE,
        ],
        subjects=[
            "Laptop fan is insanely loud — people can hear it on calls",
            "Fan noise on my laptop is unbearable",
        ],
        descriptions=[
            "My laptop fan has been running at full blast constantly for the past few days. It's so "
            "loud that colleagues sitting near me have complained, and people on Teams calls can hear "
            "it through my headset mic. I haven't changed anything on my end. Singapore office, "
            "Portfolio Management.",
            "The fan on my laptop never stops spinning at max. It starts as soon as I log in and "
            "doesn't quiet down even when I close all apps. The laptop does feel warm but not scorching.",
        ],
        next_best_actions=[
            "Remotely check running processes and CPU utilization to identify anything driving "
            "excessive load. Schedule a vent cleaning if the device is overdue.",
            "Check for background processes, Windows Update activity, or Defender scans that may "
            "be causing sustained CPU usage. Clean the fan if the device is old.",
        ],
        remediation_steps=[
            [
                "Check Task Manager remotely for processes consuming high CPU",
                "Verify Windows Update and Defender aren't running intensive background tasks",
                "Update BIOS — newer versions often improve fan curve behavior",
                "Schedule the laptop for physical fan and vent cleaning",
                "If the fan itself is failing, order a replacement fan or device",
            ],
            [
                "Review power plan settings and switch to 'Balanced' if on 'High Performance'",
                "Kill any unnecessary startup applications and background services",
                "Run hardware diagnostics to check fan RPM and thermal sensor readings",
                "If dust buildup is suspected, schedule a technician for internal cleaning",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# hw-015  Hard drive making clicking noises
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="hw-015",
        category=Category.HARDWARE,
        priority=Priority.P2,
        assigned_team=Team.ENDPOINT,
        needs_escalation=True,
        missing_information=[
            MissingInfo.DEVICE_INFO,
            MissingInfo.BUSINESS_IMPACT,
            MissingInfo.TIMESTAMP,
        ],
        subjects=[
            "Hard drive making clicking and grinding noises — worried about data loss",
            "Strange clicking sound from laptop, files taking forever to open",
        ],
        descriptions=[
            "My laptop has started making a repetitive clicking noise and everything is extremely "
            "slow. Files take minutes to open and sometimes I get errors saying a file can't be read. "
            "I have a lot of work on this machine that I'm not sure is all backed up to OneDrive. "
            "Please help — I don't want to lose my data. I'm in NYC, Credit Risk team.",
            "There's a clicking sound coming from inside my laptop whenever I try to open files. The "
            "machine is almost unusable now. Some folders won't even open. I've been saving things to "
            "the desktop because OneDrive sync kept failing. I'm really worried about losing my work.",
        ],
        next_best_actions=[
            "This is a data-loss risk — advise the user to stop using the laptop immediately. "
            "Attempt a remote backup of critical files before the drive fails completely.",
            "Escalate as urgent. Schedule an emergency data backup and prepare a replacement device. "
            "Do not run disk repair tools on a clicking drive as it may worsen the failure.",
        ],
        remediation_steps=[
            [
                "Instruct the user to save any open files and avoid writing to the drive",
                "Attempt to remotely back up critical data to OneDrive or a network share",
                "Do not run chkdsk or defrag — these can accelerate drive failure",
                "Prepare a replacement laptop and enroll it via Autopilot",
                "If possible, recover remaining data using a USB enclosure or imaging tool",
                "Decommission the failing device and update the asset record",
            ],
            [
                "Advise the user to power down the laptop to prevent further drive damage",
                "Dispatch a technician to clone the drive before it fails completely",
                "Provision a new laptop from spare inventory and restore data from backup",
                "Verify OneDrive sync status to determine how much data is already backed up",
                "Complete the migration and confirm the user has access to all critical files",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# hw-016  BIOS password locked after too many attempts
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="hw-016",
        category=Category.HARDWARE,
        priority=Priority.P2,
        assigned_team=Team.ENDPOINT,
        needs_escalation=False,
        missing_information=[
            MissingInfo.DEVICE_INFO,
            MissingInfo.AFFECTED_SYSTEM,
            MissingInfo.CONTACT_INFO,
        ],
        subjects=[
            "Locked out of BIOS — too many wrong password attempts",
            "BIOS password lockout, can't boot my laptop",
        ],
        descriptions=[
            "I was trying to change a BIOS setting and got the password wrong too many times. Now the "
            "laptop shows a lockout screen with a code and won't let me do anything. I can't even "
            "boot into Windows. I'm stuck. London office, Fixed Income desk.",
            "My laptop is locked at the BIOS screen. It asks for a password and I have no idea what "
            "it is — I've never set one. After several tries it locked me out completely. The machine "
            "is completely unusable.",
        ],
        next_best_actions=[
            "Use the BIOS lockout code displayed on screen to generate a master unlock password "
            "through the vendor's IT admin portal.",
            "Retrieve the BIOS admin password from the endpoint management system or contact the "
            "hardware vendor with the device service tag for a master password reset.",
        ],
        remediation_steps=[
            [
                "Obtain the lockout code or challenge code displayed on the BIOS screen",
                "Use the hardware vendor's IT admin portal to generate a master unlock password",
                "Enter the master password to unlock the BIOS",
                "Reset the BIOS password to the organization's standard and document it",
                "Verify the laptop boots into Windows normally after unlocking",
            ],
            [
                "Collect the device service tag and BIOS lockout code from the user",
                "Contact the hardware vendor's enterprise support with the service tag for a reset",
                "If remote unlock is not possible, schedule an on-site technician visit",
                "Once unlocked, set the BIOS password to the standard managed value",
                "Confirm normal boot and update the asset management record",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# hw-017  Laptop won't turn on at all
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="hw-017",
        category=Category.HARDWARE,
        priority=Priority.P2,
        assigned_team=Team.ENDPOINT,
        needs_escalation=False,
        missing_information=[
            MissingInfo.DEVICE_INFO,
            MissingInfo.TIMESTAMP,
            MissingInfo.STEPS_TO_REPRODUCE,
        ],
        subjects=[
            "Laptop completely dead — won't turn on",
            "Laptop won't power on at all, no lights, no fan",
        ],
        descriptions=[
            "I came in this morning and my laptop is completely dead. No lights, no fan, nothing when "
            "I press the power button. I've tried plugging in the charger — the charging LED doesn't "
            "come on either. It was working fine when I shut it down last night. I'm in NYC, "
            "Operations team, and I have a critical report due by noon.",
            "My laptop won't turn on. Tried holding the power button, tried a different charger from "
            "a colleague, nothing. The screen stays black, no sounds at all. It's like the thing is "
            "just dead. I need a machine urgently.",
        ],
        next_best_actions=[
            "Attempt a static discharge by holding the power button for 30 seconds with the charger "
            "disconnected. If that fails, issue a loaner laptop immediately.",
            "Walk the user through a hard reset procedure. If the device remains unresponsive, "
            "replace it and initiate a repair or warranty claim.",
        ],
        remediation_steps=[
            [
                "Instruct user to disconnect the charger and hold the power button for 30 seconds",
                "Reconnect the charger and attempt to power on",
                "If no response, try a different known-good charger",
                "If still dead, issue a loaner laptop from the local office spare pool",
                "Submit the unresponsive laptop for warranty diagnosis and repair",
                "Migrate user profile to the replacement device via Autopilot and OneDrive",
            ],
            [
                "Walk the user through a battery reset (if the model supports a pinhole reset)",
                "Try booting with the charger connected and no peripherals attached",
                "If the laptop shows no signs of life, declare it a hardware failure",
                "Provision a replacement laptop and restore the user's profile",
                "Send the failed unit for repair and track the warranty case",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# hw-018  Hardware refresh request — laptop 4+ years old
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="hw-018",
        category=Category.HARDWARE,
        priority=Priority.P4,
        assigned_team=Team.ENDPOINT,
        needs_escalation=False,
        missing_information=[
            MissingInfo.DEVICE_INFO,
            MissingInfo.BUSINESS_IMPACT,
        ],
        subjects=[
            "Requesting a new laptop — mine is over 4 years old",
            "Hardware refresh request — laptop is slow and out of warranty",
        ],
        descriptions=[
            "My laptop is over 4 years old and has become painfully slow. It takes about 5 minutes to "
            "boot up and applications freeze regularly. I know Contoso has a hardware refresh cycle and "
            "I think I'm overdue. I'm a VP in the London office, Corporate Banking team. Can I get a "
            "replacement?",
            "Requesting a hardware refresh. My current laptop was issued when I joined in 2020 and it "
            "can barely keep up anymore. Outlook takes forever to load, Excel crashes on large files, "
            "and the battery only lasts about 45 minutes. Several colleagues have already received new "
            "machines this year.",
        ],
        next_best_actions=[
            "Verify the device age and warranty status in the CMDB. If it qualifies for the refresh "
            "cycle, initiate the standard hardware replacement workflow.",
            "Check the device against the hardware refresh policy. If eligible, add the user to the "
            "next refresh batch and provide an expected timeline.",
        ],
        remediation_steps=[
            [
                "Look up the device in the CMDB to confirm asset age and warranty status",
                "Verify the user qualifies under the hardware refresh policy (typically 3-4 year cycle)",
                "Add the user to the hardware refresh queue for their office location",
                "Order the standard-spec replacement laptop for the user's role and department",
                "Schedule the device swap and data migration with the user",
                "Decommission the old device and update the asset record",
            ],
            [
                "Confirm the laptop model and age from the asset management system",
                "Check if any interim performance improvements can be made (SSD upgrade, RAM increase)",
                "If the device is beyond the refresh threshold, process the replacement request",
                "Coordinate with procurement for the new device and notify the user of the timeline",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# hw-019  USB printer not recognized after driver update
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="hw-019",
        category=Category.HARDWARE,
        priority=Priority.P4,
        assigned_team=Team.ENDPOINT,
        needs_escalation=False,
        missing_information=[
            MissingInfo.DEVICE_INFO,
            MissingInfo.ERROR_MESSAGE,
            MissingInfo.APPLICATION_VERSION,
        ],
        subjects=[
            "USB printer not recognized after Windows Update",
            "Personal desk printer stopped working after a driver update",
        ],
        descriptions=[
            "My USB label printer stopped working after the last Windows Update. The printer doesn't "
            "show up in Devices and Printers anymore. I use it to print shipping labels for our "
            "Singapore office's mailroom operations. It was fine until the update pushed last Tuesday.",
            "After a driver update this week, my desk printer isn't recognized when I plug in the USB "
            "cable. Windows makes the connection sound but nothing appears in the device list. I've "
            "tried different USB ports.",
        ],
        next_best_actions=[
            "Check Windows Update history for recently installed driver updates that may have "
            "replaced the printer driver. Roll back the driver if applicable.",
            "Reinstall the printer driver manually from the manufacturer's website. Check if the "
            "Windows Update replaced a working driver with an incompatible one.",
        ],
        remediation_steps=[
            [
                "Check Windows Update history for recently installed printer or USB driver updates",
                "Roll back the printer driver to the previous version via Device Manager",
                "If rollback is unavailable, download and install the correct driver from the manufacturer",
                "Reconnect the printer and verify it appears in Devices and Printers",
                "Print a test page to confirm functionality",
            ],
            [
                "Uninstall the printer from Device Manager including driver software",
                "Download the latest driver from the printer manufacturer's website",
                "Reinstall the driver and reconnect the USB cable",
                "If Windows Update keeps overwriting the driver, configure a driver block policy via Intune",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# hw-020  Projector bulb dead in conference room
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="hw-020",
        category=Category.HARDWARE,
        priority=Priority.P2,
        assigned_team=Team.ENDPOINT,
        needs_escalation=False,
        missing_information=[
            MissingInfo.AFFECTED_SYSTEM,
            MissingInfo.NETWORK_LOCATION,
        ],
        subjects=[
            "Conference room projector not working — executive meeting tomorrow",
            "Projector bulb dead in the large boardroom",
        ],
        descriptions=[
            "The projector in the NYC 15th-floor boardroom isn't turning on. The power light blinks "
            "orange which I think means the bulb is dead. We have an executive committee meeting "
            "tomorrow at 9 AM and this room is the only one large enough. This is urgent — the CFO "
            "will be presenting to the board.",
            "The projector in our main conference room has stopped working. It tries to turn on but "
            "shuts off after a few seconds. We've got a big client presentation this week and there's "
            "no other room with a large enough display. Can someone fix or replace it ASAP?",
        ],
        next_best_actions=[
            "Check if a spare projector bulb is available in the AV inventory. If not, arrange a "
            "portable projector or large display as a backup for the meeting.",
            "Coordinate with facilities to either replace the bulb or set up an alternate display "
            "in the room before the scheduled meeting.",
        ],
        remediation_steps=[
            [
                "Check the AV inventory for a compatible replacement projector bulb",
                "If a bulb is available, dispatch a technician to replace it and test",
                "If no spare bulb is in stock, source a portable projector or large-screen TV as backup",
                "Verify the replacement display works with the room's AV system and video conferencing",
                "Order a replacement bulb for long-term fix if one was not in stock",
            ],
            [
                "Confirm the projector model and check if the issue is the bulb or another component",
                "Arrange a temporary large display or portable projector for the upcoming meeting",
                "Order a replacement bulb or projector through the standard procurement process",
                "Schedule installation and testing outside of meeting hours",
                "Update the conference room AV equipment inventory",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# hw-021  Mobile device touchscreen unresponsive
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="hw-021",
        category=Category.HARDWARE,
        priority=Priority.P3,
        assigned_team=Team.ENDPOINT,
        needs_escalation=False,
        missing_information=[
            MissingInfo.DEVICE_INFO,
            MissingInfo.STEPS_TO_REPRODUCE,
            MissingInfo.REPRODUCTION_FREQUENCY,
        ],
        subjects=[
            "Company phone touchscreen not responding",
            "iPhone touchscreen frozen — can't use Authenticator app",
        ],
        descriptions=[
            "My company iPhone's touchscreen is not responding at all. I can see notifications come in "
            "but I can't swipe or tap anything. This is a big problem because I use the Authenticator "
            "app on it for MFA and now I can't approve sign-in requests. I've tried restarting it by "
            "holding the buttons but the screen still won't respond. I'm in London, Compliance team.",
            "Touchscreen on my work phone is completely dead. The phone seems to be on — it rings and "
            "I can hear notification sounds — but I can't interact with it at all. I need it for MFA "
            "approvals and Teams calls when I'm away from my desk.",
        ],
        next_best_actions=[
            "Issue a temporary MFA bypass or alternative authentication method so the user isn't "
            "blocked. Arrange a phone replacement through the mobile device program.",
            "Add a temporary authentication phone number in Entra ID for MFA. Schedule a device "
            "swap from the mobile device inventory.",
        ],
        remediation_steps=[
            [
                "Set up a temporary MFA method (SMS or phone call) in Entra ID so user isn't blocked",
                "Attempt a force restart of the device (model-specific button combination)",
                "If the screen remains unresponsive, wipe the device remotely via Intune",
                "Issue a replacement phone from the mobile device inventory",
                "Enroll the new device in Intune and restore the user's Authenticator configuration",
            ],
            [
                "Provide a temporary authentication bypass so the user can still sign in",
                "Try a hard reset by connecting the phone to a computer and using recovery mode",
                "If recovery doesn't fix the screen, declare a hardware failure",
                "Order a replacement device and configure it with the user's profile and apps",
                "Remotely wipe the old device and update the mobile asset record",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# hw-022  Laptop WiFi card not detecting any networks
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="hw-022",
        category=Category.HARDWARE,
        priority=Priority.P2,
        assigned_team=Team.ENDPOINT,
        needs_escalation=False,
        missing_information=[
            MissingInfo.DEVICE_INFO,
            MissingInfo.ERROR_MESSAGE,
            MissingInfo.ENVIRONMENT_DETAILS,
        ],
        subjects=[
            "WiFi not detecting any networks at all",
            "Laptop wireless card seems dead — no networks found",
            "No WiFi networks showing up on my laptop",
        ],
        descriptions=[
            "My laptop doesn't see any WiFi networks. The WiFi icon shows a globe with a 'no internet' "
            "indicator, and when I click on it there are zero networks listed. Airplane mode is off. "
            "Other people around me are connected fine. I can't do any work without WiFi since we "
            "don't have Ethernet at the hot desks. Singapore office, FX Trading.",
            "WiFi stopped working completely. No networks show up at all — not even the guest network. "
            "I've toggled WiFi off and on, turned airplane mode on and off, and restarted the laptop. "
            "Nothing helps. I'm completely offline and I have a trade reconciliation due in two hours.",
        ],
        next_best_actions=[
            "Check Device Manager for the WiFi adapter status. Try disabling and re-enabling the "
            "adapter. If the hardware is failed, provide a USB WiFi adapter as a workaround.",
            "Verify the wireless adapter isn't disabled in BIOS or by a physical switch. Reinstall "
            "the WiFi driver and test. Provide a USB Ethernet adapter as a fallback.",
        ],
        remediation_steps=[
            [
                "Check if the laptop has a physical WiFi toggle switch and ensure it is on",
                "Open Device Manager and check the WiFi adapter for errors or disabled status",
                "Disable and re-enable the WiFi adapter in Network Connections",
                "Uninstall and reinstall the WiFi driver from Device Manager",
                "If the adapter is not detected at all, provide a USB WiFi or Ethernet adapter",
                "If hardware failure is confirmed, initiate a repair or replacement",
            ],
            [
                "Run the Windows Network Troubleshooter to detect common issues",
                "Check BIOS settings for a wireless adapter disable option",
                "Reset network settings via Settings > Network & Internet > Advanced > Network reset",
                "If the driver reinstall fails, test with a USB WiFi dongle as a workaround",
                "Submit a hardware repair ticket if the internal WiFi card has failed",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# hw-023  Desktop PC making grinding noise
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="hw-023",
        category=Category.HARDWARE,
        priority=Priority.P3,
        assigned_team=Team.ENDPOINT,
        needs_escalation=False,
        missing_information=[
            MissingInfo.DEVICE_INFO,
            MissingInfo.TIMESTAMP,
            MissingInfo.AFFECTED_SYSTEM,
        ],
        subjects=[
            "Desktop PC making a loud grinding noise",
            "Tower under my desk is making an awful mechanical sound",
        ],
        descriptions=[
            "The desktop PC under my desk has started making a grinding noise. It's intermittent — "
            "comes and goes throughout the day. It sounds like it's coming from the front of the tower, "
            "maybe a fan hitting something. Performance seems fine for now. NYC office, Back Office "
            "settlements team.",
            "My desktop tower is making a really bad grinding/rattling noise. It started a couple days "
            "ago and it's getting worse. My neighbors can hear it too. Not sure if it's a fan or the "
            "hard drive. The machine still works but I'm nervous it's going to break.",
        ],
        next_best_actions=[
            "Schedule a technician to physically inspect the desktop. The noise is likely a failing "
            "fan or a cable touching a fan blade — but could indicate a dying hard drive.",
            "Have the user gently check if the side panel is loose. Dispatch a technician to "
            "diagnose whether the noise is from a fan, HDD, or cable obstruction.",
        ],
        remediation_steps=[
            [
                "Dispatch a technician to inspect the desktop at the user's desk",
                "Identify the noise source — fan, hard drive, or loose component",
                "If a fan is failing, replace it with a compatible spare from inventory",
                "If the hard drive is making noise, immediately back up data and replace the drive",
                "Run hardware diagnostics after the fix to verify system health",
            ],
            [
                "Ask the user if the noise changes when the PC is under load vs idle",
                "Schedule a physical inspection by the local endpoint team",
                "Replace the failing component (fan, HDD, or cable management fix)",
                "If the machine is old, consider a full desktop replacement",
                "Update the asset record with the repair details",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# hw-024  Thunderbolt dock firmware update bricked the dock
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="hw-024",
        category=Category.HARDWARE,
        priority=Priority.P2,
        assigned_team=Team.ENDPOINT,
        needs_escalation=False,
        missing_information=[
            MissingInfo.DEVICE_INFO,
            MissingInfo.ERROR_MESSAGE,
            MissingInfo.STEPS_TO_REPRODUCE,
        ],
        subjects=[
            "Dock bricked after firmware update — nothing works",
            "Thunderbolt dock dead after applying firmware update from Intune",
        ],
        descriptions=[
            "I got a notification from the Dell Command Update to update my Thunderbolt dock firmware. "
            "The update ran and then the dock just died. No lights, no power delivery, monitors don't "
            "work, nothing. My laptop doesn't even detect it anymore. I was in the middle of a trading "
            "day and now I'm working off just the laptop screen. NYC, Equities desk.",
            "My dock stopped working entirely after a firmware update was pushed. The update seemed to "
            "fail halfway through and now the dock is completely unresponsive. I've tried unplugging it "
            "for several minutes and plugging back in. Still dead. I need my dual-monitor setup for "
            "work — this is critical.",
        ],
        next_best_actions=[
            "Attempt a dock recovery using the vendor's firmware recovery tool. If recovery fails, "
            "replace the dock immediately from spare inventory.",
            "Try a forced firmware reflash using the vendor's command-line recovery utility. If the "
            "dock cannot be recovered, swap it with a spare and RMA the bricked unit.",
        ],
        remediation_steps=[
            [
                "Attempt a hard reset by unplugging the dock from power for 60 seconds",
                "Download the vendor's dock firmware recovery tool and attempt a reflash",
                "If the recovery tool cannot detect the dock, the firmware chip may be corrupted",
                "Replace the dock from the local spare inventory",
                "Verify the replacement dock works with the user's laptop and monitors",
                "RMA the bricked dock and flag the firmware version for review with the vendor",
            ],
            [
                "Try connecting the dock with a different USB-C/Thunderbolt cable",
                "Attempt a firmware recovery using the vendor's command-line recovery utility",
                "If unrecoverable, issue a replacement dock and configure it for the user's setup",
                "Report the firmware issue to the vendor and check if other users are affected",
                "If widespread, pause the firmware deployment in Intune pending investigation",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# hw-025  Multi-monitor setup only showing clone not extend
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="hw-025",
        category=Category.HARDWARE,
        priority=Priority.P4,
        assigned_team=Team.ENDPOINT,
        needs_escalation=False,
        missing_information=[
            MissingInfo.DEVICE_INFO,
            MissingInfo.CONFIGURATION_DETAILS,
            MissingInfo.ENVIRONMENT_DETAILS,
        ],
        subjects=[
            "Monitors showing the same thing — can't extend display",
            "Dual monitors are mirrored instead of extended",
            "Multi-monitor won't go to extend mode, only clone",
        ],
        descriptions=[
            "Both my external monitors are showing the exact same thing as my laptop screen. I need "
            "them to extend so I can have different windows on each screen. I've tried right-clicking "
            "the desktop and going to Display Settings but the 'Extend' option doesn't seem to stick — "
            "it goes right back to 'Duplicate.' London office, Structured Products team.",
            "My two monitors are cloned instead of extended. Every time I change it to 'Extend these "
            "displays' and click Apply, it reverts back to Duplicate after a few seconds. This has "
            "been going on since I got a new dock last week. I really need three separate screens for "
            "my workflow.",
        ],
        next_best_actions=[
            "Check if the dock supports multi-stream transport (MST) for extending displays. Verify "
            "GPU driver version and display configuration in the vendor's display management tool.",
            "Update the GPU driver and dock firmware. Check if the monitors are daisy-chained and "
            "whether MST is enabled on the dock and monitors.",
        ],
        remediation_steps=[
            [
                "Open Display Settings and check how many monitors Windows detects",
                "Verify the dock supports extending displays (MST capability)",
                "Update the GPU driver to the latest version from the vendor",
                "Check the dock firmware version and update if available",
                "Manually set each display to 'Extend' and click Apply, then confirm the arrangement",
                "If the setting won't persist, check for Group Policy or Intune display configuration conflicts",
            ],
            [
                "Verify the display cable types — some adapters only support mirroring",
                "Check if the monitors support DisplayPort MST if daisy-chained",
                "Update the dock firmware and Thunderbolt/DisplayLink drivers",
                "Test with a direct laptop-to-monitor connection to rule out dock limitations",
                "If the dock doesn't support extending, replace with an MST-capable model",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# hw-026  Laptop screen cracked — no photo evidence
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="hw-026",
        category=Category.HARDWARE,
        priority=Priority.P2,
        assigned_team=Team.ENDPOINT,
        needs_escalation=False,
        missing_information=[
            MissingInfo.SCREENSHOT_OR_ATTACHMENT,
            MissingInfo.DEVICE_INFO,
        ],
        subjects=[
            "Laptop screen is cracked — need a replacement",
            "Display cracked on my work laptop — can't use it",
            "Broken laptop screen — requesting repair or replacement",
        ],
        descriptions=[
            "My laptop screen is cracked. I think it happened in my bag during my commute. The "
            "display has a big spiderweb crack on the right side and part of the screen is black. "
            "I can still see about half the screen but it's unusable for real work. I don't have "
            "a photo of the damage — I'm submitting this from my phone. I'm in the London office, "
            "Operations team, and I need a working machine urgently.",
            "The screen on my laptop is shattered. I opened it this morning and it was already "
            "cracked — not sure what happened. I can barely make out anything on the display. "
            "I didn't take a picture because I figured you'd just need my asset tag, but I don't "
            "know my asset tag either. Can someone come look at it?",
        ],
        next_best_actions=[
            "Request a photo of the damage for the warranty or insurance claim. Identify the "
            "device model and asset tag, then issue a loaner while the screen is repaired.",
        ],
        remediation_steps=[
            [
                "Ask the user to take a photo of the screen damage and attach it to the ticket",
                "Identify the device model and asset tag from the CMDB or device label",
                "Issue a loaner laptop from the local spare pool",
                "Submit the damaged laptop for screen repair under warranty or accidental damage coverage",
                "Migrate the user's profile to the loaner via Autopilot and OneDrive",
                "Track the repair and swap back once the original device is fixed",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# hw-027  Repeat hardware failure — prior ticket reference
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="hw-027",
        category=Category.HARDWARE,
        priority=Priority.P2,
        assigned_team=Team.ENDPOINT,
        needs_escalation=False,
        missing_information=[
            MissingInfo.PREVIOUS_TICKET_ID,
            MissingInfo.DEVICE_INFO,
        ],
        subjects=[
            "Same laptop issue AGAIN — this was supposedly fixed last month",
            "Repeat hardware failure — third time reporting this",
            "Laptop overheating problem is back — had a ticket for this before",
        ],
        descriptions=[
            "My laptop is overheating and shutting down randomly again. This is the same problem "
            "I reported before — IT replaced the thermal paste and cleaned the fans last time, "
            "but the issue is back after just three weeks. I don't have the old ticket number "
            "handy. The laptop gets extremely hot on the bottom and then just shuts off without "
            "warning. I'm losing unsaved work every time. NYC office, Risk team.",
            "This is the third time I'm reporting the same issue. My laptop randomly freezes and "
            "then blue-screens. It was sent for repair twice already. I know there are previous "
            "tickets but I didn't save the numbers. At this point I think the machine needs to be "
            "fully replaced rather than repaired again.",
        ],
        next_best_actions=[
            "Search for the user's previous hardware tickets to review repair history. If the "
            "device has had multiple failures, escalate for a full replacement.",
        ],
        remediation_steps=[
            [
                "Search the ticketing system for the user's previous hardware repair tickets",
                "Review the device's repair history in the CMDB or asset management system",
                "If the device has had three or more repairs, process a full replacement",
                "Issue a loaner immediately to minimize productivity loss",
                "Decommission the repeatedly failing device and update asset records",
                "Provision a new laptop and migrate the user's profile",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# hw-028  Remote worker equipment broken — no callback info
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="hw-028",
        category=Category.HARDWARE,
        priority=Priority.P3,
        assigned_team=Team.ENDPOINT,
        needs_escalation=False,
        missing_information=[
            MissingInfo.CONTACT_INFO,
            MissingInfo.DEVICE_INFO,
        ],
        subjects=[
            "Remote worker keyboard and trackpad not working",
            "Work-from-home setup broken — keyboard died",
            "Home office equipment failure — need replacement shipped",
        ],
        descriptions=[
            "I work from home full-time and my laptop keyboard just stopped working. Several keys "
            "are unresponsive and the trackpad is glitchy. I'm typing this from an old personal "
            "keyboard I found. I need a repair or replacement shipped to me but I realize you "
            "might not have my current home address on file — I moved last month. I also don't "
            "have a direct desk phone since I'm remote.",
            "My company-issued monitor died — the screen just went black and won't turn back on. "
            "I'm fully remote so I can't just walk up to the IT desk. I need a replacement "
            "shipped but I'm not sure if my shipping address in the system is correct. I don't "
            "have a good phone number for callbacks either since I mostly use Teams, which I "
            "currently can't access without the second screen.",
        ],
        next_best_actions=[
            "Verify the remote worker's current shipping address and preferred contact method. "
            "Arrange equipment replacement via courier to their home office.",
        ],
        remediation_steps=[
            [
                "Contact the user via Teams or email to confirm their current mailing address",
                "Verify the device model and warranty status from the CMDB",
                "Ship a replacement device via next-day courier to the confirmed address",
                "Provide remote setup instructions or schedule a remote support session",
                "Arrange a return shipping label for the defective equipment",
                "Update the user's contact and address records in the HR and IT systems",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# hw-029  Monitor color calibration off — no screenshot
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="hw-029",
        category=Category.HARDWARE,
        priority=Priority.P4,
        assigned_team=Team.ENDPOINT,
        needs_escalation=False,
        missing_information=[
            MissingInfo.SCREENSHOT_OR_ATTACHMENT,
            MissingInfo.ENVIRONMENT_DETAILS,
        ],
        subjects=[
            "Monitor colors look completely wrong",
            "External monitor has a yellow/green tint — display is off",
            "Color calibration on my monitor is way off since this morning",
        ],
        descriptions=[
            "My external monitor's colors are completely off. Everything has a yellowish-green "
            "tint that makes it really hard to work with. Charts and reports look wrong and I "
            "can't trust what I'm seeing on screen. I don't have a screenshot because a "
            "screenshot wouldn't show the hardware color issue — it looks fine in the screenshot "
            "but terrible on the physical screen. I'm in the Singapore office, Design team.",
            "The monitor at my desk suddenly shifted to very warm, orangey tones. Whites look "
            "yellow and blues look green. I work with financial dashboards and the color-coding "
            "is meaningless now. I tried adjusting the monitor's on-screen settings but nothing "
            "helped. I can't easily photograph it because the camera doesn't capture it well. "
            "Not sure if it's the cable, the monitor, or a Windows setting.",
        ],
        next_best_actions=[
            "Ask the user to take a phone photo of the monitor showing the color issue. Check "
            "whether it's a hardware fault, a cable issue, or a Night Light / color profile setting.",
        ],
        remediation_steps=[
            [
                "Ask the user to capture a phone photo of the monitor to document the color shift",
                "Check Windows display settings — verify Night Light and HDR are off",
                "Reset the color profile to sRGB default in Display Settings > Color Management",
                "Try a different display cable (HDMI, DisplayPort, or USB-C) to rule out cable faults",
                "Test the monitor with another laptop to determine if the issue is monitor-specific",
                "If the monitor is faulty, replace it from inventory and update asset records",
            ],
        ],
    )
)

# ---------------------------------------------------------------------------
# hw-030  Second docking station failure — prior ticket reference
# ---------------------------------------------------------------------------
register(
    ScenarioTemplate(
        scenario_id="hw-030",
        category=Category.HARDWARE,
        priority=Priority.P3,
        assigned_team=Team.ENDPOINT,
        needs_escalation=False,
        missing_information=[
            MissingInfo.PREVIOUS_TICKET_ID,
            MissingInfo.SCREENSHOT_OR_ATTACHMENT,
        ],
        subjects=[
            "Docking station failed again — same issue as before",
            "Replacement dock also not working — this is the second one",
            "Another docking station failure — had a ticket for the first one",
        ],
        descriptions=[
            "The replacement docking station I received last month is now having the same issue as "
            "the original one. It intermittently loses connection to my monitors and Ethernet — "
            "everything flickers off for a few seconds and comes back. This happened with the "
            "previous dock too and I had a ticket open for it, but I don't remember the ticket "
            "number. I didn't capture a video of the flicker because it's unpredictable. London "
            "office, Equities desk.",
            "This is my second dock failure in two months. The first one was replaced after I "
            "reported it but the new one is doing the exact same thing — random disconnects of "
            "all peripherals. I think there might be a ticket from when the first dock was "
            "replaced but I can't find the reference. It's hard to capture because it happens "
            "randomly and only lasts a few seconds.",
        ],
        next_best_actions=[
            "Look up the user's previous dock-related ticket to review the pattern. Investigate "
            "whether the issue is the dock model, the laptop's Thunderbolt port, or a driver problem.",
        ],
        remediation_steps=[
            [
                "Search for the user's prior dock replacement ticket in the ticketing system",
                "Compare the dock models from both failures to identify a pattern",
                "Ask the user to capture a short video next time the flicker occurs",
                "Test the laptop with a different dock model to rule out a laptop port issue",
                "Update Thunderbolt and dock firmware to the latest versions",
                "If the laptop port is suspected, schedule a hardware diagnostic",
            ],
        ],
    )
)
