from sqlalchemy.orm import Session
from app import crud
from app.models import Team, User
from app.schemas.team import TeamCreate


def test_create_team(db: Session, admin_user: User) -> None:
    team_name = "random_test"
    team_in = TeamCreate(name=team_name, created_by=admin_user.id, is_active=True)
    team: Team = crud.team.create(db, obj_in=team_in)
    assert team.name == team_name
    assert team.created_by == admin_user.id


def test_add_user_to_team(
    db: Session, admin_user: User, normal_user: User, team: Team
) -> None:
    # add user to team
    crud.team.add_user(db, team_id=team.id, user_id=normal_user.id)

    # verify that user was added to team
    normal_user_teams = crud.user.get_teams(db, user_id=normal_user.id)

    assert team.id in [item.id for item in normal_user_teams]
