import logging

from flask import Blueprint, jsonify, request
from marshmallow.exceptions import ValidationError

from ..model_utils import SystemPermissionEnum
from ..utils import permissions_required, verify_content_type
from .schemas import WorkflowPipelineSchema
from .services import create_workflow_pipeline

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
                description: List of incoming Workflow Pipeline UUIDs that feed into this Workflow Pipeline
              destination_workflow_pipelines:
                type: array
                items:
                  type: string
                description: List of outgoing Workflow Pipeline UUIDs that this Workflow Pipeline's output will go.
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
    except ValidationError as ve:
        logger.warning(ve)
        return {"message": "Validation error", "errors": ve.messages}, 400
    except ValueError as e:
        logger.warning(e)
        return {
            "message": "Unable to create WorkflowPipeline",
        }, 400
