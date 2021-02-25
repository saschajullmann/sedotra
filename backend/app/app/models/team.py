from sqlalchemy import Boolean, Column, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from .user import User
from .organization import Organization

from app.db.base_class import Base


class Team(Base):
    __tablename__ = "team"
    name = Column(String, index=True)
    description = Column(String, nullable=True)
    is_active = Column(Boolean(), nullable=False, default=True)
    created_by = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)
    creator = relationship("User")
    organization_fk = Column(
        UUID(as_uuid=True), ForeignKey("organization.id"), nullable=False
    )
    organization = relationship("Organization")

    def __init__(
        self,
        name: str,
        description: str,
        is_active: bool,
        creator: User,
        organization: Organization,
    ):
        self.name = name
        self.description = description
        self.is_active = is_active
        self.creator = creator
        self.organization = organization
