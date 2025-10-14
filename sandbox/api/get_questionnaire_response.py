from logging import INFO, basicConfig, getLogger
from typing import Union

from .constants import (
    GET_QUESTIONNAIRE_RESPONSE__INVALID,
    GET_QUESTIONNAIRE_RESPONSE__NOT_FOUND,
    GET_QUESTIONNAIRE_RESPONSE__SUCCESS,
    INTERNAL_SERVER_ERROR_EXAMPLE,
    METHOD_NOT_ALLOWED,
)
from .utils import generate_response_from_example

basicConfig(level=INFO, format="%(asctime)s - %(message)s")
logger = getLogger(__name__)


def get_questionnaire_response_response(access_request_id: str) -> Union[dict, tuple]:
    """Sandbox API for GET /QuestionnaireResponse/{id}

    Returns:
        Union[dict, tuple]: Response for GET /QuestionnaireResponse/{id}
    """
    try:
        if access_request_id == "156e1560-e532-4e2a-85ad-5aeff03dc43e":
            return generate_response_from_example(GET_QUESTIONNAIRE_RESPONSE__SUCCESS, 200)
        elif access_request_id == "INVALID":
            return generate_response_from_example(GET_QUESTIONNAIRE_RESPONSE__INVALID, 400)
        elif access_request_id == "" or access_request_id is None:
            return generate_response_from_example(METHOD_NOT_ALLOWED, 405)
        elif access_request_id == "60d09b82-f4bb-41f9-b41e-767999b4ac9b":
            return generate_response_from_example(GET_QUESTIONNAIRE_RESPONSE__NOT_FOUND, 404)
        else:
            raise ValueError("Invalid access request ID")
    except Exception:
        logger.exception("GET questionnaire response failed")
        return generate_response_from_example(INTERNAL_SERVER_ERROR_EXAMPLE, 500)
