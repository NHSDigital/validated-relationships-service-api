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
    PATCH_CONSENT__MISSING_GRANTOR,
    PATCH_CONSENT__INVALID_GRANTOR_VALUE,
    PATCH_CONSENT__INVALID_GRANTOR_SYSTEM,
    PATCH_CONSENT__MISSING_GRANTOR_REFERENCE,
    PATCH_CONSENT__MISSING_GRANTOR_IDENTIFIER,
)
from .utils import generate_response_from_example

basicConfig(level=INFO, format="%(asctime)s - %(message)s")
logger = getLogger(__name__)


PATCH_CONSENT_RESPONSES = {
    "74eed847-ca25-4e76-8cf2-f2c2d7842a7a": (PATCH_CONSENT__SUCCESS, 200),
    "6b71ac92-baa3-4b76-b0f5-a601257e2722": (PATCH_CONSENT__SUCCESS, 200),
    "43003db8-ffcd-4bd6-ab2f-b49b9656f9e5": (PATCH_CONSENT__SUCCESS, 200),
    "849ea584-2318-471b-a24c-cee1b5ad0137": (PATCH_CONSENT__INVALID_PATCH_FORMAT, 400),
    "01abb0c5-b1ac-499d-9655-9cd0b8d3588f": (PATCH_CONSENT__INVALID_PATH, 400),
    "78c35330-fa2f-4934-a5dd-fff847f38de5": (PATCH_CONSENT__INVALID_STATUS_CODE, 422),
    "51fb4df5-815a-45cd-8427-04d6558336b7": (PATCH_CONSENT__INVALID_STATUS_REASON, 422),
    "7b7f47b8-96e5-43eb-b733-283bf1449f2c": (
        PATCH_CONSENT__INVALID_STATE_TRANSITION,
        422,
    ),
    "d4e8a6f2-1c3b-4a7e-9d2f-8b5c7e9f1a3d": (
        PATCH_CONSENT__MISSING_FREE_TEXT_FOR_OTHER,
        400,
    ),
    "a1b2c3d4-e5f6-4789-a0b1-c2d3e4f5a6b7": (PATCH_CONSENT__SUCCESS, 200),
    "b2c3d4e5-f6a7-4890-b1c2-d3e4f5a6b7c8": (PATCH_CONSENT__SUCCESS, 200),
    "c3d4e5f6-a7b8-4901-c2d3-e4f5a6b7c8d9": (PATCH_CONSENT__SUCCESS, 200),
    "90957744-b971-496e-b7c3-ab971868ce14": (PATCH_CONSENT__MISSING_GRANTOR, 400),
    "b68cbfc8-ccc2-48ad-b97b-b7410d773dc1": (PATCH_CONSENT__INVALID_GRANTOR_VALUE, 422),
    "fd189522-68e5-42dc-b44c-989be0eaa2bf": (
        PATCH_CONSENT__INVALID_GRANTOR_SYSTEM,
        422,
    ),
    "7e764160-38b6-41eb-9012-a3e476cbc517": (
        PATCH_CONSENT__MISSING_GRANTOR_REFERENCE,
        400,
    ),
    "faefd8c5-5e24-4415-8252-96e9241c7e78": (
        PATCH_CONSENT__MISSING_GRANTOR_IDENTIFIER,
        400,
    ),
}


def patch_consent_response(id: str) -> Union[dict, tuple]:
    """Sandbox API for PATCH /Consent

    Args:
        id (str): Consent id to be patched

    Returns:
        Union[dict, tuple]: Response for PATCH /Consent
    """
    try:
        logger.debug("Received request to PATCH consent")

        example, status_code = PATCH_CONSENT_RESPONSES.get(id, (PATCH_CONSENT__RESOURCE_NOT_FOUND, 404))
        return generate_response_from_example(example, status_code)

    except Exception:
        logger.exception("PATCH Consent failed")
        return generate_response_from_example(INTERNAL_SERVER_ERROR_EXAMPLE, 500)
