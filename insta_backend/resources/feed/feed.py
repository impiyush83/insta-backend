import json

from flask import Blueprint, request, jsonify

from insta_backend.extensions import redis_client
from insta_backend.models.post.post import PostMethods
from insta_backend.models.user.friendship import FollowerMethods
from insta_backend.models.user.user import UserMethods
from insta_backend.utils import generate_user_from_auth_token

bp_feed = Blueprint("feed", __name__)


@bp_feed.route('/', methods=['GET'])
def custom_feed():
    auth_token = request.headers.get('access_token')
    current_user = generate_user_from_auth_token(auth_token)
    #  HIT REDIS FOR ALL POSTS RELATED TO
    followees = FollowerMethods.get_followees(current_user.id)
    posts = []
    for followee in followees:
        user = UserMethods.get_record_with_id(followee.followee_id)
        user_posts = redis_client.lrange(user.username, 0, -1)
        for post in user_posts:
            posts.append(json.loads(post))
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
