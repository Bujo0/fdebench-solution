#!/usr/bin/env python3
"""Generate eval dataset for IT ticket triage evaluation.

Usage:
    cd docs/eval
    python generate_evals.py --count 2500 --seed 42

Output:
    ../data/tickets/generated_eval.json
    ../data/tickets/generated_eval_gold.json
"""

import argparse
import json
import sys
from pathlib import Path

from generator.engine import TicketGenerator
from generator.engine import print_statistics
from generator.engine import save_dataset
from generator.models import Scenario
from generator.scenarios.access_auth import SCENARIOS as ACCESS_AUTH_SCENARIOS
from generator.scenarios.data_storage import SCENARIOS as DATA_STORAGE_SCENARIOS
from generator.scenarios.edge_cases import SCENARIOS as EDGE_CASE_SCENARIOS
from generator.scenarios.financial_services import SCENARIOS as FINANCIAL_SERVICES_SCENARIOS
from generator.scenarios.general_inquiry import SCENARIOS as GENERAL_INQUIRY_SCENARIOS
from generator.scenarios.hardware import SCENARIOS as HARDWARE_SCENARIOS
from generator.scenarios.low_priority import SCENARIOS as LOW_PRIORITY_SCENARIOS
from generator.scenarios.network import SCENARIOS as NETWORK_SCENARIOS
from generator.scenarios.not_a_ticket import SCENARIOS as NOT_A_TICKET_SCENARIOS
from generator.scenarios.responsible_ai import SCENARIOS as RESPONSIBLE_AI_SCENARIOS
from generator.scenarios.security import SCENARIOS as SECURITY_SCENARIOS
from generator.scenarios.software import SCENARIOS as SOFTWARE_SCENARIOS
from generator.validator import validate_dataset


def collect_all_scenarios() -> list[Scenario]:
    """Collect all scenarios from all category modules."""
    all_scenarios: list[Scenario] = []
    all_scenarios.extend(ACCESS_AUTH_SCENARIOS)
    all_scenarios.extend(HARDWARE_SCENARIOS)
    all_scenarios.extend(NETWORK_SCENARIOS)
    all_scenarios.extend(SOFTWARE_SCENARIOS)
    all_scenarios.extend(SECURITY_SCENARIOS)
    all_scenarios.extend(DATA_STORAGE_SCENARIOS)
    all_scenarios.extend(GENERAL_INQUIRY_SCENARIOS)
    all_scenarios.extend(NOT_A_TICKET_SCENARIOS)
    all_scenarios.extend(EDGE_CASE_SCENARIOS)
    all_scenarios.extend(FINANCIAL_SERVICES_SCENARIOS)
    all_scenarios.extend(LOW_PRIORITY_SCENARIOS)
    all_scenarios.extend(RESPONSIBLE_AI_SCENARIOS)
    return all_scenarios


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate eval dataset for IT ticket triage.")
    parser.add_argument(
        "--count",
        type=int,
        default=2500,
        help="Target number of tickets to generate (default: 2500)",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Random seed for reproducibility (default: 42)",
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default=None,
        help="Output directory (default: ../data/tickets/)",
    )
    parser.add_argument(
        "--validate-only",
        action="store_true",
        help="Only validate existing generated files",
    )
    args = parser.parse_args()

    # Resolve output directory
    output_dir = Path(args.output_dir) if args.output_dir else Path(__file__).parent.parent / "data" / "tickets"

    tickets_path = output_dir / "eval_generated.json"
    golds_path = output_dir / "eval_generated_gold.json"

    if args.validate_only:
        if not tickets_path.exists() or not golds_path.exists():
            print("Error: generated files not found for validation")
            return 1
        tickets = json.loads(tickets_path.read_text())
        golds = json.loads(golds_path.read_text())
        errors = validate_dataset(tickets, golds)
        if errors:
            print(f"Validation FAILED with {len(errors)} errors:")
            for err in errors[:20]:
                print(f"  ✗ {err}")
            if len(errors) > 20:
                print(f"  ... and {len(errors) - 20} more errors")
            return 1
        print(f"Validation PASSED: {len(tickets)} tickets, {len(golds)} gold answers")
        print_statistics(tickets, golds)
        return 0

    # Collect all scenarios
    all_scenarios = collect_all_scenarios()
    print(f"Loaded {len(all_scenarios)} unique scenarios across all categories")

    # Check for duplicate scenario IDs
    ids = [s.scenario_id for s in all_scenarios]
    dupes = [sid for sid in ids if ids.count(sid) > 1]
    if dupes:
        print(f"Warning: duplicate scenario IDs found: {set(dupes)}")

    # Generate
    generator = TicketGenerator(seed=args.seed)
    print(f"Generating {args.count} tickets with seed={args.seed}...")

    tickets, golds = generator.generate_dataset(all_scenarios, target_count=args.count)

    # Validate
    errors = validate_dataset(tickets, golds)
    if errors:
        print(f"\nValidation FAILED with {len(errors)} errors:")
        for err in errors[:20]:
            print(f"  ✗ {err}")
        if len(errors) > 20:
            print(f"  ... and {len(errors) - 20} more errors")
        print("\nFix validation errors before saving.")
        return 1

    print("Validation PASSED")

    # Save
    output_dir.mkdir(parents=True, exist_ok=True)
    save_dataset(tickets, golds, tickets_path, golds_path)
    print(f"\nSaved {len(tickets)} tickets to {tickets_path}")
    print(f"Saved {len(golds)} gold answers to {golds_path}")

    # Print statistics
    print_statistics(tickets, golds)

    return 0


if __name__ == "__main__":
    sys.exit(main())
