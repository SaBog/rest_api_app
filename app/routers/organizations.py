from typing import List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.schemas.schemas import BuildingWithOrganizationsResponse, OrganizationWithBuilding
from app.services.organization_service import *

router = APIRouter(prefix='/organizations', tags=['Organizations'])

@router.get("/search", response_model=List[OrganizationWithBuilding])
async def search_organizations(
    name: str = Query(..., min_length=2, description="Name of the organization to search for"),
    db: AsyncSession = Depends(get_db)
):
    """
    Endpoint to search for organizations by name.

    Args:
        name (str): The name of the organization to search for. Must be at least 2 characters long.
        db (AsyncSession): The database session.

    Returns:
        List[OrganizationWithBuilding]: A list of organizations matching the search name, including their associated building.
    """
    # Perform the search query to find organizations matching the name
    organizations = await search_organizations_by_name(db, name)
    
    # Return the list of found organizations
    return organizations

@router.get("/nearby/circular", response_model=List[BuildingWithOrganizationsResponse])
async def fetch_buildings_in_circular_area(
    latitude: float = Query(
        ..., ge=-90, le=90, description="Latitude of the center point in degrees"
    ),
    longitude: float = Query(
        ..., ge=-180, le=180, description="Longitude of the center point in degrees"
    ),
    radius: float = Query(..., gt=0, description="Radius in kilometers"),
    db: AsyncSession = Depends(get_db),
):
    """
    Fetch all buildings within a given circular area.

    Args:
        latitude (float): The latitude of the center point.
        longitude (float): The longitude of the center point.
        radius (float): The radius in kilometers.
        db (AsyncSession): The database session.

    Returns:
        List[BuildingWithOrganizationsResponse]: A list of buildings within the circular area, including their associated organizations.
    """
    buildings = await get_buildings_in_circular_area(db, latitude, longitude, radius)
    if not buildings:
        raise HTTPException(status_code=404, detail="No buildings found in the specified area")
    return buildings

@router.get("/nearby/rectangular", response_model=List[BuildingWithOrganizationsResponse])
async def fetch_buildings_in_rectangular_area(
    # The minimum latitude of the rectangular area
    min_lat: float = Query(..., ge=-90, le=90, description="Minimum latitude"),
    # The maximum latitude of the rectangular area
    max_lat: float = Query(..., ge=-90, le=90, description="Maximum latitude"),
    # The minimum longitude of the rectangular area
    min_lon: float = Query(..., ge=-180, le=180, description="Minimum longitude"),
    # The maximum longitude of the rectangular area
    max_lon: float = Query(..., ge=-180, le=180, description="Maximum longitude"),
    # The database session
    db: AsyncSession = Depends(get_db),
):
    """
    Fetch all buildings within a given rectangular area.

    Args:
        min_lat (float): The minimum latitude of the rectangular area.
        max_lat (float): The maximum latitude of the rectangular area.
        min_lon (float): The minimum longitude of the rectangular area.
        max_lon (float): The maximum longitude of the rectangular area.
        db (AsyncSession): The database session.

    Returns:
        List[BuildingWithOrganizationsResponse]: A list of buildings within the rectangular area, including their associated organizations.
    """
    buildings = await get_buildings_in_rectangular_area(db, min_lat, max_lat, min_lon, max_lon)
    if not buildings:
        raise HTTPException(status_code=404, detail="No buildings found in the specified area")
    return buildings


@router.get("/{organization_id}", response_model=OrganizationWithBuilding)
async def get_organization(
    organization_id: int, db: AsyncSession = Depends(get_db)
):
    """
    Fetch an organization by its ID.

    Args:
        organization_id (int): The ID of the organization to fetch.
        db (AsyncSession): The database session.

    Returns:
        OrganizationWithBuilding: The organization with its associated building.

    Raises:
        HTTPException: If no organization is found for the given ID.
    """
    organization = await get_organization_by_id(db, organization_id)
    if not organization:
        raise HTTPException(status_code=404, detail="Organization not found")
    return organization
