# Copyright (c) Microsoft. All rights reserved.
"""Main generator that expands scenario definitions into ticket + gold-answer pairs."""

import hashlib
import json
import random
from pathlib import Path

from ms.eval_generator.models import Reporter
from ms.eval_generator.models import Ticket
from ms.eval_generator.models import TriageGold
from ms.eval_generator.models import VALID_CATEGORIES
from ms.eval_generator.models import VALID_CHANNELS
from ms.eval_generator.models import VALID_MISSING_INFO
from ms.eval_generator.models import VALID_PRIORITIES
from ms.eval_generator.models import VALID_TEAMS
from ms.eval_generator.reporters import COMMON_ATTACHMENTS
from ms.eval_generator.reporters import DEPARTMENTS
from ms.eval_generator.reporters import FIRST_NAMES
from ms.eval_generator.reporters import LAST_NAMES
from ms.eval_generator.scenarios import ScenarioDefinition
from ms.eval_generator.scenarios import collect_all_scenarios

# ── Channels with weights (email is most common in enterprise) ────────────────

CHANNEL_WEIGHTS = {"email": 0.35, "portal": 0.30, "chat": 0.20, "phone": 0.15}

# ── Timestamp generation ──────────────────────────────────────────────────────

BUSINESS_HOURS = list(range(7, 20))  # 7 AM to 7 PM
AFTER_HOURS = [0, 1, 2, 3, 4, 5, 6, 20, 21, 22, 23]


def _generate_timestamp(rng: random.Random, *, after_hours: bool = False) -> str:
    """Generate a realistic ISO 8601 timestamp in March 2026."""
    day = rng.randint(2, 27)
    hours = AFTER_HOURS if after_hours else BUSINESS_HOURS
    hour = rng.choice(hours)
    minute = rng.randint(0, 59)
    return f"2026-03-{day:02d}T{hour:02d}:{minute:02d}:00Z"


def _generate_reporter(rng: random.Random, departments: tuple[str, ...]) -> Reporter:
    """Generate a unique reporter with a name, email, and department."""
    first = rng.choice(FIRST_NAMES)
    last = rng.choice(LAST_NAMES)
    dept = rng.choice(list(departments)) if departments else rng.choice(DEPARTMENTS)
    email = f"{first.lower()}.{last.lower().replace(' ', '')}@contoso.com"
    return Reporter(name=f"{first} {last}", email=email, department=dept)


def _pick_channel(rng: random.Random, channels: tuple[str, ...]) -> str:
    """Pick a submission channel, respecting scenario constraints."""
    if channels:
        return rng.choice(list(channels))
    options = list(CHANNEL_WEIGHTS.keys())
    weights = list(CHANNEL_WEIGHTS.values())
    return rng.choices(options, weights=weights, k=1)[0]


def _pick_attachments(rng: random.Random, attachment_sets: tuple[tuple[str, ...], ...]) -> list[str]:
    """Pick an attachment set for a ticket."""
    if attachment_sets:
        return list(rng.choice(attachment_sets))
    # 60% no attachments, 40% some attachment
    if rng.random() < 0.6:
        return []
    att_type = rng.choice(list(COMMON_ATTACHMENTS.keys()))
    return list(rng.choice(COMMON_ATTACHMENTS[att_type]))


def _validate_scenario(scenario: ScenarioDefinition) -> list[str]:
    """Validate a scenario definition against known constraints."""
    errors: list[str] = []
    gold = scenario.gold

    if gold.category not in VALID_CATEGORIES:
        errors.append(f"[{scenario.scenario_id}] Invalid category: {gold.category}")
    if gold.priority not in VALID_PRIORITIES:
        errors.append(f"[{scenario.scenario_id}] Invalid priority: {gold.priority}")
    if gold.assigned_team not in VALID_TEAMS:
        errors.append(f"[{scenario.scenario_id}] Invalid team: {gold.assigned_team}")
    for mi in gold.missing_information:
        if mi not in VALID_MISSING_INFO:
            errors.append(f"[{scenario.scenario_id}] Invalid missing_info term: {mi}")
    if not gold.next_best_action:
        errors.append(f"[{scenario.scenario_id}] Empty next_best_action")
    if not gold.remediation_steps:
        errors.append(f"[{scenario.scenario_id}] Empty remediation_steps")

    if not scenario.subjects:
        errors.append(f"[{scenario.scenario_id}] No subjects defined")
    if not scenario.descriptions:
        errors.append(f"[{scenario.scenario_id}] No descriptions defined")

    return errors


class EvalDatasetGenerator:
    """Generates an eval dataset by expanding scenarios into ticket+gold pairs."""

    def __init__(self, seed: int = 42, max_variants_per_scenario: int = 6) -> None:
        self._seed = seed
        self._max_variants = max_variants_per_scenario
        self._rng = random.Random(seed)

    def generate(self) -> tuple[list[Ticket], list[TriageGold]]:
        """Generate all tickets and gold answers from scenario definitions."""
        scenarios = collect_all_scenarios()

        # Validate all scenarios first
        all_errors: list[str] = []
        for s in scenarios:
            all_errors.extend(_validate_scenario(s))
        if all_errors:
            raise ValueError(f"Scenario validation errors:\n" + "\n".join(all_errors))

        tickets: list[Ticket] = []
        golds: list[TriageGold] = []
        ticket_counter = 5001  # Start after existing INC-0001..INC-1050 range

        for scenario in scenarios:
            variants = self._expand_scenario(scenario)
            for subject, description in variants:
                ticket_id = f"INC-{ticket_counter:04d}"
                ticket_counter += 1

                reporter = _generate_reporter(self._rng, scenario.departments)
                channel = _pick_channel(self._rng, scenario.channels)
                attachments = _pick_attachments(self._rng, scenario.attachment_sets)
                timestamp = _generate_timestamp(self._rng)

                ticket = Ticket(
                    ticket_id=ticket_id,
                    subject=subject,
                    description=description,
                    reporter=reporter,
                    created_at=timestamp,
                    channel=channel,
                    attachments=attachments,
                )

                gold = TriageGold(
                    ticket_id=ticket_id,
                    category=scenario.gold.category,
                    priority=scenario.gold.priority,
                    assigned_team=scenario.gold.assigned_team,
                    needs_escalation=scenario.gold.needs_escalation,
                    missing_information=list(scenario.gold.missing_information),
                    next_best_action=scenario.gold.next_best_action,
                    remediation_steps=list(scenario.gold.remediation_steps),
                )

                tickets.append(ticket)
                golds.append(gold)

        # Shuffle to avoid category clustering
        combined = list(zip(tickets, golds))
        self._rng.shuffle(combined)
        tickets = [t for t, _ in combined]
        golds = [g for _, g in combined]

        return tickets, golds

    def _expand_scenario(self, scenario: ScenarioDefinition) -> list[tuple[str, str]]:
        """Expand a scenario into (subject, description) pairs."""
        pairs: list[tuple[str, str]] = []
        for subj in scenario.subjects:
            for desc in scenario.descriptions:
                pairs.append((subj, desc))

        # Limit to max_variants, randomly sampled if too many
        if len(pairs) > self._max_variants:
            pairs = self._rng.sample(pairs, self._max_variants)

        return pairs

    def write_dataset(self, output_dir: Path) -> tuple[Path, Path]:
        """Generate and write the eval dataset to JSON files."""
        tickets, golds = self.generate()

        output_dir.mkdir(parents=True, exist_ok=True)
        tickets_path = output_dir / "eval_dataset.json"
        golds_path = output_dir / "eval_dataset_gold.json"

        tickets_data = [t.model_dump() for t in tickets]
        golds_data = [g.model_dump() for g in golds]

        tickets_path.write_text(json.dumps(tickets_data, indent=2, ensure_ascii=False) + "\n")
        golds_path.write_text(json.dumps(golds_data, indent=2, ensure_ascii=False) + "\n")

        return tickets_path, golds_path


def print_dataset_stats(tickets: list[Ticket], golds: list[TriageGold]) -> None:
    """Print distribution statistics for the generated dataset."""
    from collections import Counter

    print(f"\n{'=' * 60}")
    print(f"  EVAL DATASET STATISTICS")
    print(f"{'=' * 60}\n")
    print(f"  Total tickets: {len(tickets)}\n")

    cats = Counter(g.category for g in golds)
    print("  Category distribution:")
    for cat, count in sorted(cats.items()):
        pct = count / len(golds) * 100
        print(f"    {cat:<30s} {count:4d} ({pct:5.1f}%)")

    print()
    pris = Counter(g.priority for g in golds)
    print("  Priority distribution:")
    for pri in ["P1", "P2", "P3", "P4"]:
        count = pris.get(pri, 0)
        pct = count / len(golds) * 100
        print(f"    {pri:<30s} {count:4d} ({pct:5.1f}%)")

    print()
    teams = Counter(g.assigned_team for g in golds)
    print("  Team distribution:")
    for team, count in sorted(teams.items()):
        pct = count / len(golds) * 100
        print(f"    {team:<30s} {count:4d} ({pct:5.1f}%)")

    print()
    channels = Counter(t.channel for t in tickets)
    print("  Channel distribution:")
    for ch, count in sorted(channels.items()):
        pct = count / len(tickets) * 100
        print(f"    {ch:<30s} {count:4d} ({pct:5.1f}%)")

    print()
    esc = Counter(g.needs_escalation for g in golds)
    print("  Escalation distribution:")
    for val in [True, False]:
        count = esc.get(val, 0)
        pct = count / len(golds) * 100
        print(f"    {str(val):<30s} {count:4d} ({pct:5.1f}%)")

    print()
    mi_counter: Counter[str] = Counter()
    for g in golds:
        for mi in g.missing_information:
            mi_counter[mi] += 1
    print("  Missing information term usage:")
    for term, count in mi_counter.most_common():
        print(f"    {term:<30s} {count:4d}")

    # Compute a deterministic hash of the dataset for versioning
    content = json.dumps([t.model_dump() for t in tickets], sort_keys=True)
    dataset_hash = hashlib.sha256(content.encode()).hexdigest()[:12]
    print(f"\n  Dataset hash: {dataset_hash}")
    print()
