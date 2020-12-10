import requests

from flask import current_app
from requests import HTTPError

from application_roles.decorators import ROLES_KEY
from app.constants import WORKFLOW_API_TOKEN, WORKFLOW_HOSTNAME

from app.pipelines.models import OrganizationPipeline
from app.workflows.models import (
    OrganizationWorkflow,
    OrganizationWorkflowPipeline,
    db,
)
from app.pipelines.queries import (
    find_organization_pipeline,
    find_organization_pipeline_by_id,
    find_organization_pipelines,
)
from app.workflows.queries import (
    find_organization_workflow,
    find_organization_workflows,
    find_organization_workflow_pipeline,
    find_organization_workflow_pipelines,
)

from .schemas import CreateWorkflowPipelineSchema


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


def fetch_workflow(organization_uuid, organization_workflow_uuid):
    """Fetch a Organization Workflow. """

    organization_workflow = find_organization_workflow(
        organization_uuid, organization_workflow_uuid
    )

    if not organization_workflow:
        raise ValueError("Organization Workflow not found.")

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

        workflow["uuid"] = organization_workflow_uuid
        return workflow

    except ValueError as value_error:
        raise HTTPError("Non JSON payload returned") from value_error
    except HTTPError as http_error:
        raise ValueError(workflow) from http_error


def update_workflow(organization_uuid, organization_workflow_uuid, request_json):
    """Update an Organization Workflow. """

    organization_workflow = find_organization_workflow(
        organization_uuid, organization_workflow_uuid
    )

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

        workflow["uuid"] = organization_workflow.uuid

        return workflow

    except ValueError as value_error:
        raise HTTPError("Non JSON payload returned") from value_error
    except HTTPError as http_error:
        raise ValueError(workflow) from http_error


def delete_workflow(organization_uuid, organization_workflow_uuid):
    """Delete an Organization Workflow. """

    organization_workflow = find_organization_workflow(
        organization_uuid, organization_workflow_uuid
    )

    if not organization_workflow:
        raise ValueError("Organization Workflow not found.")

    response = requests.delete(
        f"{current_app.config[WORKFLOW_HOSTNAME]}/v1/workflows/{organization_workflow.workflow_uuid}",
        headers={
            "Content-Type": "application/json",
            ROLES_KEY: current_app.config[WORKFLOW_API_TOKEN],
        },
    )

    response.raise_for_status()

    organization_workflow.is_deleted = True
    db.session.commit()


def create_workflow_pipeline(
    organization_uuid, organization_workflow_uuid, request_json
):
    """Creates an Organization Workflow Pipeline."""

    data = CreateWorkflowPipelineSchema().load(request_json)

    organization_workflow = find_organization_workflow(
        organization_uuid, organization_workflow_uuid
    )

    if not organization_workflow:
        raise ValueError("Organization Workflow not found.")

    org_pipeline = find_organization_pipeline(
        organization_uuid, data.get("pipeline_uuid")
    )

    if not org_pipeline:
        raise ValueError("Organization Pipeline not found.")

    associated_org_workflow_pipelines = find_organization_workflow_pipelines(
        organization_workflow_uuid, org_pipeline.id
    )

    org_workflow_pipelines = {
        ow_p.uuid: ow_p.workflow_pipeline_uuid
        for ow_p in associated_org_workflow_pipelines
    }

    # org workflow pipelines
    src_org_workflow_pipelines = data.get("source_workflow_pipelines", [])
    dest_org_workflow_pipelines = data.get("destination_workflow_pipelines", [])

    # workflow pipelines
    if len(set(src_org_workflow_pipelines) - set(org_workflow_pipelines)) > 0:
        raise ValueError("Invalid UUIDs provided to source_workflow_pipelines")
    src_workflow_pipelines = [
        org_workflow_pipelines[sp_uuid] for sp_uuid in src_org_workflow_pipelines
    ]
    if len(set(dest_org_workflow_pipelines) - set(org_workflow_pipelines)) > 0:
        raise ValueError("Invalid UUIDs provided to destination_workflow_pipelines")
    dest_workflow_pipelines = [
        org_workflow_pipelines[dp_uuid] for dp_uuid in dest_org_workflow_pipelines
    ]

    response = requests.post(
        f"{current_app.config[WORKFLOW_HOSTNAME]}/v1/workflows/{organization_workflow.workflow_uuid}/pipelines",
        headers={
            "Content-Type": "application/json",
            ROLES_KEY: current_app.config[WORKFLOW_API_TOKEN],
        },
        json={
            "pipeline_uuid": org_pipeline.pipeline_uuid,
            "source_workflow_pipelines": src_workflow_pipelines,
            "destination_workflow_pipelines": dest_workflow_pipelines,
        },
    )

    try:
        json_value = response.json()

        response.raise_for_status()

        new_org_workflow_pipeline = OrganizationWorkflowPipeline(
            organization_workflow_uuid=organization_workflow_uuid,
            organization_pipeline_id=org_pipeline.id,
            workflow_pipeline_uuid=json_value.get("uuid"),
        )

        db.session.add(new_org_workflow_pipeline)
        db.session.commit()

        json_value["uuid"] = new_org_workflow_pipeline.uuid
        json_value["pipeline_uuid"] = org_pipeline.uuid
        json_value["source_workflow_pipelines"] = src_org_workflow_pipelines
        json_value["destination_workflow_pipelines"] = dest_org_workflow_pipelines

        return json_value
    except ValueError as value_error:
        raise HTTPError("Non JSON payload returned") from value_error
    except HTTPError as http_error:
        raise ValueError(json_value) from http_error


def fetch_workflow_pipelines(organization_uuid, organization_workflow_uuid):
    """Fetches all Organization Workflow Pipelines."""

    organization_workflow = find_organization_workflow(
        organization_uuid, organization_workflow_uuid
    )

    if not organization_workflow:
        raise ValueError("Organization Workflow not found.")

    response = requests.get(
        f"{current_app.config[WORKFLOW_HOSTNAME]}/v1/workflows/{organization_workflow.workflow_uuid}/pipelines",
        headers={
            "Content-Type": "application/json",
            ROLES_KEY: current_app.config[WORKFLOW_API_TOKEN],
        },
    )

    try:
        json_value = response.json()

        response.raise_for_status()
        valid_workflows = []

        # map workflow pipelines to org pipeline ids and uuids
        org_pipelines = {
            o_p.pipeline_uuid: (
                o_p.id,
                o_p.uuid,
            )
            for o_p in find_organization_pipelines(organization_uuid)
        }

        for workflow in json_value:
            org_pipeline_id, org_pipeline_uuid = org_pipelines[
                workflow["pipeline_uuid"]
            ]

            # map workflow pipelines to org workflow pipeline uuids
            associated_org_workflow_pipelines = find_organization_workflow_pipelines(
                organization_workflow_uuid, org_pipeline_id
            )

            org_workflow_pipelines = {
                ow_p.workflow_pipeline_uuid: ow_p.uuid
                for ow_p in associated_org_workflow_pipelines
            }

            workflow["uuid"] = org_workflow_pipelines[workflow["uuid"]]
            workflow["pipeline_uuid"] = org_pipeline_uuid

            for key in ["source_workflow_pipelines", "destination_workflow_pipelines"]:
                workflow[key] = [org_workflow_pipelines[uuid] for uuid in workflow[key]]

        return json_value
    except ValueError as value_error:
        raise HTTPError("Non JSON payload returned") from value_error
    except HTTPError as http_error:
        raise ValueError(json_value) from http_error


def fetch_workflow_pipeline(
    organization_uuid, organization_workflow_uuid, organization_workflow_pipeline_uuid
):
    """Fetches an Organization Workflow Pipeline."""
    organization_workflow_pipeline = find_organization_workflow_pipeline(
        organization_workflow_uuid, organization_workflow_pipeline_uuid
    )

    if not organization_workflow_pipeline:
        raise ValueError("Organization Workflow Pipeline not found.")

    organization_workflow = organization_workflow_pipeline.organization_workflow

    if not organization_workflow:
        raise ValueError("Organization Workflow not found.")

    w_uuid = organization_workflow.workflow_uuid
    wp_uuid = organization_workflow_pipeline.workflow_pipeline_uuid

    response = requests.get(
        f"{current_app.config[WORKFLOW_HOSTNAME]}/v1/workflows/{w_uuid}/pipelines/{wp_uuid}",
        headers={
            "Content-Type": "application/json",
            ROLES_KEY: current_app.config[WORKFLOW_API_TOKEN],
        },
    )

    try:
        workflow = response.json()
        response.raise_for_status()

        org_pipeline = find_organization_pipeline_by_id(
            organization_workflow_pipeline.organization_pipeline_id
        )

        org_workflow_pipelines = {
            ow_p.workflow_pipeline_uuid: ow_p.uuid
            for ow_p in org_pipeline.organization_workflow_pipelines
        }

        workflow["uuid"] = org_workflow_pipelines[workflow["uuid"]]
        workflow["pipeline_uuid"] = org_pipeline.uuid

        for key in ["source_workflow_pipelines", "destination_workflow_pipelines"]:
            workflow[key] = [org_workflow_pipelines[uuid] for uuid in workflow[key]]

        return workflow
    except ValueError as value_error:
        raise HTTPError("Non JSON payload returned") from value_error
    except HTTPError as http_error:
        raise ValueError(workflow) from http_error


def update_workflow_pipeline(
    organization_uuid,
    organization_workflow_uuid,
    organization_workflow_pipeline_uuid,
    request_json,
):
    """Updates an Organization Workflow Pipeline. """

    data = CreateWorkflowPipelineSchema().load(request_json)

    organization_workflow = find_organization_workflow(
        organization_uuid, organization_workflow_uuid
    )

    if not organization_workflow:
        raise ValueError("Organization Workflow not found.")

    org_pipeline = find_organization_pipeline(
        organization_uuid, data.get("pipeline_uuid")
    )

    if not org_pipeline:
        raise ValueError("Organization Pipeline not found.")

    # fetch all org workflow pipelines for target pipeline and assoc piplines.
    associated_org_workflow_pipelines = find_organization_workflow_pipelines(
        organization_workflow_uuid, org_pipeline.id
    )

    org_workflow_pipelines = {
        ow_p.uuid: ow_p.workflow_pipeline_uuid
        for ow_p in associated_org_workflow_pipelines
    }

    if organization_workflow_pipeline_uuid not in org_workflow_pipelines:
        raise ValueError("Organization Workflow Pipeline not found.")

    # org workflow pipelines
    src_org_workflow_pipelines = data.get("source_workflow_pipelines", [])
    dest_org_workflow_pipelines = data.get("destination_workflow_pipelines", [])

    # workflow pipelines
    src_workflow_pipelines = [
        org_workflow_pipelines[sp_uuid] for sp_uuid in src_org_workflow_pipelines
    ]
    dest_workflow_pipelines = [
        org_workflow_pipelines[dp_uuid] for dp_uuid in dest_org_workflow_pipelines
    ]

    w_uuid = organization_workflow.workflow_uuid
    wp_uuid = org_workflow_pipelines[organization_workflow_pipeline_uuid]

    response = requests.put(
        f"{current_app.config[WORKFLOW_HOSTNAME]}/v1/workflows/{w_uuid}/pipelines/{wp_uuid}",
        headers={
            "Content-Type": "application/json",
            ROLES_KEY: current_app.config[WORKFLOW_API_TOKEN],
        },
        json={
            "pipeline_uuid": org_pipeline.pipeline_uuid,
            "source_workflow_pipelines": src_workflow_pipelines,
            "dest_workflow_pipelines": dest_workflow_pipelines,
        },
    )

    try:
        json_value = response.json()
        response.raise_for_status()

        json_value["uuid"] = organization_workflow_pipeline_uuid
        json_value["pipeline_uuid"] = org_pipeline.uuid
        json_value["source_workflow_pipelines"] = src_org_workflow_pipelines
        json_value["destination_workflow_pipelines"] = dest_org_workflow_pipelines

        return json_value
    except ValueError as value_error:
        raise HTTPError("Non JSON payload returned") from value_error
    except HTTPError as http_error:
        raise ValueError(json_value) from http_error


def delete_workflow_pipeline(
    organization_uuid, organization_workflow_uuid, organization_workflow_pipeline_uuid
):
    """Deletes an Organization Workflow Pipeline. """

    organization_workflow_pipeline = find_organization_workflow_pipeline(
        organization_workflow_uuid, organization_workflow_pipeline_uuid
    )

    if not organization_workflow_pipeline:
        raise ValueError("Organization Workflow Pipeline not found.")

    organization_workflow = organization_workflow_pipeline.organization_workflow

    w_uuid = organization_workflow.workflow_uuid
    wp_uuid = organization_workflow_pipeline.workflow_pipeline_uuid

    response = requests.delete(
        f"{current_app.config[WORKFLOW_HOSTNAME]}/v1/workflows/{w_uuid}/pipelines/{wp_uuid}",
        headers={
            "Content-Type": "application/json",
            ROLES_KEY: current_app.config[WORKFLOW_API_TOKEN],
        },
    )

    response.raise_for_status()

    organization_workflow_pipeline.is_deleted = True

    db.session.commit()
