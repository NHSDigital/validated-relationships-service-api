from logging import INFO, basicConfig, getLogger
from typing import Union
from json import dumps

from flask import Flask, request, Response

from .utils import check_for_errors, load_json_file

NOT_FOUND = "./api/responses/GET_RelatedPerson/not_found.json"
EMPTY_RESPONSE = "./api/responses/GET_RelatedPerson/empty_response_9000000033.json"
LIST_RELATIONSHIP = (
    "./api/responses/GET_RelatedPerson/list_relationship_9000000017.json"
)
LIST_RELATIONSHIP_INCLUDE = (
    "./api/responses/GET_RelatedPerson/list_relationship_include_9000000017.json"
)
VALIDATE_RELATIONSHIP_009 = (
    "./api/responses/GET_RelatedPerson/verify_relationship_9000000009.json"
)
VALIDATE_RELATIONSHIP_INCLUDE_009 = (
    "./api/responses/GET_RelatedPerson/verify_relationship_include_9000000009.json"
)
VALIDATE_RELATIONSHIP_025 = (
    "./api/responses/GET_RelatedPerson/verify_relationship_9000000025.json"
)
VALIDATE_RELATIONSHIP_INCLUDE_025 = (
    "./api/responses/GET_RelatedPerson/verify_relationship_include_9000000025.json"
)
ERROR_RESPONSE = "./api/responses/internal_server_error.json"
INCLUDE_FLAG = "RelatedPerson:patient"

PATIENT_IDENTIFIERS = ["9000000017", "9000000033"]
RELATED_IDENTIFIERS = ["9000000009", "9000000025"]

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

        if empty := __check_for_empty(identifier, patient_identifier):
            return empty

        # Successful request, select response
        if zero_nine := __check_for_validate(
            "9000000009",
            identifier,
            patient_identifier,
            include,
            VALIDATE_RELATIONSHIP_009,
            VALIDATE_RELATIONSHIP_INCLUDE_009,
        ):
            return zero_nine

        if two_five := __check_for_validate(
            "9000000025",
            identifier,
            patient_identifier,
            include,
            VALIDATE_RELATIONSHIP_025,
            VALIDATE_RELATIONSHIP_INCLUDE_025,
        ):
            return two_five

        if one_seven := __check_for_list(
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
        return __generate_response(load_json_file(ERROR_RESPONSE), 500)


def __check_for_empty(identifier: str, patient_identifier: str) -> Response:
    """Checks for not found or empty responses

    Args:
        identifier (str): The identifier supplied to the request
        patient_identifier (str): The patient:identifier supplied to the request

    Returns:
        Response: Resultant response or None
    """
    if identifier and identifier not in PATIENT_IDENTIFIERS:
        # Request with identifier - but its not in a list of identifiers
        return __generate_response(load_json_file(NOT_FOUND), 404)
    elif patient_identifier and (patient_identifier not in RELATED_IDENTIFIERS):
        # Request with patient:identifier - but its not in a list of identifiers
        return __generate_response(load_json_file(NOT_FOUND), 404)
    elif identifier == "9000000033":
        # Request with identifier for empty record
        return __generate_response(load_json_file(EMPTY_RESPONSE))


def __check_for_validate(
    value: str,
    identifier: str,
    patient_identifier: str,
    include: str,
    basefile: str,
    incfile: str,
) -> Response:
    """Checks for validate request responses for a given relationship record

    Args:
        value (str): NHS number of the relationship to look for
        identifier (str): The identifier supplied to the request
        patient_identifier (str): The patient:identifier supplied to the request
        include (str): The include parameter supplied to the request
        basefile (str): The file to return when record matches but does not request includeded data
        incfile (str): The file to return when record matches and does request included data

    Returns:
        Response: Resultant response or None
    """
    if identifier and patient_identifier == value and include == INCLUDE_FLAG:
        # Request with identifier, patient and _include=patient
        return __generate_response(load_json_file(incfile))
    elif identifier and patient_identifier == value:
        # Request with identifier and patient
        return __generate_response(load_json_file(basefile))


def __check_for_list(
    value: str, identifier: str, include: str, basefile: str, incfile: str
) -> Response:
    """Check for a list relationship response for a given NHS number

    Args:
        value (str): NHS number of the relationship to look for
        identifier (str): The identifier supplied to the request
        include (str): The include parameter supplied to the request
        basefile (str): The file to return when record matches but does not request includeded data
        incfile (str): The file to return when record matches and does request included data

    Returns:
        Response: Resultant response or None
    """
    if identifier == value and include == INCLUDE_FLAG:
        # Request with identifier and _include=patient
        return __generate_response(load_json_file(incfile))
    elif identifier:
        # Request with identifier
        return __generate_response(load_json_file(basefile))


def __generate_response(content: str, status: int = 200):
    """Creates a response object with the supplied data and content type of "application/fhir+json"

    Args:
        content (json): The content for the response
        status (int, optional): The status header of the response. Defaults to 200.

    Returns:
        Response: Resultant Response object based on input.
    """
    return Response(dumps(content), status=status, mimetype="application/fhir+json")
