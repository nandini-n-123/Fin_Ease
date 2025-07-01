# tests/test_main.py

import pytest
from fastapi.testclient import TestClient
from backend.main import app

# This fixture creates a synchronous test client for your app
@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c

# This is now a standard, synchronous test function
def test_root_health_check(client: TestClient):
    """
    Tests that the root endpoint returns a 200 OK status.
    """
    response = client.get("/")
    assert response.status_code == 200
    # You can add more assertions here if needed
    # For example: assert response.json() == {"message": "OK"}