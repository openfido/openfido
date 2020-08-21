import logging
from functools import wraps

from flask import Blueprint, current_app, g, jsonify, request

from .models import db
from .queries import find_pipeline, find_pipelines, find_pipeline_run
from .services import create_pipeline, create_pipeline_run, delete_pipeline

logger = logging.getLogger("pipelines")

pipeline_bp = Blueprint("pipelines", __name__)


def toISO8601(date):
    """ Return an ISO8601 formatted date """
    return date.isoformat()


def pipeline_to_json(pipeline):
    return {
        "uuid": pipeline.uuid,
        "name": pipeline.name,
        "description": pipeline.description,
        "docker_image_url": pipeline.docker_image_url,
        "repository_ssh_url": pipeline.repository_ssh_url,
        "repository_branch": pipeline.repository_branch,
        "created_at": toISO8601(pipeline.created_at),
        "updated_at": toISO8601(pipeline.updated_at),
    }


def pipeline_run_to_json(pipeline_run):
    return jsonify(
        uuid=pipeline_run.uuid,
        sequence=pipeline_run.sequence,
        created_at=toISO8601(pipeline_run.created_at),
        inputs=[
            {"name": i.filename, "url": i.url,}
            for i in pipeline_run.pipeline_run_inputs
        ],
        states=[
            {"state": s.run_state_type.name, "created_at": toISO8601(s.created_at),}
            for s in pipeline_run.pipeline_run_states
        ],
    )


def verify_content_type_and_params(required_keys, optional_keys):
    """ Decorator enforcing content type and body keys in an endpoint. """

    def decorator(view):
        @wraps(view)
        def wrapper(*args, **kwargs):
            if request.headers.get("Content-Type", None) != "application/json":
                logger.warning("invalid content type")
                return {}, 400

            required_set = set(required_keys)
            optional_set = set(optional_keys)
            if len(required_set) == len(optional_set) == 0:
                return view(*args, **kwargs)

            request_keys = set(request.json.keys())
            if not required_set <= request_keys:
                logger.warning(
                    f"create: invalid payload keys {list(request.json.keys())}, requires {required_keys}",
                )
                return {}, 400
            if len(request_keys - required_set.union(optional_set)) > 0:
                logger.warning("unknown key passed to request")
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


@pipeline_bp.route("/<pipeline_uuid>", methods=["GET"])
@verify_content_type_and_params([], [])
def get(pipeline_uuid):
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
    pipeline = find_pipeline(pipeline_uuid)
    if pipeline is None:
        return {}, 404

    return jsonify(pipeline_to_json(pipeline))


@pipeline_bp.route("/<pipeline_uuid>", methods=["DELETE"])
@verify_content_type_and_params([], [])
def remove(pipeline_uuid):
    """ Delete a pipeline.
    ---
    parameters:
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
        return {}, 400


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


@pipeline_bp.route("/<pipeline_uuid>/runs", methods=["POST"])
@verify_content_type_and_params(["inputs"], [])
def create_run(pipeline_uuid):
    """Create a new pipeline run.
    ---

    requestBody:
      description: "A list of inputs"
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              items:
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
    # Validate the input fields are all strings and only have name/url in
    # them
    inputs = request.json["inputs"]
    if not isinstance(inputs, list):
        return {}, 400
    for i in inputs:
        allowed_keys = set(["name", "url"])
        if set(i.keys()) != allowed_keys:
            return {}, 400

    try:
        pipeline_run = create_pipeline_run(pipeline_uuid, inputs)
        db.session.commit()

        return pipeline_run_to_json(pipeline_run)
    except ValueError:
        return {}, 400


@pipeline_bp.route("/<pipeline_uuid>/runs/<pipeline_run_uuid>", methods=["GET"])
def get_run(pipeline_uuid, pipeline_run_uuid):
    """ Get a pipeline run.
    ---
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
    pipeline = find_pipeline(pipeline_uuid)
    if pipeline is None:
        return {}, 404

    pipeline_run = find_pipeline_run(pipeline_run_uuid)
    if pipeline_run is None:
        return {}, 404

    return pipeline_run_to_json(pipeline_run)
