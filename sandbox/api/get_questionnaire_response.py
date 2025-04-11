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
        reference_code = request.args.get("referenceCode")
        if reference_code == "19318ZGLAB":
            return generate_response_from_example(GET_QUESTIONNAIRE_RESPONSE__SUCCESS, 200)
        elif reference_code == "INVALID":
            return generate_response_from_example(GET_QUESTIONNAIRE_RESPONSE__INVALID, 400)
        elif reference_code == "" or reference_code is None:
            return generate_response_from_example(GET_QUESTIONNAIRE_RESPONSE__MISSING, 404)
        elif reference_code == "ABC123XY":
            return generate_response_from_example(GET_QUESTIONNAIRE_RESPONSE__NOT_FOUND, 404)
        else:
            raise ValueError("Invalid reference code")
    except Exception:
        logger.exception("GET questionnaire response failed")
        return generate_response_from_example(INTERNAL_SERVER_ERROR_EXAMPLE, 500)
