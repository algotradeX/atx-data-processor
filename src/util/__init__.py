import inspect
from datetime import datetime

from marshmallow import ValidationError

from src.common import Logger

log = Logger()


def get_initial_create_time_dict():
    return {"createdTime": datetime.utcnow(), "updatedTime": datetime.utcnow()}


def get_update_time_dict():
    return {"updatedTime": datetime.utcnow()}


def has_no_empty_params(rule):
    defaults = rule.defaults if rule.defaults is not None else ()
    arguments = rule.arguments if rule.arguments is not None else ()
    return len(defaults) >= len(arguments)


def parse_request_using_schema(request, schema):
    func_name = inspect.stack()[1][3]
    log.info(f"Request received : {func_name}")
    request_body = request.get_json()
    validate_schema(request_body, schema)
    data = schema.dump(request_body)
    log.info(f"{func_name} : {data}")
    return data


def validate_and_dump_in_schema(obj, schema):
    validate_schema(obj, schema)
    return schema.dump(obj)


def validate_schema(obj, schema):
    validation_errors_dict = schema.validate(obj)
    if len(validation_errors_dict) > 0:
        raise ValidationError(validation_errors_dict)
