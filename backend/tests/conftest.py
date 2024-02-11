import pytest

from backend.app import create_app


@pytest.fixture()
def app():
    _, app = create_app()
    app.config.update({"TESTING": True})

    yield app


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def runner(app):
    return app.test_cli_runner()
