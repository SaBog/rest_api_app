import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import Organization, Building  # Adjust the import based on your project structure

@pytest.mark.asyncio
async def test_search_organizations_by_name(api_key_client: TestClient, get_test_session: AsyncSession):
    """Test searching organizations by name."""
    # Create test data
    building = Building(id=1, address="Test Address", latitude=0.0, longitude=0.0)
    organization1 = Organization(
        id=1, name="Test Organization", phone_numbers=["123-456"], building_id=1
    )
    organization2 = Organization(
        id=2, name="Another Organization", phone_numbers=["789-012"], building_id=1
    )

    # Add data to the database
    async with get_test_session as session:
        session.add(building)
        session.add(organization1)
        session.add(organization2)
        await session.commit()

    # Test the endpoint with a valid search
    response = api_key_client.get("/api/organizations/search?name=Test")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0] == {
        "id": 1,
        "name": "Test Organization",
        "phone_numbers": ["123-456"],
        "building": {
            "id": 1,
            "address": "Test Address",
            "latitude": 0.0,
            "longitude": 0.0
        },
        "activities": []
    }

    # Test the endpoint with a search that returns no results
    response = api_key_client.get("/api/organizations/search?name=Nonexistent")
    assert response.status_code == 200
    assert response.json() == []