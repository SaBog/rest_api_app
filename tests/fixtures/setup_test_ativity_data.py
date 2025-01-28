import pytest_asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.models import Organization, Activity, Building 


@pytest_asyncio.fixture
async def setup_test_data(get_test_session: AsyncSession):
    """Fixture to set up test data for organization and activity."""
    building = Building(id=1, address="Test Address", latitude=0.0, longitude=0.0)
    
    # Create activities
    activity_food = Activity(id=1, name="Food")
    activity_meat = Activity(id=2, name="Meat Products", parent_id=1)  
    activity_dairy = Activity(id=3, name="Dairy Products", parent_id=1)

    # Create organizations
    organization1 = Organization(
        id=1, name="Meat Shop", phone_numbers=["123-456"], building_id=1
    )
    organization2 = Organization(
        id=2, name="Dairy Store", phone_numbers=["789-012"], building_id=1
    )

    # Associate organizations with activities
    organization1.activities.append(activity_meat)
    organization2.activities.append(activity_dairy)

    # Add data to the database
    async with get_test_session as session:
        session.add(building)
        session.add(activity_food)
        session.add(activity_meat)
        session.add(activity_dairy)
        session.add(organization1)
        session.add(organization2)
        await session.commit()

    return {
        "building_id": building.id,
        "activity_food_id": activity_food.id,
        "activity_meat_id": activity_meat.id,
        "activity_dairy_id": activity_dairy.id,
        "organization1_id": organization1.id,
        "organization2_id": organization2.id,
    }
