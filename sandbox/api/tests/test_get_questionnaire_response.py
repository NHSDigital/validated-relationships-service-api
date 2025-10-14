from unittest.mock import MagicMock, patch
import pytest
from flask import Response
from json import dumps, loads

from pycparser.plyparser import parameterized

GET_QUESTIONNAIRE_RESPONSE_API_ENDPOINT = "/FHIR/R4/QuestionnaireResponse"


@pytest.mark.parametrize(
    ("path", "response_file_name", "status_code"),
    [
        (
            "/156e1560-e532-4e2a-85ad-5aeff03dc43e",
            "./api/examples/GET_QuestionnaireResponse/success.yaml",
            200,
        ),
        (
            "/INVALID",
            "./api/examples/GET_QuestionnaireResponse/errors/invalid_access_request_id.yaml",
            400,
        ),
        (
            "/60d09b82-f4bb-41f9-b41e-767999b4ac9b",
            "./api/examples/GET_QuestionnaireResponse/errors/questionnaire_response_not_found.yaml",
            404,
        ),
        (
            "/INVALID_CODE",
            "./api/examples/errors/internal-server-error.yaml",
            500,
        ),
    ],
)
@patch("sandbox.api.get_questionnaire_response.generate_response_from_example")
def test_get_questionnaire_response_id_returns_expected_responses__mocked_utils(
    mock_generate_response_from_example: MagicMock,
    path: str,
    response_file_name: str,
    status_code: int,
    client: object,
) -> None:
    """Test GET /QuestionnaireResponse/{id} endpoint."""
    mock_generate_response_from_example.return_value = mocked_response = Response(
        dumps({"data": "mocked"}),
        status=status_code,
        content_type="application/json",
    )
    # Act
    response = client.get(f"{GET_QUESTIONNAIRE_RESPONSE_API_ENDPOINT}{path}")
    # Assert
    mock_generate_response_from_example.assert_called_once_with(response_file_name, status_code)
    assert response.status_code == status_code
    assert response.json == loads(mocked_response.get_data(as_text=True))


@pytest.mark.parametrize("path", ["/",""])
@patch("sandbox.api.app.generate_response_from_example")
def test_get_questionnaire_response_without_path_params_return_405_errors(
    mock_generate_response_from_example: MagicMock,
    path: str,
    client: object,
) -> None:
    """Test the GET /QuestionnaireResponse endpoint with no path params."""
    mock_generate_response_from_example.return_value = mocked_response = Response(
        dumps({"data": "mocked"}),
        status=405,
        content_type="application/json",
    )
    # Act
    response = client.get(f"{GET_QUESTIONNAIRE_RESPONSE_API_ENDPOINT}{path}")
    # Assert
    mock_generate_response_from_example.assert_called_once_with("./api/examples/errors/method-not-allowed.yaml", 405)
    assert response.status_code == 405
    assert response.json == loads(mocked_response.get_data(as_text=True))
