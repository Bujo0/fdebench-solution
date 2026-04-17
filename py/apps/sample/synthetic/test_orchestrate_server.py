#!/usr/bin/env python3
"""Test edge case scenarios against the running orchestrate server on port 8080."""

import json
import sys
from pathlib import Path

import httpx

SERVER = "http://localhost:8080"

# Standard tool definitions matching what the eval provides
TOOLS = [
    {"name": "crm_search", "description": "Search CRM", "endpoint": f"{SERVER}/mock/crm_search",
     "parameters": [{"name": "filter", "type": "string", "description": "filter", "required": True},
                    {"name": "limit", "type": "integer", "description": "limit", "required": False}]},
    {"name": "crm_get_account", "description": "Get account", "endpoint": f"{SERVER}/mock/crm_get_account",
     "parameters": [{"name": "account_id", "type": "string", "description": "account ID", "required": True}]},
    {"name": "subscription_check", "description": "Check subscription", "endpoint": f"{SERVER}/mock/subscription_check",
     "parameters": [{"name": "account_id", "type": "string", "description": "account ID", "required": True}]},
    {"name": "notification_send", "description": "Send notification", "endpoint": f"{SERVER}/mock/notification_send",
     "parameters": [{"name": "user_id", "type": "string", "description": "user", "required": True},
                    {"name": "channel", "type": "string", "description": "channel", "required": True},
                    {"name": "message", "type": "string", "description": "message", "required": True}]},
    {"name": "email_send", "description": "Send email", "endpoint": f"{SERVER}/mock/email_send",
     "parameters": [{"name": "account_id", "type": "string", "description": "account ID", "required": True},
                    {"name": "template", "type": "string", "description": "template", "required": True},
                    {"name": "subject", "type": "string", "description": "subject", "required": True}]},
    {"name": "calendar_check", "description": "Check calendar", "endpoint": f"{SERVER}/mock/calendar_check",
     "parameters": [{"name": "user_id", "type": "string", "description": "user", "required": True},
                    {"name": "start_date", "type": "string", "description": "start", "required": True},
                    {"name": "end_date", "type": "string", "description": "end", "required": True}]},
    {"name": "audit_log", "description": "Write audit log", "endpoint": f"{SERVER}/mock/audit_log",
     "parameters": [{"name": "action", "type": "string", "description": "action", "required": True},
                    {"name": "details", "type": "object", "description": "details", "required": False}]},
    {"name": "inventory_query", "description": "Query inventory", "endpoint": f"{SERVER}/mock/inventory_query",
     "parameters": [{"name": "sku", "type": "string", "description": "SKU", "required": True},
                    {"name": "warehouse", "type": "string", "description": "warehouse", "required": True}]},
]


def load_scenarios():
    path = Path(__file__).parent / "orchestrate_v2.json"
    with open(path) as f:
        return json.load(f)


def test_scenario(client: httpx.Client, scenario: dict, idx: int) -> dict:
    """Send a single scenario to the server and validate the response."""
    payload = {
        "task_id": f"synth-{idx:04d}",
        "goal": scenario["goal"],
        "available_tools": TOOLS,
        "constraints": ["Complete the workflow"],
    }

    try:
        resp = client.post(f"{SERVER}/orchestrate", json=payload, timeout=30.0)
        result = {
            "goal": scenario["goal"][:80],
            "expected_template": scenario.get("expected_template"),
            "edge_case": scenario.get("edge_case", ""),
            "status_code": resp.status_code,
        }

        if resp.status_code == 200:
            data = resp.json()
            result["response_status"] = data.get("status")
            result["steps_count"] = len(data.get("steps_executed", []))
            result["has_task_id"] = "task_id" in data
            result["has_status"] = "status" in data
            result["has_steps"] = "steps_executed" in data
            result["valid"] = (
                data.get("status") == "completed"
                and "task_id" in data
                and "steps_executed" in data
            )
        else:
            result["valid"] = False
            result["error"] = resp.text[:200]

        return result
    except Exception as e:
        return {
            "goal": scenario["goal"][:80],
            "expected_template": scenario.get("expected_template"),
            "status_code": 0,
            "valid": False,
            "error": str(e)[:200],
        }


def main():
    scenarios = load_scenarios()
    print(f"Testing {len(scenarios)} scenarios against {SERVER}/orchestrate\n")

    client = httpx.Client()
    results = []
    errors = []

    for i, s in enumerate(scenarios):
        r = test_scenario(client, s, i)
        results.append(r)
        status = "✓" if r["valid"] else "✗"
        ec = f" [{r.get('edge_case', '')}]" if r.get("edge_case") else ""
        if not r["valid"]:
            errors.append(r)
            print(f"  {status} [{i:3d}] HTTP {r['status_code']:3d} | {r['goal'][:60]}{ec}")
            if "error" in r:
                print(f"         Error: {r['error'][:100]}")

    client.close()

    # Summary
    valid_count = sum(1 for r in results if r["valid"])
    http_200 = sum(1 for r in results if r.get("status_code") == 200)
    completed = sum(1 for r in results if r.get("response_status") == "completed")
    http_500 = sum(1 for r in results if r.get("status_code") == 500)

    print(f"\n{'=' * 72}")
    print("SERVER TEST RESULTS")
    print("=" * 72)
    print(f"  Total scenarios:      {len(scenarios)}")
    print(f"  HTTP 200:             {http_200}/{len(scenarios)}")
    print(f"  HTTP 500:             {http_500}/{len(scenarios)}")
    print(f"  Status 'completed':   {completed}/{len(scenarios)}")
    print(f"  Valid responses:      {valid_count}/{len(scenarios)} ({valid_count/len(scenarios)*100:.1f}%)")

    if errors:
        print(f"\n  FAILURES ({len(errors)}):")
        for e in errors:
            ec = f" [{e.get('edge_case', '')}]" if e.get("edge_case") else ""
            print(f"    HTTP {e.get('status_code', '?')}: {e['goal'][:60]}{ec}")
    else:
        print("\n  ✓ All scenarios passed!")

    return len(errors)


if __name__ == "__main__":
    failures = main()
    sys.exit(1 if failures else 0)
