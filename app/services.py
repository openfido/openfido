import json
import logging
import os
import urllib.request
import uuid
from urllib.error import URLError

import boto3
from botocore.client import Config
from flask import current_app
from marshmallow.exceptions import ValidationError
from werkzeug.utils import secure_filename

from .constants import BLOB_API_SERVER, BLOB_API_TOKEN
from .models import (
    Pipeline, PipelineRun, PipelineRunArtifact, PipelineRunInput, PipelineRunState, RunStateEnum,
    db)
from .queries import find_pipeline, find_pipeline_run, find_run_state_type
from .schemas import CreateRunSchema, UpdateRunStateSchema
from .tasks import execute_pipeline

# TODO make this configurable
s3 = boto3.client(
    "s3",
    endpoint_url="http://storage:9000",
    aws_access_key_id="AKIAIOSFODNN7EXAMPLE",
    aws_secret_access_key="wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY",
    config=Config(signature_version="s3v4"),
    region_name="us-east-1",
)

# make the request lib mockable for testing:
urllib_request = urllib.request

CALLBACK_TIMEOUT = 100

logger = logging.getLogger("services")


def delete_pipeline(uuid):
    """Delete a pipeline.

    Note: The db.session is not committed. Be sure to commit the session.
    """
    pipeline = find_pipeline(uuid)
    if pipeline is None:
        raise ValueError("no pipeline found")

    pipeline.is_deleted = True


def _validate_pipeline_params(
    name, description, docker_image_url, repository_ssh_url, repository_branch
):
    if len(name) == 0 or len(description) == 0:
        raise ValueError("name and description must be supplied.")
    if len(docker_image_url) == 0:
        raise ValueError("A docker image URL must be supplied.")
    if len(repository_ssh_url) == 0 or len(repository_branch) == 0:
        raise ValueError("A ssh URL must be supplied.")


def create_pipeline(
    name, description, docker_image_url, repository_ssh_url, repository_branch
):
    """Create a Pipeline.

    Note: The db.session is not committed. Be sure to commit the session.
    """
    _validate_pipeline_params(
        name, description, docker_image_url, repository_ssh_url, repository_branch
    )

    pipeline = Pipeline(
        name=name,
        description=description,
        docker_image_url=docker_image_url,
        repository_ssh_url=repository_ssh_url,
        repository_branch=repository_branch,
    )
    db.session.add(pipeline)

    return pipeline


def update_pipeline(
    uuid, name, description, docker_image_url, repository_ssh_url, repository_branch
):
    """Update a Pipeline.

    Note: The db.session is not committed. Be sure to commit the session.
    """
    _validate_pipeline_params(
        name, description, docker_image_url, repository_ssh_url, repository_branch
    )
    pipeline = find_pipeline(uuid)
    if pipeline is None:
        raise ValueError("no pipeline found")

    pipeline.name = name
    pipeline.description = description
    pipeline.docker_image_url = docker_image_url
    pipeline.repository_ssh_url = repository_ssh_url
    pipeline.repository_branch = repository_branch
    db.session.add(pipeline)

    return pipeline


def create_pipeline_run_state(run_state):
    run_state_type = find_run_state_type(run_state)
    pipeline_run_state = PipelineRunState(
        name=run_state_type.name,
        description=run_state_type.description,
        code=run_state_type.code,
    )
    run_state_type.pipeline_run_states.append(pipeline_run_state)

    return pipeline_run_state


def create_pipeline_run(uuid, inputs_json):
    """ Create a new PipelineRun for a Pipeline's uuid """
    CreateRunSchema().load(inputs_json)

    pipeline = find_pipeline(uuid)
    if pipeline is None:
        raise ValueError("no pipeline found")

    sequence = len(pipeline.pipeline_runs) + 1
    pipeline_run = PipelineRun(
        sequence=sequence, callback_url=inputs_json["callback_url"]
    )

    for i in inputs_json["inputs"]:
        pipeline_run.pipeline_run_inputs.append(
            PipelineRunInput(filename=i["name"], url=i["url"])
        )

    pipeline_run.pipeline_run_states.append(
        create_pipeline_run_state(RunStateEnum.NOT_STARTED)
    )
    pipeline.pipeline_runs.append(pipeline_run)
    db.session.add(pipeline)

    db.session.commit()

    execute_pipeline.delay(
        uuid,
        pipeline_run.uuid,
        inputs_json["inputs"],
        pipeline.docker_image_url,
        pipeline.repository_ssh_url,
        pipeline.repository_branch,
    )

    return pipeline_run


def update_pipeline_run_output(uuid, std_out, std_err):
    """ Update the pipeline run output. """
    pipeline_run = find_pipeline_run(uuid)
    if pipeline_run is None:
        raise ValueError("pipeline run not found")

    pipeline_run.std_out = std_out
    pipeline_run.std_err = std_err

    db.session.commit()


def notify_callback(pipeline_run):
    uuid = pipeline_run.uuid
    url = pipeline_run.callback_url
    state = pipeline_run.pipeline_run_states[-1]

    data = json.dumps({"pipeline_run_uuid": uuid, "state": state.name})

    request = urllib_request.Request(
        url, data.encode("ascii"), {"content-type": "application/json"}
    )
    try:
        urllib_request.urlopen(request, timeout=CALLBACK_TIMEOUT)
    except URLError as e:
        logger.warning(e)


def update_pipeline_run_state(uuid, run_state_json):
    """Update the pipeline run state.

    This method ensures that no invalid state transitions occur.
    """
    schema = UpdateRunStateSchema()
    data = schema.load(run_state_json)

    pipeline_run = find_pipeline_run(uuid)
    if pipeline_run is None:
        raise ValueError("pipeline run not found")

    last_run_state = pipeline_run.pipeline_run_states[-1]
    if not RunStateEnum(last_run_state.code).is_valid_transition(data["state"]):
        raise ValueError("Invalid state transition")

    pipeline_run.pipeline_run_states.append(create_pipeline_run_state(data["state"]))

    db.session.commit()

    notify_callback(pipeline_run)


def create_pipeline_run_artifact(run_uuid, filename, request):
    pipeline_run = find_pipeline_run(run_uuid)
    if pipeline_run is None:
        raise ValueError("pipeline run not found")

    sname = secure_filename(filename)
    artifact_uuid = uuid.uuid4().hex
    if "artifacts" not in [b["Name"] for b in s3.list_buckets()["Buckets"]]:
        s3.Bucket("artifacts").create()
    s3.upload_fileobj(request.stream, "artifacts", f"{artifact_uuid}-{sname}")

    artifact = PipelineRunArtifact(uuid=artifact_uuid, name=filename)
    pipeline_run.pipeline_run_artifacts.append(artifact)

    db.session.commit()
