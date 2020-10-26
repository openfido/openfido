from unittest.mock import patch
from blob_utils import get_s3
from blob_utils.constants import (
    S3_ACCESS_KEY_ID,
    S3_BUCKET,
    S3_SECRET_ACCESS_KEY,
    S3_ENDPOINT_URL,
    S3_REGION_NAME,
    S3_PRESIGNED_TIMEOUT,
)


@patch("blob_utils.boto3.client")
def test_get_s3(client_mock, app):
    app.config[S3_ENDPOINT_URL] = "http://example.com"
    app.config[S3_REGION_NAME] = "a-region"
    assert get_s3() is not None
    client_mock.assert_called()
