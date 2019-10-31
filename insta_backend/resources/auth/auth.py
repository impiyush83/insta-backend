from flask import request, Blueprint

from insta_backend.auth.auth import encode_auth_token
from insta_backend.exceptions.custom_exceptions import NoResultFound
from insta_backend.models.user.user import User, Entity
from insta_backend.views.auth.signup import process_signup

bp_auth = Blueprint("auth", __name__, url_prefix='/auth')


@bp_auth.route('/login', methods=['POST'])
def login():
    request_data = request.json
    username = request_data.get('username')
    password = request_data.get('password')
    user = User.query.filter_by(username=username).first()
    if user is None or user.check_password(password):
        raise NoResultFound("User not found with the entered credentials")
    token = encode_auth_token(user.id, Entity.USER.value)
    return {"auth_token": token}


@bp_auth.route('/signup', methods=['POST'])
def signup():
    request_data = request.json
    process_signup(request_data)
    return {"message": "Success"}
