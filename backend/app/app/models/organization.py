from sqlalchemy import Boolean, Column, String

from app.db.base_class import Base


class Organization(Base):
    __tablename__ = "organization"
    name = Column(String, index=True, unique=True)
    description = Column(String, nullable=True)
    is_active = Column(Boolean(), nullable=False, default=True)

    def __init__(self, name: str, description: str):
        self.name = name
        self.description = description
