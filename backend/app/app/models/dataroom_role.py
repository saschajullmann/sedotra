from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base_class import Base
from app.models import Dataroom, User
from sqlalchemy_oso.roles import resource_role_class

DataRoomRoleMixin = resource_role_class(
    declarative_base=Base,
    user_model=User,
    resource_model=Dataroom,
    role_choices=["OWNER", "ADMIN", "MEMBER", "GUEST"],
)


class DataRoomRole(Base, DataRoomRoleMixin):
    team_id = Column(Integer, ForeignKey("team.id"))
    team = relationship("Team", backref="dataroom_roles", lazy=True)
