import json
from backend.lib.apispec import get_apispec
from flask import Flask
from flask_socketio import SocketIO

from backend.handlers import health, auth, lots, swagger, websocket
from backend.config import get_config
from backend.services.db import db, migrate
from backend.services.aws import configure_aws
from backend.lib.auth import jwt


def create_app() -> tuple[SocketIO, Flask]:
    app = Flask(__name__)
    config = get_config()
    app.config.from_object(config)

    app.register_blueprint(health.bp)
    app.register_blueprint(auth.bp)
    app.register_blueprint(lots.bp)

    db.init_app(app)
    migrate.init_app(app, db)

    configure_aws(config)
    app.logger.info("AWS service configured")

    jwt.init_app(app)

    @app.route("/swagger")
    def create_swagger_spec():
        return json.dumps(get_apispec(app).to_dict())

    app.register_blueprint(swagger.bp)

    socketio = SocketIO(path="/ws")
    socketio.init_app(app)
    socketio.on_namespace(websocket.BetsLogNamespace("/bets"))

    return socketio, app
