from json import load
from typing import Optional

from flask import request


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
