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
    PATCH_CONSENT__INVALID_STATUS_REASON,
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

        if identifier == "c512b0db-6702-43ee-8c21-bbded2552da9":
            # Successful status update
            return generate_response_from_example(PATCH_CONSENT__SUCCESS, 200)

        elif identifier == "6b71ac92-baa3-4b76-b0f5-a601257e2722":
            # Successful end date for a role
            return generate_response_from_example(PATCH_CONSENT__SUCCESS, 200)

        elif identifier == "43003db8-ffcd-4bd6-ab2f-b49b9656f9e5":
            # Multiple valid changes
            return generate_response_from_example(PATCH_CONSENT__SUCCESS, 200)

        elif identifier == "849ea584-2318-471b-a24c-cee1b5ad0137":
            # Invalid patch format
            return generate_response_from_example(PATCH_CONSENT__INVALID_PATCH_FORMAT, 400)

        elif identifier == "01abb0c5-b1ac-499d-9655-9cd0b8d3588f":
            # Invalid path
            return generate_response_from_example(PATCH_CONSENT__INVALID_PATH, 400)

        elif identifier == "78c35330-fa2f-4934-a5dd-fff847f38de5":
            # Invalid status code
            return generate_response_from_example(PATCH_CONSENT__INVALID_STATUS_CODE, 422)

        elif identifier == "51fb4df5-815a-45cd-8427-04d6558336b7":
            # Invalid status reason
            return generate_response_from_example(PATCH_CONSENT__INVALID_STATUS_REASON, 422)

        elif identifier == "7b7f47b8-96e5-43eb-b733-283bf1449f2c":
            # Invalid state transition
            return generate_response_from_example(PATCH_CONSENT__INVALID_STATE_TRANSITION, 422)

        else:
            # Resource not found
            return generate_response_from_example(PATCH_CONSENT__RESOURCE_NOT_FOUND, 404)

    except Exception:
        # Handle any general error
        logger.exception("PATCH Consent failed")
        return generate_response_from_example(INTERNAL_SERVER_ERROR_EXAMPLE, 500)
