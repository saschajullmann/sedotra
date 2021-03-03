from app.db.base_class import Base
from app.models import Team, User
from sqlalchemy_oso.roles import resource_role_class

# ROLE MODELS ##
TeamRoleMixin = resource_role_class(Base, User, Team, ["OWNER", "ADMIN", "MEMBER"])


class TeamRole(Base, TeamRoleMixin):
    pass
