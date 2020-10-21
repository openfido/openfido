import logging

from flask import Blueprint, jsonify, request
from requests import HTTPError

from app.utils import validate_organization, any_application_required

from .services import fetch_pipelines, create_pipeline, update_pipeline, delete_pipeline

logger = logging.getLogger("organization-pipelines")

organization_pipeline_bp = Blueprint("organization-pipelines", __name__)


@organization_pipeline_bp.route("/<organization_uuid>/pipelines", methods=["POST"])
@any_application_required
@validate_organization()
def create(organization_uuid):
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
