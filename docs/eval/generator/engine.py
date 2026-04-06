"""Core ticket generator engine.

Takes scenario definitions and produces diverse ticket/gold-answer pairs
through parametric variation of reporters, channels, writing styles,
dates, and cross-cutting modifiers.
"""

import json
import random
from collections import Counter
from datetime import datetime
from datetime import timedelta
from datetime import timezone
from pathlib import Path

from generator.models import CHANNELS
from generator.models import GeneratedTicket
from generator.models import GoldAnswer
from generator.models import Scenario
from generator.reporters import REGULAR_REPORTERS
from generator.reporters import VIP_REPORTERS
from generator.text_variation import apply_auto_translated
from generator.text_variation import apply_base64_content
from generator.text_variation import apply_chat_style
from generator.text_variation import apply_conversation_history
from generator.text_variation import apply_corporate_jargon
from generator.text_variation import apply_email_signature
from generator.text_variation import apply_email_style
from generator.text_variation import apply_extremely_long
from generator.text_variation import apply_form_template
from generator.text_variation import apply_minimal
from generator.text_variation import apply_multilingual_content
from generator.text_variation import apply_panicked_style
from generator.text_variation import apply_passive_aggressive
from generator.text_variation import apply_phone_transcription_style
from generator.text_variation import apply_prompt_injection
from generator.text_variation import apply_stack_trace
from generator.text_variation import apply_typos
from generator.text_variation import apply_verbose_style


class TicketGenerator:
    """Generates diverse eval tickets from scenario definitions."""

    def __init__(self, seed: int = 42) -> None:
        self.rng = random.Random(seed)
        self.ticket_counter = 2001  # Start after INC-2000 to avoid conflicts
        self.used_scenario_subject_pairs: set[tuple[str, int]] = set()

    def _next_ticket_id(self) -> str:
        tid = f"INC-{self.ticket_counter:04d}"
        self.ticket_counter += 1
        return tid

    def _random_datetime(self) -> str:
        """Generate a random datetime in March 2026."""
        base = datetime(2026, 3, 1, tzinfo=timezone.utc)
        offset = timedelta(
            days=self.rng.randint(0, 30),
            hours=self.rng.randint(6, 22),
            minutes=self.rng.randint(0, 59),
        )
        dt = base + offset
        return dt.strftime("%Y-%m-%dT%H:%M:%SZ")

    def _pick_channel(self, scenario: Scenario) -> str:
        """Pick a channel based on scenario weights."""
        channels = list(scenario.channel_weights.keys())
        weights = list(scenario.channel_weights.values())
        return self.rng.choices(channels, weights=weights, k=1)[0]

    def _pick_reporter(self, is_vip_ticket: bool = False) -> tuple[str, str, str, bool]:
        """Pick a reporter. Returns (name, email, department, is_vip)."""
        if is_vip_ticket and VIP_REPORTERS:
            reporter = self.rng.choice(VIP_REPORTERS)
        else:
            reporter = self.rng.choice(REGULAR_REPORTERS)
        return reporter.name, reporter.email, reporter.department, reporter.is_vip

    def _generate_attachments(self, channel: str) -> list[str]:
        """Generate realistic attachment filenames."""
        if self.rng.random() > 0.25:
            return []

        attachment_pool = [
            "screenshot.png",
            "error_log.txt",
            "screenshot_2026-03-17.png",
            "event_viewer_export.evtx",
            "network_trace.pcap",
            "config_backup.xml",
            "error_screenshot.jpg",
            "system_info.txt",
            "crash_dump.dmp",
            "diagnostic_report.html",
            "teams_logs.zip",
            "browser_console.log",
            "vpn_client_log.txt",
            "policy_violation_report.pdf",
            "scan_results.csv",
            "affected_users_list.xlsx",
            "architecture_diagram.vsdx",
            "meeting_recording.mp4",
        ]

        count = self.rng.randint(1, 3)
        return self.rng.sample(attachment_pool, k=min(count, len(attachment_pool)))

    def _apply_style_modifiers(
        self,
        description: str,
        channel: str,
        reporter_name: str,
        reporter_email: str,
        tags: list[str],
    ) -> str:
        """Apply writing style modifiers based on channel and tags."""
        # Channel-specific styling
        if channel == "phone":
            description = apply_phone_transcription_style(description, self.rng)
        elif channel == "chat":
            description = apply_chat_style(description, self.rng)
        elif channel == "email" and self.rng.random() < 0.6:
            description = apply_email_style(description, reporter_name, self.rng)

        # Tag-based modifiers
        if "panicked" in tags:
            description = apply_panicked_style(description, self.rng)
        if "verbose" in tags:
            description = apply_verbose_style(description, self.rng)
        if "prompt_injection" in tags:
            injection_type = self.rng.choice(["prefix", "suffix", "inline"])
            description = apply_prompt_injection(description, injection_type, self.rng)
        if "conversation_history" in tags:
            description = apply_conversation_history(description, reporter_name, reporter_email, self.rng)
        if "base64_content" in tags:
            description = apply_base64_content(description, self.rng)
        if "multilingual" in tags:
            language = self.rng.choice(["japanese", "korean", "spanish", "french", "german", "portuguese"])
            description = apply_multilingual_content(description, language, self.rng)
        if "typos" in tags:
            description = apply_typos(description, self.rng)
        if "extremely_long" in tags:
            description = apply_extremely_long(description, self.rng)
        if "minimal" in tags:
            description = apply_minimal(description, self.rng)
        if "stack_trace" in tags:
            description = apply_stack_trace(description, self.rng)
        if "auto_translated" in tags:
            description = apply_auto_translated(description, self.rng)
        if "passive_aggressive" in tags:
            description = apply_passive_aggressive(description, self.rng)
        if "corporate_jargon" in tags:
            description = apply_corporate_jargon(description, self.rng)
        if "form_template" in tags:
            description = apply_form_template(description, reporter_name, self.rng)
        if "email_signature" in tags and channel == "email":
            description = apply_email_signature(description, reporter_name, self.rng)

        return description

    def generate_from_scenario(
        self,
        scenario: Scenario,
        subject_idx: int | None = None,
        desc_idx: int | None = None,
        force_vip: bool = False,
        extra_tags: list[str] | None = None,
    ) -> tuple[GeneratedTicket, GoldAnswer]:
        """Generate a single ticket + gold answer from a scenario."""
        ticket_id = self._next_ticket_id()

        # Pick subject and description variants
        if subject_idx is None:
            subject_idx = self.rng.randint(0, len(scenario.subjects) - 1)
        else:
            subject_idx = subject_idx % len(scenario.subjects)

        if desc_idx is None:
            desc_idx = self.rng.randint(0, len(scenario.descriptions) - 1)
        else:
            desc_idx = desc_idx % len(scenario.descriptions)

        subject = scenario.subjects[subject_idx]
        description = scenario.descriptions[desc_idx]

        # Pick channel and reporter
        channel = self._pick_channel(scenario)
        name, email, dept, is_vip = self._pick_reporter(is_vip_ticket=force_vip)

        # Combine tags
        tags = list(scenario.tags)
        if extra_tags:
            tags.extend(extra_tags)

        # Apply style modifiers
        description = self._apply_style_modifiers(description, channel, name, email, tags)

        # Generate attachments
        attachments = self._generate_attachments(channel)

        # Determine gold answer
        priority = scenario.priority
        needs_escalation = scenario.needs_escalation

        # VIP modifier: bump priority and escalate
        if is_vip or force_vip:
            priority_order = ["P4", "P3", "P2", "P1"]
            current_idx = priority_order.index(priority)
            if current_idx < len(priority_order) - 1:
                priority = priority_order[current_idx + 1]
            needs_escalation = True

        # Pick gold answer text variants
        nba_idx = self.rng.randint(0, len(scenario.next_best_actions) - 1)
        rem_idx = self.rng.randint(0, len(scenario.remediation_steps) - 1)

        ticket = GeneratedTicket(
            ticket_id=ticket_id,
            subject=subject,
            description=description,
            reporter_name=name,
            reporter_email=email,
            reporter_department=dept,
            created_at=self._random_datetime(),
            channel=channel,
            attachments=attachments,
        )

        gold = GoldAnswer(
            ticket_id=ticket_id,
            category=scenario.category,
            priority=priority,
            assigned_team=scenario.assigned_team,
            needs_escalation=needs_escalation,
            missing_information=list(scenario.missing_information),
            next_best_action=scenario.next_best_actions[nba_idx],
            remediation_steps=list(scenario.remediation_steps[rem_idx]),
        )

        return ticket, gold

    def generate_dataset(
        self,
        scenarios: list[Scenario],
        target_count: int = 2500,
    ) -> tuple[list[dict], list[dict]]:
        """Generate a balanced dataset from scenario definitions.

        Returns (tickets_list, golds_list) as JSON-serializable dicts.
        """
        tickets: list[dict] = []
        golds: list[dict] = []

        # Calculate how many tickets per scenario for balance
        base_per_scenario = max(1, target_count // len(scenarios))
        remainder = target_count - (base_per_scenario * len(scenarios))

        # Build generation plan: (scenario, count)
        plan: list[tuple[Scenario, int]] = []
        for i, scenario in enumerate(scenarios):
            count = base_per_scenario + (1 if i < remainder else 0)
            plan.append((scenario, count))

        # Shuffle plan for randomized generation order
        self.rng.shuffle(plan)

        # Modifier distribution for extra tags
        modifier_pool = [
            (0.05, ["panicked"]),
            (0.05, ["verbose"]),
            (0.03, ["prompt_injection"]),
            (0.04, ["conversation_history"]),
            (0.02, ["base64_content"]),
            (0.03, ["multilingual"]),
            (0.04, ["typos"]),
            (0.02, ["extremely_long"]),
            (0.02, ["minimal"]),
            (0.03, ["stack_trace"]),
            (0.02, ["auto_translated"]),
            (0.03, ["passive_aggressive"]),
            (0.03, ["corporate_jargon"]),
            (0.02, ["form_template"]),
            (0.04, ["email_signature"]),
        ]

        for scenario, count in plan:
            for i in range(count):
                # Determine extra tags
                extra_tags: list[str] = []
                for probability, tag_list in modifier_pool:
                    if self.rng.random() < probability:
                        extra_tags.extend(tag_list)

                # Force VIP ~5% of the time
                force_vip = self.rng.random() < 0.05

                # Vary subject and description indices
                subject_idx = i % len(scenario.subjects)
                desc_idx = i % len(scenario.descriptions)

                ticket, gold = self.generate_from_scenario(
                    scenario,
                    subject_idx=subject_idx,
                    desc_idx=desc_idx,
                    force_vip=force_vip,
                    extra_tags=extra_tags,
                )

                ticket_dict = {
                    "ticket_id": ticket.ticket_id,
                    "subject": ticket.subject,
                    "description": ticket.description,
                    "reporter": {
                        "name": ticket.reporter_name,
                        "email": ticket.reporter_email,
                        "department": ticket.reporter_department,
                    },
                    "created_at": ticket.created_at,
                    "channel": ticket.channel,
                    "attachments": ticket.attachments,
                }

                gold_dict = {
                    "ticket_id": gold.ticket_id,
                    "category": gold.category,
                    "priority": gold.priority,
                    "assigned_team": gold.assigned_team,
                    "needs_escalation": gold.needs_escalation,
                    "missing_information": gold.missing_information,
                    "next_best_action": gold.next_best_action,
                    "remediation_steps": gold.remediation_steps,
                }

                tickets.append(ticket_dict)
                golds.append(gold_dict)

        # Shuffle final order
        combined = list(zip(tickets, golds, strict=True))
        self.rng.shuffle(combined)
        tickets = [t for t, _ in combined]
        golds = [g for _, g in combined]

        # Re-assign sequential ticket IDs after shuffle
        self.ticket_counter = 2001
        for ticket, gold in zip(tickets, golds, strict=True):
            new_id = self._next_ticket_id()
            ticket["ticket_id"] = new_id
            gold["ticket_id"] = new_id

        return tickets, golds


def save_dataset(
    tickets: list[dict],
    golds: list[dict],
    tickets_path: Path,
    golds_path: Path,
) -> None:
    """Save generated dataset to JSON files."""
    tickets_path.write_text(json.dumps(tickets, indent=2, ensure_ascii=False) + "\n")
    golds_path.write_text(json.dumps(golds, indent=2, ensure_ascii=False) + "\n")


def print_statistics(
    tickets: list[dict],
    golds: list[dict],
) -> None:
    """Print dataset statistics for verification."""

    print(f"\n{'=' * 60}")
    print("  DATASET STATISTICS")
    print(f"{'=' * 60}\n")
    print(f"  Total tickets: {len(tickets)}")

    # Category distribution
    cat_counts = Counter(g["category"] for g in golds)
    print("\n  Category distribution:")
    for cat, count in sorted(cat_counts.items()):
        pct = count / len(golds) * 100
        print(f"    {cat:<30s} {count:4d}  ({pct:.1f}%)")

    # Priority distribution
    pri_counts = Counter(g["priority"] for g in golds)
    print("\n  Priority distribution:")
    for pri in ["P1", "P2", "P3", "P4"]:
        count = pri_counts.get(pri, 0)
        pct = count / len(golds) * 100
        print(f"    {pri:<10s} {count:4d}  ({pct:.1f}%)")

    # Team distribution
    team_counts = Counter(g["assigned_team"] for g in golds)
    print("\n  Team distribution:")
    for team, count in sorted(team_counts.items()):
        pct = count / len(golds) * 100
        print(f"    {team:<35s} {count:4d}  ({pct:.1f}%)")

    # Channel distribution
    ch_counts = Counter(t["channel"] for t in tickets)
    print("\n  Channel distribution:")
    for ch in CHANNELS:
        count = ch_counts.get(ch, 0)
        pct = count / len(tickets) * 100
        print(f"    {ch:<10s} {count:4d}  ({pct:.1f}%)")

    # Escalation distribution
    esc_true = sum(1 for g in golds if g["needs_escalation"])
    esc_false = len(golds) - esc_true
    print("\n  Escalation distribution:")
    print(f"    True:  {esc_true:4d}  ({esc_true / len(golds) * 100:.1f}%)")
    print(f"    False: {esc_false:4d}  ({esc_false / len(golds) * 100:.1f}%)")

    # Missing info vocabulary coverage
    all_missing = set()
    for g in golds:
        all_missing.update(g["missing_information"])
    print(f"\n  Missing info vocabulary coverage: {len(all_missing)}/16 values used")
    print(f"    Values: {sorted(all_missing)}")

    print(f"\n{'=' * 60}\n")

