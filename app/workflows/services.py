import requests

from flask import current_app
from requests import HTTPError

from application_roles.decorators import ROLES_KEY
from app.constants import WORKFLOW_API_TOKEN, WORKFLOW_HOSTNAME

from app.workflows.models import (
    OrganizationWorkflow,
    db,
)
from app.workflows.queries import (
    find_organization_workflow,
    find_organization_workflows,
)


def create_workflow(organization_uuid, request_json):
    """ Create a new workflow associated with an organization. """
    response = requests.post(
        f"{current_app.config[WORKFLOW_HOSTNAME]}/v1/workflows",
        headers={
            "Content-Type": "application/json",
            ROLES_KEY: current_app.config[WORKFLOW_API_TOKEN],
        },
        json=request_json,
    )

    try:
        json_value = response.json()
        response.raise_for_status()

        workflow = OrganizationWorkflow(
            organization_uuid=organization_uuid,
            workflow_uuid=json_value.get("uuid"),
        )
        db.session.add(workflow)
        db.session.commit()

        json_value["uuid"] = workflow.uuid
        return json_value
    except ValueError as value_error:
        raise HTTPError("Non JSON payload returned") from value_error
    except HTTPError as http_error:
        raise ValueError(json_value) from http_error


def fetch_workflows(organization_uuid):
    """Fetch all Organization Workflows. """

    organization_workflows = find_organization_workflows(organization_uuid)

    response = requests.post(
        f"{current_app.config[WORKFLOW_HOSTNAME]}/v1/workflows/search",
        headers={
            "Content-Type": "application/json",
            ROLES_KEY: current_app.config[WORKFLOW_API_TOKEN],
        },
        json={"uuids": [op.workflow_uuid for op in organization_workflows]},
    )

    try:
        json_value = response.json()

        response.raise_for_status()
        valid_workflows = []

        for workflow in json_value:
            matching_workflows = []

            for org_w in organization_workflows:
                if org_w.workflow_uuid == workflow["uuid"]:
                    matching_workflows = [org_w.uuid]

            if len(matching_workflows) != 1:
                continue

            workflow["uuid"] = matching_workflows[0]
            valid_workflows.append(workflow)

        return valid_workflows
    except ValueError as value_error:
        raise HTTPError("Non JSON payload returned") from value_error
    except HTTPError as http_error:
        raise ValueError(json_value) from http_error


def fetch_workflow(organization_uuid, workflow_uuid):
    """Fetch a Organization Workflow. """

    organization_workflow = find_organization_workflow(organization_uuid, workflow_uuid)

    response = requests.get(
        f"{current_app.config[WORKFLOW_HOSTNAME]}/v1/workflows/{organization_workflow.workflow_uuid}",
        headers={
            "Content-Type": "application/json",
            ROLES_KEY: current_app.config[WORKFLOW_API_TOKEN],
        },
    )

    try:
        workflow = response.json()
        response.raise_for_status()

        return workflow

    except ValueError as value_error:
        raise HTTPError("Non JSON payload returned") from value_error
    except HTTPError as http_error:
        raise ValueError(workflow) from http_error


def update_workflow(organization_uuid, workflow_uuid, request_json):
    """Update an Organization Workflow. """

    organization_workflow = find_organization_workflow(organization_uuid, workflow_uuid)

    if not organization_workflow:
        raise ValueError("Organization Workflow not found.")

    if "name" not in request_json or "description" not in request_json:
        raise ValueError("Name and Description are required.")

    response = requests.put(
        f"{current_app.config[WORKFLOW_HOSTNAME]}/v1/workflows/{organization_workflow.workflow_uuid}",
        headers={
            "Content-Type": "application/json",
            ROLES_KEY: current_app.config[WORKFLOW_API_TOKEN],
        },
        json=request_json,
    )

    try:
        workflow = response.json()
        response.raise_for_status()

        return workflow

    except ValueError as value_error:
        raise HTTPError("Non JSON payload returned") from value_error
    except HTTPError as http_error:
        raise ValueError(json_value) from http_error
