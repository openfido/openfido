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