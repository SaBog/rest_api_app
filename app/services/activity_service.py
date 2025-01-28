from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from app.db.models import Activity, Organization, organization_activity

async def get_nested_activity_ids(db: AsyncSession, activity_id: int, depth: int) -> List[int]:
    """Fetch IDs of nested activities using a recursive CTE."""
    cte = (
        select(Activity.id)
        .where(Activity.id == activity_id)
        .cte(recursive=True)
    )

    child_activities = select(Activity.id).where(Activity.parent_id == cte.c.id)
    cte = cte.union_all(child_activities)

    query = select(cte.c.id).limit(depth)
    result = await db.execute(query)
    return result.scalars().all()


async def search_organizations_by_activity(db: AsyncSession, activity_id: int, depth: int) -> List[Organization]:
    """Fetch organizations related to an activity, including nested activities."""
    activity_ids = await get_nested_activity_ids(db, activity_id, depth)
    query = (
        select(Organization)
        .join(organization_activity)
        .where(organization_activity.c.activity_id.in_(activity_ids))
        .options(joinedload(Organization.building))
    )
    result = await db.execute(query)
    return result.scalars().all()
