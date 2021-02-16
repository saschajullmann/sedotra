import os
import pytest
import time
from tempfile import NamedTemporaryFile
from typing import Dict, Generator

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session, Session

from app import crud
from app.core.config import settings
from app.authorization.oso import init_oso
from app.main import app
from app.api.deps import get_db
from app.db import base
from app.models import Team, User, Document, Dataroom
from app.object_storage import ObjectStorage
from app.schemas import UserCreate, DocumentCreate
from app.schemas.dataroom import DataRoomCreate
from app.schemas.team import TeamCreate


engine = create_engine(settings.SQLALCHEMY_DATABASE_TEST_URI, pool_pre_ping=True)
ScopedSession = scoped_session(sessionmaker(bind=engine))
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

NORMAL_USER_EMAIL = "normal@normal.com"
NORMAL_USER_PW = "my_password"


@pytest.fixture(scope="module")
def object_storage() -> Generator:
    # instantiate ObjectStorage class with
    # testing bucket (testing bucket needs to be
    # created by hand)
    object_storage = ObjectStorage(bucket="sedotra-test")
    object_storage._client.create_bucket(Bucket=object_storage.bucket)
    yield object_storage
    object_storage._client.delete_bucket(Bucket=object_storage.bucket)


@pytest.fixture(scope="module")
def db() -> Generator:
    base.Base.metadata.create_all(bind=engine)
    yield ScopedSession()
    ScopedSession().close()
    base.Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="module")
def oso(db) -> Generator:
    oso_client = init_oso(db)
    yield oso_client


@pytest.fixture(scope="module")
def client(db) -> Generator:
    """
    The test client needs the same database access
    as the rest of the fixtures so that the test db
    can be prepared before the client accesses the data
    """

    def override_get_db():
        try:
            yield db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="module")
def admin_user(db: Session) -> Dict[str, str]:
    email = "admin@admin.com"
    password = "super_admin"
    user_in = UserCreate(email=email, password=password, is_superuser=True)
    return crud.user.create(db, obj_in=user_in)


@pytest.fixture(scope="module")
def team(db: Session, admin_user: User) -> Team:
    team_in = TeamCreate(name="random_team", is_active=True, created_by=admin_user.id)
    return crud.team.create(db, obj_in=team_in)


@pytest.fixture(scope="module")
def normal_user(db: Session) -> Dict[str, str]:
    email = NORMAL_USER_EMAIL
    password = NORMAL_USER_PW
    user_in = UserCreate(
        email=email, password=password, is_superuser=False, is_active=True
    )
    return crud.user.create(db, obj_in=user_in)


@pytest.fixture(scope="module")
def dataroom(db: Session, team: Team, normal_user: User) -> Dataroom:
    dataroom_in = DataRoomCreate(
        name="Test Room", created_by=normal_user.id, team_fk=team.id
    )
    return crud.dataroom.create(db, obj_in=dataroom_in)


@pytest.fixture(scope="module")
def document(db: Session, dataroom: Dataroom, normal_user: User) -> Document:
    obj_in = DocumentCreate(
        name="Test Document",
        file_name="test_doc",
        extension="txt",
        mime_type="text/plain",
        md5_sum="87a6909ab71ec463f013325dbf9f3545",
        size=466730,
        dataroom_fk=dataroom.id,
        created_by=normal_user.id,
    )
    return crud.document.create(db, obj_in=obj_in)


@pytest.fixture(scope="module")
def key(object_storage: ObjectStorage) -> Generator:
    random_file = "random_file.txt"
    with open(random_file, "w") as file:
        file.write("Blah blah")

    object_storage._client.upload_file(
        file.name, Bucket=object_storage.bucket, Key=file.name
    )
    yield file.name
    os.remove(random_file)
    object_storage._client.delete_object(Bucket=object_storage.bucket, Key=file.name)


@pytest.fixture(scope="module")
def user_authentication_headers(
    *, client: TestClient, normal_user: User
) -> Dict[str, str]:
    data = {"username": normal_user.email, "password": NORMAL_USER_PW}

    r = client.post(f"{settings.API_V1_STR}/login/access-token", data=data)
    response = r.json()
    auth_token = response["access_token"]
    headers = {"Authorization": f"Bearer {auth_token}"}
    return headers
