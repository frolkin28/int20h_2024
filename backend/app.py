import json
from apispec import APISpec
from backend.lib.apispec import get_apispec
from flask import Flask
from flask_jwt_extended import JWTManager

from backend.handlers import health, auth, swagger
from backend.config import get_config
from backend.services.db import db, migrate


def create_app() -> Flask:
    app = Flask(__name__)
    app.config.from_object(get_config())

    app.register_blueprint(health.bp)
    app.register_blueprint(auth.bp)

    db.init_app(app)
    migrate.init_app(app, db)
    jwt_manager = JWTManager()
    jwt_manager.init_app(app)

    @app.route("/swagger")
    def create_swagger_spec():
        return json.dumps(get_apispec(app).to_dict())

    app.register_blueprint(swagger.bp)

    return app
