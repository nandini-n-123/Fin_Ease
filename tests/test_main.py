# tests/test_main.py
import pytest
from httpx import AsyncClient
from backend.main import app # Import your FastAPI app

# This "fixture" creates a test client for our app that tests can use
@pytest.fixture
async def client():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

# Our first test function
@pytest.mark.asyncio
async def test_root_health_check(client: AsyncClient):
    """Tests if the root endpoint '/' is running and returns the correct message."""
    response = await client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "FinEase Web-RAG Backend is running!"}