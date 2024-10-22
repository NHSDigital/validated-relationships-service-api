from json import load, dumps
from typing import Optional

from flask import Request, Response

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

QUESTIONNAIRE_RESPONSE_SUCCESS = (
    "./api/responses/POST_QuestionnaireResponse/questionnaire_response_success.json"
)


def load_json_file(file_name: str) -> dict:
    """Get response from file. Expected file content is a JSON."""
    with open(file_name, "r") as file:
        return load(file)


def check_for_errors(request: Request) -> Optional[tuple]:
    """Check for errors in the request headers and arguments

    Args:
        request (Request): Flask request object

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


def generate_response(content: str, status: int = 200):
    """Creates a response object with the supplied data and content type of "application/fhir+json"

    Args:
        content (json): The content for the response
        status (int, optional): The status header of the response. Defaults to 200.

    Returns:
        Response: Resultant Response object based on input.
    """
    return Response(dumps(content), status=status, mimetype="application/fhir+json")
