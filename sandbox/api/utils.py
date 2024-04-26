from json import load
from typing import Optional

from flask import request


def get_response(proxy_url: str, file_name: str) -> dict:
    """Get response from file. Expected file content is a JSON.

    Args:
        proxy_url (str): Proxy URL
        file_name (str): File name

    Returns:
        dict: Response from file
    """
    with open(file_name, "r") as file:
        file_contents = load(file)
    return file_contents.replace("{{proxy_url}}", proxy_url)


def get_error(file_name: str) -> dict:
    """Get response from file. Expected file content is a JSON.

    Args:
        file_name (str): File name

    Returns:
        dict: Response from file
    """
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
            get_error(
                "./api/responses/GET_RelatedPerson/bad_request_identifier_missing.json"
            ),
            400,
        )
    elif request.args.get("identifier") and len(request.args.get("identifier")) != 10:
        return (
            get_error(
                "./api/responses/GET_RelatedPerson/bad_request_identifier_not_as_expected.json"
            ),
            400,
        )
