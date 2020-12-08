import pytest
from typing import Dict, Generator

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session, Session

from app import crud
from app.core.config import settings
from app.main import app
from app.db import base
from app.models import Team, User
from app.schemas import UserCreate
from app.schemas.team import TeamCreate


engine = create_engine(settings.SQLALCHEMY_DATABASE_TEST_URI, pool_pre_ping=True)
ScopedSession = scoped_session(sessionmaker(bind=engine))
# SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture(scope="module")
def db() -> Generator:
    base.Base.metadata.create_all(bind=engine)
    yield ScopedSession()
    ScopedSession().close()
    base.Base.metadata.drop_all(bind=engine)


@pytest.fixture(scope="module")
def client() -> Generator:
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
    email = "normal@normal.com"
    password = "my_password"
    user_in = UserCreate(email=email, password=password, is_superuser=False)
    return crud.user.create(db, obj_in=user_in)