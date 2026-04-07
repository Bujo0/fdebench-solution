# Copyright (c) Microsoft. All rights reserved.
"""Dataset exporter for evaluation scenarios.

Converts scenario (TicketInput, TriageDecision) pairs into JSON files
compatible with the run_eval.py evaluation harness.
"""

import json
from pathlib import Path

from ms.eval.models import TicketInput
from ms.eval.models import TriageDecision


def export_dataset(
    scenarios: list[tuple[TicketInput, TriageDecision]],
    tickets_path: Path,
    gold_path: Path,
) -> None:
    """Export scenarios to ticket and gold JSON files.

    Args:
        scenarios: List of (TicketInput, TriageDecision) pairs.
        tickets_path: Output path for the ticket dataset JSON.
        gold_path: Output path for the gold answers JSON.
    """
    tickets = [ticket.model_dump() for ticket, _ in scenarios]
    golds = [gold.model_dump() for _, gold in scenarios]

    tickets_path.parent.mkdir(parents=True, exist_ok=True)
    gold_path.parent.mkdir(parents=True, exist_ok=True)

    tickets_path.write_text(json.dumps(tickets, indent=2, ensure_ascii=False))
    gold_path.write_text(json.dumps(golds, indent=2, ensure_ascii=False))
