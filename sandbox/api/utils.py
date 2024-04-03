from json import load


def get_response(file_name: str) -> dict:
    """Get response from file. Expected file content is a JSON."""
    with open(file_name, "r") as file:
        return load(file)
