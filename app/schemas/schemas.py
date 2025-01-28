from pydantic import BaseModel, ConfigDict
from pydantic_extra_types.coordinate import Latitude, Longitude
from typing import List


class ActivityBase(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(
        from_attributes = True
    )

class BuildingBase(BaseModel):
    id: int
    address: str
    latitude: Latitude
    longitude: Longitude

    model_config = ConfigDict(
        from_attributes=True
    )

class OrganizationBase(BaseModel):
    id: int
    name: str
    phone_numbers: List[str]  
    activities: List[ActivityBase] 

    model_config = ConfigDict(
        from_attributes=True
    )

class BuildingWithOrganizationsResponse(BuildingBase):
    organizations: List[OrganizationBase] 

    model_config = ConfigDict(
        from_attributes=True
    )

class OrganizationWithBuilding(OrganizationBase):
    building: BuildingBase 

    model_config = ConfigDict(
        from_attributes=True
    )
