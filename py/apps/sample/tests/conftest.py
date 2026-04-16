"""Shared pytest fixtures for FDEBench tests.

This module provides:
- FastAPI test client with mocked AOAI credentials
- Sample data fixtures from task1/task3
- Environment setup for testing without live Azure OpenAI calls
"""

import json
import os
from pathlib import Path
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from fastapi.testclient import TestClient


# Data directory relative to this file
DATA_DIR = Path(__file__).parent.parent.parent.parent / "data"


@pytest.fixture(autouse=True)
def setup_test_env():
    """Set test environment variables before importing app."""
    os.environ.setdefault("AZURE_OPENAI_ENDPOINT", "https://test.openai.azure.com/")
    os.environ.setdefault("AZURE_OPENAI_API_KEY", "test-key")
    os.environ.setdefault("TRIAGE_MODEL", "gpt-5-4-nano")
    os.environ.setdefault("EXTRACT_MODEL", "gpt-5-4")
    os.environ.setdefault("ORCHESTRATE_MODEL", "gpt-5-4")
    yield
    # Cleanup if needed


@pytest.fixture
def client():
    """Create FastAPI test client with mocked AOAI.

    The client is configured with test credentials and the AOAI client
    is mocked to avoid live API calls during testing.
    """
    # Mock the AsyncAzureOpenAI client before importing the app
    with patch("llm_client.AsyncAzureOpenAI") as mock_aoai_class:
        # Create a mock client instance
        mock_client = AsyncMock()
        mock_aoai_class.return_value = mock_client

        # Import app after mocking
        from main import app

        return TestClient(app)


@pytest.fixture
def mock_aoai_client():
    """Return a mocked AsyncAzureOpenAI client for testing LLM calls.

    This fixture can be used to mock the response of Azure OpenAI calls
    in integration tests that specifically test LLM behavior.
    """
    mock = AsyncMock()
    return mock


@pytest.fixture
def sample_triage_input():
    """Load the first sample triage input from task1/sample.json."""
    with open(DATA_DIR / "task1" / "sample.json") as f:
        data = json.load(f)
    return data[0]


@pytest.fixture
def sample_triage_gold():
    """Load sample triage gold answers from task1/sample_gold.json."""
    with open(DATA_DIR / "task1" / "sample_gold.json") as f:
        return json.load(f)


@pytest.fixture
def sample_triage_gold_first():
    """Load the first gold answer for triage."""
    with open(DATA_DIR / "task1" / "sample_gold.json") as f:
        data = json.load(f)
    return data[0]


@pytest.fixture
def sample_orchestrate_input():
    """Load the first sample orchestration input from task3/public_eval_50.json."""
    with open(DATA_DIR / "task3" / "public_eval_50.json") as f:
        data = json.load(f)
    return data[0]


@pytest.fixture
def sample_orchestrate_gold():
    """Load sample orchestration gold answers from task3/public_eval_50_gold.json."""
    with open(DATA_DIR / "task3" / "public_eval_50_gold.json") as f:
        return json.load(f)


@pytest.fixture
def sample_orchestrate_gold_first():
    """Load the first gold answer for orchestration."""
    with open(DATA_DIR / "task3" / "public_eval_50_gold.json") as f:
        data = json.load(f)
    return data[0]
