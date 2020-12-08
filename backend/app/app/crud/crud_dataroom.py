from typing import Any
from sqlalchemy.orm import Session
from uuid import UUID

from app.crud.base import CRUDBase
from app.models.dataroom import Dataroom
from app.schemas.dataroom import DataRoomCreate, DataRoomUpdate


class CRUDDataRoom(CRUDBase[Dataroom, DataRoomCreate, DataRoomUpdate]):
    def create(self, db: Session, *, obj_in: DataRoomCreate) -> Dataroom:
        db_obj = Dataroom(
            name=obj_in.name,
            description=obj_in.description,
            created_by=obj_in.created_by,
            team_fk=obj_in.team_fk,
        )
        db.add_all([db_obj])
        db.commit()
        db.refresh(db_obj)
        return db_obj


dataroom = CRUDDataRoom(Dataroom)
