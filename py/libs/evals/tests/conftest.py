# Copyright (c) Microsoft. All rights reserved.
"""Shared fixtures for evaluation tests."""

import pytest
from evals.scenarios.data_cleanup import build_data_cleanup_suite
from evals.scenarios.responsible_ai import build_responsible_ai_suite


@pytest.fixture(scope="session")
def data_cleanup_suite():
    """Build the data cleanup scenario suite once per session."""
    return build_data_cleanup_suite()


@pytest.fixture(scope="session")
def responsible_ai_suite():
    """Build the responsible AI scenario suite once per session."""
    return build_responsible_ai_suite()
