import logging

logger = logging.getLogger('openfido.services')

def _call_api(session, url, method="get", json_data=None):
    """ Call a URL within a session and return the JSON response. """
    logger.debug("json_data:")
    logger.debug(json_data)
    response = getattr(session, method)(url, json=json_data)
    logger.debug(response.text)
    response_json = response.json()
    response.raise_for_status()

    return response_json


def login(auth_session, app_session, api_url, email, password):
    """ Login as email. On success, store the JWT token and organization uuid in
    the app_session headers for future use.

    TODO if the user is a member of more than one organization, raises an error.
    """
    auth_json = _call_api(auth_session, f"{api_url}/users/auth", "post", {
        'email': email,
        'password': password
    })

    app_session.headers['Authorization'] = f"Bearer {auth_json['token']}"
    auth_session.headers['Authorization'] = f"Bearer {auth_json['token']}"

    orgs_json = _call_api(auth_session, f"{api_url}/users/{auth_json['uuid']}/organizations")

    if len(orgs_json) != 1:
        raise ValueError("User is either not a member of an organization, or a member of many!")

    app_session.headers['X-Organization'] = orgs_json[0]["uuid"]


def view_workflow(app_session, app_url, uuid):
    workflow_json = _call_api(
        app_session,
        f"{app_url}/v1/organizations/{app_session.headers['X-Organization']}/workflows/{uuid}",
    )
    workflow_pipelines = _call_api(
        app_session,
        f"{app_url}/v1/organizations/{app_session.headers['X-Organization']}/workflows/{uuid}/pipelines"
    )

    print(f"Name: {workflow_json['name']}")
    print(f"ID: {workflow_json['uuid']}")
    print()
    print("Pipelines:")
    for wp in workflow_pipelines:
        workflow_pipeline = _call_api(
            app_session,
            f"{app_url}/v1/organizations/{app_session.headers['X-Organization']}/workflows/{uuid}/pipelines/{wp['uuid']}"
        )
        print(f"ID: {wp['uuid']}")
        print("Dependencies:")


def _update_workflow_pipelines(app_session, app_url, create_workflow_data, uuid):
    workflow_pipelines = _call_api(
        app_session,
        f"{app_url}/v1/organizations/{app_session.headers['X-Organization']}/workflows/{uuid}/pipelines"
    )

    # TODO compare the sets.

    # Create a workflow pipeline in the workflow if it doesn't already exist:
    for pipeline in create_workflow_data['pipelines']:
        if pipeline['uuid'] not in [wp['pipeline_uuid'] for wp in workflow_pipelines]:
            _call_api(
                app_session,
                f"{app_url}/v1/organizations/{app_session.headers['X-Organization']}/workflows/{uuid}/pipelines",
                'post',
                {
                    'pipeline_uuid': pipeline['uuid'],
                    'source_workflow_pipelines': [],
                    'destination_workflow_pipelines': [],
                }
            )

    # TODO remove workflow pipelines when relationships are gone.

    workflow_pipelines = _call_api(
        app_session,
        f"{app_url}/v1/organizations/{app_session.headers['X-Organization']}/workflows/{uuid}/pipelines"
    )

    # Update the workflow pipeline relationships
    for pipeline in create_workflow_data['pipelines']:
        workflow_pipeline_uuid = next(wp['uuid'] for wp in workflow_pipelines if wp['pipeline_uuid'] == pipeline['uuid'])
        dependencies = pipeline.get('dependencies', [])
        _call_api(
            app_session,
            f"{app_url}/v1/organizations/{app_session.headers['X-Organization']}/workflows/{uuid}/pipelines/{workflow_pipeline_uuid}",
            'put',
            {
                'pipeline_uuid': pipeline['uuid'],
                'source_workflow_pipelines': [wp['uuid'] for wp in workflow_pipelines if wp['pipeline_uuid'] in dependencies],
                'destination_workflow_pipelines': [],
            }
        )


def create_workflow(app_session, app_url, create_workflow_data):
    """ Create a new Workflow. Returns workflow UUID. """
    workflow_json = _call_api(
        app_session,
        f"{app_url}/v1/organizations/{app_session.headers['X-Organization']}/workflows",
        'post',
        {
            "name": create_workflow_data["name"],
            "description": create_workflow_data["description"],
        }
    )

    _update_workflow_pipelines(app_session, app_url, create_workflow_data, workflow_json["uuid"])

    return workflow_json["uuid"]


def update_workflow(app_session, app_url, uuid, create_workflow_data):
    """ Update a Workflow. Returns workflow UUID. """
    _call_api(
        app_session,
        f"{app_url}/v1/organizations/{app_session.headers['X-Organization']}/workflows/{uuid}",
        'put',
        {
            "name": create_workflow_data["name"],
            "description": create_workflow_data["description"],
        }
    )

    _update_workflow_pipelines(app_session, app_url, create_workflow_data, uuid)

    return uuid
