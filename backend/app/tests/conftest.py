import os
import pytest
from typing import Dict, Generator

from oso import Oso
from sqlalchemy_oso import roles as oso_roles
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session, close_all_sessions

from app import crud
from app.core.config import settings
from app.authorization.oso import init_oso
from app.main import app
from app.api.deps import get_db
from app.db import base
from app.models import Team, User, Document, Dataroom, Organization
from app.object_storage import ObjectStorage
from app.schemas import UserCreate, DocumentCreate, OrgCreate
from app.schemas.dataroom import DataRoomCreate
from .fixtures.role_data import load_role_fixtures, Data


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
def engine() -> Generator:
    engine = create_engine(
        settings.SQLALCHEMY_DATABASE_TEST_URI, pool_pre_ping=True, pool_size=20
    )
    base.Base.metadata.create_all(engine)  # type: ignore

    yield engine

    base.Base.metadata.drop_all(engine)  # type: ignore


@pytest.fixture(scope="module")
def db(engine) -> Generator:
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session: Session = SessionLocal()
    yield session
    close_all_sessions()


@pytest.fixture(scope="module")
def oso(db) -> Oso:
    return init_oso(db)


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
def data(db) -> Data:
    data = load_role_fixtures(db)
    return data


@pytest.fixture(scope="module")
def admin_user(db: Session) -> User:
    email = "admin@admin.com"
    password = "super_admin"
    user_in = UserCreate(email=email, password=password, is_superuser=True)
    return crud.user.create(db, obj_in=user_in)


@pytest.fixture(scope="module")
def organization(db: Session) -> Organization:
    org_in = OrgCreate(name="My Org", is_active=True)
    return crud.org.create(db, obj_in=org_in)


@pytest.fixture(scope="module")
def org_admin(db: Session, admin_user: User, organization: Organization) -> User:
    oso_roles.add_user_role(db, admin_user, organization, "ADMIN", commit=True)
    return admin_user


@pytest.fixture(scope="module")
def org_lead(db: Session, normal_user: User, organization: Organization) -> User:
    oso_roles.add_user_role(db, normal_user, organization, "LEAD", commit=True)
    return normal_user


@pytest.fixture(scope="module")
def team(db: Session, admin_user: User, organization: Organization) -> Team:
    new_team = Team(
        name="Fake Name",
        description="this is a test team",
        is_active=True,
        creator=admin_user,
        organization=organization,
    )
    db.add(new_team)
    db.commit()
    db.refresh(new_team)
    return new_team


@pytest.fixture(scope="module")
def normal_user(db: Session) -> User:
    email = NORMAL_USER_EMAIL
    password = NORMAL_USER_PW
    user_in = UserCreate(
        email=email, password=password, is_superuser=False, is_active=True
    )
    return crud.user.create(db, obj_in=user_in)


@pytest.fixture(scope="module")
def dataroom(db: Session, organization: Organization, normal_user: User) -> Dataroom:
    dataroom_in = DataRoomCreate(
        name="Test Room", creator=normal_user, organization=organization
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
        dataroom=dataroom,
        creator=normal_user,
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
