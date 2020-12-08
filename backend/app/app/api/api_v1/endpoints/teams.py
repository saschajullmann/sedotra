from typing import Any, List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


@router.post("/", response_model=schemas.TeamInDBBase)
def create_team(
    *,
    db: Session = Depends(deps.get_db),
    team_in: schemas.TeamCreateRequest,
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Create new team. Only superuser is allowed to create new teams
    """
    team_db_create = schemas.TeamCreate(
        name=team_in.name,
        description=team_in.description,
        created_by=current_user.id,
        is_active=True,
    )

    team = crud.team.create(db, obj_in=team_db_create)
    return team


@router.post("/{team_id}/user/{user_id}")
def add_user_to_team(
    team_id: UUID,
    user_id: UUID,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_superuser),
) -> Any:
    """
    Add a user to a team
    """
    try:
        crud.team.add_user(db, team_id=team_id, user_id=user_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Cannot add user - {e}")
    return "OK"


# DataRoom routes
@router.post("/{team_id}/datarooms", response_model=List[schemas.DataRoomBase])
def create_dataroom(
    team_id: UUID,
    dataroom_request: schemas.DataRoomCreateRequest,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create a new dataroom under a given team
    Only teammembers and superadmins are allowed to create a dataroom
    """

    # verify that requesting user is superuser
    # of belongs to the team in question
    is_superuser = current_user.is_superuser
    belongs_to_team = team_id in [team.id for team in current_user.teams]

    if not is_superuser or not belongs_to_team:
        raise HTTPException(
            status_code=400,
            detail="You don't have the privileges to create a room in that team",
        )
    dataroom_create = schemas.DataRoomCreate(
        name=dataroom_request.name,
        description=dataroom_request.description,
        created_by=current_user.id,
        team_fk=team_id,
    )

    try:
        dataroom = crud.dataroom.create(db, obj_in=dataroom_create)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Cannot add user - {e}")

    return dataroom


@router.get("/{team_id}/datarooms", response_model=List[schemas.DataRoomInDBBase])
def get_datarooms_per_team(
    team_id: UUID,
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Get all datarooms under a given team
    Only teammembers are allowed to get a dataroom
    """

    if team_id not in [team.id for team in current_user.teams]:
        raise HTTPException(
            status_code=404, detail="User is not allowed to see datarooms"
        )

    try:
        datarooms = crud.dataroom.get_multi(db)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Cannot add user - {e}")

    return datarooms