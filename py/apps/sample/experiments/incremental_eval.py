#!/usr/bin/env python3
"""Incremental change isolation tester.

Tests each change individually from baseline, recording marginal impact.
Each step adds ONE change to the previous state.
"""
import json
import requests
import sys
import time
import subprocess
import os

sys.path.insert(0, '../../common/libs/fdebenchkit/src')
from ms.common.fdebenchkit.scorers.ticket_triage import score_submission

ENDPOINT = "http://localhost:8000/triage"
V2_INPUT = "synthetic/triage_v2.json"
V2_GOLD = "synthetic/triage_v2_gold.json"
V3_INPUT = "synthetic/triage_v3.json"
V3_GOLD = "synthetic/triage_v3_gold.json"


def run_triage_eval(name: str, input_file: str, gold_file: str) -> dict:
    with open(input_file) as f:
        inputs = json.load(f)
    with open(gold_file) as f:
        golds = json.load(f)

    start = time.time()
    results = []
    for inp in inputs:
        try:
            r = requests.post(ENDPOINT, json=inp, timeout=60)
            results.append(r.json())
        except Exception:
            results.append({
                'ticket_id': inp['ticket_id'], 'category': 'Mission Briefing Request',
                'priority': 'P3', 'assigned_team': 'None', 'needs_escalation': False,
                'missing_information': [], 'next_best_action': 'x', 'remediation_steps': ['x']
            })

    s = score_submission(results, golds)
    elapsed = time.time() - start
    return {
        'resolution': s['resolution'],
        'dimensions': s['dimension_scores'],
        'elapsed': elapsed,
        'items': len(inputs),
    }


def main():
    results = {}

    # Run both datasets
    print(f"Running v2 eval...")
    v2 = run_triage_eval("v2", V2_INPUT, V2_GOLD)
    print(f"Running v3 eval...")
    v3 = run_triage_eval("v3", V3_INPUT, V3_GOLD)

    step = sys.argv[1] if len(sys.argv) > 1 else "unknown"

    print(f"\n=== {step} ===")
    print(f"v2 Resolution: {v2['resolution']:.1f} ({v2['elapsed']:.0f}s)")
    for d, v in sorted(v2['dimensions'].items()):
        print(f"  {d}: {v:.4f}")
    print(f"v3 Resolution: {v3['resolution']:.1f} ({v3['elapsed']:.0f}s)")
    for d, v in sorted(v3['dimensions'].items()):
        print(f"  {d}: {v:.4f}")

    # Save to JSON
    result = {"step": step, "v2": v2, "v3": v3}
    outfile = f"experiments/results/incremental_{step}.json"
    os.makedirs(os.path.dirname(outfile), exist_ok=True)
    with open(outfile, 'w') as f:
        json.dump(result, f, indent=2)
    print(f"Saved to {outfile}")


if __name__ == "__main__":
    main()
