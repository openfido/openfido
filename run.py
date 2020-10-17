from app import create_app
from flasgger import Swagger


(app, _, _) = create_app()
app.config["SWAGGER"] = {
    "title": "OpenFIDO Account Service",
    "openapi": "3.0.2",
}
swagger = Swagger(app)


app.run(debug=True)
