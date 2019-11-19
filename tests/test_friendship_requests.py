import pytest
from hamcrest import is_, assert_that

from insta_backend.models.user.friendship import Follower, FollowRequest
from insta_backend.views.friendship.friendship import accept_follow_requests, \
    send_follow_request, follow_public_user, unfollow_user
from tests.factories import UserFactory


class TestFriendshipRequests:
    @pytest.fixture(autouse=True)
    def setup(self, testapp, db):
        self.testapp = testapp
        self.db = db


    @staticmethod
    def create_and_save_user(db, status="public"):
        user = UserFactory(status=status)
        db.add(user)
        db.commit()
        return user

    def test_user_follows_and_unfollow_public_profile_user(self):
        public_user_1 = self.create_and_save_user(self.db, status="public")
        public_user_2 = self.create_and_save_user(self.db, status="public")
        follower_id = public_user_1.id
        followee_id = public_user_2.id
        follow_public_user(follower_id, followee_id)
        follow_entry = self.db.query(Follower).filter(
            Follower.follower_id == follower_id,
            Follower.followee_id == followee_id,
        ).first()
        assert_that(follow_entry.followee_id, is_(followee_id))
        assert_that(follow_entry.follower_id, is_(follower_id))

        unfollow_user(follower_id, followee_id)

        follow_entry = self.db.query(Follower).filter(
            Follower.follower_id == follower_id,
            Follower.followee_id == followee_id,
        ).first()

        assert_that(follow_entry, is_(None))

    def test_user_follows_and_unfollow_to_private_profile_user(self):
        private_user_1 = self.create_and_save_user(self.db, status="private")
        public_user_2 = self.create_and_save_user(self.db, status="public")
        follower_id = public_user_2.id
        followee_id = private_user_1.id
        send_follow_request(follower_id, followee_id)
        follow_request_entry = self.db.query(FollowRequest).filter(
            FollowRequest.follower_id == follower_id,
            FollowRequest.followee_id == followee_id,
        ).first()
        assert_that(follow_request_entry.followee_id, is_(followee_id))
        assert_that(follow_request_entry.follower_id, is_(follower_id))

        accept_follow_requests(follower_id, followee_id)
        follow_entry = self.db.query(Follower).filter(
            Follower.follower_id == follower_id,
            Follower.followee_id == followee_id,
        ).first()
        assert follow_entry.followee_id, is_(followee_id)
        assert follow_entry.follower_id, is_(follower_id)

        unfollow_user(follower_id, followee_id)

        follow_entry = self.db.query(Follower).filter(
            Follower.follower_id == follower_id,
            Follower.followee_id == followee_id,
        ).first()

        assert_that(follow_entry, is_(None))
