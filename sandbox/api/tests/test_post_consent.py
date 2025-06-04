from json import dumps, loads
from unittest.mock import MagicMock, patch

import pytest
from flask import Response

from sandbox.api.constants import (
    POST_CONSENT__DUPLICATE_RELATIONSHIP_ERROR,
    POST_CONSENT__PERFORMER_IDENTIFIER_ERROR,
    POST_CONSENT__SUCCESS,
)

CONSENT_API_ENDPOINT = "/FHIR/R4/Consent"


@pytest.mark.parametrize(
    ("nhs_num", "response_file_name", "status_code", "id"),
    [
        (
            "9000000009",
            POST_CONSENT__SUCCESS,
            201,
            "90b9863e-e33c-4895-a333-fd0ea0e23205",
        ),
        (
            "9000000017",
            POST_CONSENT__SUCCESS,
            201,
            "90b9863e-e33c-4895-a333-fd0ea0e23205",
        ),
        ("9000000000", POST_CONSENT__PERFORMER_IDENTIFIER_ERROR, 422, None),
        ("9000000049", POST_CONSENT__DUPLICATE_RELATIONSHIP_ERROR, 409, None),
    ],
)
@patch("sandbox.api.post_consent.generate_response_from_example")
def test_post_consent_when_valid_returns_expected_response(
    mock_generate_response_from_example: MagicMock,
    response_file_name: str,
    nhs_num: str,
    id: str,
    client: object,
    status_code: int,
) -> None:
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
    if id is not None:
        mock_generate_response_from_example.assert_called_once_with(
            response_file_name,
            status_code,
            headers={"location": f"https://sandbox.api.service.nhs.uk/validated-relationships/FHIR/R4/Consent/{id}"},
        )
    else:
        mock_generate_response_from_example.assert_called_once_with(response_file_name, status_code)
    assert response.status_code == status_code
    assert response.json == loads(mocked_response.get_data(as_text=True))
