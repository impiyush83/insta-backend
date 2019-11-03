from flask import Blueprint, request, jsonify
from insta_backend.models.post.post import PostMethods

bp_feed = Blueprint("feed", __name__)


@bp_feed.route('/', methods=['GET'])
def custom_feed():
    auth_token = request.headers.get('access_token')
    # current_user = generate_user_from_auth_token(auth_token)
    # GET PAGINATED POSTS
    #  HIT REDIS FOR PAGE LIST
    pass


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
