from unittest.mock import MagicMock, patch

import pytest

from ..app import app


@pytest.fixture()
def client() -> object:
    """Create a test client for the app."""
    return app.test_client()


@patch("sandbox.api.app.get_response")
def test_related_person(mock_get_response: MagicMock, client: object) -> None:
    """"""
    # Arrange
    mock_get_response.return_value = {"data": "mocked"}
    # Act
    client.get("/RelatedPerson?identifier=1234")
    # Assert
    mock_get_response.assert_called_once_with("./api/responses/RelatedPerson.json")
