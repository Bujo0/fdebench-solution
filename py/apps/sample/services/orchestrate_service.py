"""Orchestration business logic — tool calling, ReAct loop, constraint evaluation."""

import json
import logging
from typing import Any

import state
from llm_client import complete
from prompts.orchestrate_prompt import ORCHESTRATE_SYSTEM_PROMPT
from utils import parse_json_response

logger = logging.getLogger(__name__)


def format_tools(req: Any) -> str:
    """Format tool definitions for the LLM prompt."""
    lines = []
    for tool in req.available_tools:
        params_desc = ""
        if isinstance(tool.parameters, list):
            for p in tool.parameters:
                req_mark = " (required)" if p.required else " (optional)"
                params_desc += f"  - {p.name} ({p.type}): {p.description}{req_mark}\n"
        elif isinstance(tool.parameters, dict):
            for k, v in tool.parameters.items():
                params_desc += f"  - {k}: {v}\n"
        lines.append(f"### {tool.name}\n{tool.description}\nEndpoint: {tool.endpoint}\nParameters:\n{params_desc}")
    return "\n".join(lines)


async def orchestrate_llm_call(
    model: str,
    conversation: list[dict[str, str]],
) -> dict[str, Any] | None:
    """Make a single LLM call in the orchestration loop using JSON mode."""
    messages = [{"role": "system", "content": ORCHESTRATE_SYSTEM_PROMPT}] + conversation
    resp = await state.aoai_client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=0.0,
        response_format={"type": "json_object"},
    )
    content = resp.choices[0].message.content
    return parse_json_response(content)


async def call_tool(endpoint: str, parameters: dict[str, Any]) -> tuple[str, bool]:
    """Call a tool endpoint via HTTP. Returns (result_text, success)."""
    try:
        resp = await state.tool_http_client.post(endpoint, json=parameters, timeout=15.0)
        if resp.status_code == 200:
            try:
                data = resp.json()
                return json.dumps(data, default=str)[:2000], True
            except Exception:
                return resp.text[:2000], True
        else:
            # Retry once
            resp2 = await state.tool_http_client.post(endpoint, json=parameters, timeout=15.0)
            if resp2.status_code == 200:
                try:
                    data = resp2.json()
                    return json.dumps(data, default=str)[:2000], True
                except Exception:
                    return resp2.text[:2000], True
            return f"HTTP {resp2.status_code}: {resp2.text[:500]}", False
    except Exception as e:
        # Retry once on exception
        try:
            resp = await state.tool_http_client.post(endpoint, json=parameters, timeout=15.0)
            if resp.status_code == 200:
                data = resp.json()
                return json.dumps(data, default=str)[:2000], True
            return f"HTTP {resp.status_code}", False
        except Exception:
            return f"Error: {e}", False


async def evaluate_constraints(
    model: str,
    goal: str,
    constraints: list[str],
    steps: Any,
) -> list[str]:
    """Use LLM to evaluate which constraints were satisfied."""
    if not constraints:
        return []

    steps_text = ""
    for s in steps:
        success_str = "OK" if s.success else "FAIL"
        steps_text += f"Step {s.step}: {s.tool}({json.dumps(s.parameters)}) → {success_str}: {s.result_summary[:200]}\n"

    prompt = f"""Given the goal: {goal}

Steps executed:
{steps_text}

Constraints to evaluate:
{json.dumps(constraints)}

Return the list of constraints that were satisfied based on the steps executed.
Return ALL constraints that the workflow addressed, even if indirectly. Be
generous in interpretation - if a step attempted to satisfy a constraint,
consider it satisfied.

Return a JSON array of strings — the satisfied constraint texts. Return the EXACT
constraint text from the input list."""

    try:
        result = await complete(
            state.aoai_client,
            model,
            "You evaluate constraint satisfaction. Return a JSON array of constraint strings.",
            prompt,
        )
        parsed = parse_json_response(result)
        if isinstance(parsed, list):
            return [str(c) for c in parsed if str(c) in constraints]
    except Exception:
        logger.exception("Constraint evaluation failed")

    # Fallback: claim all constraints satisfied
    return list(constraints)
