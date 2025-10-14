from logging import getLogger
from typing import Union

from flask import request

from .constants import (
    INTERNAL_SERVER_ERROR_EXAMPLE,
    GET_CONSENT__SINGLE_CONSENTING_ADULT_RELATIONSHIP,
    GET_CONSENT__SINGLE_CONSENTING_ADULT_RELATIONSHIP_INCLUDE_BOTH,
    GET_CONSENT__SINGLE_CONSENTING_ADULT_RELATIONSHIP_INCLUDE_PATIENT,
    GET_CONSENT__SINGLE_CONSENTING_ADULT_RELATIONSHIP_INCLUDE_PERFORMER,
    GET_CONSENT__SINGLE_MOTHER_CHILD_RELATIONSHIP,
    GET_CONSENT__SINGLE_MOTHER_CHILD_RELATIONSHIP_INCLUDE_BOTH,
    GET_CONSENT__SINGLE_MOTHER_CHILD_RELATIONSHIP_INCLUDE_PATIENT,
    GET_CONSENT__SINGLE_MOTHER_CHILD_RELATIONSHIP_INCLUDE_PERFORMER,
    GET_CONSENT_BY_ID__INVALID_ID_ERROR,
    BAD_REQUEST_INCLUDE_PARAM_INVALID,
    INVALIDATED_RESOURCE,
)
from .utils import generate_response_from_example, check_for_consent_include_params

logger = getLogger(__name__)


def get_consent_by_id_response(identifier: str) -> Union[dict, tuple]:
    """Sandbox API for GET /Consent/{id}

    Returns:
        Union[dict, tuple]: Response for GET /Consent/{id}
    """
    try:
        params = request.args.to_dict()
        if "_include" not in params and len(params) > 0:
            return generate_response_from_example(
                BAD_REQUEST_INCLUDE_PARAM_INVALID, 422
            )
        else:
            _include = request.args.getlist("_include")

        if identifier == "74eed847-ca25-4e76-8cf2-f2c2d7842a7a":
            return check_for_consent_include_params(
                _include,
                GET_CONSENT__SINGLE_CONSENTING_ADULT_RELATIONSHIP,
                GET_CONSENT__SINGLE_CONSENTING_ADULT_RELATIONSHIP_INCLUDE_BOTH,
                GET_CONSENT__SINGLE_CONSENTING_ADULT_RELATIONSHIP_INCLUDE_PATIENT,
                GET_CONSENT__SINGLE_CONSENTING_ADULT_RELATIONSHIP_INCLUDE_PERFORMER,
            )
        elif identifier == "39df03a2-1b14-4d19-b1dc-d5d8cbf96948":
            return check_for_consent_include_params(
                _include,
                GET_CONSENT__SINGLE_MOTHER_CHILD_RELATIONSHIP,
                GET_CONSENT__SINGLE_MOTHER_CHILD_RELATIONSHIP_INCLUDE_BOTH,
                GET_CONSENT__SINGLE_MOTHER_CHILD_RELATIONSHIP_INCLUDE_PATIENT,
                GET_CONSENT__SINGLE_MOTHER_CHILD_RELATIONSHIP_INCLUDE_PERFORMER,
            )
        elif identifier == "a0922245-1072-40c3-8f4e-a7490c10d365":
            return generate_response_from_example(INVALIDATED_RESOURCE, 404)
        else:
            return generate_response_from_example(
                GET_CONSENT_BY_ID__INVALID_ID_ERROR, 400
            )

    except Exception:
        logger.exception("An error occurred while processing the request")
        return generate_response_from_example(INTERNAL_SERVER_ERROR_EXAMPLE, 500)
