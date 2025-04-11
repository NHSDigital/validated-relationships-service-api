from json import dumps, loads
from unittest.mock import MagicMock, patch

import pytest
from flask import Response

QUESTIONNAIRE_RESPONSE_API_ENDPOINT = "/FHIR/R4/QuestionnaireResponse"


@pytest.mark.parametrize(
    ("url_path", "response_file_name", "status_code"),
    [
        (
            QUESTIONNAIRE_RESPONSE_API_ENDPOINT,
            "./api/examples/POST_QuestionnaireResponse/success.yaml",
            200,
        ),
    ],
)
@patch("sandbox.api.post_questionnaire_response.generate_response_from_example")
def test_post_questionnaire_response(
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
