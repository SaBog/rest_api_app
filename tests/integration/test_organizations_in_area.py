import pytest
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import Building, Organization

@pytest.mark.asyncio
async def test_get_buildings_in_circular_area(api_key_client: TestClient, get_test_session: AsyncSession):
    """Test searching for buildings within a circular area."""
    # Create test data
    building1 = Building(id=1, address="Building 1", latitude=55.7558, longitude=37.6176)
    building2 = Building(id=2, address="Building 2", latitude=55.7600, longitude=37.6200)
    organization1 = Organization(id=1, name="Org 1", phone_numbers=["111-111"], building_id=1)
    organization2 = Organization(id=2, name="Org 2", phone_numbers=["222-222"], building_id=2)

    # Add data to the database
    async with get_test_session as session:
        session.add_all([building1, building2, organization1, organization2])
        await session.commit()

    # Test the endpoint
    response = api_key_client.get("api/organizations/nearby/circular?latitude=55.7558&longitude=37.6176&radius=1")
    assert response.status_code == 200
    assert len(response.json()) == 2  # Both buildings are within the radius

@pytest.mark.asyncio
async def test_get_buildings_in_circular_area_no_results(api_key_client: TestClient, get_test_session: AsyncSession):
    """Test searching for buildings within a circular area with no results."""
    # Create test data
    building = Building(id=1, address="Building 1", latitude=55.7558, longitude=37.6176)
    organization = Organization(id=1, name="Org 1", phone_numbers=["111-111"], building_id=1)

    # Add data to the database
    async with get_test_session as session:
        session.add(building)
        session.add(organization)
        await session.commit()

    # Test the endpoint with a radius that excludes the building
    response = api_key_client.get("api/organizations/nearby/circular?latitude=55.7558&longitude=38.6176&radius=1")
    assert response.status_code == 404
    assert response.json() == {"detail": "No buildings found in the specified area"}

    response = api_key_client.get("api/organizations/nearby/circular?latitude=55.7558&longitude=38.6176&radius=80")
    assert response.status_code == 200
    assert len(response.json()) == 1  # Both buildings are within the radius

@pytest.mark.asyncio
async def test_get_buildings_in_rectangular_area(api_key_client: TestClient, get_test_session: AsyncSession):
    """Test searching for buildings within a rectangular area."""
    # Create test data
    building1 = Building(id=1, address="Building 1", latitude=55.7558, longitude=37.6176)
    building2 = Building(id=2, address="Building 2", latitude=55.7600, longitude=37.6200)
    organization1 = Organization(id=1, name="Org 1", phone_numbers=["111-111"], building_id=1)
    organization2 = Organization(id=2, name="Org 2", phone_numbers=["222-222"], building_id=2)

    # Add data to the database
    async with get_test_session as session:
        session.add_all([building1, building2, organization1, organization2])
        await session.commit()

    # Test the endpoint
    response = api_key_client.get(
        "api/organizations/nearby/rectangular?min_lat=55.75&max_lat=55.77&min_lon=37.61&max_lon=37.63"
    )
    assert response.status_code == 200
    assert len(response.json()) == 2  # Both buildings are within the bounding box