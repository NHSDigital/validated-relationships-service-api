from logging import INFO, basicConfig, getLogger
from typing import Union

from .constants import INTERNAL_SERVER_ERROR_EXAMPLE, POST_QUESTIONNAIRE_RESPONSE__SUCCESS
from .utils import generate_response_from_example

basicConfig(level=INFO, format="%(asctime)s - %(message)s")
logger = getLogger(__name__)


def post_questionnaire_response_response() -> Union[dict, tuple]:
    """Sandbox API for POST /QuestionnaireResponse

    Returns:
        Union[dict, tuple]: Response for POST /QuestionnaireResponse
    """
    try:
        return generate_response_from_example(POST_QUESTIONNAIRE_RESPONSE__SUCCESS, 200)
    except Exception:
        logger.exception("POST questionnaire response failed")
        return generate_response_from_example(INTERNAL_SERVER_ERROR_EXAMPLE, 500)
