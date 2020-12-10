from openfido import services
import responses

empty = {
  "name": "Example workflow",
  "description": "description example",
  "pipelines": [ ]
}

line = {
  "name": "Line workflow",
  "description": "description example",
  "pipelines": [
    {
      "uuid": "04f01114cbaf4ca98724a7c7965f9df3"
    },
    {
      "uuid": "cef461a5c10945e4b81ae480fe3c8b38",
      "dependencies": [
        "04f01114cbaf4ca98724a7c7965f9df3"
      ]
    }
  ]
}


@responses.activate
def test_create_workflow_empty(session):
    responses.add(
        responses.POST,
        f"http://app-api/v1/organizations/organization-uuid/workflows",
        match=[
            responses.json_params_matcher({
                "name": empty["name"],
                "description": empty["description"],
            })
        ],
        json={
            "created_at": "2020-12-10T16:39:01.189231",
            "description": empty["description"],
            "name": empty["name"],
            "updated_at": "2020-12-10T16:39:30.324064",
            "uuid": "a-uuid"
        },
    )
    responses.add(
        responses.GET,
        f"http://app-api/v1/organizations/organization-uuid/workflows/a-uuid/pipelines",
        json=[],
    )
    assert services.create_workflow(session, 'http://app-api', empty) == 'a-uuid'


@responses.activate
def test_update_workflow_empty(session):
    responses.add(
        responses.PUT,
        f"http://app-api/v1/organizations/organization-uuid/workflows/a-uuid",
        match=[
            responses.json_params_matcher({
                "name": empty["name"],
                "description": empty["description"],
            })
        ],
        json={
            "created_at": "2020-12-10T16:39:01.189231",
            "description": empty["description"],
            "name": empty["name"],
            "updated_at": "2020-12-10T16:39:30.324064",
            "uuid": "e1fc3a54188b4f43a3b45b621c782fe8"
        },
    )
    responses.add(
        responses.GET,
        f"http://app-api/v1/organizations/organization-uuid/workflows/a-uuid/pipelines",
        json=[],
    )
    assert services.update_workflow(session, 'http://app-api', 'a-uuid', empty) == 'a-uuid'


# @responses.activate
# def test_update_workflow_line(session):
#     responses.add(
#         responses.PUT,
#         f"http://app-api/v1/organizations/organization-uuid/workflows/a-uuid",
#         match=[
#             responses.json_params_matcher({
#                 "name": empty["name"],
#                 "description": empty["description"],
#             })
#         ],
#         json={
#             "created_at": "2020-12-10T16:39:01.189231",
#             "description": "description example",
#             "name": "Line workflow",
#             "updated_at": "2020-12-10T16:39:30.324064",
#             "uuid": "e1fc3a54188b4f43a3b45b621c782fe8"
#         },
#     )
#     responses.add(
#         responses.GET,
#         f"http://app-api/v1/organizations/organization-uuid/workflows/a-uuid/pipelines",
#         json=[{
#             "created_at": "2020-12-10T16:46:10.965112",
#             "destination_workflow_pipelines": [],
#             "pipeline_uuid": "cef461a5c10945e4b81ae480fe3c8b38",
#             "source_workflow_pipelines": [],
#             "updated_at": "2020-12-10T16:46:10.965127",
#             "uuid": "daa74cfa1f1f439cafd4bf4d8fa1e71b"
#         }],
#     )
#     services.update_workflow(session, 'http://app-api', 'a-uuid', empty)
