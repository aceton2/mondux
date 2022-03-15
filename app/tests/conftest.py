import pytest
import os
from flaskr import create_app


@pytest.fixture
def app():

    app = create_app({
        'TESTING': True,
        'DATABASE': {
            'database': os.getenv("API_TEST_DB"),
            'user': os.getenv("API_DB_USER"),
            'password': os.getenv("API_DB_PASSWORD"),
            'host': os.getenv("API_DB_HOST")
        }
    })

    yield app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()
