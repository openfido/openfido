import uuid

import requests
from app.constants import WORKFLOW_API_TOKEN, WORKFLOW_HOSTNAME, S3_BUCKET
from application_roles.decorators import ROLES_KEY
from blob_utils import upload_stream, create_url
from flask import current_app
from requests import HTTPError

from .models import (
    OrganizationWorkflow,
    OrganizationWorkflowPipeline,
    OrganizationWorkflowPipelineRun,
    db,
)
from .queries import (
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

        for workflow in json_value:
            matching_workflows = []
            org_workflow = None

            for ow in organization_workflows:
                if ow.workflow_uuid == workflow["uuid"]:
                    matching_workflows = [ow.uuid]

            if len(matching_workflows) != 1:
                continue

            workflow["uuid"] = matching_workflows[0]

        return json_value
    except ValueError as value_error:
        raise HTTPError("Non JSON payload returned") from value_error
    except HTTPError as http_error:
        raise ValueError(json_value) from http_error