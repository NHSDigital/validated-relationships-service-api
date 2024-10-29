from json import load, dumps
from typing import Optional, Any

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
    identifier = request.args.get("identifier")
    identifier_without_system = remove_system(request.args.get("identifier"))

    if not identifier:
        return (
            load_json_file(
                "./api/responses/GET_RelatedPerson/bad_request_identifier_missing.json"
            ),
            400,
        )
    elif identifier and len(identifier_without_system) != 10:
        # invalid identifier
        return (
            load_json_file(
                "./api/responses/GET_RelatedPerson/bad_request_identifier_invalid.json"
            ),
            400,
        )
    elif (
        isinstance(identifier, str)
        and "|" in identifier
        and "https://fhir.nhs.uk/Id/nhs-number" != identifier.split("|", maxsplit=2)[0]
    ):
        # invalid identifier system
        return (
            load_json_file(
                "./api/responses/GET_RelatedPerson/bad_request_identifier_invalid_system.json"
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
    base_file: str,
    inc_file: str,
) -> Response:
    """Checks for validate request responses for a given relationship record

    Args:
        value (str): NHS number of the relationship to look for
        identifier (str): The identifier supplied to the request
        patient_identifier (str): The patient:identifier supplied to the request
        include (str): The include parameter supplied to the request
        base_file (str): The file to return when record matches but does not request included data
        inc_file (str): The file to return when record matches and does request included data

    Returns:
        Response: Resultant response or None
    """
    if identifier and patient_identifier == value and include == INCLUDE_FLAG:
        # Request with identifier, patient and _include=patient
        return generate_response(load_json_file(inc_file))
    elif identifier and patient_identifier == value:
        # Request with identifier and patient
        return generate_response(load_json_file(base_file))


def check_for_list(
    value: str, identifier: str, include: str, base_file: str, inc_file: str
) -> Response:
    """Check for a list relationship response for a given NHS number

    Args:
        value (str): NHS number of the relationship to look for
        identifier (str): The identifier supplied to the request
        include (str): The include parameter supplied to the request
        base_file (str): The file to return when record matches but does not request included data
        inc_file (str): The file to return when record matches and does request included data

    Returns:
        Response: Resultant response or None
    """
    if identifier == value and include == INCLUDE_FLAG:
        # Request with identifier and _include=patient
        return generate_response(load_json_file(inc_file))
    elif identifier:
        # Request with identifier
        return generate_response(load_json_file(base_file))


def generate_response(content: str, status: int = 200):
    """Creates a response object with the supplied data and content type of "application/fhir+json"

    Args:
        content (json): The content for the response
        status (int, optional): The status header of the response. Defaults to 200.

    Returns:
        Response: Resultant Response object based on input.
    """
    return Response(dumps(content), status=status, mimetype="application/fhir+json")


def remove_system(identifier: Any) -> str:
    if isinstance(identifier, str):
        if "|" in identifier:
            # Identifier includes system
            return identifier.split("|", maxsplit=1)[1]
        return identifier
    return ""
