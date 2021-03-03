from typing import Optional
from uuid import UUID

from pydantic import BaseModel

from app.models import User, Organization


class DataRoomBase(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


class DataRoomCreateRequest(DataRoomBase):
    name: str


class DataRoomCreate(DataRoomCreateRequest):
    creator: User
    organization: Organization

    class Config:
        arbitrary_types_allowed = True


class DataRoomUpdate(DataRoomBase):
    pass


class DataRoomInDBBase(DataRoomBase):
    id: Optional[UUID] = None

    class Config:
        orm_mode = True
