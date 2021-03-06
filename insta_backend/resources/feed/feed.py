import json
from flask import Blueprint, request, jsonify
from datetime import datetime
from insta_backend.extensions import redis_client, db
from insta_backend.models.post.post import PostMethods, Post
from insta_backend.models.user.friendship import FollowerMethods
from insta_backend.models.user.user import UserMethods
from insta_backend.utils import generate_user_from_auth_token

bp_feed = Blueprint("feed", __name__)


# Fetch followees posts from redis
@bp_feed.route('/', methods=['GET'])
def custom_feed():
    auth_token = request.headers.get('access_token')
    current_user = generate_user_from_auth_token(auth_token)
    #  HIT REDIS FOR ALL POSTS RELATED T
    followees = FollowerMethods.get_followees(current_user.id)
    posts = []
    for followee in followees:
        user = UserMethods.get_record_with_id(followee.followee_id)
        start_time = datetime.utcnow()
        user_posts = redis_client.lrange(user.username, 0, -1)
        print(datetime.utcnow() - start_time)
        for post in user_posts:
            posts.append(json.loads(post))
    return jsonify({"posts": posts})


# Fetch followees posts from database
@bp_feed.route('/feed', methods=['GET'])
def feed():
    auth_token = request.headers.get('access_token')
    current_user = generate_user_from_auth_token(auth_token)
    #  HIT REDIS FOR ALL POSTS RELATED TO
    followees = FollowerMethods.get_followees(current_user.id)
    posts = []
    for followee in followees:
        user = UserMethods.get_record_with_id(followee.followee_id)
        start_time = datetime.utcnow()
        user_posts = db.query(Post).filter(Post.user_id == user.id).all()
        print(datetime.utcnow() - start_time)
        for post in user_posts:
            posts.append(
                dict(
                    caption=post.caption,
                    image=post.image._public_url,
                    user_id=post.user_id
                )
            )
    return jsonify({"posts": posts})


# can be used by everyone anonymous so no authentication
@bp_feed.route('/explore/<page>', methods=['GET'])
def explore(page):
    sa_posts = PostMethods.get_latest_public_posts(
        page
    )
    next_posts_url = None
    prev_posts_url = None
    if sa_posts.has_next:
        next_posts_url = '/explore/' + page + 1
    if sa_posts.has_prev:
        prev_posts_url = '/explore/' + page - 1

    posts = dict()
    cnt = 1
    for sa_post in sa_posts.items:
        posts[cnt] = dict(sa_post)
        cnt += 1

    return jsonify({"posts": posts, "next_posts_url": next_posts_url,
                    "prev_posts_url": prev_posts_url})
