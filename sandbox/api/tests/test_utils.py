from json import dumps
from unittest.mock import MagicMock, patch

import pytest
from flask import Response

from ..utils import load_json_file
from .conftest import RELATED_PERSON_API_ENDPOINT

FILE_PATH = "sandbox.api.utils"


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
    "request_args,response_file_name,status_code",
    [
        (
            "",  # identifier is missing
            "./api/examples/errors/missing-identifier.yaml",
            400,
        ),
        (
            "identifier=123456789",  # identifier length is less than 10
            "./api/examples/errors/invalid-identifier.yaml",
            400,
        ),
        # (
        #     "identifier=https://fhir.nhs.uk/ID/nhs-number|1234567890",  # identifier system invalid
        #     "./api/responses/GET_RelatedPerson/bad_request_identifier_invalid_system.json",
        #     400,
        # ),
    ],
)
@patch(f"{FILE_PATH}.generate_response_from_example")
def test_check_for_errors(
    mock_generate_response_from_example: MagicMock,
    request_args: str,
    response_file_name: str,
    status_code: int,
    client: object,
) -> None:
    mock_generate_response_from_example.return_value = mocked_response = (
        Response(
            dumps({"data": "mocked"}),
            status=status_code,
            content_type="application/json"
        )
    )
    # Act
    response = client.get(f"{RELATED_PERSON_API_ENDPOINT}?{request_args}")
    # Assert
    mock_generate_response_from_example.assert_called_once_with(response_file_name, status_code)
    assert response.status_code == status_code
