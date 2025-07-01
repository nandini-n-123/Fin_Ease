# File: tests/test_main.py

import pytest
from httpx import AsyncClient
from backend.main import app # Import your FastAPI app from its file

# This fixture creates a test client that can make requests to your app
@pytest.fixture
async def client():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

# This is your test function
@pytest.mark.asyncio
async def test_root_health_check(client: AsyncClient):
    """Tests if the root endpoint '/' is working correctly."""
    response = await client.get("/")
    
    # Assertions check if the result is what we expect.
    # If any assert fails, the test fails.
    assert response.status_code == 200
    assert response.json() == {"message": "FinEase Web-RAG Backend is running!"}