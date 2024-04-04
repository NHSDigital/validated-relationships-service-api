import pytest

from ..app import app


@pytest.fixture()
def client() -> object:
    """Create a test client for the app."""
    return app.test_client()
