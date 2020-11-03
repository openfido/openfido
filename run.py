from app import create_app
from flasgger import Swagger


(app, _, _) = create_app()
app.config["SWAGGER"] = {
    "title": "OpenFIDO Account Service",
    "description": "The OpenFIDO account microservice",
    "openapi": "3.0.3",
    "doc_dir": "docs/swagger/",
}
swagger = Swagger(app)


app.run(debug=True)
