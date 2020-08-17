from app import create_app
from flasgger import Swagger


(app, _, _, _) = create_app()
app.config["SWAGGER"] = {
    "title": "Presence Account Service",
    "openapi": "3.0.2",
}
swagger = Swagger(app)


app.run(debug=True)
