from datetime import datetime
import inflection
import sqlalchemy as sa
from sqlalchemy import Integer, Column, String, ForeignKey
from sqlalchemy.ext.declarative import declared_attr

from insta_backend import Model


# COMMON TABLES

class Timestamp:
    created = sa.Column(sa.DateTime, default=datetime.utcnow, nullable=False,
                        index=True)
    updated = sa.Column(sa.DateTime, default=datetime.utcnow, nullable=False)


@sa.event.listens_for(Timestamp, 'before_update', propagate=True)
def timestamp_before_update(mapper, connection, target):
    # When a model with a timestamp is updated; force update the updated
    # timestamp.
    target.updated = datetime.utcnow()


class SurrogatePK:
    __table_args__ = {'extend_existing': True}

    id = Column(Integer, autoincrement=True, primary_key=True)


class HasTablename:
    @declared_attr
    def __tablename__(cls):
        return inflection.underscore(cls.__name__)


class Base(HasTablename, SurrogatePK):
    def update_attributes(self, dict):
        for name, value in list(dict.items()):
            setattr(self, name, value)

    def __repr__(self):
        return '<{model}({id})>'.format(model=self.__class__.__name__,
                                        id=self.id)


#  ACTUAL TABLES
class User(Base, Model, Timestamp):
    email = Column(String(256), unique=True, index=True)


class Follower(Base, Model, Timestamp):
    follower_id = Column(Integer, ForeignKey('user.id'))
    followee_id = Column(Integer, ForeignKey('user.id'))


class Post(Base, Model, Timestamp):
    text = Column(String(256))
    image_url = Column()
    user_id = Column(Integer, ForeignKey('user.id'))


class Comment(Base, Model, Timestamp):
    pass


class Likes(Base, Model, Timestamp):
    pass
