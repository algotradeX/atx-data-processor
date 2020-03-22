"""Application error handlers."""
import json
import traceback
from functools import reduce

from flask import Blueprint, jsonify
from marshmallow import ValidationError
from psycopg2 import (
    InterfaceError,
    DatabaseError,
    DataError,
    OperationalError,
    IntegrityError,
    InternalError,
    ProgrammingError,
    NotSupportedError,
)

errors = Blueprint("errors", __name__)
db_err_list = [
    InterfaceError,
    DatabaseError,
    DataError,
    OperationalError,
    IntegrityError,
    InternalError,
    ProgrammingError,
    NotSupportedError,
]


@errors.app_errorhandler(Exception)
def handle_error(error):
    if reduce(lambda a, b: a and isinstance(error, b), db_err_list):
        response = {
            "success": False,
            "error": {
                "type": error.__class__.__name__,
                "message": str(error),
                "data": error.messages,
            },
        }
        status_code = 500
    elif isinstance(error, ValidationError):
        response = {
            "success": False,
            "error": {
                "type": error.__class__.__name__,
                "message": str(error),
                "data": error.messages,
            },
        }
        status_code = 400
    else:
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
            "error": {
                "type": error.__class__.__name__,
                "message": message,
                "data": data,
            },
        }

    # et, ei, tb = sys.exc_info()
    print(traceback.print_stack())
    print(traceback.print_exc())

    return jsonify(response), status_code
