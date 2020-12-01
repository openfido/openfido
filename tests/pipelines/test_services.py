import io
from unittest.mock import patch

import pytest
import responses
from app.constants import WORKFLOW_API_TOKEN, WORKFLOW_HOSTNAME
from app.pipelines.models import (
    OrganizationPipeline,
    OrganizationPipelineRun,
    ArtifactChart,
    db,
)
from app.pipelines.services import (
    create_artifact_chart,
    create_pipeline,
    create_pipeline_input_file,
    create_pipeline_run,
    delete_pipeline,
    fetch_artifact_charts,
    fetch_pipeline,
    fetch_pipeline_run,
    fetch_pipeline_run_console,
    fetch_pipeline_runs,
    fetch_pipelines,
    update_pipeline,
)
from application_roles.decorators import ROLES_KEY
from requests import HTTPError
from marshmallow.exceptions import ValidationError

from ..conftest import (
    ORGANIZATION_UUID,
    PIPELINE_RUN_INPUT_FILE_UUID,
    PIPELINE_RUN_UUID,
    PIPELINE_UUID,
)

PIPELINE_RUN_JSON = {
    "inputs": [PIPELINE_RUN_INPUT_FILE_UUID],
}
PIPELINE_RUN_INPUT_FILE_JSON = {
    "name": f"{PIPELINE_UUID}organization_pipeline_input_file.csv",
    "url": "http://somefileurl.com",
    "uuid": PIPELINE_RUN_INPUT_FILE_UUID,
}
PIPELINE_RUN_RESPONSE_JSON = {
    "artifacts": [],
    "created_at": "2020-10-28T22:01:48.950370",
    "inputs": [PIPELINE_RUN_INPUT_FILE_JSON],
    "sequence": 1,
    "states": [
        {"created_at": "2020-10-28T22:01:48.951140", "state": "QUEUED"},
        {"created_at": "2020-10-28T22:01:48.955688", "state": "NOT_STARTED"},
    ],
    "uuid": PIPELINE_RUN_UUID,
}
FINISHED_PIPELINE_RUN_RESPONSE_JSON = dict(PIPELINE_RUN_RESPONSE_JSON)
FINISHED_PIPELINE_RUN_RESPONSE_JSON["artifacts"] = [
    {
        "name": "inputfiles.txt",
        "url": "http://example.com/file.txt",
        "uuid": "81695d86c7a14156aa911ee513ed68a7",
    }
]
FINISHED_PIPELINE_RUN_RESPONSE_JSON["states"].append(
    [
        {"created_at": "2020-10-28T22:02:48.955688", "state": "RUNNING"},
    ]
)
FINISHED_PIPELINE_RUN_RESPONSE_JSON["states"].append(
    [
        {"created_at": "2020-10-28T22:03:48.955688", "state": "COMPLETED"},
    ]
)
PIPELINE_RUN_CONSOLE_RESPONSE_JSON = {
    "std_out": "success messages",
    "std_err": "the error output...",
}
PIPELINE_JSON = {
    "description": "a pipeline",
    "docker_image_url": "python:3",
    "name": "pipeline 1",
    "repository_branch": "master",
    "repository_ssh_url": "https://github.com/PresencePG/presence-pipeline-example.git",
    "last_pipeline_run": PIPELINE_RUN_RESPONSE_JSON,
}
CHART_JSON = {
    "name": "My Chart",
    "artifact_uuid": FINISHED_PIPELINE_RUN_RESPONSE_JSON["artifacts"][0]["uuid"],
    "chart_type_code": "LINE_CHART",
    "chart_config": {
        "x-axis": ["column1", "column2", "column3"],
        "y-axis": ["column1", "column2", "column3"],
    },
}


@responses.activate
def test_create_pipeline_bad_response(app):
    responses.add(
        responses.POST,
        f"{app.config[WORKFLOW_HOSTNAME]}/v1/pipelines",
        json=PIPELINE_JSON,
        status=500,
    )
    with pytest.raises(ValueError):
        create_pipeline(ORGANIZATION_UUID, PIPELINE_JSON)


@responses.activate
def test_create_pipeline_bad_json(app):
    responses.add(
        responses.POST, f"{app.config[WORKFLOW_HOSTNAME]}/v1/pipelines", body="notjson"
    )
    with pytest.raises(HTTPError):
        create_pipeline(ORGANIZATION_UUID, PIPELINE_JSON)


@responses.activate
def test_create_pipeline(app):
    json_response = dict(PIPELINE_JSON)
    json_response.update(
        {
            "created_at": "2020-10-08T14:22:26.276242",
            "updated_at": "2020-10-08T14:22:26.276278",
            "uuid": "83ac3b4e9433431fbd6d21e7a56b6f0a",
        }
    )
    responses.add(
        responses.POST,
        f"{app.config[WORKFLOW_HOSTNAME]}/v1/pipelines",
        json=json_response,
    )
    created_pipeline = create_pipeline(ORGANIZATION_UUID, PIPELINE_JSON)
    pipeline = OrganizationPipeline.query.order_by(
        OrganizationPipeline.id.desc()
    ).first()
    json_response["uuid"] = pipeline.uuid
    assert created_pipeline == json_response


@responses.activate
def test_fetch_pipelines_bad_workflow_response(app, organization_pipeline):
    responses.add(
        responses.POST,
        f"{app.config[WORKFLOW_HOSTNAME]}/v1/pipelines/search",
        status=500,
    )

    with pytest.raises(HTTPError):
        fetch_pipelines(ORGANIZATION_UUID)


@patch("app.pipelines.services.fetch_pipeline_run")
@patch("app.pipelines.services.requests.post")
def test_fetch_pipelines_bad_workflow_json(
    post_mock, mock_runs, app, organization_pipeline
):
    mock_runs.return_value = None
    pipeline_list = [
        {"uuid": organization_pipeline.pipeline_uuid, "name": "name 1"},
        {"uuid": "12345", "name": "name 2"},
    ]
    post_mock().json.return_value = pipeline_list

    with pytest.raises(ValueError):
        fetch_pipelines(ORGANIZATION_UUID)


@patch("app.pipelines.services.fetch_pipeline_run")
@patch("app.pipelines.services.requests.post")
def test_fetch_pipelines_no_runs(post_mock, mock_runs, app, organization_pipeline):
    mock_runs.return_value = None
    pipeline_list = [
        {"uuid": organization_pipeline.pipeline_uuid, "name": "name 1"},
    ]
    post_mock().json.return_value = pipeline_list

    expected_result = [
        {
            "uuid": organization_pipeline.uuid,
            "name": "name 1",
        },
    ]

    assert fetch_pipelines(ORGANIZATION_UUID) == expected_result
    post_mock.assert_called()
    get_call = post_mock.call_args
    assert get_call[0][0].startswith(app.config[WORKFLOW_HOSTNAME])
    assert get_call[1]["headers"][ROLES_KEY] == app.config[WORKFLOW_API_TOKEN]
    assert get_call[1]["json"] == {"uuids": [organization_pipeline.pipeline_uuid]}

    post_mock().raise_for_status.assert_called()
    post_mock().json.assert_called()
    assert not mock_runs.called


def test_fetch_pipeline_no_org_run(app):
    with pytest.raises(ValueError):
        assert fetch_pipeline(ORGANIZATION_UUID, "nosuchid")


@responses.activate
def test_fetch_pipeline(app, organization_pipeline, organization_pipeline_run):
    responses.add(
        responses.GET,
        f"{app.config[WORKFLOW_HOSTNAME]}/v1/pipelines/{organization_pipeline.pipeline_uuid}",
        json=PIPELINE_JSON,
    )

    pipeline_json = dict(PIPELINE_JSON)
    pipeline_json["uuid"] = organization_pipeline.uuid
    assert (
        fetch_pipeline(
            ORGANIZATION_UUID, organization_pipeline_run.organization_pipeline.uuid
        )
        == pipeline_json
    )


@patch("app.pipelines.services.fetch_pipeline_run")
@patch("app.pipelines.services.requests.post")
@responses.activate
def test_fetch_pipelines(
    post_mock, mock_runs, app, organization_pipeline, organization_pipeline_run
):
    mock_runs.return_value = PIPELINE_RUN_RESPONSE_JSON
    pipeline_list = [
        {
            "uuid": organization_pipeline.pipeline_uuid,
            "name": "name 1",
            "last_pipeline_run": PIPELINE_RUN_RESPONSE_JSON,
        }
    ]
    post_mock().json.return_value = pipeline_list
    responses.add(
        responses.GET,
        f"{app.config[WORKFLOW_HOSTNAME]}/v1/pipelines/{organization_pipeline.pipeline_uuid}/runs/{organization_pipeline_run.pipeline_run_uuid}",
        json=PIPELINE_RUN_RESPONSE_JSON,
    )

    expected_result = [
        {
            "uuid": organization_pipeline.uuid,
            "name": "name 1",
            "last_pipeline_run": PIPELINE_RUN_RESPONSE_JSON,
        }
    ]
    assert fetch_pipelines(ORGANIZATION_UUID) == expected_result
    post_mock.assert_called()
    get_call = post_mock.call_args
    assert get_call[0][0].startswith(app.config[WORKFLOW_HOSTNAME])
    assert get_call[1]["headers"][ROLES_KEY] == app.config[WORKFLOW_API_TOKEN]
    assert get_call[1]["json"] == {"uuids": [organization_pipeline.pipeline_uuid]}

    post_mock().raise_for_status.assert_called()
    post_mock().json.assert_called()
    mock_runs.assert_called()


@responses.activate
def test_update_pipeline_bad_response(app, organization_pipeline):
    responses.add(
        responses.PUT,
        f"{app.config[WORKFLOW_HOSTNAME]}/v1/pipelines/{organization_pipeline.pipeline_uuid}",
        json=PIPELINE_JSON,
        status=500,
    )
    with pytest.raises(ValueError):
        update_pipeline(ORGANIZATION_UUID, organization_pipeline.uuid, PIPELINE_JSON)


def test_update_pipeline_no_pipeline(app):
    with pytest.raises(ValueError):
        update_pipeline(ORGANIZATION_UUID, PIPELINE_UUID, PIPELINE_JSON)


@responses.activate
def test_update_pipeline_bad_json(app, organization_pipeline):
    responses.add(
        responses.PUT,
        f"{app.config[WORKFLOW_HOSTNAME]}/v1/pipelines/{organization_pipeline.pipeline_uuid}",
        body="notjson",
    )
    with pytest.raises(HTTPError):
        update_pipeline(ORGANIZATION_UUID, organization_pipeline.uuid, PIPELINE_JSON)


@responses.activate
def test_update_pipeline(app, organization_pipeline):
    json_response = dict(PIPELINE_JSON)
    json_response.update(
        {
            "updated_at": "2020-10-08T14:22:26.276242",
            "created_at": "2020-10-08T14:22:26.276278",
            "uuid": "83ac3b4e9433431fbd6d21e7a56b6f0a",
        }
    )
    responses.add(
        responses.PUT,
        f"{app.config[WORKFLOW_HOSTNAME]}/v1/pipelines/{organization_pipeline.pipeline_uuid}",
        json=json_response,
    )
    updated_pipeline = update_pipeline(
        ORGANIZATION_UUID, organization_pipeline.uuid, PIPELINE_JSON
    )
    organization_pipeline = OrganizationPipeline.query.order_by(
        OrganizationPipeline.id.desc()
    ).first()
    json_response["uuid"] = organization_pipeline.uuid
    assert updated_pipeline == json_response


@responses.activate
def test_delete_pipeline_no_pipeline(app, organization_pipeline):
    with pytest.raises(ValueError):
        delete_pipeline(ORGANIZATION_UUID, "badid")
    organization_pipeline = set(OrganizationPipeline.query.all()) == set(
        [organization_pipeline]
    )


@responses.activate
def test_delete_pipeline(app, organization_pipeline):
    responses.add(
        responses.DELETE,
        f"{app.config[WORKFLOW_HOSTNAME]}/v1/pipelines/{organization_pipeline.pipeline_uuid}",
    )
    delete_pipeline(ORGANIZATION_UUID, organization_pipeline.uuid)

    assert organization_pipeline.is_deleted


def test_create_pipeline_input_file_no_org(app, organization_pipeline):
    with pytest.raises(ValueError):
        create_pipeline_input_file(None, "saname.txt" * 26, None)


@patch("app.pipelines.services.upload_stream")
def test_create_pipeline_input_file_validate(
    upload_stream_mock, app, organization_pipeline
):
    data = io.StringIO("some data")
    with pytest.raises(ValueError):
        create_pipeline_input_file(organization_pipeline, "saname.txt" * 26, data)
    with pytest.raises(ValueError):
        create_pipeline_input_file(organization_pipeline, "1", data)
    assert not upload_stream_mock.called


@patch("app.pipelines.services.upload_stream")
def test_create_pipeline_input_file(upload_stream_mock, app, organization_pipeline):
    data = io.StringIO("some data")
    input_file = create_pipeline_input_file(organization_pipeline, "aname.txt", data)
    assert input_file.name == "aname.txt"
    assert upload_stream_mock.called
    assert set(organization_pipeline.organization_pipeline_input_files) == {input_file}


@patch("app.pipelines.services.create_url")
@responses.activate
def test_create_pipeline_run(
    mock_url, app, organization_pipeline, organization_pipeline_input_file
):
    json_response = dict(PIPELINE_RUN_RESPONSE_JSON)
    mock_url.return_value = "http://somefileurl.com"

    pipeline = OrganizationPipeline.query.order_by(
        OrganizationPipeline.id.desc()
    ).first()

    responses.add(
        responses.POST,
        f"{app.config[WORKFLOW_HOSTNAME]}/v1/pipelines/{pipeline.pipeline_uuid}/runs",
        json=json_response,
    )

    created_pipeline_run = create_pipeline_run(
        pipeline.organization_uuid, pipeline.uuid, PIPELINE_RUN_JSON
    )

    new_run = OrganizationPipelineRun.query.filter(
        OrganizationPipelineRun.pipeline_run_uuid == created_pipeline_run["uuid"]
    ).first()

    assert new_run is not None
    assert created_pipeline_run == json_response


@patch("app.pipelines.services.create_url")
def test_create_pipeline_run_invalid_org(
    mock_url, app, organization_pipeline, organization_pipeline_input_file
):
    mock_url.return_value = "http://somefileurl.com"
    json_request = {"inputs": []}

    with pytest.raises(ValueError):
        created_pipeline_run = create_pipeline_run("12345", "12345", json_request)


@patch("app.pipelines.services.create_url")
@responses.activate
def test_create_pipeline_run_missing_pipeline(
    mock_url, app, organization_pipeline, organization_pipeline_input_file
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

    with pytest.raises(ValueError):
        created_pipeline_run = create_pipeline_run(
            pipeline.organization_uuid, "1234", PIPELINE_RUN_JSON
        )


@patch("app.pipelines.services.create_url")
@responses.activate
def test_create_pipeline_run_response_error(
    mock_url, app, organization_pipeline, organization_pipeline_input_file
):

    mock_url.return_value = "http://somefileurl.com"
    json_response = dict(PIPELINE_RUN_RESPONSE_JSON)

    responses.add(
        responses.POST,
        f"{app.config[WORKFLOW_HOSTNAME]}/v1/pipelines/{organization_pipeline.pipeline_uuid}/runs",
        status=503,
    )

    with pytest.raises(HTTPError):
        created_pipeline_run = create_pipeline_run(
            organization_pipeline.organization_uuid,
            organization_pipeline.uuid,
            PIPELINE_RUN_JSON,
        )


@patch("app.pipelines.services.create_url")
@responses.activate
def test_create_pipeline_run_notfound_error(
    mock_url, app, organization_pipeline, organization_pipeline_input_file
):

    mock_url.return_value = "http://somefileurl.com"
    json_response = dict(PIPELINE_RUN_RESPONSE_JSON)

    responses.add(
        responses.POST,
        f"{app.config[WORKFLOW_HOSTNAME]}/v1/pipelines/{organization_pipeline.pipeline_uuid}/runs",
        json={"error": "not found"},
        status=404,
    )

    with pytest.raises(ValueError):
        created_pipeline_run = create_pipeline_run(
            organization_pipeline.organization_uuid,
            organization_pipeline.uuid,
            PIPELINE_RUN_JSON,
        )


@patch("app.pipelines.services.create_url")
@responses.activate
def test_fetch_pipeline_runs(
    mock_url,
    app,
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

    pipeline_runs = fetch_pipeline_runs(pipeline.organization_uuid, pipeline.uuid)

    assert pipeline_runs is not None
    assert pipeline_runs == json_response


@responses.activate
def test_fetch_pipeline_runs_response_error(app, organization_pipeline):
    json_response = dict(PIPELINE_RUN_RESPONSE_JSON)

    responses.add(
        responses.GET,
        f"{app.config[WORKFLOW_HOSTNAME]}/v1/pipelines/{organization_pipeline.pipeline_uuid}/runs",
        status=503,
    )

    with pytest.raises(HTTPError):
        fetch_pipeline_runs(
            organization_pipeline.organization_uuid, organization_pipeline.uuid
        )


@responses.activate
def test_fetch_pipeline_runs_notfound_error(app, organization_pipeline):
    json_response = dict(PIPELINE_RUN_RESPONSE_JSON)

    responses.add(
        responses.GET,
        f"{app.config[WORKFLOW_HOSTNAME]}/v1/pipelines/{organization_pipeline.pipeline_uuid}/runs",
        json={"error": "not found"},
        status=404,
    )

    with pytest.raises(ValueError):
        fetch_pipeline_runs(
            organization_pipeline.organization_uuid, organization_pipeline.uuid
        )


@patch("app.pipelines.services.create_url")
@responses.activate
def test_fetch_pipeline_run(
    mock_url,
    app,
    organization_pipeline,
    organization_pipeline_run,
    organization_pipeline_input_file,
):
    json_response = dict(PIPELINE_RUN_RESPONSE_JSON)

    mock_url.return_value = "http://somefileurl.com"
    responses.add(
        responses.GET,
        f"{app.config[WORKFLOW_HOSTNAME]}/v1/pipelines/{organization_pipeline.pipeline_uuid}/runs/{organization_pipeline_run.pipeline_run_uuid}",
        json=json_response,
    )

    pipeline_run = fetch_pipeline_run(
        organization_pipeline.organization_uuid,
        organization_pipeline.uuid,
        organization_pipeline_run.uuid,
    )

    assert pipeline_run is not None
    assert pipeline_run == json_response


@responses.activate
def test_fetch_pipeline_error(app, organization_pipeline, organization_pipeline_run):
    responses.add(
        responses.GET,
        f"{app.config[WORKFLOW_HOSTNAME]}/v1/pipelines/{organization_pipeline.pipeline_uuid}/runs/{organization_pipeline_run.pipeline_run_uuid}",
        status=503,
    )

    with pytest.raises(HTTPError):
        fetch_pipeline_run(
            organization_pipeline.organization_uuid,
            organization_pipeline.uuid,
            organization_pipeline_run.uuid,
        )


@responses.activate
def test_fetch_pipeline_notfound(app, organization_pipeline, organization_pipeline_run):
    responses.add(
        responses.GET,
        f"{app.config[WORKFLOW_HOSTNAME]}/v1/pipelines/{organization_pipeline.pipeline_uuid}/runs/{organization_pipeline_run.pipeline_run_uuid}",
        json={"error": "not found"},
        status=404,
    )

    with pytest.raises(ValueError):
        fetch_pipeline_run(
            organization_pipeline.organization_uuid,
            organization_pipeline.uuid,
            organization_pipeline_run.uuid,
        )


@responses.activate
def test_fetch_pipeline_run_console(
    app, organization_pipeline, organization_pipeline_run
):
    json_response = dict(PIPELINE_RUN_CONSOLE_RESPONSE_JSON)

    responses.add(
        responses.GET,
        f"{app.config[WORKFLOW_HOSTNAME]}/v1/pipelines/{organization_pipeline.pipeline_uuid}/runs/{organization_pipeline_run.pipeline_run_uuid}/console",
        json=json_response,
    )

    console_output = fetch_pipeline_run_console(
        organization_pipeline.organization_uuid,
        organization_pipeline.uuid,
        organization_pipeline_run.uuid,
    )

    assert console_output is not None
    assert console_output == json_response


@responses.activate
def test_fetch_pipeline_run_error(
    app, organization_pipeline, organization_pipeline_run
):
    responses.add(
        responses.GET,
        f"{app.config[WORKFLOW_HOSTNAME]}/v1/pipelines/{organization_pipeline.pipeline_uuid}/runs/{organization_pipeline_run.pipeline_run_uuid}/console",
        status=503,
    )

    with pytest.raises(HTTPError):
        fetch_pipeline_run_console(
            organization_pipeline.organization_uuid,
            organization_pipeline.uuid,
            organization_pipeline_run.uuid,
        )


@responses.activate
def test_fetch_pipeline_run_notfound(
    app, organization_pipeline, organization_pipeline_run
):
    responses.add(
        responses.GET,
        f"{app.config[WORKFLOW_HOSTNAME]}/v1/pipelines/{organization_pipeline.pipeline_uuid}/runs/{organization_pipeline_run.pipeline_run_uuid}/console",
        json={},
        status=404,
    )

    with pytest.raises(ValueError):
        fetch_pipeline_run_console(
            organization_pipeline.organization_uuid,
            organization_pipeline.uuid,
            organization_pipeline_run.uuid,
        )


@responses.activate
def test_create_artifact_chart_no_pipeline_run_found(
    app, organization_pipeline, organization_pipeline_run
):
    responses.add(
        responses.GET,
        f"{app.config[WORKFLOW_HOSTNAME]}/v1/pipelines/{organization_pipeline.pipeline_uuid}/runs/{organization_pipeline_run.pipeline_run_uuid}",
        json={},
        status=404,
    )
    with pytest.raises(ValueError):
        create_artifact_chart(organization_pipeline_run, CHART_JSON)
    assert set(ArtifactChart.query.all()) == set()


@responses.activate
def test_create_artifact_chart_no_artifact_found(
    app, organization_pipeline, organization_pipeline_run
):
    responses.add(
        responses.GET,
        f"{app.config[WORKFLOW_HOSTNAME]}/v1/pipelines/{organization_pipeline.pipeline_uuid}/runs/{organization_pipeline_run.pipeline_run_uuid}",
        json=PIPELINE_RUN_RESPONSE_JSON,
    )
    with pytest.raises(ValueError):
        create_artifact_chart(organization_pipeline_run, CHART_JSON)
    assert set(ArtifactChart.query.all()) == set()


@responses.activate
def test_create_artifact_chart_bad_name(
    app, organization_pipeline, organization_pipeline_run
):
    chart_json = dict(CHART_JSON)
    chart_json["name"] = ""
    with pytest.raises(ValidationError):
        create_artifact_chart(organization_pipeline_run, chart_json)
    assert set(ArtifactChart.query.all()) == set()


@responses.activate
def test_create_artifact_chart(app, organization_pipeline, organization_pipeline_run):
    responses.add(
        responses.GET,
        f"{app.config[WORKFLOW_HOSTNAME]}/v1/pipelines/{organization_pipeline.pipeline_uuid}/runs/{organization_pipeline_run.pipeline_run_uuid}",
        json=FINISHED_PIPELINE_RUN_RESPONSE_JSON,
    )

    chart_json_result = create_artifact_chart(organization_pipeline_run, CHART_JSON)
    chart = ArtifactChart.query.first()

    assert chart_json_result == {
        "uuid": chart.uuid,
        "name": chart.name,
        "artifact": FINISHED_PIPELINE_RUN_RESPONSE_JSON["artifacts"][0],
        "chart_type_code": chart.chart_type_code,
        "chart_config": chart.chart_config,
        "created_at": chart.created_at.isoformat(),
        "updated_at": chart.updated_at.isoformat(),
    }
    assert chart.organization_pipeline_run == organization_pipeline_run


@responses.activate
def test_create_artifact_chart_no_config(
    app, organization_pipeline, organization_pipeline_run
):
    responses.add(
        responses.GET,
        f"{app.config[WORKFLOW_HOSTNAME]}/v1/pipelines/{organization_pipeline.pipeline_uuid}/runs/{organization_pipeline_run.pipeline_run_uuid}",
        json=FINISHED_PIPELINE_RUN_RESPONSE_JSON,
    )

    chart_json = dict(CHART_JSON)
    del chart_json["chart_config"]
    chart_json_result = create_artifact_chart(organization_pipeline_run, chart_json)
    chart = ArtifactChart.query.first()

    assert chart_json_result == {
        "uuid": chart.uuid,
        "name": chart.name,
        "artifact": FINISHED_PIPELINE_RUN_RESPONSE_JSON["artifacts"][0],
        "chart_type_code": chart.chart_type_code,
        "chart_config": {},
        "created_at": chart.created_at.isoformat(),
        "updated_at": chart.updated_at.isoformat(),
    }
    assert chart.organization_pipeline_run == organization_pipeline_run


@responses.activate
def test_fetch_artifact_charts_no_chart_found(
    app, organization_pipeline, organization_pipeline_run
):
    responses.add(
        responses.GET,
        f"{app.config[WORKFLOW_HOSTNAME]}/v1/pipelines/{organization_pipeline.pipeline_uuid}/runs/{organization_pipeline_run.pipeline_run_uuid}",
        json=FINISHED_PIPELINE_RUN_RESPONSE_JSON,
    )

    chart = ArtifactChart(
        name="a chart",
        artifact_uuid="noid",
        chart_type_code="ACODE",
        chart_config="{}",
    )
    organization_pipeline_run.artifact_charts.append(chart)
    db.session.commit()

    with pytest.raises(ValueError):
        fetch_artifact_charts(organization_pipeline_run)


@responses.activate
def test_fetch_artifact_charts(app, organization_pipeline, organization_pipeline_run):
    responses.add(
        responses.GET,
        f"{app.config[WORKFLOW_HOSTNAME]}/v1/pipelines/{organization_pipeline.pipeline_uuid}/runs/{organization_pipeline_run.pipeline_run_uuid}",
        json=FINISHED_PIPELINE_RUN_RESPONSE_JSON,
    )

    chart = ArtifactChart(
        name="a chart",
        artifact_uuid=FINISHED_PIPELINE_RUN_RESPONSE_JSON["artifacts"][0]["uuid"],
        chart_type_code="ACODE",
        chart_config="{}",
    )
    organization_pipeline_run.artifact_charts.append(chart)
    db.session.commit()

    chart_json_result = fetch_artifact_charts(organization_pipeline_run)

    assert chart_json_result == [
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
