from app.crud.base import CRUDBase
from app.models.dataroom import Dataroom
from app.schemas.dataroom import DataRoomCreate, DataRoomUpdate


class CRUDDataRoom(CRUDBase[Dataroom, DataRoomCreate, DataRoomUpdate]):
    pass


dataroom = CRUDDataRoom(Dataroom)
