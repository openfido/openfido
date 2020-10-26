import requests
from app.constants import WORKFLOW_API_TOKEN, WORKFLOW_HOSTNAME
from application_roles.decorators import ROLES_KEY
from flask import current_app
from requests import HTTPError

from .models import OrganizationPipeline, db
from .queries import find_organization_pipeline, find_organization_pipelines


def create_pipeline(organization_uuid, request_json):
    """ Create a new pipeline associated with an organization. """
    response = requests.post(
        f"{current_app.config[WORKFLOW_HOSTNAME]}/v1/pipelines",
        headers={
            "Content-Type": "application/json",
            ROLES_KEY: current_app.config[WORKFLOW_API_TOKEN],
        },
        json=request_json,
    )

    try:
        json_value = response.json()
        response.raise_for_status()

        pipeline = OrganizationPipeline(
            organization_uuid=organization_uuid,
            pipeline_uuid=json_value["uuid"],
        )
        db.session.add(pipeline)
        db.session.commit()

        json_value["uuid"] = pipeline.uuid
        return json_value
    except ValueError as value_error:
        raise HTTPError("Non JSON payload returned") from value_error
    except HTTPError as http_error:
        raise ValueError(json_value) from http_error


def update_pipeline(organization_uuid, pipeline_uuid, request_json):
    """ Update a pipeline associated with an organization. """
    organization_pipeline = find_organization_pipeline(organization_uuid, pipeline_uuid)
    if not organization_pipeline:
        raise ValueError({"message": "organizational_pipeline_uuid not found"})

    response = requests.put(
        f"{current_app.config[WORKFLOW_HOSTNAME]}/v1/pipelines/{organization_pipeline.pipeline_uuid}",
        headers={
            "Content-Type": "application/json",
            ROLES_KEY: current_app.config[WORKFLOW_API_TOKEN],
        },
        json=request_json,
    )

    try:
        json_value = response.json()
        response.raise_for_status()

        json_value["uuid"] = organization_pipeline.uuid
        return json_value
    except ValueError as value_error:
        raise HTTPError("Non JSON payload returned") from value_error
    except HTTPError as http_error:
        raise ValueError(json_value) from http_error


def delete_pipeline(organization_uuid, organization_pipeline_uuid):
    """Delete a OrganizationPipeline.

    Note: assumes that the organization_uuid has already been verified (by
    validate_organization() mixin)

    Raises a an HTTPError when there is some unrecoverable downstream error.
    Raises a ValueError when there is some downstream error (its
    args[0] contains the json message from the backing server)
    """

    organization_pipeline = find_organization_pipeline(
        organization_uuid, organization_pipeline_uuid
    )
    if not organization_pipeline:
        raise ValueError({"message": "organizational_pipeline_uuid not found"})

    response = requests.delete(
        f"{current_app.config[WORKFLOW_HOSTNAME]}/v1/pipelines/{organization_pipeline.pipeline_uuid}",
        headers={
            "Content-Type": "application/json",
            ROLES_KEY: current_app.config[WORKFLOW_API_TOKEN],
        },
    )

    response.raise_for_status()

    organization_pipeline.is_deleted = True
    db.session.commit()


def fetch_pipelines(organization_uuid):
    """Find OrganizationPipelines for an organization.

    Note: assumes that the organization_uuid has already been verified (by
    validate_organization() mixin)

    Raises a an HTTPError when there is some unrecoverable downstream error.
    Raises a ValueError when there is some downstream error (its
    args[0] contains the json message from the backing server)
    """

    organization_pipelines = find_organization_pipelines(organization_uuid)

    # TODO timeouts - enforce a strict timeout.
    response = requests.post(
        f"{current_app.config[WORKFLOW_HOSTNAME]}/v1/pipelines/search",
        headers={
            "Content-Type": "application/json",
            ROLES_KEY: current_app.config[WORKFLOW_API_TOKEN],
        },
        json={"uuids": [op.pipeline_uuid for op in organization_pipelines]},
    )

    try:
        json_value = response.json()
        response.raise_for_status()

        for pipeline in json_value:
            matching_pipelines = [
                op.uuid
                for op in organization_pipelines
                if op.pipeline_uuid == pipeline["uuid"]
            ]
            if len(matching_pipelines) != 1:
                raise ValueError("Unexpected response from workflow service")
            pipeline["uuid"] = matching_pipelines[0]
        return json_value
    except ValueError as value_error:
        raise HTTPError("Non JSON payload returned") from value_error
    except HTTPError as http_error:
        raise ValueError(json_value) from http_error
