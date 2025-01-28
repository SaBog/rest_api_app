from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from app.db.models import Building

async def get_building_with_organizations(db: AsyncSession, building_id: int) -> Building:
    """
    Retrieve a building and its associated organizations.
    """
    result = await db.execute(
        select(Building)
        .options(joinedload(Building.organizations))
        .where(Building.id == building_id) 
    )
    building = result.scalars().first() 
    return building
