from logging import INFO, basicConfig, getLogger
from typing import Union

from flask import request

from .constants import (
    INTERNAL_SERVER_ERROR_EXAMPLE,
    RELATED__LIST_RELATIONSHIP,
    RELATED__LIST_RELATIONSHIP_WITH_INCLUDE,
    RELATED__VERIFY_RELATIONSHIP_09,
    RELATED__VERIFY_RELATIONSHIP_09_WITH_INCLUDE,
    RELATED__VERIFY_RELATIONSHIP_25,
    RELATED__VERIFY_RELATIONSHIP_25_WITH_INCLUDE,
)
from .utils import (
    check_for_empty,
    check_for_get_related_person_errors,
    check_for_list,
    check_for_validate,
    generate_response_from_example,
    remove_system,
)

basicConfig(level=INFO, format="%(asctime)s - %(message)s")
logger = getLogger(__name__)


def get_related_person_response() -> Union[dict, tuple]:
    """Sandbox API for GET /RelatedPerson

    Returns:
        Union[dict, tuple]: Response for GET /RelatedPerson
    """
    try:
        # Check Headers
        if errors := check_for_get_related_person_errors(request):
            return errors

        identifier = remove_system(request.args.get("identifier"))
        patient_identifier = remove_system(request.args.get("patient:identifier"))
        include = request.args.get("_include")

        if empty := check_for_empty(identifier, patient_identifier):
            return empty

        # Successful request, select response
        if zero_nine := check_for_validate(
            "9000000009",
            identifier,
            patient_identifier,
            include,
            RELATED__VERIFY_RELATIONSHIP_09,
            RELATED__VERIFY_RELATIONSHIP_09_WITH_INCLUDE,
        ):
            return zero_nine

        if two_five := check_for_validate(
            "9000000025",
            identifier,
            patient_identifier,
            include,
            RELATED__VERIFY_RELATIONSHIP_25,
            RELATED__VERIFY_RELATIONSHIP_25_WITH_INCLUDE,
        ):
            return two_five

        if one_seven := check_for_list(
            "9000000017",
            identifier,
            include,
            RELATED__LIST_RELATIONSHIP,
            RELATED__LIST_RELATIONSHIP_WITH_INCLUDE,
        ):
            return one_seven

        raise ValueError("Invalid request")

    except Exception:
        logger.exception("GET related person failed")
        return generate_response_from_example(INTERNAL_SERVER_ERROR_EXAMPLE, 500)
