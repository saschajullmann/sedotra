from typing import Any
from sqlalchemy.orm import Session
from uuid import UUID

from app.crud.base import CRUDBase
from app.models.document import Document
from app.schemas.dataroom import DataRoomCreate, DataRoomUpdate


class CRUDDocument(CRUDBase[Document, DataRoomCreate, DataRoomUpdate]):
    pass


document = CRUDDocument(Document)
