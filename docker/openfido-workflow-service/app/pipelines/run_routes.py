import logging

from flask import Blueprint, jsonify, request
from marshmallow.exceptions import ValidationError

from ..model_utils import SystemPermissionEnum
from ..utils import permissions_required, verify_content_type_and_params
from .queries import find_pipeline, find_pipeline_run
from .schemas import PipelineRunSchema
from .services import (
    create_pipeline_run,
    create_pipeline_run_artifact,
    update_pipeline_run_output,
    update_pipeline_run_state,
    delete_pipeline_run,
)

logger = logging.getLogger("pipeline-runs")

run_bp = Blueprint("pipeline-runs", __name__)


@run_bp.route("/<pipeline_uuid>/runs", methods=["POST"])
@verify_content_type_and_params(["inputs"], ["callback_url"])
@permissions_required([SystemPermissionEnum.PIPELINES_CLIENT])
def create_run(pipeline_uuid):
    """Create a new pipeline run.
    ---

    tags:
      - pipeline runs
    parameters:
      - in: header
        name: Workflow-API-Key
        description: Requires key type PIPELINES_CLIENT
        schema:
          type: string
    requestBody:
      description: "A list of inputs"
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              callback_url:
                type: string
              inputs:
                type: array
                items:
                  type: object
                  properties:
                    name:
                      type: string
                      example: name.pdf
                    url:
                      type: string
                      example: https://example.com/name.pdf
    responses:
      "200":
        description: "Created"
        content:
          application/json:
            schema:
              type: object
              properties:
                uuid:
                  type: string
                  example: "5ea9102b2abd498f9830389debb21fb8"
                sequence:
                  type: integer
                  example: 1
                created_at:
                  type: string
                  example: "2020-08-05T08:15:30-05:00"
                inputs:
                  type: array
                  items:
                    type: object
                    properties:
                      uuid:
                        type: string
                        example: "5ea9102b2abd498f9830389debb21fb8"
                      name:
                        type: string
                        example: name.pdf
                      url:
                        type: string
                        example: https://example.com/name.pdf
                states:
                  type: array
                  items:
                    type: object
                    properties:
                      state:
                        type: string
                        example: NOT_STARTED
                      created_at:
                        type: string
                        example: "2020-08-05T08:15:30-05:00"
      "400":
        description: "Bad request"
    """
    try:
        pipeline_run = create_pipeline_run(pipeline_uuid, request.json)

        return jsonify(PipelineRunSchema().dump(pipeline_run))
    except ValidationError as validation_err:
        logger.warning(validation_err)
        return {"message": "Validation error", "errors": validation_err.messages}, 400
    except ValueError:
        logger.warning("unable to create pipeline run")
        return {
            "message": "Unable to create workflow",
        }, 400


@run_bp.route("/<pipeline_uuid>/runs/<pipeline_run_uuid>", methods=["GET"])
@permissions_required([SystemPermissionEnum.PIPELINES_CLIENT])
def get_run(pipeline_uuid, pipeline_run_uuid):
    """Get a pipeline run.
    ---

    tags:
      - pipeline runs
    parameters:
      - in: header
        name: Workflow-API-Key
        description: Requires key type PIPELINES_CLIENT
        schema:
          type: string
    responses:
      "200":
        description: "Fetched"
        content:
          application/json:
            schema:
              type: object
              properties:
                uuid:
                  type: string
                  example: "5ea9102b2abd498f9830389debb21fb8"
                sequence:
                  type: integer
                  example: 1
                created_at:
                  type: string
                  example: "2020-08-05T08:15:30-05:00"
                inputs:
                  type: array
                  items:
                    type: object
                    properties:
                      uuid:
                        type: string
                        example: "5ea9102b2abd498f9830389debb21fb8"
                      name:
                        type: string
                        example: name.pdf
                      url:
                        type: string
                        example: https://example.com/name.pdf
                states:
                  type: array
                  items:
                    type: object
                    properties:
                      state:
                        type: string
                        example: NOT_STARTED
                      created_at:
                        type: string
                        example: "2020-08-05T08:15:30-05:00"
      "400":
        description: "Bad request"
    """
    pipeline = find_pipeline(pipeline_uuid)
    if pipeline is None:
        logger.warning("no pipeline found")
        return {}, 404

    pipeline_run = find_pipeline_run(pipeline_run_uuid)
    if pipeline_run is None:
        logger.warning("no pipeline run found")
        return {}, 404

    return jsonify(PipelineRunSchema().dump(pipeline_run))

@run_bp.route("/<pipeline_uuid>/runs/<pipeline_run_uuid>", methods=["DELETE"])
@permissions_required([SystemPermissionEnum.PIPELINES_CLIENT])
def delete_run(pipeline_uuid, pipeline_run_uuid):
    """Delete a pipeline run.
    ---
    tags:
      - pipelines
    parameters:
      - in: header
        name: Workflow-API-Key
        description: Requires key type PIPELINES_CLIENT
        schema:
          type: string
    parameters:
      - name: pipeline_uuid
        in: path
        required: true
        description: UUID of a pipeline.
      - name: pipeline_run_uuid
        in: path
        required: true
        description: UUID of a pipeline run.
    responses:
      "200":
        description: "Deleted"
      "400":
        description: "Bad request"
    """
    try:
        delete_pipeline_run(pipeline_uuid, pipeline_run_uuid)
        return {}, 200
    except ValueError:
        return {
            "message": "Unable to delete workflow pipeline run",
        }, 400

@run_bp.route("/<pipeline_uuid>/runs/<pipeline_run_uuid>", methods=["DELETE"])
@permissions_required([SystemPermissionEnum.PIPELINES_CLIENT])
def delete_run(pipeline_uuid, pipeline_run_uuid):
    """Delete a pipeline run.
    ---

    tags:
      - pipeline runs
    parameters:
      - in: header
        name: Workflow-API-Key
        description: Requires key type PIPELINES_CLIENT
        schema:
          type: string
    responses:
      "200":
        description: "Deleted"
      "400":
        description: "Bad request"
    """
    try:
        delete_pipeline_run(pipeline_uuid, pipeline_run_uuid)
        return {}, 200
    except ValueError:
        return {
            "message": "Unable to delete workflow pipeline run",
        }, 400


@run_bp.route("/<pipeline_uuid>/runs", methods=["GET"])
@permissions_required([SystemPermissionEnum.PIPELINES_CLIENT])
def get_runs(pipeline_uuid):
    """Get a all pipeline runs for a pipeline.
    ---

    tags:
      - pipeline runs
    parameters:
      - in: header
        name: Workflow-API-Key
        description: Requires key type PIPELINES_CLIENT
        schema:
          type: string
    responses:
      "200":
        description: "Fetched"
        content:
          application/json:
            schema:
              type: array
              items:
                type: object
                properties:
                  uuid:
                    type: string
                    example: "5ea9102b2abd498f9830389debb21fb8"
                  sequence:
                    type: integer
                    example: 1
                  created_at:
                    type: string
                    example: "2020-08-05T08:15:30-05:00"
                  inputs:
                    type: array
                    items:
                      type: object
                      properties:
                        uuid:
                          type: string
                          example: "5ea9102b2abd498f9830389debb21fb8"
                        name:
                          type: string
                          example: name.pdf
                        url:
                          type: string
                          example: https://example.com/name.pdf
                  states:
                    type: array
                    items:
                      type: object
                      properties:
                        state:
                          type: string
                          example: NOT_STARTED
                        created_at:
                          type: string
                          example: "2020-08-05T08:15:30-05:00"
      "400":
        description: "Bad request"
    """
    pipeline = find_pipeline(pipeline_uuid)
    if pipeline is None:
        logger.warning("no pipeline found")
        return {}, 404

    return jsonify(
        [
            PipelineRunSchema().dump(pr)
            for pr in pipeline.pipeline_runs
            if not pr.is_deleted
        ]
    )


@run_bp.route("/<pipeline_uuid>/runs/<pipeline_run_uuid>/console", methods=["GET"])
@permissions_required([SystemPermissionEnum.PIPELINES_CLIENT])
def get_run_output(pipeline_uuid, pipeline_run_uuid):
    """Get the console output of a run.
    ---

    tags:
      - pipeline runs
    parameters:
      - in: header
        name: Workflow-API-Key
        description: Requires key type PIPELINES_CLIENT
        schema:
          type: string
    responses:
      "200":
        description: "Fetched"
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
    """
    pipeline = find_pipeline(pipeline_uuid)
    if pipeline is None:
        logger.warning("no pipeline found")
        return {}, 404

    pipeline_run = find_pipeline_run(pipeline_run_uuid)
    if pipeline_run is None:
        logger.warning("no pipeline run found")
        return {}, 404

    return jsonify(
        std_out=pipeline_run.std_out or "",
        std_err=pipeline_run.std_err or "",
    )


@run_bp.route("/<pipeline_uuid>/runs/<pipeline_run_uuid>/console", methods=["PUT"])
@verify_content_type_and_params(["std_out", "std_err"], [])
@permissions_required([SystemPermissionEnum.PIPELINES_WORKER])
def upload_run_output(pipeline_uuid, pipeline_run_uuid):
    """Update the console output.
    ---

    tags:
      - pipeline runs
    parameters:
      - in: header
        name: Workflow-API-Key
        description: Requires key type PIPELINES_WORKER
        schema:
          type: string
    requestBody:
      description: "standard output and error"
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              std_out:
                type: string
              std_err:
                type: string
    responses:
      "200":
        description: "Updated"
      "400":
        description: "Bad request"
    """
    pipeline = find_pipeline(pipeline_uuid)
    if pipeline is None:
        logger.warning("no pipeline found")
        return {}, 404

    pipeline_run = find_pipeline_run(pipeline_run_uuid)
    if pipeline_run is None:
        logger.warning("no pipeline run found")
        return {}, 404

    update_pipeline_run_output(
        pipeline_run.uuid, request.json["std_out"], request.json["std_err"]
    )

    return {}, 200


@run_bp.route("/<pipeline_uuid>/runs/<pipeline_run_uuid>/state", methods=["PUT"])
@verify_content_type_and_params(["state"], [])
@permissions_required([SystemPermissionEnum.PIPELINES_WORKER])
def upload_run_state(pipeline_uuid, pipeline_run_uuid):
    """Update a run state.
    ---

    tags:
      - pipeline runs
    parameters:
      - in: header
        name: Workflow-API-Key
        description: Requires key type PIPELINES_WORKER
        schema:
          type: string
    requestBody:
      description: "run state"
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              state:
                type: string
                example: RUNNING
    responses:
      "200":
        description: "Updated"
      "400":
        description: "Bad request"
    """
    pipeline = find_pipeline(pipeline_uuid)
    if pipeline is None:
        logger.warning("no pipeline found")
        return {}, 404

    pipeline_run = find_pipeline_run(pipeline_run_uuid)
    if pipeline_run is None:
        logger.warning("no pipeline run found")
        return {}, 404

    try:
        update_pipeline_run_state(pipeline_run.uuid, request.json)
    except ValidationError as validation_err:
        logger.warning(validation_err)
        return {}, 400
    except ValueError as value_err:
        logger.warning(value_err)
        return {}, 400

    return {}, 200


@run_bp.route("/<pipeline_uuid>/runs/<pipeline_run_uuid>/artifacts", methods=["POST"])
@permissions_required([SystemPermissionEnum.PIPELINES_WORKER])
def upload_run_artifact(pipeline_uuid, pipeline_run_uuid):
    """Upload an artifact associated with a pipeline run.
    ---

    tags:
      - pipeline runs
    parameters:
      - in: header
        name: Workflow-API-Key
        description: Requires key type PIPELINES_WORKER
        schema:
          type: string
      - in: query
        name: name
        schema:
          type: string
    requestBody:
      description: "binary file content"
      required: true
    responses:
      "200":
        description: "Updated"
      "400":
        description: "Bad request"
      "413":
        description: "Payload Too Large"
    """
    if "name" not in request.args:
        logger.warning("Invalid query arguments")
        return {}, 400
    filename = request.args["name"]
    if len(filename) > 255:
        logger.warning("filename too long")
        return {}, 400

    pipeline = find_pipeline(pipeline_uuid)
    if pipeline is None:
        logger.warning("no pipeline found")
        return {}, 404

    pipeline_run = find_pipeline_run(pipeline_run_uuid)
    if pipeline_run is None:
        logger.warning("no pipeline run found")
        return {}, 404

    try:
        create_pipeline_run_artifact(pipeline_run.uuid, filename, request.stream)
        return {}, 200
    except ValueError as value_err:
        logger.warning(value_err)
        return {}, 400
