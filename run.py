from flasgger import Swagger

from app import create_app

(app, _, _) = create_app()
app.config["SWAGGER"] = {
    "title": "OpenFIDO app service",
    "description": "The main OpenFIDO service.",
    "openapi": "3.0.3",
    "doc_dir": "docs/swagger/",
}
swagger = Swagger(app)


app.run(debug=True)
