from flasgger import Swagger

from app import create_app

(app, _, _, _) = create_app()
app.config["SWAGGER"] = {
    "title": "Presence Workflow Service",
    "description": (
        "These endpoints define a job queueing API. See " +
        "[the github project](https://github.com/PresencePG/presence-workflow-service) " +
        "for more information"
    ),
    "openapi": "3.0.3",
    "doc_dir": "docs/swagger/",
}
swagger = Swagger(app)


app.run(debug=True)
