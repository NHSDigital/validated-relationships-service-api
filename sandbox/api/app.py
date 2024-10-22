from logging import INFO, basicConfig, getLogger
from typing import Union

from flask import Flask, request
from .related_person import determine_success_response
from .utils import (
    ERROR_RESPONSE,
    QUESTIONNAIRE_RESPONSE_SUCCESS,
    EMPTY_RESPONSE,
    check_for_errors,
    generate_response,
    load_json_file,
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

        identifier = request.args.get("identifier", "")
        patient_identifier = request.args.get("patient:identifier", "")
        include = request.args.get("_include", "")

        if identifier == "9000000033":
            # 200 But Empty response
            return generate_response(load_json_file(EMPTY_RESPONSE))

        return determine_success_response(identifier, patient_identifier, include)

    except Exception as e:
        logger.error(e)
        return generate_response(load_json_file(ERROR_RESPONSE), 500)


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
        return generate_response(load_json_file(ERROR_RESPONSE), 500)
