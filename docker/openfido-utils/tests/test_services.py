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


@responses.activate
def test_create_workflow_empty(session):
    responses.add(
        responses.POST,
        f"http://app-api/v1/organizations/organization-1/workflows",
        match=[
            responses.json_params_matcher({
                "name": EMPTY["name"],
                "description": EMPTY["description"],
            })
        ],
        json={
            "created_at": "2020-12-10T16:39:01.189231",
            "description": EMPTY["description"],
            "name": EMPTY["name"],
            "updated_at": "2020-12-10T16:39:30.324064",
            "uuid": "workflow-1"
        },
    )
    responses.add(
        responses.GET,
        f"http://app-api/v1/organizations/organization-1/workflows/workflow-1/pipelines",
        json=[],
    )
    assert services.create_workflow(session, 'http://app-api', EMPTY) == 'workflow-1'


@responses.activate
def test_update_workflow_empty(session):
    responses.add(
        responses.PUT,
        f"http://app-api/v1/organizations/organization-1/workflows/workflow-1",
        match=[
            responses.json_params_matcher({
                "name": EMPTY["name"],
                "description": EMPTY["description"],
            })
        ],
        json={
            "created_at": "2020-12-10T16:39:01.189231",
            "description": EMPTY["description"],
            "name": EMPTY["name"],
            "updated_at": "2020-12-10T16:39:30.324064",
            "uuid": "workflow-1"
        },
    )
    responses.add(
        responses.GET,
        f"http://app-api/v1/organizations/organization-1/workflows/workflow-1/pipelines",
        json=[],
    )
    assert services.update_workflow(session, 'http://app-api', 'workflow-1', EMPTY) == 'workflow-1'


@responses.activate
def test_update_workflow_line(session):
    responses.add(
        responses.PUT,
        f"http://app-api/v1/organizations/organization-1/workflows/workflow-1",
        match=[
            responses.json_params_matcher({
                "name": LINE["name"],
                "description": LINE["description"],
            })
        ],
        json={
            "created_at": "2020-12-10T16:39:01.189231",
            "description": LINE["description"],
            "name": LINE["name"],
            "updated_at": "2020-12-10T16:39:30.324064",
            "uuid": "workflow-1"
        },
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
            f"http://app-api/v1/organizations/organization-1/workflows/workflow-1/pipelines/workflow-{pipeline['uuid']}",
            json={},
            match=[
                responses.json_params_matcher({
                    'pipeline_uuid': pipeline['uuid'],
                    'source_workflow_pipelines': [f"workflow-{p}" for p in pipeline.get('dependencies', [])],
                    'destination_workflow_pipelines': [],
                })
            ],
        )

    assert services.update_workflow(session, 'http://app-api', 'workflow-1', LINE) == 'workflow-1'
