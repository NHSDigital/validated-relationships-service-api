import json
from json import dumps
from unittest.mock import MagicMock, patch

import pytest
from flask import Response

from ..utils import load_json_file
from .conftest import RELATED_PERSON_API_ENDPOINT, CONSENT_API_ENDPOINT

FILE_PATH = "sandbox.api.utils"


@pytest.mark.parametrize(
    "request_args,response_file_name,status_code",
    [
        (
            "identifier=9000000041",
            "./api/examples/errors/not-found.yaml",
            404,
        ),
        (
            "identifier=9000000017&patient:identifier=9000000041",
            "./api/examples/errors/not-found.yaml",
            404,
        ),
    ],
)
@patch(f"{FILE_PATH}.generate_response_from_example")
def test_related_person__not_found(
    mock_generate_response_from_example: MagicMock,
    request_args: str,
    response_file_name: str,
    status_code: int,
    client: object,
) -> None:
    """Test related_persons endpoint."""
    # Arrange
    mock_generate_response_from_example.return_value = mocked_response = Response(
        dumps({"data": "mocked"}), status=status_code, content_type="application/json"
    )
    # Act
    response = client.get(f"{RELATED_PERSON_API_ENDPOINT}?{request_args}")
    # Assert
    mock_generate_response_from_example.assert_called_once_with(
        response_file_name, status_code
    )
    assert response.status_code == status_code
    assert response.json == json.loads(mocked_response.get_data(as_text=True))


@pytest.mark.parametrize(
    ("request_args,response_file_name,status_code"),
    [
        (
            "performer:identifier=9000000017&status=active",
            "./api/examples/GET_Consent/filtered-relationships-status-active.yaml",
            200,
        ),
        (
            "performer:identifier=9000000017&status=inactive",
            "./api/examples/GET_Consent/filtered-relationships-status-inactive.yaml",
            200,
        ),
        (
            "performer:identifier=9000000017&status=proposed,active",
            "./api/examples/GET_Consent/filtered-relationships-status-proposed-active.yaml",
            200,
        ),
        (
            "performer:identifier=9000000022",
            "./api/examples/GET_Consent/multiple-relationships.yaml",
            200,
        ),
        (
            "performer:identifier=9000000022&_include=Consent:patient",
            "./api/examples/GET_Consent/multiple-relationships-include-patient.yaml",
            200,
        ),
        (
            "performer:identifier=9000000022&_include=Consent:performer",
            "./api/examples/GET_Consent/multiple-relationships-include-performer.yaml",
            200,
        ),
        (
            "performer:identifier=9000000022&_include=Consent:performer,Consent:patient",
            "./api/examples/GET_Consent/multiple-relationships-include-performer-patient.yaml",
            200,
        ),
        (
            "performer:identifier=9000000010",
            "./api/examples/GET_Consent/single-consenting-adult-relationship.yaml",
            200,
        ),
        (
            "performer:identifier=9000000010&_include=Consent:performer,Consent:patient",
            "./api/examples/GET_Consent/single-consenting-adult-relationship-include-performer-patient.yaml",
            200,
        ),
        (
            "performer:identifier=9000000019",
            "./api/examples/GET_Consent/single-mother-child-relationship.yaml",
            200,
        ),
        (
            "performer:identifier=9000000019&_include=Consent:performer,Consent:patient",
            "./api/examples/GET_Consent/single-mother-child-relationship-include-performer-patient.yaml",
            200,
        ),
        (
            "performer:identifier=9000000017&status=test", #Invalid status parameter error
            "./api/examples/GET_Consent/errors/invalid-status-parameter.yaml",
            400,
        ),
        (
            "performer:identifier=9000000019&_include=test", #Invalid include parameter error
            "./api/examples/errors/invalid-include-parameter.yaml",
            400,
        ),
    ],
)
@patch(f"{FILE_PATH}.generate_response_from_example")
def test_consent(
    mock_generate_response_from_example: MagicMock,
    request_args: str,
    response_file_name: str,
    status_code: int,
    client: object,
) -> None:
    """Test Consent endpoint."""
    mock_generate_response_from_example.return_value = mocked_response = Response(
        dumps({"data": "mocked"}), status=status_code, content_type="application/json"
    )
    # Act
    response = client.get(f"{CONSENT_API_ENDPOINT}?{request_args}")
    # Assert
    mock_generate_response_from_example.assert_called_once_with(
        response_file_name, status_code
    )
    assert response.status_code == status_code
    assert response.json == json.loads(mocked_response.get_data(as_text=True))


@patch(f"{FILE_PATH}.open")
def test_get_response(mock_open: MagicMock) -> None:
    # Arrange
    mock_open.return_value.__enter__.return_value.read.return_value = (
        '{"data": "mocked"}'
    )
    file_name = "./api/responses/GET_RelatedPerson/identifier.json"
    # Act
    response = load_json_file(file_name)
    # Assert
    mock_open.assert_called_once_with(file_name, "r")
    assert response == {"data": "mocked"}


@pytest.mark.parametrize(
    "endpoint,request_args,response_file_name,status_code",
    [
        (
            RELATED_PERSON_API_ENDPOINT, # Related person - identifier is missing
            "",
            "./api/examples/errors/missing-identifier.yaml",
            400,
        ),
        (
            RELATED_PERSON_API_ENDPOINT,  # Related person - identifier length is less than 10
            "identifier=123456789",
            "./api/examples/errors/invalid-identifier.yaml",
            400,
        ),
        (
            RELATED_PERSON_API_ENDPOINT, # Related person  - identifier system invalid
            "identifier=https://fhir.nhs.uk/Id/nhs-number|A730675929",
            "./api/examples/errors/invalid-identifier-system.yaml",
            400,
        ),
        (
            CONSENT_API_ENDPOINT,  # Consent - Invalid performer identifier
            "performer:identifier=90000009990",
            "./api/examples/errors/invalid-identifier.yaml",
            400,
        ),
        (
            CONSENT_API_ENDPOINT, # Consent - missing performer identifier
            "",
            "./api/examples/errors/missing-identifier.yaml",
            400,
        ),
        (
            CONSENT_API_ENDPOINT,  # Related person  - identifier system invalid
            "performer:identifier=https://fhir.nhs.uk/Id/nhs-number|A730675929",
            "./api/examples/errors/invalid-identifier-system.yaml",
            400,
        ),
    ],
)
@patch(f"{FILE_PATH}.generate_response_from_example")
def test_check_for_errors(
    mock_generate_response_from_example: MagicMock,
    endpoint : str,
    request_args: str,
    response_file_name: str,
    status_code: int,
    client: object,
) -> None:
    mock_generate_response_from_example.return_value = Response(
        dumps({"data": "mocked"}), status=status_code, content_type="application/json"
    )
    # Act
    response = client.get(f"{endpoint}?{request_args}")
    # Assert
    mock_generate_response_from_example.assert_called_once_with(
        response_file_name, status_code
    )
    assert response.status_code == status_code
