import pytest

from app import create_app, db
from config import TestConfig
from tests.factories import UserFactory


@pytest.fixture
def app():
    app = create_app()
    app.config.from_object(TestConfig)

    with app.app_context():
        yield app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def test_db(app):
    with app.app_context():
        db.create_all()
        yield db
        db.session.remove()
        db.drop_all()


@pytest.fixture(autouse=True)
def setup_default_user(test_db):
    UserFactory.create(id="mocked_user_id")
