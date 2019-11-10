from flask import request, jsonify, Blueprint
from werkzeug.exceptions import NotFound

from insta_backend.extensions import db
from insta_backend.models.post.post import PostMethods, LikeMethods
from insta_backend.models.user.friendship import FollowerMethods
from insta_backend.models.user.user import UserMethods
from insta_backend.utils import generate_user_from_auth_token

bp_like = Blueprint("likes", __name__)


@bp_like.route('/<username>/posts/<post_id>/like', methods=['POST'])
def like_action_on_post(username, post_id):
    current_user = generate_user_from_auth_token(
        request.headers.get('access-token'))
    post_user = UserMethods.get_user_by_username(username)
    if current_user.id == post_user.id or \
            post_user.status.value == "public" or \
            FollowerMethods.is_following(current_user.id, post_user.id):
        # send all data like comments, likes and post details
        if not PostMethods.get_record_with_id(post_id):
            raise NotFound("Post not found")
        LikeMethods.create_record(
            **dict(
                photo_id=post_id,
                user_id=current_user.id
            )
        )
        db.commit()
        return jsonify(dict(message="Successfully like the post"))
    else:
        return jsonify(
            dict(message="Profile is private! Follow to like the post !")
        ), 400


@bp_like.route('/<username>/posts/<post_id>/like', methods=['DELETE'])
def unlike_action_on_post(username, post_id):
    current_user = generate_user_from_auth_token(
        request.headers.get('access-token'))
    post_user = UserMethods.get_user_by_username(username)
    if current_user.id == post_user.id or \
            post_user.status.value == "public" or \
            FollowerMethods.is_following(current_user.id, post_user.id):
        # send all data like comments, likes and post details
        if not PostMethods.get_record_with_id(post_id):
            raise NotFound("Post not found")
        LikeMethods.delete_record(post_id, post_user.id)
        db.commit()
        return jsonify(dict(message="Successfully unliked the post"))
    else:
        return jsonify(
            dict(message="Profile is private! Follow to unlike the post !")
        ), 400
