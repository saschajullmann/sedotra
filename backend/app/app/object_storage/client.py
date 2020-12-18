from dataclasses import dataclass
import boto3
from botocore.client import Config
from botocore.exceptions import ClientError
from app.core.config import settings
from app.models import Document


@dataclass
class ObjectStorage:
    service: str = "s3"
    endpoint: str = settings.OBJECT_ENDPOINT
    access_key: str = settings.OBJECT_ACCESS_KEY
    secret_key: str = settings.OBJECT_SECRET_KEY
    bucket: str = settings.OBJECT_BUCKET
    config: Config = Config(signature_version="s4v4")
    _client: boto3.client = None

    def __post_init__(self):
        my_session = boto3.session.Session()
        self._client = my_session.client(
            self.service,
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key,
            endpoint_url=self.endpoint,
            config=Config(signature_version="s3v4"),
        )

    def list_objects(self):
        return self._client.list_objects_v2(Bucket=self.bucket)

    def generate_post(self, doc: Document):
        fields = {
            "Content-MD5": str(doc.md5),
            "Content-Type": doc.mime_type,
        }
        url = self._client.generate_presigned_post(
            self.bucket, doc.key, ExpiresIn=300, Fields=fields
        )
        return url

    def does_key_exist(self, key: str) -> bool:
        try:
            self._client.head_object(Bucket=self.bucket, Key=key)
        except ClientError as e:
            if e.response["Error"]["Code"] == "404":
                # The object does not exist.
                return False
        else:
            return True
