from sqlalchemy.orm import Session
from app.db.base_class import Base
from oso import Oso
from sqlalchemy_oso.auth import register_models
from sqlalchemy_oso import set_get_session
from sqlalchemy_oso.roles import enable_roles


def init_oso(db: Session):
    oso = Oso()
    register_models(oso, Base)
    set_get_session(oso, lambda: db)
    oso.load_file("app/authorization/rules/role_basics.polar")
    oso.load_file("app/authorization/rules/organization_permissions.polar")
    oso.load_file("app/authorization/rules/team_permissions.polar")
    oso.load_file("app/authorization/rules/dataroom_permissions.polar")
    enable_roles(oso)

    return oso
