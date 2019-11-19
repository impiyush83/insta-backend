from insta_backend.models.user.friendship import FollowerMethods, \
    FollowRequestMethods


def accept_follow_requests(follower_id, followee_id):
    if not FollowerMethods.is_following(follower_id, followee_id):
        FollowRequestMethods.remove_request(follower_id, followee_id)
        FollowerMethods.follow(follower_id, followee_id)


def decline_follow_requests(follower_id, followee_id):
    FollowRequestMethods.remove_request(follower_id, followee_id)


def send_follow_request(follower_id, followee_id):
    FollowRequestMethods.send_follow_request(follower_id, followee_id)


def follow_public_user(follower_id, followee_id):
    FollowerMethods.follow(follower_id, followee_id)


def unfollow_user(follower_id, followee_id):
    FollowerMethods.unfollow(follower_id, followee_id)
