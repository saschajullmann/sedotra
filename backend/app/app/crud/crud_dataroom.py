from typing import List
from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.models.dataroom import Dataroom, Organization
from app.schemas.dataroom import DataRoomCreate, DataRoomUpdate


class CRUDDataRoom(CRUDBase[Dataroom, DataRoomCreate, DataRoomUpdate]):
    def get_multi_by_org(
        self, db: Session, org: Organization, skip: int = 0, limit: int = 100
    ) -> List[Dataroom]:
        return (
            db.query(self.model)
            .filter_by(organization=org)
            .offset(skip)
            .limit(limit)
            .all()
        )


dataroom = CRUDDataRoom(Dataroom)
