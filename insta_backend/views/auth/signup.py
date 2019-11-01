import os

from sqlalchemy.exc import IntegrityError

from insta_backend.exceptions.custom_exceptions import ResourceAlreadyPresent
from insta_backend.extensions import db
from insta_backend.models.user.user import UserMethods
from insta_backend.utils import encrypt_password


def process_signup(user_payload):
    try:
        # set default image
        current_directory = os.path.dirname(__file__)
        filename = os.path.join(
                current_directory,
                "../../static/images/default_profile_picture.png"
        )
        image = open(filename, "r+b")
        user_payload['password'] = encrypt_password(user_payload.get('password'))
        user_payload['display_picture'] = image
        UserMethods.create_record(**user_payload)
    except IntegrityError:
        db.session.rollback()
        raise ResourceAlreadyPresent("User already registered")
