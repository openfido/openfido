import logging
from functools import wraps

from flask import Blueprint, current_app, g, jsonify, request

from .models import db
from .queries import find_pipeline, find_pipelines
from .services import create_pipeline

logger = logging.getLogger("pipelines")

pipeline_bp = Blueprint("pipelines", __name__)


def pipeline_to_json(pipeline):
    return {
        "uuid": pipeline.uuid,
        "name": pipeline.name,
        "description": pipeline.description,
        "docker_image_url": pipeline.docker_image_url,
        "repository_ssh_url": pipeline.repository_ssh_url,
        "repository_branch": pipeline.repository_branch,
        "created_at": pipeline.created_at,
        "updated_at": pipeline.updated_at,
    }


def verify_content_type_and_params(required_keys, optional_keys):
    """ Decorator enforcing content type and body keys in an endpoint. """

    def decorator(view):
        @wraps(view)
        def wrapper(*args, **kwargs):
            if request.headers.get("Content-Type", None) != "application/json":
                logger.warn("invalid content type")
                return {}, 400

            required_set = set(required_keys)
            optional_set = set(optional_keys)
            if len(required_set) == len(optional_set) == 0:
                return view(*args, **kwargs)

            request_keys = set(request.json.keys())
            if not required_set <= request_keys:
                logger.warn(
                    f"create: invalid payload keys {list(request.json.keys())}, requires {required_keys}",
                )
                return {}, 400
            if len(request_keys - required_set.union(optional_set)) > 0:
                logger.warn("unknown key passed to request")
                return {}, 400

            return view(*args, **kwargs)

        return wrapper

    return decorator


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
def create():
    """ Create a pipeline.
    ---

    requestBody:
      description: "Pipeline description and configuration."
      required: true
      content:
        application/json:
          schema:
            type: object
            required:
              - password
              - reset_token
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

        return jsonify(pipeline_to_json(pipeline))
    except ValueError:
        return {}, 400


@pipeline_bp.route("/<uuid>", methods=["GET"])
@verify_content_type_and_params([], [])
def get(uuid):
    """ Get a pipeline.
    ---
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
    pipeline = find_pipeline(uuid)
    if pipeline is None:
        return {}, 404

    return jsonify(pipeline_to_json(pipeline))


@pipeline_bp.route("", methods=["GET"])
@verify_content_type_and_params([], [])
def list_pipelines():
    """ List all pipelines.
    ---
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
    return jsonify(list(map(pipeline_to_json, pipelines)))
