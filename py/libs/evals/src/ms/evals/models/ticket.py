# Copyright (c) Microsoft. All rights reserved.
"""Pydantic models for IT support ticket input.

Mirrors the input schema at docs/data/schemas/input.json.
"""

from typing import Literal

from ms.common.models.base import FrozenBaseModel


class TicketReporter(FrozenBaseModel):
    """Reporter information attached to a support ticket."""

    name: str
    email: str
    department: str


class Ticket(FrozenBaseModel):
    """An IT support ticket submitted to the triage API.

    Matches the input schema: ticket_id, subject, description, reporter,
    created_at, channel, and optional attachments.
    """

    ticket_id: str
    subject: str
    description: str
    reporter: TicketReporter
    created_at: str
    channel: Literal["email", "chat", "portal", "phone"]
    attachments: list[str] = []
