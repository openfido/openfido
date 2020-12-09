import logging

logger = logging.getLogger('openfido.services')


def login(auth_session, app_session, api_url, email, password):
    """ Login as email. On success, store the JWT token and organization uuid in
    the app_session headers for future use.

    TODO if the user is a member of more than one organization, raises an error.
    """
    auth = auth_session.post(f"{api_url}/users/auth",
                            json={
                                'email': email,
                                'password': password
                            })
    auth_json = auth.json()
    logger.debug(auth_json)
    auth.raise_for_status()

    app_session.headers['Authorization'] = f"Bearer {auth_json['token']}"
    auth_session.headers['Authorization'] = f"Bearer {auth_json['token']}"

    orgs = auth_session.get(f"{api_url}/users/{auth_json['uuid']}/organizations")
    orgs_json = orgs.json()
    logger.debug(orgs_json)
    orgs.raise_for_status()

    if len(orgs_json) != 1:
        raise ValueError("User is either not a member of an organization, or a member of many!")

    app_session.headers['X-Organization'] = orgs_json[0]["uuid"]


def create_workflow(app_session, app_url, create_workflow_data):
    """ Create a new Workflow. Returns workflow UUID. """
    workflow = app_session.post(
        f"{app_url}/v1/organizations/{app_session.headers['X-Organization']}/workflows",
        json={
            "name": create_workflow_data["name"],
            "description": create_workflow_data["description"],
        }
    )
    workflow_json = workflow.json()
    logger.debug(workflow_json)
    workflow.raise_for_status()

    return workflow_json["uuid"]


def update_workflow(app_session, app_url, uuid, create_workflow_data):
    """ Update a Workflow. Returns workflow UUID. """
    workflow = app_session.put(
        f"{app_url}/v1/organizations/{app_session.headers['X-Organization']}/workflows/{uuid}",
        json={
            "name": create_workflow_data["name"],
            "description": create_workflow_data["description"],
        }
    )
    workflow_json = workflow.json()
    logger.debug(workflow_json)
    workflow.raise_for_status()

    return workflow_json["uuid"]
