from logging import INFO, basicConfig, getLogger
from typing import Union
from flask import Flask, request

from .constants import (
    INTERNAL_SERVER_ERROR_EXAMPLE,
    QUESTIONNAIRE_RESPONSE__SUCCESS,
    RELATED__LIST_RELATIONSHIP,
    RELATED__LIST_RELATIONSHIP_WITH_INCLUDE,
    RELATED__VERIFY_RELATIONSHIP_09,
    RELATED__VERIFY_RELATIONSHIP_09_WITH_INCLUDE,
    RELATED__VERIFY_RELATIONSHIP_25,
    RELATED__VERIFY_RELATIONSHIP_25_WITH_INCLUDE,
    POST_CONSENT__SUCCESS,
    POST_CONSENT__DUPLICATE_RELATIONSHIP_ERROR,
    POST_CONSENT__INVALID_ACCESS_LEVEL_ERROR,
    POST_CONSENT__INVALID_EVIDENCE_ERROR,
    POST_CONSENT__INVALID_PATIENT_AGE_ERROR,
    POST_CONSENT__PERFORMER_IDENTIFIER_ERROR,
)
from .get_consent import get_consent_response
from .utils import (
    check_for_empty,
    check_for_list,
    check_for_related_person_errors,
    check_for_validate,
    generate_response_from_example,
    remove_system,
)

app = Flask(__name__)
basicConfig(level=INFO, format="%(asctime)s - %(message)s")
logger = getLogger(__name__)
APP_BASE_PATH = "https://sandbox.api.service.nhs.uk/validated-relationships/FHIR/R4/Consent"
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

    try:
        # Check Headers
        if errors := check_for_related_person_errors(request):
            return errors

        identifier = remove_system(request.args.get("identifier"))
        patient_identifier = remove_system(request.args.get("patient:identifier"))
        include = request.args.get("_include")

        if empty := check_for_empty(identifier, patient_identifier):
            return empty

        # Successful request, select response
        if zero_nine := check_for_validate(
            "9000000009",
            identifier,
            patient_identifier,
            include,
            RELATED__VERIFY_RELATIONSHIP_09,
            RELATED__VERIFY_RELATIONSHIP_09_WITH_INCLUDE,
        ):
            return zero_nine

        if two_five := check_for_validate(
            "9000000025",
            identifier,
            patient_identifier,
            include,
            RELATED__VERIFY_RELATIONSHIP_25,
            RELATED__VERIFY_RELATIONSHIP_25_WITH_INCLUDE,
        ):
            return two_five

        if one_seven := check_for_list(
            "9000000017",
            identifier,
            include,
            RELATED__LIST_RELATIONSHIP,
            RELATED__LIST_RELATIONSHIP_WITH_INCLUDE,
        ):
            return one_seven

        raise ValueError("Invalid request")

    except Exception:
        logger.exception("GET related person failed")
        return generate_response_from_example(INTERNAL_SERVER_ERROR_EXAMPLE, 500)


@app.route(f"/{COMMON_PATH}/QuestionnaireResponse", methods=["POST"])
def post_questionnaire_response() -> Union[dict, tuple]:
    """Sandbox API for POST /QuestionnaireResponse

    Returns:
        Union[dict, tuple]: Response for POST /QuestionnaireResponse
    """

    try:
        return generate_response_from_example(QUESTIONNAIRE_RESPONSE__SUCCESS, 200)
    except Exception:
        logger.exception("POST questionnaire response failed")
        return generate_response_from_example(INTERNAL_SERVER_ERROR_EXAMPLE, 500)


@app.route(f"/{COMMON_PATH}/Consent", methods=["GET"])
def get_consent() -> Union[dict, tuple]:
    """Sandbox API for GET /Consent

    Returns:
        Union[dict, tuple]: Response for GET /Consent
    """
    return get_consent_response()


@app.route(f"/{COMMON_PATH}/Consent", methods=["POST"])
def post_consent() -> Union[dict, tuple]:
    """Sandbox API for POST /Consent

    Returns:
        Union[dict, tuple]: Response for POST /Consent
    """
    try:
        logger.debug("Received request to POST consent")
        # Validate body - beyond the scope of sandbox - assume body is valid for scenario
        json = request.get_json()
        patient_identifier = json["performer"][0]["identifier"]["value"]
        response = None

        # Successful parent-child proxy creation
        # Successful adult-adult proxy creation
        if patient_identifier == "9000000009" or patient_identifier == "9000000017":
            header = {"location": f"{APP_BASE_PATH}/{patient_identifier}"}
            response = generate_response_from_example(POST_CONSENT__SUCCESS, 201, headers=header)

        # Invalid access level
        elif patient_identifier == "9000000025":
            response = generate_response_from_example(POST_CONSENT__INVALID_ACCESS_LEVEL_ERROR, 403)

        # Missing required evidence
        elif patient_identifier == "9000000033":
            response = generate_response_from_example(POST_CONSENT__INVALID_EVIDENCE_ERROR, 422)

        # Patient age validation failure
        elif patient_identifier == "9000000041":
            response = generate_response_from_example(POST_CONSENT__INVALID_PATIENT_AGE_ERROR, 422)

        # Duplicate relationship
        elif patient_identifier == "9000000049":
            response = generate_response_from_example(POST_CONSENT__DUPLICATE_RELATIONSHIP_ERROR, 409)

        # Invalid performer NHS number
        elif patient_identifier == "9000000000":
            response = generate_response_from_example(POST_CONSENT__PERFORMER_IDENTIFIER_ERROR, 422)

        else:
            # Out of scope errors
            raise ValueError("Invalid Request")

        return response

    except Exception:
        # Handle any general error
        logger.exception("POST Consent failed")
        return generate_response_from_example(INTERNAL_SERVER_ERROR_EXAMPLE, 500)
