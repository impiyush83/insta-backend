from enum import Enum
from depot.fields.specialized.image import UploadedImageWithThumb
from depot.fields.sqlalchemy import UploadedFileField
from sqlalchemy import String, Column, Integer, ForeignKey
from insta_backend.common.custom_types import EnumChoiceType
from insta_backend.database import Base, Model, Timestamp
from insta_backend.models.common import BaseModel


class PostType(Enum):
    PUBLIC = 'public'
    PRIVATE = 'private'


class LikeStatus(Enum):
    ACTIVE = 'active'
    INACTIVE = 'inactive'


class Post(Base, Model, Timestamp):
    __tablename__ = "post"
    caption = Column(String(256))
    image = Column(
        UploadedFileField(upload_type=UploadedImageWithThumb),
        nullable=False
    )
    user_id = Column(Integer, ForeignKey('user.id'))
    # if public display in common_feed and everyone, else only to subscribed
    status = Column(EnumChoiceType(PostType, impl=String(30)))


class Comment(Base, Model, Timestamp):
    __tablename__ = "comment"
    photo_id = Column(Integer, ForeignKey('post.id'))
    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(String(512), nullable=False)


class Like(Base, Model, Timestamp):
    __tablename__ = "like"
    photo_id = Column(Integer, ForeignKey('post.id'))
    user_id = Column(Integer, ForeignKey('user.id'))
    status = Column(
        EnumChoiceType(LikeStatus, impl=String(64)),
        default=LikeStatus.ACTIVE,
        nullable=False
    )


class PostMethods(BaseModel):
    model = Post

    pass
