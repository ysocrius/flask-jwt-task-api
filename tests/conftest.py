import pytest
import sys
import os

# Ensure src/backend is in the Python path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src/backend')))

from app import create_app
from models import db

@pytest.fixture(scope="function")
def app():
    """Create and configure a test app instance."""
    # Use the testing configuration defined in src/backend/config.py
    app = create_app(config_name="testing")

    # Tables are created in factory with app.app_context()
    # But we'll ensure a clean session for each test
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture(scope="function")
def client(app):
    """A test client for making requests."""
    return app.test_client()
