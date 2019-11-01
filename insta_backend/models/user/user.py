import os
from enum import Enum

from depot.fields.specialized.image import UploadedImageWithThumb
from depot.fields.sqlalchemy import UploadedFileField
from flask import Config
from sqlalchemy import String, Column
from sqlalchemy.orm import relationship

from insta_backend.common.custom_types import EnumChoiceType
from insta_backend.database import Base, Model, Timestamp
from insta_backend.extensions import db
from insta_backend.models.common import BaseModel

config_name = 'insta_backend.config.{}Config'.format(
    os.environ.get('INSTA_ENV'))
config = Config('')
config.from_object(config_name)


class UserType(Enum):
    PUBLIC = 'public'
    PRIVATE = 'private'


class User(Base, Model, Timestamp):
    __tablename__ = "user"
    email = Column(String(256), unique=True, index=True)
    display_picture = Column(
        UploadedFileField(upload_type=UploadedImageWithThumb))
    username = Column(String(256), unique=True, index=True)
    password = Column(String(256), nullable=False)
    # if public display in common_feed and everyone, else only to subscribed
    status = Column(EnumChoiceType(UserType, impl=String(30)))
    posts = relationship('Post', backref='owner', lazy='dynamic')


class Entity(Enum):
    USER = 'user'


class UserMethods(BaseModel):
    model = User

    @classmethod
    def get_user_by_username(cls, username):
        return db.query(cls.model).filter_by(username=username).first()
