from insta_backend.extensions import db
from insta_backend.models.common import BaseModel
from insta_backend.models.user.user import User, Follower


class UserMethods(BaseModel):
    model = User

    @classmethod
    def get_user_by_username(cls, username):
        return db.query(cls.model).filter_by(username=username).first()


class FollowerMethods(BaseModel):
    model = Follower

    @classmethod
    def follow(cls, follower_id, followee_id):
        cls.create_record(
            **dict(
                followee_id=followee_id,
                follower_id=follower_id)
        )

    @classmethod
    def unfollow(cls, follower_id, followee_id):
        db.query(cls.model).filter(
            cls.model.follower_id == follower_id,
            cls.model.followee_id == followee_id
        ).delete()

    @classmethod
    def is_following(cls, follower_id, followee_id):
        entry = db.query(cls.model).filter(
            Follower.follower_id == follower_id,
            Follower.followee_id == followee_id
        ).first()
        if entry:
            return True
        return False
