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
    PATCH_CONSENT__MISSING_FREE_TEXT_FOR_OTHER,
    PATCH_CONSENT__MISSING_GRANTOR_FOR_ACTIVE,
)
from .utils import generate_response_from_example

basicConfig(level=INFO, format="%(asctime)s - %(message)s")
logger = getLogger(__name__)


def patch_consent_response(id: str) -> Union[dict, tuple]:
    """Sandbox API for PATCH /Consent

    Args:
        id (str): Consent id to be patched

    Returns:
        Union[dict, tuple]: Response for PATCH /Consent
    """
    try:
        logger.debug("Received request to PATCH consent")
        # Validate body - validation is beyond the scope of the sandbox.
        # Assume all requests are valid

        if id == "74eed847-ca25-4e76-8cf2-f2c2d7842a7a":
            # Successful status update
            return generate_response_from_example(PATCH_CONSENT__SUCCESS, 200)

        elif id == "6b71ac92-baa3-4b76-b0f5-a601257e2722":
            # Successful end date for a role
            return generate_response_from_example(PATCH_CONSENT__SUCCESS, 200)

        elif id == "43003db8-ffcd-4bd6-ab2f-b49b9656f9e5":
            # Multiple valid changes
            return generate_response_from_example(PATCH_CONSENT__SUCCESS, 200)

        elif id == "849ea584-2318-471b-a24c-cee1b5ad0137":
            # Invalid patch format
            return generate_response_from_example(PATCH_CONSENT__INVALID_PATCH_FORMAT, 400)

        elif id == "01abb0c5-b1ac-499d-9655-9cd0b8d3588f":
            # Invalid path
            return generate_response_from_example(PATCH_CONSENT__INVALID_PATH, 400)

        elif id == "78c35330-fa2f-4934-a5dd-fff847f38de5":
            # Invalid status code
            return generate_response_from_example(PATCH_CONSENT__INVALID_STATUS_CODE, 422)

        elif id == "51fb4df5-815a-45cd-8427-04d6558336b7":
            # Invalid status reason
            return generate_response_from_example(PATCH_CONSENT__INVALID_STATUS_REASON, 422)

        elif id == "7b7f47b8-96e5-43eb-b733-283bf1449f2c":
            # Invalid state transition
            return generate_response_from_example(PATCH_CONSENT__INVALID_STATE_TRANSITION, 422)

        # Mandatory free text for OTHER reason codes
        elif id == "d4e8a6f2-1c3b-4a7e-9d2f-8b5c7e9f1a3d":
            # Missing free text for OTHER reason code (should fail)
            return generate_response_from_example(PATCH_CONSENT__MISSING_FREE_TEXT_FOR_OTHER, 400)

        elif id == "a1b2c3d4-e5f6-4789-a0b1-c2d3e4f5a6b7":
            # Valid OTHER reason code WITH free text (should succeed)
            return generate_response_from_example(PATCH_CONSENT__SUCCESS, 200)

        # Optional free text for non-OTHER reason codes
        elif id == "b2c3d4e5-f6a7-4890-b1c2-d3e4f5a6b7c8":
            # Non-OTHER reason code WITHOUT free text (should succeed)
            return generate_response_from_example(PATCH_CONSENT__SUCCESS, 200)

        elif id == "c3d4e5f6-a7b8-4901-c2d3-e4f5a6b7c8d9":
            # Non-OTHER reason code WITH free text (should succeed)
            return generate_response_from_example(PATCH_CONSENT__SUCCESS, 200)

        elif id == "90957744-b971-496e-b7c3-ab971868ce14":
            # PATCH to activate proxy role without providing grantor extension
            return generate_response_from_example(PATCH_CONSENT__MISSING_GRANTOR_FOR_ACTIVE, 400)

        else:
            # Resource not found
            return generate_response_from_example(PATCH_CONSENT__RESOURCE_NOT_FOUND, 404)

    except Exception:
        # Handle any general error
        logger.exception("PATCH Consent failed")
        return generate_response_from_example(INTERNAL_SERVER_ERROR_EXAMPLE, 500)
