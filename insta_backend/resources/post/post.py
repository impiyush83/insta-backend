from flask import Blueprint, request, jsonify
from werkzeug.exceptions import NotFound
from insta_backend.extensions import db
from insta_backend.models.post.post import PostMethods
from insta_backend.models.user.friendship import FollowerMethods
from insta_backend.models.user.user import UserMethods
from insta_backend.utils import generate_user_from_auth_token

bp_post = Blueprint("posts", __name__)


@bp_post.route('/posts', methods=['POST'])
def create_new_post():
    current_user = generate_user_from_auth_token(
        request.headers.get('access-token'))
    request_data = request.form
    image = request.files.getlist('image')[0]
    PostMethods.create_record(
        **dict(caption=request_data.get('caption'),
               image=image,
               user_id=current_user.id
               )
    )
    db.commit()
    return jsonify({"message": "Hurray your post is on its way !!"}), 200


@bp_post.route('/<username>/posts/<post_id>', methods=['GET'])
def get_user_post(username, post_id):
    current_user = generate_user_from_auth_token(
        request.headers.get('access-token'))
    post_user = UserMethods.get_user_by_username(username)
    if current_user.id == post_user.id or \
            post_user.status.value == "public" or \
            FollowerMethods.is_following(current_user.id, post_user.id):
        # send all data like comments, likes and post details
        if not PostMethods.get_record_with_id(post_id):
            raise NotFound("Post not found")
        post = PostMethods.get_record_with_id(post_id)
        comments = post.post_comments
        like_count = post.total_number_of_likes
        likes = post.post_likes
        response = dict(post=post, comments=comments, like_count=like_count,
                        likes=likes)
        return jsonify(response)
    else:
        return jsonify(
            dict(message="Profile is private! Follow to see the post !")
        ), 400
