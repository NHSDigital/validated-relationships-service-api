from json import dumps, loads
from unittest.mock import MagicMock, patch

import pytest
from flask import Response

RELATED_PERSON_API_ENDPOINT = "/FHIR/R4/RelatedPerson"


@pytest.mark.parametrize(
    ("request_args", "response_file_name", "status_code"),
    [
        (
            "identifier=9000000033",
            "./api/examples/GET_RelatedPerson/empty_response_9000000033.yaml",
            200,
        ),
        (
            "identifier=9000000017",
            "./api/examples/GET_RelatedPerson/list_relationship_9000000017.yaml",
            200,
        ),
        (
            "identifier=9000000017&_include=RelatedPerson:patient",
            "./api/examples/GET_RelatedPerson/list_relationship_9000000017_include.yaml",
            200,
        ),
        (
            "patient:identifier=9000000042",
            "./api/examples/GET_RelatedPerson/list_relationship_9000000042.yaml",
            200,
        ),
        (
            "patient:identifier=9000000042&_include=RelatedPerson:patient",
            "./api/examples/GET_RelatedPerson/list_relationship_9000000042_include.yaml",
            200,
        ),
        (
            "identifier=9000000017&_include=any",
            "./api/examples/GET_RelatedPerson/list_relationship_9000000017.yaml",
            200,
        ),
        (
            "identifier=9000000017&patient:identifier=9000000009",
            "./api/examples/GET_RelatedPerson/verify_relationship_9000000009.yaml",
            200,
        ),
        (
            "identifier=9000000017&patient:identifier=9000000009&_include=RelatedPerson:patient",
            "./api/examples/GET_RelatedPerson/verify_relationship_9000000009_include.yaml",
            200,
        ),
        (
            "identifier=9000000017&patient:identifier=9000000009&_include=any",
            "./api/examples/GET_RelatedPerson/verify_relationship_9000000009.yaml",
            200,
        ),
        (
            "identifier=9000000017&patient:identifier=9000000025",
            "./api/examples/GET_RelatedPerson/verify_relationship_9000000025.yaml",
            200,
        ),
        (
            "identifier=9000000017&patient:identifier=9000000025&_include=RelatedPerson:patient",
            "./api/examples/GET_RelatedPerson/verify_relationship_9000000025_include.yaml",
            200,
        ),
        (
            "identifier=9000000017&patient:identifier=9000000025&_include=any",
            "./api/examples/GET_RelatedPerson/verify_relationship_9000000025.yaml",
            200,
        ),
        (
            "identifier=9000000041",
            "./api/examples/errors/invalidated-resource.yaml",
            404,
        ),
        (
            "identifier=9000000017&patient:identifier=9000000041",
            "./api/examples/errors/invalidated-resource.yaml",
            404,
        ),
        (
            "",  # identifier is missing
            "./api/examples/GET_RelatedPerson/errors/invalid-identifier-missing.yaml",
            400,
        ),
        (
            "identifier=123456789",  # identifier length is less than 10
            "./api/examples/GET_RelatedPerson/errors/invalid-identifier.yaml",
            400,
        ),
        (
            "identifier=https://fhir.nhs.uk/Id/nhs-number|A730675929",  # identifier system invalid
            "./api/examples/GET_RelatedPerson/errors/invalid-identifier-system.yaml",
            400,
        ),
    ],
)
@patch("sandbox.api.utils.generate_response_from_example")
def test_related_person(
    mock_generate_response_from_example: MagicMock,
    request_args: str,
    response_file_name: str,
    status_code: int,
    client: object,
) -> None:
    """Test related_persons endpoint."""

    # Arrange
    mock_generate_response_from_example.return_value = mocked_response = Response(
        dumps({"data": "mocked"}),
        status=status_code,
        content_type="application/json",
    )
    # Act
    response = client.get(f"{RELATED_PERSON_API_ENDPOINT}?{request_args}")
    # Assert
    mock_generate_response_from_example.assert_called_once_with(response_file_name, status_code)
    assert response.status_code == status_code
    assert response.json == loads(mocked_response.get_data(as_text=True))
