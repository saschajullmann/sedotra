from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class DataRoomBase(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None


class DataRoomCreateRequest(DataRoomBase):
    name: str


class DataRoomCreate(DataRoomCreateRequest):
    created_by: UUID
    team_fk: UUID


class DataRoomUpdate(DataRoomBase):
    pass


class DataRoomInDBBase(DataRoomBase):
    id: Optional[UUID] = None

    class Config:
        orm_mode = True