from sqlalchemy import Boolean, Column, String, ForeignKey, BigInteger
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from app.db.base_class import Base


"""
The idea for the creating documents in the system is as follows:
Upon a POST request to the specific documents endpoint the documents
metadata is stored in the db.
When the metadata could be stored successfully in the db then
a upload url is returned which enables the frontend to upload the file
to the object storage (e.g. S3).
After a successful upload to the object storage a second call needs
to be made to the documents endpoint which marks a document as 'uploaded'
"""


class Document(Base):
    __tablename__ = "document"
    name = Column(String, index=True, unique=True)
    description = Column(String, nullable=True)
    file_name = Column(String, index=True)
    # based on this answer i decided to store the md5 of a document as uuid column type
    # https://dba.stackexchange.com/a/115316
    md5_sum = Column(UUID(as_uuid=True), index=True)
    size = Column(BigInteger, nullable=False)
    is_deleted = Column(Boolean(), nullable=False, default=False)
    is_uploaded = Column(Boolean(), nullable=False, default=False)
    created_by = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)
    creator = relationship("User")
    dataroom_fk = Column(UUID(as_uuid=True), ForeignKey("dataroom.id"), nullable=False)
    dataroom = relationship("Dataroom")
