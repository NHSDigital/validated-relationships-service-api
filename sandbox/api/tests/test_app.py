from unittest.mock import MagicMock, patch

import pytest

FILE_PATH = "sandbox.api.app"


@pytest.mark.parametrize("endpoint", ["/_status", "/_ping", "/health"])
def test_health_check(client: object, endpoint: str) -> None:
    """Test health check endpoints."""
    # Act
    response = client.get(endpoint)
    # Assert
    assert response.status_code == 200
    assert response.json == {
        "status": "online",
        "message": "Validated Relationships Service Sandbox is running",
    }


@patch(f"{FILE_PATH}.get_response")
def test_related_person__identifier_only(
    mock_get_response: MagicMock, client: object
) -> None:
    """Test related_persons endpoint with identifier only."""
    # Arrange
    mock_get_response.return_value = expected_body = {"data": "mocked"}
    # Act
    response = client.get("/RelatedPerson?identifier=1234567890")
    # Assert
    mock_get_response.assert_called_once_with(
        "./api/responses/GET_RelatedPerson/identifier.json"
    )
    assert response.status_code == 200
    assert response.json == expected_body


@patch(f"{FILE_PATH}.get_response")
def test_related_person__identifier_and_patient(
    mock_get_response: MagicMock, client: object
) -> None:
    """Test related_persons endpoint with identifier and patient."""
    # Arrange
    mock_get_response.return_value = expected_body = {"data": "mocked"}
    # Act
    response = client.get("/RelatedPerson?identifier=1234567890&patient=0987654321")
    # Assert
    mock_get_response.assert_called_once_with(
        "./api/responses/GET_RelatedPerson/identifier_and_patient.json"
    )
    assert response.status_code == 200
    assert response.json == expected_body
