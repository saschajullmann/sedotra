from typing import Any
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps
from app.object_storage import ObjectStorage
from app.utils import (
    generate_document_is_uploaded_token,
    verify_document_is_uploaded_token,
)

router = APIRouter()


@router.post(
    "/{org_id}/datarooms/{dataroom_id}/documents",
    response_model=schemas.DocumentResponse,
)
def create_document(
    request: Request,
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
    dataroom = crud.dataroom.get(db, id=dataroom_id)
    obj_in = schemas.DocumentCreate(
        dataroom=dataroom,
        creator=current_user,
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

    url_for_mark_as_uploaded_url = request.url_for(
        "mark_document_as_uploaded",
        **{"document_id": document.id},
    )

    response_object = {
        "document": doc_schema,
        "upload_url": url_objects["url"],
        "upload_form_fields": url_objects["fields"],
        "mark_as_uploaded_url": url_for_mark_as_uploaded_url,
        "mark_as_uploaded_token": mark_as_uploaded_token,
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

    crud.document.mark_as_uploaded(db, document_id=document_id)

    return {"msg": "Marked successfully"}
