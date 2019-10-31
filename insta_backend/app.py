from flask import Flask
from depot.manager import DepotManager
from insta_backend.extensions import db, migrate, jwt
from insta_backend.models.post import post
from insta_backend.models.user import user
from insta_backend.resources.auth.auth import bp_auth
from insta_backend.resources.user.follow import bp_user


def create_app(config_object):
    app = Flask(__name__)
    app.config.from_object(config_object)
    register_extensions(app)
    register_blueprints(app)
    register_shellcontext(app)
    # Configure a *default* depot to store files on MongoDB GridFS
    # print(app.config['DEPOT_MANAGER_CONFIG'])
    DepotManager.configure('default', app.config['DEPOT_MANAGER_CONFIG'])
    return app


def register_blueprints(app):
    app.register_blueprint(bp_auth)
    app.register_blueprint(bp_user)


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
''