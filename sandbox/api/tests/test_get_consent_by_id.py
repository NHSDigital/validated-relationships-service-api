from json import dumps, loads
from unittest.mock import MagicMock, patch

import pytest
from flask import Response

CONSENT_API_ENDPOINT = "/FHIR/R4/Consent"
GET_CONSENT_BY_ID_FILE_PATH = "sandbox.api.get_consent_by_id"


@pytest.mark.parametrize(
    ("consent_id", "include_params", "response_file_name", "status_code"),
    [
        (
            "a0922245-1072-40c3-8f4e-a7490c10d365",  # Invalid parameters
            "_invalid=test",
            "./api/examples/errors/invalid-include-parameter.yaml",
            422,
        ),
        (
            "a0922245-1072-40c3-8f4e-a7490c10d365",  # No proxy-role record found error
            "",
            "./api/examples/errors/invalidated-resource.yaml",
            404,
        ),
        (
            " ",  # Missing consent ID
            "",
            "./api/examples/GET_Consent/ID/errors/invalid-id.yaml",
            400,
        ),
        (
            "test",  # Invalid consent ID
            "",
            "./api/examples/GET_Consent/ID/errors/invalid-id.yaml",
            400,
        ),
    ],
)
@patch(f"{GET_CONSENT_BY_ID_FILE_PATH}.generate_response_from_example")
def test_get_consent_by_id_returns_expected_responses__mocked_get_consent_by_id(
    mock_generate_response_from_example: MagicMock,
    consent_id: str,
    include_params: str,
    response_file_name: str,
    status_code: int,
    client: object,
) -> None:
    """Test GET /Consent/{ID} endpoint."""
    mock_generate_response_from_example.return_value = mocked_response = Response(
        dumps({"data": "mocked"}),
        status=status_code,
        content_type="application/json",
    )
    # Act
    response = client.get(f"{CONSENT_API_ENDPOINT}/{consent_id}?{include_params}")
    # import pdb; pdb.set_trace()
    # Assert
    mock_generate_response_from_example.assert_called_once_with(
        response_file_name, status_code
    )
    assert response.status_code == status_code
    assert response.json == loads(mocked_response.get_data(as_text=True))


@pytest.mark.parametrize(
    ("consent_id", "include_params", "response_file_name", "status_code"),
    [
        (
            "74eed847-ca25-4e76-8cf2-f2c2d7842a7a",  # Single consenting adult relationship no include
            "",
            "./api/examples/GET_Consent/single-consenting-adult-relationship.yaml",
            200,
        ),
        (
            "74eed847-ca25-4e76-8cf2-f2c2d7842a7a",  # Single consenting adult relationship with include performer
            "_include=Consent:performer",
            "./api/examples/GET_Consent/single-consenting-adult-relationship-include-performer.yaml",
            200,
        ),
        (
            "74eed847-ca25-4e76-8cf2-f2c2d7842a7a",  # Single consenting adult relationship with include patient
            "_include=Consent:patient",
            "./api/examples/GET_Consent/single-consenting-adult-relationship-include-patient.yaml",
            200,
        ),
        (
            "74eed847-ca25-4e76-8cf2-f2c2d7842a7a",  # Single consenting adult relationship with include both
            "_include=Consent:performer&_include=Consent:patient",
            "./api/examples/GET_Consent/single-consenting-adult-relationship-include-performer-patient.yaml",
            200,
        ),
        (
            "39df03a2-1b14-4d19-b1dc-d5d8cbf96948",  # Single adult-child relationship no include
            "",
            "./api/examples/GET_Consent/single-mother-child-relationship.yaml",
            200,
        ),
        (
            "39df03a2-1b14-4d19-b1dc-d5d8cbf96948",  # Single adult-child relationship with include performer
            "_include=Consent:performer",
            "./api/examples/GET_Consent/single-mother-child-relationship-include-performer.yaml",
            200,
        ),
        (
            "39df03a2-1b14-4d19-b1dc-d5d8cbf96948",  # Single adult-child relationship with include patient
            "_include=Consent:patient",
            "./api/examples/GET_Consent/single-mother-child-relationship-include-patient.yaml",
            200,
        ),
        (
            "39df03a2-1b14-4d19-b1dc-d5d8cbf96948",  # Single adult-child relationship with include both
            "_include=Consent:performer&_include=Consent:patient",
            "./api/examples/GET_Consent/single-mother-child-relationship-include-performer-patient.yaml",
            200,
        ),
    ],
)
@patch("sandbox.api.utils.generate_response_from_example")
def test_get_consent_by_id_returns_expected_responses__mocked_utils(
    mock_generate_response_from_example: MagicMock,
    consent_id: str,
    include_params: str,
    response_file_name: str,
    status_code: int,
    client: object,
) -> None:
    """Test GET /Consent/{ID} endpoint."""
    mock_generate_response_from_example.return_value = mocked_response = Response(
        dumps({"data": "mocked"}),
        status=status_code,
        content_type="application/json",
    )
    # Act
    response = client.get(f"{CONSENT_API_ENDPOINT}/{consent_id}?{include_params}")
    # import pdb; pdb.set_trace()
    # Assert
    mock_generate_response_from_example.assert_called_once_with(
        response_file_name, status_code
    )
    assert response.status_code == status_code
    assert response.json == loads(mocked_response.get_data(as_text=True))


@patch(f"{GET_CONSENT_BY_ID_FILE_PATH}.check_for_consent_include_params")
@patch(f"{GET_CONSENT_BY_ID_FILE_PATH}.generate_response_from_example")
def test_get_consent_by_id__500_internal_server_error(
    mock_generate_response_from_example: MagicMock,
    mock_check_for_consent_include_params: MagicMock,
    client: object,
) -> None:
    """Test GET /Consent/{ID} endpoint."""
    mock_check_for_consent_include_params.side_effect = Exception("Test exception")
    # Act
    client.get(f"{CONSENT_API_ENDPOINT}/74eed847-ca25-4e76-8cf2-f2c2d7842a7a")
    # Assert
    mock_generate_response_from_example.assert_called_once_with(
        "./api/examples/errors/internal-server-error.yaml", 500
    )
