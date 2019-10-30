import os
from datetime import datetime
from enum import Enum

from depot.fields.specialized.image import UploadedImageWithThumb
from depot.fields.sqlalchemy import UploadedFileField
from flask import Config
from sqlalchemy import String, Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship, backref

from insta_backend.common.custom_types import PasswordType
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
    followed = relationship(
        'User', follower,
        primaryjoin=(follower.c.follower_id == id),
        secondaryjoin=(follower.c.followee_id == id),
        backref=backref('follower', lazy='dynamic'), lazy='dynamic')


class Entity(Enum):
    USER = 'user'
