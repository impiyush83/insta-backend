from flask import request, Blueprint, jsonify
from werkzeug.exceptions import NotFound

from insta_backend.auth.auth import encode_auth_token
from insta_backend.extensions import db
from insta_backend.models.user.user import User, Entity
from insta_backend.utils import check_encrypted_password
from insta_backend.views.auth.signup import process_signup

bp_auth = Blueprint("auth", __name__)


@bp_auth.route('/signin', methods=['GET'])
def login():
    request_data = request.json
    username = request_data.get('username')
    password = request_data.get('password')
    user = db.query(User).filter(User.username == username).first()
    if user is None or not check_encrypted_password(password, user.password):
        raise NotFound("User not found with the entered credentials")
    token = encode_auth_token(user.username, Entity.USER.value)
    return jsonify({"auth_token": token}), 200


@bp_auth.route('/signup', methods=['POST'])
def signup():
    request_data = request.json
    process_signup(request_data)
    db.commit()
    return jsonify({"message": "Success"}), 200
