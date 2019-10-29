from flask import Flask

from insta_backend.api import restful_api
from insta_backend.extensions import db, migrate, jwt
from insta_backend.models import user, post


def create_app(config_object):
    app = Flask(__name__)
    app.config.from_object(config_object)
    register_extensions(app)
    register_shellcontext(app)
    restful_api(app)
    return app


def register_blueprints(app):
    pass


def register_extensions(app):
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)


def register_shellcontext(app):
    def shell_context():
        """Shell context objects."""
        return {
            'db': db,
            'User': user.User,
            'Follower': user.Follower,
            'Post': post.Post,
            'Comment': post.Comment,
            'Like': post.Like,
        }

    app.shell_context_processor(shell_context)
