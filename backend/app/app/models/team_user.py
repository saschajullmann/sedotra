from sqlalchemy import Table, Column, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from app.db.base_class import Base

association_table = Table(
    "team_user",
    Base.metadata,
    Column("team_fk", UUID(as_uuid=True), ForeignKey("team.id")),
    Column("user_fk", UUID(as_uuid=True), ForeignKey("user.id")),
)
