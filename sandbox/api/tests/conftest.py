import pytest

from ..app import app

FHIR_PATH = "/FHIR/R4"
RELATED_PERSON_API_ENDPOINT = f"{FHIR_PATH}/RelatedPerson"
QUESTIONNAIRE_RESPONSE_API_ENDPOINT = f"{FHIR_PATH}/QuestionnaireResponse"


@pytest.fixture()
def client() -> object:
    """Create a test client for the app."""
    return app.test_client()
