# Copyright (c) Microsoft. All rights reserved.
"""Input ticket model matching docs/data/schemas/input.json."""

from ms.common.models.base import FrozenBaseModel
from ms.evals_core.constants import Channel


class Reporter(FrozenBaseModel):
    """Ticket reporter details."""

    name: str
    email: str
    department: str


class Ticket(FrozenBaseModel):
    """An IT support ticket submitted to Contoso Financial Services.

    Matches the JSON schema at docs/data/schemas/input.json.
    """

    ticket_id: str
    subject: str
    description: str
    reporter: Reporter
    created_at: str
    channel: Channel
    attachments: list[str] = []
