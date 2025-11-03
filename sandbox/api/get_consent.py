from logging import INFO, basicConfig, getLogger
from typing import Union

from flask import request

from .constants import (
    GET_CONSENT__FILTERED_RELATIONSHIPS_STATUS_ACTIVE,
    GET_CONSENT__FILTERED_RELATIONSHIPS_STATUS_INACTIVE,
    GET_CONSENT__FILTERED_RELATIONSHIPS_STATUS_PROPOSED_ACTIVE,
    GET_CONSENT__MULTIPLE_RELATIONSHIPS_SINGLE_PATIENT,
    GET_CONSENT__MULTIPLE_RELATIONSHIPS_SINGLE_PATIENT_INCLUDE_PATIENT,
    GET_CONSENT__MULTIPLE_RELATIONSHIPS_SINGLE_PATIENT_INCLUDE_PERFORMER,
    GET_CONSENT__MULTIPLE_RELATIONSHIPS_SINGLE_PATIENT_INCLUDE_BOTH,
    GET_CONSENT__MULTIPLE_RELATIONSHIPS,
    GET_CONSENT__MULTIPLE_RELATIONSHIPS_INCLUDE_BOTH,
    GET_CONSENT__MULTIPLE_RELATIONSHIPS_INCLUDE_PATIENT,
    GET_CONSENT__MULTIPLE_RELATIONSHIPS_INCLUDE_PERFORMER,
    GET_CONSENT__NO_RELATIONSHIPS,
    GET_CONSENT__SINGLE_CONSENTING_ADULT_RELATIONSHIP,
    GET_CONSENT__SINGLE_CONSENTING_ADULT_RELATIONSHIP_INCLUDE_BOTH,
    GET_CONSENT__SINGLE_MOTHER_CHILD_RELATIONSHIP,
    GET_CONSENT__SINGLE_MOTHER_CHILD_RELATIONSHIP_INCLUDE_BOTH,
    INTERNAL_SERVER_ERROR_EXAMPLE,
    INVALIDATED_RESOURCE, GET_CONSENT__SINGLE_MOTHER_CHILD_RELATIONSHIP_UNKNOWN_LEGAL_BASIS,
    GET_CONSENT__SINGLE_MOTHER_CHILD_RELATIONSHIP_UNKNOWN_LEGAL_BASIS_INCLUDE_BOTH,
    GET_CONSENT__SINGLE_MOTHER_CHILD_RELATIONSHIP_UNKNOWN_LEGAL_BASIS_INCLUDE_PATIENT,
    GET_CONSENT__SINGLE_MOTHER_CHILD_RELATIONSHIP_UNKNOWN_LEGAL_BASIS_INCLUDE_PERFORMER,
)
from .utils import (
    check_for_consent_filtering,
    check_for_consent_include_params,
    check_for_get_consent_errors,
    generate_response_from_example,
    remove_system,
)

basicConfig(level=INFO, format="%(asctime)s - %(message)s")
logger = getLogger(__name__)


def get_consent_response() -> Union[dict, tuple]:
    """Sandbox API for GET /Consent

    Returns:
        Union[dict, tuple]: Response for GET /Consent
    """
    try:
        # Check Headers
        if errors := check_for_get_consent_errors(request):
            return errors

        performer_identifier = remove_system(request.args.get("performer:identifier"))
        patient_identifier = remove_system(request.args.get("patient:identifier"))
        status = request.args.getlist("status")
        _include = request.args.getlist("_include")

        # Single consenting adult relationship
        if performer_identifier == "9000000010" or patient_identifier == "9000000005":
            return check_for_consent_include_params(
                _include,
                GET_CONSENT__SINGLE_CONSENTING_ADULT_RELATIONSHIP,
                GET_CONSENT__SINGLE_CONSENTING_ADULT_RELATIONSHIP_INCLUDE_BOTH,
            )
        # Single mother child relationship
        elif performer_identifier == "9000000019" or patient_identifier == "9000000009":
            return check_for_consent_include_params(
                _include,
                GET_CONSENT__SINGLE_MOTHER_CHILD_RELATIONSHIP,
                GET_CONSENT__SINGLE_MOTHER_CHILD_RELATIONSHIP_INCLUDE_BOTH,
            )
        # Single mother-child relationship with unknown legal basis
        elif performer_identifier == "9000000999" or patient_identifier == "9000000998":
            return check_for_consent_include_params(
                _include,
                GET_CONSENT__SINGLE_MOTHER_CHILD_RELATIONSHIP_UNKNOWN_LEGAL_BASIS,
                GET_CONSENT__SINGLE_MOTHER_CHILD_RELATIONSHIP_UNKNOWN_LEGAL_BASIS_INCLUDE_BOTH,
                GET_CONSENT__SINGLE_MOTHER_CHILD_RELATIONSHIP_UNKNOWN_LEGAL_BASIS_INCLUDE_PATIENT,
                GET_CONSENT__SINGLE_MOTHER_CHILD_RELATIONSHIP_UNKNOWN_LEGAL_BASIS_INCLUDE_PERFORMER,
            )

        elif patient_identifier == "9000000100":
            return check_for_consent_include_params(
                _include,
                GET_CONSENT__MULTIPLE_RELATIONSHIPS_SINGLE_PATIENT,
                GET_CONSENT__MULTIPLE_RELATIONSHIPS_SINGLE_PATIENT_INCLUDE_BOTH,
                GET_CONSENT__MULTIPLE_RELATIONSHIPS_SINGLE_PATIENT_INCLUDE_PATIENT,
                GET_CONSENT__MULTIPLE_RELATIONSHIPS_SINGLE_PATIENT_INCLUDE_PERFORMER,
            )
        # Filtering
        elif performer_identifier == "9000000017":
            return check_for_consent_filtering(
                status,
                _include,
                GET_CONSENT__FILTERED_RELATIONSHIPS_STATUS_ACTIVE,
                GET_CONSENT__FILTERED_RELATIONSHIPS_STATUS_INACTIVE,
                GET_CONSENT__FILTERED_RELATIONSHIPS_STATUS_PROPOSED_ACTIVE,
            )

        elif performer_identifier == "9000000022":
            return check_for_consent_include_params(
                _include,
                GET_CONSENT__MULTIPLE_RELATIONSHIPS,
                GET_CONSENT__MULTIPLE_RELATIONSHIPS_INCLUDE_BOTH,
                GET_CONSENT__MULTIPLE_RELATIONSHIPS_INCLUDE_PATIENT,
                GET_CONSENT__MULTIPLE_RELATIONSHIPS_INCLUDE_PERFORMER,
            )
        # No relationships
        elif performer_identifier == "9000000025":
            return generate_response_from_example(GET_CONSENT__NO_RELATIONSHIPS, 200)
        else:
            logger.error("Performer identifier does not match examples")
            return generate_response_from_example(INVALIDATED_RESOURCE, 404)

    except Exception:
        logger.exception("An error occurred while processing the request")
        return generate_response_from_example(INTERNAL_SERVER_ERROR_EXAMPLE, 500)
