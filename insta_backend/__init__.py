from flask import Flask
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from sqlalchemy_wrapper import SQLAlchemy
from insta_backend.models import models
from insta_backend.api import restful_api

db = SQLAlchemy()
migrate = Migrate(compare_type=True)
Model = db.Model


def create_app(config_object):
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
    migrate.init_app(app, db)
