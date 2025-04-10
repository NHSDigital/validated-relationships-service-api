from json import dumps, loads
from unittest.mock import MagicMock, patch

import pytest
from flask import Response

from sandbox.api.constants import (
    PATCH_CONSENT__INVALID_PATCH_FORMAT,
    PATCH_CONSENT__INVALID_PATH,
    PATCH_CONSENT__INVALID_STATE_TRANSITION,
    PATCH_CONSENT__INVALID_STATUS_CODE,
    PATCH_CONSENT__RESOURCE_NOT_FOUND,
    PATCH_CONSENT__SUCCESS,
)

CONSENT_API_ENDPOINT = "/FHIR/R4/Consent"


@pytest.mark.parametrize(
    ("nhs_num", "response_file_name", "status_code"),
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
@patch("sandbox.api.patch_consent.generate_response_from_example")
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
    Expected Behaviors: Request is handled and appropriate response is returned
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
