from flask import Blueprint, request, jsonify
from werkzeug.exceptions import BadRequest, NotFound
from insta_backend.extensions import db
from insta_backend.models.user.friendship import FollowerMethods, \
    FollowRequestMethods
from insta_backend.models.user.user import UserMethods
from insta_backend.utils import generate_user_from_auth_token
from insta_backend.views.friendship.friendship import accept_follow_requests, \
    decline_follow_requests, send_follow_request, follow_public_user, \
    unfollow_user

bp_friendship = Blueprint("friendships", __name__, url_prefix='/friendships')
bp_requestors = Blueprint("requestors", __name__)


@bp_friendship.route('/<followee_username>/follow', methods=['POST'])
def follow(followee_username):
    follower_user = generate_user_from_auth_token(
        request.headers.get('access-token'))
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
        if followee_user.status.value == "public":
            follow_public_user(follower_user.id, followee_user.id)
            db.commit()
            return jsonify({"message": "Successfully followed"}), 200
        else:
            send_follow_request(follower_user.id,
                                followee_user.id)
            db.commit()
            return jsonify({"message": "Follow request sent"}), 200


@bp_friendship.route('<followee_username>/unfollow', methods=['POST'])
def unfollow(followee_username):
    follower_user = generate_user_from_auth_token(
        request.headers.get('access-token'))
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
        unfollow_user(follower_user.id, followee_user.id)

    db.commit()
    return jsonify({"message": "Successfully unfollowed"}), 200


@bp_requestors.route('/requesters', methods=['GET'])
def follow_requests():
    current_user = generate_user_from_auth_token(
        request.headers.get('access-token'))
    requestors = FollowRequestMethods.get_follow_requests(current_user.id)
    request_list = []
    # HATEOS CONCEPT USAGE
    for request_item in requestors:
        request_list.append(
            dict(
                requestor_id=request_item.follower_id,
                follow_accept_url='/friendships/request/accept/' + str(
                    request_item.follower_id),
                follow_decline_url='/friendships/request/decline/' + str(
                    request_item.follower_id)
            )
        )
    response = dict(requestors=request_list)
    return jsonify(response), 200


@bp_friendship.route('/request/accept/<follower_id>', methods=['POST'])
def accept_follow_request(follower_id):
    followee_user = generate_user_from_auth_token(
        request.headers.get('access-token'))
    accept_follow_requests(follower_id, followee_user.id)
    db.commit()
    return jsonify({"message": "Follow request accepted"}), 200


@bp_friendship.route('/request/decline/<follower_id>', methods=['POST'])
def decline_follow_request(follower_id):
    followee_user = generate_user_from_auth_token(
        request.headers.get('access-token'))
    decline_follow_requests(follower_id, followee_user.id)
    db.commit()
    return jsonify({"message": "Follow request declined"}), 200
