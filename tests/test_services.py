from unittest.mock import MagicMock, patch

from app.utils import fetch_is_user_in_org


@patch("app.pipelines.services.requests.get")
def test_fetch_is_user_in_org(get_mock, app):
    pass
