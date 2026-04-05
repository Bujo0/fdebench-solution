# Copyright (c) Microsoft. All rights reserved.
"""Evaluation scenario model: a ticket paired with its expected gold answer and metadata."""

from typing import Literal

from ms.common.models.base import FrozenBaseModel
from ms.evals_core.models.ticket import Ticket
from ms.evals_core.models.triage_decision import TriageDecision

ScenarioCategory = Literal["data_cleanup", "responsible_ai"]


class Scenario(FrozenBaseModel):
    """A single evaluation scenario.

    Pairs an input ticket with its expected gold-standard triage decision,
    along with metadata describing what the scenario tests.
    """

    ticket: Ticket
    gold: TriageDecision
    scenario_category: ScenarioCategory
    scenario_tag: str
    description: str
