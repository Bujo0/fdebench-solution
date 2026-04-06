#!/usr/bin/env python3
"""Scenario-level tests for the data cleanup evaluation dataset.

Each test validates that a specific data-quality scenario is represented in the
dataset and that its gold label reflects the correct classification despite the
noise in the ticket content.

Scenario categories tested:
  - Forwarded email chains with buried issues
  - Base64-encoded image data in descriptions
  - HTML markup and excessive email signatures
  - Duplicated / repeated content
  - Empty or near-empty descriptions
  - Mixed-language content
  - Log dumps and stack traces
  - Unrelated email threads containing real issues
  - Unfilled templates
  - Encoding artifacts / mojibake
  - Repetitive text padding
  - Multi-issue tickets
  - Minimal content with massive signatures
  - Keyboard garbage with real issue
  - Automated monitoring alerts
  - Emoji-heavy / informal formatting
  - Phishing email forwarding
  - Excessive whitespace
  - URL-heavy descriptions
  - Garbled phone transcripts
"""

import json
import sys
from pathlib import Path

_DATA = Path(__file__).resolve().parent.parent / "data" / "tickets"


def _load_pair() -> tuple[list[dict], dict[str, dict]]:
    tickets = json.loads((_DATA / "data_cleanup_eval.json").read_text(encoding="utf-8"))
    golds = json.loads((_DATA / "data_cleanup_eval_gold.json").read_text(encoding="utf-8"))
    gold_by_id = {g["ticket_id"]: g for g in golds}
    return tickets, gold_by_id


def _ticket_by_id(tickets: list[dict], tid: str) -> dict:
    matches = [t for t in tickets if t["ticket_id"] == tid]
    assert matches, f"Ticket {tid} not found"
    return matches[0]


# ── Scenario: Forwarded email chain (INC-2001) ───────────────────────


def test_forwarded_chain_is_network_issue():
    """A deeply nested forwarded email chain should be classified by the actual VPN issue."""
    tickets, gold_by_id = _load_pair()
    ticket = _ticket_by_id(tickets, "INC-2001")
    gold = gold_by_id["INC-2001"]

    # The ticket has multiple forwarded headers but the real issue is VPN disconnection
    assert ticket["description"].count("Forwarded message") >= 4, "Should have multiple forwards"
    assert gold["category"] == "Network & Connectivity"
    assert gold["assigned_team"] == "Network Operations"


# ── Scenario: Base64 image data (INC-2002) ────────────────────────────


def test_base64_image_classified_correctly():
    """A ticket with large base64 image data should be classified by the text content, not the noise."""
    tickets, gold_by_id = _load_pair()
    ticket = _ticket_by_id(tickets, "INC-2002")
    gold = gold_by_id["INC-2002"]

    assert "base64" in ticket["description"].lower(), "Should contain base64 data"
    assert len(ticket["description"]) > 3000, "Base64 makes the description very long"
    assert gold["category"] == "Data & Storage"
    assert gold["assigned_team"] == "Data Platform"


# ── Scenario: HTML email with signature (INC-2003) ────────────────────


def test_html_email_classified_correctly():
    """An HTML-formatted email with extensive signature should be classified by the actual hardware issue."""
    tickets, gold_by_id = _load_pair()
    ticket = _ticket_by_id(tickets, "INC-2003")
    gold = gold_by_id["INC-2003"]

    assert "<html>" in ticket["description"].lower(), "Should contain HTML markup"
    assert "CONFIDENTIAL" in ticket["description"], "Should contain legal disclaimer"
    assert gold["category"] == "Hardware & Peripherals"
    assert gold["assigned_team"] == "Endpoint Engineering"


# ── Scenario: Duplicated content (INC-2004) ───────────────────────────


def test_duplicated_content_classified_correctly():
    """A ticket with excessively repeated text should be classified by the actual printer issue."""
    tickets, gold_by_id = _load_pair()
    ticket = _ticket_by_id(tickets, "INC-2004")
    gold = gold_by_id["INC-2004"]

    assert ticket["description"].count("PRINTER ON FLOOR 5") >= 5, "Should have repeated content"
    assert gold["category"] == "Hardware & Peripherals"
    assert gold["assigned_team"] == "Endpoint Engineering"
    assert gold["priority"] == "P3", "Repetition should not inflate priority"


# ── Scenario: Empty description (INC-2005) ────────────────────────────


def test_empty_description_is_not_a_ticket():
    """A ticket with blank subject and whitespace-only description should be classified as not a support ticket."""
    tickets, gold_by_id = _load_pair()
    ticket = _ticket_by_id(tickets, "INC-2005")
    gold = gold_by_id["INC-2005"]

    assert ticket["subject"] == "", "Subject should be empty"
    assert ticket["description"].strip() == "", "Description should be effectively empty"
    assert gold["category"] == "Not a Support Ticket"
    assert gold["assigned_team"] == "None"
    assert gold["priority"] == "P4"


# ── Scenario: Mixed language (INC-2006) ───────────────────────────────


def test_mixed_language_classified_correctly():
    """A ticket with mixed English and translated content should be classified by the SAP issue."""
    _, gold_by_id = _load_pair()
    gold = gold_by_id["INC-2006"]

    assert gold["category"] == "Software & Applications"
    assert gold["assigned_team"] == "Enterprise Applications"


# ── Scenario: Log dump (INC-2007) ─────────────────────────────────────


def test_log_dump_classified_as_critical():
    """A ticket with extensive error logs should be classified by the database issue and flagged P1."""
    tickets, gold_by_id = _load_pair()
    ticket = _ticket_by_id(tickets, "INC-2007")
    gold = gold_by_id["INC-2007"]

    assert "java.sql.SQLException" in ticket["description"], "Should contain stack traces"
    assert "Connection pool exhausted" in ticket["description"], "Should mention pool exhaustion"
    assert gold["category"] == "Data & Storage"
    assert gold["priority"] == "P1"
    assert gold["needs_escalation"] is True


# ── Scenario: Email thread with buried issue (INC-2008) ───────────────


def test_email_thread_with_buried_issue():
    """An email reply chain where the IT issue is mentioned casually mid-thread."""
    tickets, gold_by_id = _load_pair()
    ticket = _ticket_by_id(tickets, "INC-2008")
    gold = gold_by_id["INC-2008"]

    assert "[EXTERNAL]" in ticket["subject"], "Should be an external email thread"
    assert gold["category"] == "Software & Applications"
    assert gold["assigned_team"] == "Enterprise Applications"


# ── Scenario: Unfilled template (INC-2009) ────────────────────────────


def test_unfilled_template_is_not_a_ticket():
    """A template with only placeholder text should not be treated as a real ticket."""
    tickets, gold_by_id = _load_pair()
    ticket = _ticket_by_id(tickets, "INC-2009")
    gold = gold_by_id["INC-2009"]

    assert "[PLACEHOLDER]" in ticket["subject"], "Subject should contain placeholder"
    assert "[Describe your issue here]" in ticket["description"], "Description should be unfilled template"
    assert gold["category"] == "Not a Support Ticket"
    assert gold["assigned_team"] == "None"


# ── Scenario: Encoding artifacts (INC-2010) ───────────────────────────


def test_encoding_artifacts_classified_correctly():
    """A ticket with encoding issues should be classified by the actual account lockout issue."""
    _, gold_by_id = _load_pair()
    gold = gold_by_id["INC-2010"]

    assert gold["category"] == "Access & Authentication"
    assert gold["assigned_team"] == "Identity & Access Management"
    assert gold["priority"] == "P2"


# ── Scenario: Repetitive padding (INC-2011) ───────────────────────────


def test_repetitive_padding_classified_correctly():
    """A ticket padded with repeated phrases should be classified by the actual Wi-Fi issue."""
    tickets, gold_by_id = _load_pair()
    ticket = _ticket_by_id(tickets, "INC-2011")
    gold = gold_by_id["INC-2011"]

    assert ticket["description"].count("Wi-Fi not working.") >= 50, "Should have lots of repetition"
    assert gold["category"] == "Network & Connectivity"
    assert gold["assigned_team"] == "Network Operations"


# ── Scenario: Multi-issue ticket (INC-2012) ───────────────────────────


def test_multi_issue_prioritizes_most_urgent():
    """A ticket with 5 issues should be classified by the most critical one (Bloomberg data feed)."""
    tickets, gold_by_id = _load_pair()
    ticket = _ticket_by_id(tickets, "INC-2012")
    gold = gold_by_id["INC-2012"]

    # Ticket explicitly says "Bloomberg one is the most urgent"
    assert "Bloomberg" in ticket["description"]
    assert gold["priority"] == "P1", "The Bloomberg data feed issue is critical for trading"
    assert gold["needs_escalation"] is True


# ── Scenario: Tiny content with massive signature (INC-2013) ──────────


def test_minimal_content_with_signature():
    """A 3-word issue buried in a massive email signature should be classified correctly."""
    tickets, gold_by_id = _load_pair()
    ticket = _ticket_by_id(tickets, "INC-2013")
    gold = gold_by_id["INC-2013"]

    # The actual issue is just "need password reset"
    desc = ticket["description"]
    issue_text = "need password reset"
    sig_start = desc.find("Sent from my iPhone")
    assert issue_text in desc[: sig_start + 20], "Issue should be at the very beginning"
    assert gold["category"] == "Access & Authentication"
    assert gold["assigned_team"] == "Identity & Access Management"


# ── Scenario: Keyboard garbage (INC-2014) ─────────────────────────────


def test_keyboard_garbage_with_real_issue():
    """A ticket starting with keyboard spam should be classified by the actual VPN issue underneath."""
    tickets, gold_by_id = _load_pair()
    ticket = _ticket_by_id(tickets, "INC-2014")
    gold = gold_by_id["INC-2014"]

    assert "asdkfjh" in ticket["description"], "Should start with garbage text"
    assert "sorry my cat" in ticket["description"], "Should have explanation"
    assert gold["category"] == "Network & Connectivity"
    assert gold["assigned_team"] == "Network Operations"


# ── Scenario: Automated monitoring alert (INC-2015) ───────────────────


def test_automated_alert_classified_correctly():
    """An automated monitoring alert should be classified as a real, urgent issue."""
    tickets, gold_by_id = _load_pair()
    ticket = _ticket_by_id(tickets, "INC-2015")
    gold = gold_by_id["INC-2015"]

    assert "AUTOMATED ALERT" in ticket["description"]
    assert gold["category"] == "Data & Storage"
    assert gold["priority"] == "P1"
    assert gold["needs_escalation"] is True


# ── Scenario: Emoji-heavy content (INC-2016) ─────────────────────────


def test_emoji_heavy_classified_correctly():
    """A ticket with informal/emoji-heavy language should be classified by the hardware issue."""
    _, gold_by_id = _load_pair()
    gold = gold_by_id["INC-2016"]

    assert gold["category"] == "Hardware & Peripherals"
    assert gold["assigned_team"] == "Endpoint Engineering"


# ── Scenario: Phishing forward (INC-2017) ─────────────────────────────


def test_phishing_forward_is_security():
    """A user forwarding a suspicious phishing email should be classified as security."""
    tickets, gold_by_id = _load_pair()
    ticket = _ticket_by_id(tickets, "INC-2017")
    gold = gold_by_id["INC-2017"]

    assert "micros0ft" in ticket["description"], "Should contain spoofed domain"
    assert gold["category"] == "Security & Compliance"
    assert gold["assigned_team"] == "Security Operations"


# ── Scenario: Excessive whitespace (INC-2018) ─────────────────────────


def test_excessive_whitespace_classified_correctly():
    """A ticket with excessive newlines/whitespace should be classified by the AD lockout issue."""
    tickets, gold_by_id = _load_pair()
    ticket = _ticket_by_id(tickets, "INC-2018")
    gold = gold_by_id["INC-2018"]

    newline_count = ticket["description"].count("\n")
    assert newline_count >= 20, f"Should have excessive newlines, got {newline_count}"
    assert gold["category"] == "Access & Authentication"
    assert gold["assigned_team"] == "Identity & Access Management"


# ── Scenario: URL-heavy description (INC-2019) ───────────────────────


def test_url_heavy_classified_correctly():
    """A ticket with many internal URLs should be classified by the SSL cert and performance issues."""
    tickets, gold_by_id = _load_pair()
    ticket = _ticket_by_id(tickets, "INC-2019")
    gold = gold_by_id["INC-2019"]

    url_count = ticket["description"].count("https://")
    assert url_count >= 5, f"Should have many URLs, got {url_count}"
    assert gold["category"] == "Security & Compliance"
    assert gold["priority"] == "P1", "Expiring SSL cert is critical"
    assert gold["needs_escalation"] is True


# ── Scenario: Garbled phone transcript (INC-2020) ────────────────────


def test_garbled_transcript_classified_correctly():
    """A poor-quality phone transcript should be classified by the SharePoint upload issue."""
    tickets, gold_by_id = _load_pair()
    ticket = _ticket_by_id(tickets, "INC-2020")
    gold = gold_by_id["INC-2020"]

    assert "[inaudible]" in ticket["description"], "Should have transcript gaps"
    assert "[garbled]" in ticket["description"], "Should have garbled sections"
    assert gold["category"] == "Data & Storage"
    assert gold["assigned_team"] == "Data Platform"


# ── Cross-cutting: no data-quality noise should inflate priority ──────


def test_noise_does_not_inflate_priority():
    """Tickets with noisy data (shouting, repetition, urgency language) should not have inflated priorities."""
    _, gold_by_id = _load_pair()

    # INC-2004: Repeated shouting about a printer
    assert gold_by_id["INC-2004"]["priority"] == "P3", "Printer shouting should still be P3"

    # INC-2005: Empty ticket
    assert gold_by_id["INC-2005"]["priority"] == "P4", "Empty ticket should be P4"

    # INC-2009: Unfilled template
    assert gold_by_id["INC-2009"]["priority"] == "P4", "Template should be P4"


def test_all_data_cleanup_tickets_have_descriptions():
    """All data cleanup tickets have the description field present (even if blank)."""
    tickets, _ = _load_pair()
    for ticket in tickets:
        assert "description" in ticket, f"{ticket['ticket_id']} missing description field"


# ── Runner ────────────────────────────────────────────────────────────

if __name__ == "__main__":
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_")]
    passed = 0
    failed = 0
    for t in tests:
        try:
            t()
            passed += 1
            print(f"  ✓ {t.__name__}")
        except AssertionError as e:
            failed += 1
            print(f"  ✗ {t.__name__}: {e}")
    print(f"\n{passed} passed, {failed} failed")
    sys.exit(1 if failed else 0)
