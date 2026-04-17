"""Generate synthetic Task 1 (Signal Triage) benchmark dataset v3.

Targets equal category distribution for macro-F1 optimisation:
  - 62 per category × 8 = 496, + 4 extra for rarest = 500
  - 350 standard, 150 adversarial

Focus areas (from gap analysis):
  1. Cross-category ambiguity (100): keywords from 2+ categories
  2. Priority gray zones (100): P1 calm, P2↔P3, P3↔P4 confusion
  3. Rare categories (100): Telemetry, Hull, Flight Software, Threat — 25 each
  4. Non-incidents + Briefings (100): auto-replies, thank-yous, questions, onboarding
  5. Realistic varied scenarios (100): general distribution filler

Usage:
    cd /home/fbujaroski/be-an-fde-for-a-day/py
    source .venv/bin/activate
    python apps/sample/synthetic/generate_triage_v3.py
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

# ── Paths ────────────────────────────────────────────────────────────
ROOT = Path(__file__).resolve().parents[3]  # be-an-fde-for-a-day/py
ENV_PATH = ROOT.parent / ".env"
ROUTING_GUIDE = ROOT.parent / "docs" / "challenge" / "task1" / "routing_guide.md"
OUT_DIR = Path(__file__).resolve().parent
OUT_SIGNALS = OUT_DIR / "triage_v3.json"
OUT_GOLD = OUT_DIR / "triage_v3_gold.json"

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

CATEGORY_TEAM: dict[str, str] = {
    "Communications & Navigation": "Deep Space Communications",
    "Crew Access & Biometrics": "Crew Identity & Airlock Control",
    "Hull & Structural Systems": "Spacecraft Systems Engineering",
    "Flight Software & Instruments": "Mission Software Operations",
    "Threat Detection & Containment": "Threat Response Command",
    "Telemetry & Data Banks": "Telemetry & Data Core",
    "Mission Briefing Request": "None",
    "Not a Mission Signal": "None",
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
    "Yamamoto", "Rivera", "Sokolova", "Ahmed", "Bergstrom", "Kapoor",
    "Santos", "Hayashi", "Mueller", "Osei", "Park", "Fernandez",
    "Ivanova", "Bell", "Nguyen", "Torres", "Kim", "Bjork", "Nwosu",
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


# ── Focus area 1: Cross-category ambiguity (100 signals) ─────────────

def _make_cross_category_ambiguity_specs(rng: random.Random) -> list[dict[str, Any]]:
    """100 signals with keywords from 2+ categories."""
    specs = []

    scenarios = [
        # "Relay" ambiguity: telemetry vs comms
        ("Telemetry & Data Banks", "Telemetry & Data Core", "P3",
         "Data relay module failing to forward sensor telemetry to archive — relay buffers full"),
        ("Telemetry & Data Banks", "Telemetry & Data Core", "P2",
         "Internal relay service for telemetry aggregation crashed — data not reaching storage"),
        ("Communications & Navigation", "Deep Space Communications", "P3",
         "Subspace relay intermittent, causing dropped messages to outpost Alpha"),
        ("Communications & Navigation", "Deep Space Communications", "P2",
         "Comm relay overloaded — signal routing to sector command failing"),

        # "Access" ambiguity: biometrics vs data
        ("Telemetry & Data Banks", "Telemetry & Data Core", "P3",
         "Cannot access archived telemetry logs — permission denied on data query"),
        ("Telemetry & Data Banks", "Telemetry & Data Core", "P2",
         "Data access layer returning 403 for all sensor archive queries"),
        ("Crew Access & Biometrics", "Crew Identity & Airlock Control", "P3",
         "Badge access revoked unexpectedly for deck 5 airlocks"),
        ("Crew Access & Biometrics", "Crew Identity & Airlock Control", "P2",
         "Biometric access system rejecting valid palm scans station-wide"),

        # "Console" ambiguity: software vs hardware
        ("Flight Software & Instruments", "Mission Software Operations", "P3",
         "Navigation console application crashes when loading sector charts — hardware fine"),
        ("Flight Software & Instruments", "Mission Software Operations", "P2",
         "Console software on bridge throwing unhandled exception on trajectory calc"),
        ("Hull & Structural Systems", "Spacecraft Systems Engineering", "P3",
         "Physical console panel on deck 2 shows hardware fault LED — touch unresponsive"),
        ("Hull & Structural Systems", "Spacecraft Systems Engineering", "P2",
         "Environmental console hardware unit producing error codes — display dead"),

        # "Security" ambiguity: certs vs threats vs access
        ("Threat Detection & Containment", "Threat Response Command", "P2",
         "Security certificate for weapons API expiring in 24 hours — need rotation"),
        ("Threat Detection & Containment", "Threat Response Command", "P3",
         "Security scan found suspicious process running on shared network drive"),
        ("Crew Access & Biometrics", "Crew Identity & Airlock Control", "P3",
         "Security badge system showing incorrect clearance level for my profile"),
        ("Crew Access & Biometrics", "Crew Identity & Airlock Control", "P2",
         "Security lockout triggered on entire airlock ring after badge reader glitch"),

        # "Sensor" ambiguity: hull vs telemetry vs threat
        ("Hull & Structural Systems", "Spacecraft Systems Engineering", "P3",
         "Hull integrity sensor near airlock 7 returning inconsistent pressure readings"),
        ("Telemetry & Data Banks", "Telemetry & Data Core", "P3",
         "Sensor data pipeline dropping records — archive missing last hour of readings"),
        ("Threat Detection & Containment", "Threat Response Command", "P3",
         "Perimeter sensor triggered but threat assessment shows no hostile activity"),
        ("Hull & Structural Systems", "Spacecraft Systems Engineering", "P1",
         "Hull sensor array detecting micro-fractures near viewport seal — decompression risk"),

        # "Panel" ambiguity: access vs hull vs software
        ("Crew Access & Biometrics", "Crew Identity & Airlock Control", "P3",
         "BioAuth panel at Lab 6 entrance not reading any biometric input"),
        ("Hull & Structural Systems", "Spacecraft Systems Engineering", "P3",
         "Structural monitoring panel showing hardware error near engine mount"),
        ("Flight Software & Instruments", "Mission Software Operations", "P3",
         "Control panel software for nav display stuck in boot loop"),
        ("Flight Software & Instruments", "Mission Software Operations", "P4",
         "Admin panel UI for instrument calibration has rendering glitch"),

        # "Network" ambiguity: comms vs software vs data
        ("Communications & Navigation", "Deep Space Communications", "P3",
         "Network connectivity to relay station dropping every 20 minutes"),
        ("Communications & Navigation", "Deep Space Communications", "P2",
         "Mesh network on deck 11 fully unresponsive — 30 crew without comms"),
        ("Flight Software & Instruments", "Mission Software Operations", "P3",
         "Software update server unreachable — network connection refused on flight tools"),
        ("Telemetry & Data Banks", "Telemetry & Data Core", "P3",
         "Database connection pool exhausted — network layer returning timeouts"),

        # "System" maximally ambiguous
        ("Flight Software & Instruments", "Mission Software Operations", "P2",
         "System update failed on mission planning suite — application won't launch"),
        ("Hull & Structural Systems", "Spacecraft Systems Engineering", "P3",
         "Environmental control system hardware making unusual noise on deck 8"),
        ("Communications & Navigation", "Deep Space Communications", "P2",
         "Comm system backbone router reporting critical link-state errors"),
        ("Crew Access & Biometrics", "Crew Identity & Airlock Control", "P2",
         "Identity management system sync failed — crew directory 18 hours stale"),

        # "Scan" ambiguity
        ("Crew Access & Biometrics", "Crew Identity & Airlock Control", "P3",
         "Retina scan enrollment expired — scanner won't accept my biometric"),
        ("Telemetry & Data Banks", "Telemetry & Data Core", "P3",
         "Deep-space scan results not syncing to archival database"),
        ("Hull & Structural Systems", "Spacecraft Systems Engineering", "P3",
         "Hull scan suite near engine 2 returning contradictory thickness readings"),
        ("Threat Detection & Containment", "Threat Response Command", "P2",
         "Intrusion scan detected anomalous traffic from unregistered device"),

        # "Module" ambiguity
        ("Flight Software & Instruments", "Mission Software Operations", "P3",
         "Sensor integration module in FlightOS crashes on spectral analysis"),
        ("Hull & Structural Systems", "Spacecraft Systems Engineering", "P3",
         "Habitat module B7 showing structural vibration beyond normal parameters"),
        ("Telemetry & Data Banks", "Telemetry & Data Core", "P3",
         "Data ingest module dropping records from arrays 4 and 5"),
        ("Communications & Navigation", "Deep Space Communications", "P3",
         "Comm module firmware update stalled — relay node 6 not responding to ping"),

        # "Alert" / "alarm" ambiguity
        ("Threat Detection & Containment", "Threat Response Command", "P3",
         "False alarm on containment sensor — no actual bio-hazard but needs reset"),
        ("Hull & Structural Systems", "Spacecraft Systems Engineering", "P1",
         "Pressure differential alarm on observation deck — possible viewport failure"),
        ("Telemetry & Data Banks", "Telemetry & Data Core", "P3",
         "Storage capacity alert threshold triggered — 92% full on archive array"),
        ("Communications & Navigation", "Deep Space Communications", "P3",
         "Bandwidth alert on primary comm array during peak shift hours"),

        # "Log" ambiguity: data vs software vs threat
        ("Telemetry & Data Banks", "Telemetry & Data Core", "P3",
         "Mission log archive query returning duplicate entries for sensor IDs"),
        ("Flight Software & Instruments", "Mission Software Operations", "P3",
         "FlightOS debug log growing unbounded — disk filling on nav console"),
        ("Threat Detection & Containment", "Threat Response Command", "P3",
         "Audit log showing gaps — 2 hours of access records missing"),
        ("Telemetry & Data Banks", "Telemetry & Data Core", "P4",
         "How do I export raw sensor logs to external analysis tools?"),

        # "Calibration" ambiguity: instruments vs hull sensors
        ("Flight Software & Instruments", "Mission Software Operations", "P3",
         "Instrument calibration wizard crashes on step 4 for spectral analyzer"),
        ("Hull & Structural Systems", "Spacecraft Systems Engineering", "P3",
         "Hull sensor calibration drift causing false temperature readings"),
        ("Telemetry & Data Banks", "Telemetry & Data Core", "P3",
         "Calibration offset data not being applied to archived sensor readings"),
        ("Flight Software & Instruments", "Mission Software Operations", "P4",
         "Calibration history not visible in admin panel for nav instruments"),

        # "Update" / "upgrade" ambiguity
        ("Flight Software & Instruments", "Mission Software Operations", "P3",
         "FlightOS update failed midway — mission apps stuck on old version"),
        ("Communications & Navigation", "Deep Space Communications", "P3",
         "Firmware update on relay node 3 not propagating to mesh controllers"),
        ("Crew Access & Biometrics", "Crew Identity & Airlock Control", "P3",
         "Badge firmware update bricked 4 scanners on deck 9"),
        ("Telemetry & Data Banks", "Telemetry & Data Core", "P3",
         "Database schema update broke backward-compatible queries on old data"),

        # "Timeout" ambiguity
        ("Communications & Navigation", "Deep Space Communications", "P3",
         "Subspace relay handshake timing out for long-range transmissions"),
        ("Telemetry & Data Banks", "Telemetry & Data Core", "P3",
         "Archive database queries timing out for date ranges > 30 days"),
        ("Flight Software & Instruments", "Mission Software Operations", "P3",
         "Mission planner API calls timing out when loading complex routes"),
        ("Crew Access & Biometrics", "Crew Identity & Airlock Control", "P3",
         "SSO authentication timing out during peak shift login period"),

        # "Error" ambiguity
        ("Flight Software & Instruments", "Mission Software Operations", "P2",
         "Critical error in trajectory calculation module — wrong output values"),
        ("Hull & Structural Systems", "Spacecraft Systems Engineering", "P3",
         "Environmental system error code E-447 on deck 3 ventilation unit"),
        ("Telemetry & Data Banks", "Telemetry & Data Core", "P2",
         "Data pipeline error — all incoming telemetry being silently discarded"),
        ("Communications & Navigation", "Deep Space Communications", "P3",
         "DNS resolution error affecting beacon lookups on outer ring"),

        # "Monitoring" ambiguity
        ("Telemetry & Data Banks", "Telemetry & Data Core", "P3",
         "Monitoring dashboard frozen — not updating with live sensor feeds"),
        ("Hull & Structural Systems", "Spacecraft Systems Engineering", "P3",
         "Structural monitoring sensor offline on portside hull section"),
        ("Threat Detection & Containment", "Threat Response Command", "P3",
         "Security monitoring feed for restricted corridor showing blank"),
        ("Communications & Navigation", "Deep Space Communications", "P3",
         "Network monitoring tools showing phantom devices on mesh"),

        # "Connection" / "link" ambiguity
        ("Communications & Navigation", "Deep Space Communications", "P2",
         "Primary uplink to sector command severed — backup link degraded"),
        ("Telemetry & Data Banks", "Telemetry & Data Core", "P3",
         "Database connection dropping after idle — queries fail silently"),
        ("Flight Software & Instruments", "Mission Software Operations", "P3",
         "License server connection refused — 20 instrument consoles locked out"),
        ("Crew Access & Biometrics", "Crew Identity & Airlock Control", "P3",
         "Directory sync connection to central identity service interrupted"),

        # "Backup" ambiguity
        ("Telemetry & Data Banks", "Telemetry & Data Core", "P2",
         "Backup job for critical mission data failed — no redundancy for 48 hours"),
        ("Hull & Structural Systems", "Spacecraft Systems Engineering", "P3",
         "Backup power coupling for deck 4 lighting showing fault indicator"),
        ("Communications & Navigation", "Deep Space Communications", "P3",
         "Backup comm relay not activating when primary drops"),
        ("Flight Software & Instruments", "Mission Software Operations", "P3",
         "Backup configuration for FlightOS not loading after crash recovery"),

        # "Queue" ambiguity
        ("Telemetry & Data Banks", "Telemetry & Data Core", "P3",
         "Telemetry ingest queue backing up — processing lag of 45 minutes"),
        ("Communications & Navigation", "Deep Space Communications", "P3",
         "Message queue on relay 5 overflowing during burst transmissions"),
        ("Flight Software & Instruments", "Mission Software Operations", "P3",
         "Print queue for mission reports stuck — 30 jobs pending"),
        ("Crew Access & Biometrics", "Crew Identity & Airlock Control", "P3",
         "Badge provisioning queue stalled — 8 new crew waiting for badges"),

        # More mixed scenarios
        ("Threat Detection & Containment", "Threat Response Command", "P2",
         "Malware signature detected in routine scan of engineering shared drive"),
        ("Threat Detection & Containment", "Threat Response Command", "P3",
         "Phishing email targeting crew with fake badge renewal request"),
        ("Hull & Structural Systems", "Spacecraft Systems Engineering", "P3",
         "Fabricator on deck 6 not recognizing new material cartridge format"),
        ("Crew Access & Biometrics", "Crew Identity & Airlock Control", "P4",
         "How do I update my biometric profile photo in the crew directory?"),

        # Extra for rare categories
        ("Telemetry & Data Banks", "Telemetry & Data Core", "P4",
         "Feature request: add CSV export to the telemetry dashboard"),
        ("Threat Detection & Containment", "Threat Response Command", "P4",
         "Question: what is the procedure for reporting a found unattended device?"),
        ("Hull & Structural Systems", "Spacecraft Systems Engineering", "P4",
         "Minor squeak on cargo bay door when closing — cosmetic only"),
        ("Flight Software & Instruments", "Mission Software Operations", "P4",
         "Suggestion: add dark mode to the mission planning application"),
    ]

    for cat, team, priority, hint in scenarios:
        needs_esc = (priority == "P1") or (cat == "Threat Detection & Containment" and priority in ("P1", "P2"))
        specs.append({
            "weakness": "cross_category_ambiguity",
            "hint": hint,
            "category": cat,
            "priority": priority,
            "assigned_team": team,
            "needs_escalation": needs_esc,
            "missing_information": _pick_missing_info(cat, priority, True, rng),
            "difficulty": "adversarial",
        })

    return specs[:100]


# ── Focus area 2: Priority gray zones (100 signals) ──────────────────

def _make_priority_gray_zone_specs(rng: random.Random) -> list[dict[str, Any]]:
    """100 signals testing priority calibration boundaries."""
    specs = []

    # P1 signals written with calm/understated tone (25)
    p1_calm = [
        ("Hull & Structural Systems", "Spacecraft Systems Engineering",
         "Small pressure drop noticed in section 7 — probably nothing but noting the reading"),
        ("Hull & Structural Systems", "Spacecraft Systems Engineering",
         "Seeing some atmospheric numbers that look a bit off in cargo bay C"),
        ("Hull & Structural Systems", "Spacecraft Systems Engineering",
         "Hull sensor flagged what might be a micro-fracture near airlock 3, could be sensor glitch"),
        ("Hull & Structural Systems", "Spacecraft Systems Engineering",
         "Life support panel lit up with some warnings — switched to backup, seems stable now"),
        ("Hull & Structural Systems", "Spacecraft Systems Engineering",
         "Oxygen recycler made a funny noise and went offline — we're on reserves but it's fine for now"),
        ("Threat Detection & Containment", "Threat Response Command",
         "Got a containment alarm in bio-lab but I think it's just the cat stepping on the sensor"),
        ("Threat Detection & Containment", "Threat Response Command",
         "Seeing an odd reading on the containment field monitor — might be calibration drift"),
        ("Hull & Structural Systems", "Spacecraft Systems Engineering",
         "Viewport in observation lounge has a tiny crack I just noticed — still holding pressure"),
        ("Hull & Structural Systems", "Spacecraft Systems Engineering",
         "CO2 scrubber went down but I think it'll restart on its own like last time"),
        ("Hull & Structural Systems", "Spacecraft Systems Engineering",
         "Radiation monitor spiked briefly on the port side — back to normal now but odd"),
        ("Hull & Structural Systems", "Spacecraft Systems Engineering",
         "Decompression alarm chirped once on deck 12 — didn't repeat, probably a sensor hiccup"),
        ("Threat Detection & Containment", "Threat Response Command",
         "Something tripped the intruder alarm near the server room — could be the cleaning bot"),
        ("Hull & Structural Systems", "Spacecraft Systems Engineering",
         "Temperature creeping up in core engineering — thermostat issue maybe?"),
        ("Threat Detection & Containment", "Threat Response Command",
         "Minor containment field fluctuation in the specimen lab — nothing escaped I think"),
        ("Communications & Navigation", "Deep Space Communications",
         "Navigation system seems confused — position display is way off but we're probably fine"),
        ("Hull & Structural Systems", "Spacecraft Systems Engineering",
         "Emergency seal activated on deck 8 corridor — might have been a drill glitch?"),
        ("Threat Detection & Containment", "Threat Response Command",
         "Weapons control console showing some unauthorized access attempts — probably a glitch"),
        ("Hull & Structural Systems", "Spacecraft Systems Engineering",
         "Slight hissing sound near the outer wall of section 3 — could be ventilation"),
        ("Hull & Structural Systems", "Spacecraft Systems Engineering",
         "Life support backup just kicked in automatically — primary shows fault but air is fine"),
        ("Hull & Structural Systems", "Spacecraft Systems Engineering",
         "Pressure alarm on cargo bay B went off — crew says it sealed itself"),
        ("Threat Detection & Containment", "Threat Response Command",
         "Bio-hazard sensor in ventilation giving readings — maintenance probably stirred up dust"),
        ("Hull & Structural Systems", "Spacecraft Systems Engineering",
         "Hull panel looks like it shifted a bit during that last maneuver — visual check only"),
        ("Flight Software & Instruments", "Mission Software Operations",
         "Autopilot isn't responding to course correction input — will try manual in a bit"),
        ("Hull & Structural Systems", "Spacecraft Systems Engineering",
         "Thermal regulation seems to have stopped working in the command section — getting warm"),
        ("Hull & Structural Systems", "Spacecraft Systems Engineering",
         "Airlock inner door indicator shows it's not fully sealed — outer door still closed though"),
    ]

    for cat, team, hint in p1_calm:
        specs.append({
            "weakness": "priority_gray_zone",
            "subtype": "p1_calm_tone",
            "hint": hint,
            "category": cat,
            "priority": "P1",
            "assigned_team": team,
            "needs_escalation": True,
            "missing_information": _pick_missing_info(cat, "P1", False, rng),
            "difficulty": "adversarial",
        })

    # P2 that look like P3 (25) — major issues described casually
    p2_as_p3 = [
        ("Communications & Navigation", "Deep Space Communications",
         "Subspace relay is down but we can use backup channels for now I guess"),
        ("Telemetry & Data Banks", "Telemetry & Data Core",
         "Telemetry pipeline seems to have stopped — no data flowing but maybe it's scheduled maintenance"),
        ("Flight Software & Instruments", "Mission Software Operations",
         "FlightOS crashed on all nav consoles — using paper charts for now, no big deal"),
        ("Crew Access & Biometrics", "Crew Identity & Airlock Control",
         "SSO is down for everyone — people are sharing a local admin account to work"),
        ("Communications & Navigation", "Deep Space Communications",
         "Long-range comms are completely offline — we're isolated but not in a hurry"),
        ("Telemetry & Data Banks", "Telemetry & Data Core",
         "Database server failed — running on primary only, no backup but it should be okay"),
        ("Flight Software & Instruments", "Mission Software Operations",
         "All instrument consoles locked out due to licensing — 40 people can't work"),
        ("Crew Access & Biometrics", "Crew Identity & Airlock Control",
         "Badge system rejecting 30+ crew after that update — they can't get into their sections"),
        ("Hull & Structural Systems", "Spacecraft Systems Engineering",
         "Power grid fluctuating on 3 decks — some brownouts but nothing critical I think"),
        ("Communications & Navigation", "Deep Space Communications",
         "Signal routing tables got corrupted — messages going to wrong stations but some get through"),
        ("Telemetry & Data Banks", "Telemetry & Data Core",
         "Storage array at 99% — we're dropping new telemetry data but old data is fine"),
        ("Flight Software & Instruments", "Mission Software Operations",
         "Mission planning software giving wrong trajectory calculations — double-checking manually"),
        ("Crew Access & Biometrics", "Crew Identity & Airlock Control",
         "Badge provisioning system crashed — 12 new crew arriving tomorrow with no access"),
        ("Communications & Navigation", "Deep Space Communications",
         "Bandwidth saturation on primary comm — even emergency channels affected a bit"),
        ("Hull & Structural Systems", "Spacecraft Systems Engineering",
         "Multiple fabricators across 3 decks all malfunctioning at once — no spare parts output"),
        ("Telemetry & Data Banks", "Telemetry & Data Core",
         "Data archive corruption found — might have lost 3 days of mission logs, checking"),
        ("Flight Software & Instruments", "Mission Software Operations",
         "Instrument calibration software serving wrong corrections — science data might be bad"),
        ("Crew Access & Biometrics", "Crew Identity & Airlock Control",
         "Identity directory 18 hours stale — SSO not syncing but logins still work for some"),
        ("Communications & Navigation", "Deep Space Communications",
         "DNS beacon failure station-wide — all systems resolving wrong but cached entries work"),
        ("Hull & Structural Systems", "Spacecraft Systems Engineering",
         "3 decks reporting simultaneous power coupling faults — non-essential systems browning out"),
        ("Telemetry & Data Banks", "Telemetry & Data Core",
         "Real-time telemetry feed permissions broken — entire science team locked out of data"),
        ("Flight Software & Instruments", "Mission Software Operations",
         "FlightOS sensor overlay showing wrong data on all bridge stations — using raw feeds"),
        ("Crew Access & Biometrics", "Crew Identity & Airlock Control",
         "Airlock access policy corrupted — random crew being locked out of their assigned areas"),
        ("Communications & Navigation", "Deep Space Communications",
         "Comm array lost contact with sector command — trying alternative frequencies"),
        ("Threat Detection & Containment", "Threat Response Command",
         "Unusual data exfiltration pattern on internal network — investigating but might be backups"),
    ]

    for cat, team, hint in p2_as_p3:
        needs_esc = (cat == "Threat Detection & Containment") or rng.random() < 0.15
        specs.append({
            "weakness": "priority_gray_zone",
            "subtype": "p2_casual_tone",
            "hint": hint,
            "category": cat,
            "priority": "P2",
            "assigned_team": team,
            "needs_escalation": needs_esc,
            "missing_information": _pick_missing_info(cat, "P2", False, rng),
            "difficulty": "adversarial",
        })

    # P3 that look like P4 (25) — real issues phrased as questions/comments
    p3_as_p4 = [
        ("Communications & Navigation", "Deep Space Communications",
         "Is it just me or is the relay dropping messages every few hours? Having to resend a lot"),
        ("Crew Access & Biometrics", "Crew Identity & Airlock Control",
         "Quick question — is the badge scanner on deck 5 supposed to be this slow?"),
        ("Flight Software & Instruments", "Mission Software Operations",
         "The nav console display flickers sometimes when I load star charts — is that normal?"),
        ("Telemetry & Data Banks", "Telemetry & Data Core",
         "The archive search seems much slower lately — is anyone else noticing this?"),
        ("Hull & Structural Systems", "Spacecraft Systems Engineering",
         "That buzzing from the lighting panel on deck 4 is getting pretty annoying"),
        ("Crew Access & Biometrics", "Crew Identity & Airlock Control",
         "My retina scan stopped working but my palm still does — should I re-enroll?"),
        ("Communications & Navigation", "Deep Space Communications",
         "Mesh latency spiking to 200ms during shift change — used to be 14ms"),
        ("Flight Software & Instruments", "Mission Software Operations",
         "Star chart app crashes whenever I try to load the Gamma quadrant area"),
        ("Telemetry & Data Banks", "Telemetry & Data Core",
         "Dashboard showing data from 30 minutes ago — is real-time broken?"),
        ("Hull & Structural Systems", "Spacecraft Systems Engineering",
         "Env monitor in Lab 2 gives weird temperature readings once in a while"),
        ("Crew Access & Biometrics", "Crew Identity & Airlock Control",
         "That access policy change I submitted last week still hasn't hit deck 7"),
        ("Communications & Navigation", "Deep Space Communications",
         "One relay node keeps dropping packets — backup path works fine though"),
        ("Flight Software & Instruments", "Mission Software Operations",
         "Mission log export times out if I try more than 500 entries — any tips?"),
        ("Telemetry & Data Banks", "Telemetry & Data Core",
         "Backup job for sensor logs finishing but taking 3x as long as before"),
        ("Threat Detection & Containment", "Threat Response Command",
         "Got a phishing email — obviously spam, just forwarding for your records"),
        ("Hull & Structural Systems", "Spacecraft Systems Engineering",
         "Minor vibration near engine mount 3 — within tolerance but thought I'd mention it"),
        ("Crew Access & Biometrics", "Crew Identity & Airlock Control",
         "SSO session keeps expiring after 30 min instead of 8 hours — is that a setting?"),
        ("Communications & Navigation", "Deep Space Communications",
         "Static on every third comm badge transmission — audio quality is degraded"),
        ("Flight Software & Instruments", "Mission Software Operations",
         "The instrument calibration wizard looks different — still works but UI is confusing"),
        ("Telemetry & Data Banks", "Telemetry & Data Core",
         "Data query returning some duplicate rows for certain sensor IDs — not critical"),
        ("Crew Access & Biometrics", "Crew Identity & Airlock Control",
         "Badge occasionally fails first tap at cargo bay — second tap always works"),
        ("Communications & Navigation", "Deep Space Communications",
         "Comm panel in briefing room B has slight audio echo during calls"),
        ("Flight Software & Instruments", "Mission Software Operations",
         "Navigation software sometimes shows deprecated coordinate format"),
        ("Hull & Structural Systems", "Spacecraft Systems Engineering",
         "Deck plate sensor near obs lounge showing very slight drift"),
        ("Telemetry & Data Banks", "Telemetry & Data Core",
         "Archive query sometimes returns results from the wrong date range"),
    ]

    for cat, team, hint in p3_as_p4:
        specs.append({
            "weakness": "priority_gray_zone",
            "subtype": "p3_looks_p4",
            "hint": hint,
            "category": cat,
            "priority": "P3",
            "assigned_team": team,
            "needs_escalation": False,
            "missing_information": _pick_missing_info(cat, "P3", False, rng),
            "difficulty": "adversarial",
        })

    # P4 that look like P3 (25) — mundane things phrased urgently
    p4_as_p3 = [
        ("Flight Software & Instruments", "Mission Software Operations",
         "URGENT: How do I export my mission logs to a personal datapad? Need this ASAP"),
        ("Crew Access & Biometrics", "Crew Identity & Airlock Control",
         "IMPORTANT: Is there a way to add a secondary email to my crew profile?"),
        ("Communications & Navigation", "Deep Space Communications",
         "Quick — what protocol does the subspace relay use for handshakes?"),
        ("Telemetry & Data Banks", "Telemetry & Data Core",
         "The font size on the telemetry dashboard is WAY too small — can't read anything"),
        ("Hull & Structural Systems", "Spacecraft Systems Engineering",
         "HELP: The light in my quarters closet flickers when I open the door"),
        ("Flight Software & Instruments", "Mission Software Operations",
         "CRITICAL REQUEST: Please update the splash screen — still shows last year's logo"),
        ("Crew Access & Biometrics", "Crew Identity & Airlock Control",
         "Need help immediately — how do I change my profile photo in the directory?"),
        ("Communications & Navigation", "Deep Space Communications",
         "Feature request NEEDED: dark mode for comm monitoring — eyes burning on night shift"),
        ("Telemetry & Data Banks", "Telemetry & Data Core",
         "Cannot find documentation for the new telemetry API — this is blocking me!"),
        ("Hull & Structural Systems", "Spacecraft Systems Engineering",
         "The label on junction box 14B is peeling off — it's confusing our new crew"),
        ("Flight Software & Instruments", "Mission Software Operations",
         "Mission planner MUST have an undo button — I keep losing my work"),
        ("Crew Access & Biometrics", "Crew Identity & Airlock Control",
         "Can I use my badge for both gym and lab? Need to know right now"),
        ("Communications & Navigation", "Deep Space Communications",
         "Typo on comm status page says 'recieved' — making us look unprofessional"),
        ("Telemetry & Data Banks", "Telemetry & Data Core",
         "We desperately need CSV export on the data dashboard — Excel won't import JSON"),
        ("Hull & Structural Systems", "Spacecraft Systems Engineering",
         "Cargo bay door squeaks when closing — it's driving everyone crazy"),
        ("Flight Software & Instruments", "Mission Software Operations",
         "The keyboard shortcut guide for FlightOS is incomplete — very frustrating"),
        ("Crew Access & Biometrics", "Crew Identity & Airlock Control",
         "How often do biometric templates refresh? This has been bugging me"),
        ("Communications & Navigation", "Deep Space Communications",
         "We NEED a notification sound for incoming subspace messages"),
        ("Telemetry & Data Banks", "Telemetry & Data Core",
         "Dashboard timestamps should be in local station time — UTC is confusing everyone"),
        ("Hull & Structural Systems", "Spacecraft Systems Engineering",
         "Paint chipping on corridor wall near Section 5 — looks terrible"),
        ("Flight Software & Instruments", "Mission Software Operations",
         "The tooltip text on the instrument panel is wrong — says 'click' but it's a tap"),
        ("Crew Access & Biometrics", "Crew Identity & Airlock Control",
         "Where do I find the badge FAQ? Searched everywhere, can't locate it"),
        ("Communications & Navigation", "Deep Space Communications",
         "The old comm interface should be retired — everyone prefers the new one"),
        ("Telemetry & Data Banks", "Telemetry & Data Core",
         "Can we get a color-blind friendly mode on the sensor data visualization?"),
        ("Hull & Structural Systems", "Spacecraft Systems Engineering",
         "Carpet in crew quarters hallway is wearing thin — could someone look at it?"),
    ]

    for cat, team, hint in p4_as_p3:
        specs.append({
            "weakness": "priority_gray_zone",
            "subtype": "p4_urgent_tone",
            "hint": hint,
            "category": cat,
            "priority": "P4",
            "assigned_team": team,
            "needs_escalation": False,
            "missing_information": _pick_missing_info(cat, "P4", False, rng),
            "difficulty": "adversarial",
        })

    return specs


# ── Focus area 3: Rare categories (100 signals) ─────────────────────

def _make_rare_category_specs(rng: random.Random) -> list[dict[str, Any]]:
    """100 signals for underrepresented categories: 25 each."""
    specs = []

    # Telemetry & Data Banks (25)
    telemetry = [
        ("P2", "Telemetry pipeline completely down — no sensor data reaching mission control"),
        ("P2", "Archive corruption detected — 5 days of critical experiment data at risk"),
        ("P2", "Storage array failed — active telemetry being dropped with no backup"),
        ("P3", "Sensor array 7 data delayed by 10 minutes — processing bottleneck"),
        ("P3", "Telemetry dashboard widget not auto-refreshing — need manual reload"),
        ("P3", "Backup job for environmental sensor data completing but with errors"),
        ("P3", "Data query API returning incorrect aggregation for multi-day ranges"),
        ("P3", "Archive search returning partial results for deep space survey data"),
        ("P3", "Sensor data timestamp mismatch between raw feed and stored records"),
        ("P3", "Replication lag between primary and secondary data nodes is 2 hours"),
        ("P3", "Telemetry ingest service dropping records during burst periods"),
        ("P3", "Sensor calibration data not being applied to incoming readings"),
        ("P3", "Data export function generating malformed output files"),
        ("P3", "Historical query performance degraded after last schema migration"),
        ("P4", "How do I set up automated alerts for sensor threshold breaches?"),
        ("P4", "Documentation for telemetry API v3 endpoints seems outdated"),
        ("P4", "Can we add a histogram view to the sensor data dashboard?"),
        ("P4", "Feature request: ability to tag sensor data with experiment IDs"),
        ("P4", "Would like to customize the default time range on the dashboard"),
        ("P4", "Question about data retention policy for non-critical sensor logs"),
        ("P2", "All telemetry streams showing zero values — sensors report normal"),
        ("P3", "Data deduplication process removing valid records — false matches"),
        ("P3", "Real-time feed showing 15-second lag instead of sub-second"),
        ("P3", "Cross-reference query between sensor arrays timing out consistently"),
        ("P4", "Suggestion: add data lineage tracking to the telemetry pipeline"),
    ]

    for priority, hint in telemetry:
        specs.append({
            "weakness": "rare_category",
            "hint": hint,
            "category": "Telemetry & Data Banks",
            "priority": priority,
            "assigned_team": "Telemetry & Data Core",
            "needs_escalation": priority == "P1",
            "missing_information": _pick_missing_info("Telemetry & Data Banks", priority, False, rng),
            "difficulty": "standard",
        })

    # Hull & Structural Systems (25)
    hull = [
        ("P1", "Hull breach alarm triggered on deck 14 — automatic sealing engaged"),
        ("P1", "Atmospheric pressure dropping in section 6 — possible seal failure"),
        ("P1", "Decompression warning in cargo bay A — crew evacuating"),
        ("P1", "Life-support CO2 scrubbers showing cascade failure across all units"),
        ("P1", "Radiation shielding degraded on starboard side — exposure levels rising"),
        ("P2", "Power grid instability on 4 decks — non-essential systems offline"),
        ("P2", "Environmental control system failure on deck 5 — temperature at 35°C"),
        ("P2", "Multiple fabricators offline simultaneously — no spare parts production"),
        ("P3", "Deck 4 lighting buzzing — illumination fine but noise is constant"),
        ("P3", "Environmental sensor reading 2°C high on deck 3"),
        ("P3", "Fabricator in workshop C not accepting new material cartridges"),
        ("P3", "Auxiliary power coupling showing intermittent fault on deck 7"),
        ("P3", "Minor vibration detected near propulsion mount 2"),
        ("P3", "Waste recycler efficiency dropped to 60% from usual 95%"),
        ("P3", "Gravity plating on deck 9 corridor showing slight variation"),
        ("P4", "Label on junction box 22A is illegible — needs replacement"),
        ("P4", "Cargo bay door makes grinding noise — functional but annoying"),
        ("P4", "Paint chipping near the main corridor junction — cosmetic"),
        ("P4", "Can someone explain the maintenance schedule for hull sensors?"),
        ("P4", "Request to install additional handrails in zero-g transition zone"),
        ("P2", "Airlock cycling mechanism jammed — outer door won't seal properly"),
        ("P3", "Water recycler showing elevated mineral content in output"),
        ("P3", "Air filtration unit on deck 12 running at reduced capacity"),
        ("P3", "Deck plating expansion joint showing signs of wear"),
        ("P4", "The observation deck chairs are uncomfortable — can we get cushions?"),
    ]

    for priority, hint in hull:
        needs_esc = priority == "P1"
        specs.append({
            "weakness": "rare_category",
            "hint": hint,
            "category": "Hull & Structural Systems",
            "priority": priority,
            "assigned_team": "Spacecraft Systems Engineering",
            "needs_escalation": needs_esc,
            "missing_information": _pick_missing_info("Hull & Structural Systems", priority, False, rng),
            "difficulty": "standard",
        })

    # Flight Software & Instruments (25)
    flight_sw = [
        ("P1", "Autopilot locked in incorrect trajectory — manual override not responding"),
        ("P2", "FlightOS crashed across all navigation consoles — running on backup only"),
        ("P2", "Mission planning software returning corrupted trajectory calculations"),
        ("P2", "Licensing server down — 40+ instrument consoles locked out"),
        ("P2", "Instrument calibration software serving wrong correction factors"),
        ("P3", "Star chart overlay misaligned with current position data"),
        ("P3", "Instrument readout lag of 5 seconds on secondary science console"),
        ("P3", "Mission planner crashes when route has more than 20 waypoints"),
        ("P3", "Nav software showing deprecated coordinate format for new sectors"),
        ("P3", "Calibration wizard for spectral analyzer incomplete — skips step 3"),
        ("P3", "FlightOS memory leak — performance degrades after 48 hours uptime"),
        ("P3", "Sensor data visualization rendering incorrectly on wide displays"),
        ("P3", "Mission report generator producing wrong units for velocity"),
        ("P3", "Automated trajectory optimizer suggesting inefficient routes"),
        ("P3", "Instrument firmware update mechanism failing silently"),
        ("P4", "Feature request: add waypoint search to mission planner"),
        ("P4", "Keyboard shortcut documentation is incomplete for FlightOS"),
        ("P4", "The splash screen on nav console still shows old branding"),
        ("P4", "Can someone explain how to use the spectral analysis tool?"),
        ("P4", "Suggestion: mission planner needs an undo function"),
        ("P2", "All science instrument consoles showing sensor data from wrong array"),
        ("P3", "Batch processing of stellar data stuck at 60% completion"),
        ("P3", "FlightOS audit log not recording certain admin actions"),
        ("P3", "Nav console rendering engine stuttering during approach maneuvers"),
        ("P4", "Would like to customize the default view on instrument dashboard"),
    ]

    for priority, hint in flight_sw:
        needs_esc = priority == "P1"
        specs.append({
            "weakness": "rare_category",
            "hint": hint,
            "category": "Flight Software & Instruments",
            "priority": priority,
            "assigned_team": "Mission Software Operations",
            "needs_escalation": needs_esc,
            "missing_information": _pick_missing_info("Flight Software & Instruments", priority, False, rng),
            "difficulty": "standard",
        })

    # Threat Detection & Containment (25)
    threat = [
        ("P1", "Active hostile vessel on intercept course — confirmed by long-range sensors"),
        ("P1", "Containment field failure in bio-lab 2 — specimens may have escaped"),
        ("P1", "Confirmed security breach — unauthorized individual in weapons storage"),
        ("P1", "Unknown biological agent in ventilation — deck 5 crew reporting symptoms"),
        ("P2", "Unauthorized data access — someone pulled classified files from archives"),
        ("P2", "Suspicious login from unregistered device on command network"),
        ("P2", "Malware signature found during routine scan of shared engineering drive"),
        ("P2", "Data exfiltration attempt blocked — source traced to internal terminal"),
        ("P2", "Certificate for weapons control API compromised — rotation required"),
        ("P3", "Phishing email received — lottery scam, not clicking, forwarding for records"),
        ("P3", "Spam message pretending to be from Command — forwarding for awareness"),
        ("P3", "False positive on security scan — flagged known safe file"),
        ("P3", "Outdated service account found in audit — no evidence of misuse"),
        ("P3", "SSL certificate warning on internal page — just needs renewal"),
        ("P3", "Containment protocol documentation references deprecated procedures"),
        ("P3", "Low-severity finding from latest automated security scan"),
        ("P3", "Access log shows brief anomaly for decommissioned account"),
        ("P4", "Question: what is the process for requesting a security clearance upgrade?"),
        ("P4", "Can someone review the containment drill schedule for next quarter?"),
        ("P4", "Perimeter sensor sensitivity — is the current threshold optimal?"),
        ("P2", "Multiple unauthorized access attempts to restricted database"),
        ("P3", "Security camera in corridor 7 showing static — feed intermittent"),
        ("P3", "Firewall rule blocking legitimate traffic to science lab network"),
        ("P3", "Intrusion detection system generating excessive false alerts"),
        ("P4", "Request for updated security awareness training materials"),
    ]

    for priority, hint in threat:
        needs_esc = priority == "P1" or (priority == "P2")
        specs.append({
            "weakness": "rare_category",
            "hint": hint,
            "category": "Threat Detection & Containment",
            "priority": priority,
            "assigned_team": "Threat Response Command",
            "needs_escalation": needs_esc,
            "missing_information": _pick_missing_info("Threat Detection & Containment", priority, False, rng),
            "difficulty": "standard",
        })

    return specs


# ── Focus area 4: Non-incidents + Briefings (100 signals) ───────────

def _make_non_incident_specs(rng: random.Random) -> list[dict[str, Any]]:
    """100 signals: 50 Not a Mission Signal + 50 Mission Briefing Request."""
    specs = []

    # Not a Mission Signal (50)
    nams = [
        ("thank_you", "Thanks for fixing the relay yesterday — running smoothly now"),
        ("thank_you", "Just wanted to say the BioAuth panel is perfect after your fix"),
        ("thank_you", "Nav console update resolved everything — great work team"),
        ("thank_you", "Much appreciated on that hull sensor recalibration"),
        ("thank_you", "The comm array fix from last cycle is holding perfectly"),
        ("thank_you", "Quick shoutout for the fast turnaround on my access request"),
        ("thank_you", "Telemetry pipeline fix is working beautifully — data flowing again"),
        ("thank_you", "Wanted to thank whoever patched the FlightOS bug — mission-saver"),
        ("ooo_cryo", "Going into cryo-stasis from stardate 47634 — redirect to Lt. Chen"),
        ("ooo_cryo", "Off-shift for deep sleep rotation — Sgt. Patel has my duties"),
        ("ooo_cryo", "Medical leave from 0800 today through end of month"),
        ("ooo_cryo", "Auto-reply: Currently in cryo-hibernation cycle 7"),
        ("ooo_cryo", "Shore leave at Starbase Gamma until the 28th — no comms needed"),
        ("resolved", "Got it working — just needed to recalibrate the phase discriminator"),
        ("resolved", "False alarm — badge battery was dead, all good now"),
        ("resolved", "Disregard my earlier report — console rebooted and fixed itself"),
        ("resolved", "Found the answer in the wiki — closing this out"),
        ("resolved", "Intermittent dropouts were scheduled maintenance — never mind"),
        ("resolved", "Was using wrong frequency band — my mistake, sorry"),
        ("auto_reply", "Automated message confirming receipt of signal SIG-3001"),
        ("auto_reply", "Auto-forward from Medical Bay re: annual physical schedule"),
        ("auto_reply", "Delivery notification: your message to Engineering was delivered"),
        ("auto_reply", "This mailbox is not monitored — contact Bridge Ops for urgent matters"),
        ("auto_reply", "Automated acknowledgement — request #5588 logged in queue"),
        ("broadcast", "Reminder: emergency drill at 0800 tomorrow — NOT a real emergency"),
        ("broadcast", "Station-wide: protein cube supply restocked in all mess halls"),
        ("broadcast", "FYI: rec lounge holoprojector maintenance 1400-1600 today"),
        ("broadcast", "Stardate corrections posted — check updated calendar in crew portal"),
        ("broadcast", "Annual safety certification due by end of cycle 12"),
        ("spam", "CONGRATULATIONS! You won the Galactic Lottery — claim 10M credits NOW"),
        ("spam", "Urgent: station account compromised — click here to verify identity"),
        ("spam", "Buy genuine Romulan ale at 50% off — limited time for CDSS crew"),
        ("spam", "Forward: chain message for good luck on your next mission"),
        ("spam", "Selected for free Premium Quarters upgrade — act fast"),
        ("wrong_channel", "What's the cafeteria schedule for gamma shift?"),
        ("wrong_channel", "Has anyone seen Nebula the station cat? Missing since Tuesday"),
        ("wrong_channel", "Dress code for the ambassador reception tomorrow?"),
        ("wrong_channel", "Is the gym open during night cycle? Asking for security team"),
        ("wrong_channel", "Holodeck program recommendations anyone?"),
        ("social", "Happy birthday Lt. Chen! Celebrating in Mess Hall B at 1900"),
        ("social", "Movie night Friday — vote on the rec room terminal"),
        ("social", "Lost: personal datapad left in observation lounge"),
        ("social", "Petition to name new lab module after Dr. Mehta — sign on portal"),
        ("social", "Congrats to Ensign Park on the promotion — well deserved"),
        ("social", "Vending machine on Deck 7 dispensing wrong nutrient paste flavor"),
        ("wrong_channel", "Anyone up for zero-g basketball after shift? Cargo Bay 3"),
        ("social", "Welcome aboard new engineering team — see you at orientation"),
        ("resolved", "Update: the sensor anomaly I reported resolved on its own"),
        ("broadcast", "Quarterly crew appreciation lunch in the mess hall tomorrow 1200"),
        ("wrong_channel", "Can someone recommend a good sleep cycle app for the night rotation?"),
    ]

    for subtype, hint in nams:
        specs.append({
            "weakness": "non_incident",
            "subtype": subtype,
            "hint": hint,
            "category": "Not a Mission Signal",
            "priority": "P4",
            "assigned_team": "None",
            "needs_escalation": False,
            "missing_information": [],
            "difficulty": "adversarial" if subtype in ("spam", "auto_reply") else "standard",
        })

    # Mission Briefing Request (50)
    briefings = [
        ("onboarding_setup", "Spacecraft Systems Engineering", "P3",
         "New science officer arriving next week — needs full station access"),
        ("onboarding_setup", "Spacecraft Systems Engineering", "P3",
         "Three engineering interns starting — need workstations and badges"),
        ("onboarding_setup", "Spacecraft Systems Engineering", "P2",
         "Commander Vasquez transferring in — needs bridge-level clearance urgently"),
        ("onboarding_setup", "Spacecraft Systems Engineering", "P3",
         "New medical staff joining — need lab access, quarters, system accounts"),
        ("onboarding_setup", "Spacecraft Systems Engineering", "P3",
         "Civilian researcher Dr. Kim needs temp access to Stellar Cartography"),
        ("onboarding_setup", "Spacecraft Systems Engineering", "P3",
         "5 data science recruits arriving stardate 47700 — provision accounts"),
        ("onboarding_setup", "Spacecraft Systems Engineering", "P3",
         "Diplomatic attaché needs guest quarters and limited network for 30 days"),
        ("onboarding_setup", "Spacecraft Systems Engineering", "P3",
         "New pilot transferring from Starbase 12 — needs flight sim access"),
        ("offboarding_disable", "Crew Identity & Airlock Control", "P3",
         "Lt. Chen departing next cycle — disable all access and accounts"),
        ("offboarding_disable", "Crew Identity & Airlock Control", "P2",
         "Crew member Petrov transferring — revoke biometric access to Labs 3-7 today"),
        ("offboarding_disable", "Crew Identity & Airlock Control", "P3",
         "Ensign O'Brien tour ends Friday — standard departure procedures"),
        ("offboarding_disable", "Crew Identity & Airlock Control", "P3",
         "Dr. Sharma retiring — full offboarding: access, files, equipment"),
        ("offboarding_disable", "Crew Identity & Airlock Control", "P3",
         "Contractor team project ended — remove all visitor access"),
        ("offboarding_disable", "Crew Identity & Airlock Control", "P2",
         "3 officers rotating to Starbase Gamma — exit processing needed ASAP"),
        ("offboarding_disable", "Crew Identity & Airlock Control", "P3",
         "Sgt. Rivera discharged — deactivate biometric profile effective today"),
        ("room_booking", "None", "P4",
         "Need Briefing Room Alpha for 0900 delegation meeting tomorrow"),
        ("room_booking", "None", "P4",
         "Book main conference room for 2-hour mission planning session"),
        ("room_booking", "None", "P4",
         "Reserve Holodeck 3 for crew training Tuesday 0800-1200"),
        ("room_booking", "None", "P4",
         "Need secure briefing room for classified review Friday"),
        ("room_booking", "None", "P4",
         "Reserve Lab 5 for week-long experiment starting next cycle"),
        ("equipment_provision", "Spacecraft Systems Engineering", "P3",
         "Need 3 workstations for new engineering team by Friday"),
        ("equipment_provision", "Spacecraft Systems Engineering", "P3",
         "Requesting portable scanner kit for away team mission"),
        ("equipment_provision", "Spacecraft Systems Engineering", "P3",
         "Lab needs new holoprojector for next week's presentation"),
        ("equipment_provision", "Spacecraft Systems Engineering", "P4",
         "Request 10 replacement datapads for training cohort"),
        ("equipment_provision", "Spacecraft Systems Engineering", "P3",
         "Need secure terminal installed in new intelligence office"),
        ("software_howto", "Mission Software Operations", "P4",
         "How do I request a security badge replacement?"),
        ("software_howto", "Mission Software Operations", "P4",
         "Process for changing biometric enrollment?"),
        ("software_howto", "Mission Software Operations", "P4",
         "How to set up remote access to mission planning tools?"),
        ("software_howto", "Mission Software Operations", "P4",
         "Where's the form for shift schedule change requests?"),
        ("software_howto", "Mission Software Operations", "P4",
         "Procedure for reporting a lost communicator?"),
        ("status_inquiry", "None", "P4",
         "What's the ETA on my access request from last week?"),
        ("status_inquiry", "None", "P4",
         "Checking on workstation order from 3 days ago"),
        ("status_inquiry", "None", "P4",
         "Update on conference room booking for Thursday?"),
        ("status_inquiry", "None", "P4",
         "Transfer paperwork submitted 5 cycles ago — status?"),
        ("status_inquiry", "None", "P4",
         "Following up on lab equipment request"),
        ("status_inquiry", "None", "P4",
         "New crew badges — told 48 hours, been a week"),
        ("status_inquiry", "None", "P4",
         "Security clearance application status for my team?"),
        ("status_inquiry", "None", "P4",
         "Has medical supplies requisition been processed?"),
        ("status_inquiry", "None", "P4",
         "Has IT started on the network extension to new wing?"),
        ("general_admin", "None", "P4",
         "Can someone help me locate the inventory management documentation?"),
        ("onboarding_setup", "Spacecraft Systems Engineering", "P3",
         "Visiting ambassador delegation needs temporary comms and navigation access"),
        ("offboarding_disable", "Crew Identity & Airlock Control", "P3",
         "Temporary research crew departing — revoke all lab and data access"),
        ("room_booking", "None", "P4",
         "Block observation lounge for awards ceremony next Tuesday"),
        ("equipment_provision", "Spacecraft Systems Engineering", "P3",
         "Need 2 additional monitoring consoles in Telemetry Bay C"),
        ("software_howto", "Mission Software Operations", "P4",
         "How to update emergency contact information in the system?"),
        ("software_howto", "Mission Software Operations", "P4",
         "Walk me through the new inventory requisition portal?"),
        ("general_admin", "None", "P4",
         "Where can I find the standard operating procedures document?"),
        ("room_booking", "None", "P4",
         "Small huddle room near Engineering for daily standups"),
        ("equipment_provision", "Spacecraft Systems Engineering", "P3",
         "Need additional portable terminals for the EVA team"),
        ("onboarding_setup", "Spacecraft Systems Engineering", "P3",
         "4 new security officers arriving — need full system provisioning"),
    ]

    for subtype, team, priority, hint in briefings:
        specs.append({
            "weakness": "non_incident",
            "subtype": subtype,
            "hint": hint,
            "category": "Mission Briefing Request",
            "priority": priority,
            "assigned_team": team,
            "needs_escalation": False,
            "missing_information": _pick_missing_info("Mission Briefing Request", priority, False, rng),
            "difficulty": "standard",
        })

    return specs


# ── Focus area 5: General filler (100 signals) ──────────────────────

def _make_filler_specs(rng: random.Random, count: int) -> list[dict[str, Any]]:
    """General distribution filler to balance category counts."""
    specs = []

    filler_hints = {
        "Communications & Navigation": [
            "Subspace relay latency spike on frequency band 4",
            "Local comm mesh showing packet loss on deck 8",
            "Signal routing inconsistency between relay nodes 2 and 5",
            "Comm badge interference near the engineering section",
            "DNS beacon update not propagating to outer ring terminals",
            "Voice comm quality degraded during solar flare activity",
            "Relay node 9 firmware outdated — performance degraded",
            "Interstation link unstable since last maintenance window",
        ],
        "Crew Access & Biometrics": [
            "Badge reader on deck 5 requires double-tap sometimes",
            "Directory sync still showing my old department",
            "SSO login prompt appearing more frequently than before",
            "Guest access badge expired for conference room",
            "Biometric enrollment screen hanging on step 3 of 4",
            "New crew badge not activating for restricted zones",
            "Badge photo doesn't match after recent update",
            "Multi-factor auth prompt not showing on deck terminals",
        ],
        "Hull & Structural Systems": [
            "Corridor vibration near storage bay — slight but persistent",
            "Environmental sensor on deck 3 reading 2°C high",
            "Fabricator in workshop B rejecting material cartridges",
            "Deck plate sensor near observation lounge showing drift",
            "Power coupling for auxiliary lights intermittent",
            "Air quality sensor in Lab 4 needs recalibration",
            "Water pressure low in crew quarters section C",
        ],
        "Flight Software & Instruments": [
            "Star chart overlay not aligning with position data",
            "Instrument readout lag on secondary science console",
            "Mission planner tool crashes with 20+ waypoints",
            "Nav software showing deprecated coordinate format",
            "Calibration wizard for spectral analyzer missing steps",
            "FlightOS auto-save corrupting large mission files",
            "Orbital calculation rounding errors in edge cases",
        ],
        "Threat Detection & Containment": [
            "Completed security scan with one low finding",
            "Containment protocol docs reference old procedures",
            "Old service account found in access log audit",
            "Perimeter sensor sensitivity seems miscalibrated",
            "Security certificate renewal reminder for gateway",
            "Firewall logs showing unusual traffic pattern to review",
        ],
        "Telemetry & Data Banks": [
            "Sensor data from array 3 arriving with 5-min delay",
            "Archive query returning wrong date range results",
            "Dashboard widget not auto-refreshing",
            "Storage utilization report showing discrepancy",
            "Backup job for deck 7 sensors skipping entries",
            "Data pipeline latency increased after config change",
        ],
        "Mission Briefing Request": [
            "Need access credentials for visiting inspector",
            "Shared workspace setup for cross-team project",
            "Room booking for weekly departmental sync",
            "Equipment requisition for field research kit",
        ],
        "Not a Mission Signal": [
            "Thanks — that fix is working perfectly now",
            "Out of office until next rotation cycle",
            "Resolved my own issue — config mismatch fixed",
            "Social: crew trivia night at 2000 in the rec room",
        ],
    }

    # Categories that need more representation in filler
    cats_for_filler = [
        "Communications & Navigation",
        "Crew Access & Biometrics",
        "Hull & Structural Systems",
        "Flight Software & Instruments",
        "Threat Detection & Containment",
        "Telemetry & Data Banks",
        "Mission Briefing Request",
        "Not a Mission Signal",
    ]

    for i in range(count):
        cat = cats_for_filler[i % len(cats_for_filler)]
        team = CATEGORY_TEAM[cat]

        if cat == "Mission Briefing Request":
            team = rng.choice(["None", "Spacecraft Systems Engineering",
                               "Crew Identity & Airlock Control", "Mission Software Operations"])

        hints = filler_hints.get(cat, ["Standard issue"])
        hint = hints[i % len(hints)]

        if cat == "Not a Mission Signal":
            priority = "P4"
        elif cat == "Mission Briefing Request":
            priority = rng.choice(["P3", "P4", "P4"])
        else:
            priority = rng.choices(["P1", "P2", "P3", "P4"], [0.05, 0.15, 0.50, 0.30])[0]

        if priority == "P1":
            needs_esc = True
        elif cat == "Threat Detection & Containment" and priority == "P2":
            needs_esc = True
        else:
            needs_esc = False

        specs.append({
            "weakness": "filler",
            "hint": hint,
            "category": cat,
            "priority": priority,
            "assigned_team": team,
            "needs_escalation": needs_esc,
            "missing_information": _pick_missing_info(cat, priority, False, rng),
            "difficulty": "standard",
        })

    return specs


# ── Assemble all specs ───────────────────────────────────────────────

def generate_all_specs(target: int = 500, seed: int = 43) -> list[dict[str, Any]]:
    """Build the full spec list with equal category distribution."""
    rng = random.Random(seed)

    specs: list[dict[str, Any]] = []
    specs.extend(_make_cross_category_ambiguity_specs(rng))  # 100
    specs.extend(_make_priority_gray_zone_specs(rng))        # 100
    specs.extend(_make_rare_category_specs(rng))             # 100
    specs.extend(_make_non_incident_specs(rng))              # 100

    # Count categories so far
    cat_counts = Counter(s["category"] for s in specs)
    print(f"  Before filler: {dict(sorted(cat_counts.items()))}")

    # Add filler (100) to approach equal distribution
    filler_needed = target - len(specs)
    if filler_needed > 0:
        specs.extend(_make_filler_specs(rng, filler_needed))

    # Shuffle deterministically
    rng.shuffle(specs)

    # Assign metadata
    used_names: set[str] = set()
    for i, spec in enumerate(specs):
        spec["ticket_id"] = f"SYN-{7000 + i}"

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
        spec["reporter_department"] = rng.choice(DEPARTMENTS)

        if spec["priority"] == "P1":
            spec["channel"] = rng.choice(["emergency_beacon", "bridge_terminal"])
        else:
            spec["channel"] = rng.choice(CHANNELS)

        day = rng.randint(1, 28)
        hour = rng.randint(0, 23)
        minute = rng.randint(0, 59)
        spec["created_at"] = f"2026-04-{day:02d}T{hour:02d}:{minute:02d}:00Z"

    return specs[:target]


# ── LLM prompt builder ──────────────────────────────────────────────

def build_generation_prompt(spec: dict[str, Any]) -> str:
    priority_context = {
        "P1": "CRITICAL — hull breach, life-support failure, containment failure, hostile contact, decompression",
        "P2": "HIGH — major system failure, no workaround, multiple crew affected, no immediate safety threat",
        "P3": "STANDARD — operational issue with workaround or limited scope, single user/system",
        "P4": "LOW — routine question, minor annoyance, cosmetic issue, informational",
    }

    cat_guidance = {
        "Not a Mission Signal": (
            "This is NOT a support ticket. Generate one of: thank-you, out-of-office/cryo notice, "
            "self-resolved closure, auto-reply, broadcast, spam/phishing, social message, wrong channel question. "
            "NO technical issues or support requests."
        ),
        "Mission Briefing Request": (
            "This is an admin/logistics request, NOT a technical incident: onboarding, offboarding, "
            "room booking, equipment provisioning, how-to question, or status inquiry."
        ),
    }

    weakness_guidance = {
        "cross_category_ambiguity": (
            "ADVERSARIAL: Use keywords that suggest a DIFFERENT category, but the actual issue belongs "
            "to the target category. Subject can be misleading; description must point to correct category."
        ),
        "priority_gray_zone": {
            "p1_calm_tone": (
                "Write this P1-CRITICAL signal in a very CALM, understated tone. "
                "The crew member downplays the severity — says 'probably nothing', 'might be a glitch', "
                "'seems fine for now'. But the underlying issue IS critical (hull/life-support/containment/hostile)."
            ),
            "p2_casual_tone": (
                "Write this P2-HIGH signal casually, as if the reporter doesn't realize the severity. "
                "Describe a MAJOR system failure but use phrases like 'no big deal', 'should be okay', "
                "'probably fine'. The scope of impact (multiple crew, no workaround) must come through."
            ),
            "p3_looks_p4": (
                "Write this P3-STANDARD signal as a question or offhand comment. "
                "The reporter phrases it casually ('is it just me?', 'is this normal?') but describes "
                "a real operational issue with measurable impact."
            ),
            "p4_urgent_tone": (
                "Write this P4-LOW signal with URGENT language ('CRITICAL', 'HELP', 'ASAP'). "
                "But the actual issue is purely cosmetic, a question, or a feature request."
            ),
        },
        "rare_category": "Generate a clear, unambiguous signal for this category.",
        "non_incident": "Generate a signal that clearly belongs to this non-technical category.",
        "filler": "Generate a standard, realistic signal for this category.",
    }

    wg = weakness_guidance.get(spec.get("weakness", ""), "")
    if isinstance(wg, dict):
        wg = wg.get(spec.get("subtype", ""), "")

    cat_note = cat_guidance.get(spec["category"], "")

    missing_note = ""
    if spec["missing_information"]:
        fields = ", ".join(spec["missing_information"])
        missing_note = f"\nMISSING INFO: The signal should naturally lack: {fields}. Do NOT include these details."

    escalation_hint = ""
    if spec["needs_escalation"] and spec["priority"] != "P1":
        escalation_hint = "\nInclude hints of escalation need: recurring issue, command-level reporter, or hostile/security risk."

    return f"""Generate a realistic space station IT support signal for the Contoso Deep Space Station (CDSS).

TARGET LABELS (do NOT include in signal text):
- Category: {spec["category"]}
- Priority: {spec["priority"]} ({priority_context[spec["priority"]]})
- Team: {spec["assigned_team"]}
- Needs Escalation: {spec["needs_escalation"]}

SCENARIO: {spec.get("hint", "Generate realistic signal")}

{cat_note}
{wg}
{missing_note}
{escalation_hint}

RULES:
1. Write ONLY subject and description. No other fields.
2. Description: 2-6 sentences, first person, as a real crew member.
3. Include specific technical details relevant to the category.
4. Match tone to priority (P1=urgent unless told otherwise, P4=casual).
5. Occasional personality (station cats, protein cubes, Mehta's notes) is fine.
6. Do NOT include category/priority/team names in the text.
7. Make it feel like a real support ticket.

Respond with ONLY valid JSON:
{{"subject": "...", "description": "..."}}"""


# ── LLM generation ──────────────────────────────────────────────────

async def generate_signal_text(
    client,  # AsyncAzureOpenAI
    spec: dict[str, Any],
    semaphore: asyncio.Semaphore,
) -> dict[str, Any] | None:
    prompt = build_generation_prompt(spec)

    async with semaphore:
        for attempt in range(3):
            try:
                resp = await client.chat.completions.create(
                    model="gpt-5-4",
                    messages=[
                        {"role": "system", "content": "Generate realistic space station support signals. Respond with valid JSON only. No markdown fences."},
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


async def generate_batch(client, specs, batch_num, total_batches):
    semaphore = asyncio.Semaphore(15)
    print(f"\n  Batch {batch_num}/{total_batches}: generating {len(specs)} signals...")
    tasks = [generate_signal_text(client, spec, semaphore) for spec in specs]
    results = await asyncio.gather(*tasks)
    return list(zip(specs, results, strict=False))


async def generate_all(specs: list[dict[str, Any]]) -> tuple[list[dict], list[dict]]:
    from azure.identity import DefaultAzureCredential, get_bearer_token_provider
    from openai import AsyncAzureOpenAI

    credential = DefaultAzureCredential()
    token_provider = get_bearer_token_provider(credential, "https://cognitiveservices.azure.com/.default")
    client = AsyncAzureOpenAI(
        azure_endpoint="https://fbujaroski-fdebench-aoai.openai.azure.com/",
        azure_ad_token_provider=token_provider,
        api_version="2025-01-01-preview",
        max_retries=3,
        timeout=90,
    )
    print("  Using DefaultAzureCredential for auth")

    batch_size = 50
    batches = [specs[i:i + batch_size] for i in range(0, len(specs), batch_size)]
    total_batches = len(batches)

    signals: list[dict] = []
    gold: list[dict] = []
    failed = 0

    for batch_num, batch_specs in enumerate(batches, 1):
        results = await generate_batch(client, batch_specs, batch_num, total_batches)

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

        print(f"  Batch {batch_num} done. Total: {len(signals)} signals, {failed} failed")

    print(f"\nGenerated: {len(signals)}, Failed: {failed}")
    return signals, gold


# ── Validation ───────────────────────────────────────────────────────

def validate_format(signals: list[dict], gold: list[dict]) -> bool:
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

    return ok


def validate_with_scorer(gold: list[dict]) -> None:
    sys.path.insert(0, str(ROOT / "common" / "libs" / "fdebenchkit" / "src"))
    from ms.common.fdebenchkit.scorers.ticket_triage import score_submission

    result = score_submission(gold, gold)
    print("\nScorer validation (gold vs gold):")
    print(f"  Resolution: {result['resolution']}")
    print(f"  Dimensions: {result['dimension_scores']}")
    print(f"  Tickets: {result['tickets_scored']}, Errors: {result['tickets_errored']}")

    if result["resolution"] != 100.0:
        print(f"  [WARN] Expected 100.0, got {result['resolution']}")
    else:
        print("  ✓ Perfect score — format is valid")


# ── Main ─────────────────────────────────────────────────────────────

async def main() -> None:
    print("=== Synthetic Triage Dataset Generator v3 ===")
    print("=== Equal category distribution for macro-F1 ===\n")

    print("Step 1: Generating gold label specs...")
    specs = generate_all_specs(target=500, seed=43)

    cat_counts = Counter(s["category"] for s in specs)
    pri_counts = Counter(s["priority"] for s in specs)
    diff_counts = Counter(s["difficulty"] for s in specs)
    weakness_counts = Counter(s["weakness"] for s in specs)
    esc_count = sum(1 for s in specs if s["needs_escalation"])

    print(f"\n  Categories: {dict(sorted(cat_counts.items()))}")
    print(f"  Priorities: {dict(sorted(pri_counts.items()))}")
    print(f"  Difficulties: {dict(diff_counts)}")
    print(f"  Focus areas: {dict(sorted(weakness_counts.items()))}")
    print(f"  Escalations: {esc_count}/{len(specs)}")

    print("\nStep 2: Generating signal text via Azure OpenAI (batches of 50)...")
    signals, gold = await generate_all(specs)

    print("\nStep 3: Validating format...")
    format_ok = validate_format(signals, gold)
    if format_ok:
        print("  ✓ All format checks passed")

    print("\nStep 4: Saving...")
    with open(OUT_SIGNALS, "w") as f:
        json.dump(signals, f, indent=4)
    print(f"  Signals: {OUT_SIGNALS} ({len(signals)} items)")

    with open(OUT_GOLD, "w") as f:
        json.dump(gold, f, indent=4)
    print(f"  Gold:    {OUT_GOLD} ({len(gold)} items)")

    print("\nStep 5: Scorer validation...")
    validate_with_scorer(gold)

    final_cat = Counter(g["category"] for g in gold)
    final_pri = Counter(g["priority"] for g in gold)
    final_diff = Counter(g["difficulty"] for g in gold)

    print("\n=== FINAL SUMMARY ===")
    print(f"Total: {len(signals)}")
    print(f"\nCategory distribution:")
    for cat in sorted(final_cat.keys()):
        print(f"  {cat}: {final_cat[cat]}")
    print(f"\nPriority: {dict(sorted(final_pri.items()))}")
    print(f"Difficulty: {dict(final_diff)}")
    print("\n=== DONE ===")


if __name__ == "__main__":
    asyncio.run(main())
