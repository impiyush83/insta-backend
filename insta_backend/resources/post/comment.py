from flask import request, jsonify, Blueprint
from werkzeug.exceptions import NotFound

from insta_backend.extensions import db
from insta_backend.models.post.post import PostMethods, CommentMethods
from insta_backend.models.user.friendship import FollowerMethods
from insta_backend.models.user.user import UserMethods
from insta_backend.utils import generate_user_from_auth_token

bp_comment = Blueprint("comments", __name__)


@bp_comment.route('/<username>/posts/<post_id>/comment', methods=['POST'])
def comment_on_post(username, post_id):
    current_user = generate_user_from_auth_token(
        request.headers.get('access-token'))
    post_user = UserMethods.get_user_by_username(username)
    if current_user.id == post_user.id or \
            post_user.status.value == "public" or \
            FollowerMethods.is_following(current_user.id, post_user.id):
        # send all data like comments, likes and post details
        if not PostMethods.get_record_with_id(post_id):
            raise NotFound("Post not found")
        CommentMethods.create_record(
            **dict(
                photo_id=post_id,
                user_id=current_user.id,
                comment=request.get('comment')
            )
        )
        db.commit()
        return jsonify(dict(message="Successfully Commented on the post"))
    else:
        return jsonify(
            dict(message="Profile is private! Follow to comment on the post !")
        ), 400
