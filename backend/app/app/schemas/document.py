from typing import Optional, Dict
from uuid import UUID
from pydantic import BaseModel


class DocumentBase(BaseModel):
    name: str
    description: Optional[str] = None
    file_name: str
    dataroom_fk: Optional[UUID] = None
    created_by: Optional[UUID] = None


class DocumentCreateRequest(DocumentBase):
    name: str
    file_name: str
    md5_sum: str
    size: int
    mime_type: str


class DocumentCreate(DocumentCreateRequest):
    file_name: str
    extension: str


class DocumentUpdate(DocumentBase):
    pass


class DocumentInDB(DocumentBase):
    id: UUID
    extension: str

    class Config:
        orm_mode = True


class DocumentResponse(BaseModel):
    document: DocumentInDB
    upload_url: str
    upload_form_fields: Dict
