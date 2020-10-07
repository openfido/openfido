from unittest.mock import MagicMock, patch

from app.constants import WORKFLOW_API_TOKEN, WORKFLOW_HOSTNAME
from app.pipelines.services import fetch_pipelines
from application_roles.decorators import ROLES_KEY

from ..conftest import JWT_TOKEN, ORGANIZATION_UUID, USER_UUID


@patch("app.pipelines.services.requests.post")
def test_fetch_pipelines(post_mock, app):
    post_mock().json.return_value = ["somedata"]

    assert fetch_pipelines(ORGANIZATION_UUID) == ["somedata"]
    post_mock.assert_called()
    get_call = post_mock.call_args
    assert get_call[0][0].startswith(app.config[WORKFLOW_HOSTNAME])
    assert get_call[1]["headers"][ROLES_KEY] == app.config[WORKFLOW_API_TOKEN]
    assert get_call[1]["json"] == {"uuids": []}

    post_mock().raise_for_status.assert_called()
    post_mock().json.assert_called()
