"""Generate synthetic Task 1 (Signal Triage) benchmark dataset v2.

Targets known generalization weaknesses:
  - "Not a Mission Signal" (40+ signals)
  - "Mission Briefing Request" (40+ signals)
  - Priority calibration P1-P4 boundary cases (80+ signals)
  - Category confusion / misleading keywords (50+ signals)
  - Escalation edge cases (20+ signals)

Uses Azure OpenAI (gpt-5-4) with DefaultAzureCredential.
Generates in batches of 50 to avoid timeouts.

Usage:
    cd /home/fbujaroski/be-an-fde-for-a-day/py
    source .venv/bin/activate
    set -a; source ../.env; set +a
    python apps/sample/synthetic/generate_triage_v2.py
"""

import asyncio
import json
import os
import random
import sys
from collections import Counter
from pathlib import Path
from typing import Any

from dotenv import load_dotenv
from openai import AsyncAzureOpenAI

# ── Paths ────────────────────────────────────────────────────────────
ROOT = Path(__file__).resolve().parents[3]  # be-an-fde-for-a-day/py
ENV_PATH = ROOT.parent / ".env"
ROUTING_GUIDE = ROOT.parent / "docs" / "challenge" / "task1" / "routing_guide.md"
OUT_DIR = Path(__file__).resolve().parent
OUT_SIGNALS = OUT_DIR / "triage_v2.json"
OUT_GOLD = OUT_DIR / "triage_v2_gold.json"

load_dotenv(ENV_PATH)

# ── Constants ────────────────────────────────────────────────────────

CATEGORIES = [
    "Communications & Navigation",
    "Crew Access & Biometrics",
    "Hull & Structural Systems",
    "Flight Software & Instruments",
    "Threat Detection & Containment",
    "Telemetry & Data Banks",
    "Mission Briefing Request",
    "Not a Mission Signal",
]

CATEGORY_TEAM_PRIMARY: dict[str, str] = {
    "Communications & Navigation": "Deep Space Communications",
    "Crew Access & Biometrics": "Crew Identity & Airlock Control",
    "Hull & Structural Systems": "Spacecraft Systems Engineering",
    "Flight Software & Instruments": "Mission Software Operations",
    "Threat Detection & Containment": "Threat Response Command",
    "Telemetry & Data Banks": "Telemetry & Data Core",
    "Mission Briefing Request": "None",
    "Not a Mission Signal": "None",
}

# Mission Briefing can route to multiple teams depending on context
BRIEFING_TEAM_MAP: dict[str, str] = {
    "onboarding_setup": "Spacecraft Systems Engineering",
    "offboarding_disable": "Crew Identity & Airlock Control",
    "software_howto": "Mission Software Operations",
    "room_booking": "None",
    "equipment_provision": "Spacecraft Systems Engineering",
    "status_inquiry": "None",
    "general_admin": "None",
}

CHANNELS = ["subspace_relay", "holodeck_comm", "bridge_terminal", "emergency_beacon"]

DEPARTMENTS = [
    "Propulsion Engineering", "Diplomatic Corps", "Command Bridge",
    "Stellar Cartography", "Space Law Division", "Exobiology Lab",
    "Astro-Science Division", "Power Core Engineering", "Flight Deck Operations",
    "Structural Integrity", "Sensor Operations", "Medical Bay",
    "Crew Quarters Admin", "Navigation Control", "Environmental Systems",
    "Security Division", "Data Sciences", "Supply & Logistics",
    "Communications Hub", "Weapons Systems",
]

FIRST_NAMES = [
    "Sarah", "Marcus", "Diana", "Jordan", "Priya", "Thomas", "Yuki",
    "Alejandro", "Fatima", "Dmitri", "Zara", "Chen", "Kwame", "Ingrid",
    "Raj", "Sofia", "Nikolai", "Amara", "Liam", "Mei", "Omar", "Elena",
    "Kofi", "Astrid", "Hassan", "Suki", "Diego", "Anya", "Tariq", "Freya",
    "Ravi", "Nadia", "Kaito", "Isabella", "Viktor", "Luna", "Jamal",
    "Hana", "Felix", "Olga", "Aisha", "Pavel", "Carmen", "Idris",
    "Yuna", "Sven", "Leila", "Matthias", "Rosa", "Kenji",
]

LAST_NAMES = [
    "Chen", "Rodriguez", "Marsh", "Lee", "Sharma", "Wright", "Tanaka",
    "Reyes", "Al-Hassan", "Petrov", "Okafor", "Nakamura", "Asante",
    "Lindqvist", "Patel", "Moreau", "Volkov", "Diallo", "O'Brien",
    "Zhang", "Al-Rashid", "Kowalski", "Mensah", "Johansson", "Khan",
    "Yamamoto", "Rivera", "Sokolova", "Ahmed", "Bergström", "Kapoor",
    "Santos", "Hayashi", "Müller", "Osei", "Park", "Fernandez",
    "Ivanova", "Bell", "Nguyen", "Torres", "Kim", "Björk", "Nwosu",
    "Gupta", "Larsson", "Costa", "Weber", "Choi", "Bakker",
]

MISSING_INFO_FIELDS = [
    "affected_subsystem", "anomaly_readout", "sequence_to_reproduce",
    "affected_crew", "habitat_conditions", "stardate", "previous_signal_id",
    "crew_contact", "module_specs", "software_version", "sector_coordinates",
    "mission_impact", "recurrence_pattern", "sensor_log_or_capture",
    "biometric_method", "system_configuration",
]

CATEGORY_MISSING_INFO_AFFINITY: dict[str, list[str]] = {
    "Communications & Navigation": [
        "affected_subsystem", "anomaly_readout", "sector_coordinates",
        "module_specs", "mission_impact", "recurrence_pattern",
        "sensor_log_or_capture", "system_configuration",
    ],
    "Crew Access & Biometrics": [
        "affected_subsystem", "biometric_method", "module_specs",
        "software_version", "sequence_to_reproduce", "anomaly_readout",
        "affected_crew", "previous_signal_id",
    ],
    "Hull & Structural Systems": [
        "module_specs", "anomaly_readout", "affected_crew",
        "habitat_conditions", "sector_coordinates", "recurrence_pattern",
        "sensor_log_or_capture",
    ],
    "Flight Software & Instruments": [
        "software_version", "module_specs", "sequence_to_reproduce",
        "anomaly_readout", "affected_subsystem", "sensor_log_or_capture",
        "system_configuration",
    ],
    "Threat Detection & Containment": [
        "stardate", "system_configuration", "habitat_conditions",
        "affected_subsystem", "sensor_log_or_capture", "affected_crew",
        "sector_coordinates",
    ],
    "Telemetry & Data Banks": [
        "affected_subsystem", "module_specs", "system_configuration",
        "anomaly_readout", "recurrence_pattern", "mission_impact",
    ],
    "Mission Briefing Request": [
        "crew_contact", "affected_crew", "stardate", "module_specs",
        "mission_impact",
    ],
    "Not a Mission Signal": [],
}


# ── Spec definitions for each weakness area ──────────────────────────

def _make_not_a_mission_signal_specs(rng: random.Random, start_id: int) -> list[dict[str, Any]]:
    """Generate 45 'Not a Mission Signal' specs covering all subtypes."""
    subtypes = [
        # Thank-you / gratitude (7)
        ("thank_you", "Thanks for fixing the relay issue yesterday, works great now"),
        ("thank_you", "Just wanted to say the BioAuth panel is working perfectly after your fix"),
        ("thank_you", "Quick note to say thanks — the nav console update resolved everything"),
        ("thank_you", "Much appreciated on the hull sensor recalibration, you all are the best"),
        ("thank_you", "Hey team, the comm array fix from last cycle is holding steady — thank you!"),
        ("thank_you", "Wanted to send a note of appreciation for the quick turnaround on my access request"),
        ("thank_you", "Great work on the telemetry pipeline — running smooth as silk now"),
        # Out-of-office / cryo notices (5)
        ("ooo_cryo", "I'll be in cryo-stasis from stardate 47634 until 47650, redirect signals to Lt. Chen"),
        ("ooo_cryo", "Going off-shift for deep sleep rotation, Sgt. Patel covering my duties"),
        ("ooo_cryo", "Out of office: medical leave from 0800 today through end of month"),
        ("ooo_cryo", "Automated reply: I am currently in cryo-hibernation cycle 7 and cannot respond"),
        ("ooo_cryo", "Shore leave approved — I'll be at Starbase Gamma until the 28th, no comms needed"),
        # Resolved / self-closed (6)
        ("resolved", "Got it working — turns out I needed to recalibrate the phase discriminator"),
        ("resolved", "False alarm — my badge just needed a battery swap, all good now"),
        ("resolved", "Can disregard my earlier report, the console rebooted and everything's fine"),
        ("resolved", "Closing this out — found the answer in the wiki under 'phase 3 procedures'"),
        ("resolved", "Never mind, the intermittent comms dropout was actually scheduled maintenance"),
        ("resolved", "Resolved: I was using the wrong frequency band. My mistake, sorry for the noise"),
        # Auto-replies and forwards (5)
        ("auto_reply", "This is an automated message confirming receipt of your signal SIG-2001"),
        ("auto_reply", "Auto-forward: Original message from Medical Bay re: annual physical schedule"),
        ("auto_reply", "Delivery notification: Your previous message to Engineering was delivered successfully"),
        ("auto_reply", "This mailbox is not monitored. For urgent matters, contact Bridge Ops directly"),
        ("auto_reply", "Automated acknowledgement — your request #4477 has been logged in the queue"),
        # Informational broadcasts (5)
        ("broadcast", "Reminder: emergency drill at 0800 tomorrow, all decks. This is NOT a real emergency"),
        ("broadcast", "Station-wide notice: protein cube supply restocked in all mess halls"),
        ("broadcast", "FYI: The rec lounge holoprojector maintenance is scheduled for 1400-1600 today"),
        ("broadcast", "Comm note: stardate corrections posted — check updated calendar in crew portal"),
        ("broadcast", "Notice to all crew: annual safety certification due by end of cycle 12"),
        # Spam / phishing (5)
        ("spam", "CONGRATULATIONS! You have won the Galactic Lottery! Claim 10 million credits NOW"),
        ("spam", "Urgent: Your station account has been compromised, click here to verify identity"),
        ("spam", "Buy genuine Romulan ale at 50% off — limited time offer for CDSS crew only"),
        ("spam", "Forward: chain message — send to 10 crew members for good luck on your next mission"),
        ("spam", "You have been selected for a free upgrade to Premium Quarters — act fast"),
        # Questions / wrong channel (6)
        ("wrong_channel", "What's the cafeteria schedule for gamma shift this week?"),
        ("wrong_channel", "Does anyone know where the station cat went? Haven't seen Nebula since Tuesday"),
        ("wrong_channel", "Can someone remind me of the dress code for the ambassador reception?"),
        ("wrong_channel", "Hey is the gym open during night cycle? Asking for the whole security team"),
        ("wrong_channel", "Looking for recommendations for a good holodeck program, any suggestions?"),
        ("wrong_channel", "Social: Anyone up for zero-g basketball after shift? Meet at Cargo Bay 3"),
        # Social messages (6)
        ("social", "Happy birthday Lt. Chen! The whole deck is celebrating in Mess Hall B at 1900"),
        ("social", "Crew movie night this Friday — voting on the selection in the rec room terminal"),
        ("social", "Lost and found: someone left a personal datapad in the observation lounge"),
        ("social", "Petition to name the new lab module after Dr. Mehta — sign on the crew portal"),
        ("social", "Congrats to Ensign Park on their promotion! Well deserved"),
        ("social", "Just FYI the vending machine on Deck 7 is still dispensing the wrong flavor of nutrient paste, but it's kind of growing on me honestly"),
    ]

    specs = []
    for i, (subtype, hint) in enumerate(subtypes):
        specs.append({
            "weakness": "not_a_mission_signal",
            "subtype": subtype,
            "hint": hint,
            "category": "Not a Mission Signal",
            "priority": "P4",
            "assigned_team": "None",
            "needs_escalation": False,
            "missing_information": [],
            "difficulty": "adversarial" if subtype in ("spam", "auto_reply") else "standard",
        })

    return specs[:45]


def _make_mission_briefing_specs(rng: random.Random, start_id: int) -> list[dict[str, Any]]:
    """Generate 45 'Mission Briefing Request' specs covering all subtypes."""
    subtypes = [
        # Onboarding (8)
        ("onboarding_setup", "New science officer arriving next week, needs full station access"),
        ("onboarding_setup", "Three new engineering interns starting — need workstation setup and access badges"),
        ("onboarding_setup", "Incoming crew transfer: Commander Vasquez needs bridge-level clearance"),
        ("onboarding_setup", "New medical staff joining — need lab access, quarters assignment, system accounts"),
        ("onboarding_setup", "Civilian researcher Dr. Kim needs temporary access to Stellar Cartography lab"),
        ("onboarding_setup", "Please provision accounts for 5 new data science recruits arriving stardate 47700"),
        ("onboarding_setup", "Diplomatic attaché needs guest quarters and limited network access for 30 days"),
        ("onboarding_setup", "New pilot transferring from Starbase 12 — needs flight sim access and deck clearance"),
        # Offboarding (7)
        ("offboarding_disable", "Lt. Chen departing station next cycle — please disable all access and accounts"),
        ("offboarding_disable", "Crew member Petrov transferring out — need to revoke biometric access to Labs 3-7"),
        ("offboarding_disable", "Ensign O'Brien's tour ends Friday — standard departure procedures needed"),
        ("offboarding_disable", "Dr. Sharma retiring — full offboarding: access, files, equipment return"),
        ("offboarding_disable", "Removing contractor access for visiting engineering team — their project ended"),
        ("offboarding_disable", "Crew departure: 3 officers rotating to Starbase Gamma, need exit processing"),
        ("offboarding_disable", "Please deactivate Sgt. Rivera's biometric profile — honorable discharge effective today"),
        # Room/facility booking (7)
        ("room_booking", "Need Briefing Room Alpha for 0900 delegation meeting tomorrow"),
        ("room_booking", "Can I book the main conference room for a 2-hour mission planning session?"),
        ("room_booking", "Reserve Holodeck 3 for crew training exercises next Tuesday 0800-1200"),
        ("room_booking", "Need the secure briefing room for classified intelligence review Friday"),
        ("room_booking", "Can we get Lab 5 reserved for a week-long experiment starting next cycle?"),
        ("room_booking", "Request to block the observation lounge for an awards ceremony"),
        ("room_booking", "Need to book the small huddle room near Engineering for daily standups"),
        # Equipment provisioning (6)
        ("equipment_provision", "Need 3 workstations set up for the new engineering team by Friday"),
        ("equipment_provision", "Requesting a portable scanner kit for the away team mission"),
        ("equipment_provision", "Our lab needs a new holoprojector for the presentation next week"),
        ("equipment_provision", "Can we get 10 replacement datapads for the training cohort?"),
        ("equipment_provision", "Need a secure terminal installed in the new intelligence office"),
        ("equipment_provision", "Request for 2 additional monitoring consoles in Telemetry Bay C"),
        # How-to questions (8)
        ("software_howto", "How do I request a security badge replacement?"),
        ("software_howto", "What's the process for changing my biometric enrollment?"),
        ("software_howto", "How do I set up remote access to the mission planning tools?"),
        ("software_howto", "Where do I find the form for requesting a shift schedule change?"),
        ("software_howto", "How do I get access to the classified document archive?"),
        ("software_howto", "What's the procedure for reporting a lost communicator?"),
        ("software_howto", "How do I update my emergency contact information in the system?"),
        ("software_howto", "Can someone walk me through the new inventory requisition portal?"),
        # Status inquiries (9)
        ("status_inquiry", "What's the ETA on my access request from last week?"),
        ("status_inquiry", "Checking in on the workstation order I submitted 3 days ago"),
        ("status_inquiry", "Any update on the conference room booking I put in for Thursday?"),
        ("status_inquiry", "Status check: my transfer paperwork was submitted 5 cycles ago"),
        ("status_inquiry", "Following up on my request for additional lab equipment"),
        ("status_inquiry", "When will the new crew badges be ready? Was told 48 hours, it's been a week"),
        ("status_inquiry", "Can I get an update on the security clearance application for my team?"),
        ("status_inquiry", "Checking if my requisition for medical supplies has been processed"),
        ("status_inquiry", "Has the IT team started on the network extension to the new wing?"),
    ]

    specs = []
    for subtype, hint in subtypes:
        team = BRIEFING_TEAM_MAP.get(subtype, "None")
        # Status inquiries and how-to are P4, most others are P3 or P2
        if subtype in ("status_inquiry", "software_howto", "room_booking"):
            priority = "P4"
        elif subtype == "offboarding_disable":
            priority = rng.choice(["P2", "P3"])
        elif subtype == "onboarding_setup":
            priority = rng.choice(["P3", "P3", "P2"])
        else:
            priority = rng.choice(["P3", "P4"])

        needs_escalation = False
        missing_info = _pick_missing_info("Mission Briefing Request", priority, False, rng)

        specs.append({
            "weakness": "mission_briefing",
            "subtype": subtype,
            "hint": hint,
            "category": "Mission Briefing Request",
            "priority": priority,
            "assigned_team": team,
            "needs_escalation": needs_escalation,
            "missing_information": missing_info,
            "difficulty": "standard",
        })

    return specs[:45]


def _make_priority_calibration_specs(rng: random.Random) -> list[dict[str, Any]]:
    """Generate 80 signals specifically targeting priority boundaries."""
    specs = []

    # ── P1: 20 clear critical signals ────────────────────────────────
    p1_scenarios = [
        ("Hull & Structural Systems", "Spacecraft Systems Engineering",
         "Hull breach detected on deck 12 but automatic sealing engaged"),
        ("Hull & Structural Systems", "Spacecraft Systems Engineering",
         "Atmospheric pressure dropping slowly in section 4 — might be a seal issue"),
        ("Hull & Structural Systems", "Spacecraft Systems Engineering",
         "Decompression warning on cargo bay B, crew evacuating"),
        ("Hull & Structural Systems", "Spacecraft Systems Engineering",
         "Hull integrity sensor showing micro-fracture pattern near airlock 9"),
        ("Threat Detection & Containment", "Threat Response Command",
         "Active hostile vessel detected on long-range sensors, approach vector confirmed"),
        ("Threat Detection & Containment", "Threat Response Command",
         "Containment field failure in bio-lab 3, specimens may have escaped"),
        ("Threat Detection & Containment", "Threat Response Command",
         "Confirmed security breach — unauthorized individual in restricted section"),
        ("Hull & Structural Systems", "Spacecraft Systems Engineering",
         "Life-support system primary and backup both showing fault codes"),
        ("Hull & Structural Systems", "Spacecraft Systems Engineering",
         "Oxygen recycler offline in habitation ring — switching to reserves"),
        ("Hull & Structural Systems", "Spacecraft Systems Engineering",
         "Temperature anomaly in cryo-bay, containment may be compromised"),
        ("Communications & Navigation", "Deep Space Communications",
         "Navigation system total failure — cannot determine current position or trajectory"),
        ("Threat Detection & Containment", "Threat Response Command",
         "Containment breach in hazmat storage — toxic atmosphere spreading to adjacent sections"),
        ("Hull & Structural Systems", "Spacecraft Systems Engineering",
         "Emergency: hull panel separation detected on dorsal section during EVA operations"),
        ("Hull & Structural Systems", "Spacecraft Systems Engineering",
         "Pressure differential alarm on observation deck — possible viewport seal failure"),
        ("Threat Detection & Containment", "Threat Response Command",
         "Unknown biological agent detected in ventilation system of deck 5"),
        ("Hull & Structural Systems", "Spacecraft Systems Engineering",
         "Radiation shielding failure on port side — crew exposure levels rising"),
        ("Flight Software & Instruments", "Mission Software Operations",
         "Autopilot locked in incorrect trajectory — manual override not responding"),
        ("Hull & Structural Systems", "Spacecraft Systems Engineering",
         "Life-support CO2 scrubber cascade failure — all three units down"),
        ("Threat Detection & Containment", "Threat Response Command",
         "Multiple unauthorized access attempts to weapons control systems detected"),
        ("Hull & Structural Systems", "Spacecraft Systems Engineering",
         "Thermal regulation failure — core temperature rising beyond safe parameters"),
    ]

    for cat, team, hint in p1_scenarios:
        specs.append({
            "weakness": "priority_calibration",
            "subtype": "clear_p1",
            "hint": hint,
            "category": cat,
            "priority": "P1",
            "assigned_team": team,
            "needs_escalation": True,
            "missing_information": _pick_missing_info(cat, "P1", False, rng),
            "difficulty": rng.choice(["standard", "adversarial"]),
        })

    # ── P2: 20 clear high-priority signals ───────────────────────────
    p2_scenarios = [
        ("Communications & Navigation", "Deep Space Communications",
         "Subspace relay completely down — entire wing cannot send or receive messages"),
        ("Communications & Navigation", "Deep Space Communications",
         "Station-wide DNS beacon failure — all systems resolving incorrectly"),
        ("Telemetry & Data Banks", "Telemetry & Data Core",
         "Telemetry pipeline failure — no data flowing from any sensor array to mission control"),
        ("Flight Software & Instruments", "Mission Software Operations",
         "FlightOS crashed on all navigation consoles — manual backup only"),
        ("Crew Access & Biometrics", "Crew Identity & Airlock Control",
         "SSO system completely down — no crew can authenticate to any station system"),
        ("Threat Detection & Containment", "Threat Response Command",
         "Suspicious data exfiltration pattern detected on internal network — investigating"),
        ("Communications & Navigation", "Deep Space Communications",
         "Bandwidth saturation on primary comm array — emergency channels affected"),
        ("Telemetry & Data Banks", "Telemetry & Data Core",
         "Backup database server failed — we're running on primary only with no redundancy"),
        ("Flight Software & Instruments", "Mission Software Operations",
         "Mission planning software returning corrupted trajectory calculations"),
        ("Crew Access & Biometrics", "Crew Identity & Airlock Control",
         "Biometric system rejecting 30+ crew members after directory update — mass lockout"),
        ("Hull & Structural Systems", "Spacecraft Systems Engineering",
         "Multiple fabricators across 3 decks simultaneously malfunctioning — no spare parts production"),
        ("Communications & Navigation", "Deep Space Communications",
         "Long-range communications completely offline — cannot reach sector command"),
        ("Flight Software & Instruments", "Mission Software Operations",
         "Instrument calibration software serving wrong correction factors — all science data suspect"),
        ("Telemetry & Data Banks", "Telemetry & Data Core",
         "Data archive corruption detected — 3 days of mission logs may be compromised"),
        ("Threat Detection & Containment", "Threat Response Command",
         "Unusual network traffic pattern from an unknown device on the internal network"),
        ("Crew Access & Biometrics", "Crew Identity & Airlock Control",
         "Badge provisioning system down — 12 new crew arriving tomorrow cannot get access"),
        ("Hull & Structural Systems", "Spacecraft Systems Engineering",
         "Power grid fluctuations on 3 decks — non-essential systems brown-outs"),
        ("Communications & Navigation", "Deep Space Communications",
         "Signal routing tables corrupted — automated relay forwarding sending messages to wrong stations"),
        ("Flight Software & Instruments", "Mission Software Operations",
         "Licensing server unreachable — 40+ instrument consoles locked out of analysis tools"),
        ("Telemetry & Data Banks", "Telemetry & Data Core",
         "Storage array at 99% capacity — new telemetry data being dropped"),
    ]

    for cat, team, hint in p2_scenarios:
        needs_esc = cat == "Threat Detection & Containment" or rng.random() < 0.15
        specs.append({
            "weakness": "priority_calibration",
            "subtype": "clear_p2",
            "hint": hint,
            "category": cat,
            "priority": "P2",
            "assigned_team": team,
            "needs_escalation": needs_esc,
            "missing_information": _pick_missing_info(cat, "P2", False, rng),
            "difficulty": rng.choice(["standard", "adversarial"]),
        })

    # ── P3: 20 clear standard-priority signals ───────────────────────
    p3_scenarios = [
        ("Communications & Navigation", "Deep Space Communications",
         "Subspace relay has intermittent dropouts every few hours — workaround is to resend"),
        ("Crew Access & Biometrics", "Crew Identity & Airlock Control",
         "Badge scan taking 5 seconds instead of usual 1 — functional but slow"),
        ("Flight Software & Instruments", "Mission Software Operations",
         "Nav console display flickers occasionally when running star charts"),
        ("Telemetry & Data Banks", "Telemetry & Data Core",
         "Old archive search taking much longer than usual — still returning results"),
        ("Hull & Structural Systems", "Spacecraft Systems Engineering",
         "Deck 4 lighting panel buzzing — annoying but illumination is fine"),
        ("Crew Access & Biometrics", "Crew Identity & Airlock Control",
         "My second biometric method (retina) stopped working, but palm still works fine"),
        ("Communications & Navigation", "Deep Space Communications",
         "Local mesh latency spiking to 200ms during peak hours — usually 14ms"),
        ("Flight Software & Instruments", "Mission Software Operations",
         "Star chart application crashes when loading sectors beyond Gamma quadrant"),
        ("Telemetry & Data Banks", "Telemetry & Data Core",
         "Telemetry dashboard showing stale data — 30-minute lag instead of real-time"),
        ("Hull & Structural Systems", "Spacecraft Systems Engineering",
         "Environmental monitor in Lab 2 giving spurious temperature readings intermittently"),
        ("Crew Access & Biometrics", "Crew Identity & Airlock Control",
         "Access policy change I submitted last week hasn't propagated to deck 7 panels"),
        ("Communications & Navigation", "Deep Space Communications",
         "One relay node dropping packets — rerouting through backup path works"),
        ("Flight Software & Instruments", "Mission Software Operations",
         "Mission log export function timing out for reports over 500 entries"),
        ("Telemetry & Data Banks", "Telemetry & Data Core",
         "Backup job for sensor logs completing but taking 3x longer than usual"),
        ("Threat Detection & Containment", "Threat Response Command",
         "Reporting a phishing email I received — clearly spam, not clicking anything"),
        ("Hull & Structural Systems", "Spacecraft Systems Engineering",
         "Minor vibration detected near engine mount 3 — within tolerance but noting it"),
        ("Crew Access & Biometrics", "Crew Identity & Airlock Control",
         "SSO session expires after 30 minutes instead of the configured 8 hours"),
        ("Communications & Navigation", "Deep Space Communications",
         "Comm badge audio quality degraded — static on every third transmission"),
        ("Flight Software & Instruments", "Mission Software Operations",
         "Instrument calibration wizard showing deprecated UI — still functional but confusing"),
        ("Telemetry & Data Banks", "Telemetry & Data Core",
         "Data query returning duplicate rows for some sensor IDs — cosmetic but messy"),
    ]

    for cat, team, hint in p3_scenarios:
        specs.append({
            "weakness": "priority_calibration",
            "subtype": "clear_p3",
            "hint": hint,
            "category": cat,
            "priority": "P3",
            "assigned_team": team,
            "needs_escalation": False,
            "missing_information": _pick_missing_info(cat, "P3", False, rng),
            "difficulty": "standard",
        })

    # ── P4: 20 clear low-priority signals ────────────────────────────
    p4_scenarios = [
        ("Flight Software & Instruments", "Mission Software Operations",
         "How do I export my mission logs to a personal datapad?"),
        ("Crew Access & Biometrics", "Crew Identity & Airlock Control",
         "Is there a way to add a secondary email to my crew profile?"),
        ("Communications & Navigation", "Deep Space Communications",
         "Just curious — what protocol does the subspace relay use for handshakes?"),
        ("Telemetry & Data Banks", "Telemetry & Data Core",
         "The font size on the telemetry dashboard is too small for my liking"),
        ("Hull & Structural Systems", "Spacecraft Systems Engineering",
         "The light in my quarters closet flickers when I open the door — very minor"),
        ("Flight Software & Instruments", "Mission Software Operations",
         "Can someone update the splash screen on the nav console? It still shows last year's logo"),
        ("Crew Access & Biometrics", "Crew Identity & Airlock Control",
         "My profile photo in the crew directory is outdated — how do I change it?"),
        ("Communications & Navigation", "Deep Space Communications",
         "Feature request: add a dark mode to the comm monitoring interface"),
        ("Telemetry & Data Banks", "Telemetry & Data Core",
         "Is there documentation for the new telemetry API format?"),
        ("Hull & Structural Systems", "Spacecraft Systems Engineering",
         "The label on junction box 14B is peeling off — cosmetic only"),
        ("Flight Software & Instruments", "Mission Software Operations",
         "Suggestion: the mission planner should have an undo button"),
        ("Crew Access & Biometrics", "Crew Identity & Airlock Control",
         "Question: can I use my badge for both gym and lab access or do I need separate ones?"),
        ("Communications & Navigation", "Deep Space Communications",
         "Minor typo in the comm system status page — says 'recieved' instead of 'received'"),
        ("Telemetry & Data Banks", "Telemetry & Data Core",
         "Would be nice if the data export included CSV format option"),
        ("Hull & Structural Systems", "Spacecraft Systems Engineering",
         "The cargo bay door makes a slight squeak when closing — not urgent"),
        ("Flight Software & Instruments", "Mission Software Operations",
         "The keyboard shortcut guide for FlightOS seems incomplete"),
        ("Crew Access & Biometrics", "Crew Identity & Airlock Control",
         "Idle question: how often do biometric templates get refreshed?"),
        ("Communications & Navigation", "Deep Space Communications",
         "Can we get a notification sound option for incoming subspace messages?"),
        ("Telemetry & Data Banks", "Telemetry & Data Core",
         "Could the dashboard show timestamps in local station time instead of UTC?"),
        ("Hull & Structural Systems", "Spacecraft Systems Engineering",
         "The paint is chipping on the corridor wall near Section 5 — just cosmetic"),
    ]

    for cat, team, hint in p4_scenarios:
        specs.append({
            "weakness": "priority_calibration",
            "subtype": "clear_p4",
            "hint": hint,
            "category": cat,
            "priority": "P4",
            "assigned_team": team,
            "needs_escalation": False,
            "missing_information": _pick_missing_info(cat, "P4", False, rng),
            "difficulty": "standard",
        })

    return specs


def _make_category_confusion_specs(rng: random.Random) -> list[dict[str, Any]]:
    """Generate 55 signals where keywords are misleading."""
    specs = []

    confusing_scenarios = [
        # "Relay" in telemetry context (NOT comms)
        ("Telemetry & Data Banks", "Telemetry & Data Core", "P3",
         "relay_not_comms", "Data relay module dropping telemetry packets between sensor arrays and database"),
        ("Telemetry & Data Banks", "Telemetry & Data Core", "P3",
         "relay_not_comms", "Internal relay process for telemetry data aggregation is lagging behind"),
        ("Telemetry & Data Banks", "Telemetry & Data Core", "P2",
         "relay_not_comms", "Relay buffer overflow in data pipeline — sensor data not reaching archive"),
        ("Telemetry & Data Banks", "Telemetry & Data Core", "P3",
         "relay_not_comms", "Relay scheduler skipping some data batches in the telemetry ingest queue"),
        ("Telemetry & Data Banks", "Telemetry & Data Core", "P4",
         "relay_not_comms", "Question about how the data relay service routes sensor logs to long-term storage"),

        # "Access" in data context (NOT crew access)
        ("Telemetry & Data Banks", "Telemetry & Data Core", "P3",
         "access_not_biometric", "Cannot access archived mission logs from last quarter — search returns empty"),
        ("Telemetry & Data Banks", "Telemetry & Data Core", "P2",
         "access_not_biometric", "Access to real-time telemetry feed denied — data permissions issue"),
        ("Telemetry & Data Banks", "Telemetry & Data Core", "P3",
         "access_not_biometric", "Database access timeout when querying historical sensor readings"),
        ("Telemetry & Data Banks", "Telemetry & Data Core", "P4",
         "access_not_biometric", "How do I get read access to the deep-space survey data archive?"),
        ("Telemetry & Data Banks", "Telemetry & Data Core", "P3",
         "access_not_biometric", "API access token for telemetry service expired — can't pull dashboard data"),

        # "Console" in software context (NOT hardware)
        ("Flight Software & Instruments", "Mission Software Operations", "P3",
         "console_not_hardware", "Navigation console application freezing when loading waypoint editor"),
        ("Flight Software & Instruments", "Mission Software Operations", "P3",
         "console_not_hardware", "Console error messages appearing in FlightOS debug log during route calculation"),
        ("Flight Software & Instruments", "Mission Software Operations", "P2",
         "console_not_hardware", "Console application on all bridge stations showing wrong sensor overlay"),
        ("Flight Software & Instruments", "Mission Software Operations", "P4",
         "console_not_hardware", "Console output formatting broken on the mission planning software"),
        ("Flight Software & Instruments", "Mission Software Operations", "P3",
         "console_not_hardware", "The admin console for instrument management shows blank calibration history"),

        # "Security" in cert context vs threat context
        ("Threat Detection & Containment", "Threat Response Command", "P2",
         "security_cert", "Security certificate for internal API gateway expiring in 48 hours"),
        ("Threat Detection & Containment", "Threat Response Command", "P3",
         "security_cert", "Security audit log showing certificate validation warnings on 3 endpoints"),
        ("Threat Detection & Containment", "Threat Response Command", "P2",
         "security_threat", "Security camera footage shows unrecognized individual near server room"),
        ("Threat Detection & Containment", "Threat Response Command", "P3",
         "security_threat", "Security scan found suspicious file on shared network drive — likely false positive"),
        ("Threat Detection & Containment", "Threat Response Command", "P3",
         "security_cert", "SSL/TLS certificate mismatch error on the crew portal — users seeing warnings"),

        # Multi-system issues — PRIMARY determines category
        ("Communications & Navigation", "Deep Space Communications", "P2",
         "multi_system_comms", "Comms array primary issue with secondary effect on nav display"),
        ("Hull & Structural Systems", "Spacecraft Systems Engineering", "P2",
         "multi_system_hull", "Hull sensor malfunction causing incorrect readings on telemetry dashboard"),
        ("Crew Access & Biometrics", "Crew Identity & Airlock Control", "P3",
         "multi_system_access", "Badge system glitch also causing incorrect log entries in audit trail"),
        ("Flight Software & Instruments", "Mission Software Operations", "P3",
         "multi_system_software", "FlightOS bug in sensor integration module — hardware sensors are fine"),
        ("Telemetry & Data Banks", "Telemetry & Data Core", "P2",
         "multi_system_data", "Data pipeline failure blocking both telemetry and comms log archival"),

        # Software running on hardware (software issue, not hardware)
        ("Flight Software & Instruments", "Mission Software Operations", "P3",
         "software_on_hardware", "The software on the bridge console keeps crashing — hardware seems fine"),
        ("Flight Software & Instruments", "Mission Software Operations", "P3",
         "software_on_hardware", "App running on deck display panel showing wrong data — panel hardware works"),
        ("Flight Software & Instruments", "Mission Software Operations", "P2",
         "software_on_hardware", "Mission control software on the main screen throwing unhandled exceptions"),
        ("Flight Software & Instruments", "Mission Software Operations", "P4",
         "software_on_hardware", "The instrument panel application has a rendering bug on the side monitor"),
        ("Flight Software & Instruments", "Mission Software Operations", "P3",
         "software_on_hardware", "Sensor analysis software on the lab terminal gives wrong calculations"),

        # "Network" / "connection" could be comms or software or data
        ("Communications & Navigation", "Deep Space Communications", "P3",
         "network_comms", "Network connectivity to outpost Alpha-7 has been intermittent since yesterday"),
        ("Communications & Navigation", "Deep Space Communications", "P2",
         "network_comms", "Local network mesh on deck 9 completely unresponsive — affects 20 crew"),
        ("Flight Software & Instruments", "Mission Software Operations", "P3",
         "network_software", "Software update server unreachable from the console — connection refused error"),
        ("Telemetry & Data Banks", "Telemetry & Data Core", "P3",
         "network_data", "Database connection pool exhausted — queries backing up"),
        ("Communications & Navigation", "Deep Space Communications", "P3",
         "network_comms", "DNS beacon resolution failing for station services — some consoles affected"),

        # "Panel" could be access, hull, software
        ("Crew Access & Biometrics", "Crew Identity & Airlock Control", "P3",
         "panel_access", "BioAuth panel outside Lab 4 not accepting any biometric input"),
        ("Hull & Structural Systems", "Spacecraft Systems Engineering", "P3",
         "panel_hull", "Hull integrity monitoring panel near Airlock 2 showing hardware fault"),
        ("Flight Software & Instruments", "Mission Software Operations", "P3",
         "panel_software", "Control panel software for environmental displays stuck in boot loop"),
        ("Crew Access & Biometrics", "Crew Identity & Airlock Control", "P3",
         "panel_access", "Door panel showing 'access denied' for all crew on deck 3 — policy issue"),
        ("Hull & Structural Systems", "Spacecraft Systems Engineering", "P2",
         "panel_hull", "Structural monitoring panel displaying error codes — unable to read hull data"),

        # "Scan" could be biometrics or sensors
        ("Crew Access & Biometrics", "Crew Identity & Airlock Control", "P3",
         "scan_biometric", "Fingerprint scan keeps failing on the cargo bay entrance"),
        ("Telemetry & Data Banks", "Telemetry & Data Core", "P3",
         "scan_data", "Deep-space scan results not syncing to the archive database"),
        ("Hull & Structural Systems", "Spacecraft Systems Engineering", "P3",
         "scan_hull", "Hull scan sensor suite returning inconsistent readings near engine mount"),
        ("Crew Access & Biometrics", "Crew Identity & Airlock Control", "P4",
         "scan_biometric", "My iris scan enrollment seems to have expired — how do I re-enroll?"),
        ("Telemetry & Data Banks", "Telemetry & Data Core", "P4",
         "scan_data", "Can someone explain how to run a sector scan and export results to CSV?"),

        # "System" is maximally ambiguous
        ("Flight Software & Instruments", "Mission Software Operations", "P2",
         "system_software", "System update failed midway — mission planning suite won't launch"),
        ("Hull & Structural Systems", "Spacecraft Systems Engineering", "P3",
         "system_hull", "Environmental control system hardware unit making unusual noise on deck 6"),
        ("Communications & Navigation", "Deep Space Communications", "P2",
         "system_comms", "Communication system backbone router reporting critical errors"),
        ("Crew Access & Biometrics", "Crew Identity & Airlock Control", "P2",
         "system_access", "Identity management system sync failed — crew directory is 12 hours stale"),
        ("Telemetry & Data Banks", "Telemetry & Data Core", "P3",
         "system_data", "Data archival system running out of storage — approaching warning threshold"),
    ]

    for cat, team, priority, subtype, hint in confusing_scenarios:
        needs_esc = (priority == "P1") or (cat == "Threat Detection & Containment" and priority in ("P1", "P2"))
        specs.append({
            "weakness": "category_confusion",
            "subtype": subtype,
            "hint": hint,
            "category": cat,
            "priority": priority,
            "assigned_team": team,
            "needs_escalation": needs_esc,
            "missing_information": _pick_missing_info(cat, priority, True, rng),
            "difficulty": "adversarial",
        })

    return specs


def _make_escalation_edge_specs(rng: random.Random) -> list[dict[str, Any]]:
    """Generate 25 signals testing escalation boundaries."""
    specs = []

    escalation_scenarios = [
        # P2 threats SHOULD escalate
        ("Threat Detection & Containment", "Threat Response Command", "P2", True,
         "esc_p2_threat", "Unauthorized data access detected — someone pulled classified files"),
        ("Threat Detection & Containment", "Threat Response Command", "P2", True,
         "esc_p2_threat", "Suspicious login from unregistered device on the command network"),
        ("Threat Detection & Containment", "Threat Response Command", "P2", True,
         "esc_p2_threat", "Malware signature detected in routine scan of shared drive"),
        ("Threat Detection & Containment", "Threat Response Command", "P2", True,
         "esc_p2_threat", "Data exfiltration attempt blocked by firewall — source traced to internal terminal"),
        ("Threat Detection & Containment", "Threat Response Command", "P2", True,
         "esc_p2_threat", "Certificate for weapons control API compromised — rotating now"),

        # P3 threats should NOT escalate (routine reports)
        ("Threat Detection & Containment", "Threat Response Command", "P3", False,
         "esc_p3_no_threat", "Reporting spam email received — clearly a lottery scam, not clicking"),
        ("Threat Detection & Containment", "Threat Response Command", "P3", False,
         "esc_p3_no_threat", "Got a phishing message pretending to be from Command — forwarding for records"),
        ("Threat Detection & Containment", "Threat Response Command", "P3", False,
         "esc_p3_no_threat", "Minor false positive on security scan — flagged a known safe file"),
        ("Threat Detection & Containment", "Threat Response Command", "P3", False,
         "esc_p3_no_threat", "Security audit found an outdated service account — no evidence of misuse"),
        ("Threat Detection & Containment", "Threat Response Command", "P3", False,
         "esc_p3_no_threat", "SSL certificate warning on internal page — cert just needs renewal"),

        # Recurring issues SHOULD escalate
        ("Communications & Navigation", "Deep Space Communications", "P3", True,
         "esc_recurring", "This is the FOURTH time the relay has dropped in 2 weeks — pattern is clear"),
        ("Crew Access & Biometrics", "Crew Identity & Airlock Control", "P3", True,
         "esc_recurring", "Badge scan failure happening every other day now — reported 3 times before"),
        ("Flight Software & Instruments", "Mission Software Operations", "P3", True,
         "esc_recurring", "Same FlightOS crash happening weekly — previous tickets SIG-100, SIG-150, SIG-200"),
        ("Telemetry & Data Banks", "Telemetry & Data Core", "P2", True,
         "esc_recurring", "Data pipeline keeps breaking in the same spot — 5th occurrence this month"),
        ("Hull & Structural Systems", "Spacecraft Systems Engineering", "P3", True,
         "esc_recurring", "Deck 4 power fluctuation happening again — same issue as last 3 reports"),

        # Command-level reporters SHOULD escalate
        ("Communications & Navigation", "Deep Space Communications", "P3", True,
         "esc_command", "Station Commander reporting: comm delay to sector command is unacceptable"),
        ("Flight Software & Instruments", "Mission Software Operations", "P3", True,
         "esc_command", "Admiral's aide: the mission briefing software crashed during a flag-level meeting"),
        ("Crew Access & Biometrics", "Crew Identity & Airlock Control", "P3", True,
         "esc_command", "First Officer reporting: my bridge access was revoked without explanation"),
        ("Hull & Structural Systems", "Spacecraft Systems Engineering", "P2", True,
         "esc_command", "Captain's log: structural vibration in the command section requires immediate attention"),
        ("Telemetry & Data Banks", "Telemetry & Data Core", "P3", True,
         "esc_command", "Mission Director needs urgent access to classified telemetry — clearance issue"),

        # First-time routine issues should NOT escalate
        ("Communications & Navigation", "Deep Space Communications", "P3", False,
         "esc_first_time", "First time seeing this — relay 7 showed brief signal loss, came back on its own"),
        ("Crew Access & Biometrics", "Crew Identity & Airlock Control", "P3", False,
         "esc_first_time", "My badge didn't scan on the first try at Lab 4 — worked on second attempt"),
        ("Flight Software & Instruments", "Mission Software Operations", "P3", False,
         "esc_first_time", "FlightOS showed an error once when loading charts — hasn't happened again"),
        ("Telemetry & Data Banks", "Telemetry & Data Core", "P4", False,
         "esc_first_time", "Noticed a small data gap in yesterday's sensor log — probably a one-off"),
        ("Hull & Structural Systems", "Spacecraft Systems Engineering", "P4", False,
         "esc_first_time", "Minor creak heard near junction 14B — first time, probably thermal expansion"),
    ]

    for cat, team, priority, needs_esc, subtype, hint in escalation_scenarios:
        specs.append({
            "weakness": "escalation_edge",
            "subtype": subtype,
            "hint": hint,
            "category": cat,
            "priority": priority,
            "assigned_team": team,
            "needs_escalation": needs_esc,
            "missing_information": _pick_missing_info(cat, priority, False, rng),
            "difficulty": "adversarial",
        })

    return specs


def _make_filler_standard_specs(rng: random.Random, count: int) -> list[dict[str, Any]]:
    """Generate standard-difficulty filler signals to reach target count."""
    categories_weighted = [
        ("Communications & Navigation", 0.25),
        ("Crew Access & Biometrics", 0.20),
        ("Hull & Structural Systems", 0.10),
        ("Flight Software & Instruments", 0.15),
        ("Threat Detection & Containment", 0.10),
        ("Telemetry & Data Banks", 0.10),
        ("Mission Briefing Request", 0.05),
        ("Not a Mission Signal", 0.05),
    ]
    cats = [c for c, _ in categories_weighted]
    weights = [w for _, w in categories_weighted]

    filler_hints = {
        "Communications & Navigation": [
            "Subspace relay latency higher than normal on frequency band 4",
            "Local comm mesh showing packet loss on deck 8",
            "Signal routing table inconsistency between relay nodes",
            "Comm badge interference near engineering section",
            "DNS beacon update not propagating to outer ring",
        ],
        "Crew Access & Biometrics": [
            "Badge reader on deck 5 sometimes requires double-tap",
            "Directory sync shows my old department still",
            "SSO login prompt appearing more frequently than before",
            "Guest access badge not working for conference room",
            "Biometric enrollment screen hanging on step 3",
        ],
        "Hull & Structural Systems": [
            "Minor vibration in corridor near storage bay",
            "Environmental sensor on deck 3 reads 2 degrees high",
            "Fabricator in workshop B not recognizing material cartridges",
            "Deck plate sensor near observation lounge showing drift",
            "Power coupling for auxiliary lights flickering",
        ],
        "Flight Software & Instruments": [
            "Star chart overlay not aligning with current position data",
            "Instrument readout lag on secondary science console",
            "Mission planner tool crashes when adding 20+ waypoints",
            "Nav software showing deprecated coordinate format",
            "Calibration wizard for spectral analyzer incomplete",
        ],
        "Threat Detection & Containment": [
            "Security scan completed with one low-severity finding",
            "Containment protocol documentation seems outdated",
            "Access log anomaly for an old service account",
            "Perimeter sensor sensitivity threshold seems too low",
            "Security certificate renewal reminder for lab gateway",
        ],
        "Telemetry & Data Banks": [
            "Sensor data from array 3 arriving with 5-minute delay",
            "Archive query returning results from wrong date range",
            "Telemetry dashboard widget not refreshing automatically",
            "Storage utilization report showing discrepancy",
            "Backup job for deck 7 sensors skipping some entries",
        ],
        "Mission Briefing Request": [
            "Need access credentials for visiting inspector",
            "How do I set up a shared workspace for cross-team project?",
            "Room booking request for weekly departmental sync",
        ],
        "Not a Mission Signal": [
            "Thanks — the fix you applied yesterday is working great",
            "Out of office: on leave until next cycle",
            "Resolved my own issue — it was a config mismatch",
        ],
    }

    specs = []
    for _ in range(count):
        cat = rng.choices(cats, weights)[0]
        team = CATEGORY_TEAM_PRIMARY[cat]
        if cat == "Mission Briefing Request":
            team = rng.choice(["None", "Spacecraft Systems Engineering", "Crew Identity & Airlock Control",
                               "Mission Software Operations"])
        hints = filler_hints.get(cat, ["Standard issue"])
        hint = rng.choice(hints)

        if cat == "Not a Mission Signal":
            priority = "P4"
        elif cat == "Mission Briefing Request":
            priority = rng.choice(["P3", "P4", "P4"])
        else:
            priority = rng.choices(["P1", "P2", "P3", "P4"], [0.05, 0.20, 0.45, 0.30])[0]

        if priority == "P1":
            needs_esc = True
        elif cat == "Threat Detection & Containment" and priority == "P2":
            needs_esc = True
        else:
            needs_esc = False

        specs.append({
            "weakness": "filler",
            "subtype": "standard",
            "hint": hint,
            "category": cat,
            "priority": priority,
            "assigned_team": team,
            "needs_escalation": needs_esc,
            "missing_information": _pick_missing_info(cat, priority, False, rng),
            "difficulty": "standard",
        })

    return specs


def _pick_missing_info(category: str, priority: str, is_adversarial: bool, rng: random.Random) -> list[str]:
    if category == "Not a Mission Signal":
        return []
    if category == "Mission Briefing Request":
        affinity = CATEGORY_MISSING_INFO_AFFINITY.get(category, [])
        n = rng.choice([0, 0, 1, 1, 2])
        if n == 0 or not affinity:
            return []
        return sorted(rng.sample(affinity, min(n, len(affinity))))

    affinity = CATEGORY_MISSING_INFO_AFFINITY.get(category, MISSING_INFO_FIELDS[:6])
    if priority == "P1" and rng.random() < 0.4:
        return []
    n = rng.choice([0, 1, 1, 2, 2, 3])
    if n == 0:
        return []
    n = min(n, len(affinity))
    return sorted(rng.sample(affinity, n))


# ── Assemble all specs ───────────────────────────────────────────────

def generate_all_specs(target: int = 500, seed: int = 99) -> list[dict[str, Any]]:
    """Build the full spec list targeting weaknesses."""
    rng = random.Random(seed)

    specs: list[dict[str, Any]] = []
    specs.extend(_make_not_a_mission_signal_specs(rng, 6000))    # 45
    specs.extend(_make_mission_briefing_specs(rng, 6100))        # 45
    specs.extend(_make_priority_calibration_specs(rng))          # 80
    specs.extend(_make_category_confusion_specs(rng))            # 55
    specs.extend(_make_escalation_edge_specs(rng))               # 25

    weakness_count = len(specs)
    filler_needed = target - weakness_count
    if filler_needed > 0:
        specs.extend(_make_filler_standard_specs(rng, filler_needed))

    # Shuffle but keep deterministic
    rng.shuffle(specs)

    # Assign ticket IDs, reporters, channels, timestamps
    used_names: set[str] = set()
    for i, spec in enumerate(specs):
        spec["ticket_id"] = f"SYN-{6000 + i}"

        # Reporter
        while True:
            first = rng.choice(FIRST_NAMES)
            last = rng.choice(LAST_NAMES)
            full = f"{first} {last}"
            if full not in used_names:
                used_names.add(full)
                break
        clean_last = last.lower().replace("'", "").replace("ö", "o").replace("ü", "u")
        spec["reporter_name"] = full
        spec["reporter_email"] = f"{first.lower()}.{clean_last}@cdss.space"

        # Department — command reporters get Command Bridge
        if spec.get("subtype") == "esc_command":
            spec["reporter_department"] = "Command Bridge"
        else:
            spec["reporter_department"] = rng.choice(DEPARTMENTS)

        # Channel
        if spec["priority"] == "P1":
            spec["channel"] = rng.choice(["emergency_beacon", "bridge_terminal"])
        elif spec["category"] == "Not a Mission Signal":
            spec["channel"] = rng.choice(CHANNELS)
        else:
            spec["channel"] = rng.choice(CHANNELS)

        # Timestamp
        day = rng.randint(1, 28)
        hour = rng.randint(0, 23)
        minute = rng.randint(0, 59)
        spec["created_at"] = f"2026-04-{day:02d}T{hour:02d}:{minute:02d}:00Z"

    return specs[:target]


# ── LLM prompt builder ──────────────────────────────────────────────

def build_generation_prompt(spec: dict[str, Any], routing_guide: str) -> str:
    """Build the prompt to generate a single realistic signal."""
    priority_context = {
        "P1": "CRITICAL — hull breach, life-support failure, containment failure, hostile contact, decompression",
        "P2": "HIGH — major system failure, no workaround, multiple crew affected, but not immediate safety threat",
        "P3": "STANDARD — operational issue with workaround or limited scope, single user/system",
        "P4": "LOW — routine question, minor annoyance, cosmetic issue, informational",
    }

    # Category-specific generation guidance
    cat_guidance = {
        "Not a Mission Signal": (
            "This is NOT a support ticket for a real issue. Generate one of these:\n"
            "- A thank-you reply for a previous fix\n"
            "- An out-of-office or cryo-stasis notice\n"
            "- A self-resolved closure ('Got it working, never mind')\n"
            "- An auto-reply or forwarded message\n"
            "- An informational broadcast (drill reminders, schedule notices)\n"
            "- Spam, phishing, or lottery scam\n"
            "- A social message or question not related to IT support\n"
            "- A wrong-channel message (cafeteria schedule, gym hours, etc.)\n"
            "The signal should clearly NOT be an incident or support request."
        ),
        "Mission Briefing Request": (
            "This is an administrative/logistics request, NOT a technical incident:\n"
            "- Crew onboarding (new crew needs access, accounts, equipment)\n"
            "- Crew offboarding (departing crew needs access disabled)\n"
            "- Room/facility booking\n"
            "- Equipment provisioning\n"
            "- How-to questions about procedures\n"
            "- Status inquiries about pending requests\n"
            "It should read as a routine admin request, not a system failure."
        ),
    }

    weakness_guidance = {
        "priority_calibration": (
            "IMPORTANT: The signal must clearly read as the assigned priority level.\n"
            "- P1: Include safety/hull/life-support/containment/hostile keywords naturally\n"
            "- P2: Major failure affecting multiple crew, but no immediate safety threat\n"
            "- P3: Issue exists but there's a workaround or limited impact\n"
            "- P4: Question, cosmetic issue, or minor annoyance\n"
            "Do NOT make the priority ambiguous."
        ),
        "category_confusion": (
            "ADVERSARIAL: Use keywords that typically suggest a DIFFERENT category,\n"
            "but the actual issue clearly belongs to the target category.\n"
            f"Keywords to naturally include: based on subtype '{spec.get('subtype', '')}'\n"
            "The subject can be misleading but the description must clearly point to the correct category."
        ),
        "escalation_edge": (
            "Generate a signal that tests escalation boundaries.\n"
            f"Escalation expected: {spec['needs_escalation']}\n"
            "If escalation=True, include hints: recurring issue, command-level reporter, "
            "hostile/containment/malware risk, unauthorized access, or data exfiltration.\n"
            "If escalation=False, make it a first-time, routine, non-threatening report."
        ),
    }

    category_note = cat_guidance.get(spec["category"], "")
    weakness_note = weakness_guidance.get(spec.get("weakness", ""), "")

    missing_info_note = ""
    if spec["missing_information"]:
        fields = ", ".join(spec["missing_information"])
        missing_info_note = f"\nMISSING INFO: The signal should naturally lack: {fields}. Do NOT include these details."
    else:
        missing_info_note = "\nCOMPLETENESS: Include all relevant information for triage."

    escalation_hint = ""
    if spec["needs_escalation"] and spec["priority"] != "P1":
        if spec.get("subtype", "").startswith("esc_recurring"):
            escalation_hint = "\nHint in the text that this is a RECURRING issue (reference previous tickets or 'this keeps happening')."
        elif spec.get("subtype", "").startswith("esc_command"):
            escalation_hint = "\nThe reporter is a high-ranking officer (commander, captain, admiral's aide, etc.)."
        elif spec["category"] == "Threat Detection & Containment":
            escalation_hint = "\nInclude clear indicators of hostile activity, unauthorized access, or malware."

    return f"""You are generating a realistic space station IT support signal for the Contoso Deep Space Station (CDSS).

TARGET TRIAGE LABELS (do NOT include these in the signal text):
- Category: {spec["category"]}
- Priority: {spec["priority"]} ({priority_context[spec["priority"]]})
- Team: {spec["assigned_team"]}
- Needs Escalation: {spec["needs_escalation"]}

SCENARIO HINT: {spec.get("hint", "Generate a realistic signal for this category")}

{category_note}
{weakness_note}
{missing_info_note}
{escalation_hint}

RULES:
1. Write ONLY subject and description. Nothing else.
2. Description: 2-6 sentences, first person, as a real crew member.
3. Include specific technical details relevant to the category.
4. Match tone to priority (P1=urgent, P4=casual).
5. Include occasional personality (station cats, protein cubes, Mehta's margin notes).
6. Do NOT include category, priority, team names, or triage labels in the text.
7. Do NOT make it obvious this is a test case.
8. Make it feel like a real support ticket.
9. For "Not a Mission Signal" — do NOT describe any technical issue needing support.
10. For "Mission Briefing Request" — describe an admin/logistics request, not a technical failure.

Respond with ONLY valid JSON:
{{"subject": "...", "description": "..."}}"""


# ── LLM generation ──────────────────────────────────────────────────

async def generate_signal_text(
    client: AsyncAzureOpenAI,
    spec: dict[str, Any],
    routing_guide: str,
    semaphore: asyncio.Semaphore,
) -> dict[str, Any] | None:
    """Generate signal text for a single spec via Azure OpenAI."""
    prompt = build_generation_prompt(spec, routing_guide)

    async with semaphore:
        for attempt in range(3):
            try:
                resp = await client.chat.completions.create(
                    model="gpt-5-4",
                    messages=[
                        {
                            "role": "system",
                            "content": "You generate realistic space station support signals. Respond with valid JSON only. No markdown fences.",
                        },
                        {"role": "user", "content": prompt},
                    ],
                    temperature=0.9,
                    max_completion_tokens=600,
                )
                content = resp.choices[0].message.content.strip()
                if content.startswith("```"):
                    content = content.split("\n", 1)[1] if "\n" in content else content[3:]
                    if content.endswith("```"):
                        content = content[:-3]
                    content = content.strip()

                parsed = json.loads(content)
                if "subject" in parsed and "description" in parsed:
                    return parsed
                print(f"  [WARN] {spec['ticket_id']}: Missing fields, retry {attempt + 1}")
            except json.JSONDecodeError as e:
                print(f"  [WARN] {spec['ticket_id']}: JSON parse error ({e}), retry {attempt + 1}")
            except Exception as e:
                print(f"  [WARN] {spec['ticket_id']}: API error ({e}), retry {attempt + 1}")
                await asyncio.sleep(2 ** attempt)

    print(f"  [ERROR] {spec['ticket_id']}: Failed after 3 attempts")
    return None


async def generate_batch(
    client: AsyncAzureOpenAI,
    specs: list[dict[str, Any]],
    routing_guide: str,
    batch_num: int,
    total_batches: int,
) -> list[tuple[dict[str, Any], dict[str, Any] | None]]:
    """Generate a batch of signals concurrently."""
    semaphore = asyncio.Semaphore(15)
    print(f"\n  Batch {batch_num}/{total_batches}: generating {len(specs)} signals...")
    tasks = [generate_signal_text(client, spec, routing_guide, semaphore) for spec in specs]
    results = await asyncio.gather(*tasks)
    return list(zip(specs, results, strict=False))


async def generate_all(specs: list[dict[str, Any]], routing_guide: str) -> tuple[list[dict], list[dict]]:
    """Generate all signals in batches of 50."""
    endpoint = os.environ.get("AZURE_OPENAI_ENDPOINT", "")
    api_version = os.environ.get("AZURE_OPENAI_API_VERSION", "2025-01-01-preview")

    try:
        from azure.identity import DefaultAzureCredential, get_bearer_token_provider
        credential = DefaultAzureCredential()
        token_provider = get_bearer_token_provider(credential, "https://cognitiveservices.azure.com/.default")
        client = AsyncAzureOpenAI(
            azure_endpoint=endpoint,
            azure_ad_token_provider=token_provider,
            api_version=api_version,
            max_retries=3,
            timeout=90,
        )
        print("  Using DefaultAzureCredential for auth")
    except Exception as e:
        print(f"  DefaultAzureCredential failed ({e}), falling back to API key")
        api_key = os.environ.get("AZURE_OPENAI_API_KEY", "")
        client = AsyncAzureOpenAI(
            azure_endpoint=endpoint,
            api_key=api_key,
            api_version=api_version,
            max_retries=3,
            timeout=90,
        )

    # Process in batches of 50
    batch_size = 50
    batches = [specs[i:i + batch_size] for i in range(0, len(specs), batch_size)]
    total_batches = len(batches)

    signals: list[dict] = []
    gold: list[dict] = []
    failed = 0

    for batch_num, batch_specs in enumerate(batches, 1):
        results = await generate_batch(client, batch_specs, routing_guide, batch_num, total_batches)

        for spec, result in results:
            if result is None:
                failed += 1
                continue

            signal = {
                "ticket_id": spec["ticket_id"],
                "subject": result["subject"],
                "description": result["description"],
                "reporter": {
                    "name": spec["reporter_name"],
                    "email": spec["reporter_email"],
                    "department": spec["reporter_department"],
                },
                "created_at": spec["created_at"],
                "channel": spec["channel"],
                "attachments": [],
            }

            gold_answer = {
                "difficulty": spec["difficulty"],
                "ticket_id": spec["ticket_id"],
                "category": spec["category"],
                "priority": spec["priority"],
                "assigned_team": spec["assigned_team"],
                "needs_escalation": spec["needs_escalation"],
                "missing_information": spec["missing_information"],
                "next_best_action": "Investigate and resolve the reported issue.",
                "remediation_steps": ["Review signal details.", "Route to assigned team."],
            }

            signals.append(signal)
            gold.append(gold_answer)

        print(f"  Batch {batch_num} done. Running total: {len(signals)} signals, {failed} failed")

    print(f"\nGenerated: {len(signals)}, Failed: {failed}")
    return signals, gold


# ── Validation ───────────────────────────────────────────────────────

def validate_format(signals: list[dict], gold: list[dict]) -> bool:
    """Validate output matches expected schemas."""
    ok = True

    if len(signals) != len(gold):
        print(f"[FAIL] Signal count ({len(signals)}) != gold count ({len(gold)})")
        ok = False

    sig_ids = {s["ticket_id"] for s in signals}
    gold_ids = {g["ticket_id"] for g in gold}
    if sig_ids != gold_ids:
        print(f"[FAIL] Ticket ID mismatch: {sig_ids.symmetric_difference(gold_ids)}")
        ok = False

    valid_categories = set(CATEGORIES)
    valid_teams = {
        "Crew Identity & Airlock Control", "Spacecraft Systems Engineering",
        "Deep Space Communications", "Mission Software Operations",
        "Threat Response Command", "Telemetry & Data Core", "None",
    }
    valid_priorities = {"P1", "P2", "P3", "P4"}
    valid_channels = set(CHANNELS)
    valid_missing = set(MISSING_INFO_FIELDS)

    for s in signals:
        if not s["ticket_id"].startswith("SYN-"):
            print(f"[FAIL] Invalid ticket_id format: {s['ticket_id']}")
            ok = False
        if s["channel"] not in valid_channels:
            print(f"[FAIL] Invalid channel for {s['ticket_id']}: {s['channel']}")
            ok = False
        for field in ["subject", "description"]:
            if not s.get(field) or len(s[field]) < 5:
                print(f"[FAIL] Empty/short {field} for {s['ticket_id']}")
                ok = False

    for g in gold:
        if g["category"] not in valid_categories:
            print(f"[FAIL] Invalid category for {g['ticket_id']}: {g['category']}")
            ok = False
        if g["priority"] not in valid_priorities:
            print(f"[FAIL] Invalid priority for {g['ticket_id']}: {g['priority']}")
            ok = False
        if g["assigned_team"] not in valid_teams:
            print(f"[FAIL] Invalid team for {g['ticket_id']}: {g['assigned_team']}")
            ok = False
        if not isinstance(g["needs_escalation"], bool):
            print(f"[FAIL] needs_escalation not bool for {g['ticket_id']}")
            ok = False
        for mi in g.get("missing_information", []):
            if mi not in valid_missing:
                print(f"[FAIL] Invalid missing_info '{mi}' for {g['ticket_id']}")
                ok = False

    return ok


def validate_with_scorer(gold: list[dict]) -> None:
    """Run the official scorer (gold vs gold) to verify format compatibility."""
    sys.path.insert(0, str(ROOT / "common" / "libs" / "fdebenchkit" / "src"))
    from ms.common.fdebenchkit.scorers.ticket_triage import score_submission

    result = score_submission(gold, gold)
    print("\nScorer validation (gold vs gold):")
    print(f"  Resolution score: {result['resolution']}")
    print(f"  Dimension scores: {result['dimension_scores']}")
    print(f"  Tickets scored: {result['tickets_scored']}")
    print(f"  Errors: {result['tickets_errored']}")

    if result["resolution"] != 100.0:
        print(f"  [WARN] Expected 100.0, got {result['resolution']}")
    else:
        print("  ✓ Perfect score — format is valid")


# ── Main ─────────────────────────────────────────────────────────────

async def main() -> None:
    print("=== Synthetic Triage Dataset Generator v2 ===")
    print("=== Targeting known generalization weaknesses ===\n")

    routing_guide = ROUTING_GUIDE.read_text() if ROUTING_GUIDE.exists() else ""
    if not routing_guide:
        print("[WARN] Routing guide not found")

    # Generate specs
    print("Step 1: Generating deterministic gold label specs...")
    specs = generate_all_specs(target=500, seed=99)

    # Print distribution
    cat_counts = Counter(s["category"] for s in specs)
    pri_counts = Counter(s["priority"] for s in specs)
    diff_counts = Counter(s["difficulty"] for s in specs)
    weakness_counts = Counter(s["weakness"] for s in specs)
    team_counts = Counter(s["assigned_team"] for s in specs)
    esc_count = sum(1 for s in specs if s["needs_escalation"])

    print(f"\n  Categories: {dict(sorted(cat_counts.items()))}")
    print(f"  Priorities: {dict(sorted(pri_counts.items()))}")
    print(f"  Difficulties: {dict(diff_counts)}")
    print(f"  Weakness areas: {dict(sorted(weakness_counts.items()))}")
    print(f"  Teams: {dict(sorted(team_counts.items()))}")
    print(f"  Escalations: {esc_count}/{len(specs)}")

    # Generate signal text via LLM
    print("\nStep 2: Generating signal descriptions via Azure OpenAI (in batches of 50)...")
    signals, gold = await generate_all(specs, routing_guide)

    # Validate format
    print("\nStep 3: Validating output format...")
    format_ok = validate_format(signals, gold)
    if format_ok:
        print("  ✓ All format checks passed")

    # Save
    print("\nStep 4: Saving output files...")
    with open(OUT_SIGNALS, "w") as f:
        json.dump(signals, f, indent=4)
    print(f"  Signals: {OUT_SIGNALS} ({len(signals)} items)")

    with open(OUT_GOLD, "w") as f:
        json.dump(gold, f, indent=4)
    print(f"  Gold:    {OUT_GOLD} ({len(gold)} items)")

    # Run scorer validation
    print("\nStep 5: Running scorer validation...")
    validate_with_scorer(gold)

    # Final summary
    final_cat = Counter(g["category"] for g in gold)
    final_pri = Counter(g["priority"] for g in gold)
    final_diff = Counter(g["difficulty"] for g in gold)
    final_team = Counter(g["assigned_team"] for g in gold)
    final_esc = sum(1 for g in gold if g["needs_escalation"])

    print("\n=== FINAL SUMMARY ===")
    print(f"Total signals: {len(signals)}")
    print(f"\nCategory distribution:")
    for cat in sorted(final_cat.keys()):
        print(f"  {cat}: {final_cat[cat]}")
    print(f"\nPriority distribution:")
    for pri in sorted(final_pri.keys()):
        print(f"  {pri}: {final_pri[pri]}")
    print(f"\nDifficulty: {dict(final_diff)}")
    print(f"\nTeam distribution:")
    for team in sorted(final_team.keys()):
        print(f"  {team}: {final_team[team]}")
    print(f"\nEscalations: {final_esc}/{len(gold)}")
    print("\n=== DONE ===")


if __name__ == "__main__":
    asyncio.run(main())
