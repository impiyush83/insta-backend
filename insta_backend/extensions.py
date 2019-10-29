from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from sqlalchemy_wrapper import SQLAlchemy

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()
