import pytest

from ..app import app
RELATED_PERSON_API_ENDPOINT = "/FHIR/R4/RelatedPerson"

@pytest.fixture()
def client() -> object:
    """Create a test client for the app."""
    return app.test_client()
