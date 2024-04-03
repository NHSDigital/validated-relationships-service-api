from logging import INFO, basicConfig, getLogger
from typing import Union

from flask import Flask, request

from .utils import get_response

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
        if not request.args.get("identifier"):
            print(f"Args not found: {request.args}")
            return {"error": "Missing required parameter 'identifier'"}, 400

        if request.args.get("identifier") and request.args.get("patient"):
            return get_response(
                "./api/responses/RelatedPerson_identifier_and_patient.json"
            )
        elif request.args.get("identifier"):
            return get_response("./api/responses/RelatedPerson.json")
        else:
            raise Exception("Invalid request")

    except Exception as e:
        logger.error(e)
        return {"error": "Sandbox Internal Server Error"}, 500
