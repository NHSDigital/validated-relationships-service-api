from logging import INFO, basicConfig, getLogger
from typing import Union

from flask import Flask, request

from .constants import (
    CONSENT__ADULT_CONSENTING_EXAMPLE,
    CONSENT__MIXED_EXAMPLE,
    CONSENT__MOTHER_CHILD_EXAMPLE,
    CONSENT_PERFORMER,
    INTERNAL_ERROR_RESPONSE,
    INTERNAL_SERVER_ERROR_EXAMPLE,
    LIST_RELATIONSHIP,
    LIST_RELATIONSHIP_INCLUDE,
    NOT_FOUND,
    QUESTIONNAIRE_RESPONSE_SUCCESS,
    VALIDATE_RELATIONSHIP_009,
    VALIDATE_RELATIONSHIP_025,
    VALIDATE_RELATIONSHIP_INCLUDE_009,
    VALIDATE_RELATIONSHIP_INCLUDE_025,
)
from .utils import (
    check_for_empty,
    check_for_errors,
    check_for_list,
    check_for_validate,
    generate_response,
    generate_response_from_example,
    load_json_file,
    remove_system,
)

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

    try:
        # Check Headers
        if errors := check_for_errors(request):
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
            VALIDATE_RELATIONSHIP_009,
            VALIDATE_RELATIONSHIP_INCLUDE_009,
        ):
            return zero_nine

        if two_five := check_for_validate(
            "9000000025",
            identifier,
            patient_identifier,
            include,
            VALIDATE_RELATIONSHIP_025,
            VALIDATE_RELATIONSHIP_INCLUDE_025,
        ):
            return two_five

        if one_seven := check_for_list(
            "9000000017",
            identifier,
            include,
            LIST_RELATIONSHIP,
            LIST_RELATIONSHIP_INCLUDE,
        ):
            return one_seven

        raise ValueError("Invalid request")

    except Exception as e:
        logger.error(e)
        return generate_response(load_json_file(INTERNAL_ERROR_RESPONSE), 500)


@app.route(f"/{COMMON_PATH}/QuestionnaireResponse", methods=["POST"])
def post_questionnaire_response() -> Union[dict, tuple]:
    """Sandbox API for POST /QuestionnaireResponse

    Returns:
        Union[dict, tuple]: Response for POST /QuestionnaireResponse
    """

    try:
        return generate_response(load_json_file(QUESTIONNAIRE_RESPONSE_SUCCESS), 200)
    except Exception as e:
        logger.error(e)
        return generate_response(load_json_file(INTERNAL_ERROR_RESPONSE), 500)


@app.route(f"/{COMMON_PATH}/Consent", methods=["GET"])
def get_consent() -> Union[dict, tuple]:
    """Sandbox API for GET /Consent

    Returns:
        Union[dict, tuple]: Response for GET /Consent
    """
    try:
        performer_identifier = remove_system(request.args.get("performer:identifier"))
        status = request.args.get("status")
        _include = request.args.get("_include")

        if (
            performer_identifier == "9000000010"
            and status == "active"
            and _include == CONSENT_PERFORMER
        ):
            return generate_response_from_example(
                CONSENT__ADULT_CONSENTING_EXAMPLE, 200
            )
        elif (
            performer_identifier == "9000000017"
            and status == "active"
            and _include == CONSENT_PERFORMER
        ):
            return generate_response_from_example(CONSENT__MIXED_EXAMPLE, 200)
        elif (
            performer_identifier == "9000000019"
            and status == "active"
            and _include == CONSENT_PERFORMER
        ):
            return generate_response_from_example(CONSENT__MOTHER_CHILD_EXAMPLE, 200)
        else:
            return generate_response(load_json_file(NOT_FOUND), 400)
    except Exception as e:
        logger.error(e)
        return generate_response_from_example(INTERNAL_SERVER_ERROR_EXAMPLE, 500)
