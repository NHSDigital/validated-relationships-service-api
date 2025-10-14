from logging import INFO, basicConfig, getLogger
from typing import Union

from flask import request

from .constants import (
    INTERNAL_SERVER_ERROR_EXAMPLE,
    POST_QUESTIONNAIRE_RESPONSE__SUCCESS,
    POST_QUESTIONNAIRE_RESPONSE__DUPLICATE_RELATIONSHIP_ERROR,
)
from .utils import generate_response_from_example

QUESTIONNAIRE_RESPONSE_APP_BASE_PATH = (
    "https://sandbox.api.service.nhs.uk/validated-relationships/FHIR/R4/QuestionnaireResponse"
)
basicConfig(level=INFO, format="%(asctime)s - %(message)s")
logger = getLogger(__name__)


def post_questionnaire_response_response() -> Union[dict, tuple]:
    """Sandbox API for POST /QuestionnaireResponse

    Returns:
        Union[dict, tuple]: Response for POST /QuestionnaireResponse
    """
    try:
        logger.debug("Received request to POST questionnaire response")
        # Validate body - beyond the scope of sandbox - assume body is valid for scenario
        json = request.get_json()
        source_identifier = json.get("source", {}).get("identifier", {}).get("value")
        response = None

        # Successful questionnaire response
        if source_identifier in ["9000000009", "9000000017"]:
            header = {"location": f"{QUESTIONNAIRE_RESPONSE_APP_BASE_PATH}?ID=156e1560-e532-4e2a-85ad-5aeff03dc43e"}
            response = generate_response_from_example(POST_QUESTIONNAIRE_RESPONSE__SUCCESS, 200, headers=header)
        # Duplicate relationship
        elif source_identifier == "9000000049":
            response = generate_response_from_example(POST_QUESTIONNAIRE_RESPONSE__DUPLICATE_RELATIONSHIP_ERROR, 409)
        else:
            # Out of scope errors
            raise ValueError("Invalid Request")

        return response

    except Exception:
        logger.exception("POST questionnaire response failed")
        return generate_response_from_example(INTERNAL_SERVER_ERROR_EXAMPLE, 500)
