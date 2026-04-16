"""Triage router — POST /triage endpoint."""

import logging

from fastapi import APIRouter, Response

from llm_client import complete
from models import Category, Team, TriageRequest, TriageResponse
from prompts.triage_prompt import TRIAGE_SYSTEM_PROMPT
from services.triage_service import (
    TriageLLMResponse,
    match_category,
    match_missing_info,
    match_team,
    validate_category_team,
)
from utils import display_model

import state

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/triage")
async def triage(req: TriageRequest, response: Response) -> TriageResponse:
    model = state.settings.triage_model
    response.headers["X-Model-Name"] = display_model(model)

    try:
        user_content = f"""<signal>
Subject: {req.subject}
Description: {req.description[:800]}
Reporter: {req.reporter.name} ({req.reporter.department})
Channel: {req.channel}
</signal>"""

        full_system_prompt = TRIAGE_SYSTEM_PROMPT
        if state.FEW_SHOT_EXAMPLES:
            full_system_prompt += "\n\nFEW-SHOT EXAMPLES:\n" + state.FEW_SHOT_EXAMPLES

        result = await complete(
            state.aoai_client,
            model,
            full_system_prompt,
            user_content,
            response_format=TriageLLMResponse,
        )

        category = match_category(result.category)
        team = match_team(result.assigned_team)
        validated_team_str = validate_category_team(category.value, team.value)
        team = match_team(validated_team_str)
        priority = result.priority if result.priority in ("P1", "P2", "P3", "P4") else "P3"
        missing = match_missing_info(result.missing_information)

        needs_escalation = result.needs_escalation
        if priority == "P1":
            needs_escalation = True
        if category == Category.THREAT:
            needs_escalation = True

        return TriageResponse(
            ticket_id=req.ticket_id,
            category=category,
            priority=priority,
            assigned_team=team,
            needs_escalation=needs_escalation,
            missing_information=missing,
            next_best_action=result.next_best_action or "Investigate the reported issue.",
            remediation_steps=result.remediation_steps or ["Review the signal details."],
        )
    except Exception:
        logger.exception("Triage LLM error for %s", req.ticket_id)
        return TriageResponse(
            ticket_id=req.ticket_id,
            category=Category.BRIEFING,
            priority="P3",
            assigned_team=Team.NONE,
            needs_escalation=False,
            missing_information=[],
            next_best_action="Investigate the reported issue.",
            remediation_steps=["Review the signal details."],
        )
