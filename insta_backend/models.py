import os

from flask import Config
from flask_migrate import Migrate
from sqlalchemy_wrapper import SQLAlchemy

config_name = 'insta_backend.config.{}Config'.format(
    os.environ.get('INSTA_ENV'))
config = Config("")
config.from_object(config_name)

isolation_level = 'SERIALIZABLE'
db = SQLAlchemy(
    uri=config['SQLALCHEMY_DATABASE_URI'],
    pool_pre_ping=True,
    # tests connections for liveness upon each checkout. By firing select 1;
    # query
    pool_timeout=30,
    # – number of seconds to wait before giving up on getting a connection
    # from the pool
)

migrate = Migrate(compare_type=True)
Model = db.Model

#   ADD TABLES

