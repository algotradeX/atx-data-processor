"""Application error handlers."""
import json
import traceback

from flask import Blueprint, jsonify
from marshmallow import ValidationError
from sqlalchemy import exc

errors = Blueprint("errors", __name__)


@errors.app_errorhandler(exc.IntegrityError)
@errors.app_errorhandler(exc.OperationalError)
def handle_db_exception(error):
    try:
        response = {
            "success": False,
            "error": {
                "type": error.__class__.__name__,
                "message": f"psycopg2 error code: {error.orig.pgcode}",
                "data": str(error.orig.pgerror),
            },
        }
        status_code = 400
        return jsonify(response), status_code
    except AttributeError:
        handle_error(error)
    except Exception:
        handle_error(error)


@errors.app_errorhandler(Exception)
def handle_error(error):
    if isinstance(error, ValidationError):
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
