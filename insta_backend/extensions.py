import os

import redis
from flask import Config
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from sqlalchemy_wrapper import SQLAlchemy

config_name = 'insta_backend.config.{}Config'.format(
    os.environ.get('INSTA_ENV'))
config = Config("")
config.from_object(config_name)

db = SQLAlchemy(uri=config['SQLALCHEMY_DATABASE_URI'])
migrate = Migrate(compare_type=True)
jwt = JWTManager()
redis_client = redis.Redis(host='localhost', port=6379, db=0)
