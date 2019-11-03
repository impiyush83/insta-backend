from flask import Blueprint, request

from insta_backend.models.user.friendship import FollowerMethods
from insta_backend.models.user.user import UserMethods
from insta_backend.utils import generate_user_from_auth_token

bp_user = Blueprint("users", __name__)


@bp_user.route('/<username>', methods=['GET'])
def user_profile(username):
    current_user = generate_user_from_auth_token(
        request.headers.get('access-token'))
    profile_user = UserMethods.get_user_by_username(username)

    response = dict(
        name=profile_user.name,
        username=profile_user.username,
        display_picture=dict(profile_user.display_picture)
    )
    #  HATEOS CONCEPT USED FOR POSTS
    #  no circular checking
    if current_user.username != username:
        # check if following
        if FollowerMethods.is_following(current_user.id, profile_user.id):
            response['posts'] = profile_user.all_posts
    else:
        response['posts'] = profile_user.all_posts
    return response
