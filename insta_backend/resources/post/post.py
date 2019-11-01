# from flask import Blueprint, request
#
# from insta_backend.auth.auth import decode_auth_token
# from insta_backend.exceptions.custom_exceptions import NoResultFound
# from insta_backend.extensions import db
# from insta_backend.models.user.user import User, Entity
# from insta_backend.models.user.user_methods import FollowerMethods, UserMethods
#
# bp_posts = Blueprint("feed", __name__, url_prefix='/posts')
#
#
# @bp_user.route('/follow/<followee_username>', methods=['POST'])
# def follow(followee_username):
#     payload = decode_auth_token(
#         request.headers.get('access_token'),
#         Entity.USER.value
#     )
#     follower_username = payload.get('entity_id')
#     follower_user = UserMethods.get_user_by_username(follower_username)
#
#     followee_user = UserMethods.get_user_by_username(followee_username)
#     if followee_user is None:
#         raise NoResultFound(
#             'No user with username {username} found'.format(
#                 username=followee_username
#             )
#         )
#
#     if not FollowerMethods.is_following(follower_user.id, followee_user.id):
#         FollowerMethods.follow(follower_user.id, followee_user.id)
#
#     db.commit()
#     return {"message": "Success"}