#!/usr/bin/env python3
"""
validate_schema.py

Validates a given example file against the schema specification
"""
from json import loads
from yaml import safe_load
from typing import Union
from os import path
from openapi_schema_validator import OAS30Validator
import json
import datetime
from requests import get
import sys

SCHEMA_FILE_PATH = "../specification/validated-relationships-service-api.yaml"
SCHEMA_FILE = path.join(
        path.dirname(path.realpath(__file__)), SCHEMA_FILE_PATH
    )
openapi_schema = {}
import pdb

def main(openapi_schema:dict):
    """Main entrypoint"""
    args = sys.argv
    if (len(args) != 3):
        print("Require schema reference and file to validate")
        exit()

    schema = schema_lookup(args[1])
    file = args[2]
    if (len(openapi_schema) == 0):
        openapi_schema = safe_load(load_file(SCHEMA_FILE))
    validate_consent(openapi_schema, schema, file)

def schema_lookup(schema:str) -> str:
    schema = schema.lower()
    if schema == "consent":
        return "#/components/schemas/ConsentBundle"
    if schema == "relatedperson":
        return "#/components/schemas/RelatedPersonBundle"

    print("")

def validate_consent(schema:dict, schema_ref:str, file:str) -> None:
    schema["$ref"] = schema_ref
    # openapi_schema["$ref"] = [
    #     "#/components/schemas/ConsentBundle",
    #     "#/components/schemas/Consent",
    #     "#/components/schemas/CodeableConcept"
    # ]
    json_contents = load_example_file(file)
    OAS30Validator(schema).validate(json_contents)

def load_example_file(file:str) -> dict:

    patch = path.join(
        path.dirname(path.realpath(__file__)), file
    )
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
