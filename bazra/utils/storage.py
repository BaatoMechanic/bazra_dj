import os

from storages.backends.s3boto3 import S3Boto3Storage
from botocore.client import Config


class StaticFileStorage(S3Boto3Storage):
    """
    For staticfiles
    """

    bucket_name = os.environ.get("PRIVATE_BUCKET_NAME")
    location = "static"
    default_acl = "public-read"


class MediaFileStorage(S3Boto3Storage):
    """
    For general public uploads
    """

    bucket_name = os.environ.get("PUBLIC_BUCKET_NAME")
    location = "media"
    default_acl = "public-read"


class PrivateMediaStorage(S3Boto3Storage):
    access_key = os.environ.get("PRIVATE_BUCKET_ACCESS_KEY")
    secret_key = os.environ.get("PRIVATE_BUCKET_SECRET_KEY")
    bucket_name = os.environ.get("PRIVATE_BUCKET_NAME")
    location = "media"
    default_acl = "private"
    custom_domain = False
    file_overwrite = False
    endpoint_url = os.environ.get("PRIVATE_BUCKET_ENDPOINT_URL")

    config = Config(signature_version="s3v4")

    def __init__(self, *args, **kwargs):
        kwargs["access_key"] = self.access_key
        kwargs["secret_key"] = self.secret_key
        kwargs["bucket_name"] = self.bucket_name
        kwargs["endpoint_url"] = self.endpoint_url
        kwargs["region_name"] = os.environ.get("PRIVATE_BUCKET_REGION_NAME", "auto")
        super().__init__(*args, **kwargs)
