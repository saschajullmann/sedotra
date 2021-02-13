import os
import time
import hashlib
import mimetypes
import requests
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

    # Read in test document from disk
    with open("./tests/data/my_test_doc.txt", "r", encoding="utf-8") as test_doc:
        doc_contents = test_doc.read().encode("utf-8")

        # calculate md5 sum of documents contents
        md5_hash = hashlib.md5()
        md5_hash.update(doc_contents)
        digest = md5_hash.hexdigest().encode("utf-8")
        md5_string = digest.decode("utf-8")

        # make api request to create new document
        file_name = os.path.basename(test_doc.name)
        new_document_request = {
            "name": "My Test Document",
            "file_name": file_name,
            "md5_sum": md5_string,
            "size": 45,
            "mime_type": "text/plain",
        }

        response = client.post(
            f"{settings.API_V1_STR}/teams/{dataroom.team_fk}/datarooms/{dataroom.id}/documents",
            headers=user_authentication_headers,
            json=new_document_request,
        )
        assert response.status_code == 200

        # grab urls and tokens for subsequent requests
        response_data = response.json()
        document_id = response_data["document"]["id"]
        upload_payload = response_data["upload_form_fields"]
        upload_url = response_data["upload_url"]
        mark_as_uploaded_url = response_data["mark_as_uploaded_url"]
        mark_as_uploaded_token = response_data["mark_as_uploaded_token"]
        files = {"file": doc_contents}

        # upload file to object storage
        r = requests.post(url=upload_url, data=upload_payload, files=files)

        assert r.status_code == 204

        mark_as_uploaded_payload = {"token": mark_as_uploaded_token}

        # mark file as uploaded
        response = client.patch(
            mark_as_uploaded_url,
            headers=user_authentication_headers,
            params=mark_as_uploaded_payload,
        )
        assert response.status_code == 200

        # verify that document was indeed marked as uploaded
        db_document = crud.document.get(db, document_id)

        assert db_document.is_uploaded
