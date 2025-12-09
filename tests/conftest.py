import os
os.environ["TESTING"] = "1"

import pytest
from api.app import app, db


@pytest.fixture
def client():
    # Aktiver Flask test-mode
    app.config["TESTING"] = True
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
    app.config["WTF_CSRF_ENABLED"] = False

    # Opbyg frisk database før test
    with app.app_context():
        db.drop_all()
        db.create_all()

    # Flask test client
    with app.test_client() as client:
        yield client

    # Rydning efter test
    with app.app_context():
        db.session.remove()
        db.drop_all()

