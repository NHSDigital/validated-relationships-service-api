from typing import Any, Optional

from .utils import generate_response, load_json_file, EMPTY_RESPONSE

INCLUDE_FLAG = "RelatedPerson:patient"


def special_cases(identifier: str) -> Optional[dict]:
    """Determines if the identifier is a special case"""
    if identifier == "9000000033":
        # 200 But Empty response
        return generate_response(load_json_file(EMPTY_RESPONSE))


def determine_success_response(
    identifier: str, patient_identifier: str, include: str
) -> dict:
    """Determines the response for a successful request"""

    if identifier and not patient_identifier:
        # One to many
        response = load_json_file(
            check_for_include(
                include,
                "./api/responses/GET_RelatedPerson/list_relationship.json",
                "./api/responses/GET_RelatedPerson/list_relationship_include.json",
            )
        )
        response = update_values("9000000017", identifier, response)
        return generate_response(response)

    if identifier and patient_identifier:
        # One to one
        response = load_json_file(
            check_for_include(
                include,
                "./api/responses/GET_RelatedPerson/verify_relationship.json",
                "./api/responses/GET_RelatedPerson/verify_relationship_include.json",
            )
        )
        response = update_values("9000000017", identifier, response)
        response = update_values("9000000009", patient_identifier, response)
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


def update_values(from_str: str, to_str: str, data: Any) -> dict:
    """Updates values in the response (can be run recursively)

    Args:
        from_str (str): The string to replace
        to_str (str): The string to replace with
        data (Any): The response to update, likely to dict/list

    Returns:
        dict: The updated response
    """
    if isinstance(data, dict):
        # If the data is a dictionary, iterate over its items
        for key, value in data.items():
            if isinstance(value, (dict, list)):
                # If the value is a dictionary, call the function recursively
                update_values(from_str, to_str, value)
            elif value == from_str:
                # If the value matches, update it
                data[key] = to_str
            elif isinstance(value, str):
                # Value may be inside a string so replace if in string
                data[key] = value.replace(from_str, to_str)
    elif isinstance(data, list):
        # If the data is a list, iterate over its elements
        for index, item in enumerate(data):
            if isinstance(item, (dict, list)):
                # Recurse if the item is a nested dictionary or list
                data[index] = update_values(from_str, to_str, item)
            elif item == from_str:
                # Update if the item matches the target_value
                data[index] = to_str
    return data
