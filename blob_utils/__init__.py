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
    FLASK_ENV
)

def get_s3():
    """ Get access to the Boto s3 service. """

    # For local development we need to explicitly set the S3 keys:
    if FLASK_ENV in current_app.config and current_app.config[FLASK_ENV] != 'production':
        params = {
            "aws_access_key_id": current_app.config[S3_ACCESS_KEY_ID],
            "aws_secret_access_key": current_app.config[S3_SECRET_ACCESS_KEY],
            "endpoint_url": current_app.config[S3_ENDPOINT_URL],
            "config": Config(signature_version="s3v4"),
            "region_name": current_app.config[S3_REGION_NAME],
        }
        return boto3.client("s3", **params)

    return boto3.client("s3")


def upload_stream(key, stream, s3_client=None):
    """ Upload a io stream to an s3 bucket with the specified key. """

    if not s3_client:
        s3_client = get_s3()

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

    return (
        s3_client
        .get_object(Bucket=current_app.config[S3_BUCKET], Key=key)
        .get("Body")

    )
