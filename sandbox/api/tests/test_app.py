from unittest.mock import MagicMock, patch

import pytest

from .conftest import RELATED_PERSON_API_ENDPOINT

FILE_PATH = "sandbox.api.utils"


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
    "request_args,response_file_name,status_code",
    [
        (
            "identifier=9000000041",
            "./api/responses/GET_RelatedPerson/not_found.json",
            404,
        ),
        (
            "identifier=9000000017&patient:identifier=9000000041",
            "./api/responses/GET_RelatedPerson/not_found.json",
            404,
        ),
        (
            "identifier=9000000033",
            "./api/responses/GET_RelatedPerson/empty_response_9000000033.json",
            200,
        ),
        (
            "identifier=9000000017",
            "./api/responses/GET_RelatedPerson/list_relationship_9000000017.json",
            200,
        ),
        (
            "identifier=9000000017&_include=RelatedPerson:patient",
            "./api/responses/GET_RelatedPerson/list_relationship_include_9000000017.json",
            200,
        ),
        (
            "identifier=9000000017&_include=any",
            "./api/responses/GET_RelatedPerson/list_relationship_9000000017.json",
            200,
        ),
        (
            "identifier=9000000017&patient:identifier=9000000009",
            "./api/responses/GET_RelatedPerson/verify_relationship_9000000009.json",
            200,
        ),
        (
            "identifier=9000000017&patient:identifier=9000000009&_include=RelatedPerson:patient",
            "./api/responses/GET_RelatedPerson/verify_relationship_include_9000000009.json",
            200,
        ),
        (
            "identifier=9000000017&patient:identifier=9000000009&_include=any",
            "./api/responses/GET_RelatedPerson/verify_relationship_9000000009.json",
            200,
        ),
        (
            "identifier=9000000017&patient:identifier=9000000025",
            "./api/responses/GET_RelatedPerson/verify_relationship_9000000025.json",
            200,
        ),
        (
            "identifier=9000000017&patient:identifier=9000000025&_include=RelatedPerson:patient",
            "./api/responses/GET_RelatedPerson/verify_relationship_include_9000000025.json",
            200,
        ),
        (
            "identifier=9000000017&patient:identifier=9000000025&_include=any",
            "./api/responses/GET_RelatedPerson/verify_relationship_9000000025.json",
            200,
        ),
    ],
)
@patch(f"{FILE_PATH}.load_json_file")
def test_related_person(
    mock_get_response: MagicMock,
    request_args: str,
    response_file_name: str,
    client: object,
    status_code: int,
) -> None:
    """Test related_persons endpoint with identifier only."""
    # Arrange
    mock_get_response.return_value = expected_body = {"data": "mocked"}
    # Act
    response = client.get(f"{RELATED_PERSON_API_ENDPOINT}?{request_args}")
    # Assert
    mock_get_response.assert_called_once_with(response_file_name)
    assert response.status_code == status_code
    assert response.json == expected_body
