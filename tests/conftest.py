import os
import pytest
from api.app import app, db   # <- korrekt til din struktur

@pytest.fixture
def client():
    # Test mode aktiveret
    app.config["TESTING"] = True

    # Test database
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
        "TEST_DB_URI",
        "mysql+pymysql://flask:iri123@localhost/iridium_test"
    )

    app.config["WTF_CSRF_ENABLED"] = False

    # Reset DB før hver test
    with app.app_context():
        db.drop_all()
        db.create_all()

    # Flask test client
    with app.test_client() as client:
        yield client

    # Ryd DB efter test
    with app.app_context():
        db.session.remove()
        db.drop_all()


