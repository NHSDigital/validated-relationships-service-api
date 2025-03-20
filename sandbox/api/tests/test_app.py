from json import dumps, loads
from unittest.mock import MagicMock, patch

import pytest
from flask import Response

from sandbox.api.constants import (
    POST_CONSENT__SUCCESS,
    POST_CONSENT__DUPLICATE_RELATIONSHIP_ERROR,
    POST_CONSENT__PERFORMER_IDENTIFIER_ERROR,
    PATCH_CONSENT__SUCCESS,
    PATCH_CONSENT__INVALID_PATCH_FORMAT,
    PATCH_CONSENT__INVALID_PATH,
    PATCH_CONSENT__INVALID_STATUS_CODE,
    PATCH_CONSENT__RESOURCE_NOT_FOUND,
    PATCH_CONSENT__INVALID_STATE_TRANSITION,
)

from .conftest import (
    CONSENT_API_ENDPOINT,
    QUESTIONNAIRE_RESPONSE_API_ENDPOINT,
    RELATED_PERSON_API_ENDPOINT,
)

UTILS_FILE_PATH = "sandbox.api.utils"
APP_FILE_PATH = "sandbox.api.app"
GET_CONSENT_FILE_PATH = "sandbox.api.get_consent"


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
            "identifier=9000000033",
            "./api/examples/GET_RelatedPerson/empty_response_9000000033.yaml",
            200,
        ),
        (
            "identifier=9000000017",
            "./api/examples/GET_RelatedPerson/list_relationship_9000000017.yaml",
            200,
        ),
        (
            "identifier=9000000017&_include=RelatedPerson:patient",
            "./api/examples/GET_RelatedPerson/list_relationship_9000000017_include.yaml",
            200,
        ),
        (
            "identifier=9000000017&_include=any",
            "./api/examples/GET_RelatedPerson/list_relationship_9000000017.yaml",
            200,
        ),
        (
            "identifier=9000000017&patient:identifier=9000000009",
            "./api/examples/GET_RelatedPerson/verify_relationship_9000000009.yaml",
            200,
        ),
        (
            "identifier=9000000017&patient:identifier=9000000009&_include=RelatedPerson:patient",
            "./api/examples/GET_RelatedPerson/verify_relationship_9000000009_include.yaml",
            200,
        ),
        (
            "identifier=9000000017&patient:identifier=9000000009&_include=any",
            "./api/examples/GET_RelatedPerson/verify_relationship_9000000009.yaml",
            200,
        ),
        (
            "identifier=9000000017&patient:identifier=9000000025",
            "./api/examples/GET_RelatedPerson/verify_relationship_9000000025.yaml",
            200,
        ),
        (
            "identifier=9000000017&patient:identifier=9000000025&_include=RelatedPerson:patient",
            "./api/examples/GET_RelatedPerson/verify_relationship_9000000025_include.yaml",
            200,
        ),
        (
            "identifier=9000000017&patient:identifier=9000000025&_include=any",
            "./api/examples/GET_RelatedPerson/verify_relationship_9000000025.yaml",
            200,
        ),
    ],
)
@patch("sandbox.api.utils.generate_response_from_example")
def test_related_person(
    mock_generate_response_from_example: MagicMock,
    request_args: str,
    response_file_name: str,
    status_code: int,
    client: object,
) -> None:
    """Test related_persons endpoint."""

    # Arrange
    mock_generate_response_from_example.return_value = mocked_response = Response(
        dumps({"data": "mocked"}),
        status=status_code,
        content_type="application/json",
    )
    # Act
    response = client.get(f"{RELATED_PERSON_API_ENDPOINT}?{request_args}")
    # Assert
    mock_generate_response_from_example.assert_called_once_with(response_file_name, status_code)
    assert response.status_code == status_code
    assert response.json == loads(mocked_response.get_data(as_text=True))


@pytest.mark.parametrize(
    "url_path,response_file_name,status_code",
    [
        (
            QUESTIONNAIRE_RESPONSE_API_ENDPOINT,
            "./api/examples/POST_QuestionnaireResponse/success.yaml",
            200,
        ),
    ],
)
@patch(f"{APP_FILE_PATH}.generate_response_from_example")
def test_questionnaire_response(
    mock_generate_response_from_example: MagicMock,
    url_path: str,
    response_file_name: str,
    client: object,
    status_code: int,
) -> None:
    """Test related_persons endpoint with identifier only."""
    # Arrange
    mock_generate_response_from_example.return_value = mocked_response = Response(
        dumps({"data": "mocked"}),
        status=status_code,
        content_type="application/json",
    )
    # Act
    response = client.post(url_path, json={"data": "mocked"})
    # Assert
    mock_generate_response_from_example.assert_called_once_with(response_file_name, status_code)
    assert response.status_code == status_code
    assert response.json == loads(mocked_response.get_data(as_text=True))


@pytest.mark.parametrize(
    ("request_args,response_file_name,status_code"),
    [
        (
            "performer:identifier=9000000025",  # No performer record found error
            "./api/examples/GET_Consent/no-relationships.yaml",
            200,
        ),
        (
            "performer:identifier=9000000999",  # No performer record found error
            "./api/examples/errors/invalidated-resource.yaml",
            404,
        ),
    ],
)
@patch(f"{GET_CONSENT_FILE_PATH}.generate_response_from_example")
def test_get_consent(
    mock_generate_response_from_example: MagicMock,
    request_args: str,
    response_file_name: str,
    status_code: int,
    client: object,
) -> None:
    """Test Consent endpoint."""
    mock_generate_response_from_example.return_value = mocked_response = Response(
        dumps({"data": "mocked"}),
        status=status_code,
        content_type="application/json",
    )
    # Act
    response = client.get(f"{CONSENT_API_ENDPOINT}?{request_args}")
    # Assert
    mock_generate_response_from_example.assert_called_once_with(response_file_name, status_code)
    assert response.status_code == status_code
    assert response.json == loads(mocked_response.get_data(as_text=True))


@pytest.mark.parametrize(
    "nhs_num,response_file_name,status_code,location",
    [
        (
            "9000000009",
            POST_CONSENT__SUCCESS,
            201,
            "https://sandbox.api.service.nhs.uk/validated-relationships/FHIR/R4/Consent/9000000009",
        ),
        (
            "9000000017",
            POST_CONSENT__SUCCESS,
            201,
            "https://sandbox.api.service.nhs.uk/validated-relationships/FHIR/R4/Consent/9000000017",
        ),
        ("9000000000", POST_CONSENT__PERFORMER_IDENTIFIER_ERROR, 422, None),
        ("9000000049", POST_CONSENT__DUPLICATE_RELATIONSHIP_ERROR, 409, None),
    ],
)
@patch(f"{APP_FILE_PATH}.generate_response_from_example")
def test_post_consent_when_valid_returns_success(
    mock_generate_response_from_example: MagicMock,
    response_file_name: str,
    nhs_num: str,
    location: str,
    client: object,
    status_code: int,
) -> None:
    """
    Function: app.post_consent
    Scenario: Valid consent is POSTed to /consent
    Expected Behavior: Request is accepted and 201 response returned
    """
    # Arrange
    mock_generate_response_from_example.return_value = mocked_response = Response(
        dumps({"data": "mocked"}),
        status=status_code,
        content_type="application/json",
    )
    # Act
    json = {"performer": [{"identifier": {"value": nhs_num}}]}
    response = client.post(CONSENT_API_ENDPOINT, json=json)
    # Assert
    if location is not None:
        mock_generate_response_from_example.assert_called_once_with(
            response_file_name, status_code, headers={"location": location}
        )
    else:
        mock_generate_response_from_example.assert_called_once_with(response_file_name, status_code)
    assert response.status_code == status_code
    assert response.json == loads(mocked_response.get_data(as_text=True))


@pytest.mark.parametrize(
    "nhs_num,response_file_name,status_code",
    [
        ("c6f48e4d", PATCH_CONSENT__SUCCESS, 200),
        ("0c56a594", PATCH_CONSENT__SUCCESS, 200),
        ("b02ea26c", PATCH_CONSENT__SUCCESS, 200),
        ("3a2679eb", PATCH_CONSENT__INVALID_PATCH_FORMAT, 400),
        ("94df7c8f", PATCH_CONSENT__INVALID_PATH, 400),
        ("2a7b736d", PATCH_CONSENT__INVALID_STATUS_CODE, 422),
        ("6fb4361b", PATCH_CONSENT__INVALID_STATE_TRANSITION, 422),
        ("xxxxxxxx", PATCH_CONSENT__RESOURCE_NOT_FOUND, 404),
        ("12345678", PATCH_CONSENT__RESOURCE_NOT_FOUND, 404),
    ],
)
@patch(f"{APP_FILE_PATH}.generate_response_from_example")
def test_patch_consent_on_request_returns_expected_response(
    mock_generate_response_from_example: MagicMock,
    response_file_name: str,
    nhs_num: str,
    client: object,
    status_code: int,
) -> None:
    """
    Function: app.patch_consent
    Scenario: Valid consent is PATCHed to /consent
    Expected Behavior: Request is handled and appropriate response is returned
    """
    # Arrange
    mock_generate_response_from_example.return_value = mocked_response = Response(
        dumps({"data": "mocked"}),
        status=status_code,
        content_type="application/json",
    )
    # Act
    json = [{"op": "replace", "path": "/status", "value": "inactive"}]
    response = client.patch(CONSENT_API_ENDPOINT + f"/{nhs_num}", json=json)
    # Assert
    mock_generate_response_from_example.assert_called_once_with(response_file_name, status_code)
    assert response.status_code == status_code
    assert response.json == loads(mocked_response.get_data(as_text=True))


@patch(f"{GET_CONSENT_FILE_PATH}.remove_system")
@patch(f"{GET_CONSENT_FILE_PATH}.generate_response_from_example")
def test_consent__500_internal_server_error(
    mock_generate_response_from_example: MagicMock,
    mock_remove_system: MagicMock,
    client: object,
) -> None:
    """Test Consent endpoint."""
    mock_remove_system.side_effect = Exception("Test exception")
    # Act
    client.get(f"{CONSENT_API_ENDPOINT}?performer:identifier=9000000015&status=active&_include=Consent:performer")
    # Assert
    mock_generate_response_from_example.assert_called_once_with("./api/examples/errors/internal-server-error.yaml", 500)
