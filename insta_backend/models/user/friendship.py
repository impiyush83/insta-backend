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

    @classmethod
    def get_followees(cls, user_id):
        return db.query(cls.model).filter(Follower.follower_id == user_id).all()




class FollowRequest(Base, Model, Timestamp):
    __tablename__ = "follow_request"

    follower_id = Column(Integer, ForeignKey('user.id'))
    followee_id = Column(Integer, ForeignKey('user.id'))


class FollowRequestMethods(BaseModel):
    model = FollowRequest

    @classmethod
    def send_follow_request(cls, follower_id, followee_id):
        cls.create_record(
            **dict(
                followee_id=followee_id,
                follower_id=follower_id)
        )

    @classmethod
    def get_follow_requests(cls, followee_id):
        return db.query(cls.model).filter(
            cls.model.followee_id == followee_id).all()

    @classmethod
    def remove_request(cls, follower_id, followee_id):
        db.query(cls.model).filter(
            cls.model.followee_id == followee_id,
            cls.model.follower_id == follower_id
        ).delete()
