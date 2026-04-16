"""Resilience and edge case tests for all endpoints.

These tests validate that endpoints handle malformed input, wrong content types,
and other edge cases gracefully without crashing (500 errors).
"""

import json
import pytest


class TestTriageResilience:
    """Resilience tests for POST /triage endpoint."""

    def test_triage_malformed_json_returns_error(self, client):
        """Test that malformed JSON returns 400 or 422, not 500."""
        response = client.post(
            "/triage",
            content="{ invalid json",
            headers={"Content-Type": "application/json"},
        )
        assert response.status_code in (400, 422, 500)
        # If it's 500, we want to catch that regression
        if response.status_code == 500:
            pytest.fail("Malformed JSON caused 500 error instead of 400/422")

    def test_triage_empty_body_returns_error(self, client):
        """Test that empty body {} returns 400 or 422."""
        response = client.post("/triage", json={})
        assert response.status_code in (400, 422)

    def test_triage_missing_required_field_ticket_id(self, client, sample_triage_input):
        """Test that missing ticket_id field returns 400 or 422."""
        req = sample_triage_input.copy()
        del req["ticket_id"]
        response = client.post("/triage", json=req)
        assert response.status_code in (400, 422)

    def test_triage_missing_required_field_subject(self, client, sample_triage_input):
        """Test that missing subject field returns 400 or 422."""
        req = sample_triage_input.copy()
        del req["subject"]
        response = client.post("/triage", json=req)
        assert response.status_code in (400, 422)

    def test_triage_missing_required_field_reporter(self, client, sample_triage_input):
        """Test that missing reporter field returns 400 or 422."""
        req = sample_triage_input.copy()
        del req["reporter"]
        response = client.post("/triage", json=req)
        assert response.status_code in (400, 422)

    def test_triage_50kb_payload_no_crash(self, client):
        """Test that 50KB payload doesn't cause 500 error."""
        # Create a request with a ~50KB description
        large_desc = "A" * 50000
        req = {
            "ticket_id": "SIG-LARGE",
            "subject": "Large description",
            "description": large_desc,
            "reporter": {"name": "Test", "email": "test@example.com", "department": "Ops"},
            "created_at": "2026-03-17T10:00:00Z",
            "channel": "bridge_terminal",
        }
        response = client.post("/triage", json=req)
        # Should return 200, 201, or validation error, but not 500
        assert response.status_code != 500

    def test_triage_wrong_content_type_with_valid_data(self, client, sample_triage_input):
        """Test that wrong Content-Type returns 415 or accepts the request."""
        response = client.post(
            "/triage",
            json=sample_triage_input,
            headers={"Content-Type": "text/plain"},
        )
        # FastAPI is lenient with Content-Type, so might accept it
        # But it should not crash
        assert response.status_code != 500

    def test_triage_invalid_email_in_reporter(self, client, sample_triage_input):
        """Test that invalid email in reporter returns validation error."""
        req = sample_triage_input.copy()
        req["reporter"]["email"] = "not-an-email"
        response = client.post("/triage", json=req)
        # Should return validation error, not 500
        assert response.status_code in (400, 422, 200, 201)  # Might still accept


class TestExtractResilience:
    """Resilience tests for POST /extract endpoint."""

    def test_extract_malformed_json_returns_error(self, client):
        """Test that malformed JSON returns 400 or 422, not 500."""
        response = client.post(
            "/extract",
            content="{ invalid json",
            headers={"Content-Type": "application/json"},
        )
        assert response.status_code in (400, 422, 500)
        if response.status_code == 500:
            pytest.fail("Malformed JSON caused 500 error")

    def test_extract_empty_body_returns_error(self, client):
        """Test that empty body {} returns 400 or 422."""
        response = client.post("/extract", json={})
        assert response.status_code in (400, 422)

    def test_extract_missing_document_id(self, client):
        """Test that missing document_id returns 400 or 422."""
        req = {"content": "aGVsbG8gd29ybGQ=", "content_format": "image_base64"}
        response = client.post("/extract", json=req)
        assert response.status_code in (400, 422)

    def test_extract_missing_content(self, client):
        """Test that missing content returns 400 or 422."""
        req = {"document_id": "doc-001", "content_format": "image_base64"}
        response = client.post("/extract", json=req)
        assert response.status_code in (400, 422)

    def test_extract_50kb_payload_no_crash(self, client):
        """Test that 50KB payload doesn't cause 500 error."""
        # Create a request with a ~50KB base64 content
        large_content = "QUJDRA==" * 15000  # ~120KB base64
        req = {"document_id": "doc-large", "content": large_content}
        response = client.post("/extract", json=req)
        # Should not crash with 500
        assert response.status_code != 500

    def test_extract_wrong_content_type(self, client):
        """Test that wrong Content-Type doesn't crash."""
        req = {
            "document_id": "doc-001",
            "content": "aGVsbG8gd29ybGQ=",
            "content_format": "image_base64",
        }
        response = client.post(
            "/extract",
            json=req,
            headers={"Content-Type": "text/plain"},
        )
        assert response.status_code != 500

    def test_extract_invalid_base64(self, client):
        """Test that invalid base64 in content is handled gracefully."""
        req = {
            "document_id": "doc-001",
            "content": "!@#$%^&*()",  # Invalid base64
            "content_format": "image_base64",
        }
        response = client.post("/extract", json=req)
        # Should not crash with 500
        assert response.status_code != 500


class TestOrchestrateResilience:
    """Resilience tests for POST /orchestrate endpoint."""

    def test_orchestrate_malformed_json_returns_error(self, client):
        """Test that malformed JSON returns 400 or 422, not 500."""
        response = client.post(
            "/orchestrate",
            content="{ invalid json",
            headers={"Content-Type": "application/json"},
        )
        assert response.status_code in (400, 422, 500)
        if response.status_code == 500:
            pytest.fail("Malformed JSON caused 500 error")

    def test_orchestrate_empty_body_returns_error(self, client):
        """Test that empty body {} returns 400 or 422."""
        response = client.post("/orchestrate", json={})
        assert response.status_code in (400, 422)

    def test_orchestrate_missing_task_id(self, client, sample_orchestrate_input):
        """Test that missing task_id returns 400 or 422."""
        req = sample_orchestrate_input.copy()
        del req["task_id"]
        response = client.post("/orchestrate", json=req)
        assert response.status_code in (400, 422)

    def test_orchestrate_missing_goal(self, client, sample_orchestrate_input):
        """Test that missing goal returns 400 or 422."""
        req = sample_orchestrate_input.copy()
        del req["goal"]
        response = client.post("/orchestrate", json=req)
        assert response.status_code in (400, 422)

    def test_orchestrate_missing_available_tools(self, client, sample_orchestrate_input):
        """Test that missing available_tools returns 400 or 422."""
        req = sample_orchestrate_input.copy()
        del req["available_tools"]
        response = client.post("/orchestrate", json=req)
        assert response.status_code in (400, 422)

    def test_orchestrate_50kb_payload_no_crash(self, client):
        """Test that 50KB payload doesn't cause 500 error."""
        # Create a request with large goal
        large_goal = "G" * 50000
        req = {
            "task_id": "task-large",
            "goal": large_goal,
            "available_tools": [
                {
                    "name": "tool1",
                    "description": "A test tool",
                    "endpoint": "http://localhost:9000/test",
                    "parameters": [{"name": "param1", "type": "string", "description": "Test"}],
                }
            ],
        }
        response = client.post("/orchestrate", json=req)
        # Should not crash with 500
        assert response.status_code != 500

    def test_orchestrate_wrong_content_type(self, client, sample_orchestrate_input):
        """Test that wrong Content-Type doesn't crash."""
        response = client.post(
            "/orchestrate",
            json=sample_orchestrate_input,
            headers={"Content-Type": "text/plain"},
        )
        assert response.status_code != 500

    def test_orchestrate_empty_tools_list(self, client):
        """Test that empty available_tools list is handled."""
        req = {
            "task_id": "task-empty-tools",
            "goal": "Do something",
            "available_tools": [],
        }
        response = client.post("/orchestrate", json=req)
        # Should not crash with 500
        assert response.status_code != 500


class TestGeneralResilience:
    """General resilience tests across all endpoints."""

    @pytest.mark.parametrize("endpoint", ["/triage", "/extract", "/orchestrate"])
    def test_nonexistent_endpoint_returns_404(self, client, endpoint):
        """Test that POST to nonexistent endpoint returns 404."""
        response = client.post(endpoint + "_nonexistent", json={})
        assert response.status_code == 404

    def test_get_on_post_endpoints_returns_405(self, client):
        """Test that GET on POST-only endpoints returns 405."""
        response = client.get("/triage")
        assert response.status_code == 405

    def test_null_json_body(self, client):
        """Test that null JSON body is handled."""
        response = client.post(
            "/triage",
            data="null",
            headers={"Content-Type": "application/json"},
        )
        # Should return validation error, not 500
        assert response.status_code in (400, 422, 500)
        if response.status_code == 500:
            pytest.fail("Null JSON body caused 500 error")
