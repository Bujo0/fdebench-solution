# Copyright (c) Microsoft. All rights reserved.
"""Input ticket model matching the docs/data/schemas/input.json schema."""

from enum import StrEnum

from ms.common.models.base import FrozenBaseModel


class Channel(StrEnum):
    """Ticket submission channel."""

    EMAIL = "email"
    CHAT = "chat"
    PORTAL = "portal"
    PHONE = "phone"


class Reporter(FrozenBaseModel):
    """The person who submitted the ticket."""

    name: str
    email: str
    department: str


class Ticket(FrozenBaseModel):
    """An IT support ticket submitted to Contoso Financial Services.

    Matches the input schema defined in docs/data/schemas/input.json.
    """

    ticket_id: str
    subject: str
    description: str
    reporter: Reporter
    created_at: str
    channel: Channel
    attachments: list[str] = []
