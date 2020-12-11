from openfido import services
import responses

EMPTY = {
  "name": "Example workflow",
  "description": "description example",
  "pipelines": [ ]
}

LINE = {
  "name": "Line workflow",
  "description": "description example",
  "pipelines": [
    {
      "uuid": "pipeline-1"
    },
    {
      "uuid": "pipeline-2",
      "dependencies": [
        "pipeline-1"
      ]
    }
  ]
}


def _test_empty(method, session, extra_param=''):
    workflow_json = {
        "created_at": "2020-12-10T16:39:01.189231",
        "description": EMPTY["description"],
        "name": EMPTY["name"],
        "updated_at": "2020-12-10T16:39:30.324064",
        "uuid": "workflow-1"
    }
    responses.add(
        method,
        f"http://app-api/v1/organizations/organization-1/workflows{extra_param}",
        match=[
            responses.json_params_matcher({
                "name": EMPTY["name"],
                "description": EMPTY["description"],
            })
        ],
        json=workflow_json,
    )
    responses.add(
        responses.GET,
        f"http://app-api/v1/organizations/organization-1/workflows/workflow-1/pipelines",
        json=[],
    )
    # view the results:
    responses.add(
        responses.GET,
        f"http://app-api/v1/organizations/organization-1/workflows/workflow-1",
        json=workflow_json,
    )


@responses.activate
def test_create_workflow_empty(session):
    _test_empty(responses.POST, session)
    services.create_workflow(session, 'http://app-api', EMPTY)


@responses.activate
def test_update_workflow_empty(session):
    _test_empty(responses.PUT, session, '/workflow-1')
    services.update_workflow(session, 'http://app-api', 'workflow-1', EMPTY)


def _test_line(method, session, extra_param=''):
    workflow_json = {
        "created_at": "2020-12-10T16:39:01.189231",
        "description": LINE["description"],
        "name": LINE["name"],
        "updated_at": "2020-12-10T16:39:30.324064",
        "uuid": "workflow-1"
    }
    responses.add(
        method,
        f"http://app-api/v1/organizations/organization-1/workflows{extra_param}",
        match=[
            responses.json_params_matcher({
                "name": LINE["name"],
                "description": LINE["description"],
            })
        ],
        json=workflow_json,
    )
    responses.add(
        responses.GET,
        f"http://app-api/v1/organizations/organization-1/workflows/workflow-1/pipelines",
        json=[{
            "created_at": "2020-12-10T16:46:10.965112",
            "destination_workflow_pipelines": [],
            "pipeline_uuid": "pipeline-1",
            "source_workflow_pipelines": [],
            "updated_at": "2020-12-10T16:46:10.965127",
            "uuid": "workflow-pipeline-1"
        }, {
            "created_at": "2020-12-10T16:46:10.965112",
            "destination_workflow_pipelines": [],
            "pipeline_uuid": "pipeline-2",
            "source_workflow_pipelines": [],
            "updated_at": "2020-12-10T16:46:10.965127",
            "uuid": "workflow-pipeline-2"
        }],
    )

    for pipeline in LINE['pipelines']:
        responses.add(
            responses.POST,
            f"http://app-api/v1/organizations/organization-1/workflows/workflow-1/pipelines",
            json={},
            match=[
                responses.json_params_matcher({
                    'pipeline_uuid': pipeline['uuid'],
                    'source_workflow_pipelines': [],
                    'destination_workflow_pipelines': [],
                })
            ],
        )

    responses.add(
        responses.PUT,
        f"http://app-api/v1/organizations/organization-1/workflows/workflow-1/pipelines/workflow-{LINE['pipelines'][0]['uuid']}",
        json={},
        match=[
            responses.json_params_matcher({
                'pipeline_uuid': LINE['pipelines'][0]['uuid'],
                'source_workflow_pipelines': [],
                'destination_workflow_pipelines': [f"workflow-{LINE['pipelines'][1]['uuid']}"],
            })
        ],
    )
    responses.add(
        responses.PUT,
        f"http://app-api/v1/organizations/organization-1/workflows/workflow-1/pipelines/workflow-{LINE['pipelines'][1]['uuid']}",
        json={},
        match=[
            responses.json_params_matcher({
                'pipeline_uuid': LINE['pipelines'][1]['uuid'],
                'source_workflow_pipelines': [f"workflow-{LINE['pipelines'][0]['uuid']}"],
                'destination_workflow_pipelines': [],
            })
        ],
    )
    # view the results:
    responses.add(
        responses.GET,
        f"http://app-api/v1/organizations/organization-1/workflows/workflow-1",
        json=workflow_json,
    )
    responses.add(
        responses.GET,
        f"http://app-api/v1/organizations/organization-1/workflows/workflow-1/pipelines/workflow-{LINE['pipelines'][0]['uuid']}",
        json={
            "source_workflow_pipelines": [],
        },
    )
    responses.add(
        responses.GET,
        f"http://app-api/v1/organizations/organization-1/workflows/workflow-1/pipelines/workflow-{LINE['pipelines'][1]['uuid']}",
        json={
            "source_workflow_pipelines": [],
        },
    )


@responses.activate
def test_create_workflow_line(session):
    _test_line(responses.POST, session)
    services.create_workflow(session, 'http://app-api', LINE)


@responses.activate
def test_update_workflow_line(session):
    _test_line(responses.PUT, session, '/workflow-1')
    services.update_workflow(session, 'http://app-api', 'workflow-1', LINE)
