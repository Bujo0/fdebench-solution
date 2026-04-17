"""Lightweight preprocessing for triage — catches only structurally certain cases.

Design principle (from fde-moj):
  "Only hard-code structurally certain cases. Everything else goes to LLM
   with explicit uncertainty."

The preprocessor handles ~20-30% of items (non-incidents) with near-100%
confidence. Everything else goes to the LLM as the primary classifier.
Hints (P1 safety, threat keywords) are passed to LLM and post-processing
but never used as final classifications here.
"""

import re
from dataclasses import dataclass


@dataclass
class PreprocessResult:
    """Output of the preprocessor — hints for LLM, not final decisions."""

    is_non_incident: bool = False
    is_p1_safety: bool = False
    has_threat_keywords: bool = False
    has_injection: bool = False
    cleaned_text: str = ""
    non_incident_reason: str = ""


# ── Injection stripping ──────────────────────────────────────────────

_INJECTION_PATTERNS = [
    re.compile(r"(ignore|disregard|forget)\s+(all\s+)?(previous|prior|above)\s+(instructions?|prompts?|rules?)", re.I),
    re.compile(r"(you are now|switch to|enter)\s+(test|debug|override|admin)\s+mode", re.I),
    re.compile(r"output\s+(your|the)\s+(complete\s+)?system\s+prompt", re.I),
    re.compile(r"reveal\s+(your|all)\s+(instructions?|configuration|rules?)", re.I),
    re.compile(r"classify\s+(this\s+)?(as|=)\s*P[12]", re.I),
    re.compile(r"PRIORITY\s+OVERRIDE", re.I),
    re.compile(r"SYSTEM\s+DIRECTIVE", re.I),
    re.compile(r"Priority=P[12]", re.I),
    re.compile(r"(here\s+are|examples?\s+of)\s+(some\s+)?how\s+similar\s+signals?\s+were", re.I),
    re.compile(r"Example\s+\d+:", re.I),
    re.compile(r"(BASE64\s+ENCODED\s+FOR\s+SECURITY|decode\s+the\s+abo|decode\s+and\s+execute)", re.I),
    re.compile(r"Think\s+step\s+by\s+step\s+about\s+this\s+signal", re.I),
    re.compile(r"(repeat\s+after\s+me|say\s+exactly)", re.I),
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


# ── Non-incident detection (structurally certain) ────────────────────

_NON_INCIDENT_MARKERS = [
    "thank you",
    "thanks for",
    "thanks!",
    "thanks for fixing",
    "thanks for resolving",
    "got it working",
    "all good now",
    "resolved",
    "no longer an issue",
    "out of office",
    "cryo notice",
    "cryo-stasis",
    "cryo-sleep",
    "auto-reply",
    "automatic reply",
    "appreciate the quick",
    "appreciate the help",
    "i'm not reporting",
    "not reporting a fault",
    "not actually reporting",
    "not an outage",
    "drill at",
    "scheduled maintenance",
    "cafeteria",
]

_NON_INCIDENT_SUBJECTS = [
    "thanks",
    "re: [signal",
    "maintenance notification",
    "reminder:",
    "fyi:",
    "info:",
    "etiquette",
]

_REAL_ISSUE_MARKERS = [
    "not working",
    "error",
    "failure",
    "crash",
    "broken",
    "outage",
    "suspicious",
    "unauthorized",
    "failing",
    "down ",
    "delay",
    "lag",
    "intermittent",
    "dropout",
    "dropping",
    "timeout",
    "drift",
    "misrouting",
    "stuttered",
    "corrupting",
    "out of sync",
    "disable",
    "revoke",
    "onboarding",
    "offboarding",
    "requesting",
    "request for",
    "need to know",
    "how do i",
    "set up",
    "setup needed",
    "new crew member",
]

# ── P1 safety keywords (defined in routing guide as always-P1) ───────

_P1_SAFETY_KEYWORDS = [
    "hull breach",
    "decompression",
    "atmospheric compromise",
    "containment failure",
    "life support failure",
    "life-support failure",
    "life support threat",
    "life-support threat",
    "oxygen failure",
    "hostile contact",
]

# ── Threat keywords (hints only — not final classification) ──────────

_THREAT_HINTS = [
    "malware",
    "unauthorized access",
    "unauthorized login",
    "phishing",
    "exfiltration",
    "social engineering",
    "impersonation",
    "containment breach",
    "data breach",
]


def preprocess_signal(
    subject: str,
    description: str,
) -> PreprocessResult:
    """Lightweight preprocessing — catches only structurally certain cases.

    Returns hints for the LLM prompt and post-processing. Only
    ``is_non_incident`` is used as a final classification; everything
    else is advisory.
    """
    raw_text = f"{subject} {description}"
    cleaned = strip_injection(raw_text)
    lower = cleaned.lower()
    subj_lower = subject.lower()

    has_injection = any(pat.search(raw_text) for pat in _INJECTION_PATTERNS)

    # P1 safety detection (hint for post-processing override)
    is_p1_safety = any(kw in lower for kw in _P1_SAFETY_KEYWORDS)

    # Threat keyword detection (hint for LLM)
    has_threat_kw = any(kw in lower for kw in _THREAT_HINTS)

    # Non-incident detection — structurally obvious non-incidents
    non_incident_hits = sum(1 for m in _NON_INCIDENT_MARKERS if m in lower)
    if any(p in subj_lower for p in _NON_INCIDENT_SUBJECTS):
        non_incident_hits += 1

    is_non_incident = False
    reason = ""
    if non_incident_hits >= 1 and not is_p1_safety:
        real_issue_hits = sum(1 for kw in _REAL_ISSUE_MARKERS if kw in lower)
        if real_issue_hits == 0:
            is_non_incident = True
            reason = "auto-reply, thank-you, closure, or informational noise"

    return PreprocessResult(
        is_non_incident=is_non_incident,
        is_p1_safety=is_p1_safety,
        has_threat_keywords=has_threat_kw,
        has_injection=has_injection,
        cleaned_text=cleaned,
        non_incident_reason=reason,
    )
