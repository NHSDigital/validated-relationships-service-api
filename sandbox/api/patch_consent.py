from logging import INFO, basicConfig, getLogger
from typing import Union

from .constants import (
    INTERNAL_SERVER_ERROR_EXAMPLE,
    PATCH_CONSENT__INVALID_PATCH_FORMAT,
    PATCH_CONSENT__INVALID_PATH,
    PATCH_CONSENT__INVALID_STATE_TRANSITION,
    PATCH_CONSENT__INVALID_STATUS_CODE,
    PATCH_CONSENT__RESOURCE_NOT_FOUND,
    PATCH_CONSENT__SUCCESS,
)
from .utils import generate_response_from_example

basicConfig(level=INFO, format="%(asctime)s - %(message)s")
logger = getLogger(__name__)


def patch_consent_response(identifier: str) -> Union[dict, tuple]:
    """Sandbox API for PATCH /Consent

    Args:
        identifier (str): Consent identifier to be patched

    Returns:
        Union[dict, tuple]: Response for PATCH /Consent
    """
    try:
        logger.debug("Received request to PATCH consent")
        # Validate body - validation is beyond the scope of the sandbox.
        # Assume all requests are valid

        if identifier == "c6f48e4d":
            # Successful status update
            return generate_response_from_example(PATCH_CONSENT__SUCCESS, 200)

        elif identifier == "0c56a594":
            # Successful end date for a role
            return generate_response_from_example(PATCH_CONSENT__SUCCESS, 200)

        elif identifier == "b02ea26c":
            # Multiple valid changes
            return generate_response_from_example(PATCH_CONSENT__SUCCESS, 200)

        elif identifier == "3a2679eb":
            # Invalid patch format
            return generate_response_from_example(PATCH_CONSENT__INVALID_PATCH_FORMAT, 400)

        elif identifier == "94df7c8f":
            # Invalid path
            return generate_response_from_example(PATCH_CONSENT__INVALID_PATH, 400)

        elif identifier == "2a7b736d":
            # Invalid status code
            return generate_response_from_example(PATCH_CONSENT__INVALID_STATUS_CODE, 422)

        elif identifier == "6fb4361b":
            # Invalid state transition
            return generate_response_from_example(PATCH_CONSENT__INVALID_STATE_TRANSITION, 422)

        else:
            # Resource not found
            return generate_response_from_example(PATCH_CONSENT__RESOURCE_NOT_FOUND, 404)

    except Exception:
        # Handle any general error
        logger.exception("PATCH Consent failed")
        return generate_response_from_example(INTERNAL_SERVER_ERROR_EXAMPLE, 500)
