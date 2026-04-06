# Copyright (c) Microsoft. All rights reserved.
"""CLI entry point for running evaluations via ``python -m ms.evals``.

Delegates to the ``ms.evals_core`` runner CLI which drives ``EvalRunner``
against a live triage endpoint.

Usage::

    cd py
    uv run python -m ms.evals --endpoint http://localhost:8000 --dataset eval_data_cleanup
    uv run python -m ms.evals --endpoint http://localhost:8000 --dataset eval_responsible_ai
    uv run python -m ms.evals --endpoint http://localhost:8000 --dataset sample
"""

import sys

from ms.evals_core.runner_cli import main

if __name__ == "__main__":
    sys.exit(main())
