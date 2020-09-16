import logging

from flask import Blueprint, jsonify, request
from marshmallow.exceptions import ValidationError

from ..model_utils import SystemPermissionEnum
from ..utils import permissions_required, verify_content_type
from .schemas import WorkflowSchema
from .services import create_workflow, update_workflow, delete_workflow

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
                value: { "message": "An error", "errors": { "name": "Must be provided" } }
                summary: An error with validation messages.
    """
    try:
        workflow = create_workflow(request.json)

        return jsonify(WorkflowSchema().dump(workflow))
    except ValidationError as ve:
        return {"message": "Validation error", "errors": ve.messages}, 400
    except ValueError:
        return {
            "message": "Unable to create workflow",
        }, 400


@workflow_bp.route("/<workflow_uuid>", methods=["DELETE"])
@permissions_required([SystemPermissionEnum.PIPELINES_CLIENT])
def remove(workflow_uuid):
    """Delete a Workflow.
    ---

    responses:
      "200":
        description: "Removed"
      "400":
        description: "Bad request"
    """
    try:
        delete_workflow(workflow_uuid)
        return {}, 200
    except ValueError:
        return {
            "message": "Unable to delete workflow",
        }, 400


@workflow_bp.route("/<workflow_uuid>", methods=["PUT"])
@verify_content_type()
@permissions_required([SystemPermissionEnum.PIPELINES_CLIENT])
def update(workflow_uuid):
    """Update a Workflow.
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
        description: "Updated"
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
                value: { "message": "An error", "errors": { "name": "Must be provided" } }
                summary: An error with validation messages.
    """
    try:
        workflow = update_workflow(workflow_uuid, request.json)

        return jsonify(WorkflowSchema().dump(workflow))
    except ValidationError as ve:
        return {"message": "Validation error", "errors": ve.messages}, 400
    except ValueError:
        return {
            "message": "Unable to update workflow",
        }, 400
