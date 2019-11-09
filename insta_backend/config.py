import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = os.environ.get('SECRET_KEY', os.urandom(24))
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'SECRET')
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'SQLALCHEMY_DATABASE_URI',
        default='postgresql://insta_user:insta_password@localhost:5432/insta'
    )
    DEPOT_MANAGER_CONFIG = {'depot.storage_path': '/static/media'}
    MAX_POSTS_PER_PAGE = os.environ.get("MAX_POSTS_PER_PAGE", "10")
    MAX_REDIS_CACHED_POSTS = os.environ.get('MAX_REDIS_CACHED_POSTS', "10")


class ProdConfig(Config):
    DEBUG = False
    DEPOT_MANAGER_CONFIG = {'depot.backend': 'depot.io.boto3.S3Storage',
                            'depot.access_key_id': os.environ.get(
                                'AWS_ACCESS_KEY',
                                None),
                            'depot.secret_access_key': os.environ.get(
                                'AWS_SECRET_KEY', None),
                            'depot.bucket': 'insta-backend-' +
                                            os.environ.get('INSTA_ENV').lower(),
                            'depot.region_name': 'ap-south-1'}


class DevConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'SQLALCHEMY_DATABASE_URI',
        default='postgresql://insta_user:insta_password@localhost:5432/insta'
    )

    DEPOT_MANAGER_CONFIG = {'depot.backend': 'depot.io.boto3.S3Storage',
                            'depot.access_key_id': os.environ.get(
                                'AWS_ACCESS_KEY',
                                None),
                            'depot.secret_access_key': os.environ.get(
                                'AWS_SECRET_KEY', None),
                            'depot.bucket': 'insta-backend-' +
                                            os.environ.get('INSTA_ENV').lower(),
                            'depot.region_name': 'ap-south-1'}


class TestConfig(Config):
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'SQLALCHEMY_DATABASE_URI',
        default='postgresql://insta_user:insta_password@localhost:5432'
                '/insta_test '
    )
