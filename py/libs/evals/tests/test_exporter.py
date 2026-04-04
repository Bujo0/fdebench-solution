"""Tests for the scenario exporter."""

import json
import tempfile
from pathlib import Path

from ms.libs.evals.exporter import export_scenario_metadata, export_scenarios_to_json
from ms.libs.evals.models.enums import ScenarioTag
from ms.libs.evals.registry import get_all_scenarios, get_scenarios_by_tag


class TestExporter:
    def test_export_produces_valid_json(self) -> None:
        scenarios = get_all_scenarios()
        with tempfile.TemporaryDirectory() as tmpdir:
            tickets_path = Path(tmpdir) / "tickets.json"
            gold_path = Path(tmpdir) / "gold.json"

            export_scenarios_to_json(scenarios, tickets_path, gold_path)

            tickets = json.loads(tickets_path.read_text())
            golds = json.loads(gold_path.read_text())

            assert len(tickets) == len(scenarios)
            assert len(golds) == len(scenarios)

    def test_exported_tickets_have_required_fields(self) -> None:
        scenarios = get_all_scenarios()
        with tempfile.TemporaryDirectory() as tmpdir:
            tickets_path = Path(tmpdir) / "tickets.json"
            gold_path = Path(tmpdir) / "gold.json"

            export_scenarios_to_json(scenarios, tickets_path, gold_path)

            tickets = json.loads(tickets_path.read_text())
            required_fields = {"ticket_id", "subject", "description", "reporter", "created_at", "channel"}
            for ticket in tickets:
                assert required_fields.issubset(ticket.keys()), (
                    f"Ticket {ticket.get('ticket_id')} missing required fields"
                )

    def test_exported_golds_have_required_fields(self) -> None:
        scenarios = get_all_scenarios()
        with tempfile.TemporaryDirectory() as tmpdir:
            tickets_path = Path(tmpdir) / "tickets.json"
            gold_path = Path(tmpdir) / "gold.json"

            export_scenarios_to_json(scenarios, tickets_path, gold_path)

            golds = json.loads(gold_path.read_text())
            required_fields = {
                "ticket_id", "category", "priority", "assigned_team",
                "needs_escalation", "missing_information", "next_best_action",
                "remediation_steps",
            }
            for gold in golds:
                assert required_fields.issubset(gold.keys()), (
                    f"Gold {gold.get('ticket_id')} missing required fields"
                )

    def test_ticket_ids_match_between_files(self) -> None:
        scenarios = get_all_scenarios()
        with tempfile.TemporaryDirectory() as tmpdir:
            tickets_path = Path(tmpdir) / "tickets.json"
            gold_path = Path(tmpdir) / "gold.json"

            export_scenarios_to_json(scenarios, tickets_path, gold_path)

            tickets = json.loads(tickets_path.read_text())
            golds = json.loads(gold_path.read_text())

            ticket_ids = [t["ticket_id"] for t in tickets]
            gold_ids = [g["ticket_id"] for g in golds]
            assert ticket_ids == gold_ids


class TestMetadataExporter:
    def test_export_metadata(self) -> None:
        scenarios = get_all_scenarios()
        with tempfile.TemporaryDirectory() as tmpdir:
            metadata_path = Path(tmpdir) / "metadata.json"
            export_scenario_metadata(scenarios, metadata_path)

            metadata = json.loads(metadata_path.read_text())
            assert len(metadata) == len(scenarios)

            for entry in metadata:
                assert "ticket_id" in entry
                assert "tag" in entry
                assert "test_name" in entry
                assert "test_description" in entry


class TestRegistry:
    def test_get_all_scenarios(self) -> None:
        scenarios = get_all_scenarios()
        assert len(scenarios) >= 30

    def test_get_data_cleanup_scenarios(self) -> None:
        scenarios = get_scenarios_by_tag(ScenarioTag.DATA_CLEANUP)
        assert len(scenarios) >= 15
        assert all(s.tag == ScenarioTag.DATA_CLEANUP for s in scenarios)

    def test_get_responsible_ai_scenarios(self) -> None:
        scenarios = get_scenarios_by_tag(ScenarioTag.RESPONSIBLE_AI)
        assert len(scenarios) >= 15
        assert all(s.tag == ScenarioTag.RESPONSIBLE_AI for s in scenarios)

    def test_no_duplicate_ticket_ids_across_all(self) -> None:
        scenarios = get_all_scenarios()
        ids = [s.ticket.ticket_id for s in scenarios]
        assert len(ids) == len(set(ids)), f"Duplicate ticket IDs across scenarios: {ids}"
