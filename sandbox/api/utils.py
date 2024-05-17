from json import load, dumps
from typing import Optional

from flask import request, Response

NOT_FOUND = "./api/responses/not_found.json"
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

QUESTIONNAIRE_RESPONSE_SUCCESS = (
    "./api/responses/POST_QuestionnaireResponse/questionnaire_response_success.json"
)

PATIENT_IDENTIFIERS = ["9000000017", "9000000033"]
RELATED_IDENTIFIERS = ["9000000009", "9000000025"]


def load_json_file(file_name: str) -> dict:
    """Get response from file. Expected file content is a JSON."""
    with open(file_name, "r") as file:
        return load(file)


def check_for_errors(request: request) -> Optional[tuple]:
    """Check for errors in the request headers and arguments

    Args:
        request (request): Flask request object

    Returns:
        Optional[tuple]: Tuple with response and status code if error is found
    """
    if not request.args.get("identifier"):
        return (
            load_json_file(
                "./api/responses/GET_RelatedPerson/bad_request_identifier_missing.json"
            ),
            400,
        )
    elif request.args.get("identifier") and len(request.args.get("identifier")) != 10:
        return (
            load_json_file(
                "./api/responses/GET_RelatedPerson/bad_request_identifier_not_as_expected.json"
            ),
            400,
        )


def check_for_empty(identifier: str, patient_identifier: str) -> Response:
    """Checks for not found or empty responses

    Args:
        identifier (str): The identifier supplied to the request
        patient_identifier (str): The patient:identifier supplied to the request

    Returns:
        Response: Resultant response or None
    """
    if identifier and identifier not in PATIENT_IDENTIFIERS:
        # Request with identifier - but its not in a list of identifiers
        return generate_response(load_json_file(NOT_FOUND), 404)
    elif patient_identifier and (patient_identifier not in RELATED_IDENTIFIERS):
        # Request with patient:identifier - but its not in a list of identifiers
        return generate_response(load_json_file(NOT_FOUND), 404)
    elif identifier == "9000000033":
        # Request with identifier for empty record
        return generate_response(load_json_file(EMPTY_RESPONSE))


def check_for_validate(
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
        return generate_response(load_json_file(incfile))
    elif identifier and patient_identifier == value:
        # Request with identifier and patient
        return generate_response(load_json_file(basefile))


def check_for_list(
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
        return generate_response(load_json_file(incfile))
    elif identifier:
        # Request with identifier
        return generate_response(load_json_file(basefile))


def generate_response(content: str, status: int = 200):
    """Creates a response object with the supplied data and content type of "application/fhir+json"

    Args:
        content (json): The content for the response
        status (int, optional): The status header of the response. Defaults to 200.

    Returns:
        Response: Resultant Response object based on input.
    """
    return Response(dumps(content), status=status, mimetype="application/fhir+json")
