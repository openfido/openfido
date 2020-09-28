import logging

from flask import Blueprint, jsonify, request
from marshmallow.exceptions import ValidationError

from .models import db
from ..model_utils import SystemPermissionEnum
from .queries import find_pipeline, find_pipelines
from .schemas import PipelineSchema
from .services import (
    create_pipeline,
    delete_pipeline,
    update_pipeline,
)
from ..utils import verify_content_type_and_params, permissions_required

logger = logging.getLogger("pipelines")

pipeline_bp = Blueprint("pipelines", __name__)


@pipeline_bp.route("", methods=["POST"])
@verify_content_type_and_params(
    [
        "name",
        "description",
        "docker_image_url",
        "repository_ssh_url",
        "repository_branch",
    ],
    [],
)
@permissions_required([SystemPermissionEnum.PIPELINES_CLIENT])
def create():
    """Create a pipeline.
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
    name = request.json["name"]
    description = request.json["description"]
    docker_image_url = request.json["docker_image_url"]
    repository_ssh_url = request.json["repository_ssh_url"]
    repository_branch = request.json["repository_branch"]
    try:
        pipeline = create_pipeline(
            name, description, docker_image_url, repository_ssh_url, repository_branch
        )
        db.session.commit()

        return jsonify(PipelineSchema().dump(pipeline))
    except ValueError:
        return {"message": "Unable to create pipeline"}, 400


@pipeline_bp.route("/<pipeline_uuid>", methods=["GET"])
@verify_content_type_and_params([], [])
@permissions_required([SystemPermissionEnum.PIPELINES_CLIENT])
def get(pipeline_uuid):
    """Get a pipeline.
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
      - name: uuid
        in: path
        required: true
        description: UUID of a pipeline.
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
    pipeline = find_pipeline(pipeline_uuid)
    if pipeline is None:
        return {"message": "Pipeline not found"}, 404

    return jsonify(PipelineSchema().dump(pipeline))


@pipeline_bp.route("/<pipeline_uuid>", methods=["DELETE"])
@verify_content_type_and_params([], [])
@permissions_required([SystemPermissionEnum.PIPELINES_CLIENT])
def remove(pipeline_uuid):
    """Delete a pipeline.
    ---
    tags:
      - pipelines
    parameters:
      - in: header
        name: Workflow-API-Key
        description: Requires key type PIPELINES_CLIENT
        schema:
          type: string
      - name: uuid
        in: path
        required: true
        description: UUID of a pipeline.
    responses:
      "200":
        description: "Deleted"
      "400":
        description: "Bad request"
    """
    try:
        delete_pipeline(pipeline_uuid)
        return {}, 200
    except ValueError:
        return {
            "message": "Unable to delete workflow",
        }, 400


@pipeline_bp.route("", methods=["GET"])
@verify_content_type_and_params([], [])
@permissions_required([SystemPermissionEnum.PIPELINES_CLIENT])
def list_pipelines():
    """List all pipelines.
    ---
    tags:
      - pipelines
    parameters:
      - in: header
        name: Workflow-API-Key
        description: Requires key type PIPELINES_CLIENT
        schema:
          type: string
    responses:
      "200":
        description: "Listed"
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
    pipelines = find_pipelines()
    return jsonify([PipelineSchema().dump(p) for p in pipelines])


@pipeline_bp.route("/<pipeline_uuid>", methods=["PUT"])
@verify_content_type_and_params(
    [
        "name",
        "description",
        "docker_image_url",
        "repository_ssh_url",
        "repository_branch",
    ],
    [],
)
@permissions_required([SystemPermissionEnum.PIPELINES_CLIENT])
def update(pipeline_uuid):
    """Update a pipeline.
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
    name = request.json["name"]
    description = request.json["description"]
    docker_image_url = request.json["docker_image_url"]
    repository_ssh_url = request.json["repository_ssh_url"]
    repository_branch = request.json["repository_branch"]
    try:
        pipeline = update_pipeline(
            pipeline_uuid,
            name,
            description,
            docker_image_url,
            repository_ssh_url,
            repository_branch,
        )
        db.session.commit()

        return jsonify(PipelineSchema().dump(pipeline))
    except ValueError:
        return {"message": "Unable to update pipeline"}, 400


@pipeline_bp.route("/search", methods=["POST"])
@verify_content_type_and_params(["uuids"], [])
@permissions_required([SystemPermissionEnum.PIPELINES_CLIENT])
def search():
    """Search for pipelines with specific UUIDs.
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
                value: { "message": "An error", "errors": { "name": "invalid uuid format" } }
                summary: An error with validation messages.
    """
    try:
        pipelines = find_pipelines(request.json)

        return jsonify([PipelineSchema().dump(p) for p in pipelines])
    except ValidationError as ve:
        return {"message": "Unable to search pipeline", "errors": ve.messages}, 400
