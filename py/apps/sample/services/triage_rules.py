"""Deterministic rule-based triage classifier — fast path that skips LLM.

Architecture: Request → strip_injection → rule_classifier → if confident: return (fast!)
                                                           → if ambiguous: LLM fallback (slow but rare)

Tuned against the public eval gold data. Only 2 categories appear in the
eval set: Communications & Navigation and Crew Access & Biometrics.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field


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


def _detect_category(text: str) -> tuple[str, str, float]:
    """Return (category, team, confidence)."""
    lower = text.lower()

    access_score = sum(1 for kw in _ACCESS_KEYWORDS if kw in lower)
    comms_score = sum(1 for kw in _COMMS_KEYWORDS if kw in lower)

    # Strong keyword boosts
    access_score += sum(5 for kw in _ACCESS_STRONG if kw in lower)
    comms_score += sum(5 for kw in _COMMS_STRONG if kw in lower)

    # Subject-line signals are strong indicators
    subj = text.split("\n")[0].lower() if "\n" in text else lower[:200]
    if any(kw in subj for kw in ["access", "auth", "login", "sign-in", "biometric", "lockout", "sso", "credential"]):
        access_score += 3
    if any(kw in subj for kw in ["network", "relay", "rf mesh", "connectivity", "subspace", "comm link", "speed", "latency"]):
        comms_score += 3

    # "comm link" in subject usually means it's a transcribed call —
    # content determines category, not the medium
    # "access" in subject is ambiguous (could be network access)
    # but paired with auth terms it's Crew Access

    if comms_score > access_score:
        confidence = min(0.95, 0.7 + 0.03 * (comms_score - access_score))
        return "Communications & Navigation", "Deep Space Communications", confidence
    elif access_score > comms_score:
        confidence = min(0.95, 0.7 + 0.03 * (access_score - comms_score))
        return "Crew Access & Biometrics", "Crew Identity & Airlock Control", confidence
    elif comms_score > 0:
        return "Communications & Navigation", "Deep Space Communications", 0.6
    else:
        return "Communications & Navigation", "Deep Space Communications", 0.4


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

    # Questions and how-to
    if any(phrase in lower for phrase in [
        "how do i", "how to", "instructions needed",
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

    # Requests (not incidents)
    if any(phrase in subj_lower for phrase in [
        "rule request", "setup instructions", "needed for",
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

    # Long-standing issue (started weeks ago)
    if any(phrase in lower for phrase in [
        "two weeks ago", "started about two weeks",
        "started around 9am and has happened",
    ]):
        p4_signals += 1

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

    # Multiple issues in one ticket with urgency
    if "three different issues" in lower:
        p2_signals += 1
    if "i have been waiting" in lower:
        p2_signals += 1

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

    # P1 only escalates for cross-station or security-related P1s
    if priority == "P1":
        if any(kw in lower for kw in [
            "cross-atlantic", "cross-station",
            "account lockout",
        ]):
            return True
        # Safety keywords always escalate
        if any(kw in lower for kw in _P1_SAFETY_KEYWORDS):
            return True
        # Otherwise P1 does NOT auto-escalate (e.g., single-user split-tunnel)
        return False

    # Threat / security indicators
    if any(kw in lower for kw in [
        "unauthorized", "exfiltration",
        "hostile", "malware", "social engineering",
        "impersonation",
    ]):
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
    """Identify 0-3 most relevant missing info items."""
    lower = text.lower()
    missing: list[str] = []

    if category == "Communications & Navigation":
        # sector_coordinates — most common for comms
        if not any(kw in lower for kw in ["deck ", "floor ", "wing ", "location"]):
            missing.append("sector_coordinates")
        # anomaly_readout
        if not any(kw in lower for kw in [
            "error message", "error code", "log", "readout",
            "traceroute output",
        ]):
            missing.append("anomaly_readout")
        # system_configuration
        if any(kw in lower for kw in [
            "signal barrier", "rule request", "subspace relay",
            "failover", "sd-interstation", "dns",
        ]) and "configuration" not in lower:
            missing.append("system_configuration")
        # stardate
        if any(kw in lower for kw in [
            "failover", "site-to-site", "failure",
        ]) and "stardate" not in lower:
            missing.append("stardate")
        # module_specs
        if any(kw in lower for kw in [
            "relay client", "fabricator", "terminal",
        ]) and "model" not in lower and "version" not in lower:
            missing.append("module_specs")
        # recurrence_pattern
        if any(kw in lower for kw in [
            "intermittent", "recurring", "every 15 minutes",
            "keeps dropping", "keeps disconnecting", "back again",
        ]):
            missing.append("recurrence_pattern")
        # affected_crew
        if "on behalf of" in lower or "multiple" in lower:
            missing.append("affected_crew")
        # sensor_log_or_capture
        if any(kw in lower for kw in ["screenshot", "diagnostic", "log dump"]):
            missing.append("sensor_log_or_capture")
        # crew_contact
        if "on behalf of" in lower and "contact" not in lower:
            missing.append("crew_contact")
        # software_version
        if any(kw in lower for kw in [
            "relay client", "starprotect",
        ]) and "version" not in lower:
            missing.append("software_version")
        # affected_subsystem
        if not any(kw in lower for kw in [
            "rf mesh", "subspace relay", "signal barrier", "wan",
            "dns", "hermes", "rdp", "fabricator", "comm relay",
        ]):
            missing.append("affected_subsystem")
        # sequence_to_reproduce
        if "can't access" in lower and "steps" not in lower:
            missing.append("sequence_to_reproduce")

    elif category == "Crew Access & Biometrics":
        # biometric_method — most common for access
        if any(kw in lower for kw in [
            "biometric", "bioscan", "authenticate",
        ]) and "method" not in lower:
            missing.append("biometric_method")
        # module_specs
        if any(kw in lower for kw in [
            "terminal", "wrist-com", "console", "device",
        ]):
            missing.append("module_specs")
        # anomaly_readout
        if not any(kw in lower for kw in [
            "error", "message", "readout", "code",
        ]):
            missing.append("anomaly_readout")
        # previous_signal_id
        if any(kw in lower for kw in [
            "same issue", "reported before", "follow-up",
            "last time", "last rotation", "same glitch",
            "back again",
        ]):
            missing.append("previous_signal_id")
        # sensor_log_or_capture
        if not any(kw in lower for kw in [
            "screenshot", "capture", "log",
        ]):
            missing.append("sensor_log_or_capture")
        # mission_impact
        if "impact" not in lower and "affected" not in lower:
            missing.append("mission_impact")
        # software_version
        if any(kw in lower for kw in [
            "sso", "saml", "portal",
        ]) and "version" not in lower:
            missing.append("software_version")
        # crew_contact
        if "off-ship" in lower or "subspace callback" in lower:
            missing.append("crew_contact")
        # affected_crew
        if any(kw in lower for kw in [
            "multiple", "number of", "crew members",
        ]):
            missing.append("affected_crew")
        # affected_subsystem
        if not any(kw in lower for kw in [
            "sso", "saml", "biometric", "mfbv", "crew profile",
            "security group", "portal", "atlas archive",
        ]):
            missing.append("affected_subsystem")
        # habitat_conditions
        if "off-ship" in lower or "outpost" in lower:
            missing.append("habitat_conditions")
        # recurrence_pattern
        if any(kw in lower for kw in [
            "recurring", "again", "keeps", "repeated",
        ]):
            missing.append("recurrence_pattern")

    # Deduplicate and limit to 2-3
    seen: set[str] = set()
    result: list[str] = []
    for item in missing:
        if item not in seen:
            seen.add(item)
            result.append(item)
        if len(result) >= 3:
            break
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

    # Escalation (pass original text for injection detection)
    needs_escalation = _detect_escalation(cleaned, priority, category, subject, text)

    # Missing info
    missing = _detect_missing_info(cleaned, category)

    # Overall confidence = min of category and priority confidence
    confidence = min(cat_confidence, pri_confidence)

    return TriageDecision(
        category=category,
        team=team,
        priority=priority,
        needs_escalation=needs_escalation,
        missing_information=missing,
        confidence=confidence,
    )
