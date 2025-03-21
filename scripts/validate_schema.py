#!/usr/bin/env python3
"""
validate_schema.py

Validates a given example file against the schema specification
"""
from yaml import safe_load
from os import path
from openapi_schema_validator import OAS30Validator
import json
import datetime
import sys

EXAMPLES_PATH = "../"
SCHEMA_FILE_PATH = "../specification/validated-relationships-service-api.yaml"
SCHEMA_FILE = path.join(path.dirname(path.realpath(__file__)), SCHEMA_FILE_PATH)
openapi_schema = {}


def main(openapi_schema: dict):
    """Main entrypoint"""
    args = sys.argv
    if len(args) != 3:
        print("Require schema reference and file to validate")
        exit()

    schema = schema_lookup(args[1])
    file = args[2]
    if len(openapi_schema) == 0:
        openapi_schema = safe_load(load_file(SCHEMA_FILE))
    validate_consent(openapi_schema, schema, file)


def schema_lookup(schema: str) -> str:
    """Returns the schema reference to use

    Args:
        schema (str): The type of record being validated

    Returns:
        str: The schema reference
    """
    schema = schema.lower()
    if schema == "consent":
        return "#/components/schemas/ConsentBundle"
    if schema == "relatedperson":
        return "#/components/schemas/RelatedPersonBundle"
    if schema == "operationoutcome":
        return "#/components/schemas/OperationOutcome"
    if schema == "questionnaireresponse":
        return "#/components/schemas/QuestionnaireResponse"


def validate_consent(schema: dict, schema_ref: str, file: str) -> None:
    schema["$ref"] = schema_ref
    json_contents = load_yaml_file_as_json(file)
    OAS30Validator(schema).validate(json_contents)


def load_yaml_file_as_json(file: str) -> dict:
    """Loads the specified yaml file

    Args:
        file (str): Path to the file

    Returns:
        dict: File converted as json dict
    """
    patch = path.join(path.dirname(path.realpath(__file__)), file)
    yamlfile = safe_load(load_file(patch))
    jsonstr = json.dumps(yamlfile[next(iter(yamlfile))]["value"], default=date_converter)
    return json.loads(jsonstr)


def date_converter(obj):
    """Date and datetime converter to correctly render dates in json"""
    if isinstance(obj, datetime.datetime):
        return obj.replace(tzinfo=datetime.timezone.utc).isoformat()
    if isinstance(obj, datetime.date):
        return obj.isoformat()
    return obj


def load_file(file_path) -> None:
    with open(file_path) as file:
        return file.read()


if __name__ == "__main__":
    main(openapi_schema)
