"""Hardware & Peripherals category scenarios for eval dataset."""

from ms.evals_core.constants import Category
from ms.evals_core.constants import Channel
from ms.evals_core.constants import MissingInfo
from ms.evals_core.constants import Priority
from ms.evals_core.constants import Team
from ms.evals_core.scenarios.base import ScenarioDefinition


def get_scenarios() -> list[ScenarioDefinition]:
    """Return all Hardware & Peripherals evaluation scenarios."""
    return [
        # ──────────────────────────────────────────────────────────────
        # 1. Swollen battery — safety-critical
        # ──────────────────────────────────────────────────────────────
        ScenarioDefinition(
            scenario_id="hardware_001",
            subject="URGENT: Laptop battery swelling — trackpad pushed up",
            description=(
                "My Dell Latitude 5540 has a visibly swollen battery. The bottom case is bulging and the"
                " trackpad is pushed upward and barely clicks. I noticed it yesterday but today it is worse."
                " The laptop gets extremely hot near the hinge. I am on the 7th floor of the NYC office,"
                " Building 3. Should I keep using it? I have a board deck due tomorrow."
            ),
            category=Category.HARDWARE,
            priority=Priority.P1,
            team=Team.ENDPOINT,
            needs_escalation=True,
            missing_info=[MissingInfo.DEVICE_INFO],
            next_best_action=(
                "Instruct user to power off the laptop immediately, move it away from flammable materials,"
                " and dispatch a technician to safely collect the device"
            ),
            remediation_steps=[
                "Advise the user to shut down and unplug the laptop immediately",
                "Have the user place the device on a non-flammable surface away from people",
                "Dispatch an on-site technician to safely retrieve the laptop",
                "Provide a loaner laptop so the user can continue working",
                "Submit a warranty claim for battery replacement or full device swap",
                "Log the incident in the safety tracking system per compliance requirements",
            ],
            reporter_name="Rachel Novak",
            reporter_email="rachel.novak@contoso.com",
            reporter_department="Wealth Management",
            channel=Channel.PHONE,
            attachments=["swollen_battery_photo.jpg"],
            created_at="2026-03-03T08:22:00Z",
            tags=["safety", "battery", "urgent", "nyc"],
            difficulty="medium",
        ),
        # ──────────────────────────────────────────────────────────────
        # 2. Laptop won't boot — BSOD loop
        # ──────────────────────────────────────────────────────────────
        ScenarioDefinition(
            scenario_id="hardware_002",
            subject="Laptop stuck in boot loop after Windows update",
            description=(
                "Hi team, my ThinkPad X1 Carbon Gen 11 won't boot this morning. It was installing updates"
                " overnight and now it keeps showing the Lenovo splash, then a brief blue recovery screen,"
                " and reboots again. I've tried holding the power button for 30 seconds but same thing."
                " I have a client presentation at 2 PM and all my files are local. Asset tag is CTF-LT-4821."
            ),
            category=Category.HARDWARE,
            priority=Priority.P2,
            team=Team.ENDPOINT,
            needs_escalation=False,
            missing_info=[MissingInfo.ERROR_MESSAGE],
            next_best_action="Attempt Windows Recovery Environment boot and roll back the failed update",
            remediation_steps=[
                "Boot into Windows Recovery Environment using F8 or recovery USB",
                "Attempt to roll back the most recent Windows update",
                "If rollback fails, run Startup Repair from the recovery console",
                "If the device remains unbootable, back up data via recovery USB and reimage",
                "Provide a loaner laptop if repair will take more than 4 hours",
            ],
            reporter_name="James Park",
            reporter_email="james.park@contoso.com",
            reporter_department="Trading",
            channel=Channel.PORTAL,
            created_at="2026-03-04T07:45:00Z",
            tags=["laptop", "boot-loop", "windows-update"],
            difficulty="medium",
        ),
        # ──────────────────────────────────────────────────────────────
        # 3. Cracked laptop screen
        # ──────────────────────────────────────────────────────────────
        ScenarioDefinition(
            scenario_id="hardware_003",
            subject="Screen cracked",
            description=(
                "dropped my laptop bag this morning and now the screen is cracked. big spider web crack on"
                " the left side. can still see part of the desktop on the right half. need this fixed asap"
                " pls. im in london office."
            ),
            category=Category.HARDWARE,
            priority=Priority.P3,
            team=Team.ENDPOINT,
            needs_escalation=False,
            missing_info=[
                MissingInfo.DEVICE_INFO,
                MissingInfo.SCREENSHOT_OR_ATTACHMENT,
                MissingInfo.BUSINESS_IMPACT,
            ],
            next_best_action=(
                "Provide a loaner laptop and arrange screen replacement through the warranty or repair program"
            ),
            remediation_steps=[
                "Confirm the device make, model, and asset tag",
                "Issue a loaner laptop with user profile configured",
                "Submit a repair request to the hardware vendor for screen replacement",
                "Transfer user data to the loaner if needed",
                "Return the repaired device and reclaim the loaner",
            ],
            reporter_name="Oliver Hughes",
            reporter_email="oliver.hughes@contoso.com",
            reporter_department="Marketing",
            channel=Channel.CHAT,
            created_at="2026-03-05T09:10:00Z",
            tags=["laptop", "screen", "physical-damage", "london"],
            difficulty="easy",
        ),
        # ──────────────────────────────────────────────────────────────
        # 4. Laptop overheating during summer — thermal throttling
        # ──────────────────────────────────────────────────────────────
        ScenarioDefinition(
            scenario_id="hardware_004",
            subject="Laptop extremely hot and fans running full blast",
            description=(
                "For the past week my Surface Laptop 5 has been running incredibly hot. The fans spin at"
                " maximum constantly and the keyboard area is almost too hot to touch. Performance has"
                " tanked — Excel takes 15+ seconds to recalculate my pricing models. I sit near the"
                " south-facing windows on floor 8 in the Singapore office and the AC has been spotty."
                " This happens every day from around 1 PM onwards. Asset tag CTF-LT-3192."
            ),
            category=Category.HARDWARE,
            priority=Priority.P3,
            team=Team.ENDPOINT,
            needs_escalation=False,
            missing_info=[MissingInfo.ENVIRONMENT_DETAILS],
            next_best_action=("Run hardware thermal diagnostics and coordinate with Facilities about the AC issue"),
            remediation_steps=[
                "Run vendor thermal diagnostics to check fan and heat sink condition",
                "Clean dust from vents and verify thermal paste integrity",
                "Check for runaway processes consuming excessive CPU",
                "Coordinate with Facilities to address the HVAC issue near the user's desk",
                "If thermals remain critical, replace the thermal module or swap the device",
            ],
            reporter_name="Priya Sharma",
            reporter_email="priya.sharma@contoso.com",
            reporter_department="Quantitative Analysis",
            channel=Channel.PORTAL,
            created_at="2026-03-06T13:30:00Z",
            tags=["laptop", "overheating", "thermal", "singapore"],
            difficulty="medium",
        ),
        # ──────────────────────────────────────────────────────────────
        # 5. Keyboard keys not working
        # ──────────────────────────────────────────────────────────────
        ScenarioDefinition(
            scenario_id="hardware_005",
            subject="Several keys on laptop keyboard stopped working",
            description=(
                "The E, R, and T keys on my HP EliteBook 860 G10 no longer register when pressed. Started"
                " two days ago. I spilled a small amount of coffee near the keyboard last week but cleaned"
                " it up right away. The rest of the keys work fine. Currently using an external USB keyboard"
                " as a workaround. Asset tag CTF-LT-5540."
            ),
            category=Category.HARDWARE,
            priority=Priority.P3,
            team=Team.ENDPOINT,
            needs_escalation=False,
            missing_info=[MissingInfo.STEPS_TO_REPRODUCE],
            next_best_action="Schedule keyboard replacement under warranty or accidental damage coverage",
            remediation_steps=[
                "Verify the issue is hardware-related by booting into BIOS and testing the keys",
                "Check if an external keyboard is already in use as a workaround",
                "Submit a repair ticket for keyboard replacement",
                "If under warranty, arrange vendor on-site repair",
                "If out of warranty, order a replacement keyboard module and schedule the swap",
            ],
            reporter_name="David Chen",
            reporter_email="david.chen@contoso.com",
            reporter_department="Compliance",
            channel=Channel.PORTAL,
            created_at="2026-03-06T10:15:00Z",
            tags=["laptop", "keyboard", "hardware-failure"],
            difficulty="easy",
        ),
        # ──────────────────────────────────────────────────────────────
        # 6. External monitor flickering
        # ──────────────────────────────────────────────────────────────
        ScenarioDefinition(
            scenario_id="hardware_006",
            subject="Monitor keeps flickering on and off",
            description=(
                "My Dell U2723QE monitor has been flickering intermittently since Monday. The screen goes"
                " black for about 2 seconds then comes back. Happens roughly every 10-15 minutes. I've"
                " tried a different DisplayPort cable and the issue persists. Connected through the Lenovo"
                " USB-C dock. Other monitor on the same dock works fine. NYC office, floor 4."
            ),
            category=Category.HARDWARE,
            priority=Priority.P3,
            team=Team.ENDPOINT,
            needs_escalation=False,
            missing_info=[MissingInfo.DEVICE_INFO],
            next_best_action="Test the monitor with a direct connection bypassing the dock to isolate the fault",
            remediation_steps=[
                "Test the monitor connected directly to the laptop bypassing the dock",
                "Try a different port on the docking station",
                "Update the docking station firmware and display drivers",
                "If the issue persists with a direct connection, replace the monitor",
                "If the issue only occurs through the dock, replace the docking station",
            ],
            reporter_name="Sarah Mitchell",
            reporter_email="sarah.mitchell@contoso.com",
            reporter_department="Finance",
            channel=Channel.EMAIL,
            created_at="2026-03-07T11:00:00Z",
            tags=["monitor", "flickering", "display", "dock"],
            difficulty="medium",
        ),
        # ──────────────────────────────────────────────────────────────
        # 7. Multi-monitor setup not detected
        # ──────────────────────────────────────────────────────────────
        ScenarioDefinition(
            scenario_id="hardware_007",
            subject="Second monitor not detected after office move",
            description=(
                "I moved desks last Friday to floor 6 in the London office. Since then my second monitor"
                " (the one on the right) isn't detected by Windows. It shows 'No Signal' on the screen."
                " The left monitor works. Both are connected through my ThinkPad USB-C dock. I've restarted"
                " multiple times. DisplayPort cables look fine, they click in securely."
            ),
            category=Category.HARDWARE,
            priority=Priority.P3,
            team=Team.ENDPOINT,
            needs_escalation=False,
            missing_info=[MissingInfo.DEVICE_INFO, MissingInfo.CONFIGURATION_DETAILS],
            next_best_action="Verify dock firmware version and test monitor with alternate cable and port",
            remediation_steps=[
                "Swap the two monitors' cables to determine if the issue follows the cable or the port",
                "Try a different port on the docking station for the second monitor",
                "Update docking station firmware to the latest version",
                "Check Display Settings in Windows and attempt to detect the second display manually",
                "If unresolved, test with a known-good dock to isolate the fault",
            ],
            reporter_name="Emma Blackwell",
            reporter_email="emma.blackwell@contoso.com",
            reporter_department="Legal",
            channel=Channel.PORTAL,
            created_at="2026-03-10T08:45:00Z",
            tags=["monitor", "multi-monitor", "dock", "london"],
            difficulty="easy",
        ),
        # ──────────────────────────────────────────────────────────────
        # 8. Docking station USB-C not charging
        # ──────────────────────────────────────────────────────────────
        ScenarioDefinition(
            scenario_id="hardware_008",
            subject="Dock not charging my laptop anymore",
            description=(
                "My Lenovo ThinkPad USB-C Dock Gen 2 stopped charging my laptop about 3 days ago. The"
                " displays and peripherals still work through the dock, but the laptop battery drains while"
                " docked. I have to plug in the separate power adapter. The dock power light is on."
                " Model 40AS. NYC, Building 2, floor 5."
            ),
            category=Category.HARDWARE,
            priority=Priority.P3,
            team=Team.ENDPOINT,
            needs_escalation=False,
            missing_info=[MissingInfo.DEVICE_INFO],
            next_best_action=("Test with a replacement dock power supply and update dock firmware"),
            remediation_steps=[
                "Verify the dock's power adapter output matches the required wattage for the laptop",
                "Test with a known-good dock power supply",
                "Update the docking station firmware via Lenovo Vantage",
                "Try a different USB-C cable between the dock and laptop",
                "If charging still fails, replace the docking station",
            ],
            reporter_name="Marcus Williams",
            reporter_email="marcus.williams@contoso.com",
            reporter_department="Operations",
            channel=Channel.CHAT,
            created_at="2026-03-10T14:20:00Z",
            tags=["dock", "charging", "usb-c"],
            difficulty="easy",
        ),
        # ──────────────────────────────────────────────────────────────
        # 9. Docking station ports not working
        # ──────────────────────────────────────────────────────────────
        ScenarioDefinition(
            scenario_id="hardware_009",
            subject="USB ports on dock completely dead",
            description=(
                "None of the USB-A ports on my docking station work. Mouse, keyboard, webcam — nothing is"
                " recognized when plugged in. The dock display output and charging still work. I've tried"
                " unplugging the dock and reconnecting, restarting my laptop, different USB devices. It was"
                " working fine yesterday afternoon. ThinkPad Universal USB-C Dock, Singapore office."
            ),
            category=Category.HARDWARE,
            priority=Priority.P3,
            team=Team.ENDPOINT,
            needs_escalation=False,
            missing_info=[MissingInfo.DEVICE_INFO, MissingInfo.TIMESTAMP],
            next_best_action="Reset the dock by disconnecting all cables for 30 seconds and update firmware",
            remediation_steps=[
                "Perform a full dock reset by disconnecting all cables including power for 30 seconds",
                "Reconnect and check Device Manager for USB host controller errors",
                "Update dock firmware to the latest version",
                "Test the USB ports with a known-good device",
                "If ports remain dead, replace the docking station",
            ],
            reporter_name="Wei Lin Tan",
            reporter_email="weilin.tan@contoso.com",
            reporter_department="Risk Management",
            channel=Channel.PORTAL,
            created_at="2026-03-11T09:00:00Z",
            tags=["dock", "usb", "ports", "singapore"],
            difficulty="easy",
        ),
        # ──────────────────────────────────────────────────────────────
        # 10. Mouse erratic / jumping
        # ──────────────────────────────────────────────────────────────
        ScenarioDefinition(
            scenario_id="hardware_010",
            subject="Wireless mouse cursor jumping all over the screen",
            description=(
                "My Logitech MX Master 3S cursor keeps jumping randomly across the screen. It happens every"
                " few seconds and makes it impossible to click on anything accurately. New batteries didn't"
                " help. I'm using the Logitech Unifying receiver plugged into my dock. This started after IT"
                " pushed something to my laptop last week."
            ),
            category=Category.HARDWARE,
            priority=Priority.P4,
            team=Team.ENDPOINT,
            needs_escalation=False,
            missing_info=[
                MissingInfo.DEVICE_INFO,
                MissingInfo.ENVIRONMENT_DETAILS,
                MissingInfo.NETWORK_LOCATION,
            ],
            next_best_action=("Try the receiver directly in the laptop USB port and re-pair the mouse"),
            remediation_steps=[
                "Move the Unifying receiver from the dock to a direct USB port on the laptop",
                "Re-pair the mouse through Logitech Options+ software",
                "Check for wireless interference from nearby devices",
                "Test on a different surface or mouse pad",
                "If issue persists, replace the mouse",
            ],
            reporter_name="Angela Torres",
            reporter_email="angela.torres@contoso.com",
            reporter_department="HR",
            channel=Channel.CHAT,
            created_at="2026-03-11T15:45:00Z",
            tags=["mouse", "peripheral", "wireless"],
            difficulty="easy",
        ),
        # ──────────────────────────────────────────────────────────────
        # 11. Headset audio cuts out in Teams calls
        # ──────────────────────────────────────────────────────────────
        ScenarioDefinition(
            scenario_id="hardware_011",
            subject="Headset audio keeps cutting out during Teams meetings",
            description=(
                "I'm having a really frustrating issue with my Jabra Evolve2 75 headset. During Microsoft"
                " Teams calls, the audio drops out every 30-60 seconds for about 2-3 seconds. Other people"
                " on the call say they can't hear me during the dropouts either. It's fine for Spotify and"
                " YouTube. I'm connected via Bluetooth. This has been happening for about a week. I'm in"
                " back-to-back client calls all day and this is embarrassing. NYC office, floor 3."
            ),
            category=Category.HARDWARE,
            priority=Priority.P3,
            team=Team.ENDPOINT,
            needs_escalation=False,
            missing_info=[MissingInfo.DEVICE_INFO],
            next_best_action="Switch the headset to the USB dongle connection instead of Bluetooth and update firmware",
            remediation_steps=[
                "Switch from Bluetooth to the Jabra Link 380 USB dongle for a more stable connection",
                "Update headset firmware through Jabra Direct software",
                "Set the headset as the default communication device in Windows Sound settings",
                "Check Teams audio device settings to ensure the correct device is selected",
                "If dropouts continue on the dongle, replace the headset",
            ],
            reporter_name="Michael Russo",
            reporter_email="michael.russo@contoso.com",
            reporter_department="Client Services",
            channel=Channel.EMAIL,
            created_at="2026-03-12T08:30:00Z",
            tags=["headset", "audio", "teams", "bluetooth"],
            difficulty="medium",
        ),
        # ──────────────────────────────────────────────────────────────
        # 12. Webcam black screen
        # ──────────────────────────────────────────────────────────────
        ScenarioDefinition(
            scenario_id="hardware_012",
            subject="Camera shows black screen in all apps",
            description=(
                "My laptop camera just shows a black screen. Teams, Zoom, even the Windows Camera app —"
                " all black. There's no physical privacy shutter on my model (HP EliteBook 840 G9). I've"
                " checked the privacy settings and the camera is enabled. Restarted twice."
            ),
            category=Category.HARDWARE,
            priority=Priority.P4,
            team=Team.ENDPOINT,
            needs_escalation=False,
            missing_info=[
                MissingInfo.DEVICE_INFO,
                MissingInfo.TIMESTAMP,
                MissingInfo.STEPS_TO_REPRODUCE,
            ],
            next_best_action="Check Device Manager for camera driver status and reinstall the driver",
            remediation_steps=[
                "Verify the camera is not disabled in BIOS settings",
                "Check Device Manager for the camera device and note any error codes",
                "Uninstall and reinstall the camera driver",
                "Test in Safe Mode to rule out third-party software conflicts",
                "If still black, the camera module may need hardware replacement",
            ],
            reporter_name="Lisa Okonkwo",
            reporter_email="lisa.okonkwo@contoso.com",
            reporter_department="Product Management",
            channel=Channel.PORTAL,
            created_at="2026-03-12T10:00:00Z",
            tags=["webcam", "camera", "laptop"],
            difficulty="easy",
        ),
        # ──────────────────────────────────────────────────────────────
        # 13. Network printer offline
        # ──────────────────────────────────────────────────────────────
        ScenarioDefinition(
            scenario_id="hardware_013",
            subject="Floor 5 printer showing offline — entire team affected",
            description=(
                "The HP LaserJet Enterprise M611 on floor 5 (printer name NYC-PRN-F5-01) has been showing"
                " as offline since this morning. About 20 people on this floor use it and we have"
                " compliance documents that need to be printed and signed today. The printer display shows"
                " it's online and connected. We've tried restarting it. The print queue on everyone's"
                " machine is stuck."
            ),
            category=Category.HARDWARE,
            priority=Priority.P2,
            team=Team.NETWORK_OPS,
            needs_escalation=False,
            missing_info=[MissingInfo.ERROR_MESSAGE],
            next_best_action=("Check the print server queue and network connectivity to the printer"),
            remediation_steps=[
                "Verify network connectivity by pinging the printer IP address",
                "Check the print server for stuck jobs and restart the print spooler service",
                "Clear all queued print jobs on the server",
                "Restart the printer and verify it re-registers on the network",
                "Push a driver update to affected workstations if needed",
                "Confirm users can print a test page successfully",
            ],
            reporter_name="Daniel Foster",
            reporter_email="daniel.foster@contoso.com",
            reporter_department="Compliance",
            channel=Channel.PHONE,
            created_at="2026-03-13T09:15:00Z",
            tags=["printer", "network-printer", "multi-user", "nyc"],
            difficulty="medium",
        ),
        # ──────────────────────────────────────────────────────────────
        # 14. Printer paper jam recurring
        # ──────────────────────────────────────────────────────────────
        ScenarioDefinition(
            scenario_id="hardware_014",
            subject="Printer jams every 5-10 pages",
            description=(
                "The color printer near the London trading floor (LON-PRN-TF-02) keeps jamming. We clear"
                " the jam, print a few pages, and it jams again. Always in tray 2. We've tried different"
                " paper. It's been like this for 3 days. We really need color printing for client"
                " presentations."
            ),
            category=Category.HARDWARE,
            priority=Priority.P3,
            team=Team.ENDPOINT,
            needs_escalation=False,
            missing_info=[MissingInfo.DEVICE_INFO, MissingInfo.REPRODUCTION_FREQUENCY],
            next_best_action="Inspect tray 2 rollers for wear and schedule a maintenance visit from the vendor",
            remediation_steps=[
                "Inspect tray 2 feed rollers and separation pad for wear or debris",
                "Clean the paper path and rollers with a lint-free cloth",
                "Try using tray 1 or tray 3 as a temporary workaround",
                "If rollers are worn, schedule a vendor maintenance visit for parts replacement",
                "Redirect users to an alternate color printer in the meantime",
            ],
            reporter_name="Charlotte Davies",
            reporter_email="charlotte.davies@contoso.com",
            reporter_department="Institutional Trading",
            channel=Channel.EMAIL,
            created_at="2026-03-13T14:30:00Z",
            tags=["printer", "paper-jam", "london"],
            difficulty="easy",
        ),
        # ──────────────────────────────────────────────────────────────
        # 15. Scan-to-email broken
        # ──────────────────────────────────────────────────────────────
        ScenarioDefinition(
            scenario_id="hardware_015",
            subject="Scan to email not working on MFP",
            description=(
                "The scan-to-email function on the Ricoh multifunction printer in the Singapore office"
                " mailroom (SG-MFP-01) stopped working. When I scan a document and enter my email, it"
                " shows 'Send Failed — SMTP Error' on the display. Regular printing and copying still"
                " work fine. We use this daily for contract scanning."
            ),
            category=Category.HARDWARE,
            priority=Priority.P3,
            team=Team.NETWORK_OPS,
            needs_escalation=False,
            missing_info=[MissingInfo.ERROR_MESSAGE, MissingInfo.CONFIGURATION_DETAILS],
            next_best_action="Verify the SMTP relay configuration on the printer and check for mail flow issues",
            remediation_steps=[
                "Check the printer's SMTP relay configuration for correct server and port settings",
                "Verify that the printer's IP is still authorized on the SMTP relay",
                "Test SMTP connectivity from the printer's network segment",
                "Check if any recent mail flow policy changes blocked the printer's send address",
                "Reconfigure SMTP settings if needed and test a scan-to-email",
            ],
            reporter_name="Kenneth Loh",
            reporter_email="kenneth.loh@contoso.com",
            reporter_department="Settlements",
            channel=Channel.PORTAL,
            created_at="2026-03-14T04:15:00Z",
            tags=["printer", "scanner", "email", "smtp", "singapore"],
            difficulty="medium",
        ),
        # ──────────────────────────────────────────────────────────────
        # 16. Meeting room projector dead
        # ──────────────────────────────────────────────────────────────
        ScenarioDefinition(
            scenario_id="hardware_016",
            subject="Projector in Boardroom A not turning on — board meeting in 2 hours",
            description=(
                "The Epson projector in Boardroom A (NYC, Building 1, floor 10) will not power on at all."
                " No lights, no fan, nothing when we press the power button or use the remote. We have a"
                " board of directors meeting in 2 hours and this is the only room large enough. The HDMI"
                " cables and wall plate are fine — we tested with a laptop directly. Please send someone"
                " immediately."
            ),
            category=Category.HARDWARE,
            priority=Priority.P1,
            team=Team.ENDPOINT,
            needs_escalation=True,
            missing_info=[MissingInfo.DEVICE_INFO],
            next_best_action=("Dispatch a technician immediately with a portable display or backup projector"),
            remediation_steps=[
                "Dispatch an on-site technician to Boardroom A immediately",
                "Bring a backup projector or large portable display as a contingency",
                "Check the projector power supply, outlet, and circuit breaker",
                "If the projector cannot be revived, set up the backup display",
                "After the meeting, arrange for projector repair or replacement",
            ],
            reporter_name="Victoria Lane",
            reporter_email="victoria.lane@contoso.com",
            reporter_department="Executive Operations",
            channel=Channel.PHONE,
            created_at="2026-03-17T07:00:00Z",
            tags=["projector", "meeting-room", "urgent", "board-meeting", "nyc"],
            difficulty="medium",
        ),
        # ──────────────────────────────────────────────────────────────
        # 17. Teams Room device frozen
        # ──────────────────────────────────────────────────────────────
        ScenarioDefinition(
            scenario_id="hardware_017",
            subject="Teams Room touchscreen frozen in conf room 6B",
            description=(
                "The Microsoft Teams Room device in conference room 6B (London office, floor 4) is"
                " completely frozen. The touchscreen shows the Teams interface but nothing responds to"
                " touch. We can't start or join meetings from the room. Already tried tapping the screen"
                " repeatedly. Haven't found a power button to restart it."
            ),
            category=Category.HARDWARE,
            priority=Priority.P2,
            team=Team.ENDPOINT,
            needs_escalation=False,
            missing_info=[MissingInfo.DEVICE_INFO, MissingInfo.TIMESTAMP],
            next_best_action="Power-cycle the Teams Room compute module and touch panel",
            remediation_steps=[
                "Locate the compute module (usually under the table or behind the display) and power-cycle it",
                "Power-cycle the touch panel by disconnecting its network cable for 10 seconds",
                "Wait for the Teams Room app to fully reboot and check for pending updates",
                "Apply any available firmware or Teams Room app updates",
                "If the device continues to freeze, open a support case with the hardware vendor",
            ],
            reporter_name="Aisha Patel",
            reporter_email="aisha.patel@contoso.com",
            reporter_department="Portfolio Management",
            channel=Channel.CHAT,
            created_at="2026-03-17T10:30:00Z",
            tags=["teams-room", "meeting-room", "frozen", "london"],
            difficulty="easy",
        ),
        # ──────────────────────────────────────────────────────────────
        # 18. Conference phone echo
        # ──────────────────────────────────────────────────────────────
        ScenarioDefinition(
            scenario_id="hardware_018",
            subject="Terrible echo on conference room speakerphone",
            description=(
                "Every call in meeting room 4C has a terrible echo. The people on the other end say they"
                " hear themselves repeated back with a slight delay. We've been dealing with this for a"
                " couple of weeks and just used our personal headsets as a workaround, but we had a"
                " 15-person all-hands today and it was unusable. The speakerphone is a Poly Trio C60."
                " NYC office, floor 4."
            ),
            category=Category.HARDWARE,
            priority=Priority.P3,
            team=Team.ENDPOINT,
            needs_escalation=False,
            missing_info=[MissingInfo.ENVIRONMENT_DETAILS, MissingInfo.CONFIGURATION_DETAILS],
            next_best_action="Update the Poly Trio firmware and adjust acoustic echo cancellation settings",
            remediation_steps=[
                "Update the Poly Trio C60 firmware to the latest version",
                "Verify acoustic echo cancellation is enabled in the device settings",
                "Check the room for reflective surfaces that may worsen echo",
                "Adjust microphone sensitivity and speaker volume levels",
                "If echo persists after firmware update, contact Poly support for RMA",
            ],
            reporter_name="Tom Bradley",
            reporter_email="tom.bradley@contoso.com",
            reporter_department="Corporate Strategy",
            channel=Channel.EMAIL,
            created_at="2026-03-17T16:00:00Z",
            tags=["conference-phone", "echo", "meeting-room", "audio"],
            difficulty="medium",
        ),
        # ──────────────────────────────────────────────────────────────
        # 19. Company mobile phone cracked screen
        # ──────────────────────────────────────────────────────────────
        ScenarioDefinition(
            scenario_id="hardware_019",
            subject="Company iPhone screen shattered",
            description=(
                "I dropped my company-issued iPhone 15 Pro and the screen is completely shattered."
                " Touchscreen still works but glass shards are coming off. I need this phone for"
                " two-factor authentication and Bloomberg alerts. Phone number is +1-212-555-0147."
                " Can I get a replacement? I have AppleCare I think."
            ),
            category=Category.HARDWARE,
            priority=Priority.P3,
            team=Team.ENDPOINT,
            needs_escalation=False,
            missing_info=[MissingInfo.DEVICE_INFO, MissingInfo.BUSINESS_IMPACT],
            next_best_action=("Verify AppleCare coverage and schedule a screen repair or device swap"),
            remediation_steps=[
                "Verify AppleCare coverage status for the device",
                "If covered, schedule an Apple Store repair appointment or mail-in repair",
                "Provide a loaner phone with Intune MDM enrollment for continuity",
                "Ensure MFA and Bloomberg app are configured on the loaner",
                "Once repaired, return the loaner and re-provision the original device",
            ],
            reporter_name="Raj Kapoor",
            reporter_email="raj.kapoor@contoso.com",
            reporter_department="Equity Trading",
            channel=Channel.CHAT,
            created_at="2026-03-18T08:00:00Z",
            tags=["mobile", "iphone", "screen", "applecare"],
            difficulty="easy",
        ),
        # ──────────────────────────────────────────────────────────────
        # 20. MDM enrollment failed on new phone
        # ──────────────────────────────────────────────────────────────
        ScenarioDefinition(
            scenario_id="hardware_020",
            subject="Can't enroll new phone in Intune",
            description=(
                "I received my new company Samsung Galaxy S24 yesterday. When I try to set it up and enroll"
                " in Microsoft Intune, it gets to 'Registering device...' then fails with error code"
                " 0x80180026. I've tried factory resetting and starting over twice. My old phone was an"
                " iPhone and it worked fine with Intune."
            ),
            category=Category.HARDWARE,
            priority=Priority.P3,
            team=Team.ENDPOINT,
            needs_escalation=False,
            missing_info=[MissingInfo.DEVICE_INFO, MissingInfo.ENVIRONMENT_DETAILS],
            next_best_action=("Check Intune device enrollment restrictions for Android and verify the user's license"),
            remediation_steps=[
                "Verify the user has an Intune license assigned in Entra ID",
                "Check Intune enrollment restrictions to ensure Samsung Galaxy S24 is not blocked",
                "Verify Android Enterprise enrollment profile is correctly configured",
                "Have the user attempt enrollment on a different Wi-Fi network to rule out network issues",
                "If error persists, collect Intune diagnostic logs from the device and escalate to Intune support",
            ],
            reporter_name="Natasha Volkov",
            reporter_email="natasha.volkov@contoso.com",
            reporter_department="Business Development",
            channel=Channel.PORTAL,
            created_at="2026-03-18T11:15:00Z",
            tags=["mobile", "intune", "mdm", "enrollment", "android"],
            difficulty="hard",
        ),
        # ──────────────────────────────────────────────────────────────
        # 21. Bloomberg terminal screen issue
        # ──────────────────────────────────────────────────────────────
        ScenarioDefinition(
            scenario_id="hardware_021",
            subject="Bloomberg terminal monitor showing garbled colors",
            description=(
                "One of my four Bloomberg terminal monitors is displaying garbled colors and horizontal"
                " lines across the screen. It's the top-right monitor in my quad setup. The other three"
                " screens are fine. I've reseated the DVI cable but no change. This is my primary"
                " Bloomberg workstation on the London trading floor and I cannot trade effectively with"
                " only 3 screens during market hours. Asset ID: CTF-BT-0312."
            ),
            category=Category.HARDWARE,
            priority=Priority.P2,
            team=Team.ENDPOINT,
            needs_escalation=True,
            missing_info=[MissingInfo.DEVICE_INFO],
            next_best_action=(
                "Swap the affected monitor with a spare and contact Bloomberg hardware support for replacement"
            ),
            remediation_steps=[
                "Test the affected monitor with a different cable and port on the Bloomberg terminal",
                "Swap with a spare Bloomberg-compatible monitor to restore the quad setup immediately",
                "If the original monitor is faulty, open a hardware case with Bloomberg support",
                "If the issue follows the port rather than the monitor, escalate to Bloomberg for terminal repair",
                "Ensure the replacement monitor matches the required resolution and color profile",
            ],
            reporter_name="George Hamilton",
            reporter_email="george.hamilton@contoso.com",
            reporter_department="Fixed Income",
            channel=Channel.PHONE,
            created_at="2026-03-18T07:30:00Z",
            tags=["bloomberg", "monitor", "trading", "london"],
            difficulty="hard",
        ),
        # ──────────────────────────────────────────────────────────────
        # 22. Bloomberg biometric reader not working
        # ──────────────────────────────────────────────────────────────
        ScenarioDefinition(
            scenario_id="hardware_022",
            subject="Bloomberg fingerprint reader won't recognize me",
            description=(
                "The fingerprint reader on my Bloomberg terminal stopped recognizing my fingerprint. I've"
                " cleaned my finger and the sensor. It just blinks red three times and then asks for my"
                " password. This started after the terminal was powered off over the weekend for the floor"
                " electrical work. Singapore trading floor, seat 14B."
            ),
            category=Category.HARDWARE,
            priority=Priority.P2,
            team=Team.ENDPOINT,
            needs_escalation=False,
            missing_info=[MissingInfo.DEVICE_INFO, MissingInfo.ERROR_MESSAGE],
            next_best_action=("Re-enroll the user's fingerprint on the Bloomberg biometric reader"),
            remediation_steps=[
                "Verify the biometric reader is detected by the Bloomberg terminal",
                "Attempt to re-enroll the user's fingerprint through Bloomberg settings",
                "Clean the biometric sensor with isopropyl alcohol and a lint-free cloth",
                "If re-enrollment fails, check the USB connection of the biometric reader",
                "Contact Bloomberg support if the reader hardware appears faulty",
            ],
            reporter_name="Hiroshi Tanaka",
            reporter_email="hiroshi.tanaka@contoso.com",
            reporter_department="Derivatives",
            channel=Channel.CHAT,
            created_at="2026-03-18T03:45:00Z",
            tags=["bloomberg", "biometric", "fingerprint", "singapore"],
            difficulty="medium",
        ),
        # ──────────────────────────────────────────────────────────────
        # 23. New laptop procurement request
        # ──────────────────────────────────────────────────────────────
        ScenarioDefinition(
            scenario_id="hardware_023",
            subject="Request for new laptop — starting April 7",
            description=(
                "Hi, I'm a new hire starting on April 7th in the Data Engineering team in New York."
                " My manager, Kevin Zhou, told me to reach out to IT to get my laptop ordered. I'll need"
                " something with good specs for data engineering work — lots of RAM and fast storage."
                " I don't have an employee ID yet but my HR onboarding contact is Jessica Tan."
            ),
            category=Category.HARDWARE,
            priority=Priority.P3,
            team=Team.ENDPOINT,
            needs_escalation=False,
            missing_info=[
                MissingInfo.DEVICE_INFO,
                MissingInfo.CONFIGURATION_DETAILS,
                MissingInfo.BUSINESS_IMPACT,
            ],
            next_best_action=(
                "Verify the new hire record with HR and initiate the standard laptop provisioning workflow"
            ),
            remediation_steps=[
                "Confirm the new hire record and start date with HR contact Jessica Tan",
                "Determine the standard laptop configuration for Data Engineering roles",
                "Submit a procurement request for the approved laptop model",
                "Pre-configure the device with the Data Engineering software image",
                "Schedule the laptop for delivery to the user's desk by April 7th",
            ],
            reporter_name="Alex Rivera",
            reporter_email="alex.rivera@contoso.com",
            reporter_department="Data Engineering",
            channel=Channel.EMAIL,
            created_at="2026-03-19T09:00:00Z",
            tags=["procurement", "new-hire", "laptop", "onboarding"],
            difficulty="easy",
        ),
        # ──────────────────────────────────────────────────────────────
        # 24. Monitor upgrade request
        # ──────────────────────────────────────────────────────────────
        ScenarioDefinition(
            scenario_id="hardware_024",
            subject="Request to upgrade to ultrawide monitor",
            description=(
                "I'd like to request an upgrade from my current dual 24-inch monitor setup to a single"
                " 34-inch ultrawide monitor (Dell U3423WE or similar). I'm a UX designer and the"
                " ultrawide would significantly improve my workflow with Figma. My manager, Sarah Chen,"
                " has approved this. I'm in the London office, floor 3."
            ),
            category=Category.HARDWARE,
            priority=Priority.P4,
            team=Team.ENDPOINT,
            needs_escalation=False,
            missing_info=[MissingInfo.DEVICE_INFO, MissingInfo.CONFIGURATION_DETAILS],
            next_best_action=(
                "Verify manager approval and check if the requested monitor is on the approved hardware list"
            ),
            remediation_steps=[
                "Confirm manager approval in writing",
                "Verify the requested monitor model is on the approved hardware catalog",
                "Submit a procurement request through the standard hardware ordering process",
                "Schedule delivery and desk setup with the user",
                "Reclaim the existing dual monitors for reallocation",
            ],
            reporter_name="Yuki Nakamura",
            reporter_email="yuki.nakamura@contoso.com",
            reporter_department="Frontend Engineering",
            channel=Channel.PORTAL,
            created_at="2026-03-19T11:30:00Z",
            tags=["procurement", "monitor", "upgrade", "london"],
            difficulty="easy",
        ),
        # ──────────────────────────────────────────────────────────────
        # 25. Asset return / warranty claim
        # ──────────────────────────────────────────────────────────────
        ScenarioDefinition(
            scenario_id="hardware_025",
            subject="Returning equipment — last day is March 28",
            description=(
                "My last day at Contoso is March 28th. I need to return my laptop (ThinkPad X1 Carbon,"
                " asset CTF-LT-2918), docking station, two monitors, headset, and mouse. I'm in the"
                " NYC office. Where do I bring everything? Also, I have personal files on the laptop"
                " that I need to transfer to a USB drive before I return it — is that allowed?"
            ),
            category=Category.HARDWARE,
            priority=Priority.P4,
            team=Team.ENDPOINT,
            needs_escalation=False,
            missing_info=[MissingInfo.CONTACT_INFO],
            next_best_action=(
                "Initiate the standard offboarding equipment return process and clarify the data transfer policy"
            ),
            remediation_steps=[
                "Confirm the offboarding date with HR and validate the asset list",
                "Advise the user on the personal data transfer policy per security guidelines",
                "Schedule an equipment return appointment at the IT depot",
                "Process returned equipment: wipe the laptop, inspect all items, update the asset register",
                "Issue a return receipt to the user and HR",
            ],
            reporter_name="Brian Kowalski",
            reporter_email="brian.kowalski@contoso.com",
            reporter_department="Consulting",
            channel=Channel.EMAIL,
            created_at="2026-03-19T14:00:00Z",
            tags=["offboarding", "asset-return", "nyc"],
            difficulty="easy",
        ),
        # ──────────────────────────────────────────────────────────────
        # 26. USB external drive not recognized
        # ──────────────────────────────────────────────────────────────
        ScenarioDefinition(
            scenario_id="hardware_026",
            subject="USB drive not showing up",
            description=(
                "I plugged in my encrypted USB external hard drive (Samsung T7 Shield) and Windows doesn't"
                " see it. No notification, nothing in File Explorer, doesn't show in Disk Management. It"
                " works on my personal computer at home. I need files from this drive for an audit."
            ),
            category=Category.HARDWARE,
            priority=Priority.P3,
            team=Team.ENDPOINT,
            needs_escalation=False,
            missing_info=[
                MissingInfo.DEVICE_INFO,
                MissingInfo.ENVIRONMENT_DETAILS,
                MissingInfo.NETWORK_LOCATION,
            ],
            next_best_action=("Check if Intune device compliance policies are blocking external USB storage devices"),
            remediation_steps=[
                "Check Intune device compliance policies for USB storage restrictions",
                "Verify the USB drive is not blocked by endpoint DLP or device control policies",
                "If the drive is blocked by policy, work with the user's manager to request a policy exception",
                "If an exception is granted, apply a temporary device control policy allowing the specific drive",
                "Recommend transferring files via an approved method such as SharePoint or OneDrive",
            ],
            reporter_name="Catherine Moore",
            reporter_email="catherine.moore@contoso.com",
            reporter_department="Internal Audit",
            channel=Channel.CHAT,
            created_at="2026-03-20T09:30:00Z",
            tags=["usb", "external-drive", "policy", "blocked"],
            difficulty="hard",
        ),
        # ──────────────────────────────────────────────────────────────
        # 27. Security key not recognized
        # ──────────────────────────────────────────────────────────────
        ScenarioDefinition(
            scenario_id="hardware_027",
            subject="YubiKey stopped working after Windows update",
            description=(
                "My YubiKey 5 NFC isn't being recognized by my laptop after yesterday's Windows update."
                " The LED on the key doesn't light up when I plug it in. I use this for MFA to access"
                " our trading systems and Azure portal. I'm completely locked out of critical systems"
                " right now. I've tried all three USB ports on my laptop."
            ),
            category=Category.HARDWARE,
            priority=Priority.P2,
            team=Team.ENDPOINT,
            needs_escalation=False,
            missing_info=[MissingInfo.DEVICE_INFO, MissingInfo.ERROR_MESSAGE],
            next_best_action=("Check Device Manager for USB driver issues and test the YubiKey on another machine"),
            remediation_steps=[
                "Check Device Manager for unrecognized USB devices or driver errors",
                "Test the YubiKey on a different computer to rule out key hardware failure",
                "Roll back the USB driver if it was updated recently",
                "If the YubiKey works on another machine, troubleshoot the laptop's USB drivers",
                "If the YubiKey is dead, issue a replacement and re-register it in Entra ID",
                "Provide a temporary alternative MFA method while the issue is resolved",
            ],
            reporter_name="Ivan Petrov",
            reporter_email="ivan.petrov@contoso.com",
            reporter_department="Cloud Infrastructure",
            channel=Channel.PHONE,
            created_at="2026-03-20T08:15:00Z",
            tags=["yubikey", "security-key", "mfa", "usb"],
            difficulty="medium",
        ),
        # ──────────────────────────────────────────────────────────────
        # 28. Desktop PC won't power on
        # ──────────────────────────────────────────────────────────────
        ScenarioDefinition(
            scenario_id="hardware_028",
            subject="Desktop computer completely dead",
            description=(
                "My desktop workstation (Dell OptiPlex 7010) won't turn on. No lights, no fan spin,"
                " nothing happens when I press the power button. I've verified the power strip is on"
                " and other devices plugged into the same strip work fine. I tried a different power"
                " cable too. This machine has been in use for about 3 years. NYC, floor 2, desk 214."
                " Asset tag CTF-DT-1088."
            ),
            category=Category.HARDWARE,
            priority=Priority.P3,
            team=Team.ENDPOINT,
            needs_escalation=False,
            missing_info=[],
            next_best_action="Test with a known-good power supply unit to determine if the PSU or motherboard failed",
            remediation_steps=[
                "Test the wall outlet with another device to confirm power availability",
                "Open the case and check the PSU connection to the motherboard",
                "Test with a replacement PSU to isolate the failure",
                "If PSU replacement doesn't work, the motherboard may have failed — plan a full replacement",
                "Provide a loaner workstation and migrate the user's data from the old drive",
            ],
            reporter_name="Frank O'Brien",
            reporter_email="frank.obrien@contoso.com",
            reporter_department="Middle Office",
            channel=Channel.PORTAL,
            created_at="2026-03-20T13:00:00Z",
            tags=["desktop", "power", "hardware-failure", "nyc"],
            difficulty="medium",
        ),
        # ──────────────────────────────────────────────────────────────
        # 29. Desktop fans loud / random shutdowns
        # ──────────────────────────────────────────────────────────────
        ScenarioDefinition(
            scenario_id="hardware_029",
            subject="PC shutting down randomly with loud fan noise",
            description=(
                "my desktop keeps randomly shutting down. no warning, no blue screen, just off. happens"
                " maybe 2-3 times a day. before it shuts down the fans get REALLY loud. like jet engine"
                " loud. started about a week ago. its getting worse. i cant trust saving anything because"
                " it might just die mid-save. dell optiplex, not sure which model. singapore office."
            ),
            category=Category.HARDWARE,
            priority=Priority.P2,
            team=Team.ENDPOINT,
            needs_escalation=False,
            missing_info=[
                MissingInfo.DEVICE_INFO,
                MissingInfo.ERROR_MESSAGE,
                MissingInfo.TIMESTAMP,
            ],
            next_best_action="Run hardware thermal diagnostics — likely CPU overheating causing thermal shutdown",
            remediation_steps=[
                "Run Dell built-in diagnostics (ePSA) to check thermal sensors and fans",
                "Open the case and clean dust from the CPU heatsink, fans, and vents",
                "Check that the CPU heatsink is properly seated and thermal paste is intact",
                "Monitor CPU temperatures after cleaning to verify normal operating range",
                "If shutdowns continue, replace the CPU cooler assembly or the entire unit",
            ],
            reporter_name="Andy Ng",
            reporter_email="andy.ng@contoso.com",
            reporter_department="Backend Engineering",
            channel=Channel.CHAT,
            created_at="2026-03-21T06:30:00Z",
            tags=["desktop", "overheating", "shutdown", "fans", "singapore"],
            difficulty="medium",
        ),
        # ──────────────────────────────────────────────────────────────
        # 30. Network switch in server room
        # ──────────────────────────────────────────────────────────────
        ScenarioDefinition(
            scenario_id="hardware_030",
            subject="Switch in NYC MDF flashing amber on multiple ports",
            description=(
                "During routine inspection of the NYC MDF (Main Distribution Frame) in Building 1"
                " basement, I noticed switch NYC-SW-CORE-02 has amber/error LEDs on ports 22-28."
                " These ports serve the 6th floor west wing. I haven't received any user complaints"
                " yet but wanted to flag this proactively. The switch is a Cisco Catalyst 9300."
                " Uptime shows 247 days. Log capture attached."
            ),
            category=Category.HARDWARE,
            priority=Priority.P2,
            team=Team.NETWORK_OPS,
            needs_escalation=False,
            missing_info=[MissingInfo.ERROR_MESSAGE],
            next_best_action="Review the switch logs for port error details and check for CRC or link flap issues",
            remediation_steps=[
                "Pull interface error counters and logs for ports 22 through 28",
                "Check for CRC errors, input errors, or link flap events on the affected ports",
                "Inspect the physical cabling and patch panel for the affected port range",
                "If errors indicate a failing GBIC/SFP or line card, schedule replacement during maintenance window",
                "Monitor the ports for 24 hours after remediation to confirm stability",
            ],
            reporter_name="Derek Washington",
            reporter_email="derek.washington@contoso.com",
            reporter_department="DevOps",
            channel=Channel.EMAIL,
            attachments=["nyc-sw-core-02-log-capture.txt"],
            created_at="2026-03-21T16:45:00Z",
            tags=["network-switch", "infrastructure", "proactive", "nyc"],
            difficulty="hard",
        ),
        # ──────────────────────────────────────────────────────────────
        # 31. Wireless AP flashing red
        # ──────────────────────────────────────────────────────────────
        ScenarioDefinition(
            scenario_id="hardware_031",
            subject="WiFi access point on floor 3 blinking red",
            description=(
                "The wireless access point mounted on the ceiling near the elevators on floor 3 of the"
                " London office is blinking red. Several people around that area are complaining about"
                " slow or no WiFi. I can see the AP label says LON-AP-F3-02. It used to have a solid"
                " green light. Not sure when it changed."
            ),
            category=Category.HARDWARE,
            priority=Priority.P2,
            team=Team.NETWORK_OPS,
            needs_escalation=False,
            missing_info=[MissingInfo.AFFECTED_USERS, MissingInfo.TIMESTAMP],
            next_best_action="Check the wireless controller for AP LON-AP-F3-02 status and attempt a remote reboot",
            remediation_steps=[
                "Check the wireless LAN controller for the status of AP LON-AP-F3-02",
                "Attempt a remote reboot of the access point from the controller",
                "If the AP does not rejoin, check the switch port and PoE power delivery",
                "If PoE is fine, schedule a physical inspection and potential AP replacement",
                "Verify neighboring APs are handling the load while the AP is down",
            ],
            reporter_name="Fiona Campbell",
            reporter_email="fiona.campbell@contoso.com",
            reporter_department="Regulatory Affairs",
            channel=Channel.CHAT,
            created_at="2026-03-21T12:00:00Z",
            tags=["wifi", "access-point", "network", "london"],
            difficulty="medium",
        ),
        # ──────────────────────────────────────────────────────────────
        # 32. CEO's laptop dead before board meeting — executive VIP
        # ──────────────────────────────────────────────────────────────
        ScenarioDefinition(
            scenario_id="hardware_032",
            subject="CEO laptop not working — BOARD MEETING IN 45 MINS",
            description=(
                "This is Maria from the CEO's office. Mr. Henderson's laptop is showing a blue screen"
                " and won't get past it. He has the quarterly board presentation in 45 minutes and the"
                " deck is on his laptop. He is extremely frustrated. He's in his office on the 10th"
                " floor, NYC Building 1. Please send your best person up here RIGHT NOW. This cannot wait."
            ),
            category=Category.HARDWARE,
            priority=Priority.P1,
            team=Team.ENDPOINT,
            needs_escalation=True,
            missing_info=[MissingInfo.DEVICE_INFO, MissingInfo.ERROR_MESSAGE],
            next_best_action=(
                "Dispatch a senior technician immediately with a pre-configured loaner laptop and recover"
                " the presentation from OneDrive or recent backups"
            ),
            remediation_steps=[
                "Dispatch a senior technician to the CEO's office immediately with a loaner laptop",
                "Recover the board presentation from OneDrive, SharePoint, or local backup",
                "Configure the loaner laptop with the CEO's profile and necessary applications",
                "Attempt to repair the original laptop after the board meeting",
                "If unrepairable, provision a permanent replacement and migrate all data",
                "Conduct a post-incident review to prevent recurrence for executive devices",
            ],
            reporter_name="Maria Gonzalez",
            reporter_email="maria.gonzalez@contoso.com",
            reporter_department="Executive Operations",
            channel=Channel.PHONE,
            created_at="2026-03-24T08:15:00Z",
            tags=["vip", "ceo", "urgent", "bsod", "board-meeting", "nyc"],
            difficulty="extreme",
        ),
        # ──────────────────────────────────────────────────────────────
        # 33. Entire floor docking stations died — batch failure
        # ──────────────────────────────────────────────────────────────
        ScenarioDefinition(
            scenario_id="hardware_033",
            subject="URGENT: All docking stations on floor 7 stopped working simultaneously",
            description=(
                "At approximately 9:05 AM, every docking station on floor 7 of the NYC Building 2 office"
                " stopped working at the same time. Roughly 60 users are affected. Displays went black,"
                " peripherals disconnected, and charging stopped. The laptops themselves are fine when"
                " undocked. We had a brief power flicker around 9:03 AM. All docks are Lenovo ThinkPad"
                " USB-C Dock Gen 2 (40AS). This is the entire Institutional Trading floor and people"
                " cannot work."
            ),
            category=Category.HARDWARE,
            priority=Priority.P1,
            team=Team.ENDPOINT,
            needs_escalation=True,
            missing_info=[],
            next_best_action=(
                "Investigate the power flicker as root cause, reset all docking stations,"
                " and coordinate with Facilities on the electrical issue"
            ),
            remediation_steps=[
                "Coordinate with Facilities to investigate the power flicker and UPS status on floor 7",
                "Have users perform a full dock reset: disconnect all cables including power for 30 seconds",
                "If mass reset does not work, dispatch technicians with replacement power adapters for the docks",
                "Check if the docks require firmware recovery after the power event",
                "Verify all 60 workstations are fully functional before closing the incident",
                "Request Facilities install surge protectors or validate UPS coverage for the floor",
            ],
            reporter_name="Patricia Wyatt",
            reporter_email="patricia.wyatt@contoso.com",
            reporter_department="Institutional Trading",
            channel=Channel.PHONE,
            created_at="2026-03-24T09:10:00Z",
            tags=["dock", "mass-failure", "power", "multi-user", "urgent", "nyc"],
            difficulty="extreme",
        ),
        # ──────────────────────────────────────────────────────────────
        # 34. Laptop damaged in transit — travel scenario
        # ──────────────────────────────────────────────────────────────
        ScenarioDefinition(
            scenario_id="hardware_034",
            subject="Laptop damaged during business travel",
            description=(
                "I'm currently in Singapore for client meetings (I'm usually based in NYC). My laptop"
                " was in my checked luggage — I know, I shouldn't have — and the hinge is bent and the"
                " screen doesn't close properly anymore. The laptop still works but the display wobbles"
                " and I'm worried it'll snap off. I have meetings all week. Is there a way to get a"
                " loaner in the Singapore office? ThinkPad X1 Carbon, asset CTF-LT-4102."
            ),
            category=Category.HARDWARE,
            priority=Priority.P2,
            team=Team.ENDPOINT,
            needs_escalation=False,
            missing_info=[MissingInfo.BUSINESS_IMPACT],
            next_best_action=(
                "Arrange a loaner laptop from the Singapore office inventory and ship the damaged unit back for repair"
            ),
            remediation_steps=[
                "Check Singapore office loaner inventory for an available device",
                "Configure the loaner with the user's profile via Intune and OneDrive sync",
                "Issue the loaner to the user at the Singapore office",
                "Arrange for the damaged laptop to be shipped back to NYC for warranty repair",
                "Remind the user of the travel policy regarding carrying laptops in hand luggage",
            ],
            reporter_name="Steven Grant",
            reporter_email="steven.grant@contoso.com",
            reporter_department="Client Services",
            channel=Channel.EMAIL,
            created_at="2026-03-25T02:30:00Z",
            tags=["travel", "physical-damage", "loaner", "singapore"],
            difficulty="medium",
        ),
        # ──────────────────────────────────────────────────────────────
        # 35. Standing desk request — procurement
        # ──────────────────────────────────────────────────────────────
        ScenarioDefinition(
            scenario_id="hardware_035",
            subject="Request for standing desk — ergonomic assessment completed",
            description=(
                "I recently completed an ergonomic assessment with the company's ergonomics consultant"
                " and they recommended I switch to a sit-stand desk due to lower back issues. The"
                " assessment report (ref ERG-2026-0341) was submitted to HR last week. My manager,"
                " Jennifer Wu, has approved the purchase. I'm in the London office, floor 5, desk 512."
                " Could you let me know the timeline for getting this set up?"
            ),
            category=Category.HARDWARE,
            priority=Priority.P4,
            team=Team.ENDPOINT,
            needs_escalation=False,
            missing_info=[MissingInfo.CONFIGURATION_DETAILS],
            next_best_action=(
                "Verify the ergonomic assessment approval and initiate the standing desk procurement process"
            ),
            remediation_steps=[
                "Verify the ergonomic assessment report and manager approval with HR",
                "Select the appropriate sit-stand desk model from the approved vendor catalog",
                "Submit a procurement request and confirm estimated delivery timeline",
                "Coordinate with Facilities for desk installation and cable management",
                "Follow up with the user after installation to confirm the setup meets their needs",
            ],
            reporter_name="Hannah Wright",
            reporter_email="hannah.wright@contoso.com",
            reporter_department="Research",
            channel=Channel.PORTAL,
            created_at="2026-03-25T10:00:00Z",
            tags=["procurement", "ergonomic", "standing-desk", "london"],
            difficulty="easy",
        ),
    ]
