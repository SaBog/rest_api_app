from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import joinedload
from sqlalchemy.sql.expression import and_
from typing import List, Optional
from app.db.models import Organization, Building
from app.utils.math import haversine

async def get_organization_by_id(db: AsyncSession, organization_id: int) -> Optional[Organization]:
    """Fetch an organization and its associated building by its ID.

    Args:
        db (AsyncSession): The database session.
        organization_id (int): The ID of the organization to fetch.

    Returns:
        Organization: The organization with its associated building.
    """
    result = await db.execute(
        select(Organization)
        .options(
            joinedload(Organization.building), 
        )
        .where(Organization.id == organization_id) 
    )
    return result.unique().scalar_one_or_none()

async def search_organizations_by_name(db: AsyncSession, name: str) -> List[Organization]: 
    """
    Search for organizations by their name, including their associated building.

    Args:
        db (AsyncSession): The database session.
        name (str): The name to search for, case-insensitive.

    Returns:
        List[Organization]: A list of organizations matching the search criteria.
    """
    result = await db.execute(
        select(Organization)
        .options(
            joinedload(Organization.building),
        )
        .where(Organization.name.ilike(f"%{name}%"))  # Case-insensitive search
    )
    return result.unique().scalars().all()

async def get_buildings_in_circular_area(
    db: AsyncSession,
    latitude: float,
    longitude: float,
    radius: float,
) -> List[Building]:
    """
    Fetch all buildings within a given circular area.

    Args:
        db (AsyncSession): The database session.
        latitude (float): The latitude of the center point.
        longitude (float): The longitude of the center point.
        radius (float): The radius in kilometers.

    Returns:
        List[Building]: A list of buildings within the circular area, including their associated organizations.
    """
    # Fetch all buildings with their associated organizations
    query = select(Building).options(joinedload(Building.organizations))
    result = await db.execute(query)
    buildings = result.unique().scalars().all()

    # Filter the buildings based on the circular area
    filtered_buildings = [
        building
        for building in buildings
        if haversine(latitude, longitude, building.latitude, building.longitude) <= radius
    ]

    return filtered_buildings

async def get_buildings_in_rectangular_area(
    db: AsyncSession,
    min_lat: float,
    max_lat: float,
    min_lon: float,
    max_lon: float,
) -> List[Building]:
    """
    Fetch all buildings within a given rectangular area.

    Args:
        db (AsyncSession): The database session.
        min_lat (float): The minimum latitude of the rectangular area.
        max_lat (float): The maximum latitude of the rectangular area.
        min_lon (float): The minimum longitude of the rectangular area.
        max_lon (float): The maximum longitude of the rectangular area.

    Returns:
        List[Building]: A list of buildings within the rectangular area, including their associated organizations.
    """
    # Fetch all buildings with their associated organizations
    query = (
        select(Building)
        .options(joinedload(Building.organizations))
        # Filter the buildings based on the rectangular area
        .where(
            (Building.latitude >= min_lat) &
            (Building.latitude <= max_lat) &
            (Building.longitude >= min_lon) &
            (Building.longitude <= max_lon)
        )
    )
    result = await db.execute(query)
    return result.unique().scalars().all()
