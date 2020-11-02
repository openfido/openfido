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

    params = { }
    if S3_ACCESS_KEY_ID in current_app.config:
        params["aws_access_key_id"] = current_app.config[S3_ACCESS_KEY_ID]
        params["aws_secret_access_key"] = current_app.config[S3_SECRET_ACCESS_KEY]
        params["endpoint_url"] = current_app.config[S3_ENDPOINT_URL]
        params["config"] = Config(signature_version="s3v4"),
        params["region_name"] = current_app.config[S3_REGION_NAME],

    return boto3.client("s3", **params)


def verify_bucket(s3_client):
    """Takes an s3 client, fetches a list of buckets, and verifies the
    bucket exists. If not, create the configured bucket.
    """
    target_bucket = current_app.config[S3_BUCKET]

    buckets = (s3_client.list_buckets() or {}).get("Buckets", [])

    if target_bucket not in [bucket["Name"] for bucket in buckets]:
        s3_client.create_bucket(ACL="private", Bucket=target_bucket)


def upload_stream(key, stream, s3_client=None):
    """ Upload a io stream to an s3 bucket with the specified key. """

    if not s3_client:
        s3_client = get_s3()

    verify_bucket(s3_client)

    s3_client.upload_fileobj(
        stream,
        current_app.config[S3_BUCKET],
        key,
    )

def create_url(key, s3_client=None):
    """ Generate a publicly visible URL for this key. """

    if not s3_client:
        s3_client = get_s3()

    return s3_client.generate_presigned_url(
        "get_object",
        Params={
            "Bucket": current_app.config[S3_BUCKET],
            "Key": key,
        },
        ExpiresIn=current_app.config[S3_PRESIGNED_TIMEOUT],
    )


def get_file(key, s3_client=None):
    """ Return the binary content of key. """

    if not s3_client:
        s3_client = get_s3()

    verify_bucket(s3_client)

    return (
        s3_client
        .get_object(Bucket=current_app.config[S3_BUCKET], Key=key)
        .get("Body")

    )
