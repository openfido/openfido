import logging

from flask import Blueprint, jsonify, request
from requests import HTTPError

from app.utils import validate_organization, any_application_required

from .services import (
    fetch_pipelines,
    create_pipeline,
    update_pipeline,
    delete_pipeline,
    create_pipeline_input_file,
    fetch_pipeline_run,
    fetch_pipeline_runs,
    create_pipeline_run,
    fetch_pipeline_run_console,
)

from .queries import find_organization_pipeline

logger = logging.getLogger("organization-pipelines")

organization_pipeline_bp = Blueprint("organization-pipelines", __name__)


@organization_pipeline_bp.route("/<organization_uuid>/pipelines", methods=["POST"])
@any_application_required
@validate_organization()
def create(organization_uuid):
    """Create a Organization Pipeline.
    ---
    tags:
      - pipelines
    parameters:
      - in: header
        name: Workflow-API-Key
        description: Requires key type REACT_CLIENT
        schema:
          type: string
    requestBody:
      description: "Pipeline description and configuration."
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              name:
                type: string
              description:
                type: string
              docker_image_url:
                type: string
              repository_ssh_url:
                type: string
              repository_branch:
                type: string
    responses:
      "200":
        description: "Updated OrganizationPipeline"
        content:
          application/json:
            schema:
              type: object
              properties:
                uuid:
                  type: string
                name:
                  type: string
                description:
                  type: string
                docker_image_url:
                  type: string
                repository_ssh_url:
                  type: string
                repository_branch:
                  type: string
                created_at:
                  type: string
                updated_at:
                  type: string
      "400":
        description: "Bad request"
    """
    try:
        return jsonify(create_pipeline(organization_uuid, request.json))
    except ValueError as value_error:
        return jsonify(value_error.args[0]), 400
    except HTTPError as http_error:
        return {"message": http_error.args[0]}, 503


@organization_pipeline_bp.route(
    "/<organization_uuid>/pipelines/<organization_pipeline_uuid>", methods=["PUT"]
)
@any_application_required
@validate_organization()
def update(organization_uuid, organization_pipeline_uuid):
    """Update Organization Pipeline.
    ---
    tags:
      - pipelines
    parameters:
      - in: header
        name: Workflow-API-Key
        description: Requires key type REACT_CLIENT
        schema:
          type: string
    requestBody:
      description: "Pipeline description and corganization_pipeline_uuid"
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              name:
                type: string
              description:
                type: string
              docker_image_url:
                type: string
              repository_ssh_url:
                type: string
              repository_branch:
                type: string
    responses:
      "200":
        description: "Updated OrganizationPipeline"
        content:
          application/json:
            schema:
              type: object
              properties:
                uuid:
                  type: string
                name:
                  type: string
                description:
                  type: string
                docker_image_url:
                  type: string
                repository_ssh_url:
                  type: string
                repository_branch:
                  type: string
                created_at:
                  type: string
                updated_at:
                  type: string
      "400":
        description: "Bad request"
    """
    try:
        return jsonify(
            update_pipeline(organization_uuid, organization_pipeline_uuid, request.json)
        )
    except ValueError as value_error:
        return jsonify(value_error.args[0]), 400
    except HTTPError as http_error:
        return {"message": http_error.args[0]}, 503


@organization_pipeline_bp.route(
    "/<organization_uuid>/pipelines/<organization_pipeline_uuid>", methods=["DELETE"]
)
@any_application_required
@validate_organization(False)
def remove(organization_uuid, organization_pipeline_uuid):
    """Delete a Organization Pipeline.
    ---
    tags:
      - pipelines
    parameters:
      - in: header
        name: Workflow-API-Key
        description: Requires key type REACT_CLIENT
        schema:
          type: string
    responses:
      "200":
        description: "Deleted OrganizationPipeline"
      "400":
        description: "Bad request"
    """
    try:
        delete_pipeline(organization_uuid, organization_pipeline_uuid)
        return {}, 200
    except ValueError as value_error:
        return jsonify(value_error.args[0]), 400
    except HTTPError as http_error:
        return {"message": http_error.args[0]}, 503


@organization_pipeline_bp.route("/<organization_uuid>/pipelines", methods=["GET"])
@any_application_required
@validate_organization(False)
def pipelines(organization_uuid):
    """List all Organization Pipelines.
    ---
    tags:
      - pipelines
    parameters:
      - in: header
        name: Workflow-API-Key
        description: Requires key type REACT_CLIENT
        schema:
          type: string
    responses:
      "200":
        description: "List of pipelines"
        content:
          application/json:
            schema:
              type: array
              items:
                type: object
                properties:
                  uuid:
                    type: string
                  name:
                    type: string
                  description:
                    type: string
                  docker_image_url:
                    type: string
                  repository_ssh_url:
                    type: string
                  repository_branch:
                    type: string
                  created_at:
                    type: string
                  updated_at:
                    type: string
      "400":
        description: "Bad request"
    """
    try:
        return jsonify(fetch_pipelines(organization_uuid))
    except ValueError as value_error:
        return jsonify(value_error.args[0]), 400
    except HTTPError as http_error:
        return {"message": http_error.args[0]}, 503


@organization_pipeline_bp.route(
    "/<organization_uuid>/pipelines/<organization_pipeline_uuid>/input_files",
    methods=["POST"],
)
@any_application_required
@validate_organization(False)
def upload_input_file(organization_uuid, organization_pipeline_uuid):
    """Upload a file that will be used as an input to a PipelineRun.
    ---
    tags:
      - pipelines
    parameters:
      - in: header
        name: Workflow-API-Key
        description: Requires key type REACT_CLIENT
        schema:
          type: string
      - in: query
        name: name
        schema:
          type: string
    responses:
      "200":
        description: "OK"
        content:
          application/json:
            schema:
              type: object
              properties:
                uuid:
                  type: string
                name:
                  type: string
      "400":
        description: "Bad request"
    """
    organization_pipeline = find_organization_pipeline(
        organization_uuid, organization_pipeline_uuid
    )
    if not organization_pipeline:
        return {"message": "No such pipeline found"}, 400
    if "name" not in request.args:
        logger.warning("Invalid query arguments")
        return {}, 400
    filename = request.args["name"]

    try:
        input_file = create_pipeline_input_file(
            organization_pipeline, filename, request.stream
        )
        return jsonify(uuid=input_file.uuid, name=input_file.name)
    except ValueError as value_error:
        return jsonify(value_error.args[0]), 400
    except HTTPError as http_error:
        return {"message": http_error.args[0]}, 503


@organization_pipeline_bp.route(
    "/<organization_uuid>/pipelines/<organization_pipeline_uuid>/runs",
    methods=["POST"],
)
@any_application_required
@validate_organization(False)
def create_pipeline_runs(organization_uuid, organization_pipeline_uuid):
    """Create a Pipeline Run
    ---
    tags:
      - pipeline runs
    parameters:
      - in: header
        name: Workflow-API-Key
        description: Requires key type REACT_CLIENT
        schema:
          type: string
    responses:
      "200":
        description: "Create a pipeline run"
        content:
          application/json:
            schema:
              type: object
              properties:
                artifacts:
                  type: array
                  items:
                    type: object
                sequence:
                  type: string
                states:
                  type: array
                  items:
                    type: object
                    properties:
                      created_at:
                        type: string
                      state:
                        type: string
                created_at:
                  type: string
                uuid:
                  type: string
      "400":
        description: "Bad request"
      "503":
        description: "Http error"
    """

    try:
        return jsonify(
            create_pipeline_run(
                organization_uuid, organization_pipeline_uuid, request.json
            )
        )
    except ValueError as value_error:
        return jsonify(value_error.args[0]), 400
    except HTTPError as http_error:
        return {"message": http_error.args[0]}, 503


@organization_pipeline_bp.route(
    "/<organization_uuid>/pipelines/<organization_pipeline_uuid>/runs",
    methods=["GET"],
)
@any_application_required
@validate_organization(False)
def pipeline_runs(organization_uuid, organization_pipeline_uuid):
    """List all Organization Pipeline Runs.
    ---
    tags:
      - pipeline runs
    parameters:
      - in: header
        name: Workflow-API-Key
        description: Requires key type REACT_CLIENT
        schema:
          type: string
    responses:
      "200":
        description: "List of pipeline runs"
        content:
          application/json:
            schema:
              type: array
              items:
                type: object
                properties:
                  artifacts:
                    type: array
                    items:
                      type: object
                  sequence:
                    type: string
                  states:
                    type: array
                    items:
                      type: object
                      properties:
                        created_at:
                          type: string
                        state:
                          type: string
                  created_at:
                    type: string
                  uuid:
                    type: string
      "400":
        description: "Bad request"
      "503":
        description: "Http error"
    """

    try:
        return jsonify(
            fetch_pipeline_runs(organization_uuid, organization_pipeline_uuid)
        )
    except ValueError as value_error:
        return jsonify(value_error.args[0]), 400
    except HTTPError as http_error:
        return {"message": http_error.args[0]}, 503


@organization_pipeline_bp.route(
    "/<organization_uuid>/pipelines/<organization_pipeline_uuid>/runs/<organization_pipeline_run_uuid>",
    methods=["GET"],
)
@any_application_required
@validate_organization(False)
def pipeline_run(
    organization_uuid, organization_pipeline_uuid, organization_pipeline_run_uuid
):
    """Fetch an Organization Pipeline Run
    ---
    tags:
      - pipeline runs
    parameters:
      - in: header
        name: Workflow-API-Key
        description: Requires key type REACT_CLIENT
        schema:
          type: string
    responses:
      "200":
        description: "Get a Pipeline Run"
        content:
          application/json:
            schema:
              type: object
              properties:
                artifacts:
                  type: array
                  items:
                    type: object
                sequence:
                  type: string
                states:
                  type: array
                  items:
                    type: object
                    properties:
                      created_at:
                        type: string
                      state:
                        type: string
                created_at:
                  type: string
                uuid:
                  type: string
      "400":
        description: "Bad request"
      "503":
        description: "Http error"
    """

    organization_pipeline = find_organization_pipeline(
        organization_uuid, organization_pipeline_uuid
    )
    if not organization_pipeline:
        return {"message": "No such pipeline found"}, 400

    try:
        return jsonify(
            fetch_pipeline_run(
                organization_uuid,
                organization_pipeline_uuid,
                organization_pipeline_run_uuid,
            )
        )
    except ValueError as value_error:
        return jsonify(value_error.args[0]), 400
    except HTTPError as http_error:
        return {"message": http_error.args[0]}, 503


@organization_pipeline_bp.route(
    "/<organization_uuid>/pipelines/<organization_pipeline_uuid>/runs/<organization_pipeline_run_uuid>/console",
    methods=["GET"],
)
@any_application_required
@validate_organization(False)
def pipeline_run_console(
    organization_uuid, organization_pipeline_uuid, organization_pipeline_run_uuid
):
    """Fetch an Organization Pipeline Run Console Output
    ---
    tags:
      - pipeline runs
    parameters:
      - in: header
        name: Workflow-API-Key
        description: Requires key type REACT_CLIENT
        schema:
          type: string
    responses:
      "200":
        description: "Get a Pipeline Run"
        content:
          application/json:
            schema:
              type: object
              properties:
                std_out:
                  type: string
                std_err:
                  type: string
      "400":
        description: "Bad request"
      "503":
        description: "Http error"
    """

    organization_pipeline = find_organization_pipeline(
        organization_uuid, organization_pipeline_uuid
    )

    if not organization_pipeline:
        return {"message": "No such pipeline found"}, 400

    try:
        return jsonify(
            fetch_pipeline_run_console(
                organization_uuid,
                organization_pipeline_uuid,
                organization_pipeline_run_uuid,
            )
        )
    except ValueError as value_error:
        return jsonify(value_error.args[0]), 400
    except HTTPError as http_error:
        return {"message": http_error.args[0]}, 503
