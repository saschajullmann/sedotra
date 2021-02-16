from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.team import Team
from app.models.user import User
from app.schemas.team import TeamCreate, TeamUpdate


class CRUDTeam(CRUDBase[Team, TeamCreate, TeamUpdate]):
    def create(self, db: Session, *, obj_in: TeamCreate) -> Team:
        creating_user_id = obj_in.created_by
        user = db.query(User).filter_by(id=creating_user_id).first()
        db_obj = Team(
            name=obj_in.name,
            description=obj_in.description,
            created_by=creating_user_id,
        )
        user.teams.append(db_obj)
        db.add_all([db_obj, user])
        db.commit()
        db.refresh(db_obj)
        return db_obj


team = CRUDTeam(Team)
