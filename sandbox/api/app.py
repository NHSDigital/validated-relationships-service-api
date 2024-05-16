from logging import INFO, basicConfig, getLogger
from typing import Union

from flask import Flask, request

from .utils import (
    VALIDATE_RELATIONSHIP_009,
    VALIDATE_RELATIONSHIP_INCLUDE_009,
    VALIDATE_RELATIONSHIP_025,
    VALIDATE_RELATIONSHIP_INCLUDE_025,
    LIST_RELATIONSHIP,
    LIST_RELATIONSHIP_INCLUDE,
    ERROR_RESPONSE,
    check_for_errors,
    check_for_empty,
    check_for_validate,
    check_for_list,
    generate_response,
    load_json_file,
)

app = Flask(__name__)
basicConfig(level=INFO, format="%(asctime)s - %(message)s")
logger = getLogger(__name__)


@app.route("/_status", methods=["GET"])
@app.route("/_ping", methods=["GET"])
@app.route("/health", methods=["GET"])
def health() -> dict:
    """Health check endpoint"""
    return {
        "status": "online",
        "message": "Validated Relationships Service Sandbox is running",
    }


@app.route("/FHIR/R4/RelatedPerson", methods=["GET"])
def get_related_persons() -> Union[dict, tuple]:
    """Sandbox API for GET /RelatedPerson

    Returns:
        Union[dict, tuple]: Response for GET /RelatedPerson
    """

    try:
        # Check Headers
        if errors := check_for_errors(request):
            return errors

        identifier = request.args.get("identifier")
        patient_identifier = request.args.get("patient:identifier")
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
        return generate_response(load_json_file(ERROR_RESPONSE), 500)
