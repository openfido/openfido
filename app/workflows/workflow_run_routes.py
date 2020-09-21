import logging

from flask import Blueprint, jsonify, request

from app.pipelines.schemas import PipelineRunSchema
from marshmallow.exceptions import ValidationError

from ..model_utils import SystemPermissionEnum
from ..utils import permissions_required, verify_content_type
from .schemas import WorkflowRunSchema
from .services import create_workflow_pipeline_run

logger = logging.getLogger("workflow-runs")

workflow_run_bp = Blueprint("workflow-runs", __name__)


@workflow_run_bp.route("/<workflow_uuid>/runs", methods=["POST"])
@verify_content_type()
@permissions_required([SystemPermissionEnum.PIPELINES_CLIENT])
def create_run(workflow_uuid):
    """Create a new workflow run.
    ---

    tags:
      - workflow runs
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
        workflow_run = create_workflow_pipeline_run(workflow_uuid, request.json)

        return jsonify(WorkflowRunSchema().dump(workflow_run))
    except ValidationError as validation_err:
        logger.warning(validation_err)
        return {"message": "Validation error", "errors": validation_err.messages}, 400
    except ValueError:
        logger.warning("unable to create pipeline run")
        return {
            "message": "Unable to create workflow",
        }, 400
