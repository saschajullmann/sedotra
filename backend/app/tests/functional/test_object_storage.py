from app.models.document import Document
from app.object_storage import ObjectStorage


def test_object_storage_url(object_storage: ObjectStorage, document: Document) -> None:
    """
    GIVEN a just created document
    WHEN a new url for uploading is requested
    THEN a new url object should be created with url and fields keys
    """
    url_object = object_storage.generate_post(document)
    assert "url" in url_object
    assert "fields" in url_object
    assert url_object["fields"]["Content-MD5"] == document.md5
    assert url_object["fields"]["Content-Type"] == document.mime_type


def test_object_storage_key_exists_false(object_storage: ObjectStorage) -> None:
    response = object_storage.does_key_exist("random_object.txt")
    assert response is False


def test_object_storage_key_exists_true(
    object_storage: ObjectStorage, key: str
) -> None:
    response = object_storage.does_key_exist(key)
    assert response is True
