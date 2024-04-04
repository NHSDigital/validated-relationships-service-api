from logging import INFO, basicConfig, getLogger
from typing import Union

from flask import Flask, request

from .utils import check_for_errors, get_response

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
        # Successful request, select response
        if request.args.get("identifier") and request.args.get("patient"):
            return get_response(
                "./api/responses/GET_RelatedPerson/identifier_and_patient.json"
            )
        elif request.args.get("identifier"):
            return get_response("./api/responses/GET_RelatedPerson/identifier.json")
        else:
            raise ValueError("Invalid request")

    except Exception as e:
        logger.error(e)
        return get_response("./api/responses/internal_server_error.json"), 500
