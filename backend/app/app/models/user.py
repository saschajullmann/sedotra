from sqlalchemy import Boolean, Column, String

from app.db.base_class import Base


class User(Base):
    __tablename__ = "user"
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean(), default=True)
    is_superuser = Column(Boolean(), default=False)

    def __init__(
        self, first_name: str, last_name: str, email: str, hashed_password: str
    ):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.hashed_password = hashed_password
