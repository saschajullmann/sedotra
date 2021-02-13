from app.models import Document
from app.utils import (
    generate_document_is_uploaded_token,
    verify_document_is_uploaded_token,
)


def test_document_is_uploaded_token(document: Document):
    """
    GIVEN that new document metadata was added to db
    WHEN a document_id is supplied to the function
    THEN a new JWT should be created with that document_id embedded
    """
    new_token = generate_document_is_uploaded_token(str(document.id))
    decoded = verify_document_is_uploaded_token(new_token)
    assert decoded == str(document.id)
