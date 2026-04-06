# Copyright (c) Microsoft. All rights reserved.
"""Shared fixtures for evals tests."""

from pathlib import Path

import pytest


@pytest.fixture
def data_dir() -> Path:
    """Path to the docs/data/tickets/ directory."""
    current = Path(__file__).resolve()
    for parent in current.parents:
        tickets_dir = parent / "docs" / "data" / "tickets"
        if tickets_dir.is_dir():
            return tickets_dir
    pytest.fail("Could not locate docs/data/tickets/ directory")
