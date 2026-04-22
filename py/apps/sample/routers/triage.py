"""Triage router — POST /triage endpoint.

Architecture: LLM-only classification with minimal validation.
No preprocessing, no MI post-processing — let the model decide.
"""

import logging
import time

import state
from fastapi import APIRouter
from fastapi import Response
from models import Category
from models import Team
from models import TriageRequest
from models import TriageResponse
from prompts.triage_prompt import TRIAGE_SYSTEM_PROMPT
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
    t0 = time.time()

    try:
        desc = req.description[:4000] if req.description else ""
        attachments = getattr(req, "attachments", None) or []
        att_line = f"\nAttachments: {', '.join(attachments)}" if attachments else ""

        logger.info("T1 input: %s ch=%s dept=%s subj_len=%d desc_len=%d att=%d att_names=%s",
                     req.ticket_id, req.channel, req.reporter.department,
                     len(req.subject), len(desc), len(attachments),
                     ",".join(attachments)[:200] if attachments else "none")

        user_content = f"""<signal>
Subject: {req.subject}
Description: {desc}
Reporter: {req.reporter.name} ({req.reporter.department})
Channel: {req.channel}
Created: {req.created_at}{att_line}
</signal>"""

        routing_guide = state.ROUTING_GUIDE or ""
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
        llm_ms = int((time.time() - t0) * 1000)

        # Basic validation
        raw_cat = llm_result.category
        raw_team = llm_result.assigned_team
        category = match_category(raw_cat)
        team = match_team(raw_team)
        validated_team_str = validate_category_team(category.value, team.value)
        team_overridden = validated_team_str != team.value
        team = match_team(validated_team_str)

        priority = llm_result.priority if llm_result.priority in ("P1", "P2", "P3", "P4") else "P3"

        needs_escalation = llm_result.needs_escalation
        esc_override = "none"

        if priority == "P1":
            if not needs_escalation:
                esc_override = "P1_forced_true"
            needs_escalation = True

        if category == Category.THREAT:
            if not needs_escalation:
                esc_override = "Threat_forced_true"
            needs_escalation = True

        if category == Category.NOT_SIGNAL:
            if needs_escalation:
                esc_override = "NotSignal_forced_false"
            needs_escalation = False
            priority = "P4"

        missing = match_missing_info(llm_result.missing_information)
        mi_names = [m.value for m in missing]

        logger.info("T1 result: %s cat=%s pri=%s team=%s esc=%s mi=%s "
                     "team_override=%s esc_override=%s llm_ms=%d",
                     req.ticket_id, category.value, priority, team.value,
                     needs_escalation, ",".join(mi_names) if mi_names else "[]",
                     team_overridden, esc_override, llm_ms)

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
        elapsed_ms = int((time.time() - t0) * 1000)
        logger.exception("T1 FALLBACK: %s after %dms — using BRIEFING/P3/None",
                          req.ticket_id, elapsed_ms)
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
