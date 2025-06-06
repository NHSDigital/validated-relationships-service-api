from logging import INFO, basicConfig, getLogger
from typing import Union

from flask import Flask

from .get_consent import get_consent_response
from .get_consent_by_id import get_consent_by_id_response
from .get_questionnaire_response import get_questionnaire_response_response
from .get_related_person import get_related_person_response
from .patch_consent import patch_consent_response
from .post_consent import post_consent_response
from .post_questionnaire_response import post_questionnaire_response_response

app = Flask(__name__)
basicConfig(level=INFO, format="%(asctime)s - %(message)s")
logger = getLogger(__name__)

COMMON_PATH = "FHIR/R4"


@app.route("/_status", methods=["GET"])
@app.route("/_ping", methods=["GET"])
@app.route("/health", methods=["GET"])
def health() -> dict:
    """Health check endpoint"""
    return {
        "status": "online",
        "message": "Validated Relationships Service Sandbox is running",
    }


@app.route(f"/{COMMON_PATH}/RelatedPerson", methods=["GET"])
def get_related_persons() -> Union[dict, tuple]:
    """Sandbox API for GET /RelatedPerson

    Returns:
        Union[dict, tuple]: Response for GET /RelatedPerson
    """
    return get_related_person_response()


@app.route(f"/{COMMON_PATH}/QuestionnaireResponse", methods=["GET"])
def get_questionnaire_response() -> Union[dict, tuple]:
    """Sandbox API for GET /QuestionnaireResponse

    Returns:
        Union[dict, tuple]: Response for GET /QuestionnaireResponse
    """
    return get_questionnaire_response_response()


@app.route(f"/{COMMON_PATH}/QuestionnaireResponse", methods=["POST"])
def post_questionnaire_response() -> Union[dict, tuple]:
    """Sandbox API for POST /QuestionnaireResponse

    Returns:
        Union[dict, tuple]: Response for POST /QuestionnaireResponse
    """
    return post_questionnaire_response_response()


@app.route(f"/{COMMON_PATH}/Consent", methods=["GET"])
def get_consent() -> Union[dict, tuple]:
    """Sandbox API for GET /Consent

    Returns:
        Union[dict, tuple]: Response for GET /Consent
    """
    return get_consent_response()


@app.route(f"/{COMMON_PATH}/Consent/<identifier>", methods=["GET"])
def get_consent_by_id(identifier: str) -> Union[dict, tuple]:
    """Sandbox API for GET /Consent/{id}

    Returns:
        Union[dict, tuple]: Response for GET /Consent/{id}
    """
    return get_consent_by_id_response(identifier)


@app.route(f"/{COMMON_PATH}/Consent", methods=["POST"])
def post_consent() -> Union[dict, tuple]:
    """Sandbox API for POST /Consent

    Returns:
        Union[dict, tuple]: Response for POST /Consent
    """
    return post_consent_response()


@app.route(f"/{COMMON_PATH}/Consent/<identifier>", methods=["PATCH"])
def patch_consent(identifier: str) -> Union[dict, tuple]:
    """Sandbox API for PATCH /Consent

    Args:
        identifier (str): Consent identifier to be patched

    Returns:
        Union[dict, tuple]: Response for PATCH /Consent
    """
    return patch_consent_response(identifier)
