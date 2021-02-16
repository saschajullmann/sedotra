from sqlalchemy.orm import Session
from app.db.base_class import Base
from oso import Oso
from sqlalchemy_oso import register_models, set_get_session
from sqlalchemy_oso.roles import enable_roles


def init_oso(db: Session):
    oso = Oso()
    register_models(oso, Base)
    set_get_session(oso, lambda: db)
    oso.load_file("app/authorization/rules/rules.polar")
    enable_roles(oso)

    return oso
