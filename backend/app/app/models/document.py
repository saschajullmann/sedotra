from sqlalchemy import Boolean, Column, String, ForeignKey, BigInteger
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from app.db.base_class import Base


class Document(Base):
    __tablename__ = "document"
    name = Column(String, index=True, unique=True)
    description = Column(String, nullable=True)
    file_name = Column(String, index=True)
    md5_sum = Column(UUID(as_uuid=True), index=True)
    size = Column(BigInteger, nullable=False)
    is_deleted = Column(Boolean(), nullable=False, default=False)
    is_uploaded = Column(Boolean(), nullable=False, default=False)
    created_by = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)
    creator = relationship("User")
    dataroom_fk = Column(UUID(as_uuid=True), ForeignKey("dataroom.id"), nullable=False)
    dataroom = relationship("Dataroom")
