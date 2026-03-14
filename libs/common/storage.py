from __future__ import annotations
import os
from typing import BinaryIO, Optional
import boto3
from botocore.client import Config
from .config import settings

def s3_client():
    return boto3.client(
        "s3",
        endpoint_url=settings.S3_ENDPOINT,
        aws_access_key_id=settings.S3_ACCESS_KEY,
        aws_secret_access_key=settings.S3_SECRET_KEY,
        config=Config(signature_version="s3v4"),
        region_name="us-east-1",
    )

def upload_file(local_path: str, bucket: str, key: str) -> str:
    if not os.path.exists(local_path):
        raise FileNotFoundError(local_path)
    client = s3_client()
    client.upload_file(local_path, bucket, key)
    return f"s3://{bucket}/{key}"

def download_file(bucket: str, key: str, local_path: str) -> str:
    os.makedirs(os.path.dirname(local_path), exist_ok=True)
    client = s3_client()
    client.download_file(bucket, key, local_path)
    return local_path