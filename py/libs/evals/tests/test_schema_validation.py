# Copyright (c) Microsoft. All rights reserved.
"""Tests for schema validation logic."""

from evals.validators.schema import validate_triage_response


class TestSchemaValidation:
    """Tests for the schema validator."""

    def test_valid_response_no_violations(self):
        response = {
            "ticket_id": "INC-0001",
            "category": "Network & Connectivity",
            "priority": "P3",
            "assigned_team": "Network Operations",
            "needs_escalation": False,
            "missing_information": [],
            "next_best_action": "Check the VPN",
            "remediation_steps": ["Step 1"],
        }
        violations = validate_triage_response(response)
        assert violations == []

    def test_missing_required_field(self):
        response = {
            "ticket_id": "INC-0001",
            "category": "Network & Connectivity",
            # priority missing
            "assigned_team": "Network Operations",
            "needs_escalation": False,
            "missing_information": [],
            "next_best_action": "Check the VPN",
            "remediation_steps": ["Step 1"],
        }
        violations = validate_triage_response(response)
        assert any(v.field == "priority" for v in violations)

    def test_invalid_category(self):
        response = {
            "ticket_id": "INC-0001",
            "category": "Invalid Category",
            "priority": "P3",
            "assigned_team": "Network Operations",
            "needs_escalation": False,
            "missing_information": [],
            "next_best_action": "Check the VPN",
            "remediation_steps": ["Step 1"],
        }
        violations = validate_triage_response(response)
        assert any(v.field == "category" for v in violations)

    def test_invalid_priority(self):
        response = {
            "ticket_id": "INC-0001",
            "category": "Network & Connectivity",
            "priority": "P5",
            "assigned_team": "Network Operations",
            "needs_escalation": False,
            "missing_information": [],
            "next_best_action": "Check the VPN",
            "remediation_steps": ["Step 1"],
        }
        violations = validate_triage_response(response)
        assert any(v.field == "priority" for v in violations)

    def test_invalid_team(self):
        response = {
            "ticket_id": "INC-0001",
            "category": "Network & Connectivity",
            "priority": "P3",
            "assigned_team": "Invalid Team",
            "needs_escalation": False,
            "missing_information": [],
            "next_best_action": "Check the VPN",
            "remediation_steps": ["Step 1"],
        }
        violations = validate_triage_response(response)
        assert any(v.field == "assigned_team" for v in violations)

    def test_invalid_escalation_type(self):
        response = {
            "ticket_id": "INC-0001",
            "category": "Network & Connectivity",
            "priority": "P3",
            "assigned_team": "Network Operations",
            "needs_escalation": "yes",
            "missing_information": [],
            "next_best_action": "Check the VPN",
            "remediation_steps": ["Step 1"],
        }
        violations = validate_triage_response(response)
        assert any(v.field == "needs_escalation" for v in violations)

    def test_invalid_missing_info_value(self):
        response = {
            "ticket_id": "INC-0001",
            "category": "Network & Connectivity",
            "priority": "P3",
            "assigned_team": "Network Operations",
            "needs_escalation": False,
            "missing_information": ["invalid_field"],
            "next_best_action": "Check the VPN",
            "remediation_steps": ["Step 1"],
        }
        violations = validate_triage_response(response)
        assert any(v.field == "missing_information" for v in violations)

    def test_missing_info_not_list(self):
        response = {
            "ticket_id": "INC-0001",
            "category": "Network & Connectivity",
            "priority": "P3",
            "assigned_team": "Network Operations",
            "needs_escalation": False,
            "missing_information": "error_message",
            "next_best_action": "Check the VPN",
            "remediation_steps": ["Step 1"],
        }
        violations = validate_triage_response(response)
        assert any(v.field == "missing_information" for v in violations)

    def test_remediation_not_list(self):
        response = {
            "ticket_id": "INC-0001",
            "category": "Network & Connectivity",
            "priority": "P3",
            "assigned_team": "Network Operations",
            "needs_escalation": False,
            "missing_information": [],
            "next_best_action": "Check the VPN",
            "remediation_steps": "Step 1",
        }
        violations = validate_triage_response(response)
        assert any(v.field == "remediation_steps" for v in violations)

    def test_empty_response_multiple_violations(self):
        violations = validate_triage_response({})
        assert len(violations) == 8  # All required fields missing

    def test_all_valid_categories_accepted(self):
        categories = [
            "Access & Authentication",
            "Hardware & Peripherals",
            "Network & Connectivity",
            "Software & Applications",
            "Security & Compliance",
            "Data & Storage",
            "General Inquiry",
            "Not a Support Ticket",
        ]
        for cat in categories:
            response = {
                "ticket_id": "INC-0001",
                "category": cat,
                "priority": "P3",
                "assigned_team": "Network Operations",
                "needs_escalation": False,
                "missing_information": [],
                "next_best_action": "Test",
                "remediation_steps": ["Step 1"],
            }
            violations = validate_triage_response(response)
            assert not any(v.field == "category" for v in violations), f"Category {cat!r} rejected"

    def test_all_valid_teams_accepted(self):
        teams = [
            "Identity & Access Management",
            "Endpoint Engineering",
            "Network Operations",
            "Enterprise Applications",
            "Security Operations",
            "Data Platform",
            "None",
        ]
        for team in teams:
            response = {
                "ticket_id": "INC-0001",
                "category": "Network & Connectivity",
                "priority": "P3",
                "assigned_team": team,
                "needs_escalation": False,
                "missing_information": [],
                "next_best_action": "Test",
                "remediation_steps": ["Step 1"],
            }
            violations = validate_triage_response(response)
            assert not any(v.field == "assigned_team" for v in violations), f"Team {team!r} rejected"

    def test_all_valid_missing_info_accepted(self):
        valid_fields = [
            "affected_system",
            "error_message",
            "steps_to_reproduce",
            "affected_users",
            "environment_details",
            "timestamp",
            "previous_ticket_id",
            "contact_info",
            "device_info",
            "application_version",
            "network_location",
            "business_impact",
            "reproduction_frequency",
            "screenshot_or_attachment",
            "authentication_method",
            "configuration_details",
        ]
        response = {
            "ticket_id": "INC-0001",
            "category": "Network & Connectivity",
            "priority": "P3",
            "assigned_team": "Network Operations",
            "needs_escalation": False,
            "missing_information": valid_fields,
            "next_best_action": "Test",
            "remediation_steps": ["Step 1"],
        }
        violations = validate_triage_response(response)
        assert not any(v.field == "missing_information" for v in violations)
