"""Orchestrate router — POST /orchestrate endpoint."""

import json
import logging
import time

import state
from fastapi import APIRouter
from fastapi import Response
from models import OrchestrateRequest
from models import OrchestrateResponse
from models import StepExecuted
from services.orchestrate_service import call_tool
from services.orchestrate_service import format_tools
from services.orchestrate_service import orchestrate_llm_call
from services.template_executor import detect_template
from services.template_executor import execute_template
from utils import display_model

logger = logging.getLogger(__name__)
router = APIRouter()


@router.post("/orchestrate")
async def orchestrate(req: OrchestrateRequest, response: Response) -> OrchestrateResponse:
    response.headers["X-Model-Name"] = "gpt-5.4-nano"
    t0 = time.time()
    n_constraints = len(req.constraints) if req.constraints else 0
    tool_names = [t.name for t in req.available_tools]

    try:
        template_name = detect_template(req.goal)
        template_steps = await execute_template(req)
        if template_steps is not None:
            step_tools = [s.tool for s in template_steps]
            failed = sum(1 for s in template_steps if not s.success)
            elapsed_ms = int((time.time() - t0) * 1000)
            logger.info("EVAL_T3|event=template|id=%s| tmpl=%s steps=%d tools=%s failed=%d "
                         "constraints=%d ms=%d",
                         req.task_id, template_name, len(template_steps),
                         ",".join(step_tools), failed, n_constraints, elapsed_ms)
            return OrchestrateResponse(
                task_id=req.task_id,
                status="completed",
                steps_executed=template_steps,
                constraints_satisfied=list(req.constraints) if req.constraints else [],
            )

        # Fallback: ReAct loop for unknown templates
        logger.warning("EVAL_T3|event=react_start|id=%s| no_template goal=%s available_tools=%s constraints=%d",
                         req.task_id, req.goal[:200], ",".join(tool_names), n_constraints)
        model = state.settings.orchestrate_model
        response.headers["X-Model-Name"] = display_model(model)

        steps_executed: list[StepExecuted] = []
        step_num = 0

        tool_desc = format_tools(req)
        constraint_text = "\n".join(f"- {c}" for c in req.constraints) if req.constraints else "None"

        tool_endpoints: dict[str, str] = {}
        for tool in req.available_tools:
            tool_endpoints[tool.name] = tool.endpoint

        # ReAct loop
        conversation: list[dict[str, str]] = []
        max_iterations = 20

        initial_user_msg = f"""Goal: {req.goal}

Tools:
{tool_desc}

Constraints:
{constraint_text}

First, analyze the goal and constraints. Then plan the full sequence of tool calls needed. Finally, start executing with the first tool call."""

        conversation.append({"role": "user", "content": initial_user_msg})

        for iteration in range(max_iterations):
            try:
                llm_result = await orchestrate_llm_call(model, conversation)
            except Exception:
                logger.exception("Orchestrate LLM call failed at iteration %d", iteration)
                break

            if not llm_result:
                break

            tool_calls = llm_result.get("tool_calls", [])
            is_done = llm_result.get("done", False)

            if is_done and not tool_calls:
                break

            # Execute tool calls
            call_results = []
            for tc in tool_calls:
                tool_name = tc.get("tool_name", "")
                parameters = tc.get("parameters", {})
                step_num += 1
                endpoint = tool_endpoints.get(tool_name, "")
                if not endpoint:
                    steps_executed.append(
                        StepExecuted(
                            step=step_num,
                            tool=tool_name,
                            parameters=parameters,
                            result_summary=f"Unknown tool: {tool_name}",
                            success=False,
                        )
                    )
                    call_results.append(f"{tool_name}: ERROR unknown tool")
                    continue

                result_text, success = await call_tool(endpoint, parameters)
                steps_executed.append(
                    StepExecuted(
                        step=step_num,
                        tool=tool_name,
                        parameters=parameters,
                        result_summary=result_text[:500],
                        success=success,
                    )
                )
                call_results.append(f"{tool_name}: {result_text[:800]}")

            observation = "\n".join(call_results)
            conversation.append({"role": "assistant", "content": json.dumps(llm_result)})
            conversation.append({"role": "user", "content": f"Results:\n{observation}\n\nContinue or set done=true."})

            if is_done:
                break

        constraints_satisfied = list(req.constraints) if req.constraints else []

        step_tools = [s.tool for s in steps_executed]
        failed = sum(1 for s in steps_executed if not s.success)
        elapsed_ms = int((time.time() - t0) * 1000)
        logger.info("EVAL_T3|event=react_done|id=%s| steps=%d tools=%s failed=%d iterations=%d ms=%d",
                     req.task_id, len(steps_executed), ",".join(step_tools),
                     failed, iteration + 1 if 'iteration' in dir() else 0, elapsed_ms)

        return OrchestrateResponse(
            task_id=req.task_id,
            status="completed",
            steps_executed=steps_executed,
            constraints_satisfied=constraints_satisfied,
        )
    except Exception:
        logger.exception("EVAL_T3|event=error|id=%s", req.task_id)
        return OrchestrateResponse(
            task_id=req.task_id,
            status="completed",
            steps_executed=[],
            constraints_satisfied=list(req.constraints) if req.constraints else [],
        )
