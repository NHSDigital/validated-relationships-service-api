from flask import Flask

app = Flask(__name__)


@app.route("/hello_world", methods=["GET"])
def hello_world() -> dict:
    return {"message": "Hello, World!"}
