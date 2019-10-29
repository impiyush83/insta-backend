import os
from datetime import datetime

from depot.fields.specialized.image import UploadedImageWithThumb
from depot.fields.sqlalchemy import UploadedFileField
from sqlalchemy import String, Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship, backref
import sqlalchemy as sa

from insta_backend.common.custom_types import PasswordType
from flask import Config
from insta_backend.database import Base, Model, Timestamp

config_name = 'insta_backend.config.{}Config'.format(
    os.environ.get('INSTA_ENV'))
config = Config('')
config.from_object(config_name)


class Follower(Base, Model, Timestamp):
    follower_id = Column(Integer, ForeignKey('user.id'))
    followee_id = Column(Integer, ForeignKey('user.id'))


follower = Follower.__table__


class User(Base, Model, Timestamp):
    email = Column(String(256), unique=True, index=True)
    display_picture = Column(
        UploadedFileField(upload_type=UploadedImageWithThumb))
    username = Column(String(256), unique=True, index=True)
    password = Column(PasswordType(schemes=config['HASH_SCHEMES']))
    photos = relationship('Post', backref='owner', lazy='dynamic')
    last_seen = Column(DateTime, default=datetime.utcnow)
    followed = relationship(
        'User', follower,
        primaryjoin=(follower.c.follower_id == id),
        secondaryjoin=(follower.c.followee_id == id),
        backref=backref('followers', lazy='dynamic'), lazy='dynamic')


@sa.event.listens_for(User, 'before_update', propagate=True)
def timestamp_before_update(mapper, connection, target):
    # When a model with a timestamp is updated; force update the updated
    # timestamp.
    target.updated = datetime.utcnow()
