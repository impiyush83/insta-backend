from flask import Flask
from flask_jwt_extended import JWTManager

from insta_backend.api import restful_api
from insta_backend.models import config_name, db, migrate


def create_app(config_object=config_name):
    app = Flask(__name__)
    app.config.from_object(config_object)
    restful_api(app)
    register_extensions(app)
    JWTManager(app)
    # register_blueprints(app)
    return app


def register_blueprints(app):
    pass


def register_extensions(app):
    db.init_app(app)
    migrate.init_app(app)
