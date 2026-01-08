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
    PATCH_CONSENT__INVALID_STATUS_REASON,
    PATCH_CONSENT__MISSING_FREE_TEXT_FOR_OTHER,
)

CONSENT_API_ENDPOINT = "/FHIR/R4/Consent"


@pytest.mark.parametrize(
    ("nhs_num", "response_file_name", "status_code"),
    [
        ("74eed847-ca25-4e76-8cf2-f2c2d7842a7a", PATCH_CONSENT__SUCCESS, 200),
        ("6b71ac92-baa3-4b76-b0f5-a601257e2722", PATCH_CONSENT__SUCCESS, 200),
        ("43003db8-ffcd-4bd6-ab2f-b49b9656f9e5", PATCH_CONSENT__SUCCESS, 200),
        (
            "849ea584-2318-471b-a24c-cee1b5ad0137",
            PATCH_CONSENT__INVALID_PATCH_FORMAT,
            400,
        ),
        ("01abb0c5-b1ac-499d-9655-9cd0b8d3588f", PATCH_CONSENT__INVALID_PATH, 400),
        (
            "78c35330-fa2f-4934-a5dd-fff847f38de5",
            PATCH_CONSENT__INVALID_STATUS_CODE,
            422,
        ),
        (
            "51fb4df5-815a-45cd-8427-04d6558336b7",
            PATCH_CONSENT__INVALID_STATUS_REASON,
            422,
        ),
        (
            "7b7f47b8-96e5-43eb-b733-283bf1449f2c",
            PATCH_CONSENT__INVALID_STATE_TRANSITION,
            422,
        ),
        (
            "d4e8a6f2-1c3b-4a7e-9d2f-8b5c7e9f1a3d",
            PATCH_CONSENT__MISSING_FREE_TEXT_FOR_OTHER,
            400,
        ),
        (
            "a1b2c3d4-e5f6-4789-a0b1-c2d3e4f5a6b7",
            PATCH_CONSENT__SUCCESS,
            200,
        ),
        (
            "b2c3d4e5-f6a7-4890-b1c2-d3e4f5a6b7c8",
            PATCH_CONSENT__SUCCESS,
            200,
        ),
        (
            "c3d4e5f6-a7b8-4901-c2d3-e4f5a6b7c8d9",
            PATCH_CONSENT__SUCCESS,
            200,
        ),
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
