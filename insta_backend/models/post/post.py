from depot.fields.sqlalchemy import UploadedFileField
from sqlalchemy import String, Column, Integer, ForeignKey

from insta_backend.database import Base, Model, Timestamp
from insta_backend.extensions import db
from insta_backend.models.common import BaseModel


class Post(Base, Model, Timestamp):
    __tablename__ = "post"
    caption = Column(String(256))
    image = Column(
        UploadedFileField(),
        nullable=False
    )
    user_id = Column(Integer, ForeignKey('user.id'))


class Comment(Base, Model, Timestamp):
    __tablename__ = "comment"
    photo_id = Column(Integer, ForeignKey('post.id'))
    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(String(512), nullable=False)


class Like(Base, Model, Timestamp):
    __tablename__ = "like"
    photo_id = Column(Integer, ForeignKey('post.id'))
    user_id = Column(Integer, ForeignKey('user.id'))


class PostMethods(BaseModel):
    model = Post

    @classmethod
    def get_latest_public_posts(cls, page):
        page = int(page)
        # gives 10 results as default is 10 in paginate method
        return db.query(Post).order_by(Post.created.desc()).paginate(
            page=page)
