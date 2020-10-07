import jwt
import requests
from app.constants import WORKFLOW_API_TOKEN, WORKFLOW_HOSTNAME
from application_roles.decorators import ROLES_KEY
from flask import current_app

from .queries import find_organization_pipelines


def fetch_pipelines(organization_uuid):
    """Verify that user is a member of AUTH_HOSTNAME

    Note: assumes that the organization_uuid has already been verified (by
    validate_organization() mixin)
    """

    organization_pipelines = find_organization_pipelines(organization_uuid)

    # TODO timeouts
    response = requests.post(
        f"{current_app.config[WORKFLOW_HOSTNAME]}/v1/pipelines/search",
        headers={
            "Content-Type": "application/json",
            ROLES_KEY: current_app.config[WORKFLOW_API_TOKEN],
        },
        json={"uuids": [op.pipeline_uuid for op in organization_pipelines]},
    )
    response.raise_for_status()

    return response.json()
