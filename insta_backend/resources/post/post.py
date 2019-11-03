from flask import Blueprint, request, jsonify
from insta_backend.auth.auth import decode_auth_token
from insta_backend.extensions import db
from insta_backend.models.post.post import PostMethods
from insta_backend.models.user.user import Entity, UserMethods

bp_post = Blueprint("posts", __name__)


@bp_post.route('/post', methods=['POST'])
def create_new_post():
    payload = decode_auth_token(
        request.headers.get('access_token'),
        Entity.USER.value
    )
    username = payload.get('entity_id')
    current_user = UserMethods.get_user_by_username(username)
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
