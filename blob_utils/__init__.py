from flask import request, current_app
import boto3
from botocore.client import Config
from .constants import (
    S3_ACCESS_KEY_ID,
    S3_BUCKET,
    S3_SECRET_ACCESS_KEY,
    S3_ENDPOINT_URL,
    S3_REGION_NAME,
    S3_PRESIGNED_TIMEOUT,
)

def get_s3():
    """ Get access to the Boto s3 service. """

    params = {
        "endpoint_url": current_app.config[S3_ENDPOINT_URL],
        "config": Config(signature_version="s3v4"),
        "region_name": current_app.config[S3_REGION_NAME],
    }
    if S3_ACCESS_KEY_ID in current_app.config:
        params["aws_access_key_id"] = current_app.config[S3_ACCESS_KEY_ID]
        params["aws_secret_access_key"] = current_app.config[S3_SECRET_ACCESS_KEY]

    return boto3.client("s3", **params)


def upload_stream(key, stream):
    """ Upload a io stream to an s3 bucket with the specified key. """

    bucket = current_app.config[S3_BUCKET]
    s3_client = get_s3()
    if bucket not in [b["Name"] for b in s3_client.list_buckets()["Buckets"]]:
        s3_client.create_bucket(ACL="private", Bucket=bucket)
    s3_client.upload_fileobj(
        stream,
        bucket,
        key,
    )


def create_url(key):
    """ Generate a publicly visible URL for this key. """

    return get_s3().generate_presigned_url(
        "get_object",
        Params={
            "Bucket": current_app.config[S3_BUCKET],
            "Key": key,
        },
        ExpiresIn=S3_PRESIGNED_TIMEOUT,
    )

def get_file(key):
    """ Return the binary content of key. """

    s3_client = get_s3()
    bucket_name = os.environ.get("S3_BUCKET")
    if bucket_name not in [b["Name"] for b in s3_client.list_buckets()["Buckets"]]:
        s3_client.create_bucket(ACL="private", Bucket=bucket_name)

    response = s3_client.get_object(Bucket=bucket_name, Key=filename)

    return response["Body"]
