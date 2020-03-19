import inspect

from marshmallow import ValidationError

from src.common import Logger

log = Logger()


def has_no_empty_params(rule):
    defaults = rule.defaults if rule.defaults is not None else ()
    arguments = rule.arguments if rule.arguments is not None else ()
    return len(defaults) >= len(arguments)


def parse_request_using_schema(request, schema):
    func_name = inspect.stack()[1][3]
    log.info(f"Request received : {func_name}")
    request_body = request.get_json()
    validation_errors_dict = schema.validate(request_body)
    if len(validation_errors_dict) > 0:
        raise ValidationError(validation_errors_dict)
    data = schema.dump(request_body)
    log.info(f"{func_name} : {data}")
    return data
