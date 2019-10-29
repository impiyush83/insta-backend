from functools import wraps
from flask import request, jsonify
from insta_backend.exceptions.custom_exceptions import \
    RequestValidationException
from cerberus import Validator as CerberusValidator
from insta_backend.utils import parse_date, parse_int, parse_decimal


class Validator(CerberusValidator):

    def __init__(self, *args, **kwargs):
        if 'additional_context' in kwargs:
            self.additional_context = kwargs['additional_context']
        super(Validator, self).__init__(*args, **kwargs)

    @staticmethod
    def _validate_type_unicode(value):
        return True if type(value) is str else False

    @staticmethod
    def _validate_type_utc_date(value):
        date_value = parse_date(value)
        return True if date_value else False

    @staticmethod
    def _validate_type_integer_string(value):
        integer_value = parse_int(value)
        return True if integer_value is not None else False

    @staticmethod
    def _validate_type_decimal_string(value):
        decimal_value = parse_decimal(value)
        return True if decimal_value is not None else False


def request_data_validator(schema):
    def decorator(func):
        @wraps(func)
        def validate(*args, **kwargs):
            validator = Validator(schema)
            if validator.validate(request.json):
                return func(*args, **kwargs)
            else:
                raise RequestValidationException(jsonify(validator.errors))
        return validate
    return decorator
