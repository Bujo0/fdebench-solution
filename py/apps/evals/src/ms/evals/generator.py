# Copyright (c) Microsoft. All rights reserved.
"""Core eval dataset generation engine.

Combines scenario templates, fixtures, and modifiers to produce
diverse, balanced ticket datasets with deterministic gold answers.
"""

import random
from collections import Counter
from datetime import datetime
from datetime import timedelta
from datetime import timezone

from ms.evals.constants import CATEGORY_WEIGHTS
from ms.evals.constants import CHANNEL_WEIGHTS
from ms.evals.constants import PRIORITY_WEIGHTS
from ms.evals.constants import Category
from ms.evals.constants import Priority
from ms.evals.fixtures import generate_reporter
from ms.evals.fixtures import pick_attachments
from ms.evals.models import GenerationStats
from ms.evals.models import Reporter
from ms.evals.models import ScenarioTemplate
from ms.evals.models import Ticket
from ms.evals.models import TriageGold
from ms.evals.modifiers import apply_modifier
from ms.evals.modifiers import select_modifiers
from ms.evals.scenarios.registry import pick_scenario


def _weighted_choice(rng: random.Random, options: dict[str, float]) -> str:
    """Select from weighted options."""
    items = list(options.keys())
    weights = list(options.values())
    return rng.choices(items, weights=weights, k=1)[0]


def _generate_timestamp(rng: random.Random, base_date: datetime) -> str:
    """Generate a realistic ticket creation timestamp.

    80% during business hours (8am-6pm), 20% off-hours.
    Spread across a 30-day window from base_date.
    """
    day_offset = rng.randint(0, 29)
    date = base_date + timedelta(days=day_offset)

    if rng.random() < 0.80:
        hour = rng.randint(8, 17)
        minute = rng.randint(0, 59)
    else:
        hour = rng.choice([*range(0, 8), *range(18, 24)])
        minute = rng.randint(0, 59)

    dt = date.replace(hour=hour, minute=minute, second=0, microsecond=0, tzinfo=timezone.utc)
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")


def _render_description(template: str, rng: random.Random) -> str:
    """Replace simple placeholders in description templates."""
    replacements = {
        "{department}": rng.choice([
            "Wealth Management", "Trading", "Compliance", "Finance",
            "Engineering", "Marketing", "Operations", "HR",
            "Risk Management", "Treasury", "Legal", "Procurement",
            "Client Services", "Research", "Internal Audit", "DevOps",
            "Investor Relations", "Corporate Strategy", "Data Science",
            "Backend Engineering", "Frontend Engineering", "Product Management",
        ]),
        "{app}": rng.choice([
            "Salesforce", "SAP", "Bloomberg Terminal", "Power BI",
            "Concur", "Workday", "ServiceNow", "Azure DevOps",
            "Jira", "Confluence", "Tableau", "Snowflake",
            "Databricks", "DocuSign", "Slack", "Zoom",
            "CrowdStrike", "Splunk", "Datadog", "GitHub Enterprise",
        ]),
        "{name}": rng.choice([
            "John", "Sarah", "David", "Lisa", "Mike", "Emma",
            "Priya", "Carlos", "Wei", "Fatima", "Ravi", "Sophie",
            "Ahmed", "Maria", "Yuki", "Hassan", "Nina", "Kofi",
        ]),
        "{name1}": rng.choice(["alice.jones", "mark.taylor", "priya.kumar", "chen.wei"]),
        "{name2}": rng.choice(["bob.smith", "sarah.martinez", "ravi.patel", "emma.wilson"]),
        "{name3}": rng.choice(["carol.white", "james.garcia", "yuki.tanaka", "fatima.hassan"]),
        "{number}": str(rng.randint(10000, 99999)),
        "{date}": f"2026-{rng.randint(1, 12):02d}-{rng.randint(1, 28):02d}",
        "{time}": f"{rng.randint(7, 18):02d}:{rng.randint(0, 59):02d}",
        "{floor}": str(rng.choice([2, 3, 4, 5, 6, 7, 8, 10, 12, 14, 15, 18, 22])),
        "{office}": rng.choice(["NYC", "London", "Singapore"]),
        "{os}": rng.choice(["Windows 11", "Windows 10", "macOS Sonoma", "macOS Ventura"]),
        "{browser}": rng.choice(["Chrome", "Edge", "Firefox", "Safari"]),
        "{vpn}": rng.choice(["GlobalProtect", "Cisco AnyConnect", "Zscaler", "Pulse Secure"]),
        "{error_code}": f"0x{rng.randint(0x80000000, 0x8FFFFFFF):08X}",
    }
    result = template
    for placeholder, value in replacements.items():
        result = result.replace(placeholder, value)
    return result


def generate_ticket_pair(
    ticket_id: str,
    scenario: ScenarioTemplate,
    channel: str,
    rng: random.Random,
    base_date: datetime,
    modifiers: list[str] | None = None,
) -> tuple[Ticket, TriageGold, list[str]]:
    """Generate a single ticket + gold answer pair from a scenario template.

    Args:
        ticket_id: Unique ticket ID (e.g., "INC-2001").
        scenario: The scenario template to instantiate.
        channel: Submission channel.
        rng: Seeded random generator.
        base_date: Base date for timestamp generation.
        modifiers: Optional list of modifier names to apply.

    Returns:
        Tuple of (ticket, gold_answer, applied_modifiers).
    """
    name, email, department = generate_reporter(rng)
    subject = rng.choice(scenario.subjects)
    description = _render_description(rng.choice(scenario.descriptions), rng)
    attachments = pick_attachments(rng)

    if scenario.attachment_options:
        extra = rng.choice(scenario.attachment_options)
        attachments = list(set(attachments + extra))

    applied_modifiers: list[str] = modifiers if modifiers is not None else select_modifiers(rng)
    original_subject = subject
    original_description = description
    for mod in applied_modifiers:
        subject, description = apply_modifier(mod, subject, description, rng)

    # Ensure modifiers didn't produce empty content
    if not subject.strip():
        subject = original_subject
    if not description.strip():
        description = original_description

    timestamp = _generate_timestamp(rng, base_date)

    ticket = Ticket(
        ticket_id=ticket_id,
        subject=subject,
        description=description,
        reporter=Reporter(name=name, email=email, department=department),
        created_at=timestamp,
        channel=channel,
        attachments=attachments,
    )

    next_action = rng.choice(scenario.next_best_actions)
    steps = rng.choice(scenario.remediation_steps)

    gold = TriageGold(
        ticket_id=ticket_id,
        category=scenario.category.value,
        priority=scenario.priority.value,
        assigned_team=scenario.assigned_team.value,
        needs_escalation=scenario.needs_escalation,
        missing_information=[m.value for m in scenario.missing_information],
        next_best_action=_render_description(next_action, rng),
        remediation_steps=[_render_description(s, rng) for s in steps],
    )

    return ticket, gold, applied_modifiers


def generate_dataset(
    count: int,
    seed: int = 42,
    start_id: int = 2001,
    base_date: datetime | None = None,
) -> tuple[list[Ticket], list[TriageGold], GenerationStats]:
    """Generate a complete eval dataset with balanced distributions.

    Args:
        count: Number of tickets to generate.
        seed: Random seed for reproducibility.
        start_id: Starting ticket ID number.
        base_date: Base date for timestamps (defaults to 2026-03-15).

    Returns:
        Tuple of (tickets, gold_answers, generation_stats).
    """
    # Import all scenario modules to populate the registry
    import ms.evals.scenarios.access_auth  # noqa: F401, PLC0415
    import ms.evals.scenarios.data_storage  # noqa: F401, PLC0415
    import ms.evals.scenarios.general_inquiry  # noqa: F401, PLC0415
    import ms.evals.scenarios.hardware  # noqa: F401, PLC0415
    import ms.evals.scenarios.low_priority  # noqa: F401, PLC0415
    import ms.evals.scenarios.network  # noqa: F401, PLC0415
    import ms.evals.scenarios.not_support  # noqa: F401, PLC0415
    import ms.evals.scenarios.security  # noqa: F401, PLC0415
    import ms.evals.scenarios.software  # noqa: F401, PLC0415

    rng = random.Random(seed)
    if base_date is None:
        base_date = datetime(2026, 3, 15, tzinfo=timezone.utc)

    tickets: list[Ticket] = []
    golds: list[TriageGold] = []

    # Track distributions for balancing
    cat_counter: Counter[str] = Counter()
    pri_counter: Counter[str] = Counter()
    chan_counter: Counter[str] = Counter()
    esc_counter: Counter[str] = Counter()
    modifier_counter: Counter[str] = Counter()
    team_counter: Counter[str] = Counter()
    missing_counter: Counter[str] = Counter()

    seen_subjects: set[str] = set()
    seen_descriptions: set[str] = set()

    for i in range(count):
        ticket_id = f"INC-{start_id + i}"

        # Select category with distribution awareness
        category_str = _balanced_select(
            rng, {k.value: v for k, v in CATEGORY_WEIGHTS.items()}, cat_counter, i,
        )
        category = Category(category_str)

        # Pick a scenario for this category
        scenario = pick_scenario(category, rng)

        # Override priority if needed for balance
        if i > count * 0.1:
            target_pri = _balanced_select(
                rng, {k.value: v for k, v in PRIORITY_WEIGHTS.items()}, pri_counter, i,
            )
            if target_pri != scenario.priority.value:
                scenario = _adjust_priority(scenario, Priority(target_pri))

        # Select channel with balance
        channel = _balanced_select(
            rng, {k.value: v for k, v in CHANNEL_WEIGHTS.items()}, chan_counter, i,
        )

        # Generate ticket pair
        ticket, gold, applied_mods = generate_ticket_pair(
            ticket_id=ticket_id,
            scenario=scenario,
            channel=channel,
            rng=rng,
            base_date=base_date,
        )

        # Ensure uniqueness (regenerate if duplicate)
        attempts = 0
        while (ticket.subject in seen_subjects or ticket.description in seen_descriptions) and attempts < 10:
            ticket, gold, applied_mods = generate_ticket_pair(
                ticket_id=ticket_id,
                scenario=scenario,
                channel=channel,
                rng=rng,
                base_date=base_date,
            )
            attempts += 1

        tickets.append(ticket)
        golds.append(gold)
        seen_subjects.add(ticket.subject)
        seen_descriptions.add(ticket.description)

        # Update counters
        cat_counter[gold.category] += 1
        pri_counter[gold.priority] += 1
        chan_counter[ticket.channel] += 1
        team_counter[gold.assigned_team] += 1
        esc_counter[str(gold.needs_escalation)] += 1
        for mod in applied_mods:
            modifier_counter[mod] += 1
        for mi in gold.missing_information:
            missing_counter[mi] += 1

    stats = GenerationStats(
        total_tickets=len(tickets),
        category_counts=dict(cat_counter),
        priority_counts=dict(pri_counter),
        team_counts=dict(team_counter),
        channel_counts=dict(chan_counter),
        escalation_counts=dict(esc_counter),
        missing_info_counts=dict(missing_counter),
        modifier_counts=dict(modifier_counter),
        unique_subjects=len(seen_subjects),
        unique_descriptions=len(seen_descriptions),
    )

    return tickets, golds, stats


def _balanced_select(
    rng: random.Random,
    target_weights: dict[str, float],
    current_counts: Counter[str],
    total_so_far: int,
) -> str:
    """Select a value that helps maintain the target distribution.

    Uses a mix of target-weighted random selection and deficit-based correction.
    """
    if total_so_far < 10:
        return _weighted_choice(rng, target_weights)

    # Calculate deficit for each option
    adjusted_weights: dict[str, float] = {}
    for key, target_pct in target_weights.items():
        current_pct = current_counts.get(key, 0) / max(total_so_far, 1)
        deficit = target_pct - current_pct
        adjusted_weights[key] = max(target_pct + deficit * 2.0, 0.01)

    return _weighted_choice(rng, adjusted_weights)


def _adjust_priority(scenario: ScenarioTemplate, new_priority: Priority) -> ScenarioTemplate:
    """Create a copy of a scenario with adjusted priority.

    Also adjusts escalation based on priority rules.
    """
    needs_escalation = scenario.needs_escalation
    if new_priority == Priority.P1 and scenario.category in (
        Category.SECURITY,
        Category.DATA,
    ):
        needs_escalation = True

    return ScenarioTemplate(
        scenario_id=scenario.scenario_id,
        category=scenario.category,
        priority=new_priority,
        assigned_team=scenario.assigned_team,
        needs_escalation=needs_escalation,
        missing_information=scenario.missing_information,
        subjects=scenario.subjects,
        descriptions=scenario.descriptions,
        next_best_actions=scenario.next_best_actions,
        remediation_steps=scenario.remediation_steps,
        attachment_options=scenario.attachment_options,
    )
