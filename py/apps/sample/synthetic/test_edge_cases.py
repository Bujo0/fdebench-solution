#!/usr/bin/env python3
"""Test the rules engine against edge case signals and report accuracy."""

import json
import sys
from pathlib import Path

# Add the app to the path
app_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(app_dir.parent.parent.parent))  # py/ directory
sys.path.insert(0, str(app_dir))

from services.triage_rules import classify_by_rules

EDGE_CASES = app_dir / "synthetic" / "triage_edge_cases.json"
GOLD_LABELS = app_dir / "synthetic" / "triage_edge_cases_gold.json"


def main():
    with open(EDGE_CASES) as f:
        signals = json.load(f)
    with open(GOLD_LABELS) as f:
        golds = json.load(f)

    gold_map = {g["ticket_id"]: g for g in golds}

    # Track results per field and per category group
    fields = ["category", "priority", "assigned_team", "needs_escalation"]
    correct = {f: 0 for f in fields}
    total = len(signals)
    failures: list[dict] = []

    for sig in signals:
        tid = sig["ticket_id"]
        gold = gold_map[tid]

        result = classify_by_rules(
            subject=sig["subject"],
            description=sig["description"],
            reporter_dept=sig["reporter"]["department"],
            channel=sig["channel"],
        )

        predicted = {
            "category": result.category,
            "priority": result.priority,
            "assigned_team": result.team,
            "needs_escalation": result.needs_escalation,
        }

        ticket_failures = []
        for f in fields:
            if predicted[f] == gold[f]:
                correct[f] += 1
            else:
                ticket_failures.append({
                    "field": f,
                    "predicted": predicted[f],
                    "gold": gold[f],
                })

        if ticket_failures:
            failures.append({
                "ticket_id": tid,
                "subject": sig["subject"],
                "rationale": gold.get("rationale", ""),
                "errors": ticket_failures,
                "confidence": round(result.confidence, 3),
            })

    # Print summary
    print("=" * 72)
    print("EDGE CASE RULES ENGINE ACCURACY REPORT")
    print("=" * 72)
    print(f"\nTotal signals: {total}")
    print()

    for f in fields:
        pct = correct[f] / total * 100
        print(f"  {f:25s}  {correct[f]:2d}/{total}  ({pct:5.1f}%)")

    all_correct = total - len(failures)
    print(f"\n  {'ALL FIELDS CORRECT':25s}  {all_correct:2d}/{total}  ({all_correct/total*100:5.1f}%)")

    # Failures by category group
    groups = {
        "Category Confusion (EDGE-CAT-*)": [],
        "Priority Calibration (EDGE-PRI-*)": [],
        "Escalation Edge (EDGE-ESC-*)": [],
        "Missing Info Edge (EDGE-MIS-*)": [],
    }

    for fail in failures:
        tid = fail["ticket_id"]
        if tid.startswith("EDGE-CAT"):
            groups["Category Confusion (EDGE-CAT-*)"].append(fail)
        elif tid.startswith("EDGE-PRI"):
            groups["Priority Calibration (EDGE-PRI-*)"].append(fail)
        elif tid.startswith("EDGE-ESC"):
            groups["Escalation Edge (EDGE-ESC-*)"].append(fail)
        elif tid.startswith("EDGE-MIS"):
            groups["Missing Info Edge (EDGE-MIS-*)"].append(fail)

    print("\n" + "=" * 72)
    print("FAILURES BY CATEGORY GROUP")
    print("=" * 72)

    for group_name, group_failures in groups.items():
        prefix = group_name.split("(")[1].rstrip(")*").replace("*", "")
        group_total = sum(1 for s in signals if s["ticket_id"].startswith(prefix.rstrip("-")))
        group_correct = group_total - len(group_failures)
        print(f"\n── {group_name}: {group_correct}/{group_total} fully correct ──")

        if not group_failures:
            print("  ✓ All correct!")
            continue

        for fail in group_failures:
            print(f"\n  ✗ {fail['ticket_id']}: {fail['subject']}")
            print(f"    Confidence: {fail['confidence']}")
            for err in fail["errors"]:
                print(f"    {err['field']:25s}  predicted={err['predicted']!r:40s}  gold={err['gold']!r}")
            if fail["rationale"]:
                # Wrap rationale text
                rat = fail["rationale"]
                print(f"    Rationale: {rat[:100]}")
                if len(rat) > 100:
                    for i in range(100, len(rat), 100):
                        print(f"              {rat[i:i+100]}")

    print("\n" + "=" * 72)
    print("VULNERABILITY SUMMARY — Fields the hidden eval may exploit")
    print("=" * 72)

    # Collect unique vulnerability types
    vuln_types: dict[str, list[str]] = {}
    for fail in failures:
        for err in fail["errors"]:
            key = err["field"]
            vuln_types.setdefault(key, []).append(
                f"{fail['ticket_id']}: {err['predicted']!r} → {err['gold']!r}"
            )

    for field, examples in sorted(vuln_types.items(), key=lambda x: -len(x[1])):
        print(f"\n  {field} ({len(examples)} failures):")
        for ex in examples:
            print(f"    • {ex}")


if __name__ == "__main__":
    main()
