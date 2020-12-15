from typing import Optional
from uuid import UUID
from pydantic import BaseModel


class DocumentBase(BaseModel):
    name: str
    description: Optional[str] = None
    file_name: str
    dataroom_fk: Optional[UUID] = None
    created_by: Optional[UUID] = None


class DocumentCreate(DocumentBase):
    name: str
    file_name: str
    md5_sum: str
    size: int


class DocumentUpdate(DocumentBase):
    pass


class DocumentInDB(DocumentBase):
    id: UUID

    class config:
        orm_mode = True
