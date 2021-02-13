from typing import Any
from sqlalchemy.orm import Session
from uuid import UUID

from app.crud.base import CRUDBase
from app.models.document import Document
from app.schemas.document import DocumentCreate, DocumentUpdate


class CRUDDocument(CRUDBase[Document, DocumentCreate, DocumentUpdate]):
    def mark_as_uploaded(self, db: Session, *, document_id: UUID) -> Document:
        db_obj: Document = db.query(Document).filter(Document.id == document_id).first()
        db_obj.is_uploaded = True
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


document = CRUDDocument(Document)
