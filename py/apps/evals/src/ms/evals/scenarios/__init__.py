# Copyright (c) Microsoft. All rights reserved.
"""Scenario package - provides all IT support ticket scenario templates."""

import importlib


def load_all_scenarios() -> None:
    """Import all scenario modules to trigger their registry side effects."""
    _scenario_modules = [
        "ms.evals.scenarios.access_auth",
        "ms.evals.scenarios.data_storage",
        "ms.evals.scenarios.general_inquiry",
        "ms.evals.scenarios.hardware",
        "ms.evals.scenarios.low_priority",
        "ms.evals.scenarios.network",
        "ms.evals.scenarios.not_support",
        "ms.evals.scenarios.security",
        "ms.evals.scenarios.software",
    ]
    for mod in _scenario_modules:
        importlib.import_module(mod)
