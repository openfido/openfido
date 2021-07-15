import logging

from flask import Blueprint, jsonify, request
from marshmallow.exceptions import ValidationError

from ..model_utils import SystemPermissionEnum
from ..utils import permissions_required, verify_content_type
from .queries import find_workflow, find_workflows
from .schemas import WorkflowSchema
from .services import create_workflow, update_workflow, delete_workflow
from ..utils import verify_content_type_and_params, permissions_required

logger = logging.getLogger("workflows")

workflow_bp = Blueprint("workflow", __name__)


@workflow_bp.route("", methods=["POST"])
@verify_content_type()
@permissions_required([SystemPermissionEnum.PIPELINES_CLIENT])
def create():
    """Create a Workflow.
    ---

    tags:
      - workflows
    parameters:
      - in: header
        name: Workflow-API-Key
        description: Requires key type PIPELINES_CLIENT
        schema:
          type: string
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
    except ValidationError as validation_err:
        logger.warning(validation_err)
        return {"message": "Validation error", "errors": validation_err.messages}, 400
    except ValueError as value_err:
        logger.warning(value_err)
        return {
            "message": "Unable to create workflow",
        }, 400


@workflow_bp.route("", methods=["GET"])
@verify_content_type()
@permissions_required([SystemPermissionEnum.PIPELINES_CLIENT])
def list():
    """List Workflows.
    ---

    tags:
      - workflows
    parameters:
      - in: header
        name: Workflow-API-Key
        description: Requires key type PIPELINES_CLIENT
        schema:
          type: string
    responses:
      "200":
        description: "Found"
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
                value: { "message": "An error occurred" }
                summary: An error occurred
    """
    workflows = find_workflows()

    return jsonify([WorkflowSchema().dump(w) for w in workflows])


@workflow_bp.route("/<workflow_uuid>", methods=["GET"])
@verify_content_type()
@permissions_required([SystemPermissionEnum.PIPELINES_CLIENT])
def get(workflow_uuid):
    """Get a Workflow.
    ---

    tags:
      - workflows
    parameters:
      - in: header
        name: Workflow-API-Key
        description: Requires key type PIPELINES_CLIENT
        schema:
          type: string
    responses:
      "200":
        description: "Found"
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
                value: { "message": "An error occurred" }
                summary: An error occurred
    """
    workflow = find_workflow(workflow_uuid)
    if workflow is None:
        logger.warning("no workflow found")
        return {
            "message": "Unable to get workflow",
        }, 400

    return jsonify(WorkflowSchema().dump(workflow))


@workflow_bp.route("/<workflow_uuid>", methods=["DELETE"])
@permissions_required([SystemPermissionEnum.PIPELINES_CLIENT])
def remove(workflow_uuid):
    """Delete a Workflow.
    ---

    tags:
      - workflows
    parameters:
      - in: header
        name: Workflow-API-Key
        description: Requires key type PIPELINES_CLIENT
        schema:
          type: string
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

    tags:
      - workflows
    parameters:
      - in: header
        name: Workflow-API-Key
        description: Requires key type PIPELINES_CLIENT
        schema:
          type: string
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
    except ValidationError as validation_err:
        logger.warning(validation_err)
        return {"message": "Validation error", "errors": validation_err.messages}, 400
    except ValueError as value_err:
        logger.warning(value_err)
        return {
            "message": "Unable to update workflow",
        }, 400


@workflow_bp.route("/search", methods=["POST"])
@verify_content_type_and_params(["uuids"], [])
@permissions_required([SystemPermissionEnum.PIPELINES_CLIENT])
def search():
    """Search for workflows with specific UUIDs.
    ---

    tags:
      - workflows
    parameters:
      - in: header
        name: Workflow-API-Key
        description: Requires key type PIPELINES_CLIENT
        schema:
          type: string
    requestBody:
      description: "Workflow description and configuration."
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              uuids:
                type: array
                items:
                  type: string
                  example: "uuid1"
    responses:
      "200":
        description: "Matching UUIDs"
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
                value: { "message": "Unable to search workflow", "errors": { "name": "invalid uuid format" } }
                summary: An error with validation messages.
    """
    try:
        workflows = find_workflows(request.json)

        return jsonify([WorkflowSchema().dump(w) for w in workflows])
    except ValidationError as ve:
        return {"message": "Unable to search workflow", "errors": ve.messages}, 400
