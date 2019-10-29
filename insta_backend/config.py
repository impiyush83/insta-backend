import os

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    DEBUG = False
    TESTING = False
    CSRF_ENABLED = True
    SECRET_KEY = os.environ.get('SECRET_KEY', os.urandom(24))
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY', 'SECRET')


class ProdConfig(Config):
    DEBUG = False
    HASH_SCHEMES = ['plaintext']
    HASH_SCHEMES = ['bcrypt_sha256']

class DevConfig(Config):
    DEVELOPMENT = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'SQLALCHEMY_DATABASE_URI',
        default='postgresql://insta_user:insta_password@localhost:5432/insta'
    )
    HASH_SCHEMES = ['plaintext']


class TestConfig(Config):
    TESTING = True
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'SQLALCHEMY_DATABASE_URI',
        default='postgresql://insta_user:insta_password@localhost:5432'
                '/insta_test '
    )
    HASH_SCHEMES = ['plaintext']
