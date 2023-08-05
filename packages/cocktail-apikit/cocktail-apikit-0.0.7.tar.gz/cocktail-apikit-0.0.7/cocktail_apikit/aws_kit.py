from datetime import datetime

import boto3
from botocore.config import Config
from .settings_kit import DefaultSettings


class S3Helper:
    AWS_CONFIG = None

    def __init__(self):
        print('aws configuration:', DefaultSettings.AWS_REGION, DefaultSettings.BUCKET_NAME, '\n')
        self.client = boto3.client('s3', region_name=DefaultSettings.AWS_REGION,
                                   config=Config(s3={'addressing_style': 'auto'}))
        self.bucket_name = DefaultSettings.BUCKET_NAME
        self.resource = boto3.resource('s3', region_name=DefaultSettings.AWS_REGION,
                                       config=Config(s3={'addressing_style': 'path'}))
        self.bucket = self.resource.Bucket(self.bucket_name)

    def upload_file_obj(self, file_obj, key_name):
        self.client.upload_fileobj(file_obj, self.bucket_name, key_name)

    def get_object_presigned_url(self, key_name: str = None, expires_in: int = None) -> str:
        expires_in = expires_in or 24 * 60 * 60  # one day
        now = datetime.now()
        expires_in = expires_in - (now.hour * 60 * 60 + now.minute * 60 + now.second)
        return self.client.generate_presigned_url(
            'get_object',
            Params={'Bucket': self.bucket_name, 'Key': key_name},
            ExpiresIn=expires_in
        )
