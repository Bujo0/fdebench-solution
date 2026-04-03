"""Schema validation for generated tickets and gold answers."""

from __future__ import annotations

import re

from generator.models import (
    CATEGORIES,
    CHANNELS,
    MISSING_INFO_VOCABULARY,
    PRIORITIES,
    TEAMS,
)


def validate_ticket(ticket: dict) -> list[str]:
    """Validate a generated ticket against the input schema. Returns list of errors."""
    errors: list[str] = []
    tid = ticket.get("ticket_id", "UNKNOWN")

    # Required fields
    for field in ["ticket_id", "subject", "description", "reporter", "created_at", "channel"]:
        if field not in ticket:
            errors.append(f"{tid}: missing required field '{field}'")

    # ticket_id format
    if "ticket_id" in ticket:
        if not re.match(r"^INC-\d+$", ticket["ticket_id"]):
            errors.append(f"{tid}: ticket_id does not match pattern ^INC-\\d+$")

    # channel
    if ticket.get("channel") and ticket["channel"] not in CHANNELS:
        errors.append(f"{tid}: invalid channel '{ticket['channel']}'")

    # reporter
    reporter = ticket.get("reporter", {})
    for field in ["name", "email", "department"]:
        if field not in reporter:
            errors.append(f"{tid}: missing reporter.{field}")

    # attachments
    if "attachments" in ticket and not isinstance(ticket["attachments"], list):
        errors.append(f"{tid}: attachments must be a list")

    # subject and description must be non-empty
    if not ticket.get("subject", "").strip():
        errors.append(f"{tid}: subject is empty")
    if not ticket.get("description", "").strip():
        errors.append(f"{tid}: description is empty")

    return errors


def validate_gold(gold: dict) -> list[str]:
    """Validate a gold answer against the output schema. Returns list of errors."""
    errors: list[str] = []
    tid = gold.get("ticket_id", "UNKNOWN")

    # Required fields
    for field in [
        "ticket_id", "category", "priority", "assigned_team",
        "needs_escalation", "missing_information", "next_best_action",
        "remediation_steps",
    ]:
        if field not in gold:
            errors.append(f"{tid}: missing required field '{field}'")

    # category
    if gold.get("category") and gold["category"] not in CATEGORIES:
        errors.append(f"{tid}: invalid category '{gold['category']}'")

    # priority
    if gold.get("priority") and gold["priority"] not in PRIORITIES:
        errors.append(f"{tid}: invalid priority '{gold['priority']}'")

    # assigned_team
    if gold.get("assigned_team") and gold["assigned_team"] not in TEAMS:
        errors.append(f"{tid}: invalid assigned_team '{gold['assigned_team']}'")

    # needs_escalation
    if "needs_escalation" in gold and not isinstance(gold["needs_escalation"], bool):
        errors.append(f"{tid}: needs_escalation must be boolean")

    # missing_information
    mi = gold.get("missing_information", [])
    if not isinstance(mi, list):
        errors.append(f"{tid}: missing_information must be a list")
    else:
        for item in mi:
            if item not in MISSING_INFO_VOCABULARY:
                errors.append(f"{tid}: invalid missing_information item '{item}'")

    # remediation_steps
    rs = gold.get("remediation_steps", [])
    if not isinstance(rs, list):
        errors.append(f"{tid}: remediation_steps must be a list")
    elif len(rs) == 0:
        errors.append(f"{tid}: remediation_steps is empty")

    # next_best_action
    if not gold.get("next_best_action", "").strip():
        errors.append(f"{tid}: next_best_action is empty")

    return errors


def validate_dataset(
    tickets: list[dict], golds: list[dict]
) -> list[str]:
    """Validate an entire dataset. Returns list of errors."""
    errors: list[str] = []

    # Check counts match
    if len(tickets) != len(golds):
        errors.append(f"Ticket count ({len(tickets)}) != gold count ({len(golds)})")

    # Check ticket IDs align
    ticket_ids = [t["ticket_id"] for t in tickets]
    gold_ids = [g["ticket_id"] for g in golds]

    if ticket_ids != gold_ids:
        mismatches = [
            (t, g) for t, g in zip(ticket_ids, gold_ids) if t != g
        ]
        errors.append(
            f"Ticket ID mismatch at {len(mismatches)} positions. "
            f"First: {mismatches[0] if mismatches else 'N/A'}"
        )

    # Check uniqueness
    if len(set(ticket_ids)) != len(ticket_ids):
        errors.append(f"Duplicate ticket IDs found")

    # Validate each ticket and gold
    for ticket in tickets:
        errors.extend(validate_ticket(ticket))

    for gold in golds:
        errors.extend(validate_gold(gold))

    return errors
