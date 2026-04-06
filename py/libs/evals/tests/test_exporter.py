# Copyright (c) Microsoft. All rights reserved.
"""Tests for the JSON exporter and scenario registry."""

import json
import tempfile
from pathlib import Path

from ms.evals_core.framework.exporter import export_category_to_json
from ms.evals_core.framework.models.scenario import ScenarioCategory
from ms.evals_core.framework.scenarios.registry import default_registry


def _ensure_scenarios_loaded() -> None:
    """Import scenario modules to trigger registration."""
    import ms.evals_core.framework.scenarios.data_cleanup  # noqa: F401, PLC0415
    import ms.evals_core.framework.scenarios.responsible_ai  # noqa: F401, PLC0415


def test_all_scenarios_registered() -> None:
    """Total scenarios should be the sum of data cleanup and responsible AI."""
    _ensure_scenarios_loaded()
    all_scenarios = default_registry.all()
    assert len(all_scenarios) > 0


def test_scenarios_sorted_by_id() -> None:
    """all() should return scenarios sorted by scenario_id."""
    _ensure_scenarios_loaded()
    all_scenarios = default_registry.all()
    ids = [s.scenario_id for s in all_scenarios]
    assert ids == sorted(ids)


def test_get_by_category_data_cleanup() -> None:
    """Filter by DATA_CLEANUP should return scenarios."""
    _ensure_scenarios_loaded()
    dc = default_registry.by_category(ScenarioCategory.DATA_CLEANUP)
    assert len(dc) > 0
    assert all(s.category == ScenarioCategory.DATA_CLEANUP for s in dc)


def test_get_by_category_responsible_ai() -> None:
    """Filter by RESPONSIBLE_AI should return scenarios."""
    _ensure_scenarios_loaded()
    rai = default_registry.by_category(ScenarioCategory.RESPONSIBLE_AI)
    assert len(rai) > 0
    assert all(s.category == ScenarioCategory.RESPONSIBLE_AI for s in rai)


def test_export_data_cleanup_json() -> None:
    """Export data cleanup scenarios to JSON and validate structure."""
    _ensure_scenarios_loaded()

    with tempfile.TemporaryDirectory() as tmpdir:
        tickets_path = Path(tmpdir) / "data_cleanup.json"
        gold_path = Path(tmpdir) / "data_cleanup_gold.json"

        count = export_category_to_json(ScenarioCategory.DATA_CLEANUP, tickets_path, gold_path)
        assert count > 0

        tickets = json.loads(tickets_path.read_text())
        gold = json.loads(gold_path.read_text())

        assert len(tickets) == count
        assert len(gold) == count

        for ticket in tickets:
            assert "ticket_id" in ticket
            assert "subject" in ticket
            assert "description" in ticket
            assert "reporter" in ticket
            assert "created_at" in ticket
            assert "channel" in ticket


def test_export_responsible_ai_json() -> None:
    """Export responsible AI scenarios to JSON and validate structure."""
    _ensure_scenarios_loaded()

    with tempfile.TemporaryDirectory() as tmpdir:
        tickets_path = Path(tmpdir) / "responsible_ai.json"
        gold_path = Path(tmpdir) / "responsible_ai_gold.json"

        count = export_category_to_json(ScenarioCategory.RESPONSIBLE_AI, tickets_path, gold_path)
        assert count > 0

        tickets = json.loads(tickets_path.read_text())
        gold = json.loads(gold_path.read_text())

        assert len(tickets) == count
        assert len(gold) == count


def test_ticket_ids_match_between_tickets_and_gold() -> None:
    """Ticket IDs in the tickets file should match those in the gold file."""
    _ensure_scenarios_loaded()

    with tempfile.TemporaryDirectory() as tmpdir:
        for category in ScenarioCategory:
            tickets_path = Path(tmpdir) / f"{category.value}.json"
            gold_path = Path(tmpdir) / f"{category.value}_gold.json"

            export_category_to_json(category, tickets_path, gold_path)

            tickets = json.loads(tickets_path.read_text())
            gold = json.loads(gold_path.read_text())

            ticket_ids = [t["ticket_id"] for t in tickets]
            gold_ids = [g["ticket_id"] for g in gold]
            assert ticket_ids == gold_ids
