from unittest.mock import MagicMock, patch

from ..utils import load_json_file

FILE_PATH = "sandbox.api.utils"


@patch(f"{FILE_PATH}.open")
def test_get_response(mock_open: MagicMock) -> None:
    # Arrange
    mock_open.return_value.__enter__.return_value.read.return_value = '{"data": "mocked"}'
    file_name = "./api/responses/GET_RelatedPerson/identifier.json"
    # Act
    response = load_json_file(file_name)
    # Assert
    mock_open.assert_called_once_with(file_name, "r")
    assert response == {"data": "mocked"}
