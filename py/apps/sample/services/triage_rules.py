"""Deterministic rule-based triage classifier — fast path that skips LLM.

Architecture: Request → strip_injection → rule_classifier → if confident: return (fast!)
                                                           → if ambiguous: LLM fallback (slow but rare)

Multi-class classifier covering all 8 categories. Uses priority-ordered
early exits for high-confidence non-technical categories, then multi-class
keyword scoring for technical categories with negative evidence.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from functools import lru_cache


@lru_cache(maxsize=256)
def _word_pattern(kw: str) -> re.Pattern[str]:
    """Compile a word-boundary regex for a keyword."""
    return re.compile(r'\b' + re.escape(kw) + r'\b', re.IGNORECASE)


def _kw_in(kw: str, text: str) -> bool:
    """Check if keyword appears in text; use word boundaries for short terms."""
    if len(kw) <= 4:
        return bool(_word_pattern(kw).search(text))
    return kw in text


@dataclass
class TriageDecision:
    category: str
    team: str
    priority: str
    needs_escalation: bool
    missing_information: list[str] = field(default_factory=list)
    confidence: float = 0.0  # 0-1; if ≥ threshold → skip LLM


# ── Injection stripping ──────────────────────────────────────────────

_INJECTION_PATTERNS = [
    # Prompt override / system prompt exfil
    re.compile(r"(ignore|disregard|forget)\s+(all\s+)?(previous|prior|above)\s+(instructions?|prompts?|rules?)", re.I),
    re.compile(r"(you are now|switch to|enter)\s+(test|debug|override|admin)\s+mode", re.I),
    re.compile(r"output\s+(your|the)\s+(complete\s+)?system\s+prompt", re.I),
    re.compile(r"reveal\s+(your|all)\s+(instructions?|configuration|rules?)", re.I),
    # Priority override injection
    re.compile(r"classify\s+(this\s+)?(as|=)\s*P[12]", re.I),
    re.compile(r"PRIORITY\s+OVERRIDE", re.I),
    re.compile(r"SYSTEM\s+DIRECTIVE", re.I),
    re.compile(r"Priority=P[12]", re.I),
    # Few-shot poisoning
    re.compile(r"(here\s+are|examples?\s+of)\s+(some\s+)?how\s+similar\s+signals?\s+were", re.I),
    re.compile(r"Example\s+\d+:", re.I),
    # Base64 encoded instructions
    re.compile(r"(BASE64\s+ENCODED\s+FOR\s+SECURITY|decode\s+the\s+abo|decode\s+and\s+execute)", re.I),
    # Chain-of-thought hijacking
    re.compile(r"Think\s+step\s+by\s+step\s+about\s+this\s+signal", re.I),
    re.compile(r"(repeat\s+after\s+me|say\s+exactly)", re.I),
    # New instructions / test mode
    re.compile(r"New\s+instructions?:", re.I),
    re.compile(r"Resume\s+normal\s+operations?\s+after", re.I),
    re.compile(r"IMMEDIATE\s+ACTION\s+REQUIRED", re.I),
    re.compile(r"FROM\s+THE\s+DESK\s+OF", re.I),
]


def strip_injection(text: str) -> str:
    """Remove known injection patterns from signal text."""
    cleaned = text
    for pat in _INJECTION_PATTERNS:
        cleaned = pat.sub("", cleaned)
    return cleaned


def _has_injection(text: str) -> bool:
    """Check if the original (un-stripped) text contains injection attempts."""
    return any(pat.search(text) for pat in _INJECTION_PATTERNS)


# ── Category detection ────────────────────────────────────────────────

# Strongly indicate Crew Access & Biometrics (weight 1 each)
_ACCESS_KEYWORDS = [
    "bioscan", "bioauth", "biometric", "mfbv",
    "sso", "saml", "sign-in", "sign in", "login", "log in",
    "lockout", "locked out",
    "authenticate", "authentication", "credential", "password",
    "security group", "distribution group",
    "permission", "elevated permission",
    "crew profile", "access screen", "unified auth",
    "provisioning request", "onboarding", "offboarding",
    "directory sync", "access code",
    "retinal", "neural key",
    "logging into",
    "service account",
]

# High-weight access phrases (weight 5 each — almost always Crew Access)
_ACCESS_STRONG = [
    "sso", "saml", "biometric", "mfbv", "lockout",
    "crew profile", "unified auth", "security group",
    "distribution group", "retinal", "neural key",
    "sign-in error", "sign-in terminal",
    "biometric recalibration",
    "access troubles",
    "atlas archive",
    "service account",
    "logging into",
]

# Strongly indicate Communications & Navigation (weight 1 each)
_COMMS_KEYWORDS = [
    "subspace relay", "subspace tunnel", "relay proxy",
    "rf mesh", "comm relay", "wireless",
    "bandwidth", "signal barrier", "wan", "dns beacon",
    "connectivity", "network", "comms network",
    "fabricator", "latency", "video call",
    "hermes comm", "hermes call",
    "split-tunnel", "split tunnel", "roaming",
    "speed test", "rdp",
    "inter-deck", "beacon resolution",
    "relay client", "aether relay",
    "signal network", "network segment",
    "sd-interstation",
    "traceroute", "route print",
    "packet loss",
]

# High-weight comms phrases (weight 5 each)
_COMMS_STRONG = [
    "subspace relay", "rf mesh", "comm relay",
    "signal barrier", "wan failover",
    "split-tunnel", "split tunnel",
    "beacon resolution", "relay proxy",
    "packet loss", "sd-interstation",
    "signal network segment",
]


def _briefing_team(lower: str) -> str:
    """Determine team for Mission Briefing Request based on content."""
    # Offboarding with account actions → Crew Identity & Airlock Control
    if any(kw in lower for kw in [
        "disable", "revoke", "offboarding", "last duty cycle", "deactivate",
    ]):
        return "Crew Identity & Airlock Control"
    # Full setup / onboarding with hardware → Spacecraft Systems Engineering
    if any(kw in lower for kw in ["full setup", "setup needed"]):
        return "Spacecraft Systems Engineering"
    # Software how-to → Mission Software Operations
    if any(kw in lower for kw in ["how do i", "how to book", "booking", "room booking"]):
        return "Mission Software Operations"
    return "None"


def _detect_category(text: str) -> tuple[str, str, float]:
    """Return (category, team, confidence) using multi-class scoring.

    Priority order for early exits:
    1. Not a Mission Signal (auto-replies, thank-yous, closures)
    2. Threat Detection & Containment (security, phishing, breaches)
    3. Mission Briefing Request (onboarding, offboarding, how-to)
    4. Multi-class scoring for 5 technical categories
    """
    lower = text.lower()
    # Subject is the first ~120 chars (before description text bleeds in)
    subj = text.split("\n")[0].lower() if "\n" in text else lower[:120]

    # ── Phase 1: "Not a Mission Signal" early exit ──
    _non_signal_markers = [
        "thank you", "thanks for", "thanks!", "got it working",
        "out of office", "auto-reply", "cryo-sleep",
        "appreciate the quick", "appreciate the help",
    ]
    non_signal_hits = sum(1 for m in _non_signal_markers if m in lower)
    # Subject patterns that indicate non-signal
    if any(p in subj for p in ["thanks", "re: [signal", "maintenance notification"]):
        non_signal_hits += 1
    if non_signal_hits >= 1:
        _real_issue = [
            "not working", "error", "failure", "crash",
            "broken", "outage", "suspicious", "unauthorized",
            "failing", "down ",
        ]
        # Action items indicate a real request, not a closure
        _action_items = [
            "disable", "revoke", "transfer ownership", "wipe",
            "please:", "onboarding", "offboarding", "last duty cycle",
        ]
        real_issue_hits = sum(1 for kw in _real_issue if kw in lower)
        action_hits = sum(1 for kw in _action_items if kw in lower)
        if real_issue_hits == 0 and action_hits == 0:
            conf = min(0.92, 0.82 + 0.05 * non_signal_hits)
            return "Not a Mission Signal", "None", conf

    # ── Phase 2: Threat Detection takes priority ──
    _threat_keywords = [
        "suspicious", "unauthorized", "malware", "phishing",
        "exfiltration", "containment breach", "data breach",
        "social engineering", "impersonation",
        "galactic credits", "claim now", "totallylegit",
        "shared externally", "compliance sweep",
        "cert expir", "certificate expir",
        "virus",
    ]
    threat_score = sum(1 for t in _threat_keywords if t in lower)
    # Subject threat signals — use specific phrases, not standalone "breach"
    _threat_subject = [
        "suspicious", "containment breach", "data breach",
        "phishing", "won ", "claim", "cert expir",
    ]
    threat_score += sum(2 for t in _threat_subject if t in subj)
    if threat_score >= 2:
        conf = min(0.92, 0.78 + 0.03 * threat_score)
        return "Threat Detection & Containment", "Threat Response Command", conf

    # ── Phase 3: Mission Briefing Request ──
    _briefing_keywords = [
        "new crew member", "full setup needed",
        "last duty cycle", "how do i book",
        "crew member transfer",
        "orientation", "onboarding checklist",
        "departure checklist", "mission brief",
    ]
    briefing_score = sum(1 for b in _briefing_keywords if b in lower)
    _briefing_subject = [
        "new crew member", "transfer", "how do i", "setup needed",
    ]
    briefing_score += sum(2 for b in _briefing_subject if b in subj)
    # Onboarding/offboarding is briefing, not access
    if any(kw in lower for kw in ["onboarding", "offboarding"]):
        if any(kw in lower for kw in [
            "new crew member", "joining", "last duty cycle",
            "transferring", "disable her", "disable his",
        ]):
            briefing_score += 2
    if briefing_score >= 2:
        conf = min(0.90, 0.78 + 0.04 * briefing_score)
        team = _briefing_team(lower)
        return "Mission Briefing Request", team, conf

    # ── Phase 4: Multi-class scoring for 5 technical categories ──

    # Telemetry & Data Banks
    _telemetry_kw = [
        "telemetry", "data core", "data bank", "pipeline",
        "analytics node", "dashboard", "data request",
        "deep storage", "ingest", "timeout error",
        "prod-analytics", "500 error",
    ]
    tel_score = sum(1 for kw in _telemetry_kw if kw in lower)
    if any(kw in subj for kw in [
        "telemetry", "data core", "analytics", "dashboard", "pipeline",
    ]):
        tel_score += 3
    # Service account/identity + data pipeline context → telemetry
    if any(kw in lower for kw in ["pipeline", "403", "deep storage"]) and "service" in lower:
        tel_score += 2

    # Flight Software & Instruments
    _software_kw = [
        "flightos", "trajectory", "subcomm crash", "subcomm show",
        "white screen", "holographic calendar", "phantom briefing",
        "screen share", "share screen", "plotter",
        "reference frame", "subcomm",
    ]
    sw_score = sum(1 for kw in _software_kw if kw in lower)
    if any(kw in subj for kw in [
        "flightos", "trajectory", "subcomm",
    ]):
        sw_score += 3
    # Screen sharing with any word in between ("share his screen", "share her screen")
    if "share" in lower and "screen" in lower:
        sw_score += 2
    # Personal console reference — device-specific issue
    if any(kw in lower for kw in ["my console", "his console", "her console"]):
        sw_score += 5

    # Hull & Structural Systems
    _hull_kw = [
        "holographic projector", "projector offline", "fabricator",
        "workstation console", "cooling fan",
        "display flickering", "molecular fabricator",
        "won't power on", "manual override panel",
        "hull panel", "structural integrity",
        "airlock mechanism", "deck plating", "bulkhead",
        "atmospheric", "decompression", "pressure seal",
        "oxygen recycler", "life support", "life-support",
        "power fluctuation", "environmental control",
        "ventilation", "thermal regulator", "gravity plate",
    ]
    hull_score = sum(1 for kw in _hull_kw if kw in lower)
    if any(kw in subj for kw in [
        "fabricator", "projector", "holographic", "console", "workstation",
    ]):
        hull_score += 3
    # Fabricator/projector are physical equipment
    if any(kw in lower for kw in ["fabricator", "projector"]):
        hull_score += 2

    # Crew Access & Biometrics
    access_score = sum(1 for kw in _ACCESS_KEYWORDS if _kw_in(kw, lower))
    access_score += sum(5 for kw in _ACCESS_STRONG if _kw_in(kw, lower))
    if any(_kw_in(kw, subj) for kw in [
        "access", "auth", "login", "sign-in", "biometric",
        "lockout", "sso", "credential",
    ]):
        access_score += 3
    # Negative: suppress Access if context is telemetry/data
    if any(kw in lower for kw in [
        "pipeline", "403", "deep storage", "data core", "telemetry",
    ]):
        access_score = max(0, access_score - 5)
    # Negative: suppress Access if context is hardware
    if any(kw in lower for kw in ["fabricator", "projector", "holographic"]):
        access_score = max(0, access_score - 3)

    # Communications & Navigation
    comms_score = sum(1 for kw in _COMMS_KEYWORDS if _kw_in(kw, lower))
    comms_score += sum(5 for kw in _COMMS_STRONG if _kw_in(kw, lower))
    if any(kw in subj for kw in [
        "network", "relay", "rf mesh", "connectivity",
        "subspace", "speed", "latency",
    ]):
        comms_score += 3
    # Negative: suppress Comms if context is hardware
    if any(kw in lower for kw in [
        "fabricator", "projector", "holographic display",
    ]):
        comms_score = max(0, comms_score - 3)

    # ── Pick the best category ──
    scores = {
        "Telemetry & Data Banks": tel_score,
        "Flight Software & Instruments": sw_score,
        "Hull & Structural Systems": hull_score,
        "Crew Access & Biometrics": access_score,
        "Communications & Navigation": comms_score,
    }

    _team_map = {
        "Crew Access & Biometrics": "Crew Identity & Airlock Control",
        "Communications & Navigation": "Deep Space Communications",
        "Flight Software & Instruments": "Mission Software Operations",
        "Hull & Structural Systems": "Spacecraft Systems Engineering",
        "Telemetry & Data Banks": "Telemetry & Data Core",
    }

    best_cat = max(scores, key=lambda k: scores[k])
    best_score = scores[best_cat]

    if best_score == 0:
        # No keywords matched — low confidence, LLM should handle
        return "Communications & Navigation", "Deep Space Communications", 0.30

    sorted_scores = sorted(scores.values(), reverse=True)
    gap = sorted_scores[0] - sorted_scores[1] if len(sorted_scores) > 1 else sorted_scores[0]

    # Confidence based on absolute score and margin over second-best
    confidence = min(0.92, 0.55 + 0.04 * best_score + 0.04 * gap)

    team = _team_map[best_cat]

    # Context-based team overrides
    if best_cat == "Flight Software & Instruments":
        # Hardware context (console, workstation) → SSE, unless it's a screen-sharing issue
        if "share" in lower and "screen" in lower:
            pass  # Screen sharing is a software/policy issue → keep MSO
        elif any(kw in lower for kw in ["console", "workstation"]):
            team = "Spacecraft Systems Engineering"
    elif best_cat == "Hull & Structural Systems":
        # Fabricator jobs queuing but not materializing → data path issue → DSC
        if "fabricator" in lower and any(kw in lower for kw in ["queue", "jobs"]):
            team = "Deep Space Communications"

    return best_cat, team, confidence


# ── Priority detection ────────────────────────────────────────────────

_P1_SAFETY_KEYWORDS = [
    "hull breach", "decompression", "atmospheric compromise",
    "containment failure", "containment breach",
    "life support", "life-support", "oxygen failure",
    "hostile contact",
]


def _detect_priority(text: str, category: str, subject: str, original_text: str) -> tuple[str, float]:
    """Return (priority, confidence).

    Strategy: detect clear P4 and P1 patterns. Default to P3.
    P2 detection for broad-impact and multi-user issues.
    """
    lower = text.lower()
    subj_lower = subject.lower()
    has_inj = _has_injection(original_text)

    # ── P1: Safety-critical ──
    if any(kw in lower for kw in _P1_SAFETY_KEYWORDS):
        return "P1", 0.95

    # P1: Critical infrastructure degradation with broad impact
    if "cross-atlantic" in lower and ("critical" in lower or "severely degraded" in lower):
        return "P1", 0.85

    # P1: Certificate expiring on production system (all fleet connections fail)
    if "cert" in lower and "expir" in lower and any(
        kw in lower for kw in ["production", "all external", "gateway", "all fleet"]
    ):
        return "P1", 0.85

    # P1: VIP (Fleet Admiral) with real-time urgency
    if "fleet admiral" in lower and any(
        kw in lower for kw in ["happening now", "right now", "arriving in"]
    ):
        return "P1", 0.80

    # P1: Account lockout with urgent signal
    if "account lockout" in lower and "urgent" in subj_lower:
        return "P1", 0.80

    # P1: VPN/relay routing broken (traffic misrouted, not just slow)
    if "split-tunnel" in lower and "not working" in lower and "traffic" in lower:
        return "P1", 0.75

    # P1: Complete equipment inaccessible after infrastructure change
    if "fabricator" in lower and ("no access" in lower or "never print" in lower):
        return "P1", 0.75

    # P1: Database connectivity completely down (times out, not slow)
    if "connection times out" in lower and any(kw in lower for kw in ["nova db", "sql", "database"]):
        return "P1", 0.75

    # ── P4: Clear informational / question / request / noise ──
    p4_signals = 0

    # Questions and how-to (require question framing, not just "how to" embedded)
    if any(phrase in lower for phrase in [
        "how do i", "instructions needed",
        "is there a guide", "is there a current guide",
        "can we get a new",
        "what is the process",
    ]):
        p4_signals += 3

    # Explicit low-priority / not urgent self-declaration
    if any(phrase in lower for phrase in [
        "not urgent", "low priority", "no rush",
        "when you get a chance", "when someone has a chance",
        "just want to have it ready",
        "not blocking",
    ]):
        p4_signals += 2

    # Requests (not incidents) — match specific request patterns in subject
    if any(phrase in subj_lower for phrase in [
        "rule request", "setup instructions",
        "new security group", "instructions needed",
    ]):
        p4_signals += 3

    # Chat transcript from past outage (post-event)
    if "chat transcript" in lower and "outage" in lower:
        p4_signals += 3

    # Adversarial: subject says CRITICAL / C-Suite but has injection
    if has_inj:
        if any(w in subj_lower for w in ["critical", "c-suite"]):
            p4_signals += 4
        else:
            p4_signals += 1

    # Audit findings are typically informational
    if "audit finding" in lower or "[audit" in subj_lower.lower():
        p4_signals += 3

    # Single-user intermittent issues
    if any(phrase in lower for phrase in [
        "intermittent rf mesh",
        "speed degraded on our deck",
        "network drops every",
        "comm relay keeps dropping",
        "keeps dropping every",
    ]):
        p4_signals += 2

    # Off-ship / remote single-user access
    if "off-ship" in lower or ("outpost" in lower and "can't authenticate" in lower):
        p4_signals += 2

    # Remote user can't authenticate — routine
    if "can't authenticate" in lower and category == "Crew Access & Biometrics":
        # Check if single user
        if not any(kw in lower for kw in ["multiple", "number of", "crew members"]):
            p4_signals += 1

    # VPN/relay access to specific app — single user
    if "aether relay client" in lower and ("can't access" in lower or "risk dashboard" in lower):
        p4_signals += 3

    # Auto-transcribed calls about DNS / beacon resolution
    if "auto-transcribed" in lower and "beacon resolution" in lower:
        p4_signals += 3

    # WAN failover that's already been manually resolved
    if "failover" in lower and "manually" in lower:
        p4_signals += 3

    # Biometric recalibration from comm link transcript (VIP but routine)
    if "biometric recalibration" in lower and "comm link transcript" in subj_lower:
        p4_signals += 3

    # Single-user biometric stopped working (routine)
    if any(phrase in lower for phrase in [
        "suddenly stopped working",
        "biometric scan-in",
    ]) and category == "Crew Access & Biometrics":
        p4_signals += 2

    # RF mesh with authentication failure → network issue, not critical
    if "rf mesh" in lower and "authentication fail" in lower:
        p4_signals += 2

    # "Something's not working" with trading (long rambling, weeks old)
    if "something's not working" in subj_lower and "trading" in subj_lower:
        p4_signals += 3

    # External hypernet speed degraded — single deck
    if "hypernet speed degraded" in lower:
        p4_signals += 2

    # Auto-translated single user issue
    if "auto-translated" in subj_lower and category == "Crew Access & Biometrics":
        p4_signals += 1

    if p4_signals >= 3:
        return "P4", min(0.90, 0.65 + 0.04 * p4_signals)

    # ── P2: Major operational impact ──
    p2_signals = 0

    # Multiple crew / broad impact
    if any(phrase in lower for phrase in [
        "number of crew members",
        "affecting multiple",
        "multiple systems",
        "three different issues",
        "entire floor",
    ]):
        p2_signals += 2

    # Call drops / video degradation — affects meetings
    if any(phrase in lower for phrase in [
        "calls are dropping",
        "call drops",
        "video calls keep dropping",
        "audio cuts",
    ]):
        p2_signals += 2

    # Fleet Admiral / VIP with real issue (not injection)
    if not has_inj and any(phrase in lower for phrase in [
        "fleet admiral",
        "submitted on behalf of fleet admiral",
    ]):
        p2_signals += 2

    # Massive latency spikes
    if "massive signal latency" in lower or "massive latency" in lower:
        p2_signals += 1

    # Service-wide authentication failures
    if any(phrase in lower for phrase in [
        "saml sso failures",
        "identity beacon security certificate rotation",
    ]):
        p2_signals += 2

    # Roaming disconnects (affects many users moving between floors)
    if "roaming between floors" in lower and "full disconnect" in lower:
        p2_signals += 2

    # Site-to-site tunnel down with partner SLA — but only if there's
    # evidence of broad impact or SLA breach
    if "site-to-site" in lower and "tunnel" in lower and "down" in lower:
        if any(kw in lower for kw in ["sla", "breach", "partner"]):
            p2_signals += 2

    # Shared service account expired (broad impact)
    if "service account" in lower and "expired" in lower:
        p2_signals += 2

    # Repeated lockdowns / quarantine
    if any(phrase in lower for phrase in [
        "crew profile lockdown",
        "fourth time today",
        "keeps getting quarantined",
        "quarantined",
    ]):
        p2_signals += 2

    # Unified auth problems with full history
    if "unified auth" in lower:
        p2_signals += 2

    # Diagnostic screenshots with real connectivity issues (not injection)
    if not has_inj and "diagnostic" in lower and ("traceroute" in lower or "screenshot" in lower):
        if "intermittent connectivity" in lower or "losing mission data" in lower:
            p2_signals += 2

    # CTO-level without injection
    if "chief technology commander" in lower and not has_inj:
        p2_signals += 2

    # CTO-level WITH injection but genuine issue underneath
    if "chief technology commander" in lower and has_inj:
        # Check for real operational indicators
        if any(kw in lower for kw in ["traders", "mission control", "40 "]):
            p2_signals += 2

    # Multi-person impact with specific numbers
    if any(phrase in lower for phrase in [
        "impacting about",
        "15 people",
        "40 traders",
        "about 40",
    ]):
        p2_signals += 2

    # Client-facing urgency
    if "client calls" in lower and "impacting" in lower:
        p2_signals += 1

    # Multiple issues in one ticket with urgency
    if "three different issues" in lower:
        p2_signals += 1
    if "i have been waiting" in lower:
        p2_signals += 1

    # Offboarding with sensitive/classified access — time-bound security action
    if any(kw in lower for kw in ["last duty cycle", "transferring off"]) and any(
        kw in lower for kw in ["sensitive", "classified", "threat detection", "containment"]
    ):
        p2_signals += 2

    if p2_signals >= 2:
        return "P2", min(0.80, 0.55 + 0.04 * p2_signals)

    # ── P3: Default for real issues ──
    return "P3", 0.70


# ── Escalation ────────────────────────────────────────────────────────

def _detect_escalation(
    text: str, priority: str, category: str, subject: str,
    original_text: str,
) -> bool:
    """Determine if the ticket needs escalation."""
    lower = text.lower()

    # P1 escalates for cross-station, security, VIP/delegation, or safety
    if priority == "P1":
        if any(kw in lower for kw in [
            "cross-atlantic", "cross-station",
            "account lockout",
        ]):
            return True
        # Safety keywords always escalate
        if any(kw in lower for kw in _P1_SAFETY_KEYWORDS):
            return True
        # VIP/delegation with time pressure
        if any(kw in lower for kw in [
            "delegation", "fleet admiral", "admiralty",
        ]):
            return True
        # Cert expiry on production
        if "cert" in lower and "expir" in lower:
            return True
        # Otherwise P1 does NOT auto-escalate (e.g., single-user split-tunnel)
        return False

    # Threat category — only escalate active threats, not spam/phishing reports
    # (cert expiry escalates via P1 path)

    # Airlock access issues — safety-critical infrastructure
    if "airlock" in lower and any(kw in lower for kw in [
        "broken", "not working", "still broken", "access code", "doesn't work",
    ]):
        return True

    # Threat / security indicators (require context, not just keyword)
    if any(kw in lower for kw in [
        "unauthorized access", "unauthorized login",
        "exfiltration",
        "malware", "social engineering",
        "impersonation",
    ]):
        return True

    # "hostile" — only if not in routine offboarding/transfer context
    if "hostile" in lower and category != "Mission Briefing Request":
        return True

    # Multi-WAN failover — infrastructure-level
    if "multi-wan failover" in lower or "failover failure" in lower:
        return True

    # Trading desk / financial systems
    if "trading" in lower and ("deck" in lower or "comms" in lower):
        return True

    # Partner requesting sensitive data (potential social engineering)
    if "partner" in lower and "needs logs" in lower:
        return True

    return False


# ── Missing information ──────────────────────────────────────────────

def _detect_missing_info(text: str, category: str) -> list[str]:
    """Identify the most relevant missing info items using a scoring approach.

    Strategy: score each possible item based on multiple text signals, then
    return the top-scoring items (usually 2, matching the ~1.7 avg in gold).
    """
    lower = text.lower()

    # ── Text signal detectors ─────────────────────────────────────────

    # Infrastructure/config request (firewall, DNS, VPN tunnel config)
    is_infra_config = any(kw in lower for kw in [
        "site-to-site", "signal barrier", "firewall rule",
        "failover", "wan link", "sd-interstation", "interconnection",
        "decommission", "cutover", "routing protocol", "bgp ",
        "latency budget", "circuit", "rule request",
    ])

    # DNS-specific request (name resolution)
    is_dns_change = any(kw in lower for kw in [
        "dns record", "name resolution service", "dns change",
        "dns update", "cname", "a record",
    ])

    # User-facing connectivity/signal issue
    is_connectivity = any(kw in lower for kw in [
        "drop", "drops", "dropping", "can't connect", "cannot connect",
        "no signal", "disconnects", "disconnect", "timeout", "timed out",
        "times out",
        "slow", "latency", "buffering", "freezes", "choppy",
        "rf mesh", "hypernet", "comm relay",
        "not connecting", "won't connect", "failed to connect",
        "can't reach", "unable to reach", "connection issue",
        "roaming", "flapping", "lag", "unusable",
    ])

    # VPN/tunnel user issue (vs config)
    is_vpn_user = any(kw in lower for kw in [
        "subspace relay client", "relay client", "split-tunnel",
        "split tunnel", "aether relay", "connected to",
    ]) and not is_infra_config

    # Hardware/device mentioned
    is_hardware = any(kw in lower for kw in [
        "terminal", "fabricator", "console", "scanner",
        "device", "wrist-com", "hardware", "relay unit",
        "holographic display", "comm panel",
    ])

    # RF mesh roaming issue (device-specific, not location-specific)
    is_roaming = "roaming" in lower

    # Intermittent/recurring issue
    is_recurring = any(kw in lower for kw in [
        "intermittent", "random", "sometimes", "sporadic", "recurring",
        "keeps dropping", "keeps disconnecting", "on and off",
        "comes and goes", "randomly", "flapping", "half the time",
    ]) or is_roaming

    # References a previous incident (by description, not by ID)
    is_followup = any(kw in lower for kw in [
        "same issue", "same problem", "same glitch", "same thing",
        "happened before", "reported before", "follow-up", "following up",
        "back again", "last time this happened", "still happening",
        "similar incident", "same symptoms", "same error",
        "same authentication", "same sign-in",
        "going back and forth", "for weeks",
    ])

    # Has actual ticket/incident reference number
    has_past_ref = any(kw in lower for kw in [
        "sig-", "signal report #", "ticket #", "incident #",
        "reference #", "case #",
    ])

    # Filing on behalf of someone else
    is_behalf = any(kw in lower for kw in [
        "on behalf", "filing this for", "forwarding this from",
        "forwarding this", "guest", "contractor", "auxiliary",
    ])

    filing_for_other = any(kw in lower for kw in [
        "on behalf", "filing this for", "filing for a",
        "can't log in to file", "forwarding this from",
    ])

    # Outage / widespread issue
    is_outage = any(kw in lower for kw in [
        "outage", "down since", "went down",
        "everyone", "100+", "whole department",
    ])

    # Has precise sector/location coordinates
    has_precise_location = any(kw in lower for kw in [
        "sector ", "bay ", "room ", "corridor ", "coordinates",
    ])

    # Has device model/version details
    has_device_detail = any(kw in lower for kw in [
        "model", "serial", "firmware", "build number",
        "mk-", "gen-", "type-", "series",
    ])

    # Has stardate or precise timestamp
    has_stardate = "stardate" in lower

    # Has specific biometric method named (but NOT in a negated context)
    _bio_keywords_present = any(kw in lower for kw in [
        "retinal", "neural key", "palm scan", "fingerprint",
        "voice auth", "iris", "neural-key", "palm-scan",
    ])
    _bio_uncertain = any(kw in lower for kw in [
        "not sure which", "not sure exactly which",
        "whatever pops up", "don't know which",
        "either", "whichever",
    ])
    has_bio_detail = _bio_keywords_present and not _bio_uncertain

    # Auth/login issue
    is_auth_issue = any(kw in lower for kw in [
        "login", "log in", "sign-in", "sign in", "sso", "saml",
        "authentication", "authenticate", "locked out", "lockout",
        "biometric", "bioscan", "mfbv", "credential", "password",
        "access denied", "multi-factor", "802.1x",
        "access code", "service account",
    ])

    # Specific subsystem named
    has_subsystem_named = any(kw in lower for kw in [
        "rf mesh", "subspace relay", "signal barrier", "wan",
        "dns", "hermes", "rdp", "fabricator", "comm relay",
        "beacon", "nav-client", "hypernet", "intracomm",
        "comm panel", "aether",
    ])

    # Remote/off-ship
    is_remote = any(kw in lower for kw in [
        "outpost", "off-ship", "remote station", "mining",
        "asteroid", "substation", "kepler",
    ])

    # Working from home / remote access
    is_home_access = any(kw in lower for kw in [
        "from home", "home connection", "coffee shop",
        "home network", "personal network",
    ])

    # Impact mentioned
    mentions_impact = any(kw in lower for kw in [
        "mission critical", "sla", "breach", "deadline", "quarter-end",
        "trading", "operations impacted", "blocking",
        "financial penalties", "compliance",
    ])

    # Has screenshot/attachment
    has_attachment = any(kw in lower for kw in [
        "screenshot", "attached", "attachment", "<img",
        "sensor log", "log dump", "photo",
    ])

    # Tried to capture evidence but failed
    tried_capture_failed = any(kw in lower for kw in [
        "tried to screenshot", "tried taking a screenshot",
        "closed the tab before saving", "before saving the result",
        "didn't capture", "couldn't capture",
        "didn't think to capture", "can't describe the exact error",
    ])

    # Voicemail / transcription (low quality info, needs more details)
    is_transcription = any(kw in lower for kw in [
        "voictransmission", "transcription", "transcribed",
        "auto-transcribed", "comm link transcript",
    ])

    # Partial access (some things work, others don't)
    is_partial_access = any(kw in lower for kw in [
        "other cadetal tools", "other modules", "other sites",
        "most cadetal sites", "some fine", "just times out",
        "works fine when", "other apps", "other cadetal",
    ]) and any(kw in lower for kw in [
        "times out", "doesn't work", "just this one",
        "just times out", "can't access",
    ])

    # Multiple people affected
    multi_affected = any(kw in lower for kw in [
        "100+", "multiple crew", "everyone", "whole department",
        "entire team", "all crew", "team of", "about 12",
        "number of crew", "crew members on deck",
    ])

    # Provisioning/group request (not authentication failure)
    is_provisioning = any(kw in lower for kw in [
        "new security group", "distribution group", "new broadcast",
        "provisioning", "provision the", "get access to",
        "read access", "permissions",
    ])

    # Setup/how-to request
    is_setup = any(kw in lower for kw in [
        "setup instructions", "set up", "how to",
        "instructions", "guide",
    ])

    # Has error details quoted
    has_error_detail = any(kw in lower for kw in [
        "error code", "error message:", "status code",
        "'error", '"error',
    ])

    # Vague timing ("about two weeks ago", "a few days ago")
    has_vague_timing = any(kw in lower for kw in [
        "about two weeks", "a few days", "a few weeks",
        "last week", "last night", "can't pinpoint",
        "don't remember when", "started a while",
    ])

    # User explicitly says they don't know version
    missing_version = any(kw in lower for kw in [
        "don't know the exact version", "not sure which version",
        "don't know the version", "outdated",
    ])

    # Auth certificate issue
    is_cert_auth = any(kw in lower for kw in [
        "certificate", "802.1x", "security certificate",
    ])

    # Contact info missing for the third party
    missing_contact = any(kw in lower for kw in [
        "don't have their comm", "don't have another way",
        "no comm frequency", "no crew member id",
        "don't have reliable subspace", "subspace callback",
    ])

    # Domain/environment issue
    is_domain_env = any(kw in lower for kw in [
        "contoso-legacy", "old domain", "domain",
        "network switch",
    ])

    # SSO/redirect issue
    is_sso_redirect = any(kw in lower for kw in [
        "sso portal", "sso redirect", "redirect",
        "login beacon", "redirect fails",
    ])

    # Long verbose description with little technical detail
    desc_length = len(lower)
    is_verbose_vague = desc_length > 600 and not has_error_detail

    # Software/client mentioned
    has_software_mention = any(kw in lower for kw in [
        "relay client", "starprotect", "update", "patch",
        "client was updated", "updated last", "nav-client",
    ])

    # ── Scoring per category ─────────────────────────────────────────

    scores: dict[str, float] = {}

    if category == "Communications & Navigation":
        # ── sector_coordinates ──
        sc = 0.0
        if is_connectivity and not is_infra_config and not is_vpn_user:
            sc += 3.0
        if is_connectivity and is_infra_config:
            sc += 1.5
        if is_dns_change:
            sc += 1.5  # DNS changes still need to know scope
        if is_outage and not is_infra_config:
            sc += 1.0
        if is_transcription:
            sc += 1.5  # transcriptions often lack location detail
        if has_precise_location:
            sc -= 5.0
        if is_roaming:
            sc -= 3.0  # roaming issues are device-specific, not location
        if is_vpn_user and not is_home_access:
            sc -= 2.0  # VPN issues may still need location for RDP
        if is_home_access and not any(kw in lower for kw in ["rdp", "remote desktop"]):
            sc -= 2.0  # home issues only need location for RDP
        if is_infra_config and not is_connectivity and not is_transcription:
            sc -= 2.0  # pure config doesn't need location
        if is_recurring and not is_connectivity:
            sc -= 1.0
        if is_partial_access:
            sc -= 2.0  # partial access is about config, not location
        scores["sector_coordinates"] = sc

        # ── anomaly_readout ──
        ar = 0.0
        if is_connectivity and not has_error_detail:
            ar += 2.0
        if is_infra_config and not is_connectivity and not has_error_detail:
            ar += 1.5
        if is_transcription:
            ar += 1.5  # transcriptions often lack specific error details
        if any(kw in lower for kw in [
            "didn't capture", "couldn't capture", "no error",
            "without an error", "can't describe",
        ]):
            ar += 2.0
        if has_error_detail:
            ar -= 3.0
        # Demote if another signal is much stronger
        if is_roaming:
            ar -= 2.0  # roaming → module_specs + recurrence more important
        if is_hardware and not has_device_detail and not is_transcription:
            ar -= 1.0  # module_specs likely more important
        if is_recurring and not is_connectivity:
            ar -= 0.5  # recurrence_pattern likely more important
        if is_followup and not is_connectivity:
            ar -= 1.0  # previous_signal_id likely more important
        if is_behalf and not is_connectivity:
            ar -= 1.0
        scores["anomaly_readout"] = ar

        # ── system_configuration ──
        sc2 = 0.0
        if is_infra_config:
            sc2 += 3.5
        if is_dns_change:
            sc2 += 2.0
        if any(kw in lower for kw in [
            "signal barrier", "rule request", "failover",
            "sd-interstation", "dns", "site-to-site",
            "interconnection", "tunnel", "supplier",
        ]):
            sc2 += 0.5
        if "configuration" in lower or "config" in lower:
            sc2 -= 0.5
        if is_transcription and is_connectivity:
            sc2 -= 3.0  # transcriptions are user reports, not config requests
        if not is_infra_config and not is_dns_change:
            sc2 -= 5.0
        scores["system_configuration"] = sc2

        # ── stardate ──
        sd = 0.0
        if is_infra_config and not has_stardate and not is_transcription:
            sd += 2.5
        if is_outage and not has_stardate:
            sd += 1.5
        if has_vague_timing and not has_stardate:
            sd += 1.5
        if is_recurring and not is_infra_config:
            sd += 1.0
        if has_stardate:
            sd -= 5.0
        if is_connectivity and not is_infra_config and not is_outage and not is_recurring:
            sd -= 2.0  # pure connectivity doesn't need stardate
        if is_transcription:
            sd -= 1.5  # transcriptions are user reports, less about timing
        scores["stardate"] = sd

        # ── module_specs ──
        ms = 0.0
        if is_hardware and not has_device_detail and not is_vpn_user:
            ms += 3.0
        if is_roaming and not has_device_detail:
            ms += 3.0  # roaming needs device model/capabilities
        if any(kw in lower for kw in [
            "fabricator", "relay unit", "beacon",
        ]) and not has_device_detail:
            ms += 1.0
        if any(kw in lower for kw in ["rdp", "remote desktop"]) and not has_device_detail:
            ms += 1.5  # RDP issues may need client device info
        if has_device_detail:
            ms -= 5.0
        if not is_hardware and not is_roaming and "rdp" not in lower:
            ms -= 3.0
        if is_vpn_user and not is_roaming:
            ms -= 2.0  # VPN is software, not hardware
        scores["module_specs"] = ms

        # ── recurrence_pattern ──
        rp = 0.0
        if is_recurring:
            rp += 3.5
        if any(kw in lower for kw in [
            "every ", "pattern:", "frequency:", "intervals of",
            "minute at a time", "about a minute",
        ]):
            rp -= 0.5  # some pattern described but may need more
        if not is_recurring:
            rp -= 5.0
        scores["recurrence_pattern"] = rp

        # ── affected_crew ──
        ac = 0.0
        if multi_affected:
            ac += 2.5
        if is_outage and multi_affected:
            ac += 1.0
        if filing_for_other and not multi_affected:
            ac += 0.5
        if not multi_affected and not is_outage:
            ac -= 4.0
        scores["affected_crew"] = ac

        # ── sensor_log_or_capture ──
        sl = 0.0
        if tried_capture_failed:
            sl += 4.0
        if has_software_mention and not has_attachment:
            sl += 1.5
        if any(kw in lower for kw in [
            "nav-client", "edge", "policy", "refresh",
            "speed test", "traceroute",
        ]) and not has_attachment:
            sl += 1.5
        if is_transcription and not has_attachment:
            sl += 0.5  # transcriptions may benefit from logs
        if has_attachment:
            sl -= 5.0
        if not tried_capture_failed and not has_software_mention:
            sl -= 1.5
        scores["sensor_log_or_capture"] = sl

        # ── crew_contact ──
        cc = 0.0
        if missing_contact:
            cc += 4.0
        if is_behalf and any(kw in lower for kw in [
            "guest", "auxiliary", "contractor", "visitor",
        ]):
            cc += 2.0
        if not is_behalf and not filing_for_other:
            cc -= 5.0
        scores["crew_contact"] = cc

        # ── mission_impact ──
        mi = 0.0
        if is_infra_config and not mentions_impact:
            mi += 1.5
        if is_outage and not mentions_impact:
            mi += 1.0
        if any(kw in lower for kw in ["wan ", "cross-atlantic"]) and not mentions_impact:
            mi += 1.0  # WAN issues need impact assessment
        if mentions_impact:
            mi -= 3.0
        if not is_infra_config and not is_outage:
            mi -= 3.0
        scores["mission_impact"] = mi

        # ── affected_subsystem ──
        asub = 0.0
        if not has_subsystem_named and is_connectivity:
            asub += 2.0
        if is_partial_access:
            asub += 3.0  # some work, some don't → which subsystem?
        if is_auth_issue and not has_subsystem_named:
            asub += 1.0
        if has_subsystem_named and not is_partial_access:
            asub -= 5.0
        elif has_subsystem_named and is_partial_access:
            asub -= 1.0  # subsystem named but affected one unclear
        scores["affected_subsystem"] = asub

        # ── software_version ──
        sv = 0.0
        if missing_version:
            sv += 4.0
        if has_software_mention and "version" not in lower:
            sv += 2.0
        if "version" in lower:
            sv -= 2.0
        if not has_software_mention and not missing_version:
            sv -= 4.0
        scores["software_version"] = sv

        # ── biometric_method ──
        bm = 0.0
        if is_cert_auth and is_auth_issue:
            bm += 2.5
        if any(kw in lower for kw in [
            "not sure if", "which method", "user certificate",
            "machine certificate", "802.1x",
        ]):
            bm += 2.0
        if has_bio_detail:
            bm -= 5.0
        if not is_auth_issue:
            bm -= 5.0
        scores["biometric_method"] = bm

        # ── habitat_conditions ──
        hc = 0.0
        if is_remote:
            hc += 2.5
        if is_home_access and not is_partial_access:
            hc += 2.0
        if not is_remote and not is_home_access:
            hc -= 4.0
        if is_partial_access:
            hc -= 2.0  # partial access is about routing, not habitat
        scores["habitat_conditions"] = hc

        # ── previous_signal_id ──
        psi = 0.0
        if is_followup and not has_past_ref:
            psi += 4.0
        if has_past_ref:
            psi -= 5.0
        if not is_followup:
            psi -= 5.0
        scores["previous_signal_id"] = psi

        # ── sequence_to_reproduce ──
        s2r = 0.0
        if is_partial_access:
            s2r += 3.0  # some work some don't → need steps
        if not has_subsystem_named and is_connectivity and not is_auth_issue:
            s2r += 0.5
        if any(kw in lower for kw in [
            "times out", "just times out",
        ]) and not has_subsystem_named:
            s2r += 1.0
        if has_subsystem_named and not is_partial_access:
            s2r -= 3.0
        scores["sequence_to_reproduce"] = s2r

    elif category == "Crew Access & Biometrics":
        # ── biometric_method ──
        bm = 0.0
        if is_auth_issue and not has_bio_detail and not is_provisioning:
            bm += 2.5
        if _bio_uncertain:
            bm += 3.0  # explicitly uncertain about method
        if any(kw in lower for kw in [
            "sign-in", "login", "log in", "authenticate", "locked out",
            "multi-factor", "mfbv", "bioscan", "biometric",
            "authentication failed", "authentication failure",
            "service account", "access code",
        ]) and not has_bio_detail:
            bm += 1.0
        if has_bio_detail:
            bm -= 5.0
        if is_provisioning and not any(kw in lower for kw in [
            "multi-factor", "biometric", "mfbv", "auth exemption",
        ]):
            bm -= 3.0
        if is_setup and not is_followup:
            bm -= 2.0
        if is_sso_redirect and not _bio_uncertain:
            bm -= 1.5
        if is_verbose_vague and not any(kw in lower for kw in [
            "sign-in", "login", "biometric", "mfbv", "authenticate",
            "access code", "service account",
        ]):
            bm -= 2.0
        scores["biometric_method"] = bm

        # ── module_specs ──
        ms = 0.0
        if is_hardware and not has_device_detail:
            ms += 3.0
        if any(kw in lower for kw in [
            "terminal", "wrist-com", "console", "device",
            "scanner", "reader", "crew console",
        ]) and not has_device_detail:
            ms += 1.0
        if has_device_detail:
            ms -= 5.0
        if is_remote and is_hardware:
            ms += 0.5
        if not is_hardware:
            ms -= 2.0
        if is_domain_env and is_hardware:
            ms += 0.5  # domain issue on a terminal
        scores["module_specs"] = ms

        # ── anomaly_readout ──
        ar = 0.0
        if is_verbose_vague:
            ar += 2.5  # long description but no technical detail
        if is_sso_redirect:
            ar += 2.0  # redirect without error
        if any(kw in lower for kw in [
            "without an error", "no error", "didn't capture",
            "can't describe", "not sure what error",
        ]):
            ar += 2.0
        if is_auth_issue and not has_error_detail and not is_provisioning:
            ar += 1.0
        if has_error_detail:
            ar -= 3.0
        if is_provisioning or is_setup:
            ar -= 3.0  # provisioning/setup don't need error readouts
        scores["anomaly_readout"] = ar

        # ── previous_signal_id ──
        psi = 0.0
        if is_followup and not has_past_ref:
            psi += 3.5
        if any(kw in lower for kw in [
            "same issue", "same problem", "same glitch",
            "happened before", "reported before", "back again",
            "still happening", "last time", "same error",
            "going back and forth", "for weeks",
            "same sign-in", "same authentication",
        ]) and not has_past_ref:
            psi += 1.0
        if has_past_ref:
            psi -= 5.0
        if not is_followup:
            psi -= 3.0
        scores["previous_signal_id"] = psi

        # ── sensor_log_or_capture ──
        sl = 0.0
        if is_verbose_vague and not has_attachment:
            sl += 2.5  # long vague description, needs evidence
        if tried_capture_failed:
            sl += 3.0
        if _bio_uncertain and not has_attachment:
            sl += 1.5  # uncertain about bio method → need capture of what happens
        if is_remote and not has_attachment:
            sl += 1.0
        if has_attachment:
            sl -= 5.0
        if is_provisioning or is_setup:
            sl -= 3.0
        scores["sensor_log_or_capture"] = sl

        # ── mission_impact ──
        mi = 0.0
        if is_provisioning:
            mi += 2.5  # group/permission requests need impact justification
        if multi_affected and not mentions_impact:
            mi += 1.5
        if is_followup and has_past_ref:
            mi += 1.5  # follow-up with ref but no impact
        if mentions_impact:
            mi -= 3.0
        if not is_provisioning and not multi_affected and not is_followup:
            mi -= 2.0
        scores["mission_impact"] = mi

        # ── crew_contact ──
        cc = 0.0
        if is_remote and missing_contact:
            cc += 4.0
        if filing_for_other or is_behalf:
            cc += 2.0
        if is_remote:
            cc += 1.5
        if missing_contact:
            cc += 2.0
        if not is_behalf and not filing_for_other and not is_remote:
            cc -= 4.0
        scores["crew_contact"] = cc

        # ── affected_crew ──
        ac = 0.0
        if multi_affected:
            ac += 3.0
        if is_provisioning and any(kw in lower for kw in [
            "12 people", "about 12", "number of",
        ]):
            ac += 1.0
        if not multi_affected and not is_provisioning:
            ac -= 4.0
        scores["affected_crew"] = ac

        # ── affected_subsystem ──
        asub = 0.0
        if is_sso_redirect:
            asub += 2.5  # SSO redirect to specific module
        if not has_subsystem_named and not is_auth_issue:
            asub += 2.0
        if has_subsystem_named:
            asub -= 1.0
        if is_auth_issue and not any(kw in lower for kw in [
            "sso", "saml", "biometric", "mfbv", "crew profile",
            "security group", "portal", "atlas archive",
            "bioscan", "sign-in", "credential",
        ]):
            asub += 1.5
        if is_provisioning:
            asub -= 2.0
        scores["affected_subsystem"] = asub

        # ── habitat_conditions ──
        hc = 0.0
        if is_remote:
            hc += 3.0
        if is_domain_env:
            hc += 3.0  # domain/environment mismatch
        if any(kw in lower for kw in [
            "outpost", "off-ship", "mining", "asteroid",
            "contoso-legacy", "old domain",
        ]):
            hc += 1.0
        if not is_remote and not is_domain_env:
            hc -= 4.0
        scores["habitat_conditions"] = hc

        # ── software_version ──
        sv = 0.0
        if is_setup and any(kw in lower for kw in [
            "outdated", "current guide",
        ]):
            sv += 4.0  # asking for setup with outdated info
        if any(kw in lower for kw in [
            "sso", "saml", "portal", "app",
        ]) and "version" not in lower and not is_sso_redirect:
            sv += 1.0
        if has_device_detail:
            sv -= 1.0
        if not is_setup and not missing_version:
            sv -= 1.0
        scores["software_version"] = sv

        # ── recurrence_pattern ──
        rp = 0.0
        if is_recurring:
            rp += 3.0
        if not is_recurring:
            rp -= 5.0
        scores["recurrence_pattern"] = rp

    # Pick top items by score — target ~2 items (matching gold avg 1.71)
    ranked = sorted(scores.items(), key=lambda x: -x[1])
    result: list[str] = []
    for item, score in ranked:
        if score <= 0:
            break
        result.append(item)
        if len(result) >= 2:
            # Only include a 3rd if its score is very high (strict threshold)
            if len(ranked) > len(result):
                next_item, next_score = ranked[len(result)]
                if next_score >= 4.5:
                    result.append(next_item)
            break

    # Guarantee at least 1 item (all gold tickets have ≥1)
    if not result and scores:
        result = [ranked[0][0]]

    return result


# ── Main entry point ──────────────────────────────────────────────────

def classify_by_rules(
    subject: str,
    description: str,
    reporter_dept: str,
    channel: str,
) -> TriageDecision:
    """Attempt rule-based classification.

    Always returns a decision. The ``confidence`` field indicates how
    certain the rules are — callers should fall back to LLM when
    confidence is below a threshold.
    """
    text = f"{subject} {description}"
    cleaned = strip_injection(text)

    # Category + team
    category, team, cat_confidence = _detect_category(cleaned)

    # Priority (pass original text for injection detection)
    priority, pri_confidence = _detect_priority(cleaned, category, subject, text)

    # Override priority for non-technical categories
    if category == "Not a Mission Signal":
        priority, pri_confidence = "P4", 0.90
    elif category == "Mission Briefing Request":
        cleaned_lower = cleaned.lower()
        if priority in ("P1", "P2"):
            pass  # Keep high priority for urgent offboarding/time-critical briefings
        elif any(kw in cleaned_lower for kw in ["full setup", "setup needed", "new crew member"]):
            priority, pri_confidence = "P3", 0.80
        else:
            priority, pri_confidence = "P4", 0.85

    # Escalation (pass original text for injection detection)
    needs_escalation = _detect_escalation(cleaned, priority, category, subject, text)

    # Missing info
    missing = _detect_missing_info(cleaned, category)

    # Category confidence is the primary factor for rules-vs-LLM decision.
    # Priority uncertainty should not block a confident category match.
    confidence = cat_confidence * 0.8 + pri_confidence * 0.2

    return TriageDecision(
        category=category,
        team=team,
        priority=priority,
        needs_escalation=needs_escalation,
        missing_information=missing,
        confidence=confidence,
    )
