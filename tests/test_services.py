from unittest.mock import MagicMock, patch

from app.constants import AUTH_HOSTNAME
from app.utils import fetch_is_user_in_org

from .conftest import JWT_TOKEN, ORGANIZATION_UUID, USER_UUID


@patch("app.pipelines.services.requests.get")
def test_fetch_is_user_in_org_false(get_mock, app):
    get_mock().json.return_value = [
        {
            "created_at": "Wed, 07 Oct 2020 19:50:00 GMT",
            "name": "A test org",
            "updated_at": "Wed, 07 Oct 2020 19:50:00 GMT",
            "uuid": ORGANIZATION_UUID,
        }
    ]

    assert fetch_is_user_in_org(ORGANIZATION_UUID, JWT_TOKEN, USER_UUID)

    get_mock.assert_called()
    get_call = get_mock.call_args
    assert get_call[0][0].startswith(app.config[AUTH_HOSTNAME])
    assert get_call[1]["headers"]["Authorization"] == f"Bearer {JWT_TOKEN}"


@patch("app.pipelines.services.requests.get")
def test_fetch_is_user_in_org(get_mock, app):
    get_mock().json.return_value = [
        {
            "created_at": "Wed, 07 Oct 2020 19:50:00 GMT",
            "name": "A test org",
            "updated_at": "Wed, 07 Oct 2020 19:50:00 GMT",
            "uuid": "9cbe59ab7b7548b7830b983b2e03cfc2",
        }
    ]

    assert not fetch_is_user_in_org(ORGANIZATION_UUID, JWT_TOKEN, USER_UUID)

    get_mock.assert_called()
    get_call = get_mock.call_args
    assert get_call[0][0].startswith(app.config[AUTH_HOSTNAME])
    assert get_call[1]["headers"]["Authorization"] == f"Bearer {JWT_TOKEN}"
