"""For gunicorn running"""

import logging

from backend.app import create_app

socket, app = create_app()


gunicorn_logger = logging.getLogger("gunicorn.error")
app.logger.handlers = gunicorn_logger.handlers
app.logger.setLevel(gunicorn_logger.level)
