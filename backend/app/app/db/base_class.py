from sqlalchemy import text, Column, func, DateTime

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import UUID


class Base(object):
    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        nullable=False,
        index=True,
        server_default=text("uuid_generate_v4()"),
    )
    created_at = Column(DateTime, nullable=False, index=True, server_default=func.now())
    updated_at = Column(
        DateTime,
        nullable=False,
        index=True,
        server_default=func.now(),
        onupdate=func.now(),
    )


Base = declarative_base(cls=Base)
