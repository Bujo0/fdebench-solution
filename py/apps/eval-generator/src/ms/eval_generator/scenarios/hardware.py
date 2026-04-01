# Copyright (c) Microsoft. All rights reserved.
"""Hardware & Peripherals category scenarios for eval dataset."""

from ms.eval_generator.scenarios._base import ScenarioDefinition
from ms.eval_generator.scenarios._base import ScenarioGold

HARDWARE_SCENARIOS: list[ScenarioDefinition] = [
    # ──────────────────────────────────────────────────────────────────
    # 1. Laptop won't boot after Windows update
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="hardware-001",
        subjects=(
            "Laptop won't boot after Windows update",
            "Black screen after overnight update",
        ),
        descriptions=(
            "My Dell Latitude 5540 won't boot this morning. It was applying Windows updates overnight and "
            "now just shows a black screen with a blinking cursor. I've tried holding the power button, "
            "removing from dock — nothing works.",
            "Laptop stuck in a boot loop after last night's Windows update. It shows the Dell logo, then a "
            "blue Windows recovery screen flashes briefly, then restarts. I have a client presentation at 2 "
            "PM and all my files are on this machine.",
        ),
        gold=ScenarioGold(
            category="Hardware & Peripherals",
            priority="P2",
            assigned_team="Endpoint Engineering",
            needs_escalation=False,
            missing_information=(
                "device_info",
                "error_message",
            ),
            next_best_action="Attempt Windows recovery boot and rollback the failed update",
            remediation_steps=(
                "Boot into Windows Recovery Environment using F8 or recovery media",
                "Attempt to roll back the most recent Windows update",
                "If rollback fails, run startup repair from recovery console",
                "If device still unbootable, back up data via recovery USB and reimage",
                "Provide a loaner laptop if repair will take more than 4 hours",
            ),
        ),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 2. Blue screen of death recurring daily
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="hardware-002",
        subjects=(
            "Getting blue screen every day around 2 PM",
            "BSOD recurring — DRIVER_IRQL_NOT_LESS_OR_EQUAL",
        ),
        descriptions=(
            "My laptop blue screens at least once a day, usually mid-afternoon. The error code is "
            "DRIVER_IRQL_NOT_LESS_OR_EQUAL. I've lost unsaved work three times this week. It's a ThinkPad "
            "X1 Carbon, about 8 months old.",
            "Daily BSOD crashes. Started about two weeks ago after I plugged in a new USB-C dock. The crash "
            "dump references ndis.sys. I'm losing patience — this is affecting my productivity badly.",
        ),
        gold=ScenarioGold(
            category="Hardware & Peripherals",
            priority="P3",
            assigned_team="Endpoint Engineering",
            needs_escalation=False,
            missing_information=(
                "device_info",
                "error_message",
                "steps_to_reproduce",
            ),
            next_best_action="Collect crash dump files and analyze the BSOD driver fault",
            remediation_steps=(
                "Collect crash dump files from C:\Windows\Minidump",
                "Analyze dump with WinDbg to identify the faulting driver",
                "Update or roll back the network driver referenced in ndis.sys",
                "Test without the USB-C dock to isolate the cause",
                "If driver update doesn't resolve, run hardware diagnostics on memory and storage",
            ),
        ),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 3. Laptop battery draining in under 2 hours
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="hardware-003",
        subjects=(
            "Battery dies in less than 2 hours",
            "Laptop battery drain — barely lasts through one meeting",
        ),
        descriptions=(
            "My Surface Laptop 5 battery used to last 8+ hours but now it dies in under 2 hours. I can't "
            "make it through a single meeting without plugging in. The battery health in settings shows "
            "'consider replacing.' This laptop is only 14 months old.",
            "Terrible battery life on my work laptop. Goes from 100% to dead in about 90 minutes. I've "
            "closed all background apps, reduced screen brightness — nothing helps. I need this laptop for "
            "travel next week.",
        ),
        gold=ScenarioGold(
            category="Hardware & Peripherals",
            priority="P3",
            assigned_team="Endpoint Engineering",
            needs_escalation=False,
            missing_information=(
                "device_info",
            ),
            next_best_action="Run battery diagnostics and determine if battery replacement or device swap is needed",
            remediation_steps=(
                "Run powercfg /batteryreport to check battery health and cycle count",
                "Check for power-hungry background processes in Task Manager",
                "Update BIOS and chipset drivers to latest versions",
                "If battery health is degraded below 60%, initiate battery replacement",
                "Provide a loaner device if replacement will take more than 2 days",
            ),
        ),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 4. Cracked laptop screen
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="hardware-004",
        subjects=(
            "Laptop screen cracked — need replacement",
            "Broken display on my ThinkPad",
        ),
        descriptions=(
            "I accidentally knocked my laptop off my desk and the screen cracked. I can still see about 60% "
            "of the display but there are cracks across the top left corner and some dead pixels. I need "
            "this fixed or replaced.",
            "My laptop screen is cracked and partially unreadable. It happened when my bag fell in the "
            "parking garage this morning. Can I get a screen replacement or a new laptop? I can connect to "
            "an external monitor as a workaround for now.",
        ),
        gold=ScenarioGold(
            category="Hardware & Peripherals",
            priority="P3",
            assigned_team="Endpoint Engineering",
            needs_escalation=False,
            missing_information=(
                "device_info",
            ),
            next_best_action="Arrange screen replacement or device swap depending on warranty and repair timeline",
            remediation_steps=(
                "Document the damage and check warranty/accidental damage coverage",
                "Provide an external monitor as a temporary workaround",
                "If under warranty, initiate vendor repair request for screen replacement",
                "If out of warranty, assess repair cost vs. device replacement",
                "Schedule device swap and data migration if replacement is needed",
            ),
        ),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 5. Docking station not detecting external monitors
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="hardware-005",
        subjects=(
            "Docking station won't detect my monitors",
            "External displays not working through dock",
        ),
        descriptions=(
            "My Thunderbolt docking station stopped detecting both of my external monitors. The dock is "
            "powered on (lights are green) and other USB devices connected through it work fine (keyboard, "
            "mouse). Just no video output. Was working fine last Friday.",
            "Neither of my two monitors is being detected through my Dell WD19TB dock. I've tried different "
            "cables, different ports on the dock, and rebooting. The monitors work fine when connected "
            "directly to the laptop via HDMI.",
        ),
        gold=ScenarioGold(
            category="Hardware & Peripherals",
            priority="P3",
            assigned_team="Endpoint Engineering",
            needs_escalation=False,
            missing_information=(
                "device_info",
            ),
            next_best_action="Update docking station firmware and display drivers to resolve the video output issue",
            remediation_steps=(
                "Check if the docking station firmware is up to date",
                "Update display adapter and Thunderbolt controller drivers",
                "Try connecting monitors one at a time to isolate the issue",
                "Test the dock with a different laptop to determine if dock is faulty",
                "If dock is defective, replace with a spare from inventory",
            ),
        ),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 6. USB-connected printer paper jam and errors
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="hardware-006",
        subjects=(
            "Printer keeps jamming — paper stuck inside",
            "USB printer showing error after paper jam",
        ),
        descriptions=(
            "The HP LaserJet on my desk keeps jamming. I cleared the paper but now it shows a persistent "
            "'paper jam' error even though there's no paper stuck. I've turned it off and on multiple "
            "times. Asset tag: PRN-0847.",
            "My desk printer has been jamming every few pages for the past week. I need to print a lot of "
            "client documents today. The printer is an HP LaserJet Pro connected via USB. It's about 3 "
            "years old.",
        ),
        gold=ScenarioGold(
            category="Hardware & Peripherals",
            priority="P3",
            assigned_team="Endpoint Engineering",
            needs_escalation=False,
            missing_information=(
                "device_info",
            ),
            next_best_action="Clear persistent printer error and inspect feed rollers for wear",
            remediation_steps=(
                "Power cycle the printer and clear any error states",
                "Open all access panels and check for small paper fragments",
                "Clean the paper feed rollers with a lint-free cloth",
                "Run the printer's internal cleaning cycle",
                "If jams persist, arrange for printer replacement",
            ),
        ),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 7. Network printer not showing in print dialog
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="hardware-007",
        subjects=(
            "Can't find the floor printer in my print options",
            "Network printer disappeared from my computer",
        ),
        descriptions=(
            "The network printer on Floor 3 (HP Color LaserJet M553) is no longer showing in my print "
            "dialog. It was there last week. I've checked 'Add Printer' but I can't find it on the network "
            "either. Other people on my floor can still print to it.",
            "Our shared network printer in the Trading floor copy room vanished from everyone's computers "
            "this morning. Nobody on the floor can see it. Printer appears to be physically on and has an "
            "IP displayed on its panel: 10.20.3.45.",
        ),
        gold=ScenarioGold(
            category="Hardware & Peripherals",
            priority="P3",
            assigned_team="Network Operations",
            needs_escalation=False,
            missing_information=(
                "network_location",
            ),
            next_best_action="Verify the network printer's IP assignment and print server configuration",
            remediation_steps=(
                "Ping the printer IP to verify network connectivity",
                "Check the print server for the printer's status and shared configuration",
                "Verify DHCP lease hasn't changed the printer's IP address",
                "Re-add the printer via the print server share or direct IP",
                "If DNS/DHCP issue, assign a static IP reservation for the printer",
            ),
        ),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 8. Bluetooth headset won't pair after update
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="hardware-008",
        subjects=(
            "Bluetooth headset can't pair with laptop",
            "Jabra headset stopped connecting after Windows update",
        ),
        descriptions=(
            "My Jabra Evolve2 75 won't pair with my laptop anymore. It was working fine before the Windows "
            "update last Tuesday. Bluetooth is turned on, the headset is in pairing mode, but my laptop "
            "can't discover it. I have Teams calls all day.",
            "Bluetooth headset connectivity broken. My laptop no longer detects my headset. I've tried "
            "forgetting the device and re-pairing, but it's not even showing in the Bluetooth discovery "
            "list. Laptop: Surface Pro 9, Headset: Poly Voyager Focus 2.",
        ),
        gold=ScenarioGold(
            category="Hardware & Peripherals",
            priority="P3",
            assigned_team="Endpoint Engineering",
            needs_escalation=False,
            missing_information=(
                "device_info",
            ),
            next_best_action="Update Bluetooth drivers and reset the pairing between the headset and laptop",
            remediation_steps=(
                "Check if the Bluetooth driver was updated or replaced by the Windows update",
                "Roll back or update the Bluetooth adapter driver",
                "Remove all paired devices and restart the Bluetooth service",
                "Put headset in pairing mode and attempt a fresh connection",
                "If Bluetooth adapter is malfunctioning, test with a USB Bluetooth dongle as workaround",
            ),
        ),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 9. Webcam shows black screen in Teams calls
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="hardware-009",
        subjects=(
            "Camera shows black screen in Teams",
            "Webcam not working — just a black image",
        ),
        descriptions=(
            "My built-in webcam shows a completely black screen in Teams video calls. The camera indicator "
            "light turns on, and Teams says it detects the camera, but the preview and what others see is "
            "just black. Audio works fine.",
            "Laptop camera stopped working for video calls. It was fine until yesterday. Now I just see a "
            "black square where my video should be. I've tried Teams, Zoom, and the Windows Camera app — "
            "all show black. Restarted twice, no change.",
        ),
        gold=ScenarioGold(
            category="Hardware & Peripherals",
            priority="P3",
            assigned_team="Endpoint Engineering",
            needs_escalation=False,
            missing_information=(
                "device_info",
                "application_version",
            ),
            next_best_action="Check camera driver and privacy settings, then run hardware diagnostics",
            remediation_steps=(
                "Check Windows privacy settings to ensure camera access is enabled for apps",
                "Verify the camera is not disabled in Device Manager",
                "Update or reinstall the camera driver",
                "Test with the Windows Camera app to isolate from Teams",
                "If driver updates don't help, run hardware diagnostics on the camera module",
            ),
        ),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 10. Laptop overheating during video calls
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="hardware-010",
        subjects=(
            "Laptop gets extremely hot during Teams calls",
            "Overheating and fan noise during video meetings",
        ),
        descriptions=(
            "My laptop gets dangerously hot during Teams meetings with video on. The fans spin at max speed "
            "and it's so loud people on the call can hear them. Sometimes the laptop throttles and the "
            "video becomes choppy. It's a 2-year-old Dell Latitude 7430.",
            "Overheating problem — during any video call lasting more than 20 minutes, my laptop thermal "
            "throttles and everything slows to a crawl. The bottom of the laptop is too hot to touch. "
            "Started happening about a month ago.",
        ),
        gold=ScenarioGold(
            category="Hardware & Peripherals",
            priority="P3",
            assigned_team="Endpoint Engineering",
            needs_escalation=False,
            missing_information=(
                "device_info",
            ),
            next_best_action="Run thermal diagnostics and check for dust buildup or degraded thermal paste",
            remediation_steps=(
                "Run hardware thermal diagnostics to check temperature readings",
                "Clean the air vents and fan with compressed air",
                "Check if BIOS and thermal management firmware are up to date",
                "Verify no CPU-intensive background processes are running during calls",
                "If thermal paste is degraded, schedule internal cleaning or device replacement",
            ),
        ),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 11. Keyboard keys sticking on Surface device
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="hardware-011",
        subjects=(
            "Surface keyboard keys sticking and unresponsive",
            "Several keys on my Surface Pro Type Cover not working",
        ),
        descriptions=(
            "The 'E', 'R', and 'T' keys on my Surface Pro Type Cover are sticking and sometimes don't "
            "register at all. I have to press really hard. There was no spill or damage. I think the "
            "keyboard cover is just wearing out — it's about 2 years old.",
            "Multiple keys on my Surface keyboard are intermittently unresponsive. I'm a fast typer and "
            "this is causing constant errors. Keys affected: space bar, backspace, and left shift. Makes "
            "coding impossible.",
        ),
        gold=ScenarioGold(
            category="Hardware & Peripherals",
            priority="P3",
            assigned_team="Endpoint Engineering",
            needs_escalation=False,
            missing_information=(
                "device_info",
            ),
            next_best_action="Replace the Surface Type Cover keyboard due to mechanical key failure",
            remediation_steps=(
                "Verify the issue by testing in the UEFI/BIOS screen to rule out software",
                "Clean the keyboard connector and reattach the Type Cover",
                "Test with a different Type Cover to confirm it's a keyboard issue",
                "If confirmed faulty, order a replacement Type Cover",
                "Provide a USB keyboard as temporary workaround",
            ),
        ),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 12. Trackpad erratic behavior — cursor jumping
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="hardware-012",
        subjects=(
            "Trackpad cursor jumping around randomly",
            "Erratic trackpad behavior on laptop",
        ),
        descriptions=(
            "My laptop trackpad is moving the cursor randomly. While I'm typing, the cursor will suddenly "
            "jump to another part of the screen and I end up typing in the wrong place. Really frustrating. "
            "Using an external mouse is fine but I need the trackpad for travel.",
            "Trackpad on my ThinkPad is behaving erratically — the cursor drifts to the left on its own and "
            "clicks sometimes register in the wrong place. I've tried adjusting sensitivity settings and "
            "disabling palm rejection but nothing helps.",
        ),
        gold=ScenarioGold(
            category="Hardware & Peripherals",
            priority="P3",
            assigned_team="Endpoint Engineering",
            needs_escalation=False,
            missing_information=(
                "device_info",
            ),
            next_best_action="Update trackpad drivers and run diagnostics to determine if hardware replacement is needed",
            remediation_steps=(
                "Update the touchpad/trackpad driver to the latest version",
                "Check touchpad sensitivity and palm rejection settings",
                "Run hardware diagnostics on the input devices",
                "Test if the issue persists in BIOS/UEFI to confirm hardware fault",
                "If hardware fault confirmed, schedule device repair or replacement",
            ),
        ),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 13. External monitor flickering at 4K resolution
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="hardware-013",
        subjects=(
            "External monitor flickering when set to 4K",
            "Monitor display flickers intermittently",
        ),
        descriptions=(
            "My LG 27-inch 4K monitor flickers every few seconds when connected to my laptop through the "
            "dock. It's fine at 1080p but flickers at 4K resolution. I need 4K for the design work I do. "
            "Using a DisplayPort cable.",
            "Intermittent screen flickering on my external Dell U2723QE 4K monitor. Happens every 10-30 "
            "seconds — the screen goes black for a split second then comes back. Started after upgrading to "
            "a new USB-C cable.",
        ),
        gold=ScenarioGold(
            category="Hardware & Peripherals",
            priority="P3",
            assigned_team="Endpoint Engineering",
            needs_escalation=False,
            missing_information=(
                "device_info",
                "configuration_details",
            ),
            next_best_action="Test different cables and refresh rates to isolate the 4K display flickering issue",
            remediation_steps=(
                "Try a different DisplayPort or USB-C cable rated for 4K@60Hz",
                "Update the graphics driver and monitor firmware",
                "Try reducing the refresh rate from 60Hz to 30Hz to test if bandwidth is the issue",
                "Check if the dock supports 4K output at the desired refresh rate",
                "If cable and settings are correct, test the monitor with a different source",
            ),
        ),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 14. New laptop request for incoming hire
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="hardware-014",
        subjects=(
            "New laptop needed for upcoming hire",
            "Equipment request — new employee starting April 15",
        ),
        descriptions=(
            "We have a new senior analyst starting April 15 on the Risk Management team. They need a "
            "standard analyst laptop setup — Dell Latitude or equivalent, dual monitor capable, with "
            "docking station. Hiring manager: Janet Liu.",
            "Requesting a new laptop for an incoming team member. Start date: April 15. Role: Software "
            "Engineer in the Trading Systems team. They'll need a higher-spec machine with 32GB RAM for "
            "development work.",
        ),
        gold=ScenarioGold(
            category="Hardware & Peripherals",
            priority="P4",
            assigned_team="Endpoint Engineering",
            needs_escalation=False,
            missing_information=(),
            next_best_action="Order and provision a laptop per the standard configuration for the specified role",
            remediation_steps=(
                "Verify the new hire details and start date with HR",
                "Select the appropriate laptop model based on role requirements",
                "Order the device from the approved vendor catalog",
                "Pre-configure the device with the standard image and required software",
                "Schedule delivery and desk setup before the start date",
            ),
        ),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 15. Laptop warranty claim — motherboard failure
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="hardware-015",
        subjects=(
            "Laptop motherboard failure — under warranty",
            "ThinkPad dead — need warranty repair",
        ),
        descriptions=(
            "My ThinkPad X1 Carbon just died. Won't turn on at all — no lights, no fan, nothing. I've tried "
            "a different charger, held the power button for 30 seconds, done the pin-hole reset. It's only "
            "10 months old and should be under warranty. Asset tag: LAP-5523.",
            "Laptop completely dead. No signs of life. Was working fine at 5 PM yesterday, this morning "
            "it's a paperweight. It's a relatively new HP EliteBook 860, purchased 8 months ago. Should "
            "still be under manufacturer warranty.",
        ),
        gold=ScenarioGold(
            category="Hardware & Peripherals",
            priority="P2",
            assigned_team="Endpoint Engineering",
            needs_escalation=False,
            missing_information=(
                "device_info",
            ),
            next_best_action="Initiate vendor warranty RMA and provide a loaner laptop",
            remediation_steps=(
                "Verify the device serial number and warranty status",
                "Attempt hardware diagnostics if any LEDs or power indicators respond",
                "Initiate a warranty repair/replacement with the vendor",
                "Provide a loaner laptop with the user's profile configuration",
                "Track the warranty repair and arrange data recovery if needed",
            ),
        ),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 16. Company iPhone won't sync email
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="hardware-016",
        subjects=(
            "Work iPhone not syncing email anymore",
            "Company mobile device email sync broken",
        ),
        descriptions=(
            "My company-managed iPhone 14 stopped syncing Outlook email yesterday. Calendar and contacts "
            "still sync, but no new emails are arriving. I've tried removing and re-adding the account. I "
            "rely on this for after-hours client communications.",
            "The Intune-managed iPhone I was issued isn't pulling new emails. Notifications stopped about 2 "
            "days ago. I can see emails on my laptop in Outlook but not on the phone. I've checked — it's "
            "connected to WiFi and cellular data.",
        ),
        gold=ScenarioGold(
            category="Hardware & Peripherals",
            priority="P3",
            assigned_team="Endpoint Engineering",
            needs_escalation=False,
            missing_information=(
                "device_info",
                "application_version",
            ),
            next_best_action="Check Intune device compliance and Exchange ActiveSync configuration for the mobile device",
            remediation_steps=(
                "Verify the device compliance status in Intune",
                "Check Exchange ActiveSync partnership status for the device",
                "Verify the Outlook mobile app is up to date",
                "Remove and re-create the Outlook mail profile on the device",
                "If persistent, remove and re-enroll the device in Intune",
            ),
        ),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 17. Docking station USB ports intermittently dropping
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="hardware-017",
        subjects=(
            "Dock USB ports keep disconnecting",
            "Peripherals drop out randomly from docking station",
        ),
        descriptions=(
            "My docking station USB ports keep dropping out for a second then reconnecting. I hear the "
            "Windows disconnect/reconnect sound every 5-10 minutes. It disconnects my keyboard, mouse, and "
            "external hard drive simultaneously. Really disruptive.",
            "USB devices connected to my Dell WD22TB4 dock randomly disconnect and reconnect throughout the "
            "day. This causes me to lose my place when typing and interrupts file transfers. The dock's "
            "firmware was updated last week.",
        ),
        gold=ScenarioGold(
            category="Hardware & Peripherals",
            priority="P3",
            assigned_team="Endpoint Engineering",
            needs_escalation=False,
            missing_information=(
                "device_info",
            ),
            next_best_action="Troubleshoot USB power delivery and dock firmware to resolve intermittent disconnections",
            remediation_steps=(
                "Check the docking station firmware version and update if available",
                "Verify the USB power management settings are not set to save power",
                "Disable USB selective suspend in Windows power settings",
                "Try a different Thunderbolt/USB-C cable between laptop and dock",
                "If issue persists, replace the docking station",
            ),
        ),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 18. Monitor arm broke — ergonomic equipment request
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="hardware-018",
        subjects=(
            "Monitor arm broke — need replacement",
            "Ergonomic equipment request: monitor arm",
        ),
        descriptions=(
            "The monitor arm on my desk broke — the tension mechanism gave out and my 27-inch monitor is "
            "now sitting at an awkward angle. I can't adjust the height anymore. Can I get a replacement "
            "arm? I'm having neck strain from the current position.",
            "My Humanscale M8 monitor arm snapped at the joint. The monitor is now propped up on a stack of "
            "books which isn't ideal ergonomically. I work at my desk 9 hours a day and this is causing "
            "discomfort.",
        ),
        gold=ScenarioGold(
            category="Hardware & Peripherals",
            priority="P4",
            assigned_team="Endpoint Engineering",
            needs_escalation=False,
            missing_information=(),
            next_best_action="Order a replacement monitor arm from the approved ergonomic equipment catalog",
            remediation_steps=(
                "Document the broken equipment for asset tracking",
                "Order a replacement monitor arm from the approved vendor",
                "If user reports pain or discomfort, expedite via ergonomic accommodation process",
                "Schedule installation of the new monitor arm",
                "Dispose of the broken arm per e-waste policy",
            ),
        ),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 19. Conference room projector failure before client meeting
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="hardware-019",
        subjects=(
            "URGENT: Boardroom projector dead — client meeting in 30 min",
            "Main conference room projector not working",
        ),
        descriptions=(
            "The projector in the Main Boardroom is completely dead. No power, no lights. We have a $2.3M "
            "client contract review with external partners in 25 minutes. We need either a fix or a "
            "portable backup projector brought up immediately.",
            "EMERGENCY — the executive boardroom projector just died. Important investor presentation "
            "starts in 20 minutes. CEO and CFO are presenting. Need immediate on-site support with a backup "
            "display solution.",
        ),
        gold=ScenarioGold(
            category="Hardware & Peripherals",
            priority="P1",
            assigned_team="Endpoint Engineering",
            needs_escalation=True,
            missing_information=(
                "device_info",
            ),
            next_best_action="Dispatch immediate on-site support with a backup projector or large display to the boardroom",
            remediation_steps=(
                "Dispatch on-site technician to the boardroom immediately",
                "Bring a portable backup projector or large display from IT supply",
                "Check power source and cable connections on the existing projector",
                "Set up backup display solution before the meeting starts",
                "After the meeting, schedule full diagnostic of the boardroom projector",
            ),
        ),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 20. Laptop hard drive making clicking noises
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="hardware-020",
        subjects=(
            "Hard drive clicking sounds — worried about data loss",
            "Laptop making clicking noises from storage",
        ),
        descriptions=(
            "My laptop has been making a clicking/ticking sound for the past two days. I think it's coming "
            "from the hard drive area. The laptop also seems slower than usual. I'm worried about losing my "
            "data — I have a lot of client files that aren't backed up to OneDrive.",
            "Hearing intermittent clicking from my laptop when it's doing disk-intensive operations. "
            "Performance has degraded noticeably. I know this could mean the drive is failing. Please help "
            "before I lose everything.",
        ),
        gold=ScenarioGold(
            category="Hardware & Peripherals",
            priority="P2",
            assigned_team="Endpoint Engineering",
            needs_escalation=False,
            missing_information=(
                "device_info",
            ),
            next_best_action="Immediately back up all data and run drive diagnostics — clicking indicates imminent drive failure",
            remediation_steps=(
                "Immediately back up all user data to OneDrive or external storage",
                "Run SMART disk diagnostics to check drive health",
                "If SMART shows errors or degradation, schedule immediate drive replacement",
                "Clone the drive to a new SSD if data recovery is needed",
                "Replace the failing drive and restore from backup",
            ),
        ),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 21. Multiple laptops failing in same department
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="hardware-021",
        subjects=(
            "4 laptops failed this week in Trading — bad batch?",
            "Multiple hardware failures in same team",
        ),
        descriptions=(
            "We've had 4 laptops in the Trading department fail in the past 5 days — all with different "
            "symptoms (BSOD, battery swelling, boot failure, screen artifacts). They're all Dell Latitude "
            "5540s from the same purchase batch last September. Could we have a bad batch?",
            "This is getting ridiculous — third laptop failure in the Risk Management team this week. All "
            "purchased around the same time. Starting to wonder if there's a common defect. The team of 20 "
            "people is losing productivity. Need a proactive plan.",
        ),
        gold=ScenarioGold(
            category="Hardware & Peripherals",
            priority="P2",
            assigned_team="Endpoint Engineering",
            needs_escalation=True,
            missing_information=(
                "device_info",
                "affected_users",
            ),
            next_best_action="Investigate a potential batch defect and coordinate with the vendor for a recall or bulk replacement",
            remediation_steps=(
                "Collect serial numbers and failure details for all affected devices",
                "Check if all devices are from the same purchase order and manufacturing batch",
                "Contact the vendor to report potential batch defect",
                "Proactively inspect remaining devices from the same batch",
                "Prepare replacement devices and expedited swap plan for the affected team",
            ),
        ),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 22. Laptop stolen — needs remote wipe
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="hardware-022",
        subjects=(
            "Laptop stolen from car — need remote wipe ASAP",
            "URGENT: Company laptop theft — data at risk",
        ),
        descriptions=(
            "My company laptop was stolen from my car last night. It has client financial data and access "
            "to our trading systems. The laptop is BitLocker encrypted but I need it remotely wiped ASAP. "
            "I've filed a police report (case #2026-MPD-48291).",
            "Reporting a stolen laptop. Someone broke into my car while I was at a restaurant and took my "
            "work bag with the laptop. It has sensitive compliance documents on it. I need this device "
            "wiped and blocked from accessing our network immediately.",
        ),
        gold=ScenarioGold(
            category="Hardware & Peripherals",
            priority="P1",
            assigned_team="Endpoint Engineering",
            needs_escalation=True,
            missing_information=(),
            next_best_action="Initiate remote wipe via Intune and revoke all access tokens associated with the device",
            remediation_steps=(
                "Initiate remote wipe command via Intune immediately",
                "Disable the device in Entra ID to prevent authentication",
                "Revoke all active sessions and refresh tokens for the user",
                "Notify Security Operations for potential data exposure assessment",
                "Provision a replacement laptop and assist with re-setup",
            ),
        ),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 23. Barcode scanner not working at front desk
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="hardware-023",
        subjects=(
            "Barcode scanner at reception not scanning",
            "Front desk badge scanner broken",
        ),
        descriptions=(
            "The barcode scanner at the front desk reception area isn't reading visitor badge barcodes. We "
            "use this to check in guests and it's been broken since yesterday. We're manually logging "
            "visitors which is slow and error-prone.",
            "Our Honeywell barcode scanner at the Building A reception desk stopped working. The red scan "
            "light activates but it doesn't register any barcodes. We tried it on different barcodes — same "
            "result. Visitor check-in is impacted.",
        ),
        gold=ScenarioGold(
            category="Hardware & Peripherals",
            priority="P3",
            assigned_team="Endpoint Engineering",
            needs_escalation=False,
            missing_information=(
                "device_info",
            ),
            next_best_action="Replace or reconfigure the barcode scanner at the reception desk",
            remediation_steps=(
                "Check the USB connection and try a different USB port",
                "Clean the scanner lens with a dry microfiber cloth",
                "Test with a known-good barcode to rule out scanning target issues",
                "Check scanner configuration and driver on the reception PC",
                "If scanner is defective, replace with a spare from inventory",
            ),
        ),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 24. Dual monitor setup request for trading floor
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="hardware-024",
        subjects=(
            "Need dual monitor setup for new trading desk",
            "Request: two additional monitors for trading workstation",
        ),
        descriptions=(
            "We're setting up a new trading desk on Floor 7 and need dual 27-inch 4K monitor setups for 3 "
            "workstations. The traders need high-refresh displays for real-time market data. Monitors, "
            "arms, and appropriate cables needed. Start date: April 1.",
            "Requesting dual monitor configuration for my workstation on the trading floor. I currently "
            "have a single 24-inch monitor but need two screens to efficiently monitor positions and run "
            "the Bloomberg terminal side by side.",
        ),
        gold=ScenarioGold(
            category="Hardware & Peripherals",
            priority="P4",
            assigned_team="Endpoint Engineering",
            needs_escalation=False,
            missing_information=(),
            next_best_action="Order and install dual monitor setup per the trading floor standard configuration",
            remediation_steps=(
                "Verify the monitor specifications required for trading workstations",
                "Order monitors, monitor arms, and necessary cables from the approved catalog",
                "Schedule installation during non-trading hours to minimize disruption",
                "Configure display settings and verify with the user",
                "Update the asset inventory with the new equipment",
            ),
        ),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 25. Laptop fan running constantly
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="hardware-025",
        subjects=(
            "Laptop fan never stops running — very loud",
            "Constant fan noise on my work laptop",
        ),
        descriptions=(
            "My laptop fan has been running at full speed constantly for the past week. It sounds like a "
            "hair dryer. The laptop isn't even doing anything intensive — just Outlook and a browser. It's "
            "so loud my colleagues have complained. HP EliteBook 845 G9.",
            "Fan noise is unbearable on my work laptop. It starts spinning at max RPM the moment I log in "
            "and never slows down. The laptop feels warm but not excessively hot. This didn't happen "
            "before, started randomly last Thursday.",
        ),
        gold=ScenarioGold(
            category="Hardware & Peripherals",
            priority="P3",
            assigned_team="Endpoint Engineering",
            needs_escalation=False,
            missing_information=(
                "device_info",
            ),
            next_best_action="Clean the laptop vents and check for thermal management or background process issues",
            remediation_steps=(
                "Check Task Manager for any processes consuming high CPU",
                "Clean air intake and exhaust vents with compressed air",
                "Update BIOS and thermal management firmware",
                "Check fan health in the hardware diagnostics utility",
                "If fan is malfunctioning, schedule internal hardware cleaning or replacement",
            ),
        ),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 26. Mouse double-clicking on single click
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="hardware-026",
        subjects=(
            "Mouse registers double-click on single click",
            "Mouse clicking issue — opens everything twice",
        ),
        descriptions=(
            "My Logitech MX Master 3 is double-clicking when I single click. It opens folders twice, "
            "selects text weirdly, and makes drag-and-drop almost impossible. I've changed the double-click "
            "speed settings in Windows but that doesn't help. Seems like a hardware defect.",
            "My wireless mouse is registering double-clicks. Every single click opens things twice or "
            "deselects what I just selected. It's maddening. The mouse is about 18 months old. Can I get a "
            "replacement?",
        ),
        gold=ScenarioGold(
            category="Hardware & Peripherals",
            priority="P4",
            assigned_team="Endpoint Engineering",
            needs_escalation=False,
            missing_information=(
                "device_info",
            ),
            next_best_action="Replace the mouse with a new unit from inventory — double-click defect is a known hardware failure",
            remediation_steps=(
                "Verify the issue is hardware by testing with a different mouse",
                "Check if the Logitech software has a debounce or click speed setting",
                "If hardware fault confirmed, provide a replacement mouse from IT inventory",
                "Dispose of the defective mouse per e-waste policy",
                "Order replacement stock if inventory is low",
            ),
        ),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 27. Smart card reader not detecting PIV card
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="hardware-027",
        subjects=(
            "Smart card reader doesn't detect my badge",
            "PIV card not recognized by laptop reader",
        ),
        descriptions=(
            "My laptop's built-in smart card reader doesn't detect my PIV card anymore. I need it for "
            "accessing the classified data terminal on the secure floor. The card works fine at the door "
            "badge readers, just not in the laptop. I've tried cleaning the contacts.",
            "Can't use my smart card for certificate-based login. The card reader on my laptop shows no "
            "activity when I insert the PIV card. Windows doesn't prompt for the PIN. This is blocking my "
            "access to the secure compliance systems.",
        ),
        gold=ScenarioGold(
            category="Hardware & Peripherals",
            priority="P3",
            assigned_team="Endpoint Engineering",
            needs_escalation=False,
            missing_information=(
                "device_info",
            ),
            next_best_action="Troubleshoot the smart card reader driver and test with an external USB reader",
            remediation_steps=(
                "Check Device Manager to verify the smart card reader driver is installed",
                "Update the smart card reader driver to the latest version",
                "Test with a different PIV card to rule out card damage",
                "Try an external USB smart card reader as a workaround",
                "If built-in reader is defective, schedule hardware repair or provide external reader",
            ),
        ),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 28. Server room UPS beeping
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="hardware-028",
        subjects=(
            "UPS in server room beeping — battery warning",
            "Server room UPS alarm going off",
        ),
        descriptions=(
            "The APC UPS unit in the Building B server room (rack 4B) has been beeping for the past hour. "
            "The display shows 'Replace Battery' warning. This UPS protects our on-prem database servers. "
            "If it fails during a power event, we lose the production database.",
            "UPS alarm sounding in the 3rd floor server closet. Indicator shows battery capacity at 15% and "
            "replacement needed. This unit backs up the network switches for Floors 2-4. If power dips, "
            "we'll lose network for ~150 people.",
        ),
        gold=ScenarioGold(
            category="Hardware & Peripherals",
            priority="P2",
            assigned_team="Endpoint Engineering",
            needs_escalation=False,
            missing_information=(
                "device_info",
            ),
            next_best_action="Order replacement UPS batteries immediately and schedule off-hours battery swap",
            remediation_steps=(
                "Acknowledge the UPS alarm and document the current battery status",
                "Order replacement batteries for the specific UPS model",
                "Schedule the battery replacement during a maintenance window",
                "Verify UPS output and transfer time after battery replacement",
                "Set up proactive battery monitoring alerts to prevent future surprises",
            ),
        ),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 29. Desktop PC won't POST
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="hardware-029",
        subjects=(
            "Desktop PC won't turn on — no display at all",
            "Desktop not booting — power light on but no POST",
        ),
        descriptions=(
            "My desktop PC in the back office won't POST. Power light comes on and fans spin, but nothing "
            "appears on the monitor. No BIOS splash screen, no beep codes. Monitor works fine with my "
            "laptop. I've tried reseating the RAM and display cable.",
            "My workstation is dead. It powers on (fans and lights), but no display output and no boot "
            "beeps. I swapped monitors and cables — still nothing. This machine runs our department's "
            "scheduling software that no one else has access to.",
        ),
        gold=ScenarioGold(
            category="Hardware & Peripherals",
            priority="P2",
            assigned_team="Endpoint Engineering",
            needs_escalation=False,
            missing_information=(
                "device_info",
            ),
            next_best_action="Attempt hardware diagnostics and determine if motherboard or GPU replacement is needed",
            remediation_steps=(
                "Check all internal cable connections and reseat RAM modules",
                "Try booting with minimum hardware configuration (one RAM stick, no add-in cards)",
                "Test the GPU in a different slot or with an alternative GPU",
                "Run built-in hardware diagnostics via the diagnostic LED codes",
                "If motherboard failure confirmed, initiate replacement and data recovery from storage drive",
            ),
        ),
    ),
    # ──────────────────────────────────────────────────────────────────
    # 30. Laptop touchscreen not responding after drop
    # ──────────────────────────────────────────────────────────────────
    ScenarioDefinition(
        scenario_id="hardware-030",
        subjects=(
            "Touchscreen stopped working after I dropped my laptop",
            "Surface touchscreen unresponsive",
        ),
        descriptions=(
            "I dropped my Surface Pro 9 from about waist height onto the office carpet. The screen looks "
            "fine — no cracks — but the touchscreen is completely unresponsive. The pen doesn't work "
            "either. Mouse and keyboard through the Type Cover work fine.",
            "My convertible laptop's touchscreen stopped working after I accidentally bumped it off my "
            "standing desk. Display looks normal but touch input doesn't register at all. I use touch mode "
            "heavily for annotating documents in client meetings.",
        ),
        gold=ScenarioGold(
            category="Hardware & Peripherals",
            priority="P3",
            assigned_team="Endpoint Engineering",
            needs_escalation=False,
            missing_information=(
                "device_info",
            ),
            next_best_action="Run touch panel diagnostics and determine if the digitizer needs replacement",
            remediation_steps=(
                "Check Device Manager for any errors on the HID touch screen device",
                "Try disabling and re-enabling the touch screen driver",
                "Run the manufacturer's hardware diagnostics on the touch panel",
                "If digitizer is damaged from the drop, initiate repair or replacement",
                "Provide an external touchscreen or loaner device if repair timeline is extended",
            ),
        ),
    ),
]
