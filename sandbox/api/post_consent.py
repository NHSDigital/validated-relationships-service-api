from logging import INFO, basicConfig, getLogger
from typing import Union

from flask import request

from .constants import (
    INTERNAL_SERVER_ERROR_EXAMPLE,
    POST_CONSENT__DUPLICATE_RELATIONSHIP_ERROR,
    POST_CONSENT__PERFORMER_IDENTIFIER_ERROR,
    POST_CONSENT__SUCCESS,
    POST_CONSENT__MISSING_FREE_TEXT_FOR_OTHER,
)
from .utils import generate_response_from_example

CONSENT_APP_BASE_PATH = "https://sandbox.api.service.nhs.uk/validated-relationships/FHIR/R4/Consent"
basicConfig(level=INFO, format="%(asctime)s - %(message)s")
logger = getLogger(__name__)


def post_consent_response() -> Union[dict, tuple]:
    """Sandbox API for POST /Consent

    Returns:
        Union[dict, tuple]: Response for POST /Consent
    """
    try:
        logger.debug("Received request to POST consent")
        # Validate body - beyond the scope of sandbox - assume body is valid for scenario
        json = request.get_json()
        patient_identifier = json["performer"][0]["identifier"]["value"]
        response = None

        # Successful parent-child proxy creation
        # Successful adult-adult proxy creation
        if patient_identifier == "9000000009" or patient_identifier == "9000000017":
            header = {"location": f"{CONSENT_APP_BASE_PATH}/90b9863e-e33c-4895-a333-fd0ea0e23205"}
            response = generate_response_from_example(POST_CONSENT__SUCCESS, 201, headers=header)

        # Duplicate relationship
        elif patient_identifier == "9000000049":
            response = generate_response_from_example(POST_CONSENT__DUPLICATE_RELATIONSHIP_ERROR, 409)

        # Invalid performer NHS number
        elif patient_identifier == "9000000000":
            response = generate_response_from_example(POST_CONSENT__PERFORMER_IDENTIFIER_ERROR, 422)

        elif patient_identifier == "9000000050":
            # Missing free text for OTHER reason code (should fail)
            response = generate_response_from_example(POST_CONSENT__MISSING_FREE_TEXT_FOR_OTHER, 400)

        elif patient_identifier == "9000000051":
            # Valid OTHER reason code WITH free text (should succeed)
            header = {"location": f"{CONSENT_APP_BASE_PATH}/a1b2c3d4-e5f6-4789-a0b1-c2d3e4f5a6b7"}
            response = generate_response_from_example(POST_CONSENT__SUCCESS, 201, headers=header)

            # Optional free text for non-OTHER reason codes
        elif patient_identifier == "9000000052":
            # Non-OTHER reason code WITHOUT free text (should succeed)
            header = {"location": f"{CONSENT_APP_BASE_PATH}/b2c3d4e5-f6a7-4890-b1c2-d3e4f5a6b7c8"}
            response = generate_response_from_example(POST_CONSENT__SUCCESS, 201, headers=header)

        elif patient_identifier == "9000000053":
            # Non-OTHER reason code WITH free text (should succeed)
            header = {"location": f"{CONSENT_APP_BASE_PATH}/c3d4e5f6-a7b8-4901-c2d3-e4f5a6b7c8d9"}
            response = generate_response_from_example(POST_CONSENT__SUCCESS, 201, headers=header)

        else:
            # Out of scope errors
            raise ValueError("Invalid Request")

        return response

    except Exception:
        # Handle any general error
        logger.exception("POST Consent failed")
        return generate_response_from_example(INTERNAL_SERVER_ERROR_EXAMPLE, 500)
