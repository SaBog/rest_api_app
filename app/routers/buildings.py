from fastapi import APIRouter, HTTPException, Depends, Path
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.schemas.schemas import BuildingWithOrganizationsResponse
from app.services.building_service import get_building_with_organizations
import logging

logger = logging.getLogger(__name__)
router = APIRouter(prefix='/buildings', tags=['Buildings'])

@router.get("/{building_id}/organizations", response_model=BuildingWithOrganizationsResponse)
async def list_organizations_in_building(
    building_id: int = Path(..., gt=0),
    db: AsyncSession = Depends(get_db)
) -> BuildingWithOrganizationsResponse:
    """
    Retrieve a building and its associated organizations.

    Args:
        building_id (int): The ID of the building to retrieve.

    Returns:
        BuildingWithOrganizationsResponse: The building with its associated organizations.
    """
    building = await get_building_with_organizations(db, building_id)
    if not building:
        logger.warning(f"Building with ID {building_id} not found")
        raise HTTPException(status_code=404, detail="Building not found")

    return building

