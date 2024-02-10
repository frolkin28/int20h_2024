"""For gunicorn running"""

import logging

from dotenv import load_dotenv

from backend.app import create_app


load_dotenv()

socket, app = create_app()

gunicorn_logger = logging.getLogger("gunicorn.error")
app.logger.handlers = gunicorn_logger.handlers
app.logger.setLevel(gunicorn_logger.level)
