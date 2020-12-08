from datetime import datetime
from unittest.mock import patch

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
