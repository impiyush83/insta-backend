import os
from enum import Enum

from depot.fields.specialized.image import UploadedImageWithThumb
from depot.fields.sqlalchemy import UploadedFileField
from flask import Config
from sqlalchemy import String, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from insta_backend.database import Base, Model, Timestamp

config_name = 'insta_backend.config.{}Config'.format(
    os.environ.get('INSTA_ENV'))
config = Config('')
config.from_object(config_name)


class Follower(Base, Model, Timestamp):
    __tablename__ = "follower"
    follower_id = Column(Integer, ForeignKey('user.id'))
    followee_id = Column(Integer, ForeignKey('user.id'))


class User(Base, Model, Timestamp):
    __tablename__ = "user"
    email = Column(String(256), unique=True, index=True)
    display_picture = Column(
        UploadedFileField(upload_type=UploadedImageWithThumb))
    username = Column(String(256), unique=True, index=True)
    password = Column(String(256), nullable=False)
    posts = relationship('Post', backref='owner', lazy='dynamic')


class Entity(Enum):
    USER = 'user'
