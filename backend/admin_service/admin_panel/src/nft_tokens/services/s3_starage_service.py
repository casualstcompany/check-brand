import logging

import boto3
from botocore.client import Config
from django.conf import settings

logger = logging.getLogger(__name__)


class PreSignedUrlS3StorageService:
    s3_client = None
    ACCESS_KEY = None
    SECRET_KEY = None
    URL = None
    BUCKET_NAME = None
    EXPIRES_IN = None

    def __init__(
        self,
    ):
        self._get_config_s3_aws()
        self.s3_client = boto3.client(
            "s3",
            aws_access_key_id=self.ACCESS_KEY,
            aws_secret_access_key=self.SECRET_KEY,
            endpoint_url=self.URL,
            config=Config(signature_version="s3v4"),
        )

    def _get_config_s3_aws(self):
        self.ACCESS_KEY = settings.AWS_ACCESS_KEY_ID
        self.SECRET_KEY = settings.AWS_SECRET_ACCESS_KEY
        self.URL = settings.AWS_S3_ENDPOINT_URL
        self.BUCKET_NAME = settings.AWS_S3_BUCKET_NAME
        self.EXPIRES_IN = settings.AWS_S3_PRE_SIGNED_EXPIRES_IN

    def _get_post_pre_signed_url_data_by_key(self, key: str):
        """Тоже рабочий метод, но не загружает файлы больше 30 мб (хз почему)"""
        data = self.s3_client.generate_presigned_post(
            Bucket=self.BUCKET_NAME, Key=key, ExpiresIn=self.EXPIRES_IN
        )
        return data

    def _get_put_pre_signed_url_data_by_key(self, key: str):
        data = self.s3_client.generate_presigned_url(
            "put_object",
            Params={
                "Bucket": self.BUCKET_NAME,
                "Key": key,
            },
            ExpiresIn=self.EXPIRES_IN,
            HttpMethod="PUT",
        )
        return data

    def execute(self, filename: str) -> dict:

        if filename and filename[0] == "/":
            filename = filename[1:]

        data = self._get_put_pre_signed_url_data_by_key(key=filename)
        return data
