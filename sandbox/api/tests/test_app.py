import json
from json import dumps
from unittest.mock import MagicMock, patch

import pytest
from flask import Response

from .conftest import (
    CONSENT_API_ENDPOINT,
    QUESTIONNAIRE_RESPONSE_API_ENDPOINT,
    RELATED_PERSON_API_ENDPOINT,
)

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
    """Test related_persons endpoint."""
    # Arrange
    mock_load_json_file.return_value = expected_body = {"data": "mocked"}
    # Act
    response = client.get(f"{RELATED_PERSON_API_ENDPOINT}?{request_args}")
    # Assert
    mock_load_json_file.assert_called_once_with(response_file_name)
    assert response.status_code == status_code
    assert response.json == expected_body


@pytest.mark.parametrize(
    "request_args,response_file_name,status_code",
    [
        (
            "identifier=9000000041",
            "./api/examples/errors/not-found.yaml",
            404,
        ),
        (
            "identifier=9000000017&patient:identifier=9000000041",
            "./api/examples/errors/not-found.yaml",
            404,
        ),
    ],
)
@patch(f"{UTILS_FILE_PATH}.generate_response_from_example")
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
    assert response.json == json.loads(mocked_response.get_data(as_text=True))


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


@pytest.mark.parametrize(
    ("request_args,response_file_name,status_code"),
    [
        (
            "performer:identifier=9000000017&status=active",
            "./api/examples/GET_Consent/filtered-relationships-status-active.yaml",
            200,
        ),
        (
            "performer:identifier=9000000017&status=inactive",
            "./api/examples/GET_Consent/filtered-relationships-status-inactive.yaml",
            200,
        ),
        (
            "performer:identifier=9000000017&status=proposed,active",
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
            "performer:identifier=9000000022&_include=Consent:performer,Consent:patient",
            "./api/examples/GET_Consent/multiple-relationships-include-performer-patient.yaml",
            200,
        ),
        (
            "performer:identifier=9000000010",
            "./api/examples/GET_Consent/single-consenting-adult-relationship.yaml",
            200,
        ),
        (
            "performer:identifier=9000000010&_include=Consent:performer,Consent:patient",
            "./api/examples/GET_Consent/single-consenting-adult-relationship-include-performer-patient.yaml",
            200,
        ),
        (
            "performer:identifier=9000000019",
            "./api/examples/GET_Consent/single-mother-child-relationship.yaml",
            200,
        ),
        (
            "performer:identifier=9000000019&_include=Consent:performer,Consent:patient",
            "./api/examples/GET_Consent/single-mother-child-relationship-include-performer-patient.yaml",
            200,
        ),
    ],
)
@patch(f"{UTILS_FILE_PATH}.generate_response_from_example")
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
    assert response.json == json.loads(mocked_response.get_data(as_text=True))


@patch(f"{APP_FILE_PATH}.generate_response_from_example")
def test_consent_no_relationships(
    mock_generate_response_from_example: MagicMock, client: object
) -> None:
    """Test Consent endpoint."""
    mock_generate_response_from_example.return_value = mocked_response = Response(
        dumps({"data": "mocked"}), status=200, content_type="application/json"
    )
    # Act
    response = client.get(f"{CONSENT_API_ENDPOINT}?performer:identifier=9000000025")
    # Assert
    mock_generate_response_from_example.assert_called_once_with(
        "./api/examples/GET_Consent/no-relationships.yaml", 200
    )
    assert response.status_code == 200
    assert response.json == json.loads(mocked_response.get_data(as_text=True))


@patch(f"{APP_FILE_PATH}.generate_response_from_example")
def test_consent__404_bad_request(
    mock_generate_response_from_example: MagicMock,
    client: object,
) -> None:
    """Test Consent endpoint."""
    mock_generate_response_from_example.return_value = mocked_response = Response(
        dumps({"data": "mocked"}), status=404, content_type="application/json"
    )
    # Act
    client.get(f"{CONSENT_API_ENDPOINT}?performer:identifier=9000000999")
    # Assert
    mock_generate_response_from_example.assert_called_once_with(
        "./api/examples/errors/not-found.yaml", 404
    )


@patch(f"{APP_FILE_PATH}.remove_system")
@patch(f"{APP_FILE_PATH}.generate_response_from_example")
def test_consent__500_internal_server_error(
    mock_generate_response_from_example: MagicMock,
    mock_remove_system: MagicMock,
    client: object,
) -> None:
    """Test Consent endpoint."""
    mock_remove_system.side_effect = Exception("Test exception")
    # Act
    client.get(
        f"{CONSENT_API_ENDPOINT}?performer:identifier=9000000015&status=active&_include=Consent:performer"
    )
    # Assert
    mock_generate_response_from_example.assert_called_once_with(
        "./api/examples/errors/internal-server-error.yaml", 500
    )
