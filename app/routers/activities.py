import logging
from typing import List
from fastapi import APIRouter, Depends, Query, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.services.activity_service import search_organizations_by_activity
from app.schemas.schemas import OrganizationBase

logger = logging.getLogger(__name__)
router = APIRouter(prefix='/activities', tags=['Activities'])

@router.get("/{activity_id}/organizations/search", response_model=List[OrganizationBase])
async def search_organizations_by_activity_endpoint(
    activity_id: int,
    depth: int = Query(3, ge=1, le=3, description="Maximum depth of activity tree"),
    db: AsyncSession = Depends(get_db),
):
    """
    Endpoint to search for organizations associated with a given activity.

    Args:
        activity_id (int): The ID of the activity to search organizations for.
        depth (int): The depth of activity tree traversal (default is 3).
        db (AsyncSession): The database session.

    Returns:
        List[OrganizationBase]: A list of organizations related to the activity.

    Raises:
        HTTPException: If no organizations are found for the given activity.
    """
    # Fetch organizations related to the specified activity and depth
    organizations = await search_organizations_by_activity(db, activity_id, depth)
    
    # If no organizations are found, log a warning and raise an HTTP 404 error
    if not organizations:
        logger.warning(f"No organizations found for activity ID {activity_id}")
        raise HTTPException(status_code=404, detail="No organizations found for the given activity")
    
    # Return the list of organizations
    return organizations

