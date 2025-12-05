import pytest

# Denne antager at du har 'app = Flask(__name__)' i api/app.py
from api.app import app as flask_app


@pytest.fixture
def app():
    """Konfigurer Flask app til test-mode."""
    flask_app.config.update(
        {
            "TESTING": True
        }
    )
    yield flask_app


@pytest.fixture
def client(app):
    """Flask test-klient fixture."""
    return app.test_client()
