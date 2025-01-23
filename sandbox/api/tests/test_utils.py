from json import dumps, loads
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
            "./api/examples/errors/invalidated-resource.yaml",
            404,
        ),
        (
            "identifier=9000000017&patient:identifier=9000000041",
            "./api/examples/errors/invalidated-resource.yaml",
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
    assert response.json == loads(mocked_response.get_data(as_text=True))


@pytest.mark.parametrize(
    ("request_args,response_file_name,status_code"),
    [
        (
            "performer:identifier=9000000017&status=active&_include=Consent:performer&_include=Consent:patient",
            "./api/examples/GET_Consent/filtered-relationships-status-active-include-details.yaml",
            200,
        ),
        (
            "performer:identifier=9000000017&status=active",
            "./api/examples/errors/invalidated-resource.yaml",
            404,
        ),
        (
            "performer:identifier=9000000017&status=inactive",
            "./api/examples/GET_Consent/filtered-relationships-status-inactive.yaml",
            200,
        ),
        (
            "performer:identifier=9000000017&status=proposed&status=active",
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
            "performer:identifier=9000000022&_include=Consent:performer&_include=Consent:patient",
            "./api/examples/GET_Consent/multiple-relationships-include-performer-patient.yaml",
            200,
        ),
        (
            "performer:identifier=9000000010",
            "./api/examples/GET_Consent/single-consenting-adult-relationship.yaml",
            200,
        ),
        (
            "performer:identifier=9000000010&_include=Consent:performer&_include=Consent:patient",
            "./api/examples/GET_Consent/single-consenting-adult-relationship-include-performer-patient.yaml",
            200,
        ),
        (
            "performer:identifier=9000000019",
            "./api/examples/GET_Consent/single-mother-child-relationship.yaml",
            200,
        ),
        (
            "performer:identifier=9000000019&_include=Consent:performer&_include=Consent:patient",
            "./api/examples/GET_Consent/single-mother-child-relationship-include-performer-patient.yaml",
            200,
        ),
        (
            "performer:identifier=9000000017&status=test",  # Invalid status parameter error
            "./api/examples/GET_Consent/errors/invalid-status-parameter.yaml",
            400,
        ),
        (
            "performer:identifier=9000000019&_include=test",  # Invalid include parameter error
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
    assert response.json == loads(mocked_response.get_data(as_text=True))


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
    "request_args,response_file_name",
    [
        (
            "",  # identifier is missing
            "./api/responses/GET_RelatedPerson/bad_request_identifier_missing.json",
        ),
        (
            "identifier=123456789",  # identifier length is less than 10
            "./api/responses/GET_RelatedPerson/bad_request_identifier_invalid.json",
        ),
        (
            "identifier=https://fhir.nhs.uk/Id/nhs-number|A730675929",  # identifier system invalid
            "./api/responses/GET_RelatedPerson/bad_request_identifier_invalid_system.json",
        ),
    ],
)
@patch(f"{FILE_PATH}.load_json_file")
def test_check_for_related_person_errors(
    mock_load_json_file: MagicMock,
    request_args: str,
    response_file_name: str,
    client: object,
) -> None:
    mock_load_json_file.return_value = Response(
        dumps({"data": "mocked"}), content_type="application/json"
    )
    # Act
    response = client.get(f"{RELATED_PERSON_API_ENDPOINT}?{request_args}")
    # Assert
    mock_load_json_file.assert_called_once_with(response_file_name)
    assert response.status_code == 500


@pytest.mark.parametrize(
    "request_args,response_file_name,status_code",
    [
        (
            "performer:identifier=90000009990",  # Invalid performer identifier
            "./api/examples/GET_Consent/errors/invalid-identifier.yaml",
            400,
        ),
        (
            "",  # missing performer identifier
            "./api/examples/GET_Consent/errors/missing-identifier.yaml",
            400,
        ),
        (
            "performer:identifier=https://fhir.nhs.uk/Id/nhs-number|A730675929",  # identifier system invalid
            "./api/examples/GET_Consent/errors/invalid-identifier-system.yaml",
            400,
        ),
    ],
)
@patch(f"{FILE_PATH}.generate_response_from_example")
def test_check_for_consent_errors(
    mock_generate_response_from_example: MagicMock,
    request_args: str,
    response_file_name: str,
    status_code: int,
    client: object,
) -> None:
    mock_generate_response_from_example.return_value = Response(
        dumps({"data": "mocked"}), status=status_code, content_type="application/json"
    )
    # Act
    response = client.get(f"{CONSENT_API_ENDPOINT}?{request_args}")
    # Assert
    mock_generate_response_from_example.assert_called_once_with(
        response_file_name, status_code
    )
    assert response.status_code == status_code
