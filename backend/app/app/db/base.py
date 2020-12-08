# Import all the models, so that Base has them before being
# imported by Alembic
from app.db.base_class import Base  # noqa
from app.models.user import User  # noqa
from app.models.dataroom import Dataroom  # noqa
from app.models.team import Team  # noqa
from app.models.team_user import association_table  # noqa
