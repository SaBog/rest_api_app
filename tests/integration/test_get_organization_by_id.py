import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import Organization, Building 

@pytest.mark.asyncio
async def test_get_organization_by_id(api_key_client: TestClient, get_test_session: AsyncSession):
    """Test retrieving an organization by ID."""
    # Create test data
    building = Building(id=1, address="Test Address", latitude=0.0, longitude=0.0)
    organization = Organization(
        id=1, name="Test Organization", phone_numbers=["123-456"], building_id=1
    )

    # Add data to the database
    async with get_test_session as session:
        session.add(building)
        session.add(organization)
        await session.commit()

    # Test the endpoint
    response = api_key_client.get("/api/organizations/1")
    assert response.status_code == 200
    assert response.json() == {
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