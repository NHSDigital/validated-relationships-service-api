from json import dumps, load
from logging import getLogger
from typing import Any, List, Optional

from flask import Request, Response
from yaml import CLoader as Loader
from yaml import load as yaml_load

from .constants import (
    BAD_REQUEST_INCLUDE_PARAM_INVALID,
    CONSENT_PATIENT,
    CONSENT_PERFORMER,
    GET_CONSENT__STATUS_PARAM_INVALID,
    INCLUDE_FLAG,
    INTERNAL_SERVER_ERROR_EXAMPLE,
    INVALIDATED_RESOURCE,
    PATIENT_IDENTIFIERS,
    RELATED__EMPTY_RESPONSE,
    RELATED__ERROR_IDENTIFIER,
    RELATED__ERROR_IDENTIFIER_MISSING,
    RELATED__ERROR_IDENTIFIER_SYSTEM,
    RELATED_IDENTIFIERS,
)

FHIR_MIMETYPE = "application/fhir+json"
logger = getLogger(__name__)


def load_json_file(file_name: str) -> dict:
    """Get response from file. Expected file content is a JSON."""
    with open(file_name, "r") as file:
        return load(file)


def check_for_get_related_person_errors(request: Request) -> Optional[tuple]:
    """Check for errors in the request headers and arguments for a Get /Related Person request

    Args:
        request (Request): Flask request object

    Returns:
        Optional[tuple]: Tuple with response and status code if error is found
    """
    identifier = request.args.get("identifier")
    patient = request.args.get("patient:identifier")
    identifier_without_system = remove_system(request.args.get("identifier"))
    patient_without_system = remove_system(request.args.get("patient:identifier"))

    if not identifier and not patient:
        return generate_response_from_example(RELATED__ERROR_IDENTIFIER_MISSING, 400)
    elif identifier and len(identifier_without_system) != 10:
        # invalid identifier
        return generate_response_from_example(RELATED__ERROR_IDENTIFIER, 400)
    elif (
        isinstance(identifier, str)
        and "|" in identifier
        and "https://fhir.nhs.uk/Id/nhs-number" == identifier.split("|", maxsplit=2)[0]
    ):
        # invalid identifier system
        return generate_response_from_example(RELATED__ERROR_IDENTIFIER_SYSTEM, 400)


GET_CONSENT_ERRORS = "./api/examples/GET_Consent/errors"


def check_for_get_consent_errors(request: Request) -> Optional[tuple]:
    """Check for errors in the request headers and arguments for a GET /Consent request

    Args:
        request (Request): Flask request object

    Returns:
        Optional[tuple]: Tuple with response and status code if error is found
    """
    performer_identifier = request.args.get("performer:identifier")
    patient_identifier = request.args.get("patient:identifier")

    if not performer_identifier and not patient_identifier:
        return generate_response_from_example("./api/examples/GET_Consent/errors/missing-identifier.yaml", 400)

    for identifier in [performer_identifier, patient_identifier]:
        identifier_without_system = remove_system(identifier)

        if identifier and len(identifier_without_system) != 10:
            # invalid identifier
            return generate_response_from_example("./api/examples/GET_Consent/errors/invalid-identifier.yaml", 422)
        elif (
            isinstance(identifier, str)
            and "|" in identifier
            and "https://fhir.nhs.uk/Id/nhs-number" == identifier.split("|", maxsplit=2)[0]
        ):
            # invalid identifier system
            return generate_response_from_example(
                "./api/examples/GET_Consent/errors/invalid-identifier-system.yaml",
                422,
            )
        elif identifier_without_system == "9000000012":
            # invalid status
            return generate_response_from_example(f"{GET_CONSENT_ERRORS}/gp-practice-not-found.yaml", 404)


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
        return generate_response_from_example(INVALIDATED_RESOURCE, 404)
    elif patient_identifier and (patient_identifier not in RELATED_IDENTIFIERS):
        # Request with patient:identifier - but its not in a list of identifiers
        return generate_response_from_example(INVALIDATED_RESOURCE, 404)
    elif identifier == "9000000033":
        # Request with identifier for empty record
        return generate_response_from_example(RELATED__EMPTY_RESPONSE, 200)


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
        return generate_response_from_example(inc_file, 200)
    elif identifier and patient_identifier == value:
        # Request with identifier and patient
        return generate_response_from_example(base_file, 200)


def check_for_list(value: str, identifier: str, include: str, base_file: str, inc_file: str) -> Response:
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
        return generate_response_from_example(inc_file, 200)
    elif identifier:
        # Request with identifier
        return generate_response_from_example(base_file, 200)


def generate_response(content: str, status: int = 200):
    """Creates a response object with the supplied data and content type of "application/fhir+json"

    Args:
        content (json): The content for the response
        status (int, optional): The status header of the response. Defaults to 200.

    Returns:
        Response: Resultant Response object based on input.
    """
    return Response(dumps(content), status=status, mimetype=FHIR_MIMETYPE)


def remove_system(identifier: Any) -> str:
    """Removes the system from an identifier if it exists

    Args:
        identifier (Any): Identifier to remove system from

    Returns:
        str: Identifier without system
    """
    if isinstance(identifier, str):
        if "|" in identifier:
            # Identifier includes system
            return identifier.split("|", maxsplit=1)[1]
        return identifier
    return ""


def generate_response_from_example(example_path: str, status_code: int, headers: dict = None) -> Response:
    """Converts an example file (yaml) to a response

    Args:
        example_path (str): Path to the example file
        status_code (int): Status code for the response

    Returns:
        response: Resultant Response object based on input.
    """
    with open(example_path, "r") as file:
        content = yaml_load(file, Loader)
    # Value of response is always in the first key, then within value
    content = content[list(content.keys())[0]]["value"]
    return Response(
        dumps(content),
        status=status_code,
        mimetype=FHIR_MIMETYPE,
        headers=headers,
    )


def check_for_consent_include_params(
    _include: List[str],
    include_none_response_yaml: str,
    include_both_response_yaml: str,
    include_patient_response_yaml: str = None,
    include_performer_response_yaml: str = None,
) -> Response:
    """Checks the GET consent request include params and provides the related response

    Args:
        _include (List[str]): The include parameters supplied to the request
        include_none_response_yaml (str): Bundle to return when include params are empty
        include_both_response_yaml (str): Bundle to return when include param is Consent:performer,Consent:patient
        include_patient_response_yaml (str): (optional) Bundle to return when include param is Consent:patient
        include_performer_response_yaml (str): (optional) Bundle to return when include param is Consent:performer

    Returns:
        response: Resultant Response object based on input.
    """
    if _include == [] or _include is None:
        return generate_response_from_example(include_none_response_yaml, 200)
    elif _include == [CONSENT_PERFORMER]:
        if include_performer_response_yaml:
            return generate_response_from_example(include_performer_response_yaml, 200)
        else:
            logger.error("No consent performer example provided")
            return generate_response_from_example(INTERNAL_SERVER_ERROR_EXAMPLE, 500)
    elif _include == [CONSENT_PATIENT]:
        if include_patient_response_yaml:
            return generate_response_from_example(include_patient_response_yaml, 200)
        else:
            logger.error("No consent:patient example provided")
            return generate_response_from_example(INTERNAL_SERVER_ERROR_EXAMPLE, 500)
    elif len(_include) == 2 and CONSENT_PATIENT in _include and CONSENT_PERFORMER in _include:
        return generate_response_from_example(include_both_response_yaml, 200)
    else:
        return generate_response_from_example(BAD_REQUEST_INCLUDE_PARAM_INVALID, 422)


def check_for_consent_filtering(
    status: List[str],
    _include: List[str],
    status_active_with_details_response_yaml: str,
    status_inactive_response_yaml: str,
    status_proposed_and_active_response_yaml: str,
) -> Response:
    """Checks the GET consent request status params and provides related response

    Args:
        status (List[str]): The status parameters supplied to the request
        _include (List[str]): The include parameters supplied to the request
        status_active_with_details_response_yaml (str): Bundle to return when status param is 'active'
        status_inactive_response_yaml (str): Bundle to return when status param is 'inactive'
        status_proposed_and_active_response_yaml (str): Bundle to return when status param is 'proposed,inactive'

    Returns:
        response: Resultant Response object based on input.
    """
    if status == [] or status is None:
        return generate_response_from_example(INVALIDATED_RESOURCE, 404)
    if status == ["active"]:
        if len(_include) == 2 and CONSENT_PERFORMER in _include and CONSENT_PERFORMER in _include:
            return generate_response_from_example(status_active_with_details_response_yaml, 200)
        else:
            return generate_response_from_example(INVALIDATED_RESOURCE, 404)
    elif status == ["inactive"]:
        return generate_response_from_example(status_inactive_response_yaml, 200)
    elif len(status) == 2 and "active" in status and "proposed" in status:
        return generate_response_from_example(status_proposed_and_active_response_yaml, 200)
    else:
        return generate_response_from_example(GET_CONSENT__STATUS_PARAM_INVALID, 422)
