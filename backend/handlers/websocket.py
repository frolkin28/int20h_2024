from flask import current_app
from flask_socketio import Namespace


class BetsLogNamespace(Namespace):
    def on_connect(self):
        current_app.logger.info('Client connected')

    def on_disconnect(self):
        current_app.logger.info('Client disconnected')

    def on_message(self, data):
        current_app.logger.info('Message received:', data)
        self.emit('response', {'message': 'Server received your message'})
