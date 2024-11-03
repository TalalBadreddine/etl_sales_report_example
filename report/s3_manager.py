import boto3
from io import BytesIO
import os

class S3Manager:
    def __init__(self):
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
        )
        self.bucket_name = os.getenv('AWS_S3_BUCKET_NAME')

    def upload_file(self, file_content, s3_file_path):
        """
        Uploads a file to the specified S3 bucket.

        :param file_content: The content of the file to upload (as bytes or a file-like object).
        :param s3_file_path: The path where the file will be stored in the S3 bucket.
        """
        if isinstance(file_content, bytes):
            file_content = BytesIO(file_content)

        self.s3_client.upload_fileobj(file_content, self.bucket_name, s3_file_path)