# Copyright (c) Microsoft. All rights reserved.
"""Schema validation and distribution analysis for generated datasets.

Validates generated tickets and gold answers against the JSON schemas
and produces balance analysis reports.
"""

import json
from collections import Counter
from pathlib import Path

from ms.evals.constants import Category
from ms.evals.constants import Channel
from ms.evals.constants import MissingInfo
from ms.evals.constants import Priority
from ms.evals.constants import Team
from ms.evals.models import GenerationStats
from ms.evals.models import Ticket
from ms.evals.models import TriageGold


def validate_ticket(ticket: Ticket) -> list[str]:
    """Validate a ticket against the input schema constraints.

    Returns:
        List of validation error messages (empty if valid).
    """
    errors: list[str] = []

    if not ticket.ticket_id.startswith("INC-"):
        errors.append(f"ticket_id must start with 'INC-': {ticket.ticket_id}")

    if not ticket.subject:
        errors.append(f"{ticket.ticket_id}: empty subject")

    if not ticket.description:
        errors.append(f"{ticket.ticket_id}: empty description")

    valid_channels = {c.value for c in Channel}
    if ticket.channel not in valid_channels:
        errors.append(f"{ticket.ticket_id}: invalid channel '{ticket.channel}'")

    if not ticket.reporter.email.endswith("@contoso.com"):
        errors.append(f"{ticket.ticket_id}: email must be @contoso.com")

    return errors


def validate_gold(gold: TriageGold) -> list[str]:
    """Validate a gold answer against the output schema constraints.

    Returns:
        List of validation error messages (empty if valid).
    """
    errors: list[str] = []

    valid_categories = {c.value for c in Category}
    if gold.category not in valid_categories:
        errors.append(f"{gold.ticket_id}: invalid category '{gold.category}'")

    valid_priorities = {p.value for p in Priority}
    if gold.priority not in valid_priorities:
        errors.append(f"{gold.ticket_id}: invalid priority '{gold.priority}'")

    valid_teams = {t.value for t in Team}
    if gold.assigned_team not in valid_teams:
        errors.append(f"{gold.ticket_id}: invalid team '{gold.assigned_team}'")

    valid_missing = {m.value for m in MissingInfo}
    for mi in gold.missing_information:
        if mi not in valid_missing:
            errors.append(f"{gold.ticket_id}: invalid missing_info '{mi}'")

    if not gold.next_best_action:
        errors.append(f"{gold.ticket_id}: empty next_best_action")

    if not gold.remediation_steps:
        errors.append(f"{gold.ticket_id}: empty remediation_steps")

    return errors


def validate_dataset(
    tickets: list[Ticket],
    golds: list[TriageGold],
) -> list[str]:
    """Validate an entire dataset for schema compliance and consistency.

    Returns:
        List of all validation errors.
    """
    errors: list[str] = []

    if len(tickets) != len(golds):
        errors.append(f"Ticket count ({len(tickets)}) != gold count ({len(golds)})")

    ticket_ids = {t.ticket_id for t in tickets}
    gold_ids = {g.ticket_id for g in golds}

    missing_golds = ticket_ids - gold_ids
    if missing_golds:
        errors.append(f"Tickets without gold answers: {missing_golds}")

    extra_golds = gold_ids - ticket_ids
    if extra_golds:
        errors.append(f"Gold answers without tickets: {extra_golds}")

    for ticket in tickets:
        errors.extend(validate_ticket(ticket))

    for gold in golds:
        errors.extend(validate_gold(gold))

    # Check for duplicate ticket IDs
    ids = [t.ticket_id for t in tickets]
    if len(ids) != len(set(ids)):
        dupes = [tid for tid, cnt in Counter(ids).items() if cnt > 1]
        errors.append(f"Duplicate ticket IDs: {dupes}")

    return errors


def analyze_balance(stats: GenerationStats) -> str:
    """Produce a human-readable balance analysis report.

    Returns:
        Formatted report string.
    """
    lines = [
        f"{'=' * 60}",
        "  EVAL DATASET GENERATION REPORT",
        f"{'=' * 60}",
        "",
        f"  Total tickets: {stats.total_tickets}",
        f"  Unique subjects: {stats.unique_subjects}",
        f"  Unique descriptions: {stats.unique_descriptions}",
        "",
        "  Category Distribution:",
    ]

    total = stats.total_tickets
    for cat, count in sorted(stats.category_counts.items(), key=lambda x: -x[1]):
        pct = count / total * 100
        lines.append(f"    {cat:<28s}  {count:5d}  ({pct:5.1f}%)")

    lines.append("")
    lines.append("  Priority Distribution:")
    for pri in ["P1", "P2", "P3", "P4"]:
        count = stats.priority_counts.get(pri, 0)
        pct = count / total * 100
        lines.append(f"    {pri:<28s}  {count:5d}  ({pct:5.1f}%)")

    lines.append("")
    lines.append("  Team Distribution:")
    for team, count in sorted(stats.team_counts.items(), key=lambda x: -x[1]):
        pct = count / total * 100
        lines.append(f"    {team:<28s}  {count:5d}  ({pct:5.1f}%)")

    lines.append("")
    lines.append("  Channel Distribution:")
    for chan, count in sorted(stats.channel_counts.items(), key=lambda x: -x[1]):
        pct = count / total * 100
        lines.append(f"    {chan:<28s}  {count:5d}  ({pct:5.1f}%)")

    lines.append("")
    lines.append("  Escalation Distribution:")
    for esc, count in sorted(stats.escalation_counts.items()):
        pct = count / total * 100
        lines.append(f"    {esc:<28s}  {count:5d}  ({pct:5.1f}%)")

    lines.append("")
    lines.append("  Missing Info Distribution:")
    for mi, count in sorted(stats.missing_info_counts.items(), key=lambda x: -x[1]):
        lines.append(f"    {mi:<28s}  {count:5d}")

    lines.append("")
    lines.append("  Modifier Distribution:")
    for mod, count in sorted(stats.modifier_counts.items(), key=lambda x: -x[1]):
        lines.append(f"    {mod:<28s}  {count:5d}")

    lines.append("")
    lines.append(f"{'=' * 60}")

    return "\n".join(lines)


def write_dataset(
    tickets: list[Ticket],
    golds: list[TriageGold],
    output_dir: Path,
    prefix: str = "eval",
) -> tuple[Path, Path]:
    """Write tickets and gold answers to JSON files.

    Args:
        tickets: List of generated tickets.
        golds: List of gold standard answers.
        output_dir: Directory to write files to.
        prefix: Filename prefix (e.g., "eval" -> "eval.json", "eval_gold.json").

    Returns:
        Tuple of (tickets_path, gold_path).
    """
    output_dir.mkdir(parents=True, exist_ok=True)

    tickets_path = output_dir / f"{prefix}.json"
    gold_path = output_dir / f"{prefix}_gold.json"

    ticket_dicts = [json.loads(t.model_dump_json()) for t in tickets]
    gold_dicts = [json.loads(g.model_dump_json()) for g in golds]

    tickets_path.write_text(json.dumps(ticket_dicts, indent=2, ensure_ascii=False) + "\n")
    gold_path.write_text(json.dumps(gold_dicts, indent=2, ensure_ascii=False) + "\n")

    return tickets_path, gold_path
