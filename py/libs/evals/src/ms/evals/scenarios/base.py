# Copyright (c) Microsoft. All rights reserved.
"""Evaluation scenario model.

An EvalScenario bundles a synthetic test ticket with its expected gold
triage answer and metadata about what the scenario is designed to test.
"""

from ms.common.models.base import FrozenBaseModel
from ms.evals.models.ticket import Ticket
from ms.evals.models.triage import TriageResponse


class EvalScenario(FrozenBaseModel):
    """A single evaluation test case.

    Pairs a ticket input with the expected gold triage output,
    plus metadata describing the scenario's purpose and category.
    """

    scenario_id: str
    category: str
    description: str
    ticket: Ticket
    expected: TriageResponse
