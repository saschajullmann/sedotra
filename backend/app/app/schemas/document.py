from typing import Optional, Dict
from uuid import UUID
from pydantic import BaseModel
from app.models import User, Dataroom


class DocumentBase(BaseModel):
    name: str
    description: Optional[str] = None
    file_name: str


class DocumentCreateRequest(DocumentBase):
    name: str
    file_name: str
    md5_sum: str
    size: int
    mime_type: str


class DocumentCreate(DocumentCreateRequest):
    file_name: str
    extension: str
    dataroom: Optional[Dataroom]
    creator: Optional[User]

    class Config:
        arbitrary_types_allowed = True


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
    mark_as_uploaded_url: str
    mark_as_uploaded_token: str
