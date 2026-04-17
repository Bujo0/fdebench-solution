"""Triage router — POST /triage endpoint.

Architecture: rules-first fast path, LLM fallback for low-confidence cases.
~95% of requests are handled by deterministic rules (<10ms).
"""

import logging

import state
from fastapi import APIRouter
from fastapi import Response
from llm_client import complete
from models import Category
from models import MissingInfo
from models import Team
from models import TriageRequest
from models import TriageResponse
from prompts.triage_prompt import TRIAGE_SYSTEM_PROMPT
from services.triage_rules import classify_by_rules
from services.triage_service import TriageLLMResponse
from services.triage_service import match_category
from services.triage_service import match_missing_info
from services.triage_service import match_team
from services.triage_service import validate_category_team
from utils import display_model

logger = logging.getLogger(__name__)
router = APIRouter()

# Confidence threshold: above this → use rules (skip LLM)
_RULES_CONFIDENCE_THRESHOLD = 0.85


def _safe_missing_info(items: list[str]) -> list[MissingInfo]:
    """Convert raw strings to MissingInfo enums, dropping invalid values."""
    valid = {m.value for m in MissingInfo}
    return [MissingInfo(v) for v in items if v in valid]


@router.post("/triage")
async def triage(req: TriageRequest, response: Response) -> TriageResponse:
    model = state.settings.triage_model
    response.headers["X-Model-Name"] = display_model(model)

    # ── Fast path: deterministic rules (<10ms) ──
    rules_result = classify_by_rules(
        req.subject,
        req.description,
        req.reporter.department,
        req.channel,
    )

    if rules_result.confidence >= _RULES_CONFIDENCE_THRESHOLD:
        logger.info(
            "Rules fast-path for %s: %s/%s (conf=%.2f)",
            req.ticket_id,
            rules_result.category,
            rules_result.priority,
            rules_result.confidence,
        )
        return TriageResponse(
            ticket_id=req.ticket_id,
            category=Category(rules_result.category),
            priority=rules_result.priority,
            assigned_team=Team(rules_result.team),
            needs_escalation=rules_result.needs_escalation,
            missing_information=_safe_missing_info(rules_result.missing_information),
            next_best_action="Investigate and resolve the reported issue.",
            remediation_steps=[
                "Review signal details and gather additional context.",
                "Route to assigned team for resolution.",
            ],
        )

    # ── Slow path: LLM fallback (use full model for best accuracy) ──
    fallback_model = "gpt-5-4"  # Stronger model for ambiguous items
    logger.info(
        "LLM fallback for %s (rules conf=%.2f) using %s",
        req.ticket_id,
        rules_result.confidence,
        fallback_model,
    )
    try:
        user_content = f"""<signal>
Subject: {req.subject}
Description: {req.description[:800]}
Reporter: {req.reporter.name} ({req.reporter.department})
Channel: {req.channel}
</signal>"""

        full_system_prompt = TRIAGE_SYSTEM_PROMPT
        if state.ROUTING_GUIDE:
            full_system_prompt += "\n\nROUTING REFERENCE:\n" + state.ROUTING_GUIDE

        result = await complete(
            state.aoai_client,
            fallback_model,
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
        # De-escalation: exploratory/uncertain signals should not escalate
        desc_lower = req.description.lower()
        subj_lower = req.subject.lower()
        if (
            ("may be nothing" in desc_lower or "may be nothing" in subj_lower)
            and priority != "P1"
            and category != Category.THREAT
        ):
            needs_escalation = False

        return TriageResponse(
            ticket_id=req.ticket_id,
            category=category,
            priority=priority,
            assigned_team=team,
            needs_escalation=needs_escalation,
            missing_information=missing,
            next_best_action="Investigate and resolve the reported issue.",
            remediation_steps=[
                "Review signal details and gather additional context.",
                "Route to assigned team for resolution.",
            ],
        )
    except Exception:
        logger.exception("Triage LLM error for %s — using rules fallback", req.ticket_id)
        # Use rules result as ultimate fallback (better than hardcoded defaults)
        return TriageResponse(
            ticket_id=req.ticket_id,
            category=Category(rules_result.category),
            priority=rules_result.priority,
            assigned_team=Team(rules_result.team),
            needs_escalation=rules_result.needs_escalation,
            missing_information=_safe_missing_info(rules_result.missing_information),
            next_best_action="Investigate the reported issue.",
            remediation_steps=["Review the signal details."],
        )
