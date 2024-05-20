from unittest.mock import MagicMock, patch

import pytest

from .conftest import RELATED_PERSON_API_ENDPOINT, QUESTIONNAIRE_RESPONSE_API_ENDPOINT

UTILS_FILE_PATH = "sandbox.api.utils"
APP_FILE_PATH = "sandbox.api.app"


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
            "./api/responses/not_found.json",
            404,
        ),
        (
            "identifier=9000000017&patient:identifier=9000000041",
            "./api/responses/not_found.json",
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
@patch(f"{UTILS_FILE_PATH}.load_json_file")
def test_related_person(
    mock_load_json_file: MagicMock,
    request_args: str,
    response_file_name: str,
    client: object,
    status_code: int,
) -> None:
    """Test related_persons endpoint with identifier only."""
    # Arrange
    mock_load_json_file.return_value = expected_body = {"data": "mocked"}
    # Act
    response = client.get(f"{RELATED_PERSON_API_ENDPOINT}?{request_args}")
    # Assert
    mock_load_json_file.assert_called_once_with(response_file_name)
    assert response.status_code == status_code
    assert response.json == expected_body


@pytest.mark.parametrize(
    "url_path,response_file_name,status_code",
    [
        (
            QUESTIONNAIRE_RESPONSE_API_ENDPOINT,
            "./api/responses/POST_QuestionnaireResponse/questionnaire_response_success.json",
            200,
        ),
    ],
)
@patch(f"{APP_FILE_PATH}.load_json_file")
def test_questionnaire_response(
    mock_load_json_file: MagicMock,
    url_path: str,
    response_file_name: str,
    client: object,
    status_code: int,
) -> None:
    """Test related_persons endpoint with identifier only."""
    # Arrange
    mock_load_json_file.return_value = expected_body = {"data": "mocked"}
    # Act
    response = client.post(url_path, json={"data": "mocked"})
    # Assert
    mock_load_json_file.assert_called_once_with(response_file_name)
    assert response.status_code == status_code
    assert response.json == expected_body
