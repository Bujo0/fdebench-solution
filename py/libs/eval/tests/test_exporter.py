# Copyright (c) Microsoft. All rights reserved.
"""Tests for the dataset exporter.

Verifies that scenario pairs can be exported to JSON files compatible
with the run_eval.py evaluation harness.
"""

import json
from pathlib import Path

from ms.eval.exporter import export_dataset
from ms.eval.scenarios.data_cleanup import get_all_data_cleanup_scenarios
from ms.eval.scenarios.responsible_ai import get_all_responsible_ai_scenarios


class TestExportDataset:
    """Verify JSON export produces valid harness-compatible files."""

    def test_export_data_cleanup(self, tmp_path: Path) -> None:
        scenarios = get_all_data_cleanup_scenarios()
        tickets_path = tmp_path / "tickets.json"
        gold_path = tmp_path / "gold.json"

        export_dataset(scenarios, tickets_path, gold_path)

        tickets = json.loads(tickets_path.read_text())
        golds = json.loads(gold_path.read_text())

        assert len(tickets) == len(scenarios)
        assert len(golds) == len(scenarios)

        for ticket in tickets:
            assert "ticket_id" in ticket
            assert "subject" in ticket
            assert "description" in ticket
            assert "reporter" in ticket
            assert "channel" in ticket

        for gold in golds:
            assert "ticket_id" in gold
            assert "category" in gold
            assert "priority" in gold
            assert "assigned_team" in gold
            assert "needs_escalation" in gold
            assert "missing_information" in gold

    def test_export_responsible_ai(self, tmp_path: Path) -> None:
        scenarios = get_all_responsible_ai_scenarios()
        tickets_path = tmp_path / "tickets.json"
        gold_path = tmp_path / "gold.json"

        export_dataset(scenarios, tickets_path, gold_path)

        tickets = json.loads(tickets_path.read_text())
        golds = json.loads(gold_path.read_text())

        assert len(tickets) == len(scenarios)
        assert len(golds) == len(scenarios)

    def test_ticket_ids_match_between_files(self, tmp_path: Path) -> None:
        scenarios = get_all_data_cleanup_scenarios() + get_all_responsible_ai_scenarios()
        tickets_path = tmp_path / "tickets.json"
        gold_path = tmp_path / "gold.json"

        export_dataset(scenarios, tickets_path, gold_path)

        tickets = json.loads(tickets_path.read_text())
        golds = json.loads(gold_path.read_text())

        ticket_ids = [t["ticket_id"] for t in tickets]
        gold_ids = [g["ticket_id"] for g in golds]
        assert ticket_ids == gold_ids

    def test_creates_parent_directories(self, tmp_path: Path) -> None:
        tickets_path = tmp_path / "nested" / "dir" / "tickets.json"
        gold_path = tmp_path / "nested" / "dir" / "gold.json"

        export_dataset(get_all_data_cleanup_scenarios(), tickets_path, gold_path)

        assert tickets_path.exists()
        assert gold_path.exists()

    def test_unicode_preserved(self, tmp_path: Path) -> None:
        """Verify unicode characters survive JSON serialization."""
        scenarios = get_all_data_cleanup_scenarios()
        tickets_path = tmp_path / "tickets.json"
        gold_path = tmp_path / "gold.json"

        export_dataset(scenarios, tickets_path, gold_path)

        raw = tickets_path.read_text(encoding="utf-8")
        tickets = json.loads(raw)

        # The mixed languages scenario contains Chinese characters
        mixed_lang = next(t for t in tickets if t["ticket_id"] == "INC-DC-0010")
        assert any("\u4e00" <= c <= "\u9fff" for c in mixed_lang["description"])
