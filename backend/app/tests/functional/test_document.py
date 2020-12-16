from sqlalchemy.orm import Session
from app import crud
from app.models import Dataroom
from app.models.user import User
from app.schemas import DocumentCreate


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
