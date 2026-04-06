# Copyright (c) Microsoft. All rights reserved.
"""Pydantic models for IT support ticket inputs."""

import re

from pydantic import field_validator

from ms.common.models.base import FrozenBaseModel
from ms.evals.constants import Channel


class TicketReporter(FrozenBaseModel):
    """Reporter metadata for an IT support ticket."""

    name: str
    email: str
    department: str


class TicketInput(FrozenBaseModel):
    """An IT support ticket submitted for triage.

    Matches the input schema defined in docs/data/schemas/input.json.
    """

    ticket_id: str
    subject: str
    description: str
    reporter: TicketReporter
    created_at: str
    channel: Channel
    attachments: list[str] = []

    @field_validator("ticket_id")
    @classmethod
    def validate_ticket_id(cls, v: str) -> str:
        if not re.match(r"^INC-\d+$", v):
            msg = f"ticket_id must match pattern INC-<digits>, got: {v}"
            raise ValueError(msg)
        return v
