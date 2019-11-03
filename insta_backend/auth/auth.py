import datetime

import jwt
from flask import current_app as app
from werkzeug.exceptions import Unauthorized


def encode_auth_token(entity_id, entity):
    """
    Generates the Auth Token
    :param entity_id: string
    :param entity: string
    :return: string
    """
    try:
        # jwt claims set
        payload = {
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
            'iat': datetime.datetime.utcnow(),
            'entity': entity,
            'entity_id': entity_id
        }
        return jwt.encode(
            payload,
            app.config.get('SECRET_KEY'),
            algorithm='HS256'
        ).decode('utf-8')
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
    except jwt.ExpiredSignatureError as e:
        raise Unauthorized("Expired authentication token")
    except jwt.InvalidTokenError:
        raise Unauthorized("Invalid authentication token")
