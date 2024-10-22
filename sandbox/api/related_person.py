from .utils import (
    generate_response,
    load_json_file,
)

INCLUDE_FLAG = "RelatedPerson:patient"


def determine_success_response(
    identifier: str, patient_identifier: str, include: str
) -> dict:
    """Determines the response for a successful request"""

    if identifier and not patient_identifier:
        # One to one relationship
        response = load_json_file(
            check_for_include(
                include,
                "./api/responses/GET_RelatedPerson/list_relationship.json",
                "./api/responses/GET_RelatedPerson/list_relationship_include.json",
            )
        )
        response = update_value("9000000017", identifier, response)
        return generate_response(response)

    if identifier and patient_identifier:
        # One to many relationship
        response = load_json_file(
            check_for_include(
                include,
                "./api/responses/GET_RelatedPerson/verify_relationship.json",
                "./api/responses/GET_RelatedPerson/verify_relationship_include.json",
            )
        )
        response = update_value("9000000017", identifier, response)
        response = update_value("9000000009", patient_identifier, response)
        return generate_response(response)

    raise ValueError("Invalid request")


def check_for_include(
    include: str, without_include_file: str, with_include_file: str
) -> str:
    """Checks if the include parameter is set to patient and determines the response

    Args:
        include (str): The include parameter supplied to the request
        without_include_file (str): The file to return when record matches but does not request included data
        with_include_file (str): The file to return when record matches and does request included data

    Returns:
        str: The response file to return
    """
    if include == INCLUDE_FLAG:
        return with_include_file
    else:
        return without_include_file


def update_value(from_str: str, to_str: str, response: dict) -> dict:
    """Updates values in the response (can be run recursively)

    Args:
        from_str (str): The string to replace
        to_str (str): The string to replace with
        response (dict): The response to update

    Returns:
        dict: The updated response
    """
    for key, value in response.items():
        if isinstance(value, dict):
            # If the value is a dictionary, call the function recursively
            update_value(value, from_str, to_str)
        elif value == from_str:
            # If the value matches, update it
            response[key] = to_str
        elif isinstance(value, str):
            # Value may be inside a string so replace if in string
            response[key] = value.replace(from_str, to_str)
    return response
