from flask import current_app as app, request
from flask_restful import Resource
from insta_backend.auth.auth import encode_auth_token
from insta_backend.common.validators import request_data_validator
from insta_backend.exceptions.custom_exceptions import NoResultFound
from insta_backend.models.user import User, Entity
from insta_backend.schemas.auth import login_schema


class Login(Resource):

    def __init__(self):
        app.logger.info(
            'In the constructor of {}'.format(self.__class__.__name__))

    @request_data_validator(login_schema)
    def post(self):
        """

        .. http:post::  /login

            This api will be used to login the user

            **Example request**:

            {
                "username": "impiyush83",
                "password": "secret-password"
            }

            .. sourcecode:: http

            POST  /login  HTTP/1.1

            **Example response**:

            {
                "auth_token": "jwt_token"
            }

            .. sourcecode:: http

            HTTP/1.1 200 OK
            Vary: Accept


        :statuscode 200: responses
        :statuscode 400: bad request error
        :statuscode 404: value error

        """
        request_data = request.json
        username = request_data.get('username')
        password = request_data.get('password')
        user = User.query.filter_by(username=username).first()
        if user is None or user.check_password(password):
            raise NoResultFound("User not found with the entered credentials")
        token = encode_auth_token(user.id, Entity.USER.value)
        return {"auth_token": token}
