import datetime

import jwt
from flask import current_app as app

from insta_backend.exceptions.custom_exceptions import AuthenticationException


def encode_auth_token(uuid, entity):
    """
    Generates the Auth Token
    :param uuid: string
    :param entity: string
    :return: string
    """
    try:
        # jwt claims set
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
            'iat': datetime.datetime.utcnow(),
            'sub': uuid,
            'entity': entity
        }
        return jwt.encode(
            payload,
            app.config.get('SECRET_KEY'),
            algorithm='HS256'
        )
    except Exception as e:
        return e


def decode_auth_token(auth_token, entity):
    """
    Decodes the auth token
    :param auth_token: string
    :param entity: string
    :return: integer|string
    """
    try:
        payload = jwt.decode(
            auth_token,
            app.config.get('SECRET_KEY'),
            algorithms=['HS256']
        )
        if payload.get('entity') == entity:
            return payload
        raise AuthenticationException("Invalid authentication token")
    except jwt.ExpiredSignatureError as e:
        raise AuthenticationException("Expired authentication token")
    except jwt.InvalidTokenError:
        raise AuthenticationException("Invalid authentication token")
