# Copyright (c) Microsoft. All rights reserved.
"""Base scenario definition and builder for eval ticket generation."""

from ms.evals_core.constants import Category
from ms.evals_core.constants import Channel
from ms.evals_core.constants import MissingInfo
from ms.evals_core.constants import Priority
from ms.evals_core.constants import Team
from ms.evals_core.eval_models import EvalCase
from ms.evals_core.eval_models import EvalTicket
from ms.evals_core.eval_models import GoldAnswer
from ms.evals_core.eval_models import Reporter


class ScenarioDefinition:
    """Defines a complete ticket scenario with all parameters for generation."""

    def __init__(
        self,
        *,
        scenario_id: str,
        subject: str,
        description: str,
        category: Category,
        priority: Priority,
        team: Team,
        needs_escalation: bool,
        missing_info: list[MissingInfo],
        next_best_action: str,
        remediation_steps: list[str],
        reporter_name: str,
        reporter_email: str,
        reporter_department: str,
        channel: Channel,
        attachments: list[str] | None = None,
        created_at: str = "2026-03-18T09:00:00Z",
        tags: list[str] | None = None,
        difficulty: str = "medium",
    ) -> None:
        self.scenario_id = scenario_id
        self.subject = subject
        self.description = description
        self.category = category
        self.priority = priority
        self.team = team
        self.needs_escalation = needs_escalation
        self.missing_info = missing_info
        self.next_best_action = next_best_action
        self.remediation_steps = remediation_steps
        self.reporter_name = reporter_name
        self.reporter_email = reporter_email
        self.reporter_department = reporter_department
        self.channel = channel
        self.attachments = attachments or []
        self.created_at = created_at
        self.tags = tags or []
        self.difficulty = difficulty

    def to_eval_case(self, ticket_id: str) -> EvalCase:
        """Convert this definition to an EvalCase with the given ticket ID."""
        ticket = EvalTicket(
            ticket_id=ticket_id,
            subject=self.subject,
            description=self.description,
            reporter=Reporter(
                name=self.reporter_name,
                email=self.reporter_email,
                department=self.reporter_department,
            ),
            created_at=self.created_at,
            channel=self.channel,
            attachments=self.attachments,
        )
        gold = GoldAnswer(
            ticket_id=ticket_id,
            category=self.category,
            priority=self.priority,
            assigned_team=self.team,
            needs_escalation=self.needs_escalation,
            missing_information=self.missing_info,
            next_best_action=self.next_best_action,
            remediation_steps=self.remediation_steps,
        )
        return EvalCase(
            ticket=ticket,
            gold=gold,
            tags=self.tags,
            description=f"[{self.scenario_id}] {self.subject}",
        )
