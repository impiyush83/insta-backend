import datetime
import random
import string
import uuid
from decimal import Decimal
from functools import wraps
from flask import jsonify
from passlib.context import CryptContext
from insta_backend.auth.auth import decode_auth_token
from insta_backend.models.user.user import User, Entity, UserMethods

pwd_context = CryptContext(
    schemes=["pbkdf2_sha256"],
    default="pbkdf2_sha256",
    pbkdf2_sha256__default_rounds=30000
)

date_format = '%Y-%m-%d %H:%M:%S UTC'


def jwt_identity(payload):
    return User.get_by_id(payload)


def identity_loader(user):
    return user.id


def parse_date(date_str, _format=date_format):
    try:
        if date_str is None:
            return None
        date_time = datetime.strptime(date_str, _format)
    except ValueError:
        return None
    else:
        return date_time


def date_to_str(date):
    return date and date.strftime(date_format)


def parse_int(int_str):
    try:
        return int(int_str)
    except ValueError:
        return None
    except TypeError:
        return None


def parse_decimal(decimal_str):
    try:
        return Decimal(decimal_str)
    except ValueError:
        return None
    except TypeError:
        return None
    except:
        return None


def encrypt_password(password):
    return pwd_context.encrypt(password)


def check_encrypted_password(password, hashed):
    return pwd_context.verify(password, hashed)


def generate_uuid():
    return str(uuid.uuid4())


def secret_key_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


# overrides httpexception inbuilt to give a json respsonse
def get_http_exception_handler(app):
    """Overrides the default http exception handler to return JSON."""
    handle_http_exception = app.handle_http_exception

    @wraps(handle_http_exception)
    def ret_val(exception):
        exc = handle_http_exception(exception)
        return jsonify({'code': exc.code, 'message': exc.description}), exc.code

    return ret_val


def generate_user_from_auth_token(auth_token):
    payload = decode_auth_token(
        auth_token,
        Entity.USER.value
    )
    current_username = payload.get('entity_id')
    current_user = UserMethods.get_user_by_username(current_username)
    return current_user
