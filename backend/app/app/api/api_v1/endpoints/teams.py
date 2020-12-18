from typing import Any, List
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.object_storage import ObjectStorage
from app.utils import (
    verify_document_is_uploaded_token,
    generate_document_is_uploaded_token,
)

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
@router.post("/{team_id}/datarooms", response_model=schemas.DataRoomInDBBase)
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


### DOCUMENT ROUTES ###
@router.post(
    "/{team_id}/datarooms/{dataroom_id}/documents",
    response_model=schemas.DocumentResponse,
)
def create_document(
    team_id: UUID,
    dataroom_id: UUID,
    document_request: schemas.DocumentCreateRequest,
    db: Session = Depends(deps.get_db),
    client: ObjectStorage = Depends(deps.get_object_client),
    current_user: models.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Create a new document under a given dataroom (which in turn belongs to a team).
    Only a person with write access to a given dataroom is able to generate a
    new document.
    With this endpoint a new document is created within the db representing the
    metadata of the respective document.
    An object storage presigned url is generated which will be returned upon
    successfull creation of the db entry.
    With that a user can upload files directly to the object storage.
    """
    splitted_filename = document_request.file_name.split(".")
    extension = splitted_filename[-1]
    file_name = "".join(splitted_filename[:-1])
    obj_in = schemas.DocumentCreate(
        dataroom_fk=dataroom_id,
        created_by=current_user.id,
        name=document_request.name,
        file_name=file_name,
        extension=extension,
        md5_sum=document_request.md5_sum,
        size=document_request.size,
        mime_type=document_request.mime_type,
    )
    try:
        document = crud.document.create(db, obj_in=obj_in)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Cannot add user - {e}")

    url_objects = client.generate_post(document)

    doc_schema = schemas.DocumentInDB.from_orm(document)

    mark_as_uploaded_token = generate_document_is_uploaded_token(str(document.id))

    response_object = {
        "document": doc_schema,
        "upload_url": url_objects["url"],
        "upload_form_fields": url_objects["fields"],
        "mark_as_uploaded_url": mark_as_uploaded_token,
    }
    return schemas.DocumentResponse(**response_object)


@router.patch(
    "/documents/{document_id}/mark_as_uploaded",
)
def mark_document_as_uploaded(
    token: str,
    current_user: models.User = Depends(deps.get_current_active_user),
    db: Session = Depends(deps.get_db),
    client: ObjectStorage = Depends(deps.get_object_client),
):
    """
    A document can only be marked as uploaded by the
    person that created the document and
    if it exists in the object_storage
    hence we need to check whether the key exists
    in the object_storage
    """
    document_id = verify_document_is_uploaded_token(token)
    if not document_id:
        raise HTTPException(status_code=400, detail="Invalid token")

    # check if key exists
    if not client.does_key_exist(document_id):
        raise HTTPException(status_code=400, detail="Document does not exist")

    document = crud.document.mark_as_uploaded(db, document_id=document_id)

    return {"msg": "Marked successfully"}