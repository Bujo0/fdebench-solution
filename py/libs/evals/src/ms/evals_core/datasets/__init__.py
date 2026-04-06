# Copyright (c) Microsoft. All rights reserved.
"""Dataset loading for evaluation scenarios.

Each dataset is a pair of JSON files (tickets + gold answers) shipped alongside
the project in ``docs/data/tickets/``.  This module discovers them by kind and
returns validated Pydantic models.
"""

import json
from enum import StrEnum
from pathlib import Path

from ms.evals_core.eval_models import GoldAnswer
from ms.evals_core.eval_models import Ticket


# Resolve the ``docs/data/tickets/`` directory by finding the repository root.
def _find_repo_root() -> Path:
    """Walk up from this file to find the repo root (directory with ``.git``)."""
    current = Path(__file__).resolve()
    for parent in current.parents:
        if (parent / ".git").exists():
            return parent
    msg = "could not locate repository root (.git directory)"
    raise FileNotFoundError(msg)


_REPO_ROOT = _find_repo_root()
_TICKETS_DIR = _REPO_ROOT / "docs" / "data" / "tickets"


class DatasetKind(StrEnum):
    """Identifiers for the built-in evaluation datasets."""

    SAMPLE = "sample"
    PUBLIC_EVAL = "public_eval"
    DATA_CLEANUP = "eval_data_cleanup"
    RESPONSIBLE_AI = "eval_responsible_ai"


# Mapping from dataset kind to (tickets filename, gold filename | None).
_DATASET_FILES: dict[DatasetKind, tuple[str, str | None]] = {
    DatasetKind.SAMPLE: ("sample.json", "sample_gold.json"),
    DatasetKind.PUBLIC_EVAL: ("public_eval.json", None),
    DatasetKind.DATA_CLEANUP: ("eval_data_cleanup.json", "eval_data_cleanup_gold.json"),
    DatasetKind.RESPONSIBLE_AI: ("eval_responsible_ai.json", "eval_responsible_ai_gold.json"),
}


def load_dataset(
    kind: DatasetKind,
    *,
    tickets_dir: Path | None = None,
) -> tuple[list[Ticket], list[GoldAnswer] | None]:
    """Load an evaluation dataset by kind.

    Parameters
    ----------
    kind:
        Which dataset to load.
    tickets_dir:
        Override the directory where ticket JSON files are located.
        Defaults to ``docs/data/tickets/`` relative to the repository root.

    Returns
    -------
    tuple:
        A pair of ``(tickets, gold_answers)``.  ``gold_answers`` is ``None``
        for datasets that have no gold file (e.g. ``public_eval``).

    Raises
    ------
    FileNotFoundError:
        If the expected JSON files are missing.
    ValueError:
        If ``kind`` is not a recognised dataset.
    """
    base = tickets_dir or _TICKETS_DIR

    if kind not in _DATASET_FILES:
        msg = f"Unknown dataset kind: {kind!r}"
        raise ValueError(msg)

    tickets_file, gold_file = _DATASET_FILES[kind]

    tickets_path = base / tickets_file
    if not tickets_path.exists():
        msg = f"Tickets file not found: {tickets_path}"
        raise FileNotFoundError(msg)

    raw_tickets: list[dict] = json.loads(tickets_path.read_text(encoding="utf-8"))
    tickets = [Ticket.model_validate(t) for t in raw_tickets]

    gold_answers: list[GoldAnswer] | None = None
    if gold_file is not None:
        gold_path = base / gold_file
        if not gold_path.exists():
            msg = f"Gold file not found: {gold_path}"
            raise FileNotFoundError(msg)
        raw_gold: list[dict] = json.loads(gold_path.read_text(encoding="utf-8"))
        gold_answers = [GoldAnswer.model_validate(g) for g in raw_gold]

    return tickets, gold_answers
