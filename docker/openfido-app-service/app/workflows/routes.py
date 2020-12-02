import logging

from flask import Blueprint, jsonify, request, current_app
from requests import HTTPError

from app.utils import validate_organization, any_application_required
from app.workflows.services import (
    create_workflow,
    delete_workflow,
    fetch_workflow,
    fetch_workflows,
    update_workflow,
    create_workflow_pipeline,
    fetch_workflow_pipelines,
    fetch_workflow_pipeline,
    update_workflow_pipeline,
    delete_workflow_pipeline,
)

logger = logging.getLogger("organization-workflows")

organization_workflow_bp = Blueprint("workflows", __name__)


@organization_workflow_bp.route("/<organization_uuid>/workflows", methods=["POST"])
@any_application_required
@validate_organization()
def create(organization_uuid):
    """Create a Organization Workflow.
    ---
    tags:
      - workflows
    parameters:
      - in: header
        name: Workflow-API-Key
        description: Requires key type REACT_CLIENT
        schema:
          type: string
    requestBody:
      description: "Workflow name and description."
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
        description: "Updated OrganizationWorkflow"
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
      "503":
        description: "Http error"
    """
    try:
        return jsonify(create_workflow(organization_uuid, request.json))
    except HTTPError as http_error:
        return {"message": http_error.args[0]}, 503
    except ValueError as value_error:
        return jsonify(value_error.args[0]), 400


@organization_workflow_bp.route("/<organization_uuid>/workflows", methods=["GET"])
@any_application_required
@validate_organization()
def workflows(organization_uuid):
    """Get Organization Workflows.
    ---
    tags:
      - workflows
    parameters:
      - in: header
        name: Workflow-API-Key
        description: Requires key type REACT_CLIENT
        schema:
          type: string
    responses:
      "200":
        description: "Updated OrganizationWorkflow"
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
      "503":
        description: "Http error"
    """
    try:
        return jsonify(fetch_workflows(organization_uuid))
    except HTTPError as http_error:
        return {"message": http_error.args[0]}, 503
    except ValueError as value_error:
        return jsonify(value_error.args[0]), 400


@organization_workflow_bp.route(
    "/<organization_uuid>/workflows/<organization_workflow_uuid>", methods=["GET"]
)
@any_application_required
@validate_organization(False)
def workflow(organization_uuid, organization_workflow_uuid):
    """Get Organization Workflow.
    ---
    tags:
      - workflows
    parameters:
      - in: header
        name: Workflow-API-Key
        description: Requires key type REACT_CLIENT
        schema:
          type: string
    responses:
      "200":
        description: "Updated OrganizationWorkflow"
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
      "503":
        description: "Http error"
    """
    try:
        return jsonify(fetch_workflow(organization_uuid, organization_workflow_uuid))
    except HTTPError as http_error:
        return {"message": http_error.args[0]}, 503
    except ValueError as value_error:
        return jsonify(value_error.args[0]), 400


@organization_workflow_bp.route(
    "/<organization_uuid>/workflows/<organization_workflow_uuid>", methods=["PUT"]
)
@any_application_required
@validate_organization()
def workflow_update(organization_uuid, organization_workflow_uuid):
    """Updates Organization Workflow.
    ---
    tags:
      - workflows
    parameters:
      - in: header
        name: Workflow-API-Key
        description: Requires key type REACT_CLIENT
        schema:
          type: string
    responses:
      "200":
        description: "Updated OrganizationWorkflow"
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
      "503":
        description: "Http error"
    """
    try:
        return jsonify(
            update_workflow(organization_uuid, organization_workflow_uuid, request.json)
        )
    except HTTPError as http_error:
        return {"message": http_error.args[0]}, 503
    except ValueError as value_error:
        return jsonify(value_error.args[0]), 400


@organization_workflow_bp.route(
    "/<organization_uuid>/workflows/<organization_workflow_uuid>", methods=["DELETE"]
)
@any_application_required
@validate_organization(False)
def workflow_delete(organization_uuid, organization_workflow_uuid):
    """Delete a Organization Workflow.
    ---
    tags:
      - workflows
    parameters:
      - in: header
        name: Workflow-API-Key
        description: Requires key type REACT_CLIENT
        schema:
          type: string
    responses:
      "200":
        description: "Updated OrganizationWorkflow"
      "400":
        description: "Bad request"
      "503":
        description: "Http error"
    """

    try:
        delete_workflow(organization_uuid, organization_workflow_uuid)
        return {}, 200
    except HTTPError as http_error:
        return {"message": http_error.args[0]}, 503
    except ValueError as value_error:
        return jsonify(value_error.args[0]), 400


@organization_workflow_bp.route(
    "/<organization_uuid>/workflows/<organization_workflow_uuid>/pipelines",
    methods=["POST"],
)
@any_application_required
@validate_organization()
def workflow_pipeline_create(organization_uuid, organization_workflow_uuid):
    """Create a Organization Workflow Pipeline
    ---
    tags:
      - workflows
    parameters:
      - in: header
        name: Workflow-API-Key
        description: Requires key type REACT_CLIENT
        schema:
          type: string
    requestBody:
      description: "Create a Organization Workflow Pipeline"
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
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
    responses:
      "200":
        description: "Updated OrganizationWorkflow"
        content:
          application/json:
            schema:
              type: object
              properties:
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
                uuid:
                  type: string
                created_at:
                  type: string
                updated_at:
                  type: string
      "400":
        description: "Bad request"
      "503":
        description: "Http error"
    """
    try:
        return jsonify(
            create_workflow_pipeline(
                organization_uuid, organization_workflow_uuid, request.json
            )
        )
    except HTTPError as http_error:
        return {"message": http_error.args[0]}, 503
    except ValueError as value_error:
        return jsonify(value_error.args[0]), 400


@organization_workflow_bp.route(
    "/<organization_uuid>/workflows/<organization_workflow_uuid>/pipelines",
    methods=["GET"],
)
@any_application_required
@validate_organization()
def workflow_pipelines(organization_uuid, organization_workflow_uuid):
    """Get Organization Workflow Pipelines.
    ---
    tags:
      - workflows
    parameters:
      - in: header
        name: Workflow-API-Key
        description: Requires key type REACT_CLIENT
        schema:
          type: string
    responses:
      "200":
        description: "Get Organization Workflow Pipelines."
        content:
          application/json:
            schema:
              type: array
              items:
                type: object
                properties:
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
                  uuid:
                    type: string
                  created_at:
                    type: string
                  updated_at:
                    type: string
      "400":
        description: "Bad request"
      "503":
        description: "Http error"
    """
    try:
        return jsonify(
            fetch_workflow_pipelines(organization_uuid, organization_workflow_uuid)
        )
    except HTTPError as http_error:
        return {"message": http_error.args[0]}, 503
    except ValueError as value_error:
        return jsonify(value_error.args[0]), 400


@organization_workflow_bp.route(
    "/<organization_uuid>/workflows/<organization_workflow_uuid>/pipelines/<organization_workflow_pipeline_uuid>",
    methods=["GET"],
)
@any_application_required
@validate_organization()
def workflow_pipeline(
    organization_uuid, organization_workflow_uuid, organization_workflow_pipeline_uuid
):
    """Get Organization Workflow Pipeline.
    ---
    tags:
      - workflows
    parameters:
      - in: header
        name: Workflow-API-Key
        description: Requires key type REACT_CLIENT
        schema:
          type: string
    responses:
      "200":
        description: "Get Organization Workflow Pipeline."
        content:
          application/json:
            schema:
              type: object
              properties:
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
                uuid:
                  type: string
                created_at:
                  type: string
                updated_at:
                  type: string
      "400":
        description: "Bad request"
      "503":
        description: "Http error"
    """
    try:
        return jsonify(
            fetch_workflow_pipeline(
                organization_uuid,
                organization_workflow_uuid,
                organization_workflow_pipeline_uuid,
            )
        )
    except HTTPError as http_error:
        return {"message": http_error.args[0]}, 503
    except ValueError as value_error:
        return jsonify(value_error.args[0]), 400


@organization_workflow_bp.route(
    "/<organization_uuid>/workflows/<organization_workflow_uuid>/pipelines/<organization_workflow_pipeline_uuid>",
    methods=["PUT"],
)
@any_application_required
@validate_organization()
def workflow_pipeline_update(
    organization_uuid, organization_workflow_uuid, organization_workflow_pipeline_uuid
):
    """Update Organization Workflow Pipeline.
    ---
    tags:
      - workflows
    parameters:
      - in: header
        name: Workflow-API-Key
        description: Requires key type REACT_CLIENT
        schema:
          type: string
    responses:
      "200":
        description: "Update Organization Workflow Pipeline."
        content:
          application/json:
            schema:
              type: object
              properties:
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
                uuid:
                  type: string
                created_at:
                  type: string
                updated_at:
                  type: string
      "400":
        description: "Bad request"
      "503":
        description: "Http error"
    """
    try:
        return jsonify(
            update_workflow_pipeline(
                organization_uuid,
                organization_workflow_uuid,
                organization_workflow_pipeline_uuid,
                request.json,
            )
        )
    except HTTPError as http_error:
        return {"message": http_error.args[0]}, 503
    except ValueError as value_error:
        return jsonify(value_error.args[0]), 400


@organization_workflow_bp.route(
    "/<organization_uuid>/workflows/<organization_workflow_uuid>/pipelines/<organization_workflow_pipeline_uuid>",
    methods=["DELETE"],
)
@any_application_required
@validate_organization()
def workflow_pipeline_delete(
    organization_uuid, organization_workflow_uuid, organization_workflow_pipeline_uuid
):
    """Delete an Organization Workflow Pipeline.
    ---
    tags:
      - workflows
    parameters:
      - in: header
        name: Workflow-API-Key
        description: Requires key type REACT_CLIENT
        schema:
          type: string
    responses:
      "200":
        description: "Delete an Organization Workflow Pipeline"
      "400":
        description: "Bad request"
      "503":
        description: "Http error"
    """

    try:
        delete_workflow_pipeline(
            organization_uuid,
            organization_workflow_uuid,
            organization_workflow_pipeline_uuid,
        )
        return {}, 200
    except HTTPError as http_error:
        return {"message": http_error.args[0]}, 503
    except ValueError as value_error:
        return jsonify(value_error.args[0]), 400
