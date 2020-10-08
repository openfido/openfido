import flask
from unittest.mock import patch

from app.utils import validate_organization
from .conftest import JWT_TOKEN, USER_UUID


@patch("app.utils.fetch_is_user_in_org")
def test_validate_organization(in_org_mock, app):
    @validate_organization()
    def a_view(organization_uuid):
        return {}, 200

    # A content type must be supplied
    with app.test_request_context("/a/view"):
        message, status = a_view(organization_uuid=12)
        assert status == 400
        assert not in_org_mock.called

    # Authorization header must also be supplied
    with app.test_request_context(
        "/a/view", headers={"Content-Type": "application/json"}
    ):
        message, status = a_view(organization_uuid=12)
        assert status == 401
        assert not in_org_mock.called

    headers = {"Content-Type": "application/json", "Authorization": "badvalue"}
    # Authorization header must have bearer token
    with app.test_request_context("/a/view", headers=headers):
        message, status = a_view(organization_uuid=12)
        assert status == 401
        assert not in_org_mock.called

    headers["Authorization"] = f"Bearer bad"
    # Authorization fails if the bearer token can't be decoded
    with app.test_request_context("/a/view", headers=headers):
        message, status = a_view(organization_uuid=12)
        assert status == 401
        assert not in_org_mock.called

    in_org_mock.return_value = False
    headers["Authorization"] = f"Bearer {JWT_TOKEN}"
    # Authorization fails if the organization isn't found
    with app.test_request_context("/a/view", headers=headers):
        message, status = a_view(organization_uuid=12)
        assert status == 404
        assert in_org_mock.called

    in_org_mock.reset_mock()
    in_org_mock.return_value = True
    headers["Authorization"] = f"Bearer {JWT_TOKEN}"
    # Authorization succeeds if the organization_uuid exists
    with app.test_request_context("/a/view", headers=headers):
        message, status = a_view(organization_uuid=12)
        assert status == 200
        assert in_org_mock.called
        assert flask.g.organization_uuid == 12
        assert flask.g.user_uuid == USER_UUID
        assert flask.g.jwt_token == JWT_TOKEN
