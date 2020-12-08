from uuid import UUID
from typing import Optional

from pydantic import BaseModel, EmailStr


# Shared properties
class TeamBase(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = True


class TeamCreateRequest(BaseModel):
    name: str
    description: Optional[str] = None


class TeamCreate(TeamCreateRequest):
    is_active: bool
    created_by: UUID


class TeamUpdate(TeamBase):
    pass


class TeamInDBBase(TeamBase):
    id: Optional[UUID] = None

    class Config:
        orm_mode = True


# Additional properties to return via API
class Team(TeamInDBBase):
    pass