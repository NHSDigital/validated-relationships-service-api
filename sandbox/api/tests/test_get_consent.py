from json import dumps, loads
from unittest.mock import MagicMock, patch

import pytest
from flask import Response

CONSENT_API_ENDPOINT = "/FHIR/R4/Consent"
GET_CONSENT_FILE_PATH = "sandbox.api.get_consent"


@pytest.mark.parametrize(
    ("request_args", "response_file_name", "status_code"),
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
@patch("sandbox.api.get_consent.generate_response_from_example")
def test_get_consent_returns_expected_responses__mocked_get_consent(
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
    response = client.get(f"{CONSENT_API_ENDPOINT}?{request_args}")
    # Assert
    mock_generate_response_from_example.assert_called_once_with(response_file_name, status_code)
    assert response.status_code == status_code
    assert response.json == loads(mocked_response.get_data(as_text=True))


@pytest.mark.parametrize(
    ("request_args", "response_file_name", "status_code"),
    [
        (
            "performer:identifier=9000000017&status=active&_include=Consent:performer&_include=Consent:patient",
            "./api/examples/GET_Consent/filtered-relationships-status-active-include-details.yaml",
            200,
        ),
        (
            "performer:identifier=9000000017&status=active",
            "./api/examples/errors/invalidated-resource.yaml",
            404,
        ),
        (
            "performer:identifier=9000000017&status=inactive",
            "./api/examples/GET_Consent/filtered-relationships-status-inactive.yaml",
            200,
        ),
        (
            "performer:identifier=9000000017&status=proposed&status=active",
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
            "performer:identifier=9000000022&_include=Consent:performer&_include=Consent:patient",
            "./api/examples/GET_Consent/multiple-relationships-include-performer-patient.yaml",
            200,
        ),
        (
            "performer:identifier=9000000010",  # performer:identifier resulting in single adult relationship
            "./api/examples/GET_Consent/single-consenting-adult-relationship.yaml",
            200,
        ),
        (
            "patient:identifier=9000000005",
            "./api/examples/GET_Consent/single-consenting-adult-relationship.yaml",
            200,
        ),
        (
            "performer:identifier=9000000010&patient:identifier=9000000005",
            "./api/examples/GET_Consent/single-consenting-adult-relationship.yaml",
            200,
        ),
        (
            "performer:identifier=9000000010&_include=Consent:performer&_include=Consent:patient",
            "./api/examples/GET_Consent/single-consenting-adult-relationship-include-performer-patient.yaml",
            200,
        ),
        (
            "patient:identifier=9000000005&_include=Consent:performer&_include=Consent:patient",
            "./api/examples/GET_Consent/single-consenting-adult-relationship-include-performer-patient.yaml",
            200,
        ),
        (
            "performer:identifier=9000000010&patient:identifier=9000000005&_include=Consent:performer&_include=Consent:patient",  # noqa: E501
            "./api/examples/GET_Consent/single-consenting-adult-relationship-include-performer-patient.yaml",
            200,
        ),
        (
            "performer:identifier=9000000019",
            "./api/examples/GET_Consent/single-mother-child-relationship.yaml",
            200,
        ),
        (
            "patient:identifier=9000000009",
            "./api/examples/GET_Consent/single-mother-child-relationship.yaml",
            200,
        ),
        (
            "performer:identifier=9000000019&patient:identifier=9000000009",
            "./api/examples/GET_Consent/single-mother-child-relationship.yaml",
            200,
        ),
        (
            "performer:identifier=9000000019&_include=Consent:performer&_include=Consent:patient",
            "./api/examples/GET_Consent/single-mother-child-relationship-include-performer-patient.yaml",
            200,
        ),
        (
            "patient:identifier=9000000009&_include=Consent:performer&_include=Consent:patient",
            "./api/examples/GET_Consent/single-mother-child-relationship-include-performer-patient.yaml",
            200,
        ),
        (
            "performer:identifier=9000000019&patient:identifier=9000000009&_include=Consent:performer&_include=Consent:patient",  # noqa: E501
            "./api/examples/GET_Consent/single-mother-child-relationship-include-performer-patient.yaml",
            200,
        ),
        (
            "patient:identifier=9000000100",  # Multiple relationships single patient
            "./api/examples/GET_Consent/multiple-relationships-single-patient.yaml",
            200,
        ),
        (
            "patient:identifier=9000000100&_include=Consent:performer",
            "./api/examples/GET_Consent/multiple-relationships-single-patient-include-performer.yaml",
            200,
        ),
        (
            "patient:identifier=9000000100&_include=Consent:patient",
            "./api/examples/GET_Consent/multiple-relationships-single-patient-include-patient.yaml",
            200,
        ),
        (
            "patient:identifier=9000000100&_include=Consent:performer&_include=Consent:patient",
            "./api/examples/GET_Consent/multiple-relationships-single-patient-include-performer-patient.yaml",
            200,
        ),
        (
            "performer:identifier=9000000017&status=test",  # Invalid status parameter error
            "./api/examples/GET_Consent/errors/invalid-status-parameter.yaml",
            422,
        ),
        (
            "performer:identifier=9000000019&_include=test",  # Invalid include parameter error
            "./api/examples/errors/invalid-include-parameter.yaml",
            422,
        ),
        (
            "performer:identifier=90000009990",  # Invalid performer identifier
            "./api/examples/GET_Consent/errors/invalid-identifier.yaml",
            422,
        ),
        (
            "",  # missing performer identifier
            "./api/examples/GET_Consent/errors/missing-identifier.yaml",
            400,
        ),
        (
            "performer:identifier=https://fhir.nhs.uk/Id/nhs-number|A730675929",  # identifier system invalid
            "./api/examples/GET_Consent/errors/invalid-identifier-system.yaml",
            422,
        ),
    ],
)
@patch("sandbox.api.utils.generate_response_from_example")
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
    response = client.get(f"{CONSENT_API_ENDPOINT}?{request_args}")
    # Assert
    mock_generate_response_from_example.assert_called_once_with(response_file_name, status_code)
    assert response.status_code == status_code
    assert response.json == loads(mocked_response.get_data(as_text=True))


@patch(f"{GET_CONSENT_FILE_PATH}.remove_system")
@patch(f"{GET_CONSENT_FILE_PATH}.generate_response_from_example")
def test_get_consent__500_internal_server_error(
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
