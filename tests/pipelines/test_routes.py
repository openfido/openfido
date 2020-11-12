import io
from unittest.mock import patch

import responses
from app.constants import WORKFLOW_HOSTNAME, AUTH_HOSTNAME
from app.pipelines.models import (
    ArtifactChart,
    OrganizationPipeline,
    OrganizationPipelineRun,
    OrganizationPipelineInputFile,
    db,
)
from app.pipelines.queries import find_organization_pipelines
from app.utils import ApplicationsEnum
from application_roles.decorators import ROLES_KEY
from application_roles.services import create_application
from marshmallow.exceptions import ValidationError
from requests import HTTPError

from ..conftest import (
    JWT_TOKEN,
    ORGANIZATION_UUID,
    PIPELINE_RUN_UUID,
    PIPELINE_UUID,
    USER_UUID,
)
from .test_services import (
    CHART_JSON,
    FINISHED_PIPELINE_RUN_RESPONSE_JSON,
    PIPELINE_JSON,
    PIPELINE_RUN_CONSOLE_RESPONSE_JSON,
    PIPELINE_RUN_JSON,
    PIPELINE_RUN_RESPONSE_JSON,
    PIPELINE_RUN_CONSOLE_RESPONSE_JSON,
    PIPELINE_RUN_INPUT_FILE_JSON,
)


def test_requests_have_cors(app, client, client_application):
    result = client.get(
        f"/v1/organizations/{ORGANIZATION_UUID}/pipelines",
        content_type="application/json",
    )
    assert result.headers["Access-Control-Allow-Origin"] == "*"


def test_pipelines_no_roles_provided(app, client, client_application):
    result = client.get(
        f"/v1/organizations/{ORGANIZATION_UUID}/pipelines",
        content_type="application/json",
    )
    assert result.status_code == 401

    result = client.get(
        f"/v1/organizations/{ORGANIZATION_UUID}/pipelines",
        content_type="application/json",
        headers={
            "Authorization": f"Bearer {JWT_TOKEN}",
        },
    )
    assert result.status_code == 401


@responses.activate
def test_pipelines_backing_error(app, client, client_application):
    responses.add(
        responses.POST,
        f"{app.config[WORKFLOW_HOSTNAME]}/v1/pipelines/search",
        status=500,
    )

    result = client.get(
        f"/v1/organizations/{ORGANIZATION_UUID}/pipelines",
        content_type="application/json",
        headers={
            "Authorization": f"Bearer {JWT_TOKEN}",
            ROLES_KEY: client_application.api_key,
        },
    )
    assert result.status_code == 503


@responses.activate
def test_pipelines_bad_search(app, client, client_application):
    json_response = {
        "errors": {"uuids": {"0": ["String does not match expected pattern."]}},
        "message": "Unable to search pipeline",
    }
    responses.add(
        responses.POST,
        f"{app.config[WORKFLOW_HOSTNAME]}/v1/pipelines/search",
        json=json_response,
        status=400,
    )

    result = client.get(
        f"/v1/organizations/{ORGANIZATION_UUID}/pipelines",
        content_type="application/json",
        headers={
            "Authorization": f"Bearer {JWT_TOKEN}",
            ROLES_KEY: client_application.api_key,
        },
    )
    assert result.status_code == 400
    assert result.json == json_response


@patch("app.pipelines.services.fetch_pipeline_run")
@responses.activate
def test_pipelines(
    mock_runs,
    app,
    client,
    client_application,
    organization_pipeline,
    organization_pipeline_run,
):
    mock_runs.return_value = PIPELINE_RUN_RESPONSE_JSON
    pipeline_json = dict(PIPELINE_JSON)
    pipeline_json.update(
        {
            "created_at": "2020-10-08T12:20:36.564095",
            "updated_at": "2020-10-08T12:20:36.564100",
            "uuid": organization_pipeline.pipeline_uuid,
            "last_pipeline_run": PIPELINE_RUN_RESPONSE_JSON,
        }
    )
    json_response = [pipeline_json]
    responses.add(
        responses.POST,
        f"{app.config[WORKFLOW_HOSTNAME]}/v1/pipelines/search",
        json=json_response,
    )

    result = client.get(
        f"/v1/organizations/{ORGANIZATION_UUID}/pipelines",
        content_type="application/json",
        headers={
            "Authorization": f"Bearer {JWT_TOKEN}",
            ROLES_KEY: client_application.api_key,
        },
    )

    assert result.status_code == 200
    json_response[0]["uuid"] = organization_pipeline.uuid
    assert result.json == json_response


@patch("app.pipelines.routes.create_pipeline")
@responses.activate
def test_create_pipeline_backend_500(
    create_pipeline_mock, app, client, client_application
):
    create_pipeline_mock.side_effect = HTTPError("something is wrong")
    result = client.post(
        f"/v1/organizations/{ORGANIZATION_UUID}/pipelines",
        content_type="application/json",
        json=PIPELINE_JSON,
        headers={
            "Authorization": f"Bearer {JWT_TOKEN}",
            ROLES_KEY: client_application.api_key,
        },
    )
    assert result.status_code == 503
    assert result.json == {"message": "something is wrong"}


@patch("app.pipelines.routes.create_pipeline")
@responses.activate
def test_create_pipeline_backend_error(
    create_pipeline_mock, app, client, client_application
):
    message = {"message": "error"}
    create_pipeline_mock.side_effect = ValueError(message)
    result = client.post(
        f"/v1/organizations/{ORGANIZATION_UUID}/pipelines",
        content_type="application/json",
        json=PIPELINE_JSON,
        headers={
            "Authorization": f"Bearer {JWT_TOKEN}",
            ROLES_KEY: client_application.api_key,
        },
    )
    assert result.status_code == 400
    assert result.json == message


@responses.activate
def test_create_pipeline(app, client, client_application):
    json_response = dict(PIPELINE_JSON)
    json_response.update(
        {
            "created_at": "2020-10-08T12:20:36.564095",
            "updated_at": "2020-10-08T12:20:36.564100",
            "uuid": "daf6febec1714ac79a73327760c89f15",
        }
    )
    responses.add(
        responses.POST,
        f"{app.config[WORKFLOW_HOSTNAME]}/v1/pipelines",
        json=json_response,
    )

    result = client.post(
        f"/v1/organizations/{ORGANIZATION_UUID}/pipelines",
        content_type="application/json",
        json=PIPELINE_JSON,
        headers={
            "Authorization": f"Bearer {JWT_TOKEN}",
            ROLES_KEY: client_application.api_key,
        },
    )
    assert result.status_code == 200

    pipeline = OrganizationPipeline.query.order_by(
        OrganizationPipeline.id.desc()
    ).first()
    json_response["uuid"] = pipeline.uuid
    assert result.json == json_response


@patch("app.pipelines.routes.update_pipeline")
@responses.activate
def test_update_pipeline_backend_500(
    update_pipeline_mock, app, client, client_application
):
    update_pipeline_mock.side_effect = HTTPError("something is wrong")
    result = client.put(
        f"/v1/organizations/{ORGANIZATION_UUID}/pipelines/" + "0" * 32,
        content_type="application/json",
        json=PIPELINE_JSON,
        headers={
            "Authorization": f"Bearer {JWT_TOKEN}",
            ROLES_KEY: client_application.api_key,
        },
    )
    assert result.status_code == 503
    assert result.json == {"message": "something is wrong"}


@patch("app.pipelines.routes.update_pipeline")
@responses.activate
def test_update_pipeline_backend_error(
    update_pipeline_mock, app, client, client_application
):
    message = {"message": "error"}
    update_pipeline_mock.side_effect = ValueError(message)
    result = client.put(
        f"/v1/organizations/{ORGANIZATION_UUID}/pipelines/" + "0" * 32,
        content_type="application/json",
        json=PIPELINE_JSON,
        headers={
            "Authorization": f"Bearer {JWT_TOKEN}",
            ROLES_KEY: client_application.api_key,
        },
    )
    assert result.status_code == 400
    assert result.json == message


@responses.activate
def test_update_pipeline(app, client, client_application, organization_pipeline):
    json_response = dict(PIPELINE_JSON)
    json_response.update(
        {
            "updated_at": "2020-10-08T12:20:36.564095",
            "updated_at": "2020-10-08T12:20:36.564100",
            "uuid": "daf6febec1714ac79a73327760c89f15",
        }
    )
    responses.add(
        responses.PUT,
        f"{app.config[WORKFLOW_HOSTNAME]}/v1/pipelines/{organization_pipeline.pipeline_uuid}",
        json=json_response,
    )

    result = client.put(
        f"/v1/organizations/{ORGANIZATION_UUID}/pipelines/{organization_pipeline.uuid}",
        content_type="application/json",
        json=PIPELINE_JSON,
        headers={
            "Authorization": f"Bearer {JWT_TOKEN}",
            ROLES_KEY: client_application.api_key,
        },
    )
    assert result.status_code == 200

    organization_pipeline = OrganizationPipeline.query.order_by(
        OrganizationPipeline.id.desc()
    ).first()
    json_response["uuid"] = organization_pipeline.uuid
    assert result.json == json_response


@responses.activate
def test_delete_pipeline(app, client, client_application, organization_pipeline):
    responses.add(
        responses.DELETE,
        f"{app.config[WORKFLOW_HOSTNAME]}/v1/pipelines/{organization_pipeline.pipeline_uuid}",
    )

    result = client.delete(
        f"/v1/organizations/{ORGANIZATION_UUID}/pipelines/{organization_pipeline.uuid}",
        content_type="application/json",
        headers={
            "Authorization": f"Bearer {JWT_TOKEN}",
            ROLES_KEY: client_application.api_key,
        },
    )
    assert result.status_code == 200
    assert set(find_organization_pipelines(ORGANIZATION_UUID)) == set()


@patch("app.pipelines.routes.delete_pipeline")
@responses.activate
def test_delete_pipeline_http_error(
    delete_mock, app, client, client_application, organization_pipeline
):
    delete_mock.side_effect = HTTPError("something is wrong")
    result = client.delete(
        f"/v1/organizations/{ORGANIZATION_UUID}/pipelines/{organization_pipeline.uuid}",
        content_type="application/json",
        headers={
            "Authorization": f"Bearer {JWT_TOKEN}",
            ROLES_KEY: client_application.api_key,
        },
    )
    assert result.status_code == 503
    assert set(find_organization_pipelines(ORGANIZATION_UUID)) == set(
        [organization_pipeline]
    )
    assert result.json == {"message": "something is wrong"}


@patch("app.pipelines.routes.delete_pipeline")
@responses.activate
def test_delete_pipeline_bad_response(
    delete_mock, app, client, client_application, organization_pipeline
):
    message = {"message": "error"}
    delete_mock.side_effect = ValueError(message)
    result = client.delete(
        f"/v1/organizations/{ORGANIZATION_UUID}/pipelines/{organization_pipeline.uuid}",
        content_type="application/json",
        headers={
            "Authorization": f"Bearer {JWT_TOKEN}",
            ROLES_KEY: client_application.api_key,
        },
    )
    assert result.status_code == 400
    assert set(find_organization_pipelines(ORGANIZATION_UUID)) == set(
        [organization_pipeline]
    )


@responses.activate
def test_upload_input_file_bad_data(app, client, organization_pipeline):
    application = create_application("test client", ApplicationsEnum.REACT_CLIENT)

    db.session.add(application)
    db.session.commit()

    responses.add(
        responses.GET,
        f"{app.config[AUTH_HOSTNAME]}/users/{USER_UUID}/organizations",
        body="not json",
    )

    result = client.post(
        f"/v1/organizations/{ORGANIZATION_UUID}/pipelines/{organization_pipeline.uuid}/input_files",
        headers={
            "Authorization": f"Bearer {JWT_TOKEN}",
            ROLES_KEY: application.api_key,
        },
        data=io.BytesIO(b"some data"),
    )
    assert result.status_code == 401
    assert len(organization_pipeline.organization_pipeline_input_files) == 0


@responses.activate
def test_upload_input_file_no_org(
    app, client, client_application, organization_pipeline
):
    result = client.post(
        f"/v1/organizations/{ORGANIZATION_UUID}/pipelines/nouuid/input_files",
        headers={
            "Authorization": f"Bearer {JWT_TOKEN}",
            ROLES_KEY: client_application.api_key,
        },
        data=b"some data",
    )
    assert result.status_code == 400
    assert len(organization_pipeline.organization_pipeline_input_files) == 0


@responses.activate
def test_upload_input_file_invalid_args(
    app, client, client_application, organization_pipeline
):
    result = client.post(
        f"/v1/organizations/{ORGANIZATION_UUID}/pipelines/{organization_pipeline.uuid}/input_files",
        headers={
            "Authorization": f"Bearer {JWT_TOKEN}",
            ROLES_KEY: client_application.api_key,
        },
        data=b"some data",
    )
    assert result.status_code == 400
    assert len(organization_pipeline.organization_pipeline_input_files) == 0


@patch("app.pipelines.services.upload_stream")
@responses.activate
def test_upload_input_file_value_error(
    upload_stream_mock, app, client, client_application, organization_pipeline
):
    upload_stream_mock.side_effect = ValueError("blah")
    result = client.post(
        f"/v1/organizations/{ORGANIZATION_UUID}/pipelines/{organization_pipeline.uuid}/input_files?name=afile.txt",
        headers={
            "Authorization": f"Bearer {JWT_TOKEN}",
            ROLES_KEY: client_application.api_key,
        },
        data=b"some data",
    )
    assert result.status_code == 400
    assert len(organization_pipeline.organization_pipeline_input_files) == 0


@patch("app.pipelines.services.upload_stream")
@responses.activate
def test_upload_input_file_http_error(
    upload_stream_mock, app, client, client_application, organization_pipeline
):
    upload_stream_mock.side_effect = HTTPError("err")
    result = client.post(
        f"/v1/organizations/{ORGANIZATION_UUID}/pipelines/{organization_pipeline.uuid}/input_files?name=afile.txt",
        headers={
            "Authorization": f"Bearer {JWT_TOKEN}",
            ROLES_KEY: client_application.api_key,
        },
        data=b"some data",
    )
    assert result.status_code == 503
    assert len(organization_pipeline.organization_pipeline_input_files) == 0


@patch("app.pipelines.services.upload_stream")
@responses.activate
def test_upload_input_file(
    upload_stream_mock, app, client, client_application, organization_pipeline
):
    result = client.post(
        f"/v1/organizations/{ORGANIZATION_UUID}/pipelines/{organization_pipeline.uuid}/input_files?name=afile.txt",
        headers={
            "Authorization": f"Bearer {JWT_TOKEN}",
            ROLES_KEY: client_application.api_key,
        },
        data=b"some data",
    )
    assert result.status_code == 200
    assert len(organization_pipeline.organization_pipeline_input_files) == 1


@patch("app.pipelines.services.create_url")
@responses.activate
def test_create_pipeline_run(
    mock_url,
    app,
    client,
    client_application,
    organization_pipeline,
    organization_pipeline_input_file,
):

    mock_url.return_value = "http://somefileurl.com"
    json_response = dict(PIPELINE_RUN_RESPONSE_JSON)

    pipeline = OrganizationPipeline.query.order_by(
        OrganizationPipeline.id.desc()
    ).first()

    responses.add(
        responses.POST,
        f"{app.config[WORKFLOW_HOSTNAME]}/v1/pipelines/{pipeline.pipeline_uuid}/runs",
        json=json_response,
    )

    result = client.post(
        f"/v1/organizations/{pipeline.organization_uuid}/pipelines/{pipeline.uuid}/runs",
        content_type="application/json",
        json={"inputs": [organization_pipeline_input_file.uuid]},
        headers={
            "Authorization": f"Bearer {JWT_TOKEN}",
            ROLES_KEY: client_application.api_key,
        },
    )
    resp = result.json

    new_run = OrganizationPipelineRun.query.filter(
        OrganizationPipelineRun.uuid == resp["uuid"]
    ).first()

    assert result.status_code == 200
    assert new_run is not None
    assert result.json == json_response


@responses.activate
def test_create_pipeline_run_invalid_org_and_file(
    app, client, client_application, organization_pipeline
):
    result = client.post(
        f"/v1/organizations/12345/pipelines/{organization_pipeline.uuid}/runs",
        content_type="application/json",
        json={"some": "json"},
        headers={
            "Authorization": f"Bearer {JWT_TOKEN}",
            ROLES_KEY: client_application.api_key,
        },
    )

    assert result.status_code == 404


@patch("app.pipelines.routes.create_pipeline_run")
@responses.activate
def test_create_pipeline_run_value_error(
    mock_create, app, client, client_application, organization_pipeline
):
    mock_create.side_effect = ValueError("error")

    result = client.post(
        f"/v1/organizations/{organization_pipeline.organization_uuid}/pipelines/{organization_pipeline.uuid}/runs",
        content_type="application/json",
        json={"some": "json"},
        headers={
            "Authorization": f"Bearer {JWT_TOKEN}",
            ROLES_KEY: client_application.api_key,
        },
    )

    assert result.status_code == 400


@patch("app.pipelines.routes.create_pipeline_run")
@responses.activate
def test_create_pipeline_run_http_error(
    mock_create, app, client, client_application, organization_pipeline
):
    json_response = dict(PIPELINE_RUN_RESPONSE_JSON)

    mock_create.side_effect = HTTPError("error")

    result = client.post(
        f"/v1/organizations/{organization_pipeline.organization_uuid}/pipelines/{organization_pipeline.uuid}/runs",
        content_type="application/json",
        json={"some": "json"},
        headers={
            "Authorization": f"Bearer {JWT_TOKEN}",
            ROLES_KEY: client_application.api_key,
        },
    )

    assert result.status_code == 503


@patch("app.pipelines.services.create_url")
@responses.activate
def test_list_pipeline_runs(
    mock_url,
    app,
    client,
    client_application,
    organization_pipeline,
    organization_pipeline_run,
    organization_pipeline_input_file,
):
    mock_url.return_value = "http://somefileurl.com"
    json_response = [PIPELINE_RUN_RESPONSE_JSON]

    pipeline = OrganizationPipeline.query.order_by(
        OrganizationPipeline.id.desc()
    ).first()

    responses.add(
        responses.GET,
        f"{app.config[WORKFLOW_HOSTNAME]}/v1/pipelines/{pipeline.pipeline_uuid}/runs",
        json=json_response,
    )

    result = client.get(
        f"/v1/organizations/{pipeline.organization_uuid}/pipelines/{pipeline.uuid}/runs",
        content_type="application/json",
        json=PIPELINE_RUN_JSON,
        headers={
            "Authorization": f"Bearer {JWT_TOKEN}",
            ROLES_KEY: client_application.api_key,
        },
    )
    resp = result.json

    assert result.status_code == 200
    assert result.json == json_response


@patch("app.pipelines.routes.fetch_pipeline_runs")
@patch("flask.jsonify")
@responses.activate
def test_list_pipeline_runs_value_error(
    mock_fetch, mock_jsonify, app, client, client_application, organization_pipeline
):
    mock_fetch.side_effect = {"some": "json"}
    mock_jsonify.side_effect = ValueError("error")

    result = client.get(
        f"/v1/organizations/{organization_pipeline.organization_uuid}/pipelines/{organization_pipeline.uuid}/runs",
        content_type="application/json",
        json=PIPELINE_RUN_JSON,
        headers={
            "Authorization": f"Bearer {JWT_TOKEN}",
            ROLES_KEY: client_application.api_key,
        },
    )

    assert result.status_code == 400
    assert mock_jsonify.called is True


@patch("app.pipelines.routes.fetch_pipeline_runs")
@responses.activate
def test_list_pipeline_runs_http_error(
    mock_fetch, app, client, client_application, organization_pipeline
):
    mock_fetch.side_effect = HTTPError("error")

    result = client.get(
        f"/v1/organizations/{organization_pipeline.organization_uuid}/pipelines/{organization_pipeline.uuid}/runs",
        content_type="application/json",
        json=PIPELINE_RUN_JSON,
        headers={
            "Authorization": f"Bearer {JWT_TOKEN}",
            ROLES_KEY: client_application.api_key,
        },
    )

    assert result.status_code == 503


@patch("app.pipelines.services.create_url")
@responses.activate
def test_pipeline_run(
    mock_url,
    app,
    client,
    client_application,
    organization_pipeline,
    organization_pipeline_run,
    organization_pipeline_input_file,
):

    mock_url.return_value = "http://somefileurl.com"
    json_response = dict(PIPELINE_RUN_RESPONSE_JSON)

    pipeline = OrganizationPipeline.query.order_by(
        OrganizationPipeline.id.desc()
    ).first()

    pipeline_run = pipeline.organization_pipeline_runs[0]

    responses.add(
        responses.GET,
        f"{app.config[WORKFLOW_HOSTNAME]}/v1/pipelines/{pipeline.pipeline_uuid}/runs/{pipeline_run.pipeline_run_uuid}",
        json=json_response,
    )

    result = client.get(
        f"/v1/organizations/{pipeline.organization_uuid}/pipelines/{pipeline.uuid}/runs/{pipeline_run.uuid}",
        content_type="application/json",
        json=PIPELINE_RUN_JSON,
        headers={
            "Authorization": f"Bearer {JWT_TOKEN}",
            ROLES_KEY: client_application.api_key,
        },
    )
    resp = result.json

    assert result.status_code == 200
    assert result.json == json_response


@patch("app.pipelines.routes.fetch_pipeline_run")
@patch("flask.jsonify")
@responses.activate
def test_list_pipeline_run_value_error(
    mock_fetch,
    mock_jsonify,
    app,
    client,
    client_application,
    organization_pipeline,
    organization_pipeline_run,
):
    mock_fetch.side_effect = {"some": "json"}
    mock_jsonify.side_effect = ValueError("error")

    pipeline = OrganizationPipeline.query.order_by(
        OrganizationPipeline.id.desc()
    ).first()
    pipeline_run = pipeline.organization_pipeline_runs[0]

    result = client.get(
        f"/v1/organizations/{pipeline.organization_uuid}/pipelines/{pipeline.uuid}/runs/{pipeline_run.uuid}",
        content_type="application/json",
        json=PIPELINE_RUN_JSON,
        headers={
            "Authorization": f"Bearer {JWT_TOKEN}",
            ROLES_KEY: client_application.api_key,
        },
    )

    assert result.status_code == 400
    assert mock_jsonify.called is True


@patch("app.pipelines.routes.fetch_pipeline_run")
@responses.activate
def test_list_pipeline_run_http_error(
    mock_fetch,
    app,
    client,
    client_application,
    organization_pipeline,
    organization_pipeline_run,
):
    mock_fetch.side_effect = HTTPError("error")

    pipeline = OrganizationPipeline.query.order_by(
        OrganizationPipeline.id.desc()
    ).first()
    pipeline_run = pipeline.organization_pipeline_runs[0]

    result = client.get(
        f"/v1/organizations/{pipeline.organization_uuid}/pipelines/{pipeline.uuid}/runs/{pipeline_run.uuid}",
        content_type="application/json",
        json=PIPELINE_RUN_JSON,
        headers={
            "Authorization": f"Bearer {JWT_TOKEN}",
            ROLES_KEY: client_application.api_key,
        },
    )

    assert result.status_code == 503


@patch("app.pipelines.routes.fetch_pipeline_run")
@responses.activate
def test_list_pipeline_run_invalid_org_pipeline(
    mock_fetch,
    app,
    client,
    client_application,
    organization_pipeline,
    organization_pipeline_run,
):
    mock_fetch.side_effect = HTTPError("error")

    pipeline = OrganizationPipeline.query.order_by(
        OrganizationPipeline.id.desc()
    ).first()
    pipeline_run = pipeline.organization_pipeline_runs[0]

    result = client.get(
        f"/v1/organizations/{organization_pipeline.organization_uuid}/pipelines/123445/runs/{organization_pipeline.uuid}",
        content_type="application/json",
        json=PIPELINE_RUN_JSON,
        headers={
            "Authorization": f"Bearer {JWT_TOKEN}",
            ROLES_KEY: client_application.api_key,
        },
    )

    assert result.status_code == 400


@patch("app.pipelines.routes.find_organization_pipeline")
@responses.activate
def test_pipeline_run_console_org_not_found(
    mock_pipeline,
    app,
    client,
    client_application,
    organization_pipeline,
    organization_pipeline_run,
):
    mock_pipeline.return_value = None

    result = client.get(
        f"/v1/organizations/{organization_pipeline.organization_uuid}/pipelines/12345/runs/{organization_pipeline_run.uuid}/console",
        content_type="application/json",
        json=PIPELINE_RUN_JSON,
        headers={
            "Authorization": f"Bearer {JWT_TOKEN}",
            ROLES_KEY: client_application.api_key,
        },
    )
    resp = result.json

    assert result.status_code == 400


@patch("app.pipelines.routes.fetch_pipeline_run_console")
@responses.activate
def test_pipeline_run_console_error(
    mock_console,
    app,
    client,
    client_application,
    organization_pipeline,
    organization_pipeline_run,
):
    mock_console.side_effect = ValueError("error")
    pipeline = OrganizationPipeline.query.order_by(
        OrganizationPipeline.id.desc()
    ).first()

    pipeline_run = pipeline.organization_pipeline_runs[0]

    result = client.get(
        f"/v1/organizations/{pipeline.organization_uuid}/pipelines/{pipeline.uuid}/runs/{pipeline_run.uuid}/console",
        content_type="application/json",
        json=PIPELINE_RUN_JSON,
        headers={
            "Authorization": f"Bearer {JWT_TOKEN}",
            ROLES_KEY: client_application.api_key,
        },
    )

    assert result.status_code == 400


@patch("app.pipelines.routes.fetch_pipeline_run_console")
@responses.activate
def test_pipeline_run_console_notfound(
    mock_console,
    app,
    client,
    client_application,
    organization_pipeline,
    organization_pipeline_run,
):
    mock_console.side_effect = HTTPError("not found")
    pipeline = OrganizationPipeline.query.order_by(
        OrganizationPipeline.id.desc()
    ).first()

    pipeline_run = pipeline.organization_pipeline_runs[0]

    result = client.get(
        f"/v1/organizations/{pipeline.organization_uuid}/pipelines/{pipeline.uuid}/runs/{pipeline_run.uuid}/console",
        content_type="application/json",
        json=PIPELINE_RUN_JSON,
        headers={
            "Authorization": f"Bearer {JWT_TOKEN}",
            ROLES_KEY: client_application.api_key,
        },
    )

    assert result.status_code == 503


@responses.activate
def test_pipeline_run_console(
    app, client, client_application, organization_pipeline, organization_pipeline_run
):
    json_response = dict(PIPELINE_RUN_CONSOLE_RESPONSE_JSON)

    pipeline = OrganizationPipeline.query.order_by(
        OrganizationPipeline.id.desc()
    ).first()

    pipeline_run = pipeline.organization_pipeline_runs[0]

    responses.add(
        responses.GET,
        f"{app.config[WORKFLOW_HOSTNAME]}/v1/pipelines/{organization_pipeline.pipeline_uuid}/runs/{organization_pipeline_run.pipeline_run_uuid}/console",
        json=json_response,
    )

    result = client.get(
        f"/v1/organizations/{pipeline.organization_uuid}/pipelines/{pipeline.uuid}/runs/{pipeline_run.uuid}/console",
        content_type="application/json",
        json=PIPELINE_RUN_JSON,
        headers={
            "Authorization": f"Bearer {JWT_TOKEN}",
            ROLES_KEY: client_application.api_key,
        },
    )
    resp = result.json

    assert result.status_code == 200
    assert result.json == json_response


@responses.activate
def test_create_chart_no_organization_pipeline(
    app, client, client_application, organization_pipeline
):
    result = client.post(
        f"/v1/organizations/{ORGANIZATION_UUID}/pipelines/{'0' * 32}/runs/{'0' * 32}/charts",
        content_type="application/json",
        json=CHART_JSON,
        headers={
            "Authorization": f"Bearer {JWT_TOKEN}",
            ROLES_KEY: client_application.api_key,
        },
    )
    assert result.status_code == 400


@responses.activate
def test_create_chart_no_organization_pipeline_run(
    app, client, client_application, organization_pipeline, organization_pipeline_run
):
    result = client.post(
        f"/v1/organizations/{ORGANIZATION_UUID}/pipelines/{organization_pipeline.uuid}/runs/{'0' * 32}/charts",
        content_type="application/json",
        json=CHART_JSON,
        headers={
            "Authorization": f"Bearer {JWT_TOKEN}",
            ROLES_KEY: client_application.api_key,
        },
    )
    assert result.status_code == 400


@patch("app.pipelines.routes.create_artifact_chart")
@responses.activate
def test_create_chart_value_error(
    create_chart_mock,
    app,
    client,
    client_application,
    organization_pipeline,
    organization_pipeline_run,
):
    create_chart_mock.side_effect = ValueError("an error")

    result = client.post(
        f"/v1/organizations/{ORGANIZATION_UUID}/pipelines/{organization_pipeline.uuid}/runs/{organization_pipeline_run.uuid}/charts",
        content_type="application/json",
        json=CHART_JSON,
        headers={
            "Authorization": f"Bearer {JWT_TOKEN}",
            ROLES_KEY: client_application.api_key,
        },
    )

    assert result.status_code == 400


@patch("app.pipelines.routes.create_artifact_chart")
@responses.activate
def test_create_chart_validation_error(
    create_chart_mock,
    app,
    client,
    client_application,
    organization_pipeline,
    organization_pipeline_run,
):
    create_chart_mock.side_effect = ValidationError("an error")

    result = client.post(
        f"/v1/organizations/{ORGANIZATION_UUID}/pipelines/{organization_pipeline.uuid}/runs/{organization_pipeline_run.uuid}/charts",
        content_type="application/json",
        json=CHART_JSON,
        headers={
            "Authorization": f"Bearer {JWT_TOKEN}",
            ROLES_KEY: client_application.api_key,
        },
    )

    assert result.status_code == 400


@patch("app.pipelines.routes.create_artifact_chart")
@responses.activate
def test_create_chart_http_error(
    create_chart_mock,
    app,
    client,
    client_application,
    organization_pipeline,
    organization_pipeline_run,
):
    create_chart_mock.side_effect = HTTPError("an error")

    result = client.post(
        f"/v1/organizations/{ORGANIZATION_UUID}/pipelines/{organization_pipeline.uuid}/runs/{organization_pipeline_run.uuid}/charts",
        content_type="application/json",
        json=CHART_JSON,
        headers={
            "Authorization": f"Bearer {JWT_TOKEN}",
            ROLES_KEY: client_application.api_key,
        },
    )

    assert result.status_code == 503


@responses.activate
def test_create_chart(
    app, client, client_application, organization_pipeline, organization_pipeline_run
):
    responses.add(
        responses.GET,
        f"{app.config[WORKFLOW_HOSTNAME]}/v1/pipelines/{organization_pipeline.pipeline_uuid}/runs/{organization_pipeline_run.pipeline_run_uuid}",
        json=FINISHED_PIPELINE_RUN_RESPONSE_JSON,
    )

    result = client.post(
        f"/v1/organizations/{ORGANIZATION_UUID}/pipelines/{organization_pipeline.uuid}/runs/{organization_pipeline_run.uuid}/charts",
        content_type="application/json",
        json=CHART_JSON,
        headers={
            "Authorization": f"Bearer {JWT_TOKEN}",
            ROLES_KEY: client_application.api_key,
        },
    )
    chart = ArtifactChart.query.first()

    assert result.status_code == 200
    assert result.json == {
        "uuid": chart.uuid,
        "name": chart.name,
        "artifact": FINISHED_PIPELINE_RUN_RESPONSE_JSON["artifacts"][0],
        "chart_type_code": chart.chart_type_code,
        "chart_config": chart.chart_config,
        "created_at": chart.created_at.isoformat(),
        "updated_at": chart.updated_at.isoformat(),
    }


@responses.activate
def test_get_charts_no_organization_pipeline(
    app, client, client_application, organization_pipeline
):
    result = client.get(
        f"/v1/organizations/{ORGANIZATION_UUID}/pipelines/{'0' * 32}/runs/{'0' * 32}/charts",
        content_type="application/json",
        json=CHART_JSON,
        headers={
            "Authorization": f"Bearer {JWT_TOKEN}",
            ROLES_KEY: client_application.api_key,
        },
    )
    assert result.status_code == 400


@responses.activate
def test_get_charts_no_organization_pipeline_run(
    app, client, client_application, organization_pipeline, organization_pipeline_run
):
    result = client.get(
        f"/v1/organizations/{ORGANIZATION_UUID}/pipelines/{organization_pipeline.uuid}/runs/{'0' * 32}/charts",
        content_type="application/json",
        json=CHART_JSON,
        headers={
            "Authorization": f"Bearer {JWT_TOKEN}",
            ROLES_KEY: client_application.api_key,
        },
    )
    assert result.status_code == 400


@patch("app.pipelines.routes.fetch_artifact_charts")
@responses.activate
def test_get_charts_value_error(
    fetch_charts_mock,
    app,
    client,
    client_application,
    organization_pipeline,
    organization_pipeline_run,
):
    fetch_charts_mock.side_effect = ValueError("an error")

    result = client.get(
        f"/v1/organizations/{ORGANIZATION_UUID}/pipelines/{organization_pipeline.uuid}/runs/{organization_pipeline_run.uuid}/charts",
        content_type="application/json",
        headers={
            "Authorization": f"Bearer {JWT_TOKEN}",
            ROLES_KEY: client_application.api_key,
        },
    )

    assert result.status_code == 400


@patch("app.pipelines.routes.fetch_artifact_charts")
@responses.activate
def test_get_charts_http_error(
    fetch_charts_mock,
    app,
    client,
    client_application,
    organization_pipeline,
    organization_pipeline_run,
):
    fetch_charts_mock.side_effect = HTTPError("an error")

    result = client.get(
        f"/v1/organizations/{ORGANIZATION_UUID}/pipelines/{organization_pipeline.uuid}/runs/{organization_pipeline_run.uuid}/charts",
        content_type="application/json",
        json=CHART_JSON,
        headers={
            "Authorization": f"Bearer {JWT_TOKEN}",
            ROLES_KEY: client_application.api_key,
        },
    )

    assert result.status_code == 503


@responses.activate
def test_get_charts(
    app, client, client_application, organization_pipeline, organization_pipeline_run
):
    chart = ArtifactChart(
        name="a chart",
        artifact_uuid=FINISHED_PIPELINE_RUN_RESPONSE_JSON["artifacts"][0]["uuid"],
        chart_type_code="ACODE",
        chart_config="{}",
    )
    organization_pipeline_run.artifact_charts.append(chart)
    db.session.commit()

    responses.add(
        responses.GET,
        f"{app.config[WORKFLOW_HOSTNAME]}/v1/pipelines/{organization_pipeline.pipeline_uuid}/runs/{organization_pipeline_run.pipeline_run_uuid}",
        json=FINISHED_PIPELINE_RUN_RESPONSE_JSON,
    )

    result = client.get(
        f"/v1/organizations/{ORGANIZATION_UUID}/pipelines/{organization_pipeline.uuid}/runs/{organization_pipeline_run.uuid}/charts",
        headers={
            "Authorization": f"Bearer {JWT_TOKEN}",
            ROLES_KEY: client_application.api_key,
        },
    )

    assert result.status_code == 200
    assert result.json == [
        {
            "uuid": chart.uuid,
            "name": chart.name,
            "artifact": FINISHED_PIPELINE_RUN_RESPONSE_JSON["artifacts"][0],
            "chart_type_code": chart.chart_type_code,
            "chart_config": chart.chart_config,
            "created_at": chart.created_at.isoformat(),
            "updated_at": chart.updated_at.isoformat(),
        }
    ]
