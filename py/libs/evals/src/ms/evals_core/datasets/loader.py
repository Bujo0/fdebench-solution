# Copyright (c) Microsoft. All rights reserved.
"""Dataset loading and validation utilities.

Loads ticket datasets and gold answers from JSON files,
validates them against the Pydantic models, and provides
convenient access patterns for evaluation tests.
"""

import json
from pathlib import Path

from ms.common.models.base import FrozenBaseModel
from ms.evals_core.models.ticket_input import TicketInput
from ms.evals_core.models.triage_response import TriageResponse


class DatasetPair(FrozenBaseModel):
    """A matched pair of tickets and their gold-standard triage answers."""

    tickets: tuple[TicketInput, ...]
    golds: tuple[TriageResponse, ...]

    def get_ticket(self, ticket_id: str) -> TicketInput:
        """Retrieve a specific ticket by ID."""
        for ticket in self.tickets:
            if ticket.ticket_id == ticket_id:
                return ticket
        msg = f"ticket_id '{ticket_id}' not found in dataset"
        raise KeyError(msg)

    def get_gold(self, ticket_id: str) -> TriageResponse:
        """Retrieve a specific gold answer by ticket ID."""
        for gold in self.golds:
            if gold.ticket_id == ticket_id:
                return gold
        msg = f"ticket_id '{ticket_id}' not found in gold answers"
        raise KeyError(msg)


def load_tickets(path: Path) -> tuple[TicketInput, ...]:
    """Load and validate a ticket dataset from a JSON file."""
    raw = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, list):
        msg = f"expected a JSON array in {path}, got {type(raw).__name__}"
        raise TypeError(msg)
    return tuple(TicketInput.model_validate(item) for item in raw)


def load_golds(path: Path) -> tuple[TriageResponse, ...]:
    """Load and validate gold-standard answers from a JSON file."""
    raw = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, list):
        msg = f"expected a JSON array in {path}, got {type(raw).__name__}"
        raise TypeError(msg)
    return tuple(TriageResponse.model_validate(item) for item in raw)


def load_dataset_pair(tickets_path: Path, golds_path: Path) -> DatasetPair:
    """Load a matched ticket + gold answer dataset.

    Validates that every ticket has a corresponding gold answer and vice versa.
    """
    tickets = load_tickets(tickets_path)
    golds = load_golds(golds_path)

    ticket_ids = {t.ticket_id for t in tickets}
    gold_ids = {g.ticket_id for g in golds}

    missing_golds = ticket_ids - gold_ids
    if missing_golds:
        msg = f"tickets without gold answers: {sorted(missing_golds)}"
        raise ValueError(msg)

    extra_golds = gold_ids - ticket_ids
    if extra_golds:
        msg = f"gold answers without matching tickets: {sorted(extra_golds)}"
        raise ValueError(msg)

    return DatasetPair(tickets=tickets, golds=golds)


# Convenience: resolve paths relative to the project's docs/data/tickets/ directory
def _resolve_data_dir() -> Path:
    """Find the repo-root docs/data/tickets/ directory by walking up from this file.

    Identifies the repository root via a ``.git`` entry to avoid matching
    intermediate ``py/docs/data/tickets/`` directories.
    """
    current = Path(__file__).resolve()
    for parent in current.parents:
        if (parent / ".git").exists():
            tickets_dir = parent / "docs" / "data" / "tickets"
            if tickets_dir.is_dir():
                return tickets_dir
    msg = "could not locate docs/data/tickets/ under the repository root"
    raise FileNotFoundError(msg)


def load_data_cleanup_dataset() -> DatasetPair:
    """Load the data cleanup evaluation dataset."""
    data_dir = _resolve_data_dir()
    return load_dataset_pair(
        data_dir / "data_cleanup.json",
        data_dir / "data_cleanup_gold.json",
    )


def load_responsible_ai_dataset() -> DatasetPair:
    """Load the responsible AI evaluation dataset."""
    data_dir = _resolve_data_dir()
    return load_dataset_pair(
        data_dir / "responsible_ai.json",
        data_dir / "responsible_ai_gold.json",
    )
