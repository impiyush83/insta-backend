from flask import Blueprint, request, jsonify
from werkzeug.exceptions import BadRequest, NotFound

from insta_backend.auth.auth import decode_auth_token
from insta_backend.extensions import db
from insta_backend.models.user.friendship import FollowerMethods
from insta_backend.models.user.user import Entity, UserMethods

bp_friendship = Blueprint("friendships", __name__, url_prefix='/friendships')


@bp_friendship.route('/<followee_username>/follow', methods=['POST'])
def follow(followee_username):
    payload = decode_auth_token(
        request.headers.get('access_token'),
        Entity.USER.value
    )
    follower_username = payload.get('entity_id')
    follower_user = UserMethods.get_user_by_username(follower_username)

    followee_user = UserMethods.get_user_by_username(followee_username)
    if followee_user is None:
        raise NotFound(
            'No user with username {username} found'.format(
                username=followee_username
            )
        )

    # same user id follow request
    if follower_user.id == followee_user.id:
        raise BadRequest('Request cannot be proceesed')

    # check if not follows
    if not FollowerMethods.is_following(follower_user.id, followee_user.id):
        FollowerMethods.follow(follower_user.id, followee_user.id)

    db.commit()
    return jsonify({"message": "Successfully followed"}), 200


@bp_friendship.route('<followee_username>/unfollow', methods=['POST'])
def unfollow(followee_username):
    payload = decode_auth_token(
        request.headers.get('access_token'),
        Entity.USER.value
    )
    follower_username = payload.get('entity_id')
    follower_user = UserMethods.get_user_by_username(follower_username)

    followee_user = UserMethods.get_user_by_username(followee_username)
    if followee_user is None:
        raise NotFound(
            'No user with username {username} found'.format(
                username=followee_username
            )
        )
    # same user id unfollow request
    if follower_user.id == followee_user.id:
        raise BadRequest('Request cannot be proceesed')

    # check if it follows
    if FollowerMethods.is_following(follower_user.id, followee_user.id):
        FollowerMethods.unfollow(follower_user.id, followee_user.id)

    db.commit()
    return jsonify({"message": "Successfully unfollowed"}), 200
