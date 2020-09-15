from unittest.mock import patch
from app import utils


@patch("app.utils.boto3.client")
def test_get_s3(client_mock, app):
    assert utils.get_s3() is not None
    client_mock.assert_called()
