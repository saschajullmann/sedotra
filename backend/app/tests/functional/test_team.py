from sqlalchemy.orm import Session
from app import crud
from app.models import Team, User, Organization
from app.schemas.team import TeamCreate


def test_create_team(db: Session, admin_user: User, organization: Organization) -> None:
    team_name = "random_test"
    team_in = TeamCreate(
        name=team_name,
        creator=admin_user,
        is_active=True,
        organization=organization,
    )
    team: Team = crud.team.create(db, obj_in=team_in)
    assert team.name == team_name
    assert team.created_by == admin_user.id
