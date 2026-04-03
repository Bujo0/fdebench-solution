"""Dataset generator that converts scenarios into eval ticket + gold answer pairs."""

import json
from collections import Counter
from pathlib import Path

from ms.evals_core.constants import Category
from ms.evals_core.constants import Channel
from ms.evals_core.constants import Priority
from ms.evals_core.constants import Team
from ms.evals_core.models import Scenario
from ms.evals_core.scenarios import get_all_scenarios
from ms.evals_core.scenarios.base import ScenarioDefinition

TICKET_ID_START = 2000


def generate_dataset(scenarios: list[ScenarioDefinition] | None = None) -> list[Scenario]:
    """Generate the full eval dataset from all scenario definitions.

    Args:
        scenarios: Optional list of scenarios to use. If None, loads all registered scenarios.

    Returns:
        List of Scenario objects with unique ticket IDs.
    """
    if scenarios is None:
        scenarios = get_all_scenarios()

    dataset: list[Scenario] = []
    for idx, scenario_def in enumerate(scenarios):
        ticket_id = f"INC-{TICKET_ID_START + idx:04d}"
        scenario = scenario_def.to_scenario(ticket_id)
        dataset.append(scenario)

    return dataset


def validate_dataset(dataset: list[Scenario]) -> list[str]:
    """Validate the dataset for correctness and balance.

    Returns:
        List of warning/error messages. Empty means all good.
    """
    issues: list[str] = []

    # Check for duplicate ticket IDs
    ticket_ids = [s.ticket.ticket_id for s in dataset]
    dupes = [tid for tid, count in Counter(ticket_ids).items() if count > 1]
    if dupes:
        issues.append(f"Duplicate ticket IDs: {dupes}")

    # Check category distribution
    cat_counts = Counter(s.gold.category for s in dataset)
    total = len(dataset)
    for cat in Category:
        count = cat_counts.get(cat, 0)
        pct = count / total * 100 if total else 0
        if pct < 5:
            issues.append(f"Category '{cat}' underrepresented: {count} ({pct:.1f}%)")
        if pct > 20:
            issues.append(f"Category '{cat}' overrepresented: {count} ({pct:.1f}%)")

    # Check priority distribution
    pri_counts = Counter(s.gold.priority for s in dataset)
    for pri in Priority:
        count = pri_counts.get(pri, 0)
        pct = count / total * 100 if total else 0
        if pct < 5:
            issues.append(f"Priority '{pri}' underrepresented: {count} ({pct:.1f}%)")

    # Check team distribution
    team_counts = Counter(s.gold.assigned_team for s in dataset)
    for team in Team:
        count = team_counts.get(team, 0)
        pct = count / total * 100 if total else 0
        if team != Team.NONE and pct < 3:
            issues.append(f"Team '{team}' underrepresented: {count} ({pct:.1f}%)")

    # Check escalation balance
    esc_count = sum(1 for s in dataset if s.gold.needs_escalation)
    esc_pct = esc_count / total * 100 if total else 0
    if esc_pct < 15 or esc_pct > 50:
        issues.append(f"Escalation balance off: {esc_count} ({esc_pct:.1f}%) — target 20-40%")

    # Check channel distribution
    chan_counts = Counter(s.ticket.channel for s in dataset)
    for chan_name, count in chan_counts.items():
        pct = count / total * 100
        if pct < 5:
            issues.append(f"Channel '{chan_name}' underrepresented: {count} ({pct:.1f}%)")

    return issues


def print_distribution(dataset: list[Scenario]) -> None:
    """Print distribution statistics for the dataset."""
    total = len(dataset)
    print(f"\n{'=' * 60}")
    print(f"  EVAL DATASET STATISTICS — {total} tickets")
    print(f"{'=' * 60}\n")

    # Category distribution
    print("  Category Distribution:")
    cat_counts = Counter(s.gold.category for s in dataset)
    for cat in Category:
        count = cat_counts.get(cat, 0)
        pct = count / total * 100
        bar = "█" * int(pct / 2)
        print(f"    {cat.value:<28s}  {count:4d}  ({pct:5.1f}%)  {bar}")

    # Priority distribution
    print("\n  Priority Distribution:")
    pri_counts = Counter(s.gold.priority for s in dataset)
    for pri in Priority:
        count = pri_counts.get(pri, 0)
        pct = count / total * 100
        bar = "█" * int(pct / 2)
        print(f"    {pri.value:<28s}  {count:4d}  ({pct:5.1f}%)  {bar}")

    # Team distribution
    print("\n  Team Distribution:")
    team_counts = Counter(s.gold.assigned_team for s in dataset)
    for team in Team:
        count = team_counts.get(team, 0)
        pct = count / total * 100
        bar = "█" * int(pct / 2)
        print(f"    {team.value:<28s}  {count:4d}  ({pct:5.1f}%)  {bar}")

    # Channel distribution
    print("\n  Channel Distribution:")
    chan_counts = Counter(s.ticket.channel for s in dataset)
    for chan in Channel:
        count = chan_counts.get(chan, 0)
        pct = count / total * 100
        bar = "█" * int(pct / 2)
        print(f"    {chan.value:<28s}  {count:4d}  ({pct:5.1f}%)  {bar}")

    # Escalation
    esc_count = sum(1 for s in dataset if s.gold.needs_escalation)
    print(f"\n  Escalation: {esc_count}/{total} ({esc_count / total * 100:.1f}%)")

    # Difficulty
    print("\n  Difficulty Distribution:")
    diff_counts = Counter(s.difficulty for s in dataset)
    for diff in ["easy", "medium", "hard", "extreme"]:
        count = diff_counts.get(diff, 0)
        pct = count / total * 100
        print(f"    {diff:<28s}  {count:4d}  ({pct:5.1f}%)")

    # Tag analysis
    all_tags: list[str] = []
    for s in dataset:
        all_tags.extend(s.tags)
    tag_counts = Counter(all_tags)
    print("\n  Top 20 Tags:")
    for tag, count in tag_counts.most_common(20):
        print(f"    {tag:<28s}  {count:4d}")

    print()


def export_dataset(dataset: list[Scenario], output_dir: Path) -> tuple[Path, Path]:
    """Export the dataset as two JSON files (tickets + gold answers).

    Args:
        dataset: List of Scenario objects.
        output_dir: Directory to write the files to.

    Returns:
        Tuple of (tickets_path, gold_path).
    """
    output_dir.mkdir(parents=True, exist_ok=True)

    tickets = [
        {
            "ticket_id": s.ticket.ticket_id,
            "subject": s.ticket.subject,
            "description": s.ticket.description,
            "reporter": {
                "name": s.ticket.reporter.name,
                "email": s.ticket.reporter.email,
                "department": s.ticket.reporter.department,
            },
            "created_at": s.ticket.created_at,
            "channel": s.ticket.channel,
            "attachments": s.ticket.attachments,
        }
        for s in dataset
    ]

    golds = [
        {
            "ticket_id": s.gold.ticket_id,
            "category": s.gold.category,
            "priority": s.gold.priority,
            "assigned_team": s.gold.assigned_team,
            "needs_escalation": s.gold.needs_escalation,
            "missing_information": list(s.gold.missing_information),
            "next_best_action": s.gold.next_best_action,
            "remediation_steps": list(s.gold.remediation_steps),
        }
        for s in dataset
    ]

    tickets_path = output_dir / "generated_eval.json"
    gold_path = output_dir / "generated_eval_gold.json"

    tickets_path.write_text(json.dumps(tickets, indent=2) + "\n")
    gold_path.write_text(json.dumps(golds, indent=2) + "\n")

    return tickets_path, gold_path
