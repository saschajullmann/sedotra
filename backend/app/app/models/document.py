from uuid import UUID as PyUUID
from sqlalchemy import Boolean, Column, String, ForeignKey, BigInteger, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID

from app.db.base_class import Base
from .user import User
from .dataroom import Dataroom


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
    # name must be unique in each dataroom
    name = Column(String, index=True)
    description = Column(String, nullable=True)
    file_name = Column(String, index=True, nullable=False)
    extension = Column(String, index=True, nullable=False)
    # based on this answer i decided to store the md5 of a document as uuid column type
    # https://dba.stackexchange.com/a/115316
    md5_sum = Column(UUID(as_uuid=True), index=True, nullable=False)
    mime_type = Column(String, index=True, nullable=False)
    size = Column(BigInteger, nullable=False)
    is_deleted = Column(Boolean(), nullable=False, default=False)
    is_uploaded = Column(Boolean(), nullable=False, default=False)
    created_by = Column(UUID(as_uuid=True), ForeignKey("user.id"), nullable=False)
    creator = relationship("User")
    dataroom_fk = Column(UUID(as_uuid=True), ForeignKey("dataroom.id"), nullable=False)
    dataroom = relationship("Dataroom")
    __table_args__ = (
        UniqueConstraint("name", "dataroom_fk", name="_name_per_dataroom"),
        UniqueConstraint(
            "file_name",
            "extension",
            "md5_sum",
            "dataroom_fk",
            name="_file_per_dataroom",
        ),
    )

    def __init__(
        self,
        name: str,
        description: str,
        file_name: str,
        extension: str,
        md5_sum: PyUUID,
        mime_type: str,
        size: int,
        creator: User,
        dataroom: Dataroom,
    ):
        self.name = name
        self.description = description
        self.file_name = file_name
        self.extension = extension
        self.md5_sum = md5_sum
        self.mime_type = mime_type
        self.size = size
        self.creator = creator
        self.dataroom = dataroom

    @property
    def md5(self) -> str:
        return self.md5_sum.hex

    @property
    def key(self) -> str:
        """
        String representation of the UUID id field
        to be used in object storage as key
        """
        return str(self.id)
