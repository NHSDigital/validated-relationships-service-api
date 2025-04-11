from unittest.mock import MagicMock, patch
import pytest
from flask import Response
from json import dumps, loads

GET_QUESTIONNAIRE_RESPONSE_API_ENDPOINT = "/FHIR/R4/QuestionnaireResponse"


@pytest.mark.parametrize(
    ("request_args", "response_file_name", "status_code"),
    [
        (
            "referenceCode=19318ZGLAB",
            "./api/examples/GET_QuestionnaireResponse/success.yaml",
            200,
        ),
        (
            "referenceCode=INVALID",
            "./api/examples/GET_QuestionnaireResponse/errors/invalid-reference-code.yaml",
            400,
        ),
        (
            "referenceCode=",
            "./api/examples/GET_QuestionnaireResponse/errors/missing-reference-code.yaml",
            404,
        ),
        (
            "referenceCode=ABC123XY",
            "./api/examples/GET_QuestionnaireResponse/errors/questionnaire_response_not_found.yaml",
            404,
        ),
        (
            "referenceCode=INVALID_CODE",
            "./api/examples/errors/internal-server-error.yaml",
            500,
        ),
    ],
)
@patch("sandbox.api.get_questionnaire_response.generate_response_from_example")
def test_get_consent_returns_expected_responses__mocked_utils(
    mock_generate_response_from_example: MagicMock,
    request_args: str,
    response_file_name: str,
    status_code: int,
    client: object,
) -> None:
    """Test GET Consent endpoint."""
    mock_generate_response_from_example.return_value = mocked_response = Response(
        dumps({"data": "mocked"}),
        status=status_code,
        content_type="application/json",
    )
    # Act
    response = client.get(f"{GET_QUESTIONNAIRE_RESPONSE_API_ENDPOINT}?{request_args}")
    # Assert
    mock_generate_response_from_example.assert_called_once_with(response_file_name, status_code)
    assert response.status_code == status_code
    assert response.json == loads(mocked_response.get_data(as_text=True))
