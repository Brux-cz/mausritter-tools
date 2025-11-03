# -*- coding: utf-8 -*-
"""
Pytest configuration and fixtures for Mausritter API tests.
"""

import sys
from pathlib import Path
import pytest
from fastapi.testclient import TestClient

# Add project root to path
tests_dir = Path(__file__).parent
backend_dir = tests_dir.parent
project_root = backend_dir.parent
sys.path.insert(0, str(project_root))

from app.main import app


@pytest.fixture(scope="session")
def test_client():
    """
    Create FastAPI TestClient for all tests.

    Using scope="session" means the client is created once
    for the entire test session (more efficient).
    """
    return TestClient(app)


@pytest.fixture(scope="session")
def api_base_url():
    """Base URL for API endpoints."""
    return "/api/v1/generate"
