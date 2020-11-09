import uuid
from datetime import datetime
from datetime import timedelta

import requests
from app.constants import WORKFLOW_API_TOKEN, WORKFLOW_HOSTNAME, S3_BUCKET
from application_roles.decorators import ROLES_KEY
from blob_utils import upload_stream, create_url
from flask import current_app
from requests import HTTPError
from werkzeug.utils import secure_filename

from .models import (
    OrganizationPipeline,
    OrganizationPipelineInputFile,
    OrganizationPipelineRun,
    db,
)
from .queries import (
    find_organization_pipeline,
    find_organization_pipelines,
    find_organization_pipeline_input_files,
    find_organization_pipeline_run,
    find_latest_organization_pipeline_run,
    search_organization_pipeline_input_files,
    search_organization_pipeline_runs,
)
from ..utils import make_hash


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
            pipeline_uuid=json_value.get("uuid"),
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
            matching_pipelines = []
            org_pipeline = None

            for op in organization_pipelines:
                if op.pipeline_uuid == pipeline["uuid"]:
                    matching_pipelines = [op.uuid]
                    org_pipeline_id = op.id

            if len(matching_pipelines) != 1:
                continue

            pipeline["uuid"] = matching_pipelines[0]
            latest_pipeline_run = find_latest_organization_pipeline_run(org_pipeline_id)

            if latest_pipeline_run:
                pipeline_run = fetch_pipeline_run(
                    organization_uuid, pipeline["uuid"], latest_pipeline_run.uuid
                )

                if pipeline_run:
                    pipeline["last_pipeline_run"] = pipeline_run

        return json_value
    except ValueError as value_error:
        raise HTTPError("Non JSON payload returned") from value_error
    except HTTPError as http_error:
        raise ValueError(json_value) from http_error


def create_pipeline_input_file(organization_pipeline, filename, stream):
    """ Create a OrganizationPipelineInputFile from a stream. """
    if len(filename) < 2:
        raise ValueError("filename too short")
    if len(filename) > OrganizationPipelineInputFile.name.type.length:
        raise ValueError("filename too long")

    sname = secure_filename(filename)
    input_file_uuid = uuid.uuid4().hex
    upload_stream(
        f"{organization_pipeline.uuid}/{input_file_uuid}-{sname}",
        stream,
    )

    input_file = OrganizationPipelineInputFile(uuid=input_file_uuid, name=filename)
    organization_pipeline.organization_pipeline_input_files.append(input_file)

    db.session.commit()

    return input_file


def create_pipeline_run(organization_uuid, pipeline_uuid, request_json):
    """Creates OrganizationPipelineRuns for a pipline."""
    org_pipeline = find_organization_pipeline(organization_uuid, pipeline_uuid)

    if not org_pipeline:
        raise ValueError({"message": "organizational_pipeline_uuid not found"})

    org_pipeline_input_files = search_organization_pipeline_input_files(
        org_pipeline.id, request_json.get("inputs", [])
    )

    new_pipeline_run = OrganizationPipelineRun(
        organization_pipeline_id=org_pipeline.id,
        status_update_token=uuid.uuid4().hex,
        status_update_token_expires_at=datetime.now() + timedelta(days=7),
        share_token=uuid.uuid4().hex,
        share_password_hash=None,
        share_password_salt=None,
    )

    db.session.add(new_pipeline_run)
    db.session.flush()

    new_pipeline = {"inputs": []}

    for opf in org_pipeline_input_files:
        sname = secure_filename(opf.name)
        url = create_url(f"{pipeline_uuid}/{opf.uuid}-{sname}")
        new_pipeline["inputs"].append({"url": url, "name": opf.name})

    response = requests.post(
        f"{current_app.config[WORKFLOW_HOSTNAME]}/v1/pipelines/{org_pipeline.pipeline_uuid}/runs",
        headers={
            "Content-Type": "application/json",
            ROLES_KEY: current_app.config[WORKFLOW_API_TOKEN],
        },
        json=new_pipeline,
    )

    try:
        created_pipeline = response.json()
        response.raise_for_status()

        new_pipeline_run.uuid = (
            new_pipeline_run.pipeline_run_uuid
        ) = created_pipeline.get("uuid")
        db.session.commit()

        created_pipeline.update(
            {
                "uuid": new_pipeline_run.uuid,
            }
        )

        return created_pipeline
    except ValueError as value_error:
        raise HTTPError("Non JSON payload returned") from value_error
    except HTTPError as http_error:
        raise ValueError(created_pipeline) from http_error


def fetch_pipeline_runs(organization_uuid, pipeline_uuid):
    """Find all OrganizationPipelineRuns for a pipline."""
    org_pipeline = find_organization_pipeline(organization_uuid, pipeline_uuid)

    response = requests.get(
        f"{current_app.config[WORKFLOW_HOSTNAME]}/v1/pipelines/{org_pipeline.pipeline_uuid}/runs",
        headers={
            "Content-Type": "application/json",
            ROLES_KEY: current_app.config[WORKFLOW_API_TOKEN],
        },
    )

    try:
        pipeline_runs = response.json()
        response.raise_for_status()

        # update with org uuids
        for pr in pipeline_runs:
            opr = search_organization_pipeline_runs(org_pipeline.id, [pr.get("uuid")])[
                0
            ]
            pr["uuid"] = opr.uuid
            org_pipeline_input_files = find_organization_pipeline_input_files(
                org_pipeline.id
            )
            inputs = []

            # generate download urls and add uuid
            for opf in org_pipeline_input_files:
                sname = secure_filename(opf.name)
                url = create_url(f"{pipeline_uuid}/{opf.uuid}-{sname}")
                inputs.append({"url": url, "name": opf.name, "uuid": opf.uuid})

            pr["inputs"] = inputs

        return pipeline_runs
    except ValueError as value_error:
        raise HTTPError("Non JSON payload returned") from value_error
    except HTTPError as http_error:
        raise ValueError(pipeline_runs) from http_error


def fetch_pipeline_run(
    organization_uuid, organization_pipeline_uuid, organization_pipeline_run_uuid
):
    """Find an OrganizationPipelineRun for a pipline."""
    org_pipeline = find_organization_pipeline(
        organization_uuid, organization_pipeline_uuid
    )

    org_pipeline_run = next(
        filter(
            lambda r: r.uuid == organization_pipeline_run_uuid,
            org_pipeline.organization_pipeline_runs,
        )
    )

    response = requests.get(
        f"{current_app.config[WORKFLOW_HOSTNAME]}/v1/pipelines/{org_pipeline.pipeline_uuid}/runs/{org_pipeline_run.pipeline_run_uuid}",
        headers={
            "Content-Type": "application/json",
            ROLES_KEY: current_app.config[WORKFLOW_API_TOKEN],
        },
    )

    try:
        pipeline_run = response.json()
        response.raise_for_status()

        # update with org uuid
        opr = find_organization_pipeline_run(
            org_pipeline.id, str(pipeline_run.get("uuid"))
        )
        pipeline_run["uuid"] = opr.uuid
        org_pipeline_input_files = find_organization_pipeline_input_files(
            org_pipeline.id
        )
        inputs = []

        # generate download urls and add uuid
        for opf in org_pipeline_input_files:
            sname = secure_filename(opf.name)
            url = create_url(f"{organization_pipeline_uuid}/{opf.uuid}-{sname}")
            inputs.append({"url": url, "name": opf.name, "uuid": opf.uuid})

        pipeline_run["inputs"] = inputs

        return pipeline_run
    except ValueError as value_error:
        raise HTTPError("Non JSON payload returned") from value_error
    except HTTPError as http_error:
        raise ValueError(pipeline_run) from http_error


def fetch_pipeline_run_console(
    organization_uuid, organization_pipeline_uuid, organization_pipeline_run_uuid
):
    """Fetches console output for an OrganizationPipelineRun."""
    org_pipeline = find_organization_pipeline(
        organization_uuid, organization_pipeline_uuid
    )

    org_pipeline_run = next(
        filter(
            lambda r: r.uuid == organization_pipeline_run_uuid,
            org_pipeline.organization_pipeline_runs,
        )
    )

    response = requests.get(
        f"{current_app.config[WORKFLOW_HOSTNAME]}/v1/pipelines/{org_pipeline.pipeline_uuid}/runs/{org_pipeline_run.pipeline_run_uuid}/console",
        headers={
            "Content-Type": "application/json",
            ROLES_KEY: current_app.config[WORKFLOW_API_TOKEN],
        },
    )

    try:
        console_output = response.json()
        response.raise_for_status()

        return console_output
    except ValueError as value_error:
        raise HTTPError("Non JSON payload returned") from value_error
    except HTTPError as http_error:
        raise ValueError(console_output) from http_error
