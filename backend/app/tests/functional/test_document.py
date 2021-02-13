from sqlalchemy.orm import Session
from fastapi.testclient import TestClient
from app import crud
from app.core.config import settings
from app.models import Dataroom, Document
from app.models.user import User
from app.schemas import DocumentCreate, DocumentCreateRequest


def test_create_document(db: Session, normal_user: User, dataroom: Dataroom) -> None:
    """
    GIVEN an existing dataroom
    WHEN a new document is created in that dataroom
    THEN the metadata should exist in form of db entry
        and is_deleted and is_uploaded should both be False
    """
    obj_in = DocumentCreate(
        name="Test Doc",
        file_name="hello",
        extension="txt",
        mime_type="text/plain",
        md5_sum="87a6909ab71ec463f013325dbf9f3523",
        size=466730,
        dataroom_fk=dataroom.id,
        created_by=normal_user.id,
    )
    metadata = crud.document.create(db, obj_in=obj_in)

    assert metadata.is_deleted is False
    assert metadata.is_uploaded is False


def test_mark_document_as_uploaded(
    db: Session, normal_user: User, document: Document
) -> None:
    """
    GIVEN an existing not yet uploaded document
    WHEN the "mark_as_uploaded" function is called
    THEN the document should be marked as uploaded in db
    """
    assert document.is_uploaded is False
    new_obj = crud.document.mark_as_uploaded(db, document_id=document.id)
    assert new_obj.is_uploaded is True


def test_document_creation(
    db: Session,
    user_authentication_headers: dict,
    dataroom: Dataroom,
    client: TestClient,
) -> None:
    """
    This test is responsible for the whole process of uploading a document
    From creating the metadata in the DB, to uploading file in object storage
    To marking a file as uploaded
    """

    # First the user needs to create the document in db
    new_document_request = {
        "name": "My Test Document",
        "file_name": "my_test_doc.txt",
        "md5_sum": "226fd09401d3799e3f1c164a08ae5c43",
        "size": 45,
        "mime_type": "text/plain",
    }

    response = client.post(
        f"{settings.API_V1_STR}/teams/{dataroom.team_fk}/datarooms/{dataroom.id}/documents",
        headers=user_authentication_headers,
        json=new_document_request,
    )
    assert response.status_code == 200
