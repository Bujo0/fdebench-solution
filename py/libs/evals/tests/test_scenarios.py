# Copyright (c) Microsoft. All rights reserved.
"""Tests for scenario definitions — verify all registered scenarios are well-formed."""

import ms.evals.scenarios.data_cleanup  # noqa: F401
import ms.evals.scenarios.responsible_ai  # noqa: F401
from ms.evals.models.scenario import ScenarioCategory
from ms.evals.scenarios.registry import default_registry


class TestDefaultRegistryPopulation:
    def test_data_cleanup_scenarios_registered(self) -> None:
        dc = default_registry.by_category(ScenarioCategory.DATA_CLEANUP)
        assert len(dc) == 40

    def test_responsible_ai_scenarios_registered(self) -> None:
        rai = default_registry.by_category(ScenarioCategory.RESPONSIBLE_AI)
        assert len(rai) == 85

    def test_total_scenarios(self) -> None:
        assert default_registry.count == 125


class TestScenarioWellFormedness:
    def test_all_scenario_ids_unique(self) -> None:
        all_scenarios = default_registry.all()
        ids = [s.scenario_id for s in all_scenarios]
        assert len(ids) == len(set(ids)), f"Duplicate IDs: {[x for x in ids if ids.count(x) > 1]}"

    def test_all_ticket_ids_unique(self) -> None:
        all_scenarios = default_registry.all()
        ticket_ids = [s.ticket.ticket_id for s in all_scenarios]
        assert len(ticket_ids) == len(set(ticket_ids))

    def test_dc_ids_prefixed(self) -> None:
        dc = default_registry.by_category(ScenarioCategory.DATA_CLEANUP)
        for s in dc:
            assert s.scenario_id.startswith("dc-"), f"Data cleanup scenario {s.scenario_id} missing dc- prefix"

    def test_rai_ids_prefixed(self) -> None:
        rai = default_registry.by_category(ScenarioCategory.RESPONSIBLE_AI)
        for s in rai:
            assert s.scenario_id.startswith("rai-"), f"RAI scenario {s.scenario_id} missing rai- prefix"

    def test_all_tickets_have_required_fields(self) -> None:
        for s in default_registry.all():
            ticket = s.ticket
            assert ticket.ticket_id, f"Scenario {s.scenario_id}: missing ticket_id"
            assert ticket.subject, f"Scenario {s.scenario_id}: missing subject"
            assert ticket.reporter.name, f"Scenario {s.scenario_id}: missing reporter name"
            assert ticket.reporter.email, f"Scenario {s.scenario_id}: missing reporter email"
            assert ticket.created_at, f"Scenario {s.scenario_id}: missing created_at"
            assert ticket.channel, f"Scenario {s.scenario_id}: missing channel"

    def test_all_scenarios_have_name_and_description(self) -> None:
        for s in default_registry.all():
            assert s.name, f"Scenario {s.scenario_id}: missing name"
            assert s.description, f"Scenario {s.scenario_id}: missing description"

    def test_all_scenarios_have_tags(self) -> None:
        for s in default_registry.all():
            assert len(s.tags) > 0, f"Scenario {s.scenario_id}: missing tags"

    def test_dc_tickets_use_5xxx_ids(self) -> None:
        dc = default_registry.by_category(ScenarioCategory.DATA_CLEANUP)
        for s in dc:
            assert s.ticket.ticket_id.startswith("INC-5"), (
                f"Data cleanup ticket {s.ticket.ticket_id} should use INC-5xxx range"
            )

    def test_rai_tickets_use_6xxx_ids(self) -> None:
        rai = default_registry.by_category(ScenarioCategory.RESPONSIBLE_AI)
        for s in rai:
            assert s.ticket.ticket_id.startswith("INC-6"), (
                f"RAI ticket {s.ticket.ticket_id} should use INC-6xxx range"
            )
