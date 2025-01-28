import pytest
from fastapi.testclient import TestClient
from tests.fixtures.setup_test_ativity_data import setup_test_data

@pytest.mark.asyncio
async def test_search_organizations_by_activity_valid(
    api_key_client: TestClient, setup_test_data
):
    """Test searching organizations by valid activity ID."""
    data = setup_test_data  # Await the fixture to get the data

    activity_id = data["activity_food_id"]  # Use the food activity ID
    response = api_key_client.get(f"/api/activities/{activity_id}/organizations/search?depth=3")
    
    assert response.status_code == 200
    response_json = response.json()

    # Check that both organizations are in the response
    assert any(org['id'] == data["organization1_id"] for org in response_json)
    assert any(org['id'] == data["organization2_id"] for org in response_json)

    # Optionally, you can also check the details of each organization
    expected_organization1 = {
        "id": data["organization1_id"],
        "name": "Meat Shop",
        "phone_numbers": ["123-456"],
        "activities": [{"id": data["activity_meat_id"], "name": "Meat Products"}]
    }
    expected_organization2 = {
        "id": data["organization2_id"],
        "name": "Dairy Store",
        "phone_numbers": ["789-012"],
        "activities": [{"id": data["activity_dairy_id"], "name": "Dairy Products"}]
    }

    assert expected_organization1 in response_json
    assert expected_organization2 in response_json

@pytest.mark.asyncio
async def test_search_organizations_by_activity_not_found(
    api_key_client: TestClient, setup_test_data
):
    """Test searching organizations by non-existent activity ID."""
    # Await the setup_test_data fixture
    setup_test_data  # Await the fixture to get the data
    response = api_key_client.get("/api/activities/999/organizations/search?depth=3")
    
    assert response.status_code == 404
    assert response.json() == {"detail": "No organizations found for the given activity"}

@pytest.mark.asyncio
async def test_search_organizations_by_activity_invalid_depth(
    api_key_client: TestClient, setup_test_data ):
    """Test searching organizations with invalid depth."""
    # Await the setup_test_data fixture
    data = setup_test_data  # Await the fixture to get the data

    activity_id = data["activity_food_id"]  # Use the food activity ID
    response = api_key_client.get(f"/api/activities/{activity_id}/organizations/search?depth=0")
    
    assert response.status_code == 422  # Unprocessable Entity due to depth validation