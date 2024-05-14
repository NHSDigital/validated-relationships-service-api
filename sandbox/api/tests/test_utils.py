from unittest.mock import MagicMock, patch

import pytest

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
            "./api/responses/GET_RelatedPerson/bad_request_identifier_missing.json",
            400,
        ),
        (
            "identifier=123456789",  # identifier length is less than 10
            "./api/responses/GET_RelatedPerson/bad_request_identifier_not_as_expected.json",
            400,
        ),
    ],
)
@patch(f"{FILE_PATH}.load_json_file")
def test_check_for_errors(
    mock_get_response: MagicMock,
    request_args: str,
    response_file_name: str,
    status_code: int,
    client: object,
) -> None:
    # Act
    response = client.get(f"{RELATED_PERSON_API_ENDPOINT}?{request_args}")
    # Assert
    mock_get_response.assert_called_once_with(response_file_name)
    assert response.status_code == status_code
