from flask import Flask

from backend.handlers import health
from backend.config import get_config
from backend.services.db import db, migrate


def create_app() -> Flask:
    app = Flask(__name__)
    config = get_config()
    app.config.from_object(config)

    app.register_blueprint(health.bp)
    db.init_app(app)
    migrate.init_app(app)

    return app
