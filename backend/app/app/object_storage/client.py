import boto3
from botocore.client import Config
from app.core.config import settings

client = boto3.client(
    "s3",
    aws_access_key_id=settings.OBJECT_ACCESS_KEY,
    aws_secret_access_key=settings.OBJECT_SECRET_KEY,
    endpoint_url=settings.OBJECT_ENDPOINT,
    config=Config(signature_version="s3v4"),
)
