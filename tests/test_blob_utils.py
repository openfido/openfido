import blob_utils

from datetime import datetime
from unittest.mock import patch

from blob_utils.constants import (
    S3_ACCESS_KEY_ID,
    S3_BUCKET,
    S3_SECRET_ACCESS_KEY,
    S3_ENDPOINT_URL,
    S3_REGION_NAME,
    S3_PRESIGNED_TIMEOUT,
)
from botocore.stub import Stubber, ANY
from tests.fixtures.s3 import s3_client


@patch("blob_utils.boto3.client")
def test_get_s3(client_mock, app):
    app.config[S3_ENDPOINT_URL] = "http://example.com"
    app.config[S3_REGION_NAME] = "a-region"

    assert blob_utils.get_s3() is not None
    client_mock.assert_called()


@patch("blob_utils.get_s3")
def test_verify_bucket(client_mock, s3_client, app):
    app.config[S3_ENDPOINT_URL] = "http://example.com"
    app.config[S3_REGION_NAME] = "a-region"
    app.config[S3_BUCKET] = "missing"

    mock_response = {
        "Owner": {
            "ID": "foo",
            "DisplayName": "bar"
        },
        "Buckets": [{
            "CreationDate": datetime.now(),
            "Name": "baz"
        }]
    }
    mock_create_response = {
        "Location": "quix",
    }

    with Stubber(s3_client) as stubber:
        stubber.add_response('list_buckets', mock_response, {})
        stubber.add_response(
            'create_bucket',
            mock_create_response,
            {"ACL": "private", "Bucket": "missing"}
        )

        blob_utils.verify_bucket(stubber.client)
