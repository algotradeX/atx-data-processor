"""Application error handlers."""
import json
import sys
import traceback

from flask import Blueprint, jsonify

errors = Blueprint("errors", __name__)


@errors.app_errorhandler(Exception)
def handle_error(error):
    message = ""
    try:
        message = error.description
    except Exception:
        message = str(error)
    data = None
    try:
        if error.data["messages"] is not None:
            data = json.loads(json.dumps(error.data["messages"]))
    except Exception:
        pass
    try:
        status_code = error.code
    except Exception:
        status_code = 500
    response = {
        "success": False,
        "error": {"type": error.__class__.__name__, "message": message, "data": data},
    }

    # et, ei, tb = sys.exc_info()
    print(traceback.print_stack())
    print(traceback.print_exc())

    return jsonify(response), status_code
