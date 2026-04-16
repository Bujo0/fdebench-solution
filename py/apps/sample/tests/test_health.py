"""Test health endpoint.

Tests that the health endpoint is working and returns the expected response.
"""

import pytest


class TestHealth:
    """Health endpoint tests."""

    def test_health_returns_200(self, client):
        """Test that GET /health returns 200 OK."""
        response = client.get("/health")
        assert response.status_code == 200

    def test_health_returns_ok_status(self, client):
        """Test that GET /health returns {status: 'ok'}."""
        response = client.get("/health")
        data = response.json()
        assert data.get("status") == "ok"

    def test_health_response_is_dict(self, client):
        """Test that health response is a dictionary."""
        response = client.get("/health")
        assert isinstance(response.json(), dict)
