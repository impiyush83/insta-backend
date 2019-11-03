from flask import Flask
from depot.manager import DepotManager


from insta_backend.extensions import db, migrate, jwt
from insta_backend.models.post import post
from insta_backend.models.user import user, friendship
# Blueprints
from insta_backend.resources.auth.auth import bp_auth
from insta_backend.resources.feed.feed import bp_feed
from insta_backend.resources.post.post import bp_post
from insta_backend.resources.user.friendship import bp_friendship, bp_requestors
from insta_backend.resources.user.user import bp_user
from insta_backend.utils import get_http_exception_handler


def create_app(config_object):
    app = Flask(__name__)
    app.config.from_object(config_object)
    register_extensions(app)
    register_blueprints(app)
    register_shellcontext(app)
    # Configure a *default* depot to store files on MongoDB GridFS
    # print(app.config['DEPOT_MANAGER_CONFIG'])
    DepotManager.configure('default', app.config['DEPOT_MANAGER_CONFIG'])

    # Override the HTTP exception handler.
    # magic snippet
    app.handle_http_exception = get_http_exception_handler(app)

    return app


def register_blueprints(app):
    app.register_blueprint(bp_auth)
    app.register_blueprint(bp_friendship)
    app.register_blueprint(bp_post)
    app.register_blueprint(bp_feed)
    app.register_blueprint(bp_user)
    app.register_blueprint(bp_requestors)


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
            'Follower': friendship.Follower,
            'Post': post.Post,
            'Comment': post.Comment,
            'Like': post.Like,
            'FollowRequests': friendship.FollowRequest
        }

    app.shell_context_processor(shell_context)


''
