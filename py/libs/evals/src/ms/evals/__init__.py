# Copyright (c) Microsoft. All rights reserved.
"""Evaluation framework for IT ticket triage systems.

Provides evaluation datasets and scoring for:
- Data cleanup edge cases (noisy, malformed, oversized inputs)
- Responsible AI scenarios (prompt injection, jailbreaks, social engineering)
"""

from ms.evals.datasets import DatasetKind
from ms.evals.datasets import load_dataset
from ms.evals.models import EvalResult
from ms.evals.models import EvalSummary
from ms.evals.models import GoldAnswer
from ms.evals.models import Ticket
from ms.evals.models import TriageResponse
from ms.evals.runner import EvalRunner

__all__ = [
    "DatasetKind",
    "EvalResult",
    "EvalRunner",
    "EvalSummary",
    "GoldAnswer",
    "Ticket",
    "TriageResponse",
    "load_dataset",
]
