"""Triage router — POST /triage endpoint.

Architecture: LLM-only classification with minimal validation.
No preprocessing, no MI post-processing — let the model decide.
"""

import logging

import state
from fastapi import APIRouter
from fastapi import Response
from models import Category
from models import Team
from models import TriageRequest
from models import TriageResponse
from prompts.triage_prompt import TRIAGE_SYSTEM_PROMPT
from prompts.triage_prompt import load_routing_guide
from services.triage_service import TriageLLMResponse
from services.triage_service import match_category
from services.triage_service import match_missing_info
from services.triage_service import match_team
from services.triage_service import validate_category_team
from llm_client import complete
from utils import display_model

logger = logging.getLogger(__name__)
router = APIRouter()

_LLM_MODEL = "gpt-5-4"


@router.post("/triage")
async def triage(req: TriageRequest, response: Response) -> TriageResponse:
    response.headers["X-Model-Name"] = display_model(_LLM_MODEL)

    try:
        # Truncate very long descriptions to prevent token limit errors
        desc = req.description[:4000] if req.description else ""
        attachments = getattr(req, "attachments", None) or []
        att_line = f"\nAttachments: {', '.join(attachments)}" if attachments else ""
        user_content = f"""<signal>
Subject: {req.subject}
Description: {desc}
Reporter: {req.reporter.name} ({req.reporter.department})
Channel: {req.channel}
Created: {req.created_at}{att_line}
</signal>"""

        routing_guide = load_routing_guide()
        full_prompt = TRIAGE_SYSTEM_PROMPT
        if routing_guide:
            full_prompt += "\n\nROUTING GUIDE:\n" + routing_guide

        llm_result = await complete(
            state.aoai_client,
            _LLM_MODEL,
            full_prompt,
            user_content,
            response_format=TriageLLMResponse,
        )

        # Basic validation
        category = match_category(llm_result.category)
        team = match_team(llm_result.assigned_team)
        validated_team_str = validate_category_team(category.value, team.value)
        team = match_team(validated_team_str)

        priority = llm_result.priority if llm_result.priority in ("P1", "P2", "P3", "P4") else "P3"

        needs_escalation = llm_result.needs_escalation

        # Always escalate P1
        if priority == "P1":
            needs_escalation = True

        # Always escalate Threat
        if category == Category.THREAT:
            needs_escalation = True

        # Never escalate non-incidents
        if category == Category.NOT_SIGNAL:
            needs_escalation = False

        # Non-incident priority override
        if category == Category.NOT_SIGNAL:
            priority = "P4"

        missing = match_missing_info(llm_result.missing_information)

        return TriageResponse(
            ticket_id=req.ticket_id,
            category=category,
            priority=priority,
            assigned_team=team,
            needs_escalation=needs_escalation,
            missing_information=missing,
            next_best_action="Investigate and resolve the reported issue.",
            remediation_steps=[
                "Review signal details.",
                "Route to assigned team.",
            ],
        )

    except Exception:
        logger.exception("Triage LLM error for %s — using fallback", req.ticket_id)
        return TriageResponse(
            ticket_id=req.ticket_id,
            category=Category.BRIEFING,
            priority="P3",
            assigned_team=Team.NONE,
            needs_escalation=False,
            missing_information=[],
            next_best_action="Investigate and resolve the reported issue.",
            remediation_steps=["Review signal details.", "Route to assigned team."],
        )
