from sqlalchemy import Boolean, Column, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

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
