import logging

from collections import defaultdict

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


def list_workflows(app_session, app_url):
    workflows_json = _call_api(
        app_session,
        f"{app_url}/v1/organizations/{app_session.headers['X-Organization']}/workflows",
    )
    for workflow in workflows_json:
        print(f"Name: {workflow['name']}")
        print(f"ID: {workflow['uuid']}")
        print()


def dot_workflow(app_session, app_url, uuid):
    """ Create a graphviz dot file. """
    workflow_json = _call_api(
        app_session,
        f"{app_url}/v1/organizations/{app_session.headers['X-Organization']}/workflows/{uuid}",
    )
    workflow_pipelines = _call_api(
        app_session,
        f"{app_url}/v1/organizations/{app_session.headers['X-Organization']}/workflows/{uuid}/pipelines"
    )

    print("digraph G {")
    print('  labelloc="t";')
    print(f"  label=\"{workflow_json['name']} ({workflow_json['uuid']})\";")
    print(f"  graph[ranksep=2,splines=true];")

    for wp in workflow_pipelines:
        workflow_pipeline = _call_api(
            app_session,
            f"{app_url}/v1/organizations/{app_session.headers['X-Organization']}/workflows/{uuid}/pipelines/{wp['uuid']}"
        )
        # TODO fetch name.
        print(f"  \"{wp['uuid']}\" {{}};")
        for source in workflow_pipeline["source_workflow_pipelines"]:
            print(f"  \"{source}\" -> \"{wp['uuid']}\";")
    print("}")


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
        # TODO fetch name.
        print(f"ID: {wp['uuid']} ({wp['pipeline_uuid']})")
        if len(workflow_pipeline["source_workflow_pipelines"]) > 0:
            print("Dependencies:")
        for source in workflow_pipeline["source_workflow_pipelines"]:
            print(source)


def _update_workflow_pipelines(app_session, app_url, create_workflow_data, workflow_uuid):
    workflow_pipelines = _call_api(
        app_session,
        f"{app_url}/v1/organizations/{app_session.headers['X-Organization']}/workflows/{workflow_uuid}/pipelines"
    )

    # Create a workflow pipeline in the workflow if it doesn't already exist:
    server_pipelines = {wp['pipeline_uuid'] for wp in workflow_pipelines}
    data_pipelines = {p['uuid'] for p in create_workflow_data['pipelines']}
    for pipeline_uuid in data_pipelines - server_pipelines:
        _call_api(
            app_session,
            f"{app_url}/v1/organizations/{app_session.headers['X-Organization']}/workflows/{workflow_uuid}/pipelines",
            'post',
            {
                'pipeline_uuid': pipeline_uuid,
                'source_workflow_pipelines': [],
                'destination_workflow_pipelines': [],
            }
        )

    # Remove any pipelines that should no longer exist:
    for pipeline_uuid in server_pipelines - data_pipelines:
        wp = next(wp['uuid'] for wp in workflow_pipelines if wp['pipeline_uuid'] == pipeline_uuid)
        _call_api(
            app_session,
            f"{app_url}/v1/organizations/{app_session.headers['X-Organization']}/workflows/{workflow_uuid}/pipelines/{wp}",
            'delete'
        )

    workflow_pipelines = _call_api(
        app_session,
        f"{app_url}/v1/organizations/{app_session.headers['X-Organization']}/workflows/{workflow_uuid}/pipelines"
    )

    # Update the workflow pipeline relationships
    pipeline_to_workflow_pipeline = {
        wp['pipeline_uuid']: wp['uuid'] for wp in workflow_pipelines
    }
    source_to_dests = defaultdict(list)
    dests_to_sources = defaultdict(list)
    for pipeline in create_workflow_data['pipelines']:
        pipeline_wp = pipeline_to_workflow_pipeline[pipeline['uuid']]
        for dependency in pipeline.get('dependencies', []):
            dependency_wp = pipeline_to_workflow_pipeline[dependency]
            source_to_dests[dependency].append(pipeline_wp)
            dests_to_sources[pipeline['uuid']].append(dependency_wp)

    logger.debug("source_to_dests")
    logger.debug(source_to_dests)
    logger.debug("dests_to_sources")
    logger.debug(dests_to_sources)

    for pipeline in create_workflow_data['pipelines']:
        workflow_pipeline_uuid = next(wp['uuid'] for wp in workflow_pipelines if wp['pipeline_uuid'] == pipeline['uuid'])
        _call_api(
            app_session,
            f"{app_url}/v1/organizations/{app_session.headers['X-Organization']}/workflows/{workflow_uuid}/pipelines/{workflow_pipeline_uuid}",
            'put',
            {
                'pipeline_uuid': pipeline['uuid'],
                'source_workflow_pipelines': dests_to_sources[pipeline['uuid']],
                'destination_workflow_pipelines': source_to_dests[pipeline['uuid']]
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

    view_workflow(app_session, app_url, workflow_json["uuid"])


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

    view_workflow(app_session, app_url, uuid)
