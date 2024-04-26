from logging import INFO, basicConfig, getLogger
from typing import Union

from flask import Flask, request

from .utils import check_for_errors, get_response, get_error

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
        proxy_url = request.args.get("Proxy-URL")

        # Check Headers
        if errors := check_for_errors(request):
            return errors

        # Successful request, select response
        if (
            request.args.get("identifier")
            and request.args.get("patient")
            and request.args.get("_include") == "RelatedPerson:patient"
        ):
            # Request with identifier, patient and _include=patient
            return get_response(
                proxy_url,
                "./api/responses/GET_RelatedPerson/identifier_and_patient_identifier_include.json",
            )
        elif request.args.get("identifier") and request.args.get("patient"):
            # Request with identifier and patient
            return get_response(
                proxy_url,
                "./api/responses/GET_RelatedPerson/identifier_and_patient_identifier.json",
            )
        elif (
            request.args.get("identifier")
            and request.args.get("_include") == "RelatedPerson:patient"
        ):
            # Request with identifier and _include=patient
            return get_response(
                proxy_url, "./api/responses/GET_RelatedPerson/identifier_include.json"
            )
        elif request.args.get("identifier"):
            # Request with identifier
            return get_response(
                proxy_url, "./api/responses/GET_RelatedPerson/identifier.json"
            )
        else:
            raise ValueError("Invalid request")

    except Exception as e:
        logger.error(e)
        return get_error("./api/responses/internal_server_error.json"), 500
