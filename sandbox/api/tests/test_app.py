from unittest.mock import MagicMock, patch

import pytest

from .conftest import RELATED_PERSON_API_ENDPOINT

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


@pytest.mark.parametrize(
    "request_args,response_file_name",
    [
        ("identifier=1234567890", "./api/responses/GET_RelatedPerson/identifier.json"),
        (
            "identifier=1234567890&patient=0987654321",
            "./api/responses/GET_RelatedPerson/identifier_and_patient.json",
        ),
        (
            "identifier=1234567890&_include=patient",
            "./api/responses/GET_RelatedPerson/identifier_include.json",
        ),
        (
            "identifier=1234567890&patient=0987654321&_include=patient",
            "./api/responses/GET_RelatedPerson/identifier_and_patient_include.json",
        ),
    ],
)
@patch(f"{FILE_PATH}.get_response")
def test_related_person(
    mock_get_response: MagicMock,
    request_args: str,
    response_file_name: str,
    client: object,
) -> None:
    """Test related_persons endpoint with identifier only."""
    # Arrange
    mock_get_response.return_value = expected_body = {"data": "mocked"}
    # Act
    response = client.get(f"{RELATED_PERSON_API_ENDPOINT}?{request_args}")
    # Assert
    mock_get_response.assert_called_once_with(response_file_name)
    assert response.status_code == 200
    assert response.json == expected_body
