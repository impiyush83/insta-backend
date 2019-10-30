from flask import current_app as app, request
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError

from insta_backend.common.validators import request_data_validator
from insta_backend.exceptions.custom_exceptions import ResourceAlreadyPresent
from insta_backend.extensions import db
from insta_backend.models.user import User
from insta_backend.schemas.auth import signup_schema


class SignUp(Resource):

    def __init__(self):
        app.logger.info(
            'In the constructor of {}'.format(self.__class__.__name__))

    @request_data_validator(signup_schema)
    def post(self):
        """

        .. http:post::  /signup

            This api will be used to signup user

            **Example request**:

            {
                "username": "impiyush83",
                "password": "secret-password",
                "email": "nalawadepiyush@gmail.com",

            }

            .. sourcecode:: http

            POST  /signup  HTTP/1.1

            **Example response**:

            .. sourcecode:: http

            HTTP/1.1 200 OK
            Vary: Accept


        :statuscode 200: responses
        :statuscode 400: bad request error
        :statuscode 404: value error

        """
        request_data = request.json
        try:
            picture = 1
            user = User(display=picture, **request_data)
            db.add(user)
            db.commit()
        except IntegrityError:
            db.session.rollback()
            raise ResourceAlreadyPresent("User already registered")
        return {}