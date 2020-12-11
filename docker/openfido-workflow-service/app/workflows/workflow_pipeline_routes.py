import logging

from flask import Blueprint, jsonify, request
from marshmallow.exceptions import ValidationError

from ..model_utils import SystemPermissionEnum
from ..utils import permissions_required, verify_content_type
from .schemas import WorkflowPipelineSchema
from .services import (
    create_workflow_pipeline,
    update_workflow_pipeline,
    delete_workflow_pipeline,
    find_workflow,
    find_workflow_pipeline,
)

logger = logging.getLogger("workflow-pipeline")

workflow_pipeline_bp = Blueprint("workflow-pipeline", __name__)


@workflow_pipeline_bp.route("/<workflow_uuid>/pipelines", methods=["POST"])
@verify_content_type()
@permissions_required([SystemPermissionEnum.PIPELINES_CLIENT])
def create(workflow_uuid):
    """Add a Workflow Pipeline.
    ---

    tags:
      - workflow pipelines
    parameters:
      - in: header
        name: Workflow-API-Key
        description: Requires key type PIPELINES_CLIENT
        schema:
          type: string
    requestBody:
      description: "source and dest pipelines"
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              pipeline_uuid:
                type: string
                example: abc123
              source_workflow_pipelines:
                type: array
                items:
                  type: string
                description: List of incoming Workflow Pipeline UUIDs that feed into this.
              destination_workflow_pipelines:
                type: array
                items:
                  type: string
                description: List of outgoing Workflow Pipeline UUIDs that this output will go to.
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
                pipeline_uuid:
                  type: string
                source_workflow_pipelines:
                  type: array
                  items:
                    type: string
                destination_workflow_pipelines:
                  type: array
                  items:
                    type: string
                created_at:
                  type: string
                updated_at:
                  type: string
      "400":
        description: "Bad request"
        content:
          application/json:
            schema:
              type: object
              properties:
                message:
                  type: string
                errors:
                  type: object
            examples:
              message_and_error:
                value: { "message": "An error", "errors": { "pipeline_uuid": "Must be provided" } }
                summary: An error with validation messages.
    """
    try:
        workflow_pipeline = create_workflow_pipeline(workflow_uuid, request.json)

        return jsonify(WorkflowPipelineSchema().dump(workflow_pipeline))
    except ValidationError as validation_err:
        logger.warning(validation_err)
        return {"message": "Validation error", "errors": validation_err.messages}, 400
    except ValueError as value_err:
        logger.warning(value_err)
        return {
            "message": "Unable to create WorkflowPipeline",
        }, 400


@workflow_pipeline_bp.route(
    "/<workflow_uuid>/pipelines/<workflow_pipeline_uuid>", methods=["PUT"]
)
@verify_content_type()
@permissions_required([SystemPermissionEnum.PIPELINES_CLIENT])
def update(workflow_uuid, workflow_pipeline_uuid):
    """Update a Workflow Pipeline.
    ---

    tags:
      - workflow pipelines
    parameters:
      - in: header
        name: Workflow-API-Key
        description: Requires key type PIPELINES_CLIENT
        schema:
          type: string
    requestBody:
      description: "source and dest pipelines"
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              pipeline_uuid:
                type: string
                example: abc123
              source_workflow_pipelines:
                type: array
                items:
                  type: string
                description: List of incoming Workflow Pipeline UUIDs that feed into this.
              destination_workflow_pipelines:
                type: array
                items:
                  type: string
                description: List of outgoing Workflow Pipeline UUIDs that this output will go to.
    responses:
      "200":
        description: "Updated"
        content:
          application/json:
            schema:
              type: object
              properties:
                uuid:
                  type: string
                pipeline_uuid:
                  type: string
                source_workflow_pipelines:
                  type: array
                  items:
                    type: string
                destination_workflow_pipelines:
                  type: array
                  items:
                    type: string
                created_at:
                  type: string
                updated_at:
                  type: string
      "400":
        description: "Bad request"
        content:
          application/json:
            schema:
              type: object
              properties:
                message:
                  type: string
                errors:
                  type: object
            examples:
              message_and_error:
                value: { "message": "An error", "errors": { "pipeline_uuid": "Must be provided" } }
                summary: An error with validation messages.
    """
    try:
        workflow_pipeline = update_workflow_pipeline(
            workflow_uuid, workflow_pipeline_uuid, request.json
        )

        return jsonify(WorkflowPipelineSchema().dump(workflow_pipeline))
    except ValidationError as validation_err:
        logger.warning(validation_err)
        return {"message": "Validation error", "errors": validation_err.messages}, 400
    except ValueError as value_err:
        logger.warning(value_err)
        return {
            "message": "Unable to create WorkflowPipeline",
        }, 400


@workflow_pipeline_bp.route("/<workflow_uuid>/pipelines", methods=["GET"])
@permissions_required([SystemPermissionEnum.PIPELINES_CLIENT])
def list_workflow_pipelines(workflow_uuid):
    """Get all pipelines for a workflow.
    ---

    tags:
      - workflow pipelines
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
                  pipeline_uuid:
                    type: string
                  source_workflow_pipelines:
                    type: array
                    items:
                      type: string
                  destination_workflow_pipelines:
                    type: array
                    items:
                      type: string
                  created_at:
                    type: string
                  updated_at:
                    type: string
      "400":
        description: "Bad request"
    """
    workflow = find_workflow(workflow_uuid)
    if workflow is None:
        logger.warning("no workflow found")
        return {}, 404

    return jsonify(
        [WorkflowPipelineSchema().dump(wp) for wp in workflow.workflow_pipelines if not wp.is_deleted]
    )


@workflow_pipeline_bp.route(
    "/<workflow_uuid>/pipelines/<workflow_pipeline_uuid>", methods=["GET"]
)
@permissions_required([SystemPermissionEnum.PIPELINES_CLIENT])
def get_workflow_pipeline(workflow_uuid, workflow_pipeline_uuid):
    """Get a workflow pipeline.
    ---

    tags:
      - workflow pipelines
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
                pipeline_uuid:
                  type: string
                source_workflow_pipelines:
                  type: array
                  items:
                    type: string
                destination_workflow_pipelines:
                  type: array
                  items:
                    type: string
                created_at:
                  type: string
                updated_at:
                  type: string
      "400":
        description: "Bad request"
    """
    workflow = find_workflow(workflow_uuid)
    if workflow is None:
        logger.warning("no workflow found")
        return {}, 404

    workflow_pipeline = find_workflow_pipeline(workflow_pipeline_uuid)
    if workflow_pipeline is None:
        logger.warning("no workflow pipeline found")
        return {}, 404

    return jsonify(WorkflowPipelineSchema().dump(workflow_pipeline))


@workflow_pipeline_bp.route(
    "/<workflow_uuid>/pipelines/<workflow_pipeline_uuid>", methods=["DELETE"]
)
@permissions_required([SystemPermissionEnum.PIPELINES_CLIENT])
def delete(workflow_uuid, workflow_pipeline_uuid):
    """Delete a workflow pipeline.
    ---
    tags:
      - workflow pipelines
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
        delete_workflow_pipeline(workflow_uuid, workflow_pipeline_uuid)
        return {}, 200
    except ValueError:
        return {
            "message": "Unable to delete workflow pipeline",
        }, 400
