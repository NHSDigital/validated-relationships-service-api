from json import dumps, loads
from unittest.mock import MagicMock, patch

import pytest
from flask import Response

from sandbox.api.constants import (
    POST_QUESTIONNAIRE_RESPONSE__SUCCESS,
    POST_QUESTIONNAIRE_RESPONSE__DUPLICATE_RELATIONSHIP_ERROR,
    INTERNAL_SERVER_ERROR_EXAMPLE
)

QUESTIONNAIRE_RESPONSE_API_ENDPOINT = "/FHIR/R4/QuestionnaireResponse"


@pytest.mark.parametrize(
    ("nhs_num", "response_file_name", "status_code"),
    [
        (
            "9000000009",
            POST_QUESTIONNAIRE_RESPONSE__SUCCESS,
            200,
        ),
        (
            "9000000017",
            POST_QUESTIONNAIRE_RESPONSE__SUCCESS,
            200,
        ),
        (
            "9000000049",
            POST_QUESTIONNAIRE_RESPONSE__DUPLICATE_RELATIONSHIP_ERROR,
            409,
        ),
        (
            "INVALID_NHS_NUMBER",
            INTERNAL_SERVER_ERROR_EXAMPLE,
            500,
        ),
    ],
)
@patch("sandbox.api.post_questionnaire_response.generate_response_from_example")
def test_post_questionnaire_response(
    mock_generate_response_from_example: MagicMock,
    nhs_num: str,
    response_file_name: str,
    status_code: int,
    client: object,
) -> None:
    """Test POST QuestionnaireResponse endpoint with different scenarios."""
    # Arrange
    mock_generate_response_from_example.return_value = mocked_response = Response(
        dumps({"data": "mocked"}),
        status=status_code,
        content_type="application/json",
    )
    json = {"resourceType": "QuestionnaireResponse", "source": {"identifier": {"value": nhs_num}}}
    # Act
    response = client.post(QUESTIONNAIRE_RESPONSE_API_ENDPOINT, json=json)
    # Assert
    mock_generate_response_from_example.assert_called_once_with(response_file_name, status_code)
    assert response.status_code == status_code
    assert response.json == loads(mocked_response.get_data(as_text=True))
