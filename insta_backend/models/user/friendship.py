from sqlalchemy import Integer, ForeignKey

from insta_backend.database import Base, Model, Timestamp, Column
from insta_backend.extensions import db
from insta_backend.models.common import BaseModel


class Follower(Base, Model, Timestamp):
    __tablename__ = "follower"
    follower_id = Column(Integer, ForeignKey('user.id'))
    followee_id = Column(Integer, ForeignKey('user.id'))


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
