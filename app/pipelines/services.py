import json
import logging
import urllib
import urllib.request
import uuid
from urllib.error import URLError
from blob_utils import upload_stream

from flask import current_app
from werkzeug.utils import secure_filename

from ..constants import CALLBACK_TIMEOUT, S3_BUCKET
from ..model_utils import RunStateEnum
from ..tasks import execute_pipeline
from .models import (
    Pipeline,
    PipelineRun,
    PipelineRunArtifact,
    PipelineRunInput,
    PipelineRunState,
    db,
)
from .queries import find_pipeline, find_pipeline_run, find_run_state_type
from .schemas import CreateRunSchema, UpdateRunStateSchema, CreatePipelineSchema

# make the request lib mockable for testing:
urllib_request = urllib.request

logger = logging.getLogger("services")


def delete_pipeline(pipeline_uuid):
    """ Delete a pipeline. """
    pipeline = find_pipeline(pipeline_uuid)
    if pipeline is None:
        raise ValueError("no pipeline found")

    from ..workflows.queries import pipeline_has_workflow_pipeline

    if pipeline_has_workflow_pipeline(pipeline.id):
        raise ValueError("pipeline has an associated workflow pipeline")

    pipeline.is_deleted = True
    db.session.commit()


def create_pipeline(pipeline_json):
    """Create a Pipeline.

    Note: The db.session is not committed. Be sure to commit the session.
    """
    data = CreatePipelineSchema().load(pipeline_json)

    pipeline = Pipeline(
        name=data["name"],
        description=data["description"],
        docker_image_url=data["docker_image_url"],
        repository_ssh_url=data["repository_ssh_url"],
        repository_branch=data["repository_branch"],
        repository_script=data["repository_script"],
    )
    db.session.add(pipeline)
    db.session.commit()

    return pipeline


def update_pipeline(pipeline_uuid, pipeline_json):
    """Update a Pipeline.

    Note: The db.session is not committed. Be sure to commit the session.
    """
    data = CreatePipelineSchema().load(pipeline_json)

    pipeline = find_pipeline(pipeline_uuid)
    if pipeline is None:
        raise ValueError("no pipeline found")

    pipeline.name = data["name"]
    pipeline.description = data["description"]
    pipeline.docker_image_url = data["docker_image_url"]
    pipeline.repository_ssh_url = data["repository_ssh_url"]
    pipeline.repository_branch = data["repository_branch"]
    pipeline.repository_script = data["repository_script"]
    db.session.add(pipeline)
    db.session.commit()

    return pipeline


def create_pipeline_run_state(run_state_enum):
    run_state_type = find_run_state_type(run_state_enum)
    pipeline_run_state = PipelineRunState(
        name=run_state_type.name,
        description=run_state_type.description,
        code=int(run_state_type.code),
    )
    run_state_type.pipeline_run_states.append(pipeline_run_state)

    return pipeline_run_state


def create_pipeline_run(pipeline_uuid, inputs_json, queued=False):
    """ Create a new PipelineRun for a Pipeline's uuid. """

    data = CreateRunSchema().load(inputs_json)

    pipeline = find_pipeline(pipeline_uuid)
    if pipeline is None:
        raise ValueError("no pipeline found")

    sequence = len(pipeline.pipeline_runs) + 1
    pipeline_run = PipelineRun(sequence=sequence, callback_url=data["callback_url"])

    for i in data["inputs"]:
        pipeline_run.pipeline_run_inputs.append(
            PipelineRunInput(filename=i["name"], url=i["url"])
        )

    pipeline_run.pipeline_run_states.append(
        create_pipeline_run_state(RunStateEnum.QUEUED)
    )
    pipeline.pipeline_runs.append(pipeline_run)

    if not queued:
        start_pipeline_run(pipeline_run)

    db.session.add(pipeline_run)
    db.session.commit()

    return pipeline_run


def start_pipeline_run(pipeline_run):
    """ Begin the Celery process for a PipelineRun """

    if pipeline_run.run_state_enum() != RunStateEnum.QUEUED:
        raise ValueError("Only PipelineRun in state QUEUED can be started.")

    pipeline = pipeline_run.pipeline
    pipeline_run.pipeline_run_states.append(
        create_pipeline_run_state(RunStateEnum.NOT_STARTED)
    )
    db.session.commit()

    execute_pipeline.delay(
        pipeline.uuid,
        pipeline_run.uuid,
        [
            {"name": pri.filename, "url": pri.url}
            for pri in pipeline_run.pipeline_run_inputs
        ],
        pipeline.docker_image_url,
        pipeline.repository_ssh_url,
        pipeline.repository_branch,
    )

    return pipeline_run


def update_pipeline_run_output(pipeline_uuid, std_out, std_err):
    """ Update the pipeline run output. """
    pipeline_run = find_pipeline_run(pipeline_uuid)
    if pipeline_run is None:
        raise ValueError("pipeline run not found")

    pipeline_run.std_out = std_out
    pipeline_run.std_err = std_err

    db.session.commit()


def notify_callback(pipeline_run):
    pipeline_uuid = pipeline_run.uuid
    url = pipeline_run.callback_url
    state = pipeline_run.pipeline_run_states[-1]

    data = json.dumps({"pipeline_run_uuid": pipeline_uuid, "state": state.name})

    request = urllib_request.Request(
        url, data.encode("ascii"), {"content-type": "application/json"}
    )
    try:
        urllib_request.urlopen(request, timeout=CALLBACK_TIMEOUT)
    except URLError as e:
        logger.warning(e)


def update_pipeline_run_state(
    pipeline_uuid, run_state_json, apply_to_workflow_run=True
):
    """Update the pipeline run state.

    This method ensures that no invalid state transitions occur.
    """
    data = UpdateRunStateSchema().load(run_state_json)

    pipeline_run = find_pipeline_run(pipeline_uuid)
    if pipeline_run is None:
        raise ValueError("pipeline run not found")

    if not pipeline_run.run_state_enum().is_valid_transition(data["state"]):
        raise ValueError(
            f"Invalid state transition: {pipeline_run.run_state_enum().name}->{data['state'].name}"
        )

    pipeline_run.pipeline_run_states.append(create_pipeline_run_state(data["state"]))

    db.session.commit()

    notify_callback(pipeline_run)

    if apply_to_workflow_run:
        from app.workflows.services import update_workflow_run

        update_workflow_run(pipeline_run)


def copy_pipeline_run_artifact(pipeline_run_artifact, to_pipeline_run):
    """ Copy an artifact to a new run as input. """
    to_pipeline_run.pipeline_run_inputs.append(
        PipelineRunInput(
            filename=pipeline_run_artifact.name, url=pipeline_run_artifact.public_url()
        )
    )
    db.session.commit()


def create_pipeline_run_artifact(run_uuid, filename, stream):
    """ Create a PipelineRunArtifact from a stream. """
    pipeline_run = find_pipeline_run(run_uuid)
    if pipeline_run is None:
        raise ValueError("pipeline run not found")

    sname = secure_filename(filename)
    artifact_uuid = uuid.uuid4().hex

    upload_stream(
        f"{pipeline_run.pipeline.uuid}/{run_uuid}/{artifact_uuid}-{sname}",
        stream,
    )

    artifact = PipelineRunArtifact(uuid=artifact_uuid, name=filename)
    pipeline_run.pipeline_run_artifacts.append(artifact)

    db.session.commit()

    return artifact
