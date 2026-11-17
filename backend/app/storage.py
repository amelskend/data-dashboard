import os

import boto3
from botocore.exceptions import BotoCoreError, ClientError

S3_BUCKET = os.getenv("S3_BUCKET", "datasets")

s3 = boto3.client(
    "s3",
    endpoint_url=os.getenv("S3_ENDPOINT_URL", "http://minio:9000"),
    aws_access_key_id=os.getenv("MINIO_ROOT_USER"),
    aws_secret_access_key=os.getenv("MINIO_ROOT_PASSWORD"),
    region_name=os.getenv("AWS_DEFAULT_REGION", "us-east-1"),
)


def ensure_bucket() -> None:
    try:
        s3.head_bucket(Bucket=S3_BUCKET)
    except ClientError as error:
        error_code = error.response.get("Error", {}).get("Code")
        if error_code not in {"404", "NoSuchBucket"}:
            raise
        s3.create_bucket(Bucket=S3_BUCKET)
    except BotoCoreError:
        return