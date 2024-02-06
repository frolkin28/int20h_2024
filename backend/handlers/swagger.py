from flask_swagger_ui import get_swaggerui_blueprint

SWAGGER_URL = "/docs"
API_URL = "/swagger"

bp = get_swaggerui_blueprint(
    SWAGGER_URL, API_URL, config={"app_name": "INT20H api docs"}
)
