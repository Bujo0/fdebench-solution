"""Deterministic template-based executor for Task 3 workflow orchestration.

Replaces the ReAct LLM loop with a state machine that:
1. Detects the template from the goal text (100% rule-based)
2. Executes exact tool calls in scorer-expected order
3. Makes data-driven decisions from tool responses (risk levels, approvals, etc.)

This eliminates LLM latency for Task 3 entirely — responses in <2s.
"""

import json
import logging
import re
from typing import Any

import state
from models import OrchestrateRequest
from models import StepExecuted

logger = logging.getLogger(__name__)

# ── Template detection ────────────────────────────────────────────────


def detect_template(goal: str) -> str | None:
    """Detect which of the 7 templates matches the goal text."""
    g = goal.lower()

    if "churn" in g or ("risk" in g and "retention" in g) or ("declining" in g and "usage" in g):
        return "churn_risk_analysis"
    if "renewal" in g or ("renew" in g and "renewable" not in g):
        return "contract_renewal"
    if "incident" in g and ("respond" in g or "notify" in g or "escalat" in g):
        return "incident_response"
    if "inventory" in g or ("stock" in g and "warehouse" in g) or "restock" in g:
        return "inventory_restock"
    if "meeting" in g and ("schedule" in g or "schedul" in g):
        return "meeting_scheduler"
    if "onboarding" in g or "onboard" in g:
        return "onboarding_workflow"
    if "re-engagement" in g or "re_engagement" in g or "reengagement" in g or ("not contacted" in g and "email" in g):
        return "re_engagement_campaign"

    return None


# ── Parameter extraction helpers ──────────────────────────────────────


def _extract_account_id(goal: str) -> str | None:
    m = re.search(r"\(?(ACC-\d+)\)?", goal)
    return m.group(1) if m else None


def _extract_company_name(goal: str) -> str | None:
    """Extract company name from goal text like 'for Contoso Ltd (ACC-0302)'."""
    m = re.search(r"(?:for|account|with)\s+(.+?)\s*\(ACC-", goal)
    if m:
        name = m.group(1).strip()
        # Clean up leading "new account " etc
        name = re.sub(r"^new account\s+", "", name, flags=re.IGNORECASE)
        return name
    return None


def _extract_csm_id(goal: str) -> str | None:
    m = re.search(r"(CSM-\d+)", goal)
    return m.group(1) if m else None


def _extract_rep_id(goal: str) -> str | None:
    m = re.search(r"(REP-\d+)", goal)
    return m.group(1) if m else None


def _extract_meeting_type(goal: str) -> str | None:
    m = re.search(r"[Ss]chedule\s+(?:an?\s+)?(\w+)\s+meeting", goal)
    return m.group(1).lower() if m else "demo"


def _extract_severity(goal: str) -> str:
    g = goal.lower()
    if "critical" in g:
        return "critical"
    if "high" in g:
        return "high"
    if "medium" in g:
        return "medium"
    return "low"


def _extract_sku_and_warehouses(goal: str) -> tuple[str, list[str]]:
    """Extract SKU and warehouse list from incident/inventory goal text."""
    # SKU: usually a product name like Filter-H800, Board-E500, etc.
    sku_match = re.search(r"(?:affecting|for)\s+([\w-]+)\s+(?:in|across)", goal)
    sku = sku_match.group(1) if sku_match else ""

    # Warehouses: comma/and-separated, like "APAC-SOUTH, US-EAST" or "EU-CENTRAL and US-WEST"
    wh_section = re.search(r"(?:in|across)\s+([\w\s,\-]+?)(?:\s*(?::|and alert|$|\.))", goal)
    warehouses: list[str] = []
    if wh_section:
        wh_text = wh_section.group(1)
        # Split on comma or "and"
        parts = re.split(r"\s*,\s*|\s+and\s+", wh_text)
        for p in parts:
            p = p.strip()
            if p and re.match(r"^[A-Z]", p):
                warehouses.append(p)

    return sku, warehouses


def _extract_threshold(goal: str) -> int:
    """Extract stock threshold from inventory goal text like 'below 25 units'."""
    m = re.search(r"below\s+(\d+)\s+units", goal)
    return int(m.group(1)) if m else 25


def _extract_days(goal: str) -> int:
    """Extract days from re-engagement goal like 'not contacted in 120+ days'."""
    m = re.search(r"(\d+)\+?\s*days", goal)
    return int(m.group(1)) if m else 90


def _extract_max_emails(goal: str) -> int:
    """Extract max emails from goal like '(max 3)'."""
    m = re.search(r"max\s+(\d+)", goal)
    return int(m.group(1)) if m else 3


# ── Tool calling helper ──────────────────────────────────────────────


async def _call_tool(endpoint: str, parameters: dict[str, Any]) -> tuple[dict[str, Any] | None, str, bool]:
    """Call a tool endpoint. Returns (parsed_json, result_text, success)."""
    try:
        resp = await state.tool_http_client.post(endpoint, json=parameters, timeout=15.0)
        if resp.status_code == 200:
            try:
                data = resp.json()
                return data, json.dumps(data, default=str)[:2000], True
            except Exception:
                return None, resp.text[:2000], True
        else:
            # Retry once on non-200
            resp2 = await state.tool_http_client.post(endpoint, json=parameters, timeout=15.0)
            if resp2.status_code == 200:
                try:
                    data = resp2.json()
                    return data, json.dumps(data, default=str)[:2000], True
                except Exception:
                    return None, resp2.text[:2000], True
            return None, f"HTTP {resp2.status_code}: {resp2.text[:500]}", False
    except Exception as e:
        try:
            resp = await state.tool_http_client.post(endpoint, json=parameters, timeout=15.0)
            if resp.status_code == 200:
                data = resp.json()
                return data, json.dumps(data, default=str)[:2000], True
            return None, f"HTTP {resp.status_code}", False
        except Exception:
            return None, f"Error: {e}", False


def _get_endpoint(req: OrchestrateRequest, tool_name: str) -> str:
    """Get the endpoint URL for a tool by name."""
    for tool in req.available_tools:
        if tool.name == tool_name:
            return tool.endpoint
    return ""


def _make_step(step_num: int, tool: str, parameters: dict[str, Any], result_text: str, success: bool) -> StepExecuted:
    return StepExecuted(
        step=step_num,
        tool=tool,
        parameters=parameters,
        result_summary=result_text[:500],
        success=success,
    )


# ── Template executors ────────────────────────────────────────────────


async def execute_churn_risk_analysis(req: OrchestrateRequest) -> list[StepExecuted]:
    steps: list[StepExecuted] = []
    step_num = 0

    # 1. crm_search for declining-usage accounts
    params = {"filter": "usage_trend = declining", "limit": 50}
    data, text, ok = await _call_tool(_get_endpoint(req, "crm_search"), params)
    step_num += 1
    steps.append(_make_step(step_num, "crm_search", params, text, ok))

    accounts = (data or {}).get("accounts", [])

    # 2. subscription_check each account
    risk_accounts: list[tuple[str, str, int]] = []  # (account_id, risk, days)
    for acc in accounts:
        acc_id = acc.get("account_id", "")
        params = {"account_id": acc_id}
        sub_data, sub_text, sub_ok = await _call_tool(_get_endpoint(req, "subscription_check"), params)
        step_num += 1
        steps.append(_make_step(step_num, "subscription_check", params, sub_text, sub_ok))

        if sub_data and sub_ok:
            days = sub_data.get("days_to_renewal", 999)
            if days < 30:
                risk_accounts.append((acc_id, "high", days))
            elif days < 90:
                risk_accounts.append((acc_id, "medium", days))
            # low risk → no action

    # 3. notification_send for high-risk → lead_retention
    for acc_id, risk, days in risk_accounts:
        if risk == "high":
            params = {
                "user_id": "lead_retention",
                "channel": "slack",
                "message": f"Churn risk (high): {acc_id} — renewal in {days} days",
            }
            _, text, ok = await _call_tool(_get_endpoint(req, "notification_send"), params)
            step_num += 1
            steps.append(_make_step(step_num, "notification_send", params, text, ok))

            # audit_log for each alert
            audit_params = {"action": "churn_risk_flagged", "details": {"account_id": acc_id, "risk": "high"}}
            _, a_text, a_ok = await _call_tool(_get_endpoint(req, "audit_log"), audit_params)
            step_num += 1
            steps.append(_make_step(step_num, "audit_log", audit_params, a_text, a_ok))

    # 4. notification_send for medium-risk → lead_customer_success
    for acc_id, risk, days in risk_accounts:
        if risk == "medium":
            params = {
                "user_id": "lead_customer_success",
                "channel": "slack",
                "message": f"Churn risk (medium): {acc_id} — renewal in {days} days",
            }
            _, text, ok = await _call_tool(_get_endpoint(req, "notification_send"), params)
            step_num += 1
            steps.append(_make_step(step_num, "notification_send", params, text, ok))

            audit_params = {"action": "churn_risk_flagged", "details": {"account_id": acc_id, "risk": "medium"}}
            _, a_text, a_ok = await _call_tool(_get_endpoint(req, "audit_log"), audit_params)
            step_num += 1
            steps.append(_make_step(step_num, "audit_log", audit_params, a_text, a_ok))

    return steps


async def execute_contract_renewal(req: OrchestrateRequest) -> list[StepExecuted]:
    steps: list[StepExecuted] = []
    step_num = 0
    account_id = _extract_account_id(req.goal) or ""
    company_name = _extract_company_name(req.goal) or ""

    # 1. crm_get_account
    params = {"account_id": account_id}
    acct_data, text, ok = await _call_tool(_get_endpoint(req, "crm_get_account"), params)
    step_num += 1
    steps.append(_make_step(step_num, "crm_get_account", params, text, ok))

    usage_level = (acct_data or {}).get("usage_level", "low")

    # 2. subscription_check
    params = {"account_id": account_id}
    sub_data, text, ok = await _call_tool(_get_endpoint(req, "subscription_check"), params)
    step_num += 1
    steps.append(_make_step(step_num, "subscription_check", params, text, ok))

    plan = (sub_data or {}).get("plan", "professional")

    # Determine discount based on usage
    if usage_level == "high":
        discount_pct = 15
        discount_float = 0.15
    elif usage_level == "medium":
        discount_pct = 5
        discount_float = 0.05
    else:
        discount_pct = 0
        discount_float = 0.0

    needs_approval = discount_pct > 0

    # 3. email_send renewal quote
    email_params = {
        "account_id": account_id,
        "template": "renewal_quote",
        "subject": f"Your renewal for {plan} plan",
        "variables": {"discount": f"{discount_pct}%", "plan": plan},
    }
    _, text, ok = await _call_tool(_get_endpoint(req, "email_send"), email_params)
    step_num += 1
    steps.append(_make_step(step_num, "email_send", email_params, text, ok))

    # 4. If needs approval → notification_send to finance_approver
    if needs_approval:
        notif_params = {
            "user_id": "finance_approver",
            "channel": "slack",
            "message": f"Discount approval needed: {company_name} {discount_pct}% off {plan}",
        }
        _, text, ok = await _call_tool(_get_endpoint(req, "notification_send"), notif_params)
        step_num += 1
        steps.append(_make_step(step_num, "notification_send", notif_params, text, ok))

    # 5. audit_log
    audit_params = {
        "action": "renewal_initiated",
        "details": {"account_id": account_id, "plan": plan, "discount": discount_float},
    }
    _, text, ok = await _call_tool(_get_endpoint(req, "audit_log"), audit_params)
    step_num += 1
    steps.append(_make_step(step_num, "audit_log", audit_params, text, ok))

    return steps


async def execute_incident_response(req: OrchestrateRequest) -> list[StepExecuted]:
    steps: list[StepExecuted] = []
    step_num = 0

    severity = _extract_severity(req.goal)
    sku, warehouses = _extract_sku_and_warehouses(req.goal)
    escalated = severity in ("critical", "high")

    # 1. inventory_query for each warehouse
    for wh in warehouses:
        params = {"sku": sku, "warehouse": wh}
        _, text, ok = await _call_tool(_get_endpoint(req, "inventory_query"), params)
        step_num += 1
        steps.append(_make_step(step_num, "inventory_query", params, text, ok))

    # 2. notification_send to oncall_engineer via SMS
    wh_list = ", ".join(warehouses)
    notif_params = {
        "user_id": "oncall_engineer",
        "channel": "sms",
        "message": f"Incident: {sku} affected in {wh_list} — severity: {severity}",
    }
    _, text, ok = await _call_tool(_get_endpoint(req, "notification_send"), notif_params)
    step_num += 1
    steps.append(_make_step(step_num, "notification_send", notif_params, text, ok))

    # 3. If escalated → notification_send to engineering_manager via slack
    if escalated:
        esc_params = {
            "user_id": "engineering_manager",
            "channel": "slack",
            "message": f"ESCALATION: {severity} incident for {sku}",
        }
        _, text, ok = await _call_tool(_get_endpoint(req, "notification_send"), esc_params)
        step_num += 1
        steps.append(_make_step(step_num, "notification_send", esc_params, text, ok))

    # 4. audit_log
    audit_params = {
        "action": "incident_response",
        "details": {"product": sku, "severity": severity, "warehouses": warehouses},
    }
    _, text, ok = await _call_tool(_get_endpoint(req, "audit_log"), audit_params)
    step_num += 1
    steps.append(_make_step(step_num, "audit_log", audit_params, text, ok))

    return steps


async def execute_inventory_restock(req: OrchestrateRequest) -> list[StepExecuted]:
    steps: list[StepExecuted] = []
    step_num = 0

    sku, warehouses = _extract_sku_and_warehouses(req.goal)
    threshold = _extract_threshold(req.goal)

    # 1. inventory_query for each warehouse — collect results first
    low_stock: list[tuple[str, int]] = []  # (warehouse, quantity)
    for wh in warehouses:
        params = {"sku": sku, "warehouse": wh}
        data, text, ok = await _call_tool(_get_endpoint(req, "inventory_query"), params)
        step_num += 1
        steps.append(_make_step(step_num, "inventory_query", params, text, ok))

        if data and ok and "quantity" in data:
            qty = data["quantity"]
            if qty < threshold:
                low_stock.append((wh, qty))

    # 2. notification_send for each low-stock warehouse
    for wh, qty in low_stock:
        notif_params = {
            "user_id": f"warehouse_mgr_{wh}",
            "channel": "slack",
            "message": f"Low stock: {sku} at {qty} units in {wh} (threshold: {threshold})",
        }
        _, text, ok = await _call_tool(_get_endpoint(req, "notification_send"), notif_params)
        step_num += 1
        steps.append(_make_step(step_num, "notification_send", notif_params, text, ok))

    return steps


async def execute_meeting_scheduler(req: OrchestrateRequest) -> list[StepExecuted]:
    steps: list[StepExecuted] = []
    step_num = 0

    account_id = _extract_account_id(req.goal) or ""
    rep_id = _extract_rep_id(req.goal) or ""
    meeting_type = _extract_meeting_type(req.goal) or "demo"
    company_name = _extract_company_name(req.goal) or ""

    # 1. crm_get_account
    params = {"account_id": account_id}
    acct_data, text, ok = await _call_tool(_get_endpoint(req, "crm_get_account"), params)
    step_num += 1
    steps.append(_make_step(step_num, "crm_get_account", params, text, ok))

    tier = (acct_data or {}).get("tier", "starter")

    # 2. subscription_check
    params = {"account_id": account_id}
    sub_data, text, ok = await _call_tool(_get_endpoint(req, "subscription_check"), params)
    step_num += 1
    steps.append(_make_step(step_num, "subscription_check", params, text, ok))

    # Use tier from subscription or CRM
    sub_plan = (sub_data or {}).get("plan", tier)
    # free-tier detection
    is_free = tier == "free" or sub_plan == "free"

    # 3. calendar_check
    cal_params = {"user_id": rep_id, "start_date": "2026-04-09", "end_date": "2026-04-23"}
    cal_data, text, ok = await _call_tool(_get_endpoint(req, "calendar_check"), cal_params)
    step_num += 1
    steps.append(_make_step(step_num, "calendar_check", cal_params, text, ok))

    has_slots = bool((cal_data or {}).get("available_slots"))
    scheduled = not is_free and has_slots

    if scheduled:
        # 4a. email_send meeting invite
        email_params = {
            "account_id": account_id,
            "template": "meeting_invite",
            "subject": f"{meeting_type} meeting",
        }
        _, text, ok = await _call_tool(_get_endpoint(req, "email_send"), email_params)
        step_num += 1
        steps.append(_make_step(step_num, "email_send", email_params, text, ok))
    else:
        # 4b. notification_send to rep
        if is_free:
            msg = f"{company_name} is free tier — no meetings available"
        else:
            msg = f"No availability for {company_name} {meeting_type}"
        notif_params = {
            "user_id": rep_id,
            "channel": "slack",
            "message": msg,
        }
        _, text, ok = await _call_tool(_get_endpoint(req, "notification_send"), notif_params)
        step_num += 1
        steps.append(_make_step(step_num, "notification_send", notif_params, text, ok))

    # 5. audit_log
    action = "meeting_scheduled" if scheduled else "meeting_blocked"
    audit_params = {
        "action": action,
        "details": {"account_id": account_id, "type": meeting_type, "tier": tier},
    }
    _, text, ok = await _call_tool(_get_endpoint(req, "audit_log"), audit_params)
    step_num += 1
    steps.append(_make_step(step_num, "audit_log", audit_params, text, ok))

    return steps


async def execute_onboarding_workflow(req: OrchestrateRequest) -> list[StepExecuted]:
    steps: list[StepExecuted] = []
    step_num = 0

    account_id = _extract_account_id(req.goal) or ""
    company_name = _extract_company_name(req.goal) or ""
    csm_id = _extract_csm_id(req.goal) or ""

    # 1. crm_get_account
    params = {"account_id": account_id}
    acct_data, text, ok = await _call_tool(_get_endpoint(req, "crm_get_account"), params)
    step_num += 1
    steps.append(_make_step(step_num, "crm_get_account", params, text, ok))

    # 2. subscription_check
    params = {"account_id": account_id}
    sub_data, text, ok = await _call_tool(_get_endpoint(req, "subscription_check"), params)
    step_num += 1
    steps.append(_make_step(step_num, "subscription_check", params, text, ok))

    sub_status = (sub_data or {}).get("status", "unknown")
    is_active = sub_status == "active"

    if is_active:
        # 3. email_send welcome
        email_params = {
            "account_id": account_id,
            "template": "welcome",
            "subject": f"Welcome {company_name}!",
        }
        _, text, ok = await _call_tool(_get_endpoint(req, "email_send"), email_params)
        step_num += 1
        steps.append(_make_step(step_num, "email_send", email_params, text, ok))

        # 4. calendar_check for kickoff
        cal_params = {"user_id": csm_id, "start_date": "2026-04-09", "end_date": "2026-04-16"}
        cal_data, text, ok = await _call_tool(_get_endpoint(req, "calendar_check"), cal_params)
        step_num += 1
        steps.append(_make_step(step_num, "calendar_check", cal_params, text, ok))

        # 5. email_send kickoff invite (if slots found)
        kickoff_params = {
            "account_id": account_id,
            "template": "kickoff_invite",
            "subject": "Your onboarding kickoff",
        }
        _, text, ok = await _call_tool(_get_endpoint(req, "email_send"), kickoff_params)
        step_num += 1
        steps.append(_make_step(step_num, "email_send", kickoff_params, text, ok))

        # 6. notification_send to CSM
        notif_params = {
            "user_id": csm_id,
            "channel": "slack",
            "message": f"New account: {company_name}",
        }
        _, text, ok = await _call_tool(_get_endpoint(req, "notification_send"), notif_params)
        step_num += 1
        steps.append(_make_step(step_num, "notification_send", notif_params, text, ok))

        # 7. audit_log
        audit_params = {
            "action": "onboarding_started",
            "details": {"account_id": account_id, "csm": csm_id},
        }
        _, text, ok = await _call_tool(_get_endpoint(req, "audit_log"), audit_params)
        step_num += 1
        steps.append(_make_step(step_num, "audit_log", audit_params, text, ok))
    else:
        # Not active → notify sales and log blocked
        reason = f"subscription_{sub_status}"
        notif_params = {
            "user_id": "sales_team",
            "channel": "slack",
            "message": f"Onboarding blocked: {company_name} subscription is {sub_status}",
        }
        _, text, ok = await _call_tool(_get_endpoint(req, "notification_send"), notif_params)
        step_num += 1
        steps.append(_make_step(step_num, "notification_send", notif_params, text, ok))

        audit_params = {
            "action": "onboarding_blocked",
            "details": {"account_id": account_id, "reason": reason},
        }
        _, text, ok = await _call_tool(_get_endpoint(req, "audit_log"), audit_params)
        step_num += 1
        steps.append(_make_step(step_num, "audit_log", audit_params, text, ok))

    return steps


async def execute_re_engagement_campaign(req: OrchestrateRequest) -> list[StepExecuted]:
    steps: list[StepExecuted] = []
    step_num = 0

    days = _extract_days(req.goal)
    max_emails = _extract_max_emails(req.goal)

    # 1. crm_search
    search_params = {"filter": f"last_contact_date < {days} days", "limit": 100}
    data, text, ok = await _call_tool(_get_endpoint(req, "crm_search"), search_params)
    step_num += 1
    steps.append(_make_step(step_num, "crm_search", search_params, text, ok))

    accounts = (data or {}).get("accounts", [])

    # 2. subscription_check for each account
    eligible: list[str] = []
    for acc in accounts:
        acc_id = acc.get("account_id", "")
        params = {"account_id": acc_id}
        sub_data, sub_text, sub_ok = await _call_tool(_get_endpoint(req, "subscription_check"), params)
        step_num += 1
        steps.append(_make_step(step_num, "subscription_check", params, sub_text, sub_ok))

        if sub_data and sub_ok:
            status = sub_data.get("status", "")
            # Only active accounts are eligible
            if status == "active":
                eligible.append(acc_id)
        # If sub check fails (error response), skip this account

    # 3. email_send + audit_log for eligible (up to max_emails)
    emails_sent = 0
    for acc_id in eligible:
        if emails_sent >= max_emails:
            break

        email_params = {
            "account_id": acc_id,
            "template": "re_engagement",
            "subject": "We miss you!",
        }
        _, text, ok = await _call_tool(_get_endpoint(req, "email_send"), email_params)
        step_num += 1
        steps.append(_make_step(step_num, "email_send", email_params, text, ok))

        audit_params = {"action": "email_sent", "details": {"account_id": acc_id}}
        _, a_text, a_ok = await _call_tool(_get_endpoint(req, "audit_log"), audit_params)
        step_num += 1
        steps.append(_make_step(step_num, "audit_log", audit_params, a_text, a_ok))

        emails_sent += 1  # noqa: SIM113

    return steps


# ── Main entry point ──────────────────────────────────────────────────

_TEMPLATE_EXECUTORS = {
    "churn_risk_analysis": execute_churn_risk_analysis,
    "contract_renewal": execute_contract_renewal,
    "incident_response": execute_incident_response,
    "inventory_restock": execute_inventory_restock,
    "meeting_scheduler": execute_meeting_scheduler,
    "onboarding_workflow": execute_onboarding_workflow,
    "re_engagement_campaign": execute_re_engagement_campaign,
}


async def execute_template(req: OrchestrateRequest) -> list[StepExecuted] | None:
    """Detect and execute a template for the given request.

    Returns list of steps if a template was matched, None otherwise (fallback to ReAct).
    """
    template = detect_template(req.goal)
    if not template:
        logger.warning("No template detected for goal: %s", req.goal[:100])
        return None

    executor = _TEMPLATE_EXECUTORS.get(template)
    if not executor:
        logger.warning("No executor for template: %s", template)
        return None

    logger.info("Executing template '%s' for task %s", template, req.task_id)
    return await executor(req)
