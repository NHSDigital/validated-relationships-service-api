from logging import INFO, basicConfig, getLogger
from typing import Union

from flask import request

from .constants import (
    GET_QUESTIONNAIRE_RESPONSE__INVALID,
    GET_QUESTIONNAIRE_RESPONSE__MISSING,
    GET_QUESTIONNAIRE_RESPONSE__NOT_FOUND,
    GET_QUESTIONNAIRE_RESPONSE__SUCCESS,
    INTERNAL_SERVER_ERROR_EXAMPLE,
)
from .utils import generate_response_from_example

basicConfig(level=INFO, format="%(asctime)s - %(message)s")
logger = getLogger(__name__)


def get_questionnaire_response_response() -> Union[dict, tuple]:
    """Sandbox API for GET /QuestionnaireResponse

    Returns:
        Union[dict, tuple]: Response for GET /QuestionnaireResponse
    """
    try:
        access_request_uuid = request.args.get("accessRequestUUID")
        if access_request_uuid == "156e1560-e532-4e2a-85ad-5aeff03dc43e":
            return generate_response_from_example(GET_QUESTIONNAIRE_RESPONSE__SUCCESS, 200)
        elif access_request_uuid == "INVALID":
            return generate_response_from_example(GET_QUESTIONNAIRE_RESPONSE__INVALID, 400)
        elif access_request_uuid == "" or access_request_uuid is None:
            return generate_response_from_example(GET_QUESTIONNAIRE_RESPONSE__MISSING, 400)
        elif access_request_uuid == "60d09b82-f4bb-41f9-b41e-767999b4ac9b":
            return generate_response_from_example(GET_QUESTIONNAIRE_RESPONSE__NOT_FOUND, 404)
        else:
            raise ValueError("Invalid access request UUID")
    except Exception:
        logger.exception("GET questionnaire response failed")
        return generate_response_from_example(INTERNAL_SERVER_ERROR_EXAMPLE, 500)
