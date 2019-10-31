import os

from sqlalchemy.exc import IntegrityError

from insta_backend.exceptions.custom_exceptions import ResourceAlreadyPresent
from insta_backend.extensions import db
from insta_backend.models.user.user import User
from insta_backend.utils import encrypt_password


def process_signup(user_payload):
    try:
        import pdb
        pdb.set_trace()
        # set default image
        current_directory = os.path.dirname(__file__)
        filename = os.path.join(
                current_directory,
                "../../static/images/default_profile_picture.png"
        )
        image = open(filename, "r+b")
        user = User()
        user.password = encrypt_password(user_payload.get('password'))
        user.display_picture = image
        user.email = user_payload.get('email')
        user.username = user_payload.get('username')
        db.add(user)
        db.commit()
    except IntegrityError:
        db.session.rollback()
        raise ResourceAlreadyPresent("User already registered")
