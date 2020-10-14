import logging

from flask import Blueprint, jsonify
from requests import HTTPError

from app.utils import validate_organization, any_application_required

from .services import fetch_pipelines

logger = logging.getLogger("organization-pipelines")

organization_pipeline_bp = Blueprint("organization-pipelines", __name__)


@organization_pipeline_bp.route("/<organization_uuid>/pipelines", methods=["GET"])
@any_application_required
@validate_organization()
def pipelines(organization_uuid):
    """List all Organization Pipelines.
    ---
    tags:
      - pipelines
    parameters:
      - in: header
        name: Workflow-API-Key
        description: Requires key type PIPELINES_CLIENT
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
