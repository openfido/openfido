import logging

from flask import Blueprint, jsonify, request
from marshmallow.exceptions import ValidationError

from ..model_utils import SystemPermissionEnum
from ..utils import permissions_required, to_iso8601, verify_content_type
from .models import db
from .schemas import WorkflowSchema
from .services import create_workflow

logger = logging.getLogger("workflows")

workflow_bp = Blueprint("workflows", __name__)


@workflow_bp.route("", methods=["POST"])
@verify_content_type()
@permissions_required([SystemPermissionEnum.PIPELINES_CLIENT])
def create():
    """Create a Workflow.
    ---

    requestBody:
      description: "Workflow name and description"
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
                name:
                  type: string
                description:
                  type: string
                created_at:
                  type: string
                updated_at:
                  type: string
      "400":
        description: "Bad request"
    """
    # TODO provide better error message formatting.
    try:
        workflow = create_workflow(request.json)

        return jsonify(WorkflowSchema().dump(workflow))
    except ValidationError as ve:
        return {"message": "Validation error", "errors": ve.messages}, 400
    except ValueError:
        return {
            "message": "Unable to create workflow",
        }, 400
