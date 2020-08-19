import logging
from functools import wraps

from flask import Blueprint, current_app, g, jsonify, request

from .models import db
from .services import create_pipeline_version

logger = logging.getLogger("pipelines")

pipeline_bp = Blueprint("pipelines", __name__)


def verify_content_type_and_params(required_keys, optional_keys):
    """ Decorator enforcing content type and body keys in an endpoint. """

    def decorator(view):
        @wraps(view)
        def wrapper(*args, **kwargs):
            if request.headers.get("Content-Type", None) != "application/json":
                logger.warn("invalid content type")
                return {}, 400

            request_keys = set(request.json.keys())
            required_set = set(required_keys)
            optional_set = set(optional_keys)
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
    ['name',
     'description',
     'version',
     'docker_image_url',
     'repository_ssh_url',
     'repository_branch'], [])
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
              version:
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
                version:
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
                inputs:
                  type: array
                  items:
                    type: object
                    properties:
                      name:
                        type: string
                      description:
                        type: string
                      parameter_name:
                        type: string
                      mime_type:
                        type: string
      "400":
        description: "Bad request"
    """
    name = request.json["name"]
    description = request.json["description"]
    version = request.json["version"]
    docker_image_url = request.json["docker_image_url"]
    repository_ssh_url = request.json["repository_ssh_url"]
    repository_branch = request.json["repository_branch"]
    try:
        pipeline_version = create_pipeline_version(
            name, description, version, docker_image_url, repository_ssh_url, repository_branch)
        db.session.commit()

        pipeline = pipeline_version.pipeline
        return jsonify(
            uuid=pipeline.uuid,
            name=pipeline.name,
            description=pipeline.description,
            version=pipeline_version.version,
            docker_image_url=pipeline.docker_image_url,
            repository_ssh_url=pipeline.repository_ssh_url,
            repository_branch=pipeline.repository_branch,
            created_at=pipeline.created_at,
            updated_at=pipeline.updated_at,
            inputs=[],
        )
    except ValueError:
        return {}, 400
