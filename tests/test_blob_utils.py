from datetime import datetime
from unittest.mock import patch

from botocore.stub import Stubber

import blob_utils

from blob_utils.constants import (
    S3_BUCKET,
    S3_ENDPOINT_URL,
    S3_REGION_NAME,
)
from tests.fixtures.s3 import s3_client


@patch("blob_utils.boto3.client")
def test_get_s3(client_mock, app):
    """Tests s3 client."""
    app.config[S3_ENDPOINT_URL] = "http://example.com"
    app.config[S3_REGION_NAME] = "a-region"

    assert blob_utils.get_s3() is not None
    client_mock.assert_called()


def test_verify_bucket(s3_client, app):
    """Tests verifying s3 bucket helper."""
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
