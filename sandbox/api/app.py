from flask import Flask
from .utils import get_response
from logging import getLogger, basicConfig, INFO
from typing import Union

app = Flask(__name__)
basicConfig(level=INFO, format="%(asctime)s - %(message)s")
logger = getLogger(__name__)


@app.route("/RelatedPerson", methods=["GET"])
def related_persons() -> Union[dict, tuple]:
    """Sandbox API for GET /RelatedPerson

    Returns:
        Union[dict, tuple]: Response for GET /RelatedPerson
    """

    try:
        return get_response("./api/responses/RelatedPerson_identifier_and_patient.json")
    except Exception as e:
        logger.error(e)
        return {"error": "Internal Server Error"}, 500
