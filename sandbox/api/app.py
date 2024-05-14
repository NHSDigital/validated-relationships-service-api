from logging import INFO, basicConfig, getLogger
from typing import Union

from flask import Flask, request

import sandbox.api.utils as utils

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
        if errors := utils.check_for_errors(request):
            return errors

        identifier = request.args.get("identifier")
        patient_identifier = request.args.get("patient:identifier")
        include = request.args.get("_include")

        if empty := utils.check_for_empty(identifier, patient_identifier):
            return empty

        # Successful request, select response
        if zero_nine := utils.check_for_validate(
            "9000000009",
            identifier,
            patient_identifier,
            include,
            utils.VALIDATE_RELATIONSHIP_009,
            utils.VALIDATE_RELATIONSHIP_INCLUDE_009,
        ):
            return zero_nine

        if two_five := utils.check_for_validate(
            "9000000025",
            identifier,
            patient_identifier,
            include,
            utils.VALIDATE_RELATIONSHIP_025,
            utils.VALIDATE_RELATIONSHIP_INCLUDE_025,
        ):
            return two_five

        if one_seven := utils.check_for_list(
            "9000000017",
            identifier,
            include,
            utils.LIST_RELATIONSHIP,
            utils.LIST_RELATIONSHIP_INCLUDE,
        ):
            return one_seven

        raise ValueError("Invalid request")

    except Exception as e:
        logger.error(e)
        return utils.generate_response(utils.load_json_file(utils.ERROR_RESPONSE), 500)
